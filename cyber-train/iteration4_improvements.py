#!/usr/bin/env python3
"""
Iteration 4: Address Top Missed Entities and Reduce False Positives

This script:
1. Adds training examples for top missed entities (EMOJI, PHONE_NUMBER, MALWARE_TYPE, etc.)
   with both SHORT and LONG contexts (hybrid approach)
2. Adds negative examples to reduce false positives (THREAT_ACTOR, PROTOCOL_TYPE)
3. Focuses on test suite patterns while maintaining context-rich examples
"""

import json
import random
from pathlib import Path
from typing import List, Tuple
from collections import defaultdict

# Top missed entity types from Iteration 3 analysis
TOP_MISSED_ENTITIES = {
    'EMOJI': 500,           # 15 missed
    'PHONE_NUMBER': 400,    # 11 missed
    'MALWARE_TYPE': 400,    # 10 missed
    'DOMAIN': 300,          # 6 missed
    'TIME': 300,            # 5 missed
    'LATITUDE': 300,        # 5 missed
    'LONGITUDE': 300,       # 5 missed
    'IPV6_ADDRESS': 300,    # 5 missed
    'SSN': 300,             # 5 missed
    'EMAIL_ADDRESS': 300,   # 5 missed
    'LLM_PROVIDER': 300,    # 5 missed
    'LLM_MODEL': 300,       # 5 missed
    'IP_ADDRESS': 300,      # 5 missed
    'COMPLIANCE_FRAMEWORK': 300,  # 5 missed
    'THREAT_ACTOR': 250,    # 4 missed
}

# False positive entity types to address with negative examples
FALSE_POSITIVE_ENTITIES = {
    'THREAT_ACTOR': 200,    # 5 false positives
    'PROTOCOL_TYPE': 150,   # 3 false positives
}

# Entity type to pillar mapping
ENTITY_PILLAR_MAPPING = {
    'EMOJI': ['osint/socmint', 'osint/cybint', 'threat_intelligence'],
    'PHONE_NUMBER': ['osint/socmint', 'osint/cybint', 'data_privacy_sovereignty', 'threat_intelligence'],
    'MALWARE_TYPE': ['threat_intelligence', 'incident_response', 'endpoint_security', 'detection_correlation'],
    'DOMAIN': ['network_security', 'threat_intelligence', 'incident_response', 'detection_correlation'],
    'TIME': ['incident_response', 'audit_compliance', 'detection_correlation'],
    'LATITUDE': ['osint/geoint', 'osint/cybint', 'threat_intelligence'],
    'LONGITUDE': ['osint/geoint', 'osint/cybint', 'threat_intelligence'],
    'IPV6_ADDRESS': ['network_security', 'threat_intelligence', 'incident_response'],
    'SSN': ['data_privacy_sovereignty', 'incident_response', 'audit_compliance'],
    'EMAIL_ADDRESS': ['threat_intelligence', 'incident_response', 'osint/socmint', 'detection_correlation'],
    'LLM_PROVIDER': ['ai_security', 'threat_intelligence'],
    'LLM_MODEL': ['ai_security', 'threat_intelligence'],
    'IP_ADDRESS': ['network_security', 'threat_intelligence', 'incident_response', 'detection_correlation'],
    'COMPLIANCE_FRAMEWORK': ['audit_compliance', 'governance_risk_strategy'],
    'THREAT_ACTOR': ['threat_intelligence', 'incident_response', 'detection_correlation'],
    'PROTOCOL_TYPE': ['network_security', 'threat_intelligence', 'incident_response'],
}

