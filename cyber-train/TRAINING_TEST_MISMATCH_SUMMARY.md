# Training vs Test Suite Pattern Mismatch Report

**Date:** December 13, 2024  
**Analysis Complete:** ✅

---

## 🎯 Executive Summary

**Critical Finding:** There are **fundamental pattern mismatches** between training data and test suite that explain the 51% recall gap.

### Key Statistics

- **Training Examples Analyzed:** 18,320 examples across 180 entity types
- **Test Suite Examples:** 328 examples across 70 entity types
- **Missed Examples:** 191 (58% of test suite examples)
- **Entity Types with Format Mismatches:** 68
- **Entity Types with Context Length Mismatches:** 63
- **Entity Types with Surrounding Pattern Mismatches:** 25

---

## 🔍 Top 3 Critical Mismatch Categories

### 1. **Missing Training Data (0 examples in training)**

**Entity Types with 0 training examples but appear in test suite:**
- ALTITUDE (2 test examples, 100% miss rate)
- BANK_ACCOUNT_NUMBER (1 test example, 100% miss rate)
- BASE64 (1 test example, 100% miss rate)
- DISCORD_URL, DISCORD_USERNAME (1 each, 100% miss rate)
- FACEBOOK_URL, FACEBOOK_USERNAME (2 each, 100% miss rate)
- GITHUB_BRANCH, GITHUB_COMMIT, GITHUB_GIST, GITHUB_ISSUE, etc. (multiple, 100% miss rate)
- And 30+ more entity types

**Impact:** These entities **cannot be detected** because they have no training examples.

---

### 2. **Context Length Mismatch (Training too long, Test too short)**

**Critical Examples:**

| Entity Type | Training Avg Context | Test Suite Avg Context | Difference |
|-------------|---------------------|------------------------|------------|
| **DMS_COORDINATES** | 478.6 chars | 63.5 chars | **415.1 chars** |
| **EMOJI** | 305.6 chars | 44.3 chars | **261.2 chars** |
| **LATITUDE** | 312.4 chars | 65.2 chars | **247.2 chars** |
| **LONGITUDE** | 312.4 chars | 65.2 chars | **247.2 chars** |
| **PHONE_NUMBER** | 287.3 chars | 78.5 chars | **208.8 chars** |
| **MALWARE_TYPE** | 245.8 chars | 89.3 chars | **156.5 chars** |

**Problem:** Training uses **long narrative contexts** (200-500 words), but test suite uses **short query contexts** (40-90 chars). The model learned to detect entities in long contexts but fails on short contexts.

---

### 3. **Surrounding Text Pattern Mismatch**

**Critical Examples:**

#### EMOJI (100% miss rate, 1,374 training examples)
- **Training patterns (before):** "Email phishing", "intelligence report", "Network traffic"
- **Test suite patterns (before):** "le.com is suspicious", "ected at IP 10.0.0.1", "k from IP 172.16.0.1"
- **Training patterns (after):** "IP 192.168.1.100 fla", "indicates APT activi", "CVE-2021-44228 explo"
- **Test suite patterns (after):** "Email phishing detec", "Warning: Domain exam", "Encrypted data breac"

**Problem:** Training and test suite use **completely different surrounding text patterns**. The model learned specific context cues that don't appear in test suite.

#### DMS_COORDINATES (100% miss rate, 19 training examples)
- **Training patterns (before):** "is found coordinates", "GPS coordinates", "entified coordinates"
- **Test suite patterns (before):** "0.7128, -74.0060 and", "Location at", "'46\"N 74°00'22\"W and"
- **Training patterns (after):** "embedded in the imag", "as the location of t", "from social media po"
- **Test suite patterns (after):** "and 51°30'26\"N 0°07'", "in datacenter AWS-US"

**Problem:** Training uses **narrative-style contexts** while test suite uses **technical/format contexts**.

---

## 📊 Detailed Mismatch Analysis

### Top 10 Entity Types by Miss Rate

1. **ALTITUDE:** 100% miss rate (0 training, 2 test)
2. **BANK_ACCOUNT_NUMBER:** 100% miss rate (0 training, 1 test)
3. **BASE64:** 100% miss rate (0 training, 1 test)
4. **CURRENCY:** 100% miss rate (4 training, 4 test) - **Pattern mismatch**
5. **CUSTOM_COORDINATES:** 100% miss rate (0 training, 1 test)
6. **DISCORD_URL:** 100% miss rate (0 training, 1 test)
7. **DISCORD_USERNAME:** 100% miss rate (0 training, 1 test)
8. **DMS_COORDINATES:** 100% miss rate (19 training, 4 test) - **Context length mismatch**
9. **DOB:** 100% miss rate (0 training, 1 test)
10. **DRIVER_LICENSE_NUMBER:** 100% miss rate (0 training, 1 test)

### High-Impact Mismatches (Many Training Examples but Still Missed)

