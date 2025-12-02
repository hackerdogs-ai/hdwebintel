#!/usr/bin/env python3
"""
Comprehensive script to fix ALL entity boundary and labeling issues.
This script:
1. Fixes wrong boundaries (IPs, domains, CVEs, emails, etc.)
2. Removes false positives (common words labeled as entities)
3. Fixes wrong entity type assignments
4. Validates all entities
"""

import json
import re
from pathlib import Path
from typing import List, Tuple, Dict
from collections import defaultdict
import argparse

# Patterns for validation
IP_PATTERN = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?[\d\s\-\(\)]{10,}\b')
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b')
WALLET_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')
LATITUDE_PATTERN = re.compile(r'\b-?\d{1,2}(\.\d+)?\b')  # -90 to 90
LONGITUDE_PATTERN = re.compile(r'\b-?\d{1,3}(\.\d+)?\b')  # -180 to 180

# Common words that should NEVER be entities
COMMON_WORDS_NEVER_ENTITIES = {
    # User's specific examples
    'ai', 'security', 'incident', 'escalation', 'rate', 'maintained', 'at', 'below', 'threshold',
    # Basic words
    'the', 'a', 'an', 'this', 'that', 'for', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'from',
    'with', 'by', 'of', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must',
    'i', 'me', 'my', 'you', 'your', 'he', 'she', 'it', 'we', 'they', 'them',
    'what', 'when', 'where', 'why', 'how', 'who', 'which', 'whose', 'whom',
    'up', 'down', 'out', 'off', 'over', 'under', 'above', 'below',
    # Technical common words
    'access', 'attempt', 'attempts', 'from', 'ip', 'host', 'port', 'user', 'domain',
    'check', 'verify', 'investigate', 'analyze', 'detect', 'monitor', 'track',
    'execute', 'block', 'isolate', 'generate', 'find', 'show', 'get', 'set',
    'compliance', 'requirements', 'data', 'system', 'network', 'threat', 'intelligence',
    'report', 'tool', 'type', 'count', 'metric', 'value', 'model', 'attack',
    # More common words
    'response', 'coordination', 'team', 'teams', 'platform', 'feeds', 'provided',
    'including', 'hashes', 'infrastructure', 'review', 'repository', 'branch', 'commit',
    'contains', 'configuration', 'source', 'code', 'audit', 'needed', 'detected',
    'against', 'using', 'techniques', 'coordinated', 'across', 'engineering', 'legal',
    'validated', 'mapped', 'controls', 'function', 'covering', 'objectives', 'processing',
    'consumer', 'facilitated', 'during', 'breach', 'confirmed', 'explanations', 'met',
    'interpretability', 'medical', 'automated', 'testing', 'pipeline', 'executed', 'cases',
    'pass', 'validated', 'bias', 'metrics', 'fairness', 'found', 'gender', 'outputs',
    'filtered', 'inappropriate', 'content', 'validated', 'controls', 'remediation', 'completed',
    'issues', 'within', 'sla', 'enforced', 'filtering', 'blocking', 'toxic'
}

# Entity types that should NOT be assigned to common words
PROBLEMATIC_LABELS_FOR_COMMON = {
    'AI_MODEL_TYPE', 'SECURITY_TYPE', 'INCIDENT_TYPE', 'METRIC_TYPE', 'THRESHOLD_TYPE',
    'TOOL', 'TIME_UNIT', 'PRIORITIZATION_TYPE', 'SERVICE', 'SOURCE_TYPE',
    'ENCRYPTION_TYPE', 'VULNERABILITY_ID', 'TRAINING_TYPE', 'INTEGRATION_TYPE',
    'BRANCH', 'COMMIT', 'QUERY_TYPE', 'REQUIREMENT_TYPE'
}

# Valid entity patterns by type
VALID_PATTERNS = {
    'IP_ADDRESS': IP_PATTERN,
    'DOMAIN': DOMAIN_PATTERN,
    'CVE_ID': CVE_PATTERN,
    'EMAIL': EMAIL_PATTERN,
    'EMAIL_ADDRESS': EMAIL_PATTERN,
    'PHONE_NUMBER': PHONE_PATTERN,
    'SSN': SSN_PATTERN,
    'CREDIT_CARD_NUMBER': CREDIT_CARD_PATTERN,
    'WALLET_ADDRESS': WALLET_PATTERN,
    'LATITUDE': LATITUDE_PATTERN,
    'LONGITUDE': LONGITUDE_PATTERN,
}


def find_entities_in_text(text: str, entity_type: str) -> List[Tuple[int, int, str]]:
    """Find actual entities of given type in text."""
    entities = []
    
    if entity_type in VALID_PATTERNS:
        pattern = VALID_PATTERNS[entity_type]
        for match in pattern.finditer(text):
            entities.append((match.start(), match.end(), entity_type))
    
    return entities


