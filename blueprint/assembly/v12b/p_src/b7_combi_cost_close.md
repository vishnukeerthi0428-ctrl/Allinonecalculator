
## 11.17.14 Combinatorial models and the generated test catalogue

### 11.17.14.1 Method

| Item | Specification |
|---|---|
| Generator | `assembly/v12b/p_combinatorial.py` (Python 3, standard library only; deterministic seeds 840/841/842/845/850). Run: `python3 -I assembly/v12b/p_combinatorial.py assembly/v12b/p_frag2` |
| Algorithm | Greedy t-way covering array (IPOG-style row construction: each new row is seeded from an uncovered t-tuple and filled value by value to maximise newly covered t-tuples; 60 candidate rows per step), with constraint handling (forbidden partial assignments are neither required nor generated) |
| Verification | Independent `verify()` recomputes every t-tuple of every model and checks it occurs in at least one row: **0 missing 3-tuples** for models M, C, B and the constrained positive model of C; **0 missing pairs** for the pairwise story Examples |
| Oracle | Expected results are computed by executable oracles that implement the binding rule orders: `oracle_m` = PDP rules 0–14 (§11.17.5.12); `oracle_c` = commerce/payment order (§11.17.6.4–6.5); `oracle_b` = submission mode and guard (§11.17.7); `oracle_k` = kill-switch phase rules (§11.17.5.13). The same oracles are imported by the automated tests (one source of truth) |
| Masking problem and the three layers | A plain 3-way array is dominated by early gates (kill switch, L0, unapproved packs), which **mask** deep paths: in model M the plain array produced 0 ALLOW rows. Each model is therefore covered by three layers: **L1** full 3-way over all values (tests precedence when several faults coincide); **L2** the positive (gate-passing) sub-space, exhaustive when ≤ 64 combinations, otherwise 3-way under constraints; **L3** single-fault rows: every fault value once per positive value of a context parameter, with all other parameters positive (tests each deep rule in isolation) |
| Exhaustive models | Kill switch scope × phase × actor = 8 × 4 × 2 = 64 → exhaustive (V12B rule "≤ 64") |
| Stories | Pairwise arrays of the same models are emitted as Gherkin `Examples:` rows (US-18-ZP03, US-24-ZP04, US-14-ZP02) |

### 11.17.14.2 Parameter models

**Model M: mandated dispatch (PDP).**

| Parameter | Values | Positive values |
|---|---|---|
| AUT autonomy level | L0, L1, L2, L3, L4 | L3, L4 |
| MST mandate state | Draft, PendingSecondApproval, Active, Suspended, Expired, Revoked, Exhausted | Active |
| VAL value vs cap | BelowCap, AtCap, AbovePerActionCap, CrossesAggregateCap | BelowCap, AtCap |
| CPT counterparty trust | AllowlistedVerified, CredentialExpired, NotAllowlisted, CounterpartyRevoked | AllowlistedVerified |
| JUR jurisdiction pack | IN-Approved, EU-Approved, Pack-Draft, Pack-Missing | IN-Approved, EU-Approved |
| PAY payment method | UPI-AutoPay, e-NACH, Card-MIT-Token, SEPA-DD, No-Payment | all (constraint: UPI/e-NACH only IN; SEPA only EU) |
| WIN time window | Inside, BeforeStart, AfterEnd, OutsideDailyHours | Inside |
| KS kill switch | Off, Mandate, Tenant, Platform | Off |

**Model C: agentic commerce and payment.**

| Parameter | Values | Positive values |
|---|---|---|
| VC counterparty credential | Valid, Expired, StatusRevoked, SignatureInvalid, IssuerNotTrusted | Valid |
| OFFER counterparty offer vs bounds | WithinBounds, AtFloor, BeyondBounds, ForbiddenTerm | WithinBounds, AtFloor |
| ROUND negotiation round | UnderMaxRounds, MaxRoundsReached | both |
| AMT amount vs caps | BelowTxnCap, AtTxnCap, AboveTxnCap, PeriodCapExceeded | BelowTxnCap, AtTxnCap |
| PMT payment method | UPI-AutoPay, e-NACH, Card-MIT, SEPA-DD, NetworkAgentToken | all (constraint by jurisdiction) |
| AUTH customer authentication | ExemptOrPreAuthorised, AFA-SCA-Completed, AFA-SCA-Missing | first two |
| PSP response | Success, Pending, Declined, Timeout | all |
| JUR jurisdiction | IN, EU, PackNotApproved | IN, EU |

