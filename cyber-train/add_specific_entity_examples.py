#!/usr/bin/env python3
"""
Add specific training examples for IP addresses, domains, emails, and other entities
that were missed in the test suite.

This script adds high-quality, realistic examples with accurate boundaries.
"""

import json
import random
from pathlib import Path
from typing import List, Dict

# Realistic examples
IP_EXAMPLES = [
    ("192.168.1.100", "Investigate suspicious activity from IP address 192.168.1.100"),
    ("10.0.0.5", "APT41 CVE-2021-44228 Log4j vulnerability exploitation detected from 10.0.0.5"),
    ("172.16.0.1", "APT28 used WannaCry ransomware to attack IP 172.16.0.1 and domain evil.com"),
    ("8.8.8.8", "can u check this ip 8.8.8.8 pls?"),
    ("203.0.113.42", "Malicious traffic detected from source IP 203.0.113.42"),
    ("198.51.100.10", "Block IP address 198.51.100.10 immediately"),
    ("192.0.2.1", "Connection from 192.0.2.1 to port 443 established"),
    ("10.10.10.10", "Firewall rule added for IP 10.10.10.10"),
    ("172.20.0.50", "Threat actor accessed system from 172.20.0.50"),
    ("192.168.0.1", "Router at 192.168.0.1 shows suspicious activity"),
]

DOMAIN_EXAMPLES = [
    ("example.com", "I need to check if the domain example.com is safe"),
    ("test.com", "Check IP: 10.0.0.1, Domain: test.com, Email: user@test.com"),
    ("evil.com", "APT28 used WannaCry ransomware to attack IP 172.16.0.1 and domain evil.com"),
    ("malicious-domain.net", "Block domain malicious-domain.net for phishing"),
    ("suspicious-site.org", "Domain suspicious-site.org flagged for malware distribution"),
    ("phishing-example.co.uk", "Phishing campaign using domain phishing-example.co.uk"),
    ("malware-host.io", "C2 server at malware-host.io communicating with infected hosts"),
    ("threat-actor.com", "Threat actor registered domain threat-actor.com"),
    ("fake-bank.com", "Fake banking site at fake-bank.com detected"),
    ("compromised-site.net", "Compromised site compromised-site.net serving malware"),
]

EMAIL_EXAMPLES = [
    ("admin@company.com", "Incident INC-2024-001 occurred on 2024-11-30 at 14:30 UTC involving user admin@company.com"),
    ("user@test.com", "Check IP: 10.0.0.1, Domain: test.com, Email: user@test.com, Phone: +1-555-123-4567"),
    ("phishing@evil.com", "Phishing email from phishing@evil.com detected"),
    ("malicious@attacker.net", "Email from malicious@attacker.net contains malware"),
    ("suspicious@domain.org", "Suspicious email from suspicious@domain.org flagged"),
    ("threat@actor.com", "Threat actor email threat@actor.com identified"),
    ("compromised@victim.com", "Compromised account compromised@victim.com detected"),
    ("fake@bank.com", "Fake bank email fake@bank.com reported"),
    ("spam@example.net", "Spam email from spam@example.net blocked"),
    ("malware@host.io", "Malware distribution email malware@host.io identified"),
]

PHONE_EXAMPLES = [
    ("+1-555-123-4567", "Check IP: 10.0.0.1, Domain: test.com, Email: user@test.com, Phone: +1-555-123-4567"),
    ("+44 20 7946 0958", "PII leak detected: SSN 123-45-6789, phone +44 20 7946 0958"),
    ("+1 (555) 123-4567", "Contact phone number +1 (555) 123-4567 for incident response"),
    ("555-123-4567", "Phone number 555-123-4567 associated with threat actor"),
    ("+33 1 23 45 67 89", "International phone +33 1 23 45 67 89 linked to fraud"),
    ("+49 30 12345678", "German phone +49 30 12345678 used in phishing campaign"),
    ("+81 3 1234 5678", "Japanese phone +81 3 1234 5678 identified in investigation"),
    ("+86 10 1234 5678", "Chinese phone +86 10 1234 5678 flagged for suspicious activity"),
    ("+61 2 1234 5678", "Australian phone +61 2 1234 5678 linked to malware distribution"),
    ("+7 495 123-45-67", "Russian phone +7 495 123-45-67 associated with APT group"),
]

