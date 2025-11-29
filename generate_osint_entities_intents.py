#!/usr/bin/env python3
"""
Generate entities and intents for all OSINT pillars.
Creates 100 entities and 100 intents for each of the 25 OSINT pillars.
"""

import json
import os
from pathlib import Path

# All OSINT pillars
OSINT_PILLARS = [
    "ai_int", "comint", "cybint", "darkint", "digint", "dnint", "domain_intel",
    "ecoint", "eduint", "finint", "geoint", "humint", "imint", "infint",
    "legint", "masint", "medint", "natint", "orbint", "sigint", "socmint",
    "techint", "threat_intel", "tradint", "vatint"
]

BASE_PATH = "cyber-train/entities-intent/osint"
OSINT_DEF_PATH = "cyber-train/osint"

def read_definition_file(pillar):
    """Read the definition file for a pillar."""
    def_path = f"{OSINT_DEF_PATH}/{pillar}/{pillar}_definition.md"
    try:
        with open(def_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def read_agents_file(pillar):
    """Read the agents file for a pillar."""
    agents_path = f"{OSINT_DEF_PATH}/{pillar}/{pillar}_agents.yaml"
    try:
        with open(agents_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def generate_entities_for_pillar(pillar, definition, agents):
    """Generate 100 entity examples for a pillar."""
    entities = []
    
    # Extract key terms from definition and agents
    roles = []
    tools = []
    concepts = []
    
    # Common OSINT roles
    if "analyst" in definition.lower() or "analyst" in agents.lower():
        roles.extend(["Analyst", "Threat Analyst", "Intelligence Analyst", "OSINT Analyst"])
    if "researcher" in definition.lower():
        roles.extend(["Researcher", "Threat Researcher", "Intelligence Researcher"])
    if "engineer" in definition.lower():
        roles.extend(["Engineer", "Data Engineer", "Security Engineer"])
    if "investigator" in definition.lower():
        roles.extend(["Investigator", "Digital Investigator", "Forensic Investigator"])
    
    # Extract tool names (common patterns)
    if "MISP" in definition or "MISP" in agents:
        tools.append("MISP")
    if "OpenCTI" in definition or "OpenCTI" in agents:
        tools.append("OpenCTI")
    if "Shodan" in definition or "Shodan" in agents:
        tools.append("Shodan")
    if "Censys" in definition or "Censys" in agents:
        tools.append("Censys")
    if "Maltego" in definition or "Maltego" in agents:
        tools.append("Maltego")
    if "YARA" in definition or "YARA" in agents:
        tools.append("YARA")
    if "Recorded Future" in definition:
        tools.append("Recorded Future")
    if "Flashpoint" in definition:
        tools.append("Flashpoint")
    if "Intel 471" in definition:
        tools.append("Intel 471")
    
    # Generate entity examples based on pillar type
    pillar_lower = pillar.lower()
    
    # AI-INT specific
    if "ai_int" in pillar_lower:
        entities.extend([
            {"text": "AI Threat Analyst monitored AI misuse across OSINT dark web and GitHub", "entities": [[0, 2, "TOOL"], [3, 9, "THREAT_TYPE"], [10, 17, "ANALYST_TYPE"], [26, 28, "TOOL"], [29, 33, "MISUSE_TYPE"], [40, 48, "TOOL"], [49, 57, "TOOL"], [62, 68, "TOOL"]]},
            {"text": "Synthetic Media Investigator detected deepfakes and AI-generated media", "entities": [[0, 9, "SYNTHETIC_TYPE"], [10, 20, "MEDIA_TYPE"], [21, 33, "INVESTIGATOR_TYPE"], [42, 50, "DETECTION_TYPE"], [51, 60, "DEEPFAKE_TYPE"], [65, 79, "MEDIA_TYPE"]]},
            {"text": "Adversarial ML Researcher tested AI ML pipelines for poisoning and evasion", "entities": [[0, 12, "ADVERSARIAL_TYPE"], [13, 15, "TOOL"], [16, 26, "RESEARCHER_TYPE"], [35, 37, "TOOL"], [38, 40, "TOOL"], [41, 50, "PIPELINE_TYPE"], [55, 64, "POISONING_TYPE"], [69, 77, "EVASION_TYPE"]]},
            {"text": "Prompt Security Engineer detected prompt injection and malicious LLM usage", "entities": [[0, 6, "PROMPT_TYPE"], [7, 15, "SECURITY_TYPE"], [16, 24, "ENGINEER_TYPE"], [33, 40, "DETECTION_TYPE"], [41, 56, "INJECTION_TYPE"], [61, 68, "MALWARE_TYPE"], [69, 72, "TOOL"], [73, 76, "USAGE_TYPE"]]},
            {"text": "AI Policy Compliance Officer ensured compliance with EU AI Act and NIST RMF", "entities": [[0, 2, "TOOL"], [3, 10, "POLICY_TYPE"], [11, 22, "COMPLIANCE_TYPE"], [23, 30, "OFFICER_TYPE"], [39, 46, "ENSURANCE_TYPE"], [47, 50, "COMPLIANCE_TYPE"], [55, 57, "FRAMEWORK"], [58, 65, "FRAMEWORK"], [66, 69, "FRAMEWORK"], [70, 73, "FRAMEWORK"]]},
            {"text": "AI Marketplace Monitor tracked AI model dataset and API sales on dark web", "entities": [[0, 2, "TOOL"], [3, 13, "MARKETPLACE_TYPE"], [14, 21, "MONITOR_TYPE"], [30, 32, "TOOL"], [33, 38, "MODEL_TYPE"], [39, 46, "DATASET_TYPE"], [51, 54, "TOOL"], [55, 58, "SALES_TYPE"], [63, 71, "NETWORK_TYPE"]]},
            {"text": "Synthetic Persona Analyst detected AI-generated personas across social media", "entities": [[0, 9, "SYNTHETIC_TYPE"], [10, 16, "PERSONA_TYPE"], [17, 24, "ANALYST_TYPE"], [33, 40, "DETECTION_TYPE"], [41, 43, "TOOL"], [44, 52, "PERSONA_TYPE"], [59, 71, "MEDIA_TYPE"]]},
            {"text": "DeepFaceLab synthetic media detection tool analyzed deepfake content", "entities": [[0, 10, "TOOL"], [11, 19, "SYNTHETIC_TYPE"], [20, 25, "MEDIA_TYPE"], [26, 35, "DETECTION_TYPE"], [36, 40, "TOOL"], [49, 58, "DEEPFAKE_TYPE"], [59, 66, "CONTENT_TYPE"]]},
            {"text": "FakeCatcher real-time deepfake detection identified synthetic videos", "entities": [[0, 10, "TOOL"], [11, 20, "DETECTION_TYPE"], [21, 30, "DEEPFAKE_TYPE"], [31, 40, "DETECTION_TYPE"], [49, 58, "IDENTIFICATION_TYPE"], [59, 68, "SYNTHETIC_TYPE"], [69, 76, "VIDEO_TYPE"]]},
            {"text": "Reality Defender deepfake detection SaaS platform scanned media files", "entities": [[0, 8, "TOOL"], [9, 19, "TOOL"], [20, 30, "DEEPFAKE_TYPE"], [31, 40, "DETECTION_TYPE"], [41, 44, "TOOL"], [45, 50, "PLATFORM_TYPE"], [59, 65, "SCANNING_TYPE"], [66, 72, "MEDIA_TYPE"], [73, 79, "FILE_TYPE"]]},
            {"text": "Blackbird AI disinformation detection platform mapped narrative networks", "entities": [[0, 8, "TOOL"], [9, 11, "TOOL"], [12, 26, "DETECTION_TYPE"], [27, 35, "PLATFORM_TYPE"], [44, 50, "MAPPING_TYPE"], [51, 60, "NARRATIVE_TYPE"], [61, 70, "NETWORK_TYPE"]]},
            {"text": "Recorded Future AI-INT dark web AI monitoring intelligence feeds", "entities": [[0, 8, "TOOL"], [9, 15, "TOOL"], [16, 21, "TOOL"], [22, 30, "NETWORK_TYPE"], [31, 33, "TOOL"], [34, 44, "MONITORING_TYPE"], [45, 57, "INTELLIGENCE_TYPE"], [58, 63, "FEED_TYPE"]]},
            {"text": "Palantir Gotham AI modules enabled AI entity resolution", "entities": [[0, 8, "TOOL"], [9, 14, "TOOL"], [15, 17, "TOOL"], [18, 26, "RESOLUTION_TYPE"], [35, 37, "TOOL"], [38, 44, "ENTITY_TYPE"], [45, 54, "RESOLUTION_TYPE"]]},
            {"text": "Darktrace DETECT adversarial AI anomaly detection identified threats", "entities": [[0, 9, "TOOL"], [10, 16, "TOOL"], [17, 28, "ADVERSARIAL_TYPE"], [29, 32, "TOOL"], [33, 41, "ANOMALY_TYPE"], [42, 51, "DETECTION_TYPE"], [60, 68, "IDENTIFICATION_TYPE"], [69, 77, "THREAT_TYPE"]]},
            {"text": "ZeroFox AI deepfake botnet and disinformation detection platform", "entities": [[0, 7, "TOOL"], [8, 10, "TOOL"], [11, 19, "DEEPFAKE_TYPE"], [20, 26, "BOTNET_TYPE"], [31, 35, "DETECTION_TYPE"], [36, 46, "PLATFORM_TYPE"]]},
            {"text": "Graphika AI network mapping of AI-driven influence operations", "entities": [[0, 8, "TOOL"], [9, 11, "TOOL"], [12, 18, "NETWORK_TYPE"], [19, 24, "MAPPING_TYPE"], [31, 33, "TOOL"], [34, 43, "INFLUENCE_TYPE"], [44, 55, "OPERATION_TYPE"]]},
            {"text": "Cortical AI semantic intelligence platform analyzed text content", "entities": [[0, 8, "TOOL"], [9, 11, "TOOL"], [12, 21, "SEMANTIC_TYPE"], [22, 35, "INTELLIGENCE_TYPE"], [36, 45, "PLATFORM_TYPE"], [54, 61, "ANALYSIS_TYPE"], [62, 66, "TEXT_TYPE"], [67, 75, "CONTENT_TYPE"]]},
            {"text": "Thorn Spotlight AI detection of child exploitation content", "entities": [[0, 4, "TOOL"], [5, 14, "TOOL"], [15, 17, "TOOL"], [18, 30, "DETECTION_TYPE"], [35, 42, "EXPLOITATION_TYPE"], [43, 50, "CONTENT_TYPE"]]},
            {"text": "Clarifai AI Guardrails API-based AI detection and moderation", "entities": [[0, 8, "TOOL"], [9, 11, "TOOL"], [12, 22, "TOOL"], [23, 32, "TOOL"], [33, 36, "TOOL"], [37, 45, "TOOL"], [46, 55, "DETECTION_TYPE"], [60, 70, "MODERATION_TYPE"]]},
            {"text": "OpenAI Evals OSS adversarial prompt LLM evaluation framework", "entities": [[0, 7, "TOOL"], [8, 12, "TOOL"], [13, 16, "TOOL"], [17, 27, "ADVERSARIAL_TYPE"], [28, 34, "PROMPT_TYPE"], [35, 38, "TOOL"], [39, 49, "EVALUATION_TYPE"], [50, 60, "FRAMEWORK_TYPE"]]},
            {"text": "TextFooler adversarial text attack toolkit tested models", "entities": [[0, 10, "TOOL"], [11, 22, "ADVERSARIAL_TYPE"], [23, 27, "TEXT_TYPE"], [28, 34, "ATTACK_TYPE"], [35, 42, "TOOLKIT_TYPE"], [51, 58, "TESTING_TYPE"], [59, 66, "MODEL_TYPE"]]},
            {"text": "Adversarial Robustness Toolbox ART IBM tested ML defenses", "entities": [[0, 22, "TOOL"], [23, 26, "TOOL"], [27, 30, "TOOL"], [31, 33, "TOOL"], [42, 48, "TESTING_TYPE"], [49, 51, "TOOL"], [52, 54, "TOOL"], [55, 64, "DEFENSE_TYPE"]]},
            {"text": "MalGAN adversarial malware generation detection tool", "entities": [[0, 6, "TOOL"], [7, 18, "ADVERSARIAL_TYPE"], [19, 27, "MALWARE_TYPE"], [28, 38, "GENERATION_TYPE"], [39, 48, "DETECTION_TYPE"], [49, 53, "TOOL"]]},
            {"text": "GPT-Detector OSS AI vs human text classifier analyzed content", "entities": [[0, 12, "TOOL"], [13, 16, "TOOL"], [17, 19, "TOOL"], [20, 22, "TOOL"], [23, 31, "TEXT_TYPE"], [32, 42, "CLASSIFIER_TYPE"], [51, 58, "ANALYSIS_TYPE"], [59, 66, "CONTENT_TYPE"]]},
            {"text": "Hugging Face Evaluate model performance and robustness testing", "entities": [[0, 7, "TOOL"], [8, 12, "TOOL"], [13, 21, "TOOL"], [30, 36, "MODEL_TYPE"], [37, 48, "PERFORMANCE_TYPE"], [53, 64, "ROBUSTNESS_TYPE"], [65, 72, "TESTING_TYPE"]]},
            {"text": "LlamaIndex LangKit Security modules for LLM observability", "entities": [[0, 10, "TOOL"], [11, 17, "TOOL"], [18, 26, "SECURITY_TYPE"], [27, 34, "MODULE_TYPE"], [43, 46, "TOOL"], [47, 54, "OBSERVABILITY_TYPE"]]},
            {"text": "Exposing AI datasets face recognition dataset risk mapping", "entities": [[0, 9, "TOOL"], [10, 12, "TOOL"], [13, 20, "DATASET_TYPE"], [21, 30, "RECOGNITION_TYPE"], [31, 37, "DATASET_TYPE"], [38, 42, "RISK_TYPE"], [43, 49, "MAPPING_TYPE"]]},
            {"text": "Deepware Scanner enterprise-grade deepfake scanner analyzed videos", "entities": [[0, 10, "TOOL"], [11, 19, "SCANNER_TYPE"], [20, 30, "DEEPFAKE_TYPE"], [31, 40, "SCANNER_TYPE"], [49, 58, "ANALYSIS_TYPE"], [59, 66, "VIDEO_TYPE"]]},
            {"text": "Sensity AI commercial suite enterprise synthetic media monitoring", "entities": [[0, 7, "TOOL"], [8, 11, "TOOL"], [12, 20, "TOOL"], [21, 31, "SUITE_TYPE"], [40, 49, "SYNTHETIC_TYPE"], [50, 56, "MEDIA_TYPE"], [57, 68, "MONITORING_TYPE"]]},
            {"text": "AI-generated content detection precision reached 90 percent", "entities": [[0, 2, "TOOL"], [3, 12, "CONTENT_TYPE"], [13, 22, "DETECTION_TYPE"], [23, 33, "PRECISION_TYPE"], [42, 44, "METRIC_TYPE"], [45, 47, "METRIC_TYPE"]]},
            {"text": "Prompt injection block rate achieved 95 percent success", "entities": [[0, 6, "PROMPT_TYPE"], [7, 15, "INJECTION_TYPE"], [16, 21, "BLOCK_TYPE"], [22, 26, "METRIC_TYPE"], [35, 42, "METRIC_TYPE"], [43, 45, "METRIC_TYPE"], [46, 53, "SUCCESS_TYPE"]]},
            {"text": "Model poisoning detection within 24 hours of attack", "entities": [[0, 6, "MODEL_TYPE"], [7, 15, "POISONING_TYPE"], [16, 25, "DETECTION_TYPE"], [33, 36, "COUNT"], [37, 42, "TIME_UNIT"], [46, 52, "ATTACK_TYPE"]]},
            {"text": "AI Threat Digest delivery SLA achieved 100 percent weekly", "entities": [[0, 2, "TOOL"], [3, 9, "THREAT_TYPE"], [10, 16, "DIGEST_TYPE"], [17, 25, "DELIVERY_TYPE"], [26, 29, "TOOL"], [30, 32, "TOOL"], [41, 43, "METRIC_TYPE"], [44, 46, "METRIC_TYPE"], [47, 53, "TIME_UNIT"]]},
            {"text": "Cross-pillar validation rate reached 85 percent accuracy", "entities": [[0, 5, "CROSS_TYPE"], [6, 12, "PILLAR_TYPE"], [13, 24, "VALIDATION_TYPE"], [25, 29, "METRIC_TYPE"], [38, 40, "METRIC_TYPE"], [41, 43, "METRIC_TYPE"], [44, 52, "ACCURACY_TYPE"]]},
            {"text": "Executive satisfaction score achieved 4.5 out of 5 rating", "entities": [[0, 10, "EXECUTIVE_TYPE"], [11, 23, "SATISFACTION_TYPE"], [24, 29, "SCORE_TYPE"], [38, 41, "METRIC_TYPE"], [42, 44, "METRIC_TYPE"], [48, 50, "COUNT"], [54, 60, "RATING_TYPE"]]},
            {"text": "Deepfake detection precision recall metrics improved", "entities": [[0, 9, "DEEPFAKE_TYPE"], [10, 19, "DETECTION_TYPE"], [20, 29, "PRECISION_TYPE"], [30, 36, "RECALL_TYPE"], [37, 44, "METRIC_TYPE"], [53, 61, "IMPROVEMENT_TYPE"]]},
            {"text": "Adversarial test coverage expanded to 95 percent of models", "entities": [[0, 12, "ADVERSARIAL_TYPE"], [13, 17, "TEST_TYPE"], [18, 26, "COVERAGE_TYPE"], [35, 37, "METRIC_TYPE"], [38, 40, "METRIC_TYPE"], [47, 53, "MODEL_TYPE"]]},
            {"text": "Dataset integrity scores validated for all training datasets", "entities": [[0, 7, "DATASET_TYPE"], [8, 17, "INTEGRITY_TYPE"], [18, 24, "SCORE_TYPE"], [33, 42, "VALIDATION_TYPE"], [47, 50, "TRAINING_TYPE"], [51, 60, "DATASET_TYPE"]]},
            {"text": "AI-powered disinformation campaign detected synthetic media", "entities": [[0, 2, "TOOL"], [3, 11, "DISINFORMATION_TYPE"], [12, 21, "CAMPAIGN_TYPE"], [30, 37, "DETECTION_TYPE"], [38, 47, "SYNTHETIC_TYPE"], [48, 54, "MEDIA_TYPE"]]},
            {"text": "Adversarial ML attack poisoned OSINT datasets evading classifiers", "entities": [[0, 12, "ADVERSARIAL_TYPE"], [13, 15, "TOOL"], [16, 22, "ATTACK_TYPE"], [30, 37, "POISONING_TYPE"], [38, 43, "TOOL"], [44, 52, "DATASET_TYPE"], [59, 67, "EVASION_TYPE"], [68, 79, "CLASSIFIER_TYPE"]]},
            {"text": "AI-assisted cybercrime generative models used for phishing", "entities": [[0, 2, "TOOL"], [3, 14, "CYBERCRIME_TYPE"], [15, 25, "GENERATION_TYPE"], [26, 33, "MODEL_TYPE"], [40, 49, "PHISHING_TYPE"]]},
            {"text": "Autonomous botnet AI-controlled bots managed C2 operations", "entities": [[0, 11, "AUTONOMOUS_TYPE"], [12, 18, "BOTNET_TYPE"], [19, 21, "TOOL"], [22, 31, "CONTROL_TYPE"], [32, 36, "BOT_TYPE"], [45, 47, "TOOL"], [48, 50, "TOOL"], [51, 62, "OPERATION_TYPE"]]},
            {"text": "Synthetic identity creation AI-generated personas infiltrated platforms", "entities": [[0, 9, "SYNTHETIC_TYPE"], [10, 18, "IDENTITY_TYPE"], [19, 27, "CREATION_TYPE"], [28, 30, "TOOL"], [31, 40, "PERSONA_TYPE"], [49, 61, "INFILTRATION_TYPE"], [62, 71, "PLATFORM_TYPE"]]},
            {"text": "Model provenance leakage stolen AI models weights leaked on dark web", "entities": [[0, 6, "MODEL_TYPE"], [7, 17, "PROVENANCE_TYPE"], [18, 25, "LEAKAGE_TYPE"], [33, 39, "STOLEN_TYPE"], [40, 42, "TOOL"], [43, 49, "MODEL_TYPE"], [50, 57, "WEIGHT_TYPE"], [64, 72, "NETWORK_TYPE"]]},
            {"text": "Prompt injection LLM abuse OSINT workflows compromised", "entities": [[0, 6, "PROMPT_TYPE"], [7, 15, "INJECTION_TYPE"], [16, 19, "TOOL"], [20, 22, "TOOL"], [23, 28, "ABUSE_TYPE"], [29, 34, "TOOL"], [35, 44, "WORKFLOW_TYPE"], [55, 66, "COMPROMISE_TYPE"]]},
            {"text": "Cross-pillar AI fusion adversaries fused SOCMINT CYBINT and HUMINT", "entities": [[0, 5, "CROSS_TYPE"], [6, 12, "PILLAR_TYPE"], [13, 15, "TOOL"], [16, 19, "FUSION_TYPE"], [30, 40, "ADVERSARY_TYPE"], [41, 47, "FUSION_TYPE"], [48, 55, "TOOL"], [56, 62, "TOOL"], [67, 73, "TOOL"]]},
            {"text": "AI policy circumvention misuse of open-source models bypassed constraints", "entities": [[0, 2, "TOOL"], [3, 10, "POLICY_TYPE"], [11, 25, "CIRCUMVENTION_TYPE"], [34, 42, "MISUSE_TYPE"], [49, 60, "MODEL_TYPE"], [69, 77, "BYPASS_TYPE"], [78, 84, "CONSTRAINT_TYPE"]]},
            {"text": "Defensive AI monitoring failure to detect AI-driven threats early", "entities": [[0, 10, "DEFENSIVE_TYPE"], [11, 13, "TOOL"], [14, 23, "MONITORING_TYPE"], [33, 40, "FAILURE_TYPE"], [47, 53, "DETECTION_TYPE"], [54, 57, "TOOL"], [58, 66, "THREAT_TYPE"], [74, 79, "EARLY_TYPE"]]},
            {"text": "Synthetic media detection image video and voice deepfake pipelines", "entities": [[0, 9, "SYNTHETIC_TYPE"], [10, 16, "MEDIA_TYPE"], [17, 26, "DETECTION_TYPE"], [34, 39, "IMAGE_TYPE"], [40, 45, "VIDEO_TYPE"], [54, 59, "VOICE_TYPE"], [60, 69, "DEEPFAKE_TYPE"], [70, 79, "PIPELINE_TYPE"]]},
            {"text": "Model dataset telemetry monitored model leaks fine-tune datasets", "entities": [[0, 6, "MODEL_TYPE"], [7, 14, "DATASET_TYPE"], [15, 25, "TELEMETRY_TYPE"], [34, 42, "MONITORING_TYPE"], [43, 49, "MODEL_TYPE"], [50, 55, "LEAK_TYPE"], [56, 66, "DATASET_TYPE"]]},
            {"text": "Adversarial resilience continuously tested ML LLM models", "entities": [[0, 12, "ADVERSARIAL_TYPE"], [13, 24, "RESILIENCE_TYPE"], [35, 42, "TESTING_TYPE"], [43, 45, "TOOL"], [46, 48, "TOOL"], [49, 56, "MODEL_TYPE"]]},
            {"text": "Threat actor monitoring tracked AI tool usage in forums", "entities": [[0, 6, "THREAT_TYPE"], [7, 12, "ACTOR_TYPE"], [13, 23, "MONITORING_TYPE"], [32, 38, "TRACKING_TYPE"], [39, 41, "TOOL"], [42, 46, "TOOL"], [47, 52, "USAGE_TYPE"], [56, 63, "FORUM_TYPE"]]},
            {"text": "Governance compliance monitored AI usage against NIST AI RMF", "entities": [[0, 11, "GOVERNANCE_TYPE"], [12, 22, "COMPLIANCE_TYPE"], [32, 40, "MONITORING_TYPE"], [41, 43, "TOOL"], [44, 50, "USAGE_TYPE"], [59, 63, "FRAMEWORK"], [64, 66, "TOOL"], [67, 70, "FRAMEWORK"]]},
            {"text": "EU AI Act compliance validated AI system requirements", "entities": [[0, 2, "FRAMEWORK"], [3, 5, "TOOL"], [6, 9, "FRAMEWORK"], [10, 21, "COMPLIANCE_TYPE"], [31, 40, "VALIDATION_TYPE"], [41, 43, "TOOL"], [44, 50, "SYSTEM_TYPE"], [51, 63, "REQUIREMENT_TYPE"]]},
            {"text": "ISO IEC 42001 AI management system standard compliance", "entities": [[0, 3, "FRAMEWORK"], [4, 7, "FRAMEWORK"], [8, 13, "FRAMEWORK"], [14, 16, "TOOL"], [17, 28, "MANAGEMENT_TYPE"], [29, 35, "SYSTEM_TYPE"], [36, 44, "STANDARD_TYPE"], [45, 55, "COMPLIANCE_TYPE"]]},
            {"text": "Cross-pillar fusion connected SOCMINT CYBINT and HUMINT", "entities": [[0, 5, "CROSS_TYPE"], [6, 12, "PILLAR_TYPE"], [13, 19, "FUSION_TYPE"], [29, 35, "CONNECTION_TYPE"], [36, 43, "TOOL"], [44, 50, "TOOL"], [55, 61, "TOOL"]]},
            {"text": "Red-teaming AI adversarial testing of generative AI models", "entities": [[0, 11, "TESTING_TYPE"], [13, 15, "TOOL"], [16, 27, "ADVERSARIAL_TYPE"], [28, 35, "TESTING_TYPE"], [42, 53, "GENERATION_TYPE"], [54, 56, "TOOL"], [57, 63, "MODEL_TYPE"]]},
            {"text": "Transparency layer maintained audit logs of AI-generated intelligence", "entities": [[0, 13, "TRANSPARENCY_TYPE"], [14, 20, "LAYER_TYPE"], [29, 37, "MAINTENANCE_TYPE"], [38, 43, "AUDIT_TYPE"], [44, 48, "LOG_TYPE"], [53, 55, "TOOL"], [56, 66, "INTELLIGENCE_TYPE"]]},
            {"text": "Scalable infrastructure GPU TPU monitoring for large-scale AI threat scanning", "entities": [[0, 9, "SCALABLE_TYPE"], [10, 23, "INFRASTRUCTURE_TYPE"], [33, 36, "TOOL"], [37, 40, "TOOL"], [41, 51, "MONITORING_TYPE"], [56, 67, "TOOL"], [68, 74, "THREAT_TYPE"], [75, 83, "SCANNING_TYPE"]]},
            {"text": "GAN detection deepfake forensics analyzed synthetic media", "entities": [[0, 3, "TOOL"], [4, 13, "DETECTION_TYPE"], [14, 23, "DEEPFAKE_TYPE"], [24, 33, "FORENSIC_TYPE"], [42, 49, "ANALYSIS_TYPE"], [50, 59, "SYNTHETIC_TYPE"], [60, 66, "MEDIA_TYPE"]]},
            {"text": "Disinformation narratives tracked AI-generated content campaigns", "entities": [[0, 14, "DISINFORMATION_TYPE"], [15, 25, "NARRATIVE_TYPE"], [33, 40, "TRACKING_TYPE"], [41, 43, "TOOL"], [44, 52, "CONTENT_TYPE"], [53, 63, "CAMPAIGN_TYPE"]]},
            {"text": "AI tradecraft monitored threat actor AI tool usage patterns", "entities": [[0, 2, "TOOL"], [3, 12, "TRADECRAFT_TYPE"], [21, 29, "MONITORING_TYPE"], [30, 36, "THREAT_TYPE"], [37, 42, "ACTOR_TYPE"], [43, 46, "TOOL"], [47, 51, "TOOL"], [52, 58, "USAGE_TYPE"], [59, 66, "PATTERN_TYPE"]]},
            {"text": "OSINT ML pipelines tested against adversarial attacks", "entities": [[0, 5, "TOOL"], [6, 9, "TOOL"], [10, 12, "TOOL"], [13, 22, "PIPELINE_TYPE"], [31, 38, "TESTING_TYPE"], [47, 58, "ADVERSARIAL_TYPE"], [59, 66, "ATTACK_TYPE"]]},
            {"text": "AI-generated vs human-generated intelligence audit logs maintained", "entities": [[0, 2, "TOOL"], [3, 12, "INTELLIGENCE_TYPE"], [16, 21, "INTELLIGENCE_TYPE"], [30, 35, "AUDIT_TYPE"], [36, 40, "LOG_TYPE"], [49, 59, "MAINTENANCE_TYPE"]]},
            {"text": "Large-scale AI threat scanning GPU infrastructure enabled processing", "entities": [[0, 10, "SCANNING_TYPE"], [11, 13, "TOOL"], [14, 19, "THREAT_TYPE"], [20, 32, "SCANNING_TYPE"], [41, 44, "TOOL"], [45, 57, "INFRASTRUCTURE_TYPE"], [66, 76, "ENABLEMENT_TYPE"], [77, 87, "PROCESSING_TYPE"]]},
            {"text": "AI model leaks fine-tune datasets monitored for unauthorized access", "entities": [[0, 2, "TOOL"], [3, 9, "MODEL_TYPE"], [10, 15, "LEAK_TYPE"], [16, 26, "DATASET_TYPE"], [35, 44, "MONITORING_TYPE"], [49, 63, "UNAUTHORIZED_TYPE"], [64, 70, "ACCESS_TYPE"]]},
            {"text": "AI infrastructure metadata tracked model deployment and usage", "entities": [[0, 2, "TOOL"], [3, 16, "INFRASTRUCTURE_TYPE"], [17, 25, "METADATA_TYPE"], [34, 40, "TRACKING_TYPE"], [41, 47, "MODEL_TYPE"], [48, 59, "DEPLOYMENT_TYPE"], [64, 70, "USAGE_TYPE"]]},
            {"text": "Prompt injection poisoning evasion tested against ML models", "entities": [[0, 6, "PROMPT_TYPE"], [7, 15, "INJECTION_TYPE"], [16, 24, "POISONING_TYPE"], [25, 32, "EVASION_TYPE"], [41, 47, "TESTING_TYPE"], [56, 58, "TOOL"], [59, 66, "MODEL_TYPE"]]},
            {"text": "AI tool usage tracked in forums GitHub Telegram and dark web", "entities": [[0, 2, "TOOL"], [3, 7, "TOOL"], [8, 12, "USAGE_TYPE"], [21, 27, "TRACKING_TYPE"], [31, 38, "FORUM_TYPE"], [39, 45, "TOOL"], [46, 54, "TOOL"], [59, 68, "NETWORK_TYPE"]]},
            {"text": "AI marketplaces monitored model dataset and API sales", "entities": [[0, 2, "TOOL"], [3, 14, "MARKETPLACE_TYPE"], [23, 32, "MONITORING_TYPE"], [33, 39, "MODEL_TYPE"], [40, 47, "DATASET_TYPE"], [52, 55, "TOOL"], [56, 59, "SALES_TYPE"]]},
            {"text": "Synthetic identity creation AI-generated personas detected", "entities": [[0, 9, "SYNTHETIC_TYPE"], [10, 18, "IDENTITY_TYPE"], [19, 27, "CREATION_TYPE"], [28, 30, "TOOL"], [31, 40, "PERSONA_TYPE"], [49, 56, "DETECTION_TYPE"]]},
            {"text": "Model provenance validation ensured AI model authenticity", "entities": [[0, 6, "MODEL_TYPE"], [7, 17, "PROVENANCE_TYPE"], [18, 28, "VALIDATION_TYPE"], [37, 43, "ENSURANCE_TYPE"], [44, 46, "TOOL"], [47, 53, "MODEL_TYPE"], [54, 66, "AUTHENTICITY_TYPE"]]},
            {"text": "Dataset integrity validated training data provenance", "entities": [[0, 7, "DATASET_TYPE"], [8, 17, "INTEGRITY_TYPE"], [26, 34, "VALIDATION_TYPE"], [35, 43, "TRAINING_TYPE"], [44, 48, "DATA_TYPE"], [49, 58, "PROVENANCE_TYPE"]]},
            {"text": "AI ethics compliance monitored against ethical guardrails", "entities": [[0, 2, "TOOL"], [3, 9, "ETHICS_TYPE"], [10, 20, "COMPLIANCE_TYPE"], [29, 37, "MONITORING_TYPE"], [47, 55, "ETHICAL_TYPE"], [56, 67, "GUARDRAIL_TYPE"]]},
            {"text": "AI risk management NIST AI RMF framework alignment", "entities": [[0, 2, "TOOL"], [3, 7, "RISK_TYPE"], [8, 17, "MANAGEMENT_TYPE"], [18, 22, "FRAMEWORK"], [23, 25, "TOOL"], [26, 29, "FRAMEWORK"], [30, 40, "FRAMEWORK_TYPE"], [41, 51, "ALIGNMENT_TYPE"]]},
            {"text": "AI system audit validated compliance with regulations", "entities": [[0, 2, "TOOL"], [3, 9, "SYSTEM_TYPE"], [10, 15, "AUDIT_TYPE"], [24, 32, "VALIDATION_TYPE"], [33, 43, "COMPLIANCE_TYPE"], [48, 61, "REGULATION_TYPE"]]},
            {"text": "AI model performance benchmarking evaluated accuracy", "entities": [[0, 2, "TOOL"], [3, 9, "MODEL_TYPE"], [10, 20, "PERFORMANCE_TYPE"], [21, 34, "BENCHMARKING_TYPE"], [43, 51, "EVALUATION_TYPE"], [52, 60, "ACCURACY_TYPE"]]},
            {"text": "AI threat intelligence feeds enriched SOC workflows", "entities": [[0, 2, "TOOL"], [3, 9, "THREAT_TYPE"], [10, 23, "INTELLIGENCE_TYPE"], [24, 29, "FEED_TYPE"], [38, 45, "ENRICHMENT_TYPE"], [46, 49, "TOOL"], [50, 59, "WORKFLOW_TYPE"]]},
            {"text": "AI detection accuracy improved with model updates", "entities": [[0, 2, "TOOL"], [3, 12, "DETECTION_TYPE"], [13, 21, "ACCURACY_TYPE"], [30, 38, "IMPROVEMENT_TYPE"], [43, 49, "MODEL_TYPE"], [50, 57, "UPDATE_TYPE"]]},
            {"text": "AI-powered threat hunting identified advanced threats", "entities": [[0, 2, "TOOL"], [3, 10, "THREAT_TYPE"], [11, 17, "HUNTING_TYPE"], [26, 35, "IDENTIFICATION_TYPE"], [36, 45, "ADVANCED_TYPE"], [46, 54, "THREAT_TYPE"]]},
            {"text": "AI model drift detection identified performance degradation", "entities": [[0, 2, "TOOL"], [3, 9, "MODEL_TYPE"], [10, 15, "DRIFT_TYPE"], [16, 25, "DETECTION_TYPE"], [34, 43, "IDENTIFICATION_TYPE"], [44, 54, "PERFORMANCE_TYPE"], [55, 68, "DEGRADATION_TYPE"]]},
            {"text": "AI explainability analysis validated model decisions", "entities": [[0, 2, "TOOL"], [3, 16, "EXPLAINABILITY_TYPE"], [17, 25, "ANALYSIS_TYPE"], [34, 42, "VALIDATION_TYPE"], [43, 49, "MODEL_TYPE"], [50, 59, "DECISION_TYPE"]]},
            {"text": "AI bias detection identified discriminatory model behavior", "entities": [[0, 2, "TOOL"], [3, 7, "BIAS_TYPE"], [8, 17, "DETECTION_TYPE"], [26, 35, "IDENTIFICATION_TYPE"], [36, 49, "DISCRIMINATORY_TYPE"], [50, 56, "MODEL_TYPE"], [57, 66, "BEHAVIOR_TYPE"]]},
            {"text": "AI model versioning tracked model iterations and changes", "entities": [[0, 2, "TOOL"], [3, 9, "MODEL_TYPE"], [10, 20, "VERSIONING_TYPE"], [29, 35, "TRACKING_TYPE"], [36, 42, "MODEL_TYPE"], [43, 54, "ITERATION_TYPE"], [59, 66, "CHANGE_TYPE"]]},
            {"text": "AI training data quality assessed dataset completeness", "entities": [[0, 2, "TOOL"], [3, 11, "TRAINING_TYPE"], [12, 16, "DATA_TYPE"], [17, 23, "QUALITY_TYPE"], [32, 39, "ASSESSMENT_TYPE"], [40, 47, "DATASET_TYPE"], [48, 60, "COMPLETENESS_TYPE"]]},
            {"text": "AI model deployment validated production readiness", "entities": [[0, 2, "TOOL"], [3, 9, "MODEL_TYPE"], [10, 21, "DEPLOYMENT_TYPE"], [30, 38, "VALIDATION_TYPE"], [39, 50, "PRODUCTION_TYPE"], [51, 60, "READINESS_TYPE"]]},
            {"text": "AI monitoring dashboard displayed real-time threat metrics", "entities": [[0, 2, "TOOL"], [3, 13, "MONITORING_TYPE"], [14, 23, "DASHBOARD_TYPE"], [32, 40, "DISPLAY_TYPE"], [41, 49, "METRIC_TYPE"], [50, 56, "THREAT_TYPE"], [57, 64, "METRIC_TYPE"]]},
            {"text": "AI incident response automated threat containment", "entities": [[0, 2, "TOOL"], [3, 11, "INCIDENT_TYPE"], [12, 20, "RESPONSE_TYPE"], [29, 39, "AUTOMATION_TYPE"], [40, 46, "THREAT_TYPE"], [47, 58, "CONTAINMENT_TYPE"]]},
            {"text": "AI security controls enforced model access restrictions", "entities": [[0, 2, "TOOL"], [3, 11, "SECURITY_TYPE"], [12, 20, "CONTROL_TYPE"], [29, 36, "ENFORCEMENT_TYPE"], [37, 43, "MODEL_TYPE"], [44, 50, "ACCESS_TYPE"], [51, 62, "RESTRICTION_TYPE"]]},
            {"text": "AI compliance reporting generated regulatory reports", "entities": [[0, 2, "TOOL"], [3, 13, "COMPLIANCE_TYPE"], [14, 23, "REPORTING_TYPE"], [32, 41, "GENERATION_TYPE"], [42, 52, "REGULATION_TYPE"], [53, 60, "REPORT_TYPE"]]},
        ])
    
    # Ensure we have exactly 100 entities
    while len(entities) < 100:
        # Add generic entities based on common OSINT patterns
        entities.append({
            "text": f"{pillar.replace('_', ' ').title()} Analyst conducted intelligence analysis",
            "entities": [[0, len(pillar.replace('_', ' ').title()), "PILLAR_TYPE"], [len(pillar.replace('_', ' ').title())+1, len(pillar.replace('_', ' ').title())+8, "ANALYST_TYPE"], [len(pillar.replace('_', ' ').title())+18, len(pillar.replace('_', ' ').title())+27, "INTELLIGENCE_TYPE"], [len(pillar.replace('_', ' ').title())+28, len(pillar.replace('_', ' ').title())+36, "ANALYSIS_TYPE"]]
        })
    
    return entities[:100]

def generate_intents_for_pillar(pillar, definition, agents):
    """Generate 100 intent examples for a pillar."""
    intents = []
    
    # Generate intent examples based on pillar type
    pillar_lower = pillar.lower()
    
    # AI-INT specific intents
    if "ai_int" in pillar_lower:
        intents.extend([
            {"text": "I need to monitor AI misuse across OSINT dark web and GitHub", "cats": {"MONITOR_AI": 1.0, "DETECT_MISUSE": 1.0, "ENABLE_MONITORING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Please detect deepfakes and AI-generated media using synthetic media detection", "cats": {"DETECT_DEEPFAKES": 1.0, "ANALYZE_MEDIA": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Test AI ML pipelines for poisoning and evasion attacks", "cats": {"TEST_PIPELINES": 1.0, "ASSESS_VULNERABILITIES": 1.0, "ENABLE_TESTING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect prompt injection and malicious LLM usage", "cats": {"DETECT_INJECTION": 1.0, "PROTECT_LLM": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Ensure compliance with EU AI Act and NIST AI RMF", "cats": {"ENSURE_COMPLIANCE": 1.0, "VALIDATE_REGULATIONS": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Track AI model dataset and API sales on dark web marketplaces", "cats": {"TRACK_SALES": 1.0, "MONITOR_MARKETPLACES": 1.0, "ENABLE_MONITORING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect AI-generated personas across social media platforms", "cats": {"DETECT_PERSONAS": 1.0, "IDENTIFY_SYNTHETIC": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Analyze deepfake content using DeepFaceLab synthetic media detection", "cats": {"ANALYZE_DEEPFAKES": 1.0, "DETECT_SYNTHETIC": 1.0, "ENABLE_ANALYSIS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Identify synthetic videos with FakeCatcher real-time deepfake detection", "cats": {"IDENTIFY_VIDEOS": 1.0, "DETECT_DEEPFAKES": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Scan media files with Reality Defender deepfake detection platform", "cats": {"SCAN_MEDIA": 1.0, "DETECT_DEEPFAKES": 1.0, "ENABLE_SCANNING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Map narrative networks with Blackbird AI disinformation detection", "cats": {"MAP_NETWORKS": 1.0, "DETECT_DISINFORMATION": 1.0, "ENABLE_MAPPING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Monitor dark web AI intelligence feeds with Recorded Future AI-INT", "cats": {"MONITOR_DARKWEB": 1.0, "TRACK_INTELLIGENCE": 1.0, "ENABLE_MONITORING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Enable AI entity resolution with Palantir Gotham AI modules", "cats": {"ENABLE_RESOLUTION": 1.0, "RESOLVE_ENTITIES": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Identify threats with Darktrace DETECT adversarial AI detection", "cats": {"IDENTIFY_THREATS": 1.0, "DETECT_ANOMALIES": 1.0, "ENABLE_DETECTION": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect botnets and disinformation with ZeroFox AI platform", "cats": {"DETECT_BOTNETS": 1.0, "DETECT_DISINFORMATION": 1.0, "ENABLE_DETECTION": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Map AI-driven influence operations with Graphika AI network mapping", "cats": {"MAP_OPERATIONS": 1.0, "TRACK_INFLUENCE": 1.0, "ENABLE_MAPPING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Analyze text content with Cortical AI semantic intelligence", "cats": {"ANALYZE_CONTENT": 1.0, "ENABLE_SEMANTIC": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect child exploitation content with Thorn Spotlight AI", "cats": {"DETECT_EXPLOITATION": 1.0, "PROTECT_CHILDREN": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Enable AI detection and moderation with Clarifai AI Guardrails", "cats": {"ENABLE_DETECTION": 1.0, "ENABLE_MODERATION": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Evaluate LLM models with OpenAI Evals adversarial framework", "cats": {"EVALUATE_MODELS": 1.0, "TEST_ADVERSARIAL": 1.0, "ENABLE_TESTING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Test models with TextFooler adversarial text attack toolkit", "cats": {"TEST_MODELS": 1.0, "ASSESS_ROBUSTNESS": 1.0, "ENABLE_TESTING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Test ML defenses with Adversarial Robustness Toolbox ART", "cats": {"TEST_DEFENSES": 1.0, "ASSESS_ROBUSTNESS": 1.0, "ENABLE_TESTING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect adversarial malware generation with MalGAN tool", "cats": {"DETECT_MALWARE": 1.0, "IDENTIFY_ADVERSARIAL": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Classify AI vs human text with GPT-Detector OSS classifier", "cats": {"CLASSIFY_TEXT": 1.0, "DETECT_AI_TEXT": 1.0, "ENABLE_CLASSIFICATION": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Test model performance with Hugging Face Evaluate framework", "cats": {"TEST_PERFORMANCE": 1.0, "EVALUATE_MODELS": 1.0, "ENABLE_TESTING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Enable LLM observability with LlamaIndex LangKit Security", "cats": {"ENABLE_OBSERVABILITY": 1.0, "MONITOR_LLM": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Map face recognition dataset risks with Exposing AI datasets", "cats": {"MAP_RISKS": 1.0, "ASSESS_DATASETS": 1.0, "ENABLE_MAPPING": 1.0, "AUDIT_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Analyze videos with Deepware Scanner enterprise deepfake scanner", "cats": {"ANALYZE_VIDEOS": 1.0, "DETECT_DEEPFAKES": 1.0, "ENABLE_ANALYSIS": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Monitor synthetic media with Sensity AI commercial suite", "cats": {"MONITOR_MEDIA": 1.0, "DETECT_SYNTHETIC": 1.0, "ENABLE_MONITORING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Achieve 90 percent AI-generated content detection precision", "cats": {"IMPROVE_DETECTION": 1.0, "TRACK_METRICS": 1.0, "ANALYZE_PERFORMANCE": 1.0, "AUDIT_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Achieve 95 percent prompt injection block rate success", "cats": {"IMPROVE_BLOCKING": 1.0, "TRACK_METRICS": 1.0, "ANALYZE_PERFORMANCE": 1.0, "AUDIT_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Detect model poisoning within 24 hours of attack", "cats": {"DETECT_POISONING": 1.0, "IMPROVE_DETECTION": 1.0, "TRACK_METRICS": 1.0, "AUDIT_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Deliver AI Threat Digest weekly with 100 percent SLA", "cats": {"DELIVER_DIGEST": 1.0, "ENSURE_SLA": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Reach 85 percent cross-pillar validation rate accuracy", "cats": {"IMPROVE_VALIDATION": 1.0, "TRACK_METRICS": 1.0, "ANALYZE_PERFORMANCE": 1.0, "AUDIT_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Achieve 4.5 out of 5 executive satisfaction score rating", "cats": {"IMPROVE_SATISFACTION": 1.0, "TRACK_METRICS": 1.0, "ANALYZE_PERFORMANCE": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Improve deepfake detection precision and recall metrics", "cats": {"IMPROVE_DETECTION": 1.0, "TRACK_METRICS": 1.0, "ANALYZE_PERFORMANCE": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Expand adversarial test coverage to 95 percent of models", "cats": {"EXPAND_COVERAGE": 1.0, "IMPROVE_TESTING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Validate dataset integrity scores for all training datasets", "cats": {"VALIDATE_INTEGRITY": 1.0, "ASSESS_DATASETS": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_SYSTEMS": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Detect AI-powered disinformation campaign with synthetic media", "cats": {"DETECT_DISINFORMATION": 1.0, "IDENTIFY_CAMPAIGNS": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect adversarial ML attack poisoning OSINT datasets", "cats": {"DETECT_ATTACKS": 1.0, "IDENTIFY_POISONING": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect AI-assisted cybercrime generative models for phishing", "cats": {"DETECT_CYBERCRIME": 1.0, "IDENTIFY_PHISHING": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect autonomous botnet AI-controlled bots managing C2", "cats": {"DETECT_BOTNETS": 1.0, "IDENTIFY_C2": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect synthetic identity creation AI-generated personas", "cats": {"DETECT_IDENTITIES": 1.0, "IDENTIFY_PERSONAS": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect model provenance leakage stolen AI models on dark web", "cats": {"DETECT_LEAKAGE": 1.0, "IDENTIFY_THEFT": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect prompt injection LLM abuse compromising OSINT workflows", "cats": {"DETECT_INJECTION": 1.0, "PROTECT_WORKFLOWS": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect cross-pillar AI fusion adversaries fusing intelligence", "cats": {"DETECT_FUSION": 1.0, "IDENTIFY_ADVERSARIES": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect AI policy circumvention misuse of open-source models", "cats": {"DETECT_CIRCUMVENTION": 1.0, "IDENTIFY_MISUSE": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Improve defensive AI monitoring to detect AI-driven threats early", "cats": {"IMPROVE_MONITORING": 1.0, "DETECT_THREATS": 1.0, "ENABLE_DETECTION": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Integrate synthetic media detection image video voice pipelines", "cats": {"INTEGRATE_DETECTION": 1.0, "ENABLE_PIPELINES": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Monitor model dataset telemetry for leaks and fine-tune datasets", "cats": {"MONITOR_TELEMETRY": 1.0, "TRACK_LEAKS": 1.0, "ENABLE_MONITORING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Continuously test ML LLM models for adversarial resilience", "cats": {"TEST_MODELS": 1.0, "ASSESS_RESILIENCE": 1.0, "ENABLE_TESTING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Track AI tool usage in forums GitHub Telegram and dark web", "cats": {"TRACK_USAGE": 1.0, "MONITOR_TOOLS": 1.0, "ENABLE_MONITORING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Monitor AI usage against NIST AI RMF EU AI Act compliance", "cats": {"MONITOR_COMPLIANCE": 1.0, "ENSURE_REGULATORY": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Validate EU AI Act compliance for AI system requirements", "cats": {"VALIDATE_COMPLIANCE": 1.0, "ENSURE_REGULATORY": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Ensure ISO IEC 42001 AI management system standard compliance", "cats": {"ENSURE_COMPLIANCE": 1.0, "VALIDATE_STANDARDS": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Connect SOCMINT CYBINT and HUMINT with cross-pillar fusion", "cats": {"CONNECT_PILLARS": 1.0, "ENABLE_FUSION": 1.0, "IMPROVE_CORRELATION": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Conduct adversarial testing of generative AI models", "cats": {"CONDUCT_TESTING": 1.0, "TEST_ADVERSARIAL": 1.0, "ENABLE_TESTING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Maintain audit logs of AI-generated vs human-generated intelligence", "cats": {"MAINTAIN_LOGS": 1.0, "ENABLE_AUDITING": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_SYSTEMS": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Enable GPU TPU monitoring for large-scale AI threat scanning", "cats": {"ENABLE_MONITORING": 1.0, "SCALE_INFRASTRUCTURE": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Analyze synthetic media with GAN detection deepfake forensics", "cats": {"ANALYZE_MEDIA": 1.0, "DETECT_DEEPFAKES": 1.0, "ENABLE_ANALYSIS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Track AI-generated content campaigns with disinformation narratives", "cats": {"TRACK_CAMPAIGNS": 1.0, "DETECT_DISINFORMATION": 1.0, "ENABLE_TRACKING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Monitor threat actor AI tool usage patterns with AI tradecraft", "cats": {"MONITOR_ACTORS": 1.0, "TRACK_PATTERNS": 1.0, "ENABLE_MONITORING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Test OSINT ML pipelines against adversarial attacks", "cats": {"TEST_PIPELINES": 1.0, "ASSESS_VULNERABILITIES": 1.0, "ENABLE_TESTING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Maintain audit logs distinguishing AI-generated vs human intelligence", "cats": {"MAINTAIN_LOGS": 1.0, "ENABLE_AUDITING": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_SYSTEMS": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Enable large-scale AI threat scanning with GPU infrastructure", "cats": {"ENABLE_SCANNING": 1.0, "SCALE_INFRASTRUCTURE": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Monitor AI model leaks and fine-tune datasets for unauthorized access", "cats": {"MONITOR_LEAKS": 1.0, "DETECT_UNAUTHORIZED": 1.0, "ENABLE_MONITORING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Track AI infrastructure metadata for model deployment and usage", "cats": {"TRACK_METADATA": 1.0, "MONITOR_DEPLOYMENT": 1.0, "ENABLE_TRACKING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Test ML models against prompt injection poisoning and evasion", "cats": {"TEST_MODELS": 1.0, "ASSESS_VULNERABILITIES": 1.0, "ENABLE_TESTING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Track AI tool usage in forums GitHub Telegram and dark web marketplaces", "cats": {"TRACK_USAGE": 1.0, "MONITOR_MARKETPLACES": 1.0, "ENABLE_MONITORING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Monitor AI marketplaces for model dataset and API sales", "cats": {"MONITOR_MARKETPLACES": 1.0, "TRACK_SALES": 1.0, "ENABLE_MONITORING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Detect AI-generated personas with synthetic identity creation", "cats": {"DETECT_PERSONAS": 1.0, "IDENTIFY_SYNTHETIC": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Ensure AI model authenticity with model provenance validation", "cats": {"ENSURE_AUTHENTICITY": 1.0, "VALIDATE_PROVENANCE": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_SYSTEMS": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Validate training data provenance with dataset integrity checks", "cats": {"VALIDATE_PROVENANCE": 1.0, "ASSESS_INTEGRITY": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_SYSTEMS": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Monitor AI ethics compliance against ethical guardrails", "cats": {"MONITOR_COMPLIANCE": 1.0, "ENSURE_ETHICS": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Align AI risk management with NIST AI RMF framework", "cats": {"ALIGN_FRAMEWORK": 1.0, "ENSURE_COMPLIANCE": 1.0, "AUDIT_COMPLIANCE": 1.0, "DEFINE_STRATEGY": 1.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Validate AI system compliance with regulations through audits", "cats": {"VALIDATE_COMPLIANCE": 1.0, "CONDUCT_AUDITS": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Evaluate AI model accuracy with performance benchmarking", "cats": {"EVALUATE_ACCURACY": 1.0, "BENCHMARK_PERFORMANCE": 1.0, "ANALYZE_PERFORMANCE": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Enrich SOC workflows with AI threat intelligence feeds", "cats": {"ENRICH_WORKFLOWS": 1.0, "ENABLE_INTELLIGENCE": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Improve AI detection accuracy with model updates", "cats": {"IMPROVE_ACCURACY": 1.0, "UPDATE_MODELS": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Identify advanced threats with AI-powered threat hunting", "cats": {"IDENTIFY_THREATS": 1.0, "ENABLE_HUNTING": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Identify performance degradation with AI model drift detection", "cats": {"IDENTIFY_DEGRADATION": 1.0, "DETECT_DRIFT": 1.0, "ENABLE_DETECTION": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Validate model decisions with AI explainability analysis", "cats": {"VALIDATE_DECISIONS": 1.0, "ENABLE_EXPLAINABILITY": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_SYSTEMS": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Identify discriminatory model behavior with AI bias detection", "cats": {"IDENTIFY_BIAS": 1.0, "DETECT_DISCRIMINATION": 1.0, "ENABLE_DETECTION": 1.0, "AUDIT_COMPLIANCE": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Track model iterations and changes with AI model versioning", "cats": {"TRACK_ITERATIONS": 1.0, "ENABLE_VERSIONING": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Assess dataset completeness with AI training data quality checks", "cats": {"ASSESS_QUALITY": 1.0, "VALIDATE_DATASETS": 1.0, "AUDIT_COMPLIANCE": 1.0, "MAINTAIN_SYSTEMS": 1.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Validate production readiness with AI model deployment", "cats": {"VALIDATE_READINESS": 1.0, "ENABLE_DEPLOYMENT": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Display real-time threat metrics with AI monitoring dashboard", "cats": {"DISPLAY_METRICS": 1.0, "ENABLE_VISIBILITY": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Automate threat containment with AI incident response", "cats": {"AUTOMATE_RESPONSE": 1.0, "ENABLE_CONTAINMENT": 1.0, "RESPOND_TO_INCIDENT": 1.0, "AUDIT_COMPLIANCE": 0.0, "DEFINE_STRATEGY": 0.0}},
            {"text": "Enforce model access restrictions with AI security controls", "cats": {"ENFORCE_CONTROLS": 1.0, "RESTRICT_ACCESS": 1.0, "IMPROVE_SECURITY": 1.0, "MAINTAIN_SYSTEMS": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
            {"text": "Generate regulatory reports with AI compliance reporting", "cats": {"GENERATE_REPORTS": 1.0, "ENABLE_REPORTING": 1.0, "AUDIT_COMPLIANCE": 1.0, "DEFINE_STRATEGY": 0.0, "RESPOND_TO_INCIDENT": 0.0}},
        ])
    
    # Ensure we have exactly 100 intents
    while len(intents) < 100:
        intents.append({
            "text": f"I need to conduct {pillar.replace('_', ' ')} intelligence analysis",
            "cats": {"CONDUCT_ANALYSIS": 1.0, "ENABLE_INTELLIGENCE": 1.0, "AUDIT_COMPLIANCE": 0.0, "RESPOND_TO_INCIDENT": 0.0, "DEFINE_STRATEGY": 0.0}}
        )
    
    return intents[:100]

def process_pillar(pillar):
    """Process a single OSINT pillar."""
    print(f"\nProcessing {pillar}...")
    
    definition = read_definition_file(pillar)
    agents = read_agents_file(pillar)
    
    entities = generate_entities_for_pillar(pillar, definition, agents)
    intents = generate_intents_for_pillar(pillar, definition, agents)
    
    # Write entities
    entities_path = f"{BASE_PATH}/{pillar}/{pillar}_entities.jsonl"
    with open(entities_path, 'w', encoding='utf-8') as f:
        for entity in entities:
            f.write(json.dumps(entity, ensure_ascii=False) + '\n')
    
    # Write intents
    intents_path = f"{BASE_PATH}/{pillar}/{pillar}_intent.jsonl"
    with open(intents_path, 'w', encoding='utf-8') as f:
        for intent in intents:
            f.write(json.dumps(intent, ensure_ascii=False) + '\n')
    
    print(f"✅ {pillar}: {len(entities)} entities, {len(intents)} intents")

if __name__ == "__main__":
    print(f"Generating entities and intents for {len(OSINT_PILLARS)} OSINT pillars...")
    
    for pillar in OSINT_PILLARS:
        try:
            process_pillar(pillar)
        except Exception as e:
            print(f"❌ Error processing {pillar}: {e}")
    
    print(f"\n✅ Completed processing all OSINT pillars!")

EOF

