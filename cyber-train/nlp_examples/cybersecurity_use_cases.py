#!/usr/bin/env python3
"""
Cybersecurity Use Cases - NER and Intent Classification Examples

This script demonstrates real-world cybersecurity scenarios:
- Incident response
- Threat hunting
- Vulnerability management
- Compliance auditing
- Security monitoring
"""

import spacy
from pathlib import Path
from typing import List, Dict
from datetime import datetime


def load_models():
    """Load the trained models."""
    ner_model = spacy.load("cyber-train/models/ner_model/model-best")
    intent_model = spacy.load("cyber-train/models/intent_model/model-best")
    return ner_model, intent_model


def incident_response_analysis(ner_model, intent_model):
    """Example: Incident response analysis."""
    print("="*70)
    print("USE CASE 1: INCIDENT RESPONSE ANALYSIS")
    print("="*70)
    
    incident_report = """
    Our security operations center detected a sophisticated attack campaign originating from 
    IP address 192.168.1.100 that began on 2024-12-15 at 14:30 UTC. The threat actor, identified 
    as APT29, used WannaCry ransomware variant to compromise multiple systems. The attack 
    targeted our domain controller at evil.com and attempted to exfiltrate sensitive customer 
    data. Our incident response team immediately blocked IP 192.168.1.100 at the firewall and 
    isolated the affected systems. The investigation revealed that the attacker gained initial 
    access through a phishing email sent to admin@company.com. We have notified law enforcement 
    and are working with our threat intelligence partners to track the campaign.
    """
    
    doc_ner = ner_model(incident_report)
    doc_intent = intent_model(incident_report)
    
    print("\n📋 Incident Report Analysis:")
    print(f"   Text length: {len(incident_report)} characters")
    
    print("\n🏷️  Entities Extracted:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Detected Intents:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def threat_hunting_query(ner_model, intent_model):
    """Example: Threat hunting query."""
    print("\n" + "="*70)
    print("USE CASE 2: THREAT HUNTING")
    print("="*70)
    
    hunting_query = """
    Hunt for indicators of APT28 activity in our network. Look for connections to known 
    command and control servers at IP 172.16.0.1 and domain c2.attack.net. Check for 
    WannaCry malware signatures and any lateral movement patterns. Focus on systems that 
    communicated with IP 10.0.0.5 between 2024-12-01 and 2024-12-15. Also investigate 
    any emails from suspicious domains like phishing@evil.com.
    """
    
    doc_ner = ner_model(hunting_query)
    doc_intent = intent_model(hunting_query)
    
    print("\n🔍 Threat Hunting Query Analysis:")
    
    print("\n🏷️  Threat Indicators Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Recommended Actions (Intents):")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def vulnerability_management(ner_model, intent_model):
    """Example: Vulnerability management."""
    print("\n" + "="*70)
    print("USE CASE 3: VULNERABILITY MANAGEMENT")
    print("="*70)
    
    vuln_query = """
    Scan our infrastructure for CVE-2021-44228 (Log4j) and CVE-2021-45046 vulnerabilities. 
    Check all systems with IP addresses in the range 192.168.1.0/24. Prioritize systems 
    accessible from the internet, especially those hosting web applications. Generate a 
    compliance report for PCI DSS and NIST CSF requirements. Ensure all patches are applied 
    by 2024-12-20.
    """
    
    doc_ner = ner_model(vuln_query)
    doc_intent = intent_model(vuln_query)
    
    print("\n🔒 Vulnerability Management Query Analysis:")
    
    print("\n🏷️  Security Entities Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Recommended Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def compliance_audit(ner_model, intent_model):
    """Example: Compliance audit."""
    print("\n" + "="*70)
    print("USE CASE 4: COMPLIANCE AUDIT")
    print("="*70)
    
    audit_query = """
    Conduct a comprehensive compliance audit for our organization. Verify that we meet 
    all requirements for HIPAA, PCI DSS, and SOC 2 Type II. Check that our data protection 
    measures comply with GDPR and CCPA regulations. Review our security controls against 
    NIST CSF framework. Generate a detailed compliance report for the audit scheduled on 
    2024-12-25.
    """
    
    doc_ner = ner_model(audit_query)
    doc_intent = intent_model(audit_query)
    
    print("\n📊 Compliance Audit Query Analysis:")
    
    print("\n🏷️  Compliance Entities Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Audit Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def security_monitoring(ner_model, intent_model):
    """Example: Security monitoring."""
    print("\n" + "="*70)
    print("USE CASE 5: SECURITY MONITORING")
    print("="*70)
    
    monitoring_query = """
    Monitor network traffic for suspicious activity. Alert on any connections to IP 8.8.8.8 
    from internal systems, as this could indicate data exfiltration. Track all DNS queries 
    to domain malware.evil.com and block them immediately. Monitor for Emotet and TrickBot 
    malware signatures. Set up alerts for any email addresses matching patterns from 
    phishing@evil.com. Report any anomalies detected in the last 24 hours.
    """
    
    doc_ner = ner_model(monitoring_query)
    doc_intent = intent_model(monitoring_query)
    
    print("\n👁️  Security Monitoring Query Analysis:")
    
    print("\n🏷️  Threat Indicators Found:")
    entities = [(e.text, e.label_) for e in doc_ner.ents]
    for entity_text, label in entities:
        print(f"   • {entity_text} → {label}")
    
    print("\n🎯 Monitoring Actions:")
    intents = sorted(doc_intent.cats.items(), key=lambda x: x[1], reverse=True)
    for intent, score in intents[:5]:
        if score >= 0.3:
            print(f"   • {intent}: {score:.4f} ({score*100:.1f}%)")
    
    return entities, intents


def main():
    """Run all cybersecurity use case examples."""
    print("="*70)
    print("CYBERSECURITY USE CASES - NER AND INTENT CLASSIFICATION")
    print("="*70)
    
    # Load models
    print("\n📦 Loading models...")
    ner_model, intent_model = load_models()
    print("✅ Models loaded successfully")
    
    # Run use cases
    incident_response_analysis(ner_model, intent_model)
    threat_hunting_query(ner_model, intent_model)
    vulnerability_management(ner_model, intent_model)
    compliance_audit(ner_model, intent_model)
    security_monitoring(ner_model, intent_model)
    
    print("\n" + "="*70)
    print("✅ CYBERSECURITY USE CASES COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()