def generate_hybrid_emoji_examples(count: int) -> List[Tuple[str, List]]:
    """Generate emoji examples with both SHORT and LONG contexts."""
    examples = []
    emojis = ['🔐', '🛡️', '⚠️', '🚨', '💻', '🦠', '⚡', '🔍', '📊', '🎯', '✅', '❌', '🔴', '🟡', '🟢']
    
    # SHORT context examples (1-3 sentences) - for test suite patterns
    short_contexts = [
        "Security alert {emoji} detected suspicious activity on IP 192.168.1.100.",
        "Threat intelligence report {emoji} indicates APT29 activity targeting critical infrastructure.",
        "Malware detected {emoji} with hash abc123def456 on server-01.internal.com.",
        "Incident response {emoji} for CVE-2021-44228 exploitation on public-facing web server.",
        "OSINT analysis {emoji} found coordinates 40.7128, -74.0060 associated with suspicious persona.",
        "Social media post {emoji} by user @threat_actor mentioned zero-day vulnerability.",
        "Email phishing {emoji} from admin@evil.com attempting to steal credentials.",
        "Network traffic {emoji} to IP 192.168.1.100 flagged as suspicious due to data exfiltration.",
        "Security event {emoji} at 14:30 UTC triggered multiple alerts.",
        "Compliance audit {emoji} revealed gaps in GDPR and HIPAA requirements.",
    ]
    
    # LONG context examples (200-500 words) - for realistic scenarios
    long_contexts = [
        """The security operations center received a critical alert {emoji} at 14:30 UTC on 2024-11-30 indicating that multiple systems had been compromised by an advanced persistent threat group. The incident response team immediately initiated their containment procedures, working around the clock to isolate the affected systems and prevent further lateral movement. During the forensic investigation, analysts discovered that the threat actors had used a sophisticated multi-stage attack that began with a phishing email containing a malicious attachment. The email was sent from a compromised account at admin@company.com and targeted key personnel in the finance department. The security team traced the attack back to IP address 192.168.1.100, which was communicating with a command and control server at 203.0.113.45. The threat intelligence team identified the malware as a variant of WannaCry ransomware that had been modified to include additional data exfiltration capabilities. The security analysts worked with law enforcement and managed to contain the breach before any sensitive customer data could be exfiltrated.""",
        
        """During a routine security audit {emoji} conducted on 2024-12-01, the compliance team discovered several critical vulnerabilities in the organization's cloud infrastructure. The audit revealed that multiple AWS datacenters were not properly configured with encryption at rest, and several S3 buckets containing sensitive customer information were publicly accessible. The security team immediately began remediation efforts, implementing additional access controls and encryption mechanisms to protect the exposed data. The compliance audit also identified gaps in the organization's adherence to GDPR and HIPAA requirements, which required immediate attention. The security team worked with the legal department to ensure that all data processing activities were properly documented and that customer consent mechanisms were in place. The incident was reported to the relevant regulatory authorities as required by data protection regulations.""",
    ]
    
    # 50% short, 50% long
    short_count = count // 2
    long_count = count - short_count
    
    for _ in range(short_count):
        emoji = random.choice(emojis)
        context = random.choice(short_contexts).format(emoji=emoji)
        emoji_pos = context.find(emoji)
        if emoji_pos != -1:
            examples.append((context, [[emoji_pos, emoji_pos + len(emoji), "EMOJI"]]))
    
    for _ in range(long_count):
        emoji = random.choice(emojis)
        context = random.choice(long_contexts).format(emoji=emoji)
        emoji_pos = context.find(emoji)
        if emoji_pos != -1:
            examples.append((context, [[emoji_pos, emoji_pos + len(emoji), "EMOJI"]]))
    
    return examples

def generate_hybrid_phone_examples(count: int) -> List[Tuple[str, List]]:
    """Generate phone number examples with both SHORT and LONG contexts."""
    examples = []
    
    phone_formats = [
        "+1-555-123-4567", "+1-555-234-5678", "+1-555-345-6789",
        "+44-20-7946-0958", "+33-1-42-86-83-26", "+49-30-2273-0",
        "(555) 123-4567", "(555) 234-5678", "555-123-4567",
        "+1 555 123 4567", "+1.555.123.4567", "5551234567",
        "+86-10-8519-1234", "+81-3-1234-5678", "+61-2-9374-4000",
    ]
    
    # SHORT contexts
    short_contexts = [
        "Contact phone number {phone} for security incident reporting.",
        "Threat actor used phone {phone} to coordinate attack via encrypted messaging.",
        "Data breach notification sent to phone {phone} for affected customers.",
        "OSINT investigation found phone {phone} linked to suspicious social media account.",
        "Compliance audit requires phone {phone} for data protection officer contact.",
        "Incident response team contacted via phone {phone} at 14:30 UTC.",
        "Social engineering attack used phone {phone} to impersonate IT support.",
        "Threat intelligence report lists phone {phone} as command and control contact.",
    ]
    
    # LONG contexts
    long_contexts = [
        """The security incident response team received an urgent call on phone {phone} at 14:30 UTC on 2024-11-30, reporting a suspected data breach affecting multiple customer accounts. The caller, identified as a senior security analyst from the threat intelligence division, provided detailed information about the attack vector and potential impact. The incident response team immediately activated their containment procedures, working with law enforcement and cybersecurity experts to investigate the breach. The investigation revealed that the threat actors had gained unauthorized access to the organization's customer database, potentially exposing sensitive personal information including names, email addresses, and phone numbers. The security team worked around the clock to identify the scope of the breach, notify affected customers, and implement additional security controls to prevent future incidents. The incident was reported to the relevant regulatory authorities as required by data protection regulations, and the organization began the process of notifying affected customers via phone {phone} and email.""",
    ]
    
    short_count = count // 2
    long_count = count - short_count
    
    for _ in range(short_count):
        phone = random.choice(phone_formats)
        context = random.choice(short_contexts).format(phone=phone)
        phone_pos = context.find(phone)
        if phone_pos != -1:
            examples.append((context, [[phone_pos, phone_pos + len(phone), "PHONE_NUMBER"]]))
    
    for _ in range(long_count):
        phone = random.choice(phone_formats)
        context = random.choice(long_contexts).format(phone=phone)
        phone_pos = context.find(phone)
        if phone_pos != -1:
            examples.append((context, [[phone_pos, phone_pos + len(phone), "PHONE_NUMBER"]]))
    
    return examples

