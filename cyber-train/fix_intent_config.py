#!/usr/bin/env python3
"""
Fix intent classification config to use textcat_multilabel instead of textcat.
This is needed because our training data has multiple intents per document.
"""

import re
from pathlib import Path
import sys


def fix_config(config_path: Path):
    """Fix config file to use textcat_multilabel."""
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return False
    
    print(f"📝 Fixing config file: {config_path}")
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Replace pipeline
    content = content.replace(
        'pipeline = ["tok2vec","textcat"]',
        'pipeline = ["tok2vec","textcat_multilabel"]'
    )
    
    # Replace component section header
    content = content.replace(
        '[components.textcat]',
        '[components.textcat_multilabel]'
    )
    
    # Replace factory
    content = content.replace(
        'factory = "textcat"',
        'factory = "textcat_multilabel"'
    )
    
    # Replace scorer
    content = content.replace(
        'scorer = {"@scorers":"spacy.textcat_scorer.v1"}',
        'scorer = {"@scorers":"spacy.textcat_multilabel_scorer.v1"}'
    )
    
    # Update exclusive_classes
    content = re.sub(
        r'exclusive_classes = true',
        'exclusive_classes = false',
        content
    )
    
    # Update all component references
    content = re.sub(
        r'\[components\.textcat\.model\]',
        '[components.textcat_multilabel.model]',
        content
    )
    content = re.sub(
        r'\[components\.textcat\.model\.tok2vec\]',
        '[components.textcat_multilabel.model.tok2vec]',
        content
    )
    content = re.sub(
        r'\[components\.textcat\.model\.linear_model\]',
        '[components.textcat_multilabel.model.linear_model]',
        content
    )
    
    # Update architecture reference if present
    content = content.replace(
        '@architectures = "spacy.TextCatEnsemble.v2"',
        '@architectures = "spacy.TextCatEnsemble.v2"'
    )
    
    if content != original_content:
        # Backup original
        backup_path = config_path.with_suffix('.cfg.backup')
        with open(backup_path, 'w') as f:
            f.write(original_content)
        print(f"   Created backup: {backup_path}")
        
        # Write fixed config
        with open(config_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Config file fixed!")
        print(f"   Changed: textcat → textcat_multilabel")
        print(f"   Updated: exclusive_classes = false")
        return True
    else:
        print("⚠️  No changes needed (config already correct)")
        return True


if __name__ == "__main__":
    config_path = Path("cyber-train/models/configs/config_intent.cfg")
    
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    
    if fix_config(config_path):
        print("\n✅ You can now retrain the intent model:")
        print("   python3 cyber-train/train_spacy_models.py --intent-only --skip-config")
        sys.exit(0)
    else:
        sys.exit(1)


