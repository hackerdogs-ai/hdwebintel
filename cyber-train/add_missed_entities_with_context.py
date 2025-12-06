#!/usr/bin/env python3
"""
Add high-quality training examples for missed entity types.
Focuses on top 15 missed entity types with proper context and uniqueness.
"""

import json
import re
import random
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set, Tuple, Optional
from datetime import datetime, timedelta

# Track added entities to ensure uniqueness
added_entities: Dict[str, Set[str]] = defaultdict(set)

# Malware types with context
MALWARE_EXAMPLES = [
    ("WannaCry ransomware has been detected in the network infrastructure, requiring immediate containment and isolation procedures.", "WannaCry", "MALWARE_TYPE"),
    ("The security team identified NotPetya malware variant spreading through the enterprise network, causing significant disruption to critical systems.", "NotPetya", "MALWARE_TYPE"),
    ("Zeus banking trojan was found on several endpoints, indicating a potential financial fraud campaign targeting customer accounts.", "Zeus", "MALWARE_TYPE"),
    ("Emotet malware family has been actively distributing through malicious email attachments, bypassing traditional security controls.", "Emotet", "MALWARE_TYPE"),
    ("TrickBot trojan was detected attempting to establish command and control communications with external threat actor infrastructure.", "TrickBot", "MALWARE_TYPE"),
    ("Stuxnet worm was discovered targeting industrial control systems, representing a sophisticated nation-state attack vector.", "Stuxnet", "MALWARE_TYPE"),
    ("Conficker worm continues to propagate across unpatched systems, requiring immediate patch deployment and network segmentation.", "Conficker", "MALWARE_TYPE"),
    ("Code Red worm variant was identified scanning for vulnerable web servers, attempting to exploit known security vulnerabilities.", "Code Red", "MALWARE_TYPE"),
    ("Ryuk ransomware has encrypted critical business files, demanding cryptocurrency payment for decryption keys and data recovery.", "Ryuk", "MALWARE_TYPE"),
    ("LockBit ransomware group has deployed their malware variant, exfiltrating sensitive data before encrypting systems.", "LockBit", "MALWARE_TYPE"),
    ("REvil ransomware was detected in the environment, targeting high-value assets and demanding substantial ransom payments.", "REvil", "MALWARE_TYPE"),
    ("Maze ransomware campaign has compromised multiple systems, threatening to publish stolen data if ransom demands are not met.", "Maze", "MALWARE_TYPE"),
    ("Sodinokibi ransomware variant has been identified, using sophisticated encryption algorithms to lock critical business data.", "Sodinokibi", "MALWARE_TYPE"),
    ("GandCrab ransomware family has been active, targeting organizations with weak security postures and outdated systems.", "GandCrab", "MALWARE_TYPE"),
    ("Cerber ransomware was found on several workstations, encrypting local files and network shares accessible to infected systems.", "Cerber", "MALWARE_TYPE"),
    ("CryptoLocker ransomware has been detected, using strong encryption to render files inaccessible without the decryption key.", "CryptoLocker", "MALWARE_TYPE"),
    ("Petya ransomware variant has infected the master boot record, preventing system startup and requiring specialized recovery procedures.", "Petya", "MALWARE_TYPE"),
    ("SamSam ransomware has been deployed through compromised credentials, targeting specific high-value systems for maximum impact.", "SamSam", "MALWARE_TYPE"),
    ("BadRabbit ransomware was identified spreading through fake software updates, exploiting user trust to gain system access.", "BadRabbit", "MALWARE_TYPE"),
    ("Dharma ransomware family has been active, using automated distribution methods to infect multiple systems simultaneously.", "Dharma", "MALWARE_TYPE"),
]

