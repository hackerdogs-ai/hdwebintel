#!/usr/bin/env python3
"""
Comprehensive OSINT entities and intents generator.
Generates 100 entities and 100 intents for each of 25 OSINT pillars.
"""

import json
import os
import re
from pathlib import Path

OSINT_PILLARS = [
    "ai_int", "comint", "cybint", "darkint", "digint", "dnint", "domain_intel",
    "ecoint", "eduint", "finint", "geoint", "humint", "imint", "infint",
    "legint", "masint", "medint", "natint", "orbint", "sigint", "socmint",
    "techint", "threat_intel", "tradint", "vatint"
]

BASE_PATH = "cyber-train/entities-intent/osint"
OSINT_DEF_PATH = "cyber-train/osint"

# Comprehensive metadata for each pillar (from osint_pillars.md)
PILLAR_DATA = {
    "socmint": {
        "tools": ["snscrape", "Sherlock", "OSINTgram", "Maltego CE", "SpiderFoot", "Meltwater", "Brandwatch", "SproutSocial", "Babel X", "Social Links"],
        "roles": ["SOCMINT Analyst", "Disinformation Researcher", "Data Scientist", "Digital Forensics Specialist", "Incident Responder"],
        "scenarios": ["disinformation campaigns", "extremist chatter", "influence operations", "brand reputation attacks", "viral misinformation", "coordinated botnets", "fake news", "sentiment analysis"]
    },
    "geoint": {
        "tools": ["QGIS", "SentinelSat", "OpenStreetMap", "Google Earth Pro", "GeoServer", "Planet Labs", "Maxar", "SkyWatch", "Esri ArcGIS", "Hexagon"],
        "roles": ["GEOINT Analyst", "Satellite Imagery Specialist", "Remote Sensing Engineer", "Crisis Response Team", "Geospatial Analyst"],
        "scenarios": ["conflict zones", "disaster response", "facility construction", "illegal activities", "location verification", "maritime tracking", "troop movements", "environmental monitoring"]
    },
    "imint": {
        "tools": ["ExifTool", "ffmpeg", "Image Analyzer", "OpenCV", "InVID", "Amped Authenticate", "Magnet Axiom", "Adobe Photoshop", "Clearview AI", "ShadowDragon"],
        "roles": ["Forensic Analyst", "Verification Specialist", "Imagery Scientist", "Deepfake Detector", "Image Analyst"],
        "scenarios": ["deepfake detection", "object identification", "geolocation", "authenticity verification", "change analysis", "image forensics", "metadata extraction", "reverse image search"]
    },
    "humint": {
        "tools": ["Maigret", "GHunt", "Little Brother", "theHarvester", "Recon-ng", "Pipl", "Skopenow", "Spokeo", "Lampyre", "PeopleXploit"],
        "roles": ["OSINT Analyst", "Cybercrime Investigator", "Insider Risk Analyst", "Fraud Investigator", "Background Check Specialist"],
        "scenarios": ["background checks", "persona attribution", "identity verification", "insider risk", "alias resolution", "employment verification", "social engineering assessment", "reputation analysis"]
    },
    "sigint": {
        "tools": ["Wireshark", "Zeek", "Snort", "rtl_433", "GNU Radio", "GreyNoise", "Censys", "Farsight DNSDB", "Palantir COMINT", "SignalGuard"],
        "roles": ["SIGINT Analyst", "RF Data Engineer", "Spectrum Threat Hunter", "Aviation Signal Specialist", "Maritime Signal Analyst"],
        "scenarios": ["ADS-B tracking", "AIS monitoring", "IoT device analysis", "RF emissions", "unauthorized communications", "signal spoofing", "spectrum analysis", "radio frequency monitoring"]
    },
    "comint": {
        "tools": ["rtl_433", "GNU Radio", "SDR#", "OpenWebRX", "SigDigger", "Palantir COMINT", "SignalGuard", "Krypto500", "Rohde & Schwarz", "TCI Model"],
        "roles": ["COMINT Collection Officer", "Voice Analyst", "Network Telephony Analyst", "Spectrum Analyst", "Communications Specialist"],
        "scenarios": ["VoIP monitoring", "radio chatter", "public broadcasts", "communication patterns", "anomaly detection", "call metadata", "voice analysis", "telephony intelligence"]
    },
    "masint": {
        "tools": ["Seiscomp3", "GNU Radio", "ObsPy", "Pyrocko", "MSNoise", "Janes MASINT", "Hexagon Geospatial", "Geospiza", "SeismicAI", "BlackSky"],
        "roles": ["MASINT Engineer", "Seismologist", "Acoustic Analyst", "Nuclear Detection Specialist", "Measurement Analyst"],
        "scenarios": ["nuclear test detection", "seismic monitoring", "acoustic signatures", "geological changes", "environmental anomalies", "vibration analysis", "signature intelligence", "measurement analysis"]
    },
    "domain_intel": {
        "tools": ["Amass", "Sublist3r", "theHarvester", "DNSRecon", "Fierce", "DomainTools", "SecurityTrails", "RiskIQ", "WhoisXML API", "Farsight DNSDB"],
        "roles": ["Threat Hunter", "Infrastructure Analyst", "DNS Specialist", "Subdomain Discovery Specialist", "Domain Analyst"],
        "scenarios": ["subdomain discovery", "phishing detection", "infrastructure mapping", "DNS changes", "certificate anomalies", "domain registration", "whois analysis", "DNS enumeration"]
    },
    "threat_intel": {
        "tools": ["MISP", "YARA", "Sigma", "OpenCTI", "ThreatCrowd", "Recorded Future", "Flashpoint", "Anomali", "ThreatConnect", "IntSights"],
        "roles": ["Threat Intel Analyst", "Malware Researcher", "Dark Web Analyst", "Data Engineer", "CTI Analyst"],
        "scenarios": ["IOC enrichment", "adversary tracking", "campaign attribution", "threat landscape", "real-time feeds", "malware analysis", "TTP mapping", "threat actor profiling"]
    },
    "cybint": {
        "tools": ["OpenCTI", "ATT&CK Navigator", "Cuckoo Sandbox", "SpiderFoot", "Recon-ng", "CrowdStrike", "FireEye iSight", "Palo Alto Unit 42", "IBM X-Force", "Maltego"],
        "roles": ["Cyber Threat Analyst", "Malware Reverse Engineer", "Threat Hunter", "Vulnerability Intelligence Analyst", "Cyber Intelligence Analyst"],
        "scenarios": ["intrusion detection", "malware intelligence", "incident response", "threat actor infrastructure", "zero-day intel", "exploit tracking", "vulnerability analysis", "cyber attribution"]
    },
    "techint": {
        "tools": ["Nmap", "WhatWeb", "Wappalyzer", "Metasploit", "Nessus", "Qualys", "Rapid7 Nexpose", "Tenable.io", "ImmuniWeb", "Acunetix"],
        "roles": ["Reverse Engineer", "Exploit Developer", "Security Researcher", "Vulnerability Analyst", "Technical Analyst"],
        "scenarios": ["vulnerability research", "exploit detection", "technology fingerprinting", "attack surface mapping", "misconfiguration identification", "penetration testing", "security assessment", "technical intelligence"]
    },
    "darkint": {
        "tools": ["OnionScan", "TorBot", "Darkdump", "Ahmia", "Hunchly", "DarkOwl", "IntSights", "Flashpoint", "Recorded Future", "KELA"],
        "roles": ["Dark Web Analyst", "Threat Intelligence Analyst", "Crypto Intelligence Analyst", "Threat Researcher", "Dark Web Investigator"],
        "scenarios": ["data leak detection", "ransomware tracking", "threat actor communications", "stolen credentials", "illicit markets", "dark web forums", "cryptocurrency tracing", "underground monitoring"]
    },
    "finint": {
        "tools": ["OpenSanctions", "BusinessRadar", "Aleph", "OpenCorporates", "FEC.gov", "Orbis", "World-Check", "PitchBook", "Dow Jones Risk", "LexisNexis Bridger"],
        "roles": ["FININT Analyst", "Blockchain Tracer", "Forensic Accountant", "Beneficial Ownership Analyst", "Financial Crime Analyst"],
        "scenarios": ["money laundering", "sanctions evasion", "terrorist financing", "corporate fraud", "cryptocurrency tracing", "transaction monitoring", "AML compliance", "financial investigation"]
    },
    "ecoint": {
        "tools": ["TradeMapAPI", "OpenTradeStats", "World Bank Data", "IMF Data", "UN Comtrade", "Refinitiv", "Bloomberg", "S&P Global", "IHS Markit", "Fitch Solutions"],
        "roles": ["Trade Analyst", "Supply Chain Researcher", "Economist", "Market Analyst", "Economic Intelligence Analyst"],
        "scenarios": ["sanctions impact", "resource dependencies", "trade patterns", "economic risks", "supply chain vulnerabilities", "market analysis", "economic forecasting", "trade intelligence"]
    },
    "medint": {
        "tools": ["WHO Epidata", "EpiJSON", "HealthMap", "ProMED-mail", "BioCaster", "BlueDot", "HealthMap", "Metabiota", "EIOS", "GIDEON"],
        "roles": ["Epidemiologist", "Health Intel Analyst", "Public Health Researcher", "Outbreak Investigator", "Medical Intelligence Analyst"],
        "scenarios": ["pandemic monitoring", "outbreak detection", "disease spread", "health trends", "crisis response", "epidemiological analysis", "public health intelligence", "disease surveillance"]
    },
    "legint": {
        "tools": ["CaseLawAccess", "CourtListener", "RECAP", "Justia", "OpenJurist", "LexisNexis", "Westlaw", "Bloomberg Law", "Fastcase", "Casetext"],
        "roles": ["Legal Researcher", "Compliance Analyst", "Paralegal", "Litigation Support Specialist", "Legal Intelligence Analyst"],
        "scenarios": ["litigation support", "compliance audits", "regulatory changes", "legal proceedings", "legal risks", "case research", "legal document analysis", "regulatory intelligence"]
    },
    "dnint": {
        "tools": ["BGPStream", "RIPEstat", "CAIDA", "PeeringDB", "OpenINTEL", "Kentik", "ThousandEyes", "Arbor Networks", "Cisco ThousandEyes", "Nokia Deepfield"],
        "roles": ["Network Security Analyst", "BGP Specialist", "Internet Researcher", "Network Topology Analyst", "Digital Network Analyst"],
        "scenarios": ["BGP leak detection", "network infrastructure mapping", "routing changes", "network anomalies", "internet topology", "ASN analysis", "routing intelligence", "network security"]
    },
    "vatint": {
        "tools": ["adsbSnoop", "AIS-catcher", "OpenSky Network", "FlightAware", "MarineTraffic", "MarineTraffic", "FlightRadar24", "VesselFinder", "PlaneFinder", "ShipFinder"],
        "roles": ["Transportation OSINT Analyst", "Aviation Specialist", "Maritime Analyst", "Customs Enforcement Officer", "Vehicle Tracking Analyst"],
        "scenarios": ["ADS-B plane tracking", "AIS vessel movements", "suspicious routes", "customs enforcement", "transportation security", "flight tracking", "ship monitoring", "vehicle intelligence"]
    },
    "orbint": {
        "tools": ["STK Free", "Skyfield", "Heavens-Above", "CelesTrak", "SatNOGS", "LeoLabs", "Spire Global", "Planet Labs", "Maxar", "NorthStar"],
        "roles": ["Remote Sensing Analyst", "Orbital Mechanics Specialist", "Satellite Tracking Analyst", "Space Situational Awareness Officer", "Orbital Intelligence Analyst"],
        "scenarios": ["satellite tracking", "orbital debris monitoring", "space events", "space situational awareness", "space threats", "orbital analysis", "satellite intelligence", "space monitoring"]
    },
    "tradint": {
        "tools": ["UN Comtrade API", "OpenCorporates", "Panjiva", "ImportGenius", "TradeAtlas", "Panjiva", "ImportGenius", "Descartes Datamyne", "PIERS", "Kuehne + Nagel"],
        "roles": ["Trade Analyst", "Market Researcher", "Supply Chain Analyst", "Customs Intelligence Officer", "Trade Intelligence Analyst"],
        "scenarios": ["import/export flows", "sanctions violations", "supply chain mapping", "trade anomalies", "customs intelligence", "trade pattern analysis", "supply chain intelligence", "trade monitoring"]
    },
    "digint": {
        "tools": ["MITMproxy", "MobSF", "Frida", "Burp Suite", "Wireshark", "Cellebrite", "Grayshift", "Oxygen Forensics", "Magnet Forensics", "Paraben E3"],
        "roles": ["IoT Analyst", "Forensic Team Member", "Mobile Security Analyst", "Digital Forensics Specialist", "Digital Intelligence Analyst"],
        "scenarios": ["IoT telemetry", "app metadata", "device fingerprints", "digital footprints", "forensic investigations", "mobile device analysis", "digital evidence", "device intelligence"]
    },
    "ai_int": {
        "tools": ["HuggingFace Models", "DetectGPT", "OpenAI API", "TensorFlow", "PyTorch", "Fiddler AI", "TruEra", "OpenAI moderation", "IBM Watson", "Google AI"],
        "roles": ["AI Threat Analyst", "Synthetic Media Investigator", "Adversarial ML Researcher", "Prompt Security Engineer", "AI Intelligence Analyst"],
        "scenarios": ["AI-powered disinformation", "adversarial ML attacks", "AI-assisted cybercrime", "synthetic identity", "model provenance", "deepfake detection", "AI model analysis", "synthetic media"]
    },
    "infint": {
        "tools": ["InVID", "Hoaxy", "Botometer", "NewsGuard", "Graphika", "NewsGuard", "Graphika", "Logically", "Cyabra", "Yonder"],
        "roles": ["Fact-checker", "Disinformation Researcher", "Verification Specialist", "Narrative Analyst", "Information Environment Analyst"],
        "scenarios": ["fake news debunking", "narrative analysis", "bot network detection", "disinformation campaigns", "information verification", "fact-checking", "narrative tracking", "information warfare"]
    },
    "eduint": {
        "tools": ["OpenAlex", "Semantic Scholar API", "arXiv API", "PubMed", "ORCID", "Elsevier Scopus", "Web of Science", "Dimensions.ai", "Quid Pro", "LexisNexis Academic"],
        "roles": ["Academic Intelligence Analyst", "Research Analyst", "Talent Tracker", "Technology Intelligence Specialist", "Educational Intelligence Analyst"],
        "scenarios": ["emerging technologies", "research espionage", "academic collaborations", "talent migration", "campus activism", "research analysis", "academic intelligence", "technology tracking"]
    },
    "natint": {
        "tools": ["FAOSTAT", "UN Comtrade", "World Bank Open Data", "USGS Earth Explorer", "Global Forest Watch", "Palantir Foundry", "Bloomberg Terminal", "Refinitiv Eikon", "Wood Mackenzie", "S&P Global"],
        "roles": ["Resource Analyst", "Geospatial Specialist", "Commodity Researcher", "Environmental Analyst", "Natural Resources Analyst"],
        "scenarios": ["resource conflicts", "strategic dependencies", "illegal exploitation", "climate-driven scarcity", "supply chain decisions", "resource monitoring", "environmental intelligence", "commodity analysis"]
    }
}

