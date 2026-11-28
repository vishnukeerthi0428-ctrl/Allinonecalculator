
## 11.17.12 Test scenarios and test cases

Template: Part 6.2a §6.2.1.2 exactly (full form and parameterized form; columns ID · Title · Links · Preconditions · Test data · Steps · Expected result · P · Type · Tech · Auto · Lvl). Conventions: NSE = no side effect (no state change, no outbox row, empty provider/portal simulator log for the correlation ID, no reservation, denial audit event written); U404 = uniform 404; precondition profiles PP-01…PP-07 (Part 6.2a §6.2.1.3) with these Group P additions:

| Profile | Context | Defaults |
|---|---|---|
| **PP-P1 Mandate IT** | PP-05 plus MND service, AU-260…268, KMS local stub (ES256), Valkey, synthetic rule packs `RP-IN-PAY-syn`, `RP-EU-PAY-syn`, `RP-GL-AGENTCOM-syn`, `RP-IN-PROC-syn` in state Approved unless stated | Virtual clock CLK-P0 = Tue 2027-03-02 11:00:00 IST; tenant T1 "Owner Portfolio", company OrganicSpec (IN) and tenant T3 "EuroAgri GmbH" (EU); mandate MND-41 (MT-PAY, per action ₹50,000.00, aggregate ₹2,00,000.00/month, count 10, velocity 3/10 min, Mon–Fri 09:00–18:00 IST) Active, not in shadow |
| **PP-P2 Commerce IT** | PP-P1 plus agent gateway, AU-269…277, DID resolver stub, status-list stub, PSP simulator (modes success, pending, declined, timeout, soft-decline-auth) | Counterparty "did:web:agents.greenfarms.example" T3; MT-COM MND-60 (list ₹4,000.00, floor ₹3,520.00, step 2%, rounds 4) |
| **PP-P3 Bid IT** | PP-P1 plus AU-278/279, portal simulator per adapter (accept, reject, timeout, captcha), S3 object-lock emulator | Tender TND-2027-118 deadline 2027-05-12 17:00 IST; B_auto 6 h; B_hard 2 h |

### 11.17.12.1 Test scenarios

| TS ID | Scenario | Linked stories / FR | Risk area · Priority | TCs |
|---|---|---|---|---|
| TS-18-ZP01 | PDP decides every mandated dispatch by the fixed rule order (3-way, positive and single-fault layers) | US-18-ZP03 · FR-V12-P-040…052 | Unauthorized or duplicate external action · **P0** | TC-V12-P-001…300 |
| TS-18-ZP02 | Kill switch blocks or reconciles every phase at every scope (exhaustive) | US-18-ZP06 · FR-V12-P-053…058 | Rollback / stop · **P0** | TC-V12-P-653…716, 730, 731 |
| TS-18-ZP03 | Mandate lifecycle, approvals, digest and versioning | US-18-ZP01/02/05 · FR-V12-P-006…022, 032 | Unauthorized authority · **P0** | TC-V12-P-717…725, 732…740, 757…763 |
| TS-18-ZP04 | Ledger concurrency, idempotency and caps | US-18-ZP04 · FR-V12-P-023…036 | Financial accuracy · **P0** | TC-V12-P-726…729 |
| TS-18-ZP05 | Reconciliation, anomaly detection, shadow and evidence | US-18-ZP07/08/09 · FR-V12-P-037, 059…067 | Financial accuracy · **P0** | TC-V12-P-741…754, 764 |
| TS-18-ZP06 | L4 binding, regulatory override, residency | US-18-ZP10 · FR-V12-P-004, 005, 098 | Regulatory eligibility · **P0** | TC-V12-P-753, 755, 756 |
| TS-24-ZP01 | Agent identity, verification, tiers, interop gate | US-24-ZP01/02/05 · FR-V12-P-070…077, 094, 097 | Impersonation · **P0** | TC-V12-P-765…772, 785, 788 |
| TS-24-ZP02 | Negotiation and payment decision (3-way, positive and single-fault layers) | US-24-ZP03/04 · FR-V12-P-078…087 | Unauthorized commitment or payment · **P0** | TC-V12-P-301…523, 773, 781…784, 786, 787, 789 |
| TS-15-ZP01 | PSP mandates, execution, settlement, ledger, refunds, disputes | US-15-ZP01…03 · FR-V12-P-083…092 | Financial accuracy · **P0** | TC-V12-P-774…780 |
| TS-14-ZP01 | Bid submission mode, mandate, guard, receipt (3-way, positive and single-fault layers) | US-14-ZP01…04 · FR-V12-P-110…135 | Unapproved submission; deadline · **P0** | TC-V12-P-524…652, 790…815 |
| TS-P-NFR | Performance, accessibility, localisation, DR for Group P | All | NFR · **P1** | TC-V12-P-816…826 |

