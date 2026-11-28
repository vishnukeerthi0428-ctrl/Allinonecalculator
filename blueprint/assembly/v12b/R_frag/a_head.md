# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.19a), Platform Decisions Implementation: SSO/SCIM in R1, Developer Platform and Connectors in R1, Vercel Personal-Data Path, RPO ≤ 15 min, Model Registry, Cross-Tenant Benchmarks, Supabase Access Model — Material, Coverage, Register and Designs C1–C4

| Field | Value |
|---|---|
| Document | Part 11.19a: the implementation specification of the Founder platform decisions DEC-778 and DEC-784…789 (with DEC-772 residency). This file holds the material reviewed, the coverage of every V12 aspect that these decisions touch, the detailed register, the catalogue reconciliation and the full-depth designs of capability C1 (enterprise identity: SSO, SCIM, custom roles and separation of duties), C2 (developer platform), C3 (CRM, SMS and voice connectors) and C4 (Vercel personal-data path). Part 11.19b holds C5 (RPO ≤ 15 min), C6 (model registry), C7 (cross-tenant benchmarks), C8 (Supabase access model), automations AU-290…299, the FR register, ADRs, cut-over and cost. Part 11.19c holds epics, stories, the combinatorial test design, test cases, conflicts, decisions, persona review, tags and the quality gate |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Part 11.14 (DEC-770…791); Part 11.5a §11.5.5.2 (identity), Part 11.5b §11.5.5.8–9 (infrastructure, DR); Part 11.6b §11.6.5.3 (model registry); Part 11.8b §11.8.5.4–11 (developer platform, webhooks, connectors, hosting); Part 11.9b (DDL-V12-I, Supabase operating model); Part 11.13b (AU-143); Part 3.2, 3.3, 4.1, 4.3; templates Part 5.1a/b (stories), Part 6.1/6.2a/6.4 (tests), Part 8.1/8.2 (plan) |
| Precedence | V12-B brief > Part 11.14 > this part > Parts 11.1–11.13 > earlier parts (DEC-415 extended) |
| ID ranges used | DEC-880…899 · ASSUMPTION/GAP/CONFLICT/RECOMMENDATION-1080…1099 · ADR-255…264 · FR-V12-R-001…155 · AU-290…299 · US-<EP>-ZR01…29 · TS-V12-R-01…13, 21…28 · TC-V12-R-001…086 (full form) and TC-V12-R-101…1172 (generated) |
| Roles applied | Identity architect (SAML/OIDC, SCIM 2.0, custom roles/SoD) · Developer-platform product lead · Integration architect (CRM, SMS-DLT, voice) · Privacy and cloud-security lead · Database reliability engineer · LLM platform lead · Privacy-preserving analytics scientist · QA Lead · FinOps Lead · DevOps/SRE Lead |

---

## 11.19.0 How to read this part

**What the Founder decided and what this part does.** On 28 Nov 2026 the Founder adopted V12 for every pending item "irrespective of time and cost" (Part 11.14). Seven decisions are platform decisions owned by this group. Earlier review groups had already *specified* most of these capabilities, but had parked them behind conflicts on **timing** (V12 places SCIM, custom roles, OAuth client credentials, the developer portal and sandbox in phase R2, and SDKs in R3) or on **scope** (no external CRM, personal data not through Vercel, Supabase daily backups only, Claude-only model routing, no cross-tenant analytics). This part turns each decision into an implementable, testable and costed specification that a team can build in Release 1 (or Release 2 where stated) with no further clarification.

