#!/usr/bin/env python3
"""
Comprehensive boundary fix script.
Fixes partial words, wrong boundaries, and validates against patterns.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
import shutil
from datetime import datetime

# Patterns for validation
IP_PATTERN = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?[\d\s\-\(\)]{10,}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
COORDINATE_PAIR_PATTERN = re.compile(r'\b(-?[0-8]?[0-9](?:\.[0-9]+)?|90(?:\.0+)?)\s*[,;]\s*(-?(?:[0-9]?[0-9]?[0-9](?:\.[0-9]+)?|1[0-7][0-9](?:\.[0-9]+)?|180(?:\.0+)?))\b')

VALID_PATTERNS = {
    'IP_ADDRESS': IP_PATTERN,
    'DOMAIN': DOMAIN_PATTERN,
    'CVE_ID': CVE_PATTERN,
    'EMAIL': EMAIL_PATTERN,
    'EMAIL_ADDRESS': EMAIL_PATTERN,
    'PHONE_NUMBER': PHONE_PATTERN,
    'WALLET_ADDRESS': WALLET_PATTERN,
}

# Common words that should NEVER be entities
COMMON_WORDS_NEVER = {
    'the', 'a', 'an', 'this', 'that', 'for', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'from',
    'with', 'by', 'of', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must',
    'i', 'me', 'my', 'you', 'your', 'he', 'she', 'it', 'we', 'they', 'them',
    'what', 'when', 'where', 'why', 'how', 'who', 'which', 'whose', 'whom',
    'up', 'down', 'out', 'off', 'over', 'under', 'above', 'below',
    'access', 'attempt', 'attempts', 'from', 'ip', 'host', 'port', 'user', 'domain',
    'check', 'verify', 'investigate', 'analyze', 'detect', 'monitor', 'track',
    'execute', 'block', 'isolate', 'generate', 'find', 'show', 'get', 'set',
    'compliance', 'requirements', 'data', 'system', 'network', 'threat', 'intelligence',
    'report', 'tool', 'type', 'count', 'metric', 'value', 'number', 'phone', 'email', 'address',
    'card', 'credit', 'bank', 'account', 'ssn', 'long', 'various', 'types', 'appear',
    'anomalies', 'lateral', 'latitude', 'longitude', 'used', 'wannacry', 'campaign'
}

def find_entities_in_text(text: str, pattern: re.Pattern) -> List[Tuple[int, int, str]]:
    """Find all matches of a pattern in text."""
    entities = []
    for match in pattern.finditer(text):
        entities.append((match.start(), match.end(), match.group()))
    return entities

def fix_entity_boundary(text: str, start: int, end: int, label: str) -> Tuple[int, int, bool]:
    """Fix entity boundary to match correct span."""
    entity_text = text[start:end].strip()
    
    # If label has a pattern, try to find correct boundary
    if label in VALID_PATTERNS:
        pattern = VALID_PATTERNS[label]
        # Search around the current position
        search_start = max(0, start - 20)
        search_end = min(len(text), end + 20)
        search_text = text[search_start:search_end]
        
        for match in pattern.finditer(search_text):
            match_start = search_start + match.start()
            match_end = search_start + match.end()
            match_text = match.group()
            
            # Check if this match overlaps with or is near our entity
            if (match_start <= end and match_end >= start) or \
               (abs(match_start - start) < 10 and abs(match_end - end) < 10):
                # Found correct boundary
                return (match_start, match_end, True)
    
    # If no pattern match, try to fix partial words
    # Remove leading partial word
    while start > 0 and text[start-1].isalnum():
        start -= 1
    
    # Remove trailing partial word
    while end < len(text) and text[end].isalnum():
        end += 1
    
    # Trim whitespace
    while start < len(text) and text[start].isspace():
        start += 1
    while end > start and text[end-1].isspace():
        end -= 1
    
    return (start, end, False)

def is_valid_entity(text: str, start: int, end: int, label: str) -> bool:
    """Check if entity is valid."""
    entity_text = text[start:end].strip()
    
    # Too short
    if len(entity_text) < 2 and label not in ['IP_ADDRESS', 'DOMAIN', 'CVE_ID', 'EMAIL', 'PHONE_NUMBER']:
        return False
    
    # Common word
    if entity_text.lower() in COMMON_WORDS_NEVER:
        return False
    
    # Check pattern
    if label in VALID_PATTERNS:
        pattern = VALID_PATTERNS[label]
        if not pattern.fullmatch(entity_text):
            return False
    
    # Check for partial words
    if start > 0 and text[start-1].isalnum():
        return False
    if end < len(text) and text[end].isalnum():
        return False
    
    return True

def fix_file(file_path: Path) -> Dict:
    """Fix boundaries in a single file."""
    backup_path = file_path.with_suffix(file_path.suffix + f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    shutil.copy2(file_path, backup_path)
    
    results = {
        'file': str(file_path),
        'total_examples': 0,
        'entities_before': 0,
        'entities_after': 0,
        'fixed': 0,
        'removed': 0,
        'errors': []
    }
    
    fixed_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
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
                    # Fix boundary
                    new_start, new_end, pattern_found = fix_entity_boundary(text, start, end, label)
                    
                    # Validate
                    if is_valid_entity(text, new_start, new_end, label):
                        fixed_entities.append([new_start, new_end, label])
                        if (new_start, new_end) != (start, end):
                            results['fixed'] += 1
                    else:
                        results['removed'] += 1
                
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
                
            except json.JSONDecodeError as e:
                results['errors'].append(f"Line {line_num}: {e}")
            except Exception as e:
                results['errors'].append(f"Line {line_num}: {e}")
    
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
    print("COMPREHENSIVE BOUNDARY FIX")
    print("="*80)
    print(f"\nFound {len(entity_files)} files to fix\n")
    
    all_results = []
    
    for file_path in sorted(entity_files):
        print(f"Fixing: {file_path.name}...", end=' ', flush=True)
        result = fix_file(file_path)
        all_results.append(result)
        
        print(f"✅ Fixed {result['fixed']} boundaries, removed {result['removed']} invalid")
        print(f"   Entities: {result['entities_before']} → {result['entities_after']}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    total_fixed = sum(r['fixed'] for r in all_results)
    total_removed = sum(r['removed'] for r in all_results)
    total_before = sum(r['entities_before'] for r in all_results)
    total_after = sum(r['entities_after'] for r in all_results)
    
    print(f"\nTotal boundaries fixed: {total_fixed:,}")
    print(f"Total invalid entities removed: {total_removed:,}")
    print(f"Total entities: {total_before:,} → {total_after:,}")
    print(f"Reduction: {total_before - total_after:,} entities")

if __name__ == '__main__':
    main()

