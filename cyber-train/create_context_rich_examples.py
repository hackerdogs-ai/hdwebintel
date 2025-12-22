#!/usr/bin/env python3
"""
Create Context-Rich Training Examples for Missed Entities

This script generates longer, narrative-style examples where entities appear
naturally within realistic cybersecurity and OSINT scenarios. The goal is to
help the model learn to identify entities only when they appear in proper context,
not just as isolated patterns.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict, Counter

# Top missed entity types from Iteration 2
TOP_MISSED_TYPES = {
    'EMOJI': 300,
    'PHONE_NUMBER': 300,
    'DATE': 300,
    'MALWARE_TYPE': 300,
    'IP_ADDRESS': 300,
    'SSN': 300,
    'LLM_MODEL': 300,
    'TIME': 300,
    'LONGITUDE': 300,
    'DATACENTER': 300,
    'COMPLIANCE_FRAMEWORK': 300,
    'LATITUDE': 300,
    'GITHUB_REPO_URL': 300,
    'IPV6_ADDRESS': 300,
    'EMAIL_ADDRESS': 300,
}

# Entity type to pillar mapping
ENTITY_PILLAR_MAPPING = {
    'EMOJI': ['osint/socmint', 'osint/cybint', 'threat_intelligence'],
    'PHONE_NUMBER': ['osint/socmint', 'osint/cybint', 'data_privacy_sovereignty', 'threat_intelligence'],
    'DATE': ['incident_response', 'audit_compliance', 'detection_correlation', 'threat_intelligence'],
    'MALWARE_TYPE': ['threat_intelligence', 'incident_response', 'endpoint_security', 'detection_correlation'],
    'IP_ADDRESS': ['network_security', 'threat_intelligence', 'incident_response', 'detection_correlation'],
    'SSN': ['data_privacy_sovereignty', 'incident_response', 'audit_compliance'],
    'LLM_MODEL': ['ai_security', 'threat_intelligence'],
    'TIME': ['incident_response', 'audit_compliance', 'detection_correlation'],
    'LONGITUDE': ['osint/geoint', 'osint/cybint', 'threat_intelligence'],
    'DATACENTER': ['cloud_security', 'threat_intelligence', 'osint/geoint'],
    'COMPLIANCE_FRAMEWORK': ['audit_compliance', 'governance_risk_strategy'],
    'LATITUDE': ['osint/geoint', 'osint/cybint', 'threat_intelligence'],
    'GITHUB_REPO_URL': ['threat_intelligence', 'osint/cybint', 'application_security'],
    'IPV6_ADDRESS': ['network_security', 'threat_intelligence', 'incident_response'],
    'EMAIL_ADDRESS': ['threat_intelligence', 'incident_response', 'osint/socmint', 'detection_correlation'],
}

def create_context_rich_emoji_examples(count: int) -> List[Tuple[str, List]]:
    """Create context-rich emoji examples in realistic scenarios."""
    examples = []
    
    emojis = ['🔐', '🛡️', '⚠️', '🚨', '💻', '🦠', '⚡', '🔍', '📊', '🎯', '✅', '❌', '🔴', '🟡', '🟢', '✓', '✗', '🔒', '🔓', '📱', '💬', '🌐', '🔗']
    
    # Long narrative scenarios where emojis appear naturally
    narrative_templates = [
        """The security operations center received a critical alert 🚨 at 14:30 UTC on 2024-11-30 indicating that multiple systems had been compromised by an advanced persistent threat group. The incident response team immediately initiated their containment procedures, working around the clock to isolate the affected systems and prevent further lateral movement. During the forensic investigation, analysts discovered that the threat actors had used a sophisticated multi-stage attack that began with a phishing email containing a malicious attachment. The email was sent from a compromised account at admin@company.com and targeted key personnel in the finance department. The security team traced the attack back to IP address 192.168.1.100, which was communicating with a command and control server at 203.0.113.45. The threat intelligence team identified the malware as a variant of WannaCry ransomware that had been modified to include additional data exfiltration capabilities. The security analysts worked with law enforcement and managed to contain the breach before any sensitive customer data could be exfiltrated.""",
        
        """During a routine security audit ⚠️ conducted on 2024-12-01, the compliance team discovered several critical vulnerabilities in the organization's cloud infrastructure. The audit revealed that multiple AWS datacenters were not properly configured with encryption at rest, and several S3 buckets containing sensitive customer information were publicly accessible. The security team immediately began remediation efforts, implementing additional access controls and encryption mechanisms to protect the exposed data. The compliance audit also identified gaps in the organization's adherence to GDPR and HIPAA requirements, which required immediate attention. The security team worked with the legal department to ensure that all data processing activities were properly documented and that customer consent mechanisms were in place. The incident was reported to the relevant regulatory authorities as required by data protection regulations.""",
        
        """The threat intelligence team published a comprehensive report 🔍 analyzing the tactics, techniques, and procedures used by the APT29 threat actor group in their recent attack campaign. The report detailed how the threat actors used social engineering techniques to gain initial access to target organizations, followed by the deployment of custom malware variants designed to evade traditional security controls. The security researchers discovered that the threat actors were using GitHub repositories to host their malicious code, including exploit tools and backdoors. The OSINT investigation team analyzed social media posts and discovered that the threat actors were using encrypted messaging platforms like Telegram and WhatsApp to coordinate their activities. The geolocation analysis of the threat actor infrastructure revealed that the command and control servers were located in multiple countries, making it difficult for law enforcement to take action. The security team shared this intelligence with other organizations to help them defend against similar attacks.""",
        
        """The security incident response team successfully contained a ransomware attack 💻 that had encrypted critical systems across the organization's network. The attack began when an employee opened a malicious email attachment that appeared to be from a trusted vendor. The malware quickly spread through the network, encrypting files on multiple servers and workstations. The security team immediately isolated the affected systems and began forensic analysis to determine the scope of the breach. The investigation revealed that the ransomware was a variant of NotPetya that had been modified to include additional persistence mechanisms. The security team worked with cybersecurity experts to develop decryption tools and managed to recover most of the encrypted data. The incident highlighted the importance of regular backups and employee security awareness training.""",
        
        """The OSINT investigation team conducted a comprehensive analysis 📊 of a suspected threat actor's online presence, discovering multiple social media accounts and forum posts that revealed their operational security practices. The investigation began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The OSINT analysts used various techniques including reverse image search, geolocation analysis, and social network analysis to build a comprehensive profile of the threat actor. The investigation revealed that the threat actor was using encrypted messaging apps to communicate with other members of their group, and that they were sharing tools and techniques on dark web forums. The geolocation analysis of images posted by the threat actor revealed GPS coordinates embedded in the EXIF metadata, which helped law enforcement identify their physical location. The security team shared this intelligence with law enforcement agencies, leading to the arrest of several individuals involved in the attack campaign.""",
    ]
    
    for i in range(count):
        emoji = random.choice(emojis)
        template = random.choice(narrative_templates)
        
        # Insert emoji at a natural position in the narrative
        # Try to place it where it makes contextual sense
        sentences = template.split('. ')
        if len(sentences) > 2:
            # Insert emoji in the first or second sentence
            insert_pos = random.choice([0, 1])
            sentences[insert_pos] = f"{emoji} {sentences[insert_pos]}"
            context = '. '.join(sentences)
        else:
            context = f"{emoji} {template}"
        
        emoji_pos = context.find(emoji)
        if emoji_pos != -1:
            examples.append((context, [[emoji_pos, emoji_pos + len(emoji), "EMOJI"]]))
    
    return examples

