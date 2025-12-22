#!/usr/bin/env python3
"""
OSINT Use Cases - NER and Intent Classification Examples

This script demonstrates real-world OSINT scenarios:
- Social media investigation
- Threat actor attribution
- Geolocation analysis
- Image verification
- Domain investigation
"""

import spacy
from pathlib import Path
from typing import List, Dict


def load_models():
    """Load the trained models."""
    ner_model = spacy.load("cyber-train/models/ner_model/model-best")
    intent_model = spacy.load("cyber-train/models/intent_model/model-best")
    return ner_model, intent_model


def social_media_investigation(ner_model, intent_model):
    """Example: Social media investigation."""
    print("="*70)
    print("USE CASE 1: SOCIAL MEDIA INVESTIGATION")
    print("="*70)
    
    investigation_query = """
    Investigate the social media account @suspicious_user across multiple platforms. 
    The account has been spreading disinformation and we need to verify its authenticity. 
    Check Instagram profile at instagram.com/suspicious_user and Facebook page at 
    facebook.com/suspicious_user. Also investigate their LinkedIn profile and Telegram 
    channel. The account was last active on 2024-12-10 and has connections to known 
    threat actors. Verify the GPS coordinates latitude 40.7128 longitude -74.0060 
    associated with their posts.
    """
    
    doc_ner = ner_model(investigation_query)
    doc_intent = intent_model(investigation_query)
    
    print("\n🔍 Social Media Investigation Analysis:")
    
    print("\n🏷️  Entities Extracted:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Investigation Intents:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def threat_actor_attribution(ner_model, intent_model):
    """Example: Threat actor attribution."""
    print("\n" + "="*70)
    print("USE CASE 2: THREAT ACTOR ATTRIBUTION")
    print("="*70)
    
    attribution_query = """
    Attribute the recent cyber attack to a specific threat actor group. The attack 
    originated from IP address 172.16.0.1 and used techniques consistent with APT29 
    operations. The malware sample matches known Lazarus group tools. Investigate 
    connections to FIN7 and UNC2452 campaigns. The command and control server was 
    hosted at domain c2.attack.net. Cross-reference with threat intelligence feeds 
    to identify the threat actor.
    """
    
    doc_ner = ner_model(attribution_query)
    doc_intent = intent_model(attribution_query)
    
    print("\n🎭 Threat Actor Attribution Analysis:")
    
    print("\n🏷️  Threat Indicators Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Attribution Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def geolocation_analysis(ner_model, intent_model):
    """Example: Geolocation analysis."""
    print("\n" + "="*70)
    print("USE CASE 3: GEOLOCATION ANALYSIS")
    print("="*70)
    
    geo_query = """
    Perform geolocation analysis on images posted by the subject. Extract EXIF data 
    and verify GPS coordinates. The images contain metadata showing location at 
    latitude 37.7749 longitude -122.4194, which corresponds to San Francisco. 
    Verify the authenticity of these coordinates and check if they match the subject's 
    claimed location. Also analyze DMS coordinates 40°42'46"N 74°00'22"W found in 
    another image. Cross-reference with known locations and verify timestamps.
    """
    
    doc_ner = ner_model(geo_query)
    doc_intent = intent_model(geo_query)
    
    print("\n🌍 Geolocation Analysis:")
    
    print("\n🏷️  Geographic Entities Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Analysis Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def image_verification(ner_model, intent_model):
    """Example: Image verification."""
    print("\n" + "="*70)
    print("USE CASE 4: IMAGE VERIFICATION")
    print("="*70)
    
    verification_query = """
    ✅ Verify the authenticity of images posted on social media. Check for deepfake 
    indicators and verify EXIF metadata. The images claim to show events on 2024-12-15 
    at 14:30 UTC, but the metadata suggests they were created on 2024-12-10. Perform 
    reverse image search to find the original source. Verify GPS coordinates latitude 
    52.53076 longitude 13.38492 embedded in the image metadata. Check for any 
    manipulation or editing artifacts that would indicate the images are not authentic.
    """
    
    doc_ner = ner_model(verification_query)
    doc_intent = intent_model(verification_query)
    
    print("\n🖼️  Image Verification Analysis:")
    
    print("\n🏷️  Verification Entities Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Verification Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def domain_investigation(ner_model, intent_model):
    """Example: Domain investigation."""
    print("\n" + "="*70)
    print("USE CASE 5: DOMAIN INVESTIGATION")
    print("="*70)
    
    domain_query = """
    Investigate the suspicious domain malware.evil.com that has been associated with 
    phishing campaigns. Check WHOIS records and DNS history. Verify nameservers 
    ns1.example.com and ns2.example.com. The domain was registered using IP address 
    192.168.1.1 and email admin@company.org. Check for connections to known threat 
    actors and previous malicious activities. Verify if the domain is currently 
    active and what services it's hosting.
    """
    
    doc_ner = ner_model(domain_query)
    doc_intent = intent_model(domain_query)
    
    print("\n🌐 Domain Investigation Analysis:")
    
    print("\n🏷️  Domain Entities Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Investigation Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def main():
    """Run all OSINT use case examples."""
    print("="*70)
    print("OSINT USE CASES - NER AND INTENT CLASSIFICATION")
    print("="*70)
    
    # Load models
    print("\n📦 Loading models...")
    ner_model, intent_model = load_models()
    print("✅ Models loaded successfully")
    
    # Run use cases
    social_media_investigation(ner_model, intent_model)
    threat_actor_attribution(ner_model, intent_model)
    geolocation_analysis(ner_model, intent_model)
    image_verification(ner_model, intent_model)
    domain_investigation(ner_model, intent_model)
    
    print("\n" + "="*70)
    print("✅ OSINT USE CASES COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()

