### 2.6.5.8 Part 6 enhancements: test cases, UAT packs and acceptance procedures

**Legend.** P = priority (P0 blocks release, P1 high, P2 normal). Type: FUN functional, NEG negative, SEC security/isolation, EDG edge/boundary, CON concurrency, A11Y accessibility, UAT business acceptance. Tech: EP equivalence partitioning, BVA boundary value, ST state transition, DT decision table, UC use case, RACE race condition. Lvl: UT unit, SYS system, SIT system integration, UAT. Fixtures: GSE-SYN two-tenant data (Part 6.1) plus the group A fixtures FX-A-01…06 below. No real outreach, payment or publication is used (SP-03 §Additional responsibilities).

#### 2.6.5.8.1 Group A fixtures

| Fixture | Content | Source |
|---|---|---|
| FX-A-01 | Persona accounts: one per P01–P20 and variant, each with separate tenant/startup grants in tenants T-OWN (owner portfolio) and T-NOVA (external, "Nova Industrial (demo)"); plus T-ACME second external tenant | SP-03 §Persona journey table |
| FX-A-02 | OrganicSpec RamVan offering *Approved and Available* (synthetic only), price list PL-7 at INR 500.00 per unit, Green Valley Distributor (demo) organization, website enquiry E-001 and research signal S-91 for the same organization | SP-37 §02 |
| FX-A-03 | Quote 100 units × INR 500.00 = INR 50,000.00 pre-tax; invoice basis variants: (a) INR 50,000.00 total, (b) INR 59,000.00 with 18% GST; receipts INR 50,000.00 | SP-37 §03 |
| FX-A-04 | Budget: approved demo cap INR 500.00; committed/actual INR 420.00; proposed charges INR 100.00 and INR 50.00 | SP-37 §06 Budget fixture |
| FX-A-05 | Five synthetic documents: D1, D2, D3 permitted and fresh (one professional contact each), D4 from a restricted source, D5 permitted but 120 days old with TTL 90 | SP-11 §Coverage and examples |
| FX-A-06 | Relationship ledger events E-001…E-007 for REL-COM-001 with fixed source event IDs | SP-37 §07 |

