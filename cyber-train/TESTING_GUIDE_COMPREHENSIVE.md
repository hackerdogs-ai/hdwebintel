# 🧪 Comprehensive Testing Guide

This guide covers testing the trained models with multiple types of inputs.

## 🚀 Quick Start

### Run Comprehensive Test Suite

```bash
# Run all test types automatically
python3 cyber-train/comprehensive_test_suite.py --comprehensive
```

This will test:
- Natural language queries
- Technical queries
- Casual/informal queries
- Multi-entity queries
- OSINT queries
- Cybersecurity queries
- Complex/compound queries
- Edge cases
- Question format
- Command format
- And more...

### Interactive Testing

```bash
# Test queries interactively
python3 cyber-train/comprehensive_test_suite.py --interactive
```

Then type your queries and see results in real-time.

### Test Single Query

```bash
# Test a specific query
python3 cyber-train/comprehensive_test_suite.py --text "Check IP 192.168.1.1 for threats"
```

### Custom Test File

```bash
# Test from custom JSON file
python3 cyber-train/comprehensive_test_suite.py --custom test_inputs_examples.json
```

---

## 📊 Test Categories

### 1. Natural Language Queries
- Conversational style
- User-friendly language
- Example: "Can you help me investigate this suspicious IP address?"

### 2. Technical Queries
- Professional/technical language
- Specific terminology
- Example: "APT41 CVE-2021-44228 Log4j vulnerability exploitation detected"

### 3. Casual/Informal Queries
- Slang, abbreviations
- Informal tone
- Example: "hey what's up with that malware thing?"

### 4. Multi-Entity Queries
- Multiple entities in one query
- Complex relationships
- Example: "APT28 used WannaCry to attack IP 172.16.0.1 and domain evil.com"

### 5. OSINT Queries
- Open source intelligence
- Social media, geolocation
- Example: "Verify image authenticity and check GPS coordinates"

### 6. Cybersecurity Queries
- Security operations
- Incident response
- Example: "Execute incident response playbook for ransomware"

### 7. Complex/Compound Queries
- Multiple intents
- Long sentences
- Example: "Investigate breach, analyze malware, generate report"

### 8. Edge Cases
- Very short queries
- Very long queries
- Special characters
- Formatted data

### 9. Question Format
- Questions starting with "What", "How", "Why"
- Example: "What is the threat level for IP 203.0.113.0?"

### 10. Command Format
- Imperative statements
- Direct commands
- Example: "Block IP 192.168.1.50 and isolate host"

---

## 📝 Creating Custom Test Files

Create a JSON file with your test cases:

```json
[
  {
    "text": "Your test query here",
    "category": "your_category",
    "expected_entities": [
      ["entity_text", "ENTITY_TYPE"]
    ],
    "expected_intents": ["INTENT1", "INTENT2"]
  }
]
```

Then run:
```bash
python3 cyber-train/comprehensive_test_suite.py --custom your_test_file.json
```

---

## 📊 Understanding Results

### Entity Results
- **Entity Text**: The extracted text
- **Entity Label**: The predicted entity type
- **Count**: Number of entities found

### Intent Results
- **Intent Name**: The predicted intent
- **Score**: Confidence score (0.0 to 1.0)
- **Percentage**: Confidence as percentage
- Only intents with score > 0.3 are shown

### Expected vs Actual
- ✅ Green checkmark: Matches expected
- ⚠️ Yellow warning: Doesn't match expected

---

## 🎯 Test Scenarios

### Scenario 1: Basic Entity Extraction
```bash
python3 cyber-train/comprehensive_test_suite.py --text "IP address 192.168.1.1 is suspicious"
```

**Expected:**
- Entity: `192.168.1.1` → `IP_ADDRESS`
- Intent: `INVESTIGATE` or `DETECT`

### Scenario 2: Multiple Entities
```bash
python3 cyber-train/comprehensive_test_suite.py --text "APT41 attacked domain example.com on port 443"
```

**Expected:**
- Entities: `APT41` (THREAT_ACTOR), `example.com` (DOMAIN), `443` (PORT)
- Intents: `INVESTIGATE`, `DETECT`

### Scenario 3: OSINT Query
```bash
python3 cyber-train/comprehensive_test_suite.py --text "Verify social media account @user123 on Twitter"
```

**Expected:**
- Entity: `@user123` (USERNAME)
- Intents: `VERIFY`, `VALIDATE`

### Scenario 4: Complex Query
```bash
python3 cyber-train/comprehensive_test_suite.py --text "I need to investigate the breach, analyze the malware, generate a report, and ensure compliance"
```

**Expected:**
- Multiple intents: `INVESTIGATE`, `ANALYZE`, `GENERATE_REPORTS`, `ENSURE_COMPLIANCE`

---

## 📈 Performance Metrics

After running comprehensive tests, you'll get:

1. **Summary Statistics**
   - Total test cases
   - Total entities found
   - Total intents found
   - Averages per query

2. **Performance by Category**
   - How well each category performs
   - Entity/intent counts per category

3. **Results File**
   - JSON file with all results
   - Can be analyzed further
   - Saved as `comprehensive_test_results.json`

---

## 🔍 Analyzing Results

### View Results File
```bash
cat comprehensive_test_results.json | python3 -m json.tool | less
```

### Extract Specific Information
```python
import json

with open('comprehensive_test_results.json') as f:
    results = json.load(f)

# Find queries with no entities
no_entities = [r for r in results['test_cases'] if r['entity_count'] == 0]

# Find queries with many entities
many_entities = [r for r in results['test_cases'] if r['entity_count'] > 5]

# Find queries by category
osint_queries = [r for r in results['test_cases'] if 'osint' in r['category']]
```

---

## 🎨 Example Test Cases

See `test_inputs_examples.json` for example test cases covering:
- Email security
- Network analysis
- Cloud security
- Threat intelligence
- OSINT verification
- API security
- Compliance reporting
- Blockchain OSINT
- Forensics
- Threat response

---

## 💡 Tips

1. **Start with comprehensive tests** to see overall performance
2. **Use interactive mode** for quick ad-hoc testing
3. **Create custom test files** for domain-specific scenarios
4. **Review results file** for detailed analysis
5. **Compare expected vs actual** to identify issues

---

## 🚨 Troubleshooting

### Models Not Loading
```bash
# Check if models exist
ls -la cyber-train/models/*/model-best/

# Verify model paths
python3 cyber-train/comprehensive_test_suite.py --ner-model <path> --intent-model <path>
```

### No Results
- Check if models are loaded successfully
- Verify input text is not empty
- Check for errors in console output

### Unexpected Results
- Review entity types in `entity_types.txt`
- Review intent types in `intent_types.txt`
- Check if query matches training data style
- Consider adding more training examples

---

## 📋 Next Steps

1. Run comprehensive test suite
2. Review results and identify edge cases
3. Add more training data for weak areas
4. Retrain models
5. Re-test and iterate

---

**Happy Testing!** 🎉

