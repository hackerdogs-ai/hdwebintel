# Application Security (AppSec) Engineer Standard Operating Procedure

**Role:** Principal Application Security Engineer  
**Mission:** Embed security throughout the SSDLC/DevSecOps pipeline, prevent exploitable flaws before release, and maintain runtime security posture.  
**Scope:** All applications, services, APIs, mobile apps, infrastructure-as-code, and CI/CD pipelines (first-party and third-party).

---

## 1. Role Charter & Authority

### Principal AppSec Engineer (PAE) Responsibilities

* **End-to-End Ownership:** Design → Build → Test → Release → Operate security controls
* **Security Automation:** Design, build, and maintain security gates, scanning tools, and monitoring systems
* **Threat Analysis:** Perform threat modeling, penetration testing, security reviews, and incident response
* **Deliverable Production:** Create all security documentation, dashboards, exception records, and sign-offs
* **Security DRI:** Act as security decision-maker for critical vulnerabilities and release gates

### Authority & Guardrails

* **Release Authority:** Can block releases on security grounds (documented process)
* **Pipeline Control:** Can introduce/modify CI/CD security gates and rules
* **Incident Escalation:** Can page incident command and security leadership
* **Policy Enforcement:** Can mandate security training and compliance requirements

---

## 2. RACI Matrix

| Activity | **PAE** | Development Teams | Product/Engineering | SOC/Operations |
|----------|---------|------------------|-------------------|----------------|
| Security intake & risk tiering | **R/A** | C | I | I |
| Security requirements & user stories | **R/A** | C | I | I |
| Threat modeling & design review | **R/A** | C | I | I |
| Pipeline security gates (SAST/SCA/Secrets/IaC) | **R/A** | C | I | I |
| SBOM generation & supply-chain policy | **R/A** | C | I | I |
| DAST/IAST/mobile/k8s posture scans | **R/A** | C | I | I |
| Targeted pen testing (scoping, execution, retest) | **R/A** | C | I | I |
| Vulnerability triage, SLAs, verification | **R/A** | C | I | I |
| Security release Go/No-Go | **R/A** | I | I | I |
| Runtime detections (WAF/RASP/SIEM rules) | **R/A** | C | I | C |
| CSPM/drift audits | **R/A** | C | I | C |
| Exceptions & risk acceptance records | **R/A** | I | I | I |
| Incident escalation & security actions | **R/A** | C | I | C |
| Program metrics/KPIs & quarterly planning | **R/A** | I | I | I |

**Legend:** R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## 3. End-to-End Security Process

### Phase 1: Plan & Design (Shift Left & Requirements)

| Step | Goal | Input to Step | Output Deliverable | Essential Content |
|------|------|----------------|-------------------|------------------|
| **1. Security Intake & Risk Tiering** | Classify security risk and data sensitivity | Epic/PRD, architecture sketch, data types | **Security Intake Record** | Risk tier, data classes, owners, target dates, compliance requirements |
| **2. Security Requirements & User Stories** | Translate risk into mandatory development standards | Intake record, compliance requirements | **Security Requirements Spec** | User stories, acceptance criteria, OWASP mapping, verification hooks |
| **3. Threat Modeling** | Prevent architectural flaws and identify threats | HLD/DFDs, trust boundaries, asset inventory | **Threat Model Report** | Attack trees, threat scenarios, mitigations, risk ratings, test cases |
| **4. Security Design Review** | Validate authentication, authorization, crypto, tenancy | Design documents, architecture diagrams | **Design Review Notes** | Mitigation tasks, Jira IDs, standards references |
| **5. Component/Vendor Approval** | Evaluate OSS licenses and CVEs | Dependency list, third-party components | **Approved Components List** | Name/version/license, rationale, pinned versions |

### Phase 2: Code & Pre-Commit (Immediate Developer Feedback)

| Step | Tool/Procedure | CI/CD Integration Point | Input to Step | Output Deliverable | Essential Content |
|------|----------------|------------------------|----------------|-------------------|------------------|
| **1. Static Code Analysis (SAST)** | Scan source code for security flaws | IDE/commit hooks, PR annotations | New source code, SAST ruleset | **SAST Gate Status** | File:line of flaw, vulnerability type, secure fix code snippet |
| **2. Dependency & Artifact Inventory (SBOM)** | Create complete component list | Build pipeline, artifact registry | Source code, dependency files | **SBOM (SPDX/CycloneDX)** | Component name, version, hash, license information |
| **3. Secrets Scanning** | Scan for exposed credentials | Git hooks, PR validation | Git commits, secrets rules | **Secrets Incident Ticket** | Commit hash, file path, revocation/rotation evidence |
| **4. Infrastructure-as-Code (IaC) Scan** | Check cloud/k8s configuration | CI/CD pipeline, deployment gates | Terraform/K8s manifests | **IaC Violations Report** | Resource name, policy violated, corrected code snippet |

