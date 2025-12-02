# 📋 Step-by-Step Execution Guide

**Simple, clear steps to run the complete training pipeline.**

---

## 🎯 Quick Reference

```bash
# 1. Activate environment
cd /Users/tredkar/Documents/GitHub/hdwebintel
source venv/bin/activate

# 2. Prepare data
python3 cyber-train/prepare_spacy_training.py

# 3. Train models (GPU)
python3 cyber-train/train_spacy_models.py --gpu

# 4. Test models
python3 cyber-train/comprehensive_test_suite.py --comprehensive
```

---

## 📝 Detailed Steps

### Step 1: Prepare Training Data

**Command:**
```bash
cd /Users/tredkar/Documents/GitHub/hdwebintel
source venv/bin/activate
python3 cyber-train/prepare_spacy_training.py
```

**What it does:**
- Reads all `*_entities.jsonl` and `*_intent.jsonl` files from `cyber-train/entities-intent/`
- Validates data format
- Converts to spaCy `.spacy` binary format
- Splits into train (70%), dev (15%), test (15%)
- Saves to `cyber-train/models/training_data/`

**Success indicators:**
- ✅ "Loaded 20922 entity examples from 49 files"
- ✅ "Loaded 18716 intent examples from 49 files"
- ✅ Files created in `cyber-train/models/training_data/`

**Time:** ~2-5 minutes

---

### Step 2: Train Models

**Command:**
```bash
python3 cyber-train/train_spacy_models.py --gpu
```

**What it does:**
- Creates spaCy config files for NER and Intent models
- Trains NER model (entity extraction)
- Trains Intent model (intent classification)
- Uses GPU if available (much faster)

**Success indicators:**
- ✅ "NER Model trained successfully"
- ✅ "Intent Classification Model trained successfully"
- ✅ Models saved to `cyber-train/models/ner_model/model-best/` and `cyber-train/models/intent_model/model-best/`

**Time:** 
- NER: 1-3 hours (GPU) or 3-6 hours (CPU)
- Intent: 30-60 minutes (GPU) or 1-2 hours (CPU)

**If GPU not available:**
```bash
# Remove --gpu flag for CPU training
python3 cyber-train/train_spacy_models.py
```

---

### Step 3: Test Models

**Command:**
```bash
python3 cyber-train/comprehensive_test_suite.py --comprehensive
```

**What it does:**
- Tests models with 30+ different input types
- Natural language queries
- Technical queries
- OSINT scenarios
- Cybersecurity scenarios
- Edge cases

**Success indicators:**
- ✅ Test results summary displayed
- ✅ Entity extraction accuracy reported
- ✅ Intent classification accuracy reported
- ✅ False positive rate reported

**Time:** ~5-10 minutes

**Other test options:**
```bash
# Test single query
python3 cyber-train/comprehensive_test_suite.py --text "Check IP 192.168.1.1"

# Interactive mode
python3 cyber-train/comprehensive_test_suite.py --interactive
```

---

## 🔄 All-in-One Script

**Instead of running steps individually, use the script:**

```bash
cd /Users/tredkar/Documents/GitHub/hdwebintel
source venv/bin/activate
./cyber-train/QUICK_TRAIN_GPU.sh
```

This runs all three steps automatically.

---

## ✅ Verification Checklist

After each step, verify:

### After Step 1 (Prepare):
```bash
ls -lh cyber-train/models/training_data/
# Should see 6 .spacy files + 2 .txt label files
```

### After Step 2 (Train):
```bash
ls -lh cyber-train/models/ner_model/model-best/
ls -lh cyber-train/models/intent_model/model-best/
# Should see model files (config.cfg, model files, etc.)
```

### After Step 3 (Test):
- Check console output for accuracy metrics
- Review test results summary

---

## 🐛 Common Issues

### Issue: "No module named 'spacy'"
**Fix:**
```bash
source venv/bin/activate
pip install -r cyber-train/requirements_training.txt
```

### Issue: "No entity files found"
**Fix:**
- Make sure you're in project root: `/Users/tredkar/Documents/GitHub/hdwebintel`
- Check `cyber-train/entities-intent/` exists and has JSONL files

### Issue: GPU not available
**Fix:**
- Remove `--gpu` flag
- Training will use CPU (slower but works)

### Issue: Out of memory during training
**Fix:**
- Reduce batch size in config
- Use CPU instead of GPU
- Close other applications

---

## 📊 Expected Results

**After successful completion:**

- **NER Model:**
  - F1 Score: ~95%+
  - Precision: ~90%+
  - Recall: ~90%+

- **Intent Model:**
  - F1 Score: ~99%+
  - Accuracy: ~99%+

- **Files Created:**
  - 6 `.spacy` training files
  - 2 trained model directories
  - Training logs and reports

---

## 🚀 Next Steps

After training and testing:

1. **Review training logs:**
   ```bash
   cat cyber-train/models/ner_model/training.log
   ```

2. **Evaluate on test set:**
   ```bash
   python3 cyber-train/test_models.py --evaluate-ner cyber-train/models/training_data/entities_test.spacy
   ```

3. **Use models in your application:**
   ```python
   import spacy
   ner_model = spacy.load("cyber-train/models/ner_model/model-best")
   intent_model = spacy.load("cyber-train/models/intent_model/model-best")
   ```

---

**That's it! Follow these steps in order for successful training.** ✅

