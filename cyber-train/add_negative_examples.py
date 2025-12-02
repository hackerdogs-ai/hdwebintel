#!/usr/bin/env python3
"""
Add negative examples (true negatives) to training data.
These are sentences with NO entities that help the model learn boundaries.
"""

import json
from pathlib import Path
import argparse
from typing import List, Dict

# Negative examples - sentences with NO entities
# These help the model learn what NOT to extract
NEGATIVE_EXAMPLES = [
    # Common phrases that should NOT have entities
    "Can you help me with this?",
    "I need to check something.",
    "What is the status?",
    "How do I do this?",
    "Tell me more about it.",
    "Is this safe to use?",
    "Let me know if you need anything.",
    "Thanks for your help.",
    "I will get back to you.",
    "Please review this document.",
    
    # Questions without entities
    "What should I do next?",
    "How does this work?",
    "Why is this happening?",
    "When will this be ready?",
    "Where can I find this?",
    "Who should I contact?",
    
    # Casual conversation
    "Hey, what's up?",
    "That's interesting.",
    "I see what you mean.",
    "That makes sense.",
    "Got it, thanks.",
    
    # Instructions without entities
    "Follow the steps carefully.",
    "Make sure to save your work.",
    "Check the settings first.",
    "Review the documentation.",
    "Read the instructions.",
    
    # General statements
    "This is important.",
    "That looks good.",
    "Everything seems fine.",
    "Nothing to report.",
    "All systems operational.",
    
    # Cybersecurity context (no entities)
    "The system is secure.",
    "All checks passed.",
    "No issues detected.",
    "Everything is working correctly.",
    "The configuration looks good.",
    "No vulnerabilities found.",
    "Security measures are in place.",
    "The audit was successful.",
    
    # OSINT context (no entities)
    "The information is verified.",
    "Sources are reliable.",
    "The data is consistent.",
    "No discrepancies found.",
    "The analysis is complete.",
    "All sources checked.",
    "The report is ready.",
    
    # Technical context (no entities)
    "The process completed successfully.",
    "All tests passed.",
    "The system is functioning normally.",
    "No errors occurred.",
    "The operation was successful.",
    "Everything is configured correctly.",
    
    # Common false positive patterns (explicitly negative)
    "I need to investigate this.",
    "Can you check this for me?",
    "Is this safe to use?",
    "What's the status?",
    "How do I proceed?",
    "Tell me what you think.",
    "Let me know if you need help.",
    "Thanks for the information.",
    "I will follow up on this.",
    "Please keep me updated.",
    
    # Edge cases that should NOT be entities
    "The word 'investigate' appears in the text.",
    "The phrase 'check this' is common.",
    "The term 'safe' is used frequently.",
    "The word 'me' is a pronoun.",
    "The phrase 'I need' is common.",
    "The word 'hey' is informal.",
    
    # More cybersecurity/OSINT negative examples
    "The security team reviewed the findings.",
    "The investigation is ongoing.",
    "The analysis revealed no issues.",
    "The system is operating normally.",
    "All security controls are active.",
    "The monitoring is working correctly.",
    "The alert was a false positive.",
    "The scan completed without issues.",
    "The report shows no anomalies.",
    "The data is consistent across sources.",
    
    # More OSINT negative examples
    "The source verification is complete.",
    "The information was cross-referenced.",
    "The analysis confirms the findings.",
    "The data points are consistent.",
    "The investigation found nothing suspicious.",
    "The review process is standard.",
    "The verification steps were followed.",
    "The information is reliable.",
    "The sources are credible.",
    "The analysis methodology is sound.",
]

# Add more examples by generating variations
def generate_negative_variations():
    """Generate more negative examples from templates."""
    templates = [
        "The {noun} is {adjective}.",
        "All {noun} are {adjective}.",
        "The {noun} was {verb}.",
        "No {noun} were found.",
        "The {noun} needs to be {verb}.",
        "All {noun} are working correctly.",
        "The {noun} is functioning normally.",
        "No issues with the {noun}.",
    ]
    
    nouns = ["system", "process", "function", "feature", "component", "module", "service"]
    adjectives = ["working", "operational", "functional", "active", "ready", "complete"]
    verbs = ["completed", "finished", "done", "executed", "processed"]
    
    variations = []
    for template in templates:
        if "{noun}" in template and "{adjective}" in template:
            for noun in nouns:
                for adj in adjectives:
                    variations.append(template.format(noun=noun, adjective=adj))
        elif "{noun}" in template and "{verb}" in template:
            for noun in nouns:
                for verb in verbs:
                    variations.append(template.format(noun=noun, verb=verb))
    
    return variations

