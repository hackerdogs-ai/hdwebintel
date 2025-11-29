#!/usr/bin/env python3
"""
Generate realistic OSINT entities and intents.
Creates natural, domain-specific examples based on real OSINT operations.
"""

import json
import os
import re

OSINT_PILLARS = [
    "ai_int", "comint", "cybint", "darkint", "digint", "dnint", "domain_intel",
    "ecoint", "eduint", "finint", "geoint", "humint", "imint", "infint",
    "legint", "masint", "medint", "natint", "orbint", "sigint", "socmint",
    "techint", "threat_intel", "tradint", "vatint"
]

BASE_PATH = "cyber-train/entities-intent/osint"
OSINT_DEF_PATH = "cyber-train/osint"

# Realistic examples for each pillar based on actual OSINT operations
REALISTIC_EXAMPLES = {
    "socmint": {
        "entities": [
            "SOCMINT Analyst detected coordinated disinformation campaign #BreakingNews with 85% bot amplification score requiring immediate response",
            "Disinformation Researcher validated viral video using reverse image search on TinEye and Yandex Images confirming deepfake with 93% confidence",
            "Data Scientist mapped influence network graph showing 450 nodes and 1200 edges using Gephi visualization identifying bot cluster",
            "Digital Forensics Specialist flagged suspicious account @suspicious_user with bot score 0.92 requiring SOC team review",
            "Incident Responder generated real-time alert for brand impersonation campaign targeting AcmeCorp on Twitter and Facebook",
            "SOCMINT Analyst monitored hashtag #Election2025 detecting 1200 coordinated posts from bot cluster with 78% inauthentic behavior",
            "Using snscrape to collect Twitter data for hashtag analysis and sentiment scoring across 15 languages",
            "Sherlock username enumeration found @target_user across 15 platforms including Telegram Discord and Reddit",
            "Meltwater social listening detected 340 negative mentions requiring brand reputation response team escalation",
            "Brandwatch identified narrative shift in sentiment from 65% positive to 32% positive over 48 hours indicating coordinated attack",
            "OSINTgram Instagram mining extracted 2500 posts from target account showing suspicious activity patterns",
            "Hoaxy disinformation tracking detected viral misinformation spread across 8 platforms with 45000 shares",
            "Gephi network analysis revealed influence operation with 3 core influencers and 120 amplifier accounts",
            "Maltego CE relationship mapping connected 45 accounts to known threat actor group with 89% confidence",
            "CrowdTangle Facebook monitoring identified coordinated inauthentic behavior targeting election integrity",
            "Talkwalker multilingual sentiment analysis detected negative sentiment spike in German and French markets",
            "Dataminr real-time alerts flagged breaking event 2 hours before mainstream media coverage",
            "Graphika influence operation mapping identified Russian-linked campaign with AMITT framework tactics",
            "Tinfoleak Twitter forensic analysis extracted deleted tweets showing evidence of manipulation",
            "SocioSpyder large-scale topic analysis identified 5 emerging narratives requiring analyst attention",
        ],
        "intents": [
            "What's the bot score for account @suspicious_user?",
            "Can you verify if this viral video is a deepfake?",
            "Show me the influence network graph for hashtag #BreakingNews",
            "Are there any coordinated bot campaigns targeting our brand?",
            "What's the sentiment trend for our company over the last week?",
            "Can you check if this image was posted before using reverse image search?",
            "Who are the top influencers spreading this disinformation narrative?",
            "Is this account a sockpuppet or real user?",
            "What platforms is username @target_user active on?",
            "Generate a report on disinformation campaigns detected this month",
            "Monitor hashtag #Election2025 for coordinated inauthentic behavior",
            "Validate this viral media content for manipulation indicators",
            "Map the network connections for this influence operation",
            "Detect any bot clusters amplifying this narrative",
            "What's the narrative momentum index for this campaign?",
            "Flag any suspicious accounts posting about our brand",
            "Analyze sentiment trends across Twitter Facebook and Instagram",
            "Identify the source of this viral misinformation",
            "Track the spread of this disinformation across platforms",
            "Generate an attribution report for this coordinated campaign",
        ]
    },
    "threat_intel": {
        "entities": [
            "Threat Intel Analyst enriched IOC domain secure-login.net with WHOIS pDNS CT log and sandbox data",
            "Malware Researcher analyzed sample SHA256 abc123def456 identifying QakBot family with 95% confidence",
            "Dark Web Analyst found brand mention AcmeCorp in 5 forums with 12 credential dumps requiring immediate action",
            "CTI Analyst mapped campaign OperationShadow to MITRE ATT&CK techniques T1566 T1071 T1105",
            "Threat Intelligence Analyst published STIX feed with 2100 IOCs to OpenCTI MISP and Splunk platforms",
            "Malware Researcher generated YARA rule for Emotet variant detecting 87% of samples in wild",
            "Threat Hunter created hunting pack with Sigma rules for T1059 command execution technique",
            "IOC enrichment found related IPs 1.2.3.4 and 5.6.7.8 linked to C2 infrastructure",
            "Recorded Future threat feed identified 47 new domains associated with APT29 activity",
            "Flashpoint dark web monitoring detected ransomware leak site posting victim data",
            "MISP threat intelligence platform correlated 320 IOCs into 8 campaign clusters",
            "OpenCTI knowledge base updated with new threat actor profile for GroupX",
            "YARA signature matching detected 23 samples matching known malware family patterns",
            "Sigma detection rules identified 12 suspicious events in SIEM logs",
            "ThreatCrowd IOC analysis revealed 15 related domains and 8 IP addresses",
            "Anomali ThreatStream enriched domain with 92% risk score and actor attribution",
            "ThreatConnect platform mapped campaign to 5 threat actors with confidence scores",
            "IntSights threat intelligence identified new ransomware variant targeting healthcare",
            "VirusTotal API analysis confirmed malware sample with 45 antivirus detections",
            "Abuse.ch threat feed provided IOCs for ongoing phishing campaign",
        ],
        "intents": [
            "Enrich this IOC domain secure-login.net with all available data",
            "What malware family is this sample SHA256 abc123def456?",
            "Are there any mentions of our brand on dark web forums?",
            "Map this campaign to MITRE ATT&CK techniques",
            "What threat actors are using technique T1566 this quarter?",
            "Generate YARA rules for this malware sample",
            "What IOCs are associated with APT29?",
            "Is this domain part of a known phishing campaign?",
            "What's the attribution confidence for this attack?",
            "Create a hunting pack for ransomware indicators",
            "Ingest and normalize these IOCs from threat feeds",
            "Score these IOCs using ML and historical context",
            "Check which IOCs matched in our SIEM",
            "Update actor profiles with new TTPs and campaigns",
            "Correlate these IOCs into campaign clusters",
            "Generate threat landscape report for executives",
            "Produce ATT&CK-based hunt packs for SOC",
            "Tune detection rules based on false positive feedback",
            "What's the IOC coverage percentage for our feeds?",
            "Generate executive threat intelligence briefing",
        ]
    },
    "cybint": {
        "entities": [
            "Cyber Threat Analyst investigated phishing domain secure-login-apple.com with kit detection and infrastructure mapping",
            "Malware Reverse Engineer analyzed QakBot sample extracting C2 domains 8.8.8.8 and registry keys",
            "Threat Hunter tracked zero-day exploit CVE-2025-1111 with EPSS score 0.91 and KEV listing",
            "Vulnerability Intelligence Analyst prioritized CVE-2025-2222 based on exploit availability and CVSS score",
            "Cyber Intelligence Analyst correlated IOCs into campaign cluster with 7 related samples and 82% confidence",
            "Secret Exposure Analyst detected 15 exposed API keys on GitHub requiring immediate revocation",
            "Dark Web Analyst found credential leak CompanyX_Creds with 5000 records on BreachForums",
            "Threat Researcher identified LockBit ransomware group targeting healthcare sector with 5 new victims",
            "IOC feed ingestion processed 5400 indicators with 32% deduplication rate and 92% enrichment success",
            "Campaign tracking mapped OperationPhish to ATT&CK techniques with 82% attribution confidence",
            "OpenCTI platform enriched IOC with actor links to APT29 and risk score 0.92",
            "ATT&CK Navigator mapped incident to 12 techniques including T1566 T1071 T1105",
            "Cuckoo Sandbox analyzed malware sample showing HTTP beacon behavior and file exfiltration",
            "SpiderFoot automated OSINT correlation found 8 related domains and 3 IP addresses",
            "Recon-ng reconnaissance framework discovered 25 subdomains for target infrastructure",
            "CrowdStrike Falcon Intelligence provided adversary TTPs for threat actor profiling",
            "FireEye iSight threat intelligence identified APT group campaign targeting financial sector",
            "Palo Alto Unit 42 research linked malware to known threat actor with high confidence",
            "IBM X-Force Exchange enriched IOC with threat intelligence and reputation data",
            "Maltego relationship mapping connected domains IPs and certificates to infrastructure cluster",
        ],
        "intents": [
            "Investigate this phishing domain secure-login-apple.com",
            "What C2 infrastructure is this malware sample connecting to?",
            "Is CVE-2025-1111 being actively exploited in the wild?",
            "What's the EPSS score for this vulnerability?",
            "Are there any exposed API keys for our organization on GitHub?",
            "What ransomware group is behind this attack?",
            "Correlate these IOCs into campaign clusters",
            "What's the time-to-detect for credential leaks?",
            "Generate Sigma rules for this attack technique",
            "What's the false positive rate for our IOC feeds?",
            "Enrich this IOC with WHOIS pDNS and CT log data",
            "Analyze this malware sample and extract IOCs",
            "Track zero-day exploits and prioritize vulnerabilities",
            "Monitor dark web for brand mentions and leaks",
            "Map this incident to MITRE ATT&CK framework",
            "Generate hunting queries for threat actor TTPs",
            "Review IOC detection efficacy in SIEM",
            "Monitor supply chain for malicious packages",
            "Generate threat landscape report for executives",
            "Tune detection rules based on field feedback",
        ]
    },
    "darkint": {
        "entities": [
            "Dark Web Analyst validated leak CompanyX_Creds from BreachForums with 5000 records confirmed",
            "Crypto Intelligence Analyst traced wallet bc1qxyz123 finding 125 transactions through MixerX",
            "Threat Researcher investigated LockBit ransomware group activity identifying 5 new victims",
            "Dark Web Analyst compiled takedown package for brand impersonation acme-support.top domain",
            "Marketplace monitoring detected 230 new listings including 7 credential dumps and 3 exploit kits",
            "Leak site tracking found 15 new victims on ransomware leak sites with high-value targets",
            "Forum activity scan identified 12 keyword hits for brand AcmeCorp across 25 forums",
            "Credential reset pack generated 1743 accounts requiring password reset with admin VPN tags",
            "Actor reputation scoring updated 120 actors with 24 new alias links and scam probability",
            "Ransomware ecosystem report identified 2 new groups and 10 affiliates with T1486 T1566 techniques",
            "OnionScan dark web scanning discovered 8 new onion services hosting malicious content",
            "TorBot automated crawling found 3 marketplace listings selling stolen credentials",
            "Darkdump paste site monitoring detected leaked database with 12000 user records",
            "Ahmia search engine indexed 45 new dark web pages mentioning target keywords",
            "Hunchly investigation platform captured evidence from 12 dark web forums",
            "DarkOwl commercial platform detected brand mention in 8 underground forums",
            "IntSights threat intelligence identified ransomware leak site posting victim data",
            "Flashpoint deep web monitoring found exploit discussion targeting our infrastructure",
            "Recorded Future dark web intelligence provided actor profile for threat group",
            "KELA marketplace monitoring detected sale of access credentials for our systems",
        ],
        "intents": [
            "Validate this leak CompanyX_Creds from BreachForums",
            "Trace this crypto wallet bc1qxyz123 through the blockchain",
            "What ransomware groups have new victims this week?",
            "Compile a takedown package for this impersonation domain",
            "How many credential dumps mention our brand?",
            "What's the scam probability for this marketplace listing?",
            "Are there any VIP exposure risks we should know about?",
            "What's the success rate for our takedown requests?",
            "Screen these wallets against sanctions lists",
            "What's the market trend for exploit kits this month?",
            "Monitor marketplaces for credentials exploits and fraud goods",
            "Track ransomware leak sites for new victim postings",
            "Scan forums and Telegram for brand keyword mentions",
            "Generate credential reset packs from validated leaks",
            "Update actor reputation scores and alias linkages",
            "Analyze ransomware ecosystem trends and affiliate activity",
            "Trace crypto laundering paths for market and ransom wallets",
            "Fuse dark web indicators with other intelligence sources",
            "Generate market trends report for dark web commodities",
            "Compile brand exposure report with risk index",
        ]
    },
    "geoint": {
        "entities": [
            "GEOINT Analyst performed geolocation of photo identifying coordinates 36.45 37.12 with 91% confidence",
            "Satellite Imagery Specialist built facility baseline for Port Alpha showing 1.3 km2 footprint",
            "Remote Sensing Engineer produced damage assessment for Earthquake2025 with 78% damage index",
            "Maritime Analyst investigated dark voyage IMO1234567 with 8-hour AIS gap and ship-to-ship transfer",
            "Aviation Analyst detected suspicious flight path N123AB with hex spoofing and loitering behavior",
            "Sensor Tasking Coordinator ordered Planet Labs imagery for Port Bravo with 24-hour revisit rate",
            "Imagery Analyst monitored AOI detecting new construction activity requiring change detection",
            "Crisis Response Team generated rapid damage assessment heatmap for disaster zone",
            "Geospatial Analyst identified troop movement patterns using Sentinel-2 satellite imagery",
            "QGIS analysis revealed infrastructure changes at facility requiring further investigation",
            "SentinelSat satellite data processing identified illegal logging activity in protected area",
            "OpenStreetMap geospatial analysis mapped road network changes in conflict zone",
            "Google Earth Pro historical imagery comparison showed facility expansion over 6 months",
            "GeoServer map server generated interactive visualization for crisis response team",
            "Planet Labs daily satellite imagery detected new construction at military facility",
            "Maxar high-resolution imagery confirmed troop deployment in border region",
            "SkyWatch satellite tasking ordered imagery for disaster response coordination",
            "Esri ArcGIS geospatial analysis mapped infrastructure damage from natural disaster",
            "Hexagon Geospatial platform processed satellite data for change detection analysis",
            "Sentinel Hub API retrieved satellite imagery for AOI monitoring and analysis",
        ],
        "intents": [
            "Geolocate this photo to coordinates if possible",
            "What's the damage assessment for this disaster zone?",
            "Build a facility baseline for Port Alpha",
            "Are there any dark voyage segments for vessel IMO1234567?",
            "Detect suspicious flight paths for aircraft N123AB",
            "Order satellite imagery tasking for this AOI",
            "What infrastructure changes are visible in this imagery?",
            "Generate a change detection report for this facility",
            "What's the confidence score for this geolocation?",
            "Monitor this conflict zone for troop movements",
            "Perform ad-hoc geolocation with chronolocation if feasible",
            "Investigate maritime dark activity and AIS gaps",
            "Analyze suspicious aviation routes and transponder spoofing",
            "Monitor priority AOIs using daily satellite passes",
            "Generate facility baseline studies with annotated imagery",
            "Produce rapid post-event damage assessments",
            "Track vessel movements and detect anomalies",
            "Analyze satellite imagery for change detection",
            "Generate geospatial intelligence reports",
            "Coordinate sensor tasking for commercial imagery",
        ]
    },
    "humint": {
        "entities": [
            "HUMINT Researcher built actor dossier for InsiderX with 87% credibility score and GroupA affiliation",
            "OSINT Analyst validated HUMINT claim Factory shutdown using SOCMINT IMINT GEOINT correlation",
            "Cybercrime Investigator mapped network GroupZ with 45 nodes and 112 edges showing connections",
            "Insider Risk Analyst detected deception in HUMINT claim with 74% deception probability",
            "Fraud Investigator found insider leak hr_records.txt on Pastebin with 81% credibility",
            "Event Monitoring Specialist flagged TechConf2025 for suspicious recruitment activity",
            "Forum monitoring detected flagged posts on Telegram with high risk indicators",
            "Background Check Specialist verified identity using Maigret finding 8 platform matches",
            "GHunt Google account footprinting identified email address linked to 3 services",
            "Pipl deep web search found 12 public records matching target individual",
            "Maigret multi-platform lookup discovered username across 15 social media platforms",
            "Skiptracer people search enriched profile with employment history and contact information",
            "theHarvester email harvesting found 8 email addresses associated with target domain",
            "Recon-ng reconnaissance framework discovered social media profiles and public records",
            "OSINT-SPY profile analysis identified cross-platform presence and activity patterns",
            "IntelTechniques toolkit collected public records and social media intelligence",
            "Social Analyzer automated account discovery found 6 profiles across platforms",
            "SpiderFoot OSINT correlation linked identities to organizations and locations",
            "Maltego CE relationship mapping connected individuals to networks and groups",
            "Namechk username availability scan identified registered accounts across 20 platforms",
        ],
        "intents": [
            "Build an actor dossier for InsiderX",
            "Validate this HUMINT claim using cross-pillar correlation",
            "Map the network connections for GroupZ",
            "What's the deception probability for this claim?",
            "Are there any insider leaks mentioning our company?",
            "Monitor this conference for suspicious recruitment activity",
            "What platforms is this username active on?",
            "Find all public records for this individual",
            "What's the credibility score for this source?",
            "Generate a background check report",
            "Investigate suspected insider leaks on forums and paste sites",
            "Monitor public forums for insider chatter and activist planning",
            "Map HUMINT-based networks and produce network graphs",
            "Detect deception in HUMINT claims and identify manipulation",
            "Monitor open conferences and events for HUMINT signals",
            "Conduct background investigations and due diligence",
            "Resolve cross-platform aliases and usernames",
            "Assess insider risk and leak detection",
            "Profile threat actors through human intelligence",
            "Generate identity attribution reports",
        ]
    },
    "finint": {
        "entities": [
            "FININT Analyst checked entity XYZ Ltd against OFAC sanctions finding SDN match with 93% confidence",
            "Blockchain Tracer analyzed transaction 0x1234 finding darknet mixer links with 125000 USD value",
            "Beneficial Ownership Analyst investigated shell company XYZ Holdings in BVI jurisdiction",
            "TBML Investigator flagged trade transaction T12345 for over-invoicing with 2M USD value",
            "Adverse Media Analyst found 27 media hits for Acme FZE with PEP exposure requiring EDD",
            "Financial Disinfo Analyst validated annual report detecting metadata mismatch indicators",
            "Sanctions ingestion processed 35 new entries with 12 resolved matches in 2 hours",
            "Crypto alerts detected suspicious wallet activity with 1500 transactions totaling 12M USD",
            "Orbis corporate registry search identified beneficial owner John Doe for offshore entity",
            "World-Check screening found sanctions match requiring immediate compliance review",
            "OpenSanctions database search identified entity on OFAC SDN list",
            "BusinessRadar corporate intelligence found shell company structure with hidden ownership",
            "Aleph investigation platform mapped financial network with 8 related entities",
            "OpenCorporates registry search revealed beneficial ownership chain",
            "FEC.gov campaign finance data identified political contributions",
            "PitchBook financial database provided company ownership and investment data",
            "Dow Jones Risk screening detected sanctions and PEP matches",
            "LexisNexis Bridger Insight enriched entity with comprehensive risk data",
            "Sayari graph analysis mapped corporate relationships and ownership",
            "Diligence platform screened entity against sanctions and watchlists",
        ],
        "intents": [
            "Check if entity XYZ Ltd is on any sanctions lists",
            "Trace this crypto transaction 0x1234 through the blockchain",
            "Who is the beneficial owner of shell company XYZ Holdings?",
            "Flag this trade transaction for TBML risk",
            "What's the PEP exposure for this entity?",
            "Validate this financial document for authenticity",
            "What's the sanctions match rate for our screening?",
            "How much crypto value is linked to this wallet?",
            "What's the materiality score for this adverse media?",
            "Generate an AML compliance report",
            "Ingest and normalize sanctions list updates",
            "Monitor crypto transactions for suspicious activity",
            "Investigate shell companies and offshore structures",
            "Analyze trade transactions for money laundering indicators",
            "Screen entities for adverse media and PEP exposure",
            "Validate financial filings and corporate documents",
            "Generate financial intelligence reports",
            "Map beneficial ownership networks",
            "Track cryptocurrency flows and laundering paths",
            "Generate compliance and risk assessment reports",
        ]
    },
    "domain_intel": {
        "entities": [
            "Domain Threat Analyst investigated lookalike domain secure-login-apple.com with brand distance 0.92",
            "Infrastructure Analyst built attribution graph showing shared certificates and NS records",
            "Brand Abuse Lead compiled takedown package for phishing domain with registrar evidence",
            "DGA Campaign Sweep detected 47 candidate domains with seed analysis and clustering",
            "WHOIS monitoring detected registration changes for suspicious domain requiring review",
            "Certificate Transparency logs identified new SSL cert for malicious domain",
            "Subdomain discovery found 120 subdomains for target domain using Amass tool",
            "DNS enumeration revealed C2 infrastructure with 8 related domains and IPs",
            "DomainTools analysis showed domain age and registration history patterns",
            "SecurityTrails identified historical DNS records linking domains to threat actor",
            "Amass OSINT DNS mapping discovered 45 subdomains and related infrastructure",
            "Subfinder subdomain discovery found 23 previously unknown subdomains",
            "dnsx DNS resolution identified active domains and IP addresses",
            "dnstwist typosquat generation found 12 lookalike domains targeting brand",
            "ZMap internet scanning discovered 8 domains with suspicious certificates",
            "Sublist3r subdomain enumeration found 67 subdomains across multiple domains",
            "theHarvester domain discovery identified 15 domains associated with target",
            "DNSRecon DNS reconnaissance mapped DNS infrastructure and records",
            "Fierce DNS scanner discovered subdomains and related infrastructure",
            "WhoisXML API enriched domain with registration and ownership data",
        ],
        "intents": [
            "Investigate this lookalike domain secure-login-apple.com",
            "What infrastructure is this domain connected to?",
            "Compile a takedown package for this phishing domain",
            "Detect any DGA domains in this campaign",
            "What WHOIS changes occurred for this domain?",
            "Find all subdomains for this target domain",
            "What's the brand distance score for this domain?",
            "Map the certificate relationships for this infrastructure",
            "What's the registration history for this domain?",
            "Generate an IOC feed for malicious domains",
            "Perform rapid triage of suspicious FQDN",
            "Build infrastructure attribution graph",
            "Detect and list candidate DGA domains",
            "Monitor new domains and newly observed hosts",
            "Track WHOIS RDAP and CT log changes",
            "Generate domain cluster rollups and campaign graphs",
            "Evaluate DGA and fast-flux detection models",
            "Generate executive brief on domain threats",
            "Audit evidence packs and takedown processes",
            "Review vendor coverage and latency benchmarks",
        ]
    },
    "imint": {
        "entities": [
            "Forensic Analyst verified image authenticity using ExifTool detecting metadata manipulation",
            "Verification Specialist performed reverse image search finding original source on 3 platforms",
            "Imagery Scientist geolocated photo using terrain features and shadow analysis",
            "Deepfake Detector analyzed video with 93% confidence identifying AI-generated content",
            "Image Analyst extracted metadata showing GPS coordinates and camera model",
            "Media Forensics Expert validated viral video using InVID detecting deepfake synthesis",
            "Amped Authenticate tool confirmed image authenticity with 95% confidence score",
            "Clearview AI reverse image search found 12 matches across social media platforms",
            "ffmpeg video analysis extracted frames showing manipulation indicators",
            "OpenCV object detection identified vehicles and buildings in satellite imagery",
            "ExifTool metadata extraction revealed camera settings and GPS coordinates",
            "Image Analyzer detected image manipulation and editing artifacts",
            "InVID video verification platform identified deepfake and synthetic media",
            "Magnet Axiom forensic analysis extracted deleted images and metadata",
            "Adobe Photoshop analysis detected image editing and manipulation",
            "ShadowDragon image intelligence platform found matches across platforms",
            "Yandex Images reverse search identified original source and variations",
            "TinEye reverse image search found 8 matches with timestamps",
            "Google Images search identified similar images and sources",
            "Bing Visual Search found related images and reverse matches",
        ],
        "intents": [
            "Verify if this image is authentic or manipulated",
            "Perform reverse image search to find original source",
            "Geolocate this photo using terrain and shadow analysis",
            "Detect if this video is a deepfake",
            "Extract metadata from this image file",
            "Analyze this video for manipulation indicators",
            "Identify objects and locations in this imagery",
            "Compare this image with historical versions",
            "Validate this media content for authenticity",
            "Generate a forensics report for this image",
            "Detect deepfakes and AI-generated content",
            "Identify objects and locations in images",
            "Verify authenticity of viral media",
            "Geolocate photos and videos",
            "Analyze change over time in imagery",
            "Extract intelligence from images and videos",
            "Perform image forensics and metadata analysis",
            "Detect manipulation and editing artifacts",
            "Generate verification reports with confidence scores",
            "Map imagery to geographic locations",
        ]
    },
    "sigint": {
        "entities": [
            "SIGINT Analyst detected ADS-B spoofing for aircraft N123AB with hex code manipulation",
            "RF Data Engineer monitored AIS signals identifying dark voyage segments",
            "Spectrum Threat Hunter detected rogue Wi-Fi access point with IMSI catcher indicators",
            "Aviation Signal Specialist analyzed flight path anomalies showing loitering behavior",
            "Maritime Signal Analyst tracked vessel IMO1234567 with 8-hour AIS transmission gap",
            "GNU Radio SDR scanning detected unauthorized RF emissions in protected spectrum",
            "GQRX spectrum analyzer identified signal anomalies requiring further investigation",
            "Wireshark protocol analysis revealed suspicious network traffic patterns",
            "rtl_433 IoT monitoring detected SCADA device signals in unauthorized frequency",
            "Kismet Wi-Fi scanning found rogue access points with suspicious SSID patterns",
            "Zeek network analysis identified protocol anomalies and suspicious connections",
            "Snort IDS detected network intrusion attempts and malicious traffic",
            "Farsight DNSDB enriched signal data with DNS and network intelligence",
            "Palantir COMINT platform correlated signals with other intelligence sources",
            "SignalGuard maritime monitoring detected vessel tracking anomalies",
            "HawkEye 360 RF geolocation identified signal sources from space",
            "Thales RESOLVE signal analysis platform processed RF data",
            "Keysight Signal Analyzer detected spectrum violations and interference",
            "Rohde & Schwarz PR200 signal monitoring identified unauthorized transmissions",
            "CRFS RFeye spectrum monitoring detected signal anomalies",
        ],
        "intents": [
            "Detect ADS-B spoofing for aircraft tracking",
            "Monitor AIS signals for dark voyage segments",
            "Identify rogue Wi-Fi access points and IMSI catchers",
            "Analyze flight path anomalies and suspicious routes",
            "Track vessel movements with AIS monitoring",
            "Scan spectrum for unauthorized RF emissions",
            "Detect signal anomalies and interference",
            "Analyze network traffic for suspicious patterns",
            "Monitor IoT and SCADA device signals",
            "Identify Wi-Fi and Bluetooth security threats",
            "Continuous SDR spectrum scanning for anomalies",
            "Compile weekly SIGINT anomaly summaries",
            "Generate signal environment baselines by AOI",
            "Correlate SIGINT anomalies with other intelligence",
            "Update adversary TTP mapping for signal spoofing",
            "Conduct red-team SIGINT spoofing drills",
            "Generate executive SIGINT threat briefings",
            "Audit signal metadata retention for compliance",
            "Refresh SIGINT strategy and vendor evaluation",
            "Participate in national security exercises",
        ]
    },
    "comint": {
        "entities": [
            "COMINT Collection Officer investigated VoIP fraud case voip_2025_001 detecting 45 fraudulent calls",
            "Voice Analyst analyzed radio chatter in Arabic identifying coded language and operation keywords",
            "Network Telephony Analyst detected satcom signal anomaly satcom_008 with jamming indicators",
            "Spectrum Analyst validated emergency broadcast alert_101 detecting spoofing with 88% confidence",
            "Communications Specialist detected voice cloning in VoIP recording vc_2025_001 with 91% confidence",
            "Radio Analyst built call graph for fraud cluster analyzing STIR SHAKEN anomalies",
            "rtl_433 signal monitoring detected IoT device communications in unauthorized bands",
            "GNU Radio SDR processing identified suspicious radio transmissions",
            "SDR# software defined radio captured HF VHF signals for analysis",
            "OpenWebRX web-based SDR detected unauthorized communications",
            "SigDigger signal analysis tool identified modulation anomalies",
            "Palantir COMINT platform correlated communications with threat intelligence",
            "SignalGuard monitoring detected telephony fraud patterns",
            "Krypto500 encryption analysis identified weak cipher usage",
            "Rohde & Schwarz CA100 signal analyzer processed RF data",
            "TCI Model 9038 monitoring detected spectrum violations",
            "SDRuno software identified signal anomalies",
            "HDSDR spectrum analysis revealed unauthorized transmissions",
            "Voice language analyst transcribed intercepted communications",
            "Telephony intelligence analyst mapped call patterns and attribution",
        ],
        "intents": [
            "Investigate suspected VoIP fraud or vishing campaigns",
            "Analyze intercepted radio chatter for coded language",
            "Check for anomalous satcom transmissions",
            "Validate suspected manipulation of emergency broadcasts",
            "Detect voice cloning or synthetic audio in recordings",
            "Build telephony call graph for fraud cluster",
            "Monitor unsecured VoIP radio and push-to-talk communications",
            "Detect fraudulent call campaigns and robocalls",
            "Identify interceptable open radio chatter",
            "Collect public satcom signals and distress communications",
            "Capture emergency services leaks and non-encrypted chatter",
            "Detect pirate radio stations used for propaganda",
            "Identify covert communications in ham radio bands",
            "Track VoIP abuse for command-and-control operations",
            "Monitor emergency broadcasts for disinformation",
            "Detect espionage tradecraft using amateur comms",
            "Analyze communication patterns and anomalies",
            "Generate communications intelligence reports",
            "Map call metadata and carrier paths",
            "Validate STIR SHAKEN authentication anomalies",
        ]
    },
    "digint": {
        "entities": [
            "IoT Analyst detected mobile app telemetry leakage exposing user device patterns",
            "Forensic Team Member extracted IoT wearables exhaust from BLE Wi-Fi signals",
            "Mobile Security Analyst identified web app tracking chains with cookie syncs",
            "Digital Forensics Specialist found enterprise app misconfig exposing debug endpoints",
            "Digital Intelligence Analyst detected AdTech correlation enabling deanonymization",
            "Mobile Forensics Analyst identified supply-chain SDK risk with trojaned libraries",
            "MITMproxy interception captured mobile app traffic revealing sensitive data",
            "MobSF mobile security framework analyzed app for vulnerabilities",
            "Frida dynamic instrumentation detected app behavior and API calls",
            "Burp Suite Community analyzed web app traffic and API endpoints",
            "Wireshark network analysis captured IoT device communications",
            "Cellebrite mobile forensics extracted data from device",
            "Grayshift device extraction recovered app data and metadata",
            "Oxygen Forensics analyzed mobile device for intelligence",
            "Magnet Forensics extracted digital evidence from devices",
            "Paraben E3 forensic platform processed mobile and IoT data",
            "Autopsy digital forensics analyzed device images",
            "Volatility memory analysis extracted runtime data",
            "IoT telemetry analysis identified device fingerprints",
            "Digital exhaust monitoring detected metadata leakage",
        ],
        "intents": [
            "Detect mobile app telemetry leakage and SDK beacons",
            "Extract IoT wearables exhaust from BLE and Wi-Fi",
            "Analyze web app tracking chains and cookie syncs",
            "Find enterprise app misconfigurations and debug endpoints",
            "Detect AdTech correlation and attribution networks",
            "Identify supply-chain SDK risks and trojaned libraries",
            "Monitor network telemetry for misuse",
            "Track location exhaust from apps and SDKs",
            "Analyze automotive telematics and OBD dongles",
            "Detect cross-pillar fusion risks",
            "Capture client network and backend communications",
            "Analyze protocols HTTP gRPC WebSocket QUIC MQTT",
            "Build attribution graph for apps SDKs and endpoints",
            "Use ML-assisted discovery for endpoint clustering",
            "Perform pre-prod privacy tests and post-prod monitoring",
            "Extract intelligence from digital exhaust",
            "Analyze app metadata and device fingerprints",
            "Monitor digital footprints and forensic investigations",
            "Detect device intelligence and mobile forensics",
            "Generate digital intelligence reports",
        ]
    },
    "dnint": {
        "entities": [
            "DNINT Analyst investigated suspicious domain malicious-example.com for hijacking and sinkholes",
            "BGP Specialist analyzed BGP hijack event AS98765 affecting prefix 192.0.2.0/24",
            "Internet Researcher mapped botnet ExampleBot with 54 nodes and C2 IPs",
            "Network Topology Analyst verified TLS certificate for secure-bank.com detecting rogue CA",
            "Digital Network Analyst investigated fast-flux domain flux-domain.com with 88% confidence",
            "Network Security Analyst generated sinkhole recommendations for botnet domains",
            "BGPStream monitoring detected routing anomalies and hijack events",
            "RIPEstat BGP analysis identified ASN mismatches",
            "CAIDA internet research mapped network topology",
            "PeeringDB database queried for ASN relationships",
            "OpenINTEL passive DNS provided historical DNS records",
            "Kentik network intelligence analyzed traffic patterns",
            "ThousandEyes network monitoring detected outages",
            "Arbor Networks DDoS protection identified attacks",
            "Cisco ThousandEyes mapped network paths",
            "Nokia Deepfield analyzed network infrastructure",
            "RouteViews BGP data identified routing changes",
            "RIPE RIS routing information service provided data",
            "Wireshark protocol analysis revealed network anomalies",
            "Zeek network analysis identified suspicious connections",
        ],
        "intents": [
            "Investigate suspicious domains for hijacking and sinkholes",
            "Analyze suspected BGP hijack events and origin-AS mismatches",
            "Investigate emerging botnet clusters and generate infrastructure graphs",
            "Verify suspicious TLS certificate issuance and detect rogue CAs",
            "Investigate fast-flux domains for adversarial hosting",
            "Generate sinkhole recommendations for botnet domains",
            "Detect C2 and infrastructure tracking",
            "Identify DNS and domain hijacking attempts",
            "Monitor BGP hijack and malicious rerouting",
            "Track TLS PKI intelligence and fraudulent certificates",
            "Correlate traffic metadata for hidden relationships",
            "Discover botnet P2P and centralized infrastructures",
            "Map network attack surfaces and exploitable services",
            "Feed insights to THREAT_INTEL CYBINT and DOMAIN_INTEL",
            "Monitor DNS manipulations and routing anomalies",
            "Detect DNS poisoning typosquatting and sinkhole attempts",
            "Identify traffic interception and malicious rerouting",
            "Track fraudulent certificate issuance",
            "Map network infrastructure and relationships",
            "Generate network intelligence reports",
        ]
    },
    "ecoint": {
        "entities": [
            "Trade Analyst analyzed sanctions impact on trade flows identifying 15% reduction",
            "Supply Chain Researcher tracked resource dependencies for critical minerals",
            "Economist identified trade pattern anomalies in import export data",
            "Market Analyst assessed economic risks from geopolitical tensions",
            "Economic Intelligence Analyst detected supply chain vulnerabilities in semiconductor sector",
            "Trade Intelligence Analyst monitored trade flows using UN Comtrade API",
            "TradeMapAPI provided trade statistics and flow analysis",
            "OpenTradeStats database queried for import export data",
            "World Bank Data analyzed economic indicators",
            "IMF Data provided financial and trade statistics",
            "UN Comtrade API retrieved trade flow information",
            "Refinitiv platform analyzed economic trends",
            "Bloomberg Terminal provided market intelligence",
            "S&P Global Market Intelligence analyzed trade patterns",
            "IHS Markit research identified economic risks",
            "Fitch Solutions assessed economic forecasts",
            "Trading Economics provided economic indicators",
            "OECD Stats database analyzed trade statistics",
            "Economic forecasting identified supply chain risks",
            "Trade pattern analysis detected anomalies",
        ],
        "intents": [
            "Analyze sanctions impact on trade flows",
            "Track resource dependencies for critical materials",
            "Monitor trade patterns for anomalies",
            "Assess economic risks from geopolitical events",
            "Identify supply chain vulnerabilities",
            "Monitor economic trends and indicators",
            "Analyze trade flows and import export data",
            "Track resource dependencies and strategic materials",
            "Detect trade anomalies and violations",
            "Assess economic risks and forecasts",
            "Monitor supply chain vulnerabilities",
            "Analyze market trends and patterns",
            "Generate economic intelligence reports",
            "Track commodity prices and flows",
            "Monitor trade disruptions and embargoes",
            "Assess economic warfare indicators",
            "Identify critical dependencies",
            "Analyze trade intelligence data",
            "Generate economic risk assessments",
            "Monitor global trade patterns",
        ]
    },
    "eduint": {
        "entities": [
            "Academic Intelligence Analyst identified emerging technology in research publications",
            "Research Analyst detected foreign influence in academic research labs",
            "Talent Tracker mapped academic collaborations across 12 universities",
            "Technology Intelligence Specialist tracked talent migration patterns",
            "Educational Intelligence Analyst monitored campus activism and protests",
            "Research Intelligence Analyst analyzed preprint publications on arXiv",
            "OpenAlex database searched for research publications",
            "Semantic Scholar API retrieved academic paper data",
            "arXiv API accessed preprint publications",
            "PubMed database queried for medical research",
            "ORCID researcher profiles identified academic networks",
            "Elsevier Scopus analyzed research output",
            "Web of Science indexed academic publications",
            "Dimensions.ai research platform analyzed collaborations",
            "Quid Pro research intelligence identified trends",
            "LexisNexis Academic database searched publications",
            "Research analysis identified emerging technologies",
            "Academic collaboration mapping revealed networks",
            "Talent migration tracking identified movements",
            "Campus activism monitoring detected activities",
        ],
        "intents": [
            "Identify emerging technologies in research publications",
            "Detect foreign influence in academic research",
            "Map academic collaborations and networks",
            "Track talent migration and researcher movements",
            "Monitor campus activism and protests",
            "Analyze research output and publications",
            "Track academic research trends",
            "Identify research espionage indicators",
            "Map academic collaboration networks",
            "Monitor talent migration patterns",
            "Detect campus activism and protests",
            "Analyze research intelligence data",
            "Generate academic intelligence reports",
            "Track technology emergence in research",
            "Monitor research lab activities",
            "Identify academic collaboration patterns",
            "Assess research security risks",
            "Generate educational intelligence reports",
            "Track academic research trends",
            "Monitor educational sector intelligence",
        ]
    },
    "infint": {
        "entities": [
            "Fact-checker debunked fake news article with 95% confidence using source verification",
            "Disinformation Researcher analyzed narrative spread across 8 platforms",
            "Verification Specialist detected bot network with 450 accounts amplifying misinformation",
            "Narrative Analyst tracked disinformation campaign OperationEcho with AMITT tactics",
            "Information Environment Analyst verified information authenticity using cross-source validation",
            "Verification Analyst identified falsehood in viral claim requiring correction",
            "InVID video verification platform analyzed media content",
            "Hoaxy disinformation tracking mapped spread patterns",
            "Botometer bot detection identified inauthentic accounts",
            "NewsGuard credibility scoring rated source reliability",
            "Graphika network mapping identified influence operations",
            "Logically fact-checking platform verified claims",
            "Cyabra bot detection identified coordinated behavior",
            "Yonder narrative analysis tracked information campaigns",
            "FactCheck.org verified claim accuracy",
            "PolitiFact fact-checking rated statement truthfulness",
            "Fake news debunking identified falsehoods",
            "Narrative analysis tracked information spread",
            "Bot network detection identified coordinated accounts",
            "Information verification validated authenticity",
        ],
        "intents": [
            "Debunk this fake news article",
            "Analyze the narrative spread for this disinformation",
            "Detect bot networks amplifying this information",
            "Track this disinformation campaign",
            "Verify the authenticity of this information",
            "Fact-check this viral claim",
            "Identify the source of this misinformation",
            "Map the network spreading this narrative",
            "Detect coordinated inauthentic behavior",
            "Generate verification report for this content",
            "Analyze information environment and narratives",
            "Detect bot networks and coordinated accounts",
            "Track disinformation campaigns",
            "Verify information authenticity",
            "Debunk fake news and falsehoods",
            "Analyze narrative trends and spread",
            "Identify information warfare indicators",
            "Generate fact-checking reports",
            "Monitor information environment",
            "Detect misinformation and disinformation",
        ]
    },
    "legint": {
        "entities": [
            "Legal Researcher provided litigation support for case LAW-2025-123",
            "Compliance Analyst conducted compliance audit identifying 3 regulatory gaps",
            "Paralegal tracked regulatory changes affecting industry standards",
            "Litigation Support Specialist monitored legal proceedings in federal court",
            "Legal Intelligence Analyst identified legal risks requiring counsel review",
            "Legal Analyst researched case law for precedent analysis",
            "CaseLawAccess database searched for relevant cases",
            "CourtListener platform monitored court filings",
            "RECAP database accessed federal court records",
            "Justia legal database searched for case law",
            "OpenJurist platform analyzed legal documents",
            "LexisNexis legal research provided case analysis",
            "Westlaw database searched for legal precedents",
            "Bloomberg Law analyzed regulatory changes",
            "Fastcase legal research identified relevant cases",
            "Casetext AI legal research analyzed documents",
            "PACER federal court records accessed",
            "Justia Dockets monitored case filings",
            "Legal document analysis identified risks",
            "Regulatory intelligence tracked changes",
        ],
        "intents": [
            "Provide litigation support for this case",
            "Conduct compliance audit for regulatory requirements",
            "Track regulatory changes affecting our industry",
            "Monitor legal proceedings in relevant courts",
            "Identify legal risks requiring review",
            "Research case law for precedent analysis",
            "Generate compliance reports",
            "Monitor legal proceedings and filings",
            "Track regulatory changes and updates",
            "Identify legal risks and exposures",
            "Research legal documents and cases",
            "Analyze regulatory compliance",
            "Generate legal intelligence reports",
            "Monitor litigation and legal proceedings",
            "Track compliance requirements",
            "Identify regulatory changes",
            "Research legal precedents",
            "Generate legal risk assessments",
            "Monitor legal environment",
            "Track legal and regulatory intelligence",
        ]
    },
    "masint": {
        "entities": [
            "MASINT Engineer detected nuclear test signature with 92% confidence",
            "Seismologist monitored seismic activity identifying earthquake patterns",
            "Acoustic Analyst analyzed acoustic signatures for anomaly detection",
            "Nuclear Detection Specialist identified nuclear test indicators",
            "Measurement Analyst tracked geological changes using seismic data",
            "Signature Analyst detected environmental anomalies in measurement data",
            "Seiscomp3 seismic monitoring detected earthquake events",
            "GNU Radio signal processing analyzed measurement data",
            "ObsPy seismic analysis identified earthquake patterns",
            "Pyrocko seismic processing detected events",
            "MSNoise seismic monitoring analyzed data",
            "Janes MASINT platform provided measurement intelligence",
            "Hexagon Geospatial analyzed measurement signatures",
            "Geospiza measurement analysis identified anomalies",
            "SeismicAI platform detected seismic events",
            "BlackSky measurement intelligence analyzed data",
            "IRIS seismic network provided data",
            "USGS earthquake data analyzed patterns",
            "Nuclear test detection identified signatures",
            "Seismic monitoring tracked activity",
        ],
        "intents": [
            "Detect nuclear test signatures and indicators",
            "Monitor seismic activity for earthquake patterns",
            "Analyze acoustic signatures for anomalies",
            "Track geological changes and environmental data",
            "Identify measurement anomalies",
            "Detect signature intelligence indicators",
            "Monitor seismic events and activity",
            "Analyze measurement and signature data",
            "Detect nuclear test indicators",
            "Track environmental anomalies",
            "Generate measurement intelligence reports",
            "Monitor seismic monitoring networks",
            "Analyze acoustic signature data",
            "Detect measurement anomalies",
            "Track geological changes",
            "Identify signature intelligence patterns",
            "Generate MASINT analysis reports",
            "Monitor measurement and signature intelligence",
            "Detect nuclear and seismic events",
            "Analyze measurement intelligence data",
        ]
    },
    "medint": {
        "entities": [
            "Epidemiologist monitored pandemic indicators detecting early outbreak signals",
            "Health Intel Analyst detected disease spread patterns across 5 countries",
            "Public Health Researcher analyzed health trends identifying risk factors",
            "Outbreak Investigator tracked disease transmission with 89% confidence",
            "Medical Intelligence Analyst monitored health crisis requiring response",
            "Health Intelligence Analyst analyzed epidemiological data",
            "WHO Epidata database accessed for outbreak information",
            "EpiJSON format provided epidemiological data",
            "HealthMap platform monitored disease spread",
            "ProMED-mail early warning system detected outbreaks",
            "BioCaster disease surveillance identified patterns",
            "BlueDot outbreak detection provided alerts",
            "HealthMap monitoring tracked disease spread",
            "Metabiota epidemiological analysis identified risks",
            "EIOS epidemic intelligence analyzed data",
            "GIDEON medical database provided information",
            "CDC Data accessed for health statistics",
            "Johns Hopkins tracking provided pandemic data",
            "Pandemic monitoring detected early signals",
            "Outbreak detection identified disease spread",
        ],
        "intents": [
            "Monitor pandemic indicators and early outbreak signals",
            "Detect disease spread patterns across regions",
            "Analyze health trends and risk factors",
            "Track disease transmission and outbreaks",
            "Monitor health crisis requiring response",
            "Analyze epidemiological data and patterns",
            "Detect early outbreak signals",
            "Track disease spread and transmission",
            "Monitor health trends and indicators",
            "Generate health intelligence reports",
            "Analyze public health intelligence",
            "Detect disease surveillance patterns",
            "Monitor epidemiological trends",
            "Track outbreak intelligence",
            "Generate medical intelligence reports",
            "Monitor public health indicators",
            "Detect disease spread early",
            "Analyze health crisis data",
            "Track pandemic preparedness",
            "Generate health intelligence assessments",
        ]
    },
    "natint": {
        "entities": [
            "Resource Analyst anticipated resource conflict in water-scarce region",
            "Geospatial Specialist mapped strategic dependencies for rare earth minerals",
            "Commodity Researcher detected illegal exploitation of protected resources",
            "Environmental Analyst monitored climate-driven scarcity indicators",
            "Natural Resources Analyst supported supply chain decisions with intelligence",
            "Resource Intelligence Analyst tracked commodity prices and availability",
            "FAOSTAT database accessed for agricultural data",
            "UN Comtrade provided trade statistics for resources",
            "World Bank Open Data analyzed resource availability",
            "USGS Earth Explorer accessed geological data",
            "Global Forest Watch monitored deforestation",
            "Palantir Foundry analyzed resource intelligence",
            "Bloomberg Terminal provided commodity prices",
            "Refinitiv Eikon analyzed resource markets",
            "Wood Mackenzie energy research provided data",
            "S&P Global Market Intelligence analyzed resources",
            "EIA energy data accessed statistics",
            "IEA energy analysis provided intelligence",
            "Resource monitoring tracked availability",
            "Commodity analysis identified trends",
        ],
        "intents": [
            "Anticipate resource conflicts in water-scarce regions",
            "Map strategic dependencies for critical resources",
            "Detect illegal exploitation of protected resources",
            "Monitor climate-driven scarcity indicators",
            "Support supply chain decisions with intelligence",
            "Track commodity prices and availability",
            "Analyze resource dependencies",
            "Monitor resource availability and trends",
            "Detect illegal resource exploitation",
            "Assess climate impact on resources",
            "Generate resource intelligence reports",
            "Track commodity markets and prices",
            "Monitor environmental degradation",
            "Analyze resource supply chains",
            "Detect resource conflict indicators",
            "Generate natural resources intelligence",
            "Monitor resource markets",
            "Track commodity intelligence",
            "Analyze resource risks",
            "Generate resource assessments",
        ]
    },
    "orbint": {
        "entities": [
            "Remote Sensing Analyst tracked satellite movements identifying orbital changes",
            "Orbital Mechanics Specialist monitored orbital debris detecting collision risks",
            "Satellite Tracking Analyst detected space events requiring attention",
            "Space Situational Awareness Officer identified space threats",
            "Orbital Intelligence Analyst analyzed satellite intelligence data",
            "Satellite Analyst tracked satellite positions and orbits",
            "STK Free satellite toolkit calculated orbital parameters",
            "Skyfield astronomy library predicted satellite positions",
            "Heavens-Above satellite tracking provided predictions",
            "CelesTrak orbital data accessed satellite information",
            "SatNOGS network tracked satellite signals",
            "LeoLabs space tracking monitored satellites",
            "Spire Global satellite data provided intelligence",
            "Planet Labs satellite imagery analyzed orbits",
            "Maxar satellite tracking provided data",
            "NorthStar Earth & Space monitored orbital activity",
            "Space-Track database accessed satellite information",
            "GPredict satellite tracking predicted positions",
            "Orbital analysis identified changes",
            "Satellite intelligence tracked movements",
        ],
        "intents": [
            "Track satellite movements and orbital changes",
            "Monitor orbital debris for collision risks",
            "Detect space events requiring attention",
            "Identify space threats and anomalies",
            "Analyze satellite intelligence data",
            "Track satellite positions and orbits",
            "Monitor space situational awareness",
            "Detect orbital anomalies",
            "Track satellite intelligence",
            "Generate orbital intelligence reports",
            "Monitor satellite movements",
            "Track orbital debris",
            "Detect space events",
            "Analyze orbital mechanics",
            "Generate space intelligence",
            "Monitor space threats",
            "Track satellite tracking data",
            "Analyze orbital intelligence",
            "Detect space anomalies",
            "Generate space situational awareness reports",
        ]
    },
    "techint": {
        "entities": [
            "TechINT Analyst investigated exploit CVE-2025-XXXX with CVSS 9.8 and EPSS 0.91",
            "Reverse Engineer analyzed malware binary SHA256 identifying Emotet family",
            "Exploit Developer validated PoC for vulnerability requiring mitigation",
            "Security Researcher detected supply chain alert for package leftpadx",
            "Vulnerability Analyst investigated ICS exposure finding 42 nodes",
            "Technical Analyst analyzed firmware image detecting hardcoded credentials",
            "Nmap network scanning identified open ports and services",
            "WhatWeb web technology detection identified CMS versions",
            "Wappalyzer technology fingerprinting detected frameworks",
            "Metasploit exploit framework tested vulnerabilities",
            "Nessus vulnerability scanner identified security issues",
            "Qualys vulnerability management assessed risks",
            "Rapid7 Nexpose scanned for vulnerabilities",
            "Tenable.io platform analyzed security posture",
            "ImmuniWeb security testing identified issues",
            "Acunetix web vulnerability scanner detected flaws",
            "Burp Suite web security testing analyzed applications",
            "OWASP ZAP security testing identified vulnerabilities",
            "Vulnerability research identified exploits",
            "Technical intelligence analyzed artifacts",
        ],
        "intents": [
            "Investigate this newly reported CVE and exploit",
            "Reverse engineer this malware binary",
            "Validate PoC for this vulnerability",
            "Investigate suspected malicious package",
            "Check ICS IoT exposure and enumerate devices",
            "Analyze firmware image for vulnerabilities",
            "Conduct vulnerability research",
            "Detect exploits and security issues",
            "Fingerprint technologies and frameworks",
            "Map attack surfaces and misconfigurations",
            "Identify penetration testing opportunities",
            "Conduct security assessments",
            "Generate technical intelligence reports",
            "Analyze software and infrastructure artifacts",
            "Detect exploit development indicators",
            "Assess vulnerability risks",
            "Generate technical analysis reports",
            "Monitor exploit development",
            "Track vulnerability trends",
            "Analyze technical intelligence",
        ]
    },
    "tradint": {
        "entities": [
            "Trade Analyst investigated sanctions evasion case for entity XYZ Ltd",
            "Market Researcher traced dual-use goods export for chips and drones",
            "Supply Chain Analyst investigated counterfeit goods shipment ID12345",
            "Customs Intelligence Officer analyzed transshipment route through third countries",
            "Trade Intelligence Analyst mapped import export flows detecting anomalies",
            "Supply Chain Intelligence Analyst identified trade pattern violations",
            "UN Comtrade API retrieved trade flow data",
            "OpenCorporates registry searched for company information",
            "Panjiva trade data analyzed shipments",
            "ImportGenius database queried for import data",
            "TradeAtlas platform analyzed trade flows",
            "Descartes Datamyne trade intelligence provided data",
            "PIERS trade database accessed information",
            "Kuehne + Nagel trade data analyzed flows",
            "Trade Data Monitor tracked shipments",
            "Global Trade Atlas analyzed trade patterns",
            "Sanctions evasion detection identified violations",
            "Trade flow analysis detected anomalies",
            "Supply chain mapping identified routes",
            "Trade intelligence tracked patterns",
        ],
        "intents": [
            "Investigate suspected sanctions evasion involving shipment",
            "Trace dual-use goods exports like chips and drones",
            "Investigate suspected counterfeit or illegal shipments",
            "Analyze transshipment routes through third countries",
            "Map import export flows and detect anomalies",
            "Detect sanctions violations in trade",
            "Track supply chains and trade routes",
            "Identify trade anomalies and violations",
            "Monitor trade patterns and flows",
            "Generate trade intelligence reports",
            "Analyze trade flows and shipments",
            "Detect sanctions evasion attempts",
            "Track supply chain intelligence",
            "Monitor trade compliance",
            "Generate customs intelligence",
            "Analyze trade pattern anomalies",
            "Detect trade violations",
            "Track import export intelligence",
            "Monitor supply chain risks",
            "Generate trade assessment reports",
        ]
    },
    "vatint": {
        "entities": [
            "Transportation OSINT Analyst tracked ADS-B plane N123AB detecting suspicious route",
            "Aviation Specialist monitored flight path identifying loitering behavior",
            "Maritime Analyst tracked AIS vessel IMO1234567 with dark voyage segments",
            "Customs Enforcement Officer identified suspicious routes requiring investigation",
            "Vehicle Tracking Analyst monitored transportation security threats",
            "Transportation Intelligence Analyst analyzed vehicle aircraft and ship movements",
            "adsbSnoop ADS-B monitoring detected aircraft signals",
            "AIS-catcher maritime tracking monitored vessel movements",
            "OpenSky Network provided aircraft tracking data",
            "FlightAware platform tracked flight paths",
            "MarineTraffic vessel tracking monitored ships",
            "FlightRadar24 aircraft tracking provided data",
            "VesselFinder maritime intelligence tracked vessels",
            "PlaneFinder aircraft tracking monitored flights",
            "ShipFinder vessel tracking provided intelligence",
            "VesselTracker maritime monitoring tracked ships",
            "Aircraft tracking identified suspicious routes",
            "Vessel monitoring detected anomalies",
            "Transportation security analyzed movements",
            "Vehicle intelligence tracked activities",
        ],
        "intents": [
            "Track ADS-B planes for suspicious routes",
            "Monitor AIS vessel movements for anomalies",
            "Identify suspicious transportation routes",
            "Support customs enforcement with intelligence",
            "Enable transportation security monitoring",
            "Track aircraft movements and routes",
            "Monitor vessel movements and voyages",
            "Detect suspicious transportation patterns",
            "Generate transportation intelligence",
            "Analyze vehicle aircraft and ship tracking",
            "Monitor ADS-B and AIS signals",
            "Track flight paths and routes",
            "Monitor maritime vessel movements",
            "Detect transportation anomalies",
            "Generate transportation security reports",
            "Track vehicle movements",
            "Monitor aircraft and vessel intelligence",
            "Analyze transportation patterns",
            "Detect suspicious routes",
            "Generate transportation intelligence reports",
        ]
    },
    "ai_int": {
        "entities": [
            "AI Threat Analyst monitored AI misuse across OSINT dark web and GitHub",
            "Synthetic Media Investigator detected deepfakes using DeepFaceLab with 93% confidence",
            "Adversarial ML Researcher tested AI ML pipelines for poisoning and evasion",
            "Prompt Security Engineer detected prompt injection attempts on LLM systems",
            "AI Intelligence Analyst ensured compliance with EU AI Act and NIST AI RMF",
            "ML Security Analyst tracked AI model dataset and API sales on dark web",
            "HuggingFace Models platform analyzed AI model performance",
            "DetectGPT tool identified AI-generated text content",
            "OpenAI API moderation detected malicious usage",
            "TensorFlow framework analyzed model behavior",
            "PyTorch platform processed AI models",
            "Fiddler AI model monitoring analyzed performance",
            "TruEra AI explainability provided insights",
            "OpenAI moderation detected policy violations",
            "IBM Watson AI platform analyzed threats",
            "Google AI tools detected misuse",
            "DeepFaceLab synthetic media detection analyzed content",
            "FakeCatcher deepfake detection identified synthetic media",
            "AI model analysis detected threats",
            "Synthetic media monitoring identified deepfakes",
        ],
        "intents": [
            "Monitor AI misuse across OSINT and dark web",
            "Detect deepfakes and AI-generated media",
            "Test AI ML pipelines for poisoning attacks",
            "Detect prompt injection and malicious LLM usage",
            "Ensure compliance with EU AI Act and NIST RMF",
            "Track AI model dataset and API sales",
            "Detect AI-generated personas across platforms",
            "Analyze deepfake content using detection tools",
            "Identify synthetic videos with real-time detection",
            "Scan media files for deepfake indicators",
            "Map narrative networks with AI detection",
            "Monitor dark web AI intelligence feeds",
            "Enable AI entity resolution",
            "Identify threats with adversarial AI detection",
            "Detect botnets and disinformation with AI",
            "Map AI-driven influence operations",
            "Analyze text content with semantic intelligence",
            "Detect child exploitation content with AI",
            "Enable AI detection and moderation",
            "Evaluate LLM models with adversarial testing",
        ]
    }
}

