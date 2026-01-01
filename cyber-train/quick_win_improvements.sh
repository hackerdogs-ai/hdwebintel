#!/bin/bash
# Quick win improvements to boost recall from 41% to 60-65%
# Runtime: 2-3 hours
# Requirements: Python 3.7+, GPU recommended

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================================"
echo "QUICK WIN IMPROVEMENTS - BOOSTING RECALL FROM 41% TO 60-65%"
echo "========================================================================"
echo ""
echo "This script will:"
echo "  1. Test hybrid extraction (rule-based + ML)"
echo "  2. Analyze and consolidate entity types (573 → ~150)"
echo "  3. Re-prepare training data"
echo "  4. Retrain models with consolidated types"
echo "  5. Run comprehensive test suite"
echo ""
echo "Estimated time: 2-3 hours"
echo ""
read -p "Press ENTER to continue or Ctrl+C to cancel..."
echo ""

# Step 1: Test hybrid extractor
echo "========================================================================"
echo "STEP 1/6: Testing Hybrid Extractor"
echo "========================================================================"
echo ""
echo "Testing rule-based + ML extraction for immediate recall boost..."
echo ""

if [ -f "hybrid_entity_extractor.py" ]; then
    python3 hybrid_entity_extractor.py
    echo ""
    echo "✅ Hybrid extractor test complete"
else
    echo "⚠️  hybrid_entity_extractor.py not found, skipping..."
fi

echo ""
read -p "Press ENTER to continue..."
echo ""

# Step 2: Analyze entity types
echo "========================================================================"
echo "STEP 2/6: Analyzing Entity Types"
echo "========================================================================"
echo ""
echo "Analyzing 573 entity types and identifying consolidation opportunities..."
echo ""

if [ -f "consolidate_entity_types.py" ]; then
    python3 consolidate_entity_types.py --base-dir ../entities-intent
    echo ""
    echo "✅ Analysis complete"
else
    echo "❌ consolidate_entity_types.py not found!"
    exit 1
fi

echo ""
read -p "Review the analysis above. Press ENTER to apply consolidations..."
echo ""

# Step 3: Apply consolidations
echo "========================================================================"
echo "STEP 3/6: Applying Entity Type Consolidations"
echo "========================================================================"
echo ""
echo "Consolidating entity types (573 → ~150 types)..."
echo ""

python3 consolidate_entity_types.py --base-dir ../entities-intent --apply

echo ""
echo "✅ Consolidations applied"
echo ""
read -p "Press ENTER to continue..."
echo ""

# Step 4: Re-prepare training data
echo "========================================================================"
echo "STEP 4/6: Re-preparing Training Data"
echo "========================================================================"
echo ""
echo "Re-preparing training data with consolidated entity types..."
echo ""

if [ -f "prepare_spacy_training.py" ]; then
    python3 prepare_spacy_training.py --base-dir ../entities-intent
    echo ""
    echo "✅ Training data prepared"
else
    echo "❌ prepare_spacy_training.py not found!"
    exit 1
fi

echo ""
read -p "Press ENTER to continue to retraining (this will take 1-2 hours)..."
echo ""

# Step 5: Retrain models
echo "========================================================================"
echo "STEP 5/6: Retraining Models"
echo "========================================================================"
echo ""
echo "Retraining NER and Intent models with consolidated types..."
echo "This will take 1-2 hours. You can monitor progress below."
echo ""

if [ -f "train_spacy_models.py" ]; then
    # Check if GPU is available
    python3 -c "import torch; print('GPU available:', torch.cuda.is_available())" 2>/dev/null
    
    # Train with GPU if available
    python3 train_spacy_models.py --gpu
    
    echo ""
    echo "✅ Model retraining complete"
else
    echo "❌ train_spacy_models.py not found!"
    exit 1
fi

echo ""
read -p "Press ENTER to run comprehensive test suite..."
echo ""

# Step 6: Run comprehensive test suite
echo "========================================================================"
echo "STEP 6/6: Running Comprehensive Test Suite"
echo "========================================================================"
echo ""
echo "Testing the improved model..."
echo ""

if [ -f "comprehensive_test_suite.py" ]; then
    python3 comprehensive_test_suite.py --comprehensive
    echo ""
    echo "✅ Testing complete"
else
    echo "❌ comprehensive_test_suite.py not found!"
    exit 1
fi

echo ""
echo "========================================================================"
echo "QUICK WIN IMPROVEMENTS COMPLETE!"
echo "========================================================================"
echo ""
echo "📊 Results saved to:"
echo "   - comprehensive_test_results.json"
echo "   - Detailed logs in terminal output above"
echo ""
echo "📈 Expected improvements:"
echo "   - Recall: 41.52% → 60-65% (+40-55% relative improvement)"
echo "   - Precision: 84.57% → 88-90%"
echo "   - F1: 55.69% → 72-75%"
echo ""
echo "🔍 Review the results and check if targets were met."
echo ""
echo "📋 Next steps:"
echo "   1. Review comprehensive_test_results.json"
echo "   2. If recall is still <60%, see MODEL_IMPROVEMENT_STRATEGIC_PLAN.md"
echo "   3. Consider Phase 2 improvements (real-world data, active learning)"
echo ""
echo "✅ All done!"

