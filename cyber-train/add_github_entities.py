#!/usr/bin/env python3
"""
Add GitHub-related entities:
- GitHub repository names
- GitHub repository URLs
- GitHub usernames
- GitHub organizations
- GitHub gists
- GitHub issues
- GitHub pull requests
- GitHub commits
- GitHub branches
- GitHub tags
- GitHub releases
"""

import json
import re
import random
from pathlib import Path
from typing import List, Dict

# Patterns
GITHUB_REPO_PATTERN = re.compile(r'[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+')
GITHUB_URL_PATTERN = re.compile(r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(?:/[a-zA-Z0-9_.-]+)*')
GITHUB_USER_PATTERN = re.compile(r'@?[a-zA-Z0-9]([a-zA-Z0-9]|-(?![.-])){0,38}')
GITHUB_GIST_PATTERN = re.compile(r'https?://gist\.github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9]+')
GITHUB_ISSUE_PATTERN = re.compile(r'#[0-9]+')
GITHUB_COMMIT_PATTERN = re.compile(r'[a-f0-9]{7,40}')
GITHUB_BRANCH_PATTERN = re.compile(r'[a-zA-Z0-9_.-]+')
GITHUB_TAG_PATTERN = re.compile(r'v?\d+\.\d+(?:\.\d+)?(?:-[a-zA-Z0-9]+)?')

# Common GitHub usernames and orgs for examples
GITHUB_USERS = ['octocat', 'torvalds', 'gaearon', 'tj', 'defunkt', 'mojombo', 'pjhyatt', 'wycats', 'ezmobius', 'brynary']
GITHUB_ORGS = ['microsoft', 'google', 'facebook', 'apple', 'netflix', 'uber', 'airbnb', 'twitter', 'github', 'docker']

def generate_github_repo_examples(count: int) -> List[Dict]:
    """Generate GitHub repository examples."""
    examples = []
    repo_names = ['awesome-project', 'security-tool', 'vulnerability-scanner', 'osint-framework', 
                  'threat-intel', 'malware-analysis', 'pentest-toolkit', 'forensics-tool']
    
    for i in range(count):
        user = random.choice(GITHUB_USERS + GITHUB_ORGS)
        repo = random.choice(repo_names)
        repo_full = f"{user}/{repo}"
        
        contexts = [
            f"Repository {repo_full} contains sensitive data",
            f"Clone {repo_full} for analysis",
            f"Repo {repo_full} flagged for security issues",
            f"Monitor {repo_full} for updates",
            f"Repository {repo_full} under investigation",
            f"Scan {repo_full} for vulnerabilities",
            f"Repo {repo_full} linked to threat actor",
            f"Analyze {repo_full} source code",
            f"Repository {repo_full} contains malware",
            f"Check {repo_full} commit history"
        ]
        text = random.choice(contexts)
        match = GITHUB_REPO_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'GITHUB_REPO']]
            })
    return examples

def generate_github_url_examples(count: int) -> List[Dict]:
    """Generate GitHub URL examples."""
    examples = []
    repo_names = ['awesome-project', 'security-tool', 'vulnerability-scanner', 'osint-framework']
    paths = ['', '/tree/main', '/blob/main/README.md', '/issues', '/pulls', '/releases']
    
    for i in range(count):
        user = random.choice(GITHUB_USERS + GITHUB_ORGS)
        repo = random.choice(repo_names)
        path = random.choice(paths)
        url = f"https://github.com/{user}/{repo}{path}"
        
        contexts = [
            f"Repository URL {url} under investigation",
            f"Monitor {url} for suspicious activity",
            f"URL {url} linked to threat actor",
            f"Clone from {url}",
            f"Repository {url} contains vulnerabilities",
            f"Scan {url} for security issues",
            f"URL {url} flagged",
            f"Analyze {url} source code",
            f"Repository {url} associated with attack",
            f"Check {url} commit history"
        ]
        text = random.choice(contexts)
        match = GITHUB_URL_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'GITHUB_REPO_URL']]
            })
    return examples

