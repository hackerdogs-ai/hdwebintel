# 🎯 Next Steps Action Plan

**Date:** December 2, 2025  
**Current Status:** ✅ All 3 steps complete - Ready for improvement iteration

---

## 📊 Current Performance

### Test Suite Results
- **Precision:** 51.0% ✅ (up from 36.2%, +41.0%)
- **Recall:** 21.3% ✅ (up from 12.1%, +76.2%)
- **F1 Score:** 30.1% ✅ (up from 18.1%, +66.3%)
- **False Positives:** 71 (down from 74, -4.1%)
- **Missed Entities:** 270

### Training Metrics (Excellent)
- **NER Precision:** 96.52%
- **NER Recall:** 92.65%
- **NER F1:** 94.55%

**Gap Analysis:** Training metrics are excellent, but test suite shows lower performance due to:
1. False positives in training data
2. Missing examples for underrepresented entity types
3. Model being conservative on unseen patterns

---

## 🎯 Priority Actions

### **Phase 1: Fix False Positives** (Priority: HIGH)

**Goal:** Reduce false positives from 71 to <20

#### 1.1 Fix TOOL False Positives (12 instances)
**Issue:** Common words like "CSRF", "JavaScript", "Base64", "JSON" labeled as TOOL

**Action:**
```bash
# Create script to remove TOOL false positives
python3 fix_tool_false_positives.py
```

**Target:** Remove 10-12 TOOL false positives

#### 1.2 Fix REPOSITORY vs URL Confusion (6 instances)
**Issue:** URLs incorrectly labeled as REPOSITORY

**Action:**
```bash
# Fix URL/REPOSITORY label confusion
python3 fix_url_repository_confusion.py
```

**Target:** Fix 6 REPOSITORY false positives

#### 1.3 Fix DATE vs FILE_PATH Confusion (4 instances)
**Issue:** File paths like `C:\Users\Admin\Desktop\malware.exe` labeled as DATE

**Action:**
```bash
# Fix DATE/FILE_PATH label confusion
python3 fix_date_filepath_confusion.py
```

**Target:** Fix 4 DATE false positives

#### 1.4 Fix DOMAIN/EMAIL False Positives (8 instances)
**Issue:** False domain and email detections

**Action:**
```bash
# Improve domain/email validation
python3 fix_domain_email_false_positives.py
```

**Target:** Fix 8 DOMAIN/EMAIL false positives

**Expected Result:** Reduce false positives from 71 to ~40-45

---

### **Phase 2: Add Examples for Missed Entities** (Priority: HIGH)

**Goal:** Improve recall from 21.3% to >40%

#### 2.1 Top 5 Most Missed Entity Types

**Target Entity Types:**
1. **MALWARE_TYPE** (16 missed) - Add 200 examples
2. **HASH** (15 missed) - Add 200 examples
3. **EMOJI** (15 missed) - Add 200 examples
4. **DATE** (14 missed) - Add 200 examples
5. **COMPLIANCE_FRAMEWORK** (14 missed) - Add 200 examples

**Action:**
```bash
# Add examples for top missed entities
python3 add_missed_entity_examples.py --focus-top-5
```

**Target:** Add 1,000 examples for top 5 types

#### 2.2 Next 10 Most Missed Entity Types

**Target Entity Types:**
6. **URL** (13 missed) - Add 150 examples
7. **PHONE_NUMBER** (11 missed) - Add 150 examples
8. **THREAT_ACTOR** (10 missed) - Add 150 examples
9. **IP_ADDRESS** (10 missed) - Add 150 examples
10. **LLM_MODEL** (10 missed) - Add 150 examples
11. **EMAIL_ADDRESS** (9 missed) - Add 100 examples
12. **LLM_PROVIDER** (7 missed) - Add 100 examples
13. **SSN** (6 missed) - Add 100 examples
14. **TIME** (5 missed) - Add 100 examples
15. **LATITUDE** (5 missed) - Add 100 examples