### Phase 3: Build & Integrate (CI/CD Pipeline)

| Step | Tool/Procedure | CI/CD Integration Point | Input to Step | Output Deliverable | Essential Content |
|------|----------------|------------------------|----------------|-------------------|------------------|
| **1. Comprehensive SAST Scan** | Deep codebase analysis | Build pipeline, quality gates | Full repository code | **SAST Gate Status** | Pass/fail status, High/Critical count, OWASP Top 10 compliance |
| **2. Container & Artifact Scanning (SCA)** | Check images for vulnerabilities | Image registry, deployment pipeline | Container images, SBOM | **SCA Vulnerability Report** | Exploitable CVEs, affected components, fix versions, gate decision |
| **3. Supply Chain Security** | Verify artifact integrity and provenance | Build pipeline, artifact signing | Build artifacts, signing keys | **Supply Chain Attestation** | Provenance evidence, signature verification, tamper detection |

### Phase 4: Test & Verify (Runtime Vulnerability Assessment)

| Step | Tool/Procedure | Testing Environment | Input to Step | Output Deliverable | Essential Content |
|------|----------------|-------------------|----------------|-------------------|------------------|
| **1. Dynamic Application Testing (DAST)** | Scan running application | Staging/QA environment | Deployed app URL, credentials | **DAST Findings Report** | Affected route/parameter, PoC steps, request/response artifacts |
| **2. Interactive Application Testing (IAST)** | Correlate runtime to code paths | Application with agent | IAST agent, application | **IAST Correlation Report** | Sink/source mapping, file:line, exploitability assessment |
| **3. Mobile Application Testing** | Analyze mobile binary | Mobile testing environment | APK/IPA files | **Mobile Security Report** | Insecure API use, data protection status, store go/no-go |
| **4. Kubernetes & Cluster Security** | Scan live cluster configuration | Kubernetes cluster | Cluster credentials, benchmarks | **Cluster Compliance Report** | Failed controls, remediation commands, compliance score |
| **5. Penetration Testing** | Manual adversarial testing | Staging environment | All prior reports, test scope | **Penetration Test Report** | Executive summary, CVSS scores, step-by-step PoCs, fix recommendations |

### Phase 5: Release & Operate (Protection and Monitoring)

| Step | Tool/Procedure | Runtime Environment | Input to Step | Output Deliverable | Essential Content |
|------|----------------|-------------------|----------------|-------------------|------------------|
| **1. Security Go/No-Go Decision** | Approve release based on security posture | Release pipeline | All security reports, gate statuses | **Security Go/No-Go Memo** | Zero Critical/High vulnerabilities, approved exceptions, signatures |
| **2. Runtime Security Monitoring** | Detect and alert on security events | Production environment | Application logs, security thresholds | **Security Alert Catalog** | Rule IDs, thresholds, runbook links, suppression policies |
| **3. Cloud Security Posture Management (CSPM)** | Audit cloud configuration | Cloud environment | Cloud APIs, compliance policies | **CSPM Weekly Report** | New violations, trend analysis, remediation status |
| **4. Vulnerability Management** | Track and verify remediation | Vulnerability management platform | Security reports, fix evidence | **Vulnerability Register** | Owner, SLA due date, status, verification evidence |

---

## 4. Daily Operations Cadence

### Daily Tasks
- **Triage Security Queue:** Review SAST/SCA/DAST/secrets findings → **Daily Triage Log**
- **CI Gate Health Check:** Monitor pipeline security gates → **Gate Health Snapshot**
- **Runtime Alerts Review:** Analyze security events and incidents → **Alert Summary**
- **Hot CVE Advisory Scan:** Check for new critical vulnerabilities → **Advisory Ticket**

### Weekly Tasks
- **Vulnerability Status Review:** Meet with owning teams → **Weekly Vulnerability Deck**
- **CSPM Drift Analysis:** Review cloud configuration changes → **Weekly CSPM Report**
- **Training Progress Check:** Monitor security training completion → **Training Roster Update**

