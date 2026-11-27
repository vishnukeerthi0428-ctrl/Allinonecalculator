# Part 6 test-case batches brief (6.2, 6.3, 6.4, 6.5)

Read `SHARED_BRIEF.md` first. Then read **`Part-06-1_Test_Strategy.md` in full**. It defines the conventions you must follow: ID formats TS-<EP>-##, TC-<EP>-###, TC-AI-…, the test case template, priorities P0–P3, test types, techniques, the synthetic dataset GSE-SYN, clock control, the provider simulator, severity and the SM-* alias mapping.

## Client specification (Section 6.10, test design portion)
- **Test scenarios:** high-level scenarios per epic.
- **Test cases:** ID, linked requirement/story, preconditions, test data, steps, expected result, priority, type, automation candidate (Y/N). Derive them with equivalence partitioning, boundary value analysis, decision tables, state-transition testing and pairwise/combinatorial testing, and **show the technique used for each group**.
- **AI test cases:** groundedness, accuracy, bias, refusal, injection resistance, schema compliance, latency, cost per task, fallback behaviour.
- A **requirement-to-test traceability matrix** with coverage % and any uncovered items flagged (batch 6.5).

## Rules for case batches
- Source the stories from Part 5 (`Part-05-*.md`): every **story's AC (AC-xxxx-yy) must be covered by ≥ 1 test case**. Every FR in your epics, and every BRL rule those stories cite, must have ≥ 1 test case.
- Organize per epic:
  1. Scenario table: TS ID, title, linked US/FR, risk priority.
  2. Test-case **groups** per technique, each with a heading such as "Group TC-08-A: Decision table – eligibility at dispatch (technique: decision table)". For decision tables and state transitions, include the table or transition matrix itself.
  3. Test case table with the template columns. Make each test case concrete: real data values, units, currencies, timezones, roles R01–R20 and personas P01–P16.
- **Include negative, boundary, permission/scope (cross-tenant), duplicate/replay, uncertain-outcome, simulation, accessibility and localization cases** wherever relevant.
- **Volume guidance:** about 3–6 test cases per story on average, more for P0 areas.
- **End each batch with:** (a) a coverage table (story → TC IDs, FR → TC IDs, AC → TC IDs if compact, or a statement with counts); (b) totals by priority, type, technique and automation candidate; (c) tags register and quality gate.
- **Tag ranges:** 6.2 RECOMMENDATION-075…076, ASSUMPTION-185…187; 6.3 RECOMMENDATION-077…078, ASSUMPTION-188…190; 6.4 RECOMMENDATION-079, ASSUMPTION-191…193, GAP-168…169; 6.5 ASSUMPTION-194…196, GAP-170…172.
- Render with make_pdf.sh. Do not git commit. Report back: files, pages, counts (scenarios, cases by priority), uncovered items, inconsistencies.
