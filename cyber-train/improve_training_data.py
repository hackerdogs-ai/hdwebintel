#!/usr/bin/env python3
"""
Comprehensive Training Data Improvement Script

This script:
1. Fixes false positives (especially TOOL entity type)
2. Fixes boundary issues (partial entities)
3. Fixes label confusion (DOMAIN vs HOST_TYPE, etc.)
4. Adds 700+ training examples for missed entity types
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Set
import random

# Common words that should NOT be TOOL
COMMON_WORDS_NOT_TOOL = {
    "find", "extract", "url", "json", "xml", "python", "javascript",
    "instagram", "facebook", "twitter", "linkedin", "telegram", "discord",
    "slack", "whatsapp", "github", "git", "code", "import", "os", "found",
    "detected", "check", "verify", "analyze", "investigate", "scan",
    "monitor", "track", "report", "generate", "create", "update", "delete"
}

# Label confusion mappings (wrong_label -> correct_label based on context)
LABEL_FIXES = {
    # DOMAIN vs HOST_TYPE: If it's a hostname with internal/private domain, it's HOST_TYPE
    # DOMAIN vs EMAIL_ADDRESS: If it's just a domain (no @), it's DOMAIN
    # REPOSITORY vs FILE_PATH: If it starts with / or ~ or C:\, it's FILE_PATH
}

# Entity type distribution across files
ENTITY_FILE_MAPPING = {
    "MALWARE_TYPE": ["threat_intelligence", "incident_response", "endpoint_security", "detection_correlation"],
    "LLM_MODEL": ["ai_security", "threat_intelligence"],
    "DATE": ["audit_compliance", "incident_response", "threat_intelligence"],
    "HASH": ["incident_response", "endpoint_security", "threat_intelligence"],
    "PHONE_NUMBER": ["data_privacy_sovereignty", "osint"],
    "COMPLIANCE_FRAMEWORK": ["audit_compliance", "governance_risk_strategy"],
    "URL": ["network_security", "osint", "threat_intelligence"],
    "LLM_PROVIDER": ["ai_security", "threat_intelligence"],
    "THREAT_ACTOR": ["threat_intelligence", "incident_response"],
    "TIME": ["audit_compliance", "incident_response"],
    "IP_ADDRESS": ["network_security", "incident_response", "threat_intelligence"],
    "FILE_PATH": ["endpoint_security", "incident_response"],
    "DOMAIN": ["network_security", "threat_intelligence", "osint"],
    "EMOJI": ["osint"],
    "IPV6_ADDRESS": ["network_security", "threat_intelligence"],
    "SSN": ["data_privacy_sovereignty"],
    "CREDIT_CARD_NUMBER": ["data_privacy_sovereignty"],
    "LATITUDE": ["osint"],
    "LONGITUDE": ["osint"],
    "DATACENTER": ["cloud_security_cnapp", "network_security"],
    "EMOJI": ["osint"],
    "IPV6_ADDRESS": ["network_security", "threat_intelligence"],
    "SSN": ["data_privacy_sovereignty"],
    "CREDIT_CARD_NUMBER": ["data_privacy_sovereignty"],
    "URL": ["network_security", "osint", "threat_intelligence"],
}

def fix_entity_boundaries(text: str, start: int, end: int, label: str) -> Tuple[int, int]:
    """Fix entity boundaries to match word boundaries."""
    # Extend to word boundaries
    while start > 0 and text[start-1] not in ' \n\t':
        start -= 1
    while end < len(text) and text[end] not in ' \n\t':
        end += 1
    
    # Trim whitespace
    while start < len(text) and text[start] in ' \n\t':
        start += 1
    while end > start and text[end-1] in ' \n\t':
        end -= 1
    
    return start, end

def is_valid_entity(text: str, start: int, end: int, label: str) -> bool:
    """Check if entity is valid."""
    if start < 0 or end > len(text) or start >= end:
        return False
    
    entity_text = text[start:end].strip()
    if not entity_text:
        return False
    
    # Check for common words as TOOL (more aggressive)
    if label == "TOOL":
        entity_lower = entity_text.lower()
        if entity_lower in COMMON_WORDS_NOT_TOOL:
            return False
        # Also check if it's a common verb or noun
        if len(entity_text) < 4:  # Very short words are likely not tools
            return False
        if entity_text.lower() in ["url", "json", "xml", "api", "http", "https", "dns", "ssl", "tls"]:
            return False
    
    # Check for partial phone numbers
    if label == "PHONE_NUMBER":
        if not re.match(r'^\+?\d', entity_text):  # Should start with + or digit
            return False
        digits_only = re.sub(r'\D', '', entity_text)
        # International numbers can be shorter (e.g., German +49 30 2273 0)
        # But should have at least 7 digits
        if len(digits_only) < 7:
            return False
        # Check if it's just a partial (starts with -)
        if entity_text.startswith('-'):
            return False
    
    # Check for partial file paths
    if label == "FILE_PATH":
        if not (entity_text.startswith('/') or entity_text.startswith('~') or 
                entity_text.startswith('C:\\') or entity_text.startswith('\\')):
            # If it's not a full path, might be REPOSITORY
            return False
    
    # Check for standalone numbers as various types
    if label in ["METRIC_TYPE", "PROTOCOL_TYPE", "PORT_TYPE"]:
        if entity_text.isdigit() and len(entity_text) <= 3:
            # Standalone small numbers are likely not entities
            return False
    
    return True

def fix_label_confusion(text: str, start: int, end: int, label: str) -> str:
    """Fix label confusion based on context."""
    entity_text = text[start:end]
    context_before = text[max(0, start-20):start].lower()
    context_after = text[end:min(len(text), end+20)].lower()
    
    # DOMAIN vs HOST_TYPE
    if label == "DOMAIN":
        if "internal" in context_before or "internal" in context_after or \
           ".internal" in entity_text or "server" in context_before or \
           "host" in context_before:
            return "HOST_TYPE"
    
    # DOMAIN vs EMAIL_ADDRESS
    if label == "EMAIL_ADDRESS":
        if "@" not in entity_text:
            return "DOMAIN"
    
    # REPOSITORY vs FILE_PATH
    if label == "REPOSITORY":
        if entity_text.startswith('/') or entity_text.startswith('~') or \
           entity_text.startswith('C:\\') or entity_text.startswith('\\'):
            return "FILE_PATH"
        if "/.ssh/" in entity_text or "/.config/" in entity_text:
            return "FILE_PATH"
    
    return label

def generate_malware_examples() -> List[Dict]:
    """Generate training examples for malware types."""
    malware_names = [
        "WannaCry", "NotPetya", "Ryuk", "Zeus", "Emotet", "TrickBot",
        "Conficker", "Stuxnet", "Code Red", "Slammer", "Blaster",
        "Mydoom", "ILOVEYOU", "Melissa", "CryptoLocker", "Locky",
        "Petya", "Bad Rabbit", "SamSam", "GandCrab"
    ]
    
    examples = []
    contexts = [
        "Detected {malware} malware on endpoint",
        "Threat actor used {malware} ransomware in attack",
        "Investigate {malware} infection on system",
        "Block {malware} variant from network",
        "Analyze {malware} payload and behavior",
        "Report {malware} detection to security team",
        "Quarantine {malware} sample for analysis",
        "Track {malware} campaign indicators",
        "Remediate {malware} infection on host",
        "Monitor for {malware} activity in network"
    ]
    
    for malware in malware_names:
        for context_template in contexts:
            text = context_template.format(malware=malware)
            start = text.find(malware)
            end = start + len(malware)
            examples.append({
                "text": text,
                "entities": [[start, end, "MALWARE_TYPE"]]
            })
    
    return examples

def generate_llm_model_examples() -> List[Dict]:
    """Generate training examples for LLM models."""
    models = [
        ("GPT-4", "OpenAI"), ("GPT-3.5", "OpenAI"), ("Claude-3", "Anthropic"),
        ("Claude-2", "Anthropic"), ("Llama-2", "Meta"), ("Llama-3", "Meta"),
        ("Gemini Pro", "Google"), ("Gemini Ultra", "Google"), ("PaLM-2", "Google"),
        ("Jurassic-2", "AI21"), ("Command", "Cohere"), ("GPT-4o", "OpenAI")
    ]
    
    examples = []
    contexts = [
        "Using {model} LLM model for analysis",
        "AI model {model} from {provider} detected",
        "LLM {model} generated suspicious content",
        "Monitor {model} API usage and costs",
        "Review {model} model outputs for security",
        "Audit {model} access and permissions",
        "Investigate {model} model behavior",
        "Track {model} from {provider} usage",
        "Analyze {model} model performance",
        "Secure {model} API keys and tokens"
    ]
    
    for model, provider in models:
        for context_template in contexts:
            text = context_template.format(model=model, provider=provider)
            model_start = text.find(model)
            model_end = model_start + len(model)
            provider_start = text.find(provider)
            provider_end = provider_start + len(provider) if provider_start >= 0 else -1
            
            entities = [[model_start, model_end, "LLM_MODEL"]]
            if provider_end > 0:
                entities.append([provider_start, provider_end, "LLM_PROVIDER"])
            
            examples.append({
                "text": text,
                "entities": entities
            })
    
    return examples

def generate_date_examples() -> List[Dict]:
    """Generate training examples for dates."""
    date_formats = [
        "2024-11-30", "2024-11-01", "2024-12-15", "2023-01-01",
        "11/30/2024", "11-30-2024", "30-Nov-2024", "November 30, 2024",
        "2024/11/30", "30/11/2024"
    ]
    
    examples = []
    contexts = [
        "Incident occurred on {date}",
        "Vulnerability discovered on {date}",
        "Report generated on {date}",
        "Attack detected on {date}",
        "Compliance audit on {date}",
        "Security scan on {date}",
        "Event logged on {date}",
        "Alert triggered on {date}",
        "Backup created on {date}",
        "Access granted on {date}"
    ]
    
    for date in date_formats:
        for context_template in contexts:
            text = context_template.format(date=date)
            start = text.find(date)
            end = start + len(date)
            examples.append({
                "text": text,
                "entities": [[start, end, "DATE"]]
            })
    
    return examples

def generate_hash_examples() -> List[Dict]:
    """Generate training examples for hashes."""
    hash_examples = [
        ("5d41402abc4b2a76b9719d911017c592", "MD5"),
        ("da39a3ee5e6b4b0d3255bfef95601890afd80709", "SHA1"),
        ("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "SHA256"),
        ("a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3", "SHA256"),
    ]
    
    examples = []
    contexts = [
        "File hash {hash} detected as malicious",
        "MD5 hash {hash} matches known malware",
        "SHA256 hash {hash} verified",
        "Hash {hash} found in threat database",
        "Verify file hash {hash}",
        "Check hash {hash} against IOC database",
        "Hash {hash} identified as suspicious",
        "Analyze hash {hash} for indicators",
        "Hash {hash} matches threat actor tool",
        "Investigate hash {hash} origin"
    ]
    
    for hash_val, hash_type in hash_examples:
        for context_template in contexts:
            text = context_template.format(hash=hash_val)
            start = text.find(hash_val)
            end = start + len(hash_val)
            examples.append({
                "text": text,
                "entities": [[start, end, "HASH"]]
            })
    
    return examples

def generate_phone_examples() -> List[Dict]:
    """Generate training examples for phone numbers."""
    phone_numbers = [
        "+1-555-123-4567", "+44 20 7946 0958", "+33 1 42 86 83 26",
        "+49 30 2273 0", "+81 3-1234-5678", "+86 10 1234 5678",
        "555-123-4567", "(555) 123-4567", "555.123.4567",
        "+1 (555) 123-4567", "+1 555 123 4567"
    ]
    
    examples = []
    contexts = [
        "Contact phone number {phone}",
        "Phone {phone} associated with account",
        "Investigate phone {phone}",
        "Verify phone number {phone}",
        "Phone {phone} linked to incident",
        "Check phone {phone} for fraud",
        "Phone {phone} reported as suspicious",
        "Validate phone {phone} format",
        "Phone {phone} used in attack",
        "Monitor phone {phone} activity"
    ]
    
    for phone in phone_numbers:
        for context_template in contexts:
            text = context_template.format(phone=phone)
            start = text.find(phone)
            end = start + len(phone)
            examples.append({
                "text": text,
                "entities": [[start, end, "PHONE_NUMBER"]]
            })
    
    return examples

def generate_compliance_framework_examples() -> List[Dict]:
    """Generate training examples for compliance frameworks."""
    frameworks = [
        "PCI DSS", "HIPAA", "SOC 2", "FedRAMP", "CMMC", "CIS Controls",
        "OWASP Top 10", "NIST CSF", "ISO 27001", "GDPR", "CCPA",
        "PIPEDA", "FISMA", "FIPS 140-2", "SOX", "GLBA"
    ]
    
    examples = []
    contexts = [
        "Compliance with {framework} requirements",
        "Audit for {framework} compliance",
        "Verify {framework} controls",
        "Assess {framework} compliance status",
        "Review {framework} requirements",
        "Check {framework} compliance",
        "Validate {framework} controls",
        "Report on {framework} compliance",
        "Ensure {framework} compliance",
        "Monitor {framework} requirements"
    ]
    
    for framework in frameworks:
        for context_template in contexts:
            text = context_template.format(framework=framework)
            start = text.find(framework)
            end = start + len(framework)
            examples.append({
                "text": text,
                "entities": [[start, end, "COMPLIANCE_FRAMEWORK"]]
            })
    
    return examples

def generate_threat_actor_examples() -> List[Dict]:
    """Generate training examples for threat actors."""
    actors = [
        "APT29", "APT28", "Lazarus", "FIN7", "UNC2452", "APT41",
        "Wizard Spider", "Ryuk", "Conti", "Maze", "REvil", "LockBit"
    ]
    
    examples = []
    contexts = [
        "Threat actor {actor} detected",
        "APT group {actor} activity",
        "Investigate {actor} campaign",
        "Track {actor} indicators",
        "Analyze {actor} tactics",
        "Report {actor} activity",
        "Monitor {actor} operations",
        "Attribute attack to {actor}",
        "Identify {actor} infrastructure",
        "Block {actor} communications"
    ]
    
    for actor in actors:
        for context_template in contexts:
            text = context_template.format(actor=actor)
            start = text.find(actor)
            end = start + len(actor)
            examples.append({
                "text": text,
                "entities": [[start, end, "THREAT_ACTOR"]]
            })
    
    return examples

def generate_emoji_examples() -> List[Dict]:
    """Generate training examples for emojis."""
    emojis = ["😀", "😎", "🔥", "💯", "✅", "❌", "⚠️", "🚨", "🔒", "🛡️", "⚡", "🎯"]
    
    examples = []
    contexts = [
        "User posted {emoji} in message",
        "Social media post contains {emoji}",
        "Message includes {emoji} emoji",
        "Profile has {emoji} symbol",
        "Content tagged with {emoji}",
        "Post reaction {emoji} detected",
        "Comment includes {emoji}",
        "Status update with {emoji}",
        "Tweet contains {emoji}",
        "Message sent with {emoji}"
    ]
    
    for emoji in emojis:
        for context_template in contexts:
            text = context_template.format(emoji=emoji)
            start = text.find(emoji)
            end = start + len(emoji)
            examples.append({
                "text": text,
                "entities": [[start, end, "EMOJI"]]
            })
    
    return examples

def generate_ipv6_examples() -> List[Dict]:
    """Generate training examples for IPv6 addresses."""
    ipv6_addresses = [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "2001:db8:85a3::8a2e:370:7334",
        "fe80::1",
        "::1",
        "2001:db8::1",
        "2001:0db8:0000:0000:0000:0000:0000:0001"
    ]
    
    examples = []
    contexts = [
        "IPv6 address {ipv6} detected",
        "Connection from {ipv6}",
        "Traffic to {ipv6}",
        "Source IP {ipv6}",
        "Destination {ipv6}",
        "Block {ipv6} address",
        "Investigate {ipv6}",
        "Monitor {ipv6} activity",
        "Log traffic from {ipv6}",
        "Analyze {ipv6} connections"
    ]
    
    for ipv6 in ipv6_addresses:
        for context_template in contexts:
            text = context_template.format(ipv6=ipv6)
            start = text.find(ipv6)
            end = start + len(ipv6)
            examples.append({
                "text": text,
                "entities": [[start, end, "IPV6_ADDRESS"]]
            })
    
    return examples

def generate_ssn_examples() -> List[Dict]:
    """Generate training examples for SSN."""
    ssn_formats = [
        "123-45-6789",
        "123 45 6789",
        "123456789"
    ]
    
    examples = []
    contexts = [
        "SSN {ssn} found in document",
        "Social Security Number {ssn}",
        "PII data includes SSN {ssn}",
        "Leaked SSN {ssn} detected",
        "Data breach contains {ssn}",
        "Verify SSN {ssn} format",
        "Protect SSN {ssn} data",
        "Encrypt SSN {ssn}",
        "Mask SSN {ssn}",
        "Redact SSN {ssn}"
    ]
    
    for ssn in ssn_formats:
        for context_template in contexts:
            text = context_template.format(ssn=ssn)
            start = text.find(ssn)
            end = start + len(ssn)
            examples.append({
                "text": text,
                "entities": [[start, end, "SSN"]]
            })
    
    return examples

def generate_credit_card_examples() -> List[Dict]:
    """Generate training examples for credit card numbers."""
    cc_formats = [
        "4532-1234-5678-9010",
        "4532 1234 5678 9010",
        "4532123456789010"
    ]
    
    examples = []
    contexts = [
        "Credit card {cc} detected",
        "Card number {cc} found",
        "PII includes card {cc}",
        "Payment card {cc}",
        "Leaked card {cc}",
        "Protect card {cc}",
        "Encrypt card {cc}",
        "Mask card {cc}",
        "Redact card {cc}",
        "Tokenize card {cc}"
    ]
    
    for cc in cc_formats:
        for context_template in contexts:
            text = context_template.format(cc=cc)
            start = text.find(cc)
            end = start + len(cc)
            examples.append({
                "text": text,
                "entities": [[start, end, "CREDIT_CARD_NUMBER"]]
            })
    
    return examples

def generate_url_examples() -> List[Dict]:
    """Generate training examples for URLs."""
    urls = [
        "https://example.com/path",
        "http://test.com/api",
        "https://malicious.com/evil",
        "http://192.168.1.1/admin",
        "https://api.example.com/v1/data"
    ]
    
    examples = []
    contexts = [
        "URL {url} detected",
        "Link to {url}",
        "Access {url}",
        "Block {url}",
        "Investigate {url}",
        "Monitor {url}",
        "Analyze {url}",
        "Report {url}",
        "Check {url}",
        "Verify {url}"
    ]
    
    for url in urls:
        for context_template in contexts:
            text = context_template.format(url=url)
            start = text.find(url)
            end = start + len(url)
            examples.append({
                "text": text,
                "entities": [[start, end, "URL"]]
            })
    
    return examples

def process_file(file_path: Path) -> Dict:
    """Process a single entity file to fix issues."""
    fixes = {
        "removed": 0,
        "fixed_boundaries": 0,
        "fixed_labels": 0,
        "total_entities": 0
    }
    
    new_lines = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                new_lines.append(line)
                continue
            
            try:
                data = json.loads(line)
                text = data.get("text", "")
                entities = data.get("entities", [])
                
                new_entities = []
                for orig_start, orig_end, orig_label in entities:
                    fixes["total_entities"] += 1
                    
                    # Fix boundaries
                    start, end = fix_entity_boundaries(text, orig_start, orig_end, orig_label)
                    
                    # Fix label confusion
                    label = fix_label_confusion(text, start, end, orig_label)
                    
                    # Validate entity
                    if is_valid_entity(text, start, end, label):
                        new_entities.append([start, end, label])
                        if start != orig_start or end != orig_end:
                            fixes["fixed_boundaries"] += 1
                        if label != orig_label:
                            fixes["fixed_labels"] += 1
                    else:
                        fixes["removed"] += 1
                
                new_lines.append(json.dumps({
                    "text": text,
                    "entities": new_entities
                }, ensure_ascii=False) + "\n")
                
            except json.JSONDecodeError:
                new_lines.append(line)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return fixes

def add_missed_entity_examples(base_dir: Path):
    """Add training examples for missed entity types."""
    examples_added = Counter()
    
    # Generate examples
    all_examples = {
        "MALWARE_TYPE": generate_malware_examples(),
        "LLM_MODEL": generate_llm_model_examples(),
        "DATE": generate_date_examples(),
        "HASH": generate_hash_examples(),
        "PHONE_NUMBER": generate_phone_examples(),
        "COMPLIANCE_FRAMEWORK": generate_compliance_framework_examples(),
        "THREAT_ACTOR": generate_threat_actor_examples(),
        "EMOJI": generate_emoji_examples(),
        "IPV6_ADDRESS": generate_ipv6_examples(),
        "SSN": generate_ssn_examples(),
        "CREDIT_CARD_NUMBER": generate_credit_card_examples(),
        "URL": generate_url_examples(),
    }
    
    # Distribute examples to appropriate files
    for entity_type, examples in all_examples.items():
        if entity_type in ENTITY_FILE_MAPPING:
            files = ENTITY_FILE_MAPPING[entity_type]
            examples_per_file = len(examples) // len(files)
            
            for file_name in files:
                file_path = base_dir / file_name / f"{file_name}_entities.jsonl"
                if file_path.exists():
                    file_examples = examples[:examples_per_file]
                    examples = examples[examples_per_file:]
                    
                    with open(file_path, 'a', encoding='utf-8') as f:
                        for example in file_examples:
                            f.write(json.dumps(example, ensure_ascii=False) + "\n")
                            examples_added[entity_type] += 1
    
    return examples_added

def main():
    base_dir = Path("entities-intent")
    
    print("="*80)
    print("TRAINING DATA IMPROVEMENT")
    print("="*80)
    
    # Step 1: Fix existing files
    print("\n📝 Step 1: Fixing existing training data...")
    total_fixes = defaultdict(int)
    
    for pillar_dir in base_dir.iterdir():
        if pillar_dir.is_dir() and not pillar_dir.name.startswith('.'):
            entity_file = pillar_dir / f"{pillar_dir.name}_entities.jsonl"
            if entity_file.exists():
                print(f"   Processing {pillar_dir.name}...")
                fixes = process_file(entity_file)
                for key, value in fixes.items():
                    total_fixes[key] += value
    
    print(f"\n✅ Fixed {total_fixes['removed']} false positives")
    print(f"✅ Fixed {total_fixes['fixed_boundaries']} boundaries")
    print(f"✅ Fixed {total_fixes['fixed_labels']} labels")
    
    # Step 2: Add missed entity examples
    print("\n📝 Step 2: Adding training examples for missed entities...")
    examples_added = add_missed_entity_examples(base_dir)
    
    print(f"\n✅ Added examples:")
    for entity_type, count in examples_added.items():
        print(f"   {entity_type}: {count} examples")
    
    print(f"\n✅ Total examples added: {sum(examples_added.values())}")
    
    print("\n" + "="*80)
    print("✅ TRAINING DATA IMPROVEMENT COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    main()

