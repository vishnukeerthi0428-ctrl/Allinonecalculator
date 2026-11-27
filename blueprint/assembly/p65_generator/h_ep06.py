from h_ep01 import R

INTRO = """Risk area RA-21 scoring and qualification (P1, depth D3); contact discovery under RA-22 (P1) with "no guessed emails" and "Verified ≠ consent" as P0 compliance cases; accessibility RA-30. Wave W1 for all stories. The scoring engine is the main target of **boundary value analysis (DEC-011)**: band edges, the 0.60 known-weight rule, half-up rounding to an integer, weight-sum validation and component range checks, plus property-based tests. A score never grants permission to contact (BRL-ELG-04, tested with the PDP in EP-03)."""

EXTRA_TS = []

SCORE_TABLE = """Formula (DEC-011; BRL-SCR-01): `score = ROUND_HALF_UP(100 × Σ wᵢcᵢ ÷ Σ w_known)`, default weights fit 0.25, evidence 0.25, intent 0.20, readiness 0.15, timing 0.15; Unknown when Σ w_known < 0.60 (BRL-SCR-02); bands ≥ 75 Priority review, 50–74 Research/nurture, < 50 Archive/review (BRL-SCR-03). Components are Decimals in [0, 1]. With default weights the achievable known-weight sums near the boundary are 0.55 and 0.60; 0.59 needs the test-only weight set **W-T** (0.29, 0.30, 0.21, 0.10, 0.10), activated as scoring version `SV-TEST-BVA` in the `test` environment only.

| Case | Inputs (fit, evidence, intent, readiness, timing; – = unknown) | Σ w_known | Raw | Score | Band |
|---|---|---|---|---|---|
| S1 all known | 0.90, 0.90, 0.80, 0.70, 0.60 | 1.00 | 80.5 | 81 | Priority review |
| S2 partial | 0.80, 0.90, 0.60, –, – | 0.70 | 77.857 | 78 | Priority review |
| S3 known weight 0.60 | 0.80, –, 0.60, 0.70, – | 0.60 | 70.833 | 71 | Research/nurture |
| S4 known weight 0.55 | 0.80, –, –, 0.70, 0.60 | 0.55 | — | Unknown | review group |
| S5 known weight 0.59 (W-T) | 0.80, 0.90, –, –, – | 0.59 | — | Unknown | review group |
| S6 known weight 0.50 | 0.80, 0.90, –, –, – | 0.50 | — | Unknown | review group |
| S7 band edge 75 | all 0.75 | 1.00 | 75.0 | 75 | Priority review |
| S8 band edge 74 | all 0.74 | 1.00 | 74.0 | 74 | Research/nurture |
| S9 band edge 50 | all 0.50 | 1.00 | 50.0 | 50 | Research/nurture |
| S10 band edge 49 | all 0.49 | 1.00 | 49.0 | 49 | Archive/review |
| S11 half-up at x.5 | all 0.745 | 1.00 | 74.5 | **75** (banker's rounding would give 74) | Priority review |
| S12 half-up at 49.5 | all 0.495 | 1.00 | 49.5 | **50** | Research/nurture |
| S13 extremes | all 0.00 / all 1.00 | 1.00 | 0 / 100 | 0 / 100 | Archive / Priority |
| S14 invalid component | fit 1.01 or −0.01 | — | — | 400 `COMPONENT_OUT_OF_RANGE` | — |"""

