# 📱 Pillar 21: Digital Exhaust Intelligence (DIGINT)

*(Following the exact pillar template structure and pillar ordering. DIGINT is Pillar #21 in your master table.)*&#x20;

---

## 1) Scenarios to Protect

1. **Mobile app telemetry leakage** – SDK beacons, analytics/advertising IDs, and crash logs exposing user/device/org patterns.
2. **IoT & wearables exhaust** – inadvertent broadcasting (BLE, Wi-Fi, Zigbee, UWB) revealing presence, movement, or inventory.
3. **Web/app tracking chains** – cookie syncs, tag piggybacking, and third-party pixels mapping users across domains.
4. **Enterprise app misconfig** – verbose logs, debug endpoints, or hidden APIs exposing credentials or sensitive metadata.
5. **AdTech/MarTech correlation** – attribution networks (IDFA/AAID, SKAdNetwork) enabling deanonymization or targeting.
6. **Supply-chain SDK risk** – trojaned ad SDKs/analytics libraries exfiltrating data or enabling code execution.
7. **Network telemetry misuse** – DPI, NetFlow/sFlow, and CDN logs abused for traffic de-anonymization or deanonymized routing.
8. **Location exhaust** – background location pings from apps/SDKs and passive Wi-Fi probe requests.
9. **Automotive/telematics** – vehicle apps and OBD dongles leaking route, VIN, or driver behavior.
10. **Cross-pillar fusion risks** – DIGINT signals stitched to CYBINT/THREAT\_INTEL/FININT for targeting or fraud.

---

## 2) Design Points

* **End-to-end capture**: client (mobile/web/IoT) ↔ network ↔ backend, across testbeds and production mirrors.
* **Protocol versatility**: HTTP(S), gRPC, WebSocket, QUIC, MQTT, CoAP, BLE, Zigbee, UWB, mDNS, SSDP.
* **Safe interception**: compliant MITM on owned/test devices; record-replay; PII minimization by default.
* **Attribution graph**: apps ↔ SDKs ↔ endpoints ↔ clouds (CDN/ASN) ↔ owners; enrich with WHOIS/DNS/ASN.
* **ML-assisted discovery**: automatic endpoint clustering, secret/PII detectors, tracker classification.
* **Red-blue loops**: pre-prod privacy tests & post-prod monitoring with drift alerts.
* **Compliance guardrails**: GDPR/CCPA, platform terms, and explicit consent boundaries baked into pipelines.
* **Cross-pillar connectors**: push enriched signals to CYBINT, THREAT\_INTEL, FININT, and DOMAIN\_INTEL.
* **Operational hardening**: rate-limiters, safe sandboxes, audit logging, chain-of-custody packaging.
* **Outcome focus**: measurable reduction in sensitive exhaust and faster detection of risky SDKs.
  *(Template alignment: “Design Points” section)*&#x20;

---

## 3) Roles & Ownership

### Strategic Roles

* **CISO / Chief Privacy Officer** – policy, risk appetite, reporting.
* **Chief Data Officer** – data governance, minimization standards.
* **Head of Mobile / IoT** – platform decisions, SDK/vendor approvals.
* **VP Trust & Safety** – user protection, abuse response.

### Operational Roles

* **DIGINT Analyst** – capture, label, and correlate digital exhaust.
* **Mobile Reverser / AppSec Engineer** – APK/IPA reversing, SDK mapping.
* **IoT Protocol Engineer** – RF/low-power protocol inspection and fuzzing.
* **Network Forensics Engineer** – packet/flow analysis, endpoint attribution.
* **Privacy Engineer** – PII/secret detection, redaction pipelines.
* **Data/ML Engineer** – clustering, tracker classification, drift monitoring.
  *(Template alignment: “Roles & Ownership” section)*&#x20;

---

## 4) Role Tasks & Cadence

* **Daily**

  * Capture test runs (mobile/web/IoT) through controlled MITM; diff endpoints/trackers.
  * Monitor production mirrors for new third-party domains/SDKs and secrets in transit.
  * Auto-classify trackers; route P1 leaks to IR/Legal.

* **Weekly**

  * Update SDK/vendor inventory & risk scores; review new hostnames/ASNs.
  * Publish “Exhaust Delta” (what changed in endpoints/params).
  * Validate fixes (regression runs) and refresh detection patterns.

* **Monthly**

  * Full app/SDK crawl audit; privacy design review of top apps/services.
  * Cross-pillar correlation: DIGINT ↔ CYBINT/THREAT\_INTEL/DOMAIN\_INTEL.
  * Update blocklists/allowlists and DLP/edge policies.

* **Quarterly**

  * Red-team privacy exercise (record-replay & deanonymization attempts).
  * Supplier/SDK due diligence refresh; tabletop with Legal & PR.
  * Executive metrics and roadmap adjustments.

* **Yearly**

  * Program maturity review; policy & consent model refresh; training.
  * External assessment vs. industry frameworks; publish annual report.

*(Template alignment: “Role Tasks & Cadence” section)*&#x20;

---

## 5) Tools & Reporting

### 🧑‍💻 Open-Source (≥10)

1. **mitmproxy** (TLS interception, HTTP/2/HTTP/3)
2. **MobSF** (mobile app static/dynamic analysis)
3. **Frida** + **Objection** (runtime instrumentation/hooking)
4. **jadx / apktool / Ghidra** (reverse engineering)
5. **Wireshark / TShark** (packet analysis)
6. **Zeek** (network telemetry & protocol parsing)
7. **Kismet / bettercap** (Wi-Fi/BLE/Zigbee reconnaissance)
8. **nfdump / nTopng** (NetFlow/sFlow)
9. **Osquery** (endpoint telemetry queries)
10. **Logstash/Elastic** (pipeline & indexing)
11. **mitmproxy2swagger** (API spec inference)
12. **TruffleHog / detect-secrets** (secret discovery)

### 💼 Commercial (≥10)

1. **Cellebrite** / **Magnet AXIOM** (mobile forensics)
2. **Grayshift GrayKey** (iOS acquisition in lawful contexts)
3. **NowSecure** / **Guardsquare** (AppSweep) (mobile security & privacy testing)
4. **Armis / Forescout / Claroty / Nozomi** (IoT/OT visibility)
5. **RiskIQ / Cortex Xpanse / Censys** (internet surface & tracker endpoints)
6. **mParticle / Segment / Tealium** (event/identity pipelines)
7. **Adjust / AppsFlyer / Kochava / Branch** (attribution/AdTech mapping)
8. **Apptopia / data.ai** (market/app intel)
9. **Palantir Gotham / Maltego** (entity resolution & correlation)
10. **Splunk / Sumo Logic** (telemetry analytics)
11. **Akamai / Cloudflare** (edge logs & request fingerprinting)

### Reporting & Dashboard Metrics

* **Executive KPIs**: Exhaust Reduction %, Time-to-Detect (TTD), High-Risk SDK Count, Cross-Pillar Confirmation Rate.
* **Analyst KPIs**: Tracker Classification Precision/Recall, Secret-in-Transit Incidents, New Endpoint Discovery Rate, Fix Verification SLAs.
  *(Template alignment: “Tools & Reporting” section; includes ≥10 OSS & ≥10 commercial)*&#x20;

---

## 6) Problems Solved & Expected Success Metrics

### Problems Solved

* Detects and stops sensitive **PII/secret leakage** in app, web, and IoT traffic.
* Maps **SDK/third-party data flows** and their real owners (domains/ASNs).
* Reduces **tracking/deanonymization risk** from AdTech/MarTech chains.
* Prevents **credential/session exposure** via misconfigured endpoints or verbose logs.
* Provides measurable **privacy posture** improvements and legal/comms defensibility.
* Feeds **THREAT\_INTEL/CYBINT** with high-value exhaust indicators.

### Expected Success Metrics

* **TTD for High-Risk Exhaust**: ≤ 24 hours (P1 incidents).
* **Tracker Classification**: ≥ 90% precision / ≥ 85% recall.
* **Exhaust Reduction**: ≥ 50% fewer sensitive parameters over 2 quarters.
* **Secret-in-Transit Incidents**: 0 critical by Q+1; ≤ 1 low/month thereafter.
* **Cross-Pillar Validation**: ≥ 90% confirmations with CYBINT/THREAT\_INTEL.
* **Remediation SLA Compliance**: ≥ 95% of P1/P2 issues within policy windows.

---

**Notes:**

* DIGINT is explicitly defined as “Digital exhaust (apps, IoT, metadata)” with app/device coverage and metadata correlation outcomes in your pillars table; roles and use-cases here follow that scope.&#x20;
* Sectioning, cadence, and “Tools & Reporting” layout strictly follow your pillar template conventions.&#x20;

If this meets your bar, I’ll proceed to **Step 2: DIGINT Dashboard Definition** using the same template discipline.
