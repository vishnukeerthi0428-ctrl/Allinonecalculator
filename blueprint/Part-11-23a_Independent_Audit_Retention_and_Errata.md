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
| Files read | **76** normative chapter files (BRD 00–25 + appendix; FSD 00–40 + appendices A, A2, B, C, C2, D) |
| Bytes read | **3,681,899** bytes (≈ 3.7 MB) |
| Excluded | `BRD/ZZ_Historical_annex.txt` (4,015,412 B) and `FSD/ZZ_Historical_annex.txt` (11,356,732 B): "V1 retained text (non-normative)", audited separately by Part 11.12 |
| Statements extracted | **19,274** requirement-like statements (15,568 unique after normalisation; duplicates are the same requirement stated in BRD and FSD or repeated per screen/workflow) |
| Unit types | row 15,843; prose 1,821; heading 625; ddl 502; api 327; dto 156 |
| Blueprint compared | every `Part-*.md` in the blueprint directory except this part: 134 files, 197,332 lines (Parts 0–9.10, 0B, 11.0–11.22 as present at the run) |

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

1. **Triage set.** 1,078 statements: weak or none matches, plus statements whose thresholds were not found, plus statements carrying an ID absent from the blueprint.
2. **Context reading.** Each triaged statement was printed with its chapter, section path and best blueprint location, de-duplicated by text, and read. Rows that follow one template (for example the "source disposition candidate" rows of FSD chapter 40, or the DDL statements of Appendices C/C2) were verified **programmatically per row**: the object each row names (API path, entity, QC, task, test ID, table) was looked up in the blueprint and its location recorded.
3. **Classes.** *Covered in different words* (citation: part, section, line, ID) · *Not covered* (content written in §11.23.5 with FR-V12-V / TC-V12-V / US-…-ZV IDs) · *Superseded by a Founder decision* (DEC cited). An overlay also catches statements that **match** the blueprint lexically but state a rule that a Founder decision has since changed.
4. **Manual decisions.** 96 distinct statements needed a reader's judgement; each decision is listed in §11.23.3.4 and stored in `v_manual.tsv` keyed by the statement's text hash, so identical BRD and FSD copies share one decision.

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

Outputs: `final/coverage_v12/V_audit.csv` (one row per statement, 19,274 rows, with the measures, the classification and the citation), `final/supersession_index.csv`, and the working files in `assembly/v12b/v_out/`.

---

## 11.23.2 Coverage summary (measured before and after)

### 11.23.2.1 Measured lexical match

"Before" is the blueprint without this part; "after" includes Parts 11.23a–c. Both runs used the same snapshot of the other parts.

| Measure | Before (blueprint without Part 11.23) | After (with Part 11.23) | Method |
|---|---|---|---|
| Statements extracted (requirement-like) | 19,274 | 19,274 | `v_01_extract.py`: prose sentences with a modal, ID or threshold; every non-header table row; ID headings; 330 OpenAPI operations; 156 DTO schemas; SQL statements |
| Distinct V12 IDs in the statements | 6,795 | 6,795 | `ID_RE` + screen IDs |
| ID presence, literal | 90.26% | 90.34% | exact ID string in `Part-*.md` |
| ID presence, literal + range/compressed | 99.92% | 100.00% | adds range notation (`X-001…045`) and the Part 11.10b compressed test catalogue |
| Distinct IDs absent | 11 | 0 | listed in §11.23.5.2 |
| Mean 6-gram containment | 0.491 | 0.504 | share of the statement's 6-word shingles found anywhere in the blueprint |
| Mean token containment (best passage) | 0.853 | 0.860 | content tokens of the statement found in the best blueprint passage (line ±2) or in the lines carrying its IDs |
| Threshold presence (1,074 statements with thresholds) | 97.11% | 98.29% | numbers with unit, comparator, currency or decimals found in the matched passage, the ID lines, or a line sharing ≥ 50% of the tokens |
| Level exact | 5,123 | 5,328 | §11.23.1.3 thresholds |
| Level strong | 10,698 | 10,828 | §11.23.1.3 thresholds |
| Level moderate | 2,409 | 2,355 | §11.23.1.3 thresholds |
| Level weak | 1,015 | 755 | §11.23.1.3 thresholds |
| Level none | 29 | 8 | §11.23.1.3 thresholds |
| **Measured lexical match (exact + strong + moderate)** | **94.58%** | **96.04%** | deterministic; reproducible with `v_02_match.py before` and `after` |

**Reading.** The blueprint already reproduced V12 closely: 94.58% of the statements match at moderate level or better before this audit, and 99.92% of V12 ID occurrences are present (literally or through range and compressed notation). The weak residue is concentrated in metadata-heavy registers (FSD 40 source dispositions, prototype lineage, DDL policies) and in a small set of genuinely missing items. After the restored content, the measured match is **96.04%**; the remaining lexical gap is closed by classification, not by copying text (§11.23.2.2).

### 11.23.2.2 End state of every statement (after classification)

| End state | Statements | Share | Meaning |
|---|---|---|---|
| Matched (measured exact/strong/moderate, not triaged) | 18,194 | 94.4% | text, IDs and thresholds found |
| Covered in different words (cited) | 910 | 4.7% | read in context; part, section, line and ID cited in `V_audit.csv` |
| Not covered → restored in this part | 164 | 0.9% | FR-V12-V-001…007 at full depth (§11.23.5) |
| Correctly superseded by a Founder decision | 6 | 0.0% | DEC cited |
| **Total with a verified end state** | **19,274** | **100%** | 0 unclassified |

### 11.23.2.3 What was genuinely missing

| # | Missing content | Statements | Restored as |
|---|---|---|---|
| 1 | Artifact lineage and integrity: SHA-256 of the V7/V8/V9/V12 prototypes and documents, the V8 merge lineage, the V8 stage-gate register, version-label defects | 48 | FR-V12-V-001, §11.23.5.1 (also found: the four V12 HTML files as received do **not** match their declared hashes until CRLF line endings are normalised — CONFLICT-1184) |
| 2 | V12 identifiers absent from the blueprint: PT-V7-02, -03, -09, -10, -14; DB-V2-SUBSCRIPTION; DB-V2-CONFIG; SM-V5-PLANNING; family labels BR-V7-AI and BR-V7-CJ; truncated UX-TASK-A11 | 14 | FR-V12-V-002, §11.23.5.2 |
| 3 | Illustrative cost per invocation for workflows whose seed was absent | 7 | FR-V12-V-003, §11.23.5.3 |
| 4 | ICP attribute set of MT-04 | 1 | FR-V12-V-004, §11.23.5.4 |
| 5 | FX rate entry below 1 (D15) | 2 | FR-V12-V-005, §11.23.5.5 |
| 6 | Production rule "one implementation per behaviour" (D12) | 2 | FR-V12-V-006, §11.23.5.6 |
| 7 | The V12 per-screen "V2 rule" for Admin screens (stated on 90 registered screens) | 90 | FR-V12-V-007, §11.23.5.7 |
| 8 | Two consequences found by the audit (not V12 statements): the mandate engine's treatment of securities-governed INV actions, and errata governance | — | FR-V12-V-008 and FR-V12-V-009, §11.23.5.8–11.23.5.9 |

---

## 11.23.3 Detailed register

### 11.23.3.1 Not covered → restored in this part (every statement)

