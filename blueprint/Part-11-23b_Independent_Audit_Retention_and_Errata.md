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

| Family | Baseline IDs | Retained unchanged | Amended | Superseded | Missing |
|---|---|---|---|---|---|
| AC | 1,687 | 1,687 | 0 | 0 | 0 |
| ADR | 107 | 102 | 5 | 0 | 0 |
| AG | 83 | 80 | 3 | 0 | 0 |
| API | 624 | 621 | 3 | 0 | 0 |
| AU | 120 | 116 | 4 | 0 | 0 |
| BR | 209 | 204 | 5 | 0 | 0 |
| BRL | 358 | 343 | 14 | 1 | 0 |
| CFG | 53 | 53 | 0 | 0 | 0 |
| DEC | 348 | 287 | 52 | 9 | 0 |
| ENT | 214 | 207 | 7 | 0 | 0 |
| FR | 801 | 793 | 8 | 0 | 0 |
| KPI | 61 | 60 | 1 | 0 | 0 |
| NFR | 130 | 127 | 3 | 0 | 0 |
| OKPI | 35 | 33 | 2 | 0 | 0 |
| RP | 52 | 52 | 0 | 0 | 0 |
| RSK | 218 | 215 | 3 | 0 | 0 |
| SCREEN | 233 | 160 | 72 | 1 | 0 |
| TC | 4,653 | 4,633 | 20 | 0 | 0 |
| US | 475 | 470 | 5 | 0 | 0 |
| VER | 68 | 68 | 0 | 0 | 0 |
| WF | 40 | 38 | 2 | 0 | 0 |
| **Total** | **10,569** | **10,349** | **209** | **11** | **0** |

**Reading.** All 10,569 baseline IDs are still present in the revised blueprint and none is missing from the pre-V12 registers. 209 IDs are amended and 11 are superseded by later decisions; every one of them is listed individually in §11.23.6.4 and in `final/supersession_index.csv`. Tests (TC), acceptance criteria (AC), stories (US), configuration domains (CFG), reports (RP) and verification items (VER) are retained; the few TC/US/FR rows amended are those whose own text states a rule a Founder decision changed (they remain valid outside the new scope and are read with the cited DEC).

### 11.23.6.4 Amended and superseded IDs (every ID)

