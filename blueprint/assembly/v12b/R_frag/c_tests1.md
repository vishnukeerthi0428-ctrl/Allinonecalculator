
---

### 11.19.5.15 Test strategy delta (Part 6.1 applied to P4)

| Aspect | Rule for P4 | Source |
|---|---|---|
| Risk areas | Confidentiality across tenants and zones (RA-01), unauthorized external action (RA-03/04), regulatory eligibility (RA-03), recoverability (RA-21), AI routing compliance (RA-13) — all **P0** where the row decides access, residency, money, law or recovery | Part 6.1 §6.1.4 |
| Levels | UT (oracles, SDK verify), IT (PP-05 with real PostgreSQL + RLS + simulators), SYS (PP-01 per zone), E2E (drills, browser SSO), UAT (tenant IdP pilot with an owned startup) | Part 6.1 §6.1.2 |
| Simulators | IdP (Okta, Entra ID, Google, generic SAML/OIDC payload shapes), SCIM client (vendor quirks), CRM (three providers), SMS aggregator (DLT, DND, DLR), CPaaS, webhook receiver, model gateway (registry fixture REG-FIX-3), Vercel API mock for AU-296 | Part 6.1 §6.1.6 |
| Zones | Every SYS suite runs in the IN cell; EU suites run in the EU cell when provisioned and in an EU-configured test cell before (CJ-TC-09 both directions) | DEC-772 |
| Combinatorial design | Parameters and values declared per capability (§11.19.5.16); **3-way** for identity, credentials, connectors (law), residency path, recovery, model routing and benchmarks; **pairwise** for SoD, webhook delivery and DB access; **exhaustive** where ≤ 64 valid combinations (signature verification, registry approval) | V12-B brief |
| Oracle | Each generated row's expected result is computed by the model's oracle function in `R_02_combinatorics.py` from the rules in Part 11.19a/b; disagreements between the system and the oracle are triaged as defects in either | Part 6.1 §6.1.11 |
| Blocking suites | M01, M02, M03, M04, M07 (gate rows), M08, M09, M10, M12 P0 rows; TC-V12-R-001…086 P0 rows; KPI-32 drill | Release 1 gate (GNG-R-01…10) |
| Conformance | SCIM RFC 7644 conformance suite; SAML XSW corpus (12 variants); OIDC conformance profile checks for RP (OpenID Foundation suite, verify availability) | ADR-255/256 |
| Performance | RL-KEY fairness (k6, 2 tenants, one noisy); SCIM bulk 100 ops ≤ 5 s p95; webhook first attempt ≤ 5 s p95; replication lag < 60 s at load profile `m` | Part 6.1 §6.1.3 |
| Accessibility | A203, A002 Roles tab, A168, A204, A008, A011 Registry tab, A042 Benchmarks tab, W47 portal: WCAG 2.2 AA (axe + manual AT pass PP-07) | Part 2.5 |
| Evidence | Each test run exports results per TC ID to the release evidence store; drills write `restore_drill` | Part 6.1 §6.1.12 |

### 11.19.5.16 Combinatorial test design (parameter models, method, counts)

**Generation method.** For each model the script enumerates every combination of the declared values, removes the combinations forbidden by the model's constraints (for example, a generic SAML IdP cannot speak OIDC; sandbox installations cannot have an incomplete gate; Tier 2 rows cannot be chosen for embedding), lists every valid t-tuple (t = 2 or 3) that occurs in at least one valid row, and then repeatedly selects the valid row covering the largest number of still-uncovered t-tuples until all are covered (a deterministic greedy covering-array construction in the AETG family). Spaces with ≤ 64 valid rows are enumerated exhaustively. The oracle then computes each row's expected result. Re-running the script reproduces the same rows and IDs.

{{COMBO_SUMMARY}}

{{MODELS}}

### 11.19.5.17 Test scenarios

