# 📦 Pillar 10: Container Security

**Scenarios to Protect:**

* Containerized workloads (Kubernetes, Docker, OpenShift, ECS, AKS, GKE, etc.)
* Risks from vulnerable container images, misconfigurations, runtime exploits
* Preventing supply chain attacks via malicious images or registries

**Design Points:**

* Secure base images & signed images (SBOM validation)
* Vulnerability scanning for images, IaC, and dependencies
* Runtime protection (container escape, privilege escalation, abnormal behavior)
* Kubernetes security: RBAC, admission controllers, pod security standards
* Shift-left security integrated into CI/CD pipelines

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Design, Oversight)**

* **CISO:** Owns container and cloud-native security strategy.
* **Principal Cloud/Container Security Architect:** Designs Kubernetes/OCI security architecture, image signing, runtime controls.
* **Head of Cloud Security:** Leads adoption of container security standards (CIS benchmarks, NIST 800-190).

### **Execution Roles (Implementation, Operations, Monitoring)**

* **DevSecOps Engineer:** Integrates scanning into CI/CD, enforces admission policies.
* **Container Security Engineer:** Manages runtime protection, admission controllers, K8s RBAC.
* **SOC Analyst / NDR Analyst:** Monitors runtime alerts and container anomaly detection.
* **Platform Engineer / SRE:** Operates Kubernetes/Docker clusters with secure configs.
* **Vulnerability Engineer:** Manages container image scanning.
* **Incident Responder:** Handles container breakouts or exploited workloads.
* **Red Team / Pen Tester:** Tests container escape, misconfigured registries, K8s API bypasses.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Scan new container images pushed to registry (Vuln Engineer).
* Monitor runtime alerts for suspicious behavior (SOC + Container Security Engineer).
* Block non-compliant image deployments via admission controller (DevSecOps).

### **Weekly Tasks**

* Review container image vulnerabilities (CVEs, dependencies).
* Validate Kubernetes RBAC changes and privileges.
* Analyze runtime anomalies (unexpected network, file access).
* Test CI/CD pipeline enforcement of container policies.

### **Monthly Tasks**

* Audit container registries for outdated or unmaintained images.
* Review Pod Security Admission/OPA Gatekeeper policies.
* Patch Kubernetes control plane and worker nodes.
* Generate vulnerability and compliance reports for leadership.

### **Quarterly Tasks**

* Run Red Team exercises (container escape, API server privilege escalation).
* Perform full cluster penetration test.
* Review and clean up unused images in registries.
* Update CIS Kubernetes/OCI benchmark compliance.

### **Yearly Tasks**

* Refresh container/Kubernetes security policy.
* Vendor evaluation for container security platforms.
* Conduct full disaster recovery simulation (cluster compromise).
* External audit for compliance (e.g., PCI DSS in Kubernetes).

---

## 3. Tools Used

### **Top Open Source Tools**

1. **Trivy** – Vulnerability scanner for containers, IaC, dependencies.
2. **Clair** – Container image vulnerability scanning.
3. **Anchore Engine** – Image scanning and policy enforcement.
4. **Kube-bench** – Kubernetes CIS benchmark testing.
5. **Kube-hunter** – Kubernetes penetration testing.
6. **OPA Gatekeeper** – Policy-as-code for Kubernetes.
7. **Falco** – Runtime security monitoring for containers.
8. **Sysdig OSS** – Runtime monitoring and forensics.
9. **Grafeas** – Metadata and artifact security (supply chain).
10. **Harbor** – Secure container registry with vulnerability scanning & signing.

### **Top Commercial Tools**

1. **Aqua Security** – Full lifecycle container and K8s security.
2. **Prisma Cloud (Palo Alto)** – Container, serverless, cloud-native security.
3. **Sysdig Secure** – Runtime and compliance monitoring.
4. **StackRox / Red Hat Advanced Cluster Security (ACS)** – K8s-native container security.
5. **Snyk Container** – Image scanning integrated into CI/CD.
6. **JFrog Xray** – Container dependency & artifact scanning.
7. **Qualys Container Security** – Vulnerability detection & runtime defense.
8. **Tenable.io Container Security** – Vulnerability scanning for registries.
9. **Docker Security Scanning (Docker Hub/EE)** – Built-in scanning.
10. **Trend Micro Cloud One – Container Security** – Runtime + vulnerability defense.

---

## 4. Problems Solved & Expected Success Rate

* **Vulnerable Images:** Image scanning + CI/CD enforcement prevents \~85–90% of known exploitable images from being deployed.
* **Misconfigurations in Kubernetes:** Benchmark checks + policy enforcement reduce insecure configs by \~80%.
* **Runtime Exploits (escape, privilege escalation):** Falco/Sysdig runtime detection detects abnormal behavior with \~75–85% success rate.
* **Supply Chain Attacks:** Signed images, SBOM validation, and trusted registries reduce malicious package introduction by \~70–80%.
* **Compliance Failures:** Automated CIS/NIST compliance ensures \~95–100% readiness for containerized workloads.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Container Security Pillar:**

* 📦 **% of Images Scanned Before Deployment**
* 🛡 **% of Images Passing Vulnerability Policy** (CVSS threshold compliance)
* 🚨 **Number of Blocked Deployments (non-compliant images)**
* 📊 **Runtime Alerts Investigated (Falco/Sysdig)**
* 🔒 **Kubernetes RBAC Violations Detected**
* 🧾 **Cluster Compliance Score (CIS/NIST benchmarks)**
* 🌐 **# of Registries with Signed Images Only**
* ⏱ **Mean Time to Patch Vulnerable Images**
* 📉 **Unused Images/Artifacts Cleaned Up per Quarter**
* 🕵️ **Red Team Findings (container escape / privilege escalation success rate)**

---


