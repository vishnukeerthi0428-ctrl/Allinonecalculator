## 2.6.6 Conflicts and proposed resolutions

| ID | Conflict | Source position | Blueprint position | Proposed resolution (for coordinator decision) | Impact if accepted | Decision owner |
|---|---|---|---|---|---|---|
| CONFLICT-300 | Two opportunity scoring models | SP-11 §Business-specific: fit/evidence/intent/readiness/timing 25/25/20/15/15, bands ≥ 75 / 50–74 / < 50. SP-11 §Coverage and examples: capability 30 / explicit need 25 / qualification 15 / geography 10 / budget 10 / timing 10, review defaults fit ≥ 70 and coverage ≥ 70 | DEC-011 and BRL-SCR-01…03 adopt only the first model | Keep DEC-011 as the **default and only active model at launch**. Register the six-factor model as an **optional scoring-version template "partnership-fit"** for partnership opportunity types (FR-ENH-A-007). Activation requires a benchmark on the same labelled set showing precision ≥ the default (BRL-ENH-A-01). "Coverage ≥ 70" is interpreted as the known-weight share (BRL-SCR-02 uses 0.60); when this version is active its own thresholds apply | No change to W1 build; 1–2 person-days later (Could) | Product Owner, AI lead |
| CONFLICT-301 | Residual investor/fundraising wording in group A documents | SP-03 OPT-15-03 "authorized investor/customer completes synthetic enquiry"; SP-12 "create scoped lead/investor record"; SP-12/13/14 OPT-12-03 "verified funding"; SP-13/14 "Investor app only fundraising"; SP-14 "Issuer or business line experiment", "Investment excludes ads/SEO"; SP-03 filters "offering/issuer thesis", "investment/delivery geography" | DEC-002 replaces such wording; DEC-058 separates the investor product | Apply DEC-002 to these **new instances**: read "investor/customer" as "customer", "lead/investor record" as "lead record", "verified funding" as "verified commercial receipt", "issuer" as "business line". The sentences "Investor app only fundraising" and "Investment excludes ads/SEO" describe the sibling product and impose no requirement here beyond DEC-058. No fundraising feature is added | None (wording) | Founder / Product Owner |
| CONFLICT-302 | Definition of source coverage | SP-11: successful fresh eligible source checks ÷ eligible due sources, per country and source category | KPI-27: approved sources monitored ÷ registry by country/sector | Keep **KPI-27** as the inventory measure. Add **KPI-ENH-A-01 "Fresh source coverage"** with the SP-11 formula, computed from the coverage ledger. Show both side by side on RP-04 and RP-ENH-A-01 | One extra KPI; no change to KPI-27 | Research lead |
| CONFLICT-303 | Reply classification taxonomy | SP-12: interest, decline, objection, unsubscribe, bounce, out-of-office, meeting, escalation | Part 2.2 WF-06: STOP, positive, question, objection, out of office, urgent, clinical | Adopt the **11-class union** in §2.6.5.2.6 (adds decline, meeting request and unknown; treats bounce as a provider event; keeps clinical and question). Add "decline" to the BRL-SEQ-02 stop list | AG-013 schema and eval set update; small | Product Owner, AI lead |
| CONFLICT-304 | Single relationship stage vs separate state machines | SP-37 §07: one relationship moves New → Qualified → Engaged → Quote requested → Negotiation → Contracted → Paid/fulfilment; SP-13 "shared relationship … IDs" | Part 2.3 keeps separate Lead, Opportunity, Deal, Quote, Contract, Payment, Order state machines; no relationship ID | Keep the separate state machines as the **only writable states**. Add a stable `relationship_id` and a **read-only derived relationship stage** (§2.6.5.2.7, FR-ENH-A-016). Never set the stage by hand or AI | Read model and Customer 360 panel; 3–5 person-days | Solutions Architect, Product Owner |

**Inconsistencies found in earlier parts (reported, not fixed):**

