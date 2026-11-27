# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 0, Document Ingestion and Validation

| Field | Value |
|---|---|
| Document | Application Blueprint, Part 0 of 10 |
| Version | 0.1 (draft for Product Owner review) |
| Date | 27 Nov 2026 |
| Inputs | `01_Business_Requirements.docx` (BRD), `02_Functional_Specification.docx` (FRD) |
| Status | Part 0 complete. Awaiting "continue" for Part 1 |
| Authoring lens | Product Owner, BSA, Solutions/Technical Architect, Principal Engineer, UX Lead, Data Architect, QA Lead, Security/Compliance/AI Governance, DevOps/SRE, FinOps |

---

## 0.1 Ingestion record

### 0.1.1 Files received and read

| # | File | Size | SHA-256 (first 16) | Readable | Extracted volume | Read in full |
|---|---|---|---|---|---|---|
| 1 | 01_Business_Requirements.docx (BRD) | 67,864 bytes | 67f8d6b7b5d20722 | Yes | 1,481 lines / 88 KB text, 17 top-level sections, 139 headings | Yes |
| 2 | 02_Functional_Specification.docx (FRD) | 110,824 bytes | a1591e96063a06fc | Yes | 3,028 lines / 360 KB text, 16 top-level sections, 256 headings (incl. 147 screen specs) | Yes |

**Extraction method:** I parsed the OOXML (`word/document.xml`) directly. I kept the heading styles and the table rows. I did not use OCR, and no content was lost. Both documents are complete and readable, so **Part 0 does not stop.** Some artefacts that the documents *reference* were not attached. I log them as gaps (GAP-007) and none of them blocks the blueprint.

### 0.1.2 Citation convention ([ASSUMPTION-000])
Neither document numbers its sections. For citations I number the top-level headings in document order, and I number sub-headings in order within each section.

**BRD section map**

| BRD § | Title | Content type |
|---|---|---|
| §1 | Product purpose and operating boundary (§1.1 Initial startup configurations; §1.2 Technology and execution principles) | Scope, independence, tenancy, 4 startups, stack |
| §2 | Authority and data protection | 7 actor types and their restrictions |
| §3 | Unified Command Centre, seven primary views | Admin information architecture |
| §4 | Business-specific acquisition and commercial conversion | 4 vertical sequences, scoring formula, KPIs |
| §5 | Workflow register, end-to-end execution | 14 workflows and the engine pattern |
| §6 | Consolidated effort and operating cost assumptions | Effort (person-days), monthly run-cost table |
| §7 | Commercial business requirement register (§7.1–§7.66) | 66 module requirements (objective, dependency, acceptance) |
| §8 | Commercial strategy and operating requirements | MedMaarg strategy, GTM, phase gates (Day 1–365), budgets, verified sources |
| §9 | Website and confidential Admin operating contract (§9.1 Business acceptance and outcomes) | Surfaces, routing, publication |
| §10 | Cost-efficient automation and acceptance policy | Open-source-first, paid-fallback rule, UAT rule |
| §11 | Business acceptance and ownership | Vertical acceptance statements |
| §12 | Implementation, verification and delivery controls (§12.1 Success controls; §12.2 Evidence record) | M01–M66 + B-TENANT/B-WEB/B-AUTO/B-SVC/B-QA table |
| §13 | Business outcome acceptance and authority (§13.1 Measurable outcomes; §13.2 Activation boundary) | Outcome definitions |
| §14 | Optimization engineering and acceptance (§14.1 Cost; §14.2 Automation; §14.3 Business Conversion; §14.4 SaaS Profitability) | OPT-03/04/12/20 items |
| §15 | Implementation acceptance and verification | 5 acceptance procedures |
| §16 | Implementation acceptance and final decision controls | Repeat of §15 plus boundary conditions |
| §17 | Current multi-startup, omnichannel and automation scope (§17.1) | 9 new interfaces (W31–W34, A109–A113) |

**FRD section map**

| FRD § | Title | Content type |
|---|---|---|
| §1 | Product purpose and operating boundary (§1.1, §1.2) | Same as BRD §1 |
| §2 | Global filter hierarchy and contextual filters | 11 filter families and filter rules |
| §3 | Unified Command Centre, seven primary views | Same as BRD §3 |
| §4 | Authority and data protection | Same as BRD §2 |
| §5 | Engineering contracts | API semantics, DB conventions, outbox, RLS |
| §6 | Workflow register (§6.1–§6.66 module functional specs) | Per module: UI, Django design, admin, entities, API, trigger, tools, licence/cost |
| §7 | Business-specific acquisition and commercial conversion | Same as BRD §4 |
| §8 | Website and confidential Admin operating contract (§8.1 Publication lifecycle) | Publication state machine, external-user behaviour |
| §9 | Provider-independent functions and testable behaviour | Adapter contract, fallback rule, configurable state machines |
| §10 | Functional readiness and exception paths | Mandatory path coverage per function |
| §11 | Implementation, verification and delivery controls (§11.1 Functional behaviour standards; §11.2 Evidence record) | SM-FR-W01…A108 and OP001–OP003 (141 FRs) |
| §12 | Functional decision matrix and fail-closed behaviour (§12.1 Business transitions; §12.2 Global UI states) | Worked examples |
| §13 | Optimization engineering and acceptance (§13.1 Security … §13.6 UI/UX) | OPT-01/04/07/10/11/15 items |
| §14 | Implementation acceptance and verification | 5 procedures |
| §15 | Implementation acceptance and final decision controls | Repeat of §14 plus boundary conditions |
| §16 | Current multi-startup, omnichannel and automation scope (§16.1 Functional behaviour; §16.2 Screen-specific field and automation decisions W01–A113; §16.3 Applicant draft boundary) | 147 screen field/automation specs |

---

## 0.2 Summary of understanding (under 400 words)

The **AI Growth Engine – Employee Sales & Marketing Automation** is an **independently deployed, multi-tenant, configuration-driven commercial growth platform** (BRD §1). Employees use it to run market intelligence, content and campaigns, outreach, enquiries, project bids, quotes, buy/sell orders, agreements, onboarding, fulfilment and renewals. **Fundraising and investor activity are explicitly excluded.** Those belong to a separate investor application that shares SSO but not product access or data.

The platform serves **25+ owned startups** and **independently onboarded third-party SaaS tenants**. A *tenant* is the security and billing boundary; a *startup* is a legal-entity workspace. The four seed startups have different commercial routes (BRD §1.1, §4):
- **AppNAI**: global RFP and bid pipeline.
- **MedMaarg**: institutional wellness pilots, with no patient data.
- **EduVerse**: student and institutional education, with child-safety constraints.
- **OrganicSpec**: agri buy/sell, RFQ, orders and payables/receivables.

There are **two React frontends**: a public Website and external Portal (34 interfaces), and a confidential Admin "Command Centre" (113 interfaces, seven primary views). They sit over a **Django REST modular monolith** with PostgreSQL (RLS, optionally pgvector), Celery/Beat, Valkey, and object storage. Integrations go through typed provider adapters (BRD §1.2, FRD §5, §9).

The governing design principles are:
- Rules-first, fail-closed and evidence-based.
- Every externally consequential action passes scope, permission, consent/eligibility, budget reservation, approved content hash and idempotent outbox checks, which are **rechecked at dispatch** (BRD §5).
- AI drafts, classifies, extracts and matches. It never signs, transfers money, makes binding offers or treats a forecast as revenue.
- Automation runs under four autonomy modes (Manual, Assisted, Supervised, Controlled Autonomous) with simulation, an emergency stop, and human escalation for claims, pricing exceptions, contracts, complaints and clinical or minor-related cases.

**Scope inventory.** The BRD contains 66 module requirements (M01–M66) and five cross-cutting outcomes (B-TENANT, B-WEB, B-AUTO, B-SVC, B-QA). The FRD derives 141 functional requirements and 147 screen-level field and automation specifications. The documents *claim* a retained baseline of 302 API operations, 149 entities and 624 tests, plus 19, 6 and 175 candidates. **Those catalogues are not included.**

**Economics.** Engineering effort is 287–483 person-days (₹13.05–32.93 lakh). The pilot run cost is ₹16,675–31,165/month including contingency. The production AI inference reserve is only **₹3,000/month**, which is a decisive constraint for Part 7. The delivery horizon is a 90-day foundation, a 180-day rollout and selective expansion up to day 365, with a lean team of about 3 FTE.

