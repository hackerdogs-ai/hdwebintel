#!/usr/bin/env python3
"""
Generate realistic OSINT entities and intents based on actual task definitions.
Reads real task files and definition files to create natural, realistic examples.
"""

import json
import os
import re
import yaml
from pathlib import Path
from collections import defaultdict

OSINT_PILLARS = [
    "ai_int", "comint", "cybint", "darkint", "digint", "dnint", "domain_intel",
    "ecoint", "eduint", "finint", "geoint", "humint", "imint", "infint",
    "legint", "masint", "medint", "natint", "orbint", "sigint", "socmint",
    "techint", "threat_intel", "tradint", "vatint"
]

BASE_PATH = "cyber-train/entities-intent/osint"
OSINT_DEF_PATH = "cyber-train/osint"

def extract_tasks_from_yaml(pillar):
    """Extract task descriptions and expected outputs from tasks.yaml."""
    tasks = []
    tasks_path = f"{OSINT_DEF_PATH}/{pillar}/{pillar}_tasks.yaml"
    
    try:
        with open(tasks_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Parse YAML tasks
            for match in re.finditer(r'(\w+):\s*\n\s*description:\s*[\'"]?([^\n]+)', content):
                task_name = match.group(1)
                description = match.group(2).strip().strip("'\"")
                tasks.append({
                    "name": task_name,
                    "description": description
                })
    except Exception as e:
        pass
    
    return tasks

def extract_agents_from_yaml(pillar):
    """Extract agent roles and goals from agents.yaml."""
    agents = []
    agents_path = f"{OSINT_DEF_PATH}/{pillar}/{pillar}_agents.yaml"
    
    try:
        with open(agents_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract role and goal
            for match in re.finditer(r'(\w+):\s*\n\s*role:\s*>\s*\n\s*([^\n]+)', content, re.MULTILINE):
                agent_name = match.group(1)
                role = match.group(2).strip()
                agents.append({
                    "name": agent_name,
                    "role": role
                })
    except Exception as e:
        pass
    
    return agents

def extract_from_definition(pillar):
    """Extract key terms from definition.md."""
    def_path = f"{OSINT_DEF_PATH}/{pillar}/{pillar}_definition.md"
    content = ""
    
    try:
        with open(def_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        pass
    
    # Extract tools (from numbered lists)
    tools = []
    for match in re.finditer(r'\d+\.\s*\*\*([^*]+)\*\*', content):
        tools.append(match.group(1).strip())
    
    # Extract scenarios (from bullet points)
    scenarios = []
    for match in re.finditer(r'[•\*]\s*([^•\*\n]+)', content):
        scenario = match.group(1).strip()
        if len(scenario) > 15 and len(scenario) < 150:
            scenarios.append(scenario)
    
    # Extract roles
    roles = []
    for match in re.finditer(r'\*\*([^*]+Analyst[^*]*)\*\*', content):
        roles.append(match.group(1).strip())
    for match in re.finditer(r'\*\*([^*]+Specialist[^*]*)\*\*', content):
        roles.append(match.group(1).strip())
    for match in re.finditer(r'\*\*([^*]+Researcher[^*]*)\*\*', content):
        roles.append(match.group(1).strip())
    
    return {
        "tools": tools[:15],
        "scenarios": scenarios[:20],
        "roles": list(set(roles))[:10]
    }

def find_entities_in_text(text, metadata):
    """Find realistic entity spans based on OSINT terminology."""
    entities = []
    text_lower = text.lower()
    
    # Common OSINT entity patterns
    entity_patterns = [
        (r'\b([a-z0-9-]+\.(com|net|org|io|co|gov|edu|ru|cn|de|uk|jp|au|ca|fr|it|es|nl|se|no|dk|fi|pl|cz|hu|ro|gr|pt|ie|be|at|ch|il|ae|sa|in|kr|sg|my|th|ph|id|vn|nz|za|br|mx|ar|cl|co|pe|ve|ec|uy|py|bo|cr|pa|do|gt|hn|ni|sv|bz|jm|tt|bb|gd|lc|vc|ag|dm|kn|bs|sr|gy|gf|fk|ai|vg|ky|bm|tc|ms|aw|cw|sx|bq|mf|gp|mq|re|yt|pm|bl|wf|pf|nc|vu|fj|pg|sb|nc|as|gu|mp|pw|fm|mh|ki|tv|nr|nu|ck|pn|gs|tf|hm|aq|bv|sj|ax|fo|gi|je|gg|im|mt|mc|sm|va|ad|li|mo|hk|tw))\b', "DOMAIN"),
        (r'\b([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\b', "IP_ADDRESS"),
        (r'\b([a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64})\b', "HASH"),
        (r'\b(CVE-\d{4}-\d{4,7})\b', "CVE"),
        (r'\b(T\d{4}(\.\d{3})?)\b', "ATTACK_TECHNIQUE"),
        (r'\b(APT\d+|APT-[A-Z0-9]+|Lazarus|Fancy Bear|Cozy Bear|Sandworm|Turla|Equation Group)\b', "THREAT_ACTOR"),
        (r'\b(LockBit|Conti|REvil|BlackCat|ALPHV|RansomExx|Maze|Ryuk|WannaCry|NotPetya)\b', "RANSOMWARE_GROUP"),
        (r'\b(Emotet|QakBot|TrickBot|IcedID|ZLoader|BazarLoader|Cobalt Strike|Metasploit)\b', "MALWARE_FAMILY"),
        (r'\b(bc1[a-z0-9]{25,62}|1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34})\b', "CRYPTO_WALLET"),
        (r'\b(0x[a-f0-9]{40})\b', "ETH_WALLET"),
        (r'\b(@[a-zA-Z0-9_]{1,15})\b', "SOCIAL_HANDLE"),
        (r'\b(#[a-zA-Z0-9_]+)\b', "HASHTAG"),
        (r'\b(INC\d+|CASE-\d+|RFI-\d+)\b', "CASE_ID"),
        (r'\b([A-Z]{2,10}-\d{4,6})\b', "CAMPAIGN_ID"),
    ]
    
    for pattern, label in entity_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            start, end = match.span()
            entities.append([start, end, label])
    
    # Find roles
    for role in metadata.get("roles", []):
        idx = text_lower.find(role.lower())
        if idx != -1:
            entities.append([idx, idx + len(role), "ROLE"])
    
    # Find tools
    for tool in metadata.get("tools", []):
        idx = text_lower.find(tool.lower())
        if idx != -1:
            entities.append([idx, idx + len(tool), "TOOL"])
    
    # Remove overlapping entities (keep longest)
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

def generate_realistic_entities(pillar, tasks, agents, metadata):
    """Generate 100 realistic entity examples based on actual tasks."""
    entities = []
    
    # Realistic sentence patterns based on actual tasks
    patterns = []
    
    # Patterns from task descriptions
    for task in tasks[:20]:
        desc = task["description"]
        # Create natural sentences from task descriptions
        if "investigate" in desc.lower():
            patterns.append(f"Can you investigate {desc.lower().replace('investigate', '').strip()}?")
        if "monitor" in desc.lower():
            patterns.append(f"We need to monitor {desc.lower().replace('monitor', '').strip()}")
        if "analyze" in desc.lower():
            patterns.append(f"Please analyze {desc.lower().replace('analyze', '').strip()}")
        if "detect" in desc.lower():
            patterns.append(f"Detect {desc.lower().replace('detect', '').strip()}")
        if "validate" in desc.lower():
            patterns.append(f"Validate {desc.lower().replace('validate', '').strip()}")
        if "track" in desc.lower():
            patterns.append(f"Track {desc.lower().replace('track', '').strip()}")
    
    # Add role-based patterns
    for agent in agents[:10]:
        role = agent["role"]
        if "analyst" in role.lower():
            patterns.append(f"{role} conducted investigation on suspicious activity")
        if "researcher" in role.lower():
            patterns.append(f"{role} analyzed threat intelligence data")
        if "specialist" in role.lower():
            patterns.append(f"{role} identified security indicators")
    
    # Add scenario-based patterns
    for scenario in metadata.get("scenarios", [])[:15]:
        if len(scenario) > 20:
            # Extract key phrase
            words = scenario.split()[:5]
            key_phrase = " ".join(words)
            patterns.append(f"Detected {key_phrase} requiring immediate analysis")
            patterns.append(f"Monitoring {key_phrase} across multiple platforms")
    
    # Add tool-based patterns
    for tool in metadata.get("tools", [])[:15]:
        patterns.append(f"Using {tool} to analyze threat indicators")
        patterns.append(f"{tool} detected suspicious domain example.com")
        patterns.append(f"{tool} identified IOC hash abc123def456")
    
    # Generate realistic examples with actual OSINT terminology
    realistic_examples = [
        # SOCMINT examples
        "SOCMINT Analyst detected coordinated disinformation campaign #BreakingNews with 85% bot amplification score",
        "Disinformation Researcher validated viral video using reverse image search on TinEye and Yandex Images",
        "Data Scientist mapped influence network graph showing 450 nodes and 1200 edges using Gephi visualization",
        "Digital Forensics Specialist flagged suspicious account @suspicious_user with bot score 0.92 requiring review",
        "Incident Responder generated real-time alert for brand impersonation campaign targeting AcmeCorp on Twitter",
        "SOCMINT Analyst monitored hashtag #Election2025 detecting 1200 coordinated posts from bot cluster",
        "Using snscrape to collect Twitter data for hashtag analysis and sentiment scoring",
        "Sherlock username enumeration found @target_user across 15 platforms including Telegram and Discord",
        "Meltwater social listening detected 340 negative mentions requiring brand reputation response",
        "Brandwatch identified narrative shift in sentiment from 65% positive to 32% positive over 48 hours",
        
        # Threat Intel examples
        "Threat Intel Analyst enriched IOC domain secure-login.net with WHOIS pDNS and CT log data",
        "Malware Researcher analyzed sample SHA256 abc123def456 identifying QakBot family with 95% confidence",
        "Dark Web Analyst found brand mention AcmeCorp in 5 forums with 12 credential dumps",
        "CTI Analyst mapped campaign OperationShadow to MITRE ATT&CK techniques T1566 T1071 T1105",
        "Threat Intelligence Analyst published STIX feed with 2100 IOCs to OpenCTI and MISP platforms",
        "Malware Researcher generated YARA rule for Emotet variant detecting 87% of samples",
        "Threat Hunter created hunting pack with Sigma rules for T1059 command execution",
        "IOC enrichment found related IPs 1.2.3.4 and 5.6.7.8 linked to C2 infrastructure",
        "Recorded Future threat feed identified 47 new domains associated with APT29 activity",
        "Flashpoint dark web monitoring detected ransomware leak site posting victim data",
        
        # CYBINT examples
        "Cyber Threat Analyst investigated phishing domain secure-login-apple.com with kit detection",
        "Malware Reverse Engineer analyzed QakBot sample extracting C2 domains and registry keys",
        "Threat Hunter tracked zero-day exploit CVE-2025-1111 with EPSS score 0.91 and KEV listing",
        "Vulnerability Intelligence Analyst prioritized CVE-2025-2222 based on exploit availability",
        "Cyber Intelligence Analyst correlated IOCs into campaign cluster with 7 related samples",
        "Secret Exposure Analyst detected 15 exposed API keys on GitHub requiring immediate revocation",
        "Dark Web Analyst found credential leak CompanyX_Creds with 5000 records on BreachForums",
        "Threat Researcher identified LockBit ransomware group targeting healthcare sector",
        "IOC feed ingestion processed 5400 indicators with 32% deduplication rate",
        "Campaign tracking mapped OperationPhish to ATT&CK techniques with 82% attribution confidence",
        
        # DARKINT examples
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
        
        # GEOINT examples
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
        
        # HUMINT examples
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
        
        # FININT examples
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
        
        # Domain Intel examples
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
        
        # IMINT examples
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
        
        # SIGINT examples
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
    ]
    
    # Generate 100 examples
    for i in range(100):
        if i < len(realistic_examples):
            text = realistic_examples[i]
        else:
            # Generate from patterns
            pattern = patterns[i % len(patterns)] if patterns else f"{pillar} analysis"
            text = pattern
            
            # Add realistic details
            if i % 3 == 0 and metadata.get("tools"):
                tool = metadata["tools"][i % len(metadata["tools"])]
                text = f"Using {tool} {text}"
            if i % 5 == 0 and metadata.get("roles"):
                role = metadata["roles"][i % len(metadata["roles"])]
                text = f"{role} {text}"
        
        entity_spans = find_entities_in_text(text, metadata)
        entities.append({
            "text": text,
            "entities": entity_spans
        })
    
    return entities[:100]

def generate_realistic_intents(pillar, tasks, agents, metadata):
    """Generate 100 realistic intent examples based on actual user queries."""
    intents = []
    
    # Realistic user query patterns based on actual tasks
    query_patterns = []
    
    # From task descriptions - make them sound like real questions
    for task in tasks[:30]:
        desc = task["description"].lower()
        
        # Convert task descriptions to natural questions
        if "investigate" in desc:
            query_patterns.append(f"Can you investigate {desc.replace('investigate', '').strip()}?")
            query_patterns.append(f"I need to investigate {desc.replace('investigate', '').strip()}")
        if "monitor" in desc:
            query_patterns.append(f"Please monitor {desc.replace('monitor', '').strip()}")
            query_patterns.append(f"Set up monitoring for {desc.replace('monitor', '').strip()}")
        if "analyze" in desc:
            query_patterns.append(f"Analyze {desc.replace('analyze', '').strip()} for me")
            query_patterns.append(f"Can you analyze {desc.replace('analyze', '').strip()}?")
        if "validate" in desc:
            query_patterns.append(f"Validate {desc.replace('validate', '').strip()}")
            query_patterns.append(f"Please validate {desc.replace('validate', '').strip()}")
        if "detect" in desc:
            query_patterns.append(f"Detect {desc.replace('detect', '').strip()}")
        if "track" in desc:
            query_patterns.append(f"Track {desc.replace('track', '').strip()}")
        if "check" in desc:
            query_patterns.append(f"Check {desc.replace('check', '').strip()}")
        if "build" in desc:
            query_patterns.append(f"Build {desc.replace('build', '').strip()}")
        if "generate" in desc:
            query_patterns.append(f"Generate {desc.replace('generate', '').strip()}")
        if "create" in desc:
            query_patterns.append(f"Create {desc.replace('create', '').strip()}")
    
    # Add natural question patterns
    natural_queries = [
        # SOCMINT
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
        
        # Threat Intel
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
        
        # CYBINT
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
        
        # DARKINT
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
        
        # GEOINT
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
        
        # HUMINT
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
        
        # FININT
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
        
        # Domain Intel
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
    ]
    
    # Intent categories based on actual OSINT operations
    base_cats = {
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
    
    for i in range(100):
        if i < len(natural_queries):
            text = natural_queries[i]
        elif i < len(natural_queries) + len(query_patterns):
            text = query_patterns[i - len(natural_queries)]
        else:
            # Generate from task descriptions
            if tasks:
                task = tasks[i % len(tasks)]
                text = f"Can you {task['description'].lower()}?"
            else:
                text = f"I need to perform {pillar.replace('_', ' ')} analysis"
        
        # Determine intent categories based on keywords
        cats = base_cats.copy()
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ["investigate", "check", "find", "who", "what", "where"]):
            cats["INVESTIGATE"] = 1.0
        if any(kw in text_lower for kw in ["monitor", "track", "watch", "follow"]):
            cats["MONITOR"] = 1.0
            cats["TRACK"] = 1.0
        if any(kw in text_lower for kw in ["analyze", "analysis", "examine", "review"]):
            cats["ANALYZE"] = 1.0
        if any(kw in text_lower for kw in ["validate", "verify", "confirm", "authenticate"]):
            cats["VALIDATE"] = 1.0
        if any(kw in text_lower for kw in ["detect", "identify", "flag", "discover"]):
            cats["DETECT"] = 1.0
        if any(kw in text_lower for kw in ["enrich", "enhance", "add data"]):
            cats["ENRICH"] = 1.0
        if any(kw in text_lower for kw in ["map", "graph", "network", "relationship"]):
            cats["MAP"] = 1.0
        if any(kw in text_lower for kw in ["generate", "create", "build", "compile", "produce"]):
            cats["GENERATE"] = 1.0
        
        # If no category matched, assign based on position
        if sum(cats.values()) == 0:
            cats[list(cats.keys())[i % len(cats)]] = 1.0
        
        intents.append({
            "text": text,
            "cats": cats
        })
    
    return intents[:100]

def process_pillar(pillar):
    """Process a single OSINT pillar."""
    print(f"Processing {pillar}...", end=" ", flush=True)
    
    try:
        tasks = extract_tasks_from_yaml(pillar)
        agents = extract_agents_from_yaml(pillar)
        metadata = extract_from_definition(pillar)
        
        entities = generate_realistic_entities(pillar, tasks, agents, metadata)
        intents = generate_realistic_intents(pillar, tasks, agents, metadata)
        
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
    print(f"Generating realistic entities and intents for {len(OSINT_PILLARS)} OSINT pillars...\n")
    
    success_count = 0
    for pillar in OSINT_PILLARS:
        if process_pillar(pillar):
            success_count += 1
    
    print(f"\n✅ Completed {success_count}/{len(OSINT_PILLARS)} OSINT pillars!")

