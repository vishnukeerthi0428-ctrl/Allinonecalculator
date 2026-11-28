# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.1a), V12 Business Requirements (BRD chapters 01–07 and 10–25): Review, Coverage and Catalogue Reconciliation

| Field | Value |
|---|---|
| Document | Part 11, Batch 1a (Part 11.1a). Continued in Part 11.1b (enhancements, conflicts, decisions, persona review, tags, quality gate) |
| Version | 1.0 · 28 Nov 2026 |
| Purpose | Line-by-line review of the customer's **BRD V12** business chapters (front matter, reading guide, chapters 01–07, 10–25 and the ID-index appendix) against the blueprint; an atomic aspect inventory; status before and after; catalogue reconciliation; the full enhancement set to reach a 100% match (Part 11.1b) |
| Authority | Customer revision V12 (28 Nov 2026). Under the V12 brief, V12 wording, numbers and IDs are adopted by default and amend earlier blueprint text and decisions, **except** where they meet a Founder decision (DEC-002, DEC-228, DEC-230/231/422, DEC-418, DEC-420, DEC-421) or a safety invariant: those items are raised as `[CONFLICT-###]` and recorded "Pending Founder decision". Earlier parts are not edited; the decisions in §11.1.7 amend them |
| Baseline | Parts 0–9.10 and Part 0B (346 decisions DEC-001…422; 80 agents, 119 automations, 38 workflows; 147 + 71 screens; precedence DEC-415). Approved budgets unchanged: Ledger A DEC-230, Ledger B re-based by DEC-422 (₹26,105–35,362/month pilot running). Hosting DEC-421 (Vercel + Supabase + AWS ap-south-1). Claude Sonnet primary DEC-418 |
| Material | `scratchpad/v12/BRD/00_*`, `01_*`…`07_*`, `10_*`…`25_*`, `AP_Appendix_ID_index.txt` (25 files, 4,465 lines, 202,960 bytes). Excluded by allocation: chapter 08 (Group B), chapter 09 (Groups C/D), `ZZ_Historical_annex` (Group L) |
| Scripts | `assembly/v12/a_parse_brd.py` (aspect inventory), `assembly/v12/a_classify.py` (status rules, CSV), `assembly/v12/a_register_md.py` (this register) |
| Register | `final/coverage_v12/A_coverage.csv` (1,310 rows; columns `doc,chapter,section,aspect_id,aspect_summary,status_before,blueprint_location,action,new_ids,status_after`) |
| ID ranges used | Tags 760–777 · DEC-500…519 · ADR-180…184 · FR-V12-A-### · US-&lt;EP&gt;-YA&lt;nn&gt; · TC-V12-A-### · local family KPI-V12-A-## (business and AI/compliance metrics, [ASSUMPTION-772]) |
| Roles applied | Chief Product Officer (B2B SaaS, lead) · Principal Business Systems Analyst · SaaS monetization and pricing strategist · Head of Governance, Risk and Compliance (DPDP/GDPR) · Customer Success executive; consulted: Solutions Architect, FinOps Lead, QA Lead |

**Acronyms used in this part.** ABM account-based marketing · ACR accessibility conformance report · BYO bring your own · BYOK bring your own key · CAC customer acquisition cost · CASL Canada's Anti-Spam Legislation · CES customer effort score · CSAT customer satisfaction · DLT distributed ledger technology (TRAI telemarketing registration) · DPA data processing agreement · DPDP Digital Personal Data Protection Act 2023 (India) · DPIA data protection impact assessment · DSAR data-subject access request · ENT enterprise requirement (V12) · FX foreign exchange · GA general availability · GRR gross revenue retention · IdP identity provider · IRN invoice reference number (GST e-invoice) · LGPD Lei Geral de Proteção de Dados (Brazil) · LTV lifetime value · MRR monthly recurring revenue · NRR net revenue retention · OSS One-Stop Shop (EU VAT) · PDPL Personal Data Protection Law (UAE) · PLG product-led growth · RCTCFE the customer's weighted evaluation rubric · ROAS return on ad spend · RTL right-to-left · SCIM System for Cross-domain Identity Management · SEV severity · SIEM security information and event management · SKU stock-keeping unit (here: a sellable automation service) · SoD separation of duties · SSO single sign-on · TCO total cost of ownership · TCPA Telephone Consumer Protection Act (US).

**How V12 is layered.** Every BRD chapter stacks version sections (V12 → V11 → V10 → V9 → V8 → V7 → V6 → V5 → V4). The reading guide (chapter 00) and chapter 01 state that the active V12 sections are authoritative and earlier sections stay normative unless superseded (`00_Reading_guide`, `01 §V10`). This review therefore treats every version section as an aspect source, folds exact repeats (10 folded), and marks superseded inventories, artifact checksums, self-scores and prototype evidence as *Not applicable* with the reason stated.

---

## 11.1.1 Material reviewed

### 11.1.1.1 Files

| File | Lines | Bytes | Headings | Version sections present | Purpose | Pattern | Aspects |
|---|---|---|---|---|---|---|---|
| `00_front.txt` | 9 | 874 | 0 | V12 | Title page and status line (39 / 156 / 25 / 15; 233 + 65 ENT requirements; 23 + 10 jurisdiction rules) | Prose | 10 |
| `00_Reading_guide_and_chapter_navigation.txt` | 27 | 1,852 | 1 | V10 | Reading order; 25 chapter titles | Prose list | 26 |
| `01_Executive_Summary_Product_Vision.txt` | 896 | 36,137 | 16 | V12, V11, V10, V9, V8, V7, V6, V5 | Baseline inventory, enterprise readiness by area, change history (C1–C8, D1–D15), promotion P1–P9, BR-V3-01…14, BR-C01…15 | Tables + prose | 210 |
| `02_Business_Objectives_Success_Criteria.txt` | 22 | 1,324 | 2 | V5 | BR-OBJ-01…05; pilot outcome hypotheses | Table + prose | 6 |
| `03_Market_Positioning_Competitive_Strategy.txt` | 23 | 779 | 1 | — | Positioning; four segments with pilot evidence | Table | 5 |
| `04_Stakeholders_Personas_Customer_Segmenta.txt` | 113 | 5,029 | 6 | V10, V9, V6 | REC-07; journey patterns; P-01…06; 14 customer types (MT-04); actor table; ICP | Tables | 24 |
| `05_SaaS_Business_Commercial_Operating_Mode.txt` | 83 | 3,084 | 3 | V12, V5 | BR-V12-01…10; AT-15; lifecycle and delivery models | Tables | 16 |
| `06_Multi_Tenant_Multi_Company_Business_Arc.txt` | 39 | 5,115 | 9 | V7, V6, V5 | MOB-01; tenant/organization/company/portfolio model; MT-01, 05, 07, 33; GC-01, 02, 12 | Requirement blocks | 11 |
| `07_Universal_Business_Configuration_Onboar.txt` | 177 | 12,701 | 20 | V10, V7, V6, V5, V4 | REC-04; MOB-04, 11, 16; MT-03, 08…11, 15, 17…19, 29; SEC-05, FL-12, CV-01/02; journey; configuration groups; canonical application SM-APPLICATION-4 | Requirement blocks + tables | 43 |
| `10_Subscription_Bundle_Entitlement_Model.txt` | 94 | 6,004 | 7 | V6, V5 | MT-06, 16, 30; RT-07, RT-11, CV-12, CV-13; subscription rules; commercial lifecycle decisions | Requirement blocks + tables | 24 |
| `11_Pricing_Billing_Commercial_Unit_Economi.txt` | 410 | 20,037 | 9 | V9, V7, V6, V5 | Plugin economics; MOB-13, 15; MT-14, 21; AI-01…15; GC-03…15; CV-05; CS-14; cost formulas; 39 SKU meters | Requirement lines + tables | 93 |
| `12_Public_SaaS_Website_Customer_Acquisitio.txt` | 314 | 13,861 | 7 | V8, V7, V5, V4 | BR-V7-WEB/ADM; MOB-02, 03; AT-01…14; CV-03…15; W01…W34 neutral route list | Tables + requirement lines | 71 |
| `13_Market_Intelligence_Lead_Generation.txt` | 32 | 1,361 | 3 | V6 | MT-13; SKU 01–05 outcomes | Table | 6 |
| `14_Digital_Marketing_Omnichannel_Engagemen.txt` | 73 | 3,394 | 4 | V6 | MT-22, 23; SKU 06–16, 26, 27, 38 outcomes | Table | 17 |
| `15_Sales_Intelligence_Revenue_Conversion.txt` | 54 | 2,003 | 2 | V10 | REC-28; SKU 17–21, 24, 29, 36, 37 | Table | 11 |
| `16_Commerce_Procurement_Partner_Operations.txt` | 23 | 999 | 1 | — | SKU 28, 31, 32, 39 | Table | 5 |
| `17_Customer_Success_Retention_Product_Led.txt` | 196 | 13,213 | 8 | V10, V7, V5 | REC-25, 27; delivery stages; MOB-05, 14, 17; RT-01…15; CS-01…13; SKU 22, 23, 25, 30, 33…35 | Requirement lines + tables | 45 |
| `18_AI_Automation_Authority_Business_Govern.txt` | 196 | 11,682 | 11 | V10, V8, V7, V6, V5 | REC-01, 03, 09, 11, 12; BR-V7-AI-01…08; MOB-09; MT-12, 28, 32, 35; FL-01…15; authority L0–L4 | Tables + requirement lines | 40 |
| `19_Portfolio_Command_Centre_Business_Analy.txt` | 212 | 11,140 | 14 | V10, V7, V6, V5, V4 | REC-02, 06, 13…15; MOB-06…08; MT-02, 25, 26; 14 views; 9 optimization perspectives | Tables + requirement blocks | 48 |
| `20_Business_Security_Privacy_Compliance.txt` | 526 | 21,591 | 13 | V12, V10, V9, V8, V7, V6, V5 | 10 V12 draft market rules; REC-10; CJ-GL-01…13; BR-V7-CJ-01…12; CJ-IN-01…11; CJ-EU-01…10; CJ-UK-01; CJ-US-01; MOB-10; MT-20, 24; SEC-01…15; CS-15 | Tables | 91 |
| `21_SLA_Support_Service_Delivery.txt` | 227 | 11,780 | 8 | V12, V10, V9, V7, V5 | ENT-OPS-01…07; REC-22…24, 26; alert review; recovery objectives; MOB-12; ST-01…15; CS-03, 10, 11; service obligations | Tables + requirement lines | 48 |
| `22_Business_KPI_Performance_Framework.txt` | 387 | 8,785 | 10 | V10, V9, V8, V6, V5 | REC-16; 20-dimension scorecard; KPI-01…35; 7 AI/compliance KPIs; MT-27, 31, 40; metric definitions; 12 business KPIs | Tables | 83 |
| `23_Roadmap_Prioritization_Commercial_Readi.txt` | 139 | 4,767 | 7 | V12, V10, V9, V6, V5 | R0…R5; REC-20, 21; GO-01…08; MT-39; P0/P1/P2; release gates | Tables | 28 |
| `24_Business_Acceptance_Requirement_Traceab.txt` | 1,373 | 34,422 | 20 | V12, V11, V10, V9, V8, V7, V6, V5, V4 | Readiness; RCTCFE scores; REC-17…19; E-001…007; XS-01…10; MOB V8 log; BR-V7 traceability; V8-QA-001…071; MT-36…38; 39 SKU entitlement tests; V4 browser record | Tables | 299 |
| `25_Decision_Register_Migration_Source_Appe.txt` | 244 | 7,227 | 7 | V12, V11, V10, V9, V8 | DEC-V12-01…07; DEC-V11-01, 02; REC-30; DEC-V9-01…04; DEC-V7-01…08; old REC series; decision ownership | Tables | 38 |
| `AP_Appendix_ID_index.txt` | 54 | 906 | 1 | — | 12 ID families and ranges | Table | 12 |
| **Total (25 files)** | **4,465** | **202,960** | **185** | | | | **1,310** |

### 11.1.1.2 Aspect inventory method

1. **Parse.** `a_parse_brd.py` reads every line. Every table row except the header becomes one aspect (`table_row`, 979); every `<Heading3>` requirement block (MT-, MOB-) and every optimization requirement line group (`AT-15 · P1 · …` + Requirement + Acceptance + Owner) becomes one aspect (`requirement`, 192); every other non-empty line becomes one aspect (`paragraph`, 139). Exact repeats across version sections (for example the "Commercial unit rule" sentence and repeated checksum rows) are folded once with a repeat count (10 folded).
2. **Key.** A row whose first cell is a source ID (BR-, MT-, MOB-, REC-, CJ-, KPI-, DEC-, ENT-, SM-SVC-, GO-, XS-, E-, P-, V8-QA-, AT-/RT-/CV-/CS-/SEC-/ST-/FL-/GC-/AI-) keeps that ID as `aspect_id`; where the same source ID appears in more than one chapter the chapter is appended (`BR-C01@20`). Other aspects receive `A-<chapter>-<seq>`.
3. **Classify.** `a_classify.py` applies 281 ordered rules. Each rule cites the blueprint location found by searching Parts 0–9.10 (for example DEC-047, BRL-SVC-03, Part 8.3c CSO-01…12) and states the action and the new IDs. Conflicts with Founder decisions and safety invariants are evaluated first.
4. **Count.** 1,310 aspects: 503 Covered, 352 Partially covered, 135 Not covered, 92 Conflict, 228 Not applicable (reasons stated).

### 11.1.1.3 Artifact identities recorded (V12)

| Artifact | SHA-256 (as stated in BRD chapter 01 and 24) |
|---|---|
| `commercial_website_desktop_V12.html` | b9c3fa5cad677a9268d4124ad93679574579fe63dc8952d7d6fb5ba5236c60e2 |
| `commercial_website_mobile_V12.html` | 84c748e298ddb27104565667398b57ef24a33230365ed3f09f6b83aac95754b3 |
| `commercial_admin_desktop_V12.html` | 2801359a3d598d51e5b5bc44737f712a8171252cb6f4379e66bb82d98f4dade0 |
| `commercial_admin_mobile_V12.html` | 5995a670fd635d2795e479240e3bd5e633e1b1df601ef55c10faceb30a0a7e2c |

The customer's own weighted RCTCFE score (V12 8.54 / 10; BRD V12 8.6, FSD V12 8.8) is a self-assessment of the customer's documents and prototypes. It is recorded here and is not a product requirement. The BRD states plainly that V12 "is still a specification and a prototype" and that certifications, legal approvals, live integrations, drills and customer operations are earned during R0–R5 (`01 §V12 Honest boundary`). The blueprint adopts that boundary: no V12 statement is treated as production evidence.

---

## 11.1.2 Coverage summary

### 11.1.2.1 Overall

| Status | Before | After |
|---|---|---|
| Covered → **Matched** | 503 | — |
| Partially covered (352) → enhanced → **Matched** | 324 | — |
| Not covered → enhanced → **Matched** | 135 | — |
| Conflict → adopted (V12 governs; earlier decision amended) → **Matched** | 60 | — |
| Conflict → **Pending Founder decision** | 32 | — |
| Partially covered, delivery needs funding beyond approved budgets → **Pending Founder decision** | 28 | — |
| **Matched** | — | **1,022** |
| **Pending Founder decision** | — | **60** |
| **Not applicable** (reason recorded per row) | 228 | 228 |
| **Total** | **1,310** | **1,310** |

Matched + Not applicable = 1,250 of 1,310 (95.4%); with the Founder-pending rows every aspect has a recorded end state. The 60 Pending Founder rows group into four conflicts: enterprise-readiness scope versus approved budgets and staffing (CONFLICT-760, 38 rows, including the R1/R2/R4/R5 phase rows under ASSUMPTION-770, the cost proposal RECOMMENDATION-775 and the connector-timing conflict CONFLICT-776), the V12 autonomy scale L0–L4 and bounded mandates versus the L1 cap on consequential actions (CONFLICT-762, 10 rows), EU and multi-region residency versus DEC-421 (CONFLICT-761, 8 rows) and the 2-hour growth recovery objective versus its running cost (CONFLICT-765, 4 rows). Each has a recommended resolution in Part 11.1b §11.1.6.

### 11.1.2.2 By chapter

The table counts aspects by status **before** (Covered, Partial, Not covered, Conflict, N/A) and **after** (Matched, Pending Founder, N/A).

| Ch | Chapter | Aspects | Covered | Partial | Not covered | Conflict | N/A | **Matched** | **Pending Founder** | **N/A after** |
|---|---|---|---|---|---|---|---|---|---|---|
| 00 | Front matter and reading guide | 36 | 0 | 4 | 0 | 0 | 32 | 4 | 0 | 32 |
| 01 | Executive Summary Product Vision | 210 | 25 | 55 | 11 | 11 | 108 | 92 | 10 | 108 |
| 02 | Business Objectives Success Criteria | 6 | 0 | 6 | 0 | 0 | 0 | 6 | 0 | 0 |
| 03 | Market Positioning Competitive Strategy | 5 | 0 | 5 | 0 | 0 | 0 | 5 | 0 | 0 |
| 04 | Stakeholders Personas Customer Segmenta | 24 | 21 | 1 | 2 | 0 | 0 | 24 | 0 | 0 |
| 05 | SaaS Business Commercial Operating Mode | 16 | 3 | 13 | 0 | 0 | 0 | 6 | 10 | 0 |
| 06 | Multi Tenant Multi Company Business Arc | 11 | 5 | 1 | 0 | 5 | 0 | 11 | 0 | 0 |
| 07 | Universal Business Configuration Onboar | 43 | 6 | 26 | 11 | 0 | 0 | 43 | 0 | 0 |
| 10 | Subscription Bundle Entitlement Model | 24 | 6 | 12 | 6 | 0 | 0 | 24 | 0 | 0 |
| 11 | Pricing Billing Commercial Unit Economi | 93 | 40 | 7 | 45 | 0 | 1 | 92 | 0 | 1 |
| 12 | Public SaaS Website Customer Acquisitio | 71 | 15 | 19 | 0 | 36 | 1 | 70 | 0 | 1 |
| 13 | Market Intelligence Lead Generation | 6 | 0 | 6 | 0 | 0 | 0 | 6 | 0 | 0 |
| 14 | Digital Marketing Omnichannel Engagemen | 17 | 1 | 16 | 0 | 0 | 0 | 17 | 0 | 0 |
| 15 | Sales Intelligence Revenue Conversion | 11 | 2 | 9 | 0 | 0 | 0 | 11 | 0 | 0 |
| 16 | Commerce Procurement Partner Operations | 5 | 0 | 4 | 0 | 1 | 0 | 4 | 1 | 0 |
| 17 | Customer Success Retention Product Led | 45 | 20 | 23 | 2 | 0 | 0 | 45 | 0 | 0 |
| 18 | AI Automation Authority Business Govern | 40 | 23 | 10 | 0 | 7 | 0 | 33 | 7 | 0 |
| 19 | Portfolio Command Centre Business Analy | 48 | 7 | 37 | 0 | 0 | 4 | 44 | 0 | 4 |
| 20 | Business Security Privacy Compliance | 91 | 60 | 22 | 1 | 8 | 0 | 88 | 3 | 0 |
| 21 | SLA Support Service Delivery | 48 | 36 | 8 | 2 | 2 | 0 | 45 | 3 | 0 |
| 22 | Business KPI Performance Framework | 83 | 66 | 16 | 0 | 1 | 0 | 82 | 1 | 0 |
| 23 | Roadmap Prioritization Commercial Readi | 28 | 12 | 8 | 0 | 8 | 0 | 20 | 8 | 0 |
| 24 | Business Acceptance Requirement Traceab | 299 | 140 | 34 | 41 | 2 | 82 | 208 | 9 | 82 |
| 25 | Decision Register Migration Source Appe | 38 | 15 | 10 | 2 | 11 | 0 | 30 | 8 | 0 |
| AP | Appendix: ID index | 12 | 0 | 0 | 12 | 0 | 0 | 12 | 0 | 0 |
| **Total** | | **1310** | **503** | **352** | **135** | **92** | **228** | **1022** | **60** | **228** |

---

## 11.1.3 Detailed register

