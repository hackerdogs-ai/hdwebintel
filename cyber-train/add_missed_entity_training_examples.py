#!/usr/bin/env python3
"""
Add Training Examples for Top Missed Entity Types

This script adds training examples for the top 20 missed entity types
identified in the comprehensive test suite analysis.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
import random
from collections import Counter

# Load catalog files
def load_catalog(catalog_path: Path) -> List[str]:
    """Load entities from catalog file."""
    if not catalog_path.exists():
        return []
    entities = []
    with open(catalog_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                entities.append(line)
    return entities

# Top 20 missed entity types with target counts
MISSED_ENTITY_TARGETS = {
    'EMOJI': 200,
    'PHONE_NUMBER': 150,
    'MALWARE_TYPE': 100,
    'TIME': 100,
    'LONGITUDE': 100,
    'LATITUDE': 100,
    'IPV6_ADDRESS': 50,
    'SSN': 50,
    'LLM_PROVIDER': 50,
    'LLM_MODEL': 50,
    'IP_ADDRESS': 50,
    'COMPLIANCE_FRAMEWORK': 50,
    'GITHUB_REPO_URL': 50,
    'EMAIL_ADDRESS': 50,
    'DMS_COORDINATES': 50,
    'HASH': 50,
    'PORT': 50,
    'HOST_TYPE': 50,
    'THREAT_ACTOR': 50,
    'CVE_ID': 50,
}

# Entity type to pillar mapping
ENTITY_PILLAR_MAPPING = {
    'EMOJI': ['socmint', 'osint', 'threat_intel'],
    'PHONE_NUMBER': ['socmint', 'osint', 'data_privacy_sovereignty', 'threat_intel'],
    'MALWARE_TYPE': ['threat_intel', 'incident_response', 'endpoint_security', 'detection_correlation'],
    'TIME': ['incident_response', 'audit_compliance', 'detection_correlation'],
    'LONGITUDE': ['geoint', 'osint', 'threat_intel'],
    'LATITUDE': ['geoint', 'osint', 'threat_intel'],
    'IPV6_ADDRESS': ['network_security', 'threat_intel', 'incident_response'],
    'SSN': ['data_privacy_sovereignty', 'incident_response', 'audit_compliance'],
    'LLM_PROVIDER': ['ai_security', 'threat_intel'],
    'LLM_MODEL': ['ai_security', 'threat_intel'],
    'IP_ADDRESS': ['network_security', 'threat_intel', 'incident_response', 'detection_correlation'],
    'COMPLIANCE_FRAMEWORK': ['audit_compliance', 'governance_risk_strategy'],
    'GITHUB_REPO_URL': ['threat_intel', 'osint', 'application_security'],
    'EMAIL_ADDRESS': ['threat_intel', 'incident_response', 'socmint', 'detection_correlation'],
    'DMS_COORDINATES': ['geoint', 'osint'],
    'HASH': ['incident_response', 'endpoint_security', 'threat_intel'],
    'PORT': ['network_security', 'threat_intel', 'incident_response'],
    'HOST_TYPE': ['network_security', 'threat_intel', 'incident_response'],
    'THREAT_ACTOR': ['threat_intel', 'incident_response', 'detection_correlation'],
    'CVE_ID': ['vulnerability_mgmt', 'threat_intel', 'incident_response'],
}

def generate_emoji_examples(count: int) -> List[Tuple[str, List]]:
    """Generate emoji examples with longer context."""
    examples = []
    emojis = ['🔐', '🛡️', '⚠️', '🚨', '💻', '🦠', '⚡', '🔍', '📊', '🎯', '✅', '❌', '🔴', '🟡', '🟢']
    
    contexts = [
        "Security alert {emoji} detected suspicious activity on the network. The security operations center received multiple alerts indicating potential breach attempts from IP address 192.168.1.100. The threat intelligence team immediately began investigating the source of the attack and discovered that the malicious actor was attempting to exploit a known vulnerability CVE-2021-44228 in the Log4j library.",
        "Threat intelligence report {emoji} indicates APT activity in the organization's network. The security analysts discovered that the advanced persistent threat group APT29 was responsible for the sophisticated attack campaign that targeted multiple endpoints across the corporate network. The investigation revealed that the attackers used custom malware variants including WannaCry and NotPetya to compromise systems.",
        "Malware detected {emoji} hash: abc123def4567890abcdef1234567890abcdef12. The endpoint detection and response system identified a suspicious file with the SHA-256 hash that matched known threat signatures in the VirusTotal database. The security team immediately quarantined the infected system and began forensic analysis to determine the scope of the infection.",
        "Incident response {emoji} CVE-2021-44228 exploited on production server. The security incident response team was alerted to a critical vulnerability exploitation that occurred on the main web server at IP address 10.0.0.5. The Log4j vulnerability was actively being exploited by threat actors who gained unauthorized access to sensitive customer data stored in the database.",
        "OSINT analysis {emoji} found coordinates 40.7128, -74.0060 in image metadata. The open source intelligence investigation team analyzed social media posts and discovered that threat actors were sharing geolocation information embedded in image files. The coordinates pointed to a location in New York City where the threat actors were operating from.",
        "Social media post {emoji} user @threat_actor mentioned suspicious activity. The security team monitoring social media platforms identified a post from a known threat actor account that was discussing potential attack targets. The OSINT analysts cross-referenced the information with threat intelligence feeds and discovered connections to previous attack campaigns.",
        "Email phishing {emoji} from admin@evil.com targeting employees. The email security gateway detected a sophisticated phishing campaign originating from the domain evil.com. The malicious emails were designed to trick employees into clicking on links that would download malware onto their workstations. The security team immediately blocked the sender domain and notified all employees.",
        "Network traffic {emoji} IP 192.168.1.100 flagged by intrusion detection system. The network security monitoring system detected anomalous traffic patterns from the internal IP address that were consistent with data exfiltration attempts. The security analysts reviewed the network logs and discovered that the compromised system was attempting to communicate with external command and control servers.",
    ]
    
    for _ in range(count):
        emoji = random.choice(emojis)
        context = random.choice(contexts).format(emoji=emoji)
        emoji_pos = context.find(emoji)
        if emoji_pos != -1:
            examples.append((context, [[emoji_pos, emoji_pos + len(emoji), "EMOJI"]]))
    
    return examples

def generate_phone_examples(count: int) -> List[Tuple[str, List]]:
    """Generate phone number examples with longer context."""
    examples = []
    
    formats = [
        "+1-555-123-4567",
        "(555) 123-4567",
        "555.123.4567",
        "+15551234567",
        "+44 20 7946 0958",
        "+49 30 2273 0",
        "+33 1 42 86 83 26",
        "+81 3 1234 5678",
        "555-1234",
        "+1 (555) 123-4567 ext 123",
    ]
    
    contexts = [
        "The security incident response team received a call from contact number {phone} reporting a potential data breach. The caller identified themselves as an employee from the finance department who noticed unusual activity in their account. The security analysts immediately began investigating the reported incident and discovered that unauthorized access had been gained to sensitive financial records.",
        "The threat intelligence investigation revealed that phone number {phone} was associated with a known threat actor group. The OSINT analysts discovered that this phone number was used to register multiple fake social media accounts that were used to spread disinformation and conduct social engineering attacks. The security team added this phone number to the threat intelligence database for ongoing monitoring.",
        "During the OSINT investigation, the security analysts found that phone number {phone} was reported in multiple data breach databases. The phone number appeared in leaked credential databases from previous security incidents, indicating that it may have been compromised. The security team recommended that any accounts associated with this phone number should be immediately reviewed and secured.",
        "The user registration system recorded phone number {phone} during account creation. The security team discovered that this phone number was used to create multiple accounts with different email addresses, which is a common pattern for fraudulent account creation. The security analysts flagged these accounts for review and implemented additional verification requirements.",
        "The data privacy investigation revealed that phone number {phone} was included in a PII data leak that occurred last month. The leaked information included names, email addresses, and phone numbers of customers who had registered for the company's services. The security team immediately notified affected customers and implemented additional security measures to prevent future data breaches.",
        "The social media investigation found that phone number {phone} was linked to a suspicious profile on multiple platforms. The OSINT analysts discovered that this phone number was used to verify accounts that were later used to spread malicious content and conduct phishing campaigns. The security team reported these findings to the social media platforms for account suspension.",
    ]
    
    for _ in range(count):
        phone = random.choice(formats)
        context = random.choice(contexts).format(phone=phone)
        phone_pos = context.find(phone)
        if phone_pos != -1:
            examples.append((context, [[phone_pos, phone_pos + len(phone), "PHONE_NUMBER"]]))
    
    return examples

def generate_malware_examples(count: int, catalog: List[str]) -> List[Tuple[str, List]]:
    """Generate malware type examples with longer context."""
    examples = []
    
    if not catalog:
        catalog = ['Trojan', 'Virus', 'Worm', 'Ransomware', 'Spyware', 'Rootkit', 'Botnet', 'WannaCry', 'NotPetya', 'Ryuk', 'Emotet', 'TrickBot']
    
    contexts = [
        "The endpoint detection and response system detected {malware} malware on an employee workstation. The security team immediately isolated the infected system from the network to prevent the malware from spreading to other devices. The forensic analysis revealed that the malware was delivered through a malicious email attachment that was opened by an unsuspecting employee. The security analysts identified the malware variant and began remediation procedures.",
        "The threat intelligence team discovered that the threat actor deployed a {malware} variant as part of their attack campaign. The malware was specifically designed to evade traditional antivirus detection by using advanced obfuscation techniques. The security team analyzed the malware sample and discovered that it was capable of establishing persistent backdoor access to compromised systems. The threat actors used this malware to maintain long-term access to the organization's network.",
        "During the incident response investigation, the security team found evidence of {malware} infection on multiple systems across the network. The malware had been present in the environment for several weeks before being detected, allowing the threat actors to exfiltrate sensitive data. The security analysts worked around the clock to contain the infection and prevent further data loss. The incident response team documented all findings for the post-incident review.",
        "The malware analysis team identified the {malware} family through static and dynamic analysis of the malicious code. The security researchers discovered that the malware was part of a larger malware-as-a-service operation that was being used by multiple threat actor groups. The analysis revealed sophisticated evasion techniques including code obfuscation, anti-debugging measures, and encrypted command and control communications. The security team shared the findings with the threat intelligence community.",
        "The security operations center received an alert indicating that {malware} was detected in the network traffic. The network security monitoring system identified suspicious communication patterns that were consistent with known malware behavior. The security analysts immediately began investigating the source of the infection and discovered that the malware was attempting to establish connections to external command and control servers. The firewall rules were updated to block these malicious connections.",
        "The digital forensics investigation revealed that {malware} had implemented a sophisticated persistence mechanism that allowed it to survive system reboots. The malware created multiple registry entries and scheduled tasks to ensure it would continue running even after system restarts. The security team developed a comprehensive removal procedure that addressed all persistence mechanisms used by the malware. The incident response team verified that all instances of the malware were successfully removed from the affected systems.",
    ]
    
    for _ in range(count):
        malware = random.choice(catalog)
        context = random.choice(contexts).format(malware=malware)
        malware_pos = context.find(malware)
        if malware_pos != -1:
            examples.append((context, [[malware_pos, malware_pos + len(malware), "MALWARE_TYPE"]]))
    
    return examples

def generate_time_examples(count: int) -> List[Tuple[str, List]]:
    """Generate time examples with longer context."""
    examples = []
    
    formats = [
        "14:30",
        "2:30 PM",
        "14:30:00",
        "2:30:00 PM",
        "14:30 UTC",
        "02:30:00",
    ]
    
    contexts = [
        "The security incident occurred at {time} on 2024-11-30 when the intrusion detection system detected unauthorized access attempts from multiple IP addresses. The security operations center immediately began investigating the incident and discovered that the threat actors had gained access to the corporate network through a compromised user account. The incident response team worked throughout the night to contain the breach and prevent further unauthorized access to sensitive systems.",
        "The security event monitoring system detected an anomalous event with timestamp {time} that triggered multiple security alerts. The security analysts reviewed the event logs and discovered that the event was associated with a known attack pattern used by advanced persistent threat groups. The security team immediately escalated the incident to the threat intelligence team for further analysis and began implementing additional security controls to prevent similar attacks.",
        "The network security monitoring system triggered an alert at {time} for suspicious activity originating from IP address 192.168.1.100. The security analysts reviewed the network traffic logs and discovered that the system was attempting to establish connections to external command and control servers. The security team immediately blocked the malicious IP address and began investigating the source of the compromise to determine how the system was initially infected.",
        "The security log analysis revealed a log entry at {time} that showed suspicious activity patterns consistent with data exfiltration attempts. The security analysts discovered that the threat actors were attempting to transfer large amounts of data from the internal network to external servers. The security team immediately implemented network segmentation to prevent further data loss and began forensic analysis to determine the scope of the data breach.",
        "The security investigation determined that the attack started at {time} and lasted approximately 2 hours before being detected by the security monitoring systems. During this time, the threat actors were able to access multiple systems and exfiltrate sensitive customer data. The security team worked with law enforcement to investigate the attack and implemented additional security measures to prevent future incidents. The post-incident review identified several areas for improvement in the security monitoring and response procedures.",
    ]
    
    for _ in range(count):
        time_str = random.choice(formats)
        context = random.choice(contexts).format(time=time_str)
        time_pos = context.find(time_str)
        if time_pos != -1:
            examples.append((context, [[time_pos, time_pos + len(time_str), "TIME"]]))
    
    return examples

def generate_coordinate_examples(count: int, coord_type: str) -> List[Tuple[str, List]]:
    """Generate latitude or longitude examples with longer context."""
    examples = []
    
    if coord_type == 'LATITUDE':
        values = ['40.7128', '-40.7128', '52.5200', '-33.8688', '35.6762', '51.5074']
        coord_name = 'latitude'
    else:  # LONGITUDE
        values = ['-74.0060', '13.4050', '151.2093', '139.6503', '139.6917', '-0.1278']
        coord_name = 'longitude'
    
    contexts = [
        "The geolocation analysis of the threat actor's network infrastructure revealed coordinates with {coord_name} {coord} that pointed to a location in a major metropolitan area. The OSINT investigation team cross-referenced these coordinates with known threat actor locations and discovered that this location was associated with previous cyber attacks. The security team shared this intelligence with law enforcement agencies for further investigation.",
        "The GPS location metadata analysis identified {coord_name} {coord} embedded in image files that were shared on social media platforms by the threat actors. The security analysts discovered that the threat actors were inadvertently revealing their location through geotagged images. The OSINT team used this information to track the threat actors' movements and identify potential safe houses or operational bases.",
        "The open source intelligence analysis found coordinates with {coord_name} {coord} in leaked documents that were published on dark web forums. The security researchers discovered that these coordinates were associated with a known threat actor group's operational infrastructure. The threat intelligence team added this information to their database and began monitoring for additional indicators of compromise associated with this location.",
        "The IP geolocation analysis determined that the threat actor's command and control servers were located at coordinates with {coord_name} {coord} in a country known for hosting malicious infrastructure. The security team discovered that the threat actors were using compromised cloud infrastructure to host their malicious servers. The security analysts worked with the cloud provider to take down the malicious infrastructure and prevent further attacks.",
        "The digital forensics investigation of image files discovered that the EXIF metadata contained {coord_name} {coord} that revealed the location where the images were taken. The security team discovered that the threat actors were taking photos of sensitive facilities and inadvertently including GPS coordinates in the image metadata. The OSINT analysts used this information to identify the specific locations that were being targeted by the threat actors.",
    ]
    
    for _ in range(count):
        coord = random.choice(values)
        context = random.choice(contexts).format(coord=coord, coord_name=coord_name)
        coord_pos = context.find(coord)
        if coord_pos != -1:
            examples.append((context, [[coord_pos, coord_pos + len(coord), coord_type]]))
    
    return examples

def generate_ipv6_examples(count: int) -> List[Tuple[str, List]]:
    """Generate IPv6 address examples with longer context."""
    examples = []
    
    formats = [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "2001:db8:85a3::8a2e:370:7334",
        "2001:db8::1",
        "::1",
        "2001:db8:85a3:0:0:8a2e:370:7334",
        "fe80::1%lo0",
    ]
    
    contexts = [
        "The network security monitoring system detected IPv6 address {ipv6} in network traffic that was attempting to establish connections to internal systems. The security analysts reviewed the network flow data and discovered that the IPv6 address was associated with a known threat actor infrastructure. The security team immediately blocked all traffic from this IPv6 address and began investigating the scope of the potential compromise.",
        "The threat intelligence feeds indicated that IPv6 address {ipv6} was being used as a command and control server by an advanced persistent threat group. The security team discovered that the threat actors were using IPv6 addresses to evade detection since many security tools are not properly configured to monitor IPv6 traffic. The security operations center updated their monitoring rules to include IPv6 addresses in threat intelligence feeds.",
        "The next-generation firewall blocked a connection attempt from IPv6 address {ipv6} that was attempting to access internal resources. The security team reviewed the firewall logs and discovered that the connection attempt was part of a larger reconnaissance campaign targeting the organization's network infrastructure. The security analysts added this IPv6 address to the threat intelligence database and implemented additional network segmentation controls.",
        "The network vulnerability scan discovered that IPv6 address {ipv6} was responding on port 443 with a web server that contained known security vulnerabilities. The security team discovered that this IPv6 address was hosting a phishing website that was designed to steal user credentials. The security analysts worked with the hosting provider to take down the malicious website and prevent further attacks.",
        "The security operations center received an alert indicating suspicious activity originating from IPv6 address {ipv6} that was attempting to perform port scans on internal systems. The security analysts discovered that the IPv6 address was associated with a botnet that was scanning for vulnerable systems. The security team immediately blocked the IPv6 address and began monitoring for additional attack attempts from similar sources.",
    ]
    
    for _ in range(count):
        ipv6 = random.choice(formats)
        context = random.choice(contexts).format(ipv6=ipv6)
        ipv6_pos = context.find(ipv6)
        if ipv6_pos != -1:
            examples.append((context, [[ipv6_pos, ipv6_pos + len(ipv6), "IPV6_ADDRESS"]]))
    
    return examples

def generate_ssn_examples(count: int) -> List[Tuple[str, List]]:
    """Generate SSN examples with longer context."""
    examples = []
    
    formats = [
        "123-45-6789",
        "123 45 6789",
        "123456789",
    ]
    
    contexts = [
        "The data privacy investigation revealed that the PII data leak included SSN {ssn} along with other sensitive personal information such as names, addresses, and phone numbers. The security team discovered that the data breach occurred when an unauthorized third party gained access to the customer database through a compromised API endpoint. The organization immediately notified affected customers and regulatory authorities as required by data protection regulations.",
        "The security incident response team discovered that the data breach exposed SSN {ssn} and other personally identifiable information of over 10,000 customers. The forensic investigation revealed that the threat actors had gained access to the database through a SQL injection vulnerability in the web application. The security team worked with law enforcement to investigate the breach and implemented additional security controls to prevent future incidents.",
        "The compliance audit team found a privacy violation where SSN {ssn} was discovered in unencrypted log files that were accessible to unauthorized personnel. The security team discovered that the application was logging sensitive customer information without proper encryption or access controls. The compliance team immediately implemented data masking procedures and updated the logging policies to prevent sensitive information from being stored in plain text.",
        "The security compliance audit discovered that SSN {ssn} was stored in an unprotected database table that was accessible to all database users. The security team found that the sensitive data was not encrypted at rest and was accessible through standard database queries. The compliance team immediately implemented database encryption and access controls to protect the sensitive information and ensure compliance with data protection regulations.",
        "The GDPR compliance review identified a violation where SSN {ssn} was stored in an unencrypted format in the customer relationship management system. The security team discovered that the system was not properly configured to encrypt sensitive personal data as required by the General Data Protection Regulation. The compliance team immediately implemented encryption for all sensitive data fields and updated the data processing procedures to ensure full compliance with GDPR requirements.",
    ]
    
    for _ in range(count):
        ssn = random.choice(formats)
        context = random.choice(contexts).format(ssn=ssn)
        ssn_pos = context.find(ssn)
        if ssn_pos != -1:
            examples.append((context, [[ssn_pos, ssn_pos + len(ssn), "SSN"]]))
    
    return examples

def generate_llm_examples(count: int, entity_type: str, catalog: List[str]) -> List[Tuple[str, List]]:
    """Generate LLM model or provider examples with longer context."""
    examples = []
    
    if not catalog:
        if entity_type == 'LLM_MODEL':
            catalog = ['GPT-4', 'GPT-3.5', 'Claude 3', 'Gemini Pro', 'LLaMA 2']
        else:
            catalog = ['OpenAI', 'Anthropic', 'Google', 'Microsoft', 'Meta']
    
    if entity_type == 'LLM_MODEL':
        contexts = [
            "The AI security team conducted a comprehensive security analysis using the {llm} model to identify potential vulnerabilities in the organization's AI infrastructure. The security assessment revealed several security concerns including prompt injection vulnerabilities and data leakage risks. The security team developed a comprehensive security framework to address these issues and ensure the safe deployment of AI models in production environments.",
            "The threat detection system was powered by the {llm} model to analyze large volumes of security logs and identify potential threats. The AI-powered threat detection system was able to identify sophisticated attack patterns that traditional signature-based detection systems would have missed. The security operations center integrated the AI model into their security monitoring workflow to improve threat detection capabilities.",
            "The security team performed a vulnerability assessment of the {llm} model implementation to identify potential security weaknesses. The assessment revealed that the model was vulnerable to adversarial attacks and prompt injection techniques that could be used to extract sensitive information. The security team worked with the AI development team to implement security controls and mitigate the identified vulnerabilities.",
            "The security review of the {llm} model implementation identified several security concerns including insufficient access controls and lack of input validation. The security team discovered that the model was processing sensitive customer data without proper encryption or access controls. The security team recommended implementing additional security measures to protect the sensitive data and ensure compliance with data protection regulations.",
        ]
    else:  # LLM_PROVIDER
        contexts = [
            "The security team conducted a comprehensive security assessment of LLM provider {llm} to evaluate their security practices and data protection measures. The assessment included reviewing the provider's security certifications, data handling procedures, and incident response capabilities. The security team discovered that the provider had implemented strong security controls including encryption at rest and in transit, regular security audits, and comprehensive access controls.",
            "The organization's AI security policy requires that all LLM providers including {llm} must undergo regular security assessments to ensure compliance with security standards. The security team reviewed the provider's security documentation and conducted penetration testing to identify potential vulnerabilities. The assessment revealed that the provider had strong security controls in place but recommended additional monitoring and logging capabilities.",
            "The data privacy team evaluated LLM provider {llm} to ensure that they meet the organization's data protection requirements. The evaluation included reviewing the provider's data processing agreements, privacy policies, and compliance certifications. The team discovered that the provider was compliant with major data protection regulations including GDPR and HIPAA, making them suitable for processing sensitive data.",
            "The security operations center monitored the usage of LLM provider {llm} to detect any suspicious activity or potential security incidents. The monitoring system tracked API usage patterns, data access logs, and authentication events to identify potential security threats. The security team discovered that the provider had implemented comprehensive logging and monitoring capabilities that enabled effective security monitoring.",
        ]
    
    for _ in range(count):
        llm = random.choice(catalog)
        context = random.choice(contexts).format(llm=llm)
        llm_pos = context.find(llm)
        if llm_pos != -1:
            examples.append((context, [[llm_pos, llm_pos + len(llm), entity_type]]))
    
    return examples

def generate_ip_examples(count: int) -> List[Tuple[str, List]]:
    """Generate IP address examples with longer context."""
    examples = []
    
    ips = [
        "192.168.1.100",
        "10.0.0.1",
        "172.16.0.1",
        "203.0.113.1",
        "198.51.100.1",
    ]
    
    contexts = [
        "The network security monitoring system detected suspicious activity from IP address {ip} in the network logs that was attempting to access multiple internal systems. The security analysts reviewed the network flow data and discovered that the IP address was associated with a known threat actor infrastructure. The security team immediately blocked all traffic from this IP address and began investigating the scope of the potential compromise to determine if any systems were successfully breached.",
        "The threat intelligence investigation revealed that IP address {ip} was being used as a command and control server by an advanced persistent threat group. The security team discovered that the threat actors were using this IP address to communicate with compromised systems and exfiltrate sensitive data. The security operations center updated their threat intelligence feeds to include this IP address and implemented network controls to block all communication with this malicious infrastructure.",
        "The next-generation firewall automatically blocked a connection attempt from IP address {ip} that was attempting to exploit a known vulnerability in the web application. The security team reviewed the firewall logs and discovered that the connection attempt was part of a larger automated attack campaign targeting multiple organizations. The security analysts added this IP address to the threat intelligence database and shared the information with other security teams to help prevent similar attacks.",
        "The security operations center received an alert indicating malicious activity originating from IP address {ip} that was attempting to perform brute force attacks on user accounts. The security analysts discovered that the IP address was associated with a botnet that was conducting coordinated attacks against multiple organizations. The security team immediately blocked the IP address and implemented additional authentication controls to prevent successful brute force attacks.",
        "The network vulnerability scan identified IP address {ip} as a compromised system that was being used to launch attacks against other systems on the network. The security team discovered that the system had been infected with malware that was allowing threat actors to maintain persistent access. The incident response team immediately isolated the compromised system from the network and began forensic analysis to determine how the system was initially compromised and what data may have been accessed.",
    ]
    
    for _ in range(count):
        ip = random.choice(ips)
        context = random.choice(contexts).format(ip=ip)
        ip_pos = context.find(ip)
        if ip_pos != -1:
            examples.append((context, [[ip_pos, ip_pos + len(ip), "IP_ADDRESS"]]))
    
    return examples

def generate_compliance_examples(count: int, catalog: List[str]) -> List[Tuple[str, List]]:
    """Generate compliance framework examples with longer context."""
    examples = []
    
    if not catalog:
        catalog = ['GDPR', 'HIPAA', 'PCI DSS', 'SOX', 'NIST CSF', 'ISO 27001']
    
    contexts = [
        "The compliance team conducted a comprehensive audit to ensure that all security controls meet the {framework} requirements for data protection and security. The audit included reviewing security policies, access controls, encryption procedures, and incident response capabilities. The security team discovered several areas where the organization needed to implement additional controls to achieve full compliance with the framework requirements. The compliance team developed a remediation plan to address the identified gaps and ensure ongoing compliance.",
        "The security architecture team designed the security controls to be aligned with the {framework} security standards to ensure that the organization meets all regulatory requirements. The security team implemented comprehensive access controls, encryption mechanisms, and monitoring capabilities that are consistent with the framework's security recommendations. The compliance team regularly reviews the security controls to ensure they continue to meet the framework requirements as the threat landscape evolves.",
        "The security assessment team performed a detailed compliance assessment against the {framework} to evaluate the organization's current security posture. The assessment included reviewing security documentation, conducting technical testing, and interviewing key personnel to understand the security implementation. The assessment revealed that the organization had implemented most of the required security controls but identified several areas for improvement to achieve full compliance with the framework standards.",
        "The compliance review team conducted a comprehensive review of the organization's security posture against the {framework} requirements to identify any compliance gaps. The review included evaluating security policies, procedures, and technical controls to ensure they meet the framework's security standards. The team discovered that the organization had a strong security foundation but needed to enhance documentation and implement additional monitoring capabilities to fully comply with the framework requirements.",
        "The security team evaluated the organization's security posture against the {framework} standards to determine the current level of compliance. The evaluation included reviewing security controls, conducting risk assessments, and analyzing security incident data to identify areas of non-compliance. The security team developed a comprehensive compliance roadmap that outlines the steps needed to achieve and maintain full compliance with the framework requirements.",
    ]
    
    for _ in range(count):
        framework = random.choice(catalog)
        context = random.choice(contexts).format(framework=framework)
        framework_pos = context.find(framework)
        if framework_pos != -1:
            examples.append((context, [[framework_pos, framework_pos + len(framework), "COMPLIANCE_FRAMEWORK"]]))
    
    return examples

def generate_github_repo_url_examples(count: int) -> List[Tuple[str, List]]:
    """Generate GitHub repo URL examples with longer context."""
    examples = []
    
    repos = [
        "https://github.com/user/repo",
        "github.com/user/repo",
        "https://github.com/org/malware",
        "github.com/threat-actor/tools",
    ]
    
    contexts = [
        "The threat intelligence team discovered that threat actors were using GitHub repository {repo} to host malicious code and share attack tools with other members of their group. The security analysts reviewed the repository contents and discovered that it contained multiple malware samples, exploit code, and detailed instructions for conducting cyber attacks. The security team reported the repository to GitHub's security team and worked with them to have the malicious content removed.",
        "The OSINT investigation team discovered GitHub repository {repo} during their analysis of threat actor infrastructure. The security researchers found that the repository contained source code for custom malware variants and tools used in previous attack campaigns. The security team analyzed the code to understand the threat actors' capabilities and developed countermeasures to detect and prevent attacks using these tools.",
        "The security analysis team conducted a comprehensive security review of GitHub repository {repo} to identify potential security vulnerabilities and malicious code. The analysis revealed that the repository contained multiple security issues including hardcoded credentials, vulnerable dependencies, and code that could be used for malicious purposes. The security team documented their findings and recommended security improvements to the repository maintainers.",
        "The threat intelligence investigation identified GitHub repository {repo} as hosting malicious code that was being used in active attack campaigns. The security team discovered that the repository contained exploit code, malware samples, and tools designed to compromise systems and exfiltrate data. The security analysts worked with GitHub's security team to have the repository taken down and prevent further distribution of the malicious code.",
    ]
    
    for _ in range(count):
        repo = random.choice(repos)
        context = random.choice(contexts).format(repo=repo)
        repo_pos = context.find(repo)
        if repo_pos != -1:
            examples.append((context, [[repo_pos, repo_pos + len(repo), "GITHUB_REPO_URL"]]))
    
    return examples

def generate_email_examples(count: int) -> List[Tuple[str, List]]:
    """Generate email address examples with longer context."""
    examples = []
    
    emails = [
        "admin@company.com",
        "user@example.com",
        "threat@evil.com",
        "phishing@malicious.org",
    ]
    
    contexts = [
        "The email security gateway detected a sophisticated phishing email from {email} that was designed to trick employees into revealing their login credentials. The security team analyzed the email content and discovered that it contained a malicious link that would redirect users to a fake login page designed to steal their credentials. The security team immediately blocked the sender's email address and notified all employees about the phishing attempt to prevent them from falling victim to the attack.",
        "The threat intelligence investigation identified email address {email} as being used by a known threat actor group to conduct social engineering attacks. The security analysts discovered that the threat actors were using this email address to send targeted phishing emails to key personnel in the organization. The security team added this email address to the threat intelligence database and implemented additional email security controls to prevent similar attacks.",
        "The security operations center received an alert indicating that a suspicious email from {email} had been detected by the email security system. The security team reviewed the email content and discovered that it contained a malicious attachment that was designed to install malware on the recipient's computer. The security team immediately quarantined the email and began investigating to determine if any systems had been compromised by the malicious attachment.",
        "The OSINT investigation team discovered email address {email} in multiple data breach databases that were published on dark web forums. The security analysts found that this email address was associated with compromised accounts from previous security incidents. The security team cross-referenced this information with their own user database and discovered that several employees had accounts associated with this email address, requiring immediate password resets and security reviews.",
    ]
    
    for _ in range(count):
        email = random.choice(emails)
        context = random.choice(contexts).format(email=email)
        email_pos = context.find(email)
        if email_pos != -1:
            examples.append((context, [[email_pos, email_pos + len(email), "EMAIL_ADDRESS"]]))
    
    return examples

def generate_dms_coordinates_examples(count: int) -> List[Tuple[str, List]]:
    """Generate DMS coordinate examples with longer context."""
    examples = []
    
    formats = [
        "40°42'46\"N 74°00'22\"W",
        "52°31'44.7\"N 13°23'05.7\"E",
        "40°42'46.0\"N 74°00'22.0\"W",
    ]
    
    contexts = [
        "The digital forensics investigation of image files discovered GPS coordinates {coords} embedded in the image metadata that revealed the exact location where the photos were taken. The security team discovered that threat actors were taking photographs of sensitive facilities and inadvertently including precise GPS coordinates in the image EXIF data. The OSINT analysts used this information to identify the specific locations that were being targeted by the threat actors and shared this intelligence with law enforcement agencies.",
        "The geolocation data extraction process identified coordinates {coords} from social media posts that were shared by the threat actors. The security analysts discovered that the threat actors were using social media platforms to share information about their operations and were inadvertently revealing their location through geotagged content. The OSINT team cross-referenced these coordinates with known threat actor locations and discovered connections to previous attack campaigns.",
        "The open source intelligence analysis found coordinates {coords} in leaked documents that were published on dark web forums by the threat actors. The security researchers discovered that these coordinates were associated with a known threat actor group's operational infrastructure and safe houses. The threat intelligence team added this information to their database and began monitoring for additional indicators of compromise associated with this location.",
        "The threat intelligence investigation identified coordinates {coords} as the location of threat actor command and control infrastructure based on IP geolocation data and network traffic analysis. The security team discovered that the threat actors were using compromised cloud infrastructure hosted at this location to operate their malicious servers. The security analysts worked with the cloud provider and law enforcement to take down the malicious infrastructure and prevent further attacks.",
    ]
    
    for _ in range(count):
        coords = random.choice(formats)
        context = random.choice(contexts).format(coords=coords)
        coords_pos = context.find(coords)
        if coords_pos != -1:
            examples.append((context, [[coords_pos, coords_pos + len(coords), "DMS_COORDINATES"]]))
    
    return examples

def generate_hash_examples(count: int) -> List[Tuple[str, List]]:
    """Generate hash examples with longer context."""
    examples = []
    
    formats = [
        "abc123def456",
        "a1b2c3d4e5f6",
        "5d41402abc4b2a76b9719d911017c592",
        "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ]
    
    contexts = [
        "The endpoint detection and response system detected malware with hash {hash} in the threat intelligence database that matched a known malicious file signature. The security team immediately quarantined the infected system and began forensic analysis to determine how the malware was delivered and what systems may have been compromised. The security analysts discovered that the malware was part of a larger attack campaign targeting multiple organizations in the same industry sector.",
        "The file integrity monitoring system identified a file with hash {hash} that matched a known threat signature in the VirusTotal database. The security team discovered that the file was attempting to execute on a critical server that contained sensitive customer data. The security operations center immediately blocked the file execution and began investigating to determine if the malware had successfully compromised the system or if it was detected before it could cause damage.",
        "The security scanning system found a file with hash {hash} during a routine security scan that was flagged as potentially malicious by multiple antivirus engines. The security team analyzed the file and discovered that it contained code designed to establish a backdoor connection to external command and control servers. The security analysts worked with the threat intelligence team to identify the threat actor group responsible for the malware and develop countermeasures.",
        "The threat intelligence feed identified hash {hash} as being associated with a sophisticated malware variant that was being used in active attack campaigns. The security team discovered that the malware was designed to evade traditional antivirus detection by using advanced obfuscation techniques and polymorphic code. The security operations center updated their threat detection rules to include this hash and began monitoring for any systems that may have been infected with this malware variant.",
    ]
    
    for _ in range(count):
        hash_val = random.choice(formats)
        context = random.choice(contexts).format(hash=hash_val)
        hash_pos = context.find(hash_val)
        if hash_pos != -1:
            examples.append((context, [[hash_pos, hash_pos + len(hash_val), "HASH"]]))
    
    return examples

def generate_port_examples(count: int) -> List[Tuple[str, List]]:
    """Generate port examples with longer context."""
    examples = []
    
    ports = ['443', '80', '22', '8080', '3306', '5432', '3389', '1433']
    
    contexts = [
        "The network security scan discovered that port {port} was open on the production server, which was unexpected based on the server's configuration. The security team reviewed the network configuration and discovered that the port had been opened to allow remote access for maintenance purposes but was not properly secured. The security team immediately implemented additional security controls including firewall rules and access restrictions to prevent unauthorized access through this port.",
        "The vulnerability assessment found that port {port} was exposed on the network perimeter without proper security controls. The security analysts discovered that the port was being used to host a web application that contained known security vulnerabilities. The security team recommended closing the port or implementing additional security controls including web application firewall rules and intrusion detection monitoring to protect against potential attacks.",
        "The firewall configuration review identified that port {port} had a firewall rule that was allowing unrestricted access from the internet. The security team discovered that this configuration violated the organization's security policy which requires that all external-facing ports must be restricted to specific IP addresses or networks. The security team immediately updated the firewall rules to restrict access and prevent unauthorized connections.",
        "The security monitoring system generated an alert indicating that port {port} was being accessed by an unauthorized IP address that was not in the approved access list. The security analysts reviewed the network logs and discovered that the connection attempt was part of a port scanning campaign targeting the organization's network infrastructure. The security team immediately blocked the malicious IP address and implemented additional monitoring to detect similar attack attempts.",
    ]
    
    for _ in range(count):
        port = random.choice(ports)
        context = random.choice(contexts).format(port=port)
        port_pos = context.find(port)
        if port_pos != -1:
            examples.append((context, [[port_pos, port_pos + len(port), "PORT"]]))
    
    return examples

def generate_host_type_examples(count: int) -> List[Tuple[str, List]]:
    """Generate host type examples with longer context."""
    examples = []
    
    hosts = [
        "server-01.internal.com",
        "db.internal.example.com",
        "web.internal.local",
        "mail.company.internal",
    ]
    
    contexts = [
        "The security incident response team discovered that host {host} had been compromised in a sophisticated attack that allowed threat actors to gain unauthorized access to sensitive systems. The security analysts reviewed the system logs and discovered that the threat actors had been present in the environment for several weeks before being detected. The security team immediately isolated the compromised host from the network and began forensic analysis to determine the scope of the breach and identify what data may have been accessed.",
        "The security team conducted a comprehensive security scan of host {host} to identify potential vulnerabilities and security misconfigurations. The scan revealed multiple security issues including outdated software, weak authentication mechanisms, and unnecessary services running on the system. The security team worked with the system administrators to remediate the identified issues and implement additional security controls to prevent future compromises.",
        "The network traffic analysis identified host {host} as the source of suspicious network activity that was consistent with data exfiltration attempts. The security team discovered that the host was attempting to establish connections to external servers that were not part of the organization's approved network infrastructure. The security analysts immediately blocked the suspicious connections and began investigating to determine if the host had been compromised or if the activity was the result of a misconfiguration.",
        "The threat intelligence investigation revealed that threat actors had successfully accessed host {host} through a compromised user account that had administrative privileges. The security team discovered that the threat actors had used this access to install additional malware and establish persistent backdoor access to the system. The incident response team worked around the clock to remove the threat actors' access and prevent further damage to the organization's systems and data.",
    ]
    
    for _ in range(count):
        host = random.choice(hosts)
        context = random.choice(contexts).format(host=host)
        host_pos = context.find(host)
        if host_pos != -1:
            examples.append((context, [[host_pos, host_pos + len(host), "HOST_TYPE"]]))
    
    return examples

def generate_threat_actor_examples(count: int, catalog: List[str]) -> List[Tuple[str, List]]:
    """Generate threat actor examples with longer context."""
    examples = []
    
    if not catalog:
        catalog = ['APT29', 'APT28', 'Lazarus', 'FIN7', 'UNC2452']
    
    contexts = [
        "The threat intelligence team discovered that threat actor {actor} was actively operating in the organization's network based on analysis of attack patterns and infrastructure. The security analysts reviewed the threat intelligence feeds and discovered that the attack techniques used in the recent security incidents matched the known tactics, techniques, and procedures used by this threat actor group. The security team immediately implemented additional security controls and monitoring to detect and prevent further attacks from this threat actor.",
        "The security investigation determined that APT group {actor} was responsible for the sophisticated attack campaign that targeted multiple systems across the organization's network. The forensic analysis revealed that the threat actors had been present in the environment for several months before being detected, allowing them to exfiltrate large amounts of sensitive data. The security team worked with law enforcement and threat intelligence partners to investigate the attack and develop countermeasures to prevent future incidents.",
        "The threat intelligence analysis attributed the recent security breach to threat actor {actor} based on the attack techniques, infrastructure, and malware variants used in the attack. The security team discovered that the threat actors were using custom malware and tools that were previously associated with this threat actor group. The security analysts shared this intelligence with other organizations in the same industry sector to help them prepare for similar attacks.",
        "The security investigation team identified threat actor {actor} as the source of the ongoing attack campaign after analyzing the attack patterns and comparing them with known threat actor profiles. The security team discovered that the threat actors were using sophisticated techniques to evade detection including living-off-the-land tactics and fileless malware. The security operations center updated their detection rules and monitoring capabilities to better identify and respond to attacks from this threat actor group.",
    ]
    
    for _ in range(count):
        actor = random.choice(catalog)
        context = random.choice(contexts).format(actor=actor)
        actor_pos = context.find(actor)
        if actor_pos != -1:
            examples.append((context, [[actor_pos, actor_pos + len(actor), "THREAT_ACTOR"]]))
    
    return examples

def generate_cve_examples(count: int) -> List[Tuple[str, List]]:
    """Generate CVE ID examples with longer context."""
    examples = []
    
    cves = [
        "CVE-2021-44228",
        "cve-2021-44228",
        "CVE-2024-1234",
        "CVE-2023-5678",
    ]
    
    contexts = [
        "The security incident response team discovered that vulnerability {cve} was actively being exploited in the attack that compromised multiple systems in the organization's network. The security analysts reviewed the system logs and discovered that the threat actors had used this vulnerability to gain initial access to the network and then moved laterally to compromise additional systems. The security team immediately applied the available security patches and implemented additional security controls to prevent further exploitation of this vulnerability.",
        "The vulnerability management team identified that security patch for {cve} was required on multiple systems across the organization's network to prevent potential exploitation. The security team discovered that the vulnerability affected a critical component of the organization's infrastructure and could be exploited remotely without authentication. The security operations center prioritized the patching of this vulnerability and worked with system administrators to ensure all affected systems were updated as quickly as possible.",
        "The threat intelligence feeds indicated that vulnerability {cve} was being actively exploited by multiple threat actor groups in attacks targeting organizations in the same industry sector. The security team discovered that the vulnerability was being used as part of a larger attack campaign that was targeting critical infrastructure and sensitive data. The security analysts immediately began scanning the organization's systems to identify any instances of this vulnerability and implemented additional monitoring to detect exploitation attempts.",
        "The security vulnerability scan detected that vulnerability {cve} was present on several systems in the organization's network that had not yet been patched. The security team discovered that the vulnerability was rated as critical severity and could allow threat actors to execute arbitrary code on affected systems. The security operations center immediately began the patch deployment process and implemented network segmentation to isolate the vulnerable systems until they could be patched.",
    ]
    
    for _ in range(count):
        cve = random.choice(cves)
        context = random.choice(contexts).format(cve=cve)
        cve_pos = context.find(cve)
        if cve_pos != -1:
            examples.append((context, [[cve_pos, cve_pos + len(cve), "CVE_ID"]]))
    
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
    catalog_dir = Path("catalogs")
    
    print("=" * 80)
    print("ADDING TRAINING EXAMPLES FOR TOP MISSED ENTITY TYPES")
    print("=" * 80)
    print()
    
    total_added = 0
    
    # Load catalogs
    malware_catalog = load_catalog(catalog_dir / "malware_types.txt")
    threat_actor_catalog = load_catalog(catalog_dir / "threat_actors.txt")
    compliance_catalog = load_catalog(catalog_dir / "compliance_frameworks.txt")
    llm_model_catalog = load_catalog(catalog_dir / "llm_models.txt")
    llm_provider_catalog = load_catalog(catalog_dir / "llm_providers.txt")
    
    # Generate and add examples for each entity type
    generators = {
        'EMOJI': generate_emoji_examples,
        'PHONE_NUMBER': generate_phone_examples,
        'MALWARE_TYPE': lambda c: generate_malware_examples(c, malware_catalog),
        'TIME': generate_time_examples,
        'LONGITUDE': lambda c: generate_coordinate_examples(c, 'LONGITUDE'),
        'LATITUDE': lambda c: generate_coordinate_examples(c, 'LATITUDE'),
        'IPV6_ADDRESS': generate_ipv6_examples,
        'SSN': generate_ssn_examples,
        'LLM_PROVIDER': lambda c: generate_llm_examples(c, 'LLM_PROVIDER', llm_provider_catalog),
        'LLM_MODEL': lambda c: generate_llm_examples(c, 'LLM_MODEL', llm_model_catalog),
        'IP_ADDRESS': generate_ip_examples,
        'COMPLIANCE_FRAMEWORK': lambda c: generate_compliance_examples(c, compliance_catalog),
        'GITHUB_REPO_URL': generate_github_repo_url_examples,
        'EMAIL_ADDRESS': generate_email_examples,
        'DMS_COORDINATES': generate_dms_coordinates_examples,
        'HASH': generate_hash_examples,
        'PORT': generate_port_examples,
        'HOST_TYPE': generate_host_type_examples,
        'THREAT_ACTOR': lambda c: generate_threat_actor_examples(c, threat_actor_catalog),
        'CVE_ID': generate_cve_examples,
    }
    
    for entity_type, target_count in MISSED_ENTITY_TARGETS.items():
        print(f"Processing {entity_type} (target: {target_count} examples)...")
        
        # Generate examples
        generator = generators.get(entity_type)
        if not generator:
            print(f"  ⚠️  No generator for {entity_type}")
            continue
        
        examples = generator(target_count)
        print(f"  Generated {len(examples)} examples")
        
        # Get relevant files
        pillars = ENTITY_PILLAR_MAPPING.get(entity_type, ['threat_intel', 'incident_response'])
        
        for pillar in pillars:
            pillar_dir = base_dir / pillar
            entity_file = pillar_dir / f"{pillar}_entities.jsonl"
            
            if entity_file.exists():
                added = add_examples_to_file(entity_file, examples, entity_type)
                total_added += added
            else:
                print(f"  ⚠️  File not found: {entity_file}")
        
        print()
    
    print("=" * 80)
    print(f"✅ COMPLETE: Added {total_added} total examples")
    print("=" * 80)

if __name__ == "__main__":
    main()

