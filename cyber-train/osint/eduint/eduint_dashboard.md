# 📊 Pillar 24: EDUINT (Educational Intelligence) — Step 2: Dashboard Definition

## 1) Dashboard Purpose

Deliver a unified strategic + operational view of the global education ecosystem—research output, collaborations, funding, mobility, campus risk, and dual-use exposure—so leaders can anticipate technology shifts, spot influence/espionage vectors, and prioritize interventions.

---

## 2) Dashboard Sections

### A) Executive Overview (Strategic)

* **🎯 EDUINT Risk Index (Gauge):** Composite score from dual-use exposure, suspicious collaborations, campus unrest, and cyber incidents.
* **📈 Research Velocity (Sparkline KPIs):** Preprints/day, grants/week, patents/month; 7/30/90-day deltas.
* **🌍 Collaboration Heatmap (Choropleth):** Cross-border co-authorship & funding ties by country/region.
* **🧪 Dual-Use Exposure (Treemap):** Share of outputs in AI/biotech/quantum/aero/defense; drill into institutions.
* **💡 Executive Insights (Narrative):** LLM-generated summary of top shifts, risks, and recommended actions.

### B) Real-Time Monitoring (Operational)

* **📰 Live Research Feed (Table):** New arXiv/PubMed/Scopus entries with topics, affiliations, funding, OA links.
* **🏫 Campus Events & Activism (Ticker):** Event mentions, protest alerts, incident geotags; severity & confidence.
* **🔐 Academic Cyber Watch (Panel):** EDU-sector phishing, credential dumps, compromised lab pages; IOC quick-add.
* **🏷 Funding Announcements (Cards):** Grants/tenders with donor origin classification (domestic/foreign/state-linked).
* **🔎 Credential/Publication Verification (Widget):** On-click verification status (DOI/ORCID/affiliation match).

### C) Campaign, Actor & Network Analysis

* **🧩 Researcher Graph (Force Graph):** ORCID ↔ co-author ↔ institution; centrality, community detection.
* **🤝 Institution-to-Sponsor Matrix (Bipartite Heatmap):** Funding flows to labs/departments; highlight foreign/state-linked.
* **🕵️ Influence/Transfer Watch (Caseboard):** Possible tech-transfer vectors; linked publications, patents, travel, and grants.
* **🗺 Mobility Flows (Chord/Flow Map):** Student/faculty movement between regions; directionality & volume.

### D) Trend & Benchmarking

* **📊 Topic Trajectories (Multi-Series):** Growth/decline of critical domains (AI safety, gene editing, hypersonics).
* **🧫 Dual-Use Risk Trend (Stacked Area):** Proportion of flagged outputs per month; compare peers/countries.
* **🏅 Institution Benchmarking (Ranked Bars):** Output, impact, dual-use share, cyber incidents per 10k researchers.
* **🔁 Replication & Retraction Tracker (Timeseries + Table):** Retractions/expressions of concern by field/institution.

### E) Alerts & Incident Response

* **🔔 Active Alerts (Queue):** Triggers for suspicious collaboration, sudden topic spikes, activism escalation, cyber overlap.
* **⏱ MTTD/MTTR (KPI):** Time to detect & resolve EDU incidents; SLO thermometer vs targets.
* **📂 Case Management (Embedded):** Create/attach cases in TheHive/Jira; artifact checklist; chain-of-custody.
* **🧷 Watchlists (Panel):** Entities (institutions, labs, PIs) under review; add/remove with justification.

### F) Compliance & Audit

* **📑 Export-Control Screen (Grid):** EAR/ITAR red flags, dual-use classification, license needs; exception queue.
* **🔒 Privacy & Data Handling (Scorecard):** FERPA/GDPR posture; data minimization & retention status.
* **📜 Funding Source Integrity (Traffic-Light Table):** High-risk donors and recurring opaque intermediaries.
* **🧭 Policy Actions Log (Table):** Approvals/denials, disclosures, COIs; audit trail with signatures.

---

## 3) Metrics

### Strategic (Executive)

* **EDUINT Risk Index** (0–100) and change vs last quarter
* **Dual-Use Exposure %** by domain & institution
* **Foreign-linked Funding %** (tiered by risk)
* **Coverage Rate** (% institutions/labs tracked vs target)
* **Cross-Pillar Confirmation Rate** (EDUINT ↔ CYBINT/THREAT\_INTEL)

### Operational (Analyst)

* **TTD/MTTR** for EDU alerts (hrs)
* **Verification Accuracy** (DOI/ORCID/affiliation match rate)
* **Topic Classifier Precision/Recall/F1** (per domain)
* **Protest Detection Precision/Recall** (with false-positive rate)
* **Grant → Output Latency** (median days from award to first output)

---

## 4) Dashboard Technology & Implementation

* **Ingestion:** ArXiv, Crossref, PubMed, OpenAlex, ORCID, institutions’ RSS; grants/tenders portals; social & news feeds.
* **Pipelines:** Kafka → dbt/Logstash → Elasticsearch/Postgres/TimescaleDB; batch + streaming lanes.
* **NLP/ML:** Hugging Face topic & dual-use classifiers; NER for entities; weak-supervision labeling; dedup.
* **Graph:** Neo4j for co-author/funder networks; Graph Data Science for centrality/community/drift.
* **UI/Vis:** Streamlit (analyst UI), Grafana/Kibana (timeseries & search), Kepler.gl/Mapbox (geo).
* **Case & TI:** TheHive/Jira for cases; OpenCTI/MISP for indicators; export-control rules engine.
* **Controls:** PII minimization, COI flags, audit logging, role-based redaction; configurable retention.

---

## 5) Example Layout (One-Page “Fusion”)

**Top Filters:** Date range, Region, Institution, Domain, Risk tier, Funding origin
**Row 1 (Exec KPIs):** EDUINT Risk Index • Dual-Use % • Foreign-Funding % • Coverage % • TTD/MTTR
**Row 2:** Collaboration Heatmap • Live Research Feed • Funding Announcements
**Row 3:** Researcher Graph • Institution-Sponsor Matrix • Mobility Flows
**Row 4:** Topic Trajectories • Dual-Use Trend • Institution Benchmarking
**Row 5:** Alerts Queue • Case Management • Compliance Scorecard & Actions Log

---

### Widget Definitions (selected)

* **Live Research Feed:** columns = title, DOI, authors, ORCID match %, institutions, domain tags, dual-use score, link.
* **EDUINT Risk Index:** weighted: dual-use (35%), foreign-funding risk (25%), activism/cyber overlap (20%), anomalous patterns (20%).
* **Institution-Sponsor Matrix:** cells show funding \$ and risk tier; click to open grant docs, disclosures, and linked outputs.
* **Cross-Pillar Overlay:** toggle to overlay CYBINT incidents and THREAT\_INTEL narratives on EDUINT entities.

---

If this matches your bar, I’ll proceed to **Step 3: EDUINT agents.yaml & tasks.yaml** (CrewAI-compliant, with on-demand + cadence tasks and structured expected outputs).
