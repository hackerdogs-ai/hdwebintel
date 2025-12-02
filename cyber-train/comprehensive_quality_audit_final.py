#!/usr/bin/env python3
"""
COMPREHENSIVE QUALITY AUDIT - PRODUCTION GRADE
Checks:
1. Boundary accuracy (correct start/end positions)
2. Entity type accuracy (valid labels)
3. Whitespace issues
4. Overlapping entities
5. Invalid boundaries
6. Missing obvious entities
7. Intent file accuracy
8. JSON validity
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import defaultdict, Counter
import sys

# Patterns for validation
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?1?[-.\s(]?\(?\d{3}\)?[-.\s)]?\d{3}[-.\s]?\d{4}\b')
IP_PATTERN = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
PERCENTAGE_PATTERN = re.compile(r'\d+%')

# Load valid entity types
VALID_ENTITY_TYPES = set()
with open('cyber-train/entity_types.txt', 'r') as f:
    for line in f:
        if line.strip():
            VALID_ENTITY_TYPES.add(line.strip())

# Load valid intent types
VALID_INTENT_TYPES = set()
intent_file = Path('cyber-train/intent_types.txt')
if intent_file.exists():
    with open(intent_file, 'r') as f:
        for line in f:
            if line.strip():
                VALID_INTENT_TYPES.add(line.strip())

class QualityAuditor:
    def __init__(self):
        self.issues = defaultdict(list)
        self.stats = defaultdict(int)
        
    def check_boundary_accuracy(self, text: str, start: int, end: int, label: str) -> List[str]:
        """Check if boundary is accurate."""
        issues = []
        
        # Check bounds
        if start < 0:
            issues.append(f"INVALID_START: start < 0")
        if end > len(text):
            issues.append(f"INVALID_END: end > text length")
        if start >= end:
            issues.append(f"INVALID_RANGE: start >= end")
        
        if start < 0 or end > len(text) or start >= end:
            return issues
        
        entity_text = text[start:end]
        
        # Check whitespace
        if entity_text != entity_text.strip():
            if entity_text[0].isspace():
                issues.append(f"WHITESPACE_START: leading whitespace")
            if entity_text[-1].isspace():
                issues.append(f"WHITESPACE_END: trailing whitespace")
        
        # Check if entity text matches expected pattern
        if label == 'CVE_ID' and not CVE_PATTERN.fullmatch(entity_text):
            issues.append(f"PATTERN_MISMATCH: '{entity_text}' doesn't match CVE pattern")
        elif label == 'EMAIL_ADDRESS' and not EMAIL_PATTERN.fullmatch(entity_text):
            issues.append(f"PATTERN_MISMATCH: '{entity_text}' doesn't match EMAIL pattern")
        elif label == 'PHONE_NUMBER' and not PHONE_PATTERN.fullmatch(entity_text):
            issues.append(f"PATTERN_MISMATCH: '{entity_text}' doesn't match PHONE pattern")
        elif label == 'IP_ADDRESS' and not IP_PATTERN.fullmatch(entity_text):
            issues.append(f"PATTERN_MISMATCH: '{entity_text}' doesn't match IP pattern")
        elif label == 'URL' and not URL_PATTERN.fullmatch(entity_text):
            issues.append(f"PATTERN_MISMATCH: '{entity_text}' doesn't match URL pattern")
        elif label == 'PERCENTAGE' and not PERCENTAGE_PATTERN.fullmatch(entity_text):
            issues.append(f"PATTERN_MISMATCH: '{entity_text}' doesn't match PERCENTAGE pattern")
        
        return issues
    
    def check_entity_type(self, label: str) -> List[str]:
        """Check if entity type is valid."""
        issues = []
        if label not in VALID_ENTITY_TYPES:
            issues.append(f"INVALID_LABEL: '{label}' not in entity_types.txt")
        return issues
    
    def check_overlaps(self, entities: List[List]) -> List[str]:
        """Check for overlapping entities."""
        issues = []
        for i, (start1, end1, label1) in enumerate(entities):
            for j, (start2, end2, label2) in enumerate(entities[i+1:], i+1):
                if not (end1 <= start2 or start1 >= end2):
                    issues.append(f"OVERLAP: [{start1}:{end1}] {label1} overlaps with [{start2}:{end2}] {label2}")
        return issues
    
    def check_missing_entities(self, text: str, existing_entities: List[List]) -> List[str]:
        """Check for obviously missing entities."""
        missing = []
        existing_spans = set((e[0], e[1]) for e in existing_entities)
        
        # Check for CVE IDs
        for match in CVE_PATTERN.finditer(text):
            span = (match.start(), match.end())
            if span not in existing_spans:
                missing.append(f"MISSING_CVE: '{match.group()}' at [{match.start()}:{match.end()}]")
        
        # Check for email addresses
        for match in EMAIL_PATTERN.finditer(text):
            span = (match.start(), match.end())
            if span not in existing_spans:
                missing.append(f"MISSING_EMAIL: '{match.group()}' at [{match.start()}:{match.end()}]")
        
        # Check for URLs
        for match in URL_PATTERN.finditer(text):
            span = (match.start(), match.end())
            if span not in existing_spans:
                missing.append(f"MISSING_URL: '{match.group()}' at [{match.start()}:{match.end()}]")
        
        return missing
    
    def audit_entity_file(self, file_path: Path) -> Dict:
        """Audit an entity file."""
        results = {
            'file': str(file_path),
            'total_lines': 0,
            'valid_lines': 0,
            'invalid_json': 0,
            'total_entities': 0,
            'valid_entities': 0,
            'boundary_issues': 0,
            'label_issues': 0,
            'whitespace_issues': 0,
            'overlap_issues': 0,
            'missing_entities': 0,
            'empty_entity_lines': 0,
            'issues_by_type': defaultdict(int),
            'issue_details': [],
        }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                
                results['total_lines'] += 1
                
                try:
                    data = json.loads(line)
                except json.JSONDecodeError as e:
                    results['invalid_json'] += 1
                    results['issue_details'].append({
                        'line': line_num,
                        'type': 'INVALID_JSON',
                        'error': str(e)
                    })
                    continue
                
                text = data.get('text', '')
                entities = data.get('entities', [])
                
                if not entities:
                    results['empty_entity_lines'] += 1
                
                results['total_entities'] += len(entities)
                
                # Check each entity
                for start, end, label in entities:
                    # Boundary accuracy
                    boundary_issues = self.check_boundary_accuracy(text, start, end, label)
                    if boundary_issues:
                        results['boundary_issues'] += 1
                        for issue in boundary_issues:
                            results['issues_by_type'][issue] += 1
                            results['issue_details'].append({
                                'line': line_num,
                                'type': issue,
                                'entity': [start, end, label],
                                'text': text[start:end] if 0 <= start < end <= len(text) else 'INVALID',
                                'context': text[max(0, start-20):min(len(text), end+20)]
                            })
                    else:
                        results['valid_entities'] += 1
                    
                    # Label validity
                    label_issues = self.check_entity_type(label)
                    if label_issues:
                        results['label_issues'] += 1
                        for issue in label_issues:
                            results['issues_by_type'][issue] += 1
                
                # Check overlaps
                overlap_issues = self.check_overlaps(entities)
                if overlap_issues:
                    results['overlap_issues'] += len(overlap_issues)
                    for issue in overlap_issues:
                        results['issues_by_type']['OVERLAP'] += 1
                
                # Check whitespace
                for start, end, label in entities:
                    if 0 <= start < end <= len(text):
                        entity_text = text[start:end]
                        if entity_text != entity_text.strip():
                            results['whitespace_issues'] += 1
                            results['issues_by_type']['WHITESPACE'] += 1
                
                # Check missing entities (only for lines with entities)
                if entities:
                    missing = self.check_missing_entities(text, entities)
                    if missing:
                        results['missing_entities'] += len(missing)
                
                results['valid_lines'] += 1
        
        return results
    
    def audit_intent_file(self, file_path: Path) -> Dict:
        """Audit an intent file."""
        results = {
            'file': str(file_path),
            'total_lines': 0,
            'valid_lines': 0,
            'invalid_json': 0,
            'total_intents': 0,
            'valid_intents': 0,
            'invalid_labels': 0,
            'issues_by_type': defaultdict(int),
        }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                
                results['total_lines'] += 1
                
                try:
                    data = json.loads(line)
                except json.JSONDecodeError as e:
                    results['invalid_json'] += 1
                    continue
                
                # Check for 'cats' (spaCy format) or 'intents'
                intents = data.get('cats', {}) or data.get('intents', {})
                
                if not intents:
                    results['issues_by_type']['EMPTY_INTENTS'] += 1
                    continue
                
                for intent_label, value in intents.items():
                    results['total_intents'] += 1
                    if intent_label not in VALID_INTENT_TYPES:
                        results['invalid_labels'] += 1
                        results['issues_by_type']['INVALID_LABEL'] += 1
                    else:
                        results['valid_intents'] += 1
                
                results['valid_lines'] += 1
        
        return results

def main():
    base_dir = Path('cyber-train/entities-intent')
    
    auditor = QualityAuditor()
    
    entity_files = list(base_dir.rglob('*_entities.jsonl'))
    intent_files = list(base_dir.rglob('*_intent.jsonl'))
    
    print("="*80)
    print("COMPREHENSIVE QUALITY AUDIT - PRODUCTION GRADE")
    print("="*80)
    print(f"\nEntity files: {len(entity_files)}")
    print(f"Intent files: {len(intent_files)}\n")
    
    # Audit entity files
    entity_results = []
    for file_path in sorted(entity_files):
        print(f"Auditing: {file_path.name}...", end=' ', flush=True)
        result = auditor.audit_entity_file(file_path)
        entity_results.append(result)
        
        # Calculate accuracy
        if result['total_entities'] > 0:
            accuracy = (result['valid_entities'] / result['total_entities']) * 100
            print(f"✅ {accuracy:.2f}% accuracy ({result['valid_entities']}/{result['total_entities']} entities)")
        else:
            print(f"⚠️  No entities")
    
    # Audit intent files
    intent_results = []
    for file_path in sorted(intent_files):
        print(f"Auditing: {file_path.name}...", end=' ', flush=True)
        result = auditor.audit_intent_file(file_path)
        intent_results.append(result)
        
        if result['total_intents'] > 0:
            accuracy = (result['valid_intents'] / result['total_intents']) * 100
            print(f"✅ {accuracy:.2f}% accuracy ({result['valid_intents']}/{result['total_intents']} intents)")
        else:
            print(f"⚠️  No intents")
    
    # Generate summary report
    print("\n" + "="*80)
    print("SUMMARY REPORT")
    print("="*80)
    
    # Entity files summary
    total_entity_lines = sum(r['total_lines'] for r in entity_results)
    total_entity_entities = sum(r['total_entities'] for r in entity_results)
    total_valid_entities = sum(r['valid_entities'] for r in entity_results)
    total_boundary_issues = sum(r['boundary_issues'] for r in entity_results)
    total_label_issues = sum(r['label_issues'] for r in entity_results)
    total_whitespace_issues = sum(r['whitespace_issues'] for r in entity_results)
    total_overlap_issues = sum(r['overlap_issues'] for r in entity_results)
    total_empty_lines = sum(r['empty_entity_lines'] for r in entity_results)
    total_missing = sum(r['missing_entities'] for r in entity_results)
    
    if total_entity_entities > 0:
        entity_accuracy = (total_valid_entities / total_entity_entities) * 100
    else:
        entity_accuracy = 0.0
    
    print(f"\nENTITY FILES:")
    print(f"  Total files: {len(entity_files)}")
    print(f"  Total lines: {total_entity_lines:,}")
    print(f"  Total entities: {total_entity_entities:,}")
    print(f"  Valid entities: {total_valid_entities:,}")
    print(f"  Overall accuracy: {entity_accuracy:.2f}%")
    print(f"\n  Issues:")
    print(f"    Boundary issues: {total_boundary_issues:,}")
    print(f"    Label issues: {total_label_issues:,}")
    print(f"    Whitespace issues: {total_whitespace_issues:,}")
    print(f"    Overlap issues: {total_overlap_issues:,}")
    print(f"    Empty entity lines: {total_empty_lines:,}")
    print(f"    Missing entities: {total_missing:,}")
    
    # Intent files summary
    total_intent_lines = sum(r['total_lines'] for r in intent_results)
    total_intent_intents = sum(r['total_intents'] for r in intent_results)
    total_valid_intents = sum(r['valid_intents'] for r in intent_results)
    
    if total_intent_intents > 0:
        intent_accuracy = (total_valid_intents / total_intent_intents) * 100
    else:
        intent_accuracy = 0.0
    
    print(f"\nINTENT FILES:")
    print(f"  Total files: {len(intent_files)}")
    print(f"  Total lines: {total_intent_lines:,}")
    print(f"  Total intents: {total_intent_intents:,}")
    print(f"  Valid intents: {total_valid_intents:,}")
    print(f"  Overall accuracy: {intent_accuracy:.2f}%")
    
    # Issue breakdown
    all_issue_types = defaultdict(int)
    for result in entity_results:
        for issue_type, count in result['issues_by_type'].items():
            all_issue_types[issue_type] += count
    
    if all_issue_types:
        print(f"\nISSUE BREAKDOWN:")
        for issue_type, count in sorted(all_issue_types.items(), key=lambda x: x[1], reverse=True)[:20]:
            print(f"  {issue_type:30} {count:6,}")
    
    # Per-file details
    print(f"\n{'='*80}")
    print("PER-FILE DETAILS")
    print("="*80)
    
    for result in sorted(entity_results, key=lambda x: x['boundary_issues'] + x['label_issues'], reverse=True)[:10]:
        if result['total_entities'] > 0:
            accuracy = (result['valid_entities'] / result['total_entities']) * 100
            print(f"\n{Path(result['file']).name}:")
            print(f"  Accuracy: {accuracy:.2f}% ({result['valid_entities']}/{result['total_entities']} entities)")
            print(f"  Issues: {result['boundary_issues']} boundary, {result['label_issues']} label, {result['whitespace_issues']} whitespace")
            print(f"  Empty lines: {result['empty_entity_lines']}")
    
    # Save detailed report
    report = {
        'summary': {
            'entity_files': len(entity_files),
            'intent_files': len(intent_files),
            'total_entity_lines': total_entity_lines,
            'total_entity_entities': total_entity_entities,
            'total_valid_entities': total_valid_entities,
            'overall_entity_accuracy': entity_accuracy,
            'total_intent_lines': total_intent_lines,
            'total_intent_intents': total_intent_intents,
            'total_valid_intents': total_valid_intents,
            'overall_intent_accuracy': intent_accuracy,
            'total_boundary_issues': total_boundary_issues,
            'total_label_issues': total_label_issues,
            'total_whitespace_issues': total_whitespace_issues,
            'total_overlap_issues': total_overlap_issues,
            'total_empty_lines': total_empty_lines,
            'total_missing_entities': total_missing,
        },
        'entity_files': entity_results,
        'intent_files': intent_results,
        'issue_breakdown': dict(all_issue_types),
    }
    
    with open('cyber-train/COMPREHENSIVE_QUALITY_AUDIT_FINAL.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n✅ Detailed report saved to: cyber-train/COMPREHENSIVE_QUALITY_AUDIT_FINAL.json")

if __name__ == '__main__':
    main()

