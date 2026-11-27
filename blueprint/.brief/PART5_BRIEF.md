# Part 5 brief: Epics and User Stories (applies to batches 5.1, 5.2, 5.3)

Read `SHARED_BRIEF.md` first. This file adds Part 5 rules that are common to all three batches so the results are consistent.

## Client specification (Section 6.9)
- **Each epic:** ID, title, business value, linked BR/FR, scope (in/out), dependencies, priority, estimated size.
- **Each story:** "As a [persona], I want [capability] so that [benefit]"; linked FR/NFR; priority; story points (estimate); dependencies; and **Gherkin acceptance criteria** covering the **happy path, alternate paths, negative paths, validations, permissions and edge cases**.
- Include **technical enablers, spikes, data migration, security, accessibility and observability stories**, not only functional ones.
- Stories meet INVEST and the Definition of Ready / Done (defined in batch 5.1).
- Permutation coverage: persona/role × permission level × object state × data condition (valid/invalid/boundary/null/duplicate/large) × channel (web/mobile/API) × tenant/config variation × integration availability × locale. The dimension matrix and its coverage rationale are defined once in batch 5.1. All batches must apply it in their AC.

## Fixed conventions (all batches must use exactly these)
- **Epic IDs:** EP-01 … EP-21 as listed in Part 0 §0.10.2 / Part 1 §1.12.1 (titles as given there).
- **Story ID:** `US-<epic 2 digits><sequence 2 digits>`, e.g. `US-0101`, `US-0102`, `US-1401`.
- **AC ID:** `AC-<story digits>-<2-digit seq>`, e.g. `AC-0101-01`. Each Gherkin `Scenario:` line starts with its AC ID: `Scenario: AC-0101-01 Happy path – ...`.
- **Story types:** Feature, Enabler, Spike, Security, Accessibility, Observability, Data-migration, Compliance.
- **Persona references:** P01–P16 (Part 1 §1.8). **Role references:** R01–R20 (Part 2.3).
- **Priority:** MoSCoW, consistent with the BR's priority in Part 1 §1.12.1 (a story may be lower than its BR, never higher). **Wave:** W0–W6, consistent with the FR's wave in Part 2.1.
- **Story points:** Fibonacci 1, 2, 3, 5, 8, 13, given as a range (e.g. "3–5"). No story above 13; split instead.
- **Estimation basis [ASSUMPTION owned by batch 5.1]:** 1 story point ≈ 0.5–1.0 person-day (central 0.7) for this team (DEC-005). Epic person-day range = Σ story points × 0.5 (low) to × 1.0 (high). Overall the 21 epics must land within the BRD §6 envelope of **287–483 person-days**.
- **Indicative mid-point person-days per epic** (guidance; deviate if justified, and explain why):
  | Epic | Mid pd | Epic | Mid pd | Epic | Mid pd |
  |---|---|---|---|---|---|
  | EP-01 | 28 | EP-08 | 25 | EP-15 | 17 |
  | EP-02 | 15 | EP-09 | 9 | EP-16 | 15 |
  | EP-03 | 23 | EP-10 | 13 | EP-17 | 15 |
  | EP-04 | 19 | EP-11 | 15 | EP-18 | 25 |
  | EP-05 | 26 | EP-12 | 17 | EP-19 | 21 |
  | EP-06 | 15 | EP-13 | 21 | EP-20 | 13 |
  | EP-07 | 19 | EP-14 | 17 | EP-21 | 14 |
  (Total ≈ 382 pd.)
- **Coverage obligation:** every FR whose *Epic* column in Part 2.1 is one of your epics must be covered by ≥ 1 story. Also cover every primary BR mapped to your epics in Part 1 §1.12.1, the relevant BR-S statements, and the relevant BRL rules and DECs. End each batch with a **coverage table**: FR → story IDs, and BR → story IDs. Flag any FR you could not cover.
- **AC depth:** typically 4–8 Gherkin scenarios per story. Use concrete data, e.g. INR amounts with Decimal values, dates with time zones, quantities with units. Use the FRD §12.1 worked examples where relevant (quote 2 × 150.00 with 10% discount = 270.00 INR; bid deadline 2030-06-01 09:00 UTC; order 2 kg delivered 1 kg twice with the same event key; routing of AI project vs school education). Cite the BRL rule each negative scenario enforces.
- **Every story must include at least one permission/scope scenario.** This can be inherited by citing the acceptance profile (CA-ADMIN, CA-PORTAL, etc.), but write at least one explicit denial scenario per story.
- **Gherkin formatting:** fenced ```gherkin blocks; `Feature:` line = story title; `Background:` where useful.
- **Format per story:** a compact header table (ID, Title, Type, Story statement, Persona, Linked FR/BR/NFR/BRL/DEC, Priority, Wave, Points, Dependencies, Notes), then the Gherkin block.
- **Format per epic:** an epic card table (ID, title, business value, linked BRs/FRs, in scope, out of scope, dependencies, priority, wave(s), size in SP range and pd range, stories count), then the stories, then a small epic summary.
- Diagrams are not required in Part 5.

## File naming
- Batch 5.1 → `Part-05-1_Epics_Stories_Foundation.md` (may split into `Part-05-1a_…`, `Part-05-1b_…` if very long). Header label "Application Blueprint · Part 5.1".
- Batch 5.2 → `Part-05-2_Epics_Stories_Engagement_and_Commerce.md` (may split as above). Label "Part 5.2".
- Batch 5.3 → `Part-05-3_Epics_Stories_Closure_Automation_Web_SaaS.md` (may split as above). Label "Part 5.3".

Render each file with `make_pdf.sh` (zero diagram errors trivially, since there are no diagrams). Do not git commit.

## Report back
File names, page counts, number of stories per epic, total story points range and pd range per epic, FRs not covered (should be none), tags issued, and inconsistencies found.