| TS ID | Scenario | Linked stories / FR | Risk area · Priority | TCs |
|---|---|---|---|---|
| TS-V12-R-21 | SSO configuration, enforcement, break-glass, MFA and session policy behave as specified and fail closed | US-01-ZR01, ZR02 · FR-V12-R-001…010 | RA-01 · **P0** | TC-V12-R-001…010 |
| TS-V12-R-22 | SCIM provisioning, mapping, de-provisioning and SLA; custom roles, SoD, SIEM, audit export, JIT, recertification | US-01-ZR03…05 · FR-V12-R-011…026 | RA-01 · **P0** | TC-V12-R-011…020 |
| TS-V12-R-23 | Developer credentials, webhooks, SDKs, portal and sandbox | US-20-ZR06…10 · FR-V12-R-031…055 | RA-01, RA-04 · **P0** | TC-V12-R-021…036 |
| TS-V12-R-24 | Connector gate, CRM sync and ownership, SMS-DLT, voice transport | US-18-ZR11, US-07-ZR12/13, US-23-ZR14, US-22-ZR15 · FR-V12-R-056…080 | RA-03, RA-04 · **P0** | TC-V12-R-037…050 |
| TS-V12-R-25 | Vercel personal-data path controls | US-21-ZR16/17 · FR-V12-R-081…095 | RA-01 · **P0** | TC-V12-R-051…058 |
| TS-V12-R-26 | Recovery paths, monitor and drills | US-21-ZR18/19 · FR-V12-R-096…110 | RA-21 · **P0** | TC-V12-R-059…066 |
| TS-V12-R-27 | Model registry approval, routing, fallback, kill switch, re-certification | US-04-ZR20…23 · FR-V12-R-111…130 | RA-13 · **P0** | TC-V12-R-067…074 |
| TS-V12-R-28 | Benchmarks and database access model | US-17-ZR24/25, US-01-ZR26/27 · FR-V12-R-131…155 | RA-01 · **P0** | TC-V12-R-075…086 |
| TS-V12-R-01…13 | Generated combinatorial suites M01…M13 (one TS per model) | per model (§11.19.5.16) | per model · **P0** | TC-V12-R-101…1172 |

### 11.19.5.18 Test cases (full form)

