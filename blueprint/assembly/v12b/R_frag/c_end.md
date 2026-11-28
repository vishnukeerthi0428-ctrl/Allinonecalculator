
---

## 11.19.6 Conflicts and proposed resolutions

All conflicts that earlier groups raised on these topics are closed by the Founder decisions; this part records how each is implemented. The new conflicts (1091–1095) are differences between earlier blueprint text and the decisions; each is resolved here, none is pending.

| Conflict | Subject | Earlier position | Resolution implemented | Status |
|---|---|---|---|---|
| CONFLICT-760 / 834 / 887 | Enterprise identity scope and timing | Specified; SCIM and custom roles R2; Release 1 budget fixed | DEC-784 → all in Release 1 (DEC-880, 881, 898); §11.19.5.1 | Resolved |
| CONFLICT-886 | Developer platform timing | ENT-API R1/R2/R3 | DEC-785 → all in Release 1 (DEC-882, 883, 899); §11.19.5.2 | Resolved |
| CONFLICT-888 / 776 | Connector kinds; X-09 CRM exclusion | One CRM in R1 pending; SMS pending; voice W6 | DEC-785 → three CRMs, SMS-DLT, voice transport in Release 1 (DEC-884, 885); §11.19.5.3 | Resolved |
| CONFLICT-889 | Personal data through Vercel | DEC-421 "no personal data in functions"; option A recommended | DEC-786 → regional projects, controls VD-01…12, DEC-886/887; §11.19.5.4 | Resolved |
| CONFLICT-833 | RPO 15 min, WAL, PITR 35 days | Daily backups; PITR at growth gate | DEC-787 → dual path P1 + P2 (DEC-888/889); §11.19.5.5 | Resolved |
| CONFLICT-850, 851, 853, 855, 857 (852 via DEC-772) | Provider-neutral registry; MDL-S1 open-weight; MDL-L1 and multimodal; 111 suites; fallback rule | DEC-418 Claude-only routing; Tier 2 free | DEC-788 → registry with zone routing and Claude Sonnet approved primary (DEC-890…892); §11.19.5.6 | Resolved |
| CONFLICT-983 | Cross-tenant benchmarks | AU-143 proposal, pending | DEC-789 → C7 with DP (DEC-893); §11.19.5.7 | Resolved |
| [CONFLICT-1091] | V12 phases SCIM, custom roles, SIEM, JIT (R2), OAuth CC, portal, sandbox, versioning (R2), SDKs (R3) vs DEC-784/785 "Release 1" | V12 phase column | Founder decision prevails; phase column amended for the blueprint (§11.19.4.1); V12 IDs and acceptance unchanged | Resolved (DEC-881, 882) |
| [CONFLICT-1092] | Database role names: DEC-778 "one canonical name `app_rw`" vs Part 11.9b DDL `ge_app`/`ge_worker`/`ge_owner` | Part 11.9b SB-04 | Canonical `app_*` names; idempotent rename DDL-V12-R-16; Part 11.9b not edited (reported) | Resolved (DEC-894) |
| [CONFLICT-1093] | Part 11.8b scope registry text "consequential actions stay capped at L1" vs DEC-779 bounded mandates | Part 11.8b §11.8.5.4 | API still has no consequential scope; consequential execution only through the Part 11.17 mandate engine, never by API scope | Resolved (DEC-883) |
| [CONFLICT-1094] | Part 11.9b `ai_model_t2_data_ck` (tier T2 non-personal) cannot express DEC-788 open-weight masked personal | Part 11.9b C3 | Hosting-based checks replace tier-based check (DDL-V12-R-14); free third-party still non-personal only | Resolved (DEC-890) |
| [CONFLICT-1095] | AU-143 parameters (ε = 1, W6+/A4, k ≥ 10) vs DEC-789 implementation | Part 11.13b | AU-299 supersedes AU-143: ε = 0.5 per metric per month, yearly cap 6, reciprocity, zone-local computation, Release 2 | Resolved (DEC-893) |

---

