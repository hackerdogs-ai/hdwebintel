#!/usr/bin/env python3
"""
Comprehensive verification script to find ALL remaining boundary and labeling issues.
This script checks:
1. Wrong boundaries (IPs, domains, CVEs, emails that don't match patterns)
2. Common words still labeled as entities
3. Partial words still labeled as entities
4. Entities that don't match their expected patterns
5. Boundary validation (start/end positions)
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

# Patterns for validation
IP_PATTERN = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?[\d\s\-\(\)]{10,}\b')
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
URL_PATTERN = re.compile(r'https?://[^\s]+|www\.[^\s]+', re.IGNORECASE)

# Common words that should NEVER be entities
COMMON_WORDS_NEVER_ENTITIES = {
    'ai', 'security', 'incident', 'escalation', 'rate', 'maintained', 'at', 'below', 'threshold',
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
    'report', 'tool', 'type', 'count', 'metric', 'value', 'model', 'attack',
    'response', 'coordination', 'team', 'teams', 'platform', 'feeds', 'provided',
    'including', 'hashes', 'infrastructure', 'review', 'repository', 'branch', 'commit',
    'contains', 'configuration', 'source', 'code', 'audit', 'needed', 'detected',
    'against', 'using', 'techniques', 'coordinated', 'across', 'engineering', 'legal',
    'validated', 'mapped', 'controls', 'function', 'covering', 'objectives', 'processing',
    'consumer', 'facilitated', 'during', 'breach', 'confirmed', 'explanations', 'met',
    'interpretability', 'medical', 'automated', 'testing', 'pipeline', 'executed', 'cases',
    'pass', 'validated', 'bias', 'metrics', 'fairness', 'found', 'gender', 'outputs',
    'filtered', 'inappropriate', 'content', 'validated', 'controls', 'remediation', 'completed',
    'issues', 'within', 'sla', 'enforced', 'filtering', 'blocking', 'toxic',
    'ma', 'rat', 'ed', 'at', 'securit', 'inciden', 'escalat', 'maintain'
}

# Problematic labels for common words
PROBLEMATIC_LABELS = {
    'AI_MODEL_TYPE', 'SECURITY_TYPE', 'INCIDENT_TYPE', 'METRIC_TYPE', 'THRESHOLD_TYPE',
    'TOOL', 'TIME_UNIT', 'PRIORITIZATION_TYPE', 'SERVICE', 'SOURCE_TYPE',
    'ENCRYPTION_TYPE', 'VULNERABILITY_ID', 'TRAINING_TYPE', 'INTEGRATION_TYPE',
    'BRANCH', 'COMMIT', 'QUERY_TYPE', 'REQUIREMENT_TYPE'
}

# Pattern validation by entity type
PATTERN_VALIDATION = {
    'IP_ADDRESS': IP_PATTERN,
    'DOMAIN': DOMAIN_PATTERN,
    'CVE_ID': CVE_PATTERN,
    'EMAIL': EMAIL_PATTERN,
    'EMAIL_ADDRESS': EMAIL_PATTERN,
    'PHONE_NUMBER': PHONE_PATTERN,
    'SSN': SSN_PATTERN,
    'CREDIT_CARD_NUMBER': CREDIT_CARD_PATTERN,
    'WALLET_ADDRESS': WALLET_PATTERN,
    'URL': URL_PATTERN,
}


def check_entity(text: str, start: int, end: int, label: str) -> List[Dict]:
    """Check a single entity for issues."""
    issues = []
    
    # Validate boundaries
    if start < 0 or end > len(text) or start >= end:
        issues.append({
            'type': 'INVALID_BOUNDARY',
            'message': f'Invalid boundary: start={start}, end={end}, text_length={len(text)}',
            'entity_text': text[max(0, start):min(end, len(text))] if start < len(text) else '',
            'label': label
        })
        return issues
    
    entity_text = text[start:end]
    entity_lower = entity_text.lower().strip()
    
    # Check if it's a common word
    if entity_lower in COMMON_WORDS_NEVER_ENTITIES:
        issues.append({
            'type': 'COMMON_WORD',
            'message': f'Common word labeled as entity: "{entity_text}"',
            'entity_text': entity_text,
            'label': label
        })
    
    # Check if it's a partial word (substring of common word)
    for common_word in COMMON_WORDS_NEVER_ENTITIES:
        if entity_lower in common_word and len(entity_lower) < len(common_word) and len(entity_lower) <= 5:
            issues.append({
                'type': 'PARTIAL_WORD',
                'message': f'Partial word "{entity_text}" (from "{common_word}")',
                'entity_text': entity_text,
                'label': label,
                'parent_word': common_word
            })
            break
    
    # Check problematic labels
    if label in PROBLEMATIC_LABELS:
        if entity_lower in COMMON_WORDS_NEVER_ENTITIES or len(entity_lower) <= 5:
            issues.append({
                'type': 'PROBLEMATIC_LABEL',
                'message': f'Problematic label {label} for "{entity_text}"',
                'entity_text': entity_text,
                'label': label
            })
    
    # Check pattern validation
    if label in PATTERN_VALIDATION:
        pattern = PATTERN_VALIDATION[label]
        if not pattern.match(entity_text):
            # Find what should be there
            matches = list(pattern.finditer(text))
            if matches:
                expected = matches[0].group()
                expected_start = matches[0].start()
                expected_end = matches[0].end()
                issues.append({
                    'type': 'WRONG_BOUNDARY',
                    'message': f'Wrong boundary: got "{entity_text}" (pos {start}-{end}), expected "{expected}" (pos {expected_start}-{expected_end})',
                    'entity_text': entity_text,
                    'expected_text': expected,
                    'label': label,
                    'got_pos': f'{start}-{end}',
                    'expected_pos': f'{expected_start}-{expected_end}'
                })
            else:
                issues.append({
                    'type': 'INVALID_PATTERN',
                    'message': f'Entity "{entity_text}" does not match pattern for {label}',
                    'entity_text': entity_text,
                    'label': label
                })
    
    # Check for entities with leading/trailing spaces
    if entity_text != entity_text.strip():
        issues.append({
            'type': 'WHITESPACE',
            'message': f'Entity has leading/trailing whitespace: "{entity_text}"',
            'entity_text': entity_text,
            'label': label
        })
    
    # Check for very short entities (likely false positives)
    if len(entity_text.strip()) <= 2 and label not in ['IP_ADDRESS', 'DOMAIN', 'CVE_ID']:
        issues.append({
            'type': 'TOO_SHORT',
            'message': f'Entity too short: "{entity_text}"',
            'entity_text': entity_text,
            'label': label
        })
    
    return issues


def verify_file(file_path: Path) -> Dict:
    """Verify all entities in a file."""
    stats = {
        'file': str(file_path),
        'total_lines': 0,
        'total_entities': 0,
        'issues': [],
        'issues_by_type': defaultdict(int),
        'issues_by_label': defaultdict(int)
    }
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            stats['total_lines'] += 1
            try:
                data = json.loads(line)
                text = data.get('text', '')
                entities = data.get('entities', [])
                stats['total_entities'] += len(entities)
                
                for start, end, label in entities:
                    issues = check_entity(text, start, end, label)
                    for issue in issues:
                        issue['line'] = line_num
                        issue['text_preview'] = text[:100] if len(text) > 100 else text
                        stats['issues'].append(issue)
                        stats['issues_by_type'][issue['type']] += 1
                        stats['issues_by_label'][label] += 1
                        
            except Exception as e:
                stats['issues'].append({
                    'type': 'PARSE_ERROR',
                    'message': f'Error parsing line {line_num}: {e}',
                    'line': line_num
                })
                stats['issues_by_type']['PARSE_ERROR'] += 1
    
    return stats


def main():
    base_dir = Path("cyber-train/entities-intent")
    entity_files = sorted(list(base_dir.rglob("*_entities.jsonl")))
    
    print("="*70)
    print("COMPREHENSIVE BOUNDARY VERIFICATION")
    print("="*70)
    print(f"\nFiles to verify: {len(entity_files)}")
    
    all_stats = []
    total_issues = 0
    
    for file_path in entity_files:
        print(f"\n📄 Verifying: {file_path.relative_to(base_dir)}")
        stats = verify_file(file_path)
        all_stats.append(stats)
        
        if stats['issues']:
            print(f"   ⚠️  Found {len(stats['issues'])} issues")
            total_issues += len(stats['issues'])
            
            # Show top issue types
            top_types = sorted(stats['issues_by_type'].items(), key=lambda x: x[1], reverse=True)[:5]
            for issue_type, count in top_types:
                print(f"      • {issue_type}: {count}")
        else:
            print(f"   ✅ No issues found")
    
    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    print(f"Total files: {len(entity_files)}")
    print(f"Total lines: {sum(s['total_lines'] for s in all_stats):,}")
    print(f"Total entities: {sum(s['total_entities'] for s in all_stats):,}")
    print(f"Total issues: {total_issues:,}")
    
    if total_issues > 0:
        print(f"\n⚠️  ISSUES FOUND - Details below")
        print("-"*70)
        
        # Aggregate by type
        all_issues_by_type = defaultdict(int)
        for stats in all_stats:
            for issue_type, count in stats['issues_by_type'].items():
                all_issues_by_type[issue_type] += count
        
        print("\nIssues by type:")
        for issue_type, count in sorted(all_issues_by_type.items(), key=lambda x: x[1], reverse=True):
            print(f"  {issue_type:30s}: {count:6,}")
        
        # Files with most issues
        files_with_issues = [(s['file'], len(s['issues'])) for s in all_stats if s['issues']]
        files_with_issues.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\nTop 10 files with issues:")
        for file_path, count in files_with_issues[:10]:
            print(f"  {Path(file_path).name:50s}: {count:6,} issues")
        
        # Save detailed report
        report_file = Path("cyber-train/BOUNDARY_VERIFICATION_REPORT.json")
        with open(report_file, 'w') as f:
            json.dump({
                'summary': {
                    'total_files': len(entity_files),
                    'total_lines': sum(s['total_lines'] for s in all_stats),
                    'total_entities': sum(s['total_entities'] for s in all_stats),
                    'total_issues': total_issues,
                    'issues_by_type': dict(all_issues_by_type)
                },
                'files': all_stats
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Show sample issues
        print(f"\n📋 Sample Issues (first 10):")
        print("-"*70)
        sample_count = 0
        for stats in all_stats:
            if stats['issues'] and sample_count < 10:
                for issue in stats['issues'][:3]:
                    print(f"\n  File: {Path(stats['file']).name}")
                    print(f"  Line: {issue.get('line', 'N/A')}")
                    print(f"  Type: {issue['type']}")
                    print(f"  Message: {issue['message']}")
                    if 'entity_text' in issue:
                        print(f"  Entity: '{issue['entity_text']}'")
                    if 'expected_text' in issue:
                        print(f"  Expected: '{issue['expected_text']}'")
                    sample_count += 1
                    if sample_count >= 10:
                        break
            if sample_count >= 10:
                break
    else:
        print(f"\n✅ NO ISSUES FOUND - All boundaries are correct!")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()