**Reading the register.** Partially covered, Not covered and Conflict aspects are listed one per row with the V12 wording abridged to 150 characters (the CSV holds 300). Covered and Not applicable aspects are grouped per chapter with their blueprint locations or reasons. "New IDs" point to the enhancements in Part 11.1b §11.1.5 (FR-V12-A-###), the decisions in §11.1.7 (DEC-500…519), the ADRs (ADR-180…184) and the tags in §11.1.9. A row ends **Matched** when the enhancement or decision closes it; **Pending Founder decision** when it meets a Founder decision or a safety invariant. *(v1.2: every item counted here as "Pending Founder decision" was adopted by DEC-770…791 — Part 11.14; read as Adopted. Part 11.25.)*


#### 11.1.3.00 Chapter 00: Front matter and reading guide

**Not applicable (grouped, 32):** 26 × chapter navigation; 6 × title page.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| A-00-0001 | V10 reading order: chapter 01 V10 release baseline, V10 sections in active master chapters, then compatible V9/V8/V7 requirements and Appendices A–D.… | Partially covered | DEC-415; Part 0B | V12 inventory and reading order | DEC-500 | Matched |
| A-00-0031 | VERSION 12.0 • 28 NOVEMBER 2026 • 2031 HORIZON | Partially covered | DEC-415; Part 0B | V12 inventory and reading order | DEC-500 | Matched |
| A-00-0033 | Universal multi-tenant, multi-business, multi-product, multi-country, omnichannel platform. Neutral public SaaS storefront; private customer operatio… | Partially covered | DEC-415; Part 0B | V12 inventory and reading order | DEC-500 | Matched |
| A-00-0034 | Status: V12 enterprise-readiness baseline. 233 controlled requirements + 65 enterprise requirements (ENT), 30 reconciliation actions, 35 release KPIs… | Partially covered | DEC-415; Part 0B | V12 inventory and reading order | DEC-500 | Matched |

#### 11.1.3.01 Chapter 01: Executive Summary Product Vision

**Covered (grouped, 25):** P1@01, P2@01, P3, P4, P5, P6, P7, P8 → OKPI; PERF; BR-M; Part 8.2 GO; PEN; Part 7.4 VND; E-001; TRN; A-01-0158, A-01-0159, A11Y, D10, D11, D14, D15 → BRL-APR-01; UI states; WCAG; DEC-027; Part 4.1; Part 7; BR-C05@01, BR-C06@01, BR-C11@01, BR-C13, BR-C14@01 → PDP; RLS; BR-M18/19; Part 8.2; DEC-058; C3, C7 → DEC-518; A-01-0177 → DEC-002; DEC-058; X-01; BR-V3-14 → Part 8.2 gates; BR-C08 → DEC-052. All Matched.

**Not applicable (grouped, 108):** 23 × provenance record; 6 × prototype defect fixed by customer; 55 × superseded historical inventory; V12 inventory governs; 13 × customer document/prototype change history; 11 × artifact checksum.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| A-01-0037 | V12 adds every ingredient that global enterprise SaaS needs — identity federation, governed access, a developer platform, data control, integrations,… | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| A-01-0038 | Honest boundary. V12 is still a specification and a prototype. Enterprise grade is earned in production: certifications, legal approvals, live integr… | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| A-01-0039 | Commercial unit rule. 39 service SKUs are sold; 156 workflows are included under their parent SKU and never sold separately. | Conflict | DEC-047 | 39 SKUs sold; 156 workflows included | DEC-501; CONFLICT-767 | Matched |
| A-01-0040 | V12 inventory: Service SKUs / workflows / steps / Verified count: 39 / 156 / 517 | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0041 | V12 inventory: Website routes / Admin screens (each on desktop and mobile) / Verified count: 41 / 153 (W37–W41 and A122–A131 added) | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0042 | V12 inventory: Requirements / Verified count: 233 controlled + 65 enterprise (ENT) + 10 BR-V12 business requirements | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0043 | V12 inventory: Jurisdiction rules / Verified count: 23 (IN, EU, UK/US placeholders) + 10 draft rules for US, UK, CA, AU, SG, AE, BR | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0044 | V12 inventory: API operations / Verified count: 282 (Appendix A) + 48 enterprise (Appendix A2) — OpenAPI 3.1 validated | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0045 | V12 inventory: Database tables / Verified count: 118 (Appendix C) + 19 enterprise (Appendix C2) — applied and tested on PostgreSQL 16 | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0046 | V12 inventory: Locales in prototype / Verified count: English, Hindi, German, French, Arabic (RTL) on navigation, home and footer | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0047 | V12 inventory: V12 browser checks / Verified count: 77 regression + 36 enterprise = 113, all pass | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0048 | V12 inventory: Automated accessibility / Verified count: 0 WCAG 2.1 A/AA violations on all builds and in all five languages | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0049 | V12 inventory: Weighted RCTCFE score / Verified count: 8.54 / 10 (12/10 aspirational; production gate open) | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0050 | Area: Product functionality (39 services / 156 workflows) / Specified: Yes / Prototype-demonstrated: Yes (simulated) / Production-proven: No | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| A-01-0051 | Area: Multi-tenant isolation / Specified: Yes (DDL + RLS tested) / Prototype-demonstrated: Yes / Production-proven: No | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| A-01-0052 | Area: Identity: SSO, SCIM, MFA, sessions / Specified: Yes (V12) / Prototype-demonstrated: Yes (A122, simulated IdP) / Production-proven: No | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-784) |
| A-01-0053 | Area: Custom roles, separation of duties, audit/SIEM / Specified: Yes (V12) / Prototype-demonstrated: Yes (A123, A124) / Production-proven: No | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-775) |
| A-01-0054 | Area: API platform, webhooks, SDKs, developer portal / Specified: Yes (V12, OpenAPI A2) / Prototype-demonstrated: Partly (A125, W39) / Production-pro… | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-785) |
| A-01-0055 | Area: Data export, residency, BYOK, sandboxes / Specified: Yes (V12) / Prototype-demonstrated: Yes (A126, A127) / Production-proven: No | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-772) |
| A-01-0056 | Area: Integrations / connectors / Specified: Yes (INT-01…11) / Prototype-demonstrated: Simulated (A128) / Production-proven: No | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-785) |
| A-01-0057 | Area: AI governance and evaluation / Specified: Yes / Prototype-demonstrated: Yes (A114–A117) / Production-proven: No (no approved models) | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| A-01-0058 | Area: Compliance: jurisdictions, consent, DSAR, breach / Specified: Yes (IN, EU; 7 more markets draft) / Prototype-demonstrated: Yes (A118–A121, W35)… | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| A-01-0059 | Area: Security programme and certifications / Specified: Yes (V12) / Prototype-demonstrated: Tracker only (A129) / Production-proven: No (no audit or… | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-775) |
| A-01-0060 | Area: Reliability: SLOs, incidents, status, DR / Specified: Yes / Prototype-demonstrated: Simulated (A130, W40) / Production-proven: No (no drills) | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-775) |
| A-01-0061 | Area: Global readiness: locales, RTL, tax, regions / Specified: Yes (V12) / Prototype-demonstrated: Partial (5 locales on key pages, A131 tax preview… | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-776) |
| A-01-0062 | Area: Business operations: billing, support, contracts / Specified: Yes (V12) / Prototype-demonstrated: Preview (A131) / Production-proven: No | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| A-01-0063 | Area: Accessibility / Specified: Yes (WCAG 2.2 AA target) / Prototype-demonstrated: Automated WCAG 2.1 A/AA pass / Production-proven: No manual audit | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| A-01-0068 | V11 is the final controlled baseline. It applies the eight corrections found in the review of V10, records the approval evidence, adds V11 scores and… | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| A-01-0084 | V10 is the current controlled development baseline. Read this baseline and V10 sections first; retain compatible V9/V8/V7 contracts, 35 release KPIs,… | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| A-01-0096 | V11 verification evidence: FSD chapter 33 (V11 section) and chapter 34 (scores). V9/V10 evidence remains historical. KPI release gates are binding (F… | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| REC-29 | ID / priority / owner: REC-29 · P0 / Document owner / Source D38 / Required change: One V10 precedence and authoritative inventory; preserve V9/V8 re… | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0098 | V9 reviews the original 38-document specification set. 1,275 of 1,279 substantive table cells were already present in V8, but almost entirely inside … | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| P9 | ID: P9 / Source document: 36 Comprehensive Product Optimization Engineering + 29 Performance, Load, Scalability & Reliability / Promoted content: Rec… | Conflict | DEC-018; CONFLICT-462 | Growth RTO | DEC-515; CONFLICT-765 | Adopted (DEC-790) |
| A-01-0108 | Not promoted. Page counts (38); API, table, test and traceability catalogues (06, 07, 08, 22, 24) — superseded by Appendices A–C, step tests and the … | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0109 | Commercial unit rule. 39 service SKUs are sold; 156 workflows are included under their parent SKU and are never sold separately. | Conflict | DEC-047 | 39 SKUs sold; 156 workflows included | DEC-501; CONFLICT-767 | Matched |
| A-01-0122 | V8 merges the two V7 lines into one controlled baseline: the responsive V7 set (BRD, FSD and four desktop/mobile HTML builds with 18 MOB requirements… | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| A-01-0123 | Commercial unit rule. Sellable services and included automation flows are different commercial units: 39 service SKUs are sold (Website, BRD); 156 wo… | Conflict | DEC-047 | 39 SKUs sold; 156 workflows included | DEC-501; CONFLICT-767 | Matched |
| A-01-0144 | V8 keeps the product scope (39 sellable services, 156 included workflows) and adds what a multi-country AI platform needs to launch: a compliance and… | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0189 | V6 handoff contract SM-APPLICATION-6 remains unchanged and is used by all four V7 builds. The preceding V6 checksums and screenshots are historical s… | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| A-01-0190 | V6 product vision: Universal Multi-Tenant, Multi-Business, Multi-Product, Multi-Country, Omnichannel AI Sales & Marketing Automation Platform. AppNAI… | Partially covered | Part 0B; §11.1.4 | Inventory reconciled | DEC-500 | Matched |
| A-01-0191 | Requirement precedence: MT-01–40 govern the new hierarchy and configuration experience; BR-C01–15 and the 135 V5 optimization requirements remain bin… | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| A-01-0192 | V5 scope and authority: This version integrates all 135 optimization requirements into the numbered master chapters. Scope remains 39 independently p… | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| A-01-0193 | Status and precedence: V5 OPT requirement IDs supersede less-specific inherited guidance where compatible with BR-C01–15 and authorized scope. No mod… | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| A-01-0194 | Dimension: AI cost optimization / Requirements: 15 / P0 / P1 / P2: 6 / 9 / 0 | Not covered | None (OPT taxonomy differs) | 135-OPT crosswalk §11.1.4 | DEC-500 | Matched |
| A-01-0195 | Dimension: General cost optimization / Requirements: 15 / P0 / P1 / P2: 6 / 8 / 1 | Not covered | None (OPT taxonomy differs) | 135-OPT crosswalk §11.1.4 | DEC-500 | Matched |
| A-01-0196 | Dimension: Application security / Requirements: 15 / P0 / P1 / P2: 14 / 1 / 0 | Not covered | None (OPT taxonomy differs) | 135-OPT crosswalk §11.1.4 | DEC-500 | Matched |
| A-01-0197 | Dimension: Application stability / Requirements: 15 / P0 / P1 / P2: 11 / 4 / 0 | Not covered | None (OPT taxonomy differs) | 135-OPT crosswalk §11.1.4 | DEC-500 | Matched |
| A-01-0198 | Dimension: AI flow automation / Requirements: 15 / P0 / P1 / P2: 7 / 7 / 1 | Not covered | None (OPT taxonomy differs) | 135-OPT crosswalk §11.1.4 | DEC-500 | Matched |
| A-01-0199 | Dimension: Customer attraction / Requirements: 15 / P0 / P1 / P2: 1 / 12 / 2 | Not covered | None (OPT taxonomy differs) | 135-OPT crosswalk §11.1.4 | DEC-500 | Matched |
| A-01-0200 | Dimension: Customer retention / Requirements: 15 / P0 / P1 / P2: 2 / 12 / 1 | Not covered | None (OPT taxonomy differs) | 135-OPT crosswalk §11.1.4 | DEC-500 | Matched |
| A-01-0201 | Dimension: Customer conversion / Requirements: 15 / P0 / P1 / P2: 3 / 12 / 0 | Not covered | None (OPT taxonomy differs) | 135-OPT crosswalk §11.1.4 | DEC-500 | Matched |
| A-01-0202 | Dimension: Customer satisfaction / Requirements: 15 / P0 / P1 / P2: 4 / 11 / 0 | Not covered | None (OPT taxonomy differs) | 135-OPT crosswalk §11.1.4 | DEC-500 | Matched |
| A-01-0203 | Dimension: Total / Requirements: 135 / P0 / P1 / P2: 54 / 76 / 5 | Not covered | None (OPT taxonomy differs) | 135-OPT crosswalk §11.1.4 | DEC-500 | Matched |
| A-01-0214 | Source precedence: current V6 instructions and MT-01–40; active governing business requirements and V5 OPT-135; 2031 catalogue; V6 prototype intent; … | Partially covered | DEC-415 precedence; Part 0B | V12 precedence and inventory | DEC-500 | Matched |
| BR-V3-01 | ID / subject: BR-V3-01 — Catalogue and sales unit / Requirement: 39 independently purchasable planned SM-SVC SKUs; 156 workflow contracts included un… | Conflict | DEC-047 plan archetypes | 39 SKUs independently purchasable; archetypes become bundles | DEC-501; CONFLICT-767; FR-V12-A-001..006 | Matched |
| BR-V3-02 | ID / subject: BR-V3-02 — Customer discovery / Requirement: Customers can search individual services and inspect four workflow triggers, inputs, outpu… | Partially covered | W04/W05/W11/W31 | Storefront discovery/selection | FR-V12-A-055..057 | Matched |
| BR-V3-03 | ID / subject: BR-V3-03 — Service recommendation / Requirement: Objective and business model guide a transparent rule-based prototype recommendation. … | Partially covered | W04/W05/W11/W31 | Storefront discovery/selection | FR-V12-A-055..057 | Matched |
| BR-V3-04 | ID / subject: BR-V3-04 — Commercial configuration / Requirement: Full/partial/selective selection, delivery mode, billing cycle and currency. Compare… | Partially covered | W04/W05/W11/W31 | Storefront discovery/selection | FR-V12-A-055..057 | Matched |
| BR-V3-05 | ID / subject: BR-V3-05 — Private onboarding / Requirement: Collect validated business identity and administrator email, company model, region, offeri… | Partially covered | W32/W33/US-2004 | Onboarding envelope | FR-V12-A-090..097 | Matched |
| BR-V3-06 | ID / subject: BR-V3-06 — Revision integrity / Requirement: Application ID is stable for a submitted registration. Revision increments on material cha… | Partially covered | W32/W33/US-2004 | Onboarding envelope | FR-V12-A-090..097 | Matched |
| BR-V3-07 | ID / subject: BR-V3-07 — Application intake / Requirement: Validate canonical V4 schema, configuration bounds and stable SKU IDs; reject altered fing… | Partially covered | W32/W33/US-2004 | Onboarding envelope | FR-V12-A-090..097 | Matched |
| BR-V3-08 | ID / subject: BR-V3-08 — Customer parity and roles / Requirement: Owned companies follow the same SaaS lifecycle as independent customers. Demo membe… | Conflict | DEC-065 | Customer parity | DEC-504; CONFLICT-763 | Matched |
| BR-V3-09 | ID / subject: BR-V3-09 — Usage and authority / Requirement: Usage is cumulative by company, service and sample month. Pending, queued, running and un… | Partially covered | BRL-SVC-03 | Reservation at pending/queued/running | FR-V12-A-014 | Matched |
| BR-V3-10 | ID / subject: BR-V3-10 — Management experience / Requirement: All fourteen management views have differentiated KPI panels and relevant run subsets. … | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| BR-V3-11 | ID / subject: BR-V3-11 — Daily operations / Requirement: All 39 workspaces have domain-specific draft and evidence fields, searchable scoped records,… | Partially covered | Part 2.1 modules | 39 service workspaces (Group B) | FR-V12-A-003 | Matched |
| BR-V3-12 | ID / subject: BR-V3-12 — Lifecycle and commercial controls / Requirement: Operator tracks applications and sample quote/agreement/payment-evidence re… | Partially covered | A101; CSO | Lifecycle controls | FR-V12-A-016..022 | Matched |
| BR-V3-13 | ID / subject: BR-V3-13 — Service operations / Requirement: Control centre offers 156 workflow-specific input previews, 517 manual step walkthroughs a… | Partially covered | A033/A110 | 156 previews/517 walkthroughs (Groups C/D) | FR-V12-A-002 | Matched |
| A-01-0231 | Purpose: a neutral SaaS product selling configurable sales and marketing automation, not a public marketplace of customer companies. The operator sel… | Conflict | BR-WEB (startup publication) | Neutral storefront | DEC-505; CONFLICT-764 | Matched |
| BR-C01@01 | ID / rule: BR-C01 — Neutral storefront / Business obligation: Public assets contain only approved platform service information and synthetic examples… | Conflict | FR-W02 directory; FR-W03 startup site; API-497; US-1905 | Neutral storefront; platform directory retired; startup sites only on tenant-verified pro… | DEC-505; CONFLICT-764; FR-V12-A-050..052 | Matched |
| BR-C02 | ID / rule: BR-C02 — Customer parity / Business obligation: Owned and third-party companies use identical registration, payment, provisioning and enti… | Conflict | DEC-065 one Owner Portfolio tenant; DEC-055; Part 2.4 §2.35.1 | Each owned company becomes its own tenant; portfolio = revocable grant | DEC-504; CONFLICT-763; ADR-180; FR-V12-A-070..074 | Matched |
| BR-C03 | ID / rule: BR-C03 — Scope / Business obligation: 39 SM-SVC SKUs; 156 workflows; 25 included foundation; 100 legacy capability IDs; 15 shared engine t… | Partially covered | Part 1 scope | 39/156/25/15 inventory | FR-V12-A-001 | Matched |
| BR-C04 | ID / rule: BR-C04 — Independent service purchase / Business obligation: Any released SKU purchasable alone with authorized equivalent inputs. Full an… | Conflict | DEC-047 plan archetypes | 39 SKUs independently purchasable; archetypes become bundles | DEC-501; CONFLICT-767; FR-V12-A-001..006 | Matched |
| BR-C07 | ID / rule: BR-C07 — Portfolio / Business obligation: 25+ owned companies configurable; revocable grants only; no default external customer aggregatio… | Partially covered | DEC-055 | Revocable grants | FR-V12-A-072 | Matched |
| BR-C09@01 | ID / rule: BR-C09 — Effects / Business obligation: Draft/simulation no external effects. Real external actions require exact approval or eligible bou… | Conflict | DEC-064; BRL-APR-01 | Exact approval adopted; bounded mandate restricted to DEC-064 routine class | DEC-508; CONFLICT-762 | Adopted (DEC-779) |
| BR-C10 | ID / rule: BR-C10 — Commercial terms / Business obligation: Versioned quote and approved fees, unit, caps, taxes, delivery mode, pass-through and ren… | Partially covered | Part 8.3c §8.3.5.13.2 | Versioned SaaS quote | FR-V12-A-017; FR-V12-A-030 | Matched |
| BR-C12 | ID / rule: BR-C12 — Migration / Business obligation: Stable IDs, versioned definitions, rights mapping, reversible changes; active run uses snapshot … | Partially covered | Part 3 migration | Catalogue versioning and alias map | FR-V12-A-004 | Matched |
| BR-C15 | ID / rule: BR-C15 — Precedence / Business obligation: Current instruction and active V2 governing decisions > 2031 catalogue > neutral route intent >… | Not covered | DEC-415 precedence | V12 precedence | DEC-500 | Matched |

#### 11.1.3.02 Chapter 02: Business Objectives Success Criteria

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| A-02-0247 | Proposed pilot outcomes: Freeze a representative workload and cohort before any comparison. Candidate objectives: AI inference cost 20–40% lower, tot… | Partially covered | Part 1 §1.13 hypotheses | Hypotheses registered (not targets) | FR-V12-A-221 | Matched |
| BR-OBJ-01 | Requirement / field: BR-OBJ-01 / Specification: Reduce time from authorized source to qualified opportunity; compare measured baseline by sector and … | Partially covered | Part 1 §1.4.1 goals; KPI-01..31 | Objectives adopted with KPI-V12-A | FR-V12-A-220; DEC-511 | Matched |
| BR-OBJ-02 | Requirement / field: BR-OBJ-02 / Specification: Reduce time-to-first-value: verified registration to first accepted output; track median and p90. | Partially covered | Part 1 §1.4.1 goals; KPI-01..31 | Objectives adopted with KPI-V12-A | FR-V12-A-220; DEC-511 | Matched |
| BR-OBJ-03 | Requirement / field: BR-OBJ-03 / Specification: Increase verified commercial outcomes using evidence-linked funnel and controlled experiments, not AI… | Partially covered | Part 1 §1.4.1 goals; KPI-01..31 | Objectives adopted with KPI-V12-A | FR-V12-A-220; DEC-511 | Matched |
| BR-OBJ-04 | Requirement / field: BR-OBJ-04 / Specification: Operate with sustainable gross margin and configurable service caps; owner approves targets before pr… | Partially covered | Part 1 §1.4.1 goals; KPI-01..31 | Objectives adopted with KPI-V12-A | FR-V12-A-220; DEC-511 | Matched |
| BR-OBJ-05 | Requirement / field: BR-OBJ-05 / Specification: Zero critical isolation violations and unapproved effects in mandatory acceptance tests; no release w… | Partially covered | Part 1 §1.4.1 goals; KPI-01..31 | Objectives adopted with KPI-V12-A | FR-V12-A-220; DEC-511 | Matched |

#### 11.1.3.03 Chapter 03: Market Positioning Competitive Strategy

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| A-03-0253 | Position against CRM, channel tools and point automation through independent SKU purchase, evidence-linked outputs, configurable orchestration, provi… | Partially covered | Part 1 §1.3; §1.13 | Positioning and segment evidence | FR-V12-A-222 | Matched |
| A-03-0254 | Segment: Startup / SME / Primary need: Discovery, engagement and proposals / Pilot evidence: Time saved and accepted leads | Partially covered | Part 1 §1.3; §1.13 | Positioning and segment evidence | FR-V12-A-222 | Matched |
| A-03-0255 | Segment: Enterprise / Primary need: ABM, approval, integrations and SLA / Pilot evidence: Security review and successful integration | Partially covered | Part 1 §1.3; §1.13 | Positioning and segment evidence | FR-V12-A-222 | Matched |
| A-03-0256 | Segment: Agency / partner / Primary need: Delegated multi-client service / Pilot evidence: Scope and client consent test | Partially covered | Part 1 §1.3; §1.13 | Positioning and segment evidence | FR-V12-A-222 | Matched |
| A-03-0257 | Segment: Institutional / regulated / Primary need: Evidence, permissions, controlled claims / Pilot evidence: Legal and domain approval | Partially covered | Part 1 §1.3; §1.13 | Positioning and segment evidence | FR-V12-A-222 | Matched |

#### 11.1.3.04 Chapter 04: Stakeholders Personas Customer Segmenta

**Covered (grouped, 21):** A-04-0273, A-04-0274, A-04-0275, A-04-0276, A-04-0277, A-04-0279, A-04-0280 → Part 1 personas; Part 2.3 roles R01-R20; P-01, P-02, P-03, P-04, P-05, P-06 → Part 1 P01-P16; Part 8.3b TRN; A-04-0260, A-04-0261, A-04-0262, A-04-0263, A-04-0264 → DEC-052 capability routing; REC-07 → Part 8.3b journeys; BRL-TEN-11 templates; A-04-0259 → Part 8.3c; Part 4.3; Part 8.3b (38-document pack coverage); A-04-0281 → Part 2.4 CFG; W33. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| A-04-0271 | Customer profiles: Individual professional, freelancer, solopreneur, creator, proprietorship, partnership, startup, SME, enterprise, institution, age… | Not covered | None | 14 customer types | FR-V12-A-080 | Matched |
| MT-04 | MT-04 — Individual and professional customer types / Requirement: Support 14 configurable customer types; individual uses personal business workspace… | Not covered | None (startup legal entity assumed) | 14 customer types | FR-V12-A-080 | Matched |
| A-04-0278 | Actor: Portfolio owner / Authority / responsibility: Explicit grant to selected company aggregates; no automatic record access | Partially covered | DEC-055 | Explicit grant | FR-V12-A-072 | Matched |

#### 11.1.3.05 Chapter 05: SaaS Business Commercial Operating Mode

**Covered (grouped, 3):** A-05-0293, A-05-0294 → CSO-01..12; WF-01..14; A-05-0296 → Part 4.1; DPA. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| BR-V12-01 | ID: BR-V12-01 / Capability: Enterprise identity / Business outcome: Organisations sign in with their own identity provider, provision users automatic… | Partially covered | Part 9.9a CAP-X3; Part 4.1; Part 8.3c | Adopted as business requirement with release mapping; funding beyond approved budget | FR-V12-A-180..189; DEC-513; CONFLICT-760 | Adopted (DEC-790) |
| BR-V12-02 | ID: BR-V12-02 / Capability: Governed access / Business outcome: Customers define their own roles; conflicting duties are impossible; every action is … | Partially covered | Part 9.9a CAP-X3; Part 4.1; Part 8.3c | Adopted as business requirement with release mapping; funding beyond approved budget | FR-V12-A-180..189; DEC-513; CONFLICT-760 | Adopted (DEC-790) |
| BR-V12-03 | ID: BR-V12-03 / Capability: Developer platform / Business outcome: Customers integrate through a documented, versioned API, signed webhooks and SDKs,… | Partially covered | Part 9.9a CAP-X3; Part 4.1; Part 8.3c | Adopted as business requirement with release mapping; funding beyond approved budget | FR-V12-A-180..189; DEC-513; CONFLICT-760 | Adopted (DEC-785) |
| BR-V12-04 | ID: BR-V12-04 / Capability: Data ownership / Business outcome: Customers can export all their data, choose where it lives and, on eligible plans, hol… | Partially covered | Part 9.9a CAP-X3; Part 4.1; Part 8.3c | Adopted as business requirement with release mapping; funding beyond approved budget | FR-V12-A-180..189; DEC-513; CONFLICT-760 | Adopted (DEC-790) |
| BR-V12-05 | ID: BR-V12-05 / Capability: Ecosystem / Business outcome: Customers connect their CRM, messaging, calendar, advertising, payment and warehouse tools … | Partially covered | Part 9.9a CAP-X3; Part 4.1; Part 8.3c | Adopted as business requirement with release mapping; funding beyond approved budget | FR-V12-A-180..189; DEC-513; CONFLICT-760 | Adopted (DEC-780) |
| BR-V12-06 | ID: BR-V12-06 / Capability: Assured security / Business outcome: Independent testing, a vulnerability programme and recognised certifications (SOC 2,… | Partially covered | Part 9.9a CAP-X3; Part 4.1; Part 8.3c | Adopted as business requirement with release mapping; funding beyond approved budget | FR-V12-A-180..189; DEC-513; CONFLICT-760 | Adopted (DEC-775) |
| BR-V12-07 | ID: BR-V12-07 / Capability: Legal readiness / Business outcome: Customers receive approved legal documents and a DPA; each new market opens only afte… | Partially covered | Part 9.9a CAP-X3; Part 4.1; Part 8.3c | Adopted as business requirement with release mapping; funding beyond approved budget | FR-V12-A-180..189; DEC-513; CONFLICT-760 | Adopted (DEC-790) |
| BR-V12-08 | ID: BR-V12-08 / Capability: Global reach / Business outcome: The product works in the customer’s language, currency, tax system and region, starting … | Partially covered | Part 9.9a CAP-X3; Part 4.1; Part 8.3c | Adopted as business requirement with release mapping; funding beyond approved budget | FR-V12-A-180..189; DEC-513; CONFLICT-760 | Adopted (DEC-776) |
| BR-V12-09 | ID: BR-V12-09 / Capability: Dependable service / Business outcome: Contracted availability, a public status page, 24×7 incident response and responsi… | Partially covered | Part 9.9a CAP-X3; Part 4.1; Part 8.3c | Adopted as business requirement with release mapping; funding beyond approved budget | FR-V12-A-180..189; DEC-513; CONFLICT-760 | Adopted (DEC-773) |
| BR-V12-10 | ID: BR-V12-10 / Capability: Commercial operations / Business outcome: Accurate billing with tax, contracts, onboarding and success programmes, and an… | Partially covered | Part 9.9a CAP-X3; Part 4.1; Part 8.3c | Adopted as business requirement with release mapping; funding beyond approved budget | FR-V12-A-180..189; DEC-513; CONFLICT-760 | Adopted (DEC-776) |
| AT-15 | AT-15 · P1 · Operator acquisition workspace / Requirement: Use subscribed commercial services under separate operator tenant for SaaS acquisition. / … | Partially covered | A108 operator enquiries | Operator acquisition tenant | FR-V12-A-073 | Matched |
| A-05-0295 | Lifecycle: Delivery models / State / business rules: Self-service, assisted, managed and enterprise. Delegation is scoped, revocable, and audited; ma… | Partially covered | Part 8.3c service model | Assisted and enterprise models added | FR-V12-A-024 | Matched |
| A-05-0297 | Lifecycle: Partner / reseller / State / business rules: Optional future release; contract, separate tenant consent, attribution and billing ownership… | Partially covered | DEC-046; X-09 | Future option recorded; white-label never weakens isolation | FR-V12-A-020 | Matched |

#### 11.1.3.06 Chapter 06: Multi Tenant Multi Company Business Arc

**Covered (grouped, 5):** GC-01, GC-02, GC-12 → Part 3.1 modular monolith; design system; MOB-01@06 → DEC-043; MT-33 → Part 3.3 master data. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| A-06-0299 | Contract and portfolio separation: A tenant is the independent SaaS contract and data security boundary. Each tenant may have one or more organizatio… | Conflict | DEC-065; Part 2.4 §2.35 | Adopt tenant/company/portfolio-grant model | DEC-504; CONFLICT-763; ADR-180 | Matched |
| A-06-0300 | Logical hierarchy: Tenant → organization → company → division → brand → subscriber offering. Market and channel account are company-owned profiles, l… | Partially covered | Tenant/Startup/BusinessLine/Offering (DEC-016) | Organization, division, brand, market, channel account added | DEC-506; FR-V12-A-075..080 | Matched |
| MT-01 | MT-01 — Separate tenant, organization and company master entities / Requirement: Tenant is contract/security root; organization and company are separ… | Conflict | DEC-065 one Owner Portfolio tenant; DEC-055; Part 2.4 §2.35.1 | Each owned company becomes its own tenant; portfolio = revocable grant | DEC-504; CONFLICT-763; ADR-180; FR-V12-A-070..074 | Matched |
| MT-05 | MT-05 — Multiple companies under an authorized tenant / Requirement: One tenant may contractually authorize several operating companies; explicit com… | Conflict | DEC-065 one Owner Portfolio tenant; DEC-055; Part 2.4 §2.35.1 | Each owned company becomes its own tenant; portfolio = revocable grant | DEC-504; CONFLICT-763; ADR-180; FR-V12-A-070..074 | Matched |
| MT-07 | MT-07 — Independent portfolio grants / Requirement: Grants explicit, revocable, resource and aggregate scoped; independent clients excluded unless se… | Conflict | DEC-065 one Owner Portfolio tenant; DEC-055; Part 2.4 §2.35.1 | Each owned company becomes its own tenant; portfolio = revocable grant | DEC-504; CONFLICT-763; ADR-180; FR-V12-A-070..074 | Matched |
| A-06-0308 | Tenant is the contractual customer organization; company is a scoped operating business within the tenant. Default one independently subscribed custo… | Conflict | DEC-065; Part 2.4 §2.35 | Adopt tenant/company/portfolio-grant model | DEC-504; CONFLICT-763; ADR-180 | Matched |

#### 11.1.3.07 Chapter 07: Universal Business Configuration Onboar

**Covered (grouped, 6):** REC-04@07 → A112; Part 2.4 §2.33.3; A-07-0314 → DEC-031; AP-01; MT-03 → BRL-TEN-11; AP-01; MT-19 → IANA time zones (Part 3.3); FL-12 → BRL-TEN-11; CV-02 → BRL-SVC-02. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| MOB-04@07 | MOB-04 Progressive onboarding / Owner — Customer success + frontend / Business requirement — Customers across all 14 supported types can configure or… | Partially covered | W32/W33; BRL-SVC-02 | Eight-stage wizard | FR-V12-A-090..092 | Matched |
| MOB-11@07 | MOB-11 Session and draft recovery / Owner — IAM + customer success / Business requirement — Session end clears synthetic private company graph, signa… | Partially covered | W32/W33; BRL-SVC-02 | Eight-stage wizard | FR-V12-A-090..092 | Matched |
| MOB-16@07 | MOB-16 Cross-device application handoff / Owner — Frontend + integration / Business requirement — An application produced on desktop can be reviewed … | Not covered | None | Cross-device signed handoff | FR-V12-A-095 | Matched |
| A-07-0313 | Private onboarding and organization manager: W32 private registration and W33 eight-stage configuration use identity, organizations/companies, divisi… | Partially covered | W32/W33; A099/A100/A112 | Organization management centre | FR-V12-A-090..093 | Matched |
| MT-08 | MT-08 — Eight-stage private configuration wizard / Requirement: Identity; organizations/companies; divisions/brands; markets/offerings; channel accou… | Partially covered | W33 wizard | Eight stages | FR-V12-A-090 | Matched |
| MT-09 | MT-09 — Business division master / Requirement: Division stable ID and scoped company FK; lifecycle independent of name; all relevant records use ref… | Not covered | Part 3.3 (division partial) | Hierarchy and country model | FR-V12-A-075..078 | Matched |
| MT-10 | MT-10 — Brand management / Requirement: Brand owned by division; scoped brand configuration and approved claims; reusable in offering records. / Acce… | Not covered | Part 3.3 (division partial) | Hierarchy and country model | FR-V12-A-075..078 | Matched |
| MT-11 | MT-11 — Unified subscriber offering master / Requirement: Product, service, programme, solution separate from platform SKU; versioned brand FK, statu… | Partially covered | Offering version; DEC-060 readiness gate | Lifecycle states adopted | FR-V12-A-079 | Matched |
| MT-15 | MT-15 — Offering lifecycle and launch approvals / Requirement: Draft/pilot/active/suspended/retired; authorization gate for live external effect; his… | Partially covered | Offering version; DEC-060 readiness gate | Lifecycle states adopted | FR-V12-A-079 | Matched |
| MT-17 | MT-17 — Separate registration, operating and target countries / Requirement: Company registration country distinct from operating countries, market a… | Not covered | Part 3.3 (division partial) | Hierarchy and country model | FR-V12-A-075..078 | Matched |
| MT-18 | MT-18 — Multiple countries per offering / Requirement: Market profiles reused through offering-market associations; each market independently eligibl… | Not covered | Part 3.3 (division partial) | Hierarchy and country model | FR-V12-A-075..078 | Matched |
| MT-29 | MT-29 — Industry/business workflow templates / Requirement: Template is versioned configuration referencing canonical workflow; review industry-speci… | Partially covered | BRL-TEN-11 templates | Template references canonical workflow | FR-V12-A-094 | Matched |
| SEC-05 | SEC-05 · P0 · Authenticated application integrity / Requirement: Keep V4 demo envelope compatible; production binds signed identity, canonical digest… | Partially covered | US-2004 import; BRL-SVC-01 | Signed identity + canonical digest | FR-V12-A-096 | Matched |
| CV-01 | CV-01 · P1 · Progressive onboarding / Requirement: Collect minimal essential fields first; defer optional details until review, preserve validation. … | Partially covered | W33 | Minimal-first onboarding | FR-V12-A-091 | Matched |
| A-07-0329 | Stage: Discovery / Required behavior / decision: W01/W04/W05: service outcomes, comparison, prerequisites, illustrative ROI; no outcome guarantees. | Partially covered | W01-W06, W32-W34, A099-A101 | Journey stages adopted | FR-V12-A-090..097 | Matched |
| A-07-0330 | Stage: Selection / Required behavior / decision: W06/W11/W31: recommend with explanation, select valid SKU IDs; retain customer control. | Partially covered | W01-W06, W32-W34, A099-A101 | Journey stages adopted | FR-V12-A-090..097 | Matched |
| A-07-0331 | Stage: Private intake / Required behavior / decision: W32/W33: configure business model/locale, targets, evidence, consent and authority. | Partially covered | W01-W06, W32-W34, A099-A101 | Journey stages adopted | FR-V12-A-090..097 | Matched |
| A-07-0332 | Stage: Review and export / Required behavior / decision: O02: verify V4 envelope, application ID, revision and fingerprint; reject replay, update onl… | Partially covered | W01-W06, W32-W34, A099-A101 | Journey stages adopted | FR-V12-A-090..097 | Matched |
| A-07-0333 | Stage: Operator review / Required behavior / decision: O02: import allowlisted fields, verify and hold; create pending workspace without entitlements. | Partially covered | W01-W06, W32-W34, A099-A101 | Journey stages adopted | FR-V12-A-090..097 | Matched |
| A-07-0334 | Stage: Commercial lifecycle / Required behavior / decision: O03/O04: local quote preparation → agreement review → payment evidence pending. Productio… | Partially covered | W01-W06, W32-W34, A099-A101 | Journey stages adopted | FR-V12-A-090..097 | Matched |
| A-07-0335 | Stage: Renewal / changes / Required behavior / decision: Production must enforce upgrade/downgrade timing, grace periods, proration, credits, cancell… | Not covered | None | Proration/grace/offboarding | FR-V12-A-016; FR-V12-A-021..022 | Matched |
| A-07-0336 | V4 chapter guidance: BR-V3-05–07: current application fields, revision invalidation and pending intake are defined in the current chapter registers. | Partially covered | US-2004 | Envelope parity | FR-V12-A-096 | Matched |
| A-07-0337 | Configuration group: Identity / Required business information: Legal name, registration and tax identifiers where required, country, region, timezone… | Partially covered | Part 2.4 CFG-01..32; W33 | Configuration groups adopted | FR-V12-A-090 | Matched |
| A-07-0338 | Configuration group: Business model / Required business information: B2B/B2C/D2C/B2G/institutional/marketplace/hybrid; offerings and approved claims | Partially covered | Part 2.4 CFG-01..32; W33 | Configuration groups adopted | FR-V12-A-090 | Matched |
| A-07-0339 | Configuration group: ICP / sales / Required business information: Target geographies, account/lead types, sales stages, qualification, owners, territ… | Partially covered | Part 2.4 CFG-01..32; W33 | Configuration groups adopted | FR-V12-A-090 | Matched |
| A-07-0340 | Configuration group: Channels / Required business information: Sender identity, lawful basis and consent, provider account, quiet hours, caps, langua… | Partially covered | Part 2.4 CFG-01..32; W33 | Configuration groups adopted | FR-V12-A-090 | Matched |
| A-07-0341 | Configuration group: Governance / Required business information: Approval hierarchy, spend caps, discount bounds, sensitive data exclusions, delegate… | Partially covered | Part 2.4 CFG-01..32; W33 | Configuration groups adopted | FR-V12-A-090 | Matched |
| A-07-0342 | Configuration group: Commercial / Required business information: SKU IDs, plan version, quota, payment status, service model | Partially covered | Part 2.4 CFG-01..32; W33 | Configuration groups adopted | FR-V12-A-090 | Matched |
| A-07-0343 | Configuration group: Activation / Required business information: Validate required inputs; simulation with synthetic or authorized data; owner approv… | Partially covered | Part 2.4 CFG-01..32; W33 | Configuration groups adopted | FR-V12-A-090 | Matched |
| A-07-0344 | The same contract governs Website W32–W34 and operator O02. Never include actual credentials in the offline prototype. Customer parity applies to own… | Partially covered | US-2004 | Envelope parity | FR-V12-A-096 | Matched |
| A-07-0345 | Area: Envelope / Canonical fields / decision: schema = SM-APPLICATION-4; product = commercial; kind = request; fingerprint; configuration; notice / V… | Not covered | US-2004 (no canonical envelope) | Canonical application envelope | FR-V12-A-096..097 | Matched |
| A-07-0346 | Area: Identity / Canonical fields / decision: applicationId (APP-DEMO-…), revision (positive integer), name (≤150), administratorEmail (valid email),… | Partially covered | Part 2.4 CFG-01..32; W33 | Configuration groups adopted | FR-V12-A-090 | Matched |
| A-07-0347 | Area: Operating configuration / Canonical fields / decision: description, lines, offerings, objectives, caps, icp, claims, language, timezone, channe… | Not covered | US-2004 (no canonical envelope) | Canonical application envelope | FR-V12-A-096..097 | Matched |
| A-07-0348 | Area: Usage / Canonical fields / decision: budget: finite 0–10^12; volume: whole 1–10^8 / Validation and effect: Illustrative amounts/units; no appro… | Not covered | US-2004 (no canonical envelope) | Canonical application envelope | FR-V12-A-096..097 | Matched |
| A-07-0349 | Area: Commercial / Canonical fields / decision: currency, service, plan, selectionMode, selectedServiceIds, selectedAutomationIds, billingCycle, appr… | Partially covered | Part 2.4 CFG-01..32; W33 | Configuration groups adopted | FR-V12-A-090 | Matched |
| A-07-0350 | Area: Fingerprint / Canonical fields / decision: Canonical allowlisted configuration in fixed key order; 32-bit FNV-1a demo fingerprint / Validation … | Not covered | US-2004 (no canonical envelope) | Canonical application envelope | FR-V12-A-096..097 | Matched |
| A-07-0351 | Area: Replay and revision / Canonical fields / decision: Application ID unique; same or older revision rejected; greater revision updates pending rec… | Not covered | US-2004 (no canonical envelope) | Canonical application envelope | FR-V12-A-096..097 | Matched |

#### 11.1.3.10 Chapter 10: Subscription Bundle Entitlement Model

**Covered (grouped, 6):** MT-06 → BRL-SVC-06; CSO-11/12; WF-14; CV-13 → DEC-022 payment adapter; webhook verification; A-10-0360 → BRL-SVC-05; A-10-0362 → CSO-03..07; A-10-0366 → BRL-SVC-03; A-10-0370 → BRL-FIN-08. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| A-10-0352 | Independent purchase and scoped use: A subscriber may use one purchased SKU across multiple permitted offerings and markets within agreed usage/entit… | Not covered | BRL-SVC-03; US-2001 | SKU entitlement scoped by company/offering/market | FR-V12-A-010..012 | Matched |
| MT-16 | MT-16 — Purchased automation mapped to offerings / Requirement: Configurations reference entitlement and SKU/workflow; scope by company/offer/market/… | Not covered | BRL-SVC-03 | Entitlement-scoped configuration | FR-V12-A-011 | Matched |
| MT-30 | MT-30 — Scoped automation budgets and schedules / Requirement: Company/offering/workflow configuration budgets plus tenant aggregate cap, currency, p… | Partially covered | DEC-008; M53 budgets per startup | Company/offering/workflow budgets + tenant cap | FR-V12-A-014 | Matched |
| RT-07 | RT-07 · P0 · Consumption forecasts and quota alerts / Requirement: Compute remaining allowance, reservations and trend; alert thresholds before cap. … | Partially covered | BRL-SVC-03; A101 | Forecast and threshold alerts | FR-V12-A-015 | Matched |
| RT-11 | RT-11 · P1 · Flexible plan changes / Requirement: Define effective date, proration, usage reconciliation and pause/downgrade/cancellation under appro… | Not covered | None (no proration) | Plan change preview, effective date, proration | FR-V12-A-016 | Matched |
| CV-12 | CV-12 · P0 · Versioned quote and agreement acceptance / Requirement: Bind accepted quote and agreement revisions to verified signer and exact digest.… | Partially covered | DEC-023 hash-bound e-sign (subscriber quotes) | SaaS quote/agreement bound to signer and digest | FR-V12-A-017 | Matched |
| A-10-0361 | Rule / state: Quote / Business requirement: Versioned selected SKUs, allowance, currency, taxes, delivery model and validity; selection change invali… | Partially covered | US-2005 | Quote binds application revision | FR-V12-A-017 | Matched |
| A-10-0363 | Rule / state: Upgrade/downgrade / Business requirement: Effective date and prorating policy quoted; no silent rights loss; active work held or comple… | Not covered | None | Proration rules | FR-V12-A-016 | Matched |
| A-10-0364 | Rule / state: Failed payment / Business requirement: Approved grace and notification policy; block new effects on suspension; allow authorized export… | Partially covered | BRL-SVC-06; CSO-12 | Grace/retry/notice policy | FR-V12-A-021 | Matched |
| A-10-0365 | Rule / state: Cancel / renew / Business requirement: Explicit terms, renewal notice, opt-out, final usage settlement, export and retention. | Partially covered | CSO-09..11; BRL-SVC-07 | Cancellation, final settlement, credit note | FR-V12-A-022 | Matched |
| A-10-0367 | Rule / state: Refund / Business requirement: Finance approval and linked credit note; do not equate reversal with deletion of audit. | Partially covered | BRL-SVC-07 | Credit note linked to refund | FR-V12-A-022 | Matched |
| A-10-0368 | Rule / state: New SKU / Business requirement: Full plan expansion only according to signed version/terms; no auto billing. | Not covered | None | Expansion only by signed version | FR-V12-A-012 | Matched |
| A-10-0369 | Rule / state: BYO provider / Business requirement: Customer-owned credential, verified permissions and quoted responsibility; no credential sharing. | Partially covered | CSO-05 credential model | Retained; responsibility quoted | FR-V12-A-023 | Matched |
| A-10-0371 | State: Quote / Business rule: Quote must bind application ID/revision, SKU versions, usage, billing cycle, currency, taxes and expiry; customer accep… | Partially covered | US-2005 | Quote binds application revision | FR-V12-A-017 | Matched |
| A-10-0372 | State: Upgrade/downgrade / Business rule: Proposed: upgrade on approved effective date with explicit proration; downgrade at renewal unless signed ex… | Not covered | None | Proration rules | FR-V12-A-016 | Matched |
| A-10-0373 | State: Suspension and renewal / Business rule: Grace period, retries, renewal invoice, suspension date and reactivation are contract-specific. No new… | Partially covered | BRL-SVC-06; CSO-12 | Grace/retry/notice policy | FR-V12-A-021 | Matched |
| A-10-0374 | State: Refund/cancellation / Business rule: Credit/reversal entries, approved eligibility, verified amount, cancellation date, export and retention; … | Partially covered | CSO-09..11; BRL-SVC-07 | Cancellation, final settlement, credit note | FR-V12-A-022 | Matched |
| A-10-0375 | State: Pricing / Business rule: Base subscription + usage overage or prepaid credits + approved provider pass-through + managed effort + taxes; never… | Partially covered | Part 8.3c §8.3.5.13.2 | Price composition adopted | FR-V12-A-030 | Matched |

#### 11.1.3.11 Chapter 11: Pricing Billing Commercial Unit Economi

**Covered (grouped, 40):** AI-01, AI-02, AI-03, AI-04, AI-05, AI-08, AI-09, AI-10, AI-11, AI-12, AI-14, AI-15 → Part 7.3 routing/cache/eval; DEC-418 tier order; GC-03, GC-04, GC-05, GC-06, GC-07, GC-08, GC-09, GC-11, GC-14 → Part 3.1; Part 4.2; Part 8.4; DEC-421; A-11-0381, A-11-0382, A-11-0383, A-11-0384, A-11-0385, A-11-0386, A-11-0387 → Part 7.4a/b paid-plugin register; A-11-0377, A-11-0378, A-11-0379, A-11-0380 → Part 7.4a plugin register; X-10; MT-14, MT-21 → DEC-027; offering version (Part 2.1); A-11-0376 → Part 7.4a; DEC open-source first; MOB-13@11 → OKPI-29..31; NFR web vitals; MOB-15@11 → DEC-027; MT-21; A-11-0390 → BRL-FIN-08; DEC-027; CV-05 → DEC-047 price on request; A-11-0428 → DEC-047. All Matched.

**Not applicable (grouped, 1):** 1 × table header row.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| A-11-0393 | Commercial economics: Monthly TCO = subscription + provider fees + managed operations + amortized setup + other direct costs. Report one-time costs s… | Partially covered | Part 8.3c §8.3.5.13.7 | TCO and contribution formula adopted | FR-V12-A-031 | Matched |
| AI-06 | AI-06 · P0 · Dynamic context budgeting / Requirement: Allocate tokens by task class; reserve output and safety margin; trim irrelevant evidence befor… | Partially covered | Part 7.3 token budgets | Context budget and summarisation rule adopted; detail Group F | FR-V12-A-113 | Matched |
| AI-07 | AI-07 · P1 · Intelligent conversation summarization / Requirement: Persist scoped fact/decision summaries with evidence and corrections; preserve unr… | Partially covered | Part 7.3 token budgets | Context budget and summarisation rule adopted; detail Group F | FR-V12-A-113 | Matched |
| AI-13 | AI-13 · P1 · Multimodal cost tiers / Requirement: Use thumbnail/text/transcript snippets first; require quality or business justification for full me… | Partially covered | Part 7.3 token budgets | Context budget and summarisation rule adopted; detail Group F | FR-V12-A-113 | Matched |
| GC-10 | GC-10 · P1 · Bring-your-own-provider accounts / Requirement: Offer isolated credential references and clearly allocated fees, permissions, support an… | Partially covered | CSO-05 | BYO charges separated | FR-V12-A-023 | Matched |
| GC-13 | GC-13 · P1 · Self-service operations / Requirement: Provide setup checklist, connector diagnostics and knowledge-based troubleshooting with human esc… | Partially covered | Part 8.3b help; Part 9.9a CAP-X3-21 | Self-service ops checklist and idle detection | FR-V12-A-165 | Matched |
| GC-15 | GC-15 · P1 · Idle resource detection / Requirement: Inventory unused connectors, idle infrastructure and orphaned artifacts; recommend safe cleanup w… | Partially covered | Part 8.3b help; Part 9.9a CAP-X3-21 | Self-service ops checklist and idle detection | FR-V12-A-165 | Matched |
| CS-14 | CS-14 · P0 · Billing dispute management / Requirement: Show itemized usage, invoice, credits and refund review with approved policies. / Acceptance O… | Not covered | None | Billing dispute workflow | FR-V12-A-034 | Matched |
| A-11-0423 | For every SKU, model actual per accepted output: internal LLM input/output/reasoning/embedding + search/licensed data + verification + channel/provid… | Not covered | Part 8.4 ledger (not per SKU) | Per-SKU cost model | FR-V12-A-032; GAP-769 | Matched |
| A-11-0424 | Requirement / field: Cost formula / Specification: C = sum(quantity × contracted unit cost) + allocated direct labor + allocated direct infrastructur… | Not covered | None | Formula adopted | FR-V12-A-032..033 | Matched |
| A-11-0425 | Requirement / field: Accepted result cost / Specification: Total eligible direct costs / accepted results; denominator zero → undefined, not zero. | Not covered | None | Formula adopted | FR-V12-A-032..033 | Matched |
| A-11-0426 | Requirement / field: Price floor / Specification: C / (1 − target gross margin); use approved margin in [0,1); tax and pass-through separate. | Not covered | None | Formula adopted | FR-V12-A-032..033 | Matched |
| A-11-0427 | Requirement / field: Meter policy / Specification: Billable unit per contract; retries caused by platform not automatically billable; credits/reversa… | Not covered | None | Formula adopted | FR-V12-A-032..033 | Matched |
| SM-SVC-01@11 | SM-SVC-01 / market research batch / 100 / 1.05 – 1.61 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-02@11 | SM-SVC-02 / discovery batch / 100 / 0.55 – 1.43 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-03@11 | SM-SVC-03 / contact assessed / 500 / 0.15 – 0.75 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-04@11 | SM-SVC-04 / lead assessed / 500 / 0.15 – 0.87 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-05@11 | SM-SVC-05 / relationship update / 500 / 0.15 – 0.75 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-06@11 | SM-SVC-06 / email attempt / 1000 / 0.15 – 0.69 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-07@11 | SM-SVC-07 / message attempt / 500 / 0.15 – 0.55 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-08@11 | SM-SVC-08 / follow-up decision / 1000 / 0.15 – 0.67 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-09@11 | SM-SVC-09 / conversation item / 1000 / 0.15 – 1.15 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-10@11 | SM-SVC-10 / meeting cycle / 100 / 0.15 – 1.45 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-11@11 | SM-SVC-11 / content draft / 100 / 0.55 – 2.27 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-12@11 | SM-SVC-12 / social action or listening batch / 300 / 0.15 – 1.25 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-13@11 | SM-SVC-13 / page or keyword review / 200 / 0.55 – 0.97 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-14@11 | SM-SVC-14 / campaign review or action / 100 / 0.15 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-15@11 | SM-SVC-15 / page draft or enquiry event / 500 / 0.15 – 1.77 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-16@11 | SM-SVC-16 / attendee or referral event / 500 / 0.47 – 0.55 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-17@11 | SM-SVC-17 / proposal or quotation case / 100 / 0.15 – 1.77 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-18@11 | SM-SVC-18 / agreement case / 50 / 0.15 – 1.95 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-19@11 | SM-SVC-19 / tender case / 50 / 0.55 – 2.31 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-20@11 | SM-SVC-20 / order case / 200 / 0.15 – 0.55 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-21@11 | SM-SVC-21 / invoice or receipt record / 500 / 0.15 – 0.55 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-22@11 | SM-SVC-22 / onboarding case / 100 / 0.15 – 0.97 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-23@11 | SM-SVC-23 / customer review / 500 / 0.15 – 0.87 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-24@11 | SM-SVC-24 / analytics review / 100 / 0.15 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-25@11 | SM-SVC-25 / document processed / 200 / 0.55 – 1.35 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-26@11 | SM-SVC-26 / Call minute / 100 / 0.55 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-27@11 | SM-SVC-27 / Creative asset / 50 / 0.55 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-28@11 | SM-SVC-28 / Agent transaction case / 50 / 0.55 – 0.55 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-29@11 | SM-SVC-29 / Account review / 100 / 0.55 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-30@11 | SM-SVC-30 / Experiment / 30 / 0.55 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-31@11 | SM-SVC-31 / Marketplace order/event / 500 / 0.55 – 0.55 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-32@11 | SM-SVC-32 / Partner opportunity / 100 / 0.55 – 0.55 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-33@11 | SM-SVC-33 / Support case / 500 / 0.55 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-34@11 | SM-SVC-34 / Account usage review / 200 / 0.55 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-35@11 | SM-SVC-35 / Review item / 200 / 0.55 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-36@11 | SM-SVC-36 / Coaching session / 100 / 0.55 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-37@11 | SM-SVC-37 / Pricing scenario / 50 / 0.55 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-38@11 | SM-SVC-38 / Message attempt / 500 / 0.55 – 0.55 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |
| SM-SVC-39@11 | SM-SVC-39 / Procurement case / 200 / 0.55 – 1.05 / Quote pending; excludes external fees | Not covered | None (no SKU meters) | SKU meter and pilot cap registry | FR-V12-A-035; GAP-769 | Matched |

#### 11.1.3.12 Chapter 12: Public SaaS Website Customer Acquisitio

**Covered (grouped, 15):** CV-09, CV-10, CV-11, CV-14 → W18; DEC-024; sequences; experiments; BR-V7-ADM-01@12, BR-V7-ADM-02@12, BR-V7-ADM-03@12 → BRL-APR-01; DEC-050; Part 2.5; BR-V7-WEB-01@12, BR-V7-WEB-02@12 → Part 2.5 UI states; WCAG 2.2 AA; MOB-02@12, MOB-03@12 → DEC-043; Part 2.5 responsive; AT-02, AT-09 → W07; W08; AT-10 → DEC-046; W20; AT-14 → Cookie consent; Part 2.4 §2.31. All Matched.

**Not applicable (grouped, 1):** 1 × navigation note.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| BR-V7-WEB-03@12 | ID: BR-V7-WEB-03 / Subject: Data-rights page / Requirement: Public page to submit a data-rights request. / Acceptance: PT-V7-07 / FSD trace: CJ-R07 /… | Partially covered | W30 privacy; BRL-PRV-01 | Data-rights and AI-transparency public pages | FR-V12-A-053..054 | Matched |
| BR-V7-WEB-04@12 | ID: BR-V7-WEB-04 / Subject: AI transparency page / Requirement: Public page explaining AI use and safeguards. / Acceptance: W36 renders / FSD trace: … | Partially covered | W30 privacy; BRL-PRV-01 | Data-rights and AI-transparency public pages | FR-V12-A-053..054 | Matched |
| A-12-0478 | Public storefront V5: W11/W07 offer optional, rule-based readiness reports and service recommendations; W06 adds a TCO and sensitivity estimator plus… | Partially covered | W06/W11/W31 | Storefront tools adopted | FR-V12-A-055..061 | Matched |
| AT-01 | AT-01 · P1 · Crawlable service pages / Requirement: Generate canonical production routes and metadata for each of 39 services; sitemap and public pro… | Partially covered | Sitemap; W31; W08; CAP-X3-12 | Storefront capability adopted | FR-V12-A-055..061 | Matched |
| AT-03 | AT-03 · P1 · Persona-based entry journeys / Requirement: Offer founder, marketing, sales and enterprise paths with relevant value propositions. / Acc… | Partially covered | Sitemap; W31; W08; CAP-X3-12 | Storefront capability adopted | FR-V12-A-055..061 | Matched |
| AT-04 | AT-04 · P1 · Transparent solution comparisons / Requirement: Explain capabilities, prerequisites and limitations compared with manual/point-tool alte… | Partially covered | Sitemap; W31; W08; CAP-X3-12 | Storefront capability adopted | FR-V12-A-055..061 | Matched |
| AT-05 | AT-05 · P1 · Free automation maturity assessment / Requirement: Collect nonidentifying readiness answers; compute explainable category score. / Accep… | Partially covered | Sitemap; W31; W08; CAP-X3-12 | Storefront capability adopted | FR-V12-A-055..061 | Matched |
| AT-06 | AT-06 · P1 · Personalized opportunity report / Requirement: Generate local report with score, reasons and suggested service IDs; no guarantee. / Acce… | Partially covered | Sitemap; W31; W08; CAP-X3-12 | Storefront capability adopted | FR-V12-A-055..061 | Matched |
| AT-07 | AT-07 · P1 · Controlled sandbox / Requirement: Expose synthetic sample execution with hard limits, no external effects and clear status. / Acceptance… | Partially covered | Sitemap; W31; W08; CAP-X3-12 | Storefront capability adopted | FR-V12-A-055..061 | Matched |
| AT-08 | AT-08 · P1 · Downloadable sample outputs / Requirement: Provide labeled fictional outputs for each of 39 services and associated workflows. / Accepta… | Partially covered | Sitemap; W31; W08; CAP-X3-12 | Storefront capability adopted | FR-V12-A-055..061 | Matched |
| AT-11 | AT-11 · P1 · Integration compatibility directory / Requirement: Show provider prerequisites, availability and last verification; no unsupported claim… | Partially covered | Sitemap; W31; W08; CAP-X3-12 | Storefront capability adopted | FR-V12-A-055..061 | Matched |
| AT-12 | AT-12 · P0 · Verified trust centre / Requirement: Disclose data ownership, security controls, operational status and evidence gaps. / Acceptance OPT-… | Partially covered | Sitemap; W31; W08; CAP-X3-12 | Storefront capability adopted | FR-V12-A-055..061 | Matched |
| AT-13 | AT-13 · P2 · Regional and multilingual content / Requirement: Version translations and locale/currency/timezone settings; review claims. / Acceptance… | Conflict | DEC-026 locales | en+hi at Release 2 Website chrome; de/fr/ar with market packs | DEC-516; CONFLICT-777 | Matched |
| CV-03 | CV-03 · P1 · Explainable recommended bundles / Requirement: Map objective, business model and constraints to SKU suggestions and optional prerequisit… | Partially covered | W11; W31; KPI-26 | Selection, TCO/ROI and conversion intelligence | FR-V12-A-056..060 | Matched |
| CV-04 | CV-04 · P1 · Side-by-side service comparison / Requirement: Compare output, limits, dependencies, meter and approved costs; unknown prices explicit. … | Partially covered | W11; W31; KPI-26 | Selection, TCO/ROI and conversion intelligence | FR-V12-A-056..060 | Matched |
| CV-06 | CV-06 · P1 · Total cost of ownership estimator / Requirement: Use customer-supplied subscription, provider, labor and implementation assumptions; sho… | Partially covered | W11; W31; KPI-26 | Selection, TCO/ROI and conversion intelligence | FR-V12-A-056..060 | Matched |
| CV-07 | CV-07 · P1 · Service-specific ROI sensitivity / Requirement: Compute estimated value from workload, time saved, labor and cost ranges; disclose assum… | Partially covered | W11; W31; KPI-26 | Selection, TCO/ROI and conversion intelligence | FR-V12-A-056..060 | Matched |
| CV-08 | CV-08 · P1 · Guided use-case demonstrations / Requirement: Show synthetic output walkthroughs relevant to chosen use case and selected SKUs. / Accept… | Partially covered | W11; W31; KPI-26 | Selection, TCO/ROI and conversion intelligence | FR-V12-A-056..060 | Matched |
| CV-15 | CV-15 · P1 · Operator conversion intelligence / Requirement: Track acquisition source and funnel events by cohort, industry and selected service; dis… | Partially covered | W11; W31; KPI-26 | Selection, TCO/ROI and conversion intelligence | FR-V12-A-056..060 | Matched |
| A-12-0504 | 34 route baseline, with public access only to neutral marketing/catalogue and minimal private intake. The 75 old selectable capability entries are no… | Conflict | Part 2.1 FR-W01..W34; Part 2.5 §2.x | Adopt neutral storefront routes; route remap by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W01 | Route: W01 / Name: Home / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W02 | Route: W02 / Name: Automation categories / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W03 | Route: W03 / Name: Automation family details / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W04 | Route: W04 / Name: Complete automation catalog / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W05 | Route: W05 / Name: Individual automation details / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W06 | Route: W06 / Name: Plans & automation selection / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W07 | Route: W07 / Name: Industry solution guide / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W08 | Route: W08 / Name: Resources & automation guides / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W09 | Route: W09 / Name: Illustrative use cases / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W10 | Route: W10 / Name: Campaign automation overview / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W11 | Route: W11 / Name: Automation selection assistant / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W12 | Route: W12 / Name: Service enquiry / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W13 | Route: W13 / Name: Product demo & partnership enquiry / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W14 | Route: W14 / Name: Custom quotation request / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W15 | Route: W15 / Name: Automation requirements builder / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W16 | Route: W16 / Name: Channel & integration options / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W17 | Route: W17 / Name: Service delivery models / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W18 | Route: W18 / Name: Consultation & demo booking / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W19 | Route: W19 / Name: Product webinars & events / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W20 | Route: W20 / Name: Service referral programme / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W21 | Route: W21 / Name: Client sign-in & recovery / Access / business outcome: Sign-in entry | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W22 | Route: W22 / Name: Client service dashboard / Access / business outcome: Authenticated client | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W23 | Route: W23 / Name: Subscription quotation review / Access / business outcome: Authenticated client | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W24 | Route: W24 / Name: Service agreement review / Access / business outcome: Authenticated client | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W25 | Route: W25 / Name: Subscription order status / Access / business outcome: Authenticated client | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W26 | Route: W26 / Name: Billing & invoice status / Access / business outcome: Authenticated client | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W27 | Route: W27 / Name: Private onboarding checklist / Access / business outcome: Authenticated client | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W28 | Route: W28 / Name: Support, feedback & renewal / Access / business outcome: Authenticated client | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W29 | Route: W29 / Name: Communication preferences / Access / business outcome: Authenticated client | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W30 | Route: W30 / Name: Contact, privacy & help / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W31 | Route: W31 / Name: Compare bundles & service coverage / Access / business outcome: Public | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W32 | Route: W32 / Name: Private client registration / Access / business outcome: Public entry | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W33 | Route: W33 / Name: Private configuration wizard / Access / business outcome: Authenticated client | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| W34 | Route: W34 / Name: Client service portal / Access / business outcome: Authenticated client | Conflict | Part 2.5 screen inventory (same ID, different purpose) | V12 route purpose adopted; ID namespacing V12-Wnn by Group G | DEC-505; CONFLICT-764; RECOMMENDATION-773 | Matched |
| A-12-0539 | W05 displays the four workflow contracts and opens a visible fictional output preview for each of 156 workflows. The artifact fields are derived from… | Partially covered | None | Workflow output previews for 156 workflows | FR-V12-A-058 | Matched |

#### 11.1.3.13 Chapter 13: Market Intelligence Lead Generation

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| MT-13 | MT-13 — Offering-specific audiences / Requirement: Separate ICP, segment, market eligibility and source rights by offering; no cross-product prospect… | Partially covered | Offering/ICP config | Offering-scoped audiences | FR-V12-A-078 | Matched |
| SM-SVC-01@13 | SKU: SM-SVC-01 / Business capability: Market & Competitive Intelligence Automation / Outcome: Evidence-linked market signals, competitor updates and … | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-02@13 | SKU: SM-SVC-02 / Business capability: Global Business Opportunity Discovery Automation / Outcome: Evidence-linked business opportunity records and al… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-03@13 | SKU: SM-SVC-03 / Business capability: B2B Contact & Decision-Maker Intelligence Automation / Outcome: Verified contact candidates, role mapping and c… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-04@13 | SKU: SM-SVC-04 / Business capability: Lead Qualification & Intelligent Matching Automation / Outcome: Qualified or held opportunities, fit explanatio… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-05@13 | SKU: SM-SVC-05 / Business capability: CRM & Sales Pipeline Automation / Outcome: Shared CRM records, pipeline state and next-action queue | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |

#### 11.1.3.14 Chapter 14: Digital Marketing Omnichannel Engagemen

**Covered (grouped, 1):** A-14-0546 → BR-M18/M19; DEC-029; PDP. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| MT-22 | MT-22 — Multiple independent channel configurations / Requirement: Company may have multiple channel accounts; offering-market mapping and independen… | Partially covered | Sender identities (Part 2.4) | Multiple accounts per channel/market | FR-V12-A-077 | Matched |
| MT-23 | MT-23 — Multiple accounts and sender identities / Requirement: Scoped provider identity, credential reference and sender aliases; no credential secre… | Partially covered | Sender identities (Part 2.4) | Multiple accounts per channel/market | FR-V12-A-077 | Matched |
| SM-SVC-06@14 | SKU: SM-SVC-06 / Business capability: Email Marketing & Outreach Automation / Outcome: Email drafts, dispatch status and delivery evidence | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-07@14 | SKU: SM-SVC-07 / Business capability: WhatsApp Business Marketing Automation / Outcome: Template decisions, message records and conversation updates | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-08@14 | SKU: SM-SVC-08 / Business capability: Omnichannel Follow-up & Lead Nurturing Automation / Outcome: Scheduled steps, follow-up drafts, paused sequence… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-09@14 | SKU: SM-SVC-09 / Business capability: AI Chat, Unified Inbox & Objection Automation / Outcome: Classified intent, evidence-grounded response, shared … | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-10@14 | SKU: SM-SVC-10 / Business capability: Meeting, Demo & Appointment Automation / Outcome: Confirmed or proposed appointments, briefings, reminders and … | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-11@14 | SKU: SM-SVC-11 / Business capability: Content Marketing Automation / Outcome: Content calendar, drafts, verified claims and approval queue | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-12@14 | SKU: SM-SVC-12 / Business capability: Social Media Publishing & Listening Automation / Outcome: Scheduled publications, provider status, permitted en… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-13@14 | SKU: SM-SVC-13 / Business capability: SEO & Search Visibility Automation / Outcome: SEO issue backlog, keyword plan and approved optimization drafts | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-14@14 | SKU: SM-SVC-14 / Business capability: Paid Digital Advertising Automation / Outcome: Approved campaign configuration, spend alerts and conversion rep… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-15@14 | SKU: SM-SVC-15 / Business capability: Landing Page & Website Lead Intake Automation / Outcome: Page draft, versioned form, captured leads and routing… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-16@14 | SKU: SM-SVC-16 / Business capability: Webinar, Event & Referral Acquisition Automation / Outcome: Registration records, eligible reminders, attendanc… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-26@14 | SKU: SM-SVC-26 / Business capability: AI Voice & Intelligent Telephony Automation / Outcome: Call disposition; Call event or hold; Booking or handoff… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-27@14 | SKU: SM-SVC-27 / Business capability: Multimodal Creative & Localization Automation / Outcome: Image drafts; Video draft; Localized asset; Creative Q… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-38@14 | SKU: SM-SVC-38 / Business capability: SMS, RCS & Business Messaging Automation / Outcome: Eligibility decision; Delivery event; Relationship update; … | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |

#### 11.1.3.15 Chapter 15: Sales Intelligence Revenue Conversion

**Covered (grouped, 2):** REC-28 → E-001..E-007 (Part 2.6); A-15-0564 → DEC-038; DEC-053; KPI-29. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| SM-SVC-17@15 | SKU: SM-SVC-17 / Business capability: Proposal & Quotation Automation / Outcome: Proposal and calculated quote with revision, approval and validity | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-18@15 | SKU: SM-SVC-18 / Business capability: Negotiation, Contract & MoU Automation / Outcome: Negotiation notes, contract draft, approved agreement and sig… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-19@15 | SKU: SM-SVC-19 / Business capability: Tender & Project Bid Automation / Outcome: Bid/no-bid assessment, draft response, submission and deadline tasks | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-20@15 | SKU: SM-SVC-20 / Business capability: Sales Order & Fulfillment Automation / Outcome: Purchase/sales order drafts, validated totals, milestones and a… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-21@15 | SKU: SM-SVC-21 / Business capability: Payment, Invoice & Reconciliation Automation / Outcome: Matched balances, discrepancy queue, verified closure s… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-24@15 | SKU: SM-SVC-24 / Business capability: Revenue, Attribution & Sales Forecast Automation / Outcome: Revenue dashboards, attribution, forecast scenarios… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-29@15 | SKU: SM-SVC-29 / Business capability: Account-Based Marketing & Enterprise Buying Group Automation / Outcome: Account plan; Buying group map; Account… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-36@15 | SKU: SM-SVC-36 / Business capability: AI Sales Enablement & Coaching Automation / Outcome: Playbook; Practice report; Coaching feedback; Training plan | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-37@15 | SKU: SM-SVC-37 / Business capability: Pricing, Offer & Revenue Optimization Automation / Outcome: Profitability report; Scenario report; Pricing expe… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |

#### 11.1.3.16 Chapter 16: Commerce Procurement Partner Operations

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| A-16-0574 | No autonomous commitment without mandate, explicit provider approval and reconciliation. Maintain inventory/version controls, partner sharing consent… | Conflict | DEC-064; X-06 | Commitments stay human-approved; mandate only for routine non-binding actions | DEC-508; CONFLICT-762 | Adopted (DEC-779) |
| SM-SVC-28@16 | SKU: SM-SVC-28 / Business capability: Agentic Commerce & AI-to-AI Business Transaction Automation / Outcome: Machine-readable catalog; Authorized quo… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-31@16 | SKU: SM-SVC-31 / Business capability: Marketplace & E-commerce Channel Operations Automation / Outcome: Listing state; Availability update; Order eve… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-32@16 | SKU: SM-SVC-32 / Business capability: Partner, Distributor & Co-Selling Automation / Outcome: Partner shortlist; Enablement record; Deal registration… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-39@16 | SKU: SM-SVC-39 / Business capability: Procurement & Supplier Management Automation / Outcome: Supplier shortlist and requirement; Quotation compariso… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |

#### 11.1.3.17 Chapter 17: Customer Success Retention Product Led

**Covered (grouped, 20):** A-17-0582, A-17-0583, A-17-0584, A-17-0585, A-17-0586, A-17-0587, A-17-0588, A-17-0589 → Part 8.3c CSO-01..12; CS-04, CS-05, CS-06, CS-08, CS-09 → A110; certainty badges; A084; Part 2.4 §2.30.5; MOB-05@17, MOB-14@17, MOB-17@17 → W21-W29 guard; Part 2.4 §2.30; RT-10, RT-14 → CSO-08/09; Part 9.8 QBR; REC-27 → CSO-11/12; A-17-0581 → Part 8.3c; Part 4.3; Part 8.3b (38-document pack coverage). All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| REC-25 | ID / priority / owner: REC-25 · P1 / Customer success / Source D33,34 / Required change: Contextual role guides, first-value and service activation c… | Not covered | None | First-value checklist | FR-V12-A-160..161 | Matched |
| A-17-0593 | Customer success: First value is the first reviewed and accepted service output, not merely login or a completed run. Establish service-specific time… | Not covered | None | First value = first accepted output | DEC-519; FR-V12-A-160 | Matched |
| RT-01 | RT-01 · P1 · Customer health scoring / Requirement: Use adoption, quality, value, reliability, support and renewal signals; show missing data and con… | Partially covered | Part 9.8a health v2; Part 8.3c report | Customer success capability | FR-V12-A-160..170 | Matched |
| RT-02 | RT-02 · P0 · Service first-value milestones / Requirement: Define first accepted deliverable for all 39 services and track time from activation. / Ac… | Partially covered | Part 9.8a health v2; Part 8.3c report | Customer success capability | FR-V12-A-160..170 | Matched |
| RT-03 | RT-03 · P1 · Personalized success plans / Requirement: Generate approved checklist from selected SKUs, data rights and connector readiness. / Accepta… | Partially covered | Part 9.8a health v2; Part 8.3c report | Customer success capability | FR-V12-A-160..170 | Matched |
| RT-04 | RT-04 · P1 · Underused-service detection / Requirement: Detect eligible inactive subscription and offer contextual guidance, not forced upsell. / Acc… | Partially covered | Part 9.8a health v2; Part 8.3c report | Customer success capability | FR-V12-A-160..170 | Matched |
| RT-05 | RT-05 · P1 · Connector and expiry alerts / Requirement: Notify authorized owner before credential/config expiry and on failure; respect preferences. … | Partially covered | Part 9.8a health v2; Part 8.3c report | Customer success capability | FR-V12-A-160..170 | Matched |
| RT-06 | RT-06 · P1 · Periodic customer value reports / Requirement: Show accepted outputs, usage, measured outcomes and assumptions by period. / Acceptance O… | Partially covered | Part 9.8a health v2; Part 8.3c report | Customer success capability | FR-V12-A-160..170 | Matched |
| RT-08 | RT-08 · P1 · Customer-controlled schedules / Requirement: Allow scoped pause, timezone-aware cadence and preferences under policy. / Acceptance OPT-T… | Partially covered | Part 9.8a health v2; Part 8.3c report | Customer success capability | FR-V12-A-160..170 | Matched |
| RT-09 | RT-09 · P1 · Evidence-based complementary services / Requirement: Recommend optional services using unmet objective and actual usage, with clear reas… | Partially covered | Part 9.8a health v2; Part 8.3c report | Customer success capability | FR-V12-A-160..170 | Matched |
| RT-12 | RT-12 · P1 · Cancellation reason and ethical win-back / Requirement: Allow cancellation without forced retention; optional reason and consented follo… | Partially covered | Part 9.8a health v2; Part 8.3c report | Customer success capability | FR-V12-A-160..170 | Matched |
| RT-13 | RT-13 · P1 · Adoption and training guidance / Requirement: Recommend tutorials using authorized adoption events and role preferences. / Acceptance OP… | Partially covered | Part 9.8a health v2; Part 8.3c report | Customer success capability | FR-V12-A-160..170 | Matched |
| RT-15 | RT-15 · P1 · Private product-feedback tracker / Requirement: Capture feature requests and status with authorized scope and resolution notice. / Accep… | Partially covered | Part 9.8a health v2; Part 8.3c report | Customer success capability | FR-V12-A-160..170 | Matched |
| CS-01 | CS-01 · P1 · Contextual guided tours / Requirement: Show service-specific setup and next action with optional dismiss and resume. / Acceptance OPT-TC… | Partially covered | CAP-X3-30; DEC-035 | Portal guidance and grounded help | FR-V12-A-166..169 | Matched |
| CS-02 | CS-02 · P1 · Searchable help and grounded AI support / Requirement: Retrieve approved scoped knowledge, cite version and route uncertainty to human. … | Partially covered | CAP-X3-30; DEC-035 | Portal guidance and grounded help | FR-V12-A-166..169 | Matched |
| CS-07 | CS-07 · P1 · Scoped correction memory / Requirement: Store approved corrections in tenant knowledge with provenance, expiry and revocation. / Accepta… | Partially covered | CAP-X3-30; DEC-035 | Portal guidance and grounded help | FR-V12-A-166..169 | Matched |
| CS-13 | CS-13 · P1 · Closed-loop feedback / Requirement: Assign owner, priority, status and resolution; notify customer under preferences. / Acceptance OPT-T… | Partially covered | CAP-X3-30; DEC-035 | Portal guidance and grounded help | FR-V12-A-166..169 | Matched |
| A-17-0616 | Define onboarding readiness, activation metrics, evidence-grounded support, SLA escalation, consented usage events, churn and reputation signals. Exp… | Partially covered | CSO-06/07 | Activation metrics | FR-V12-A-161 | Matched |
| SM-SVC-22@17 | SKU: SM-SVC-22 / Business capability: Customer, Partner & Institutional Onboarding Automation / Outcome: Onboarding plan, milestones, pilot/deploymen… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-23@17 | SKU: SM-SVC-23 / Business capability: Customer Retention, Renewal & Feedback Automation / Outcome: Renewal tasks, feedback insights and eligible re-e… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-25@17 | SKU: SM-SVC-25 / Business capability: Business Document & Knowledge Intelligence Automation / Outcome: Versioned knowledge entries, extracted metadat… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-30@17 | SKU: SM-SVC-30 / Business capability: Conversion Rate Optimization & Intelligent Experimentation Automation / Outcome: Funnel report; Experiment exec… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-33@17 | SKU: SM-SVC-33 / Business capability: Customer Service & Support Operations Automation / Outcome: Support case; Resolution or handover; SLA exception… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-34@17 | SKU: SM-SVC-34 / Business capability: Product-Led Growth & Usage Intelligence Automation / Outcome: Usage scorecard; Activation journey; Expansion re… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |
| SM-SVC-35@17 | SKU: SM-SVC-35 / Business capability: Brand Reputation & Review Intelligence Automation / Outcome: Review queue; Response draft; Incident alert; Impr… | Partially covered | Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk) | SKU mapped; service specification by Group B | FR-V12-A-001 | Matched |

#### 11.1.3.18 Chapter 18: AI Automation Authority Business Govern

**Covered (grouped, 23):** FL-05, FL-06, FL-07, FL-08, FL-11, FL-13, FL-14, FL-15 → Outbox; DEC-051; dry-run; Part 7.3; A113; REC-01, REC-03, REC-09, REC-11, REC-12@18 → A109; A111; DEC-051; PDP; DEC-061; BR-V7-AI-02@18, BR-V7-AI-03@18, BR-V7-AI-06@18, BR-V7-AI-08@18 → PDP; DEC-061; Part 6.4 injection; kill switch; MT-12, MT-28, MT-32, MT-35 → M02 claims; Part 2.35.3; A112; Part 7 registry; A-18-0629 → Part 1 §1.2.3 principles; MOB-09@18 → Step-up; no approval from notification. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| BR-V7-AI-01@18 | ID: BR-V7-AI-01 / Subject: AI transparency / Requirement: Customers and their contacts can see where AI is used; AI-generated messages and assets are… | Partially covered | AI disclosure labels | AI transparency page and labels | FR-V12-A-054; FR-V12-A-114 | Matched |
| BR-V7-AI-04@18 | ID: BR-V7-AI-04 / Subject: AI spend control / Requirement: Tenants set AI budgets; a hard cap prevents overspend; cost per accepted result is reporte… | Partially covered | DEC-008 hard caps | Cost per accepted result report | FR-V12-A-033; FR-V12-A-115 | Matched |
| BR-V7-AI-05@18 | ID: BR-V7-AI-05 / Subject: Customer data stays private / Requirement: Customer data is not used to train models and is processed in the tenant’s regi… | Partially covered | Provider DPA no-training; DEC-421 | India region now; EU with CONFLICT-761 | FR-V12-A-116 | Matched |
| BR-V7-AI-07@18 | ID: BR-V7-AI-07 / Subject: Launch languages / Requirement: Quality is proven for English and Hindi (India) and English, German and French (EU) before… | Partially covered | Part 6.4 eval sets (en) | Language slice gates | FR-V12-A-117 | Matched |
| A-18-0638 | Scope. Where AI may run: of 517 workflow steps, 159 are AI-inference steps; the rest are rules, policy gates, evidence retrieval or controlled effect… | Partially covered | Part 7.1 AI inventory | 159 of 517 steps AI; step detail Groups C/D/F | FR-V12-A-118 | Matched |
| FL-01 | FL-01 · P0 · Machine-readable workflow registry / Requirement: Version 156 workflow definitions; immutable run snapshots; stable SKU and workflow IDs… | Partially covered | WF-01..14; DEC-051 | 156-workflow registry; detail Groups C/D/E | FR-V12-A-002 | Matched |
| FL-02 | FL-02 · P0 · Canonical typed input contracts / Requirement: Replace descriptive-text heuristics with reviewed DTOs, types, ranges and required eviden… | Partially covered | WF-01..14; DEC-051 | 156-workflow registry; detail Groups C/D/E | FR-V12-A-002 | Matched |
| FL-03 | FL-03 · P0 · Executable step handlers / Requirement: Map 517 step IDs to executor, inputs, outputs, state transition, timeout, recovery and tests. / … | Partially covered | WF-01..14; DEC-051 | 156-workflow registry; detail Groups C/D/E | FR-V12-A-002 | Matched |
| FL-04 | FL-04 · P1 · Reusable child workflows / Requirement: Extract common research, evidence, validation, approval and reconciliation with versioned interf… | Partially covered | WF-01..14; DEC-051 | 156-workflow registry; detail Groups C/D/E | FR-V12-A-002 | Matched |
| FL-09 | FL-09 · P0 · Persistent approval mandates / Requirement: Bind actor, resource, payload digest, action, amount, policy, expiry and revocation. / Accep… | Conflict | DEC-064; Part 2.3 BRL-APR | Mandate record adopted for routine class only | DEC-508; CONFLICT-762; FR-V12-A-112 | Adopted (DEC-779) |
| FL-10 | FL-10 · P1 · Tenant-scoped cross-workflow events / Requirement: Share authorized business-object references with version and correlation; require tar… | Partially covered | WF-01..14; DEC-051 | 156-workflow registry; detail Groups C/D/E | FR-V12-A-002 | Matched |
| L0 | Authority: L0 / Business boundary: Manual action recorded | Conflict | DEC-064 autonomy cap; Part 9.2 glossary L0-L3 | Map V12 L0-L4 to L0-L3; consequential stays human-approved per action | DEC-508; CONFLICT-762; FR-V12-A-110..112 | Adopted (DEC-779) |
| L1 | Authority: L1 / Business boundary: AI proposes or drafts; human decides | Conflict | DEC-064 autonomy cap; Part 9.2 glossary L0-L3 | Map V12 L0-L4 to L0-L3; consequential stays human-approved per action | DEC-508; CONFLICT-762; FR-V12-A-110..112 | Adopted (DEC-779) |
| L2 | Authority: L2 / Business boundary: Exact approved action with reviewer, expiry and limits | Conflict | DEC-064 autonomy cap; Part 9.2 glossary L0-L3 | Map V12 L0-L4 to L0-L3; consequential stays human-approved per action | DEC-508; CONFLICT-762; FR-V12-A-110..112 | Adopted (DEC-779) |
| L3 | Authority: L3 / Business boundary: Bounded routine actions under approved mandate, scope, expiry and caps | Conflict | DEC-064 autonomy cap; Part 9.2 glossary L0-L3 | Map V12 L0-L4 to L0-L3; consequential stays human-approved per action | DEC-508; CONFLICT-762; FR-V12-A-110..112 | Adopted (DEC-779) |
| L4 | Authority: L4 / Business boundary: Adaptive orchestration inside L3 constraints; never expands authority | Conflict | DEC-064 autonomy cap; Part 9.2 glossary L0-L3 | Map V12 L0-L4 to L0-L3; consequential stays human-approved per action | DEC-508; CONFLICT-762; FR-V12-A-110..112 | Adopted (DEC-779) |
| A-18-0663 | R3 financial/legal/commitment actions default L2; regulatory or contractual requirements override any automation preference. No simulation external e… | Conflict | DEC-064; DEC-053 | V12-L2 equals blueprint L1 (exact human approval); mandates limited to routine class | DEC-508; CONFLICT-762 | Adopted (DEC-779) |

#### 11.1.3.19 Chapter 19: Portfolio Command Centre Business Analy

**Covered (grouped, 7):** REC-02, REC-06@19, REC-13 → A110; A106; saved views; MOB-06@19, MOB-07@19, MOB-08@19 → Part 2.5 responsive; MT-02 → Startup switcher (Part 2.5). All Matched.

**Not applicable (grouped, 4):** 3 × presentation inventory; screens owned by Group G; 1 × navigation rule; Group G.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| REC-14 | ID / priority / owner: REC-14 · P0 / Frontend lead / Source D06,17 / Required change: Cascading and multi-select filter semantics OR within/AND acros… | Partially covered | Part 2.4 §2.31 rules | Cascading filters and reconciled drill-down | FR-V12-A-123..124 | Matched |
| REC-15 | ID / priority / owner: REC-15 · P1 / Analytics lead / Source D06,17 / Required change: Timestamped scoped drill-down, record count, unknown indicator… | Partially covered | Part 2.4 §2.31 rules | Cascading filters and reconciled drill-down | FR-V12-A-123..124 | Matched |
| A-19-0676 | Universal Command Centre: A089 retains 14 management views and 9 V5 optimization laboratories. Context selection explicitly separates demo identity/m… | Partially covered | A089; Part 8.3c §8.3.5.15.7 | 14 views + 9 perspectives | DEC-509; FR-V12-A-120..121 | Matched |
| MT-25 | MT-25 — Restore business, offering and opportunity filters / Requirement: Company context and relevant primary/advanced filters prominently available… | Partially covered | Part 2.4 filters | Context filters | FR-V12-A-122..123 | Matched |
| MT-26 | MT-26 — Cascading context filters / Requirement: Changing tenant/company/division/brand/offer/market invalidates descendants; options derive from all… | Partially covered | Part 2.4 filters | Context filters | FR-V12-A-122..123 | Matched |
| A-19-0680 | Nine optimization views: A089 keeps its fourteen business management views; V5 adds nine integrated optimization laboratory perspectives: AI cost, Ge… | Partially covered | A089; Part 8.3c §8.3.5.15.7 | 14 views + 9 perspectives | DEC-509; FR-V12-A-120..121 | Matched |
| A-19-0681 | View within A089: Executive Overview / Management use: Business and workflow health; priority work | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0682 | View within A089: Market Intelligence / Management use: Evidence and market changes | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0683 | View within A089: Lead & Contact Intelligence / Management use: Lead fit and account intelligence | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0684 | View within A089: Digital Marketing / Management use: Campaign and content effectiveness | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0685 | View within A089: Omnichannel Engagement / Management use: Engagement and consent-safe channel activity | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0686 | View within A089: Follow-up & Meetings / Management use: Nurture and meeting status | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0687 | View within A089: Objection & Negotiation / Management use: Objection/negotiation exceptions | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0688 | View within A089: Sales Pipeline & Closure / Management use: Pipeline and closure priorities | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0689 | View within A089: Revenue & Financial Intelligence / Management use: Revenue, receipts and pricing | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0690 | View within A089: Customer Success / Management use: Onboarding and retention | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0691 | View within A089: Partner & Procurement / Management use: Partners, marketplace and procurement | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0692 | View within A089: AI & Automation Control / Management use: Run state, usage and controls | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0693 | View within A089: Governance & Risk / Management use: Approvals and policy exceptions | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0694 | View within A089: Optimization Intelligence / Management use: Experiment and optimization reviews | Partially covered | A089 | 14 views | FR-V12-A-120 | Matched |
| A-19-0695 | V4 chapter guidance: the current chapter registers defines the fourteen A089 views and role/scope filter behavior. | Partially covered | A089; Part 8.3c §8.3.5.15.7 | 14 views + 9 perspectives | DEC-509; FR-V12-A-120..121 | Matched |
| A-19-0696 | Private Command Centre: aggregate only approved companies and metrics; filter tenant/company, product, service, region, team, period, channel, stage … | Partially covered | DEC-055 | Object-level drill-down grant | DEC-509; FR-V12-A-125 | Matched |
| A-19-0697 | Each KPI is a labeled synthetic local aggregate. Do not substitute run counts for actual business outcomes. Production calculations require metric de… | Partially covered | A089; Part 8.3c §8.3.5.15.7 | 14 views + 9 perspectives | DEC-509; FR-V12-A-120..121 | Matched |
| A-19-0698 | No.: 1 / View: Executive performance / Local KPI labels: Opportunity records; Open pipeline; Won deals; Sample receipts / Measurement scope: Scoped s… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0699 | No.: 2 / View: Market intelligence / Local KPI labels: Market research runs; Evidence reviews; Held signals; Completed research / Measurement scope: … | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0700 | No.: 3 / View: Lead & contact intelligence / Local KPI labels: Discovered prospects; Qualified prospects; Contact & lead runs; Pending reviews / Meas… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0701 | No.: 4 / View: Digital marketing / Local KPI labels: Marketing runs; Completed campaigns; Held campaign actions; Sample marketing receipts / Measurem… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0702 | No.: 5 / View: Omnichannel engagement / Local KPI labels: Engagement runs; Completed messages / tasks; Held outreach; Channel records / Measurement s… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0703 | No.: 6 / View: Follow-up & meetings / Local KPI labels: Follow-up runs; Meeting-stage records; Pending approvals; Held tasks / Measurement scope: Sco… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0704 | No.: 7 / View: Objection & negotiation / Local KPI labels: Negotiation runs; Proposal-stage records; Awaiting review; Held negotiations / Measurement… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0705 | No.: 8 / View: Sales pipeline & closure / Local KPI labels: Open opportunities; Proposal-stage records; Won deals; Open pipeline / Measurement scope:… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0706 | No.: 9 / View: Revenue & financial intelligence / Local KPI labels: Sample receipts; Open pipeline; Won deals; Financial runs / Measurement scope: Sc… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0707 | No.: 10 / View: Customer success / Local KPI labels: Lifecycle runs; Completed lifecycle runs; Open reviews; Held lifecycle actions / Measurement sco… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0708 | No.: 11 / View: Partner & procurement / Local KPI labels: Partner / procurement runs; Completed runs; Pending reviews; Held purchasing actions / Meas… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0709 | No.: 12 / View: AI & automation control / Local KPI labels: Total runs; Completed runs; Reserved units; Held / failed runs / Measurement scope: Scope… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0710 | No.: 13 / View: Governance & risk / Local KPI labels: Awaiting approval; Held runs; Failed runs; Uncertain outcomes / Measurement scope: Scoped synth… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |
| A-19-0711 | No.: 14 / View: Optimization intelligence / Local KPI labels: Optimization runs; Completed runs; Pending review; Held experiments / Measurement scope… | Partially covered | A089; RP-01..30 | View KPI labels | FR-V12-A-121 | Matched |

#### 11.1.3.20 Chapter 20: Business Security Privacy Compliance

**Covered (grouped, 60):** SEC-01, SEC-02, SEC-03, SEC-04, SEC-06, SEC-07, SEC-08, SEC-09, SEC-10, SEC-11, SEC-12, SEC-13, SEC-14, SEC-15 → Part 4.1; Part 4.4a; CJ-GL-01, CJ-GL-02, CJ-GL-03, CJ-GL-04, CJ-GL-05, CJ-GL-06, CJ-GL-07, CJ-GL-08, CJ-GL-09, CJ-GL-10, CJ-GL-11, CJ-GL-12, CJ-GL-13 → BR-M18/M19/M56/M02/M04/M25/M10/M31/M57/M51/M42/M43/M36; CJ-IN-01, CJ-IN-02, CJ-IN-03, CJ-IN-04, CJ-IN-05, CJ-IN-06, CJ-IN-08, CJ-IN-09, CJ-IN-10, CJ-IN-11 → Part 4.1 DPDP/TRAI/CERT-In; DEC-027; DEC-030; BR-V7-CJ-02@20, BR-V7-CJ-03@20, BR-V7-CJ-06@20, BR-V7-CJ-08@20, BR-V7-CJ-09@20, BR-V7-CJ-11@20, BR-V7-CJ-12@20 → PDP; consent ledger; Part 4.1 breach; DEC-030; DPA; A-20-0738, A-20-0774, A-20-0775, A-20-0776, A-20-0777, A-20-0802 → Part 4.1 roles; DEC-029; BR-C05@20, BR-C06@20, BR-C11@20, BR-C14@20 → See BR-C rows (chapter 01); MT-20, MT-24 → Jurisdiction rule pack; consent ledger; REC-10@20 → Consent withdrawal scoped (Part 2.3); A-20-0724 → BR-M rules; MOB-10@20 → ADR-139 PWA offline drafts only; CS-15 → CSO-10/11. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| CJ-US-02 | Rule: CJ-US-02 / Market: US / Channel: Email / Obligation (summary): Commercial email: no deceptive headers or subject lines, identify as advertising… | Partially covered | DEC-029 (US/UK/AE/SG/AU summary) | Draft pack recorded, disabled until counsel approval | DEC-507; CONFLICT-766; FR-V12-A-131 | Matched |
| CJ-US-03 | Rule: CJ-US-03 / Market: US / Channel: SMS / Voice / Obligation (summary): Marketing calls and texts using automated systems need prior express writt… | Partially covered | DEC-029 (US/UK/AE/SG/AU summary) | Draft pack recorded, disabled until counsel approval | DEC-507; CONFLICT-766; FR-V12-A-131 | Matched |
| CJ-US-04 | Rule: CJ-US-04 / Market: US / Channel: Privacy / Obligation (summary): State privacy laws (e.g. California CCPA/CPRA): notice at collection; rights t… | Partially covered | DEC-029 (US/UK/AE/SG/AU summary) | Draft pack recorded, disabled until counsel approval | DEC-507; CONFLICT-766; FR-V12-A-131 | Matched |
| CJ-UK-02 | Rule: CJ-UK-02 / Market: UK / Channel: Email / SMS / Obligation (summary): Electronic marketing to individuals needs consent; soft opt-in only for ex… | Partially covered | DEC-029 (US/UK/AE/SG/AU summary) | Draft pack recorded, disabled until counsel approval | DEC-507; CONFLICT-766; FR-V12-A-131 | Matched |
| CJ-UK-03 | Rule: CJ-UK-03 / Market: UK / Channel: Platform / Obligation (summary): Data-subject requests within one month; reportable breaches to the ICO within… | Partially covered | DEC-029 (US/UK/AE/SG/AU summary) | Draft pack recorded, disabled until counsel approval | DEC-507; CONFLICT-766; FR-V12-A-131 | Matched |
| CJ-CA-01 | Rule: CJ-CA-01 / Market: CA / Channel: Electronic messages / Obligation (summary): Commercial electronic messages need express or implied consent, se… | Partially covered | DEC-029 (US/UK/AE/SG/AU summary) | Draft pack recorded, disabled until counsel approval | DEC-507; CONFLICT-766; FR-V12-A-131 | Matched |
| CJ-AU-01 | Rule: CJ-AU-01 / Market: AU / Channel: Email / SMS / Voice / Obligation (summary): Commercial messages need consent, sender identification and a func… | Partially covered | DEC-029 (US/UK/AE/SG/AU summary) | Draft pack recorded, disabled until counsel approval | DEC-507; CONFLICT-766; FR-V12-A-131 | Matched |
| CJ-SG-01 | Rule: CJ-SG-01 / Market: SG / Channel: SMS / Voice / Email / Obligation (summary): Check the Do Not Call Registry before marketing calls and messages… | Partially covered | DEC-029 (US/UK/AE/SG/AU summary) | Draft pack recorded, disabled until counsel approval | DEC-507; CONFLICT-766; FR-V12-A-131 | Matched |
| CJ-AE-01 | Rule: CJ-AE-01 / Market: AE / Channel: All / Obligation (summary): Lawful basis and consent for personal data processing, data-subject rights and cro… | Partially covered | DEC-029 (US/UK/AE/SG/AU summary) | Draft pack recorded, disabled until counsel approval | DEC-507; CONFLICT-766; FR-V12-A-131 | Matched |
| CJ-BR-01 | Rule: CJ-BR-01 / Market: BR / Channel: All / Obligation (summary): Legal basis for each processing purpose, data-subject rights and breach communicat… | Partially covered | DEC-029 (US/UK/AE/SG/AU summary) | Draft pack recorded, disabled until counsel approval | DEC-507; CONFLICT-766; FR-V12-A-131 | Matched |
| A-20-0722 | Each market opens only after qualified counsel approves its pack (ENT-CMP-08, DEC-V12-07). | Conflict | DEC-029 | Adopted | DEC-507; CONFLICT-766 | Matched |
| BR-V7-CJ-01@20 | ID: BR-V7-CJ-01 / Subject: Launch jurisdictions / Requirement: Launch in India with the EU as recommended second market; UK and US added later as con… | Conflict | DEC-029 Year-1 outbound allowlist | Market opens only after counsel approves its pack; IN first, EU second | DEC-507; CONFLICT-766; RECOMMENDATION-774 | Matched |
| BR-V7-CJ-04@20 | ID: BR-V7-CJ-04 / Subject: India telecom rules / Requirement: SMS and voice use registered DLT entities, headers and templates, scrub preference regi… | Partially covered | DLT; BRL-PRV; DEC-027 | DLT number series, nomination/grievance, EU VAT | FR-V12-A-132..134 | Matched |
| BR-V7-CJ-05@20 | ID: BR-V7-CJ-05 / Subject: Individual data rights / Requirement: Individuals can request access, correction, erasure, objection, grievance or nominat… | Partially covered | DLT; BRL-PRV; DEC-027 | DLT number series, nomination/grievance, EU VAT | FR-V12-A-132..134 | Matched |
| BR-V7-CJ-07@20 | ID: BR-V7-CJ-07 / Subject: Data residency / Requirement: Customers choose India or EU data region at onboarding; data stays there. / Acceptance: Cros… | Conflict | DEC-421 (Mumbai only); Part 2.4 §2.35.5 | India region through Release 2; EU/US region and tax provider at an approved R3/R5 gate | DEC-514; CONFLICT-761 | Adopted (DEC-772) |
| BR-V7-CJ-10@20 | ID: BR-V7-CJ-10 / Subject: Tax / Requirement: GST and VAT/OSS configuration approved before invoices are issued. / Acceptance: Invoice blocked withou… | Partially covered | DLT; BRL-PRV; DEC-027 | DLT number series, nomination/grievance, EU VAT | FR-V12-A-132..134 | Matched |
| CJ-IN-07 | Rule: CJ-IN-07 / Market: IN / Channel: Voice / Obligation: Promotional calls from the designated 140 number series; service/transactional calls from … | Not covered | None | 140/160 number series rule | FR-V12-A-133 | Matched |
| CJ-EU-01 | Rule: CJ-EU-01 / Market: EU / Channel: All / Obligation: A documented lawful basis per processing purpose; consent must be demonstrable and withdrawa… | Partially covered | DEC-029 EU rules | EU pack disabled until counsel approval | DEC-507; FR-V12-A-131 | Matched |
| CJ-EU-02 | Rule: CJ-EU-02 / Market: EU / Channel: Email / SMS / Obligation: Unsolicited electronic marketing to individuals needs prior consent; soft opt-in onl… | Partially covered | DEC-029 EU rules | EU pack disabled until counsel approval | DEC-507; FR-V12-A-131 | Matched |
| CJ-EU-03 | Rule: CJ-EU-03 / Market: EU / Channel: All / Obligation: Objection to direct marketing is absolute: stop processing for that purpose. / Legal source:… | Partially covered | DEC-029 EU rules | EU pack disabled until counsel approval | DEC-507; FR-V12-A-131 | Matched |
| CJ-EU-04 | Rule: CJ-EU-04 / Market: EU / Channel: All / Obligation: Respond to data-subject requests within one month (extendable by two months with reasons). /… | Partially covered | DEC-029 EU rules | EU pack disabled until counsel approval | DEC-507; FR-V12-A-131 | Matched |
| CJ-EU-05 | Rule: CJ-EU-05 / Market: EU / Channel: Platform / Obligation: Notify the supervisory authority within 72 hours of awareness; inform data subjects wit… | Partially covered | DEC-029 EU rules | EU pack disabled until counsel approval | DEC-507; FR-V12-A-131 | Matched |
| CJ-EU-06 | Rule: CJ-EU-06 / Market: EU / Channel: AI / Obligation: Solely automated decisions with legal or similarly significant effects need safeguards and hu… | Partially covered | DEC-029 EU rules | EU pack disabled until counsel approval | DEC-507; FR-V12-A-131 | Matched |
| CJ-EU-07 | Rule: CJ-EU-07 / Market: EU / Channel: Platform / Obligation: Transfers outside the EEA need adequacy or appropriate safeguards (e.g. SCCs plus trans… | Partially covered | DEC-029 EU rules | EU pack disabled until counsel approval | DEC-507; FR-V12-A-131 | Matched |
| CJ-EU-08 | Rule: CJ-EU-08 / Market: EU / Channel: Website / Obligation: Non-essential cookies and similar tracking require prior consent. / Legal source: ePriva… | Partially covered | DEC-029 EU rules | EU pack disabled until counsel approval | DEC-507; FR-V12-A-131 | Matched |
| CJ-EU-09 | Rule: CJ-EU-09 / Market: EU / Channel: AI / Obligation: Tell people when they interact with an AI system; mark AI-generated content in machine-readab… | Partially covered | AI disclosure | AI Act Art. 50 labels | FR-V12-A-114 | Matched |
| CJ-EU-10 | Rule: CJ-EU-10 / Market: EU / Channel: Billing / Obligation: VAT on B2C electronic services at the customer member-state rate via OSS; B2B reverse ch… | Conflict | DEC-421 (Mumbai only); Part 2.4 §2.35.5 | India region through Release 2; EU/US region and tax provider at an approved R3/R5 gate | DEC-514; CONFLICT-761 | Adopted (DEC-776) |
| CJ-UK-01 | Rule: CJ-UK-01 / Market: UK / Channel: Email / SMS / Obligation: Draft only: PECR and UK GDPR rules not yet reviewed; pack disabled. / Legal source: … | Conflict | DEC-029 Year-1 outbound allowlist | Market opens only after counsel approves its pack; IN first, EU second | DEC-507; CONFLICT-766; RECOMMENDATION-774 | Matched |
| CJ-US-01 | Rule: CJ-US-01 / Market: US / Channel: SMS / Voice / Obligation: Draft only: CAN-SPAM, TCPA and state privacy rules not yet reviewed; pack disabled. … | Conflict | DEC-029 Year-1 outbound allowlist | Market opens only after counsel approves its pack; IN first, EU second | DEC-507; CONFLICT-766; RECOMMENDATION-774 | Matched |
| BR-C01@20 | Control: BR-C01 / Business obligation: Public assets contain only approved platform service information and synthetic examples. No customer profiles,… | Conflict | FR-W02 directory; FR-W03 startup site; API-497; US-1905 | Neutral storefront; platform directory retired; startup sites only on tenant-verified pro… | DEC-505; CONFLICT-764; FR-V12-A-050..052 | Matched |
| BR-C09@20 | Control: BR-C09 / Business obligation: Draft/simulation no external effects. Real external actions require exact approval or eligible bounded mandate… | Conflict | DEC-064; BRL-APR-01 | Exact approval adopted; bounded mandate restricted to DEC-064 routine class | DEC-508; CONFLICT-762 | Adopted (DEC-779) |

#### 11.1.3.21 Chapter 21: SLA Support Service Delivery

**Covered (grouped, 36):** ST-01, ST-02, ST-03, ST-04, ST-05, ST-06, ST-07, ST-08, ST-09, ST-10, ST-11, ST-12, ST-13, ST-14, ST-15 → Part 4.2; Part 4.3; Part 4.4a; A-21-0815, A-21-0816, A-21-0817, A-21-0818, A-21-0819, A-21-0820, A-21-0821, A-21-0822 → Part 4.3 alerts; Part 4.4a; REC-22, REC-23, REC-24 → Part 3.6; Part 4.3; MNT calendar; A-21-0823, A-21-0825 → DEC-018; RC-2; CS-03, CS-10 → Support escalation; WCAG; A-21-0849, A-21-0850 → DEC-056; CSO-10/11; ENT-OPS-07 → SLA-09 post-incident ≤ 5 business days; A-21-0814 → Part 8.3c; Part 4.3; Part 8.3b (38-document pack coverage); MOB-12@21 → WCAG 2.2 AA; A-21-0845 → SLA-02. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| ENT-OPS-01 | ID: ENT-OPS-01 / Commitment: SLA tiers (proposed): Standard 99.5%, Business 99.9%, Enterprise 99.95% monthly, with service credits. / Acceptance: Con… | Partially covered | Part 8.3c SLA-02; DEC-018; DEC-044 | Standard/Business tiers adopted as contract templates; 99.95% tier needs Multi-AZ and 24x7 | DEC-510; FR-V12-A-140; CONFLICT-760 | Adopted (DEC-773) |
| ENT-OPS-02 | ID: ENT-OPS-02 / Commitment: Public status page with component status, incidents and maintenance. / Acceptance: Status page hosted independently of t… | Partially covered | Part 8.3c SLA-05/09; CAP-X3-12 | Severity, status page, tiered support | DEC-510; FR-V12-A-141..143 | Matched |
| ENT-OPS-03 | ID: ENT-OPS-03 / Commitment: Incident severity SEV1–SEV4 with communication timelines and incident commander roles. / Acceptance: Game-day drill meet… | Partially covered | Part 8.3c SLA-05/09; CAP-X3-12 | Severity, status page, tiered support | DEC-510; FR-V12-A-141..143 | Matched |
| ENT-OPS-04 | ID: ENT-OPS-04 / Commitment: 24×7 on-call for SEV1/SEV2 from R2. / Acceptance: Paging test each month. | Conflict | DEC-228 staffing; DEC-422 budget; Part 9.9a CAP-X3-17 | Separately costed enterprise-readiness proposal | DEC-513; CONFLICT-760; RECOMMENDATION-775 | Adopted (DEC-773) |
| ENT-OPS-05 | ID: ENT-OPS-05 / Commitment: Support desk with tiered response targets (proposed: Enterprise P1 1 h, Business 4 h, Standard next business day). / Acc… | Partially covered | Part 8.3c SLA-05/09; CAP-X3-12 | Severity, status page, tiered support | DEC-510; FR-V12-A-141..143 | Matched |
| ENT-OPS-06 | ID: ENT-OPS-06 / Commitment: Help centre and in-product guides, localised with the UI. / Acceptance: Top 50 tasks documented. | Partially covered | Part 8.3b help; DEC-026 | Help centre top-50 tasks | FR-V12-A-144 | Matched |
| REC-26 | ID / priority / owner: REC-26 · P1 / Service owner / Source D34 / Required change: Service-specific SLA, delivery responsibility, monthly value and a… | Partially covered | SLA framework | Per-SKU workflow SLA matrix | FR-V12-A-145 | Matched |
| A-21-0824 | Data class: Growth workload (critical) / RPO: ≤ 15 min / RTO: ≤ 2 h / KPI: KPI-18, KPI-32 / Verification: Growth recovery drill | Conflict | CONFLICT-462; NFR-057 | Growth RTO 2 h held as target pending cost | DEC-515; CONFLICT-765 | Adopted (DEC-790) |
| CS-11 | CS-11 · P1 · Service status and incident history / Requirement: Publish verified neutral service status and private scoped incident detail. / Accepta… | Partially covered | CAP-X3-12 | Public neutral status + private incident detail | FR-V12-A-142 | Matched |
| A-21-0846 | Service obligation: Support / Proposed baseline / acceptance: P1 critical initial response proposed 1 hour during contracted coverage; P2 4 business … | Partially covered | SLA-05 | P1 1 h / P2 4 h / P3 NBD as contract option | DEC-510 | Matched |
| A-21-0847 | Service obligation: Workflow SLA / Proposed baseline / acceptance: Define turnaround by SKU, volume, provider and approval wait; report p50/p95 exclu… | Not covered | None | Per-SKU turnaround p50/p95 excl. held | FR-V12-A-145 | Matched |
| A-21-0848 | Service obligation: Customer responsibilities / Proposed baseline / acceptance: Authorized source, usable inputs, configuration, consent, connector g… | Not covered | None | Customer responsibility schedule | FR-V12-A-146 | Matched |

#### 11.1.3.22 Chapter 22: Business KPI Performance Framework

**Covered (grouped, 66):** KPI-01, KPI-02, KPI-03, KPI-04, KPI-05, KPI-06, KPI-07, KPI-08, KPI-09, KPI-10, KPI-11, KPI-12, KPI-13, KPI-14, KPI-15, KPI-16, KPI-17, KPI-18, KPI-19, KPI-20, KPI-21, KPI-22, KPI-23, KPI-24, KPI-25, KPI-26, KPI-27, KPI- → Part 8.3c §8.3.5.15.4 OKPI-nn (alias of V12 KPI-nn); A-22-0852, A-22-0853, A-22-0854, A-22-0855, A-22-0856, A-22-0857, A-22-0858, A-22-0859, A-22-0860, A-22-0861, A-22-0862, A-22-0863, A-22-0864, A-22-0865, A-22-0866, A-22-0867, A-22-0868, A-22-0869, A-22-0870, A-22-0871 → Part 8.3c OPT-01..20 weights; A-22-0922, A-22-0923, A-22-0927, A-22-0928, A-22-0931, A-22-0932 → 8.3c cohort metrics; KPI-09/13/16/29; MT-27, MT-31, MT-40 → Part 2.4 §2.31; Part 9.3 duplicate-ID scan; A-22-0872, REC-16 → Part 8.3c §8.3.5.15.1; A-22-0915 → Part 2.4 §2.31.2. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| KPI-32 | KPI: KPI-32 / Metric: Growth critical RTO / Target: ≤ 120 minutes / Gate: Blocking | Conflict | Part 4.4a OKPI-32; CONFLICT-462 (RC-1) | Adopt 2 h growth RTO as target; binding needs Topology B cost approval | DEC-515; CONFLICT-765; FR-V12-A-147 | Adopted (DEC-790) |
| A-22-0908 | KPI: AI evaluation pass rate / Definition: AI-enabled workflows with a passing current suite ÷ AI-enabled workflows / Target: 100% before go-live / O… | Partially covered | Part 6.4; Part 4.1 | AI/compliance KPI registered | DEC-511; FR-V12-A-150; ASSUMPTION-772 | Matched |
| A-22-0909 | KPI: Cost per accepted result / Definition: AI + provider + retry cost ÷ accepted outputs, per workflow / Target: Baseline in pilot; owner sets targe… | Partially covered | Part 6.4; Part 4.1 | AI/compliance KPI registered | DEC-511; FR-V12-A-150; ASSUMPTION-772 | Matched |
| A-22-0910 | KPI: Injection red-team violations / Definition: Policy violations in AI-INJ suite / Target: 0 / Owner: Security | Partially covered | Part 6.4; Part 4.1 | AI/compliance KPI registered | DEC-511; FR-V12-A-150; ASSUMPTION-772 | Matched |
| A-22-0911 | KPI: Preflight hold rate / Definition: Effects held by jurisdiction preflight ÷ effects attempted / Target: Monitored; spikes investigated / Owner: C… | Partially covered | Part 6.4; Part 4.1 | AI/compliance KPI registered | DEC-511; FR-V12-A-150; ASSUMPTION-772 | Matched |
| A-22-0912 | KPI: DSAR on-time rate / Definition: Requests closed by due date ÷ requests due / Target: 100% / Owner: Privacy operations | Partially covered | Part 6.4; Part 4.1 | AI/compliance KPI registered | DEC-511; FR-V12-A-150; ASSUMPTION-772 | Matched |
| A-22-0913 | KPI: Breach notification on-time / Definition: Notifications made before statutory deadline / Target: 100% / Owner: Security | Partially covered | Part 6.4; Part 4.1 | AI/compliance KPI registered | DEC-511; FR-V12-A-150; ASSUMPTION-772 | Matched |
| A-22-0914 | KPI: Consent coverage / Definition: Sends with a valid consent/basis record ÷ sends / Target: 100% / Owner: Compliance | Partially covered | Part 6.4; Part 4.1 | AI/compliance KPI registered | DEC-511; FR-V12-A-150; ASSUMPTION-772 | Matched |
| A-22-0919 | Metric definitions: Cost per accepted result = eligible execution costs / accepted outputs; undefined when denominator zero. CAC = eligible acquisiti… | Partially covered | Part 1 §1.4.2 rules; CAP-X3-04 | Metric registry | DEC-511; FR-V12-A-151..152 | Matched |
| CS-12 | CS-12 · P1 · CSAT, CES and NPS measurement / Requirement: Collect optional feedback at defined milestones; report denominator and period. / Acceptanc… | Partially covered | Part 9.8 NPS/CSAT | CSAT/CES/NPS definitions | FR-V12-A-153 | Matched |
| A-22-0921 | KPI: MRR / Formula / source / period: Sum recurring subscription revenue normalized monthly; exclude one-off and pass-through; billing ledger monthly | Partially covered | KPI-10; KPI-25 | Business KPI registered | DEC-511; FR-V12-A-150 | Matched |
| A-22-0924 | KPI: Activation / Formula / source / period: Activated eligible tenants / verified new tenants; cohort weekly | Partially covered | KPI-10; KPI-25 | Business KPI registered | DEC-511; FR-V12-A-150 | Matched |
| A-22-0925 | KPI: Accepted result rate / Formula / source / period: Accepted outputs / completed eligible runs; per workflow version weekly | Partially covered | KPI-10; KPI-25 | Business KPI registered | DEC-511; FR-V12-A-150 | Matched |
| A-22-0926 | KPI: Lead-to-opportunity / Formula / source / period: Qualified opportunity count / eligible lead cohort; CRM monthly | Partially covered | KPI-10; KPI-25 | Business KPI registered | DEC-511; FR-V12-A-150 | Matched |
| A-22-0929 | KPI: ROAS / Formula / source / period: Attributed eligible revenue / ad spend; attribution version and window; channel monthly | Partially covered | KPI-10; KPI-25 | Business KPI registered | DEC-511; FR-V12-A-150 | Matched |
| A-22-0930 | KPI: CAC / LTV / Formula / source / period: Acquisition spend / new customers; discounted or cohort-based contribution estimate with assumptions | Partially covered | KPI-10; KPI-25 | Business KPI registered | DEC-511; FR-V12-A-150 | Matched |
| A-22-0933 | Metric owner, approved denominator, event sources, version, period, filters, freshness and threshold must be stored in metric registry. Zero denomina… | Partially covered | Part 1 §1.4.2 rules; CAP-X3-04 | Metric registry | DEC-511; FR-V12-A-151..152 | Matched |

#### 11.1.3.23 Chapter 23: Roadmap Prioritization Commercial Readi

**Covered (grouped, 12):** GO-01, GO-02, GO-03, GO-04, GO-05, GO-06, GO-07, GO-08 → Part 8.2 go-live; REC-20, REC-21 → Part 6.9 backlog; Part 4.3 pipeline; A-23-0940 → Part 8.1 estimates; MT-39 → DEC-031; AP-01; Part 6.7. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| R0 | Phase: R0 / Name: Foundations / Scope: Build core platform from Appendices A–C/A2/C2; identity reuse; CI/CD with SAST/DAST/SBOM; infrastructure as co… | Partially covered | Part 8.1 W0-W2; DEC-034 | R0 mapped to W0-W2 | DEC-512; ASSUMPTION-770; FR-V12-A-190 | Matched |
| R1@23 | Phase: R1 / Name: Private beta — India (owned companies) / Scope: SSO/MFA, audit, API keys, webhooks, exports, connectors for email/WhatsApp/SMS-DLT/… | Conflict | Part 8.1 waves; DEC-411 A1-A3; DEC-230/422 | Map phase to waves/A-releases; beyond-budget items costed separately | DEC-512; CONFLICT-760; ASSUMPTION-770 | Adopted (DEC-784) |
| R2@23 | Phase: R2 / Name: General availability — India / Scope: Billing and tax live, status page, support desk, SLA tiers, custom roles, SCIM, sandbox; WCAG… | Conflict | Part 8.1 waves; DEC-411 A1-A3; DEC-230/422 | Map phase to waves/A-releases; beyond-budget items costed separately | DEC-512; CONFLICT-760; ASSUMPTION-770 | Adopted (DEC-774) |
| R3@23 | Phase: R3 / Name: EU launch / Scope: EU region, GDPR/ePrivacy/AI Act assessments, German/French locales, BYOK, SDKs, bug bounty. / Exit criteria: SOC… | Conflict | DEC-421; DEC-411 | EU launch needs EU region and budget | DEC-512; DEC-514; CONFLICT-761 | Adopted (DEC-772) |
| R4@23 | Phase: R4 / Name: UK, Middle East and APAC / Scope: UK, UAE, Singapore, Australia packs and providers; Arabic (RTL); partner programme. / Exit criter… | Conflict | Part 8.1 waves; DEC-411 A1-A3; DEC-230/422 | Map phase to waves/A-releases; beyond-budget items costed separately | DEC-512; CONFLICT-760; ASSUMPTION-770 | Adopted (DEC-776) |
| R5 | Phase: R5 / Name: Americas / Scope: US (CAN-SPAM, TCPA, state privacy), Canada (CASL), Brazil (LGPD); US region. / Exit criteria: Packs approved; US … | Conflict | Part 8.1 waves; DEC-411 A1-A3; DEC-230/422 | Map phase to waves/A-releases; beyond-budget items costed separately | DEC-512; CONFLICT-760; ASSUMPTION-770 | Adopted (DEC-790) |
| A-23-0952 | Execution order: 54 P0 controls gate affected production releases, followed by 76 P1 optimization items and 5 P2 maturity items. Sequence security, s… | Partially covered | Part 8.1 waves | P0/P1/P2 gating | FR-V12-A-191 | Matched |
| P0 | Priority: P0 / Count: 54 / Gate: Applicable production release blocker until accepted | Partially covered | Part 8.1 MoSCoW | Priority gates | FR-V12-A-191 | Matched |
| P1@23 | Priority: P1 / Count: 76 / Gate: High-value optimization; schedule by measured opportunity | Partially covered | Part 8.1 MoSCoW | Priority gates | FR-V12-A-191 | Matched |
| P2@23 | Priority: P2 / Count: 5 / Gate: Advanced maturity; approve business case | Partially covered | Part 8.1 MoSCoW | Priority gates | FR-V12-A-191 | Matched |
| A-23-0956 | Release gate: Foundation / Proposed scope / dependency: Identity reuse verification; isolation, entitlements, quote/billing, workflow registry, audit… | Partially covered | Part 8.1 waves | SKU release groups mapped | FR-V12-A-192 | Matched |
| R1@23.2 | Release gate: R1 intelligence / Proposed scope / dependency: SVC 01–05, 25 with licensed inputs and evidence | Conflict | Part 8.1 waves; DEC-411 A1-A3; DEC-230/422 | Map phase to waves/A-releases; beyond-budget items costed separately | DEC-512; CONFLICT-760; ASSUMPTION-770 | Adopted (DEC-790) |
| R2@23.2 | Release gate: R2 engagement / Proposed scope / dependency: SVC 06–13,15–16; approved channels and consent | Conflict | Part 8.1 waves; DEC-411 A1-A3; DEC-230/422 | Map phase to waves/A-releases; beyond-budget items costed separately | DEC-512; CONFLICT-760; ASSUMPTION-770 | Adopted (DEC-790) |
| R3@23.2 | Release gate: R3 conversion / Proposed scope / dependency: SVC 17–24,29,32–33; finance/legal and integrations | Partially covered | Part 8.1 waves | SKU release groups mapped | FR-V12-A-192 | Matched |
| R4@23.2 | Release gate: R4 advanced / Proposed scope / dependency: SVC 14,26–28,30–31,34–39 after pilot, provider capability, risk and economic approval | Conflict | Part 8.1 waves; DEC-411 A1-A3; DEC-230/422 | Map phase to waves/A-releases; beyond-budget items costed separately | DEC-512; CONFLICT-760; ASSUMPTION-770 | Adopted (DEC-790) |
| A-23-0961 | Release tags are proposed planning groups only. Full suite means all released eligible SKUs. No artificial target dates or approved backlog estimates. | Partially covered | Part 8.1 waves | P0/P1/P2 gating | FR-V12-A-191 | Matched |

#### 11.1.3.24 Chapter 24: Business Acceptance Requirement Traceab

**Covered (grouped, 140):** V8-QA-001, V8-QA-002, V8-QA-003, V8-QA-004, V8-QA-005, V8-QA-006, V8-QA-007, V8-QA-008, V8-QA-009, V8-QA-010, V8-QA-011, V8-QA-012, V8-QA-013, V8-QA-014, V8-QA-015, V8-QA-016, V8-QA-017, V8-QA-018, V8-QA-019, V8-QA-020,  → Part 6 regression (see §11.1.4 V8-QA map); XS-01, XS-02, XS-03, XS-04, XS-05, XS-06, XS-07, XS-08, XS-09, XS-10 → AP-01..09; Part 6; A-24-1019, A-24-1080, A-24-1187, A-24-1188, A-24-1189, A-24-1190, A-24-1191, A-24-1192, A-24-1193 → Part 8.2 release gates; Part 6.6 RTM; E-001, E-002, E-003, E-004, E-005, E-006, E-007 → Part 2.6 E-001..E-007; BR-V7-CJ-02@24, BR-V7-CJ-03@24, BR-V7-CJ-06@24, BR-V7-CJ-08@24, BR-V7-CJ-09@24, BR-V7-CJ-11@24, BR-V7-CJ-12@24 → PDP; consent ledger; Part 4.1 breach; DEC-030; DPA; A-24-1014, A-24-1015, A-24-1016, A-24-1017, A-24-1018 → Parts 3.5/3.6/6.8/6.9 reconciliation; BR-V7-AI-02@24, BR-V7-AI-03@24, BR-V7-AI-06@24, BR-V7-AI-08@24 → PDP; DEC-061; Part 6.4 injection; kill switch; REC-17, REC-18, REC-19 → Parts 3.5, 3.6, 6.8, 6.9; MOB-05@24, MOB-14@24, MOB-17@24 → W21-W29 guard; Part 2.4 §2.30; MOB-06@24, MOB-07@24, MOB-08@24 → Part 2.5 responsive; BR-V7-ADM-01@24, BR-V7-ADM-02@24, BR-V7-ADM-03@24 → BRL-APR-01; DEC-050; Part 2.5; MT-36, MT-37, MT-38 → Part 3.5; design system; Part 6.8; MOB-02@24, MOB-03@24 → DEC-043; Part 2.5 responsive; MOB-18@24, MOB-18@24.2 → DEC-043 one codebase; BR-V7-WEB-01@24, BR-V7-WEB-02@24 → Part 2.5 UI states; WCAG 2.2 AA; MOB-01@24 → DEC-043; MOB-09@24 → Step-up; no approval from notification; MOB-10@24 → ADR-139 PWA offline drafts only; MOB-12@24 → WCAG 2.2 AA; MOB-13@24 → OKPI-29..31; NFR web vitals; MOB-15@24 → DEC-027; MT-21. All Matched.

**Not applicable (grouped, 82):** 54 × customer's RCTCFE self-scores of its own artifacts; 6 × prototype evidence statement; 4 × customer REC status counts; 5 × prototype test evidence; 13 × prototype browser evidence.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| A-24-0962 | Area: Product functionality (39 services / 156 workflows) / Specified: Yes / Prototype: Yes (simulated) / Production: No | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| A-24-0963 | Area: Multi-tenant isolation / Specified: Yes (DDL + RLS tested) / Prototype: Yes / Production: No | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| A-24-0964 | Area: Identity: SSO, SCIM, MFA, sessions / Specified: Yes (V12) / Prototype: Yes (A122, simulated IdP) / Production: No | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-784) |
| A-24-0965 | Area: Custom roles, separation of duties, audit/SIEM / Specified: Yes (V12) / Prototype: Yes (A123, A124) / Production: No | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-775) |
| A-24-0966 | Area: API platform, webhooks, SDKs, developer portal / Specified: Yes (V12, OpenAPI A2) / Prototype: Partly (A125, W39) / Production: No | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-785) |
| A-24-0967 | Area: Data export, residency, BYOK, sandboxes / Specified: Yes (V12) / Prototype: Yes (A126, A127) / Production: No | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-772) |
| A-24-0968 | Area: Integrations / connectors / Specified: Yes (INT-01…11) / Prototype: Simulated (A128) / Production: No | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-785) |
| A-24-0969 | Area: AI governance and evaluation / Specified: Yes / Prototype: Yes (A114–A117) / Production: No (no approved models) | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| A-24-0970 | Area: Compliance: jurisdictions, consent, DSAR, breach / Specified: Yes (IN, EU; 7 more markets draft) / Prototype: Yes (A118–A121, W35) / Production… | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| A-24-0971 | Area: Security programme and certifications / Specified: Yes (V12) / Prototype: Tracker only (A129) / Production: No (no audit or pen test yet) | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-775) |
| A-24-0972 | Area: Reliability: SLOs, incidents, status, DR / Specified: Yes / Prototype: Simulated (A130, W40) / Production: No (no drills) | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-775) |
| A-24-0973 | Area: Global readiness: locales, RTL, tax, regions / Specified: Yes (V12) / Prototype: Partial (5 locales on key pages, A131 tax preview) / Productio… | Partially covered | Part 9.9a CAP-X3-12..27; Part 4.1 | Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved bud… | FR-V12-A-180..189; CONFLICT-760 | Adopted (DEC-776) |
| A-24-0974 | Area: Business operations: billing, support, contracts / Specified: Yes (V12) / Prototype: Preview (A131) / Production: No | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| A-24-0975 | Area: Accessibility / Specified: Yes (WCAG 2.2 AA target) / Prototype: Automated WCAG 2.1 A/AA pass / Production: No manual audit | Partially covered | Part 9.3 quality report | Readiness register adopted | FR-V12-A-200 | Matched |
| MOB-04@24 | MOB: MOB-04 / Title: Progressive onboarding / V8 change: Inline, announced field errors on registration and wizard; focus to first error. | Partially covered | W32/W33; BRL-SVC-02 | Eight-stage wizard | FR-V12-A-090..092 | Matched |
| MOB-11@24 | MOB: MOB-11 / Title: Session and draft recovery / V8 change: No change in V8. | Partially covered | W32/W33; BRL-SVC-02 | Eight-stage wizard | FR-V12-A-090..092 | Matched |
| MOB-16@24 | MOB: MOB-16 / Title: Cross-device application handoff / V8 change: No change; SM-APPLICATION-6 unchanged. | Not covered | None | Cross-device signed handoff | FR-V12-A-095 | Matched |
| BR-V7-AI-01@24 | BR ID: BR-V7-AI-01 / FSD requirements: CJ-R13, AIX-11 / Screens: W36, A116 / Acceptance evidence: W36 published; undisclosed AI content held in EU ma… | Partially covered | AI disclosure labels | AI transparency page and labels | FR-V12-A-054; FR-V12-A-114 | Matched |
| BR-V7-AI-04@24 | BR ID: BR-V7-AI-04 / FSD requirements: AIX-12…14 / Screens: A117 / Acceptance evidence: Hard cap holds AI steps; report shows denominator. | Partially covered | DEC-008 hard caps | Cost per accepted result report | FR-V12-A-033; FR-V12-A-115 | Matched |
| BR-V7-AI-05@24 | BR ID: BR-V7-AI-05 / FSD requirements: AIX-17, CJ-R09 / Screens: A114 / Acceptance evidence: Provider DPA evidence; region pinning test. | Partially covered | Provider DPA no-training; DEC-421 | India region now; EU with CONFLICT-761 | FR-V12-A-116 | Matched |
| BR-V7-AI-07@24 | BR ID: BR-V7-AI-07 / FSD requirements: AIX-19 / Screens: A115 / Acceptance evidence: Language slice gates pass. | Partially covered | Part 6.4 eval sets (en) | Language slice gates | FR-V12-A-117 | Matched |
| BR-V7-CJ-01@24 | BR ID: BR-V7-CJ-01 / FSD requirements: CJ-R01, CJ-R19, DEC-V7-01 / Screens: A118 / Acceptance evidence: Approved IN and EU packs; UK/US disabled draf… | Conflict | DEC-029 Year-1 outbound allowlist | Market opens only after counsel approves its pack; IN first, EU second | DEC-507; CONFLICT-766; RECOMMENDATION-774 | Matched |
| BR-V7-CJ-04@24 | BR ID: BR-V7-CJ-04 / FSD requirements: CJ-R06 / Screens: A118 / Acceptance evidence: Unregistered or unscrubbed send held. | Partially covered | DLT; BRL-PRV; DEC-027 | DLT number series, nomination/grievance, EU VAT | FR-V12-A-132..134 | Matched |
| BR-V7-CJ-05@24 | BR ID: BR-V7-CJ-05 / FSD requirements: CJ-R07 / Screens: W35, A120 / Acceptance evidence: W35 intake; due dates per pack; legal-hold reason recorded. | Partially covered | DLT; BRL-PRV; DEC-027 | DLT number series, nomination/grievance, EU VAT | FR-V12-A-132..134 | Matched |
| BR-V7-CJ-07@24 | BR ID: BR-V7-CJ-07 / FSD requirements: CJ-R09, DEC-V7-08 / Screens: W33 / Acceptance evidence: Cross-region write test fails. | Conflict | DEC-421 (Mumbai only); Part 2.4 §2.35.5 | India region through Release 2; EU/US region and tax provider at an approved R3/R5 gate | DEC-514; CONFLICT-761 | Adopted (DEC-776) |
| BR-V7-CJ-10@24 | BR ID: BR-V7-CJ-10 / FSD requirements: CJ-R16 / Screens: O03/O04 / Acceptance evidence: Invoice blocked without approval. | Partially covered | DLT; BRL-PRV; DEC-027 | DLT number series, nomination/grievance, EU VAT | FR-V12-A-132..134 | Matched |
| BR-V7-WEB-03@24 | BR ID: BR-V7-WEB-03 / FSD requirements: CJ-R07 / Screens: W35 / Acceptance evidence: PT-V7-07 | Partially covered | W30 privacy; BRL-PRV-01 | Data-rights and AI-transparency public pages | FR-V12-A-053..054 | Matched |
| BR-V7-WEB-04@24 | BR ID: BR-V7-WEB-04 / FSD requirements: CJ-R13 / Screens: W36 / Acceptance evidence: W36 renders | Partially covered | W30 privacy; BRL-PRV-01 | Data-rights and AI-transparency public pages | FR-V12-A-053..054 | Matched |
| A-24-1197 | Acceptance and traceability: All 135 IDs have acceptance tests OPT-TC-{ID} in the corresponding BRD and FSD chapter register. These are proposed prod… | Partially covered | None | OPT-TC alias to TC-V12-A | FR-V12-A-201 | Matched |
| SM-SVC-01-ENT-AT01 | Test: SM-SVC-01-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-02-ENT-AT01 | Test: SM-SVC-02-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-03-ENT-AT01 | Test: SM-SVC-03-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-04-ENT-AT01 | Test: SM-SVC-04-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-05-ENT-AT01 | Test: SM-SVC-05-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-06-ENT-AT01 | Test: SM-SVC-06-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-07-ENT-AT01 | Test: SM-SVC-07-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-08-ENT-AT01 | Test: SM-SVC-08-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-09-ENT-AT01 | Test: SM-SVC-09-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-10-ENT-AT01 | Test: SM-SVC-10-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-11-ENT-AT01 | Test: SM-SVC-11-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-12-ENT-AT01 | Test: SM-SVC-12-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-13-ENT-AT01 | Test: SM-SVC-13-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-14-ENT-AT01 | Test: SM-SVC-14-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-15-ENT-AT01 | Test: SM-SVC-15-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-16-ENT-AT01 | Test: SM-SVC-16-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-17-ENT-AT01 | Test: SM-SVC-17-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-18-ENT-AT01 | Test: SM-SVC-18-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-19-ENT-AT01 | Test: SM-SVC-19-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-20-ENT-AT01 | Test: SM-SVC-20-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-21-ENT-AT01 | Test: SM-SVC-21-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-22-ENT-AT01 | Test: SM-SVC-22-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-23-ENT-AT01 | Test: SM-SVC-23-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-24-ENT-AT01 | Test: SM-SVC-24-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-25-ENT-AT01 | Test: SM-SVC-25-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-26-ENT-AT01 | Test: SM-SVC-26-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-27-ENT-AT01 | Test: SM-SVC-27-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-28-ENT-AT01 | Test: SM-SVC-28-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-29-ENT-AT01 | Test: SM-SVC-29-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-30-ENT-AT01 | Test: SM-SVC-30-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-31-ENT-AT01 | Test: SM-SVC-31-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-32-ENT-AT01 | Test: SM-SVC-32-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-33-ENT-AT01 | Test: SM-SVC-33-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-34-ENT-AT01 | Test: SM-SVC-34-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-35-ENT-AT01 | Test: SM-SVC-35-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-36-ENT-AT01 | Test: SM-SVC-36-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-37-ENT-AT01 | Test: SM-SVC-37-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-38-ENT-AT01 | Test: SM-SVC-38-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| SM-SVC-39-ENT-AT01 | Test: SM-SVC-39-ENT-AT01 / Scenario: Single SKU, authorized equivalent input; no upstream purchase / Expected: Activate with foundation; unrelated SK… | Not covered | None (no SKU entitlement test) | Parameterised SKU entitlement test | TC-V12-A-020 | Matched |
| A-24-1238 | Business acceptance owner signs deliverable, limits, SLA, pricing and rights per SKU. QA links actual evidence; all scenarios remain not run. FSD cha… | Not covered | Part 8.2 sign-off (not per SKU) | Per-SKU acceptance record | FR-V12-A-202 | Matched |
| A-24-1243 | Check: application_invalidation / Observed result: True / Test scope: Targeted Chromium test; synthetic local prototype only | Partially covered | US-2004; BRL-SVC-03 | Behaviour covered by TC-V12-A | TC-V12-A-095..099 | Matched |
| A-24-1246 | Check: duplicate_import / Observed result: True / Test scope: Targeted Chromium test; synthetic local prototype only | Partially covered | US-2004; BRL-SVC-03 | Behaviour covered by TC-V12-A | TC-V12-A-095..099 | Matched |
| A-24-1247 | Check: new_revision_updates_pending / Observed result: True / Test scope: Targeted Chromium test; synthetic local prototype only | Partially covered | US-2004; BRL-SVC-03 | Behaviour covered by TC-V12-A | TC-V12-A-095..099 | Matched |
| A-24-1248 | Check: fingerprint_reject / Observed result: True / Test scope: Targeted Chromium test; synthetic local prototype only | Partially covered | US-2004; BRL-SVC-03 | Behaviour covered by TC-V12-A | TC-V12-A-095..099 | Matched |
| A-24-1249 | Check: no_activation / Observed result: True / Test scope: Targeted Chromium test; synthetic local prototype only | Partially covered | US-2004; BRL-SVC-03 | Behaviour covered by TC-V12-A | TC-V12-A-095..099 | Matched |
| A-24-1251 | Check: quota_and_trace / Observed result: True / Test scope: Targeted Chromium test; synthetic local prototype only | Partially covered | US-2004; BRL-SVC-03 | Behaviour covered by TC-V12-A | TC-V12-A-095..099 | Matched |
| A-24-1252 | Check: budget_hold / Observed result: True / Test scope: Targeted Chromium test; synthetic local prototype only | Partially covered | US-2004; BRL-SVC-03 | Behaviour covered by TC-V12-A | TC-V12-A-095..099 | Matched |
| A-24-1253 | Check: reviewer_approval / Observed result: True / Test scope: Targeted Chromium test; synthetic local prototype only | Partially covered | US-2004; BRL-SVC-03 | Behaviour covered by TC-V12-A | TC-V12-A-095..099 | Matched |

