#!/usr/bin/env python3
"""
Minimal Integration Example

Copy this file to your project and modify as needed.
"""

import spacy
from pathlib import Path
from typing import List, Tuple, Dict, Optional


class MinimalNLP:
    """
    Minimal wrapper for NER and Intent models.
    
    Usage:
        nlp = MinimalNLP(model_dir="models")
        entities = nlp.extract_entities("Check IP 192.168.1.1")
        intents = nlp.classify_intents("Check IP 192.168.1.1")
    """
    
    def __init__(self, model_dir: str = "models"):
        """
        Initialize and load models.
        
        Args:
            model_dir: Path to directory containing ner_model and intent_model
        """
        self.model_dir = Path(model_dir)
        self.ner_model = None
        self.intent_model = None
        self._load_models()
    
    def _load_models(self):
        """Load NER and Intent models."""
        ner_path = self.model_dir / "ner_model" / "model-best"
        intent_path = self.model_dir / "intent_model" / "model-best"
        
        if not ner_path.exists():
            raise FileNotFoundError(f"NER model not found at {ner_path}")
        if not intent_path.exists():
            raise FileNotFoundError(f"Intent model not found at {intent_path}")
        
        print(f"Loading NER model from {ner_path}...")
        self.ner_model = spacy.load(str(ner_path))
        print(f"✅ NER model loaded: {len(self.ner_model.get_pipe('ner').labels)} labels")
        
        print(f"Loading Intent model from {intent_path}...")
        self.intent_model = spacy.load(str(intent_path))
        print(f"✅ Intent model loaded: {len(self.intent_model.get_pipe('textcat_multilabel').labels)} labels")
    
    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract entities from text.
        
        Args:
            text: Input text
        
        Returns:
            List of (entity_text, label) tuples
        """
        if self.ner_model is None:
            raise RuntimeError("NER model not loaded")
        
        doc = self.ner_model(text)
        return [(ent.text, ent.label_) for ent in doc.ents]
    
    def classify_intents(self, text: str, threshold: float = 0.3) -> List[Tuple[str, float]]:
        """
        Classify intents from text.
        
        Args:
            text: Input text
            threshold: Minimum confidence score (default: 0.3)
        
        Returns:
            List of (intent, score) tuples sorted by score
        """
        if self.intent_model is None:
            raise RuntimeError("Intent model not loaded")
        
        doc = self.intent_model(text)
        intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
        return [(intent, score) for intent, score in intents if score >= threshold]
    
    def analyze(self, text: str, threshold: float = 0.3) -> Dict:
        """
        Extract entities and classify intents from text.
        
        Args:
            text: Input text
            threshold: Minimum confidence score for intents
        
        Returns:
            Dictionary with 'entities' and 'intents' keys
        """
        entities = self.extract_entities(text)
        intents = self.classify_intents(text, threshold)
        
        return {
            "entities": entities,
            "intents": intents,
            "entity_count": len(entities),
            "intent_count": len(intents)
        }
    
    def batch_extract_entities(self, texts: List[str]) -> List[List[Tuple[str, str]]]:
        """
        Extract entities from multiple texts efficiently.
        
        Args:
            texts: List of input texts
        
        Returns:
            List of entity lists (one per text)
        """
        if self.ner_model is None:
            raise RuntimeError("NER model not loaded")
        
        docs = list(self.ner_model.pipe(texts))
        return [[(ent.text, ent.label_) for ent in doc.ents] for doc in docs]
    
    def batch_classify_intents(self, texts: List[str], threshold: float = 0.3) -> List[List[Tuple[str, float]]]:
        """
        Classify intents from multiple texts efficiently.
        
        Args:
            texts: List of input texts
            threshold: Minimum confidence score
        
        Returns:
            List of intent lists (one per text)
        """
        if self.intent_model is None:
            raise RuntimeError("Intent model not loaded")
        
        docs = list(self.intent_model.pipe(texts))
        results = []
        for doc in docs:
            intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
            results.append([(intent, score) for intent, score in intents if score >= threshold])
        return results


# Example usage
if __name__ == "__main__":
    # Initialize (loads models)
    nlp = MinimalNLP(model_dir="cyber-train/models")
    
    # Example 1: Extract entities
    text = "Check IP 192.168.1.1 for suspicious activity"
    entities = nlp.extract_entities(text)
    print(f"\nEntities: {entities}")
    
    # Example 2: Classify intents
    intents = nlp.classify_intents(text)
    print(f"Intents: {intents[:5]}")  # Top 5
    
    # Example 3: Combined analysis
    result = nlp.analyze(text)
    print(f"\nAnalysis Result:")
    print(f"  Entities: {result['entity_count']}")
    print(f"  Intents: {result['intent_count']}")
    
    # Example 4: Batch processing
    texts = [
        "Check IP 192.168.1.1",
        "APT28 used WannaCry ransomware",
        "Verify compliance with NIST CSF"
    ]
    batch_entities = nlp.batch_extract_entities(texts)
    print(f"\nBatch Entities: {batch_entities}")