#### 2.6.5.8.2 Persona journey acceptance pack PJ-01…09 (SP-03)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-ENH-A-001 | PJ-01 Commercial employee: full journey and foreign-startup denial | SP-03 §Implementation controls; AP-02; ABAC-01 | FX-A-01 R03 of OrganicSpec; FX-A-02 | Select OrganicSpec; qualify Green Valley; draft approved outreach; submit; record follow-up; then call GET on a MedMaarg deal ID and on `/investor` route | Business records created in OrganicSpec only; MedMaarg request 404 (not 403, no existence leak); investor audience token rejected 401 (DEC-058) | P0 | SEC | UC | Y | SYS |
| TC-ENH-A-002 | PJ-02 Marketing manager: unapproved claim and suppressed recipient | BRL-MKT-01; BRL-ELG | R05 of MedMaarg; claim CL-9 unapproved; contact on suppression list | Draft post using CL-9; submit; then build audience containing suppressed contact and simulate | Submit blocked BRL-MKT-01; simulation excludes contact with rule ID | P0 | NEG | DT | Y | SYS |
| TC-ENH-A-003 | PJ-03 Bid/procurement operator: expired bid and unauthorized price change | FR-DM-02; BRL-QTE | R06 AppNAI tender deadline 2030-06-01 09:00 UTC; clock at deadline; R07 quote on approved PL-7 | Attempt submission record; R07 edits unit price to INR 450.00 without approval | Submission rejected and exception created; price change makes quote "Pending approval", cannot be delivered | P0 | NEG | BVA | Y | SYS |
| TC-ENH-A-004 | PJ-04 Education counsellor: guardian path and external AI project reroute | DEC-030; FR-DM-04; P03b | R03 of EduVerse; enquiry from learner aged 16 without guardian; enquiry "build us an AI chatbot" | Process both enquiries | Minor: no direct outreach, institution/guardian route task; AI build request routed to AppNAI intake, not EduVerse pipeline | P0 | NEG | DT | Y | SYS |
| TC-ENH-A-005 | PJ-05 Healthcare partnerships manager: clinical data rejected | BRL-ELG-14; P03a; SPB-14 | R03 of MedMaarg; note text containing a patient diagnosis | Save note on hospital opportunity | 422 sensitive-data detector; note not stored; incident counter incremented | P0 | NEG | EP | Y | SYS |
| TC-ENH-A-006 | PJ-06 External customer/supplier: foreign grant and expired invite | FR-W24; R16 | Portal user of T-OWN/OrganicSpec; invite expired CLK-0 − 1 h; object grant for another customer's quote | Open expired invite; GET foreign quote | Invite rejected with re-request path; foreign quote 404; no Admin route reachable | P0 | SEC | EP | Y | SYS |
| TC-ENH-A-007 | PJ-07 Relationship user denied SaaS billing | SP-03 §Personas and journeys; BRL-SVC | R16 portal user | Request W34 and `~/portal/service/invoices` | 403/404; W34 navigation absent | P0 | SEC | EP | Y | SYS |
| TC-ENH-A-008 | PJ-08 Tenant admin and support with limited grant | DEC-056; AP-10 | R12 of T-NOVA; R13 with approved 4 h read-only grant for Outreach module | R13 opens Outreach list, then Closure, then T-ACME | Outreach readable; Closure denied; T-ACME denied; all accesses audited; grant expiry ends access | P0 | SEC | ST | Y | SYS |
| TC-ENH-A-009 | PJ-09 Client admin revokes support and exports own data; finance cannot bypass second approver | SP-03 §Role-specific acceptance; BRL-APR | R12 of T-NOVA; R08 maker on a payment | Client revokes R13 grant; exports contacts; R08 tries to also act as checker | Grant revoked immediately; export contains T-NOVA only; checker action 403 | P0 | SEC | UC | Y | SYS |

#### 2.6.5.8.3 Research, playbooks, scoring and benchmark tests

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-ENH-A-010 | Five-document synthetic proof and paid-provider gate | SP-11 §Coverage and examples; FR-ENH-A-006; BRL-ENH-A-03 | FX-A-05 | Run discovery over D1–D5; then request activation of paid provider PRV-X with no benchmark | Exactly 3 professional contacts from D1–D3; none from D4 (blocked, logged) or D5 (stale); activation blocked | P0 | FUN | EP | Y | SIT |
| TC-ENH-A-011 | Visitors cannot enumerate research candidates | A11-35; FR-ENH-A-004 | Public client, no session | Probe public API, sitemap, search and error messages for organization or score data | No research record, score, source URL or contact appears; 404 for internal IDs | P0 | SEC | EP | Y | SYS |
| TC-ENH-A-012 | Discovery benchmark report with interval and gate | FR-ENH-A-005; BRL-ENH-A-04 | 50 labelled records, 30 proposed, 26 correct, 34 known eligible | Generate report | Precision 0.867 (0.703–0.947), recall 0.765, n shown; family remains Pilot | P1 | FUN | BVA | Y | SYS |
| TC-ENH-A-013 | Partnership-fit score computation and review defaults | FR-ENH-A-007; CONFLICT-300 | Components per US-06-EA01 | Compute score | 73; coverage 65 → research/nurture | P1 | FUN | DT | Y | UT |
| TC-ENH-A-014 | Alternative scoring version activation needs benchmark | BRL-ENH-A-01 | Version PF-1 without benchmark; then with benchmark precision 0.84 vs default 0.86 | Activate twice | Both blocked (missing; lower precision) | P1 | NEG | DT | Y | SYS |
| TC-ENH-A-015 | Launch checklist and coverage counters | FR-ENH-A-001, 004 | SPB-05 incomplete; SPB-04 run with 12 items, 2 blocked, 1 stale | Schedule SPB-05; run SPB-04 | SPB-05 422; ledger attempted 12, succeeded 9, blocked 2, stale 1 | P0 | FUN | EP | Y | SYS |
| TC-ENH-A-016 | Geography triple filtering | FR-ENH-A-002 | Opportunity: counterparty UK, client UK, delivery Odisha | Filter delivery region = Odisha; client geography = India | Appears in first filter only | P2 | FUN | EP | Y | SYS |
| TC-ENH-A-017 | Coverage planner excludes prohibited families and explains ranking | FR-ENH-A-003 | AOP-02; SPB-05 manual-only | Generate suggestions | Factors shown; no SPB-05 automated suggestion | P1 | NEG | EP | Y | SYS |

