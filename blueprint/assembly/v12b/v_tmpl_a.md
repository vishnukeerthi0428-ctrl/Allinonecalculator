# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.23a), Independent Completeness Audit (V12 → Blueprint) and Baseline Retention Check — A. Measured V12 Coverage and Restored Content

| Field | Value |
|---|---|
| Document | Part 11.23a: independent, measured completeness audit of the customer revision V12 (BRD V12 + FSD V12 normative chapters) against the whole blueprint, classification of every weak match, and the content restored where coverage was missing |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Parts 0–9.10, Part 0B and Parts 11.0–11.22 as present at the audit run; Founder decisions DEC-770…791 (Part 11.14), V12 adopted on every item |
| Companion files | Part 11.23b (baseline retention check, supersession index), Part 11.23c (cross-part errata, conflicts, decisions DEC-960…970, tags 1180–1189, quality gate) |
| Group and ID ranges | P8, letter V: DEC-960…979 (960…970 used) · tags 1180–1199 (1180…1189 used) · FR-V12-V-### · TC-V12-V-### · US-&lt;EP&gt;-ZV&lt;nn&gt; · errata E-V-## |
| Roles applied | Forensic requirements auditor · Configuration-management and baseline-integrity lead · Principal Business Systems Analyst (with QA Lead and Security/AI-governance reviewers for the restored content) |
| Independence | The panel wrote none of the blueprint. Self-reported coverage CSVs (`final/coverage_v12/A…R_coverage.csv`) were **not** used as evidence; every result below is measured from the text by the scripts in `assembly/v12b/v_*.py` |

**Acronyms used in this part.** BVA boundary-value analysis · CI continuous integration · CRLF / LF carriage-return line feed / line feed (line-ending conventions) · DDL data definition language · DTO data transfer object · ICP ideal customer profile · INV Investment Automation product · PDP Policy Decision Point · RCTCFE the customer's review method (stage gates and rubric score) · RLS row-level security · SHA-256 Secure Hash Algorithm, 256-bit · SoD separation of duties.

**How to read this part.** §11.23.1 explains what was read and how it was measured. §11.23.2 gives the measured match before and after this part. §11.23.3 lists every statement that matched weakly, with its classification. §11.23.4 reconciles by chapter and unit type. §11.23.5 holds the restored content at full depth (FR-V12-V-001…009, tests and stories). Part 11.23b and 11.23c complete the audit.

---

## 11.23.1 Material reviewed and method

### 11.23.1.1 Files, sizes and purpose

| Item | Value |
|---|---|
| Source directory | `scratchpad/v12/BRD/` and `scratchpad/v12/FSD/` (customer revision V12 received 28 Nov 2026) |
| Files read | **{{M:EX.files}}** normative chapter files (BRD 00–25 + appendix; FSD 00–40 + appendices A, A2, B, C, C2, D) |
| Bytes read | **{{M:EX.total_bytes_fmt}}** bytes (≈ 3.7 MB) |
| Excluded | `BRD/ZZ_Historical_annex.txt` (4,015,412 B) and `FSD/ZZ_Historical_annex.txt` (11,356,732 B): "V1 retained text (non-normative)", audited separately by Part 11.12 |
| Statements extracted | **{{M:EX.statements_fmt}}** requirement-like statements ({{M:EX.unique_fmt}} unique after normalisation; duplicates are the same requirement stated in BRD and FSD or repeated per screen/workflow) |
| Unit types | {{M:EX.kinds}} |
| Blueprint compared | every `Part-*.md` in the blueprint directory except this part: {{M:SB.files}} files, {{M:SB.lines_fmt}} lines (Parts 0–9.10, 0B, 11.0–11.22 as present at the run) |

The per-file table with statement counts and the measured match per chapter is in §11.23.4.1.

### 11.23.1.2 Extraction rules (`v_01_extract.py`)

| Rule | Detail |
|---|---|
| Prose | Each line outside tables is split into sentences. A sentence is a statement when it contains a modal or control word (shall, must, should, required, never, only, cannot, blocking, at least, within, limit, cap, threshold, target, …), a requirement ID, or a threshold-bearing number |
| Tables | Every row after the header row is a statement (cells joined with " \| "); the header is kept as context |
| Headings | A heading that carries an ID (for example `MT-06 — Tenant lifecycle management`) is a statement |
| OpenAPI (App. A, A2) | One statement per operation: method, path, operationId, summary, idempotency flag (282 + 48 operations) |
| DTO schemas (App. B) | One statement per workflow schema: `$id` and the required input and output fields (156) |
| DDL (App. C, C2) | One statement per SQL statement (CREATE TABLE, CREATE POLICY, ALTER, INSERT, functions and triggers) |
| IDs | Uppercase families with a hyphen and a digit (e.g. `SM-SVC-06-WF01`, `ENT-DAT-04`, `MT-TC-MT-06`, `V12-QA-002`) plus screen IDs `A###`/`W##`; standard names (ISO-, RFC-, TLS-, UTF-, …) excluded |
| Thresholds | Numbers that carry a unit (%, ms, min, h, d, ₹, …), a comparator (≤, ≥, <, >, =), a currency or a decimal point. Bare integers such as chapter, row or step numbers are not thresholds |

### 11.23.1.3 Matching rules (`v_02_match.py`)

| Measure | Definition |
|---|---|
| Exact ID presence | Each V12 ID is looked up in an index of every ID string in the blueprint. A second figure also accepts IDs implied by range notation (`V7-QA-004…039`) and by the compressed workflow test catalogue of Part 11.10b §11.10.4.2 (one row per workflow lists the scenario suffixes and numbered step tests) |
| 6-gram containment | Share of the statement's 6-word shingles (stemmed, lower case) that occur anywhere in the blueprint |
| Token containment | Content tokens (stop words removed, stemmed) of the statement found in the best blueprint passage. Candidates are the lines that carry the statement's IDs (or the IDs of its section) and the lines sharing its rarest tokens; a passage is the candidate line ±2 lines of the same file. The union of the ID lines is also scored (× 0.9) |
| Threshold presence | Each threshold of the statement is searched in the best passage ±3 lines and in the ID lines; failing that, in any blueprint line that shares ≥ 50% of the statement's content tokens |
| Level | **exact**: 6-gram ≥ 0.8 · **strong**: 6-gram ≥ 0.5, or token ≥ 0.8, or all IDs present and token ≥ 0.6 · **moderate**: token ≥ 0.6, or all IDs present and token ≥ 0.45, or 6-gram ≥ 0.3 · **weak**: token ≥ 0.35 or any ID present · **none**: otherwise |
| Measured match | exact + strong + moderate, as a share of all statements |

[ASSUMPTION-1181] The thresholds are a lexical proxy for coverage. They are deliberately strict on the 6-gram side (literal adoption) and generous on the token side (paraphrase). Every statement below "moderate", every threshold miss and every absent ID was therefore read in context and classified by hand or by a stated rule (§11.23.3); the lexical score alone never closes a statement.

### 11.23.1.4 Triage and classification (`v_03_triage_set.py`, `v_04_classify.py`, `v_manual_src.py`)

