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
