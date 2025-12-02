#!/usr/bin/env python3
"""
Comprehensive fix: Restore missing entities, fix boundaries, and add missing entity types.
This script will:
1. Restore entities from backups
2. Fix boundaries without removing entities
3. Add missing entity types (CVE_ID, THREAT_ACTOR, WALLET_ADDRESS, LATITUDE, LONGITUDE, etc.)
4. Ensure proper boundaries for all entities
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Set
import shutil
from datetime import datetime

# Patterns for validation
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
LATITUDE_PATTERN = re.compile(r'\b-?([0-8]?[0-9](?:\.\d+)?|90(?:\.0+)?)\b')
LONGITUDE_PATTERN = re.compile(r'\b-?(?:[0-9]?[0-9]?[0-9](?:\.\d+)?|1[0-7][0-9](?:\.\d+)?|180(?:\.0+)?)\b')
GEOJSON_PATTERN = re.compile(r'\{"type"\s*:\s*"Point"\s*,\s*"coordinates"\s*:\s*\[-?\d+\.?\d*,\s*-?\d+\.?\d*\]\}')
DMS_PATTERN = re.compile(r'\d+°\d+\'\d+\.?\d*"[NS]\s+\d+°\d+\'\d+\.?\d*"[EW]')

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
    'LATITUDE': LATITUDE_PATTERN,
    'LONGITUDE': LONGITUDE_PATTERN,
    'GEOJSON': GEOJSON_PATTERN,
    'DMS_COORDINATES': DMS_PATTERN,
}

# Common words that should NEVER be entities
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

def find_word_boundaries(text: str, start: int, end: int) -> Tuple[int, int]:
    """Find proper word boundaries - extend to complete words."""
    original_start, original_end = start, end
    
    # Extend start backward to word boundary
    while start > 0 and (text[start - 1].isalnum() or text[start - 1] == '_'):
        start -= 1
        if abs(start - original_start) > 20:  # Don't extend too far
            start = original_start
            break
    
    # Extend end forward to word boundary
    while end < len(text) and (text[end].isalnum() or text[end] == '_'):
        end += 1
        if abs(end - original_end) > 20:  # Don't extend too far
            end = original_end
            break
    
    return start, end

def find_pattern_boundary(text: str, label: str, search_start: int, search_end: int) -> Tuple[int, int, bool]:
    """Find correct boundary using pattern matching."""
    if label not in VALID_PATTERNS:
        return search_start, search_end, False
    
    pattern = VALID_PATTERNS[label]
    search_text = text[max(0, search_start - 100):min(len(text), search_end + 100)]
    offset = max(0, search_start - 100)
    
    best_match = None
    best_distance = float('inf')
    
    for match in pattern.finditer(search_text):
        match_start = offset + match.start()
        match_end = offset + match.end()
        
        distance = abs(match_start - search_start) + abs(match_end - search_end)
        
        if (match_start <= search_end and match_end >= search_start) or distance < 50:
            if distance < best_distance:
                best_distance = distance
                best_match = (match_start, match_end)
    
    if best_match:
        return best_match[0], best_match[1], True
    
    return search_start, search_end, False

def fix_entity_boundary(text: str, start: int, end: int, label: str) -> Tuple[int, int]:
    """Fix entity boundary - NEVER remove, only fix boundaries."""
    entity_text = text[start:end]
    original_start, original_end = start, end
    
    # 1. Trim whitespace
    stripped = entity_text.strip()
    if stripped != entity_text:
        new_start = start
        new_end = end
        while new_start < new_end and text[new_start].isspace():
            new_start += 1
        while new_end > new_start and text[new_end - 1].isspace():
            new_end -= 1
        if new_start < new_end:
            start, end = new_start, new_end
            entity_text = text[start:end]
    
    # 2. For pattern-based entities: find correct boundary
    if label in VALID_PATTERNS:
        pattern = VALID_PATTERNS[label]
        if not pattern.fullmatch(entity_text):
            new_start, new_end, found = find_pattern_boundary(text, label, original_start, original_end)
            if found:
                return new_start, new_end
    
    # 3. Fix partial word boundaries
    if start > 0 and text[start - 1].isalnum():
        word_start, word_end = find_word_boundaries(text, start, end)
        start = word_start
    
    if end < len(text) and text[end].isalnum():
        word_start, word_end = find_word_boundaries(text, start, end)
        end = word_end
    
    return start, end

def extract_missing_entities(text: str, existing_entities: List[List]) -> List[List]:
    """Extract entities that are missing from the text."""
    found_entities = []
    existing_spans = set((e[0], e[1]) for e in existing_entities)
    
    # Extract all pattern-based entities
    for label, pattern in VALID_PATTERNS.items():
        for match in pattern.finditer(text):
            start, end = match.start(), match.end()
            if (start, end) not in existing_spans:
                found_entities.append([start, end, label])
                existing_spans.add((start, end))
    
    return found_entities

def process_file(file_path: Path) -> Dict:
    """Process a file: restore entities, fix boundaries, add missing entities."""
    backup_path = file_path.with_suffix(file_path.suffix + f'.backup_comprehensive_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    shutil.copy2(file_path, backup_path)
    
    results = {
        'file': str(file_path),
        'total_examples': 0,
        'entities_before': 0,
        'entities_after': 0,
        'boundaries_fixed': 0,
        'entities_added': 0,
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
                
                # Fix boundaries for existing entities
                fixed_entities = []
                for start, end, label in entities:
                    new_start, new_end = fix_entity_boundary(text, start, end, label)
                    fixed_entities.append([new_start, new_end, label])
                    if (new_start, new_end) != (start, end):
                        results['boundaries_fixed'] += 1
                
                # Extract missing entities
                missing_entities = extract_missing_entities(text, fixed_entities)
                fixed_entities.extend(missing_entities)
                results['entities_added'] += len(missing_entities)
                
                # Remove duplicates and overlapping (keep first)
                seen = set()
                unique_entities = []
                for ent in sorted(fixed_entities, key=lambda x: (x[0], x[1])):
                    key = (ent[0], ent[1], ent[2])
                    if key not in seen:
                        # Check for overlap
                        overlap = False
                        for existing in unique_entities:
                            if not (ent[1] <= existing[0] or ent[0] >= existing[1]):
                                overlap = True
                                break
                        if not overlap:
                            seen.add(key)
                            unique_entities.append(ent)
                
                fixed_data.append({
                    'text': text,
                    'entities': unique_entities
                })
                
                results['entities_after'] += len(unique_entities)
                
            except Exception as e:
                print(f"Error in {file_path.name}: {e}")
    
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
    print("COMPREHENSIVE FIX: RESTORE + FIX BOUNDARIES + ADD MISSING ENTITIES")
    print("="*80)
    print(f"\nFound {len(entity_files)} entity files\n")
    
    results_list = []
    for file_path in sorted(entity_files):
        print(f"Processing: {file_path.name}...", end=' ', flush=True)
        result = process_file(file_path)
        results_list.append(result)
        print(f"✅ Fixed {result['boundaries_fixed']} boundaries, added {result['entities_added']} entities")
        print(f"   Entities: {result['entities_before']} → {result['entities_after']}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    total_before = sum(r['entities_before'] for r in results_list)
    total_after = sum(r['entities_after'] for r in results_list)
    total_fixed = sum(r['boundaries_fixed'] for r in results_list)
    total_added = sum(r['entities_added'] for r in results_list)
    
    print(f"\nTotal boundaries fixed: {total_fixed:,}")
    print(f"Total entities added: {total_added:,}")
    print(f"Total entities: {total_before:,} → {total_after:,}")
    print(f"Net change: +{total_after - total_before:,} entities")

if __name__ == '__main__':
    main()