| # | ID | Status | Authority | Replacement / alias | Evidence | Note |
|---|---|---|---|---|---|---|
| 1 | ADR-019 | amended | DEC-772 | — | Part 3.1 L1407 (baseline row) | Read with DEC-772: India (Mumbai) and EU residency stacks; further regions per DEC-776 when their rule pack is approved |
| 2 | ADR-028 | amended | DEC-564 | — | Part 11.4d §11.4.7 Decisions (L1783) | Amends ADR-028 wording, AU-028 and Part 3.3 ENT-161 |
| 3 | ADR-030 | amended | DEC-565 | — | Part 11.4d §11.4.7 Decisions (L1784) | Narrows ADR-030 to REST resources; |
| 4 | ADR-085 | amended | DEC-845 | — | Part 11.17a §11.17.6.10 Decisions recorded in this file (L9… | extends ADR-085 |
| 5 | ADR-138 | amended | DEC-645 | — | Part 11.8b §11.8.8.5 Inconsistencies found in earlier parts… | / 2 / Part 3.2 §3.2.1.13 vs Part 9.9a ADR-138 / Part 3.2 says outbound webhooks are not offered in W0–W6; Part 9.9a specifies them for A3 / Supersede… |
| 6 | AG-045 | amended | DEC-870 | — | Part 11.18d §11.18.6 Conflicts and proposed resolutions (L9… | Also: DEC-782. / [CONFLICT-1069] / SM-SVC-36 "review recordings and training outputs" / DEC-386: AG-045/AG-046 outputs private, team-level k ≥ 5, no… |
| 7 | AG-046 | amended | DEC-870 | — | Part 11.18d §11.18.6 Conflicts and proposed resolutions (L9… | / [CONFLICT-1069] / SM-SVC-36 "review recordings and training outputs" / DEC-386: AG-045/AG-046 outputs private, team-level k ≥ 5, no employee evalua… |
| 8 | AG-075 | amended | DEC-618 | — | Part 11.6a §11.6.3.1 Partially covered, not covered and con… | / F18-001 / 18 · V12 compliance / ENT-CMP-01 (P0): SOC 2 Type I at R2 and Type II at R3 / Conflict / AG-075 SOC 2-aligned narratives; no audit commit… |
| 9 | API-067 | amended | DEC-641 | API-V12-H-059 | Part 11.8a §11.8.3.1 Partial, not covered, conflict and not… | / HAA-post_consents_id_withdraw / FSD V12 Appendix A / POST /api/v1/consents/{id}/withdraw [Compliance] Withdraw consent and suppress (CJ-R05); reque… |
| 10 | API-082 | amended | DEC-641 | API-V12-H-059 | Part 11.8a §11.8.3.1 Partial, not covered, conflict and not… | / HAA-post_consents_id_withdraw / FSD V12 Appendix A / POST /api/v1/consents/{id}/withdraw [Compliance] Withdraw consent and suppress (CJ-R05); reque… |
| 11 | API-497 | amended | DEC-505 | — | Part 11.1b §11.1.7 Decisions (L847) | Amends FR-W02, FR-W03, API-497, US-1905 (CONFLICT-764) |
| 12 | AU-001 | amended | DEC-606 | AU-152 | Part 11.6b §11.6.7 Decisions (L2061) | Also: DEC-562. AU-152 extends AU-001 rules R6/R8 |
| 13 | AU-002 | amended | DEC-567 | — | Part 11.4d §11.4.7 Decisions (L1786) | Also: DEC-607. Extends DEC-321 and AU-002 |
| 14 | AU-009 | amended | DEC-613 | AU-171 | Part 11.6b §11.6.7 Decisions (L2068) | Also: DEC-546. AU-171 extends AU-009 |
| 15 | AU-028 | amended | DEC-564 | — | Part 11.4d §11.4.7 Decisions (L1783) | Amends ADR-028 wording, AU-028 and Part 3.3 ENT-161 |
| 16 | BR-S003 | amended | DEC-783 | — | Part 5.1c L1982 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 17 | BR-S004 | amended | DEC-579 | — | Part 11.4d §11.4.7 Decisions (L1798) | Extends WF-10 and the OrganicSpec route (BR-S004) |
| 18 | BR-S021 | amended | DEC-783 | — | Part 1 L611 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 19 | BR-S062 | amended | DEC-783 | — | Part 1 L667 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 20 | BR-S110 | amended | DEC-783 | — | Part 1 L735 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 21 | BRL-ADV-X2-16 | amended | DEC-782 | — | Part 9.8a L315 (baseline row) | Read with DEC-782: AI voice and recordings adopted with AI disclosure, consent, calling windows and retention controls (Part 11.18) |
| 22 | BRL-ADV-X2-42 | amended | DEC-781 | — | Part 9.8a L341 (baseline row) | Read with DEC-781: Automatic bid submission allowed only under a per-tender bounded mandate (Part 11.17b); unmandated submission still blocked |
| 23 | BRL-AI-07 | amended | DEC-841 | — | Part 11.17a §11.17.6.10 Decisions recorded in this file (L9… | Also: DEC-540. Amends DEC-064, BRL-AUT-01, BRL-AI-07 (scoped) |
| 24 | BRL-APR-07 | amended | DEC-849 | — | Part 11.17a (DEC-849) | Exact automated PSP matches close without manual verification; mismatches to Finance maker-checker |
| 25 | BRL-AUT-01 | amended | DEC-841 | — | Part 11.17a §11.17.6.10 Decisions recorded in this file (L9… | Also: DEC-546. Amends DEC-064, BRL-AUT-01, BRL-AI-07 (scoped) |
| 26 | BRL-AUT-03 | amended | DEC-569 | — | Part 11.4a §11.4.3.1 Common aspects (FSD ch12 preamble, ch1… | / D-B09-003 / MT-34 one definition per stable workflow/version; child step reuse via contracts; per-customer configuration only; MT-TC-MT-34 add 25 c… |
| 27 | BRL-BID-01 | amended | DEC-852 | — | Part 11.17b §11.17.16.1 Decisions (L3239) | Also: DEC-781, DEC-841. Amends BRL-BID-01 for automated attempts; |
| 28 | BRL-BID-04 | amended | DEC-851 | — | Part 11.17b §11.17.16.1 Decisions (L3238) | Also: DEC-841. Amends BRL-BID-04, DEC-053 (scoped); |
| 29 | BRL-CTR-04 | amended | DEC-779 | — | Part 2.3 L189 (baseline row) | Read with DEC-779: L1 cap lifted only for actions under an Active, eligible bounded mandate in an approved jurisdiction (DEC-841) |
| 30 | BRL-ELG-05 | amended | DEC-507 | — | Part 11.15a §11.15.3.4 Jurisdiction-detection logic (L164) | **Resolution rules.** (a) The resolved set is the **union** of all jurisdictions indicated by J1–J7 (never a "best guess" single country). (b) Confli… |
| 31 | BRL-ELG-08 | superseded | DEC-777 | — | Part 11.14 §11.14.1 Founder decisions recorded (28 Nov 2026… | Supersedes the 09:00–19:00 Mon–Sat default of BRL-ELG-08; |
| 32 | BRL-ELG-18 | amended | DEC-507 | — | Part 11.15a §11.15.3.4 Jurisdiction-detection logic (L164) | **Resolution rules.** (a) The resolved set is the **union** of all jurisdictions indicated by J1–J7 (never a "best guess" single country). (b) Confli… |
| 33 | BRL-FIN-07 | amended | DEC-841 | — | Part 11.17a §11.17.3 Detailed register (L122) | / P-AMD-BRL-FIN-07 / Blueprint — · BRL-FIN-07 / Amend/scope BRL-FIN-07 (No card/bank credentials) for actions under an Active mandate / Covered / Par… |
| 34 | BRL-SVC-01 | amended | DEC-502 | — | Part 11.1b §11.1.7 Decisions (L844) | Extends BRL-SVC-01…07 and CSO-01…12 |
| 35 | BRL-TEN-12 | amended | DEC-783 | — | Part 2.3 L36 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 36 | DEC-002 | superseded | DEC-783 | — | Part 11.14 §11.14.1 (DEC-783) | Investor and fundraising exclusion withdrawn; Investment Automation product adopted with securities rule packs and counsel gates |
| 37 | DEC-003 | amended | DEC-713 | — | Part 11.11b §11.11.7 Decisions (L804) | Amends DEC-003 scope |
| 38 | DEC-006 | amended | DEC-784 | — | Part 11.20a §11.20.3.1 Why the release structure changes (L… | Part 8.1 planned two releases (R1 = W0–W3, R2 = W4–W5) and W6; Part 9.10 added A1–A3. The Founder decisions of 28 Nov 2026 add four kinds of scope th… |
| 39 | DEC-008 | amended | DEC-607 | — | Part 11.6a §11.6.3.1 Partially covered, not covered and con… | / F16-065 / 16 · 16.7 / Budgets: soft cap (default 80%) alerts; hard cap holds new AI steps while deterministic steps continue; caps per tenant, comp… |
| 40 | DEC-016 | amended | DEC-506 | — | Part 11.1b §11.1.7 Decisions (L848) | Also: DEC-581. Extends DEC-016 entities |
| 41 | DEC-018 | amended | DEC-771 | — | Part 11.14 §11.14.1 (DEC-771) | RTO: growth-critical <= 120 min release-blocking (DEC-771); RPO <= 15 min (DEC-787); staged 4 h pilot target of DEC-158 superseded |
| 42 | DEC-021 | amended | DEC-787 | — | Part 11.14 §11.14.1 (DEC-787) | RPO <= 15 min in every residency region (continuous WAL, daily base, 35-day PITR) |
| 43 | DEC-022 | amended | DEC-501 | — | Part 11.1a §11.1.4.9 The two REC series (L1081) | Chapter 25 contains an older table whose rows are labelled "REC-01/05", "REC-02/03", "REC-04", "REC-06", "REC-07/08", "REC-09/11", "REC-10", "REC-12"… |
| 44 | DEC-023 | amended | DEC-779 | — | Part 0A L60 (baseline row) | Read with DEC-779: L1 cap lifted only for actions under an Active, eligible bounded mandate in an approved jurisdiction (DEC-841) |
| 45 | DEC-026 | amended | DEC-776 | — | Part 11.14 §11.14.1 Founder decisions recorded (28 Nov 2026… | Also: DEC-516, DEC-625, DEC-633. Amends DEC-040/421 (regions), DEC-026/404 (locales), DEC-027 (tax beyond India GST) and DEC-405 (BYOK beyond AWS KMS… |
| 46 | DEC-027 | amended | DEC-776 | — | Part 11.14 §11.14.1 Founder decisions recorded (28 Nov 2026… | Also: DEC-543, DEC-587, DEC-664. Amends DEC-040/421 (regions), DEC-026/404 (locales), DEC-027 (tax beyond India GST) and DEC-405 (BYOK beyond AWS KMS… |
| 47 | DEC-029 | amended | DEC-776 | — | Part 11.14 §11.14.1 Founder decisions recorded (28 Nov 2026… | Also: DEC-507, DEC-611, DEC-772. **The legal gates stay:** each market opens only when its jurisdiction rule pack is signed off by counsel (DEC-029 a… |
| 48 | DEC-034 | amended | DEC-512 | — | Part 11.1a §11.1.3.23 Chapter 23: Roadmap Prioritization Co… | / R0 / Phase: R0 / Name: Foundations / Scope: Build core platform from Appendices A–C/A2/C2; identity reuse; CI/CD with SAST/DAST/SBOM; infrastructur… |
| 49 | DEC-040 | amended | DEC-776 | — | Part 11.14 §11.14.1 Founder decisions recorded (28 Nov 2026… | Amends DEC-040/421 (regions), DEC-026/404 (locales), DEC-027 (tax beyond India GST) and DEC-405 (BYOK beyond AWS KMS). |
| 50 | DEC-043 | amended | DEC-623 | — | Part 11.7c §11.7.7 Decisions (L739) | Also: DEC-633. Amends DEC-043 for Admin; |
| 51 | DEC-044 | superseded | DEC-773 | — | Part 11.14 §11.14.1 (DEC-773) | Business-hours support replaced by 24x7 human on-call for SEV1/SEV2 (DEC-702: DEC-044 kept only for the owned-portfolio support schedule) |
| 52 | DEC-047 | amended | DEC-501 | — | Part 11.1b §11.1.7 Decisions (L843) | Also: DEC-503, DEC-521, DEC-584. Amends DEC-047 (CONFLICT-767) |
| 53 | DEC-050 | amended | DEC-853 | — | Part 11.17b §11.17.16.1 Decisions (L3240) | Extends DEC-050 |
| 54 | DEC-053 | amended | DEC-781 | — | Part 11.14 §11.14.1 (DEC-781) | Superseded for mandated tenders only; unmandated bid submission remains human |
| 55 | DEC-055 | amended | DEC-504 | — | Part 11.1b §11.1.7 Decisions (L846) | Also: DEC-509. Amends DEC-065, DEC-055 (CONFLICT-763) |
| 56 | DEC-057 | amended | DEC-783 | — | Part 0A L101 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 57 | DEC-058 | amended | DEC-517 | — | Part 11.1b §11.1.6 Conflicts and proposed resolutions (L834) | **Investor / fundraising check (DEC-002).** The assigned BRD chapters do **not** extend scope to investors or fundraising. They reaffirm the exclusio… |
| 58 | DEC-062 | amended | DEC-509 | — | Part 11.1b §11.1.7 Decisions (L851) | Extends DEC-055, DEC-062 |
| 59 | DEC-064 | amended | DEC-779 | — | Part 11.14 §11.14.1 (DEC-779); Part 11.17a DEC-841 | L1 cap lifted only for actions covered by an Active, eligible bounded mandate in an approved jurisdiction |
| 60 | DEC-065 | amended | DEC-504 | — | Part 11.1b §11.1.7 Decisions (L846) | Amends DEC-065, DEC-055 (CONFLICT-763) |
| 61 | DEC-068 | amended | DEC-782 | — | Part 9.1 L22 (baseline row) | Read with DEC-782: AI voice and recordings adopted with AI disclosure, consent, calling windows and retention controls (Part 11.18) |
| 62 | DEC-079 | amended | DEC-771 | — | Part 9.1 L33 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 63 | DEC-080 | superseded | DEC-773 | — | Part 11.14 §11.14.1 (DEC-773) | Business-hours support model replaced by 24x7 on-call |
| 64 | DEC-158 | superseded | DEC-771 | — | Part 11.14 §11.14.1 (DEC-771) | Staged RTO (4 h at pilot, 2 h after Topology B) replaced by growth RTO <= 120 min blocking |
| 65 | DEC-169 | amended | DEC-783 | — | Part 9.2 L1918 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 66 | DEC-176 | amended | DEC-781 | — | Part 9.2 L1925 (baseline row) | Read with DEC-781: Automatic bid submission allowed only under a per-tender bounded mandate (Part 11.17b); unmandated submission still blocked |
| 67 | DEC-178 | amended | DEC-700 | — | Part 11.11b §11.11.7 Decisions (L791) | CDEC-001…180 ≡ SPDEC-001…180 (extends DEC-178). |
| 68 | DEC-179 | amended | DEC-783 | — | Part 9.5 L81 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 69 | DEC-209 | amended | DEC-702 | — | Part 11.11b §11.11.7 Decisions (L793) | Amends DEC-327 and DEC-209 for contracted tiers; |
| 70 | DEC-210 | amended | DEC-521 | — | Part 11.2c §11.2.7 Decisions (L822) | Amends DEC-047, DEC-210, DEC-326; |
| 71 | DEC-218 | amended | DEC-782 | — | Part 11.14 §11.14.1 Founder decisions recorded (28 Nov 2026… | Also: DEC-529, DEC-531, DEC-572, DEC-870. Supersedes DEC-386, 387 and 392, and DEC-218 where it restricts recording and transcripts. |
| 72 | DEC-228 | amended | DEC-770 | — | Part 11.14 §11.14.1 (DEC-770) | Staffing Option 2b kept; fixed dates become indicative |
| 73 | DEC-230 | amended | DEC-790 | — | Part 11.17b §11.17.15 Effort and cost (L3162) | Also: DEC-500, DEC-578. All figures are **estimates** for a separately approvable change request **CR-V12-P** under DEC-790 ("all V12 change requests… |
| 74 | DEC-231 | amended | DEC-790 | — | Part 11.17b §11.17.15 Effort and cost (L3162) | All figures are **estimates** for a separately approvable change request **CR-V12-P** under DEC-790 ("all V12 change requests are funded"); they are… |
| 75 | DEC-245 | amended | DEC-783 | — | Part 9.2 L1993 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 76 | DEC-252 | amended | DEC-783 | — | Part 9.6a L1309 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 77 | DEC-304 | amended | DEC-783 | — | Part 9.6b L1432 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 78 | DEC-306 | amended | DEC-712 | — | Part 11.11b §11.11.7 Decisions (L803) | Amends DEC-306 for tenant-level defaults |
| 79 | DEC-321 | amended | DEC-567 | — | Part 11.4d §11.4.7 Decisions (L1786) | Extends DEC-321 and AU-002 |
| 80 | DEC-325 | superseded | DEC-774 | — | Part 11.14 §11.14.1 (DEC-774) | SLA tiers 99.5/99.9/99.95% contractual with service credits |
| 81 | DEC-326 | amended | DEC-521 | — | Part 11.2c §11.2.7 Decisions (L822) | Amends DEC-047, DEC-210, DEC-326; |
| 82 | DEC-327 | amended | DEC-702 | — | Part 11.11b §11.11.7 Decisions (L793) | Amends DEC-327 and DEC-209 for contracted tiers; |
| 83 | DEC-386 | superseded | DEC-782 | — | Part 11.14 §11.14.1 (DEC-782) | Recording exclusion lifted; recording with jurisdictional notice/consent, retention and redaction (Part 11.18) |
| 84 | DEC-387 | superseded | DEC-782 | — | Part 11.14 §11.14.1 (DEC-782) | Superseded by AI voice calling adoption (Part 11.18) |
| 85 | DEC-388 | amended | DEC-847 | — | Part 11.15d §11.15.25.4 Rules (L1168) | / RP-GL-AGENTCOM-005 / Every price, discount, quantity, date and amount in an agent message shall be produced by the deterministic negotiation bound… |
| 86 | DEC-392 | superseded | DEC-782 | — | Part 11.14 §11.14.1 (DEC-782) | No-voice/SMS-in-W0-W5 note superseded; SMS connectors in Release 1 (DEC-785, DEC-884) |
| 87 | DEC-404 | amended | DEC-625 | — | Part 11.7c §11.7.7 Decisions (L741) | Amends DEC-026/DEC-404 for the website; |
| 88 | DEC-405 | amended | DEC-776 | — | Part 11.14 §11.14.1 Founder decisions recorded (28 Nov 2026… | Amends DEC-040/421 (regions), DEC-026/404 (locales), DEC-027 (tax beyond India GST) and DEC-405 (BYOK beyond AWS KMS). |
| 89 | DEC-406 | amended | DEC-703 | — | Part 11.11b §11.11.9.2 Inconsistencies found in earlier par… | / 3 / Part 4.3 §4.43.4 / "Status page: Not defined [GAP-126]" although DEC-406 closed GAP-126 / Read with DEC-406/DEC-703 / |
| 90 | DEC-408 | superseded | DEC-775 | — | Part 11.14 §11.14.1 (DEC-775) | Certification sequence SOC 2 Type I (R2) -> SOC 2 Type II + ISO 27001 (R3) -> ISO 27701 + ISO 42001 (R4) |
| 91 | DEC-410 | amended | DEC-770 | — | Part 11.20a §Application Blueprint: PART 11 (Batch 11.20a),… | / Baseline / Part 11.14 (Founder decisions DEC-770…791, binding); Part 8.1 and 8.2 (template, capacity method, gates, RACI, risk method); Part 8.4 (t… |
| 92 | DEC-411 | amended | DEC-741 | — | Part 11.13b §11.13.7 Decisions (L1491) | Also: DEC-512, DEC-790, DEC-905. Extends DEC-411 roadmap |
| 93 | DEC-415 | amended | DEC-500 | — | Part 11.1b §11.1.7 Decisions (L842) | Also: DEC-580, DEC-770. Extends DEC-415 |
| 94 | DEC-418 | amended | DEC-788 | — | Part 11.14 §11.14.1 (DEC-788) | Claude Sonnet stays primary by approval through the provider-neutral model registry |
| 95 | DEC-421 | amended | DEC-772 | DEC-778 DEC-786 DEC-776 | Part 11.14 §11.14.1 (DEC-772, DEC-778, DEC-786) | Hosting stays Vercel + Supabase + AWS; adds EU stack (DEC-772), roadmap regions (DEC-776); service-key wording withdrawn (DEC-778, roles DEC-894); pe… |
| 96 | DEC-422 | amended | DEC-771 | DEC-772 DEC-773 DEC-774 | Part 11.14 §11.14.1 | Running-cost lines added: PITR and standby (DEC-771), EU stack (DEC-772), 24x7 on-call (DEC-773), Enterprise SLA uplift (DEC-774) |
| 97 | ENT-161 | amended | DEC-564 | — | Part 11.4d §11.4.7 Decisions (L1783) | Amends ADR-028 wording, AU-028 and Part 3.3 ENT-161 |
| 98 | ENT-162 | amended | DEC-561 | — | Part 11.4d §11.4.7 Decisions (L1780) | Amends Part 2.3 §2.27.14 and Part 3.3 ENT-162/163 state CHECKs |
| 99 | ENT-181 | amended | DEC-584 | — | Part 11.5b §11.5.9.2 Inconsistencies found in earlier parts… | / 4 / Part 3.3 ENT-181 / Entitlement has meter dimension only; no SKU dimension / Add `saas_sku_grant` (DEC-584) / |
| 100 | ENT-182 | amended | DEC-585 | — | Part 11.5b §11.5.7 Decisions (L968) | Amends ENT-182 state set and §2.27.18 |
| 101 | ENT-183 | amended | DEC-586 | — | Part 11.5b §11.5.7 Decisions (L969) | Also: DEC-661. Amends ENT-183 role |
| 102 | ENT-184 | amended | DEC-587 | — | Part 11.5b §11.5.7 Decisions (L970) | Amends ENT-184/185 money types; |
| 103 | ENT-189 | amended | DEC-673 | — | Part 11.9c §11.9.7 Decisions (L301) | Part 3.3 ENT-189 extended |
| 104 | FR-A113 | amended | DEC-569 | — | Part 11.4d §11.4.7 Decisions (L1788) | Amends A113 template semantics (FR-A113) |
| 105 | FR-ENH-H-006 | amended | DEC-685 | — | Part 11.10b §11.10.4.1 Archived registers in FSD V12 chapte… | Chapter 40 lists every archived row of source documents D22 (tests), D23 (QCs) and D20 (work items) with the disposition "pending semantic mapping",… |
| 106 | FR-ENH-J-019 | amended | DEC-771 | — | Part 6.6 L1027 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 107 | FR-NEG-01 | amended | DEC-783 | — | Part 2.1 L402 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 108 | FR-W01 | amended | DEC-621 | — | Part 11.7c §11.7.7 Decisions (L737) | Amends Part 2.5 §2.43.1–2.43.3 and the FR-W01…W34 key fields; |
| 109 | FR-W02 | amended | DEC-505 | — | Part 11.1b §11.1.7 Decisions (L847) | Amends FR-W02, FR-W03, API-497, US-1905 (CONFLICT-764) |
| 110 | FR-W03 | amended | DEC-505 | — | Part 11.1b §11.1.7 Decisions (L847) | Amends FR-W02, FR-W03, API-497, US-1905 (CONFLICT-764) |
| 111 | FR-W31 | amended | DEC-783 | — | Part 2.1 L207 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 112 | KPI-25 | amended | DEC-519 | — | Part 11.1b §11.1.7 Decisions (L861) | Extends KPI-25 and CSO-06/07 |
| 113 | NFR-057 | amended | DEC-771 | — | Part 4.2 L106 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 114 | NFR-ADV-X3-10 | amended | DEC-701 | — | Part 11.11b §11.11.7 Decisions (L792) | the single communication matrix of §11.11.5.3 supersedes the differing notice targets of Part 4.3 §4.43.1/4.43.4, Part 8.3c SLA-09 and Part 9.9a NFR-… |
| 115 | NFR-ENH-B-06 | amended | DEC-771 | — | Part 3.4 L720 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 116 | OKPI-19 | amended | DEC-771 | — | Part 8.3c L573 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 117 | OKPI-32 | amended | DEC-771 | — | Part 11.14 §11.14.1 (DEC-771) | Growth-critical RTO <= 120 min becomes a release-blocking gate (was CONFLICT-462/444) |
| 118 | RSK-028 | amended | DEC-772 | — | Part 8.2 L62 (baseline row) | Read with DEC-772: India (Mumbai) and EU residency stacks; further regions per DEC-776 when their rule pack is approved |
| 119 | RSK-304 | amended | DEC-772 | — | Part 3.1 L1777 (baseline row) | Read with DEC-772: India (Mumbai) and EU residency stacks; further regions per DEC-776 when their rule pack is approved |
| 120 | RSK-342 | amended | DEC-772 | — | Part 4.2 L427 (baseline row) | Read with DEC-772: India (Mumbai) and EU residency stacks; further regions per DEC-776 when their rule pack is approved |
| 121 | A001 | amended | DEC-707 | — | Part 11.11a §11.11.4.2 Operational training register TRN-00… | Also: DEC-500, DEC-623, DEC-642, DEC-721, DEC-801. The customer register has one row per retained screen (W01–W30, A001–A108). Each row was matched b… |
| 122 | A002 | amended | DEC-783 | A197 A203 | Part 11.22b §US-01-ZU01 Product separation between Sales &… | Also: DEC-620, DEC-941. / Notes / Wording amended by DEC-783: investor entities exist only in the separate Investment Automation product code; the se… |
| 123 | A007 | amended | DEC-941 | A201 A202 | Part 11.22b §US-03-ZU01 Deny-reason precedence in the V12 o… | / Notes / Acceptance binding: US-03-YE01 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the t… |
| 124 | A008 | amended | DEC-941 | — | Part 11.22c §US-20-ZU28 Invoice preview with per-line tax d… | Also: DEC-620, DEC-785. / Notes / Acceptance binding: US-20-YH01 carries the statement and its build points; this story adds the Gherkin AC, the gene… |
| 125 | A009 | amended | DEC-783 | A197 A203 | Part 11.22b §US-01-ZU01 Product separation between Sales &… | Also: DEC-620, DEC-941. / Notes / Wording amended by DEC-783: investor entities exist only in the separate Investment Automation product code; the se… |
| 126 | A011 | amended | DEC-941 | A198 | Part 11.22b §US-03-ZU08 AI-assisted labelling of every Part… | Also: DEC-785. / Notes / Acceptance binding: US-03-YM38 carries the statement and its build points; this story adds the Gherkin AC, the generated Exa… |
| 127 | A012 | amended | DEC-941 | A198 | Part 11.22b §US-03-ZU08 AI-assisted labelling of every Part… | Also: DEC-620. / Notes / Acceptance binding: US-03-YM38 carries the statement and its build points; this story adds the Gherkin AC, the generated Exa… |
| 128 | A013 | amended | DEC-941 | A201 A202 | Part 11.22b §US-03-ZU01 Deny-reason precedence in the V12 o… | / Notes / Acceptance binding: US-03-YE01 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the t… |
| 129 | A014 | amended | DEC-941 | A190 | Part 11.22c §US-20-ZU11 BR-V12 capability register (1/3): i… | / Notes / Acceptance binding: US-20-YA08 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the t… |
| 130 | A042 | amended | DEC-893 | — | Part 11.19 (DEC-893) | Benchmarks tab added (opt-in, step-up); screen otherwise unchanged |
| 131 | A045 | amended | DEC-837 | — | Part 11.16 (DEC-837) | Legacy route not used for issuer publication; Sales & Marketing use unchanged |
| 132 | A046 | amended | DEC-837 | — | Part 11.16 (DEC-837) | Legacy route not used for issuer publication; Sales & Marketing use unchanged |
| 133 | A049 | amended | DEC-801 | A205 A232 A194 | Part 11.16a §11.16.4.5 Technical Map (42 rows): admin scree… | **Screen ID rule (DEC-801).** Investment admin IDs collide with the Sales & Marketing A001–A113; they are re-identified A205–A232 and keep the INV ID… |
| 134 | A087 | amended | DEC-941 | A191 | Part 11.22b §US-17-ZU01 Native-currency integrity and recon… | Also: DEC-770. / Notes / Acceptance binding: US-17-YA02 carries the statement and its build points; this story adds the Gherkin AC, the generated Exa… |
| 135 | A089 | amended | DEC-509 | — | Part 11.1a §11.1.3.19 Chapter 19: Portfolio Command Centre… | Also: DEC-623, DEC-770, DEC-941. / A-19-0680 / Nine optimization views: A089 keeps its fourteen business management views; V5 adds nine integrated op… |
| 136 | A090 | amended | DEC-941 | A190 | Part 11.22c §US-20-ZU11 BR-V12 capability register (1/3): i… | / Notes / Acceptance binding: US-20-YA08 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the t… |
| 137 | A099 | amended | DEC-783 | A197 A203 | Part 11.22b §US-01-ZU01 Product separation between Sales &… | Also: DEC-941. / Notes / Wording amended by DEC-783: investor entities exist only in the separate Investment Automation product code; the separation… |
| 138 | A101 | amended | DEC-941 | A184 A188 | Part 11.22b §US-15-ZU01 Distinct ledgers, native-currency r… | Also: DEC-620. / Notes / Acceptance binding: US-15-YE01 carries the statement and its build points; this story adds the Gherkin AC, the generated Exa… |
| 139 | A102 | amended | DEC-941 | A192 A195 | Part 11.22c §US-18-ZU03 Circuit breakers, backpressure and… | / Notes / Acceptance binding: US-18-YE02 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the t… |
| 140 | A103 | amended | DEC-620 | — | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | / G-F22-0005 / A126 Data export, portability & encryption keys — audience Tenant; requirements ENT-DAT-01, 02 / Partially covered / Blueprint A103 (a… |
| 141 | A106 | amended | DEC-941 | A191 | Part 11.22b §US-17-ZU01 Native-currency integrity and recon… | Also: DEC-770. / Notes / Acceptance binding: US-17-YA02 carries the statement and its build points; this story adds the Gherkin AC, the generated Exa… |
| 142 | A107 | amended | DEC-622 | — | Part 11.7c §11.7.7 Decisions (L738) | Also: DEC-536, DEC-621. A107 renamed "Tenant-owned website intake configuration"; |
| 143 | A108 | amended | DEC-622 | — | Part 11.7c §11.7.7 Decisions (L738) | Also: DEC-536, DEC-621, DEC-707. A108 renamed "Tenant-owned landing page review & intake analytics" |
| 144 | A109 | amended | DEC-707 | — | Part 11.11a §11.11.4.2 Operational training register TRN-00… | Also: DEC-941. The customer register has one row per retained screen (W01–W30, A001–A108). Each row was matched by script to the Part 8.3b card `TRN-… |
| 145 | A113 | amended | DEC-569 | — | Part 11.4d §11.4.7 Decisions (L1788) | Also: DEC-642, DEC-707, DEC-721, DEC-801, DEC-941. Amends A113 template semantics (FR-A113) |
| 146 | A114 | amended | DEC-620 | — | Part 11.7c §11.7.7 Decisions (L736) | Also: DEC-619. V12 screen IDs that collide with blueprint IDs (A114–A131, W35–W41) are kept as qualified aliases `V12-<ID>`; |
| 147 | A115 | amended | DEC-619 | — | Part 11.6a §11.6.3.1 Partially covered, not covered and con… | Also: DEC-620. / F16-089 / 16 · 16.8 / UI mapping: Admin A114 model registry, A115 evaluation, A116 injection defence, A117 cost per tenant; Website… |
| 148 | A116 | amended | DEC-619 | — | Part 11.6a §11.6.3.1 Partially covered, not covered and con… | Also: DEC-620. / F16-089 / 16 · 16.8 / UI mapping: Admin A114 model registry, A115 evaluation, A116 injection defence, A117 cost per tenant; Website… |
| 149 | A117 | amended | DEC-619 | — | Part 11.6a §11.6.3.1 Partially covered, not covered and con… | Also: DEC-620. / F16-089 / 16 · 16.8 / UI mapping: Admin A114 model registry, A115 evaluation, A116 injection defence, A117 cost per tenant; Website… |
| 150 | A118 | amended | DEC-620 | — | Part 11.7a §Register F24: FSD ch24 UI/UX master (prose, MOB… | / G-F24-0054 / A118 Jurisdiction policy packs & send preflight (Compliance) audiences Operator, automation ops, tenant; interactions Rule register wi… |
| 151 | A119 | amended | DEC-620 | A201 | Part 11.7a §Register F24: FSD ch24 UI/UX master (prose, MOB… | / G-F24-0055 / A119 Consent & suppression ledger (Compliance) audiences Tenant, automation ops; interactions Search, withdrawal → suppression → held… |
| 152 | A120 | amended | DEC-620 | — | Part 11.7a §Register F24: FSD ch24 UI/UX master (prose, MOB… | / G-F24-0056 / A120 Data-rights requests (DSAR) (Compliance) audiences Tenant (act), operator (view); interactions Due dates, identity verification,… |
| 153 | A121 | amended | DEC-500 | — | Part 11.1a §11.1.3.AP Chapter AP: Appendix: ID index (L884) | Also: DEC-620, DEC-623. / A-AP-1306 / ID family: Website route / Admin screen / Format / range: W01…W36 / A001…A121, X26…X39, O01…O08 / Where: ch12,… |
| 154 | A122 | amended | DEC-620 | A203 | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | / G-F22-0001 / A122 Identity, SSO, SCIM & MFA — audience Tenant (manage), operator (state only); requirements ENT-IDN-01…06 / Not covered / Blueprint… |
| 155 | A123 | amended | DEC-620 | — | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | / G-F22-0002 / A123 Custom roles & separation of duties — audience Tenant; requirements ENT-ACC-01, 02 / Partially covered / Blueprint A002 (alias);… |
| 156 | A124 | amended | DEC-620 | — | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | / G-F22-0003 / A124 Audit log & SIEM export — audience Tenant, operator; requirements ENT-ACC-03, 04 / Partially covered / Blueprint A009 (alias); V1… |
| 157 | A125 | amended | DEC-620 | — | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | / G-F22-0004 / A125 API keys & webhooks — audience Tenant; requirements ENT-API-01, 05 / Partially covered / Blueprint A168 (alias); V12 ID collides… |
| 158 | A126 | amended | DEC-620 | — | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | / G-F22-0005 / A126 Data export, portability & encryption keys — audience Tenant; requirements ENT-DAT-01, 02 / Partially covered / Blueprint A103 (a… |
| 159 | A127 | amended | DEC-620 | — | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | / G-F22-0006 / A127 Sandbox environments — audience Tenant; requirements ENT-DAT-04, 05 / Not covered / Blueprint A204 (new); V12 ID collides with Pa… |
| 160 | A128 | amended | DEC-941 | A198 | Part 11.22b §US-03-ZU08 AI-assisted labelling of every Part… | Also: DEC-619, DEC-620, DEC-649. / Notes / Acceptance binding: US-03-YM38 carries the statement and its build points; this story adds the Gherkin AC,… |
| 161 | A129 | amended | DEC-620 | — | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | Also: DEC-639. / G-F22-0008 / A129 Trust, certification & vulnerability programme — audience Operator (manage), tenant (read); requirements ENT-SEC-0… |
| 162 | A130 | amended | DEC-620 | — | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | / G-F22-0009 / A130 Reliability, incidents & status page — audience Operator, automation ops, tenant (read); requirements ENT-OPS-01…04, 07 / Partial… |
| 163 | A131 | amended | DEC-620 | — | Part 11.7c §11.7.7 Decisions (L736) | V12 screen IDs that collide with blueprint IDs (A114–A131, W35–W41) are kept as qualified aliases `V12-<ID>`; |
| 164 | A156 | amended | DEC-941 | A190 | Part 11.22c §US-20-ZU11 BR-V12 capability register (1/3): i… | Also: DEC-620. / Notes / Acceptance binding: US-20-YA08 carries the statement and its build points; this story adds the Gherkin AC, the generated Exa… |
| 165 | A159 | amended | DEC-941 | A190 | Part 11.22c §US-20-ZU11 BR-V12 capability register (1/3): i… | Also: DEC-620, DEC-639. / Notes / Acceptance binding: US-20-YA08 carries the statement and its build points; this story adds the Gherkin AC, the gene… |
| 166 | A163 | amended | DEC-620 | — | Part 11.7a §Register F24: FSD ch24 UI/UX master (prose, MOB… | / G-F24-0056 / A120 Data-rights requests (DSAR) (Compliance) audiences Tenant (act), operator (view); interactions Due dates, identity verification,… |
| 167 | A168 | amended | DEC-941 | — | Part 11.22c §US-20-ZU28 Invoice preview with per-line tax d… | Also: DEC-620, DEC-785. / Notes / Acceptance binding: US-20-YH01 carries the statement and its build points; this story adds the Gherkin AC, the gene… |
| 168 | A199 | amended | DEC-941 | A198 | Part 11.22b §US-03-ZU08 AI-assisted labelling of every Part… | Also: DEC-620. / Notes / Acceptance binding: US-03-YM38 carries the statement and its build points; this story adds the Gherkin AC, the generated Exa… |
| 169 | A200 | amended | DEC-941 | A201 A202 | Part 11.22b §US-03-ZU01 Deny-reason precedence in the V12 o… | Also: DEC-620. / Notes / Acceptance binding: US-03-YE01 carries the statement and its build points; this story adds the Gherkin AC, the generated Exa… |
| 170 | A204 | amended | DEC-941 | — | Part 11.22c §US-20-ZU28 Invoice preview with per-line tax d… | Also: DEC-620, DEC-785. / Notes / Acceptance binding: US-20-YH01 carries the statement and its build points; this story adds the Gherkin AC, the gene… |
| 171 | W01 | amended | DEC-707 | — | Part 11.11a §11.11.4.2 Operational training register TRN-00… | Also: DEC-500, DEC-620, DEC-621, DEC-623, DEC-642, DEC-721. The customer register has one row per retained screen (W01–W30, A001–A108). Each row was… |
| 172 | W02 | superseded | DEC-621 | W54 | Part 11.7a §11.7.1.3 What V12 changes in the UI (headline)… | / 1 / Website becomes a **neutral SaaS storefront**: 34 route IDs kept, names and purpose replaced (for example W02 "Company and startup business dir… |
| 173 | W03 | amended | DEC-621 | W54 | Part 11.7c §11.7.6 Conflicts and proposed resolutions (L727) | / CONFLICT-873 / **Neutral storefront replaces the portfolio public website** / W01–W34 re-purposed; client names, profiles, products and published s… |
| 174 | W04 | amended | DEC-621 | W54 | Part 11.7c §11.7.6 Conflicts and proposed resolutions (L727) | / CONFLICT-873 / **Neutral storefront replaces the portfolio public website** / W01–W34 re-purposed; client names, profiles, products and published s… |
| 175 | W05 | amended | DEC-621 | W54 | Part 11.7c §11.7.6 Conflicts and proposed resolutions (L727) | / CONFLICT-873 / **Neutral storefront replaces the portfolio public website** / W01–W34 re-purposed; client names, profiles, products and published s… |
| 176 | W12 | amended | DEC-621 | W54 | Part 11.7c §11.7.6 Conflicts and proposed resolutions (L727) | / CONFLICT-873 / **Neutral storefront replaces the portfolio public website** / W01–W34 re-purposed; client names, profiles, products and published s… |
| 177 | W17 | amended | DEC-621 | W54 | Part 11.7c §11.7.6 Conflicts and proposed resolutions (L727) | / CONFLICT-873 / **Neutral storefront replaces the portfolio public website** / W01–W34 re-purposed; client names, profiles, products and published s… |
| 178 | W20 | amended | DEC-621 | W54 | Part 11.7c §11.7.6 Conflicts and proposed resolutions (L727) | / CONFLICT-873 / **Neutral storefront replaces the portfolio public website** / W01–W34 re-purposed; client names, profiles, products and published s… |
| 179 | W29 | amended | DEC-941 | A201 A202 | Part 11.22b §US-03-ZU01 Deny-reason precedence in the V12 o… | / Notes / Acceptance binding: US-03-YE01 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the t… |
| 180 | W30 | amended | DEC-707 | — | Part 11.11a §11.11.4.2 Operational training register TRN-00… | Also: DEC-941. The customer register has one row per retained screen (W01–W30, A001–A108). Each row was matched by script to the Part 8.3b card `TRN-… |
| 181 | W31 | amended | DEC-707 | — | Part 11.11a §11.11.4.2 Operational training register TRN-00… | Also: DEC-783, DEC-941. The customer register has one row per retained screen (W01–W30, A001–A108). Each row was matched by script to the Part 8.3b c… |
| 182 | W34 | amended | DEC-621 | — | Part 11.7c §11.7.7 Decisions (L737) | Also: DEC-642, DEC-707, DEC-721, DEC-941. Amends Part 2.5 §2.43.1–2.43.3 and the FR-W01…W34 key fields; |
| 183 | W35 | amended | DEC-620 | — | Part 11.7c §11.7.7 Decisions (L736) | V12 screen IDs that collide with blueprint IDs (A114–A131, W35–W41) are kept as qualified aliases `V12-<ID>`; |
| 184 | W36 | amended | DEC-500 | — | Part 11.1a §11.1.3.AP Chapter AP: Appendix: ID index (L884) | Also: DEC-619, DEC-620, DEC-623. / A-AP-1306 / ID family: Website route / Admin screen / Format / range: W01…W36 / A001…A121, X26…X39, O01…O08 / Wher… |
| 185 | W37 | amended | DEC-620 | W51 | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | / G-F22-0011 / W37 Enterprise capabilities — audience Public; requirements BR-V12-01…05 / Not covered / Blueprint W51 (new); V12 ID collides with Par… |
| 186 | W38 | amended | DEC-620 | — | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | Also: DEC-639. / G-F22-0012 / W38 Trust centre — audience Public; requirements ENT-CMP-01…06, ENT-SEC-05 / Partially covered / Blueprint W46 (alias);… |
| 187 | W39 | amended | DEC-620 | — | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | Also: DEC-646. / G-F22-0013 / W39 Developers & API — audience Public; requirements ENT-API-04, 06, 07 / Partially covered / Blueprint W47 (alias); V1… |
| 188 | W40 | amended | DEC-620 | — | Part 11.7a §Register F22: FSD ch22 Platform operator (27 as… | / G-F22-0014 / W40 System status — audience Public; requirements ENT-OPS-02, 03 / Partially covered / Blueprint W45 (alias); V12 ID collides with Par… |
| 189 | W41 | amended | DEC-620 | — | Part 11.7c §11.7.7 Decisions (L736) | V12 screen IDs that collide with blueprint IDs (A114–A131, W35–W41) are kept as qualified aliases `V12-<ID>`; |
| 190 | W45 | amended | DEC-941 | W54 | Part 11.22b §US-16-ZU02 First-value milestone, activation c… | Also: DEC-620. / Notes / Acceptance binding: US-16-YA01 carries the statement and its build points; this story adds the Gherkin AC, the generated Exa… |
| 191 | W46 | amended | DEC-941 | A190 | Part 11.22c §US-20-ZU11 BR-V12 capability register (1/3): i… | Also: DEC-620, DEC-639. / Notes / Acceptance binding: US-20-YA08 carries the statement and its build points; this story adds the Gherkin AC, the gene… |
| 192 | W47 | amended | DEC-941 | — | Part 11.22c §US-20-ZU28 Invoice preview with per-line tax d… | Also: DEC-620, DEC-785. / Notes / Acceptance binding: US-20-YH01 carries the statement and its build points; this story adds the Gherkin AC, the gene… |
| 193 | W49 | amended | DEC-620 | — | Part 11.7a §Register F24: FSD ch24 UI/UX master (prose, MOB… | / G-F24-0058 / W35 Privacy & data-rights request (Website) audiences Public; interactions Request form with inline validation; reference and due date… |
| 194 | TC-03-009 | amended | DEC-777 | — | Part 6.5 L764 (baseline row) | Read with DEC-777: Promotional window is now 09:00-21:00 recipient local time unless a rule pack is stricter |
| 195 | TC-18-025 | amended | DEC-779 | — | Part 6.3a L854 (baseline row) | Read with DEC-779: L1 cap lifted only for actions under an Active, eligible bounded mandate in an approved jurisdiction (DEC-841) |
| 196 | TC-21-068 | amended | DEC-771 | — | Part 6.3b L642 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 197 | TC-21-091 | amended | DEC-771 | — | Part 6.3b L684 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 198 | TC-21-092 | amended | DEC-771 | — | Part 6.3b L685 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 199 | TC-AI-AG030-003 | amended | DEC-783 | — | Part 6.4 L1657 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 200 | TC-ALN-A-021 | amended | DEC-783 | — | Part 9.6a L1387 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 201 | TC-ALN-A-022 | amended | DEC-783 | — | Part 9.6a L1388 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 202 | TC-ALN-B-013 | amended | DEC-771 | — | Part 9.6b L1513 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 203 | TC-AU-AU005-003 | amended | DEC-779 | — | Part 6.4 L2415 (baseline row) | Read with DEC-779: L1 cap lifted only for actions under an Active, eligible bounded mandate in an approved jurisdiction (DEC-841) |
| 204 | TC-BRS-002 | amended | DEC-783 | — | Part 6.7 L449 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 205 | TC-ENH-A-001 | amended | DEC-783 | — | Part 2.6 L1736 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 206 | TC-ENH-B-032 | amended | DEC-782 | — | Part 3.4 L1686 (baseline row) | Read with DEC-782: AI voice and recordings adopted with AI disclosure, consent, calling windows and retention controls (Part 11.18) |
| 207 | TC-ENH-C-020 | amended | DEC-783 | — | Part 2.7a L936 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 208 | TC-ENH-D-C06 | amended | DEC-783 | — | Part 3.5b L1640 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 209 | TC-ENH-E-017 | amended | DEC-771 | — | Part 3.6b L805 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 210 | TC-ENH-G-038 | amended | DEC-771 | — | Part 6.8c L174 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 211 | TC-ENH-J-018 | amended | DEC-771 | — | Part 8.3c L623 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 212 | TC-ENH-K-022 | amended | DEC-782 | — | Part 6.10 L100 (baseline row) | Read with DEC-782: AI voice and recordings adopted with AI disclosure, consent, calling windows and retention controls (Part 11.18) |
| 213 | TC-NFR-057 | amended | DEC-771 | — | Part 6.7 L179 (baseline row) | Read with DEC-771: Growth RTO <= 120 min is release-blocking; RPO <= 15 min (DEC-787) |
| 214 | US-0101 | amended | DEC-783 | — | Part 8.1 L337 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 215 | US-0114 | amended | DEC-783 | — | Part 5.1b L846 (baseline row) | Read with DEC-783: Investor/fundraising adopted with securities rule packs (Parts 11.16a-e) |
| 216 | US-09-EB01 | amended | DEC-782 | — | Part 3.4 L1526 (baseline row) | Read with DEC-782: AI voice and recordings adopted with AI disclosure, consent, calling windows and retention controls (Part 11.18) |
| 217 | US-1905 | amended | DEC-505 | — | Part 11.1b §11.1.7 Decisions (L847) | Amends FR-W02, FR-W03, API-497, US-1905 (CONFLICT-764) |
| 218 | US-21-EH01 | amended | DEC-785 | — | Part 11.22c §US-21-ZU19 ENT-INT-05 acceptance: connector ac… | / Notes / FR-V12-K-128: release per DEC-785 (developer platform and connectors in Release 1) · Acceptance binding: US-21-EH01 carries the statement a… |
| 219 | WF-01 | amended | DEC-560 | — | Part 11.4d §11.4.7 Decisions (L1779) | blueprint WF-01…39 remain end-to-end journeys mapped in §11.4.4.1 |
| 220 | WF-10 | amended | DEC-579 | — | Part 11.4d §11.4.7 Decisions (L1798) | Extends WF-10 and the OrganicSpec route (BR-S004) |

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
| Baseline IDs referenced but never defined by a row or heading | 958 strings; after review all are prefixes, placeholders or reserved-unused numbers, not lost requirements: family stubs (`US-08XX`, `BRL-X3`, `RSK-ADV-X1`, `KPI-ADV-X2`, …), source-numbered FRD/test aliases (`FR-001…`, `TC-01-A…`), reserved and unused numbers (DEC-271…299 and DEC-333…379 stated unused in Parts 9.6a/b; WF-24 and WF-40 stated unused in Part 9.10; ADR-044…049 allocation line), and SIT aliases read as screens (`A280`, `A302` from `SM-SIT-A280/A302`) | none |
| Placeholders never resolved | `ENT-200…203` ("final ENT numbers to be assigned by the coordinator", Part 3.6a/9.5) and `API-556+` ("the coordinator may renumber them into API-556+", Part 3.5b) were never assigned; the entities and operations live on as `ENT-ENH-*` and `API-ENH-*` | **DEC-967**: the ENH IDs are canonical; no renumbering; [GAP-1183] closed |

**Conclusion.** No baseline ID was lost in the V12 revision. The retention risk is not loss but **silent contradiction**: 220 baseline IDs (and many more sentences) still read as before while a later decision changed them. That is why every amended and superseded ID is listed above with its authority, and why Part 11.23c turns each stale statement into an erratum with the current rule.

### 11.23.6.7 Supersession index file

`final/supersession_index.csv` has one row per baseline ID (10,569 rows):

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