1. **Triage set.** {{M:SB.triage_n}} statements: weak or none matches, plus statements whose thresholds were not found, plus statements carrying an ID absent from the blueprint.
2. **Context reading.** Each triaged statement was printed with its chapter, section path and best blueprint location, de-duplicated by text, and read. Rows that follow one template (for example the "source disposition candidate" rows of FSD chapter 40, or the DDL statements of Appendices C/C2) were verified **programmatically per row**: the object each row names (API path, entity, QC, task, test ID, table) was looked up in the blueprint and its location recorded.
3. **Classes.** *Covered in different words* (citation: part, section, line, ID) · *Not covered* (content written in §11.23.5 with FR-V12-V / TC-V12-V / US-…-ZV IDs) · *Superseded by a Founder decision* (DEC cited). An overlay also catches statements that **match** the blueprint lexically but state a rule that a Founder decision has since changed.
4. **Manual decisions.** {{M:n_manual}} distinct statements needed a reader's judgement; each decision is listed in §11.23.3.4 and stored in `v_manual.tsv` keyed by the statement's text hash, so identical BRD and FSD copies share one decision.

### 11.23.1.5 Reproducibility

```text
cd blueprint/assembly/v12b
python3 v_01_extract.py            # statements.json, extract_summary.json
python3 v_02_match.py before       # excludes Part-11-23*; match_before*.json
python3 v_03_triage_set.py         # triage_before.json
python3 v_manual_src.py            # v_manual.tsv (manual decisions by text hash)
python3 v_04_classify.py           # classified.json (0 unclassified required)
python3 v_02_match.py after        # includes Part-11-23*; match_after*.json
python3 v_10_baseline.py && python3 v_11_supersession.py   # Part 11.23b
python3 v_20_errata.py && python3 v_21_screen_clash.py      # Part 11.23c
python3 v_31_combi.py && python3 v_30_fragments.py && python3 v_32_assemble.py
```

Outputs: `final/coverage_v12/V_audit.csv` (one row per statement, {{M:EX.statements_fmt}} rows, with the measures, the classification and the citation), `final/supersession_index.csv`, and the working files in `assembly/v12b/v_out/`.

---

## 11.23.2 Coverage summary (measured before and after)

### 11.23.2.1 Measured lexical match

"Before" is the blueprint without this part; "after" includes Parts 11.23a–c. Both runs used the same snapshot of the other parts.

{{F:summary}}

**Reading.** The blueprint already reproduced V12 closely: {{M:SB.matched_pct}}% of the statements match at moderate level or better before this audit, and {{M:SB.id_presence_pct}}% of V12 ID occurrences are present (literally or through range and compressed notation). The weak residue is concentrated in metadata-heavy registers (FSD 40 source dispositions, prototype lineage, DDL policies) and in a small set of genuinely missing items. After the restored content, the measured match is **{{M:SA.matched_pct}}%**; the remaining lexical gap is closed by classification, not by copying text (§11.23.2.2).

### 11.23.2.2 End state of every statement (after classification)

{{F:final}}

### 11.23.2.3 What was genuinely missing

| # | Missing content | Statements | Restored as |
|---|---|---|---|
| 1 | Artifact lineage and integrity: SHA-256 of the V7/V8/V9/V12 prototypes and documents, the V8 merge lineage, the V8 stage-gate register, version-label defects | {{M:fr.FR-V12-V-001}} | FR-V12-V-001, §11.23.5.1 (also found: the four V12 HTML files as received do **not** match their declared hashes until CRLF line endings are normalised — CONFLICT-1184) |
| 2 | V12 identifiers absent from the blueprint: PT-V7-02, -03, -09, -10, -14; DB-V2-SUBSCRIPTION; DB-V2-CONFIG; SM-V5-PLANNING; family labels BR-V7-AI and BR-V7-CJ; truncated UX-TASK-A11 | {{M:fr.FR-V12-V-002}} | FR-V12-V-002, §11.23.5.2 |
| 3 | Illustrative cost per invocation for workflows whose seed was absent | {{M:fr.FR-V12-V-003}} | FR-V12-V-003, §11.23.5.3 |
| 4 | ICP attribute set of MT-04 | {{M:fr.FR-V12-V-004}} | FR-V12-V-004, §11.23.5.4 |
| 5 | FX rate entry below 1 (D15) | {{M:fr.FR-V12-V-005}} | FR-V12-V-005, §11.23.5.5 |
| 6 | Production rule "one implementation per behaviour" (D12) | {{M:fr.FR-V12-V-006}} | FR-V12-V-006, §11.23.5.6 |
| 7 | The V12 per-screen "V2 rule" for Admin screens (stated on {{M:n_v2}} registered screens) | {{M:fr.FR-V12-V-007}} | FR-V12-V-007, §11.23.5.7 |
| 8 | Two consequences found by the audit (not V12 statements): the mandate engine's treatment of securities-governed INV actions, and errata governance | — | FR-V12-V-008 and FR-V12-V-009, §11.23.5.8–11.23.5.9 |

---

## 11.23.3 Detailed register

### 11.23.3.1 Not covered → restored in this part (every statement)

{{F:n_reg}}

### 11.23.3.2 Superseded by a Founder decision (every statement)

{{F:s_reg}}

The two overlay rows (VND-86, VND-95) matched the blueprint lexically (Part 11.8 plugin register) but carry the pre-DEC-783 position. All other V12 positions that differ from earlier blueprint text were adopted by DEC-770…791, so the earlier **blueprint** text is what is superseded; those cases are handled as baseline amendments (Part 11.23b) and errata (Part 11.23c), not here.

### 11.23.3.3 Covered in different words (grouped by rule; every row cited in `V_audit.csv`)

{{F:c_rules}}

**Notes on the large groups.**

- **FSD 40 source disposition candidates (628 triaged rows).** Each row names an archived source-pack object (API operation, entity, QC, task or test) and a review instruction ("verify DTO and scope", "map to current gate", "retain predecessor/estimate; not approved"). Every one of the named objects is present in the blueprint (checked per row); the instructions are executed by Part 11.12 (residual registers R-API, R-DB, R-QC, R-TASK, R-TEST) and Part 11.11a §11.11.4.5. The weak lexical score comes from the instruction wording, which is not requirement text.
- **Appendix C/C2 DDL (138 triaged statements).** Every table and policy name is present; Part 11.9a reproduced the customer DDL and re-ran DB-T1…T9 and C2-T1…T11 (20/20), and Part 11.9b carries the corrected RLS DDL. The weak score is the repeated policy boilerplate.
- **ID-bearing rows.** Requirement-status rows (for example `AIX-04 | P0 | Prompt registry | … | Production pending`) whose IDs are present; the residual words are status and evidence metadata.

### 11.23.3.4 Manual decisions (each read in context)

{{F:manual}}

---

## 11.23.4 Catalogue reconciliation

### 11.23.4.1 By chapter file

{{F:chapters}}

### 11.23.4.2 By unit type (before)

{{F:kinds}}

### 11.23.4.3 ID families

| Check | Result |
|---|---|
| Distinct V12 IDs | {{M:SB.distinct_ids_fmt}} |
| Literal presence before | {{M:SB.id_literal_pct}}% of ID occurrences |
| With range and compressed notation | {{M:SB.id_presence_pct}}% |
| Compressed notation that explains most literal misses | Part 11.10b §11.10.4.2 lists, per workflow, the scenario suffixes (POS, INPUT, SCOPE, ENT, DUP, QUALITY, BUDGET, RECOVERY, APPROVAL, EFFECT) and the numbered step tests; the 1,867 `SM-SVC-##-WF#-TC-*` and `…-STEP-##-TC` IDs are therefore present by construction. Part 11.10a lists the V7/V8/V9/V11/V12 QA checks as ranges |
| Colliding families | V12 `DEC-###` and `DEC-Vn-##` (written CDEC, DEC-700), V12 `KPI-##` (= OKPI, DEC-681), V12 screen IDs A114–A131/W35–W41 (aliases `V12-…`, DEC-620), V12 `REC-##` (DEC-964), V12 `ENT-…` enterprise requirement IDs versus blueprint `ENT-###` entities (different shape, no clash) |
| IDs still absent after this part | {{M:SA.distinct_ids_missing}} (all 11 IDs restored in §11.23.5.2 are now present) |

