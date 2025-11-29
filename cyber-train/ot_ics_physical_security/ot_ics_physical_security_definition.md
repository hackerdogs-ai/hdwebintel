# 🏭 Pillar 20: OT/ICS & Physical Security

**Scenarios to Protect:**

* Industrial control systems (ICS), SCADA, and IoT devices vulnerable to cyber/physical attacks.
* Nation-state threats targeting critical infrastructure (e.g., power, water, manufacturing).
* Insider or contractor misuse of physical access (tailgating, badge theft).
* Lack of visibility into OT networks due to air-gapped or legacy devices.
* Regulatory obligations (NERC CIP, ISA/IEC 62443, TSA pipeline directives).

**Design Points:**

* Converged IT + OT security strategy with segmentation.
* Zero Trust applied to OT/ICS networks.
* Physical security integrated with logical controls.
* Network monitoring specialized for OT protocols (Modbus, DNP3, OPC-UA).
* Access governance for contractors and vendors.
* Resiliency planning for cyber-physical incidents (fires, floods, ransomware).

---

## 1. Roles & Ownership

### **Strategic Roles (Oversight & Governance)**

* **Chief Security Officer (CSO) / CISO:** Owns integrated cyber-physical strategy.
* **Head of OT Security / Plant CISO:** Focuses on ICS/SCADA/IoT environments.
* **Facilities/Physical Security Director:** Owns building and perimeter security.
* **Principal ICS Architect:** Designs segmentation, monitoring, and secure controls.

### **Execution Roles (Operations & Monitoring)**

* **OT Security Engineer:** Implements firewalls, IDS/IPS, and asset inventory in OT networks.
* **ICS/SCADA Engineer:** Operates and maintains industrial systems securely.
* **SOC Analyst (OT specialization):** Monitors ICS/OT traffic for anomalies.
* **Physical Security Officer / Guard Force:** Monitors physical access points, CCTV, alarms.
* **Facilities Technician:** Maintains badge systems, sensors, and environmental controls.
* **Incident Responder (OT/Physical):** Handles cyber-physical incidents.
* **Vendor/Contractor Manager:** Manages third-party access to OT and facilities.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Monitor OT network traffic for anomalies (SOC).
* Review building access logs for suspicious activity.
* Validate CCTV and physical intrusion detection systems are operational.

### **Weekly Tasks**

* Validate contractor/vendor badge access rights.
* Check OT asset inventory for new/unapproved devices.
* Test environmental and safety controls (fire alarms, sensors).

### **Monthly Tasks**

* Conduct OT vulnerability scans (non-intrusive to avoid downtime).
* Review physical access control lists.
* Patch and update ICS HMIs, PLC firmware (where possible).
* Generate OT/physical incident reports.

### **Quarterly Tasks**

* Run Red Team/Blue Team cyber-physical attack simulations.
* Audit OT network segmentation policies.
* Review badge/access card issuance vs. HR records.
* Conduct tabletop exercises simulating insider physical attacks.

### **Yearly Tasks**

* Full disaster recovery simulation (including physical scenarios like fire/flood).
* External audit of OT/ICS compliance (NERC CIP, IEC 62443).
* Test power, cooling, and redundancy for critical facilities.
* Re-certify vendor/contractor access to OT/physical environments.

---

## 3. Tools Used

### **Top Open Source Tools**

1. **GRASSMARLIN** – OT/ICS network visualization and monitoring.
2. **Wireshark (ICS protocol dissectors)** – OT protocol analysis.
3. **Security Onion (OT integrations)** – Intrusion detection for OT.
4. **Zeek with ICS parsers** – OT traffic anomaly detection.
5. **OpenPLC** – Testbed for ICS security testing.
6. **ELK Stack** – Log analysis for OT and physical security.
7. **ZoneMinder** – Open-source CCTV monitoring system.
8. **OSQuery** – Monitoring access control devices.
9. **ModSecurity** – Gateway security for ICS web interfaces.
10. **OpenVAS** – Vulnerability scanning adapted for OT.

### **Top Commercial Tools**

1. **Dragos Platform** – ICS threat detection and response.
2. **Claroty xDome** – OT visibility, monitoring, and segmentation.
3. **Nozomi Networks Guardian** – ICS anomaly detection.
4. **Armis** – Agentless OT/IoT device security.
5. **Fortinet OT Security Fabric** – Firewalls and monitoring for ICS.
6. **Palo Alto Networks OT Security** – NGFW with OT DPI.
7. **Cisco Cyber Vision** – ICS visibility and monitoring.
8. **Johnson Controls P2000 / Lenel OnGuard** – Physical access control.
9. **Genetec Security Center** – Unified video + access control.
10. **Honeywell OT Security Suite** – ICS security for industrial environments.

---

## 4. Problems Solved & Expected Success Rate

* **Unmonitored OT Assets:** OT inventory tools reduce visibility gaps by \~85–90%.
* **Unauthorized Physical Access:** Badge + CCTV integration cuts tailgating/unauthorized access by \~80%.
* **Nation-State/Advanced ICS Threats:** Dragos/Claroty detection prevents \~70–75% of common TTPs.
* **Legacy ICS Risks:** Segmentation and monitoring reduce risk exposure by \~60–70%.
* **Compliance Gaps (NERC CIP, IEC 62443):** Automated monitoring ensures \~95–100% audit readiness.
* **Insider Threats:** Contractor/vendor access reviews reduce misuse risk by \~75–80%.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for OT/ICS & Physical Security Pillar:**

* 🏭 **% OT Assets Discovered vs. Unknown**
* 🔑 **# of Unauthorized Access Attempts (physical/OT)**
* 📊 **Patch/Update Coverage % for ICS Devices**
* 🚨 **# of OT/Physical Incidents Detected per Quarter**
* 📉 **Mean Time to Detect & Respond (MTTD/MTTR) OT Incidents**
* 🧾 **Compliance Audit Pass Rate (NERC CIP, IEC 62443)**
* 🌐 **Network Segmentation Coverage % (IT vs. OT)**
* 👥 **Contractor/Vendor Access Compliance %**
* 📷 **CCTV Coverage Uptime %**
* 📋 **Residual OT/Physical Risk Trend Over Time**

---