GROUPS = [
    dict(ts="US-0601", heading="Boundary value analysis – opportunity score, bands and rounding (DEC-011)", tech="BVA, PBT", intro=SCORE_TABLE, rows=[
        R("S1: score 81 Priority review with breakdown bars", "AC-0601-01; FR-A022; DEC-011; BRL-SCR-01", "SV-MM-1 active for MedMaarg; OPP-7001", "1. Calculate with S1 inputs. 2. Render breakdown", "1: 81, Priority review. 2: weighted contributions 22.5, 22.5, 16.0, 10.5, 9.0", "P1", "T01", "BVA", "Y", "UT"),
        R("S2: re-normalize partially known components to 78", "AC-0601-02; BRL-SCR-01", "As above", "1. Calculate with S2", "78; readiness and timing listed \"Unknown\"", "P1", "T01", "BVA", "Y", "UT"),
        R("S3 vs S4: a number at known weight 0.60, Unknown at 0.55", "AC-0601-03; BRL-SCR-02; FR-UIS-02", "As above", "1. Calculate S3. 2. Calculate S4", "1: 71 Research/nurture. 2: \"Unknown – review required\", no band, sorted into the review group", "P1", "T01", "BVA", "Y", "UT"),
        R("S5 and S6: Unknown at known weight 0.59 (W-T) and 0.50", "AC-0601-03; BRL-SCR-02", "SV-TEST-BVA for S5; SV-MM-1 for S6", "1. Calculate S5. 2. Calculate S6", "Both Unknown; no number displayed anywhere (list, card, export)", "P1", "T01", "BVA", "Y", "UT"),
        R("S7–S10: band edges 75, 74, 50, 49", "AC-0601-04; BRL-SCR-03", "Uniform component sets", "1. Calculate each", "Priority review · Research/nurture · Research/nurture · Archive/review", "P1", "T01", "BVA", "Y", "UT"),
        R("S11–S12: round 74.5 up to 75 and 49.5 up to 50 using Decimal arithmetic", "AC-0601-04; DEC-011; EG-02; ASSUMPTION-184", "Inputs as JSON strings \"0.745\" (never floats)", "1. Calculate S11. 2. Calculate S12. 3. Static check: no `round()` or float in the scoring module", "1: 75 Priority review. 2: 50 Research/nurture. 3: check passes", "P1", "T01", "BVA", "Y", "UT"),
        R("S13–S14: extremes 0 and 100 accepted; components outside [0, 1] refused", "AC-0601-04; BRL-SCR-01", "As table", "1. Calculate extremes. 2. Submit fit 1.01 and −0.01", "1: 0 and 100. 2: 400 `COMPONENT_OUT_OF_RANGE`; no ScoreVersion", "P1", "T01", "BVA", "Y", "UT"),
        R("Property: score bounded, monotonic per component and Unknown iff known weight < 0.60", "AC-0601-01…04; BRL-SCR-01, BRL-SCR-02; Part 6.1 §6.1.11.7", "Hypothesis: components Decimal in [0, 1] at 0.005 steps or None; weights from SV-MM-1, SV-MM-2, W-T", "1. Generate; compare with reference implementation", "0 ≤ score ≤ 100; raising any one component never lowers the score; Unknown exactly when Σ w_known < 0.60; matches reference", "P1", "T01", "PBT", "Y", "UT"),
        R("Recalculate on new evidence once despite a duplicated event and keep history", "AC-0601-06; BRL-SCR-08; NFR-005", "OPP-7001 at 81; intent raised to 0.90", "1. Deliver the recalculation event twice", "One new ScoreVersion 83; 81 retained in history", "P1", "T16", "EG", "Y", "IT"),
        R("Offer no outreach for a score of 81 whose only contact is suppressed", "AC-0601-05; BRL-ELG-04", "OPP-7001 81; contact suppressed", "1. Open shortlist", "\"Not contactable (suppressed)\"; no outreach action; PDP not bypassed", "P0", "T19", "DT", "Y", "SYS"),
    ]),
    dict(ts="US-0602", heading="Boundary values and state transition – scoring version approval", tech="BVA, ST", intro="", rows=[
        R("Accept weights summing to 1.00 and refuse 0.99 and 1.01", "AC-0602-02; FR-A023; BRL-SCR-01", "R04 drafts SV-MM-2", "1. Save weights summing 0.99. 2. 1.00. 3. 1.01. 4. 1.05", "2: saved. 1, 3, 4: blocked \"Weights must total 100% (currently 99% / 101% / 105%)\"", "P1", "T01", "BVA", "Y", "SYS"),
        R("Simulate on val-mm-80, approve the hash, activate and queue recalculation", "AC-0602-01; BRL-APR-02; CA-CONFIG", "SV-MM-2 (.30/.25/.20/.15/.10)", "1. Simulate. 2. R02 approves. 3. Activate", "1: \"12 move to Priority review, 5 move to Research/nurture\". 3: active; MedMaarg opportunities queued", "P1", "T01", "ST", "Y", "SYS"),
        R("Void approval when the version is edited after approval", "AC-0602-03; BRL-APR-02", "SV-MM-2 approved, not active", "1. R04 edits weights. 2. Activate", "1: new Draft revision. 2: 409 approval required", "P1", "T01", "ST", "Y", "SYS"),
        R("Complete an in-flight batch on SV-MM-1 when SV-MM-2 activates mid-batch", "AC-0602-05; BRL-AUT-03", "Batch of 500 opportunities started on SV-MM-1", "1. Activate SV-MM-2 after 200 processed", "All 500 scored on SV-MM-1; follow-up batch applies SV-MM-2", "P1", "T01", "ST", "Y", "IT"),
    ]),
    dict(ts="US-0604", heading="Boundary values – contact verification expiry (180 days, ERRATA-38)", tech="BVA",
         intro="`contact_verification_days` default 180 (ASSUMPTION-155; GAP-151 resolution in ERRATA-38). Verified 2027-02-16 → expiry 2027-08-15. Interpretation [ASSUMPTION-196]: Verified through 2027-08-14 23:59:59 IST; Stale from 2027-08-15 00:00 IST.",
         rows=[
        R("Verify with expiry 2027-08-15 and show \"Verified ≠ consent\"", "AC-0604-01; FR-A025; BRL-ELG-03", "R04; admin.office@kims-hospital.example.com published on contact page", "1. Verify on 2027-02-16", "Verified; expiry 2027-08-15; banner shown", "P1", "T01", "BVA", "Y", "SYS"),
        R("Stay Verified at 2027-08-14 23:59:59 and become Stale at 2027-08-15 00:00", "AC-0604-03; BRL-SRC-06", "Clock control", "1. Evaluate at both instants", "Verified, then Stale; recheck job queued; NT-005 to R04 only if recheck fails", "P1", "T01", "BVA", "Y", "SYS"),
        R("Keep eligibility \"no lawful basis\" after verification", "AC-0604-02; BRL-ELG-03", "Verified contact without basis", "1. PDP check for marketing email", "Deny `NO_LAWFUL_BASIS`", "P0", "T19", "DT", "Y", "UT"),
    ]),
    dict(ts="US-0606", heading="Decision table – qualification checklist and autonomy gate (BRL-SCR-06, -07)", tech="DT",
         intro="""| Condition / Rule | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 |
|---|---|---|---|---|---|---|
| Single-startup scope | N | Y | Y | Y | Y | Y |
| Actor human (R04/R02) or agent at L2 with benchmark ≥ 0.90 on ≥ 200 items | – | N | Y | Y | Y | Y |
| Need Confirmed with evidence | – | – | N | Y | Y | Y |
| Offering Available | – | – | – | N | Y | Y |
| ≥ 1 Eligible contact | – | – | – | – | N | Y |
| Owner selected (and not a duplicate org × offering × startup) | – | – | – | – | – | Y |
| **Action** | 409 `SELECT_SINGLE_STARTUP` | PDP deny `QUALIFICATION_L1_ONLY` | Accept disabled; checklist "Need – missing" | "Offering – missing" | "Eligible contact – missing" | Qualified; NT-001 to owner; `opportunity.qualified` emitted |""",
         rows=[
        R("Q6: accept OPP-7001 with all four criteria and assign Ravi", "AC-0606-01; FR-A027; BRL-SCR-06; KPI-07", "OPP-7001 PriorityReview score 81; N-501 Confirmed; offering Available; Dr. A. Nair Eligible", "1. R04 accepts with owner ravi.k", "Qualified; NT-001 to Ravi; event `opportunity.qualified`", "P1", "T01", "DT", "Y", "SYS"),
        R("Q5: disable Accept when no contact is Eligible", "AC-0606-02; BRL-SCR-06", "Contacts all Ineligible", "1. Open review. 2. POST accept via API", "1: Accept disabled; \"Eligible contact – missing\". 2: 409 `CHECKLIST_INCOMPLETE`", "P1", "T01", "DT", "Y", "SYS"),
        R("Q3/Q4: block acceptance when the need is unconfirmed or the offering is Planned", "US-0606; BRL-SCR-06; BRL-SCR-04", "Variant A need inferred only; variant B offering Doctor Connect Planned", "1. Accept each", "Both 409; checklist shows the missing item", "P1", "T01", "DT", "Y", "SYS"),
        R("Q2: deny agent L2 qualification at benchmark precision 0.86", "AC-0606-05; BRL-SCR-07; DEC-001", "qual-medmaarg-v1 precision 0.86", "1. Agent requests qualify OPP-7003 at L2", "PDP deny `QUALIFICATION_L1_ONLY`; item stays in the human queue", "P0", "T19", "DT", "Y", "SYS"),
        R("Q1: hide Accept/Reject in portfolio scope and return 409 on the API", "AC-0606-06; BRL-TEN-05; DM-R20", "Founder All startups", "1. Open queue. 2. POST accept", "1: actions hidden. 2: 409 `SELECT_SINGLE_STARTUP`", "P0", "T15", "DT", "Y", "SYS"),
        R("Duplicate org × offering × startup is linked and counted once in KPI-07", "AC-0606-04; BRL-SCR-06; NFR-005", "OPP-7001 Qualified for KIMS × Wellness Scanner", "1. Accept another opportunity for the same pair", "Linked as duplicate; KPI-07 counts 1", "P1", "T16", "DT", "Y", "SYS"),
        R("Exclude a rejected opportunity's contacts from every channel", "AC-0606-03; BRL-ELG-15", "R04 rejects OPP-7002 \"Outside service region\"", "1. Reject. 2. PDP check on its behalf for email and WhatsApp", "Rejected; both Ineligible (BRL-ELG-15)", "P0", "T19", "DT", "Y", "SYS"),
    ]),
]

TS_TITLE = {
    "US-0601": "Scores follow DEC-011 exactly; Unknown below 0.60 known weight",
    "US-0602": "Scoring versions simulated, approved and pinned",
    "US-0603": "Contacts only from published organizational sources",
    "US-0604": "Contact verification expires and never implies consent",
    "US-0605": "Contact roles normalized; merges never invent channels",
    "US-0606": "Qualification needs all four criteria; L1 until the benchmark gate",
    "US-0607": "Internal research alert rules with deduplication",
    "US-0608": "Review queues and score visuals are accessible",
}
