Perfect 👍 — continuing with **Pillar 6: COMINT (Communications Intelligence from Open Sources)**.
This will follow your **pillar template** strictly: six numbered sections, ≥10 OSS + ≥10 commercial tools, cadence, reporting metrics, and problems solved.

---

# 📞 **Step 1: Pillar Definition – COMINT (Communications Intelligence from Open Sources)**

---

### **1. Scenarios to Protect**

* 📡 Monitoring **unsecured VoIP, radio, or push-to-talk communications** linked to criminal or extremist groups.
* 📞 Detecting **fraudulent call campaigns** (vishing, robocalls, scam centers).
* 🎧 Identifying **interceptable open radio chatter** in conflict or crisis zones.
* 🛰️ Collecting **public satcom signals** or maritime/aviation distress communications.
* 📻 Capturing **emergency services leaks** (non-encrypted police/fire chatter).
* 🔊 Detecting **pirate radio stations** used for illicit propaganda.
* 🕵️ Identifying **covert communications** hidden in open ham radio / shortwave bands.
* 🌐 Tracking **VoIP abuse for command-and-control** (botnets, fraud rings).
* 🚨 Monitoring **emergency broadcasts** for disinformation or manipulation.
* 🛡️ Detecting **espionage tradecraft** using amateur comms for cover.

---

### **2. Design Points**

* 📶 **Source scope**: open/public comms only (shortwave, ham, VHF/UHF, VoIP metadata).
* 🔐 **Compliance**: collect **only non-encrypted, publicly accessible comms**.
* 🔍 **Fusion**: COMINT → supports HUMINT (actor ID), SIGINT (technical RF), SOCMINT (actor chatter).
* 🧩 **Correlation**: tie comms anomalies to geospatial activity (GEOINT) or signal baselines (SIGINT).
* 📊 **Automation**: SDR & speech-to-text pipelines for large-scale capture & transcription.
* 🧪 **AI/ML**: NLP models for speaker clustering, language ID, and intent classification.
* ⚖️ **Ethical design**: filter out PII, apply strict audit trails, role-based access.
* 🔄 **Operational link**: COMINT often forms **tactical intelligence** for incident response.

---

### **3. Roles & Ownership**

**🎯 Strategic Roles**

* Director of Intelligence / National Security Lead.
* Head of Crisis Operations / Incident Commander.
* CISO / Chief Risk Officer.
* Communications Policy & Compliance Officer.

**🛠 Operational Roles**

* COMINT Collection Officer (radio & VoIP sweeps).
* Voice/Language Analyst (transcription & translation).
* COMINT Data Engineer (pipeline, SDR, transcription QC).
* Network Telephony Analyst (VoIP anomalies, call metadata).
* Spectrum/Radio Monitoring Analyst.
* NLP Model Engineer (speaker ID, keyword spotting).

---

### **4. Role Tasks & Cadence**

**Daily 🗓️**

* Monitor radio/VoIP channels for anomalies, keywords, threat chatter.
* Transcribe open comms into searchable text.
* Flag high-risk or suspicious call activity.

**Weekly 📅**

* Produce summaries of open comms activity by AOI.
* Update voice/language models with new accents or slang.
* Review VoIP metadata anomalies.

**Monthly 📆**

* Compile COMINT intelligence reports for execs & SOC teams.
* Cross-pillar validation (COMINT → HUMINT/SIGINT).
* Update watchlists (keywords, frequencies, call numbers).

**Quarterly 📤**

* Run tabletop crisis simulations with COMINT injects.
* Conduct compliance audits (legality, minimization).
* Refresh SDR pipeline and transcription accuracy benchmarks.

**Yearly 📈**

* Strategic review: COMINT coverage, sources, compliance frameworks.
* Vendor/tool assessment and upgrades.
* Red-team COMINT deception tests (false chatter injections).

---

### **5. Tools & Reporting**

**🧑‍💻 Open-Source Tools (≥10)**

1. GNU Radio
2. GQRX (SDR signal monitoring)
3. SDRangel
4. gr-gsm (GSM comms decoding)
5. DeepSpeech / Whisper.cpp (speech-to-text)
6. Audacity (audio analysis)
7. SigDigger (signal analysis)
8. rtl\_433 (decode IoT/SCADA chatter)
9. Wireshark VoIP plugins (SIP/RTP analysis)
10. Kismet (radio/Wi-Fi scanning)
11. Sonobus (low-latency VoIP capture OSS)

**💼 Commercial Tools (≥10)**

1. Babel Street / Babel X Voice Intelligence
2. Palantir Gotham (COMINT fusion)
3. Thales COMINT systems
4. Rohde & Schwarz COMINT suite (EB500, DDF family)
5. Keysight VoIP Monitoring & Anomaly Detection
6. NICE Nexidia (speech analytics)
7. Verint Voice Intelligence
8. Fivecast Onyx (multi-INT integration)
9. Dataminr (real-time voice/event alerts)
10. Cobwebs Technologies COMINT modules
11. Blackdot Solutions Videris (telephony integration)

**📊 Reporting & Dashboard Metrics**

* # of COMINT anomalies detected per day/week.
* % of anomalies validated by HUMINT/SIGINT.
* Mean time-to-transcription (minutes).
* Voice/language model accuracy (%).
* False positive/false negative rates on keyword spotting.
* Executive decisions influenced by COMINT.
* Compliance adherence (audit logs closed).

---

### **6. Problems Solved & Expected Success Metrics**

**🔒 Problems Solved**

* Detects open comms used by criminals/extremists.
* Identifies fraudulent VoIP or call campaign patterns.
* Provides tactical warning for crisis response.
* Validates HUMINT claims with real comms chatter.
* Bridges spectrum intelligence (SIGINT) with narrative analysis (SOCMINT).
* Enables executive awareness of comms-based threats.

**📊 Expected Success Metrics**

* ≥90% validated transcription accuracy.
* Mean time-to-detection for suspicious comms ≤ 10 minutes.
* ≥80% of COMINT anomalies cross-validated with other INTs.
* ≥95% uptime of COMINT monitoring pipelines.
* ≥4 executive decisions per quarter influenced by COMINT reporting.
* Stakeholder satisfaction ≥ 4.5/5.

---

✅ This completes **Step 1: Pillar Definition for COMINT (Pillar 6)** in world-class format.

Would you like me to now continue to **Step 2: COMINT Dashboard Definition** (sections, widgets, metrics, layout) just like we did for SIGINT and HUMINT?
