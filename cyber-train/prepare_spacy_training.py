#!/usr/bin/env python3
"""
Comprehensive script to prepare JSONL files for spaCy training
for Cybersecurity and OSINT NER and Intent Classification models.

This script:
1. Collects all entity and intent JSONL files
2. Validates data format and quality
3. Converts JSONL to spaCy's .spacy format
4. Splits data into train/dev/test sets
5. Generates statistics and reports
"""

import json
import spacy
from spacy.tokens import DocBin
from pathlib import Path
import random
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Set
import argparse
from datetime import datetime

# Set random seed for reproducibility
random.seed(42)


class SpacyDataPreparer:
    """Prepares JSONL data for spaCy training."""
    
    def __init__(self, base_dir: str = "entities-intent", output_dir: str = "models/training_data"):
        # Resolve paths: script can be run from project root or cyber-train/ directory
        import os
        # Get script directory
        script_file = os.path.abspath(__file__)
        script_dir = Path(script_file).parent
        cwd = Path.cwd()
        
        # Try paths in order of likelihood
        candidates = [
            script_dir / base_dir,  # When run from cyber-train/
            cwd / "cyber-train" / base_dir,  # When run from project root
            cwd / base_dir,  # Fallback
        ]
        
        # Find first existing path
        self.base_dir = None
        self.output_dir = None
        for candidate in candidates:
            if candidate.exists():
                self.base_dir = candidate
                # Set output_dir relative to the found base_dir
                if candidate == script_dir / base_dir:
                    self.output_dir = script_dir / output_dir
                elif candidate == cwd / "cyber-train" / base_dir:
                    self.output_dir = cwd / "cyber-train" / output_dir
                else:
                    self.output_dir = cwd / output_dir
                break
        
        # If none exist, use script directory
        if self.base_dir is None:
            self.base_dir = script_dir / base_dir
            self.output_dir = script_dir / output_dir
        
        # Convert to absolute paths
        self.base_dir = self.base_dir.resolve()
        self.output_dir = self.output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Statistics
        self.stats = {
            "entities": {"total": 0, "files": 0, "labels": set()},
            "intents": {"total": 0, "files": 0, "labels": set()}
        }
        
    def find_jsonl_files(self) -> Tuple[List[Path], List[Path]]:
        """Find all entity and intent JSONL files."""
        entity_files = list(self.base_dir.rglob("*_entities.jsonl"))
        intent_files = list(self.base_dir.rglob("*_intent.jsonl"))
        
        print(f"Found {len(entity_files)} entity files and {len(intent_files)} intent files")
        return entity_files, intent_files
    
    def validate_entity_format(self, data: dict) -> bool:
        """Validate entity JSONL format."""
        if "text" not in data:
            return False
        if "entities" not in data:
            return False
        if not isinstance(data["entities"], list):
            return False
        for entity in data["entities"]:
            if not isinstance(entity, list) or len(entity) != 3:
                return False
            if not isinstance(entity[0], int) or not isinstance(entity[1], int):
                return False
            if not isinstance(entity[2], str):
                return False
        return True
    
    def validate_intent_format(self, data: dict) -> bool:
        """Validate intent JSONL format."""
        if "text" not in data:
            return False
        if "cats" not in data:
            return False
        if not isinstance(data["cats"], dict):
            return False
        return True
    
    def load_entity_data(self, file_path: Path) -> List[dict]:
        """Load and validate entity data from JSONL file."""
        data = []
        errors = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                    if self.validate_entity_format(item):
                        data.append(item)
                        # Track labels
                        for entity in item["entities"]:
                            self.stats["entities"]["labels"].add(entity[2])
                    else:
                        errors.append(f"{file_path}:{line_num} - Invalid format")
                except json.JSONDecodeError as e:
                    errors.append(f"{file_path}:{line_num} - JSON decode error: {e}")
        
        if errors:
            print(f"⚠️  {len(errors)} errors in {file_path.name}")
            if len(errors) <= 5:
                for err in errors:
                    print(f"   {err}")
        
        self.stats["entities"]["total"] += len(data)
        self.stats["entities"]["files"] += 1
        return data
    
    def load_intent_data(self, file_path: Path) -> List[dict]:
        """Load and validate intent data from JSONL file."""
        data = []
        errors = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                    if self.validate_intent_format(item):
                        data.append(item)
                        # Track labels
                        for label in item["cats"].keys():
                            self.stats["intents"]["labels"].add(label)
                    else:
                        errors.append(f"{file_path}:{line_num} - Invalid format")
                except json.JSONDecodeError as e:
                    errors.append(f"{file_path}:{line_num} - JSON decode error: {e}")
        
        if errors:
            print(f"⚠️  {len(errors)} errors in {file_path.name}")
            if len(errors) <= 5:
                for err in errors:
                    print(f"   {err}")
        
        self.stats["intents"]["total"] += len(data)
        self.stats["intents"]["files"] += 1
        return data
    
    def convert_entities_to_spacy(self, data: List[dict], lang: str = "en") -> DocBin:
        """Convert entity data to spaCy DocBin format."""
        nlp = spacy.blank(lang)
        doc_bin = DocBin()
        
        for item in data:
            text = item["text"]
            doc = nlp.make_doc(text)
            
            # Create entity spans with overlap resolution
            raw_ents = []
            for start, end, label in item["entities"]:
                # Handle character offsets - try multiple alignment modes
                span = None
                for alignment_mode in ["contract", "expand", "strict"]:
                    span = doc.char_span(start, end, label=label, alignment_mode=alignment_mode)
                    if span is not None:
                        break
                
                if span is not None:
                    raw_ents.append((span.start, span.end, span.label_))
            
            # Resolve overlapping entities
            # Strategy: Sort by start position, then by length (longest first)
            # Keep entities that don't overlap with previously added ones
            raw_ents.sort(key=lambda x: (x[0], -(x[1] - x[0])))  # Sort by start, then by length (desc)
            
            ents = []
            used_tokens = set()
            skipped_count = 0
            
            for start, end, label in raw_ents:
                # Check if this entity overlaps with any already added
                entity_tokens = set(range(start, end))
                if not entity_tokens.intersection(used_tokens):
                    # No overlap, add this entity
                    span = doc[start:end]
                    span.label_ = label
                    ents.append(span)
                    used_tokens.update(entity_tokens)
                else:
                    # Overlap detected, skip this entity
                    skipped_count += 1
            
            # Set entities (spaCy will validate)
            try:
                doc.ents = ents
            except ValueError as e:
                # If still fails, use spaCy's built-in overlap resolver
                # This handles edge cases where token boundaries cause issues
                try:
                    from spacy.util import filter_spans
                    filtered_ents = filter_spans(ents)
                    if filtered_ents:
                        doc.ents = filtered_ents
                        if len(filtered_ents) < len(ents):
                            skipped_count += (len(ents) - len(filtered_ents))
                    else:
                        # If no valid entities after filtering, skip this document
                        print(f"⚠️  Skipping document with no valid entities after filtering: {text[:50]}...")
                        continue
                except (ImportError, AttributeError):
                    # Fallback: manually filter overlapping spans
                    # Keep only the longest non-overlapping spans
                    filtered_ents = []
                    for span in sorted(ents, key=lambda s: (s.start, -(s.end - s.start))):
                        overlaps = False
                        for existing in filtered_ents:
                            if not (span.end <= existing.start or existing.end <= span.start):
                                overlaps = True
                                break
                        if not overlaps:
                            filtered_ents.append(span)
                    
                    if filtered_ents:
                        doc.ents = filtered_ents
                    else:
                        print(f"⚠️  Skipping document with no valid entities: {text[:50]}...")
                        continue
            
            doc_bin.add(doc)
        
        return doc_bin
    
    def convert_intents_to_spacy(self, data: List[dict], lang: str = "en") -> DocBin:
        """Convert intent data to spaCy DocBin format."""
        nlp = spacy.blank(lang)
        doc_bin = DocBin()
        
        non_binary_count = 0
        
        for item in data:
            text = item["text"]
            doc = nlp.make_doc(text)
            
            # Convert intent scores to binary (0 or 1) for multilabel classification
            # Threshold at 0.5: values >= 0.5 become 1.0, values < 0.5 become 0.0
            binary_cats = {}
            for label, value in item["cats"].items():
                # Ensure values are binary (0.0 or 1.0)
                if isinstance(value, (int, float)):
                    # Convert to binary: >= 0.5 -> 1.0, < 0.5 -> 0.0
                    binary_value = 1.0 if value >= 0.5 else 0.0
                    if value != binary_value and value not in [0.0, 1.0, 0, 1]:
                        non_binary_count += 1
                    binary_cats[label] = binary_value
                else:
                    # Handle non-numeric values
                    binary_cats[label] = 1.0 if value else 0.0
            
            doc.cats = binary_cats
            doc_bin.add(doc)
        
        if non_binary_count > 0:
            print(f"   ⚠️  Converted {non_binary_count} non-binary intent values to binary (threshold: 0.5)")
        
        return doc_bin
    
    def split_data(self, data: List[dict], train_ratio: float = 0.7, 
                   dev_ratio: float = 0.15, test_ratio: float = 0.15) -> Tuple[List[dict], List[dict], List[dict]]:
        """Split data into train/dev/test sets."""
        assert abs(train_ratio + dev_ratio + test_ratio - 1.0) < 0.01, "Ratios must sum to 1.0"
        
        random.shuffle(data)
        total = len(data)
        
        train_end = int(total * train_ratio)
        dev_end = train_end + int(total * dev_ratio)
        
        train_data = data[:train_end]
        dev_data = data[train_end:dev_end]
        test_data = data[dev_end:]
        
        return train_data, dev_data, test_data
    
    def process_entities(self, train_ratio: float = 0.7, dev_ratio: float = 0.15, test_ratio: float = 0.15):
        """Process all entity files and create .spacy files."""
        print("\n" + "="*70)
        print("PROCESSING ENTITY FILES FOR NER TRAINING")
        print("="*70)
        
        entity_files, _ = self.find_jsonl_files()
        
        # Load all entity data
        all_entity_data = []
        for file_path in entity_files:
            data = self.load_entity_data(file_path)
            all_entity_data.extend(data)
        
        if len(all_entity_data) == 0:
            print(f"\n❌ ERROR: No entity data found!")
            print(f"   Searched in: {self.base_dir}")
            print(f"   Found {len(entity_files)} entity files")
            if len(entity_files) == 0:
                print(f"   ⚠️  No *_entities.jsonl files found in {self.base_dir}")
                print(f"   Please check the path and ensure files exist")
            return
        
        print(f"\n✅ Loaded {len(all_entity_data)} entity examples from {len(entity_files)} files")
        print(f"   Unique entity labels: {len(self.stats['entities']['labels'])}")
        
        # Split data
        train_data, dev_data, test_data = self.split_data(
            all_entity_data, train_ratio, dev_ratio, test_ratio
        )
        
        print(f"\n📊 Data Split:")
        print(f"   Train: {len(train_data)} ({len(train_data)/len(all_entity_data)*100:.1f}%)")
        print(f"   Dev:   {len(dev_data)} ({len(dev_data)/len(all_entity_data)*100:.1f}%)")
        print(f"   Test:  {len(test_data)} ({len(test_data)/len(all_entity_data)*100:.1f}%)")
        
        # Convert to spaCy format
        print("\n🔄 Converting to spaCy format...")
        train_docbin = self.convert_entities_to_spacy(train_data)
        dev_docbin = self.convert_entities_to_spacy(dev_data)
        test_docbin = self.convert_entities_to_spacy(test_data)
        
        # Save .spacy files
        train_path = self.output_dir / "entities_train.spacy"
        dev_path = self.output_dir / "entities_dev.spacy"
        test_path = self.output_dir / "entities_test.spacy"
        
        train_docbin.to_disk(train_path)
        dev_docbin.to_disk(dev_path)
        test_docbin.to_disk(test_path)
        
        print(f"✅ Saved entity training files:")
        print(f"   {train_path}")
        print(f"   {dev_path}")
        print(f"   {test_path}")
        
        # Save entity labels
        labels_path = self.output_dir / "entity_labels.txt"
        with open(labels_path, 'w') as f:
            for label in sorted(self.stats['entities']['labels']):
                f.write(f"{label}\n")
        print(f"✅ Saved entity labels: {labels_path}")
        
        return train_path, dev_path, test_path, labels_path
    
    def process_intents(self, train_ratio: float = 0.7, dev_ratio: float = 0.15, test_ratio: float = 0.15):
        """Process all intent files and create .spacy files."""
        print("\n" + "="*70)
        print("PROCESSING INTENT FILES FOR TEXT CLASSIFICATION TRAINING")
        print("="*70)
        
        _, intent_files = self.find_jsonl_files()
        
        # Load all intent data
        all_intent_data = []
        for file_path in intent_files:
            data = self.load_intent_data(file_path)
            all_intent_data.extend(data)
        
        if len(all_intent_data) == 0:
            print(f"\n❌ ERROR: No intent data found!")
            print(f"   Searched in: {self.base_dir}")
            print(f"   Found {len(intent_files)} intent files")
            if len(intent_files) == 0:
                print(f"   ⚠️  No *_intent.jsonl files found in {self.base_dir}")
                print(f"   Please check the path and ensure files exist")
            return
        
        print(f"\n✅ Loaded {len(all_intent_data)} intent examples from {len(intent_files)} files")
        print(f"   Unique intent labels: {len(self.stats['intents']['labels'])}")
        
        # Split data
        train_data, dev_data, test_data = self.split_data(
            all_intent_data, train_ratio, dev_ratio, test_ratio
        )
        
        print(f"\n📊 Data Split:")
        print(f"   Train: {len(train_data)} ({len(train_data)/len(all_intent_data)*100:.1f}%)")
        print(f"   Dev:   {len(dev_data)} ({len(dev_data)/len(all_intent_data)*100:.1f}%)")
        print(f"   Test:  {len(test_data)} ({len(test_data)/len(all_intent_data)*100:.1f}%)")
        
        # Convert to spaCy format
        print("\n🔄 Converting to spaCy format...")
        train_docbin = self.convert_intents_to_spacy(train_data)
        dev_docbin = self.convert_intents_to_spacy(dev_data)
        test_docbin = self.convert_intents_to_spacy(test_data)
        
        # Save .spacy files
        train_path = self.output_dir / "intents_train.spacy"
        dev_path = self.output_dir / "intents_dev.spacy"
        test_path = self.output_dir / "intents_test.spacy"
        
        train_docbin.to_disk(train_path)
        dev_docbin.to_disk(dev_path)
        test_docbin.to_disk(test_path)
        
        print(f"✅ Saved intent training files:")
        print(f"   {train_path}")
        print(f"   {dev_path}")
        print(f"   {test_path}")
        
        # Save intent labels
        labels_path = self.output_dir / "intent_labels.txt"
        with open(labels_path, 'w') as f:
            for label in sorted(self.stats['intents']['labels']):
                f.write(f"{label}\n")
        print(f"✅ Saved intent labels: {labels_path}")
        
        return train_path, dev_path, test_path, labels_path
    
    def generate_report(self):
        """Generate a comprehensive report of the data preparation."""
        report_path = self.output_dir / "preparation_report.txt"
        
        with open(report_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("SPACY TRAINING DATA PREPARATION REPORT\n")
            f.write("="*70 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("ENTITY DATA STATISTICS\n")
            f.write("-"*70 + "\n")
            f.write(f"Total examples: {self.stats['entities']['total']}\n")
            f.write(f"Files processed: {self.stats['entities']['files']}\n")
            f.write(f"Unique labels: {len(self.stats['entities']['labels'])}\n")
            f.write(f"\nTop 20 Entity Labels:\n")
            # Count label frequency would require re-reading files
            f.write("(See entity_labels.txt for full list)\n\n")
            
            f.write("INTENT DATA STATISTICS\n")
            f.write("-"*70 + "\n")
            f.write(f"Total examples: {self.stats['intents']['total']}\n")
            f.write(f"Files processed: {self.stats['intents']['files']}\n")
            f.write(f"Unique labels: {len(self.stats['intents']['labels'])}\n")
            f.write(f"\nTop 20 Intent Labels:\n")
            f.write("(See intent_labels.txt for full list)\n\n")
            
            f.write("NEXT STEPS\n")
            f.write("-"*70 + "\n")
            f.write("1. Review the generated .spacy files\n")
            f.write("2. Create spaCy config files using:\n")
            f.write("   python -m spacy init config config_ner.cfg --lang en --pipeline ner\n")
            f.write("   python -m spacy init config config_intent.cfg --lang en --pipeline textcat\n")
            f.write("3. Train the models using:\n")
            f.write("   python -m spacy train config_ner.cfg --output ./models/ner_model\n")
            f.write("   python -m spacy train config_intent.cfg --output ./models/intent_model\n")
            f.write("4. Evaluate the models on test sets\n")
        
        print(f"\n✅ Generated report: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Prepare JSONL files for spaCy training"
    )
    parser.add_argument(
        "--base-dir",
        default="cyber-train/entities-intent",
        help="Base directory containing JSONL files"
    )
    parser.add_argument(
        "--output-dir",
        default="cyber-train/spacy-training",
        help="Output directory for .spacy files"
    )
    parser.add_argument(
        "--train-ratio",
        type=float,
        default=0.7,
        help="Ratio of training data (default: 0.7)"
    )
    parser.add_argument(
        "--dev-ratio",
        type=float,
        default=0.15,
        help="Ratio of dev data (default: 0.15)"
    )
    parser.add_argument(
        "--test-ratio",
        type=float,
        default=0.15,
        help="Ratio of test data (default: 0.15)"
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
    
    args = parser.parse_args()
    
    # Validate ratios
    if abs(args.train_ratio + args.dev_ratio + args.test_ratio - 1.0) > 0.01:
        print("❌ Error: train_ratio + dev_ratio + test_ratio must equal 1.0")
        return
    
    preparer = SpacyDataPreparer(args.base_dir, args.output_dir)
    
    if not args.intents_only:
        preparer.process_entities(args.train_ratio, args.dev_ratio, args.test_ratio)
    
    if not args.entities_only:
        preparer.process_intents(args.train_ratio, args.dev_ratio, args.test_ratio)
    
    preparer.generate_report()
    
    print("\n" + "="*70)
    print("✅ DATA PREPARATION COMPLETE!")
    print("="*70)


if __name__ == "__main__":
    main()