| # | Statement ID | Chapter | Section | Statement (V12, literal) | Restored by |
|---|---|---|---|---|---|
| 1 | VS-000042 | 01_Executive_Summary_P | V11 / Final controlled baseline | C8 / Stale label / Website browser-tab title still showed “V9”. / Corrected to V11 on both website builds. | FR-V12-V-001 |
| 2 | VS-000087 | 01_Executive_Summary_P | V9 / Release baseline — promotion of retained s… | commercial_website_desktop_V9.html / 2e3cba0d309fb73fb37a03ff13c9e7524eeaca5e068d8766a92600a66df5e5b9 | FR-V12-V-001 |
| 3 | VS-000088 | 01_Executive_Summary_P | V9 / Release baseline — promotion of retained s… | commercial_website_mobile_V9.html / 60d9e7a2ea6e7794821ffe0c081f97533885e6edff92fdd39f5386b959c7a6bc | FR-V12-V-001 |
| 4 | VS-000089 | 01_Executive_Summary_P | V9 / Release baseline — promotion of retained s… | commercial_admin_desktop_V9.html / aa7fe03ca5ee38e3fc209e6628bc5961bf7f746aa62749e6faf1198458f4142f | FR-V12-V-001 |
| 5 | VS-000090 | 01_Executive_Summary_P | V9 / Release baseline — promotion of retained s… | commercial_admin_mobile_V9.html / 5cf8bccfe336ac9ec928e51d030fb0c45e50894c9d41192cc59b73497db628f3 | FR-V12-V-001 |
| 6 | VS-000101 | 01_Executive_Summary_P | V8 / Release baseline, merge lineage and source… | commercial_website_desktop_V9.html / 2e3cba0d309fb73fb37a03ff13c9e7524eeaca5e068d8766a92600a66df5e5b9 | FR-V12-V-001 |
| 7 | VS-000102 | 01_Executive_Summary_P | V8 / Release baseline, merge lineage and source… | commercial_website_mobile_V9.html / 60d9e7a2ea6e7794821ffe0c081f97533885e6edff92fdd39f5386b959c7a6bc | FR-V12-V-001 |
| 8 | VS-000103 | 01_Executive_Summary_P | V8 / Release baseline, merge lineage and source… | commercial_admin_desktop_V9.html / aa7fe03ca5ee38e3fc209e6628bc5961bf7f746aa62749e6faf1198458f4142f | FR-V12-V-001 |
| 9 | VS-000104 | 01_Executive_Summary_P | V8 / Release baseline, merge lineage and source… | commercial_admin_mobile_V9.html / 5cf8bccfe336ac9ec928e51d030fb0c45e50894c9d41192cc59b73497db628f3 | FR-V12-V-001 |
| 10 | VS-000105 | 01_Executive_Summary_P | Source reconciliation (inputs to V8) | Sales_Marketing_Automation_BRD_V7.docx (responsive) / User / Base document for BRD V8 / 49b96a10f6ecc51b… | FR-V12-V-001 |
| 11 | VS-000106 | 01_Executive_Summary_P | Source reconciliation (inputs to V8) | Sales_Marketing_Automation_FSD_V7.docx (responsive) / User / Base document for FSD V8 / 61f5753fbe0de5a4… | FR-V12-V-001 |
| 12 | VS-000107 | 01_Executive_Summary_P | Source reconciliation (inputs to V8) | commercial_website_desktop_V7.html / User / Base for website desktop V8 / 1f2743a4587c2bd7… | FR-V12-V-001 |
| 13 | VS-000108 | 01_Executive_Summary_P | Source reconciliation (inputs to V8) | commercial_website_mobile_V7.html / User / Base for website mobile V8 / 7001283bb524d203… | FR-V12-V-001 |
| 14 | VS-000109 | 01_Executive_Summary_P | Source reconciliation (inputs to V8) | commercial_admin_desktop_V7.html / User / Base for Admin desktop V8 / a5cd10f964b75b7c… | FR-V12-V-001 |
| 15 | VS-000110 | 01_Executive_Summary_P | Source reconciliation (inputs to V8) | commercial_admin_mobile_V7.html / User / Base for Admin mobile V8 / 85179014b82161a1… | FR-V12-V-001 |
| 16 | VS-000112 | 01_Executive_Summary_P | Source reconciliation (inputs to V8) | Sales_Marketing_Automation_FSD_V7.docx (functional) / Claude / Source of AIX/CJ-R, appendices A–D, registers, tests / 6e7e68ccfed4a206… | FR-V12-V-001 |
| 17 | VS-000113 | 01_Executive_Summary_P | Source reconciliation (inputs to V8) | commercial_website_V7.html (functional) / Claude / Source of website functional layer / 0fd2e7f1a9cbeb10… | FR-V12-V-001 |
| 18 | VS-000114 | 01_Executive_Summary_P | Source reconciliation (inputs to V8) | commercial_admin_V7.html (functional) / Claude / Source of Admin functional layer / 2a5e141ead128326… | FR-V12-V-001 |
| 19 | VS-000116 | 01_Executive_Summary_P | V8 / Executive change summary | D1 / Version labels / HTML titles and banners showed V5/V6. / All four artifacts labelled V8.0; SHA-256 of delivered HTML recorded in BRD and FSD. | FR-V12-V-001 |
| 20 | VS-000127 | 01_Executive_Summary_P | V8 / Executive change summary | D12 / Layered prototype code / v4/v5/v6 function layers. / Still partial by design: prototypes keep traceable layers (V3–V8); one implementation per… | FR-V12-V-006 |
| 21 | VS-000131 | 01_Executive_Summary_P | V8 / Executive change summary | M1 / Two V7 lines / The responsive V7 set (6 files, 18 MOB requirements) and the functional V7 set (4 files, AI + compliance) diverged from V6. / Mer… | FR-V12-V-001 |
| 22 | VS-000133 | 01_Executive_Summary_P | V8 / Executive change summary | D15 / FX rate entry (new) / Rate inputs used integer stepping, so realistic rates below 1 (e.g. INR→USD 0.012) failed browser validation and could no… | FR-V12-V-005 |
| 23 | VS-000141 | 01_Executive_Summary_P | V8 / Executive change summary | New V7 business requirements / 27 (BR-V7-AI 8, BR-V7-CJ 12, BR-V7-WEB/ADM 7) | FR-V12-V-002 |
| 24 | VS-000242 | 04_Stakeholders_Person | MT-04 — Individual and professional customer ty… | ICP: industry, geography, language, business size, sales motion, target personas, volume, data readiness, regulatory constraints, budget and maturity. | FR-V12-V-004 |
| 25 | VS-001422 | 12_Public_SaaS_Website | V8 / Website trust, privacy and usability requi… | BR-V7-WEB-01 / Not-found handling / Unknown website or admin addresses show a clear not-found page. / PT-V7-02, PT-V7-10 / FSD ch24 / W*, A* | FR-V12-V-002 |
| 26 | VS-001423 | 12_Public_SaaS_Website | V8 / Website trust, privacy and usability requi… | BR-V7-WEB-02 / Accessible form errors / Form errors appear next to the field, are announced to screen readers and move focus to the first error. / PT… | FR-V12-V-002 |
| 27 | VS-001426 | 12_Public_SaaS_Website | V8 / Website trust, privacy and usability requi… | BR-V7-ADM-01 / Separation of duties / The person who requests a run or record cannot approve it. / PT-V7-14; DB-T5 / MT/approval policy / A033/A110,… | FR-V12-V-002 |
| 28 | VS-001427 | 12_Public_SaaS_Website | V8 / Website trust, privacy and usability requi… | BR-V7-ADM-02 / Reconciled completion / A run is complete only after the provider receipt is matched. / PT-V7-14; DB-T6 / FSD ch03 runtime / A033/A110 | FR-V12-V-002 |
| 29 | VS-001428 | 12_Public_SaaS_Website | V8 / Website trust, privacy and usability requi… | BR-V7-ADM-03 / Useful workspaces / Every operational workspace shows searchable, filterable fictional records with review actions. / PT-V7-09 / FSD c… | FR-V12-V-002 |
| 30 | VS-002214 | 24_Business_Acceptance | V8 / Requirement traceability (new requirements) | BR-V7-WEB-01 / FSD ch24 / W*, A* / PT-V7-02, PT-V7-10 | FR-V12-V-002 |
| 31 | VS-002215 | 24_Business_Acceptance | V8 / Requirement traceability (new requirements) | BR-V7-WEB-02 / FSD ch24 / W12–W20, W32, W33, W35 / PT-V7-03, PT-V7-07 | FR-V12-V-002 |
| 32 | VS-002218 | 24_Business_Acceptance | V8 / Requirement traceability (new requirements) | BR-V7-ADM-01 / MT/approval policy / A033/A110, generic screens / PT-V7-14; DB-T5 | FR-V12-V-002 |
| 33 | VS-002219 | 24_Business_Acceptance | V8 / Requirement traceability (new requirements) | BR-V7-ADM-02 / FSD ch03 runtime / A033/A110 / PT-V7-14; DB-T6 | FR-V12-V-002 |
| 34 | VS-002220 | 24_Business_Acceptance | V8 / Requirement traceability (new requirements) | BR-V7-ADM-03 / FSD ch24 / All A screens / PT-V7-09 | FR-V12-V-002 |
| 35 | VS-002462 | 01_Specification_Contr | V11 / Final controlled baseline | C8 / Stale label / Website browser-tab title still showed “V9”. / Corrected to V11 on both website builds. | FR-V12-V-001 |
| 36 | VS-002507 | 01_Specification_Contr | V9 / Release baseline — promotion of retained s… | commercial_website_desktop_V9.html / 2e3cba0d309fb73fb37a03ff13c9e7524eeaca5e068d8766a92600a66df5e5b9 | FR-V12-V-001 |
| 37 | VS-002508 | 01_Specification_Contr | V9 / Release baseline — promotion of retained s… | commercial_website_mobile_V9.html / 60d9e7a2ea6e7794821ffe0c081f97533885e6edff92fdd39f5386b959c7a6bc | FR-V12-V-001 |
| 38 | VS-002509 | 01_Specification_Contr | V9 / Release baseline — promotion of retained s… | commercial_admin_desktop_V9.html / aa7fe03ca5ee38e3fc209e6628bc5961bf7f746aa62749e6faf1198458f4142f | FR-V12-V-001 |
| 39 | VS-002510 | 01_Specification_Contr | V9 / Release baseline — promotion of retained s… | commercial_admin_mobile_V9.html / 5cf8bccfe336ac9ec928e51d030fb0c45e50894c9d41192cc59b73497db628f3 | FR-V12-V-001 |
| 40 | VS-002521 | 01_Specification_Contr | V8 / Release baseline, merge lineage and source… | commercial_website_desktop_V9.html / 2e3cba0d309fb73fb37a03ff13c9e7524eeaca5e068d8766a92600a66df5e5b9 | FR-V12-V-001 |
| 41 | VS-002522 | 01_Specification_Contr | V8 / Release baseline, merge lineage and source… | commercial_website_mobile_V9.html / 60d9e7a2ea6e7794821ffe0c081f97533885e6edff92fdd39f5386b959c7a6bc | FR-V12-V-001 |
| 42 | VS-002523 | 01_Specification_Contr | V8 / Release baseline, merge lineage and source… | commercial_admin_desktop_V9.html / aa7fe03ca5ee38e3fc209e6628bc5961bf7f746aa62749e6faf1198458f4142f | FR-V12-V-001 |
| 43 | VS-002524 | 01_Specification_Contr | V8 / Release baseline, merge lineage and source… | commercial_admin_mobile_V9.html / 5cf8bccfe336ac9ec928e51d030fb0c45e50894c9d41192cc59b73497db628f3 | FR-V12-V-001 |
| 44 | VS-002525 | 01_Specification_Contr | Source reconciliation (inputs to V8) | Sales_Marketing_Automation_BRD_V7.docx (responsive) / User / Base document for BRD V8 / 49b96a10f6ecc51b… | FR-V12-V-001 |
| 45 | VS-002526 | 01_Specification_Contr | Source reconciliation (inputs to V8) | Sales_Marketing_Automation_FSD_V7.docx (responsive) / User / Base document for FSD V8 / 61f5753fbe0de5a4… | FR-V12-V-001 |
| 46 | VS-002527 | 01_Specification_Contr | Source reconciliation (inputs to V8) | commercial_website_desktop_V7.html / User / Base for website desktop V8 / 1f2743a4587c2bd7… | FR-V12-V-001 |
| 47 | VS-002528 | 01_Specification_Contr | Source reconciliation (inputs to V8) | commercial_website_mobile_V7.html / User / Base for website mobile V8 / 7001283bb524d203… | FR-V12-V-001 |
| 48 | VS-002529 | 01_Specification_Contr | Source reconciliation (inputs to V8) | commercial_admin_desktop_V7.html / User / Base for Admin desktop V8 / a5cd10f964b75b7c… | FR-V12-V-001 |
| 49 | VS-002530 | 01_Specification_Contr | Source reconciliation (inputs to V8) | commercial_admin_mobile_V7.html / User / Base for Admin mobile V8 / 85179014b82161a1… | FR-V12-V-001 |
| 50 | VS-002532 | 01_Specification_Contr | Source reconciliation (inputs to V8) | Sales_Marketing_Automation_FSD_V7.docx (functional) / Claude / Source of AIX/CJ-R, appendices A–D, registers, tests / 6e7e68ccfed4a206… | FR-V12-V-001 |
| 51 | VS-002533 | 01_Specification_Contr | Source reconciliation (inputs to V8) | commercial_website_V7.html (functional) / Claude / Source of website functional layer / 0fd2e7f1a9cbeb10… | FR-V12-V-001 |
| 52 | VS-002534 | 01_Specification_Contr | Source reconciliation (inputs to V8) | commercial_admin_V7.html (functional) / Claude / Source of Admin functional layer / 2a5e141ead128326… | FR-V12-V-001 |
| 53 | VS-002536 | 01_Specification_Contr | RCTCFE stage-gate register (V8 cycle) | 1 Gap analysis / Six user V7 files + four Claude V7 files / Delta found: two divergent V7 lines; mobile docs lacked AI/compliance; functional docs la… | FR-V12-V-001 |
| 54 | VS-002537 | 01_Specification_Contr | RCTCFE stage-gate register (V8 cycle) | 2 BRD/FSD upgrade / Responsive BRD/FSD V7 / AI, compliance, appendices, registers integrated once; MOB scope aligned to 36/143 / Pass | FR-V12-V-001 |
| 55 | VS-002539 | 01_Specification_Contr | RCTCFE stage-gate register (V8 cycle) | 4 Cross-artifact alignment / Six V8 artifacts / IDs, counts and SHA-256 synchronised; services ≠ flows confirmed / Pass | FR-V12-V-001 |
| 56 | VS-002540 | 01_Specification_Contr | RCTCFE stage-gate register (V8 cycle) | 5 RCTCFE evaluation / V8 builds / 71 browser checks, axe audit, DB and contract validation; scoring in ch34 / Pass | FR-V12-V-001 |
| 57 | VS-002542 | 01_Specification_Contr | RCTCFE stage-gate register (V8 cycle) | 7 Optimization register / 135 OPT / Status recorded for all 135 (ch34); none double-counted / Pass | FR-V12-V-001 |
| 58 | VS-002543 | 01_Specification_Contr | RCTCFE stage-gate register (V8 cycle) | 8 Defect resolution / D1–D15 / D14 skip link and D15 FX decimals fixed in V8; D12 partial by design / Pass with recorded exception | FR-V12-V-001 |
| 59 | VS-002545 | 01_Specification_Contr | RCTCFE stage-gate register (V8 cycle) | 10 Architecture/redundancy audit / 40 MT + 18 MOB + 40 V7 / One requirement per behaviour; duplicates linked not re-numbered / Pass | FR-V12-V-001 |
| 60 | VS-002546 | 01_Specification_Contr | RCTCFE stage-gate register (V8 cycle) | 11 Universal implementation / Six artifacts / Synchronised V8 delivered; production gate open / Pass (prototype/document) | FR-V12-V-001 |
| 61 | VS-002547 | 01_Specification_Contr | V8 / Change control, verified inventory and art… | D1 / Version labels / HTML titles and banners showed V5/V6. / All four artifacts labelled V8.0; SHA-256 of delivered HTML recorded in BRD and FSD. | FR-V12-V-001 |
| 62 | VS-002558 | 01_Specification_Contr | V8 / Change control, verified inventory and art… | D12 / Layered prototype code / v4/v5/v6 function layers. / Still partial by design: prototypes keep traceable layers (V3–V8); one implementation per… | FR-V12-V-006 |
| 63 | VS-002562 | 01_Specification_Contr | V8 / Change control, verified inventory and art… | M1 / Two V7 lines / The responsive V7 set (6 files, 18 MOB requirements) and the functional V7 set (4 files, AI + compliance) diverged from V6. / Mer… | FR-V12-V-001 |
| 64 | VS-002564 | 01_Specification_Contr | V8 / Change control, verified inventory and art… | D15 / FX rate entry (new) / Rate inputs used integer stepping, so realistic rates below 1 (e.g. INR→USD 0.012) failed browser validation and could no… | FR-V12-V-005 |
| 65 | VS-002593 | 01_Specification_Contr | V5 optimization requirements and controls | SM-V5-PLANNING remains a non-identity worksheet. | FR-V12-V-002 |
| 66 | VS-003634 | 12_Executable_Workflow | SM-SVC-01-WF01 — Market and demand monitoring | Cost source / Illustrative internal INR 1.51/invocation; excludes provider/retry/labor and other fees. | FR-V12-V-003 |
| 67 | VS-003689 | 12_Executable_Workflow | SM-SVC-01-WF03 — Trend report and evidence refr… | Cost source / Illustrative internal INR 1.37/invocation; excludes provider/retry/labor and other fees. | FR-V12-V-003 |
| 68 | VS-003773 | 12_Executable_Workflow | SM-SVC-02-WF02 — Supplier, distributor and part… | Cost source / Illustrative internal INR 1.25/invocation; excludes provider/retry/labor and other fees. | FR-V12-V-003 |
| 69 | VS-003801 | 12_Executable_Workflow | SM-SVC-02-WF03 — Opportunity monitoring and ale… | Cost source / Illustrative internal INR 0.67/invocation; excludes provider/retry/labor and other fees. | FR-V12-V-003 |
| 70 | VS-004541 | 12_Executable_Workflow | SM-SVC-09-WF01 — Unified conversation capture | Cost source / Illustrative internal INR 0.71/invocation; excludes provider/retry/labor and other fees. | FR-V12-V-003 |
| 71 | VS-004819 | 12_Executable_Workflow | SM-SVC-11-WF03 — Content review and optimization | Cost source / Illustrative internal INR 1.19/invocation; excludes provider/retry/labor and other fees. | FR-V12-V-003 |
| 72 | VS-005700 | 12_Executable_Workflow | SM-SVC-19-WF02 — Bid/no-bid assessment | Cost source / Illustrative internal INR 1.25/invocation; excludes provider/retry/labor and other fees. | FR-V12-V-003 |
| 73 | VS-009760 | 24_UI_UX_Components_Sc | A003 — Growth workspace navigation | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 74 | VS-009776 | 24_UI_UX_Components_Sc | A005 — Product knowledge catalog | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 75 | VS-009784 | 24_UI_UX_Components_Sc | A006 — Knowledge documents and approval | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 76 | VS-009800 | 24_UI_UX_Components_Sc | A008 — Integration connections | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 77 | VS-009816 | 24_UI_UX_Components_Sc | A010 — Source permissions and registry | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 78 | VS-009824 | 24_UI_UX_Components_Sc | A011 — AI configuration and evaluation | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 79 | VS-009840 | 24_UI_UX_Components_Sc | A013 — Privacy request queue | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 80 | VS-009848 | 24_UI_UX_Components_Sc | A014 — System health and incidents | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 81 | VS-009856 | 24_UI_UX_Components_Sc | A015 — Research planner | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 82 | VS-009864 | 24_UI_UX_Components_Sc | A016 — Market discovery results | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 83 | VS-009872 | 24_UI_UX_Components_Sc | A017 — Evidence detail panel | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 84 | VS-009880 | 24_UI_UX_Components_Sc | A018 — Organization directory | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 85 | VS-009888 | 24_UI_UX_Components_Sc | A019 — Buying signals board | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 86 | VS-009896 | 24_UI_UX_Components_Sc | A020 — Business need review | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 87 | VS-009904 | 24_UI_UX_Components_Sc | A021 — Product solution matching | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 88 | VS-009912 | 24_UI_UX_Components_Sc | A022 — Opportunity shortlist and scoring | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 89 | VS-009920 | 24_UI_UX_Components_Sc | A023 — Research rules and scoring settings | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 90 | VS-009928 | 24_UI_UX_Components_Sc | A024 — Decision-maker and contact discovery | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 91 | VS-009936 | 24_UI_UX_Components_Sc | A025 — Contact verification queue | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 92 | VS-009944 | 24_UI_UX_Components_Sc | A026 — Contact quality and role mapping | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 93 | VS-009952 | 24_UI_UX_Components_Sc | A027 — Qualified opportunity review | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 94 | VS-009960 | 24_UI_UX_Components_Sc | A028 — Research approval and alert rules | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 95 | VS-009976 | 24_UI_UX_Components_Sc | A030 — Sales pipeline and assignment rules | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 96 | VS-009984 | 24_UI_UX_Components_Sc | A031 — Lead form and routing configuration | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 97 | VS-010016 | 24_UI_UX_Components_Sc | A035 — Message templates and approval queue | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 98 | VS-010024 | 24_UI_UX_Components_Sc | A036 — Email channel configuration | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 99 | VS-010040 | 24_UI_UX_Components_Sc | A038 — Follow-up sequences and tasks | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 100 | VS-010048 | 24_UI_UX_Components_Sc | A039 — Follow-up policies | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 101 | VS-010056 | 24_UI_UX_Components_Sc | A040 — Meeting calendar and agenda | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 102 | VS-010064 | 24_UI_UX_Components_Sc | A041 — Calendar configuration | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 103 | VS-010080 | 24_UI_UX_Components_Sc | A043 — Management dashboard | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 104 | VS-010088 | 24_UI_UX_Components_Sc | A044 — WhatsApp channel and templates | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 105 | VS-010096 | 24_UI_UX_Components_Sc | A045 — WhatsApp conversations | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 106 | VS-010104 | 24_UI_UX_Components_Sc | A046 — Chat FAQ and omnichannel routing | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 107 | VS-010112 | 24_UI_UX_Components_Sc | A047 — Compliance incident dashboard | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 108 | VS-010120 | 24_UI_UX_Components_Sc | A048 — Social listening feed | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 109 | VS-010128 | 24_UI_UX_Components_Sc | A049 — Social source permissions | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 110 | VS-010136 | 24_UI_UX_Components_Sc | A050 — Content studio | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 111 | VS-010144 | 24_UI_UX_Components_Sc | A051 — Content and claims approval | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 112 | VS-010152 | 24_UI_UX_Components_Sc | A052 — Social publishing calendar | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 113 | VS-010160 | 24_UI_UX_Components_Sc | A053 — Social account and publishing controls | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 114 | VS-010168 | 24_UI_UX_Components_Sc | A054 — SEO and visibility dashboard | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 115 | VS-010176 | 24_UI_UX_Components_Sc | A055 — SEO review backlog | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 116 | VS-010184 | 24_UI_UX_Components_Sc | A056 — Landing page builder | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 117 | VS-010192 | 24_UI_UX_Components_Sc | A057 — Landing page approvals | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 118 | VS-010200 | 24_UI_UX_Components_Sc | A058 — Campaign builder and audience | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 119 | VS-010208 | 24_UI_UX_Components_Sc | A059 — Campaign approval and budgets | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 120 | VS-010216 | 24_UI_UX_Components_Sc | A060 — Paid advertising dashboard | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 121 | VS-010224 | 24_UI_UX_Components_Sc | A061 — Advertising spend controls | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 122 | VS-010232 | 24_UI_UX_Components_Sc | A062 — Webinar and demo event manager | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 123 | VS-010240 | 24_UI_UX_Components_Sc | A063 — Event and reminder settings | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 124 | VS-010248 | 24_UI_UX_Components_Sc | A064 — Referral and partner approvals | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 125 | VS-010256 | 24_UI_UX_Components_Sc | A065 — Proposal builder and preview | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 126 | VS-010264 | 24_UI_UX_Components_Sc | A066 — Proposal approval queue | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 127 | VS-010280 | 24_UI_UX_Components_Sc | A068 — Price and discount approval | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 128 | VS-010288 | 24_UI_UX_Components_Sc | A069 — Negotiation and objections | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 129 | VS-010296 | 24_UI_UX_Components_Sc | A070 — Negotiation exception queue | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 130 | VS-010304 | 24_UI_UX_Components_Sc | A071 — Contracts and MoUs | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 131 | VS-010312 | 24_UI_UX_Components_Sc | A072 — Contract and legal approvals | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 132 | VS-010320 | 24_UI_UX_Components_Sc | A073 — Payment and deal closure | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 133 | VS-010328 | 24_UI_UX_Components_Sc | A074 — Payment reconciliation | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 134 | VS-010336 | 24_UI_UX_Components_Sc | A075 — Customer onboarding checklist | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 135 | VS-010344 | 24_UI_UX_Components_Sc | A076 — Onboarding assignment | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 136 | VS-010352 | 24_UI_UX_Components_Sc | A077 — Partner deployment pipeline | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 137 | VS-010360 | 24_UI_UX_Components_Sc | A078 — Deployment readiness approval | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 138 | VS-010368 | 24_UI_UX_Components_Sc | A079 — Renewal and retention calendar | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 139 | VS-010376 | 24_UI_UX_Components_Sc | A080 — Renewal policies | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 140 | VS-010384 | 24_UI_UX_Components_Sc | A081 — Lost deal and feedback | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 141 | VS-010392 | 24_UI_UX_Components_Sc | A082 — Revenue and attribution dashboard | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 142 | VS-010400 | 24_UI_UX_Components_Sc | A083 — Revenue reconciliation and KPI settings | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 143 | VS-010408 | 24_UI_UX_Components_Sc | A084 — AI quality and feedback review | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 144 | VS-010416 | 24_UI_UX_Components_Sc | A085 — Competitor and market watch | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 145 | VS-010424 | 24_UI_UX_Components_Sc | A086 — Competitor source review | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 146 | VS-010432 | 24_UI_UX_Components_Sc | A087 — Sales forecasting dashboard | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 147 | VS-010440 | 24_UI_UX_Components_Sc | A088 — Forecast model settings | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 148 | VS-010464 | 24_UI_UX_Components_Sc | A091 — Insurance institutional pilot | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 149 | VS-010472 | 24_UI_UX_Components_Sc | A092 — Insurance pilot approval | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 150 | VS-010480 | 24_UI_UX_Components_Sc | A093 — Technology licensing enquiries | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 151 | VS-010488 | 24_UI_UX_Components_Sc | A094 — Licensing and API scope approval | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 152 | VS-010496 | 24_UI_UX_Components_Sc | A095 — Phygital expansion tracker | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 153 | VS-010504 | 24_UI_UX_Components_Sc | A096 — Phygital readiness approval | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 154 | VS-010512 | 24_UI_UX_Components_Sc | A097 — Future product catalog view | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 155 | VS-010520 | 24_UI_UX_Components_Sc | A098 — Future product launch approval | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 156 | VS-010528 | 24_UI_UX_Components_Sc | A099 — Tenant, startup and membership administr… | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 157 | VS-010536 | 24_UI_UX_Components_Sc | A100 — Business profile templates and branding | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 158 | VS-010552 | 24_UI_UX_Components_Sc | A102 — Autonomous commercial planner and simula… | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 159 | VS-010568 | 24_UI_UX_Components_Sc | A104 — Global project bid and tender desk | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 160 | VS-010592 | 24_UI_UX_Components_Sc | A107 — Website configuration and content manage… | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 161 | VS-010624 | 24_UI_UX_Components_Sc | A111 — Automation Coordination & Conflict Resol… | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 162 | VS-010632 | 24_UI_UX_Components_Sc | A112 — Business Configuration Change Centre | V2 rule / Resolve audience and object permissions; public tenant publication prohibited; source mappings not approved. Form validation, empty/loading… | FR-V12-V-007; TC-V12-V-019…026; US-01-Z… |
| 163 | VS-011114 | 26_PostgreSQL_Database | V5 optimization requirements and controls | DB-V2-SUBSCRIPTION / scope; quote_version; state; start/end; plan_version; entitlement refs; version | FR-V12-V-002 |
| 164 | VS-011115 | 26_PostgreSQL_Database | V5 optimization requirements and controls | DB-V2-CONFIG / scope; schema_version; revision; typed settings; approver_ref; active flag; unique active version per company | FR-V12-V-002 |

