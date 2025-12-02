#!/usr/bin/env python3
"""
Double the training data for each pillar by duplicating existing entries.
This will help improve model training with more examples.
"""

import json
from pathlib import Path
import argparse
import random
from typing import List, Dict


def double_jsonl_file(file_path: Path, shuffle: bool = True, backup: bool = True):
    """
    Double the content of a JSONL file by duplicating all entries.
    
    Args:
        file_path: Path to the JSONL file
        shuffle: Whether to shuffle the data after doubling
        backup: Whether to create a backup of the original file
    """
    if not file_path.exists():
        print(f"⚠️  File not found: {file_path}")
        return False
    
    # Read all lines
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original_count = len(lines)
    
    if original_count == 0:
        print(f"⚠️  File is empty: {file_path}")
        return False
    
    # Create backup if requested
    if backup:
        backup_path = file_path.with_suffix('.jsonl.backup')
        if not backup_path.exists():
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"   📦 Backup created: {backup_path.name}")
    
    # Double the data
    doubled_lines = lines + lines  # Duplicate all lines
    
    # Shuffle if requested (helps with training)
    if shuffle:
        random.shuffle(doubled_lines)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(doubled_lines)
    
    print(f"   ✅ Doubled: {original_count} → {len(doubled_lines)} entries")
    return True


def double_all_training_data(base_dir: Path, 
                            entities_only: bool = False,
                            intents_only: bool = False,
                            shuffle: bool = True,
                            backup: bool = True):
    """
    Double all training data files in the base directory.
    
    Args:
        base_dir: Base directory containing JSONL files
        entities_only: Only process entity files
        intents_only: Only process intent files
        shuffle: Whether to shuffle data after doubling
        backup: Whether to create backups
    """
    print("="*70)
    print("DOUBLING TRAINING DATA")
    print("="*70)
    
    # Find all JSONL files
    entity_files = []
    intent_files = []
    
    for jsonl_file in base_dir.rglob("*.jsonl"):
        if "_entities.jsonl" in jsonl_file.name:
            entity_files.append(jsonl_file)
        elif "_intent.jsonl" in jsonl_file.name:
            intent_files.append(jsonl_file)
    
    print(f"\n📊 Found:")
    print(f"   Entity files: {len(entity_files)}")
    print(f"   Intent files: {len(intent_files)}")
    
    # Process entity files
    if not intents_only:
        print(f"\n🔄 Processing entity files...")
        entity_success = 0
        entity_total = 0
        
        for file_path in sorted(entity_files):
            print(f"\n   Processing: {file_path.relative_to(base_dir)}")
            if double_jsonl_file(file_path, shuffle=shuffle, backup=backup):
                entity_success += 1
                entity_total += 1
            else:
                entity_total += 1
        
        print(f"\n   ✅ Processed {entity_success}/{entity_total} entity files")
    
    # Process intent files
    if not entities_only:
        print(f"\n🔄 Processing intent files...")
        intent_success = 0
        intent_total = 0
        
        for file_path in sorted(intent_files):
            print(f"\n   Processing: {file_path.relative_to(base_dir)}")
            if double_jsonl_file(file_path, shuffle=shuffle, backup=backup):
                intent_success += 1
                intent_total += 1
            else:
                intent_total += 1
        
        print(f"\n   ✅ Processed {intent_success}/{intent_total} intent files")
    
    print("\n" + "="*70)
    print("✅ DOUBLING COMPLETE!")
    print("="*70)
    print("\n📋 Next steps:")
    print("   1. Re-run data preparation:")
    print("      python3 cyber-train/prepare_spacy_training.py")
    print("   2. Retrain models with doubled data")
    print("   3. Compare performance with previous models")


def main():
    parser = argparse.ArgumentParser(
        description="Double training data for all pillars"
    )
    parser.add_argument(
        "--base-dir",
        default="cyber-train/entities-intent",
        help="Base directory containing JSONL files"
    )
    parser.add_argument(
        "--entities-only",
        action="store_true",
        help="Only process entity files"
    )
    parser.add_argument(
        "--intents-only",
        action="store_true",
        help="Only process intent files"
    )
    parser.add_argument(
        "--no-shuffle",
        action="store_true",
        help="Don't shuffle data after doubling"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup files"
    )
    
    args = parser.parse_args()
    
    base_dir = Path(args.base_dir)
    if not base_dir.exists():
        print(f"❌ Base directory not found: {base_dir}")
        return
    
    double_all_training_data(
        base_dir=base_dir,
        entities_only=args.entities_only,
        intents_only=args.intents_only,
        shuffle=not args.no_shuffle,
        backup=not args.no_backup
    )


if __name__ == "__main__":
    main()


