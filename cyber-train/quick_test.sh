#!/bin/bash
# Quick test script for trained models
# This script tests the models with sample queries

set -e

echo "=========================================="
echo "Quick Model Test"
echo "=========================================="
echo ""

# Check if models exist
NER_MODEL="cyber-train/models/ner_model/model-best"
INTENT_MODEL="cyber-train/models/intent_model/model-best"

if [ ! -d "$NER_MODEL" ]; then
    echo "❌ NER model not found at: $NER_MODEL"
    exit 1
fi

if [ ! -d "$INTENT_MODEL" ]; then
    echo "⚠️  Intent model not found at: $INTENT_MODEL"
    echo "   You can train it with: python3 cyber-train/train_spacy_models.py --intent-only"
    INTENT_AVAILABLE=false
else
    INTENT_AVAILABLE=true
fi

echo "✅ NER model found"
if [ "$INTENT_AVAILABLE" = true ]; then
    echo "✅ Intent model found"
fi
echo ""

# Run test script
echo "Running test suite..."
echo ""

if [ "$INTENT_AVAILABLE" = true ]; then
    python3 cyber-train/test_models.py --test-suite
else
    echo "Testing NER model only..."
    python3 cyber-train/test_models.py --test-suite 2>&1 | head -100
fi

echo ""
echo "=========================================="
echo "✅ Test Complete!"
echo "=========================================="
echo ""
echo "For more testing options:"
echo "  python3 cyber-train/test_models.py --interactive"
echo "  python3 cyber-train/test_models.py --text 'Your query here'"
echo ""


