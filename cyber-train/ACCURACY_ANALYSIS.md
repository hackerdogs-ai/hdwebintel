# 📊 Model Accuracy Analysis & Next Steps

## 🔍 Test Results Review

### NER Model Issues

**Critical Problems Identified:**

1. **High False Positive Rate**
   - Common words incorrectly labeled as entities
   - Examples: "I" → NETWORK_TYPE, ":" → LONGITUDE, "," → LOCATION
   - Punctuation marks extracted as entities

2. **Incorrect Entity Types**
   - "APT41" → API_TYPE (should be THREAT_ACTOR)
   - "latitude" → ALTITUDE (should be LATITUDE)
   - Many semantic mismatches

3. **Wrong Entity Boundaries**
   - "investigate this" extracted as single entity (METRIC_TYPE)
   - "Analyze the" extracted as entity (TOOL)
   - Multi-word phrases incorrectly segmented

4. **Missing Critical Entities**
   - IP addresses not detected (10.0.0.1, 192.168.1.1)
   - CVE IDs not detected (CVE-2021-44228)
   - Coordinates partially detected but incorrectly

5. **Intent Model Performance**
   - ✅ Better performance than NER
   - Top intents are reasonable (INVESTIGATE, MAINTAIN_SYSTEMS)
   - Confidence scores reasonable (50-80%)
   - Some generic intents (MAINTAIN_SYSTEMS appears too frequently)

### Estimated Accuracy

**NER Model:**
- Precision: ~20-30% (many false positives)
- Recall: ~30-40% (many missed entities)
- F1 Score: ~25-35% (needs significant improvement)

**Intent Model:**
- Precision: ~70-80% (reasonable)
- Recall: ~60-70% (acceptable)
- F1 Score: ~65-75% (decent but can improve)

---

## 🎯 Root Causes

### 1. Training Data Quality Issues
- **Over-labeling**: Too many entities per sentence
- **Inconsistent boundaries**: Entity spans not properly aligned
- **Label noise**: Wrong entity types in training data
- **Class imbalance**: Some entity types have very few examples

### 2. Model Configuration Issues
- **Threshold too low**: Model too permissive in entity detection
- **No negative examples**: Model hasn't learned what NOT to extract
- **Tokenization issues**: Entity boundaries don't align with tokens

### 3. Data Distribution Issues
- **Test set mismatch**: Test queries may not match training distribution
- **Domain shift**: Real queries differ from training examples
- **Rare entities**: Important entities (IPs, CVEs) may be underrepresented

---

## 🚀 Next Steps & Recommendations

### Priority 1: Fix Training Data (CRITICAL)

#### 1.1 Review and Clean Training Data
```bash
# Check for problematic examples
python3 cyber-train/analyze_training_data.py --check-entities
```

**Actions:**
- Remove false positive examples (common words labeled as entities)
- Fix incorrect entity boundaries
- Correct wrong entity type labels
- Add negative examples (sentences with NO entities)

#### 1.2 Add More High-Quality Examples
**Focus Areas:**
- IP addresses (IPv4 and IPv6)
- CVE IDs (CVE-YYYY-NNNNN format)
- Coordinates (latitude/longitude patterns)
- Domain names
- Threat actors (APT groups, malware names)

**Target:** Add 200-500 examples per critical entity type

#### 1.3 Balance Entity Types
- Ensure important entity types have sufficient examples (min 50-100)
- Remove or consolidate rare entity types with F1 = 0.0
- Focus on 100-200 most important entity types

### Priority 2: Improve Model Training

#### 2.1 Adjust Training Configuration
```python
# In config_ner.cfg, adjust:
[training]
dropout = 0.2  # Increase from 0.1
patience = 3200  # Increase from 1600
max_steps = 40000  # Increase from 20000

[components.ner]
# Add negative examples handling
```

#### 2.2 Use Pretrained Vectors
```bash
# Download English model
python -m spacy download en_core_web_sm

# Update config to use pretrained vectors
```

#### 2.3 Add Negative Sampling
- Include sentences with NO entities in training
- Helps model learn what NOT to extract
- Target: 10-20% of training data should be negative examples

### Priority 3: Post-Processing & Validation