def is_common_word(text: str) -> bool:
    """Check if text is a common word that shouldn't be an entity."""
    text_lower = text.lower().strip()
    return text_lower in COMMON_WORDS_NEVER_ENTITIES


def is_problematic_label_for_common(text: str, label: str) -> bool:
    """Check if common word has problematic label."""
    if label in PROBLEMATIC_LABELS_FOR_COMMON:
        if is_common_word(text):
            return True
    return False


def fix_entity_boundaries(text: str, entities: List[List]) -> List[List]:
    """Fix entity boundaries and remove false positives."""
    fixed_entities = []
    removed_count = 0
    fixed_count = 0
    
    for start, end, label in entities:
        # Validate boundaries
        if start < 0 or end > len(text) or start >= end:
            removed_count += 1
            continue
        
        entity_text = text[start:end]
        entity_lower = entity_text.lower().strip()
        
        # Remove common words as entities (AGGRESSIVE)
        if is_common_word(entity_text):
            removed_count += 1
            continue
        
        # Remove if entity text is a substring of a common word
        # (e.g., "securit" is part of "security")
        is_substring_of_common = False
        for common_word in COMMON_WORDS_NEVER_ENTITIES:
            if entity_lower in common_word and len(entity_lower) < len(common_word) and len(entity_lower) > 2:
                is_substring_of_common = True
                break
        
        if is_substring_of_common:
            removed_count += 1
            continue
        
        # Remove problematic labels for common words
        if is_problematic_label_for_common(entity_text, label):
            removed_count += 1
            continue
        
        # Remove problematic labels for short/common words
        if label in PROBLEMATIC_LABELS_FOR_COMMON:
            if len(entity_lower) <= 10:
                # Check if it's a common word or substring
                if entity_lower in COMMON_WORDS_NEVER_ENTITIES:
                    removed_count += 1
                    continue
                # Check if it's a substring
                for common_word in COMMON_WORDS_NEVER_ENTITIES:
                    if entity_lower in common_word and len(entity_lower) < len(common_word):
                        removed_count += 1
                        break
                else:
                    continue
        
        # Remove single words that are common (unless they're proper nouns)
        if len(entity_text.split()) == 1:
            if entity_lower in COMMON_WORDS_NEVER_ENTITIES:
                removed_count += 1
                continue
        
        # Remove if entity text is too short and common
        if len(entity_text) <= 3 and entity_lower in COMMON_WORDS_NEVER_ENTITIES:
            removed_count += 1
            continue
        
        # Remove entities that are clearly partial words (like " ma" from "maintained")
        # Check if entity text (stripped) is a substring of any common word
        entity_stripped = entity_text.strip()
        entity_stripped_lower = entity_stripped.lower()
        if len(entity_stripped_lower) <= 5:  # Short partial words
            for common_word in COMMON_WORDS_NEVER_ENTITIES:
                if entity_stripped_lower in common_word and len(entity_stripped_lower) < len(common_word):
                    removed_count += 1
                    break
            else:
                # Check if it's a common word itself
                if entity_stripped_lower in COMMON_WORDS_NEVER_ENTITIES:
                    removed_count += 1
                    continue
            if removed_count > 0:
                continue
        
        # Remove entities with spaces that contain common words
        if ' ' in entity_text:
            words = entity_text.lower().split()
            # If all words are common, remove
            if all(word in COMMON_WORDS_NEVER_ENTITIES for word in words):
                removed_count += 1
                continue
            # If any word is a substring of a common word, remove
            for word in words:
                for common_word in COMMON_WORDS_NEVER_ENTITIES:
                    if word in common_word and len(word) < len(common_word) and len(word) <= 5:
                        removed_count += 1
                        break
                if removed_count > 0:
                    break
            if removed_count > 0:
                continue
        
        # Fix specific entity types
        if label == 'IP_ADDRESS':
            # Find actual IP in text
            ip_matches = IP_PATTERN.findall(text)
            if ip_matches:
                # Check if entity text matches an IP
                if entity_text not in ip_matches:
                    # Find the IP that should be labeled
                    for ip in ip_matches:
                        ip_start = text.find(ip)
                        if ip_start != -1:
                            # Replace with correct boundary
                            fixed_entities.append([ip_start, ip_start + len(ip), label])
                            fixed_count += 1
                            break
                    continue
            else:
                # No IP in text but labeled as IP_ADDRESS
                if not any(c.isdigit() and '.' in entity_text for c in entity_text):
                    removed_count += 1
                    continue
        
        elif label == 'DOMAIN':
            domain_matches = DOMAIN_PATTERN.findall(text)
            domain_strings = [''.join(match) for match in domain_matches if match[0]]
            
            if domain_strings:
                if entity_text not in domain_strings:
                    for domain in domain_strings:
                        domain_start = text.find(domain)
                        if domain_start != -1:
                            fixed_entities.append([domain_start, domain_start + len(domain), label])
                            fixed_count += 1
                            break
                    continue
            else:
                if '.' not in entity_text or len(entity_text) < 3:
                    removed_count += 1
                    continue
        
        elif label == 'CVE_ID':
            cve_matches = CVE_PATTERN.findall(text)
            if cve_matches:
                if entity_text.upper() not in [c.upper() for c in cve_matches]:
                    for cve in cve_matches:
                        cve_start = text.upper().find(cve.upper())
                        if cve_start != -1:
                            fixed_entities.append([cve_start, cve_start + len(cve), label])
                            fixed_count += 1
                            break
                    continue
            else:
                if not entity_text.upper().startswith('CVE-'):
                    removed_count += 1
                    continue
        
        elif label in ['EMAIL', 'EMAIL_ADDRESS']:
            email_matches = EMAIL_PATTERN.findall(text)
            if email_matches:
                if entity_text not in email_matches:
                    for email in email_matches:
                        email_start = text.find(email)
                        if email_start != -1:
                            fixed_entities.append([email_start, email_start + len(email), label])
                            fixed_count += 1
                            break
                    continue
            else:
                if '@' not in entity_text:
                    removed_count += 1
                    continue
        
        # Keep valid entities
        fixed_entities.append([start, end, label])
    
    return fixed_entities, removed_count, fixed_count