**Model B: automatic bid submission.**

| Parameter | Values | Positive values |
|---|---|---|
| AUT level | L1, L2, L3 | L3 |
| MST MT-BID state | Active, PendingSecondApproval, Revoked, Expired | Active |
| HASH package vs approval | Match, PackageChanged, ApprovalMissing | Match |
| PORTAL capability | API-Permitted, Automation-Permitted, AssistedOnly, ManualOnly | first two |
| DEADLINE position | BeforeBuffer, InsideBuffer, AfterDeadline | BeforeBuffer |
| SIGN signing rule | OrgSignerAvailable, HumanDSCOnly, NotRequired | OrgSignerAvailable, NotRequired |
| RECEIPT portal outcome | ReceiptOK, TimeoutUnknown, RejectedValidation | all |
| KS kill switch | Off, On | Off |
| JUR procurement pack | PackApproved, PackNotApproved | PackApproved |

**Model K: kill switch.** SCOPE (Platform, Tenant, Company, Agent, Mandate, Counterparty, Portal, PaymentMethod) × PHASE (NotStarted, Reserved, DispatchedAwaitingProvider, CompletedUnreconciled) × ACTOR (R01, R10).

### 11.17.14.3 Counts

| Model | Parameters (domain sizes) | Full space | t-tuples to cover | L1 3-way rows | L2 positive rows | L3 single-fault rows | Pairwise story rows (pairs) | TC range |
|---|---|---|---|---|---|---|---|---|
| M | 8 (5,7,4,4,4,5,4,4) | 179,200 | 5,435 triples | 231 | 28 (exhaustive, all ALLOW) | 41 | 39 (595) | TC-V12-P-001…300 |
| C | 8 (5,4,2,4,5,3,4,3) | 28,800 | 2,868 triples | 137 | 46 (3-way of 448 valid positive combinations) | 40 | 30 (390) | TC-V12-P-301…523 |
| B | 9 (3,4,3,4,3,3,3,2,2) | 15,552 | 2,226 triples | 75 | 12 (exhaustive) | 42 | 20 (322) | TC-V12-P-524…652 |
| K | 3 (8,4,2) | 64 | — | — | — | — | — | TC-V12-P-653…716 (exhaustive 64) |
| **Total generated** | | | | **443** | **86** | **123** | **89 Examples rows** | **716 test cases** |

**Verdict distribution (shows deep paths are reached).** M-L1: BLOCKED 116, RECORD_ONLY 53, HOLD 31, DENY 30, ROUTE 1; M-L2: ALLOW 28; M-L3: HOLD 15, DENY 12, BLOCKED 6, ROUTE 5, DEFER 2, RECORD_ONLY 1. C-L1: DENY 87, HOLD 40, ESCALATE 5, COUNTER 2, AWAIT 1, FAILED 1, RECONCILING 1; C-L2: CAPTURED 14, AWAIT 11, RECONCILING 11, FAILED 10; C-L3: DENY 16, HOLD 12, ESCALATE 11, COUNTER 1. B-L1: EXPIRED 20, HOLD 19, BLOCKED 18, MANUAL 9, ASSISTED 8, DENY 1; B-L2: SUBMITTED 4, RECONCILING 4, FAILED 4; B-L3: ASSISTED 12, HOLD 9, MANUAL 6, DENY 6, ESCALATE 3, EXPIRED 3, BLOCKED 3. K: BLOCKED 32, RECONCILING 16, RECONCILE 16.

### 11.17.14.4 Generated test cases (parameterized form, Part 6.2a)

