Excellent 🚀 — moving to **Pillar 5: SIGINT (Signals Intelligence from Open Sources)**.
I will adhere **strictly** to the six-part template, with ≥10 OSS + ≥10 commercial tools, cadence, metrics, and problems solved.

---

# 📡 **Step 1: Pillar Definition – SIGINT (Signals Intelligence from Open Sources)**

---

### **1. Scenarios to Protect**

* 📶 Detection of suspicious radio, Wi-Fi, or Bluetooth activity near sensitive facilities.
* 🛰️ Monitoring satellite communications for illicit or adversarial transmissions.
* 📡 Tracking maritime/aviation signals (AIS/ADSB) for spoofing or anomalies.
* 📱 Identifying IMSI catchers or rogue base stations targeting employees.
* 📻 Interception of unencrypted VHF/UHF comms used by illicit actors.
* 🔊 Monitoring push-to-talk and walkie-talkie chatter in crisis zones.
* 🌐 Detecting cross-border smuggling routes via signal anomalies.
* 🎯 Pinpointing hostile RF jamming or GPS spoofing attempts.
* 🛰️ Identifying foreign SIGINT collection around critical infrastructure.
* 🛡️ Monitoring for cyber-physical attacks that use wireless vectors (IoT exploitation, RF hacking).

---

### **2. Design Points**

* 📡 **Signal coverage**: include RF spectrum (HF/VHF/UHF), satellite, cellular (2G–5G), Wi-Fi/Bluetooth, and IoT protocols.
* 🔐 **Legality**: only unencrypted or lawfully accessible signals are collected.
* 🔍 **Correlation**: signals → geolocation (GEOINT), identity resolution (HUMINT), activity patterns (SOCMINT).
* 🧩 **Automation**: SDR (software-defined radio) pipelines for scanning & anomaly detection.
* 🛰️ **Fusion**: AIS/ADSB/SIGINT fusion to track maritime/aviation anomalies.
* 📊 **Analytics**: anomaly scoring models for spoofing/jamming detection.
* 🛡️ **Red-teaming**: periodic spoof/jam simulations to validate defenses.
* ⚖️ **Data minimization**: only retain metadata for compliance/privacy.
* 🔄 **Cross-pillar flow**: SIGINT triggers GEOINT (AOI validation) or SOCMINT (actor chatter).

---

### **3. Roles & Ownership**

**🎯 Strategic Roles**

* Chief Information Security Officer (CISO).
* Director of Threat Intelligence.
* Head of Spectrum Security.
* National Security Liaison Officer.

**🛠 Operational Roles**

* SIGINT Analyst (SDR operations).
* RF Data Engineer (signal pipeline engineer).
* Spectrum Threat Hunter.
* Aviation/Maritime Signal Specialist.
* Jamming/Spoofing Incident Responder.
* Compliance & Privacy Officer.

---

### **4. Role Tasks & Cadence**

**Daily 🗓️**

* Continuous SDR spectrum scanning for anomalies.
* AIS/ADSB spoofing detection.
* Rogue Wi-Fi/IMSI catcher detection.

**Weekly 📅**

* Compile weekly SIGINT anomaly summaries.
* Update RF anomaly models and thresholds.
* Review maritime/aviation anomaly alerts.

**Monthly 📆**

* Generate signal environment baselines by AOI.
* Correlate SIGINT anomalies with HUMINT/SOCMINT reports.
* Update adversary TTP mapping for signal spoofing/jamming.

**Quarterly 📤**

* Conduct red-team SIGINT spoofing/jamming drills.
* Executive SIGINT threat posture briefings.
* Audit signal metadata retention for compliance.

**Yearly 📈**

* Refresh SIGINT strategy (coverage, vendors, models).
* Vendor/tool evaluation and upgrade cycles.
* National security exercise participation (multi-pillar).

---

### **5. Tools & Reporting**

**🧑‍💻 Top Open-Source Tools (10+)**

1. GNU Radio
2. GQRX
3. SigDigger
4. gr-gsm (GSM decoding)
5. dump1090 (ADSB decoding)
6. rtl\_433 (IoT/SCADA signals)
7. OpenCPN (AIS integration)
8. SatDump (satellite signal analysis)
9. Kismet (Wi-Fi/Bluetooth scanning)
10. Wireshark (protocol analysis)
11. SDRangel

**💼 Top Commercial Tools (10+)**

1. Palantir Gotham (SIGINT integration)
2. BlackSky Spectra
3. HawkEye 360 (RF geolocation from space)
4. Thales RESOLVE
5. Keysight Signal Analyzer
6. Rohde & Schwarz PR200/EB500
7. CRFS RFeye
8. SignalGuard
9. Spectrum Guard (Maritime/Border)
10. TCI International Monitoring Systems
11. Dataminr Pulse (integrated alerts)

**📊 Reporting & Dashboard Metrics**

* # of daily RF anomalies detected.
* % of anomalies validated as true positives.
* Mean time-to-detection for spoofing/jamming.
* Signal environment baseline variance (by AOI).
* Cross-pillar correlation % (SIGINT validated by GEOINT/IMINT).
* Executive risk index for spectrum threats.
* Stakeholder satisfaction with SIGINT reporting.

---

### **6. Problems Solved & Expected Success Metrics**

**🔒 Problems Solved**

* Detects spoofing/jamming attempts before operational impact.
* Identifies illicit maritime/aviation “dark” activities.
* Provides early warning for insider/activist use of rogue signals.
* Validates HUMINT claims with technical RF data.
* Strengthens cyber-physical defense against RF-enabled attacks.
* Informs compliance and audit reports for lawful SIGINT.

**📊 Expected Success Metrics**

* ≥90% true positive rate on validated anomalies.
* Mean time-to-detection ≤ 15 minutes for spoofing/jamming.
* ≥80% of SIGINT anomalies cross-validated with other INTs.
* ≥95% uptime of SDR monitoring pipeline.
* ≥3 executive decisions per quarter supported by SIGINT insights.
* Stakeholder satisfaction ≥ 4.5/5 on SIGINT briefs.

---

✅ This completes **Step 1: Pillar Definition for SIGINT (Pillar 5)** in strict template format.

Would you like me to proceed with **Step 2: SIGINT Dashboard Definition** (sections, widgets, metrics, tech stack) — same world-class style we used for SOCMINT, IMINT, and HUMINT?
