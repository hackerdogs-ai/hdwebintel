#!/usr/bin/env python3
"""Run OSINT scenario processing with detailed logging."""
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Redirect output to log file
log_file = '/tmp/osint_processing.log'
log = open(log_file, 'w')

def log_print(*args, **kwargs):
    """Print to both console and log file."""
    msg = ' '.join(str(arg) for arg in args)
    print(msg, **kwargs)
    log.write(msg + '\n')
    log.flush()

log_print("=" * 70)
log_print(f"OSINT Scenario Processing - Started at {datetime.now()}")
log_print("=" * 70)

try:
    sys.path.insert(0, '.')
    from create_osint_from_scenarios import (
        OSINT_PILLARS,
        process_pillar_from_scenarios,
        load_scenario_file
    )
    
    log_print(f"\nTotal pillars to process: {len(OSINT_PILLARS)}")
    log_print(f"Pillars: {', '.join(OSINT_PILLARS[:5])}...")
    
    success_count = 0
    
    for idx, pillar in enumerate(OSINT_PILLARS, 1):
        log_print(f"\n[{idx}/{len(OSINT_PILLARS)}] Processing {pillar}...")
        
        try:
            # Check scenario file
            scenarios_data = load_scenario_file(pillar)
            if scenarios_data:
                scenario_count = len(scenarios_data.get('scenarios', []))
                log_print(f"  Loaded {scenario_count} scenarios")
            else:
                log_print(f"  No scenario file found")
            
            # Process
            result = process_pillar_from_scenarios(pillar)
            log_print(f"  Processing result: {result}")
            
            # Verify files
            pillar_dir = Path(f"cyber-train/entities-intent/osint/{pillar}")
            entities_file = pillar_dir / f"{pillar}_entities.jsonl"
            intents_file = pillar_dir / f"{pillar}_intent.jsonl"
            
            if entities_file.exists():
                with open(entities_file) as f:
                    entity_lines = len(f.readlines())
                log_print(f"  ✓ Entities file: {entity_lines} lines")
            else:
                log_print(f"  ✗ Entities file not found")
            
            if intents_file.exists():
                with open(intents_file) as f:
                    intent_lines = len(f.readlines())
                log_print(f"  ✓ Intents file: {intent_lines} lines")
            else:
                log_print(f"  ✗ Intents file not found")
            
            if result and entities_file.exists() and intents_file.exists():
                success_count += 1
                
        except Exception as e:
            log_print(f"  ✗ Error: {e}")
            import traceback
            log_print(traceback.format_exc())
    
    log_print("\n" + "=" * 70)
    log_print(f"Completed: {success_count}/{len(OSINT_PILLARS)} pillars")
    log_print(f"Finished at {datetime.now()}")
    log_print("=" * 70)
    log_print(f"\nLog file: {log_file}")
    
except Exception as e:
    log_print(f"\nFATAL ERROR: {e}")
    import traceback
    log_print(traceback.format_exc())
finally:
    log.close()
    print(f"\nProcessing complete. Check log file: {log_file}")

