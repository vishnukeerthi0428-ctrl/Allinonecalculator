# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.23c), Independent Completeness Audit (V12 → Blueprint) and Baseline Retention Check — C. Cross-Part Errata, Conflicts, Decisions and Quality Gate

| Field | Value |
|---|---|
| Document | Part 11.23c: one erratum per stale statement pattern found across the parts, with the binding current rule; conflicts; decisions DEC-960…970; expert review; tags register; quality gate |
| Version | 1.0 · 28 Nov 2026 |
| Precedence | Part 11.14 (Founder decisions) > **these errata** (they only restate decided rules) > Parts 11.1–11.22 > Part 9.10 > earlier parts (DEC-961, extending DEC-415/500) |
| Roles applied | Configuration-management and baseline-integrity lead · Forensic requirements auditor · Principal Business Systems Analyst · Security, data and AI-governance reviewers |

---

## 11.23.7 Cross-part consistency: errata

### 11.23.7.1 Method

1. **Collect.** Every "Inconsistencies found in earlier parts" section of Parts 11.1–11.22 was read (Parts 11.2c, 11.3c, 11.4a, 11.4d, 11.5b, 11.6b, 11.7c, 11.8b, 11.9c, 11.10c, 11.11b, 11.12, 11.17b, 11.18d, 11.19c), plus the known issues named in the task (L1 cap, service key, role names, AWS-only topology, PostgreSQL 17/RDS, screen-ID clashes, RTO/RPO, region count, EP-22 vs EP-08, `eng_call` vs `voice_session`, CP-O-04/DEC-822 vs DEC-779).
2. **Find more.** The audit's own scans added stale patterns: the safety envelope sentence ("never pays, submits bids"), customer decision IDs written `DEC-Vn-##`, V12 KPI IDs without the OKPI alias, V12 `REC-##` against blueprint REC-01…09, the 09:00–19:00 window, business-hours support, investor exclusion, voice/SMS prohibition, fixed release dates, "Pending Founder decision" labels left after DEC-791, the stale "A205–A259 reserved and unused" note and Group P's provisional screen range.
3. **Measure.** `v_20_errata.py` counts every line that matches each stale pattern in every part. A line that already names the superseding authority (or says superseded/withdrawn/amended) is **annotated**; otherwise it is **stale** and could mislead a developer. `v_21_screen_clash.py` checks that no screen ID is *defined* with two different names in two parts (result: 0 definition clashes; the V12/blueprint clash is a numbering clash handled by aliases).
4. **Write the erratum.** One entry per pattern: the stale statement, the binding current rule, the authority, the count and first locations, and a developer instruction. The parts themselves are not edited (task boundary); the erratum governs (DEC-961) and FR-V12-V-009 keeps the count from growing.

### 11.23.7.2 Errata summary

47 errata; 1,667 stale line occurrences across the parts (full list with part, line and text: `assembly/v12b/v_out/errata_occurrences.csv`).

