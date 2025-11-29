Excellent 👍 — let’s build **Step 2: Dashboard Definition for COMINT (Pillar 6)**.
This follows the **pillar template** you provided: purpose, sections, widgets, metrics, technology, and layout.

---

# 📊 **Step 2: COMINT Dashboard Definition** 📞

---

## **1. Dashboard Purpose**

The COMINT dashboard provides **real-time visibility, transcription, analysis, and validation of open communications** (radio, VoIP, satcom). It helps:

* **Executives**: assess comms-related risks, fraud campaigns, and compliance posture.
* **Analysts**: monitor live comms, run anomaly detection, and correlate chatter with other OSINT pillars (HUMINT, SIGINT, SOCMINT).

---

## **2. Dashboard Sections**

### **A. Executive Overview (Strategic View)**

**Widgets**

* 📡 **COMINT Anomalies Detected (Gauge):** # anomalies validated vs. false positives.
* 🌍 **Global COMINT Heatmap (Choropleth):** chatter intensity by AOI/frequency band.
* 📞 **VoIP Fraud Alerts (Card):** count + severity of active fraud/vishing campaigns.
* 📊 **Executive Risk Index (Trend Line):** aggregated COMINT threat index (0–100).
* 🏢 **Decisions Influenced (Counter):** # of executive actions tied to COMINT reporting.

---

### **B. Operational Monitoring (Analyst View)**

**Widgets**

* 🎧 **Live Comms Monitor (Waveform + Spectrogram):** real-time audio/RF visualization.
* 📝 **Live Transcription Feed (Panel):** streaming transcription w/ language detection.
* 📋 **Anomaly Feed (Table):** flagged conversations, keywords, call patterns.
* 🔎 **Source Provenance Tracker (Table):** comms metadata, geolocation, SDR IDs.
* 📞 **VoIP Metadata Analyzer (Panel):** suspicious call patterns, C2-style behaviors.

---

### **C. Transcription & Language Analytics**

**Widgets**

* 🗣️ **Language ID Distribution (Pie Chart):** % of conversations by language.
* 📚 **Keyword Spotting (Word Cloud/Table):** flagged terms, frequency, risk tags.
* 👥 **Speaker Clustering (Graph):** voiceprints grouped into speaker identities.
* 📊 **Confidence Score Gauge:** transcription accuracy % and validation rate.

---

### **D. Threat & Narrative Analysis**

**Widgets**

* ⚠️ **Fraud/Scam Campaign Tracker (Timeline):** major call campaign events.
* 🎯 **Actor Network Map (Interactive):** voice IDs → HUMINT actor profiles.
* 📻 **Emergency Broadcast Anomalies (Card):** manipulated or spoofed alerts flagged.
* 📈 **Trend Over Time (Line Chart):** anomalies/week and risk severity.
* 🧩 **Cross-Pillar Validation Table:** COMINT chatter confirmed by HUMINT/SIGINT.

---

### **E. Alerts & Incident Response**

**Widgets**

* 🔔 **Active COMINT Threat Alerts (Card Stack):** ongoing P1/P2 anomalies.
* 🛠️ **Alert Workflow Funnel (Funnel Chart):** anomaly → triage → escalation → closure.
* ⏱️ **Mean Time-to-Transcription (KPI):** average time from comms capture to usable transcript.
* 📑 **Case Management Integration (Embedded):** links to TheHive/Jira/ServiceNow.

---

### **F. Compliance & Audit**

**Widgets**

* 📋 **Collection Log (Table):** metadata of comms collected (time, frequency, classification).
* 🔒 **Compliance Gauge:** % adherence to privacy/legal filters.
* 📊 **Audit Findings (Bar Chart):** # of open vs. resolved compliance issues.
* 🧾 **Data Minimization Tracker (Stacked Chart):** retention adherence & anonymization applied.

---

## **3. Metrics (Aligned to Step 1)**

**Strategic Metrics (Executive Level)**

* # anomalies detected & validated per week/month.
* Mean time-to-detection (MTTD) of suspicious comms.
* Transcription accuracy rate (%).
* Risk index (0–100) for comms-related threats.
* Cross-pillar validation % of COMINT reports.
* Compliance adherence %.

**Operational Metrics (Analyst Level)**

* Daily anomaly feed volume.
* Avg. time-to-transcription (minutes).
* False positive / false negative rates on keyword spotting.
* Speaker clustering accuracy %.
* Active case queue length and closure rates.

---

## **4. Dashboard Technology & Implementation**

* **Visualization Layer:** Streamlit (analyst workflow), Grafana (real-time feeds), PowerBI/Tableau (executive reporting).
* **Signal Capture:** GNU Radio, GQRX, SDRangel for RF; Wireshark SIP/RTP plugins for VoIP.
* **Speech Processing:** Whisper.cpp, DeepSpeech, commercial APIs (Nexidia, Verint).
* **Storage:** PostgreSQL + TimescaleDB for comms metadata; VictoriaLogs for logs.
* **Alerting:** Slack/Teams, Jira, TheHive connectors.
* **ML/NLP Models:** transcription accuracy, keyword spotting, language ID, speaker clustering.

---

## **5. Example Layout (COMINT Fusion Dashboard)**

* **Top Bar:** Filters (Date, AOI, Source Type: Radio/VoIP, Language, Severity).
* **Left Panel:** Navigation (Executive, Operational, Transcription, Threats, Alerts, Compliance).
* **Main Grid:**

  * **Top row:** KPIs (Anomalies, Risk Index, Compliance Gauge).
  * **Middle row:** Live Comms Monitor, Transcription Feed, Anomaly Table.
  * **Bottom row:** Actor Network Map, Cross-Pillar Validation, Audit Log.

---

✅ This completes **Step 2: COMINT Dashboard Definition (Pillar 6)** in template quality.

Would you like me to proceed with **Step 3: COMINT Agents & Tasks YAML (CrewAI schema-compliant with on-demand + cadence tasks)** next?