**Action:**
```bash
# Add examples for next 10 missed entities
python3 add_missed_entity_examples.py --focus-next-10
```

**Target:** Add 1,250 examples for next 10 types

**Expected Result:** Improve recall from 21.3% to >40%

---

### **Phase 3: Add Negative Examples** (Priority: MEDIUM)

**Goal:** Help model learn what NOT to extract

**Action:**
```bash
# Add negative examples (sentences with no entities)
python3 add_negative_examples.py
```

**Target:** Add 500-1,000 negative examples (2-4% of training data)

**Expected Result:** Further reduce false positives

---

### **Phase 4: Retrain and Re-test** (Priority: HIGH)

**Goal:** Validate improvements

#### 4.1 Re-prepare Training Data
```bash
python3 prepare_spacy_training.py --base-dir entities-intent
```

#### 4.2 Retrain Models
```bash
python3 train_spacy_models.py --gpu
```

#### 4.3 Re-run Comprehensive Tests
```bash
python3 comprehensive_test_suite.py --comprehensive
```

**Expected Results:**
- **Precision:** >70% (up from 51.0%)
- **Recall:** >40% (up from 21.3%)
- **F1 Score:** >50% (up from 30.1%)
- **False Positives:** <20 (down from 71)

---

## 📋 Detailed Action Plan

### **Step 1: Create False Positive Fix Scripts** (1-2 hours)

Create scripts to fix each category of false positives:

1. **`fix_tool_false_positives.py`**
   - Remove common words from TOOL entity
   - Add validation: TOOL must be a real tool name
   - Examples to remove: "CSRF", "JavaScript", "Base64", "JSON", "Debunk", "Relative"

2. **`fix_url_repository_confusion.py`**
   - Distinguish URLs from repositories
   - URLs: http://, https://, ftp://
   - Repositories: github.com/user/repo, gitlab.com/user/repo

3. **`fix_date_filepath_confusion.py`**
   - Distinguish dates from file paths
   - Dates: YYYY-MM-DD, MM/DD/YYYY, etc.
   - File paths: C:\, /home/, \\server\, etc.

4. **`fix_domain_email_false_positives.py`**
   - Improve domain validation
   - Improve email validation
   - Remove false detections

### **Step 2: Create Missed Entity Examples Script** (2-3 hours)

Create `add_missed_entity_examples.py` to add examples for top 15 missed types:

**Features:**
- Generate realistic examples for each entity type
- Use diverse contexts and formats
- Ensure correct boundaries
- Distribute across relevant pillar files

**Target:** Add 2,250 examples total

### **Step 3: Create Negative Examples Script** (1 hour)

Create `add_negative_examples.py` to add sentences with no entities:

**Features:**
- Generate realistic sentences with no entities
- Cover various topics and contexts
- Help model learn boundaries

**Target:** Add 500-1,000 negative examples

### **Step 4: Execute All Fixes** (1 hour)

Run all scripts in sequence:
```bash
# Fix false positives
python3 fix_tool_false_positives.py
python3 fix_url_repository_confusion.py
python3 fix_date_filepath_confusion.py
python3 fix_domain_email_false_positives.py

# Add missed entity examples
python3 add_missed_entity_examples.py --focus-top-5
python3 add_missed_entity_examples.py --focus-next-10

# Add negative examples
python3 add_negative_examples.py
```

### **Step 5: Re-prepare, Retrain, Re-test** (2-3 hours)

```bash
# Re-prepare
python3 prepare_spacy_training.py --base-dir entities-intent

# Retrain
python3 train_spacy_models.py --gpu

# Re-test
python3 comprehensive_test_suite.py --comprehensive
```

---

## 📊 Success Metrics

### Target Performance (After All Fixes)

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| **Precision** | 51.0% | >70% | +37% |
| **Recall** | 21.3% | >40% | +88% |
| **F1 Score** | 30.1% | >50% | +66% |
| **False Positives** | 71 | <20 | -72% |
| **Missed Entities** | 270 | <150 | -44% |

