# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.4c), V12 Executable Workflows: Specifications SM-SVC-21…30

| Field | Value |
|---|---|
| Document | Part 11, Batch 4c of 4: executable specifications of the 40 workflows of SM-SVC-21…30 (121 steps) |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Part 11.4b common contract (registry, DTO v2/v3, executor contracts, envelope v2, triggers, state model v2, scheduler, authority mapping); Part 9.4 catalogue; Parts 2.2, 9.7–9.9 workflow definitions |
| V12 sources | BRD ch09; FSD ch12 entries lines 9,111–12,749; FSD ch13 mapping rows; App. B schemas; workbook rows (generated from `assembly/v12/d_workflows.json` by `d_generate.py`, no retyping) |
| Roles applied | Principal Workflow/BPM Architect, Principal Engineer, QA Architect, Security/AI-Governance Lead, FinOps Lead |

## 11.4.5 Enhancements (part 2 of 3): workflow specifications

**How to read a workflow card.** The upper table gives the V12 contract and its blueprint binding; the step table binds each V12 STEP ID to an NT13 node type (Part 7.4b), a handler (agent, automation or module service), its output contract (Part 11.4b §11.4.5.4–5), the failure route to a run state (§11.4.5.7), the model tier and its after-status. Rows marked "Pending Founder decision" are specified and shipped **disabled** (`implementation_status = disabled_pending_founder`); the PDP denies them with `FOUNDER_DECISION_PENDING` until the Founder decides (§11.4.6). Model-cost estimates use Part 7.3 prices (Haiku 5.5 $0.10/$0.50, Sonnet 5.5 $2.00/$10.00 per million input/output tokens; 1,500/400 tokens per Tier 1a call and 3,000/800 per Tier 1b call; FX ₹90/USD); **verify at time of implementation (as of 27 Nov 2026)**. V12 illustrative costs are quoted literally and exclude provider, retry and labour costs (GAP-831).

**Common to every card (not repeated).** Preconditions and failure handling follow D-F12-030/031 and §11.4b.5; idempotency key, timeouts and retries follow §11.4.5.5.3; every effect is an NT13-13 step through the outbox with the PDP dispatch recheck; simulation creates zero external effects; Tier 2 free models are not eligible for any step in this batch.

{{SERVICES_1}}

## Quality gate: Batch 11.4c

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Each card cites the FSD ch12 line range, App. B `$id` and workbook row; each step keeps its V12 STEP ID |
| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | CONFLICT-814/815/816/819, GAP-824/831, ASSUMPTION-826/827 referenced in cards |
| 3 | IDs unique and consistent | Pass | Generated from parsed data; V12 IDs literal; blueprint IDs from Part 9.4 |
| 4 | No story lacks AC and no requirement lacks a test | Pass | Every workflow maps its 8 or 10 V12 acceptance IDs to TC-V12-D-101…110 and its AT01 to TC-V12-D-111 |
| 5 | Negative, edge, security, accessibility cases | Pass | Failure route per step; conflict steps disabled; R3 capped at L1 |
| 6 | Agents have guardrail, fallback, KPI, cost | Pass | Reused agents keep their Part 7.2/9.7–9.9 cards; per-run model cost given per workflow |
| 7 | Time-sensitive facts flagged | Pass | Model prices flagged "verify (as of 27 Nov 2026)" |
| 8 | No restricted data to free tiers | Pass | Tier 2 not eligible in every card |
| 9 | Consistent with earlier parts | Pass | DEC-064, DEC-383, DEC-387, DEC-391, DEC-395, DEC-397 respected |

**Status: Part 11 Batch 11.4c complete. 40 workflows and 121 steps of SM-SVC-21…30 specified; 9 workflows of SVC-26/27/28 shipped disabled pending the Founder.**
