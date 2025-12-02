#!/usr/bin/env python3
"""
Comprehensive test suite for NER and Intent models with multiple input types.
Tests various query styles, domains, complexity levels, and edge cases.
"""

import spacy
from pathlib import Path
import json
from typing import List, Dict, Tuple, Optional
import argparse
from datetime import datetime
import sys

# Import post-processing filter if available
try:
    from fix_entity_extraction import post_process_entities
    USE_FILTER = True
except ImportError:
    USE_FILTER = False


class ComprehensiveTester:
    """Comprehensive test suite for trained models."""
    
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
        
        self.results = {
            "test_cases": [],
            "summary": {},
            "timestamp": datetime.now().isoformat()
        }
    
    def load_models(self):
        """Load the trained models."""
        print("="*70)
        print("LOADING MODELS")
        print("="*70)
        
        if self.ner_model_path.exists():
            try:
                print(f"\n📦 Loading NER model from: {self.ner_model_path}")
                self.ner_model = spacy.load(str(self.ner_model_path))
                print(f"✅ NER model loaded successfully")
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
            except Exception as e:
                print(f"❌ Error loading Intent model: {e}")
                self.intent_model = None
        else:
            print(f"⚠️  Intent model not found at: {self.intent_model_path}")
        
        print()
    
    def test_query(self, text: str, category: str = "general", 
                   expected_entities: List[Tuple[str, str]] = None,
                   expected_intents: List[str] = None) -> Dict:
        """Test a single query and return results."""
        result = {
            "text": text,
            "category": category,
            "entities": [],
            "intents": [],
            "entity_count": 0,
            "intent_count": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        # Test NER
        if self.ner_model:
            doc = self.ner_model(text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            
            # Apply post-processing filter if available
            if USE_FILTER:
                entities = post_process_entities(entities, apply_filter=True, apply_validation=True)
            
            result["entities"] = entities
            result["entity_count"] = len(entities)
        
        # Test Intent
        if self.intent_model:
            doc = self.intent_model(text)
            intents = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
            # Filter to top intents with score > 0.3
            intents = [(intent, score) for intent, score in intents if score > 0.3]
            result["intents"] = intents
            result["intent_count"] = len(intents)
        
        # Compare with expected if provided
        if expected_entities:
            result["expected_entities"] = expected_entities
            result["entity_match"] = set(result["entities"]) == set(expected_entities)
        
        if expected_intents:
            result["expected_intents"] = expected_intents
            result["intent_match"] = any(intent in [i[0] for i in result["intents"]] for intent in expected_intents)
        
        return result
    
    def print_result(self, result: Dict, show_details: bool = True):
        """Print test result in a formatted way."""
        print(f"\n{'='*70}")
        print(f"📝 Query: {result['text']}")
        print(f"📂 Category: {result['category']}")
        print("-"*70)
        
        if result['entities']:
            print(f"🏷️  Entities Found ({result['entity_count']}):")
            for entity_text, label in result['entities']:
                print(f"   • {entity_text} → {label}")
        else:
            print("🏷️  No entities found")
        
        if result['intents']:
            print(f"\n🎯 Top Intents ({result['intent_count']}):")
            for intent, score in result['intents'][:5]:
                print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
        else:
            print("\n🎯 No intents detected")
        
        if show_details and ('expected_entities' in result or 'expected_intents' in result):
            print("\n📊 Expected vs Actual:")
            if 'expected_entities' in result:
                match = result.get('entity_match', False)
                status = "✅" if match else "⚠️"
                print(f"   {status} Entity match: {match}")
            if 'expected_intents' in result:
                match = result.get('intent_match', False)
                status = "✅" if match else "⚠️"
                print(f"   {status} Intent match: {match}")
    
    def run_comprehensive_tests(self):
        """Run comprehensive test suite with multiple input types."""
        print("\n" + "="*70)
        print("COMPREHENSIVE TEST SUITE - MULTIPLE INPUT TYPES")
        print("="*70)
        
        test_cases = self._get_test_cases()
        
        print(f"\n📊 Running {len(test_cases)} test cases across multiple categories...")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n[Test {i}/{len(test_cases)}]")
            result = self.test_query(**test_case)
            self.print_result(result, show_details=False)
            self.results["test_cases"].append(result)
        
        # Generate summary
        self._generate_summary()
        self._print_summary()
    
    def _get_test_cases(self) -> List[Dict]:
        """Get comprehensive test cases covering multiple input types."""
        return [
            # ========== NATURAL LANGUAGE QUERIES ==========
            {
                "text": "Can you help me investigate this suspicious IP address 192.168.1.100?",
                "category": "natural_language",
                "expected_entities": [("192.168.1.100", "IP_ADDRESS")],
                "expected_intents": ["INVESTIGATE"]
            },
            {
                "text": "I need to check if the domain example.com is safe",
                "category": "natural_language",
                "expected_entities": [("example.com", "DOMAIN")],
                "expected_intents": ["CHECK", "VALIDATE"]
            },
            
            # ========== TECHNICAL QUERIES ==========
            {
                "text": "APT41 CVE-2021-44228 Log4j vulnerability exploitation detected on 10.0.0.5",
                "category": "technical",
                "expected_entities": [
                    ("APT41", "THREAT_ACTOR"),
                    ("CVE-2021-44228", "CVE_ID"),
                    ("10.0.0.5", "IP_ADDRESS")
                ],
                "expected_intents": ["DETECT", "INVESTIGATE"]
            },
            {
                "text": "Perform memory forensics on host server-01.internal.com port 443",
                "category": "technical",
                "expected_entities": [
                    ("server-01.internal.com", "HOST_TYPE"),
                    ("443", "PORT")
                ],
                "expected_intents": ["PERFORM_MEMORY_FORENSICS", "ANALYZE"]
            },
            
            # ========== CASUAL/INFORMAL QUERIES ==========
            {
                "text": "hey what's up with that malware thing?",
                "category": "casual",
                "expected_intents": ["INVESTIGATE", "ANALYZE"]
            },
            {
                "text": "can u check this ip 8.8.8.8 pls?",
                "category": "casual",
                "expected_entities": [("8.8.8.8", "IP_ADDRESS")],
                "expected_intents": ["CHECK", "VALIDATE"]
            },
            
            # ========== MULTI-ENTITY QUERIES ==========
            {
                "text": "APT28 used WannaCry ransomware to attack IP 172.16.0.1 and domain evil.com on port 8080",
                "category": "multi_entity",
                "expected_entities": [
                    ("APT28", "THREAT_ACTOR"),
                    ("WannaCry", "MALWARE_TYPE"),
                    ("172.16.0.1", "IP_ADDRESS"),
                    ("evil.com", "DOMAIN"),
                    ("8080", "PORT")
                ],
                "expected_intents": ["INVESTIGATE", "DETECT"]
            },
            {
                "text": "Incident INC-2024-001 occurred on 2024-11-30 at 14:30 UTC involving user admin@company.com",
                "category": "multi_entity",
                "expected_entities": [
                    ("INC-2024-001", "INCIDENT_ID"),
                    ("2024-11-30", "DATE"),
                    ("14:30", "TIME"),
                    ("admin@company.com", "EMAIL")
                ],
                "expected_intents": ["INVESTIGATE", "DOCUMENT_INCIDENT"]
            },
            
            # ========== OSINT QUERIES ==========
            {
                "text": "Verify the authenticity of this image and check the GPS coordinates latitude 40.7128 longitude -74.0060",
                "category": "osint",
                "expected_entities": [
                    ("40.7128", "LATITUDE"),
                    ("-74.0060", "LONGITUDE")
                ],
                "expected_intents": ["VERIFY", "VALIDATE", "CHECK"]
            },
            {
                "text": "Track the social media account @suspicious_user across Twitter, Facebook, and LinkedIn",
                "category": "osint",
                "expected_entities": [
                    ("@suspicious_user", "USERNAME"),
                    ("Twitter", "PLATFORM"),
                    ("Facebook", "PLATFORM"),
                    ("LinkedIn", "PLATFORM")
                ],
                "expected_intents": ["TRACK", "MONITOR"]
            },
            
            # ========== CYBERSECURITY QUERIES ==========
            {
                "text": "Execute incident response playbook for ransomware containment and isolate affected systems",
                "category": "cybersecurity",
                "expected_intents": ["RESPOND_TO_INCIDENT", "ISOLATE_ASSETS", "EXECUTE_PLAYBOOK"]
            },
            {
                "text": "Hunt for lateral movement indicators and privilege escalation attempts in the environment",
                "category": "cybersecurity",
                "expected_intents": ["HUNT", "DETECT", "INVESTIGATE"]
            },
            
            # ========== COMPLEX/COMPOUND QUERIES ==========
            {
                "text": "I need to investigate the data breach, analyze the malware sample, and generate a report for the compliance team by tomorrow",
                "category": "complex",
                "expected_intents": ["INVESTIGATE", "ANALYZE", "GENERATE_REPORTS", "ENSURE_COMPLIANCE"]
            },
            {
                "text": "Monitor network traffic, detect anomalies, correlate with threat intelligence, and escalate if severity is high",
                "category": "complex",
                "expected_intents": ["MONITOR", "DETECT_ANOMALIES", "CORRELATE_EVENTS", "ESCALATE_INCIDENT"]
            },
            
            # ========== EDGE CASES ==========
            {
                "text": "test",
                "category": "edge_case_short",
                "expected_entities": [],
                "expected_intents": []
            },
            {
                "text": "This is a very long query that contains multiple sentences and should test how the model handles longer inputs with various types of information including IP addresses like 192.168.1.1, domains like example.com, and various technical terms that might appear in cybersecurity or OSINT contexts.",
                "category": "edge_case_long",
                "expected_entities": [
                    ("192.168.1.1", "IP_ADDRESS"),
                    ("example.com", "DOMAIN")
                ]
            },
            {
                "text": "Check IP: 10.0.0.1, Domain: test.com, Email: user@test.com, Phone: +1-555-123-4567",
                "category": "edge_case_formatted",
                "expected_entities": [
                    ("10.0.0.1", "IP_ADDRESS"),
                    ("test.com", "DOMAIN"),
                    ("user@test.com", "EMAIL"),
                    ("+1-555-123-4567", "PHONE_NUMBER")
                ]
            },
            
            # ========== QUESTION FORMAT ==========
            {
                "text": "What is the threat level for IP address 203.0.113.0?",
                "category": "question_format",
                "expected_entities": [("203.0.113.0", "IP_ADDRESS")],
                "expected_intents": ["ASSESS_RISK", "INVESTIGATE"]
            },
            {
                "text": "How do I investigate this security incident?",
                "category": "question_format",
                "expected_intents": ["INVESTIGATE", "RESPOND_TO_INCIDENT"]
            },
            
            # ========== COMMAND/IMPERATIVE FORMAT ==========
            {
                "text": "Block IP 192.168.1.50 and isolate host server-02",
                "category": "command_format",
                "expected_entities": [
                    ("192.168.1.50", "IP_ADDRESS"),
                    ("server-02", "HOST_TYPE")
                ],
                "expected_intents": ["BLOCK_IPS", "ISOLATE_ASSETS"]
            },
            {
                "text": "Generate threat intelligence report for APT29 campaign",
                "category": "command_format",
                "expected_entities": [("APT29", "THREAT_ACTOR")],
                "expected_intents": ["GENERATE_REPORTS", "GATHER_INTELLIGENCE"]
            },
            
            # ========== MIXED DOMAINS ==========
            {
                "text": "Cross-reference OSINT data from social media with cybersecurity threat intelligence to identify the threat actor",
                "category": "mixed_domains",
                "expected_intents": ["CORRELATE_EVENTS", "IDENTIFY_THREAT_ACTOR", "GATHER_INTELLIGENCE"]
            },
            {
                "text": "Verify the source of the leaked document and check if it contains any PII or sensitive data",
                "category": "mixed_domains",
                "expected_intents": ["VERIFY", "CHECK", "DETECT_PII"]
            },
            
            # ========== TIME-BASED QUERIES ==========
            {
                "text": "Show me all security events from the last 24 hours",
                "category": "time_based",
                "expected_intents": ["MONITOR", "ANALYZE", "GENERATE_REPORTS"]
            },
            {
                "text": "What happened on November 30, 2024 at 3:00 PM?",
                "category": "time_based",
                "expected_entities": [
                    ("November 30, 2024", "DATE"),
                    ("3:00 PM", "TIME")
                ],
                "expected_intents": ["INVESTIGATE", "ANALYZE"]
            },
            
            # ========== GEOGRAPHIC QUERIES ==========
            {
                "text": "Find all activities from coordinates 37.7749, -122.4194 in San Francisco",
                "category": "geographic",
                "expected_entities": [
                    ("37.7749", "LATITUDE"),
                    ("-122.4194", "LONGITUDE"),
                    ("San Francisco", "LOCATION")
                ],
                "expected_intents": ["INVESTIGATE", "MAP", "TRACK"]
            },
            
            # ========== COMPLIANCE/AUDIT QUERIES ==========
            {
                "text": "Generate compliance report for GDPR audit covering data privacy and protection measures",
                "category": "compliance",
                "expected_intents": ["GENERATE_REPORTS", "ENSURE_COMPLIANCE", "AUDIT_COMPLIANCE"]
            },
            {
                "text": "Check if our security controls meet ISO 27001 requirements",
                "category": "compliance",
                "expected_entities": [("ISO 27001", "COMPLIANCE_FRAMEWORK")],
                "expected_intents": ["CHECK", "ENSURE_COMPLIANCE", "AUDIT_COMPLIANCE"]
            },
            
            # ========== VULNERABILITY QUERIES ==========
            {
                "text": "Scan for CVE-2021-44228 and CVE-2021-45046 vulnerabilities in our systems",
                "category": "vulnerability",
                "expected_entities": [
                    ("CVE-2021-44228", "CVE_ID"),
                    ("CVE-2021-45046", "CVE_ID")
                ],
                "expected_intents": ["SCAN", "DETECT", "ASSESS_RISK"]
            },
            
            # ========== FINANCIAL/OSINT QUERIES ==========
            {
                "text": "Track cryptocurrency wallet address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb and monitor transactions",
                "category": "financial_osint",
                "expected_entities": [
                    ("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "WALLET_ADDRESS")
                ],
                "expected_intents": ["TRACK", "MONITOR"]
            },
        ]
    
    def _generate_summary(self):
        """Generate summary statistics from test results."""
        total = len(self.results["test_cases"])
        categories = {}
        entity_counts = []
        intent_counts = []
        
        for result in self.results["test_cases"]:
            category = result["category"]
            if category not in categories:
                categories[category] = {"count": 0, "entities": 0, "intents": 0}
            categories[category]["count"] += 1
            categories[category]["entities"] += result["entity_count"]
            categories[category]["intents"] += result["intent_count"]
            
            entity_counts.append(result["entity_count"])
            intent_counts.append(result["intent_count"])
        
        self.results["summary"] = {
            "total_tests": total,
            "categories": categories,
            "entity_stats": {
                "total": sum(entity_counts),
                "average": sum(entity_counts) / len(entity_counts) if entity_counts else 0,
                "max": max(entity_counts) if entity_counts else 0,
                "min": min(entity_counts) if entity_counts else 0
            },
            "intent_stats": {
                "total": sum(intent_counts),
                "average": sum(intent_counts) / len(intent_counts) if intent_counts else 0,
                "max": max(intent_counts) if intent_counts else 0,
                "min": min(intent_counts) if intent_counts else 0
            }
        }
    
    def _print_summary(self):
        """Print summary statistics."""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        summary = self.results["summary"]
        print(f"\n📊 Overall Statistics:")
        print(f"   Total test cases: {summary['total_tests']}")
        print(f"   Total entities found: {summary['entity_stats']['total']}")
        print(f"   Total intents found: {summary['intent_stats']['total']}")
        print(f"   Average entities per query: {summary['entity_stats']['average']:.2f}")
        print(f"   Average intents per query: {summary['intent_stats']['average']:.2f}")
        
        print(f"\n📂 Performance by Category:")
        for category, stats in sorted(summary['categories'].items()):
            print(f"   {category:20s}: {stats['count']:2d} tests, "
                  f"{stats['entities']:3d} entities, {stats['intents']:3d} intents")
        
        print("\n" + "="*70)
    
    def save_results(self, output_file: str = "comprehensive_test_results.json"):
        """Save test results to JSON file."""
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n✅ Results saved to: {output_path}")
    
    def run_interactive_mode(self):
        """Interactive testing mode."""
        print("\n" + "="*70)
        print("INTERACTIVE TESTING MODE")
        print("="*70)
        print("Enter queries to test (or 'quit' to exit):\n")
        
        while True:
            try:
                text = input("> ").strip()
                if text.lower() in ['quit', 'exit', 'q']:
                    break
                if not text:
                    continue
                
                result = self.test_query(text, category="interactive")
                self.print_result(result, show_details=True)
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def run_custom_tests(self, test_file: str):
        """Run tests from a custom JSON file."""
        test_path = Path(test_file)
        if not test_path.exists():
            print(f"❌ Test file not found: {test_path}")
            return
        
        with open(test_path, 'r') as f:
            custom_tests = json.load(f)
        
        print(f"\n📂 Loading {len(custom_tests)} custom test cases from {test_path}")
        
        for i, test_case in enumerate(custom_tests, 1):
            print(f"\n[Custom Test {i}/{len(custom_tests)}]")
            result = self.test_query(**test_case)
            self.print_result(result)
            self.results["test_cases"].append(result)
        
        self._generate_summary()
        self._print_summary()


def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive test suite for NER and Intent models"
    )
    parser.add_argument(
        "--ner-model",
        default="cyber-train/models/ner_model/model-best",
        help="Path to NER model"
    )
    parser.add_argument(
        "--intent-model",
        default="cyber-train/models/intent_model/model-best",
        help="Path to Intent model"
    )
    parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Run comprehensive test suite"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--custom",
        help="Run custom tests from JSON file"
    )
    parser.add_argument(
        "--save-results",
        default="comprehensive_test_results.json",
        help="Save results to JSON file"
    )
    parser.add_argument(
        "--text",
        help="Test a single query"
    )
    
    args = parser.parse_args()
    
    tester = ComprehensiveTester(
        ner_model_path=args.ner_model,
        intent_model_path=args.intent_model
    )
    
    tester.load_models()
    
    if not tester.ner_model and not tester.intent_model:
        print("❌ No models loaded. Exiting.")
        return
    
    if args.text:
        # Single query test
        result = tester.test_query(args.text, category="single_query")
        tester.print_result(result, show_details=True)
        tester.results["test_cases"].append(result)
        tester.save_results(args.save_results)
    
    elif args.interactive:
        tester.run_interactive_mode()
    
    elif args.custom:
        tester.run_custom_tests(args.custom)
        tester.save_results(args.save_results)
    
    elif args.comprehensive:
        tester.run_comprehensive_tests()
        tester.save_results(args.save_results)
    
    else:
        # Default: run comprehensive tests
        tester.run_comprehensive_tests()
        tester.save_results(args.save_results)


if __name__ == "__main__":
    main()

