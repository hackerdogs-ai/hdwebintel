Perfect 👍 Thanks for clarifying.
We’ll now work on **Pillar 9: THREAT\_INTEL (Threat Intelligence)** — strictly following your **Pillar template** (5 numbered sections, structured, world-class, with ≥10 OSS and ≥10 commercial tools, emojis, problems solved, success metrics, reporting & cadence).

---

# 🛡 **Step 1: THREAT\_INTEL Pillar Definition**

---

## **1. Pillar Overview**

**Definition:**
Threat Intelligence (THREAT\_INTEL) focuses on the systematic collection, analysis, enrichment, and dissemination of adversary tactics, techniques, procedures (TTPs), indicators of compromise (IOCs), and campaign-level insights from open, deep, dark, and technical sources.

**Purpose:**

* Enable proactive defense by detecting threats before exploitation.
* Enrich SOC, SIEM, and SOAR workflows with curated intelligence.
* Support strategic decision-making by CISOs, SOC leads, and executives.
* Enable cross-pillar correlation (e.g., linking CYBINT, DOMAIN\_INTEL, and HUMINT).

**Scope:**
Covers tactical (IOCs), operational (campaigns, threat groups), and strategic (geopolitical, risk context) intelligence.

---

## **2. Key Scenarios**

1. 🔍 **IOC Enrichment** – Identify, validate, and enrich IOCs (domains, IPs, hashes).
2. ⚔️ **Adversary Tracking** – Monitor APTs, cybercriminal gangs, ransomware affiliates.
3. 🧩 **Campaign Attribution** – Link campaigns across malware, infra, and TTPs.
4. 📊 **Threat Landscape Reports** – Generate quarterly threat briefs for executives.
5. ⚡ **Real-time Threat Feeds** – Stream curated intel to SIEM/TIP/SOAR platforms.
6. 🛡 **Threat Hunting Support** – Supply enriched TTPs for hunt missions.
7. 🌐 **Dark Web & Forums Monitoring** – Detect chatter, leaked data, or exploits.
8. 🏛 **Compliance & Governance** – Support NIST, ISO, SOC2, GDPR, and sector mandates.
9. 🧭 **Fusion & Correlation** – Cross-reference intel with SOC telemetry and OSINT pillars.
10. 🧠 **Machine Learning & Automation** – Apply AI to deduplicate, score, and prioritize threats.

---

## **3. Role Tasks & Cadence**

### 🎯 **Strategic Roles**

* **Threat Intelligence Strategist** – Aligns TI program with org risk posture, manages vendors.
* **CISO / Exec Stakeholders** – Consume high-level threat reports, track ROI of TI.

### ⚙️ **Operational Roles**

* **Threat Intel Analyst (Tactical/Operational)** – Collects and enriches IOCs, monitors threat actors.
* **Malware Researcher** – Reverse engineers samples, produces YARA/Sigma rules.
* **Dark Web Analyst** – Monitors underground forums, leak sites, marketplaces.
* **Data Engineer** – Maintains pipelines for feeds, normalization, enrichment.

### 📅 **Cadence**

* **On-Demand:** IOC investigation, malware analysis, actor profile update.
* **Daily:** Feed ingestion, IOC deduplication, intel scoring, publication.
* **Weekly:** Actor tracking, campaign linkage, dark web monitoring summaries.
* **Monthly:** Threat landscape reporting, hunting packs, detection tuning.
* **Quarterly:** Executive briefs, maturity assessments, vendor reviews.
* **Yearly:** Strategy refresh, budget & roadmap alignment.

---

## **4. Tools & Platforms**

### 🔓 **Open Source Tools (≥10)**

1. **MISP** – Threat intel platform & IOC correlation.
2. **OpenCTI** – Collaborative threat intelligence knowledge base.
3. **YARA** – Malware signature rules.
4. **Sigma** – Generic SIEM detection rules.
5. **Suricata** – IDS/IPS rules for network threats.
6. **TheHive** – Case management & incident correlation.
7. **Cortex** – IOC enrichment engine.
8. **OSINT Framework** – Collection pathways for open threat data.
9. **IntelMQ** – Threat data pipeline automation.
10. **Yeti** – TI management and IOC enrichment platform.
11. **Harpoon** – IOC hunting & enrichment tool.
12. **CAPEv2** – Malware sandbox for behavior analysis.

### 💼 **Commercial Tools (≥10)**

1. **Recorded Future** – Strategic and tactical TI feeds.
2. **Anomali ThreatStream** – Threat intel platform with multi-source integration.
3. **ThreatConnect** – TIP with automation, scoring, and workflows.
4. **CrowdStrike Falcon Intelligence** – Adversary TTPs and reports.
5. **FireEye/Mandiant Advantage** – APT group intelligence & campaign insights.
6. **Kaspersky Threat Intelligence Portal** – Malware & IOC data at scale.
7. **Group-IB Threat Intelligence** – Underground monitoring, fraud intel.
8. **Flashpoint** – Deep/dark web monitoring.
9. **Intel 471** – Adversary tracking and dark web monitoring.
10. **EclecticIQ Platform** – Threat intel management.
11. **Palo Alto AutoFocus** – Malware/IOC intelligence enrichment.
12. **Check Point ThreatCloud** – Global network-based TI.

---

## **5. Problems Solved & Success Metrics**

### ⚡ **Problems Solved**

* Overload of raw feeds without context → normalized, enriched, and prioritized intelligence.
* Siloed data in SOC/SIEM/SOAR → centralized TIP integration.
* Delayed detection of campaigns → proactive actor tracking and infrastructure correlation.
* Low exec visibility into TI ROI → quarterly strategic briefs and metrics.
* Fragmented dark web coverage → consolidated forum and marketplace monitoring.

### 📈 **Success Metrics**

* **IOC Enrichment Coverage ≥ 90%** (vs. raw feed).
* **False Positive Reduction ≥ 30%** in IOC feeds.
* **Threat-to-Detection Lead Time** reduced by ≥ 25%.
* **≥ 85% Correlation Accuracy** for campaign clustering.
* **Executive Satisfaction ≥ 4.5/5** on briefs.
* **TIP/SIEM Ingestion Success ≥ 99%**.
* **IOC efficacy (hit rate in SIEM hunts) ≥ 70%**.
* **Compliance Audit Pass Rate 100%**.

---

✅ This completes **Step 1: THREAT\_INTEL Pillar Definition** in your strict template style.
Would you like me to now move on to **Step 2: THREAT\_INTEL Dashboard Definition** (sections, widgets, metrics, automation hooks, reporting)?