### 11.17.12.2 Test cases: mandate lifecycle, approvals and ledger (full form)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-P-717 | Two distinct Finance users approve the same digest | TS-18-ZP03 · US-18-ZP02 AC-18ZP02-01 · FR-V12-P-015; TPA-01/02; DEC-842 | Pre: PP-P1, MND-77 v1 PendingApproval1 requested by `meera` R07. Data: `lata` R08 MFA 2 min, `arjun` R09 MFA 1 min | 1. POST approval as `lata` with digest D1. 2. POST approval as `arjun` with D1. 3. GET mandate | 1: 201, state PendingApproval2. 2: 201, state Approved, JWS `kid=mnd-sign-IN#…`. 3: two approval rows with mfa_at; audit `mandate.approved` chained | P0 | T01, T07 | ST | Y | IT |
| TC-V12-P-718 | Requester and second account of the same person cannot approve | TS-18-ZP03 · AC-18ZP02-02 · TPA-02; ABAC-03; THR-V12-P-15; ABU-P-02 | Pre: PP-P1. Data: `meera` and `meera.alt` linked to the same IdP person ID | Approve as `meera`; approve as `meera.alt` | Both 403 `SOD_VIOLATION`; NSE; security event `SEC-MND-03` | P0 | T07 | EG | Y | IT |
| TC-V12-P-719 | Delegation to the requester is blocked | TS-18-ZP03 · TPA-07; BRL-APR-09; ABU-P-10 | Pre: PP-P1. Data: `lata` delegates to `meera` for 7 days | `meera` approves as delegate | 403 `SOD_VIOLATION`; delegation itself rejected at creation for MND scope (422 `DELEGATE_IS_REQUESTER`) | P0 | T07 | EG | Y | IT |
| TC-V12-P-720 | R3 type without Finance approver cannot reach Approved | TS-18-ZP03 · TPA-04; MC-07 | Pre: PP-P1. Data: MT-PAY approvals by R02 and R03L | Approve twice | Second approval 403 `ROLE_MIX_REQUIRED` (needs R08/R09); state PendingApproval2 | P0 | T07, T19 | DT | Y | IT |
| TC-V12-P-721 | Stale step-up and unknown device | TS-18-ZP03 · AC-18ZP02-04 · TPA-05; MC-22; THR-V12-P-14; ABU-P-19 | Pre: PP-P1. Data: `arjun` MFA 6 min; second run new device | Approve | 401 `STEP_UP_REQUIRED`; on new device: approval allowed after WebAuthn, new-device notification sent, `SEC-MND-04` logged | P0 | T07 | BVA | Y | IT |
| TC-V12-P-722 | Approval cannot happen from a notification | TS-18-ZP03 · AC-18ZP02-08 · MC-23; MOB-09 | Pre: PP-06 mobile viewport 390×844. Data: push deep link | Tap link; try `POST /approvals` without the A262 flow token | A262 opens with full mandate; direct POST without A262 view token 409 `REVIEW_VIEW_REQUIRED`; NSE | P0 | T07, T10 | EG | Y | E2E |
| TC-V12-P-723 | Digest mismatch and tampered row | TS-18-ZP03 · AC-18ZP02-05, AC-18ZP03-02 · FR-V12-P-021; THR-V12-P-16, 21; ABU-P-11 | Pre: PP-P1. Data: approval with digest D2 ≠ stored D1; later SQL update to body under break-glass in test DB | 1. Approve with D2. 2. Tamper body. 3. Dispatch | 1: 409 `DIGEST_MISMATCH`. 3: DENY `MANDATE_INTEGRITY_FAILURE`; mandate Suspended; `SEC-MND-01`; NSE | P0 | T07 | EG | Y | IT |
| TC-V12-P-724 | Tightening overlay immediate; loosening refused | TS-18-ZP03 · AC-18ZP05-02/03 · FR-V12-P-022; MC-08; BRL-APR-11 | Pre: PP-P1. Data: per action 50,000.00 → 25,000.00; then → 60,000.00 | POST restrictions; dispatch ₹30,000.00 | Tighten 201; dispatch ROUTE `PER_ACTION_CAP_EXCEEDED_L2`; loosen 422 `NOT_TIGHTENING` | P0 | T01 | BVA | Y | IT |
| TC-V12-P-725 | ROUTE creates an exact-item approval task | TS-18-ZP03 · FR-V12-P-002 | Pre: PP-P1. Data: intent ₹60,000.00 | Dispatch; approve task in A106 with exact hash; redispatch | Task holds payload hash; after approval the effect executes once as L2 and counts against aggregate | P1 | T01 | UC | Y | SYS |
| TC-V12-P-726 | 100 concurrent reservations respect aggregate | TS-18-ZP04 · AC-18ZP04-03 · LED-02; THR-V12-P-10 | Pre: PP-P1. Data: headroom ₹17,500.00; 100 intents ₹1,000.00 | Fire in parallel (100 threads) | Exactly 17 Reserved; 83 ROUTE; Σ reserved = ₹17,000.00; no deadlock > 5 s | P0 | T16, T03 | PBT | Y | IT |
| TC-V12-P-727 | Boundary inclusive | TS-18-ZP04 · AC-18ZP04-01/02 · DEC-843 | Pre: PP-P1. Data: ₹17,500.00 / ₹17,500.01 | Two dispatches | ALLOW / ROUTE `AGGREGATE_CAP_EXCEEDED_L2` | P0 | T01 | BVA | Y | UT |
| TC-V12-P-728 | Idempotency key replay | TS-18-ZP04 · AC-18ZP04-05 · MC-21; KPI-P-09 | Pre: PP-P1 | Same intent twice; also after worker crash between reserve and call | One reservation; one PSP call; KPI duplicate = 0 | P0 | T16 | EG | Y | IT |
| TC-V12-P-729 | Reservation TTL release only if no call made | TS-18-ZP04 · LED-03 | Pre: PP-P1. Data: reservation aged 16 min with/without outbox call | Run AU-263 sweeper | Without call: Released. With call: Held(Reconciling) | P0 | T18 | ST | Y | IT |
| TC-V12-P-730 | Revocation latency and PSP cancel | TS-18-ZP02 · AC-18ZP05-01 · MC-06; FR-V12-P-095; KPI-P-03 | Pre: PP-P2 with UPI-MD-7781 | Revoke; dispatch at +1 s, +5 s; read PSP simulator | +5 s DENY `MANDATE_REVOKED`; p99 measured ≤ 5 s over 200 trials; PSP cancel request and ack stored | P0 | T07, T21 | ST | Y | IT |
| TC-V12-P-731 | Adapter gateway rejects forged or stale decision | TS-18-ZP02 · AC-18ZP05-05 · THR-V12-P-08, 09 | Pre: PP-P1 | Call adapter with fabricated decision ID; with fence 41 when current 42 | 403 `DECISION_INVALID`; 409 `STALE_FENCE`; `SEC-MND-02`; NSE | P0 | T07 | EG | Y | IT |
| TC-V12-P-732 | Company ceiling loosening needs two people | TS-18-ZP03 · ABU-P-12; BRL-APR-11 | Pre: PP-P1. Data: R12 raises CFG-P-01 | PATCH config | Pending second approval; ceiling unchanged until approved | P0 | T07 | EG | Y | IT |
| TC-V12-P-733 | Dormant mandate reactivation after contract end | TS-18-ZP03 · ABU-P-13 | Pre: PP-P1. Data: MND-41 no effects for 60 days; contract ended flag | Dispatch | AR-11/AR-03 shadow L2; revocation suggestion RV-08 | P1 | T19 | UC | Y | IT |
| TC-V12-P-734 | Resume needs two people and cause evidence | TS-18-ZP03 · TPA-10; ABU-P-14 | Pre: PP-P1 MND-41 Suspended (AR-07) | Resume by one; by two without evidence; with evidence | 403; 422 `CAUSE_EVIDENCE_REQUIRED`; 200 Active after PDP recheck | P0 | T07 | DT | Y | IT |
| TC-V12-P-735 | Pending approval auto-withdraws after 7 days | TS-18-ZP03 · TPA-08 | Pre: PP-P1, clock +7 d | Advance clock | Draft; escalation at 1 bd recorded; never auto-approved | P1 | T01 | ST | Y | IT |
| TC-V12-P-736 | Conflict-of-interest approver excluded | TS-18-ZP03 · TPA-09 | Pre: PP-P1. Data: `lata` owns CRM account Green Farms | Assign approvers | `lata` not eligible; reason shown | P1 | T07 | DT | Y | IT |
| TC-V12-P-737 | Approved mandate does not activate while a pack is Draft | TS-18-ZP03 · MC-10 | Pre: PP-P1, RP-IN-PAY-syn Draft | AU-262 tick | Stays Approved; reason `JURISDICTION_PACK_NOT_APPROVED` | P0 | T19 | ST | Y | IT |
| TC-V12-P-738 | MT-PAY not Active until PSP mandate active | TS-18-ZP03 · §11.17.5.8 | Pre: PP-P2, PSP mandate pending | Tick | Approved; after webhook `mandate.active` → Active | P0 | T01 | ST | Y | IT |
| TC-V12-P-739 | Expiry inline even if scheduler is down | TS-18-ZP03 · AU-262 | Pre: PP-P1, scheduler stopped, clock past expires_at | Dispatch | DENY `MANDATE_WINDOW_ENDED` | P0 | T01 | EG | Y | IT |
| TC-V12-P-740 | Exhaustion by count | TS-18-ZP03 · FR-V12-P-023 | Pre: PP-P1, 10th payment of month | Commit; next dispatch | State Exhausted (if period=mandate) or `COUNT_CAP_REACHED` HOLD until next month | P1 | T01 | BVA | Y | IT |
| TC-V12-P-741 | Clean daily reconciliation | TS-18-ZP05 · AC-18ZP08-01 · RC-P-01/02 | Pre: PP-P2, 12 committed with receipts and settlement file | Run AU-268/274 | 12 matched; 0 breaks | P0 | T01 | EP | Y | IT |
| TC-V12-P-742 | Unexpected PSP capture suspends mandate | TS-18-ZP05 · AC-18ZP08-02 · MC-14; SEC-PAY-02 | Pre: PP-P2. Data: capture with no reservation | Run recon | Break `UNEXPECTED_EFFECT`; Suspended; SEV2 | P0 | T19 | EG | Y | IT |
| TC-V12-P-743 | PSP mandate active while platform revoked | TS-18-ZP05 · RC-P-04 | Pre: PP-P2 | Run RC-P-04 | AU-266 re-cancel; SEV2 | P0 | T19 | EG | Y | IT |
| TC-V12-P-744 | Break closure by maker ≠ checker with evidence | TS-18-ZP05 · BRL-APR-07; ABU-P-15 | Pre: PP-P2 open break | Close by maker only; by maker+checker without evidence; with evidence | 409; 422; 200 | P0 | T07 | DT | Y | IT |
| TC-V12-P-745 | AR-01 near-cap clustering | TS-18-ZP05 · AR-01 | Pre: PP-P1. Data: 3 × ₹47,600.00 (≥ 95%) | Dispatch 4th | ROUTE; alert AR-01 | P1 | T19 | BVA | Y | IT |
| TC-V12-P-746 | AR-04 split transactions | TS-18-ZP05 · AC-18ZP07-01 · ABU-P-01 | Pre: PP-P1. Data: 3 × ₹30,000.00 same day | Dispatch 3rd | ROUTE; AG-201 explanation cites 3 rows | P0 | T19 | EG | Y | IT |
| TC-V12-P-747 | AR-06 instrument change suspends | TS-18-ZP05 · AC-18ZP07-02 · FC-02; THR-V12-P-22 | Pre: PP-P2 instrument changed 3 days ago | Dispatch | Suspended for counterparty; call-back task | P0 | T07 | EG | Y | IT |
| TC-V12-P-748 | AR-08 decline rate suspends | TS-18-ZP05 · AR-08 | Pre: PP-P2, 5 of last 20 declined | Dispatch | Suspended | P1 | T19 | BVA | Y | IT |
| TC-V12-P-749 | Anomaly thresholds cannot be loosened by tenant | TS-18-ZP05 · ABU-P-16; MC-15 | Pre: PP-P1, R11 | PATCH AR-01 threshold 3 → 10 | 422 `TIGHTEN_ONLY`; 3 → 2 accepted | P0 | T07 | EG | Y | IT |
| TC-V12-P-750 | Heartbeat loss suspends money mandates | TS-18-ZP05 · AC-18ZP07-04 · THR-V12-P-23 | Pre: PP-P1, stop AU-267 | Advance 15 min | MT-PAY Suspended `ANOMALY_ENGINE_DOWN` | P0 | T21 | ST | Y | IT |
| TC-V12-P-751 | Shadow period lifecycle | TS-18-ZP05 · AC-18ZP09-01…03 · MC-16 | Pre: PP-P1 first MT-PAY in shadow | 20 decisions over 14 d; R10 sign-off; then a rejection in another tenant | ROUTE `SHADOW_PERIOD_L2` until exit; ALLOW after; reset on rejection | P0 | T01 | ST | Y | IT |
| TC-V12-P-752 | MT-OUT still applies consent, quiet hours, first-touch | TS-18-ZP05 · MC-19; ABU-P-05; DEC-777 | Pre: PP-P1 MND-50 MT-OUT; recipient opted out; one at 21:05 local; one first-touch | Dispatch three | HOLD `SUPPRESSED`; DEFER window; ROUTE L2 first-touch | P0 | T19 | DT | Y | IT |
| TC-V12-P-753 | Residency of mandate execution | TS-18-ZP06 · MC-20; FR-V12-P-098; THR-V12-P-26 | Pre: PP-P1 tenant T3 EU | Create mandate, dispatch, export pack; inspect network egress | All writes in EU DB; PSP EU account; no call to IN endpoints (egress log) | P0 | T19, T15 | EG | Y | SYS |
| TC-V12-P-754 | Evidence pack signed and complete | TS-18-ZP05 · AC-18ZP08-03 · MC-24 | Pre: PP-P2 MND-41 with 12 effects | Export; verify manifest | ZIP contents complete; signature verifies; hash of each file matches manifest | P0 | T19 | EP | Y | IT |
| TC-V12-P-755 | L4 plan cannot expand authority | TS-18-ZP06 · AC-18ZP10-01…03 · THR-V12-P-24; ABU-P-17 | Pre: PP-P1 PLN-9 bound to MND-50 | Run plan; inject new action type; plan budget 300 | L4 dispatches decided; DENY `ACTION_NOT_IN_MANDATE`; 422 on budget | P0 | T07 | DT | Y | IT |
| TC-V12-P-756 | Stricter rule pack overrides the mandate level | TS-18-ZP06 · FR-V12-P-005 | Pre: PP-P1, RP-IN-PAY-syn rule "max level L2 for amounts > ₹15,000.00 without AFA" | Dispatch ₹20,000.00 under L3 mandate | ROUTE L2 with pack rule ID | P0 | T19 | DT | Y | IT |
| TC-V12-P-757 | Mandate schema validation | TS-18-ZP03 · FR-V12-P-006…012 | Pre: PP-01 | 35-field fuzz with Hypothesis (release profile 10,000) | Invalid → 422 with field paths; valid → 201; no 500 | P1 | T01 | PBT | Y | UT |
| TC-V12-P-758 | Ineligible workflow rejected at submit | TS-18-ZP03 · AC-18ZP01-05 · FR-V12-P-013 | Pre: PP-01 | Submit MT-PAY with SM-SVC-01-WF01 | 422 `WORKFLOW_NOT_ELIGIBLE` | P0 | T01 | EP | Y | IT |
| TC-V12-P-759 | Type rules (allowed actions, max validity) | TS-18-ZP03 · FR-V12-P-014 | Pre: PP-01. Data: MT-PAY validity 45 d; action `bid.submit` | Submit | 422 per rule | P1 | T01 | DT | Y | UT |
| TC-V12-P-760 | Simulation has zero effects | TS-18-ZP03 · AC-18ZP01-01 · FR-V12-P-028; BRL-AUT-04 | Pre: PP-P2 | Simulate | Report fields present; NSE | P0 | T17 | EP | Y | IT |
| TC-V12-P-761 | Illegal lifecycle transitions | TS-18-ZP03 · FR-V12-P-032 | Pre: PP-P1 | Try Revoked→Active, Draft→Approved, Closed→Suspended | 409 each; state unchanged | P1 | T01 | ST | Y | UT |
| TC-V12-P-762 | A260–A264 UI acceptance including minimum review time | TS-18-ZP03 · FR-V12-P-038; ABU-P-03 | Pre: PP-06 | Walk builder, approval, monitor, kill switch | Approve enabled after 30 s on A262; worst-case shown; states per Part 2.5 | P1 | T01, T08 | UC | Y | E2E |
| TC-V12-P-763 | Mandate API contract | TS-18-ZP03 · FR-V12-P-039 | Pre: PP-05 | Schemathesis against OpenAPI | 0 schema violations; idempotency honoured | P1 | T01 | PBT | Y | CT |
| TC-V12-P-764 | KPI tiles equal ledger truth | TS-18-ZP05 · FR-V12-P-068, 130 | Pre: PP-P2 seeded month | Compare A263/A089 tiles with SQL | Equal for KPI-P-01…12 | P2 | T01 | EP | Y | SYS |