### Monthly Tasks
- **Base Image & Dependency Patching:** Update security patches → **Monthly Patch Bulletin**
- **Threat Model Updates:** Review changed systems → **Threat Model Delta Report**
- **KPI Dashboard Publication:** Publish security metrics → **AppSec KPI Pack**

### Quarterly Tasks
- **Penetration Testing:** Execute on high-risk applications → **Quarterly Pen Test Report**
- **Incident Response Tabletop:** Conduct security exercises → **Exercise Report**
- **Policy & Gate Review:** Update security standards → **Standards Update PRs**

### Annual Tasks
- **SSDLC Audit:** Comprehensive security program review → **Annual Audit Report**
- **Program Roadmap:** Plan security initiatives → **AppSec Roadmap**
- **Training Refresh:** Update security training curriculum → **Annual Training Plan**

---

## 5. Success Metrics & KPIs

### Shift-Left & Build Metrics
- **≥ 90%** repositories with SAST/SCA/Secrets/IaC gates enabled
- **≥ 85%** of PRs with zero new High/Critical SAST issues
- **≤ 5%** false-positive rate (sampled monthly)

### Vulnerability Management
- **MTTR Critical ≤ 7 days, High ≤ 14 days**
- **≤ 5%** past-due Critical/High vulnerabilities
- **CVE Exposure Window** trending downward quarter-over-quarter

### Supply Chain Security
- **100%** releases have SBOM attached
- **0** secrets incidents reaching production
- **< 2 hours** secret revocation MTTR

### Design Coverage
- **100%** Threat Models for High-risk applications
- **≥ 70%** Threat Models for Medium-risk applications

### Runtime & Cloud Security
- **≥ 90%** internet-exposed applications behind WAF/RASP
- **≤ 5 days** CSPM High drift MTTR

### Program Effectiveness
- **≥ 95%** training completion by due dates
- **≥ 1:1** bug bounty valid:invalid ratio

---

## 6. Exception Management & Escalation

### Security Exceptions
- **Criteria:** Only for business-critical releases with compensating controls
- **Documentation:** Exception Record (risk/CWE/OWASP, compensating control, expiry ≤90 days)
- **Approval:** Security leadership approval required
- **Renewal:** Barred without retest and re-approval

### Escalation Triggers (Immediate Response Required)
- Authentication/authorization bypass vulnerabilities
- Remote code execution (RCE) vulnerabilities
- PII/PHI exfiltration indicators
- Leaked secrets in active use
- Cloud-wide public data exposure
- Actively exploited zero-day in core components

### Escalation Chain
**PAE → Security IC/CISO → Legal/Executive Leadership**

**Deliverable:** Incident Timeline Document (who/what/when, containment, eradication, lessons learned) within 5 business days

---

## 7. OWASP Top 10 & CWE Mapping

Every security finding must map to:
- **OWASP Top 10** category
- **CWE (Common Weakness Enumeration)** identifier
- **CVSS (Common Vulnerability Scoring System)** score

**Deliverable:** OWASP/CWE Mapping Table maintained in repository wiki with:
- Category → controls/tests/tools mapping
- Exemplar fixes and remediation guidance
- Scanner configuration references

---

## 8. Tool Stack & Runbooks

### Security Testing Tools
- **SAST:** Semgrep, SonarQube
- **SCA/SBOM:** Trivy, Grype, Syft
- **Secrets:** TruffleHog, GitGuardian
- **IaC/K8s:** Terrascan, Checkov, Kubescape
- **DAST:** OWASP ZAP, Burp Suite
- **IAST/RASP:** Contrast Security
- **Mobile:** MobSF
- **CSPM:** Scout Suite, AWS Security Hub

### Monitoring & Response Tools
- **SIEM:** Elastic Security, Splunk
- **WAF:** CloudFlare, AWS WAF
- **RASP:** Contrast Protect, Imperva
- **Vulnerability Management:** Jira, ServiceNow

### Documentation Requirements
Each tool requires:
- **Owner:** PAE responsible
- **Policy Baseline:** Security standards
- **Gate Thresholds:** Pass/fail criteria
- **Dashboard URL:** Monitoring interface
- **Runbook:** Operational procedures

---

## 9. Release Security Gates

