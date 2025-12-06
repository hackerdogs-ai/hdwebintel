#!/usr/bin/env python3
"""
Improve post-processing filter to catch more false positives.
This script updates the filter with better patterns and validation.
"""

import re
from pathlib import Path

# Enhanced common words that should NOT be entities
ENHANCED_COMMON_WORDS = {
    'csrf', 'javascript', 'json', 'xml', 'html', 'css', 'python', 'base64',
    'debunk', 'relative', 'absolute', 'find', 'extract', 'url', 'import',
    'investigate', 'check', 'verify', 'analyze', 'detect', 'monitor', 'track',
    'race', 'time', 'events', 'exercise', 'kernel-level', 'log', 'syslog',
    'api', 'transfer', 'endpoint', 'path', 'file', 'directory', 'system',
    'security', 'threat', 'attack', 'malware', 'vulnerability', 'incident',
    'response', 'forensics', 'analysis', 'investigation', 'compliance',
    'audit', 'policy', 'control', 'access', 'permission', 'user', 'admin',
    'server', 'client', 'network', 'protocol', 'port', 'service', 'application',
    'database', 'storage', 'backup', 'recovery', 'encryption', 'authentication',
    'authorization', 'identity', 'session', 'token', 'certificate', 'key',
    'password', 'credential', 'account', 'login', 'logout', 'session',
    'request', 'response', 'query', 'command', 'execution', 'process',
    'thread', 'memory', 'disk', 'file', 'directory', 'path', 'location',
    'configuration', 'setting', 'parameter', 'option', 'flag', 'switch',
    'mode', 'state', 'status', 'result', 'output', 'input', 'data',
    'information', 'content', 'message', 'notification', 'alert', 'warning',
    'error', 'exception', 'failure', 'success', 'completion', 'progress',
    'action', 'operation', 'task', 'job', 'work', 'activity', 'event',
    'occurrence', 'instance', 'example', 'case', 'scenario', 'situation',
    'condition', 'requirement', 'specification', 'documentation', 'report',
    'log', 'entry', 'record', 'entry', 'item', 'element', 'component',
    'module', 'function', 'method', 'procedure', 'routine', 'algorithm',
    'logic', 'code', 'script', 'program', 'application', 'software',
    'hardware', 'device', 'equipment', 'tool', 'utility', 'resource',
    'asset', 'property', 'attribute', 'characteristic', 'feature', 'capability',
    'functionality', 'behavior', 'performance', 'efficiency', 'effectiveness',
    'quality', 'reliability', 'availability', 'scalability', 'maintainability',
    'usability', 'accessibility', 'compatibility', 'interoperability',
    'portability', 'security', 'privacy', 'confidentiality', 'integrity',
    'availability', 'authenticity', 'non-repudiation', 'accountability',
    'traceability', 'auditability', 'compliance', 'governance', 'risk',
    'threat', 'vulnerability', 'exploit', 'attack', 'incident', 'breach',
    'compromise', 'intrusion', 'infection', 'malware', 'virus', 'trojan',
    'worm', 'ransomware', 'spyware', 'adware', 'rootkit', 'backdoor',
    'keylogger', 'botnet', 'phishing', 'spoofing', 'sniffing', 'eavesdropping',
    'man-in-the-middle', 'denial-of-service', 'distributed-denial-of-service',
    'buffer-overflow', 'sql-injection', 'cross-site-scripting', 'csrf',
    'session-hijacking', 'privilege-escalation', 'lateral-movement',
    'persistence', 'evasion', 'defense-evasion', 'credential-access',
    'discovery', 'collection', 'exfiltration', 'impact', 'execution',
    'command-and-control', 'initial-access', 'execution', 'persistence',
    'privilege-escalation', 'defense-evasion', 'credential-access',
    'discovery', 'lateral-movement', 'collection', 'command-and-control',
    'exfiltration', 'impact', 'reconnaissance', 'weaponization', 'delivery',
    'exploitation', 'installation', 'command-and-control', 'actions-on-objectives',
}

