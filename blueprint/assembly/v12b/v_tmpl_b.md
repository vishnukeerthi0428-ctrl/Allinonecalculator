# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.23b), Independent Completeness Audit (V12 → Blueprint) and Baseline Retention Check — B. Baseline Retention Check and Supersession Index

| Field | Value |
|---|---|
| Document | Part 11.23b: retention check of every ID of the pre-V12 blueprint (Parts 0–9.10 and 0B, and the pre-V12 registers) in the revised blueprint; status per ID; the supersession index `final/supersession_index.csv` |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Part 11.23a §11.23.1; Founder decisions DEC-770…791; Part 11 decision registers DEC-500…959 as present at the run |
| Roles applied | Configuration-management and baseline-integrity lead (lead) · Forensic requirements auditor · Principal Business Systems Analyst |

---

## 11.23.6 Baseline retention check

### 11.23.6.1 Baseline definition

| Item | Definition and evidence |
|---|---|
| Pre-V12 baseline | Parts 0, 0A, 0B and 1–9.10 (59 part files) plus the pre-V12 registers `final/RTM.csv`, `final/RTM_advanced.csv`, `final/dec_index.csv`, `final/adr_index.csv` and `final/coverage/*.csv` |
| Why the files are the baseline | The customer revision arrived on 28 Nov 2026 at 14:50 (V12 brief). Every Part 0–9.10 file was last modified on or before 28 Nov 2026 08:03 and the registers on or before 08:37 (v1.1 consolidation), so the working-tree files **are** the pre-V12 state. Every V12 group was forbidden to edit earlier parts, and none did (no Part 0–9 file changed after 08:03) |
| git | Not run (task constraint). [ASSUMPTION-1180] The file timestamps above are accepted as evidence of the baseline in place of the commit before "V12 customer revision"; the consolidation owner can confirm with `git diff <that commit> -- 'Part-0*'`, which must be empty |
| Revised blueprint | All `Part-*.md` except Part 11.23 (Parts 11.0–11.22 present at the run) |
| Families audited | BR, FR, NFR, US, AC, TC, VER, API, ENT, screen IDs (A###, W##), AG, AU, WF, DEC, ADR, RSK, KPI, OKPI, BRL, CFG, RP — including their sub-families (FR-ENH, FR-ADV, TC-ENH, TC-AI, TC-AU, US-##-E…, API-ENH, VER-ENH, BRL-ENH, …) |
| Scripts | `v_10_baseline.py` (inventory and presence), `v_11_supersession.py` (status and index), `v_overrides.tsv` (curated decisions, each with its authority) |

### 11.23.6.2 Method

1. **Inventory.** Every literal ID of the audited families in the baseline files (ranges such as `TC-21-068…072` are used for presence only, never to invent IDs). A descriptor is taken from the row or heading that starts with the ID.
2. **Presence.** Each baseline ID is looked up in the revised blueprint (literal or range-implied). The pre-V12 registers are scanned too: an ID they carry that no part carries would be **missing**.
3. **Status evidence**, strongest first:
   - (1) decision rows `| DEC-### |` of Parts 11.x (post-baseline decisions DEC-423 and above), sentence by sentence: a sentence that names a baseline ID with *supersede / replace / withdraw / lift* is **superseded**, or **amended** when the sentence scopes it ("for actions covered by an active mandate", "only", "where", "for the Admin"); a sentence with *amend / extend / alias / narrow / refine / align / re-plan / indicative* is **amended**;
   - (2) other Part 11 lines that name a baseline ID, a post-baseline DEC and a change verb (**amended**, or **superseded** when the verb binds to the ID);
   - (3) baseline rows whose own text states a rule that a Founder decision changed (09:00–19:00 window, investor exclusion, voice/recording prohibition, bid submission, L1 cap, service key, RTO 4 h, business-hours support, RDS/PostgreSQL 17, single region) — **amended (read with DEC-…)**;
   - (4) curated overrides (`v_overrides.tsv`) where the automatic reading was wrong or too weak (for example a CDEC equivalence row is not an amendment; DEC-421 is amended, not superseded).
4. **Status values.** *Retained unchanged* · *Amended* (authority named) · *Superseded* (replacement and decision named) · *Missing* (an error; restored in §11.23.6.6).

### 11.23.6.3 Result by family

{{F:base}}

**Reading.** All {{M:base.n_fmt}} baseline IDs are still present in the revised blueprint and none is missing from the pre-V12 registers. {{M:base.amended}} IDs are amended and {{M:base.superseded}} are superseded by later decisions; every one of them is listed individually in §11.23.6.4 and in `final/supersession_index.csv`. Tests (TC), acceptance criteria (AC), stories (US), configuration domains (CFG), reports (RP) and verification items (VER) are retained; the few TC/US/FR rows amended are those whose own text states a rule a Founder decision changed (they remain valid outside the new scope and are read with the cited DEC).

### 11.23.6.4 Amended and superseded IDs (every ID)

{{F:changed}}

### 11.23.6.5 Key supersessions in plain words (for the development team)

| Baseline position | Now | Authority |
|---|---|---|
| DEC-002 / CC-01: no investor or fundraising features | Investor mode and the Investment Automation product are in scope, behind securities rule packs and counsel sign-off | DEC-783 |
| DEC-064: consequential actions capped at L1 | Cap lifted only for actions covered by an Active, eligible bounded mandate in an approved jurisdiction; everything else stays L1 | DEC-779, DEC-841 |
| DEC-053: no automatic bid submission | Allowed per tender under a bounded mandate with an approved package hash; unmandated stays human | DEC-781 |
| DEC-386/387/392 (and DEC-218 where it restricts recording): no AI voice, no recordings, no SMS in W0–W5 | AI voice and recordings with disclosure, consent, windows, retention; SMS via DLT aggregator in Release 1 | DEC-782, DEC-785, DEC-884 |
| DEC-158 (RTO 4 h at pilot) and DEC-018/021 | Growth RTO ≤ 120 min blocking; RPO ≤ 15 min everywhere | DEC-771, DEC-787 |
| DEC-421: Vercel + Supabase + AWS Mumbai, "service key server-side" | Same providers, Mumbai + EU stacks, least-privilege `app_rw` role, personal data via Vercel with controls | DEC-772, DEC-776, DEC-778, DEC-786, DEC-894 |
| DEC-044/080: business-hours support | 24×7 on-call for SEV1/SEV2 from Release 2 GA | DEC-773 |
| DEC-325: SLA | 99.5 / 99.9 / 99.95% tiers with service credits | DEC-774 |
| DEC-408: certify on contract trigger | SOC 2 I (R2) → SOC 2 II + ISO 27001 (R3) → ISO 27701 + ISO 42001 (R4) | DEC-775 |
| BRL-ELG-08: 09:00–19:00 Mon–Sat | 09:00–21:00 recipient local time unless a pack is stricter | DEC-777 |
| DEC-418: Claude Sonnet primary | Primary by approval in a provider-neutral registry | DEC-788 |
| DEC-228 fixed dates | Dates indicative; scope not cut for dates | DEC-770 |
| DEC-230/231/422 budgets | Extended by funded change requests and the new running-cost lines | DEC-790, DEC-771…774 |

### 11.23.6.6 Missing IDs and dangling placeholders

| Check | Result | Action |
|---|---|---|
| Baseline IDs absent from the revised blueprint | **0** | none |
| IDs in the pre-V12 registers absent from every part | **0** | none |
| Baseline IDs referenced but never defined by a row or heading | {{M:base_undef}} strings; after review all are prefixes, placeholders or reserved-unused numbers, not lost requirements: family stubs (`US-08XX`, `BRL-X3`, `RSK-ADV-X1`, `KPI-ADV-X2`, …), source-numbered FRD/test aliases (`FR-001…`, `TC-01-A…`), reserved and unused numbers (DEC-271…299 and DEC-333…379 stated unused in Parts 9.6a/b; WF-24 and WF-40 stated unused in Part 9.10; ADR-044…049 allocation line), and SIT aliases read as screens (`A280`, `A302` from `SM-SIT-A280/A302`) | none |
| Placeholders never resolved | `ENT-200…203` ("final ENT numbers to be assigned by the coordinator", Part 3.6a/9.5) and `API-556+` ("the coordinator may renumber them into API-556+", Part 3.5b) were never assigned; the entities and operations live on as `ENT-ENH-*` and `API-ENH-*` | **DEC-967**: the ENH IDs are canonical; no renumbering; [GAP-1183] closed |

**Conclusion.** No baseline ID was lost in the V12 revision. The retention risk is not loss but **silent contradiction**: {{M:base.changed}} baseline IDs (and many more sentences) still read as before while a later decision changed them. That is why every amended and superseded ID is listed above with its authority, and why Part 11.23c turns each stale statement into an erratum with the current rule.

### 11.23.6.7 Supersession index file

`final/supersession_index.csv` has one row per baseline ID ({{M:base.n_fmt}} rows):

| Column | Content |
|---|---|
| id | baseline ID |
| family | audited family |
| baseline_location | first occurrence in Parts 0–9.10 (part and line) |
| baseline_descriptor | the row or heading text that defines the ID (truncated) |
| status | retained unchanged / amended / superseded / missing |
| authority | the decision or part that changed it |
| replacement_ids | new or alias IDs of the same family (for example W02 → W54) |
| evidence_location | Part 11 location of the evidence (part, section, line) |
| evidence_or_note | the sentence that changes it, or the curated note |

The file is regenerated by `v_11_supersession.py`; FR-V12-V-009 runs it in documentation CI.

---

**Continued in Part 11.23c (cross-part errata, conflicts, decisions, tags, quality gate).**