## 11.19.7 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-880 | Tenant federation uses the reused IdP as broker per connection; Okta, Entra ID, Google Workspace certified plus generic SAML 2.0 and OIDC; up to 5 connections per tenant; fallback in-product SP behind a flag if Sprint 0 check 13 fails | Customer revision V12 (28 Nov 2026); implements Founder DEC-784 | ADR-255; §11.19.5.1 |
| DEC-881 | SCIM 2.0, custom roles, SIEM streaming and JIT support access move into Release 1; de-provisioning ≤ 60 s product side and ≤ 15 min end to end (binding); group-to-role mappings need a second approver | Customer revision V12 (28 Nov 2026); implements Founder DEC-784 | Amends the V12 phase column (CONFLICT-1091) |
| DEC-882 | Developer platform fully in Release 1: zone-bound API keys, OAuth client credentials (private_key_jwt preferred), rate limits, URL versioning with 12-month notice, signed webhooks with fixed 24 h schedule, portal, SDKs in TypeScript, Python and Java | Customer revision V12 (28 Nov 2026); implements Founder DEC-785 | ADR-257/258 |
| DEC-883 | No API scope exists for consequential actions; consequential execution happens only by a human with step-up or under a Part 11.17 bounded mandate | Customer revision V12 (28 Nov 2026); consistent with DEC-779 | Closes CONFLICT-1093 |
| DEC-884 | Connectors in Release 1: framework and gate (with counsel-approved rule pack per market), CRM adapters for Zoho CRM, HubSpot and Salesforce (all BYO), SMS via a DLT-registered aggregator, voice CPaaS transport (140/160 series) | Customer revision V12 (28 Nov 2026); implements Founder DEC-785 | Supersedes RECOMMENDATION-902; ADR-259 |
| DEC-885 | Platform is system of record for consent, suppression, approvals, mandates, audit and AI outputs; CRM opt-outs import as suppression; other fields by per-field policy with a conflict queue | Customer revision V12 (28 Nov 2026) | DDL protected-field check |
| DEC-886 | Vercel: one project per surface per zone, functions pinned to bom1/fra1 (verify), Edge Middleware non-personal only, header allowlist, origin verify, metadata-only logs, no caching of personal responses, VD-01…12 enforced by CI and AU-296 | Customer revision V12 (28 Nov 2026); implements Founder DEC-786 | Amends DEC-421 hosting statement; ADR-260 |
| DEC-887 | TLS termination at a Vercel edge location outside the zone is treated as transit; storage and processing stay in-zone; the position is written into the IN and EU rule packs and needs counsel sign-off before the first EU tenant | Customer revision V12 (28 Nov 2026); legal gate per Part 11.15 | GAP-1088 |
| DEC-888 | RPO ≤ 15 min through two independent paths per zone: Supabase PITR and an in-zone AWS standby with WAL-G continuous archiving and daily base backups; drills at each release gate and quarterly | Customer revision V12 (28 Nov 2026); implements Founder DEC-787 (and DEC-771) | ADR-261 |
| DEC-889 | The 35-day PITR window is guaranteed by the WAL-G archive when the Supabase option is shorter; archives replicate only inside the zone | Customer revision V12 (28 Nov 2026) | ASSUMPTION-1081 |
| DEC-890 | Registry rows by provider × version × hosting × zone × modality; seven evidence items; two distinct approvers; 12-month re-certification and event triggers (AU-298); Tier 2 free rows only if they pass the same gate and only for non-personal data | Customer revision V12 (28 Nov 2026); implements Founder DEC-788 | Resolves CONFLICT-857/1094; ADR-262 |
| DEC-891 | Model routing is zone-aware: EU tenants only to rows with EU processing; India tenants only to rows permitted for India; otherwise HOLD/Tier 3, never cross-zone | Customer revision V12 (28 Nov 2026); DEC-772 | ASSUMPTION-1083 |
| DEC-892 | Advanced tier (MDL-L1) and multimodal rows (image, video, voice) are registered and activate on approval; Claude Sonnet remains primary for MDL-M1 by Founder approval | Customer revision V12 (28 Nov 2026); implements Founder DEC-788 | — |
| DEC-893 | Benchmarks: opt-in under clause BM-CL-1, reciprocity, k ≥ 10, dominance ≤ 30%, tenant-level DP with Laplace ε = 0.5 per metric per cell per month (yearly cap 6), zone-local computation, Owner Portfolio excluded unless R01 opts in; built in Release 2 | Customer revision V12 (28 Nov 2026); implements Founder DEC-789 | Supersedes AU-143 parameters; ADR-263 |
| DEC-894 | Canonical database roles `app_owner`, `app_migrator`, `app_rw`, `app_worker`, `app_readonly`, `app_retention`, `app_platform_sec`, `app_bench`, `app_registry`; all NOBYPASSRLS; Data API off; `service_role` only for CI migrations under two-person, time-boxed break-glass | Customer revision V12 (28 Nov 2026); implements DEC-778 | Resolves CONFLICT-1092; ADR-264 |
| DEC-895 | A global, non-personal tenant directory resolves the zone before any personal data is processed; misdirected requests get 421 and are never proxied across zones; residency is chosen at onboarding | Customer revision V12 (28 Nov 2026); DEC-772/776 | §11.19.5.0 |
| DEC-896 | Feature flags per capability default off until each activation gate passes; owned startups adopt SSO and connectors first | Customer revision V12 (28 Nov 2026) | §11.19.5.12 |
| DEC-897 | Proposal CR-V12-R-01: net development 120 / 176 / 253 pd (₹5.45 / 10.00 / 17.25 L), external ₹4.6–10.8 L, running ₹15,300–54,000 per month per zone (excluding the conditional open-weight line); funded under DEC-790 | Customer revision V12 (28 Nov 2026); funding by Founder DEC-790 | Development and running in separate tables (§11.19.5.13) |
| DEC-898 | SoD matrix extended by eight pairs (finance dual verification, billing, roles, mandates, connectors, models, benchmarks, unmasked scopes); quarterly access recertification | Customer revision V12 (28 Nov 2026); implements Founder DEC-784 | §11.19.5.1.F |
| DEC-899 | Sandbox tenants (synthetic only) and configuration promotion in Release 1 | Customer revision V12 (28 Nov 2026); implements Founder DEC-785 | ENT-DAT-04/05 |

