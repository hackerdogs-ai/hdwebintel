# NLP Examples - Usage Guide

This directory contains practical examples demonstrating how to use the trained NER and Intent Classification models for cybersecurity, OSINT, and SaaS Operations use cases.

---

## 📁 Files Overview

### 1. `basic_usage.py`
**Basic usage examples** showing how to:
- Load the trained models
- Extract entities from text
- Classify intents from text
- Handle common use cases

**Run:**
```bash
cd /Users/tredkar/Documents/GitHub/hdwebintel/cyber-train
source ../venv/bin/activate
python3 nlp_examples/basic_usage.py
```

---

### 2. `cybersecurity_use_cases.py`
**Cybersecurity scenarios** including:
- Incident response analysis
- Threat hunting queries
- Vulnerability management
- Compliance auditing
- Security monitoring

**Run:**
```bash
python3 nlp_examples/cybersecurity_use_cases.py
```

---

### 3. `osint_use_cases.py`
**OSINT investigation scenarios** including:
- Social media investigation
- Threat actor attribution
- Geolocation analysis
- Image verification
- Domain investigation

**Run:**
```bash
python3 nlp_examples/osint_use_cases.py
```

---

### 4. `saas_operations_use_cases.py`
**SaaS Operations scenarios** including:
- API monitoring
- Cloud infrastructure management
- AI model deployment
- Customer support
- Performance optimization

**Run:**
```bash
python3 nlp_examples/saas_operations_use_cases.py
```

---

### 5. `batch_processing.py`
**Batch processing example** showing how to:
- Process multiple queries efficiently
- Generate reports
- Handle errors gracefully
- Analyze results

**Run:**
```bash
python3 nlp_examples/batch_processing.py
```

---

## 🚀 Quick Start

### Basic Example

```python
import spacy

# Load models
ner_model = spacy.load("cyber-train/models/ner_model/model-best")
intent_model = spacy.load("cyber-train/models/intent_model/model-best")

# Analyze a query
query = "Check IP 192.168.1.1 for suspicious activity"

# Extract entities
doc_ner = ner_model(query)
entities = [(e.text, e.label_) for e in doc_ner.ents]
print(f"Entities: {entities}")

# Classify intents
doc_intent = intent_model(query)
intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
top_intents = [(intent, score) for intent, score in intents if score >= 0.3]
print(f"Intents: {top_intents[:5]}")
```

---

## 📊 Model Performance

### Training Metrics
- **Precision:** 97.19%
- **Recall:** 94.76%
- **F1 Score:** 95.96%

### Test Suite Metrics
- **Precision:** 84.57%
- **Recall:** 41.52%
- **F1 Score:** 55.69%

---

## 🏷️ Supported Entity Types

The models support **573 unique entity types** including:

- **Network:** IP_ADDRESS, IPV6_ADDRESS, DOMAIN, URL, PORT, PROTOCOL_TYPE
- **Security:** CVE_ID, MALWARE_TYPE, THREAT_ACTOR, HASH, INCIDENT_ID
- **AI/ML:** LLM_PROVIDER, LLM_MODEL, AI_MODEL
- **Compliance:** COMPLIANCE_FRAMEWORK, REGULATION
- **OSINT:** EMOJI, LATITUDE, LONGITUDE, DMS_COORDINATES, GEOJSON
- **PII:** EMAIL_ADDRESS, PHONE_NUMBER, SSN, CREDIT_CARD
- **Social Media:** INSTAGRAM_USERNAME, FACEBOOK_URL, LINKEDIN_URL, etc.
- **GitHub:** GITHUB_REPO_URL, GITHUB_USER, GITHUB_ORGANIZATION, etc.
- **And many more...**

---

## 🎯 Supported Intent Types

The models support **3,058 unique intent types** including:

- **Investigation:** INVESTIGATE, INVESTIGATE_THREATS, INVESTIGATE_INCIDENT
- **Detection:** DETECT, DETECT_ANOMALIES, DETECT_MALWARE
- **Response:** RESPOND_TO_INCIDENT, CONTAIN_THREAT, ISOLATE_ASSETS
- **Analysis:** ANALYZE, ANALYZE_BEHAVIOR, ANALYZE_THREATS
- **Compliance:** ENSURE_COMPLIANCE, AUDIT_COMPLIANCE, VALIDATE_COMPLIANCE
- **Monitoring:** MONITOR, TRACK, TRACK_METRICS
- **And many more...**

---

## 💡 Usage Tips

### 1. Entity Extraction
- Entities are extracted as `(text, label)` tuples
- Multiple entities can be found in a single query
- Entity boundaries are precise (character-level)

### 2. Intent Classification
- Multiple intents can be detected per query (multilabel)
- Intents are scored from 0.0 to 1.0
- Filter by threshold (e.g., 0.3) to get relevant intents

### 3. Performance
- Models are optimized for batch processing
- Use `nlp.pipe()` for processing multiple texts efficiently
- Models are thread-safe for concurrent processing

### 4. Error Handling
- Always check if models loaded successfully
- Handle cases where no entities/intents are found
- Use try-except blocks for robust error handling

---

## 📝 Example Output

```
======================================================================
QUERY: APT28 used WannaCry ransomware to attack IP 172.16.0.1
======================================================================

🏷️  Entities Found (3):
   • APT28 → THREAT_ACTOR
   • WannaCry → MALWARE_TYPE
   • 172.16.0.1 → IP_ADDRESS

🎯 Top Intents (5):
   • INVESTIGATE: 0.9230 (92.3%)
   • INVESTIGATE_THREATS: 0.9312 (93.1%)
   • DETECT: 0.9264 (92.6%)
   • TRACK_ACTORS: 0.9285 (92.9%)
   • ANALYZE_ADVERSARIES: 0.8734 (87.3%)
```

---

## 🔧 Requirements

- Python 3.8+
- spaCy 3.0+
- Trained models in `cyber-train/models/`

---

## 📚 Additional Resources

- Model training scripts: `train_spacy_models.py`
- Test suite: `comprehensive_test_suite.py`
- Training data preparation: `prepare_spacy_training.py`

---

**Status:** ✅ Examples ready for use