def find_entities(text, pillar):
    """Find entity spans in text."""
    entities = []
    text_lower = text.lower()
    
    # Domain patterns
    for match in re.finditer(r'\b([a-z0-9-]+\.(com|net|org|io|co|gov|edu|ru|cn|de|uk|jp))\b', text, re.IGNORECASE):
        entities.append([match.start(), match.end(), "DOMAIN"])
    
    # IP addresses
    for match in re.finditer(r'\b([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\b', text):
        entities.append([match.start(), match.end(), "IP_ADDRESS"])
    
    # Hashes
    for match in re.finditer(r'\b([a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64})\b', text, re.IGNORECASE):
        entities.append([match.start(), match.end(), "HASH"])
    
    # CVEs
    for match in re.finditer(r'\b(CVE-\d{4}-\d{4,7})\b', text):
        entities.append([match.start(), match.end(), "CVE"])
    
    # ATT&CK techniques
    for match in re.finditer(r'\b(T\d{4}(\.\d{3})?)\b', text):
        entities.append([match.start(), match.end(), "ATTACK_TECHNIQUE"])
    
    # Threat actors
    for match in re.finditer(r'\b(APT\d+|APT-[A-Z0-9]+|Lazarus|Fancy Bear|Cozy Bear|Sandworm|Turla)\b', text, re.IGNORECASE):
        entities.append([match.start(), match.end(), "THREAT_ACTOR"])
    
    # Ransomware groups
    for match in re.finditer(r'\b(LockBit|Conti|REvil|BlackCat|ALPHV|RansomExx|Maze|Ryuk)\b', text, re.IGNORECASE):
        entities.append([match.start(), match.end(), "RANSOMWARE_GROUP"])
    
    # Malware families
    for match in re.finditer(r'\b(Emotet|QakBot|TrickBot|IcedID|ZLoader|BazarLoader|Cobalt Strike)\b', text, re.IGNORECASE):
        entities.append([match.start(), match.end(), "MALWARE_FAMILY"])
    
    # Crypto wallets
    for match in re.finditer(r'\b(bc1[a-z0-9]{25,62}|1[a-km-zA-HJ-NP-Z1-9]{25,34}|0x[a-f0-9]{40})\b', text, re.IGNORECASE):
        entities.append([match.start(), match.end(), "CRYPTO_WALLET"])
    
    # Social handles
    for match in re.finditer(r'\b(@[a-zA-Z0-9_]{1,15})\b', text):
        entities.append([match.start(), match.end(), "SOCIAL_HANDLE"])
    
    # Hashtags
    for match in re.finditer(r'\b(#[a-zA-Z0-9_]+)\b', text):
        entities.append([match.start(), match.end(), "HASHTAG"])
    
    # Case IDs
    for match in re.finditer(r'\b(INC\d+|CASE-\d+|RFI-\d+|Operation[A-Z]+)\b', text):
        entities.append([match.start(), match.end(), "CASE_ID"])
    
    # Roles (common patterns)
    role_patterns = [
        r'\b([A-Z][a-z]+ Analyst)\b',
        r'\b([A-Z][a-z]+ Researcher)\b',
        r'\b([A-Z][a-z]+ Specialist)\b',
        r'\b([A-Z][a-z]+ Engineer)\b',
    ]
    for pattern in role_patterns:
        for match in re.finditer(pattern, text):
            entities.append([match.start(), match.end(), "ROLE"])
    
    # Tools (capitalized words that are tools)
    tool_names = [
        "MISP", "OpenCTI", "YARA", "Sigma", "Maltego", "Shodan", "Censys", "GreyNoise",
        "Recorded Future", "Flashpoint", "Anomali", "ThreatConnect", "IntSights",
        "CrowdStrike", "FireEye", "Palo Alto", "IBM X-Force", "VirusTotal", "Abuse.ch",
        "snscrape", "Sherlock", "OSINTgram", "Gephi", "Hoaxy", "TinEye", "Yandex",
        "Meltwater", "Brandwatch", "CrowdTangle", "Talkwalker", "Dataminr", "Graphika",
        "QGIS", "SentinelSat", "OpenStreetMap", "Google Earth", "Planet Labs", "Maxar",
        "ExifTool", "ffmpeg", "OpenCV", "InVID", "Amped", "Clearview", "ShadowDragon",
        "Maigret", "GHunt", "Skiptracer", "theHarvester", "Recon-ng", "Pipl", "Spokeo",
        "GNU Radio", "GQRX", "Wireshark", "Zeek", "Snort", "rtl_433", "Kismet",
        "Amass", "Sublist3r", "DNSRecon", "Fierce", "DomainTools", "SecurityTrails",
    ]
    for tool in tool_names:
        idx = text_lower.find(tool.lower())
        if idx != -1:
            entities.append([idx, idx + len(tool), "TOOL"])
    
    # Remove overlapping entities
    entities = sorted(entities, key=lambda x: (x[0], -x[1]))
    filtered = []
    for ent in entities:
        overlap = False
        for f in filtered:
            if ent[0] < f[1] and ent[1] > f[0]:
                overlap = True
                if (ent[1] - ent[0]) > (f[1] - f[0]):
                    filtered.remove(f)
                    filtered.append(ent)
                break
        if not overlap:
            filtered.append(ent)
    
    return sorted(filtered, key=lambda x: x[0])

