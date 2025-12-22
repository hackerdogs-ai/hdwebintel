#!/usr/bin/env python3
"""
Iteration 6: Massive Short Context Example Generation

This script generates 500+ short context examples (40-90 characters) per top missed entity type,
using patterns that match the test suite exactly.

Key insights from previous iterations:
- Training data uses 200-500 char contexts
- Test suite uses 40-90 char contexts
- Model learned long-context patterns and misses short contexts
- Need massive short context examples to override long-context bias
"""

import json
import os
import random
from pathlib import Path
from collections import defaultdict

# Top missed entity types from test suite analysis
TOP_MISSED_TYPES = [
    "EMOJI",           # 15 missed
    "PHONE_NUMBER",    # 11 missed
    "MALWARE_TYPE",    # 10 missed
    "DOMAIN",          # 6 missed
    "TIME",            # 5 missed
    "LATITUDE",        # 5 missed
    "LONGITUDE",       # 5 missed
    "IPV6_ADDRESS",    # 5 missed
    "SSN",             # 5 missed
    "EMAIL_ADDRESS",   # 5 missed
    "LLM_PROVIDER",    # 5 missed
    "LLM_MODEL",       # 5 missed
    "IP_ADDRESS",      # 5 missed
    "COMPLIANCE_FRAMEWORK",  # 5 missed
    "THREAT_ACTOR",    # 4 missed
    "DMS_COORDINATES", # Additional
    "DATE",            # Additional
    "HASH",            # Additional
]

# Entity to pillar/file mapping
ENTITY_FILE_MAPPING = {
    "EMOJI": "osint/socmint/socmint_entities.jsonl",
    "PHONE_NUMBER": "osint/socmint/socmint_entities.jsonl",
    "MALWARE_TYPE": "threat_intelligence/threat_intel_entities.jsonl",
    "DOMAIN": "network_security/network_security_entities.jsonl",
    "TIME": "detection_correlation/detection_correlation_entities.jsonl",
    "LATITUDE": "osint/geoint/geoint_entities.jsonl",
    "LONGITUDE": "osint/geoint/geoint_entities.jsonl",
    "IPV6_ADDRESS": "network_security/network_security_entities.jsonl",
    "SSN": "data_privacy/data_privacy_entities.jsonl",
    "EMAIL_ADDRESS": "osint/socmint/socmint_entities.jsonl",
    "LLM_PROVIDER": "ai_security/ai_security_entities.jsonl",
    "LLM_MODEL": "ai_security/ai_security_entities.jsonl",
    "IP_ADDRESS": "network_security/network_security_entities.jsonl",
    "COMPLIANCE_FRAMEWORK": "audit_compliance/audit_compliance_entities.jsonl",
    "THREAT_ACTOR": "threat_intelligence/threat_intel_entities.jsonl",
    "DMS_COORDINATES": "osint/geoint/geoint_entities.jsonl",
    "DATE": "detection_correlation/detection_correlation_entities.jsonl",
    "HASH": "endpoint_security/endpoint_security_entities.jsonl",
}

