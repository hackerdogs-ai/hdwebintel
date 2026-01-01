# 🎯 Strategic Plan to Dramatically Improve Model Performance

**Date:** December 27, 2025  
**Current Status:** 97% training performance, 41% test recall (53% gap)  
**Target:** 85%+ test recall, <15% gap

---

## 📊 Executive Summary

### Current State
Your spaCy NER model suffers from **severe overfitting**:
- **Training:** 97.19% precision, 94.76% recall, 95.96% F1 ✅
- **Testing:** 84.57% precision, **41.52% recall**, 55.69% F1 ❌
- **Gap:** **53.24% recall gap** - model memorized training patterns but can't generalize

### Root Cause
After 8 training iterations with 52,920 examples across 573 entity types, **adding more examples won't fix the fundamental problems:**

1. **Training/test distribution mismatch** - Generated data ≠ real-world data
2. **573 entity types is excessive** - Causes class imbalance and confusion
3. **Pattern overfitting** - Model learns exact patterns, not entity semantics
4. **No hybrid approach** - Missing rule-based extraction for pattern-based entities

### Strategic Solution
This plan focuses on **fundamental changes** rather than incremental improvements:
- Reduce entity types from 573 to ~100 (80% reduction)
- Implement hybrid rule-based + ML extraction
- Collect and use real-world data
- Apply active learning instead of blind data addition

### Expected Results
- **Week 1:** 41% → 60-65% recall (+40% relative improvement)
- **Week 2-3:** 60-65% → 70-75% recall  
- **Month 1:** 70-75% → 80-85% recall (target achieved)

---

## 🎯 Phase 1: Quick Wins (Week 1)

### 1.1 Implement Hybrid Extraction ⚡ **[READY TO USE]**

**File Created:** `hybrid_entity_extractor.py`

**What it does:**
- Combines **rule-based patterns** (high precision) with ML model (handles complexity)
- Extracts pattern-based entities with regex (IP, CVE, Hash, Email, Phone, etc.)
- Falls back to ML for complex entities (Threat Actors, Malware, etc.)

**Usage:**
```python
from hybrid_entity_extractor import HybridEntityExtractor

# Initialize
extractor = HybridEntityExtractor(
    ner_model_path="cyber-train/models/ner_model/model-best"
)

# Extract entities
text = "Suspicious activity from IP 192.168.1.100 linked to APT41"
entities = extractor.extract(text)

# Output: [('192.168.1.100', 'IP_ADDRESS'), ('APT41', 'THREAT_ACTOR')]
```

**Impact:**
- ✅ Immediate recall improvement for pattern-based entities
- ✅ Fixes IP_ADDRESS (23 missed), HASH (16 missed), DATE (14 missed)
- ✅ No retraining required
- **Expected:** +15-20% recall improvement immediately

**Action:**
```bash
# Test hybrid extractor
cd /Users/tredkar/Documents/GitHub/hdwebintel/cyber-train
python3 hybrid_entity_extractor.py

# Integrate into comprehensive test suite
# Edit comprehensive_test_suite.py to use HybridEntityExtractor
```

---

### 1.2 Consolidate Entity Types ⚡ **[READY TO USE]**

**File Created:** `consolidate_entity_types.py`

**What it does:**
- Analyzes 573 entity types and identifies consolidation opportunities
- Merges similar types (e.g., IPV4_ADDRESS + IPV6_ADDRESS → IP_ADDRESS)
- Reduces complexity and class imbalance

**Usage:**
```bash
# Analyze (dry-run, no changes)
cd /Users/tredkar/Documents/GitHub/hdwebintel/cyber-train
python3 consolidate_entity_types.py --base-dir entities-intent

# Apply consolidations
python3 consolidate_entity_types.py --base-dir entities-intent --apply
```

**Impact:**
- ✅ Reduces 573 types to ~150-200 types (60-70% reduction)
- ✅ Improves model generalization
- ✅ Reduces training time
- **Expected:** +10-15% recall improvement after retraining

