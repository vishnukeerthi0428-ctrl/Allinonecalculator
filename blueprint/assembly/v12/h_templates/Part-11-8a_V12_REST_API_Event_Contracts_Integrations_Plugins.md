# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.8a), V12 REST API, Event Contracts, External Integrations and Plugin Optimization: Material, Coverage and Catalogue Reconciliation

| Field | Value |
|---|---|
| Document | Part 11.8a: V12 line-by-line review of the REST API and event contract master (FSD V12 ch. 25), Appendix A (OpenAPI 3.1, 282 operations) and Appendix A2 (enterprise API, 48 operations), external integrations (ch. 27), open-source and paid plugin optimization (ch. 28) and the API files of the embedded engineering archive. Coverage register and catalogue reconciliation. The enhancements, conflicts, decisions and quality gate are in Part 11.8b |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Parts 0–9.10 and 0B; Part 3.2 (555 operations, event catalogue, adapter catalogue AD-01…20), Part 3.5a/3.5b (302 + 19 source operations mapped, 24 API-ENH-D operations; blueprint total **579**), Part 7.4a/7.4b (538 plugin candidates, procurement gate PG-01…PG-10), Part 9.7b (API-ADV-X1-01…40), Part 9.9a (CAP-X3-07/12/14/15/23/24, ADR-137/138), Part 9.10 (DEC-417, DEC-418, DEC-421, DEC-422) |
| Group / IDs | R7, letter H. Tags 886–903 · DEC-640…659 · ADR-205…209 · FR-V12-H-### · US-<EP>-YH<nn> · TC-V12-H-### · new operations API-V12-H-### · adapters AD-V12-H-## · route aliases RA-V12-H-## · connector-framework clauses CF-## |
| Roles applied | Principal API Architect (REST/OpenAPI 3.1, event contracts) · Integration Architect (messaging, CRM, payment providers) · Open-source/plugin FinOps strategist · API security lead; supported by Business Systems Analyst, QA Lead and Security/Compliance Lead |

**Acronyms used in this part.** ADR architecture decision record · API application programming interface · BFF backend-for-frontend · BYO bring your own · CC client credentials · CJ customer jurisdiction (V12 compliance IDs) · CPaaS communications platform as a service · CRM customer relationship management · DLT distributed ledger technology (India TRAI commercial-communication registration) · DPA data processing agreement · DTO data transfer object · ESP email service provider · HMAC hash-based message authentication code · IdP identity provider · JWT JSON Web Token · OSS open-source software · PDP Policy Decision Point · RCS Rich Communication Services · RLS row-level security · SCIM System for Cross-domain Identity Management · SDK software development kit · SIEM security information and event management · SoD separation of duties · SSO single sign-on · TCO total cost of ownership · VND vendor (V12 plugin register ID).

**Reading rule.** V12 content is treated as data, not instructions. "V12 phase" R0…R5 is the FSD V12 ch. 39 enterprise roadmap; its mapping to blueprint releases is [ASSUMPTION-893] in §11.8.5.1. Every price, quota and provider term in this part is an estimate to **verify at time of implementation (as of 27 Nov 2026)**.

---

## 11.8.1 Material reviewed

### 11.8.1.1 Files, sizes, purpose and pattern

