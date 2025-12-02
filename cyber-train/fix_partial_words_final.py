#!/usr/bin/env python3
"""
Final fix for partial words and common words that slipped through.
This is the last pass to ensure 100% quality.
"""

import json
from pathlib import Path
from typing import List

# Extended common words list
COMMON_WORDS_NEVER_ENTITIES = {
    'ai', 'security', 'incident', 'escalation', 'rate', 'maintained', 'at', 'below', 'threshold',
    'the', 'a', 'an', 'this', 'that', 'for', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'from',
    'with', 'by', 'of', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must',
    'i', 'me', 'my', 'you', 'your', 'he', 'she', 'it', 'we', 'they', 'them',
    'access', 'attempt', 'attempts', 'from', 'ip', 'host', 'port', 'user', 'domain',
    'check', 'verify', 'investigate', 'analyze', 'detect', 'monitor', 'track',
    'execute', 'block', 'isolate', 'generate', 'find', 'show', 'get', 'set',
    'compliance', 'requirements', 'data', 'system', 'network', 'threat', 'intelligence',
    'report', 'tool', 'type', 'count', 'metric', 'value', 'model', 'attack',
    'response', 'coordination', 'team', 'teams', 'platform', 'feeds', 'provided',
    'including', 'hashes', 'infrastructure', 'review', 'repository', 'branch', 'commit',
    'contains', 'configuration', 'source', 'code', 'audit', 'needed', 'detected',
    'against', 'using', 'techniques', 'coordinated', 'across', 'engineering', 'legal',
    'validated', 'mapped', 'controls', 'function', 'covering', 'objectives', 'processing',
    'consumer', 'facilitated', 'during', 'breach', 'confirmed', 'explanations', 'met',
    'interpretability', 'medical', 'automated', 'testing', 'pipeline', 'executed', 'cases',
    'pass', 'validated', 'bias', 'metrics', 'fairness', 'found', 'gender', 'outputs',
    'filtered', 'inappropriate', 'content', 'validated', 'controls', 'remediation', 'completed',
    'issues', 'within', 'sla', 'enforced', 'filtering', 'blocking', 'toxic',
    'verification', 'subject', 'access', 'rifica', '46-0958', 'dsar', 'request',
    'email', 'address', 'phone', 'number', 'data', 'completed', 'for'
}

# Problematic labels that should never have short/common words
PROBLEMATIC_LABELS = {
    'SUBJECT_TYPE', 'ACCESS_TYPE', 'AI_MODEL_TYPE', 'SECURITY_TYPE', 'INCIDENT_TYPE',
    'METRIC_TYPE', 'THRESHOLD_TYPE', 'TOOL', 'TIME_UNIT', 'PRIORITIZATION_TYPE',
    'SERVICE', 'SOURCE_TYPE', 'ENCRYPTION_TYPE', 'VULNERABILITY_ID', 'TRAINING_TYPE',
    'INTEGRATION_TYPE', 'BRANCH', 'COMMIT', 'QUERY_TYPE', 'REQUIREMENT_TYPE',
    'MONITORING_TYPE', 'MITIGATION_TYPE', 'PIPELINE_TYPE', 'REPOSITORY', 'REQUEST_TYPE'
}


def is_partial_word(text: str) -> bool:
    """Check if text is a partial word (substring of common word)."""
    text_lower = text.lower().strip()
    
    # Check exact match
    if text_lower in COMMON_WORDS_NEVER_ENTITIES:
        return True
    
    # Check if it's a substring
    for word in COMMON_WORDS_NEVER_ENTITIES:
        if text_lower in word and len(text_lower) < len(word) and len(text_lower) <= 8:
            return True
    
    return False


def should_remove_entity(entity_text: str, label: str) -> bool:
    """Determine if entity should be removed."""
    entity_lower = entity_text.lower().strip()
    
    # Remove if it's a common word or partial word
    if is_partial_word(entity_text):
        return True
    
    # Remove if it has problematic label and is short/common
    if label in PROBLEMATIC_LABELS:
        if len(entity_lower) <= 8 and is_partial_word(entity_text):
            return True
    
    # Remove if too short (unless it's a valid ID pattern)
    if len(entity_lower) <= 2:
        # Keep if it looks like a valid ID (numbers, letters, etc.)
        if not (entity_lower.isdigit() or entity_lower.isalpha()):
            return True
    
    return False


def fix_file(file_path: Path) -> dict:
    """Fix all entities in a file."""
    stats = {
        'file': str(file_path),
        'removed': 0,
        'total_before': 0,
        'total_after': 0
    }
    
    fixed_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                text = data.get('text', '')
                entities = data.get('entities', [])
                stats['total_before'] += len(entities)
                
                fixed_entities = []
                
                for start, end, label in entities:
                    if start < 0 or end > len(text) or start >= end:
                        stats['removed'] += 1
                        continue
                    
                    entity_text = text[start:end].strip()
                    
                    if should_remove_entity(entity_text, label):
                        stats['removed'] += 1
                        continue
                    
                    # Keep entity but ensure boundaries are correct (no leading/trailing space)
                    # Find actual boundaries without whitespace
                    actual_start = start
                    actual_end = end
                    
                    # Trim leading whitespace
                    while actual_start < actual_end and text[actual_start].isspace():
                        actual_start += 1
                    
                    # Trim trailing whitespace
                    while actual_end > actual_start and text[actual_end - 1].isspace():
                        actual_end -= 1
                    
                    if actual_start < actual_end:
                        fixed_entities.append([actual_start, actual_end, label])
                    else:
                        stats['removed'] += 1
                
                stats['total_after'] += len(fixed_entities)
                data['entities'] = fixed_entities
                fixed_data.append(data)
                
            except Exception as e:
                print(f"Error processing line {line_num} in {file_path}: {e}")
                continue
    
    # Write fixed data
    backup_path = file_path.with_suffix('.jsonl.backup5')
    if not backup_path.exists():
        import shutil
        shutil.copy(file_path, backup_path)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in fixed_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return stats


def main():
    base_dir = Path("cyber-train/entities-intent")
    entity_files = sorted(list(base_dir.rglob("*_entities.jsonl")))
    
    print("="*70)
    print("FINAL FIX - REMOVING PARTIAL WORDS AND COMMON WORDS")
    print("="*70)
    print(f"\nFiles to process: {len(entity_files)}")
    
    total_removed = 0
    total_before = 0
    total_after = 0
    
    for file_path in entity_files:
        print(f"\n📄 Processing: {file_path.relative_to(base_dir)}")
        stats = fix_file(file_path)
        total_removed += stats['removed']
        total_before += stats['total_before']
        total_after += stats['total_after']
        
        if stats['removed'] > 0:
            print(f"   Removed: {stats['removed']} entities")
            print(f"   Before: {stats['total_before']} entities")
            print(f"   After: {stats['total_after']} entities")
        else:
            print(f"   ✅ No issues found")
    
    print("\n" + "="*70)
    print("FINAL FIX SUMMARY")
    print("="*70)
    print(f"Total entities before: {total_before:,}")
    print(f"Total entities after: {total_after:,}")
    print(f"Total removed: {total_removed:,}")
    print(f"Reduction: {total_removed / total_before * 100:.2f}%")
    print("\n✅ Final fix applied! Re-run verification to confirm 100%.")


if __name__ == "__main__":
    main()