**Success** is measured by verified business outcomes, not AI activity: qualified opportunities, meetings, awarded bids, fulfilled orders, reconciled receipts, renewals and margin (BRD §12.1, §13.1).

---

## 0.3 Requirements inventory

### 0.3.1 Headline counts

| Category | Count found | Where | Blueprint ID scheme |
|---|---|---|---|
| **Primary business requirements**: module register | **66** (M01–M66, contiguous, none missing) | BRD §7, §12 | `BR-M01` … `BR-M66` (original IDs preserved per BRD §12) |
| **Primary business requirements**: cross-cutting | **5** (B-TENANT, B-WEB, B-AUTO, B-SVC, B-QA) | BRD §12 | `BR-TENANT`, `BR-WEB`, `BR-AUTO`, `BR-SVC`, `BR-QA` |
| **Total primary BRs** | **71** | | |
| Supplementary business statements (rules, outcomes, gates, policies) | **118** (detailed in 0.3.2) | BRD §1–§17 | `BR-S001` … `BR-S118` (assigned in Part 1) |
| **Functional requirements**: interface FRs (SM-FR) | **138** (W01–W30, A001–A108) | FRD §11 | `FR-W01` … `FR-A108` (alias of SM-FR) |
| **Functional requirements**: non-screen operations | **3** (OP001 AI run, OP002 health, OP003 ready) | FRD §11 | `FR-OP001`–`FR-OP003` |
| **Functional requirements**: new interfaces with no SM-FR row | **9** (W31–W34, A109–A113) | FRD §16.1, §16.2 | `FR-W31`…`FR-W34`, `FR-A109`…`FR-A113` (created per [RECOMMENDATION-014]) |
| **Total interface/operation FRs** | **150** | | |
| Screen-level field and automation specs (SM-UX-FR) | **147** (34 Website + 113 Admin) | FRD §16.2 | `FR-UX-W01` … `FR-UX-A113` |
| Module functional specs (UI / backend / admin / entities / API / trigger / tools) | **66** | FRD §6.1–§6.66 | Linked to BR-Mxx |
| Global filter families | **11** | FRD §2 | `FR-FLT-01`…`11` |
| Functional behaviour standards / decision matrix / UI states | **4 / 4 / 4** | FRD §11.1, §12.1, §12.2 | `FR-STD-01..04`, `FR-DM-01..04`, `FR-UIS-01..04` |
| Publication lifecycle and engineering-contract statements | **2** | FRD §5, §8.1 | `FR-ENG-01`, `FR-PUB-01` |
| FRD optimization items (OPT) | **13** (OPT-01-01; 04-01…04-08; 07-01; 10-01; 11-01; 15-01) | FRD §13 | Kept as OPT IDs; mapped to NFR/FR |
| **Explicitly labelled NFRs** | **0** | none | |
| **Implicit NFR statements extracted** | **38** (0.3.3) | BRD/FRD passim | `NFR-001` … `NFR-038` |
| Interfaces (screens) | **147** = 34 Website (W01–W34) + 113 Admin (A001–A113) | BRD §9, FRD §16.2 | Kept |
| Workflows | **14** | BRD §5 / FRD §6 | `WF-01` … `WF-14` |
| Logical entities: claimed | 149 retained + 6 candidate = **155** | BRD §9 | |
| Logical entities: actually named in the documents | **132** distinct | FRD §6.x | Others marked [GAP-002] |
| API operations: claimed | 302 retained + 19 candidate = **321** | BRD §9 | |
| API operations: actually named | **102** distinct (FRD §6) + 3 (OP) = **105** | FRD §6, §11 | Others marked [GAP-001] |
| Tests: claimed | 624 retained + 175 candidate = **799** | BRD §9 | |
| Test IDs referenced but undefined | 63 SM-UT IDs (SM-UT-001…066), 138 SM-UAT-S IDs, 147 SM-UX-UAT IDs | FRD §11, §16.2 | [GAP-003]; Part 6 will define test cases |
| Actors / roles | **7** | BRD §2, FRD §4 | Personas in Part 2 |
| Seed startups (legal entities) | **4** | BRD §1.1 | Tenancy config fixtures |
| Cost lines (monthly) | **10** + contingency rate | BRD §6 | FinOps baseline |
| Effort work packages | **4** (+ total) | BRD §6 | Part 8 estimation basis |

**Consistency checks I ran on the numbers in the source:**

| Check | Formula | Result |
|---|---|---|
| Interface count | 34 + 113 | 147 ✔ (BRD §9, §17; FRD §8) |
| Original + new interfaces | 138 + 9 | 147 ✔ |
| Effort total (low) | 194 + 35 + 30 + 28 | 287 ✔ |
| Effort total (high) | 323 + 60 + 52 + 48 | 483 ✔ |
| Engineering value (low) | 287 pd ÷ 22 × ₹1.0 L | ₹13.05 L ✔ |
| Engineering value (high) | 483 pd ÷ 22 × ₹1.5 L | ₹32.93 L ✔ |
| Pilot base run cost | 5,000 + 3,000 + 1,500 + 1,000 + 500 + 2,000 + 500 + 1,000 | ₹14,500 ✔ |
| Base with contingency | 14,500 × 1.15 | ₹16,675 ✔ |
| Full with Apollo and seats | (14,500 + 9,000 + 3,600) × 1.15 | ₹31,165 ✔ |
| Developer seats | 2 × $20 × ₹90 | ₹3,600 ✔ |
| Scoring weights | 25 + 25 + 20 + 15 + 15 | 100 ✔ |
| Quote example (FRD §12.1) | 2 × 150.00 × (1 − 0.10) | 270.00 INR ✔ |

### 0.3.2 Supplementary business statements (118)

| Group | Count | Source | Examples |
|---|---|---|---|
| Vertical operating sequences | 4 | BRD §4 | AppNAI RFP→bid/no-bid→…→verified payment |
| Source scoring and KPI rule | 1 | BRD §4 | 25/25/20/15/15 weights; ≥75/50–74/<50 thresholds |
| Workflow register | 14 | BRD §5 | Startup catalogue … Suspend/offboard |
| Actor authority rules | 7 | BRD §2 | Finance/legal maker-checker; no autonomous transfer |
| Command Centre views | 7 | BRD §3 | Overview, Discovery, Outreach & Marketing, Follow-ups, Objections, Closure, Automation |
| Vertical acceptance statements | 5 | BRD §11 | "No submission without mandatory checks" |
| Business success controls | 5 | BRD §12.1 | Qualified opportunity, conversion outcome, global coverage, service economics, delivery exit |
| Measurable outcome definitions | 4 | BRD §13.1 | Qualified lead, won deal, receipts, acquisition conversion |
| Activation boundaries | 3 | BRD §13.2 | Owned portfolio, external clients, uncertain opportunity |
| BRD OPT items | 10 | BRD §14 | OPT-03-01, 04-01, 12-01…04, 20-01…04 |
| Acceptance procedures (unique) | 5 | BRD §15/§16 | Synthetic 26th startup; scope separation; qualification; closure/receipt; sensitive data |
| Strategy and operating statements | 13 | BRD §8 | Core product, traction, GTM, insurance boundary, build/buy, automation definition |
| Phase gates (Day 1–365) | 7 | BRD §8 | Day 1–15 foundation … Day 181–365 expansion |
| Budget, volume and scale-gate statements | 5 | BRD §8 | Pilot volumes: 500 fetches, 100 signals, 20 accounts, 5 demos |
| Monthly cost lines | 11 | BRD §6 | AWS ₹5,000; AI ₹3,000; … contingency 15% |
| Effort work packages | 4 | BRD §6 | 66 modules 194–323 pd |
| Website surface rules | 4 | BRD §9 | Public, Portal, Admin, Internal/callback |
| New interface definitions | 9 | BRD §17 | W31–W34, A109–A113 |
| **Total** | **118** | | Many overlap with the M-register. Overlaps are merged in Part 1 and every one stays traceable. |

### 0.3.3 Implicit NFRs extracted (38)

The documents have no NFR section. The statements below are non-functional in nature. I have extracted them verbatim or near-verbatim and given them provisional IDs. Measurable targets that are missing are flagged; Part 4 proposes targets as [RECOMMENDATION].