# Enhanced common phrases
ENHANCED_COMMON_PHRASES = {
    'i need', 'i want', 'i have', 'i am', 'i was', 'i will', 'i can', 'i should',
    'is safe', 'is not', 'is good', 'is bad', 'is ok', 'is fine', 'is working',
    "what's up", "what's", "that's", "it's", "there's", "here's", "who's",
    'can you', 'could you', 'would you', 'should you', 'will you', 'do you',
    'need to', 'want to', 'have to', 'got to', 'going to', 'trying to',
    'look at', 'look for', 'look up', 'check if', 'check for', 'check on',
    'help me', 'help with', 'help to', 'let me', 'tell me', 'show me',
    'the system', 'the security', 'the application', 'the network',
    'the server', 'the client', 'the user', 'the admin', 'the team',
    'security team', 'incident response', 'threat intelligence',
    'security monitoring', 'security analysis', 'security investigation',
    'security audit', 'security compliance', 'security policy',
    'security control', 'security measure', 'security procedure',
    'security requirement', 'security standard', 'security framework',
    'security best practice', 'security guideline', 'security recommendation',
}

# Patterns for validation
VALIDATION_PATTERNS = {
    'IP_ADDRESS': re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'),
    'DOMAIN': re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'),
    'EMAIL_ADDRESS': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
    'URL': re.compile(r'^https?://[^\s]+|ftp://[^\s]+|www\.[^\s]+'),
    'FILE_PATH': re.compile(r'^[A-Z]:\\|^/|^\\\\|^~/'),
    'PHONE_NUMBER': re.compile(r'^\+?[\d\s\-\(\)]{7,}$'),
    'HASH': re.compile(r'^[a-fA-F0-9]{32,64}$'),
    'CVE_ID': re.compile(r'^CVE-\d{4}-\d{4,7}$', re.IGNORECASE),
    'DATE': re.compile(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|[A-Z][a-z]+ \d{1,2}, \d{4}'),
    'TIME': re.compile(r'\d{1,2}:\d{2}(:\d{2})?( [AP]M)?'),
}

def is_false_positive(text: str, label: str) -> bool:
    """Check if entity is likely a false positive."""
    text_lower = text.lower().strip()
    
    # Check common words
    if text_lower in ENHANCED_COMMON_WORDS:
        # Allow only if it's a legitimate entity type
        if label not in ['PERSON', 'ORGANIZATION', 'LOCATION', 'THREAT_ACTOR', 'MALWARE_TYPE']:
            return True
    
    # Check common phrases
    if text_lower in ENHANCED_COMMON_PHRASES:
        return True
    
    # Check if it's a partial word (common in false positives)
    if len(text) <= 2 and label not in ['PORT', 'CVE_ID']:
        return True
    
    # Validate against patterns
    if label in VALIDATION_PATTERNS:
        pattern = VALIDATION_PATTERNS[label]
        if not pattern.match(text):
            return True
    
    # TOOL entity validation - must be a real tool name
    if label == "TOOL":
        if text_lower in ['csrf', 'javascript', 'json', 'xml', 'html', 'base64', 'debunk', 'relative']:
            return True
        # TOOL should be capitalized or be a known tool
        if not (text[0].isupper() or text_lower in ['nmap', 'wireshark', 'metasploit', 'burp', 'owasp']):
            if text_lower in ENHANCED_COMMON_WORDS:
                return True
    
    # REPOSITORY validation - must be in format user/repo
    if label == "REPOSITORY":
        if not re.match(r'^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$|github\.com/[^\s]+|gitlab\.com/[^\s]+', text):
            # Check if it's actually a URL
            if VALIDATION_PATTERNS['URL'].match(text):
                return True  # Should be URL, not REPOSITORY
            # Check if it's actually a file path
            if VALIDATION_PATTERNS['FILE_PATH'].match(text):
                return True  # Should be FILE_PATH, not REPOSITORY
            return True
    
    # DATE validation - must match date patterns
    if label == "DATE":
        if not VALIDATION_PATTERNS['DATE'].search(text):
            # Check if it's actually a file path
            if VALIDATION_PATTERNS['FILE_PATH'].match(text):
                return True  # Should be FILE_PATH, not DATE
            return True
    
    return False

def update_filter_file():
    """Update the post-processing filter file."""
    filter_file = Path("fix_entity_extraction.py")
    
    if not filter_file.exists():
        print(f"⚠️  Filter file not found: {filter_file}")
        return
    
    # Read current file
    with open(filter_file, 'r') as f:
        content = f.read()
    
    # Update COMMON_WORDS
    old_common_words = "COMMON_WORDS = {"
    if old_common_words in content:
        # Find and replace
        start = content.find(old_common_words)
        end = content.find("}", start) + 1
        new_common_words = "COMMON_WORDS = {\n    " + ",\n    ".join([f"'{w}'" for w in sorted(ENHANCED_COMMON_WORDS)]) + "\n}"
        content = content[:start] + new_common_words + content[end:]
    
    # Update COMMON_PHRASES
    old_common_phrases = "COMMON_PHRASES = {"
    if old_common_phrases in content:
        start = content.find(old_common_phrases)
        end = content.find("}", start) + 1
        new_common_phrases = "COMMON_PHRASES = {\n    " + ",\n    ".join([f"'{p}'" for p in sorted(ENHANCED_COMMON_PHRASES)]) + "\n}"
        content = content[:start] + new_common_phrases + content[end:]
    
    # Add enhanced validation
    validation_code = '''
def is_false_positive_enhanced(text: str, label: str) -> bool:
    """Enhanced false positive detection."""
    text_lower = text.lower().strip()
    
    # Check common words
    if text_lower in COMMON_WORDS:
        if label not in ['PERSON', 'ORGANIZATION', 'LOCATION', 'THREAT_ACTOR', 'MALWARE_TYPE']:
            return True
    
    # Check common phrases
    if text_lower in COMMON_PHRASES:
        return True
    
    # TOOL validation
    if label == "TOOL":
        if text_lower in ['csrf', 'javascript', 'json', 'xml', 'html', 'base64', 'debunk', 'relative']:
            return True
    
    # REPOSITORY validation
    if label == "REPOSITORY":
        if not re.match(r'^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$|github\\.com/[^\\s]+|gitlab\\.com/[^\\s]+', text):
            if ENTITY_PATTERNS.get('URL', re.compile('')).match(text):
                return True
            if ENTITY_PATTERNS.get('FILE_PATH', re.compile('')).match(text):
                return True
            return True
    
    # DATE validation
    if label == "DATE":
        if not ENTITY_PATTERNS.get('DATE', re.compile('')).search(text):
            if ENTITY_PATTERNS.get('FILE_PATH', re.compile('')).match(text):
                return True
            return True
    
    return False
'''
    
    # Add validation function if not present
    if "is_false_positive_enhanced" not in content:
        # Find filter_entities function and add before it
        if "def filter_entities" in content:
            pos = content.find("def filter_entities")
            content = content[:pos] + validation_code + "\n" + content[pos:]
    
    # Update filter_entities to use enhanced validation
    if "def filter_entities" in content and "is_false_positive_enhanced" in content:
        # Update the function to use enhanced validation
        old_check = "if text_lower in COMMON_WORDS and label not in"
        if old_check in content:
            # Replace with enhanced check
            content = content.replace(
                "if text_lower in COMMON_WORDS and label not in ['PERSON', 'ORGANIZATION', 'LOCATION', 'THREAT_ACTOR']:",
                "if is_false_positive_enhanced(text_clean, label):"
            )
    
    # Write updated file
    with open(filter_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Updated filter file: {filter_file}")

def main():
    print("="*80)
    print("IMPROVE POST-PROCESSING FILTER")
    print("="*80)
    print("\nEnhancing filter with:")
    print("  - Expanded common words list")
    print("  - Enhanced common phrases")
    print("  - Better TOOL validation")
    print("  - Better REPOSITORY vs URL distinction")
    print("  - Better DATE vs FILE_PATH distinction")
    print()
    
    update_filter_file()
    
    print("\n✅ Filter improvements applied!")
    print("="*80)

if __name__ == "__main__":
    main()

