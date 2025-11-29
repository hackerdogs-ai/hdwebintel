# Detection Engineer Standard Operating Procedure

**Role:** Principal Detection Engineer  
**Mission:** Develop, implement, and maintain threat detection capabilities, security monitoring systems, and incident response procedures to protect organizational assets.  
**Scope:** Enterprise-wide threat detection, security monitoring, incident response, forensic analysis, and security operations.

---

## 1. Role Charter & Authority

### Principal Detection Engineer (PDE) Responsibilities

* **End-to-End Detection:** Design → Build → Test → Deploy → Monitor threat detection capabilities
* **Security Monitoring:** Design, build, and maintain security monitoring and alerting systems
* **Incident Response:** Perform threat analysis, incident investigation, and forensic analysis
* **Deliverable Production:** Create all detection documentation, runbooks, and incident reports
* **Security DRI:** Act as security decision-maker for threat detection and incident response

### Authority & Guardrails

* **Detection Authority:** Can implement/modify threat detection rules and signatures
* **Incident Authority:** Can activate incident response and coordinate response activities
* **Monitoring Control:** Can configure security monitoring and alerting systems
* **Escalation Authority:** Can escalate security incidents to incident command and leadership

---

## 2. RACI Matrix

| Activity | **PDE** | Security Teams | SOC/Operations | Management |
|----------|---------|----------------|----------------|------------|
| Threat detection rule development | **R/A** | C | I | I |
| Security monitoring implementation | **R/A** | C | I | I |
| Incident response procedures | **R/A** | C | I | I |
| Forensic analysis and investigation | **R/A** | C | I | I |
| Threat hunting activities | **R/A** | C | I | I |
| Security tool management | **R/A** | C | I | I |
| Detection rule tuning and optimization | **R/A** | C | I | I |
| Security alert analysis | **R/A** | C | I | I |
| Threat intelligence integration | **R/A** | C | I | I |
| Security incident documentation | **R/A** | C | I | I |
| Detection capability assessment | **R/A** | C | I | I |
| Security training and awareness | **R/A** | C | I | I |

**Legend:** R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## 3. End-to-End Security Process

### Phase 1: Detection Design & Planning (Threat Detection Strategy)

| Step | Goal | Input to Step | Output Deliverable | Essential Content |
|------|------|----------------|-------------------|------------------|
| **1. Threat Detection Strategy** | Define comprehensive threat detection strategy | Threat landscape, business requirements, security objectives | **Threat Detection Strategy** | Detection goals, coverage, methodology, success metrics |
| **2. Detection Rule Development** | Develop threat detection rules and signatures | Threat intelligence, attack patterns, security requirements | **Detection Rule Library** | Rule definitions, logic, testing, validation |
| **3. Security Monitoring Design** | Design security monitoring and alerting systems | Security requirements, threat landscape, monitoring needs | **Security Monitoring Framework** | Monitoring strategy, tools, processes, alerting |
| **4. Incident Response Planning** | Develop incident response procedures | Threat landscape, business requirements, response needs | **Incident Response Procedures** | Response procedures, roles, communication, recovery |
| **5. Forensic Analysis Capabilities** | Establish forensic analysis capabilities | Security requirements, legal requirements, investigation needs | **Forensic Analysis Framework** | Analysis procedures, tools, documentation, reporting |

### Phase 2: Detection Implementation & Testing (Detection Development)

| Step | Tool/Procedure | Detection Integration | Input to Step | Output Deliverable | Essential Content |
|------|----------------|---------------------|----------------|-------------------|------------------|
| **1. Detection Rule Implementation** | Implement threat detection rules | SIEM platform, detection tools, rule engine | Detection rules, testing data, validation criteria | **Detection Rule Status** | Rule implementation, testing results, validation status |
| **2. Security Monitoring Setup** | Configure security monitoring systems | SIEM, monitoring tools, alerting systems | Monitoring requirements, alerting thresholds, notification rules | **Security Monitoring Status** | Monitoring configuration, alerting setup, notification testing |
| **3. Threat Hunting Implementation** | Implement threat hunting capabilities | Threat hunting tools, intelligence feeds, hunting procedures | Threat intelligence, hunting procedures, analysis tools | **Threat Hunting Program** | Hunting procedures, tools, intelligence, analysis |
| **4. Forensic Analysis Setup** | Establish forensic analysis capabilities | Forensic tools, analysis procedures, documentation systems | Forensic requirements, legal requirements, analysis procedures | **Forensic Analysis Capabilities** | Analysis tools, procedures, documentation, reporting |

### Phase 3: Detection Operations & Monitoring (Operational Detection)

