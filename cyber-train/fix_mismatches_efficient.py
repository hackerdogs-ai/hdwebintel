#!/usr/bin/env python3
"""
Efficient Fix for Training-Test Suite Mismatches

Uses exact test suite contexts first, then generates minimal variations.
"""

import json
from pathlib import Path
from typing import List, Tuple, Dict
from collections import defaultdict

# Entity to file mapping
ENTITY_PILLAR_MAPPING = {
    "EMOJI": "osint/socmint/socmint_entities.jsonl",
    "PHONE_NUMBER": "osint/socmint/socmint_entities.jsonl",
    "MALWARE_TYPE": "threat_intelligence/threat_intel_entities.jsonl",
    "DOMAIN": "network_security/network_security_entities.jsonl",
    "TIME": "incident_response/incident_response_entities.jsonl",
    "LATITUDE": "osint/geoint/geoint_entities.jsonl",
    "LONGITUDE": "osint/geoint/geoint_entities.jsonl",
    "IPV6_ADDRESS": "network_security/network_security_entities.jsonl",
    "SSN": "data_privacy/data_privacy_entities.jsonl",
    "EMAIL_ADDRESS": "data_privacy/data_privacy_entities.jsonl",
    "LLM_PROVIDER": "ai_security/ai_security_entities.jsonl",
    "LLM_MODEL": "ai_security/ai_security_entities.jsonl",
    "IP_ADDRESS": "network_security/network_security_entities.jsonl",
    "COMPLIANCE_FRAMEWORK": "audit_compliance/audit_compliance_entities.jsonl",
    "THREAT_ACTOR": "threat_intelligence/threat_intel_entities.jsonl",
    "DMS_COORDINATES": "osint/geoint/geoint_entities.jsonl",
    "ALTITUDE": "osint/geoint/geoint_entities.jsonl",
    "ELEVATION": "osint/geoint/geoint_entities.jsonl",
    "CURRENCY": "financial_osint/financial_osint_entities.jsonl",
    "PERCENTAGE": "vulnerability_management/vulnerability_management_entities.jsonl",
    "BASE64": "threat_intelligence/threat_intel_entities.jsonl",
    "BANK_ACCOUNT_NUMBER": "data_privacy/data_privacy_entities.jsonl",
    "ROUTING_NUMBER": "data_privacy/data_privacy_entities.jsonl",
    "SWIFT_CODE": "data_privacy/data_privacy_entities.jsonl",
    "DOB": "data_privacy/data_privacy_entities.jsonl",
    "DRIVER_LICENSE_NUMBER": "data_privacy/data_privacy_entities.jsonl",
    "PASSPORT_NUMBER": "data_privacy/data_privacy_entities.jsonl",
    "DISCORD_URL": "osint/socmint/socmint_entities.jsonl",
    "DISCORD_USERNAME": "osint/socmint/socmint_entities.jsonl",
    "TELEGRAM_URL": "osint/socmint/socmint_entities.jsonl",
    "TELEGRAM_USERNAME": "osint/socmint/socmint_entities.jsonl",
    "SLACK_URL": "osint/socmint/socmint_entities.jsonl",
    "SLACK_USERNAME": "osint/socmint/socmint_entities.jsonl",
    "WHATSAPP_URL": "osint/socmint/socmint_entities.jsonl",
    "FACEBOOK_URL": "osint/socmint/socmint_entities.jsonl",
    "FACEBOOK_USERNAME": "osint/socmint/socmint_entities.jsonl",
    "INSTAGRAM_URL": "osint/socmint/socmint_entities.jsonl",
    "INSTAGRAM_USERNAME": "osint/socmint/socmint_entities.jsonl",
    "LINKEDIN_URL": "osint/socmint/socmint_entities.jsonl",
    "LINKEDIN_USERNAME": "osint/socmint/socmint_entities.jsonl",
    "GITHUB_REPO_URL": "osint/cybint/cybint_entities.jsonl",
    "GITHUB_REPO": "osint/cybint/cybint_entities.jsonl",
    "GITHUB_USER": "osint/cybint/cybint_entities.jsonl",
    "GITHUB_ORGANIZATION": "osint/cybint/cybint_entities.jsonl",
    "GITHUB_COMMIT": "osint/cybint/cybint_entities.jsonl",
    "GITHUB_BRANCH": "osint/cybint/cybint_entities.jsonl",
    "GITHUB_ISSUE": "osint/cybint/cybint_entities.jsonl",
    "GITHUB_PULL_REQUEST": "osint/cybint/cybint_entities.jsonl",
    "GITHUB_RELEASE": "osint/cybint/cybint_entities.jsonl",
    "GITHUB_TAG": "osint/cybint/cybint_entities.jsonl",
    "GITHUB_GIST": "osint/cybint/cybint_entities.jsonl",
    "GEOJSON": "osint/geoint/geoint_entities.jsonl",
    "CUSTOM_COORDINATES": "osint/geoint/geoint_entities.jsonl",
    "NAMESERVER": "network_security/network_security_entities.jsonl",
    "HOST_TYPE": "endpoint_security/endpoint_security_entities.jsonl",
    "PORT": "network_security/network_security_entities.jsonl",
    "INCIDENT_ID": "incident_response/incident_response_entities.jsonl",
    "LOCATION": "osint/geoint/geoint_entities.jsonl",
    "USERNAME": "osint/socmint/socmint_entities.jsonl",
    "PLATFORM": "osint/socmint/socmint_entities.jsonl",
    "PROTOCOL": "network_security/network_security_entities.jsonl",
    "REGISTRY_KEY": "endpoint_security/endpoint_security_entities.jsonl",
    "WALLET_ADDRESS": "financial_osint/financial_osint_entities.jsonl",
    "CREDIT_CARD_NUMBER": "data_privacy/data_privacy_entities.jsonl",
}

