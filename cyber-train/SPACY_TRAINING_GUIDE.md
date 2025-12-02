# 🚀 Complete Guide: Training spaCy Models for Cybersecurity & OSINT

This guide provides step-by-step instructions for preparing JSONL training data and training custom spaCy models for Named Entity Recognition (NER) and Intent Classification in cybersecurity and OSINT domains.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Data Preparation](#data-preparation)
4. [Model Training](#model-training)
5. [Evaluation](#evaluation)
6. [Usage](#usage)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This training pipeline creates two specialized spaCy models:

1. **NER Model**: Extracts cybersecurity and OSINT entities (IP addresses, CVEs, threat actors, domains, etc.)
2. **Intent Classification Model**: Classifies user queries into cybersecurity and OSINT intents (investigate, detect, monitor, analyze, etc.)

### Current Dataset Statistics

- **Entity Types**: 1,067 unique entity labels
- **Intent Types**: 3,057 unique intent labels
- **Training Examples**: ~5,000+ entity examples, ~5,000+ intent examples
- **Coverage**: 24 cybersecurity pillars + 25 OSINT pillars

---

## 🔧 Prerequisites

### 1. Install Required Packages

```bash
pip install spacy>=3.7.0
python -m spacy download en_core_web_sm  # Base English model
```

### 2. Verify Installation

```bash
python -c "import spacy; print(spacy.__version__)"
```

### 3. Directory Structure

Ensure you have the following structure:

```
cyber-train/
├── entities-intent/
│   ├── osint/
│   │   ├── socmint/
│   │   │   ├── socmint_entities.jsonl
│   │   │   └── socmint_intent.jsonl
│   │   └── ...
│   └── incident_response/
│       ├── incident_response_entities.jsonl
│       └── incident_response_intent.jsonl
├── spacy-training/          # Created by prepare script
└── models/                  # Created by train script
```

---

## 📊 Data Preparation

### Step 1: Prepare JSONL Files for Training

The `prepare_spacy_training.py` script:
- Validates all JSONL files
- Converts JSONL to spaCy's binary `.spacy` format
- Splits data into train/dev/test sets (70/15/15 by default)
- Generates statistics and reports

#### Run Data Preparation

```bash
# Process both entities and intents
python cyber-train/prepare_spacy_training.py

# Process only entities
python cyber-train/prepare_spacy_training.py --entities-only

# Process only intents
python cyber-train/prepare_spacy_training.py --intents-only

# Custom data split ratios
python cyber-train/prepare_spacy_training.py --train-ratio 0.8 --dev-ratio 0.1 --test-ratio 0.1
```

#### Output Files

After running the preparation script, you'll have:

```
cyber-train/spacy-training/
├── entities_train.spacy      # Training data for NER
├── entities_dev.spacy        # Development/validation data for NER
├── entities_test.spacy       # Test data for NER
├── entity_labels.txt         # List of all entity labels
├── intents_train.spacy       # Training data for Intent Classification
├── intents_dev.spacy         # Development/validation data for Intent Classification
├── intents_test.spacy        # Test data for Intent Classification
├── intent_labels.txt         # List of all intent labels
└── preparation_report.txt    # Detailed statistics report
```

### Step 2: Review Data Quality

Check the preparation report:

```bash
cat cyber-train/spacy-training/preparation_report.txt
```

Key things to verify:
- ✅ Total examples loaded
- ✅ Number of unique labels
- ✅ Train/dev/test split ratios
- ✅ No format errors

---

## 🎓 Model Training

### Step 1: Train NER Model

The `train_spacy_models.py` script handles:
- Creating spaCy config files
- Training models with optimal hyperparameters
- Evaluating on test sets
- Generating evaluation reports

#### Run Training

```bash
# Train both NER and Intent models
python cyber-train/train_spacy_models.py

# Train only NER model
python cyber-train/train_spacy_models.py --ner-only

# Train only Intent Classification model
python cyber-train/train_spacy_models.py --intent-only

# Use GPU (if available)
python cyber-train/train_spacy_models.py --gpu

# Skip config creation (use existing configs)
python cyber-train/train_spacy_models.py --skip-config
```

#### Training Process

1. **Config Creation**: Automatically generates optimized config files
2. **Training**: Trains model with early stopping based on dev set performance
3. **Evaluation**: Evaluates best model on test set
4. **Output**: Saves `model-best` and `model-last` in output directory

### Step 2: Monitor Training

Training output includes:
- Training loss and metrics
- Validation metrics (precision, recall, F1)
- Best model checkpoint saved automatically
- Training time and iterations

### Step 3: Review Training Results

After training, check:

```bash
# NER Model evaluation
cat cyber-train/models/ner_model/ner_evaluation.json

# Intent Model evaluation
cat cyber-train/models/intent_model/intent_evaluation.json
```

---

## 📈 Evaluation

### Manual Evaluation

You can evaluate models manually:

```bash
# Evaluate NER model
python -m spacy evaluate \
  cyber-train/models/ner_model/model-best \
  cyber-train/spacy-training/entities_test.spacy \
  --output cyber-train/models/ner_evaluation.json

# Evaluate Intent model
python -m spacy evaluate \
  cyber-train/models/intent_model/model-best \
  cyber-train/spacy-training/intents_test.spacy \
  --output cyber-train/models/intent_evaluation.json
```

### Expected Performance

Based on dataset size and quality:
- **NER Model**: F1 score of 75-85% (varies by entity type)
- **Intent Model**: Accuracy of 80-90% (varies by intent category)

---

## 💻 Usage

### Load and Use NER Model

```python
import spacy

# Load the trained NER model
nlp_ner = spacy.load("cyber-train/models/ner_model/model-best")

# Process text
text = "APT41 used WannaCry malware to attack IP 192.168.1.1. CVE-2021-44228 was exploited."
doc = nlp_ner(text)

# Extract entities
for ent in doc.ents:
    print(f"{ent.text} -> {ent.label_}")

# Output:
# APT41 -> THREAT_ACTOR
# WannaCry -> MALWARE_TYPE
# 192.168.1.1 -> IP_ADDRESS
# CVE-2021-44228 -> CVE_ID
```

### Load and Use Intent Model

```python
import spacy

# Load the trained Intent Classification model
nlp_intent = spacy.load("cyber-train/models/intent_model/model-best")

# Process text
text = "I need to investigate this suspicious IP address for potential threats"
doc = nlp_intent(text)

# Get intent predictions
for intent, score in sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"{intent}: {score:.4f}")

# Output:
# INVESTIGATE: 0.9850
# DETECT: 0.8230
# ANALYZE: 0.7120
# MONITOR: 0.4560
# VALIDATE: 0.2340
```

### Combined Pipeline

```python
import spacy

# Load both models
nlp_ner = spacy.load("cyber-train/models/ner_model/model-best")
nlp_intent = spacy.load("cyber-train/models/intent_model/model-best")

# Process query
query = "Analyze the malware sample from IP 10.0.0.1 and extract IOCs"

# Get intent
intent_doc = nlp_intent(query)
top_intent = max(intent_doc.cats.items(), key=lambda x: x[1])

# Get entities
ner_doc = nlp_ner(query)
entities = [(ent.text, ent.label_) for ent in ner_doc.ents]

print(f"Intent: {top_intent[0]} (confidence: {top_intent[1]:.2%})")
print(f"Entities: {entities}")

# Output:
# Intent: ANALYZE_MALWARE_SAMPLE (confidence: 92.50%)
# Entities: [('10.0.0.1', 'IP_ADDRESS'), ('IOCs', 'IOC_TYPE')]
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. "No module named 'spacy'"

```bash
pip install spacy
```

#### 2. "FileNotFoundError: entities_train.spacy"

Run the data preparation script first:
```bash
python cyber-train/prepare_spacy_training.py
```

#### 3. "ValueError: [E1030] Attempted to create overlapping entity"

This means entity spans overlap in your training data. The preparation script should catch these, but if not:
- Review the JSONL files for overlapping entities
- Ensure entity spans don't overlap
- Use `alignment_mode="contract"` or `alignment_mode="expand"` in the conversion

#### 4. Low Model Performance

- **Increase training data**: Add more examples to JSONL files
- **Balance classes**: Ensure all entity/intent types have sufficient examples
- **Tune hyperparameters**: Edit config files to adjust learning rate, batch size, etc.
- **Check data quality**: Review preparation report for errors

#### 5. Out of Memory Errors

- Reduce batch size in config file
- Use smaller transformer models
- Process data in smaller chunks

### Config File Customization

Edit config files to customize training:

```bash
# Edit NER config
nano cyber-train/models/configs/config_ner.cfg

# Edit Intent config
nano cyber-train/models/configs/config_intent.cfg
```

Key parameters to adjust:
- `[training.batch_size]`: Increase for faster training (if memory allows)
- `[training.optimizer.learn_rate]`: Adjust learning rate (default: 0.001)
- `[training.max_epochs]`: Maximum training iterations
- `[components.ner.model]`: Choose transformer model (e.g., `roberta-base`)

---

## 📚 Additional Resources

- [spaCy Training Documentation](https://spacy.io/usage/training)
- [spaCy NER Training Guide](https://spacy.io/usage/training#ner)
- [spaCy Text Classification Guide](https://spacy.io/usage/training#textcat)
- [spaCy Config System](https://spacy.io/usage/training#config)

---

## 🎯 Next Steps

1. **Fine-tune Models**: Adjust config files for better performance
2. **Add More Data**: Continuously improve by adding more examples
3. **Deploy Models**: Integrate into production systems
4. **Monitor Performance**: Track model performance on real-world data
5. **Update Regularly**: Retrain models as new data becomes available

---

## 📝 Notes

- Training time varies based on dataset size and hardware
- GPU training is significantly faster (10-50x speedup)
- Models are saved as `model-best` (best dev performance) and `model-last` (final iteration)
- Always evaluate on held-out test set before deployment

---

**Generated**: 2025-01-XX  
**Dataset Version**: 1.0  
**spaCy Version**: 3.7.0+