### Mandatory Security Checks
**Block release unless ALL of the following pass:**

1. **SAST/SCA/Secrets/IaC gates pass** with zero Critical/High findings
2. **SBOM present** and attached to release
3. **No open Critical/High** from DAST/IAST/penetration testing
4. **Security Go/No-Go** signed by PAE
5. **WAF/SIEM rules** active for production
6. **Exception records** approved (if applicable)

### Security Sign-off Process
1. **Automated Gates:** CI/CD pipeline validates all security checks
2. **Manual Review:** PAE reviews exception requests and compensating controls
3. **Final Approval:** Security Go/No-Go memo with signatures
4. **Release Authorization:** Only after all gates pass and approvals obtained

---

## 10. Incident Response Integration

### Security Incident Types
- **Critical:** Authentication bypass, RCE, data exfiltration
- **High:** Privilege escalation, sensitive data exposure
- **Medium:** Information disclosure, denial of service
- **Low:** Information leakage, minor configuration issues

### Response Procedures
1. **Detection:** Automated alerts, manual discovery, external reports
2. **Triage:** PAE assesses severity and impact
3. **Containment:** Immediate actions to prevent further damage
4. **Investigation:** Root cause analysis and scope determination
5. **Eradication:** Remove threat and vulnerabilities
6. **Recovery:** Restore normal operations with monitoring
7. **Lessons Learned:** Post-incident review and process improvement

---

## 11. Training & Awareness

### Security Training Requirements
- **New Hire:** Mandatory security awareness training
- **Role-Specific:** Developer, DevOps, and management training
- **Annual Refresh:** Updated training on new threats and controls
- **Incident-Based:** Targeted training after security incidents

### Training Topics
- Secure coding practices
- OWASP Top 10 vulnerabilities
- Threat modeling techniques
- Security testing methodologies
- Incident response procedures
- Compliance requirements

---

## 12. Compliance & Audit

### Regulatory Requirements
- **GDPR:** Data protection and privacy controls
- **HIPAA:** Healthcare data security
- **SOX:** Financial data integrity
- **PCI DSS:** Payment card data security
- **SOC 2:** Service organization controls

### Audit Preparation
- **Documentation:** Maintain security policies and procedures
- **Evidence:** Collect security testing results and remediation proof
- **Gap Analysis:** Identify compliance gaps and remediation plans
- **Continuous Monitoring:** Ongoing compliance validation

---

## 13. Continuous Improvement

### Metrics Review
- **Monthly:** Security metrics dashboard review
- **Quarterly:** KPI analysis and trend identification
- **Annually:** Program effectiveness assessment

### Process Optimization
- **Tool Evaluation:** Regular assessment of security tools
- **Automation Enhancement:** Increase security automation coverage
- **Training Updates:** Refresh training content based on new threats
- **Policy Updates:** Revise security policies based on lessons learned

---

## 14. Emergency Procedures

### Critical Security Incident Response
1. **Immediate Containment:** Isolate affected systems
2. **Notification:** Alert security leadership and stakeholders
3. **Investigation:** Determine scope and impact
4. **Communication:** Provide regular updates to leadership
5. **Recovery:** Restore services with enhanced monitoring
6. **Post-Incident:** Conduct thorough review and implement improvements

### Contact Information
- **Security Hotline:** [Emergency contact number]
- **Escalation Path:** PAE → CISO → Executive Leadership
- **External Resources:** Law enforcement, legal counsel, PR team

---

## 15. Appendices

### A. Security Checklist Templates
- **Pre-Release Security Checklist**
- **Threat Model Review Checklist**
- **Penetration Test Scope Template**
- **Vulnerability Assessment Template**

### B. Tool Configuration Guides
- **SAST Rule Configuration**
- **SCA Policy Setup**
- **Secrets Detection Rules**
- **IaC Security Baselines**

### C. Incident Response Playbooks
- **Data Breach Response**
- **Malware Incident Response**
- **Insider Threat Response**
- **Third-Party Security Incident**

### D. Compliance Mapping
- **OWASP Top 10 to Controls**
- **CWE to Remediation**
- **Regulatory Requirements Matrix**
- **Security Framework Mapping**

---

**Document Version:** 1.0  
**Last Updated:** [Current Date]  
**Next Review:** [Date + 1 Year]  
**Approved By:** [Security Leadership]  
**Distribution:** Security Team, Engineering Leadership, Compliance Team