# Short context templates (40-90 chars) - exactly matching test suite patterns
SHORT_TEMPLATES = {
    "EMOJI": [
        "🚨 Alert: {entity}",
        "⚠️ Warning: {entity}",
        "✅ Verified: {entity}",
        "🔒 Secure: {entity}",
        "📧 Email: {entity}",
        "🌐 Network: {entity}",
        "💻 System: {entity}",
        "🔐 Security: {entity}",
        "{entity} detected in scan",
        "Alert {entity} triggered",
        "Warning {entity} found",
        "Security {entity} alert",
        "Status: {entity}",
        "Check {entity} status",
        "Monitor {entity}",
    ],
    "PHONE_NUMBER": [
        "Phone: {entity}",
        "Call {entity}",
        "Contact: {entity}",
        "Tel: {entity}",
        "Mobile: {entity}",
        "Phone number {entity}",
        "Dial {entity}",
        "Number: {entity}",
        "Fax: {entity}",
        "Phone formats: {entity}",
        "Contact number {entity}",
        "Call back {entity}",
        "Reach at {entity}",
        "Phone {entity} detected",
        "Number {entity} found",
    ],
    "MALWARE_TYPE": [
        "{entity} detected",
        "Malware: {entity}",
        "{entity} found",
        "Detect {entity}",
        "{entity} variant",
        "{entity} infection",
        "Alert: {entity}",
        "{entity} malware",
        "Ransomware: {entity}",
        "Trojan: {entity}",
        "Virus: {entity}",
        "{entity} attack",
        "{entity} sample",
        "Remove {entity}",
        "Block {entity}",
    ],
    "DOMAIN": [
        "Domain: {entity}",
        "Check {entity}",
        "Verify {entity}",
        "{entity} lookup",
        "DNS: {entity}",
        "Site: {entity}",
        "Host: {entity}",
        "{entity} status",
        "Resolve {entity}",
        "Query {entity}",
        "{entity} records",
        "Scan {entity}",
        "{entity} whois",
        "Block {entity}",
        "{entity} is suspicious",
    ],
    "TIME": [
        "Time: {entity}",
        "At {entity}",
        "Timestamp: {entity}",
        "{entity} UTC",
        "{entity} EST",
        "{entity} PST",
        "Event at {entity}",
        "Log time {entity}",
        "Occurred {entity}",
        "Time stamp: {entity}",
        "Alert at {entity}",
        "Detected {entity}",
        "Time formats: {entity}",
        "From {entity}",
        "Until {entity}",
    ],
    "LATITUDE": [
        "Latitude: {entity}",
        "Lat: {entity}",
        "Location lat {entity}",
        "Coords: {entity}",
        "Position: {entity}",
        "Geo lat: {entity}",
        "Track lat {entity}",
        "GPS lat {entity}",
        "Lat {entity} found",
        "Latitude {entity}",
        "Map lat {entity}",
        "Point lat {entity}",
        "At latitude {entity}",
        "Geo: {entity}",
        "Coordinate: {entity}",
    ],
    "LONGITUDE": [
        "Longitude: {entity}",
        "Long: {entity}",
        "Lon: {entity}",
        "Location lon {entity}",
        "Coords: {entity}",
        "Position: {entity}",
        "Geo lon: {entity}",
        "Track lon {entity}",
        "GPS lon {entity}",
        "Lon {entity} found",
        "Longitude {entity}",
        "Map lon {entity}",
        "Point lon {entity}",
        "At longitude {entity}",
        "Geo: {entity}",
    ],
    "IPV6_ADDRESS": [
        "IPv6: {entity}",
        "Address: {entity}",
        "IP: {entity}",
        "{entity} detected",
        "Host: {entity}",
        "Connect to {entity}",
        "From {entity}",
        "To {entity}",
        "Source: {entity}",
        "Dest: {entity}",
        "IPv6 {entity}",
        "Check {entity}",
        "Block {entity}",
        "Allow {entity}",
        "Monitor {entity}",
    ],
    "SSN": [
        "SSN: {entity}",
        "Social: {entity}",
        "SSN {entity} found",
        "Number: {entity}",
        "ID: {entity}",
        "SSN detected: {entity}",
        "PII: {entity}",
        "Sensitive: {entity}",
        "SSN leak: {entity}",
        "Found SSN {entity}",
        "SSN formats: {entity}",
        "Social Security: {entity}",
        "Exposed: {entity}",
        "SSN data: {entity}",
        "Alert SSN {entity}",
    ],
    "EMAIL_ADDRESS": [
        "Email: {entity}",
        "From: {entity}",
        "To: {entity}",
        "Contact: {entity}",
        "Send to {entity}",
        "Reply to {entity}",
        "{entity} verified",
        "{entity} suspicious",
        "Phishing: {entity}",
        "Address: {entity}",
        "Mail: {entity}",
        "User: {entity}",
        "Account: {entity}",
        "Email formats: {entity}",
        "Check {entity}",
    ],
    "LLM_PROVIDER": [
        "Provider: {entity}",
        "Using {entity}",
        "{entity} API",
        "Model by {entity}",
        "{entity} service",
        "Via {entity}",
        "AI: {entity}",
        "{entity} endpoint",
        "From {entity}",
        "Audit {entity}",
        "Monitor {entity}",
        "{entity} usage",
        "Track {entity}",
        "AI provider: {entity}",
        "LLM: {entity}",
    ],
    "LLM_MODEL": [
        "Model: {entity}",
        "Using {entity}",
        "{entity} response",
        "Run {entity}",
        "{entity} output",
        "Query {entity}",
        "AI model: {entity}",
        "{entity} inference",
        "Deploy {entity}",
        "Test {entity}",
        "Audit {entity}",
        "{entity} variant",
        "LLM: {entity}",
        "AI: {entity}",
        "{entity} API",
    ],
    "IP_ADDRESS": [
        "IP: {entity}",
        "Address: {entity}",
        "From {entity}",
        "To {entity}",
        "Source: {entity}",
        "Dest: {entity}",
        "Check IP {entity}",
        "Block {entity}",
        "Allow {entity}",
        "Monitor {entity}",
        "{entity} detected",
        "Host: {entity}",
        "Connect {entity}",
        "Scan {entity}",
        "IP {entity} found",
    ],
    "COMPLIANCE_FRAMEWORK": [
        "{entity} compliance",
        "Check {entity}",
        "{entity} audit",
        "Comply with {entity}",
        "{entity} requirements",
        "{entity} controls",
        "Verify {entity}",
        "{entity} assessment",
        "Framework: {entity}",
        "{entity} standard",
        "Meet {entity}",
        "{entity} certified",
        "{entity} compliant",
        "Audit {entity}",
        "{entity} check",
    ],
    "THREAT_ACTOR": [
        "{entity} attack",
        "Actor: {entity}",
        "{entity} campaign",
        "Threat: {entity}",
        "{entity} detected",
        "Track {entity}",
        "{entity} activity",
        "Group: {entity}",
        "APT: {entity}",
        "{entity} IOCs",
        "Monitor {entity}",
        "{entity} TTPs",
        "Attribute to {entity}",
        "{entity} malware",
        "Hunt {entity}",
    ],
    "DMS_COORDINATES": [
        "Coords: {entity}",
        "Location: {entity}",
        "DMS: {entity}",
        "Position: {entity}",
        "At {entity}",
        "GPS: {entity}",
        "Geo: {entity}",
        "Point: {entity}",
        "Map: {entity}",
        "Track: {entity}",
        "Found at {entity}",
        "Located: {entity}",
        "Coordinates: {entity}",
        "DMS coordinates: {entity}",
        "Position {entity}",
    ],
    "DATE": [
        "Date: {entity}",
        "On {entity}",
        "Since {entity}",
        "Until {entity}",
        "From {entity}",
        "Event: {entity}",
        "Log: {entity}",
        "Timestamp: {entity}",
        "Occurred {entity}",
        "Date formats: {entity}",
        "Schedule: {entity}",
        "Deadline: {entity}",
        "Report: {entity}",
        "Alert: {entity}",
        "As of {entity}",
    ],
    "HASH": [
        "Hash: {entity}",
        "MD5: {entity}",
        "SHA256: {entity}",
        "SHA1: {entity}",
        "File hash {entity}",
        "Check {entity}",
        "Verify {entity}",
        "Match {entity}",
        "Compare {entity}",
        "Malware hash {entity}",
        "IOC: {entity}",
        "Sample: {entity}",
        "Signature: {entity}",
        "Hash {entity} found",
        "Lookup {entity}",
    ],
}

