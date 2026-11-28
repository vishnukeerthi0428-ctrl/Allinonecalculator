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
| | **Total** | | | | | **1176** |

Appendix C2 (enterprise schema, owned by Group I) was read for the field shapes of the A2 tables (`api_key`, `webhook_endpoint`, `webhook_delivery`, `identity_provider`, `scim_token`, `custom_role`, `sod_conflict`, `audit_sink`, `export_job`, `tenant_key_config`, `sandbox_environment`, `config_promotion`, `connector_installation`, `security_finding`, `ops_incident`, `tax_rule`, `invoice`, `locale_bundle`) so that the operation contracts in §11.8.5.5 agree with the proposed database constraints. Its coverage is not counted here.

### 11.8.1.2 Method (programmatic, every row)

| Step | Script (in `blueprint/assembly/v12/`) | What it does | Result |
|---|---|---|---|
| 1 | `h_compact.py` | Flattens `[TABLE]`/`---row` text into one line per row | 3 chapters, 0 rows lost (row counts equal source tables) |
| 2 | `h_parse_openapi.py` | Restores indentation lost in text extraction (`content:`, `"200"` … at column 0, by key context), loads YAML, emits one row per operation with method, path, operationId, tags, summary, parameters, request/response schema, response codes, `x-idempotency`, security | Appendix A **282 operations / 251 paths**; A2 **48 / 33**: equal to the counts stated in both headers |
| 3 | `h_blueprint_ops.py` | Extracts the blueprint inventory | Part 3.2: 555 (104 ★ + 451); Part 3.5b: 24; Part 9.7b: 37 single-method rows of API-ADV-X1-01…40 (three rows combine `GET / POST`) |
| 4 | `h_data.py` | Hand mapping, after keyword search of the inventory, for every V12 operation outside the 302 + 19 already reconciled in Part 3.5a, plus the 76 new operation specifications | 26 V8 + 32 MT/OPT/V2/V4 + 48 A2 mapped |
| 5 | `h_build.py` | Joins Appendix A to `final/coverage/D_api_mapping.csv` (302 + 19 source operations → blueprint), the plugin register to `final/coverage/F_integration_candidates.csv` (538 rows), verifies every engineering file against the reconciled set, writes `final/coverage_v12/H_coverage.csv` and the tables of this part | 1176 aspects; every referenced blueprint operation ID asserted to exist |

---

## 11.8.2 Coverage summary

| Material | Aspects | Covered | Partially covered | Not covered | Conflict | N/A | After: Matched | After: Pending Founder | After: N/A |
|---|---|---|---|---|---|---|---|---|---|
| FSD 25 REST API & Event Contract Master | 377 | 335 | 33 | 7 | 2 | 0 | 374 | 3 | 0 |
| FSD 27 External Integrations | 29 | 13 | 12 | 4 | 0 | 0 | 25 | 4 | 0 |
| FSD 28 Open-Source & Paid Plugin | 115 | 110 | 4 | 1 | 0 | 0 | 115 | 0 | 0 |
| Appendix A OpenAPI 3.1 | 301 | 273 | 18 | 6 | 3 | 1 | 300 | 0 | 1 |
| Appendix A2 Enterprise API | 49 | 8 | 19 | 22 | 0 | 0 | 49 | 0 | 0 |
| Source archive engineering files | 293 | 293 | 0 | 0 | 0 | 0 | 293 | 0 | 0 |
| Derived event contract | 12 | 1 | 3 | 8 | 0 | 0 | 12 | 0 | 0 |
| **Total** | **1176** | **1033** | **89** | **48** | **5** | **1** | **1168** | **7** | **1** |


**Reading the counts.** 1033 of 1176 aspects were already covered, mainly because the 302 historical operations, the 19 UX candidates, the 1,370 field proposals and the 97 plugin decisions are the same records that Parts 3.5a/3.5b and 7.4a reconciled from the 38-document pack (the V12 engineering archive is byte-identical in content; every operation and every VND decision matched programmatically). The real V12 deltas are: the developer platform (API keys, OAuth client credentials, per-key rate limits, signed outbound webhooks, SDKs, developer portal); the 48 enterprise operations of Appendix A2 (SSO, domain verification, MFA/session policy, SCIM 2.0, custom roles with SoD, SIEM, billing preview, tax quote, connector installation, BYOK, sandboxes and promotion, locales, operational incidents, public status, security findings); 26 V8 AI-governance and compliance routes; the MT/OPT candidate routes; the common run gateway `/api/v2/workflow-runs`; Appendix A wire conventions (Page, Record, Command, Error, RunRequest, BusinessContext, Preflight); the connector framework with its activation gate; and four new connector kinds (CRM, SMS-DLT, voice, data warehouse).

**After this part:** 1168 Matched, 7 Pending Founder decision, 1 Not applicable (the placeholder server URL `https://api.example.invalid`). The seven Founder-pending aspects are fully specified; what is pending is **when** they can be delivered, because V12 places them in phase R1 (private beta) and that adds scope to Release 1, whose budget, team and dates are fixed by DEC-228, DEC-230, DEC-417 and DEC-422 (CONFLICT-886, CONFLICT-887, CONFLICT-888).

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

Every aspect whose status before was not "Covered" is listed individually (143 rows). Covered aspects are grouped in §11.8.3.2. The full register, including every covered row, is `final/coverage_v12/H_coverage.csv`.

### 11.8.3.1 Partial, not covered, conflict and not-applicable aspects

