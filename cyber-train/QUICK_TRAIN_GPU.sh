#!/bin/bash
# Quick training script with GPU support
# Run from PROJECT ROOT (not cyber-train directory)

set -e

echo "=========================================="
echo "QUICK TRAINING WITH GPU"
echo "=========================================="

# Check if we're in project root
if [ ! -d "cyber-train" ]; then
    echo "❌ Error: Must run from project root (where cyber-train/ directory exists)"
    exit 1
fi

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Error: venv not found. Create it first: python3 -m venv venv"
    exit 1
fi

# Step 1: Prepare training data
echo ""
echo "=========================================="
echo "Step 1: Preparing training data..."
echo "=========================================="
python3 cyber-train/prepare_spacy_training.py

# Step 2: Train models (creates configs and trains)
echo ""
echo "=========================================="
echo "Step 2: Training models (with GPU)..."
echo "=========================================="
python3 cyber-train/train_spacy_models.py --gpu

# Step 3: Test models
echo ""
echo "=========================================="
echo "Step 3: Testing models..."
echo "=========================================="
python3 cyber-train/comprehensive_test_suite.py --comprehensive

echo ""
echo "=========================================="
echo "✅ TRAINING COMPLETE!"
echo "=========================================="
echo ""
echo "Models saved to:"
echo "  - cyber-train/models/ner_model/model-best/"
echo "  - cyber-train/models/intent_model/model-best/"