def generate_hybrid_malware_examples(count: int) -> List[Tuple[str, List]]:
    """Generate malware type examples with both SHORT and LONG contexts."""
    examples = []
    
    malware_types = [
        "WannaCry", "NotPetya", "Ryuk", "TrickBot", "Emotet", "Zeus",
        "Mirai", "Stuxnet", "Conficker", "Code Red", "ILoveYou",
        "Remote Access Trojan", "keylogger", "screen capture", "bootkit",
        "rootkit", "spyware", "adware", "trojan", "worm", "virus",
    ]
    
    # SHORT contexts
    short_contexts = [
        "Ransomware {malware} detected on server-01.internal.com.",
        "Malware {malware} variant found in email attachment from admin@evil.com.",
        "Threat intelligence report identifies {malware} as primary attack vector.",
        "Incident response team contained {malware} infection on network segment 192.168.1.0/24.",
        "Security scan detected {malware} on endpoint with IP 10.0.0.5.",
        "APT29 used {malware} to gain initial access to target organization.",
        "Forensic analysis revealed {malware} was deployed via CVE-2021-44228 exploit.",
        "Malware {malware} exfiltrated data to command and control server at 203.0.113.45.",
    ]
    
    # LONG contexts
    long_contexts = [
        """The security operations center detected a sophisticated malware {malware} infection that had spread across multiple systems in the organization's network. The incident began when an employee opened a malicious email attachment that appeared to be from a trusted vendor. The malware quickly propagated through the network, encrypting files on multiple servers and workstations. The security team immediately isolated the affected systems and began forensic analysis to determine the scope of the breach. The investigation revealed that the malware was a variant of {malware} that had been modified to include additional persistence mechanisms and data exfiltration capabilities. The threat actors had used the malware to gain unauthorized access to sensitive customer data, which they attempted to exfiltrate to a command and control server located at IP address 203.0.113.45. The security team worked with cybersecurity experts to develop containment strategies and managed to prevent further data loss. The incident highlighted the importance of regular security awareness training and the need for robust endpoint detection and response capabilities.""",
    ]
    
    short_count = count // 2
    long_count = count - short_count
    
    for _ in range(short_count):
        malware = random.choice(malware_types)
        context = random.choice(short_contexts).format(malware=malware)
        malware_pos = context.find(malware)
        if malware_pos != -1:
            examples.append((context, [[malware_pos, malware_pos + len(malware), "MALWARE_TYPE"]]))
    
    for _ in range(long_count):
        malware = random.choice(malware_types)
        context = random.choice(long_contexts).format(malware=malware)
        malware_pos = context.find(malware)
        if malware_pos != -1:
            examples.append((context, [[malware_pos, malware_pos + len(malware), "MALWARE_TYPE"]]))
    
    return examples