# Add generated variations
NEGATIVE_EXAMPLES.extend(generate_negative_variations())


def create_negative_examples_file(output_dir: Path, pillar_name: str = "all", count: int = None):
    """
    Create a JSONL file with negative examples.
    
    Args:
        output_dir: Directory to save the file
        pillar_name: Name of the pillar (or "all" for general)
        count: Number of examples to include (None = all)
    """
    examples = NEGATIVE_EXAMPLES[:count] if count else NEGATIVE_EXAMPLES
    
    if pillar_name == "all":
        output_file = output_dir / "negative_examples.jsonl"
    else:
        output_file = output_dir / f"{pillar_name}_negative_examples.jsonl"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for text in examples:
            data = {
                "text": text,
                "entities": []  # Explicitly empty - no entities
            }
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    return output_file, len(examples)


def add_to_existing_file(jsonl_file: Path, count: int = 50):
    """
    Add negative examples to an existing JSONL file.
    
    Args:
        jsonl_file: Path to existing JSONL file
        count: Number of negative examples to add
    """
    examples = NEGATIVE_EXAMPLES[:count]
    
    # Read existing data
    existing_data = []
    if jsonl_file.exists():
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    existing_data.append(json.loads(line))
                except:
                    continue
    
    # Add negative examples
    for text in examples:
        existing_data.append({
            "text": text,
            "entities": []
        })
    
    # Write back
    backup_file = jsonl_file.with_suffix('.jsonl.backup')
    if not backup_file.exists():
        import shutil
        shutil.copy(jsonl_file, backup_file)
    
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for item in existing_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return len(examples)


def main():
    parser = argparse.ArgumentParser(
        description="Add negative examples (true negatives) to training data"
    )
    parser.add_argument(
        "--base-dir",
        default="cyber-train/entities-intent",
        help="Base directory containing JSONL files"
    )
    parser.add_argument(
        "--pillar",
        help="Specific pillar to add examples to (or 'all' for general)"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=200,
        help="Number of negative examples to add (default: 200)"
    )
    parser.add_argument(
        "--add-to-existing",
        action="store_true",
        help="Add negative examples to existing entity files (10% of each file)"
    )
    parser.add_argument(
        "--create-separate",
        action="store_true",
        help="Create separate negative examples file"
    )
    
    args = parser.parse_args()
    
    base_dir = Path(args.base_dir)
    
    print("="*70)
    print("ADDING NEGATIVE EXAMPLES (TRUE NEGATIVES)")
    print("="*70)
    
    if args.create_separate:
        # Create separate file
        output_file, count = create_negative_examples_file(
            base_dir, 
            pillar_name=args.pillar or "all",
            count=args.count
        )
        print(f"\n✅ Created negative examples file: {output_file}")
        print(f"   Added {count} negative examples")
        print(f"   These are sentences with NO entities")
        print(f"   They help the model learn what NOT to extract")
    
    if args.add_to_existing:
        # Add to existing files
        if args.pillar:
            entity_files = [base_dir / args.pillar / f"{args.pillar}_entities.jsonl"]
        else:
            entity_files = list(base_dir.rglob("*_entities.jsonl"))
        
        total_added = 0
        for entity_file in entity_files:
            if entity_file.exists():
                # Add 10% of file size as negative examples
                with open(entity_file, 'r') as f:
                    line_count = sum(1 for _ in f)
                
                examples_to_add = max(10, line_count // 10)  # 10% or at least 10
                added = add_to_existing_file(entity_file, count=examples_to_add)
                total_added += added
                print(f"  Added {added} negative examples to {entity_file.name}")
        
        print(f"\n✅ Added {total_added} total negative examples to existing files")
    
    if not args.create_separate and not args.add_to_existing:
        print("\n💡 Usage:")
        print("  --create-separate: Create separate negative examples file")
        print("  --add-to-existing: Add negative examples to existing entity files")
        print("\nExample:")
        print("  python3 add_negative_examples.py --create-separate --count 200")
        print("  python3 add_negative_examples.py --add-to-existing --pillar ai_security")


if __name__ == "__main__":
    main()

