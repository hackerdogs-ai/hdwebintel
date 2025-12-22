#!/usr/bin/env python3
"""
SaaS Operations Use Cases - NER and Intent Classification Examples

This script demonstrates real-world SaaS Operations scenarios:
- API monitoring
- Cloud infrastructure management
- AI model deployment
- Customer support
- Performance optimization
"""

import spacy
from pathlib import Path
from typing import List, Dict


def load_models():
    """Load the trained models."""
    ner_model = spacy.load("cyber-train/models/ner_model/model-best")
    intent_model = spacy.load("cyber-train/models/intent_model/model-best")
    return ner_model, intent_model


def api_monitoring(ner_model, intent_model):
    """Example: API monitoring."""
    print("="*70)
    print("USE CASE 1: API MONITORING")
    print("="*70)
    
    monitoring_query = """
    Monitor API usage for our GPT-4 and Claude-3 deployments. Track requests from 
    IP address 10.0.0.1 that are making excessive API calls. The customer using 
    IP 192.168.1.100 has been experiencing high latency. Check API endpoints for 
    GPT-4-turbo and Llama-2 models. Generate a usage report for the period from 
    2024-12-01 to 2024-12-15. Alert if any IP address exceeds 10,000 requests per hour.
    """
    
    doc_ner = ner_model(monitoring_query)
    doc_intent = intent_model(monitoring_query)
    
    print("\n📊 API Monitoring Analysis:")
    
    print("\n🏷️  Entities Extracted:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Monitoring Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def cloud_infrastructure(ner_model, intent_model):
    """Example: Cloud infrastructure management."""
    print("\n" + "="*70)
    print("USE CASE 2: CLOUD INFRASTRUCTURE MANAGEMENT")
    print("="*70)
    
    infra_query = """
    Manage our cloud infrastructure across multiple datacenters. Monitor AWS-US-EAST-1, 
    GCP-US-CENTRAL1, and Azure-EAST-US datacenters. Check network connectivity from 
    IP 172.16.0.1 to our cloud services. Optimize routing for customers connecting 
    from IP 8.8.8.8. Ensure compliance with SOC 2 Type II and FedRAMP requirements. 
    Generate infrastructure health reports for the last 7 days.
    """
    
    doc_ner = ner_model(infra_query)
    doc_intent = intent_model(infra_query)
    
    print("\n☁️  Cloud Infrastructure Analysis:")
    
    print("\n🏷️  Infrastructure Entities Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Infrastructure Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def ai_model_deployment(ner_model, intent_model):
    """Example: AI model deployment."""
    print("\n" + "="*70)
    print("USE CASE 3: AI MODEL DEPLOYMENT")
    print("="*70)
    
    deployment_query = """
    Deploy new AI models to production. We're rolling out GPT-4, Claude-3-Opus, and 
    Gemini-Pro models. Monitor performance metrics for each model. Track API usage 
    and costs for GPT-4-turbo and Llama-3 deployments. Ensure all models comply with 
    our security policies and data privacy requirements. Generate deployment reports 
    for models deployed on 2024-12-15.
    """
    
    doc_ner = ner_model(deployment_query)
    doc_intent = intent_model(deployment_query)
    
    print("\n🤖 AI Model Deployment Analysis:")
    
    print("\n🏷️  Model Entities Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Deployment Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def customer_support(ner_model, intent_model):
    """Example: Customer support."""
    print("\n" + "="*70)
    print("USE CASE 4: CUSTOMER SUPPORT")
    print("="*70)
    
    support_query = """
    Customer reported issues accessing our API from their network. They're connecting 
    from IP address 203.0.113.1 and experiencing timeouts. Check their account status 
    and API usage for GPT-4 and Claude-3 models. Verify their email contact@business.com 
    is properly configured. Review their service tier and ensure they have appropriate 
    rate limits. Generate a support ticket for this issue.
    """
    
    doc_ner = ner_model(support_query)
    doc_intent = intent_model(support_query)
    
    print("\n💬 Customer Support Analysis:")
    
    print("\n🏷️  Customer Entities Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Support Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def performance_optimization(ner_model, intent_model):
    """Example: Performance optimization."""
    print("\n" + "="*70)
    print("USE CASE 5: PERFORMANCE OPTIMIZATION")
    print("="*70)
    
    optimization_query = """
    Optimize performance for our AI model infrastructure. Analyze latency for GPT-4 
    and Claude-3 model requests. Customers from IP 192.168.1.1 are experiencing 
    slower response times. Implement caching strategies for frequently used models 
    like Llama-2 and PaLM-2. Optimize routing for requests from IP 10.0.0.1. Generate 
    performance reports comparing GPT-4-turbo and gpt-4o model response times.
    """
    
    doc_ner = ner_model(optimization_query)
    doc_intent = intent_model(optimization_query)
    
    print("\n⚡ Performance Optimization Analysis:")
    
    print("\n🏷️  Performance Entities Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Optimization Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def main():
    """Run all SaaS Operations use case examples."""
    print("="*70)
    print("SAAS OPERATIONS USE CASES - NER AND INTENT CLASSIFICATION")
    print("="*70)
    
    # Load models
    print("\n📦 Loading models...")
    ner_model, intent_model = load_models()
    print("✅ Models loaded successfully")
    
    # Run use cases
    api_monitoring(ner_model, intent_model)
    cloud_infrastructure(ner_model, intent_model)
    ai_model_deployment(ner_model, intent_model)
    customer_support(ner_model, intent_model)
    performance_optimization(ner_model, intent_model)
    
    print("\n" + "="*70)
    print("✅ SAAS OPERATIONS USE CASES COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()