def create_context_rich_phone_examples(count: int) -> List[Tuple[str, List]]:
    """Create context-rich phone number examples in realistic scenarios."""
    examples = []
    
    phone_formats = [
        "+1-555-123-4567", "+1-555-234-5678", "+1-555-345-6789",
        "(555) 123-4567", "(555) 234-5678", "(555) 345-6789",
        "555-123-4567", "555-234-5678", "555-345-6789",
        "+44 20 7946 0958", "+44 20 1234 5678",
        "+33-1-42-86-83-26", "+33-1-23-45-67-89",
        "+1.555.123.4567", "+1.555.234.5678",
    ]
    
    narrative_templates = [
        """The security incident response team received a call from an employee reporting suspicious activity on their workstation. The employee, who works in the finance department, noticed that their computer was running slowly and that several files had been modified without their knowledge. The security team immediately began investigating the incident, discovering that the employee's system had been compromised by malware that was attempting to exfiltrate sensitive financial data. During the investigation, the security analysts discovered that the malware was communicating with an external command and control server and that the employee's credentials had been stolen through a phishing attack. The security team worked with the employee to reset their passwords and implemented additional security controls to prevent further unauthorized access. The employee provided their contact information including phone number {phone} so that the security team could reach them if additional information was needed.""",
        
        """The OSINT investigation team discovered that a known threat actor was using phone number {phone} to register multiple fake social media accounts that were being used to conduct social engineering attacks. The investigation began when the security team received intelligence about a potential attack targeting the organization's employees. The OSINT analysts used various techniques to track the threat actor's online activities, discovering that they were using multiple phone numbers to verify accounts on various social media platforms. The investigation revealed that the threat actor was using these fake accounts to befriend employees and gather information about the organization's security practices. The security team discovered that the threat actor was also using encrypted messaging apps to communicate with other members of their group, and that they were sharing tools and techniques on dark web forums. The geolocation analysis of the phone numbers revealed that they were registered in multiple countries, making it difficult for law enforcement to take action.""",
        
        """During a data privacy investigation, the security team discovered that phone number {phone} was included in a data breach that exposed personally identifiable information of over 10,000 customers. The investigation began when the organization received reports from customers that their personal information had been compromised. The security team immediately began investigating the breach, discovering that an unauthorized third party had gained access to the customer database through a compromised API endpoint. The forensic investigation revealed that the threat actors had used a SQL injection vulnerability to gain access to the database, and that they had exfiltrated customer data including names, email addresses, phone numbers, and in some cases, Social Security numbers. The security team worked with law enforcement to investigate the breach and implemented additional security controls to prevent future incidents. The organization immediately notified affected customers and regulatory authorities as required by data protection regulations.""",
        
        """The threat intelligence team identified phone number {phone} as being associated with a known threat actor group that was conducting coordinated attacks against multiple organizations. The investigation began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The threat intelligence analysts discovered that the threat actor was using this phone number to register accounts on various platforms and to communicate with other members of their group. The investigation revealed that the threat actor was using encrypted messaging apps to coordinate their activities, and that they were sharing tools and techniques on dark web forums. The security team discovered that the threat actor was also using multiple phone numbers to avoid detection, and that they were rotating through different numbers to maintain operational security. The geolocation analysis of the phone numbers revealed that they were registered in multiple countries, making it difficult for law enforcement to take action.""",
        
        """The compliance audit team discovered that phone number {phone} was stored in an unencrypted format in the customer relationship management system, which violated the organization's data protection policies. The audit was conducted as part of the organization's regular compliance review process, and it revealed several areas where the organization needed to improve its data protection practices. The security team discovered that the CRM system was not properly configured to encrypt sensitive customer information, and that phone numbers, email addresses, and other personally identifiable information were being stored in plain text. The compliance team immediately implemented encryption for all sensitive data fields and updated the data processing procedures to ensure full compliance with data protection regulations. The security team also discovered that the system was logging sensitive customer information without proper encryption or access controls, which required immediate remediation.""",
    ]
    
    for i in range(count):
        phone = random.choice(phone_formats)
        template = random.choice(narrative_templates)
        context = template.format(phone=phone)
        
        phone_pos = context.find(phone)
        if phone_pos != -1:
            examples.append((context, [[phone_pos, phone_pos + len(phone), "PHONE_NUMBER"]]))
    
    return examples