**Common for TC-V12-P-001…300 (model M):** Pre: PP-P1; the row's values are applied as fixture state (mandate MND-41 state and windows, counterparty registry, synthetic pack states, payment method on the intent, kill-switch flags); VAL is realised as: BelowCap ₹10,000.00, AtCap ₹50,000.00, AbovePerActionCap ₹50,000.01, CrossesAggregateCap ₹20,000.00 with ₹1,85,000.00 already committed. Steps: call `POST /api/v2/internal/mandates/decide` as R19; then, for ALLOW, run the adapter with the returned fence and read the ledger. Expected: verdict and reason exactly as listed (oracle `oracle_m`); for non-ALLOW verdicts NSE; audit row `mandate.decision` with the rule number.

**L1: 3-way over all values (precedence)**

<!--INCLUDE:p_frag2/M_L1_3way.md-->

**L2: positive sub-space (exhaustive)**

<!--INCLUDE:p_frag2/M_L2_positive.md-->

**L3: single-fault rows**

<!--INCLUDE:p_frag2/M_L3_singlefault.md-->

**Common for TC-V12-P-301…523 (model C):** Pre: PP-P2; the row's values configure the counterparty credential stub, the counterparty's offer relative to MND-60 bounds (WithinBounds ₹3,800.00; AtFloor ₹3,520.00; BeyondBounds ₹3,400.00; ForbiddenTerm "unlimited liability"), round counter, payment amount vs MT-PAY caps (Below ₹10,000.00; At ₹50,000.00; Above ₹50,000.01; PeriodCapExceeded with aggregate used), method, authentication state at the PSP simulator, PSP simulator mode and jurisdiction pack. Steps: inject the signed counterparty message; let WF-59 run to the payment step. Expected: outcome and reason exactly as listed (oracle `oracle_c`); PSP call count as listed; mandate-ledger effect as listed; journals only on CAPTURED (J-02).

**L1: 3-way over all values**

<!--INCLUDE:p_frag2/C_L1_3way.md-->

**L2: positive sub-space (3-way under the jurisdiction × method constraint)**

<!--INCLUDE:p_frag2/C_L2_positive.md-->

**L3: single-fault rows**

<!--INCLUDE:p_frag2/C_L3_singlefault.md-->

**Common for TC-V12-P-524…652 (model B):** Pre: PP-P3; the row's values configure the run level, the MT-BID state, whether the sealed package hash equals the approved hash (PackageChanged = one file replaced after approval; ApprovalMissing = no MT-BID), the portal profile capability and signing rule, the clock (BeforeBuffer = deadline − 30 h; InsideBuffer = deadline − 4 h; AfterDeadline = deadline + 1 min), the portal simulator answer, the kill switch and the RP-IN-PROC-syn state. Steps: `POST /api/v2/bids/{id}/submissions`. Expected: outcome and reason exactly as listed (oracle `oracle_b`); portal submit calls as listed; ASSISTED creates an assisted-session task; MANUAL creates a manual-evidence task.

**L1: 3-way over all values**

<!--INCLUDE:p_frag2/B_L1_3way.md-->

**L2: positive sub-space (exhaustive)**

<!--INCLUDE:p_frag2/B_L2_positive.md-->

**L3: single-fault rows**

<!--INCLUDE:p_frag2/B_L3_singlefault.md-->

**Common for TC-V12-P-653…716 (model K, exhaustive):** Pre: PP-P1 with one MT-PAY effect placed in the row's phase; the row's actor engages the switch at the row's scope (scope chosen so that it encloses the effect). Steps: engage; wait 60 s on the virtual clock; read effect, ledger, PSP simulator log and events. Expected as listed.

<!--INCLUDE:p_frag2/K_exhaustive.md-->

## 11.17.15 Effort and cost

All figures are **estimates** for a separately approvable change request **CR-V12-P** under DEC-790 ("all V12 change requests are funded"); they are outside the approved Ledger A (DEC-230) and Ledger B (DEC-231/422) figures and are added to the re-plan in Part 11.20. Rates: ₹4,545 / ₹5,682 / ₹6,818 per person-day (Part 8.4; Part 9.10). Prices, vendor fees and legal fees: **verify at time of implementation (as of 27 Nov 2026)**.

### 11.17.15.1 Development (one-time) — effort

