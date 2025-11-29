Awesome — moving in the correct sequence, here is **Pillar #8: DOMAIN\_INTEL** — **Step 1: Pillar Definition** — in your strict five-section template (with clear subsections, emojis, ≥10 OSS and ≥10 commercial tools, cadence, reporting metrics, and problems solved & success rates).

---

# 🌐 **Pillar #8 — DOMAIN\_INTEL (Domain & DNS Intelligence)**

*Open-source intelligence on domains, DNS, certificates, hosting, and infrastructure links that power detection, attribution, and takedowns.*

---

## **1) Pillar Definition & Scenarios to Protect**

### 1.1 Purpose & Scope

* Provide **end-to-end visibility** into domains, DNS records, passive DNS (pDNS), hosting, CDN, SSL/TLS certificates, and historical changes.
* Enable **brand protection, phishing disruption, C2/infra attribution, typosquat detection, and sanctions/compliance screening** of web infrastructure.
* Fuse with other pillars (CYBINT, COMINT, SIGINT, FININT) for **campaign-level understanding**.

### 1.2 Core Intelligence Questions

* Who **registered** this domain? When did it change? What’s the **infrastructure** behind it (NS/A/AAAA/MX/TXT/CNAME, CDN, ASN)?
* Is it part of a **malware/C2** graph, **phishing** kit cluster, or a **brand abuse** campaign?
* What **historical resolution** patterns exist (pDNS)? Which **neighbors** (co-hosting, same certificate/registrant/ASN) correlate?
* Does it use **DGA**, **fast-flux**, or **bulletproof** services?
* What’s the **jurisdiction**, **registrar**, and **policy leverage** for takedown?

### 1.3 Scenarios to Protect (with Problems Solved)

* 🎯 **Phishing & Brand Abuse:** Detect lookalikes/typosquats; block & take down.
* 🕵️ **Malware C2 & Botnets:** Map domain clusters, DGAs, and fast-flux to cut command chains.
* 🔐 **Account Takeover Domains:** Catch credential-harvesting infrastructure early.
* 🧩 **Fraud & Scams:** Identify disposable domains, hosting churn, and mule ecosystems.
* ⚖️ **Sanctions/Compliance:** Screen domains/hosts linked to restricted parties.
* 🧭 **Attribution Support:** Link infra (WHOIS, certs, pDNS) to actor fingerprints.

### 1.4 Expected Success Rates (targets)

* **Phishing/typosquat precision ≥ 0.90**, recall ≥ 0.85.
* **Malicious domain takedown success ≥ 75%** within SLA.
* **Average discovery lead-time advantage ≥ 48h** vs. public reporting.
* **Infrastructure correlation accuracy ≥ 0.9** across pDNS/cert/ASN graphs.

---

## **2) Design Principles (Design Points)**

### 2.1 Collection & Coverage

* Multi-source ingestion: **TLD zone files**, **WHOIS/RDAP**, **pDNS**, **SSL/TLS CT logs**, **BGP/ASN**, **hosting/CDN**, **DNSSEC**, **sinkholes**, **open crawlers**.
* High-frequency refresh (minutes → hours) for volatile DNS.

### 2.2 Normalization & Fusion

* Normalize to a common schema (domain, FQDN, RRsets, TTL, first\_seen/last\_seen, registrant, registrar, ASN, CA/cert fingerprint).
* Graph correlation on **co-hosting, cert reuse (SPKI/SPKI-SHA256), name server reuse, registrar reuse, SOA email**, and **TXT/DMARC/DKIM** fingerprints.

### 2.3 Analytics & Detection

* **DGA detection**, **fast-flux scoring**, **new-domain risk**, **string similarity** (LD, Jaro-Winkler), **brand distance**, **WHOIS privacy heuristics**, **registrar risk**, **hosting risk**, **CERT transparency anomalies**.

### 2.4 Policy, Ethics & Compliance

* Respect **ToS**, **robots**, **rate limits**, **privacy** (avoid unnecessary PII storage).
* Evidence chain for **takedowns** and **legal escalations**.

### 2.5 Cross-Pillar Integrations

* **CYBERINT:** IOC enrichment, malware infra → domain graphs.
* **COMINT/SIGINT:** Correlate DNS with network telemetry or RF beacons.
* **FININT:** Registrar/hosting payments & owners for sanctions/UBO risk.

---

## **3) Roles & Ownership**

### 3.1 Strategic Roles

* **Domain Intelligence Strategist** 🧭 — sets roadmap, success KPIs, policy posture.
* **CISO / Brand Risk Owner** 👔 — consumes impact metrics, approves takedown posture.

### 3.2 Operational Roles

