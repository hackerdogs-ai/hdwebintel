#!/usr/bin/env python3
"""
Comprehensive Boundary Accuracy Checker
Reviews EVERY file, EVERY line, EVERY entity boundary
Measures accuracy of each boundary and reports total accuracy %
"""

import json
import re
from pathlib import Path
from typing import List, Tuple, Dict
from collections import defaultdict

# Patterns for validation
IP_PATTERN = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_INTL_PATTERN = re.compile(r'\b\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}\b')
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
LATITUDE_PATTERN = re.compile(r'\b-?\d{1,2}(\.\d+)?\b')
LONGITUDE_PATTERN = re.compile(r'\b-?\d{1,3}(\.\d+)?\b')

# Common words that should NEVER be entities
COMMON_WORDS_NEVER_ENTITIES = {
    'ai', 'security', 'incident', 'escalation', 'rate', 'maintained', 'threshold',
    'ma', 'rat', 'ed', 'at', 'below', 'ed at', 'at 2%', 'ed at 2%',
    'me', 'i', 'the', 'a', 'an', 'this', 'that', 'for', 'and', 'or', 'but',
    'in', 'on', 'to', 'from', 'with', 'by', 'of', 'is', 'are', 'was', 'were',
    'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'can', 'must',
    'you', 'your', 'he', 'she', 'it', 'we', 'they', 'them',
    'what', 'when', 'where', 'why', 'how', 'who', 'which',
    'hey', 'hi', 'hello', 'thanks', 'please',
    'valid', 'ted', 'ing', 'tion', 'ed at', 'at 2%', 'cal', 'ded', 'med',
    'check', 'verify', 'investigate', 'analyze', 'detect', 'monitor', 'track',
    'execute', 'block', 'isolate', 'generate', 'find', 'show', 'get', 'set',
    'compliance', 'requirements', 'data', 'system', 'network', 'threat',
    'intelligence', 'report', 'tool', 'type', 'count', 'metric', 'value',
    'model', 'attack', 'response', 'coordination', 'team', 'teams',
    'platform', 'feeds', 'provided', 'including', 'hashes', 'infrastructure',
    'review', 'repository', 'branch', 'commit', 'contains', 'configuration',
    'source', 'code', 'audit', 'needed', 'detected', 'against', 'using',
    'techniques', 'coordinated', 'across', 'engineering', 'legal', 'validated',
    'mapped', 'controls', 'function', 'covering', 'objectives', 'processing',
    'consumer', 'facilitated', 'during', 'breach', 'confirmed', 'explanations',
    'met', 'interpretability', 'medical', 'automated', 'testing', 'pipeline',
    'executed', 'cases', 'pass', 'bias', 'metrics', 'fairness', 'found',
    'gender', 'outputs', 'filtered', 'inappropriate', 'content', 'remediation',
    'completed', 'issues', 'within', 'sla', 'enforced', 'filtering', 'blocking',
    'toxic', 'release', 'across', 'controls', 'filtered', 'content', 'outputs',
    'validated', 'mapped', 'function', 'covering', 'objectives', 'processing',
    'consumer', 'facilitated', 'during', 'breach', 'confirmed', 'explanations',
    'met', 'automated', 'testing', 'pipeline', 'executed', 'cases', 'pass',
    'bias', 'metrics', 'fairness', 'found', 'gender', 'outputs', 'filtered',
    'inappropriate', 'content', 'remediation', 'completed', 'issues', 'within',
    'sla', 'enforced', 'filtering', 'blocking', 'toxic', 'release'
}

# Problematic labels for common words
PROBLEMATIC_LABELS = {
    'AI_MODEL_TYPE': {'ai'},
    'SECURITY_TYPE': {'security'},
    'INCIDENT_TYPE': {'incident'},
    'METRIC_TYPE': {'rate', 'escalation', 'maintained', 'ma', 'rat', 'metric', 'metrics'},
    'THRESHOLD_TYPE': {'threshold'},
    'TOOL': {'tool', 'tools', 'check', 'verify', 'investigate', 'analyze'},
    'BRANCH': {'branch', 'branches'},
    'COMMIT': {'commit', 'commits'},
    'TRAINING_TYPE': {'training', 'test', 'testing'},
    'INTEGRATION_TYPE': {'integration', 'integrate'},
    'ENCRYPTION_TYPE': {'encryption', 'encrypt'},
    'VULNERABILITY_ID': {'vulnerability', 'vulnerabilities'},
    'QUERY_TYPE': {'query', 'queries'},
    'REQUIREMENT_TYPE': {'requirement', 'requirements'},
}