---

## 11.23.5 Enhancements: restored content at full depth

The functional requirements below carry V12 wording literally where V12 states the rule, and cite the V12 location. They are binding on the build exactly like the FRs of Parts 11.1–11.22.

### 11.23.5.1 FR-V12-V-001 Artifact lineage and integrity register

| Field | Specification |
|---|---|
| ID | FR-V12-V-001 |
| Title | Customer-artifact lineage and integrity register (configuration items of the requirement baseline) |
| Source | BRD/FSD V12 ch01: "V8 \| Release baseline, merge lineage and source reconciliation", "Source reconciliation (inputs to V8)", "RCTCFE stage-gate register (V8 cycle)", "V8 \| Executive change summary" (D1, M1), "V9 \| Release baseline — promotion of retained specifications", "V11 \| Final controlled baseline" (C8), "V12 \| Enterprise-readiness baseline" (artifact SHA-256), "Four HTML artifact identities" |
| Requirement | The programme keeps a register of every customer-delivered artifact that defines the requirement baseline: documents (BRD, FSD), HTML prototypes (desktop and mobile, website and Admin), archives and source packs. Each entry records artifact name, version, role (base, functional layer, evaluation method, historical archive), owner, declared SHA-256 (as stated in the documents), as-received SHA-256, normalised SHA-256 (LF line endings for text artifacts), verification result, verification date and verifier. On every customer delivery the integrity check runs **before** any review group starts. A mismatch that persists after LF normalisation blocks the baseline (status "Held — integrity") and is raised to the customer; it is never silently accepted |
| Normalisation rule | Text artifacts (HTML, TXT, CSV, JSON, YAML, SQL) are hashed twice: as received, and after converting CRLF to LF. A declared hash is matched if either form matches; the register records which. Binary artifacts (DOCX, ZIP, PDF, images) are hashed as received only |
| Lineage | Each version entry names its inputs and their roles (e.g. V8 = responsive V7 base + functional V7 layer); merges are recorded once, with the stage-gate evidence |
| Owner | Configuration-management lead (programme); Product Owner approves baseline promotion |
| Where | `final/artifact_register.csv` (to be generated by the CI job of FR-V12-V-009) and this section as the initial content |
| Acceptance | TC-V12-V-001…007; US-21-ZV01 |
| Wave / release | W0 (applies from the V12 baseline onward); Release 1 |

**A. V12 artifacts: declared versus received (verified 28 Nov 2026 by this audit).**

| Artifact | Declared SHA-256 (BRD/FSD V12 ch01) | As-received SHA-256 | LF-normalised SHA-256 | Result |
|---|---|---|---|---|
{{F:art_rows}}

The four HTML prototypes contain CRLF line endings (381 lines in each website build, 635 in each Admin build) that were added in transit; after normalisation all four match the declared hashes, so the content is the declared V12 content. The two Word documents carry no declared hash (a document cannot carry its own hash); their as-received hashes are now the reference. The historical archive matches byte for byte. [CONFLICT-1184] records the as-received mismatch and its resolution (DEC-968).

**B. V9 prototype identities (BRD/FSD V12 ch01 "V9 \| Release baseline", "Four HTML artifact identities").**

| Artifact | SHA-256 |
|---|---|
| commercial_website_desktop_V9.html | 2e3cba0d309fb73fb37a03ff13c9e7524eeaca5e068d8766a92600a66df5e5b9 |
| commercial_website_mobile_V9.html | 60d9e7a2ea6e7794821ffe0c081f97533885e6edff92fdd39f5386b959c7a6bc |
| commercial_admin_desktop_V9.html | aa7fe03ca5ee38e3fc209e6628bc5961bf7f746aa62749e6faf1198458f4142f |
| commercial_admin_mobile_V9.html | 5cf8bccfe336ac9ec928e51d030fb0c45e50894c9d41192cc59b73497db628f3 |

**C. Source reconciliation (inputs to V8), literal.**

| Input | Owner | Use in V8 | SHA-256 (prefix) |
|---|---|---|---|
| Sales_Marketing_Automation_BRD_V7.docx (responsive) | User | Base document for BRD V8 | 49b96a10f6ecc51b… |
| Sales_Marketing_Automation_FSD_V7.docx (responsive) | User | Base document for FSD V8 | 61f5753fbe0de5a4… |
| commercial_website_desktop_V7.html | User | Base for website desktop V8 | 1f2743a4587c2bd7… |
| commercial_website_mobile_V7.html | User | Base for website mobile V8 | 7001283bb524d203… |
| commercial_admin_desktop_V7.html | User | Base for Admin desktop V8 | a5cd10f964b75b7c… |
| commercial_admin_mobile_V7.html | User | Base for Admin mobile V8 | 85179014b82161a1… |
| Sales_Marketing_Automation_BRD_V7.docx (functional) | Claude | Source of BR-V7 requirements, compliance and AI business chapters | 5d1139143327800b… |
| Sales_Marketing_Automation_FSD_V7.docx (functional) | Claude | Source of AIX/CJ-R, appendices A–D, registers, tests | 6e7e68ccfed4a206… |
| commercial_website_V7.html (functional) | Claude | Source of website functional layer | 0fd2e7f1a9cbeb10… |
| commercial_admin_V7.html (functional) | Claude | Source of Admin functional layer | 2a5e141ead128326… |
| Investment_Automation_RCTCFE_Master_Prompt.docx | User | Evaluation method, applied to the Commercial product (no Investment scope copied — **superseded by DEC-783**: the Investment Automation product is now in scope) | ea4f2a8966bf742d… |

**D. V8 merge lineage and version-label defects, literal.** M1 Two V7 lines: the responsive V7 set (6 files, 18 MOB requirements) and the functional V7 set (4 files, AI + compliance) diverged from V6 → merged into one V8 baseline: the responsive build is the base; the functional layer is applied to all four HTML builds; both documents carry every requirement once. D1 Version labels: HTML titles and banners showed V5/V6 → all four artifacts labelled V8.0; SHA-256 of delivered HTML recorded in BRD and FSD. C8 Stale label: website browser-tab title still showed "V9" → corrected to V11 on both website builds. The V12 website title reads "Commercial Website \| V12.0" (verified in the received file).

**E. RCTCFE stage-gate register (V8 cycle), literal.**

