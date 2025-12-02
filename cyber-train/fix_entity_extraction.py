"""
Post-processing filter for NER model to remove false positives.
This should be applied after entity extraction to improve precision.
"""
import re
from typing import List, Tuple

# Common words that should NOT be entities
COMMON_WORDS = {
    'i', 'me', 'my', 'you', 'your', 'he', 'she', 'it', 'we', 'they', 'them',
    'the', 'a', 'an', 'this', 'that', 'these', 'those', 'for', 'and', 'or', 'but',
    'in', 'on', 'at', 'to', 'from', 'with', 'by', 'of', 'is', 'are', 'was', 'were',
    'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'can', 'must', 'hey', 'hi', 'hello',
    'what', 'when', 'where', 'why', 'how', 'who', 'which', 'whose', 'whom',
    'up', 'down', 'out', 'off', 'over', 'under', 'above', 'below', 'across',
    'through', 'during', 'before', 'after', 'while', 'until', 'since', 'ago',
    'safe', 'thing', 'things', 'stuff', 'way', 'ways', 'time', 'times',
    'investigate', 'check', 'verify', 'analyze', 'detect', 'monitor'  # Common verbs
}

# Common phrases that should NOT be entities
COMMON_PHRASES = {
    'i need', 'i want', 'i have', 'i am', 'i was', 'i will', 'i can', 'i should',
    'is safe', 'is not', 'is good', 'is bad', 'is ok', 'is fine',
    "what's up", "what's", "that's", "it's", "there's", "here's",
    'can you', 'could you', 'would you', 'should you', 'will you',
    'need to', 'want to', 'have to', 'got to', 'going to', 'trying to',
    'look at', 'look for', 'look up', 'check if', 'check for', 'check on',
    'help me', 'help with', 'help to', 'let me', 'tell me', 'show me'
}

# Punctuation that should NOT be entities
PUNCTUATION = {':', ',', '.', ';', '-', '(', ')', '[', ']', '{', '}', 
               '!', '?', '"', "'", '/', '\\', '|', '&', '%', '$', '#', '@'}

# Patterns for validating entity types
ENTITY_PATTERNS = {
    'IP_ADDRESS': re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'),
    'CVE_ID': re.compile(r'^CVE-\d{4}-\d{4,7}$', re.IGNORECASE),
    'LATITUDE': re.compile(r'^-?\d{1,2}(\.\d+)?$'),  # -90 to 90
    'LONGITUDE': re.compile(r'^-?\d{1,3}(\.\d+)?$'),  # -180 to 180
    'DOMAIN': re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'),
    'EMAIL': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
    'PHONE_NUMBER': re.compile(r'^\+?[\d\s\-\(\)]{10,}$'),
    'SSN': re.compile(r'^\d{3}-\d{2}-\d{4}$'),
    'CREDIT_CARD_NUMBER': re.compile(r'^\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}$'),
}

# Entity types that should be validated against patterns
VALIDATED_TYPES = set(ENTITY_PATTERNS.keys())