#### 2.6.5.8.4 Channel, experiment and publication tests

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-ENH-A-018 | Recording requires permission; MedMaarg never recorded | BRL-ENH-A-05 | Meeting without permission; MedMaarg demo | Try Record / Transcribe | Actions disabled with reason; API 422 | P1 | NEG | DT | Y | SYS |
| TC-ENH-A-019 | Reply taxonomy effects including decline and meeting request | FR-ENH-A-008; CONFLICT-303 | Sequence SEQ-4; 11 reply fixtures (one per class) | Ingest replies | Effects exactly as §2.6.5.2.6; unknown pauses | P0 | FUN | DT | Y | SIT |
| TC-ENH-A-020 | Spend-cap race | SP-12 §Acquisition mechanism; FR-ENH-A-011 | Cap with INR 80.00 available; two workers request INR 50.00 concurrently (100 repetitions) | Run concurrently | Exactly one reservation per repetition; the other held BUDGET_EXHAUSTED; never overspent | P0 | CON | RACE | Y | SYS |
| TC-ENH-A-021 | Opt-out race: queue before lease | SP-12 §Opt-out race; Part 2.2 §2.6.1 | Step queued 10:00:00; opt-out 10:00:05; lease 10:00:09 | Process | Zero provider calls; one suppressed outcome; audit; reservation released | P0 | CON | RACE | Y | SYS |
| TC-ENH-A-022 | Social publication uncertain then reconciled | FR-ENH-A-009; DEC-050 | Provider simulator: timeout after accept | Publish; reconcile | State uncertain → reconciled_confirmed with external post ID; no duplicate post | P1 | EDG | ST | Y | SIT |
| TC-ENH-A-023 | Experiment overlap blocked; stop trigger pauses arm | FR-ENH-A-011; BRL-ENH-A-13 | EXP-7 running; EXP-8 overlapping; complaint rate fixture | Create EXP-8; inject complaints | EXP-8 blocked; arm B paused; NT-ENH-A-01 sent | P1 | FUN | DT | Y | SYS |
| TC-ENH-A-028 | Website publisher SoD for sensitive claims | BRL-ENH-A-09 | R05L authored page with price claim | Publish | 403; different publisher succeeds | P0 | SEC | DT | Y | SYS |
| TC-ENH-A-033 | Legal disclosure incomplete blocks publication | FR-ENH-A-017 | OrganicSpec en-IN disclosure missing grievance contact | Publish | Blocked; after completion and R10 approval, publish succeeds and footer shows fields | P0 | NEG | EP | Y | SYS |

