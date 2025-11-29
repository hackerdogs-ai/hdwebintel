# ☁️ Pillar X: Cloud Security (Including CNAPP)

**Scenarios to Protect:**

* Misconfigured cloud services (S3 buckets, IAM roles, Kubernetes clusters).
* Over-privileged cloud accounts leading to lateral movement.
* Cloud-native workload risks: containers, serverless, microservices.
* Compliance and data residency issues in multi-cloud environments.
* Lack of visibility into ephemeral assets (functions, containers, short-lived workloads).

**Design Points:**

* Cloud Security Posture Management (CSPM) for configuration governance.
* Cloud Infrastructure Entitlement Management (CIEM) for least privilege.
* CNAPP (CSPM + CWPP + CIEM + Kubernetes security + IaC scanning) integration.
* Workload Protection (CWPP) for containers, VMs, and serverless.
* IaC scanning and policy-as-code to shift security left.
* Multi-cloud strategy with consistent controls (AWS, Azure, GCP).

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Oversight, Architecture)**

* **CISO:** Owns cloud security strategy, reports posture to the board.
* **Principal Cloud Security Architect:** Designs multi-cloud security architecture, defines baseline guardrails, CNAPP adoption.
* **Head of Cloud Security / Cloud Risk Officer:** Ensures operational execution, compliance across all clouds.

### **Execution Roles (Operations, Monitoring, Engineering)**

* **Cloud Security Engineer:** Implements CSPM, CWPP, CNAPP controls.
* **DevSecOps Engineer:** Integrates IaC scanning and security gates in pipelines.
* **SOC Analyst (Cloud Focus):** Monitors cloud logs, detects misconfigurations and attacks.
* **IAM Engineer (Cloud):** Manages cloud entitlements and privileged roles.
* **Platform Engineer / SRE:** Ensures Kubernetes, serverless, and workloads adhere to security baselines.
* **Compliance Analyst:** Aligns cloud posture with regulatory frameworks (HIPAA, PCI, GDPR, FedRAMP).
* **Red Team / Cloud Pen Tester:** Tests cloud misconfigurations, privilege escalation, and lateral movement.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Monitor CNAPP dashboards for misconfigurations, vulnerabilities, drift.
* SOC triage cloud security alerts (API abuse, abnormal IAM activity).
* Enforce IaC scanning in CI/CD builds.

### **Weekly Tasks**

* Review identity/entitlement changes in cloud accounts (IAM team).
* Validate logging coverage (CloudTrail, GuardDuty, Security Command Center).
* Patch cloud-native workloads (containers, serverless).

### **Monthly Tasks**

* Cloud compliance scans (CIS benchmarks, NIST mappings).
* Run incident response tabletop exercises for cloud breaches.
* Validate encryption & key management compliance in cloud services.
* Analyze cloud usage reports for shadow IT accounts.

### **Quarterly Tasks**

* Conduct Red Team cloud attack simulation (IAM privilege escalation, misconfig abuse).
* Audit third-party SaaS integrations into the cloud environment.
* Validate DR strategy with cloud-native backups and cross-region replication.
* Update IaC templates with latest security baselines.

### **Yearly Tasks**

* Refresh multi-cloud security strategy (CISO + Architect).
* External audit of cloud compliance (SOC 2, PCI DSS, ISO 27001).
* Vendor review of CNAPP/CSPM/CWPP tools.
* Enterprise-wide cloud incident simulation (supply chain / cloud outage).

---

## 3. Tools Used

### **Top Open Source Tools**

1. **Cloud Custodian** – Policy-as-code for cloud governance.
2. **Terrascan** – IaC security scanning.
3. **Checkov (Bridgecrew)** – IaC vulnerability scanning.
4. **Kube-bench** – Kubernetes CIS benchmark testing.
5. **Falco** – Runtime security for containers and Kubernetes.
6. **Prowler** – AWS/Azure/GCP security scanning.
7. **ScoutSuite** – Multi-cloud auditing tool.
8. **CloudMapper** – AWS environment visualization & misconfig detection.
9. **Trivy** – Container and IaC vulnerability scanning.
10. **Kubescape** – Kubernetes and cloud-native compliance scanning.

### **Top Commercial Tools (CNAPP Leaders)**

1. **Prisma Cloud (Palo Alto)** – CNAPP: CSPM, CWPP, CIEM, IaC.
2. **Wiz Security** – Agentless CNAPP with strong visibility.
3. **Orca Security** – Agentless CNAPP for multi-cloud.
4. **Lacework** – CNAPP with anomaly detection.
5. **Microsoft Defender for Cloud** – CSPM + CWPP for Azure, AWS, GCP.
6. **Check Point CloudGuard** – Multi-cloud CSPM/CWPP.
7. **Trend Micro Cloud One** – Cloud security platform (workloads, containers, IaC).
8. **Aqua Security** – Kubernetes and container-focused CNAPP.
9. **Sysdig Secure** – Runtime security and compliance for containers/K8s.
10. **Tenable.cs / Qualys Cloud Security** – Cloud posture and workload protection.

---

## 4. Problems Solved & Expected Success Rate

* **Cloud Misconfigurations (open buckets, weak IAM):** CSPM reduces risk by \~80–90%.
* **Excessive Privileges in Cloud IAM:** CIEM reduces identity-related risks by \~85%.
* **Workload Exploits (containers, serverless):** CWPP runtime defense mitigates \~75–85% of threats.
* **IaC Misconfigurations:** Policy-as-code scanning blocks \~70–80% before deployment.
* **Compliance Gaps:** Automated compliance scans ensure \~95–100% readiness.
* **Shadow IT Cloud Services:** CNAPP discovery reduces unknown risks by \~60–70%.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Cloud Security & CNAPP Pillar:**

* ☁️ **% Cloud Resources Compliant with Baselines (CIS, NIST)**
* 🔑 **% Identities with Least Privilege Access (CIEM metric)**
* 🚨 **# of Misconfigurations Detected & Remediated**
* 📦 **% Containers/Serverless Functions Covered by CWPP**
* ⏱ **Mean Time to Detect & Remediate Misconfigurations**
* 🌐 **Cloud Account Coverage % (CSPM deployment across AWS/Azure/GCP)**
* 🧾 **Compliance Audit Pass Rate (PCI, HIPAA, FedRAMP)**
* 📉 **% High-Risk IaC Misconfigs Blocked Pre-Deployment**
* 🕵️ **Red Team Findings vs. Mitigated Gaps (quarterly)**
* 🔒 **% Encryption Coverage (storage, DBs, snapshots, backups)**

---


