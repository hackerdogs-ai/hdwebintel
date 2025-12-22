# Minimal Integration Guide

**What you need to include these models in another project**

---

## 📦 Required Files

### 1. Model Files (Required)

Copy these directories to your project:

```
your-project/
└── models/
    ├── ner_model/
    │   └── model-best/          # NER model directory
    │       ├── config.cfg
    │       ├── meta.json
    │       ├── tokenizer/
    │       ├── vocab/
    │       └── ... (all model files)
    └── intent_model/
        └── model-best/           # Intent model directory
            ├── config.cfg
            ├── meta.json
            ├── vocab/
            └── ... (all model files)
```

**Size:** ~50-200 MB per model (depending on training data)

---

## 🔧 Dependencies

### Python Requirements

**Minimum Python version:** 3.8+

**Required packages:**

```txt
spacy>=3.7.0
```

That's it! Just spaCy.

**Install:**
```bash
pip install spacy
```

---

## 💻 Minimal Usage Code

### Basic Integration (3 files)

#### 1. `requirements.txt`
```txt
spacy>=3.7.0
```

#### 2. `model_loader.py`
```python
import spacy
from pathlib import Path

class NLPModels:
    def __init__(self, model_dir="models"):
        self.model_dir = Path(model_dir)
        self.ner_model = None
        self.intent_model = None
        self._load_models()
    
    def _load_models(self):
        """Load NER and Intent models."""
        ner_path = self.model_dir / "ner_model" / "model-best"
        intent_path = self.model_dir / "intent_model" / "model-best"
        
        if not ner_path.exists():
            raise FileNotFoundError(f"NER model not found at {ner_path}")
        if not intent_path.exists():
            raise FileNotFoundError(f"Intent model not found at {intent_path}")
        
        self.ner_model = spacy.load(str(ner_path))
        self.intent_model = spacy.load(str(intent_path))
    
    def extract_entities(self, text):
        """Extract entities from text."""
        if self.ner_model is None:
            raise RuntimeError("NER model not loaded")
        
        doc = self.ner_model(text)
        return [(ent.text, ent.label_) for ent in doc.ents]
    
    def classify_intents(self, text, threshold=0.3):
        """Classify intents from text."""
        if self.intent_model is None:
            raise RuntimeError("Intent model not loaded")
        
        doc = self.intent_model(text)
        intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
        return [(intent, score) for intent, score in intents if score >= threshold]
    
    def analyze(self, text, threshold=0.3):
        """Extract entities and classify intents."""
        entities = self.extract_entities(text)
        intents = self.classify_intents(text, threshold)
        return {
            "entities": entities,
            "intents": intents
        }
```

#### 3. `example_usage.py`
```python
from model_loader import NLPModels

# Initialize models
nlp = NLPModels(model_dir="models")

# Extract entities
text = "Check IP 192.168.1.1 for suspicious activity"
entities = nlp.extract_entities(text)
print(f"Entities: {entities}")

# Classify intents
intents = nlp.classify_intents(text)
print(f"Intents: {intents}")

# Combined analysis
result = nlp.analyze(text)
print(f"Result: {result}")
```

---

## 📋 Quick Start

### Step 1: Copy Models

```bash
# From your training directory
cp -r cyber-train/models/ner_model/model-best /path/to/your-project/models/ner_model/
cp -r cyber-train/models/intent_model/model-best /path/to/your-project/models/intent_model/
```

### Step 2: Install Dependencies

```bash
pip install spacy
```

### Step 3: Use in Your Code

```python
import spacy

# Load models
ner_model = spacy.load("models/ner_model/model-best")
intent_model = spacy.load("models/intent_model/model-best")

# Use
doc = ner_model("Check IP 192.168.1.1")
entities = [(e.text, e.label_) for e in doc.ents]
print(entities)
```

---

## 🎯 Minimal File Structure

```
your-project/
├── models/
│   ├── ner_model/
│   │   └── model-best/          # Copy entire directory
│   └── intent_model/
│       └── model-best/          # Copy entire directory
├── requirements.txt              # Just: spacy>=3.7.0
└── your_code.py                  # Your application code
```

---

## 💡 Integration Examples

### Example 1: Simple Function

```python
import spacy

# Load once (do this at startup)
ner_model = spacy.load("models/ner_model/model-best")
intent_model = spacy.load("models/intent_model/model-best")

def process_text(text):
    """Process text and return entities and intents."""
    # Extract entities
    doc_ner = ner_model(text)
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    
    # Classify intents
    doc_intent = intent_model(text)
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    intents = [(intent, score) for intent, score in intents if score >= 0.3]
    
    return {"entities": entities, "intents": intents}
```

### Example 2: Class-Based