### 11.23.3.2 Superseded by a Founder decision (every statement)

| # | Statement ID | Chapter | Statement (V12) | Superseded by | Current rule |
|---|---|---|---|---|---|
| 1 | VS-000037 | 01_Executive_Summary_P | C3 / Document contradiction / Chapter 01 called recovery objectives “proposed … pending verification of authorization evidence” while KPI t… | DEC-771; DEC-787 | Recovery-objective approval contradiction resolved by Founder decisions RTO <= 120 min and RPO <= 15 min |
| 2 | VS-000115 | 01_Executive_Summary_P | Investment_Automation_RCTCFE_Master_Prompt.docx / User / Evaluation method, applied to the Commercial product (no Investment scope copied)… | DEC-783 | Lineage row restored in FR-V12-V-001; its note "no Investment scope copied" is superseded by DEC-783 |
| 3 | VS-002457 | 01_Specification_Contr | C3 / Document contradiction / Chapter 01 called recovery objectives “proposed … pending verification of authorization evidence” while KPI t… | DEC-771; DEC-787 | Recovery-objective approval contradiction resolved by Founder decisions RTO <= 120 min and RPO <= 15 min |
| 4 | VS-002535 | 01_Specification_Contr | Investment_Automation_RCTCFE_Master_Prompt.docx / User / Evaluation method, applied to the Commercial product (no Investment scope copied)… | DEC-783 | Lineage row restored in FR-V12-V-001; its note "no Investment scope copied" is superseded by DEC-783 |
| 5 | VS-011804 | 28_Open_Source_Paid_Pl | VND-86 / Bio Research / Defer unless commercial evidence need approved / Public market / investor search — No investment or confidential fu… | DEC-783 | V12 vendor note "no investment or confidential fundraising use" superseded: Investment Automation adopted (Parts 11.16a-e) |
| 6 | VS-011813 | 28_Open_Source_Paid_Pl | VND-95 / Equity Research / Defer unless commercial evidence need approved / Public market / investor search — No investment or confidential… | DEC-783 | V12 vendor note "no investment or confidential fundraising use" superseded: Investment Automation adopted (Parts 11.16a-e) |