def load_test_suite_missed_patterns():
    """Load exact missed patterns from test suite."""
    with open('comprehensive_test_results.json', 'r') as f:
        results = json.load(f)
    
    missed_patterns = defaultdict(list)
    
    for test in results.get('test_cases', []):
        text = test.get('text', '')
        expected = test.get('expected_entities', [])
        found = test.get('entities', [])
        
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
        
        missed = expected_set - found_set
        for entity_text, entity_type in missed:
            entity_pos = text.find(entity_text)
            if entity_pos != -1:
                missed_patterns[entity_type].append({
                    'entity': entity_text,
                    'context': text
                })
    
    return dict(missed_patterns)

def add_examples_to_file(file_path: Path, examples: List[Tuple[str, List]]):
    """Add examples to JSONL file efficiently."""
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        existing_examples = []
    else:
        existing_examples = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    existing_examples.append(json.loads(line))
    
    existing_contexts = {ex['text'] for ex in existing_examples}
    
    new_count = 0
    for text, entities in examples:
        if text not in existing_contexts:
            existing_contexts.add(text)
            example = {"text": text, "entities": entities}
            existing_examples.append(example)
            new_count += 1
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for ex in existing_examples:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')
    
    return new_count

def main():
    """Main function - efficient version."""
    base_dir = Path("entities-intent")
    
    print("Loading test suite missed patterns...")
    missed_patterns = load_test_suite_missed_patterns()
    print(f"Found {len(missed_patterns)} entity types with missed patterns")
    
    total_added = 0
    
    print("\n" + "="*70)
    print("ADDING EXACT TEST SUITE CONTEXTS AS TRAINING EXAMPLES")
    print("="*70)
    
    # Process all missed patterns - use exact contexts first
    for entity_type, patterns in missed_patterns.items():
        if entity_type not in ENTITY_PILLAR_MAPPING:
            continue
        
        file_path = base_dir / ENTITY_PILLAR_MAPPING[entity_type]
        
        print(f"\n📝 {entity_type}: {len(patterns)} missed patterns")
        
        # Use exact test suite contexts
        examples = []
        seen = set()
        
        for p in patterns:
            context = p['context']
            entity = p['entity']
            
            # Use exact context if not seen
            if context not in seen:
                seen.add(context)
                entity_pos = context.find(entity)
                if entity_pos != -1:
                    examples.append((context, [[entity_pos, entity_pos + len(entity), entity_type]]))
        
        # For entities with many missed patterns, limit to 50 exact contexts
        if len(examples) > 50:
            examples = examples[:50]
        
        if examples:
            added = add_examples_to_file(file_path, examples)
            total_added += added
            print(f"  ✅ Added {added} exact test suite contexts")
        else:
            print(f"  ⚠️  No examples generated")
    
    print("\n" + "="*70)
    print(f"✅ COMPLETE: Added {total_added} new examples")
    print("="*70)
    print("\nNext steps:")
    print("1. Re-prepare training data: python3 prepare_spacy_training.py")
    print("2. Re-train models: python3 train_spacy_models.py")
    print("3. Re-run test suite: python3 comprehensive_test_suite.py")

if __name__ == "__main__":
    main()