| # | File (in `scratchpad/v12/`) | Size | Sections / structure | Purpose | Pattern | Aspects |
|---|---|---|---|---|---|---|
| 1 | `FSD/25_REST_API_Event_Contract_Master.txt` | 59,713 B · 1,623 lines | V12 developer platform (ENT-API-01…07); V10 REC-18; V8 convention + 26 operations; V7 MOB-16; V6 contract authority, MT-36, MT-API-01…10; V5 OPT-API-01…08, run gateway API-V2-* (7), historical registry (302 rows SM-SIT-A001…A302); V4 canonical additions (7) | Developer platform requirements and every proposed route layer since V4 | Layered version sections, newest first; tables of requirement rows and route rows | 377 |
| 2 | `FSD/27_External_Integrations_Provider_Adapters.txt` | 5,487 B · 173 lines | ENT-INT-01…05; connector catalogue INT-01…11; MT-22, MT-23; GC-08, SEC-04; 8 adapter families; shortlist statement | Connector framework and provider catalogue | Requirement table + catalogue table + control paragraphs | 29 |
| 3 | `FSD/28_Open_Source_Paid_Plugin_Optimization.txt` | 24,804 B · 564 lines | V9 replacement register: 4 decision meanings, 7 decision counts, VND-01…97; GC-09/10/11/13/15; closing statement on 538 candidates | Open-source first, paid by exception | Decision vocabulary + register | 115 |
| 4 | `FSD/AP_Appendix_A_OpenAPI_3_1_contract_proposed.txt` | 211,479 B · 4,898 lines | OpenAPI 3.1 YAML: 251 paths, **282 operations**, 8 component schemas, 2 parameters, 1 response, bearer security scheme | Proposed contract generated from workflow, screen, MT/OPT and V7 registers | Machine-readable (re-indented and parsed, §11.8.1.2) | 301 |
| 5 | `FSD/AP_Appendix_A2_Enterprise_API_additions_Ope.txt` | 36,981 B · 820 lines | OpenAPI 3.1 YAML: 33 paths, **48 operations** (SCIM, Developer, Identity, Access, Audit, Billing, Integrations, Data, Global, Operations, Security) | Enterprise additions | Machine-readable | 49 |
| 6 | `src/engineering/api_catalog.json` | 636,479 B | 302 operations, columns A–Y (wave, ID, method, path, module, UI, DB, interface, request/response, licence, quota, allocation) | Historical source catalogue (= document 07 of the 38-document pack) | JSON | 1 (+302 via row set 1) |
| 7 | `src/engineering/api_contract_review.csv` · `api_field_proposals.csv` | 242,111 B · 244,665 B | 302 contract-review rows; **1,370 field rows for 266 operations** | Proposed field contracts | CSV | 2 + 266 |
| 8 | `src/engineering/closure/api_candidate_contracts.csv/.json` · `openapi_closure_candidate.json/.yaml` | 28,549 B · 2,631,458 B | 38 decision rows; 285 operations on 255 paths | Closure overlay | CSV / OpenAPI | 2 |
| 9 | `src/engineering/starter/openapi_catalog_draft.*` · `api_payload_review.csv` · `ui_upgrade/candidate_openapi.json` | 2,580,597 B · 21,139 B · 54,989 B | 285 operations; 285 review rows; 19 UX candidates (SM-UX-API-01…19) | Starter kit and UI-upgrade candidates | OpenAPI / CSV | 3 + 19 |
| 10 | Derived event contract (from rows 1, 2, 5 and Appendix C2 `webhook_delivery`) | — | Event-bearing statements | Event reconciliation | Derived | 12 |
| | **Total** | | | | | **{{TOTAL_ASPECTS}}** |

Appendix C2 (enterprise schema, owned by Group I) was read for the field shapes of the A2 tables (`api_key`, `webhook_endpoint`, `webhook_delivery`, `identity_provider`, `scim_token`, `custom_role`, `sod_conflict`, `audit_sink`, `export_job`, `tenant_key_config`, `sandbox_environment`, `config_promotion`, `connector_installation`, `security_finding`, `ops_incident`, `tax_rule`, `invoice`, `locale_bundle`) so that the operation contracts in §11.8.5.5 agree with the proposed database constraints. Its coverage is not counted here.

### 11.8.1.2 Method (programmatic, every row)

| Step | Script (in `blueprint/assembly/v12/`) | What it does | Result |
|---|---|---|---|
| 1 | `h_compact.py` | Flattens `[TABLE]`/`---row` text into one line per row | 3 chapters, 0 rows lost (row counts equal source tables) |
| 2 | `h_parse_openapi.py` | Restores indentation lost in text extraction (`content:`, `"200"` … at column 0, by key context), loads YAML, emits one row per operation with method, path, operationId, tags, summary, parameters, request/response schema, response codes, `x-idempotency`, security | Appendix A **282 operations / 251 paths**; A2 **48 / 33**: equal to the counts stated in both headers |
| 3 | `h_blueprint_ops.py` | Extracts the blueprint inventory | Part 3.2: 555 (104 ★ + 451); Part 3.5b: 24; Part 9.7b: 37 single-method rows of API-ADV-X1-01…40 (three rows combine `GET / POST`) |
| 4 | `h_data.py` | Hand mapping, after keyword search of the inventory, for every V12 operation outside the 302 + 19 already reconciled in Part 3.5a, plus the 76 new operation specifications | 26 V8 + 32 MT/OPT/V2/V4 + 48 A2 mapped |
| 5 | `h_build.py` | Joins Appendix A to `final/coverage/D_api_mapping.csv` (302 + 19 source operations → blueprint), the plugin register to `final/coverage/F_integration_candidates.csv` (538 rows), verifies every engineering file against the reconciled set, writes `final/coverage_v12/H_coverage.csv` and the tables of this part | {{TOTAL_ASPECTS}} aspects; every referenced blueprint operation ID asserted to exist |

