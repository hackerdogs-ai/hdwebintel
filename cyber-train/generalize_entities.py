#!/usr/bin/env python3
"""
Generalize entities to avoid overfitting:
1. Consolidate social media usernames to SOCIAL_USER_NAME
2. Consolidate social media URLs to SOCIAL_MEDIA_URL
3. Remove product-centric entities (GitHub, Slack, etc.)
4. Fix overlapping entities
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from typing import List, Dict, Set, Tuple

# Social media entities to consolidate
SOCIAL_MEDIA_USERNAMES = {
    'INSTAGRAM_USERNAME',
    'FACEBOOK_USERNAME',
    'LINKEDIN_USERNAME',
    'TELEGRAM_USERNAME',
    'DISCORD_USERNAME',
    'SLACK_USERNAME',
    'WHATSAPP_USERNAME',
    'TWITTER_USERNAME',
    'TIKTOK_USERNAME',
    'YOUTUBE_USERNAME',
}

SOCIAL_MEDIA_URLS = {
    'INSTAGRAM_URL',
    'FACEBOOK_URL',
    'LINKEDIN_URL',
    'TELEGRAM_URL',
    'DISCORD_URL',
    'SLACK_URL',
    'WHATSAPP_URL',
    'TWITTER_URL',
    'TIKTOK_URL',
    'YOUTUBE_URL',
    'REDDIT_URL',
    'SNAPCHAT_URL',
}

# Product-centric entities to remove or generalize
PRODUCT_CENTRIC_TO_REMOVE = {
    'GITHUB_USER',  # Remove - too specific, causes overfitting
    'GITHUB_ORGANIZATION',  # Remove
    'SLACK_USERNAME',  # Already in SOCIAL_MEDIA_USERNAMES
    'DISCORD_USERNAME',  # Already in SOCIAL_MEDIA_USERNAMES
}

# Product-centric entities to keep but generalize
PRODUCT_CENTRIC_TO_GENERALIZE = {
    'GITHUB_REPO': 'REPOSITORY',  # Generalize to REPOSITORY
    'GITHUB_REPO_URL': 'REPOSITORY_URL',  # Generalize to REPOSITORY_URL
    'GITHUB_GIST': 'CODE_SNIPPET',  # Generalize to CODE_SNIPPET
    'GITHUB_ISSUE': 'ISSUE_ID',  # Generalize to ISSUE_ID
    'GITHUB_PULL_REQUEST': 'PULL_REQUEST_ID',  # Generalize to PULL_REQUEST_ID
    'GITHUB_COMMIT': 'COMMIT_HASH',  # Generalize to COMMIT_HASH
    'GITHUB_BRANCH': 'BRANCH_NAME',  # Generalize to BRANCH_NAME
    'GITHUB_TAG': 'VERSION_TAG',  # Generalize to VERSION_TAG
    'GITHUB_RELEASE': 'RELEASE_VERSION',  # Generalize to RELEASE_VERSION
}

# Statistics
stats = {
    'files_processed': 0,
    'lines_processed': 0,
    'social_username_consolidated': 0,
    'social_url_consolidated': 0,
    'product_centric_removed': 0,
    'product_centric_generalized': 0,
    'overlaps_resolved': 0,
}

def consolidate_entities(entities: List[List], text: str) -> List[List]:
    """Consolidate and fix entities."""
    if not entities:
        return entities
    
    # Track used spans to avoid overlaps
    used_spans = set()
    consolidated = []
    
    for start, end, label in entities:
        span = (start, end)
        
        # Skip if span already used
        if span in used_spans:
            stats['overlaps_resolved'] += 1
            continue
        
        # Remove product-centric entities
        if label in PRODUCT_CENTRIC_TO_REMOVE:
            stats['product_centric_removed'] += 1
            continue
        
        # Generalize product-centric entities
        if label in PRODUCT_CENTRIC_TO_GENERALIZE:
            new_label = PRODUCT_CENTRIC_TO_GENERALIZE[label]
            consolidated.append([start, end, new_label])
            used_spans.add(span)
            stats['product_centric_generalized'] += 1
            continue
        
        # Consolidate social media usernames
        if label in SOCIAL_MEDIA_USERNAMES:
            consolidated.append([start, end, 'SOCIAL_USER_NAME'])
            used_spans.add(span)
            stats['social_username_consolidated'] += 1
            continue
        
        # Consolidate social media URLs
        if label in SOCIAL_MEDIA_URLS:
            consolidated.append([start, end, 'SOCIAL_MEDIA_URL'])
            used_spans.add(span)
            stats['social_url_consolidated'] += 1
            continue
        
        # Keep other entities as-is
        consolidated.append([start, end, label])
        used_spans.add(span)
    
    # Sort by start position
    consolidated.sort(key=lambda x: x[0])
    
    return consolidated

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
                
                entities = data.get('entities', [])
                if entities:
                    consolidated_entities = consolidate_entities(entities, data.get('text', ''))
                    data['entities'] = consolidated_entities
                
                lines.append(json.dumps(data, ensure_ascii=False) + '\n')
            except json.JSONDecodeError:
                lines.append(line)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    stats['files_processed'] += 1

def update_entity_types_file():
    """Update entity_types.txt to reflect changes."""
    entity_types_file = Path('entity_types.txt')
    if not entity_types_file.exists():
        return
    
    # Read existing types
    with open(entity_types_file, 'r') as f:
        types = set(line.strip() for line in f if line.strip())
    
    # Remove product-centric types
    types -= PRODUCT_CENTRIC_TO_REMOVE
    types -= SOCIAL_MEDIA_USERNAMES
    types -= SOCIAL_MEDIA_URLS
    
    # Add generalized types
    types.add('SOCIAL_USER_NAME')
    types.add('SOCIAL_MEDIA_URL')
    types.update(PRODUCT_CENTRIC_TO_GENERALIZE.values())
    
    # Write back
    with open(entity_types_file, 'w') as f:
        for entity_type in sorted(types):
            f.write(f"{entity_type}\n")
    
    print(f"\n✅ Updated entity_types.txt")
    print(f"   Removed: {len(PRODUCT_CENTRIC_TO_REMOVE) + len(SOCIAL_MEDIA_USERNAMES) + len(SOCIAL_MEDIA_URLS)} types")
    print(f"   Added: {len(PRODUCT_CENTRIC_TO_GENERALIZE) + 2} generalized types")

def main():
    """Main function."""
    print("="*80)
    print("GENERALIZING ENTITIES TO AVOID OVERFITTING")
    print("="*80)
    
    # Find all entity files
    entity_files = list(Path('entities-intent').rglob('*_entities.jsonl'))
    entity_files = [f for f in entity_files if not f.name.endswith('.backup')]
    
    print(f"\nFound {len(entity_files)} entity files to process")
    print(f"\nConsolidating:")
    print(f"  - Social media usernames → SOCIAL_USER_NAME")
    print(f"  - Social media URLs → SOCIAL_MEDIA_URL")
    print(f"  - Removing: {PRODUCT_CENTRIC_TO_REMOVE}")
    print(f"  - Generalizing: {PRODUCT_CENTRIC_TO_GENERALIZE}")
    
    # Process each file
    for file_path in entity_files:
        try:
            process_file(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Update entity_types.txt
    update_entity_types_file()
    
    # Print statistics
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Files processed: {stats['files_processed']}")
    print(f"Lines processed: {stats['lines_processed']}")
    print(f"Social usernames consolidated: {stats['social_username_consolidated']}")
    print(f"Social URLs consolidated: {stats['social_url_consolidated']}")
    print(f"Product-centric removed: {stats['product_centric_removed']}")
    print(f"Product-centric generalized: {stats['product_centric_generalized']}")
    print(f"Overlaps resolved: {stats['overlaps_resolved']}")
    print("="*80)

if __name__ == '__main__':
    main()

