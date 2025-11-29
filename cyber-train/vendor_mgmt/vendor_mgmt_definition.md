# 🤝 Pillar 12: 3rd-Party / Vendor Management

**Scenarios to Protect:**

* Risks introduced via third-party SaaS, cloud, and service providers
* Supply chain attacks (e.g., SolarWinds, Kaseya)
* Insider or external vendor misuse of access rights
* Non-compliance with regulations due to vendor gaps

**Design Points:**

* Vendor risk assessment & due diligence before onboarding
* Continuous monitoring of 3rd-party integrations and access
* Contractual SLAs for security & compliance (SOC2, ISO, GDPR, HIPAA, etc.)
* Access review for vendors (least privilege, just-in-time)
* Secure data sharing & 3rd-party incident notification requirements

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Design, Oversight)**

* **CISO:** Owns third-party risk management strategy, ensures it aligns with enterprise security posture.
* **Chief Procurement Officer (CPO) / Vendor Risk Officer:** Oversees vendor onboarding/offboarding and contractual security clauses.
* **Principal Security Architect:** Designs secure integration standards (e.g., API/SSO requirements, encryption for data exchanges).
* **Head of Governance, Risk & Compliance (GRC):** Defines vendor risk assessment process and compliance mappings.

### **Execution Roles (Implementation, Operations, Monitoring)**

* **Vendor Risk Analyst:** Conducts due diligence, reviews SOC2/ISO 27001 reports, manages risk questionnaires.
* **IAM Engineer:** Enforces vendor access controls (SSO, MFA, least privilege).
* **SOC Analyst:** Monitors vendor accounts/integrations for anomalies.
* **IT Procurement Team:** Coordinates vendor contracts and renewals.
* **Business Unit Owner (Data Steward):** Approves vendor use and validates business justification.
* **Incident Responder:** Coordinates with vendors during security incidents.
* **Legal & Compliance Officer:** Ensures vendor agreements cover breach notification, data protection clauses.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Monitor 3rd-party access activity (SOC).
* Enforce vendor logins via SSO + MFA (IAM).
* Detect unusual data transfers involving vendor accounts (SOC).

### **Weekly Tasks**

* Review vendor tickets, incidents, or access requests.
* Track SLA compliance for vendor security commitments.
* Validate integrity of vendor integrations in production environments.

### **Monthly Tasks**

* Conduct risk scoring updates for key vendors (Vendor Risk Analyst).
* Review access entitlements for active vendors (IAM + Business Owner).
* Audit vendor logs for anomalies.
* Report vendor risk posture to GRC leadership.

### **Quarterly Tasks**

* Run vendor security review meetings with critical partners.
* Validate SOC2/ISO27001 certifications or equivalent assurance.
* Conduct tabletop exercises simulating vendor breach scenarios.
* Update vendor tiering classifications (critical/high/medium/low).

### **Yearly Tasks**

* Perform enterprise-wide vendor risk assessment (all active vendors).
* Refresh vendor risk management policies & playbooks.
* Commission external audits for strategic/critical vendors.
* Review vendor termination/offboarding procedures for completeness.

---

## 3. Tools Used

### **Top Open Source Tools**

1. **osquery** – Monitor vendor endpoint activity.
2. **Wazuh** – Detect anomalous vendor activity.
3. **GRR Rapid Response** – Vendor endpoint forensics.
4. **Metasploit / Nmap** – Vendor integration penetration testing.
5. **GRC Toolkits (Eramba OSS)** – Vendor compliance tracking.
6. **OpenVAS / Greenbone** – Vulnerability scans of vendor connections.
7. **Elastic Stack (ELK)** – Vendor log ingestion and monitoring.
8. **MISP** – Threat intel sharing with vendors.
9. **OpenSCAP** – Vendor compliance baseline scanning.
10. **PrivacyIDEA** – MFA enforcement for vendor logins.

### **Top Commercial Tools**

1. **BitSight** – Continuous vendor cyber risk ratings.
2. **SecurityScorecard** – External vendor risk monitoring.
3. **Archer GRC** – Vendor risk workflows.
4. **OneTrust Vendor Risk Management** – Compliance & data privacy focus.
5. **ServiceNow VRM** – Vendor risk workflow automation.
6. **Prevalent VRM** – Third-party risk assessments & monitoring.
7. **UpGuard Vendor Risk** – Automated vendor assessments.
8. **Panorays** – Vendor cyber risk platform.
9. **RiskRecon (Mastercard)** – Continuous vendor cyber risk scanning.
10. **CyberGRX** – Shared vendor risk exchange platform.

---

## 4. Problems Solved & Expected Success Rate

* **Supply Chain Attacks:** Continuous monitoring + vendor tiering detects \~70–80% of risks before impact.
* **Excessive Vendor Access:** IAM enforcement (least privilege, MFA, JIT) reduces insider/vendor abuse risk by \~85–90%.
* **Compliance Failures:** Contractual clauses + certifications ensure \~95–100% regulatory readiness.
* **Shadow Vendors (unauthorized SaaS):** Discovery + review reduces unmanaged vendors by \~70–80%.
* **Incident Response Gaps:** Vendor coordination playbooks cut IR delays by \~50%.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for 3rd-Party / Vendor Management Pillar:**

* 🤝 **# of Active Vendors by Risk Tier (critical/high/medium/low)**
* 🔑 **% Vendor Accounts with SSO + MFA Enabled**
* 🚨 **Vendor-Related Incidents Detected per Quarter**
* 📊 **% Vendors with Up-to-Date Security Certifications (SOC2, ISO, PCI, HIPAA)**
* 📉 **Average Time to Complete Vendor Risk Assessment**
* 🕵️ **Unmanaged/Shadow Vendors Discovered**
* ⏱ **Mean Time to Respond to Vendor-Linked Incidents**
* 🧾 **Compliance Audit Pass Rate for Vendor Controls**
* 📋 **% Vendors with Signed Security SLAs**
* 🌐 **Third-Party Data Sharing Events (monitored vs. unmonitored)**

---




1. **Consolidate all pillars (2–12) into a master leadership/board matrix** (roles, tasks, tools, metrics side-by-side), or
2. **Continue extending into the extra Hackerdogs pillars (AppSec, Threat Intel, Governance, Awareness, Data Protection)** in the same deep-dive format?
