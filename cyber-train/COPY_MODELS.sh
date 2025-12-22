#!/bin/bash
# Script to copy models to another project

# Configuration
SOURCE_DIR="cyber-train/models"
DEST_DIR="${1:-../your-project/models}"

echo "=========================================="
echo "Copying Models to Another Project"
echo "=========================================="
echo ""
echo "Source: $SOURCE_DIR"
echo "Destination: $DEST_DIR"
echo ""

# Create destination directory
mkdir -p "$DEST_DIR/ner_model"
mkdir -p "$DEST_DIR/intent_model"

# Copy NER model
if [ -d "$SOURCE_DIR/ner_model/model-best" ]; then
    echo "📦 Copying NER model..."
    cp -r "$SOURCE_DIR/ner_model/model-best" "$DEST_DIR/ner_model/"
    echo "✅ NER model copied"
else
    echo "❌ NER model not found at $SOURCE_DIR/ner_model/model-best"
    exit 1
fi

# Copy Intent model
if [ -d "$SOURCE_DIR/intent_model/model-best" ]; then
    echo "📦 Copying Intent model..."
    cp -r "$SOURCE_DIR/intent_model/model-best" "$DEST_DIR/intent_model/"
    echo "✅ Intent model copied"
else
    echo "❌ Intent model not found at $SOURCE_DIR/intent_model/model-best"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Models copied successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Install dependencies: pip install spacy"
echo "2. Use minimal_integration.py or copy the code"
echo "3. Load models: spacy.load('$DEST_DIR/ner_model/model-best')"
echo ""

