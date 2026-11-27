from h_ep01 import R

INTRO = """Risk area RA-13 model gateway (likelihood 5 × impact 5 = 25, the highest in the matrix; P0, D4). Waves W0 (US-0401…0406, 0408; harness and CI gate in W0 per DEC-061) and W5 (US-0407). This batch tests the **gateway, routing, budget and guardrail mechanics deterministically** (stub provider, recorded responses, provider simulator). Statistical agent quality (precision, groundedness, refusal, bias, injection resistance per agent, AG-001…AG-036) is in Batch 6.4 as TC-AI cases; the harness that runs them is tested here (US-0402). Model names and prices are illustrative only (DEC-042; verify at implementation, as of 27 Nov 2026)."""

EXTRA_TS = []

GROUPS = [
    dict(ts="US-0401", heading="State transition – model run lifecycle and repair bound", tech="ST, BVA",
         intro="""Run states (US-0401 notes): reserved → running → validated / rejected / degraded / uncertain.

| From \\ Event | provider OK + schema valid | schema invalid (repair n) | provider 5xx before submit | timeout after submit | budget denied |
|---|---|---|---|---|---|
| (request) | — | — | — | — | → degraded (Tier 3), no reservation |
| reserved | → running | — | → degraded (Tier 3, human task) | — | — |
| running | → validated; actual cost replaces reservation | n ≤ 2 → running (repair); n = 3 → rejected → degraded | → degraded | → uncertain (reservation kept, 202) | — |
| uncertain | reconcile → validated | — | — | stays uncertain; no re-send | — |""",
         rows=[
        R("Reserve before the provider call, validate, and replace the reservation with actual cost", "AC-0401-01; FR-OP001; BRL-AI-01, BRL-AI-08; NFR-014", "Task signal.classify, pv-signal-1.0.0, Tier 1a; AppNAI budget ₹3,000.00 with ₹1,200.00 consumed; stub provider", "1. R19 calls POST `/api/v1/commercial/internal/ai/run` (2,400 input tokens est., max 300 output). 2. Inspect DB ordering and ModelRun", "1: 200 validated. 2: reservation row committed before provider call timestamp; actual cost posted, reservation released; ModelRun holds task, prompt version, model revision, tier, tokens, cost, correlation ID, redacted digests", "P0", "T20", "ST", "Y", "IT"),
        R("Repair invalid output at most twice: valid after 2nd repair vs rejected after 3rd failure", "AC-0401-03; BRL-AI-02", "Stub returns JSON missing `signal_type` k times, then valid", "1. Run with k = 2. 2. Run with k = 3", "1: validated after 2 repairs (3 provider calls). 2: rejected after 2 repairs; Tier 3 degraded; human task; no 4th call", "P0", "T14", "BVA", "Y", "IT"),
        R("Return 202 uncertain on timeout after submission and never re-send before reconciliation", "AC-0401-07; FR-STD-02; DEC-050; NFR-026", "Simulator `timeout_after_submit`", "1. Run. 2. Re-submit with a new idempotency key for the same task item. 3. Reconcile success", "1: 202 uncertain, reservation kept. 2: refused `RUN_UNCERTAIN`. 3: validated; cost posted once", "P0", "T18", "ST", "Y", "IT"),
        R("Return the first run for a repeated idempotency key", "AC-0401-06; NFR-005", "Same key twice within 5 s", "1. Submit twice", "One ModelRun, one reservation; second returns first run's result", "P0", "T16", "EG", "Y", "IT"),
        R("Degrade without provider call when ai.enabled is OFF for External-A", "AC-0401-08; NFR-037; DM-R38", "Flag ai.enabled OFF for T2", "1. T2 job requests a run", "Tier 3 \"degraded – AI disabled\"; 0 simulator calls; 0 reservations", "P0", "T20", "DT", "Y", "IT"),
        R("Block direct provider SDK use outside the gateway (CI and egress)", "AC-0401-02; BRL-AI-01", "PR importing the provider SDK in module `crm`; runtime egress rules", "1. Run architecture test. 2. From a non-gateway container call the provider host", "1: CI fails. 2: egress denied", "P0", "T07", "EG", "Y", "CT"),
    ]),
    dict(ts="US-0402", heading="Boundary values – evaluation gates and regression tolerance (DEC-001, DEC-061)", tech="BVA",
         intro="""| Gate | Below | On | Above | Source |
|---|---|---|---|---|
| Qualification L2 eligibility precision | 0.895 → L1 only | 0.900 → L2 eligible | 0.905 → L2 eligible | DEC-001; BRL-SCR-07 |
| Qualification sample size | 199 → insufficient | 200 → valid | — | DEC-001 |
| Signal W1 precision | 0.799 (79/100 rounded) → not met | 0.800 (80/100) → met | — | DEC-001 |
| Regression tolerance per metric (2.0 pp default, ASSUMPTION-155) | drop 1.9 pp → pass | drop 2.0 pp → pass | drop 2.1 pp → fail | NFR-033; BRL-AI-09 |

Interpretation [ASSUMPTION-196]: a drop exactly equal to the tolerance passes (fail only when the drop is strictly greater).""",
         rows=[
        R("Mark L2 eligible at precision 0.900 with 200 items and L1 only at 0.895", "AC-0402-03; BRL-SCR-07; DEC-001", "Benchmark qual-medmaarg-v1, 200 labelled items; scorer stub returning fixed confusion matrices (180/200 and 179/200 TP rate equivalents)", "1. Run gate with precision 0.900. 2. With 0.895", "1: \"L2 eligible\". 2: \"L1 only\"", "P0", "T14", "BVA", "Y", "CT"),
        R("Refuse L2 eligibility on 199 items even at precision 0.95", "AC-0402-04; DEC-001", "Dataset of 199 items", "1. Run gate", "\"insufficient sample: 199 < 200\"; not L2 eligible", "P0", "T14", "BVA", "Y", "CT"),
        R("Pass a 2.0 pp drop and fail a 2.1 pp drop against baseline 0.84", "AC-0402-02; BRL-AI-09; NFR-033; ASSUMPTION-196", "Baseline precision 0.840", "1. Candidate 0.820. 2. Candidate 0.819. 3. Candidate 0.810", "1: pass. 2: fail \"precision dropped 2.1 pp (tolerance 2.0 pp)\". 3: fail (3.0 pp) although 0.81 ≥ 0.80", "P0", "T14", "BVA", "Y", "CT"),
        R("Record a passing eval with dataset hash and block when the provider is down", "AC-0402-01, AC-0402-06; DEC-061", "Dataset signals-appnai-v1 (120 items, hash ds-9c1…); provider 503 variant", "1. PR changes pv-signal-1.0.0 → 1.1.0. 2. Repeat with provider 503", "1: results recorded (precision, recall, schema validity, cost per item) with dataset hash; pass. 2: \"eval not executed\"; merge blocked; stub unit tests still run", "P0", "T14", "UC", "Y", "CT"),
        R("Fall back to the 30-item smoke subset when a full run would exceed the CI eval budget", "AC-0402-07; NFR-014", "CI eval budget ₹300.00/month (estimate) with ₹295.00 used", "1. Trigger full run", "Smoke subset (30 items per task) runs; \"full eval pending\" flag blocks release until a full run passes", "P1", "T20", "BVA", "Y", "CT"),
    ]),
    dict(ts="US-0403", heading="Decision table – tier routing with data-classification guard (DEC-007)", tech="DT",
         intro="""Unclassified input is treated as Restricted (fail closed). Tier 2 = free/open-weight fallback, tenant opt-in approved by R01 + R10, default OFF.

| Rule | Tier 0 cache hit | Data class | Tier 1a parity proven | Tier 1 available | Tier 2 opted in | Route |
|---|---|---|---|---|---|---|
| T1 | Y | any | – | – | – | Tier 0, ₹0.00, no provider call |
| T2 | N | Public / Internal-non-personal | Y | Y | – | Tier 1a |
| T3 | N | Restricted / Internal-personal | N | Y | – | Tier 1b |
| T4 | N | Public | – | N | Y | Tier 2 (`fallback=tier2`) |
| T5 | N | Public | – | N | N | Tier 3 degrade |
| T6 | N | Restricted or unclassified | – | N | Y | Tier 3 degrade; `RESTRICTED_NOT_ALLOWED_TIER2` |
| T7 | N | any | – | Y, confidence < threshold | – | abstain → human queue |""",
         rows=[
        R("T1: serve an identical normalized input from Tier 0 cache with zero cost", "AC-0403-01; DEC-007; BRL-AI-04", "need.extract validated result 2 h old", "1. Submit same input", "Tier 0; cost ₹0.00; 0 provider calls", "P1", "T20", "DT", "Y", "IT"),
        R("T2/T3: route signal.classify to Tier 1a only with proven parity; message.draft stays Tier 1b", "AC-0403-02; RECOMMENDATION-003; NFR-030", "Parity record 0.84 vs 0.85 within tolerance for signal.classify; none for message.draft", "1. Route both", "signal.classify → Tier 1a; message.draft → Tier 1b", "P0", "T14", "DT", "Y", "UT"),
        R("T6: refuse Tier 2 for Restricted data even when opted in and Tier 1 is down", "AC-0403-03; BRL-AI-06; DEC-007", "T1 opted in to Tier 2; Tier 1 simulator 503; task with contact personal data", "1. Submit", "Tier 3 degraded; log `RESTRICTED_NOT_ALLOWED_TIER2`; 0 Tier 2 calls (S1 if any)", "P0", "T07", "DT", "Y", "UT"),
        R("T6: treat unclassified input as Restricted", "AC-0403-07; BRL-AI-06", "Task without data_classification at router level (gateway API validation bypassed in UT)", "1. Route with Tier 1 down and Tier 2 on", "Restricted path; never Tier 2", "P0", "T07", "DT", "Y", "UT"),
        R("T4: use Tier 2 for a Public task when approved and Tier 1 returns 503", "AC-0403-05; DEC-007", "Tier 2 approved and enabled; task query.expand Public", "1. Submit", "Tier 2 used; `fallback=tier2` recorded; same schema validation passed", "P1", "T14", "DT", "Y", "IT"),
        R("T5: degrade a Public task to Tier 3 when Tier 2 is not opted in", "US-0403; DEC-007; NFR-037", "Tier 2 OFF; Tier 1 503", "1. Submit", "Tier 3 degraded result with human task; 0 Tier 2 calls", "P0", "T14", "DT", "Y", "UT"),
        R("T7: abstain at confidence 0.69 and accept at 0.70", "AC-0403-06; BRL-AI-04", "Threshold 0.70", "1. Model confidence 0.69. 2. 0.70. 3. 0.55", "1, 3: abstained → review queue. 2: accepted", "P0", "T14", "BVA", "Y", "UT"),
        R("Hold a Tier 2 opt-in by R11 until R01 and R10 approve", "AC-0403-04; CFG-25; BRL-APR-11", "R11 enables Tier 2 for External-A", "1. Submit change. 2. R01 approves. 3. R10 approves", "1–2: Pending; routing unchanged. 3: active; A011 shows data-classification warning", "P0", "T07", "DT", "Y", "SYS"),
    ]),
    dict(ts="US-0404", heading="Boundary values – budget reservation, 80% alert and hard cap (BRL-AI-08, DEC-008)", tech="BVA",
         intro="""Illustrative reservation (US-0404 notes): (3,000 × $2 + 800 × $10) ÷ 1,000,000 × ₹90 = **₹1.26** (prices and FX unverified; DEC-042). Budget ₹3,000.00 for 2027-02 (B02 pilot ceiling, DEC-008).

| Consumed + reserved | Next reservation | Expected |
|---|---|---|
| ₹2,399.99 (79.99%) | — | no alert |
| ₹2,400.00 (80.00%) | — | NT-025 High once (deduplicated by budget ID + threshold) |
| ₹2,998.74 | ₹1.26 → total ₹3,000.00 | allowed (reaches 100% exactly) |
| ₹2,999.50 | ₹1.26 → ₹3,000.76 | denied `BUDGET_EXCEEDED`, NT-025 Critical |""",
         rows=[
        R("Reserve ₹1.26, show ₹648.74 remaining, post actual ₹0.97 and release ₹0.29", "AC-0404-01; FR-A012; BRL-AI-08", "AppNAI ₹2,350.00 consumed", "1. Tier 1b run reserves. 2. Complete with actual ₹0.97", "1: remaining ₹648.74 (reserved-adjusted). 2: ledger actual ₹0.97; release ₹0.29; consumed ₹2,350.97", "P0", "T20", "BVA", "Y", "IT"),
        R("No alert at 79.99%; one NT-025 High at 80.00% even when crossed twice", "AC-0404-02; BRL-AI-08; NT-025", "Clock control within 2027-02", "1. Bring total to ₹2,399.99. 2. To ₹2,400.00. 3. Release and re-cross 80%", "1: none. 2: NT-025 to R01, R08, R11. 3: no second alert", "P0", "T20", "BVA", "Y", "IT"),
        R("Allow a reservation that reaches exactly 100% and deny one that would exceed it", "AC-0404-03; NFR-014; BRL-AI-08", "Totals ₹2,998.74 and ₹2,999.50", "1. Reserve ₹1.26 at each total", "1st: allowed (₹3,000.00). 2nd: denied `BUDGET_EXCEEDED`; 0 provider calls; Tier 3; NT-025 Critical", "P0", "T20", "BVA", "Y", "IT"),
        R("Prove the stop in staging: ₹10.00 cap, 100 runs of ₹0.50 → exactly 20 complete", "AC-0404-04; NFR-014; KR1.4", "Staging budget ₹10.00; 100 concurrent runs (k6)", "1. Submit 100 runs", "Exactly 20 complete, 80 denied; ledger total ₹10.00; no overspend under concurrency", "P0", "T20", "BVA", "Y", "SYS"),
        R("Reset the budget at month start and keep February overspend at zero", "US-0404; BRL-AI-08", "February exhausted; clock to 2027-03-01T00:00:00+05:30", "1. Reserve at 2027-02-28T23:59:59. 2. At 2027-03-01T00:00:00", "1: denied. 2: allowed against March budget", "P0", "T20", "BVA", "Y", "IT"),
        R("Record one cost-ledger entry for a duplicated usage callback", "AC-0404-07; NFR-005; NFR-035", "Usage callback for MR-4410 twice", "1. Deliver twice", "One ledger entry", "P0", "T16", "EG", "Y", "IT"),
        R("Allow R11 to tighten to ₹2,500.00 and refuse a raise to ₹4,000.00", "AC-0404-05; BRL-APR-11", "R11 session", "1. PUT cap 2,500.00. 2. PUT cap 4,000.00", "1: effective immediately. 2: 403 `FOUNDER_APPROVAL_REQUIRED`", "P0", "T20", "DT", "Y", "SYS"),
    ]),
    dict(ts="US-0406", heading="Error guessing – deterministic guardrail checks (agent-level red team in Batch 6.4)", tech="EG",
         intro="", rows=[
        R("Strip an uncited factual claim and record UNCITED_CLAIM", "AC-0406-03; BRL-AI-03", "Draft with \"Our scanner reduces ICU admissions by 40%\" and no citation", "1. Run output guard", "Sentence removed; reason `UNCITED_CLAIM`; remaining text schema-valid", "P0", "T14", "EG", "Y", "UT"),
        R("Reject a citation ID not in the run's evidence set", "AC-0406-07; BRL-AI-03", "Output cites EV-99999", "1. Run citation check", "`INVALID_CITATION`; sentence removed", "P0", "T14", "EP", "Y", "UT"),
        R("Reject an output carrying an action field", "AC-0406-05; BRL-AI-07; DEC-064", "Model returns `\"approve\": true`", "1. Validate against schema", "Rejected (no action field exists); no state change", "P0", "T07", "EG", "Y", "UT"),
        R("Block medical advice for MedMaarg and route to a human", "AC-0406-04; BRL-AI-05", "Answer contains \"You should stop taking metformin\"", "1. Run prohibited-content guard", "`PROHIBITED_MEDICAL_ADVICE`; blocked; human task", "P0", "T14", "EG", "Y", "UT"),
    ]),
]

TS_TITLE = {
    "US-0401": "Every model call goes through the gateway with reservation, validation and reconciliation",
    "US-0402": "Eval harness gates every prompt, model or route change",
    "US-0403": "Rules-first routing never sends Restricted data to Tier 2",
    "US-0404": "Budgets reserve before the call and never exceed the hard cap",
    "US-0405": "AI configuration promotes only evaluated versions",
    "US-0406": "Prompt-injection isolation and output guardrails",
    "US-0407": "AI feedback becomes eval cases, never direct production changes",
    "US-0408": "AI run logs redacted and cost per task reported",
}