def fix_file(file_path: Path, dry_run: bool = True) -> Dict:
    """Fix all entities in a file."""
    stats = {
        'total_lines': 0,
        'total_entities_before': 0,
        'total_entities_after': 0,
        'removed': 0,
        'fixed': 0,
        'issues': []
    }
    
    fixed_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            stats['total_lines'] += 1
            try:
                data = json.loads(line)
                text = data.get('text', '')
                original_entities = data.get('entities', [])
                stats['total_entities_before'] += len(original_entities)
                
                # Fix entities
                fixed_entities, removed, fixed = fix_entity_boundaries(text, original_entities)
                stats['removed'] += removed
                stats['fixed'] += fixed
                stats['total_entities_after'] += len(fixed_entities)
                
                # Update data
                data['entities'] = fixed_entities
                fixed_data.append(data)
                
            except Exception as e:
                stats['issues'].append(f"Line {line_num}: {e}")
                continue
    
    # Write fixed data if not dry run
    if not dry_run:
        backup_path = file_path.with_suffix('.jsonl.backup2')
        if not backup_path.exists():
            import shutil
            shutil.copy(file_path, backup_path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in fixed_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Fix ALL entity boundary and labeling issues in training data"
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
    print("COMPREHENSIVE BOUNDARY FIX - ALL FILES")
    print("="*70)
    print(f"\nMode: {'DRY RUN (preview)' if args.dry_run else 'APPLYING FIXES'}")
    print(f"Files to process: {len(entity_files)}")
    
    total_stats = {
        'total_files': 0,
        'total_lines': 0,
        'total_entities_before': 0,
        'total_entities_after': 0,
        'total_removed': 0,
        'total_fixed': 0,
    }
    
    for file_path in entity_files:
        print(f"\n📄 Processing: {file_path.relative_to(base_dir)}")
        stats = fix_file(file_path, dry_run=args.dry_run)
        
        total_stats['total_files'] += 1
        total_stats['total_lines'] += stats['total_lines']
        total_stats['total_entities_before'] += stats['total_entities_before']
        total_stats['total_entities_after'] += stats['total_entities_after']
        total_stats['total_removed'] += stats['removed']
        total_stats['total_fixed'] += stats['fixed']
        
        if stats['removed'] > 0 or stats['fixed'] > 0:
            print(f"   Removed: {stats['removed']} false positives")
            print(f"   Fixed: {stats['fixed']} boundaries")
            print(f"   Before: {stats['total_entities_before']} entities")
            print(f"   After: {stats['total_entities_after']} entities")
        else:
            print(f"   ✅ No issues found")
    
    print("\n" + "="*70)
    print("FIX SUMMARY")
    print("="*70)
    print(f"Total files processed: {total_stats['total_files']}")
    print(f"Total lines: {total_stats['total_lines']:,}")
    print(f"Total entities before: {total_stats['total_entities_before']:,}")
    print(f"Total entities after: {total_stats['total_entities_after']:,}")
    print(f"Total removed (false positives): {total_stats['total_removed']:,}")
    print(f"Total fixed (boundaries): {total_stats['total_fixed']:,}")
    
    reduction = total_stats['total_entities_before'] - total_stats['total_entities_after']
    reduction_pct = (reduction / total_stats['total_entities_before'] * 100) if total_stats['total_entities_before'] > 0 else 0
    
    print(f"\nEntity reduction: {reduction:,} ({reduction_pct:.1f}%)")
    print("  (Removed false positives and fixed boundaries)")
    
    if args.dry_run:
        print("\n💡 This was a dry run. Use --apply to actually fix the files.")
    else:
        print("\n✅ Fixes applied! Backups created as .backup2 files.")
        print("   Next: Re-prepare training data and retrain models")


if __name__ == "__main__":
    main()