#### Group TC-V12-R-A: Equivalence partitioning and error guessing – enterprise identity (US-01-ZR01…05)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-001 | Create, test and activate an Okta SAML connection | TS-V12-R-21 · US-01-ZR01 AC-01ZR01-01 · FR-V12-R-001, 004, 029; ENT-IDN-01 | Pre: PP-01 IN; R12 `meera` with WebAuthn age 1 h. Data: okta-sim metadata with 2 signing certificates | 1. POST connection. 2. POST test-login; complete with valid assertion. 3. POST activate. 4. SELECT from `ge.identity_provider` view | 1: 201 `draft`. 2: 202 then event `tested` ok. 3: 200 `active`, `last_test_ok_at` set. 4: one row with protocol `SAML 2.0` | P0 | T01 | UC | Y | SYS |
| TC-V12-R-002 | Reject http metadata and weak algorithms; bind issuer to connection | TS-V12-R-21 · AC-01ZR01-02 · FR-V12-R-002, 003 | Pre: PP-01. Data: `http://…/metadata`; metadata signed RSA-SHA1; assertion from issuer of another tenant | Submit each | 422 `METADATA_URL_NOT_HTTPS`; 422 `UNSUPPORTED_ALG`; sign-in 401 `SSO_ISSUER_MISMATCH`; NSE | P0 | T07 | EP | Y | SYS |
| TC-V12-R-003 | XML signature wrapping corpus is rejected | TS-V12-R-21 · FR-V12-R-003; ADR-255 | Pre: PP-05 broker adapter. Data: XSW-1…XSW-8, comment-in-NameID, duplicate assertion, unsigned assertion in signed response (12 variants) | Post each to the ACS | 12/12 rejected with `SSO_SIGNATURE_INVALID` or `SSO_SCHEMA_INVALID`; SEV3 events; no session | P0 | T07 | EG | Y | IT |
| TC-V12-R-004 | Activation needs a successful test; AU-290 warns before certificate expiry | TS-V12-R-21 · AC-01ZR01-04 · FR-V12-R-004, 027 | Pre: PP-01. Data: certificate `not_after` = CLK-0 + 14 days | 1. Activate untested. 2. Run AU-290 | 1: 409 `TEST_LOGIN_REQUIRED`. 2: `identity.certificate.expiring` (14-day threshold) and R12 notification | P1 | T01 | EP | Y | SYS |
| TC-V12-R-005 | Zone resolution before personal data | TS-V12-R-21 · FR-V12-R-005; DEC-895 | Pre: IN and EU test cells. Data: email `anna@nordlicht.example.de` (EU tenant) entered on `admin.in` | Discover; follow redirect | Redirect to `admin.eu`; IN cell logs contain only the domain hash; no IN session row | P0 | T15 | EP | Y | SYS |
| TC-V12-R-006 | Domain verification and loss after two misses | TS-V12-R-21 · AC-01ZR02-01/03 · FR-V12-R-006 | Pre: DNS simulator. Data: TXT present, then absent on 2 daily checks | Verify; run AU-290 twice | `verified`; after miss 1 still `verified` (misses=1); after miss 2 `verification_lost`, High notice; enforced sign-in still works | P0 | T01 | ST | Y | SYS |
| TC-V12-R-007 | Enforcement guard in API and trigger | TS-V12-R-21 · AC-01ZR02-02 · FR-V12-R-007 | Pre: PP-05. Data: verified domain, no break-glass | 1. POST enforce. 2. `UPDATE ge.idp_connection SET enforced = true` as app_rw | 1: 409 `SSO_ENFORCEMENT_REQUIRES_BREAKGLASS`. 2: exception same code; NSE | P0 | T07 | DT | Y | IT |
| TC-V12-R-008 | Break-glass requires hardware key; use raises SEV3 | TS-V12-R-21 · AC-01ZR02-04 · FR-V12-R-008 | Pre: PP-01. Data: account without hardware key; then with | 1. Create without key. 2. Create with key. 3. Sign in | 1: 422 `HARDWARE_KEY_REQUIRED`. 2: 201. 3: SEV3, notifications to all R12/R10 ≤ 5 min | P0 | T07 | EP | Y | SYS |
| TC-V12-R-009 | Step-up for privileged role when IdP amr lacks phishing-resistant factor | TS-V12-R-21 · FR-V12-R-009; DEC-077 | Pre: PP-01. Data: R02 sign-in with `amr=["pwd","otp"]` | Sign in; call privileged API; complete WebAuthn; call again | First call 403 `STEP_UP_REQUIRED`; after WebAuthn 200; session `amr` updated | P0 | T07 | DT | Y | SYS |
| TC-V12-R-010 | Session policy boundaries and revocation ≤ 60 s | TS-V12-R-21 · AC-01ZR02-05 · FR-V12-R-010 | Pre: PP-01. Data: values 0/1/24/25 h and 4/5/120/121 min | PATCH each; revoke a session; call API at +59 s and +61 s | Out-of-range 422; in-range 200 (privileged capped 12 h/30 min); revoked call 401 by +60 s | P1 | T07 | BVA | Y | SYS |
| TC-V12-R-011 | SCIM conformance suite | TS-V12-R-22 · FR-V12-R-011 | Pre: PP-01 SCIM base IN. Data: RFC 7644 conformance suite run against tenant T1 | Run suite | All mandatory checks pass (Users, Groups, filter, PATCH, ETag, errors) | P0 | T10 | EP | Y | SYS |
| TC-V12-R-012 | Unmapped group grants nothing; mapping needs second approver | TS-V12-R-22 · AC-01ZR03-03 · FR-V12-R-013 | Pre: PP-01. Data: group `All-Staff` | Add user; request mapping; approve by requester; approve by another R12 | No role; 403 `SAME_APPROVER`; after approval role granted ≤ 60 s | P0 | T07 | DT | Y | SYS |
| TC-V12-R-013 | SCIM token shown once, hashed, zone-bound | TS-V12-R-22 · FR-V12-R-012 | Pre: PP-01. Data: lifetime 398 days; then 365 | Create; read DB; use on EU host | 422 for 398; 201 token once; DB has hash only; EU host 401 | P0 | T07 | BVA | Y | SYS |
| TC-V12-R-014 | RL-SCIM and Bulk limits | TS-V12-R-22 · FR-V12-R-016 | Pre: PP-01. Data: 61 requests in 60 s; Bulk with 101 ops | Send | 61st → 429 `tooMany`; Bulk 101 → 413/`tooMany` with no partial apply | P1 | T03 | BVA | Y | SYS |
| TC-V12-R-015 | De-provisioning revokes sessions, keys, clients; re-queues approvals | TS-V12-R-22 · AC-01ZR03-02 · FR-V12-R-014 | Pre: PP-05. Data: user with 2 sessions, 1 key, 1 OAuth client, 2 pending approvals | PATCH active=false; observe for 60 s | All revoked ≤ 60 s; approvals assigned to R12 queue; scheduled jobs re-assigned; `identity.revocation.completed` with `product_ms` ≤ 60,000 | P0 | T07 | UC | Y | IT |
| TC-V12-R-016 | End-to-end SLA breach detection | TS-V12-R-22 · AC-01ZR03-05 · FR-V12-R-015 | Pre: PP-05. Data: `idp_changed_at` 18 min before receipt | Run AU-291 | `end_to_end_s` = 1,080; SEV2; RB-ID-04 linked | P0 | T21 | EP | Y | IT |
| TC-V12-R-017 | Permission catalogue generated and flagged | TS-V12-R-22 · FR-V12-R-017 | Pre: CI. Data: RBAC YAML v12 | Generate; diff | Every permission `Resource:action`, flags set; catalogue_version increments; unknown permission in role → 422 `UNKNOWN_PERMISSION` | P1 | T01 | EP | Y | UT |
| TC-V12-R-018 | Consequential permission in custom role needs R10 co-approval | TS-V12-R-22 · FR-V12-R-018, 022 | Pre: PP-01. Data: role with `Mandates:request` | Create as R12; approve as R10 | Pending until R10 approves; then active | P0 | T07 | DT | Y | SYS |
| TC-V12-R-019 | SoD matrix of record, SIEM sink and audit export | TS-V12-R-22 · FR-V12-R-020, 024, 025 | Pre: PP-05. Data: 12 pairs; sink https test collector; 1,000 audit rows, one edited | Query matrix; send test; export; verify | 12 pairs present; test delivered; export count = filter count; verify reports break at edited row | P0 | T19 | EP | Y | IT |
| TC-V12-R-020 | Role applies at API, worker and UI; JIT ticket; recertification suspension | TS-V12-R-22 · FR-V12-R-021, 023, 026 | Pre: PP-01/06. Data: custom role without `Leads:write` | Try write via API, via worker task, via UI; JIT grant without ticket; let recert lapse | 403 / task denied / control hidden; JIT 422 `TICKET_REQUIRED`; privileged permissions suspended day 14 | P0 | T15 | EP | Y | SYS |