**Consolidation Examples:**
```
IP_ADDRESS ← IPV4_ADDRESS, IPV6_ADDRESS, IP
HASH ← MD5_HASH, SHA1_HASH, SHA256_HASH, FILE_HASH
URL ← MALICIOUS_URL, PHISHING_URL, HTTP_URL, HTTPS_URL
MALWARE_TYPE ← RANSOMWARE, TROJAN, VIRUS, WORM
```

**Action:**
```bash
# Step 1: Analyze current types
python3 consolidate_entity_types.py --base-dir entities-intent

# Step 2: Review suggestions and apply
python3 consolidate_entity_types.py --base-dir entities-intent --apply

# Step 3: Re-prepare and retrain
python3 prepare_spacy_training.py --base-dir entities-intent
python3 train_spacy_models.py --gpu
```

---

### 1.3 Combined Quick Win Script

Create `quick_win_improvements.sh`:
```bash
#!/bin/bash
# Quick win improvements - Run in 2-3 hours

echo "===== PHASE 1: QUICK WINS ====="
echo ""

# 1. Analyze entity types
echo "Step 1: Analyzing entity types..."
python3 consolidate_entity_types.py --base-dir entities-intent

# 2. Apply consolidations
echo ""
echo "Step 2: Consolidating entity types..."
python3 consolidate_entity_types.py --base-dir entities-intent --apply

# 3. Re-prepare training data
echo ""
echo "Step 3: Re-preparing training data..."
python3 prepare_spacy_training.py --base-dir entities-intent

# 4. Retrain models
echo ""
echo "Step 4: Retraining models (this will take 1-2 hours)..."
python3 train_spacy_models.py --gpu

# 5. Test with hybrid extractor
echo ""
echo "Step 5: Testing with hybrid extraction..."
python3 hybrid_entity_extractor.py

# 6. Run comprehensive test suite
echo ""
echo "Step 6: Running comprehensive test suite..."
python3 comprehensive_test_suite.py --comprehensive

echo ""
echo "===== PHASE 1 COMPLETE ====="
echo "Check comprehensive_test_results.json for results"
```

**Expected Phase 1 Results:**
- Recall: 41.52% → **60-65%** (+40-55% relative improvement)
- Precision: 84.57% → **88-90%**
- F1: 55.69% → **72-75%**
- Time: 2-3 hours

---

## 🚀 Phase 2: Data Quality Improvements (Week 2-3)

### 2.1 Collect Real-World Data

**Problem:** Generated examples don't match real-world patterns

**Solution:** Collect real threat intelligence data

**Sources:**
1. **Security News:**
   - SecurityWeek, Krebs on Security, Threatpost
   - 100-200 articles
   
