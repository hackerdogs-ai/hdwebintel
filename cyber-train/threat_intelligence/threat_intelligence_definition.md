# 🧠 Pillar 16: Threat Intelligence & Monitoring

**Scenarios to Protect:**

* Lack of visibility into emerging threats (malware, ransomware, APTs)
* Missed opportunities to proactively detect attackers before impact
* Disconnected SOC operations without enrichment from external CTI feeds
* Failure to comply with regulatory obligations (e.g., FS-ISAC for finance)

**Design Points:**

* Ingest and normalize internal + external threat feeds (OSINT, ISACs, commercial feeds)
* Correlate TI with SIEM/SOAR for detection and response
* Use frameworks like MITRE ATT\&CK, STIX/TAXII for structured intel
* Establish threat hunting functions and purple teaming
* Share validated intelligence with trusted communities

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Design, Oversight)**

* **CISO:** Owns enterprise threat intelligence (CTI) strategy, board reporting.
* **Principal Security Architect:** Designs CTI architecture (feeds, SIEM, SOAR, TIP).
* **Head of Threat Intelligence:** Leads CTI team, sets priorities, manages vendor relationships.

### **Execution Roles (Implementation, Operations, Monitoring)**

* **Threat Intelligence Analyst:** Collects, enriches, and analyzes CTI feeds.
* **SOC Analyst:** Consumes CTI for detection and alert triage.
* **Threat Hunter:** Proactively hunts for adversary TTPs in the environment.
* **Malware Analyst / Reverse Engineer:** Analyzes malware samples and creates signatures.
* **Incident Responder:** Uses CTI to contain incidents faster.
* **Red Team / Purple Team:** Uses CTI to emulate adversaries and validate defenses.
* **GRC Analyst:** Maps CTI-driven detections to compliance frameworks (NIST, ISO, PCI DSS).

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Ingest and normalize threat feeds (TI Analyst).
* Review new IOCs (indicators of compromise) and enrich with context.
* Correlate IOCs against SIEM logs for hits (SOC).
* Share validated intelligence internally and externally (MISP, ISAC).

### **Weekly Tasks**

* Update detection rules based on emerging threats (SOC + TI Analyst).
* Conduct hunts for new adversary TTPs in MITRE ATT\&CK (Threat Hunter).
* Reverse-engineer new malware samples (Malware Analyst).
* Track adversary campaigns relevant to sector/industry.

### **Monthly Tasks**

* Produce a threat landscape report for leadership.
* Map detection coverage to MITRE ATT\&CK heatmaps.
* Tune SIEM/SOAR rules for false positive reduction.
* Review intelligence sharing activity with partners.

### **Quarterly Tasks**

* Run purple team exercises with Red Team to test defenses against top threats.
* Evaluate CTI vendor feeds and adjust subscriptions.
* Conduct gap analysis of detection coverage vs. ATT\&CK matrix.
* Validate CTI integration with incident response workflows.

### **Yearly Tasks**

* Refresh CTI strategy and roadmap (CISO + Head of TI).
* Conduct enterprise threat modeling exercise.
* External audit of CTI maturity (using frameworks like CMMI-TI).
* Benchmark against peer organizations (ISAC/industry consortiums).

---

## 3. Tools Used

### **Top Open Source Tools**

1. **MISP** – Malware Information Sharing Platform.
2. **OpenCTI** – CTI platform for structured intel (STIX/TAXII).
3. **TheHive + Cortex** – Case management with TI enrichment.
4. **YARA** – Custom malware detection signatures.
5. **Sigma Rules** – Generic detection rules convertible to SIEM queries.
6. **Suricata / Zeek** – Network intrusion detection with TI feeds.
7. **Osquery** – Endpoint hunting.
8. **ELK Stack (ElasticSearch, Logstash, Kibana)** – Threat log analysis.
9. **ATT\&CK Navigator (MITRE)** – Visualize TTP detection coverage.
10. **IntelMQ** – Threat feed processing and automation.

### **Top Commercial Tools**

1. **Recorded Future** – Threat intel platform with contextual enrichment.
2. **Anomali ThreatStream** – Threat intel aggregation and distribution.
3. **ThreatConnect** – CTI management + orchestration.
4. **CrowdStrike Falcon X** – Threat intel and malware analysis.
5. **Palo Alto AutoFocus** – Threat intel platform.
6. **Flashpoint** – Deep/dark web threat intel.
7. **IBM X-Force Exchange** – Commercial threat feed + analysis.
8. **FireEye/Mandiant Threat Intelligence** – Adversary-focused intel.
9. **Check Point ThreatCloud** – Network threat intel.
10. **Cisco Talos** – Global TI + integration with Cisco products.

---

## 4. Problems Solved & Expected Success Rate

* **Blindness to Emerging Threats:** External TI reduces unknown threats by \~70–80%.
* **Slow Detection & Response:** CTI-enriched alerts reduce MTTD/MTTR by \~50%.
* **Reinventing the Wheel:** Shared intelligence prevents duplication of effort (\~80% faster IOC validation).
* **Adversary Simulation Gaps:** Threat-informed red/purple teaming increases detection resilience by \~60–70%.
* **Compliance Failures:** Mapped TI ensures \~100% alignment with frameworks requiring threat monitoring.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Threat Intelligence & Monitoring Pillar:**

* 🧾 **# of Threat Feeds Integrated & Actively Used**
* 📊 **IOC Coverage % (IPs/domains/hashes tracked vs. acted upon)**
* ⏱ **Mean Time from IOC Publication → Actionable Detection**
* 🚨 **# of Threat Hunts Conducted per Month**
* 🕵️ **Detection Coverage Against MITRE ATT\&CK (heatmap %)**
* 📉 **False Positive Rate of TI-driven Alerts**
* 🌐 **# of Shared Intelligence Contributions (MISP/ISAC)**
* 👥 **Red/Purple Team Simulation Success Rate vs. CTI**
* 📋 **Compliance Mapping Coverage (PCI DSS, HIPAA, NIST)**
* 📈 **Trends in Sector-Specific Threats Over Time**

---


