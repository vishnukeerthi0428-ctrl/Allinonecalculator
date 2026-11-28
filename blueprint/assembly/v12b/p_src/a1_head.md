# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.17), Bounded Mandates, Agentic Commerce and Payments, and Automatic Bid Submission

| Field | Value |
|---|---|
| Document | Part 11, Batch 11.17, file **a of 2**. File a holds §11.17.0–§11.17.6: material reviewed, coverage, the register of superseded positions, the **mandate engine** (object, scope, limits, windows, lifecycle, two-person approval, ledger, PDP recheck, revocation and kill switch, evidence, reconciliation, monitoring and anomaly detection, the L0–L4 controls matrix and the workflow eligibility register) and **agentic commerce and payments** (agent identity, verifiable credentials, counterparty protocol, negotiation bounds, payment execution through a licensed payment service provider, payment-mandate types, spend caps, settlement, refunds, disputes and chargebacks, ledger postings, fraud controls). File b (`Part-11-17b_…`) holds §11.17.7–§11.17.16: automatic bid submission, agents AG-200…209, automations AU-260…279, workflows WF-57…60, screens, entities, APIs, events, audit, STRIDE threat model and abuse cases, stories, tests, AI evaluation cases, the 3-way combinatorial catalogue, effort and cost, decisions, tags and the quality gate |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Part 11.14 DEC-779 (bounded mandates), DEC-780 (agentic commerce and payments), DEC-781 (automatic bid submission), DEC-772 (IN/EU residency), DEC-776 (legal gates per market), DEC-788 (model registry); Part 11.15a (rule-pack framework, strictest-wins precedence, AU-128 loader); Part 11.1b §11.1.5.7 (CONFLICT-762); Part 11.2c (CONFLICT-778, 781; DEC-532, 533); Part 11.3c (CONFLICT-798…800; DEC-548…550); Part 11.4d (CONFLICT-814, 816; DEC-573, 577); Part 11.6b (CONFLICT-854; AG-104, AU-175); Part 2.3 (BRL-APR-01…11, BRL-AUT-01…10, BRL-BID-01…06, BRL-FIN-01…08, roles R01–R20, ABAC-01…12, §2.27.4 bid, §2.27.7 payment, §2.27.14 run, §2.27.15 plan); Part 4.1 (STRIDE method §4.2.1, THR-045…058, step-up §4.3.3, signing §4.5.4, SC-01…); Part 7.3 (§7.6.1 HITL policy, §7.6.2 thresholds, §7.6.11 kill switch ADR-085); DEC-038, DEC-050, DEC-053, DEC-064 |
| V12 source | BRD V12 ch01 (BR-C09), ch08 (SM-SVC-19, SM-SVC-28), ch09, ch16, ch18 (L0–L4, FL-09), ch20; FSD V12 ch11, ch12 (SM-SVC-19-WF03, SM-SVC-28-WF01…04, R2/R3 authority rows), ch13 (approve/dispatch registry), ch15 (external agent interoperability), ch16 (AI-INJ-06, CTRL-AI-08), ch18 (FL-09, effect classes R0–R3, approval record, V6 dual control, MOB-09), ch20 (website fixtures), ch21 (domain panels), ch24 (X28), ch26 (agent_transaction), ch33 (TC families), ch40 (QC-26), App. B (DTO schemas SM-SVC-28-WF01…04) |
| Roles applied | Principal Agent-Safety Architect (delegated authority) · Payments Architect (PSP mandates, UPI AutoPay, RBI e-mandates, card networks, PSD2 SCA) · Public-Procurement and e-Tendering Specialist (GeM, CPPP, EU TED, US SAM.gov) · Fraud and Risk Lead · AI Governance Lead · QA Architect; supported by the shared-brief virtual team (Product Owner, BSA, Data Architect, Security/Compliance, DevOps/SRE, FinOps) |
| ID ranges used | DEC-840…857 · ADR-240…247 · ASSUMPTION/GAP/CONFLICT/RECOMMENDATION-1040…1059 · FR-V12-P-001…150 · AG-200…209 · AU-260…279 · WF-57…60 · US-14-ZP01…, US-15-ZP01…, US-18-ZP01…, US-24-ZP01… · TC-V12-P-001…826 · TC-AI-AG200…AG209 · screens A260…A269 (provisional, [ASSUMPTION-1040]) · KPI-P-01…12 · THR-V12-P-01…30 · ABU-P-01…20 · MC-01…24 (mandate controls) · CoA-P-1xxx (ledger accounts) |
| Precedence | Part 11.14 > this part > Parts 11.1–11.13 for mandates, agentic commerce and bid submission. Where this part and an earlier rule differ, §11.17.4.2 states the amendment |