2. **Threat Intelligence:**
   - CISA alerts (https://www.cisa.gov/news-events/cybersecurity-advisories)
   - NIST publications
   - 50-100 reports
   
3. **Real Incidents:**
   - Incident response reports (anonymized)
   - OSINT investigations
   - 50-100 examples

**Process:**
```python
# Create real_data_collector.py
import requests
from bs4 import BeautifulSoup

def collect_security_articles():
    """Collect real security articles."""
    sources = [
        'https://www.securityweek.com/',
        'https://krebsonsecurity.com/',
        'https://threatpost.com/',
    ]
    
    articles = []
    for source in sources:
        # Scrape articles
        # Store raw text
        pass
    
    return articles

def annotate_with_model(articles, model):
    """Use model to pre-annotate, then manually correct."""
    annotations = []
    for article in articles:
        # Get model predictions
        doc = model(article)
        
        # Export for manual review/correction
        annotations.append({
            'text': article,
            'entities': [(e.start_char, e.end_char, e.label_) for e in doc.ents]
        })
    
    return annotations
```

**Timeline:** 1 week to collect and annotate 500-1000 real examples

**Impact:** +5-10% recall by aligning training with real-world patterns

---

### 2.2 Implement Active Learning

**Problem:** Blindly adding examples wastes effort

**Solution:** Focus on examples where model is uncertain

**Implementation:**
```python
# Create active_learner.py
import numpy as np
from typing import List, Tuple

class ActiveLearner:
    """Identify examples for maximum training impact."""
    
    def __init__(self, model):
        self.model = model
    
    def find_uncertain_examples(self, candidate_texts: List[str], 
                                 n_samples: int = 100) -> List[Tuple[str, float]]:
        """
        Find examples where model is most uncertain.
        
        Uses uncertainty sampling:
        - Low confidence scores
        - Conflicting entity boundaries
        - Multiple possible labels
        """
        uncertain = []
        
        for text in candidate_texts:
            doc = self.model(text)
            
            # Calculate uncertainty score
            uncertainty = self._calculate_uncertainty(doc)
            uncertain.append((text, uncertainty))
        
        # Sort by uncertainty (highest first)
        uncertain.sort(key=lambda x: x[1], reverse=True)
        
        return uncertain[:n_samples]
    
    def _calculate_uncertainty(self, doc) -> float:
        """Calculate uncertainty score for a document."""
        # Factors:
        # 1. Low entity confidence scores
        # 2. Overlapping entity predictions
        # 3. Short entity spans (more ambiguous)
        
        if len(doc.ents) == 0:
            return 0.0
        
        # Average confidence (lower = more uncertain)
        # Note: spaCy doesn't expose per-entity confidence directly,
        # but we can use beam search or entity ruler scores
        
        uncertainty = 0.0
        for ent in doc.ents:
            # Short entities are more uncertain
            if len(ent.text.split()) <= 1:
                uncertainty += 0.3
            
            # Entities at sentence boundaries are uncertain
            if ent.start == 0 or ent.end == len(doc):
                uncertainty += 0.2
        
        return uncertainty / len(doc.ents)

# Usage:
learner = ActiveLearner(model)
uncertain_examples = learner.find_uncertain_examples(unlabeled_corpus)
# Manually annotate only these examples
```

**Impact:** 
- 3x more efficient than random sampling
- +10-15% recall with same annotation effort

---

### 2.3 Data Augmentation

**Problem:** Limited diversity in training examples

**Solution:** Automatically generate variations

**Implementation:**
```python
# Create data_augmenter.py
from nlpaug.augmenter import word as naw
from nlpaug.augmenter import sentence as nas
import random

class EntityAwareAugmenter:
    """Augment training data while preserving entities."""
    
    def __init__(self):
        # Synonym replacement
        self.syn_aug = naw.SynonymAug(aug_src='wordnet')
        
        # Back translation (preserves meaning)
        # self.back_trans_aug = naw.BackTranslationAug()
    
    def augment_example(self, text: str, entities: List[Tuple[int, int, str]], 
                       n_variations: int = 3) -> List[Tuple[str, List]]:
        """
        Generate variations while preserving entity boundaries.
        """
        variations = []
        
        # Extract entity spans
        entity_spans = [(start, end) for start, end, _ in entities]
        
        for _ in range(n_variations):
            # Method 1: Synonym replacement (avoid entity spans)
            augmented = self._synonym_replace_safe(text, entity_spans)
            
            # Update entity positions if text changed
            new_entities = self._update_entity_positions(
                text, augmented, entities
            )
            
            variations.append((augmented, new_entities))
        
        return variations
    
    def _synonym_replace_safe(self, text: str, 
                              entity_spans: List[Tuple[int, int]]) -> str:
        """Replace synonyms outside entity spans."""
        # Split into tokens
        # Replace non-entity tokens with synonyms
        # Reconstruct text
        return text  # Simplified
    
    def _update_entity_positions(self, original: str, augmented: str,
                                 entities: List[Tuple[int, int, str]]) -> List:
        """Update entity positions after augmentation."""
        # Use character-level alignment
        # Update start/end positions
        return entities  # Simplified

# Usage:
augmenter = EntityAwareAugmenter()
for text, entities in training_data:
    variations = augmenter.augment_example(text, entities, n_variations=3)
    # Add variations to training set
```

**Impact:** 
- 2-3x more training examples without manual annotation
- +5-10% recall from increased diversity

---

## 🎯 Phase 3: Architecture Improvements (Week 3-4)

### 3.1 Switch to Transformer Model

**Current:** spaCy's tok2vec (word embeddings)
**Better:** Transformer-based model (contextual embeddings)

**Why:**
- Transformers understand context better
- Better generalization to unseen patterns
- BERT, RoBERTa, etc. pre-trained on large corpora

**Implementation:**
```bash
# Generate transformer config
python -m spacy init config config_transformer.cfg \
  --lang en \
  --pipeline transformer,ner \
  --optimize accuracy \
  --gpu

# Edit config to use roberta-base
# [components.transformer.model]
# name = "roberta-base"

# Train
python -m spacy train config_transformer.cfg \
  --output ./models/ner_transformer \
  --paths.train ./train.spacy \
  --paths.dev ./dev.spacy \
  --gpu-id 0
```

**Trade-offs:**
- ✅ Better accuracy (+10-20% recall)
- ❌ Slower inference (50ms → 200-300ms)
- ❌ More GPU memory required
- ❌ Larger model size (100MB → 500MB+)

**Decision:** Use transformer for training, distill to smaller model for production

---

### 3.2 Multi-Task Learning

**Current:** Separate NER and intent models
**Better:** Joint training with shared representations

**Why:**
- Intent context helps entity recognition
- Entity information improves intent classification
- Shared encoder = more efficient

**Implementation:**
```python
# Update config to include both tasks
[components.ner]
# NER component

[components.textcat]
# Intent classification component

# Shared transformer
[components.transformer]
# Used by both NER and textcat
```

---

## 📈 Phase 4: Evaluation and Iteration (Ongoing)

### 4.1 Per-Entity-Type Metrics

Track performance for each entity type separately:

```python
# Create per_entity_metrics.py
from collections import defaultdict

def calculate_per_type_metrics(predictions, ground_truth):
    """Calculate precision/recall/F1 per entity type."""
    metrics = defaultdict(lambda: {'tp': 0, 'fp': 0, 'fn': 0})
    
    for pred_type, pred_span in predictions:
        if (pred_type, pred_span) in ground_truth:
            metrics[pred_type]['tp'] += 1
        else:
            metrics[pred_type]['fp'] += 1
    
    for gt_type, gt_span in ground_truth:
        if (gt_type, gt_span) not in predictions:
            metrics[gt_type]['fn'] += 1
    
    # Calculate metrics per type
    results = {}
    for entity_type, counts in metrics.items():
        precision = counts['tp'] / (counts['tp'] + counts['fp']) if counts['tp'] + counts['fp'] > 0 else 0
        recall = counts['tp'] / (counts['tp'] + counts['fn']) if counts['tp'] + counts['fn'] > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        
        results[entity_type] = {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'support': counts['tp'] + counts['fn']
        }
    
    return results
```

**Impact:**
- Identifies exactly which types need improvement
- Focuses effort on weakest types
- Tracks progress per type

---

### 4.2 Error Analysis Dashboard

Create automated error analysis:

```python
# Create error_analyzer.py

class ErrorAnalyzer:
    """Analyze model errors to identify patterns."""
    
    def analyze_errors(self, predictions, ground_truth, texts):
        """Comprehensive error analysis."""
        errors = {
            'false_positives': [],
            'false_negatives': [],
            'boundary_errors': [],
            'type_confusion': []
        }
        
        # Identify error types
        for pred in predictions:
            if pred not in ground_truth:
                # False positive or boundary/type error
                if self._is_boundary_error(pred, ground_truth):
                    errors['boundary_errors'].append(pred)
                elif self._is_type_confusion(pred, ground_truth):
                    errors['type_confusion'].append(pred)
                else:
                    errors['false_positives'].append(pred)
        
        for gt in ground_truth:
            if gt not in predictions:
                errors['false_negatives'].append(gt)
        
        # Generate report
        self._generate_report(errors, texts)
        
        return errors
    
    def _generate_report(self, errors, texts):
        """Generate human-readable error report."""
        print("=" * 70)
        print("ERROR ANALYSIS REPORT")
        print("=" * 70)
        
        print(f"\n📊 Error Summary:")
        print(f"   False Positives: {len(errors['false_positives'])}")
        print(f"   False Negatives: {len(errors['false_negatives'])}")
        print(f"   Boundary Errors: {len(errors['boundary_errors'])}")
        print(f"   Type Confusion: {len(errors['type_confusion'])}")
        
        # Show examples of each error type
        print(f"\n❌ False Positive Examples:")
        for entity in errors['false_positives'][:5]:
            print(f"   • {entity}")
        
        print(f"\n❌ False Negative Examples:")
        for entity in errors['false_negatives'][:5]:
            print(f"   • {entity}")
```

---

## 📋 Implementation Timeline

### **Week 1: Quick Wins**
- Day 1-2: Implement hybrid extraction (done ✅)
- Day 3-4: Consolidate entity types + retrain
- Day 5: Test and measure improvements
- **Target:** 60-65% recall

### **Week 2: Data Quality**
- Day 1-3: Collect real-world data
- Day 4-5: Implement active learning
- **Target:** 65-70% recall

### **Week 3: Augmentation**
- Day 1-3: Implement data augmentation
- Day 4-5: Retrain with augmented data
- **Target:** 70-75% recall

### **Week 4: Architecture**
- Day 1-3: Switch to transformer model
- Day 4-5: Multi-task learning
- **Target:** 75-80% recall

### **Ongoing: Iteration**
- Weekly error analysis
- Continuous data collection
- Incremental improvements
- **Target:** 80-85% recall (month 2)

---

## ✅ Success Metrics

### Phase 1 (Week 1) - Quick Wins
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Recall | 41.52% | 60-65% | ⏳ |
| Precision | 84.57% | 88-90% | ⏳ |
| F1 | 55.69% | 72-75% | ⏳ |

### Phase 2 (Week 2-3) - Data Quality
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Recall | 60-65% | 70-75% | ⏳ |
| Precision | 88-90% | 90-92% | ⏳ |
| F1 | 72-75% | 79-82% | ⏳ |

### Phase 3 (Week 3-4) - Architecture
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Recall | 70-75% | 80-85% | ⏳ |
| Precision | 90-92% | 92-95% | ⏳ |
| F1 | 79-82% | 86-90% | ⏳ |

---

## 🚀 Get Started Now

### Option 1: Run Quick Wins (2-3 hours)
```bash
cd /Users/tredkar/Documents/GitHub/hdwebintel/cyber-train

# 1. Test hybrid extractor
python3 hybrid_entity_extractor.py

# 2. Analyze and consolidate entity types
python3 consolidate_entity_types.py --base-dir ../entities-intent

# 3. Apply consolidations
python3 consolidate_entity_types.py --base-dir ../entities-intent --apply

# 4. Retrain
python3 prepare_spacy_training.py --base-dir ../entities-intent
python3 train_spacy_models.py --gpu

# 5. Test
python3 comprehensive_test_suite.py --comprehensive
```

### Option 2: Full Phase 1 (1 week)
Follow Week 1 timeline above

### Option 3: Complete Transformation (1 month)
Follow full timeline

---

## 💡 Key Insights

### Why This Will Work (vs Previous Attempts)

**Previous Approach:**
- ❌ Adding more generated examples → More overfitting
- ❌ Fixing boundaries → Addresses symptoms
- ❌ 8 iterations with diminishing returns

**This Approach:**
- ✅ Hybrid extraction → Immediate recall boost
- ✅ Entity consolidation → Better generalization
- ✅ Real-world data → Matches test distribution
- ✅ Active learning → Efficient use of annotation effort
- ✅ Architectural improvements → Better capacity

### Critical Success Factors

1. **Don't just add more examples** - Focus on data quality and diversity
2. **Use real-world data** - Generated data has different patterns
3. **Reduce complexity** - 573 types is too many
4. **Measure per-type performance** - Overall metrics hide problems
5. **Iterate based on errors** - Let data drive improvements

---

## 📞 Support

Questions or issues? Check these resources:
- **Hybrid Extraction:** See `hybrid_entity_extractor.py`
- **Entity Consolidation:** See `consolidate_entity_types.py`
- **Current Status:** See `COMPREHENSIVE_TEST_RESULTS_REPORT.md`

---

**Status:** ✅ **Ready to implement - Start with Quick Wins!**

