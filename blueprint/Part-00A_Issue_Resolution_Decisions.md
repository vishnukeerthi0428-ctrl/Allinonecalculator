# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 0A, Issue Resolution and Decision Log

| Field | Value |
|---|---|
| Document | Application Blueprint, Part 0A (addendum to Part 0) |
| Version | 1.0 |
| Date | 27 Nov 2026 |
| Decision authority | **Delegated by the Product Owner (instruction of 27 Nov 2026):** "the issues found could be human errors; make the corrections to the best of your expertise and answer the open questions to the best of your expertise, then proceed." |
| Effect | Every CONFLICT, GAP, ambiguity (AMB) and open question (OQ) from Part 0 is closed with a decision (`DEC-###`). Later parts treat these decisions as baseline requirements. The Product Owner may override any decision through normal change control (BRD §11) |
| Tagging | Decisions that add content beyond the source documents remain traceable as **[RECOMMENDATION-###] → accepted under DEC-###**. Time-sensitive facts remain marked *verify at implementation (as of 27 Nov 2026)* |

---

## A. Decision principles applied

The documents themselves supplied the criteria for every correction:

1. **Most recent and most specific text wins.** "Current scope" sections (BRD §1, §17; FRD §1, §16) override legacy or retained wording (BRD §9 routing decision: "explicit access classification … override any older role wording").
2. **Fail closed.** When two readings differ, choose the safer one: deny, approval required, or no external effect (FRD §12).
3. **Rules first, open-source first, lowest sustainable cost** (BRD §10; FRD OPT-03-01, OPT-10-01).
4. **No silent invention.** Anything added is labelled, justified and reversible.
5. **Verified outcomes over activity** (BRD §12.1, §13.1).

---

## B. Corrections of probable human errors in the source documents

| DEC | Item | Probable error | Correction (now baseline) |
|---|---|---|---|
| DEC-001 | CONFLICT-001: 80% vs 90% precision | Two numbers written for two different gates without saying so | **Two gates.** (a) *Signal classification* (M14) must reach **≥ 80% precision** on ≥ 100 human-reviewed pilot signals to exit Wave 1. (b) *Qualification* (OPT-04-02) must reach **≥ 90% precision** on the approved benchmark set (≥ 200 labelled items per vertical) before any qualification step runs at Supervised (L2) or Controlled Autonomous (L3) level. Below 90%, qualification stays at Assisted (L1, human accepts each item). Recall is also tracked (target ≥ 60%) to stop over-abstention |
| DEC-002 | CONFLICT-002: fundraising wording left over | Text copied from the sibling investor application | Replacements: "offerings or fundraising thesis" → **"offerings and commercial objectives"** (W33); "customize offerings or funding goals" → **"customize offerings and commercial objectives"**; "offering/issuer thesis" → **"offering / commercial objective"** (filter scope); "investment/delivery geography" → **"delivery geography"**; "verified funding or commercial receipt" → **"verified commercial receipt"** (OPT-12-03); "Investor app only fundraising" → **"This product exposes no fundraising capability; a negative test proves it."** A permanent regression test (no investor entities, routes, filters or terms) is added |
| DEC-003 | CONFLICT-003: "M01 already developed in AppNAI", "Approved AppNAI product truth" | The identity line and the catalogue line were written while AppNAI was the only startup | M01 = **reuse the AppNAI identity/security codebase as a shared library and IdP** with a new, separate OAuth audience `growth-engine` and two clients (`growth-website`, `growth-admin`). Identity is shared; product access is not. M02 = **"Approved startup offering truth" per startup workspace**. AppNAI is one workspace among many |
| DEC-004 | CONFLICT-004: ₹14,500 vs ₹15,000 base | Rounding in the narrative | **₹14,500** base, **₹16,675** with 15% contingency, **₹31,165** with Apollo reserve and developer seats. These are the authoritative figures |
| DEC-005 | CONFLICT-005: effort vs timeline vs team | The team assumption (3 FTE including 0.5 non-engineering) cannot deliver 287–483 person-days in 180 days | **Core delivery team of 4.0 engineering FTE + 0.5 growth/compliance lead**: 1 backend (Django), 1 full-stack, 1 frontend (React), 0.5 QA automation, 0.5 DevOps/SRE (part-time contractor), plus founder/CTO as Product Owner and architect. Capacity ≈ 4.0 × 125 working days × 0.8 focus ≈ **400 person-days in 180 days**, which covers the midpoint (385 pd). Overflow beyond the midpoint goes to Wave 6 (Day 181–365) by MoSCoW (Could items first). Indicative staffing cost: 4.0 FTE × 6 months × ₹1.0–1.5 L = **₹24–36 L**, consistent with the source range ₹13.05–32.93 L plus utilization slack. If the extra FTE is not approved, the fallback is **3 engineering FTE with Waves 0–5 stretched to ≈ 7.5 months** |
| DEC-006 | CONFLICT-006: "no release labels" vs Release 1/2/Future | Prompt vocabulary vs source vocabulary | Use **delivery waves W0–W6** mapped to the source day-phases. "Release 1" = W0–W3 (Day 1–90), "Release 2" = W4–W5 (Day 91–180), "Future" = W6+ (Day 181–365+). These are *planning groupings*, not product versions; production is one continuously deployed product behind feature flags |
| DEC-007 | CONFLICT-007: model provider and routing | The FRD lists "Claude/OpenAI"; the prompt mandates Sonnet primary plus free fallbacks | **Tier 0:** deterministic rules, templates, exact/semantic cache (no LLM). **Tier 1a:** lighter Claude tier (Haiku-class) for high-volume classification and extraction, only where evals show parity ([RECOMMENDATION-003] accepted). **Tier 1b:** Claude Sonnet (latest GA) for complex reasoning, high-stakes or customer-facing drafts. **Tier 2:** free-tier/open-weight fallbacks, **only for data classified Public or Internal-non-personal**, opt-in per tenant, default OFF. **Tier 3:** graceful degradation (queue, cached or partial result, human task). OpenAI and other *paid* non-Anthropic providers stay disabled by default (BRD §10) |
| DEC-008 | CONFLICT-008: ₹3,000/month AI reserve | Reserve sized for a "small pilot" before the agent scope was defined | **Three budget ceilings, each a hard cap enforced by M53:** Pilot **₹3,000/month** (owned portfolio, BRD §8 pilot volumes); Growth gate **₹12,000/month** (unlocked only when the BRD §8 scale gate passes: measured cost per qualified opportunity, consent compliance and conversion); Scale **₹40,000/month** for owned startups. SaaS client tenants carry **their own metered AI budget** charged through their plan (B-SVC), never subsidized by the owned-portfolio budget. Part 7 sizes every agent to fit. All figures are estimates; verify model prices at implementation |
| DEC-009 | CONFLICT-009: operator/admin workspace and "shared PostgreSQL" | Older architecture wording | **Two frontends only:** `commercial-website-react` (public site + external portal) and `commercial-admin-react` (Command Centre, where "Automation" is a separately permissioned route group). **One PostgreSQL cluster for this product**, shared by all its tenants with RLS and composite tenant keys. It is fully independent of the investor product's database |
| DEC-010 | CONFLICT-010: A104/A105 under-mapped | Mapping omission | A104 → BR-TENANT, WF-08, BR-M43, BR-M44, BR-M46. A105 → BR-TENANT, WF-10, BR-M44, BR-M47, BR-M48 |
| DEC-011 | CONFLICT-011: 0–1 components vs 0–100 thresholds | Scale not stated | **Opportunity score = round(100 × Σ wᵢ·cᵢ / Σ wⱼ over known components)** with w = fit 0.25, evidence 0.25, intent 0.20, readiness 0.15, timing 0.15. If the known components carry less than 0.60 total weight, the score is **"Unknown – review required"**, never a number. Bands: ≥ 75 priority review; 50–74 research/nurture; < 50 archive/review. A score never grants permission to contact (BRD §4) |
| DEC-012 | CONFLICT-012: superseded estimate retained | Historical text | Planning basis = **287–483 person-days (₹13.05–32.93 L)**. The ₹9–13.5 L and ₹18–27 L figures are historical references only |
| DEC-013 | CONFLICT-013: "MVP growth dashboard" | Label inconsistency | Drop "MVP". M30 "Growth dashboard" is delivered in W2 |
| DEC-014 | CONFLICT-014: duplicated acceptance procedures | Copy-paste repetition | One **Acceptance Procedure Register (AP-01…AP-09)**: AP-01 Configurable owned startups (26th synthetic startup); AP-02 Scope separation of business capabilities; AP-03 Opportunity qualification; AP-04 Closure and receipt distinction; AP-05 Sensitive-data exclusions; AP-06 Autonomy and approval; AP-07 Reusable business templates; AP-08 Requirements traceability semantic approval; AP-09 Entitlement and trial controls; plus **AP-10 Boundary and acceptance conditions** (two-tenant fixture) |

---

## C. Resolution of gaps

| DEC | Gap | Decision (baseline from now on) |
|---|---|---|
| DEC-015 | GAP-001 API catalogue missing | Part 3 publishes a **derived API catalogue** covering every screen action and module operation, marked *DERIVED*. The 105 named operations keep their paths (legacy contract retention, BRD §9). New operations use `/api/v1/commercial/{public|portal|admin|internal}/…`. If the original 302-operation catalogue surfaces later, it is reconciled by a mapping table |
| DEC-016 | GAP-002 entity catalogue missing | Part 3 adds the unnamed core entities as *DERIVED*: Tenant, Startup, BusinessLine, Offering, OfferingVersion, CapabilityProfile, Domain, Publication, PublicationSnapshot, PreviewGrant, Bid, BidChecklistItem, Order, OrderLine, FulfillmentEvent, ReceivableEntry, PayableEntry, Plan, PlanVersion, Entitlement, UsageMeterReading, ServiceInvoice, Trigger, NodeTemplate, WorkflowTemplate, ConfigRevision, ApplicationDraft, ConflictCase, SupportAccessGrant, ExportJob, ImportJob, JurisdictionRule, ApprovalPolicy, TaxProfile, FxSnapshot |
| DEC-017 | GAP-003 test catalogue missing | Part 6 defines test cases (TC-###). The referenced SM-UT-001…066, SM-UAT-S###, SM-UX-UAT-### IDs are kept as **aliases** inside the traceability matrix so source references still resolve |
| DEC-018 | GAP-004 NFR targets missing | [RECOMMENDATION-002] accepted: Website/Portal availability **99.5%** monthly (pilot) → **99.9%** at scale gate; Admin **99.5%**; API p95 **≤ 500 ms reads / ≤ 800 ms writes** (excluding provider latency); public page TTFB p95 **≤ 800 ms** (CDN-cached ≤ 200 ms); outbox dispatch lag p95 **≤ 60 s**; **RPO ≤ 15 min** (point-in-time recovery), **RTO ≤ 4 h**; capacity for **10× pilot volume** without re-architecture. Full NFR catalogue in Part 4 |
| DEC-019 | GAP-005 H02/H03 undefined | Interpreted as **H02 = existing identity service (login, sessions, recovery)** and **H03 = existing security controls (MFA, session revocation, audit of auth events)**. A Sprint 0 **compatibility spike** (2–3 days) produces a pass/fail report on 12 checks: product audience, separate clients, PKCE, refresh rotation, MFA (TOTP minimum, WebAuthn for privileged roles), revocation latency ≤ 60 s, membership claims, external-user registration, recovery isolation, rate limiting, audit events, logout propagation. Any failed check becomes a change request (ASSUMPTION-019). **Pattern:** a Backend-for-Frontend in Django per frontend origin holds tokens server-side; the browser gets only `HttpOnly; Secure; SameSite=Strict` session cookies |
| DEC-020 | GAP-006 budget IDs undefined | **B01** AWS hosting ₹5,000 · **B02** production AI inference ₹3,000 · **B03** public search API ₹1,500 · **B04** extraction compute/overage ₹1,000 · **B05** email delivery ₹500 · **B06** WhatsApp Business ₹2,000 · **B07** monitoring/security/CI ₹500 · **B08** Apollo enrichment reserve ₹9,000 (conditional, OFF by default) · **B09** Claude Code developer seats ₹3,600 · **B10** optional integration reserve ₹1,000 · **B11** contingency 15%. **B12–B22 reserved, ₹0 until approved:** B12 paid ads media spend (per startup, separate approval) · B13 e-signature · B14 payment gateway fees (pass-through %) · B15 calendar/meeting · B16 social platform APIs · B17 SEO data · B18 contact verification API · B19 embeddings/vector overage · B20 backup/DR storage · B21 CDN/WAF · B22 LLM observability/eval. **C03** = engineering delivery budget (person-day package, BRD §6) |
| DEC-021 | GAP-007 artefacts not attached | Proceed without them. MedMaarg claims (750+ users, ~150 monthly users, one Odisha location) are **management claims, not independently audited** (BRD §8). They may be published only after claim approval in M02/A051 with evidence. Integration choices follow the decisions in this log, and Part 7 has a "verify" column |
| DEC-022 | GAP-008 payment provider | **Payment adapter interface.** Pilot path (W4): (1) **bank transfer / UPI with evidence upload + finance maker-checker verification**, which suits B2B, tenders and institutions; (2) **an Indian payment gateway with payment links and signed webhooks** (shortlist: Razorpay, Cashfree, PayU; verify terms, fees and webhook signing at procurement). International (AppNAI, W6): Stripe or equivalent where entity eligibility allows (verify). The platform never stores card or bank credentials |
| DEC-023 | GAP-009 e-signature provider | **E-sign adapter interface.** Pilot (W4): **signed-PDF upload** + SHA-256 hash + counter-party confirmation through the portal (W24), with legal approval of the exact hash. W5: integrate one provider supporting Aadhaar eSign and DSC for Indian counter-parties (shortlist: Leegality, Digio, Zoho Sign; DocuSign for international). **Verify legal validity under the IT Act 2000 and the provider's current terms.** AI never signs (M46) |
| DEC-024 | GAP-010 calendar | Google Workspace Calendar first (W2); Microsoft 365/Graph in W5. Free/busy only; no event-content reading beyond the booking's own events |
| DEC-025 | GAP-011 email | **Amazon SES** (matches budget B05); dedicated configuration set per startup sender; SPF/DKIM/DMARC enforced; bounce/complaint SNS webhooks → suppression. Resend stays an alternative adapter, not installed |
| DEC-026 | GAP-012 locales | Admin UI: **English (en-IN)** only. Website/portal UI chrome: en-IN at launch, i18n-ready (ICU message format). **Content locales** (pages, templates, WhatsApp templates): en-IN at launch; **hi-IN, ta-IN, or-IN** enabled in W5 for MedMaarg/EduVerse/OrganicSpec where approved translations exist. Machine translation produces drafts only and requires approval |
| DEC-027 | GAP-013 tax, rounding, FX | **TaxProfile per startup** (GSTIN, state, LUT for exports); **HSN/SAC per offering**; intra-state CGST+SGST, inter-state IGST, exports zero-rated under LUT. **Rounding:** ROUND_HALF_UP to 2 decimals per line, document total = sum of rounded lines (FRD §12.1 example: 2 × 150.00 × 0.90 = 270.00). **FX:** never converts actuals. Reporting conversions use a recorded FxSnapshot (source, rate, date). **Statutory GST e-invoice (IRN) generation is out of scope.** Startups above the e-invoicing threshold record the IRN from their accounting system. The platform issues proformas/quotations and commercial invoices for startups below the threshold and for SaaS billing. *Verify current GST rules and thresholds with the finance advisor* |
| DEC-028 | GAP-014 retention | ASSUMPTION-018 adopted as baseline (subject to legal confirmation): invoices/financial records **8 years** · contracts **term + 8 years** · audit log **7 years** · marketing contact data **24 months after last eligible interaction** · suppression list **indefinite (minimal hashed identifier)** · research evidence **12 months** (metadata kept, page content purged) · AI run logs **90 days redacted** (aggregates kept) · chat transcripts **90 days** · rejected/withdrawn leads **6 months** · application drafts **30 days** · backups **35 days** rolling. Legal hold overrides deletion. Deletion never removes the suppression record (M56) |
| DEC-029 | GAP-015 non-Indian jurisdictions | **Jurisdiction Rule Pack** in the Policy Decision Point ([RECOMMENDATION-016] accepted). Year 1 outbound allowlist: **India** (DPDP + TRAI rules), **EU/EEA/UK** (B2B email only to role-based or professionally published addresses, legitimate-interest assessment recorded, mandatory one-click opt-out, no WhatsApp cold outreach), **US** (CAN-SPAM: identification, physical address, opt-out honoured within 10 business days, practically immediate), **UAE/Singapore/Australia** (consent-first; opt-in only). **Any other jurisdiction: outbound denied; inbound replies allowed.** Tender-portal submissions follow each portal's own terms. *Verify each rule with counsel before activation* |
| DEC-030 | GAP-016 children / guardian consent | **No direct outreach, profiling or targeted advertising to anyone under 18.** EduVerse acquisition goes through **institutions** (schools/colleges under MoU) and **verified guardians**. Intake (W17) asks age band first. Under 18 → guardian name and contact required; guardian verified by OTP to the guardian's own channel + explicit declaration + consent record. The learner's data is limited to name, grade band and programme. No minor data in AI prompts beyond the grade band. A DPIA is required before activation. *Verify the DPDP Rules' verifiable-consent mechanism (e.g. DigiLocker-based tokens) at implementation* |
| DEC-031 | GAP-017 scale | ASSUMPTION-002 adopted: Year 1 = **25–40 startup workspaces, 2–10 external tenants, 15–60 internal users, ≤ 500 portal users/month, ≤ 5,000 public sessions/month**. Year 2 design point: 100 workspaces, 30 tenants, 200 internal users, 5,000 portal users/month, 50,000 public sessions/month |
| DEC-032 | GAP-018 "agreed window" | **Transactional automation** (replies, follow-ups, notifications): ≥ 99% of eligible due runs started **within 15 minutes** of the due time. **Scheduled batch** (discovery, enrichment, reports): ≥ 99% **within 24 hours**. Quiet hours and time zones are honoured and not counted as late |
| DEC-033 | GAP-019 missing FR rows | Created as **FR-W31, FR-W32, FR-W33, FR-W34, FR-A109, FR-A110, FR-A111, FR-A112, FR-A113** in Part 2, using the BRD §17 purpose/acceptance text and the FRD §16.2 field specs |
| DEC-034 | GAP-020 phase gates vs M-ranges | Phase gates follow **register (dependency) order**, not numeric order. W0 = M01–M09 + M53 + M56 + M58; W1 = M10–M20; W2 = M21–M30 + M55; W3 = M31–M42 + M57; W4 = M43–M51; W5 = M52, M54, M59–M62; W6 = M63–M66. M54 (AI quality) is built in W0 as the eval harness of M08 and completed in W5 |
| DEC-035 | GAP-021 Copilot | **Admin Copilot** ([RECOMMENDATION-008] accepted): Admin-only side panel; answers questions over records the user is already authorized to see and over approved knowledge, **with citations**; can create *drafts* (message, task, note, filter) at L1; cannot approve, send, publish, spend, change configuration or reveal other scopes; refuses when no evidence exists; every turn is logged |
| DEC-036 | GAP-022 internal notifications | **In-app notification centre (A106)** + **email digest** (immediate for severity High/Critical, hourly or daily digest otherwise, per user preference). No WhatsApp/SMS to internal staff in W0–W5 |
| DEC-037 | GAP-023 global search | Scoped global search (Admin) over organizations, contacts, deals, bids, orders, documents and content using PostgreSQL full-text + trigram; RLS enforced; results show only permitted fields |
| DEC-038 | GAP-024 approval thresholds | **Default approval policy** (configurable per startup, versioned, tightening needs no approval, loosening needs founder approval): any discount **> 0% → Sales Manager**; **> 10% → Startup Head**; **> 20%, or margin below the startup's floor (default 25%) → Founder + Finance**; any non-standard term → **Legal**; contract value **≥ ₹10 lakh or any cross-border contract → Founder + Legal**; every invoice and payment verification → **Finance maker-checker** (two different people); bid submission → **Startup Head**; campaign launch → **Marketing Lead + claims approval**; ad spend → **within approved cap only**; publishing → **Content approver ≠ author** |
| DEC-039 | GAP-025 migration | No legacy system migration assumed. **Import via A103** using versioned CSV/JSON templates for organizations, contacts (with consent evidence and source), offerings, price lists and open deals; dry-run validation report; imported contacts are **not eligible for outreach until consent/lawful basis is verified** |
| DEC-040 | GAP-026 hosting/HA | AWS **ap-south-1**. Pilot: cost-minimal topology within B01 (managed PostgreSQL with PITR, containerized Django/Celery on small instances, S3, CloudFront). Scale gate: Multi-AZ database and two app instances behind a load balancer. Backups copied cross-region (verify ap-south-2 availability). Sizing and costs in Part 3 (estimates, verify) |
| DEC-041 | GAP-027 monitoring | OpenTelemetry instrumentation; **Sentry** (errors, free/developer tier first, verify limits) + **CloudWatch** (infra metrics/logs/alarms) + **Prometheus/Grafana OSS** optional at scale; SLO dashboards and alert routing defined in Part 4 |
| DEC-042 | GAP-028 model names and prices | Treated as **unverified, time-sensitive**. Part 7 shows pricing as formula inputs with "verify at implementation (as of 27 Nov 2026)" |
| DEC-043 | GAP-029 devices | Responsive web: Website/Portal mobile-first (360 px+), Admin desktop-first (1280 px+, usable down to 768 px for review/approval screens). Supported browsers: last 2 versions of Chrome, Edge, Firefox, Safari (iOS/macOS) |
| DEC-044 | GAP-030 SaaS support | Pilot support: **10:00–18:00 IST, Monday–Saturday**, via portal tickets (W28/W34) and email. Internal response targets (not contractual): S1 2 h, S2 8 business hours, S3 3 business days. No public SLA until measured (OPT-20-03) |
| DEC-045 | GAP-031 inventory | OrganicSpec: per-SKU **availability status + available quantity + reservation on order approval** (released on cancellation or expiry). No warehouse, lot or batch management (Later) |
| DEC-046 | GAP-032 referral commission | **Record only:** partner, referral, attribution, proposed commission %, approval. Payouts happen outside the platform (finance system) |
| DEC-047 | GAP-033 SaaS plans | Three **plan archetypes** with configurable entitlements and **no published price until the Service Owner approves**: *Starter* (1 startup workspace, 3 users, email channel, 1,000 AI tasks/month), *Growth* (3 workspaces, 10 users, email + WhatsApp + website, 5,000 AI tasks/month), *Scale* (custom). Metering dimensions: workspaces, users, AI tasks, outbound messages, research fetches, storage GB. Overage only if approved |
| DEC-048 | GAP-034 tool registry | Part 7 defines the agent **tool registry** (allowlisted internal tools, scopes, rate limits, side-effect class). No agent gets a tool with an external side effect without the dispatch guard |

---

## D. Resolution of ambiguities

| DEC | AMB | Decision |
|---|---|---|
| DEC-049 | AMB-1 Copilot | See DEC-035 |
| DEC-050 | AMB-2 Outcome certainty | Enum `confirmed`, `uncertain`, `failed`, `reconciled_confirmed`, `reconciled_failed`. Uncertain blocks retry until reconciled |
| DEC-051 | AMB-3 Workflow builder | Declarative DAG from approved node types (A113); conditions use a sandboxed expression language over typed fields; **no code nodes, no secrets in configuration** |
| DEC-052 | AMB-4 Capability-based bid/order | Bid and order desks are enabled by **capability profile** per startup/tenant. Owned-portfolio routing default: external AI project → AppNAI; education → EduVerse; healthcare partnership → MedMaarg; organic trade → OrganicSpec (FRD §12.1) |
| DEC-053 | AMB-5 Tender submission | **Never automated.** The system prepares the bid package and checklist; a human submits on the portal and records evidence (submission ID, timestamp, screenshot/receipt hash). Maximum autonomy L1 |
| DEC-054 | AMB-6 Closure criteria | **ClosurePolicy per opportunity type:** project/contract types close on *executed contract* (Won-Contracted) and are separately marked *Paid* on verified receipt; product/order types close on *verified payment or accepted delivery per terms*. Dashboards always show Awarded, Signed, Delivered and Paid separately (BRD §13.1) |
| DEC-055 | AMB-7 Portfolio read-only | The portfolio (multi-startup) scope renders aggregates and drill-down only. Every mutating control is hidden and also denied server-side until exactly one startup is selected |
| DEC-056 | AMB-8 Support access | **SupportAccessGrant:** requested by platform support, approved by the tenant admin, scoped (modules, read-only by default), time-boxed (max 72 h), every access audited and visible to the tenant |
| DEC-057 | AMB-9 Founder snapshot import | One-way file import (A103) of non-confidential business facts into M02 drafts. Still subject to claim approval. No live link to the investor product |
| DEC-058 | AMB-10 Investor app | Separate product with a shared IdP and a distinct audience. Tokens for the investor audience are rejected here (NFR-001/OPT-01-01) |

---

## E. Answers to the open questions (delegated)

| OQ | Question | Answer (decision) | DEC |
|---|---|---|---|
| OQ-001 | Precision target | Two gates: 80% signals, 90% qualification | DEC-001 |
| OQ-002 | Remove fundraising wording | Yes, with replacement list and negative regression test | DEC-002 |
| OQ-003 | Existing identity (H02/H03) | Reuse AppNAI identity as library/IdP, new audience, BFF pattern; Sprint 0 compatibility spike with 12 checks | DEC-003, DEC-019 |
| OQ-004 | Payment gateway | Adapter; bank/UPI evidence + Indian gateway payment links (shortlist), international later | DEC-022 |
| OQ-005 | E-signature | Signed-PDF + hash in W4; Indian e-sign provider in W5 | DEC-023 |
| OQ-006 | Calendar | Google first, Microsoft W5 | DEC-024 |
| OQ-007 | Email provider | Amazon SES | DEC-025 |
| OQ-008 | Locales | en-IN; hi/ta/or content locales W5 | DEC-026 |
| OQ-009 | AI ceiling | ₹3,000 pilot, ₹12,000 growth gate, ₹40,000 scale; tenants self-funded | DEC-008 |
| OQ-010 | Jurisdictions | Rule pack; India, EU/UK, US, selected opt-in markets; others denied outbound | DEC-029 |
| OQ-011 | SLOs/RTO/RPO | Accepted | DEC-018, DEC-032 |
| OQ-012 | Retention | Accepted schedule (legal confirmation) | DEC-028 |
| OQ-013 | Missing catalogues | Derive and tag DERIVED; reconcile if provided | DEC-015–017, DEC-021 |
| OQ-014 | Approval thresholds | Default policy matrix | DEC-038 |
| OQ-015 | Timeline vs capacity | 4.0 engineering FTE + 0.5 growth/compliance; fallback 3 FTE over 7.5 months | DEC-005 |
| OQ-016 | Region/HA | ap-south-1; pilot single-AZ app + PITR DB; Multi-AZ at scale gate | DEC-040 |
| OQ-017 | Free-tier fallbacks | Allowed only for Public/Internal-non-personal data, per-tenant opt-in, default OFF | DEC-007 |
| OQ-018 | Copilot | Read-only grounded assistant, drafts only | DEC-035 |
| OQ-019 | Referral commission | Record only | DEC-046 |
| OQ-020 | OrganicSpec inventory | Availability + reservation | DEC-045 |
| OQ-021 | Migration | CSV/JSON import, consent-gated | DEC-039 |
| OQ-022 | SaaS plans/support | Plan archetypes, no price until approved; pilot support hours | DEC-044, DEC-047 |
| OQ-023 | Two frontends | Confirmed | DEC-009 |
| OQ-024 | Budget IDs | B01–B22, C03 defined | DEC-020 |
| OQ-025 | Tax/rounding/FX | TaxProfile, HALF_UP per line, FX snapshot, no IRN | DEC-027 |
| OQ-026 | Guardian consent | No direct outreach to minors; institution/guardian-verified intake; DPIA | DEC-030 |
| OQ-027 | Users/tenants | Year 1 and Year 2 design points | DEC-031 |
| OQ-028 | Phase-gate mapping | Register order | DEC-034 |
| OQ-029 | Internal notifications | In-app + email digest | DEC-036 |
| OQ-030 | Waves vs releases | Accepted | DEC-006 |

**Open-question status after Part 0A: 30 of 30 answered. 0 open. 0 blocking.** The validations still pending (Sprint 0 identity spike, legal confirmation of retention/jurisdiction/e-sign/children rules, procurement verification of providers and prices) are logged as **risks and verification tasks** (RSK and Sprint 0 enablers), not as open questions.

---

## F. Additional corrections found on a second reading

| DEC | Finding | Correction |
|---|---|---|
| DEC-059 | Part 0 counted **118** supplementary business statements. A second pass found **22 more platform-principle statements** (BRD §1, §1.2, §2, §3, §5, §6 SaaS paragraph, §9, §9.1, §10, §11, §12.2, §16, §17.1, §17 release condition) | Supplementary BR count corrected to **140 (BR-S001…BR-S140)**, registered in Part 1 §1.12. Total business requirements = 71 primary + 140 supplementary = **211** |
| DEC-060 | M66 "Future product commercialization" is placed in the last phase, but its control ("planned offerings not promoted") is needed from day one | The **readiness gate** (planned/approved/available status blocks promotion) is built in **W0 within M02**. The **launch-approval workflow** (A097/A098) is delivered in **W6** |
| DEC-061 | M54 "AI quality and feedback" is placed in Day 121–180, yet "Regression fails block deploy" is needed as soon as any AI feature ships | **Eval harness and CI regression gate in W0** (with M08); **human-feedback loop UI (A084) in W5** |
| DEC-062 | M61 "Admin command center" is in the last build phase, but the seven-view navigation (BRD §3) is the frame for every screen | **Command Centre shell and navigation (A003, A089 frame) in W0–W2**; cross-startup aggregate projections and exception queue completed in W5 |
| DEC-063 | M62 "End-to-end production release" is listed as a module, but release gating applies to every wave | **Release pipeline and gates in W0 (with M09)**; the full synthetic E2E journey suite is completed in W5 |
| DEC-064 | Workflow register text "No AI direct finance or binding terms" and actor rule "no autonomous financial transfer" lack a numeric autonomy cap | **Autonomy cap matrix:** money movement = not supported (record/verify only); contracts, quotes, discounts, bid submission, legal terms = **L1 maximum**; publishing and campaigns = **L1** (approved hash) then **L2 dispatch** of the approved item; routine replies from approved FAQ, eligible follow-ups, reminders = up to **L3** within caps |
| DEC-065 | "Startup" vs "tenant" for owned portfolio is not stated | **Owned portfolio = one tenant ("Owner Portfolio Tenant") containing 25+ startup workspaces.** Each external SaaS client = its own tenant with one or more startup workspaces. Cross-tenant aggregation is never permitted; cross-startup aggregation within a tenant is read-only for authorized owners |

---

## G. Updated registers (summary)

| Register | Part 0 | Part 0A status |
|---|---|---|
| CONFLICT-001…014 | Open | **All resolved** (DEC-001…014) |
| GAP-001…034 | Open | **All resolved** (DEC-015…048); validations moved to Sprint 0 tasks/risks |
| AMB-1…10 | Open | **All resolved** (DEC-049…058) |
| OQ-001…030 | Open | **All answered** |
| ASSUMPTION-000…020 | Stated | Retained; ASSUMPTION-002, -018 now baseline via DEC-031, DEC-028 |
| RECOMMENDATION-001…018 | Proposed | **All accepted** (via DEC references) |
| New decisions | none | **DEC-001…DEC-065** |

## H. Quality gate: Part 0A

| Check | Result | Note |
|---|---|---|
| Every decision traced to a source item | Pass | Each DEC cites a CONFLICT/GAP/AMB/OQ and the BRD/FRD section via Part 0 |
| Assumptions/gaps/conflicts tagged and logged | Pass | All closed with DEC IDs |
| IDs unique and consistent | Pass | DEC-001…065 new; no reuse |
| Time-sensitive facts flagged | Pass | Providers, prices, regulations, region availability marked "verify" |
| No restricted data to free-tier models | Pass | DEC-007 restricts Tier 2 to Public/Internal-non-personal |
| Consistency with Part 0 | Pass, with one correction | Supplementary BR count corrected (DEC-059) |

**Status: Part 0A complete. All issues resolved. Continue with Part 1.**
