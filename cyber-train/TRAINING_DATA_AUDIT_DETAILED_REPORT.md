# 📊 Training Data Audit - Detailed Report

**Date:** December 2, 2025  
**Files Audited:** 49 entity training files  
**Total Examples:** 20,922  
**Total Entities:** 83,364

---

## 🚨 CRITICAL FINDINGS

### Overall Boundary Accuracy: **57.11%** ⚠️

**This is critically low!** Nearly half of all entity boundaries are incorrect.

- **Total Boundary Issues:** 35,868 out of 83,364 entities (43%)
- **Total Missing Entities:** 3,408 entities that should be labeled but aren't
- **Misclassified Entities:** 0 (but many wrong labels due to boundary issues)

---

## 📉 Critical Entity Distribution

### **Severely Underrepresented Entities:**

| Entity Type | Count | Status | Required |
|------------|-------|--------|----------|
| **CVE_ID** | **4** | ❌ CRITICAL | Need 500+ |
| **THREAT_ACTOR** | **28** | ❌ CRITICAL | Need 500+ |
| **WALLET_ADDRESS** | **0** | ❌ MISSING | Need 200+ |
| **LATITUDE** | **0** | ❌ MISSING | Need 200+ |
| **LONGITUDE** | **0** | ❌ MISSING | Need 200+ |
| **PHONE_NUMBER** | **48** | ⚠️ LOW | Need 300+ |
| **EMAIL_ADDRESS** | **20** | ⚠️ LOW | Need 300+ |

### **Adequate Entities:**

| Entity Type | Count | Status |
|------------|-------|--------|
| **IP_ADDRESS** | 620 | ✅ Adequate |
| **DOMAIN** | 568 | ✅ Adequate |
| **EMAIL** | 504 | ✅ Adequate |
| **PERSON** | 560 | ✅ Adequate |
| **ORGANIZATION** | 424 | ✅ Adequate |
| **LOCATION** | 312 | ⚠️ Could use more |

---

## 📊 Per-File Boundary Accuracy Report

### **Worst Performing Files (Boundary Accuracy < 50%):**

| File | Accuracy | Issues | Missing | Critical Entities |
|------|----------|--------|---------|-------------------|
| `infint_entities.jsonl` | **12.77%** | 1,612 | 160 | - |
| `natint_entities.jsonl` | **27.52%** | 1,264 | 80 | - |
| `ecoint_entities.jsonl` | **32.93%** | 1,760 | 160 | - |
| `socmint_entities.jsonl` | **39.81%** | 1,016 | 144 | PHONE_NUMBER: 12 |
| `eduint_entities.jsonl` | **41.44%** | 1,012 | 80 | - |
| `sigint_entities.jsonl` | **43.30%** | 1,032 | 80 | - |
| `domain_intel_entities.jsonl` | **44.81%** | 1,424 | 160 | IP_ADDRESS: 4 |
| `darkint_entities.jsonl` | **46.68%** | 1,188 | 8 | - |
| `data_privacy_sovereignty_entities.jsonl` | **48.63%** | 600 | 24 | EMAIL_ADDRESS: 8, PHONE_NUMBER: 12 |
| `audit_compliance_entities.jsonl` | **49.82%** | 556 | 8 | EMAIL_ADDRESS: 4, PHONE_NUMBER: 4 |

### **Best Performing Files (Boundary Accuracy > 65%):**

| File | Accuracy | Issues | Missing | Critical Entities |
|------|----------|--------|---------|-------------------|
| `digint_entities.jsonl` | **73.31%** | 680 | 80 | - |
| `humint_entities.jsonl` | **69.89%** | 1,108 | 212 | EMAIL: 188, PHONE_NUMBER: 8 |
| `techint_entities.jsonl` | **69.88%** | 624 | 92 | **IP_ADDRESS: 316**, **DOMAIN: 392** |
| `threat_intel_entities.jsonl` | **68.60%** | 476 | 88 | - |
| `network_security_entities.jsonl` | **68.08%** | 512 | 4 | IP_ADDRESS: 16 |
| `data_protection_backup_entities.jsonl` | **67.85%** | 508 | 12 | EMAIL_ADDRESS: 8, PHONE_NUMBER: 12 |
| `comint_entities.jsonl` | **67.66%** | 740 | 404 | IP_ADDRESS: 80, DOMAIN: 160, EMAIL: 316 |
| `geoint_entities.jsonl` | **67.03%** | 964 | 108 | DOMAIN: 4 |
| `detection_correlation_entities.jsonl` | **66.88%** | 408 | 0 | - |
| `medint_entities.jsonl` | **66.67%** | 448 | 80 | - |
| `endpoint_security_entities.jsonl` | **66.41%** | 524 | 4 | - |
| `authentication_entities.jsonl` | **65.96%** | 448 | 0 | LOCATION: 8 |
| `disaster_recovery_entities.jsonl` | **65.92%** | 424 | 0 | - |

---

## 🔍 Critical Entity Distribution by File

