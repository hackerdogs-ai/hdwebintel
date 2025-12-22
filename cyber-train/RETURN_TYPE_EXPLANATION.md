# Return Type Explanation: `classify_intents`

## Function Analysis

```python
def classify_intents(self, text, threshold=0.3):
    if self.intent_model is None:
        raise RuntimeError("Intent model not loaded")
    doc = self.intent_model(text)
    intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
    return [(intent, score) for intent, score in intents if score >= threshold]
```

---

## Return Type

**Type:** `List[Tuple[str, float]]`

- **List** of tuples
- Each tuple contains:
  - **`str`**: Intent label (e.g., "INVESTIGATE", "DETECT")
  - **`float`**: Confidence score (0.0 to 1.0)

---

## Step-by-Step Breakdown

### 1. `doc.cats.items()`
```python
# Returns: dict_items([('INVESTIGATE', 0.9980), ('DETECT', 0.8486), ...])
# Type: dict_items (view of key-value pairs)
```

### 2. `sorted(..., key=lambda x: x[1], reverse=True)`
```python
# Sorts by score (x[1]) in descending order
# Returns: [('INVESTIGATE', 0.9980), ('DETECT', 0.8486), ...]
# Type: List[Tuple[str, float]]
```

### 3. List Comprehension with Filter
```python
# Filters by threshold and returns list of tuples
# Returns: [('INVESTIGATE', 0.9980), ('DETECT', 0.8486), ...]
# Type: List[Tuple[str, float]]
```

---

## Example Output

### Input:
```python
text = "Check IP 192.168.1.1"
threshold = 0.3
```

### Output:
```python
[
    ('INVESTIGATE', 0.9980),
    ('DETECT', 0.8486),
    ('INVESTIGATE_THREATS', 0.8208),
    ('CONTAIN_THREAT', 0.7948),
    ('MAINTAIN_SYSTEMS', 0.7614)
]
```

**Type:** `List[Tuple[str, float]]`

---

## Type Hints (Recommended)

### With Type Hints:
```python
from typing import List, Tuple

def classify_intents(self, text: str, threshold: float = 0.3) -> List[Tuple[str, float]]:
    if self.intent_model is None:
        raise RuntimeError("Intent model not loaded")
    doc = self.intent_model(text)
    intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
    return [(intent, score) for intent, score in intents if score >= threshold]
```

### Usage Example:
```python
# Type: List[Tuple[str, float]]
results = nlp.classify_intents("Check IP 192.168.1.1", threshold=0.3)

# Access individual results
for intent, score in results:
    print(f"{intent}: {score:.4f} ({score*100:.1f}%)")

# Or unpack
top_intent, top_score = results[0] if results else (None, 0.0)
```

---

## Data Structure Details

### Each Tuple:
```python
(intent: str, score: float)
```

- **`intent`**: String label like "INVESTIGATE", "DETECT", "ANALYZE"
- **`score`**: Float between 0.0 and 1.0 (confidence score)

### List Properties:
- **Ordered**: Sorted by score (highest first)
- **Filtered**: Only includes scores >= threshold
- **Empty**: Returns `[]` if no intents meet threshold

---

## Example: Accessing Results

```python
# Get results
intents = nlp.classify_intents("Check IP 192.168.1.1", threshold=0.3)

# Type checking
from typing import List, Tuple
assert isinstance(intents, List)
assert all(isinstance(item, Tuple) and len(item) == 2 for item in intents)

# Access first intent
if intents:
    top_intent, top_score = intents[0]
    print(f"Top intent: {top_intent} ({top_score:.4f})")

# Iterate all
for intent, score in intents:
    print(f"{intent}: {score:.4f}")

# Convert to dictionary
intent_dict = dict(intents)
# Result: {'INVESTIGATE': 0.9980, 'DETECT': 0.8486, ...}

# Get just the labels
labels = [intent for intent, score in intents]
# Result: ['INVESTIGATE', 'DETECT', ...]

# Get just the scores
scores = [score for intent, score in intents]
# Result: [0.9980, 0.8486, ...]
```

---

## Comparison with Similar Functions

### `extract_entities()` returns:
```python
List[Tuple[str, str]]  # (entity_text, label)
# Example: [('192.168.1.1', 'IP_ADDRESS'), ('evil.com', 'DOMAIN')]
```

### `classify_intents()` returns:
```python
List[Tuple[str, float]]  # (intent, score)
# Example: [('INVESTIGATE', 0.9980), ('DETECT', 0.8486)]
```

**Difference:** Second element is `str` (label) vs `float` (score)

---

## Summary

| Aspect | Value |
|--------|-------|
| **Return Type** | `List[Tuple[str, float]]` |
| **List Elements** | Tuples of (intent_label, confidence_score) |
| **Intent Label** | `str` (e.g., "INVESTIGATE") |
| **Score** | `float` (0.0 to 1.0) |
| **Ordering** | Descending by score |
| **Filtering** | Only scores >= threshold |
| **Empty Case** | Returns `[]` if no matches |

---

**Answer:** The function returns `List[Tuple[str, float]]` - a list of tuples where each tuple contains an intent label (string) and its confidence score (float).