| Erratum | Stale statement | Occurrences (stale / total) | Parts with stale text | Authority |
|---|---|---|---|---|
| E-V-01 | Consequential actions always capped at L1 | 42 / 56 | 0, 11.11a, 11.12, 11.13a, 11.13b, 11.17a, 11.1b, 11.2a, 11.3c, 11.4c … | DEC-779, DEC-841, DEC-883 |
| E-V-02 | Safety envelope "AI never signs, pays, submits bids, sets prices" | 31 / 44 | 0, 0A, 11.11a, 11.12, 11.13a, 11.1a, 11.1b, 11.2b, 11.2c, 11.3c … | DEC-779, DEC-780, DEC-781 |
| E-V-03 | "Service key held server-side" for the Django API | 3 / 8 | 11.8b, 11.9b, 11.9c | DEC-778, DEC-894 (ADR-264) |
| E-V-04 | Database role names `ge_app` / `ge_worker` / `ge_owner` / `app_user` | 35 / 50 | 11.19a, 11.19b, 11.9a, 11.9b, 11.9c, 3.3 | DEC-778, DEC-894 |
| E-V-05 | AWS-only topology (RDS, CloudFront, RDS cross-Region backups) | 30 / 34 | 11.1b, 3.1, 3.2, 3.3, 5.1b, 6.5, 8.4, 9.10, 9.2, 9.6a … | DEC-421, DEC-772, DEC-786 |
| E-V-06 | PostgreSQL 17 on Amazon RDS | 4 / 5 | 3.1, 3.3, 9.2 | DEC-421, DEC-772 |
| E-V-07 | V12 screen IDs used bare where they collide with blueprint IDs | 15 / 26 | 11.10a, 11.10c, 11.19a, 11.6a, 11.6b, 11.7a | DEC-620, DEC-700, DEC-801, DEC-962 |
| E-V-08 | Screen range A205–A259 / W55–W99 "reserved and unused" | 1 / 1 | 11.7c | DEC-801, DEC-962 |
| E-V-09 | RTO 4 h at pilot / staged RTO | 60 / 77 | 0, 0A, 11.10c, 11.12, 11.1a, 11.1b, 11.22a, 3.1, 3.2, 3.3 … | DEC-771, DEC-787, CDEC-V9-01 |
| E-V-10 | Single-region pilot / region count | 25 / 25 | 11.1a, 11.1b, 11.5a, 11.5b, 11.6b, 11.9a, 11.9c, 3.1, 4.2, 8.2 … | DEC-772, DEC-776 |
| E-V-11 | SM-SVC-26 voice assigned to EP-08 | 2 / 4 | 11.4c, 11.7b | Part 11.2a; Part 11.18d |
| E-V-12 | Voice domain named `eng_call` | 3 / 17 | 11.18a, 11.4c, 11.4d | Part 11.18d (V12 canonical) |
| E-V-13 | Mandates and securities-governed investment actions | 1 / 1 | 11.14 | DEC-779 (lawful condition), DEC-783, DEC-822, DEC-963 |
| E-V-14 | Customer decision IDs written DEC-Vn-## / DEC-### for V12 decisions | 149 / 155 | 11.10c, 11.12, 11.14, 11.18a, 11.19a, 11.19b, 11.1a, 11.1b, 11.22a, 11.5a … | DEC-700 |
| E-V-15 | V12 KPI-## used without the OKPI alias | 26 / 32 | 11.14, 11.22a, 11.9a, 11.9c | DEC-681 |
| E-V-16 | V12 REC-01…30 collide with blueprint reconciliation jobs REC-01…09 | 193 / 196 | 11.11a, 11.11b, 11.12, 11.13a, 11.13b, 11.15e, 11.18a, 11.18b, 11.18c, 11.18d … | DEC-964 |
| E-V-17 | Messaging window 09:00–19:00 Mon–Sat | 25 / 28 | 11.11a, 11.11b, 11.15a, 11.15d, 11.15e, 2.3, 5.1a, 5.1b, 5.2, 6.1 … | DEC-777 |
| E-V-18 | Business-hours support | 4 / 5 | 0, 11.11b, 9.1, 9.2 | DEC-773 |
| E-V-19 | Investor / fundraising exclusion | 38 / 40 | 0, 1, 11.12, 11.16a, 11.16b, 11.16d, 11.7c, 11.8a, 11.8b, 2.6 … | DEC-783 |
| E-V-20 | Voice / recording / SMS prohibited | 13 / 13 | 11.15e, 11.2c, 11.7b | DEC-782, DEC-785, DEC-884 |
| E-V-21 | Automatic bid submission prohibited | 23 / 26 | 11.12, 11.13a, 11.15c, 11.1b, 11.2a, 11.2b, 11.2c, 11.3c, 11.5a, 3.5b … | DEC-781, DEC-851, DEC-852 |
| E-V-24 | Tier 2 free providers described as an active fallback chain | 1 / 1 | 11.6b | DEC-788 |
| E-V-25 | Fixed release dates as commitments | 53 / 53 | 11.11a, 11.11b, 11.5b, 11.8b, 9.10, 9.2, 9.5 | DEC-770 |
| E-V-26 | Judge agreement ≥ 85% vs κ ≥ 0.8 | 4 / 6 | 6.4, 7.2, 9.7b | DEC-603 |
| E-V-27 | Admin not targeted below 768 px | 7 / 9 | 0A, 2.7a, 5.3, 6.1, 9.2 | DEC-623 |
| E-V-28 | Outbound webhooks not offered | 5 / 6 | 11.8a, 9.2, 9.9a, 9.9b | DEC-645, DEC-785 |
| E-V-29 | Benchmarks disabled / ε = 1 | 3 / 4 | 11.13b, 11.19c | DEC-789, DEC-893 |
| E-V-30 | Voice transport "R3+ → W6" | 1 / 2 | 11.8b | DEC-785, DEC-884 |
| E-V-31 | Missing tenant context returns zero rows | 0 / 2 | — | CONFLICT-909 resolution (Part 11.9c) |
| E-V-32 | BYOK limited to AWS KMS | 2 / 2 | 11.11a, 11.11b | DEC-776 |
| E-V-33 | Money stored as numeric(18,2) | 24 / 30 | 3.3, 3.6a, 3.6b | DEC-587 |
| E-V-34 | Run-state vocabularies differ | 0 / 1 | — | DEC-561 |
| E-V-35 | Workflow catalogue titled WF-01…39 / WF-01 to WF-14 | 4 / 5 | 11.13a, 9.2, 9.4 | Part 9.10; Part 11.4d |
| E-V-36 | Side-effect classes R0/W1/X2 vs none/internal/external | 2 / 3 | 11.6a | DEC-570, DEC-965 |
| E-V-37 | SEV1 notice targets differ | 1 / 3 | 4.3 | DEC-701 |
| E-V-38 | Status page "Not defined [GAP-126]" | 0 / 1 | — | DEC-406, DEC-703 |
| E-V-39 | Effort 287–483 pd / ₹13.05–32.93 lakh as current budget | 48 / 54 | 0, 0A, 1, 2.6, 2.7a, 3.4, 4.4b, 5.1a, 5.1c, 5.2 … | DEC-228, DEC-230, DEC-770, DEC-790 |
| E-V-40 | IdP: one connection per tenant | 0 / 1 | — | DEC-784; FR-V12-R-029 |
| E-V-41 | API catalogue count 579 only | 2 / 2 | 11.1a, 11.2a | Part 11.8 |
| E-V-42 | Tests count 4,156 vs indexable rows | 1 / 2 | 11.10a | Part 11.10c |
| E-V-43 | Hosting cost lines without PITR / standby | 4 / 4 | 11.5b, 11.9b | DEC-771, DEC-787 |
| E-V-44 | X-09 developer platform exclusion | 3 / 4 | 11.1b | DEC-785 |
| E-V-45 | A172 agentic commerce workspace "EP-13 · Future (W6+)" | 2 / 3 | 11.7b | DEC-780 |
| E-V-46 | Decisions left "Pending Founder decision" | 774 / 797 | 11.10a, 11.10c, 11.11a, 11.11b, 11.12, 11.13a, 11.13b, 11.14, 11.16c, 11.16e … | DEC-770…791 |
| E-V-47 | Group P provisional screens A260–A269 | 2 / 2 | 11.17a, 11.17b | DEC-962 |
| E-V-49 | Workbook token rates treated as prices | 0 / 1 | — | DEC-788 |
| E-V-50 | Appendix C workflow IDs with one-digit suffix | 1 / 84 | 11.9b | DEC-966 |

### 11.23.7.3 Errata entries (current rule for the development team)

#### E-V-01 Consequential actions always capped at L1

| Field | Entry |
|---|---|
| Stale statement | Consequential actions always capped at L1 |
| **Current rule (binding)** | L0–L2 by default; L3/L4 only under an Active, eligible bounded mandate approved by two authorized people, scoped (counterparty, action type, per-action and aggregate value cap, time window, jurisdiction, data class), instantly revocable, with kill switch, PDP dispatch recheck, audit and reconciliation, in a jurisdiction whose rule pack permits it. No API scope for consequential actions (DEC-883). |
| Authority | DEC-779, DEC-841, DEC-883 |
| Stale occurrences | 42 of 56 matching lines carry no reference to the authority; first locations: Part 0 L318; Part 2.2 L77; Part 5.3 L1780; Part 6.3a L854; Part 6.4 L2415; Part 7.1 L202 |
| Reported by | Brief; Part 11.19c #2 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-02 Safety envelope "AI never signs, pays, submits bids, sets prices"

| Field | Entry |
|---|---|
| Stale statement | Safety envelope "AI never signs, pays, submits bids, sets prices" |
| **Current rule (binding)** | AI still never signs contracts and never sets prices autonomously; payments (DEC-780) and bid submission (DEC-781) may be executed by an agent only under a bounded mandate, through a licensed PSP or the approved portal, with exact package/amount hash, caps, kill switch and reconciliation. |
| Authority | DEC-779, DEC-780, DEC-781 |
| Stale occurrences | 31 of 44 matching lines carry no reference to the authority; first locations: Part 0A L60; Part 0 L89; Part 2.3 L189; Part 5.2 L2922; Part 6.1 L295; Part 7.1 L237 |
| Reported by | Audit (this part) |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-03 "Service key held server-side" for the Django API

