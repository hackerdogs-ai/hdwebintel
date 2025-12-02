#!/bin/bash
# Improved training script with better configuration

set -e

echo "======================================================================"
echo "IMPROVED MODEL TRAINING"
echo "======================================================================"

# Check if pretrained model is available
echo ""
echo "📦 Checking for pretrained vectors..."
if python3 -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
    echo "✅ en_core_web_sm found"
    USE_PRETRAINED=true
else
    echo "⚠️  en_core_web_sm not found. Downloading..."
    python3 -m spacy download en_core_web_sm
    USE_PRETRAINED=true
fi

# Prepare training data if needed
if [ ! -f "cyber-train/spacy-training/entities_train.spacy" ]; then
    echo ""
    echo "📊 Preparing training data..."
    python3 cyber-train/prepare_spacy_training.py --entities-only
fi

if [ ! -f "cyber-train/spacy-training/intents_train.spacy" ]; then
    echo ""
    echo "📊 Preparing intent training data..."
    python3 cyber-train/prepare_spacy_training.py --intents-only
fi

# Train NER model with improved config
echo ""
echo "======================================================================"
echo "TRAINING NER MODEL (IMPROVED CONFIG)"
echo "======================================================================"

if [ "$USE_PRETRAINED" = true ]; then
    CONFIG="cyber-train/models/configs/config_ner_improved.cfg"
    echo "Using improved config with pretrained vectors"
else
    CONFIG="cyber-train/models/configs/config_ner.cfg"
    echo "Using basic config (pretrained vectors not available)"
fi

python3 -m spacy train "$CONFIG" \
    --output cyber-train/models/ner_model_improved \
    --paths.train cyber-train/spacy-training/entities_train.spacy \
    --paths.dev cyber-train/spacy-training/entities_dev.spacy \
    --gpu-id 0 2>/dev/null || python3 -m spacy train "$CONFIG" \
    --output cyber-train/models/ner_model_improved \
    --paths.train cyber-train/spacy-training/entities_train.spacy \
    --paths.dev cyber-train/spacy-training/entities_dev.spacy

echo ""
echo "✅ NER model training complete!"
echo "   Model saved to: cyber-train/models/ner_model_improved/model-best"

# Train Intent model
echo ""
echo "======================================================================"
echo "TRAINING INTENT MODEL"
echo "======================================================================"

python3 -m spacy train cyber-train/models/configs/config_intent.cfg \
    --output cyber-train/models/intent_model_improved \
    --paths.train cyber-train/spacy-training/intents_train.spacy \
    --paths.dev cyber-train/spacy-training/intents_dev.spacy \
    --gpu-id 0 2>/dev/null || python3 -m spacy train cyber-train/models/configs/config_intent.cfg \
    --output cyber-train/models/intent_model_improved \
    --paths.train cyber-train/spacy-training/intents_train.spacy \
    --paths.dev cyber-train/spacy-training/intents_dev.spacy

echo ""
echo "✅ Intent model training complete!"
echo "   Model saved to: cyber-train/models/intent_model_improved/model-best"

echo ""
echo "======================================================================"
echo "✅ TRAINING COMPLETE!"
echo "======================================================================"
echo ""
echo "📊 Next steps:"
echo "   1. Test the improved models:"
echo "      python3 cyber-train/test_models.py --test-suite"
echo ""
echo "   2. Compare with previous models"
echo "   3. Evaluate on test set"
echo ""


