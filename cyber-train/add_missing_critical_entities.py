#!/usr/bin/env python3
"""
Add missing critical entity examples with proper boundaries:
- CVE_ID
- WALLET_ADDRESS  
- LATITUDE
- LONGITUDE
- PHONE_NUMBER
- EMAIL_ADDRESS
"""

import json
import re
from pathlib import Path
from typing import List
import random

# Patterns for validation
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?1?[-.\s(]?\(?\d{3}\)?[-.\s)]?\d{3}[-.\s]?\d{4}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
LATITUDE_PATTERN = re.compile(r'\b-?([0-8]?[0-9](?:\.\d+)?|90(?:\.0+)?)\b')
LONGITUDE_PATTERN = re.compile(r'\b-?(?:[0-9]?[0-9]?[0-9](?:\.\d+)?|1[0-7][0-9](?:\.\d+)?|180(?:\.0+)?)\b')

# Realistic examples to add
CVE_EXAMPLES = [
    "CVE-2024-1234",
    "CVE-2023-5678",
    "CVE-2024-9012",
    "CVE-2023-3456",
    "CVE-2024-7890",
]

WALLET_EXAMPLES = [
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "0x8ba1f109551bD432803012645Hac136c22C3e623",
    "0x1234567890123456789012345678901234567890",
]

EMAIL_EXAMPLES = [
    "security@example.com",
    "admin@company.org",
    "alice.smith@domain.net",
    "john.doe@test.io",
    "contact@business.com",
]

PHONE_EXAMPLES = [
    "+1-555-123-4567",
    "(555) 987-6543",
    "555-234-5678",
    "+44 20 7946 0958",
    "1-800-555-0199",
]

LATITUDE_EXAMPLES = [
    "40.7128",
    "-33.8688",
    "51.5074",
    "35.6762",
    "37.7749",
]

LONGITUDE_EXAMPLES = [
    "-74.0060",
    "151.2093",
    "-0.1278",
    "139.6503",
    "-122.4194",
]

def generate_realistic_examples(entity_type: str, count: int) -> List[dict]:
    """Generate realistic examples with proper entity boundaries."""
    examples = []
    
    if entity_type == 'CVE_ID':
        templates = [
            "Vulnerability scanner detected {cve} in production system",
            "Security team patched {cve} affecting critical infrastructure",
            "Threat intelligence report mentions {cve} being actively exploited",
            "CVE database shows {cve} has CVSS score 9.8",
            "Incident response team investigating {cve} exploitation attempt",
        ]
        for i in range(count):
            cve = random.choice(CVE_EXAMPLES)
            template = random.choice(templates)
            text = template.format(cve=cve)
            # Find the CVE in the text
            match = CVE_PATTERN.search(text)
            if match:
                examples.append({
                    'text': text,
                    'entities': [[match.start(), match.end(), 'CVE_ID']]
                })
    
    elif entity_type == 'WALLET_ADDRESS':
        templates = [
            "Blockchain analysis identified wallet {wallet} linked to ransomware payments",
            "Cryptocurrency transaction traced to wallet address {wallet}",
            "Threat actor wallet {wallet} received 50 BTC from victim",
            "Forensics team extracted wallet {wallet} from malware configuration",
            "Dark web marketplace uses wallet {wallet} for payments",
        ]
        for i in range(count):
            wallet = random.choice(WALLET_EXAMPLES)
            template = random.choice(templates)
            text = template.format(wallet=wallet)
            match = WALLET_PATTERN.search(text)
            if match:
                examples.append({
                    'text': text,
                    'entities': [[match.start(), match.end(), 'WALLET_ADDRESS']]
                })
    
    elif entity_type == 'EMAIL_ADDRESS':
        templates = [
            "Phishing email sent from {email} targeting employees",
            "Security alert: suspicious login attempt from {email}",
            "Incident report: data breach notification sent to {email}",
            "Threat actor used {email} for command and control communication",
            "Forensics analysis found {email} in compromised account logs",
        ]
        for i in range(count):
            email = random.choice(EMAIL_EXAMPLES)
            template = random.choice(templates)
            text = template.format(email=email)
            match = EMAIL_PATTERN.search(text)
            if match:
                examples.append({
                    'text': text,
                    'entities': [[match.start(), match.end(), 'EMAIL_ADDRESS']]
                })
    
    elif entity_type == 'PHONE_NUMBER':
        templates = [
            "Suspicious call logged from phone number {phone}",
            "Two-factor authentication code sent to {phone}",
            "Threat intelligence indicates {phone} used in social engineering attack",
            "Incident response contacted victim at {phone}",
            "Forensics team traced call to {phone}",
        ]
        for i in range(count):
            phone = random.choice(PHONE_EXAMPLES)
            template = random.choice(templates)
            text = template.format(phone=phone)
            match = PHONE_PATTERN.search(text)
            if match:
                examples.append({
                    'text': text,
                    'entities': [[match.start(), match.end(), 'PHONE_NUMBER']]
                })
    
    elif entity_type == 'LATITUDE':
        templates = [
            "Geolocation analysis shows attack originated at latitude {lat}",
            "GPS coordinates indicate latitude {lat} for incident location",
            "Threat intelligence report includes latitude {lat} for threat actor location",
            "Forensics team identified latitude {lat} from device logs",
            "Security incident occurred at latitude {lat} according to logs",
        ]
        for i in range(count):
            lat = random.choice(LATITUDE_EXAMPLES)
            template = random.choice(templates)
            text = template.format(lat=lat)
            match = LATITUDE_PATTERN.search(text)
            if match:
                examples.append({
                    'text': text,
                    'entities': [[match.start(), match.end(), 'LATITUDE']]
                })
    
    elif entity_type == 'LONGITUDE':
        templates = [
            "Geolocation analysis shows attack originated at longitude {lon}",
            "GPS coordinates indicate longitude {lon} for incident location",
            "Threat intelligence report includes longitude {lon} for threat actor location",
            "Forensics team identified longitude {lon} from device logs",
            "Security incident occurred at longitude {lon} according to logs",
        ]
        for i in range(count):
            lon = random.choice(LONGITUDE_EXAMPLES)
            template = random.choice(templates)
            text = template.format(lon=lon)
            match = LONGITUDE_PATTERN.search(text)
            if match:
                examples.append({
                    'text': text,
                    'entities': [[match.start(), match.end(), 'LONGITUDE']]
                })
    
    return examples

