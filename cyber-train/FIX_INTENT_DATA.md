# 🔧 Fix: Intent Data Binary Conversion

## Issue
The intent training data has values like `0.5`, but `textcat_multilabel` only accepts `0` or `1`.

## Solution
The `prepare_spacy_training.py` script has been updated to automatically convert all intent values to binary (0 or 1) using a threshold of 0.5.

## Steps to Fix

### 1. Re-run Data Preparation (with Binary Conversion)

```bash
# Reconvert intent data with binary values
python3 cyber-train/prepare_spacy_training.py --intents-only
```

This will:
- Load all intent JSONL files
- Convert all values >= 0.5 → 1.0
- Convert all values < 0.5 → 0.0
- Regenerate the .spacy files with binary values

### 2. Retrain Intent Model

```bash
# Retrain with the fixed data
python3 cyber-train/train_spacy_models.py --intent-only --skip-config
```

### 3. Test the Model

```bash
# Test the trained model
python3 cyber-train/test_models.py --test-suite
```

## What Changed

**Before:**
```json
{"cats": {"INVESTIGATE": 1.0, "DETECT": 1.0, "RESPOND_TO_INCIDENT": 0.5}}
```

**After (in .spacy file):**
```json
{"cats": {"INVESTIGATE": 1.0, "DETECT": 1.0, "RESPOND_TO_INCIDENT": 1.0}}
```

Values >= 0.5 become 1.0, values < 0.5 become 0.0.

## Verification

After reconverting, you can verify the fix worked by checking the training output - it should show:
```
⚠️  Converted X non-binary intent values to binary (threshold: 0.5)
```

Then training should proceed without the `[E851]` error.


