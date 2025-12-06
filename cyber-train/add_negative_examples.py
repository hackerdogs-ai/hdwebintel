#!/usr/bin/env python3
"""
Add negative examples (sentences with no entities) to help model learn boundaries.
This helps reduce false positives by teaching the model what NOT to extract.
"""

import json
import random
from pathlib import Path
from typing import List
from collections import defaultdict

# Negative example templates (sentences with NO entities)
NEGATIVE_TEMPLATES = [
    # Common queries that shouldn't extract entities
    "Can you help me with this security issue?",
    "I need to investigate the problem and find a solution.",
    "What should I do about this security concern?",
    "How can I improve the security posture of my organization?",
    "Please check if everything is working correctly.",
    "I want to verify that the system is secure.",
    "Let me know if there are any issues to address.",
    "What is the best way to handle this situation?",
    "I need assistance with security configuration.",
    "Can you provide guidance on security best practices?",
    "How do I implement proper security controls?",
    "What are the recommended security procedures?",
    "I need to understand the security requirements.",
    "Please explain how to secure the system properly.",
    "What steps should I take to improve security?",
    "I want to ensure compliance with security standards.",
    "How can I monitor security events effectively?",
    "What tools are available for security analysis?",
    "I need to review the security documentation.",
    "Can you help me understand security policies?",
    
    # Common words that might be misidentified
    "The security team needs to investigate and analyze the situation.",
    "We should check and verify all security controls regularly.",
    "The system requires monitoring and tracking of security events.",
    "Security professionals need to detect and respond to threats quickly.",
    "The organization must maintain and improve security posture continuously.",
    "Security awareness training helps employees understand risks better.",
    "The incident response process involves investigation and containment.",
    "Security audits require thorough review and documentation of findings.",
    "The compliance team ensures adherence to security regulations.",
    "Security policies define acceptable use and access controls.",
    
    # Technical terms that aren't entities
    "The application uses JavaScript for frontend development.",
    "The system processes JSON data for API communication.",
    "The security team implements CSRF protection mechanisms.",
    "The network uses Base64 encoding for data transmission.",
    "The application requires XML parsing for configuration files.",
    "The system supports HTML rendering for user interfaces.",
    "The security framework includes Python scripts for automation.",
    "The monitoring system tracks relative performance metrics.",
    "The analysis tool provides absolute measurements of system health.",
    "The security process involves finding and extracting relevant information.",
    
    # Common phrases
    "I need to check if the system is safe and secure.",
    "The security team will investigate the issue thoroughly.",
    "We should verify that all controls are working properly.",
    "The organization needs to analyze the security posture regularly.",
    "Security professionals must detect and respond to threats effectively.",
    "The system requires monitoring and tracking of security events.",
    "Security awareness helps employees understand risks and threats.",
    "The incident response process involves investigation and documentation.",
    "Security audits require review and validation of security controls.",
    "The compliance team ensures adherence to security requirements.",
    
    # Questions without entities
    "What is the current security status?",
    "How do I improve security posture?",
    "What are the security requirements?",
    "How can I verify security controls?",
    "What steps should I take for security?",
    "How do I implement security measures?",
    "What are the best security practices?",
    "How can I monitor security effectively?",
    "What tools are available for security?",
    "How do I ensure security compliance?",
    
    # Commands without entities
    "Please investigate the security issue.",
    "Check the system security configuration.",
    "Verify that all controls are working.",
    "Review the security documentation carefully.",
    "Analyze the security posture thoroughly.",
    "Monitor security events continuously.",
    "Track security metrics regularly.",
    "Document security findings properly.",
    "Report security incidents immediately.",
    "Respond to security threats quickly.",
    
    # Statements without entities
    "The security system is functioning normally.",
    "All security controls are properly configured.",
    "The security team is monitoring the situation.",
    "Security policies are being enforced correctly.",
    "The security posture is improving gradually.",
    "Security awareness training is ongoing.",
    "The incident response process is effective.",
    "Security audits are conducted regularly.",
    "Compliance requirements are being met.",
    "Security documentation is up to date.",
]

# Additional negative examples for specific false positive patterns
SPECIFIC_NEGATIVES = [
    # TOOL false positives
    "The application uses CSRF tokens for security protection.",
    "JavaScript is used for frontend development in the application.",
    "The system processes JSON data for API communication.",
    "Base64 encoding is used for data transmission.",
    "The security team implements XML parsing for configuration.",
    "HTML rendering is used for user interface display.",
    "Python scripts are used for automation tasks.",
    "The analysis involves finding relevant information.",
    "The system extracts data from various sources.",
    "The process requires checking and verifying results.",
    
    # REPOSITORY false positives
    "The API endpoint handles user requests properly.",
    "The system processes log files for analysis.",
    "The application uses configuration files for settings.",
    "The security team reviews access logs regularly.",
    "The system monitors application performance continuously.",
    
    # DATE false positives
    "The system processes files in the directory structure.",
    "The application uses configuration paths for settings.",
    "The security team reviews system logs for analysis.",
    "The process involves checking file permissions.",
    "The system tracks file access patterns.",
    
    # DOMAIN/EMAIL false positives
    "The security team reviews access patterns regularly.",
    "The system monitors user activity continuously.",
    "The application processes authentication requests.",
    "The security controls verify user permissions.",
    "The system tracks login attempts effectively.",
]

def add_negative_examples_to_file(file_path: Path, count: int):
    """Add negative examples to a JSONL file."""
    examples = []
    
    # Combine templates
    all_templates = NEGATIVE_TEMPLATES + SPECIFIC_NEGATIVES
    
    # Select random templates
    selected = random.sample(all_templates, min(count, len(all_templates)))
    
    for text in selected:
        examples.append({
            "text": text,
            "entities": []  # No entities - this is a negative example
        })
    
    if examples:
        with open(file_path, 'a', encoding='utf-8') as f:
            for example in examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    return len(examples)

def main():
    base_dir = Path("entities-intent")
    
    print("="*80)
    print("ADD NEGATIVE EXAMPLES")
    print("="*80)
    print("\nAdding sentences with NO entities to help model learn boundaries.")
    print("This reduces false positives by teaching what NOT to extract.")
    print()
    
    # Target: 500-1000 negative examples (2-4% of training data)
    target_total = 800
    examples_per_file = 30  # Distribute across files
    
    total_added = 0
    files_processed = 0
    
    # Process all entity files
    for pillar_dir in sorted(base_dir.iterdir()):
        if pillar_dir.is_dir() and not pillar_dir.name.startswith('.'):
            entity_file = pillar_dir / f"{pillar_dir.name}_entities.jsonl"
            if entity_file.exists():
                print(f"📝 Processing {pillar_dir.name}...")
                added = add_negative_examples_to_file(entity_file, examples_per_file)
                total_added += added
                files_processed += 1
                print(f"   ✅ Added {added} negative examples")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Files processed: {files_processed}")
    print(f"Total negative examples added: {total_added}")
    print(f"Target: {target_total}")
    print(f"Coverage: {total_added/target_total*100:.1f}%")
    print("="*80)

if __name__ == "__main__":
    main()
