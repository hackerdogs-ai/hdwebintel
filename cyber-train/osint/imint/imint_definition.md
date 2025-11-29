# **Step 1; Pillar Definition**&#x20;

## 📌 **Pillar 3: Imagery Intelligence (IMINT) 🛰️🗺️**

---

### **1. Scenarios to Protect**

* 🧱 Undeclared facility construction/expansion (dual-use, defense, energy)
* 🚢 Maritime smuggling, dark vessels, IUU fishing, ship-to-ship transfers
* 🛢️ Sanctions evasion via covert logistics, pipeline taps, and masked storage
* ⚡ Critical infrastructure risks (substations, telecom, dams, pipelines)
* 🔥 Wildfires, floods, earthquakes—rapid damage & accessibility assessment
* 🧨 Conflict indicators: force mobilization, airfield activity, artillery impacts
* ⛏️ Illegal mining/logging and environmental degradation at protected sites
* 🚧 Border incursions, new roads, bridging, and choke-point changes
* 🏗️ Real-estate fraud & zoning violations at scale
* 🛰️ Disinformation rebuttal with verifiable before/after imagery

---

### **2. Design Points**

* 🖼️ **Sensor mix:** EO (RGB/panchromatic), multispectral, hyperspectral, thermal, **SAR** for all-weather/night; UAV and aerial as supplements
* ⏱️ **Revisit & latency:** tasking → delivery SLAs; tip-and-cue from other pillars to optimize windows
* 🧭 **Geo-accuracy:** orthorectification, DEM use, RMSE tracking, consistent CRSs
* ☁️ **Pre-processing:** cloud/shadow masks, atmospheric correction, pansharpening
* 🔁 **Change detection:** pixel/object-based (OSCD), time-series, and persistent change filters
* 🤖 **ML/CV:** object detection (vessels, aircraft, vehicles), segmentation (burn scars, water), counting, anomaly detection, explainability
* 🧩 **Fusion:** join with GEOINT basemaps, SOCMINT narratives, and HUMINT leads for attribution
* 🧰 **Pipelines:** scalable ingestion, tiling/COGs, STAC catalogs, metadata lineage
* 🔒 **Governance:** licensing/ToS compliance, privacy & ethical capture, export controls
* 🧪 **Validation:** ground-truth sampling, analyst review queues, precision/recall dashboards

---

### **3. Roles & Ownership**

**🎯 Strategic Roles**

* Chief Intelligence Officer / Director of Geospatial Intelligence
* Head of Risk & Compliance / ESG Lead
* Crisis Management & Business Continuity Director
* National Security / Public Safety Leadership

**🛠 Operational Roles**

* IMINT Analyst / Geospatial Intelligence Analyst
* SAR Specialist / Imagery Scientist
* Geospatial Data Engineer / Pipeline SRE
* CV/ML Engineer (Detection & Change)
* Maritime/Tradecraft Analyst (AIS fusion)
* Energy/Infra Analyst & Environmental Analyst



---

### **4. Role Tasks & Cadence**

**Daily 🗓️**

* Monitor AOIs for change; triage vendor/new scenes; run cloud/SAR alternates
* Execute automated object & change detection; push P1 alerts
* Verify high-impact events with multi-source imagery (SAR+EO) and basemaps

**Weekly 📅**

* Refresh AOI baselines; update tip-and-cue rules from SOCMINT/HUMINT
* Curate analyst-verified training chips; retrain/threshold detection models
* Publish “Weekly IMINT Change Log” with evidence packs

**Monthly 📆**

* Deep-dive reports (facility growth, maritime patterns, infra risk)
* Coverage audit: revisit gaps, latency, cloud-free %, SAR utilization
* Update AOI roster, vendor tasking priorities, and ML evaluation sets

**Quarterly 📤**

* Readiness/tabletop for disaster & conflict surges
* Vendor & sensor mix review; cost/coverage optimization
* Governance & legal audit of licensing, retention, access controls

**Yearly 📈**

* Strategy/SOP refresh; dataset curation; model re-baselining
* External maturity assessment; red-team deception & spoofing drills



---

### **5. Tools & Reporting**

**🧑‍💻 Top Open Source Tools (10+)**

1. **QGIS** – desktop GIS & plugin ecosystem
2. **GRASS GIS** – advanced raster/terrain analytics
3. **ESA SNAP** – Sentinel/SAR processing toolkit
4. **GDAL** – raster/vector conversions & warping
5. **Rasterio** – Python raster IO/analysis
6. **Orfeo ToolBox (OTB)** – remote sensing ML & segmentation
7. **OpenDroneMap** – UAV photogrammetry/orthomosaics
8. **OpenAerialMap** – community aerial imagery & tiling
9. **Semi-Automatic Classification Plugin (QGIS)** – supervised classification
10. **CesiumJS** – 3D tiling & time-dynamic visualization
11. **Leaflet** – lightweight web mapping
12. **ExifTool / ImageJ(Fiji) / OpenCV** – metadata & CV analysis

**💼 Top Commercial Tools (10+)**

1. **Maxar SecureWatch** – high-res archive & tasking
2. **Planet (PlanetScope/SkySat/Explorer)** – high-cadence EO
3. **Airbus OneAtlas / UP42** – tasking + analytics marketplace
4. **Capella Space** – high-res taskable SAR
5. **ICEYE** – very-high-revisit SAR
6. **BlackSky Spectra** – rapid-revisit EO + alerts
7. **Satellogic Aleph** – constellation access & analytics
8. **Descartes Labs Platform** – geospatial cloud & ML pipelines
9. **Orbital Insight GO** – activity analytics (counts, anomalies)
10. **SkyWatch EarthCache** – multi-provider imagery API
11. **Esri ArcGIS Pro/Online** – enterprise geospatial & dissemination
12. **EOS LandViewer / LiveEO / SpaceKnow** – discovery, change & infra risk

**📊 Reporting & Dashboard Metrics**

* **Strategic:** AOI Coverage %, Average Revisit (hrs), Time-to-Insight (TTI), Incident Lead Time vs. media, Cost-per-AOI, Risk Reduction Score
* **Operational:** Cloud-free % (by AOI/sensor), Tasking→Delivery SLA, Georegistration RMSE, Detection Precision/Recall/F1, Analyst Verification Throughput, Cross-Pillar Validation Rate



---

### **6. Problems Solved & Expected Success Metrics**

**🔒 Problems Solved**

* Early warning of construction/mobilization; independent verification in crises
* All-weather/night coverage with SAR when EO is clouded or dark
* Rapid disaster mapping & access planning for responders
* Detection of maritime sanctions evasion and illicit resource extraction
* Continuous infra risk monitoring for utilities, energy, telecom, and transport

**📊 Expected Success Metrics**

* **Time-to-Insight (TTI):** ≤ 6–12 hrs for priority AOIs (SAR-enabled)
* **Detection Quality:** object/change **precision ≥ 0.90**, **recall ≥ 0.85**
* **Coverage:** ≥ 90% AOIs imaged monthly; **cloud-free ≥ 70%** (EO) with SAR backfill
* **Geo-accuracy:** orthorectification **RMSE ≤ 5 m** (sensor-dependent)
* **SLA:** tasking→delivery **≤ 6 hrs** (priority) / **≤ 24 hrs** (standard)
* **Validation:** cross-pillar confirmation **≥ 85%** (SOCMINT/HUMINT/GEOINT)
* **Adoption:** 100% priority incidents include IMINT evidence packs in briefs

---

*This section mirrors your required headings, cadence blocks, and tools/reporting structure from the template.*&#x20;