def generate_github_user_examples(count: int) -> List[Dict]:
    """Generate GitHub username examples."""
    examples = []
    
    for i in range(count):
        user = random.choice(GITHUB_USERS)
        # Sometimes with @, sometimes without
        username = f"@{user}" if random.random() < 0.5 else user
        
        contexts = [
            f"GitHub user {username} under investigation",
            f"Monitor {username} repositories",
            f"User {username} linked to threat actor",
            f"Profile {username} flagged",
            f"GitHub account {username} suspicious",
            f"User {username} repositories analyzed",
            f"Account {username} associated with attack",
            f"Profile {username} under review",
            f"GitHub user {username} in contact list",
            f"Account {username} verified"
        ]
        text = random.choice(contexts)
        # Find username in text
        idx = text.find(username)
        if idx != -1:
            examples.append({
                'text': text,
                'entities': [[idx, idx + len(username), 'GITHUB_USER']]
            })
    return examples

def generate_github_org_examples(count: int) -> List[Dict]:
    """Generate GitHub organization examples."""
    examples = []
    
    for i in range(count):
        org = random.choice(GITHUB_ORGS)
        
        contexts = [
            f"GitHub organization {org} repositories scanned",
            f"Monitor {org} organization activity",
            f"Org {org} linked to security research",
            f"Organization {org} repositories analyzed",
            f"GitHub org {org} under investigation",
            f"Monitor {org} for security updates",
            f"Organization {org} flagged",
            f"GitHub org {org} repositories reviewed",
            f"Org {org} associated with threat intelligence",
            f"Organization {org} verified"
        ]
        text = random.choice(contexts)
        idx = text.find(org)
        if idx != -1:
            examples.append({
                'text': text,
                'entities': [[idx, idx + len(org), 'GITHUB_ORGANIZATION']]
            })
    return examples

def generate_github_gist_examples(count: int) -> List[Dict]:
    """Generate GitHub gist examples."""
    examples = []
    
    for i in range(count):
        user = random.choice(GITHUB_USERS)
        gist_id = ''.join(random.choices('0123456789abcdef', k=32))
        gist_url = f"https://gist.github.com/{user}/{gist_id}"
        
        contexts = [
            f"Gist {gist_url} contains sensitive code",
            f"Analyze gist {gist_url}",
            f"Gist {gist_url} flagged for security issues",
            f"Monitor {gist_url} for changes",
            f"Gist {gist_url} under investigation",
            f"Review {gist_url} content",
            f"Gist {gist_url} linked to threat",
            f"Check {gist_url} for vulnerabilities",
            f"Gist {gist_url} contains malware",
            f"Analyze {gist_url} code"
        ]
        text = random.choice(contexts)
        match = GITHUB_GIST_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'GITHUB_GIST']]
            })
    return examples

def generate_github_issue_examples(count: int) -> List[Dict]:
    """Generate GitHub issue examples."""
    examples = []
    
    for i in range(count):
        issue_num = random.randint(1, 9999)
        issue_ref = f"#{issue_num}"
        
        contexts = [
            f"Issue {issue_ref} contains vulnerability details",
            f"Monitor issue {issue_ref}",
            f"Issue {issue_ref} flagged for security",
            f"Review {issue_ref} for sensitive data",
            f"Issue {issue_ref} under investigation",
            f"Check {issue_ref} for disclosure",
            f"Issue {issue_ref} linked to threat",
            f"Analyze {issue_ref} comments",
            f"Issue {issue_ref} contains exploit code",
            f"Review {issue_ref} content"
        ]
        text = random.choice(contexts)
        match = GITHUB_ISSUE_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'GITHUB_ISSUE']]
            })
    return examples