#### 3.1 Add Entity Validation Rules
```python
# Post-process entities to filter false positives
def validate_entity(text, label):
    # Reject single-character entities
    if len(text.strip()) <= 1:
        return False
    
    # Reject punctuation-only entities
    if text.strip() in [':', ',', '.', ';', '-']:
        return False
    
    # Reject common words for certain labels
    common_words = {'I', 'the', 'a', 'an', 'this', 'that'}
    if text.lower() in common_words:
        return False
    
    return True
```

#### 3.2 Add Pattern-Based Validation
```python
# Validate entity types match patterns
PATTERNS = {
    'IP_ADDRESS': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
    'CVE_ID': r'^CVE-\d{4}-\d{4,7}$',
    'LATITUDE': r'^-?\d+\.?\d*$',  # -90 to 90
    'LONGITUDE': r'^-?\d+\.?\d*$',  # -180 to 180
    'DOMAIN': r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
}
```

### Priority 4: Evaluation & Monitoring

#### 4.1 Create Validation Test Set
- Curate 100-200 high-quality test examples
- Include edge cases and common false positives
- Run evaluation after each training iteration

#### 4.2 Add Confidence Thresholds
```python
# Filter low-confidence entities
MIN_CONFIDENCE = 0.5  # Adjust based on precision/recall tradeoff

filtered_entities = [
    ent for ent in doc.ents 
    if ent._.confidence >= MIN_CONFIDENCE
]
```

---

## 📋 Action Plan

### Week 1: Data Quality Fixes
- [ ] Review 500 random training examples
- [ ] Remove false positive examples
- [ ] Fix incorrect entity boundaries
- [ ] Add 200 examples for critical entity types (IP, CVE, Domain)
- [ ] Add 100 negative examples (no entities)

### Week 2: Model Retraining
- [ ] Update config with better hyperparameters
- [ ] Use pretrained vectors (en_core_web_sm)
- [ ] Retrain with cleaned data
- [ ] Evaluate on validation set

### Week 3: Post-Processing & Validation
- [ ] Implement entity validation rules
- [ ] Add pattern-based validation
- [ ] Test on real queries
- [ ] Fine-tune thresholds

### Week 4: Production Readiness
- [ ] Create comprehensive test suite
- [ ] Document entity types and patterns
- [ ] Set up monitoring
- [ ] Deploy and iterate

---

## 🔧 Quick Fixes (Can Do Now)

### 1. Add Post-Processing Filter
```python
# In test_models.py, add filtering
def filter_entities(doc):
    """Remove obviously incorrect entities."""
    valid_entities = []
    for ent in doc.ents:
        # Skip single characters
        if len(ent.text.strip()) <= 1:
            continue
        # Skip punctuation
        if ent.text.strip() in [':', ',', '.', ';', '-', '(', ')']:
            continue
        # Skip common words
        if ent.text.lower() in ['i', 'the', 'a', 'an', 'this', 'that', 'for', 'and']:
            continue
        valid_entities.append(ent)
    return valid_entities
```

### 2. Add Pattern Validation
```python
import re

def validate_entity_type(text, label):
    """Validate entity matches expected pattern."""
    patterns = {
        'IP_ADDRESS': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
        'CVE_ID': r'^CVE-\d{4}-\d{4,7}$',
    }
    
    if label in patterns:
        return bool(re.match(patterns[label], text))
    return True  # No pattern, accept
```

### 3. Increase Confidence Threshold
```python
# Only show entities with high confidence
MIN_CONFIDENCE = 0.6  # Adjust as needed
```

---

## 📊 Success Metrics

**Target Performance:**
- NER Precision: > 0.80
- NER Recall: > 0.75
- NER F1: > 0.77
- Intent Precision: > 0.85
- Intent Recall: > 0.80
- Intent F1: > 0.82

**Current Performance:**
- NER F1: ~0.25-0.35 (needs 2x improvement)
- Intent F1: ~0.65-0.75 (needs 10-20% improvement)

---

## 🎯 Immediate Next Steps

1. **Run data quality check:**
   ```bash
   python3 cyber-train/analyze_training_data.py --check-quality
   ```

2. **Add post-processing filter to test script**

3. **Create focused training set** for critical entity types

4. **Retrain with cleaned data**

5. **Re-evaluate on test set**

---

**Priority:** Fix training data quality first - this will have the biggest impact on accuracy.


