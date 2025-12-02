# 🚀 Quick Start Guide: Training Pipeline

**Step-by-step procedure to prepare data, train models, and test them.**

---

## Prerequisites

```bash
# 1. Activate virtual environment
cd /Users/tredkar/Documents/GitHub/hdwebintel
source venv/bin/activate

# 2. Verify you're in the project root
pwd  # Should show: /Users/tredkar/Documents/GitHub/hdwebintel
```

---

## Step 1: Prepare Training Data

**Convert JSONL files to spaCy format**

```bash
# From project root
python3 cyber-train/prepare_spacy_training.py
```

**What this does:**
- Loads all entity and intent JSONL files from `cyber-train/entities-intent/`
- Converts to `.spacy` binary format
- Splits into train/dev/test (70/15/15)
- Saves to `cyber-train/models/training_data/`

**Expected output:**
```
✅ Loaded 20922 entity examples from 49 files
✅ Loaded 18716 intent examples from 49 files
✅ Saved entity training files
✅ Saved intent training files
```

**Verify:**
```bash
ls -lh cyber-train/models/training_data/
# Should see:
# - entities_train.spacy
# - entities_dev.spacy
# - entities_test.spacy
# - intents_train.spacy
# - intents_dev.spacy
# - intents_test.spacy
```

---

## Step 2: Train Models (with GPU)

**Create configs and train both NER and Intent models**

```bash
# From project root
python3 cyber-train/train_spacy_models.py --gpu
```

**What this does:**
- Creates spaCy config files
- Trains NER model (extracts entities)
- Trains Intent model (classifies intents)
- Uses GPU if available (faster training)

**Expected output:**
```
✅ NER Model trained
✅ Intent Model trained
✅ Models saved to cyber-train/models/ner_model/ and cyber-train/models/intent_model/
```

**Training time:**
- NER: 1-3 hours (depending on GPU)
- Intent: 30-60 minutes

**Verify:**
```bash
ls -lh cyber-train/models/ner_model/model-best/
ls -lh cyber-train/models/intent_model/model-best/
```

---

## Step 3: Test Models

**Run comprehensive test suite**

```bash
# From project root
python3 cyber-train/comprehensive_test_suite.py --comprehensive
```

**What this does:**
- Tests with 30+ different input types
- Natural language, technical, casual queries
- OSINT and cybersecurity scenarios
- Edge cases

**Expected output:**
```
✅ Test Results Summary
✅ Entity extraction accuracy
✅ Intent classification accuracy
✅ False positive rate
```

**Interactive testing:**
```bash
# Test single query
python3 cyber-train/comprehensive_test_suite.py --text "Check IP 192.168.1.1 for threats"

# Interactive mode
python3 cyber-train/comprehensive_test_suite.py --interactive
```

---

## Complete Command Sequence

**Run everything in order:**

```bash
# 1. Activate environment
cd /Users/tredkar/Documents/GitHub/hdwebintel
source venv/bin/activate

# 2. Prepare data
python3 cyber-train/prepare_spacy_training.py

# 3. Train models (with GPU)
python3 cyber-train/train_spacy_models.py --gpu

# 4. Test models
python3 cyber-train/comprehensive_test_suite.py --comprehensive
```

---

## Alternative: Use Shell Script (All-in-One)

**If you prefer a single command:**

```bash
cd /Users/tredkar/Documents/GitHub/hdwebintel
source venv/bin/activate
./cyber-train/QUICK_TRAIN_GPU.sh
```

**Note:** This script runs all steps automatically.

---

## Troubleshooting

### If prepare_spacy_training.py fails:
- Make sure you're in project root: `/Users/tredkar/Documents/GitHub/hdwebintel`
- Check that `cyber-train/entities-intent/` exists and has JSONL files

### If training fails:
- Check GPU availability: `python3 -c "import torch; print(torch.cuda.is_available())"`
- Use CPU instead: Remove `--gpu` flag
- Check disk space: Training creates large model files

### If testing fails:
- Make sure models exist: `ls cyber-train/models/ner_model/model-best/`
- Check model paths in test script

---

## Expected File Structure After Completion

```
cyber-train/
├── entities-intent/          # Source JSONL files
├── models/
│   ├── training_data/        # Prepared .spacy files
│   │   ├── entities_train.spacy
│   │   ├── entities_dev.spacy
│   │   ├── entities_test.spacy
│   │   ├── intents_train.spacy
│   │   ├── intents_dev.spacy
│   │   └── intents_test.spacy
│   ├── ner_model/            # Trained NER model
│   │   └── model-best/
│   └── intent_model/         # Trained Intent model
│       └── model-best/
└── comprehensive_test_suite.py
```

---

## Next Steps

After successful training and testing:

1. **Review training metrics:**
   ```bash
   cat cyber-train/models/ner_model/training.log
   ```

2. **Evaluate on test set:**
   ```bash
   python3 cyber-train/test_models.py --evaluate-ner cyber-train/models/training_data/entities_test.spacy
   ```

3. **Deploy to production** (see `step-by-step-training-to-production.md`)

---

**That's it! Follow these steps in order and you'll have trained models ready to use.** ✅

