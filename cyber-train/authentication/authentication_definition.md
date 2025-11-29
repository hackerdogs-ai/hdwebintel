# 🔐 1. Authentication

**Scenarios to Protect:**

* User logins
* Employee access to internal systems

**Design Points:**

* Strong password policy
* Multi-factor authentication (MFA)

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Design, Architecture):**

* **CISO (Chief Information Security Officer):** Sets overall authentication and access control policies.
* **Principal Security Architect:** Defines MFA/SSO standards, federation models (SAML/OAuth2), and IAM architecture.
* **Head of Identity & Access Management (IAM):** Owns enterprise identity strategy, vendor/tool selection, roadmap.

### **Execution Roles (Operations, Monitoring, Implementation):**

* **IAM Engineer / Security Engineer:** Implements and maintains identity systems (Okta, Azure AD, Keycloak, etc.).
* **SOC Analyst:** Monitors authentication logs, detects anomalies (failed logins, brute force).
* **IT Helpdesk / Access Admin:** Handles account provisioning, MFA resets, access revocations.
* **Red Team / Pen Tester:** Tests for weak authentication and bypasses.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Monitor login anomalies (SOC Analyst)
* Handle MFA/SSO login issues (IT Helpdesk)
* Apply emergency access revocations (IAM Engineer)
* Track brute-force attempts and phishing MFA bypass attempts (SOC Analyst)

### **Weekly Tasks**

* Review privileged access activity (IAM Engineer, SOC)
* Validate authentication system health (IAM Engineer)
* Run detection rules on impossible travel / geo-location anomalies (SOC Analyst)
* Red Team short tests on phishing-resistant MFA flows (Red Team)

### **Monthly Tasks**

* Test password policy compliance (IAM Engineer)
* Patch and update IAM systems (IAM Engineer)
* Review helpdesk authentication-related tickets for patterns (IT Helpdesk Lead)
* Audit stale accounts and orphaned identities (IAM Engineer)

### **Quarterly Tasks**

* Run enterprise-wide access review (IAM + Business Unit Owners)
* Perform SSO/Federation tests for SaaS integrations (IAM Engineer)
* Red Team authentication bypass assessments (Red Team)
* Report metrics to Security Leadership Team (CISO/Principal Architect)

### **Yearly Tasks**

* Update authentication policies and standards (Principal Security Architect, CISO)
* Enterprise-wide MFA resiliency tests (SOC + Red Team)
* Vendor evaluation / RFP for IAM solutions (Head of IAM)
* Compliance-driven audits (GDPR, SOX, HIPAA)

---

## 3. Tools Used

### **Top Open Source Tools**

1. **Keycloak** – Open source IAM & SSO
2. **Authelia** – Authentication & authorization server
3. **FreeIPA** – Linux-based identity and authentication
4. **Wazuh** – Authentication log monitoring and alerts
5. **OpenIAM** – Identity governance & administration
6. **PrivacyIDEA** – Open source MFA solution
7. **Elastalert / ELK Stack** – Log correlation for login attempts
8. **OSSEC** – Log-based intrusion detection for authentication logs
9. **CrowdSec** – Collaborative brute force detection
10. **Fail2Ban** – Protects from brute force attacks

### **Top Commercial Tools**

1. **Okta Workforce Identity** – Enterprise SSO, MFA
2. **Microsoft Entra ID (Azure AD)** – Cloud identity & federation
3. **Ping Identity** – Federation, SSO, MFA
4. **Duo Security (Cisco)** – MFA & device trust
5. **CyberArk Idaptive** – Identity & privilege management
6. **ForgeRock Identity Platform** – IAM suite
7. **IBM Security Verify** – Enterprise IAM
8. **SailPoint IdentityNow** – Identity governance
9. **RSA SecurID** – MFA
10. **Google Cloud Identity** – IAM for GCP/enterprise

---

## 4. Problems Solved & Expected Success Rate

* **Account Takeover (ATO) Prevention:** MFA + anomaly detection stops >95% of brute force/phishing attempts.
* **Privilege Abuse:** Regular reviews + least-privilege policies reduce unauthorized access risk by \~80%.
* **Credential Stuffing Attacks:** Rate-limiting & behavioral detection lowers success rates to <5%.
* **Compliance Gaps:** Governance + audit trails ensure near 100% audit readiness.
* **SaaS Sprawl Authentication:** Federation (Okta/Azure AD/Keycloak) centralizes access to hundreds of SaaS apps with >90% adoption rates.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Authentication Pillar:**

* 🔑 **Login Success/Failure Rates** (daily, per app)
* 🚨 **Failed Login Anomalies** (geo, device, velocity)
* 🛡 **MFA Coverage %** (users enrolled vs. required)
* 📊 **Privileged Account Login Activity** (per quarter)
* 🕵️ **Account Lockouts & Resets** (helpdesk tickets trend)
* 🧾 **Audit Results** (policy compliance, stale accounts count)
* 📉 **Credential Stuffing Attempts Blocked**
* ⏱ **Authentication Latency** (SSO login response time SLA)
* 👤 **Inactive Accounts Detected & Removed**
* 🔒 **% of SaaS Apps Federated via SSO**

---


