#!/usr/bin/env python3
"""
Conservative fix - ONLY fixes clearly wrong issues without being aggressive.
Line by line, precise fixes only.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
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

def fix_entity_conservative(text: str, start: int, end: int, label: str) -> Tuple[int, int, bool]:
    """
    ULTRA CONSERVATIVE fix - ONLY fixes clearly wrong issues:
    1. Whitespace trimming (ONLY if entity becomes empty)
    2. Common words incorrectly labeled (ONLY if clearly wrong)
    3. Pattern-based entities that don't match (try to find correct boundary, but KEEP if not found)
    DOES NOT REMOVE ENTITIES unless they are clearly invalid (empty, punctuation-only, or common words)
    """
    entity_text = text[start:end]
    original_start, original_end = start, end
    
    # 1. Fix whitespace (trim only if it makes entity empty)
    stripped = entity_text.strip()
    if stripped != entity_text:
        # Adjust boundaries to remove whitespace
        new_start = start
        new_end = end
        while new_start < new_end and text[new_start].isspace():
            new_start += 1
        while new_end > new_start and text[new_end - 1].isspace():
            new_end -= 1
        if new_start < new_end:
            start, end = new_start, new_end
            entity_text = text[start:end]
        else:
            # Entity is only whitespace
            return start, end, False
    
    # 2. Check if empty
    if len(entity_text.strip()) == 0:
        return start, end, False
    
    # 3. Check for punctuation-only
    if all(c in '.,;:!?()[]{}\'"' for c in entity_text.strip()):
        return start, end, False
    
    # 4. Check for common words incorrectly labeled (ONLY if clearly wrong)
    if entity_text.lower().strip() in COMMON_WORDS_NEVER and label in PROBLEMATIC_LABELS:
        # Only remove if it's a single common word, not part of a phrase
        if len(entity_text.strip().split()) == 1:
            return start, end, False
    
    # 5. For pattern-based entities: try to fix boundaries, but KEEP if can't find match
    if label in VALID_PATTERNS:
        pattern = VALID_PATTERNS[label]
        
        # Check if current text matches pattern
        if not pattern.fullmatch(entity_text):
            # Try to find correct boundary nearby (within 50 chars)
            search_start = max(0, original_start - 50)
            search_end = min(len(text), original_end + 50)
            search_text = text[search_start:search_end]
            offset = search_start
            
            best_match = None
            best_distance = float('inf')
            
            for match in pattern.finditer(search_text):
                match_start = offset + match.start()
                match_end = offset + match.end()
                
                # Calculate distance from original position
                distance = abs(match_start - original_start) + abs(match_end - original_end)
                
                # Prefer matches that overlap or are very close
                if (match_start <= original_end and match_end >= original_start) or distance < 30:
                    if distance < best_distance:
                        best_distance = distance
                        best_match = (match_start, match_end)
            
            if best_match:
                # Found correct boundary - use it
                return best_match[0], best_match[1], True
            # If pattern not found, KEEP the entity anyway (don't remove)
    
    # 6. For non-pattern entities: KEEP them as-is
    # Only validate that boundaries are reasonable
    if start < 0 or end > len(text) or start >= end:
        return start, end, False
    
    # 7. Final validation - KEEP entity if it has any content
    if len(entity_text.strip()) > 0:
        return start, end, True
    
    return start, end, False

def fix_file_conservative(file_path: Path) -> Dict:
    """Conservative fix for a file - line by line."""
    backup_path = file_path.with_suffix(file_path.suffix + f'.backup_conservative_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
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
                    new_start, new_end, should_keep = fix_entity_conservative(text, start, end, label)
                    
                    if should_keep:
                        fixed_entities.append([new_start, new_end, label])
                        if (new_start, new_end) != (start, end):
                            results['fixed'] += 1
                    else:
                        results['removed'] += 1
                
                # Remove duplicates (keep first occurrence)
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
                
            except Exception as e:
                print(f"Error in {file_path.name} line {line_num}: {e}")
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
    print("CONSERVATIVE FIX - LINE BY LINE")
    print("="*80)
    print(f"\nFound {len(entity_files)} entity files\n")
    
    results_list = []
    for file_path in sorted(entity_files):
        print(f"Fixing: {file_path.name}...", end=' ', flush=True)
        result = fix_file_conservative(file_path)
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