| ID | NFR statement (from source) | Category | Source | Measurable in source? |
|---|---|---|---|---|
| NFR-001 | Separate origins, sessions, OAuth clients/audiences, route allowlists, build artefacts; no Admin JS/routes/private data in public bundles | Security / architecture | BRD §1, FRD §1 | Yes (binary) |
| NFR-002 | Server-side permission on every object, nested FK, search, vector retrieval, export, notification, worker, webhook; claims from current membership | Security | BRD §2, FRD §4 | Yes (binary) |
| NFR-003 | MFA for privileged roles; revoked/wrong-audience requests = 0 successes | Security | FRD §13.1 OPT-01-01 | Yes |
| NFR-004 | Secrets never returned in any API response | Security | BRD §7 M05 | Yes |
| NFR-005 | Duplicate delivery has exactly one effect; replay produces no duplicate message, revenue or publication | Reliability / integrity | M06, M26, M35, M47 | Yes |
| NFR-006 | Transactional outbox; authoritative state and outbox written atomically; row locks | Reliability | FRD §5 | Yes (binary) |
| NFR-007 | Provider outage does not lose events | Reliability | M58 | Yes (binary) |
| NFR-008 | Customer 360 updates visible within 60 s | Performance (freshness) | M23 | Yes (60 s) |
| NFR-009 | Workflow completion ≥ 99% of eligible due runs within the agreed window | Reliability | FRD OPT-04-07 | Partly (window undefined → GAP-018) |
| NFR-010 | ≥ 90% of eligible steps automated, no bypass of mandatory approval | Automation efficiency | FRD OPT-04-08 | Yes |
| NFR-011 | Buying-signal precision ≥ 80% (pilot) / qualification precision ≥ 90% (benchmark) | AI quality | M14; FRD OPT-04-02 | Yes, but conflicting (CONFLICT-001) |
| NFR-012 | Restore drill, secret scan and smoke test pass per release | DevSecOps | M09 | Yes (binary) |
| NFR-013 | All critical tests pass and rollback verified before production | Release | M62, B-QA | Yes (binary) |
| NFR-014 | Cost cap enforced before every paid call; a simulated cap stops requests | FinOps | M08, M53 | Yes |
| NFR-015 | REST/JSON/HTTPS; typed I/O; allowlisted filters; cursor pagination; request ID; version; idempotency key + body hash; defined status codes 200/201/202/400/401/403/404/409/429/503 | Interoperability | FRD §5 | Yes |
| NFR-016 | Exponential backoff with jitter, capped retries, exception queue | Reliability | FRD §5 | Partly (caps undefined) |
| NFR-017 | UUID PKs, UTC timestamps, Decimal amounts + ISO 4217 currency, composite tenant/startup FKs, RLS, revisions | Data integrity | FRD §5 | Yes |
| NFR-018 | Approval, financial and audit records are immutable (append-only) | Auditability | FRD §5, BRD §5 | Yes |
| NFR-019 | `/health` (no DB) and `/ready` endpoints without sensitive detail | Operability | FRD §11 OP002/003 | Yes |
| NFR-020 | Unknown host → 404; atomic publish pointer swap; tenant-keyed cache invalidation; portal content never in public CDN | Security / performance | FRD §8 | Yes |
| NFR-021 | Uploaded files scanned before use; separate approval for public assets | Security | FRD §8, W15, W27, A006 | Yes (binary) |
| NFR-022 | Abuse controls and rate limits on public intake and chat | Security / availability | SM-FR-W01–W30, W11 | No thresholds (GAP) |
| NFR-023 | Accessibility preferences, accessibility needs, accessibility result on page approval | Accessibility | W01, W19, A057 | No standard named → [RECOMMENDATION-001] WCAG 2.2 AA |
| NFR-024 | Language, locale fallback, timezone, currency handled per scope | Localization | FRD §2, W08, A107 | Locales undefined (GAP-012) |
| NFR-025 | Stale revision → 409; never silently overwrite approved state | Integrity | FRD §5, §11.1 | Yes |
| NFR-026 | Provider timeout after submission = "uncertain"; reconcile before replay | Reliability | FRD §11.1, §12.2 | Yes (binary) |
| NFR-027 | Scope switch cancels stale queries, clears cache and selections | Usability / security | FRD §2, §11.1, §12.2 | Yes (binary) |
| NFR-028 | 100% of actionable records have permitted provenance; missing rights quarantined | Data quality / compliance | FRD OPT-11-01 | Yes |
| NFR-029 | Modular monolith; each runtime dependency justified by ADR; no per-startup workflow framework | Maintainability | FRD OPT-07-01 | Yes (binary) |
| NFR-030 | Rules-first model routing; compare quality, latency and INR per task on the same dataset | Cost / AI | FRD OPT-10-01 | Partly |
| NFR-031 | Independent DB, object storage, vector index, queues, credentials, budget, billing, audit, backup per product | Portability / isolation | BRD §1 | Yes (binary) |
| NFR-032 | Two-tenant fixture: zero cross-scope disclosure or side effects | Security / multi-tenancy | B-TENANT, FRD §15 | Yes |
| NFR-033 | AI regression failures block deployment | AI quality / release | M54 | Yes (binary) |
| NFR-034 | Users locate the approved operation and complete core scenarios; clicks and time measured against baseline | Usability | FRD OPT-15-01 | Baseline undefined |
| NFR-035 | 100% attributable usage reconciled to charges | FinOps / billing | BRD OPT-20-02, B-SVC | Yes |
| NFR-036 | Deletion or correction honoured; deletion does not re-enable outreach; legal hold respected | Privacy | M56, W29 | Retention periods undefined (GAP-014) |
| NFR-037 | Open-source-first; zero unapproved paid calls; paid fallback disabled by default | Cost governance | BRD §10, OPT-03-01, FRD §9 | Yes |
| NFR-038 | Simulation or dry run has zero live effects | Safety | BRD §1.2, FRD §9 | Yes (binary) |

**Absent categories (no statement at all):** availability SLO, p95 latency, throughput and concurrency, RTO/RPO, data volumes and growth, browser/device support, portability across clouds, log retention. See GAP-004. Proposed targets will be tagged [RECOMMENDATION] in Part 4.

---

## 0.4 Gaps register (GAP-###): missing information