#### 11.1.3.25 Chapter 25: Decision Register Migration Source Appe

**Covered (grouped, 15):** DEC-V7-02, DEC-V7-04, DEC-V7-05, DEC-V7-06, DEC-V7-07 → DEC-418; quiet hours; DLT; DEC-001/OKPI-13; DEC-008; DEC-V9-02, DEC-V9-03, DEC-V9-04 → Part 0B coverage; BR-M rules; DEC-004 Apollo reserve; A-25-1283, A-25-1292 → Part 0B; Part 9.1; REC-30 → CONFLICT-462; REC-04@25 → A112; Part 2.4 §2.33.3; REC-06@25 → A110; A106; saved views; REC-10@25 → Consent withdrawal scoped (Part 2.3); REC-12@25 → A109; A111; DEC-051; PDP; DEC-061. All Matched.

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| DEC-V12-01 | ID: DEC-V12-01 / Decision: Certification sequence / Recommendation: SOC 2 Type I (R2) → Type II + ISO 27001 (R3) → ISO 27701 + 42001 (R4) / Owner: Co… | Conflict | DEC-228 staffing; DEC-422 budget; Part 9.9a CAP-X3-17 | Separately costed enterprise-readiness proposal | DEC-513; CONFLICT-760; RECOMMENDATION-775 | Adopted (DEC-775) |
| DEC-V12-02 | ID: DEC-V12-02 / Decision: Identity providers and SCIM scope for R1/R2 / Recommendation: Okta, Entra ID and Google first; SCIM at R2 / Owner: IAM lea… | Conflict | DEC-228 staffing; DEC-422 budget; Part 9.9a CAP-X3-17 | Separately costed enterprise-readiness proposal | DEC-513; CONFLICT-760; RECOMMENDATION-775 | Adopted (DEC-784) |
| DEC-V12-03 | ID: DEC-V12-03 / Decision: SLA tier targets and service credits / Recommendation: 99.5 / 99.9 / 99.95% monthly (proposed); credits per contract / Own… | Partially covered | Part 8.3c SLA-10; DEC-044 | SLA tiers and credits as templates; Enterprise tier pending | DEC-510; CONFLICT-760 | Adopted (DEC-774) |
| DEC-V12-04 | ID: DEC-V12-04 / Decision: Locale sequence / Recommendation: en + hi (R2), de + fr (R3), ar (R4); professional translation review each / Owner: Produ… | Conflict | DEC-026 locales | en+hi at Release 2 Website chrome; de/fr/ar with market packs | DEC-516; CONFLICT-777 | Matched |
| DEC-V12-05 | ID: DEC-V12-05 / Decision: US sales-tax and global tax provider / Recommendation: Select provider before R5; India/EU rules configured internally / O… | Conflict | DEC-421 (Mumbai only); Part 2.4 §2.35.5 | India region through Release 2; EU/US region and tax provider at an approved R3/R5 gate | DEC-514; CONFLICT-761 | Adopted (DEC-776) |
| DEC-V12-06 | ID: DEC-V12-06 / Decision: Region expansion order and cloud regions / Recommendation: IN → EU → UK/ME/APAC → US / Owner: Platform owner / Status: Open | Conflict | DEC-421 (Mumbai only); Part 2.4 §2.35.5 | India region through Release 2; EU/US region and tax provider at an approved R3/R5 gate | DEC-514; CONFLICT-761 | Adopted (DEC-776) |
| DEC-V12-07 | ID: DEC-V12-07 / Decision: Additional jurisdiction packs / Recommendation: US, UK, CA, AU, SG, AE, BR drafts need counsel review before market entry … | Conflict | DEC-029 Year-1 outbound allowlist | Market opens only after counsel approves its pack; IN first, EU second | DEC-507; CONFLICT-766; RECOMMENDATION-774 | Matched |
| DEC-V11-01 | ID: DEC-V11-01 / Decision: Approval evidence for DEC-V9-01 and DEC-V9-02 / Resolution: Product owner instructed adoption of the stricter recovery obj… | Not covered | None | Recorded in V12 decision import | DEC-518 | Matched |
| DEC-V11-02 | ID: DEC-V11-02 / Decision: V11 is the final controlled baseline / Resolution: All later changes require a new controlled revision with fresh evidence… | Not covered | None | Recorded in V12 decision import | DEC-518 | Matched |
| DEC-V9-01 | ID: DEC-V9-01 / Decision: Recovery objectives / Resolution: Adopt the stricter retained targets (table above); supersedes RPO 1 h proposal / Owner: P… | Conflict | DEC-018 RPO 15 min/RTO 4 h; CONFLICT-462 | Record customer approval DEC-V11-01; cost confirmation to Founder | DEC-515; CONFLICT-765 | Adopted (DEC-790) |
| DEC-V7-01 | ID: DEC-V7-01 / Decision: Second launch jurisdiction after India / Recommendation / options: Recommend EU (GDPR/ePrivacy/AI Act) — strictest baseline… | Conflict | DEC-029 Year-1 outbound allowlist | Market opens only after counsel approves its pack; IN first, EU second | DEC-507; CONFLICT-766; RECOMMENDATION-774 | Matched |
| DEC-V7-03 | ID: DEC-V7-03 / Decision: Cloud provider and regions / Recommendation / options: One provider with an India region and an EU region; managed PostgreS… | Conflict | DEC-421 (Mumbai only); Part 2.4 §2.35.5 | India region through Release 2; EU/US region and tax provider at an approved R3/R5 gate | DEC-514; CONFLICT-761 | Adopted (DEC-772) |
| DEC-V7-08 | ID: DEC-V7-08 / Decision: Data residency choice at onboarding / Recommendation / options: Region chosen at onboarding (IN or EU) and fixed; migration… | Conflict | DEC-421 (Mumbai only); Part 2.4 §2.35.5 | India region through Release 2; EU/US region and tax provider at an approved R3/R5 gate | DEC-514; CONFLICT-761 | Adopted (DEC-772) |
| REC-01/05 | Decision: REC-01/05 / Resolution proposed: Retire public directory and publication APIs; neutral catalogue only; client own-property private intake /… | Conflict | FR-W02 directory; FR-W03 startup site; API-497; US-1905 | Neutral storefront; platform directory retired; startup sites only on tenant-verified pro… | DEC-505; CONFLICT-764; FR-V12-A-050..052 | Matched |
| REC-02/03 | Decision: REC-02/03 / Resolution proposed: 39 SKUs, 156 workflows, 25 included foundations; legacy alias crosswalk / Owner / gate: Product / billing | Partially covered | Old REC series (V2) reused IDs | Disambiguated as REC-V2-nn | GAP-768; DEC-518 | Matched |
| REC-07/08 | Decision: REC-07/08 / Resolution proposed: Workflow-specific steps, KPIs and risk classes; review actual effect / Owner / gate: Engineering / policy | Partially covered | Old REC series (V2) reused IDs | Disambiguated as REC-V2-nn | GAP-768; DEC-518 | Matched |
| REC-09/11 | Decision: REC-09/11 / Resolution proposed: Historical counts are candidate; resolve scope/DTO/DDL before deployment / Owner / gate: Engineering | Partially covered | Old REC series (V2) reused IDs | Disambiguated as REC-V2-nn | GAP-768; DEC-518 | Matched |
| A-25-1293 | Responsible role: Product owner / finance / Decision or evidence required: Approve 39 service release states, pricing, meter allowances, SLA, contrac… | Partially covered | Part 8.2 RACI | Decision ownership register | FR-V12-A-210 | Matched |
| A-25-1294 | Responsible role: Backend / database leads / Decision or evidence required: Review proposed OpenAPI/DTO and physical schema, migration, scoped RLS, a… | Partially covered | Part 8.2 RACI | Decision ownership register | FR-V12-A-210 | Matched |
| A-25-1295 | Responsible role: Security / privacy / legal / Decision or evidence required: Approve role matrix, policies, source rights, channel/jurisdiction cont… | Partially covered | Part 8.2 RACI | Decision ownership register | FR-V12-A-210 | Matched |
| A-25-1296 | Responsible role: Integrations / FinOps / Decision or evidence required: Verify provider permissions, limits, actual pricing, failover, measured cost… | Partially covered | Part 8.2 RACI | Decision ownership register | FR-V12-A-210 | Matched |
| A-25-1297 | Responsible role: AI / QA / Decision or evidence required: Approve model and prompt evaluation, deterministic constraints, fixture and live test cove… | Partially covered | Part 8.2 RACI | Decision ownership register | FR-V12-A-210 | Matched |
| A-25-1298 | Responsible role: Delivery owner / Decision or evidence required: Assign each inherited decision ID to responsible named owner, due date and affected… | Partially covered | Part 8.2 RACI | Decision ownership register | FR-V12-A-210 | Matched |