| Stage | Input | Result | Gate |
|---|---|---|---|
| 1 Gap analysis | Six user V7 files + four Claude V7 files | Delta found: two divergent V7 lines; mobile docs lacked AI/compliance; functional docs lacked MOB | Pass |
| 2 BRD/FSD upgrade | Responsive BRD/FSD V7 | AI, compliance, appendices, registers integrated once; MOB scope aligned to 36/143 | Pass |
| 3 Website/Admin upgrade | Four responsive HTML V7 | Functional layer on all four builds; W35/W36, A114–A121 | Pass |
| 4 Cross-artifact alignment | Six V8 artifacts | IDs, counts and SHA-256 synchronised; services ≠ flows confirmed | Pass |
| 5 RCTCFE evaluation | V8 builds | 71 browser checks, axe audit, DB and contract validation; scoring in ch34 | Pass |
| 6 Functional upgrade | Admin/website | Separation of duties, reconciliation states, seeded workspaces retained | Pass |
| 7 Optimization register | 135 OPT | Status recorded for all 135 (ch34); none double-counted | Pass |
| 8 Defect resolution | D1–D15 | D14 skip link and D15 FX decimals fixed in V8; D12 partial by design | Pass with recorded exception |
| 9 Optimization implementation | A089 laboratory + V8 layer | Prototype demonstrations retained; production pending | Prototype only |
| 10 Architecture/redundancy audit | 40 MT + 18 MOB + 40 V7 | One requirement per behaviour; duplicates linked not re-numbered | Pass |
| 11 Universal implementation | Six artifacts | Synchronised V8 delivered; production gate open | Pass (prototype/document) |

The blueprint uses this register as historical evidence only: stage gates of the build are the release gates of Part 8.1/11.20, and the prototype "Pass" values are not production acceptance (Part 11.10a §11.10.3.10).

### 11.23.5.2 FR-V12-V-002 Restored V12 identifiers and their mapping

| Field | Specification |
|---|---|
| ID | FR-V12-V-002 |
| Requirement | Every V12 identifier that the measured audit found absent from the blueprint is registered here with its V12 meaning and its blueprint mapping, so that the traceability chain V12 ID → blueprint requirement → test is complete. The RTM generator (Part 6.6 / 11.11) reads this table |
| Acceptance | TC-V12-V-008…011; US-21-ZV02 |

| V12 ID | V12 location and meaning (literal) | Blueprint mapping | Test evidence |
|---|---|---|---|
| PT-V7-02 | BRD 12 / BRD 24: acceptance evidence of BR-V7-WEB-01 "Not-found handling — Unknown website or admin addresses show a clear not-found page" (website) | FR-V12-G route rules (Part 11.7b "Rules common to all 34 routes"); not-found view | TC-V12-J-102 (unknown route shows not-found view, V12-QA-004), TC-V12-V-008 |
| PT-V7-10 | Same requirement, Admin addresses | Admin router 404 view inside the authenticated shell; no data leaked | TC-V12-J-101, TC-V12-V-008 |
| PT-V7-03 | Acceptance evidence of BR-V7-WEB-02 "Accessible form errors — Form errors appear next to the field, are announced to screen readers and move focus to the first error" (W12–W20, W32, W33, W35) | Part 11.7b accessibility contract §11.7.5.10; Part 2.5 WCAG 2.2 AA | TC-V12-J-103, TC-V12-J-113, TC-V12-V-009 |
| PT-V7-09 | Acceptance evidence of BR-V7-ADM-03 "Useful workspaces — Every operational workspace shows searchable, filterable fictional records with review actions" (all A screens) | Production reading: every operational workspace lists real records of the granted scope with search, status filters and the review actions of its contract card (Part 2.7b); fictional records only in the sandbox | TC-V12-J-101, TC-V12-V-010 |
| PT-V7-14 | Acceptance evidence of BR-V7-ADM-01 "Separation of duties — The person who requests a run or record cannot approve it" (with DB-T5) and BR-V7-ADM-02 "Reconciled completion — A run is complete only after the provider receipt is matched" (with DB-T6) | BRL-APR (no self-approval); run states Running → Reconciling → Succeeded (DEC-561); Part 11.9a DB-T5/T6 | TC-V12-J-107, TC-16-050, TC-01-063, TC-15-048, TC-V12-V-011 |
| DB-V2-SUBSCRIPTION | FSD 26 "V5 optimization requirements and controls": "scope; quote_version; state; start/end; plan_version; entitlement refs; version" | `saas_subscription` (Part 3.3, Part 11.5a) + `saas_sku_grant` (DEC-584); quote version bound at acceptance (CV-12) | Part 11.5b TC-V12-E tests for subscription lifecycle |
| DB-V2-CONFIG | FSD 26: "scope; schema_version; revision; typed settings; approver_ref; active flag; unique active version per company" | `configuration_revision` (Part 11.9a/b): partial unique index on (tenant_id, company_id) where active; approver ≠ author | Part 11.9b DDL tests |
| SM-V5-PLANNING | FSD 01: "Historical V5 compatibility rule (superseded by MT-08) … SM-V5-PLANNING remains a non-identity worksheet" | Never an identity or hand-off contract; the hand-off contract is SM-APPLICATION-6 (Part 11.5a, MT-08). Imports that present SM-V5-PLANNING as identity are rejected | Part 11.5b application intake tests |
| BR-V7-AI | Family label in "New V7 business requirements \| 27 (BR-V7-AI 8, BR-V7-CJ 12, BR-V7-WEB/ADM 7)" | Family of BR-V7-AI-01…08 (Part 11.1a, Part 11.13a) | per member |
| BR-V7-CJ | Same row; family of BR-V7-CJ-01…12 | BR-V7-CJ-01…12 (Part 11.1a, Part 11.15) | per member |
| UX-TASK-A11 | FSD 40 row D20/T14/R014 "UX-TASK-QA … UX-TASK-A109; UX-TASK-A110; UX-TASK-A111; UX-TASK-A11" — truncated in the customer text | Read as **UX-TASK-A112** (the next item of the sequence; present in Part 6.9a §… row UX-TASK-A112) | Part 6.9a work-item mapping |
| CJ-BR-01 citation | BRD 20 / FSD 18 "CJ-BR-01 \| BR \| All \| Legal basis … breach communication to the ANPD \| LGPD (Law 13.709/2018)" | Brazil pack (Part 11.1b ADR-184; Part 11.15) — the statute is cited as **Lei Geral de Proteção de Dados, Law No. 13.709/2018** (verify current text and ANPD regulations at implementation, as of 28 Nov 2026) | Pack activation gate tests |

### 11.23.5.3 FR-V12-V-003 Per-workflow illustrative cost seeds

| Field | Specification |
|---|---|
| ID | FR-V12-V-003 |
| Requirement | Where FSD ch12 states an "Illustrative internal INR x/invocation" cost source for a workflow, that figure is the default **seed** for (a) the budget reservation estimate of the workflow before measured cost exists and (b) the AU cost estimate column. It "excludes provider/retry/labor and other fees". The seed is replaced by the measured cost per accepted result after 30 days of pilot traffic (OKPI-11/12). The audit found the seed absent for the rows below; all other workflows' seeds are present in Parts 11.3/11.4 |
| Acceptance | TC-V12-V-012; US-04-ZV01 |

{{F:cost}}

All figures are illustrative internal estimates from the customer text, not prices; verify at implementation (as of 28 Nov 2026).

### 11.23.5.4 FR-V12-V-004 ICP attribute set (MT-04)

| Field | Specification |
|---|---|
| ID | FR-V12-V-004 |
| Source | BRD 04 "MT-04 — Individual and professional customer types": "ICP: industry, geography, language, business size, sales motion, target personas, volume, data readiness, regulatory constraints, budget and maturity." |
| Requirement | Each company's operating configuration (configuration revision, A100 business profile template and the onboarding wizard stage "ICP / sales", Part 11.1a A-07-0339) holds an ICP object with all eleven V12 attributes. The ICP feeds discovery scoring (SM-SVC-02), qualification and the matching agents; it never contains personal data |
| Acceptance | TC-V12-V-013…014; US-20-ZV01 |