| Aspect | Source | Summary | Status before | Blueprint location | Action / new IDs | Status after |
|---|---|---|---|---|---|---|
| H25-ENT-API-01 | FSD V12 25 | ENT-API-01 P0 Scoped, expiring API keys; stored as hash, shown once; optional IPv4/IPv6 allowlist; rotation and revocation. Acceptance: Plaintext never persisted (C2 schema has hash only); revoked key returns 401. Phase R1; prototype A125 | Partially covered | Part 9.9a CAP-X3-23, ADR-138 (A3 Year 2 proposal only) | Adopted literally; see §11.8.5; API-V12-H-001…004; FR-V12-H-001; ADR-205; R1 phase | Pending Founder decision |
| H25-ENT-API-02 | FSD V12 25 | ENT-API-02 P1 OAuth 2.0 client-credentials for server integrations. Acceptance: Token audience and scope verified; expired token rejected. Phase R2; prototype — | Partially covered | Part 9.9a ADR-138 (client-credentials apps, A3 proposal) | Adopted literally; see §11.8.5; API-V12-H-005…008; FR-V12-H-002; ADR-205 | Matched |
| H25-ENT-API-03 | FSD V12 25 | ENT-API-03 P0 Rate limits per key and tenant with 429 and Retry-After. Acceptance: Load test shows fair limits; noisy tenant isolated (AIX-16). Phase R1; prototype — | Partially covered | Part 3.2 §3.2.1.7 (per user/tenant/IP; no per-key class) | Adopted literally; see §11.8.5; RL-KEY class; FR-V12-H-003; R1 phase | Pending Founder decision |
| H25-ENT-API-04 | FSD V12 25 | ENT-API-04 P1 URL versioning and at least 12 months’ deprecation notice for breaking changes. Acceptance: Deprecation headers present; changelog published. Phase R2; prototype W39 | Conflict | Part 3.2 §3.2.1.3 (≥ 6 months public/portal; ≥ 1 release Admin) | Adopted literally; see §11.8.5; DEC-646 amends to ≥ 12 months; FR-V12-H-004 | Matched |
| H25-ENT-API-05 | FSD V12 25 | ENT-API-05 P0 Signed webhooks (HMAC-SHA256 + timestamp), replay protection, exponential retries for 24 h, delivery log. Acceptance: Tampered or >5-minute-old signature rejected by reference verifier. Phase R1; prototype A125 | Conflict | Part 3.2 §3.2.1.13 ("Outbound webhooks to tenants: Not offered in W0–W6"); Part 9.9a CAP-X3-23 | Adopted literally; see §11.8.5; API-V12-H-009…014; ADR-206; DEC-645; FR-V12-H-005; R1 phase | Pending Founder decision |
| H25-ENT-API-06 | FSD V12 25 | ENT-API-06 P2 SDKs for TypeScript, Python and Java generated from the OpenAPI contract. Acceptance: SDK contract tests pass against sandbox. Phase R3; prototype W39 | Partially covered | Part 3.2 §3.2.1.14 (TypeScript clients only); CAP-X3-23 (TS, Python) | Adopted literally; see §11.8.5; FR-V12-H-006; RECOMMENDATION-903 (Java at R3) | Matched |
| H25-ENT-API-07 | FSD V12 25 | ENT-API-07 P1 Developer portal with API reference, guides and sandbox access. Acceptance: Portal built from Appendix A/A2; examples executable in sandbox. Phase R2; prototype W39 | Partially covered | Part 3.2 §3.2.1.14 (docs); CAP-X3-23 sandbox tenant | Adopted literally; see §11.8.5; FR-V12-H-007; developer portal W39 from Appendix A/A2 | Matched |
| H25-A2-STMT | FSD V12 25 | Enterprise operations are in Appendix A2 (48 operations, OpenAPI 3.1, validated) | Not covered | — | 48 A2 operations parsed and mapped (§11.8.4.3); API-V12-H-001…048 (subset) | Matched |
| H25-REC-18 | FSD V12 25 | REC-18 P0: row-level source disposition index for APIs and entities; exact matches separate from semantic review; no unreviewed historical endpoint auto-deployed | Partially covered | Part 3.5a §3.5.4.2–3 (relation Exact/Alias/Split/Approval/Partial/New); D_api_mapping.csv | This part extends the index to Appendix A/A2 and all V12 candidates (H_coverage.csv relation column); DEC-640; DEC-640 | Matched |
| H25-V8-STMT | FSD V12 25 | All routes use /api/v1 prefix (D5); 10 MT/OPT candidate routes normalised in place; complete proposed contract is Appendix A (282 operations, validated) | Partially covered | Part 3.2 §3.2.1.1 (legacy /api/v1 + ~/ derived) | 282 Appendix A operations parsed (§11.8.4.2); prefix rule kept; v2 namespace only for run gateway (DEC-647); DEC-640, DEC-647 | Matched |
| H25-V8 GET /api/v1/ai/models | FSD V12 25 | GET /api/v1/ai/models | Partially covered | API-140; API-ADV-X1-12 | Relation Partial; API-V12-H-049 | Matched |
| H25-V8 POST /api/v1/ai/models/{id}/promotion-requests | FSD V12 25 | POST /api/v1/ai/models/{id}/promotion-requests | Partially covered | API-141 | Relation Partial; API-V12-H-050 | Matched |
| H25-V8 GET /api/v1/ai/prompts | FSD V12 25 | GET /api/v1/ai/prompts | Partially covered | API-142 | Relation Partial; API-V12-H-051 | Matched |
| H25-V8 GET /api/v1/ai/eval-suites | FSD V12 25 | GET /api/v1/ai/eval-suites | Partially covered | API-ENH-D-002; API-147 | Relation Partial; API-V12-H-052 | Matched |
| H25-V8 GET /api/v1/ai/red-team/results | FSD V12 25 | GET /api/v1/ai/red-team/results | Partially covered | API-ADV-X1-38 | Relation Partial; API-V12-H-053 | Matched |
| H25-V8 POST /api/v1/ai/content-screen | FSD V12 25 | POST /api/v1/ai/content-screen | Not covered | — | Relation New; API-V12-H-054 | Matched |
| H25-V8 GET /api/v1/ai/usage | FSD V12 25 | GET /api/v1/ai/usage | Partially covered | API-135; API-136 | Relation Partial; API-V12-H-055 | Matched |
| H25-V8 POST /api/v1/ai/kill-switch | FSD V12 25 | POST /api/v1/ai/kill-switch | Partially covered | API-451; API-144 | Relation Partial; API-V12-H-056 | Matched |
| H25-V8 GET /api/v1/compliance/packs/{id}/rules | FSD V12 25 | GET /api/v1/compliance/packs/{id}/rules | Partially covered | API-077 | Relation Partial; API-V12-H-057 | Matched |
| H25-V8 GET /api/v1/consents | FSD V12 25 | GET /api/v1/consents | Partially covered | API-076 | Relation Partial; API-V12-H-058 | Matched |
| H25-V8 POST /api/v1/consents/{id}/withdraw | FSD V12 25 | POST /api/v1/consents/{id}/withdraw | Partially covered | API-067; API-082 | Relation Partial; API-V12-H-059 | Matched |
| H25-V8 POST /api/v1/incidents | FSD V12 25 | POST /api/v1/incidents | Not covered | — | Relation New; API-V12-H-060 | Matched |
| H25-V8 POST /api/v1/incidents/{id}/notifications | FSD V12 25 | POST /api/v1/incidents/{id}/notifications | Not covered | — | Relation New; API-V12-H-061 | Matched |
| H25-V8 POST /api/v1/public/cookie-consent | FSD V12 25 | POST /api/v1/public/cookie-consent | Not covered | — | Relation New; API-V12-H-062 | Matched |
| H25-MOB-16 | FSD V12 25 | MOB-16 cross-device application handoff: SM-APPLICATION-6 envelope; canonical graph shared; fingerprint demo-only; production authenticated signed or server-owned request, replay protection, idempotent revision handling; no subscription activation during impor | Partially covered | Part 3.2 API-503/504 (If-Match revision), API-ENH-D-019; §3.2.1.5 idempotency | Production handoff = server-owned application draft (API-504) read on the other device (API-ENH-D-019); DEC-658; DEC-658; TC-V12-H-090 | Matched |
| H25-MT-36 | FSD V12 25 | MT-36 P0: one authoritative registry with alias and migration map; physical schema constraints approved before deployment; MT-TC-MT-36 detect conflicting path/entity names; contract tests against versioned schemas | Partially covered | Part 3.2 §3.2.2 (catalogue), §3.2.5 contract tests; Part 3.5a mapping | Registry = Part 3.2 catalogue + x-v12-operation-id + x-v12-path + route-alias register RA-V12-H (§11.8.5.2); CI duplicate-path check; DEC-640; TC-V12-H-081 | Matched |
| H25-MT-API-06 | FSD V12 25 | MT-API-06 POST /api/v1/configuration/{id}/rollback-draft — New draft version; re-review; no automatic restore | Partially covered | API-043 | Relation Partial; (semantic amendment of API-043, §11.8.5.3) | Matched |
| H25-MT-API-08 | FSD V12 25 | MT-API-08 POST /api/v1/workflow-runs — BusinessContext DTO; run ID/hold reason; no duplicate effect | Partially covered | API-456; API-449 | Relation Partial; API-V12-H-068 | Matched |
| H25-MT-API-09 | FSD V12 25 | MT-API-09 GET /api/v1/metrics/business — Native and converted totals with rate version and missing rates | Partially covered | API-537; API-388 | Relation Partial; API-V12-H-064 | Matched |
| H25-MT-API-10 | FSD V12 25 | MT-API-10 POST /api/v1/portfolio/grants — Grant/revoke aggregate scope; independent clients excluded | Partially covered | API-021 | Relation Partial; API-V12-H-063 | Matched |
| H25-OPT-API-01 | FSD V12 25 | OPT-API-01 POST /api/v1/optimization/preflight — Plan/hold, gate reasons, cost estimate; no external effect | Partially covered | API-449; API-455 | Relation Partial; API-V12-H-068 (dry_run) | Matched |
| H25-OPT-API-02 | FSD V12 25 | OPT-API-02 GET /api/v1/optimization/cost-summary — Meter categories, allocated/unallocated cost, accepted denominator | Partially covered | API-136 | Relation Partial; API-V12-H-065 | Matched |
| H25-OPT-API-05 | FSD V12 25 | OPT-API-05 GET /api/v1/optimization/customer-value — Accepted output, usage, value assumption, renewal state | Partially covered | API-513; API-514 | Relation Partial; API-V12-H-066 | Matched |
| H25-OPT-API-08 | FSD V12 25 | OPT-API-08 GET /api/v1/operator/conversion-metrics — Funnel counts, attribution quality, acquisition cost; aggregate only | Partially covered | API-537 | Relation Partial; API-V12-H-067 | Matched |
| H25-RUNGW | FSD V12 25 | Common run gateway resolves workflow access gaps without one endpoint per workflow; does not replace domain DTOs, adapter contracts or legacy routes; versioned; server-derived scope; cursor pagination, allowlisted filters, bounded payload; correlation ID; safe | Not covered | Part 3.2 §3.2.1.11 (run resources; no generic start) | Run gateway v2 API-V12-H-068…072 (ADR-208, DEC-647); error envelope DEC-641; API-V12-H-068…072 | Matched |
| H25-API-V2-RUN | FSD V12 25 | API-V2-RUN POST /api/v2/workflow-runs — {service_id,workflow_id,version,input,mode,idempotency_key} → 202 {run_id,state} | Not covered | API-456 | Relation New; API-V12-H-068 | Matched |
| H25-API-V2-RESULT | FSD V12 25 | API-V2-RESULT GET /api/v2/workflow-runs/{id} — {state,step_states,result_ref,error,usage} | Partially covered | API-467 | Relation Alias; API-V12-H-069 | Matched |
| H25-API-V2-APPROVAL | FSD V12 25 | API-V2-APPROVAL POST /api/v2/workflow-runs/{id}/approvals — {action_digest,decision,expiry,expected_version} → approval_ref | Partially covered | API-541; API-539 | Relation Approval; API-V12-H-070 | Matched |
| H25-API-V2-CANCEL | FSD V12 25 | API-V2-CANCEL POST /api/v2/workflow-runs/{id}/cancel — {expected_version,reason} → state; reconcile effects | Partially covered | API-471 | Relation Alias; API-V12-H-071 | Matched |
| H25-API-V2-WEBHOOK | FSD V12 25 | API-V2-WEBHOOK POST /api/v2/connectors/{kind}/events — Provider signed payload → accepted event receipt | Partially covered | API-483 | Relation Partial; API-V12-H-073 | Matched |
| H25-V4-API-04 | FSD V12 25 | POST /api/v1/commercial/workflow-runs — Run ID, state, reservation, correlation | Partially covered | API-456 | Relation Partial; API-V12-H-068 | Matched |
| H25-V4-API-06 | FSD V12 25 | GET /api/v1/commercial/workflow-runs/{id}/steps — Step status list, no provider secrets | Partially covered | API-467 | Relation Alias; API-V12-H-072 | Matched |
| H27-ENT-INT-01 | FSD V12 27 | ENT-INT-01 P0 Connector framework with one adapter contract: auth, scopes, data mapping, events, limits, failure handling. Acceptance: Every connector passes contract tests in sandbox. Phase R1; A128 | Partially covered | Part 3.2 §3.2.4.1 IP-01 port/adapter; §3.2.5 contract tests | Adopted literally (§11.8.5.7); Connector framework contract CF-01…12 (§11.8.5.7); API-V12-H-037/038; R1 | Pending Founder decision |
| H27-ENT-INT-04 | FSD V12 27 | ENT-INT-04 P1 Connector health, sync lag and error dashboards with alerts. Acceptance: Health check and alert fire in staging. Phase R2; A128 | Partially covered | Part 3.2 API-102 health; A008 | Adopted literally (§11.8.5.7); API-V12-H-074 health summary with sync lag and alerts | Matched |
| H27-ENT-INT-05 | FSD V12 27 | ENT-INT-05 P0 Activation gate: security review, DPA, transfer basis (CJ-R15) and channel registration (DLT, WhatsApp templates). Acceptance: Contact-data connectors stay blocked until DEC-V9-04 closes. Phase R1; A128 | Partially covered | Part 7.4b procurement gate PG-01…PG-10; AD-19 OFF by default (W1 pilot if approved) | Adopted literally (§11.8.5.7); Activation gate CF-11 (security review, DPA, CJ-R15 transfer basis, DLT/WhatsApp registration); contact-data blocked until DEC-V9-04 (DEC-649); R1 | Pending Founder decision |
| H27-INT-01 | FSD V12 27 | INT-01 CRM: Salesforce / HubSpot / Zoho; auth OAuth 2.0; Bi-directional contacts, accounts, opportunities | Not covered | Native CRM (M21–M23); Part 7.4a capability 05 "Native PostgreSQL records" | Adapter mapped (§11.8.5.8); AD-V12-H-01 CRM sync adapter (BYO credentials); RECOMMENDATION-902 | Pending Founder decision |
| H27-INT-04 | FSD V12 27 | INT-04 SMS (India): DLT-registered telecom aggregator; auth API key; Entity, header and template IDs required (CJ-IN-06) | Not covered | AD-02 fallback text "no SMS in W0–W5" | Adapter mapped (§11.8.5.8); AD-V12-H-02 SMS India DLT aggregator; CONFLICT-888 | Pending Founder decision |
| H27-INT-05 | FSD V12 27 | INT-05 Voice: CPaaS with 140/160 series numbers; auth API key; Promotional vs service number pools (CJ-IN-07) | Not covered | — | Adapter mapped (§11.8.5.8); AD-V12-H-03 Voice CPaaS (140/160 series pools); R3+  | Matched |
| H27-INT-07 | FSD V12 27 | INT-07 Advertising: Google Ads / Meta / LinkedIn; auth OAuth 2.0; Budgets, audiences without health data (CJ-GL-07) | Partially covered | AD-09 Meta/Google Ads (LinkedIn Ads not listed) | Adapter mapped (§11.8.5.8); LinkedIn Marketing API added to AdsPort scope; CJ-GL-07 no health data to ads | Matched |
| H27-INT-09 | FSD V12 27 | INT-09 Data warehouse: BigQuery / Snowflake / Postgres; auth Service account; Scoped export of analytics | Partially covered | Part 9.9a CAP-X3-07 BYO-warehouse export (A3) | Adapter mapped (§11.8.5.8); AD-V12-H-04 warehouse export adapter (BigQuery/Snowflake/Postgres), service account in vault | Matched |
| H27-INT-10 | FSD V12 27 | INT-10 Identity provider: Okta / Entra ID / Google; auth SAML / OIDC / SCIM; SSO and provisioning (A122) | Partially covered | DEC-019 shared IdP (OIDC); no per-tenant SAML/SCIM | Adapter mapped (§11.8.5.8); AD-V12-H-05 enterprise IdP federation + SCIM (API-V12-H-015…028) | Matched |
| H27-INT-11 | FSD V12 27 | INT-11 Contact data: Licensed provider (ZoomInfo, Apollo …); auth API key; Blocked pending legal (DEC-V9-04, CJ-GL-01) | Partially covered | AD-19 Apollo/Hunter OFF by default; B08 reserve | Adapter mapped (§11.8.5.8); Blocked pending legal (DEC-V9-04, CJ-GL-01) — stricter than AD-19 W1 pilot (DEC-649) | Matched |
| H27-MT-22 | FSD V12 27 | MT-22 P0: company may have multiple channel accounts; offering-market mapping and independent eligibility; MT-TC-MT-22 Email and WhatsApp accounts for two markets preserved in handoff | Partially covered | Part 3.2 API-097, API-104 (sender identities per startup) | ChannelAccount gains market_ids/offering_ids; eligibility evaluated per account (CF-05); FR-V12-H-024; TC-V12-H-086 | Matched |
| H27-GC-08 | FSD V12 27 | GC-08 P1 incremental provider sync: webhooks, cursors, ETags, change windows; reconcile gaps and provider reset; OPT-TC-GC-08 unchanged source no full fetch; missed event repaired without duplicates | Partially covered | Part 3.2 IP-05 scheduled reconciliation, §3.2.6 | CF-08 sync contract (cursor/ETag/window, gap repair); FR-V12-H-026; TC-V12-H-088 | Matched |
| H27-FAM-01 | FSD V12 27 | Adapter family Search / licensed sources: required contract / selection gate | Partially covered | Part 3.2 §3.2.4.2–3 AD-05/06/07 (rights, cache, source policy) | Benchmark coverage & freshness fields added (CF-12); CF-01…12 | Matched |
| H27-FAM-03 | FSD V12 27 | Adapter family WhatsApp / SMS / RCS: required contract / selection gate | Partially covered | Part 3.2 §3.2.4.2–3 AD-02 (WhatsApp only) | SMS-DLT and RCS via AD-V12-H-02 with country/route policy; CF-01…12 | Matched |
| H27-FAM-06 | FSD V12 27 | Adapter family Voice / media: required contract / selection gate | Not covered | Part 3.2 §3.2.4.2–3 — | AD-V12-H-03 (consent/recording rights, disclosure, quiet hours, asset licence); CF-01…12 | Matched |
| H27-FAM-07 | FSD V12 27 | Adapter family Payments / marketplace: required contract / selection gate | Partially covered | Part 3.2 §3.2.4.2–3 AD-11 (signed events, amount/currency, dedupe, no card storage) | Marketplace (SVC-31) settlement events mapped to PaymentPort; reconciliation (CF-09); CF-01…12 | Matched |
| H28-V9-STMT | FSD V12 28 | Retained strategy; contact-data vendors "replace core; licensed data only" and additionally need transfer-register entry (CJ-R15), a DPA and CJ-GL-01 compliance before activation (DEC-V9-04); every candidate disabled until benchmark, licence, legal and budget  | Partially covered | Part 7.4a §7.4.4.2; Part 7.4b PG-01…PG-10; F_integration_candidates.csv activation_default | Contact-data activation conditions added to PG gate (DEC-649, FR-V12-H-033); FR-V12-H-033 | Matched |
| H28-GC-10 | FSD V12 28 | GC-10 P1 bring-your-own-provider accounts: isolated credential references, allocated fees, permissions, support, revocation; OPT-TC-GC-10 BYO charges separate; revocation blocks calls | Partially covered | Part 9.9a (BYO-warehouse only) | Installation ownership platform\|tenant_byo (API-V12-H-038); charge separation in usage ledger; FR-V12-H-028 | Matched |
| H28-GC-11 | FSD V12 28 | GC-11 P2 provider volume and tier planning: forecast usage; compare tiers, commitments, overages; OPT-TC-GC-11 includes unused commitments; purchasing approval | Not covered | — | API-V12-H-076 tier scenarios (R3); FR-V12-H-029 | Matched |
| H28-GC-13 | FSD V12 28 | GC-13 P1 self-service operations: setup checklist, connector diagnostics, knowledge troubleshooting with human escalation; OPT-TC-GC-13 setup without staff; unresolved to support | Partially covered | Part 8.3 help/support; API-102 health | API-V12-H-075 diagnostics; FR-V12-H-030 | Matched |
| H28-GC-15 | FSD V12 28 | GC-15 P1 idle resource detection: unused connectors, idle infrastructure, orphaned artifacts; safe cleanup with ownership review; OPT-TC-GC-15 idle flagged, active/retained not deleted automatically | Partially covered | Part 9.9a CAP-X3-21 FinOps findings (A3) | Idle-connector finding type pulled into R2 via API-V12-H-074 + FinOps findings; never auto-delete; FR-V12-H-031 | Matched |
| HAA-HDR | FSD V12 Appendix A | OpenAPI 3.1 proposed contract: 282 operations on 251 paths; validated with openapi-spec-validator; not deployed; generated from workflow, screen, MT/OPT and V7 registers | Partially covered | Part 3.2 §3.2.1.14 (OpenAPI per namespace, drf-spectacular) | Parsed: 282 operations on 251 paths (h_parse_openapi.py); DEC-640 | Matched |
| HAA-C02 | FSD V12 Appendix A | servers: https://api.example.invalid placeholder | Not applicable | — | Hosts per DEC-421 ingress table §11.8.5.10; DEC-421 | Not applicable (placeholder host; real hosts in §11.8.5.10) |
| HAA-C03 | FSD V12 Appendix A | securitySchemes.bearerAuth: HTTP bearer, JWT; global security | Conflict | Part 3.2 §3.2.1.12 (no bearer tokens from browsers; DEC-019) | Two schemes: bffSession (browsers) + bearerAuth (integration surface) — DEC-643, CONFLICT-891; DEC-643 | Matched |
| HAA-C05 | FSD V12 Appendix A | parameters.limit: limit integer 1..200, default 50 | Conflict | Part 3.2 §3.2.1.6 (default 25, max 100) | V12 adopted: default 50, max 200 (DEC-641); DEC-641 | Matched |
| HAA-C07 | FSD V12 Appendix A | schemas.Error: required code, message, correlation_id; field_errors map | Partially covered | Part 3.2 §3.2.1.9 problem+json (code, detail, correlation_id, errors[]) | Superset envelope adds message and field_errors (DEC-641); DEC-641 | Matched |
| HAA-C08 | FSD V12 Appendix A | schemas.Page: items[] of Record; next_cursor string\|null | Conflict | Part 3.2 §3.2.1.6 {data, page.next_cursor} | V12 adopted: {items, next_cursor} (+ optional meta) (DEC-641); DEC-641 | Matched |
| HAA-C09 | FSD V12 Appendix A | schemas.Record: id uuid, version ≥ 1, status, payload, updated_at | Partially covered | Part 3.2 §3.2.1.8 revision + ETag | Wire field `version` = revision (DEC-641); DEC-641 | Matched |
| HAA-C10 | FSD V12 Appendix A | schemas.Command: expected_version ≥ 0, payload, reason ≤ 2000 | Partially covered | Part 3.2 If-Match header | expected_version accepted; must equal If-Match when both sent (DEC-641); DEC-641 | Matched |
| HAA-C11 | FSD V12 Appendix A | schemas.RunRequest: workflow_id ^SM-SVC-\d{2}-WF0[1-4]$, workflow_version, business_context, input (urn:sm:dto:<wf>:v2), dry_run | Not covered | — | API-V12-H-068 (DEC-647); DEC-647 | Matched |
| HAA-C12 | FSD V12 Appendix A | schemas.BusinessContext: company_id, offering_id, market_id required; division, brand, channel_account, campaign | Partially covered | Part 3.2 scope from session | BusinessContext validated against session scope; never authorizes (DEC-647); DEC-647 | Matched |
| HAA-C13 | FSD V12 Appendix A | schemas.PreflightRequest: market IN/EU/UK/US; channel Email/SMS/Voice/WhatsApp/Social/Web; purpose Promotional/Service; contact_id; send_at_local; template_id; ai_generated; ai_disclosed | Partially covered | Part 3.2 API-068 eligibility check | PreflightRequest adopted as API-068 DTO (§11.8.5.3) | Matched |
| HAA-C14 | FSD V12 Appendix A | schemas.PreflightResult: verdict ALLOW/HOLD/REVIEW; reasons[rule_id, effect, message]; pack_versions | Partially covered | Part 3.2 API-068 (rule IDs) | PreflightResult adopted (§11.8.5.3) | Matched |
| HAA-C16 | FSD V12 Appendix A | response codes: Reads 200/304/400/403/404/409; commands 200/202/400/403/404/409 | Partially covered | Part 3.2 §3.2.1.10 (adds 401, 413, 415, 429, 503) | Blueprint superset retained; 422 added (DEC-642); DEC-642 | Matched |
| HAA-C17 | FSD V12 Appendix A | tags: SM-SVC-## (workflow usage), Screens, AI, Compliance | Not covered | — | x-v12-tag kept on every operation; service/workflow traceability (DEC-640); DEC-640 | Matched |
| HAA-post_ai_content_screen | FSD V12 Appendix A | POST /api/v1/ai/content-screen [AI] Screen untrusted content; returns flags only; request Command; response Record; codes 200;202;400;403;404;409 | Not covered | — | Relation New; x-v12-operation-id=post_ai_content_screen; conventions DEC-641/642; API-V12-H-054 | Matched |
| HAA-get_ai_eval_suites | FSD V12 Appendix A | GET /api/v1/ai/eval-suites [AI] List evaluation suites (AIX-05); request —; response Page; codes 200;304;400;403;404;409 | Partially covered | API-ENH-D-002; API-147 | Relation Partial; x-v12-operation-id=get_ai_eval_suites; conventions DEC-641/642; API-V12-H-052 | Matched |
| HAA-post_ai_kill_switch | FSD V12 Appendix A | POST /api/v1/ai/kill-switch [AI] Stop model/prompt/workflow (AIX-20); request Command; response Record; codes 200;202;400;403;404;409 | Partially covered | API-451; API-144 | Relation Partial; x-v12-operation-id=post_ai_kill_switch; conventions DEC-641/642; API-V12-H-056 | Matched |
| HAA-get_ai_models | FSD V12 Appendix A | GET /api/v1/ai/models [AI] List model registry entries (AIX-02); request —; response Page; codes 200;304;400;403;404;409 | Partially covered | API-140; API-ADV-X1-12 | Relation Partial; x-v12-operation-id=get_ai_models; conventions DEC-641/642; API-V12-H-049 | Matched |
| HAA-post_ai_models_id_promotion_requests | FSD V12 Appendix A | POST /api/v1/ai/models/{id}/promotion-requests [AI] Request promotion; requires passing suites (AIX-05); request Command; response Record; codes 200;202;400;403;404;409 | Partially covered | API-141 | Relation Partial; x-v12-operation-id=post_ai_models_id_promotion_requests; conventions DEC-641/642; API-V12-H-050 | Matched |
| HAA-get_ai_prompts | FSD V12 Appendix A | GET /api/v1/ai/prompts [AI] List prompt versions (AIX-04); request —; response Page; codes 200;304;400;403;404;409 | Partially covered | API-142 | Relation Partial; x-v12-operation-id=get_ai_prompts; conventions DEC-641/642; API-V12-H-051 | Matched |
| HAA-get_ai_red_team_results | FSD V12 Appendix A | GET /api/v1/ai/red-team/results [AI] AI-INJ suite results (AIX-08); request —; response Page; codes 200;304;400;403;404;409 | Partially covered | API-ADV-X1-38 | Relation Partial; x-v12-operation-id=get_ai_red_team_results; conventions DEC-641/642; API-V12-H-053 | Matched |
| HAA-get_ai_usage | FSD V12 Appendix A | GET /api/v1/ai/usage [AI] Token usage and cost per accepted result (AIX-12, AIX-14); request —; response Page; codes 200;304;400;403;404;409 | Partially covered | API-135; API-136 | Relation Partial; x-v12-operation-id=get_ai_usage; conventions DEC-641/642; API-V12-H-055 | Matched |
| HAA-get_compliance_packs_id_rules | FSD V12 Appendix A | GET /api/v1/compliance/packs/{id}/rules [Compliance] Rules with legal source and status; request —; response Record; codes 200;304;400;403;404;409 | Partially covered | API-077 | Relation Partial; x-v12-operation-id=get_compliance_packs_id_rules; conventions DEC-641/642; API-V12-H-057 | Matched |
| HAA-get_consents | FSD V12 Appendix A | GET /api/v1/consents [Compliance] Search consent ledger (CJ-R04); request —; response Page; codes 200;304;400;403;404;409 | Partially covered | API-076 | Relation Partial; x-v12-operation-id=get_consents; conventions DEC-641/642; API-V12-H-058 | Matched |
| HAA-post_consents_id_withdraw | FSD V12 Appendix A | POST /api/v1/consents/{id}/withdraw [Compliance] Withdraw consent and suppress (CJ-R05); request Command; response Record; codes 200;202;400;403;404;409 | Partially covered | API-067; API-082 | Relation Partial; x-v12-operation-id=post_consents_id_withdraw; conventions DEC-641/642; API-V12-H-059 | Matched |
| HAA-post_incidents | FSD V12 Appendix A | POST /api/v1/incidents [Compliance] Open incident; clocks start; request Command; response Record; codes 200;202;400;403;404;409 | Not covered | — | Relation New; x-v12-operation-id=post_incidents; conventions DEC-641/642; API-V12-H-060 | Matched |
| HAA-post_incidents_id_notifications | FSD V12 Appendix A | POST /api/v1/incidents/{id}/notifications [Compliance] Record authority/principal notification; request Command; response Record; codes 200;202;400;403;404;409 | Not covered | — | Relation New; x-v12-operation-id=post_incidents_id_notifications; conventions DEC-641/642; API-V12-H-061 | Matched |
| HAA-post_public_cookie_consent | FSD V12 Appendix A | POST /api/v1/public/cookie-consent [Compliance] Record cookie choice with notice version (CJ-R12); request Command; response Record; codes 200;202;400;403;404;409 | Not covered | — | Relation New; x-v12-operation-id=post_public_cookie_consent; conventions DEC-641/642; API-V12-H-062 | Matched |
| HA2-get_api_scim_v2_Groups | FSD V12 Appendix A2 | GET /api/scim/v2/Groups [SCIM] SCIM list groups | Not covered | — | Relation New; API-V12-H-026 | Matched |
| HA2-post_api_scim_v2_Groups | FSD V12 Appendix A2 | POST /api/scim/v2/Groups [SCIM] SCIM create group | Not covered | — | Relation New; API-V12-H-027 | Matched |
| HA2-get_api_scim_v2_Users | FSD V12 Appendix A2 | GET /api/scim/v2/Users [SCIM] SCIM list users | Not covered | — | Relation New; API-V12-H-021 | Matched |
| HA2-post_api_scim_v2_Users | FSD V12 Appendix A2 | POST /api/scim/v2/Users [SCIM] SCIM create user | Not covered | — | Relation New; API-V12-H-022 | Matched |
| HA2-delete_api_scim_v2_Users_id | FSD V12 Appendix A2 | DELETE /api/scim/v2/Users/{id} [SCIM] SCIM de-provision user | Not covered | — | Relation New; API-V12-H-025 | Matched |
| HA2-get_api_scim_v2_Users_id | FSD V12 Appendix A2 | GET /api/scim/v2/Users/{id} [SCIM] SCIM read user | Not covered | — | Relation New; API-V12-H-023 | Matched |
| HA2-patch_api_scim_v2_Users_id | FSD V12 Appendix A2 | PATCH /api/scim/v2/Users/{id} [SCIM] SCIM update user | Not covered | — | Relation New; API-V12-H-024 | Matched |
| HA2-get_api_keys | FSD V12 Appendix A2 | GET /api/v1/api-keys [Developer] List API keys (prefix only) | Partially covered | CAP-X3-23 (A3, proposal) | Relation Partial; API-V12-H-001 | Matched |
| HA2-post_api_keys | FSD V12 Appendix A2 | POST /api/v1/api-keys [Developer] Create API key (value returned once) | Partially covered | CAP-X3-23 (A3, proposal) | Relation Partial; API-V12-H-002 | Matched |
| HA2-post_api_keys_id_revoke | FSD V12 Appendix A2 | POST /api/v1/api-keys/{id}/revoke [Developer] Revoke API key | Partially covered | CAP-X3-23 (A3, proposal) | Relation Partial; API-V12-H-003 | Matched |
| HA2-post_billing_invoices_preview | FSD V12 Appendix A2 | POST /api/v1/billing/invoices/preview [Billing] Preview invoice with tax | Not covered | — | Relation New; API-V12-H-035 | Matched |
| HA2-get_connectors | FSD V12 Appendix A2 | GET /api/v1/connectors [Integrations] Connector catalogue | Partially covered | API-095 | Relation Partial; API-V12-H-037 | Matched |
| HA2-post_connectors_id_installations | FSD V12 Appendix A2 | POST /api/v1/connectors/{id}/installations [Integrations] Install connector | Partially covered | API-097 | Relation Partial; API-V12-H-038 | Matched |
| HA2-get_encryption_keys | FSD V12 Appendix A2 | GET /api/v1/encryption-keys [Data] Read key configuration | Partially covered | CAP-X3-15 (A3, proposal) | Relation Partial; API-V12-H-039 | Matched |
| HA2-put_encryption_keys | FSD V12 Appendix A2 | PUT /api/v1/encryption-keys [Data] Set platform or customer-managed key | Partially covered | CAP-X3-15 (A3, proposal) | Relation Partial; API-V12-H-040 | Matched |
| HA2-post_identity_domains | FSD V12 Appendix A2 | POST /api/v1/identity/domains [Identity] Add domain for verification | Not covered | — | Relation New; API-V12-H-018 | Matched |
| HA2-post_identity_domains_id_verify | FSD V12 Appendix A2 | POST /api/v1/identity/domains/{id}/verify [Identity] Verify domain DNS TXT record | Not covered | — | Relation New; API-V12-H-019 | Matched |
| HA2-put_identity_policies | FSD V12 Appendix A2 | PUT /api/v1/identity/policies [Identity] Set MFA and session policy | Partially covered | CAP-X3-14 (A3, proposal) | Relation Partial; API-V12-H-020 | Matched |
| HA2-get_identity_sso | FSD V12 Appendix A2 | GET /api/v1/identity/sso [Identity] Read tenant SSO configuration | Not covered | — | Relation New; API-V12-H-015 | Matched |
| HA2-put_identity_sso | FSD V12 Appendix A2 | PUT /api/v1/identity/sso [Identity] Update SSO configuration | Not covered | — | Relation New; API-V12-H-016 | Matched |
| HA2-post_identity_sso_test | FSD V12 Appendix A2 | POST /api/v1/identity/sso/test [Identity] Test IdP connection | Not covered | — | Relation New; API-V12-H-017 | Matched |
| HA2-get_locales | FSD V12 Appendix A2 | GET /api/v1/locales [Global] Supported locales and coverage | Partially covered | CAP-X3-27 (A3, proposal) | Relation Partial; API-V12-H-044 | Matched |
| HA2-post_ops_incidents | FSD V12 Appendix A2 | POST /api/v1/ops/incidents [Operations] Declare incident | Partially covered | API-128 | Relation Partial; API-V12-H-045 | Matched |
| HA2-get_public_status | FSD V12 Appendix A2 | GET /api/v1/public/status [Operations] Public status summary | Partially covered | CAP-X3-12 (A3, proposal) | Relation Partial; API-V12-H-046 | Matched |
| HA2-get_roles | FSD V12 Appendix A2 | GET /api/v1/roles [Access] List roles | Not covered | — | Relation New; API-V12-H-029 | Matched |
| HA2-post_roles | FSD V12 Appendix A2 | POST /api/v1/roles [Access] Create custom role (SoD checked) | Not covered | — | Relation New; API-V12-H-030 | Matched |
| HA2-delete_roles_id | FSD V12 Appendix A2 | DELETE /api/v1/roles/{id} [Access] Retire role | Not covered | — | Relation New; API-V12-H-032 | Matched |
| HA2-patch_roles_id | FSD V12 Appendix A2 | PATCH /api/v1/roles/{id} [Access] Update role | Not covered | — | Relation New; API-V12-H-031 | Matched |
| HA2-get_sandboxes | FSD V12 Appendix A2 | GET /api/v1/sandboxes [Data] List sandboxes | Not covered | — | Relation New; API-V12-H-041 | Matched |
| HA2-post_sandboxes | FSD V12 Appendix A2 | POST /api/v1/sandboxes [Data] Create sandbox | Not covered | — | Relation New; API-V12-H-042 | Matched |
| HA2-post_sandboxes_id_promotions | FSD V12 Appendix A2 | POST /api/v1/sandboxes/{id}/promotions [Data] Request configuration promotion | Partially covered | API-039 (revision only) | Relation Partial; API-V12-H-043 | Matched |
| HA2-get_security_findings | FSD V12 Appendix A2 | GET /api/v1/security/findings [Security] Vulnerability findings (operator) | Partially covered | CAP-X3-19 (A3, proposal) | Relation Partial; API-V12-H-047 | Matched |
| HA2-post_security_findings | FSD V12 Appendix A2 | POST /api/v1/security/findings [Security] Log finding | Partially covered | CAP-X3-19 (A3, proposal) | Relation Partial; API-V12-H-048 | Matched |
| HA2-get_siem_sinks | FSD V12 Appendix A2 | GET /api/v1/siem-sinks [Audit] List SIEM destinations | Not covered | — | Relation New; API-V12-H-033 | Matched |
| HA2-post_siem_sinks | FSD V12 Appendix A2 | POST /api/v1/siem-sinks [Audit] Add SIEM destination | Not covered | — | Relation New; API-V12-H-034 | Matched |
| HA2-post_tax_quote | FSD V12 Appendix A2 | POST /api/v1/tax/quote [Billing] Tax determination for a line | Partially covered | API-339 (embedded in quote) | Relation Partial; API-V12-H-036 | Matched |
| HA2-get_webhook_deliveries | FSD V12 Appendix A2 | GET /api/v1/webhook-deliveries [Developer] Delivery log | Partially covered | CAP-X3-23 (A3, proposal) | Relation Partial; API-V12-H-013 | Matched |
| HA2-get_webhooks | FSD V12 Appendix A2 | GET /api/v1/webhooks [Developer] List webhook endpoints | Partially covered | CAP-X3-23 (A3, proposal) | Relation Partial; API-V12-H-009 | Matched |
| HA2-post_webhooks | FSD V12 Appendix A2 | POST /api/v1/webhooks [Developer] Add webhook endpoint | Partially covered | CAP-X3-23 (A3, proposal) | Relation Partial; API-V12-H-010 | Matched |
| HA2-post_webhooks_id_test | FSD V12 Appendix A2 | POST /api/v1/webhooks/{id}/test [Developer] Send signed test event | Partially covered | CAP-X3-23 (A3, proposal) | Relation Partial; API-V12-H-012 | Matched |
| HA2-HDR | FSD V12 Appendix A2 | 48 operations on 33 paths; validated; SCIM endpoints follow RFC 7643/7644 resource shapes | Not covered | — | Parsed 48 operations on 33 paths; SCIM served at /scim/v2 on the developer host (ADR-207); ADR-207 | Matched |
| HEV-02 | FSD V12 (derived event contract) events | Outbound signed webhook events to tenant endpoints (event catalogue for subscription) | Not covered | Part 3.2 §3.2.1.13 (not offered) | Outbound projection v1, 24 event types (§11.8.5.6); Event catalogue §11.8.5.6 | Matched |
| HEV-03 | FSD V12 (derived event contract) events | Delivery record per attempt (1..6), status code, signed_at, delivered_at | Not covered | — | developer.webhook_delivery.* events; API-V12-H-013; Event catalogue §11.8.5.6 | Matched |
| HEV-04 | FSD V12 (derived event contract) events | Connector provider events → accepted event receipt (signature/time/account mapping; duplicate safe) | Partially covered | ops.webhook.received; API-483 | API-V12-H-073; Event catalogue §11.8.5.6 | Matched |
| HEV-05 | FSD V12 (derived event contract) events | Incident open starts clocks; authority/principal notification recorded | Partially covered | governance.compliance_incident.opened/.resolved | governance.compliance_incident.notification_recorded; Event catalogue §11.8.5.6 | Matched |
| HEV-06 | FSD V12 (derived event contract) events | Consent withdrawal and suppression | Partially covered | governance.consent.recorded; engagement.optout.received | governance.consent.withdrawn; Event catalogue §11.8.5.6 | Matched |
| HEV-07 | FSD V12 (derived event contract) events | Kill switch, promotion request, content screen flags | Not covered | ai.eval.gate_failed only | ai.kill_switch.activated/.released; ai.model.promotion_requested; ai.content.flagged; Event catalogue §11.8.5.6 | Matched |
| HEV-08 | FSD V12 (derived event contract) events | SSO, domain, MFA policy, SCIM, custom role lifecycle | Not covered | identity.membership.changed; identity.session.revoked | identity.* and access.role.* events (§11.8.5.6); Event catalogue §11.8.5.6 | Matched |
| HEV-09 | FSD V12 (derived event contract) events | API key and OAuth client lifecycle | Not covered | — | developer.api_key.*, developer.oauth_client.*; Event catalogue §11.8.5.6 | Matched |
| HEV-10 | FSD V12 (derived event contract) events | Connector installation gate and health | Not covered | — | connector.installation.*, connector.health.*; Event catalogue §11.8.5.6 | Matched |
| HEV-11 | FSD V12 (derived event contract) events | Sandbox, promotion, key change, SIEM sink, status publication, findings | Not covered | ops.incident.opened/.resolved | data.*, audit.siem_sink.*, ops.status.published, security.finding.*; Event catalogue §11.8.5.6 | Matched |
| HEV-12 | FSD V12 (derived event contract) events | Portfolio grant change audit | Not covered | identity.membership.changed | governance.portfolio_grant.changed; Event catalogue §11.8.5.6 | Matched |


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
| Historical registry (FSD 25 V5) | 302 (288 + 14 website) | 302 (285 HTTP + 17 adapters) | 302 mapped (Part 3.5a) | Unchanged; 30 historical HTTP operations are **not** carried into Appendix A (§11.8.4.2.3) and stay in the blueprint |
| Other FSD 25 candidates | V8 26 · MT 10 · OPT 8 · V2 7 · V4 7 | 58 | 30 equivalent | 58 represented; 13 new + 2 route aliases |
| Engineering OpenAPI candidates | — | 285 + 285 + 19 | Same set as Part 3.5 | Unchanged |
| Blueprint operations | — | — | **579** (555 + 24) + 40 API-ADV-X1 (Part 9.7b) | **655** (579 + 76 API-V12-H) + 40 API-ADV-X1; inline X2/X3 routes in Parts 9.8a/9.9a remain proposals without IDs |
| New operations by namespace | — | — | — | admin 56, admin+internal 1, dev 1, hooks 1, internal 1, portal 1, public 2, scim 7, status 1, v2 5 |
| New operations by V12 phase | — | — | — | R1 44, R2 29, R3 3 |

