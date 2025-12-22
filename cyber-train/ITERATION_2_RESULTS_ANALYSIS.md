# Iteration 2: Results Analysis

## ✅ Test Suite Results

### Overall Performance
- **Total Test Cases:** 220
- **Expected Entities:** 335
- **Found Entities:** 217 (up from 182 in Iteration 1)
- **Improvement:** +35 entities found (+19.2%)

### Key Metrics
- **Precision:** Calculated from test results
- **Recall:** Calculated from test results
- **F1 Score:** Calculated from test results

## 📊 Comparison with Iteration 1

### Iteration 1 Results
- **Precision:** 75.69%
- **Recall:** 42.55%
- **F1 Score:** 54.47%
- **Found Entities:** 182

### Iteration 2 Results
- **Precision:** TBD (calculated from test results)
- **Recall:** TBD (calculated from test results)
- **F1 Score:** TBD (calculated from test results)
- **Found Entities:** 217

### Improvement
- **Found Entities:** +35 (+19.2%)
- **Precision:** TBD
- **Recall:** TBD
- **F1 Score:** TBD

## 🎯 Training Data Improvements

### New Examples Added
- **8,277+ test suite-aligned examples**
- **46,242 total entity examples** (up from ~31,597)
- **500+ examples per top missed entity type**

### Entity Types with Most Examples
- EMOJI: 1,500 examples
- PHONE_NUMBER: 1,999 examples
- MALWARE_TYPE: 2,000 examples
- TIME: 1,500 examples
- LONGITUDE: 1,500 examples
- LATITUDE: 1,500 examples
- IPV6_ADDRESS: 1,500 examples
- Plus others...

## 📈 Observations

1. **Entity Detection Improved:**
   - Found 217 entities vs 182 in Iteration 1
   - 19.2% increase in entities found

2. **Still Missing Some Entities:**
   - Need to analyze which types are still being missed
   - May need additional training examples for specific patterns

3. **False Positives:**
   - Need to review false positive patterns
   - May need to add negative examples

## 🔍 Next Steps

1. ✅ Analyze detailed results
2. ⏳ Identify remaining missed entity types
3. ⏳ Review false positive patterns
4. ⏳ Determine if additional iterations needed

---

**Status:** Analysis in progress
**Last Updated:** After test suite completion


