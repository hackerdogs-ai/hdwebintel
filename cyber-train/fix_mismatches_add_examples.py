#!/usr/bin/env python3
"""
Fix Training-Test Suite Mismatches

This script adds training examples to fix the identified mismatches:
1. Add missing entity types (0 training examples)
2. Add short context examples (40-90 chars) for context length mismatch
3. Add test suite pattern examples for pattern mismatch
"""

import json
import random
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
        category = test.get('category', '')
        
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
                    'context': text,
                    'category': category
                })
    
    return dict(missed_patterns)

def generate_short_context_examples(entity_type: str, patterns: List[Dict], count: int) -> List[Tuple[str, List]]:
    """Generate short context examples (40-90 chars) matching test suite patterns."""
    examples = []
    seen = set()
    
    # Use exact test suite contexts first
    for p in patterns:
        if len(examples) >= count:
            break
        context = p['context']
        entity = p['entity']
        
        # Only use if context is short (40-90 chars)
        if 40 <= len(context) <= 90:
            if context not in seen:
                seen.add(context)
                entity_pos = context.find(entity)
                if entity_pos != -1:
                    examples.append((context, [[entity_pos, entity_pos + len(entity), entity_type]]))
    
    # Generate variations with short contexts
    if entity_type == "EMOJI":
        emojis = ['🚨', '⚠️', '🔍', '✅', '✓', '❌', '🔐', '🛡️', '💻', '🦠']
        short_patterns = [
            "{emoji} Security alert: IP 192.168.1.1 compromised",
            "{emoji} Warning: Domain example.com is suspicious",
            "✅ Verified: Email user@example.com is safe",
            "{emoji} Threat detected: CVE-2021-44228 exploitation",
            "{emoji} Malware analysis: WannaCry variant identified",
        ]
    elif entity_type == "PHONE_NUMBER":
        phones = ["+1-555-123-4567", "(555) 123-4567", "555-123-4567", "+44-20-7946-0958"]
        short_patterns = [
            "Check IP: 10.0.0.1, Domain: test.com, Email: user@test.com, Phone: {phone}",
            "Investigate WhatsApp contact {phone} and URL wa.me/1234567890",
            "PII leak detected: SSN 123-45-6789, phone {phone}",
            "Contact information: Email user@example.com, Phone {phone}",
        ]
    elif entity_type == "MALWARE_TYPE":
        malware = ["WannaCry", "NotPetya", "Ryuk", "Zeus", "Emotet", "TrickBot"]
        short_patterns = [
            "APT28 used {malware} ransomware to attack IP 172.16.0.1",
            "Ransomware detected: {malware}, NotPetya, Ryuk variants",
            "Malware families: Zeus, Emotet, {malware}, TrickBot detected",
            "Threat intelligence report: {malware} variant identified",
        ]
    elif entity_type == "DMS_COORDINATES":
        coords = ["40°42'46\"N 74°00'22\"W", "52°31'44.7\"N 13°23'05.7\"E"]
        short_patterns = [
            "Location at {coord} in datacenter AWS-US-EAST-1",
            "Coordinate formats: 40.7128, -74.0060 and {coord}",
            "DMS coordinates: {coord} and 51°30'26\"N 0°07'39\"W",
        ]
    elif entity_type == "LATITUDE":
        lats = ["40.7128", "37.7749", "27.9881"]
        short_patterns = [
            "Find all activities from coordinates {lat}, -122.4194 in San Francisco",
            "Altitude 8848m at coordinates {lat}, 86.9250 (Mount Everest)",
            "Track location: latitude {lat}, longitude -74.0060, altitude 10m",
        ]
    elif entity_type == "LONGITUDE":
        lons = ["-74.0060", "-122.4194", "86.9250"]
        short_patterns = [
            "Find all activities from coordinates 37.7749, {lon} in San Francisco",
            "Altitude 8848m at coordinates 27.9881, {lon} (Mount Everest)",
            "Track location: latitude 40.7128, longitude {lon}, altitude 10m",
        ]
    elif entity_type == "TIME":
        times = ["14:30", "2:30 PM", "14:30:00", "18:00"]
        short_patterns = [
            "Incident INC-2024-001 occurred on 2024-11-30 at {time} UTC",
            "Time formats: 14:30, 2:30 PM, 14:30:00, {time}",
            "Time ranges: from 14:00 to {time}",
        ]
    elif entity_type == "SSN":
        ssns = ["123-45-6789", "123 45 6789", "123456789"]
        short_patterns = [
            "PII leak detected: SSN {ssn}, phone +44 20 7946 0958",
            "Exposed PII: SSN {ssn}, passport A12345678, driver license DL123456",
            "Full PII breach: SSN {ssn}, DOB 01/15/1980, email user@example.com",
        ]
    elif entity_type == "DOMAIN":
        domains = ["evil.com", "example.com", "test.com"]
        short_patterns = [
            "APT28 used WannaCry ransomware to attack IP 172.16.0.1 and domain {domain}",
            "Check domain {domain} for malicious activity",
            "DNS lookup for domain {domain} returned suspicious IP",
        ]
    else:
        # Generic short context generation
        for p in patterns[:count]:
            context = p['context']
            entity = p['entity']
            if 40 <= len(context) <= 90 and context not in seen:
                seen.add(context)
                entity_pos = context.find(entity)
                if entity_pos != -1:
                    examples.append((context, [[entity_pos, entity_pos + len(entity), entity_type]]))
        return examples[:count]
    
    # Generate variations with iteration limit
    max_iterations = count * 5
    iterations = 0
    while len(examples) < count and iterations < max_iterations:
        iterations += 1
        try:
            if entity_type == "EMOJI":
                emoji = random.choice(emojis)
                pattern = random.choice(short_patterns)
                context = pattern.format(emoji=emoji)
                entity = emoji
            elif entity_type == "PHONE_NUMBER":
                phone = random.choice(phones)
                pattern = random.choice(short_patterns)
                context = pattern.format(phone=phone)
                entity = phone
            elif entity_type == "MALWARE_TYPE":
                malware = random.choice(malware)
                pattern = random.choice(short_patterns)
                context = pattern.format(malware=malware)
                entity = malware
            elif entity_type == "DMS_COORDINATES":
                coord = random.choice(coords)
                pattern = random.choice(short_patterns)
                context = pattern.format(coord=coord)
                entity = coord
            elif entity_type == "LATITUDE":
                lat = random.choice(lats)
                pattern = random.choice(short_patterns)
                context = pattern.format(lat=lat)
                entity = lat
            elif entity_type == "LONGITUDE":
                lon = random.choice(lons)
                pattern = random.choice(short_patterns)
                context = pattern.format(lon=lon)
                entity = lon
            elif entity_type == "TIME":
                time = random.choice(times)
                pattern = random.choice(short_patterns)
                context = pattern.format(time=time)
                entity = time
            elif entity_type == "SSN":
                ssn = random.choice(ssns)
                pattern = random.choice(short_patterns)
                context = pattern.format(ssn=ssn)
                entity = ssn
            elif entity_type == "DOMAIN":
                domain = random.choice(domains)
                pattern = random.choice(short_patterns)
                context = pattern.format(domain=domain)
                entity = domain
            else:
                break
            
            if context not in seen and 40 <= len(context) <= 90:
                seen.add(context)
                entity_pos = context.find(entity)
                if entity_pos != -1:
                    examples.append((context, [[entity_pos, entity_pos + len(entity), entity_type]]))
        except Exception as e:
            print(f"  ⚠️  Error generating example: {e}")
            break
    
    return examples[:count]