def is_partial_word(text: str, entity_text: str, start: int, end: int) -> bool:
    """Check if entity is a partial word."""
    entity_lower = entity_text.lower().strip()
    
    if len(entity_lower) <= 2:
        return False  # Too short to determine
    
    # Check if it's a substring of a word in the text
    search_start = max(0, start - 15)
    search_end = min(len(text), end + 15)
    search_region = text[search_start:search_end]
    
    # Find all words in the region
    words = re.findall(r'\b\w+\b', search_region)
    for word in words:
        word_lower = word.lower()
        if entity_lower in word_lower and len(entity_lower) < len(word_lower):
            # Check if it's clearly partial (not a valid standalone word)
            if len(entity_lower) <= 5:
                return True
    
    # Check if it ends with partial suffixes
    if entity_lower.endswith(('ed', 'ing', 'tion', 'ted', 'cal', 'ded', 'med', 'ed at', 'at 2%')):
        # Check if it's at word boundary (suggesting it's cut off)
        if end < len(text) and text[end].isalnum():
            return True
    
    return False


def check_boundary_accuracy(text: str, start: int, end: int, label: str) -> Dict:
    """
    Check if boundary is accurate.
    Returns dict with accuracy status and issues.
    """
    issues = []
    is_accurate = True
    
    # Basic validation
    if start < 0 or end > len(text) or start >= end:
        return {
            'accurate': False,
            'issues': ['INVALID_BOUNDARY: start/end out of range'],
            'entity_text': '',
            'should_remove': True
        }
    
    entity_text = text[start:end]
    entity_clean = entity_text.strip()
    entity_lower = entity_clean.lower()
    
    # Check for whitespace
    if entity_text != entity_clean:
        issues.append('WHITESPACE: Entity has leading/trailing whitespace')
        is_accurate = False
    
    # Check if too short
    if len(entity_clean) <= 1 and entity_clean not in ['I', 'A']:
        issues.append('TOO_SHORT: Entity is too short')
        is_accurate = False
    
    # Check if common word
    if entity_lower in COMMON_WORDS_NEVER_ENTITIES:
        issues.append(f'COMMON_WORD: "{entity_clean}" is a common word that should not be an entity')
        is_accurate = False
    
    # Check if problematic label for common word
    if label in PROBLEMATIC_LABELS:
        if entity_lower in PROBLEMATIC_LABELS[label]:
            issues.append(f'PROBLEMATIC_LABEL: "{entity_clean}" should not be labeled as {label}')
            is_accurate = False
    
    # Check if partial word
    if is_partial_word(text, entity_clean, start, end):
        issues.append(f'PARTIAL_WORD: "{entity_clean}" appears to be a partial word')
        is_accurate = False
    
    # Validate pattern-based entities
    if label == 'IP_ADDRESS':
        if not IP_PATTERN.fullmatch(entity_clean):
            issues.append(f'INVALID_PATTERN: "{entity_clean}" does not match IP address pattern')
            is_accurate = False
        else:
            # Check if boundary is correct (find actual IP in text)
            matches = list(IP_PATTERN.finditer(text))
            if matches:
                found = False
                for match in matches:
                    if match.start() == start and match.end() == end:
                        found = True
                        break
                if not found:
                    issues.append(f'WRONG_BOUNDARY: IP address boundary incorrect')
                    is_accurate = False
    
    elif label == 'DOMAIN':
        if not DOMAIN_PATTERN.fullmatch(entity_clean):
            issues.append(f'INVALID_PATTERN: "{entity_clean}" does not match domain pattern')
            is_accurate = False
        else:
            matches = list(DOMAIN_PATTERN.finditer(text))
            if matches:
                found = False
                for match in matches:
                    if match.start() == start and match.end() == end:
                        found = True
                        break
                if not found:
                    issues.append(f'WRONG_BOUNDARY: Domain boundary incorrect')
                    is_accurate = False
    
    elif label == 'CVE_ID':
        if not CVE_PATTERN.fullmatch(entity_clean):
            issues.append(f'INVALID_PATTERN: "{entity_clean}" does not match CVE pattern')
            is_accurate = False
        else:
            matches = list(CVE_PATTERN.finditer(text))
            if matches:
                found = False
                for match in matches:
                    if match.start() == start and match.end() == end:
                        found = True
                        break
                if not found:
                    issues.append(f'WRONG_BOUNDARY: CVE boundary incorrect')
                    is_accurate = False
    
    elif label in ['EMAIL', 'EMAIL_ADDRESS']:
        if not EMAIL_PATTERN.fullmatch(entity_clean):
            issues.append(f'INVALID_PATTERN: "{entity_clean}" does not match email pattern')
            is_accurate = False
        else:
            matches = list(EMAIL_PATTERN.finditer(text))
            if matches:
                found = False
                for match in matches:
                    if match.start() == start and match.end() == end:
                        found = True
                        break
                if not found:
                    issues.append(f'WRONG_BOUNDARY: Email boundary incorrect')
                    is_accurate = False
    
    elif label == 'PHONE_NUMBER':
        if not PHONE_INTL_PATTERN.fullmatch(entity_clean) and not re.match(r'\b\+?[\d\s\-\(\)]{10,}\b', entity_clean):
            issues.append(f'INVALID_PATTERN: "{entity_clean}" does not match phone pattern')
            is_accurate = False
    
    elif label == 'SSN':
        if not SSN_PATTERN.fullmatch(entity_clean):
            issues.append(f'INVALID_PATTERN: "{entity_clean}" does not match SSN pattern')
            is_accurate = False
    
    elif label == 'CREDIT_CARD_NUMBER':
        if not CREDIT_CARD_PATTERN.fullmatch(entity_clean):
            issues.append(f'INVALID_PATTERN: "{entity_clean}" does not match credit card pattern')
            is_accurate = False
    
    elif label == 'WALLET_ADDRESS':
        if not WALLET_PATTERN.fullmatch(entity_clean):
            issues.append(f'INVALID_PATTERN: "{entity_clean}" does not match wallet address pattern')
            is_accurate = False
    
    elif label == 'LATITUDE':
        if not LATITUDE_PATTERN.fullmatch(entity_clean):
            issues.append(f'INVALID_PATTERN: "{entity_clean}" does not match latitude pattern')
            is_accurate = False
    
    elif label == 'LONGITUDE':
        if not LONGITUDE_PATTERN.fullmatch(entity_clean):
            issues.append(f'INVALID_PATTERN: "{entity_clean}" does not match longitude pattern')
            is_accurate = False
    
    # Check if entity text contains common phrase
    for phrase in COMMON_WORDS_NEVER_ENTITIES:
        if len(phrase) > 2 and phrase in entity_lower:
            issues.append(f'CONTAINS_COMMON_PHRASE: Entity contains common phrase "{phrase}"')
            is_accurate = False
            break
    
    return {
        'accurate': is_accurate,
        'issues': issues,
        'entity_text': entity_clean,
        'should_remove': len(issues) > 0 and any('COMMON_WORD' in i or 'PROBLEMATIC_LABEL' in i or 'PARTIAL_WORD' in i for i in issues)
    }