#### Group TC-V12-R-B: Developer platform (US-20-ZR06…10)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-021 | Key created once, stored as hash with zone | TS-V12-R-23 · AC-20ZR06-01 · FR-V12-R-031 | Pre: PP-01 IN | Create; GET key list; SELECT row | Plaintext only in create response, `no-store`; list shows prefix+last4; row has hash, `zone=IN` | P0 | T07 | EP | Y | SYS |
| TC-V12-R-022 | Rotation overlap, revocation ≤ 60 s and leak response | TS-V12-R-23 · FR-V12-R-033, 052 | Pre: PP-01. Data: overlap 24 h; leak report webhook | Rotate; call with old at +23 h and +25 h; post leak report | Old works at +23 h, 401 at +25 h; leaked key 401 ≤ 60 s; R12 notified | P0 | T07 | BVA | Y | SYS |
| TC-V12-R-023 | No consequential scope possible (API and DB) | TS-V12-R-23 · AC-20ZR06-02 · FR-V12-R-034 | Pre: PP-05. Data: scopes `send`, `pay`, `bids:submit` | API create; direct INSERT | 422 `SCOPE_NOT_GRANTABLE`; check violation `api_key_no_consequential_scope_ck` | P0 | T07 | EP | Y | IT |
| TC-V12-R-024 | Client credentials with private_key_jwt | TS-V12-R-23 · AC-20ZR07-01 · FR-V12-R-035 | Pre: PP-01. Data: ES256 key pair, JWKS URL | Token request; API call | 200 token, 15 min, aud `api.in`; API 200 | P0 | T01 | UC | Y | SYS |
| TC-V12-R-025 | Assertion replay and exp window | TS-V12-R-23 · AC-20ZR07-02/04 · FR-V12-R-036 | Pre: PP-01. Data: same jti twice; exp +300 s | Post | 400 `invalid_client` both; no token | P0 | T07 | EG | Y | SYS |
| TC-V12-R-026 | Token revocation and client suspension | TS-V12-R-23 · AC-20ZR07-05 · FR-V12-R-037 | Pre: PP-01 | Revoke; call; suspend client; request token | 401; 400 `invalid_client` | P1 | T07 | EP | Y | SYS |
| TC-V12-R-027 | Signature format and dual signatures during rotation | TS-V12-R-23 · FR-V12-R-041 | Pre: PP-05 receiver simulator | Rotate secret; deliver event | Header has two `v1` values for 24 h; one after | P0 | T07 | EP | Y | IT |
| TC-V12-R-028 | Retry schedule and exhaustion | TS-V12-R-23 · AC-20ZR08-03 · FR-V12-R-042 | Pre: PP-05 virtual clock. Data: receiver 503 always | Deliver | Attempts at T, +5 m, +35 m, +2 h 35 m, +8 h 35 m, +23 h 35 m (±10%); `exhausted` | P1 | T18 | BVA | Y | IT |
| TC-V12-R-029 | Delivery log and replay window | TS-V12-R-23 · AC-20ZR08-04 · FR-V12-R-044 | Pre: PP-01. Data: deliveries 29 and 31 days old | Replay each | 202 for 29 days; 409 `OUTSIDE_REPLAY_WINDOW` for 31 | P2 | T01 | BVA | Y | SYS |
| TC-V12-R-030 | SSRF guard at registration and delivery (DNS rebinding) | TS-V12-R-23 · AC-20ZR08-02 · FR-V12-R-045 | Pre: PP-05 DNS simulator. Data: `169.254.169.254`, `10.0.0.5`, `[::1]`, host that resolves public then private | Register; deliver after re-resolution | 422 at registration; delivery refused when resolution turns private; no redirect followed | P0 | T07 | EG | Y | IT |
| TC-V12-R-031 | Payloads carry references only | TS-V12-R-23 · FR-V12-R-046, 047 | Pre: PP-05. Data: lead with phone and email | Emit `lead.created`; `consent.withdrawn` | Payload has IDs and changed field names only; withdrawn uses subject hash | P0 | T19 | EP | Y | IT |
| TC-V12-R-032 | Portal, changelog and deprecation headers | TS-V12-R-23 · AC-20ZR09-04 · FR-V12-R-040, 051 | Pre: portal build. Data: deprecated op with sunset | Build; call op | Portal lists region base URLs; headers `Deprecation`, `Sunset`, `Link` present | P1 | T01 | EP | Y | SYS |
| TC-V12-R-033 | SDK contract suites in three languages | TS-V12-R-23 · AC-20ZR10-01 · FR-V12-R-048…050 | Pre: sandbox IN and EU | Run suite per language and zone | 6/6 green; artefacts verified signatures | P1 | T10 | PW | Y | CT |
| TC-V12-R-034 | Sandbox synthetic-only and simulator-only | TS-V12-R-23 · AC-20ZR09-02 · FR-V12-R-053 | Pre: sandbox tenant. Data: CSV with a real-format number not in generator pattern; request for production adapter | Import; dispatch | Import 422 `SANDBOX_SYNTHETIC_ONLY`; adapter registry returns simulator only | P0 | T17 | EG | Y | SYS |
| TC-V12-R-035 | Promotion review with requester ≠ approver | TS-V12-R-23 · AC-20ZR09-03 · FR-V12-R-054 | Pre: PP-01 | Request; self-approve; approve by other | 403 `SAME_APPROVER`; then revision Active with diff hash | P0 | T07 | DT | Y | SYS |
| TC-V12-R-036 | Promotion refused with sandbox credential | TS-V12-R-23 · FR-V12-R-055 | Pre: PP-01. Data: revision referencing `gek_test_` | Request promotion | 422 `CONTAINS_SANDBOX_CREDENTIAL` | P1 | T07 | EP | Y | SYS |

