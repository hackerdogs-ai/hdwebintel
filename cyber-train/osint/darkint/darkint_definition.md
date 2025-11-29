Got it — here is **Step 1: DARKINT Pillar Definition** following your exact pillar template format (numbered sections, subsections, emojis, ≥10 OSS and ≥10 commercial tools, plus Problems Solved & Expected Success Metrics).&#x20;

---

# 📟 Pillar 13: Dark Web Intelligence (DARKINT) 🕳️🕵️

---

## **1. Scenarios to Protect**

* 🕸️ **Illicit marketplace activity** (malware kits, exploits, data dumps, PII/PHI for sale)
* 🔓 **Credential & session theft** (initial access brokerage, stealer logs, OTP bypass tools)
* 💳 **Financial fraud enablement** (fullz, BIN lists, money mule networks, cash-out guides)
* 🧪 **Exploit & ransomware ecosystem** (affiliate recruiting, RaaS updates, leak site posts)
* 🧰 **Tooling distribution** (phishing kits, obfuscators, crypters, loaders, C2 panels)
* 🏴‍☠️ **Insider threat & doxxing** (company insiders, whistleblows, extortion threats)
* 🧬 **Sector-specific threats** (healthcare data auctions, ICS access, telecom creds)
* 🛰️ **Geo/security operations** (weapon sales, travel docs, forged IDs, OPSEC guides)
* 🧯 **Extortion & brand abuse** (domain impersonation, takedown evasion, smear ops)
* 🧭 **Cross-pillar tasking** (pivot to CYBINT/THREAT\_INTEL/FININT for attribution)

---

## **2. Design Points**

* 🌐 **Coverage breadth:** Tor (.onion), I2P, Telegram/IRC bridges, invite-only forums, paste sites
* 🔍 **Discovery & persistence:** crawler rotation, invite acquisition, handle stewardship, OPSEC playbooks
* 🔐 **Safe collection:** sandboxed Tor gateways, egress controls, content hashing, malware detonation isolation
* 🧩 **Entity resolution:** seller ↔ handle ↔ crypto wallet ↔ infrastructure (domain/IP/cert)
* 🧠 **Enrichment & scoring:** actor trust/reputation, commodity quality, scam probability, risk scores
* 🧵 **Thread intelligence:** topic evolution, affiliate relationships, broker–buyer links
* 💱 **Crypto analytics:** wallet clustering, on/off-ramp attribution, mixer heuristics
* 🧪 **Verification:** cross-source corroboration, proof-of-goods checks, decoy buys (lawful), leak validation
* 🧭 **Cross-pillar fusion:** map DARKINT → ATT\&CK/CYBINT/FININT for detections & takedowns
* 🛡️ **Compliance & ethics:** GDPR/ToS alignment, no entrapment/solicitation, evidence chain-of-custody

---

## **3. Roles & Ownership**

### 🎯 **Strategic Roles**

* **Head of Threat Intelligence** 🛡️
* **CISO / Chief Risk Officer** 🧭
* **Fraud & Financial Crime Director** 💳
* **Brand & Trust/Safety Leader** 🏷️

### 🛠 **Operational Roles**

* **Dark Web Analyst** 🕵️ – forum monitoring, actor engagement triage, leak validation
* **Crypto Intelligence Analyst** ₿ – wallet clustering, cash-out pathfinding, sanctions checks
* **Threat Researcher (RaaS/Exploit)** 🧪 – affiliate tracking, TTP mapping, kit analysis
* **Data Engineer (Collection/ETL)** ⚙️ – robust crawlers, de-duplication, normalization, storage
* **Intel Integrations Engineer (STIX/TAXII)** 🔗 – TIP/SIEM/SOAR delivery and telemetry loopback
* **Legal/Compliance Officer** ⚖️ – policy guardrails, approvals, audit & retention control

---

## **4. Role Tasks & Cadence**

**Daily 🗓️**

* Crawl markets/forums/leak sites; normalize listings and dumps
* Triage mentions of brand, domains, VIPs, products, and high-value secrets
* Resolve wallets, price points, escrow terms; enrich with risk/actor scores
* Generate alerts to SOC/IR/Fraud/Brand teams (P1–P3)

**Weekly 📅**

* Update **actor dossiers** (handles, rep scores, known alts, crypto clusters)
* Summarize **RaaS & exploit trends**; leak-site activity deltas
* Validate **credential dumps** and stealer-logs; produce block/reset lists

**Monthly 📆**

* **Market ecosystem report** (commodities, prices, scams, supply shifts)
* **Crypto flow reports** (wallet clustering, exchange exposure, sanction risk)
* **Detection packs** for SOC (IOCs, YARA/Sigma, ATT\&CK technique mapping)

**Quarterly 📤**

