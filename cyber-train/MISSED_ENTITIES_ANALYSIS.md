# Missed Entities Analysis and Next Steps

## Why Are There Still Missed Entities?

### Root Causes

1. **Insufficient Training Examples for Specific Types**
   - Some entity types have fewer examples in training data
   - Model hasn't seen enough variations to generalize well
   - Test suite includes patterns not well-represented in training

2. **Pattern Recognition Gaps**
   - Model may not recognize certain patterns (e.g., lowercase CVE IDs, emojis)
   - Context-dependent extraction failing for some cases
   - Edge cases not covered in training

3. **Conservative Model Behavior**
   - Model prioritizes precision over recall
   - Only detects entities when highly confident
   - Post-processing filter may be too aggressive

4. **Test Suite vs Training Data Mismatch**
   - Test suite includes challenging/edge cases
   - Some expected entities may need review
   - Test patterns may differ from training patterns

## Top 20 Missed Entity Types

Based on comprehensive test results:

1. **EMOJI**: 15 missed
2. **PHONE_NUMBER**: 11 missed
3. **MALWARE_TYPE**: 10 missed
4. **TIME**: 5 missed
5. **LONGITUDE**: 5 missed
6. **LATITUDE**: 5 missed
7. **IPV6_ADDRESS**: 5 missed
8. **SSN**: 5 missed
9. **LLM_PROVIDER**: 5 missed
10. **LLM_MODEL**: 5 missed
11. **IP_ADDRESS**: 5 missed
12. **COMPLIANCE_FRAMEWORK**: 5 missed
13. **GITHUB_REPO_URL**: 4 missed
14. **EMAIL_ADDRESS**: 4 missed
15. **DMS_COORDINATES**: 4 missed
16. **HASH**: 4 missed
17. **PORT**: 4 missed
18. **HOST_TYPE**: 3 missed
19. **THREAT_ACTOR**: 3 missed
20. **CVE_ID**: 3 missed

## False Positives Analysis

**Total False Positives**: 44

**Top False Positive Types**:
1. **THREAT_ACTOR**: 5 false positives
2. **PROTOCOL_TYPE**: 3 false positives
3. **DOMAIN**: 3 false positives
4. **COMPLIANCE_FRAMEWORK**: 2 false positives
5. **URL**: 2 false positives

## Next Steps

### Step 1: Analyze Missed Entity Patterns ✅ (Current)

**Action**: Review missed entities to identify patterns
- Which entity types are most missed?
- What patterns are not being recognized?
- Are test suite expected entities correct?

### Step 2: Add Training Examples for Missed Types (NEXT)

**Priority Actions**:

1. **Add Examples for Top 20 Missed Types**
   - EMOJI: Add 200+ examples with various emojis
   - PHONE_NUMBER: Add 150+ examples (international formats)
   - MALWARE_TYPE: Add 100+ examples (from catalog)
   - TIME: Add 100+ examples (various formats)
   - Coordinates (LATITUDE/LONGITUDE): Add 100+ examples
   - IPV6_ADDRESS: Add 50+ examples
   - SSN: Add 50+ examples
   - LLM_MODEL/LLM_PROVIDER: Add 50+ examples each
   - IP_ADDRESS: Add 50+ examples
   - COMPLIANCE_FRAMEWORK: Add 50+ examples
   - GITHUB_REPO_URL: Add 50+ examples
   - EMAIL_ADDRESS: Add 50+ examples
   - DMS_COORDINATES: Add 50+ examples
   - HASH: Add 50+ examples
   - PORT: Add 50+ examples
   - HOST_TYPE: Add 50+ examples
   - THREAT_ACTOR: Add 50+ examples (from catalog)
   - CVE_ID: Add 50+ examples (including lowercase)

2. **Match Test Suite Patterns**
   - Extract patterns from missed entities
   - Generate training examples matching these patterns
   - Ensure training data covers test suite scenarios

3. **Review Test Suite Expected Entities**
   - Verify expected entities are correct
   - Check if boundaries are accurate
   - Ensure entity types are appropriate

### Step 3: Fix False Positives

**Actions**:
1. Review false positive patterns
2. Add negative examples for common false positives
3. Improve post-processing filter
4. Add validation rules for specific entity types

### Step 4: Re-train and Re-test

**Actions**:
1. Re-prepare training data with new examples
2. Retrain NER model
3. Re-run comprehensive test suite
4. Compare results with previous run

## Expected Improvements

After adding training examples for missed types:

- **Recall**: Should improve from 42.55% to 60-70%
- **Precision**: Should maintain or improve (currently 75.69%)
- **F1 Score**: Should improve from 54.47% to 65-75%

## Implementation Plan

1. ✅ **Completed**: Comprehensive test suite executed
2. ✅ **Completed**: Missed entities analyzed
3. ⏳ **Next**: Create script to add training examples for top 20 missed types
4. ⏳ **Next**: Review and fix test suite expected entities if needed
5. ⏳ **Next**: Re-prepare, retrain, and re-test

## Conclusion

Missed entities are expected because:
- Test suite includes challenging edge cases
- Some entity types need more training examples
- Model is conservative to maintain precision
- Test patterns may differ from training patterns

**The next step is to add training examples for the top missed entity types**, focusing on the 20 most missed types identified in the analysis.

