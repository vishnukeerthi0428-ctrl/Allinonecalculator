## 2.6.4 Catalogue reconciliation

### 2.6.4.1 Conversion capability cards (document 13) vs Part 3.2 API catalogue and Part 3.3 entities

`build.py` extracted every "REST API / runtime interface" and "Database entities" line from the ten conversion capability cards and searched for each operation (method + path suffix) in the Part 3.2 operation tables and for each entity name in Part 3.3.

{{recon_api}}

**Finding.** All operations are already FRD-named (★) operations in Part 3.2 and all entities exist in Part 3.3. Document 13 adds no new operation or entity. Its new content is the **tool-candidate and licence lines**, dispositioned in §2.6.5.6.

### 2.6.4.2 Screen IDs referenced by the group A documents vs the Part 2.5 inventory

{{recon_screens}}

**Finding.** Every screen hop in the document 37 worked journeys resolves to a screen in the 147-screen inventory. No new screen is required by group A. The enhancements in §2.6.5 add **panels and fields to existing screens** only (§2.6.5.4).

### 2.6.4.3 Verification of repeated sections in document 14

{{recon_dup}}

### 2.6.4.4 Source personas (document 03 and document 37) vs blueprint personas and roles

| # | Source persona (SP-03 unless stated) | Blueprint persona | Blueprint role(s) | Status | Enhancement |
|---|---|---|---|---|---|
| 1 | Portfolio owner | P01 | R01 | Covered | — |
| 2 | Tenant administrator | P11 | R12 | Covered | — |
| 3 | Platform support operator | P12 | R13 | Covered | — |
| 4 | Finance controller | P08 | R08, R09 | Partially covered | BRL-ENH-A-07 no cross-entity allocation |
| 5 | Legal/compliance approver | P09 | R10 | Covered | — |
| 6 | External tenant founder | P13 | R17 → R12 of own tenant | Partially covered | Variant **P13b** |
| 7 | Service billing administrator | P12 | R14 | Covered | — |
| 8 | Growth manager | P03 | R03 | Covered | — |
| 9 | Digital marketing executive | P05 | R05 | Covered | — |
| 10 | Research analyst | P04 | R04 | Covered | — |
| 11 | Sales executive | P03 | R03 | Covered | — |
| 12 | Bid manager | P06 | R06 | Covered | — |
| 13 | Procurement manager | P07 | R07 | Partially covered | Variant **P07a** (buy-side) |
| 14 | Customer success manager | P03 (J-48) | R03 | Partially covered | Variant **P03c** |
| 15 | Healthcare partnerships manager | P03 | R03 | Partially covered | Variant **P03a** |
| 16 | Education counsellor | — | — | Not covered | Variant **P03b** |
| 17 | School administrator | P14c | R16 | Partially covered | Variant **P14e** |
| 18 | Buyer | P14d | R16 | Covered | — |
| 19 | Supplier | P14d | R16 | Covered | — |
| 20 | Commercial delivery coordinator | P07 | R07 | Partially covered | Variant **P07b** |
| 21 | Agency / managed-service operator | — | — | Not covered | New **P17**, role **R21** |
| 22 | Public visitor (website persona) | P15 | R18 | Covered | — |
| 23 | External registered user (website persona) | P14 | R16 | Covered | — |
| 24 | Website content author / publisher / reviewer | P05, P09 | R05, R05L, R10 | Partially covered | Website role mapping, BRL-ENH-A-09 |
| 25 | Admin operator | P03–P10 | R03–R11 | Covered | — |
| 26 | Integration administrator | — | — | Not covered | New **P18**, sub-role **R12I** |
| 27 | QA engineer (synthetic only) | — | (test identities) | Covered | Recorded as **P20** for completeness |
| 28 | Security/finance reviewer | P09, P08 | R15, R10, R08/R09 | Covered | — |
| 29 | SaaS applicant | P13 | R17 | Covered | Variant **P13a** recorded |
| 30 | Client administrator | P13 | R17 → R12 | Covered | — |
| 31 | Template reviewer | — | — | Not covered | New **P19**, sub-role **R11T** |
| 32 | Automation operator | P10 | R11 | Partially covered | Variant **P10a** |
| 33 | Research/qualification, document/conversation agents (SP-37 §07) | P16 | R19, R20 | Covered | — |

**Result: 33 source personas → 20 Covered, 9 Partially covered, 4 Not covered. Proposed additions: 12 variants (P03a, P03b, P03c, P07a, P07b, P10a, P13a, P13b, P14e, plus website roles P05w-author, P05w-publisher, P09w-reviewer), 4 new personas (P17–P20), 1 new role (R21) and 2 sub-roles (R11T, R12I).**

### 2.6.4.5 Optimization controls (OPT-) quoted in the group A documents vs the blueprint

The blueprint already carries 22 OPT IDs from the BRD and FRD. The group A documents quote 29 distinct OPT controls. 9 were already traced by ID; the other 20 were traced only by content (15) or are partially covered (5). The table maps each one. Measurement depth for OPT controls belongs to the document 36 reviewer; this table only closes the ID trace.