| Cap. | Capability | Founder decision | Earlier design reused (cited, not repeated) | Release placement in this part | Section |
|---|---|---|---|---|---|
| C1 | Enterprise SSO (SAML 2.0, OIDC), verified domains, MFA and session policy, break-glass, **SCIM 2.0**, **custom roles and separation of duties** | DEC-784 | Part 11.5a §11.5.5.2 (ENT-IDN-01…06, ENT-ACC-01…05), Part 11.8b §11.8.5.11, C2/C3 DDL in Part 11.9b | **Release 1** (all, including SCIM and custom roles that V12 phases at R2) | §11.19.5.1 |
| C2 | Developer platform: API keys, **OAuth client credentials**, rate limits, versioning, **signed webhooks**, **developer portal**, **SDKs** (TypeScript, Python, Java), **sandbox** | DEC-785 | Part 11.8b §11.8.5.4/6 (ENT-API-01…07), C2 tables `api_key`, `webhook_endpoint`, `webhook_delivery`, `sandbox_environment` | **Release 1** (all) | §11.19.5.2 |
| C3 | Connector framework with activation gate; **CRM** (Salesforce, HubSpot, Zoho CRM), **SMS via DLT** (India), **voice connector** (CPaaS 140/160 series) | DEC-785 | Part 11.8b §11.8.5.7/8 (CF-01…12, AD-V12-H-01…03) | **Release 1** (framework, all three CRMs, SMS-DLT, voice transport); AI voice behaviour per Part 11.18 | §11.19.5.3 |
| C4 | Personal data through Vercel (API rewrites and server functions) with DPA, region pinning, no body logging, TLS end to end, header allowlist | DEC-786 (+ DEC-772) | Part 11.8b §11.8.5.10 (CONFLICT-889 option A), Part 11.5b §11.5.5.8 | **Release 1** (IN); EU stack at first EU contract (DEC-772) | §11.19.5.4 |
| C5 | RPO ≤ 15 minutes: continuous WAL archiving, daily base backup, 35-day PITR in every residency region, restore drills at each release gate | DEC-787 (+ DEC-771 RTO ≤ 120 min) | Part 11.5b §11.5.5.9 (DR-01…05) | **Release 1** gate (IN); EU at EU provisioning | Part 11.19b §11.19.5.5 |
| C6 | Provider-neutral model registry; Claude Sonnet approved as primary through the registry; open-weight models with masked personal data; advanced tier and multimodal; V12 fallback rule; 111 evaluation suites | DEC-788 | Part 11.6b §11.6.5.3, AU-151/152/154 | **Release 1** (registry, approval, routing); candidates added as they pass | Part 11.19b §11.19.5.6 |
| C7 | Cross-tenant benchmarks with privacy-preserving aggregation (contract clause, opt-in, k ≥ 10, noise) | DEC-789 | Part 11.13b AU-143 (CONFLICT-983 proposal) | Build in **Release 2**; activates per cohort when k ≥ 10 opted-in tenants exist [ASSUMPTION-1085] | Part 11.19b §11.19.5.7 |
| C8 | Supabase access model: least-privilege RLS-bound role `app_rw`, never `service_role`; Data API disabled for application schemas; `service_role` only for CI migrations behind break-glass | DEC-778 | Part 11.9b §11.9.5.2/4 (SB-01…10) | **Sprint 0–1** (before any tenant data) | Part 11.19b §11.19.5.8 |

**Safety statement (V12-B).** None of these capabilities widens what an automated caller may do on its own. API keys, OAuth clients, connectors and SCIM can create records and drafts and read within scope. Consequential actions (send, publish, pay, sign, submit bids, set prices) are executed either by a human with step-up or by the **bounded-mandate engine of Part 11.17** (DEC-779), which keeps the two-person approval, scope and value caps, revocation, kill switch, PDP dispatch recheck, audit and reconciliation. No API scope grants a consequential action (§11.19.5.2.C). Jurisdiction rule packs (Part 11.15) gate SMS, voice and CRM transfers per market; a connector activates in a jurisdiction only when that pack is counsel-approved. These are mandatory controls, never options.

**Terms used.** IdP identity provider; SP service provider; HRD home-realm discovery; SCIM System for Cross-domain Identity Management; SoD separation of duties; JIT just-in-time; PKCE Proof Key for Code Exchange; HMAC hash-based message authentication code; DLT distributed-ledger registration of entities, headers and templates mandated by TRAI in India; CPaaS communications platform as a service; NCPR National Customer Preference Register (India); PITR point-in-time recovery; WAL write-ahead log; RPO/RTO recovery point/time objective; DP differential privacy; ε privacy-loss parameter; k minimum cohort size; RLS row-level security; PDP policy decision point.

---

## 11.19.1 Material reviewed

{{INV_TABLE}}