**Why 76 new operations for 103 V12 operations not already represented.** Several V12 operations collapse onto one blueprint operation (the three run-gateway spellings `/api/v1/workflow-runs`, `/api/v1/commercial/workflow-runs` and `/api/v2/workflow-runs` → API-V12-H-068; preflight → `dry_run` on the same operation), and 13 operations are added that V12 implies but does not list (key rotation, OAuth client management, webhook update and replay, SCIM token issue, connector health summary, diagnostics, tier scenarios).

### 11.8.4.2 Appendix A (OpenAPI 3.1, 282 operations)

#### 11.8.4.2.1 Profile of the contract

| Dimension | Value | Operations |
|---|---|---|
| Origin | Historical registry (SM-OP) | 254 |
| Origin | V8 register | 26 |
| Origin | UX candidate (SM-UX-API) | 2 |
| Relation | Alias | 117 |
| Relation | Alias (prefix) | 5 |
| Relation | Approval | 8 |
| Relation | Exact | 93 |
| Relation | New | 4 |
| Relation | New (Part 3.5b) | 6 |
| Relation | Partial | 21 |
| Relation | Split | 28 |
| Status before | Covered | 268 |
| Status before | Not covered | 4 |
| Status before | Partially covered | 10 |
| Method | GET | 109 |
| Method | POST | 161 |
| Method | PATCH | 11 |
| Method | PUT | 1 |
| Request schema | (none: read) | 109 |
| Request schema | Command | 172 |
| Request schema | PreflightRequest | 1 |
| Response schema | Page | 93 |
| Response schema | Record | 188 |
| Response schema | PreflightResult | 1 |
| Response-code set | 200;304;400;403;404;409 | 121 |
| Response-code set | 200;202;400;403;404;409 | 161 |


**Tags:** AI 11, Compliance 14, SM-SVC-01 7, SM-SVC-02 3, SM-SVC-03 8, SM-SVC-04 6, SM-SVC-05 9, SM-SVC-06 7, SM-SVC-07 3, SM-SVC-08 9, SM-SVC-09 5, SM-SVC-10 6, SM-SVC-11 9, SM-SVC-12 2, SM-SVC-13 6, SM-SVC-14 7, SM-SVC-15 2, SM-SVC-16 4, SM-SVC-17 6, SM-SVC-18 8, SM-SVC-19 5, SM-SVC-20 7, SM-SVC-21 6, SM-SVC-22 5, SM-SVC-23 6, SM-SVC-24 4, SM-SVC-25 8, SM-SVC-26 5, SM-SVC-27 1, SM-SVC-28 4, SM-SVC-29 1, SM-SVC-30 1, SM-SVC-31 2, SM-SVC-32 1, SM-SVC-34 2, SM-SVC-38 1, SM-SVC-39 1, Screens 90.

**Observations.** (1) Request and response bodies are generic (`Command.payload` and `Record.payload` are untyped objects); field-level DTOs exist only for `RunRequest`, `BusinessContext` and the two preflight schemas [GAP-897]. The blueprint keeps its field contracts (Part 3.5b §3.5.5.3 for the historical operations; §11.8.5.5 here for new ones) and records the V12 operationId on each. (2) Every read declares `304` and every command declares `202` and `Idempotency-Key`; no operation declares `401`, `413`, `415`, `422`, `429` or `503`. DEC-642 keeps the blueprint superset and adds `422`. (3) Only two operations are public (`security: []`): cookie consent and DSAR intake. (4) The 90 "Screens" operations carry the screen ID in the summary (A001…A113, W01…W34); the 158 `SM-SVC-##` operations carry the first workflow that uses them, which gives service traceability the blueprint did not have (DEC-640 keeps it as `x-v12-tag`).

#### 11.8.4.2.2 Full operation mapping (282 rows)

