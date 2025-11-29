# 💻 Pillar 8: Endpoint / Terminal Security

**Scenarios to Protect:**

* Employee laptops, desktops, and mobile devices
* Servers (physical, virtual, cloud-based)
* Remote/hybrid work devices
* Preventing malware, ransomware, insider misuse, and data leakage

**Design Points:**

* Standardized endpoint baseline images (secure configuration)
* Endpoint Detection & Response (EDR) or Extended Detection & Response (XDR)
* Mobile Device Management (MDM) + Zero Trust posture enforcement
* Disk encryption and DLP (Data Loss Prevention)
* Continuous monitoring and automated remediation

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Design, Governance)**

* **CISO:** Owns enterprise endpoint security strategy and posture reporting.
* **Principal Security Architect:** Designs endpoint security architecture (EDR/XDR, MDM, DLP, hardening standards).
* **Head of Endpoint Security / Device Security Manager:** Defines baselines, drives endpoint security roadmap, vendor management.

### **Execution Roles (Implementation, Operations, Monitoring)**

* **Endpoint Security Engineer:** Manages EDR/AV/patching platforms, configures policies.
* **SOC Analyst:** Monitors endpoint alerts (malware, ransomware, insider activity).
* **IT Helpdesk / Desktop Support:** Implements baseline configs, remediates user issues, enforces MDM policies.
* **Patch Management Engineer:** Applies OS/application updates.
* **Incident Responder:** Contains and remediates endpoint compromises.
* **Forensic Analyst:** Investigates infected/compromised endpoints (malware samples, memory dumps).
* **Red Team / Pen Tester:** Simulates endpoint compromise and lateral movement.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* SOC Analysts review endpoint alerts (malware, privilege misuse).
* Endpoint Engineers validate EDR health and sensor coverage.
* Helpdesk resets/re-enrolls devices into MDM after issues.
* Patch Team handles critical out-of-band updates.

### **Weekly Tasks**

* Apply OS/application patches to pilot groups (Patch Engineer).
* Review blocked/quarantined files from EDR (SOC).
* Analyze suspicious PowerShell/macOS/Linux scripts (SOC + IR).
* Validate compliance of new device enrollments (Endpoint Engineer).

### **Monthly Tasks**

* Push enterprise patch cycle across OS/apps (Patch Mgmt).
* Review endpoint compliance reports (MDM/DLP coverage).
* Conduct malware trend analysis (SOC + Threat Intel).
* Collect forensic samples from high-risk cases for deeper review.

### **Quarterly Tasks**

* Endpoint hardening review (CIS benchmarks).
* DLP policy tuning (false positive/negative review).
* Simulated ransomware exercise on endpoints (Red Team).
* Endpoint fleet posture report to leadership (Head of Endpoint Security).

### **Yearly Tasks**

* Refresh endpoint baseline image (OS, configs, tooling).
* Review and update endpoint security standards (Architect).
* Perform enterprise-wide device encryption validation.
* Commission external endpoint security assessment.

---

## 3. Tools Used

### **Top Open Source Tools**

1. **OSQuery** – Endpoint telemetry and compliance queries.
2. **Wazuh** – Endpoint monitoring, malware detection, log analysis.
3. **Velociraptor** – Digital forensics and incident response (DFIR).
4. **GRR Rapid Response** – Remote live forensics.
5. **ClamAV** – Open-source antivirus.
6. **FleetDM** – Endpoint visibility and OSQuery management.
7. **Kolide** – Endpoint compliance enforcement (based on OSQuery).
8. **Autopsy/Sleuth Kit** – Forensic analysis.
9. **Falco** – Runtime security (containers, Linux).
10. **TheHive + Cortex** – Incident investigation/automation for endpoint cases.

### **Top Commercial Tools**

1. **CrowdStrike Falcon** – Market-leading EDR/XDR.
2. **Microsoft Defender for Endpoint (MDE)** – Built-in EDR for Windows + cross-platform.
3. **SentinelOne Singularity** – Autonomous EDR.
4. **Carbon Black (VMware)** – Endpoint security + threat hunting.
5. **Sophos Intercept X** – Next-gen AV + EDR.
6. **McAfee Endpoint Security** – AV + DLP + EDR.
7. **Symantec Endpoint Protection** – Enterprise endpoint suite.
8. **Jamf Pro** – Apple MDM for macOS/iOS.
9. **MobileIron / Ivanti** – Enterprise MDM/EMM.
10. **Zscaler Client Connector** – Endpoint for Zero Trust network access.

---

## 4. Problems Solved & Expected Success Rate

* **Malware/Ransomware Infection:** EDR + patching reduces success by \~90–95%.
* **Unpatched Vulnerabilities:** Automated patch management closes exposure window by \~80–90%.
* **Data Leakage:** DLP and disk encryption mitigate \~85% of insider/lost device risks.
* **Shadow IT Devices:** MDM ensures only compliant devices connect (\~90% coverage if enforced).
* **Incident Response Gaps:** Forensics and EDR telemetry improve investigation success by \~80%.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Endpoint / Terminal Security Pillar:**

* 💻 **Endpoint Coverage %** (EDR/MDM-enrolled vs. total endpoints).
* 🛡 **Malware Incidents Detected & Blocked per Month**.
* ⏱ **Mean Time to Detect (MTTD) & Contain (MTTC) Endpoint Threats**.
* 📊 **Patch Compliance %** (critical/high severity).
* 🔒 **Disk Encryption Coverage %** (BitLocker/FileVault/others).
* 📉 **False Positive Rate for Endpoint Alerts**.
* 🚨 **Number of Ransomware Simulation Failures**.
* 🧾 **Endpoint Compliance Score (CIS/NIST benchmarks)**.
* 🌐 **Shadow IT Device Detections**.
* 👤 **User Awareness Phishing Click Rate (endpoint delivered)**.

---


