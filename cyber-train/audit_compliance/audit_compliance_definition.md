# 📋 5. Audit # 📋 Pillar 6: Audit & Compliance Compliance

**Scenarios to Protect:**

* Regulatory obligations (SOX, PCI DSS, HIPAA, GDPR, ISO 27001, FedRAMP, etc.)
* Internal and external audit readiness
* Ensuring policies and controls are enforced and evidenced

**Design Points:**

* Continuous compliance monitoring (CCM) instead of point-in-time checks
* Log completeness, retention, and immutability
* Policy automation and evidence collection
* Business unit accountability for regulatory compliance

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Oversight, Governance)**

* **CISO:** Owns compliance program strategy, board-level reporting.
* **Chief Risk Officer (CRO) / Compliance Officer:** Ensures adherence to regulatory frameworks, leads audits.
* **Principal Security Architect:** Designs audit logging, evidence pipelines, policy-as-code integration.
* **Head of Governance, Risk & Compliance (GRC):** Leads GRC program, frameworks, control mapping, tooling.

### **Execution Roles (Implementation, Operations, Monitoring)**

* **GRC Analyst:** Collects evidence, maps controls to frameworks, manages audits.
* **Security Engineer (Logging & SIEM):** Ensures log capture, integrity, and immutability.
* **SOC Analyst:** Monitors for compliance violations (e.g., unauthorized access to regulated data).
* **Internal Auditor:** Conducts periodic internal reviews of control effectiveness.
* **External Auditor (3rd-party):** Provides certification (SOC 2, ISO 27001, PCI DSS).
* **DevSecOps Engineer:** Automates compliance controls in CI/CD, enforces policy-as-code.
* **Data Protection Officer (DPO):** Oversees GDPR compliance.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Monitor compliance-related alerts (SOC Analyst).
* Validate logging pipeline integrity (Security Engineer).
* Track non-compliant events in regulated systems (SOC + GRC Analyst).

### **Weekly Tasks**

* Review audit trail completeness for critical systems (Security Engineer).
* Conduct spot checks of log immutability & evidence collection (GRC Analyst).
* Ensure policy enforcement in CI/CD pipelines (DevSecOps).

### **Monthly Tasks**

* Generate compliance status reports for leadership (GRC Analyst).
* Perform gap analysis against frameworks (e.g., PCI DSS Req 10, HIPAA §164.312).
* Review access logs for regulated systems (SOC Analyst).
* Update compliance mappings in GRC tools (GRC Analyst).

### **Quarterly Tasks**

* Conduct internal audits against key frameworks (Internal Auditor + GRC Team).
* Run control testing & remediation reviews (Principal Security Architect).
* Policy reviews with business owners (CISO + CRO).
* Present compliance scorecard to executive team (CISO).

### **Yearly Tasks**

* Prepare for and undergo external audits (SOC 2, ISO, PCI DSS, HIPAA).
* Refresh compliance policies and procedures (GRC + Architect).
* Conduct org-wide compliance training and awareness sessions.
* Vendor/third-party compliance risk assessments.

---

## 3. Tools Used

### **Top Open Source Tools**

1. **Wazuh** – Compliance monitoring (PCI DSS, HIPAA, GDPR).
2. **Elastic Stack (ELK)** – Centralized log collection and compliance dashboards.
3. **Graylog** – Compliance-oriented log management.
4. **Osquery** – Host-level compliance enforcement and audit trails.
5. **Auditd (Linux Audit Framework)** – Low-level audit logging.
6. **Falco** – Runtime security compliance monitoring for containers.
7. **ComplianceAsCode / OpenSCAP** – Automated compliance scanning & baselines.
8. **Eramba** – Open-source GRC platform.
9. **Grafana Loki** – Log aggregation & retention validation.
10. **ModSecurity (WAF)** – Web app compliance & logging enforcement.

### **Top Commercial Tools**

1. **Splunk Enterprise Security (ES)** – Compliance dashboards & log integrity.
2. **ServiceNow GRC** – Governance, risk, and compliance workflow automation.
3. **Archer GRC (RSA)** – Risk and compliance management.
4. **OneTrust** – Privacy and compliance automation (GDPR, CCPA).
5. **MetricStream** – Enterprise GRC management.
6. **Microsoft Purview Compliance** – Data classification & compliance.
7. **Google Chronicle Security Operations** – Log integrity & compliance.
8. **IBM QRadar SIEM** – Compliance dashboards and evidence pipelines.
9. **Sumo Logic Cloud SIEM** – Log retention compliance & audits.
10. **Proofpoint CASB/DLP** – Data compliance for cloud and SaaS.

---

## 4. Problems Solved & Expected Success Rate

* **Regulatory Non-Compliance:** Continuous monitoring + automated evidence collection ensures near-100% audit readiness.
* **Audit Failures:** Policy-as-code and automated evidence reduce manual errors (\~90–95% success).
* **Log Gaps:** Immutable log pipelines guarantee audit trail completeness (\~98% assurance).
* **Manual Compliance Fatigue:** GRC automation reduces effort by \~60–70%.
* **Vendor Risk Blind Spots:** Third-party compliance monitoring prevents \~80% of hidden vendor-related gaps.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Audit & Compliance Pillar:**

* 📋 **% Audit Controls Passing vs. Total Controls**
* 📊 **Compliance Framework Coverage %** (PCI, HIPAA, GDPR, etc.)
* ⏱ **Time to Collect Audit Evidence** (manual vs. automated)
* 📁 **Log Completeness %** (collected vs. required sources)
* 🔒 **Retention SLA Compliance** (90-day/1-year log retention)
* 🚨 **Number of Compliance Violations Detected & Remediated**
* 🧾 **Audit Remediation SLA Compliance %**
* 🌐 **3rd-Party/Vendor Compliance Coverage %**
* 👩‍💻 **Compliance Training Completion Rate**
* 📉 **Audit Findings Over Time (trend)**

---