**Method (programmatic, every line).** `assembly/v12b/R_01_inventory.py` reads every line of the 25 BRD and 40 FSD V12 chapters and their appendices (the historical annexes `ZZ_*` are non-normative and excluded), splits headings and table rows, matches nine topic patterns (identity, developer API, webhooks, connectors, region/hosting, recovery, model registry, benchmarks, database access), removes repeated boilerplate (the FSD repeats requirement tables in ch. 01, 40 and the appendices), and writes one atomic aspect per distinct statement to `final/coverage_v12/R_coverage.csv`. A line is **core** when it sits in an architecture, identity, API, integration, security, infrastructure, recovery, roadmap or decision chapter, or carries an ENT-, MDL-, AIX-, SCIM, RPO or DEC-V9-01 token; all other matches are workflow-level mentions (for example "webhook" in a step of SM-SVC-14) that Parts 11.2–11.4 already specify and that inherit the platform controls designed here.

| Source used for design (beyond V12) | Why |
|---|---|
| Part 11.14 DEC-770…791 | Binding decisions; DEC-778 and DEC-784…789 are implemented here |
| Part 11.5a §11.5.5.2, Part 11.8b §11.8.5.4–11, Part 11.9b | Earlier designs; reused and completed, not repeated |
| Part 11.6b §11.6.5.3, AU-151/152/154 | Model registry routing reconciled with DEC-418 before DEC-788 |
| Part 11.13b AU-143, CONFLICT-983 | Benchmark proposal superseded by §11.19.5.7 |
| Part 4.1 §4.3 (sessions, MFA), §4.6 (secrets); Part 4.3 (environments) | Platform floors that tenant policy may only tighten |
| RFC 7643/7644 (SCIM), SAML 2.0 Core and Bindings, OpenID Connect Core 1.0, RFC 6749/7523/7636 (OAuth, JWT bearer/client assertion, PKCE), RFC 9457 (problem details), RFC 9110 (HTTP) | Protocol conformance; versions verify at time of implementation (as of 27 Nov 2026) |
| TRAI Telecom Commercial Communications Customer Preference Regulations (TCCCPR, DLT), DPDP Act 2023 and Rules, GDPR Art. 28/44–49 | Legal basis of gates; the jurisdiction packs of Part 11.15 hold the counsel-approved wording; verify current text at implementation (as of 27 Nov 2026) |

---

## 11.19.2 Coverage summary

{{COV_SUMMARY}}

**Reading the result.** Before this part, {{PENDING_N}} of the core aspects were *specified* but **Pending Founder decision** on timing or scope (Conflict), and a further group were *partially covered* (designed, but scheduled for R2/R3 or limited by DEC-421 wording). After this part every aspect is **Matched**: the Founder decisions settle timing and scope, and §11.19.5 supplies the remaining design depth (sequence diagrams, configuration, DDL deltas, APIs, events, runbooks, controls, cut-over, stories and tests). No aspect is left "Pending Founder decision" and none is "Not applicable".

---

## 11.19.3 Detailed register

### 11.19.3.1 Conflict and partially covered aspects (each listed individually)

The table lists every core aspect whose status before this part was *Conflict* or *Partially covered*. "Owner before" is the earlier blueprint location; "Resolved by" names the section of this part and the IDs created.

{{REGISTER}}

### 11.19.3.2 Covered aspects (grouped)

{{REGISTER_GROUPED}}

---

## 11.19.4 Catalogue reconciliation

### 11.19.4.1 V12 phase versus blueprint release after DEC-784…789

V12 FSD ch. 39 defines phases R0–R5 and states that durations are not estimated. Part 11.8b mapped V12-R1 to Release 1 and V12-R2 to Release 2 pending the Founder (ASSUMPTION-893). DEC-784/785 move the items below **into Release 1** even where V12 phases them later. This is an amendment of the V12 phase column by the Founder, recorded as DEC-881 and DEC-882 and as [CONFLICT-1091] (resolved).

