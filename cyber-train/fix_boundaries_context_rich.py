#!/usr/bin/env python3
"""
Fix Boundaries and Labels in Context-Rich Examples

This script reviews and fixes any boundary or labeling issues in the
context-rich training examples, ensuring entities are correctly labeled
and boundaries are accurate.
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple
import re

def fix_entity_boundaries(text: str, entities: List[List]) -> List[List]:
    """Fix entity boundaries to ensure they're correct."""
    fixed_entities = []
    
    for start, end, label in entities:
        # Validate boundaries
        if start < 0:
            start = 0
        if end > len(text):
            end = len(text)
        if start >= end:
            continue  # Skip invalid boundaries
        
        # Get entity text
        entity_text = text[start:end]
        
        # Trim whitespace if entity should not have it
        # But preserve if it's part of the entity (e.g., phone numbers with spaces)
        trimmed_start = start
        trimmed_end = end
        
        # For most entities, trim leading/trailing whitespace
        # But keep it for entities that might legitimately have spaces
        space_preserving_labels = ['PHONE_NUMBER', 'SSN', 'COMPLIANCE_FRAMEWORK', 'MALWARE_TYPE']
        
        if label not in space_preserving_labels:
            # Trim leading whitespace
            while trimmed_start < trimmed_end and text[trimmed_start].isspace():
                trimmed_start += 1
            # Trim trailing whitespace
            while trimmed_end > trimmed_start and text[trimmed_end - 1].isspace():
                trimmed_end -= 1
        
        if trimmed_start < trimmed_end:
            fixed_entities.append([trimmed_start, trimmed_end, label])
    
    return fixed_entities

def validate_entity_in_text(text: str, entity_text: str, start: int, end: int) -> bool:
    """Validate that entity text matches what's at the given position."""
    if start < 0 or end > len(text) or start >= end:
        return False
    
    actual_text = text[start:end]
    # Allow for case differences
    return actual_text.strip().lower() == entity_text.strip().lower()

def review_and_fix_file(file_path: Path) -> Tuple[int, int, int]:
    """Review and fix a single JSONL file."""
    fixed_count = 0
    removed_count = 0
    total_examples = 0
    
    # Read all examples
    examples = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    examples.append(data)
                    total_examples += 1
                except:
                    pass
    
    # Fix examples
    fixed_examples = []
    for data in examples:
        text = data.get('text', '')
        entities = data.get('entities', [])
        
        # Fix boundaries
        fixed_entities = fix_entity_boundaries(text, entities)
        
        # Remove duplicates (same position and label)
        seen = set()
        unique_entities = []
        for start, end, label in fixed_entities:
            key = (start, end, label)
            if key not in seen:
                seen.add(key)
                unique_entities.append([start, end, label])
        
        if len(unique_entities) != len(entities):
            fixed_count += 1
        
        if len(unique_entities) < len(entities):
            removed_count += (len(entities) - len(unique_entities))
        
        # Update data
        data['entities'] = unique_entities
        fixed_examples.append(data)
    
    # Write back
    if fixed_count > 0 or removed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            for data in fixed_examples:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    return total_examples, fixed_count, removed_count

def main():
    base_dir = Path("entities-intent")
    
    print("=" * 80)
    print("REVIEWING AND FIXING BOUNDARIES IN CONTEXT-RICH EXAMPLES")
    print("=" * 80)
    print()
    
    total_files = 0
    total_examples = 0
    total_fixed = 0
    total_removed = 0
    
    # Process all entity files
    for jsonl_file in base_dir.rglob('*_entities.jsonl'):
        total_files += 1
        examples, fixed, removed = review_and_fix_file(jsonl_file)
        total_examples += examples
        total_fixed += fixed
        total_removed += removed
        
        if fixed > 0 or removed > 0:
            print(f"✅ Fixed {jsonl_file.name}: {fixed} examples fixed, {removed} duplicate entities removed")
    
    print()
    print("=" * 80)
    print(f"✅ COMPLETE: Reviewed {total_files} files, {total_examples:,} examples")
    print(f"   Fixed: {total_fixed} examples")
    print(f"   Removed: {total_removed} duplicate entities")
    print("=" * 80)

if __name__ == "__main__":
    main()