| Step | Tool/Procedure | Operations Integration | Input to Step | Output Deliverable | Essential Content |
|------|----------------|---------------------|----------------|-------------------|------------------|
| **1. Threat Detection Operations** | Operate threat detection capabilities | SIEM, detection tools, monitoring systems | Detection rules, monitoring data, alerting systems | **Threat Detection Status** | Detection performance, alerting status, rule effectiveness |
| **2. Security Incident Response** | Respond to security incidents | Incident response tools, communication systems, response procedures | Security incidents, response procedures, communication plans | **Incident Response Status** | Response activities, containment actions, recovery status |
| **3. Forensic Analysis Operations** | Conduct forensic analysis | Forensic tools, analysis procedures, documentation systems | Security incidents, forensic requirements, analysis procedures | **Forensic Analysis Report** | Analysis findings, evidence collection, documentation |
| **4. Threat Hunting Operations** | Conduct threat hunting activities | Threat hunting tools, intelligence feeds, hunting procedures | Threat intelligence, hunting procedures, analysis tools | **Threat Hunting Report** | Hunting activities, findings, intelligence, analysis |

### Phase 4: Detection Analysis & Investigation (Security Analysis)

| Step | Tool/Procedure | Analysis Integration | Input to Step | Output Deliverable | Essential Content |
|------|----------------|-------------------|----------------|-------------------|------------------|
| **1. Security Alert Analysis** | Analyze security alerts and incidents | SIEM, analysis tools, investigation procedures | Security alerts, incident data, analysis procedures | **Security Alert Analysis** | Alert analysis, incident assessment, response recommendations |
| **2. Threat Intelligence Analysis** | Analyze threat intelligence and indicators | Intelligence platforms, analysis tools, intelligence procedures | Threat intelligence, indicators, analysis procedures | **Threat Intelligence Analysis** | Intelligence analysis, indicator assessment, threat assessment |
| **3. Incident Investigation** | Investigate security incidents | Investigation tools, forensic procedures, documentation systems | Security incidents, investigation procedures, forensic requirements | **Incident Investigation Report** | Investigation findings, evidence analysis, root cause analysis |
| **4. Detection Capability Assessment** | Assess detection capabilities | Assessment tools, evaluation procedures, metrics systems | Detection capabilities, assessment criteria, evaluation procedures | **Detection Capability Assessment** | Capability assessment, performance evaluation, improvement recommendations |

### Phase 5: Detection Optimization & Improvement (Continuous Improvement)

| Step | Tool/Procedure | Improvement Integration | Input to Step | Output Deliverable | Essential Content |
|------|----------------|----------------------|----------------|-------------------|------------------|
| **1. Detection Rule Optimization** | Optimize detection rules and signatures | Rule optimization tools, testing procedures, performance metrics | Detection rules, performance data, optimization criteria | **Detection Rule Optimization** | Rule optimization, performance improvement, tuning recommendations |
| **2. Security Monitoring Enhancement** | Enhance security monitoring capabilities | Monitoring tools, enhancement procedures, performance metrics | Monitoring requirements, performance data, enhancement criteria | **Security Monitoring Enhancement** | Monitoring improvement, capability enhancement, performance optimization |
| **3. Threat Hunting Enhancement** | Enhance threat hunting capabilities | Hunting tools, enhancement procedures, intelligence feeds | Threat hunting requirements, intelligence data, enhancement criteria | **Threat Hunting Enhancement** | Hunting improvement, capability enhancement, intelligence optimization |
| **4. Detection Program Assessment** | Assess detection program effectiveness | Assessment tools, evaluation procedures, metrics systems | Detection program, assessment criteria, evaluation procedures | **Detection Program Assessment** | Program assessment, effectiveness evaluation, improvement recommendations |

---

## 4. Daily Operations Cadence

### Daily Tasks
- **Security Alert Review:** Review security alerts and incidents → **Daily Alert Summary**
- **Threat Detection Monitoring:** Monitor threat detection capabilities → **Daily Detection Status**
- **Incident Response Activities:** Respond to security incidents → **Daily Incident Summary**
- **Forensic Analysis Activities:** Conduct forensic analysis → **Daily Forensic Summary**

### Weekly Tasks
- **Detection Rule Review:** Review and optimize detection rules → **Weekly Detection Rule Report**
- **Threat Hunting Activities:** Conduct threat hunting activities → **Weekly Threat Hunting Report**
- **Security Analysis Review:** Review security analysis findings → **Weekly Security Analysis Report**
- **Tool and Platform Management:** Manage security tools and platforms → **Weekly Tool Management Report**

### Monthly Tasks
- **Detection Capability Assessment:** Assess detection capabilities → **Monthly Detection Assessment**
- **Security Operations Review:** Review security operations effectiveness → **Monthly Security Operations Report**
- **Threat Intelligence Review:** Review threat intelligence and indicators → **Monthly Threat Intelligence Report**
- **Detection Program Planning:** Plan detection program improvements → **Monthly Detection Program Plan**