| Field | Entry |
|---|---|
| Stale statement | "Service key held server-side" for the Django API |
| **Current rule (binding)** | Django API and workers connect as least-privilege NOBYPASSRLS roles (`app_rw`, `app_worker`) setting `app.tenant_id` and `app.company_ids` per transaction; Data API (PostgREST) disabled for application schemas; `service_role` only in the CI migration pipeline under two-person, time-boxed break-glass with audit. |
| Authority | DEC-778, DEC-894 (ADR-264) |
| Stale occurrences | 3 of 8 matching lines carry no reference to the authority; first locations: Part 11.8b L583; Part 11.9b L54; Part 11.9c L332 |
| Reported by | Brief; Parts 11.9c, 11.19c #4 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-04 Database role names `ge_app` / `ge_worker` / `ge_owner` / `app_user`

| Field | Entry |
|---|---|
| Stale statement | Database role names `ge_app` / `ge_worker` / `ge_owner` / `app_user` |
| **Current rule (binding)** | Canonical roles: `app_owner`, `app_migrator`, `app_rw`, `app_worker`, `app_readonly`, `app_retention`, `app_platform_sec`, `app_bench`, `app_registry` (all NOBYPASSRLS). `ge_app` → `app_rw`, `ge_worker` → `app_worker`, `ge_owner` → `app_owner`, V12 `app_user` → `app_rw` (rename migration DDL-V12-R-16). |
| Authority | DEC-778, DEC-894 |
| Stale occurrences | 35 of 50 matching lines carry no reference to the authority; first locations: Part 3.3 L2170; Part 3.3 L2180; Part 3.3 L2181; Part 3.3 L2182; Part 3.3 L3686; Part 3.3 L3688 |
| Reported by | Parts 11.9c #2, 11.19c #1 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-05 AWS-only topology (RDS, CloudFront, RDS cross-Region backups)

| Field | Entry |
|---|---|
| Stale statement | AWS-only topology (RDS, CloudFront, RDS cross-Region backups) |
| **Current rule (binding)** | Vercel (web, edge firewall, region-pinned functions) + Supabase PostgreSQL (RLS, pgvector, PITR) + AWS (API, workers, Valkey, S3, SES, Secrets Manager/KMS) in Mumbai, with an EU stack for EU-resident tenants; deployment view Part 11.5b §11.5.5.8–11.5.5.9. |
| Authority | DEC-421, DEC-772, DEC-786 |
| Stale occurrences | 30 of 34 matching lines carry no reference to the authority; first locations: Part 3.1 L204; Part 3.1 L793; Part 3.1 L845; Part 3.1 L856; Part 3.1 L885; Part 3.1 L929 |
| Reported by | Part 11.5b #1, #5; Part 11.8b #3 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-06 PostgreSQL 17 on Amazon RDS

| Field | Entry |
|---|---|
| Stale statement | PostgreSQL 17 on Amazon RDS |
| **Current rule (binding)** | Supabase-managed PostgreSQL (major version as provided by Supabase at provisioning; V12 DDL tested on 16.15 — verify at implementation, as of 28 Nov 2026); extensions pgvector and pg_cron subject to Supabase availability. |
| Authority | DEC-421, DEC-772 |
| Stale occurrences | 4 of 5 matching lines carry no reference to the authority; first locations: Part 3.1 L164; Part 3.1 L204; Part 3.3 L4370; Part 9.2 L741 |
| Reported by | Part 11.9c #3 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-07 V12 screen IDs used bare where they collide with blueprint IDs

| Field | Entry |
|---|---|
| Stale statement | V12 screen IDs used bare where they collide with blueprint IDs |
| **Current rule (binding)** | Blueprint screen IDs are primary. A V12 screen ID that collides (A114–A131, W35–W41) is always written `V12-<ID>` and mapped by the binding crosswalk (Part 11.7a §11.7.4.2–11.7.4.3; e.g. V12 A122 → A203). Investment screens are A205–A232 / W55–W76 (DEC-801) and A233–A259 / W77–W99 (Group O); Group P uses A260–A269 (DEC-962). |
| Authority | DEC-620, DEC-700, DEC-801, DEC-962 |
| Stale occurrences | 15 of 26 matching lines carry no reference to the authority; first locations: Part 11.10a L706; Part 11.10a L745; Part 11.10c L370; Part 11.19a L212; Part 11.6a L179; Part 11.6b L350 |
| Reported by | Brief; Parts 11.6b #1, 11.7c #3, 11.11b #4 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-08 Screen range A205–A259 / W55–W99 "reserved and unused"

| Field | Entry |
|---|---|
| Stale statement | Screen range A205–A259 / W55–W99 "reserved and unused" |
| **Current rule (binding)** | A205–A232/W55–W76 are used by Group N (DEC-801), A233–A259/W77–W99 by Group O; A260–A269 by Group P (DEC-962). Next free Admin ID: A270; next free Website ID: W100. |
| Authority | DEC-801, DEC-962 |
| Stale occurrences | 1 of 1 matching lines carry no reference to the authority; first locations: Part 11.7c L799 |
| Reported by | Audit (this part) |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-09 RTO 4 h at pilot / staged RTO

| Field | Entry |
|---|---|
| Stale statement | RTO 4 h at pilot / staged RTO |
| **Current rule (binding)** | RPO ≤ 15 min in every residency region (continuous WAL, daily base backup, 35-day PITR; DEC-787). Growth-critical RTO ≤ 120 min is a release-blocking gate from Release 1 (OKPI-32 = V12 KPI-32; DEC-771). Core critical-tier RTO ≤ 4 h stays as the outer bound only for non-growth platform components (CDEC-V9-01). Regenerable stores RTO 24 h / RPO 8 h. |
| Authority | DEC-771, DEC-787, CDEC-V9-01 |
| Stale occurrences | 60 of 77 matching lines carry no reference to the authority; first locations: Part 0A L55; Part 0 L339; Part 3.1 L32; Part 3.1 L1358; Part 3.1 L1412; Part 3.1 L1709 |
| Reported by | Brief; Part 11.5b #2, #6 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-10 Single-region pilot / region count

| Field | Entry |
|---|---|
| Stale statement | Single-region pilot / region count |
| **Current rule (binding)** | Two residency stacks are built: India (Mumbai) and EU (e.g. Frankfurt), never writing one zone's personal data to the other (CJ-TC-09 blocking both ways; DEC-772). Further regions (UK, Middle East, APAC, then US) open only when each jurisdiction rule pack is counsel-approved (DEC-776). Residency is chosen at tenant onboarding. |
| Authority | DEC-772, DEC-776 |
| Stale occurrences | 25 of 25 matching lines carry no reference to the authority; first locations: Part 3.1 L1407; Part 3.1 L1709; Part 3.1 L1777; Part 3.1 L1805; Part 4.2 L427; Part 8.2 L62 |
| Reported by | Brief |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-11 SM-SVC-26 voice assigned to EP-08

