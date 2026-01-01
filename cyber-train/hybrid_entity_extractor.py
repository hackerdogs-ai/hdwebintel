#!/usr/bin/env python3
"""
Hybrid entity extractor combining rule-based patterns with ML model.
This addresses the low recall issue by using high-precision rules for pattern-based entities.
"""

import re
import spacy
from typing import List, Tuple, Dict, Set
from pathlib import Path


class HybridEntityExtractor:
    """Combines rule-based extraction with ML-based extraction for better recall."""
    
    # High-precision regex patterns for well-defined entity types
    PATTERNS = {
        'IP_ADDRESS': [
            # IPv4
            r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            # IPv6
            r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b',
            r'\b(?:[0-9a-fA-F]{1,4}:){1,7}:\b',
            r'\b(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}\b',
        ],
        'CVE_ID': [
            r'\bCVE-\d{4}-\d{4,7}\b',
        ],
        'HASH': [
            # MD5 (32 hex chars)
            r'\b[a-fA-F0-9]{32}\b',
            # SHA1 (40 hex chars)
            r'\b[a-fA-F0-9]{40}\b',
            # SHA256 (64 hex chars)
            r'\b[a-fA-F0-9]{64}\b',
        ],
        'EMAIL_ADDRESS': [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        ],
        'PHONE_NUMBER': [
            # US/International formats
            r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'\+[0-9]{1,3}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}',
        ],
        'URL': [
            r'\b(?:https?|ftp)://[^\s/$.?#].[^\s]*\b',
            r'\bwww\.[^\s/$.?#].[^\s]*\b',
        ],
        'DOMAIN': [
            r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b',
        ],
        'SSN': [
            r'\b\d{3}-\d{2}-\d{4}\b',
            r'\b\d{9}\b',  # Without dashes
        ],
        'CREDIT_CARD_NUMBER': [
            # Visa, MasterCard, Amex, Discover patterns
            r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b',
        ],
        'DATE': [
            # YYYY-MM-DD
            r'\b\d{4}-\d{2}-\d{2}\b',
            # MM/DD/YYYY
            r'\b\d{2}/\d{2}/\d{4}\b',
            # DD-MM-YYYY
            r'\b\d{2}-\d{2}-\d{4}\b',
        ],
        'TIME': [
            # HH:MM:SS or HH:MM
            r'\b\d{2}:\d{2}(?::\d{2})?\b',
        ],
    }
    
    def __init__(self, ner_model_path: str = None):
        """
        Initialize hybrid extractor.
        
        Args:
            ner_model_path: Path to spaCy NER model (optional)
        """
        self.ner_model = None
        if ner_model_path:
            model_path = Path(ner_model_path)
            if model_path.exists():
                try:
                    self.ner_model = spacy.load(str(model_path))
                    print(f"✅ Loaded NER model from: {ner_model_path}")
                except Exception as e:
                    print(f"⚠️  Could not load NER model: {e}")
        
        # Compile regex patterns once
        self.compiled_patterns = {}
        for entity_type, patterns in self.PATTERNS.items():
            self.compiled_patterns[entity_type] = [
                re.compile(pattern) for pattern in patterns
            ]
    
    def extract_with_rules(self, text: str) -> List[Tuple[str, str, int, int]]:
        """
        Extract entities using rule-based patterns.
        
        Args:
            text: Input text
            
        Returns:
            List of (entity_text, entity_type, start, end)
        """
        entities = []
        
        for entity_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    entity_text = match.group(0)
                    start = match.start()
                    end = match.end()
                    
                    # Additional validation for specific types
                    if self._validate_entity(entity_text, entity_type):
                        entities.append((entity_text, entity_type, start, end))
        
        return entities
    
    def extract_with_ml(self, text: str) -> List[Tuple[str, str, int, int]]:
        """
        Extract entities using ML model.
        
        Args:
            text: Input text
            
        Returns:
            List of (entity_text, entity_type, start, end)
        """
        if not self.ner_model:
            return []
        
        doc = self.ner_model(text)
        entities = []
        
        for ent in doc.ents:
            entities.append((ent.text, ent.label_, ent.start_char, ent.end_char))
        
        return entities
    
    def extract(self, text: str, use_rules: bool = True, use_ml: bool = True) -> List[Tuple[str, str]]:
        """
        Extract entities using hybrid approach.
        
        Args:
            text: Input text
            use_rules: Whether to use rule-based extraction
            use_ml: Whether to use ML-based extraction
            
        Returns:
            List of (entity_text, entity_type) tuples (deduplicated)
        """
        all_entities = []
        
        # Rule-based extraction (high precision)
        if use_rules:
            rule_entities = self.extract_with_rules(text)
            all_entities.extend(rule_entities)
        
        # ML-based extraction (handles complex cases)
        if use_ml:
            ml_entities = self.extract_with_ml(text)
            all_entities.extend(ml_entities)
        
        # Deduplicate and resolve conflicts
        merged_entities = self._merge_entities(all_entities)
        
        # Return as simple (text, type) tuples
        return [(ent[0], ent[1]) for ent in merged_entities]
    
    def _validate_entity(self, entity_text: str, entity_type: str) -> bool:
        """
        Additional validation for extracted entities.
        
        Args:
            entity_text: Extracted text
            entity_type: Entity type
            
        Returns:
            True if entity is valid
        """
        # Domain validation: exclude common false positives
        if entity_type == 'DOMAIN':
            # Exclude domains that are too short or common words
            if len(entity_text) < 4:
                return False
            # Exclude if it's a common file extension
            if entity_text.lower() in ['exe', 'pdf', 'doc', 'txt', 'zip', 'rar']:
                return False
        
        # IP address validation: exclude invalid IPs
        if entity_type == 'IP_ADDRESS':
            parts = entity_text.split('.')
            if len(parts) == 4:
                try:
                    # Check each octet is 0-255
                    for part in parts:
                        if int(part) > 255:
                            return False
                except ValueError:
                    return False
        
        # Hash validation: ensure it's not a common word
        if entity_type == 'HASH':
            # Hashes should be hexadecimal
            if not all(c in '0123456789abcdefABCDEF' for c in entity_text):
                return False
        
        return True
    
    def _merge_entities(self, entities: List[Tuple[str, str, int, int]]) -> List[Tuple[str, str, int, int]]:
        """
        Merge and deduplicate entities, resolving conflicts.
        
        Strategy:
        - If entities overlap, prefer rule-based over ML
        - If same span, prefer more specific type
        - Remove duplicates
        
        Args:
            entities: List of (text, type, start, end)
            
        Returns:
            Deduplicated list of entities
        """
        if not entities:
            return []
        
        # Sort by start position
        entities = sorted(entities, key=lambda x: (x[2], x[3]))
        
        merged = []
        for entity in entities:
            text, ent_type, start, end = entity
            
            # Check for overlap with existing entities
            overlapping = False
            for i, existing in enumerate(merged):
                ex_text, ex_type, ex_start, ex_end = existing
                
                # Check if they overlap
                if not (end <= ex_start or start >= ex_end):
                    overlapping = True
                    
                    # Conflict resolution:
                    # 1. Prefer exact match
                    if start == ex_start and end == ex_end:
                        # Same span - keep more specific type
                        if self._is_more_specific(ent_type, ex_type):
                            merged[i] = entity
                    # 2. Prefer longer span
                    elif (end - start) > (ex_end - ex_start):
                        merged[i] = entity
                    # 3. Keep existing if it's longer
                    break
            
            if not overlapping:
                merged.append(entity)
        
        return merged
    
    def _is_more_specific(self, type1: str, type2: str) -> bool:
        """
        Determine if type1 is more specific than type2.
        
        Args:
            type1: First entity type
            type2: Second entity type
            
        Returns:
            True if type1 is more specific
        """
        # Define type specificity hierarchy
        specificity_order = {
            'IP_ADDRESS': 10,
            'CVE_ID': 10,
            'EMAIL_ADDRESS': 10,
            'URL': 9,
            'DOMAIN': 8,
            'HASH': 10,
            'PHONE_NUMBER': 10,
            'SSN': 10,
            'CREDIT_CARD_NUMBER': 10,
            'DATE': 8,
            'TIME': 8,
        }
        
        score1 = specificity_order.get(type1, 5)
        score2 = specificity_order.get(type2, 5)
        
        return score1 > score2


def main():
    """Test the hybrid extractor."""
    # Initialize extractor
    extractor = HybridEntityExtractor(
        ner_model_path="cyber-train/models/ner_model/model-best"
    )
    
    # Test cases
    test_cases = [
        "Suspicious activity from IP 192.168.1.100 detected at 14:30:00",
        "CVE-2021-44228 affects Apache Log4j versions 2.0-beta9 to 2.15.0",
        "Contact admin@company.com for access to https://internal.example.com",
        "Hash: a1b2c3d4e5f6789012345678901234567890abcd",
        "Phone: +1-555-123-4567 or email: security@company.com",
        "Domain evil.com is hosting malware at http://evil.com/payload.exe",
    ]
    
    print("="*70)
    print("HYBRID ENTITY EXTRACTOR - TEST RESULTS")
    print("="*70)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n[Test {i}]")
        print(f"Text: {text}")
        print("\nExtracted Entities:")
        
        entities = extractor.extract(text)
        
        if entities:
            for entity_text, entity_type in entities:
                print(f"  • {entity_text} → {entity_type}")
        else:
            print("  (no entities found)")


if __name__ == "__main__":
    main()