### Quarterly Tasks
- **Detection Program Assessment:** Assess detection program effectiveness → **Quarterly Detection Program Assessment**
- **Threat Detection Strategy Review:** Review threat detection strategy → **Quarterly Detection Strategy Review**
- **Security Tool Evaluation:** Evaluate security tools and platforms → **Quarterly Security Tool Evaluation**
- **Detection Training Program:** Conduct detection training and awareness → **Quarterly Detection Training Report**

### Annual Tasks
- **Detection Program Audit:** Comprehensive detection program review → **Annual Detection Program Audit**
- **Detection Strategy Planning:** Plan detection strategy and roadmap → **Annual Detection Strategy Plan**
- **Security Tool Roadmap:** Plan security tool roadmap and initiatives → **Annual Security Tool Roadmap**
- **Detection Training Curriculum:** Update detection training curriculum → **Annual Detection Training Plan**

---

## 5. Success Metrics & KPIs

### Detection & Monitoring Metrics
- **≥ 95%** detection rule accuracy and effectiveness
- **≤ 5%** false positive rate for detection rules
- **≥ 90%** security monitoring coverage of critical systems
- **≤ 4 hours** mean time to detect security incidents

### Incident Response Metrics
- **≤ 1 hour** mean time to respond to security incidents
- **≤ 24 hours** mean time to resolve security incidents
- **≥ 95%** incident response procedure compliance
- **≤ 5%** incident escalation rate

### Forensic Analysis Metrics
- **≤ 48 hours** mean time to complete forensic analysis
- **≥ 95%** forensic analysis accuracy and completeness
- **≤ 2 hours** mean time to collect forensic evidence
- **≥ 90%** forensic analysis documentation completeness

### Threat Hunting Metrics
- **≥ 80%** threat hunting coverage of critical systems
- **≤ 24 hours** mean time to complete threat hunting activities
- **≥ 90%** threat hunting procedure compliance
- **≤ 10%** threat hunting false positive rate

### Program Effectiveness Metrics
- **≥ 95%** detection training completion rate
- **≥ 90%** security tool utilization and effectiveness
- **≤ 5%** detection program budget variance
- **≥ 85%** stakeholder satisfaction with detection services

---

## 6. Exception Management & Escalation

### Security Exceptions
- **Criteria:** Only for business-critical operations with compensating controls
- **Documentation:** Exception Record (risk assessment, compensating controls, approval, expiry ≤90 days)
- **Approval:** Security leadership approval required
- **Renewal:** Barred without reassessment and re-approval

### Escalation Triggers (Immediate Response Required)
- Critical security incidents requiring immediate response
- Advanced persistent threat (APT) detection or indicators
- Data breach or data exfiltration indicators
- Critical system compromise or unauthorized access
- Regulatory compliance violations or audit failures
- Executive or management security concerns

### Escalation Chain
**PDE → Security IC/CISO → Executive Leadership**

**Deliverable:** Incident Response Report (incident summary, response actions, containment, lessons learned) within 24 hours

---

## 7. Threat Detection & Response Framework Mapping

Every detection capability must map to:
- **Threat Categories** (Malware, APT, Insider Threats, etc.)
- **Attack Techniques** (MITRE ATT&CK, OWASP, etc.)
- **Security Controls** (NIST, ISO 27001, CIS Controls)

**Deliverable:** Detection Mapping Matrix maintained in detection documentation with:
- Threat category → detection rules mapping
- Attack technique → detection signatures mapping
- Security control → monitoring and alerting mapping

---

## 8. Tool Stack & Runbooks

### Detection & Monitoring Tools
- **SIEM:** Splunk, Elastic Security, QRadar, Sentinel
- **Detection:** YARA, Sigma, Suricata, Snort
- **Forensics:** Volatility, Autopsy, Wireshark, FTK
- **Threat Hunting:** MISP, ThreatConnect, OpenCTI

### Analysis & Investigation Tools
- **Log Analysis:** ELK Stack, Splunk, Graylog
- **Network Analysis:** Wireshark, tcpdump, NetFlow
- **Malware Analysis:** Cuckoo, YARA, VirusTotal
- **Incident Response:** TheHive, MISP, Phantom

### Documentation Requirements
Each tool requires:
- **Owner:** PDE responsible
- **Policy Baseline:** Security standards and requirements
- **Detection Thresholds:** Alerting and response criteria
- **Dashboard URL:** Monitoring and analysis interface
- **Runbook:** Operational procedures and escalation

---

## 9. Detection Security Gates

### Mandatory Detection Checks
**Block operations unless ALL of the following pass:**

