#!/usr/bin/env python3
"""Execute OSINT scenario-based generation with progress tracking."""
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '.')

try:
    from create_osint_from_scenarios import (
        OSINT_PILLARS, 
        process_pillar_from_scenarios,
        load_scenario_file
    )
    
    print(f"Generating OSINT entities and intents from scenario files...")
    print(f"Target: 500 entities and 500 intents per pillar\n")
    
    success_count = 0
    total_pillars = len(OSINT_PILLARS)
    
    for idx, pillar in enumerate(OSINT_PILLARS, 1):
        print(f"[{idx}/{total_pillars}] Processing {pillar}...", end=" ", flush=True)
        
        try:
            # Check if scenario file exists
            scenarios_data = load_scenario_file(pillar)
            if scenarios_data:
                print(f"Found {len(scenarios_data.get('scenarios', []))} scenarios", end=" ", flush=True)
            
            result = process_pillar_from_scenarios(pillar)
            
            if result:
                # Verify files were created
                pillar_dir = Path(f"cyber-train/entities-intent/osint/{pillar}")
                entities_file = pillar_dir / f"{pillar}_entities.jsonl"
                intents_file = pillar_dir / f"{pillar}_intent.jsonl"
                
                if entities_file.exists() and intents_file.exists():
                    with open(entities_file) as f:
                        entity_count = len(f.readlines())
                    with open(intents_file) as f:
                        intent_count = len(f.readlines())
                    print(f"✅ {entity_count} entities, {intent_count} intents")
                    success_count += 1
                else:
                    print(f"❌ Files not created")
            else:
                print(f"❌ Processing failed")
                
        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"Completed: {success_count}/{total_pillars} pillars")
    print(f"{'='*60}")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure create_osint_from_scenarios.py exists and is correct")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