| # | Component | Basis | Low pd | Central pd | High pd |
|---|---|---|---|---|---|
| 1 | Mandate engine core: object, versions, lifecycle, digest/JWS, APIs, eligibility register | 6 tables, 14 endpoints, state machine | 25 | 35 | 50 |
| 2 | Two-person approval, SoD, CoI, step-up integration, delegation rules | AU-261; IdP | 8 | 12 | 18 |
| 3 | PDP rules 0–14, ledger, fence tokens, kill-switch extension, adapter gateway | AU-263/264/265; ADR-241/246 | 20 | 28 | 40 |
| 4 | Anomaly rules AR-01…12, reconciliation RC-P-01…06, evidence packs | AU-267/268 | 15 | 22 | 32 |
| 5 | Screens A260–A264 | 5 screens (Part 2.5 patterns) | 15 | 22 | 30 |
| 6 | Agent identity (DID/VC/JWS), gateway, 4 protocol adapters, interop gate | AU-269/270; ADR-242 | 25 | 38 | 55 |
| 7 | Negotiation bound engine, term library, A265/A266 | AU-271 | 15 | 22 | 30 |
| 8 | PSP adapters (2 India, 2 EU), payment-mandate registration, pre-debit notices, executor, webhooks | AU-272/273/274; ADR-243 | 30 | 45 | 65 |
| 9 | Settlement, CoA-P sub-ledger and journals, refunds, disputes, A267 | AU-274…277; ADR-244 | 20 | 30 | 42 |
| 10 | Bid sealing, deadline guard, portal registry, adapters (PA-ARIBA, PA-COUPA, PA-EMAIL, PA-PEPPOL, assisted framework for GeM/NIC/US), receipts, A268/A269 | AU-278/279; ADR-245 | 30 | 45 | 65 |
| 11 | Agents AG-200…209 | Part 9.7b sizes: S 2/3/5, M 4/6/8, C 6/9/13 (AG-202, 206 = C; 200, 203, 204, 207 = M; others S) | 36 | 54 | 78 |
| 12 | Evaluation datasets DS-P-01…07, RT-P-01…03 (synthetic drafting + double labelling, DEC-420) | ~1,600 items | 10 | 15 | 22 |
| 13 | Test automation: combinatorial harness and oracles, 716 generated + 110 hand-written TCs, AI eval cases, simulators (PSP, portal, DID) | §11.17.12–14 | 25 | 38 | 55 |
| 14 | Security: threat model upkeep, internal security testing, fixes | §11.17.10 | 8 | 12 | 18 |
| 15 | Rule-pack engineering support (synthetic packs, YAML, AU-128 keys) | §11.17.5.15 | 5 | 8 | 12 |
| 16 | Runbooks, drills, documentation | Kill switch, PSP outage, portal outage | 6 | 9 | 13 |
| | **Total** | | **293** | **435** | **625** |
| | **Development labour cost** | pd × rate | **₹13.3 L** (293 × ₹4,545) | **₹24.7 L** (435 × ₹5,682) | **₹42.6 L** (625 × ₹6,818) |

Story-point view (§11.17.11): 22 stories, 130–210 SP, central ≈ 119 pd. The bottom-up component total (435 pd central) is higher because adapters per PSP, portal and protocol, simulators, datasets and drills become enabler stories at backlog refinement (Part 5 rule: ≤ 13 SP per story) [ASSUMPTION-1057]. The component estimate governs the budget.

### 11.17.15.2 Development (one-time) — external costs

| Item | Basis | Low | Central | High |
|---|---|---|---|---|
| Counsel: draft review and sign-off of RP-IN-PAY, RP-EU-PAY, RP-GL-AGENTCOM, RP-IN-AGENTCOM, RP-EU-AGENTCOM, RP-IN-PROC, RP-EU-PROC, RP-US-PROC | 8 packs (Part 11.15 format) | ₹6.0 L | ₹12.0 L | ₹20.0 L |
| Counsel: portal terms reviews (≈ 10 portal families) and framework-agreement template for agent contracting | [GAP-1045], [GAP-1046] | ₹2.0 L | ₹4.0 L | ₹7.0 L |
| External penetration test of agent gateway, PSP webhooks, approval flows | 1 engagement | ₹3.0 L | ₹5.0 L | ₹8.0 L |
| PSP integration certification / go-live reviews | Per PSP (often free; verify) | ₹0 | ₹0.5 L | ₹1.5 L |
| **Total external one-time** | | **₹11.0 L** | **₹21.5 L** | **₹36.5 L** |
| **Total development (labour + external)** | | **₹24.3 L** | **₹46.2 L** | **₹79.1 L** |