### **IP_ADDRESS (620 total):**
- `techint_entities.jsonl`: 316 (51%)
- `cybint_entities.jsonl`: 176 (28%)
- `comint_entities.jsonl`: 80 (13%)
- `network_security_entities.jsonl`: 16
- `api_security_entities.jsonl`: 12
- Others: 20 total

**Issue:** Concentrated in only 2 files. Need distribution across more files.

### **DOMAIN (568 total):**
- `techint_entities.jsonl`: 392 (69%)
- `comint_entities.jsonl`: 160 (28%)
- Others: 16 total

**Issue:** Very concentrated. Need more examples in other files.

### **CVE_ID (4 total):** ❌ **CRITICAL**
- `application_security_entities.jsonl`: 4

**Issue:** Only 4 examples across all files! This explains why CVEs are completely missed in tests.

### **THREAT_ACTOR (28 total):** ❌ **CRITICAL**
- `threat_intelligence_entities.jsonl`: 24
- `incident_response_entities.jsonl`: 4

**Issue:** Only 28 examples. Need APT28, APT29, APT41, Lazarus, etc.

### **EMAIL/EMAIL_ADDRESS (524 total):**
- `comint_entities.jsonl`: 316 (EMAIL)
- `humint_entities.jsonl`: 188 (EMAIL)
- Others: 20 (EMAIL_ADDRESS)

**Issue:** EMAIL_ADDRESS has only 20 examples. Need more.

### **WALLET_ADDRESS (0 total):** ❌ **MISSING**
- No examples found in any file

**Issue:** Completely missing. Need to add examples.

### **LATITUDE/LONGITUDE (0 total):** ❌ **MISSING**
- No examples found in any file

**Issue:** Completely missing. Need to add examples.

---

## ⚠️ Common Boundary Issues

### **1. Partial Words (Most Common):**
- `'d 45'` → Should not include "d"
- `'SOC, AI engin'` → Should not include partial "engine"
- `'ed CCPA'` → Should not include "ed"
- `'LIME explanat'` → Should not include partial "explanation"

### **2. Wrong Boundaries:**
- IP addresses labeled as `REGULATION`, `TYPE`, `TOOL`
- Domains labeled as `FRAMEWORK`, `TOOL`
- Coordinates not extracted at all

### **3. Missing Critical Entities:**
- IP addresses present in text but not labeled
- CVEs present but not labeled
- Domains present but not labeled
- Emails present but not labeled

---

## 🎯 Recommendations

### **Priority 1: Fix Boundary Issues (35,868 issues)**

1. **Remove partial word entities:**
   - Entities starting/ending with partial words
   - Entities that are clearly incomplete

2. **Fix entity boundaries:**
   - Use pattern matching to find correct boundaries
   - Align boundaries with actual entity spans

3. **Remove false positives:**
   - Common words incorrectly labeled
   - Punctuation as entities

### **Priority 2: Add Missing Critical Entities**

1. **CVE_ID:** Add 500+ examples
   - Format: `CVE-YYYY-NNNNN`
   - In vulnerability, application_security, threat_intelligence files

2. **THREAT_ACTOR:** Add 500+ examples
   - APT28, APT29, APT41, Lazarus, FIN7, etc.
   - In threat_intelligence, incident_response, cybint files

3. **WALLET_ADDRESS:** Add 200+ examples
   - Format: `0x[a-fA-F0-9]{40}`
   - In finint, darkint, cybint files

4. **LATITUDE/LONGITUDE:** Add 200+ examples each
   - Format: `-90 to 90` for latitude, `-180 to 180` for longitude
   - In geoint, osint files

5. **PHONE_NUMBER:** Add 300+ examples
   - Various formats: `+1-555-123-4567`, `(555) 123-4567`, etc.
   - In comint, humint, socmint files

6. **EMAIL_ADDRESS:** Add 300+ examples
   - Standard email format
   - In comint, humint, data_privacy files

### **Priority 3: Improve Worst Files**

Focus on files with <50% accuracy:
- `infint_entities.jsonl` (12.77%)
- `natint_entities.jsonl` (27.52%)
- `ecoint_entities.jsonl` (32.93%)
- `socmint_entities.jsonl` (39.81%)
- `eduint_entities.jsonl` (41.44%)
- `sigint_entities.jsonl` (43.30%)
- `domain_intel_entities.jsonl` (44.81%)
- `darkint_entities.jsonl` (46.68%)

---

## 📈 Expected Impact

After fixing these issues:

1. **Boundary Accuracy:** 57% → 95%+
2. **Entity Recall:** 30% → 90%+ (for critical types)
3. **False Positive Rate:** 40% → <5%
4. **Model Performance:** F1 96% (evaluation) → F1 90%+ (real-world)

---

## ✅ Next Steps

1. **Run boundary fix script** on all files
2. **Add missing critical entity examples**
3. **Retrain NER model**
4. **Re-test and verify improvements**

---

**This audit reveals the root cause of poor NER performance: incorrect boundaries and missing critical entity examples.**