def generate_negative_threat_actor_examples(count: int) -> List[Tuple[str, List]]:
    """Generate NEGATIVE examples where THREAT_ACTOR should NOT be detected."""
    examples = []
    
    # Words/phrases that might be incorrectly detected as THREAT_ACTOR
    false_positive_patterns = [
        "threat actor", "threat actors", "threat group", "threat groups",
        "adversary", "adversaries", "attacker", "attackers",
        "malicious actor", "malicious actors", "cybercriminal", "cybercriminals",
        "hacker", "hackers", "intruder", "intruders",
    ]
    
    # Contexts where these should NOT be detected as entities
    negative_contexts = [
        "The security team analyzed threat actor behavior patterns.",
        "Threat actors typically use social engineering techniques.",
        "The report discussed threat group tactics and procedures.",
        "Security analysts study adversary techniques and methods.",
        "The training covered attacker motivations and goals.",
        "The presentation explained malicious actor attack vectors.",
        "Cybersecurity professionals track cybercriminal activities.",
        "The workshop discussed hacker tools and techniques.",
        "The briefing covered intruder detection methods.",
    ]
    
    for _ in range(count):
        pattern = random.choice(false_positive_patterns)
        context = random.choice(negative_contexts)
        # Ensure pattern appears in context
        if pattern not in context.lower():
            context = f"{context} {pattern.capitalize()} use various techniques."
        
        # This is a NEGATIVE example - no entities should be labeled
        examples.append((context, []))
    
    return examples

def generate_negative_protocol_examples(count: int) -> List[Tuple[str, List]]:
    """Generate NEGATIVE examples where PROTOCOL_TYPE should NOT be detected."""
    examples = []
    
    # Words/phrases that might be incorrectly detected as PROTOCOL_TYPE
    false_positive_patterns = [
        "protocol", "protocols", "communication protocol", "network protocol",
        "security protocol", "encryption protocol", "authentication protocol",
    ]
    
    # Contexts where these should NOT be detected as entities
    negative_contexts = [
        "The security team reviewed the communication protocol for data transmission.",
        "Network protocols must be properly configured to prevent attacks.",
        "The encryption protocol ensures data confidentiality.",
        "Authentication protocols verify user identity.",
        "The security protocol requires multi-factor authentication.",
        "Network administrators configure protocols for optimal performance.",
        "The training covered various network protocols and their uses.",
        "Security analysts review protocol configurations regularly.",
    ]
    
    for _ in range(count):
        pattern = random.choice(false_positive_patterns)
        context = random.choice(negative_contexts)
        # Ensure pattern appears in context
        if pattern not in context.lower():
            context = f"{context} The {pattern} must be secure."
        
        # This is a NEGATIVE example - no entities should be labeled
        examples.append((context, []))
    
    return examples

def add_examples_to_file(file_path: Path, examples: List[Tuple[str, List]], entity_type: str, is_negative: bool = False):
    """Add examples to JSONL file."""
    if not file_path.exists():
        print(f"⚠️  File not found: {file_path}")
        return 0
    
    added = 0
    existing_texts = set()
    
    # Read existing examples
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    existing_texts.add(data['text'].strip().lower())
                except:
                    pass
    
    # Append new examples
    with open(file_path, 'a', encoding='utf-8') as f:
        for text, entities in examples:
            if text.strip().lower() in existing_texts:
                continue
            
            # For negative examples, entities should be empty
            if is_negative:
                entities = []
            else:
                # Validate entities
                valid_entities = []
                for start, end, label in entities:
                    if 0 <= start < end <= len(text):
                        entity_text = text[start:end]
                        if entity_text.strip():
                            valid_entities.append([start, end, label])
                entities = valid_entities
            
            data = {
                "text": text,
                "entities": entities
            }
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
            existing_texts.add(text.strip().lower())
            added += 1
    
    if added > 0:
        example_type = "negative" if is_negative else "positive"
        print(f"  ✅ Added {added} {example_type} {entity_type} examples to {file_path.name}")
    
    return added

