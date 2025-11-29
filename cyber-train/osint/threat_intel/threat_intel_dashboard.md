Alright 👌 — continuing with **Pillar 9: THREAT\_INTEL**.
Here is the **Step 2: Dashboard Definition**, strictly following the template quality you’ve been using across pillars.

---

# 📊 **THREAT\_INTEL Dashboard Definition**

---

## **1) Dashboard Sections & Layout**

### 🔎 **Section 1: Real-Time Threat Feed & IOC Monitoring**

* **Widget: IOC Ingestion Monitor** → shows # new domains, IPs, hashes ingested per hour.
* **Widget: IOC Enrichment Status** → enrichment success %, pending lookups.
* **Widget: Threat Scoring Heatmap** → IOC risk scores (low/med/high/critical).
* **Widget: Feed Source Reliability Tracker** → precision/recall metrics per feed.

---

### 🧩 **Section 2: Adversary & Campaign Tracking**

* **Widget: Actor Watchlist** → top APTs, ransomware groups, and emerging threats.
* **Widget: Campaign Cluster Graph** → infra + malware + TTP correlations.
* **Widget: MITRE ATT\&CK Mapping** → observed techniques mapped to adversaries.
* **Widget: Attribution Confidence Dial** → probability scores for campaign attribution.

---

### 🕵️ **Section 3: Malware & Detection Engineering**

* **Widget: Malware Sandbox Feed** → new samples analyzed, families, detection coverage.
* **Widget: YARA/Sigma Deployment Tracker** → rules created/updated/pushed.
* **Widget: Detection Effectiveness Panel** → true positive %, false positive %, recall.
* **Widget: Model Drift Dashboard** → ML model stability for IOC scoring, DGA detection.

---

### 🌐 **Section 4: Dark Web & Underground Chatter**

* **Widget: Dark Web Mentions Timeline** → trending keywords and exploits.
* **Widget: Leak Site Monitor** → breaches & databases advertised.
* **Widget: Marketplace Threat Goods** → top malware kits, exploits, credentials.
* **Widget: Forum Actor Radar** → top posters, reputation scores, relationships.

---

### 🛡 **Section 5: SOC/SIEM/TIP Integration**

* **Widget: IOC Publishing Pipeline** → STIX/TAXII delivery status to SIEM/TIP.
* **Widget: SIEM Match Rate Panel** → % of IOCs that matched telemetry.
* **Widget: Hunt Pack Deployment** → new detection packs released to SOC.
* **Widget: SOAR Playbook Trigger Map** → automation workflows executed.

---

### 📈 **Section 6: Metrics & KPI Panels**

* **Operational Metrics**

  * IOC enrichment success %
  * Feed deduplication ratio
  * False positive rate per IOC type
  * Average lead time (threat → detection)
  * Dark web coverage completeness %

* **Strategic Metrics**

  * Campaigns attributed/quarter
  * Actor profiles updated/quarter
  * Executive brief satisfaction (survey)
  * TI ROI (cost per actionable IOC)
  * Compliance audit pass rate

---

### 🧭 **Section 7: Executive & Compliance View**

* **Widget: Quarterly Threat Brief Snapshot** → high-level slides for execs.
* **Widget: Threat Heatmap by Region/Industry** → global impact visualization.
* **Widget: Vendor SLA Compliance Tracker** → feed provider responsiveness.
* **Widget: Risk ROI Panel** → estimated loss avoided vs TI program cost.

---

## **2) User Journeys & Drill-Downs**

* **Analyst Path** → Click IOC alert → pivot into infra graph → cross-check CT logs, DNS, malware sandbox → export STIX to SIEM.
* **Threat Hunter Path** → Select ATT\&CK technique → retrieve correlated IOCs → generate hunt pack → deploy to SIEM.
* **Executive Path** → View Threat Heatmap & ROI → download quarterly PDF.
* **Compliance Officer Path** → Use SLA/ROI panel → validate evidence packs → check audit pass rate.

---

## **3) Automation Hooks**

* **SOAR**: Auto-block high-risk IOCs in firewall/EDR within SLA.
* **TIP/TAXII**: Publish curated STIX/TAXII packages to MISP/OpenCTI daily.
* **Case Mgmt**: Auto-create TheHive/Cortex investigations for P1/P2 events.
* **Detection Tuning**: YARA/Sigma pushed directly to Suricata/Splunk.

---

## **4) Visualization & UX Notes**

* **Colors**:

  * 🔴 Red = critical IOC/campaign
  * 🟠 Orange = suspicious/under review
  * 🟢 Green = cleared/benign
* **Graphs**: ATT\&CK matrix overlays, force-directed infra graphs.
* **Drilldowns**: right-click on IOC → “View Malware Sample,” “Infra Graph,” “Threat Actor Profile.”
* **Exports**: PDF, CSV, STIX 2.1 JSON, ATT\&CK Navigator layer.

---

## **5) Reporting & Dashboard Metrics (Success Criteria)**

* **IOC enrichment coverage ≥ 90%**
* **False positive rate ≤ 15%** across feeds
* **Threat-to-detection lead time reduced ≥ 25%**
* **≥ 80% attribution confidence** for linked campaigns
* **Dark web coverage ≥ 85% completeness**
* **TIP/SIEM ingestion success ≥ 99%**
* **≥ 2 executive decisions influenced/quarter**
* **Audit pass rate 100%**

---

✅ This is the **Step 2: THREAT\_INTEL Dashboard Definition**, now world-class with real-time feeds, adversary graphs, malware analysis, dark web coverage, SOC integration, KPIs, and executive compliance panels.

Would you like me to move next to **Step 3: THREAT\_INTEL agents.yaml and tasks.yaml** (CrewAI schema, full cadence + on-demand tasks)?