| Attribute | Type and validation | Notes |
|---|---|---|
| industry | 1–10 codes from the versioned industry registry | same registry as DTO `industry` (App. B) |
| geography | 1–50 ISO 3166-1/-2 codes | outreach still gated by jurisdiction packs |
| language | 1–10 BCP 47 tags from enabled locales (DEC-776) | |
| business_size | enum: micro, small, medium, large, enterprise, plus optional employee band | |
| sales_motion | enum: self-serve, inside sales, field sales, partner-led, tender/bid, marketplace | |
| target_personas | 1–20 persona references (role, seniority, function) | no named individuals |
| volume | expected monthly leads/accounts as integer range (min ≤ max) | sizing input for quotas |
| data_readiness | enum: none, spreadsheet, CRM connected, warehouse; plus data-quality score 0–100 | drives onboarding tasks |
| regulatory_constraints | list of rule-pack references and sector flags (e.g. no patient data, no minors) | MedMaarg and EduVerse invariants enforced |
| budget | amount in minor units + currency + period | used for plan fit, never shown to other tenants |
| maturity | enum: exploring, piloting, scaling, optimizing | |

### 11.23.5.5 FR-V12-V-005 FX rate entry below 1 (D15)

| Field | Specification |
|---|---|
| ID | FR-V12-V-005 |
| Source | BRD/FSD V12 ch01 D15 "FX rate entry (new) — Rate inputs used integer stepping, so realistic rates below 1 (e.g. INR→USD 0.012) failed browser validation and could not be applied. → Rate inputs accept decimals (step any, min 0); negative rates still rejected; conversion verified (A-FX, desktop and mobile)." App. C `fx_rate … rate numeric(20,10) NOT NULL CHECK (rate > 0)` |
| Requirement | Every FX rate input (A083 revenue reconciliation and KPI settings, A110 currency settings, operator rate cards) accepts decimals with up to 10 fractional digits, rejects zero, negatives, non-numeric input and grouping separators, and stores the value in `fx_rate.rate numeric(20,10)` with base and quote currency, direction, effective time, source, version and approver. The UI uses a decimal text input (`inputmode="decimal"`, no integer step), shows the inverse rate and a conversion preview, and formats per locale while storing the canonical dot decimal. Native ledgers stay immutable; converted reporting values reference the rate version (MT-21) |
| Acceptance | TC-V12-V-015…018 (BVA, 11 values exhaustive); US-15-ZV01 |

### 11.23.5.6 FR-V12-V-006 One implementation per behaviour (D12)

| Field | Specification |
|---|---|
| ID | FR-V12-V-006 |
| Source | BRD/FSD V12 ch01 D12 "Layered prototype code … one implementation per behaviour is a production React/TypeScript rule (FSD ch35)"; stage 10 "One requirement per behaviour; duplicates linked not re-numbered" |
| Requirement | The production code holds exactly one implementation of each behaviour (validation rule, policy check, state transition, formatter, API client call). Prototype layers (v4/v5/v6…V8 function layers) are never ported. Shared behaviour lives in one package (`@ge/ui`, `@ge/domain`, Django `core/` services) and is imported, not copied. CI enforces it: a duplicate-code check (token-based, ≥ 50 tokens repeated across modules fails the build unless an ADR exception is linked) and a rule that every requirement ID maps to one owning module |
| Acceptance | TC-V12-V-031…032; US-21-ZV03 |

### 11.23.5.7 FR-V12-V-007 Admin screen baseline rule ("V2 rule")

| Field | Specification |
|---|---|
| ID | FR-V12-V-007 |
| Source | FSD 24 "Admin route registry — 135 registered screens", per screen, row "V2 rule": "Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading/error/held states, audit and keyboard/mobile." |
| Requirement | For **every** registered Admin screen (the {{M:n_v2}} listed below and every later Admin screen): (1) the server resolves the audience (operator, tenant workspace, portfolio, automation operations) and the object-level permission for each record before any data is returned; the client never decides access; (2) no Admin screen publishes tenant content publicly — publication happens only through the authorized SM-SVC-15 path; (3) source mappings shown in V12 (route/data mapping rows) are **not** wired until the API/DTO mapping is approved in Part 11.8; (4) forms validate inline (aria-invalid, aria-describedby, focus to first error); (5) the screen implements loading, empty, error, held and success states; (6) every write emits an audit event with actor, scope and correlation ID; (7) the screen is fully keyboard operable and usable in the compact (mobile) layout (DEC-623). Portfolio audience sees aggregates only; drill-down needs an object-level grant (DEC-504) |
| Acceptance | TC-V12-V-019…026 (classes) and the 40-row exhaustive Examples of US-01-ZV01 |

**Screens carrying the V2 rule in V12 ch24 (literal names).**

{{F:v2}}

### 11.23.5.8 FR-V12-V-008 Mandate engine: securities-governed investment actions are never mandated

| Field | Specification |
|---|---|
| ID | FR-V12-V-008 |
| Source | DEC-779 ("each jurisdiction must permit the action — where lawful"), DEC-783 (securities-law gates), DEC-822 and CP-O-04 (Part 11.16), Part 11.17a mandate engine; erratum E-V-13 |
| Requirement | The Part 11.17 mandate engine keeps a deny-list of action classes that no mandate may cover: offer issue, offering-tagged (promotion) dispatch, closing, allotment reference, filing status, cap-table revision, vote certification, KYC decision and external submission of the Investment Automation product. A mandate whose scope includes any of them is rejected at issue (`MANDATE_NOT_ALLOWED_SECURITIES`), and the PDP rejects any dispatch of these classes that references a mandate, even if one exists. These actions stay L1 with hash-bound, per-action approval (two-person for closing and cap table). The only INV mandate type is `inv_ir_message` for non-offering investor-relations messages, which follows all DEC-779 conditions |
| Acceptance | TC-V12-V-027…030 and the 40-row exhaustive Examples of US-18-ZV01 |

### 11.23.5.9 FR-V12-V-009 Errata governance and documentation lint

| Field | Specification |
|---|---|
| ID | FR-V12-V-009 |
| Requirement | The errata of Part 11.23c are binding (DEC-961). A documentation CI job runs `v_20_errata.py` (stale patterns) and `v_21_screen_clash.py` on every change to `Part-*.md`; a new stale occurrence that does not cite its authority fails the job. The job also regenerates `final/supersession_index.csv` and the artifact register of FR-V12-V-001 |
| Acceptance | TC-V12-V-033…034; US-21-ZV04 |