### 11.17.12.3 Test cases: agentic commerce and payments (full form)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-P-765 | DID document and JWKS publish without private material | TS-24-ZP01 · AC-24ZP01-01 · FR-V12-P-070 | Pre: PP-P2 | GET did.json, jwks.json | Keys public only; `kid` matches KMS key; served only on verified domain | P0 | T07 | EP | Y | IT |
| TC-V12-P-766 | Mandate VC selective disclosure hides floor | TS-24-ZP01 · AC-24ZP01-03 · FR-V12-P-071; THR-V12-P-04 | Pre: PP-P2 MND-60 | Present VC to stub verifier | No `floor`, `ceiling`, `min_margin_pct` claims; signature valid | P0 | T07 | EP | Y | IT |
| TC-V12-P-767 | Envelope signature, tamper and replay | TS-24-ZP01 · AC-24ZP02-03 · FR-V12-P-072; THR-V12-P-02, 07 | Pre: PP-P2 | Send valid; body-altered; replayed nonce; exp passed | 202; 401 `SIGNATURE_INVALID`; 409 `REPLAY`; 401 `EXPIRED`; NSE for rejects | P0 | T07 | EG | Y | IT |
| TC-V12-P-768 | Tier gates actions | TS-24-ZP01 · FR-V12-P-074 | Pre: PP-P2 counterparties T0–T3 | RFQ, order ₹3,00,000.00 from each | T0 reject; T1 human quote only; T2 order > ₹2,00,000.00 ROUTE; T3 per mandate | P0 | T19 | DT | Y | IT |
| TC-V12-P-769 | Protocol adapters normalise to one envelope | TS-24-ZP01 · FR-V12-P-075 | Pre: PP-P2 fixtures A2A, AP2, ACP, MCP (versions verified at implementation) | Send equivalent RFQ via each | Identical internal envelope (except protocol field) | P1 | T01 | EP | Y | CT |
| TC-V12-P-770 | Interop gate five conditions | TS-24-ZP01 · AC-24ZP05-01/02 · FR-V12-P-076 | Pre: PP-P2 | Exhaustive 2⁵ = 32 combinations of the five conditions | Only all-true processes; others 403 `INTEROP_DISABLED` | P0 | T19 | EX | Y | IT |
| TC-V12-P-771 | Only Approved catalog version exposed | TS-24-ZP01 · AC-24ZP01-02 · FR-V12-P-077 | Pre: PP-P2 v6 Approved, v7 Draft | GET /agent/catalog | v6 only | P0 | T07 | EP | Y | IT |
| TC-V12-P-772 | Quote only after verification | TS-24-ZP01 · FR-V12-P-078 | Pre: PP-P2 resolver stub down | RFQ | HOLD; no quote; retried when resolver up | P0 | T01 | EG | Y | IT |
| TC-V12-P-773 | Commerce state machine and signed acceptance stored | TS-24-ZP02 · FR-V12-P-082; THR-V12-P-03 | Pre: PP-P2 | Walk Received→…→Paid; try Quoted→Paid | Legal path ok, acceptance JWS stored; illegal 409 | P1 | T01 | ST | Y | IT |
| TC-V12-P-774 | Unlicensed PSP cannot be activated | TS-15-ZP01 · FR-V12-P-083 | Pre: PP-01, PSP registry entry without licence evidence | Activate PSP | 422 `PSP_LICENCE_EVIDENCE_REQUIRED` | P0 | T19 | EP | Y | IT |
| TC-V12-P-775 | PSP mandate registered with platform cap; no credential stored | TS-15-ZP01 · AC-15ZP01-01/02 · FR-V12-P-084; BRL-FIN-07 | Pre: PP-P2 | Register UPI AutoPay; scan DB and logs with PAN/UPI-PIN/IBAN regexes | max = ₹50,000.00; only refs; 0 regex hits | P0 | T07 | EP | Y | IT |
| TC-V12-P-776 | Pre-debit notice lead time | TS-15-ZP01 · AC-15ZP01-03 · FR-V12-P-085 | Pre: PP-P2, RP-IN-PAY-syn lead 24 h; SDD-syn 14 d | Schedule debits | Debit not requested before notice + lead; boundary at exactly lead allowed | P0 | T19 | BVA | Y | IT |
| TC-V12-P-777 | Webhook signature and dedup | TS-15-ZP01 · FR-V12-P-088; THR-V12-P-18 | Pre: PP-P2 | Valid webhook twice; forged webhook | One capture recorded; forged 400 + `SEC-PAY-01`; NSE | P0 | T07, T16 | EG | Y | IT |
| TC-V12-P-778 | Refund to original instrument only | TS-15-ZP01 · AC-15ZP03-01/02 · FR-V12-P-090; ABU-P-09 | Pre: PP-P2 PAY-881 ₹11,800.00 | Refund ₹1,180.00 original; refund to other; refund ₹10,621.00 after first (total > captured) | J-05; ROUTE; 422 `REFUND_EXCEEDS_CAPTURED` | P0 | T01 | BVA | Y | IT |
| TC-V12-P-779 | Chargeback case, deadline and suspension | TS-15-ZP01 · AC-15ZP03-03 · FR-V12-P-091; THR-V12-P-30; ABU-P-20 | Pre: PP-P2 | Two chargebacks in 30 d on MND-41 | Cases with deadlines PSP − 3 bd; J-06; counterparty T0; mandate Suspended after 2nd | P0 | T19 | ST | Y | IT |
| TC-V12-P-780 | Journals balance; J-01…J-09 examples | TS-15-ZP01 · AC-15ZP02-01/03 · FR-V12-P-092 | Pre: PP-P2 | Post each example of §11.17.6.7; post unbalanced | All balance as tabled; unbalanced rejected | P0 | T01 | EP | Y | IT |
| TC-V12-P-781 | Message flood rate-limited per DID | TS-24-ZP02 · THR-V12-P-05 | Pre: PP-P2 | 500 RFQs/min from one DID | 429 after limit; AI budget reservation unchanged beyond quota | P1 | T20 | BVA | Y | IT |
| TC-V12-P-782 | Budget protection of commerce agents | TS-24-ZP02 · BRL-AI-08 | Pre: PP-P2, AG-202 budget 100% | RFQ | Tier 3: human queue; no model call | P0 | T20 | EP | Y | IT |
| TC-V12-P-783 | BEC payee swap blocked | TS-24-ZP02 · FC-02; THR-V12-P-22 | Pre: PP-P2 | Counterparty message announces new bank account; payment due | Payment HOLD; AR-06; call-back task | P0 | T07 | EG | Y | IT |
| TC-V12-P-784 | Floor probing detected | TS-24-ZP02 · ABU-P-08; AR-10 | Pre: PP-P2 | 30 small RFQs in 1 h | Rate limit; AR-10 alert; tier downgrade proposal | P1 | T19 | EG | Y | IT |
| TC-V12-P-785 | Sanctions screening downgrade | TS-24-ZP01 · AC-24ZP02-04 · FR-V12-P-094 | Pre: PP-P2 screening stub hit | Run 30-day job | T0; mandates suspended for counterparty | P0 | T19 | EP | Y | IT |
| TC-V12-P-786 | Negotiation counter arithmetic | TS-24-ZP02 · AC-24ZP03-01…03 · AU-271 | Pre: PP-P2 MND-60 | Offers ₹3,400.00 (r1), ₹3,520.00, ₹3,500.00 (r4) | ₹3,920.00 counter; ALLOW accept; ESCALATE | P0 | T01 | BVA | Y | UT |
| TC-V12-P-787 | A265–A267 UI acceptance | TS-24-ZP02 · FR-V12-P-096 | Pre: PP-06 | Walk screens as R03/R08/R10 | Floor hidden from R03 non-approver; untrusted badge on messages; maker-checker enforced | P1 | T01, T08 | UC | Y | E2E |
| TC-V12-P-788 | Consumer DID refused (B2B only) | TS-24-ZP01 · FR-V12-P-097 | Pre: PP-P2 DID without business identity VC | RFQ | T0; 403 `BUSINESS_IDENTITY_REQUIRED` | P0 | T19 | EP | Y | IT |
| TC-V12-P-789 | DTO enums and meter | TS-24-ZP02 · FR-V12-P-099 | Pre: PP-01 | Validate SM-SVC-28 DTO v2 with new enums; count sessions | Valid; meter = sessions reaching Accepted/Escalated | P1 | T01 | EP | Y | UT |