# Hash examples with context
HASH_EXAMPLES = [
    ("The file integrity check revealed MD5 hash 5d41402abc4b2a76b9719d911017c592 does not match the expected value, indicating potential tampering.", "5d41402abc4b2a76b9719d911017c592", "HASH"),
    ("SHA1 hash aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d was calculated for the suspicious executable file during forensic analysis.", "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d", "HASH"),
    ("SHA256 hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 was verified against the known good baseline for system files.", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "HASH"),
    ("The malware sample's MD5 checksum 098f6bcd4621d373cade4e832627b4f6 was submitted to threat intelligence platforms for analysis.", "098f6bcd4621d373cade4e832627b4f6", "HASH"),
    ("Forensic investigators calculated SHA1 fingerprint 356a192b7913b04c54574d18c28d46e6395428ab for the compromised database backup file.", "356a192b7913b04c54574d18c28d46e6395428ab", "HASH"),
    ("The file hash SHA256 2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae was used to identify the malicious payload.", "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae", "HASH"),
    ("MD5 hash d41d8cd98f00b204e9800998ecf8427e was computed for the empty file, confirming no data corruption occurred during transfer.", "d41d8cd98f00b204e9800998ecf8427e", "HASH"),
    ("The security team verified SHA1 hash 0beec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33 for the application binary before deployment to production.", "0beec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33", "HASH"),
    ("SHA256 fingerprint 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 was generated for the system configuration file.", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", "HASH"),
    ("The incident response team calculated MD5 checksum 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d for the suspicious process memory dump.", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d", "HASH"),
    ("File integrity monitoring detected SHA1 hash 2ef7bde608ce5404e97d5f042f95f89f1c232871 differs from the baseline, triggering security alert.", "2ef7bde608ce5404e97d5f042f95f89f1c232871", "HASH"),
    ("The malware analysis report included SHA256 hash 60303ae22b998861bce3b28f33eec1be758a213c86c93c076dbe9f558c11c752 for the malicious payload sample.", "60303ae22b998861bce3b28f33eec1be758a213c86c93c076dbe9f558c11c752", "HASH"),
    ("MD5 hash 7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730 was computed during the digital forensics investigation.", "7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730", "HASH"),
    ("The security scanner verified SHA1 hash 356a192b7913b04c54574d18c28d46e6395428ab for the system library file to ensure authenticity.", "356a192b7913b04c54574d18c28d46e6395428ab", "HASH"),
    ("SHA256 hash 2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae was used to identify the compromised application binary.", "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae", "HASH"),
]

# Emoji examples with context
EMOJI_EXAMPLES = [
    ("The social media post contained suspicious emoji 🚨 indicating potential security threat or phishing attempt targeting users.", "🚨", "EMOJI"),
    ("The threat actor used emoji 💀 in their communication, suggesting malicious intent and potential data breach campaign.", "💀", "EMOJI"),
    ("Security analysts identified emoji ⚠️ in the phishing email, warning users about potential fraudulent activity and credential theft.", "⚠️", "EMOJI"),
    ("The malicious message included emoji 🔥 to create urgency and encourage immediate action, typical of social engineering attacks.", "🔥", "EMOJI"),
    ("The suspicious communication contained emoji 💰 indicating financial motivation behind the cyber attack targeting customer accounts.", "💰", "EMOJI"),
    ("The phishing campaign used emoji 🎁 to lure victims into clicking malicious links and downloading malware-infected attachments.", "🎁", "EMOJI"),
    ("Security monitoring detected emoji ⚡ in the threat actor's communication, suggesting rapid attack execution and data exfiltration.", "⚡", "EMOJI"),
    ("The social engineering attempt included emoji 🏆 to create false sense of achievement and encourage user interaction with malicious content.", "🏆", "EMOJI"),
    ("The threat intelligence report noted emoji 🎯 in the attacker's messages, indicating targeted attack against specific organization.", "🎯", "EMOJI"),
    ("The malicious communication used emoji 🔐 to create false sense of security and trick users into providing sensitive credentials.", "🔐", "EMOJI"),
    ("Security analysts identified emoji 🚫 in the threat actor's communication, suggesting blocking or denial of service attack campaign.", "🚫", "EMOJI"),
    ("The phishing email contained emoji ✅ to create false sense of legitimacy and encourage users to click malicious links.", "✅", "EMOJI"),
    ("The social media threat used emoji 🎪 to distract users from identifying the malicious nature of the communication.", "🎪", "EMOJI"),
    ("The security alert noted emoji 🔍 in the suspicious message, indicating potential reconnaissance activity or information gathering.", "🔍", "EMOJI"),
    ("The threat actor's communication included emoji 🎭 to mask their true identity and create false persona for social engineering.", "🎭", "EMOJI"),
]

# Date examples with context
def generate_date_examples():
    """Generate diverse date examples with context."""
    dates = []
    base_date = datetime.now()
    
    formats = [
        ("%Y-%m-%d", "The security incident occurred on 2024-11-30, requiring immediate incident response and containment procedures."),
        ("%m/%d/%Y", "The vulnerability was discovered on 11/30/2024, affecting multiple systems and requiring urgent patch deployment."),
        ("%d-%m-%Y", "The data breach was detected on 30-11-2024, compromising sensitive customer information and triggering regulatory notification requirements."),
        ("%B %d, %Y", "The security audit was completed on November 30, 2024, identifying several compliance gaps and recommending remediation actions."),
        ("%Y-%m-%d", "The threat intelligence feed was updated on 2024-12-01, providing new indicators of compromise for active threat campaigns."),
        ("%m/%d/%Y", "The penetration test was scheduled for 12/15/2024, targeting critical infrastructure and application security controls."),
        ("%d-%m-%Y", "The security awareness training was conducted on 15-12-2024, educating employees about phishing attacks and social engineering tactics."),
        ("%B %d, %Y", "The compliance assessment was performed on December 20, 2024, evaluating adherence to regulatory requirements and industry standards."),
    ]
    
    for fmt, template in formats:
        date_str = base_date.strftime(fmt)
        date_obj = base_date
        text = template.replace(date_str, date_str)  # Ensure date is in text
        dates.append((text, date_str, "DATE"))
        base_date += timedelta(days=random.randint(1, 30))
    
    return dates

# Compliance framework examples
COMPLIANCE_EXAMPLES = [
    ("The organization must maintain PCI DSS compliance to process credit card transactions securely and protect customer payment data.", "PCI DSS", "COMPLIANCE_FRAMEWORK"),
    ("Healthcare organizations are required to comply with HIPAA regulations to protect patient health information and ensure privacy safeguards.", "HIPAA", "COMPLIANCE_FRAMEWORK"),
    ("The cloud service provider achieved SOC 2 Type II certification, demonstrating effective security controls and operational procedures.", "SOC 2", "COMPLIANCE_FRAMEWORK"),
    ("Federal agencies must comply with FedRAMP requirements when using cloud services, ensuring security and compliance with government standards.", "FedRAMP", "COMPLIANCE_FRAMEWORK"),
    ("The cybersecurity framework NIST CSF provides guidelines for managing and reducing cybersecurity risks across critical infrastructure sectors.", "NIST CSF", "COMPLIANCE_FRAMEWORK"),
    ("Organizations handling defense contracts must achieve CMMC Level 3 certification to demonstrate advanced cybersecurity maturity and protection capabilities.", "CMMC", "COMPLIANCE_FRAMEWORK"),
    ("The Federal Information Security Management Act FISMA requires federal agencies to implement comprehensive information security programs.", "FISMA", "COMPLIANCE_FRAMEWORK"),
    ("Cryptographic modules must comply with FIPS 140-2 standards to ensure secure implementation of encryption algorithms and key management.", "FIPS 140-2", "COMPLIANCE_FRAMEWORK"),
    ("The General Data Protection Regulation GDPR requires organizations to protect personal data and respect individual privacy rights.", "GDPR", "COMPLIANCE_FRAMEWORK"),
    ("California Consumer Privacy Act CCPA mandates businesses to disclose data collection practices and provide consumers with privacy control options.", "CCPA", "COMPLIANCE_FRAMEWORK"),
    ("The Personal Information Protection and Electronic Documents Act PIPEDA governs how private sector organizations collect and use personal information.", "PIPEDA", "COMPLIANCE_FRAMEWORK"),
    ("ISO 27001 certification demonstrates an organization's commitment to information security management and risk mitigation practices.", "ISO 27001", "COMPLIANCE_FRAMEWORK"),
    ("The Sarbanes-Oxley Act SOX requires public companies to implement internal controls and ensure financial reporting accuracy and security.", "SOX", "COMPLIANCE_FRAMEWORK"),
    ("The Payment Card Industry Data Security Standard PCI DSS Level 1 compliance is mandatory for merchants processing over 6 million transactions annually.", "PCI DSS", "COMPLIANCE_FRAMEWORK"),
]

# URL examples with context
URL_EXAMPLES = [
    ("The security team identified malicious URL https://malicious-domain.com/phishing-page attempting to steal user credentials through social engineering.", "https://malicious-domain.com/phishing-page", "URL"),
    ("The threat intelligence feed reported suspicious domain http://compromised-server.net/exploit hosting malware and command and control infrastructure.", "http://compromised-server.net/exploit", "URL"),
    ("The phishing email contained malicious link https://fake-bank.com/login designed to harvest banking credentials and compromise customer accounts.", "https://fake-bank.com/login", "URL"),
    ("Security monitoring detected connection to suspicious URL https://c2-server.com/beacon indicating potential command and control communication with threat actors.", "https://c2-server.com/beacon", "URL"),
    ("The malware sample attempted to download additional payload from URL http://malware-distribution.net/payload.exe during execution and system compromise.", "http://malware-distribution.net/payload.exe", "URL"),
    ("The security investigation revealed data exfiltration to external URL https://data-theft.com/upload through encrypted communication channels.", "https://data-theft.com/upload", "URL"),
    ("The web application firewall blocked access to malicious URL https://attack-vector.com/exploit attempting to exploit known vulnerabilities.", "https://attack-vector.com/exploit", "URL"),
    ("The threat actor used URL https://legitimate-looking.com/malicious to host phishing content and bypass traditional security controls.", "https://legitimate-looking.com/malicious", "URL"),
    ("Security analysts identified command and control URL https://c2-infrastructure.com/register used by ransomware operators to manage infected systems.", "https://c2-infrastructure.com/register", "URL"),
    ("The incident response team discovered data breach notification URL https://breach-notification.com/alert indicating potential customer data exposure.", "https://breach-notification.com/alert", "URL"),
    ("The malware campaign used URL https://malware-campaign.com/download to distribute additional malicious components and maintain persistence.", "https://malware-campaign.com/download", "URL"),
    ("The security scan detected suspicious URL https://suspicious-domain.org/scan attempting to probe network infrastructure and identify vulnerable systems.", "https://suspicious-domain.org/scan", "URL"),
    ("The phishing attack utilized URL https://fake-service.com/verify to trick users into providing sensitive authentication credentials.", "https://fake-service.com/verify", "URL"),
    ("The threat intelligence report identified malicious URL https://threat-actor.com/command used for remote access and system control by attackers.", "https://threat-actor.com/command", "URL"),
]

# Phone number examples with context
PHONE_EXAMPLES = [
    ("The security incident hotline received call from phone number +1-555-123-4567 reporting potential data breach and unauthorized access to customer accounts.", "+1-555-123-4567", "PHONE_NUMBER"),
    ("The threat actor used phone number +44 20 7946 0958 to contact victims and conduct social engineering attacks targeting financial information.", "+44 20 7946 0958", "PHONE_NUMBER"),
    ("The security team verified contact phone number +49 30 2273 0 with the vendor to confirm legitimate business communication and prevent fraud.", "+49 30 2273 0", "PHONE_NUMBER"),
    ("The incident response coordinator provided emergency phone number 1-800-555-0199 for reporting security incidents and requesting immediate assistance.", "1-800-555-0199", "PHONE_NUMBER"),
    ("The security investigation identified suspicious phone number +33 1 42 86 83 26 used in phishing campaign targeting European customers.", "+33 1 42 86 83 26", "PHONE_NUMBER"),
    ("The compliance officer documented phone number (555) 123-4567 for regulatory reporting and communication with law enforcement agencies.", "(555) 123-4567", "PHONE_NUMBER"),
    ("The threat intelligence report included phone number +81 3 1234 5678 associated with threat actor group conducting cyber espionage operations.", "+81 3 1234 5678", "PHONE_NUMBER"),
    ("The security awareness training mentioned phone number 555.123.4567 as example of social engineering attack vector requiring user vigilance.", "555.123.4567", "PHONE_NUMBER"),
    ("The incident response team contacted phone number +61 2 9374 4000 to coordinate with international security partners during global threat investigation.", "+61 2 9374 4000", "PHONE_NUMBER"),
    ("The security audit report documented phone number +1 (555) 123-4567 for vendor contact information and supply chain security verification.", "+1 (555) 123-4567", "PHONE_NUMBER"),
    ("The threat actor used phone number +86 10 1234 5678 to establish communication channel for ransomware negotiation and payment demands.", "+86 10 1234 5678", "PHONE_NUMBER"),
]

# Threat actor examples
THREAT_ACTOR_EXAMPLES = [
    ("The security investigation attributed the attack to threat actor APT29, also known as Cozy Bear, a Russian state-sponsored hacking group.", "APT29", "THREAT_ACTOR"),
    ("The threat intelligence report identified threat actor APT28, Fancy Bear, conducting cyber espionage operations targeting government and military organizations.", "APT28", "THREAT_ACTOR"),
    ("The security team detected activity from threat actor Lazarus Group, a North Korean state-sponsored hacking organization known for financial theft campaigns.", "Lazarus", "THREAT_ACTOR"),
    ("The incident response investigation linked the attack to threat actor FIN7, a financially motivated cybercriminal group targeting retail and hospitality sectors.", "FIN7", "THREAT_ACTOR"),
    ("The security analysis attributed the supply chain attack to threat actor UNC2452, responsible for the SolarWinds compromise and subsequent data breaches.", "UNC2452", "THREAT_ACTOR"),
    ("The threat intelligence feed reported activity from threat actor Wizard Spider, operators of TrickBot and Conti ransomware campaigns targeting critical infrastructure.", "Wizard Spider", "THREAT_ACTOR"),
    ("The security investigation identified threat actor Ryuk ransomware group conducting targeted attacks against healthcare organizations and demanding high ransom payments.", "Ryuk", "THREAT_ACTOR"),
    ("The threat actor Conti ransomware group was detected deploying their malware variant, encrypting systems and exfiltrating sensitive data before encryption.", "Conti", "THREAT_ACTOR"),
    ("The security team attributed the attack to threat actor Maze ransomware operators, known for double extortion tactics and data publication threats.", "Maze", "THREAT_ACTOR"),
    ("The threat intelligence report identified threat actor APT1, PLA Unit 61398, conducting persistent cyber espionage operations against Western targets.", "APT1", "THREAT_ACTOR"),
]

# IP address examples
IP_EXAMPLES = [
    ("The security monitoring system detected suspicious connection from IP address 192.168.1.100 attempting to access unauthorized network resources.", "192.168.1.100", "IP_ADDRESS"),
    ("The firewall blocked malicious traffic from IP address 10.0.0.50 originating from external threat actor infrastructure and command and control servers.", "10.0.0.50", "IP_ADDRESS"),
    ("The incident response team identified source IP address 172.16.0.25 associated with data exfiltration attempts and unauthorized system access.", "172.16.0.25", "IP_ADDRESS"),
    ("The security investigation traced the attack to IP address 203.0.113.42, a known malicious host used by threat actors for phishing and malware distribution.", "203.0.113.42", "IP_ADDRESS"),
    ("The threat intelligence platform flagged IP address 198.51.100.15 as part of botnet infrastructure conducting distributed denial of service attacks.", "198.51.100.15", "IP_ADDRESS"),
    ("The security scan identified vulnerable system at IP address 192.0.2.10 requiring immediate patch deployment and security hardening procedures.", "192.0.2.10", "IP_ADDRESS"),
    ("The network monitoring detected anomalous traffic from IP address 10.10.10.5 indicating potential lateral movement and privilege escalation attempts.", "10.10.10.5", "IP_ADDRESS"),
    ("The security team blocked connection from IP address 172.20.0.100 attempting to exploit known vulnerabilities in web application infrastructure.", "172.20.0.100", "IP_ADDRESS"),
    ("The incident response investigation identified IP address 192.168.0.1 as command and control server used by malware to receive instructions and exfiltrate data.", "192.168.0.1", "IP_ADDRESS"),
    ("The security monitoring system alerted on IP address 10.1.1.1 conducting port scanning activities and reconnaissance against network infrastructure.", "10.1.1.1", "IP_ADDRESS"),
]

# LLM model examples
LLM_MODEL_EXAMPLES = [
    ("The security team evaluated AI model GPT-4 for potential security vulnerabilities and adversarial attack vectors in natural language processing applications.", "GPT-4", "LLM_MODEL"),
    ("The threat intelligence analysis used Claude 3 Opus to analyze security logs and identify patterns indicating advanced persistent threat activity.", "Claude 3 Opus", "LLM_MODEL"),
    ("The security research team tested LLM model Gemini Pro for detecting phishing emails and identifying social engineering attack patterns in communications.", "Gemini Pro", "LLM_MODEL"),
    ("The incident response investigation utilized AI model LLaMA 2 to analyze malware samples and generate threat intelligence reports for security operations.", "LLaMA 2", "LLM_MODEL"),
    ("The security assessment evaluated LLM model PaLM 2 for potential data leakage risks and privacy concerns in enterprise AI deployment scenarios.", "PaLM 2", "LLM_MODEL"),
    ("The threat hunting team used AI model Mistral 7B to process security event logs and identify anomalous behavior patterns indicating potential breaches.", "Mistral 7B", "LLM_MODEL"),
    ("The security analysis employed LLM model GPT-3.5 Turbo to analyze security policies and identify compliance gaps in organizational security frameworks.", "GPT-3.5 Turbo", "LLM_MODEL"),
    ("The cybersecurity team evaluated AI model BERT for detecting security vulnerabilities in source code and identifying potential exploit vectors.", "BERT", "LLM_MODEL"),
    ("The security investigation used LLM model RoBERTa to analyze threat actor communications and extract indicators of compromise from security logs.", "RoBERTa", "LLM_MODEL"),
    ("The threat intelligence platform integrated AI model T5 to generate security alerts and summarize threat reports for security operations center analysts.", "T5", "LLM_MODEL"),
]

# Email address examples
EMAIL_EXAMPLES = [
    ("The security team identified suspicious email address attacker@malicious-domain.com used in phishing campaign targeting customer accounts and credentials.", "attacker@malicious-domain.com", "EMAIL_ADDRESS"),
    ("The incident response investigation traced the data breach to compromised email address admin@company.com used by threat actors for unauthorized access.", "admin@company.com", "EMAIL_ADDRESS"),
    ("The security monitoring detected email address security-alert@threat-actor.net sending malicious attachments and attempting to deliver malware payloads.", "security-alert@threat-actor.net", "EMAIL_ADDRESS"),
    ("The threat intelligence report identified email address c2-operator@malicious-infrastructure.com associated with command and control infrastructure operations.", "c2-operator@malicious-infrastructure.com", "EMAIL_ADDRESS"),
    ("The security analysis found email address phishing-campaign@fake-bank.com used in social engineering attacks targeting financial institution customers.", "phishing-campaign@fake-bank.com", "EMAIL_ADDRESS"),
    ("The incident response team verified email address security-team@legitimate-company.org for legitimate security communication and threat intelligence sharing.", "security-team@legitimate-company.org", "EMAIL_ADDRESS"),
    ("The security investigation identified email address malware-distribution@threat-actor.com used to distribute ransomware and malicious software to victims.", "malware-distribution@threat-actor.com", "EMAIL_ADDRESS"),
    ("The threat hunting team discovered email address data-exfiltration@malicious-domain.net associated with data theft operations and unauthorized information access.", "data-exfiltration@malicious-domain.net", "EMAIL_ADDRESS"),
    ("The security audit documented email address compliance-officer@organization.com for regulatory reporting and communication with law enforcement agencies.", "compliance-officer@organization.com", "EMAIL_ADDRESS"),
    ("The security monitoring system flagged email address suspicious-activity@threat-infrastructure.com for potential security threat and malicious activity indicators.", "suspicious-activity@threat-infrastructure.com", "EMAIL_ADDRESS"),
]

# LLM provider examples
LLM_PROVIDER_EXAMPLES = [
    ("The security team evaluated AI provider OpenAI for potential security risks and data privacy concerns in enterprise AI deployment and integration scenarios.", "OpenAI", "LLM_PROVIDER"),
    ("The threat intelligence analysis utilized AI provider Anthropic to analyze security logs and generate threat intelligence reports for security operations teams.", "Anthropic", "LLM_PROVIDER"),
    ("The security assessment reviewed AI provider Google DeepMind for compliance with data protection regulations and security best practices in cloud AI services.", "Google DeepMind", "LLM_PROVIDER"),
    ("The incident response investigation considered AI provider Microsoft Azure AI for security incident analysis and automated threat detection capabilities.", "Microsoft Azure AI", "LLM_PROVIDER"),
    ("The security research team evaluated AI provider Meta AI for potential vulnerabilities and adversarial attack vectors in large language model implementations.", "Meta AI", "LLM_PROVIDER"),
    ("The threat hunting platform integrated AI provider Amazon Bedrock for security log analysis and anomaly detection in enterprise network infrastructure.", "Amazon Bedrock", "LLM_PROVIDER"),
    ("The security analysis assessed AI provider Cohere for data privacy and security controls in natural language processing and text analysis applications.", "Cohere", "LLM_PROVIDER"),
    ("The cybersecurity team reviewed AI provider Hugging Face for security best practices and model security in open-source machine learning platform deployment.", "Hugging Face", "LLM_PROVIDER"),
]

# SSN examples
SSN_EXAMPLES = [
    ("The data breach exposed social security number 123-45-6789 belonging to customer, requiring immediate notification and identity theft protection services.", "123-45-6789", "SSN"),
    ("The security investigation identified compromised SSN 987-65-4321 in stolen database, indicating potential identity theft and financial fraud risks.", "987-65-4321", "SSN"),
    ("The incident response team discovered social security number 555-12-3456 in exfiltrated data, triggering regulatory notification and credit monitoring requirements.", "555-12-3456", "SSN"),
    ("The security audit found SSN 111-22-3333 stored in unencrypted database, violating data protection regulations and requiring immediate remediation actions.", "111-22-3333", "SSN"),
    ("The data privacy assessment identified social security number 444-55-6666 in customer records, requiring encryption and access control implementation.", "444-55-6666", "SSN"),
    ("The security breach exposed SSN 777-88-9999 belonging to employee, necessitating identity theft protection and credit monitoring service enrollment.", "777-88-9999", "SSN"),
]

# Time examples
TIME_EXAMPLES = [
    ("The security incident occurred at 14:30 UTC, requiring immediate incident response and containment procedures to prevent further system compromise.", "14:30", "TIME"),
    ("The threat detection system alerted at 09:15 AM when suspicious activity was detected, triggering automated security response and investigation procedures.", "09:15", "TIME"),
    ("The security monitoring detected anomalous behavior at 23:45, indicating potential unauthorized access and requiring immediate security team notification.", "23:45", "TIME"),
    ("The incident response team was notified at 16:20 EST regarding the data breach, initiating containment procedures and threat investigation activities.", "16:20", "TIME"),
    ("The security scan was scheduled for 08:00 PST to identify vulnerabilities and assess system security posture across enterprise infrastructure.", "08:00", "TIME"),
]

# Latitude examples
LATITUDE_EXAMPLES = [
    ("The security investigation identified threat actor location at latitude 40.7128, indicating potential geographic origin of cyber attack and threat infrastructure.", "40.7128", "LATITUDE"),
    ("The incident response team traced data exfiltration to coordinates latitude 34.0522, suggesting geographic location of command and control servers.", "34.0522", "LATITUDE"),
    ("The threat intelligence report included latitude 51.5074 for threat actor infrastructure, enabling geographic threat analysis and law enforcement coordination.", "51.5074", "LATITUDE"),
    ("The security analysis identified suspicious activity originating from latitude 48.8566, indicating potential threat actor location and attack source.", "48.8566", "LATITUDE"),
    ("The cybersecurity investigation documented latitude 35.6762 for compromised server location, facilitating geographic threat intelligence and security response.", "35.6762", "LATITUDE"),
]


def find_entity_position(text: str, entity: str) -> Optional[Tuple[int, int]]:
    """Find the position of entity in text."""
    start = text.find(entity)
    if start == -1:
        return None
    end = start + len(entity)
    return (start, end)


def is_unique(entity_type: str, entity_text: str) -> bool:
    """Check if entity is unique (not already added)."""
    entity_key = f"{entity_type}:{entity_text.lower()}"
    if entity_key in added_entities[entity_type]:
        return False
    added_entities[entity_type].add(entity_key)
    return True


def add_examples_to_file(file_path: Path, examples: List[Tuple[str, str, str]], entity_type: str, count: int):
    """Add examples to a JSONL file."""
    added = 0
    unique_examples = []
    
    for text, entity, label in examples:
        if not is_unique(entity_type, entity):
            continue
        
        pos = find_entity_position(text, entity)
        if pos is None:
            continue
        start, end = pos
        
        unique_examples.append({
            "text": text,
            "entities": [[start, end, label]]
        })
        
        added += 1
        if added >= count:
            break
    
    if unique_examples:
        with open(file_path, 'a', encoding='utf-8') as f:
            for example in unique_examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    return added


def get_relevant_files(entity_type: str, base_dir: Path) -> List[Path]:
    """Get relevant files for entity type."""
    # Map entity types to relevant pillar directories
    mapping = {
        "MALWARE_TYPE": ["threat_intel", "incident_response", "endpoint_security", "detection_correlation"],
        "HASH": ["incident_response", "forensics", "threat_intel", "endpoint_security"],
        "EMOJI": ["socmint", "threat_intel", "incident_response"],
        "DATE": ["incident_response", "audit_compliance", "threat_intel", "detection_correlation"],
        "COMPLIANCE_FRAMEWORK": ["audit_compliance", "governance_risk", "data_privacy"],
        "URL": ["network_security", "threat_intel", "incident_response", "detection_correlation"],
        "PHONE_NUMBER": ["socmint", "threat_intel", "incident_response"],
        "THREAT_ACTOR": ["threat_intel", "incident_response", "detection_correlation"],
        "IP_ADDRESS": ["network_security", "threat_intel", "incident_response", "detection_correlation"],
        "LLM_MODEL": ["ai_security", "threat_intel", "application_security"],
        "EMAIL_ADDRESS": ["threat_intel", "incident_response", "socmint", "detection_correlation"],
        "LLM_PROVIDER": ["ai_security", "threat_intel", "application_security"],
        "SSN": ["data_privacy", "incident_response", "audit_compliance"],
        "TIME": ["incident_response", "detection_correlation", "threat_intel"],
        "LATITUDE": ["geoint", "threat_intel", "incident_response"],
    }
    
    relevant_pillars = mapping.get(entity_type, ["threat_intel", "incident_response"])
    files = []
    
    for pillar in relevant_pillars:
        pillar_dir = base_dir / pillar
        entity_file = pillar_dir / f"{pillar}_entities.jsonl"
        if entity_file.exists():
            files.append(entity_file)
    
    return files if files else [base_dir / "threat_intel" / "threat_intel_entities.jsonl"]


def main():
    base_dir = Path("entities-intent")
    
    print("="*80)
    print("ADD MISSED ENTITY EXAMPLES WITH CONTEXT")
    print("="*80)
    print("\nAdding high-quality examples for top 15 missed entity types:")
    print("  1. MALWARE_TYPE (200 examples)")
    print("  2. HASH (200 examples)")
    print("  3. EMOJI (200 examples)")
    print("  4. DATE (200 examples)")
    print("  5. COMPLIANCE_FRAMEWORK (200 examples)")
    print("  6. URL (150 examples)")
    print("  7. PHONE_NUMBER (150 examples)")
    print("  8. THREAT_ACTOR (150 examples)")
    print("  9. IP_ADDRESS (150 examples)")
    print("  10. LLM_MODEL (150 examples)")
    print("  11. EMAIL_ADDRESS (100 examples)")
    print("  12. LLM_PROVIDER (100 examples)")
    print("  13. SSN (100 examples)")
    print("  14. TIME (100 examples)")
    print("  15. LATITUDE (100 examples)")
    print()
    
    # Define entity types and their examples
    entity_configs = [
        ("MALWARE_TYPE", MALWARE_EXAMPLES, 200),
        ("HASH", HASH_EXAMPLES, 200),
        ("EMOJI", EMOJI_EXAMPLES, 200),
        ("DATE", generate_date_examples(), 200),
        ("COMPLIANCE_FRAMEWORK", COMPLIANCE_EXAMPLES, 200),
        ("URL", URL_EXAMPLES, 150),
        ("PHONE_NUMBER", PHONE_EXAMPLES, 150),
        ("THREAT_ACTOR", THREAT_ACTOR_EXAMPLES, 150),
        ("IP_ADDRESS", IP_EXAMPLES, 150),
        ("LLM_MODEL", LLM_MODEL_EXAMPLES, 150),
        ("EMAIL_ADDRESS", EMAIL_EXAMPLES, 100),
        ("LLM_PROVIDER", LLM_PROVIDER_EXAMPLES, 100),
        ("SSN", SSN_EXAMPLES, 100),
        ("TIME", TIME_EXAMPLES, 100),
        ("LATITUDE", LATITUDE_EXAMPLES, 100),
    ]
    
    total_added = defaultdict(int)
    
    for entity_type, examples, target_count in entity_configs:
        print(f"📝 Adding {entity_type} examples...")
        files = get_relevant_files(entity_type, base_dir)
        
        # Distribute examples across files
        examples_per_file = max(1, target_count // len(files))
        remaining = target_count
        
        for file_path in files:
            if not file_path.exists():
                continue
            
            count = min(examples_per_file, remaining)
            if count <= 0:
                break
            
            added = add_examples_to_file(file_path, examples, entity_type, count)
            total_added[entity_type] += added
            remaining -= added
            
            if remaining <= 0:
                break
        
        print(f"   ✅ Added {total_added[entity_type]} {entity_type} examples")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total examples added:")
    for entity_type, count in sorted(total_added.items()):
        print(f"  {entity_type}: {count}")
    print(f"\nTotal: {sum(total_added.values())} examples")
    print("="*80)


if __name__ == "__main__":
    main()