| ID | Gap | Source context | Impact | Severity | Handling / proposed default | OQ |
|---|---|---|---|---|---|---|
| GAP-001 | API catalogue of 302 retained + 19 candidate operations is not attached; only 105 operations are named | BRD §9; FRD §6, §11 | API design completeness, contract tests | High | Part 3 derives a complete API catalogue from the 147 screens + 66 module specs, tagged *DERIVED*; reconcile when the source catalogue arrives | OQ-013 |
| GAP-002 | Entity catalogue of 149 + 6 is not attached; 132 named. Core entities are unnamed: Tenant, Startup, BusinessLine, Offering/SKU, PublicationSnapshot, Domain, Bid/Tender, Order, OrderLine, FulfillmentEvent, Plan, Entitlement, ServiceInvoice, UsageMeter, Trigger, NodeTemplate, ConfigRevision, ApplicationDraft, ConflictCase | BRD §9; FRD §6, §16.2–§16.3 | Data model | High | Part 3 adds the missing entities as *DERIVED* | OQ-013 |
| GAP-003 | Test catalogue (624 + 175) is not attached. SM-UT-001…066, SM-UAT-S001…, SM-UX-UAT-* are referenced but not defined | FRD §11, §16.2 | QA traceability | High | Part 6 defines test cases and maps the referenced IDs as aliases | OQ-013 |
| GAP-004 | No explicit NFR targets: availability, latency, throughput, concurrency, RTO/RPO, volume growth, browser support | none | Architecture sizing, SLOs | High | [RECOMMENDATION-002] targets in Part 4 | OQ-011 |
| GAP-005 | Identity dependencies "H02, H03" undefined; the existing auth technology (session vs OIDC provider, MFA method) is unknown | BRD §7 M01 | Sprint 1 auth integration | High (Sprint 1) | Sprint 0 spike; assume Django + OIDC-capable ([ASSUMPTION-013]) | OQ-003 |
| GAP-006 | Budget IDs B01–B22 and engineering ID C03 are referenced, but the cost table rows carry no IDs; "11 Budget" section is not present | BRD §6, §8; FRD §6 | FinOps traceability | Medium | Assign B01–B10 to the 10 cost lines in table order, B11 = contingency; B12–B22 undefined | OQ-024 |
| GAP-007 | Referenced artefacts not attached: MedMaarg investor/business deck (slides 2–17), integration workbook (rows 4–541, 538 candidates), HTML prototypes, "20 role perspectives" checklist, sibling investor-application spec | BRD §8, §17 | Claims, integrations, UI | Medium | Proceed without; MedMaarg claims must come from the approved catalogue (M02) | OQ-013 |
| GAP-008 | Payment provider unnamed ("existing payment provider subject to API") | FRD §6 M47 | Closure, reconciliation | Medium (Day 91+) | Generic payment adapter; Indian hosted-checkout gateway assumed ([ASSUMPTION-015]) | OQ-004 |
| GAP-009 | E-signature provider unnamed | FRD §6 M46 | Contracts | Medium | Generic e-sign adapter; verify Indian IT Act e-sign validity | OQ-005 |
| GAP-010 | Calendar provider unnamed | FRD §6 M29 | Meetings | Low | Google Workspace first, Microsoft 365 second | OQ-006 |
| GAP-011 | Email provider undecided (Resend vs Amazon SES); budget assumes SES | FRD §6 M26, A036; BRD §6 | Messaging | Low | Amazon SES | OQ-007 |
| GAP-012 | Supported languages and locales not listed | FRD §2, W01, W08 | i18n | Medium | English at launch; i18n-ready; Hindi/Tamil/Odia candidates | OQ-008 |
| GAP-013 | Tax rules (GST, cross-border), rounding rule, FX rate source not specified | A067, A074, A101, W06 | Quote and invoice accuracy | High (closure) | Tax profile per startup; banker's vs half-up rounding to be decided; FX snapshot with source and date | OQ-025 |
| GAP-014 | Retention periods per data class not specified | M56, A013, A103 | Privacy, storage cost | High | Proposed schedule in Part 3 ([ASSUMPTION-018]), legal confirmation required | OQ-012 |
| GAP-015 | Regulations outside India not addressed although AppNAI is worldwide (GDPR/UK GDPR/PECR, CAN-SPAM, CASL, etc.) | BRD §1.1, §8 | Outreach legality | High | Jurisdiction rules in the eligibility engine; default-deny for unknown jurisdictions | OQ-010 |
| GAP-016 | Mechanism for verifiable guardian consent (children) not specified | W17, EduVerse rows | Legal exposure (DPDP) | High | Guardian/institution-mediated intake only; no direct child outreach | OQ-026 |
| GAP-017 | Number of internal users, portal users and growth trajectory unknown | none | Capacity, licence, cost | Medium | [ASSUMPTION-002] | OQ-027 |
| GAP-018 | "Agreed window" for the 99% workflow-completion target undefined | FRD OPT-04-07 | SLO | Medium | 15 min for transactional, 24 h for scheduled discovery | OQ-011 |
| GAP-019 | The 9 new interfaces have SM-UX-FR rows but no SM-FR rows | FRD §11 vs §16 | Traceability | Low | Create FR-W31…FR-A113 ([RECOMMENDATION-014]) | none |
| GAP-020 | Phase gates cite M-ranges ("M01–M09", "M10–M20" …), but IDs are not sequential in the register (M53, M56, M58 sit in the foundation block; M55 in the CRM block; M41 in omnichannel) | BRD §8, §12 | Sprint and phase mapping | Medium | Map by register position (dependency order), not numeric range | OQ-028 |
| GAP-021 | "Approved Copilot" is mentioned with no functional spec, screen or limits | BRD §3, FRD §3 | AI scope | Medium | Admin Copilot = read-only, grounded Q&A + draft (L0/L1) | OQ-018 |
| GAP-022 | Internal notification channels (in-app, email, push, chat) and digest rules unspecified | A106 | UX | Low | In-app + email digest | OQ-029 |
| GAP-023 | Global search across records is not specified beyond filters and knowledge search | FRD §2, M03 | UX | Low | PostgreSQL full-text, scope-filtered ([RECOMMENDATION-009]) | none |
| GAP-024 | Approval thresholds not quantified (discount %, margin floor, amount bands needing finance/legal, autonomy limits) | A068, A070, A072 | Workflow rules | High | Configurable policy with conservative defaults (any discount → approval) | OQ-014 |
| GAP-025 | No data migration source described (existing CRM, spreadsheets, contact lists) | BRD §1 founder snapshot; A103 | Migration plan | Medium | CSV/JSON import via A103 with validation and consent evidence | OQ-021 |
| GAP-026 | Hosting region, HA tier and DR design unspecified ("validate region/HA needs") | BRD §6 | Architecture, cost | Medium | AWS ap-south-1, single-region Multi-AZ DB; cross-region backups | OQ-016 |
| GAP-027 | Monitoring stack only "CloudWatch/Sentry candidates"; no SLOs or alert thresholds | FRD §6 M58 | Operability | Medium | Part 4 defines it | OQ-011 |
| GAP-028 | Model names and prices quoted in the FRD (Claude Haiku 5.5 $0.10/$0.50, Sonnet 5.5 $2/$10 per MTok) are time-sensitive and unverified | FRD §6.2 | AI cost model | Medium | Flagged "verify at time of implementation, as of 27 Nov 2026" | OQ-009 |
| GAP-029 | Device/channel support not stated (mobile web? native apps?) | none | UX, testing | Low | Responsive web only ([ASSUMPTION-014]) | none |
| GAP-030 | Support model and SLAs for SaaS clients undefined ("no unverified SLA promise") | BRD OPT-20-03 | Service operations | Medium | Business-hours support, best-effort, no contractual SLA in pilot | OQ-022 |
| GAP-031 | OrganicSpec inventory/stock reservation is referenced, but no inventory model or rules exist | A105 | Orders | Medium | Availability flag + optional reservation, no full WMS | OQ-020 |
| GAP-032 | Referral commission referenced ("Commission approval") without commission rules | A064 | Partner payouts | Low | Record only; payouts manual and out of scope | OQ-019 |
| GAP-033 | SaaS plan catalogue (plans, quotas, prices for W31/A101) not provided | W31, A101, B-SVC | Billing | Medium | Configurable plan entity; no default prices published | OQ-022 |
| GAP-034 | Admin "Copilot" and agent permissions to call internal tools are not enumerated (tool registry) | BRD §3; FRD §9 | AI safety | Medium | Part 7 defines the tool registry | none |

---

## 0.5 Conflicts register (CONFLICT-###): where documents or sections contradict

