# 🛠 Pillar 15: Application Security

**Scenarios to Protect:**

* Vulnerabilities in in-house or third-party applications (web, mobile, desktop, SaaS).
* Injection, XSS, CSRF, insecure deserialization, broken access control.
* Flaws introduced in the SDLC due to insecure coding or insufficient testing.
* Open-source supply chain risks (malicious packages, outdated dependencies).

**Design Points:**

* Secure Software Development Lifecycle (SSDLC) integrated into DevOps.
* Automated code scanning (SAST/DAST/IAST/SCA) in CI/CD pipelines.
* Manual and automated penetration testing.
* AppSec champions embedded in dev teams.
* Alignment with OWASP ASVS and OWASP Top 10.

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Design, Oversight)**

* **CISO:** Owns enterprise AppSec strategy and budget, reports risk posture to leadership.
* **Principal Application Security Architect:** Defines SSDLC, secure coding standards, and toolchain integration.
* **Head of Application Security:** Runs AppSec program, manages champions, interfaces with dev leadership.

### **Execution Roles (Implementation, Operations, Monitoring)**

* **AppSec Engineer:** Implements SAST/DAST/SCA/IAST tooling, fixes pipeline integrations.
* **DevSecOps Engineer:** Embeds security in CI/CD, configures policy enforcement gates.
* **Developers:** Write secure code, remediate findings, follow secure coding guidelines.
* **SOC Analyst:** Monitors production applications for anomalous traffic/exploitation.
* **Penetration Tester / Red Team:** Performs targeted application penetration testing.
* **Threat Modeling Specialist:** Facilitates STRIDE, DREAD, or PASTA threat modeling exercises.
* **Compliance Analyst:** Maps application security to PCI DSS, HIPAA, GDPR, etc.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Developers run local SAST/linters pre-commit.
* AppSec Engineers triage automated scan results.
* SOC monitors WAF/production application logs for anomalies.

### **Weekly Tasks**

* Conduct dependency vulnerability scans (SCA) on all builds.
* Review and remediate high-priority security findings with dev teams.
* Run fuzz testing on critical APIs/app endpoints.

### **Monthly Tasks**

* Threat modeling workshops for new projects/features.
* Conduct DAST scans on staging/production apps.
* Provide secure coding training sessions to dev teams.
* Patch vulnerable third-party libraries.

### **Quarterly Tasks**

* Perform penetration tests (internal or external).
* Review SSDLC metrics with leadership (time-to-fix, backlog trends).
* Audit CI/CD security gates for coverage and bypasses.
* Update secure coding guidelines (e.g., OWASP ASVS alignment).

### **Yearly Tasks**

* Commission external application security assessment.
* Refresh AppSec roadmap (tool upgrades, methodology improvements).
* Run enterprise-wide secure development maturity benchmark (e.g., BSIMM, SAMM).
* Validate compliance-driven AppSec requirements (PCI DSS, HIPAA, SOX).

---

## 3. Tools Used

### **Top Open Source Tools**

1. **OWASP ZAP** – DAST scanning.
2. **SonarQube (Community)** – SAST and code quality.
3. **Bandit (Python), Brakeman (Rails), ESLint Security Rules** – Language-specific SAST.
4. **Trivy / Grype** – Dependency and container image scanning.
5. **Dependency-Check (OWASP)** – Software Composition Analysis (SCA).
6. **FindSecBugs** – Static analysis for Java.
7. **Semgrep** – Lightweight static analysis with custom rules.
8. **Fuzzing Tools (AFL, Jazzer)** – Automated input fuzzing.
9. **Gauntlt** – DevSecOps test automation.
10. **Threat Dragon (OWASP)** – Threat modeling diagrams.

### **Top Commercial Tools**

1. **Veracode** – Enterprise SAST/DAST/SCA.
2. **Checkmarx One** – SAST, SCA, IaC scanning.
3. **Synopsys Coverity / Black Duck** – SAST + dependency risk.
4. **Fortify (Micro Focus)** – Mature SAST/DAST suite.
5. **Contrast Security** – IAST and RASP (runtime protection).
6. **AppScan (HCL)** – DAST + compliance testing.
7. **Burp Suite Pro / Enterprise** – Pen testing & automated scanning.
8. **WhiteSource / Mend** – Open-source SCA & license compliance.
9. **Snyk** – Dev-friendly dependency scanning and CI/CD integration.
10. **GitHub Advanced Security** – CodeQL SAST, Dependabot SCA, secret scanning.

---

## 4. Problems Solved & Expected Success Rate

* **Vulnerable Code in Production:** CI/CD security gates reduce exploitable vulns by \~70–85%.
* **Third-Party Dependency Risks:** SCA tools block outdated or malicious libraries (\~80% reduction in exposure).
* **Zero-Day Exploits in Apps:** Threat modeling + secure design mitigates \~60–70% of classes of issues.
* **Missed Bugs Due to Manual Testing Limits:** Automated fuzzing and IAST improve coverage by \~75%.
* **Audit/Compliance Gaps:** SSDLC evidence ensures \~100% readiness for PCI DSS, HIPAA, SOX audits.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Application Security Pillar:**

* 🛠 **% of Builds Passing Security Gates** (SAST, DAST, SCA).
* 📊 **# of Critical/High Findings per 1,000 LOC**.
* ⏱ **Mean Time to Remediate (MTTR) Application Vulns**.
* 🔒 **Dependency Coverage % (apps scanned with SCA)**.
* 🧾 **Threat Models Completed per New Project**.
* 🚨 **# of Production Exploits Detected vs. Blocked**.
* 📉 **Backlog of Unremediated Findings**.
* 👩‍💻 **% of Developers Trained in Secure Coding**.
* 🌐 **% of Applications Behind a WAF or RASP**.
* 📋 **Compliance Audit Pass Rate for AppSec Controls**.

---