def generate_github_commit_examples(count: int) -> List[Dict]:
    """Generate GitHub commit hash examples."""
    examples = []
    
    for i in range(count):
        commit_hash = ''.join(random.choices('0123456789abcdef', k=random.choice([7, 8, 40])))
        
        contexts = [
            f"Commit {commit_hash} contains malicious code",
            f"Analyze commit {commit_hash}",
            f"Commit {commit_hash} flagged for review",
            f"Check {commit_hash} changes",
            f"Commit {commit_hash} under investigation",
            f"Review {commit_hash} diff",
            f"Commit {commit_hash} linked to attack",
            f"Examine {commit_hash} modifications",
            f"Commit {commit_hash} contains backdoor",
            f"Analyze {commit_hash} changes"
        ]
        text = random.choice(contexts)
        match = GITHUB_COMMIT_PATTERN.search(text)
        if match:
            examples.append({
                'text': text,
                'entities': [[match.start(), match.end(), 'GITHUB_COMMIT']]
            })
    return examples

def generate_github_branch_examples(count: int) -> List[Dict]:
    """Generate GitHub branch examples."""
    examples = []
    branch_names = ['main', 'master', 'develop', 'feature/security', 'hotfix/vuln', 'release/v1.0']
    
    for i in range(count):
        branch = random.choice(branch_names)
        
        contexts = [
            f"Branch {branch} contains sensitive data",
            f"Check branch {branch} for vulnerabilities",
            f"Branch {branch} flagged for review",
            f"Monitor {branch} commits",
            f"Branch {branch} under investigation",
            f"Review {branch} changes",
            f"Branch {branch} linked to threat",
            f"Analyze {branch} code",
            f"Branch {branch} contains malware",
            f"Check {branch} for security issues"
        ]
        text = random.choice(contexts)
        idx = text.find(branch)
        if idx != -1:
            examples.append({
                'text': text,
                'entities': [[idx, idx + len(branch), 'GITHUB_BRANCH']]
            })
    return examples

def generate_github_tag_examples(count: int) -> List[Dict]:
    """Generate GitHub tag examples."""
    examples = []
    tag_formats = ['v1.0.0', 'v2.1.3', '1.0.0', '2.1.3', 'v1.0.0-beta', 'v2.0.0-rc1']
    
    for i in range(count):
        tag = random.choice(tag_formats)
        
        contexts = [
            f"Tag {tag} contains vulnerabilities",
            f"Check tag {tag} for security issues",
            f"Tag {tag} flagged for review",
            f"Monitor {tag} release",
            f"Tag {tag} under investigation",
            f"Review {tag} changes",
            f"Tag {tag} linked to threat",
            f"Analyze {tag} code",
            f"Tag {tag} contains backdoor",
            f"Check {tag} for exploits"
        ]
        text = random.choice(contexts)
        idx = text.find(tag)
        if idx != -1:
            examples.append({
                'text': text,
                'entities': [[idx, idx + len(tag), 'GITHUB_TAG']]
            })
    return examples

def generate_github_release_examples(count: int) -> List[Dict]:
    """Generate GitHub release examples."""
    examples = []
    release_names = ['v1.0.0', 'v2.1.3', 'Security Update', 'Critical Patch', 'v1.0.0-beta']
    
    for i in range(count):
        release = random.choice(release_names)
        
        contexts = [
            f"Release {release} contains security fixes",
            f"Check release {release} for vulnerabilities",
            f"Release {release} flagged for review",
            f"Monitor {release} downloads",
            f"Release {release} under investigation",
            f"Review {release} changes",
            f"Release {release} linked to threat",
            f"Analyze {release} artifacts",
            f"Release {release} contains backdoor",
            f"Check {release} for exploits"
        ]
        text = random.choice(contexts)
        idx = text.find(release)
        if idx != -1:
            examples.append({
                'text': text,
                'entities': [[idx, idx + len(release), 'GITHUB_RELEASE']]
            })
    return examples