* **Domain Threat Analyst** 🔎 — investigations, clustering, attributions.
* **pDNS/Telemetry Engineer** 🛠 — ingestion reliability, schema, and scaling.
* **Detection Scientist (DGA/Flux)** 🧪 — models for DGA/fast-flux/brand distance.
* **Brand Abuse & Takedown Lead** 🛡 — filings to registrars/hosts/CAs.
* **CTI Integrations Engineer** ⚙️ — IOC feeds → SIEM/SOAR/TIP (STIX/TAXII).
* **Compliance Officer** 📜 — ToS/legal review, audit evidence packs.

---

## **4) Role Tasks & Cadence**

### 4.1 On-Demand (RFI/Investigations)

* **RFI\_Lookalike\_Domain\_Investigation:** rapid triage of suspicious FQDN.
* **RFI\_Infrastructure\_Attribution:** build infra graph (pDNS/cert/ASN/NS).
* **RFI\_Takedown\_Package:** compile registrar/host/CA evidence & filings.
* **RFI\_DGA\_Campaign\_Sweep:** detect & list candidate DGAs with seeds.

### 4.2 Daily

* New-domain & newly-observed-host detection; brand distance alerts.
* WHOIS/RDAP changes; CT-log deltas; NS/MX/TXT drifts.
* Publish **IOC feed** (malicious domains/FQDNs) to SIEM/SOAR/TIP.

### 4.3 Weekly

* Domain-cluster rollups (campaign graphs, shared certs/NS/ASN).
* Registrar/host takedown success tracking; false-positive review.

### 4.4 Monthly

* DGA & fast-flux model eval; threshold tuning; precision/recall report.
* Registrar/host/CA risk league table; sanction/compliance exposure.

### 4.5 Quarterly

* Executive brief; red-team simulation (brand-phish & DGA drill).
* Compliance audit of evidence packs & takedown process.

### 4.6 Yearly

* Strategy refresh; vendor review; coverage & latency benchmarking.

---

## **5) Tools & Reporting**

### 5.1 Open-Source Tools (≥10) 🧑‍💻

1. **Amass** (OSINT DNS mapping)
2. **Subfinder** (subdomain discovery)
3. **dnsx / massdns** (DNS resolution at scale)
4. **dnstwist** (typosquat/lookalike generation)
5. **ZMap / zgrab2** (Internet-wide scanning, banners/certs)
6. **certstream / crt.sh** (Certificate Transparency feeds)
7. **Censys Search (OSS API tier)**
8. **Shodan (community/OSS tooling)**
9. **Whois/RDAP CLI & python-whois**
10. **Maltego CE** (link analysis)
11. **Urlscan.io (public API)**
12. **IntelOwl** (multi-source enrichment)

### 5.2 Commercial Tools (≥10) 💼

1. **RiskIQ / Microsoft Defender TI**
2. **Recorded Future** (domain risk, brand abuse)
3. **PassiveTotal (RiskIQ)** (historic DNS/WHOIS)
4. **DomainTools Iris** (pDNS, WHOIS history, risk score)
5. **Farsight DNSDB / SecurityTrails** (historic DNS)
6. **Quad9 / Cisco Umbrella** (resolution telemetry/blocks)
7. **BrandShield / ZeroFox** (brand abuse detection)
8. **Flashpoint** (underground + domain risk)
9. **CrowdStrike Falcon Intel** (infra context)
10. **Palo Alto AutoFocus** (campaign infra)
11. **Akamai Guardicore/ETP** (DNS/host intel)
12. **Illuminati/WhoisXML API** (WHOIS datasets)

### 5.3 Reporting & Dashboard Metrics 📊

**Operational KPIs**

* **New malicious domains detected/day**; **pDNS coverage %**; **CT-log delta count**.
* **DGA precision/recall**, **fast-flux score accuracy**, **brand distance F1**.
* **Takedown success rate** and **mean time-to-takedown (TTTD)**.
* **False positive rate**; **investigation cycle time**; **evidence pack completeness %**.

**Strategic KPIs**

* **Campaigns disrupted/quarter**; **registrar/host cooperation index**.
* **Decision impact (# exec actions)**; **compliance audit pass rate (100%)**.
* **Lead-time advantage vs. public reporting (hours/days)**.

**Success Targets**

* TTTD **≤ 72h (p75)**; FP rate **≤ 10%** on brand lookalikes; **≥ 85%** campaign clustering accuracy; evidence packs **100%** ToS-compliant.

---

If this matches your template requirements for Step 1, I’ll proceed to **Step 2: DOMAIN\_INTEL Dashboard Definition** next (sections, widgets, and metric wiring), keeping the same quality bar and format.
