#!/usr/bin/env python3
"""
Generate comprehensive test cases for production-quality test suite.
This script creates 200+ test cases covering all entity types, edge cases, and scenarios.
"""

def get_comprehensive_test_cases():
    """
    Generate comprehensive test cases covering:
    - All entity types (578 types)
    - Edge cases and boundary conditions
    - Negative test cases (true negatives)
    - Format variations
    - Security-specific scenarios
    - Production-ready coverage
    """
    
    test_cases = [
        # ========== EXISTING TEST CASES (30) - KEEPING FOR COMPATIBILITY ==========
        {
            "text": "Can you help me investigate this suspicious IP address 192.168.1.100?",
            "category": "natural_language",
            "expected_entities": [("192.168.1.100", "IP_ADDRESS")],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "I need to check if the domain example.com is safe",
            "category": "natural_language",
            "expected_entities": [("example.com", "DOMAIN")],
            "expected_intents": ["CHECK", "VALIDATE"]
        },
        {
            "text": "APT41 CVE-2021-44228 Log4j vulnerability exploitation detected on 10.0.0.5",
            "category": "technical",
            "expected_entities": [
                ("APT41", "THREAT_ACTOR"),
                ("CVE-2021-44228", "CVE_ID"),
                ("10.0.0.5", "IP_ADDRESS")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "Perform memory forensics on host server-01.internal.com port 443",
            "category": "technical",
            "expected_entities": [
                ("server-01.internal.com", "HOST_TYPE"),
                ("443", "PORT")
            ],
            "expected_intents": ["PERFORM_MEMORY_FORENSICS", "ANALYZE"]
        },
        {
            "text": "hey what's up with that malware thing?",
            "category": "casual",
            "expected_intents": ["INVESTIGATE", "ANALYZE"]
        },
        {
            "text": "can u check this ip 8.8.8.8 pls?",
            "category": "casual",
            "expected_entities": [("8.8.8.8", "IP_ADDRESS")],
            "expected_intents": ["CHECK", "VALIDATE"]
        },
        {
            "text": "APT28 used WannaCry ransomware to attack IP 172.16.0.1 and domain evil.com on port 8080",
            "category": "multi_entity",
            "expected_entities": [
                ("APT28", "THREAT_ACTOR"),
                ("WannaCry", "MALWARE_TYPE"),
                ("172.16.0.1", "IP_ADDRESS"),
                ("evil.com", "DOMAIN"),
                ("8080", "PORT")
            ],
            "expected_intents": ["INVESTIGATE", "DETECT"]
        },
        {
            "text": "Incident INC-2024-001 occurred on 2024-11-30 at 14:30 UTC involving user admin@company.com",
            "category": "multi_entity",
            "expected_entities": [
                ("INC-2024-001", "INCIDENT_ID"),
                ("2024-11-30", "DATE"),
                ("14:30", "TIME"),
                ("admin@company.com", "EMAIL_ADDRESS")
            ],
            "expected_intents": ["INVESTIGATE", "DOCUMENT_INCIDENT"]
        },
        {
            "text": "Verify the authenticity of this image and check the GPS coordinates latitude 40.7128 longitude -74.0060",
            "category": "osint",
            "expected_entities": [
                ("40.7128", "LATITUDE"),
                ("-74.0060", "LONGITUDE")
            ],
            "expected_intents": ["VERIFY", "VALIDATE", "CHECK"]
        },
        {
            "text": "Track the social media account @suspicious_user across Twitter, Facebook, and LinkedIn",
            "category": "osint",
            "expected_entities": [
                ("@suspicious_user", "USERNAME"),
                ("Twitter", "PLATFORM"),
                ("Facebook", "PLATFORM"),
                ("LinkedIn", "PLATFORM")
            ],
            "expected_intents": ["TRACK", "MONITOR"]
        },
        {
            "text": "Execute incident response playbook for ransomware containment and isolate affected systems",
            "category": "cybersecurity",
            "expected_intents": ["RESPOND_TO_INCIDENT", "ISOLATE_ASSETS", "EXECUTE_PLAYBOOK"]
        },
        {
            "text": "Hunt for lateral movement indicators and privilege escalation attempts in the environment",
            "category": "cybersecurity",
            "expected_intents": ["HUNT", "DETECT", "INVESTIGATE"]
        },
        {
            "text": "I need to investigate the data breach, analyze the malware sample, and generate a report for the compliance team by tomorrow",
            "category": "complex",
            "expected_intents": ["INVESTIGATE", "ANALYZE", "GENERATE_REPORTS", "ENSURE_COMPLIANCE"]
        },
        {
            "text": "Monitor network traffic, detect anomalies, correlate with threat intelligence, and escalate if severity is high",
            "category": "complex",
            "expected_intents": ["MONITOR", "DETECT_ANOMALIES", "CORRELATE_EVENTS", "ESCALATE_INCIDENT"]
        },
        {
            "text": "test",
            "category": "edge_case_short",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "This is a very long query that contains multiple sentences and should test how the model handles longer inputs with various types of information including IP addresses like 192.168.1.1, domains like example.com, and various technical terms that might appear in cybersecurity or OSINT contexts.",
            "category": "edge_case_long",
            "expected_entities": [
                ("192.168.1.1", "IP_ADDRESS"),
                ("example.com", "DOMAIN")
            ]
        },
        {
            "text": "Check IP: 10.0.0.1, Domain: test.com, Email: user@test.com, Phone: +1-555-123-4567",
            "category": "edge_case_formatted",
            "expected_entities": [
                ("10.0.0.1", "IP_ADDRESS"),
                ("test.com", "DOMAIN"),
                ("user@test.com", "EMAIL_ADDRESS"),
                ("+1-555-123-4567", "PHONE_NUMBER")
            ]
        },
        {
            "text": "What is the threat level for IP address 203.0.113.0?",
            "category": "question_format",
            "expected_entities": [("203.0.113.0", "IP_ADDRESS")],
            "expected_intents": ["ASSESS_RISK", "INVESTIGATE"]
        },
        {
            "text": "How do I investigate this security incident?",
            "category": "question_format",
            "expected_intents": ["INVESTIGATE", "RESPOND_TO_INCIDENT"]
        },
        {
            "text": "Block IP 192.168.1.50 and isolate host server-02",
            "category": "command_format",
            "expected_entities": [
                ("192.168.1.50", "IP_ADDRESS"),
                ("server-02", "HOST_TYPE")
            ],
            "expected_intents": ["BLOCK_IPS", "ISOLATE_ASSETS"]
        },
        {
            "text": "Generate threat intelligence report for APT29 campaign",
            "category": "command_format",
            "expected_entities": [("APT29", "THREAT_ACTOR")],
            "expected_intents": ["GENERATE_REPORTS", "GATHER_INTELLIGENCE"]
        },
        {
            "text": "Cross-reference OSINT data from social media with cybersecurity threat intelligence to identify the threat actor",
            "category": "mixed_domains",
            "expected_intents": ["CORRELATE_EVENTS", "IDENTIFY_THREAT_ACTOR", "GATHER_INTELLIGENCE"]
        },
        {
            "text": "Verify the source of the leaked document and check if it contains any PII or sensitive data",
            "category": "mixed_domains",
            "expected_intents": ["VERIFY", "CHECK", "DETECT_PII"]
        },
        {
            "text": "Show me all security events from the last 24 hours",
            "category": "time_based",
            "expected_intents": ["MONITOR", "ANALYZE", "GENERATE_REPORTS"]
        },
        {
            "text": "What happened on November 30, 2024 at 3:00 PM?",
            "category": "time_based",
            "expected_entities": [
                ("November 30, 2024", "DATE"),
                ("3:00 PM", "TIME")
            ],
            "expected_intents": ["INVESTIGATE", "ANALYZE"]
        },
        {
            "text": "Find all activities from coordinates 37.7749, -122.4194 in San Francisco",
            "category": "geographic",
            "expected_entities": [
                ("37.7749", "LATITUDE"),
                ("-122.4194", "LONGITUDE"),
                ("San Francisco", "LOCATION")
            ],
            "expected_intents": ["INVESTIGATE", "MAP", "TRACK"]
        },
        {
            "text": "Generate compliance report for GDPR audit covering data privacy and protection measures",
            "category": "compliance",
            "expected_intents": ["GENERATE_REPORTS", "ENSURE_COMPLIANCE", "AUDIT_COMPLIANCE"]
        },
        {
            "text": "Check if our security controls meet ISO 27001 requirements",
            "category": "compliance",
            "expected_entities": [("ISO 27001", "COMPLIANCE_FRAMEWORK")],
            "expected_intents": ["CHECK", "ENSURE_COMPLIANCE", "AUDIT_COMPLIANCE"]
        },
        {
            "text": "Scan for CVE-2021-44228 and CVE-2021-45046 vulnerabilities in our systems",
            "category": "vulnerability",
            "expected_entities": [
                ("CVE-2021-44228", "CVE_ID"),
                ("CVE-2021-45046", "CVE_ID")
            ],
            "expected_intents": ["SCAN", "DETECT", "ASSESS_RISK"]
        },
        {
            "text": "Track cryptocurrency wallet address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb and monitor transactions",
            "category": "financial_osint",
            "expected_entities": [
                ("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "WALLET_ADDRESS")
            ],
            "expected_intents": ["TRACK", "MONITOR"]
        },
        
        # ========== SOCIAL MEDIA ENTITIES (10 tests) ==========
        {
            "text": "Monitor Instagram account @suspicious_user123 and check posts",
            "category": "social_media_instagram",
            "expected_entities": [("@suspicious_user123", "INSTAGRAM_USERNAME")],
            "expected_intents": ["MONITOR", "INVESTIGATE"]
        },
        {
            "text": "Check Instagram profile at https://instagram.com/malicious_account",
            "category": "social_media_instagram",
            "expected_entities": [("https://instagram.com/malicious_account", "INSTAGRAM_URL")],
            "expected_intents": ["CHECK", "INVESTIGATE"]
        },
        {
            "text": "Investigate Facebook user facebook.com/profile/suspect and LinkedIn profile linkedin.com/in/target",
            "category": "social_media_multi",
            "expected_entities": [
                ("facebook.com/profile/suspect", "FACEBOOK_URL"),
                ("linkedin.com/in/target", "LINKEDIN_URL")
            ],
            "expected_intents": ["INVESTIGATE", "TRACK"]
        },
        {
            "text": "Track LinkedIn user @professional_target and Facebook username @suspicious_person",
            "category": "social_media_users",
            "expected_entities": [
                ("@professional_target", "LINKEDIN_USERNAME"),
                ("@suspicious_person", "FACEBOOK_USERNAME")
            ],
            "expected_intents": ["TRACK", "MONITOR"]
        },
        {
            "text": "Investigate Telegram channel @evil_channel and Discord server discord.gg/malicious",
            "category": "social_media_communication",
            "expected_entities": [
                ("@evil_channel", "TELEGRAM_USERNAME"),
                ("discord.gg/malicious", "DISCORD_URL")
            ],
            "expected_intents": ["INVESTIGATE", "MONITOR"]
        },
        {
            "text": "Check Telegram URL t.me/malicious_channel and Discord username @hacker#1234",
            "category": "social_media_communication",
            "expected_entities": [
                ("t.me/malicious_channel", "TELEGRAM_URL"),
                ("@hacker#1234", "DISCORD_USERNAME")
            ],
            "expected_intents": ["CHECK", "INVESTIGATE"]
        },
        {
            "text": "Monitor Slack workspace slack.com/workspace/team and Slack user @slack_user",
            "category": "social_media_work",
            "expected_entities": [
                ("slack.com/workspace/team", "SLACK_URL"),
                ("@slack_user", "SLACK_USERNAME")
            ],
            "expected_intents": ["MONITOR", "TRACK"]
        },
        {
            "text": "Investigate WhatsApp contact +1-555-123-4567 and WhatsApp URL wa.me/1234567890",
            "category": "social_media_whatsapp",
            "expected_entities": [
                ("+1-555-123-4567", "PHONE_NUMBER"),
                ("wa.me/1234567890", "WHATSAPP_URL")
            ],
            "expected_intents": ["INVESTIGATE", "MONITOR"]
        },
        {
            "text": "Cross-reference social media accounts: Instagram @user1, Facebook @user2, LinkedIn @user3",
            "category": "social_media_crossref",
            "expected_entities": [
                ("@user1", "INSTAGRAM_USERNAME"),
                ("@user2", "FACEBOOK_USERNAME"),
                ("@user3", "LINKEDIN_USERNAME")
            ],
            "expected_intents": ["CORRELATE_EVENTS", "INVESTIGATE"]
        },
        {
            "text": "Verify all social media URLs: instagram.com/user, facebook.com/user, linkedin.com/in/user",
            "category": "social_media_urls",
            "expected_entities": [
                ("instagram.com/user", "INSTAGRAM_URL"),
                ("facebook.com/user", "FACEBOOK_URL"),
                ("linkedin.com/in/user", "LINKEDIN_URL")
            ],
            "expected_intents": ["VERIFY", "CHECK"]
        },
        
        # ========== GITHUB ENTITIES (12 tests) ==========
        {
            "text": "Scan GitHub repository github.com/evilorg/malware for vulnerabilities",
            "category": "github_repo",
            "expected_entities": [("github.com/evilorg/malware", "GITHUB_REPO_URL")],
            "expected_intents": ["SCAN_GITHUB_REPO", "DETECT_GITHUB_VULNERABILITIES"]
        },
        {
            "text": "Analyze GitHub repo evilorg/malware and check for malicious code",
            "category": "github_repo",
            "expected_entities": [("evilorg/malware", "GITHUB_REPO")],
            "expected_intents": ["ANALYZE_GITHUB_REPO", "REVIEW_GITHUB_CODE"]
        },
        {
            "text": "Investigate GitHub user @hacker123 and organization @evilcorp",
            "category": "github_users",
            "expected_entities": [
                ("@hacker123", "GITHUB_USER"),
                ("@evilcorp", "GITHUB_ORGANIZATION")
            ],
            "expected_intents": ["INVESTIGATE_GITHUB_USER", "ANALYZE_GITHUB_ORGANIZATION"]
        },
        {
            "text": "Review GitHub issue #42 and pull request #15 in repo github.com/org/repo",
            "category": "github_issues",
            "expected_entities": [
                ("#42", "GITHUB_ISSUE"),
                ("#15", "GITHUB_PULL_REQUEST"),
                ("github.com/org/repo", "GITHUB_REPO_URL")
            ],
            "expected_intents": ["ANALYZE_GITHUB_ISSUES", "REVIEW_GITHUB_PULL_REQUESTS"]
        },
        {
            "text": "Track GitHub commit a1b2c3d4e5f6 and branch feature/malicious-code",
            "category": "github_code",
            "expected_entities": [
                ("a1b2c3d4e5f6", "GITHUB_COMMIT"),
                ("feature/malicious-code", "GITHUB_BRANCH")
            ],
            "expected_intents": ["TRACK_GITHUB_COMMITS", "MONITOR_GITHUB_BRANCHES"]
        },
        {
            "text": "Monitor GitHub release v2.0.0 and tag malicious-tag in repository",
            "category": "github_releases",
            "expected_entities": [
                ("v2.0.0", "GITHUB_RELEASE"),
                ("malicious-tag", "GITHUB_TAG")
            ],
            "expected_intents": ["TRACK_GITHUB_RELEASES", "TRACK_GITHUB_TAGS"]
        },
        {
            "text": "Check GitHub gist gist.github.com/user/abc123def456 for exposed secrets",
            "category": "github_gist",
            "expected_entities": [("gist.github.com/user/abc123def456", "GITHUB_GIST")],
            "expected_intents": ["ANALYZE_GITHUB_GISTS", "DETECT_GITHUB_EXPLOITS"]
        },
        {
            "text": "Analyze GitHub commits in repo github.com/org/repo from user @developer",
            "category": "github_activity",
            "expected_entities": [
                ("github.com/org/repo", "GITHUB_REPO_URL"),
                ("@developer", "GITHUB_USER")
            ],
            "expected_intents": ["ANALYZE_GITHUB_COMMITS", "MONITOR_GITHUB_ACTIVITY"]
        },
        {
            "text": "Search GitHub repositories for malware patterns and suspicious code",
            "category": "github_search",
            "expected_intents": ["SEARCH_GITHUB_REPOS", "EXTRACT_GITHUB_INTELLIGENCE"]
        },
        {
            "text": "Clone and analyze GitHub repository github.com/suspicious/repo",
            "category": "github_analysis",
            "expected_entities": [("github.com/suspicious/repo", "GITHUB_REPO_URL")],
            "expected_intents": ["CLONE_GITHUB_REPO", "ANALYZE_GITHUB_REPO"]
        },
        {
            "text": "Monitor GitHub organization @evilorg for new repositories and releases",
            "category": "github_monitoring",
            "expected_entities": [("@evilorg", "GITHUB_ORGANIZATION")],
            "expected_intents": ["MONITOR_GITHUB_REPO", "ANALYZE_GITHUB_ORGANIZATION"]
        },
        {
            "text": "Review GitHub code in commit abc123def456789 for security vulnerabilities",
            "category": "github_security",
            "expected_entities": [("abc123def456789", "GITHUB_COMMIT")],
            "expected_intents": ["REVIEW_GITHUB_CODE", "DETECT_GITHUB_VULNERABILITIES"]
        },
        
        # ========== IPV6 & ADVANCED URLS (10 tests) ==========
        {
            "text": "Block IPv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            "category": "ipv6",
            "expected_entities": [("2001:0db8:85a3:0000:0000:8a2e:0370:7334", "IPV6_ADDRESS")],
            "expected_intents": ["BLOCK_IPS"]
        },
        {
            "text": "Check IPv6 2001:db8::1 and compressed format 2001:db8:0:0:0:0:0:1",
            "category": "ipv6_variations",
            "expected_entities": [
                ("2001:db8::1", "IPV6_ADDRESS"),
                ("2001:db8:0:0:0:0:0:1", "IPV6_ADDRESS")
            ],
            "expected_intents": ["CHECK", "INVESTIGATE"]
        },
        {
            "text": "Monitor IPv6 address ::1 and fe80::1%eth0",
            "category": "ipv6_special",
            "expected_entities": [
                ("::1", "IPV6_ADDRESS"),
                ("fe80::1%eth0", "IPV6_ADDRESS")
            ],
            "expected_intents": ["MONITOR", "TRACK"]
        },
        {
            "text": "Check URL https://evil.com:8080/api?key=value#section",
            "category": "advanced_urls",
            "expected_entities": [("https://evil.com:8080/api?key=value#section", "URL")],
            "expected_intents": ["CHECK", "INVESTIGATE"]
        },
        {
            "text": "Investigate URLs: ftp://files.example.com/path, sftp://secure.example.com, file:///local/path",
            "category": "url_schemes",
            "expected_entities": [
                ("ftp://files.example.com/path", "URL"),
                ("sftp://secure.example.com", "URL"),
                ("file:///local/path", "URL")
            ],
            "expected_intents": ["INVESTIGATE", "CHECK"]
        },
        {
            "text": "Check URL with authentication https://user:pass@example.com:443/path?query=value",
            "category": "url_auth",
            "expected_entities": [("https://user:pass@example.com:443/path?query=value", "URL")],
            "expected_intents": ["CHECK", "INVESTIGATE"]
        },
        {
            "text": "Monitor URL patterns: http://example.com, https://secure.example.com, http://example.com:8080",
            "category": "url_patterns",
            "expected_entities": [
                ("http://example.com", "URL"),
                ("https://secure.example.com", "URL"),
                ("http://example.com:8080", "URL")
            ],
            "expected_intents": ["MONITOR", "TRACK"]
        },
        {
            "text": "Block IPv6 2001:0db8::/32 subnet and URL https://malicious.com",
            "category": "ipv6_url_combined",
            "expected_entities": [
                ("2001:0db8::/32", "IPV6_ADDRESS"),
                ("https://malicious.com", "URL")
            ],
            "expected_intents": ["BLOCK_IPS", "INVESTIGATE"]
        },
        {
            "text": "Check IPv6 address with port [2001:db8::1]:8080",
            "category": "ipv6_port",
            "expected_entities": [("2001:db8::1", "IPV6_ADDRESS")],
            "expected_intents": ["CHECK", "INVESTIGATE"]
        },
        {
            "text": "Investigate IPv6 link-local fe80::1 and site-local addresses",
            "category": "ipv6_scopes",
            "expected_entities": [("fe80::1", "IPV6_ADDRESS")],
            "expected_intents": ["INVESTIGATE", "ANALYZE"]
        },
        
        # ========== PII ENTITIES (12 tests) ==========
        {
            "text": "PII leak detected: SSN 123-45-6789, phone +44 20 7946 0958",
            "category": "pii_leak",
            "expected_entities": [
                ("123-45-6789", "SSN"),
                ("+44 20 7946 0958", "PHONE_NUMBER")
            ],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        {
            "text": "Credit card number 4532-1234-5678-9010 found in breach data",
            "category": "pii_credit_card",
            "expected_entities": [("4532-1234-5678-9010", "CREDIT_CARD_NUMBER")],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        {
            "text": "Exposed PII: SSN 123-45-6789, passport A12345678, driver license DL123456",
            "category": "pii_multiple",
            "expected_entities": [
                ("123-45-6789", "SSN"),
                ("A12345678", "PASSPORT_NUMBER"),
                ("DL123456", "DRIVER_LICENSE_NUMBER")
            ],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        {
            "text": "Bank account number 1234567890 and routing number 021000021 found in logs",
            "category": "pii_financial",
            "expected_entities": [
                ("1234567890", "BANK_ACCOUNT_NUMBER"),
                ("021000021", "ROUTING_NUMBER")
            ],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        {
            "text": "International phone numbers: +1-555-123-4567, +44-20-7946-0958, +33-1-42-86-83-26",
            "category": "pii_phones",
            "expected_entities": [
                ("+1-555-123-4567", "PHONE_NUMBER"),
                ("+44-20-7946-0958", "PHONE_NUMBER"),
                ("+33-1-42-86-83-26", "PHONE_NUMBER")
            ],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        {
            "text": "Phone formats: (555) 123-4567, 555-123-4567, +1.555.123.4567",
            "category": "pii_phone_formats",
            "expected_entities": [
                ("(555) 123-4567", "PHONE_NUMBER"),
                ("555-123-4567", "PHONE_NUMBER"),
                ("+1.555.123.4567", "PHONE_NUMBER")
            ],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        {
            "text": "SWIFT code CHASUS33 and credit card 4532 1234 5678 9010",
            "category": "pii_financial_codes",
            "expected_entities": [
                ("CHASUS33", "SWIFT_CODE"),
                ("4532 1234 5678 9010", "CREDIT_CARD_NUMBER")
            ],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        {
            "text": "Email with display name: \"John Doe\" <john.doe@example.com>",
            "category": "pii_email_formats",
            "expected_entities": [("john.doe@example.com", "EMAIL_ADDRESS")],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        {
            "text": "Email plus addressing: user+tag@example.com and subdomain user@mail.example.com",
            "category": "pii_email_variations",
            "expected_entities": [
                ("user+tag@example.com", "EMAIL_ADDRESS"),
                ("user@mail.example.com", "EMAIL_ADDRESS")
            ],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        {
            "text": "Full PII breach: SSN 123-45-6789, DOB 01/15/1980, email user@example.com, phone 555-1234",
            "category": "pii_complete",
            "expected_entities": [
                ("123-45-6789", "SSN"),
                ("01/15/1980", "DOB"),
                ("user@example.com", "EMAIL_ADDRESS"),
                ("555-1234", "PHONE_NUMBER")
            ],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        {
            "text": "Credit card formats: 4532-1234-5678-9010, 4532 1234 5678 9010, 4532123456789010",
            "category": "pii_credit_formats",
            "expected_entities": [
                ("4532-1234-5678-9010", "CREDIT_CARD_NUMBER"),
                ("4532 1234 5678 9010", "CREDIT_CARD_NUMBER"),
                ("4532123456789010", "CREDIT_CARD_NUMBER")
            ],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        {
            "text": "SSN formats: 123-45-6789, 123 45 6789, 123456789",
            "category": "pii_ssn_formats",
            "expected_entities": [
                ("123-45-6789", "SSN"),
                ("123 45 6789", "SSN"),
                ("123456789", "SSN")
            ],
            "expected_intents": ["DETECT_PII", "INVESTIGATE"]
        },
        
        # ========== AI/LLM ENTITIES (8 tests) ==========
        {
            "text": "AI security incident involving GPT-4 from OpenAI provider",
            "category": "ai_entities",
            "expected_entities": [
                ("GPT-4", "LLM_MODEL"),
                ("OpenAI", "LLM_PROVIDER")
            ],
            "expected_intents": ["INVESTIGATE", "ANALYZE"]
        },
        {
            "text": "Check LLM models: Claude-3 from Anthropic, Llama-2 from Meta, GPT-3.5 from OpenAI",
            "category": "ai_models",
            "expected_entities": [
                ("Claude-3", "LLM_MODEL"),
                ("Anthropic", "LLM_PROVIDER"),
                ("Llama-2", "LLM_MODEL"),
                ("Meta", "LLM_PROVIDER"),
                ("GPT-3.5", "LLM_MODEL"),
                ("OpenAI", "LLM_PROVIDER")
            ],
            "expected_intents": ["CHECK", "ANALYZE"]
        },
        {
            "text": "Monitor AI model usage: GPT-4, Claude-3-Opus, Gemini-Pro from Google",
            "category": "ai_monitoring",
            "expected_entities": [
                ("GPT-4", "LLM_MODEL"),
                ("Claude-3-Opus", "LLM_MODEL"),
                ("Gemini-Pro", "LLM_MODEL"),
                ("Google", "LLM_PROVIDER")
            ],
            "expected_intents": ["MONITOR", "TRACK"]
        },
        {
            "text": "AI model security: Check GPT-4, Claude-3, and Llama-2 for vulnerabilities",
            "category": "ai_security",
            "expected_entities": [
                ("GPT-4", "LLM_MODEL"),
                ("Claude-3", "LLM_MODEL"),
                ("Llama-2", "LLM_MODEL")
            ],
            "expected_intents": ["CHECK", "TEST_SECURITY"]
        },
        {
            "text": "LLM providers: OpenAI, Anthropic, Google, Meta, Microsoft",
            "category": "ai_providers",
            "expected_entities": [
                ("OpenAI", "LLM_PROVIDER"),
                ("Anthropic", "LLM_PROVIDER"),
                ("Google", "LLM_PROVIDER"),
                ("Meta", "LLM_PROVIDER"),
                ("Microsoft", "LLM_PROVIDER")
            ],
            "expected_intents": ["ANALYZE", "INVESTIGATE"]
        },
        {
            "text": "AI model types: GPT-4-turbo, Claude-3-Sonnet, Llama-2-70b",
            "category": "ai_model_variants",
            "expected_entities": [
                ("GPT-4-turbo", "LLM_MODEL"),
                ("Claude-3-Sonnet", "LLM_MODEL"),
                ("Llama-2-70b", "LLM_MODEL")
            ],
            "expected_intents": ["ANALYZE", "INVESTIGATE"]
        },
        {
            "text": "Investigate AI security: GPT-4 from OpenAI and Claude-3 from Anthropic",
            "category": "ai_investigation",
            "expected_entities": [
                ("GPT-4", "LLM_MODEL"),
                ("OpenAI", "LLM_PROVIDER"),
                ("Claude-3", "LLM_MODEL"),
                ("Anthropic", "LLM_PROVIDER")
            ],
            "expected_intents": ["INVESTIGATE", "ANALYZE"]
        },
        {
            "text": "AI model audit: Review GPT-4, Claude-3, and Llama-2 usage",
            "category": "ai_audit",
            "expected_entities": [
                ("GPT-4", "LLM_MODEL"),
                ("Claude-3", "LLM_MODEL"),
                ("Llama-2", "LLM_MODEL")
            ],
            "expected_intents": ["AUDIT_COMPLIANCE", "REVIEW"]
        },
        
        # ========== GEOGRAPHIC ADVANCED (10 tests) ==========
        {
            "text": "Location at 52°31'44.7\"N 13°23'05.7\"E in datacenter AWS-US-EAST-1",
            "category": "geographic_dms",
            "expected_entities": [
                ("52°31'44.7\"N 13°23'05.7\"E", "DMS_COORDINATES"),
                ("AWS-US-EAST-1", "DATACENTER")
            ],
            "expected_intents": ["INVESTIGATE", "MAP"]
        },
        {
            "text": "Coordinates in GeoJSON format: {\"type\": \"Point\", \"coordinates\": [-74.006, 40.7128]}",
            "category": "geographic_geojson",
            "expected_entities": [("{\"type\": \"Point\", \"coordinates\": [-74.006, 40.7128]}", "GEOJSON")],
            "expected_intents": ["INVESTIGATE", "MAP"]
        },
        {
            "text": "Custom coordinates: {\"location\": {\"latitude\": 52.53076, \"longitude\": 13.38492}}",
            "category": "geographic_custom",
            "expected_entities": [("{\"location\": {\"latitude\": 52.53076, \"longitude\": 13.38492}}", "CUSTOM_COORDINATES")],
            "expected_intents": ["INVESTIGATE", "MAP"]
        },
        {
            "text": "Datacenter locations: AWS-US-EAST-1, GCP-US-CENTRAL1, Azure-EAST-US",
            "category": "geographic_datacenters",
            "expected_entities": [
                ("AWS-US-EAST-1", "DATACENTER"),
                ("GCP-US-CENTRAL1", "DATACENTER"),
                ("Azure-EAST-US", "DATACENTER")
            ],
            "expected_intents": ["INVESTIGATE", "MAP"]
        },
        {
            "text": "Nameserver ns1.example.com and ns2.example.com for domain tracking",
            "category": "geographic_nameservers",
            "expected_entities": [
                ("ns1.example.com", "NAMESERVER"),
                ("ns2.example.com", "NAMESERVER")
            ],
            "expected_intents": ["INVESTIGATE", "TRACK"]
        },
        {
            "text": "Altitude 8848m at coordinates 27.9881, 86.9250 (Mount Everest)",
            "category": "geographic_altitude",
            "expected_entities": [
                ("8848m", "ALTITUDE"),
                ("27.9881", "LATITUDE"),
                ("86.9250", "LONGITUDE")
            ],
            "expected_intents": ["INVESTIGATE", "MAP"]
        },
        {
            "text": "Elevation 282 feet at location 40.7128, -74.0060",
            "category": "geographic_elevation",
            "expected_entities": [
                ("282 feet", "ELEVATION"),
                ("40.7128", "LATITUDE"),
                ("-74.0060", "LONGITUDE")
            ],
            "expected_intents": ["INVESTIGATE", "MAP"]
        },
        {
            "text": "DMS coordinates: 40°42'46\"N 74°00'22\"W and 51°30'26\"N 0°07'39\"W",
            "category": "geographic_dms_multiple",
            "expected_entities": [
                ("40°42'46\"N 74°00'22\"W", "DMS_COORDINATES"),
                ("51°30'26\"N 0°07'39\"W", "DMS_COORDINATES")
            ],
            "expected_intents": ["INVESTIGATE", "MAP"]
        },
        {
            "text": "GeoJSON Point at [-122.4194, 37.7749] and datacenter GCP-US-WEST1",
            "category": "geographic_combined",
            "expected_entities": [
                ("[-122.4194, 37.7749]", "GEOJSON"),
                ("GCP-US-WEST1", "DATACENTER")
            ],
            "expected_intents": ["INVESTIGATE", "MAP"]
        },
        {
            "text": "Track location: latitude 40.7128, longitude -74.0060, altitude 10m, datacenter AWS-US-EAST-1",
            "category": "geographic_complete",
            "expected_entities": [
                ("40.7128", "LATITUDE"),
                ("-74.0060", "LONGITUDE"),
                ("10m", "ALTITUDE"),
                ("AWS-US-EAST-1", "DATACENTER")
            ],
            "expected_intents": ["TRACK", "MAP"]
        },
        
        # ========== HASH VALUES (8 tests) ==========
        {
            "text": "Malware hash MD5: 5d41402abc4b2a76b9719d911017c592 SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "category": "hash_entities",
            "expected_entities": [
                ("5d41402abc4b2a76b9719d911017c592", "HASH"),
                ("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "HASH")
            ],
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "File hash SHA1: da39a3ee5e6b4b0d3255bfef95601890afd80709",
            "category": "hash_sha1",
            "expected_entities": [("da39a3ee5e6b4b0d3255bfef95601890afd80709", "HASH")],
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "Multiple hashes: MD5 abc123, SHA256 def456, SHA1 ghi789",
            "category": "hash_multiple",
            "expected_entities": [
                ("abc123", "HASH"),
                ("def456", "HASH"),
                ("ghi789", "HASH")
            ],
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "Malware sample hash: 5d41402abc4b2a76b9719d911017c592 (MD5)",
            "category": "hash_md5",
            "expected_entities": [("5d41402abc4b2a76b9719d911017c592", "HASH")],
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "SHA256 hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 matches known malware",
            "category": "hash_sha256",
            "expected_entities": [("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "HASH")],
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "File hashes: MD5=abc123def456, SHA256=ghi789jkl012",
            "category": "hash_formatted",
            "expected_entities": [
                ("abc123def456", "HASH"),
                ("ghi789jkl012", "HASH")
            ],
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "Compare hashes: original 5d41402abc4b2a76b9719d911017c592 vs modified e3b0c44298fc1c149afbf4c8996fb924",
            "category": "hash_comparison",
            "expected_entities": [
                ("5d41402abc4b2a76b9719d911017c592", "HASH"),
                ("e3b0c44298fc1c149afbf4c8996fb924", "HASH")
            ],
            "expected_intents": ["ANALYZE", "COMPARE"]
        },
        {
            "text": "Hash database lookup: MD5 abc123, SHA1 def456, SHA256 ghi789",
            "category": "hash_database",
            "expected_entities": [
                ("abc123", "HASH"),
                ("def456", "HASH"),
                ("ghi789", "HASH")
            ],
            "expected_intents": ["INVESTIGATE", "ANALYZE"]
        },
        
        # ========== NEGATIVE TEST CASES (15 tests) ==========
        {
            "text": "This is just a normal sentence with no security information.",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "The weather is nice today and I'm going for a walk.",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "Hello, how are you doing?",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "I need to buy groceries: milk, eggs, bread, and cheese.",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "The meeting is scheduled for tomorrow at 3 PM.",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "Can you please help me with this task?",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "I love programming and software development.",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "The book is on the table next to the window.",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "What time is it?",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "Thank you for your help!",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "I'm learning about machine learning and artificial intelligence.",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "The cat sat on the mat.",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "Please send me the document when you have a chance.",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "I enjoy reading books and watching movies.",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "The restaurant serves delicious food and has great service.",
            "category": "negative_case",
            "expected_entities": [],
            "expected_intents": []
        },
        
        # ========== UNICODE/EMOJIS (8 tests) ==========
        {
            "text": "🚨 Security alert: IP 192.168.1.1 compromised © 2024",
            "category": "unicode_emojis",
            "expected_entities": [
                ("192.168.1.1", "IP_ADDRESS"),
                ("🚨", "EMOJI")
            ],
            "expected_intents": ["INVESTIGATE", "DETECT"]
        },
        {
            "text": "⚠️ Warning: Domain example.com is suspicious 🔍",
            "category": "unicode_emojis",
            "expected_entities": [
                ("example.com", "DOMAIN"),
                ("⚠️", "EMOJI"),
                ("🔍", "EMOJI")
            ],
            "expected_intents": ["WARN", "INVESTIGATE"]
        },
        {
            "text": "✅ Verified: Email user@example.com is safe ✓",
            "category": "unicode_emojis",
            "expected_entities": [
                ("user@example.com", "EMAIL_ADDRESS"),
                ("✅", "EMOJI"),
                ("✓", "EMOJI")
            ],
            "expected_intents": ["VERIFY", "CHECK"]
        },
        {
            "text": "🔒 Encrypted data breach detected at IP 10.0.0.1 🚨",
            "category": "unicode_emojis",
            "expected_entities": [
                ("10.0.0.1", "IP_ADDRESS"),
                ("🔒", "EMOJI"),
                ("🚨", "EMOJI")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "📧 Email phishing detected: phishing@evil.com ⚠️",
            "category": "unicode_emojis",
            "expected_entities": [
                ("phishing@evil.com", "EMAIL_ADDRESS"),
                ("📧", "EMOJI"),
                ("⚠️", "EMOJI")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "🌐 Network attack from IP 172.16.0.1 🔥",
            "category": "unicode_emojis",
            "expected_entities": [
                ("172.16.0.1", "IP_ADDRESS"),
                ("🌐", "EMOJI"),
                ("🔥", "EMOJI")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "💻 Malware detected: hash abc123def456 🦠",
            "category": "unicode_emojis",
            "expected_entities": [
                ("abc123def456", "HASH"),
                ("💻", "EMOJI"),
                ("🦠", "EMOJI")
            ],
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "🔐 Security breach: CVE-2021-44228 exploited ⚡",
            "category": "unicode_emojis",
            "expected_entities": [
                ("CVE-2021-44228", "CVE_ID"),
                ("🔐", "EMOJI"),
                ("⚡", "EMOJI")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        
        # ========== FORMAT VARIATIONS (20 tests) ==========
        {
            "text": "Check IP 192.168.1.1 (lowercase)",
            "category": "format_variations",
            "expected_entities": [("192.168.1.1", "IP_ADDRESS")],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "CHECK IP 192.168.1.1 (UPPERCASE)",
            "category": "format_variations",
            "expected_entities": [("192.168.1.1", "IP_ADDRESS")],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "ChEcK iP 192.168.1.1 (MiXeD cAsE)",
            "category": "format_variations",
            "expected_entities": [("192.168.1.1", "IP_ADDRESS")],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "Check 1P 192.168.1.1 (leet speak)",
            "category": "format_variations",
            "expected_entities": [("192.168.1.1", "IP_ADDRESS")],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "Domain example.com in various formats: EXAMPLE.COM, Example.Com, eXaMpLe.CoM",
            "category": "format_variations",
            "expected_entities": [
                ("example.com", "DOMAIN"),
                ("EXAMPLE.COM", "DOMAIN"),
                ("Example.Com", "DOMAIN"),
                ("eXaMpLe.CoM", "DOMAIN")
            ],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "Date formats: 2024-11-30, 11/30/2024, November 30, 2024, 30-Nov-2024",
            "category": "format_variations",
            "expected_entities": [
                ("2024-11-30", "DATE"),
                ("11/30/2024", "DATE"),
                ("November 30, 2024", "DATE"),
                ("30-Nov-2024", "DATE")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "Time formats: 14:30, 2:30 PM, 14:30:00, 2:30:00 PM",
            "category": "format_variations",
            "expected_entities": [
                ("14:30", "TIME"),
                ("2:30 PM", "TIME"),
                ("14:30:00", "TIME"),
                ("2:30:00 PM", "TIME")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "Email formats: user@example.com, User@Example.COM, user+tag@example.com",
            "category": "format_variations",
            "expected_entities": [
                ("user@example.com", "EMAIL_ADDRESS"),
                ("User@Example.COM", "EMAIL_ADDRESS"),
                ("user+tag@example.com", "EMAIL_ADDRESS")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "Phone formats: +1-555-123-4567, (555) 123-4567, 555.123.4567, +15551234567",
            "category": "format_variations",
            "expected_entities": [
                ("+1-555-123-4567", "PHONE_NUMBER"),
                ("(555) 123-4567", "PHONE_NUMBER"),
                ("555.123.4567", "PHONE_NUMBER"),
                ("+15551234567", "PHONE_NUMBER")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "CVE formats: CVE-2021-44228, cve-2021-44228, CVE202144228",
            "category": "format_variations",
            "expected_entities": [
                ("CVE-2021-44228", "CVE_ID"),
                ("cve-2021-44228", "CVE_ID"),
                ("CVE202144228", "CVE_ID")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "URL formats: http://example.com, https://EXAMPLE.COM, HTTP://example.com/path",
            "category": "format_variations",
            "expected_entities": [
                ("http://example.com", "URL"),
                ("https://EXAMPLE.COM", "URL"),
                ("HTTP://example.com/path", "URL")
            ],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "Threat actor formats: APT29, apt29, Apt29, APT-29",
            "category": "format_variations",
            "expected_entities": [
                ("APT29", "THREAT_ACTOR"),
                ("apt29", "THREAT_ACTOR"),
                ("Apt29", "THREAT_ACTOR"),
                ("APT-29", "THREAT_ACTOR")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "Wallet address formats: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb, 0X742D35CC6634C0532925A3B844BC9E7595F0BEB",
            "category": "format_variations",
            "expected_entities": [
                ("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "WALLET_ADDRESS"),
                ("0X742D35CC6634C0532925A3B844BC9E7595F0BEB", "WALLET_ADDRESS")
            ],
            "expected_intents": ["TRACK"]
        },
        {
            "text": "Coordinate formats: 40.7128, -74.0060 and 40°42'46\"N 74°00'22\"W",
            "category": "format_variations",
            "expected_entities": [
                ("40.7128", "LATITUDE"),
                ("-74.0060", "LONGITUDE"),
                ("40°42'46\"N 74°00'22\"W", "DMS_COORDINATES")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "ISO 8601 date: 2024-11-30T14:30:00Z and Unix timestamp 1701350400",
            "category": "format_variations",
            "expected_entities": [
                ("2024-11-30T14:30:00Z", "DATE"),
                ("1701350400", "DATE")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "Relative dates: yesterday, last week, 24 hours ago, tomorrow",
            "category": "format_variations",
            "expected_entities": [],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "Percentage formats: 50%, 50 percent, 0.5, 1/2",
            "category": "format_variations",
            "expected_entities": [
                ("50%", "PERCENTAGE"),
                ("50 percent", "PERCENTAGE"),
                ("0.5", "PERCENTAGE"),
                ("1/2", "PERCENTAGE")
            ],
            "expected_intents": ["ANALYZE"]
        },
        {
            "text": "Currency formats: $100, USD 100, 100 dollars, €100, £100",
            "category": "format_variations",
            "expected_entities": [
                ("$100", "CURRENCY"),
                ("USD 100", "CURRENCY"),
                ("€100", "CURRENCY"),
                ("£100", "CURRENCY")
            ],
            "expected_intents": ["ANALYZE"]
        },
        {
            "text": "Port formats: 443, port 443, :443, 443/tcp",
            "category": "format_variations",
            "expected_entities": [
                ("443", "PORT"),
                ("443", "PORT"),
                ("443", "PORT"),
                ("443", "PORT")
            ],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "Protocol formats: HTTP, https, http/2, HTTPS/1.1",
            "category": "format_variations",
            "expected_entities": [
                ("HTTP", "PROTOCOL"),
                ("https", "PROTOCOL"),
                ("http/2", "PROTOCOL"),
                ("HTTPS/1.1", "PROTOCOL")
            ],
            "expected_intents": ["CHECK"]
        },
        
        # ========== BOUNDARY CASES (15 tests) ==========
        {
            "text": "",
            "category": "boundary_empty",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "   ",
            "category": "boundary_whitespace",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "\n\n",
            "category": "boundary_newlines",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "a",
            "category": "boundary_single_char",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "12345",
            "category": "boundary_numbers_only",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "!!!???",
            "category": "boundary_punctuation_only",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "A" * 10000,  # Very long string
            "category": "boundary_very_long",
            "expected_entities": [],
            "expected_intents": []
        },
        {
            "text": "IP 192.168.1.1" + " " * 1000 + "Domain example.com",
            "category": "boundary_large_whitespace",
            "expected_entities": [
                ("192.168.1.1", "IP_ADDRESS"),
                ("example.com", "DOMAIN")
            ],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "192.168.1.1" * 100,  # Repeated IP
            "category": "boundary_repeated",
            "expected_entities": [("192.168.1.1", "IP_ADDRESS")],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "a" * 5000 + "192.168.1.1" + "b" * 5000,  # IP in middle of long string
            "category": "boundary_long_with_entity",
            "expected_entities": [("192.168.1.1", "IP_ADDRESS")],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "IP:192.168.1.1,Domain:example.com,Email:user@test.com",  # No spaces
            "category": "boundary_no_spaces",
            "expected_entities": [
                ("192.168.1.1", "IP_ADDRESS"),
                ("example.com", "DOMAIN"),
                ("user@test.com", "EMAIL_ADDRESS")
            ],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "IP\t192.168.1.1\tDomain\texample.com",  # Tabs
            "category": "boundary_tabs",
            "expected_entities": [
                ("192.168.1.1", "IP_ADDRESS"),
                ("example.com", "DOMAIN")
            ],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "IP\n192.168.1.1\nDomain\nexample.com",  # Newlines
            "category": "boundary_newlines",
            "expected_entities": [
                ("192.168.1.1", "IP_ADDRESS"),
                ("example.com", "DOMAIN")
            ],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "192.168.1.1" + "\x00" * 10 + "example.com",  # Null bytes
            "category": "boundary_null_bytes",
            "expected_entities": [
                ("192.168.1.1", "IP_ADDRESS"),
                ("example.com", "DOMAIN")
            ],
            "expected_intents": ["CHECK"]
        },
        {
            "text": "Check IP 192.168.1.1 and domain example.com and email user@test.com and phone 555-1234",
            "category": "boundary_many_entities",
            "expected_entities": [
                ("192.168.1.1", "IP_ADDRESS"),
                ("example.com", "DOMAIN"),
                ("user@test.com", "EMAIL_ADDRESS"),
                ("555-1234", "PHONE_NUMBER")
            ],
            "expected_intents": ["CHECK"]
        },
        
        # ========== SECURITY PATTERNS (12 tests) ==========
        {
            "text": "Detected SQL injection attempt: ' OR '1'='1 in query parameter",
            "category": "security_patterns",
            "expected_intents": ["DETECT", "PREVENT_INJECTION"]
        },
        {
            "text": "XSS attack detected: <script>alert('XSS')</script> in user input",
            "category": "security_patterns",
            "expected_intents": ["DETECT", "PREVENT_ATTACKS"]
        },
        {
            "text": "Command injection attempt: ; rm -rf / detected in input",
            "category": "security_patterns",
            "expected_intents": ["DETECT", "PREVENT_INJECTION"]
        },
        {
            "text": "Path traversal attempt: ../../../etc/passwd in file request",
            "category": "security_patterns",
            "expected_intents": ["DETECT", "PREVENT_ATTACKS"]
        },
        {
            "text": "LDAP injection: *)(& detected in search query",
            "category": "security_patterns",
            "expected_intents": ["DETECT", "PREVENT_INJECTION"]
        },
        {
            "text": "XML injection: <!ENTITY xxe SYSTEM \"file:///etc/passwd\"> detected",
            "category": "security_patterns",
            "expected_intents": ["DETECT", "PREVENT_INJECTION"]
        },
        {
            "text": "NoSQL injection: {\"$ne\": null} in MongoDB query",
            "category": "security_patterns",
            "expected_intents": ["DETECT", "PREVENT_INJECTION"]
        },
        {
            "text": "Template injection: {{7*7}} in template engine",
            "category": "security_patterns",
            "expected_intents": ["DETECT", "PREVENT_INJECTION"]
        },
        {
            "text": "SSRF attempt: http://internal-server.local detected",
            "category": "security_patterns",
            "expected_entities": [("http://internal-server.local", "URL")],
            "expected_intents": ["DETECT", "PREVENT_ATTACKS"]
        },
        {
            "text": "CSRF token missing in POST request to /api/transfer",
            "category": "security_patterns",
            "expected_intents": ["DETECT", "PREVENT_ATTACKS"]
        },
        {
            "text": "Buffer overflow detected: payload exceeds maximum length",
            "category": "security_patterns",
            "expected_intents": ["DETECT", "PREVENT_ATTACKS"]
        },
        {
            "text": "Race condition detected in file upload process",
            "category": "security_patterns",
            "expected_intents": ["DETECT", "PREVENT_ATTACKS"]
        },
        
        # ========== FILE PATHS (6 tests) ==========
        {
            "text": "Malicious file path detected: C:\\Users\\Admin\\Desktop\\malware.exe",
            "category": "file_paths",
            "expected_entities": [("C:\\Users\\Admin\\Desktop\\malware.exe", "FILE_PATH")],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "Unix path /home/user/.ssh/id_rsa contains private key",
            "category": "file_paths",
            "expected_entities": [("/home/user/.ssh/id_rsa", "FILE_PATH")],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "Network path \\\\server\\share\\file.txt accessed",
            "category": "file_paths",
            "expected_entities": [("\\\\server\\share\\file.txt", "FILE_PATH")],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "File paths: /etc/passwd, C:\\Windows\\System32\\config\\SAM, ~/.bashrc",
            "category": "file_paths",
            "expected_entities": [
                ("/etc/passwd", "FILE_PATH"),
                ("C:\\Windows\\System32\\config\\SAM", "FILE_PATH"),
                ("~/.bashrc", "FILE_PATH")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "Sensitive file accessed: /var/log/auth.log, /var/log/syslog",
            "category": "file_paths",
            "expected_entities": [
                ("/var/log/auth.log", "FILE_PATH"),
                ("/var/log/syslog", "FILE_PATH")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "Windows registry key: HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows",
            "category": "file_paths",
            "expected_entities": [("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows", "REGISTRY_KEY")],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        
        # ========== CODE SNIPPETS (6 tests) ==========
        {
            "text": "Code snippet detected: <?php system($_GET['cmd']); ?>",
            "category": "code_snippets",
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "JavaScript code: <script>eval(atob('base64code'))</script>",
            "category": "code_snippets",
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "Python code: import os; os.system('rm -rf /')",
            "category": "code_snippets",
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "Base64 encoded: dXNlckBleGFtcGxlLmNvbQ== (user@example.com)",
            "category": "code_snippets",
            "expected_entities": [("dXNlckBleGFtcGxlLmNvbQ==", "BASE64")],
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "JSON payload: {\"username\": \"admin\", \"password\": \"secret\"}",
            "category": "code_snippets",
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        {
            "text": "XML payload: <user><name>admin</name><pass>secret</pass></user>",
            "category": "code_snippets",
            "expected_intents": ["DETECT", "ANALYZE"]
        },
        
        # ========== MALWARE/RANSOMWARE (8 tests) ==========
        {
            "text": "Ransomware detected: WannaCry, NotPetya, Ryuk variants",
            "category": "malware_ransomware",
            "expected_entities": [
                ("WannaCry", "MALWARE_TYPE"),
                ("NotPetya", "MALWARE_TYPE"),
                ("Ryuk", "MALWARE_TYPE")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "Malware families: Zeus, Emotet, TrickBot, Emotet detected",
            "category": "malware_families",
            "expected_entities": [
                ("Zeus", "MALWARE_TYPE"),
                ("Emotet", "MALWARE_TYPE"),
                ("TrickBot", "MALWARE_TYPE")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "APT groups: APT29, APT28, Lazarus, FIN7, UNC2452",
            "category": "apt_groups",
            "expected_entities": [
                ("APT29", "THREAT_ACTOR"),
                ("APT28", "THREAT_ACTOR"),
                ("Lazarus", "THREAT_ACTOR"),
                ("FIN7", "THREAT_ACTOR"),
                ("UNC2452", "THREAT_ACTOR")
            ],
            "expected_intents": ["INVESTIGATE", "TRACK_ACTOR"]
        },
        {
            "text": "Trojan detected: Remote Access Trojan (RAT) variant",
            "category": "malware_types",
            "expected_entities": [("Remote Access Trojan", "MALWARE_TYPE")],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "Spyware: keylogger and screen capture malware detected",
            "category": "malware_types",
            "expected_entities": [
                ("keylogger", "MALWARE_TYPE"),
                ("screen capture", "MALWARE_TYPE")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "Rootkit detected: bootkit and kernel-level rootkit",
            "category": "malware_types",
            "expected_entities": [
                ("bootkit", "MALWARE_TYPE"),
                ("kernel-level rootkit", "MALWARE_TYPE")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "Botnet: Mirai, Emotet botnet, and TrickBot C2",
            "category": "malware_botnets",
            "expected_entities": [
                ("Mirai", "MALWARE_TYPE"),
                ("Emotet", "MALWARE_TYPE"),
                ("TrickBot", "MALWARE_TYPE")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        {
            "text": "Worm detected: Conficker, Stuxnet, and Code Red variants",
            "category": "malware_worms",
            "expected_entities": [
                ("Conficker", "MALWARE_TYPE"),
                ("Stuxnet", "MALWARE_TYPE"),
                ("Code Red", "MALWARE_TYPE")
            ],
            "expected_intents": ["DETECT", "INVESTIGATE"]
        },
        
        # ========== ADDITIONAL COMPLIANCE FRAMEWORKS (6 tests) ==========
        {
            "text": "Check compliance with NIST CSF, PCI DSS, and HIPAA requirements",
            "category": "compliance_frameworks",
            "expected_entities": [
                ("NIST CSF", "COMPLIANCE_FRAMEWORK"),
                ("PCI DSS", "COMPLIANCE_FRAMEWORK"),
                ("HIPAA", "COMPLIANCE_FRAMEWORK")
            ],
            "expected_intents": ["ENSURE_COMPLIANCE", "AUDIT_COMPLIANCE"]
        },
        {
            "text": "SOC 2 Type II audit and FedRAMP compliance check",
            "category": "compliance_frameworks",
            "expected_entities": [
                ("SOC 2 Type II", "COMPLIANCE_FRAMEWORK"),
                ("FedRAMP", "COMPLIANCE_FRAMEWORK")
            ],
            "expected_intents": ["AUDIT_COMPLIANCE", "ENSURE_COMPLIANCE"]
        },
        {
            "text": "CMMC Level 3 and CIS Controls compliance assessment",
            "category": "compliance_frameworks",
            "expected_entities": [
                ("CMMC Level 3", "COMPLIANCE_FRAMEWORK"),
                ("CIS Controls", "COMPLIANCE_FRAMEWORK")
            ],
            "expected_intents": ["ENSURE_COMPLIANCE", "AUDIT_COMPLIANCE"]
        },
        {
            "text": "OWASP Top 10 and SANS Top 25 security controls",
            "category": "compliance_frameworks",
            "expected_entities": [
                ("OWASP Top 10", "COMPLIANCE_FRAMEWORK"),
                ("SANS Top 25", "COMPLIANCE_FRAMEWORK")
            ],
            "expected_intents": ["ENSURE_COMPLIANCE", "AUDIT_COMPLIANCE"]
        },
        {
            "text": "FISMA and FIPS 140-2 compliance requirements",
            "category": "compliance_frameworks",
            "expected_entities": [
                ("FISMA", "COMPLIANCE_FRAMEWORK"),
                ("FIPS 140-2", "COMPLIANCE_FRAMEWORK")
            ],
            "expected_intents": ["ENSURE_COMPLIANCE", "AUDIT_COMPLIANCE"]
        },
        {
            "text": "CCPA and PIPEDA data privacy compliance",
            "category": "compliance_frameworks",
            "expected_entities": [
                ("CCPA", "COMPLIANCE_FRAMEWORK"),
                ("PIPEDA", "COMPLIANCE_FRAMEWORK")
            ],
            "expected_intents": ["ENSURE_COMPLIANCE", "AUDIT_COMPLIANCE"]
        },
        
        # ========== ADDITIONAL TIME FORMATS (6 tests) ==========
        {
            "text": "ISO 8601 timestamp: 2024-11-30T14:30:00Z and 2024-11-30T14:30:00+00:00",
            "category": "time_formats",
            "expected_entities": [
                ("2024-11-30T14:30:00Z", "DATE"),
                ("2024-11-30T14:30:00+00:00", "DATE")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "Unix timestamps: 1701350400 and 1701350400.123",
            "category": "time_formats",
            "expected_entities": [
                ("1701350400", "DATE"),
                ("1701350400.123", "DATE")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "Relative time: yesterday, last week, 24 hours ago, tomorrow, next month",
            "category": "time_formats",
            "expected_entities": [],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "Timezones: 2024-11-30 14:30 EST, 2024-11-30 14:30 PST, 2024-11-30 14:30 UTC",
            "category": "time_formats",
            "expected_entities": [
                ("2024-11-30 14:30 EST", "DATE"),
                ("2024-11-30 14:30 PST", "DATE"),
                ("2024-11-30 14:30 UTC", "DATE")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "Duration: 24 hours, 7 days, 30 minutes, 2 weeks",
            "category": "time_formats",
            "expected_entities": [],
            "expected_intents": ["INVESTIGATE"]
        },
        {
            "text": "Time ranges: 2024-11-01 to 2024-11-30, from 14:00 to 18:00",
            "category": "time_formats",
            "expected_entities": [
                ("2024-11-01", "DATE"),
                ("2024-11-30", "DATE"),
                ("14:00", "TIME"),
                ("18:00", "TIME")
            ],
            "expected_intents": ["INVESTIGATE"]
        },
        
        # ========== ADDITIONAL OSINT SCENARIOS (8 tests) ==========
        {
            "text": "Verify image metadata and check EXIF data for GPS coordinates",
            "category": "osint_image",
            "expected_intents": ["VERIFY_IMAGE", "EXTRACT_METADATA"]
        },
        {
            "text": "Verify video authenticity and check for deepfake indicators",
            "category": "osint_video",
            "expected_intents": ["VERIFY_VIDEO", "ANALYZE"]
        },
        {
            "text": "Verify social media profile @user123 and check for fake account indicators",
            "category": "osint_profile",
            "expected_entities": [("@user123", "USERNAME")],
            "expected_intents": ["VERIFY_PROFILE", "DEBUNK"]
        },
        {
            "text": "Debunk misinformation: fact-check claim about security breach",
            "category": "osint_debunk",
            "expected_intents": ["DEBUNK", "VERIFY"]
        },
        {
            "text": "Extract metadata from document: author, creation date, modification date",
            "category": "osint_metadata",
            "expected_intents": ["EXTRACT_METADATA", "ANALYZE"]
        },
        {
            "text": "Reverse image search: find original source of image",
            "category": "osint_reverse",
            "expected_intents": ["VERIFY_IMAGE", "INVESTIGATE"]
        },
        {
            "text": "Geolocation analysis: determine location from image metadata",
            "category": "osint_geolocation",
            "expected_intents": ["MAP", "INVESTIGATE"]
        },
        {
            "text": "Timeline analysis: correlate events across multiple sources",
            "category": "osint_timeline",
            "expected_intents": ["CORRELATE_EVENTS", "ANALYZE"]
        },
        
        # ========== ADDITIONAL CYBERSECURITY SCENARIOS (10 tests) ==========
        {
            "text": "Perform memory forensics on system dump memory.dmp",
            "category": "forensics_memory",
            "expected_intents": ["PERFORM_MEMORY_FORENSICS", "ANALYZE_MEMORY_DUMP"]
        },
        {
            "text": "Perform disk forensics on disk image disk.img",
            "category": "forensics_disk",
            "expected_intents": ["PERFORM_DISK_FORENSICS", "ANALYZE_DISK_IMAGE"]
        },
        {
            "text": "Hunt for APT activity and lateral movement indicators",
            "category": "threat_hunting",
            "expected_intents": ["HUNT_APT", "HUNT_LATERAL_MOVEMENT"]
        },
        {
            "text": "Report to law enforcement: cybercrime incident details",
            "category": "law_enforcement",
            "expected_intents": ["REPORT_TO_LAW_ENFORCEMENT", "DOCUMENT_INCIDENT"]
        },
        {
            "text": "Executive brief: prepare security incident report for board",
            "category": "executive_brief",
            "expected_intents": ["EXECUTIVE_BRIEF", "BOARD_BRIEF", "GENERATE_REPORTS"]
        },
        {
            "text": "Board brief: cybersecurity posture and risk assessment",
            "category": "board_brief",
            "expected_intents": ["BOARD_BRIEF", "EXECUTIVE_BRIEF", "REPORT_TO_BOARD"]
        },
        {
            "text": "Blue team defend: implement security controls and monitoring",
            "category": "blue_team",
            "expected_intents": ["BLUE_TEAM_DEFEND", "DEFEND", "MONITOR"]
        },
        {
            "text": "Blue team respond: incident response and containment",
            "category": "blue_team",
            "expected_intents": ["BLUE_TEAM_RESPOND", "RESPOND_TO_INCIDENT"]
        },
        {
            "text": "Penetration test: authorized security assessment",
            "category": "penetration_test",
            "expected_intents": ["PENETRATION_TEST", "PEN_TEST", "ASSESS_RISK"]
        },
        {
            "text": "Red team exercise: simulate adversary attack",
            "category": "red_team",
            "expected_intents": ["SIMULATE_COMPROMISE", "TEST_SECURITY"]
        },
    ]
    
    return test_cases

if __name__ == "__main__":
    test_cases = get_comprehensive_test_cases()
    print(f"Generated {len(test_cases)} comprehensive test cases")
    print(f"Categories: {len(set(tc['category'] for tc in test_cases))}")