| Field | Entry |
|---|---|
| Stale statement | SM-SVC-26 voice assigned to EP-08 |
| **Current rule (binding)** | SM-SVC-26 (AI voice) belongs to epic EP-22 (Part 11.2a registry; Part 11.18). Pattern references to EP-08 are read as EP-22. |
| Authority | Part 11.2a; Part 11.18d |
| Stale occurrences | 2 of 4 matching lines carry no reference to the authority; first locations: Part 11.4c L792; Part 11.7b L1210 |
| Reported by | Brief; Part 11.18d #4 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-12 Voice domain named `eng_call`

| Field | Entry |
|---|---|
| Stale statement | Voice domain named `eng_call` |
| **Current rule (binding)** | The V12 canonical domain is `voice_session` (with `voice_turn`, recording and consent artefacts per Part 11.18); `eng_call` is withdrawn. |
| Authority | Part 11.18d (V12 canonical) |
| Stale occurrences | 3 of 17 matching lines carry no reference to the authority; first locations: Part 11.18a L9; Part 11.4c L801; Part 11.4d L1381 |
| Reported by | Brief; Part 11.18d #2 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-13 Mandates and securities-governed investment actions

| Field | Entry |
|---|---|
| Stale statement | Mandates and securities-governed investment actions |
| **Current rule (binding)** | DEC-779 mandates apply only "where lawful". Securities-governed INV actions (offer issue, offering-tagged dispatch, closing, allotment reference, filing status, cap-table revision, vote certification, KYC decision, external submission) stay L1 with hash-bound, per-action approval (two-person for closing and cap table) and are never mandate-authorised (DEC-822, CP-O-04). A DEC-779 mandate may automate only non-offering investor-relations messages (mandate type `inv_ir_message`). The Part 11.17 mandate engine must reject these action types at issue and at dispatch. |
| Authority | DEC-779 (lawful condition), DEC-783, DEC-822, DEC-963 |
| Stale occurrences | 1 of 1 matching lines carry no reference to the authority; first locations: Part 11.14 L29 |
| Reported by | Brief; Parts 11.16a/b/d |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-14 Customer decision IDs written DEC-Vn-## / DEC-### for V12 decisions

| Field | Entry |
|---|---|
| Stale statement | Customer decision IDs written DEC-Vn-## / DEC-### for V12 decisions |
| **Current rule (binding)** | Customer decisions are written CDEC-### and CDEC-Vn-## (DEC-700); bare DEC-### always means a blueprint decision. |
| Authority | DEC-700 |
| Stale occurrences | 149 of 155 matching lines carry no reference to the authority; first locations: Part 11.10c L721; Part 11.12 L17; Part 11.12 L80; Part 11.12 L146; Part 11.12 L196; Part 11.12 L220 |
| Reported by | Parts 11.9c #6, 11.12 #2; audit |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-15 V12 KPI-## used without the OKPI alias

| Field | Entry |
|---|---|
| Stale statement | V12 KPI-## used without the OKPI alias |
| **Current rule (binding)** | V12 KPI-01…35 = OKPI-01…35 (DEC-681). Blueprint KPI-01…35 are the Part 1 business KPIs. Always write OKPI-## for V12 release KPIs. |
| Authority | DEC-681 |
| Stale occurrences | 26 of 32 matching lines carry no reference to the authority; first locations: Part 11.14 L21; Part 11.22a L344; Part 11.9a L246; Part 11.9a L247; Part 11.9a L248; Part 11.9a L249 |
| Reported by | Parts 11.10c #2, 11.12 #2 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-16 V12 REC-01…30 collide with blueprint reconciliation jobs REC-01…09

| Field | Entry |
|---|---|
| Stale statement | V12 REC-01…30 collide with blueprint reconciliation jobs REC-01…09 |
| **Current rule (binding)** | Blueprint REC-01…09 are reconciliation jobs (Part 3.2). V12 REC-01…30 are reconciliation actions; write them `V12-REC-##`. |
| Authority | DEC-964 |
| Stale occurrences | 193 of 196 matching lines carry no reference to the authority; first locations: Part 3.2 L1371; Part 3.2 L1372; Part 3.2 L1373; Part 3.2 L1374; Part 3.2 L1375; Part 3.2 L1376 |
| Reported by | Part 11.12 #1 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-17 Messaging window 09:00–19:00 Mon–Sat

| Field | Entry |
|---|---|
| Stale statement | Messaging window 09:00–19:00 Mon–Sat |
| **Current rule (binding)** | Promotional messages 09:00–21:00 in the recipient's local time (DEC-777); a stricter rule pack window wins; quiet hours, consent and suppression unchanged; transactional messages follow their own rules. |
| Authority | DEC-777 |
| Stale occurrences | 25 of 28 matching lines carry no reference to the authority; first locations: Part 2.3 L49; Part 5.1a L380; Part 5.1b L1689; Part 5.1b L1809; Part 5.2 L505; Part 5.2 L917 |
| Reported by | Part 11.14 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-18 Business-hours support

| Field | Entry |
|---|---|
| Stale statement | Business-hours support |
| **Current rule (binding)** | 24×7 human on-call for SEV1/SEV2 and 24×7 security monitoring from Release 2 GA (contracted NOC/SOC first line, internal rota second line). |
| Authority | DEC-773 |
| Stale occurrences | 4 of 5 matching lines carry no reference to the authority; first locations: Part 0 L258; Part 9.1 L34; Part 9.2 L1829; Part 11.11b L777 |
| Reported by | Part 11.14 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-19 Investor / fundraising exclusion

| Field | Entry |
|---|---|
| Stale statement | Investor / fundraising exclusion |
| **Current rule (binding)** | Investor/fundraising mode and the Investment Automation product (INV-SVC-01…24, 96 workflows) are in scope with securities rule packs, eligibility verification, no public offer where prohibited, counsel sign-off per jurisdiction and no investment advice by AI. |
| Authority | DEC-783 |
| Stale occurrences | 38 of 40 matching lines carry no reference to the authority; first locations: Part 0 L76; Part 0 L271; Part 1 L18; Part 2.6 L1876; Part 3.4 L336; Part 3.4 L1799 |
| Reported by | Part 11.14 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-20 Voice / recording / SMS prohibited

| Field | Entry |
|---|---|
| Stale statement | Voice / recording / SMS prohibited |
| **Current rule (binding)** | AI voice calling and recordings adopted (DEC-782) with AI self-identification, consent and DND scrubbing, calling windows, notice/consent for recording (all-party where required), retention limits, redaction and human hand-off. SMS via a DLT-registered aggregator in Release 1 (DEC-785, DEC-884). |
| Authority | DEC-782, DEC-785, DEC-884 |
| Stale occurrences | 13 of 13 matching lines carry no reference to the authority; first locations: Part 11.15e L1145; Part 11.15e L1272; Part 11.15e L1599; Part 11.15e L1612; Part 11.15e L1718; Part 11.15e L1861 |
| Reported by | Part 11.2c #1 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-21 Automatic bid submission prohibited

