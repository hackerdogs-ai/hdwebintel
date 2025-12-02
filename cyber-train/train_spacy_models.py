#!/usr/bin/env python3
"""
Script to train spaCy NER and Intent Classification models
for Cybersecurity and OSINT use cases.

This script:
1. Creates spaCy config files
2. Trains NER model
3. Trains Intent Classification model
4. Evaluates models
5. Generates training reports
"""

import subprocess
import sys
from pathlib import Path
import argparse
from datetime import datetime


def run_command(cmd: list, description: str, show_output: bool = True):
    """Run a command and handle errors."""
    print(f"\n{'='*70}")
    print(f"{description}")
    print(f"{'='*70}")
    print(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error: {description}")
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        return False
    else:
        if show_output and result.stdout:
            print(result.stdout)
        return True


def create_ner_config(output_path: Path, train_path: Path, dev_path: Path, 
                     labels_path: Path, gpu: bool = False):
    """Create spaCy config for NER training."""
    print("\n📝 Creating NER config file...")
    
    # Read entity labels
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f if line.strip()]
    
    # Create config using spaCy CLI
    # Use "efficiency" to avoid requiring large model (en_core_web_lg)
    # User can manually edit config later if they want to use large model
    cmd = [
        sys.executable, "-m", "spacy", "init", "config",
        str(output_path),
        "--lang", "en",
        "--pipeline", "ner",
        "--optimize", "efficiency",  # Changed: always use efficiency to avoid en_core_web_lg requirement
        "--force"  # Overwrite existing config
    ]
    
    if not run_command(cmd, "Creating base NER config"):
        return False
    
    # Note: Labels will be auto-detected from training data
    # But we can manually add them if needed
    print(f"✅ Config created: {output_path}")
    print(f"   Labels will be auto-detected from training data")
    print(f"   Total labels: {len(labels)}")
    print(f"   Using textcat_multilabel (multiple intents per document)")
    
    return True


def create_intent_config(output_path: Path, train_path: Path, dev_path: Path,
                        labels_path: Path, gpu: bool = False):
    """Create spaCy config for Intent Classification training."""
    print("\n📝 Creating Intent Classification config file...")
    
    # Read intent labels
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f if line.strip()]
    
    # Create config using spaCy CLI
    # Note: textcat_multilabel is needed for multi-label classification
    # Use "efficiency" to avoid requiring large model (en_core_web_lg)
    cmd = [
        sys.executable, "-m", "spacy", "init", "config",
        str(output_path),
        "--lang", "en",
        "--pipeline", "textcat_multilabel",  # Changed from textcat to textcat_multilabel
        "--optimize", "efficiency"  # Changed: always use efficiency to avoid en_core_web_lg requirement
    ]
    
    if not run_command(cmd, "Creating base Intent Classification config"):
        # Fallback: try with textcat if multilabel fails
        print("⚠️  Trying with textcat instead of textcat_multilabel...")
        cmd = [
            sys.executable, "-m", "spacy", "init", "config",
            str(output_path),
            "--lang", "en",
            "--pipeline", "textcat",
            "--optimize", "efficiency" if not gpu else "accuracy"
        ]
        if not run_command(cmd, "Creating base Intent Classification config (fallback)"):
            return False
    
    print(f"✅ Config created: {output_path}")
    print(f"   Labels will be auto-detected from training data")
    print(f"   Total labels: {len(labels)}")
    print(f"   Note: Using multilabel classification (multiple intents per text)")
    
    return True


def train_ner_model(config_path: Path, output_dir: Path, train_path: Path, 
                   dev_path: Path, gpu: bool = False):
    """Train NER model."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        sys.executable, "-m", "spacy", "train",
        str(config_path),
        "--output", str(output_dir),
        "--paths.train", str(train_path),
        "--paths.dev", str(dev_path),
    ]
    
    if gpu:
        cmd.append("--gpu-id")
        cmd.append("0")
    
    return run_command(cmd, "Training NER Model")


def train_intent_model(config_path: Path, output_dir: Path, train_path: Path,
                      dev_path: Path, gpu: bool = False):
    """Train Intent Classification model."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        sys.executable, "-m", "spacy", "train",
        str(config_path),
        "--output", str(output_dir),
        "--paths.train", str(train_path),
        "--paths.dev", str(dev_path),
    ]
    
    if gpu:
        cmd.append("--gpu-id")
        cmd.append("0")
    
    return run_command(cmd, "Training Intent Classification Model")