#### 11.1.3.AP Chapter AP: Appendix: ID index

| Aspect | Summary (V12 wording, abridged) | Before | Blueprint location | Action | New IDs | After |
|---|---|---|---|---|---|---|
| A-AP-1299 | ID family: Service SKU / Format / range: SM-SVC-01…39 / Where: ch08 | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |
| A-AP-1300 | ID family: Workflow / Format / range: SM-SVC-nn-WF01…04 (156) / Where: ch09 | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |
| A-AP-1301 | ID family: Foundation / Format / range: SM-01-01…SM-14-05 (25) / Where: ch08 | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |
| A-AP-1302 | ID family: Business requirement / Format / range: BR-V3-01…14, BR-C01…15, BR-V7-AI-01…08, BR-V7-CJ-01…12, BR-V7-WEB-01…04, BR-V7-ADM-01…03 / Where: c… | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |
| A-AP-1303 | ID family: Optimization / architecture / Format / range: 135 OPT (AI-, GC-, SEC-, ST-, FL-, AT-, RT-, CV-, CS-) / MT-01…40 / Where: chapters 01–25 | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |
| A-AP-1304 | ID family: Jurisdiction rule / Format / range: CJ-IN-01…11, CJ-EU-01…10, CJ-UK-01, CJ-US-01 / Where: ch20 | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |
| A-AP-1305 | ID family: Engineering requirement / Format / range: AIX-01…20, CJ-R01…20 / Where: FSD ch16, ch18 | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |
| A-AP-1306 | ID family: Website route / Admin screen / Format / range: W01…W36 / A001…A121, X26…X39, O01…O08 / Where: ch12, ch19 | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |
| A-AP-1307 | ID family: Decision / Format / range: DEC-V7-01…08 (+180 inherited) / Where: ch25 | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |
| A-AP-1308 | ID family: Prototype check / Format / range: V8-QA-001…071 / Where: ch24 | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |
| A-AP-1309 | ID family: Mobile requirement / Format / range: MOB-01…18 / Where: ch24 | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |
| A-AP-1310 | ID family: Change / Format / range: D1…D13, CJ, AI / Where: ch01 | Not covered | None (V12 ID families absent) | ID family alias map §11.1.4 | DEC-500 | Matched |


