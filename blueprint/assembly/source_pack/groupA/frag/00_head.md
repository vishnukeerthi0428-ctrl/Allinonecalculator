# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 2 (Batch 2.6), Source Pack Business Domain Enhancements

| Field | Value |
|---|---|
| Document | Application Blueprint · Part 2.6: line-by-line coverage review of source-pack documents 03, 11, 12, 13, 14 and 37 against the blueprint, with enhancements |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | Part 0 (inventory, NFR-001…038, EP-01…EP-21), Part 0A (DEC-001…DEC-065), Part 1 (BR, P01–P16, KPI-01…31), Part 2.1 (FR register), Part 2.2 (WF-01…WF-14), Part 2.3 (BRL, R01–R20, state machines), Part 2.4 (NT, RP-01…30, CFG), Part 2.5 (147 screens), Part 5 (stories), Part 6 (TCs), Part 7 (AG-001…036) |
| Source documents reviewed | 03 End User Personas · 11 Global Market Intelligence & Opportunity Discovery · 12 Digital Marketing & Customer Acquisition Automation · 13 Sales Intelligence & Commercial Conversion · 14 Global Customer, Partner & Account Acquisition Strategy · 37 Sales & Marketing Automation Illustrative Workflow (38-document package; plain-text extraction) |
| Group | **A**: business domain experts |
| Roles applied | Product Owner (lead), Business Systems Analyst, Growth/Marketing Strategist, Sales Operations Lead, UX Researcher; reviewed from the QA Lead, Security/Compliance and FinOps viewpoints |
| Tag ranges used | ASSUMPTION-300…306 · GAP-300…310 · CONFLICT-300…304 · RECOMMENDATION-300…315 |
| New ID families | FR-ENH-A-001…020 · BRL-ENH-A-01…14 · US-<EP>-EA<nn> · TC-ENH-A-001…050 · KPI-ENH-A-01…05 · RP-ENH-A-01…04 · SPB-01…24 · AOP-01…05 · AP-ENH-A-01…12 · personas P17–P20 and variants · roles R21, R11T, R12I |

**How to read this part.** Sections 2.6.1 to 2.6.4 are the audit: what each source document says, what the blueprint already covers, and the programmatic reconciliations. Section 2.6.5 is the main body: the missing content, written at blueprint depth and organized by the blueprint part it extends. Nothing in Parts 0–9 is changed by this part. Every addition is tagged, and every conflict carries a proposed resolution for the coordinator to turn into a binding decision.

**Conventions.** Citations follow Part 0 §0.1.2 (`BRD §n`, `FRD §n`) and add `SP-NN §heading` for the 38-document source pack (for example `SP-11 §Coverage and examples`). The source pack's own optimization KPIs are referred to as **OKPI-01…OKPI-35** to avoid a clash with the blueprint's KPI-01…31. Money is in INR and is an **estimate** unless it is a test fixture. Prices, quotas and provider terms say "verify at time of implementation (as of 27 Nov 2026)".

**Heading-number note.** The coordinator assigned section numbers `2.6.x` to this part. Part 2.2 already uses `## 2.6 Universal execution engine` and `### 2.6.1 Dispatch sequence`. To avoid ambiguity, cross-references in this part always say "Part 2.2 §2.6.1" for the earlier section and "§2.6.x (this part)" for sections here. The collision is reported in §2.6.6.

**Acronyms used in this part.** AOP acquisition operating plan · AP acceptance procedure · CAC customer acquisition cost · CSM customer success manager · EVR evidence record (Part 6.1) · FPO farmer producer organization · KPI key performance indicator · MoU memorandum of understanding · OKPI source-pack optimization KPI · PDP Policy Decision Point · PJ persona journey · RFP/RFQ request for proposal / quotation · SoD segregation of duties · SPB source-family or segment playbook · TTL time to live · UAT user acceptance testing · WAR weekly acquisition review.

---

## 2.6.1 Documents reviewed

