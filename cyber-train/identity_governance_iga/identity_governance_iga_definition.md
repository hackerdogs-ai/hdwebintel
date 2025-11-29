# 🆔 Pillar 18: Identity Governance & Administration (IGA)

**Scenarios to Protect:**

* Orphaned accounts after employees leave (joiner/mover/leaver risk).
* Excessive entitlements and privilege creep across business units.
* Regulatory fines for failing to enforce user access reviews (e.g., SOX, HIPAA).
* Lack of visibility into who has access to what across SaaS, cloud, and on-prem.
* Insider threats or compromised accounts with unnecessary access.

**Design Points:**

* Centralized IGA platform for provisioning, de-provisioning, and certification.
* Role-Based Access Control (RBAC) & Attribute-Based Access Control (ABAC).
* Periodic access reviews & recertifications.
* Automated joiner/mover/leaver workflows integrated with HRIS.
* Segregation of Duties (SoD) enforcement (e.g., can’t request and approve payments).
* Integration with IAM (AuthN/AuthZ) and PAM (Privileged Access Mgmt).

---

## 1. Roles & Ownership

### **Strategic Roles (Oversight & Governance)**

* **CISO:** Owns identity governance strategy and reporting.
* **CIO / Head of IT:** Ensures integration with HR and IT systems.
* **Principal Identity Architect:** Designs IGA frameworks (RBAC/ABAC, SoD rules).
* **Head of IGA / Identity Risk Manager:** Oversees certification campaigns, risk management.

### **Execution Roles (Implementation & Operations)**

* **IGA Engineer:** Manages IGA platforms (SailPoint, Saviynt, Keycloak extensions).
* **IAM Engineer:** Implements access control enforcement.
* **HR / People Ops Integration Lead:** Ensures joiner/mover/leaver automation.
* **SOC Analyst:** Monitors identity-related anomalies (e.g., credential abuse).
* **Auditors (Internal/External):** Validate access reviews and certifications.
* **Business Unit Managers:** Certify user access for their teams.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Automate provisioning/de-provisioning for HR-driven changes.
* Monitor orphaned accounts and remediate immediately.
* Detect abnormal access patterns (SOC + IGA Engineer).

### **Weekly Tasks**

* Review access requests awaiting approval.
* Validate SoD enforcement across critical systems.
* Report anomalous entitlements to business owners.

### **Monthly Tasks**

* Conduct targeted mini-certification campaigns (high-risk apps).
* Patch and update connectors for SaaS/cloud integrations.
* Review privileged accounts for compliance.

### **Quarterly Tasks**

* Run enterprise-wide access recertifications by business unit managers.
* Audit SoD conflicts and remediate.
* Report access compliance status to leadership.

### **Yearly Tasks**

* Refresh IGA policies and access baseline roles.
* Commission external IGA compliance audit (SOX, HIPAA, PCI DSS).
* Benchmark IGA maturity against industry frameworks.
* Full joiner/mover/leaver simulation to validate automation.

---

## 3. Tools Used

### **Top Open Source Tools**

1. **Keycloak** – Open-source IAM/IGA extensions.
2. **midPoint (Evolveum)** – Open-source IGA platform.
3. **Apache Syncope** – IGA for provisioning, roles, policies.
4. **PrivacyIDEA** – MFA + identity workflows.
5. **OpenIAM** – Open-source IAM/IGA suite.
6. **Wazuh** – Detect anomalies in identity activity.
7. **Elastic Stack (ELK)** – Audit log monitoring.
8. **Gluu Server** – Identity & access management with governance add-ons.
9. **LDAP / FreeIPA** – Directory-based role enforcement.
10. **SORMAS** – Workflow management for access review processes.

### **Top Commercial Tools**

1. **SailPoint IdentityNow / IdentityIQ** – Market leader in IGA.
2. **Saviynt Enterprise Identity Cloud** – Cloud-first IGA.
3. **Okta Identity Governance** – Lifecycle + policy enforcement.
4. **Ping Identity IGA** – Access governance and SoD management.
5. **IBM Security Verify Governance** – Mature enterprise IGA.
6. **Oracle Identity Governance** – Legacy-heavy IGA platform.
7. **One Identity Manager** – Comprehensive IGA suite.
8. **CyberArk Identity** – IGA integrated with PAM.
9. **Microsoft Entra ID Governance** – Cloud-native identity governance.
10. **RSA SecurID Governance & Lifecycle** – Identity lifecycle management.

---

## 4. Problems Solved & Expected Success Rate

* **Orphaned Accounts:** Automated de-provisioning reduces exposure by \~90–95%.
* **Privilege Creep:** Quarterly certifications & SoD enforcement cut risk by \~80%.
* **Audit Failures (SOX, HIPAA):** Automated reporting ensures \~100% readiness.
* **Insider Threat:** Least-privilege + recertifications reduce insider abuse risk by \~70%.
* **Slow Offboarding:** HR-integrated IGA automation cuts offboarding delay by \~85%.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for IGA Pillar:**

* 🆔 **% Orphaned Accounts Detected vs. Remediated**
* 🔑 **% Users with Excessive Privileges (vs. baseline)**
* 📊 **Certification Completion Rate %** (per campaign)
* ⏱ **Mean Time to De-Provision Accounts**
* 🧾 **Audit Findings Related to Access Reviews**
* 👥 **# of SoD Conflicts Detected vs. Remediated**
* 📉 **Privilege Creep Trend Over Time**
* 🌐 **% of Apps Integrated into IGA Platform**
* 🚨 **Identity-Related Security Incidents (quarterly)**
* 📋 **IGA Maturity Score (vs. industry benchmark)**

---