### 11.23.5.10 Test cases (Part 6.2a format)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-V-001 | As-received V12 HTML hash differs from the declared hash | FR-V12-V-001 · US-21-ZV01 AC-21ZV01-01 | `commercial_website_desktop_V12.html` as received (CRLF) | 1. Run the integrity check. 2. Read the register row | As-received 8ceb0c24…; declared b9c3fa5c…; result "MISMATCH as received" recorded, then normalisation step runs | P1 | Negative | EP | Y | SYS |
| TC-V12-V-002 | LF-normalised hash matches the declared hash | FR-V12-V-001 · AC-21ZV01-01 | Same file | 1. Convert CRLF→LF in memory. 2. Hash | b9c3fa5c… equals declared; result "MATCH (LF-normalised)"; baseline not held | P1 | Positive | EP | Y | SYS |
| TC-V12-V-003 | All four HTML prototypes verified | FR-V12-V-001 · AC-21ZV01-01 | 4 HTML files (M4 rows 1–8) | 1. Run the check for each | 4/4 LF-normalised matches; 4 as-received mismatches recorded with cause "CRLF in transit" | P1 | Positive | EP | Y | SYS |
| TC-V12-V-004 | Binary artifacts without a declared hash become the reference | FR-V12-V-001 · AC-21ZV01-02 | BRD/FSD V12 .docx | 1. Run the check | Rows created with as-received SHA-256 7be408bf… and 0c90b8d6…; result "reference set" | P2 | Positive | EP | Y | SYS |
| TC-V12-V-005 | Historical archive matches byte for byte | FR-V12-V-001 | `38 documents.zip` | 1. Hash | 6fa3a27b… equals declared | P2 | Positive | EP | Y | SYS |
| TC-V12-V-006 | Tampered text artifact holds the baseline | FR-V12-V-001 · AC-21ZV01-03 | Copy of the website desktop file with one character changed | 1. Run the check | Both hashes mismatch; status "Held — integrity"; review groups cannot start; CONFLICT raised to the customer | P0 | Negative | EG | Y | SYS |
| TC-V12-V-007 | Lineage entry required for a merged version | FR-V12-V-001 · AC-21ZV01-04 | New version V13 registered without inputs | 1. Promote V13 | Promotion refused "LINEAGE_REQUIRED" until inputs and roles are recorded | P2 | Negative | EP | Y | SYS |
| TC-V12-V-008 | Unknown Website and Admin addresses show the not-found view (PT-V7-02, PT-V7-10) | FR-V12-V-002 · BR-V7-WEB-01 · TC-V12-J-102 | Signed out: `/does-not-exist`; signed in Admin: `/admin/zzz` | 1. Open each | Website 404 view with navigation; Admin 404 inside the shell; HTTP 404; no tenant data; no console error | P2 | Negative | EP | Y | E2E |
| TC-V12-V-009 | Accessible form errors (PT-V7-03) | FR-V12-V-002 · BR-V7-WEB-02 · TC-V12-J-103 | W12 lead form empty submit | 1. Submit empty. 2. Read focus and ARIA | Errors next to fields; aria-invalid and aria-describedby set; focus on first invalid field; screen reader announces the error | P1 | Negative | EP | Y | E2E |
| TC-V12-V-010 | Operational workspace search and filter (PT-V7-09) | FR-V12-V-002 · BR-V7-ADM-03 | A038 with 120 records of the granted company | 1. Search "renewal". 2. Filter status Held | Only matching records of the granted scope; review actions shown per contract card | P2 | Positive | EP | Y | E2E |
| TC-V12-V-011 | Requester cannot approve; completion only after receipt (PT-V7-14) | FR-V12-V-002 · BR-V7-ADM-01/02 · DB-T5/T6 | Run requested by `asha`; provider receipt pending | 1. `asha` approves. 2. Another reviewer approves. 3. Receipt arrives | Step 1 → 403 SELF_APPROVAL; step 2 → Running→Reconciling; Succeeded only after the receipt matches | P0 | Negative | DT | Y | SYS |
| TC-V12-V-012 | Cost seed used until measured cost exists | FR-V12-V-003 | SM-SVC-01-WF01 seed INR 1.51/invocation; no measured cost | 1. Start a run. 2. Read reservation | Reservation estimate uses ₹1.51 × invocations; after 30 days of measured cost the seed is replaced and the change audited | P2 | Positive | EP | Y | IT |
| TC-V12-V-013 | ICP accepts all eleven attributes | FR-V12-V-004 | Valid ICP JSON for AppNAI | 1. Save configuration revision | Saved; revision increments; approver ≠ author | P2 | Positive | EP | Y | IT |
| TC-V12-V-014 | ICP rejects personal data and invalid ranges | FR-V12-V-004 | target_personas contains an e-mail address; volume min > max | 1. Save | 422 ICP_PERSONAL_DATA and ICP_RANGE; nothing saved | P1 | Negative | BVA | Y | IT |
| TC-V12-V-015 | FX rate 0.012 accepted (D15) | FR-V12-V-005 · M3 row 1 | INR→USD | 1. Enter 0.012 on A110 | Stored 0.0120000000; inverse 83.33 shown; audit event | P1 | Positive | BVA | Y | E2E |
| TC-V12-V-016 | FX rate 0 and negative rejected | FR-V12-V-005 · M3 rows 7–8 | 0; -0.5 | 1. Enter each | FX_RATE_NOT_POSITIVE inline; nothing stored | P1 | Negative | BVA | Y | E2E |
| TC-V12-V-017 | FX precision bound | FR-V12-V-005 · M3 rows 5–6 | 0.0000000001; 0.00000000001 | 1. Enter each | First accepted; second FX_RATE_PRECISION | P2 | Negative | BVA | Y | IT |
| TC-V12-V-018 | FX format rules and locale | FR-V12-V-005 · M3 rows 9–11 | "abc"; "1,000.5"; de-DE entry "83,25" | 1. Enter each | FX_RATE_FORMAT for the first two; de-DE value parsed to 83.25 and stored with dot decimal | P2 | Negative | EP | Y | E2E |
| TC-V12-V-019 | Ungranted object never rendered (any audience) | FR-V12-V-007 · M1 rows "not granted" | 20 rows of M1 | 1. Open screen with object not granted | 403 from API; denied view; no record data in DOM or bundle; audit `access.denied` | P0 | Negative | DT | Y | E2E |
| TC-V12-V-020 | Portfolio audience sees aggregates only | FR-V12-V-007 · DEC-504 | R01 portfolio, A089 | 1. Open; 2. Try drill-down without object grant | Aggregates only; drill-down denied | P0 | Negative | EP | Y | E2E |
| TC-V12-V-021 | Loading state | FR-V12-V-007 | Slow API (2 s stub) | 1. Open A058 | Skeleton with aria-busy; actions disabled; no partial rows | P2 | Positive | EP | Y | E2E |
| TC-V12-V-022 | Empty state | FR-V12-V-007 | Granted company with 0 records | 1. Open A065 | Empty state with only permitted create action | P3 | Positive | EP | Y | E2E |
| TC-V12-V-023 | Error state keeps form values | FR-V12-V-007 | API 500 on save | 1. Save a form | Error with retry and correlation ID; values kept; no duplicate write on retry (idempotency key) | P1 | Negative | EG | Y | E2E |
| TC-V12-V-024 | Held state disables effects | FR-V12-V-007 | Record held by PDP (BUDGET_EXHAUSTED) | 1. Open | Held banner with reason code and owner; effect actions disabled | P1 | Negative | EP | Y | E2E |
| TC-V12-V-025 | No public tenant publication from Admin | FR-V12-V-007 | A107/A108 publish attempt outside SM-SVC-15 | 1. Call publish | 403 PUBLICATION_NOT_AUTHORIZED; nothing published | P0 | Negative | EP | Y | SYS |
| TC-V12-V-026 | Keyboard and compact layout | FR-V12-V-007 | Every registered screen at 390 px | 1. Tab through; 2. operate primary action | All actions reachable by keyboard; no page-level horizontal overflow (TC-V12-J-102) | P2 | Positive | EP | Y | E2E |
| TC-V12-V-027 | Mandate including a securities action rejected at issue | FR-V12-V-008 · DEC-822 | Draft mandate scope {closing} | 1. Submit for two-person approval | MANDATE_NOT_ALLOWED_SECURITIES; mandate not created | P0 | Negative | DT | Y | SYS |
| TC-V12-V-028 | Dispatch of a securities action referencing a mandate rejected by the PDP | FR-V12-V-008 · M2 | Active `inv_ir_message` mandate; dispatch class "offering-tagged dispatch" | 1. Dispatch | PDP deny; held for per-action L1 approval | P0 | Negative | DT | Y | SYS |
| TC-V12-V-029 | Non-offering IR message under an Active mandate in an approved jurisdiction | FR-V12-V-008 · M2 | Mandate Active; pack Approved; caps not exceeded | 1. Dispatch | Allowed (L3) after PDP recheck; audit and reconciliation records | P1 | Positive | DT | Y | SYS |
| TC-V12-V-030 | IR message with revoked mandate or unapproved jurisdiction | FR-V12-V-008 · M2 | Mandate Revoked / pack Not approved | 1. Dispatch | MANDATE_INACTIVE or JURISDICTION_NOT_APPROVED; held; no dispatch | P0 | Negative | DT | Y | SYS |
| TC-V12-V-031 | Duplicate implementation fails CI | FR-V12-V-006 | PR copies a 60-token validation function into a second module | 1. Run CI | Duplicate-code check fails with both locations; merge blocked unless ADR exception linked | P2 | Negative | EG | Y | UT |
| TC-V12-V-032 | Requirement owned by one module | FR-V12-V-006 | Two modules annotate `@req FR-A034` as owner | 1. Run CI | OWNER_DUPLICATE failure | P3 | Negative | EP | Y | UT |
| TC-V12-V-033 | New stale statement fails the documentation lint | FR-V12-V-009 | PR adds "service key held server-side" to a part | 1. Run doc CI | E-V-03 stale occurrence; job fails | P2 | Negative | EP | Y | UT |
| TC-V12-V-034 | Annotated mention passes | FR-V12-V-009 | PR adds the same phrase with "superseded by DEC-778" | 1. Run doc CI | Counted as annotated; job passes | P3 | Positive | EP | Y | UT |