* **Executive brief** on DARKINT risk posture & ROI (loss avoided, takedown efficacy)
* **Tabletop exercises** (extortion/leak scenarios with Legal/PR/IR)
* **Compliance audits** (collection scope, retention, ToS/GDPR adherence)

**Yearly 📈**

* **Strategy refresh** & vendor/tooling review; coverage/maturity benchmarking
* **Training** (language/localization, OPSEC, crypto analytics, evidence handling)
* **State of Dark Web Threats** report for board/regulators

---

## **5. Tools & Reporting**

### 🧑‍💻 **Top Open Source Tools (≥10)**

* **Tor Project (Tor Browser, tor, torsocks)** – safe access/egress to .onion services
* **Ahmia API** – dark-web search/index queries
* **OnionScan / onionprobe** – .onion service scanning & misconfig checks
* **Scrapy / Scrapy-Playwright / Trafilatura** – resilient crawling & content extraction
* **Stormcrawler** – large-scale, distributed crawling
* **SpiderFoot (OSS modules)** – data enrichment (handles, emails, domains)
* **ExifTool / OCRmyPDF** – artifact parsing from dumps/evidence packs
* **Hashcat / John the Ripper** – password hash assessment (lawful testing)
* **BlockSci / bitcoinlib** – blockchain parsing & analytics
* **Maltego CE + custom transforms** – link analysis (wallets ↔ handles ↔ infra)

### 💼 **Top Commercial Tools (≥10)**

* **Flashpoint** – deep/dark monitoring, finished intel
* **DarkOwl Vision** – broad .onion coverage & searchable archives
* **KELA** – closed-forum/market insights, actor tracking
* **Intel 471** – cybercrime ecosystem & access brokers
* **Cybersixgill** – automated collection & actor analytics
* **S2W (Flare/DarkTracer)** – leak site & credential exposure monitoring
* **Recorded Future** – dark-web integrations & risk scoring
* **ZeroFox** – brand/digital risk + takedown workflows
* **Constella / SpyCloud** – identity & account takeover data
* **Chainalysis / TRM Labs / Elliptic** – crypto tracing & sanctions/exchange attribution

### 📊 **Reporting & Dashboard Metrics**

**Strategic Metrics (Executive Level)**

* 💰 **Loss Avoided (USD)** via early resets/blocks & takedowns
* 🧭 **Exposure Risk Index** (brand/VIP/product composite)
* 🔗 **Actor Disruption Impact** (# disrupted sellers, affiliate shutdowns)
* 🧾 **Regulatory/Audit Readiness** (evidence packs, chain-of-custody completeness)
* 🧯 **Extortion Lead-Time Advantage** (hours before public leak)

**Operational Metrics (Analyst Level)**

* 📈 **Collection Coverage** (# sources/markets/forums actively indexed)
* 🧵 **Validated Leaks** (# dumps verified with sampled records)
* 👤 **Actor Dossier Freshness** (median days since last update)
* 🪙 **Wallet Attribution Rate** (% clustered with exchange/on-ramp link)
* 📨 **Alert Actionability** (% alerts that drove resets/blocks/cases)
* 🔁 **Cross-Pillar Validation** (% DARKINT signals affirmed by CYBINT/FININT/THREAT\_INTEL)

---

## **6. Problems Solved & Expected Success Metrics**

### 🔒 **Problems Solved**

* **Early warning** of breaches, credential exposures, and insider sales
* **Disruption of criminal supply chains** (access brokerage, RaaS, data brokers)
* **Actionable remediation** (reset lists, domain/brand takedowns, wallet reporting)
* **Attribution lift** via wallet clustering, handle linkage, and infra pivots
* **Fraud reduction** by blocking monetization paths and mule onboarding
* **Executive visibility** with quantifiable **loss-avoided** and takedown ROI
* **Audit-safe operations** (ToS/GDPR-respecting collection, reproducible evidence)

### 📈 **Expected Success Metrics**

* ⏱ **Mean Time-to-Alert (MTTA)** for high-risk findings: **≤ 6 hours**
* 🧵 **Leak Validation Accuracy**: **≥ 95%** (sampled records)
* 👤 **Actor Dossier Coverage (priority set)**: **≥ 90%** updated monthly
* 🪙 **Wallet Attribution Rate**: **≥ 70%** clustered with risk labels/exchanges
* 📣 **Alert Actionability**: **≥ 80%** result in resets/blocks/cases within SLA
* 💰 **Loss Avoided** (quarterly): trend **↑**, target **>\$X** (program-specific)
* 🧯 **Extortion Lead-Time Advantage**: **≥ 24h** before public disclosure
* 🧾 **Chain-of-Custody Completeness**: **100%** for P1 cases

---

If you’re happy with this **Step 1 (DARKINT)**, I’ll proceed to **Step 2: DARKINT Dashboard Definition** in the same template-quality style next.