The two overlay rows (VND-86, VND-95) matched the blueprint lexically (Part 11.8 plugin register) but carry the pre-DEC-783 position. All other V12 positions that differ from earlier blueprint text were adopted by DEC-770…791, so the earlier **blueprint** text is what is superseded; those cases are handled as baseline amendments (Part 11.23b) and errata (Part 11.23c), not here.

### 11.23.3.3 Covered in different words (grouped by rule; every row cited in `V_audit.csv`)

| Group (rule) | Statements | Why the weak score | Where covered (examples; every row cited in `V_audit.csv`) |
|---|---|---|---|
| FSD 40 source disposition candidates — Test | 167 | Source-pack object SM-UT-001 present; the V12 disposition text is a review instruction, executed by Parts 11.11a/11.12 | Part 6.8a §6.8.1 Documents reviewed (L26); Part 11.12 §11.12 residual register R-TEST (di…; Part 6.8b §6.8.4.3 SM-UT alias realignment (supersedes the inferred family labels (L87);… |
| FSD 40 source disposition candidates — API | 155 | Source-pack object /auth/login present; the V12 disposition text is a review instruction, executed by Parts 11.11a/11.12 | Part 3.5a §3.5.4.3 Full operation mapping: source operation → blueprint operation (L280);…; Part 3.5a §3.5.4.3 Full operation mapping: source operation → blueprint operation (L281);… |
| FSD 40 source disposition candidates — Entity | 155 | Source-pack object existing present; the V12 disposition text is a review instruction, executed by Parts 11.11a/11.12 | Part 3.5a §3.5.1.3 Per-operation field semantics (columns of the source register) (L74);…; Part 3.5a §3.5.1.3 Per-operation field semantics (columns of the source register) (L74);… |
| Appendix C/C2 DDL (RLS policy) | 116 | tenant RLS policy (USING and WITH CHECK on app.tenant_id) for identity_provider; reproduced in Part 11.9a/11.9b (tests DB-T1…T9, C2-T1…T11… | Part 11.19a §11.19.4.3 Appendix A2 and C2 objects used by this part (L399); Part 11.9b §1…; Part 11.19a §11.19.4.3 Appendix A2 and C2 objects used by this part (L399); Part 11.9b §1… |
| FSD 40 source disposition candidates — Task | 96 | Source-pack object TASK-W02 present; the V12 disposition text is a review instruction, executed by Parts 11.11a/11.12 | Part 6.9a §6.9.4.5 Work items (162) → stories (L572); Part 11.12 §11.12 residual register…; Part 6.9a §6.9.4.5 Work items (162) → stories (L574); Part 11.12 §11.12 residual register… |
| Manual decisions (read in context) | 86 | Part 11.12 treats the historical annex as non-normative; semantic mappings approved there | Part 11.0 §11.0.1 What the revision is (L13); Part 11.0 §11.0.1 What the revision is (L13) |
| FSD 40 source disposition candidates — QC | 55 | Source-pack object QC-043 present; the V12 disposition text is a review instruction, executed by Parts 11.11a/11.12 | Part 6.9b §6.9.5.1.8 QC register (245 checks) (L250); Part 11.12 §11.12 residual register…; Part 6.9b §6.9.5.1.8 QC register (245 checks) (L252); Part 11.12 §11.12 residual register… |
| ID-bearing rows (status/evidence wording only) | 25 | ID present; residual words are status/evidence metadata (e.g. "Production pending", "PASS") | Part 11.10c §11.10.5.5 Prototype-parity regression classes TC-V12-J-101…114 (L360) (A001); Part 11.1a §11.1.3.01 Chapter 01: Executive Summary Product Vision (L193) (SM-APPLICATION… |
| Appendix C/C2 DDL (table) | 22 | table definition for webhook_endpoint; reproduced in Part 11.9a/11.9b (tests DB-T1…T9, C2-T1…T11 re-run 20/20) | Part 11.16c §11.16.15.18 Data entities, ER views and RLS (L4650); Part 11.9b §11.9b DDL w…; Part 11.19a §11.19.0 How to read this part (L22); Part 11.9b §11.9b DDL with RLS (Appendi… |
| A113 template rows X26–X39 | 14 | A113 template X26: input/output refs present in Part 11.4a DTO registry; screen via A113 contract | Part 11.18a §11.18.1 Material reviewed (L34); Part 11.3c §SM-SVC-11 Content Marketing Automation (L46) |
| Threshold located in another line of the same section | 12 | Threshold present in a different line of the same section | Part 11.1a L167 (11.1.3.01 Chapter 01: Executive Summary Product Vision) (threshold locat…; Part 11.10a L636 (11.10.3.8 Prose rules of chapters 33, 34 and 35) (threshold located by… |
| Customer decision rows (CDEC) | 7 | Customer decision row; status text only | Part 11.11a §11.11.4.3 Customer decision register (CDEC) against DEC-001…422 (L554) (cust…; Part 11.11a §11.11.4.3 Customer decision register (CDEC) against DEC-001…422 (L562) (cust… |

**Notes on the large groups.**

- **FSD 40 source disposition candidates (628 triaged rows).** Each row names an archived source-pack object (API operation, entity, QC, task or test) and a review instruction ("verify DTO and scope", "map to current gate", "retain predecessor/estimate; not approved"). Every one of the named objects is present in the blueprint (checked per row); the instructions are executed by Part 11.12 (residual registers R-API, R-DB, R-QC, R-TASK, R-TEST) and Part 11.11a §11.11.4.5. The weak lexical score comes from the instruction wording, which is not requirement text.
- **Appendix C/C2 DDL (138 triaged statements).** Every table and policy name is present; Part 11.9a reproduced the customer DDL and re-ran DB-T1…T9 and C2-T1…T11 (20/20), and Part 11.9b carries the corrected RLS DDL. The weak score is the repeated policy boilerplate.
- **ID-bearing rows.** Requirement-status rows (for example `AIX-04 | P0 | Prompt registry | … | Production pending`) whose IDs are present; the residual words are status and evidence metadata.

### 11.23.3.4 Manual decisions (each read in context)

| # | Statement (first occurrence) | Chapter | Class | Citation / authority | Reading note |
|---|---|---|---|---|---|
| 1 | Historical annex is non-normative; unresolved decisions and semantic mappings require explicit approval. | 00_Reading_guide_and_cha | C | Part 11.0 §11.0.1 What the revision is (L13) | Part 11.12 treats the historical annex as non-normative; semantic mappings approved there |
| 2 | C2 / Demonstration gap / All 60 seeded runs lacked recipient evidence, so no seeded run could complete and wi… | 01_Executive_Summary_Pro | C | Part 11.10a §11.10.3.8 Prose rules of chapters 33, 34 and 35 (L623) | Prototype demonstration gap; production seeds and negative cases in Part 11.10a §11.10.3.10 |
| 3 | C3 / Document contradiction / Chapter 01 called recovery objectives “proposed … pending verification of autho… | 01_Executive_Summary_Pro | S | DEC-771; DEC-787 | Recovery-objective approval contradiction resolved by Founder decisions RTO <= 120 min and RPO <= 15 min |
| 4 | C5 / Evidence breadth / V10 recorded 34 targeted checks and no accessibility result. / 77/77 independent brow… | 01_Executive_Summary_Pro | C | Part 11.10a §11.10.3.7 Scorecards, weights and gates (RCTCFE, artifact scores,… | Prototype evidence breadth; Part 11.10a §11.10.3.10 prototype verification evidence |
| 5 | C8 / Stale label / Website browser-tab title still showed “V9”. / Corrected to V11 on both website builds. | 01_Executive_Summary_Pro | N | FR-V12-V-001 | Version-label defect recorded in the artifact lineage register |
| 6 | D1 / Version labels / HTML titles and banners showed V5/V6. / All four artifacts labelled V8.0; SHA-256 of de… | 01_Executive_Summary_Pro | N | FR-V12-V-001 | Version labels and SHA-256 of delivered HTML: artifact integrity register |
| 7 | D2 / FSD DTO types / 290 DTO fields typed “string / configured enum”; 65 of them were really free text, dates… | 01_Executive_Summary_Pro | C | Part 11.4b §11.4.5.4 DTO schema registry and BusinessContext (DEC-565, ADR-198,… | DTO typing corrections adopted in Part 11.4b DTO registry (156 schemas) |
| 8 | D3 / Traceability chain / Foundations and agents had no IDs in the documents. / Foundation register (SM-xx-yy… | 01_Executive_Summary_Pro | C | Part 11.10b §11.10.4.2 Workflow test catalogue (156 workflows) (L92) | Foundation register, AGT registry and 156-row traceability register in Parts 11.6a/11.11a |
| 9 | D7 / Navigation / No Word TOC field or ID index. / TOC field (levels 1–2) and ID index appendix. | 01_Executive_Summary_Pro | C | Part 11.11b §11.11.5.15 ID-family register — FR-V12-K-026 (L368) | Blueprint ID index: final/id_registry.csv and Part 9.2 registers |
| 10 | D12 / Layered prototype code / v4/v5/v6 function layers. / Still partial by design: prototypes keep traceable… | 01_Executive_Summary_Pro | N | FR-V12-V-006 | Production rule "one implementation per behaviour" not stated in coding standards |
| 11 | M1 / Two V7 lines / The responsive V7 set (6 files, 18 MOB requirements) and the functional V7 set (4 files,… | 01_Executive_Summary_Pro | N | FR-V12-V-001 | Merge lineage of the two V7 lines into V8 recorded in the lineage register |
| 12 | D15 / FX rate entry (new) / Rate inputs used integer stepping, so realistic rates below 1 (e.g. INR→USD 0.012… | 01_Executive_Summary_Pro | N | FR-V12-V-005 | FX rate input must accept decimals below 1; UI validation rule not specified |
| 13 | A11Y / Colour contrast and link affordance (new) / axe-core found muted text at 4.34:1 and colour-only inline… | 01_Executive_Summary_Pro | C | Part 11.7b §11.7.5.10 Accessibility contract (WCAG 2.2 AA; target, not certific… | Contrast tokens adopted in Part 11.7b accessibility contract |
| 14 | EVD / Evidence and registers / No single status view of all requirements; RCTCFE stage records missing. / Sta… | 01_Executive_Summary_Pro | C | Part 11.10a §11.10.1.1 Files, sizes, purpose and pattern (L27) | Requirement status register and evidence scoring: Part 11.10a scorecards |
| 15 | Dynamic detail views / 517 source-derived step contracts; manual walkthrough and state-derived simulated trac… | 01_Executive_Summary_Pro | C | Part 11.0 §Application Blueprint: PART 11 (Batch 11.0), Customer Revision V12:… | 517 step contracts: Part 11.10b/11.10c step tests |
| 16 | ICP: industry, geography, language, business size, sales motion, target personas, volume, data readiness, reg… | 04_Stakeholders_Personas | N | FR-V12-V-004 | ICP attribute set (MT-04) only partly specified (A-07-0339 partial) |
| 17 | Subscriber / Research → lead → qualification → engagement → opportunity → proposal → order → fulfillment → ve… | 05_SaaS_Business_Commerc | C | Part 11.10a §11.10.3.5 Release scenarios, UAT-E2E-01, exceptions and reconcilia… | Subscriber value chain to verified receipt: Parts 1/2.2 |
| 18 | Data ownership / Tenant owns supplied business data and authorized outputs subject to agreement; operator ret… | 05_SaaS_Business_Commerc | C | Part 11.1a §11.1.3.05 Chapter 05: SaaS Business Commercial Operating Mode (L273) | Data ownership: BR-V12-04 (Part 11.1a) and offboarding with legal hold (Part 11.5a/b) |
| 19 | Operator and subscriber metrics, receivables, CRM, support, orders and invoices must be separate. | 06_Multi_Tenant_Multi_Co | C | Part 11.7a §11.7.4.5 Access experiences (DEC-624) (L1830) | Operator ledger separate from subscriber data: Part 11.7b A187/A188 and Part 11.5a tenant lifecycle |
| 20 | Applicable customer / sector / Digital acquisition and commerce businesses | 08_Master_Automation_Ser | C | Part 11.2c §11.2.5.40 SM-SVC-30 Conversion Rate Optimization & Intelligent Expe… | Service sector: Part 11.2c |
| 21 | Applicable customer / sector / Retail, wholesale, D2C, manufacturers | 08_Master_Automation_Ser | C | Part 11.2c §11.2.5.41 SM-SVC-31 Marketplace & E-commerce Channel Operations Aut… | Service sector: Part 11.2c |
| 22 | Replace / Equivalent core automation can be owned by the platform. / Implement reusable native/OSS adapter; b… | 11_Pricing_Billing_Comme | C | ?Defer / exclude | Plugin economics classes: Part 11.8a/b plugin register |
| 23 | Conditional external service / Proprietary data, communication, payment, verification or other entitlement ma… | 11_Pricing_Billing_Comme | C | ?Defer / exclude | Plugin economics classes: Part 11.8a/b plugin register |
| 24 | Defer / exclude / Not required for the product or no verified runtime requirement. / No installation, subscri… | 11_Pricing_Billing_Comme | C | ?Defer / exclude | Plugin economics classes: Part 11.8a/b plugin register |
| 25 | Real support, value reports, renewal, data portability and billing disputes require approved production polic… | 17_Customer_Success_Rete | C | Part 11.10a §11.10.3.4 V12 acceptance register: V5 optimization requirements (1… | Billing disputes, value reports, renewal and portability policies: OPT CS-14/CS-15, Part 11.10a/c and Part 11… |
| 26 | Exit / Export permitted data in structured formats; revoke integrations and secrets; delete subject to lawful… | 21_SLA_Support_Service_D | C | Part 11.5b §11.5.5.15 Test cases (TC-V12-E) (L807) | Exit: export, revoke, delete subject to legal hold: Part 11.5a/b TC-V12-E-061 |
| 27 | BRD V12 / 8.6 | 24_Business_Acceptance_R | C | Part 11.10a §11.10.3.7 Scorecards, weights and gates (RCTCFE, artifact scores,… | V12 readiness score recorded in Part 11.10a scorecards |
| 28 | Done / 3 | 24_Business_Acceptance_R | C | Part 11.10a §11.10.1.1 Files, sizes, purpose and pattern (L29) | Reconciliation inventory counts: Parts 11.10a/11.12 |
| 29 | API / 321 | 24_Business_Acceptance_R | C | Part 11.11a §11.11.1.3 Aspect inventory (L42) | API disposition count 321: Part 11.12 |
| 30 | Test / 1029 | 24_Business_Acceptance_R | C | Part 11.10a §11.10.1.1 Files, sizes, purpose and pattern (L29) | Test disposition count 1,029: Part 11.10a |
| 31 | QC / 245 | 24_Business_Acceptance_R | C | Part 11.0 §11.0.2 Coverage by review group (L27) | QC disposition count 245: Part 11.12 |
| 32 | The following responsibility categories are proposed; individual assignees and dates require the actual devel… | 25_Decision_Register_Mig | C | Part 11.1a §11.1.3.25 Chapter 25: Decision Register Migration Source Appe (L866) | Responsibility categories: RACI in Parts 0/8.1 |
| 33 | 1 Gap analysis / Six user V7 files + four Claude V7 files / Delta found: two divergent V7 lines; mobile docs… | 01_Specification_Control | N | FR-V12-V-001 | RCTCFE V8 stage-gate register restored |
| 34 | 2 BRD/FSD upgrade / Responsive BRD/FSD V7 / AI, compliance, appendices, registers integrated once; MOB scope… | 01_Specification_Control | N | FR-V12-V-001 | RCTCFE V8 stage-gate register restored |
| 35 | 4 Cross-artifact alignment / Six V8 artifacts / IDs, counts and SHA-256 synchronised; services ≠ flows confir… | 01_Specification_Control | N | FR-V12-V-001 | RCTCFE V8 stage-gate register restored |
| 36 | 5 RCTCFE evaluation / V8 builds / 71 browser checks, axe audit, DB and contract validation; scoring in ch34 /… | 01_Specification_Control | N | FR-V12-V-001 | RCTCFE V8 stage-gate register restored |
| 37 | 7 Optimization register / 135 OPT / Status recorded for all 135 (ch34); none double-counted / Pass | 01_Specification_Control | N | FR-V12-V-001 | RCTCFE V8 stage-gate register restored |
| 38 | 8 Defect resolution / D1–D15 / D14 skip link and D15 FX decimals fixed in V8; D12 partial by design / Pass wi… | 01_Specification_Control | N | FR-V12-V-001 | RCTCFE V8 stage-gate register restored |
| 39 | 10 Architecture/redundancy audit / 40 MT + 18 MOB + 40 V7 / One requirement per behaviour; duplicates linked… | 01_Specification_Control | N | FR-V12-V-001 | RCTCFE V8 stage-gate register restored |
| 40 | 11 Universal implementation / Six artifacts / Synchronised V8 delivered; production gate open / Pass (prototy… | 01_Specification_Control | N | FR-V12-V-001 | RCTCFE V8 stage-gate register restored |
| 41 | 34 W routes / 135 Admin screens (113 A + 14 X + 8 O) / V3 prototype inventory; 113 A is historical baseline;… | 01_Specification_Control | C | Part 11.7a §Register PAD: Prototype admin datasets (117 aspects) (L1351) | Route and screen counts: Part 11.7a |
| 42 | Policy / Policy & jurisdiction engine (in-process library + cache) / Entitlement, consent, budget, CJ preflig… | 02_System_Context_Soluti | C | Part 11.10a §11.10.3.2 V12 acceptance register: multi-tenant architecture (MT-0… | Policy engine in-process, fail closed: Part 11.19b / Part 3.1 PDP |
| 43 | Modular monolith for core transaction integrity plus worker processes; extracted services only when measured… | 03_High_Level_Design | C | Part 11.1a §11.1.3.06 Chapter 06: Multi Tenant Multi Company Business Arc (L286) | Modular monolith: Part 3.1 |
| 44 | Transaction boundary: domain record + outbox in one commit; external effects cannot be atomic with DB, so per… | 04_Detailed_Component_De | C | Part 11.10a §11.10.3.9 Coding and review controls (chapter 35, V10, source D25… | Transactional outbox and reconciliation: Part 3.1 |
| 45 | Authorization matrix: Anonymous: neutral catalog only; verified customer identity: own tenant memberships; te… | 06_Identity_Roles_Author | C | Part 11.10a §11.10.3.10 Prototype verification evidence (V3–V12) (L696) | Authorization matrix: roles R01–R20 and ABAC (Part 2.3), custom roles (Part 11.19a) |
| 46 | Failed step held, compensate only newly created resources; never delete pre-existing data. | 07_Tenant_Provisioning_B | C | Part 11.5a §C. Provisioning saga PS-01…PS-08 (FR-V12-E-038) (L633) | Provisioning saga compensation: Part 11.5a |
| 47 | Only group names/counts are recoverable here; the original 100 entries and 20 named industry templates are no… | 12_Executable_Workflow_S | C | Part 11.11a §11.11.4.4 Reconciliation actions REC-01…30 (V11) (L605) | Historical use-case groups: REC-08 in Parts 11.3a/11.11a |
| 48 | V4 adds input controls derived from required-input descriptions, sample budget, authority mode and scheduling… | 12_Executable_Workflow_S | C | Part 11.10a §11.10.1.1 Files, sizes, purpose and pattern (L27) | Prototype workflow guard: Part 11.3a |
| 49 | Role separation / Requester creates run; reviewer can inspect and approve eligible awaiting-approval payload;… | 12_Executable_Workflow_S | C | Part 11.10a §11.10.3.10 Prototype verification evidence (V3–V12) (L691) | Role separation: BRL-APR, Part 2.3 |
| 50 | Scope / Check current company entitlement and pause. Portfolio gets aggregates only. Company capability demo… | 12_Executable_Workflow_S | C | Part 11.10a §11.10.3.4 V12 acceptance register: V5 optimization requirements (1… | Portfolio aggregates only; capability checks: Part 11.5a |
| 51 | Duplicate / failures / Explicit duplicate scenario or repeated reference+workflow+channel yields held status.… | 12_Executable_Workflow_S | C | Part 11.10c §11.10.5.2 Workflow scenario classes TC-V12-J-001…010 and approval-… | Duplicate and failure holds: workflow scenario classes DUP/BUDGET/RECOVERY (Part 11.10c) |
| 52 | The architecture separates reader steps (may see untrusted content, have no effect tools) from actor steps (m… | 16_AI_Models_Prompts_Eva | C | Part 11.10a §11.10.3.1 V12 acceptance register: AI execution controls (AIX-01…2… | Reader/actor separation: AIX-09 in Parts 11.10a/11.13a |
| 53 | Matching local configuration has status and illustrative cumulative cap; inherited per-company quotas remain. | 19_Automation_Scheduler_ | C | Part 11.10a §11.10.3.2 V12 acceptance register: multi-tenant architecture (MT-0… | Scoped budgets: MT-30 in Part 11.5a |
| 54 | All new configuration inputs are fictional and stored in browser memory only. | 20_Public_SaaS_Website_S | C | Part 11.9a §11.9.3.1 Requirement, test, entity, analytics, security and enginee… | Prototype-only browser memory; production stores configuration revisions server-side (Part 11.9a/b) |
| 55 | Demo identity (Admin) / Separate “Demo user” selector; runs record requested_by; reviewer must be a different… | 24_UI_UX_Components_Scre | C | Part 11.10a §11.10.3.10 Prototype verification evidence (V3–V12) (L691) | Demo identity -> production SoD rule (BRL-APR) |
| 56 | Source route / data mapping / GET /api/v1/admin/ai/runs; GET /api/v1/evidence/{id}; GET /api/v1/evidence; ADA… | 24_UI_UX_Components_Scre | C | Part 11.11a §11.11.4.2 Operational training register TRN-001…138 → Part 8.3b sc… | A017 data mapping: Part 2.7b card and Part 11.7a |
| 57 | Purpose / access candidate / Configure campaigns, audiences and schedules; Admin | 24_UI_UX_Components_Scre | C | Part 11.10b §11.10.4.2 Workflow test catalogue (156 workflows) (L144) | A058 purpose: Part 2.5/2.7b |
| 58 | Purpose / access candidate / Generate, edit and version B2B proposals; Admin | 24_UI_UX_Components_Scre | C | Part 11.10b §11.10.4.2 Workflow test catalogue (156 workflows) (L156) | A065 purpose: Part 2.5/2.7b |
| 59 | X26 / AI Voice & Intelligent Telephony Automation; call_ref,contact_ref,script_ref,recording_permission_ref;… | 24_UI_UX_Components_Scre | C | Part 11.18a §11.18.1 Material reviewed (L34) | A113 template X26: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 60 | X27 / Multimodal Creative & Localization Automation; brief_ref,brand_ref,asset_rights_refs,target_language; r… | 24_UI_UX_Components_Scre | C | Part 11.3c §SM-SVC-11 Content Marketing Automation (L46) | A113 template X27: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 61 | X28 / Agentic Commerce & AI-to-AI Business Transaction Automation; agent_ref,mandate_ref,offering_ref,order_r… | 24_UI_UX_Components_Scre | C | Part 11.17a §11.17.3 Detailed register (L100) | A113 template X28: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 62 | X29 / Account-Based Marketing & Enterprise Buying Group Automation; account_ref,icp_ref,role_evidence_refs,en… | 24_UI_UX_Components_Scre | C | Part 11.3b §SM-SVC-05 CRM & Sales Pipeline Automation (L978) | A113 template X29: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 63 | X30 / Conversion Rate Optimization & Intelligent Experimentation Automation; hypothesis_ref,variant_refs,allo… | 24_UI_UX_Components_Scre | C | Part 11.4a §11.4.3.4 DTO fields (Appendix B), all N→M (L344) | A113 template X30: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 64 | X31 / Marketplace & E-commerce Channel Operations Automation; marketplace_ref,sku_ref,inventory_ref,event_ref… | 24_UI_UX_Components_Scre | C | Part 11.4a §11.4.3.4 DTO fields (Appendix B), all N→M (L345) | A113 template X31: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 65 | X32 / Partner, Distributor & Co-Selling Automation; partner_ref,territory_ref,material_refs,deal_ref; result… | 24_UI_UX_Components_Scre | C | Part 11.3c §SM-SVC-16 Webinar, Event & Referral Acquisition Automation (L1233) | A113 template X32: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 66 | X33 / Customer Service & Support Operations Automation; customer_ref,enquiry_ref,sla_policy_ref,knowledge_ref… | 24_UI_UX_Components_Scre | C | Part 11.4a §11.4.3.4 DTO fields (Appendix B), all N→M (L336) | A113 template X33: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 67 | X34 / Product-Led Growth & Usage Intelligence Automation; account_ref,event_refs,feature_refs,plan_ref; resul… | 24_UI_UX_Components_Scre | C | Part 11.3b §SM-SVC-05 CRM & Sales Pipeline Automation (L978) | A113 template X34: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 68 | X35 / Brand Reputation & Review Intelligence Automation; brand_ref,review_refs,source_ids,threshold_ref; resu… | 24_UI_UX_Components_Scre | C | Part 11.3c §SM-SVC-11 Content Marketing Automation (L45) | A113 template X35: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 69 | X36 / AI Sales Enablement & Coaching Automation; learner_ref,playbook_ref,scenario_ref,authorized_session_ref… | 24_UI_UX_Components_Scre | C | Part 11.18b §11.18.5.24 Entities and data model (L368) | A113 template X36: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 70 | X37 / Pricing, Offer & Revenue Optimization Automation; offer_ref,cost_revision_ref,price_bounds_ref,history_… | 24_UI_UX_Components_Scre | C | Part 11.4a §11.4.3.4 DTO fields (Appendix B), all N→M (L351) | A113 template X37: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 71 | X38 / SMS, RCS & Business Messaging Automation; sender_ref,template_ref,recipient_refs,consent_refs; result e… | 24_UI_UX_Components_Scre | C | Part 11.3b §SM-SVC-06 Email Marketing & Outreach Automation (L1207) | A113 template X38: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 72 | X39 / Procurement & Supplier Management Automation; requirement_ref,supplier_refs,quote_refs,budget_ref; resu… | 24_UI_UX_Components_Scre | C | Part 11.4a §11.4.3.4 DTO fields (Appendix B), all N→M (L353) | A113 template X39: input/output refs present in Part 11.4a DTO registry; screen via A113 contract |
| 73 | API contract authority: Proposed routes below require reconciliation with inherited physical API inventory an… | 25_REST_API_Event_Contra | C | Part 11.10b §11.10.4.2 Workflow test catalogue (156 workflows) (L180) | API contract authority: Part 11.8a |
| 74 | POST /api/v1/commercial/applications / Application DTO + revision + digest; authenticated private intake; uni… | 25_REST_API_Event_Contra | C | Part 11.7b §A185 Customer applications & provisioning (V12 O02) (L1638) | Part 11.8a |
| 75 | GET /api/v1/commercial/applications/{id} / Verified tenant membership or operator intake scope / Minimal auth… | 25_REST_API_Event_Contra | C | Part 11.7b §A185 Customer applications & provisioning (V12 O02) (L1638) | Part 11.8a |
| 76 | ChannelAccount / tenant_id, company_id, account_id, channel, sender_alias, credential_ref, consent_policy, ca… | 26_PostgreSQL_Database_S | C | Part 11.5a §11.5.5.1 Tenancy hierarchy and isolation (MT-01, MT-05, MT-07; ch05… | Part 11.5a/11.8a |
| 77 | opt_scoped_cache / scope/purpose/input_hash/model/prompt/policy/evidence_version; expiry; artifact_ref / Uniq… | 26_PostgreSQL_Database_S | C | Part 11.9a §11.9.4.3 V5 and V4 candidate entities → blueprint (L640) | Part 11.9a |
| 78 | growth_model_run / prompt_version_id:uuid; job_run_id:uuid; model:text; input_tokens:int; output_tokens:int;… | 26_PostgreSQL_Database_S | C | Part 2.7a §2.7.4.5 Table reconciliation (155 source tables) (L596) | Part 3.6a/b |
| 79 | growth_budget / scope:text; period_start:date; limit_inr:decimal(14,2); reserved_inr:decimal(14,2); spent_inr… | 26_PostgreSQL_Database_S | C | Part 11.2b §11.2.5.16 SM-SVC-06 Email Marketing & Outreach Automation (L224) | Part 3.6a/b |
| 80 | growth_message / thread_id:uuid; draft_id:uuid nullable; direction:text; provider_message_id:text nullable; b… | 26_PostgreSQL_Database_S | C | Part 11.2b §11.2.5.16 SM-SVC-06 Email Marketing & Outreach Automation (L224) | Part 3.6a/b |
| 81 | growth_enrollment / sequence_id:uuid; contact_id:uuid; deal_id:uuid nullable; next_step_id:uuid nullable; sta… | 26_PostgreSQL_Database_S | C | Part 11.11a §11.11.4.8.2a The 156 chains (one row per workflow) (L798) | Part 3.6a/b |
| 82 | sales_usage_charge / tenant_id; subscription_id; usage_id; invoice_id; charge_key; units decimal; unit_price… | 26_PostgreSQL_Database_S | C | Part 11.8a §11.8.4.2.2 Full operation mapping (282 rows) (L563) | Part 3.6a/b |
| 83 | sales_data_transfer / tenant_id; startup_id; direction; dataset; checksum; object_ref; manifest jsonb; approv… | 26_PostgreSQL_Database_S | C | Part 11.8a §11.8.4.2.2 Full operation mapping (282 rows) (L530) | Part 3.6a/b |
| 84 | sales_action_plan / tenant_id; startup_id; objective; autonomy; input_hash; policy_hash; actions jsonb; simul… | 26_PostgreSQL_Database_S | C | Part 11.8a §11.8.4.2.2 Full operation mapping (282 rows) (L523) | Part 3.6a/b |
| 85 | sales_bid / tenant_id; startup_id; opportunity_id; proposal_id; deadline; source; eligibility jsonb; requirem… | 26_PostgreSQL_Database_S | C | Part 11.2b §11.2.5.29 SM-SVC-19 Tender & Project Bid Automation (L693) | Part 3.6a/b; automatic submission now under DEC-781 |
| 86 | sales_order_line / tenant_id; startup_id; order_id; product_id; description; quantity decimal; unit; price de… | 26_PostgreSQL_Database_S | C | Part 11.2b §11.2.5.30 SM-SVC-20 Sales Order & Fulfillment Automation (L729) | Part 3.6a/b |
| 87 | application / application_id UUID; revision integer; administrator_email text; config JSONB; digest text; sta… | 26_PostgreSQL_Database_S | C | Part 11.7b §A185 Customer applications & provisioning (V12 O02) (L1638) | Application intake persistence: Part 11.8a/11.9a |
| 88 | approval_decision / scope/run/payload_digest/policy_version; requester_id/reviewer_id; decision; expires_at;… | 26_PostgreSQL_Database_S | C | Part 11.9a §11.9.4.3 V5 and V4 candidate entities → blueprint (L653) | Part 11.9a |
| 89 | workflow_step_event / scope/run/step_id; sequence; state; artifact refs; error code; retry_after; observed_at… | 26_PostgreSQL_Database_S | C | Part 11.9a §11.9.4.3 V5 and V4 candidate entities → blueprint (L654) | Part 11.9a |
| 90 | Executed on the delivered V11 files with Playwright + Chromium (desktop 1366 px, mobile 390 px, desktop build… | 33_Unit_SIT_UAT_AI_Test_ | C | Part 11.10a §Application Blueprint: PART 11 (Batch 11.10a), V12 Tests (Unit/SIT… | Prototype evidence tooling: Part 11.10a |
| 91 | Not run / Manual screen-reader study, physical-device testing, load/failover/restore drills, real-model bench… | 33_Unit_SIT_UAT_AI_Test_ | C | Part 11.10a §11.10.3.7 Scorecards, weights and gates (RCTCFE, artifact scores,… | Not-run production tests are scheduled in Parts 6.1/11.10 |
| 92 | Change from V8 (8.2): traceability, security and reliability specifications are more complete (binding KPIs,… | 34_Quality_Control_Accep | C | Part 11.10a §11.10.3.7 Scorecards, weights and gates (RCTCFE, artifact scores,… | Score history: Part 11.10a |
| 93 | Eight-stage wizard / PASS / Local browser fixture | 34_Quality_Control_Accep | C | Part 11.1a §11.1.3.07 Chapter 07: Universal Business Configuration Onboar (L303) | Prototype check; production wizard Part 11.1a/11.5b |
| 94 | V5 browser regression evidence: Chromium rendered the generated HTML through in-memory page content because d… | 34_Quality_Control_Accep | C | Part 11.10a §Application Blueprint: PART 11 (Batch 11.10a), V12 Tests (Unit/SIT… | Prototype regression evidence metadata |
| 95 | Portfolio operator analytics absent / PASS / Local fixture; not production acceptance | 34_Quality_Control_Accep | C | Part 11.10a §11.10.3.4 V12 acceptance register: V5 optimization requirements (1… | Portfolio operator analytics absent: aggregate-only rule |
| 96 | After incident / Root cause, fix, regression test, review control gaps and notify stakeholders under approved… | 39_Release_Rollback_Cont | C | Part 11.11a §11.11.4.1 Enterprise requirement register ENT-* (65 rows) (L226) | After-incident review: Parts 8.3c/11.11 |

---

## 11.23.4 Catalogue reconciliation

### 11.23.4.1 By chapter file

| Doc | Chapter file | Bytes | Statements | Measured match before | After | C (different words) | N (restored) | S (superseded) |
|---|---|---|---|---|---|---|---|---|
| BRD | 00_Reading_guide_and_chapter_navigation | 1,852 | 2 | 0.0% | 100.0% | 2 | 0 | 0 |
| BRD | 00_front | 874 | 2 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 01_Executive_Summary_Product_Vision | 36,137 | 203 | 84.2% | 99.0% | 11 | 23 | 2 |
| BRD | 02_Business_Objectives_Success_Criteria | 1,324 | 6 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 03_Market_Positioning_Competitive_Strategy | 779 | 4 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 04_Stakeholders_Personas_Customer_Segmenta | 5,029 | 25 | 96.0% | 100.0% | 0 | 1 | 0 |
| BRD | 05_SaaS_Business_Commercial_Operating_Mode | 3,084 | 17 | 88.2% | 100.0% | 2 | 0 | 0 |
| BRD | 06_Multi_Tenant_Multi_Company_Business_Arc | 5,115 | 26 | 92.3% | 96.2% | 2 | 0 | 0 |
| BRD | 07_Universal_Business_Configuration_Onboar | 12,701 | 68 | 98.5% | 98.5% | 1 | 0 | 0 |
| BRD | 08_Master_Automation_Service_Catalogue_39 | 115,756 | 698 | 99.7% | 100.0% | 8 | 0 | 0 |
| BRD | 09_Business_Workflow_Catalogue_156_Workflo | 41,668 | 200 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 10_Subscription_Bundle_Entitlement_Model | 6,004 | 33 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 11_Pricing_Billing_Commercial_Unit_Economi | 20,037 | 137 | 97.8% | 100.0% | 3 | 0 | 0 |
| BRD | 12_Public_SaaS_Website_Customer_Acquisitio | 13,861 | 110 | 98.2% | 100.0% | 0 | 5 | 0 |
| BRD | 13_Market_Intelligence_Lead_Generation | 1,361 | 8 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 14_Digital_Marketing_Omnichannel_Engagemen | 3,394 | 20 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 15_Sales_Intelligence_Revenue_Conversion | 2,003 | 11 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 16_Commerce_Procurement_Partner_Operations | 999 | 4 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 17_Customer_Success_Retention_Product_Led | 13,213 | 77 | 98.7% | 100.0% | 1 | 0 | 0 |
| BRD | 18_AI_Automation_Authority_Business_Govern | 11,682 | 64 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 19_Portfolio_Command_Centre_Business_Analy | 11,140 | 62 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 20_Business_Security_Privacy_Compliance | 21,591 | 109 | 100.0% | 100.0% | 1 | 0 | 0 |
| BRD | 21_SLA_Support_Service_Delivery | 11,780 | 71 | 98.6% | 100.0% | 1 | 0 | 0 |
| BRD | 22_Business_KPI_Performance_Framework | 8,785 | 91 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 23_Roadmap_Prioritization_Commercial_Readi | 4,767 | 29 | 100.0% | 100.0% | 0 | 0 | 0 |
| BRD | 24_Business_Acceptance_Requirement_Traceab | 34,422 | 291 | 96.9% | 96.9% | 9 | 5 | 0 |
| BRD | 25_Decision_Register_Migration_Source_Appe | 7,227 | 38 | 97.4% | 100.0% | 1 | 0 | 0 |
| BRD | AP_Appendix_ID_index | 906 | 12 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 00_Reading_guide_and_chapter_navigation | 2,363 | 4 | 50.0% | 100.0% | 2 | 0 | 0 |
| FSD | 00_front | 891 | 2 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 01_Specification_Control_Reading_Guide | 35,592 | 210 | 80.0% | 99.0% | 14 | 31 | 2 |
| FSD | 02_System_Context_Solution_Architecture | 3,874 | 25 | 96.0% | 100.0% | 1 | 0 | 0 |
| FSD | 03_High_Level_Design | 2,041 | 8 | 87.5% | 100.0% | 1 | 0 | 0 |
| FSD | 04_Detailed_Component_Design | 1,462 | 11 | 90.9% | 100.0% | 1 | 0 | 0 |
| FSD | 05_Multi_Tenant_Data_Isolation_Architectur | 2,544 | 12 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 06_Identity_Roles_Authorization | 5,390 | 29 | 96.6% | 96.6% | 1 | 0 | 0 |
| FSD | 07_Tenant_Provisioning_Business_Configurat | 10,413 | 50 | 96.0% | 98.0% | 2 | 0 | 0 |
| FSD | 08_SaaS_Catalogue_Service_Registry | 3,346 | 46 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 09_Subscription_Entitlement_Engine | 5,781 | 31 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 10_Billing_Metering_Financial_Reconciliati | 8,079 | 46 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 11_Master_Functional_Specification_39_Serv | 99,442 | 507 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 12_Executable_Workflow_Specification_156_W | 855,963 | 4728 | 99.9% | 100.0% | 5 | 7 | 0 |
| FSD | 13_Workflow_Step_Trigger_Event_Registry | 30,021 | 193 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 14_Shared_AI_Automation_Engines | 4,266 | 21 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 15_AI_Agent_Registry_Orchestration | 6,428 | 33 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 16_AI_Models_Prompts_Evaluation | 29,419 | 205 | 99.5% | 100.0% | 1 | 0 | 0 |
| FSD | 17_RAG_Knowledge_Evidence_Engineering | 4,779 | 28 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 18_Policy_Approval_Human_in_the_Loop_Engin | 27,272 | 136 | 100.0% | 100.0% | 2 | 0 | 0 |
| FSD | 19_Automation_Scheduler_Execution_Control | 4,406 | 19 | 94.7% | 100.0% | 1 | 0 | 0 |
| FSD | 20_Public_SaaS_Website_Specification | 57,068 | 378 | 99.7% | 100.0% | 1 | 0 | 0 |
| FSD | 21_Tenant_Portal_Business_Workspace_Specif | 25,512 | 142 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 22_Platform_Operator_Administration | 3,108 | 24 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 23_Authorized_Portfolio_Command_Centre | 4,317 | 20 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 24_UI_UX_Components_Screens_Interaction_Ma | 171,941 | 1329 | 91.8% | 99.9% | 19 | 90 | 0 |
| FSD | 25_REST_API_Event_Contract_Master | 59,713 | 379 | 99.2% | 100.0% | 3 | 0 | 0 |
| FSD | 26_PostgreSQL_Database_Schema_Master | 91,065 | 637 | 97.5% | 99.7% | 14 | 2 | 0 |
| FSD | 27_External_Integrations_Provider_Adapters | 5,487 | 35 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 28_Open_Source_Paid_Plugin_Optimization | 24,804 | 126 | 97.6% | 100.0% | 3 | 0 | 2 |
| FSD | 29_Analytics_Attribution_KPI_Engineering | 9,908 | 50 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 30_AI_Cost_Performance_Optimization | 6,658 | 35 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 31_Cybersecurity_Privacy_Threat_Management | 9,077 | 52 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 32_Error_Handling_Retry_Recovery | 4,816 | 37 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 33_Unit_SIT_UAT_AI_Test_Specifications | 344,598 | 2351 | 99.8% | 99.9% | 5 | 0 | 0 |
| FSD | 34_Quality_Control_Acceptance_Evidence | 94,691 | 958 | 98.9% | 99.4% | 11 | 0 | 0 |
| FSD | 35_Coding_Standards_Development_Backlog | 8,771 | 48 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 36_Cloud_Infrastructure_CI_CD | 6,541 | 39 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 37_Observability_Incidents_Support | 122,513 | 173 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 38_Migration_Backup_Disaster_Recovery | 4,732 | 26 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | 39_Release_Rollback_Continuous_Improvement | 6,121 | 27 | 96.3% | 100.0% | 1 | 0 | 0 |
| FSD | 40_Master_Traceability_Decision_Register_S | 569,001 | 2605 | 75.4% | 77.1% | 642 | 0 | 0 |
| FSD | AP_Appendix_A2_Enterprise_API_additions_Ope | 36,981 | 49 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | AP_Appendix_A_OpenAPI_3_1_contract_proposed | 211,479 | 282 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | AP_Appendix_B_Workflow_DTO_JSON_Schemas_156 | 151,635 | 157 | 100.0% | 100.0% | 0 | 0 | 0 |
| FSD | AP_Appendix_C2_Enterprise_schema_additions | 11,461 | 67 | 70.1% | 70.1% | 21 | 0 | 0 |
| FSD | AP_Appendix_C_PostgreSQL_DDL_with_row_level | 96,436 | 447 | 73.8% | 73.8% | 117 | 0 | 0 |
| FSD | AP_Appendix_D_ID_index | 2,202 | 39 | 100.0% | 100.0% | 0 | 0 | 0 |

### 11.23.4.2 By unit type (before)

| Unit kind | Statements | Exact | Strong | Moderate | Weak | None |
|---|---|---|---|---|---|---|
| api | 327 | 0 | 306 | 21 | 0 | 0 |
| ddl | 502 | 2 | 306 | 57 | 136 | 1 |
| dto | 156 | 0 | 156 | 0 | 0 | 0 |
| heading | 625 | 429 | 196 | 0 | 0 | 0 |
| prose | 1,821 | 882 | 853 | 59 | 27 | 0 |
| row | 15,843 | 3810 | 8881 | 2272 | 852 | 28 |

### 11.23.4.3 ID families

| Check | Result |
|---|---|
| Distinct V12 IDs | 6,795 |
| Literal presence before | 90.26% of ID occurrences |
| With range and compressed notation | 99.92% |
| Compressed notation that explains most literal misses | Part 11.10b §11.10.4.2 lists, per workflow, the scenario suffixes (POS, INPUT, SCOPE, ENT, DUP, QUALITY, BUDGET, RECOVERY, APPROVAL, EFFECT) and the numbered step tests; the 1,867 `SM-SVC-##-WF#-TC-*` and `…-STEP-##-TC` IDs are therefore present by construction. Part 11.10a lists the V7/V8/V9/V11/V12 QA checks as ranges |
| Colliding families | V12 `DEC-###` and `DEC-Vn-##` (written CDEC, DEC-700), V12 `KPI-##` (= OKPI, DEC-681), V12 screen IDs A114–A131/W35–W41 (aliases `V12-…`, DEC-620), V12 `REC-##` (DEC-964), V12 `ENT-…` enterprise requirement IDs versus blueprint `ENT-###` entities (different shape, no clash) |
| IDs still absent after this part | 0 (all 11 IDs restored in §11.23.5.2 are now present) |

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
| commercial_website_desktop_V12.html | b9c3fa5cad677a9268d4124ad93679574579fe63dc8952d7d6fb5ba5236c60e2 | 8ceb0c24518ad1bc1fa993c67d9f273f41c3aafc2cd358026d576c9d2c6b5bd7 | b9c3fa5cad677a9268d4124ad93679574579fe63dc8952d7d6fb5ba5236c60e2 | Match after LF normalisation (CRLF added in transit) |
| commercial_website_mobile_V12.html | 84c748e298ddb27104565667398b57ef24a33230365ed3f09f6b83aac95754b3 | 2d1c49fb96541a0480e8134a32699ee2e47033c1c65f40a8a8a6c07614ecc9fe | 84c748e298ddb27104565667398b57ef24a33230365ed3f09f6b83aac95754b3 | Match after LF normalisation (CRLF added in transit) |
| commercial_admin_desktop_V12.html | 2801359a3d598d51e5b5bc44737f712a8171252cb6f4379e66bb82d98f4dade0 | ec90cde87bd6f2ed85bc5b4305bdb55b5622835c6ebcaf6233e758ff6cc99ad0 | 2801359a3d598d51e5b5bc44737f712a8171252cb6f4379e66bb82d98f4dade0 | Match after LF normalisation (CRLF added in transit) |
| commercial_admin_mobile_V12.html | 5995a670fd635d2795e479240e3bd5e633e1b1df601ef55c10faceb30a0a7e2c | cfd2bb40783bcc04e3e876227248fb4c170ee4f3d2f2685a22d448ccba02595f | 5995a670fd635d2795e479240e3bd5e633e1b1df601ef55c10faceb30a0a7e2c | Match after LF normalisation (CRLF added in transit) |
| Sales_Marketing_Automation_BRD_V12.docx | not declared | 7be408bf7d7450b4d6e58751a6190521819a3f72fde6387f8308de0fdeeceeec | n/a (binary) | Reference set from receipt |
| Sales_Marketing_Automation_FSD_V12.docx | not declared | 0c90b8d6da68f15eb56e773905923131312cebd97d4ce1e5b4f290c69bd49aa3 | n/a (binary) | Reference set from receipt |
| 38 documents.zip (historical archive) | 6fa3a27bbd2f6af18fe179f5e1a1ff9500dbbfa3eb1e0963475cd4bc550b0de3 | 6fa3a27bbd2f6af18fe179f5e1a1ff9500dbbfa3eb1e0963475cd4bc550b0de3 | n/a (binary) | Match as received |

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

| Workflow | V12 cost source (literal) | Use in the blueprint |
|---|---|---|
| SM-SVC-01-WF01 — Market and demand monitoring | Illustrative internal INR 1.51/invocation; excludes provider/retry/labor and other fees. | Illustrative unit-cost seed for the AU cost estimate and the workflow budget reservation default; replaced by measured cost after pilot (OKPI-11/12) |
| SM-SVC-01-WF03 — Trend report and evidence refresh | Illustrative internal INR 1.37/invocation; excludes provider/retry/labor and other fees. | Illustrative unit-cost seed for the AU cost estimate and the workflow budget reservation default; replaced by measured cost after pilot (OKPI-11/12) |
| SM-SVC-02-WF02 — Supplier, distributor and partner discovery | Illustrative internal INR 1.25/invocation; excludes provider/retry/labor and other fees. | Illustrative unit-cost seed for the AU cost estimate and the workflow budget reservation default; replaced by measured cost after pilot (OKPI-11/12) |
| SM-SVC-02-WF03 — Opportunity monitoring and alerts | Illustrative internal INR 0.67/invocation; excludes provider/retry/labor and other fees. | Illustrative unit-cost seed for the AU cost estimate and the workflow budget reservation default; replaced by measured cost after pilot (OKPI-11/12) |
| SM-SVC-09-WF01 — Unified conversation capture | Illustrative internal INR 0.71/invocation; excludes provider/retry/labor and other fees. | Illustrative unit-cost seed for the AU cost estimate and the workflow budget reservation default; replaced by measured cost after pilot (OKPI-11/12) |
| SM-SVC-11-WF03 — Content review and optimization | Illustrative internal INR 1.19/invocation; excludes provider/retry/labor and other fees. | Illustrative unit-cost seed for the AU cost estimate and the workflow budget reservation default; replaced by measured cost after pilot (OKPI-11/12) |
| SM-SVC-19-WF02 — Bid/no-bid assessment | Illustrative internal INR 1.25/invocation; excludes provider/retry/labor and other fees. | Illustrative unit-cost seed for the AU cost estimate and the workflow budget reservation default; replaced by measured cost after pilot (OKPI-11/12) |

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
| Requirement | For **every** registered Admin screen (the 90 listed below and every later Admin screen): (1) the server resolves the audience (operator, tenant workspace, portfolio, automation operations) and the object-level permission for each record before any data is returned; the client never decides access; (2) no Admin screen publishes tenant content publicly — publication happens only through the authorized SM-SVC-15 path; (3) source mappings shown in V12 (route/data mapping rows) are **not** wired until the API/DTO mapping is approved in Part 11.8; (4) forms validate inline (aria-invalid, aria-describedby, focus to first error); (5) the screen implements loading, empty, error, held and success states; (6) every write emits an audit event with actor, scope and correlation ID; (7) the screen is fully keyboard operable and usable in the compact (mobile) layout (DEC-623). Portfolio audience sees aggregates only; drill-down needs an object-level grant (DEC-504) |
| Acceptance | TC-V12-V-019…026 (classes) and the 40-row exhaustive Examples of US-01-ZV01 |

**Screens carrying the V2 rule in V12 ch24 (literal names).**

| Screen | Name (V12 ch24 registry) | Screen | Name (V12 ch24 registry) | Screen | Name (V12 ch24 registry) |
|---|---|---|---|---|---|
| A003 | Growth workspace navigation | A005 | Product knowledge catalog | A006 | Knowledge documents and approval |
| A008 | Integration connections | A010 | Source permissions and registry | A011 | AI configuration and evaluation |
| A013 | Privacy request queue | A014 | System health and incidents | A015 | Research planner |
| A016 | Market discovery results | A017 | Evidence detail panel | A018 | Organization directory |
| A019 | Buying signals board | A020 | Business need review | A021 | Product solution matching |
| A022 | Opportunity shortlist and scoring | A023 | Research rules and scoring settings | A024 | Decision-maker and contact discovery |
| A025 | Contact verification queue | A026 | Contact quality and role mapping | A027 | Qualified opportunity review |
| A028 | Research approval and alert rules | A030 | Sales pipeline and assignment rules | A031 | Lead form and routing configuration |
| A035 | Message templates and approval queue | A036 | Email channel configuration | A038 | Follow-up sequences and tasks |
| A039 | Follow-up policies | A040 | Meeting calendar and agenda | A041 | Calendar configuration |
| A043 | Management dashboard | A044 | WhatsApp channel and templates | A045 | WhatsApp conversations |
| A046 | Chat FAQ and omnichannel routing | A047 | Compliance incident dashboard | A048 | Social listening feed |
| A049 | Social source permissions | A050 | Content studio | A051 | Content and claims approval |
| A052 | Social publishing calendar | A053 | Social account and publishing controls | A054 | SEO and visibility dashboard |
| A055 | SEO review backlog | A056 | Landing page builder | A057 | Landing page approvals |
| A058 | Campaign builder and audience | A059 | Campaign approval and budgets | A060 | Paid advertising dashboard |
| A061 | Advertising spend controls | A062 | Webinar and demo event manager | A063 | Event and reminder settings |
| A064 | Referral and partner approvals | A065 | Proposal builder and preview | A066 | Proposal approval queue |
| A068 | Price and discount approval | A069 | Negotiation and objections | A070 | Negotiation exception queue |
| A071 | Contracts and MoUs | A072 | Contract and legal approvals | A073 | Payment and deal closure |
| A074 | Payment reconciliation | A075 | Customer onboarding checklist | A076 | Onboarding assignment |
| A077 | Partner deployment pipeline | A078 | Deployment readiness approval | A079 | Renewal and retention calendar |
| A080 | Renewal policies | A081 | Lost deal and feedback | A082 | Revenue and attribution dashboard |
| A083 | Revenue reconciliation and KPI settings | A084 | AI quality and feedback review | A085 | Competitor and market watch |
| A086 | Competitor source review | A087 | Sales forecasting dashboard | A088 | Forecast model settings |
| A091 | Insurance institutional pilot | A092 | Insurance pilot approval | A093 | Technology licensing enquiries |
| A094 | Licensing and API scope approval | A095 | Phygital expansion tracker | A096 | Phygital readiness approval |
| A097 | Future product catalog view | A098 | Future product launch approval | A099 | Tenant, startup and membership administration |
| A100 | Business profile templates and branding | A102 | Autonomous commercial planner and simulation | A104 | Global project bid and tender desk |
| A107 | Website configuration and content management | A111 | Automation Coordination & Conflict Resolution | A112 | Business Configuration Change Centre |

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
      | artifact | mode | expected |
      | commercial_website_desktop_V12.html | as received | MISMATCH (CRLF line endings added in transit); not a content change |
      | commercial_website_desktop_V12.html | LF-normalised | MATCH declared hash b9c3fa5cad67… |
      | commercial_website_mobile_V12.html | as received | MISMATCH (CRLF line endings added in transit); not a content change |
      | commercial_website_mobile_V12.html | LF-normalised | MATCH declared hash 84c748e298dd… |
      | commercial_admin_desktop_V12.html | as received | MISMATCH (CRLF line endings added in transit); not a content change |
      | commercial_admin_desktop_V12.html | LF-normalised | MATCH declared hash 2801359a3d59… |
      | commercial_admin_mobile_V12.html | as received | MISMATCH (CRLF line endings added in transit); not a content change |
      | commercial_admin_mobile_V12.html | LF-normalised | MATCH declared hash 5995a670fd63… |
      | Sales_Marketing_Automation_BRD_V12.docx | as received | record as-received SHA-256 as the reference (no declared hash); binary, no normalisation |
      | Sales_Marketing_Automation_BRD_V12.docx | LF-normalised | record as-received SHA-256 as the reference (no declared hash); binary, no normalisation |
      | Sales_Marketing_Automation_FSD_V12.docx | as received | record as-received SHA-256 as the reference (no declared hash); binary, no normalisation |
      | Sales_Marketing_Automation_FSD_V12.docx | LF-normalised | record as-received SHA-256 as the reference (no declared hash); binary, no normalisation |
      | 38 documents.zip (historical archive) | as received | MATCH (binary, unchanged) |
      | 38 documents.zip (historical archive) | LF-normalised | MATCH (binary, unchanged) |

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
      | input | outcome | detail |
      | 0.012 | accepted | stored as numeric(20,10) 0.0120000000 |
      | 0.5 | accepted | stored |
      | 1 | accepted | stored |
      | 83.2512 | accepted | stored |
      | 0.0000000001 | accepted | smallest positive at 10 decimals |
      | 0.00000000001 | rejected | FX_RATE_PRECISION: more than 10 decimals |
      | 0 | rejected | FX_RATE_NOT_POSITIVE |
      | -0.5 | rejected | FX_RATE_NOT_POSITIVE |
      | abc | rejected | FX_RATE_FORMAT |
      | 1,000.5 | rejected | FX_RATE_FORMAT (no grouping separators) |
      | 9999999999.9999999999 | accepted | upper bound numeric(20,10) |
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
      | audience | role | grant | state | expected |
      | Operator | R14 | granted | loading | skeleton with aria-busy, actions disabled |
      | Operator | R14 | granted | empty | empty state with permitted create action only |
      | Operator | R14 | granted | error | error state with retry and correlation ID; form values kept |
      | Operator | R14 | granted | held | held banner with reason code and owner; effect actions disabled |
      | Operator | R14 | granted | success | records of the granted scope; keyboard and compact-layout operable; audit on every write |
      | Operator | R14 | not granted | loading | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Operator | R14 | not granted | empty | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Operator | R14 | not granted | error | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Operator | R14 | not granted | held | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Operator | R14 | not granted | success | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Tenant workspace | R02 | granted | loading | skeleton with aria-busy, actions disabled |
      | Tenant workspace | R02 | granted | empty | empty state with permitted create action only |
      | Tenant workspace | R02 | granted | error | error state with retry and correlation ID; form values kept |
      | Tenant workspace | R02 | granted | held | held banner with reason code and owner; effect actions disabled |
      | Tenant workspace | R02 | granted | success | records of the granted scope; keyboard and compact-layout operable; audit on every write |
      | Tenant workspace | R02 | not granted | loading | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Tenant workspace | R02 | not granted | empty | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Tenant workspace | R02 | not granted | error | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Tenant workspace | R02 | not granted | held | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Tenant workspace | R02 | not granted | success | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Portfolio (aggregate) | R01 | granted | loading | skeleton, no partial company rows |
      | Portfolio (aggregate) | R01 | granted | empty | aggregate empty state "No reconciled data for this period" |
      | Portfolio (aggregate) | R01 | granted | error | error state with retry and correlation ID, no data |
      | Portfolio (aggregate) | R01 | granted | held | held banner with reason code, aggregate only |
      | Portfolio (aggregate) | R01 | granted | success | aggregate KPIs only; drill-down requires object-level grant |
      | Portfolio (aggregate) | R01 | not granted | loading | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Portfolio (aggregate) | R01 | not granted | empty | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Portfolio (aggregate) | R01 | not granted | error | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Portfolio (aggregate) | R01 | not granted | held | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Portfolio (aggregate) | R01 | not granted | success | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Automation ops | R13 | granted | loading | skeleton with aria-busy, actions disabled |
      | Automation ops | R13 | granted | empty | empty state with permitted create action only |
      | Automation ops | R13 | granted | error | error state with retry and correlation ID; form values kept |
      | Automation ops | R13 | granted | held | held banner with reason code and owner; effect actions disabled |
      | Automation ops | R13 | granted | success | records of the granted scope; keyboard and compact-layout operable; audit on every write |
      | Automation ops | R13 | not granted | loading | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Automation ops | R13 | not granted | empty | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Automation ops | R13 | not granted | error | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Automation ops | R13 | not granted | held | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
      | Automation ops | R13 | not granted | success | denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied` |
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
      | action_class | mandate | jurisdiction_pack | expected |
      | offer issue | Active | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | offer issue | Active | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | offer issue | Revoked | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | offer issue | Revoked | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | offering-tagged dispatch | Active | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | offering-tagged dispatch | Active | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | offering-tagged dispatch | Revoked | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | offering-tagged dispatch | Revoked | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | closing | Active | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | closing | Active | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | closing | Revoked | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | closing | Revoked | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | allotment reference | Active | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | allotment reference | Active | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | allotment reference | Revoked | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | allotment reference | Revoked | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | filing status | Active | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | filing status | Active | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | filing status | Revoked | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | filing status | Revoked | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | cap-table revision | Active | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | cap-table revision | Active | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | cap-table revision | Revoked | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | cap-table revision | Revoked | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | vote certification | Active | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | vote certification | Active | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | vote certification | Revoked | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | vote certification | Revoked | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | KYC decision | Active | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | KYC decision | Active | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | KYC decision | Revoked | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | KYC decision | Revoked | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | external submission | Active | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | external submission | Active | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | external submission | Revoked | Approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | external submission | Revoked | Not approved | MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table) |
      | non-offering IR message | Active | Approved | allowed under mandate (L3) after PDP recheck: caps, consent, quiet hours, kill switch off |
      | non-offering IR message | Active | Not approved | JURISDICTION_NOT_APPROVED; held, no dispatch |
      | non-offering IR message | Revoked | Approved | MANDATE_INACTIVE; held, human approval required |
      | non-offering IR message | Revoked | Not approved | MANDATE_INACTIVE; held, human approval required |
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