def generate_intent_categories(text):
    """Generate realistic intent categories."""
    text_lower = text.lower()
    cats = {
        "INVESTIGATE": 0.0,
        "MONITOR": 0.0,
        "ANALYZE": 0.0,
        "VALIDATE": 0.0,
        "DETECT": 0.0,
        "TRACK": 0.0,
        "ENRICH": 0.0,
        "MAP": 0.0,
        "GENERATE": 0.0,
        "CHECK": 0.0,
    }
    
    if any(kw in text_lower for kw in ["investigate", "check", "find", "who", "what", "where", "is", "are"]):
        cats["INVESTIGATE"] = 1.0
    if any(kw in text_lower for kw in ["monitor", "track", "watch", "follow"]):
        cats["MONITOR"] = 1.0
        cats["TRACK"] = 1.0
    if any(kw in text_lower for kw in ["analyze", "analysis", "examine", "review", "show"]):
        cats["ANALYZE"] = 1.0
    if any(kw in text_lower for kw in ["validate", "verify", "confirm", "authenticate"]):
        cats["VALIDATE"] = 1.0
    if any(kw in text_lower for kw in ["detect", "identify", "flag", "discover"]):
        cats["DETECT"] = 1.0
    if any(kw in text_lower for kw in ["enrich", "enhance", "add data", "get data"]):
        cats["ENRICH"] = 1.0
    if any(kw in text_lower for kw in ["map", "graph", "network", "relationship", "connections"]):
        cats["MAP"] = 1.0
    if any(kw in text_lower for kw in ["generate", "create", "build", "compile", "produce", "make"]):
        cats["GENERATE"] = 1.0
    
    if sum(cats.values()) == 0:
        cats["INVESTIGATE"] = 1.0
    
    return cats

