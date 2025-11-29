# 🚨 Pillar 9: Incident / Emergency Response

**Scenarios to Protect:**

* Security breaches (malware, ransomware, insider threat, data exfiltration)
* Large-scale operational incidents (network outages, supply chain compromise)
* Business continuity threats (natural disasters, systemic failures)

**Design Points:**

* Incident Response (IR) plan aligned with NIST 800-61, ISO 27035, and MITRE ATT\&CK
* Defined playbooks for ransomware, phishing, insider threat, data breach
* Roles and responsibilities formalized (Incident Commander, SOC, Comms)
* Post-Incident Reviews (PIR) and lessons learned integrated into improvements

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Design, Oversight)**

* **CISO:** Owns incident response strategy, reporting to executives and board.
* **Principal Security Architect:** Designs IR architecture (SIEM/SOAR integrations, automation).
* **Head of Incident Response / IR Manager:** Maintains playbooks, coordinates IR team readiness, ensures testing and exercises.

### **Execution Roles (Response, Operations, Monitoring)**

* **Incident Commander (IC):** Leads response efforts, coordinates stakeholders, makes containment decisions.
* **SOC Analyst (Tier 1–3):** Detects, triages, and escalates incidents.
* **Forensic Analyst:** Collects and analyzes artifacts (disk, memory, logs).
* **Malware Analyst / Threat Researcher:** Investigates samples, creates detection signatures.
* **Communications Lead (Comms/Case Manager):** Manages stakeholder updates, legal notifications, PR.
* **Legal & Compliance Officer:** Advises on regulatory breach notifications.
* **Red Team / Purple Team:** Validates detection and response effectiveness.
* **Business Continuity Manager:** Ensures alignment with disaster recovery (DR/BCP).

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Monitor SIEM/SOAR alerts for potential incidents (SOC).
* Triage suspicious activity and escalate confirmed incidents.
* Execute containment actions (account disable, block IP, isolate host).

### **Weekly Tasks**

* Run tabletop or simulation exercises for specific scenarios (e.g., phishing, ransomware).
* Validate incident ticket SLAs are met (IR Manager).
* Tune detection rules in SIEM/EDR/SOAR based on recent alerts.

### **Monthly Tasks**

* Generate IR metrics report for leadership (IR Manager).
* Review and refine incident playbooks.
* Conduct log and forensic tool validation (Forensics team).
* Coordinate with Legal for any reportable events.

### **Quarterly Tasks**

* Perform Red Team vs. Blue Team simulation (Purple Teaming).
* Conduct business continuity and DR drills.
* Audit IR readiness (contacts updated, tools tested, SLAs tracked).
* Review external incident case studies and update defenses.

### **Yearly Tasks**

* Full-scale enterprise-wide incident simulation (ransomware/data breach).
* Update IR policy and framework based on lessons learned.
* External penetration testing & breach simulation assessments.
* Validate compliance-driven IR requirements (e.g., PCI DSS, HIPAA breach notification timelines).

---

## 3. Tools Used

### **Top Open Source Tools**

1. **TheHive Project** – Case management for incidents.
2. **Cortex (TheHive companion)** – Automated analysis and enrichment.
3. **MISP (Malware Information Sharing Platform)** – Threat intel sharing.
4. **GRR Rapid Response** – Remote live forensics.
5. **Velociraptor** – Endpoint DFIR platform.
6. **OSQuery** – Endpoint investigation queries.
7. **Security Onion** – Detection, monitoring, response platform.
8. **Wazuh** – SIEM + response automation.
9. **YARA** – Malware signature scanning.
10. **Logstash/ELK** – Incident log correlation and analysis.

### **Top Commercial Tools**

1. **Splunk SOAR (Phantom)** – Automated IR playbooks.
2. **Cortex XSOAR (Palo Alto)** – Orchestrated incident response.
3. **Microsoft Sentinel** – Cloud-native SIEM/SOAR.
4. **CrowdStrike Falcon XDR** – Integrated IR and threat hunting.
5. **FireEye Helix** – Managed IR and detection.
6. **IBM Resilient** – Case management and IR orchestration.
7. **Rapid7 InsightConnect** – SOAR and IR automation.
8. **PagerDuty** – Incident escalation and comms.
9. **ServiceNow IR Module** – IR workflow and tracking.
10. **Dragos Platform** – IR for OT/ICS environments.

---

## 4. Problems Solved & Expected Success Rate

* **Delayed Detection:** SIEM/SOAR automation reduces detection time by \~70%.
* **Inefficient Response:** Playbooks cut containment/eradication time by \~50%.
* **Human Error in Crisis:** Formal IC role and structured comms reduce missteps (\~90% success in coordination).
* **Forensics Gaps:** DFIR tools improve evidence collection completeness (\~85–90%).
* **Regulatory Failures:** Automated tracking of notification timelines ensures \~100% compliance.
* **Recurrent Issues:** PIRs + Purple Teaming reduce recurrence of similar incidents by \~60–70%.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Incident / Emergency Response Pillar:**

* 🚨 **Mean Time to Detect (MTTD)** and **Mean Time to Respond (MTTR)**
* 📊 **Number of Incidents by Severity** (critical/high/medium/low)
* 🕵️ **% Incidents Escalated vs. False Positives**
* 🔒 **Containment SLA Compliance %** (e.g., critical incidents contained <1 hour)
* 🧾 **Regulatory Notification SLA Compliance %** (HIPAA, GDPR timelines)
* 👥 **# of Incidents per Business Unit** (insight into weak areas)
* 📉 **Repeat Incident Rate** (same root cause recurring)
* ⏱ **Time to First Response (TTFR)** per incident type
* 🧪 **Incident Simulation Frequency & Pass Rate**
* 🌐 **# of Shared Incidents with External Threat Intel Feeds (MISP, ISACs)**

---