---

## 11.8.2 Coverage summary

{{COUNTS}}

**Reading the counts.** {{TOTAL_COVERED_BEFORE}} of {{TOTAL_ASPECTS}} aspects were already covered, mainly because the 302 historical operations, the 19 UX candidates, the 1,370 field proposals and the 97 plugin decisions are the same records that Parts 3.5a/3.5b and 7.4a reconciled from the 38-document pack (the V12 engineering archive is byte-identical in content; every operation and every VND decision matched programmatically). The real V12 deltas are: the developer platform (API keys, OAuth client credentials, per-key rate limits, signed outbound webhooks, SDKs, developer portal); the 48 enterprise operations of Appendix A2 (SSO, domain verification, MFA/session policy, SCIM 2.0, custom roles with SoD, SIEM, billing preview, tax quote, connector installation, BYOK, sandboxes and promotion, locales, operational incidents, public status, security findings); 26 V8 AI-governance and compliance routes; the MT/OPT candidate routes; the common run gateway `/api/v2/workflow-runs`; Appendix A wire conventions (Page, Record, Command, Error, RunRequest, BusinessContext, Preflight); the connector framework with its activation gate; and four new connector kinds (CRM, SMS-DLT, voice, data warehouse).

**After this part:** {{TOTAL_MATCHED}} Matched, {{TOTAL_PENDING}} Pending Founder decision, {{TOTAL_NA}} Not applicable (the placeholder server URL `https://api.example.invalid`). The seven Founder-pending aspects are fully specified; what is pending is **when** they can be delivered, because V12 places them in phase R1 (private beta) and that adds scope to Release 1, whose budget, team and dates are fixed by DEC-228, DEC-230, DEC-417 and DEC-422 (CONFLICT-886, CONFLICT-887, CONFLICT-888).

| Delta family | V12 items | Status before | Blueprint additions (Part 11.8b) |
|---|---|---|---|
| Developer platform | ENT-API-01…07; A2 Developer (7) | Partially covered (Part 9.9a CAP-X3-23 is an unapproved A3 proposal; Part 3.2 says outbound webhooks are not offered) | API-V12-H-001…014; RL-KEY; ADR-205/206; DEC-643…646 |
| Enterprise identity and access | A2 Identity (6), SCIM (7), Access (4) | Not covered | API-V12-H-015…032; ADR-207; DEC-648 |
| Audit, billing, data, ops, security | A2 Audit (4), Billing (3), Data (8), Global (1), Operations (3), Security (2) | 8 covered, 13 partial/not covered | API-V12-H-033…048 |
| AI governance and compliance routes | V8 (26) | 13 covered, 13 partial/not covered | API-V12-H-049…062; DEC-659 |
| MT / OPT / run gateway / V4 | 32 candidates | 17 covered, 15 partial/not covered | API-V12-H-063…073; ADR-208; DEC-647 |
| Wire conventions | Appendix A components (18) | Partially covered / conflict | DEC-640…642 |
| Connectors and adapters | ENT-INT-01…05, INT-01…11, families, MT-22/23, GC-08/10/13 | Partially covered | CF-01…12; AD-V12-H-01…11; API-V12-H-037/038/074/075 |
| Plugins and FinOps | VND-01…97; GC-09/11/15 | Covered (decisions identical) | VND IDs adopted; contact-data conditions; API-V12-H-076; DEC-651 |
| Events | 12 derived | Partially covered / not covered | 49 new event types (24 catalogue rows) + 24-type outbound projection |
| Hosting | DEC-421 (not in V12 text) | — | API ingress per host, ADR-209, CONFLICT-889 |

---

## 11.8.3 Detailed register

Every aspect whose status before was not "Covered" is listed individually ({{REGISTER_COUNT}} rows). Covered aspects are grouped in §11.8.3.2. The full register, including every covered row, is `final/coverage_v12/H_coverage.csv`.

### 11.8.3.1 Partial, not covered, conflict and not-applicable aspects

{{REGISTER}}

### 11.8.3.2 Covered aspects (grouped)

