#!/usr/bin/env python3
"""
Clean training data by removing false positive entity examples.
This script identifies and removes problematic entity annotations.
"""

import json
from pathlib import Path
import argparse
from typing import List, Tuple, Dict

# Patterns that should NOT be entities
FALSE_POSITIVE_PATTERNS = {
    # Common words
    'me', 'i', 'hey', 'hi', 'hello', 'the', 'a', 'an', 'this', 'that',
    'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
    'can', 'must', 'thing', 'things', 'stuff', 'way', 'ways', 'safe',
    'investigate', 'check', 'verify', 'analyze', 'detect', 'monitor', 'track',
    'need', 'want', 'got', 'going', 'trying', 'look', 'help', 'let', 'tell', 'show'
}

# Common phrases that should NOT be entities
FALSE_POSITIVE_PHRASES = {
    'i need', 'i want', 'i have', 'i am', 'i was', 'i will', 'i can',
    'is safe', 'is not', 'is good', 'is bad', 'is ok', 'is fine',
    "what's up", "what's", "that's", "it's", "there's", "here's",
    'can you', 'could you', 'would you', 'should you', 'will you',
    'need to', 'want to', 'have to', 'got to', 'going to', 'trying to',
    'look at', 'look for', 'look up', 'check if', 'check for', 'check on',
    'help me', 'help with', 'help to', 'let me', 'tell me', 'show me'
}

# Entity types that are often false positives for common words
PROBLEMATIC_LABELS = {
    'BRANCH', 'COMMIT', 'TRAINING_TYPE', 'INTEGRATION_TYPE',
    'ENCRYPTION_TYPE', 'VULNERABILITY_ID', 'QUERY_TYPE', 'REQUIREMENT_TYPE'
}

# Punctuation that should NOT be entities
PUNCTUATION = {':', ',', '.', ';', '-', '(', ')', '[', ']', '{', '}',
               '!', '?', '"', "'", '/', '\\', '|', '&', '%', '$', '#', '@', "'s"}


def is_false_positive(entity_text: str, label: str, text: str) -> bool:
    """
    Check if an entity is likely a false positive.
    
    Args:
        entity_text: The entity text
        label: The entity label
        text: Full text context
    
    Returns:
        True if likely a false positive
    """
    text_lower = entity_text.lower().strip()
    
    # Check punctuation
    if text_lower in PUNCTUATION or all(c in PUNCTUATION for c in text_lower):
        return True
    
    # Check single characters (except 'I' which might be valid)
    if len(text_lower) == 1 and text_lower != 'i':
        return True
    
    # Check common words
    if text_lower in FALSE_POSITIVE_PATTERNS:
        # Only filter if it's a problematic label
        if label in PROBLEMATIC_LABELS:
            return True
        # Filter common verbs when labeled as problematic types
        if text_lower in ['investigate', 'check', 'verify', 'analyze'] and label in PROBLEMATIC_LABELS:
            return True
    
    # Check common phrases
    if text_lower in FALSE_POSITIVE_PHRASES:
        return True
    
    # Check if it's a problematic label with a common word
    if label in PROBLEMATIC_LABELS:
        if text_lower in FALSE_POSITIVE_PATTERNS:
            return True
        if len(text_lower) <= 2:  # Very short for these types
            return True
    
    return False


def clean_entity_file(file_path: Path, dry_run: bool = True) -> Dict:
    """
    Clean an entity JSONL file by removing false positive entities.
    
    Args:
        file_path: Path to JSONL file
        dry_run: If True, only report issues without modifying file
    
    Returns:
        Statistics about cleaning
    """
    stats = {
        'total_lines': 0,
        'total_entities': 0,
        'removed_entities': 0,
        'cleaned_lines': 0,
        'removed_lines': 0
    }
    
    cleaned_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            stats['total_lines'] += 1
            try:
                data = json.loads(line)
                text = data.get('text', '')
                original_entities = data.get('entities', [])
                stats['total_entities'] += len(original_entities)
                
                # Filter out false positives
                cleaned_entities = []
                for start, end, label in original_entities:
                    entity_text = text[start:end]
                    if is_false_positive(entity_text, label, text):
                        stats['removed_entities'] += 1
                    else:
                        cleaned_entities.append([start, end, label])
                
                # Update data
                data['entities'] = cleaned_entities
                
                # Skip lines with no entities (or keep them as negative examples)
                if len(cleaned_entities) == 0:
                    stats['removed_lines'] += 1
                    # Optionally keep as negative example
                    # cleaned_data.append(data)
                else:
                    stats['cleaned_lines'] += 1
                    cleaned_data.append(data)
                    
            except Exception as e:
                print(f"  ⚠️  Error processing line {stats['total_lines']}: {e}")
                continue
    
    # Write cleaned data if not dry run
    if not dry_run and cleaned_data:
        backup_path = file_path.with_suffix('.jsonl.backup')
        if not backup_path.exists():
            # Create backup
            import shutil
            shutil.copy(file_path, backup_path)
        
        # Write cleaned data
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in cleaned_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Clean training data by removing false positive entities"
    )
    parser.add_argument(
        "--base-dir",
        default="cyber-train/entities-intent",
        help="Base directory containing JSONL files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report issues, don't modify files"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually apply the cleaning (creates backups)"
    )
    
    args = parser.parse_args()
    
    if not args.apply and not args.dry_run:
        print("⚠️  Use --dry-run to preview or --apply to clean files")
        return
    
    base_dir = Path(args.base_dir)
    entity_files = list(base_dir.rglob("*_entities.jsonl"))
    
    print("="*70)
    print("CLEANING TRAINING DATA - REMOVING FALSE POSITIVES")
    print("="*70)
    print(f"\nMode: {'DRY RUN (preview only)' if args.dry_run else 'APPLYING CHANGES'}")
    print(f"Files to process: {len(entity_files)}")
    
    total_stats = {
        'total_lines': 0,
        'total_entities': 0,
        'removed_entities': 0,
        'cleaned_lines': 0,
        'removed_lines': 0
    }
    
    for file_path in sorted(entity_files):
        print(f"\n📄 Processing: {file_path.relative_to(base_dir)}")
        stats = clean_entity_file(file_path, dry_run=args.dry_run)
        
        for key in total_stats:
            total_stats[key] += stats[key]
        
        if stats['removed_entities'] > 0:
            print(f"   Removed {stats['removed_entities']} false positive entities")
            print(f"   Kept {stats['total_entities'] - stats['removed_entities']} valid entities")
        else:
            print(f"   ✅ No false positives found")
    
    print("\n" + "="*70)
    print("CLEANING SUMMARY")
    print("="*70)
    print(f"Total lines processed: {total_stats['total_lines']:,}")
    print(f"Total entities: {total_stats['total_entities']:,}")
    print(f"Removed false positives: {total_stats['removed_entities']:,}")
    print(f"Remaining entities: {total_stats['total_entities'] - total_stats['removed_entities']:,}")
    print(f"Lines with entities after cleaning: {total_stats['cleaned_lines']:,}")
    print(f"Lines removed (no entities): {total_stats['removed_lines']:,}")
    
    removal_rate = (total_stats['removed_entities'] / total_stats['total_entities'] * 100) if total_stats['total_entities'] > 0 else 0
    print(f"\nFalse positive rate: {removal_rate:.2f}%")
    
    if args.dry_run:
        print("\n💡 This was a dry run. Use --apply to actually clean the files.")
    else:
        print("\n✅ Cleaning complete! Backups created as .backup files.")
        print("   Next: Re-prepare training data and retrain models")

if __name__ == "__main__":
    main()