**Acronyms used in this part.** A2A Agent2Agent protocol · ACP Agentic Commerce Protocol · AFA additional factor of authentication (RBI) · AP2 Agent Payments Protocol · BIC/IBAN bank identifiers (EU) · CoA chart of accounts · CPPP Central Public Procurement Portal (India, eprocure.gov.in) · DID decentralized identifier · DSC digital signature certificate (India, IT Act 2000) · e-NACH electronic National Automated Clearing House mandate (NPCI) · GeM Government e-Marketplace (India) · JWS JSON Web Signature · KMS key management service · MIT merchant-initiated transaction · MND mandate engine (this part) · NPCI National Payments Corporation of India · PA payment aggregator (RBI-authorised) · PAN primary account number (card) · PDP Policy Decision Point · PISP payment initiation service provider (PSD2) · PSD2 EU Payment Services Directive 2 · PSP payment service provider · RBI Reserve Bank of India · SAM.gov US System for Award Management · SCA strong customer authentication (PSD2) · SDD SEPA Direct Debit · SEPA Single Euro Payments Area · SoD separation of duties · TED Tenders Electronic Daily (EU) · UPI Unified Payments Interface · VC verifiable credential (W3C) · VP verifiable presentation.

**Time-sensitive facts.** Every statement about payment-scheme rules (RBI e-mandate framework, AFA thresholds, pre-debit notification, UPI AutoPay limits and categories, e-NACH limits, card-network MIT rules and agentic-token programmes, PSD2/PSR SCA exemptions, SEPA rulebooks, chargeback time limits), agent protocols (A2A, AP2, ACP, MCP, W3C VC 2.0, DID methods), e-procurement portals (GeM, CPPP, national EU eSubmission platforms, TED, SAM.gov, agency portals) and their terms of use, and every price, is **unverified: verify at time of implementation (as of 27 Nov 2026)**. Legal interpretations are proposals for counsel; no capability in this part activates in a jurisdiction before its rule pack is signed off (DEC-776, Part 11.15).

**What this part is.** The Founder adopted V12 bounded mandates, agentic commerce and payments, and automatic bid submission (DEC-779…781), "irrespective of time and cost", **with V12's own conditions and full legal and operational controls** (V12B brief). This part specifies those controls so that a development team can build, test and operate them, and so that no control is optional: every capability is **built** in full, and **activates per jurisdiction only when that jurisdiction's rule pack is approved** ("where lawful"). Nothing in this part allows an AI agent to expand its own authority: an agent acts only inside a mandate that two authorized humans approved, and the deterministic PDP rechecks that mandate at every dispatch.

---

## 11.17.1 Material reviewed