### Phase-by-Phase Targets

**After Phase 1 (Fix False Positives):**
- Precision: >60% (up from 51.0%)
- False Positives: <40 (down from 71)

**After Phase 2 (Add Examples):**
- Recall: >35% (up from 21.3%)
- Missed Entities: <200 (down from 270)

**After Phase 3 (Add Negatives):**
- False Positives: <25 (down from 40)
- Precision: >65% (up from 60%)

**After Phase 4 (Retrain):**
- All metrics should meet targets

---

## 🚀 Quick Start (Recommended Order)

### **Option 1: Quick Win (2-3 hours)**
Focus on false positives first for immediate precision improvement:

1. Fix TOOL false positives (30 min)
2. Fix URL/REPOSITORY confusion (30 min)
3. Fix DATE/FILE_PATH confusion (30 min)
4. Re-prepare, retrain, re-test (1-2 hours)

**Expected:** Precision >60%, False Positives <40

### **Option 2: Balanced Approach (4-5 hours)**
Fix false positives + add examples for top 5 missed types:

1. Fix all false positives (1-2 hours)
2. Add examples for top 5 missed types (1-2 hours)
3. Re-prepare, retrain, re-test (1-2 hours)

**Expected:** Precision >65%, Recall >30%, False Positives <30

### **Option 3: Comprehensive (6-8 hours)**
Complete all phases:

1. Fix all false positives (1-2 hours)
2. Add examples for all 15 missed types (2-3 hours)
3. Add negative examples (1 hour)
4. Re-prepare, retrain, re-test (2-3 hours)

**Expected:** All targets met

---

## 📝 Implementation Notes

### False Positive Fixes

**TOOL Entity:**
- Remove common words: "CSRF", "JavaScript", "Base64", "JSON", "Debunk", "Relative"
- Add validation: Must be a real tool name (e.g., "Nmap", "Wireshark", "Metasploit")
- Check against tool list

**REPOSITORY vs URL:**
- URLs: Must start with http://, https://, ftp://
- Repositories: Must be in format github.com/user/repo or gitlab.com/user/repo
- Fix label confusion in training data

**DATE vs FILE_PATH:**
- Dates: Must match date patterns (YYYY-MM-DD, MM/DD/YYYY, etc.)
- File paths: Must contain path separators (/, \, :\)
- Fix label confusion in training data

### Missed Entity Examples

**MALWARE_TYPE:**
- Add: WannaCry, NotPetya, Zeus, Emotet, TrickBot, Stuxnet, Conficker, Code Red
- Use diverse contexts: "detected", "variant", "family", "campaign"

**HASH:**
- Add: MD5 (32 hex), SHA1 (40 hex), SHA256 (64 hex)
- Use diverse contexts: "hash", "checksum", "fingerprint", "digest"

**EMOJI:**
- Add: Common emojis in various contexts
- Use diverse contexts: social media, messages, posts

**DATE:**
- Add: Various formats (YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY, etc.)
- Use diverse contexts: "on", "at", "since", "until"

**COMPLIANCE_FRAMEWORK:**
- Add: PCI DSS, HIPAA, SOC 2, FedRAMP, NIST CSF, CMMC, FISMA, FIPS 140-2
- Use diverse contexts: "compliance", "audit", "requirements", "framework"

---

## ✅ Summary

**Current Status:** ✅ All 3 steps complete, significant improvements achieved

**Next Priority:** Fix false positives and add examples for missed entities

**Expected Timeline:**
- **Quick Win:** 2-3 hours → Precision >60%
- **Balanced:** 4-5 hours → Precision >65%, Recall >30%
- **Comprehensive:** 6-8 hours → All targets met

**Recommended:** Start with **Option 2 (Balanced Approach)** for best ROI

---

**Ready to proceed?** Start with Phase 1 (Fix False Positives) for immediate precision improvement!