### 11.23.5.11 User stories (Part 5.1a/b template; Scenario Outline + Examples from the models of `v_31_combi.py`)

##### US-21-ZV01 Artifact integrity check on every customer delivery

| Field | Value |
|---|---|
| ID | US-21-ZV01 |
| Title | Verify and register every customer artifact before review starts |
| Type | Enabler |
| Story | As the configuration-management lead, I need every delivered BRD, FSD, prototype and archive hashed, compared with its declared hash and registered with its lineage, so that the team reviews exactly the baseline the customer declared |
| Persona / roles | Configuration-management lead; Product Owner (approver) |
| Traces | FR-V12-V-001; DEC-968; CONFLICT-1184; BRD/FSD V12 ch01 |
| Priority | Must |
| Wave | W0 |
| Points | 2–3 |
| Dependencies | FR-V12-V-009 documentation CI |
| Dimension profile | A1 · S1 · D1 · T6 |
| Notes | Model M4: 7 artifacts × 2 modes = 14 combinations, exhaustive |

```gherkin
Feature: Artifact integrity check on every customer delivery
  @happy @neg
  Scenario Outline: AC-21ZV01-01 Integrity result per artifact and hashing mode
    Given the customer delivery contains "<artifact>"
    When the integrity check hashes it in mode "<mode>"
    Then the register records "<expected>"
    Examples:
{{F:m4}}

  @alt
  Scenario: AC-21ZV01-02 Binary artifact without declared hash
    Given "Sales_Marketing_Automation_BRD_V12.docx" has no declared hash
    When the integrity check runs
    Then the as-received SHA-256 becomes the reference and the row is marked "reference set"

  @neg @sec
  Scenario: AC-21ZV01-03 Content mismatch holds the baseline
    Given a text artifact whose hash mismatches in both modes
    When the integrity check runs
    Then the baseline status is "Held — integrity" and no review group can start

  @val
  Scenario: AC-21ZV01-04 Lineage required
    Given a new version without recorded inputs
    When it is promoted
    Then promotion fails with "LINEAGE_REQUIRED"
```

##### US-21-ZV02 Complete traceability for restored V12 IDs

| Field | Value |
|---|---|
| ID | US-21-ZV02 |
| Title | Register restored V12 identifiers in the RTM |
| Type | Enabler |
| Story | As the QA lead, I need PT-V7, DB-V2, SM-V5 and the V7 family labels mapped to blueprint requirements and tests, so that the RTM has no V12 ID without a home |
| Persona / roles | QA lead; Business Systems Analyst |
| Traces | FR-V12-V-002; BR-V7-WEB-01…03; BR-V7-ADM-01…03 |
| Priority | Should |
| Wave | W0 |
| Points | 1–2 |
| Dependencies | Part 11.11 RTM generator |
| Dimension profile | T6 |
| Notes | 11 IDs + 1 citation |

```gherkin
Feature: Complete traceability for restored V12 IDs
  @happy
  Scenario Outline: AC-21ZV02-01 Each restored ID resolves to a blueprint requirement and a test
    Given the RTM is generated
    When I look up "<v12_id>"
    Then it maps to "<mapping>" and test "<test>"
    Examples:
      | v12_id | mapping | test |
      | PT-V7-02 | BR-V7-WEB-01 not-found view | TC-V12-V-008 |
      | PT-V7-10 | BR-V7-WEB-01 Admin not-found view | TC-V12-V-008 |
      | PT-V7-03 | BR-V7-WEB-02 accessible form errors | TC-V12-V-009 |
      | PT-V7-09 | BR-V7-ADM-03 useful workspaces | TC-V12-V-010 |
      | PT-V7-14 | BR-V7-ADM-01/02 SoD and reconciled completion | TC-V12-V-011 |
      | DB-V2-SUBSCRIPTION | saas_subscription + saas_sku_grant | Part 11.5b subscription tests |
      | DB-V2-CONFIG | configuration_revision | Part 11.9b DDL tests |
      | SM-V5-PLANNING | non-identity worksheet; SM-APPLICATION-6 is the hand-off | Part 11.5b intake tests |
```

##### US-04-ZV01 Workflow cost seeds

| Field | Value |
|---|---|
| ID | US-04-ZV01 |
| Title | Seed budget reservations with the V12 illustrative cost until measured |
| Type | Feature |
| Story | As the FinOps lead, I need every workflow to start with the V12 illustrative cost per invocation, so that reservations are sensible from day one and are replaced by measured cost |
| Persona / roles | FinOps lead; automation operations |
| Traces | FR-V12-V-003; OKPI-11/12; DEC-008 |
| Priority | Should |
| Wave | W1 |
| Points | 1–2 |
| Dependencies | AU cost ledger |
| Dimension profile | C3 · I1 |
| Notes | Seeds are estimates; verify |

```gherkin
Feature: Workflow cost seeds
  @happy
  Scenario: AC-04ZV01-01 Seed used before measured cost
    Given workflow "SM-SVC-01-WF01" has seed ₹1.51 per invocation and no measured cost
    When a run reserves budget for 10 invocations
    Then the reservation is ₹15.10
  @alt
  Scenario: AC-04ZV01-02 Measured cost replaces the seed
    Given 30 days of measured cost per accepted result exist
    When the nightly cost job runs
    Then the seed is replaced and the change is audited
```

##### US-20-ZV01 ICP attributes

| Field | Value |
|---|---|
| ID | US-20-ZV01 |
| Title | Capture the full V12 ICP in the company configuration |
| Type | Feature |
| Story | As a tenant administrator, I want to describe my ideal customer with the eleven V12 attributes, so that discovery and qualification target the right accounts |
| Persona / roles | Tenant administrator (R02); reviewer |
| Traces | FR-V12-V-004; MT-04; A100 |
| Priority | Should |
| Wave | W1 |
| Points | 2–3 |
| Dependencies | Configuration revisions (Part 11.9a) |
| Dimension profile | D1 · I1 |
| Notes | No personal data in the ICP |