```python
import spacy
from pathlib import Path

class TextAnalyzer:
    def __init__(self, model_dir="models"):
        self.ner_model = spacy.load(str(Path(model_dir) / "ner_model" / "model-best"))
        self.intent_model = spacy.load(str(Path(model_dir) / "intent_model" / "model-best"))
    
    def analyze(self, text):
        doc_ner = self.ner_model(text)
        doc_intent = self.intent_model(text)
        
        return {
            "entities": [(e.text, e.label_) for e in doc_ner.ents],
            "intents": [(intent, score) for intent, score in sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True) if score >= 0.3]
        }

# Usage
analyzer = TextAnalyzer()
result = analyzer.analyze("Check IP 192.168.1.1")
```

### Example 3: With Error Handling

```python
import spacy
from pathlib import Path

class NLPModels:
    def __init__(self, model_dir="models"):
        self.model_dir = Path(model_dir)
        self.ner_model = None
        self.intent_model = None
        self._load_models()
    
    def _load_models(self):
        try:
            ner_path = self.model_dir / "ner_model" / "model-best"
            intent_path = self.model_dir / "intent_model" / "model-best"
            
            if not ner_path.exists():
                raise FileNotFoundError(f"NER model not found: {ner_path}")
            if not intent_path.exists():
                raise FileNotFoundError(f"Intent model not found: {intent_path}")
            
            self.ner_model = spacy.load(str(ner_path))
            self.intent_model = spacy.load(str(intent_path))
            print("✅ Models loaded successfully")
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise
    
    def extract_entities(self, text):
        if self.ner_model is None:
            raise RuntimeError("NER model not loaded")
        doc = self.ner_model(text)
        return [(ent.text, ent.label_) for ent in doc.ents]
    
    def classify_intents(self, text, threshold=0.3):
        if self.intent_model is None:
            raise RuntimeError("Intent model not loaded")
        doc = self.intent_model(text)
        intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
        return [(intent, score) for intent, score in intents if score >= threshold]
```

---

## 📦 Package Distribution

### Option 1: Copy Models Directly

```bash
# Include models in your project
your-project/
├── models/          # Copy model directories here
├── src/
└── requirements.txt
```

### Option 2: Separate Models Package

```bash
# Create a separate package for models
models-package/
├── models/
│   ├── ner_model/
│   └── intent_model/
├── setup.py
└── README.md
```

### Option 3: Download from Storage

```python
# Download models from S3/GCS/etc. at runtime
import boto3
import zipfile
from pathlib import Path

def download_models():
    s3 = boto3.client('s3')
    s3.download_file('your-bucket', 'models.zip', 'models.zip')
    with zipfile.ZipFile('models.zip', 'r') as zip_ref:
        zip_ref.extractall('models')
```

---

## ⚡ Performance Tips

### 1. Load Models Once

```python
# ✅ Good: Load once at startup
ner_model = spacy.load("models/ner_model/model-best")

def process(text):
    return ner_model(text)

# ❌ Bad: Loading on every call
def process(text):
    model = spacy.load("models/ner_model/model-best")  # Slow!
    return model(text)
```

### 2. Batch Processing

```python
# Process multiple texts efficiently
texts = ["text1", "text2", "text3"]
docs = list(ner_model.pipe(texts))  # Faster than individual calls
```

### 3. Cache Results (Optional)

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_extract(text):
    doc = ner_model(text)
    return [(e.text, e.label_) for e in doc.ents]
```

---

## 🔍 Model Information

### NER Model
- **Labels:** 565 entity types
- **Pipeline:** tok2vec, ner
- **Size:** ~50-200 MB

### Intent Model
- **Labels:** 3,040 intent types
- **Pipeline:** textcat_multilabel
- **Size:** ~50-200 MB

---

## ✅ Checklist

- [ ] Copy `model-best` directories to your project
- [ ] Install `spacy>=3.7.0`
- [ ] Load models with `spacy.load()`
- [ ] Use models in your code
- [ ] Handle errors appropriately

---

## 🚨 Common Issues

### Issue 1: Model Not Found
```
FileNotFoundError: Can't find model 'models/ner_model/model-best'
```
**Solution:** Check path is correct and model directory exists

### Issue 2: spaCy Version Mismatch
```
ValueError: Model incompatible with spaCy version
```
**Solution:** Ensure `spacy>=3.7.0` is installed

### Issue 3: Memory Issues
```
MemoryError: Unable to allocate memory
```
**Solution:** Models are large (~200MB each). Ensure sufficient RAM.

---

## 📝 Summary

**Minimal Requirements:**
1. ✅ Model files (copy `model-best` directories)
2. ✅ `spacy>=3.7.0` package
3. ✅ Load with `spacy.load()`
4. ✅ Use in your code

**That's it!** Just 3 things needed.

---

**Status:** ✅ **Minimal Integration Guide Complete**