All six documents were read line by line. Every table row was also parsed by `assembly/source_pack/groupA_parse.py` (headings, tables, rows and lines). Lines whose text occurs in five or more of the 38 documents were classed as **common core** and are reported once (§2.6.3, "Common core"). The curated aspect register and every reconciliation in this part are produced by `assembly/source_pack/groupA/register.py` and `build.py`, which also write `final/coverage/A_coverage.csv`.

| Doc | Title | Size (bytes) | Headings · tables · rows · text lines | Common-core lines | What the document is trying to tell the team | Atomic aspects |
|---|---|---|---|---|---|---|
| 03 | End User Personas | 33,319 | 44 · 7 · 50 · 261 | 87 | Who uses the product and what each role may and may not do. It lists 21 role personas (owner to agency operator), the typed global filter hierarchy, the separation of website and Admin personas, acceptance owners, training as non-authority, persona journey exercises with a mandatory negative case, UI/UX optimization controls (OPT-14/15) and four new SaaS-era personas | 49 |
| 11 | Global Market Intelligence & Opportunity Discovery | 40,599 | 59 · 7 · 40 · 399 | 87 | How to find opportunities worldwide **lawfully and measurably**: six source classes, a coverage ledger, a nine-step research pipeline, 13 source-family playbooks and 11 MedMaarg segment playbooks, low-cost tooling, a labelled benchmark (50 records per family), a second scoring model, a five-document synthetic proof and data-quality controls OPT-11-01…05 | 69 |
| 12 | Digital Marketing & Customer Acquisition Automation | 34,098 | 45 · 8 · 60 · 307 | 168 | How inbound and outbound acquisition is executed safely: per-channel contracts, reply classes, inbound capability table, 12 marketing capability cards, the 14-row workflow register, deliverability, the opt-out race, experiments and privacy controls OPT-19-01…04 | 57 |
| 13 | Sales Intelligence & Commercial Conversion | 46,323 | 51 · 8 · 44 · 396 | 120 | How interest becomes verified revenue: route-specific state transitions, ten conversion capability cards (entities, APIs, triggers, tool candidates, licence and cost lines), the external conversion interface, provider-neutral documents and payments, milestone invariants, financial fixtures and separate ledgers | 43 |
| 14 | Global Customer, Partner & Account Acquisition Strategy | 53,111 | 77 · 11 · 76 · 562 | 183 | How acquisition is **planned and governed as a business**: per-entity public sites with legal disclosure, cost per verified outcome, an acquisition operating plan per business line with accountable roles, a weekly plan, controlled experiments with stop triggers, outcome economics and cross-border decision records. About 60% of its text repeats documents 11 and 12 verbatim (verified, §2.6.4.3) | 22 |
| 37 | Sales & Marketing Automation Illustrative Workflow | 14,635 | 18 · 9 · 68 · 221 | 7 | A worked end-to-end example to use for design review and UAT: daily control loop, an OrganicSpec distributor journey from discovery to verified receipt with screen hops, multi-startup variants, SaaS onboarding with service arrangements, concurrent automation and exception recovery, a budget fixture, a seven-event relationship ledger and an eight-step demonstration script | 23 |
| — | Common core shared by all 38 documents | — | — | — | Product boundary, independent deployment, two frontends, tenancy, four startup configurations, technology principles, the Website/Admin operating contract, routing namespaces, publication configuration, evidence record, acceptance protocol and current-scope statement | 20 |
| | **Total** | **222,085** | | | | **283** |

**Pattern observed.** Each document is "common core + domain extension + repeated acceptance procedures". The acceptance procedures appear twice in every document (once as "Implementation acceptance and verification" and once as "final decision controls"); they were counted once. Document 14 copies documents 11 and 12 almost entirely and adds about 200 lines of acquisition-strategy content. Most domain content in documents 12 and 13 already reached the blueprint through the BRD and FRD (module catalogue M01–M66, WF-01…WF-14, FR-DM-01…04). The real gaps are in **personas and roles (03)**, **research coverage and benchmarking (11)**, **acquisition planning and experimentation (14)** and **worked UAT fixtures (37)**.