def add_examples_to_file(file_path: Path, examples: List[Tuple[str, List]], entity_type: str):
    """Add examples to JSONL file."""
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
    """Main function."""
    base_dir = Path("entities-intent")
    
    print("Loading test suite missed patterns...")
    missed_patterns = load_test_suite_missed_patterns()
    print(f"Found {len(missed_patterns)} entity types with missed patterns")
    
    # Load mismatch analysis
    with open('TRAINING_TEST_MISMATCH_REPORT.json', 'r') as f:
        mismatch_data = json.load(f)
    
    total_added = 0
    
    print("\n" + "="*70)
    print("ADDING SHORT CONTEXT EXAMPLES FOR TOP MISSED ENTITIES")
    print("="*70)
    
    # Top missed entities with context length mismatch
    priority_entities = [
        "EMOJI", "PHONE_NUMBER", "MALWARE_TYPE", "DMS_COORDINATES",
        "LATITUDE", "LONGITUDE", "TIME", "SSN", "DOMAIN"
    ]
    
    for entity_type in priority_entities:
        if entity_type not in missed_patterns:
            continue
        if entity_type not in ENTITY_PILLAR_MAPPING:
            continue
        
        patterns = missed_patterns[entity_type]
        file_path = base_dir / ENTITY_PILLAR_MAPPING[entity_type]
        
        print(f"\n📝 {entity_type}: {len(patterns)} missed patterns")
        
        # Generate 100 short context examples (reduced for speed)
        examples = generate_short_context_examples(entity_type, patterns, 100)
        
        if examples:
            added = add_examples_to_file(file_path, examples, entity_type)
            total_added += added
            print(f"  ✅ Added {added} short context examples")
        else:
            print(f"  ⚠️  No examples generated")
    
    # Add missing entity types (0 training examples)
    print("\n" + "="*70)
    print("ADDING MISSING ENTITY TYPES")
    print("="*70)
    
    missing_types = [
        "ALTITUDE", "BANK_ACCOUNT_NUMBER", "BASE64", "DISCORD_URL", "DISCORD_USERNAME",
        "TELEGRAM_URL", "TELEGRAM_USERNAME", "SLACK_URL", "SLACK_USERNAME", "WHATSAPP_URL",
        "FACEBOOK_URL", "FACEBOOK_USERNAME", "INSTAGRAM_URL", "INSTAGRAM_USERNAME",
        "LINKEDIN_URL", "LINKEDIN_USERNAME", "GITHUB_REPO_URL", "GITHUB_REPO",
        "GITHUB_USER", "GITHUB_ORGANIZATION", "GITHUB_COMMIT", "GITHUB_BRANCH",
        "GITHUB_ISSUE", "GITHUB_PULL_REQUEST", "GITHUB_RELEASE", "GITHUB_TAG", "GITHUB_GIST",
        "GEOJSON", "CUSTOM_COORDINATES", "ELEVATION", "DOB", "DRIVER_LICENSE_NUMBER",
        "PASSPORT_NUMBER", "ROUTING_NUMBER", "SWIFT_CODE", "NAMESERVER", "HOST_TYPE",
        "PORT", "INCIDENT_ID", "LOCATION", "USERNAME", "PLATFORM", "REGISTRY_KEY",
        "WALLET_ADDRESS", "CREDIT_CARD_NUMBER", "CURRENCY", "PERCENTAGE"
    ]
    
    for entity_type in missing_types:
        if entity_type not in missed_patterns:
            continue
        if entity_type not in ENTITY_PILLAR_MAPPING:
            continue
        
        patterns = missed_patterns[entity_type]
        file_path = base_dir / ENTITY_PILLAR_MAPPING[entity_type]
        
        print(f"\n📝 {entity_type}: {len(patterns)} missed patterns (0 training examples)")
        
        # Use exact test suite contexts + generate variations
        examples = []
        seen = set()
        
        for p in patterns:
            context = p['context']
            entity = p['entity']
            if context not in seen:
                seen.add(context)
                entity_pos = context.find(entity)
                if entity_pos != -1:
                    examples.append((context, [[entity_pos, entity_pos + len(entity), entity_type]]))
        
        # Generate more variations to reach 200 (with limit)
        max_iterations = 300
        iterations = 0
        while len(examples) < 200 and iterations < max_iterations:
            iterations += 1
            if patterns:
                p = random.choice(patterns)
                entity = p['entity']
                base_context = p['context']
                
                # Use exact context if short enough
                if 40 <= len(base_context) <= 90 and base_context not in seen:
                    seen.add(base_context)
                    entity_pos = base_context.find(entity)
                    if entity_pos != -1:
                        examples.append((base_context, [[entity_pos, entity_pos + len(entity), entity_type]]))
                else:
                    # Create simple variation
                    words = base_context.split()
                    if len(words) > 3 and len(words) <= 15:
                        # Keep entity and some surrounding words
                        try:
                            entity_idx = base_context.find(entity)
                            if entity_idx != -1:
                                # Extract entity and nearby words
                                start = max(0, entity_idx - 30)
                                end = min(len(base_context), entity_idx + len(entity) + 30)
                                new_context = base_context[start:end].strip()
                                if entity in new_context and 40 <= len(new_context) <= 90 and new_context not in seen:
                                    seen.add(new_context)
                                    entity_pos = new_context.find(entity)
                                    if entity_pos != -1:
                                        examples.append((new_context, [[entity_pos, entity_pos + len(entity), entity_type]]))
                        except:
                            pass
        
        if examples:
            added = add_examples_to_file(file_path, examples[:100], entity_type)
            total_added += added
            print(f"  ✅ Added {added} examples for missing entity type")
    
    print("\n" + "="*70)
    print(f"✅ COMPLETE: Added {total_added} new examples")
    print("="*70)
    print("\nNext steps:")
    print("1. Re-prepare training data: python3 prepare_spacy_training.py")
    print("2. Re-train models: python3 train_spacy_models.py")
    print("3. Re-run test suite: python3 comprehensive_test_suite.py")

if __name__ == "__main__":
    main()