| # | Material | Size / extent | Sections read | Purpose for this part | Pattern | Aspects |
|---|---|---|---|---|---|---|
| 1 | `v12/BRD/18_AI_Automation_Authority_Business_Govern.txt` | V5 FL-01…FL-15 block; authority table | FL-09; L0–L4; R3 default note | Autonomy scale and persistent mandates | Requirement + acceptance rows | 10 |
| 2 | `v12/FSD/18_Policy_Approval_Human_in_the_Loop_Engin.txt` | V5–V7 sections (lines 740–900) | FL-09; SEC-07; effect classes R0–R3; approval record; V6 dual control; MOB-09; MT-15/20/24/32 | Effect classes, approval record binding, dual control | Tables + prose | 10 |
| 3 | `v12/FSD/12_Executable_Workflow_Specification_156_W.txt` | 72 "mandate" hits; SM-SVC-19 (lines 8281–8620); SM-SVC-28 (lines 11968–12370); 31 R2/R3 authority rows | Full workflow blocks SVC-19-WF01…04, SVC-28-WF01…04 | Steps, DTOs, failure paths, KPIs, acceptance IDs | Field table + step table per workflow | 15 |
| 4 | `v12/FSD/11_Master_Functional_Specification_39_Serv.txt` | SM-SVC-19 (lines 770–800), SM-SVC-28 (1136–1180) | Service blocks | Provider prerequisites, channels, operating mode | Field table | 3 |
| 5 | `v12/BRD/08_Master_Automation_Service_Catalogue_39.txt` | SM-SVC-19 (1190–1200), SM-SVC-28 (1618–1670) | Full service rows | Business acceptance, risk/limits, meter | Field table | 4 |
| 6 | `v12/BRD/01`, `BRD/16`, `BRD/20`, `BRD/09` | Lines with "mandate", "AI-to-AI" | BR-C09; ch16 intro; workflow catalogue rows | Business boundary statements | Prose / rows | 2 |
| 7 | `v12/FSD/13_Workflow_Step_Trigger_Event_Registry.txt` | Stage table (lines 55–85) | Approve "Exact digest + mandate"; Dispatch; Reconcile | Prepare/approve/dispatch/reconcile separation | Table | 1 |
| 8 | `v12/FSD/15_AI_Agent_Registry_Orchestration.txt` | V5 note (line 165) | External agent interoperability | Interop gate | Prose | 1 |
| 9 | `v12/FSD/16_AI_Models_Prompts_Evaluation.txt` | §16.5 AI-INJ table; CTRL-AI-01…09 | AI-INJ-06; CTRL-AI-08 | Counterparty injection and signed limits | Tables | 2 |
| 10 | `v12/FSD/20`, `FSD/21`, `FSD/24`, `FSD/26`, `FSD/33`, `FSD/40`, `FSD/AP_Appendix_B` | Fixtures, domain panels, X28, agent_transaction schema, TC families, QC-26, DTO JSON schemas | Rows naming SVC-28, SVC-19-WF03, SVC-14-WF02, SVC-39-WF03 | UI fields, data fields, tests, schemas | Rows | 16 |
| 11 | Blueprint Parts 11.1b, 11.2c, 11.3c, 11.4d, 11.6b, 11.14 | Conflict tables and proposed resolutions | CONFLICT-762, 778, 781, 798…800, 814, 816, 854; DEC-779…781 | Positions superseded by the Founder | Conflict rows | — |
| 12 | Blueprint Parts 2.3, 4.1, 7.3, 0A, 5.1a/b, 6.2a, 6.4, 11.15a | Rules, roles, state machines, STRIDE, HITL policy, templates, rule-pack framework | As cited | Baseline rules and templates followed exactly | — | 9 (amended rules) |
| | **Total atomic aspects** | | | | | **64** |

The aspect inventory is generated by `assembly/v12b/p_coverage.py` and written to `final/coverage_v12/P_coverage.csv` (columns `doc,chapter,section,aspect_id,aspect_summary,status_before,blueprint_location,action,new_ids,status_after`). The combinatorial models are generated by `assembly/v12b/p_combinatorial.py` (§11.17.14). Repeated V12 boilerplate (FSD-POL-V6-PRECHECK, the common eight-test TC family) is listed once per workflow.

## 11.17.2 Coverage summary