def find_entity_spans(text, terms):
    """Find entity spans in text."""
    entities = []
    text_lower = text.lower()
    
    # Find roles
    for role in terms.get("roles", []):
        role_lower = role.lower()
        idx = text_lower.find(role_lower)
        if idx != -1:
            entities.append([idx, idx + len(role), "ROLE"])
    
    # Find tools
    for tool in terms.get("tools", []):
        tool_lower = tool.lower()
        idx = text_lower.find(tool_lower)
        if idx != -1:
            entities.append([idx, idx + len(tool), "TOOL"])
    
    # Find scenarios (partial matches)
    for scenario in terms.get("scenarios", []):
        words = scenario.split()
        for word in words:
            if len(word) > 4:  # Only match significant words
                word_lower = word.lower()
                idx = text_lower.find(word_lower)
                if idx != -1:
                    entities.append([idx, idx + len(word), "SCENARIO"])
    
    # Remove overlapping entities, keep longest
    entities = sorted(entities, key=lambda x: (x[0], -x[1]))
    filtered = []
    for ent in entities:
        if not any(ent[0] >= f[0] and ent[1] <= f[1] and ent != f for f in filtered):
            filtered.append(ent)
    
    return sorted(filtered, key=lambda x: x[0])

def generate_entities(pillar):
    """Generate 100 entity examples."""
    entities = []
    data = PILLAR_DATA.get(pillar, {})
    
    roles = data.get("roles", ["Analyst"])
    tools = data.get("tools", ["Tool"])
    scenarios = data.get("scenarios", ["intelligence"])
    
    # Entity generation patterns
    patterns = [
        "{role} used {tool} to analyze {scenario}",
        "{tool} enabled {role} to detect {scenario}",
        "{role} conducted {scenario} investigation using {tool}",
        "{tool} platform detected {scenario} requiring {role} review",
        "{role} monitored {scenario} with {tool} dashboard",
        "{role} identified {scenario} through {tool} analysis",
        "{tool} provided {scenario} intelligence to {role}",
        "{role} validated {scenario} using {tool} verification",
        "{tool} scanned {scenario} data for {role} review",
        "{role} tracked {scenario} patterns with {tool} system"
    ]
    
    for i in range(100):
        role = roles[i % len(roles)]
        tool = tools[i % len(tools)]
        scenario = scenarios[i % len(scenarios)]
        pattern = patterns[i % len(patterns)]
        
        text = pattern.format(role=role, tool=tool, scenario=scenario)
        entity_spans = find_entity_spans(text, data)
        
        entities.append({
            "text": text,
            "entities": entity_spans
        })
    
    return entities

