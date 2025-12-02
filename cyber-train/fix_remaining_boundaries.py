#!/usr/bin/env python3
"""
Fix the remaining 36 WRONG_BOUNDARY issues with aggressive pattern matching.
This script specifically targets edge cases where boundaries are still wrong.
"""

import json
import re
from pathlib import Path
from typing import List, Tuple, Optional

# Patterns for validation - more comprehensive
IP_PATTERN = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
DOMAIN_PATTERN = re.compile(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}\b')
CVE_PATTERN = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
EMAIL_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
PHONE_PATTERN = re.compile(r'\b\+?[\d\s\-\(\)]{10,}\b')
# More specific phone patterns
PHONE_US_PATTERN = re.compile(r'\b1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
PHONE_INTL_PATTERN = re.compile(r'\b\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}\b')
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b')
# More specific credit card - must be 16 digits total
CREDIT_CARD_STRICT = re.compile(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b')

# Pattern validation by entity type
PATTERN_VALIDATION = {
    'IP_ADDRESS': IP_PATTERN,
    'DOMAIN': DOMAIN_PATTERN,
    'CVE_ID': CVE_PATTERN,
    'EMAIL': EMAIL_PATTERN,
    'EMAIL_ADDRESS': EMAIL_PATTERN,
    'PHONE_NUMBER': PHONE_PATTERN,
    'SSN': SSN_PATTERN,
    'CREDIT_CARD_NUMBER': CREDIT_CARD_STRICT,
}


def find_best_match(text: str, label: str, current_start: int, current_end: int) -> Optional[Tuple[int, int]]:
    """Find the best matching entity in text for the given label."""
    if label not in PATTERN_VALIDATION:
        return None
    
    # For phone numbers, try more specific patterns first
    if label == 'PHONE_NUMBER':
        # Try international format (more flexible)
        intl_matches = list(PHONE_INTL_PATTERN.finditer(text))
        if intl_matches:
            matches = intl_matches
        else:
            # Try US format
            us_matches = list(PHONE_US_PATTERN.finditer(text))
            if us_matches:
                matches = us_matches
            else:
                # Fall back to general pattern
                pattern = PATTERN_VALIDATION[label]
                matches = list(pattern.finditer(text))
    else:
        pattern = PATTERN_VALIDATION[label]
        matches = list(pattern.finditer(text))
    
    if not matches:
        return None
    
    # Find match closest to current position
    best_match = None
    best_distance = float('inf')
    current_center = (current_start + current_end) / 2
    
    for match in matches:
        match_start, match_end = match.span()
        match_center = (match_start + match_end) / 2
        distance = abs(match_center - current_center)
        
        # Prefer matches that are closer and don't overlap with current
        if distance < best_distance:
            # Check if this is a better match (not overlapping with current wrong boundary)
            if not (match_start < current_end and match_end > current_start):
                best_distance = distance
                best_match = (match_start, match_end)
            elif match_start == current_start or match_end == current_end:
                # If it shares a boundary, it might be the right one
                best_distance = distance
                best_match = (match_start, match_end)
    
    # If no non-overlapping match, use closest
    if best_match is None and matches:
        for match in matches:
            match_start, match_end = match.span()
            match_center = (match_start + match_end) / 2
            distance = abs(match_center - current_center)
            if distance < best_distance:
                best_distance = distance
                best_match = (match_start, match_end)
    
    return best_match


def fix_entity_aggressive(text: str, start: int, end: int, label: str) -> Tuple[int, int, bool]:
    """
    Aggressively fix entity boundaries.
    Returns: (new_start, new_end, should_remove)
    """
    # Validate boundaries
    if start < 0 or end > len(text) or start >= end:
        return start, end, True
    
    entity_text = text[start:end].strip()
    
    # If label requires pattern validation, find correct boundary
    if label in PATTERN_VALIDATION:
        pattern = PATTERN_VALIDATION[label]
        
        # Check if current entity matches pattern
        if not pattern.match(entity_text):
            # Find what should be there
            best_match = find_best_match(text, label, start, end)
            
            if best_match:
                new_start, new_end = best_match
                # Verify the new match is valid
                new_text = text[new_start:new_end].strip()
                if pattern.match(new_text):
                    return new_start, new_end, False
                else:
                    # Try with stripped text
                    if pattern.match(new_text):
                        return new_start, new_end, False
            else:
                # No valid match found, remove
                return start, end, True
        else:
            # Current entity matches pattern, but check if there's a better match
            # (e.g., if current is partial)
            best_match = find_best_match(text, label, start, end)
            if best_match:
                new_start, new_end = best_match
                new_text = text[new_start:new_end].strip()
                # If new match is longer/more complete, use it
                if len(new_text) > len(entity_text) and pattern.match(new_text):
                    return new_start, new_end, False
    
    return start, end, False


def fix_file(file_path: Path) -> dict:
    """Fix all entities in a file."""
    stats = {
        'file': str(file_path),
        'entities_fixed': 0,
        'entities_removed': 0
    }
    
    fixed_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                text = data.get('text', '')
                entities = data.get('entities', [])
                
                fixed_entities = []
                
                for start, end, label in entities:
                    new_start, new_end, should_remove = fix_entity_aggressive(text, start, end, label)
                    
                    if should_remove:
                        stats['entities_removed'] += 1
                        continue
                    
                    if new_start != start or new_end != end:
                        stats['entities_fixed'] += 1
                    
                    fixed_entities.append([new_start, new_end, label])
                
                data['entities'] = fixed_entities
                fixed_data.append(data)
                
            except Exception as e:
                print(f"Error processing line {line_num} in {file_path}: {e}")
                continue
    
    # Write fixed data
    backup_path = file_path.with_suffix('.jsonl.backup4')
    if not backup_path.exists():
        import shutil
        shutil.copy(file_path, backup_path)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in fixed_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return stats


def main():
    # Get files with WRONG_BOUNDARY issues
    report_file = Path("cyber-train/BOUNDARY_VERIFICATION_REPORT.json")
    files_to_fix = set()
    
    if report_file.exists():
        with open(report_file, 'r') as f:
            report = json.load(f)
        
        for file_data in report['files']:
            for issue in file_data.get('issues', []):
                if issue['type'] == 'WRONG_BOUNDARY':
                    files_to_fix.add(file_data['file'])
    
    base_dir = Path("cyber-train/entities-intent")
    
    print("="*70)
    print("FIXING REMAINING WRONG_BOUNDARY ISSUES")
    print("="*70)
    print(f"\nFiles with WRONG_BOUNDARY issues: {len(files_to_fix)}")
    
    total_fixed = 0
    total_removed = 0
    
    for file_path_str in files_to_fix:
        file_path = Path(file_path_str)
        if not file_path.exists():
            # Try relative path
            file_path = base_dir / Path(file_path_str).name
            if not file_path.exists():
                # Try to find it
                found = list(base_dir.rglob(Path(file_path_str).name))
                if found:
                    file_path = found[0]
                else:
                    print(f"⚠️  File not found: {file_path_str}")
                    continue
        
        print(f"\n📄 Fixing: {file_path.relative_to(base_dir)}")
        stats = fix_file(file_path)
        total_fixed += stats['entities_fixed']
        total_removed += stats['entities_removed']
        print(f"   Fixed: {stats['entities_fixed']} boundaries")
        print(f"   Removed: {stats['entities_removed']} invalid entities")
    
    print("\n" + "="*70)
    print("FIX SUMMARY")
    print("="*70)
    print(f"Total boundaries fixed: {total_fixed}")
    print(f"Total entities removed: {total_removed}")
    print("\n✅ Fixes applied! Re-run verification to confirm.")


if __name__ == "__main__":
    main()