def process_pillar(pillar):
    """Process a single pillar."""
    print(f"Processing {pillar}...", end=" ", flush=True)
    
    try:
        # Get examples for this pillar or generate generic ones
        if pillar in REALISTIC_EXAMPLES:
            entity_texts = REALISTIC_EXAMPLES[pillar]["entities"]
            intent_texts = REALISTIC_EXAMPLES[pillar]["intents"]
        else:
            # Generate generic examples
            entity_texts = [f"{pillar.replace('_', ' ').title()} Analyst conducted intelligence analysis"]
            intent_texts = [f"I need to perform {pillar.replace('_', ' ')} analysis"]
        
        # Generate 100 entities
        entities = []
        for i in range(100):
            if i < len(entity_texts):
                text = entity_texts[i]
            else:
                # Reuse and vary
                base_text = entity_texts[i % len(entity_texts)]
                # Add variation
                text = base_text.replace("Analyst", ["Analyst", "Researcher", "Specialist", "Engineer"][i % 4])
            
            entity_spans = find_entities(text, pillar)
            entities.append({
                "text": text,
                "entities": entity_spans
            })
        
        # Generate 100 intents
        intents = []
        for i in range(100):
            if i < len(intent_texts):
                text = intent_texts[i]
            else:
                # Reuse and vary
                base_text = intent_texts[i % len(intent_texts)]
                text = base_text
            
            cats = generate_intent_categories(text)
            intents.append({
                "text": text,
                "cats": cats
            })
        
        # Write files
        pillar_dir = f"{BASE_PATH}/{pillar}"
        os.makedirs(pillar_dir, exist_ok=True)
        
        with open(f"{pillar_dir}/{pillar}_entities.jsonl", 'w', encoding='utf-8') as f:
            for entity in entities:
                f.write(json.dumps(entity, ensure_ascii=False) + '\n')
        
        with open(f"{pillar_dir}/{pillar}_intent.jsonl", 'w', encoding='utf-8') as f:
            for intent in intents:
                f.write(json.dumps(intent, ensure_ascii=False) + '\n')
        
        print(f"✅ {len(entities)} entities, {len(intents)} intents")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print(f"Generating realistic OSINT entities and intents for {len(OSINT_PILLARS)} pillars...\n")
    
    success = 0
    for pillar in OSINT_PILLARS:
        if process_pillar(pillar):
            success += 1
    
    print(f"\n✅ Completed {success}/{len(OSINT_PILLARS)} pillars!")

