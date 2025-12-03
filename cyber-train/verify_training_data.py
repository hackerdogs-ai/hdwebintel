#!/usr/bin/env python3
"""
Comprehensive Training Data Verification Script

This script:
1. Verifies all boundaries are accurate
2. Verifies all labels are correct
3. Checks entity type distribution
4. Identifies underrepresented entity types
5. Reports any issues found
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Set

# Common words that should NOT be entities
COMMON_WORDS_NOT_ENTITIES = {
    "find", "extract", "url", "json", "xml", "python", "javascript",
    "instagram", "facebook", "twitter", "linkedin", "telegram", "discord",
    "slack", "whatsapp", "github", "git", "code", "import", "os", "found",
    "detected", "check", "verify", "analyze", "investigate", "scan",
    "monitor", "track", "report", "generate", "create", "update", "delete",
    "various", "maximum", "minimum", "average", "total", "count"
}

def verify_boundaries(text: str, start: int, end: int, label: str) -> Tuple[bool, str]:
    """Verify entity boundaries are accurate."""
    issues = []
    
    # Check bounds
    if start < 0:
        issues.append(f"Start index {start} is negative")
    if end > len(text):
        issues.append(f"End index {end} exceeds text length {len(text)}")
    if start >= end:
        issues.append(f"Start {start} >= end {end}")
    
    # Get entity text
    entity_text = text[start:end]
    
    # Check for whitespace
    if entity_text != entity_text.strip():
        issues.append(f"Entity has leading/trailing whitespace: '{entity_text}'")
    
    # Check boundaries match word boundaries (for most entity types)
    if label not in ["HASH", "IP_ADDRESS", "IPV6_ADDRESS", "EMAIL_ADDRESS", "PHONE_NUMBER", "SSN", "CREDIT_CARD_NUMBER"]:
        # For text entities, check word boundaries
        if start > 0 and text[start-1] not in ' \n\t.,;:!?()[]{}"\'<>':
            # Check if it's intentional (like part of a compound word)
            if not (text[start-1].isalnum() and entity_text[0].isalnum()):
                issues.append(f"Start boundary not at word boundary: '{text[max(0,start-5):start+5]}'")
        if end < len(text) and text[end] not in ' \n\t.,;:!?()[]{}"\'<>':
            if not (text[end-1].isalnum() and text[end].isalnum()):
                issues.append(f"End boundary not at word boundary: '{text[max(0,end-5):end+5]}'")
    
    # Check entity text matches
    if not entity_text:
        issues.append("Entity text is empty")
    
    return len(issues) == 0, "; ".join(issues) if issues else "OK"

def verify_label(text: str, start: int, end: int, label: str) -> Tuple[bool, str]:
    """Verify entity label is correct."""
    entity_text = text[start:end].strip()
    context_before = text[max(0, start-30):start].lower()
    context_after = text[end:min(len(text), end+30)].lower()
    
    issues = []
    
    # Check for common words as TOOL
    if label == "TOOL" and entity_text.lower() in COMMON_WORDS_NOT_ENTITIES:
        issues.append(f"Common word '{entity_text}' labeled as TOOL")
    
    # Check DOMAIN vs HOST_TYPE
    if label == "DOMAIN":
        if "internal" in context_before or "internal" in context_after or ".internal" in entity_text:
            issues.append(f"Internal domain '{entity_text}' should be HOST_TYPE")
        if "server" in context_before or "host" in context_before:
            issues.append(f"Hostname '{entity_text}' should be HOST_TYPE")
    
    # Check DOMAIN vs EMAIL_ADDRESS
    if label == "EMAIL_ADDRESS" and "@" not in entity_text:
        issues.append(f"Domain '{entity_text}' labeled as EMAIL_ADDRESS (missing @)")
    
    # Check REPOSITORY vs FILE_PATH
    if label == "REPOSITORY":
        if entity_text.startswith('/') or entity_text.startswith('~') or \
           entity_text.startswith('C:\\') or entity_text.startswith('\\'):
            issues.append(f"File path '{entity_text}' labeled as REPOSITORY")
        if "/.ssh/" in entity_text or "/.config/" in entity_text:
            issues.append(f"File path '{entity_text}' labeled as REPOSITORY")
    
    # Check PHONE_NUMBER format
    if label == "PHONE_NUMBER":
        digits_only = re.sub(r'\D', '', entity_text)
        # International numbers can vary (e.g., German +49 30 2273 0 has 9 digits)
        if len(digits_only) < 7:
            issues.append(f"Phone number '{entity_text}' has <7 digits")
        if entity_text.startswith('-'):
            issues.append(f"Partial phone number '{entity_text}' (starts with -)")
    
    # Check for standalone numbers
    if label in ["METRIC_TYPE", "PROTOCOL_TYPE", "PORT_TYPE"]:
        if entity_text.isdigit() and len(entity_text) <= 3:
            issues.append(f"Standalone number '{entity_text}' labeled as {label}")
    
    return len(issues) == 0, "; ".join(issues) if issues else "OK"

def verify_entity(text: str, start: int, end: int, label: str) -> Dict:
    """Verify a single entity."""
    boundary_ok, boundary_issue = verify_boundaries(text, start, end, label)
    label_ok, label_issue = verify_label(text, start, end, label)
    
    return {
        "boundary_ok": boundary_ok,
        "boundary_issue": boundary_issue,
        "label_ok": label_ok,
        "label_issue": label_issue,
        "entity_text": text[start:end] if boundary_ok else "",
        "label": label
    }

def analyze_training_data(base_dir: Path) -> Dict:
    """Analyze all training data files."""
    stats = {
        "files_processed": 0,
        "total_lines": 0,
        "total_entities": 0,
        "entity_types": Counter(),
        "boundary_issues": [],
        "label_issues": [],
        "files": defaultdict(lambda: {
            "lines": 0,
            "entities": 0,
            "entity_types": Counter(),
            "boundary_issues": [],
            "label_issues": []
        })
    }
    
    for pillar_dir in sorted(base_dir.iterdir()):
        if not pillar_dir.is_dir() or pillar_dir.name.startswith('.'):
            continue
        
        entity_file = pillar_dir / f"{pillar_dir.name}_entities.jsonl"
        if not entity_file.exists():
            continue
        
        stats["files_processed"] += 1
        file_stats = stats["files"][pillar_dir.name]
        
        with open(entity_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                
                stats["total_lines"] += 1
                file_stats["lines"] += 1
                
                try:
                    data = json.loads(line)
                    text = data.get("text", "")
                    entities = data.get("entities", [])
                    
                    for start, end, label in entities:
                        stats["total_entities"] += 1
                        file_stats["entities"] += 1
                        stats["entity_types"][label] += 1
                        file_stats["entity_types"][label] += 1
                        
                        # Verify entity
                        verification = verify_entity(text, start, end, label)
                        
                        if not verification["boundary_ok"]:
                            stats["boundary_issues"].append({
                                "file": pillar_dir.name,
                                "line": line_num,
                                "issue": verification["boundary_issue"],
                                "entity": verification["entity_text"],
                                "label": label,
                                "text_snippet": text[max(0, start-20):min(len(text), end+20)]
                            })
                            file_stats["boundary_issues"].append(verification["boundary_issue"])
                        
                        if not verification["label_ok"]:
                            stats["label_issues"].append({
                                "file": pillar_dir.name,
                                "line": line_num,
                                "issue": verification["label_issue"],
                                "entity": verification["entity_text"],
                                "label": label,
                                "text_snippet": text[max(0, start-20):min(len(text), end+20)]
                            })
                            file_stats["label_issues"].append(verification["label_issue"])
                
                except json.JSONDecodeError as e:
                    print(f"⚠️  JSON error in {pillar_dir.name}:{line_num}: {e}")
    
    return stats

def generate_report(stats: Dict) -> str:
    """Generate a comprehensive report."""
    report = []
    report.append("="*80)
    report.append("TRAINING DATA VERIFICATION REPORT")
    report.append("="*80)
    report.append("")
    
    # Overall statistics
    report.append("📊 Overall Statistics:")
    report.append(f"   Files processed: {stats['files_processed']}")
    report.append(f"   Total lines: {stats['total_lines']:,}")
    report.append(f"   Total entities: {stats['total_entities']:,}")
    report.append(f"   Unique entity types: {len(stats['entity_types'])}")
    report.append("")
    
    # Boundary issues
    report.append("🔍 Boundary Issues:")
    report.append(f"   Total boundary issues: {len(stats['boundary_issues'])}")
    if stats['boundary_issues']:
        boundary_by_type = Counter(issue['issue'].split(';')[0] for issue in stats['boundary_issues'])
        report.append("   Top issues:")
        for issue_type, count in boundary_by_type.most_common(10):
            report.append(f"      {issue_type}: {count}")
        report.append("")
        report.append("   Sample issues:")
        for issue in stats['boundary_issues'][:10]:
            report.append(f"      {issue['file']}:{issue['line']} - {issue['issue']}")
            report.append(f"         Entity: '{issue['entity']}' ({issue['label']})")
            report.append(f"         Context: '...{issue['text_snippet']}...'")
            report.append("")
    else:
        report.append("   ✅ No boundary issues found!")
    report.append("")
    
    # Label issues
    report.append("🏷️  Label Issues:")
    report.append(f"   Total label issues: {len(stats['label_issues'])}")
    if stats['label_issues']:
        label_by_type = Counter(issue['issue'].split(';')[0] for issue in stats['label_issues'])
        report.append("   Top issues:")
        for issue_type, count in label_by_type.most_common(10):
            report.append(f"      {issue_type}: {count}")
        report.append("")
        report.append("   Sample issues:")
        for issue in stats['label_issues'][:10]:
            report.append(f"      {issue['file']}:{issue['line']} - {issue['issue']}")
            report.append(f"         Entity: '{issue['entity']}' ({issue['label']})")
            report.append(f"         Context: '...{issue['text_snippet']}...'")
            report.append("")
    else:
        report.append("   ✅ No label issues found!")
    report.append("")
    
    # Entity type distribution
    report.append("📊 Entity Type Distribution:")
    report.append("   Top 30 entity types:")
    for entity_type, count in stats['entity_types'].most_common(30):
        report.append(f"      {entity_type:30s}: {count:6,}")
    report.append("")
    
    # Underrepresented entity types (from test suite analysis)
    report.append("⚠️  Underrepresented Entity Types (from test suite):")
    underrepresented = {
        "MALWARE_TYPE": 200,  # We added 200, but may need more
        "LLM_MODEL": 120,     # We added 120, but may need more
        "DATE": 99,           # We added 99, but may need more
        "HASH": 39,           # We added 39, but may need more
        "PHONE_NUMBER": 55,   # We added 55, but may need more
        "COMPLIANCE_FRAMEWORK": 160,  # We added 160, but may need more
        "URL": 32,            # We added 32, but may need more
        "LLM_PROVIDER": 0,    # Need to add
        "THREAT_ACTOR": 120,  # We added 120, but may need more
        "TIME": 0,            # Need to add
        "FILE_PATH": 0,       # Need to add
        "DOMAIN": 0,          # May need more
        "EMOJI": 0,           # Need to add
        "IPV6_ADDRESS": 60,   # We added 60, but may need more
        "SSN": 30,            # We added 30, but may need more
        "CREDIT_CARD_NUMBER": 30,  # We added 30, but may need more
        "LATITUDE": 0,        # Need to add
        "LONGITUDE": 0,       # Need to add
        "DATACENTER": 0,      # Need to add
    }
    
    for entity_type, min_needed in underrepresented.items():
        current_count = stats['entity_types'].get(entity_type, 0)
        if current_count < min_needed:
            report.append(f"      {entity_type:30s}: {current_count:4,} (need {min_needed:4,} more)")
    
    report.append("")
    
    # File-level statistics
    report.append("📂 File-Level Statistics:")
    report.append("   Files with most entities:")
    files_by_entities = sorted(stats['files'].items(), key=lambda x: x[1]['entities'], reverse=True)
    for file_name, file_stats in files_by_entities[:10]:
        report.append(f"      {file_name:40s}: {file_stats['entities']:6,} entities, "
                     f"{len(file_stats['boundary_issues'])} boundary issues, "
                     f"{len(file_stats['label_issues'])} label issues")
    
    report.append("")
    report.append("="*80)
    
    return "\n".join(report)

def main():
    base_dir = Path("entities-intent")
    
    print("🔍 Analyzing training data...")
    stats = analyze_training_data(base_dir)
    
    print("📝 Generating report...")
    report = generate_report(stats)
    
    print(report)
    
    # Save report
    with open("TRAINING_DATA_VERIFICATION_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n✅ Report saved to TRAINING_DATA_VERIFICATION_REPORT.md")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ Files processed: {stats['files_processed']}")
    print(f"✅ Total entities: {stats['total_entities']:,}")
    print(f"⚠️  Boundary issues: {len(stats['boundary_issues'])}")
    print(f"⚠️  Label issues: {len(stats['label_issues'])}")
    print(f"📊 Unique entity types: {len(stats['entity_types'])}")
    print("="*80)

if __name__ == "__main__":
    main()