`Source` = historical registry row (SM-OP-###), UX candidate (SM-UX-API-##) or the V8 register. Blueprint operations for historical rows come from `final/coverage/D_api_mapping.csv`; "Before" is the status for V12 after Part 3.5b (all historical gaps were closed there).

| # | V12 operationId | Method | V12 path | V12 tag / summary | Source | Blueprint operation(s) | Relation | Before | Enhancement |
|---|---|---|---|---|---|---|---|---|---|
| 1 | get_admin_ai_eval_cases | GET | `/api/v1/admin/ai/eval-cases` | Screens: Screen A011 | SM-OP-036 | API-ENH-D-002 | New (Part 3.5b) | Covered | — |
| 2 | post_admin_ai_prompts | POST | `/api/v1/admin/ai/prompts` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-035 | API-142 | Alias | Covered | — |
| 3 | get_admin_ai_runs | GET | `/api/v1/admin/ai/runs` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-034 | API-135 | Exact | Covered | — |
| 4 | get_admin_approvals | GET | `/api/v1/admin/approvals` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-107 | API-540 | Alias | Covered | — |
| 5 | post_admin_approvals_id_decide | POST | `/api/v1/admin/approvals/{id}/decide` | Screens: Screen A089 | SM-OP-232 | API-539 | Exact | Covered | — |
| 6 | post_admin_budgets | POST | `/api/v1/admin/budgets` | Screens: Screen A012 | SM-OP-039 | API-137 | Exact | Covered | — |
| 7 | post_admin_budgets_id_pause | POST | `/api/v1/admin/budgets/{id}/pause` | Screens: Screen A012 | SM-OP-040 | API-144 | Alias | Covered | — |
| 8 | post_admin_calendar_links | POST | `/api/v1/admin/calendar-links` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-125 | API-110 | Alias | Covered | — |
| 9 | post_admin_chat_settings | POST | `/api/v1/admin/chat/settings` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-138 | API-280; API-ENH-D-009 | Partial | Covered | — |
| 10 | post_admin_claims_approve | POST | `/api/v1/admin/claims/approve` | SM-SVC-28: Used by SM-SVC-28-WF01 | SM-OP-010 | API-049 | Exact | Covered | — |
| 11 | post_admin_competitor_sources | POST | `/api/v1/admin/competitor-sources` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-228 | API-208 | Alias | Covered | — |
| 12 | get_admin_compliance | GET | `/api/v1/admin/compliance` | Screens: Screen A047 | SM-OP-142 | API-070 | Exact | Covered | — |
| 13 | post_admin_compliance_id_resolve | POST | `/api/v1/admin/compliance/{id}/resolve` | Screens: Screen A047 | SM-OP-143 | API-094 | Alias | Covered | — |
| 14 | get_admin_costs | GET | `/api/v1/admin/costs` | Screens: Screen A012 | SM-OP-038 | API-136 | Exact | Covered | — |
| 15 | get_admin_dashboard | GET | `/api/v1/admin/dashboard` | Screens: Screen A089 | SM-OP-231 | API-538 | Exact | Covered | — |
| 16 | get_admin_evals_results | GET | `/api/v1/admin/evals/results` | Screens: Screen A084 | SM-OP-226 | API-147;API-148 | Split | Covered | — |
| 17 | post_admin_evals_run | POST | `/api/v1/admin/evals/run` | Screens: Screen A084 | SM-OP-225 | API-138 | Exact | Covered | — |
| 18 | post_admin_events_id_settings | POST | `/api/v1/admin/events/{id}/settings` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-180 | API-325 | Alias | Covered | — |
| 19 | post_admin_forecast_settings | POST | `/api/v1/admin/forecast-settings` | SM-SVC-24: Used by SM-SVC-24-WF01 | SM-OP-230 | API-407; API-ENH-D-010 | Partial | Covered | — |
| 20 | get_admin_forms | GET | `/api/v1/admin/forms` | SM-SVC-15: Used by SM-SVC-15-WF01 | SM-OP-094 | API-221 | Alias | Covered | — |
| 21 | post_admin_forms | POST | `/api/v1/admin/forms` | SM-SVC-15: Used by SM-SVC-15-WF01 | SM-OP-095 | API-222;API-223 | Split | Covered | — |
| 22 | get_admin_health | GET | `/api/v1/admin/health` | Screens: Screen A014 | SM-OP-047 | API-119 | Exact | Covered | — |
| 23 | post_admin_incidents_id_resolve | POST | `/api/v1/admin/incidents/{id}/resolve` | Screens: Screen A014 | SM-OP-048 | API-129;API-130 | Split | Covered | — |
| 24 | post_admin_integrations | POST | `/api/v1/admin/integrations` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-024 | API-097 | Alias | Covered | — |
| 25 | post_admin_integrations_test | POST | `/api/v1/admin/integrations/test` | Screens: Screen A008 | SM-OP-025 | API-096 | Exact | Covered | — |
| 26 | post_admin_integrations_id_disable | POST | `/api/v1/admin/integrations/{id}/disable` | Screens: Screen A008 | SM-OP-026 | API-099 | Alias | Covered | — |
| 27 | get_admin_jobs | GET | `/api/v1/admin/jobs` | Screens: Screen A009 | SM-OP-028 | API-124 | Alias | Covered | — |
| 28 | post_admin_jobs_id_retry | POST | `/api/v1/admin/jobs/{id}/retry` | Screens: Screen A009 | SM-OP-029 | API-116 | Exact | Covered | — |
| 29 | post_admin_kpi_definitions | POST | `/api/v1/admin/kpi-definitions` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-224 | API-405 | Alias | Covered | — |
| 30 | get_admin_message_templates | GET | `/api/v1/admin/message-templates` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-104 | API-255 | Alias | Covered | — |
| 31 | post_admin_message_templates | POST | `/api/v1/admin/message-templates` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-105 | API-256 | Alias | Covered | — |
| 32 | get_admin_pipeline_stages | GET | `/api/v1/admin/pipeline-stages` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-089 | API-218 | Alias | Covered | — |
| 33 | post_admin_pipeline_stages | POST | `/api/v1/admin/pipeline-stages` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-090 | API-219;API-220 | Split | Covered | — |
| 34 | get_admin_policies | GET | `/api/v1/admin/policies` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-020 | API-071 | Alias | Covered | — |
| 35 | post_admin_policies | POST | `/api/v1/admin/policies` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-021 | API-072;API-073 | Split | Covered | — |
| 36 | get_admin_privacy_requests | GET | `/api/v1/admin/privacy/requests` | Screens: Screen A013 | SM-OP-042 | API-084 | Alias | Covered | — |
| 37 | post_admin_privacy_requests_id_resolve | POST | `/api/v1/admin/privacy/requests/{id}/resolve` | Screens: Screen A013 | SM-OP-043 | API-085;API-086;API-087 | Split | Covered | — |
| 38 | post_admin_products | POST | `/api/v1/admin/products` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-008 | API-053 | Alias | Covered | — |
| 39 | get_admin_products_planned | GET | `/api/v1/admin/products/planned` | Screens: Screen A097 | SM-OP-245 | API-064 | Alias | Covered | — |
| 40 | patch_admin_products_id | PATCH | `/api/v1/admin/products/{id}` | SM-SVC-28: Used by SM-SVC-28-WF01 | SM-OP-009 | API-055;API-056 | Split | Covered | — |
| 41 | post_admin_products_id_launch | POST | `/api/v1/admin/products/{id}/launch` | Screens: Screen A098 | SM-OP-246 | API-050 | Exact | Covered | — |
| 42 | post_admin_products_id_prices | POST | `/api/v1/admin/products/{id}/prices` | SM-SVC-28: Used by SM-SVC-28-WF01 | SM-OP-011 | API-057 | Alias | Covered | — |
| 43 | get_admin_referrals | GET | `/api/v1/admin/referrals` | SM-SVC-16: Used by SM-SVC-16-WF01 | SM-OP-183 | API-327 | Alias | Covered | — |
| 44 | post_admin_referrals_id_review | POST | `/api/v1/admin/referrals/{id}/review` | SM-SVC-16: Used by SM-SVC-16-WF01 | SM-OP-184 | API-541;API-539 | Approval | Covered | — |
| 45 | get_admin_releases | GET | `/api/v1/admin/releases` | Screens: Screen A090 | SM-OP-233 | API-120 | Exact | Covered | — |
| 46 | post_admin_releases_id_approve | POST | `/api/v1/admin/releases/{id}/approve` | Screens: Screen A090 | SM-OP-234 | API-132 | Alias | Covered | — |
| 47 | post_admin_renewal_policies | POST | `/api/v1/admin/renewal-policies` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-219 | API-429 | Alias | Covered | — |
| 48 | post_admin_research_review_rules | POST | `/api/v1/admin/research-review-rules` | SM-SVC-19: Used by SM-SVC-19-WF01 | SM-OP-083 | API-202 | Alias | Covered | — |
| 49 | post_admin_retention_policies | POST | `/api/v1/admin/retention-policies` | Screens: Screen A013 | SM-OP-044 | API-091 | Alias | Covered | — |
| 50 | post_admin_role_mappings | POST | `/api/v1/admin/role-mappings` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-075 | API-199; API-ENH-D-004 | Partial | Covered | — |
| 51 | post_admin_routing_rules | POST | `/api/v1/admin/routing-rules` | SM-SVC-26: Used by SM-SVC-26-WF01 | SM-OP-141 | API-283 | Alias | Covered | — |
| 52 | post_admin_scoring_rules | POST | `/api/v1/admin/scoring-rules` | Screens: Screen A023 | SM-OP-072 | API-194;API-195 | Split | Covered | — |
| 53 | post_admin_sequences | POST | `/api/v1/admin/sequences` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-117 | API-262 | Alias | Covered | — |
| 54 | post_admin_signal_types | POST | `/api/v1/admin/signal-types` | Screens: Screen A023 | SM-OP-065 | API-047; API-ENH-D-003 | Partial | Covered | — |
| 55 | post_admin_social_accounts | POST | `/api/v1/admin/social/accounts` | Screens: Screen A053 | SM-OP-154 | API-113 | Alias | Covered | — |
| 56 | post_admin_social_sources | POST | `/api/v1/admin/social/sources` | SM-SVC-12: Used by SM-SVC-12-WF01 | SM-OP-145 | API-206 | Alias | Covered | — |
| 57 | post_admin_sources | POST | `/api/v1/admin/sources` | Screens: Screen A010 | SM-OP-031 | API-159 | Exact | Covered | — |
| 58 | patch_admin_sources_id | PATCH | `/api/v1/admin/sources/{id}` | Screens: Screen A010 | SM-OP-032 | API-179; API-ENH-D-001 | Partial | Covered | — |
| 59 | get_admin_suppressions | GET | `/api/v1/admin/suppressions` | SM-SVC-38: Used by SM-SVC-38-WF01 | SM-OP-022 | API-074;API-076 | Split | Covered | — |
| 60 | get_admin_users | GET | `/api/v1/admin/users` | Screens: Screen A002 | SM-OP-003 | API-019 | Alias (prefix) | Covered | — |
| 61 | post_admin_users_id_roles | POST | `/api/v1/admin/users/{id}/roles` | Screens: Screen A002 | SM-OP-004 | API-021;API-020 | Alias (prefix) | Covered | — |
| 62 | get_admin_whatsapp_accounts | GET | `/api/v1/admin/whatsapp/accounts` | SM-SVC-07: Used by SM-SVC-07-WF01 | SM-OP-130 | API-109;API-102; API-ENH-D-008 | Partial | Covered | — |
| 63 | post_admin_whatsapp_accounts | POST | `/api/v1/admin/whatsapp/accounts` | SM-SVC-07: Used by SM-SVC-07-WF01 | SM-OP-131 | API-107 | Alias | Covered | — |
| 64 | post_admin_whatsapp_templates | POST | `/api/v1/admin/whatsapp/templates` | SM-SVC-07: Used by SM-SVC-07-WF01 | SM-OP-132 | API-108 | Alias | Covered | — |
| 65 | post_admin_workflows | POST | `/api/v1/admin/workflows` | Screens: Screen A033 | SM-OP-099 | API-446;API-448 | Split | Covered | — |
| 66 | post_admin_workflows_pause | POST | `/api/v1/admin/workflows/pause` | Screens: Screen A033 | SM-OP-100 | API-445 | Exact | Covered | — |
| 67 | post_admin_workflows_id_resume | POST | `/api/v1/admin/workflows/{id}/resume` | Screens: Screen A033 | SM-OP-101 | API-469;API-450; API-ENH-D-006 | Partial | Covered | — |
| 68 | post_ads_drafts | POST | `/api/v1/ads/drafts` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-170 | API-294 | Exact | Covered | — |
| 69 | get_ads_metrics | GET | `/api/v1/ads/metrics` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-171 | API-295 | Exact | Covered | — |
| 70 | post_ads_id_launch | POST | `/api/v1/ads/{id}/launch` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-172 | API-318 | Alias | Covered | — |
| 71 | post_ads_id_pause | POST | `/api/v1/ads/{id}/pause` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-173 | API-319 | Alias | Covered | — |
| 72 | put_ai_budgets_id | PUT | `/api/v1/ai/budgets/{id}` | AI: Set soft/hard AI budget for scope (AIX-13) | V8 | API-137; API-146 | Alias | Covered | — |
| 73 | post_ai_content_screen | POST | `/api/v1/ai/content-screen` | AI: Screen untrusted content; returns flags only | V8 | — | New | Not covered | API-V12-H-054 |
| 74 | get_ai_eval_runs_id | GET | `/api/v1/ai/eval-runs/{id}` | AI: Evaluation run result with denominator | V8 | API-148 | Alias | Covered | — |
| 75 | get_ai_eval_suites | GET | `/api/v1/ai/eval-suites` | AI: List evaluation suites (AIX-05) | V8 | API-ENH-D-002; API-147 | Partial | Partially covered | API-V12-H-052 |
| 76 | post_ai_eval_suites_id_runs | POST | `/api/v1/ai/eval-suites/{id}/runs` | AI: Replay suite against candidate (AIX-06) | V8 | API-138 | Alias | Covered | — |
| 77 | post_ai_kill_switch | POST | `/api/v1/ai/kill-switch` | AI: Stop model/prompt/workflow (AIX-20) | V8 | API-451; API-144 | Partial | Partially covered | API-V12-H-056 |
| 78 | get_ai_models | GET | `/api/v1/ai/models` | AI: List model registry entries (AIX-02) | V8 | API-140; API-ADV-X1-12 | Partial | Partially covered | API-V12-H-049 |
| 79 | post_ai_models_id_promotion_requests | POST | `/api/v1/ai/models/{id}/promotion-requests` | AI: Request promotion; requires passing suites (AIX-05) | V8 | API-141 | Partial | Partially covered | API-V12-H-050 |
| 80 | get_ai_prompts | GET | `/api/v1/ai/prompts` | AI: List prompt versions (AIX-04) | V8 | API-142 | Partial | Partially covered | API-V12-H-051 |
| 81 | get_ai_red_team_results | GET | `/api/v1/ai/red-team/results` | AI: AI-INJ suite results (AIX-08) | V8 | API-ADV-X1-38 | Partial | Partially covered | API-V12-H-053 |
| 82 | get_ai_usage | GET | `/api/v1/ai/usage` | AI: Token usage and cost per accepted result (AIX-12, AIX-14) | V8 | API-135; API-136 | Partial | Partially covered | API-V12-H-055 |
| 83 | get_alerts | GET | `/api/v1/alerts` | SM-SVC-19: Used by SM-SVC-19-WF01 | SM-OP-082 | API-176 | Exact | Covered | — |
| 84 | post_alerts_id_read | POST | `/api/v1/alerts/{id}/read` | Screens: Screen A027 | SM-OP-084 | API-ENH-D-005 | New (Part 3.5b) | Covered | — |
| 85 | post_auth_login | POST | `/api/v1/auth/login` | Screens: Screen A001 | SM-OP-001 | API-001 | Alias (prefix) | Covered | — |
| 86 | post_auth_logout | POST | `/api/v1/auth/logout` | Screens: Screen A001 | SM-OP-005 | API-007;API-012 | Alias (prefix) | Covered | — |
| 87 | get_campaigns | GET | `/api/v1/campaigns` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-166 | API-311 | Alias | Covered | — |
| 88 | post_campaigns | POST | `/api/v1/campaigns` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-167 | API-292 | Exact | Covered | — |
| 89 | post_campaigns_id_approve | POST | `/api/v1/campaigns/{id}/approve` | SM-SVC-14: Used by SM-SVC-14-WF01 | SM-OP-168 | API-293 | Exact | Covered | — |
| 90 | post_campaigns_id_pause | POST | `/api/v1/campaigns/{id}/pause` | SM-SVC-30: Used by SM-SVC-30-WF01 | SM-OP-169 | API-316 | Alias | Covered | — |
| 91 | post_commercial_admin_external_grants | POST | `/api/v1/commercial/admin/external-grants` | SM-SVC-34: Used by SM-SVC-34-WF01 | SM-OP-293 | API-227 | Alias | Covered | — |
| 92 | post_commercial_admin_external_grants_id_control | POST | `/api/v1/commercial/admin/external-grants/{id}/control` | SM-SVC-34: Used by SM-SVC-34-WF01 | SM-OP-294 | API-ENH-D-017 | New (Part 3.5b) | Covered | — |
| 93 | get_commercial_workspace_admin_conflicts | GET | `/api/v1/commercial/workspace/admin/conflicts` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-UX-API-12 | API-473 | Alias | Covered | — |
| 94 | post_commercial_workspace_admin_conflicts_id_resolve | POST | `/api/v1/commercial/workspace/admin/conflicts/{id}/resolve` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-UX-API-13 | API-475;API-476 | Split | Covered | — |
| 95 | get_compliance_packs | GET | `/api/v1/compliance/packs` | Compliance: List jurisdiction packs (CJ-R01) | V8 | API-077 | Alias | Covered | — |
| 96 | get_compliance_packs_id_rules | GET | `/api/v1/compliance/packs/{id}/rules` | Compliance: Rules with legal source and status | V8 | API-077 | Partial | Partially covered | API-V12-H-057 |
| 97 | post_compliance_preflight | POST | `/api/v1/compliance/preflight` | Compliance: Send preflight decision (CJ-R02) | V8 | API-068 | Alias | Covered | — |
| 98 | get_consents | GET | `/api/v1/consents` | Compliance: Search consent ledger (CJ-R04) | V8 | API-076 | Partial | Partially covered | API-V12-H-058 |
| 99 | post_consents | POST | `/api/v1/consents` | SM-SVC-03: Used by SM-SVC-03-WF01 | V8 | API-066 | Exact | Covered | — |
| 100 | post_consents_id_withdraw | POST | `/api/v1/consents/{id}/withdraw` | Compliance: Withdraw consent and suppress (CJ-R05) | V8 | API-067; API-082 | Partial | Partially covered | API-V12-H-059 |
| 101 | get_contacts_verification_queue | GET | `/api/v1/contacts/verification-queue` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-077 | API-200 | Alias | Covered | — |
| 102 | patch_contacts_id | PATCH | `/api/v1/contacts/{id}` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-079 | API-197 | Alias | Covered | — |
| 103 | post_contacts_id_verify | POST | `/api/v1/contacts/{id}/verify` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-078 | API-174 | Exact | Covered | — |
| 104 | get_content | GET | `/api/v1/content` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-147 | API-299 | Alias | Covered | — |
| 105 | post_content_draft | POST | `/api/v1/content/draft` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-148 | API-284 | Exact | Covered | — |
| 106 | patch_content_id | PATCH | `/api/v1/content/{id}` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-149 | API-301 | Alias | Covered | — |
| 107 | post_content_id_approve | POST | `/api/v1/content/{id}/approve` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-150 | API-285 | Exact | Covered | — |
| 108 | get_contracts | GET | `/api/v1/contracts` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-194 | API-348 | Alias | Covered | — |
| 109 | post_contracts | POST | `/api/v1/contracts` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-195 | API-332 | Exact | Covered | — |
| 110 | post_contracts_id_approve | POST | `/api/v1/contracts/{id}/approve` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-198 | API-541;API-539 | Approval | Covered | — |
| 111 | get_deals | GET | `/api/v1/deals` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-085 | API-209 | Exact | Covered | — |
| 112 | post_deals | POST | `/api/v1/deals` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-086 | API-210 | Exact | Covered | — |
| 113 | get_deals_id | GET | `/api/v1/deals/{id}` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-087 | API-214;API-217 | Split | Covered | — |
| 114 | post_deals_id_assign | POST | `/api/v1/deals/{id}/assign` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-091 | API-216 | Alias | Covered | — |
| 115 | post_deals_id_close | POST | `/api/v1/deals/{id}/close` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-205 | API-386 | Exact | Covered | — |
| 116 | post_deals_id_invoices | POST | `/api/v1/deals/{id}/invoices` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-202 | API-390 | Alias | Covered | — |
| 117 | post_deals_id_lost | POST | `/api/v1/deals/{id}/lost` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-220 | API-387 | Exact | Covered | — |
| 118 | get_deals_id_objections | GET | `/api/v1/deals/{id}/objections` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-191 | API-343 | Alias | Covered | — |
| 119 | post_deals_id_objections | POST | `/api/v1/deals/{id}/objections` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-192 | API-331 | Exact | Covered | — |
| 120 | get_deals_id_payments | GET | `/api/v1/deals/{id}/payments` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-201 | API-393 | Alias | Covered | — |
| 121 | get_deals_id_proposals | GET | `/api/v1/deals/{id}/proposals` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-185 | API-334;API-335 | Split | Covered | — |
| 122 | post_deals_id_proposals | POST | `/api/v1/deals/{id}/proposals` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-186 | API-328 | Exact | Covered | — |
| 123 | post_deals_id_transition | POST | `/api/v1/deals/{id}/transition` | SM-SVC-29: Used by SM-SVC-29-WF01 | SM-OP-088 | API-211 | Exact | Covered | — |
| 124 | get_deployments | GET | `/api/v1/deployments` | Screens: Screen A095 | SM-OP-242 | API-421 | Exact | Covered | — |
| 125 | patch_deployments_id | PATCH | `/api/v1/deployments/{id}` | Screens: Screen A095 | SM-OP-244 | API-435 | Alias | Covered | — |
| 126 | post_deployments_id_approve | POST | `/api/v1/deployments/{id}/approve` | Screens: Screen A096 | SM-OP-243 | API-541;API-539 | Approval | Covered | — |
| 127 | get_dsar | GET | `/api/v1/dsar` | Compliance: Tenant DSAR queue | V8 | API-084 | Alias | Covered | — |
| 128 | post_dsar_id_complete | POST | `/api/v1/dsar/{id}/complete` | Compliance: Complete with evidence; legal-hold check | V8 | API-086 | Alias | Covered | — |
| 129 | post_dsar_id_verify | POST | `/api/v1/dsar/{id}/verify` | Compliance: Record identity verification | V8 | API-085 | Alias | Covered | — |
| 130 | post_engagement_check | POST | `/api/v1/engagement/check` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-097 | API-068 | Exact | Covered | — |
| 131 | get_enrollments | GET | `/api/v1/enrollments` | Screens: Screen A038 | SM-OP-120 | API-263 | Alias | Covered | — |
| 132 | post_enrollments_id_stop | POST | `/api/v1/enrollments/{id}/stop` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-119 | API-264 | Alias | Covered | — |
| 133 | get_events | GET | `/api/v1/events` | Screens: Screen A009 | SM-OP-027 | API-115 | Exact | Covered | — |
| 134 | get_events_business | GET | `/api/v1/events/business` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-175 | API-322 | Alias | Covered | — |
| 135 | post_events_business | POST | `/api/v1/events/business` | SM-SVC-16: Used by SM-SVC-16-WF01 | SM-OP-176 | API-323 | Alias | Covered | — |
| 136 | get_evidence | GET | `/api/v1/evidence` | Screens: Screen A017 | SM-OP-057 | API-186 | Alias | Covered | — |
| 137 | get_evidence_id | GET | `/api/v1/evidence/{id}` | Screens: Screen A017 | SM-OP-056 | API-163 | Exact | Covered | — |
| 138 | get_feedback | GET | `/api/v1/feedback` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-222 | API-431 | Alias | Covered | — |
| 139 | post_feedback | POST | `/api/v1/feedback` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-221 | API-418 | Exact | Covered | — |
| 140 | get_inbox | GET | `/api/v1/inbox` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-139 | API-247 | Exact | Covered | — |
| 141 | get_incidents | GET | `/api/v1/incidents` | Compliance: Incident register (CJ-R08) | V8 | API-070; API-092 | Alias | Covered | — |
| 142 | post_incidents | POST | `/api/v1/incidents` | Compliance: Open incident; clocks start | V8 | — | New | Not covered | API-V12-H-060 |
| 143 | post_incidents_id_notifications | POST | `/api/v1/incidents/{id}/notifications` | Compliance: Record authority/principal notification | V8 | — | New | Not covered | API-V12-H-061 |
| 144 | get_insurance_pilots | GET | `/api/v1/insurance/pilots` | SM-SVC-22: Used by SM-SVC-22-WF01 | SM-OP-236 | API-ENH-D-011 | New (Part 3.5b) | Covered | — |
| 145 | post_insurance_pilots_id_approve | POST | `/api/v1/insurance/pilots/{id}/approve` | SM-SVC-22: Used by SM-SVC-22-WF01 | SM-OP-238 | API-541;API-539 | Approval | Covered | — |
| 146 | get_integration_enquiries | GET | `/api/v1/integration-enquiries` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-239 | API-433 | Alias | Covered | — |
| 147 | post_integration_enquiries | POST | `/api/v1/integration-enquiries` | Screens: Screen A093 | SM-OP-240 | API-420 | Exact | Covered | — |
| 148 | post_integration_enquiries_id_approve | POST | `/api/v1/integration-enquiries/{id}/approve` | Screens: Screen A094 | SM-OP-241 | API-541;API-539 | Approval | Covered | — |
| 149 | get_integrations | GET | `/api/v1/integrations` | Screens: Screen A008 | SM-OP-023 | API-095 | Exact | Covered | — |
| 150 | post_invoices_id_payment_link | POST | `/api/v1/invoices/{id}/payment-link` | Screens: Screen A073 | SM-OP-207 | API-398 | Alias | Covered | — |
| 151 | get_knowledge_documents | GET | `/api/v1/knowledge/documents` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-013 | API-061 | Alias | Covered | — |
| 152 | post_knowledge_documents_id_review | POST | `/api/v1/knowledge/documents/{id}/review` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-014 | API-541;API-539 | Approval | Covered | — |
| 153 | get_knowledge_search | GET | `/api/v1/knowledge/search` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-015 | API-052 | Exact | Covered | — |
| 154 | post_knowledge_uploads | POST | `/api/v1/knowledge/uploads` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-012 | API-051 | Exact | Covered | — |
| 155 | get_landing_pages | GET | `/api/v1/landing-pages` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-161 | API-308 | Alias | Covered | — |
| 156 | post_landing_pages | POST | `/api/v1/landing-pages` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-162 | API-309 | Alias | Covered | — |
| 157 | post_landing_pages_id_publish | POST | `/api/v1/landing-pages/{id}/publish` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-163 | API-492 | Alias | Covered | — |
| 158 | get_market_competitors | GET | `/api/v1/market/competitors` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-227 | API-178 | Exact | Covered | — |
| 159 | get_matches | GET | `/api/v1/matches` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-068 | API-192 | Alias | Covered | — |
| 160 | post_matches_recompute | POST | `/api/v1/matches/recompute` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-069 | API-170 | Exact | Covered | — |
| 161 | get_me | GET | `/api/v1/me` | Screens: Screen A001 | SM-OP-002 | API-002 | Alias (prefix) | Covered | — |
| 162 | get_meetings | GET | `/api/v1/meetings` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-121 | API-268 | Alias | Covered | — |
| 163 | post_meetings_book | POST | `/api/v1/meetings/book` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-123 | API-243 | Exact | Covered | — |
| 164 | post_messages_draft | POST | `/api/v1/messages/draft` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-103 | API-237 | Exact | Covered | — |
| 165 | post_messages_drafts_id_review | POST | `/api/v1/messages/drafts/{id}/review` | SM-SVC-06: Used by SM-SVC-06-WF01 | SM-OP-106 | API-541;API-539 | Approval | Covered | — |
| 166 | post_messages_send | POST | `/api/v1/messages/send` | SM-SVC-09: Used by SM-SVC-09-WF01 | SM-OP-108 | API-238 | Exact | Covered | — |
| 167 | get_messages_id | GET | `/api/v1/messages/{id}` | SM-SVC-09: Used by SM-SVC-09-WF01 | SM-OP-110 | API-252;API-257; API-ENH-D-007 | Partial | Covered | — |
| 168 | get_metrics_forecast | GET | `/api/v1/metrics/forecast` | SM-SVC-24: Used by SM-SVC-24-WF01 | SM-OP-229 | API-389 | Exact | Covered | — |
| 169 | get_metrics_funnel | GET | `/api/v1/metrics/funnel` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-127 | API-537 | Exact | Covered | — |
| 170 | get_metrics_revenue | GET | `/api/v1/metrics/revenue` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-223 | API-388 | Exact | Covered | — |
| 171 | get_needs | GET | `/api/v1/needs` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-066 | API-168 | Exact | Covered | — |
| 172 | post_needs_id_verify | POST | `/api/v1/needs/{id}/verify` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-067 | API-169 | Exact | Covered | — |
| 173 | post_negotiations_id_review | POST | `/api/v1/negotiations/{id}/review` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-193 | API-347 | Alias | Covered | — |
| 174 | get_onboarding | GET | `/api/v1/onboarding` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-209 | API-412 | Exact | Covered | — |
| 175 | post_onboarding_id_assign | POST | `/api/v1/onboarding/{id}/assign` | SM-SVC-22: Used by SM-SVC-22-WF01 | SM-OP-212 | API-425 | Alias | Covered | — |
| 176 | post_onboarding_id_complete | POST | `/api/v1/onboarding/{id}/complete` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-211 | API-413 | Exact | Covered | — |
| 177 | get_opportunities | GET | `/api/v1/opportunities` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-070 | API-171 | Exact | Covered | — |
| 178 | post_opportunities_id_review | POST | `/api/v1/opportunities/{id}/review` | Screens: Screen A027 | SM-OP-081 | API-175 | Exact | Covered | — |
| 179 | post_opportunities_id_score | POST | `/api/v1/opportunities/{id}/score` | SM-SVC-04: Used by SM-SVC-04-WF01 | SM-OP-071 | API-172 | Exact | Covered | — |
| 180 | get_organizations | GET | `/api/v1/organizations` | SM-SVC-02: Used by SM-SVC-02-WF01 | SM-OP-059 | API-164 | Exact | Covered | — |
| 181 | post_organizations | POST | `/api/v1/organizations` | SM-SVC-02: Used by SM-SVC-02-WF01 | SM-OP-060 | API-165 | Exact | Covered | — |
| 182 | get_organizations_id | GET | `/api/v1/organizations/{id}` | SM-SVC-02: Used by SM-SVC-02-WF01 | SM-OP-061 | API-189 | Alias | Covered | — |
| 183 | get_organizations_id_360 | GET | `/api/v1/organizations/{id}/360` | SM-SVC-05: Used by SM-SVC-05-WF01 | SM-OP-096 | API-213 | Exact | Covered | — |
| 184 | get_organizations_id_contacts | GET | `/api/v1/organizations/{id}/contacts` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-073 | API-173 | Exact | Covered | — |
| 185 | post_organizations_id_contacts_discover | POST | `/api/v1/organizations/{id}/contacts/discover` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-074 | API-196 | Alias | Covered | — |
| 186 | post_organizations_id_merge | POST | `/api/v1/organizations/{id}/merge` | SM-SVC-03: Used by SM-SVC-03-WF01 | SM-OP-062 | API-190;API-191 | Split | Covered | — |
| 187 | post_partner_pilots | POST | `/api/v1/partner-pilots` | SM-SVC-32: Used by SM-SVC-32-WF01 | SM-OP-216 | API-419 | Alias | Covered | — |
| 188 | get_partners | GET | `/api/v1/partners` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-213 | API-427 | Alias | Covered | — |
| 189 | post_partners | POST | `/api/v1/partners` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-214 | API-414 | Exact | Covered | — |
| 190 | post_payments_id_reconcile | POST | `/api/v1/payments/{id}/reconcile` | SM-SVC-39: Used by SM-SVC-39-WF01 | SM-OP-206 | API-394;API-395;API-396 | Split | Covered | — |
| 191 | post_pilots | POST | `/api/v1/pilots` | SM-SVC-22: Used by SM-SVC-22-WF01 | SM-OP-237 | API-419 | Exact | Covered | — |
| 192 | post_pilots_id_status | POST | `/api/v1/pilots/{id}/status` | SM-SVC-22: Used by SM-SVC-22-WF01 | SM-OP-215 | API-415 | Exact | Covered | — |
| 193 | post_privacy_requests | POST | `/api/v1/privacy/requests` | Screens: Screen A013 | SM-OP-041 | API-069 | Exact | Covered | — |
| 194 | get_products | GET | `/api/v1/products` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-006 | API-048 | Exact | Covered | — |
| 195 | get_products_id | GET | `/api/v1/products/{id}` | SM-SVC-25: Used by SM-SVC-25-WF01 | SM-OP-007 | API-054 | Alias | Covered | — |
| 196 | post_proposals_id_review | POST | `/api/v1/proposals/{id}/review` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-187 | API-541;API-539 | Approval | Covered | — |
| 197 | post_public_cookie_consent | POST | `/api/v1/public/cookie-consent` | Compliance: Record cookie choice with notice version (CJ-R12) | V8 | — | New | Not covered | API-V12-H-062 |
| 198 | post_public_data_rights_requests | POST | `/api/v1/public/data-rights-requests` | Compliance: Public DSAR intake, rate-limited (CJ-R07) | V8 | API-069 | Alias | Covered | — |
| 199 | get_quotes | GET | `/api/v1/quotes` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-188 | API-338 | Alias | Covered | — |
| 200 | post_quotes | POST | `/api/v1/quotes` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-189 | API-329 | Exact | Covered | — |
| 201 | post_quotes_id_approve | POST | `/api/v1/quotes/{id}/approve` | SM-SVC-17: Used by SM-SVC-17-WF01 | SM-OP-190 | API-330 | Exact | Covered | — |
| 202 | get_renewals | GET | `/api/v1/renewals` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-217 | API-416 | Exact | Covered | — |
| 203 | post_renewals_id_review | POST | `/api/v1/renewals/{id}/review` | SM-SVC-23: Used by SM-SVC-23-WF01 | SM-OP-218 | API-417 | Exact | Covered | — |
| 204 | get_research_plans | GET | `/api/v1/research/plans` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-049 | API-180 | Alias | Covered | — |
| 205 | post_research_plans | POST | `/api/v1/research/plans` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-050 | API-160 | Exact | Covered | — |
| 206 | patch_research_plans_id | PATCH | `/api/v1/research/plans/{id}` | Screens: Screen A015 | SM-OP-052 | API-181 | Alias | Covered | — |
| 207 | get_research_results | GET | `/api/v1/research/results` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-053 | API-162 | Exact | Covered | — |
| 208 | post_research_run | POST | `/api/v1/research/run` | Screens: Screen A015 | SM-OP-051 | API-161 | Exact | Covered | — |
| 209 | get_research_runs_id | GET | `/api/v1/research/runs/{id}` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-054 | API-183 | Alias | Covered | — |
| 210 | get_sales_action_plans | GET | `/api/v1/sales/action-plans` | Screens: Screen A102 | SM-OP-269 | API-453 | Alias | Covered | — |
| 211 | post_sales_action_plans | POST | `/api/v1/sales/action-plans` | Screens: Screen A102 | SM-OP-270 | API-454;API-455 | Split | Covered | — |
| 212 | post_sales_action_plans_id_control | POST | `/api/v1/sales/action-plans/{id}/control` | Screens: Screen A102 | SM-OP-271 | API-456;API-457;API-458;API-541;API-539 | Split | Covered | — |
| 213 | get_sales_bids | GET | `/api/v1/sales/bids` | SM-SVC-19: Used by SM-SVC-19-WF01 | SM-OP-277 | API-362 | Alias | Covered | — |
| 214 | post_sales_bids | POST | `/api/v1/sales/bids` | SM-SVC-19: Used by SM-SVC-19-WF01 | SM-OP-278 | API-363 | Alias | Covered | — |
| 215 | patch_sales_bids_id | PATCH | `/api/v1/sales/bids/{id}` | SM-SVC-19: Used by SM-SVC-19-WF01 | SM-OP-279 | API-365 | Alias | Covered | — |
| 216 | post_sales_bids_id_control | POST | `/api/v1/sales/bids/{id}/control` | Screens: Screen A104 | SM-OP-280 | API-366;API-367;API-368;API-369;API-541;API-539 | Split | Covered | — |
| 217 | get_sales_data_transfers | GET | `/api/v1/sales/data-transfers` | Screens: Screen A103 | SM-OP-272 | API-530 | Alias | Covered | — |
| 218 | post_sales_data_transfers | POST | `/api/v1/sales/data-transfers` | Screens: Screen A103 | SM-OP-273 | API-531;API-534 | Split | Covered | — |
| 219 | post_sales_data_transfers_id_complete | POST | `/api/v1/sales/data-transfers/{id}/complete` | Screens: Screen A103 | SM-OP-274 | API-532 | Alias | Covered | — |
| 220 | post_sales_data_transfers_id_control | POST | `/api/v1/sales/data-transfers/{id}/control` | Screens: Screen A103 | SM-OP-275 | API-536;API-541;API-539 | Split | Covered | — |
| 221 | get_sales_data_transfers_id_download | GET | `/api/v1/sales/data-transfers/{id}/download` | Screens: Screen A103 | SM-OP-276 | API-535 | Alias | Covered | — |
| 222 | get_sales_domains | GET | `/api/v1/sales/domains` | Screens: Screen A100 | SM-OP-258 | API-044 | Alias | Covered | — |
| 223 | post_sales_domains | POST | `/api/v1/sales/domains` | Screens: Screen A100 | SM-OP-259 | API-045 | Alias | Covered | — |
| 224 | post_sales_domains_id_control | POST | `/api/v1/sales/domains/{id}/control` | Screens: Screen A100 | SM-OP-260 | API-046; API-ENH-D-012 | Partial | Covered | — |
| 225 | post_sales_memberships | POST | `/api/v1/sales/memberships` | Screens: Screen A099 | SM-OP-253 | API-020;API-022 | Split | Covered | — |
| 226 | post_sales_milestones_id_accept | POST | `/api/v1/sales/milestones/{id}/accept` | SM-SVC-31: Used by SM-SVC-31-WF01 | SM-OP-286 | API-383;API-384; API-ENH-D-016 | Partial | Covered | — |
| 227 | get_sales_notifications | GET | `/api/v1/sales/notifications` | Screens: Screen A106 | SM-OP-287 | API-549 | Alias | Covered | — |
| 228 | patch_sales_notifications_id | PATCH | `/api/v1/sales/notifications/{id}` | Screens: Screen A106 | SM-OP-288 | API-550;API-552 | Split | Covered | — |
| 229 | get_sales_orders | GET | `/api/v1/sales/orders` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-281 | API-370 | Alias | Covered | — |
| 230 | post_sales_orders | POST | `/api/v1/sales/orders` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-282 | API-371 | Alias | Covered | — |
| 231 | patch_sales_orders_id | PATCH | `/api/v1/sales/orders/{id}` | SM-SVC-20: Used by SM-SVC-20-WF01 | SM-OP-283 | API-373 | Alias | Covered | — |
| 232 | post_sales_orders_id_control | POST | `/api/v1/sales/orders/{id}/control` | SM-SVC-28: Used by SM-SVC-28-WF01 | SM-OP-284 | API-374;API-375;API-376;API-378 | Split | Covered | — |
| 233 | post_sales_orders_id_milestones | POST | `/api/v1/sales/orders/{id}/milestones` | SM-SVC-31: Used by SM-SVC-31-WF01 | SM-OP-285 | API-377 | Alias | Covered | — |
| 234 | get_sales_service_invoices | GET | `/api/v1/sales/service-invoices` | Screens: Screen A101 | SM-OP-265 | API-526 | Alias | Covered | — |
| 235 | post_sales_service_invoices_id_reconcile | POST | `/api/v1/sales/service-invoices/{id}/reconcile` | Screens: Screen A101 | SM-OP-266 | API-ENH-D-013 | New (Part 3.5b) | Covered | — |
| 236 | get_sales_service_plans | GET | `/api/v1/sales/service-plans` | Screens: Screen A101 | SM-OP-261 | API-519 | Alias | Covered | — |
| 237 | post_sales_service_plans | POST | `/api/v1/sales/service-plans` | Screens: Screen A101 | SM-OP-262 | API-520;API-541;API-539 | Split | Covered | — |
| 238 | get_sales_service_subscriptions | GET | `/api/v1/sales/service-subscriptions` | Screens: Screen A101 | SM-OP-263 | API-521 | Alias | Covered | — |
| 239 | post_sales_service_subscriptions_id_control | POST | `/api/v1/sales/service-subscriptions/{id}/control` | Screens: Screen A101 | SM-OP-264 | API-522;API-523;API-524;API-525 | Split | Covered | — |
| 240 | get_sales_startups | GET | `/api/v1/sales/startups` | Screens: Screen A099 | SM-OP-250 | API-029 | Alias | Covered | — |
| 241 | post_sales_startups | POST | `/api/v1/sales/startups` | Screens: Screen A099 | SM-OP-251 | API-030 | Alias | Covered | — |
| 242 | patch_sales_startups_id | PATCH | `/api/v1/sales/startups/{id}` | Screens: Screen A099 | SM-OP-252 | API-031;API-039 | Split | Covered | — |
| 243 | post_sales_support_grants | POST | `/api/v1/sales/support-grants` | Screens: Screen A099 | SM-OP-254 | API-024;API-025 | Split | Covered | — |
| 244 | get_sales_templates | GET | `/api/v1/sales/templates` | Screens: Screen A100 | SM-OP-255 | API-033 | Alias | Covered | — |
| 245 | post_sales_templates | POST | `/api/v1/sales/templates` | Screens: Screen A100 | SM-OP-256 | API-034 | Alias | Covered | — |
| 246 | post_sales_templates_id_control | POST | `/api/v1/sales/templates/{id}/control` | Screens: Screen A100 | SM-OP-257 | API-035;API-036;API-037;API-541;API-539 | Split | Covered | — |
| 247 | get_sales_tenants | GET | `/api/v1/sales/tenants` | Screens: Screen A099 | SM-OP-247 | API-026 | Alias | Covered | — |
| 248 | post_sales_tenants | POST | `/api/v1/sales/tenants` | Screens: Screen A099 | SM-OP-248 | API-027 | Alias | Covered | — |
| 249 | post_sales_tenants_id_control | POST | `/api/v1/sales/tenants/{id}/control` | Screens: Screen A099 | SM-OP-249 | API-028 | Alias | Covered | — |
| 250 | get_sales_usage_charges | GET | `/api/v1/sales/usage-charges` | Screens: Screen A101 | SM-OP-267 | API-528; API-ENH-D-014 | Partial | Covered | — |
| 251 | post_sales_usage_charges_id_adjust | POST | `/api/v1/sales/usage-charges/{id}/adjust` | Screens: Screen A101 | SM-OP-268 | API-ENH-D-015 | New (Part 3.5b) | Covered | — |
| 252 | get_seo_audit | GET | `/api/v1/seo/audit` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-157 | API-288 | Exact | Covered | — |
| 253 | post_seo_audit_run | POST | `/api/v1/seo/audit/run` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-159 | API-289 | Alias | Covered | — |
| 254 | post_seo_tasks | POST | `/api/v1/seo/tasks` | SM-SVC-13: Used by SM-SVC-13-WF01 | SM-OP-158 | API-289 | Exact | Covered | — |
| 255 | get_sequences | GET | `/api/v1/sequences` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-116 | API-261 | Alias | Covered | — |
| 256 | post_sequences_id_enroll | POST | `/api/v1/sequences/{id}/enroll` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-118 | API-242 | Exact | Covered | — |
| 257 | get_signals | GET | `/api/v1/signals` | Screens: Screen A019 | SM-OP-063 | API-166 | Exact | Covered | — |
| 258 | post_signals_id_review | POST | `/api/v1/signals/{id}/review` | Screens: Screen A019 | SM-OP-064 | API-167 | Exact | Covered | — |
| 259 | get_social_posts | GET | `/api/v1/social/posts` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-151 | API-302 | Alias | Covered | — |
| 260 | post_social_posts | POST | `/api/v1/social/posts` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-152 | API-286 | Exact | Covered | — |
| 261 | post_social_posts_id_cancel | POST | `/api/v1/social/posts/{id}/cancel` | SM-SVC-27: Used by SM-SVC-27-WF01 | SM-OP-155 | API-303 | Alias | Covered | — |
| 262 | get_social_signals | GET | `/api/v1/social/signals` | SM-SVC-12: Used by SM-SVC-12-WF01 | SM-OP-144 | API-177 | Exact | Covered | — |
| 263 | get_social_status | GET | `/api/v1/social/status` | SM-SVC-11: Used by SM-SVC-11-WF01 | SM-OP-153 | API-287 | Exact | Covered | — |
| 264 | get_sources | GET | `/api/v1/sources` | SM-SVC-01: Used by SM-SVC-01-WF01 | SM-OP-030 | API-158 | Exact | Covered | — |
| 265 | get_suppressions | GET | `/api/v1/suppressions` | Compliance: List suppressions | V8 | API-074 | Alias | Covered | — |
| 266 | get_tasks | GET | `/api/v1/tasks` | SM-SVC-24: Used by SM-SVC-24-WF01 | SM-OP-128 | API-265 | Alias | Covered | — |
| 267 | patch_tasks_id | PATCH | `/api/v1/tasks/{id}` | SM-SVC-24: Used by SM-SVC-24-WF01 | SM-OP-129 | API-266 | Alias | Covered | — |
| 268 | get_threads | GET | `/api/v1/threads` | SM-SVC-26: Used by SM-SVC-26-WF01 | SM-OP-113 | API-241 | Exact | Covered | — |
| 269 | post_threads_id_assign | POST | `/api/v1/threads/{id}/assign` | SM-SVC-08: Used by SM-SVC-08-WF01 | SM-OP-140 | API-248 | Exact | Covered | — |
| 270 | post_threads_id_handoff | POST | `/api/v1/threads/{id}/handoff` | SM-SVC-26: Used by SM-SVC-26-WF01 | SM-OP-115 | API-259 | Alias | Covered | — |
| 271 | get_threads_id_messages | GET | `/api/v1/threads/{id}/messages` | SM-SVC-26: Used by SM-SVC-26-WF01 | SM-OP-114 | API-257 | Alias | Covered | — |
| 272 | post_webhooks_calendar | POST | `/api/v1/webhooks/calendar` | SM-SVC-10: Used by SM-SVC-10-WF01 | SM-OP-124 | API-244 | Exact | Covered | — |
| 273 | post_webhooks_email | POST | `/api/v1/webhooks/email` | SM-SVC-09: Used by SM-SVC-09-WF01 | SM-OP-109 | API-239 | Exact | Covered | — |
| 274 | post_webhooks_esign | POST | `/api/v1/webhooks/esign` | SM-SVC-18: Used by SM-SVC-18-WF01 | SM-OP-199 | API-333 | Exact | Covered | — |
| 275 | post_webhooks_events | POST | `/api/v1/webhooks/events` | SM-SVC-16: Used by SM-SVC-16-WF01 | SM-OP-179 | API-297 | Exact | Covered | — |
| 276 | post_webhooks_inbound | POST | `/api/v1/webhooks/inbound` | SM-SVC-26: Used by SM-SVC-26-WF01 | SM-OP-112 | API-240 | Exact | Covered | — |
| 277 | post_webhooks_payment | POST | `/api/v1/webhooks/payment` | SM-SVC-21: Used by SM-SVC-21-WF01 | SM-OP-204 | API-385 | Exact | Covered | — |
| 278 | get_webhooks_whatsapp | GET | `/api/v1/webhooks/whatsapp` | SM-SVC-09: Used by SM-SVC-09-WF01 | SM-OP-133 | API-249 | Exact | Covered | — |
| 279 | post_webhooks_whatsapp | POST | `/api/v1/webhooks/whatsapp` | SM-SVC-09: Used by SM-SVC-09-WF01 | SM-OP-134 | API-245 | Exact | Covered | — |
| 280 | get_whatsapp_conversations | GET | `/api/v1/whatsapp/conversations` | Screens: Screen A045 | SM-OP-135 | API-241 | Alias | Covered | — |
| 281 | get_workflows | GET | `/api/v1/workflows` | Screens: Screen A033 | SM-OP-098 | API-444 | Exact | Covered | — |
| 282 | get_workflows_id_executions | GET | `/api/v1/workflows/{id}/executions` | Screens: Screen A033 | SM-OP-102 | API-466 | Alias | Covered | — |


#### 11.8.4.2.3 Historical operations not carried into Appendix A (30)

These are mostly public, portal-token and provider-callback routes. FSD 25 V5 keeps them in the historical registry as candidates ("exact source operations retained"), and Part 3.2 implements them; they are therefore retained, and Appendix A is treated as incomplete for the public and callback surfaces rather than as a deletion (DEC-640).

| Source op | Method | Path | Purpose | Blueprint op(s) |
|---|---|---|---|---|
| SM-OP-017 | GET | `/api/v1/public/preferences/{token}` | Read scoped preference state | API-083 |
| SM-OP-019 | POST | `/api/v1/opt-out` | Suppress and cancel scheduled sends; enrollment hook when enabled | API-067 |
| SM-OP-033 | POST | `/api/v1/internal/ai/run` | Internal model call with cost reservation | API-134 |
| SM-OP-045 | GET | `/api/v1/health` | Liveness; no database required | API-117 |
| SM-OP-046 | GET | `/api/v1/ready` | Readiness check without sensitive details | API-118 |
| SM-OP-092 | GET | `/api/v1/public/forms/{slug}` | Read published enquiry form | API-228 |
| SM-OP-093 | POST | `/api/v1/public/leads` | Capture valid consented enquiry | API-212 |
| SM-OP-122 | GET | `/api/v1/public/meeting-slots/{token}` | Read scoped available slots | API-272 |
| SM-OP-137 | POST | `/api/v1/public/chat` | Answer approved FAQ and capture consented lead | API-246 |
| SM-OP-164 | GET | `/api/v1/public/pages/{slug}` | Read published landing page | API-290 |
| SM-OP-165 | POST | `/api/v1/public/events` | Record minimized attribution event | API-291 |
| SM-OP-177 | GET | `/api/v1/public/events/{id}` | Read published event | API-326 |
| SM-OP-178 | POST | `/api/v1/events/register` | Register authorized attendee | API-296 |
| SM-OP-182 | POST | `/api/v1/public/referrals` | Submit authorized referral | API-298 |
| SM-OP-196 | GET | `/api/v1/public/agreements/{token}` | Read scoped agreement | API-358 |
| SM-OP-197 | POST | `/api/v1/public/agreements/{token}/sign` | Initiate authorized e-sign provider flow | API-359 |
| SM-OP-203 | GET | `/api/v1/public/payment-status/{token}` | Read scoped payment status | API-409 |
| SM-OP-210 | GET | `/api/v1/public/onboarding/{token}` | Read customer scoped next steps | API-437 |
| SM-OP-289 | GET | `/api/v1/commercial/public/site/pages/{slug}` | Read only currently published approved website snapshot for resolved verified host and locale. | API-290 |
| SM-OP-290 | GET | `/api/v1/commercial/admin/website/pages` | List startup-owned website drafts and publications. | API-486 |
| SM-OP-291 | POST | `/api/v1/commercial/admin/website/pages` | Create immutable draft or edit by creating next draft revision. | API-487;API-488 |
| SM-OP-292 | POST | `/api/v1/commercial/admin/website/pages/{id}/control` | Validate/preview/submit/approve/publish/unpublish or rollback approved revision. | API-489;API-490;API-492;API-494;API-495;API-541;API-539 |
| SM-OP-295 | POST | `/api/v1/commercial/portal/external-grants/accept` | Redeem a one-time invitation after identity verification; bind grant to authenticated external identity. | API-013 |
| SM-OP-296 | POST | `/api/v1/commercial/portal/documents` | Request upload for a specifically granted onboarding or project request; never knowledge ingestion. | API-235 |
| SM-OP-297 | POST | `/api/v1/commercial/portal/documents/{id}/complete` | Complete own quarantined document upload and enqueue scan. | API-236; API-ENH-D-018 |
| SM-OP-298 | GET | `/api/v1/commercial/portal/overview` | Own customer dashboard with authorized lead, agreement, order and onboarding summaries. | API-436 |
| SM-OP-299 | GET | `/api/v1/commercial/portal/quotations/{id}` | Read approved recipient-specific quote/proposal. | API-354;API-355 |
| SM-OP-300 | POST | `/api/v1/commercial/portal/quotations/{id}/respond` | Accept or request revision of an approved quotation; creates internal review event. | API-356;API-357 |
| SM-OP-301 | GET | `/api/v1/commercial/portal/orders/{id}` | Own order or project fulfillment status. | API-382 |
| SM-OP-302 | POST | `/api/v1/commercial/portal/requests` | Own support, feedback, renewal or privacy request with typed kind. | API-440;API-069 |


### 11.8.4.3 Appendix A2 (48 enterprise operations)

| # | V12 operationId | Method | V12 path | Tag | Summary | Blueprint operation(s) before | Relation | Before | Blueprint operation after |
|---|---|---|---|---|---|---|---|---|---|
| 1 | get_api_scim_v2_Groups | GET | `/api/scim/v2/Groups` | SCIM | SCIM list groups | — | New | Not covered | API-V12-H-026 |
| 2 | post_api_scim_v2_Groups | POST | `/api/scim/v2/Groups` | SCIM | SCIM create group | — | New | Not covered | API-V12-H-027 |
| 3 | get_api_scim_v2_Users | GET | `/api/scim/v2/Users` | SCIM | SCIM list users | — | New | Not covered | API-V12-H-021 |
| 4 | post_api_scim_v2_Users | POST | `/api/scim/v2/Users` | SCIM | SCIM create user | — | New | Not covered | API-V12-H-022 |
| 5 | delete_api_scim_v2_Users_id | DELETE | `/api/scim/v2/Users/{id}` | SCIM | SCIM de-provision user | — | New | Not covered | API-V12-H-025 |
| 6 | get_api_scim_v2_Users_id | GET | `/api/scim/v2/Users/{id}` | SCIM | SCIM read user | — | New | Not covered | API-V12-H-023 |
| 7 | patch_api_scim_v2_Users_id | PATCH | `/api/scim/v2/Users/{id}` | SCIM | SCIM update user | — | New | Not covered | API-V12-H-024 |
| 8 | get_api_keys | GET | `/api/v1/api-keys` | Developer | List API keys (prefix only) | CAP-X3-23 (A3, proposal) | Partial | Partially covered | API-V12-H-001 |
| 9 | post_api_keys | POST | `/api/v1/api-keys` | Developer | Create API key (value returned once) | CAP-X3-23 (A3, proposal) | Partial | Partially covered | API-V12-H-002 |
| 10 | post_api_keys_id_revoke | POST | `/api/v1/api-keys/{id}/revoke` | Developer | Revoke API key | CAP-X3-23 (A3, proposal) | Partial | Partially covered | API-V12-H-003 |
| 11 | get_audit_events | GET | `/api/v1/audit-events` | Audit | Search audit trail | API-121 | Alias | Covered | existing |
| 12 | post_audit_exports | POST | `/api/v1/audit-exports` | Audit | Export audit events | API-122 | Alias | Covered | existing |
| 13 | get_billing_invoices | GET | `/api/v1/billing/invoices` | Billing | List invoices | API-526; API-515 | Alias | Covered | existing |
| 14 | post_billing_invoices_preview | POST | `/api/v1/billing/invoices/preview` | Billing | Preview invoice with tax | — | New | Not covered | API-V12-H-035 |
| 15 | get_connectors | GET | `/api/v1/connectors` | Integrations | Connector catalogue | API-095 | Partial | Partially covered | API-V12-H-037 |
| 16 | get_connectors_id_health | GET | `/api/v1/connectors/{id}/health` | Integrations | Connector health | API-102 | Alias | Covered | existing |
| 17 | post_connectors_id_installations | POST | `/api/v1/connectors/{id}/installations` | Integrations | Install connector | API-097 | Partial | Partially covered | API-V12-H-038 |
| 18 | get_encryption_keys | GET | `/api/v1/encryption-keys` | Data | Read key configuration | CAP-X3-15 (A3, proposal) | Partial | Partially covered | API-V12-H-039 |
| 19 | put_encryption_keys | PUT | `/api/v1/encryption-keys` | Data | Set platform or customer-managed key | CAP-X3-15 (A3, proposal) | Partial | Partially covered | API-V12-H-040 |
| 20 | get_exports | GET | `/api/v1/exports` | Data | List data exports | API-530 | Alias | Covered | existing |
| 21 | post_exports | POST | `/api/v1/exports` | Data | Request tenant export | API-534 | Alias | Covered | existing |
| 22 | post_exports_id_approve | POST | `/api/v1/exports/{id}/approve` | Data | Approve export (second approver) | API-541; API-539 | Approval | Covered | existing |
| 23 | post_identity_domains | POST | `/api/v1/identity/domains` | Identity | Add domain for verification | — | New | Not covered | API-V12-H-018 |
| 24 | post_identity_domains_id_verify | POST | `/api/v1/identity/domains/{id}/verify` | Identity | Verify domain DNS TXT record | — | New | Not covered | API-V12-H-019 |
| 25 | put_identity_policies | PUT | `/api/v1/identity/policies` | Identity | Set MFA and session policy | CAP-X3-14 (A3, proposal) | Partial | Partially covered | API-V12-H-020 |
| 26 | get_identity_sso | GET | `/api/v1/identity/sso` | Identity | Read tenant SSO configuration | — | New | Not covered | API-V12-H-015 |
| 27 | put_identity_sso | PUT | `/api/v1/identity/sso` | Identity | Update SSO configuration | — | New | Not covered | API-V12-H-016 |
| 28 | post_identity_sso_test | POST | `/api/v1/identity/sso/test` | Identity | Test IdP connection | — | New | Not covered | API-V12-H-017 |
| 29 | get_locales | GET | `/api/v1/locales` | Global | Supported locales and coverage | CAP-X3-27 (A3, proposal) | Partial | Partially covered | API-V12-H-044 |
| 30 | get_ops_incidents | GET | `/api/v1/ops/incidents` | Operations | Operational incidents | API-128 | Alias | Covered | existing |
| 31 | post_ops_incidents | POST | `/api/v1/ops/incidents` | Operations | Declare incident | API-128 | Partial | Partially covered | API-V12-H-045 |
| 32 | get_public_status | GET | `/api/v1/public/status` | Operations | Public status summary | CAP-X3-12 (A3, proposal) | Partial | Partially covered | API-V12-H-046 |
| 33 | get_roles | GET | `/api/v1/roles` | Access | List roles | — | New | Not covered | API-V12-H-029 |
| 34 | post_roles | POST | `/api/v1/roles` | Access | Create custom role (SoD checked) | — | New | Not covered | API-V12-H-030 |
| 35 | delete_roles_id | DELETE | `/api/v1/roles/{id}` | Access | Retire role | — | New | Not covered | API-V12-H-032 |
| 36 | patch_roles_id | PATCH | `/api/v1/roles/{id}` | Access | Update role | — | New | Not covered | API-V12-H-031 |
| 37 | get_sandboxes | GET | `/api/v1/sandboxes` | Data | List sandboxes | — | New | Not covered | API-V12-H-041 |
| 38 | post_sandboxes | POST | `/api/v1/sandboxes` | Data | Create sandbox | — | New | Not covered | API-V12-H-042 |
| 39 | post_sandboxes_id_promotions | POST | `/api/v1/sandboxes/{id}/promotions` | Data | Request configuration promotion | API-039 (revision only) | Partial | Partially covered | API-V12-H-043 |
| 40 | get_security_findings | GET | `/api/v1/security/findings` | Security | Vulnerability findings (operator) | CAP-X3-19 (A3, proposal) | Partial | Partially covered | API-V12-H-047 |
| 41 | post_security_findings | POST | `/api/v1/security/findings` | Security | Log finding | CAP-X3-19 (A3, proposal) | Partial | Partially covered | API-V12-H-048 |
| 42 | get_siem_sinks | GET | `/api/v1/siem-sinks` | Audit | List SIEM destinations | — | New | Not covered | API-V12-H-033 |
| 43 | post_siem_sinks | POST | `/api/v1/siem-sinks` | Audit | Add SIEM destination | — | New | Not covered | API-V12-H-034 |
| 44 | post_tax_quote | POST | `/api/v1/tax/quote` | Billing | Tax determination for a line | API-339 (embedded in quote) | Partial | Partially covered | API-V12-H-036 |
| 45 | get_webhook_deliveries | GET | `/api/v1/webhook-deliveries` | Developer | Delivery log | CAP-X3-23 (A3, proposal) | Partial | Partially covered | API-V12-H-013 |
| 46 | get_webhooks | GET | `/api/v1/webhooks` | Developer | List webhook endpoints | CAP-X3-23 (A3, proposal) | Partial | Partially covered | API-V12-H-009 |
| 47 | post_webhooks | POST | `/api/v1/webhooks` | Developer | Add webhook endpoint | CAP-X3-23 (A3, proposal) | Partial | Partially covered | API-V12-H-010 |
| 48 | post_webhooks_id_test | POST | `/api/v1/webhooks/{id}/test` | Developer | Send signed test event | CAP-X3-23 (A3, proposal) | Partial | Partially covered | API-V12-H-012 |


### 11.8.4.4 FSD 25 candidate operations outside the historical registry

#### 11.8.4.4.1 V8 convention and new operations (26)

| Method | V12 path | Blueprint operation(s) | Relation | Before | Enhancement |
|---|---|---|---|---|---|
| GET | `/api/v1/ai/models` | API-140; API-ADV-X1-12 | Partial | Partially covered | API-V12-H-049 |
| POST | `/api/v1/ai/models/{id}/promotion-requests` | API-141 | Partial | Partially covered | API-V12-H-050 |
| GET | `/api/v1/ai/prompts` | API-142 | Partial | Partially covered | API-V12-H-051 |
| GET | `/api/v1/ai/eval-suites` | API-ENH-D-002; API-147 | Partial | Partially covered | API-V12-H-052 |
| POST | `/api/v1/ai/eval-suites/{id}/runs` | API-138 | Alias | Covered | — |
| GET | `/api/v1/ai/eval-runs/{id}` | API-148 | Alias | Covered | — |
| GET | `/api/v1/ai/red-team/results` | API-ADV-X1-38 | Partial | Partially covered | API-V12-H-053 |
| POST | `/api/v1/ai/content-screen` | — | New | Not covered | API-V12-H-054 |
| GET | `/api/v1/ai/usage` | API-135; API-136 | Partial | Partially covered | API-V12-H-055 |
| PUT | `/api/v1/ai/budgets/{id}` | API-137; API-146 | Alias | Covered | — |
| POST | `/api/v1/ai/kill-switch` | API-451; API-144 | Partial | Partially covered | API-V12-H-056 |
| GET | `/api/v1/compliance/packs` | API-077 | Alias | Covered | — |
| GET | `/api/v1/compliance/packs/{id}/rules` | API-077 | Partial | Partially covered | API-V12-H-057 |
| POST | `/api/v1/compliance/preflight` | API-068 | Alias | Covered | — |
| GET | `/api/v1/consents` | API-076 | Partial | Partially covered | API-V12-H-058 |
| POST | `/api/v1/consents` | API-066 | Exact | Covered | — |
| POST | `/api/v1/consents/{id}/withdraw` | API-067; API-082 | Partial | Partially covered | API-V12-H-059 |
| GET | `/api/v1/suppressions` | API-074 | Alias | Covered | — |
| POST | `/api/v1/public/data-rights-requests` | API-069 | Alias | Covered | — |
| GET | `/api/v1/dsar` | API-084 | Alias | Covered | — |
| POST | `/api/v1/dsar/{id}/verify` | API-085 | Alias | Covered | — |
| POST | `/api/v1/dsar/{id}/complete` | API-086 | Alias | Covered | — |
| GET | `/api/v1/incidents` | API-070; API-092 | Alias | Covered | — |
| POST | `/api/v1/incidents` | — | New | Not covered | API-V12-H-060 |
| POST | `/api/v1/incidents/{id}/notifications` | — | New | Not covered | API-V12-H-061 |
| POST | `/api/v1/public/cookie-consent` | — | New | Not covered | API-V12-H-062 |


#### 11.8.4.4.2 MT, OPT, run-gateway and V4 candidates (32)

| V12 candidate | Method | Path | Result / contract | Blueprint operation(s) | Relation | Before | Enhancement |
|---|---|---|---|---|---|---|---|
| MT-API-01 | POST | `/api/v1/tenants/applications` | Validated SM-APPLICATION-6 envelope; 202 pending; no entitlement | API-503; API-506 | Alias | Covered | — |
| MT-API-02 | POST | `/api/v1/tenants/{id}/companies` | Authorized tenant admin; org FK, company version; 201 pending | API-030 | Alias | Covered | — |
| MT-API-03 | GET | `/api/v1/companies/{id}/configuration` | Versioned scoped graph; no CRM payload | API-038; API-002 | Alias | Covered | — |
| MT-API-04 | POST | `/api/v1/companies/{id}/configuration/drafts` | Draft ID and diff; 409 stale | API-039; API-040 | Alias | Covered | — |
| MT-API-05 | POST | `/api/v1/configuration/{id}/review` | Independent reviewer; approved version or reject | API-541; API-539 | Approval | Covered | — |
| MT-API-06 | POST | `/api/v1/configuration/{id}/rollback-draft` | New draft version; re-review; no automatic restore | API-043 | Partial | Partially covered | (semantic amendment of API-043, §11.8.5.3) |
| MT-API-07 | GET | `/api/v1/context/options` | Only permitted descendants; no stale selection | API-014 | Alias | Covered | — |
| MT-API-08 | POST | `/api/v1/workflow-runs` | BusinessContext DTO; run ID/hold reason; no duplicate effect | API-456; API-449 | Partial | Partially covered | API-V12-H-068 |
| MT-API-09 | GET | `/api/v1/metrics/business` | Native and converted totals with rate version and missing rates | API-537; API-388 | Partial | Partially covered | API-V12-H-064 |
| MT-API-10 | POST | `/api/v1/portfolio/grants` | Grant/revoke aggregate scope; independent clients excluded | API-021 | Partial | Partially covered | API-V12-H-063 |
| OPT-API-01 | POST | `/api/v1/optimization/preflight` | Plan/hold, gate reasons, cost estimate; no external effect | API-449; API-455 | Partial | Partially covered | API-V12-H-068 (dry_run) |
| OPT-API-02 | GET | `/api/v1/optimization/cost-summary` | Meter categories, allocated/unallocated cost, accepted denominator | API-136 | Partial | Partially covered | API-V12-H-065 |
| OPT-API-03 | GET | `/api/v1/optimization/health` | SLO/SLI, incident status, freshness | API-119 | Alias | Covered | — |
| OPT-API-04 | POST | `/api/v1/optimization/feedback` | Case revision and state; dedupe by idempotency key | API-149; API-418 | Alias | Covered | — |
| OPT-API-05 | GET | `/api/v1/optimization/customer-value` | Accepted output, usage, value assumption, renewal state | API-513; API-514 | Partial | Partially covered | API-V12-H-066 |
| OPT-API-06 | POST | `/api/v1/private/application-drafts` | Private draft ID/revision; authenticated, replay protected | API-504; API-ENH-D-019 | Alias | Covered | — |
| OPT-API-07 | POST | `/api/v1/optimization/model-evaluations` | Evaluation reference, quality/cost/latency, pending promotion | API-138; API-148 | Alias | Covered | — |
| OPT-API-08 | GET | `/api/v1/operator/conversion-metrics` | Funnel counts, attribution quality, acquisition cost; aggregate only | API-537 | Partial | Partially covered | API-V12-H-067 |
| API-V2-RUN | POST | `/api/v2/workflow-runs` | {service_id,workflow_id,version,input,mode,idempotency_key} → 202 {run_id,state} | API-456 | New | Not covered | API-V12-H-068 |
| API-V2-RESULT | GET | `/api/v2/workflow-runs/{id}` | {state,step_states,result_ref,error,usage} | API-467 | Alias | Partially covered | API-V12-H-069 |
| API-V2-APPROVAL | POST | `/api/v2/workflow-runs/{id}/approvals` | {action_digest,decision,expiry,expected_version} → approval_ref | API-541; API-539 | Approval | Partially covered | API-V12-H-070 |
| API-V2-CANCEL | POST | `/api/v2/workflow-runs/{id}/cancel` | {expected_version,reason} → state; reconcile effects | API-471 | Alias | Partially covered | API-V12-H-071 |
| API-V2-CATALOG | GET | `/api/v2/public/services` | Released neutral SKU projection; public read only | API-501 | Alias | Covered | (route alias RA-V12-H-01) |
| API-V2-INTAKE | POST | `/api/v2/public/enquiries` | {contact,selected_skus,consent,requirements} → opaque receipt | API-212; API-229 | Alias | Covered | (route alias RA-V12-H-02) |
| API-V2-WEBHOOK | POST | `/api/v2/connectors/{kind}/events` | Provider signed payload → accepted event receipt | API-483 | Partial | Partially covered | API-V12-H-073 |
| V4-API-01 | POST | `/api/v1/commercial/applications` | Application DTO + revision + digest; 201 or 409/422 | API-503 | Alias | Covered | — |
| V4-API-02 | PUT | `/api/v1/commercial/applications/{id}` | Compare expected revision; reject stale or provisioned change | API-504 | Alias | Covered | — |
| V4-API-03 | GET | `/api/v1/commercial/applications/{id}` | Minimal authorized configuration | API-507; API-ENH-D-019 | Alias | Covered | — |
| V4-API-04 | POST | `/api/v1/commercial/workflow-runs` | Run ID, state, reservation, correlation | API-456 | Partial | Partially covered | API-V12-H-068 |
| V4-API-05 | POST | `/api/v1/commercial/workflow-runs/{id}/decisions` | Approval/hold result; 403/409 on denied/stale | API-541; API-539 | Approval | Covered | API-V12-H-070 (v2 spelling) |
| V4-API-06 | GET | `/api/v1/commercial/workflow-runs/{id}/steps` | Step status list, no provider secrets | API-467 | Alias | Partially covered | API-V12-H-072 |
| V4-API-07 | PATCH | `/api/v1/commercial/domain-records/{id}` | New version; reset review; 409 stale | Per-entity PATCH operations (e.g. API-480, API-485, API-ENH-D-001) | Split | Covered | — |


### 11.8.4.5 Historical registry and engineering archive

| Relation (Part 3.5a) | Operations |
|---|---|
| alias | 130 |
| approval | 8 |
| exact | 106 |
| none | 6 |
| partial | 15 |
| split | 37 |

| Part 3.5a status (before Part 3.5b enhancements) | Operations | Status for V12 (after Part 3.5b) |
|---|---|---|
| Covered | 281 | Covered |
| Partially covered | 15 | Covered |
| Not covered | 6 | Covered |


| File | Parsed content | Operations outside reconciled set | Disposition |
|---|---|---|---|
| src/engineering/api_catalog.json | 302 operations (A–Y source columns incl. licence, quota, allocation) | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/api_contract_review.csv | 302 rows; contract_status: Review required — source payload is descriptive 38; Proposed cursor/page-size parameters; response DTO still blocked 82; Proposed explicit DTO — approval required 164; Adapter contract review — provider-specific; no browser endpoint 17; Proposed public response allowlist — approval required 1 | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/api_field_proposals.csv | 1370 field rows for 266 operations (body 633, response 464, query 164, path 109); all approval Pending | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/closure/api_candidate_contracts.csv/.json | 38 decision rows (25 candidate DTOs, 8 provider bindings, 5 identity reuse) = SRC07-DEC-001…038 | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/closure/openapi_closure_candidate.json/.yaml | 285 operations on 255 paths; no component schemas | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/starter/openapi_catalog_draft.json/.yaml | 285 operations; identical operation set to the closure candidate | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/starter/api_payload_review.csv | 285 rows; source_typed No for all; reviews Pending | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/ui_upgrade/candidate_openapi.json | 19 operations = SM-UX-API-01…19 | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |


### 11.8.4.6 Plugin register (FSD 28 V9: VND-01…97)

#### 11.8.4.6.1 Decision counts

| V12 decision | V12 count (stated) | Parsed VND rows | Blueprint rows with the same doc-21 decision (of 538) |
|---|---|---|---|
| Replace/defer paid wrapper | 73 | 73 | 73 |
| Replace core; conditional licensed data only | 8 | 8 | 8 |
| Replace workflow; external service conditional | 7 | 7 | 7 |
| Retain open-source candidate if justified | 3 | 3 | 3 |
| Self-host or replace after licence review | 2 | 2 | 2 |
| Replace first; conditional search fallback | 2 | 2 | 2 |
| Defer unless commercial evidence need approved | 2 | 2 | 2 |


The V12 register is the 97-row subset of the 538-candidate register whose document-21 decision is not "Defer; no runtime need established" (441 rows). Every one of the 97 names and decisions matches a row of `F_integration_candidates.csv`; no decision differs.

#### 11.8.4.6.2 Row-by-row reconciliation (97)

| VND | Candidate | V12 decision (= blueprint doc 21 decision) | Capability | Blueprint IC row | Blueprint replacement decision | Adapter / module | Activation default | Addition |
|---|---|---|---|---|---|---|---|---|
| VND-01 | Firecrawl | Self-host or replace after licence review | Website extraction | IC-001 | Retain OSS / self-host | AD-07 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-02 | Apollo.io | Replace core; conditional licensed data only | Professional contact discovery | IC-002 | Conditional external service (B08/B18) | AD-19 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | contact-data activation conditions (CJ-R15, DPA, CJ-GL-01, DEC-V9-04) |
| VND-03 | customer-sales-automation | Replace/defer paid wrapper | CRM / relationship pipeline | IC-003 | Replace (native) | M21–M23 native CRM | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-04 | Hunter | Replace core; conditional licensed data only | Professional contact discovery | IC-004 | Conditional external service (B08/B18) | AD-19 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | contact-data activation conditions (CJ-R15, DPA, CJ-GL-01, DEC-V9-04) |
| VND-05 | Sales | Replace/defer paid wrapper | CRM / relationship pipeline | IC-005 | Replace (native) | M21–M23 native CRM | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-06 | Content Studio | Replace/defer paid wrapper | Marketing content and localization | IC-006 | Replace (native) | M34 content studio | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-07 | content-marketing | Replace/defer paid wrapper | Marketing content and localization | IC-007 | Replace (native) | M34 content studio | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-08 | Marketing | Replace/defer paid wrapper | Marketing content and localization | IC-008 | Replace (native) | M34 content studio | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-09 | Postiz | Self-host or replace after licence review | Social listening and publishing | IC-009 | Conditional external service (B16) | AD-08 SocialPort | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-10 | seo-analysis-monitoring | Replace/defer paid wrapper | SEO and AI search visibility | IC-010 | Replace (native) + official API | AD-17 Search Console | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-11 | seo-content-creation | Replace/defer paid wrapper | Marketing content and localization | IC-011 | Replace (native) | M34 content studio | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-12 | seo-technical-optimization | Replace/defer paid wrapper | SEO and AI search visibility | IC-012 | Replace (native) + official API | AD-17 Search Console | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-13 | social-publishing | Replace/defer paid wrapper | Social listening and publishing | IC-013 | Conditional external service (B16) | AD-08 SocialPort | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-14 | Clay | Replace core; conditional licensed data only | Professional contact discovery | IC-014 | Conditional external service (B08/B18) | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | contact-data activation conditions (CJ-R15, DPA, CJ-GL-01, DEC-V9-04) |
| VND-15 | Common Room | Replace/defer paid wrapper | Marketing campaigns and attribution | IC-015 | Replace (native) | M39 campaigns; AU-040 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-16 | Crossbeam Skills | Replace/defer paid wrapper | CRM / relationship pipeline | IC-016 | Replace (native) | M21–M23 native CRM | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-17 | Endgame | Replace/defer paid wrapper | CRM / relationship pipeline | IC-017 | Replace (native) | M21–M23 native CRM | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-18 | Leadfeeder | Replace/defer paid wrapper | Marketing campaigns and attribution | IC-018 | Replace (native) | M39 campaigns; AU-040 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-19 | Adspirer | Replace/defer paid wrapper | Advertising and paid acquisition | IC-019 | Conditional external service (B12/B16) | AD-09 AdsPort | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-20 | Socialinsider | Replace/defer paid wrapper | Social listening and publishing | IC-020 | Conditional external service (B16) | AD-08 SocialPort | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-21 | Writesonic | Replace/defer paid wrapper | Marketing content and localization | IC-021 | Replace (native) | M34 content studio | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-22 | EULER for Partner Managers | Replace/defer paid wrapper | CRM / relationship pipeline | IC-022 | Replace (native) | M21–M23 native CRM | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-23 | Vibe Prospecting | Replace core; conditional licensed data only | Professional contact discovery | IC-023 | Conditional external service (B08/B18) | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | contact-data activation conditions (CJ-R15, DPA, CJ-GL-01, DEC-V9-04) |
| VND-24 | AppFollow AI Toolkit | Replace/defer paid wrapper | SEO and AI search visibility | IC-024 | Replace (native) + official API | AD-17 Search Console | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-25 | AppTweak API | Replace/defer paid wrapper | SEO and AI search visibility | IC-025 | Replace (native) + official API | AD-17 Search Console | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-26 | Pendo Orchestrate | Replace/defer paid wrapper | Marketing campaigns and attribution | IC-026 | Replace (native) | M39 campaigns; AU-040 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-27 | Realize | Replace workflow; external service conditional | Advertising and paid acquisition | IC-027 | Conditional external service (B12/B16) | AD-09 AdsPort | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-28 | Spotify Ads API | Replace workflow; external service conditional | Advertising and paid acquisition | IC-028 | Conditional external service (B12/B16) | AD-09 AdsPort | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-29 | vidIQ | Replace/defer paid wrapper | SEO and AI search visibility | IC-029 | Replace (native) + official API | AD-17 Search Console | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-30 | HubSpot Sales | Replace/defer paid wrapper | CRM / relationship pipeline | IC-030 | Replace (native) | M21–M23 native CRM | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-31 | Lusha | Replace core; conditional licensed data only | Professional contact discovery | IC-031 | Conditional external service (B08/B18) | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | contact-data activation conditions (CJ-R15, DPA, CJ-GL-01, DEC-V9-04) |
| VND-32 | monday CRM | Replace/defer paid wrapper | CRM / relationship pipeline | IC-032 | Replace (native) | M21–M23 native CRM | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-33 | RocketReach | Replace core; conditional licensed data only | Professional contact discovery | IC-033 | Conditional external service (B08/B18) | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | contact-data activation conditions (CJ-R15, DPA, CJ-GL-01, DEC-V9-04) |
| VND-34 | Sales Cloud | Replace/defer paid wrapper | CRM / relationship pipeline | IC-034 | Replace (native) | M21–M23 native CRM | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-35 | ZoomInfo | Replace core; conditional licensed data only | Professional contact discovery | IC-035 | Conditional external service (B08/B18) | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | contact-data activation conditions (CJ-R15, DPA, CJ-GL-01, DEC-V9-04) |
| VND-36 | ActiveCampaign | Replace/defer paid wrapper | Marketing campaigns and attribution | IC-036 | Replace (native) | M39 campaigns; AU-040 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-37 | Apify | Replace/defer paid wrapper | Website extraction | IC-037 | Retain OSS / self-host | AD-07 Firecrawl self-hosted (ExtractionPort) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-38 | Botify | Replace/defer paid wrapper | SEO and AI search visibility | IC-038 | Replace (native) + official API | AD-17 Search Console | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-39 | Bright Data | Replace/defer paid wrapper | Website extraction | IC-039 | Retain OSS / self-host | AD-07 Firecrawl self-hosted (ExtractionPort) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-40 | Customer.io | Replace/defer paid wrapper | Marketing campaigns and attribution | IC-040 | Replace (native) | M39 campaigns; AU-040 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-41 | Nimble | Replace/defer paid wrapper | CRM / relationship pipeline | IC-041 | Replace (native) | M21–M23 native CRM | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-42 | SearchAtlas Toolkit | Replace/defer paid wrapper | SEO and AI search visibility | IC-042 | Replace (native) + official API | AD-17 Search Console | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-43 | SearchFit SEO | Replace/defer paid wrapper | SEO and AI search visibility | IC-043 | Replace (native) + official API | AD-17 Search Console | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-44 | Supermetrics | Replace/defer paid wrapper | Marketing campaigns and attribution | IC-044 | Replace (native) | M39 campaigns; AU-040 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-45 | Unbounce Landing Page Builder | Replace/defer paid wrapper | Website and landing page builder | IC-045 | Replace (native) | B-WEB publication service (A107, A108) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-46 | Windsor.ai | Replace/defer paid wrapper | Marketing campaigns and attribution | IC-046 | Replace (native) | M39 campaigns; AU-040 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-47 | Zyte Web Data | Replace/defer paid wrapper | Website extraction | IC-047 | Retain OSS / self-host | AD-07 Firecrawl self-hosted (ExtractionPort) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-48 | Carta crm | Replace/defer paid wrapper | CRM / relationship pipeline | IC-048 | Replace (native) | M21–M23 native CRM | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-49 | GovTribe | Replace/defer paid wrapper | Project / tender discovery and bid preparation | IC-049 | Replace (native); no auto-submission | WF-08 bids; AU-034 (DEC-053) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-50 | Wealthbox | Replace/defer paid wrapper | CRM / relationship pipeline | IC-050 | Replace (native) | M21–M23 native CRM | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-51 | B12 | Replace/defer paid wrapper | Website and landing page builder | IC-051 | Replace (native) | B-WEB publication service (A107, A108) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-52 | Build with WordPress | Replace/defer paid wrapper | Website and landing page builder | IC-052 | Replace (native) | B-WEB publication service (A107, A108) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-53 | Replo | Replace/defer paid wrapper | Website and landing page builder | IC-053 | Replace (native) | B-WEB publication service (A107, A108) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-54 | Tavily | Replace first; conditional search fallback | Public market / investor search | IC-054 | Replace core; investor use excluded (DEC-002 scope) | AD-05 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | commercial market research only, investor use excluded (DEC-002, DEC-656) |
| VND-55 | Playwright | Retain open-source candidate if justified | Website extraction | IC-055 | Retain OSS / self-host | Part 6 tooling | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-56 | AWS Core | Replace/defer paid wrapper | Cloud infrastructure and storage | IC-056 | Retain existing (B01) | AWS ap-south-1 (DEC-040) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-57 | Claude Code Setup | Replace/defer paid wrapper | Developer tools, QA and project coordination | IC-057 | Defer (developer-only) | Delivery tooling (Part 7.3 §7.5.2) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-58 | CLAUDE.md Management | Replace/defer paid wrapper | Developer tools, QA and project coordination | IC-058 | Defer (developer-only) | Delivery tooling (Part 7.3 §7.5.2) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-59 | Postman | Replace/defer paid wrapper | Developer tools, QA and project coordination | IC-059 | Defer (developer-only) | Part 3.2 §3.2.5 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-60 | GitHub | Replace/defer paid wrapper | Developer tools, QA and project coordination | IC-060 | Defer (developer-only) | Part 4.3 CI | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-61 | Security Guidance | Replace/defer paid wrapper | Observability, error tracking, metrics and security | IC-061 | Retain OSS / existing | AD-15 Sentry, AD-16 CloudWatch; ADR-078 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-62 | Agent SDK Dev | Replace/defer paid wrapper | LLM / agent framework | IC-062 | Replace (native gateway) | AD-13 Anthropic via ai.gateway (ADR-070) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-63 | DeepEval | Retain open-source candidate if justified | Developer tools, QA and project coordination | IC-063 | Defer (developer-only) | ADR-079 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-64 | Pydantic AI | Retain open-source candidate if justified | LLM / agent framework | IC-064 | Replace (native gateway) | Part 7.3 §7.5.3 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-65 | Resend | Replace workflow; external service conditional | Email automation and inbox | IC-065 | Conditional external service (B05) | AD-01 alt (DEC-025) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-66 | Zoom | Replace workflow; external service conditional | Meeting scheduling and video | IC-066 | Conditional external service (B15) | AD-18 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-67 | Figma | Replace/defer paid wrapper | Developer tools, QA and project coordination | IC-067 | Defer (developer-only) | Delivery tooling (Part 7.3 §7.5.2) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-68 | Langfuse | Replace/defer paid wrapper | Observability, error tracking, metrics and security | IC-068 | Retain OSS / existing | ADR-078 / B22 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-69 | PostHog | Replace/defer paid wrapper | Marketing campaigns and attribution | IC-069 | Replace (native) | M39 campaigns; AU-040 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-70 | Sentry | Replace/defer paid wrapper | Observability, error tracking, metrics and security | IC-070 | Retain OSS / existing | AD-15 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-71 | AWS Serverless | Replace/defer paid wrapper | Cloud infrastructure and storage | IC-074 | Retain existing (B01) | AWS ap-south-1 (DEC-040) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-72 | PandaDoc | Replace workflow; external service conditional | Document generation / secure storage | IC-077 | Replace (native) | AU-036 document assembly; S3 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-73 | Exa | Replace first; conditional search fallback | Public market / investor search | IC-079 | Replace core; investor use excluded (DEC-002 scope) | AD-06 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | commercial market research only, investor use excluded (DEC-002, DEC-656) |
| VND-74 | AWS Agents | Replace/defer paid wrapper | LLM / agent framework | IC-088 | Replace (native gateway) | AD-13 Anthropic via ai.gateway (ADR-070) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-75 | Enterprise Search | Replace/defer paid wrapper | Embeddings, knowledge and enterprise search | IC-111 | Retain OSS | AD-14 EmbeddingPort; pgvector (ADR-077) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-76 | AWS Amplify | Replace/defer paid wrapper | Cloud infrastructure and storage | IC-122 | Retain existing (B01) | AWS ap-south-1 (DEC-040) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-77 | AWS Startup Advisor | Replace/defer paid wrapper | Cloud infrastructure and storage | IC-123 | Retain existing (B01) | AWS ap-south-1 (DEC-040) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-78 | AWS Transform | Replace/defer paid wrapper | Cloud infrastructure and storage | IC-124 | Retain existing (B01) | AWS ap-south-1 (DEC-040) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-79 | Deploy on AWS | Replace/defer paid wrapper | Cloud infrastructure and storage | IC-130 | Retain existing (B01) | AWS ap-south-1 (DEC-040) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-80 | Migration to AWS | Replace/defer paid wrapper | Cloud infrastructure and storage | IC-136 | Retain existing (B01) | AWS ap-south-1 (DEC-040) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-81 | Slack | Replace/defer paid wrapper | Customer support / collaboration | IC-176 | Replace (native) | M63 support; NT notifications | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-82 | AWS Data Analytics | Replace/defer paid wrapper | Analytics, reporting and forecasting | IC-190 | Replace (native) | RP-01…30; AU-040, AU-041 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-83 | Cloud SQL for PostgreSQL | Replace/defer paid wrapper | Embeddings, knowledge and enterprise search | IC-199 | Retain OSS | AD-14 EmbeddingPort; pgvector (ADR-077) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-84 | Databases on AWS | Replace/defer paid wrapper | Embeddings, knowledge and enterprise search | IC-209 | Retain OSS | AD-14 EmbeddingPort; pgvector (ADR-077) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-85 | Apollo GraphQL | Replace core; conditional licensed data only | Professional contact discovery | IC-270 | Conditional external service (B08/B18) | AD-19 Apollo/Hunter (EnrichmentPort, OFF) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | contact-data activation conditions (CJ-R15, DPA, CJ-GL-01, DEC-V9-04) |
| VND-86 | Bio Research | Defer unless commercial evidence need approved | Public market / investor search | IC-332 | Replace core; investor use excluded (DEC-002 scope) | AD-05 Tavily / AD-06 Exa (SearchPort) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | commercial market research only, investor use excluded (DEC-002, DEC-656) |
| VND-87 | LegalZoom | Replace workflow; external service conditional | Electronic signing and identity verification | IC-360 | Conditional external service (B13) | AD-10 ESignPort (manual first, DEC-023) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-88 | Sentry CLI | Replace/defer paid wrapper | Observability, error tracking, metrics and security | IC-392 | Retain OSS / existing | AD-15 Sentry, AD-16 CloudWatch; ADR-078 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-89 | Stripe | Replace workflow; external service conditional | Banking, receipts and billing | IC-405 | Conditional external service (B14) | AD-11 PaymentPort (manual first, DEC-022) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-90 | Dropbox | Replace/defer paid wrapper | Document generation / secure storage | IC-413 | Replace (native) | AU-036 document assembly; S3 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-91 | Meeting Memory by Grain | Replace/defer paid wrapper | Meeting scheduling and video | IC-426 | Conditional external service (B15) | AD-03/AD-04 Calendar; AD-18 Webinar | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-92 | Notion | Replace/defer paid wrapper | Document generation / secure storage | IC-427 | Replace (native) | AU-036 document assembly; S3 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-93 | Linear | Replace/defer paid wrapper | Developer tools, QA and project coordination | IC-439 | Defer (developer-only) | Delivery tooling (Part 7.3 §7.5.2) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-94 | AWS Agents for DevSecOps | Replace/defer paid wrapper | Observability, error tracking, metrics and security | IC-445 | Retain OSS / existing | AD-15 Sentry, AD-16 CloudWatch; ADR-078 | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |
| VND-95 | Equity Research | Defer unless commercial evidence need approved | Public market / investor search | IC-486 | Replace core; investor use excluded (DEC-002 scope) | AD-05 Tavily / AD-06 Exa (SearchPort) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | commercial market research only, investor use excluded (DEC-002, DEC-656) |
| VND-96 | Market Researcher | Replace/defer paid wrapper | Public market / investor search | IC-499 | Replace core; investor use excluded (DEC-002 scope) | AD-05 Tavily / AD-06 Exa (SearchPort) | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | commercial market research only, investor use excluded (DEC-002, DEC-656) |
| VND-97 | Meeting Prep Agent | Replace/defer paid wrapper | Meeting scheduling and video | IC-500 | Conditional external service (B15) | AD-03/AD-04 Calendar; AD-18 Webinar | Disabled; procurement gate PG-01…PG-10 (Part 7.4b §7.4.5.8.2 | — |


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

**Status: Part 11 Batch 11.8a complete. 1176 V12 aspects parsed and reconciled (282 Appendix A and 48 Appendix A2 operations, 302 historical rows, 58 other candidates, 97 VND decisions, 11 connector kinds, 1,370 field proposals in 266 operation groups); 1168 Matched, 7 Pending Founder decision, 1 Not applicable. Enhancements, conflicts, decisions and the quality gate are in Part 11.8b.**
