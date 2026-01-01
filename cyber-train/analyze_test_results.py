#!/usr/bin/env python3
"""Quick script to analyze comprehensive test results and calculate metrics."""

import json
from pathlib import Path

def analyze_results(results_file):
    """Analyze test results and calculate precision, recall, F1."""
    
    with open(results_file) as f:
        data = json.load(f)
    
    # Count entities
    total_found = 0
    total_expected = 0
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    
    for test_case in data.get('test_cases', []):
        entities_found = set((e[0], e[1]) for e in test_case.get('entities', []))
        entities_expected = set((e[0], e[1]) for e in test_case.get('expected_entities', []))
        
        total_found += len(entities_found)
        total_expected += len(entities_expected)
        
        # True positives: found and expected
        tp = entities_found & entities_expected
        true_positives += len(tp)
        
        # False positives: found but not expected
        fp = entities_found - entities_expected
        false_positives += len(fp)
        
        # False negatives: expected but not found
        fn = entities_expected - entities_found
        false_negatives += len(fn)
    
    # Calculate metrics
    precision = true_positives / total_found if total_found > 0 else 0
    recall = true_positives / total_expected if total_expected > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    print("="*70)
    print("COMPREHENSIVE TEST RESULTS ANALYSIS")
    print("="*70)
    print()
    print(f"📊 Entity Detection Metrics:")
    print(f"   Total entities found:    {total_found}")
    print(f"   Total entities expected: {total_expected}")
    print(f"   True Positives:          {true_positives}")
    print(f"   False Positives:         {false_positives}")
    print(f"   False Negatives:         {false_negatives}")
    print()
    print(f"📈 Performance Metrics:")
    print(f"   Precision:  {precision*100:.2f}%")
    print(f"   Recall:     {recall*100:.2f}%")
    print(f"   F1 Score:   {f1*100:.2f}%")
    print()
    print("="*70)
    print()
    
    # Compare with baseline
    baseline_recall = 41.52
    baseline_precision = 84.57
    baseline_f1 = 55.69
    
    recall_change = recall*100 - baseline_recall
    precision_change = precision*100 - baseline_precision
    f1_change = f1*100 - baseline_f1
    
    print("📊 Comparison with Baseline (Before Improvements):")
    print()
    print(f"   Metric      | Before   | After    | Change")
    print(f"   ------------|----------|----------|----------")
    print(f"   Precision   | {baseline_precision:.2f}%  | {precision*100:.2f}%  | {precision_change:+.2f}%")
    print(f"   Recall      | {baseline_recall:.2f}%  | {recall*100:.2f}%  | {recall_change:+.2f}%")
    print(f"   F1 Score    | {baseline_f1:.2f}%  | {f1*100:.2f}%  | {f1_change:+.2f}%")
    print()
    
    if recall*100 >= 60:
        print("✅ TARGET ACHIEVED! Recall >= 60%")
    elif recall*100 >= 50:
        print("⚠️  CLOSE TO TARGET. Recall >= 50%")
    else:
        print("❌ Target not met. Recall < 50%")
    print()
    print("="*70)

if __name__ == "__main__":
    analyze_results("/Users/tredkar/Documents/GitHub/hdwebintel/comprehensive_test_results.json")

