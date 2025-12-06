#!/usr/bin/env python3
"""
Expand missed entity examples by generating more unique examples dynamically.
This script generates additional examples beyond the initial set.
"""

import json
import re
import random
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set, Tuple, Optional
from datetime import datetime, timedelta

# Track added entities
added_entities: Dict[str, Set[str]] = defaultdict(set)


def generate_malware_examples(count: int) -> List[Tuple[str, str, str]]:
    """Generate unique malware examples."""
    malware_names = [
        "WannaCry", "NotPetya", "Zeus", "Emotet", "TrickBot", "Stuxnet",
        "Conficker", "Code Red", "Ryuk", "LockBit", "REvil", "Maze",
        "Sodinokibi", "GandCrab", "Cerber", "CryptoLocker", "Petya",
        "SamSam", "BadRabbit", "Dharma", "Conti", "BlackBasta", "ALPHV",
        "DarkSide", "Babuk", "Avaddon", "DoppelPaymer", "Egregor", "Mespinoza"
    ]
    
    contexts = [
        "ransomware has been detected in the network infrastructure, requiring immediate containment",
        "malware variant spreading through the enterprise network, causing significant disruption",
        "trojan was found on several endpoints, indicating a potential financial fraud campaign",
        "malware family has been actively distributing through malicious email attachments",
        "trojan was detected attempting to establish command and control communications",
        "worm was discovered targeting industrial control systems, representing a sophisticated attack",
        "worm continues to propagate across unpatched systems, requiring immediate patch deployment",
        "worm variant was identified scanning for vulnerable web servers",
        "ransomware has encrypted critical business files, demanding cryptocurrency payment",
        "ransomware group has deployed their malware variant, exfiltrating sensitive data",
        "ransomware was detected in the environment, targeting high-value assets",
        "ransomware campaign has compromised multiple systems, threatening to publish stolen data",
        "ransomware variant has been identified, using sophisticated encryption algorithms",
        "ransomware family has been active, targeting organizations with weak security postures",
        "ransomware was found on several workstations, encrypting local files and network shares",
        "ransomware has been detected, using strong encryption to render files inaccessible",
        "ransomware variant has infected the master boot record, preventing system startup",
        "ransomware has been deployed through compromised credentials, targeting specific systems",
        "ransomware was identified spreading through fake software updates",
        "ransomware family has been active, using automated distribution methods"
    ]
    
    examples = []
    used = set()
    
    for _ in range(count):
        malware = random.choice(malware_names)
        context = random.choice(contexts)
        
        # Ensure uniqueness
        key = f"{malware}:{context[:50]}"
        if key in used:
            continue
        used.add(key)
        
        text = f"The security team identified {malware} {context} to critical systems and infrastructure."
        examples.append((text, malware, "MALWARE_TYPE"))
    
    return examples


def generate_hash_examples(count: int) -> List[Tuple[str, str, str]]:
    """Generate unique hash examples."""
    hash_types = ["MD5", "SHA1", "SHA256"]
    contexts = [
        "was calculated for the suspicious executable file during forensic analysis",
        "was verified against the known good baseline for system files",
        "was submitted to threat intelligence platforms for analysis",
        "was computed for the compromised database backup file",
        "was used to identify the malicious payload",
        "was computed for the empty file, confirming no data corruption",
        "was verified for the application binary before deployment to production",
        "was generated for the system configuration file",
        "was calculated for the suspicious process memory dump",
        "differs from the baseline, triggering security alert",
        "was included in the malware analysis report for the malicious payload sample",
        "was computed during the digital forensics investigation",
        "was verified for the system library file to ensure authenticity",
        "was used to identify the compromised application binary"
    ]
    
    examples = []
    used = set()
    
    for _ in range(count):
        hash_type = random.choice(hash_types)
        context = random.choice(contexts)
        
        # Generate random hash
        if hash_type == "MD5":
            hash_value = ''.join(random.choices('0123456789abcdef', k=32))
        elif hash_type == "SHA1":
            hash_value = ''.join(random.choices('0123456789abcdef', k=40))
        else:  # SHA256
            hash_value = ''.join(random.choices('0123456789abcdef', k=64))
        
        key = f"{hash_value}"
        if key in used:
            continue
        used.add(key)
        
        text = f"The file integrity check revealed {hash_type} hash {hash_value} {context}."
        examples.append((text, hash_value, "HASH"))
    
    return examples


