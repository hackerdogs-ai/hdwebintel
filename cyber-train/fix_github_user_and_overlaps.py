#!/usr/bin/env python3
"""
Fix GITHUB_USER mislabeling and overlapping entities.

This script:
1. Removes GITHUB_USER labels that don't have '@' prefix or GitHub context
2. Fixes overlapping entities (IP_ADDRESS, DOMAIN, EMAIL_ADDRESS, etc.)
3. Adds more specific training data for IP addresses and other entities
4. Makes entities more unique/distinct
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set

# Entity patterns (more specific)
IP_PATTERN = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
IPV6_PATTERN = re.compile(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|::1|::')
DOMAIN_PATTERN = re.compile(r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b')
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,}\b')
PHONE_PATTERN = re.compile(r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b')
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
GITHUB_REPO_PATTERN = re.compile(r'[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+')
GITHUB_URL_PATTERN = re.compile(r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)*')
GITHUB_USER_PATTERN = re.compile(r'@[a-zA-Z0-9]([a-zA-Z0-9]|-(?![.-])){0,38}')  # MUST have @ prefix
GITHUB_COMMIT_PATTERN = re.compile(r'\b[a-f0-9]{7,40}\b')

# Common words that should NEVER be entities
COMMON_WORDS_NEVER = {
    'the', 'a', 'an', 'this', 'that', 'for', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'from',
    'with', 'by', 'of', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must',
    'i', 'me', 'my', 'you', 'your', 'he', 'she', 'it', 'we', 'they', 'them',
    'what', 'when', 'where', 'why', 'how', 'who', 'which', 'whose', 'whom',
    'up', 'down', 'out', 'off', 'over', 'under', 'above', 'below',
    'code', 'import', 'os', 'python', 'javascript', 'json', 'xml',
    'metadata', 'image', 'video', 'profile', 'social', 'media',
    'detected', 'found', 'check', 'verify', 'investigate', 'analyze', 'monitor', 'track',
    'execute', 'block', 'isolate', 'generate', 'find', 'show', 'get', 'set',
    'compliance', 'requirements', 'data', 'system', 'network', 'threat', 'intelligence',
    'report', 'tool', 'type', 'count', 'metric', 'value', 'number', 'phone', 'email', 'address',
    'card', 'credit', 'bank', 'account', 'ssn', 'long', 'various', 'types', 'appear',
    'anomalies', 'lateral', 'latitude', 'longitude', 'used', 'wannacry', 'campaign',
    'repository', 'repo', 'github', 'commit', 'branch', 'tag', 'release', 'issue', 'gist',
    'if', 'our', 'domain', 'ip', 'host', 'port', 'user', 'access', 'attempt', 'attempts',
    'identified', 'shows', 'connections', 'indicators', 'tools', 'records', 'updated',
    'analysis', 'investigation', 'intelligence', 'threat', 'policy', 'secure', 'access',
    'score', 'vulnerabilities', 'enterprise', 'policies', 'privacy', 'coverage', 'compliance',
    'improved', 'open', 'management', 'cloud', 'achieved', 'secure'
}

# Statistics
stats = {
    'files_processed': 0,
    'lines_processed': 0,
    'github_user_removed': 0,
    'github_user_kept': 0,
    'entities_fixed': 0,
    'entities_added': 0,
    'overlaps_resolved': 0
}

def is_legitimate_github_user(text: str, entity_text: str, context: str) -> bool:
    """Check if GITHUB_USER label is legitimate."""
    # Must have @ prefix
    if entity_text.startswith('@'):
        return True
    
    # Or must be in GitHub context
    context_lower = context.lower()
    github_keywords = ['github', 'repo', 'repository', 'commit', 'pull request', 'issue', 'gist', 'branch', 'tag', 'release']
    if any(keyword in context_lower for keyword in github_keywords):
        # Check if entity_text looks like a username (alphanumeric, hyphens, underscores)
        if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9]|-(?![.-])){0,38}$', entity_text):
            return True
    
    return False

def extract_entities_by_pattern(text: str) -> List[Tuple[int, int, str]]:
    """Extract entities using specific patterns."""
    entities = []
    used_spans = set()
    
    # IP addresses (IPv4)
    for match in IP_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in used_spans:
            entities.append((match.start(), match.end(), 'IP_ADDRESS'))
            used_spans.add(span)
    
    # IPv6 addresses
    for match in IPV6_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in used_spans:
            entities.append((match.start(), match.end(), 'IPV6_ADDRESS'))
            used_spans.add(span)
    
    # Domains (but not if part of email or URL)
    for match in DOMAIN_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in used_spans:
            # Check if it's part of email or URL
            context_start = max(0, match.start() - 10)
            context_end = min(len(text), match.end() + 10)
            context = text[context_start:context_end]
            if '@' not in context and 'http' not in context.lower():
                entities.append((match.start(), match.end(), 'DOMAIN'))
                used_spans.add(span)
    
    # Email addresses
    for match in EMAIL_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in used_spans:
            entities.append((match.start(), match.end(), 'EMAIL_ADDRESS'))
            used_spans.add(span)
    
    # CVE IDs
    for match in CVE_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in used_spans:
            entities.append((match.start(), match.end(), 'CVE_ID'))
            used_spans.add(span)
    
    # Phone numbers
    for match in PHONE_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in used_spans:
            entities.append((match.start(), match.end(), 'PHONE_NUMBER'))
            used_spans.add(span)
    
    # URLs
    for match in URL_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in used_spans:
            url_text = match.group()
            if 'github.com' in url_text:
                entities.append((match.start(), match.end(), 'GITHUB_REPO_URL'))
            else:
                entities.append((match.start(), match.end(), 'URL'))
            used_spans.add(span)
    
    # GitHub repos (format: user/repo, not part of URL)
    for match in GITHUB_REPO_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in used_spans:
            # Check it's not part of a URL
            if not (span[0] > 0 and text[span[0]-1] in ':/'):
                entities.append((match.start(), match.end(), 'GITHUB_REPO'))
                used_spans.add(span)
    
    # GitHub users (MUST have @ prefix)
    for match in GITHUB_USER_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in used_spans:
            entities.append((match.start(), match.end(), 'GITHUB_USER'))
            used_spans.add(span)
    
    # GitHub commits (with context)
    for match in GITHUB_COMMIT_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in used_spans:
            context_start = max(0, match.start() - 40)
            context_end = min(len(text), match.end() + 40)
            context = text[context_start:context_end].lower()
            if any(word in context for word in ['commit', 'hash', 'sha', 'git', 'repository', 'repo']):
                entities.append((match.start(), match.end(), 'GITHUB_COMMIT'))
                used_spans.add(span)
    
    return entities

def fix_entities_in_line(data: Dict) -> Dict:
    """Fix entities in a single line."""
    text = data.get('text', '')
    entities = data.get('entities', [])
    
    if not text or not entities:
        return data
    
    # Extract entities by pattern (prioritize these)
    pattern_entities = extract_entities_by_pattern(text)
    pattern_spans = {(start, end) for start, end, _ in pattern_entities}
    
    # Fix existing entities
    fixed_entities = []
    removed_count = 0
    
    for start, end, label in entities:
        entity_text = text[start:end].strip()
        entity_lower = entity_text.lower()
        
        # Skip empty entities
        if not entity_text:
            removed_count += 1
            continue
        
        # Remove common words
        if entity_lower in COMMON_WORDS_NEVER:
            removed_count += 1
            continue
        
        # Fix GITHUB_USER
        if label == 'GITHUB_USER':
            context_start = max(0, start - 50)
            context_end = min(len(text), end + 50)
            context = text[context_start:context_end]
            
            if is_legitimate_github_user(text, entity_text, context):
                # Check if it's already covered by pattern
                if (start, end) not in pattern_spans:
                    fixed_entities.append([start, end, label])
                    stats['github_user_kept'] += 1
            else:
                removed_count += 1
                stats['github_user_removed'] += 1
            continue
        
        # Check if this entity overlaps with a pattern entity
        overlaps_pattern = False
        for p_start, p_end, p_label in pattern_entities:
            if not (end <= p_start or start >= p_end):  # Overlaps
                overlaps_pattern = True
                # Use pattern entity instead
                break
        
        if overlaps_pattern:
            removed_count += 1
            stats['overlaps_resolved'] += 1
            continue
        
        # Keep the entity
        fixed_entities.append([start, end, label])
    
    # Add pattern entities that aren't already in fixed_entities
    fixed_spans = {(start, end) for start, end, _ in fixed_entities}
    for start, end, label in pattern_entities:
        if (start, end) not in fixed_spans:
            fixed_entities.append([start, end, label])
            stats['entities_added'] += 1
    
    # Sort by start position
    fixed_entities.sort(key=lambda x: x[0])
    
    # Remove duplicates
    seen = set()
    unique_entities = []
    for entity in fixed_entities:
        key = (entity[0], entity[1], entity[2])
        if key not in seen:
            seen.add(key)
            unique_entities.append(entity)
    
    stats['entities_fixed'] += len(unique_entities) - len(entities) + removed_count
    
    data['entities'] = unique_entities
    return data

def process_file(file_path: Path) -> None:
    """Process a single file."""
    print(f"Processing {file_path.name}...")
    
    lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                lines.append(line)
                continue
            
            try:
                data = json.loads(line)
                stats['lines_processed'] += 1
                fixed_data = fix_entities_in_line(data)
                lines.append(json.dumps(fixed_data, ensure_ascii=False) + '\n')
            except json.JSONDecodeError:
                lines.append(line)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    stats['files_processed'] += 1

def main():
    """Main function."""
    print("="*80)
    print("FIXING GITHUB_USER MISLABELING AND OVERLAPPING ENTITIES")
    print("="*80)
    
    # Find all entity files
    entity_files = list(Path('entities-intent').rglob('*_entities.jsonl'))
    entity_files = [f for f in entity_files if not f.name.endswith('.backup')]
    
    print(f"\nFound {len(entity_files)} entity files to process")
    
    # Process each file
    for file_path in entity_files:
        try:
            process_file(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Print statistics
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Files processed: {stats['files_processed']}")
    print(f"Lines processed: {stats['lines_processed']}")
    print(f"GITHUB_USER removed: {stats['github_user_removed']}")
    print(f"GITHUB_USER kept: {stats['github_user_kept']}")
    print(f"Entities fixed: {stats['entities_fixed']}")
    print(f"Entities added: {stats['entities_added']}")
    print(f"Overlaps resolved: {stats['overlaps_resolved']}")
    print("="*80)

if __name__ == '__main__':
    main()

