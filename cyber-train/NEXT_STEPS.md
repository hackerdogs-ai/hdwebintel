# 🎯 Next Steps After Training

Congratulations! Your spaCy models have been trained. Here's what to do next:

## ✅ Step 1: Test the Models

### Quick Test

```bash
# Run comprehensive test suite
python3 cyber-train/test_models.py --test-suite

# Test a single query
python3 cyber-train/test_models.py --text "APT41 used WannaCry malware to attack IP 192.168.1.1"

# Interactive mode
python3 cyber-train/test_models.py --interactive
```

### Expected Output

The test suite will show:
- ✅ Entities extracted (IP addresses, CVEs, threat actors, etc.)
- ✅ Intent classifications with confidence scores
- ✅ Model performance on various cybersecurity and OSINT queries

## 📊 Step 2: Evaluate on Test Set

Evaluate model performance on the held-out test set:

```bash
# Evaluate NER model
python3 cyber-train/test_models.py \
  --evaluate-ner cyber-train/spacy-training/entities_test.spacy

# Evaluate Intent model
python3 cyber-train/test_models.py \
  --evaluate-intent cyber-train/spacy-training/intents_test.spacy
```

This will generate evaluation reports with:
- Precision, Recall, F1 scores
- Per-entity-type performance (for NER)
- Per-intent performance (for Intent Classification)
- Confusion matrices

## 🔍 Step 3: Review Evaluation Results

Check the evaluation JSON files:

```bash
# View NER evaluation
cat cyber-train/models/ner_model/ner_test_evaluation.json | python3 -m json.tool

# View Intent evaluation
cat cyber-train/models/intent_model/intent_test_evaluation.json | python3 -m json.tool
```

### Key Metrics to Check

**For NER Model:**
- **Overall F1 Score**: Should be > 0.75 for good performance
- **Per-entity F1**: Check which entity types perform well/poorly
- **Precision vs Recall**: Balance between false positives and false negatives

**For Intent Model:**
- **Overall Accuracy**: Should be > 0.80 for good performance
- **Per-intent Accuracy**: Check which intents are well-classified
- **Top-3 Accuracy**: How often the correct intent is in top 3 predictions

## 🚀 Step 4: Use Models in Your Application

### Python Integration

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

### API Integration

Create a simple REST API:

```python
from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)
nlp_ner = spacy.load("cyber-train/models/ner_model/model-best")
nlp_intent = spacy.load("cyber-train/models/intent_model/model-best")

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.json.get('text', '')
    
    # Extract entities
    doc_ner = nlp_ner(text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc_ner.ents]
    
    # Classify intent
    doc_intent = nlp_intent(text)
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return jsonify({
        "entities": entities,
        "intents": [{"intent": k, "score": v} for k, v in intents]
    })

if __name__ == '__main__':
    app.run(debug=True)
```

## 🔧 Step 5: Fine-tuning (If Needed)

If performance is not satisfactory:

### 1. Add More Training Data

- Identify low-performing entity types or intents
- Add more examples to JSONL files
- Re-run training

### 2. Adjust Model Configuration

Edit config files:

```bash
# Edit NER config
nano cyber-train/models/configs/config_ner.cfg

# Key parameters to adjust:
# - [training.batch_size]: Increase for faster training
# - [training.optimizer.learn_rate]: Adjust learning rate
# - [training.max_epochs]: More iterations
```

### 3. Use Transformer Models

For better performance, use transformer-based models:

```bash
# Install transformer support
pip install spacy-transformers

# Update config to use transformer
# Edit config file to use transformer model (e.g., roberta-base)
```

## 📈 Step 6: Monitor Performance

### Track Model Performance

1. **Log predictions** for analysis
2. **Collect user feedback** on incorrect predictions
3. **Monitor entity/intent distribution** in production
4. **Track accuracy over time**

### Create Performance Dashboard

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

## 🎓 Step 7: Continuous Improvement

### Regular Retraining

1. **Weekly/Monthly**: Add new examples from production
2. **Quarterly**: Full retraining with expanded dataset
3. **Annually**: Review and update entity/intent taxonomies

### Data Collection

- Collect real-world queries
- Identify common patterns
- Add edge cases
- Balance class distributions

## 📚 Additional Resources

### Documentation

- [spaCy Usage Guide](https://spacy.io/usage)
- [spaCy Models](https://spacy.io/models)
- [spaCy Training](https://spacy.io/usage/training)

### Tools

- **Prodigy**: Advanced annotation tool for improving training data
- **spaCy Projects**: Template-based project management
- **Weights & Biases**: Training experiment tracking

## 🐛 Troubleshooting

### Low Performance

1. **Check data quality**: Review preparation report
2. **Balance classes**: Ensure all types have enough examples
3. **Increase training data**: More examples = better performance
4. **Tune hyperparameters**: Adjust learning rate, batch size

### Model Not Loading

```bash
# Verify model files exist
ls -la cyber-train/models/ner_model/model-best/
ls -la cyber-train/models/intent_model/model-best/

# Check spaCy version compatibility
python3 -c "import spacy; print(spacy.__version__)"
```

### Memory Issues

- Use smaller batch sizes
- Process in chunks
- Use CPU instead of GPU
- Reduce model size

## ✅ Checklist

- [ ] Models trained successfully
- [ ] Test suite passes
- [ ] Evaluation metrics reviewed
- [ ] Models integrated into application
- [ ] Performance monitoring set up
- [ ] Documentation updated
- [ ] Team trained on model usage

---

**Next**: Start using the models in your cybersecurity and OSINT workflows! 🚀


