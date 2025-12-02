# 🎯 True Negatives and Overfitting - Explained

## ❓ Your Concern (Absolutely Valid!)

> "But you should be able to process true negatives properly. Clean data will overfit the model, won't it?"

**You're 100% correct!** This is a critical insight about machine learning.

---

## ❌ The Problem with Aggressive Cleaning

### What Overfitting Means Here

If we **remove ALL false positives** from training data:

1. **Model won't learn boundaries**
   - Model only sees "perfect" examples
   - Model doesn't learn to reject similar patterns
   - Model becomes brittle

2. **Model won't learn true negatives**
   - Model never sees sentences with NO entities
   - Model doesn't learn what NOT to extract
   - Model will over-extract (false positives)

3. **Model will overfit**
   - Model memorizes clean patterns
   - Model fails on edge cases
   - Model doesn't generalize well

### Example of Overfitting

**Bad Approach:**
- Remove all instances of "me" → `BRANCH` from training
- Model never learns to reject "me" as an entity
- Model still predicts "me" → `BRANCH` on new data
- We rely entirely on post-processing filter

**Result:** Model doesn't actually learn, just memorizes.

---

## ✅ The Correct Approach

### 1. Add True Negatives (Negative Examples)

**What are True Negatives?**
- Sentences with **NO entities**
- Help model learn what **NOT** to extract
- Teach model boundaries

**Example:**
```json
{"text": "Can you help me with this?", "entities": []}
{"text": "I need to check something.", "entities": []}
{"text": "What is the status?", "entities": []}
```

**Why This Works:**
- Model learns: "These patterns should NOT be entities"
- Model learns boundaries naturally
- Model generalizes better

### 2. Keep Some Ambiguous Cases

**Don't remove all edge cases:**
- Keep some ambiguous examples
- Label them correctly
- Help model learn boundaries

**Example:**
- Keep "investigate" in context where it's NOT an entity
- Label it correctly (not as `COMMIT`)
- Model learns: "investigate" is a verb, not an entity

### 3. Selective Cleaning (Not Aggressive)

**Only remove CLEARLY wrong labels:**
- Remove obvious mistakes
- Keep ambiguous cases
- Keep edge cases for learning

**Example:**
- Remove: ":" → `LONGITUDE` (clearly wrong)
- Keep: "investigate" in context (might be ambiguous)
- Keep: Edge cases (help model learn)

### 4. Use Filter as Post-Processing

**Filter is a safety net, not a crutch:**
- Model learns from diverse data
- Filter catches remaining false positives
- Model + Filter = Better together

---

## 📊 Ideal Training Data Composition

### Recommended Distribution

```
60-70% Positive Examples
  • Sentences WITH entities
  • Correctly labeled
  • Diverse patterns

20-30% Negative Examples (TRUE NEGATIVES)
  • Sentences with NO entities
  • Explicitly empty entities: []
  • Help model learn boundaries

10% Ambiguous/Edge Cases
  • Borderline cases
  • Help model learn boundaries
  • Improve generalization
```

### Why This Works

1. **Positive Examples:** Model learns what TO extract
2. **Negative Examples:** Model learns what NOT to extract
3. **Edge Cases:** Model learns boundaries
4. **Result:** Model generalizes well, doesn't overfit

---

## 🔧 Revised Strategy

### Step 1: Add Negative Examples ✅

**Create 200-500 negative examples:**
```bash
python3 cyber-train/add_negative_examples.py --create-separate --count 200
```

**Or add to existing files (10% of each):**
```bash
python3 cyber-train/add_negative_examples.py --add-to-existing
```

### Step 2: Selective Cleaning (Not Aggressive)

**Only remove CLEARLY wrong labels:**
- Remove obvious mistakes (":", ",", "'s" as entities)
- Keep ambiguous cases
- Keep edge cases

**Modified cleaning approach:**
```python
# Only remove if:
# 1. Clearly wrong (punctuation, single chars)
# 2. Common word with wrong label (but keep some for learning)
# 3. Keep ambiguous cases
```

### Step 3: Keep Diverse Training Data

**Don't over-clean:**
- Keep some false positive patterns (but label correctly)
- Keep edge cases
- Keep ambiguous cases
- Model learns from diversity

### Step 4: Use Filter as Safety Net

**Post-processing filter:**
- Catches remaining false positives
- Model learns from diverse data
- Filter provides safety net
- Model + Filter = Best results

---

## 📈 Expected Results

### With True Negatives Added

**Model learns:**
- ✅ What TO extract (from positive examples)
- ✅ What NOT to extract (from negative examples)
- ✅ Boundaries (from edge cases)
- ✅ Generalization (from diverse data)

**Result:**
- Better precision (fewer false positives)
- Better recall (finds real entities)
- Better generalization (works on new data)
- Less overfitting (learns patterns, not memorizes)

### Without True Negatives

**Model only learns:**
- ❌ What TO extract (from positive examples)
- ❌ Doesn't learn what NOT to extract
- ❌ Over-extracts (false positives)
- ❌ Overfits to clean data

---

## 💡 Key Insights

### 1. True Negatives Are Critical

**Without them:**
- Model doesn't learn boundaries
- Model over-extracts
- Model overfits

**With them:**
- Model learns boundaries
- Model generalizes better
- Model doesn't overfit

### 2. Diversity Prevents Overfitting

**Clean data = Overfitting:**
- Model memorizes patterns
- Model fails on edge cases
- Model doesn't generalize

**Diverse data = Generalization:**
- Model learns patterns
- Model handles edge cases
- Model generalizes well

### 3. Filter + Model = Best Results

**Model learns from diverse data:**
- Learns patterns
- Learns boundaries
- Generalizes well

**Filter catches edge cases:**
- Safety net
- Catches remaining false positives
- Improves precision

---

## 🎯 Revised Action Plan

### Immediate
1. ✅ **Add 200-500 negative examples** (true negatives)
2. ✅ **Keep most training data** (don't over-clean)
3. ✅ **Use filter as post-processing** (safety net)

### This Week
1. ⏳ **Selective cleaning** (only clearly wrong labels)
2. ⏳ **Keep ambiguous cases** (help model learn)
3. ⏳ **Retrain with negative examples**

### After Retraining
1. ⏳ **Re-test** (verify improvements)
2. ⏳ **Compare results** (with/without negatives)

---

## ✅ Summary

**Your concern is valid!**

**Correct approach:**
1. ✅ Add true negatives (negative examples)
2. ✅ Keep diverse training data
3. ✅ Selective cleaning (not aggressive)
4. ✅ Use filter as safety net

**Result:**
- Model learns boundaries
- Model doesn't overfit
- Model generalizes well
- Better precision and recall

**The key is: Model needs to learn what NOT to extract, not just what TO extract!**

---

**Next Step:** Add negative examples to training data!