def evaluate_model(model_path: Path, test_path: Path, task_type: str):
    """Evaluate a trained model on test set."""
    print(f"\n{'='*70}")
    print(f"Evaluating {task_type} Model")
    print(f"{'='*70}")
    
    cmd = [
        sys.executable, "-m", "spacy", "evaluate",
        str(model_path),
        str(test_path),
        "--output", str(model_path.parent / f"{task_type}_evaluation.json")
    ]
    
    return run_command(cmd, f"Evaluating {task_type} model on test set")


def main():
    parser = argparse.ArgumentParser(
        description="Train spaCy models for Cybersecurity and OSINT"
    )
    parser.add_argument(
        "--data-dir",
        default="cyber-train/spacy-training",
        help="Directory containing .spacy training files"
    )
    parser.add_argument(
        "--output-dir",
        default="cyber-train/models",
        help="Output directory for trained models"
    )
    parser.add_argument(
        "--gpu",
        action="store_true",
        help="Use GPU for training"
    )
    parser.add_argument(
        "--ner-only",
        action="store_true",
        help="Only train NER model"
    )
    parser.add_argument(
        "--intent-only",
        action="store_true",
        help="Only train Intent Classification model"
    )
    parser.add_argument(
        "--skip-config",
        action="store_true",
        help="Skip config creation (use existing configs)"
    )
    
    args = parser.parse_args()
    
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for required files
    entity_train = data_dir / "entities_train.spacy"
    entity_dev = data_dir / "entities_dev.spacy"
    entity_test = data_dir / "entities_test.spacy"
    entity_labels = data_dir / "entity_labels.txt"
    
    intent_train = data_dir / "intents_train.spacy"
    intent_dev = data_dir / "intents_dev.spacy"
    intent_test = data_dir / "intents_test.spacy"
    intent_labels = data_dir / "intent_labels.txt"
    
    print("="*70)
    print("SPACY MODEL TRAINING FOR CYBERSECURITY & OSINT")
    print("="*70)
    print(f"Data directory: {data_dir}")
    print(f"Output directory: {output_dir}")
    print(f"GPU: {args.gpu}")
    
    # Train NER model
    if not args.intent_only:
        if not all([entity_train.exists(), entity_dev.exists(), entity_test.exists(), entity_labels.exists()]):
            print(f"\n❌ Missing entity training files in {data_dir}")
            print("   Run prepare_spacy_training.py first")
            return
        
        config_dir = output_dir / "configs"
        config_dir.mkdir(exist_ok=True)
        ner_config = config_dir / "config_ner.cfg"
        
        if not args.skip_config:
            if not create_ner_config(ner_config, entity_train, entity_dev, entity_labels, args.gpu):
                return
        
        ner_model_dir = output_dir / "ner_model"
        if train_ner_model(ner_config, ner_model_dir, entity_train, entity_dev, args.gpu):
            # Evaluate on test set
            best_model = ner_model_dir / "model-best"
            if best_model.exists():
                evaluate_model(best_model, entity_test, "NER")
    
    # Train Intent Classification model
    if not args.ner_only:
        if not all([intent_train.exists(), intent_dev.exists(), intent_test.exists(), intent_labels.exists()]):
            print(f"\n❌ Missing intent training files in {data_dir}")
            print("   Run prepare_spacy_training.py first")
            return
        
        config_dir = output_dir / "configs"
        config_dir.mkdir(exist_ok=True)
        intent_config = config_dir / "config_intent.cfg"
        
        if not args.skip_config:
            if not create_intent_config(intent_config, intent_train, intent_dev, intent_labels, args.gpu):
                # Fallback to manual config creation
                print("\n⚠️  CLI config creation failed, trying manual creation...")
                import subprocess
                fallback_cmd = [
                    sys.executable, "cyber-train/create_config_manual.py",
                    "--type", "intent",
                    "--data-dir", str(data_dir),
                    "--output-dir", str(config_dir)
                ]
                if subprocess.run(fallback_cmd).returncode == 0:
                    print("✅ Manual config creation succeeded")
                else:
                    print("❌ Manual config creation also failed")
                    print("   You can create the config manually or use --skip-config")
                    return
        
        intent_model_dir = output_dir / "intent_model"
        if train_intent_model(intent_config, intent_model_dir, intent_train, intent_dev, args.gpu):
            # Evaluate on test set
            best_model = intent_model_dir / "model-best"
            if best_model.exists():
                evaluate_model(best_model, intent_test, "INTENT")
    
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETE!")
    print("="*70)
    print(f"\nModels saved in: {output_dir}")
    print("\nTo use the models:")
    print("  import spacy")
    print("  nlp_ner = spacy.load('cyber-train/models/ner_model/model-best')")
    print("  nlp_intent = spacy.load('cyber-train/models/intent_model/model-best')")


if __name__ == "__main__":
    main()

