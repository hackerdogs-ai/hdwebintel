# 🚀 Step-by-Step Training to Production Guide

**Complete guide for training, improving, and deploying spaCy NER and Intent Classification models for Cybersecurity and OSINT.**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Data Preparation](#data-preparation)
4. [Model Training](#model-training)
5. [Testing & Evaluation](#testing--evaluation)
6. [Avoiding Overfitting](#avoiding-overfitting)
7. [Continuous Improvement](#continuous-improvement)
8. [Real-World Testing](#real-world-testing)
9. [Production Deployment](#production-deployment)
10. [What to Avoid](#what-to-avoid)
11. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This guide covers the complete lifecycle of training spaCy models for cybersecurity and OSINT, from initial data preparation through production deployment and continuous improvement.

### Models Created

1. **NER Model**: Extracts entities (IP addresses, CVEs, threat actors, domains, etc.)
2. **Intent Classification Model**: Classifies user queries into intents (investigate, detect, monitor, etc.)

### Current Performance

- **NER F1 Score**: 95.44% ✅
- **Intent F1 Score**: 99.89% ✅
- **False Positive Rate**: 6.1% (target: <2%)
- **Training Examples**: 169,292 entities, 18,716 intents

---

## 🔧 Prerequisites

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r cyber-train/requirements_training.txt

# Download base model
python -m spacy download en_core_web_sm
```

### 2. Directory Structure

```
cyber-train/
├── entities-intent/          # Training data (JSONL files)
│   ├── ai_security/
│   │   ├── ai_security_entities.jsonl
│   │   └── ai_security_intent.jsonl
│   └── ...
├── spacy-training/           # Prepared data (.spacy files)
├── models/                   # Trained models
│   ├── ner_model/
│   └── intent_model/
└── scripts/                  # Training scripts
```

---

## 📊 Data Preparation

### Step 1: Understand Data Requirements

#### Data Composition (Critical!)

**Ideal Training Data Distribution:**
```
60-70% Positive Examples
  • Sentences WITH entities
  • Correctly labeled
  • Diverse patterns

20-30% Negative Examples (TRUE NEGATIVES) ← CRITICAL!
  • Sentences with NO entities
  • Explicitly empty entities: []
  • Help model learn boundaries
  • Prevents overfitting

10% Ambiguous/Edge Cases
  • Borderline cases
  • Help model learn boundaries
  • Improve generalization
```

**Why This Matters:**
- **Without negative examples**: Model over-extracts (false positives)
- **Without edge cases**: Model overfits to clean data
- **With proper distribution**: Model learns boundaries and generalizes

### Step 2: Create Training Data

#### Entity Data Format (JSONL)

```json
{"text": "APT41 used WannaCry malware to attack IP 192.168.1.1", "entities": [[0, 5, "THREAT_ACTOR"], [11, 19, "MALWARE_TYPE"], [35, 45, "IP_ADDRESS"]]}
{"text": "Can you help me with this?", "entities": []}
```

**Key Points:**
- Each line is a JSON object
- `entities` is a list of `[start, end, label]` tuples
- Empty `entities: []` for negative examples (true negatives)

#### Intent Data Format (JSONL)

```json
{"text": "Investigate the suspicious IP address 192.168.1.1", "cats": {"INVESTIGATE": 1.0, "DETECT": 0.8, "ANALYZE": 0.7}}
{"text": "What is the status?", "cats": {"CHECK": 0.3}}
```

**Key Points:**
- `cats` is a dictionary of intent labels with scores (0.0 to 1.0)
- Multiple intents can be active (multilabel)
- Scores >= 0.5 are considered positive

### Step 3: Add Negative Examples

**Critical Step!** Add true negatives to prevent overfitting:

```bash
# Create separate negative examples file
python3 cyber-train/add_negative_examples.py --create-separate --count 300

# Add to existing files (10% of each)
python3 cyber-train/add_negative_examples.py --add-to-existing
```

**Why This Matters:**
- Model learns what TO extract (positive examples)
- Model learns what NOT to extract (negative examples)
- Model learns boundaries (prevents overfitting)

### Step 4: Prepare Training Data

```bash
# Convert JSONL to spaCy format
python3 cyber-train/prepare_spacy_training.py
```

**What This Does:**
- Validates all JSONL files
- Converts to `.spacy` binary format
- Splits into train/dev/test (70/15/15 by default)
- Generates statistics report

**Output:**
```
spacy-training/
├── entities_train.spacy
├── entities_dev.spacy
├── entities_test.spacy
├── intents_train.spacy
├── intents_dev.spacy
├── intents_test.spacy
└── preparation_report.txt
```

### Step 5: Review Data Quality

```bash
cat cyber-train/spacy-training/preparation_report.txt
```

**Check:**
- ✅ Total examples loaded
- ✅ Number of unique labels
- ✅ Train/dev/test split ratios
- ✅ Negative examples included (20-30%)
- ✅ No format errors

---

## 🎓 Model Training

### Step 1: Create Training Configuration

```bash
# Create config files
python3 cyber-train/train_spacy_models.py
```

**Or use improved config:**

```bash
# Use improved config with pretrained vectors
./cyber-train/train_better.sh
```

### Step 2: Train Models

```bash
# Train both models
python3 cyber-train/train_spacy_models.py

# Or use improved training
./cyber-train/train_better.sh
```

**Training Process:**
1. Loads training data
2. Initializes model architecture
3. Trains for multiple epochs
4. Evaluates on dev set
5. Saves best model
6. Generates evaluation report

**Expected Training Time:**
- NER Model: 1-3 hours (depending on data size)
- Intent Model: 30-60 minutes

### Step 3: Review Training Output

```bash
# Check training logs
cat cyber-train/models/ner_model/training.log

# Review evaluation
cat cyber-train/models/ner_model/NER_evaluation.json | python3 -m json.tool
```

**Key Metrics:**
- **F1 Score**: Should be > 0.90 for good performance
- **Precision**: Should be > 0.90 (few false positives)
- **Recall**: Should be > 0.90 (finds most entities)

---

## 🧪 Testing & Evaluation

### Step 1: Run Comprehensive Test Suite

```bash
# Test with multiple input types
python3 cyber-train/comprehensive_test_suite.py --comprehensive

# Interactive testing
python3 cyber-train/comprehensive_test_suite.py --interactive

# Test single query
python3 cyber-train/comprehensive_test_suite.py --text "Check IP 192.168.1.1 for threats"
```

**Test Categories:**
- Natural language queries
- Technical queries
- Casual/informal queries
- Multi-entity queries
- OSINT queries
- Cybersecurity queries
- Edge cases

### Step 2: Evaluate on Test Set

```bash
# Evaluate NER model
python3 cyber-train/test_models.py --evaluate-ner cyber-train/spacy-training/entities_test.spacy

# Evaluate Intent model
python3 cyber-train/test_models.py --evaluate-intent cyber-train/spacy-training/intents_test.spacy
```

### Step 3: Review Results

**Check for:**
- ✅ Overall F1 score > 0.90
- ✅ False positive rate < 2%
- ✅ Per-entity-type performance
- ✅ Edge case handling

---

## ⚠️ Avoiding Overfitting

### What is Overfitting?

**Overfitting occurs when:**
- Model memorizes training data instead of learning patterns
- Model performs well on training data but poorly on new data
- Model fails on edge cases
- Model doesn't generalize

### How to Avoid Overfitting

#### 1. Add True Negatives (Critical!)

**Problem:** Model only sees positive examples → over-extracts

**Solution:** Add 20-30% negative examples

```bash
python3 cyber-train/add_negative_examples.py --add-to-existing
```

**Why This Works:**
- Model learns what TO extract (positive examples)
- Model learns what NOT to extract (negative examples)
- Model learns boundaries naturally

#### 2. Keep Diverse Training Data

**Don't over-clean:**
- Keep ambiguous cases (help learn boundaries)
- Keep edge cases (improve generalization)
- Keep some false positive patterns (but label correctly)

**Selective Cleaning:**
```bash
# Only remove CLEARLY wrong labels
python3 cyber-train/clean_training_data.py --dry-run  # Preview
python3 cyber-train/clean_training_data.py --apply    # Apply
```

**What to Remove:**
- ✅ Punctuation as entities (":", ",", "'s")
- ✅ Single characters (except "I")
- ✅ Clearly wrong labels

**What to Keep:**
- ✅ Ambiguous cases
- ✅ Edge cases
- ✅ Borderline examples

#### 3. Use Post-Processing Filter

**Filter as Safety Net:**
- Model learns from diverse data
- Filter catches remaining false positives
- Model + Filter = Best results

```python
from fix_entity_extraction import post_process_entities

# Apply filter after model prediction
filtered_entities = post_process_entities(entities, apply_filter=True, apply_validation=True)
```

#### 4. Regularization Techniques

**In Training Config:**
- Dropout: 0.3-0.5 (prevents overfitting)
- Early stopping: Stop when dev loss stops improving
- Learning rate decay: Reduce learning rate over time

#### 5. Cross-Validation

**Split Data Properly:**
- Train: 70% (learning)
- Dev: 15% (validation during training)
- Test: 15% (final evaluation)

**Never train on test set!**

---

## 🔄 Continuous Improvement

### Step 1: Monitor Performance

**Track Metrics:**
- False positive rate
- Precision and recall
- Per-entity-type performance
- Edge case handling

**Create Logging:**
```python
import json
from datetime import datetime

def log_prediction(text, entities, intents, correct=None):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "text": text,
        "entities": entities,
        "intents": intents,
        "correct": correct
    }
    
    with open("model_predictions.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

### Step 2: Collect Real-World Data

**Sources:**
- Production queries
- User feedback
- Edge cases
- New entity types
- New intents

**Process:**
1. Log predictions in production
2. Collect user feedback
3. Identify patterns
4. Add to training data

### Step 3: Identify Improvement Areas

**Analyze Logs:**
```bash
# Find common false positives
python3 analyze_predictions.py --find-false-positives

# Find missed entities
python3 analyze_predictions.py --find-missed-entities

# Find edge cases
python3 analyze_predictions.py --find-edge-cases
```

### Step 4: Add Training Examples

**For Each Issue:**
1. Identify pattern
2. Create examples (positive and negative)
3. Add to training data
4. Retrain model
5. Verify improvement

**Example:**
```bash
# Add examples for new entity type
echo '{"text": "New entity example", "entities": [[0, 10, "NEW_TYPE"]]}' >> training_data.jsonl

# Add negative example
echo '{"text": "This should not be an entity", "entities": []}' >> training_data.jsonl
```

### Step 5: Retrain Regularly

**Schedule:**
- **Weekly**: Add new examples from production
- **Monthly**: Full retraining with expanded dataset
- **Quarterly**: Review and update entity/intent taxonomies
- **Annually**: Major model update

**Retraining Process:**
```bash
# 1. Add new examples
# 2. Re-prepare data
python3 cyber-train/prepare_spacy_training.py

# 3. Retrain models
python3 cyber-train/train_spacy_models.py

# 4. Test improvements
python3 cyber-train/comprehensive_test_suite.py --comprehensive

# 5. Compare with previous model
python3 compare_models.py --old old_model --new new_model
```

---

## 🌍 Real-World Testing

### Step 1: Deploy to Staging

**Before Production:**
1. Deploy to staging environment
2. Test with real queries
3. Monitor performance
4. Collect feedback
5. Fix issues

### Step 2: A/B Testing

**Compare Models:**
```python
# Test new model vs old model
def compare_models(text, old_model, new_model):
    old_result = old_model(text)
    new_result = new_model(text)
    
    # Compare predictions
    # Log differences
    # Track which is better
```

### Step 3: Monitor Production

**Key Metrics:**
- Prediction latency
- Error rate
- User feedback
- False positive rate
- False negative rate

**Alerting:**
- Set up alerts for high error rates
- Monitor false positive spikes
- Track performance degradation

### Step 4: Collect Feedback

**Methods:**
- User feedback buttons
- Log incorrect predictions
- Track user corrections
- Analyze common patterns

**Process:**
1. Log all predictions
2. Collect user feedback
3. Identify issues
4. Add to training data
5. Retrain model

### Step 5: Gradual Rollout

**Phased Approach:**
1. **10% traffic**: Test with small subset
2. **50% traffic**: If metrics look good
3. **100% traffic**: Full rollout

**Monitor at each stage!**

---

## 🚀 Production Deployment

### Step 1: Package Model

```bash
# Create model package
python3 -m spacy package cyber-train/models/ner_model/model-best ./packages/ner_model

# Install package
pip install ./packages/ner_model/dist/ner_model-1.0.0.tar.gz
```

### Step 2: Create API

```python
from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)
ner_model = spacy.load("ner_model")
intent_model = spacy.load("intent_model")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.json["text"]
    
    # Extract entities
    doc = ner_model(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Classify intent
    doc = intent_model(text)
    intents = {label: score for label, score in doc.cats.items() if score > 0.5}
    
    return jsonify({
        "entities": entities,
        "intents": intents
    })
```

### Step 3: Add Post-Processing

```python
from fix_entity_extraction import post_process_entities

# Filter false positives
filtered_entities = post_process_entities(entities, apply_filter=True, apply_validation=True)
```

### Step 4: Add Monitoring

```python
import logging
from datetime import datetime

logging.basicConfig(filename='model_predictions.log', level=logging.INFO)

def predict_with_logging(text):
    # Make prediction
    entities, intents = predict(text)
    
    # Log
    logging.info(f"{datetime.now()}: {text} -> {entities}, {intents}")
    
    return entities, intents
```

---

## ❌ What to Avoid

### 1. Don't Over-Clean Training Data

**Problem:**
- Removing all false positives → model overfits
- Model doesn't learn boundaries
- Model fails on edge cases

**Solution:**
- Keep diverse data
- Add negative examples
- Selective cleaning only

### 2. Don't Train Without Negative Examples

**Problem:**
- Model only sees positive examples
- Model over-extracts (false positives)
- Model doesn't learn boundaries

**Solution:**
- Add 20-30% negative examples
- Model learns what NOT to extract

### 3. Don't Test on Training Data

**Problem:**
- Overly optimistic results
- Doesn't reflect real performance
- Model overfitting not detected

**Solution:**
- Always use separate test set
- Never train on test data
- Use dev set for validation during training

### 4. Don't Ignore Edge Cases

**Problem:**
- Model fails on real-world queries
- Poor generalization
- User frustration

**Solution:**
- Include edge cases in training
- Test with comprehensive suite
- Monitor production performance

### 5. Don't Deploy Without Testing

**Problem:**
- Bugs in production
- Poor performance
- User impact

**Solution:**
- Test thoroughly before deployment
- Use staging environment
- Gradual rollout

### 6. Don't Stop Improving

**Problem:**
- Model performance degrades over time
- New patterns not learned
- User needs not met

**Solution:**
- Continuous improvement process
- Regular retraining
- Monitor and adapt

---

## 🐛 Troubleshooting

### Low Performance

**Symptoms:**
- Low F1 score (< 0.80)
- High false positive rate (> 5%)
- Poor recall (< 0.80)

**Solutions:**
1. **Check data quality**
   - Review preparation report
   - Check for format errors
   - Verify label consistency

2. **Add more training data**
   - More examples per entity type
   - More negative examples
   - More edge cases

3. **Improve training config**
   - Use pretrained vectors
   - Adjust hyperparameters
   - Train longer

4. **Clean training data**
   - Remove obvious errors
   - Fix label inconsistencies
   - Add negative examples

### High False Positive Rate

**Symptoms:**
- Common words detected as entities
- Punctuation detected as entities
- Too many entities extracted

**Solutions:**
1. **Add negative examples**
   ```bash
   python3 cyber-train/add_negative_examples.py --add-to-existing
   ```

2. **Improve post-processing filter**
   - Add more common words
   - Add common phrases
   - More aggressive filtering

3. **Clean training data**
   ```bash
   python3 cyber-train/clean_training_data.py --apply
   ```

### Overfitting

**Symptoms:**
- High training accuracy, low test accuracy
- Poor performance on new data
- Fails on edge cases

**Solutions:**
1. **Add negative examples** (20-30%)
2. **Keep diverse training data**
3. **Use regularization** (dropout, early stopping)
4. **Add more training data**

### Model Not Learning

**Symptoms:**
- No improvement during training
- Loss not decreasing
- Same predictions always

**Solutions:**
1. **Check data format**
   - Verify JSONL format
   - Check entity boundaries
   - Verify labels exist

2. **Check training config**
   - Learning rate not too low
   - Batch size appropriate
   - Enough training steps

3. **Check data quality**
   - Enough examples per label
   - Balanced classes
   - No format errors

---

## 📚 Additional Resources

### Documentation
- [spaCy Training Guide](https://spacy.io/usage/training)
- [spaCy Models](https://spacy.io/models)
- [spaCy Projects](https://spacy.io/usage/projects)

### Tools
- **Prodigy**: Advanced annotation tool
- **Weights & Biases**: Experiment tracking
- **MLflow**: Model management

### Best Practices
- Start with small dataset, iterate
- Focus on data quality over quantity
- Test thoroughly before deployment
- Monitor and improve continuously

---

## ✅ Summary Checklist

### Data Preparation
- [ ] Create training data (JSONL format)
- [ ] Add 20-30% negative examples
- [ ] Include edge cases
- [ ] Validate data format
- [ ] Prepare spaCy format

### Training
- [ ] Create training config
- [ ] Train models
- [ ] Review training output
- [ ] Check evaluation metrics

### Testing
- [ ] Run comprehensive test suite
- [ ] Evaluate on test set
- [ ] Review results
- [ ] Test edge cases

### Deployment
- [ ] Package model
- [ ] Create API
- [ ] Add post-processing
- [ ] Add monitoring
- [ ] Deploy to staging
- [ ] Test in production
- [ ] Gradual rollout

### Continuous Improvement
- [ ] Monitor performance
- [ ] Collect feedback
- [ ] Identify issues
- [ ] Add training examples
- [ ] Retrain regularly

---

**This guide covers the complete lifecycle from training to production. Follow it step-by-step for best results!** 🎉