def create_context_rich_date_examples(count: int) -> List[Tuple[str, List]]:
    """Create context-rich date examples in realistic scenarios."""
    examples = []
    
    dates = [
        "2024-11-30", "2024-12-01", "2024-12-02", "2024-11-15", "2024-11-20",
        "2024-10-30", "2024-10-15", "2024-09-30", "2024-08-15", "2024-07-30",
        "November 30, 2024", "December 1, 2024", "November 15, 2024",
        "11/30/2024", "12/01/2024", "11/15/2024",
        "30-Nov-2024", "01-Dec-2024", "15-Nov-2024",
    ]
    
    narrative_templates = [
        """The security incident response team was alerted to a critical security breach on {date} when the intrusion detection system detected unauthorized access attempts from multiple IP addresses. The incident response team immediately began investigating the breach, discovering that the threat actors had gained access to the corporate network through a compromised user account. The security analysts worked around the clock to contain the breach and prevent further unauthorized access to sensitive systems. During the forensic investigation, the team discovered that the threat actors had been present in the environment for several weeks before being detected, and that they had exfiltrated sensitive customer data including names, email addresses, and phone numbers. The security team worked with law enforcement to investigate the breach and implemented additional security controls to prevent future incidents. The organization immediately notified affected customers and regulatory authorities as required by data protection regulations.""",
        
        """The compliance audit team conducted a comprehensive security assessment on {date} to evaluate the organization's adherence to GDPR and HIPAA requirements. The audit included reviewing security policies, access controls, encryption procedures, and incident response capabilities. The security team discovered several areas where the organization needed to implement additional controls to achieve full compliance with the framework requirements. The compliance team developed a remediation plan to address the identified gaps and ensure ongoing compliance. The audit revealed that the organization had implemented most of the required security controls but identified several areas for improvement including data encryption, access controls, and incident response procedures. The security team worked with the compliance team to implement the necessary changes and ensure that the organization met all regulatory requirements.""",
        
        """The threat intelligence team published a comprehensive report on {date} analyzing the tactics, techniques, and procedures used by the APT29 threat actor group in their recent attack campaign. The report detailed how the threat actors used social engineering techniques to gain initial access to target organizations, followed by the deployment of custom malware variants designed to evade traditional security controls. The security researchers discovered that the threat actors were using GitHub repositories to host their malicious code, including exploit tools and backdoors. The OSINT investigation team analyzed social media posts and discovered that the threat actors were using encrypted messaging platforms to coordinate their activities. The geolocation analysis of the threat actor infrastructure revealed that the command and control servers were located in multiple countries, making it difficult for law enforcement to take action. The security team shared this intelligence with other organizations to help them defend against similar attacks.""",
        
        """The security operations center received a critical alert on {date} indicating that multiple systems had been compromised by an advanced persistent threat group. The incident response team immediately initiated their containment procedures, working around the clock to isolate the affected systems and prevent further lateral movement. During the forensic investigation, analysts discovered that the threat actors had used a sophisticated multi-stage attack that began with a phishing email containing a malicious attachment. The email was sent from a compromised account and targeted key personnel in the finance department. The security team traced the attack back to IP address 192.168.1.100, which was communicating with a command and control server. The threat intelligence team identified the malware as a variant of WannaCry ransomware that had been modified to include additional data exfiltration capabilities. The security analysts worked with law enforcement and managed to contain the breach before any sensitive customer data could be exfiltrated.""",
        
        """The data privacy investigation team discovered on {date} that a data breach had exposed personally identifiable information of over 10,000 customers. The investigation began when the organization received reports from customers that their personal information had been compromised. The security team immediately began investigating the breach, discovering that an unauthorized third party had gained access to the customer database through a compromised API endpoint. The forensic investigation revealed that the threat actors had used a SQL injection vulnerability to gain access to the database, and that they had exfiltrated customer data including names, email addresses, phone numbers, and in some cases, Social Security numbers. The security team worked with law enforcement to investigate the breach and implemented additional security controls to prevent future incidents. The organization immediately notified affected customers and regulatory authorities as required by data protection regulations.""",
    ]
    
    for i in range(count):
        date = random.choice(dates)
        template = random.choice(narrative_templates)
        context = template.format(date=date)
        
        date_pos = context.find(date)
        if date_pos != -1:
            examples.append((context, [[date_pos, date_pos + len(date), "DATE"]]))
    
    return examples

