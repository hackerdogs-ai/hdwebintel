#!/usr/bin/env python3
"""
Fix all issues identified in the audit:
1. Remove overlaps (keep first entity)
2. Fix pattern mismatches (dates labeled as PHONE_NUMBER)
3. Fix whitespace issues
4. Add entities to empty lines
"""

import json
import re
from pathlib import Path
from typing import List

# Patterns
DATE_PATTERN = re.compile(r'\b\d{4}-\d{2}-\d{2}\b')
PERCENTAGE_PATTERN = re.compile(r'\d+%')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?1?[-.\s(]?\(?\d{3}\)?[-.\s)]?\d{3}[-.\s]?\d{4}\b')
IP_PATTERN = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')

def fix_whitespace(text: str, start: int, end: int) -> tuple:
    """Fix whitespace in entity boundaries."""
    original_start, original_end = start, end
    
    # Trim leading whitespace
    while start < end and text[start].isspace():
        start += 1
    
    # Trim trailing whitespace
    while end > start and text[end - 1].isspace():
        end -= 1
    
    if start >= end:
        return original_start, original_end
    
    return start, end

def remove_overlaps(entities: List[List]) -> List[List]:
    """Remove overlapping entities, keeping the first one."""
    if not entities:
        return []
    
    # Sort by start position
    sorted_entities = sorted(entities, key=lambda x: (x[0], x[1]))
    
    non_overlapping = []
    for ent in sorted_entities:
        start, end, label = ent
        
        # Check if it overlaps with any existing entity
        overlaps = False
        for existing_start, existing_end, _ in non_overlapping:
            if not (end <= existing_start or start >= existing_end):
                overlaps = True
                break
        
        if not overlaps:
            non_overlapping.append(ent)
    
    return non_overlapping

def fix_pattern_mismatches(text: str, entities: List[List]) -> List[List]:
    """Fix entities with incorrect labels based on patterns."""
    fixed = []
    
    for start, end, label in entities:
        if start < 0 or end > len(text) or start >= end:
            continue
        
        entity_text = text[start:end]
        
        # Fix dates labeled as PHONE_NUMBER
        if label == 'PHONE_NUMBER' and DATE_PATTERN.fullmatch(entity_text):
            # Don't add it - it's a date, not a phone number
            continue
        
        # Fix percentages with wrong labels
        if label == 'PERCENTAGE' and not PERCENTAGE_PATTERN.fullmatch(entity_text):
            # Check if it's actually a percentage
            if '%' not in entity_text:
                continue
        
        # Fix other pattern mismatches
        if label == 'CVE_ID' and not CVE_PATTERN.fullmatch(entity_text):
            continue
        if label == 'EMAIL_ADDRESS' and not EMAIL_PATTERN.fullmatch(entity_text):
            continue
        if label == 'PHONE_NUMBER' and not PHONE_PATTERN.fullmatch(entity_text):
            continue
        if label == 'IP_ADDRESS' and not IP_PATTERN.fullmatch(entity_text):
            continue
        if label == 'URL' and not URL_PATTERN.fullmatch(entity_text):
            continue
        
        fixed.append([start, end, label])
    
    return fixed

def extract_missing_entities(text: str, existing_spans: set) -> List[List]:
    """Extract missing entities."""
    found = []
    
    # CVE IDs
    for match in CVE_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            found.append([match.start(), match.end(), 'CVE_ID'])
            existing_spans.add(span)
    
    # Email addresses
    for match in EMAIL_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            found.append([match.start(), match.end(), 'EMAIL_ADDRESS'])
            existing_spans.add(span)
    
    # URLs
    for match in URL_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            found.append([match.start(), match.end(), 'URL'])
            existing_spans.add(span)
    
    return found

def process_file(file_path: Path) -> dict:
    """Process a file and fix all issues."""
    results = {
        'whitespace_fixed': 0,
        'overlaps_removed': 0,
        'pattern_mismatches_fixed': 0,
        'entities_added': 0,
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
                
                # Fix whitespace
                fixed_entities = []
                for start, end, label in entities:
                    new_start, new_end = fix_whitespace(text, start, end)
                    if (new_start, new_end) != (start, end):
                        results['whitespace_fixed'] += 1
                    fixed_entities.append([new_start, new_end, label])
                
                # Fix pattern mismatches
                before_count = len(fixed_entities)
                fixed_entities = fix_pattern_mismatches(text, fixed_entities)
                results['pattern_mismatches_fixed'] += before_count - len(fixed_entities)
                
                # Remove overlaps
                before_count = len(fixed_entities)
                fixed_entities = remove_overlaps(fixed_entities)
                results['overlaps_removed'] += before_count - len(fixed_entities)
                
                # Add missing entities if line was empty
                if not data.get('entities'):
                    existing_spans = set((e[0], e[1]) for e in fixed_entities)
                    missing = extract_missing_entities(text, existing_spans)
                    fixed_entities.extend(missing)
                    results['entities_added'] += len(missing)
                
                fixed_data.append({
                    'text': text,
                    'entities': fixed_entities
                })
                
            except Exception as e:
                print(f"Error in {file_path.name}: {e}")
                continue
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in fixed_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return results

def main():
    base_dir = Path('cyber-train/entities-intent')
    entity_files = list(base_dir.rglob('*_entities.jsonl'))
    
    print("="*80)
    print("FIXING ALL AUDIT ISSUES")
    print("="*80)
    
    total_whitespace = 0
    total_overlaps = 0
    total_pattern = 0
    total_added = 0
    
    for file_path in sorted(entity_files):
        print(f"Processing: {file_path.name}...", end=' ', flush=True)
        result = process_file(file_path)
        total_whitespace += result['whitespace_fixed']
        total_overlaps += result['overlaps_removed']
        total_pattern += result['pattern_mismatches_fixed']
        total_added += result['entities_added']
        print(f"✅")
    
    print(f"\n✅ Fixed:")
    print(f"  Whitespace issues: {total_whitespace}")
    print(f"  Overlaps removed: {total_overlaps}")
    print(f"  Pattern mismatches fixed: {total_pattern}")
    print(f"  Entities added to empty lines: {total_added}")

if __name__ == '__main__':
    main()