| Field | Entry |
|---|---|
| Stale statement | Automatic bid submission prohibited |
| **Current rule (binding)** | Automatic bid submission allowed only under a per-tender bounded mandate: a human approves package hash, price, terms and portal/authority; the agent submits exactly that package and records the receipt. Unmandated submission stays human. |
| Authority | DEC-781, DEC-851, DEC-852 |
| Stale occurrences | 23 of 26 matching lines carry no reference to the authority; first locations: Part 3.5b L1697; Part 8.3a L112; Part 9.2 L74; Part 9.2 L1925; Part 9.5 L73; Part 9.6a L60 |
| Reported by | Part 11.17b #4 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-24 Tier 2 free providers described as an active fallback chain

| Field | Entry |
|---|---|
| Stale statement | Tier 2 free providers described as an active fallback chain |
| **Current rule (binding)** | Only models approved in the provider-neutral registry (DPA with no-training clause, region, data class, evaluation suites, cost) may run; Claude Sonnet is the approved primary; free tiers never receive personal or restricted data. |
| Authority | DEC-788 |
| Stale occurrences | 1 of 1 matching lines carry no reference to the authority; first locations: Part 11.6b L2130 |
| Reported by | Part 11.6b #3 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-25 Fixed release dates as commitments

| Field | Entry |
|---|---|
| Stale statement | Fixed release dates as commitments |
| **Current rule (binding)** | Dates are indicative; Release 1 and Release 2 are re-planned from approved effort and measured throughput; scope is not cut to meet a date (master plan Part 11.20). |
| Authority | DEC-770 |
| Stale occurrences | 53 of 53 matching lines carry no reference to the authority; first locations: Part 9.10 L166; Part 9.10 L167; Part 9.2 L444; Part 9.2 L1976; Part 9.2 L1977; Part 9.5 L154 |
| Reported by | Part 11.14 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-26 Judge agreement ≥ 85% vs κ ≥ 0.8

| Field | Entry |
|---|---|
| Stale statement | Judge agreement ≥ 85% vs κ ≥ 0.8 |
| **Current rule (binding)** | AI-judge calibration uses Cohen's κ ≥ 0.8 against human labels (AIX-07). |
| Authority | DEC-603 |
| Stale occurrences | 4 of 6 matching lines carry no reference to the authority; first locations: Part 6.4 L165; Part 6.4 L211; Part 7.2 L149; Part 9.7b L1459 |
| Reported by | Part 11.6b #2 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-27 Admin not targeted below 768 px

| Field | Entry |
|---|---|
| Stale statement | Admin not targeted below 768 px |
| **Current rule (binding)** | One responsive Admin build with a compact layout for all registered screens (MOB-01/06). |
| Authority | DEC-623 |
| Stale occurrences | 7 of 9 matching lines carry no reference to the authority; first locations: Part 0A L80; Part 2.7a L1073; Part 2.7a L1131; Part 5.3 L1173; Part 6.1 L154; Part 9.2 L1249 |
| Reported by | Part 11.7c #2 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-28 Outbound webhooks not offered

| Field | Entry |
|---|---|
| Stale statement | Outbound webhooks not offered |
| **Current rule (binding)** | Signed outbound webhooks are part of the Release 1 developer platform (DEC-785; DEC-645). |
| Authority | DEC-645, DEC-785 |
| Stale occurrences | 5 of 6 matching lines carry no reference to the authority; first locations: Part 9.2 L1347; Part 9.9a L83; Part 9.9a L418; Part 9.9b L1338; Part 11.8a L70 |
| Reported by | Part 11.8b #2 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-29 Benchmarks disabled / ε = 1

| Field | Entry |
|---|---|
| Stale statement | Benchmarks disabled / ε = 1 |
| **Current rule (binding)** | Cross-tenant benchmarks in Release 2: opt-in contract clause, cohorts ≥ 10 tenants (k ≥ 10), dominance ≤ 30%, Laplace ε = 0.5 per metric per cell per month (yearly cap 6), zone-local computation. |
| Authority | DEC-789, DEC-893 |
| Stale occurrences | 3 of 4 matching lines carry no reference to the authority; first locations: Part 11.13b L42; Part 11.13b L1189; Part 11.19c L3111 |
| Reported by | Part 11.19c #5 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-30 Voice transport "R3+ → W6"

| Field | Entry |
|---|---|
| Stale statement | Voice transport "R3+ → W6" |
| **Current rule (binding)** | Voice CPaaS transport is a Release 1 connector (DEC-884); AI voice features per Part 11.18 release plan. |
| Authority | DEC-785, DEC-884 |
| Stale occurrences | 1 of 2 matching lines carry no reference to the authority; first locations: Part 11.8b L511 |
| Reported by | Part 11.19c #6 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-31 Missing tenant context returns zero rows

| Field | Entry |
|---|---|
| Stale statement | Missing tenant context returns zero rows |
| **Current rule (binding)** | Missing `app.tenant_id` must raise an error (fail closed), not return zero rows (V12 DB-T2). |
| Authority | CONFLICT-909 resolution (Part 11.9c) |
| Stale occurrences | 0 of 2 matching lines carry no reference to the authority; first locations: — |
| Reported by | Part 11.9c #4 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-32 BYOK limited to AWS KMS

| Field | Entry |
|---|---|
| Stale statement | BYOK limited to AWS KMS |
| **Current rule (binding)** | Customer-managed keys across clouds (DEC-776). |
| Authority | DEC-776 |
| Stale occurrences | 2 of 2 matching lines carry no reference to the authority; first locations: Part 11.11a L187; Part 11.11b L780 |
| Reported by | Part 11.9c #5 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-33 Money stored as numeric(18,2)

| Field | Entry |
|---|---|
| Stale statement | Money stored as numeric(18,2) |
| **Current rule (binding)** | Money in integer minor units (`*_minor bigint`) with currency; arithmetic CHECKs in the database; expand/contract migration MG-02…04. |
| Authority | DEC-587 |
| Stale occurrences | 24 of 30 matching lines carry no reference to the authority; first locations: Part 3.3 L2130; Part 3.3 L2675; Part 3.3 L2870; Part 3.3 L2871; Part 3.3 L2872; Part 3.3 L2873 |
| Reported by | Parts 11.5b #3, 11.3c #2 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-34 Run-state vocabularies differ

| Field | Entry |
|---|---|
| Stale statement | Run-state vocabularies differ |
| **Current rule (binding)** | One run-state vocabulary: Pending, Running, Waiting, Held, Paused, Reconciling, Succeeded, Failed, Cancelled (+ Blocked for preflight holds), mapped to the Part 3.2 API states (DEC-561). |
| Authority | DEC-561 |
| Stale occurrences | 0 of 1 matching lines carry no reference to the authority; first locations: — |
| Reported by | Part 11.3c #1 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-35 Workflow catalogue titled WF-01…39 / WF-01 to WF-14

