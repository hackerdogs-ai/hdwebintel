#!/usr/bin/env python3
"""
Analyze and consolidate entity types to reduce complexity and improve generalization.

The model currently has 573 entity types, which is excessive and causes:
- Class imbalance
- Confusion between similar types
- Poor generalization

This script analyzes entity type usage and suggests consolidation strategies.
"""

import json
import srsly
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set


class EntityTypeConsolidator:
    """Analyzes and consolidates entity types."""
    
    # Consolidation rules: merge these types into parent types
    CONSOLIDATION_MAP = {
        # IP addresses
        'IPV4_ADDRESS': 'IP_ADDRESS',
        'IPV6_ADDRESS': 'IP_ADDRESS',
        'IP': 'IP_ADDRESS',
        
        # Hashes
        'MD5_HASH': 'HASH',
        'SHA1_HASH': 'HASH',
        'SHA256_HASH': 'HASH',
        'SHA512_HASH': 'HASH',
        'FILE_HASH': 'HASH',
        
        # URLs and domains
        'MALICIOUS_URL': 'URL',
        'PHISHING_URL': 'URL',
        'HTTP_URL': 'URL',
        'HTTPS_URL': 'URL',
        
        # Email
        'PHISHING_EMAIL': 'EMAIL_ADDRESS',
        'EMAIL': 'EMAIL_ADDRESS',
        
        # Vulnerabilities
        'CVE': 'CVE_ID',
        'VULNERABILITY_ID': 'CVE_ID',
        
        # Ports
        'PORT_NUMBER': 'PORT',
        'TCP_PORT': 'PORT',
        'UDP_PORT': 'PORT',
        'PORT_TYPE': 'PORT',
        
        # Files
        'MALICIOUS_FILE': 'FILE_PATH',
        'FILE_NAME': 'FILE_PATH',
        'EXECUTABLE': 'FILE_PATH',
        
        # Organizations
        'COMPANY': 'ORGANIZATION',
        'VENDOR': 'ORGANIZATION',
        'CORPORATION': 'ORGANIZATION',
        
        # Locations
        'COUNTRY': 'LOCATION',
        'CITY': 'LOCATION',
        'REGION': 'LOCATION',
        'REGION_TYPE': 'LOCATION',
        
        # Malware variants
        'RANSOMWARE': 'MALWARE_TYPE',
        'TROJAN': 'MALWARE_TYPE',
        'VIRUS': 'MALWARE_TYPE',
        'WORM': 'MALWARE_TYPE',
        'BACKDOOR': 'MALWARE_TYPE',
        
        # Tools
        'SECURITY_TOOL': 'TOOL',
        'HACKING_TOOL': 'TOOL',
        'PENETRATION_TESTING_TOOL': 'TOOL',
        
        # Protocols
        'HTTP': 'PROTOCOL_TYPE',
        'HTTPS': 'PROTOCOL_TYPE',
        'FTP': 'PROTOCOL_TYPE',
        'SSH': 'PROTOCOL_TYPE',
        'TELNET': 'PROTOCOL_TYPE',
        'PROTOCOL': 'PROTOCOL_TYPE',
        
        # Time
        'DATETIME': 'DATE',
        'TIMESTAMP': 'DATE',
        'TIME_TYPE': 'TIME',
        'YEAR_TYPE': 'YEAR',
        
        # Accounts
        'ACCOUNT_NAME': 'ACCOUNT_TYPE',
        
        # AI Models
        'AI_MODEL': 'AI_MODEL_TYPE',
        
        # Applications
        'APPLICATION_NAME': 'APPLICATION_TYPE',
        
        # Builds
        'BUILD_ID': 'BUILD_TYPE',
        
        # Currency
        'CURRENCY_TYPE': 'CURRENCY',
        
        # Data
        'DATA': 'DATA_TYPE',
        
        # Frameworks
        'FRAMEWORK_TYPE': 'FRAMEWORK',
        
        # Images
        'IMAGE_NAME': 'IMAGE_TYPE',
        
        # Incidents
        'INCIDENT_ID': 'INCIDENT_TYPE',
        
        # Issues
        'ISSUE_TYPE': 'ISSUE_ID',
        
        # Libraries
        'LIBRARY_NAME': 'LIBRARY_TYPE',
        
        # Models
        'MODEL': 'MODEL_TYPE',
        
        # Platforms
        'PLATFORM': 'PLATFORM_TYPE',
        
        # Pods
        'POD_NAME': 'POD_TYPE',
        
        # Projects
        'PROJECT_NAME': 'PROJECT_TYPE',
        
        # Records
        'RECORD': 'RECORD_TYPE',
        
        # Repositories
        'REPOSITORY_TYPE': 'REPOSITORY',
        
        # Roles
        'ROLE_TYPE': 'ROLE',
        
        # Servers
        'SERVER_NAME': 'SERVER_TYPE',
        
        # Severity
        'SEVERITY': 'SEVERITY_TYPE',
        
        # Source
        'SOURCE': 'SOURCE_TYPE',
        
        # Status
        'STATUS': 'STATUS_TYPE',
        
        # Vendors
        'VENDOR_NAME': 'VENDOR_TYPE',
        'VENDOR_ID': 'VENDOR_TYPE',
        
        # Vulnerabilities
        'VULNERABILITY_TYPE': 'VULNERABILITY_ID',
    }
    
    def __init__(self, base_dir: str = "entities-intent"):
        """
        Initialize consolidator.
        
        Args:
            base_dir: Base directory containing entity training files
        """
        self.base_dir = Path(base_dir)
        self.entity_stats = defaultdict(int)
        self.entity_examples = defaultdict(list)
        self.file_stats = defaultdict(lambda: defaultdict(int))
    
    def analyze_entity_types(self):
        """Analyze all entity types in training data."""
        print("="*70)
        print("ENTITY TYPE ANALYSIS")
        print("="*70)
        
        # Find all JSONL files
        jsonl_files = list(self.base_dir.glob("**/*_entities.jsonl"))
        
        print(f"\n📂 Found {len(jsonl_files)} entity files")
        print("\n🔍 Analyzing entity type distribution...")
        
        for file_path in jsonl_files:
            self._analyze_file(file_path)
        
        self._print_stats()
        self._suggest_consolidations()
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single JSONL file."""
        try:
            for line in srsly.read_jsonl(file_path):
                if 'entities' in line:
                    for start, end, entity_type in line['entities']:
                        self.entity_stats[entity_type] += 1
                        self.file_stats[file_path.name][entity_type] += 1
                        
                        # Store examples for rare types
                        if len(self.entity_examples[entity_type]) < 5:
                            entity_text = line['text'][start:end]
                            self.entity_examples[entity_type].append(
                                (entity_text, line['text'])
                            )
        except Exception as e:
            print(f"⚠️  Error reading {file_path.name}: {e}")
    
    def _print_stats(self):
        """Print entity type statistics."""
        print(f"\n📊 Entity Type Statistics:")
        print(f"   Total unique types: {len(self.entity_stats)}")
        print(f"   Total entity mentions: {sum(self.entity_stats.values())}")
        
        # Sort by frequency
        sorted_types = sorted(self.entity_stats.items(), 
                             key=lambda x: x[1], reverse=True)
        
        # Top 20 most frequent
        print("\n🔝 Top 20 Most Frequent Entity Types:")
        for i, (entity_type, count) in enumerate(sorted_types[:20], 1):
            print(f"   {i:2d}. {entity_type:40s} {count:6d} mentions")
        
        # Bottom 20 least frequent
        print("\n⚠️  Bottom 20 Least Frequent Entity Types:")
        for i, (entity_type, count) in enumerate(sorted_types[-20:], 1):
            example = self.entity_examples[entity_type][0][0] if entity_type in self.entity_examples else "N/A"
            print(f"   {i:2d}. {entity_type:40s} {count:6d} mentions  Example: {example[:30]}")
        
        # Distribution analysis
        print("\n📈 Distribution Analysis:")
        buckets = {
            '1-10': 0,
            '11-50': 0,
            '51-100': 0,
            '101-500': 0,
            '501-1000': 0,
            '1000+': 0
        }
        
        for count in self.entity_stats.values():
            if count <= 10:
                buckets['1-10'] += 1
            elif count <= 50:
                buckets['11-50'] += 1
            elif count <= 100:
                buckets['51-100'] += 1
            elif count <= 500:
                buckets['101-500'] += 1
            elif count <= 1000:
                buckets['501-1000'] += 1
            else:
                buckets['1000+'] += 1
        
        for bucket, count in buckets.items():
            pct = (count / len(self.entity_stats)) * 100
            print(f"   {bucket:15s} examples: {count:4d} types ({pct:5.1f}%)")
    
    def _suggest_consolidations(self):
        """Suggest entity type consolidations."""
        print("\n" + "="*70)
        print("CONSOLIDATION SUGGESTIONS")
        print("="*70)
        
        # Apply consolidation map
        consolidated_stats = defaultdict(int)
        consolidation_count = defaultdict(int)
        
        for entity_type, count in self.entity_stats.items():
            parent_type = self.CONSOLIDATION_MAP.get(entity_type, entity_type)
            consolidated_stats[parent_type] += count
            
            if parent_type != entity_type:
                consolidation_count[parent_type] += 1
        
        # Show consolidation results
        print(f"\n📉 Consolidation Results:")
        print(f"   Before: {len(self.entity_stats)} entity types")
        print(f"   After:  {len(consolidated_stats)} entity types")
        print(f"   Reduction: {len(self.entity_stats) - len(consolidated_stats)} types ({((len(self.entity_stats) - len(consolidated_stats)) / len(self.entity_stats) * 100):.1f}%)")
        
        # Show merged types
        print("\n🔄 Types to Merge:")
        for parent_type, num_merged in sorted(consolidation_count.items(), 
                                              key=lambda x: x[1], reverse=True):
            if num_merged > 0:
                child_types = [k for k, v in self.CONSOLIDATION_MAP.items() if v == parent_type]
                print(f"\n   {parent_type}:")
                print(f"      Merging {num_merged} types:")
                for child_type in child_types:
                    if child_type in self.entity_stats:
                        count = self.entity_stats[child_type]
                        print(f"         - {child_type} ({count} mentions)")
        
        # Identify similar types
        print("\n🔍 Potential Additional Consolidations:")
        self._find_similar_types()
    
    def _find_similar_types(self):
        """Find similar entity types that could be consolidated."""
        similar_groups = defaultdict(list)
        
        for entity_type in self.entity_stats.keys():
            # Extract base name (remove prefixes/suffixes)
            base = entity_type.lower()
            
            # Common patterns
            if '_type' in base:
                base = base.replace('_type', '')
            if '_id' in base:
                base = base.replace('_id', '')
            if '_name' in base:
                base = base.replace('_name', '')
            
            similar_groups[base].append(entity_type)
        
        # Print groups with multiple types
        for base, types in sorted(similar_groups.items()):
            if len(types) > 1:
                total_mentions = sum(self.entity_stats[t] for t in types)
                print(f"\n   Group '{base}' ({len(types)} types, {total_mentions} mentions):")
                for t in types:
                    print(f"      - {t} ({self.entity_stats[t]} mentions)")
    
    def apply_consolidations(self, dry_run: bool = True):
        """Apply consolidations to training data."""
        print("\n" + "="*70)
        if dry_run:
            print("DRY RUN - NO CHANGES WILL BE MADE")
        else:
            print("APPLYING CONSOLIDATIONS")
        print("="*70)
        
        jsonl_files = list(self.base_dir.glob("**/*_entities.jsonl"))
        
        for file_path in jsonl_files:
            self._consolidate_file(file_path, dry_run)
        
        if not dry_run:
            print("\n✅ Consolidation complete!")
            print("\n⚠️  Next steps:")
            print("   1. Review the changes")
            print("   2. Re-prepare training data: python3 prepare_spacy_training.py")
            print("   3. Retrain model: python3 train_spacy_models.py")
    
    def _consolidate_file(self, file_path: Path, dry_run: bool):
        """Consolidate entity types in a single file."""
        changes = 0
        
        if dry_run:
            # Just count changes
            for line in srsly.read_jsonl(file_path):
                if 'entities' in line:
                    for start, end, entity_type in line['entities']:
                        if entity_type in self.CONSOLIDATION_MAP:
                            changes += 1
            
            if changes > 0:
                print(f"   {file_path.name}: {changes} entities would be consolidated")
        else:
            # Apply changes
            updated_lines = []
            for line in srsly.read_jsonl(file_path):
                if 'entities' in line:
                    updated_entities = []
                    for start, end, entity_type in line['entities']:
                        # Apply consolidation map
                        new_type = self.CONSOLIDATION_MAP.get(entity_type, entity_type)
                        updated_entities.append([start, end, new_type])
                        if new_type != entity_type:
                            changes += 1
                    line['entities'] = updated_entities
                updated_lines.append(line)
            
            # Write back
            if changes > 0:
                srsly.write_jsonl(file_path, updated_lines)
                print(f"   ✅ {file_path.name}: Consolidated {changes} entities")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze and consolidate entity types")
    parser.add_argument('--base-dir', default='entities-intent',
                       help='Base directory containing entity files')
    parser.add_argument('--apply', action='store_true',
                       help='Apply consolidations (default is dry-run)')
    
    args = parser.parse_args()
    
    consolidator = EntityTypeConsolidator(base_dir=args.base_dir)
    
    # Analyze
    consolidator.analyze_entity_types()
    
    # Apply (or dry-run)
    consolidator.apply_consolidations(dry_run=not args.apply)


if __name__ == "__main__":
    main()