---

## 11.1.4 Catalogue reconciliation

### 11.1.4.1 V12 inventory against the blueprint (business view)

| V12 inventory item (BRD 00, 01 §V12) | V12 count | Blueprint today | Reconciliation | Owner of detail |
|---|---|---|---|---|
| Sellable service SKUs | 39 (SM-SVC-01…39) | No SKU concept; 66 modules M01–M66, plan archetypes (DEC-047) | Adopted: 39 SKUs are the commercial unit (DEC-501, CONFLICT-767); SKU → module crosswalk §11.1.4.3 | Group B (service specs) |
| Included workflows | 156 (four per SKU, never sold separately) | WF-01…14 (Part 2.2) + WF-15…38 (Part 9.4) | Adopted as included contracts under the parent SKU (DEC-501); registry FR-V12-A-002 | Groups C/D |
| Steps | 517 (159 AI-inference steps) | Flow steps inside WF-01…38 | Recorded; step contracts by Groups C/D; AI steps by Group F | Groups C/D/F |
| Included foundations | 25 (SM-01-01…SM-14-05) | Platform modules M01–M09, M53–M58 | Included, never charged (DEC-501) | Group B |
| Logical engines | 15 (V12 adds subscription/bundle/entitlement, billing/metering/reconciliation, SaaS catalogue/service registry, platform operator administration, authorized portfolio command centre) | Module catalogue Part 2.1; SaaS module `saas` | Engines map to modules; new business rules here (FR-V12-A-010…035, 120…125) | Group E |
| Agent roles | 20 | AG-001…080 (Part 9.4) | Recorded; mapping by Group F | Group F |
| Website routes / Admin screens | 41 / 153 (W01–W41, A001–A131, X26–X39, O01–O08) | 34 W + 113 A + 71 added screens (W35–W44, A114–A149 etc.) | **ID collision** (same numbers, different meaning) → namespacing recommended (RECOMMENDATION-773); purpose of W01–W34 changes to a neutral storefront (CONFLICT-764) | Group G |
| Controlled requirements | 233 = 135 OPT + 40 MT + 18 MOB + 20 AIX + 20 CJ-R; plus 65 ENT and 10 BR-V12 | BR-M01…M66, BR-S001…S140, FR registers | This part maps every OPT, MT, MOB, BR-V3, BR-C, BR-V7, BR-V12 and BR-OBJ that appears in the assigned chapters (§11.1.4.4) | Groups A (business) + E/F/I (engineering detail) |
| Release KPIs / blocking | 35 / 21 | OKPI-01…35 (Part 8.3c §8.3.5.15.4) | V12 `KPI-nn` ≡ blueprint `OKPI-nn` (DEC-511); collision with Part 1 KPI-01…31 kept resolved by the existing OKPI rule | Group A |
| Data-ethics rules | 13 (CJ-GL-01…13) | BR-M18, M19, M56, M02, M16, M66, M04, M27, M28, M41, M25, M32, M10, M37, M48, M50, M31, M33, M35, M57, M51, M42, M43, M46, M36, M59, M60 | Covered (§11.1.4.6); non-relaxable by tenants (DEC-507) | Group A |
| Jurisdiction rules | 23 (IN 11, EU 10, UK 1, US 1) + 10 draft (US, UK, CA, AU, SG, AE, BR) | DEC-029 rule pack (IN, EU/EEA/UK, US, UAE, SG, AU) | Adopted with V12 market-opening rule (DEC-507, CONFLICT-766) | Groups A + I |
| API operations | 282 + 48 ENT | 579 operations | Group H | Group H |
| Database tables | 118 + 19 ENT | Part 3.3 / 3.6 entities | Group I | Group I |
| Locales | en, hi, de, fr, ar (RTL) | en-IN; hi/ta/or content W5 (DEC-026) | Adopted sequence (DEC-516, CONFLICT-777) | Groups A + G |