def create_context_rich_malware_examples(count: int) -> List[Tuple[str, List]]:
    """Create context-rich malware type examples in realistic scenarios."""
    examples = []
    
    malware_names = [
        'WannaCry', 'wannacry', 'NotPetya', 'notpetya', 'Ryuk', 'ryuk',
        'TrickBot', 'trickbot', 'Emotet', 'emotet', 'Zeus', 'zeus',
        'Stuxnet', 'stuxnet', 'Code Red', 'code red', 'Conficker', 'conficker',
        'Mirai', 'mirai', 'Remote Access Trojan', 'RAT', 'keylogger', 'rootkit',
    ]
    
    narrative_templates = [
        """The endpoint detection and response system detected {malware} malware on an employee workstation during a routine security scan. The security team immediately isolated the infected system from the network to prevent the malware from spreading to other devices. The forensic analysis revealed that the malware was delivered through a malicious email attachment that was opened by an unsuspecting employee. The security analysts identified the malware variant and began remediation procedures to remove the threat from the network. During the investigation, the security team discovered that the malware was attempting to establish connections to external command and control servers and that it was capable of exfiltrating sensitive data. The security team worked with cybersecurity experts to analyze the malware sample and develop countermeasures to prevent similar attacks in the future. The incident highlighted the importance of employee security awareness training and the need for robust endpoint protection solutions.""",
        
        """The threat intelligence team discovered that the threat actor deployed a {malware} variant as part of their attack campaign targeting multiple organizations in the financial sector. The security team analyzed the malware sample and discovered that it was specifically designed to evade traditional antivirus detection by using advanced obfuscation techniques. The malware was capable of establishing persistent backdoor access to compromised systems, allowing the threat actors to maintain long-term access to the organization's network. The security researchers discovered that the malware was part of a larger malware-as-a-service operation that was being used by multiple threat actor groups. The analysis revealed sophisticated evasion techniques including code obfuscation, anti-debugging measures, and encrypted command and control communications. The security team shared the findings with the threat intelligence community to help other organizations defend against similar attacks.""",
        
        """During the incident response investigation, the security team found evidence of {malware} infection on multiple systems across the network. The malware had been present in the environment for several weeks before being detected, allowing the threat actors to exfiltrate sensitive data. The security analysts worked around the clock to contain the infection and prevent further data loss. The incident response team documented all findings for the post-incident review and worked with law enforcement to investigate the attack. The security team discovered that the malware was capable of establishing persistent backdoor access and that it was communicating with external command and control servers. The forensic investigation revealed that the threat actors had used the malware to steal credentials, exfiltrate sensitive data, and maintain long-term access to the organization's network. The security team implemented additional security controls to prevent similar attacks in the future.""",
        
        """The malware analysis team identified the {malware} family through static and dynamic analysis of the malicious code. The security researchers discovered that the malware was part of a larger malware-as-a-service operation that was being used by multiple threat actor groups. The analysis revealed sophisticated evasion techniques including code obfuscation, anti-debugging measures, and encrypted command and control communications. The security team discovered that the malware was capable of establishing persistent backdoor access to compromised systems and that it was designed to evade traditional security controls. The malware analysis revealed that the threat actors had used advanced techniques to avoid detection, including the use of legitimate system tools and the encryption of malicious communications. The security team shared the findings with the threat intelligence community to help other organizations defend against similar attacks.""",
        
        """Ransomware detected: {malware} variants identified in network scan. The security operations center received an alert indicating that the malware was detected in the network traffic. The network security monitoring system identified suspicious communication patterns that were consistent with known malware behavior. The security analysts immediately began investigating the source of the infection and discovered that the malware was attempting to establish connections to external command and control servers. The security team worked with cybersecurity experts to analyze the malware sample and develop countermeasures to prevent the malware from spreading to other systems. The incident response team implemented containment procedures to isolate the infected systems and prevent further damage. The security team discovered that the malware was capable of encrypting files and that it was demanding a ransom payment in exchange for the decryption key.""",
    ]
    
    for i in range(count):
        malware = random.choice(malware_names)
        template = random.choice(narrative_templates)
        context = template.format(malware=malware)
        
        malware_pos = context.find(malware)
        if malware_pos != -1:
            examples.append((context, [[malware_pos, malware_pos + len(malware), "MALWARE_TYPE"]]))
        else:
            # Try case-insensitive
            malware_lower = malware.lower()
            context_lower = context.lower()
            malware_pos_lower = context_lower.find(malware_lower)
            if malware_pos_lower != -1:
                examples.append((context, [[malware_pos_lower, malware_pos_lower + len(malware), "MALWARE_TYPE"]]))
    
    return examples

def create_context_rich_time_examples(count: int) -> List[Tuple[str, List]]:
    """Create context-rich time examples in realistic scenarios."""
    examples = []
    
    times = [
        "14:30", "14:30:00", "2:30 PM", "2:30:00 PM", "14:30 UTC",
        "09:00", "09:00:00", "9:00 AM", "9:00:00 AM",
        "18:00", "18:00:00", "6:00 PM", "6:00:00 PM",
        "23:45", "23:45:00", "11:45 PM", "11:45:00 PM",
    ]
    
    narrative_templates = [
        """The security incident occurred at {time} on 2024-11-30 when the intrusion detection system detected unauthorized access attempts from multiple IP addresses. The security operations center immediately began investigating the incident and discovered that the threat actors had gained access to the corporate network through a compromised user account. The incident response team worked throughout the night to contain the breach and prevent further unauthorized access to sensitive systems. During the forensic investigation, the security analysts discovered that the threat actors had been present in the environment for several weeks before being detected, and that they had exfiltrated sensitive customer data. The security team worked with law enforcement to investigate the breach and implemented additional security controls to prevent future incidents. The organization immediately notified affected customers and regulatory authorities as required by data protection regulations.""",
        
        """The security event monitoring system detected an anomalous event with timestamp {time} that triggered multiple security alerts. The security analysts reviewed the event logs and discovered that the event was associated with a known attack pattern used by advanced persistent threat groups. The security team immediately escalated the incident to the threat intelligence team for further analysis and began implementing additional security controls to prevent similar attacks. The investigation revealed that the threat actors had used sophisticated techniques to evade detection, including the use of legitimate system tools and the encryption of malicious communications. The security team discovered that the event was part of a larger attack campaign that had been targeting multiple organizations in the financial sector. The incident response team worked with cybersecurity experts to analyze the attack and develop countermeasures to prevent similar incidents in the future.""",
        
        """The network security monitoring system triggered an alert at {time} for suspicious activity originating from IP address 192.168.1.100. The security analysts reviewed the network traffic logs and discovered that the system was attempting to establish connections to external command and control servers. The security team immediately blocked the malicious IP address and began investigating the source of the compromise to determine how the system was initially infected. The forensic investigation revealed that the system had been compromised through a phishing email that contained a malicious attachment. The security team discovered that the malware was capable of establishing persistent backdoor access and that it was communicating with external servers to exfiltrate sensitive data. The incident response team worked with cybersecurity experts to remove the malware and restore the system to a secure state.""",
        
        """The security log analysis revealed a log entry at {time} that showed suspicious activity patterns consistent with data exfiltration attempts. The security analysts discovered that the threat actors were attempting to transfer large amounts of data from the internal network to external servers. The security team immediately implemented network segmentation to prevent further data loss and began forensic analysis to determine the scope of the data breach. The investigation revealed that the threat actors had gained access to the network through a compromised user account and that they had been present in the environment for several weeks before being detected. The security team worked with law enforcement to investigate the breach and implemented additional security controls to prevent future incidents. The organization immediately notified affected customers and regulatory authorities as required by data protection regulations.""",
        
        """The security investigation determined that the attack started at {time} and lasted approximately 2 hours before being detected by the security monitoring systems. During this time, the threat actors were able to access multiple systems and exfiltrate sensitive customer data. The security team worked with law enforcement to investigate the attack and implemented additional security measures to prevent future incidents. The forensic investigation revealed that the threat actors had used sophisticated techniques to evade detection, including the use of legitimate system tools and the encryption of malicious communications. The security team discovered that the attack was part of a larger campaign that had been targeting multiple organizations in the financial sector. The incident response team worked with cybersecurity experts to analyze the attack and develop countermeasures to prevent similar incidents in the future.""",
    ]
    
    for i in range(count):
        time_str = random.choice(times)
        template = random.choice(narrative_templates)
        context = template.format(time=time_str)
        
        time_pos = context.find(time_str)
        if time_pos != -1:
            examples.append((context, [[time_pos, time_pos + len(time_str), "TIME"]]))
    
    return examples

