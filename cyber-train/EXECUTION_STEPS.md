# 🚀 Execution Steps - Training to Production

**Status:** ✅ Training data ready with 100% boundary accuracy  
**Date:** December 1, 2024

---

## 📋 Step-by-Step Execution Guide

### **PHASE 1: Data Preparation** ✅ COMPLETE

- [x] Generate entities and intents for all 24 cybersecurity pillars
- [x] Generate entities and intents for all 25 OSINT pillars
- [x] Create entity_types.txt and intent_types.txt
- [x] Add missing entity types (latitude, longitude, nameserver, datacenter, etc.)
- [x] Add missing intent types
- [x] Double training data
- [x] Add negative examples
- [x] Fix all entity boundaries (100% accuracy achieved)
- [x] Remove invalid pattern entities

**Result:** 83,364 entities with 100% boundary accuracy across 49 files

---

### **PHASE 2: Prepare Training Data** ⏳ NEXT STEP

#### Step 1: Install Dependencies
```bash
cd /Users/tredkar/Documents/GitHub/hdwebintel/cyber-train
pip install -r requirements_training.txt
python -m spacy download en_core_web_sm
```

#### Step 2: Prepare spaCy Training Data
```bash
python prepare_spacy_training.py
```

**What this does:**
- Converts JSONL entity and intent data to spaCy DocBin format
- Splits data into train/dev/test sets (80/10/10)
- Handles overlapping entities
- Binarizes intent scores

**Expected output:**
- `models/training_data/entities_train.spacy`
- `models/training_data/entities_dev.spacy`
- `models/training_data/entities_test.spacy`
- `models/training_data/intents_train.spacy`
- `models/training_data/intents_dev.spacy`
- `models/training_data/intents_test.spacy`

---

### **PHASE 3: Train Models** ⏳ NEXT STEP

#### Step 3: Create Model Configurations
```bash
python train_spacy_models.py
```

**What this does:**
- Creates `config_ner.cfg` for NER model
- Creates `config_intent.cfg` for Intent Classification model
- Uses `textcat_multilabel` for multilabel intent classification

#### Step 4: Train NER Model
```bash
python -m spacy train models/configs/config_ner.cfg \
  --output models/ner_model \
  --paths.train models/training_data/entities_train.spacy \
  --paths.dev models/training_data/entities_dev.spacy \
  --gpu-id 0
```

**Expected output:**
- `models/ner_model/model-best/` (best model)
- `models/ner_model/model-last/` (last checkpoint)
- Training metrics and loss curves

**Training time:** ~30-60 minutes (depending on hardware)

#### Step 5: Train Intent Classification Model
```bash
python -m spacy train models/configs/config_intent.cfg \
  --output models/intent_model \
  --paths.train models/training_data/intents_train.spacy \
  --paths.dev models/training_data/intents_dev.spacy \
  --gpu-id 0
```

**Expected output:**
- `models/intent_model/model-best/` (best model)
- `models/intent_model/model-last/` (last checkpoint)
- Training metrics and loss curves

**Training time:** ~15-30 minutes (depending on hardware)

---

### **PHASE 4: Evaluate Models** ⏳ NEXT STEP

#### Step 6: Run Comprehensive Test Suite
```bash
python comprehensive_test_suite.py
```

**What this does:**
- Tests models with 30+ test cases
- Covers natural language, technical, casual, multi-entity inputs
- Tests OSINT and cybersecurity scenarios
- Applies post-processing filters
- Generates accuracy metrics

**Expected output:**
- Test results with precision, recall, F1 scores
- False positive/negative analysis
- Per-entity-type performance metrics

#### Step 7: Interactive Testing (Optional)
```bash
python test_models.py --interactive
```

**What this does:**
- Interactive mode for manual testing
- Test custom queries
- See entity extraction and intent classification results

---

### **PHASE 5: Production Integration** ⏳ NEXT STEP

#### Step 8: Create Production API/Service
```bash
# Create a simple Flask/FastAPI service
# Example structure:
# - app.py (main application)
# - models/ (load trained models)
# - api/ (endpoints for entity extraction and intent classification)
```

**Example API endpoints:**
- `POST /extract-entities` - Extract entities from text
- `POST /classify-intent` - Classify intent from text
- `POST /analyze` - Combined entity extraction + intent classification

