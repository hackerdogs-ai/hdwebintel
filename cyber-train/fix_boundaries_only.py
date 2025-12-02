#!/usr/bin/env python3
"""
Fix boundary issues ONLY - do NOT remove entities.
Only fixes:
1. Whitespace trimming
2. Pattern-based entity boundary correction
3. Partial word boundary fixes (conservative)
"""

import json
import re
from pathlib import Path
from typing import Tuple
import shutil
from datetime import datetime

# Patterns
IP_PATTERN = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
IPV6_PATTERN = re.compile(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b::1\b|\bfe80::[0-9a-fA-F:]+')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?[\d\s\-\(\)]{10,}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
GITHUB_REPO_PATTERN = re.compile(r'[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+')
GITHUB_URL_PATTERN = re.compile(r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)*')
GITHUB_USER_PATTERN = re.compile(r'@?[a-zA-Z0-9]([a-zA-Z0-9]|-(?![.-])){0,38}')
GITHUB_GIST_PATTERN = re.compile(r'https?://gist\.github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9]+')
GITHUB_ISSUE_PATTERN = re.compile(r'#[0-9]+')
GITHUB_COMMIT_PATTERN = re.compile(r'\b[a-f0-9]{7,40}\b')

VALID_PATTERNS = {
    'IP_ADDRESS': IP_PATTERN,
    'IPV6_ADDRESS': IPV6_PATTERN,
    'DOMAIN': DOMAIN_PATTERN,
    'CVE_ID': CVE_PATTERN,
    'EMAIL': EMAIL_PATTERN,
    'EMAIL_ADDRESS': EMAIL_PATTERN,
    'PHONE_NUMBER': PHONE_PATTERN,
    'WALLET_ADDRESS': WALLET_PATTERN,
    'URL': URL_PATTERN,
    'GITHUB_REPO': GITHUB_REPO_PATTERN,
    'GITHUB_REPO_URL': GITHUB_URL_PATTERN,
    'GITHUB_USER': GITHUB_USER_PATTERN,
    'GITHUB_GIST': GITHUB_GIST_PATTERN,
    'GITHUB_ISSUE': GITHUB_ISSUE_PATTERN,
    'GITHUB_COMMIT': GITHUB_COMMIT_PATTERN,
}

def fix_boundary_only(text: str, start: int, end: int, label: str) -> Tuple[int, int]:
    """
    Fix boundary ONLY - NEVER remove entity.
    Returns (new_start, new_end) - always keeps entity.
    """
    entity_text = text[start:end]
    original_start, original_end = start, end
    
    # 1. Trim whitespace
    stripped = entity_text.strip()
    if stripped != entity_text:
        new_start = start
        new_end = end
        while new_start < new_end and text[new_start].isspace():
            new_start += 1
        while new_end > new_start and text[new_end - 1].isspace():
            new_end -= 1
        if new_start < new_end:
            start, end = new_start, new_end
            entity_text = text[start:end]
    
    # 2. For pattern-based entities: try to find correct boundary
    if label in VALID_PATTERNS:
        pattern = VALID_PATTERNS[label]
        
        # Check if current text matches pattern
        if not pattern.fullmatch(entity_text):
            # Try to find correct boundary nearby
            search_start = max(0, original_start - 100)
            search_end = min(len(text), original_end + 100)
            search_text = text[search_start:search_end]
            offset = search_start
            
            best_match = None
            best_distance = float('inf')
            
            for match in pattern.finditer(search_text):
                match_start = offset + match.start()
                match_end = offset + match.end()
                
                # Calculate distance
                distance = abs(match_start - original_start) + abs(match_end - original_end)
                
                # Prefer matches that overlap or are close
                if (match_start <= original_end and match_end >= original_start) or distance < 50:
                    if distance < best_distance:
                        best_distance = distance
                        best_match = (match_start, match_end)
            
            if best_match:
                return best_match[0], best_match[1]
    
    # 3. Fix partial word boundaries (FIX THEM - this is the main issue)
    # Check if we're in middle of word at start
    if start > 0 and text[start - 1].isalnum():
        # Find word start - extend up to 20 chars
        word_start = start
        while word_start > 0 and (text[word_start - 1].isalnum() or text[word_start - 1] == '_'):
            word_start -= 1
            if abs(word_start - original_start) > 20:
                break
        # Use the word start
        start = word_start
    
    # Check if we're in middle of word at end
    if end < len(text) and text[end].isalnum():
        # Find word end - extend up to 20 chars
        word_end = end
        while word_end < len(text) and (text[word_end].isalnum() or text[word_end] == '_'):
            word_end += 1
            if abs(word_end - original_end) > 20:
                break
        # Use the word end
        end = word_end
    
    return start, end

def fix_file_boundaries(file_path: Path) -> dict:
    """Fix boundaries only - keep all entities."""
    backup_path = file_path.with_suffix(file_path.suffix + f'.backup_boundary_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    shutil.copy2(file_path, backup_path)
    
    results = {
        'file': str(file_path),
        'total_examples': 0,
        'entities_before': 0,
        'entities_after': 0,
        'fixed': 0,
    }
    
    fixed_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            
            try:
                data = json.loads(line)
                text = data.get('text', '')
                entities = data.get('entities', [])
                
                results['total_examples'] += 1
                results['entities_before'] += len(entities)
                
                fixed_entities = []
                
                for start, end, label in entities:
                    new_start, new_end = fix_boundary_only(text, start, end, label)
                    fixed_entities.append([new_start, new_end, label])
                    
                    if (new_start, new_end) != (start, end):
                        results['fixed'] += 1
                
                # Remove duplicates
                seen = set()
                unique_entities = []
                for ent in fixed_entities:
                    key = (ent[0], ent[1], ent[2])
                    if key not in seen:
                        seen.add(key)
                        unique_entities.append(ent)
                
                fixed_data.append({
                    'text': text,
                    'entities': unique_entities
                })
                
                results['entities_after'] += len(unique_entities)
                
            except Exception as e:
                print(f"Error in {file_path.name}: {e}")
    
    # Write fixed data
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in fixed_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return results

def main():
    """Main function."""
    base_dir = Path('cyber-train/entities-intent')
    if not base_dir.exists():
        base_dir = Path('entities-intent')
    
    entity_files = list(base_dir.rglob('*_entities.jsonl'))
    
    print("="*80)
    print("FIXING BOUNDARIES ONLY - KEEPING ALL ENTITIES")
    print("="*80)
    print(f"\nFound {len(entity_files)} entity files\n")
    
    results_list = []
    for file_path in sorted(entity_files):
        print(f"Fixing: {file_path.name}...", end=' ', flush=True)
        result = fix_file_boundaries(file_path)
        results_list.append(result)
        print(f"✅ Fixed {result['fixed']} boundaries")
        print(f"   Entities: {result['entities_before']} → {result['entities_after']} (KEPT ALL)")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    total_fixed = sum(r['fixed'] for r in results_list)
    total_before = sum(r['entities_before'] for r in results_list)
    total_after = sum(r['entities_after'] for r in results_list)
    
    print(f"\nTotal boundaries fixed: {total_fixed:,}")
    print(f"Total entities: {total_before:,} → {total_after:,}")
    print(f"Entity retention: {((total_after / total_before) * 100):.2f}%")

if __name__ == '__main__':
    main()