| ID | Conflict | Sources | Resolution proposed (default) | Owner | OQ |
|---|---|---|---|---|---|
| CONFLICT-001 | Precision target: "≥80% precision on reviewed pilot sample" vs "Precision ≥90% on approved benchmark" | BRD M14, §8 Day 16–30 vs FRD OPT-04-02 | Two-stage gate: ≥80% to exit the Day 16–30 pilot (signal classification); ≥90% on the approved benchmark before any qualification step runs at Supervised/Controlled-Autonomous level | Product Owner / AI lead | OQ-001 |
| CONFLICT-002 | Fundraising is excluded, yet fundraising/investor wording remains: "customize offerings or funding goals", "Offerings or fundraising thesis" (W33), "offering/issuer thesis", "investment/delivery geography" (filters), "verified funding" (OPT-12-03), "Investor app only fundraising" | BRD §1 vs BRD §15, FRD §2, §16.2 W33, BRD §14 | Treat all as legacy text from the sibling investor product. Replace with "commercial objective", "delivery geography", "commercial receipt". Keep one negative test proving no fundraising capability exists | Founder / PO | OQ-002 |
| CONFLICT-003 | "M01 Identity: already developed in AppNAI" and "M02 Approved AppNAI product truth" vs an independent, multi-startup product | BRD §12 vs BRD §1, §7 | Reuse the AppNAI auth *code/library* under a new product audience (no shared product access). M02 becomes a per-startup catalogue (AppNAI is one tenant workspace) | CTO | OQ-003 |
| CONFLICT-004 | Pilot base run cost ₹14,500 (table) vs "base runtime ₹15,000 before contingency" vs illustrative ₹15–60k | BRD §6 vs §8 | Use the table: ₹14,500 base, ₹16,675 with contingency, ₹31,165 with Apollo + seats. Treat ₹15,000 as rounding | Finance | OQ-024 |
| CONFLICT-005 | Effort 287–483 person-days with ~3 FTE (≈ 66 pd/month) gives ≈ 4.3–7.3 months, vs a 90-day foundation and 180-day rollout. Also "₹9–13.5L / 3 months" covers only ≈ 198 pd | BRD §6 vs §8 | High end overruns 180 days by ≈ 1.3 months. Options in Part 8: add 1 FTE, defer Day 181–365 items, or accept a 7–8 month rollout | Founder / CTO | OQ-015 |
| CONFLICT-006 | "One consolidated dependency-ordered plan; no separate product release labels" vs this blueprint's required Release 1 / 2 / Future and MoSCoW | BRD §1.2 vs prompt §6.1, §7.1 | Use **delivery waves** keyed to the source's day-phases (W0 Day 1–15 … W6 Day 181–365). "Release 1" = Waves 0–3 (Day 1–90), "Release 2" = Waves 4–5 (Day 91–180), "Future" = Wave 6+. Labels are for planning only, not product versions | PO | OQ-030 |
| CONFLICT-007 | AI provider: "Claude/OpenAI API", "low-cost model routing", "rules → small model → advanced only when required" vs this prompt's "Claude Sonnet primary + free-tier fallback chain" | FRD §6.8, OPT-10-01, BRD §6 vs prompt §7.3 | Tier 0 rules/cache → Tier 1 Claude Sonnet for complex/high-stakes → [RECOMMENDATION-003] lighter Claude tier for simple high-volume tasks → Tier 2 free fallbacks for Public/Internal-non-personal data only → Tier 3 degrade. Paid non-Anthropic fallbacks stay disabled by default (BRD §10) | AI lead | OQ-017 |
| CONFLICT-008 | AI budget: ₹3,000/month production inference reserve vs Sonnet-primary across many agents and discovery volumes | BRD §6 vs prompt §7.3 | Part 7 sizes token budgets to fit ₹3,000 at base pilot volume through caching, batching and rules-first design. Shows the low/base/high scenario and the ceiling needed per scale gate | Founder / FinOps | OQ-009 |
| CONFLICT-009 | "React operator workspace and separate React admin workspace … shared PostgreSQL" vs "two frontends: commercial-website-react and commercial-admin-react" and "independent PostgreSQL per product"; also "Automation: connected separate admin workspace" | BRD §8 Scope vs BRD §1, FRD §5 | The current text governs: **two** frontends. "Operator workspace" = Admin app; the "Automation" view is a separately permissioned route group of the Admin app. "Shared PostgreSQL" = one DB *shared across tenants of this product* with RLS, independent of the investor product | Solutions Architect | OQ-023 |
| CONFLICT-010 | A104 (bid desk) and A105 (order/fulfilment desk) map only to B-TENANT, but they implement the Project-bid and Order/fulfilment workflows and depend on M43/M44/M46/M47 | FRD §11 vs BRD §5 | Add trace links: A104 → BR-TENANT, WF-08, BR-M43, BR-M44, BR-M46; A105 → BR-TENANT, WF-10, BR-M44, BR-M47 | BSA | none |
| CONFLICT-011 | Scoring components are "normalized 0–1", but thresholds are "≥75 / 50–74 / <50" | BRD §4 | Score = 100 × Σ(wᵢ × cᵢ), where wᵢ ∈ {0.25, 0.25, 0.20, 0.15, 0.15} ([ASSUMPTION-009]). Unknown components excluded and flagged, never zero-filled | BSA | none |
| CONFLICT-012 | The engineering estimate is said to be "superseded", yet the "original estimate retained: ₹9–13.5L/3 months; ₹18–27L/6 months" | BRD §8 | Use the person-day estimate (₹13.05–32.93 L) as the planning basis; the historical estimate is reference only | Finance | none |
| CONFLICT-013 | "MVP growth dashboard" (M30 label in BRD §12) vs "no separate product release labels" | BRD §12 vs §1.2 | Drop "MVP" as a label; M30 is delivered in Wave 2 | PO | none |
| CONFLICT-014 | BRD §15 and §16 (and FRD §14/§15) repeat the same acceptance procedures with slightly different wording | BRD §15/§16; FRD §14/§15 | Merge into one acceptance register; the union of wording applies ([RECOMMENDATION-013]) | QA lead | none |

---

## 0.6 Ambiguities (to resolve via assumptions or questions)

| # | Ambiguity | Source | Interpretation adopted |
|---|---|---|---|
| AMB-1 | "Copilot" capabilities and allowed actions | BRD §3 | See GAP-021: read-only, grounded, drafts only |
| AMB-2 | "Outcome certainty" values in A110 | FRD §16.2 A110 | Enum: confirmed / uncertain / failed / reconciled |
| AMB-3 | "Workflow builder" is a graph editor (A033 "Edit graph") but "no arbitrary code" (A113) | FRD §16.2 | Declarative node graph from an approved node library; no scripting nodes |
| AMB-4 | "Startup position-based restrictions removed" (A104) / "fixed startup restriction removed" (A105) | FRD §16.2 | Bid and order capabilities are granted by capability profile, not hard-coded to AppNAI/OrganicSpec. Owned-portfolio routing still defaults external AI projects → AppNAI |
| AMB-5 | Is "tender submission" ever automated? | BRD §5 WF-08 | No. Submission is human-performed or human-approved (L1 maximum). The system records evidence of submission |
| AMB-6 | "Closure" criteria differ by route (signed contract vs verified payment) | FRD §6 M47 | Closure policy configured per opportunity type; both criteria available |
| AMB-7 | "Owner group view is read-only for business mutations" | BRD §1 | Portfolio aggregate views never expose mutation actions. Mutations require selecting exactly one startup |
| AMB-8 | "Support access client-approved, time-limited" | BRD §1 | Break-glass grant entity with scope, expiry and approver, audited |
| AMB-9 | "Founder-authorized nonconfidential business-fact snapshot import" | BRD §1 | One-way file import into the catalogue (A103), no live link |
| AMB-10 | "Investor app" existence and SSO | BRD §1, §15 | Separate product; shared IdP; distinct token audience; no data exchange |

---

## 0.7 Assumptions register (ASSUMPTION-###)

