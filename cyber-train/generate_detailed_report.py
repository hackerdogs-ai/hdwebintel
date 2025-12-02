#!/usr/bin/env python3
"""
Generate detailed markdown report from audit results.
"""

import json
from pathlib import Path

with open('cyber-train/COMPREHENSIVE_QUALITY_AUDIT_FINAL.json', 'r') as f:
    report = json.load(f)

summary = report['summary']

# Generate markdown report
md_report = f"""# Comprehensive Quality Audit Report - Production Grade

## Executive Summary

### Entity Files
- **Total Files**: {summary['entity_files']}
- **Total Examples**: {summary['total_entity_lines']:,}
- **Total Entities**: {summary['total_entity_entities']:,}
- **Valid Entities**: {summary['total_valid_entities']:,}
- **Overall Accuracy**: {summary['overall_entity_accuracy']:.2f}%

### Intent Files
- **Total Files**: {summary['intent_files']}
- **Total Examples**: {summary['total_intent_lines']:,}
- **Total Intents**: {summary['total_intent_intents']:,}
- **Valid Intents**: {summary['total_valid_intents']:,}
- **Overall Accuracy**: {summary['overall_intent_accuracy']:.2f}%

## Issue Summary

### Entity Issues
- **Boundary Issues**: {summary['total_boundary_issues']:,}
- **Label Issues**: {summary['total_label_issues']:,}
- **Whitespace Issues**: {summary['total_whitespace_issues']:,}
- **Overlap Issues**: {summary['total_overlap_issues']:,}
- **Empty Entity Lines**: {summary['total_empty_lines']:,}
- **Missing Entities**: {summary['total_missing_entities']:,}

## Per-File Entity Accuracy

| File | Accuracy | Valid Entities | Total Entities | Boundary Issues | Label Issues | Whitespace Issues |
|------|----------|----------------|----------------|-----------------|--------------|-------------------|
"""

# Add per-file details
for result in sorted(report['entity_files'], key=lambda x: (x['valid_entities'] / x['total_entities'] if x['total_entities'] > 0 else 0)):
    file_name = Path(result['file']).name
    if result['total_entities'] > 0:
        accuracy = (result['valid_entities'] / result['total_entities']) * 100
    else:
        accuracy = 0.0
    
    md_report += f"| {file_name} | {accuracy:.2f}% | {result['valid_entities']:,} | {result['total_entities']:,} | {result['boundary_issues']} | {result['label_issues']} | {result['whitespace_issues']} |\n"

md_report += f"""
## Per-File Intent Accuracy

| File | Accuracy | Valid Intents | Total Intents | Invalid Labels |
|------|----------|---------------|---------------|----------------|
"""

for result in sorted(report['intent_files'], key=lambda x: (x['valid_intents'] / x['total_intents'] if x['total_intents'] > 0 else 0)):
    file_name = Path(result['file']).name
    if result['total_intents'] > 0:
        accuracy = (result['valid_intents'] / result['total_intents']) * 100
    else:
        accuracy = 0.0
    
    md_report += f"| {file_name} | {accuracy:.2f}% | {result['valid_intents']:,} | {result['total_intents']:,} | {result['invalid_labels']} |\n"

md_report += f"""
## Issue Breakdown

### Top 20 Issue Types

| Issue Type | Count |
|------------|-------|
"""

issue_breakdown = report.get('issue_breakdown', {})
for issue_type, count in sorted(issue_breakdown.items(), key=lambda x: x[1], reverse=True)[:20]:
    md_report += f"| {issue_type} | {count:,} |\n"

md_report += f"""
## Files Requiring Attention

### Lowest Accuracy Entity Files

"""

lowest_accuracy = sorted(report['entity_files'], 
                        key=lambda x: (x['valid_entities'] / x['total_entities'] if x['total_entities'] > 0 else 0))[:10]

for result in lowest_accuracy:
    file_name = Path(result['file']).name
    if result['total_entities'] > 0:
        accuracy = (result['valid_entities'] / result['total_entities']) * 100
    else:
        accuracy = 0.0
    
    md_report += f"#### {file_name}\n"
    md_report += f"- **Accuracy**: {accuracy:.2f}%\n"
    md_report += f"- **Valid Entities**: {result['valid_entities']:,} / {result['total_entities']:,}\n"
    md_report += f"- **Boundary Issues**: {result['boundary_issues']}\n"
    md_report += f"- **Label Issues**: {result['label_issues']}\n"
    md_report += f"- **Whitespace Issues**: {result['whitespace_issues']}\n"
    md_report += f"- **Overlap Issues**: {result['overlap_issues']}\n"
    md_report += f"- **Empty Lines**: {result['empty_entity_lines']}\n\n"

md_report += f"""
## Recommendations

1. **Overlap Issues**: {summary['total_overlap_issues']:,} overlapping entities need resolution
2. **Boundary Issues**: {summary['total_boundary_issues']:,} boundary corrections needed
3. **Whitespace Issues**: {summary['total_whitespace_issues']:,} whitespace trimming needed
4. **Empty Lines**: {summary['total_empty_lines']:,} lines with no entities (may be intentional negative examples)
5. **Pattern Mismatches**: Dates incorrectly labeled as PHONE_NUMBER need correction

## Quality Metrics

- **Entity Accuracy**: {summary['overall_entity_accuracy']:.2f}% ✅
- **Intent Accuracy**: {summary['overall_intent_accuracy']:.2f}% ✅
- **Production Ready**: {'Yes' if summary['overall_entity_accuracy'] >= 95 and summary['overall_intent_accuracy'] >= 95 else 'Needs Improvement'}
"""

with open('cyber-train/COMPREHENSIVE_QUALITY_AUDIT_REPORT.md', 'w') as f:
    f.write(md_report)

print("✅ Detailed report generated: cyber-train/COMPREHENSIVE_QUALITY_AUDIT_REPORT.md")