#### Group TC-V12-R-C: Connectors (US-18-ZR11, US-07-ZR12/13, US-23-ZR14, US-22-ZR15)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-037 | Manifest completeness for every connector | TS-V12-R-24 · FR-V12-R-056 | Pre: CI | Validate manifests against schema | All 5 R1 connectors have auth, scopes, data classes, events, limits, failure classes, sandbox, owner | P1 | T01 | EP | Y | UT |
| TC-V12-R-038 | Secrets only in vault; workers refresh | TS-V12-R-24 · FR-V12-R-057 | Pre: PP-05 | OAuth connect; grep DB, logs, HTML for token | Only `credential_ref` stored; 0 matches; browser never receives refresh token | P0 | T07 | EG | Y | IT |
| TC-V12-R-039 | Gate checklist and SoD on activation | TS-V12-R-24 · AC-18ZR11-01…04 · FR-V12-R-058, 059 | Pre: PP-01. Data: evidence sets complete / missing each item / unapproved pack | Request; approve | Matches AC rows; DB guard raises for unapproved pack | P0 | T19 | DT | Y | SYS |
| TC-V12-R-040 | CRM consent protection and opt-out import | TS-V12-R-24 · AC-07ZR13-01/02 · FR-V12-R-063, 064 | Pre: PP-05 CRM simulator (each provider) | Send opt-in over suppression; send opt-out | Suppression kept; conflict logged; opt-out imported | P0 | T19 | DT | Y | IT |
| TC-V12-R-041 | Field policy conflicts and webhook authenticity | TS-V12-R-24 · AC-07ZR13-04 · FR-V12-R-065, 068 | Pre: PP-05. Data: simultaneous edits; forged HubSpot signature | Sync; post forged event | Conflict queued; forged event 401, not persisted | P0 | T07 | EG | Y | IT |
| TC-V12-R-042 | Change capture gap repair | TS-V12-R-24 · FR-V12-R-067 | Pre: PP-05. Data: 3 events dropped by simulator | Run sync | Gap detected; repair fetch; no duplicates | P1 | T16 | EG | Y | IT |
| TC-V12-R-043 | Health metrics and alert | TS-V12-R-24 · AC-18ZR11-05 · FR-V12-R-062 | Pre: PP-05 | Inject 60% errors | Breaker open, `Degraded`, alert ≤ 5 min | P1 | T21 | EP | Y | IT |
| TC-V12-R-044 | DLT registration formats and template match | TS-V12-R-24 · AC-23ZR14-01/02 · FR-V12-R-070, 074 | Pre: PP-05 aggregator simulator. Data: entity ID 18 digits; template with 2 vars; message with 3 | Register; dispatch | 422 `ENTITY_ID_FORMAT`; HOLD `DLT_TEMPLATE_MISMATCH` | P0 | T19 | BVA | Y | IT |
| TC-V12-R-045 | Promotional window boundaries and variable injection | TS-V12-R-24 · AC-23ZR14-04 · FR-V12-R-072 | Pre: PP-04 engine. Data: times 08:59…21:00; variable with a URL not in pattern | Evaluate | Per AC table; variable rejected `TEMPLATE_VARIABLES` | P0 | T19 | BVA | Y | UT |
| TC-V12-R-046 | DLR reconciliation and STOP | TS-V12-R-24 · AC-23ZR14-05 · FR-V12-R-073 | Pre: PP-05 | Send; DLR; inbound STOP | Delivered state; suppression ≤ 60 s; confirmation on service header | P0 | T19 | UC | Y | IT |
| TC-V12-R-047 | Transfer entry for out-of-zone provider (EU tenant, US-hosted CRM) | TS-V12-R-24 · FR-V12-R-079 | Pre: EU test cell. Data: no CJ-R15 entry | Request activation | 409 gate incomplete "transfer basis CJ-R15 missing" | P0 | T19 | EP | Y | SYS |
| TC-V12-R-048 | Number series vs purpose | TS-V12-R-24 · AC-22ZR15-02 · FR-V12-R-075 | Pre: PP-05 | Register 140 as service; promotional from 160 | 422 `SERIES_PURPOSE_MISMATCH`; HOLD | P0 | T19 | DT | Y | IT |
| TC-V12-R-049 | Click-to-call and uncertain status | TS-V12-R-24 · AC-22ZR15-01/04 · FR-V12-R-076 | Pre: PP-05 CPaaS simulator | Call; timeout after accept | Completed; second case `Uncertain` reconciled before retry | P1 | T18 | UC | Y | IT |
| TC-V12-R-050 | Recording consent and Part 11.18 interface | TS-V12-R-24 · AC-22ZR15-03 · FR-V12-R-077, 078 | Pre: PP-05; pack all-party consent | Call without consent; AI voice workflow call via VoicePort | No recording; AI workflow call carries Part 11.18 disclosure/consent fields or is refused | P0 | T19 | DT | Y | IT |