| ID | Assumption | Basis | Validate by | Risk if wrong |
|---|---|---|---|---|
| ASSUMPTION-000 | Section numbering convention per 0.1.2 | No numbering in source | N/A | Citation confusion |
| ASSUMPTION-001 | **Industry/domain:** multi-vertical B2B/B2C commercial growth SaaS covering AI services, wellness-tech partnerships, ed-tech and agri-commerce; the product itself is vertical-agnostic via templates | BRD §1, §1.1 | PO sign-off | Low |
| ASSUMPTION-002 | **Scale (planning):** Year 1 has 25–40 startup workspaces, 2–10 external tenants, 15–60 internal users, ≤ 500 portal users/month, ≤ 5,000 public sessions/month. Pilot volumes from BRD §8 (500 fetches, 100 reviewed signals, 2,000 emails, 1,000 WhatsApp templates/month). Capacity is designed for 10× pilot volume without re-architecture | BRD §8; [RECOMMENDATION] | OQ-027 | Under/over-provisioning |
| ASSUMPTION-003 | **Geography and regulation:** India primary (Odisha, Tamil Nadu), with worldwide outreach for AppNAI. Applicable: India DPDP Act 2023 + DPDP Rules (verify notified commencement dates as of implementation); IT Act 2000; TRAI TCCCPR 2018 for commercial SMS/voice (verify applicability to WhatsApp/email); Meta WhatsApp Business policies; GDPR/UK GDPR + PECR for EU/UK recipients; CAN-SPAM for US recipients; CASL for Canada. SOC 2-*aligned* controls without certification. HIPAA not applicable (no PHI by design). PCI DSS scope minimized via hosted payment pages | BRD §8 sources (DPDP, TRAI) + worldwide scope | OQ-010, legal review | High: outreach legality |
| ASSUMPTION-004 | **Cloud:** AWS, region ap-south-1 (Mumbai) primary; backups copied to a second Indian region (ap-south-2 Hyderabad, verify service availability) | BRD §6 "AWS shared hosting" | OQ-016 | Cost/latency |
| ASSUMPTION-005 | **Stack:** React + TypeScript, Django + DRF, PostgreSQL with RLS and pgvector, Celery + Celery Beat, Valkey, S3-compatible object storage, AWS Secrets Manager. Exact versions are "verify at implementation" | BRD §1.2, FRD §6 | Sprint 0 | Low |
| ASSUMPTION-006 | **Team:** 1 backend, 1 frontend, 0.5 QA, 0.5 growth/compliance lead, plus founder/CTO as Product Owner and architect. Scrum, 2-week sprints | BRD §8 Budget assumptions | OQ-015 | Timeline (CONFLICT-005) |
| ASSUMPTION-007 | **Budget:** engineering ₹13.05–32.93 L; monthly run ₹16,675 (base) to ₹31,165 (with Apollo + dev seats); ads, staff and taxes excluded | BRD §6 | Finance | Medium |
| ASSUMPTION-008 | **Monthly AI budget ceiling:** ₹3,000 production inference at pilot base (≈ USD 33 at ₹90/USD; FX to verify). Part 7 also shows the ceiling needed at growth volume | BRD §6 | OQ-009 | High: AI scope |
| ASSUMPTION-009 | Opportunity score = 100 × Σ(weight × normalized component); unknown ≠ 0 | BRD §4 (CONFLICT-011) | BSA review | Low |
| ASSUMPTION-010 | Autonomy mapping: Manual = L0 (suggest only), Assisted = L1 (draft for approval), Supervised = L2 (act with post-review, limited to routine eligible actions), Controlled Autonomous = L3 (act within guardrails). Consequential actions (formal offers, contracts, prices beyond policy, money, submissions) are capped at L1 at every mode | BRD §1.2, FRD §14 | PO | Low |
| ASSUMPTION-011 | English (en-IN) at launch; UI strings externalized; content locale per publication; Hindi, Tamil and Odia candidates for Wave 5+ | BRD §8 GTM | OQ-008 | Low |
| ASSUMPTION-012 | Base currency INR; multi-currency amounts stored as Decimal + ISO 4217; FX snapshot recorded per document; no automatic FX conversion of actuals | FRD §2, §5 | OQ-025 | Medium |
| ASSUMPTION-013 | Existing auth is Django-based and can issue product-audience tokens/sessions (OIDC-compatible) with MFA | BRD M01 | Sprint 0 spike | High for Sprint 1 |
| ASSUMPTION-014 | Channels: responsive web (desktop-first Admin, mobile-first Website/Portal) plus REST API for integrations; no native mobile apps | No mobile requirement | PO | Low |
| ASSUMPTION-015 | Payments via a hosted-checkout Indian gateway behind a provider-agnostic adapter; the platform never stores card or bank secrets | FRD M47, W26 "no raw bank secrets" | OQ-004 | Medium |
| ASSUMPTION-016 | Anyone under 18 is a child for DPDP purposes. EduVerse acquisition targets guardians, institutions and adult learners; no profiling or targeted advertising to children | BRD §5, §15 | Legal review OQ-026 | High |
| ASSUMPTION-017 | Data hosted in India by default (not asserted as a legal mandate; verify) | BRD §8 | Legal | Low |
| ASSUMPTION-018 | Provisional retention defaults (legal to confirm): financial/invoice records 8 years (verify Companies Act/GST requirements); contracts life + 8 years; audit log 7 years; marketing contact data 24 months after last eligible interaction; suppression list indefinitely (minimal hash); research evidence 12 months; AI run logs (redacted) 90 days; chat transcripts 90 days | No source periods | OQ-012 | High |
| ASSUMPTION-019 | "Existing login/security reuse" excludes the cost of new MFA/IdP features; any new auth work is a change request | BRD §6 | CTO | Medium |
| ASSUMPTION-020 | Delivery-lifecycle AI tooling (Claude Code seats) is a developer tool, not a runtime entitlement, and is budgeted separately (₹3,600) | BRD §1.2, §6 | N/A | Low |

---

## 0.8 Recommendations register (RECOMMENDATION-###): additions fully aligned with the requirements

You authorized additions that align with the requirements. Each item below fills a gap or strengthens an existing requirement. None changes stated scope.

| ID | Recommendation | Aligns with | Benefit |
|---|---|---|---|
| RECOMMENDATION-001 | Adopt **WCAG 2.2 AA** as the accessibility standard for Website, Portal and Admin; automated axe checks in CI plus manual screen-reader passes | W01, W19, A057 accessibility fields | Compliance, usability |
| RECOMMENDATION-002 | Initial SLOs: Website/Portal availability 99.5% (pilot) → 99.9% (scale gate); Admin 99.5%; p95 API read ≤ 500 ms, write ≤ 800 ms (excluding provider calls); RPO ≤ 15 min (PITR), RTO ≤ 4 h; outbox dispatch lag p95 ≤ 60 s (consistent with NFR-008) | GAP-004, M58, M23 | Testable operability |
| RECOMMENDATION-003 | Allow a lighter Claude tier (e.g. Haiku-class) for high-volume classification/extraction where evals show parity. **Deviates from "Sonnet only"**, consistent with FRD OPT-10-01 | CONFLICT-007/008 | Large cost reduction |
| RECOMMENDATION-004 | Data classification scheme (Public, Internal, Confidential, Restricted). Restricted = personal data, children's data, health-adjacent, financial, credentials. **Restricted data never goes to free-tier models**; redact or block | Prompt §7.3; BRD §2, §15 | Privacy-safe fallback |
| RECOMMENDATION-005 | Feature flags (open-source, e.g. django-waffle or Unleash OSS) for every external channel, autonomy mode and paid adapter; flags default OFF | BRD §10 "disabled by default" | Safe rollout |
| RECOMMENDATION-006 | OpenTelemetry traces/metrics with a correlation ID propagated from HTTP → outbox → Celery → adapter → webhook | FRD §5, M58, A110 | Diagnosability |
| RECOMMENDATION-007 | STRIDE threat model plus DPIAs (Data Protection Impact Assessments) for EduVerse (children) and MedMaarg (health-adjacent) flows before activation | BRD §15 sensitive-data procedure | Compliance |
| RECOMMENDATION-008 | Define the **Admin Copilot** as a read-only, grounded assistant (L0/L1) that answers from scoped records and approved knowledge with citations and can draft but never execute | GAP-021 | Clear AI boundary |
| RECOMMENDATION-009 | Scoped global search (PostgreSQL full-text + trigram) across organizations, contacts, deals, documents, with RLS enforced | GAP-023, NFR-002 | Productivity |
| RECOMMENDATION-010 | Infrastructure as Code (Terraform/OpenTofu) and immutable container images; environments dev → test → staging → prod | M09 reproducible releases | Reproducibility |
| RECOMMENDATION-011 | Consumer-driven / schema contract tests for every provider adapter and webhook, with sandbox fixtures | FRD §9 | Integration safety |
| RECOMMENDATION-012 | A single **Policy Decision Point** service (deterministic) for eligibility, consent, jurisdiction, quiet hours, frequency caps, budget and approval-hash checks, called at plan time *and* at dispatch | BRD §5 engine; M24 | Consistency, testability |
| RECOMMENDATION-013 | Merge duplicated acceptance procedures (BRD §15/§16, FRD §14/§15) into one acceptance register | CONFLICT-014 | Clarity |
| RECOMMENDATION-014 | Create FR-W31…FR-W34 and FR-A109…FR-A113 with full acceptance, matching the SM-FR pattern | GAP-019 | 100% traceability |
| RECOMMENDATION-015 | A **Reconciliation console** pattern (uncertain outcomes queue) shared by email, WhatsApp, social, ads, e-sign, payments | FRD §11.1, §12.2; A110 | No blind retries |
| RECOMMENDATION-016 | A **Jurisdiction rule pack** in the eligibility engine (India DPDP/TRAI, EU GDPR/PECR, US CAN-SPAM, Canada CASL); unknown jurisdiction = deny | GAP-015 | Lawful global outreach |
| RECOMMENDATION-017 | Seed **synthetic data sets** (two tenants, 26 startups, all four verticals, minors and health fixtures) as a versioned test asset | BRD §15, B-TENANT | Repeatable QA |
| RECOMMENDATION-018 | Use the **dual-ledger** pattern: receivables and payables as separate append-only ledgers; deal/closure states derived, never manually set | M47, A105, BRD §13.1 | Financial integrity |

---

## 0.9 Open Questions log (OQ-###)

Rule applied: proceed with the proposed default unless the question is marked **blocking**.

