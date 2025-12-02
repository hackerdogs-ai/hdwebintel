#!/usr/bin/env python3
"""
Aggressive fix for remaining entity boundary issues.
Focuses on partial word boundaries and wrong boundaries.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
import shutil
from datetime import datetime

# Patterns
IP_PATTERN = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
IPV6_PATTERN = re.compile(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b::1\b|\bfe80::[0-9a-fA-F:]+')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?[\d\s\-\(\)]{10,}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
GITHUB_REPO_PATTERN = re.compile(r'[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+')
GITHUB_URL_PATTERN = re.compile(r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)*')
GITHUB_USER_PATTERN = re.compile(r'@?[a-zA-Z0-9]([a-zA-Z0-9]|-(?![.-])){0,38}')
GITHUB_GIST_PATTERN = re.compile(r'https?://gist\.github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9]+')
GITHUB_ISSUE_PATTERN = re.compile(r'#[0-9]+')
GITHUB_COMMIT_PATTERN = re.compile(r'\b[a-f0-9]{7,40}\b')

VALID_PATTERNS = {
    'IP_ADDRESS': IP_PATTERN,
    'IPV6_ADDRESS': IPV6_PATTERN,
    'DOMAIN': DOMAIN_PATTERN,
    'CVE_ID': CVE_PATTERN,
    'EMAIL': EMAIL_PATTERN,
    'EMAIL_ADDRESS': EMAIL_PATTERN,
    'PHONE_NUMBER': PHONE_PATTERN,
    'WALLET_ADDRESS': WALLET_PATTERN,
    'URL': URL_PATTERN,
    'GITHUB_REPO': GITHUB_REPO_PATTERN,
    'GITHUB_REPO_URL': GITHUB_URL_PATTERN,
    'GITHUB_USER': GITHUB_USER_PATTERN,
    'GITHUB_GIST': GITHUB_GIST_PATTERN,
    'GITHUB_ISSUE': GITHUB_ISSUE_PATTERN,
    'GITHUB_COMMIT': GITHUB_COMMIT_PATTERN,
}

COMMON_WORDS_NEVER = {
    'the', 'a', 'an', 'this', 'that', 'for', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'from',
    'with', 'by', 'of', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must',
    'i', 'me', 'my', 'you', 'your', 'he', 'she', 'it', 'we', 'they', 'them',
    'what', 'when', 'where', 'why', 'how', 'who', 'which', 'whose', 'whom',
    'up', 'down', 'out', 'off', 'over', 'under', 'above', 'below',
    'access', 'attempt', 'attempts', 'from', 'ip', 'host', 'port', 'user', 'domain',
    'check', 'verify', 'investigate', 'analyze', 'detect', 'monitor', 'track',
    'execute', 'block', 'isolate', 'generate', 'find', 'show', 'get', 'set',
    'compliance', 'requirements', 'data', 'system', 'network', 'threat', 'intelligence',
    'report', 'tool', 'type', 'count', 'metric', 'value', 'number', 'phone', 'email', 'address',
    'card', 'credit', 'bank', 'account', 'ssn', 'long', 'various', 'types', 'appear',
    'anomalies', 'lateral', 'latitude', 'longitude', 'used', 'wannacry', 'campaign',
    'repository', 'repo', 'github', 'commit', 'branch', 'tag', 'release', 'issue', 'gist',
}

PROBLEMATIC_LABELS = {
    'AI_MODEL_TYPE', 'SECURITY_TYPE', 'INCIDENT_TYPE', 'METRIC_TYPE', 'THRESHOLD_TYPE',
    'TOOL', 'TIME_UNIT', 'PRIORITIZATION_TYPE', 'SERVICE', 'SOURCE_TYPE',
    'ENCRYPTION_TYPE', 'VULNERABILITY_ID', 'TRAINING_TYPE', 'INTEGRATION_TYPE',
    'BRANCH', 'COMMIT', 'QUERY_TYPE', 'REQUIREMENT_TYPE', 'PERCENTAGE', 'COUNT',
    'PHONE_NUMBER', 'EMAIL_ADDRESS', 'CREDIT_CARD_NUMBER', 'SSN', 'BANK_ACCOUNT_NUMBER',
    'GITHUB_BRANCH', 'GITHUB_COMMIT', 'GITHUB_TAG', 'GITHUB_RELEASE', 'GITHUB_ISSUE',
}

def find_word_start(text: str, pos: int) -> int:
    """Find the start of the word containing position pos."""
    # Move backward to find word start
    while pos > 0 and (text[pos - 1].isalnum() or text[pos - 1] == '_'):
        pos -= 1
    return pos

def find_word_end(text: str, pos: int) -> int:
    """Find the end of the word containing position pos."""
    # Move forward to find word end
    while pos < len(text) and (text[pos].isalnum() or text[pos] == '_'):
        pos += 1
    return pos

def find_pattern_in_text(text: str, pattern: re.Pattern, near_start: int, near_end: int) -> Tuple[int, int, bool]:
    """Find pattern match near the given position."""
    # Search in wider area
    search_start = max(0, near_start - 100)
    search_end = min(len(text), near_end + 100)
    search_text = text[search_start:search_end]
    offset = search_start
    
    best_match = None
    best_distance = float('inf')
    
    for match in pattern.finditer(search_text):
        match_start = offset + match.start()
        match_end = offset + match.end()
        
        # Calculate distance from original position
        distance = abs(match_start - near_start) + abs(match_end - near_end)
        
        if distance < best_distance:
            best_distance = distance
            best_match = (match_start, match_end)
    
    if best_match and best_distance < 50:
        return best_match[0], best_match[1], True
    
    return near_start, near_end, False

def fix_entity_aggressive(text: str, start: int, end: int, label: str) -> Tuple[int, int, bool]:
    """Aggressively fix entity boundaries."""
    entity_text = text[start:end]
    
    # 1. Trim whitespace
    entity_text = entity_text.strip()
    if entity_text != text[start:end]:
        # Adjust boundaries
        while start < end and text[start].isspace():
            start += 1
        while end > start and text[end - 1].isspace():
            end -= 1
        if start >= end:
            return start, end, False
        entity_text = text[start:end]
    
    # 2. Check if too short
    if len(entity_text) < 2 and label not in ['IP_ADDRESS', 'DOMAIN', 'CVE_ID', 'EMAIL', 'PHONE_NUMBER', 'GITHUB_ISSUE']:
        return start, end, False
    
    # 3. Check for common words
    if entity_text.lower() in COMMON_WORDS_NEVER and label in PROBLEMATIC_LABELS:
        return start, end, False
    
    # 4. For pattern-based entities, find correct boundary
    if label in VALID_PATTERNS:
        pattern = VALID_PATTERNS[label]
        new_start, new_end, found = find_pattern_in_text(text, pattern, start, end)
        if found:
            # Validate the found match
            match_text = text[new_start:new_end]
            if pattern.fullmatch(match_text):
                return new_start, new_end, True
        else:
            # If pattern not found, check if current text matches
            if not pattern.fullmatch(entity_text):
                return start, end, False
    
    # 5. Fix partial word boundaries for non-pattern entities
    if label not in VALID_PATTERNS:
        # Check if we're in the middle of a word
        if start > 0 and (text[start - 1].isalnum() or text[start - 1] == '_'):
            # We're in the middle of a word, try to find word start
            word_start = find_word_start(text, start)
            # Only extend if it's reasonable (not too far)
            if abs(word_start - start) <= 10:
                start = word_start
        
        if end < len(text) and (text[end].isalnum() or text[end] == '_'):
            # We're in the middle of a word, try to find word end
            word_end = find_word_end(text, end)
            # Only extend if it's reasonable (not too far)
            if abs(word_end - end) <= 10:
                end = word_end
    
    # 6. Final validation
    entity_text = text[start:end].strip()
    if len(entity_text) == 0:
        return start, end, False
    
    # Check for punctuation-only
    if all(c in '.,;:!?()[]{}\'"' for c in entity_text):
        return start, end, False
    
    # Check boundary validity
    if start < 0 or end > len(text) or start >= end:
        return start, end, False
    
    return start, end, True

def fix_file_aggressive(file_path: Path) -> Dict:
    """Aggressively fix all issues in a file."""
    backup_path = file_path.with_suffix(file_path.suffix + f'.backup_aggressive_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    shutil.copy2(file_path, backup_path)
    
    results = {
        'file': str(file_path),
        'total_examples': 0,
        'entities_before': 0,
        'entities_after': 0,
        'fixed': 0,
        'removed': 0,
    }
    
    fixed_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            
            try:
                data = json.loads(line)
                text = data.get('text', '')
                entities = data.get('entities', [])
                
                results['total_examples'] += 1
                results['entities_before'] += len(entities)
                
                fixed_entities = []
                
                for start, end, label in entities:
                    new_start, new_end, should_keep = fix_entity_aggressive(text, start, end, label)
                    
                    if should_keep:
                        fixed_entities.append([new_start, new_end, label])
                        if (new_start, new_end) != (start, end):
                            results['fixed'] += 1
                    else:
                        results['removed'] += 1
                
                # Remove duplicates and overlapping
                # Sort by start position
                fixed_entities.sort(key=lambda x: (x[0], x[1]))
                
        # Remove overlapping entities (keep the first one)
                unique_entities = []
                seen_spans = set()
                for ent in fixed_entities:
                    span = (ent[0], ent[1])
                    if span not in seen_spans:
                        # Check for overlap
                        overlap = False
                        for seen_start, seen_end in seen_spans:
                            if not (ent[1] <= seen_start or ent[0] >= seen_end):
                                overlap = True
                                break
                        if not overlap:
                            seen_spans.add(span)
                            unique_entities.append(ent)
                
                fixed_data.append({
                    'text': text,
                    'entities': unique_entities
                })
                
                results['entities_after'] += len(unique_entities)
                
            except Exception as e:
                pass
    
    # Write fixed data
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in fixed_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return results

def main():
    """Main function."""
    base_dir = Path('cyber-train/entities-intent')
    if not base_dir.exists():
        base_dir = Path('entities-intent')
    
    entity_files = list(base_dir.rglob('*_entities.jsonl'))
    
    print("="*80)
    print("AGGRESSIVE FIX FOR REMAINING ISSUES")
    print("="*80)
    print(f"\nFound {len(entity_files)} entity files\n")
    
    # Focus on worst performing files first
    results_list = []
    for file_path in sorted(entity_files):
        print(f"Fixing: {file_path.name}...", end=' ', flush=True)
        result = fix_file_aggressive(file_path)
        results_list.append(result)
        print(f"✅ Fixed {result['fixed']} boundaries, removed {result['removed']} invalid")
        print(f"   Entities: {result['entities_before']} → {result['entities_after']}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    total_fixed = sum(r['fixed'] for r in results_list)
    total_removed = sum(r['removed'] for r in results_list)
    total_before = sum(r['entities_before'] for r in results_list)
    total_after = sum(r['entities_after'] for r in results_list)
    
    print(f"\nTotal boundaries fixed: {total_fixed:,}")
    print(f"Total invalid entities removed: {total_removed:,}")
    print(f"Total entities: {total_before:,} → {total_after:,}")
    print(f"Reduction: {total_before - total_after:,} entities")

if __name__ == '__main__':
    main()

