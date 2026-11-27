# Source-pack review log (for coordinator decisions)

## Group C (docs 06, 17): done
Coverage: 2,302 Covered / 689 Partial / 245 Not covered / 9 Conflict / 35 N/A (3,280 aspects). Files: Part-02-7a (66 pp), Part-02-7b (289 pp; 147 screen contract cards + TC-ENH-C-101…247).
Conflicts: CONFLICT-340 (residual investor wording W31/W32/W34/OPT-15-03/doc 17), 341 (two products/four frontends vs DEC-009), 342 (breakpoints), 343–345 (API namespaces, generic /control, legacy approve/review; overlap with Group D), 346 (dev-time plugins listed against runtime screens), 347 (provider prices stated as fact), 348 (60 s vs 15 min projection), 349 (scale figures > DEC-031), 350 (Admin payment link listed under website ops), 351 (table naming vs entities).
Earlier-part inconsistencies: Part 2.5 ↔ 2.1 field-list cross-reference (neither had full lists; now in 2.7b cards); API-440/442 support cases lack an entity (→ ServiceRequest).
Open: 83 unmatched legacy operations need alias-vs-new decisions (Group D); 196 field types to confirm in the data dictionary (Group E).

## Group G (docs 19, 22): done
Coverage: 549 Covered / 358 Partial / 5 Not covered / 4 Conflict / 2 N/A / 5 common core (923 aspects). All 799 source tests mapped (Unit 75 / SIT 422 / UAT 302): 187 equivalent, 285 alias-equivalent, 302 operation-class, 24 partial plus a new case, 1 with no equivalent. New TC-ENH-G-001…045; 17 operation-contract classes; UAT packs MKT and CS; execution-status field.
Conflicts: CONFLICT-420 (SM-UT-037/049/050 defined by the source; overrides DEC-094), 421 (unit coverage targets differ), 422 (absolute-amount discount vs % thresholds), 423 (P0–P3 vs S1–S4), 424 (growth RTO 2 h vs 4 h).
Earlier-part issues: DEC-094/GAP-167 superseded; SM-SIT-M numbering ≠ BR-M## (mapped by name); 81 source ops lack a Part 3.2 counterpart (Group D); NFR-082 vs §6.1.9.6 coverage scope. Open: 21 nearest-match operations need API-owner confirmation.

## Group I (docs 18, 25–27, 29–32): done
Coverage: 267 Covered / 116 Partial / 37 Not covered / 25 Conflict / 38 N/A (483 aspects). Files: Part-04-4a (73 pp), 4-4b (42 pp).
Additions: coding standards (186 rules, 40-item review checklist, lint rules, AI-assisted coding policy); typed config contract and drift detection; release-gate validator; reserved control/finance queues; ordered deployment, smoke checks and canary; AL-50…58 and 3 runbooks; growth workload profiles and 6 load tests; pen-test rules of engagement; delivery package; recovery classes. 25 FRs, 10 stories, 41 TCs; +29.5–54 pd.
Conflicts CONFLICT-460…473. Key: availability 99.9% vs 99.5% (DEC-018); capacity vs DEC-031; growth RTO 2 h; 60 s projections vs 15 min.
Earlier-part issues: LT ID duplication (resolved by DEC-116/143); regional RTO 8 h (3.1) vs 24 h (4.2/8.2); Part 4.3 duplicate ADRs (DEC-150); environment naming 3.1 vs 4.3; restore-drill location/frequency; pilot load balancer assumption; §4.4 numbering clash with Part 4.1.
Open: GAP-468, mapping of the pack's outstanding approval counts and 1,188-record preflight (needs groups C/D/E/J).

## Group A (docs 03, 11–14, 37): done
Coverage: 179 Covered / 83 Partial / 13 Not covered / 4 Conflict / 4 N/A (283 aspects; the common core counted once). Doc 14 ≈ a copy of docs 11 and 12. Part-02-6 (125 pp).
Additions: persona variants and P17–P20, role R21 and sub-roles R11T/R12I; managed-service delegation; research coverage ledger; playbooks SPB-01…24; provider benchmark; AOP-01…05; experiment registry; reply taxonomy; relationship ID; doc-37 fixtures and UAT packs. 20 FRs, 14 rules, 29 stories, 50 TCs. +43–72 pd.
Conflicts 300–304 (two scoring models in doc 11; investor wording; source coverage definition; reply taxonomy; relationship stage vs state machines).
Earlier-part issues: the 2.6.x numbering clashes with Part 2.2 §2.6 (assembly heading prefix "Part 2.6" disambiguates); C03 undefined in DEC-020; RamVan/Smart Biochar missing; BRL-SEQ-02 lacks "decline". Open: GAP-300 (missing source inventory/deck).