def generate_date_examples(count: int) -> List[Tuple[str, str, str]]:
    """Generate unique date examples."""
    base_date = datetime.now()
    formats = [
        ("%Y-%m-%d", "The security incident occurred on {}, requiring immediate incident response"),
        ("%m/%d/%Y", "The vulnerability was discovered on {}, affecting multiple systems"),
        ("%d-%m-%Y", "The data breach was detected on {}, compromising sensitive customer information"),
        ("%B %d, %Y", "The security audit was completed on {}, identifying several compliance gaps"),
    ]
    
    contexts = [
        "and requiring urgent patch deployment",
        "and triggering regulatory notification requirements",
        "and recommending remediation actions",
        "for active threat campaigns",
        "targeting critical infrastructure",
        "educating employees about phishing attacks",
        "evaluating adherence to regulatory requirements"
    ]
    
    examples = []
    used = set()
    
    for i in range(count):
        fmt, template = random.choice(formats)
        date_obj = base_date + timedelta(days=random.randint(-365, 365))
        date_str = date_obj.strftime(fmt)
        
        key = date_str
        if key in used:
            continue
        used.add(key)
        
        context = random.choice(contexts)
        text = f"{template.format(date_str)} {context}."
        examples.append((text, date_str, "DATE"))
    
    return examples


def generate_url_examples(count: int) -> List[Tuple[str, str, str]]:
    """Generate unique URL examples."""
    domains = [
        "malicious-domain.com", "compromised-server.net", "fake-bank.com",
        "c2-server.com", "malware-distribution.net", "data-theft.com",
        "attack-vector.com", "legitimate-looking.com", "c2-infrastructure.com",
        "breach-notification.com", "malware-campaign.com", "suspicious-domain.org",
        "fake-service.com", "threat-actor.com", "phishing-campaign.net"
    ]
    
    paths = [
        "/phishing-page", "/exploit", "/login", "/beacon", "/payload.exe",
        "/upload", "/exploit", "/malicious", "/register", "/alert",
        "/download", "/scan", "/verify", "/command", "/threat-intel"
    ]
    
    contexts = [
        "attempting to steal user credentials through social engineering",
        "hosting malware and command and control infrastructure",
        "designed to harvest banking credentials and compromise customer accounts",
        "indicating potential command and control communication with threat actors",
        "during execution and system compromise",
        "through encrypted communication channels",
        "attempting to exploit known vulnerabilities",
        "to host phishing content and bypass traditional security controls",
        "to manage infected systems",
        "indicating potential customer data exposure"
    ]
    
    examples = []
    used = set()
    
    for _ in range(count):
        domain = random.choice(domains)
        path = random.choice(paths)
        protocol = random.choice(["https://", "http://"])
        url = f"{protocol}{domain}{path}"
        context = random.choice(contexts)
        
        key = url
        if key in used:
            continue
        used.add(key)
        
        text = f"The security team identified malicious URL {url} {context}."
        examples.append((text, url, "URL"))
    
    return examples


def generate_phone_examples(count: int) -> List[Tuple[str, str, str]]:
    """Generate unique phone number examples."""
    formats = [
        "+1-555-{}-{}", "+44 20 {} {}", "+49 30 {} {}", "1-800-555-{}",
        "+33 1 {} {}", "(555) {}-{}", "+81 3 {} {}", "555.{}.{}",
        "+61 2 {} {}", "+1 (555) {}-{}", "+86 10 {} {}"
    ]
    
    contexts = [
        "reporting potential data breach and unauthorized access",
        "to contact victims and conduct social engineering attacks",
        "with the vendor to confirm legitimate business communication",
        "for reporting security incidents and requesting immediate assistance",
        "used in phishing campaign targeting European customers",
        "for regulatory reporting and communication with law enforcement",
        "associated with threat actor group conducting cyber espionage",
        "as example of social engineering attack vector",
        "to coordinate with international security partners",
        "for vendor contact information and supply chain security"
    ]
    
    examples = []
    used = set()
    
    for _ in range(count):
        fmt = random.choice(formats)
        # Generate random digits
        parts = [str(random.randint(100, 999)) for _ in range(fmt.count('{}'))]
        phone = fmt.format(*parts)
        context = random.choice(contexts)
        
        key = phone
        if key in used:
            continue
        used.add(key)
        
        text = f"The security incident hotline received call from phone number {phone} {context}."
        examples.append((text, phone, "PHONE_NUMBER"))
    
    return examples


