# 🔍 Entity Model Diagnosis Report

**Date:** December 1, 2024  
**Issue:** Model showing 95.44% F1 in evaluation but ~10% detection rate in real tests

---

## 🚨 The Problem

**Previous Evaluation:** 95.44% F1 Score ✅  
**Current Test Results:** ~10% detection rate, 100% false positives ❌

**This is a critical discrepancy that needs diagnosis.**

---

## 🔍 Diagnostic Checks

### 1. Model Loading

**Check:** Is the correct model being loaded?

**Findings:**
- Model path: `cyber-train/models/ner_model/model-best`
- Model exists: ✅
- Model loads successfully: ✅

**Status:** Model is loading correctly.

---

### 2. Training Data Quality

**Check:** Does training data have examples for key entity types?

**Key Entity Types to Check:**
- IP_ADDRESS
- DOMAIN
- CVE_ID
- EMAIL
- THREAT_ACTOR

**Findings:**
- [ ] Check if IP_ADDRESS examples exist in training data
- [ ] Check if DOMAIN examples exist
- [ ] Check if CVE_ID examples exist
- [ ] Check entity boundaries are correct
- [ ] Check for false positives in training data

**Action:** Run diagnostic script to check training data.

---

### 3. Training Timeline

**Check:** Was model retrained after adding negative examples?

**Critical Question:**
- When were negative examples added?
- When was model last trained?
- Was model trained WITH negative examples?

**Possible Issues:**
1. **Model trained BEFORE negative examples** → Model doesn't know about negatives
2. **Model trained AFTER negative examples** → But training data may have issues
3. **Model never retrained** → Using old model

**Action:** Check file modification times.

---

### 4. Entity Boundaries

**Check:** Are entity boundaries correct in training data?

**Example:**
```json
{"text": "IP address 192.168.1.1 is suspicious", "entities": [[10, 21, "IP_ADDRESS"]]}
```

**Issues to Check:**
- Boundaries include extra characters
- Boundaries miss characters
- Boundaries overlap
- Boundaries don't match text

**Action:** Validate entity boundaries in training data.

---

### 5. False Positives in Training Data

**Check:** Does training data contain false positives?

**Common False Positives:**
- "IP" → TIME_UNIT
- "host" → PRIORITIZATION_TYPE
- "port" → SERVICE
- "Incident" → SOURCE_TYPE

**If these exist in training data:**
- Model learned them as correct
- Model will predict them
- This explains the false positives

**Action:** Check training data for false positive patterns.

---

### 6. Model Evaluation vs Real Tests

**Check:** Why does evaluation show 95.44% F1 but real tests show ~10%?

**Possible Explanations:**

1. **Evaluation on Different Data**
   - Evaluation used test set from training
   - Real tests use different queries
   - Model overfitted to test set

2. **Evaluation Metrics Misleading**
   - F1 score calculated differently
   - Evaluation on easy examples
   - Real tests use harder examples

3. **Model Degradation**
   - Model was retrained with bad data
   - Model lost performance
   - Previous model was better

4. **Data Format Mismatch**
   - Training data format different from test
   - Entity boundaries different
   - Label names different

**Action:** Compare evaluation data with test data.

---

## 🎯 Root Cause Hypotheses

### Hypothesis 1: Model Not Retrained After Negatives

**Scenario:**
- Negative examples added
- Model NOT retrained
- Model still has old behavior

**Evidence:**
- Check model modification time vs negative examples time
- If model older → Not retrained

**Fix:**
- Retrain model with negative examples

---

### Hypothesis 2: Training Data Has False Positives

**Scenario:**
- Training data contains false positives
- Model learned them as correct
- Model predicts them

**Evidence:**
- Check training data for false positive patterns
- If found → Training data issue

**Fix:**
- Clean training data
- Remove false positives
- Retrain model

---

### Hypothesis 3: Entity Boundaries Wrong

**Scenario:**
- Training data has wrong boundaries
- Model learned wrong patterns
- Model can't detect correctly

**Evidence:**
- Check entity boundaries in training data
- If wrong → Boundary issue

**Fix:**
- Fix entity boundaries
- Retrain model

---

### Hypothesis 4: Model Overfitted to Test Set

**Scenario:**
- Model trained and evaluated on same test set
- Model memorized test set
- Model fails on new data

**Evidence:**
- Check if test set was used in training
- If yes → Overfitting

**Fix:**
- Use separate test set
- Retrain model

---

### Hypothesis 5: Wrong Model Loaded

**Scenario:**
- Multiple models exist
- Wrong model being loaded
- Old/bad model used

**Evidence:**
- Check model paths
- Check model modification times
- Check model evaluation results

**Fix:**
- Load correct model
- Verify model performance

---

## 📋 Diagnostic Checklist

- [ ] Check model is loading correctly
- [ ] Check training data has examples for key types
- [ ] Check training timeline (model vs negatives)
- [ ] Check entity boundaries in training data
- [ ] Check for false positives in training data
- [ ] Compare evaluation data with test data
- [ ] Check if model was retrained
- [ ] Check if wrong model is loaded
- [ ] Check model evaluation metrics

---

## 🔧 Next Steps

1. **Run Diagnostic Scripts**
   - Check model loading
   - Check training data
   - Check training timeline
   - Check entity boundaries

2. **Identify Root Cause**
   - Review diagnostic results
   - Determine which hypothesis is correct
   - Document findings

3. **Fix Issues**
   - Retrain model if needed
   - Clean training data if needed
   - Fix entity boundaries if needed
   - Fix model loading if needed

4. **Re-test**
   - Run comprehensive test suite
   - Compare with previous results
   - Verify improvements

---

## 📊 Expected Findings

Based on the symptoms:

**Most Likely:**
1. Model not retrained after adding negatives
2. Training data has false positives
3. Entity boundaries incorrect

**Less Likely:**
1. Wrong model loaded
2. Model overfitted
3. Evaluation metrics misleading

---

**Run diagnostic scripts to identify the root cause!**

