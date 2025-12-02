#!/usr/bin/env python3
"""
FINAL PROPER FIX: 
1. Restore from best backup (with most entities)
2. Fix boundaries WITHOUT removing entities
3. Add ONLY clearly missing legitimate entities
4. NEVER remove valid entities
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Set
import shutil
from datetime import datetime
import glob

# Strict patterns - only match when confident
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?1?[-.\s(]?\(?\d{3}\)?[-.\s)]?\d{3}[-.\s]?\d{4}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
GITHUB_REPO_PATTERN = re.compile(r'\b[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+')
GITHUB_URL_PATTERN = re.compile(r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)*')
GITHUB_USER_PATTERN = re.compile(r'@[a-zA-Z0-9]([a-zA-Z0-9]|-(?![.-])){0,38}')
GITHUB_COMMIT_PATTERN = re.compile(r'\b[a-f0-9]{7,40}\b')
IP_PATTERN = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
IPV6_PATTERN = re.compile(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b')

THREAT_ACTORS = {
    'APT29', 'APT28', 'APT41', 'Lazarus', 'FIN7', 'UNC2452', 'Wizard Spider',
    'Ryuk', 'Conti', 'Maze', 'REvil', 'LockBit', 'DarkSide', 'DoppelPaymer',
    'Ragnar Locker', 'Egregor', 'Mespinoza', 'ALPHV', 'BlackCat', 'Cozy Bear',
    'Fancy Bear', 'Equation Group', 'Sandworm', 'Turla',
}

def find_best_backup(file_path: Path) -> Path:
    """Find backup with most entities."""
    backups = list(file_path.parent.glob(f"{file_path.stem}.backup*"))
    if not backups:
        return None
    
    best_backup = None
    max_entities = 0
    
    for backup in backups:
        try:
            with open(backup, 'r') as f:
                count = 0
                for line in f:
                    if line.strip():
                        try:
                            data = json.loads(line)
                            count += len(data.get('entities', []))
                        except:
                            pass
            if count > max_entities:
                max_entities = count
                best_backup = backup
        except:
            continue
    
    return best_backup

def fix_entity_boundary_conservative(text: str, start: int, end: int, label: str) -> Tuple[int, int]:
    """Fix boundary conservatively - ONLY trim whitespace, don't extend."""
    original_start, original_end = start, end
    
    # ONLY trim whitespace - don't extend
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    
    # If trimming whitespace made it invalid, revert
    if start >= end:
        return original_start, original_end
    
    return start, end

def extract_legitimate_entities(text: str, existing_spans: Set[Tuple[int, int]]) -> List[List]:
    """Extract ONLY clearly legitimate entities."""
    found = []
    
    # CVE IDs
    for match in CVE_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            found.append([match.start(), match.end(), 'CVE_ID'])
            existing_spans.add(span)
    
    # Email addresses
    for match in EMAIL_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            found.append([match.start(), match.end(), 'EMAIL_ADDRESS'])
            existing_spans.add(span)
    
    # Phone numbers (with context check)
    for match in PHONE_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            context_start = max(0, match.start() - 30)
            context_end = min(len(text), match.end() + 30)
            context = text[context_start:context_end].lower()
            if any(word in context for word in ['phone', 'call', 'contact', 'number', 'tel', 'mobile', 'cell']):
                found.append([match.start(), match.end(), 'PHONE_NUMBER'])
                existing_spans.add(span)
    
    # Wallet addresses
    for match in WALLET_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            found.append([match.start(), match.end(), 'WALLET_ADDRESS'])
            existing_spans.add(span)
    
    # URLs
    for match in URL_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            url_text = match.group()
            if 'github.com' in url_text:
                found.append([match.start(), match.end(), 'GITHUB_REPO_URL'])
            else:
                found.append([match.start(), match.end(), 'URL'])
            existing_spans.add(span)
    
    # GitHub repos (not part of URL)
    for match in GITHUB_REPO_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            # Check it's not part of a URL
            if not (span[0] > 0 and text[span[0]-1] in ':/'):
                found.append([match.start(), match.end(), 'GITHUB_REPO'])
                existing_spans.add(span)
    
    # GitHub users
    for match in GITHUB_USER_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            found.append([match.start(), match.end(), 'GITHUB_USER'])
            existing_spans.add(span)
    
    # GitHub commits (with context)
    for match in GITHUB_COMMIT_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            context_start = max(0, match.start() - 40)
            context_end = min(len(text), match.end() + 40)
            context = text[context_start:context_end].lower()
            if any(word in context for word in ['commit', 'hash', 'sha', 'git', 'repository', 'repo']):
                found.append([match.start(), match.end(), 'GITHUB_COMMIT'])
                existing_spans.add(span)
    
    # IP addresses (with context)
    for match in IP_PATTERN.finditer(text):
        span = (match.start(), match.end())
        if span not in existing_spans:
            context_start = max(0, match.start() - 40)
            context_end = min(len(text), match.end() + 40)
            context = text[context_start:context_end].lower()
            if any(word in context for word in ['ip', 'address', 'host', 'server', 'attacker', 'source', 'destination', 'from', 'to']):
                found.append([match.start(), match.end(), 'IP_ADDRESS'])
                existing_spans.add(span)
    
    # Threat actors (exact word matches)
    text_upper = text.upper()
    for actor in THREAT_ACTORS:
        actor_upper = actor.upper()
        idx = 0
        while True:
            idx = text_upper.find(actor_upper, idx)
            if idx == -1:
                break
            end_idx = idx + len(actor)
            span = (idx, end_idx)
            if span not in existing_spans:
                # Word boundary check
                if (idx == 0 or not text[idx-1].isalnum()) and \
                   (end_idx >= len(text) or not text[end_idx].isalnum()):
                    found.append([idx, end_idx, 'THREAT_ACTOR'])
                    existing_spans.add(span)
            idx = end_idx
    
    return found

