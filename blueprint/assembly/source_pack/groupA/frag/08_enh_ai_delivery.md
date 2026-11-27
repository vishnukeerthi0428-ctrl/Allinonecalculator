### 2.6.5.9 Part 7 and Part 8 enhancements: AI touchpoints, cost and delivery placement

#### 2.6.5.9.1 AI agent touchpoints (no new agent)

The group A enhancements reuse existing agents (Part 7.2). No agent gains a tool with an external side effect (DEC-048, DEC-064). Restricted data never goes to Tier 2 free models (DEC-007).

| Agent | Change | Guardrail | Fallback | KPI | Cost effect (estimate) |
|---|---|---|---|---|---|
| AG-003 Research Query Planner | Reads coverage-planner priorities (FR-ENH-A-003) and SPB access method; proposes queries only for families in Scheduled or Pilot mode | Never proposes queries for manual-only or prohibited families (SPB "Never" column) | Tier 0 template queries per SPB | KPI-ENH-A-01, KPI-02 | None (same call volume) |
| AG-005 Buying Signal Classifier | Evaluated per source family with the FR-ENH-A-005 benchmark; report carries recall and n (BRL-ENH-A-04) | Unchanged | Unchanged | KPI-02, KPI-ENH-A-04 | Benchmark runs: ≤ 50 records × 13 families per quarter on Tier 1a ≈ 650 calls; at ~2,000 input + 300 output tokens each, about 1.3M input and 0.2M output tokens ≈ $0.23 per quarter on Haiku 5.5 list price (verify at time of implementation, as of 27 Nov 2026) |
| AG-013 Inbound Intent Classifier & Router | Output enum extended to the 11-class union (FR-ENH-A-008); eval set adds ≥ 30 labelled examples per new class (decline, meeting request, unknown) | Low confidence (below a configurable threshold, default 0.60 [ASSUMPTION-309]) → `unknown` → pause and human task | Tier 0 keyword rules for STOP/unsubscribe always run first | Classification accuracy per class; zero missed STOP | None |
| AG-016 Autonomous Commercial Planner | Must cite the active AOP revision and experiment registry; cannot propose a plan outside AOP budget split | Plan hash approval unchanged (DEC-064) | Manual plan | KPI-19, KPI-20 | None |
| AG-029 Insight Narrative Agent | Drafts the WAR pack narrative from RP-ENH-A-01…04 (labelled "summary of reported figures"; no new numbers) | Numbers copied from reports only; narrative never states causality without an experiment comparison (BRL-ENH-A-14) | Template narrative (Tier 0) | WAR pack generated on time | ~30 startups × 4.3 weeks × (8,000 input + 1,500 output tokens) ≈ 1.03M input + 0.19M output tokens per month ≈ $0.20/month on Haiku 5.5 list price (verify) |
| AG-032 Partner Due-Diligence Brief | Used in SPB-22 deployment partner stage path | Organization-level public evidence only | Manual checklist | Due-diligence turnaround | Unchanged |

The cost effects are far below 1% of the ₹3,000 pilot AI ceiling (DEC-008). Exchange rate and prices must be verified at time of implementation (as of 27 Nov 2026).

#### 2.6.5.9.2 Effort estimate and wave placement (basis: Part 8.1 story-point to person-day ratio and comparable stories)

| Package | Items | Wave | MoSCoW | Effort (person-days, range) | Basis |
|---|---|---|---|---|---|
| Research coverage and playbooks | FR-ENH-A-001…004; BRL-ENH-A-02; RP-ENH-A-01; seed SPB-01…24 data | W1 | Must/Should | 8–13 | 4 stories × 3–5 points; seed data entry 1–2 days by the growth/compliance lead |
| Benchmarks | FR-ENH-A-005, 006; BRL-ENH-A-03, 04 | W1 | Must | 4–7 (engineering) + 3–5 (labelling, non-engineering) | Report generation and gate; labelling 50 records × 13 families at ~3 minutes each ≈ 33 hours across two labellers |
| Channel details | FR-ENH-A-008, 009; BRL-ENH-A-05, 06; race tests | W2–W3 | Must | 4–7 | Enum and effects; threshold job; two race tests |
| Personas, roles and governance | R21 (W5), R11T, R12I, BRL-ENH-A-07…12, training record, bulk preview, hold record | W0–W5 | Must/Should | 9–15 | ABAC rules and tests; delegation grant largest item (5–8 points) |
| Acquisition planning and experiments | FR-ENH-A-010…014; RP-ENH-A-02…04; WAR | W3–W5 | Should | 9–15 | AOP object, experiment registry, two reports, jurisdiction record |
| Website legal disclosure | FR-ENH-A-017 | W3 | Must | 1–2 | One editor block and publication check |
| Relationship timeline | FR-ENH-A-016 | W2 | Should | 3–5 | Projection query and Customer 360 panel |
| Partnership-fit scoring version | FR-ENH-A-007 | W3 (or W6) | Could | 1–2 | Version template only; reuses scoring engine |
| UAT packs and fixtures | FX-A-01…06; TC-ENH-A-034…050 | W3–W5 | Must | 4–6 | QA automation 0.5 FTE (DEC-005) |
| **Total** | | | | **43–72 engineering + 3–5 non-engineering** | Within the Part 0 effort contingency only if Could items move to W6; see note |

**Capacity note.** DEC-005 sets 4.0 engineering FTE for 287–483 person-days. Adding 43–72 person-days pushes the upper bound beyond the 180-day window. Recommendation: deliver Must items in their waves (≈ 26–42 person-days), place Should items according to the Part 8.1 sprint buffer, and defer FR-ENH-A-007 (Could) and the R21 managed-service package to W6 unless a managed-service client is signed. The coordinator decides through a DEC.

#### 2.6.5.9.3 Risks added (extend the Part 8.2 register)

| Risk | Description | Likelihood × impact | Mitigation | Owner |
|---|---|---|---|---|
| RSK-ENH-A-01 | Coverage ledger mistaken for "market coverage" in executive reporting | 3 × 3 | Mandatory wording "known approved sources"; BRL-ENH-A-04 | Product Owner |
| RSK-ENH-A-02 | Managed-service operators leak data between clients | 2 × 5 | One tenant per session, grant scope, audit with grant ID, quarterly access review | Security lead |
| RSK-ENH-A-03 | Experiments run without comparison lead to false conclusions | 3 × 3 | Registry blocks overlap; "descriptive only" label; WAR one change at a time | Growth lead |
| RSK-ENH-A-04 | Labelling effort for benchmarks not available | 3 × 2 | Start with the 3 highest-value families; full population when < 50 | Research lead |