def add_to_file(file_path: Path, examples: List[Dict], entity_type: str):
    """Add examples to a file."""
    with open(file_path, 'a', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

def main():
    """Main function."""
    base_dir = Path('cyber-train/entities-intent')
    if not base_dir.exists():
        base_dir = Path('entities-intent')
    
    entity_files = list(base_dir.rglob('*_entities.jsonl'))
    file_map = {f.name: f for f in entity_files}
    
    # Target files for GitHub entities (cybersecurity and OSINT)
    target_files = {
        'GITHUB_REPO': [
            'cybint_entities.jsonl',
            'threat_intel_entities.jsonl',
            'incident_response_entities.jsonl',
            'application_security_entities.jsonl',
            'vulnerability_mgmt_entities.jsonl',
            'ai_security_entities.jsonl',
        ],
        'GITHUB_REPO_URL': [
            'cybint_entities.jsonl',
            'threat_intel_entities.jsonl',
            'incident_response_entities.jsonl',
            'application_security_entities.jsonl',
            'vulnerability_mgmt_entities.jsonl',
        ],
        'GITHUB_USER': [
            'cybint_entities.jsonl',
            'threat_intel_entities.jsonl',
            'socmint_entities.jsonl',
            'humint_entities.jsonl',
            'incident_response_entities.jsonl',
        ],
        'GITHUB_ORGANIZATION': [
            'cybint_entities.jsonl',
            'threat_intel_entities.jsonl',
            'vulnerability_mgmt_entities.jsonl',
            'application_security_entities.jsonl',
        ],
        'GITHUB_GIST': [
            'cybint_entities.jsonl',
            'threat_intel_entities.jsonl',
            'incident_response_entities.jsonl',
        ],
        'GITHUB_ISSUE': [
            'vulnerability_mgmt_entities.jsonl',
            'application_security_entities.jsonl',
            'incident_response_entities.jsonl',
        ],
        'GITHUB_COMMIT': [
            'application_security_entities.jsonl',
            'vulnerability_mgmt_entities.jsonl',
            'incident_response_entities.jsonl',
        ],
        'GITHUB_BRANCH': [
            'application_security_entities.jsonl',
            'vulnerability_mgmt_entities.jsonl',
        ],
        'GITHUB_TAG': [
            'vulnerability_mgmt_entities.jsonl',
            'application_security_entities.jsonl',
        ],
        'GITHUB_RELEASE': [
            'vulnerability_mgmt_entities.jsonl',
            'application_security_entities.jsonl',
        ],
    }
    
    # Entity generators
    entity_generators = {
        'GITHUB_REPO': (generate_github_repo_examples, 300),
        'GITHUB_REPO_URL': (generate_github_url_examples, 300),
        'GITHUB_USER': (generate_github_user_examples, 200),
        'GITHUB_ORGANIZATION': (generate_github_org_examples, 150),
        'GITHUB_GIST': (generate_github_gist_examples, 150),
        'GITHUB_ISSUE': (generate_github_issue_examples, 200),
        'GITHUB_COMMIT': (generate_github_commit_examples, 200),
        'GITHUB_BRANCH': (generate_github_branch_examples, 150),
        'GITHUB_TAG': (generate_github_tag_examples, 150),
        'GITHUB_RELEASE': (generate_github_release_examples, 150),
    }
    
    print("="*80)
    print("ADDING GITHUB ENTITY EXAMPLES")
    print("="*80)
    
    total_added = {}
    
    for entity_type, (generator_func, total_count) in entity_generators.items():
        print(f"\n{'='*80}")
        print(f"Adding {entity_type} examples ({total_count} total)")
        print(f"{'='*80}")
        
        examples = generator_func(total_count)
        files_for_type = target_files[entity_type]
        examples_per_file = total_count // len(files_for_type)
        remainder = total_count % len(files_for_type)
        
        added_count = 0
        for i, filename in enumerate(files_for_type):
            if filename not in file_map:
                print(f"  ⚠️  File not found: {filename}")
                continue
            file_path = file_map[filename]
            
            count_for_file = examples_per_file + (1 if i < remainder else 0)
            file_examples = examples[added_count:added_count + count_for_file]
            add_to_file(file_path, file_examples, entity_type)
            added_count += len(file_examples)
            print(f"  ✅ Added {len(file_examples)} examples to {file_path.name}")
        
        total_added[entity_type] = added_count
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    for entity_type, count in total_added.items():
        print(f"  {entity_type}: {count} examples added")
    
    print(f"\n✅ Total examples added: {sum(total_added.values())}")

if __name__ == '__main__':
    main()

