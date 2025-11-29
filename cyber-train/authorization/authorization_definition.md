# 🛡 2. Authorization

**Scenarios to Protect:**

* Data access
* User roles

**Design Points:**

* Regular review
* Principle of least privilege
* Role-based access control (RBAC)

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Architecture, Oversight)**

* **CISO (Chief Information Security Officer):** Owns access governance strategy and risk posture.
* **Principal Security Architect:** Defines enterprise-wide RBAC/ABAC (Attribute-Based Access Control) models, Zero Trust access, SoD (Segregation of Duties).
* **Head of Identity & Access Management (IAM):** Oversees authorization policies, tool integration, entitlement lifecycle, roadmap.

### **Execution Roles (Implementation, Monitoring, Operations)**

* **IAM Engineer:** Configures RBAC/ABAC in IAM platforms (Okta, Keycloak, Azure AD, etc.), integrates new apps, enforces least privilege.
* **SOC Analyst:** Monitors for privilege escalations, abnormal access patterns, insider threats.
* **AppSec Engineer:** Ensures apps integrate correctly with enterprise IAM for fine-grained authorization.
* **Helpdesk / Access Admin:** Handles provisioning/deprovisioning, role assignment.
* **Data Steward / Business Role Owner:** Approves/reviews access requests for data/app ownership.
* **Red Team / Pen Tester:** Tests bypasses, privilege escalation, misconfigurations.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* SOC Analysts monitor for privilege escalation attempts or abnormal access logs.
* IAM Engineers handle emergency access revocations and privilege corrections.
* Helpdesk/Admins process new user onboarding and role assignment.
* AppSec validates that new apps enforce RBAC via IAM.

### **Weekly Tasks**

* Review high-privilege account usage (SOC + IAM).
* Detect and remediate SoD violations.
* Run anomaly detection on access logs (geo/time/device).
* AppSec confirms that code deployments enforce least privilege.

### **Monthly Tasks**

* Perform role and entitlement hygiene checks (orphaned accounts, excessive entitlements).
* Conduct targeted reviews of access to sensitive data sets (HR, finance, IP).
* Validate compliance with RBAC/ABAC models in SaaS applications.
* IAM team patches IAM/authorization systems.

### **Quarterly Tasks**

* Enterprise-wide access recertification campaigns (with business role owners).
* Privilege creep review and entitlement clean-up.
* SoD policy enforcement testing across financial & regulated apps.
* Red Team targeted privilege escalation campaigns.

### **Yearly Tasks**

* Update RBAC/ABAC models to align with org changes.
* Refresh authorization policies based on regulatory updates (SOX, HIPAA, GDPR).
* Perform 3rd-party access entitlement reviews.
* Conduct external audit of IAM/authorization practices.

---

## 3. Tools Used

### **Top Open Source Tools**

1. **Keycloak** – IAM + SSO with RBAC/ABAC support.
2. **Open Policy Agent (OPA)** – Fine-grained policy enforcement.
3. **FreeIPA** – Role/permission management for Linux domains.
4. **Wazuh** – Privileged access log monitoring.
5. **Authelia** – Authentication + authorization reverse proxy.
6. **PrivacyIDEA** – Policy-based MFA/authorization extension.
7. **Elastic Stack (ELK)** – Access log ingestion and anomaly detection.
8. **CrowdSec** – Collaborative detection of abnormal access.
9. **Osquery** – Endpoint query for privilege checks.
10. **OpenIAM** – Open-source identity governance & access certification.

### **Top Commercial Tools**

1. **Okta** – SSO, RBAC/ABAC, provisioning.
2. **Microsoft Entra ID (Azure AD)** – Conditional access, RBAC, Just-in-Time access.
3. **Ping Identity** – Federation + fine-grained access.
4. **SailPoint IdentityNow** – Governance, recertification campaigns.
5. **CyberArk** – Privileged access management.
6. **BeyondTrust** – Privilege elevation & delegation management.
7. **ForgeRock AM** – Policy-based authorization at scale.
8. **IBM Security Verify** – Access control and risk-based authorization.
9. **Oracle Identity Cloud Service (IDCS)** – Enterprise RBAC and access certification.
10. **RSA SecurID Governance & Lifecycle** – Entitlement lifecycle and compliance.

---

## 4. Problems Solved & Expected Success Rate

* **Excessive Privilege Risk:** RBAC/ABAC reduces insider threat exposure by >80%.
* **SoD Violations:** Automated detection and review prevent compliance breaches (\~90% success).
* **Shadow IT Access:** Centralized IAM + app integration captures 85–95% of SaaS access points.
* **Privilege Escalation:** Continuous monitoring + Red Team testing catch >70% attempts before abuse.
* **Audit Readiness:** Identity governance tools (SailPoint, OpenIAM) ensure >95% compliance with external audit controls.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Authorization Pillar:**

* 🔑 **% of Privileged Accounts Reviewed per Quarter**
* 📊 **Entitlement Count per User** (creep detection)
* 🚨 **SoD Violations Detected & Resolved**
* 🕵️ **Privilege Escalation Attempts Blocked**
* 📉 **% of Orphaned Accounts Remediated**
* 🔒 **% of Apps Integrated with Central IAM**
* ⏱ **Average Access Request Approval Time**
* 👤 **% of Workforce in Least Privilege Roles**
* 📋 **Compliance Campaign Completion Rate**
* 🧾 **Audit Findings Related to Access Controls**

---