| Field | Entry |
|---|---|
| Stale statement | Workflow catalogue titled WF-01…39 / WF-01 to WF-14 |
| **Current rule (binding)** | Blueprint workflows are WF-01…WF-60 with WF-24 and WF-40 unused; V12 workflows are SM-SVC-##-WF# (156) and INV workflows. |
| Authority | Part 9.10; Part 11.4d |
| Stale occurrences | 4 of 5 matching lines carry no reference to the authority; first locations: Part 9.2 L2249; Part 9.4 L22; Part 9.4 L284; Part 11.13a L8 |
| Reported by | Part 11.4d #1, #2 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-36 Side-effect classes R0/W1/X2 vs none/internal/external

| Field | Entry |
|---|---|
| Stale statement | Side-effect classes R0/W1/X2 vs none/internal/external |
| **Current rule (binding)** | Mapping R0 → none, W1 → internal, X2 → external; V12 R-classes R0…R3 govern authority (DEC-570). |
| Authority | DEC-570, DEC-965 |
| Stale occurrences | 2 of 3 matching lines carry no reference to the authority; first locations: Part 11.6a L244; Part 11.6a L245 |
| Reported by | Part 11.4d #3 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-37 SEV1 notice targets differ

| Field | Entry |
|---|---|
| Stale statement | SEV1 notice targets differ |
| **Current rule (binding)** | Single SEV communication matrix of Part 11.11 §11.11.5.3. |
| Authority | DEC-701 |
| Stale occurrences | 1 of 3 matching lines carry no reference to the authority; first locations: Part 4.3 L480 |
| Reported by | Part 11.11b #1 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-38 Status page "Not defined [GAP-126]"

| Field | Entry |
|---|---|
| Stale statement | Status page "Not defined [GAP-126]" |
| **Current rule (binding)** | Status page defined (DEC-406, DEC-703; W40 route links to the external status page). |
| Authority | DEC-406, DEC-703 |
| Stale occurrences | 0 of 1 matching lines carry no reference to the authority; first locations: — |
| Reported by | Part 11.11b #3 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-39 Effort 287–483 pd / ₹13.05–32.93 lakh as current budget

| Field | Entry |
|---|---|
| Stale statement | Effort 287–483 pd / ₹13.05–32.93 lakh as current budget |
| **Current rule (binding)** | Approved development budget DEC-230 plus CR-V12-J-01 (DEC-770) and all V12 CRs funded (DEC-790); re-forecast at each sprint review. |
| Authority | DEC-228, DEC-230, DEC-770, DEC-790 |
| Stale occurrences | 48 of 54 matching lines carry no reference to the authority; first locations: Part 0A L35; Part 0 L94; Part 0 L274; Part 1 L26; Part 1 L459; Part 2.6 L1860 |
| Reported by | Part 11.12 #3 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-40 IdP: one connection per tenant

| Field | Entry |
|---|---|
| Stale statement | IdP: one connection per tenant |
| **Current rule (binding)** | Multiple IdP connections per tenant; V12 C2 single-row `identity_provider` exposed as a compatibility view (FR-V12-R-029). |
| Authority | DEC-784; FR-V12-R-029 |
| Stale occurrences | 0 of 1 matching lines carry no reference to the authority; first locations: — |
| Reported by | Part 11.19c #7 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-41 API catalogue count 579 only

| Field | Entry |
|---|---|
| Stale statement | API catalogue count 579 only |
| **Current rule (binding)** | API register = 579 core + 40 advanced (API-ADV-X1) + V12 operations (Appendix A 282, A2 48, mapped in Part 11.8) + group additions; Part 9.2 counts are superseded by the Part 11.8 register. |
| Authority | Part 11.8 |
| Stale occurrences | 2 of 2 matching lines carry no reference to the authority; first locations: Part 11.1a L910; Part 11.2a L164 |
| Reported by | Part 11.8b #1 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-42 Tests count 4,156 vs indexable rows

| Field | Entry |
|---|---|
| Stale statement | Tests count 4,156 vs indexable rows |
| **Current rule (binding)** | Count of record 4,156 baseline tests (4,077 indexable rows; the rest as ranges) plus every TC-V12-* added in Part 11. |
| Authority | Part 11.10c |
| Stale occurrences | 1 of 2 matching lines carry no reference to the authority; first locations: Part 11.10a L8 |
| Reported by | Part 11.10c #3 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-43 Hosting cost lines without PITR / standby

| Field | Entry |
|---|---|
| Stale statement | Hosting cost lines without PITR / standby |
| **Current rule (binding)** | PITR and a warm standby are funded from Release 1 (DEC-771, DEC-787). |
| Authority | DEC-771, DEC-787 |
| Stale occurrences | 4 of 4 matching lines carry no reference to the authority; first locations: Part 11.5b L214; Part 11.5b L953; Part 11.5b L1024; Part 11.9b L60 |
| Reported by | Part 11.5b #2 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-44 X-09 developer platform exclusion

| Field | Entry |
|---|---|
| Stale statement | X-09 developer platform exclusion |
| **Current rule (binding)** | Developer platform (API keys, OAuth client credentials, signed webhooks, portal, SDKs, sandbox) is in Release 1; X-09 withdrawn. |
| Authority | DEC-785 |
| Stale occurrences | 3 of 4 matching lines carry no reference to the authority; first locations: Part 11.1b L467; Part 11.1b L831; Part 11.1b L897 |
| Reported by | Part 11.14 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-45 A172 agentic commerce workspace "EP-13 · Future (W6+)"

| Field | Entry |
|---|---|
| Stale statement | A172 agentic commerce workspace "EP-13 · Future (W6+)" |
| **Current rule (binding)** | SM-SVC-28 belongs to EP-24, Release 2 under CR-V12-P (DEC-780). |
| Authority | DEC-780 |
| Stale occurrences | 2 of 3 matching lines carry no reference to the authority; first locations: Part 11.7b L1266; Part 11.7b L1517 |
| Reported by | Part 11.17b #1 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-46 Decisions left "Pending Founder decision"

| Field | Entry |
|---|---|
| Stale statement | Decisions left "Pending Founder decision" |
| **Current rule (binding)** | Every V12 item pending a Founder decision was adopted by DEC-770…791 (DEC-791 closes the remainder). Read any "Pending Founder decision" as decided per Part 11.14. |
| Authority | DEC-770…791 |
| Stale occurrences | 774 of 797 matching lines carry no reference to the authority; first locations: Part 11.10a L94; Part 11.10a L160; Part 11.10c L720; Part 11.10c L721; Part 11.10c L722; Part 11.10c L738 |
| Reported by | Part 11.17b #3 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-47 Group P provisional screens A260–A269