```gherkin
Feature: ICP attributes
  @happy
  Scenario: AC-20ZV01-01 Save a complete ICP
    Given all eleven ICP attributes are valid
    When the administrator saves the configuration revision
    Then the revision is stored and awaits approval by another user
  @neg @priv
  Scenario: AC-20ZV01-02 Personal data rejected
    Given target_personas contains "ravi@example.com"
    When the administrator saves
    Then the API returns 422 "ICP_PERSONAL_DATA"
```

##### US-15-ZV01 FX rates below 1

| Field | Value |
|---|---|
| ID | US-15-ZV01 |
| Title | Enter realistic FX rates including values below 1 |
| Type | Feature |
| Story | As a finance user, I want to enter rates such as INR→USD 0.012, so that multi-currency reporting is correct |
| Persona / roles | Finance (R08/R09) |
| Traces | FR-V12-V-005; MT-21; D15 |
| Priority | Must |
| Wave | W2 |
| Points | 1–2 |
| Dependencies | fx_rate table |
| Dimension profile | D1 · I1 |
| Notes | Model M3, 11 values exhaustive |

```gherkin
Feature: FX rates below 1
  @happy @neg @val
  Scenario Outline: AC-15ZV01-01 Boundary values of the FX rate input
    When the finance user enters "<input>"
    Then the input is "<outcome>" with "<detail>"
    Examples:
{{F:m3}}
```

##### US-21-ZV03 One implementation per behaviour

| Field | Value |
|---|---|
| ID | US-21-ZV03 |
| Title | Enforce one implementation per behaviour in CI |
| Type | Enabler |
| Story | As the principal engineer, I need CI to fail on duplicated behaviour, so that the production code never repeats the layered prototype pattern |
| Persona / roles | Principal engineer |
| Traces | FR-V12-V-006; D12; FSD ch35 |
| Priority | Should |
| Wave | W0 |
| Points | 1–2 |
| Dependencies | CI pipeline (PL-04) |
| Dimension profile | T6 |
| Notes | ADR exception path |

```gherkin
Feature: One implementation per behaviour
  @neg
  Scenario: AC-21ZV03-01 Duplicate behaviour blocked
    Given a pull request duplicates a 60-token function in a second module
    When CI runs
    Then the duplicate-code check fails and names both locations
```

##### US-01-ZV01 Admin screen baseline rule

| Field | Value |
|---|---|
| ID | US-01-ZV01 |
| Title | Apply the V12 V2 rule to every Admin screen |
| Type | Enabler |
| Story | As the security and UX lead, I need every Admin screen to resolve audience and object permissions on the server and to implement the five UI states, audit, keyboard and compact layout, so that no screen leaks data or behaves differently from its contract |
| Persona / roles | R01, R02, R13, R14 |
| Traces | FR-V12-V-007; FSD 24 V2 rule; DEC-504; DEC-623; CA-ADMIN |
| Priority | Must |
| Wave | W0 (pattern) then per screen |
| Points | 3–5 (pattern and tests) |
| Dependencies | ABAC-01…12; Part 11.7b contracts |
| Dimension profile | A1, A5 · S1, S3 · D1 · T6 |
| Notes | Model M1: 4 audiences × 2 grants × 5 states = 40, exhaustive |

```gherkin
Feature: Admin screen baseline rule
  @perm @sec @a11y
  Scenario Outline: AC-01ZV01-01 Audience, grant and UI state
    Given a user with role "<role>" in the "<audience>" experience
    And the object permission is "<grant>"
    When the screen is in state "<state>"
    Then the user sees "<expected>"
    Examples:
{{F:m1}}
```

##### US-18-ZV01 Securities-governed actions never mandated

| Field | Value |
|---|---|
| ID | US-18-ZV01 |
| Title | Reject mandates and mandated dispatch for securities-governed INV actions |
| Type | Feature |
| Story | As the compliance lead, I need the mandate engine and the PDP to refuse any mandate for securities-governed actions, so that DEC-779 automation never touches regulated offer, closing or filing steps |
| Persona / roles | Compliance lead; issuer authority (R02); R10 |
| Traces | FR-V12-V-008; DEC-779; DEC-783; DEC-822; DEC-963; CP-O-04 |
| Priority | Must |
| Wave | W5 / Release 2 (with Part 11.16/11.17) |
| Points | 2–3 |
| Dependencies | Part 11.17 mandate engine; Part 11.16 action classes |
| Dimension profile | A1 · S1, S3 · C3 |
| Notes | Model M2: 10 action classes × 2 mandate states × 2 jurisdiction states = 40, exhaustive (3-way by construction) |

```gherkin
Feature: Securities-governed actions are never mandated
  @neg @sec @law
  Scenario Outline: AC-18ZV01-01 Mandate eligibility by action class, mandate state and jurisdiction pack
    Given an INV action of class "<action_class>"
    And a referenced mandate in state "<mandate>"
    And the jurisdiction rule pack is "<jurisdiction_pack>"
    When the PDP evaluates the dispatch
    Then the outcome is "<expected>"
    Examples:
{{F:m2}}
```

##### US-21-ZV04 Errata lint

| Field | Value |
|---|---|
| ID | US-21-ZV04 |
| Title | Fail documentation CI on new stale statements |
| Type | Enabler |
| Story | As the configuration-management lead, I need the errata patterns checked on every documentation change, so that superseded rules are never reintroduced without their authority |
| Persona / roles | Configuration-management lead |
| Traces | FR-V12-V-009; DEC-961; E-V-01…47 |
| Priority | Should |
| Wave | W0 |
| Points | 1 |
| Dependencies | `v_20_errata.py` |
| Dimension profile | T6 |
| Notes | — |

```gherkin
Feature: Errata lint
  @neg
  Scenario: AC-21ZV04-01 Stale statement fails
    Given a change adds "service key held server-side"
    When documentation CI runs
    Then erratum E-V-03 reports a stale occurrence and the job fails
  @alt
  Scenario: AC-21ZV04-02 Annotated statement passes
    Given the same phrase cites "superseded by DEC-778"
    When documentation CI runs
    Then the occurrence is counted as annotated and the job passes
```

### 11.23.5.12 Effort and cost of the restored content (estimate)

| Item | Points | Person-days (0.5 / 0.7 / 1.0 pd per SP) | Basis |
|---|---|---|---|
| US-21-ZV01 + 02 + 03 + 04 | 5–8 | 2.5 / 4.6 / 8 | Part 5.5.1 conversion |
| US-01-ZV01 | 3–5 | 1.5 / 2.8 / 5 | pattern + tests; per-screen work already inside each screen story |
| US-04-ZV01, US-20-ZV01, US-15-ZV01 | 4–7 | 2 / 3.9 / 7 | |
| US-18-ZV01 | 2–3 | 1 / 1.8 / 3 | inside CR-V12-P |
| **Total** | **14–23** | **7 / 13.1 / 23 pd** | ≈ ₹0.3–1.0 lakh at the Part 8.4 blended rate; funded under DEC-790 (estimate, verify) |

No running cost is added (CI minutes are inside the existing pipeline budget).

---

**Continued in Part 11.23b (baseline retention check) and Part 11.23c (errata, conflicts, decisions, tags, quality gate).**
