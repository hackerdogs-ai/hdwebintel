#!/usr/bin/env python3
"""
Add 500+ examples of each underrepresented critical entity type.
"""

import json
import re
import random
from pathlib import Path
from typing import List, Dict

# Patterns
IP_PATTERN = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?[\d\s\-\(\)]{10,}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')

# Threat actors
THREAT_ACTORS = [
    'APT28', 'APT29', 'APT41', 'Lazarus', 'FIN7', 'UNC2452', 'Wizard Spider',
    'Ryuk', 'Conti', 'Maze', 'REvil', 'LockBit', 'BlackCat', 'ALPHV',
    'Cozy Bear', 'Fancy Bear', 'Turla', 'Sandworm', 'Equation Group',
    'DarkSide', 'Ragnar Locker', 'DoppelPaymer', 'Mespinoza', 'Egregor'
]

# Generate examples
def generate_cve_examples(count: int) -> List[Dict]:
    """Generate CVE examples."""
    examples = []
    years = list(range(2018, 2025))
    for i in range(count):
        year = random.choice(years)
        cve_num = random.randint(1, 99999)
        cve_id = f"CVE-{year}-{cve_num:05d}"
        
        contexts = [
            f"Vulnerability {cve_id} was discovered in the system",
            f"Patch {cve_id} immediately to prevent exploitation",
            f"Scan for {cve_id} across all endpoints",
            f"Critical vulnerability {cve_id} requires immediate attention",
            f"Exploit for {cve_id} is available in the wild",
            f"Remediate {cve_id} before the next security audit",
            f"CVSS score for {cve_id} is 9.8",
            f"Affected systems must patch {cve_id} by end of week",
            f"Threat intelligence indicates active exploitation of {cve_id}",
            f"Security team investigating {cve_id} impact"
        ]
        text = random.choice(contexts)
        match = CVE_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'CVE_ID']]
            })
    return examples

def generate_threat_actor_examples(count: int) -> List[Dict]:
    """Generate threat actor examples."""
    examples = []
    for i in range(count):
        actor = random.choice(THREAT_ACTORS)
        contexts = [
            f"Threat actor {actor} has been active in recent campaigns",
            f"Investigate {actor} activities in our network",
            f"{actor} is known for targeting financial institutions",
            f"Intelligence indicates {actor} is behind this attack",
            f"Track {actor} infrastructure and indicators",
            f"{actor} uses sophisticated evasion techniques",
            f"Attribution analysis points to {actor}",
            f"Monitor for {actor} TTPs in security logs",
            f"{actor} has been linked to multiple breaches",
            f"Profile {actor} capabilities and motivations"
        ]
        text = random.choice(contexts)
        # Find actor in text
        actor_lower = actor.lower()
        text_lower = text.lower()
        idx = text_lower.find(actor_lower)
        if idx != -1:
            examples.append({
                'text': text,
                'entities': [[idx, idx + len(actor), 'THREAT_ACTOR']]
            })
    return examples

def generate_wallet_examples(count: int) -> List[Dict]:
    """Generate wallet address examples."""
    examples = []
    for i in range(count):
        wallet = '0x' + ''.join(random.choices('0123456789abcdef', k=40))
        contexts = [
            f"Track transactions from wallet {wallet}",
            f"Monitor wallet address {wallet} for suspicious activity",
            f"Wallet {wallet} received 10 BTC from darknet market",
            f"Blockchain analysis of {wallet} reveals money laundering",
            f"Investigate wallet {wallet} linked to ransomware payment",
            f"Wallet {wallet} has been flagged for investigation",
            f"Analyze {wallet} transaction history",
            f"Wallet {wallet} associated with cryptocurrency theft",
            f"Trace funds to wallet {wallet}",
            f"Wallet {wallet} shows patterns consistent with fraud"
        ]
        text = random.choice(contexts)
        match = WALLET_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'WALLET_ADDRESS']]
            })
    return examples

def generate_coordinate_examples(count: int) -> List[Dict]:
    """Generate latitude/longitude examples."""
    examples = []
    for i in range(count):
        lat = round(random.uniform(-90, 90), 6)
        lon = round(random.uniform(-180, 180), 6)
        
        formats = [
            f"Coordinates: {lat}, {lon}",
            f"Location at latitude {lat} longitude {lon}",
            f"GPS coordinates {lat}, {lon} identified",
            f"Geographic position: {lat}, {lon}",
            f"Map location {lat}, {lon}",
            f"Latitude {lat} and longitude {lon}",
            f"Coordinates {lat}, {lon} verified",
            f"Position {lat}, {lon} confirmed",
            f"Location coordinates: {lat}, {lon}",
            f"Geolocation {lat}, {lon} extracted from image"
        ]
        text = random.choice(formats)
        
        # Find coordinates
        lat_str = str(lat)
        lon_str = str(lon)
        lat_idx = text.find(lat_str)
        lon_idx = text.find(lon_str)
        
        entities = []
        if lat_idx != -1:
            entities.append([lat_idx, lat_idx + len(lat_str), 'LATITUDE'])
        if lon_idx != -1:
            entities.append([lon_idx, lon_idx + len(lon_str), 'LONGITUDE'])
        
        if entities:
            examples.append({
                'text': text,
                'entities': entities
            })
    return examples