| Field | Entry |
|---|---|
| Stale statement | Group P provisional screens A260–A269 |
| **Current rule (binding)** | A260–A269 confirmed for Group P (Part 11.17) by DEC-962. |
| Authority | DEC-962 |
| Stale occurrences | 2 of 2 matching lines carry no reference to the authority; first locations: Part 11.17a L948; Part 11.17b L3274 |
| Reported by | Part 11.17b #5 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-49 Workbook token rates treated as prices

| Field | Entry |
|---|---|
| Stale statement | Workbook token rates treated as prices |
| **Current rule (binding)** | Workbook Cost_Model rates are illustrative; model costs come from the registry rate card (DEC-788), verify at implementation. |
| Authority | DEC-788 |
| Stale occurrences | 0 of 1 matching lines carry no reference to the authority; first locations: — |
| Reported by | Part 11.2c #3 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

#### E-V-50 Appendix C workflow IDs with one-digit suffix

| Field | Entry |
|---|---|
| Stale statement | Appendix C workflow IDs with one-digit suffix |
| **Current rule (binding)** | Workflow IDs are always `SM-SVC-##-WF0#` (two digits) — the form used in Appendix C comments; chapter forms `-WF1` are aliases. |
| Authority | DEC-966 |
| Stale occurrences | 1 of 84 matching lines carry no reference to the authority; first locations: Part 11.9b L801 |
| Reported by | Part 11.9c #6 |
| Developer instruction | Implement the current rule. Where any part still states the stale text, this erratum governs (DEC-961). |

### 11.23.7.4 Notes on specific errata

- **E-V-01 / E-V-02 (L1 cap and safety envelope).** The invariant is not removed; it is scoped. Outside an Active, eligible bounded mandate in an approved jurisdiction, every consequential action remains L1 with a human approval bound to the exact payload hash. The PDP recheck at dispatch, the kill switch, audit and reconciliation apply in both cases. AI still never signs contracts, never sets prices autonomously and never gives investment advice.
- **E-V-04 (role names).** Three names circulated for the same non-owner role (Part 3.3 `ge_app`, V12 Appendix C `app_user`, Part 11.5a/11.14 `app_rw`). DEC-894 fixed the full canonical set; use it in DDL, connection strings, runbooks and tests.
- **E-V-07 / E-V-08 / E-V-47 (screen IDs).** Numbering rule now in force: blueprint IDs are primary; V12 colliding IDs are written `V12-A1xx` / `V12-W3x`; Group N A205–A232/W55–W76; Group O A233–A259/W77–W99; Group P A260–A269 (DEC-962); next free Admin A270, Website W100.
- **E-V-09 (RTO/RPO).** One table governs: RPO ≤ 15 min in every residency region; growth-critical RTO ≤ 120 min, release-blocking; core critical-tier RTO ≤ 4 h as outer bound for non-growth components; regenerable stores 24 h / 8 h; restore drills at each release gate.
- **E-V-10 (region count).** Two residency stacks are built (India, EU). Further regions are roadmap items that open market by market (DEC-776). Any text that says "single region" describes the pre-V12 pilot only.
- **E-V-13 (mandates and securities).** DEC-822 is not a contradiction of DEC-779 but its "where lawful" condition applied to securities law; FR-V12-V-008 and DEC-963 make the mandate engine enforce it.
- **E-V-46 ("Pending Founder decision").** 774 stale labels remain in Parts 11.1–11.13 registers and coverage CSVs. They must be read as decided by DEC-770…791; Part 11.0 is regenerated by the consolidation owner.

---

## 11.23.8 Conflicts and proposed resolutions

| Tag | Conflict | Resolution | Status |
|---|---|---|---|
| [CONFLICT-1184] | The four V12 HTML prototypes as received have SHA-256 values different from the hashes declared in BRD/FSD V12 ch01 | Cause found: CRLF line endings added in transit (381/635 CR characters); after LF normalisation all four match. Content is the declared content. Register both values; adopt the LF-normalisation rule for text artifacts | Resolved (DEC-968) |
| [CONFLICT-1185] | DEC-822 (no mandates for securities-governed INV actions) narrows Founder DEC-779 | Not a contradiction: DEC-779 permits mandates "where lawful"; securities law requires per-action authority. Enforce in the mandate engine (FR-V12-V-008) | Resolved (DEC-963) |
| [CONFLICT-1186] | V12 `REC-01…30` (reconciliation actions) collide with blueprint `REC-01…09` (reconciliation jobs, Part 3.2) | Qualify V12 IDs as `V12-REC-##` | Resolved (DEC-964) |
| [CONFLICT-1187] | Side-effect class vocabularies R0/W1/X2 (Part 7.4b NT13) and none/internal/external (Part 3.3) | Fixed mapping R0→none, W1→internal, X2→external; V12 R-classes govern authority (DEC-570) | Resolved (DEC-965) |

---

## 11.23.9 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-960 | **Audit acceptance rule.** Coverage of a customer revision is accepted when every extracted statement ends as measured Matched, Covered in different words (cited), Restored (new content) or Superseded (DEC cited), with 0 unclassified, and the per-statement register is published (`V_audit.csv`). Self-reported coverage registers are not evidence | Independent assurance panel (Part 11.23), under DEC-791 | V12 audit closed: 94.06% → 94.06% measured; 100% classified |
| DEC-961 | **Errata precedence.** The errata E-V-01…50 of Part 11.23c state the current rule wherever an earlier part still carries a stale statement; precedence Part 11.14 > Part 11.23c errata > Parts 11.1–11.22 > Part 9.10 > earlier parts | Independent assurance panel (Part 11.23); implements DEC-770…791 | Extends DEC-415/DEC-500; FR-V12-V-009 lint |
| DEC-962 | **Screen-ID registry.** Group P's provisional screens A260–A269 (ASSUMPTION-1040) are confirmed; Part 11.7c's note "A205–A259 and W55–W99 reserved and unused" is withdrawn (used by Groups N and O); next free IDs A270 and W100; any new screen ID is taken from the registry, never chosen locally | Independent assurance panel (Part 11.23) | Closes ASSUMPTION-1040; errata E-V-07, E-V-08, E-V-47 |
| DEC-963 | **Mandate exclusion for securities-governed actions** is enforced in the mandate engine and the PDP (FR-V12-V-008); `inv_ir_message` is the only INV mandate type | Customer revision V12 (28 Nov 2026) as decided by Founder DEC-779/783; DEC-822 | Resolves CONFLICT-1185; erratum E-V-13 |
| DEC-964 | V12 reconciliation actions are written `V12-REC-##`; blueprint REC-01…09 keep their meaning | Independent assurance panel (Part 11.23) | Resolves CONFLICT-1186; erratum E-V-16 |
| DEC-965 | Side-effect class mapping R0→none, W1→internal, X2→external, stated once here for Parts 3.3 and 7.4b | Independent assurance panel (Part 11.23) | Resolves CONFLICT-1187; erratum E-V-36 |
| DEC-966 | Workflow IDs are always written `SM-SVC-##-WF0#`; chapter forms `-WF1…4` are aliases | Independent assurance panel (Part 11.23) | Erratum E-V-50 |
| DEC-967 | `ENT-ENH-*` and `API-ENH-*` IDs are canonical; the placeholders ENT-200…203 and API-556+ are not assigned | Independent assurance panel (Part 11.23) | Closes GAP-1183 |
| DEC-968 | **Artifact integrity rule.** Every customer delivery is hashed on receipt; text artifacts are compared as received and LF-normalised; a mismatch in both forms holds the baseline; the register of FR-V12-V-001 is a configuration item | Independent assurance panel (Part 11.23) | Resolves CONFLICT-1184 |
| DEC-969 | **Bare-ID rule.** Bare `DEC-###` = blueprint decision; `CDEC-…` = customer decision; bare `KPI-##` = Part 1 business KPI; `OKPI-##` = V12 release KPI; bare `A###`/`W##` = blueprint screen; `V12-A###`/`V12-W##` = colliding customer screen | Independent assurance panel (Part 11.23); consolidates DEC-620/681/700 | Errata E-V-07, E-V-14, E-V-15 |
| DEC-970 | **Re-audit gate.** The `v_*.py` audit runs at every consolidation and on every future customer revision; acceptance per DEC-960 is a documentation release gate | Independent assurance panel (Part 11.23) | FR-V12-V-009 |