#### 2.6.5.8.5 Roles, delegation, governance and finance tests

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-ENH-A-024 | R21 without active grant denied | ABAC-ENH-A-01 | Operator O-1 R21; no grant for T-NOVA | Switch into T-NOVA | 403 DELEGATION_SCOPE; audit | P0 | SEC | EP | Y | SYS |
| TC-ENH-A-025 | R21 outside module or sender scope denied | ABAC-ENH-A-01, 02 | Grant G-1 (Discovery, Outreach; S-NOVA-1) | Open Closure; dispatch from S-OWNER-1 | Both denied | P0 | SEC | DT | Y | SYS |
| TC-ENH-A-026 | Grant revocation terminates session; one tenant per session | ABAC-ENH-A-03 | G-1 and G-2 for O-1 | Revoke G-1 during session; try cross-tenant search | Session ended ≤ 60 s; queued steps held; search returns current tenant only | P0 | SEC | ST | Y | SYS |
| TC-ENH-A-027 | R12I sees metadata only; paid adapter needs approval | R12I; NFR-037 | SES adapter with traffic; paid search adapter | Open adapter; enable paid adapter | No message content; approval request created; adapter disabled | P1 | SEC | EP | Y | SYS |
| TC-ENH-A-029 | Template reviewer cannot approve own template; published immutable | BRL-ENH-A-11 | TPL-3 v4 authored by T-1 | T-1 approves; edit v4 after another reviewer approves | 403; edit creates v5 | P0 | SEC | ST | Y | SYS |
| TC-ENH-A-030 | Jurisdiction activation gating | FR-ENH-A-014 | No Germany record; then approved record | Dispatch to German contact twice | First denied JURISDICTION_NOT_ACTIVATED; second passes PDP | P0 | NEG | ST | Y | SYS |
| TC-ENH-A-031 | Cross-entity allocation blocked | BRL-ENH-A-07 | RC-1 OrganicSpec INR 50,000.00; INV-77 MedMaarg | Allocate | 422; finance exception | P0 | NEG | EP | Y | SYS |
| TC-ENH-A-032 | No renewal after cancellation or suppression | BRL-ENH-A-12 | CT-5 Cancelled; contact suppressed; customer-initiated W28 request | Run scheduler; submit W28 | No case for scheduler; case for customer request | P1 | NEG | DT | Y | SYS |
| TC-ENH-A-040 | Training record never grants; productivity EVR | BRL-ENH-A-10; §2.6.5.1.4 | U-5 trained, no role; P04 study session | Call send API; complete study | 403; EVR with median/p90 time and error count | P1 | SEC | EP | Y | SYS |
| TC-ENH-A-043 | Bulk preview hash mismatch; startup name is never permission | FR-ENH-A-019; SP-37 §Activation controls | 120 selected; 3 opt-outs before confirm; request with `startup_name=AppNAI` but grant for OrganicSpec | Confirm bulk; call API by name | 409 PREVIEW_STALE; name-based request ignored, scope from grant only | P0 | SEC | EP | Y | SYS |

#### 2.6.5.8.6 Worked-example UAT packs (SP-37) [RECOMMENDATION-310]

