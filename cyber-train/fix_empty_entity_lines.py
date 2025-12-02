#!/usr/bin/env python3
"""
Fix lines with no entities by adding legitimate entities where appropriate.
Some lines are intentionally negative examples, but we should add entities where they exist.
"""

import json
import re
from pathlib import Path
from typing import List

# Patterns
PERCENTAGE_PATTERN = re.compile(r'\d+%')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?1?[-.\s(]?\(?\d{3}\)?[-.\s)]?\d{3}[-.\s]?\d{4}\b')
IP_PATTERN = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
GITHUB_REPO_PATTERN = re.compile(r'\b[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+')
GITHUB_URL_PATTERN = re.compile(r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)*')

def extract_entities_from_text(text: str) -> List[List]:
    """Extract entities that should be labeled."""
    entities = []
    
    # Percentages (only if in context suggesting metrics)
    if any(word in text.lower() for word in ['rate', 'percentage', 'threshold', 'metric', 'coverage', 'score', 'pass', 'fail']):
        for match in PERCENTAGE_PATTERN.finditer(text):
            entities.append([match.start(), match.end(), 'PERCENTAGE'])
    
    # CVE IDs
    for match in CVE_PATTERN.finditer(text):
        entities.append([match.start(), match.end(), 'CVE_ID'])
    
    # Email addresses
    for match in EMAIL_PATTERN.finditer(text):
        entities.append([match.start(), match.end(), 'EMAIL_ADDRESS'])
    
    # Phone numbers (with context)
    for match in PHONE_PATTERN.finditer(text):
        context_start = max(0, match.start() - 30)
        context_end = min(len(text), match.end() + 30)
        context = text[context_start:context_end].lower()
        if any(word in context for word in ['phone', 'call', 'contact', 'number', 'tel', 'mobile']):
            entities.append([match.start(), match.end(), 'PHONE_NUMBER'])
    
    # IP addresses (with context)
    for match in IP_PATTERN.finditer(text):
        context_start = max(0, match.start() - 40)
        context_end = min(len(text), match.end() + 40)
        context = text[context_start:context_end].lower()
        if any(word in context for word in ['ip', 'address', 'host', 'server', 'attacker', 'source', 'destination', 'from', 'to']):
            entities.append([match.start(), match.end(), 'IP_ADDRESS'])
    
    # URLs
    for match in URL_PATTERN.finditer(text):
        url_text = match.group()
        if 'github.com' in url_text:
            entities.append([match.start(), match.end(), 'GITHUB_REPO_URL'])
        else:
            entities.append([match.start(), match.end(), 'URL'])
    
    # GitHub repos (not part of URL)
    for match in GITHUB_REPO_PATTERN.finditer(text):
        if not (match.start() > 0 and text[match.start()-1] in ':/'):
            entities.append([match.start(), match.end(), 'GITHUB_REPO'])
    
    # Threshold mentions
    threshold_idx = text.lower().find('threshold')
    if threshold_idx != -1:
        entities.append([threshold_idx, threshold_idx + 9, 'THRESHOLD_TYPE'])
    
    # Metric mentions (if percentage present)
    if any(match for match in PERCENTAGE_PATTERN.finditer(text)):
        metric_words = ['rate', 'coverage', 'score', 'accuracy', 'precision', 'recall', 'f1', 'metric']
        for word in metric_words:
            idx = text.lower().find(word)
            if idx != -1:
                entities.append([idx, idx + len(word), 'METRIC_TYPE'])
                break
    
    # Remove duplicates and overlapping
    seen = set()
    unique_entities = []
    for ent in sorted(entities, key=lambda x: (x[0], x[1])):
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
    
    return unique_entities

def process_file(file_path: Path):
    """Process file and add entities to lines that should have them."""
    fixed_data = []
    added_count = 0
    
    with open(file_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            
            data = json.loads(line)
            text = data.get('text', '')
            existing_entities = data.get('entities', [])
            
            # If no entities, try to extract them
            if not existing_entities:
                new_entities = extract_entities_from_text(text)
                if new_entities:
                    existing_entities = new_entities
                    added_count += len(new_entities)
            
            fixed_data.append({
                'text': text,
                'entities': existing_entities
            })
    
    # Write back
    with open(file_path, 'w') as f:
        for item in fixed_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return added_count

def main():
    base_dir = Path('cyber-train/entities-intent')
    entity_files = list(base_dir.rglob('*_entities.jsonl'))
    
    print("="*80)
    print("FIXING LINES WITH NO ENTITIES")
    print("="*80)
    
    total_added = 0
    for file_path in sorted(entity_files):
        added = process_file(file_path)
        if added > 0:
            print(f"{file_path.name}: Added {added} entities to empty lines")
            total_added += added
    
    print(f"\n✅ Total entities added: {total_added}")

if __name__ == '__main__':
    main()

