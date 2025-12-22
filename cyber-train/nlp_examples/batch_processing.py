#!/usr/bin/env python3
"""
Batch Processing Example - Process Multiple Queries Efficiently

This script demonstrates how to:
- Process multiple queries in batch
- Extract entities and intents efficiently
- Generate reports
- Handle errors gracefully
"""

import spacy
from pathlib import Path
from typing import List, Dict, Tuple
import json
from datetime import datetime


def load_models():
    """Load the trained models."""
    ner_model = spacy.load("cyber-train/models/ner_model/model-best")
    intent_model = spacy.load("cyber-train/models/intent_model/model-best")
    return ner_model, intent_model


def process_batch(queries: List[str], ner_model, intent_model) -> List[Dict]:
    """
    Process a batch of queries and return results.
    
    Args:
        queries: List of query strings
        ner_model: Loaded NER model
        intent_model: Loaded Intent model
    
    Returns:
        List of result dictionaries
    """
    results = []
    
    for i, query in enumerate(queries, 1):
        try:
            # Process with NER
            doc_ner = ner_model(query)
            entities = [(e.text, e.label_) for e in doc_ner.ents]
            
            # Process with Intent
            doc_intent = intent_model(query)
            intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
            intents = [(intent, score) for intent, score in intents if score >= 0.3]
            
            result = {
                "query_id": i,
                "query": query,
                "entities": entities,
                "entity_count": len(entities),
                "intents": intents[:5],  # Top 5 intents
                "intent_count": len(intents),
                "timestamp": datetime.now().isoformat()
            }
            results.append(result)
            
        except Exception as e:
            print(f"⚠️  Error processing query {i}: {e}")
            results.append({
                "query_id": i,
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    return results


def generate_report(results: List[Dict], output_file: str = "batch_processing_report.json"):
    """Generate a report from batch processing results."""
    total_queries = len(results)
    total_entities = sum(r.get("entity_count", 0) for r in results)
    total_intents = sum(r.get("intent_count", 0) for r in results)
    
    # Entity statistics
    entity_counts = {}
    for result in results:
        for entity_text, label in result.get("entities", []):
            entity_counts[label] = entity_counts.get(label, 0) + 1
    
    # Intent statistics
    intent_counts = {}
    for result in results:
        for intent, score in result.get("intents", []):
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
    
    report = {
        "summary": {
            "total_queries": total_queries,
            "total_entities": total_entities,
            "total_intents": total_intents,
            "average_entities_per_query": total_entities / total_queries if total_queries > 0 else 0,
            "average_intents_per_query": total_intents / total_queries if total_queries > 0 else 0,
        },
        "entity_statistics": dict(sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)),
        "intent_statistics": dict(sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)),
        "results": results,
        "generated_at": datetime.now().isoformat()
    }
    
    # Save report
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    return report


def main():
    """Main function demonstrating batch processing."""
    print("="*70)
    print("BATCH PROCESSING EXAMPLE")
    print("="*70)
    
    # Load models
    print("\n📦 Loading models...")
    ner_model, intent_model = load_models()
    print("✅ Models loaded successfully")
    
    # Sample batch of queries
    batch_queries = [
        "Check IP 192.168.1.1 for suspicious activity",
        "APT28 used WannaCry ransomware to attack IP 172.16.0.1",
        "🚨 Security alert: IP 192.168.1.1 compromised",
        "AI security incident involving GPT-4 from OpenAI",
        "Monitor AI model usage: GPT-4, Claude-3-Opus, Gemini-Pro",
        "Verify GPS coordinates latitude 40.7128 longitude -74.0060",
        "Check compliance with NIST CSF, PCI DSS, and HIPAA",
        "Investigate domain malware.evil.com for phishing activity",
        "Block IP 10.0.0.1 and isolate affected systems",
        "Generate threat intelligence report for APT29 campaign",
    ]
    
    print(f"\n📝 Processing {len(batch_queries)} queries...")
    
    # Process batch
    results = process_batch(batch_queries, ner_model, intent_model)
    
    # Generate report
    print("\n📊 Generating report...")
    report = generate_report(results, "nlp_examples/batch_processing_report.json")
    
    # Print summary
    print("\n" + "="*70)
    print("BATCH PROCESSING SUMMARY")
    print("="*70)
    print(f"\nTotal queries processed: {report['summary']['total_queries']}")
    print(f"Total entities found: {report['summary']['total_entities']}")
    print(f"Total intents found: {report['summary']['total_intents']}")
    print(f"Average entities per query: {report['summary']['average_entities_per_query']:.2f}")
    print(f"Average intents per query: {report['summary']['average_intents_per_query']:.2f}")
    
    print("\n🏷️  Top 10 Entity Types Found:")
    for label, count in list(report['entity_statistics'].items())[:10]:
        print(f"   • {label}: {count}")
    
    print("\n🎯 Top 10 Intent Types Found:")
    for intent, count in list(report['intent_statistics'].items())[:10]:
        print(f"   • {intent}: {count}")
    
    print(f"\n✅ Report saved to: nlp_examples/batch_processing_report.json")
    print("\n" + "="*70)
    print("✅ BATCH PROCESSING COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()