| ID | Title | Links | Preconditions · Test data | Steps (screen hops) | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-ENH-A-041 | UAT-A-01 Discovery to engagement (OrganicSpec RamVan) | SP-37 §02 | FX-A-02 | A003–A006/A099–A100 configure → W04–W05/W12–W14 enquiry E-001 + signal S-91 (A015–A019) → A020–A032 qualify and assign → A033–A039/A044–A047 approved sequence → A037/A040/A045–A046/A069 inbound reply and demo | One organization after dedupe with two evidence links; one relationship REL-COM-001; dispatch only after consent, policy and budget pass; reply pauses competing follow-up | P0 | UAT | UC | N | UAT |
| TC-ENH-A-042 | UAT-A-02 Conversion to verified outcome (100 × INR 500) | SP-37 §03; DEC-054 | FX-A-03 | W23/A065–A066 proposal → A067–A068 quote → W24/A069–A072 negotiation and contract → W25–W26/A073–A074/A105 order and payment → W27/A075–A078 onboarding → W28/A079–A083 retention | Quote INR 50,000.00 pre-tax; basis (a) receipt INR 50,000.00 → outstanding INR 0.00; basis (b) receipt INR 50,000.00 → outstanding INR 9,000.00 shown as exception, no forced match; quoted, contracted, invoiced, received shown separately | P0 | UAT | UC | N | UAT |
| TC-ENH-A-034 | UAT-A-03 AppNAI variant | SP-37 §04; AOP-01 | Tender fixture | W15 → A015–A029 → A065 → A104 | Bid prepared; approval before submission; human submission evidence (DEC-053) | P1 | UAT | UC | N | UAT |
| TC-ENH-A-035 | UAT-A-04 MedMaarg variant | SP-37 §04; SPB-14 | Hospital fixture | W13 → A020–A032 → A075–A078 → A091 | Organization verified; no patient data anywhere; pilot tracked | P1 | UAT | UC | N | UAT |
| TC-ENH-A-036 | UAT-A-05 EduVerse variant and single active AOP | SP-37 §04; FR-ENH-A-010 | University MoU fixture; AOP-03 rev 2 and rev 3 | W17 → A031 → A065–A072 → A075; approve AOP rev 3 | MoU flow completes; external AI project request rerouted; only rev 3 active | P1 | UAT | UC | N | UAT |
| TC-ENH-A-037 | UAT-A-06 OrganicSpec variant and WAR pack | SP-37 §04; FR-ENH-A-012 | Supplier procurement fixture; clock Monday 09:00 IST | W04–W05/W16 → A067–A068 → A105; WAR pack generation | PO and payable separate from receivable; WAR pack with seven sections | P1 | UAT | UC | N | UAT |
| TC-ENH-A-038 | UAT-A-07 New independent client variant | SP-37 §04–05 | T-NOVA applicant | W31 → W32 → W33 → A099 → A112/A113 → W34/A101 → A112/A103 | No self-provisioning; unapproved actions disabled; usage and billing in W34; export limited to T-NOVA; T-OWN invisible | P0 | UAT | UC | N | UAT |
| TC-ENH-A-039 | Outcome economics and experiment scorecard | FR-ENH-A-011, 013; BRL-ENH-A-14 | Cohort costs INR 12,400.00; 4 closures; December 0 closures | Open RP-ENH-A-02 and RP-ENH-A-04 | INR 3,100.00 per outcome; December "Not assessed"; scorecard intervals and trigger log | P1 | FUN | BVA | Y | SYS |
| TC-ENH-A-044 | UAT-A-08 Twenty concurrent simulated runs and hold records | SP-37 §06; FR-ENH-A-020 | 20 runs across 2 startups; one stale evidence; one opt-out | Start all; observe A110/A111 | Separate run IDs, queues, reservations; fairness limits respected; 2 hold records with rule IDs, revision and run ID; no live side effects (simulation) | P1 | CON | UC | Y | SYS |
| TC-ENH-A-045 | Budget fixture: INR 100 charge held | SP-37 §06; FX-A-04 | Cap 500.00; committed 420.00 | Request reservation 100.00 | Available 80.00 → hold BUDGET_EXHAUSTED; reviewer notified; state preserved; no provider fallback | P0 | EDG | BVA | Y | SYS |
| TC-ENH-A-046 | Budget fixture: INR 50 reserves only after eligibility; unknown result is not retry authority | SP-37 §06; DEC-050 | FX-A-04; first with contact ineligible, then eligible; provider returns timeout | Request 50.00 twice; simulate timeout | Ineligible: no reservation; eligible: reservation 50.00 (available 30.00); timeout → uncertain, no retry until reconciled | P0 | EDG | ST | Y | SYS |
| TC-ENH-A-047 | Relationship stage projection | FR-ENH-A-016 | FX-A-06 events in order | Apply E-001…E-007 | Stages New, Qualified, Engaged, Quote requested, Negotiation, Contracted, Paid in order; direct write rejected | P1 | FUN | ST | Y | SYS |
| TC-ENH-A-048 | Replay E-004 and operator takeover | SP-37 §07 Replay | FX-A-06 after E-004 | Replay E-004 with identical event ID; operator takes over | No second task, message or side effect; monitor shows duplicate hold; communication branch paused until authorized resume | P0 | CON | RACE | Y | SYS |
| TC-ENH-A-049 | DEMO-A-01…04 | SP-37 §08 | FX-A-01…06 | (1) onboard new business; (2) one complete journey; (3) two channels with opt-out; (4) replay event and uncertain result | (1) new tenant visible only to its users, registry ID retained; (2) one relationship ID links discovery, conversation, document and outcome; (3) same timeline and consent check, opt-out blocks later send; (4) dedupe and reconciliation with reviewer decision | P0 | UAT | UC | N | UAT |
| TC-ENH-A-050 | DEMO-A-05…08 | SP-37 §08 | FX-A-01…06 | (5) configuration change; (6) financial/legal closure; (7) scope switch and reload; (8) release handoff | (5) new approved revision, active run unchanged, rollback request recorded; (6) no verified outcome without matching evidence, negative fails safely; (7) authorized views, denied route, no secrets in public projection; (8) EVR with expected/actual, defect, retest and sign-off | P0 | UAT | UC | N | UAT |

