#!/usr/bin/env python3
"""Test script to verify OSINT scenario processing works."""
import sys
import json
import os
sys.path.insert(0, '.')

print("=" * 70)
print("OSINT Scenario Processing Test")
print("=" * 70)

try:
    from create_osint_from_scenarios import (
        load_scenario_file,
        process_pillar_from_scenarios,
        OSINT_PILLARS
    )
    
    # Test one pillar
    test_pillar = 'socmint'
    print(f"\n1. Testing with pillar: {test_pillar}")
    
    # Load scenario
    print("   Loading scenario file...")
    scenarios_data = load_scenario_file(test_pillar)
    if scenarios_data:
        print(f"   ✓ Loaded {len(scenarios_data.get('scenarios', []))} scenarios")
    else:
        print("   ✗ Failed to load scenario file")
        sys.exit(1)
    
    # Process pillar
    print("   Processing pillar...")
    result = process_pillar_from_scenarios(test_pillar)
    print(f"   Result: {result}")
    
    # Check output
    entities_file = f'cyber-train/entities-intent/osint/{test_pillar}/{test_pillar}_entities.jsonl'
    intents_file = f'cyber-train/entities-intent/osint/{test_pillar}/{test_pillar}_intent.jsonl'
    
    if os.path.exists(entities_file):
        with open(entities_file) as f:
            entity_count = len(f.readlines())
        print(f"   ✓ Entities file: {entity_count} lines")
    else:
        print(f"   ✗ Entities file not found")
    
    if os.path.exists(intents_file):
        with open(intents_file) as f:
            intent_count = len(f.readlines())
        print(f"   ✓ Intents file: {intent_count} lines")
    else:
        print(f"   ✗ Intents file not found")
    
    print("\n" + "=" * 70)
    print("Test completed!")
    print("=" * 70)
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