def add_to_file(file_path: Path, entity_type: str, count: int):
    """Add examples to file."""
    examples = generate_realistic_examples(entity_type, count)
    
    # Read existing
    existing = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                existing.append(json.loads(line))
    
    # Append new examples
    existing.extend(examples)
    
    # Write back
    with open(file_path, 'w') as f:
        for item in existing:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return len(examples)

def main():
    """Main function."""
    base_dir = Path('cyber-train/entities-intent')
    
    # Files that need these entities
    files_to_update = {
        'vulnerability_mgmt': {'CVE_ID': 200},
        'threat_intelligence': {'THREAT_ACTOR': 100, 'WALLET_ADDRESS': 50, 'EMAIL_ADDRESS': 50, 'PHONE_NUMBER': 50},
        'incident_response': {'EMAIL_ADDRESS': 50, 'PHONE_NUMBER': 50, 'LATITUDE': 30, 'LONGITUDE': 30},
        'geoint': {'LATITUDE': 200, 'LONGITUDE': 200},
        'ai_security': {'CVE_ID': 50, 'EMAIL_ADDRESS': 30},
        'network_security': {'IP_ADDRESS': 50, 'EMAIL_ADDRESS': 30},
        'endpoint_security': {'EMAIL_ADDRESS': 30, 'PHONE_NUMBER': 30},
    }
    
    print("="*80)
    print("ADDING MISSING CRITICAL ENTITIES")
    print("="*80)
    
    total_added = 0
    for pillar, entities in files_to_update.items():
        file_path = base_dir / pillar / f"{pillar}_entities.jsonl"
        if not file_path.exists():
            # Try alternative names
            alt_paths = list(base_dir.rglob(f"*{pillar}*entities.jsonl"))
            if alt_paths:
                file_path = alt_paths[0]
            else:
                print(f"⚠️  {pillar}: File not found")
                continue
        
        print(f"\n{pillar}:")
        for entity_type, count in entities.items():
            if entity_type == 'THREAT_ACTOR':
                continue  # Already has these
            added = add_to_file(file_path, entity_type, count)
            total_added += added
            print(f"  ✅ Added {added} {entity_type} examples")
    
    print(f"\n✅ Total examples added: {total_added}")

if __name__ == '__main__':
    main()

