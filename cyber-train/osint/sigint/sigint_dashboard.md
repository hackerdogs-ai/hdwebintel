Perfect ✅ — let’s build **Step 2: Dashboard Definition for SIGINT (Pillar 5)**.
I’ll follow the **pillar template** strictly: purpose, sections, widgets, metrics, tech stack, and layout.

---

# 📊 **Step 2: SIGINT Dashboard Definition** 📡

---

## **1. Dashboard Purpose**

The SIGINT dashboard provides **real-time visibility into spectrum activity, anomalies, and validated threats**. It supports both **executive decision-making** (strategic risk, compliance, posture) and **operational response** (alerts, jamming/spoofing detection, maritime/aviation anomaly tracking).

* **Executives (strategic view):** high-level risk index, validated anomaly counts, compliance metrics.
* **Analysts (operational view):** live spectrum data, anomaly feeds, network maps, model performance.

---

## **2. Dashboard Sections**

### **A. Executive Overview (Strategic View)**

**Widgets:**

* 📶 **SIGINT Anomalies Detected (Gauge):** # validated anomalies vs. false positives.
* 🛰️ **Global RF Threat Heatmap (Choropleth):** anomaly density by region/AOI.
* ⚡ **Jamming & Spoofing Alerts (Card):** active critical RF threats.
* 📊 **Executive Risk Index (Trend Line):** cumulative spectrum risk score (0–100).
* 🏢 **Decisions Influenced (Counter):** # of executive actions supported by SIGINT.

---

### **B. Operational Monitoring (Analyst View)**

**Widgets:**

* 📡 **Live Spectrum Monitor (Spectrogram/Waterfall):** real-time SDR visualization.
* 🕵️ **Anomaly Feed (Table):** list of flagged signals, severity, geolocation.
* 🚢 **Maritime/Aviation Activity (Map Overlay):** AIS/ADSB anomalies, spoofing tracks.
* 📶 **IMSI Catcher / Rogue Tower Detection (Alerts Panel):** active detections.
* 🔍 **Source Provenance Tracker (Table):** anomaly metadata, SDR IDs, validation status.

---

### **C. Signal Environment Baselines**

**Widgets:**

* 📈 **Baseline Variance Trend (Line Chart):** changes from AOI baseline.
* 🗺️ **AOI Signal Map (Interactive):** spectrum intensity overlay per area.
* 📊 **Protocol Distribution (Pie Chart):** % HF/VHF/UHF/Cellular/IoT signals.
* 🧭 **Drift Detection (Gauge):** baseline drift % beyond acceptable thresholds.

---

### **D. Threat & Anomaly Analysis**

**Widgets:**

* 📊 **Spoofing Detection Confidence (Bar Chart):** probability scores by anomaly.
* ⚠️ **RF Jamming Incidents (Time Series):** incident frequency and severity.
* 🛰️ **Satellite Signal Activity (Panel):** anomalies in Satcom channels.
* 🔎 **Cross-Pillar Correlation (Table):** % of SIGINT anomalies validated by GEOINT/IMINT/SOCMINT.
* 🧪 **Deception Detection (Gauge):** false anomaly identification rate.

---

### **E. Alerts & Incident Response**

**Widgets:**

* 🔔 **Active RF Threat Alerts (Card Stack):** P1/P2 anomalies requiring triage.
* 🛠️ **Alert Workflow Funnel (Funnel Chart):** detection → triage → escalation.
* ⏱️ **Mean Time to Detection (KPI):** average anomaly detection time.
* 📑 **Case Management Integration (Embedded):** TheHive/ServiceNow cases linked.

---

### **F. Compliance & Audit**

**Widgets:**

* 📋 **SIGINT Collection Log (Table):** metadata of collected anomalies (time, AOI, classification).
* 🔒 **Compliance Gauge:** % of SIGINT activities meeting privacy/legal thresholds.
* 📊 **Audit Findings (Bar Chart):** resolved vs. open compliance findings.
* 🧩 **Retention & Minimization Tracker (Stacked Chart):** adherence to data retention limits.

---

## **3. Metrics (Aligned to Step 1)**

**Strategic Metrics (Executive Level):**

* # anomalies detected & validated per quarter.
* Mean time-to-detection (MTTD) for spoofing/jamming.
* Spectrum risk index (0–100).
* % SIGINT anomalies cross-pillar validated.
* Compliance adherence rate (%).

**Operational Metrics (Analyst Level):**

* Daily anomaly feed volume (validated vs. false positives).
* Baseline drift % by AOI.
* Protocol distribution trends.
* RF pipeline uptime (%).
* Source credibility/provenance score averages.

---

## **4. Dashboard Technology & Implementation**

* **Visualization Layer:** Grafana (real-time SDR feeds), Streamlit (analyst workflows), PowerBI/Tableau (executive briefs).
* **Signal Capture:** GNU Radio, SDRangel, SatDump, rtl\_433, dump1090.
* **Geospatial Layer:** ArcGIS, QGIS, OpenCPN for AIS/ADSB overlays.
* **Storage:** PostgreSQL + TimescaleDB for signals; VictoriaLogs/Loki for telemetry.
* **Alerting:** Slack/Teams/Jira/TheHive connectors.
* **ML Models:** anomaly detection, spoofing/jamming classifiers, baseline drift detectors.

---

## **5. Example Layout (SIGINT Fusion Dashboard)**

* **Top Bar:** Filters (Date Range, AOI, Signal Type, Protocol, Severity).
* **Left Panel:** Navigation (Executive, Operational, Baselines, Threats, Alerts, Compliance).
* **Main Grid:**

  * **Top row:** KPIs (Anomalies, Risk Index, Compliance Gauge).
  * **Middle row:** Spectrum Monitor, Anomaly Feed, Maritime/Aviation Map.
  * **Bottom row:** Baseline Variance, Cross-Pillar Validation Table, Audit Log.

---

✅ That completes **Step 2: SIGINT Dashboard Definition** in the required template style.

Would you like me to now proceed with **Step 3: SIGINT Agents & Tasks YAML** (CrewAI schema-compliant, with both cadence + on-demand tasks)?
