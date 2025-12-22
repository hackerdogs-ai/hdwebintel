# Quick Start: Integration in 3 Steps

**Minimal requirements to use these models in another project**

---

## 🚀 3-Step Integration

### Step 1: Copy Models (5 minutes)

```bash
# Option A: Use the script
./COPY_MODELS.sh /path/to/your-project/models

# Option B: Manual copy
cp -r cyber-train/models/ner_model/model-best /path/to/your-project/models/ner_model/
cp -r cyber-train/models/intent_model/model-best /path/to/your-project/models/intent_model/
```

### Step 2: Install Dependency (1 minute)

```bash
pip install spacy
```

### Step 3: Use in Your Code (2 minutes)

```python
import spacy

# Load models
ner_model = spacy.load("models/ner_model/model-best")
intent_model = spacy.load("models/intent_model/model-best")

# Extract entities
doc = ner_model("Check IP 192.168.1.1")
entities = [(e.text, e.label_) for e in doc.ents]
print(entities)  # [('192.168.1.1', 'IP_ADDRESS')]

# Classify intents
doc = intent_model("Check IP 192.168.1.1")
intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
print(intents[:3])  # Top 3 intents
```

**Done!** ✅

---

## 📦 What You Need

### Files to Copy:
- `models/ner_model/model-best/` (entire directory)
- `models/intent_model/model-best/` (entire directory)

### Dependencies:
- `spacy>=3.7.0` (that's it!)

### Code:
- Just `spacy.load()` and use!

---

## 💻 Copy-Paste Ready Code

```python
import spacy
from pathlib import Path

# Load models (do this once at startup)
MODEL_DIR = Path("models")
ner_model = spacy.load(str(MODEL_DIR / "ner_model" / "model-best"))
intent_model = spacy.load(str(MODEL_DIR / "intent_model" / "model-best"))

# Extract entities
def get_entities(text):
    doc = ner_model(text)
    return [(e.text, e.label_) for e in doc.ents]

# Classify intents
def get_intents(text, threshold=0.3):
    doc = intent_model(text)
    intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
    return [(intent, score) for intent, score in intents if score >= threshold]

# Use
entities = get_entities("Check IP 192.168.1.1")
intents = get_intents("Check IP 192.168.1.1")
```

---

## 📁 Project Structure

```
your-project/
├── models/
│   ├── ner_model/
│   │   └── model-best/          # Copy this entire directory
│   └── intent_model/
│       └── model-best/           # Copy this entire directory
├── requirements.txt              # Just: spacy>=3.7.0
└── your_code.py                  # Your application
```

---

## ✅ Checklist

- [ ] Copy model directories
- [ ] Install `spacy`
- [ ] Load models with `spacy.load()`
- [ ] Use in your code

**Total time: ~10 minutes**

---

**That's it!** No complex setup needed.