def process_file(file_path: Path) -> Dict:
    """Process file: restore, fix boundaries conservatively, add legitimate entities."""
    # Find best backup
    best_backup = find_best_backup(file_path)
    
    if best_backup:
        print(f"  Restoring from {best_backup.name}...")
        shutil.copy2(best_backup, file_path)
    
    # Create backup
    backup_path = file_path.with_suffix(file_path.suffix + f'.backup_final_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
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
                
                # Fix boundaries conservatively (ONLY trim whitespace)
                fixed_entities = []
                existing_spans = set()
                
                for start, end, label in entities:
                    new_start, new_end = fix_entity_boundary_conservative(text, start, end, label)
                    fixed_entities.append([new_start, new_end, label])
                    existing_spans.add((new_start, new_end))
                    if (new_start, new_end) != (start, end):
                        results['boundaries_fixed'] += 1
                
                # Add ONLY legitimate missing entities
                missing_entities = extract_legitimate_entities(text, existing_spans)
                fixed_entities.extend(missing_entities)
                results['entities_added'] += len(missing_entities)
                
                # Remove duplicates (keep first)
                seen = set()
                unique_entities = []
                for ent in sorted(fixed_entities, key=lambda x: (x[0], x[1])):
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
                print(f"    ERROR: {e}")
                continue
    
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
    print("FINAL PROPER FIX: RESTORE + CONSERVATIVE BOUNDARY FIX + ADD LEGITIMATE ENTITIES")
    print("="*80)
    print(f"\nFound {len(entity_files)} entity files\n")
    
    results_list = []
    for file_path in sorted(entity_files):
        print(f"Processing: {file_path.name}...")
        result = process_file(file_path)
        results_list.append(result)
        change = result['entities_after'] - result['entities_before']
        print(f"  ✅ Fixed {result['boundaries_fixed']} boundaries, added {result['entities_added']} entities")
        print(f"     Entities: {result['entities_before']} → {result['entities_after']} ({change:+d})\n")
    
    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    total_before = sum(r['entities_before'] for r in results_list)
    total_after = sum(r['entities_after'] for r in results_list)
    total_fixed = sum(r['boundaries_fixed'] for r in results_list)
    total_added = sum(r['entities_added'] for r in results_list)
    
    print(f"\nTotal boundaries fixed: {total_fixed:,}")
    print(f"Total legitimate entities added: {total_added:,}")
    print(f"Total entities: {total_before:,} → {total_after:,}")
    print(f"Net change: {total_after - total_before:+,} entities")

if __name__ == '__main__':
    main()