### 11.17.15.3 Running (recurring) costs per month

| Item | Basis | Low | Central | High |
|---|---|---|---|---|
| AI agents AG-200…209 incl. 25% overhead | §11.17.8.1 (₹219 / 731 / 2,192 × 1.25) | ₹274 | ₹914 | ₹2,740 |
| Additional workers (MND, gateway, PSP/portal executors) — India region | 1–2 small containers (DEC-421 stack) | ₹1,500 | ₹2,500 | ₹4,000 |
| Browser-automation worker pool | On-demand, isolated | ₹500 | ₹1,000 | ₹1,500 |
| KMS asymmetric keys and requests (per region) | 3 keys + requests | ₹300 | ₹550 | ₹800 |
| Evidence storage with object lock | S3 | ₹200 | ₹600 | ₹1,000 |
| DID/status-list hosting | Static on verified domain | ₹0 | ₹250 | ₹500 |
| Sanctions / restricted-party screening service | Provider or PSP add-on (verify) | ₹5,000 | ₹15,000 | ₹25,000 |
| Organisational signing certificate (where a portal permits) | Amortised (verify) | ₹1,000 | ₹2,500 | ₹4,000 |
| Counsel retainer for quarterly pack review (Part 11.15 §11.15.3.5) for the 8 new packs | Retainer (verify) | ₹25,000 | ₹50,000 | ₹75,000 |
| **Total running, India region** | | **₹33,774** | **₹73,314** | **₹1,14,540** |
| EU region increment (workers, KMS, storage) when the first EU tenant activates these capabilities (DEC-772) | Second copy of compute lines | ₹2,500 | ₹4,650 | ₹7,300 |
| PSP transaction, mandate-registration, refund and chargeback fees | **Pass-through to the tenant** (merchant of record); not a platform cost | — | — | — |

The 24×7 on-call (DEC-773) and SLA topology (DEC-774) already cover operations; no extra staffing line is added.

## 11.17.16 Decisions, expert review, tags register and quality gate

### 11.17.16.1 Decisions