def create_context_rich_coordinate_examples(count: int, coord_type: str) -> List[Tuple[str, List]]:
    """Create context-rich coordinate examples in realistic scenarios."""
    examples = []
    
    if coord_type == 'LATITUDE':
        coords = ['40.7128', '52.5200', '37.7749', '35.6762', '51.5074', '27.9881']
        coord_name = 'latitude'
    else:
        coords = ['-74.0060', '13.4050', '-122.4194', '139.6503', '-0.1278', '86.9250']
        coord_name = 'longitude'
    
    narrative_templates = [
        """The geolocation analysis of the threat actor's network infrastructure revealed coordinates with {coord_name} {coord} that pointed to a location in a major metropolitan area. The OSINT investigation team cross-referenced these coordinates with known threat actor locations and discovered that this location was associated with previous cyber attacks. The security team shared this intelligence with law enforcement agencies for further investigation. The geolocation analysis was part of a comprehensive threat intelligence investigation that began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The investigation revealed that the threat actors were using compromised cloud infrastructure to host their malicious servers, and that the servers were located in multiple countries to avoid detection. The security team worked with law enforcement to identify the physical location of the threat actors and to take down the malicious infrastructure.""",
        
        """The GPS location metadata analysis identified {coord_name} {coord} embedded in image files that were shared on social media platforms by the threat actors. The security analysts discovered that the threat actors were inadvertently revealing their location through geotagged images. The OSINT team used this information to track the threat actors' movements and identify potential safe houses or operational bases. The investigation began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The OSINT analysts used various techniques including reverse image search, geolocation analysis, and social network analysis to build a comprehensive profile of the threat actor. The investigation revealed that the threat actor was using encrypted messaging apps to communicate with other members of their group, and that they were sharing tools and techniques on dark web forums. The geolocation analysis of images posted by the threat actor revealed GPS coordinates embedded in the EXIF metadata, which helped law enforcement identify their physical location.""",
        
        """The open source intelligence analysis found coordinates with {coord_name} {coord} in leaked documents that were published on dark web forums. The security researchers discovered that these coordinates were associated with a known threat actor group's operational infrastructure. The threat intelligence team added this information to their database and began monitoring for additional indicators of compromise associated with this location. The investigation was part of a comprehensive threat intelligence operation that began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The OSINT analysts used various techniques to track the threat actor's online activities, discovering that they were using multiple platforms to share information and coordinate their activities. The geolocation analysis of the leaked documents revealed GPS coordinates that pointed to physical locations associated with the threat actor group's operations.""",
        
        """The IP geolocation analysis determined that the threat actor's command and control servers were located at coordinates with {coord_name} {coord} in a country known for hosting malicious infrastructure. The security team discovered that the threat actors were using compromised cloud infrastructure to host their malicious servers. The security analysts worked with the cloud provider to take down the malicious infrastructure and prevent further attacks. The investigation began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The threat intelligence analysts discovered that the threat actor was using multiple command and control servers located in different countries to avoid detection. The geolocation analysis of the IP addresses revealed that the servers were hosted in countries known for hosting malicious infrastructure, making it difficult for law enforcement to take action.""",
        
        """The digital forensics investigation of image files discovered that the EXIF metadata contained {coord_name} {coord} that revealed the location where the images were taken. The security team discovered that the threat actors were taking photos of sensitive facilities and inadvertently including GPS coordinates in the image metadata. The OSINT analysts used this information to identify the specific locations that were being targeted by the threat actors. The investigation was part of a comprehensive threat intelligence operation that began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The OSINT analysts used various techniques including reverse image search, geolocation analysis, and social network analysis to build a comprehensive profile of the threat actor. The geolocation analysis of images posted by the threat actor revealed GPS coordinates embedded in the EXIF metadata, which helped law enforcement identify their physical location and the locations of facilities they were targeting.""",
    ]
    
    for i in range(count):
        coord = random.choice(coords)
        template = random.choice(narrative_templates)
        context = template.format(coord=coord, coord_name=coord_name)
        
        coord_pos = context.find(coord)
        if coord_pos != -1:
            examples.append((context, [[coord_pos, coord_pos + len(coord), coord_type]]))
    
    return examples

