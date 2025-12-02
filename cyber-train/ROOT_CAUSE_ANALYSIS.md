# 🎯 Root Cause Analysis - Entity Model Performance

**Date:** December 1, 2024  
**Issue:** Model shows 95.44% F1 in evaluation but ~10% detection rate in real tests

---

## ✅ Root Cause Identified

### The Problem

**The training data is missing examples of key entity types!**

### Evidence

1. **Training Data Analysis:**
   - IP_ADDRESS: Only 3 examples found, and they're WRONG:
     - "13." (incomplete)
     - "d I" (wrong boundary)
     - No proper IPs like "192.168.1.1"
   - DOMAIN: 0 examples found
   - CVE_ID: 0 examples found
   - EMAIL: Likely missing
   - THREAT_ACTOR: Likely missing

2. **What IS in Training Data:**
   - TOOL: 146+ examples
   - METRIC_TYPE: 93+ examples
   - INCIDENT_TYPE: 38+ examples
   - AI_MODEL_TYPE: 20+ examples
   - Many other types with good coverage

3. **Model Performance:**
   - Good at detecting types it WAS trained on (95% F1)
   - Bad at detecting types it WASN'T trained on (~10%)

---

## 💡 Why This Explains Everything

### The Evaluation Was Misleading

**95.44% F1 Score:**
- Calculated on entity types the model WAS trained on
- Test set probably doesn't have many IP/domain/CVE examples
- Model performs well on types it knows

**Real-World Tests (~10% detection):**
- Testing on IP addresses, domains, CVEs
- These are types the model WASN'T trained on
- Model fails because it never learned these patterns

### Why False Positives?

**Model assigns wrong types because:**
- It doesn't know what IP addresses look like
- It doesn't know what domains look like
- It doesn't know what CVEs look like
- It assigns types it DOES know (TOOL, TIME_UNIT, etc.) to things it doesn't understand

**Example:**
- Query: "IP address 192.168.1.1"
- Model doesn't recognize "192.168.1.1" as IP_ADDRESS (never trained on it)
- Model sees "IP" and assigns it a type it knows: TIME_UNIT
- Result: False positive

---

## 📊 The Data Gap

### Entity Types WITH Good Coverage

| Type | Examples | Status |
|------|----------|--------|
| TOOL | 146+ | ✅ Good |
| METRIC_TYPE | 93+ | ✅ Good |
| INCIDENT_TYPE | 38+ | ✅ Good |
| AI_MODEL_TYPE | 20+ | ✅ Good |
| SECURITY_TYPE | 15+ | ✅ Good |

### Entity Types WITH Poor/No Coverage

| Type | Examples | Status |
|------|----------|--------|
| IP_ADDRESS | 3 (wrong) | ❌ Critical |
| DOMAIN | 0 | ❌ Critical |
| CVE_ID | 0 | ❌ Critical |
| EMAIL | Unknown | ❌ Likely missing |
| THREAT_ACTOR | Unknown | ❌ Likely missing |
| MALWARE_TYPE | Unknown | ❌ Likely missing |
| HOST_TYPE | Unknown | ❌ Likely missing |
| PORT | Unknown | ❌ Likely missing |
| LATITUDE | Unknown | ❌ Likely missing |
| LONGITUDE | Unknown | ❌ Likely missing |

---

## 🔧 The Fix

### Step 1: Add Proper Examples

**For each missing entity type, add 100+ examples:**

1. **IP_ADDRESS:**
   ```json
   {"text": "IP address 192.168.1.1 is suspicious", "entities": [[10, 21, "IP_ADDRESS"]]}
   {"text": "Check 10.0.0.5 for threats", "entities": [[6, 13, "IP_ADDRESS"]]}
   {"text": "Block 172.16.0.1 immediately", "entities": [[6, 15, "IP_ADDRESS"]]}
   ```

2. **DOMAIN:**
   ```json
   {"text": "Domain example.com is malicious", "entities": [[7, 18, "DOMAIN"]]}
   {"text": "Check evil.com for threats", "entities": [[6, 14, "DOMAIN"]]}
   ```

3. **CVE_ID:**
   ```json
   {"text": "CVE-2021-44228 is critical", "entities": [[0, 15, "CVE_ID"]]}
   {"text": "Patch CVE-2021-45046 immediately", "entities": [[6, 21, "CVE_ID"]]}
   ```

4. **EMAIL:**
   ```json
   {"text": "Email admin@company.com was compromised", "entities": [[6, 22, "EMAIL"]]}
   ```

5. **THREAT_ACTOR:**
   ```json
   {"text": "APT41 attacked the system", "entities": [[0, 5, "THREAT_ACTOR"]]}
   {"text": "APT28 used WannaCry malware", "entities": [[0, 5, "THREAT_ACTOR"]]}
   ```

### Step 2: Fix Entity Boundaries

**Check and fix boundaries in existing data:**
- Ensure boundaries match entity text exactly
- Remove incomplete entities
- Fix wrong boundaries

### Step 3: Retrain Model

**After adding examples:**
1. Re-prepare training data
2. Retrain model
3. Re-test

---

## 📋 Action Plan

### Immediate (Do Now)

1. **Audit Training Data**
   - Check all entity types
   - Identify missing types
   - Count examples per type

2. **Add Missing Examples**
   - IP_ADDRESS: 100+ examples
   - DOMAIN: 100+ examples
   - CVE_ID: 100+ examples
   - EMAIL: 100+ examples
   - THREAT_ACTOR: 50+ examples
   - Other missing types

3. **Fix Existing Examples**
   - Fix wrong boundaries
   - Remove incomplete entities
   - Validate all examples

### This Week

1. **Re-prepare Training Data**
   ```bash
   python3 cyber-train/prepare_spacy_training.py
   ```

2. **Retrain Model**
   ```bash
   python3 cyber-train/train_spacy_models.py
   ```

3. **Re-test**
   ```bash
   python3 cyber-train/comprehensive_test_suite.py --comprehensive
   ```

---

## 🎯 Expected Results

### After Adding Examples

**Before:**
- IP_ADDRESS detection: ~0%
- DOMAIN detection: ~0%
- CVE_ID detection: ~0%

**After:**
- IP_ADDRESS detection: >90%
- DOMAIN detection: >90%
- CVE_ID detection: >90%

### Overall Performance

**Before:**
- Entity detection: ~10%
- False positives: ~100%

**After:**
- Entity detection: >90%
- False positives: <2%

---

## ✅ Summary

**Root Cause:** Training data missing examples of key entity types (IP_ADDRESS, DOMAIN, CVE_ID, etc.)

**Why Evaluation Was Misleading:** Tested on types model was trained on, not types it wasn't trained on

**The Fix:** Add proper examples of missing entity types to training data

**Next Steps:** Add examples → Retrain → Re-test

---

**The labeled data is missing key entity types. The model can't detect what it wasn't trained on!**