| OPT ID | Control (short) | Quoted in | Blueprint trace before this part | Status | Mapping added here |
|---|---|---|---|---|---|
| OPT-03-01 | Native versus paid plugins | 11, 12, 14 | NFR-037; PP-09 | Covered | — |
| OPT-04-01 | Daily planning and discovery | 11, 12, 13 | BRL-SRC-09; DEC-032 | Covered | — |
| OPT-05-01 | Transactional outbox | 13 | Content: Part 3.1 outbox ADR | Covered (content) | Trace OPT-05-01 → NFR-009, Part 3.1 outbox |
| OPT-08-01 | Normalization and ownership | 13 | Content: Part 3.3 scoped FKs | Covered (content) | Trace OPT-08-01 → Part 3.3 |
| OPT-09-01 | Typed contracts | 11 | Content: Part 3.2 schema, Part 6.1 contract tests | Covered (content) | Trace OPT-09-01 → Part 3.2 |
| OPT-10-01 | Rules-first model routing | 11 | NFR-030; DEC-007 | Covered | — |
| OPT-10-02 | Prompt and context efficiency, ≥ 99.5% schema-valid | 11 | Content: Part 7.3 | Covered (content) | Trace → NFR (schema validity), Part 7.3 |
| OPT-10-03 | Evidence and uncertainty, ≥ 95% grounded accuracy | 11 | Part 6.4 groundedness evals | Partially covered | Flag for the document 15 reviewer: confirm 95% as a cross-agent gate |
| OPT-10-04 | Caching and parallelism | 11 | Content: Part 7.3 cache key | Covered (content) | Trace → Part 7.3 |
| OPT-10-05 | Model fallback and local inference | 11 | DEC-007 Tier 2 | Covered (content) | Trace → DEC-007 |
| OPT-10-06 | AI attack resistance | 11 | Part 6.4; THR-052 | Covered (content) | Trace → Part 6.4 |
| OPT-11-01 | Provenance and source rights | 11, 12, 13, 14 | NFR-028 | Covered | — |
| OPT-11-02 | Freshness and completeness | 11, 13 | BRL-SRC-06 (single default) | Partially covered | BRL-ENH-A-02 per-family TTL |
| OPT-11-03 | Identity and dedupe | 11, 13 | BRL-SRC-08 | Covered (content) | Trace → BRL-SRC-08 |
| OPT-11-04 | Relevance and accuracy, stratified, recall disclosed | 11, 13 | DEC-001; KPI-01 | Partially covered | BRL-ENH-A-04 |
| OPT-11-05 | Retention and corrections | 11, 13 | Part 3.3 erasure propagation | Covered (content) | Trace → BRL-PRV |
| OPT-12-01 | Qualified funnel | 12, 13, 14 | BR-S053 | Covered | — |
| OPT-12-02 | Objections and next action | 12, 13, 14 | KPI-28 | Covered | — |
| OPT-12-03 | Verified closure | 12, 13, 14 | KPI-31; DEC-054 | Covered | Wording per CONFLICT-301 |
| OPT-12-04 | Acquisition experiments | 12, 13, 14 | BRL-MKT-10; BR-S056 | Partially covered | FR-ENH-A-011, BRL-ENH-A-13 |
| OPT-14-01 | Shared code libraries | 03 | Content: NFR-029, DEC-009 | Covered (content) | Trace → NFR-029 |
| OPT-15-01 | Adaptive navigation | 03 | NFR-034 (baseline undefined) | Partially covered | Productivity protocol §2.6.5.1.4 |
| OPT-15-02 | Accessibility and response states | 03 | Content: Part 2.5 §2.46, §2.47 | Covered (content) | Trace → Part 2.5 |
| OPT-15-03 | External portal usability | 03 | Content: Part 2.5 §2.40.2 | Covered (content) | Wording per CONFLICT-301 |
| OPT-15-04 | Saved views and bulk actions | 03 | FR-FLT-RULES (no bulk preview) | Partially covered | FR-ENH-A-019 |
| OPT-19-01…04 | Privacy and compliance (minimize, jurisdiction, rights, clinical/education) | 12, 14 | Content: BRL-PRV, DEC-029, DEC-030 | Covered (content); OPT-19-02 partially | FR-ENH-A-014 activation record |

### 2.6.4.6 Source families and MedMaarg segments (document 11) vs blueprint source policy

| Item | Source count | Blueprint equivalent | Gap closed by |
|---|---|---|---|
| Source classes (purpose/access) | 6 | BRL-SRC-01…10, A010 registry | — (Covered) |
| Source-family playbooks (organization websites … corporate reports) | 13 | Generic source records in A010; no per-family launch gate, cost line, owner or cadence | SPB-01…13 (§2.6.5.2.2) |
| MedMaarg institutional segment playbooks (hospitals … healthtech) | 11 | BR-S002 and Part 2.2 §2.21.1 (one generic institutional route); P14b | SPB-14…24 (§2.6.5.2.3) |
| Per-family freshness TTL | 0 (rule only) | BRL-SRC-06: 90 days default, tenders 7 days | BRL-ENH-A-02 (§2.6.5.3) |
| Benchmark sample size per family | 50 | none | FR-ENH-A-005 (§2.6.5.2.4) |
