#!/usr/bin/env python3
"""
Add GitHub-related intent examples to intent JSONL files.
"""

import json
import random
from pathlib import Path
from typing import List, Dict

# GitHub-related intents
GITHUB_INTENTS = [
    'ANALYZE_GITHUB_REPO',
    'SCAN_GITHUB_REPO',
    'MONITOR_GITHUB_REPO',
    'CLONE_GITHUB_REPO',
    'INVESTIGATE_GITHUB_USER',
    'TRACK_GITHUB_COMMITS',
    'REVIEW_GITHUB_CODE',
    'DETECT_GITHUB_VULNERABILITIES',
    'ANALYZE_GITHUB_ISSUES',
    'MONITOR_GITHUB_ACTIVITY',
    'EXTRACT_GITHUB_INTELLIGENCE',
    'SEARCH_GITHUB_REPOS',
    'ANALYZE_GITHUB_ORGANIZATION',
    'TRACK_GITHUB_RELEASES',
    'MONITOR_GITHUB_BRANCHES',
    'ANALYZE_GITHUB_GISTS',
    'DETECT_GITHUB_EXPLOITS',
    'REVIEW_GITHUB_PULL_REQUESTS',
    'ANALYZE_GITHUB_COMMITS',
    'TRACK_GITHUB_TAGS',
]

# Intent examples with context
INTENT_EXAMPLES = {
    'ANALYZE_GITHUB_REPO': [
        "Analyze the GitHub repository for security vulnerabilities",
        "Review the repository code for potential threats",
        "Examine the GitHub repo for malicious code",
        "Investigate the repository for security issues",
        "Scan the GitHub repository for vulnerabilities",
    ],
    'SCAN_GITHUB_REPO': [
        "Scan the GitHub repository for security vulnerabilities",
        "Perform security scan on the repository",
        "Run vulnerability scan on GitHub repo",
        "Scan repository for exposed secrets",
        "Check repository for security issues",
    ],
    'MONITOR_GITHUB_REPO': [
        "Monitor the GitHub repository for changes",
        "Track repository activity and updates",
        "Watch for new commits in the repository",
        "Monitor repository for suspicious activity",
        "Keep track of repository changes",
    ],
    'CLONE_GITHUB_REPO': [
        "Clone the GitHub repository for analysis",
        "Download the repository for investigation",
        "Get a copy of the repository",
        "Clone repo for security review",
        "Download repository code",
    ],
    'INVESTIGATE_GITHUB_USER': [
        "Investigate the GitHub user's repositories",
        "Analyze user's GitHub activity",
        "Review user's GitHub profile",
        "Examine user's repository contributions",
        "Check user's GitHub account",
    ],
    'TRACK_GITHUB_COMMITS': [
        "Track commits in the repository",
        "Monitor repository commit history",
        "Follow commit activity in repo",
        "Track changes in repository commits",
        "Monitor commit patterns",
    ],
    'REVIEW_GITHUB_CODE': [
        "Review the GitHub repository code",
        "Examine code in the repository",
        "Analyze source code in repo",
        "Review repository codebase",
        "Check code quality in repository",
    ],
    'DETECT_GITHUB_VULNERABILITIES': [
        "Detect vulnerabilities in GitHub repository",
        "Find security issues in repo",
        "Identify vulnerabilities in code",
        "Check for security flaws in repository",
        "Detect security vulnerabilities",
    ],
    'ANALYZE_GITHUB_ISSUES': [
        "Analyze GitHub issues for security concerns",
        "Review repository issues",
        "Examine GitHub issue discussions",
        "Check issues for vulnerability disclosures",
        "Analyze issue comments for threats",
    ],
    'MONITOR_GITHUB_ACTIVITY': [
        "Monitor GitHub activity for threats",
        "Track repository activity patterns",
        "Watch for suspicious GitHub activity",
        "Monitor user activity on GitHub",
        "Track GitHub organization activity",
    ],
    'EXTRACT_GITHUB_INTELLIGENCE': [
        "Extract threat intelligence from GitHub",
        "Gather OSINT from GitHub repositories",
        "Collect intelligence from GitHub",
        "Extract security information from repo",
        "Gather threat data from GitHub",
    ],
    'SEARCH_GITHUB_REPOS': [
        "Search GitHub repositories for keywords",
        "Find repositories related to threat",
        "Search for specific code patterns",
        "Look for repositories with vulnerabilities",
        "Search GitHub for security tools",
    ],
    'ANALYZE_GITHUB_ORGANIZATION': [
        "Analyze GitHub organization repositories",
        "Review organization's security practices",
        "Examine organization's codebase",
        "Check organization for vulnerabilities",
        "Analyze org's repository security",
    ],
    'TRACK_GITHUB_RELEASES': [
        "Track GitHub repository releases",
        "Monitor new releases in repository",
        "Follow repository release updates",
        "Track version releases",
        "Monitor release activity",
    ],
    'MONITOR_GITHUB_BRANCHES': [
        "Monitor repository branches for changes",
        "Track branch activity",
        "Watch for new branches",
        "Monitor branch commits",
        "Track branch development",
    ],
    'ANALYZE_GITHUB_GISTS': [
        "Analyze GitHub gists for threats",
        "Review gist code for vulnerabilities",
        "Examine gist content",
        "Check gists for sensitive data",
        "Analyze gist for security issues",
    ],
    'DETECT_GITHUB_EXPLOITS': [
        "Detect exploit code in GitHub",
        "Find exploit repositories",
        "Identify exploit code patterns",
        "Detect malicious exploits in repo",
        "Find exploit development code",
    ],
    'REVIEW_GITHUB_PULL_REQUESTS': [
        "Review pull requests for security",
        "Examine PR changes for vulnerabilities",
        "Check pull requests for threats",
        "Review PR code changes",
        "Analyze pull request security",
    ],
    'ANALYZE_GITHUB_COMMITS': [
        "Analyze repository commits for threats",
        "Review commit history for security",
        "Examine commits for vulnerabilities",
        "Check commits for malicious code",
        "Analyze commit patterns",
    ],
    'TRACK_GITHUB_TAGS': [
        "Track repository tags and versions",
        "Monitor tag releases",
        "Follow version tags",
        "Track tag updates",
        "Monitor repository versioning",
    ],
}

