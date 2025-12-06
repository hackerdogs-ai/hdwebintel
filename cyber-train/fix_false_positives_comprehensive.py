#!/usr/bin/env python3
"""
Comprehensive script to fix false positives in training data.
Fixes TOOL, REPOSITORY, DATE, DOMAIN, and EMAIL_ADDRESS false positives.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import List, Tuple, Dict
import shutil
from datetime import datetime

# Common words that should NOT be TOOL entities
COMMON_WORDS_NOT_TOOL = {
    "csrf", "javascript", "base64", "json", "xml", "html", "css", "python",
    "debunk", "relative", "absolute", "find", "extract", "url", "import",
    "os", "found", "detected", "check", "verify", "analyze", "investigate",
    "scan", "monitor", "track", "report", "generate", "create", "update",
    "delete", "review", "audit", "manage", "implement", "deploy", "enable",
    "ensure", "identify", "assess", "evaluate", "plan", "design", "configure"
}

# URL patterns (should be URL, not REPOSITORY)
URL_PATTERNS = [
    r'https?://[^\s]+',
    r'ftp://[^\s]+',
    r'www\.[^\s]+',
    r'[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?',
]

# File path patterns (should be FILE_PATH, not DATE)
FILE_PATH_PATTERNS = [
    r'[A-Z]:\\[^\s]+',  # Windows: C:\path\to\file
    r'/[^\s]+',  # Unix: /path/to/file
    r'\\\\.*',  # UNC: \\server\share
    r'~/[^\s]+',  # Home: ~/path/to/file
]

# Date patterns (should be DATE, not FILE_PATH)
DATE_PATTERNS = [
    r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
    r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
    r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
    r'\d{1,2}/\d{1,2}/\d{4}',  # M/D/YYYY
    r'[A-Z][a-z]+ \d{1,2}, \d{4}',  # January 1, 2024
]

# Domain validation
DOMAIN_PATTERN = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$')

# Email validation
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def is_url(text: str) -> bool:
    """Check if text is a URL."""
    text = text.strip()
    for pattern in URL_PATTERNS:
        if re.match(pattern, text, re.IGNORECASE):
            return True
    return False


def is_file_path(text: str) -> bool:
    """Check if text is a file path."""
    text = text.strip()
    for pattern in FILE_PATH_PATTERNS:
        if re.match(pattern, text):
            return True
    return False


def is_date(text: str) -> bool:
    """Check if text is a date."""
    text = text.strip()
    for pattern in DATE_PATTERNS:
        if re.match(pattern, text):
            return True
    return False


def is_valid_domain(text: str) -> bool:
    """Check if text is a valid domain."""
    text = text.strip().lower()
    # Remove protocol if present
    text = re.sub(r'^https?://', '', text)
    text = re.sub(r'^www\.', '', text)
    # Remove path if present
    text = text.split('/')[0]
    return bool(DOMAIN_PATTERN.match(text))


def is_valid_email(text: str) -> bool:
    """Check if text is a valid email."""
    text = text.strip()
    return bool(EMAIL_PATTERN.match(text))


def fix_entities_in_text(text: str, entities: List[List]) -> Tuple[List[List], Dict]:
    """
    Fix false positive entities in a text.
    
    Returns:
        (fixed_entities, stats)
    """
    stats = defaultdict(int)
    fixed_entities = []
    
    for start, end, label in entities:
        entity_text = text[start:end].strip()
        entity_lower = entity_text.lower()
        
        # Fix TOOL false positives
        if label == "TOOL":
            if entity_lower in COMMON_WORDS_NOT_TOOL:
                stats['removed_tool'] += 1
                continue
            # Check if it's actually a URL
            if is_url(entity_text):
                stats['tool_to_url'] += 1
                fixed_entities.append([start, end, "URL"])
                continue
            # Check if it's actually a domain
            if is_valid_domain(entity_text):
                stats['tool_to_domain'] += 1
                fixed_entities.append([start, end, "DOMAIN"])
                continue
        
        # Fix REPOSITORY false positives (should be URL)
        if label == "REPOSITORY":
            if is_url(entity_text):
                stats['repository_to_url'] += 1
                fixed_entities.append([start, end, "URL"])
                continue
            # If it's not a valid repository format, remove it
            if not re.match(r'^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$', entity_text):
                stats['removed_repository'] += 1
                continue
        
        # Fix DATE false positives (should be FILE_PATH)
        if label == "DATE":
            if is_file_path(entity_text):
                stats['date_to_filepath'] += 1
                fixed_entities.append([start, end, "FILE_PATH"])
                continue
            # If it's not a valid date, remove it
            if not is_date(entity_text):
                stats['removed_date'] += 1
                continue
        
        # Fix DOMAIN false positives
        if label == "DOMAIN":
            if not is_valid_domain(entity_text):
                stats['removed_domain'] += 1
                continue
        
        # Fix EMAIL_ADDRESS false positives
        if label == "EMAIL_ADDRESS":
            if not is_valid_email(entity_text):
                stats['removed_email'] += 1
                continue
        
        # Keep the entity as-is
        fixed_entities.append([start, end, label])
    
    return fixed_entities, stats


def process_file(file_path: Path, dry_run: bool = False) -> Dict:
    """Process a single JSONL file."""
    total_stats = defaultdict(int)
    
    # Create backup
    if not dry_run:
        backup_path = file_path.with_suffix(f'.jsonl.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        shutil.copy2(file_path, backup_path)
        print(f"  📦 Backup created: {backup_path.name}")
    
    cleaned_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            
            try:
                data = json.loads(line)
                text = data.get('text', '')
                entities = data.get('entities', [])
                
                # Fix entities
                fixed_entities, stats = fix_entities_in_text(text, entities)
                
                # Update stats
                for key, value in stats.items():
                    total_stats[key] += value
                
                # Update data
                data['entities'] = fixed_entities
                
                # Keep line if it has entities or is a negative example
                if len(fixed_entities) > 0 or len(entities) == 0:
                    cleaned_data.append(data)
                else:
                    total_stats['removed_lines'] += 1
                    
            except Exception as e:
                print(f"  ⚠️  Error on line {line_num}: {e}")
                continue
    
    # Write cleaned data
    if not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            for data in cleaned_data:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    return total_stats


def main():
    base_dir = Path("entities-intent")
    
    print("="*80)
    print("FIX FALSE POSITIVES - COMPREHENSIVE")
    print("="*80)
    print("\nThis script fixes:")
    print("  1. TOOL false positives (common words)")
    print("  2. REPOSITORY vs URL confusion")
    print("  3. DATE vs FILE_PATH confusion")
    print("  4. DOMAIN false positives")
    print("  5. EMAIL_ADDRESS false positives")
    print()
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying files')
    args = parser.parse_args()
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified\n")
    else:
        print("⚠️  LIVE MODE - Files will be modified (backups created)\n")
    
    total_stats = defaultdict(int)
    files_processed = 0
    
    for pillar_dir in sorted(base_dir.iterdir()):
        if pillar_dir.is_dir() and not pillar_dir.name.startswith('.'):
            entity_file = pillar_dir / f"{pillar_dir.name}_entities.jsonl"
            if entity_file.exists():
                print(f"📝 Processing {pillar_dir.name}...")
                stats = process_file(entity_file, dry_run=args.dry_run)
                
                if any(stats.values()):
                    print(f"   ✅ Fixed:")
                    for key, value in sorted(stats.items()):
                        if value > 0:
                            print(f"      {key}: {value}")
                
                for key, value in stats.items():
                    total_stats[key] += value
                files_processed += 1
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Files processed: {files_processed}")
    print(f"\nTotal fixes:")
    for key, value in sorted(total_stats.items()):
        if value > 0:
            print(f"  {key}: {value}")
    
    if args.dry_run:
        print("\n🔍 This was a dry run. Use without --dry-run to apply changes.")
    else:
        print("\n✅ False positives fixed! Backups created.")
    
    print("="*80)


if __name__ == "__main__":
    main()