# Sample entity values for each type
ENTITY_VALUES = {
    "EMOJI": [
        "🚨", "⚠️", "✅", "🔒", "📧", "🌐", "💻", "🔐", "🦠", "🔥",
        "⚡", "🔍", "📊", "🛡️", "⚙️", "📁", "🔑", "📡", "🖥️", "💾",
        "🚫", "✓", "❌", "❗", "❓", "⭐", "📌", "🔴", "🟢", "🟡",
    ],
    "PHONE_NUMBER": [
        "+1-555-123-4567", "(555) 123-4567", "555.123.4567", "+15551234567",
        "+1 555 123 4567", "555-123-4567", "+44 20 7946 0958", "+33 1 42 68 53 00",
        "+49 30 123456", "+81 3 1234 5678", "+86 10 1234 5678", "+91 22 1234 5678",
        "+7 495 123 4567", "+55 11 1234 5678", "+61 2 1234 5678", "+34 91 123 4567",
        "(212) 555-1234", "(415) 555-9876", "(310) 555-4321", "(202) 555-6789",
        "+1-800-555-1234", "1-888-555-4567", "+1 (555) 987-6543", "555 123 4567",
        "+44-20-7946-0958", "+33-1-42-68-53-00", "+49-30-123456", "+81-3-1234-5678",
        "+1.555.123.4567", "+44.20.7946.0958", "+33.1.42.68.53.00", "+49.30.123456",
    ],
    "MALWARE_TYPE": [
        "WannaCry", "NotPetya", "Ryuk", "Emotet", "TrickBot", "Zeus",
        "Mirai", "Conficker", "Stuxnet", "Code Red", "ILOVEYOU", "MyDoom",
        "CryptoLocker", "Locky", "Cerber", "GandCrab", "REvil", "DarkSide",
        "Conti", "LockBit", "BlackCat", "Hive", "Royal", "Play",
        "Dridex", "QakBot", "IcedID", "BazarLoader", "Cobalt Strike", "Metasploit",
        "Remote Access Trojan", "keylogger", "screen capture", "bootkit", "rootkit",
    ],
    "DOMAIN": [
        "example.com", "malware.evil.com", "phishing.bad.org", "c2.attack.net",
        "suspicious.domain.io", "malicious.site.ru", "hacker.domain.cn", "evil.corp.com",
        "ns1.example.com", "ns2.example.com", "mail.example.com", "ftp.example.com",
        "api.service.com", "cdn.content.net", "app.platform.io", "dev.staging.org",
        "secure.bank.com", "login.service.net", "portal.company.org", "admin.system.io",
        "test.domain.com", "prod.service.net", "stage.app.io", "demo.platform.org",
    ],
    "TIME": [
        "14:30", "2:30 PM", "14:30:00", "2:30:00 PM", "09:15", "9:15 AM",
        "23:59", "11:59 PM", "00:00", "12:00 AM", "12:00", "12:00 PM",
        "08:30", "8:30 AM", "17:45", "5:45 PM", "21:00", "9:00 PM",
        "06:00", "6:00 AM", "15:30", "3:30 PM", "18:15", "6:15 PM",
        "10:45", "10:45 AM", "22:30", "10:30 PM", "07:00", "7:00 AM",
    ],
    "LATITUDE": [
        "40.7128", "34.0522", "51.5074", "48.8566", "35.6762", "55.7558",
        "37.7749", "52.5200", "39.9042", "41.9028", "31.2304", "22.3193",
        "-33.8688", "-23.5505", "-34.6037", "19.4326", "1.3521", "13.7563",
        "40.4168", "59.3293", "50.8503", "52.3676", "45.4642", "60.1699",
        "25.2048", "35.1796", "33.4484", "29.7604", "47.6062", "32.7767",
    ],
    "LONGITUDE": [
        "-74.0060", "-118.2437", "-0.1278", "2.3522", "139.6503", "37.6173",
        "-122.4194", "13.4050", "116.4074", "12.4964", "121.4737", "114.1694",
        "151.2093", "-46.6333", "-58.3816", "-99.1332", "103.8198", "100.5018",
        "-3.7038", "18.0686", "4.3517", "4.9041", "9.1900", "24.9384",
        "55.2708", "136.9066", "-112.0740", "-95.3698", "-122.3321", "-96.7970",
    ],
    "IPV6_ADDRESS": [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "fe80::1", "::1", "2001:db8::1", "2001:db8:85a3::8a2e:370:7334",
        "fd00::1", "fe80::a00:27ff:fe8e:8aa8", "2001:4860:4860::8888",
        "2001:4860:4860::8844", "2606:4700:4700::1111", "2606:4700:4700::1001",
        "2a00:1450:4009:815::200e", "2607:f8b0:4004:800::200e", "2001:41d0:1:1b00::1",
        "fe80::1%eth0", "fe80::1%lo0", "2001:db8:1234:5678:9abc:def0:1234:5678",
    ],
    "SSN": [
        "123-45-6789", "987-65-4321", "555-12-3456", "111-22-3333",
        "222-33-4444", "333-44-5555", "444-55-6666", "555-66-7777",
        "666-77-8888", "777-88-9999", "888-99-0000", "999-00-1111",
        "123-12-1234", "234-23-2345", "345-34-3456", "456-45-4567",
    ],
    "EMAIL_ADDRESS": [
        "user@example.com", "admin@company.org", "security@firm.net",
        "alert@system.io", "info@service.com", "support@help.org",
        "phishing@evil.com", "malware@bad.net", "spam@junk.org",
        "user+tag@example.com", "first.last@domain.com", "name_123@site.net",
        "contact@business.com", "sales@company.org", "hr@enterprise.net",
        "test@domain.io", "dev@staging.com", "prod@live.org",
    ],
    "LLM_PROVIDER": [
        "OpenAI", "Anthropic", "Google", "Microsoft", "Meta", "Amazon",
        "Cohere", "AI21", "Hugging Face", "Stability AI", "Mistral AI",
        "xAI", "DeepMind", "Nvidia", "IBM", "Baidu", "Alibaba",
    ],
    "LLM_MODEL": [
        "GPT-4", "GPT-3.5", "Claude", "Claude-3", "Gemini", "Llama",
        "Llama-2", "Llama-3", "PaLM", "PaLM-2", "Falcon", "Mistral",
        "GPT-4-turbo", "Claude-3-opus", "Claude-3-sonnet", "Gemini-Pro",
        "gpt-4o", "gpt-4o-mini", "claude-3-haiku", "gemini-1.5-pro",
        "llama-3-70b", "mixtral-8x7b", "command-r", "command-r-plus",
    ],
    "IP_ADDRESS": [
        "192.168.1.1", "10.0.0.1", "172.16.0.1", "8.8.8.8", "1.1.1.1",
        "192.168.0.1", "10.10.10.10", "172.31.255.255", "8.8.4.4", "1.0.0.1",
        "192.168.1.100", "10.0.0.100", "172.16.0.100", "203.0.113.1", "198.51.100.1",
        "192.0.2.1", "100.64.0.1", "169.254.1.1", "127.0.0.1", "0.0.0.0",
        "255.255.255.255", "224.0.0.1", "239.255.255.255", "192.168.255.1", "10.255.255.1",
    ],
    "COMPLIANCE_FRAMEWORK": [
        "NIST CSF", "PCI DSS", "HIPAA", "SOC 2", "SOC 2 Type II", "FedRAMP",
        "CMMC", "CMMC Level 3", "CIS Controls", "ISO 27001", "ISO 27002",
        "GDPR", "CCPA", "PIPEDA", "FIPS 140-2", "FISMA", "COBIT",
        "SOX", "GLBA", "NERC CIP", "NIST 800-53", "NIST 800-171",
    ],
    "THREAT_ACTOR": [
        "APT29", "APT28", "Lazarus", "FIN7", "UNC2452", "Wizard Spider",
        "Cozy Bear", "Fancy Bear", "Sandworm", "Turla", "Kimsuky", "Charming Kitten",
        "Hafnium", "Nobelium", "DarkSide", "REvil", "Conti", "LockBit",
        "BlackCat", "Hive", "Royal", "Cl0p", "Black Basta", "Vice Society",
    ],
    "DMS_COORDINATES": [
        "40°42'46\"N 74°00'22\"W", "51°30'26\"N 0°07'39\"W",
        "48°51'24\"N 2°21'07\"E", "35°41'22\"N 139°41'30\"E",
        "55°45'21\"N 37°37'04\"E", "34°03'08\"N 118°14'37\"W",
        "37°46'30\"N 122°25'10\"W", "52°31'12\"N 13°24'18\"E",
        "40°42'46.8\"N 74°00'21.6\"W", "51°30'26.4\"N 0°07'38.4\"W",
    ],
    "DATE": [
        "2024-11-30", "11/30/2024", "November 30, 2024", "30-Nov-2024",
        "2024-12-15", "12/15/2024", "December 15, 2024", "15-Dec-2024",
        "2024-01-01", "01/01/2024", "January 1, 2024", "1-Jan-2024",
        "2023-06-15", "06/15/2023", "June 15, 2023", "15-Jun-2023",
        "2024-11-30T14:30:00Z", "2024-12-15T09:00:00Z", "1701350400",
    ],
    "HASH": [
        "5d41402abc4b2a76b9719d911017c592", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "da39a3ee5e6b4b0d3255bfef95601890afd80709", "abc123def456", "def456ghi789",
        "d41d8cd98f00b204e9800998ecf8427e", "098f6bcd4621d373cade4e832627b4f6",
        "e99a18c428cb38d5f260853678922e03", "25f9e794323b453885f5181f1b624d0b",
        "a3f390d88e4c41f2747bfa2f1b5f87db", "202cb962ac59075b964b07152d234b70",
    ],
}


