#!/usr/bin/env python3
"""
Comprehensive fix for all quality issues identified in the audit.
Fixes entity boundaries, removes invalid entities, and binarizes intents.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
import shutil
from datetime import datetime
from collections import defaultdict

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
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b')
LATITUDE_PATTERN = re.compile(r'\b-?([0-8]?[0-9](?:\.\d+)?|90(?:\.0+)?)\b')
LONGITUDE_PATTERN = re.compile(r'\b-?(?:[0-9]?[0-9]?[0-9](?:\.\d+)?|1[0-7][0-9](?:\.\d+)?|180(?:\.0+)?)\b')
GEOJSON_PATTERN = re.compile(r'\{"type"\s*:\s*"Point"\s*,\s*"coordinates"\s*:\s*\[-?\d+\.?\d*,\s*-?\d+\.?\d*\]\}')
DMS_PATTERN = re.compile(r'\d+°\d+\'\d+\.?\d*"[NS]\s+\d+°\d+\'\d+\.?\d*"[EW]')
EMOJI_PATTERN = re.compile(r'[\U0001F300-\U0001F9FF\U0001FA00-\U0001FAFF\u2600-\u26FF\u2700-\u27BF]')

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
    'SSN': SSN_PATTERN,
    'CREDIT_CARD_NUMBER': CREDIT_CARD_PATTERN,
    'LATITUDE': LATITUDE_PATTERN,
    'LONGITUDE': LONGITUDE_PATTERN,
    'GEOJSON': GEOJSON_PATTERN,
    'DMS_COORDINATES': DMS_PATTERN,
    'EMOJI': EMOJI_PATTERN,
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

# Problematic labels for common words
PROBLEMATIC_LABELS = {
    'AI_MODEL_TYPE', 'SECURITY_TYPE', 'INCIDENT_TYPE', 'METRIC_TYPE', 'THRESHOLD_TYPE',
    'TOOL', 'TIME_UNIT', 'PRIORITIZATION_TYPE', 'SERVICE', 'SOURCE_TYPE',
    'ENCRYPTION_TYPE', 'VULNERABILITY_ID', 'TRAINING_TYPE', 'INTEGRATION_TYPE',
    'BRANCH', 'COMMIT', 'QUERY_TYPE', 'REQUIREMENT_TYPE', 'PERCENTAGE', 'COUNT',
    'PHONE_NUMBER', 'EMAIL_ADDRESS', 'CREDIT_CARD_NUMBER', 'SSN', 'BANK_ACCOUNT_NUMBER',
    'GITHUB_BRANCH', 'GITHUB_COMMIT', 'GITHUB_TAG', 'GITHUB_RELEASE', 'GITHUB_ISSUE',
}

def find_word_boundaries(text: str, start: int, end: int) -> Tuple[int, int]:
    """Find proper word boundaries for an entity - conservative approach."""
    original_start, original_end = start, end
    
    # Only extend if we're clearly in the middle of a word
    # Check start: if previous char is alnum, we might be in middle of word
    if start > 0 and text[start - 1].isalnum():
        # Find word start, but only extend if reasonable
        word_start = start
        while word_start > 0 and (text[word_start - 1].isalnum() or text[word_start - 1] == '_'):
            word_start -= 1
        # Only use if extension is small (<= 5 chars)
        if abs(word_start - start) <= 5:
            start = word_start
    
    # Check end: if next char is alnum, we might be in middle of word
    if end < len(text) and text[end].isalnum():
        # Find word end, but only extend if reasonable
        word_end = end
        while word_end < len(text) and (text[word_end].isalnum() or text[word_end] == '_'):
            word_end += 1
        # Only use if extension is small (<= 5 chars)
        if abs(word_end - end) <= 5:
            end = word_end
    
    return start, end

def find_pattern_boundary(text: str, label: str, search_start: int, search_end: int) -> Tuple[int, int, bool]:
    """Find correct boundary using pattern matching."""
    if label not in VALID_PATTERNS:
        return search_start, search_end, False
    
    pattern = VALID_PATTERNS[label]
    # Search in a wider area around the entity
    search_text = text[max(0, search_start - 50):min(len(text), search_end + 50)]
    offset = max(0, search_start - 50)
    
    for match in pattern.finditer(search_text):
        match_start = offset + match.start()
        match_end = offset + match.end()
        
        # Check if this match overlaps with or is near our entity
        if (match_start <= search_end and match_end >= search_start) or \
           (abs(match_start - search_start) < 10 and abs(match_end - search_end) < 10):
            return match_start, match_end, True
    
    return search_start, search_end, False

def fix_entity(text: str, start: int, end: int, label: str) -> Tuple[int, int, bool]:
    """Fix a single entity - returns (new_start, new_end, should_keep)."""
    entity_text = text[start:end]
    original_start, original_end = start, end
    
    # 1. Trim whitespace
    entity_text = entity_text.strip()
    if entity_text != text[start:end]:
        # Adjust boundaries to remove whitespace
        start += len(text[start:end]) - len(text[start:end].lstrip())
        end -= len(text[start:end]) - len(text[start:end].rstrip())
        entity_text = text[start:end].strip()
        if start >= end:
            return start, end, False
    
    # 2. Check if too short
    if len(entity_text) < 2 and label not in ['IP_ADDRESS', 'DOMAIN', 'CVE_ID', 'EMAIL', 'PHONE_NUMBER', 'GITHUB_ISSUE']:
        return start, end, False
    
    # 3. Check for common words incorrectly labeled
    if entity_text.lower() in COMMON_WORDS_NEVER and label in PROBLEMATIC_LABELS:
        return start, end, False
    
    # 4. Fix partial word boundaries (ONLY for pattern-based entities that don't match)
    # For pattern-based entities, use pattern matching
    if label in VALID_PATTERNS:
        pattern = VALID_PATTERNS[label]
        # Check if current text matches pattern
        if not pattern.fullmatch(entity_text):
            # Try to find correct boundary using pattern
            new_start, new_end, found = find_pattern_boundary(text, label, start, end)
            if found:
                start, end = new_start, new_end
            else:
                # Pattern not found, remove entity
                return start, end, False
    # For non-pattern entities, DON'T fix word boundaries automatically
    # Only trim whitespace and validate
    
    # 5. Validate pattern if applicable
    if label in VALID_PATTERNS:
        pattern = VALID_PATTERNS[label]
        entity_text = text[start:end]
        if not pattern.fullmatch(entity_text):
            # Try to find correct boundary
            new_start, new_end, found = find_pattern_boundary(text, label, original_start, original_end)
            if found:
                return new_start, new_end, True
            else:
                return start, end, False
    
    # 6. Final validation
    entity_text = text[start:end].strip()
    if len(entity_text) == 0:
        return start, end, False
    
    # Check for punctuation-only
    if all(c in '.,;:!?()[]{}\'"' for c in entity_text):
        return start, end, False
    
    return start, end, True

def fix_entity_file(file_path: Path) -> Dict:
    """Fix all issues in an entity file."""
    backup_path = file_path.with_suffix(file_path.suffix + f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    shutil.copy2(file_path, backup_path)
    
    results = {
        'file': str(file_path),
        'total_examples': 0,
        'entities_before': 0,
        'entities_after': 0,
        'fixed': 0,
        'removed': 0,
        'errors': []
    }
    
    fixed_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
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
                    new_start, new_end, should_keep = fix_entity(text, start, end, label)
                    
                    if should_keep:
                        fixed_entities.append([new_start, new_end, label])
                        if (new_start, new_end) != (start, end):
                            results['fixed'] += 1
                    else:
                        results['removed'] += 1
                
                # Remove duplicates
                seen = set()
                unique_entities = []
                for ent in fixed_entities:
                    key = (ent[0], ent[1], ent[2])
                    if key not in seen:
                        seen.add(key)
                        unique_entities.append(ent)
                
                fixed_data.append({
                    'text': text,
                    'entities': unique_entities
                })
                
                results['entities_after'] += len(unique_entities)
                
            except json.JSONDecodeError as e:
                results['errors'].append(f"Line {line_num}: {e}")
            except Exception as e:
                results['errors'].append(f"Line {line_num}: {e}")
    
    # Write fixed data
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in fixed_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return results

def fix_intent_file(file_path: Path) -> Dict:
    """Fix all issues in an intent file."""
    backup_path = file_path.with_suffix(file_path.suffix + f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    shutil.copy2(file_path, backup_path)
    
    results = {
        'file': str(file_path),
        'total_examples': 0,
        'fixed': 0,
        'errors': []
    }
    
    fixed_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            
            try:
                data = json.loads(line)
                text = data.get('text', '')
                # Handle both 'intents' and 'cats' (spaCy format)
                intents = data.get('intents', data.get('cats', {}))
                
                results['total_examples'] += 1
                
                # Binarize intent values
                fixed_intents = {}
                needs_fix = False
                
                for intent_name, intent_value in intents.items():
                    if isinstance(intent_value, (int, float)):
                        if intent_value >= 0.5:
                            fixed_intents[intent_name] = 1.0
                        else:
                            fixed_intents[intent_name] = 0.0
                        
                        if intent_value not in [0.0, 1.0, 0, 1]:
                            needs_fix = True
                    else:
                        # Invalid type, set to 0.0
                        fixed_intents[intent_name] = 0.0
                        needs_fix = True
                
                if needs_fix:
                    results['fixed'] += 1
                
                # Use 'intents' key (standardize on 'intents')
                fixed_data.append({
                    'text': text,
                    'intents': fixed_intents
                })
                
            except json.JSONDecodeError as e:
                results['errors'].append(f"Line {line_num}: {e}")
            except Exception as e:
                results['errors'].append(f"Line {line_num}: {e}")
    
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
    intent_files = list(base_dir.rglob('*_intent.jsonl'))
    
    print("="*80)
    print("FIXING ALL QUALITY ISSUES")
    print("="*80)
    print(f"\nFound {len(entity_files)} entity files and {len(intent_files)} intent files\n")
    
    # Fix entity files
    print("="*80)
    print("FIXING ENTITY FILES")
    print("="*80)
    entity_results = []
    for file_path in sorted(entity_files):
        print(f"Fixing: {file_path.name}...", end=' ', flush=True)
        result = fix_entity_file(file_path)
        entity_results.append(result)
        print(f"✅ Fixed {result['fixed']} boundaries, removed {result['removed']} invalid")
        print(f"   Entities: {result['entities_before']} → {result['entities_after']}")
    
    # Fix intent files
    print("\n" + "="*80)
    print("FIXING INTENT FILES")
    print("="*80)
    intent_results = []
    for file_path in sorted(intent_files):
        print(f"Fixing: {file_path.name}...", end=' ', flush=True)
        result = fix_intent_file(file_path)
        intent_results.append(result)
        print(f"✅ Fixed {result['fixed']} examples")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    total_entity_fixed = sum(r['fixed'] for r in entity_results)
    total_entity_removed = sum(r['removed'] for r in entity_results)
    total_entity_before = sum(r['entities_before'] for r in entity_results)
    total_entity_after = sum(r['entities_after'] for r in entity_results)
    
    total_intent_fixed = sum(r['fixed'] for r in intent_results)
    
    print(f"\nEntity Files:")
    print(f"  Boundaries fixed: {total_entity_fixed:,}")
    print(f"  Invalid entities removed: {total_entity_removed:,}")
    print(f"  Total entities: {total_entity_before:,} → {total_entity_after:,}")
    print(f"  Reduction: {total_entity_before - total_entity_after:,} entities")
    
    print(f"\nIntent Files:")
    print(f"  Examples fixed: {total_intent_fixed:,}")
    
    print(f"\n✅ All fixes complete! Backups created with timestamp.")

if __name__ == '__main__':
    main()