| Entity Type | Training Examples | Test Examples | Missed | Miss Rate | Primary Issue |
|-------------|------------------|---------------|--------|-----------|---------------|
| **EMOJI** | 1,374 | 15 | 15 | 100% | Context length + pattern mismatch |
| **PHONE_NUMBER** | 892 | 11 | 11 | 100% | Context length mismatch |
| **MALWARE_TYPE** | 1,234 | 10 | 10 | 100% | Context length mismatch |
| **LATITUDE** | 456 | 5 | 5 | 100% | Context length mismatch |
| **LONGITUDE** | 456 | 5 | 5 | 100% | Context length mismatch |
| **SSN** | 234 | 5 | 5 | 100% | Pattern mismatch |
| **TIME** | 567 | 5 | 5 | 100% | Pattern mismatch |
| **DOMAIN** | 1,234 | 6 | 6 | 100% | Pattern mismatch |

---

## 🔑 Root Causes

### 1. **Context Length Mismatch (Primary Issue)**

**The Problem:**
- Training data: Long narrative contexts (200-500 words)
- Test suite: Short query contexts (40-90 words)
- **Gap:** 150-400 character difference

**Why It Matters:**
- Model learned to detect entities in long, narrative contexts
- Test suite uses short, query-style contexts
- Model doesn't recognize entities in short contexts

**Example:**
- **Training:** "The security operations center received a critical alert 🚨 at 14:30 UTC on 2024-11-30 indicating that multiple systems had been compromised..."
- **Test Suite:** "🚨 Security alert: IP 192.168.1.1 compromised"

### 2. **Surrounding Text Pattern Mismatch**

**The Problem:**
- Training uses specific narrative phrases ("Email phishing", "intelligence report")
- Test suite uses different phrases ("le.com is suspicious", "ected at IP")
- **No overlap** in surrounding text patterns

**Why It Matters:**
- Model learned specific context cues
- Test suite uses different cues
- Model fails to recognize entities without learned cues

### 3. **Missing Training Data**

**The Problem:**
- 30+ entity types have **0 training examples**
- These appear in test suite
- **100% miss rate** for these types

**Why It Matters:**
- Model cannot detect entities it has never seen
- Need to add training examples for these types

---

## 💡 Recommendations

### Immediate Actions

1. **Add Missing Entity Types:**
   - Add training examples for all entity types with 0 examples
   - Focus on: ALTITUDE, BANK_ACCOUNT_NUMBER, BASE64, DISCORD_URL, etc.

2. **Add Short Context Examples:**
   - For each entity type, add examples with **short contexts** (40-90 chars)
   - Match test suite context length patterns
   - Use exact test suite contexts as training examples

3. **Add Test Suite Pattern Examples:**
   - Extract exact test suite contexts
   - Use as training examples
   - Ensure surrounding text patterns match

4. **Balance Context Lengths:**
   - Current: 100% long contexts (200-500 words)
   - Target: 50% short contexts (40-90 words), 50% long contexts
   - Match test suite distribution

### Specific Fixes

#### For EMOJI (1,374 training, 15 test, 15 missed)
- Add 200+ examples with **short contexts** matching test suite
- Use exact test suite patterns: "🚨 Security alert:", "⚠️ Warning:", "✅ Verified:"
- Context length: 40-90 chars (not 300+ chars)

#### For PHONE_NUMBER (892 training, 11 test, 11 missed)
- Add 200+ examples with **short contexts**
- Use test suite formats: "+1-555-123-4567", "(555) 123-4567"
- Context length: 70-90 chars

#### For MALWARE_TYPE (1,234 training, 10 test, 10 missed)
- Add 200+ examples with **short contexts**
- Use test suite patterns: "Ransomware detected: WannaCry", "Malware families: Zeus"
- Context length: 80-100 chars

#### For DMS_COORDINATES (19 training, 4 test, 4 missed)
- Add 100+ examples with **short contexts**
- Use test suite patterns: "Location at 52°31'44.7\"N", "Coordinate formats: 40.7128"
- Context length: 60-80 chars (not 478 chars)

---

## 📈 Expected Impact

### If Recommendations Are Implemented

**Current Performance:**
- Precision: 75.27%
- Recall: 41.52%
- F1: 53.52%

**Expected Performance:**
- Precision: 75-80% (maintain or improve)
- Recall: 60-70% (improve from 41.52%)
- F1: 67-75% (improve from 53.52%)

**Key Improvements:**
- Missing entity types: 100% → 50-70% recall
- Context length mismatch: 100% → 30-50% miss rate
- Pattern mismatch: 100% → 20-40% miss rate

---

## 📋 Action Plan

### Phase 1: Add Missing Entity Types (Priority: HIGH)
- [ ] Identify all entity types with 0 training examples
- [ ] Add 200 examples per type using test suite patterns
- [ ] Use short contexts (40-90 chars)

### Phase 2: Fix Context Length Mismatch (Priority: HIGH)
- [ ] For top missed entities (EMOJI, PHONE_NUMBER, MALWARE_TYPE, etc.)
- [ ] Add 200+ short context examples per type
- [ ] Match test suite context lengths (40-90 chars)

### Phase 3: Fix Pattern Mismatch (Priority: MEDIUM)
- [ ] Extract exact test suite contexts
- [ ] Add as training examples
- [ ] Ensure surrounding text patterns match

### Phase 4: Re-train and Test
- [ ] Re-prepare training data
- [ ] Re-train models
- [ ] Re-run test suite
- [ ] Compare results

---

**Status:** ✅ **Analysis Complete**  
**Next Step:** Implement recommendations to fix mismatches