### 11.17.12.4 Test cases: automatic bid submission (full form)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-P-790 | Seal computes hash and locks files | TS-14-ZP01 · AC-14ZP01-01 · FR-V12-P-111 | Pre: PP-P3, 9 files | Seal; attempt overwrite in S3 | Hash recorded; overwrite denied by object lock | P0 | T07 | EP | Y | IT |
| TC-V12-P-791 | Gate blocks on blocking finding or missing approvals | TS-14-ZP01 · AC-14ZP01-02 · FR-V12-P-112 | Pre: PP-P3 | Seal with AG-207 blocking; with waiver approved | 422 `CHECKLIST_BLOCKING`; then sealable | P0 | T01 | DT | Y | IT |
| TC-V12-P-792 | Hash change voids MT-BID | TS-14-ZP01 · AC-14ZP01-03 · FR-V12-P-113 | Pre: PP-P3 MT-BID Active on H1 | Replace file; request submit | HOLD `PACKAGE_HASH_CHANGED_APPROVAL_VOID`; NSE | P0 | T07 | EG | Y | IT |
| TC-V12-P-793 | Single use and tender binding | TS-14-ZP01 · FR-V12-P-114; ABU-P-06 | Pre: PP-P3 after verified receipt | Submit again; use MT-BID on TND-2027-119 | DENY `MANDATE_EXHAUSTED`; DENY `SCOPE_TENDER_MISMATCH` | P0 | T07 | EG | Y | IT |
| TC-V12-P-794 | Guard boundary at B_auto | TS-14-ZP01 · FR-V12-P-115 | Pre: PP-P3 clock deadline − 6 h 00 m 01 s and − 5 h 59 m 59 s | Request AUTO | First: AUTO proceeds. Second: ESCALATE `INSIDE_DEADLINE_BUFFER_HUMAN`, assisted session prepared | P0 | T01 | BVA | Y | IT |
| TC-V12-P-795 | No retry inside B_hard | TS-14-ZP01 · FR-V12-P-116 | Pre: PP-P3 definite failure at deadline − 2 h 05 m; next retry would be − 1 h 35 m | Run | No automated retry; human paged | P0 | T01 | BVA | Y | IT |
| TC-V12-P-796 | Human may still submit manually inside buffer | TS-14-ZP01 · ABU-P-07; BRL-BID-01 amended | Pre: PP-P3 deadline − 1 h | Record manual evidence | Accepted as Submitted (MANUAL) with evidence; automated path closed | P1 | T01 | EP | Y | IT |
| TC-V12-P-797 | Portal outage at planned time falls back early | TS-14-ZP01 · THR-V12-P-12 | Pre: PP-P3 portal 503 at T−48 h | Run with retries 10/30/60 min | 3 retries then ASSISTED task at T−46 h | P0 | T21 | ST | Y | IT |
| TC-V12-P-798 | Escalation ladder notifications | TS-14-ZP01 · FR-V12-P-117 | Pre: PP-P3 no mandate at T−24 h | Advance clock | NT to R06/R02 at T−24 h; assisted at T−6 h; SEV2 at T−1 h | P1 | T21 | ST | Y | IT |
| TC-V12-P-799 | Clock skew closes the automated path | TS-14-ZP01 · THR-V12-P-29 | Pre: PP-P3 skew 1.5 s | Request AUTO | ESCALATE `CLOCK_SKEW`; alarm | P0 | T07 | EG | Y | IT |
| TC-V12-P-800 | Unreviewed portal is MANUAL_ONLY | TS-14-ZP01 · AC-14ZP04-01 · FR-V12-P-118 | Pre: PP-P3 new profile | Request submit | MANUAL; reason `PORTAL_MANUAL_ONLY` | P0 | T19 | EP | Y | IT |
| TC-V12-P-801 | Expired counsel review reverts capability | TS-14-ZP01 · FR-V12-P-118 | Pre: PP-P3 review_expires_at past | Request AUTO | ASSISTED; registry flag "review expired" | P0 | T19 | ST | Y | IT |
| TC-V12-P-802 | Capability change two-person | TS-14-ZP01 · AC-14ZP04-02 · FR-V12-P-119 | Pre: PP-01 | Change by R11 only | Pending until R10 | P0 | T07 | EG | Y | IT |
| TC-V12-P-803 | PA-ARIBA API submission happy path | TS-14-ZP01 · FR-V12-P-120 | Pre: PP-P3 Ariba simulator `API_PERMITTED` | AUTO submit | Receipt verified; mandate Exhausted | P0 | T01 | UC | Y | IT |
| TC-V12-P-804 | PA-EMAIL submission only when RFQ designates e-mail | TS-14-ZP01 · FR-V12-P-121 | Pre: PP-P3 two RFQs (with and without e-mail designation) | AUTO submit | First sent with sealed attachments and hash list; second MANUAL | P1 | T19 | DT | Y | IT |
| TC-V12-P-805 | Adapter contract conformance | TS-14-ZP01 · FR-V12-P-122 | Pre: PP-05 | Contract suite per adapter | prepare/submit/status/fetch_receipt shapes valid; idempotency honoured | P1 | T01 | EP | Y | CT |
| TC-V12-P-806 | Assisted session hash check | TS-14-ZP01 · AC-14ZP04-03 · FR-V12-P-123; THR-V12-P-25 | Pre: PP-P3 CPPP assisted | Upload wrong file | Blocked; `SEC-BID-01` | P0 | T07 | EG | Y | E2E |
| TC-V12-P-807 | Personal DSC never stored | TS-14-ZP01 · FR-V12-P-124 | Pre: PP-P3 | Scan secrets store and DB after assisted session | No DSC PIN, no private key | P0 | T07 | EP | Y | IT |
| TC-V12-P-808 | Receipt verification | TS-14-ZP01 · AC-14ZP03-01/04 · FR-V12-P-125; THR-V12-P-19 | Pre: PP-P3 receipts: correct; wrong tender; after deadline | Verify | Submitted; Reconciling + page; Reconciling + SEV2 | P0 | T01 | DT | Y | IT |
| TC-V12-P-809 | Unknown outcome reconciliation | TS-14-ZP01 · AC-14ZP03-02/03 · FR-V12-P-126 | Pre: PP-P3 timeout after upload | Run until hard stop | Status queries every 10 min; 0 re-uploads; human task at T−2 h | P0 | T18 | ST | Y | IT |
| TC-V12-P-810 | Browser automation constraints | TS-14-ZP01 · AC-14ZP04-04 · FR-V12-P-127; THR-V12-P-13 | Pre: PP-P3 automation portal with CAPTCHA | Run | unknown → ASSISTED; egress only to portal host; video/HAR stored with secrets redacted | P0 | T07 | EG | Y | IT |
| TC-V12-P-811 | Bid state machine extension | TS-14-ZP01 · FR-V12-P-128 | Pre: PP-01 | Walk legal and illegal transitions | 409 on illegal | P1 | T01 | ST | Y | UT |
| TC-V12-P-812 | A268/A269 UI acceptance | TS-14-ZP01 · FR-V12-P-129 | Pre: PP-06 | Walk as R06, R10 | Mode and reason visible; countdown UTC + local; keyboard operable | P1 | T01, T08 | UC | Y | E2E |
| TC-V12-P-813 | Agent cannot withdraw a bid | TS-14-ZP01 · FR-V12-P-131 | Pre: PP-P3 | Executor calls withdraw | 403 `ACTION_NOT_IN_MANDATE` | P0 | T07 | EG | Y | IT |
| TC-V12-P-814 | Submission evidence pack | TS-14-ZP01 · FR-V12-P-134 | Pre: PP-P3 after AUTO | Export | Manifest, approvals, guard log, HAR/video, receipt; signature verifies | P0 | T19 | EP | Y | IT |
| TC-V12-P-815 | Award separate from submission | TS-14-ZP01 · FR-V12-P-135; BRL-BID-05 | Pre: PP-P3 Submitted | Mark Awarded without proof | 422 `AWARD_PROOF_REQUIRED` | P1 | T01 | EP | Y | IT |

