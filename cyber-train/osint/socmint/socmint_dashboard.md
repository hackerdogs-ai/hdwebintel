Perfect — we’ll stay disciplined 🔒 and fully finish **Pillar 1: SOCMINT** before moving on.
You want **Step 2: Dashboard Definition** — a **world-class, production-grade SOCMINT dashboard spec** with clear sections, metrics, and widget definitions.

Here’s the complete design:

---

# 📊 Step 2: SOCMINT Dashboard Definition

---

## **1. Dashboard Purpose**

Provide real-time and historical visibility into **social media threats, disinformation, sentiment, and influence operations**, supporting **analysts (operational)** and **executives (strategic)** with tailored views.

---

## **2. Dashboard Sections**

### **A. Executive Overview (Strategic View)**

* **Widgets:**

  * 🛡 **Brand Risk Score** (Gauge) – composite metric of negative mentions, impersonation, coordinated campaigns.
  * 🎭 **Influence Operation Detection Rate** (KPI Card) – % campaigns identified this quarter.
  * ⏱ **Time-to-Detection** (Trend Line) – average hours from campaign onset → analyst alert.
  * 🌍 **Top Global Narrative Map** (Heatmap/Choropleth) – trending disinformation topics by region.
  * 📈 **Narrative Momentum Index** (Line Chart) – spread velocity of key topics over time.

---

### **B. Real-Time Monitoring (Analyst View)**

* **Widgets:**

  * 🔴 **Live Feed Stream** (Table/Feed) – flagged posts, hashtags, mentions, and URLs in real time.
  * 🧭 **Geotagged Activity Map** (Interactive Map) – plotting protests, disasters, or conflicts.
  * 🕵️ **Bot/Account Alerts** (Card + Table) – suspicious account detection with confidence scores.
  * 📢 **Top Trending Hashtags/Keywords** (Word Cloud + Bar Chart).
  * 🎥 **Media Verification Queue** (Panel) – flagged images/videos requiring analyst validation (integrated with reverse image & deepfake detection).

---

### **C. Campaign & Network Analysis**

* **Widgets:**

  * 🗂 **Active Campaigns Timeline** (Gantt/Timeline Chart) – lifecycle of disinfo campaigns.
  * 🌐 **Influence Graph** (Force-Directed Graph via Gephi/NetworkX) – nodes (accounts), edges (interactions), color-coded for bot/human.
  * 🧑‍🤝‍🧑 **Actor Dossier Panel** (Card/Grid) – profiles of top spreaders, bots, or influencers.
  * 📊 **Platform Coverage Matrix** (Table) – # of mentions, bot detections, alerts per platform.

---

### **D. Sentiment & Trend Analysis**

* **Widgets:**

  * 😀😡😱 **Sentiment Breakdown** (Donut Chart) – positive, negative, neutral proportions.
  * 📈 **Sentiment Trend Line** – time series of sentiment change for key narratives.
  * 🗣 **Top Influencers & Amplifiers** (Leaderboard Table) – ranked by engagement & reach.
  * 📰 **Narrative Evolution Tree** (Sankey Diagram) – how stories mutate across platforms.

---

### **E. Alerts & Incident Response**

* **Widgets:**

  * 🔔 **Active Alerts Panel** (Card Stack) – high-priority incidents needing action.
  * 🛠 **Alert-to-Action Tracker** (Funnel) – % of alerts escalated, acted on, closed.
  * ⏱ **Crisis Response Lead Time** (KPI) – time delta between SOCMINT alert vs. mainstream media.
  * 📑 **Case Management Integration** (Embedded Panel) – link SOCMINT alerts → TheHive/Jira/ServiceNow tickets.

---

### **F. Compliance & Audit**

* **Widgets:**

  * 📋 **Collection Audit Log** (Table) – metadata of each collected item (timestamp, source, method).
  * 🧩 **Cross-Pillar Validation Rate** (Bar Chart) – % SOCMINT findings confirmed by GEOINT/HUMINT.
  * 🛡 **Policy Compliance Tracker** (Gauge) – monitoring GDPR/platform ToS adherence.

---

## **3. Metrics (Aligned to Step 1)**

* **Strategic Metrics:**

  * Narrative Momentum Index
  * Influence Operation Detection Rate
  * Brand Risk Score
  * Time-to-Detection (TTD)

* **Operational Metrics:**

  * Bot Detection Precision/Recall
  * Platform Coverage (# platforms, # languages)
  * Alert Actionability %
  * Cross-Pillar Validation Rate
  * Crisis Response Lead Time

---

## **4. Dashboard Technology & Implementation**

* **Visualization Layer:** Streamlit (OSINT-specific dashboards), Grafana (real-time metrics), Kibana (timeline/event correlation).
* **Data Processing:** ElasticSearch + OpenCTI for indexing and graph relationships.
* **Graph Engine:** Gephi, Neo4j, or NetworkX for social network visualizations.
* **Alerting:** Slack/Teams/Webhooks + Email for dissemination.
* **Storage:** PostgreSQL for structured data; S3/Blob for media.

---

## **5. Example Layout (SOCMINT Fusion Dashboard)**

* **Top Bar:** Filter (Date Range, Platform, Region, Language, Narrative)
* **Left Panel:** Navigation (Executive, Real-Time, Campaigns, Sentiment, Alerts, Compliance)
* **Main Grid:**

  * Top row: KPIs (Brand Risk Score, TTD, Detection Rate, Crisis Lead Time)
  * Middle row: Real-Time Feed, Map, Trending Hashtags, Influence Graph
  * Bottom row: Sentiment Breakdown, Narrative Tree, Alerts Panel

---

✅ This is a **production-grade SOCMINT dashboard spec** with **sections, metrics, and widget definitions** aligned to the Step 1 pillar definition.

---

👉 Do you want me to now move to **Step 3: Agents & Tasks (agents.yaml + tasks.yaml) for SOCMINT**, or should I expand this dashboard definition with **mock visual examples/wireframes** (e.g., Streamlit/Grafana widget layouts) before coding YAML?