| V12 ID | Requirement (short) | V12 phase | Blueprint release before | Release after this part | Authority |
|---|---|---|---|---|---|
| ENT-IDN-01, 02, 04, 05, 06 | SSO, verified domains, MFA, sessions, break-glass | R1 | Release 1 pending CONFLICT-887 | **Release 1** | DEC-784 |
| ENT-IDN-03 | SCIM 2.0 provisioning and de-provisioning | **R2** | Release 2 pending CONFLICT-887 | **Release 1** | DEC-784, DEC-881 |
| ENT-ACC-01 | Custom roles | **R2** | Release 2 | **Release 1** | DEC-784, DEC-881 |
| ENT-ACC-02, 03 | SoD matrix; hash-chained audit export | R1 | Release 1 | Release 1 | DEC-784 |
| ENT-ACC-04 | SIEM streaming | R2 | Release 2 | **Release 1** (identity events only in R1; full audit stream R1 as well, since the sink is generic) | DEC-784, DEC-881 |
| ENT-ACC-05 | JIT support access | R2 | Release 2 | **Release 1** (ticket ID mandatory on DEC-056 grants) | DEC-784 |
| ENT-API-01, 03, 05 | API keys, rate limits, signed webhooks | R1 | Release 1 pending CONFLICT-886 | **Release 1** | DEC-785 |
| ENT-API-02 | OAuth 2.0 client credentials | **R2** | Release 2 | **Release 1** | DEC-785, DEC-882 |
| ENT-API-04 | URL versioning, 12-month deprecation | **R2** | Release 2 | **Release 1** (policy active from the first published operation) | DEC-785, DEC-882 |
| ENT-API-06 | SDKs TypeScript, Python, Java | **R3** | Release 2 (TS/Py) / W6 (Java) | **Release 1** (all three) | DEC-785, DEC-882 |
| ENT-API-07 | Developer portal with sandbox access | **R2** | Release 2 | **Release 1** | DEC-785, DEC-882 |
| ENT-DAT-04, 05 | Sandbox with synthetic data; promotion to production | **R2** | Release 2 | **Release 1** | DEC-785, DEC-899 |
| ENT-INT-01, 02, 05 | Connector framework, vault, activation gate | R1 | Release 1 pending CONFLICT-888 | **Release 1** | DEC-785 |
| ENT-INT-03, 04 | Per-connector limits and breaker; health dashboards | **R2** | Release 2 | **Release 1** (needed by the R1 connectors) | DEC-785, DEC-884 |
| INT-01 | CRM Salesforce / HubSpot / Zoho | R1 | Release 1, one provider (RECOMMENDATION-902) pending CONFLICT-776/888 | **Release 1, all three providers** | DEC-785, DEC-884 |
| INT-04 | SMS India via DLT aggregator | R1 | Release 1 pending CONFLICT-888 | **Release 1** | DEC-785 |
| INT-05 | Voice CPaaS 140/160 series | R3+ (blueprint) | W6 | **Release 1** (transport connector); AI calling per Part 11.18 (DEC-782) | DEC-785, DEC-884 |
| INT-10 | Identity provider (Okta, Entra ID, Google) | R1/R2 | Release 1/2 | **Release 1** | DEC-784, DEC-880 |
| ENT-DAT-03 | Residency India and EU at onboarding | R1–R5 | DEC-772 (EU at first EU contract) | **Release 1** for the choice and routing; EU stack provisioned at first EU contract | DEC-772, DEC-895 |
| DEC-V9-01 / ch38 V8 | Critical RPO ≤ 15 min; WAL + base backup + PITR 35 days | R1 | CONFLICT-833 | **Release 1 gate** | DEC-787, DEC-888 |
| ch16.2 MDL-R0…G1, AIX-02/03 | Provider-neutral registry and routing | R1 | DEC-418 + CONFLICT-850…853/857 | **Release 1** | DEC-788, DEC-890 |
| BR-V7-AI-05 + panel M18 | Cross-tenant benchmarks | — (panel) | W6+ A4 (AU-143) | **Release 2** build; per-cohort activation | DEC-789, DEC-893 |
| ch02 "non-owner app role", ch20/31 SEC rules | Least-privilege application role | R0 | DEC-421 wording ("service key server-side") | **Sprint 0–1** | DEC-778, DEC-894 |

### 11.19.4.2 V12 identifiers mapped to blueprint identifiers