def check_file(file_path: Path) -> Dict:
    """Check all entities in a file."""
    stats = {
        'file': str(file_path),
        'total_lines': 0,
        'total_entities': 0,
        'accurate_entities': 0,
        'inaccurate_entities': 0,
        'issues_by_type': defaultdict(int),
        'entity_details': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                stats['total_lines'] += 1
                try:
                    data = json.loads(line)
                    text = data.get('text', '')
                    entities = data.get('entities', [])
                    
                    for start, end, label in entities:
                        stats['total_entities'] += 1
                        result = check_boundary_accuracy(text, start, end, label)
                        
                        if result['accurate']:
                            stats['accurate_entities'] += 1
                        else:
                            stats['inaccurate_entities'] += 1
                            for issue in result['issues']:
                                issue_type = issue.split(':')[0]
                                stats['issues_by_type'][issue_type] += 1
                            
                            stats['entity_details'].append({
                                'line': line_num,
                                'start': start,
                                'end': end,
                                'label': label,
                                'entity_text': result['entity_text'],
                                'issues': result['issues']
                            })
                
                except json.JSONDecodeError as e:
                    stats['entity_details'].append({
                        'line': line_num,
                        'error': f'JSON decode error: {str(e)}'
                    })
                    stats['inaccurate_entities'] += 1
    
    except Exception as e:
        stats['error'] = str(e)
    
    return stats


def main():
    base_dir = Path("cyber-train/entities-intent")
    entity_files = sorted(list(base_dir.rglob("*_entities.jsonl")))
    
    print("="*80)
    print("COMPREHENSIVE BOUNDARY ACCURACY CHECK")
    print("="*80)
    print(f"\nTotal files to check: {len(entity_files)}")
    print("\nChecking every file, every line, every entity boundary...\n")
    
    all_stats = []
    total_entities = 0
    total_accurate = 0
    total_inaccurate = 0
    all_issues_by_type = defaultdict(int)
    
    for file_path in entity_files:
        print(f"Checking: {file_path.relative_to(base_dir)}")
        stats = check_file(file_path)
        all_stats.append(stats)
        
        total_entities += stats['total_entities']
        total_accurate += stats['accurate_entities']
        total_inaccurate += stats['inaccurate_entities']
        
        for issue_type, count in stats['issues_by_type'].items():
            all_issues_by_type[issue_type] += count
        
        accuracy = (stats['accurate_entities'] / stats['total_entities'] * 100) if stats['total_entities'] > 0 else 0
        print(f"  Lines: {stats['total_lines']}, Entities: {stats['total_entities']}, Accurate: {stats['accurate_entities']}, Inaccurate: {stats['inaccurate_entities']}, Accuracy: {accuracy:.2f}%")
    
    # Overall accuracy
    overall_accuracy = (total_accurate / total_entities * 100) if total_entities > 0 else 0
    
    print("\n" + "="*80)
    print("OVERALL ACCURACY SUMMARY")
    print("="*80)
    print(f"\nTotal Files: {len(entity_files)}")
    print(f"Total Lines: {sum(s['total_lines'] for s in all_stats):,}")
    print(f"Total Entities: {total_entities:,}")
    print(f"Accurate Entities: {total_accurate:,}")
    print(f"Inaccurate Entities: {total_inaccurate:,}")
    print(f"\n{'='*80}")
    print(f"OVERALL BOUNDARY ACCURACY: {overall_accuracy:.2f}%")
    print(f"{'='*80}")
    
    print(f"\nIssues by Type:")
    for issue_type, count in sorted(all_issues_by_type.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_entities * 100) if total_entities > 0 else 0
        print(f"  {issue_type:30s}: {count:6,} ({pct:.2f}%)")
    
    # Per-file breakdown
    print("\n" + "="*80)
    print("PER-FILE ACCURACY BREAKDOWN")
    print("="*80)
    
    for stats in sorted(all_stats, key=lambda x: (x['inaccurate_entities'] / x['total_entities'] if x['total_entities'] > 0 else 1), reverse=True):
        accuracy = (stats['accurate_entities'] / stats['total_entities'] * 100) if stats['total_entities'] > 0 else 0
        file_name = Path(stats['file']).name
        print(f"\n{file_name}")
        print(f"  Accuracy: {accuracy:.2f}%")
        print(f"  Entities: {stats['total_entities']:,} (Accurate: {stats['accurate_entities']:,}, Inaccurate: {stats['inaccurate_entities']:,})")
        if stats['inaccurate_entities'] > 0:
            print(f"  Issues:")
            for issue_type, count in sorted(stats['issues_by_type'].items(), key=lambda x: x[1], reverse=True):
                print(f"    {issue_type:30s}: {count:6,}")
    
    # Save detailed report
    report_file = Path("cyber-train/BOUNDARY_ACCURACY_REPORT.json")
    with open(report_file, 'w') as f:
        json.dump({
            'summary': {
                'total_files': len(entity_files),
                'total_lines': sum(s['total_lines'] for s in all_stats),
                'total_entities': total_entities,
                'accurate_entities': total_accurate,
                'inaccurate_entities': total_inaccurate,
                'overall_accuracy': overall_accuracy,
                'issues_by_type': dict(all_issues_by_type)
            },
            'files': all_stats
        }, f, indent=2)
    
    print(f"\n\nDetailed report saved to: {report_file}")
    print(f"\n{'='*80}")
    print(f"FINAL RESULT: {overall_accuracy:.2f}% BOUNDARY ACCURACY")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()