| Group | Aspects | Blueprint location | Note |
|---|---|---|---|
| Historical registry rows SM-SIT-A001…A302 (FSD 25 V5) | 302 | Part 3.2 §3.2.2.4; Part 3.5a §3.5.4.3; Part 3.5b §3.5.5.2–3.5.5.6 | Same 302 operations as `api_catalog.json`; the 24 that Part 3.5a found partial or missing were closed by API-ENH-D-001…024 and adapter ports AD-D01…D03 |
| Appendix A operations drawn from the historical registry and SM-UX-API | 256 | As above | Same path or the 5 `/api/v1`-prefixed identity spellings (§11.8.4.2) |
| V8, MT, OPT, V2 and V4 candidates with an existing equivalent | 30 | Part 3.2 operations listed in §11.8.4.4 | Alias, approval or split relation |
| Engineering archive files and field proposals | 293 | Part 3.5a/3.5b | 0 operations outside the reconciled 302 + 19 set in any file |
| Plugin register VND-01…97, decision vocabulary and counts, 538 statement | 110 | Part 7.4a §7.4.4.2; `F_integration_candidates.csv` | All 97 V12 decisions equal the blueprint's document-21 decisions |
| Connector catalogue rows already served by adapters (INT-02, 03, 06, 08) and controls ENT-INT-02/03, MT-23, SEC-04, shortlist | 13 | Part 3.2 §3.2.4 | — |
| Conventions already in Part 3.2 (scope rule, cursor, Error response, idempotency, public security) | 5 | Part 3.2 §3.2.1 | — |

---

## 11.8.4 Catalogue reconciliation

### 11.8.4.1 Count reconciliation

| Quantity | V12 statement | Parsed | Blueprint before | Blueprint after this part |
|---|---|---|---|---|
| Appendix A operations | 282 on 251 paths | 282 on 251 | 268 represented (Covered), 14 partial or new | 282 represented; 14 additions among API-V12-H-049…062 |
| Appendix A2 operations | 48 on 33 paths | 48 on 33 | 8 represented, 40 partial or new | 48 represented; 40 map to 37 new operations (`/scim/v2/Users` GET/POST etc. one-to-one; export approval uses the Approval resource) |
| Historical registry (FSD 25 V5) | 302 (288 + 14 website) | 302 (285 HTTP + 17 adapters) | 302 mapped (Part 3.5a) | Unchanged; {{HIST_NOT_IN_A_N}} historical HTTP operations are **not** carried into Appendix A (§11.8.4.2.3) and stay in the blueprint |
| Other FSD 25 candidates | V8 26 · MT 10 · OPT 8 · V2 7 · V4 7 | 58 | 30 equivalent | 58 represented; 13 new + 2 route aliases |
| Engineering OpenAPI candidates | — | 285 + 285 + 19 | Same set as Part 3.5 | Unchanged |
| Blueprint operations | — | — | **579** (555 + 24) + 40 API-ADV-X1 (Part 9.7b) | **655** (579 + 76 API-V12-H) + 40 API-ADV-X1; inline X2/X3 routes in Parts 9.8a/9.9a remain proposals without IDs |
| New operations by namespace | — | — | — | {{NEWOPS_BY_NS}} |
| New operations by V12 phase | — | — | — | {{NEWOPS_BY_PHASE}} |

**Why 76 new operations for 103 V12 operations not already represented.** Several V12 operations collapse onto one blueprint operation (the three run-gateway spellings `/api/v1/workflow-runs`, `/api/v1/commercial/workflow-runs` and `/api/v2/workflow-runs` → API-V12-H-068; preflight → `dry_run` on the same operation), and 13 operations are added that V12 implies but does not list (key rotation, OAuth client management, webhook update and replay, SCIM token issue, connector health summary, diagnostics, tier scenarios).

### 11.8.4.2 Appendix A (OpenAPI 3.1, 282 operations)

#### 11.8.4.2.1 Profile of the contract

{{APPX_A_SUMMARY}}

**Tags:** {{APPX_A_TAGS}}.

**Observations.** (1) Request and response bodies are generic (`Command.payload` and `Record.payload` are untyped objects); field-level DTOs exist only for `RunRequest`, `BusinessContext` and the two preflight schemas [GAP-897]. The blueprint keeps its field contracts (Part 3.5b §3.5.5.3 for the historical operations; §11.8.5.5 here for new ones) and records the V12 operationId on each. (2) Every read declares `304` and every command declares `202` and `Idempotency-Key`; no operation declares `401`, `413`, `415`, `422`, `429` or `503`. DEC-642 keeps the blueprint superset and adds `422`. (3) Only two operations are public (`security: []`): cookie consent and DSAR intake. (4) The 90 "Screens" operations carry the screen ID in the summary (A001…A113, W01…W34); the 158 `SM-SVC-##` operations carry the first workflow that uses them, which gives service traceability the blueprint did not have (DEC-640 keeps it as `x-v12-tag`).