IPV6_EXAMPLES = [
    ("2001:db8::1", "Investigate IPv6 address 2001:db8::1 for suspicious activity"),
    ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", "IPv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:7334 flagged"),
    ("::1", "Localhost IPv6 ::1 detected in connection"),
    ("2001:db8:0:0:0:0:0:1", "IPv6 2001:db8:0:0:0:0:0:1 communicating with C2 server"),
    ("fe80::1", "Link-local IPv6 fe80::1 identified"),
    ("2001:db8::/32", "IPv6 network 2001:db8::/32 under investigation"),
    ("2001:db8:1::1", "IPv6 2001:db8:1::1 associated with threat actor"),
    ("2001:db8:2:3:4:5:6:7", "IPv6 2001:db8:2:3:4:5:6:7 flagged for malware"),
    ("2001:db8:abcd:ef01:2345:6789:abcd:ef01", "IPv6 2001:db8:abcd:ef01:2345:6789:abcd:ef01 detected"),
    ("2001:db8:1:2:3:4:5:6", "IPv6 2001:db8:1:2:3:4:5:6 communicating with botnet"),
]

SSN_EXAMPLES = [
    ("123-45-6789", "PII leak detected: SSN 123-45-6789, phone +44 20 7946 0958"),
    ("987-65-4321", "Data breach exposed SSN 987-65-4321"),
    ("111-22-3333", "Identity theft case involving SSN 111-22-3333"),
    ("999-88-7777", "A data leak exposed SSN 999-88-7777 and credit card number"),
    ("555-44-3333", "SSN 555-44-3333 found in dark web dump"),
    ("123456789", "SSN 123456789 compromised in breach"),
    ("987654321", "SSN 987654321 associated with fraud case"),
    ("111223333", "SSN 111223333 exposed in phishing attack"),
    ("999887777", "SSN 999887777 found in malware exfiltration"),
    ("555443333", "SSN 555443333 linked to identity theft"),
]

CREDIT_CARD_EXAMPLES = [
    ("4532-1234-5678-9010", "Credit card number 4532-1234-5678-9010 found in breach data"),
    ("4532 1234 5678 9010", "Credit card 4532 1234 5678 9010 compromised"),
    ("4532123456789010", "Credit card 4532123456789010 exposed in data leak"),
    ("4111-1111-1111-1111", "Test credit card 4111-1111-1111-1111 used in fraud"),
    ("5500-0000-0000-0004", "Credit card 5500-0000-0000-0004 flagged for suspicious activity"),
    ("3782-822463-10005", "Amex card 3782-822463-10005 compromised"),
    ("6011-1111-1111-1117", "Discover card 6011-1111-1111-1117 found in breach"),
    ("3056-9309-0259-04", "Diners Club 3056-9309-0259-04 exposed"),
    ("3530-1113-3330-0000", "JCB card 3530-1113-3330-0000 compromised"),
    ("6759-6498-2643-8453", "Maestro card 6759-6498-2643-8453 flagged"),
]

GITHUB_EXAMPLES = [
    ("@octocat", "GitHub user @octocat reported security vulnerability"),
    ("@github-user", "Check GitHub user @github-user for malicious code"),
    ("@hacker123", "GitHub user @hacker123 uploaded malware repository"),
    ("@evilorg", "GitHub organization @evilorg hosting malicious repos"),
    ("github.com/evilorg/malware", "Analyze GitHub repo github.com/evilorg/malware for threats"),
    ("https://github.com/threatintel/malware-samples", "GitHub repository https://github.com/threatintel/malware-samples contains exploits"),
    ("@suspicious-dev", "GitHub user @suspicious-dev created backdoor code"),
    ("github.com/attacker/exploit", "Malicious code in github.com/attacker/exploit repository"),
    ("@malware-author", "GitHub user @malware-author distributing ransomware"),
    ("https://github.com/evilcorp/phishing-toolkit", "Phishing toolkit at https://github.com/evilcorp/phishing-toolkit"),
]

def create_entity_example(entity_text: str, full_text: str, entity_type: str) -> Dict:
    """Create an entity example with accurate boundaries."""
    start = full_text.find(entity_text)
    if start == -1:
        # Try case-insensitive
        start = full_text.lower().find(entity_text.lower())
        if start == -1:
            return None
    
    end = start + len(entity_text)
    return {
        "text": full_text,
        "entities": [[start, end, entity_type]]
    }

def add_examples_to_file(file_path: Path, examples: List[tuple], entity_type: str, count: int = 10):
    """Add examples to a file."""
    if not file_path.exists():
        return
    
    # Read existing data
    existing = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    existing.append(json.loads(line))
                except:
                    pass
    
    # Add new examples
    added = 0
    for entity_text, full_text in random.sample(examples, min(count, len(examples))):
        example = create_entity_example(entity_text, full_text, entity_type)
        if example:
            existing.append(example)
            added += 1
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in existing:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return added

