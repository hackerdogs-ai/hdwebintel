#!/usr/bin/env python3
"""
Comprehensive quality audit of all entity and intent JSONL files.
Extremely detailed analysis for production quality.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple, Set
import unicodedata

# Comprehensive patterns for validation
IP_PATTERN = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
IPV6_PATTERN = re.compile(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b::1\b|\bfe80::[0-9a-fA-F:]+')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?[\d\s\-\(\)]{10,}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
GITHUB_REPO_PATTERN = re.compile(r'[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+')
GITHUB_URL_PATTERN = re.compile(r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)*')
GITHUB_USER_PATTERN = re.compile(r'@?[a-zA-Z0-9]([a-zA-Z0-9]|-(?![.-])){0,38}')
GITHUB_GIST_PATTERN = re.compile(r'https?://gist\.github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9]+')
GITHUB_ISSUE_PATTERN = re.compile(r'#[0-9]+')
GITHUB_COMMIT_PATTERN = re.compile(r'\b[a-f0-9]{7,40}\b')
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b')
LATITUDE_PATTERN = re.compile(r'\b-?([0-8]?[0-9](?:\.\d+)?|90(?:\.0+)?)\b')
LONGITUDE_PATTERN = re.compile(r'\b-?(?:[0-9]?[0-9]?[0-9](?:\.\d+)?|1[0-7][0-9](?:\.\d+)?|180(?:\.0+)?)\b')
GEOJSON_PATTERN = re.compile(r'\{"type"\s*:\s*"Point"\s*,\s*"coordinates"\s*:\s*\[-?\d+\.?\d*,\s*-?\d+\.?\d*\]\}')
DMS_PATTERN = re.compile(r'\d+°\d+\'\d+\.?\d*"[NS]\s+\d+°\d+\'\d+\.?\d*"[EW]')
EMOJI_PATTERN = re.compile(r'[\U0001F300-\U0001F9FF\U0001FA00-\U0001FAFF\u2600-\u26FF\u2700-\u27BF]')

VALID_PATTERNS = {
    'IP_ADDRESS': IP_PATTERN,
    'IPV6_ADDRESS': IPV6_PATTERN,
    'DOMAIN': DOMAIN_PATTERN,
    'CVE_ID': CVE_PATTERN,
    'EMAIL': EMAIL_PATTERN,
    'EMAIL_ADDRESS': EMAIL_PATTERN,
    'PHONE_NUMBER': PHONE_PATTERN,
    'WALLET_ADDRESS': WALLET_PATTERN,
    'URL': URL_PATTERN,
    'GITHUB_REPO': GITHUB_REPO_PATTERN,
    'GITHUB_REPO_URL': GITHUB_URL_PATTERN,
    'GITHUB_USER': GITHUB_USER_PATTERN,
    'GITHUB_GIST': GITHUB_GIST_PATTERN,
    'GITHUB_ISSUE': GITHUB_ISSUE_PATTERN,
    'GITHUB_COMMIT': GITHUB_COMMIT_PATTERN,
    'SSN': SSN_PATTERN,
    'CREDIT_CARD_NUMBER': CREDIT_CARD_PATTERN,
    'LATITUDE': LATITUDE_PATTERN,
    'LONGITUDE': LONGITUDE_PATTERN,
    'GEOJSON': GEOJSON_PATTERN,
    'DMS_COORDINATES': DMS_PATTERN,
    'EMOJI': EMOJI_PATTERN,
}

# Common words that should NEVER be entities
COMMON_WORDS_NEVER = {
    'the', 'a', 'an', 'this', 'that', 'for', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'from',
    'with', 'by', 'of', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must',
    'i', 'me', 'my', 'you', 'your', 'he', 'she', 'it', 'we', 'they', 'them',
    'what', 'when', 'where', 'why', 'how', 'who', 'which', 'whose', 'whom',
    'up', 'down', 'out', 'off', 'over', 'under', 'above', 'below',
    'access', 'attempt', 'attempts', 'from', 'ip', 'host', 'port', 'user', 'domain',
    'check', 'verify', 'investigate', 'analyze', 'detect', 'monitor', 'track',
    'execute', 'block', 'isolate', 'generate', 'find', 'show', 'get', 'set',
    'compliance', 'requirements', 'data', 'system', 'network', 'threat', 'intelligence',
    'report', 'tool', 'type', 'count', 'metric', 'value', 'number', 'phone', 'email', 'address',
    'card', 'credit', 'bank', 'account', 'ssn', 'long', 'various', 'types', 'appear',
    'anomalies', 'lateral', 'latitude', 'longitude', 'used', 'wannacry', 'campaign',
    'repository', 'repo', 'github', 'commit', 'branch', 'tag', 'release', 'issue', 'gist',
}

# Problematic labels for common words
PROBLEMATIC_LABELS = {
    'AI_MODEL_TYPE', 'SECURITY_TYPE', 'INCIDENT_TYPE', 'METRIC_TYPE', 'THRESHOLD_TYPE',
    'TOOL', 'TIME_UNIT', 'PRIORITIZATION_TYPE', 'SERVICE', 'SOURCE_TYPE',
    'ENCRYPTION_TYPE', 'VULNERABILITY_ID', 'TRAINING_TYPE', 'INTEGRATION_TYPE',
    'BRANCH', 'COMMIT', 'QUERY_TYPE', 'REQUIREMENT_TYPE', 'PERCENTAGE', 'COUNT',
    'PHONE_NUMBER', 'EMAIL_ADDRESS', 'CREDIT_CARD_NUMBER', 'SSN', 'BANK_ACCOUNT_NUMBER',
    'GITHUB_BRANCH', 'GITHUB_COMMIT', 'GITHUB_TAG', 'GITHUB_RELEASE', 'GITHUB_ISSUE',
}

def is_whitespace_char(c: str) -> bool:
    """Check if character is whitespace."""
    return c.isspace() or unicodedata.category(c) == 'Zs'

def check_entity_quality(text: str, start: int, end: int, label: str) -> Dict:
    """Comprehensive entity quality check."""
    issues = []
    entity_text = text[start:end]
    original_text = entity_text
    
    # 1. Check for leading/trailing whitespace
    if entity_text != entity_text.strip():
        issues.append({
            'type': 'WHITESPACE',
            'severity': 'HIGH',
            'message': f"Entity has leading/trailing whitespace: '{entity_text}'",
            'expected': entity_text.strip()
        })
        entity_text = entity_text.strip()
    
    # 2. Check if entity is too short
    if len(entity_text) < 2 and label not in ['IP_ADDRESS', 'DOMAIN', 'CVE_ID', 'EMAIL', 'PHONE_NUMBER', 'GITHUB_ISSUE']:
        issues.append({
            'type': 'TOO_SHORT',
            'severity': 'HIGH',
            'message': f"Entity too short: '{entity_text}' (length: {len(entity_text)})",
        })
    
    # 3. Check for partial words
    if start > 0:
        prev_char = text[start - 1]
        if prev_char.isalnum() or prev_char == '_':
            issues.append({
                'type': 'PARTIAL_WORD_START',
                'severity': 'HIGH',
                'message': f"Entity starts in middle of word: '{entity_text}' (prev char: '{prev_char}')",
            })
    
    if end < len(text):
        next_char = text[end]
        if next_char.isalnum() or next_char == '_':
            issues.append({
                'type': 'PARTIAL_WORD_END',
                'severity': 'HIGH',
                'message': f"Entity ends in middle of word: '{entity_text}' (next char: '{next_char}')",
            })
    
    # 4. Check pattern validation
    if label in VALID_PATTERNS:
        pattern = VALID_PATTERNS[label]
        if not pattern.fullmatch(entity_text):
            # Try to find correct boundary
            matches = list(pattern.finditer(text))
            correct_match = None
            for match in matches:
                if match.start() <= start and match.end() >= end:
                    correct_match = match
                    break
                if abs(match.start() - start) < 5 and abs(match.end() - end) < 5:
                    correct_match = match
                    break
            
            if correct_match:
                issues.append({
                    'type': 'WRONG_BOUNDARY',
                    'severity': 'CRITICAL',
                    'message': f"Wrong boundary for {label}: got '{entity_text}' (pos {start}-{end}), expected '{text[correct_match.start():correct_match.end()]}' (pos {correct_match.start()}-{correct_match.end()})",
                    'expected_text': text[correct_match.start():correct_match.end()],
                    'expected_start': correct_match.start(),
                    'expected_end': correct_match.end(),
                })
            else:
                issues.append({
                    'type': 'INVALID_PATTERN',
                    'severity': 'CRITICAL',
                    'message': f"Entity '{entity_text}' does not match pattern for {label}",
                })
    
    # 5. Check for common words incorrectly labeled
    if entity_text.lower() in COMMON_WORDS_NEVER and label in PROBLEMATIC_LABELS:
        issues.append({
            'type': 'COMMON_WORD_ENTITY',
            'severity': 'CRITICAL',
            'message': f"Common word '{entity_text}' incorrectly labeled as {label}",
        })
    
    # 6. Check for punctuation-only entities
    if all(c in '.,;:!?()[]{}\'"' for c in entity_text):
        issues.append({
            'type': 'PUNCTUATION_ONLY',
            'severity': 'HIGH',
            'message': f"Entity is only punctuation: '{entity_text}'",
        })
    
    # 7. Check for empty entities
    if len(entity_text.strip()) == 0:
        issues.append({
            'type': 'EMPTY_ENTITY',
            'severity': 'CRITICAL',
            'message': "Entity is empty",
        })
    
    # 8. Check boundary validity
    if start < 0 or end > len(text) or start >= end:
        issues.append({
            'type': 'INVALID_BOUNDARY',
            'severity': 'CRITICAL',
            'message': f"Invalid boundary: start={start}, end={end}, text_length={len(text)}",
        })
    
    return {
        'entity_text': original_text,
        'start': start,
        'end': end,
        'label': label,
        'issues': issues,
        'is_valid': len(issues) == 0,
        'severity': max([i['severity'] for i in issues], default='NONE')
    }

def check_intent_quality(text: str, intents: Dict) -> Dict:
    """Comprehensive intent quality check."""
    issues = []
    
    # Handle both 'intents' and 'cats' (spaCy format)
    if intents is None:
        intents = {}
    
    # 1. Check if intents is a dict
    if not isinstance(intents, dict):
        issues.append({
            'type': 'INVALID_FORMAT',
            'severity': 'CRITICAL',
            'message': f"Intents must be a dict, got {type(intents)}",
        })
        return {
            'text': text,
            'intents': intents,
            'issues': issues,
            'is_valid': False,
        }
    
    # 2. Check intent values are binary (0.0 or 1.0)
    for intent_name, intent_value in intents.items():
        if not isinstance(intent_value, (int, float)):
            issues.append({
                'type': 'INVALID_VALUE_TYPE',
                'severity': 'CRITICAL',
                'message': f"Intent '{intent_name}' has invalid value type: {type(intent_value)}",
            })
        elif intent_value not in [0.0, 1.0, 0, 1]:
            issues.append({
                'type': 'NON_BINARY_VALUE',
                'severity': 'HIGH',
                'message': f"Intent '{intent_name}' has non-binary value: {intent_value} (should be 0.0 or 1.0)",
            })
    
    # 3. Check for empty intents
    if len(intents) == 0:
        issues.append({
            'type': 'EMPTY_INTENTS',
            'severity': 'MEDIUM',
            'message': "No intents specified",
        })
    
    # 4. Check intent names are valid (alphanumeric and underscores)
    for intent_name in intents.keys():
        if not re.match(r'^[A-Z][A-Z0-9_]*$', intent_name):
            issues.append({
                'type': 'INVALID_INTENT_NAME',
                'severity': 'HIGH',
                'message': f"Invalid intent name format: '{intent_name}' (should be UPPER_CASE_WITH_UNDERSCORES)",
            })
    
    return {
        'text': text,
        'intents': intents,
        'issues': issues,
        'is_valid': len(issues) == 0,
        'severity': max([i['severity'] for i in issues], default='NONE')
    }

def audit_entity_file(file_path: Path) -> Dict:
    """Audit a single entity file."""
    results = {
        'file': str(file_path),
        'total_examples': 0,
        'total_entities': 0,
        'valid_entities': 0,
        'invalid_entities': 0,
        'issues_by_type': defaultdict(int),
        'issues_by_severity': defaultdict(int),
        'entity_issues': [],
        'boundary_accuracy': 0.0,
        'label_accuracy': 0.0,
        'overall_accuracy': 0.0,
    }
    
    try:
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
                    
                    for start, end, label in entities:
                        check_result = check_entity_quality(text, start, end, label)
                        
                        if check_result['is_valid']:
                            results['valid_entities'] += 1
                        else:
                            results['invalid_entities'] += 1
                            for issue in check_result['issues']:
                                results['issues_by_type'][issue['type']] += 1
                                results['issues_by_severity'][issue['severity']] += 1
                            
                            results['entity_issues'].append({
                                'line': line_num,
                                'text_preview': text[:100] + '...' if len(text) > 100 else text,
                                **check_result
                            })
                
                except json.JSONDecodeError as e:
                    results['entity_issues'].append({
                        'line': line_num,
                        'type': 'JSON_DECODE_ERROR',
                        'severity': 'CRITICAL',
                        'message': f"JSON decode error: {e}",
                    })
                    results['issues_by_type']['JSON_DECODE_ERROR'] += 1
                    results['issues_by_severity']['CRITICAL'] += 1
                except Exception as e:
                    results['entity_issues'].append({
                        'line': line_num,
                        'type': 'PROCESSING_ERROR',
                        'severity': 'CRITICAL',
                        'message': f"Processing error: {e}",
                    })
                    results['issues_by_type']['PROCESSING_ERROR'] += 1
                    results['issues_by_severity']['CRITICAL'] += 1
        
        # Calculate accuracies
        if results['total_entities'] > 0:
            results['boundary_accuracy'] = (results['valid_entities'] / results['total_entities']) * 100
            results['label_accuracy'] = (results['valid_entities'] / results['total_entities']) * 100
            results['overall_accuracy'] = (results['valid_entities'] / results['total_entities']) * 100
    
    except Exception as e:
        results['error'] = str(e)
        results['overall_accuracy'] = 0.0
    
    return results

def audit_intent_file(file_path: Path) -> Dict:
    """Audit a single intent file."""
    results = {
        'file': str(file_path),
        'total_examples': 0,
        'valid_examples': 0,
        'invalid_examples': 0,
        'issues_by_type': defaultdict(int),
        'issues_by_severity': defaultdict(int),
        'intent_issues': [],
        'overall_accuracy': 0.0,
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                
                try:
                    data = json.loads(line)
                    text = data.get('text', '')
                    # Handle both 'intents' and 'cats' (spaCy format)
                    intents = data.get('intents', data.get('cats', {}))
                    
                    results['total_examples'] += 1
                    
                    check_result = check_intent_quality(text, intents)
                    
                    if check_result['is_valid']:
                        results['valid_examples'] += 1
                    else:
                        results['invalid_examples'] += 1
                        for issue in check_result['issues']:
                            results['issues_by_type'][issue['type']] += 1
                            results['issues_by_severity'][issue['severity']] += 1
                        
                        results['intent_issues'].append({
                            'line': line_num,
                            'text_preview': text[:100] + '...' if len(text) > 100 else text,
                            **check_result
                        })
                
                except json.JSONDecodeError as e:
                    results['intent_issues'].append({
                        'line': line_num,
                        'type': 'JSON_DECODE_ERROR',
                        'severity': 'CRITICAL',
                        'message': f"JSON decode error: {e}",
                    })
                    results['issues_by_type']['JSON_DECODE_ERROR'] += 1
                    results['issues_by_severity']['CRITICAL'] += 1
                except Exception as e:
                    results['intent_issues'].append({
                        'line': line_num,
                        'type': 'PROCESSING_ERROR',
                        'severity': 'CRITICAL',
                        'message': f"Processing error: {e}",
                    })
                    results['issues_by_type']['PROCESSING_ERROR'] += 1
                    results['issues_by_severity']['CRITICAL'] += 1
        
        # Calculate accuracy
        if results['total_examples'] > 0:
            results['overall_accuracy'] = (results['valid_examples'] / results['total_examples']) * 100
    
    except Exception as e:
        results['error'] = str(e)
        results['overall_accuracy'] = 0.0
    
    return results

def main():
    """Main audit function."""
    base_dir = Path('cyber-train/entities-intent')
    if not base_dir.exists():
        base_dir = Path('entities-intent')
    
    entity_files = list(base_dir.rglob('*_entities.jsonl'))
    intent_files = list(base_dir.rglob('*_intent.jsonl'))
    
    print("="*80)
    print("COMPREHENSIVE QUALITY AUDIT - PRODUCTION QUALITY ANALYSIS")
    print("="*80)
    print(f"\nFound {len(entity_files)} entity files and {len(intent_files)} intent files\n")
    
    # Audit entity files
    entity_results = []
    for file_path in sorted(entity_files):
        print(f"Auditing entity file: {file_path.name}...", end=' ', flush=True)
        result = audit_entity_file(file_path)
        entity_results.append(result)
        print(f"✅ {result['overall_accuracy']:.2f}% accuracy")
    
    # Audit intent files
    intent_results = []
    for file_path in sorted(intent_files):
        print(f"Auditing intent file: {file_path.name}...", end=' ', flush=True)
        result = audit_intent_file(file_path)
        intent_results.append(result)
        print(f"✅ {result['overall_accuracy']:.2f}% accuracy")
    
    # Generate comprehensive report
    print("\n" + "="*80)
    print("GENERATING DETAILED REPORT")
    print("="*80)
    
    # Save detailed JSON report
    report = {
        'entity_files': entity_results,
        'intent_files': intent_results,
        'summary': {
            'total_entity_files': len(entity_results),
            'total_intent_files': len(intent_results),
            'total_entity_examples': sum(r['total_examples'] for r in entity_results),
            'total_entity_entities': sum(r['total_entities'] for r in entity_results),
            'total_valid_entities': sum(r['valid_entities'] for r in entity_results),
            'total_invalid_entities': sum(r['invalid_entities'] for r in entity_results),
            'total_intent_examples': sum(r['total_examples'] for r in intent_results),
            'total_valid_intents': sum(r['valid_examples'] for r in intent_results),
            'total_invalid_intents': sum(r['invalid_examples'] for r in intent_results),
        }
    }
    
    # Calculate overall accuracies
    if report['summary']['total_entity_entities'] > 0:
        report['summary']['overall_entity_accuracy'] = (
            report['summary']['total_valid_entities'] / report['summary']['total_entity_entities']
        ) * 100
    else:
        report['summary']['overall_entity_accuracy'] = 0.0
    
    if report['summary']['total_intent_examples'] > 0:
        report['summary']['overall_intent_accuracy'] = (
            report['summary']['total_valid_intents'] / report['summary']['total_intent_examples']
        ) * 100
    else:
        report['summary']['overall_intent_accuracy'] = 0.0
    
    # Save JSON report
    json_report_path = Path('cyber-train/COMPREHENSIVE_QUALITY_AUDIT_REPORT.json')
    with open(json_report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Generate markdown report
    md_report = generate_markdown_report(report)
    md_report_path = Path('cyber-train/COMPREHENSIVE_QUALITY_AUDIT_REPORT.md')
    with open(md_report_path, 'w', encoding='utf-8') as f:
        f.write(md_report)
    
    print(f"\n✅ Detailed JSON report saved to: {json_report_path}")
    print(f"✅ Detailed Markdown report saved to: {md_report_path}")
    
    # Print summary
    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)
    print(f"\nEntity Files: {report['summary']['total_entity_files']}")
    print(f"  Total Examples: {report['summary']['total_entity_examples']:,}")
    print(f"  Total Entities: {report['summary']['total_entity_entities']:,}")
    print(f"  Valid Entities: {report['summary']['total_valid_entities']:,}")
    print(f"  Invalid Entities: {report['summary']['total_invalid_entities']:,}")
    print(f"  Overall Accuracy: {report['summary']['overall_entity_accuracy']:.2f}%")
    
    print(f"\nIntent Files: {report['summary']['total_intent_files']}")
    print(f"  Total Examples: {report['summary']['total_intent_examples']:,}")
    print(f"  Valid Examples: {report['summary']['total_valid_intents']:,}")
    print(f"  Invalid Examples: {report['summary']['total_invalid_intents']:,}")
    print(f"  Overall Accuracy: {report['summary']['overall_intent_accuracy']:.2f}%")

def generate_markdown_report(report: Dict) -> str:
    """Generate detailed markdown report."""
    md = []
    md.append("# Comprehensive Quality Audit Report")
    md.append("\n**Date:** Production Quality Analysis")
    md.append("\n---\n")
    
    # Summary
    md.append("## Executive Summary\n")
    summary = report['summary']
    md.append(f"- **Total Entity Files:** {summary['total_entity_files']}")
    md.append(f"- **Total Intent Files:** {summary['total_intent_files']}")
    md.append(f"- **Total Entity Examples:** {summary['total_entity_examples']:,}")
    md.append(f"- **Total Entities:** {summary['total_entity_entities']:,}")
    md.append(f"- **Valid Entities:** {summary['total_valid_entities']:,}")
    md.append(f"- **Invalid Entities:** {summary['total_invalid_entities']:,}")
    md.append(f"- **Overall Entity Accuracy:** {summary['overall_entity_accuracy']:.2f}%")
    md.append(f"- **Total Intent Examples:** {summary['total_intent_examples']:,}")
    md.append(f"- **Valid Intent Examples:** {summary['total_valid_intents']:,}")
    md.append(f"- **Invalid Intent Examples:** {summary['total_invalid_intents']:,}")
    md.append(f"- **Overall Intent Accuracy:** {summary['overall_intent_accuracy']:.2f}%")
    
    # Entity files detailed
    md.append("\n## Entity Files - Detailed Analysis\n")
    for result in sorted(report['entity_files'], key=lambda x: x['overall_accuracy']):
        filename = Path(result['file']).name
        md.append(f"\n### {filename}\n")
        md.append(f"- **Total Examples:** {result['total_examples']:,}")
        md.append(f"- **Total Entities:** {result['total_entities']:,}")
        md.append(f"- **Valid Entities:** {result['valid_entities']:,}")
        md.append(f"- **Invalid Entities:** {result['invalid_entities']:,}")
        md.append(f"- **Boundary Accuracy:** {result['boundary_accuracy']:.2f}%")
        md.append(f"- **Label Accuracy:** {result['label_accuracy']:.2f}%")
        md.append(f"- **Overall Accuracy:** {result['overall_accuracy']:.2f}%")
        
        if result['issues_by_type']:
            md.append(f"\n**Issues by Type:**")
            for issue_type, count in sorted(result['issues_by_type'].items(), key=lambda x: x[1], reverse=True):
                md.append(f"  - {issue_type}: {count}")
        
        if result['issues_by_severity']:
            md.append(f"\n**Issues by Severity:**")
            for severity, count in sorted(result['issues_by_severity'].items(), key=lambda x: x[1], reverse=True):
                md.append(f"  - {severity}: {count}")
    
    # Intent files detailed
    md.append("\n## Intent Files - Detailed Analysis\n")
    for result in sorted(report['intent_files'], key=lambda x: x['overall_accuracy']):
        filename = Path(result['file']).name
        md.append(f"\n### {filename}\n")
        md.append(f"- **Total Examples:** {result['total_examples']:,}")
        md.append(f"- **Valid Examples:** {result['valid_examples']:,}")
        md.append(f"- **Invalid Examples:** {result['invalid_examples']:,}")
        md.append(f"- **Overall Accuracy:** {result['overall_accuracy']:.2f}%")
        
        if result['issues_by_type']:
            md.append(f"\n**Issues by Type:**")
            for issue_type, count in sorted(result['issues_by_type'].items(), key=lambda x: x[1], reverse=True):
                md.append(f"  - {issue_type}: {count}")
    
    return '\n'.join(md)

if __name__ == '__main__':
    main()