1. **Detection Rules** implemented and tested with zero critical gaps
2. **Security Monitoring** active with comprehensive coverage
3. **Incident Response** procedures tested and validated
4. **Forensic Analysis** capabilities established and ready
5. **Threat Hunting** procedures implemented and active
6. **Detection Documentation** complete and up-to-date

### Detection Security Process
1. **Detection Design:** Comprehensive detection strategy and rule development
2. **Implementation:** Detection rule implementation and testing
3. **Monitoring:** Security monitoring and alerting setup
4. **Response:** Incident response procedures and capabilities
5. **Analysis:** Forensic analysis and investigation capabilities
6. **Optimization:** Detection optimization and continuous improvement

---

## 10. Incident Response Integration

### Security Incident Types
- **Critical:** Advanced persistent threats, data breaches, system compromise
- **High:** Malware infections, unauthorized access, privilege escalation
- **Medium:** Security policy violations, suspicious activities
- **Low:** Minor security incidents, false positives

### Response Procedures
1. **Detection:** Security monitoring, threat detection, incident reporting
2. **Assessment:** PDE assesses incident severity and impact
3. **Activation:** Activate incident response team and procedures
4. **Investigation:** Conduct forensic analysis and root cause analysis
5. **Containment:** Implement containment and remediation measures
6. **Recovery:** Restore operations with enhanced monitoring
7. **Lessons Learned:** Post-incident review and process improvement

---

## 11. Training & Awareness

### Detection Training Requirements
- **Threat Detection:** Advanced threat detection training and certification
- **Incident Response:** Incident response and crisis management training
- **Forensic Analysis:** Digital forensics and evidence collection training
- **Threat Hunting:** Threat hunting and intelligence analysis training
- **Security Tools:** Security tool training and certification

### Training Topics
- Threat detection methodologies
- Incident response procedures
- Forensic analysis techniques
- Threat hunting and intelligence
- Security tool operation
- Detection optimization and tuning

---

## 12. Compliance & Audit

### Regulatory Requirements
- **GDPR:** Data protection and privacy incident response
- **HIPAA:** Healthcare data security and breach notification
- **SOX:** Financial data integrity and incident reporting
- **PCI DSS:** Payment card data security and incident response
- **SOC 2:** Service organization controls and incident management

### Audit Preparation
- **Documentation:** Maintain detection procedures and incident reports
- **Evidence:** Collect detection evidence and incident response proof
- **Gap Analysis:** Identify detection gaps and remediation plans
- **Continuous Monitoring:** Ongoing detection validation and reporting

---

## 13. Continuous Improvement

### Metrics Review
- **Daily:** Detection metrics dashboard review
- **Weekly:** Detection performance analysis and trend identification
- **Monthly:** Detection capability assessment and gap analysis
- **Quarterly:** Detection program effectiveness evaluation

### Process Optimization
- **Tool Evaluation:** Regular assessment of detection tools and platforms
- **Automation Enhancement:** Increase detection automation coverage
- **Training Updates:** Refresh detection training content based on new threats
- **Procedure Updates:** Revise detection procedures based on lessons learned

---

## 14. Emergency Procedures

### Critical Security Incident Response
1. **Immediate Detection:** Detect and assess critical security incidents
2. **Activation:** Activate incident response team and crisis management
3. **Investigation:** Conduct immediate forensic analysis and investigation
4. **Containment:** Implement immediate containment and remediation
5. **Communication:** Provide regular updates to leadership and stakeholders
6. **Recovery:** Restore services with enhanced monitoring and security

### Contact Information
- **Security Hotline:** [Emergency contact number]
- **Escalation Path:** PDE → Security IC → CISO → Executive Leadership
- **External Resources:** Law enforcement, forensic experts, threat intelligence

---

## 15. Appendices

### A. Detection Checklist Templates
- **Pre-Deployment Detection Checklist**
- **Threat Detection Rule Review Checklist**
- **Incident Response Scope Template**
- **Forensic Analysis Template**

### B. Tool Configuration Guides
- **SIEM Platform Configuration**
- **Detection Rule Setup**
- **Forensic Tool Configuration**
- **Threat Hunting Tool Setup**

### C. Incident Response Playbooks
- **Critical Security Incident Response**
- **Data Breach Response**
- **Malware Incident Response**
- **Advanced Persistent Threat Response**

### D. Detection Mapping
- **Threat Categories to Detection Rules**
- **Attack Techniques to Signatures**
- **Security Controls to Monitoring**
- **Detection Framework Mapping**

---

**Document Version:** 1.0  
**Last Updated:** [Current Date]  
**Next Review:** [Date + 1 Year]  
**Approved By:** [Security Leadership]  
**Distribution:** Security Teams, SOC Operations, Incident Response Teams, Management