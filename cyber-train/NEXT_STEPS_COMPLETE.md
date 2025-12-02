# 🚀 Next Steps - Complete Training Pipeline

## ✅ Current Status

**Data Quality:**
- ✅ Entity Accuracy: **100.00%** (274,937 entities)
- ✅ Intent Accuracy: **99.98%** (151,592 intents)
- ✅ Boundary Issues: **0**
- ✅ Label Issues: **0**
- ✅ Whitespace Issues: **0**
- ✅ Overlap Issues: **0**
- ✅ All 49 entity files verified
- ✅ All 49 intent files verified

**Production Ready:** ✅ YES

---

## 📋 Next Steps (In Order)

### Step 1: Prepare Training Data (Convert JSONL → spaCy Format)

**Purpose:** Convert your JSONL training files into spaCy's optimized binary format (`.spacy` files)

**Command:**
```bash
cd /Users/tredkar/Documents/GitHub/hdwebintel
source venv/bin/activate
python3 cyber-train/prepare_spacy_training.py
```

**What it does:**
- Reads all `*_entities.jsonl` files
- Reads all `*_intent.jsonl` files
- Converts to spaCy `DocBin` format
- Splits into train/dev/test sets (80/10/10)
- Saves to `cyber-train/spacy-training/`

**Expected Output:**
- `entities_train.spacy` - Training data for NER
- `entities_dev.spacy` - Development/validation data
- `entities_test.spacy` - Test data
- `intents_train.spacy` - Training data for Intent Classification
- `intents_dev.spacy` - Development/validation data
- `intents_test.spacy` - Test data

**Time:** ~5-10 minutes

---

### Step 2: Train the Models

**Purpose:** Train both NER and Intent Classification models

**Command (CPU):**
```bash
python3 cyber-train/train_spacy_models.py
```

**Command (GPU - Recommended):**
```bash
python3 cyber-train/train_spacy_models.py --gpu
```

**What it does:**
- Loads prepared training data
- Initializes model with `en_core_web_lg` (large model with vectors)
- Trains NER model (extracts entities)
- Trains Intent Classification model (classifies intents)
- Saves models to `cyber-train/models/ner_model/` and `cyber-train/models/intent_model/`
- Generates evaluation reports

**Expected Training Time:**
- NER Model: 1-3 hours (CPU) / 30-60 minutes (GPU)
- Intent Model: 30-60 minutes (CPU) / 10-20 minutes (GPU)

**Expected Performance:**
- NER F1 Score: > 90%
- Intent F1 Score: > 95%

---

### Step 3: Test the Models

**Purpose:** Verify models work correctly with various input types

**Command:**
```bash
python3 cyber-train/comprehensive_test_suite.py --comprehensive
```

**What it tests:**
- Natural language queries
- Technical queries
- Multi-entity extraction
- Intent classification
- Edge cases
- False positive detection

**Expected Output:**
- Test results report
- Accuracy metrics
- False positive rate
- Per-entity-type performance

---

### Step 4: Evaluate Performance

**Purpose:** Get detailed performance metrics

**Command:**
```bash
python3 cyber-train/test_models.py --evaluate-ner cyber-train/spacy-training/entities_test.spacy
python3 cyber-train/test_models.py --evaluate-intent cyber-train/spacy-training/intents_test.spacy
```

**Key Metrics to Check:**
- ✅ F1 Score > 0.90
- ✅ Precision > 0.90 (low false positives)
- ✅ Recall > 0.90 (finds most entities)
- ✅ False Positive Rate < 2%

---

## 🎯 Quick Start (All-in-One)

If you want to run everything in sequence:

```bash
cd /Users/tredkar/Documents/GitHub/hdwebintel
source venv/bin/activate

# Step 1: Prepare data
python3 cyber-train/prepare_spacy_training.py

# Step 2: Train models (with GPU if available)
python3 cyber-train/train_spacy_models.py --gpu

# Step 3: Test models
python3 cyber-train/comprehensive_test_suite.py --comprehensive
```

---

## 📊 What to Expect

### After Step 1 (Data Preparation):
- ✅ 6 `.spacy` files created in `cyber-train/spacy-training/`
- ✅ Training data split: 80% train, 10% dev, 10% test
- ✅ Ready for training

### After Step 2 (Training):
- ✅ NER model saved to `cyber-train/models/ner_model/`
- ✅ Intent model saved to `cyber-train/models/intent_model/`
- ✅ Evaluation reports generated
- ✅ Training logs available

### After Step 3 (Testing):
- ✅ Comprehensive test results
- ✅ Performance metrics
- ✅ False positive analysis
- ✅ Ready for production use

---

## ⚠️ Important Notes

1. **GPU Training:** Use `--gpu` flag if you have CUDA-capable GPU (much faster)
2. **Base Model:** Ensure `en_core_web_lg` is installed: `python -m spacy download en_core_web_lg`
3. **Training Time:** First training may take 1-3 hours (CPU) or 30-60 minutes (GPU)
4. **Memory:** Ensure sufficient RAM (8GB+ recommended)

---

## 🔍 Troubleshooting

**If preparation fails:**
- Check that all JSONL files are valid JSON
- Verify entity_types.txt and intent_types.txt exist
- Check file permissions

**If training fails:**
- Verify `en_core_web_lg` is installed
- Check GPU availability if using `--gpu`
- Review training logs for errors

**If test fails:**
- Ensure models were trained successfully
- Check model paths are correct
- Verify test data exists

---

## 📈 Success Criteria

✅ **Data Preparation:** All 6 `.spacy` files created successfully
✅ **Training:** F1 scores > 90% for both models
✅ **Testing:** False positive rate < 2%
✅ **Production Ready:** Models perform well on diverse inputs

---

**Ready to proceed? Start with Step 1: Data Preparation**
