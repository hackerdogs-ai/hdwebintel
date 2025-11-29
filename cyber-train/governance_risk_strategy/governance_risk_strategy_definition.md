# 🏛 Pillar 17: Governance, Risk & Strategy

**Scenarios to Protect:**

* Lack of alignment between business goals and security initiatives
* Security seen as a cost center rather than a business enabler
* Inconsistent risk management across business units
* Compliance-only approach without risk-based prioritization
* Poor executive/board visibility into security posture

**Design Points:**

* Governance: Policies, frameworks (NIST CSF, ISO 27001, COBIT)
* Risk Management: Risk register, scoring (CVSS, FAIR, DREAD, custom matrices)
* Strategy: Security roadmap aligned with business objectives
* Oversight: Clear reporting to board, regulators, and customers
* Continuous improvement cycle: Measure → Report → Improve

---

## 1. Roles & Ownership

### **Strategic Roles (Oversight, Policy, Alignment)**

* **Board of Directors / Risk Committee:** Provides top-level oversight, approves risk appetite.
* **CISO:** Owns enterprise risk management (ERM) for security, sets strategy, reports KPIs.
* **Chief Risk Officer (CRO):** Ensures security risk is integrated with enterprise-wide risk management.
* **Principal Security Architect:** Ensures policies translate into technical architecture.
* **Head of GRC (Governance, Risk, Compliance):** Runs frameworks, audits, and control mapping.

### **Execution Roles (Operations, Analysis, Monitoring)**

* **GRC Analysts:** Maintain risk registers, monitor control compliance, track remediation.
* **Policy & Standards Manager:** Creates and updates security policies and baselines.
* **Business Unit Security Champions:** Ensure local adoption of corporate policies.
* **SOC & Security Engineers:** Provide operational metrics to risk/governance teams.
* **Internal Audit Team:** Validates controls and risk mitigation effectiveness.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Monitor KRIs (Key Risk Indicators) dashboards for emerging risks (GRC).
* Track exceptions and policy violations (SOC + GRC Analysts).
* Provide metrics to CISO for situational awareness.

### **Weekly Tasks**

* Conduct risk scoring updates for new vulnerabilities/incidents (GRC Analysts).
* Hold cross-team risk review standups (CISO + CRO).
* Validate policy exceptions and remediation timelines.

### **Monthly Tasks**

* Update the enterprise risk register (CISO + GRC).
* Present risk posture to executive leadership.
* Ensure alignment of controls with frameworks (NIST CSF, ISO 27001, CIS 18).
* Conduct lessons-learned meetings from recent incidents.

### **Quarterly Tasks**

* Report risk posture to the Board of Directors.
* Run tabletop risk scenarios with executives (e.g., ransomware, data breach).
* Audit a subset of policies and controls for effectiveness.
* Update strategy roadmap with new threat landscape adjustments.

### **Yearly Tasks**

* Full enterprise risk assessment (aligned to NIST/ISO/FAIR).
* Refresh security strategy & budget roadmap.
* External audits & certifications (SOC 2, ISO 27001, PCI DSS).
* Benchmark against industry peers (via ISACs, Gartner, etc.).
* Conduct full policy refresh cycle.

---

## 3. Tools Used

### **Top Open Source Tools**

1. **Eramba** – Open-source GRC platform.
2. **OpenFAIR Tools** – Quantitative risk modeling.
3. **GRR Rapid Response** – Evidence for risk reporting.
4. **Osquery** – Policy compliance validation.
5. **ComplianceAsCode (OpenSCAP)** – Automates control enforcement.
6. **Risk Register Templates (OWASP Risk Rating, FAIR Excel models)**.
7. **Auditd** – Control validation for system-level events.
8. **Elastic Stack (ELK)** – Dashboarding risk/security posture.
9. **GRC module in Wazuh** – Compliance + risk management reporting.
10. **Metasploit/Red Team Tools** – Inputs for risk assessments.

### **Top Commercial Tools**

1. **RSA Archer** – Enterprise GRC management.
2. **ServiceNow GRC** – Risk, compliance, and policy workflows.
3. **MetricStream** – Risk and compliance dashboards.
4. **OneTrust GRC** – Vendor risk, privacy, and compliance alignment.
5. **LogicGate Risk Cloud** – Workflow-driven GRC.
6. **RiskRecon (Mastercard)** – Vendor risk scoring.
7. **BitSight** – Cyber risk ratings.
8. **NAVEX GRC Suite** – Policy, risk, compliance.
9. **ZenGRC** – Cloud-first GRC platform.
10. **Board Reporting Platforms (Diligent, BoardEffect)** – Board-level dashboards.

---

## 4. Problems Solved & Expected Success Rate

* **Misaligned Security Priorities:** Governance aligns security with business → \~80–90% reduction in “rogue” initiatives.
* **Inconsistent Risk Management:** Centralized risk register ensures enterprise-wide visibility → \~85% improved accountability.
* **Compliance-Only Security:** Risk-based prioritization ensures resources focus on material risks → \~70% increase in ROI.
* **Board Blind Spots:** Clear reporting improves board confidence and budget approval → \~90–95% success in executive alignment.
* **Reactive Strategy:** Structured governance ensures proactive posture → \~75% fewer surprises in audits and incidents.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Governance, Risk & Strategy Pillar:**

* 🏛 **% of Policies Reviewed & Updated Annually**
* 📊 **# of Risks in Register by Severity (critical/high/medium/low)**
* ⏱ **Mean Time to Remediate Identified Risks**
* 🧾 **Audit Control Pass Rate %** (internal/external)
* 🌐 **Framework Coverage % (NIST, ISO, CIS, PCI, HIPAA, GDPR)**
* 👥 **Business Unit Risk Participation Rate** (champions engaged)
* 🚨 **Policy Exception Rate** (open vs. closed exceptions)
* 📈 **Board Risk Score Trend Over Time**
* 💰 **% of Security Spend Mapped to Top 5 Business Risks**
* 📉 **Residual Risk Trend (after mitigation)**

---