---

## 11.19.8 Expert persona review

| Persona | Verdict | Findings and how they were addressed |
|---|---|---|
| Identity architect (SAML/OIDC, SCIM, SoD) | Approve | Insisted on XSW corpus testing, assertion-ID replay cache, `amr`-based MFA acceptance and step-up, break-glass with hardware keys, no auto-unenforce on DNS loss, group mappings with second approver, SoD at four enforcement points including the DB trigger. All present (§11.19.5.1, TC-V12-R-001…020, M01–M03). Residual risk: broker capability (RSK-V12-R-01) with flagged fallback |
| Developer-platform product lead | Approve | Zone in key format avoids cross-region lookup; private_key_jwt preferred; webhook verification challenge and SSRF re-check per delivery; SDKs generated with thin helpers to keep three languages maintainable; deprecation 12 months. Asked for SDK provenance (RECOMMENDATION-1097) and leak-response partner registration (RECOMMENDATION-1098) |
| Integration architect (CRM, SMS-DLT, voice) | Approve with conditions | Platform must stay authoritative for consent (DEC-885, DDL check); Salesforce edition limits are real (ASSUMPTION-1086); DLT IDs and scrubbing must be enforced in the PDP, not only in the adapter (done); voice series/purpose check in DDL. Condition: DLT registration starts in Sprint 0 (RSK-V12-R-03) |
| Privacy and cloud-security lead | Approve with condition | Per-zone projects and VD rules make DEC-786 enforceable; condition: counsel opinion on edge transit before the first EU tenant (DEC-887, GAP-1088), and Vercel analytics features kept off on authenticated surfaces |
| Database reliability engineer | Approve | Dual path removes single-provider dependence; logical replication caveats (DDL, sequences) handled; RPO measured every 30 s; drills produce evidence; canonical roles with CI assertions close the RLS bypass (DEC-778) |
| LLM platform lead | Approve | Registry rows include hosting and zone, so open-weight masked personal and free-tier non-personal are expressible as DB checks; zone-aware routing prevents silent transfer; Claude Sonnet primary recorded as an approval, not hard-coded |
| Privacy-preserving analytics scientist | Approve with condition | Tenant-level DP with clipping is stronger than k-anonymity alone; ε = 0.5 monthly with a yearly cap is conservative for 5 metrics; global cells by post-processing; condition: independent re-derivation before first publication (budgeted) |