### 11.17.12.5 Test cases: non-functional (parameterized form)

**Common for TC-V12-P-816…826:** Pre: PP-01/PP-06 staging with production-like data volume (10,000 mandates, 1 million decisions). Steps: run the tool named in the row. Expected as stated.

| ID | Data | Expected | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-V12-P-816 | k6: 200 PDP decisions/s for 15 min | p99 ≤ 50 ms; 0 errors | NFR-002 family; AU-264 | P1 | T03 | EP | Y | SYS |
| TC-V12-P-817 | k6: 50 reservations/s on one mandate | No deadlock; p99 ≤ 120 ms | LED-02 | P1 | T03 | EP | Y | SYS |
| TC-V12-P-818 | Kill switch drill with 20 worker pods | All acknowledge ≤ 60 s | MC-09 | P0 | T21 | EP | Y | SYS |
| TC-V12-P-819 | axe-core on A260–A269 | 0 serious/critical violations | WCAG 2.2 AA | P1 | T08 | EP | Y | E2E |
| TC-V12-P-820 | NVDA + Chrome on A262 approve flow | Digest, exposure and approve button announced; focus order logical | WCAG 2.2 AA | P1 | T08 | EXP | N (AT pass) | SYS-M |
| TC-V12-P-821 | hi-IN and de-DE locales on A261/A262 | Money formatted per locale (₹1,00,000.00 / 50.000,00 €); no truncation | DEC-776 | P2 | T13 | EP | Y | E2E |
| TC-V12-P-822 | Restore drill: PITR to T−10 min with in-flight reservations | Ledger consistent; Held reservations reconciled; RPO ≤ 15 min | DEC-787 | P0 | T21 | ST | Y | SYS |
| TC-V12-P-823 | Region failover drill (standby) during MT-PAY window | Kill switch auto-engaged for money types during failover; RTO ≤ 120 min | DEC-771 | P0 | T21 | ST | Y | SYS |
| TC-V12-P-824 | Two-tenant RLS fixture on all Group P tables | 0 cross-tenant rows; `app_rw` only | DEC-778 | P0 | T15 | EP | Y | IT |
| TC-V12-P-825 | SAST/secret scan on adapters | 0 secrets; no `service_role` usage | DEC-778 | P0 | T07 | EP | Y | CT |
| TC-V12-P-826 | Chaos: KMS unavailable 10 min | No approvals and no dispatch (fail closed); recovery automatic | AU-260 | P0 | T21 | EG | Y | SYS |
