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
