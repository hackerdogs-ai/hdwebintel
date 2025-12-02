#!/usr/bin/env python3
"""
Fix invalid pattern entities - entities that don't match their expected patterns.
This will remove entities that don't match their pattern-based labels.
"""

import json
import re
from pathlib import Path
from typing import List, Tuple

# Patterns for validation
IP_PATTERN = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_INTL_PATTERN = re.compile(r'\b\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}\b')
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
LATITUDE_PATTERN = re.compile(r'\b-?\d{1,2}(\.\d+)?\b')
LONGITUDE_PATTERN = re.compile(r'\b-?\d{1,3}(\.\d+)?\b')


def validate_pattern(entity_text: str, label: str) -> bool:
    """Validate if entity text matches its pattern-based label."""
    entity_clean = entity_text.strip()
    
    if label == 'IP_ADDRESS':
        return bool(IP_PATTERN.fullmatch(entity_clean))
    
    elif label == 'DOMAIN':
        return bool(DOMAIN_PATTERN.fullmatch(entity_clean))
    
    elif label == 'CVE_ID':
        return bool(CVE_PATTERN.fullmatch(entity_clean))
    
    elif label in ['EMAIL', 'EMAIL_ADDRESS']:
        return bool(EMAIL_PATTERN.fullmatch(entity_clean))
    
    elif label == 'PHONE_NUMBER':
        return bool(PHONE_INTL_PATTERN.fullmatch(entity_clean) or re.match(r'\b\+?[\d\s\-\(\)]{10,}\b', entity_clean))
    
    elif label == 'SSN':
        return bool(SSN_PATTERN.fullmatch(entity_clean))
    
    elif label == 'CREDIT_CARD_NUMBER':
        return bool(CREDIT_CARD_PATTERN.fullmatch(entity_clean))
    
    elif label == 'WALLET_ADDRESS':
        return bool(WALLET_PATTERN.fullmatch(entity_clean))
    
    elif label == 'LATITUDE':
        return bool(LATITUDE_PATTERN.fullmatch(entity_clean))
    
    elif label == 'LONGITUDE':
        return bool(LONGITUDE_PATTERN.fullmatch(entity_clean))
    
    # For non-pattern entities, return True (no pattern to validate)
    return True


def process_file(file_path: Path) -> dict:
    """Remove entities with invalid patterns."""
    stats = {
        'removed': 0,
        'total_before': 0,
        'total_after': 0
    }
    
    data_list = []
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            data_list.append(data)
    
    fixed_data = []
    
    for data in data_list:
        text = data.get('text', '')
        entities = data.get('entities', [])
        stats['total_before'] += len(entities)
        
        fixed_entities = []
        
        for start, end, label in entities:
            entity_text = text[start:end].strip()
            
            # Validate pattern
            if not validate_pattern(entity_text, label):
                stats['removed'] += 1
                continue
            
            fixed_entities.append([start, end, label])
        
        stats['total_after'] += len(fixed_entities)
        data['entities'] = fixed_entities
        fixed_data.append(data)
    
    # Backup
    backup_path = file_path.with_suffix('.jsonl.backup7')
    if not backup_path.exists():
        import shutil
        shutil.copy(file_path, backup_path)
    
    # Write fixed data
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in fixed_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return stats


def main():
    base_dir = Path("cyber-train/entities-intent")
    entity_files = sorted(list(base_dir.rglob("*_entities.jsonl")))
    
    print("="*80)
    print("FIXING INVALID PATTERN ENTITIES")
    print("="*80)
    print(f"\nFiles to process: {len(entity_files)}")
    
    total_removed = 0
    total_before = 0
    total_after = 0
    
    for file_path in entity_files:
        stats = process_file(file_path)
        
        if stats['removed'] > 0:
            print(f"\n📄 {file_path.relative_to(base_dir)}")
            print(f"   Removed: {stats['removed']} invalid pattern entities")
            print(f"   Before: {stats['total_before']} entities")
            print(f"   After: {stats['total_after']} entities")
        
        total_removed += stats['removed']
        total_before += stats['total_before']
        total_after += stats['total_after']
    
    print("\n" + "="*80)
    print("FIX SUMMARY")
    print("="*80)
    print(f"Total entities before: {total_before:,}")
    print(f"Total entities after: {total_after:,}")
    print(f"Total removed (invalid patterns): {total_removed:,}")
    print("\n✅ Invalid pattern entities removed!")


if __name__ == "__main__":
    main()