#### Step 9: Deploy Models
```bash
# Option 1: Local deployment
python app.py

# Option 2: Docker deployment
docker build -t cyber-intel-api .
docker run -p 5000:5000 cyber-intel-api

# Option 3: Cloud deployment (AWS, GCP, Azure)
# Follow cloud provider's ML model deployment guide
```

---

### **PHASE 6: Continuous Improvement** ⏳ ONGOING

#### Step 10: Monitor Performance
- Track model accuracy in production
- Collect false positive/negative examples
- Monitor entity extraction quality
- Track intent classification accuracy

#### Step 11: Retrain with New Data
- Add new examples from production
- Fix identified issues
- Retrain models periodically
- A/B test new model versions

#### Step 12: Update Training Data
- Add new entity types as needed
- Add new intent types as needed
- Expand training data for low-performing entity types
- Maintain 100% boundary accuracy

---

## 🎯 Quick Start Commands

### Complete Training Pipeline (All Steps)
```bash
# 1. Install dependencies
pip install -r requirements_training.txt
python -m spacy download en_core_web_sm

# 2. Prepare training data
python prepare_spacy_training.py

# 3. Train models
python train_spacy_models.py
python -m spacy train models/configs/config_ner.cfg \
  --output models/ner_model \
  --paths.train models/training_data/entities_train.spacy \
  --paths.dev models/training_data/entities_dev.spacy

python -m spacy train models/configs/config_intent.cfg \
  --output models/intent_model \
  --paths.train models/training_data/intents_train.spacy \
  --paths.dev models/training_data/intents_dev.spacy

# 4. Test models
python comprehensive_test_suite.py
```

---

## 📊 Expected Results

### NER Model Performance
- **Target F1 Score:** >95%
- **Precision:** >95%
- **Recall:** >95%
- **False Positive Rate:** <5%

### Intent Classification Model Performance
- **Target F1 Score:** >95%
- **Accuracy:** >95%
- **Per-Intent Performance:** >90% for all intents

---

## ⚠️ Important Notes

1. **GPU vs CPU:** Training is faster on GPU. Use `--gpu-id 0` for GPU, omit for CPU.

2. **Training Time:** 
   - NER model: ~30-60 minutes
   - Intent model: ~15-30 minutes
   - Total: ~1-2 hours

3. **Model Size:**
   - NER model: ~50-100 MB
   - Intent model: ~20-50 MB
   - Total: ~70-150 MB

4. **Memory Requirements:**
   - Training: 8-16 GB RAM recommended
   - Inference: 2-4 GB RAM

5. **Post-Processing:** Always use `fix_entity_extraction.py` post-processing filter in production to reduce false positives.

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'spacy'"
**Solution:**
```bash
pip install -r requirements_training.txt
```

### Issue: "ValueError: [E1010] Unable to set entity information"
**Solution:** Already fixed in `prepare_spacy_training.py` - uses `filter_spans` to handle overlaps.

### Issue: "ValueError: [E895] The 'textcat' component received multiple labels"
**Solution:** Already fixed - using `textcat_multilabel` in config.

### Issue: Low accuracy after training
**Solution:**
1. Check training data quality (boundaries, labels)
2. Increase training steps
3. Use pretrained vectors (`en_core_web_sm`)
4. Use transformer model (`en_core_web_trf`)
5. Add more training data

---

## ✅ Checklist

Before starting training:
- [x] Training data has 100% boundary accuracy
- [x] All entity types defined in `entity_types.txt`
- [x] All intent types defined in `intent_types.txt`
- [x] Negative examples added
- [x] Invalid pattern entities removed
- [ ] Dependencies installed
- [ ] Training data prepared (spaCy format)
- [ ] Models trained
- [ ] Models tested
- [ ] Models deployed

---

## 📚 Documentation

- **Training Guide:** `SPACY_TRAINING_GUIDE.md`
- **Testing Guide:** `TESTING_GUIDE_COMPREHENSIVE.md`
- **Step-by-Step:** `step-by-step-training-to-production.md`
- **Boundary Accuracy:** `BOUNDARY_ACCURACY_FINAL_REPORT.md`

---

**Ready to execute! Start with Phase 2, Step 1.**