| V12 ID family | V12 items | Blueprint IDs (earlier) | Blueprint IDs (this part) |
|---|---|---|---|
| ENT-IDN-01…06 | SSO, domains, SCIM, MFA, sessions, break-glass | FR-V12-E-010…015; FR-V12-H-036; API-V12-H-015…028; TC-V12-E-010…021 | FR-V12-R-001…016; US-01-ZR01…03; TC-V12-R-001…016, 101…382 |
| ENT-ACC-01…05 | Custom roles, SoD, audit export, SIEM, JIT | FR-V12-E-016…020; FR-V12-H-037; API-V12-H-029…032 | FR-V12-R-017…030; US-01-ZR04, ZR05; TC-V12-R-017…020, 383…406 |
| ENT-API-01…07 | Keys, OAuth CC, limits, versioning, webhooks, SDKs, portal | FR-V12-H-001…007; API-V12-H-001…014, 042 | FR-V12-R-031…055; US-20-ZR06…10; TC-V12-R-021…036, 407…537 |
| ENT-DAT-04/05 | Sandbox and promotion | FR-V12-H (H4); A204 | FR-V12-R-053…055; US-20-ZR09 |
| ENT-INT-01…05, INT-01/04/05/10 | Framework, vault, limits, health, gate; CRM, SMS, voice, IdP | CF-01…12; AD-V12-H-01/02/03/05 | FR-V12-R-056…080; US-18-ZR11, US-07-ZR12/13, US-23-ZR14, US-22-ZR15; TC-V12-R-037…050, 538…721 |
| DEC-786 (no V12 ID; V12 is host-neutral) | Vercel data path | ADR-209; CONFLICT-889 | FR-V12-R-081…095; US-21-ZR16/17; TC-V12-R-051…058, 722…767 |
| DEC-V9-01, ch38 V8, OPT-TC-ST-14, KPI-18/19/32 | RPO/RTO, WAL, PITR, drills | FR-V12-E-122…125; DR-01…05 | FR-V12-R-096…110; US-21-ZR18/19; TC-V12-R-059…066, 768…858 |
| MDL-R0, S1, M1, L1, E1, G1; AIX-02/03/20; DEC-V7-02 | Registry, routing, rollback, kill switch | FR-V12-F-002/003/037/038; AU-151/152/154 | FR-V12-R-111…130; US-04-ZR20…23; TC-V12-R-067…074, 859…1055, 1128…1172 |
| BR-V7-AI-05, panel M18 | Benchmarks | FR-V12-M-098; AU-143; API-V12-M-24 | FR-V12-R-131…142; US-17-ZR24/25; TC-V12-R-075…080, 1056…1099 |
| SEC rule "non-owner app role", ch26 RLS, C2/C3 | Database roles | SB-01…10; FR-V12-I-0xx | FR-V12-R-143…155; US-01-ZR26/27; TC-V12-R-081…086, 1100…1127 |
| Screens A122, A123, A125, A127, A128, A114, W39 | Admin identity, roles, keys/webhooks, sandbox, connectors, model registry; public developer page | Blueprint A203, A002, A168, A204, A008, A011 + Part 9.7 A115, W47 (Part 11.7a mapping; V12 IDs collide with Part 9.7) | Unchanged screen IDs; new tabs specified per capability |

### 11.19.4.3 Appendix A2 and C2 objects used by this part

| V12 object | Kind | Where specified in full | Change made here |
|---|---|---|---|
| `GET/PUT /tenants/{id}/sso`, SCIM `Users`/`Groups` (7 ops), `POST /roles` (SoD checked), `POST /api-keys`, `POST /webhooks` | Appendix A2 operations | Part 11.8b §11.8.5.5 (API-V12-H-001…032) | Region-qualified hosts; problem-detail codes added (§11.19.5.1.E, §11.19.5.2.D) |
| `identity_provider`, `scim_token`, `custom_role`, `role_permission`, `sod_conflict`, `api_key`, `webhook_endpoint`, `webhook_delivery`, `audit_sink`, `sandbox_environment`, `config_promotion`, `connector_installation` | Appendix C2 tables | Part 11.9b C3 (RLS, composite FKs, checks) | DDL-V12-R deltas: multi-connection IdP, certificates, OAuth clients, secret versions, delivery schedule, connector mappings, CRM sync state, DLT registry (§11.19.5.1.D–§11.19.5.3.D) |
| `ai_model` | Appendix C table | Part 11.6b §11.6.5.6; Part 11.9b `ai_model_tier_ck`, `ai_model_t2_data_ck` | Registry columns for hosting, processing regions, approvals, re-certification and modality (Part 11.19b §11.19.5.6.D) |
| (none in V12) | Benchmarks | Part 11.13b `benchmark_cell` | `benchmark_enrolment`, `benchmark_contribution`, `benchmark_cell`, `benchmark_privacy_ledger` (Part 11.19b §11.19.5.7.D) |
