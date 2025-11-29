Perfect ✅ — I see the **pillar template** and the **OSINT pillars table**.

From the table, **Pillar 3 is IMINT (Imagery Intelligence)**. You already have Step 1 (Pillar Definition). Now we must deliver **Step 2: Dashboard Definition** — in the *exact same style, sections, and headings* as the SOCMINT dashboard template in the document.

---

# 📊 IMINT Dashboard Definition 🛰️🖼️

---

## **1. Dashboard Purpose**

Provide **real-time and historical visibility into imagery intelligence** across satellite, aerial, UAV, and ground images. The dashboard supports:

* **Executives (strategic):** decision-making for crises, infrastructure risk, sanctions, and compliance.
* **Analysts (operational):** daily monitoring, object detection, change detection, geolocation, and media verification.

---

## **2. Dashboard Sections**

### **A. Executive Overview (Strategic View)**

**Widgets:**

* 🛰 **AOI Coverage Rate (Gauge):** % of priority Areas of Interest imaged in the last 7/30/90 days.
* 🚨 **Incident Detection Lead Time (KPI Card):** average hours from imagery collection → analyst alert.
* 📈 **Facility Growth/Change Index (Trend Line):** major infrastructure changes validated per quarter.
* 🌍 **Global Risk Heatmap (Choropleth):** regions with most IMINT alerts (conflict, disaster, infra risk).
* 💰 **Cost-per-AOI (Bar Chart):** imagery spend vs. coverage efficiency.

---

### **B. Real-Time Monitoring (Analyst View)**

**Widgets:**

* 🔴 **Live Imagery & Alerts Feed (Table):** new satellite/aerial scenes, anomalies flagged by models.
* 🧭 **Interactive AOI Map (Geospatial Panel):** clickable AOIs with overlays (EO, SAR, IR imagery).
* 🏗 **Facility Change Detector (Before/After Panel):** side-by-side imagery comparison of sites.
* 🚢 **Maritime/Aviation Overlays (Layered Map):** ship/aircraft detections matched to AIS/ADS-B.
* 📷 **Media Verification Queue (Panel):** user-generated photos/videos requiring geolocation and chronolocation.

---

### **C. Object & Change Detection Analysis**

**Widgets:**

* 🚗 **Object Detection Counts (Bar Chart):** # vehicles, aircraft, vessels detected per AOI.
* 🏭 **Infrastructure Monitoring Grid (Matrix):** ports, bases, energy facilities with activity scores.
* 🌐 **Change Detection Timeline (Line Chart):** frequency of validated site changes.
* 🧩 **Cross-Pillar Validation (Table):** SOCMINT/HUMINT correlation with IMINT findings.

---

### **D. Trend & Risk Analysis**

**Widgets:**

* 📈 **Environmental Impact Layer (Map Overlay):** deforestation, emissions, wildfires, floods.
* 🔍 **Geolocation Accuracy Tracker (Gauge):** % correctly validated coordinates from imagery.
* 🕰 **Chronolocation Precision Tracker (Timeline):** accuracy of time-of-day validation via shadows/metadata.
* 📰 **Narrative Overlay Correlation (Table):** alignment of media/social narratives with IMINT evidence.

---

### **E. Alerts & Incident Response**

**Widgets:**

* 🔔 **Active IMINT Alerts (Card Stack):** P1–P3 alerts (conflict, disaster, sanctions evasion).
* 🛠 **Alert Escalation Funnel:** % of alerts triaged → escalated → acted on → resolved.
* ⏱ **Crisis Response Lead Time (KPI):** hours between IMINT alert and executive/media reporting.
* 📑 **Case Management Integration (Embedded Panel):** push alerts into TheHive, Jira, ServiceNow.

---

### **F. Compliance & Audit**

**Widgets:**

* 📋 **Imagery Collection Audit Log (Table):** metadata (sensor, provider, timestamp, license).
* 🛡 **Policy & Licensing Tracker (Gauge):** % compliance with ToS, export controls, retention.
* 🧩 **Cross-Pillar Validation Rate (Bar Chart):** % IMINT findings validated by SOCMINT/GEOINT/HUMINT.

---

## **3. Metrics (Aligned to Step 1)**

**Strategic Metrics (Executive Level):**

* 🛰 AOI Coverage Rate (% of AOIs monitored)
* 🚨 Incident Detection Lead Time (hrs)
* 📈 Facility Growth/Change Index (# per quarter)
* 💰 Cost-per-AOI (\$ vs. coverage efficiency)
* 🛡 Risk Reduction Score (impact on crisis outcomes)

**Operational Metrics (Analyst Level):**

* 📍 Geolocation Accuracy (% correctly validated coordinates)
* ⏰ Chronolocation Precision (% within ±2h)
* 🎯 Object Detection Precision/Recall (by class: vehicles, aircraft, vessels)
* 📊 Cloud-Free Imagery % (usable EO imagery per AOI)
* 🧩 Cross-Pillar Validation Rate (% confirmed by SOCMINT/HUMINT)

---

## **4. Dashboard Technology & Implementation**

* **Visualization Layer:** Streamlit (analyst dashboards), Grafana (real-time KPIs), Kibana (event timelines).
* **Geospatial Tools:** CesiumJS, Leaflet.js, ArcGIS Online for maps and overlays.
* **Data Sources:** Maxar, Planet, Airbus, Capella SAR, ICEYE, SkyWatch APIs.
* **AI/ML Integration:** TensorFlow/PyTorch models for object detection, change detection, and anomaly scoring.
* **Alerting & Workflow:** Slack, Teams, Email, SOAR connectors (e.g., Cortex XSOAR).
* **Storage & Processing:** PostgreSQL/PostGIS, S3/Blob storage for imagery, ElasticSearch for logs.

---

## **5. Example Layout (IMINT Fusion Dashboard)**

* **Top Bar:** Filters (Date Range, AOI, Facility Type, Sensor Type, Risk Level).
* **Left Panel:** Navigation (Executive, Real-Time, Detection, Trends, Alerts, Compliance).
* **Main Grid:**

  * **Top row:** KPIs (AOI Coverage, Lead Time, Change Index, Cost-per-AOI).
  * **Middle row:** AOI Map, Facility Change Detector, Object Counts.
  * **Bottom row:** Environmental Impact Map, Narrative Overlay, Active Alerts.

---

✅ This completes **Step 2: Dashboard Definition for IMINT**, built exactly in the template style from SOCMINT.

Would you like me to now proceed to **Step 3: Agents & Tasks YAMLs for IMINT** (crewAI spec), or pause here for your review?
