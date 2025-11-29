# 🔌 10. API Security

**Scenarios to Protect:**

* Public APIs exposed to the internet (customer-facing, partner integrations)
* Internal APIs between microservices (east–west traffic)
* Unauthorized API access or privilege escalation
* Data exfiltration via poorly secured endpoints
* Abuse of APIs via brute force, credential stuffing, or DDoS

**Design Points:**

* Strong authentication/authorization for APIs (OAuth2, OIDC, JWT)
* Rate limiting & throttling to prevent abuse
* Input validation and schema enforcement (prevent injection attacks)
* API discovery and inventory management (no shadow APIs)
* Centralized API gateways with monitoring and logging

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Design, Oversight)**

* **CISO:** Owns API security strategy, ensures it aligns with overall application security program.
* **Principal Security Architect:** Designs API security framework (gateway strategy, zero-trust APIs, schema validation).
* **Head of Application Security (AppSec):** Defines API testing, secure development lifecycle (SDLC) integration.

### **Execution Roles (Implementation, Operations, Monitoring)**

* **API Security Engineer:** Configures API gateways, enforces authentication, and implements rate limiting.
* **DevSecOps Engineer:** Integrates API security scanning into CI/CD pipelines.
* **SOC Analyst:** Monitors API logs for anomalies and abuse attempts.
* **AppSec Engineer / Pen Tester:** Conducts API penetration testing (OWASP API Top 10).
* **Developers:** Implement secure coding practices for API endpoints.
* **Incident Responder:** Investigates API abuse or breach attempts.
* **Compliance Analyst:** Ensures APIs handling regulated data (HIPAA, PCI DSS) meet requirements.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Monitor API logs for anomalies (SOC Analyst).
* Detect brute force, injection attempts, and credential stuffing (SOC Analyst).
* Validate CI/CD scans for new APIs (DevSecOps).

### **Weekly Tasks**

* Run automated API vulnerability scans (AppSec Engineer).
* Review API key/token usage for abnormal patterns (SOC + API Security Engineer).
* Validate API schema enforcement and input validation (DevSecOps).

### **Monthly Tasks**

* Conduct full inventory validation of APIs (API Security Engineer).
* Patch API frameworks (e.g., Express, Spring, Django) for CVEs (Developers).
* Generate API security reports for leadership (Head of AppSec).

### **Quarterly Tasks**

* Perform penetration testing focused on OWASP API Top 10 (AppSec Engineer, Red Team).
* Review API gateway configuration and rate-limiting thresholds.
* Validate SaaS/vendor API integrations for secure authentication.

### **Yearly Tasks**

* Update API security policies and standards (CISO + Architect).
* Conduct external API security assessments (3rd-party auditors).
* Refresh developer training on API-specific security threats.
* Run breach simulation involving API abuse/exfiltration (Red Team).

---

## 3. Tools Used

### **Top Open Source Tools**

1. **OWASP ZAP** – API penetration testing.
2. **Postman + Security Plugins** – API testing & fuzzing.
3. **Burp Suite Community (or Pro)** – API security testing.
4. **APIClarity** – API visibility & runtime analysis.
5. **42Crunch (Community)** – OpenAPI/Swagger security linting.
6. **Tyk** – Open-source API gateway.
7. **Kong Gateway (OSS)** – API management with security plugins.
8. **JWT.io** – Token debugging and validation.
9. **Nmap + NSE Scripts** – API endpoint discovery.
10. **Mitmproxy** – API traffic interception and inspection.

### **Top Commercial Tools**

1. **Apigee (Google Cloud)** – API gateway with security controls.
2. **AWS API Gateway + WAF** – Managed API exposure control.
3. **Azure API Management** – Microsoft’s secure API gateway.
4. **Kong Enterprise** – Enterprise API security & gateway.
5. **NGINX Plus** – API gateway with advanced rate limiting.
6. **42Crunch Enterprise** – API security platform.
7. **Salt Security** – API threat detection & protection.
8. **Noname Security** – API discovery & runtime protection.
9. **Imperva API Security** – API protection integrated with WAF.
10. **Akana API Management** – Governance and security for APIs.

---

## 4. Problems Solved & Expected Success Rate

* **Shadow APIs (untracked endpoints):** API discovery reduces hidden exposure by \~80–90%.
* **Credential Stuffing & Abuse:** Rate limiting + MFA/API tokens reduce success by \~85–95%.
* **Injection Attacks (SQLi, XXE, command):** Schema enforcement + validation blocks \~70–80% of attempts.
* **Excessive Data Exposure:** Secure schema design + least-privilege reduces data leakage by \~85%.
* **Compliance Failures:** Tokenized access + logging ensures \~100% audit readiness (PCI DSS, HIPAA).

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for API Security Pillar:**

* 🔌 **# of APIs Discovered vs. # Documented** (shadow API gap).
* 🔑 **% APIs Using Strong Authentication (OAuth2/JWT/MFA)**.
* 🚨 **API Abuse Attempts Detected per Day** (brute force, injections).
* ⏱ **Mean Time to Detect (MTTD) API Abuse**.
* 📊 **% APIs Passing Automated Security Scans**.
* 🧾 **OWASP API Top 10 Findings per Quarter**.
* 📉 **False Positive Rate in API Alerts**.
* 🌐 **% of APIs Behind a Gateway** (vs. direct exposure).
* 🔒 **Rate Limiting Effectiveness (% blocked attacks)**.
* 🧪 **API Security Test Coverage % (manual + automated)**.

---