#### Group TC-V12-R-D: Vercel path, recovery, registry, benchmarks, database roles

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-051 | Project-zone and domain binding | TS-V12-R-25 · AC-21ZR16-02 · FR-V12-R-081 | Pre: Vercel API mock. Data: IN domain attached to `web-eu` | Run AU-296 | VD-11 fail; finding; deployment block | P0 | T19 | EP | Y | SYS |
| TC-V12-R-052 | Region pin check and fallback | TS-V12-R-25 · AC-21ZR16-01 · FR-V12-R-082, 094 | Pre: CI | Deploy with `iad1`; simulate Vercel outage | Blocked; DNS fallback runbook serves from S3/CloudFront in zone | P0 | T19 | EP | Y | SYS |
| TC-V12-R-053 | No bodies or tokens in logs | TS-V12-R-25 · AC-21ZR17-01 · FR-V12-R-085, 086 | Pre: staging. Data: 1,000 requests with bodies and `?token=` | Send; scan drain | 0 bodies, 0 tokens; lint fails on body logging | P0 | T19 | EG | Y | SYS |
| TC-V12-R-054 | Origin bypass blocked | TS-V12-R-25 · AC-21ZR17-02 · FR-V12-R-088 | Pre: staging | Direct call without header; with stale secret after overlap | 403 both | P0 | T07 | EP | Y | SYS |
| TC-V12-R-055 | Header allowlist | TS-V12-R-25 · AC-21ZR17-03 · FR-V12-R-087 | Pre: staging. Data: 20 headers | Send | Only VD-05 headers reach origin | P0 | T07 | EP | Y | SYS |
| TC-V12-R-056 | No caching of personal responses | TS-V12-R-25 · FR-V12-R-089 | Pre: staging | Two users fetch the same portal URL | `no-store`; no `x-vercel-cache: HIT` | P0 | T07 | EG | Y | SYS |
| TC-V12-R-057 | Sub-processor list and notice | TS-V12-R-25 · AC-21ZR17-04 · FR-V12-R-091 | Pre: DB | Insert row with notice 20 days | Check violation | P1 | T19 | BVA | Y | UT |
| TC-V12-R-058 | Edge-transit position in IN and EU packs | TS-V12-R-25 · FR-V12-R-095; DEC-887 | Pre: Part 11.15 packs | Document check | Both packs contain the approved wording and counsel reference | P0 | T19 | EP | N (document review) | UAT |
| TC-V12-R-059 | PITR enabled at maximum retention per zone | TS-V12-R-26 · FR-V12-R-096 | Pre: management API | Read status | Enabled; retention recorded in `recovery_path` | P0 | T21 | EP | Y | SYS |
| TC-V12-R-060 | Standby replicates with schema parity | TS-V12-R-26 · FR-V12-R-097, 101 | Pre: staging | Apply migration; write rows | Subscriber has the same schema; lag < 60 s | P0 | T21 | EP | Y | IT |
| TC-V12-R-061 | Encryption, Object Lock and two-holder restore credentials | TS-V12-R-26 · FR-V12-R-098, 110 | Pre: AWS | Attempt delete; read with one holder | Denied; restore needs both | P0 | T07 | EG | Y | SYS |
| TC-V12-R-062 | Monitor thresholds | TS-V12-R-26 · AC-21ZR18-02 · FR-V12-R-100 | Pre: stop subscriber | Wait | Warn 5, page 10, SEV1 15 min | P0 | T21 | BVA | Y | SYS |
| TC-V12-R-063 | Growth RTO ≤ 120 min drill | TS-V12-R-26 · AC-21ZR19-01 · FR-V12-R-103; KPI-32 | Pre: drill env | Run DR-R2 | `achieved_rto_min` ≤ 120 | P0 | T21 | UC | Y | E2E |
| TC-V12-R-064 | Drill cadence enforced | TS-V12-R-26 · FR-V12-R-104 | Pre: release record without drill | Open gate | Gate blocked "drill missing" | P0 | T21 | EP | Y | SYS |
| TC-V12-R-065 | PRV pack and erasure replay | TS-V12-R-26 · AC-21ZR19-03 · FR-V12-R-105, 106 | Pre: drill | Restore | PRV-01…08 pass; erased subject absent | P0 | T19 | UC | Y | E2E |
| TC-V12-R-066 | Missed RPO blocks release | TS-V12-R-26 · AC-21ZR19-02 · FR-V12-R-108 | Pre: drill with lag 17 min | Restore | `passed=false`; blocker | P0 | T21 | BVA | Y | E2E |
| TC-V12-R-067 | Registry constraints | TS-V12-R-27 · AC-04ZR20-03 · FR-V12-R-111, 112, 130 | Pre: PP-05 | Insert free-tier row with Personal; open-weight with Restricted; approved without DPA | Three check violations | P0 | T14 | EP | Y | IT |
| TC-V12-R-068 | Evidence completeness gate | TS-V12-R-27 · FR-V12-R-113 | Pre: PP-01 | Approve with each evidence item missing | 422 `EVIDENCE_INCOMPLETE` naming the item | P0 | T19 | EP | Y | SYS |
| TC-V12-R-069 | Two distinct approvers | TS-V12-R-27 · AC-04ZR20-01/02 · FR-V12-R-114 | Pre: PP-01 | Approve twice by same; then by R01 delegate | 403; then approved | P0 | T19 | DT | Y | SYS |
| TC-V12-R-070 | REG-002 Founder approval record | TS-V12-R-27 · AC-04ZR23-01 · FR-V12-R-115 | Pre: seeded registry | Read REG-002 | Approval cites DEC-788; default for MDL-M1 | P1 | T19 | EP | Y | SYS |
| TC-V12-R-071 | Fallback rule and route explanation | TS-V12-R-27 · FR-V12-R-121, 122, 128 | Pre: PP-05; primary 503 | Run step | Fallback to same-schema same-zone row or HOLD; explanation lists reasons | P0 | T14 | DT | Y | IT |
| TC-V12-R-072 | Re-certification suspension | TS-V12-R-27 · AC-04ZR21-02 · FR-V12-R-124 | Pre: row with `recert_due` yesterday | Run AU-298 | Suspended; routing updated ≤ 60 s | P0 | T19 | EP | Y | IT |
| TC-V12-R-073 | Kill switch ≤ 60 s | TS-V12-R-27 · AC-04ZR22-02 · FR-V12-R-123 | Pre: PP-05 | Set switch; run steps | No calls after 60 s; HOLD | P0 | T14 | BVA | Y | IT |
| TC-V12-R-074 | Canary promotion criteria | TS-V12-R-27 · AC-04ZR23-02 · FR-V12-R-127 | Pre: replay traffic | Run 7-day canary (accelerated) | 5% share; promoted only if not worse | P2 | T14 | EP | Y | SYS |
| TC-V12-R-075 | Opt-in and withdrawal | TS-V12-R-28 · AC-17ZR24-01 · FR-V12-R-131, 132 | Pre: PP-01 | Opt in; withdraw mid-period | Contributions from next period; withdrawal effective next period | P0 | T19 | ST | Y | SYS |
| TC-V12-R-076 | Contributions only inside tenant context | TS-V12-R-28 · FR-V12-R-135 | Pre: PP-05 | Call `bench_contribute` without context; as app_bench SELECT lead | `CONTEXT_MISSING`; permission denied | P0 | T15 | EG | Y | IT |
| TC-V12-R-077 | k = 9 suppressed, k = 10 published | TS-V12-R-28 · FR-V12-R-136 | Pre: BM-FIX-1 | Aggregate | Suppressed / published with band 10–24 | P0 | T19 | BVA | Y | IT |
| TC-V12-R-078 | Noise distribution and ledger | TS-V12-R-28 · FR-V12-R-138 | Pre: PP-04 | 10,000 draws with fixed seed | Empirical scale within 5% of Δ/ε; ledger adds 0.5 per release; 13th release in a year refused | P0 | T19 | PBT | Y | UT |
| TC-V12-R-079 | Only rates and durations, rounded | TS-V12-R-28 · FR-V12-R-140 | Pre: PP-01 | Read cells | No counts or amounts; rounding applied | P1 | T19 | EP | Y | SYS |
| TC-V12-R-080 | Merge-up and DPIA gate | TS-V12-R-28 · FR-V12-R-141, 142 | Pre: cohort with 6 in band, 11 overall | Aggregate; publish without DPIA ref | Published at merged level; publication blocked until DPIA ref present | P0 | T19 | DT | Y | SYS |
| TC-V12-R-081 | Data API closed | TS-V12-R-28 · AC-01ZR27-01 · FR-V12-R-145 | Pre: Supabase branch | Call REST/GraphQL for `ge` tables | 404 / permission denied | P0 | T07 | EP | Y | IT |
| TC-V12-R-082 | No service_role in runtime; detector | TS-V12-R-28 · AC-01ZR27-02 · FR-V12-R-144, 155 | Pre: CI and staging | Add env var to task def; open session as service_role from app subnet | Deploy fails; SEV2 ≤ 2 min | P0 | T07 | EG | Y | SYS |
| TC-V12-R-083 | Break-glass migration record | TS-V12-R-28 · AC-01ZR27-03 · FR-V12-R-146 | Pre: CI | Run with and without approvals | Without: blocked; with: audit has two approvers, expiry | P0 | T07 | DT | Y | SYS |
| TC-V12-R-084 | Context per transaction under pooling | TS-V12-R-28 · FR-V12-R-143, 148 | Pre: PP-05 Supavisor transaction mode | 1,000 interleaved requests for two tenants | 0 cross-tenant rows; missing context → `CONTEXT_MISSING` | P0 | T15 | PBT | Y | IT |
| TC-V12-R-085 | Forced RLS and no-bypass assertions; drift | TS-V12-R-28 · AC-01ZR26-02 · FR-V12-R-149, 150, 154 | Pre: branch | Create table without RLS; alter role BYPASSRLS; run AU-292 | CI raises both errors; drift finding | P0 | T07 | EG | Y | IT |
| TC-V12-R-086 | Idempotent role rename | TS-V12-R-28 · FR-V12-R-151 | Pre: DB with `ge_*` roles | Run DDL-V12-R-16 twice | Roles renamed once; second run no-op; grants intact | P1 | T16 | EP | Y | IT |

### 11.19.5.19 Test cases (generated, parameterized form)

{{TC_GEN}}
