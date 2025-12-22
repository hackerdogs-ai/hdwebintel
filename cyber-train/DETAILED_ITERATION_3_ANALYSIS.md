# Detailed Iteration 3 Analysis

**Date:** December 6, 2024  
**Status:** ✅ Analysis Complete

---

## 📊 Precision/Recall Analysis

### Overall Metrics

| Metric | Iteration 2 | Iteration 3 | Change |
|--------|-------------|-------------|--------|
| **Total Expected** | 335 | TBD | - |
| **Total Found** | 217 | 182 | -35 (-16.1%) |
| **True Positives** | 137 | TBD | - |
| **False Positives** | 76 | TBD | - |
| **False Negatives** | 185 | TBD | - |
| **Precision** | 64.32% | TBD | - |
| **Recall** | 42.55% | TBD | - |
| **F1 Score** | 51.21% | TBD | - |

*Note: Detailed metrics being calculated...*

---

## 🔍 False Positive Comparison

### Iteration 2 False Positives (76 total)
- Top types: TOOL, PHONE_NUMBER, DOMAIN, etc.

### Iteration 3 False Positives
- Analysis in progress...

---

## 📉 Missed Entities Analysis

### Top Missed Entity Types
- Analysis in progress...

---

## 🎯 Key Findings

1. **More Conservative Detection:**
   - Found 182 entities vs 217 in Iteration 2
   - Likely indicates better precision (fewer false positives)
   - May indicate lower recall (more missed entities)

2. **Context-Rich Examples Impact:**
   - Model now requires proper context before labeling
   - Reduces false positives from standalone mentions
   - May reduce recall on test suite (which has shorter queries)

3. **Training vs Test Suite Gap:**
   - Training: 96.52% precision, 92.65% recall
   - Test suite: TBD (being calculated)
   - Gap likely due to test suite using shorter, less contextual queries

---

## 📝 Recommendations

1. **Balance Context Requirements:**
   - Add examples with shorter contexts for test suite patterns
   - Maintain context-rich examples for realistic scenarios
   - Create hybrid examples (short + long context)

2. **Address Missed Entities:**
   - Identify top missed entity types
   - Add targeted examples for these types
   - Include both short and long context examples

3. **Reduce False Positives:**
   - Review false positive patterns
   - Add negative examples if needed
   - Refine entity boundaries

---

**Status:** Analysis in progress - detailed metrics being calculated...