| ID | Question | Owner | Impact | Proposed default | Blocking? | Needed by |
|---|---|---|---|---|---|---|
| OQ-001 | Which precision target governs: 80% or 90%? | PO + AI lead | AI gates, autonomy | Two-stage gate (CONFLICT-001) | No | Wave 2 |
| OQ-002 | Confirm removal of all fundraising/investor wording from this product | Founder | Scope, tests | Remove/replace (CONFLICT-002) | No | Part 1 |
| OQ-003 | What are H02/H03? What is the existing auth (IdP, protocol, MFA, session model)? Can it issue a separate product audience? | CTO | Sprint 1 build | Sprint 0 spike; ASSUMPTION-013 | **Blocking for Sprint 1 auth stories only** (not for blueprint) | Sprint 0 end |
| OQ-004 | Which payment gateway(s)? | Finance | Closure, reconciliation | Hosted-checkout adapter | No | Wave 4 (Day 91) |
| OQ-005 | Which e-signature provider? Legal validity requirements (Aadhaar e-sign vs DSC vs click-wrap)? | Legal | Contracts | Provider-agnostic adapter + manual upload of signed PDF with hash | No | Wave 4 |
| OQ-006 | Calendar providers to support? | Growth lead | Meetings | Google first, Microsoft second | No | Wave 2 |
| OQ-007 | Email provider: SES or Resend? | CTO | Messaging | Amazon SES | No | Wave 2 |
| OQ-008 | Which languages and locales at launch and later? | PO | i18n | en-IN at launch | No | Wave 3 |
| OQ-009 | Confirm the monthly AI inference ceiling (₹3,000) and the ceiling at each scale gate | Founder / FinOps | AI agent catalogue | ₹3,000 base; Part 7 proposes tiers | No | Part 7 |
| OQ-010 | Which non-Indian jurisdictions will be contacted in Year 1? | Legal / Growth | Eligibility rules | India + opt-in-only elsewhere; unknown = deny | No | Wave 2 |
| OQ-011 | Accept the proposed SLOs/RTO/RPO (RECOMMENDATION-002)? | CTO | Architecture, cost | Accept | No | Part 4 |
| OQ-012 | Approve the retention schedule (ASSUMPTION-018) | Legal / DPO | Data lifecycle | Use defaults | No | Wave 1 |
| OQ-013 | Can the API catalogue, entity catalogue, test catalogue, integration workbook, MedMaarg deck and HTML prototypes be provided? | PO | Traceability fidelity | Derive and tag *DERIVED* | No | Part 3 |
| OQ-014 | Discount, margin and amount thresholds for approvals; who approves what? | Finance / Legal | Rules engine | Any discount or non-standard term → approval; finance maker-checker for all invoices | No | Wave 4 |
| OQ-015 | Is 180 days fixed (requires extra capacity), or can rollout extend to 7–8 months? | Founder | Delivery plan | Keep 180 days for Waves 0–5 core; flex scope via MoSCoW | No | Part 8 |
| OQ-016 | Hosting region and HA tier | CTO | Cost, DR | ap-south-1, Multi-AZ DB, single-AZ app at pilot | No | Sprint 0 |
| OQ-017 | Are free-tier fallback models acceptable given data restrictions? | Security / AI lead | Model routing | Only for Public/Internal-non-personal data; per-tenant opt-in; default OFF | No | Part 7 |
| OQ-018 | Copilot scope and permitted tools | PO | AI scope | RECOMMENDATION-008 | No | Part 7 |
| OQ-019 | Referral commission rules and payouts | Finance | Partner module | Record only; payouts out of scope | No | Wave 5 |
| OQ-020 | Depth of OrganicSpec inventory (stock levels, reservations, warehouses?) | OrganicSpec lead | Order module | Availability + reservation only | No | Wave 4 |
| OQ-021 | Is there existing data (contacts, deals, catalogues) to migrate? From which systems? | Growth lead | Migration plan | CSV import with consent evidence | No | Wave 1 |
| OQ-022 | SaaS plans, prices, quotas and support commitments for external tenants | Service owner | B-SVC | Configurable; no public price until approved | No | Wave 5 |
| OQ-023 | Confirm two frontends (Website/Portal, Admin), with Automation as an Admin route group | Solutions Architect | Architecture | Yes (CONFLICT-009) | No | Part 3 |
| OQ-024 | Confirm the budget ID mapping B01–B11 and the meaning of B12–B22 and C03 | Finance | FinOps traceability | GAP-006 mapping | No | Part 7 |
| OQ-025 | Tax (GST) handling, rounding rule and FX source | Finance | Quote/invoice accuracy | Tax profile per startup; ROUND_HALF_UP at line level to 2 dp; FX source recorded | No | Wave 4 |
| OQ-026 | Guardian-consent verification method for EduVerse (DPDP) | Legal / EduVerse lead | Child safety | Institution-mediated or guardian-verified only | No (blocks EduVerse minor journeys only) | Wave 3 |
| OQ-027 | Expected users and tenants for Year 1 and Year 2 | Founder | Capacity, cost | ASSUMPTION-002 | No | Part 3 |
| OQ-028 | Confirm phase-gate mapping by register order rather than numeric M-ranges | PO | Roadmap | Register-order mapping | No | Part 8 |
| OQ-029 | Internal notification channels | PO | UX | In-app + email digest | No | Wave 2 |
| OQ-030 | Accept "delivery waves" in place of product release labels | PO | Roadmap language | Accept (CONFLICT-006) | No | Part 1 |

**Blocking status:** No question blocks writing the blueprint. OQ-003 blocks only the *build* of Sprint 1 authentication stories, and a Sprint 0 spike is planned. OQ-026 blocks only activation of EduVerse journeys involving minors.

---

## 0.10 Preliminary scope structure (for later parts)

### 0.10.1 Workflow IDs (from BRD §5)
WF-01 Startup catalogue · WF-02 Market discovery · WF-03 Professional contacts · WF-04 Inbound acquisition · WF-05 Content/campaign · WF-06 Outreach and replies · WF-07 Follow-up & meetings · WF-08 Project bid · WF-09 Proposal/quote · WF-10 Order/fulfilment · WF-11 Commercial closure · WF-12 Retention & renewal · WF-13 Autonomous plan · WF-14 Suspend/offboard.

### 0.10.2 Preliminary epic map (to be finalized in Parts 1 and 5)

| Epic | Title | Primary BRs | Key screens | Wave |
|---|---|---|---|---|
| EP-01 | Platform foundation, identity reuse and tenancy | M01, M05, M06, M09, B-TENANT | A001–A003, A008, A009, A099 | 0 |
| EP-02 | Product truth and knowledge | M02, M03, M66 | A004–A006, A097, A098 | 0 |
| EP-03 | Consent, privacy, eligibility and compliance | M04, M24, M56, M57 | A007, A013, A047, W29, W30 | 0–3 |
| EP-04 | AI gateway, cost control and AI quality | M08, M53, M54 | A011, A012, A084 | 0 |
| EP-05 | Market intelligence and discovery | M07, M10–M16, M33, M59 | A010, A015–A021, A048, A049, A085, A086 | 1 |
| EP-06 | Opportunity scoring, contacts and research review | M17–M20 | A022–A028 | 1 |
| EP-07 | CRM, lead capture and Customer 360 | M21, M22, M23 | A029–A032, W12–W17 | 2 |
| EP-08 | Messaging: drafting, email, inbound, sequences, omnichannel | M25–M28, M41 | A034–A039, A046 | 2–3 |
| EP-09 | Meetings, webinars and demos | M29, M40 | A040, A041, A062, A063, W18, W19 | 2–3 |
| EP-10 | WhatsApp and website assistant | M31, M32 | A044, A045, W11 | 3 |
| EP-11 | Content, SEO and social publishing | M34, M35, M36 | A050–A055 | 3 |
| EP-12 | Campaigns, landing pages, ads and referrals | M37, M38, M39, M42 | A056–A061, A064, W10, W20 | 3 |
| EP-13 | Proposal, quote, negotiation and contract | M43–M46 | A065–A072, W23, W24 | 4 |
| EP-14 | Bids, orders and fulfilment (vertical routes) | WF-08, WF-10, B-TENANT | A104, A105, W14–W16, W25 | 4 |
| EP-15 | Payment, closure, revenue and attribution | M47, M52 | A073, A074, A082, A083, W26 | 4–5 |
| EP-16 | Onboarding, retention, partners and expansion pilots | M48–M51, M63–M65 | A075–A081, A091–A096, W27, W28 | 4–6 |
| EP-17 | Dashboards, forecast and Command Centre | M30, M60, M61 | A042, A043, A087–A089, A106 | 2–5 |
| EP-18 | Workflow, autonomy and automation engine | M55, B-AUTO | A033, A102, A109–A113 | 0–5 |
| EP-19 | Public website and external portal | B-WEB | W01–W10, W21, W22, A107, A108 | 2–3 |
| EP-20 | SaaS client lifecycle and portability | B-SVC | W31–W34, A100, A101, A103 | 5 |
| EP-21 | Release readiness, QA and observability | M58, M62, B-QA | A014, A090 | 0–5 |

