#!/bin/bash
# Quick Start Script for spaCy Training Pipeline
# This script automates the entire training process

set -e  # Exit on error

echo "=========================================="
echo "spaCy Training Pipeline - Quick Start"
echo "=========================================="
echo ""

# Check if spaCy is installed
if ! python3 -c "import spacy" 2>/dev/null; then
    echo "❌ spaCy not installed. Installing..."
    pip install spacy>=3.7.0
    echo "✅ spaCy installed"
    echo ""
fi

# Step 1: Prepare data
echo "Step 1: Preparing training data..."
python3 cyber-train/prepare_spacy_training.py
echo ""

# Step 2: Train models
echo "Step 2: Training models..."
echo "This may take a while depending on your hardware..."
python3 cyber-train/train_spacy_models.py
echo ""

echo "=========================================="
echo "✅ Training Complete!"
echo "=========================================="
echo ""
echo "Models saved in: cyber-train/models/"
echo "  - NER Model: cyber-train/models/ner_model/model-best"
echo "  - Intent Model: cyber-train/models/intent_model/model-best"
echo ""
echo "To use the models:"
echo "  import spacy"
echo "  nlp = spacy.load('cyber-train/models/ner_model/model-best')"
echo ""