## Group F (docs 15, 16, 21, 38 §09): done
Coverage: 625 Covered / 50 Partial / 45 Not covered / 17 Conflict / 67 N/A (804 rows; 538 candidates: 485 covered, 52 N/A, 1 conflict). Part-07-4a (59 pp), 4b (54 pp).
Additions: AI result envelope v2; prompt contracts PC-01…18; RAG checks before search and after ranking, plus AU-046 revocation purge; permission-tied cache keys; procurement gate AU-044; benchmark AU-045; licence check AU-047; invoice reconciliation AU-048; tenant margin AU-049; AG-037/038; AU-050–052; 100-use-case library, 20 templates and 13 node types (proposed, ASSUMPTION-400); budget views. +68–110 pd. Pilot AI high case reaches 101% of ₹3,000, held by the hard cap with AG-037/038 deferred.
Conflicts 400–412 (search primary, extraction primary, local-model wording, alert thresholds, schema-valid/precision thresholds, investor wording, Apollo mapping, Hunter budget line, Sentry, numbering, cost routing by rules, ₹16,675 base).
Earlier-part issues: B23 not in DEC-020 (DEC-090 adds it); Part 7.3 file contains §7.4–7.9, clashing with this part's numbering; Hunter budget line; GAP-143 scope too broad.

## CROSS-CUTTING: effort growth from the enhancements
Running total so far: A +43–72, I +29.5–54, F +68–110 pd (others pending). A re-plan decision is needed: MoSCoW triage of the enhancements into R1/R2/W6.

## Group D (doc 07): done
Coverage: 394 Covered / 360 Partial / 340 Not covered / 11 Conflict / 38 N/A (1,143 aspects). Endpoints: 297/321 covered (106 exact, 139 alias, 44 split, 8 folded into Approval); 18 partial; 6 not covered. Per-operation field contracts and per-operation tests were missing → added. Part-03-5a (44 pp), 5b (96 pp).
Additions: full mapping (closes GAP-103); 24 new ops API-ENH-D-001…024; field contracts for 247 ops; SRC07-DEC-001…038 contracts; AdapterCommand/Result envelope; AD-D01…D03; provider register (74); 84-route website ingress allowlist; contract lifecycle state machine; integrity gate; 20 FR-ENH-D; 16 stories; 367 TC-ENH-D.
Conflicts 360–372: canonical paths (360); idempotency/revision placement, list envelope, async states (361–363); source DEC IDs renamed SRC07-DEC (364); inventory counts (365); Portal+Admin audience (366); token routes (367); budget allocation (368); retention semantics (369); 24 status-code differences and bid "submit" meaning (370); PandaDoc/Postiz (371); OpenAI listed (372).
Earlier-part issues: Part 6 tests lack API IDs (now addressed by TC-ENH-D); port list; API-083 token route; missing webhook/upload error codes. Open: GAP-365 (4 DB confirmations not identified), GAP-366 (OpenAPI draft not supplied), 212 blueprint-only ops lack operation-level test rows.

## Group E (docs 08, 28): done
Coverage: 1,300 Covered / 112 Partial / 209 Not covered / 16 Conflict / 4 N/A (1,641 aspects). Tables 155: 77 full, 73 column gaps, 3 column conflicts, 2 had no entity. Columns 799: 666 existing, 124 added, 6 conflict, 3 not adopted. 54 of 276 keys/indexes added. Part-03-6a (49 pp), 6b (42 pp).
Additions: GAP-112 closed (17 entities identified); 4 new entities (ENT-ENH-E-01…04: BusinessTemplate, ServiceRequest, FulfilmentMilestone, EvalCaseResult); 113 column ALTERs; 54 keys + 12 checks; exposure class per table (CI); two-level classification; evidence record; provider-replaceable persistence rules; orphan quarantine; 12-step migration gate; recovery tiers (regenerable research 24 h RPO / 8 h RTO); 14-point restore checklist; 8-step post-restore reconciliation; 10-step tenant offboarding runbook; 36 TCs, 8 FRs, 6 stories.
Conflicts 380–387: source DEC IDs renamed SDEC-08-xxx (380); embedding dim (381, resolved by DEC-088); identity table reuse vs own user table (382); milestones vs append-only events (383); global vs tenant-scoped unique keys (384); RTO 2 h vs 4 h (385); order direction values (386); delay units (387).
Earlier-part issues (7): dangling template_ref; cross-region backup retention 7 vs 35 days (3.1 vs 3.3); three different restore-drill locations; others in 3.6b.

