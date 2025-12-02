#!/usr/bin/env python3
"""
Test script for trained spaCy NER and Intent Classification models.
This script validates model performance and provides examples of usage.
"""

import spacy
from pathlib import Path
import json
from typing import List, Dict, Tuple
import argparse

# Import post-processing filter
try:
    from fix_entity_extraction import post_process_entities
    USE_FILTER = True
except ImportError:
    USE_FILTER = False
    print("⚠️  Post-processing filter not available. Install fix_entity_extraction.py for better results.")


class ModelTester:
    """Test and evaluate trained spaCy models."""
    
    def __init__(self, ner_model_path: str = None, intent_model_path: str = None):
        self.ner_model = None
        self.intent_model = None
        
        # Default paths
        if ner_model_path is None:
            ner_model_path = "cyber-train/models/ner_model/model-best"
        if intent_model_path is None:
            intent_model_path = "cyber-train/models/intent_model/model-best"
        
        self.ner_model_path = Path(ner_model_path)
        self.intent_model_path = Path(intent_model_path)
        
    def load_models(self):
        """Load the trained models."""
        print("="*70)
        print("LOADING TRAINED MODELS")
        print("="*70)
        
        if self.ner_model_path.exists():
            try:
                print(f"\n📦 Loading NER model from: {self.ner_model_path}")
                self.ner_model = spacy.load(str(self.ner_model_path))
                print(f"✅ NER model loaded successfully")
                print(f"   Pipeline: {self.ner_model.pipe_names}")
            except Exception as e:
                print(f"❌ Error loading NER model: {e}")
                self.ner_model = None
        else:
            print(f"⚠️  NER model not found at: {self.ner_model_path}")
        
        if self.intent_model_path.exists():
            try:
                print(f"\n📦 Loading Intent model from: {self.intent_model_path}")
                self.intent_model = spacy.load(str(self.intent_model_path))
                print(f"✅ Intent model loaded successfully")
                print(f"   Pipeline: {self.intent_model.pipe_names}")
            except Exception as e:
                print(f"❌ Error loading Intent model: {e}")
                self.intent_model = None
        else:
            print(f"⚠️  Intent model not found at: {self.intent_model_path}")
        
        print()
    
    def test_ner(self, text: str, use_filter: bool = True) -> List[Tuple[str, str]]:
        """Test NER model on a text."""
        if self.ner_model is None:
            return []
        
        doc = self.ner_model(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Apply post-processing filter to remove false positives
        if use_filter and USE_FILTER:
            entities = post_process_entities(entities, apply_filter=True, apply_validation=True)
        
        return entities
    
    def test_intent(self, text: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """Test Intent model on a text."""
        if self.intent_model is None:
            return []
        
        doc = self.intent_model(text)
        intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return intents
    
    def test_combined(self, text: str):
        """Test both models on the same text."""
        print(f"\n📝 Text: {text}")
        print("-" * 70)
        
        # NER results
        if self.ner_model:
            entities = self.test_ner(text)
            if entities:
                print("🏷️  Entities Found:")
                for entity_text, label in entities:
                    print(f"   • {entity_text} → {label}")
            else:
                print("🏷️  No entities found")
        else:
            print("🏷️  NER model not available")
        
        # Intent results
        if self.intent_model:
            intents = self.test_intent(text, top_n=5)
            if intents:
                print("\n🎯 Top Intents:")
                for intent, score in intents:
                    print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
            else:
                print("\n🎯 No intents found")
        else:
            print("\n🎯 Intent model not available")
    
    def run_test_suite(self):
        """Run a comprehensive test suite with cybersecurity and OSINT examples."""
        print("\n" + "="*70)
        print("COMPREHENSIVE TEST SUITE")
        print("="*70)
        
        # Cybersecurity test cases
        cybersecurity_tests = [
            "APT41 used WannaCry malware to attack IP 192.168.1.1. CVE-2021-44228 was exploited.",
            "I need to investigate this suspicious IP address 10.0.0.1 for potential threats",
            "Analyze the malware sample from domain malicious-site.com and extract IOCs",
            "Incident Commander declared SEV-1 incident INC123 coordinating response across teams",
            "Perform memory forensics on the compromised system and analyze the disk image",
            "Hunt for APT activity and lateral movement indicators in our environment",
            "Report the data breach to regulators and notify all affected data subjects",
            "Execute the incident response playbook for ransomware containment",
        ]
        
        # OSINT test cases
        osint_tests = [
            "Verify the source of this viral video and check if the image is authentic",
            "Detect bot networks and fake accounts spreading disinformation on social media",
            "Build relationship graph of the social network and map the actor network",
            "Profile the threat actor and attribute this campaign to a known group",
            "Track the actor's activity across platforms and monitor the campaign",
            "Cross-reference this information with other OSINT sources and verify the claim",
            "GPS coordinates: latitude 40.7128, longitude -74.0060. Location: New York datacenter",
            "Domain example.com uses nameserver ns1.example.com and is hosted at datacenter AWS-US-EAST-1",
        ]
        
        print("\n🔒 CYBERSECURITY TEST CASES")
        print("="*70)
        for i, test in enumerate(cybersecurity_tests, 1):
            print(f"\n[Test {i}/{len(cybersecurity_tests)}]")
            self.test_combined(test)
        
        print("\n\n🌐 OSINT TEST CASES")
        print("="*70)
        for i, test in enumerate(osint_tests, 1):
            print(f"\n[Test {i}/{len(osint_tests)}]")
            self.test_combined(test)
    
    def evaluate_on_test_set(self, test_file: str, model_type: str = "ner"):
        """Evaluate model on the test set."""
        print("\n" + "="*70)
        print(f"EVALUATING {model_type.upper()} MODEL ON TEST SET")
        print("="*70)
        
        test_path = Path(test_file)
        if not test_path.exists():
            print(f"❌ Test file not found: {test_path}")
            return
        
        model = self.ner_model if model_type == "ner" else self.intent_model
        if model is None:
            print(f"❌ {model_type.upper()} model not loaded")
            return
        
        # Use spaCy's evaluate command
        import subprocess
        import sys
        
        cmd = [
            sys.executable, "-m", "spacy", "evaluate",
            str(model_path := (self.ner_model_path if model_type == "ner" else self.intent_model_path)),
            str(test_path),
            "--output", str(model_path.parent / f"{model_type}_test_evaluation.json")
        ]
        
        print(f"\nRunning: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"\n✅ Evaluation complete. Results saved to:")
            print(f"   {model_path.parent / f'{model_type}_test_evaluation.json'}")
        else:
            print(f"❌ Evaluation failed:")
            print(result.stderr)
    
    def interactive_mode(self):
        """Interactive testing mode."""
        print("\n" + "="*70)
        print("INTERACTIVE TESTING MODE")
        print("="*70)
        print("Enter text to test (or 'quit' to exit):\n")
        
        while True:
            try:
                text = input("> ").strip()
                if text.lower() in ['quit', 'exit', 'q']:
                    break
                if not text:
                    continue
                
                self.test_combined(text)
                print()
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Test trained spaCy models for Cybersecurity and OSINT"
    )
    parser.add_argument(
        "--ner-model",
        default="cyber-train/models/ner_model/model-best",
        help="Path to NER model"
    )
    parser.add_argument(
        "--intent-model",
        default="cyber-train/models/intent_model/model-best",
        help="Path to Intent Classification model"
    )
    parser.add_argument(
        "--test-suite",
        action="store_true",
        help="Run comprehensive test suite"
    )
    parser.add_argument(
        "--evaluate-ner",
        help="Evaluate NER model on test set (path to test.spacy file)"
    )
    parser.add_argument(
        "--evaluate-intent",
        help="Evaluate Intent model on test set (path to test.spacy file)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start interactive testing mode"
    )
    parser.add_argument(
        "--text",
        help="Test a single text string"
    )
    
    args = parser.parse_args()
    
    tester = ModelTester(args.ner_model, args.intent_model)
    tester.load_models()
    
    if args.text:
        tester.test_combined(args.text)
    elif args.test_suite:
        tester.run_test_suite()
    elif args.evaluate_ner:
        tester.evaluate_on_test_set(args.evaluate_ner, "ner")
    elif args.evaluate_intent:
        tester.evaluate_on_test_set(args.evaluate_intent, "intent")
    elif args.interactive:
        tester.interactive_mode()
    else:
        # Default: run test suite
        tester.run_test_suite()
        print("\n" + "="*70)
        print("💡 TIP: Use --interactive for interactive testing")
        print("   Use --text 'your query' to test a single query")
        print("   Use --evaluate-ner/--evaluate-intent to evaluate on test sets")
        print("="*70)


if __name__ == "__main__":
    main()