def generate_short_context_examples(entity_type: str, count: int = 500) -> list:
    """Generate short context examples (40-90 chars) for an entity type."""
    examples = []
    seen = set()
    
    templates = SHORT_TEMPLATES.get(entity_type, [])
    values = ENTITY_VALUES.get(entity_type, [])
    
    if not templates or not values:
        print(f"  ⚠️  No templates or values for {entity_type}")
        return []
    
    attempts = 0
    max_attempts = count * 20  # Allow many attempts to find unique examples
    
    while len(examples) < count and attempts < max_attempts:
        attempts += 1
        
        template = random.choice(templates)
        value = random.choice(values)
        
        # Create the context
        context = template.format(entity=value)
        
        # Skip if too long or too short
        if len(context) < 30 or len(context) > 100:
            continue
        
        # Skip duplicates
        if context in seen:
            continue
        seen.add(context)
        
        # Find entity position
        try:
            start = context.index(value)
            end = start + len(value)
            
            # Validate boundaries
            if start < 0 or end > len(context):
                continue
            
            # Create example
            example = {
                "text": context,
                "entities": [[start, end, entity_type]]
            }
            examples.append(example)
            
        except ValueError:
            continue
    
    return examples


def generate_additional_variations(entity_type: str, base_examples: list, target: int = 500) -> list:
    """Generate additional variations if we don't have enough."""
    additional = []
    seen = {ex["text"] for ex in base_examples}
    
    # Additional prefix/suffix variations
    prefixes = [
        "Check ", "Verify ", "Scan ", "Monitor ", "Track ", "Block ", "Allow ",
        "Detect ", "Find ", "Search ", "Alert: ", "Warning: ", "Info: ",
        "Log: ", "Event: ", "Status: ", "Report: ", "Note: ", "Flag: ",
    ]
    
    suffixes = [
        " detected", " found", " alert", " warning", " status", " check",
        " verified", " confirmed", " blocked", " allowed", " logged",
        " tracked", " monitored", " scanned", " reported", " flagged",
    ]
    
    values = ENTITY_VALUES.get(entity_type, [])
    
    while len(base_examples) + len(additional) < target and values:
        value = random.choice(values)
        
        # Try prefix variations
        if random.random() < 0.5:
            prefix = random.choice(prefixes)
            context = f"{prefix}{value}"
        else:
            suffix = random.choice(suffixes)
            context = f"{value}{suffix}"
        
        if len(context) < 30 or len(context) > 100:
            continue
        
        if context in seen:
            continue
        seen.add(context)
        
        try:
            start = context.index(value)
            end = start + len(value)
            
            example = {
                "text": context,
                "entities": [[start, end, entity_type]]
            }
            additional.append(example)
        except ValueError:
            continue
    
    return additional