### 0.10.3 Preliminary wave mapping (from BRD §8 phase gates, CONFLICT-006)

| Wave | Days (source) | Source acceptance | Planning label |
|---|---|---|---|
| W0 | 1–15 Foundation | M01–M09 (+ M53, M56, M58 by register order) tested; owner and claims sign-off | Release 1 |
| W1 | 16–30 Intelligence pilot | M10–M20; 100 reviewed signals; precision ≥ 80% | Release 1 |
| W2 | 31–60 Sales foundation | M21–M30 (+ M55); 20 qualified accounts and 5 demo requests (target, not guarantee) | Release 1 |
| W3 | 61–90 Omnichannel | M31–M42 (+ M41, M57); opt-out and replay tests pass | Release 1 |
| W4 | 91–120 Closure | M43–M51; full synthetic deal + one real controlled pilot | Release 2 |
| W5 | 121–180 Optimization | M52–M62; 30-day monitored pilot; budget and compliance gates | Release 2 |
| W6 | 181–365 Selective expansion | M63–M66; validated contract and market-fit milestones | Future |

---

## 0.11 Part plan (N = 11 parts: Part 0 – Part 10)

Large parts are delivered in numbered batches (e.g. 5.1, 5.2). Each response ends with the status line. Every part is saved under `blueprint/` in the repository so the Part 10 assembly uses exactly the reviewed text.

| Part | Title | Contents | Expected batches |
|---|---|---|---|
| **0** | Document ingestion and validation | This document | 1 |
| **1** | Product and business foundation | Executive summary draft; vision, problem statement, goals, OKRs/KPIs with formulas; scope in/out/later; MoSCoW by wave; stakeholder map; 7 actors → 12+ personas with goals, pains and journeys; constraints; dependencies; **BR register** (BR-M01…M66, BR-TENANT…BR-QA, BR-S001…S118) with source citations; ID registry v1 | 1–2 |
| **2** | Functional design | Capability/module map; Mermaid process flows for WF-01…WF-14 and the 4 vertical routes; business rules catalogue (BRL-###: condition/action/exception); RBAC/ABAC matrix (roles × 147 screens × actions); state machines with guards (lead, opportunity, deal, bid, quote, proposal, contract, order, payment, publication, campaign, message, workflow run, tenant, privacy request); notifications; reporting/KPI definitions; search; configuration/admin; audit trail; multi-tenancy; localization; **UX/UI**: IA, screen inventory (147) with wireframe-level descriptions, navigation, design system, WCAG 2.2 AA, error/empty/loading states, responsive behaviour | 3–4 |
| **3** | Architecture, data and integration | C4 context/container/component diagrams; logical and deployment views; tech stack with rationale; ADR-001…; API design and **derived API catalogue**; idempotency, versioning, rate limits; integration patterns and adapter catalogue; batch vs real-time; caching/CDN; scalability; HA/DR (RTO/RPO); environments; conceptual/logical/physical **data model** (Mermaid ERD), data dictionary, indexes, constraints, RLS; lifecycle, retention, archival; migration plan; reference data; data-quality rules; backup/restore; PII classification and masking; **cross-role review** | 3–4 |
| **4** | Security, compliance, NFRs, DevOps, observability | STRIDE threat model; authN/SSO/MFA reuse; authZ; encryption; secrets; OWASP Top 10 (2025, verify) mitigations; audit logging; privacy by design; regulatory mapping (DPDP, TRAI, GDPR, CAN-SPAM, Meta policy, EU AI Act); vendor risk; AI-specific risks; **NFR catalogue** with targets and test methods; repo/branching; CI/CD stages and gates; IaC; feature flags; release/rollback; monitoring, SLOs, alerting; incident management; runbooks; support model; FinOps governance | 2–3 |
| **5** | Epics and user stories | 21+ epics (ID, value, BR/FR links, scope, dependencies, priority, size); stories with Gherkin AC (happy, alternate, negative, validation, permission, edge); enablers, spikes, migration, security, accessibility, observability stories; INVEST; DoR/DoD; **dimension matrix** (persona × permission × state × data condition × channel × tenant/config × integration availability × locale) with covered/merged/excluded rationale | 6–9 (≈ 3 epics per batch) |
| **6** | QA | Test strategy (levels, types, risk-based priority, entry/exit, environments, synthetic/masked data, defect severity matrix, automation pyramid/tools/CI, coverage targets, metrics); scenarios per epic; test cases (EP, BVA, decision tables, state transition, pairwise) with technique labels; AI evaluation cases; requirement → test traceability with coverage % | 4–6 |
| **7** | AI agents and automations | Discovery funnel (dimensions, raw combinations, filters, merges, final count, exclusions); catalogue AG-/AU- split Release 1/2/Future; spec table + detail cards; multi-agent orchestration; model strategy (Sonnet primary, lighter-tier recommendation, verified fallback chain with "verify availability" notes); routing tiers 0–3; data governance for fallbacks; reliability patterns; quantified cost optimization; subscriptions/tooling; AI TCO low/base/high with formulas; AI governance (HITL, injection defences, kill switch, EU AI Act classification); **cross-role review** | 3–4 |
| **8** | Delivery plan | Roadmap and waves; release plan; Sprint 0/1/2 plans; team and RACI; estimation method and ranges; critical path; risk register (RSK-###); change management and training; go-live checklist; hypercare; post-launch KPI tracking | 2 |
| **9** | Appendices and final quality report | Full traceability matrix (BR → FR → EP/US → screen/API/entity → TC); glossary; ID registry; assumption/gap/conflict/recommendation/OQ registers (final); final quality gate report; **cross-role review** | 2–3 |
| **10** | Final assembly | .docx (cover, TOC, headers/footers with page numbers, styled headings, formatted tables, Mermaid diagrams rendered to images) and .pdf with the same content; optional .xlsx (traceability, stories, test cases, agent catalogue). **Path:** files will be created here (pandoc, python-docx and LibreOffice are available) and provided as downloads | 1 |

---

## 0.12 Quality gate: Part 0 (Section 11 checklist)

| # | Check | Result | Notes / fixes applied |
|---|---|---|---|
| 1 | Every requirement in this part is traced to a source section | **Pass** | All inventory rows, NFRs, gaps and conflicts cite BRD/FRD § (ASSUMPTION-000 convention) |
| 2 | All assumptions, gaps and conflicts are tagged and logged | **Pass** | 21 ASSUMPTION (000–020), 34 GAP, 14 CONFLICT, 18 RECOMMENDATION, 10 AMB, 30 OQ |
| 3 | IDs are unique and consistent with earlier parts | **Pass** | First part; registry initialized. Source IDs (M, B-, SM-FR, W/A, OPT) preserved |
| 4 | No story lacks acceptance criteria; no requirement lacks a test | **N/A (Part 0)** | Tests are undefined in the source (GAP-003); covered in Parts 5–6 |
| 5 | Negative, edge, security and accessibility cases covered | **Partial (by design)** | Identified as NFR-001…038 and RECOMMENDATION-001; detailed in Parts 4–6 |
| 6 | No agent lacks guardrail, fallback, KPI, cost | **N/A (Part 0)** | Part 7 |
| 7 | Time-sensitive facts flagged "verify" with as-of date | **Pass** | Model prices (GAP-028), regulations (ASSUMPTION-003), region availability (ASSUMPTION-004), FX: all "verify at implementation, as of 27 Nov 2026" |
| 8 | No restricted data routed to free-tier fallback models | **Pass (policy set)** | RECOMMENDATION-004 established as a binding design rule |
| 9 | Content consistent with earlier parts | **Pass** | Baseline part |

**Self-review corrections made during drafting:**
1. I first counted only 138 functional requirements. I added the 9 new interfaces (GAP-019) and the 3 non-screen operations, giving 150.
2. I recognized that "shared PostgreSQL" means shared *within* this product across tenants (CONFLICT-009), not shared with the investor product.
3. I re-verified every arithmetic figure from the source (0.3.1 table).

---

**Status: Part 0 of 10 complete. Next: Part 1 (Product and business foundation). Reply "continue".**