DEC-840…850 are recorded in file a §11.17.6.10 and repeated here by title for completeness.

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-840 | Shared mandate engine (MND), per-region | Customer revision V12 (28 Nov 2026), under Founder DEC-779 | ADR-240 |
| DEC-841 | L0–L4 controls matrix binding; DEC-064 cap lifted only under Active eligible mandates in Approved jurisdictions | Founder DEC-779 | Amends DEC-064, BRL-AUT-01, BRL-AI-07 (scoped) |
| DEC-842 | Two-person approval TPA-01…11 | Founder DEC-779 | AU-261 |
| DEC-843 | Cap semantics and hierarchy | Customer revision V12 (28 Nov 2026) | §11.17.5.6 |
| DEC-844 | Fixed PDP rule order 0–14 is the oracle | Customer revision V12 (28 Nov 2026) | AU-264 |
| DEC-845 | Kill switch: one engages, two release; extended scopes; fence tokens | Founder DEC-779 | ADR-246 |
| DEC-846 | DID + VC + JWS identity; protocol adapters; interop gate | Founder DEC-780 | ADR-242 |
| DEC-847 | Negotiation numbers only from AU-271 | Founder DEC-780 | Resolves CONFLICT-1047 |
| DEC-848 | Licensed PSPs only; payment-mandate types; no credentials; PSP cap = platform cap | Founder DEC-780 | ADR-243 |
| DEC-849 | CoA-P sub-ledger; automated exact matches; mismatches to maker-checker | Customer revision V12 (28 Nov 2026) | Resolves CONFLICT-1048 |
| DEC-850 | Disputes human-decided; refunds bounded | Founder DEC-780 | AU-275/276 |
| DEC-851 | Bid submission modes AUTO / ASSISTED / MANUAL chosen by the portal capability registry (counsel-reviewed), the RP-xx-PROC pack and the level; AUTO only under an Active single-use MT-BID bound to the package hash; personal DSCs never held by the system | Founder DEC-781 | Amends BRL-BID-04, DEC-053 (scoped); ADR-245 |
| DEC-852 | Deadline guard defaults: B_auto 6 h, B_hard 2 h, planned submit T−48 h, definite-failure retries only, escalation ladder | Customer revision V12 (28 Nov 2026) | Amends BRL-BID-01 for automated attempts; [ASSUMPTION-1053] |
| DEC-853 | Unknown outcomes (PSP, portal, counterparty) are never retried or resubmitted before reconciliation; reservations stay held | Customer revision V12 (28 Nov 2026) | Extends DEC-050 |
| DEC-854 | Anomaly engine is tighten-only; heartbeat loss suspends money mandates | Customer revision V12 (28 Nov 2026) | AU-267; RECOMMENDATION-1049 |
| DEC-855 | Shadow period for the first mandate of each type per tenant | Customer revision V12 (28 Nov 2026) | MC-16; RECOMMENDATION-1050 |
| DEC-856 | Activation per jurisdiction requires the new packs RP-IN-PAY, RP-EU-PAY, RP-GL/IN/EU-AGENTCOM, RP-IN/EU/US-PROC in Part 11.15 format, signed off by counsel; until then the capabilities are built, tested against synthetic packs and inactive | Founder DEC-776, DEC-779…781 | GAP-1044 |
| DEC-857 | CR-V12-P costed as: development ₹24.3 / 46.2 / 79.1 L (labour + external) and running ₹33,774 / 73,314 / 1,14,540 per month (India), + EU increment; added to the Part 11.20 re-plan under DEC-790 | Founder DEC-790 | Separate from DEC-230/231 |

**Architecture decisions.**

| ADR | Decision | Alternatives rejected | Consequences |
|---|---|---|---|
| ADR-240 | Mandate engine as a module in the Django monolith with its own schema and service API; all effects pass its PDP hook | Separate microservice (more ops; DEC-421 stack); per-workflow mandate logic (inconsistent) | + one enforcement point; − module must be highly available (it is in the API tier) |
| ADR-241 | Ledger concurrency by row-locked period counters in PostgreSQL (`app_rw`) | Valkey counters (not durable); optimistic retries only (starvation under burst) | + exact caps; − lock contention measured (TC-V12-P-817) |
| ADR-242 | did:web + W3C VC 2.0 + JWS envelopes; protocol adapters | Proprietary API keys per counterparty (no portable identity); mTLS only (no delegation semantics) | + standards-based; − ecosystem still maturing (verify) |
| ADR-243 | PSP adapter abstraction with per-region PSP registry and licence evidence | Single global PSP (residency and scheme coverage) | + IN/EU coverage; − 4 adapters to maintain |
| ADR-244 | Double-entry commerce sub-ledger feeding existing ledgers | Single-entry payment table (no balance proof) | + auditability; − posting rules to maintain |
| ADR-245 | Portal capability registry + adapter contract + assisted sessions | Universal browser automation (terms risk); manual only (V12 not met) | + lawful automation where allowed; − registry upkeep with counsel |
| ADR-246 | Fence tokens checked at the adapter gateway | Rely on PDP time-of-check only (race) | + closes TOCTOU window; − token plumbing in every adapter |
| ADR-247 | Combinatorial three-layer test design with executable oracles shared by tests | Plain pairwise (masks deep paths) | + deep-path coverage proven; − oracle must be kept equal to rules (CI check: oracle unit tests mirror §11.17.5.12) |

### 11.17.16.2 Expert persona review

