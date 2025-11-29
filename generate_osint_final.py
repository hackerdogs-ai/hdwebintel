#!/usr/bin/env python3
"""
Generate realistic OSINT entities and intents - direct approach.
"""

import json
import os
import re
from pathlib import Path

OSINT_PILLARS = [
    "ai_int", "comint", "cybint", "darkint", "digint", "dnint", "domain_intel",
    "ecoint", "eduint", "finint", "geoint", "humint", "imint", "infint",
    "legint", "masint", "medint", "natint", "orbint", "sigint", "socmint",
    "techint", "threat_intel", "tradint", "vatint"
]

BASE_PATH = Path("cyber-train/entities-intent/osint")

# Read the existing realistic examples from the other file
import sys
sys.path.insert(0, '.')
try:
    from create_osint_realistic import REALISTIC_EXAMPLES
except:
    REALISTIC_EXAMPLES = {}

def find_entity_spans(text, pillar):
    """Find entity spans in text."""
    entities = []
    text_lower = text.lower()
    
    # Common entity patterns
    patterns = [
        (r'\b[A-Z][a-z]+ (?:Analyst|Researcher|Specialist|Engineer|Officer|Hunter|Investigator)\b', 'ROLE'),
        (r'\b(?:SHA256|SHA1|MD5|SHA512)\s+[a-f0-9]{32,64}\b', 'HASH'),
        (r'\b\d+\.\d+\.\d+\.\d+\b', 'IP_ADDRESS'),
        (r'\b[a-z0-9.-]+\.(?:com|net|org|io|gov|edu)\b', 'DOMAIN'),
        (r'\bCVE-\d{4}-\d{4,7}\b', 'CVE'),
        (r'\b@[a-zA-Z0-9_]+\b', 'USERNAME'),
        (r'#[a-zA-Z0-9_]+', 'HASHTAG'),
        (r'\b\d+%\b', 'PERCENTAGE'),
        (r'\b(?:MITRE|ATT&CK|T\d{4})\b', 'FRAMEWORK'),
        (r'\b(?:Operation|Campaign|Case)[A-Z][a-zA-Z]+\b', 'OPERATION'),
    ]
    
    for pattern, label in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            entities.append([match.start(), match.end(), label])
    
    # Sort by start position
    entities.sort(key=lambda x: x[0])
    return entities

def generate_intent_categories(text):
    """Generate intent categories."""
    cats = {
        "INVESTIGATE": 0.0,
        "DETECT": 0.0,
        "ENRICH": 0.0,
        "MAP": 0.0,
        "GENERATE": 0.0
    }
    
    text_lower = text.lower()
    if any(kw in text_lower for kw in ["investigate", "analyze", "check", "examine", "review"]):
        cats["INVESTIGATE"] = 1.0
    if any(kw in text_lower for kw in ["detect", "find", "identify", "flag", "discover"]):
        cats["DETECT"] = 1.0
    if any(kw in text_lower for kw in ["enrich", "enhance", "add data", "get data"]):
        cats["ENRICH"] = 1.0
    if any(kw in text_lower for kw in ["map", "graph", "network", "relationship"]):
        cats["MAP"] = 1.0
    if any(kw in text_lower for kw in ["generate", "create", "build", "compile"]):
        cats["GENERATE"] = 1.0
    
    if sum(cats.values()) == 0:
        cats["INVESTIGATE"] = 1.0
    
    return cats

def process_pillar(pillar):
    """Process a single pillar."""
    print(f"Processing {pillar}...", end=" ", flush=True)
    
    try:
        # Get examples
        if pillar in REALISTIC_EXAMPLES:
            entity_texts = REALISTIC_EXAMPLES[pillar]["entities"]
            intent_texts = REALISTIC_EXAMPLES[pillar]["intents"]
        else:
            entity_texts = [f"{pillar.replace('_', ' ').title()} Analyst conducted analysis"]
            intent_texts = [f"Perform {pillar.replace('_', ' ')} analysis"]
        
        # Generate 100 entities
        entities = []
        for i in range(100):
            if i < len(entity_texts):
                text = entity_texts[i]
            else:
                base_text = entity_texts[i % len(entity_texts)]
                text = base_text.replace("Analyst", ["Analyst", "Researcher", "Specialist"][i % 3])
            
            entity_spans = find_entity_spans(text, pillar)
            entities.append({
                "text": text,
                "entities": entity_spans
            })
        
        # Generate 100 intents
        intents = []
        for i in range(100):
            if i < len(intent_texts):
                text = intent_texts[i]
            else:
                text = intent_texts[i % len(intent_texts)]
            
            cats = generate_intent_categories(text)
            intents.append({
                "text": text,
                "cats": cats
            })
        
        # Write files
        pillar_dir = BASE_PATH / pillar
        pillar_dir.mkdir(parents=True, exist_ok=True)
        
        entities_file = pillar_dir / f"{pillar}_entities.jsonl"
        intents_file = pillar_dir / f"{pillar}_intent.jsonl"
        
        with open(entities_file, 'w', encoding='utf-8') as f:
            for entity in entities:
                f.write(json.dumps(entity, ensure_ascii=False) + '\n')
        
        with open(intents_file, 'w', encoding='utf-8') as f:
            for intent in intents:
                f.write(json.dumps(intent, ensure_ascii=False) + '\n')
        
        print(f"✅ {len(entities)} entities, {len(intents)} intents")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print(f"Generating realistic OSINT entities and intents for {len(OSINT_PILLARS)} pillars...\n")
    
    success = 0
    for pillar in OSINT_PILLARS:
        if process_pillar(pillar):
            success += 1
    
    print(f"\n✅ Completed {success}/{len(OSINT_PILLARS)} pillars!")