---

## 11.23.10 Expert persona review

| Persona | Finding | Disposition |
|---|---|---|
| Forensic requirements auditor | The measured method is reproducible and strict on literal adoption; the token measure is generous, which is why nothing below "moderate" was accepted without reading. 705 disposition rows and 142 DDL statements were verified per row, not by sampling | Accepted; method in §11.23.1 |
| Configuration-management lead | The most important finding is not a missing requirement but a baseline-integrity event: the received HTML differs from the declared hashes (CRLF in transit). Without the LF rule a future review could reject a correct baseline or accept a changed one | DEC-968, FR-V12-V-001 |
| Configuration-management lead | No baseline ID was lost, but 207 IDs changed meaning or scope, and 1,667 stale lines remain in the parts | Supersession index and errata; FR-V12-V-009 lint |
| Principal Business Systems Analyst | The restored content is small but real: the per-screen V2 rule, the ICP attribute set, FX rates below 1 and the one-implementation rule would otherwise be lost because they sit in change-history tables | FR-V12-V-004…007 |
| Security reviewer | E-V-03/E-V-04 matter most for safety: any developer following Part 11.8b or Part 3.3 literally would connect with a key that bypasses RLS or with a non-canonical role | Errata binding; DEC-894 roles |
| AI-governance reviewer | The scoped L1 invariant must be read with the mandate conditions; the securities exclusion closes the only path where a mandate could reach a regulated action | FR-V12-V-008, DEC-963 |
| QA lead | 34 new test cases and 9 stories; 4 exhaustive combinatorial models (40 + 40 + 11 + 14 = 105 Examples rows) | §11.23.5.10–11.23.5.11 |

---

## 11.23.11 Tags register

| Tag | Type | Statement | Location | Status |
|---|---|---|---|---|
| [ASSUMPTION-1180] | Assumption | The working-tree Parts 0–9.10 and pre-V12 registers are the pre-V12 baseline (timestamps before V12 receipt; git not run) | §11.23.6.1 | Open — confirm with `git diff` at consolidation |
| [ASSUMPTION-1181] | Assumption | Lexical thresholds are a proxy; every sub-moderate statement read in context | §11.23.1.3 | Accepted |
| [ASSUMPTION-1182] | Assumption | Parts 11.20–11.22 were being written in parallel; the audit is a snapshot of the parts present at the run | §11.23.1.1 | Re-run per DEC-970 at consolidation |
| [GAP-1183] | Gap | ENT-200…203 and API-556+ placeholders never assigned | §11.23.6.6 | Closed (DEC-967) |
| [CONFLICT-1184] | Conflict | V12 HTML hashes as received ≠ declared | §11.23.5.1, §11.23.8 | Resolved (DEC-968) |
| [CONFLICT-1185] | Conflict | DEC-822 narrows DEC-779 | §11.23.8 | Resolved (DEC-963) |
| [CONFLICT-1186] | Conflict | V12 REC-## vs blueprint REC-## | §11.23.8 | Resolved (DEC-964) |
| [CONFLICT-1187] | Conflict | Side-effect class vocabularies | §11.23.8 | Resolved (DEC-965) |
| [RECOMMENDATION-1188] | Recommendation | At the next revision of each earlier part, apply the errata in place and remove the stale text; until then the errata govern | §11.23.7 | Open (consolidation owner) |
| [RECOMMENDATION-1189] | Recommendation | Ask the customer to deliver future revisions with a manifest of SHA-256 values computed on LF-normalised text and to keep line endings unchanged in transit | §11.23.5.1 | Open (Product Owner) |

Tags 1190–1199 are not used.

---

## 11.23.12 Quality gate

| # | Item | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every V12 statement carries its chapter, section and statement ID in `V_audit.csv`; every restored FR cites the V12 location; every baseline status cites its authority |
| 2 | Assumptions/gaps/conflicts tagged and logged | Pass | Tags 1180–1189 in §11.23.11 |
| 3 | IDs unique and consistent with earlier parts | Pass | FR-V12-V-001…009, TC-V12-V-001…034, US-01/04/15/18/20/21-ZV, DEC-960…970, E-V-01…50 are new; no screen IDs defined; screen registry fixed by DEC-962 |
| 4 | No story lacks AC and no requirement lacks a test | Pass | 9 stories with Gherkin; each FR-V12-V maps to TC-V12-V |
| 5 | Negative, edge, security and accessibility cases covered | Pass | Integrity tampering, SoD, ungranted access, securities mandates, FX boundaries, keyboard and compact layout |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | N/A | No agent or automation added |
| 7 | Time-sensitive facts flagged "verify" with an as-of date | Pass | LGPD citation, PostgreSQL version, cost seeds and effort marked "verify (as of 28 Nov 2026)" |
| 8 | No restricted data routed to free-tier models | Pass | No model routing added; ICP forbids personal data |
| 9 | Consistent with earlier parts | Pass with findings | Inconsistencies are not edited (boundary); they are recorded as 47 errata with binding current rules (DEC-961) |

**Status: Part 11 Batch 11.23 complete. V12 → blueprint measured match 94.06% → 94.06% (100% of 19,274 statements with a verified end state: 18,090 matched, 1,011 covered in different words, 167 restored, 6 superseded); 10,569 baseline IDs checked: 0 missing, 196 amended, 11 superseded; 47 errata covering 1,667 stale occurrences; DEC-960…970.**