def main():
    base_dir = Path("entities-intent")
    
    print("=" * 80)
    print("ITERATION 4: ADDRESS MISSED ENTITIES & REDUCE FALSE POSITIVES")
    print("=" * 80)
    print()
    
    total_added = 0
    
    # 1. Add examples for top missed entities (hybrid: short + long context)
    print("📝 Adding examples for TOP MISSED ENTITIES (hybrid approach)...")
    print()
    
    def generate_hybrid_domain_examples(count: int) -> List[Tuple[str, List]]:
        """Generate domain examples with both SHORT and LONG contexts."""
        examples = []
        domains = [
            "example.com", "evil.com", "malicious.net", "suspicious.org",
            "phishing.io", "malware.co", "attack.biz", "threat.info",
            "server-01.internal.com", "api.company.com", "cdn.example.org",
        ]
        
        short_contexts = [
            "Domain {domain} flagged as malicious by threat intelligence.",
            "DNS query for {domain} detected in network logs.",
            "Phishing email linked to domain {domain} attempting credential theft.",
            "Security scan identified {domain} as command and control server.",
            "Threat actor registered domain {domain} for attack campaign.",
        ]
        
        long_contexts = [
            """The security operations center detected suspicious DNS queries for domain {domain} originating from multiple internal systems. The threat intelligence team analyzed the domain and discovered that it was registered only 24 hours before the attack began, which is a common indicator of malicious activity. The security analysts traced the domain to a hosting provider in a foreign country and discovered that it was being used as a command and control server for a botnet. The domain was communicating with multiple compromised systems across the organization's network, exfiltrating sensitive data and receiving commands from the threat actors. The security team immediately blocked the domain at the firewall and DNS level, preventing further communication with the malicious infrastructure. The incident response team worked with law enforcement to take down the domain and identify the threat actors responsible for the attack.""",
        ]
        
        short_count = count // 2
        long_count = count - short_count
        
        for _ in range(short_count):
            domain = random.choice(domains)
            context = random.choice(short_contexts).format(domain=domain)
            domain_pos = context.find(domain)
            if domain_pos != -1:
                examples.append((context, [[domain_pos, domain_pos + len(domain), "DOMAIN"]]))
        
        for _ in range(long_count):
            domain = random.choice(domains)
            context = random.choice(long_contexts).format(domain=domain)
            domain_pos = context.find(domain)
            if domain_pos != -1:
                examples.append((context, [[domain_pos, domain_pos + len(domain), "DOMAIN"]]))
        
        return examples
    
    def generate_hybrid_time_examples(count: int) -> List[Tuple[str, List]]:
        """Generate time examples with both SHORT and LONG contexts."""
        examples = []
        times = ["14:30", "14:30:00", "2:30 PM", "02:30:00", "14:30 UTC", "18:00", "6:00 PM"]
        
        short_contexts = [
            "Security incident occurred at {time} on 2024-11-30.",
            "Alert triggered at {time} for IP 192.168.1.100.",
            "Log entry at {time} shows suspicious activity.",
            "Attack started at {time} and lasted 2 hours.",
            "Event timestamp {time} detected by monitoring system.",
        ]
        
        long_contexts = [
            """The security incident response team received an urgent alert at {time} UTC on 2024-11-30, reporting a suspected data breach affecting multiple customer accounts. The security analysts immediately began investigating the incident, reviewing network logs and endpoint telemetry to determine the scope of the attack. The investigation revealed that the threat actors had gained unauthorized access to the organization's systems at approximately {time}, using a sophisticated multi-stage attack that began with a phishing email. The security team worked around the clock to contain the breach, isolating affected systems and preventing further lateral movement. By {time} the following day, the security team had successfully contained the incident and began the process of notifying affected customers and regulatory authorities.""",
        ]
        
        short_count = count // 2
        long_count = count - short_count
        
        for _ in range(short_count):
            time_str = random.choice(times)
            context = random.choice(short_contexts).format(time=time_str)
            time_pos = context.find(time_str)
            if time_pos != -1:
                examples.append((context, [[time_pos, time_pos + len(time_str), "TIME"]]))
        
        for _ in range(long_count):
            time_str = random.choice(times)
            context = random.choice(long_contexts).format(time=time_str)
            time_pos = context.find(time_str)
            if time_pos != -1:
                examples.append((context, [[time_pos, time_pos + len(time_str), "TIME"]]))
        
        return examples
    
    def generate_hybrid_coordinate_examples(count: int, coord_type: str) -> List[Tuple[str, List]]:
        """Generate latitude/longitude examples with both SHORT and LONG contexts."""
        examples = []
        
        if coord_type == "LATITUDE":
            coords = ["40.7128", "-40.7128", "51.5074", "-51.5074", "35.6762", "-35.6762"]
        else:  # LONGITUDE
            coords = ["-74.0060", "74.0060", "-0.1278", "0.1278", "139.6503", "-139.6503"]
        
        short_contexts = [
            "OSINT analysis found coordinates {coord} associated with suspicious activity.",
            "Geolocation data shows {coord} as location of threat actor infrastructure.",
            "GPS coordinates {coord} extracted from image metadata.",
            "Threat intelligence report lists {coord} as command and control location.",
            "Social media post revealed coordinates {coord} in EXIF data.",
        ]
        
        long_contexts = [
            """The OSINT investigation team conducted a comprehensive analysis of a suspected threat actor's online presence, discovering multiple social media accounts and forum posts that revealed their operational security practices. During the investigation, the analysts extracted GPS coordinates {coord} from images posted by the threat actor on various social media platforms. The geolocation analysis revealed that these coordinates corresponded to a location in a foreign country, which helped law enforcement identify the physical location of the threat actor. The security team shared this intelligence with law enforcement agencies, leading to the arrest of several individuals involved in the attack campaign. The investigation highlighted the importance of OSINT techniques in cybersecurity investigations and the need for threat actors to maintain proper operational security when using social media platforms.""",
        ]
        
        short_count = count // 2
        long_count = count - short_count
        
        for _ in range(short_count):
            coord = random.choice(coords)
            context = random.choice(short_contexts).format(coord=coord)
            coord_pos = context.find(coord)
            if coord_pos != -1:
                examples.append((context, [[coord_pos, coord_pos + len(coord), coord_type]]))
        
        for _ in range(long_count):
            coord = random.choice(coords)
            context = random.choice(long_contexts).format(coord=coord)
            coord_pos = context.find(coord)
            if coord_pos != -1:
                examples.append((context, [[coord_pos, coord_pos + len(coord), coord_type]]))
        
        return examples
    
    entity_generators = {
        'EMOJI': generate_hybrid_emoji_examples,
        'PHONE_NUMBER': generate_hybrid_phone_examples,
        'MALWARE_TYPE': generate_hybrid_malware_examples,
        'DOMAIN': generate_hybrid_domain_examples,
        'TIME': generate_hybrid_time_examples,
        'LATITUDE': lambda c: generate_hybrid_coordinate_examples(c, "LATITUDE"),
        'LONGITUDE': lambda c: generate_hybrid_coordinate_examples(c, "LONGITUDE"),
    }
    
    for entity_type, count in TOP_MISSED_ENTITIES.items():
        print(f"  Processing {entity_type} ({count} examples)...")
        
        # Generate examples
        if entity_type in entity_generators:
            examples = entity_generators[entity_type](count)
        else:
            # For now, skip types without generators
            print(f"    ⚠️  Generator not implemented for {entity_type}, skipping...")
            continue
        
        # Add to relevant files
        pillars = ENTITY_PILLAR_MAPPING.get(entity_type, ['threat_intelligence'])
        for pillar_name in pillars:
            pillar_dir = base_dir / pillar_name
            if pillar_dir.exists():
                entity_file = pillar_dir / f"{pillar_name.split('/')[-1]}_entities.jsonl"
                if entity_file.exists():
                    added = add_examples_to_file(entity_file, examples, entity_type, is_negative=False)
                    total_added += added
                else:
                    print(f"    ⚠️  File not found: {entity_file}")
    
    print()
    
    # 2. Add negative examples for false positives
    print("🚫 Adding NEGATIVE examples to reduce FALSE POSITIVES...")
    print()
    
    negative_generators = {
        'THREAT_ACTOR': generate_negative_threat_actor_examples,
        'PROTOCOL_TYPE': generate_negative_protocol_examples,
    }
    
    for entity_type, count in FALSE_POSITIVE_ENTITIES.items():
        print(f"  Processing negative examples for {entity_type} ({count} examples)...")
        
        if entity_type in negative_generators:
            examples = negative_generators[entity_type](count)
        else:
            print(f"    ⚠️  Generator not implemented for {entity_type}, skipping...")
            continue
        
        # Add to relevant files
        pillars = ENTITY_PILLAR_MAPPING.get(entity_type, ['threat_intelligence'])
        for pillar_name in pillars:
            pillar_dir = base_dir / pillar_name
            if pillar_dir.exists():
                entity_file = pillar_dir / f"{pillar_name.split('/')[-1]}_entities.jsonl"
                if entity_file.exists():
                    added = add_examples_to_file(entity_file, examples, entity_type, is_negative=True)
                    total_added += added
                else:
                    print(f"    ⚠️  File not found: {entity_file}")
    
    print()
    print("=" * 80)
    print(f"✅ COMPLETE: Added {total_added} total examples")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Review the added examples")
    print("2. Re-prepare training data: python3 prepare_spacy_training.py")
    print("3. Re-train models: python3 train_spacy_models.py")
    print("4. Re-run test suite: python3 comprehensive_test_suite.py")

if __name__ == "__main__":
    main()

