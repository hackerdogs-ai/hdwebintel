#!/usr/bin/env python3
"""
Restore entities from backup files.
This script restores entities that were incorrectly removed,
but keeps the boundary fixes that were correct.
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

# Only remove these specific common words (very limited list)
COMMON_WORDS_TO_REMOVE = {
    'ai', 'security', 'incident', 'escalation', 'rate', 'maintained', 'at', 'below', 'threshold',
    'i', 'me', 'my', 'you', 'your', 'he', 'she', 'it', 'we', 'they', 'them',
    'the', 'a', 'an', 'this', 'that', 'for', 'and', 'or', 'but', 'in', 'on', 'to', 'from',
    'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must',
    'what', 'when', 'where', 'why', 'how', 'who', 'which',
    'hey', 'hi', 'hello', 'thanks', 'please'
}

# Problematic labels ONLY for these specific words
PROBLEMATIC_LABELS_FOR_SPECIFIC_WORDS = {
    'AI_MODEL_TYPE': {'ai'},
    'SECURITY_TYPE': {'security'},
    'INCIDENT_TYPE': {'incident'},
    'METRIC_TYPE': {'rate', 'escalation', 'maintained'},
    'THRESHOLD_TYPE': {'threshold'},
}


def fix_boundary(text: str, start: int, end: int, label: str) -> Tuple[int, int]:
    """Fix entity boundary if it's wrong, but keep the entity."""
    if start < 0 or end > len(text) or start >= end:
        return start, end
    
    entity_text = text[start:end].strip()
    
    # Fix boundaries for pattern-based entities
    if label == 'IP_ADDRESS':
        matches = list(IP_PATTERN.finditer(text))
        if matches:
            for match in matches:
                if abs(match.start() - start) < 20:  # Close to current position
                    return match.start(), match.end()
    
    elif label == 'DOMAIN':
        matches = list(DOMAIN_PATTERN.finditer(text))
        if matches:
            for match in matches:
                if abs(match.start() - start) < 20:
                    return match.start(), match.end()
    
    elif label in ['CVE_ID']:
        matches = list(CVE_PATTERN.finditer(text))
        if matches:
            for match in matches:
                if abs(match.start() - start) < 20:
                    return match.start(), match.end()
    
    elif label in ['EMAIL', 'EMAIL_ADDRESS']:
        matches = list(EMAIL_PATTERN.finditer(text))
        if matches:
            for match in matches:
                if abs(match.start() - start) < 20:
                    return match.start(), match.end()
    
    return start, end


def should_remove_entity(text: str, start: int, end: int, label: str) -> bool:
    """Only remove entities that are clearly wrong - be very conservative."""
    if start < 0 or end > len(text) or start >= end:
        return True
    
    entity_text = text[start:end].strip()
    entity_lower = entity_text.lower()
    
    # Only remove if it's a very common word AND has problematic label
    if label in PROBLEMATIC_LABELS_FOR_SPECIFIC_WORDS:
        if entity_lower in PROBLEMATIC_LABELS_FOR_SPECIFIC_WORDS[label]:
            return True
    
    # Remove if it's a very common word (limited list)
    if entity_lower in COMMON_WORDS_TO_REMOVE and len(entity_text) <= 10:
        return True
    
    # Remove if it's just whitespace
    if not entity_text or entity_text.isspace():
        return True
    
    # Remove if it's a single character (unless it's a valid ID)
    if len(entity_text) == 1 and entity_text not in ['I']:
        return True
    
    return False


def restore_file(file_path: Path, backup_path: Path) -> dict:
    """Restore entities from backup, fixing boundaries but keeping valid entities."""
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
            # Fix boundary if needed
            new_start, new_end = fix_boundary(text, start, end, label)
            
            if new_start != start or new_end != end:
                stats['boundaries_fixed'] += 1
            
            # Only remove if clearly wrong
            if should_remove_entity(text, new_start, new_end, label):
                stats['removed'] += 1
                continue
            
            # Trim whitespace from boundaries
            entity_text = text[new_start:new_end]
            if entity_text != entity_text.strip():
                # Find actual boundaries without whitespace
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
    
    # Find all entity files
    entity_files = sorted(list(base_dir.rglob("*_entities.jsonl")))
    
    print("="*70)
    print("RESTORING ENTITIES FROM BACKUP")
    print("="*70)
    print(f"\nFiles to restore: {len(entity_files)}")
    
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
        
        print(f"\n📄 Restoring: {file_path.relative_to(base_dir)}")
        stats = restore_file(file_path, backup_path)
        
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
    print("\n✅ Entities restored! Now fixing boundaries only (not removing valid entities).")


if __name__ == "__main__":
    main()

