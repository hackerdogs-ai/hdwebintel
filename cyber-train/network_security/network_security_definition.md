# 🌐 6. Network Security

**Scenarios to Protect:**

* Internal and external network infrastructure
* East–west and north–south traffic visibility
* Preventing unauthorized access, lateral movement, and exfiltration

**Design Points:**

* Defense-in-depth with firewalls, IDS/IPS, segmentation
* Zero Trust Network Access (ZTNA)
* Continuous monitoring with SIEM/NDR
* Secure remote access (VPN/SDP)

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Design, Oversight)**

* **CISO:** Owns enterprise network security strategy, risk posture, reporting to board.
* **Principal Network Security Architect:** Designs segmentation, ZTNA, firewall policies, and monitoring architecture.
* **Head of Network Operations & Security:** Leads firewalls, NDR, VPN/SDP, and traffic visibility programs.

### **Execution Roles (Implementation, Operations, Monitoring)**

* **Network Security Engineer:** Configures and maintains firewalls, VPNs, IDS/IPS.
* **SOC Analyst:** Monitors network traffic alerts (DDoS, intrusion attempts, anomalies).
* **NDR Engineer:** Manages network detection and response platforms.
* **IT/Network Operations Team:** Applies changes, patching, and routing updates.
* **DevSecOps Engineer:** Ensures cloud networking security groups, VPC rules, container networking.
* **Incident Responder:** Responds to network security incidents (DDoS, intrusions).
* **Red Team / Pen Tester:** Simulates lateral movement, exfiltration, and firewall bypasses.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Monitor IDS/IPS/NDR alerts (SOC Analyst).
* Review firewall and VPN logs for anomalies (Network Security Engineer).
* Validate uptime of critical network security controls (Ops Team).

### **Weekly Tasks**

* Apply firewall/IDS signature updates (Network Security Engineer).
* Validate Zero Trust network policies and enforcement.
* Analyze outbound traffic patterns for data exfiltration (SOC + NDR Engineer).
* Perform external perimeter scans (Red Team/SOC).

### **Monthly Tasks**

* Conduct vulnerability scans on network appliances (Vuln Engineer).
* Review VPN/remote access activity for unusual usage.
* Test segmentation policies and microsegmentation boundaries.
* Patch routers, switches, firewalls, and load balancers (Network Ops).

### **Quarterly Tasks**

* Run Red Team exercises (lateral movement, exfiltration).
* Test DDoS response plans with simulations.
* Review firewall rulesets for unused/overly permissive rules.
* Report network security posture to leadership.

### **Yearly Tasks**

* Update network security policy and Zero Trust roadmap (CISO + Architect).
* Perform third-party network security assessments.
* Conduct org-wide tabletop exercise for major network outage/attack.
* Refresh hardware/software lifecycle (firewalls, IDS/IPS, switches).

---

## 3. Tools Used

### **Top Open Source Tools**

1. **Snort** – IDS/IPS for intrusion detection.
2. **Suricata** – High-performance IDS/IPS + NDR.
3. **Zeek (Bro)** – Network traffic analysis.
4. **pfSense** – Open-source firewall/router.
5. **OPNsense** – Advanced open-source firewall platform.
6. **Wireshark** – Deep packet inspection and analysis.
7. **ntopng** – Network traffic flow monitoring.
8. **Elastic Stack (ELK)** – Ingest/analyze network logs.
9. **Security Onion** – Full NSM (Network Security Monitoring) distro.
10. **Nmap** – Network scanning and discovery.

### **Top Commercial Tools**

1. **Palo Alto NGFW** – Next-gen firewall + threat prevention.
2. **Cisco Firepower** – NGFW and IPS.
3. **Fortinet FortiGate** – Enterprise NGFW platform.
4. **Check Point Quantum Security Gateway** – NGFW/IDS/IPS.
5. **Zscaler ZIA/ZPA** – Cloud-based secure access/Zero Trust.
6. **CrowdStrike Falcon NDR** – AI-driven NDR.
7. **Darktrace** – AI-based network anomaly detection.
8. **ExtraHop Reveal(x)** – NDR platform.
9. **Arista Awake Security** – NDR.
10. **Akamai Kona Site Defender** – DDoS and WAF for edge protection.

---

## 4. Problems Solved & Expected Success Rate

* **Unauthorized Access / Intrusion:** Firewalls + IDS/IPS + ZTNA block >90% of direct intrusion attempts.
* **Lateral Movement:** Microsegmentation + anomaly detection reduces risk by \~80%.
* **Data Exfiltration:** Outbound traffic monitoring + DLP reduces successful exfiltration attempts by \~85%.
* **DDoS Attacks:** Mitigation services (Akamai/Cloudflare/Fortinet) provide \~95% effectiveness against volumetric attacks.
* **Shadow IT Networking:** Continuous discovery (Nmap/Zeek) uncovers \~90% of unauthorized network assets.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Network Security Pillar:**

* 🌐 **Network Intrusion Attempts Blocked per Day**
* 🚨 **Number of IDS/IPS Alerts Investigated vs. False Positives**
* 🔒 **% Network Segmentation Coverage (zones, microsegmentation)**
* 📉 **DDoS Attack Incidents & Mitigation Success Rate**
* 🧾 **% Firewall Rules Reviewed and Updated Quarterly**
* 🕵️ **Suspicious Outbound Connections Detected**
* ⏱ **Average Time to Detect & Contain Network Intrusion**
* 🖥 **Coverage of NDR Monitoring Across Subnets/Cloud VPCs**
* 📋 **Audit Findings Related to Network Security**
* 💻 **Encrypted vs. Unencrypted Traffic % (internal & external)**

---


