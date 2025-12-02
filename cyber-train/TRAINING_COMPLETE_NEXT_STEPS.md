# ✅ Training Complete - Next Steps

## Status

Both models have been successfully trained:

- ✅ **NER Model**: `cyber-train/models/ner_model/model-best/`
- ✅ **Intent Model**: `cyber-train/models/intent_model/model-best/`

## Next Steps

### Step 1: Review Evaluation Results

Check the evaluation metrics:

```bash
# NER Model evaluation
cat cyber-train/models/ner_model/NER_evaluation.json | python3 -m json.tool

# Intent Model evaluation  
cat cyber-train/models/intent_model/INTENT_evaluation.json | python3 -m json.tool
```

### Step 2: Test Models with Real Queries

Run comprehensive test suite:

```bash
cd /Users/tredkar/Documents/GitHub/hdwebintel
source venv/bin/activate
python3 cyber-train/comprehensive_test_suite.py --comprehensive
```

**Test options:**
- `--comprehensive`: Full test suite (30+ test cases)
- `--interactive`: Interactive testing mode
- `--text "your query here"`: Test single query

### Step 3: Use Models in Your Application

```python
import spacy

# Load models
ner_model = spacy.load('cyber-train/models/ner_model/model-best')
intent_model = spacy.load('cyber-train/models/intent_model/model-best')

# Extract entities
text = "Check IP 192.168.1.1 for threats from APT41"
doc = ner_model(text)
entities = [(ent.text, ent.label_) for ent in doc.ents]
print("Entities:", entities)

# Classify intent
doc = intent_model(text)
intents = {label: score for label, score in doc.cats.items() if score > 0.5}
print("Intents:", intents)
```

### Step 4: Monitor Performance

- Test with production-like queries
- Collect false positives/negatives
- Add examples to training data for retraining

## Quick Commands

```bash
# Test models
python3 cyber-train/comprehensive_test_suite.py --comprehensive

# Test single query
python3 cyber-train/comprehensive_test_suite.py --text "Investigate suspicious activity on 10.0.0.1"

# Interactive testing
python3 cyber-train/comprehensive_test_suite.py --interactive
```

## Model Locations

- **NER Model**: `cyber-train/models/ner_model/model-best/`
- **Intent Model**: `cyber-train/models/intent_model/model-best/`
- **Training Data**: `cyber-train/models/training_data/`
- **Configs**: `cyber-train/models/configs/`

---

**Training is complete! Proceed to testing and deployment.** 🎉