#### 2.6.5.8.7 Acceptance procedure register extension AP-ENH-A-01…12 [RECOMMENDATION-313]

Extends AP-01…AP-10 (DEC-014). Each procedure is a named bundle of tests with an accountable signer (§2.6.5.1.3).

| AP | Procedure (source) | Verification | Acceptance | Accountable | Tests |
|---|---|---|---|---|---|
| AP-ENH-A-01 | Source permission and provenance (SP-11) | Synthetic public record has permission, URL, retrieval time and evidence hash | Every accepted record linked to permitted evidence and source policy | Data quality lead | TC-ENH-A-010, 015; Part 6 provenance TCs |
| AP-ENH-A-02 | Evidence freshness (SP-11, SP-14) | Age a source beyond TTL, then change content | Stale marked or refreshed; never used for a consequential decision | Data quality lead | TC-ENH-A-010, US-18-EA02 |
| AP-ENH-A-03 | Deduplication and entity resolution (SP-11) | Duplicate organization/contact with different aliases | One canonical scoped record with lineage; uncertain match reviewed | Data quality lead | TC-ENH-A-041; BRL-SRC-08 TCs |
| AP-ENH-A-04 | Classification quality (SP-11) | Labelled representative corpus; precision/recall with sample size | Precision ≥ 90% target (DEC-001 gate); recall disclosed; no claim from five synthetic documents | Data quality lead | TC-ENH-A-012 |
| AP-ENH-A-05 | Source inventory completeness (SP-11, SP-14) | Compare source families and permission policy to approved coverage; verify the preserved 15-sheet commercial source inventory when supplied (GAP-300) | All original source records retained; coverage measured, not claimed exhaustive | Data quality lead | Pending artefact |
| AP-ENH-A-06 | Follow-up stop conditions (SP-12) | Reply, opt-out, pause or policy revision before dispatch | All ineligible actions cancelled or held; no message | Automation architect | TC-ENH-A-019, 021 |
| AP-ENH-A-07 | Communication eligibility (SP-12) | Opt-out, unauthorized channel, expired permission, approved reply | No prohibited dispatch; decision logged | Privacy and compliance lead | TC-ENH-A-021, 030 |
| AP-ENH-A-08 | Public offer and claims restrictions (SP-12, SP-13) | Publish unapproved formal offer or unsupported clinical/education/commercial claim | Blocked; no unverified guarantee | Privacy and compliance lead | TC-ENH-A-002, 028 |
| AP-ENH-A-09 | Idempotency and duplicate delivery (SP-13) | Concurrent identical replay; same key with changed payload | One effect; changed payload rejected; uncertain reconciled | Reliability engineer | TC-ENH-A-048 |
| AP-ENH-A-10 | Outcome economics (SP-14) | Cost per qualified opportunity and verified closure for matching cohort, time, currency | Comparable baseline/candidate; zero denominator not assessed | Business conversion lead | TC-ENH-A-039 |
| AP-ENH-A-11 | Cross-border and regional decision (SP-14) | Record jurisdiction, source, communications, privacy, commercial route | Specialist sign-off before regulated activation | Privacy and compliance lead | TC-ENH-A-030 |
| AP-ENH-A-12 | User productivity (SP-03) | Timed representative tasks with sample users | Baseline/candidate time and error rate measured; no reduced safeguards | UX lead | TC-ENH-A-040 |

**Test count added by this part:** 50 test cases (TC-ENH-A-001…050), of which 27 are P0, 21 automated at SYS/SIT/UT level, 12 UAT. Traceability: every FR-ENH-A and BRL-ENH-A item maps to at least one TC (FR table §2.6.5.2.1 and the rules' "Tests" are listed in the stories).