### 11.1.4.2 V12 ID families and their blueprint aliases

| V12 family (Appendix ID index and chapters) | Range in V12 | Blueprint treatment | Alias rule |
|---|---|---|---|
| Service SKU | SM-SVC-01…39 | New canonical ID | Kept literally; crosswalk to modules §11.1.4.3 |
| Workflow | SM-SVC-nn-WF01…04 (156) | New canonical ID | Kept literally; WF-01…38 remain blueprint flow IDs (Groups C/D map them) |
| Foundation | SM-01-01…SM-14-05 (25) | New | Kept literally (Group B) |
| Business requirement | BR-V3-01…14, BR-C01…15, BR-V7-AI-01…08, BR-V7-CJ-01…12, BR-V7-WEB-01…04, BR-V7-ADM-01…03, BR-V12-01…10, BR-OBJ-01…05 | New canonical BR IDs beside BR-M/BR-S | Kept literally; each mapped in A_coverage.csv and traced in §11.1.5.15 |
| Optimization | 135 OPT: AI-, GC-, SEC-, ST-, FL-, AT-, RT-, CV-, CS- (each 01…15) | Not present (the blueprint's OPT-01-01…OPT-20-04 come from source-pack document 36 and are a different family) | Kept literally with prefix in prose "V12 OPT AI-01"; acceptance IDs OPT-TC-{ID} aliased to TC-V12-A (§11.1.5.15) |
| Architecture | MT-01…40 | Not present | Kept literally; acceptance MT-TC-MT-nn aliased to TC-V12-A |
| Mobile | MOB-01…18 | Not present | Kept literally; acceptance MOB-nn-AT01 aliased |
| Jurisdiction rule | CJ-IN-01…11, CJ-EU-01…10, CJ-UK-01…03, CJ-US-01…04, CJ-CA-01, CJ-AU-01, CJ-SG-01, CJ-AE-01, CJ-BR-01, CJ-GL-01…13 | DEC-029 rule pack entries | Kept literally as rule-pack rule codes |
| Engineering requirement | AIX-01…20, CJ-R01…20 | FSD-level (Groups F and I) | Referenced only |
| Release KPI | KPI-01…35 | **OKPI-01…35** | Alias (collision with Part 1 KPI-01…31) |
| Enterprise requirement | ENT-IDN, ENT-ACC, ENT-API, ENT-DAT, ENT-INT, ENT-SEC, ENT-CMP, ENT-GLB, ENT-OPS, ENT-BIZ | Not present | Kept literally; BR-V12 → ENT trace in §11.1.5.13 |
| Reconciliation action | REC-01…30 (V10) and an older REC-01…12 series (chapter 25) | Not present | V10 series kept literally; the chapter 25 series is cited as **REC-V2-nn** (GAP-768) |
| Decision | DEC-V7-01…08, DEC-V9-01…04, DEC-V11-01…02, DEC-V12-01…07 (+180 inherited) | Blueprint DEC-001…422 | Kept literally as customer decision IDs; imported by DEC-518 (§11.1.4.8) |
| Prototype check | V8-QA-001…071 | Not present | Aliased to blueprint tests (§11.1.4.7) |
| Go-live, scenario, event | GO-01…08, XS-01…10, E-001…007 | GO-/XS- not present; E-001…007 present (Part 2.6) | Kept literally |
| Persona journey | P-01…06 | Personas P01…P16 (no hyphen) | Kept; P-0n journey ≠ P0n persona (mapping in A_coverage.csv chapter 04) |
| Change | C1…C8, D1…D15, CJ, AI, M1, A11Y, EVD | Not present | Recorded as history (Not applicable where prototype-only) |
| Website route / Admin screen | W01…W41 / A001…A131, X26…X39, O01…O08 | W01…W34 / A001…A113 plus 71 added | Collision; RECOMMENDATION-773 (Group G decides) |
| Roadmap phase | R0…R5 | Waves W0…W6, releases A1…A3 | Mapped by DEC-512 (ASSUMPTION-770) |

### 11.1.4.3 SKU crosswalk: SM-SVC-01…39 → blueprint modules, epics and release groups

V12 release groups (BRD 23 §V5): **Foundation**; **R1 intelligence** SVC 01–05, 25; **R2 engagement** SVC 06–13, 15–16; **R3 conversion** SVC 17–24, 29, 32–33; **R4 advanced** SVC 14, 26–28, 30–31, 34–39. "Blueprint wave" is where the underlying capability is already planned; "New" means the blueprint has no equivalent capability and Group B specifies it.

| SKU | V12 name (BRD 13–17) | V12 outcome (abridged) | Blueprint modules / features | Epic | Blueprint wave | V12 group | Coverage of capability |
|---|---|---|---|---|---|---|---|
| SM-SVC-01 | Market & Competitive Intelligence | Evidence-linked market signals, competitor updates, trend reports | M10, M11, M12, M59 | EP-05 | W1 | R1 | Covered |
| SM-SVC-02 | Global Business Opportunity Discovery | Evidence-linked opportunity records and alerts | M13, M14, M15, M16 | EP-05 | W1 | R1 | Covered |
| SM-SVC-03 | B2B Contact & Decision-Maker Intelligence | Verified contact candidates, role mapping, channel eligibility | M18, M19, M24 | EP-06 | W1 | R1 | Covered |
| SM-SVC-04 | Lead Qualification & Intelligent Matching | Qualified or held opportunities, fit explanation, assignment | M16, M17, M20 | EP-06 | W1 | R1 | Covered |
| SM-SVC-05 | CRM & Sales Pipeline | Shared CRM records, pipeline state, next-action queue | M21, M23 | EP-07 | W2 | R1 | Covered |
| SM-SVC-06 | Email Marketing & Outreach | Drafts, dispatch status, delivery evidence | M25, M26 | EP-08 | W2 | R2 | Covered |
| SM-SVC-07 | WhatsApp Business Marketing | Template decisions, message records, conversation updates | M31 | EP-10 | W3 | R2 | Covered |
| SM-SVC-08 | Omnichannel Follow-up & Lead Nurturing | Scheduled steps, drafts, paused sequences, handover | M28, M41 | EP-08 | W2–W3 | R2 | Covered |
| SM-SVC-09 | AI Chat, Unified Inbox & Objection | Intent, grounded response, shared timeline, escalation | M27, M32, M45 | EP-08, EP-10, EP-13 | W2–W4 | R2 | Covered |
| SM-SVC-10 | Meeting, Demo & Appointment | Appointments, briefings, reminders, tasks | M29, M40 | EP-09 | W2–W3 | R2 | Covered |
| SM-SVC-11 | Content Marketing | Calendar, drafts, verified claims, approval queue | M34, M02 | EP-11 | W3 | R2 | Covered |
| SM-SVC-12 | Social Media Publishing & Listening | Scheduled publications, provider status, permitted signals | M33, M35 | EP-05, EP-11 | W3 | R2 | Covered |
| SM-SVC-13 | SEO & Search Visibility | Issue backlog, keyword plan, optimization drafts | M36 | EP-11 | W3 | R2 | Covered |
| SM-SVC-14 | Paid Digital Advertising | Campaign configuration, spend alerts, conversion report | M39, M38 | EP-12 | W3 | R4 | Covered (V12 places it in R4) |
| SM-SVC-15 | Landing Page & Website Lead Intake | Page draft, versioned form, captured leads, routing health | M22, M37; **tenant-property publication** (DEC-505) | EP-07, EP-12 | W2–W3 | R2 | Covered; publication moves to client property |
| SM-SVC-16 | Webinar, Event & Referral Acquisition | Registrations, reminders, attendance follow-up, referrals | M40, M42 | EP-09, EP-12 | W3 | R2 | Covered |
| SM-SVC-17 | Proposal & Quotation | Proposal and calculated quote with revision, approval, validity | M43, M44 | EP-13 | W4 | R3 | Covered |
| SM-SVC-18 | Negotiation, Contract & MoU | Notes, contract draft, approved agreement, signature status | M45, M46 | EP-13 | W4 | R3 | Covered |
| SM-SVC-19 | Tender & Project Bid | Bid/no-bid, draft response, submission and deadline tasks | WF-08, A104 (submission human-only, DEC-053) | EP-14 | W4 | R3 | Covered |
| SM-SVC-20 | Sales Order & Fulfillment | Order drafts, validated totals, milestones, acceptance | WF-10, A105 | EP-14 | W4 | R3 | Covered |
| SM-SVC-21 | Payment, Invoice & Reconciliation | Matched balances, discrepancy queue, verified closure | M47, M52 | EP-15 | W4–W5 | R3 | Covered |
| SM-SVC-22 | Customer, Partner & Institutional Onboarding | Plan, milestones, pilot readiness, handover | M48, M49 | EP-16 | W4 | R3 | Covered |
| SM-SVC-23 | Customer Retention, Renewal & Feedback | Renewal tasks, feedback insights, re-engagement | M50, M51 | EP-16 | W5 | R3 | Covered |
| SM-SVC-24 | Revenue, Attribution & Sales Forecast | Dashboards, attribution, forecast scenarios | M52, M60, M30 | EP-15, EP-17 | W5 | R3 | Covered |
| SM-SVC-25 | Business Document & Knowledge Intelligence | Versioned knowledge, metadata, drafts, expiry reminders | M02, M03 | EP-02 | W0 | R1 | Covered |
| SM-SVC-26 | AI Voice & Intelligent Telephony | Call disposition, call event or hold, booking, summary | None (calls are human tasks, Part 9.8) | — | — | R4 | **New** (Group B); TRAI 140/160 series rule CJ-IN-07 (FR-V12-A-133) |
| SM-SVC-27 | Multimodal Creative & Localization | Image and video drafts, localized asset, creative QA | M34 (text only) | EP-11 | — | R4 | **New** (Group B) |
| SM-SVC-28 | Agentic Commerce & AI-to-AI Transaction | Machine-readable catalog, authorized quote exchange, mandate-linked decision | None | — | — | R4 | **New** (Group B); mandates limited by CONFLICT-762 |
| SM-SVC-29 | ABM & Enterprise Buying Group | Account plan, buying group map, progression | Part 9.8 ABM (WF-25) | EP-12 | A1–A2 | R3 | Covered (advanced) |
| SM-SVC-30 | Conversion Rate Optimization & Experimentation | Funnel report, experiment record, personalization decision | M37 experiments; Part 9.8 experiments | EP-12 | W3, A1 | R4 | Partially (Group B) |
| SM-SVC-31 | Marketplace & E-commerce Channel Operations | Listing state, availability, order event ledger, reconciliation | None (OrganicSpec orders are direct, DEC-045) | — | — | R4 | **New** (Group B) |
| SM-SVC-32 | Partner, Distributor & Co-Selling | Shortlist, enablement, deal registration, partner performance | M42, M49; Part 9.8 partner portal | EP-16 | W4, A1 | R3 | Covered |
| SM-SVC-33 | Customer Service & Support Operations | Support case, resolution or handover, SLA exception | Platform support (Part 4.45) is operator-side only | — | — | R3 | **New** as subscriber service (Group B) |
| SM-SVC-34 | Product-Led Growth & Usage Intelligence | Usage scorecard, activation journey, expansion and upgrade recommendations | Part 8.3c service report; Part 9.8 expansion | EP-16 | A1 | R4 | Partially (Group B) |
| SM-SVC-35 | Brand Reputation & Review Intelligence | Review queue, response draft, incident alert, improvement plan | M33 (listening) | EP-05 | — | R4 | Partially (Group B) |
| SM-SVC-36 | AI Sales Enablement & Coaching | Playbook, practice report, coaching feedback, training plan | Part 9.8 enablement hub | EP-16 | A1–A2 | R4 | Partially; coaching never used for employment decisions (BRD 15) |
| SM-SVC-37 | Pricing, Offer & Revenue Optimization | Profitability, scenarios, pricing experiment, exceptions | M44 price books (AI never sets prices) | EP-13 | — | R4 | Partially; outputs are recommendations only (safety invariant) |
| SM-SVC-38 | SMS, RCS & Business Messaging | Eligibility decision, delivery event, control report | DLT SMS rules (Part 4.1) | EP-08 | — | R4 | **New** channel (Group B) |
| SM-SVC-39 | Procurement & Supplier Management | Supplier shortlist, quotation comparison, PO, supplier performance | OrganicSpec payables (BRD §11), W16 supplier registration, A105 | EP-14 | W4 | R4 | Partially (Group B) |

Summary: 25 SKUs map to capabilities already planned in W0–W5, 6 to advanced releases or partial capabilities, and 8 are new capabilities whose specification and costing belong to Group B (Part 11.2). Business rules that apply to all 39 (entitlement, meter, first value, acceptance) are in Part 11.1b.

### 11.1.4.4 V12 optimization requirements (135 OPT) in the assigned chapters

| Family (V12 dimension) | IDs in assigned chapters | Covered | Partial | Not covered | Conflict | Main blueprint locations | Enhancements |
|---|---|---|---|---|---|---|---|
| AI- AI cost optimization | AI-01…15 (ch 11) | 12 | 3 | 0 | 0 | Part 7.3 routing, cache, evaluation, caps; DEC-418 tier order | FR-V12-A-113 (context budget, summarisation, multimodal tiers); detail Group F |
| GC- general cost | GC-01…15 (ch 06, 11) | 12 | 3 | 0 | 0 | Part 3.1, Part 4.2, Part 8.4, DEC-421 | FR-V12-A-023, 165 |
| SEC- application security | SEC-01…15 (ch 07, 20) | 14 | 1 | 0 | 0 | Part 4.1, Part 4.4a | FR-V12-A-096 |
| ST- stability | ST-01…15 (ch 21) | 15 | 0 | 0 | 0 | Part 4.2, 4.3, 4.4a | — |
| FL- AI flow automation | FL-01…15 (ch 07, 18) | 9 | 5 | 0 | 1 (FL-09) | DEC-051, outbox, A109–A113 | FR-V12-A-002, 094, 112 |
| AT- customer attraction | AT-01…15 (ch 05, 12) | 4 | 10 | 0 | 1 (AT-13) | W07, W08, W20, cookie consent | FR-V12-A-050…061, 073 |
| RT- retention | RT-01…15 (ch 10, 17) | 2 | 12 | 1 (RT-11) | 0 | CSO-08/09, Part 9.8 QBR | FR-V12-A-015, 016, 160…170 |
| CV- conversion | CV-01…15 (ch 07, 10, 11, 12) | 7 | 8 | 0 | 0 | W18, DEC-022/023/024 | FR-V12-A-017, 030, 056…060, 091 |
| CS- satisfaction | CS-01…15 (ch 11, 17, 20, 21, 22) | 8 | 6 | 1 (CS-14) | 0 | A110, A084, Part 2.4 §2.30 | FR-V12-A-034, 142, 153, 166…169 |

All 135 V12 OPT IDs appear in the assigned chapters: the parser found 15 distinct IDs in each of the nine families across chapters 05–22 (totals: 83 Covered, 48 Partially covered, 2 Not covered, 2 Conflict; ST and SEC are almost entirely covered by Parts 4.1–4.4, while the attraction and retention families carry most of the new business work). The 54 P0 / 76 P1 / 5 P2 split (BRD 01 §V5, 23 §V5) is adopted as the gating rule in FR-V12-A-191.

### 11.1.4.5 Release KPIs

V12 KPI-01…35 (BRD 22 §V9) are the same 35 rows, names, targets and gates as source-pack document 38, already registered in the blueprint as **OKPI-01…35** (Part 8.3c §8.3.5.15.4; mandatory flags Part 6.6). Every row is Covered except KPI-32 (growth critical RTO ≤ 120 min), which stays the open item of CONFLICT-462 and is now CONFLICT-765 because the customer has recorded product-owner approval (DEC-V11-01) while the platform-owner cost confirmation is still open. The 7 AI/compliance KPIs and the 12 business KPIs of chapter 22 are registered as KPI-V12-A-01…19 (Part 11.1b §11.1.5.11).

### 11.1.4.6 Data-ethics rules CJ-GL-01…13 → blueprint rules

| V12 rule | Inherited source (BRD 20) | Blueprint enforcement | Status |
|---|---|---|---|
| CJ-GL-01 Published professional channels only; no guessed emails | M18 | BR-M18; X-05; contact verification M19 | Covered |
| CJ-GL-02 Verified contact ≠ consent | M19 | BR-M19; eligibility M24 | Covered |
| CJ-GL-03 Deletion never re-enables outreach; hashed suppression | M56 | BRL-PRV-03 | Covered |
| CJ-GL-04 Planned/unavailable offerings not promoted, matched or quoted | M02, M16, M66 | DEC-060 readiness gate | Covered |
| CJ-GL-05 STOP/opt-out/reply cancels scoped follow-ups across channels | M04, M27, M28, M41 | BRL-SEQ-02; M41 routing | Covered |
| CJ-GL-06 Urgent/clinical enquiries to a human; no medical advice | M25, M27, M32 | X-02; website assistant guardrails | Covered |
| CJ-GL-07 No health targeting, no health events to ad pixels | M10, M37, M48, M50 | X-02; BRL-PRV-06 | Covered |
| CJ-GL-08 No private-group scraping or automated DMs | M31, M33, M35 | X-05 | Covered |
| CJ-GL-09 Complaints above threshold pause the campaign | M57 | KPI-18; M57 compliance monitoring | Covered |
| CJ-GL-10 No automatic re-contact after a lost deal without policy | M51 | M51 lost-deal rules | Covered |
| CJ-GL-11 Referral leads never enrol third parties without basis | M42 | BR-M42; DEC-046 | Covered |
| CJ-GL-12 AI never signs; only approved document versions shared, hash stored | M43, M46 | X-06; DEC-023 | Covered |
| CJ-GL-13 No fabricated rankings or forecasts presented as facts | M36, M59, M60 | KPI-29 labelled estimate; claim approval | Covered |

DEC-V9-03 makes these rules active for all markets and tenants and not relaxable by tenant configuration; DEC-507 adopts that wording (BRL tightening-only rule of DEC-038 already applies).

### 11.1.4.7 Prototype checks V8-QA-001…071 → blueprint behaviour and tests

| V8-QA checks | Behaviour | Blueprint requirement | Blueprint / new test |
|---|---|---|---|
| 001–002, 014–016, 029–031 | Cookie banner on first visit; choice persists; banner above mobile navigation | BR-V7-CJ-09; cookie consent before analytics (Part 4.1) | TC-V12-A-090 (+ existing EP-19 tests) |
| 003, 017, 032, 045, 059 | Every route renders a heading, no horizontal overflow | DEC-043; Part 2.5 responsive rules | TC-V12-A-091 |
| 004, 018, 033, 046, 060 | Unknown route → not-found view | BR-V7-WEB-01; BRL-TEN-10 | TC-V12-A-091 |
| 005–006, 019–020, 034–035 | Inline, announced field errors; invalid email and `javascript:` URL rejected | BR-V7-WEB-02; WCAG 2.2 AA | TC-V12-A-092 |
| 007, 021, 036 | Valid registration proceeds to the wizard | MT-08; FR-V12-A-090 | TC-V12-A-095 |
| 008, 022, 037 | HTML in business name rendered as text | SEC-11; output encoding | TC-V12-A-092 |
| 009, 023, 038 | Data-rights request: inline errors; EU erasure gets reference and one-month due date | BR-V7-CJ-05; FR-V12-A-053 | TC-V12-A-053 |
| 010–011, 024–025, 039–040 | AI transparency page; sample output carries AI disclosure | BR-V7-AI-01; FR-V12-A-054, 114 | TC-V12-A-054 |
| 012, 027, 042 | Skip link focus | WCAG 2.2 AA | TC-V12-A-092 |
| 013, 028, 043, 057, 071 | No runtime errors | Part 6.1 quality gates | TC-V12-A-091 |
| 026, 041 | Mobile menu lists all routes | MOB-02 | TC-V12-A-091 |
| 044, 058 | 143 screens × 4 personas: access counts per persona | RBAC R01–R20 (Part 2.3) | Group G / Group J |
| 047, 061 | Preflight: IN SMS allow/hold; EU undisclosed AI hold; IN WhatsApp without opt-in hold | BR-V7-CJ-02, 04; PDP; DEC-029 | TC-V12-A-131 |
| 048, 062 | Injection screen flags override, exfiltration, invisible characters | BR-V7-AI-06; SEC-08 | Part 6.4 injection suite |
| 049, 063 | Consent withdrawal holds queued run on that channel | REC-10; BR-V7-CJ-03 | Existing consent tests (EP-03) |
| 050, 064 | Requester cannot approve own run; Running → Reconciling → Completed | BR-V7-ADM-01, 02; BRL-APR-01; DEC-050 | Existing EP-18 tests |
| 051, 065 | Run drawer keyboard focus | WCAG 2.2 AA | TC-V12-A-092 |
| 052, 066 | Units 0 and 100001 rejected; over-allowance creates Held run | BRL-SVC-03; FR-V12-A-014 | TC-V12-A-014 |
| 053, 067 | Mixed currency: missing-rate records excluded and counted; negative rate rejected | MT-21; DEC-027 | TC-V12-A-036 |
| 054, 068 | Model promotion blocked without passing evaluation | BR-V7-AI-03; DEC-061 | Part 6.4 |
| 055, 069 | DSAR erasure under legal hold blocked with reason | BRL-PRV-04 | Existing EP-03 tests |
| 056, 070 | Template screen shows seeded searchable records | BR-V7-ADM-03 | Group G |

### 11.1.4.8 Customer decision register (V12 chapter 25) → blueprint

| Customer decision | Customer status | Blueprint position | Resulting blueprint decision |
|---|---|---|---|
| DEC-V12-01 Certification sequence (SOC 2 Type I R2 → Type II + ISO 27001 R3 → ISO 27701 + 42001 R4) | Proposed | Readiness only (CAP-X3-17, A2/A3) | DEC-513 — Pending Founder (CONFLICT-760) |
| DEC-V12-02 Okta, Entra ID, Google first; SCIM at R2 | Proposed | OIDC/SAML reuse of AppNAI identity (DEC-003/019); no SCIM | DEC-513 — Pending Founder (CONFLICT-760) |
| DEC-V12-03 SLA tiers 99.5 / 99.9 / 99.95% with credits | Open | SLA-02 99.5% (Starter/Growth), 99.9% Scale after scale gate; credits placeholder | DEC-510 (Standard/Business adopted as templates; Enterprise 99.95% Pending Founder) |
| DEC-V12-04 Locale sequence en + hi (R2), de + fr (R3), ar (R4) | Proposed | DEC-026 | DEC-516 (CONFLICT-777 adopted) |
| DEC-V12-05 US sales-tax and global tax provider before R5 | Open | GST engine (DEC-027) only | DEC-514 — Pending Founder (with EU/US region) |
| DEC-V12-06 Region order IN → EU → UK/ME/APAC → US | Open | ap-south-1 only (DEC-421) | DEC-514 — Pending Founder (CONFLICT-761) |
| DEC-V12-07 Additional jurisdiction packs need counsel review | Open | DEC-029 allowed some outbound in Year 1 | DEC-507 (CONFLICT-766 adopted) |
| DEC-V11-01 Approval evidence for DEC-V9-01/02 (28 Nov 2026) | Recorded; platform-owner cost confirmation open | — | DEC-518 records it; cost part DEC-515 Pending Founder |
| DEC-V11-02 V11 final controlled baseline | Approved 28 Nov 2026 | — | Superseded by V12 itself; recorded (DEC-518) |
| DEC-V9-01 Stricter recovery objectives | Approved per DEC-V11-01 | DEC-018 RPO 15 min / RTO 4 h; CONFLICT-462 | DEC-515 — Pending Founder (CONFLICT-765) |
| DEC-V9-02 Promoted retained specifications normative | Approved per DEC-V11-01 | Part 0B / 9.6 covered all 38 documents | Recorded (DEC-518) |
| DEC-V9-03 CJ-GL-01…13 active for all tenants | Active; legal wording pending | BR-M rules | DEC-507 |
| DEC-V9-04 Contact-data vendors only licensed, after transfer register and DPA | Open | Apollo reserve optional (DEC-004); open-source first | Recorded (DEC-518): vendor use stays behind DPA and CJ-GL-01 |
| DEC-V7-01 EU second market | Open — recommendation | DEC-029 | DEC-507 |
| DEC-V7-02 AI providers and models per tier | Open | Answered: DEC-418 (Claude Sonnet primary, tier order) | Recorded (DEC-518) |
| DEC-V7-03 One cloud with India and EU regions; managed Kubernetes | Open | DEC-421 (Vercel + Supabase + AWS Mumbai) | DEC-514 — Pending Founder |
| DEC-V7-04 Promotional window 09:00–21:00 recipient time; DSAR timeline | Open | Quiet hours per jurisdiction rule pack; BRL-PRV-02 | Recorded (DEC-518) |
| DEC-V7-05 DLT operator and scrubbing API | Open | DLT rules Part 4.1 | Recorded; selection stays open |
| DEC-V7-06 Evaluation thresholds (accuracy ≥ 90%, claims 100%, citations ≥ 95%, schema 100%) | Open | DEC-001; OKPI-13 schema ≥ 99.5% | Recorded; Group F reconciles the schema 100% vs 99.5% difference |
| DEC-V7-07 Tenant AI budget defaults (soft cap 80%, hard cap per plan) | Open | DEC-008 hard caps; M53 alerts | Recorded (DEC-518); 80% soft alert adopted in FR-V12-A-015 |
| DEC-V7-08 Region chosen at onboarding and fixed | Open — recommendation | India only | DEC-514 — Pending Founder |

### 11.1.4.9 The two REC series

Chapter 25 contains an older table whose rows are labelled "REC-01/05", "REC-02/03", "REC-04", "REC-06", "REC-07/08", "REC-09/11", "REC-10", "REC-12". Their meanings (for example "REC-10 Investment comparator not commercial functionality") differ from the V10 reconciliation actions REC-01…30 of the same document (for example "REC-10 consent withdrawal matches scoped contact"). The blueprint cites the older series as **REC-V2-01…12** to keep both resolvable [GAP-768]. All REC-V2 items are Covered: REC-V2-01/05 by CONFLICT-764 (neutral storefront), REC-V2-02/03 by DEC-501, REC-V2-04 by the 147-screen baseline, REC-V2-06 by DEC-022/023 and server identity, REC-V2-07/08 by Groups C/D, REC-V2-09/11 by Parts 3.5/3.6, REC-V2-10 by DEC-002/DEC-517, REC-V2-12 by Part 6 evidence rules.

*Part 11.1 continues in Part 11.1b: §11.1.5 Enhancements, §11.1.6 Conflicts, §11.1.7 Decisions, §11.1.8 Expert persona review, §11.1.9 Tags register, §11.1.10 Quality gate.*

**Status: Part 11 Batch 11.1a complete (review, coverage and catalogue reconciliation). Quality gate for the whole of Part 11.1 is in Part 11.1b §11.1.10.**
