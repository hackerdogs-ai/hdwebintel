✅ Noted: From here on, I will **strictly follow the exact template** you approved for **Pillar 1 (SOCMINT)** — no deviations in headings, order, or structure.

Now continuing with **Pillar 2: GEOINT (Geospatial Intelligence) — Step 2: Dashboard Definition**, keeping the same level of quality and consistency.

---

# 📊 GEOINT Dashboard Definition 🛰️🌍

---

## **1. Dashboard Purpose**

Provide **real-time and historical geospatial intelligence** for monitoring activities, validating events, and supporting decision-making. The dashboard must serve both:

* **Executives (strategic):** risk assessment, crisis monitoring, and geopolitical decision support.
* **Analysts (operational):** daily monitoring, geolocation verification, chronolocation, and activity mapping.

---

## **2. Dashboard Sections**

### **A. Executive Overview (Strategic View)**

**Widgets:**

* 🛰 **Imagery Coverage Rate (Gauge):** % of priority AOIs covered in last 7/30/90 days.
* 🚨 **Crisis Detection Lead Time (KPI Card):** average hours from crisis onset → analyst alert.
* 📈 **Geospatial Risk Score (Composite Index):** weighted metric combining detected anomalies, facility changes, and illicit activity.
* 🌍 **Global AOI Heatmap (Choropleth):** high-risk regions highlighted by recent GEOINT alerts.
* 🗂 **Change Detection Timeline (Line Chart):** volume of validated geospatial changes over time.

---

### **B. Real-Time Monitoring (Analyst View)**

**Widgets:**

* 🔴 **Live Imagery & Alerts Feed (Stream Table):** new satellite passes, flagged anomalies, AIS/ADS-B events.
* 🧭 **Interactive AOI Map (Geospatial Panel):** clickable AOIs with active alerts, imagery overlays, and recent changes.
* 🚢 **Maritime & Aviation Tracker (Dual Map/Table):** AIS vessel positions + ADS-B aircraft activity with anomaly alerts.
* 🏗 **Facility Change Detector (Image Comparison Widget):** before/after snapshots of sites (military bases, infrastructure).
* 📷 **Photo/Video Verification Queue (Panel):** analyst queue for UGC needing geolocation/chronolocation validation.

---

### **C. Campaign & Pattern Analysis**

**Widgets:**

* 🗂 **Infrastructure Monitoring Dashboard (Bar/Heatmap):** frequency of construction, deforestation, mining activity across AOIs.
* 🌐 **Regional Activity Graph (Force Graph):** link analysis of facilities, transport routes, and detected events.
* 🧑‍🤝‍🧑 **Actor & Facility Profiles (Card Grid):** dossiers of flagged facilities, organizations, or shipping companies.
* 📊 **Platform/Data Source Coverage (Matrix Table):** imagery sources, AIS/ADS-B feeds, and cross-validation status.

---

### **D. Trend & Risk Analysis**

**Widgets:**

* 📈 **Risk Trend Line (Time Series):** long-term changes in regional threat/risk levels.
* 🌍 **Environmental Impact Layer (Map Overlay):** deforestation, emissions, oil spills.
* 🗣 **Narrative Overlay Integration (Table):** correlation of SOCMINT narratives with GEOINT observations.
* 📰 **Chronolocation Accuracy Tracker (Timeline):** accuracy rates for time-validation of visual media.

---

### **E. Alerts & Incident Response**

**Widgets:**

* 🔔 **Active Geospatial Alerts (Card Stack):** high-priority AOI alerts requiring action.
* 🛠 **Alert Escalation Tracker (Funnel):** % of GEOINT alerts escalated → acted upon → resolved.
* ⏱ **Crisis Response Lead Time (KPI):** time delta between GEOINT alert vs. mainstream media.
* 📑 **Case Management Integration (Embedded Panel):** auto-link alerts to TheHive, Jira, or ServiceNow for follow-up.

---

### **F. Compliance & Audit**

**Widgets:**

* 📋 **Collection & Imagery Audit Log (Table):** metadata of imagery collected (source, timestamp, resolution, provider).
* 🧩 **Cross-Pillar Validation Rate (Bar Chart):** % of GEOINT findings confirmed by SOCMINT/HUMINT/SIGINT.
* 🛡 **Policy Compliance Tracker (Gauge):** adherence to privacy, ToS, and international satellite imagery laws.

---

## **3. Metrics (Aligned to Step 1)**

**Strategic Metrics (Executive Level):**

* 🛰 Imagery Coverage Rate (% AOIs monitored per period)
* 🚨 Crisis Detection Lead Time (hours/days)
* 📈 Geospatial Risk Score (composite)
* 🗂 Change Detection Index (# validated site/facility changes per period)

**Operational Metrics (Analyst Level):**

* 📍 Geolocation Accuracy (% correctly validated coordinates)
* ⏰ Chronolocation Precision (% time estimates within ±2h)
* 🚢 Maritime/Aviation Coverage (% AIS/ADS-B anomalies tracked)
* 🗂 Reports Delivered (# tactical/strategic briefs produced)
* 🧩 Cross-Pillar Validation Rate (% confirmed with SOCMINT/HUMINT)

---

## **4. Dashboard Technology & Implementation**

* **Visualization Layer:** Streamlit (analyst dashboards), Grafana (real-time metrics), Kibana (timeline correlation).
* **Mapping/Geospatial:** Leaflet.js, CesiumJS, ArcGIS Online for 3D and AOI overlays.
* **Graph Engine:** Neo4j, NetworkX, or Gephi integration for facility/route graphs.
* **Data Sources:** Sentinel/Planet/Maxar imagery APIs, AIS (MarineTraffic), ADS-B (ADS-B Exchange).
* **Alerting:** Slack, MS Teams, Email, Webhooks.
* **Storage & Processing:** PostgreSQL/PostGIS for geospatial data, ElasticSearch for logs, S3 for imagery.

---

## **5. Example Layout (GEOINT Fusion Dashboard)**

* **Top Bar:** Filters (Date Range, AOI, Facility Type, Source, Risk Level).
* **Left Panel:** Navigation (Executive, Real-Time, Campaigns, Trends, Alerts, Compliance).
* **Main Grid:**

  * **Top row:** KPIs (Coverage Rate, Risk Score, Lead Time, Change Detection Index).
  * **Middle row:** AOI Map, Maritime/Aviation Tracker, Facility Change Detector.
  * **Bottom row:** Sentiment/Narrative Overlay, Environmental Impact Map, Active Alerts Panel.

---

✅ This is the **Step 2: Dashboard Definition for GEOINT**, built with the **exact same headings and structure as SOCMINT** — ensuring template consistency.

---

Do you want me to continue straight into **Step 3: Crewai Agents & Tasks (agents.yaml and tasks.yaml for GEOINT)**, or pause here for your validation?
