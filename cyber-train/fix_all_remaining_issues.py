#!/usr/bin/env python3
"""
Comprehensive fix for ALL remaining boundary issues:
1. WHITESPACE - Remove leading/trailing whitespace from entities
2. WRONG_BOUNDARY - Fix boundaries for IPs, domains, CVEs, emails
3. TOO_SHORT - Remove entities that are too short (likely false positives)
"""

import json
import re
from pathlib import Path
from typing import List, Tuple

# Patterns for validation
IP_PATTERN = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
URL_PATTERN = re.compile(r'https?://[^\s]+|www\.[^\s]+', re.IGNORECASE)

# Common words that should NEVER be entities
COMMON_WORDS_NEVER_ENTITIES = {
    'ai', 'security', 'incident', 'escalation', 'rate', 'maintained', 'at', 'below', 'threshold',
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
    'ma', 'rat', 'ed', 'at', 'securit', 'inciden', 'escalat', 'maintain', 'release', 'monitori',
    'ntegrator', 'nding', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
}

# Pattern validation by entity type
PATTERN_VALIDATION = {
    'IP_ADDRESS': IP_PATTERN,
    'DOMAIN': DOMAIN_PATTERN,
    'CVE_ID': CVE_PATTERN,
    'EMAIL': EMAIL_PATTERN,
    'EMAIL_ADDRESS': EMAIL_PATTERN,
    'URL': URL_PATTERN,
}


def fix_entity(text: str, start: int, end: int, label: str) -> Tuple[int, int, bool]:
    """
    Fix a single entity.
    Returns: (new_start, new_end, should_remove)
    """
    # Validate boundaries
    if start < 0 or end > len(text) or start >= end:
        return start, end, True  # Remove invalid
    
    entity_text = text[start:end]
    entity_stripped = entity_text.strip()
    
    # Fix 1: Remove whitespace
    if entity_text != entity_stripped:
        # Find new boundaries without whitespace
        # Count leading spaces
        leading_spaces = len(entity_text) - len(entity_text.lstrip())
        trailing_spaces = len(entity_text) - len(entity_text.rstrip())
        
        new_start = start + leading_spaces
        new_end = end - trailing_spaces
        
        if new_start >= new_end:
            return start, end, True  # Remove if nothing left
        
        entity_text = text[new_start:new_end]
        start, end = new_start, new_end
    else:
        entity_text = entity_stripped
    
    entity_lower = entity_text.lower()
    
    # Fix 2: Remove too short entities (unless they're valid patterns)
    if len(entity_text) <= 2:
        # Check if it's a valid pattern
        if label in PATTERN_VALIDATION:
            pattern = PATTERN_VALIDATION[label]
            if pattern.match(entity_text):
                return start, end, False  # Keep if valid pattern
        return start, end, True  # Remove if too short and not valid
    
    # Fix 3: Remove common words
    if entity_lower in COMMON_WORDS_NEVER_ENTITIES:
        return start, end, True
    
    # Fix 4: Fix wrong boundaries for pattern-based entities
    if label in PATTERN_VALIDATION:
        pattern = PATTERN_VALIDATION[label]
        
        # Check if current entity matches pattern
        if not pattern.match(entity_text):
            # Find what should be there
            matches = list(pattern.finditer(text))
            if matches:
                # Find the match closest to current position
                best_match = None
                best_distance = float('inf')
                for match in matches:
                    match_start, match_end = match.span()
                    distance = abs(match_start - start) + abs(match_end - end)
                    if distance < best_distance:
                        best_distance = distance
                        best_match = match
                
                if best_match:
                    return best_match.start(), best_match.end(), False
            else:
                # No match found, remove
                return start, end, True
    
    return start, end, False  # Keep as is


