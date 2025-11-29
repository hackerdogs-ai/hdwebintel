#!/usr/bin/env python3
"""Execute OSINT generation and verify files."""
import sys
import os
from pathlib import Path

# Import the main script
sys.path.insert(0, '.')
import create_osint_realistic

# Process all pillars
print("Starting OSINT generation...")
success_count = 0

for pillar in create_osint_realistic.OSINT_PILLARS:
    try:
        result = create_osint_realistic.process_pillar(pillar)
        if result:
            success_count += 1
            # Verify files were created
            pillar_dir = Path(f"cyber-train/entities-intent/osint/{pillar}")
            entities_file = pillar_dir / f"{pillar}_entities.jsonl"
            intents_file = pillar_dir / f"{pillar}_intent.jsonl"
            
            if entities_file.exists() and intents_file.exists():
                with open(entities_file) as f:
                    entity_count = len(f.readlines())
                with open(intents_file) as f:
                    intent_count = len(f.readlines())
                print(f"  ✓ {pillar}: {entity_count} entities, {intent_count} intents")
            else:
                print(f"  ✗ {pillar}: Files not created!")
        else:
            print(f"  ✗ {pillar}: Processing failed")
    except Exception as e:
        print(f"  ✗ {pillar}: Error - {e}")
        import traceback
        traceback.print_exc()

print(f"\nCompleted: {success_count}/{len(create_osint_realistic.OSINT_PILLARS)} pillars")