def add_examples_to_file(file_path: Path, examples: List[Tuple[str, List]], entity_type: str):
    """Add examples to JSONL file."""
    if not file_path.exists():
        print(f"⚠️  File not found: {file_path}")
        return 0
    
    added = 0
    existing_texts = set()
    
    # Read existing examples
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    existing_texts.add(data['text'].strip().lower())
                except:
                    pass
    
    # Append new examples
    with open(file_path, 'a', encoding='utf-8') as f:
        for text, entities in examples:
            if text.strip().lower() in existing_texts:
                continue
            
            # Validate entities
            valid_entities = []
            for start, end, label in entities:
                if 0 <= start < end <= len(text):
                    entity_text = text[start:end]
                    if entity_text.strip():
                        valid_entities.append([start, end, label])
            
            if valid_entities:
                data = {
                    "text": text,
                    "entities": valid_entities
                }
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
                existing_texts.add(text.strip().lower())
                added += 1
    
    if added > 0:
        print(f"  ✅ Added {added} {entity_type} examples to {file_path.name}")
    
    return added

def main():
    base_dir = Path("entities-intent")
    
    print("=" * 80)
    print("CREATING CONTEXT-RICH TRAINING EXAMPLES")
    print("=" * 80)
    print()
    
    total_added = 0
    
    # Additional generator functions
    def create_context_rich_ip_examples(count: int) -> List[Tuple[str, List]]:
        """Create context-rich IP address examples."""
        examples = []
        ips = ["192.168.1.100", "10.0.0.1", "172.16.0.1", "203.0.113.1", "198.51.100.1"]
        templates = [
            """The network security monitoring system detected suspicious activity from IP address {ip} in the network logs that was attempting to access multiple internal systems. The security analysts reviewed the network flow data and discovered that the IP address was associated with a known threat actor infrastructure. The security team immediately blocked all traffic from this IP address and began investigating the scope of the potential compromise to determine if any systems were successfully breached. During the forensic investigation, the security team discovered that the threat actors had used this IP address to establish connections to external command and control servers and that they had been exfiltrating sensitive data. The security team worked with law enforcement to investigate the breach and implemented additional security controls to prevent future incidents.""",
            """The threat intelligence investigation revealed that IP address {ip} was being used as a command and control server by an advanced persistent threat group. The security team discovered that the threat actors were using this IP address to communicate with compromised systems and exfiltrate sensitive data. The security operations center updated their threat intelligence feeds to include this IP address and implemented network controls to block all communication with this malicious infrastructure. The investigation began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The threat intelligence analysts discovered that the threat actor was using multiple IP addresses to avoid detection, and that they were rotating through different addresses to maintain operational security.""",
        ]
        for i in range(count):
            ip = random.choice(ips)
            template = random.choice(templates)
            context = template.format(ip=ip)
            ip_pos = context.find(ip)
            if ip_pos != -1:
                examples.append((context, [[ip_pos, ip_pos + len(ip), "IP_ADDRESS"]]))
        return examples
    
    def create_context_rich_ssn_examples(count: int) -> List[Tuple[str, List]]:
        """Create context-rich SSN examples."""
        examples = []
        ssns = ["123-45-6789", "234-56-7890", "345-67-8901", "123 45 6789", "123456789"]
        templates = [
            """The data privacy investigation revealed that the PII data leak included SSN {ssn} along with other sensitive personal information such as names, addresses, and phone numbers. The security team discovered that the data breach occurred when an unauthorized third party gained access to the customer database through a compromised API endpoint. The organization immediately notified affected customers and regulatory authorities as required by data protection regulations. The forensic investigation revealed that the threat actors had used a SQL injection vulnerability to gain access to the database, and that they had exfiltrated customer data including names, email addresses, phone numbers, and in some cases, Social Security numbers. The security team worked with law enforcement to investigate the breach and implemented additional security controls to prevent future incidents.""",
            """The compliance audit team found a privacy violation where SSN {ssn} was discovered in unencrypted log files that were accessible to unauthorized personnel. The security team discovered that the application was logging sensitive customer information without proper encryption or access controls. The compliance team immediately implemented data masking procedures and updated the logging policies to prevent sensitive information from being stored in plain text. The audit was conducted as part of the organization's regular compliance review process, and it revealed several areas where the organization needed to improve its data protection practices. The security team discovered that the system was logging sensitive customer information without proper encryption, and that this information was accessible to unauthorized personnel through standard log file access.""",
        ]
        for i in range(count):
            ssn = random.choice(ssns)
            template = random.choice(templates)
            context = template.format(ssn=ssn)
            ssn_pos = context.find(ssn)
            if ssn_pos != -1:
                examples.append((context, [[ssn_pos, ssn_pos + len(ssn), "SSN"]]))
        return examples
    
    def create_context_rich_llm_model_examples(count: int) -> List[Tuple[str, List]]:
        """Create context-rich LLM model examples."""
        examples = []
        models = ['GPT-4', 'GPT-3.5', 'Claude-3', 'Claude-3-Opus', 'Claude-3-Sonnet', 'Llama-2', 'Gemini-Pro', 'GPT-4-turbo']
        templates = [
            """The AI security team conducted a comprehensive security analysis using the {model} model to identify potential vulnerabilities in the organization's AI infrastructure. The security assessment revealed several security concerns including prompt injection vulnerabilities and data leakage risks. The security team developed a comprehensive security framework to address these issues and ensure the safe deployment of AI models in production environments. The investigation began when the security team received reports of suspicious activity in the organization's AI systems. The security analysts discovered that the AI models were being used to process sensitive customer data, and that there were potential security vulnerabilities that could be exploited by threat actors. The security team worked with the AI development team to implement security controls and mitigate the identified vulnerabilities.""",
            """The threat detection system was powered by the {model} model to analyze large volumes of security logs and identify potential threats. The AI-powered threat detection system was able to identify sophisticated attack patterns that traditional signature-based detection systems would have missed. The security operations center integrated the AI model into their security monitoring workflow to improve threat detection capabilities. The system was designed to analyze network traffic, log files, and other security data to identify potential threats and anomalies. The AI model was trained on a large dataset of known attack patterns and was able to identify new and emerging threats that had not been seen before. The security team discovered that the AI model was particularly effective at identifying advanced persistent threat activities and zero-day attacks.""",
        ]
        for i in range(count):
            model = random.choice(models)
            template = random.choice(templates)
            context = template.format(model=model)
            model_pos = context.find(model)
            if model_pos != -1:
                examples.append((context, [[model_pos, model_pos + len(model), "LLM_MODEL"]]))
        return examples
    
    def create_context_rich_datacenter_examples(count: int) -> List[Tuple[str, List]]:
        """Create context-rich datacenter examples."""
        examples = []
        datacenters = ['AWS-US-EAST-1', 'AWS-US-WEST-2', 'AZURE-EAST-US', 'GCP-US-CENTRAL1', 'AWS-EU-WEST-1']
        templates = [
            """The cloud security team discovered that multiple datacenters including {datacenter} were not properly configured with encryption at rest, and several S3 buckets containing sensitive customer information were publicly accessible. The security team immediately began remediation efforts, implementing additional access controls and encryption mechanisms to protect the exposed data. The investigation began when the security team received alerts about potential security misconfigurations in the cloud infrastructure. The security analysts discovered that the datacenters were hosting critical applications and that they contained sensitive customer data that needed to be protected. The security team worked with the cloud provider to implement additional security controls and ensure that all data was properly encrypted and protected.""",
            """The threat intelligence investigation identified that the threat actor's command and control infrastructure was hosted in datacenter {datacenter} using compromised cloud accounts. The security team discovered that the threat actors were using compromised cloud infrastructure to host their malicious servers, and that the servers were located in multiple datacenters to avoid detection. The security analysts worked with the cloud provider to take down the malicious infrastructure and prevent further attacks. The investigation began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The threat intelligence analysts discovered that the threat actor was using multiple cloud providers and datacenters to host their malicious infrastructure, making it difficult for law enforcement to take action.""",
        ]
        for i in range(count):
            dc = random.choice(datacenters)
            template = random.choice(templates)
            context = template.format(datacenter=dc)
            dc_pos = context.find(dc)
            if dc_pos != -1:
                examples.append((context, [[dc_pos, dc_pos + len(dc), "DATACENTER"]]))
        return examples
    
    def create_context_rich_compliance_examples(count: int) -> List[Tuple[str, List]]:
        """Create context-rich compliance framework examples."""
        examples = []
        frameworks = ['GDPR', 'HIPAA', 'PCI DSS', 'NIST CSF', 'ISO 27001', 'SOC 2 Type II', 'FedRAMP', 'CMMC Level 3']
        templates = [
            """The compliance team conducted a comprehensive audit to ensure that all security controls meet the {framework} requirements for data protection and security. The audit included reviewing security policies, access controls, encryption procedures, and incident response capabilities. The security team discovered several areas where the organization needed to implement additional controls to achieve full compliance with the framework requirements. The compliance team developed a remediation plan to address the identified gaps and ensure ongoing compliance. The audit was conducted as part of the organization's regular compliance review process, and it revealed several areas where the organization needed to improve its security practices. The security team worked with the compliance team to implement the necessary changes and ensure that the organization met all regulatory requirements.""",
            """The security architecture team designed the security controls to be aligned with the {framework} security standards to ensure that the organization meets all regulatory requirements. The security team implemented comprehensive access controls, encryption mechanisms, and monitoring capabilities that are consistent with the framework's security recommendations. The compliance team regularly reviews the security controls to ensure they continue to meet the framework requirements as the threat landscape evolves. The security team discovered that the framework provided comprehensive guidance on how to implement security controls, and that following the framework's recommendations would help the organization achieve better security posture. The compliance team worked with the security team to ensure that all security controls were properly documented and that they met the framework's requirements.""",
        ]
        for i in range(count):
            framework = random.choice(frameworks)
            template = random.choice(templates)
            context = template.format(framework=framework)
            framework_pos = context.find(framework)
            if framework_pos != -1:
                examples.append((context, [[framework_pos, framework_pos + len(framework), "COMPLIANCE_FRAMEWORK"]]))
        return examples
    
    def create_context_rich_github_examples(count: int) -> List[Tuple[str, List]]:
        """Create context-rich GitHub repo URL examples."""
        examples = []
        repos = ['https://github.com/user/repo', 'github.com/user/repo', 'https://github.com/org/malware', 'github.com/threat-actor/tools']
        templates = [
            """The threat intelligence team discovered that threat actors were using GitHub repository {repo} to host malicious code and share attack tools with other members of their group. The security analysts reviewed the repository contents and discovered that it contained multiple malware samples, exploit code, and detailed instructions for conducting cyber attacks. The security team reported the repository to GitHub's security team and worked with them to have the malicious content removed. The investigation began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The OSINT analysts used various techniques to track the threat actor's online activities, discovering that they were using GitHub to host their malicious code and share tools with other members of their group.""",
            """The OSINT investigation team discovered GitHub repository {repo} during their analysis of threat actor infrastructure. The security researchers found that the repository contained source code for custom malware variants and tools used in previous attack campaigns. The security team analyzed the code to understand the threat actors' capabilities and developed countermeasures to detect and prevent attacks using these tools. The investigation was part of a comprehensive threat intelligence operation that began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The OSINT analysts discovered that the threat actor was using GitHub to host their malicious code and share tools with other members of their group.""",
        ]
        for i in range(count):
            repo = random.choice(repos)
            template = random.choice(templates)
            context = template.format(repo=repo)
            repo_pos = context.find(repo)
            if repo_pos != -1:
                examples.append((context, [[repo_pos, repo_pos + len(repo), "GITHUB_REPO_URL"]]))
        return examples
    
    def create_context_rich_ipv6_examples(count: int) -> List[Tuple[str, List]]:
        """Create context-rich IPv6 examples."""
        examples = []
        ipv6s = ['2001:db8::1', '2001:db8:85a3::8a2e:370:7334', 'fe80::1%eth0', '::1']
        templates = [
            """The network security monitoring system detected IPv6 address {ipv6} in network traffic that was attempting to establish connections to internal systems. The security analysts reviewed the network flow data and discovered that the IPv6 address was associated with a known threat actor infrastructure. The security team immediately blocked all traffic from this IPv6 address and began investigating the scope of the potential compromise. The investigation began when the security team received alerts about suspicious network activity. The security analysts discovered that the threat actors were using IPv6 addresses to evade detection, since many security tools are not properly configured to monitor IPv6 traffic. The security team updated their monitoring rules to include IPv6 addresses in threat intelligence feeds.""",
            """The threat intelligence feeds indicated that IPv6 address {ipv6} was being used as a command and control server by an advanced persistent threat group. The security team discovered that the threat actors were using IPv6 addresses to evade detection since many security tools are not properly configured to monitor IPv6 traffic. The security operations center updated their monitoring rules to include IPv6 addresses in threat intelligence feeds. The investigation began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The threat intelligence analysts discovered that the threat actor was using multiple IPv6 addresses to avoid detection, and that they were rotating through different addresses to maintain operational security.""",
        ]
        for i in range(count):
            ipv6 = random.choice(ipv6s)
            template = random.choice(templates)
            context = template.format(ipv6=ipv6)
            ipv6_pos = context.find(ipv6)
            if ipv6_pos != -1:
                examples.append((context, [[ipv6_pos, ipv6_pos + len(ipv6), "IPV6_ADDRESS"]]))
        return examples
    
    def create_context_rich_email_examples(count: int) -> List[Tuple[str, List]]:
        """Create context-rich email address examples."""
        examples = []
        emails = ['admin@company.com', 'user@example.com', 'threat@evil.com', 'phishing@malicious.org']
        templates = [
            """The email security gateway detected a sophisticated phishing email from {email} that was designed to trick employees into revealing their login credentials. The security team analyzed the email content and discovered that it contained a malicious link that would redirect users to a fake login page designed to steal their credentials. The security team immediately blocked the sender's email address and notified all employees about the phishing attempt to prevent them from falling victim to the attack. The investigation began when the security team received reports from employees about suspicious emails. The security analysts discovered that the phishing email was part of a larger campaign targeting multiple organizations, and that the threat actors were using sophisticated techniques to make the emails appear legitimate.""",
            """The threat intelligence investigation identified email address {email} as being used by a known threat actor group to conduct social engineering attacks. The security analysts discovered that the threat actors were using this email address to send targeted phishing emails to key personnel in the organization. The security team added this email address to the threat intelligence database and implemented additional email security controls to prevent similar attacks. The investigation began when the security team received intelligence about a potential attack targeting the organization's infrastructure. The OSINT analysts used various techniques to track the threat actor's online activities, discovering that they were using multiple email addresses to conduct their attacks.""",
        ]
        for i in range(count):
            email = random.choice(emails)
            template = random.choice(templates)
            context = template.format(email=email)
            email_pos = context.find(email)
            if email_pos != -1:
                examples.append((context, [[email_pos, email_pos + len(email), "EMAIL_ADDRESS"]]))
        return examples
    
    # Generator functions
    generators = {
        'EMOJI': create_context_rich_emoji_examples,
        'PHONE_NUMBER': create_context_rich_phone_examples,
        'DATE': create_context_rich_date_examples,
        'MALWARE_TYPE': create_context_rich_malware_examples,
        'IP_ADDRESS': create_context_rich_ip_examples,
        'SSN': create_context_rich_ssn_examples,
        'LLM_MODEL': create_context_rich_llm_model_examples,
        'TIME': create_context_rich_time_examples,
        'LONGITUDE': lambda c: create_context_rich_coordinate_examples(c, 'LONGITUDE'),
        'DATACENTER': create_context_rich_datacenter_examples,
        'COMPLIANCE_FRAMEWORK': create_context_rich_compliance_examples,
        'LATITUDE': lambda c: create_context_rich_coordinate_examples(c, 'LATITUDE'),
        'GITHUB_REPO_URL': create_context_rich_github_examples,
        'IPV6_ADDRESS': create_context_rich_ipv6_examples,
        'EMAIL_ADDRESS': create_context_rich_email_examples,
    }
    
    # Generate and add examples for each entity type
    for entity_type, target_count in TOP_MISSED_TYPES.items():
        print(f"Processing {entity_type} (target: {target_count} examples)...")
        
        generator = generators.get(entity_type)
        if not generator:
            print(f"  ⚠️  No generator for {entity_type} yet")
            continue
        
        examples = generator(target_count)
        print(f"  Generated {len(examples)} context-rich examples")
        
        # Get relevant files
        pillars = ENTITY_PILLAR_MAPPING.get(entity_type, ['threat_intelligence', 'incident_response'])
        
        for pillar in pillars:
            # Handle nested paths
            if '/' in pillar:
                pillar_dir = base_dir / pillar
                pillar_name = pillar.split('/')[-1]
            else:
                pillar_dir = base_dir / pillar
                pillar_name = pillar
            
            entity_file = pillar_dir / f"{pillar_name}_entities.jsonl"
            
            if entity_file.exists():
                added = add_examples_to_file(entity_file, examples, entity_type)
                total_added += added
            else:
                print(f"  ⚠️  File not found: {entity_file}")
        
        print()
    
    print("=" * 80)
    print(f"✅ COMPLETE: Added {total_added} total context-rich examples")
    print("=" * 80)
    print()
    print("These examples feature:")
    print("  - Longer, narrative-style contexts (200-500 words)")
    print("  - Entities appearing naturally within realistic scenarios")
    print("  - Multiple related entities in the same context")
    print("  - Realistic cybersecurity and OSINT scenarios")

if __name__ == "__main__":
    main()