---

## 11.19.9 Tags register

### 11.19.9.1 Tags issued in Part 11.19 (range 1080–1099, all used)

| Tag | Type | Statement | Where |
|---|---|---|---|
| [ASSUMPTION-1080] | Assumption | The reused AppNAI IdP can broker per-tenant SAML/OIDC with issuer/audience binding and `amr` passthrough; verified by Sprint 0 check 13; otherwise in-product SP | §11.19.5.1.A |
| [ASSUMPTION-1081] | Assumption | Supabase PITR retention options and granularity (possibly < 35 days); verify at time of implementation (as of 27 Nov 2026) | §11.19.5.5 |
| [ASSUMPTION-1082] | Assumption | Vercel function region identifiers `bom1`/`fra1`, region-pinning mechanism and log-content behaviour; verify (as of 27 Nov 2026) | §11.19.5.4 |
| [ASSUMPTION-1083] | Assumption | Model providers offer EU and/or India processing locations (directly or via cloud marketplaces); verify per row | §11.19.5.6 |
| [ASSUMPTION-1084] | Assumption | "Opt-in default" in DEC-789 means participation is off until the tenant opts in under the clause | §11.19.5.7 |
| [ASSUMPTION-1085] | Assumption | Benchmarks are built in Release 2 because cohorts of 10 tenants cannot exist before external tenants onboard | §11.19.0 |
| [ASSUMPTION-1086] | Assumption | CRM API access, change capture and limits depend on the tenant's edition (e.g. Salesforce API-enabled editions); verify | §11.19.5.3 |
| [ASSUMPTION-1087] | Assumption | The DLT aggregator offers scrubbing and template validation APIs; TRAI promotional window 10:00–21:00 IST; verify current regulations | §11.19.5.3 |
| [GAP-1088] | Gap | Legal position on TLS termination at out-of-zone edge locations needs counsel opinion (IN, EU) | DEC-887 |
| [GAP-1089] | Gap | AI voice behaviour on top of VoicePort is specified by Part 11.18; this part supplies the transport contract only | §11.19.5.3 |
| [GAP-1090] | Gap | Supabase dashboard SSO/MFA and organisation roles depend on the plan; confirm at implementation | SA-10 |
| [CONFLICT-1091] | Conflict | V12 phases vs Release 1 decisions | §11.19.6 (resolved) |
| [CONFLICT-1092] | Conflict | Role names `app_rw` vs `ge_app` | §11.19.6 (resolved) |
| [CONFLICT-1093] | Conflict | Part 11.8b "L1 cap" wording vs DEC-779 | §11.19.6 (resolved) |
| [CONFLICT-1094] | Conflict | `ai_model_t2_data_ck` vs DEC-788 open-weight masked personal | §11.19.6 (resolved) |
| [CONFLICT-1095] | Conflict | AU-143 parameters vs DEC-789 implementation | §11.19.6 (resolved) |
| [RECOMMENDATION-1096] | Recommendation | Hardware security keys for break-glass accounts | §11.19.5.1.A |
| [RECOMMENDATION-1097] | Recommendation | Signed SDK releases with registry provenance (npm provenance, PyPI trusted publishing, Maven Central signing; verify) | §11.19.5.2.A |
| [RECOMMENDATION-1098] | Recommendation | Register the `gek_` prefix with secret-scanning partner programmes (verify availability) | §11.19.5.2.A |
| [RECOMMENDATION-1099] | Recommendation | Use a vetted open-source DP library (e.g. OpenDP or Google's differential-privacy library; licence verify) for noise and accounting | §11.19.5.7 |

### 11.19.9.2 Inconsistencies found in earlier parts (reported, not edited)

| # | Part | Inconsistency | Handling here |
|---|---|---|---|
| 1 | Part 11.9b SB-04 and DDL | Role names `ge_app`/`ge_worker`/`ge_owner` vs DEC-778 canonical `app_rw` | Rename migration DDL-V12-R-16 (CONFLICT-1092) |
| 2 | Part 11.8b §11.8.5.4 | "Consequential actions stay capped at L1" predates DEC-779 | DEC-883 wording (CONFLICT-1093) |
| 3 | Part 11.9b C3 | `ai_model_t2_data_ck` tier-based | Replaced by hosting-based checks (CONFLICT-1094) |
| 4 | Part 11.8b §11.8.5.10 | Database row "service key server-side" | Superseded by DEC-778/894 |
| 5 | Part 11.13b AU-143, API-V12-M-24 | Benchmarks "disabled until DEC-747", ε = 1 | Superseded by AU-299, API-V12-R-051 |
| 6 | Part 11.8b AD-V12-H-03 | Voice "R3+ → W6" | Release 1 transport (DEC-884) |
| 7 | Part 11.5a ENT-IDN-01 data model | One `IdpConnection` per tenant in V12 C2 vs multi-connection | Compatibility view (FR-V12-R-029) |

---

## 11.19.10 Quality gate: Batch 11.19 (files a, b and c)

| # | Item | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | **Pass** | {{ASPECTS}} V12 aspects in `final/coverage_v12/R_coverage.csv`; 155 FRs with source; every story and TC links FR/ENT/DEC |
| 2 | Assumptions/gaps/conflicts tagged and logged | **Pass** | 20 tags 1080–1099, all registered §11.19.9.1 |
| 3 | IDs unique and consistent with earlier parts | **Pass** | DEC-880…899, ADR-255…264, AU-290…299, FR-V12-R-001…155, US-<EP>-ZR01…29, TC-V12-R-001…086 and 101…{{LAST_TC_NUM}}; screen IDs per Part 11.7a mapping |
| 4 | No story lacks AC; no requirement lacks a test | **Pass** | 29 stories with Gherkin; every FR names a TC or model |
| 5 | Negative, edge, security and accessibility cases | **Pass** | {{TOTAL_TC}} test cases; P0 negative and security rows in every model; accessibility AC-20ZR09-05 and strategy row |
| 6 | No agent lacks guardrail, fallback, KPI, cost | **Pass / N/A** | No new agents; AU-290…299 complete |
| 7 | Time-sensitive facts flagged "verify" | **Pass** | Provider features, regions, prices, TRAI windows, model IDs (as of 27 Nov 2026) |
| 8 | No restricted data routed to free-tier models | **Pass** | DDL `ai_model_free_tier_data_ck`; M10 oracle rows for Restricted/Personal never route to free or open-weight unmasked |
| 9 | Consistent with earlier parts | **Pass with reported items** | §11.19.9.2 |
| 10 | V12-B combinatorial rule (pairwise for all; 3-way for safety/money/law; exhaustive ≤ 64) | **Pass** | 13 models: 8 × 3-way, 3 × pairwise, 2 × exhaustive; script `assembly/v12b/R_02_combinatorics.py` |
| 11 | Mermaid renders | **Pass** | 0 diagram errors in the three PDFs |

**Status: Part 11 Batch 11.19 (files a, b, c) complete. Founder decisions DEC-778 and DEC-784…789 implemented at full depth: {{ASPECTS}} V12 aspects Matched, 155 FRs, 29 stories, {{TOTAL_TC}} test cases (86 full form + {{GEN_TC}} generated from 13 combinatorial models), 10 automations, 20 decisions, 10 ADRs; no item pending.**
