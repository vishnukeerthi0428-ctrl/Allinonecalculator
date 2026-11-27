## 2.6.2 Coverage register summary

Counts are produced by `build.py` from the curated register. "Covered" means the blueprint already states the requirement with a traceable ID (the location column names it). "Partially covered" means the intent is present but a field, threshold, role, fixture or procedure the source requires is missing. "Conflict" means the source and the blueprint disagree, and §2.6.6 proposes a resolution.

{{summary}}

**Reading the numbers.** 63% of aspects (179 of 283) were already covered, mostly because documents 12 and 13 re-state BRD/FRD content that Parts 1–3 traced in full. The 100 aspects that need action (83 partially covered, 13 not covered, 4 conflicts) cluster in five themes:

| Theme | Source aspects needing action | Main enhancement (this part) |
|---|---|---|
| Personas, roles and acceptance users | A03-04, 06, 13–17, 20, 21, 25, 28, 31, 33, 35, 36, 39, 42, 43, 46, 47 | §2.6.5.1.1–2.6.5.1.4: 12 persona variants, 4 new personas, 3 new roles or sub-roles, acceptance RACI, training record, productivity protocol |
| Research coverage, source playbooks and benchmarking | A11-02, 07–31, 36, 37, 40, 44–48, 50–52, 58, 63, 65, 67, 68; CC-17 | §2.6.5.2: coverage ledger, 24 source/segment playbooks, per-family freshness, discovery benchmark, alternative scoring version |
| Channel execution details | A12-04, 08, 12, 37, 38, 41 | Reply taxonomy union, recording consent, deliverability stop thresholds, opt-out race, spend-cap race, social post proof |
| Acquisition planning, experiments and economics | A12-44, 48, 50; A14-03, 05, 06, 08, 10–16, 18–20 | Acquisition operating plan, weekly acquisition review, experiment registry with stop triggers, outcome economics, cross-border activation record, legal disclosure |
| Worked fixtures, relationship timeline and UAT packs | A13-13, 15, 26, 43; A37-04–07, 09, 12, 18, 19, 22; CC-06 | Relationship timeline projection, budget fixture, 100 × INR 500 fixture, event-ledger replay, five UAT variants, eight-step demonstration pack |

## 2.6.3 Detailed coverage register

Every aspect is listed. Partial, Not covered, Conflict and Not applicable rows are in bold status. The same rows, with identical IDs, are in `final/coverage/A_coverage.csv`.

{{detailed}}