def filter_entities(entities: List[Tuple[str, str]], min_length: int = 2) -> List[Tuple[str, str]]:
    """
    Filter out obviously incorrect entities.
    
    Args:
        entities: List of (text, label) tuples
        min_length: Minimum character length for valid entity
    
    Returns:
        Filtered list of entities
    """
    filtered = []
    
    for text, label in entities:
        text_clean = text.strip()
        
        # Skip empty or too short
        if len(text_clean) < min_length:
            continue
        
        # Skip punctuation-only
        if text_clean in PUNCTUATION or all(c in PUNCTUATION for c in text_clean):
            continue
        
        # Skip common words (unless it's a specific entity type that might legitimately be a common word)
        text_lower = text_clean.lower()
        if text_lower in COMMON_WORDS and label not in ['PERSON', 'ORGANIZATION', 'LOCATION', 'THREAT_ACTOR']:
            continue
        
        # Skip common phrases
        if text_lower in COMMON_PHRASES:
            continue
        
        # Skip if it's a common word pattern (e.g., "investigate", "check", "verify" as verbs)
        if text_lower in ['investigate', 'check', 'verify', 'analyze', 'detect', 'monitor', 'track']:
            # Only allow if it's a legitimate entity type (not COMMIT, BRANCH, etc.)
            if label in ['COMMIT', 'BRANCH', 'TRAINING_TYPE', 'INTEGRATION_TYPE']:
                continue
        
        # Skip single characters
        if len(text_clean) == 1 and text_clean not in ['I']:  # 'I' might be valid as PERSON
            continue
        
        # Validate against patterns if applicable
        if label in VALIDATED_TYPES:
            pattern = ENTITY_PATTERNS[label]
            if not pattern.match(text_clean):
                # Pattern doesn't match, but might be partial match
                # Only reject if clearly wrong
                if label == 'IP_ADDRESS' and not any(c.isdigit() for c in text_clean):
                    continue
                if label == 'CVE_ID' and not text_clean.upper().startswith('CVE-'):
                    continue
        
        # Additional heuristics
        # Skip if it's a common phrase that's unlikely to be an entity
        if ' ' in text_clean:
            words = text_clean.lower().split()
            # Skip if all words are common words
            if all(word in COMMON_WORDS for word in words) and label not in ['PERSON', 'ORGANIZATION', 'THREAT_ACTOR']:
                continue
            # Skip if it matches a common phrase
            if text_lower in COMMON_PHRASES:
                continue
        
        # Skip problematic entity types for common words
        problematic_labels_for_common = ['BRANCH', 'COMMIT', 'TRAINING_TYPE', 'INTEGRATION_TYPE', 
                                        'ENCRYPTION_TYPE', 'VULNERABILITY_ID']
        if label in problematic_labels_for_common:
            # Be extra strict - only allow if it's clearly not a common word
            if text_lower in COMMON_WORDS or text_lower in COMMON_PHRASES:
                continue
            # Skip single characters for these types
            if len(text_clean) <= 2:
                continue
        
        filtered.append((text, label))
    
    return filtered


def validate_entity_type(text: str, label: str) -> bool:
    """
    Validate that entity text matches expected pattern for its type.
    
    Args:
        text: Entity text
        label: Entity label/type
    
    Returns:
        True if valid, False otherwise
    """
    if label not in VALIDATED_TYPES:
        return True  # No pattern to validate against
    
    pattern = ENTITY_PATTERNS[label]
    return bool(pattern.match(text.strip()))


def post_process_entities(entities: List[Tuple[str, str]], 
                          apply_filter: bool = True,
                          apply_validation: bool = True) -> List[Tuple[str, str]]:
    """
    Post-process entities with filtering and validation.
    
    Args:
        entities: List of (text, label) tuples
        apply_filter: Whether to apply filtering
        apply_validation: Whether to apply pattern validation
    
    Returns:
        Post-processed list of entities
    """
    if apply_filter:
        entities = filter_entities(entities)
    
    if apply_validation:
        validated = []
        for text, label in entities:
            if validate_entity_type(text, label):
                validated.append((text, label))
            # For non-validated types, keep them
            elif label not in VALIDATED_TYPES:
                validated.append((text, label))
        entities = validated
    
    return entities


# Example usage
if __name__ == "__main__":
    # Test with problematic entities from test results
    test_entities = [
        ("APT41", "API_TYPE"),  # Wrong type
        ("I", "NETWORK_TYPE"),  # Common word
        ("investigate this", "METRIC_TYPE"),  # Wrong boundary
        (":", "LONGITUDE"),  # Punctuation
        (",", "LOCATION"),  # Punctuation
        ("192.168.1.1", "IP_ADDRESS"),  # Correct
        ("CVE-2021-44228", "CVE_ID"),  # Correct
        ("malicious-site.com", "DOMAIN"),  # Correct
    ]
    
    print("Original entities:", test_entities)
    filtered = post_process_entities(test_entities)
    print("Filtered entities:", filtered)
    
    # Expected: Only keep ("192.168.1.1", "IP_ADDRESS"), ("CVE-2021-44228", "CVE_ID"), ("malicious-site.com", "DOMAIN")


