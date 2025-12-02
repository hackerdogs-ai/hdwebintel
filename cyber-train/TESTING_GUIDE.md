# 🧪 Model Testing Guide

After training your spaCy models, use this guide to test and verify they work correctly.

## ✅ Quick Test

### Option 1: Automated Test Suite (Recommended)

```bash
# Run comprehensive test suite
python3 cyber-train/test_models.py --test-suite
```

This will test both models with 16 real-world examples covering:
- Cybersecurity queries (malware, incidents, forensics)
- OSINT queries (verification, detection, profiling)

### Option 2: Quick Shell Script

```bash
# Simple automated test
./cyber-train/quick_test.sh
```

### Option 3: Interactive Testing

```bash
# Start interactive mode
python3 cyber-train/test_models.py --interactive
```

Then type your queries and see results in real-time.

### Option 4: Single Query Test

```bash
# Test a specific query
python3 cyber-train/test_models.py --text "APT41 used WannaCry malware to attack IP 192.168.1.1"
```

## 📊 Expected Output

### NER Model Output

```
📝 Text: APT41 used WannaCry malware to attack IP 192.168.1.1
🏷️  Entities Found:
   • APT41 → THREAT_ACTOR
   • WannaCry → MALWARE_TYPE
   • 192.168.1.1 → IP_ADDRESS
```

### Intent Model Output

```
📝 Text: I need to investigate this suspicious IP address
🎯 Top Intents:
   • INVESTIGATE: 0.9850 (98.5%)
   • DETECT: 0.8230 (82.3%)
   • ANALYZE: 0.7120 (71.2%)
   • MONITOR: 0.4560 (45.6%)
   • VALIDATE: 0.2340 (23.4%)
```

## 🔍 Evaluation on Test Set

Evaluate model performance on the held-out test set:

```bash
# Evaluate NER model
python3 cyber-train/test_models.py \
  --evaluate-ner cyber-train/spacy-training/entities_test.spacy

# Evaluate Intent model
python3 cyber-train/test_models.py \
  --evaluate-intent cyber-train/spacy-training/intents_test.spacy
```

### Expected Metrics

**NER Model:**
- Overall F1 Score: > 0.75 (good), > 0.85 (excellent)
- Precision: Should be balanced with recall
- Per-entity F1: Check which entity types perform best

**Intent Model:**
- Overall Accuracy: > 0.80 (good), > 0.90 (excellent)
- Top-3 Accuracy: How often correct intent is in top 3
- Per-intent Accuracy: Check which intents are well-classified

## 🐍 Python Usage Examples

### Basic Usage

```python
import spacy

# Load models
nlp_ner = spacy.load("cyber-train/models/ner_model/model-best")
nlp_intent = spacy.load("cyber-train/models/intent_model/model-best")

# Process text
query = "I need to investigate IP 192.168.1.1 for malware activity"

# Extract entities
doc_ner = nlp_ner(query)
entities = [(ent.text, ent.label_) for ent in doc_ner.ents]
print(f"Entities: {entities}")

# Classify intent
doc_intent = nlp_intent(query)
top_intent = max(doc_intent.cats.items(), key=lambda x: x[1])
print(f"Intent: {top_intent[0]} ({top_intent[1]:.2%} confidence)")
```

### Combined Pipeline

```python
import spacy

nlp_ner = spacy.load("cyber-train/models/ner_model/model-best")
nlp_intent = spacy.load("cyber-train/models/intent_model/model-best")

def analyze_query(text):
    """Analyze a query and return entities and intents."""
    # Get entities
    doc_ner = nlp_ner(text)
    entities = [
        {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char}
        for ent in doc_ner.ents
    ]
    
    # Get intents
    doc_intent = nlp_intent(text)
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)[:5]
    intents = [{"intent": k, "score": float(v)} for k, v in intents]
    
    return {
        "text": text,
        "entities": entities,
        "intents": intents
    }

# Example usage
result = analyze_query("APT41 used WannaCry malware to attack IP 192.168.1.1")
print(json.dumps(result, indent=2))
```

## 🚨 Troubleshooting

### Model Not Loading

**Error**: `OSError: Can't find model 'cyber-train/models/ner_model/model-best'`

**Solution**: 
1. Check if model directory exists: `ls -la cyber-train/models/ner_model/`
2. Verify model was trained successfully
3. Check if you're in the correct directory

### Low Performance

**Issue**: Models not extracting entities or classifying intents correctly

**Solutions**:
1. **Check training data quality**: Review preparation report
2. **Add more examples**: Low-performing entity/intent types need more data
3. **Retrain with more epochs**: Edit config and increase `max_steps`
4. **Check class balance**: Ensure all types have sufficient examples

### Memory Issues

**Error**: Out of memory during testing

**Solutions**:
1. Process text in smaller batches
2. Use CPU instead of GPU
3. Reduce batch size in config

## 📈 Performance Benchmarks

### Good Performance Indicators

- **NER F1 Score**: > 0.75
- **Intent Accuracy**: > 0.80
- **Entity Recall**: > 0.70 (finds most entities)
- **Intent Top-3 Accuracy**: > 0.90 (correct intent in top 3)

### Per-Entity Performance

Check which entity types perform best/worst:
- High-frequency entities (IP_ADDRESS, DOMAIN) should have F1 > 0.85
- Low-frequency entities may have lower F1 but should still be > 0.60

## ✅ Testing Checklist

- [ ] Models load without errors
- [ ] NER extracts entities correctly
- [ ] Intent classification works
- [ ] Test suite passes
- [ ] Evaluation metrics are acceptable
- [ ] Models work on real-world queries
- [ ] Performance meets requirements

## 🎯 Next Steps After Testing

1. **If performance is good**: Deploy models to production
2. **If performance needs improvement**: 
   - Add more training data
   - Fine-tune hyperparameters
   - Retrain models
3. **Monitor in production**: Track accuracy over time
4. **Continuous improvement**: Add new examples regularly

---

For more details, see `NEXT_STEPS.md`