#### 11.8.4.2.2 Full operation mapping (282 rows)

`Source` = historical registry row (SM-OP-###), UX candidate (SM-UX-API-##) or the V8 register. Blueprint operations for historical rows come from `final/coverage/D_api_mapping.csv`; "Before" is the status for V12 after Part 3.5b (all historical gaps were closed there).

{{APPX_A}}

#### 11.8.4.2.3 Historical operations not carried into Appendix A ({{HIST_NOT_IN_A_N}})

These are mostly public, portal-token and provider-callback routes. FSD 25 V5 keeps them in the historical registry as candidates ("exact source operations retained"), and Part 3.2 implements them; they are therefore retained, and Appendix A is treated as incomplete for the public and callback surfaces rather than as a deletion (DEC-640).

{{HIST_NOT_IN_A}}

### 11.8.4.3 Appendix A2 (48 enterprise operations)

{{A2}}

### 11.8.4.4 FSD 25 candidate operations outside the historical registry

#### 11.8.4.4.1 V8 convention and new operations (26)

{{V8}}

#### 11.8.4.4.2 MT, OPT, run-gateway and V4 candidates (32)

{{CAND}}

### 11.8.4.5 Historical registry and engineering archive

{{HIST_SUMMARY}}

{{ENG}}

### 11.8.4.6 Plugin register (FSD 28 V9: VND-01…97)

#### 11.8.4.6.1 Decision counts

{{VND_COUNTS}}

The V12 register is the 97-row subset of the 538-candidate register whose document-21 decision is not "Defer; no runtime need established" (441 rows). Every one of the 97 names and decisions matches a row of `F_integration_candidates.csv`; no decision differs.

#### 11.8.4.6.2 Row-by-row reconciliation (97)

{{VND}}

### 11.8.4.7 Connector catalogue (FSD 27 INT-01…11) to adapters

| V12 ID | Category | V12 examples | Auth | V12 scope / rule | Blueprint before | Blueprint after | V12 phase (ch. 39) |
|---|---|---|---|---|---|---|---|
| INT-01 | CRM | Salesforce / HubSpot / Zoho | OAuth 2.0 | Bi-directional contacts, accounts, opportunities | Not covered: native CRM only (M21–M23) | **AD-V12-H-01** `CrmSyncPort`; BYO credentials; one provider first (RECOMMENDATION-902) | R1 (CONFLICT-888) |
| INT-02 | Email delivery | SES, SendGrid, Postmark or equivalent | API key in vault | Send, bounce, complaint, unsubscribe webhooks | AD-01 SES (Resend after approval) | AD-01 primary; **AD-V12-H-11** alternates behind `EmailPort` | R1 |
| INT-03 | WhatsApp | Meta Business Solution Provider | System user token | Approved templates; opt-in required (CJ-IN-08) | AD-02 | AD-02 (BSP route allowed as equivalent host of the Cloud API) | R1 |
| INT-04 | SMS (India) | DLT-registered telecom aggregator | API key | Entity, header and template IDs required (CJ-IN-06) | Not covered ("no SMS in W0–W5") | **AD-V12-H-02** `SmsPort` (+ RCS business messaging) | R1 (CONFLICT-888) |
| INT-05 | Voice | CPaaS with 140/160 series numbers | API key | Promotional vs service number pools (CJ-IN-07) | Not covered | **AD-V12-H-03** `VoicePort` | R3+ (SVC-26) |
| INT-06 | Calendar | Google Workspace / Microsoft 365 | OAuth 2.0 | Free/busy and booking | AD-03, AD-04 | Unchanged | R1 |
| INT-07 | Advertising | Google Ads / Meta / LinkedIn | OAuth 2.0 | Budgets, audiences without health data (CJ-GL-07) | AD-09 (Google, Meta) | AD-09 + LinkedIn Marketing API under `AdsPort` | R2 |
| INT-08 | Payments | Razorpay / Stripe or equivalent | API key in vault | Payment intents, receipts, refunds | AD-11 | Unchanged; refunds recorded, never AI-initiated | R2 |
| INT-09 | Data warehouse | BigQuery / Snowflake / Postgres | Service account | Scoped export of analytics | CAP-X3-07 (A3 proposal) | **AD-V12-H-04** `WarehouseExportPort` | R2 |
| INT-10 | Identity provider | Okta / Entra ID / Google | SAML / OIDC / SCIM | SSO and provisioning (A122) | Shared IdP (DEC-019) only | **AD-V12-H-05** federation + SCIM server (ADR-207) | R1 (SSO) / R2 (SCIM) |
| INT-11 | Contact data | Licensed provider (ZoomInfo, Apollo …) | API key | Blocked pending legal (DEC-V9-04, CJ-GL-01) | AD-19 OFF by default, W1 pilot if approved | AD-19 **blocked** until DEC-V9-04 closes (DEC-649) | — |

### 11.8.4.8 Event reconciliation

| V12 event-bearing item | Blueprint before (Part 3.2 §3.2.3.3) | Gap | Blueprint after (§11.8.5.6) |
|---|---|---|---|
| ESP send/bounce/complaint/unsubscribe webhooks (INT-02) | `engagement.message.sent`, `.delivered`, `.bounced`, `.complained`; `engagement.optout.received` | None | Unchanged |
| Signed outbound webhooks (ENT-API-05); `webhook_endpoint.events[]`, `webhook_delivery` (C2) | §3.2.1.13 "Outbound webhooks to tenants: Not offered in W0–W6" | No outbound projection, no delivery events | Outbound projection v1 (24 types), `developer.webhook_delivery.*` |
| Connector provider events (API-V2-WEBHOOK) | `ops.webhook.received` via API-483 | Generic intake for new connector kinds | API-V12-H-073; `connector.*` events |
| Incident clocks and notifications (V8) | `governance.compliance_incident.opened` / `.resolved` | Notification evidence | `governance.compliance_incident.notification_recorded` |
| Consent withdrawal (V8) | `governance.consent.recorded`, `engagement.optout.received` | Staff-recorded withdrawal | `governance.consent.withdrawn` |
| AI kill switch, promotion, content screening (V8) | `ai.eval.gate_failed` | Governance events | `ai.kill_switch.*`, `ai.model.promotion_requested`, `ai.content.flagged` |
| Identity, SCIM, roles (A2) | `identity.membership.changed`, `identity.session.revoked` | Enterprise identity lifecycle | `identity.sso_config.*`, `identity.email_domain.*`, `identity.mfa_policy.updated`, `identity.scim.*`, `access.role.*` |
| API keys, OAuth clients (ENT-API-01/02) | — | Credential lifecycle | `developer.api_key.*`, `developer.oauth_client.*` |
| Connector gate and health (ENT-INT-04/05) | — | Gate and health | `connector.installation.*`, `connector.health.*` |
| Sandboxes, promotion, keys, SIEM, status, findings (A2) | `ops.incident.opened` / `.resolved` | Data and security lifecycle | `data.*`, `audit.siem_sink.*`, `ops.status.published`, `security.finding.*` |
| Portfolio grants (MT-API-10) | `identity.membership.changed` | Aggregate grant audit | `governance.portfolio_grant.changed` |

## 11.8.4.9 Quality gate: Batch 11.8a

| # | Item | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Each register row cites its V12 chapter/appendix row and the blueprint location; CSV has one row per aspect |
| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | Tags 886–903 used; register in Part 11.8b §11.8.9 |
| 3 | IDs unique and consistent with earlier parts | Pass | Script asserts every referenced API-### / API-ENH-D / API-ADV-X1 / API-V12-H ID exists and aspect IDs are unique |
| 4 | No story lacks AC and no requirement lacks a test | N/A here | Stories and tests are in Part 11.8b §11.8.5.13–14 |
| 5 | Negative, edge, security and accessibility cases | N/A here | Part 11.8b |
| 6 | Agent guardrail, fallback, KPI, cost | N/A | No new agent in this group |
| 7 | Time-sensitive facts flagged "verify" | Pass | Reading rule at the top; provider facts in §11.8.4.7 carry no prices |
| 8 | No restricted data to free-tier models | Pass | No routing change; DEC-418 order retained |
| 9 | Consistent with earlier parts | Pass with findings | Inconsistencies reported in Part 11.8b §11.8.8.5 (not edited) |

**Status: Part 11 Batch 11.8a complete. {{TOTAL_ASPECTS}} V12 aspects parsed and reconciled (282 Appendix A and 48 Appendix A2 operations, 302 historical rows, 58 other candidates, 97 VND decisions, 11 connector kinds, 1,370 field proposals in 266 operation groups); {{TOTAL_MATCHED}} Matched, {{TOTAL_PENDING}} Pending Founder decision, {{TOTAL_NA}} Not applicable. Enhancements, conflicts, decisions and the quality gate are in Part 11.8b.**