| Status | Before this part (after DEC-779…781 were recorded, before specification) | After this part |
|---|---|---|
| Covered | 13 | — |
| Partially covered | 25 | — |
| Not covered | 3 | — |
| Conflict (now decided by the Founder: DEC-779/780/781) | 23 | — |
| **Matched** | — | **64** |
| Pending Founder decision | — | **0** (the Founder decided all three capabilities; activation per jurisdiction is a legal gate, not a pending decision) |
| Not applicable | — | 0 |
| **Total** | **64** | **64** |

**Reading the result.** Before this part, the blueprint either refused these capabilities (the safety invariant "consequential actions capped at L1", DEC-064, DEC-053, BRL-AI-07, BRL-BID-04, X-06) or kept them as designed-but-disabled shells (AG-104, AU-175, A172). The 23 conflict aspects are the V12 statements that those positions blocked. This part turns each into a specified, testable control set. Activation remains gated per jurisdiction by counsel-approved rule packs (§11.17.5.15; the payment, agentic-contracting and e-procurement packs are not yet in Part 11.15 [GAP-1044]).

## 11.17.3 Detailed register

Every aspect is listed individually (covered aspects included, because the register is short).

<!--INCLUDE:p_frag2/coverage_register.md-->

## 11.17.4 Reconciliation of superseded positions

### 11.17.4.1 Conflict rows closed by this part

| Conflict | Raised in | Position recommended before the Founder decision | Founder decision | What this part specifies instead | Section |
|---|---|---|---|---|---|
| CONFLICT-762 | Part 11.1b §11.1.5.7 | Keep the invariant; V12-L3 only for the DEC-064 routine class; L4 internal only | DEC-779 | Full L0–L4 controls matrix; L3 under an Active bounded mandate for any effect class where the eligibility register and the jurisdiction pack allow it; L4 bound to an L3 mandate and unable to expand it | §11.17.5.2, §11.17.5.14 |
| CONFLICT-778 | Part 11.2c | Mandate bounds negotiation only; human approval per transaction; no AI-initiated payment (DEC-532) | DEC-780 | Negotiation and payment under MT-COM and MT-PAY mandates; execution only through a licensed PSP; per-transaction and per-period caps; counterparty allowlist; signed identity and VCs; reconciliation; disputes | §11.17.6 |
| CONFLICT-781 | Part 11.2c | Human submission on every portal (DEC-533, BRL-V12-B-04) | DEC-781 | Per-tender MT-BID mandate; automatic submission of the exact approved package hash where the portal capability registry and the pack permit it; otherwise assisted or manual submission | §11.17.7 (file b) |
| CONFLICT-798 | Part 11.3c | Keep ≤ L1 for R3; disable the L3 path by flag (DEC-548) | DEC-779 | L3 path enabled per workflow in the eligibility register; R3 mandates need a Finance or Legal approver (MC-07) | §11.17.5.6, §11.17.5.14 |
| CONFLICT-799 | Part 11.3c | Mandate only for DEC-064 L3 categories (DEC-549) | DEC-779 | All 12 R2 workflows eligible for MT-OUT mandates; consent, suppression, quiet hours and the 09:00–21:00 window (DEC-777) still rechecked per message | §11.17.5.14 |
| CONFLICT-800 | Part 11.3c | Step 04 = human submission task (DEC-550) | DEC-781 | WF-60 step 04 = mandated submission through a portal adapter, with the deadline guard and receipt verification | §11.17.7 |
| CONFLICT-814 | Part 11.4d | (b)+(c): L1 per item; record-only steps at L3 (DEC-577) | DEC-779 | 10 R3 workflows (SVC-21-WF01/02, 28-WF03/04, 30-WF02, 31-WF02/03, 32-WF04, 37-WF03, 39-WF03) eligible for typed mandates | §11.17.5.14 |
| CONFLICT-816 | Part 11.4d | Catalogue and quote drafts only (DEC-573) | DEC-780 | SVC-28 WF01–WF04 specified end to end (WF-59) | §11.17.6 |
| CONFLICT-854 | Part 11.6b | Bounded R2 mandates only; R3 mandates disabled; payment mandate not supported; interop OFF | DEC-779, DEC-780 | Mandate engine with R2 and R3 types; payment mandates; external agent interoperability ON per tenant after the interop gate FR-V12-P-076 | §11.17.5, §11.17.6 |