def generate_phone_examples(count: int) -> List[Dict]:
    """Generate phone number examples."""
    examples = []
    formats = [
        lambda: f"+1-{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}",
        lambda: f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}",
        lambda: f"+44-20-{random.randint(7000,7999)}-{random.randint(1000,9999)}",
        lambda: f"+{random.randint(1,99)}-{random.randint(10,99)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
    ]
    
    for i in range(count):
        phone = random.choice(formats)()
        contexts = [
            f"Contact number {phone} is associated with the suspect",
            f"Phone {phone} was used in the fraudulent transaction",
            f"Investigate phone number {phone}",
            f"Phone {phone} linked to multiple accounts",
            f"Verify phone {phone} ownership",
            f"Phone number {phone} flagged for suspicious activity",
            f"Trace calls from {phone}",
            f"Phone {phone} registered to fake identity",
            f"Monitor communications from {phone}",
            f"Phone {phone} used in social engineering attack"
        ]
        text = random.choice(contexts)
        match = PHONE_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'PHONE_NUMBER']]
            })
    return examples

def generate_email_examples(count: int) -> List[Dict]:
    """Generate email address examples."""
    examples = []
    domains = ['example.com', 'test.org', 'company.net', 'suspicious.io', 'malicious.biz']
    usernames = ['admin', 'user', 'support', 'noreply', 'security', 'info', 'contact']
    
    for i in range(count):
        email = f"{random.choice(usernames)}{random.randint(1,999)}@{random.choice(domains)}"
        contexts = [
            f"Email {email} was compromised",
            f"Investigate account {email}",
            f"Email address {email} linked to data breach",
            f"Monitor {email} for suspicious activity",
            f"Email {email} used in phishing campaign",
            f"Verify ownership of {email}",
            f"Email {email} associated with threat actor",
            f"Account {email} shows signs of compromise",
            f"Email {email} registered with fake credentials",
            f"Contact {email} for security inquiry"
        ]
        text = random.choice(contexts)
        match = EMAIL_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'EMAIL_ADDRESS']]
            })
    return examples

def add_to_file(file_path: Path, examples: List[Dict], entity_type: str):
    """Add examples to a file."""
    with open(file_path, 'a', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

def main():
    """Main function."""
    base_dir = Path('cyber-train/entities-intent')
    if not base_dir.exists():
        base_dir = Path('entities-intent')
    
    print("="*80)
    print("ADDING CRITICAL ENTITY EXAMPLES")
    print("="*80)
    
    # Find actual files
    entity_files = list(base_dir.rglob('*_entities.jsonl'))
    file_map = {f.name: f for f in entity_files}
    
    # Target files for each entity type (using actual filenames)
    target_files = {
        'CVE_ID': [
            'vulnerability_mgmt_entities.jsonl',
            'application_security_entities.jsonl',
            'threat_intelligence_entities.jsonl',
            'incident_response_entities.jsonl',
            'cybint_entities.jsonl',
            'threat_intel_entities.jsonl',
        ],
        'THREAT_ACTOR': [
            'threat_intelligence_entities.jsonl',
            'incident_response_entities.jsonl',
            'cybint_entities.jsonl',
            'threat_intel_entities.jsonl',
            'ai_security_entities.jsonl',
            'network_security_entities.jsonl',
        ],
        'WALLET_ADDRESS': [
            'finint_entities.jsonl',
            'darkint_entities.jsonl',
            'cybint_entities.jsonl',
            'threat_intel_entities.jsonl',
            'threat_intelligence_entities.jsonl',
        ],
        'LATITUDE': [
            'geoint_entities.jsonl',
            'imint_entities.jsonl',
            'ai-int_entities.jsonl',
            'comint_entities.jsonl',
        ],
        'LONGITUDE': [
            'geoint_entities.jsonl',
            'imint_entities.jsonl',
            'ai-int_entities.jsonl',
            'comint_entities.jsonl',
        ],
        'PHONE_NUMBER': [
            'comint_entities.jsonl',
            'humint_entities.jsonl',
            'socmint_entities.jsonl',
            'data_privacy_sovereignty_entities.jsonl',
            'incident_response_entities.jsonl',
        ],
        'EMAIL_ADDRESS': [
            'comint_entities.jsonl',
            'humint_entities.jsonl',
            'data_privacy_sovereignty_entities.jsonl',
            'incident_response_entities.jsonl',
            'socmint_entities.jsonl',
        ],
    }
    
    # Remove None values
    for key in target_files:
        target_files[key] = [f for f in target_files[key] if f is not None]
    
    # Generate and add examples
    entity_generators = {
        'CVE_ID': (generate_cve_examples, 500),
        'THREAT_ACTOR': (generate_threat_actor_examples, 500),
        'WALLET_ADDRESS': (generate_wallet_examples, 200),
        'LATITUDE': (generate_coordinate_examples, 200),
        'LONGITUDE': (generate_coordinate_examples, 200),
        'PHONE_NUMBER': (generate_phone_examples, 300),
        'EMAIL_ADDRESS': (generate_email_examples, 300),
    }
    
    total_added = {}
    
    for entity_type, (generator_func, total_count) in entity_generators.items():
        print(f"\n{'='*80}")
        print(f"Adding {entity_type} examples ({total_count} total)")
        print(f"{'='*80}")
        
        examples = generator_func(total_count)
        files_for_type = target_files[entity_type]
        examples_per_file = total_count // len(files_for_type)
        remainder = total_count % len(files_for_type)
        
        added_count = 0
        for i, filename in enumerate(files_for_type):
            if filename not in file_map:
                print(f"  ⚠️  File not found: {filename}")
                continue
            file_path = file_map[filename]
            
            count_for_file = examples_per_file + (1 if i < remainder else 0)
            file_examples = examples[added_count:added_count + count_for_file]
            add_to_file(file_path, file_examples, entity_type)
            added_count += count_for_file
            print(f"  ✅ Added {len(file_examples)} examples to {file_path.name}")
        
        total_added[entity_type] = added_count
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    for entity_type, count in total_added.items():
        print(f"  {entity_type}: {count} examples added")

if __name__ == '__main__':
    main()