def fix_file(file_path: Path, dry_run: bool = True) -> dict:
    """Fix all entities in a file."""
    stats = {
        'file': str(file_path),
        'total_lines': 0,
        'entities_before': 0,
        'entities_after': 0,
        'removed': 0,
        'fixed': 0,
        'whitespace_fixed': 0,
        'boundary_fixed': 0,
        'too_short_removed': 0
    }
    
    fixed_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            stats['total_lines'] += 1
            try:
                data = json.loads(line)
                text = data.get('text', '')
                original_entities = data.get('entities', [])
                stats['entities_before'] += len(original_entities)
                
                fixed_entities = []
                original_count = len(original_entities)
                
                for start, end, label in original_entities:
                    new_start, new_end, should_remove = fix_entity(text, start, end, label)
                    
                    if should_remove:
                        stats['removed'] += 1
                        # Track why it was removed
                        if start < 0 or end > len(text) or start >= end:
                            pass  # Invalid boundary
                        elif len(text[start:end].strip()) <= 2:
                            stats['too_short_removed'] += 1
                        continue
                    
                    # Check if boundary changed
                    if new_start != start or new_end != end:
                        stats['fixed'] += 1
                        # Track what type of fix
                        original_text = text[start:end]
                        new_text = text[new_start:new_end]
                        if original_text.strip() != new_text:
                            if original_text != original_text.strip() or new_text != new_text.strip():
                                stats['whitespace_fixed'] += 1
                            else:
                                stats['boundary_fixed'] += 1
                    
                    fixed_entities.append([new_start, new_end, label])
                
                stats['entities_after'] += len(fixed_entities)
                data['entities'] = fixed_entities
                fixed_data.append(data)
                
            except Exception as e:
                print(f"Error processing line {line_num} in {file_path}: {e}")
                continue
    
    # Write fixed data if not dry run
    if not dry_run:
        backup_path = file_path.with_suffix('.jsonl.backup3')
        if not backup_path.exists():
            import shutil
            shutil.copy(file_path, backup_path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in fixed_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return stats


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Fix ALL remaining boundary issues"
    )
    parser.add_argument(
        "--base-dir",
        default="cyber-train/entities-intent",
        help="Base directory containing JSONL files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually apply the fixes (creates backups)"
    )
    parser.add_argument(
        "--file",
        help="Fix specific file only"
    )
    
    args = parser.parse_args()
    
    if not args.apply and not args.dry_run:
        print("⚠️  Use --dry-run to preview or --apply to fix files")
        return
    
    base_dir = Path(args.base_dir)
    
    if args.file:
        entity_files = [base_dir / args.file]
    else:
        entity_files = sorted(list(base_dir.rglob("*_entities.jsonl")))
    
    print("="*70)
    print("FIXING ALL REMAINING BOUNDARY ISSUES")
    print("="*70)
    print(f"\nMode: {'DRY RUN (preview)' if args.dry_run else 'APPLYING FIXES'}")
    print(f"Files to process: {len(entity_files)}")
    
    total_stats = {
        'total_files': 0,
        'total_lines': 0,
        'entities_before': 0,
        'entities_after': 0,
        'total_removed': 0,
        'total_fixed': 0,
        'whitespace_fixed': 0,
        'boundary_fixed': 0,
        'too_short_removed': 0
    }
    
    for file_path in entity_files:
        print(f"\n📄 Processing: {file_path.relative_to(base_dir)}")
        stats = fix_file(file_path, dry_run=args.dry_run)
        
        total_stats['total_files'] += 1
        total_stats['total_lines'] += stats['total_lines']
        total_stats['entities_before'] += stats['entities_before']
        total_stats['entities_after'] += stats['entities_after']
        total_stats['total_removed'] += stats['removed']
        total_stats['total_fixed'] += stats['fixed']
        total_stats['whitespace_fixed'] += stats['whitespace_fixed']
        total_stats['boundary_fixed'] += stats['boundary_fixed']
        total_stats['too_short_removed'] += stats['too_short_removed']
        
        if stats['removed'] > 0 or stats['fixed'] > 0:
            print(f"   Removed: {stats['removed']} entities")
            print(f"   Fixed: {stats['fixed']} boundaries")
            print(f"   Before: {stats['entities_before']} entities")
            print(f"   After: {stats['entities_after']} entities")
        else:
            print(f"   ✅ No issues found")
    
    print("\n" + "="*70)
    print("FIX SUMMARY")
    print("="*70)
    print(f"Total files processed: {total_stats['total_files']}")
    print(f"Total lines: {total_stats['total_lines']:,}")
    print(f"Total entities before: {total_stats['entities_before']:,}")
    print(f"Total entities after: {total_stats['entities_after']:,}")
    print(f"Total removed: {total_stats['total_removed']:,}")
    print(f"Total fixed: {total_stats['total_fixed']:,}")
    print(f"\nBreakdown:")
    print(f"  Whitespace fixed: {total_stats['whitespace_fixed']:,}")
    print(f"  Boundaries fixed: {total_stats['boundary_fixed']:,}")
    print(f"  Too short removed: {total_stats['too_short_removed']:,}")
    
    reduction = total_stats['entities_before'] - total_stats['entities_after']
    reduction_pct = (reduction / total_stats['entities_before'] * 100) if total_stats['entities_before'] > 0 else 0
    
    print(f"\nEntity reduction: {reduction:,} ({reduction_pct:.1f}%)")
    
    if args.dry_run:
        print("\n💡 This was a dry run. Use --apply to actually fix the files.")
    else:
        print("\n✅ Fixes applied! Backups created as .backup3 files.")
        print("   Next: Re-verify and re-prepare training data")


if __name__ == "__main__":
    main()