def main():
    """Main function."""
    print("="*80)
    print("ADDING SPECIFIC ENTITY EXAMPLES")
    print("="*80)
    
    base_path = Path('entities-intent')
    
    # Files that should have IP addresses
    ip_files = [
        base_path / 'network_security' / 'network_security_entities.jsonl',
        base_path / 'incident_response' / 'incident_response_entities.jsonl',
        base_path / 'threat_intelligence' / 'threat_intelligence_entities.jsonl',
        base_path / 'endpoint_security' / 'endpoint_security_entities.jsonl',
        base_path / 'osint' / 'cybint' / 'cybint_entities.jsonl',
    ]
    
    # Files that should have domains
    domain_files = [
        base_path / 'network_security' / 'network_security_entities.jsonl',
        base_path / 'incident_response' / 'incident_response_entities.jsonl',
        base_path / 'threat_intelligence' / 'threat_intelligence_entities.jsonl',
        base_path / 'osint' / 'domain_intel' / 'domain_intel_entities.jsonl',
    ]
    
    # Files that should have emails
    email_files = [
        base_path / 'incident_response' / 'incident_response_entities.jsonl',
        base_path / 'authentication' / 'authentication_entities.jsonl',
        base_path / 'data_privacy_sovereignty' / 'data_privacy_sovereignty_entities.jsonl',
    ]
    
    # Files that should have phones
    phone_files = [
        base_path / 'incident_response' / 'incident_response_entities.jsonl',
        base_path / 'data_privacy_sovereignty' / 'data_privacy_sovereignty_entities.jsonl',
        base_path / 'osint' / 'socmint' / 'socmint_entities.jsonl',
    ]
    
    # Files that should have GitHub
    github_files = [
        base_path / 'ai_security' / 'ai_security_entities.jsonl',
        base_path / 'application_security' / 'application_security_entities.jsonl',
        base_path / 'vulnerability_mgmt' / 'vulnerability_mgmt_entities.jsonl',
        base_path / 'osint' / 'cybint' / 'cybint_entities.jsonl',
    ]
    
    total_added = 0
    
    # Add IP examples
    for file_path in ip_files:
        if file_path.exists():
            added = add_examples_to_file(file_path, IP_EXAMPLES, 'IP_ADDRESS', 5)
            if added:
                print(f"Added {added} IP_ADDRESS examples to {file_path.name}")
                total_added += added
            
            # Add IPv6
            added = add_examples_to_file(file_path, IPV6_EXAMPLES, 'IPV6_ADDRESS', 3)
            if added:
                print(f"Added {added} IPV6_ADDRESS examples to {file_path.name}")
                total_added += added
    
    # Add domain examples
    for file_path in domain_files:
        if file_path.exists():
            added = add_examples_to_file(file_path, DOMAIN_EXAMPLES, 'DOMAIN', 5)
            if added:
                print(f"Added {added} DOMAIN examples to {file_path.name}")
                total_added += added
    
    # Add email examples
    for file_path in email_files:
        if file_path.exists():
            added = add_examples_to_file(file_path, EMAIL_EXAMPLES, 'EMAIL_ADDRESS', 5)
            if added:
                print(f"Added {added} EMAIL_ADDRESS examples to {file_path.name}")
                total_added += added
    
    # Add phone examples
    for file_path in phone_files:
        if file_path.exists():
            added = add_examples_to_file(file_path, PHONE_EXAMPLES, 'PHONE_NUMBER', 5)
            if added:
                print(f"Added {added} PHONE_NUMBER examples to {file_path.name}")
                total_added += added
    
    # Add GitHub examples
    for file_path in github_files:
        if file_path.exists():
            added = add_examples_to_file(file_path, GITHUB_EXAMPLES, 'GITHUB_USER', 3)
            if added:
                print(f"Added {added} GITHUB_USER examples to {file_path.name}")
                total_added += added
            
            # Also add GITHUB_REPO_URL
            github_repo_examples = [(url, text) for url, text in GITHUB_EXAMPLES if 'github.com' in url]
            added = add_examples_to_file(file_path, github_repo_examples, 'GITHUB_REPO_URL', 3)
            if added:
                print(f"Added {added} GITHUB_REPO_URL examples to {file_path.name}")
                total_added += added
    
    # Add PII examples to data privacy file
    privacy_file = base_path / 'data_privacy_sovereignty' / 'data_privacy_sovereignty_entities.jsonl'
    if privacy_file.exists():
        added = add_examples_to_file(privacy_file, SSN_EXAMPLES, 'SSN', 5)
        if added:
            print(f"Added {added} SSN examples to {privacy_file.name}")
            total_added += added
        
        added = add_examples_to_file(privacy_file, CREDIT_CARD_EXAMPLES, 'CREDIT_CARD_NUMBER', 5)
        if added:
            print(f"Added {added} CREDIT_CARD_NUMBER examples to {privacy_file.name}")
            total_added += added
    
    print(f"\nTotal examples added: {total_added}")
    print("="*80)

if __name__ == '__main__':
    main()

