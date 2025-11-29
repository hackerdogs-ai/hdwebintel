# 🔐 Pillar 4: Encryption

**Scenarios to Protect:**

* Sensitive data protection (at rest, in transit, in use)
* Secure communications across internal systems, SaaS, and partners

**Design Points:**

* TLS for all data transit
* Full-disk/database encryption at rest
* Centralized key management with regular rotation
* Compliance with industry cryptographic standards (NIST, FIPS, ISO)

---

## 1. Roles & Ownership

### **Strategic Roles (Policy, Design, Governance)**

* **CISO:** Owns encryption strategy, ensures alignment with regulatory requirements (PCI DSS, HIPAA, GDPR).
* **Principal Security Architect:** Designs enterprise-wide crypto strategy — KMS (Key Management System), certificate lifecycle management, encryption-in-use (confidential computing).
* **Head of Data Security / Head of Cryptography:** Defines key management, quantum-resistance roadmap, selects commercial encryption platforms.

### **Execution Roles (Implementation, Operations, Monitoring)**

* **Crypto / Security Engineer:** Manages encryption systems (Vault, KMS, HSMs), enforces data-at-rest & in-transit encryption.
* **Cloud Security Engineer:** Implements encryption across AWS/GCP/Azure workloads (KMS, EBS, S3, SQL).
* **Database Administrator:** Ensures DB encryption (TDE, column-level).
* **SOC Analyst:** Monitors encryption logs, alerts on weak cipher usage.
* **DevOps Engineer:** Manages TLS cert deployment, automates renewal pipelines.
* **Red Team / Pen Tester:** Tests crypto implementation flaws, TLS downgrade attacks, key exposure risks.

---

## 2. Role Tasks & Cadence

### **Daily Tasks**

* Monitor certificate expirations & TLS handshake failures (DevOps, SOC).
* Alert on use of weak or deprecated ciphers (SOC).
* Validate KMS/HSM uptime & log collection (Crypto Engineer).

### **Weekly Tasks**

* Rotate ephemeral session keys in cloud KMS (Cloud Engineer).
* Verify new app deployments enforce TLS 1.2+/1.3 only (DevOps).
* Scan internal services for unencrypted endpoints (SOC Analyst).

### **Monthly Tasks**

* Review database/storage encryption configs (DBA + Cloud Engineer).
* Audit certificate usage across enterprise apps (Crypto Engineer).
* Patch crypto libraries (e.g., OpenSSL, BouncyCastle).

### **Quarterly Tasks**

* Rotate long-lived keys (KMS/HSM policy).
* Conduct cryptographic risk assessments (Architect + Crypto Engineer).
* Perform Red Team TLS downgrade & MITM simulation tests.
* Review compliance posture for encryption standards (PCI DSS, HIPAA).

### **Yearly Tasks**

* Refresh enterprise crypto policy (Architect, CISO).
* Review NIST/ISO standard updates (e.g., post-quantum crypto planning).
* Validate 3rd-party vendor encryption (Vendor Risk + IAM teams).
* Full key lifecycle audit (Crypto Engineer + Compliance).

---

## 3. Tools Used

### **Top Open Source Tools**

1. **HashiCorp Vault** – Secrets & key management, encryption-as-a-service.
2. **OpenSSL / LibreSSL** – Crypto library, TLS/PKI enforcement.
3. **Certbot (Let’s Encrypt)** – Automated TLS certificate issuance & renewal.
4. **GnuPG (GPG)** – File/email encryption.
5. **Stunnel** – TLS tunneling for legacy apps.
6. **StrongSwan** – IPSec VPN encryption.
7. **Wazuh** – Logs/alerts on encryption policy violations.
8. **CryptoGuard (part of OSSEC ecosystem)** – Crypto compliance scanning.
9. **cfssl (Cloudflare SSL toolkit)** – PKI & TLS certificate management.
10. **KMS SDKs (AWS, GCP, Azure open SDKs)** – Programmatic key use/rotation.

### **Top Commercial Tools**

1. **AWS KMS** – Managed key service for AWS workloads.
2. **Azure Key Vault** – Secrets, certs, and keys for Microsoft ecosystem.
3. **Google Cloud KMS** – Cloud-native encryption key service.
4. **Thales CipherTrust / Vormetric** – Enterprise data encryption + HSM.
5. **Venafi Control Plane** – Certificate lifecycle management.
6. **DigiCert CertCentral** – Enterprise TLS certificate automation.
7. **IBM Key Protect / HSM** – Centralized enterprise key service.
8. **Symantec Endpoint Encryption** – Device encryption.
9. **Trend Micro Endpoint Encryption** – File/folder/full-disk encryption.
10. **Zscaler Cloud Security** – TLS inspection and encrypted traffic monitoring.

---

## 4. Problems Solved & Expected Success Rate

* **Data Breach Exposure:** Encrypted-at-rest data ensures attackers cannot directly use stolen files. (\~95% reduction in usable data theft).
* **Man-in-the-Middle (MITM) Attacks:** TLS enforcement + cert lifecycle automation prevents protocol downgrade/expired cert abuse (\~90% success).
* **Compliance Failures:** Strong encryption ensures audit readiness for HIPAA, PCI DSS, GDPR (\~100% compliance if properly enforced).
* **Key Leakage Risk:** Vault/KMS/HSM usage minimizes hard-coded secrets (\~80% success in preventing developer key exposure).
* **Downtime Due to Expired Certificates:** Automated lifecycle management reduces incidents by \~95%.

---

## 5. Reporting & Dashboard Metrics

**Key Metrics for Encryption Pillar:**

* 🔑 **% of Data Encrypted at Rest** (storage, DBs, backups).
* 🌐 **% of Data Encrypted in Transit** (TLS adoption rates, non-TLS endpoints).
* 🗝 **Key Rotation Compliance %** (daily/quarterly/yearly depending on policy).
* ⏱ **Certificate Expiry SLA** (count of certs expiring in 30/60/90 days).
* 📊 **Weak Cipher Usage Incidents** (detected + remediated).
* 🧾 **Compliance Coverage %** (PCI DSS Req 3, HIPAA §164.312).
* 🕵️ **Unencrypted Endpoints Detected** (weekly scans).
* 💾 **Encrypted Backup %** (vs. total backups).
* 📉 **Downtime from Expired Certs** (MTTR metric).
* 🔒 **% of Keys in Centralized KMS/HSM** (vs. unmanaged secrets).

---


