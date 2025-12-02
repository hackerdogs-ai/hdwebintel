# 🎯 Next Steps Action Plan

## 📊 Current Status

**NER Model Accuracy:**
- Precision: ~7-8% (VERY LOW)
- Recall: ~9% (VERY LOW)
- F1 Score: ~8% (CRITICAL - needs immediate attention)

**Intent Model Accuracy:**
- Precision: ~70-80% (ACCEPTABLE)
- Recall: ~60-70% (ACCEPTABLE)
- F1 Score: ~65-75% (DECENT - can improve)

---

## 🚨 Immediate Actions (Do First)

### 1. Apply Post-Processing Filter (QUICK WIN)

**Status:** ✅ Script created (`fix_entity_extraction.py`)

**Action:**
```bash
# The test script has been updated to use the filter
# Re-run tests to see improved results
python3 cyber-train/test_models.py --test-suite
```

**Expected Improvement:**
- Remove ~60-70% of false positives
- Improve precision from 8% to ~30-40%
- Still need to fix training data for full solution

### 2. Review Training Data Quality

**Action:**
```bash
# Sample random training examples to review
python3 << 'EOF'
import json
import random
from pathlib import Path

# Sample 50 random examples
files = list(Path("cyber-train/entities-intent").rglob("*_entities.jsonl"))
for file in files[:5]:  # Check first 5 files
    with open(file) as f:
        lines = f.readlines()
    samples = random.sample(lines, min(10, len(lines)))
    print(f"\n{file.name}:")
    for line in samples:
        data = json.loads(line)
        print(f"  Text: {data['text'][:60]}...")
        print(f"  Entities: {data['entities']}")
        print()
EOF
```

**What to Look For:**
- ❌ Common words labeled as entities
- ❌ Incorrect entity boundaries
- ❌ Wrong entity type labels
- ❌ Over-labeling (too many entities per sentence)

---

## 📋 Priority 1: Fix Training Data (BIGGEST IMPACT)

### Week 1: Data Quality Audit

**Tasks:**
1. **Review 500 random training examples**
   - Identify false positive patterns
   - Document common mistakes
   - Create cleaning checklist

2. **Remove problematic examples**
   - Delete examples with common words as entities
   - Remove examples with punctuation as entities
   - Fix incorrect entity boundaries

3. **Add critical entity examples**
   - IP addresses: 200 examples
   - CVE IDs: 100 examples
   - Domains: 200 examples
   - Coordinates: 100 examples
   - Threat actors: 100 examples

4. **Add negative examples**
   - 100-200 sentences with NO entities
   - Helps model learn what NOT to extract

**Target:** Clean 2,000-3,000 high-quality examples

### Week 2: Data Enhancement

**Tasks:**
1. **Balance entity types**
   - Ensure critical types have 50-100 examples
   - Remove or consolidate rare types (F1 = 0.0)
   - Focus on 100-200 most important types

2. **Add pattern-based examples**
   - IP address patterns (IPv4, IPv6)
   - CVE patterns (CVE-YYYY-NNNNN)
   - Domain patterns (various TLDs)
   - Coordinate patterns (lat/long formats)

3. **Validate entity boundaries**
   - Ensure entities align with token boundaries
   - Fix multi-word entity spans
   - Remove overlapping entities

---

## 📋 Priority 2: Model Improvements

### Configuration Updates

**File:** `cyber-train/models/configs/config_ner.cfg`

**Changes:**
```ini
[training]
dropout = 0.2  # Increase from 0.1
patience = 3200  # Increase from 1600
max_steps = 40000  # Increase from 20000

[components.ner]
# Consider adding negative examples handling
```

### Use Pretrained Vectors

**Action:**
```bash
# Download English model
python -m spacy download en_core_web_sm

# Update config to use pretrained vectors
# This will significantly improve performance
```

---

## 📋 Priority 3: Post-Processing & Validation

### Implement Validation Rules

**Status:** ✅ Basic filter created

**Enhancements Needed:**
1. Add more pattern validations
2. Add confidence threshold filtering
3. Add context-based validation
4. Add entity type co-occurrence rules

### Add Confidence Thresholds

```python
# Filter low-confidence entities
MIN_CONFIDENCE = 0.5  # Adjust based on precision/recall tradeoff

# Only show entities above threshold
filtered = [e for e in entities if e.confidence >= MIN_CONFIDENCE]
```

---

## 📊 Success Metrics

### Target Performance (After Fixes)

**NER Model:**
- Precision: > 0.80 (currently ~0.08)
- Recall: > 0.75 (currently ~0.09)
- F1 Score: > 0.77 (currently ~0.08)
- **Improvement needed: 10x**

**Intent Model:**
- Precision: > 0.85 (currently ~0.75)
- Recall: > 0.80 (currently ~0.65)
- F1 Score: > 0.82 (currently ~0.70)
- **Improvement needed: 15-20%**

---

## 🗓️ Timeline

### Week 1-2: Data Quality
- [ ] Review and clean training data
- [ ] Remove false positives
- [ ] Add critical entity examples
- [ ] Add negative examples

### Week 3: Retraining
- [ ] Update config files
- [ ] Retrain with cleaned data
- [ ] Evaluate on test set
- [ ] Compare with baseline

### Week 4: Optimization
- [ ] Fine-tune hyperparameters
- [ ] Add post-processing enhancements
- [ ] Create validation test suite
- [ ] Document improvements

---

## 🔧 Quick Wins (Can Do Today)

1. **✅ Apply post-processing filter** (DONE)
   - Re-run tests to see immediate improvement

2. **Sample training data**
   - Review 50 random examples
   - Identify top 10 problem patterns

3. **Create cleaning script**
   - Automate removal of obvious false positives
   - Fix common boundary issues

4. **Add pattern validation**
   - IP address regex
   - CVE ID regex
   - Domain regex

---

## 📝 Notes

- **Biggest Impact:** Fixing training data quality will have the most significant effect
- **Quick Win:** Post-processing filter provides immediate improvement
- **Long-term:** Need to retrain with cleaned data for full solution
- **Monitoring:** Set up evaluation pipeline to track improvements

---

## ✅ Checklist

- [x] Created post-processing filter
- [x] Updated test script to use filter
- [x] Created accuracy analysis report
- [ ] Review training data quality
- [ ] Remove false positive examples
- [ ] Add critical entity examples
- [ ] Add negative examples
- [ ] Retrain with cleaned data
- [ ] Evaluate improvements
- [ ] Document changes

---

**Next Immediate Step:** Re-run tests with post-processing filter to see improvement, then start data quality review.