def generate_intents(pillar):
    """Generate 100 intent examples."""
    intents = []
    data = PILLAR_DATA.get(pillar, {})
    
    scenarios = data.get("scenarios", ["intelligence"])
    tools = data.get("tools", ["tool"])
    
    intent_patterns = [
        "I need to monitor {scenario} using {tool}",
        "Please detect {scenario} with {tool} analysis",
        "Analyze {scenario} data using {tool} platform",
        "Track {scenario} patterns with {tool}",
        "Investigate {scenario} using {tool} intelligence",
        "Monitor {scenario} for threats with {tool}",
        "Detect {scenario} anomalies using {tool}",
        "Analyze {scenario} trends with {tool} dashboard",
        "Track {scenario} activities using {tool}",
        "Investigate {scenario} incidents with {tool}"
    ]
    
    base_cats = {
        "MONITOR": 1.0,
        "DETECT": 1.0,
        "ANALYZE": 1.0,
        "TRACK": 1.0,
        "INVESTIGATE": 1.0,
        "AUDIT_COMPLIANCE": 0.0,
        "RESPOND_TO_INCIDENT": 0.0,
        "DEFINE_STRATEGY": 0.0
    }
    
    for i in range(100):
        scenario = scenarios[i % len(scenarios)]
        tool = tools[i % len(tools)]
        pattern = intent_patterns[i % len(intent_patterns)]
        
        text = pattern.format(scenario=scenario, tool=tool)
        
        cats = base_cats.copy()
        if i % 3 == 0:
            cats["AUDIT_COMPLIANCE"] = 0.5
        if i % 5 == 0:
            cats["RESPOND_TO_INCIDENT"] = 0.7
        if i % 7 == 0:
            cats["DEFINE_STRATEGY"] = 0.6
        
        intents.append({
            "text": text,
            "cats": cats
        })
    
    return intents

# Main execution
print(f"Generating entities and intents for {len(OSINT_PILLARS)} OSINT pillars...\n")

for pillar in OSINT_PILLARS:
    print(f"Processing {pillar}...", end=" ")
    
    try:
        entities = generate_entities(pillar)
        intents = generate_intents(pillar)
        
        pillar_dir = f"{BASE_PATH}/{pillar}"
        os.makedirs(pillar_dir, exist_ok=True)
        
        with open(f"{pillar_dir}/{pillar}_entities.jsonl", 'w', encoding='utf-8') as f:
            for entity in entities:
                f.write(json.dumps(entity, ensure_ascii=False) + '\n')
        
        with open(f"{pillar_dir}/{pillar}_intent.jsonl", 'w', encoding='utf-8') as f:
            for intent in intents:
                f.write(json.dumps(intent, ensure_ascii=False) + '\n')
        
        print(f"✅ {len(entities)} entities, {len(intents)} intents")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

print(f"\n✅ Completed all {len(OSINT_PILLARS)} OSINT pillars!")

