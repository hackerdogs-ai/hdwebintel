#!/usr/bin/env python3
"""
Restore ALL entities from backup and fix ONLY boundaries.
Do NOT remove valid entities - only fix wrong boundaries.
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
PHONE_PATTERN = re.compile(r'\b\+?[\d\s\-\(\)]{10,}\b')
PHONE_INTL_PATTERN = re.compile(r'\b\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}\b')
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b')

# ONLY remove these specific wrong cases
WRONG_ENTITIES_TO_REMOVE = {
    # Single word "AI" labeled as AI_MODEL_TYPE (but keep "AI" in "AI Compliance Analyst")
    ('AI', 'AI_MODEL_TYPE'),
    # Single word "security" labeled as SECURITY_TYPE
    ('security', 'SECURITY_TYPE'),
    # Single word "incident" labeled as INCIDENT_TYPE
    ('incident', 'INCIDENT_TYPE'),
    # Single word "rate" labeled as METRIC_TYPE (unless it's part of a phrase)
    # But we'll be conservative - only remove if it's clearly wrong
}


def fix_boundary_for_pattern(text: str, start: int, end: int, label: str) -> Tuple[int, int]:
    """Fix boundary for pattern-based entities only."""
    if start < 0 or end > len(text) or start >= end:
        return start, end
    
    entity_text = text[start:end].strip()
    
    # Fix IP addresses
    if label == 'IP_ADDRESS':
        matches = list(IP_PATTERN.finditer(text))
        if matches:
            for match in matches:
                if abs(match.start() - start) < 30:
                    return match.start(), match.end()
    
    # Fix domains
    elif label == 'DOMAIN':
        matches = list(DOMAIN_PATTERN.finditer(text))
        if matches:
            for match in matches:
                if abs(match.start() - start) < 30:
                    return match.start(), match.end()
    
    # Fix CVEs
    elif label == 'CVE_ID':
        matches = list(CVE_PATTERN.finditer(text))
        if matches:
            for match in matches:
                if abs(match.start() - start) < 30:
                    return match.start(), match.end()
    
    # Fix emails
    elif label in ['EMAIL', 'EMAIL_ADDRESS']:
        matches = list(EMAIL_PATTERN.finditer(text))
        if matches:
            for match in matches:
                if abs(match.start() - start) < 30:
                    return match.start(), match.end()
    
    # Fix phone numbers
    elif label == 'PHONE_NUMBER':
        matches = list(PHONE_INTL_PATTERN.finditer(text))
        if matches:
            for match in matches:
                if abs(match.start() - start) < 30:
                    return match.start(), match.end()
        else:
            matches = list(PHONE_PATTERN.finditer(text))
            if matches:
                for match in matches:
                    if abs(match.start() - start) < 30:
                        return match.start(), match.end()
    
    # Fix SSN
    elif label == 'SSN':
        matches = list(SSN_PATTERN.finditer(text))
        if matches:
            for match in matches:
                if abs(match.start() - start) < 30:
                    return match.start(), match.end()
    
    # Fix credit card
    elif label == 'CREDIT_CARD_NUMBER':
        matches = list(CREDIT_CARD_PATTERN.finditer(text))
        if matches:
            for match in matches:
                if abs(match.start() - start) < 30:
                    return match.start(), match.end()
    
    return start, end


def should_remove_entity(text: str, start: int, end: int, label: str) -> bool:
    """ONLY remove entities that are clearly wrong - be very conservative."""
    if start < 0 or end > len(text) or start >= end:
        return True
    
    entity_text = text[start:end].strip()
    entity_lower = entity_text.lower()
    
    # Remove if it's just whitespace
    if not entity_text or entity_text.isspace():
        return True
    
    # Remove if it's a single character (unless it's a valid ID)
    if len(entity_text) == 1 and entity_text not in ['I', 'A']:
        return True
    
    # ONLY remove if it's the exact wrong case
    if (entity_text, label) in WRONG_ENTITIES_TO_REMOVE:
        return True
    
    # Remove if it's "AI" as AI_MODEL_TYPE and it's just the word "AI" (not part of a phrase)
    if label == 'AI_MODEL_TYPE' and entity_text == 'AI':
        # Check if it's part of a phrase like "AI Compliance" - if so, keep it
        if start > 0 and text[start-1].isalnum():
            return False  # Part of a phrase, keep it
        if end < len(text) and text[end].isalnum():
            return False  # Part of a phrase, keep it
        return True  # Standalone "AI", remove it
    
    # Remove if it's "security" as SECURITY_TYPE and it's just the word
    if label == 'SECURITY_TYPE' and entity_text.lower() == 'security':
        # Check if it's part of a phrase
        if start > 0 and text[start-1].isalnum():
            return False
        if end < len(text) and text[end].isalnum():
            return False
        return True
    
    # Remove if it's "incident" as INCIDENT_TYPE and it's just the word
    if label == 'INCIDENT_TYPE' and entity_text.lower() == 'incident':
        if start > 0 and text[start-1].isalnum():
            return False
        if end < len(text) and text[end].isalnum():
            return False
        return True
    
    return False  # Keep everything else


def restore_and_fix_file(file_path: Path, backup_path: Path) -> dict:
    """Restore all entities and fix boundaries only."""
    stats = {
        'restored': 0,
        'boundaries_fixed': 0,
        'removed': 0
    }
    
    backup_data = []
    with open(backup_path, 'r') as f:
        for line in f:
            backup_data.append(json.loads(line))
    
    restored_data = []
    
    for backup_item in backup_data:
        text = backup_item.get('text', '')
        backup_entities = backup_item.get('entities', [])
        
        restored_entities = []
        
        for start, end, label in backup_entities:
            # Check if should remove (very conservative)
            if should_remove_entity(text, start, end, label):
                stats['removed'] += 1
                continue
            
            # Fix boundary if needed (for pattern-based entities)
            new_start, new_end = fix_boundary_for_pattern(text, start, end, label)
            
            if new_start != start or new_end != end:
                stats['boundaries_fixed'] += 1
            
            # Trim whitespace from boundaries
            entity_text = text[new_start:new_end]
            if entity_text != entity_text.strip():
                actual_start = new_start
                actual_end = new_end
                
                while actual_start < actual_end and text[actual_start].isspace():
                    actual_start += 1
                
                while actual_end > actual_start and text[actual_end - 1].isspace():
                    actual_end -= 1
                
                if actual_start < actual_end:
                    restored_entities.append([actual_start, actual_end, label])
                    if actual_start != new_start or actual_end != new_end:
                        stats['boundaries_fixed'] += 1
            else:
                restored_entities.append([new_start, new_end, label])
                stats['restored'] += 1
        
        restored_data.append({
            'text': text,
            'entities': restored_entities
        })
    
    # Write restored data
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in restored_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return stats


def main():
    base_dir = Path("cyber-train/entities-intent")
    entity_files = sorted(list(base_dir.rglob("*_entities.jsonl")))
    
    print("="*70)
    print("RESTORING ALL ENTITIES AND FIXING BOUNDARIES ONLY")
    print("="*70)
    print(f"\nFiles to process: {len(entity_files)}")
    
    total_restored = 0
    total_fixed = 0
    total_removed = 0
    
    for file_path in entity_files:
        # Find backup file
        backup_path = file_path.with_suffix('.jsonl.backup2')
        if not backup_path.exists():
            backup_path = file_path.with_suffix('.jsonl.backup')
        
        if not backup_path.exists():
            print(f"\n⚠️  No backup found for: {file_path.relative_to(base_dir)}")
            continue
        
        print(f"\n📄 Processing: {file_path.relative_to(base_dir)}")
        stats = restore_and_fix_file(file_path, backup_path)
        
        total_restored += stats['restored']
        total_fixed += stats['boundaries_fixed']
        total_removed += stats['removed']
        
        print(f"   Restored: {stats['restored']} entities")
        print(f"   Boundaries fixed: {stats['boundaries_fixed']}")
        print(f"   Removed (wrong only): {stats['removed']}")
    
    print("\n" + "="*70)
    print("RESTORATION SUMMARY")
    print("="*70)
    print(f"Total entities restored: {total_restored:,}")
    print(f"Total boundaries fixed: {total_fixed:,}")
    print(f"Total removed (wrong only): {total_removed:,}")
    print("\n✅ All entities restored! Boundaries fixed only.")


if __name__ == "__main__":
    main()

