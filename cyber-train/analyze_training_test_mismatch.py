#!/usr/bin/env python3
"""
Analyze Training vs Test Suite Pattern Mismatches

This script compares training data patterns with test suite patterns
to identify why the model performs well on training but poorly on test suite.
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple

def load_training_data(base_dir: Path) -> Dict[str, List[Dict]]:
    """Load all training data from JSONL files."""
    training_patterns = defaultdict(list)
    
    # Key entity files to analyze
    key_files = [
        "osint/socmint/socmint_entities.jsonl",
        "threat_intelligence/threat_intel_entities.jsonl",
        "network_security/network_security_entities.jsonl",
        "incident_response/incident_response_entities.jsonl",
        "osint/geoint/geoint_entities.jsonl",
        "data_privacy/data_privacy_entities.jsonl",
        "ai_security/ai_security_entities.jsonl",
        "audit_compliance/audit_compliance_entities.jsonl",
    ]
    
    for file_path in key_files:
        full_path = base_dir / file_path
        if not full_path.exists():
            continue
        
        with open(full_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    text = data.get('text', '')
                    entities = data.get('entities', [])
                    
                    for entity in entities:
                        if len(entity) >= 3:
                            start, end, label = entity[0], entity[1], entity[2]
                            entity_text = text[start:end]
                            training_patterns[label].append({
                                'entity': entity_text,
                                'context': text,
                                'context_before': text[max(0, start-50):start],
                                'context_after': text[end:min(len(text), end+50)],
                                'position': start,
                                'file': file_path
                            })
                except json.JSONDecodeError:
                    continue
    
    return dict(training_patterns)

def load_test_suite_patterns() -> Dict[str, List[Dict]]:
    """Load test suite patterns from comprehensive_test_results.json."""
    with open('comprehensive_test_results.json', 'r') as f:
        results = json.load(f)
    
    test_patterns = defaultdict(list)
    missed_patterns = defaultdict(list)
    
    for test in results.get('test_cases', []):
        text = test.get('text', '')
        expected = test.get('expected_entities', [])
        found = test.get('entities', [])
        category = test.get('category', '')
        
        # Convert to sets
        expected_set = set()
        for e in expected:
            if isinstance(e, list):
                expected_set.add((e[0], e[1]))
            elif isinstance(e, tuple):
                expected_set.add(e)
        
        found_set = set()
        for e in found:
            if isinstance(e, list):
                found_set.add((e[0], e[1]))
            elif isinstance(e, tuple):
                found_set.add(e)
        
        # All expected entities (for pattern analysis)
        for entity_text, entity_type in expected_set:
            entity_pos = text.find(entity_text)
            if entity_pos != -1:
                test_patterns[entity_type].append({
                    'entity': entity_text,
                    'context': text,
                    'context_before': text[max(0, entity_pos-50):entity_pos],
                    'context_after': text[entity_pos+len(entity_text):min(len(text), entity_pos+len(entity_text)+50)],
                    'position': entity_pos,
                    'category': category,
                    'found': (entity_text, entity_type) in found_set
                })
        
        # Missed entities
        missed = expected_set - found_set
        for entity_text, entity_type in missed:
            entity_pos = text.find(entity_text)
            if entity_pos != -1:
                missed_patterns[entity_type].append({
                    'entity': entity_text,
                    'context': text,
                    'context_before': text[max(0, entity_pos-50):entity_pos],
                    'context_after': text[entity_pos+len(entity_text):min(len(text), entity_pos+len(entity_text)+50)],
                    'position': entity_pos,
                    'category': category
                })
    
    return dict(test_patterns), dict(missed_patterns)

def analyze_pattern_differences(training: Dict[str, List[Dict]], 
                                test_suite: Dict[str, List[Dict]],
                                missed: Dict[str, List[Dict]]) -> Dict:
    """Analyze differences between training and test suite patterns."""
    
    analysis = {
        'entity_types': {},
        'context_patterns': {},
        'format_differences': {},
        'length_differences': {},
        'surrounding_text': {}
    }
    
    # Analyze each entity type
    all_types = set(training.keys()) | set(test_suite.keys()) | set(missed.keys())
    
    for entity_type in sorted(all_types):
        train_examples = training.get(entity_type, [])
        test_examples = test_suite.get(entity_type, [])
        missed_examples = missed.get(entity_type, [])
        
        if not train_examples and not test_examples:
            continue
        
        # Entity format analysis
        train_formats = Counter()
        test_formats = Counter()
        missed_formats = Counter()
        
        for ex in train_examples:
            entity = ex['entity']
            # Classify format
            if re.match(r'^[\d\.]+$', entity):
                train_formats['numeric'] += 1
            elif re.match(r'^[a-zA-Z0-9\.\-]+$', entity):
                train_formats['alphanumeric'] += 1
            elif re.match(r'^[^\w\s]+$', entity):
                train_formats['symbols_only'] += 1
            else:
                train_formats['mixed'] += 1
        
        for ex in test_examples:
            entity = ex['entity']
            if re.match(r'^[\d\.]+$', entity):
                test_formats['numeric'] += 1
            elif re.match(r'^[a-zA-Z0-9\.\-]+$', entity):
                test_formats['alphanumeric'] += 1
            elif re.match(r'^[^\w\s]+$', entity):
                test_formats['symbols_only'] += 1
            else:
                test_formats['mixed'] += 1
        
        for ex in missed_examples:
            entity = ex['entity']
            if re.match(r'^[\d\.]+$', entity):
                missed_formats['numeric'] += 1
            elif re.match(r'^[a-zA-Z0-9\.\-]+$', entity):
                missed_formats['alphanumeric'] += 1
            elif re.match(r'^[^\w\s]+$', entity):
                missed_formats['symbols_only'] += 1
            else:
                missed_formats['mixed'] += 1
        
        # Context length analysis
        train_context_lengths = [len(ex['context']) for ex in train_examples]
        test_context_lengths = [len(ex['context']) for ex in test_examples]
        missed_context_lengths = [len(ex['context']) for ex in missed_examples]
        
        # Entity length analysis
        train_entity_lengths = [len(ex['entity']) for ex in train_examples]
        test_entity_lengths = [len(ex['entity']) for ex in test_examples]
        missed_entity_lengths = [len(ex['entity']) for ex in missed_examples]
        
        # Surrounding text patterns
        train_before_patterns = Counter()
        train_after_patterns = Counter()
        test_before_patterns = Counter()
        test_after_patterns = Counter()
        missed_before_patterns = Counter()
        missed_after_patterns = Counter()
        
        for ex in train_examples[:100]:  # Sample
            before = ex['context_before'].strip()[-20:] if ex['context_before'] else ''
            after = ex['context_after'].strip()[:20] if ex['context_after'] else ''
            if before:
                train_before_patterns[before] += 1
            if after:
                train_after_patterns[after] += 1
        
        for ex in test_examples:
            before = ex['context_before'].strip()[-20:] if ex['context_before'] else ''
            after = ex['context_after'].strip()[:20] if ex['context_after'] else ''
            if before:
                test_before_patterns[before] += 1
            if after:
                test_after_patterns[after] += 1
        
        for ex in missed_examples:
            before = ex['context_before'].strip()[-20:] if ex['context_before'] else ''
            after = ex['context_after'].strip()[:20] if ex['context_after'] else ''
            if before:
                missed_before_patterns[before] += 1
            if after:
                missed_after_patterns[after] += 1
        
        analysis['entity_types'][entity_type] = {
            'training_count': len(train_examples),
            'test_suite_count': len(test_examples),
            'missed_count': len(missed_examples),
            'miss_rate': len(missed_examples) / len(test_examples) * 100 if test_examples else 0,
            'formats': {
                'training': dict(train_formats),
                'test_suite': dict(test_formats),
                'missed': dict(missed_formats)
            },
            'context_length': {
                'training_avg': sum(train_context_lengths) / len(train_context_lengths) if train_context_lengths else 0,
                'test_avg': sum(test_context_lengths) / len(test_context_lengths) if test_context_lengths else 0,
                'missed_avg': sum(missed_context_lengths) / len(missed_context_lengths) if missed_context_lengths else 0
            },
            'entity_length': {
                'training_avg': sum(train_entity_lengths) / len(train_entity_lengths) if train_entity_lengths else 0,
                'test_avg': sum(test_entity_lengths) / len(test_entity_lengths) if test_entity_lengths else 0,
                'missed_avg': sum(missed_entity_lengths) / len(missed_entity_lengths) if missed_entity_lengths else 0
            },
            'top_before_patterns': {
                'training': dict(train_before_patterns.most_common(5)),
                'test_suite': dict(test_before_patterns.most_common(5)),
                'missed': dict(missed_before_patterns.most_common(5))
            },
            'top_after_patterns': {
                'training': dict(train_after_patterns.most_common(5)),
                'test_suite': dict(test_after_patterns.most_common(5)),
                'missed': dict(missed_after_patterns.most_common(5))
            }
        }
    
    return analysis

def generate_report(analysis: Dict, output_file: str):
    """Generate a comprehensive mismatch report."""
    
    report = []
    report.append("="*80)
    report.append("TRAINING vs TEST SUITE PATTERN MISMATCH ANALYSIS")
    report.append("="*80)
    report.append("")
    report.append("This report identifies specific mismatches between training data")
    report.append("patterns and test suite patterns that explain the performance gap.")
    report.append("")
    
    # Sort by miss rate
    sorted_types = sorted(
        analysis['entity_types'].items(),
        key=lambda x: x[1]['miss_rate'],
        reverse=True
    )
    
    report.append("="*80)
    report.append("TOP MISMATCHED ENTITY TYPES (by miss rate)")
    report.append("="*80)
    report.append("")
    
    for entity_type, data in sorted_types[:15]:
        if data['miss_rate'] == 0:
            continue
        
        report.append(f"\n{entity_type}")
        report.append("-" * 80)
        report.append(f"  Training Examples: {data['training_count']}")
        report.append(f"  Test Suite Examples: {data['test_suite_count']}")
        report.append(f"  Missed: {data['missed_count']} ({data['miss_rate']:.1f}% miss rate)")
        report.append("")
        
        # Format differences
        train_fmts = data['formats']['training']
        test_fmts = data['formats']['test_suite']
        missed_fmts = data['formats']['missed']
        
        if train_fmts != test_fmts:
            report.append("  ⚠️  FORMAT MISMATCH:")
            report.append(f"     Training formats: {train_fmts}")
            report.append(f"     Test suite formats: {test_fmts}")
            report.append(f"     Missed formats: {missed_fmts}")
            report.append("")
        
        # Context length differences
        train_ctx = data['context_length']['training_avg']
        test_ctx = data['context_length']['test_avg']
        missed_ctx = data['context_length']['missed_avg']
        
        if abs(train_ctx - test_ctx) > 50:
            report.append("  ⚠️  CONTEXT LENGTH MISMATCH:")
            report.append(f"     Training avg context: {train_ctx:.1f} chars")
            report.append(f"     Test suite avg context: {test_ctx:.1f} chars")
            report.append(f"     Missed avg context: {missed_ctx:.1f} chars")
            report.append(f"     Difference: {abs(train_ctx - test_ctx):.1f} chars")
            report.append("")
        
        # Entity length differences
        train_ent = data['entity_length']['training_avg']
        test_ent = data['entity_length']['test_avg']
        missed_ent = data['entity_length']['missed_avg']
        
        if abs(train_ent - test_ent) > 5:
            report.append("  ⚠️  ENTITY LENGTH MISMATCH:")
            report.append(f"     Training avg entity: {train_ent:.1f} chars")
            report.append(f"     Test suite avg entity: {test_ent:.1f} chars")
            report.append(f"     Missed avg entity: {missed_ent:.1f} chars")
            report.append("")
        
        # Surrounding text patterns
        train_before = data['top_before_patterns']['training']
        test_before = data['top_before_patterns']['test_suite']
        missed_before = data['top_before_patterns']['missed']
        
        if train_before and test_before:
            train_keys = set(train_before.keys())
            test_keys = set(test_before.keys())
            missed_keys = set(missed_before.keys())
            
            if not train_keys.intersection(test_keys):
                report.append("  ⚠️  SURROUNDING TEXT MISMATCH (BEFORE):")
                report.append(f"     Training patterns: {list(train_keys)[:3]}")
                report.append(f"     Test suite patterns: {list(test_keys)[:3]}")
                report.append(f"     Missed patterns: {list(missed_keys)[:3]}")
                report.append("")
        
        train_after = data['top_after_patterns']['training']
        test_after = data['top_after_patterns']['test_suite']
        missed_after = data['top_after_patterns']['missed']
        
        if train_after and test_after:
            train_keys = set(train_after.keys())
            test_keys = set(test_after.keys())
            missed_keys = set(missed_after.keys())
            
            if not train_keys.intersection(test_keys):
                report.append("  ⚠️  SURROUNDING TEXT MISMATCH (AFTER):")
                report.append(f"     Training patterns: {list(train_keys)[:3]}")
                report.append(f"     Test suite patterns: {list(test_keys)[:3]}")
                report.append(f"     Missed patterns: {list(missed_keys)[:3]}")
                report.append("")
    
    # Summary
    report.append("")
    report.append("="*80)
    report.append("SUMMARY OF KEY MISMATCHES")
    report.append("="*80)
    report.append("")
    
    high_miss_rate = [t for t, d in sorted_types if d['miss_rate'] > 50]
    if high_miss_rate:
        report.append(f"Entity types with >50% miss rate: {', '.join(high_miss_rate)}")
        report.append("")
    
    format_mismatches = []
    context_mismatches = []
    pattern_mismatches = []
    
    for entity_type, data in sorted_types:
        if data['miss_rate'] == 0:
            continue
        
        if data['formats']['training'] != data['formats']['test_suite']:
            format_mismatches.append(entity_type)
        
        if abs(data['context_length']['training_avg'] - data['context_length']['test_avg']) > 50:
            context_mismatches.append(entity_type)
        
        train_before = set(data['top_before_patterns']['training'].keys())
        test_before = set(data['top_before_patterns']['test_suite'].keys())
        if train_before and test_before and not train_before.intersection(test_before):
            pattern_mismatches.append(entity_type)
    
    report.append(f"Format mismatches: {', '.join(format_mismatches[:10])}")
    report.append(f"Context length mismatches: {', '.join(context_mismatches[:10])}")
    report.append(f"Surrounding pattern mismatches: {', '.join(pattern_mismatches[:10])}")
    report.append("")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    # Also save JSON for detailed analysis
    json_file = output_file.replace('.txt', '.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Report saved to: {output_file}")
    print(f"✅ Detailed JSON saved to: {json_file}")

def main():
    """Main analysis function."""
    print("Loading training data...")
    base_dir = Path("entities-intent")
    training_patterns = load_training_data(base_dir)
    print(f"Loaded {sum(len(v) for v in training_patterns.values())} training examples")
    print(f"Entity types in training: {len(training_patterns)}")
    
    print("\nLoading test suite patterns...")
    test_patterns, missed_patterns = load_test_suite_patterns()
    print(f"Loaded {sum(len(v) for v in test_patterns.values())} test suite examples")
    print(f"Entity types in test suite: {len(test_patterns)}")
    print(f"Missed examples: {sum(len(v) for v in missed_patterns.values())}")
    
    print("\nAnalyzing pattern differences...")
    analysis = analyze_pattern_differences(training_patterns, test_patterns, missed_patterns)
    
    print("\nGenerating report...")
    generate_report(analysis, "TRAINING_TEST_MISMATCH_REPORT.txt")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()