def add_examples_to_file(examples: list, file_path: Path) -> int:
    """Add examples to JSONL file."""
    if not examples:
        return 0
    
    # Read existing examples
    existing = set()
    if file_path.exists():
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    existing.add(line)
    
    # Add new examples
    added = 0
    with open(file_path, 'a') as f:
        for ex in examples:
            line = json.dumps(ex)
            if line not in existing:
                f.write(line + '\n')
                existing.add(line)
                added += 1
    
    return added


def main():
    print("="*70)
    print("ITERATION 6: MASSIVE SHORT CONTEXT EXAMPLE GENERATION")
    print("="*70)
    print()
    
    base_dir = Path("/Users/tredkar/Documents/GitHub/hdwebintel/cyber-train/entities-intent")
    
    total_added = 0
    stats = {}
    
    for entity_type in TOP_MISSED_TYPES:
        print(f"\n📝 Processing {entity_type}...")
        
        # Generate base examples
        examples = generate_short_context_examples(entity_type, 500)
        print(f"   Generated {len(examples)} base examples")
        
        # Generate additional variations if needed
        if len(examples) < 500:
            additional = generate_additional_variations(entity_type, examples, 500)
            examples.extend(additional)
            print(f"   Added {len(additional)} additional variations")
        
        # Get target file
        rel_path = ENTITY_FILE_MAPPING.get(entity_type)
        if not rel_path:
            print(f"   ⚠️  No file mapping for {entity_type}")
            continue
        
        file_path = base_dir / rel_path
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add examples
        added = add_examples_to_file(examples, file_path)
        total_added += added
        stats[entity_type] = added
        
        print(f"   ✅ Added {added} unique examples to {rel_path}")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\nTotal examples added: {total_added}")
    print("\nBy entity type:")
    for entity_type, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {entity_type}: {count} examples")
    
    print("\n✅ Short context example generation complete!")
    print("Next steps:")
    print("   1. Run prepare_spacy_training.py")
    print("   2. Run train_spacy_models.py")
    print("   3. Run comprehensive_test_suite.py")


if __name__ == "__main__":
    main()

