#!/usr/bin/env python3
"""
Add Catalog Lists and Longer Context Examples to Training Data

This script adds:
1. Domain type catalogs with examples (excluding .img as domain)
2. Longer context examples for FILE_PATH (.img files)
3. Longer context for overlapping entities
4. Catalog/list format examples for known entity types
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
import random

# Valid domain extensions (excluding .img)
VALID_DOMAIN_EXTENSIONS = [
    '.com', '.org', '.net', '.edu', '.gov', '.mil', '.int',
    '.io', '.co', '.ai', '.dev', '.tech', '.cloud', '.app',
    '.info', '.biz', '.us', '.uk', '.ca', '.au', '.de', '.fr',
    '.jp', '.cn', '.in', '.br', '.mx', '.nl', '.se', '.no',
    '.dk', '.fi', '.pl', '.it', '.es', '.pt', '.gr', '.ie',
    '.ch', '.at', '.be', '.cz', '.hu', '.ro', '.bg', '.hr',
    '.si', '.sk', '.lt', '.lv', '.ee', '.is', '.lu', '.mt',
    '.cy', '.li', '.mc', '.ad', '.sm', '.va', '.me', '.rs',
    '.ba', '.mk', '.al', '.md', '.ua', '.by', '.ru', '.kz',
    '.ge', '.am', '.az', '.kg', '.tj', '.tm', '.uz', '.mn',
    '.kr', '.tw', '.hk', '.sg', '.my', '.th', '.ph', '.vn',
    '.id', '.nz', '.za', '.eg', '.ma', '.tn', '.dz', '.ly',
    '.sd', '.et', '.ke', '.ug', '.tz', '.rw', '.gh', '.ng',
    '.sn', '.ci', '.cm', '.cd', '.ao', '.zm', '.zw', '.bw',
    '.na', '.sz', '.ls', '.mg', '.mu', '.sc', '.km', '.dj',
    '.so', '.er', '.ss', '.cf', '.td', '.ne', '.ml', '.bf',
    '.bj', '.tg', '.gw', '.gn', '.sl', '.lr', '.cv', '.mr',
    '.gq', '.ga', '.cg', '.st', '.gq', '.ao', '.zm', '.mw',
    '.mz', '.mg', '.mu', '.sc', '.km', '.dj', '.so', '.er'
]

# File extensions that should be FILE_PATH, not DOMAIN
FILE_EXTENSIONS = [
    '.img', '.exe', '.dll', '.bat', '.cmd', '.ps1', '.sh', '.py',
    '.js', '.html', '.css', '.json', '.xml', '.txt', '.log', '.csv',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.rar', '.tar', '.gz', '.7z', '.iso', '.bin', '.dat',
    '.db', '.sql', '.sqlite', '.mdb', '.accdb', '.pst', '.ost',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg',
    '.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv',
    '.psd', '.ai', '.eps', '.indd', '.sketch', '.fig', '.xd'
]

# Known entity type catalogs
KNOWN_ENTITY_CATALOGS = {
    'MALWARE_TYPE': [
        'Trojan', 'Virus', 'Worm', 'Rootkit', 'Spyware', 'Adware',
        'Ransomware', 'Botnet', 'Backdoor', 'Keylogger', 'Stealer',
        'Downloader', 'Dropper', 'DLL', 'PUP', 'PUA', 'Scareware',
        'Fileless', 'Macro', 'Script', 'Polymorphic', 'Metamorphic',
        'Obfuscated', 'Packed', 'Encrypted', 'APT', 'Zero-day'
    ],
    'THREAT_ACTOR': [
        'APT29', 'APT28', 'Lazarus', 'FIN7', 'UNC2452', 'Wizard Spider',
        'Ryuk', 'Conti', 'Maze', 'REvil', 'LockBit', 'BlackMatter',
        'DarkSide', 'DoppelPaymer', 'Egregor', 'Ragnarok', 'Sodinokibi',
        'TrickBot', 'Emotet', 'QakBot', 'IcedID', 'BazarLoader',
        'Zloader', 'Dridex', 'Gozi', 'Zeus', 'SpyEye', 'Citadel'
    ],
    'COMPLIANCE_FRAMEWORK': [
        'GDPR', 'HIPAA', 'PCI DSS', 'SOX', 'FISMA', 'NIST CSF',
        'ISO 27001', 'ISO 27002', 'SOC 2', 'FedRAMP', 'CMMC',
        'CIS Controls', 'OWASP Top 10', 'SANS Top 25', 'CCPA',
        'PIPEDA', 'LGPD', 'PDPA', 'PDPB', 'POPI', 'APPI'
    ],
    'LLM_MODEL': [
        'GPT-4', 'GPT-3.5', 'GPT-3', 'GPT-2', 'Claude 3', 'Claude 2',
        'Claude', 'Gemini Pro', 'Gemini Ultra', 'PaLM', 'LaMDA',
        'LLaMA 2', 'LLaMA', 'Mistral', 'Mixtral', 'Falcon', 'BLOOM',
        'BERT', 'RoBERTa', 'T5', 'BART', 'ELECTRA', 'ALBERT'
    ],
    'LLM_PROVIDER': [
        'OpenAI', 'Anthropic', 'Google', 'Microsoft', 'Meta', 'Amazon',
        'Cohere', 'AI21 Labs', 'Hugging Face', 'Stability AI', 'Midjourney',
        'Jasper', 'Copy.ai', 'Writer', 'Grammarly', 'Notion AI'
    ],
    'CLOUD_PROVIDER': [
        'AWS', 'Azure', 'GCP', 'Google Cloud', 'Oracle Cloud', 'IBM Cloud',
        'Alibaba Cloud', 'Tencent Cloud', 'DigitalOcean', 'Linode', 'Vultr',
        'Heroku', 'Netlify', 'Vercel', 'Cloudflare', 'Fastly', 'Akamai'
    ],
    'PROTOCOL_TYPE': [
        'HTTP', 'HTTPS', 'FTP', 'FTPS', 'SFTP', 'SSH', 'Telnet', 'RDP',
        'VNC', 'SMB', 'CIFS', 'NFS', 'LDAP', 'LDAPS', 'DNS', 'DHCP',
        'SNMP', 'ICMP', 'TCP', 'UDP', 'IP', 'IPv6', 'ARP', 'BGP',
        'OSPF', 'EIGRP', 'RIP', 'IS-IS', 'MPLS', 'VPN', 'IPsec',
        'TLS', 'SSL', 'TLS 1.3', 'TLS 1.2', 'TLS 1.1', 'TLS 1.0'
    ],
    'TOOL': [
        'Nmap', 'Wireshark', 'Metasploit', 'Burp Suite', 'OWASP ZAP',
        'Nessus', 'OpenVAS', 'Qualys', 'Rapid7', 'Tenable', 'Splunk',
        'ELK Stack', 'Elasticsearch', 'Logstash', 'Kibana', 'Grafana',
        'Prometheus', 'Nagios', 'Zabbix', 'PRTG', 'SolarWinds',
        'CrowdStrike', 'Carbon Black', 'SentinelOne', 'Cylance',
        'FireEye', 'Mandiant', 'Palo Alto', 'Fortinet', 'Check Point'
    ]
}


def generate_domain_catalog_examples() -> List[Tuple[str, List]]:
    """Generate domain catalog examples with valid extensions."""
    examples = []
    
    # Catalog format examples
    catalog_formats = [
        "Available domain types: .com, .org, .net, .edu, .gov, .io, .co, .ai, .dev, .tech",
        "Domain extensions include: .com, .org, .net, .edu, .gov, .mil, .int, .io, .co, .ai",
        "Supported TLDs: .com, .org, .net, .edu, .gov, .io, .co, .ai, .dev, .tech, .cloud, .app",
        "Valid domain suffixes: .com, .org, .net, .edu, .gov, .io, .co, .ai, .dev, .tech, .info, .biz",
        "Domain type catalog: .com (commercial), .org (organization), .net (network), .edu (education), .gov (government)",
        "Top-level domains: .com, .org, .net, .edu, .gov, .mil, .int, .io, .co, .ai, .dev, .tech",
    ]
    
    for catalog_text in catalog_formats:
        entities = []
        # Extract domains from the catalog
        for ext in VALID_DOMAIN_EXTENSIONS[:15]:  # Limit to first 15 for readability
            if ext in catalog_text:
                # Find the domain example (e.g., "example.com")
                pattern = rf'\b\w+{re.escape(ext)}\b'
                matches = re.findall(pattern, catalog_text)
                for match in matches:
                    entities.append([catalog_text.index(match), catalog_text.index(match) + len(match), "DOMAIN"])
                # Also label the extension itself if it appears standalone
                if ext in catalog_text and f'example{ext}' not in catalog_text:
                    idx = catalog_text.find(ext)
                    if idx != -1:
                        # Check if it's part of a domain or standalone
                        if idx > 0 and catalog_text[idx-1].isalnum():
                            continue  # Part of a domain
                        entities.append([idx, idx + len(ext), "DOMAIN"])
        
        if entities:
            examples.append((catalog_text, entities))
    
    return examples


def generate_file_path_context_examples() -> List[Tuple[str, List]]:
    """Generate longer context examples for FILE_PATH, especially .img files."""
    examples = []
    
    # .img file examples with longer context
    img_texts = [
        "Raj opened the xyz.img file from the local C: drive and opened it in Adobe Photoshop but the Photoshop crashed because the file xyz.img had virus XXX in it and his machine immediately got infected.",
        "The security analyst discovered a suspicious disk.img file in the C:\\Users\\Admin\\Downloads\\ directory. When they attempted to mount the disk.img file using VirtualBox, the system detected malware embedded within the disk.img file.",
        "The forensic investigator found a backup.img file in the /home/user/Documents/ folder. The backup.img file contained sensitive data and was encrypted with AES-256. When they tried to extract the backup.img file, the system reported corruption in the backup.img file structure.",
        "The malware sample malware.img was downloaded from a suspicious website. The malware.img file was analyzed in a sandbox environment, and the analysis revealed that the malware.img file contained a keylogger that was activated when the malware.img file was executed.",
    ]
    
    # Fix the entity boundaries properly
    for text in img_texts:
        entities = []
        # Find all file paths in the text
        # Pattern for Windows paths: C:\... or \\server\...
        win_pattern = r'[A-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*\.(img|exe|dll|bat|cmd|ps1|sh|py|js|html|css|json|xml|txt|log|csv|pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar|tar|gz|7z|iso|bin|dat|db|sql|sqlite|mdb|accdb|pst|ost|jpg|jpeg|png|gif|bmp|tiff|svg|mp3|mp4|avi|mov|wmv|flv|mkv|psd|ai|eps|indd|sketch|fig|xd)'
        # Pattern for Unix paths: /path/to/file.ext or ~/path/to/file.ext
        unix_pattern = r'(?:/|~)(?:[^/\s]+/)*[^/\s]+\.(img|exe|dll|bat|cmd|ps1|sh|py|js|html|css|json|xml|txt|log|csv|pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar|tar|gz|7z|iso|bin|dat|db|sql|sqlite|mdb|accdb|pst|ost|jpg|jpeg|png|gif|bmp|tiff|svg|mp3|mp4|avi|mov|wmv|flv|mkv|psd|ai|eps|indd|sketch|fig|xd)'
        # Pattern for network paths: \\server\share\file.ext
        net_pattern = r'\\\\[^\\]+(?:\\[^\\]+)+\.(img|exe|dll|bat|cmd|ps1|sh|py|js|html|css|json|xml|txt|log|csv|pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar|tar|gz|7z|iso|bin|dat|db|sql|sqlite|mdb|accdb|pst|ost|jpg|jpeg|png|gif|bmp|tiff|svg|mp3|mp4|avi|mov|wmv|flv|mkv|psd|ai|eps|indd|sketch|fig|xd)'
        # Pattern for simple filenames with extensions (standalone)
        simple_pattern = r'\b\w+\.(img|exe|dll|bat|cmd|ps1|sh|py|js|html|css|json|xml|txt|log|csv|pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar|tar|gz|7z|iso|bin|dat|db|sql|sqlite|mdb|accdb|pst|ost|jpg|jpeg|png|gif|bmp|tiff|svg|mp3|mp4|avi|mov|wmv|flv|mkv|psd|ai|eps|indd|sketch|fig|xd)\b'
        
        found_paths = set()
        for pattern in [win_pattern, unix_pattern, net_pattern, simple_pattern]:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                start, end = match.span()
                path_text = text[start:end]
                # Avoid duplicates
                if path_text not in found_paths:
                    entities.append([start, end, "FILE_PATH"])
                    found_paths.add(path_text)
        
        if entities:
            examples.append((text, entities))
    
    return examples


def generate_overlapping_entity_context() -> List[Tuple[str, List]]:
    """Generate longer context examples for overlapping entities."""
    examples = []
    
    # Examples where entities might overlap or be confused
    overlapping_texts = [
        "The security team investigated the domain example.com which was hosting malicious content. They found that the email admin@example.com was used to register the domain, and the IP address 192.168.1.100 was associated with the domain example.com in DNS records.",
        "The threat actor APT29 used the GitHub repository github.com/apt29/malware to host their tools. The repository contained multiple files including malware.exe and the configuration file config.json. The domain github.com was also used to host command and control infrastructure.",
        "The CVE-2021-44228 vulnerability was exploited on the server at IP 10.0.0.1. The server was running Apache 2.4.41 on port 443. The domain vulnerable.example.com was pointing to this IP address, and the SSL certificate for vulnerable.example.com was expired.",
    ]
    
    # Extract entities using patterns
    for text in overlapping_texts:
        entities = []
        
        # Find domains
        domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
        for match in re.finditer(domain_pattern, text):
            start, end = match.span()
            domain_text = text[start:end]
            # Skip if it's part of an email
            if start > 0 and text[start-1] == '@':
                continue
            entities.append([start, end, "DOMAIN"])
        
        # Find email addresses
        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        for match in re.finditer(email_pattern, text):
            start, end = match.span()
            entities.append([start, end, "EMAIL_ADDRESS"])
        
        # Find IP addresses
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        for match in re.finditer(ip_pattern, text):
            start, end = match.span()
            ip_text = text[start:end]
            # Validate it's a real IP
            parts = ip_text.split('.')
            if all(0 <= int(p) <= 255 for p in parts):
                entities.append([start, end, "IP_ADDRESS"])
        
        # Find CVE IDs
        cve_pattern = r'\bCVE-\d{4}-\d{4,7}\b'
        for match in re.finditer(cve_pattern, text, re.IGNORECASE):
            start, end = match.span()
            entities.append([start, end, "CVE_ID"])
        
        # Find threat actors (known ones)
        threat_actor_pattern = r'\b(APT29|APT28|Lazarus|FIN7|UNC2452)\b'
        for match in re.finditer(threat_actor_pattern, text, re.IGNORECASE):
            start, end = match.span()
            entities.append([start, end, "THREAT_ACTOR"])
        
        # Find repositories
        repo_pattern = r'github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+'
        for match in re.finditer(repo_pattern, text, re.IGNORECASE):
            start, end = match.span()
            entities.append([start, end, "REPOSITORY"])
        
        # Find file paths
        file_pattern = r'\b\w+\.(exe|dll|bat|json|img|pdf|doc|txt)\b'
        for match in re.finditer(file_pattern, text, re.IGNORECASE):
            start, end = match.span()
            entities.append([start, end, "FILE_PATH"])
        
        # Find tools
        if 'Apache' in text:
            idx = text.find('Apache')
            if idx != -1:
                entities.append([idx, idx + 6, "TOOL"])
        
        # Find ports
        port_pattern = r'\b(?:port\s+)?(\d{1,5})\b'
        for match in re.finditer(port_pattern, text, re.IGNORECASE):
            port_num = int(match.group(1))
            if 1 <= port_num <= 65535:
                start, end = match.span(1)  # Just the number
                entities.append([start, end, "PORT"])
        
        if entities:
            examples.append((text, entities))
    
    return examples


def generate_catalog_examples() -> List[Tuple[str, List]]:
    """Generate catalog/list format examples for known entity types."""
    examples = []
    
    for entity_type, items in KNOWN_ENTITY_CATALOGS.items():
        # Different catalog formats
        catalog_formats = [
            f"Available {entity_type.lower().replace('_', ' ')}s: {', '.join(items[:10])}",
            f"{entity_type} catalog: {', '.join(items[:8])}",
            f"Known {entity_type.lower().replace('_', ' ')}s include: {', '.join(items[:12])}",
            f"List of {entity_type.lower().replace('_', ' ')}s: {', '.join(items[:10])}",
            f"Supported {entity_type.lower().replace('_', ' ')}s: {', '.join(items[:8])}",
        ]
        
        for catalog_text in catalog_formats:
            entities = []
            # Find each item in the catalog
            for item in items[:15]:  # Limit to first 15
                if item in catalog_text:
                    # Find all occurrences
                    start = 0
                    while True:
                        idx = catalog_text.find(item, start)
                        if idx == -1:
                            break
                        # Check if it's a whole word (not part of another word)
                        if (idx == 0 or not catalog_text[idx-1].isalnum()) and \
                           (idx + len(item) >= len(catalog_text) or not catalog_text[idx + len(item)].isalnum()):
                            entities.append([idx, idx + len(item), entity_type])
                        start = idx + 1
            
            if entities:
                examples.append((catalog_text, entities))
    
    return examples


def add_examples_to_file(file_path: Path, examples: List[Tuple[str, List]], description: str):
    """Add examples to a JSONL file."""
    if not file_path.exists():
        print(f"⚠️  File not found: {file_path}")
        return 0
    
    added = 0
    existing_texts = set()
    
    # Read existing examples to avoid duplicates
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
            # Skip if duplicate
            if text.strip().lower() in existing_texts:
                continue
            
            # Validate entities
            valid_entities = []
            for start, end, label in entities:
                if 0 <= start < end <= len(text):
                    entity_text = text[start:end]
                    # Basic validation
                    if entity_text.strip():
                        valid_entities.append([start, end, label])
            
            if valid_entities:
                data = {
                    "text": text,
                    "entities": valid_entities
                }
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
                existing_texts.add(text.strip().lower())
                added += 1
    
    if added > 0:
        print(f"  ✅ Added {added} {description} examples to {file_path.name}")
    
    return added


def main():
    base_dir = Path("entities-intent")
    
    print("=" * 80)
    print("ADDING CATALOG LISTS AND LONGER CONTEXT EXAMPLES")
    print("=" * 80)
    print()
    
    total_added = 0
    
    # 1. Domain catalog examples
    print("1. Generating domain catalog examples...")
    domain_examples = generate_domain_catalog_examples()
    print(f"   Generated {len(domain_examples)} domain catalog examples")
    
    # Add to relevant files
    domain_files = [
        base_dir / "network_security" / "network_security_entities.jsonl",
        base_dir / "threat_intel" / "threat_intel_entities.jsonl",
        base_dir / "osint" / "osint_entities.jsonl",
    ]
    
    for file_path in domain_files:
        if file_path.exists():
            added = add_examples_to_file(file_path, domain_examples, "domain catalog")
            total_added += added
    
    print()
    
    # 2. File path context examples (especially .img)
    print("2. Generating file path context examples...")
    file_path_examples = generate_file_path_context_examples()
    print(f"   Generated {len(file_path_examples)} file path context examples")
    
    # Add to relevant files
    file_path_files = [
        base_dir / "endpoint_security" / "endpoint_security_entities.jsonl",
        base_dir / "incident_response" / "incident_response_entities.jsonl",
        base_dir / "detection_correlation" / "detection_correlation_entities.jsonl",
    ]
    
    for file_path in file_path_files:
        if file_path.exists():
            added = add_examples_to_file(file_path, file_path_examples, "file path context")
            total_added += added
    
    print()
    
    # 3. Overlapping entity context examples
    print("3. Generating overlapping entity context examples...")
    overlapping_examples = generate_overlapping_entity_context()
    print(f"   Generated {len(overlapping_examples)} overlapping entity context examples")
    
    # Add to relevant files
    overlapping_files = [
        base_dir / "threat_intel" / "threat_intel_entities.jsonl",
        base_dir / "incident_response" / "incident_response_entities.jsonl",
        base_dir / "detection_correlation" / "detection_correlation_entities.jsonl",
        base_dir / "network_security" / "network_security_entities.jsonl",
    ]
    
    for file_path in overlapping_files:
        if file_path.exists():
            added = add_examples_to_file(file_path, overlapping_examples, "overlapping entity context")
            total_added += added
    
    print()
    
    # 4. Catalog examples for known entity types
    print("4. Generating catalog examples for known entity types...")
    catalog_examples = generate_catalog_examples()
    print(f"   Generated {len(catalog_examples)} catalog examples")
    
    # Map entity types to files
    entity_file_mapping = {
        'MALWARE_TYPE': [base_dir / "threat_intel" / "threat_intel_entities.jsonl",
                        base_dir / "incident_response" / "incident_response_entities.jsonl",
                        base_dir / "endpoint_security" / "endpoint_security_entities.jsonl"],
        'THREAT_ACTOR': [base_dir / "threat_intel" / "threat_intel_entities.jsonl",
                        base_dir / "incident_response" / "incident_response_entities.jsonl"],
        'COMPLIANCE_FRAMEWORK': [base_dir / "audit_compliance" / "audit_compliance_entities.jsonl",
                                base_dir / "governance_risk_strategy" / "governance_risk_strategy_entities.jsonl"],
        'LLM_MODEL': [base_dir / "ai_security" / "ai_security_entities.jsonl"],
        'LLM_PROVIDER': [base_dir / "ai_security" / "ai_security_entities.jsonl"],
        'CLOUD_PROVIDER': [base_dir / "cloud_security_cnapp" / "cloud_security_cnapp_entities.jsonl"],
        'PROTOCOL_TYPE': [base_dir / "network_security" / "network_security_entities.jsonl"],
        'TOOL': [base_dir / "threat_intel" / "threat_intel_entities.jsonl",
                base_dir / "incident_response" / "incident_response_entities.jsonl"],
    }
    
    # Group examples by entity type
    examples_by_type = {}
    for text, entities in catalog_examples:
        for start, end, label in entities:
            if label not in examples_by_type:
                examples_by_type[label] = []
            examples_by_type[label].append((text, entities))
            break  # Only add once per example
    
    # Add to relevant files
    for entity_type, file_list in entity_file_mapping.items():
        if entity_type in examples_by_type:
            for file_path in file_list:
                if file_path.exists():
                    added = add_examples_to_file(file_path, examples_by_type[entity_type], 
                                                f"{entity_type} catalog")
                    total_added += added
    
    print()
    print("=" * 80)
    print(f"✅ COMPLETE: Added {total_added} total examples")
    print("=" * 80)


if __name__ == "__main__":
    main()