| Persona | Question asked | Finding | Resolution in this part |
|---|---|---|---|
| Principal Agent-Safety Architect | Can any agent widen its own authority? | Risk points: L4 plans, amendment flow, counterparty-supplied limits, prompt injection | L4 bound to mandate IDs; loosening only by two-person new version; limits only from our DB; reader steps tool-less; fence tokens |
| Payments Architect | Are scheme rules respected and is money safe? | AFA/SCA, pre-debit notice, MIT eligibility, refund rights differ by scheme and change often | Scheme facts flagged verify and moved into RP-IN-PAY/RP-EU-PAY; three cap layers; PSP-side cap = platform cap; no credentials stored |
| Procurement Specialist | Is automated submission lawful and reliable? | Many government portals need a personal DSC and may prohibit automation; receipts vary | Registry with counsel review per portal; ASSISTED default for GeM/NIC; deadline guard; receipt verification; unknown → no resubmit |
| Fraud and Risk Lead | Where would I attack? | Payee swap, split payments, approver ATO, collusion, floor probing, friendly fraud | FC-01…12, AR-01…12, TPA-09 CoI, step-up, chargeback suspension |
| AI Governance Lead | Are AI roles bounded and evaluable? | Commerce agents face adversarial counterparties | 10 agents with eval thresholds, RT-P corpora, numeric validators, no Tier 2, registry approval (DEC-788) |
| QA Architect | Is coverage proven, not described? | Plain 3-way masked deep paths | Three-layer design with verified covering arrays and shared oracles; 716 generated + 110 hand-written + ~95 AI cases |

### 11.17.16.3 Tags register (Part 11.17 a and b)

| Tag | Type | Statement | Status |
|---|---|---|---|
| ASSUMPTION-1040 | Assumption | Screens A260–A269 are claimed provisionally for Group P (no screen range was allocated; A205–A259 belong to Groups N/O; `SM-SIT-A260…` in Part 3.5a are test IDs). Part 11.20/11.22 consolidation confirms or renumbers | Open |
| ASSUMPTION-1041 | Assumption | Candidate PSPs (India: Razorpay, Cashfree, PayU, Juspay-orchestrated banks; EU: Stripe, Adyen, Mollie) hold the required licences and support the listed mandate schemes; single-currency mandates in this release | Open — verify at onboarding |
| ASSUMPTION-1042 | Assumption | Pilot design volumes for agent calls (§11.17.8.1) | Open — recalibrate after 90 days |
| ASSUMPTION-1043 | Assumption | A2A, AP2, ACP and MCP remain viable; the internal envelope isolates protocol churn | Open — verify versions |
| GAP-1044 | Gap | Part 11.15 has no payment, agentic-contracting or e-procurement packs; RP-IN-PAY, RP-EU-PAY, RP-GL-AGENTCOM, RP-IN-AGENTCOM, RP-EU-AGENTCOM, RP-IN-PROC, RP-EU-PROC, RP-US-PROC must be drafted and signed off before activation (DEC-856) | Open — owner Part 11.15 / counsel |
| GAP-1045 | Gap | Each portal's terms of use must be reviewed by counsel to set its capability; until reviewed, MANUAL_ONLY | Open |
| GAP-1046 | Gap | Contracting framework for agent-to-agent commerce (attribution of agent messages, error correction, liability) and platform-not-a-party terms in the MSA | Open — Legal |
| CONFLICT-1047 | Conflict | DEC-388/395 (AI never proposes or computes a price) vs DEC-780 negotiation | Resolved by DEC-847 (numbers only from the deterministic engine) |
| CONFLICT-1048 | Conflict | BRL-APR-07 Finance maker-checker for every payment verification vs automated mandate reconciliation | Resolved by DEC-849 |
| RECOMMENDATION-1049 | Recommendation | Anomaly engine tighten-only; heartbeat fail-safe | Adopted (DEC-854) |
| RECOMMENDATION-1050 | Recommendation | Shadow period for first mandates per type | Adopted (DEC-855) |
| RECOMMENDATION-1051 | Recommendation | PSP-side mandate maximum equal to the platform per-action cap | Adopted (DEC-848) |
| RECOMMENDATION-1052 | Recommendation | Kill switch one-person engage, two-person release | Adopted (DEC-845) |
| ASSUMPTION-1053 | Assumption | Deadline guard defaults B_auto 6 h, B_hard 2 h, planned T−48 h | Open — tune per portal after pilot |
| ASSUMPTION-1054 | Assumption | Settlement and dispute timelines per scheme as tabled are indicative | Open — verify; final values in RP-IN-PAY/RP-EU-PAY |
| GAP-1055 | Gap | Tenant-level liability caps and crime/cyber insurance covering agent-initiated transactions are not defined | Open — Finance/Legal |
| RECOMMENDATION-1056 | Recommendation | Rules-only anomaly detection first; statistical baselines after 90 days | Adopted |
| ASSUMPTION-1057 | Assumption | Component (bottom-up) estimate governs; story points re-split at refinement | Open |
| GAP-1058 | Gap | No national trust framework for agent business credentials; tenant trust lists + KYB tiers used meanwhile | Open |
| RECOMMENDATION-1059 | Recommendation | Mandate eligibility register is release-controlled configuration, not tenant-editable | Adopted |

