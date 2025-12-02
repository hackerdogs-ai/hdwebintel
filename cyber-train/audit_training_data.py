#!/usr/bin/env python3
"""
Comprehensive audit of training data for missed and misclassified entities.
Checks boundaries and reports accuracy per file.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple

# Critical entity types that were missed in tests
CRITICAL_ENTITY_TYPES = {
    'IP_ADDRESS', 'DOMAIN', 'CVE_ID', 'EMAIL', 'EMAIL_ADDRESS',
    'THREAT_ACTOR', 'LATITUDE', 'LONGITUDE', 'WALLET_ADDRESS',
    'PHONE_NUMBER', 'PERSON', 'ORGANIZATION', 'LOCATION'
}

# Patterns for validation
IP_PATTERN = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?[\d\s\-\(\)]{10,}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
# More specific patterns for lat/long (avoid matching random numbers)
LATITUDE_PATTERN = re.compile(r'\b-?([0-8]?[0-9]|90)(\.\d+)?\s*(degrees?|°|lat|latitude)\b', re.IGNORECASE)
LONGITUDE_PATTERN = re.compile(r'\b-?([0-9]?[0-9]?[0-9]|1[0-7][0-9]|180)(\.\d+)?\s*(degrees?|°|lon|lng|longitude)\b', re.IGNORECASE)
# Also match coordinate pairs: "40.7128, -74.0060" or "lat 40.7128 lon -74.0060"
COORDINATE_PAIR_PATTERN = re.compile(r'\b(-?[0-8]?[0-9](?:\.[0-9]+)?|90(?:\.0+)?)\s*[,;]\s*(-?(?:[0-9]?[0-9]?[0-9](?:\.[0-9]+)?|1[0-7][0-9](?:\.[0-9]+)?|180(?:\.0+)?))\b')

# Misclassified patterns (wrong labels that should be critical types)
MISCLASSIFIED_PATTERNS = {
    'IP_ADDRESS': ['REGULATION', 'TYPE', 'TOOL', 'FRAMEWORK'],
    'DOMAIN': ['FRAMEWORK', 'TOOL', 'PLATFORM'],
    'CVE_ID': ['VULNERABILITY_TYPE', 'VULNERABILITY_ID'],
    'LATITUDE': ['ALTITUDE', 'FRAMEWORK', 'COORDINATE'],
    'LONGITUDE': ['FRAMEWORK', 'COORDINATE'],
    'LOCATION': ['TOOL', 'FRAMEWORK'],
    'THREAT_ACTOR': ['ACTOR', 'ACTOR_TYPE'],
    'EMAIL_ADDRESS': ['EMAIL'],
    'PHONE_NUMBER': ['PHONE']
}

VALID_PATTERNS = {
    'IP_ADDRESS': IP_PATTERN,
    'DOMAIN': DOMAIN_PATTERN,
    'CVE_ID': CVE_PATTERN,
    'EMAIL': EMAIL_PATTERN,
    'EMAIL_ADDRESS': EMAIL_PATTERN,
    'PHONE_NUMBER': PHONE_PATTERN,
    'WALLET_ADDRESS': WALLET_PATTERN,
    'LATITUDE': LATITUDE_PATTERN,
    'LONGITUDE': LONGITUDE_PATTERN,
}

# For finding missing entities, use more lenient patterns
FIND_PATTERNS = {
    'IP_ADDRESS': IP_PATTERN,
    'DOMAIN': DOMAIN_PATTERN,
    'CVE_ID': CVE_PATTERN,
    'EMAIL': EMAIL_PATTERN,
    'EMAIL_ADDRESS': EMAIL_PATTERN,
    'PHONE_NUMBER': PHONE_PATTERN,
    'WALLET_ADDRESS': WALLET_PATTERN,
    'LATITUDE': COORDINATE_PAIR_PATTERN,  # Use coordinate pair for finding
    'LONGITUDE': COORDINATE_PAIR_PATTERN,  # Use coordinate pair for finding
}

def find_entities_in_text(text: str, pattern: re.Pattern) -> List[Tuple[int, int, str]]:
    """Find all matches of a pattern in text, returning (start, end, text) tuples."""
    entities = []
    for match in pattern.finditer(text):
        entities.append((match.start(), match.end(), match.group()))
    return entities

def check_entity_boundary(text: str, start: int, end: int, label: str) -> Dict:
    """Check if entity boundary is correct."""
    entity_text = text[start:end]
    issues = []
    
    # Check for whitespace
    if entity_text != entity_text.strip():
        issues.append('WHITESPACE')
        entity_text = entity_text.strip()
    
    # Check if too short
    if len(entity_text) < 2 and label not in ['IP_ADDRESS', 'DOMAIN', 'CVE_ID']:
        issues.append('TOO_SHORT')
    
    # Check pattern match
    if label in VALID_PATTERNS:
        pattern = VALID_PATTERNS[label]
        if not pattern.fullmatch(entity_text):
            issues.append('INVALID_PATTERN')
            # Try to find correct boundary
            correct_matches = find_entities_in_text(text, pattern)
            for cm_start, cm_end, cm_text in correct_matches:
                if cm_text == entity_text or entity_text in cm_text or cm_text in entity_text:
                    issues.append(f'WRONG_BOUNDARY: expected ({cm_start}, {cm_end})')
                    break
    
    # Check for partial words
    if len(entity_text) > 0:
        if start > 0 and text[start-1].isalnum():
            issues.append('PARTIAL_WORD_START')
        if end < len(text) and text[end].isalnum():
            issues.append('PARTIAL_WORD_END')
    
    return {
        'entity_text': entity_text,
        'start': start,
        'end': end,
        'label': label,
        'issues': issues,
        'is_valid': len(issues) == 0
    }

def audit_file(file_path: Path) -> Dict:
    """Audit a single training file."""
    results = {
        'file': str(file_path),
        'total_examples': 0,
        'total_entities': 0,
        'critical_entities': defaultdict(int),
        'misclassified': [],
        'boundary_issues': [],
        'missing_entities': [],
        'boundary_accuracy': 0.0,
        'details': []
    }
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            
            try:
                data = json.loads(line)
                text = data.get('text', '')
                entities = data.get('entities', [])
                
                results['total_examples'] += 1
                results['total_entities'] += len(entities)
                
                # Track critical entities
                for start, end, label in entities:
                    if label in CRITICAL_ENTITY_TYPES:
                        results['critical_entities'][label] += 1
                    
                    # Check boundary
                    boundary_check = check_entity_boundary(text, start, end, label)
                    if boundary_check['issues']:
                        results['boundary_issues'].append({
                            'line': line_num,
                            'text': text[:100] + '...' if len(text) > 100 else text,
                            **boundary_check
                        })
                    
                    # Check for misclassification
                    if label in MISCLASSIFIED_PATTERNS:
                        entity_text = text[start:end]
                        # Check if this should be a critical type
                        for critical_type, wrong_labels in MISCLASSIFIED_PATTERNS.items():
                            if label in wrong_labels:
                                # Check if it matches the critical type pattern
                                if critical_type in VALID_PATTERNS:
                                    pattern = VALID_PATTERNS[critical_type]
                                    if pattern.match(entity_text):
                                        results['misclassified'].append({
                                            'line': line_num,
                                            'entity_text': entity_text,
                                            'wrong_label': label,
                                            'should_be': critical_type,
                                            'text': text[:100] + '...' if len(text) > 100 else text
                                        })
                
                # Check for missing entities (entities that should be labeled but aren't)
                for critical_type, pattern in FIND_PATTERNS.items():
                    matches = find_entities_in_text(text, pattern)
                    for m_start, m_end, m_text in matches:
                        # Check if this entity is already labeled
                        found = False
                        for e_start, e_end, e_label in entities:
                            if (m_start >= e_start and m_end <= e_end) or \
                               (e_start >= m_start and e_end <= m_end):
                                found = True
                                break
                        
                        if not found:
                            results['missing_entities'].append({
                                'line': line_num,
                                'entity_text': m_text,
                                'should_be_labeled': critical_type,
                                'position': (m_start, m_end),
                                'text': text[:100] + '...' if len(text) > 100 else text
                            })
                
            except json.JSONDecodeError as e:
                results['details'].append({
                    'line': line_num,
                    'error': f'JSON decode error: {e}'
                })
    
    # Calculate boundary accuracy
    if results['total_entities'] > 0:
        valid_entities = results['total_entities'] - len(results['boundary_issues'])
        results['boundary_accuracy'] = (valid_entities / results['total_entities']) * 100
    
    return results

def main():
    """Main audit function."""
    base_dir = Path('cyber-train/entities-intent')
    if not base_dir.exists():
        base_dir = Path('entities-intent')
    
    entity_files = list(base_dir.rglob('*_entities.jsonl'))
    
    print("="*80)
    print("COMPREHENSIVE TRAINING DATA AUDIT")
    print("="*80)
    print(f"\nFound {len(entity_files)} entity training files\n")
    
    all_results = []
    total_stats = {
        'total_files': 0,
        'total_examples': 0,
        'total_entities': 0,
        'critical_entities': defaultdict(int),
        'total_misclassified': 0,
        'total_boundary_issues': 0,
        'total_missing': 0,
        'boundary_accuracy_sum': 0.0
    }
    
    for file_path in sorted(entity_files):
        print(f"\n{'='*80}")
        print(f"Auditing: {file_path.name}")
        print(f"{'='*80}")
        
        results = audit_file(file_path)
        all_results.append(results)
        
        # Update totals
        total_stats['total_files'] += 1
        total_stats['total_examples'] += results['total_examples']
        total_stats['total_entities'] += results['total_entities']
        total_stats['total_misclassified'] += len(results['misclassified'])
        total_stats['total_boundary_issues'] += len(results['boundary_issues'])
        total_stats['total_missing'] += len(results['missing_entities'])
        total_stats['boundary_accuracy_sum'] += results['boundary_accuracy']
        
        for label, count in results['critical_entities'].items():
            total_stats['critical_entities'][label] += count
        
        # Print summary for this file
        print(f"\n📊 File Statistics:")
        print(f"   Total examples: {results['total_examples']}")
        print(f"   Total entities: {results['total_entities']}")
        print(f"   Boundary accuracy: {results['boundary_accuracy']:.2f}%")
        
        print(f"\n🏷️  Critical Entities Found:")
        for label in sorted(CRITICAL_ENTITY_TYPES):
            count = results['critical_entities'][label]
            if count > 0:
                print(f"   {label}: {count}")
        
        print(f"\n⚠️  Issues Found:")
        print(f"   Misclassified: {len(results['misclassified'])}")
        print(f"   Boundary issues: {len(results['boundary_issues'])}")
        print(f"   Missing entities: {len(results['missing_entities'])}")
        
        # Show top issues
        if results['misclassified']:
            print(f"\n   Top Misclassified Examples:")
            for item in results['misclassified'][:5]:
                print(f"      Line {item['line']}: '{item['entity_text']}' → {item['wrong_label']} (should be {item['should_be']})")
        
        if results['boundary_issues']:
            print(f"\n   Top Boundary Issues:")
            for item in results['boundary_issues'][:5]:
                print(f"      Line {item['line']}: '{item['entity_text']}' ({item['label']}) - {', '.join(item['issues'])}")
        
        if results['missing_entities']:
            print(f"\n   Top Missing Entities:")
            for item in results['missing_entities'][:5]:
                print(f"      Line {item['line']}: '{item['entity_text']}' should be labeled as {item['should_be_labeled']}")
    
    # Print overall summary
    print(f"\n\n{'='*80}")
    print("OVERALL SUMMARY")
    print(f"{'='*80}")
    print(f"\nTotal Files Audited: {total_stats['total_files']}")
    print(f"Total Examples: {total_stats['total_examples']}")
    print(f"Total Entities: {total_stats['total_entities']}")
    print(f"Average Boundary Accuracy: {total_stats['boundary_accuracy_sum'] / total_stats['total_files']:.2f}%")
    
    print(f"\n📊 Critical Entities Across All Files:")
    for label in sorted(CRITICAL_ENTITY_TYPES):
        count = total_stats['critical_entities'][label]
        print(f"   {label}: {count}")
    
    print(f"\n⚠️  Overall Issues:")
    print(f"   Total Misclassified: {total_stats['total_misclassified']}")
    print(f"   Total Boundary Issues: {total_stats['total_boundary_issues']}")
    print(f"   Total Missing Entities: {total_stats['total_missing']}")
    
    # Save detailed report
    report_file = Path('cyber-train/TRAINING_DATA_AUDIT_REPORT.json')
    with open(report_file, 'w') as f:
        json.dump({
            'summary': total_stats,
            'file_results': all_results
        }, f, indent=2)
    
    print(f"\n✅ Detailed report saved to: {report_file}")
    
    # Create markdown report
    md_report = Path('cyber-train/TRAINING_DATA_AUDIT_REPORT.md')
    with open(md_report, 'w') as f:
        f.write("# Training Data Audit Report\n\n")
        f.write(f"**Date:** {Path(__file__).stat().st_mtime}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- Total Files: {total_stats['total_files']}\n")
        f.write(f"- Total Examples: {total_stats['total_examples']}\n")
        f.write(f"- Total Entities: {total_stats['total_entities']}\n")
        f.write(f"- Average Boundary Accuracy: {total_stats['boundary_accuracy_sum'] / total_stats['total_files']:.2f}%\n\n")
        f.write(f"## Critical Entities\n\n")
        for label in sorted(CRITICAL_ENTITY_TYPES):
            count = total_stats['critical_entities'][label]
            f.write(f"- {label}: {count}\n")
        f.write(f"\n## Issues\n\n")
        f.write(f"- Misclassified: {total_stats['total_misclassified']}\n")
        f.write(f"- Boundary Issues: {total_stats['total_boundary_issues']}\n")
        f.write(f"- Missing Entities: {total_stats['total_missing']}\n\n")
        f.write(f"## Per-File Results\n\n")
        for result in all_results:
            f.write(f"### {Path(result['file']).name}\n\n")
            f.write(f"- Examples: {result['total_examples']}\n")
            f.write(f"- Entities: {result['total_entities']}\n")
            f.write(f"- Boundary Accuracy: {result['boundary_accuracy']:.2f}%\n")
            f.write(f"- Misclassified: {len(result['misclassified'])}\n")
            f.write(f"- Boundary Issues: {len(result['boundary_issues'])}\n")
            f.write(f"- Missing: {len(result['missing_entities'])}\n\n")
    
    print(f"✅ Markdown report saved to: {md_report}")

if __name__ == '__main__':
    main()