def generate_intent_examples(intent_type: str, count: int) -> List[Dict]:
    """Generate intent examples."""
    examples = []
    base_examples = INTENT_EXAMPLES.get(intent_type, [f"Perform {intent_type.lower().replace('_', ' ')}"])
    
    for i in range(count):
        text = random.choice(base_examples)
        # Add some variation
        if random.random() < 0.3:
            text = text.replace("the", "a").replace("repository", "repo")
        if random.random() < 0.3:
            text = text.replace("GitHub", "github")
        
        examples.append({
            'text': text,
            'intents': {intent_type: 1.0}
        })
    
    return examples

def add_to_file(file_path: Path, examples: List[Dict]):
    """Add examples to a file."""
    with open(file_path, 'a', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

def main():
    """Main function."""
    base_dir = Path('cyber-train/entities-intent')
    if not base_dir.exists():
        base_dir = Path('entities-intent')
    
    intent_files = list(base_dir.rglob('*_intent.jsonl'))
    file_map = {f.name: f for f in intent_files}
    
    # Target files for GitHub intents
    target_files = {
        'ANALYZE_GITHUB_REPO': [
            'cybint_intent.jsonl',
            'threat_intel_intent.jsonl',
            'incident_response_intent.jsonl',
            'application_security_intent.jsonl',
        ],
        'SCAN_GITHUB_REPO': [
            'vulnerability_mgmt_intent.jsonl',
            'application_security_intent.jsonl',
            'cybint_intent.jsonl',
        ],
        'MONITOR_GITHUB_REPO': [
            'threat_intel_intent.jsonl',
            'cybint_intent.jsonl',
            'incident_response_intent.jsonl',
        ],
        'CLONE_GITHUB_REPO': [
            'cybint_intent.jsonl',
            'incident_response_intent.jsonl',
            'application_security_intent.jsonl',
        ],
        'INVESTIGATE_GITHUB_USER': [
            'cybint_intent.jsonl',
            'socmint_intent.jsonl',
            'humint_intent.jsonl',
            'threat_intel_intent.jsonl',
        ],
        'TRACK_GITHUB_COMMITS': [
            'application_security_intent.jsonl',
            'vulnerability_mgmt_intent.jsonl',
            'incident_response_intent.jsonl',
        ],
        'REVIEW_GITHUB_CODE': [
            'application_security_intent.jsonl',
            'vulnerability_mgmt_intent.jsonl',
        ],
        'DETECT_GITHUB_VULNERABILITIES': [
            'vulnerability_mgmt_intent.jsonl',
            'application_security_intent.jsonl',
            'cybint_intent.jsonl',
        ],
        'ANALYZE_GITHUB_ISSUES': [
            'vulnerability_mgmt_intent.jsonl',
            'application_security_intent.jsonl',
        ],
        'MONITOR_GITHUB_ACTIVITY': [
            'threat_intel_intent.jsonl',
            'cybint_intent.jsonl',
            'incident_response_intent.jsonl',
        ],
        'EXTRACT_GITHUB_INTELLIGENCE': [
            'cybint_intent.jsonl',
            'threat_intel_intent.jsonl',
        ],
        'SEARCH_GITHUB_REPOS': [
            'cybint_intent.jsonl',
            'threat_intel_intent.jsonl',
        ],
        'ANALYZE_GITHUB_ORGANIZATION': [
            'cybint_intent.jsonl',
            'threat_intel_intent.jsonl',
        ],
        'TRACK_GITHUB_RELEASES': [
            'vulnerability_mgmt_intent.jsonl',
            'application_security_intent.jsonl',
        ],
        'MONITOR_GITHUB_BRANCHES': [
            'application_security_intent.jsonl',
            'vulnerability_mgmt_intent.jsonl',
        ],
        'ANALYZE_GITHUB_GISTS': [
            'cybint_intent.jsonl',
            'threat_intel_intent.jsonl',
        ],
        'DETECT_GITHUB_EXPLOITS': [
            'cybint_intent.jsonl',
            'threat_intel_intent.jsonl',
            'incident_response_intent.jsonl',
        ],
        'REVIEW_GITHUB_PULL_REQUESTS': [
            'application_security_intent.jsonl',
            'vulnerability_mgmt_intent.jsonl',
        ],
        'ANALYZE_GITHUB_COMMITS': [
            'application_security_intent.jsonl',
            'incident_response_intent.jsonl',
        ],
        'TRACK_GITHUB_TAGS': [
            'vulnerability_mgmt_intent.jsonl',
            'application_security_intent.jsonl',
        ],
    }
    
    print("="*80)
    print("ADDING GITHUB INTENT EXAMPLES")
    print("="*80)
    
    total_added = {}
    
    for intent_type in GITHUB_INTENTS:
        if intent_type not in target_files:
            continue
        
        print(f"\n{'='*80}")
        print(f"Adding {intent_type} examples")
        print(f"{'='*80}")
        
        files_for_intent = target_files[intent_type]
        examples_per_file = 20  # 20 examples per file
        total_count = len(files_for_intent) * examples_per_file
        
        examples = generate_intent_examples(intent_type, total_count)
        
        added_count = 0
        for i, filename in enumerate(files_for_intent):
            if filename not in file_map:
                print(f"  ⚠️  File not found: {filename}")
                continue
            file_path = file_map[filename]
            
            file_examples = examples[added_count:added_count + examples_per_file]
            add_to_file(file_path, file_examples)
            added_count += len(file_examples)
            print(f"  ✅ Added {len(file_examples)} examples to {file_path.name}")
        
        total_added[intent_type] = added_count
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    for intent_type, count in total_added.items():
        print(f"  {intent_type}: {count} examples added")
    
    print(f"\n✅ Total intent examples added: {sum(total_added.values())}")

if __name__ == '__main__':
    main()