| # | Location | Issue | Suggested fix |
|---|---|---|---|
| 1 | Part 2.2 heading numbers | Part 2.2 uses `## 2.6 Universal execution engine` and `### 2.6.1 Dispatch sequence`; this part was assigned `2.6.x` numbering, so "§2.6.1" is ambiguous across the two files | Coordinator to renumber this part (for example 2.52.x after Part 2.5's 2.51) or always prefix with the part number in cross-references |
| 2 | Part 1 §1.8 vs SP-03 | Part 1 has 16 personas; SP-03 lists 21 role personas plus SaaS, website and acceptance personas; 4 source personas have no blueprint equivalent | Adopt §2.6.5.1.1–2 variants and P17–P20 |
| 3 | DEC-020 budget IDs | SP-11/13 cite an engineering cost line "C03" that DEC-020 does not define | Treat C03 as the engineering-effort line of Part 8.1 [ASSUMPTION-305]; add to DEC-020 if confirmed |
| 4 | BRD §1 vs blueprint seed data | RamVan and Smart Biochar are named in BRD §1 but absent from the blueprint | Seed as Planned offerings [ASSUMPTION-300] |
| 5 | BRL-SEQ-02 | Stop list lacks "decline" although SP-12 requires stop on decline | Covered by CONFLICT-303 resolution |

## 2.6.7 Expert persona review

| Persona | How the perspective was applied | What this persona would still flag |
|---|---|---|
| **Product Owner** | Classified every aspect against BR/FR/DEC; kept MoSCoW and waves; protected DEC-011, DEC-054 and DEC-064 by turning source variants into optional, gated versions; produced the AOP and WAR operating rhythm that makes KPIs actionable | Capacity: 43–72 extra person-days need a DEC on deferral (§2.6.5.9.2). The 15-sheet source inventory (GAP-300) and deck slides 10–14 are still missing |
| **Business Systems Analyst** | Built the atomic register (283 aspects) and programmatic reconciliations (17/17 APIs, 26/26 entities, 86/86 document-37 screen IDs, duplicate-section proof); wrote FRs with acceptance, rules with enforcement points and logical data | Physical schema and API paths for the new objects (AOP, experiment, delegation grant, coverage ledger) need Part 3.2/3.3 owners to assign IDs; candidate-API reconciliation for document 38 is owned by another group |
| **Growth / Marketing Strategist** | Added experiment registry with single-variable rule, holdouts, matched cohorts, stop triggers and scorecards; stage-pair funnel; outcome economics; segment playbooks for 11 MedMaarg segments | Minimum detectable effect and cohort sizing are not set; with Year-1 volumes (DEC-031) many experiments will be underpowered and must be read as descriptive |
| **Sales Operations Lead** | Reply taxonomy union with deterministic effects; relationship timeline; P03a/b/c and P07a/b variants with route-specific journeys; buy-side SoD; renewal block; cross-entity allocation block | Territory and assignment rules (round-robin vs named accounts) per persona variant are not specified in the source pack; quota/target setting per seller is absent |
| **UX Researcher** | Persona variants with goals, pains, screens and success measures; productivity protocol closing NFR-034's missing baseline; training record that never grants authority; panel additions instead of new screens; UI states per Part 2.5 §2.47 | Usability tests with real users cannot start until a clickable build exists (W2); persona variants need validation interviews with 2–3 real staff per variant |
| **QA Lead** (review) | 50 test cases including races, boundaries, isolation and UAT packs built from document 37; fixtures FX-A-01…06; AP-ENH-A register | UAT packs are manual; automation of TC-ENH-A-041/042 end-to-end in Playwright is recommended once screens stabilize |
| **Security / Compliance** (review) | R21 delegation with ABAC, one tenant per session, immediate revocation; jurisdiction activation record; recording consent; legal disclosure; website publisher SoD | Legal disclosure field list and deliverability thresholds must be confirmed by counsel and provider terms (ASSUMPTION-304, ASSUMPTION-306) |
| **FinOps** (review) | Cost lines per SPB; paid-provider gate; AI cost deltas computed (< $1/month); outcome economics with currency and zero-denominator rules | Exchange rate and provider prices to be verified at time of implementation (as of 27 Nov 2026) |

## 2.6.8 Tags register

### 2.6.8.1 Assumptions

| ID | Assumption | Where used | Validate with |
|---|---|---|---|
| ASSUMPTION-300 | RamVan and Smart Biochar are OrganicSpec offerings that stay in state Planned until readiness approval; they are Approved and Available only inside synthetic UAT fixtures | §2.6.5.1.7; CC-06; AOP-04 | OrganicSpec head |
| ASSUMPTION-301 | Benchmark uses up to 50 permitted records per source family; where fewer exist, the full permitted population is used | §2.6.5.2.4; FR-ENH-A-005 | Research lead |
| ASSUMPTION-302 | Weekly acquisition review lasts 45–60 minutes per startup or cluster, on Monday 09:00 local time | §2.6.5.1.6; CFG-ENH-A-04 | Startup heads |
| ASSUMPTION-303 | Productivity study uses 5 representative users per persona group (or all users if fewer) | §2.6.5.1.4 | UX lead |
| ASSUMPTION-304 | Deliverability thresholds: pause at hard bounce ≥ 2% or complaint ≥ 0.1% (rolling 7 days); stop at ≥ 5% or ≥ 0.3%; verify provider thresholds at time of implementation (as of 27 Nov 2026) | BRL-ENH-A-06 | Compliance lead, SES terms |
| ASSUMPTION-305 | "C03" in SP-11/SP-13 cost lines means the shared engineering-effort line (Part 8.1), not a monthly run budget | A13-15; §2.6.6 | FinOps lead |
| ASSUMPTION-306 | Legal disclosure block fields: legal name, CIN or equivalent registration ID, GSTIN where applicable, registered address, contact email/phone, grievance/privacy officer contact, links to privacy and terms; confirm per jurisdiction with counsel | FR-ENH-A-017 | Legal counsel |
| ASSUMPTION-307 | Delegation grants default to 90 days and are renewable by the client | P17; FR-ENH-A-015 | Service owner |
| ASSUMPTION-308 | Training records expire after 12 months | §2.6.5.1.4 | Tenant administrator |
| ASSUMPTION-309 | AG-013 confidence below 0.60 maps to class "unknown" (configurable) | §2.6.5.9.1 | AI lead |

### 2.6.8.2 Gaps

| ID | Gap | Impact | Proposed closure |
|---|---|---|---|
| GAP-300 | Referenced artefacts not supplied: "15-sheet commercial source cell inventory" (SP-11, SP-14) and "deck slides 10–14" (SP-11 MedMaarg segments) | AP-ENH-A-05 cannot pass; segment evidence unverified | Request from the founder; until then AP-ENH-A-05 is Pending and segment claims stay management claims (DEC-021) |
| GAP-301 | Agency / managed-service operator persona and delegation model absent | Managed-service clients cannot be served safely | P17, R21, FR-ENH-A-015 |
| GAP-302 | Service arrangement (self-service / managed / hybrid) not modelled | W31/W33 cannot offer the choice in SP-37 §05 | FR-ENH-A-015, CFG-ENH-A-07 |
| GAP-303 | Website legal disclosure per legal entity not specified | Public sites may lack required identity information | FR-ENH-A-017 |
| GAP-304 | No coverage ledger or per-family freshness | Coverage cannot be measured as SP-11 requires | FR-ENH-A-001, BRL-ENH-A-02 |
| GAP-305 | No acquisition operating plan or weekly review | KPIs are reported but not acted on in a governed cadence | FR-ENH-A-010, 012 |
| GAP-306 | NFR-034 baseline undefined | Navigation improvements cannot be proven | Productivity protocol §2.6.5.1.4 |
| GAP-307 | Integration administrator and template reviewer not defined | Credential and template governance unclear | P18/R12I, P19/R11T |
| GAP-308 | No rule on meeting/webinar recording consent | Privacy risk | BRL-ENH-A-05 |
| GAP-309 | No benchmark sample design for discovery | Precision claims not comparable | FR-ENH-A-005 |
| GAP-310 | Tool candidates (Scrapy, Trafilatura, SearXNG, PandaDoc, Crossbeam, PostHog, Socialinsider) not dispositioned | Unclear licence and cost exposure | §2.6.5.6 |

### 2.6.8.3 Conflicts

CONFLICT-300 to CONFLICT-304: see §2.6.6.

### 2.6.8.4 Recommendations

| ID | Recommendation | Section |
|---|---|---|
| RECOMMENDATION-300 | Persona variants (P03a, P03b, P03c, P07a, P07b, P10a, P13a, P13b, P14e, website roles) and new personas P17–P20 | §2.6.5.1.1–2 |
| RECOMMENDATION-301 | New role R21 and sub-roles R11T, R12I with ABAC-ENH-A-01…05 | §2.6.5.3.2–3 |
| RECOMMENDATION-302 | Source-family and segment playbook registry SPB-01…24 | §2.6.5.2.2–3 |
| RECOMMENDATION-303 | Coverage ledger and KPI-ENH-A-01 with weekly ≥ 90% target once stable | §2.6.5.1.5; FR-ENH-A-001 |
| RECOMMENDATION-304 | Paid data provider enabled only with ≥ 20% better cost per usable opportunity or incremental eligible records on the same corpus | BRL-ENH-A-03 |
| RECOMMENDATION-305 | Acquisition operating plan AOP-01…05 and weekly acquisition review | §2.6.5.1.6 |
| RECOMMENDATION-306 | Experiment registry with single-variable rule and stop triggers | FR-ENH-A-011; BRL-ENH-A-13 |
| RECOMMENDATION-307 | Outcome economics report and KPI-ENH-A-03 | FR-ENH-A-013 |
| RECOMMENDATION-308 | Jurisdiction activation decision record | FR-ENH-A-014 |
| RECOMMENDATION-309 | Relationship ID and derived relationship stage | FR-ENH-A-016 |
| RECOMMENDATION-310 | UAT packs and demonstration script from document 37 | §2.6.5.8.6 |
| RECOMMENDATION-311 | Training and competence record that never grants authority | §2.6.5.1.4; BRL-ENH-A-10 |
| RECOMMENDATION-312 | Integration candidate disposition table | §2.6.5.6 |
| RECOMMENDATION-313 | Acceptance RACI and AP-ENH-A-01…12 | §2.6.5.1.3; §2.6.5.8.7 |
| RECOMMENDATION-314 | User-productivity measurement protocol | §2.6.5.1.4 |
| RECOMMENDATION-315 | Bulk action preview with hash | FR-ENH-A-019 |

### 2.6.8.5 New identifiers issued by this part

| Family | Range | Count |
|---|---|---|
| Functional requirements | FR-ENH-A-001…020 | 20 |
| Business rules | BRL-ENH-A-01…14 | 14 |
| ABAC rules | ABAC-ENH-A-01…05 | 5 |
| User stories | US-01-EA01, US-03-EA01, US-05-EA01…04, US-06-EA01, US-08-EA01…02, US-09-EA01, US-11-EA01, US-12-EA01…03, US-14-EA01, US-15-EA01…02, US-16-EA01, US-17-EA01…02, US-18-EA01…02, US-19-EA01…02, US-20-EA01…03, US-21-EA01…02 | 30 |
| Test cases | TC-ENH-A-001…050 | 50 |
| KPIs | KPI-ENH-A-01…05 | 5 |
| Reports | RP-ENH-A-01…04 | 4 |
| Notifications | NT-ENH-A-01…07 | 7 |
| Configuration | CFG-ENH-A-01…08 | 8 |
| Playbooks | SPB-01…24 | 24 |
| Acquisition plans | AOP-01…05 | 5 |
| Acceptance procedures | AP-ENH-A-01…12 | 12 |
| Fixtures | FX-A-01…06 | 6 |
| Risks | RSK-ENH-A-01…04 | 4 |
| Personas and roles | P17–P20; 12 variants; R21, R11T, R12I | 19 |