The earlier "Pending Founder decision" DECs DEC-532, 533, 548, 549, 550, 572 (voice, not this part), 573 and 577 are **closed** by DEC-779…781 and superseded by DEC-840…857 of this part for the implementation detail.

### 11.17.4.2 Amendments to earlier rules (exact replacement wording)

Earlier parts are not edited (brief boundary). The rules below are read with this amendment from the date of this part.

| Rule | Earlier text (abridged) | Amended reading (binding) | Authority |
|---|---|---|---|
| DEC-064 / BRL-AUT-01 | Money movement unsupported; quotes, discounts, contracts, legal terms, bid submissions ≤ L1 | **Unchanged for any action not covered by an Active mandate.** An action covered by an Active, in-scope, in-window, within-cap mandate of an eligible type (§11.17.5.14) in a jurisdiction whose pack is Approved may execute at V12-L3 (or under a V12-L4 plan bound to that mandate). Money movement is supported **only** through a licensed PSP under an MT-PAY mandate | DEC-779, DEC-780; DEC-841 |
| BRL-AI-07 | AI cannot approve, sign, submit, pay, change price/terms or alter permissions | **AI still never approves anything and never alters permissions or mandates.** Under an Active mandate, the *deterministic* executor (not the model) may submit, pay or accept terms that the mandate's bounds already fix; the model only extracts, classifies and drafts wording. Signing with a legal signature remains human unless the jurisdiction pack and the portal allow an organisational signer certificate (§11.17.7.5) | DEC-779…781; DEC-847 |
| BRL-BID-04 / DEC-053 | Submission is performed by a human outside the system | Human submission remains the default (L1). Under an Active MT-BID mandate whose approved package hash equals the sealed package, the system submits through a permitted portal adapter and records the receipt; otherwise assisted (L2) or manual (L1) submission applies | DEC-781; DEC-851 |
| BRL-BID-01 | Submission blocked at or after (deadline − buffer); default buffer 24 h; minimum 2 h | Applies to **automated** attempts: the deadline guard (AU-278) forbids a first automated attempt inside the automation buffer (default 6 h, minimum 2 h) and any automated retry inside the hard-stop buffer (default 2 h). A human may still submit on the portal at any time before the deadline; the system records the evidence | DEC-852 [ASSUMPTION-1053] |
| BRL-FIN-07 | No storage of card data or bank credentials | **Unchanged and reinforced:** the platform stores only PSP tokens, mandate references (UMRN, UPI mandate ID, SDD mandate reference) and masked instrument hints; never a PAN, CVV, UPI PIN or bank login | DEC-848 |
| BRL-APR-07 | Payment verification and invoice approval require two different Finance users | Exact automated matches of PSP settlement to an MT-PAY transaction close without manual verification; any mismatch, partial, duplicate or unknown-outcome item goes to Finance maker-checker exactly as before [CONFLICT-1048, resolved] | DEC-849 |
| X-06 (Part 11.6b) | Payments never | Payments only through a licensed PSP under an MT-PAY mandate; the model never initiates a payment call (tool isolation CTRL-AI-04) | DEC-780; DEC-848 |
| DEC-388 / DEC-395 | AI never proposes or computes a price; approved price books only | Numbers in a negotiation are produced by the deterministic negotiation bound engine (AU-271) from the human-approved bounds and price book; the model writes wording only and cannot introduce a number [CONFLICT-1047, resolved] | DEC-847 |
| Part 7.3 §7.6.1 "Never automated, at any mode" | Money movement, payment verification, signing, tender submission, quotes/prices beyond approved versions | Read with "…except by the deterministic executor under an Active mandate of an eligible type, in an approved jurisdiction, after the PDP recheck (Part 11.17)". Payment *verification* of mismatches, permission changes, configuration loosening and mandate approval remain never automated | DEC-841 |

