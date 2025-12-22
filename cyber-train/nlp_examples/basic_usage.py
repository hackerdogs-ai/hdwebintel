#!/usr/bin/env python3
"""
Basic Usage Examples for NER and Intent Classification Models

This script demonstrates how to:
1. Load the trained models
2. Extract entities from text
3. Classify intents from text
4. Handle common use cases
"""

import spacy
from pathlib import Path
from typing import List, Dict, Tuple

# Model paths
NER_MODEL_PATH = "cyber-train/models/ner_model/model-best"
INTENT_MODEL_PATH = "cyber-train/models/intent_model/model-best"


def load_models():
    """Load the trained NER and Intent models."""
    print("="*70)
    print("LOADING MODELS")
    print("="*70)
    
    ner_model = None
    intent_model = None
    
    # Load NER model
    ner_path = Path(NER_MODEL_PATH)
    if ner_path.exists():
        print(f"\n📦 Loading NER model from: {ner_path}")
        ner_model = spacy.load(str(ner_path))
        print(f"✅ NER model loaded successfully")
        print(f"   Pipeline: {ner_model.pipe_names}")
        print(f"   Entity labels: {len(ner_model.get_pipe('ner').labels)} labels")
    else:
        print(f"❌ NER model not found at: {ner_path}")
    
    # Load Intent model
    intent_path = Path(INTENT_MODEL_PATH)
    if intent_path.exists():
        print(f"\n📦 Loading Intent model from: {intent_path}")
        intent_model = spacy.load(str(intent_path))
        print(f"✅ Intent model loaded successfully")
        print(f"   Pipeline: {intent_model.pipe_names}")
        print(f"   Intent labels: {len(intent_model.get_pipe('textcat_multilabel').labels)} labels")
    else:
        print(f"❌ Intent model not found at: {intent_path}")
    
    return ner_model, intent_model


def extract_entities(text: str, ner_model) -> List[Tuple[str, str]]:
    """
    Extract entities from text using the NER model.
    
    Args:
        text: Input text to analyze
        ner_model: Loaded spaCy NER model
    
    Returns:
        List of (entity_text, label) tuples
    """
    if ner_model is None:
        return []
    
    doc = ner_model(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


def classify_intents(text: str, intent_model, threshold: float = 0.3) -> List[Tuple[str, float]]:
    """
    Classify intents from text using the Intent model.
    
    Args:
        text: Input text to analyze
        intent_model: Loaded spaCy Intent model
        threshold: Minimum confidence score (default: 0.3)
    
    Returns:
        List of (intent, score) tuples sorted by score (descending)
    """
    if intent_model is None:
        return []
    
    doc = intent_model(text)
    intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
    # Filter by threshold
    intents = [(intent, score) for intent, score in intents if score >= threshold]
    return intents


def analyze_query(text: str, ner_model, intent_model):
    """
    Complete analysis: extract entities and classify intents.
    
    Args:
        text: Input text to analyze
        ner_model: Loaded spaCy NER model
        intent_model: Loaded spaCy Intent model
    """
    print("\n" + "="*70)
    print(f"QUERY: {text}")
    print("="*70)
    
    # Extract entities
    entities = extract_entities(text, ner_model)
    if entities:
        print(f"\n🏷️  Entities Found ({len(entities)}):")
        for entity_text, label in entities:
            print(f"   • {entity_text} → {label}")
    else:
        print("\n🏷️  No entities found")
    
    # Classify intents
    intents = classify_intents(text, intent_model)
    if intents:
        print(f"\n🎯 Top Intents ({len(intents)}):")
        for intent, score in intents[:5]:  # Show top 5
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    else:
        print("\n🎯 No intents detected")


def main():
    """Main function demonstrating basic usage."""
    print("="*70)
    print("BASIC USAGE EXAMPLES - NER AND INTENT CLASSIFICATION")
    print("="*70)
    
    # Load models
    ner_model, intent_model = load_models()
    
    if ner_model is None and intent_model is None:
        print("\n❌ No models loaded. Exiting.")
        return
    
    # Example queries
    example_queries = [
        # Cybersecurity
        "APT28 used WannaCry ransomware to attack IP 172.16.0.1 and domain evil.com on port 8080",
        "🚨 Security alert: IP 192.168.1.1 compromised © 2024",
        "Check compliance with NIST CSF, PCI DSS, and HIPAA requirements",
        
        # OSINT
        "Verify the authenticity of this image and check the GPS coordinates latitude 40.7128 longitude -74.0060",
        "⚠️ Warning: Domain example.com is suspicious 🔍",
        
        # AI Security
        "AI security incident involving GPT-4 from OpenAI provider",
        "Monitor AI model usage: GPT-4, Claude-3-Opus, Gemini-Pro from Google",
        
        # Multi-entity
        "Incident INC-2024-001 occurred on 2024-11-30 at 14:30 UTC involving user admin@company.com",
        
        # Simple queries
        "Check IP 192.168.1.1",
        "What is the threat level for IP address 203.0.113.0?",
    ]
    
    print("\n" + "="*70)
    print("RUNNING EXAMPLE QUERIES")
    print("="*70)
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n[Example {i}/{len(example_queries)}]")
        analyze_query(query, ner_model, intent_model)
    
    print("\n" + "="*70)
    print("✅ BASIC USAGE EXAMPLES COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()

