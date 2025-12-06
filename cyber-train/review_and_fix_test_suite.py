#!/usr/bin/env python3
"""
Review test suite expected entities and fix incorrect ones.
This script analyzes the test suite and identifies potentially incorrect expected entities.
"""

import json
import re
from pathlib import Path
from typing import List, Tuple, Dict
from collections import defaultdict

# Load test results to see what was actually detected vs expected
def load_test_results() -> List[Dict]:
    """Load comprehensive test results."""
    with open('comprehensive_test_results.json', 'r') as f:
        data = json.load(f)
    return data.get('test_cases', [])

# Patterns for validation
IP_PATTERN = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
DOMAIN_PATTERN = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$')
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
URL_PATTERN = re.compile(r'^https?://[^\s]+|ftp://[^\s]+|www\.[^\s]+')
FILE_PATH_PATTERN = re.compile(r'^[A-Z]:\\|^/|^\\\\|^~/')
DATE_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|[A-Z][a-z]+ \d{1,2}, \d{4}')
TIME_PATTERN = re.compile(r'\d{1,2}:\d{2}(:\d{2})?( [AP]M)?')
HASH_PATTERN = re.compile(r'^[a-fA-F0-9]{32,64}$')
CVE_PATTERN = re.compile(r'^CVE-\d{4}-\d{4,7}$', re.IGNORECASE)

# Common words that shouldn't be entities
COMMON_WORDS_NOT_ENTITY = {
    'csrf', 'javascript', 'json', 'xml', 'html', 'css', 'python', 'base64',
    'debunk', 'relative', 'absolute', 'find', 'extract', 'url', 'import',
    'investigate', 'check', 'verify', 'analyze', 'detect', 'monitor', 'track',
    'race', 'time', 'events', 'exercise', 'kernel-level'
}

def validate_entity(text: str, label: str) -> Tuple[bool, str]:
    """
    Validate if an entity is correct.
    Returns (is_valid, reason)
    """
    text_lower = text.lower().strip()
    
    # Check if it's a common word that shouldn't be an entity
    if text_lower in COMMON_WORDS_NOT_ENTITY:
        return False, f"Common word '{text}' should not be entity"
    
    # Validate based on label
    if label == "IP_ADDRESS":
        if not IP_PATTERN.match(text):
            return False, f"Invalid IP address format: {text}"
    
    elif label == "DOMAIN":
        if not DOMAIN_PATTERN.match(text):
            return False, f"Invalid domain format: {text}"
    
    elif label == "EMAIL_ADDRESS":
        if not EMAIL_PATTERN.match(text):
            return False, f"Invalid email format: {text}"
    
    elif label == "URL":
        if not URL_PATTERN.match(text):
            return False, f"Invalid URL format: {text}"
    
    elif label == "FILE_PATH":
        if not FILE_PATH_PATTERN.match(text):
            return False, f"Invalid file path format: {text}"
    
    elif label == "DATE":
        if not DATE_PATTERN.search(text):
            return False, f"Invalid date format: {text}"
    
    elif label == "TIME":
        if not TIME_PATTERN.search(text):
            return False, f"Invalid time format: {text}"
    
    elif label == "HASH":
        if not HASH_PATTERN.match(text):
            return False, f"Invalid hash format: {text}"
    
    elif label == "CVE_ID":
        if not CVE_PATTERN.match(text):
            return False, f"Invalid CVE format: {text}"
    
    elif label == "TOOL":
        # TOOL should be a real tool name, not common words
        if text_lower in ['csrf', 'javascript', 'json', 'xml', 'html', 'base64', 'debunk', 'relative']:
            return False, f"Common word '{text}' should not be TOOL"
    
    elif label == "REPOSITORY":
        # REPOSITORY should be in format user/repo or github.com/user/repo
        if not re.match(r'^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$|github\.com/[^\s]+|gitlab\.com/[^\s]+', text):
            if URL_PATTERN.match(text):
                return False, f"'{text}' is a URL, not REPOSITORY"
            return False, f"Invalid repository format: {text}"
    
    return True, "Valid"

def analyze_test_suite():
    """Analyze test suite for incorrect expected entities."""
    test_cases = load_test_results()
    
    issues = []
    stats = defaultdict(int)
    
    for i, test in enumerate(test_cases):
        text = test.get('text', '')
        expected = test.get('expected_entities', [])
        detected = test.get('entities', [])
        
        # Check each expected entity
        for entity_text, entity_label in expected:
            is_valid, reason = validate_entity(entity_text, entity_label)
            if not is_valid:
                issues.append({
                    'test_index': i,
                    'text': text[:100],
                    'entity': entity_text,
                    'label': entity_label,
                    'reason': reason,
                    'category': test.get('category', 'unknown')
                })
                stats['invalid_expected'] += 1
        
        # Check if expected entities match detected (potential false negatives)
        expected_set = set((t, l) for t, l in expected)
        detected_set = set((t, l) for t, l in detected)
        
        missed = expected_set - detected_set
        if missed:
            stats['missed_entities'] += len(missed)
        
        # Check for false positives (detected but not expected)
        false_pos = detected_set - expected_set
        if false_pos:
            stats['false_positives'] += len(false_pos)
    
    return issues, stats

def main():
    print("="*80)
    print("REVIEW TEST SUITE EXPECTED ENTITIES")
    print("="*80)
    print()
    
    issues, stats = analyze_test_suite()
    
    print(f"📊 Analysis Results:")
    print(f"   Total test cases analyzed: {len(load_test_results())}")
    print(f"   Invalid expected entities found: {stats['invalid_expected']}")
    print(f"   Missed entities: {stats['missed_entities']}")
    print(f"   False positives: {stats['false_positives']}")
    print()
    
    if issues:
        print(f"🚨 Issues Found ({len(issues)}):")
        print()
        
        # Group by issue type
        by_reason = defaultdict(list)
        for issue in issues:
            by_reason[issue['reason']].append(issue)
        
        for reason, issue_list in sorted(by_reason.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"   {reason}: {len(issue_list)} instances")
            for issue in issue_list[:5]:  # Show first 5
                print(f"      - Test {issue['test_index']}: '{issue['entity']}' → {issue['label']}")
                print(f"        Text: {issue['text'][:80]}...")
            if len(issue_list) > 5:
                print(f"      ... and {len(issue_list) - 5} more")
            print()
    
    # Save report
    report = {
        'total_issues': len(issues),
        'stats': dict(stats),
        'issues': issues[:50]  # First 50 issues
    }
    
    with open('test_suite_review_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Report saved to: test_suite_review_report.json")
    print("="*80)

if __name__ == "__main__":
    main()