def find_entity_position(text: str, entity: str) -> Optional[Tuple[int, int]]:
    """Find the position of entity in text."""
    start = text.find(entity)
    if start == -1:
        return None
    end = start + len(entity)
    return (start, end)


def is_unique(entity_type: str, entity_text: str) -> bool:
    """Check if entity is unique."""
    entity_key = f"{entity_type}:{entity_text.lower()}"
    if entity_key in added_entities[entity_type]:
        return False
    added_entities[entity_type].add(entity_key)
    return True


def add_examples_to_file(file_path: Path, examples: List[Tuple[str, str, str]], entity_type: str, count: int):
    """Add examples to a JSONL file."""
    added = 0
    unique_examples = []
    
    for text, entity, label in examples:
        if not is_unique(entity_type, entity):
            continue
        
        pos = find_entity_position(text, entity)
        if pos is None:
            continue
        start, end = pos
        
        unique_examples.append({
            "text": text,
            "entities": [[start, end, label]]
        })
        
        added += 1
        if added >= count:
            break
    
    if unique_examples:
        with open(file_path, 'a', encoding='utf-8') as f:
            for example in unique_examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    return added


def get_relevant_files(entity_type: str, base_dir: Path) -> List[Path]:
    """Get relevant files for entity type."""
    mapping = {
        "MALWARE_TYPE": ["threat_intel", "incident_response", "endpoint_security"],
        "HASH": ["incident_response", "threat_intel", "endpoint_security"],
        "DATE": ["incident_response", "audit_compliance", "threat_intel"],
        "URL": ["network_security", "threat_intel", "incident_response"],
        "PHONE_NUMBER": ["threat_intel", "incident_response"],
    }
    
    relevant_pillars = mapping.get(entity_type, ["threat_intel", "incident_response"])
    files = []
    
    for pillar in relevant_pillars:
        pillar_dir = base_dir / pillar
        entity_file = pillar_dir / f"{pillar}_entities.jsonl"
        if entity_file.exists():
            files.append(entity_file)
    
    return files if files else [base_dir / "threat_intel" / "threat_intel_entities.jsonl"]


def main():
    base_dir = Path("entities-intent")
    
    print("="*80)
    print("EXPAND MISSED ENTITY EXAMPLES")
    print("="*80)
    print("\nGenerating additional unique examples:")
    print("  - MALWARE_TYPE: 180 more examples")
    print("  - HASH: 187 more examples")
    print("  - DATE: 200 more examples")
    print("  - URL: 136 more examples")
    print("  - PHONE_NUMBER: 139 more examples")
    print()
    
    entity_configs = [
        ("MALWARE_TYPE", generate_malware_examples, 180),
        ("HASH", generate_hash_examples, 187),
        ("DATE", generate_date_examples, 200),
        ("URL", generate_url_examples, 136),
        ("PHONE_NUMBER", generate_phone_examples, 139),
    ]
    
    total_added = defaultdict(int)
    
    for entity_type, generator_func, target_count in entity_configs:
        print(f"📝 Generating {entity_type} examples...")
        examples = generator_func(target_count * 2)  # Generate extra for uniqueness
        files = get_relevant_files(entity_type, base_dir)
        
        examples_per_file = max(1, target_count // len(files))
        remaining = target_count
        
        for file_path in files:
            if not file_path.exists():
                continue
            
            count = min(examples_per_file, remaining)
            if count <= 0:
                break
            
            added = add_examples_to_file(file_path, examples, entity_type, count)
            total_added[entity_type] += added
            remaining -= added
            
            if remaining <= 0:
                break
        
        print(f"   ✅ Added {total_added[entity_type]} {entity_type} examples")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    for entity_type, count in sorted(total_added.items()):
        print(f"  {entity_type}: {count}")
    print(f"\nTotal: {sum(total_added.values())} examples")
    print("="*80)


if __name__ == "__main__":
    main()