### 11.17.16.4 Inconsistencies observed in earlier parts (reported, not edited)

| # | Location | Observation |
|---|---|---|
| 1 | Part 11.7b A172 | Pattern row says "EP-13 · Future (W6+); activation needs a Founder-approved mandate policy"; Part 11.2a assigns SM-SVC-28 to EP-24, and DEC-780 now approves it. Consolidation should align A172 to EP-24 and Release 2 (CR-V12-P) |
| 2 | Part 11.6b AG-104 | Release "Not before Founder decision (CONFLICT-854)"; superseded by DEC-780. Its reader role is taken over by AG-202 for WF-59 |
| 3 | Part 11.2c / 11.3c / 11.4d | DEC-532, 533, 548, 549, 550, 573, 577 remain "Pending Founder decision" in those files; closed by DEC-779…781 (Part 11.14) and detailed here |
| 4 | Part 2.3 BRL-BID-01 | Buffer rule blocks "submission" generally; for human portal submission the system can only record evidence. This part scopes the block to automated attempts (§11.17.4.2) |
| 5 | V12B allocation | Group P has no screen range (see ASSUMPTION-1040) |

### 11.17.16.5 Quality gate: Part 11.17 (a and b)

| # | Item | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | FR-V12-P-001…135 each name a V12 chapter or baseline rule; 64 aspects in `final/coverage_v12/P_coverage.csv` |
| 2 | Assumptions/gaps/conflicts tagged and logged | Pass | 20 tags (1040…1059) in §11.17.16.3 |
| 3 | IDs unique and consistent with earlier parts | Pass with note | Only Group P ranges used; A260–A269 provisional (ASSUMPTION-1040); AG-104 reader superseded, not reused |
| 4 | No story lacks AC; no requirement lacks a test | Pass | 22 stories with Gherkin (3 Scenario Outlines with 89 generated Examples rows); every FR row names a TC; 826 TC-V12-P + ~95 TC-AI |
| 5 | Negative, edge, security, accessibility cases covered | Pass | Single-fault and 3-way fault layers; STRIDE 30 threats, 20 abuse cases; a11y TCs 762, 787, 812, 819, 820 |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | Pass | AG-200…209 cards complete; AU table complete |
| 7 | Time-sensitive facts flagged "verify" with an as-of date | Pass | Scheme limits, protocols, portals, PSPs, prices, legal fees |
| 8 | No restricted data routed to free-tier models | Pass | All agents Tier 2 = No; R3 routing cases TC-AI-AG2nn-R3 |
| 9 | Consistent with earlier parts | Pass with conflicts resolved | Superseded positions listed with Founder authority; amendments stated in §11.17.4.2; inconsistencies reported in §11.17.16.4; no earlier file edited |

**Status: Part 11 Batch 11.17 complete (files a and b). Bounded mandates, agentic commerce and payments, and automatic bid submission specified at full depth with V12's conditions and mandatory controls; 64 of 64 aspects Matched; activation per jurisdiction awaits the eight new counsel-approved rule packs (DEC-856).**