## Group H (docs 20, 23, 24 + decisions in 07/08 + counts in 38): done
Coverage: 969 Covered / 525 Partial / 14 Not covered / 22 Conflict / 2 N/A (1,532 aspects). Part-06-9a (71 pp), 9b (59 pp).
Mappings: 288 FRs (141 → FR-W/A/OP, of which 11 omit source BRs; 147 = SM-UX-FR → FR-UX-*); 76 BRs (71 covered; 5 unidentified in the pack); 162 work items → stories/sprints (base 385 PD vs 382.2 pd planned; longest path 113.5 PD); 245 QCs all mapped (18 partial, 2 conflict, 1 not covered); 352 decisions → SPDEC alias.
Additions: QC register with 31 layer sign-offs (QCL-01…31); fail-closed evidence validator V-01…14; SPDEC decision queue; 1,545-record acceptance preflight; 302 SIT aliases; change-impact gate; 100% trace approval; 6 stories; FR-ENH-H-001…010; 36 TCs; 3 runbooks; 7 entities.
Conflicts 440–447: critical-rule branch coverage 90 vs 85; capacity/workload vs DEC-031; 100% trace approval vs AP-08 10% sample; projection 60 s vs 15 min; growth RTO 2 h; decision ID clash (SPDEC); expansion PD counted as additional; missing BR traces on 11 FRs.
Earlier-part issues: FR-UX alias wording; evidence record lacks an entity; RTM lacks a SIT alias column; NFR-008 vs NFR-047; ServiceRequest entity (added by Group E).

## Group B (docs 04, 05, 09, 10): done
Coverage: 319 Covered / 45 Partial / 15 Not covered / 15 Conflict (394 aspects). Part-03-4 (112 pp).
Additions: LT-ENH-B-01…04, NFR-ENH-B-01…08; recovery classes RC-1…3 (growth RTO ≤ 2 h feasible, ADR-102); adapter port v2; DRF permission base classes; route map and cache-key formula; agent envelope v1.1; product-event allowlist; workflow execution-policy schema and WQG-01…12 gates; reply taxonomy additions; 3 runbooks; backend capacity short by ~38 pd; approval-gate register. 27 FR-ENH-B, 23 stories, 40 TCs, ADR-100…109.
Conflicts 320–330: Fargate/Redis/ALB vs ECS-EC2/Valkey (ADR-013); capacity vs DEC-031; growth RTO 2 h; 99.9% availability; budget alerts 70/90 vs 80/100; no cross-region replication vs ADR-019; investor wording; "six AI responsibilities"; 385 PD/113.5 path vs Part 8; app/repo names; product webhook vs no-handoff rule.
Earlier-part issues: BRL-SEQ-02 out-of-office stop vs pause; NFR-082 line vs branch coverage; no 250-concurrent-session profile.

## Group J (docs 33–36, 38): done
Coverage: 384 Covered / 287 Partial / 85 Not covered / 18 Conflict / 12 N/A (786 aspects). Part-08-3a (52 pp), 3b (59 pp), 3c (67 pp).
Additions: 147 screen task cards (TRN-SCR); 16 learning journeys, 33 modules, 23 practice families, 16 exercises, 20 troubleshooting cards; training-gated permissions plus a TrainingRecord entity; 104 optimization controls mapped (78/20/5/1); OKPI-01…35 mapped to NFR/KPI/SLO/TC; 24 scenarios + 10 UX-QC → TC-ENH-J-001…034; scorecard in A090; SaaS lifecycle CSO-01…12; SLA template SLA-01…12; managed-service RACI; margin model; maintenance calendar MNT-*; retirement; tech-debt register. 22 FRs, 22 stories, 66 TCs.
Conflicts 480–491: 20 vs 21 dimensions (G0 gate added); projection 60 s; spend alerts 70/90; availability 99.9; scale targets; support response 15 min / 1 h vs DEC-044; schema-valid threshold; plan names; BR count 76 vs 71; effort 499 vs 416 PD; acceptance records 1,188 vs 1,545; investor wording.
