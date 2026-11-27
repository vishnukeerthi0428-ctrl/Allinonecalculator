# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 3 (Batch 3.6a), Source Pack Data Catalog Reconciliation: Documents, Coverage and Catalogue Mapping

| Field | Value |
|---|---|
| Document | Part 3, Batch 3.6a · Source-pack review of document 08 (PostgreSQL Backend Table Catalog) and document 28 (Database Migration, Data Governance, Backup and Disaster Recovery) against Part 3.3 and Parts 4.2/4.3 |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | BRD, FRD, Parts 0, 0A (DEC-001…065), 1, 2.1–2.5, 3.1–3.3, 4.1–4.3, 9.1 (DEC-066…124) |
| Companion file | Part 3.6b (enhancements, conflicts, persona review, tags, quality gate) |
| Group | E (Data Architect/DBA, data governance lead, DR engineer) |
| Roles applied | Data Architect/DBA (lead), Data Governance Lead, DR/SRE Engineer, Solutions Architect, Security/Compliance Lead, QA Lead, FinOps Lead |
| Section numbering | `3.6.x` (this batch); tags ASSUMPTION/GAP/CONFLICT/RECOMMENDATION-380…399 only |
| Machine-readable outputs | `final/coverage/E_coverage.csv` (1,641 aspect rows), `final/coverage/E_table_mapping.csv` (155 rows); scripts in `assembly/source_pack/E_*.py` |

---

## 3.6.0 How to read this batch

**Purpose.** The blueprint's data layer (Part 3.3) was written from the BRD and FRD only. Its entity catalogue is a DERIVED superset of 199 logical entities, because the original 149-entity catalogue "was not supplied" (Part 3.3 §3.3.3.4, GAP-112, DEC-087). Document 08 of the source pack **is that catalogue**. This batch reconciles it table by table, column by column and constraint by constraint, reconciles document 28 (migration, governance, backup and DR) against Part 3.3 §3.3.11–§3.3.15, Part 3.1 §3.1.13 and Part 4.3 §4.37–§4.47, and then writes every missing item at full depth (Part 3.6b).

**Acronyms used in this batch.** DCE data change evidence record · DDB disposable database · DR disaster recovery · EXP exposure class · IX index · LB logical backup step · MG migration gate · OFB offboarding step · OKPI optimization KPI (pack KPI-01…35, renamed to avoid collision with business KPI-01…31) · PITR point-in-time recovery · PR post-restore reconciliation step · RD restore-drill check · RPO/RTO recovery point/time objective · RS reference SQL smoke test · SDEC source-document decision (doc 08 "DEC-039…042", renamed, CONFLICT-380) · SDR schema decision register · UQ unique constraint · VX vector/cache invalidation rule. Other acronyms as in Part 3.3 §3.3.1.3.

**Status vocabulary.** Covered · Partially covered · Not covered · Conflict · Not applicable (with reason). "Covered" for a column means the Part 3.3 table has the same column, a renamed column, or a semantically equivalent structure (named in the crosswalk). "Not covered" for a column means Part 3.6b adds it.

---

## 3.6.1 Documents reviewed

### 3.6.1.1 Document 08: PostgreSQL Backend Table Catalog

| Item | Value |
|---|---|
| File | `08_PostgreSQL_Backend_Table_Catalog` (plain-text extraction 539,787 bytes, 4,317 lines; one Heading2 block per entity) |
| Declared content | "149 logical database entities including the additional publication and external access grant entities", plus 6 candidate entities (`sales_ui_*`) |
| Parsed content (script `E_parse_doc08.py`) | 149 entity blocks (001–149) with 147–149 attribute lines each type; **735 source columns** in 149 tables plus **64 columns** in 6 candidate tables = **799 columns**; 276 constraint/index atoms; 136 physical-schema-resolution rows; 149 field-review rows; 4 source decisions (DEC-039…042, renamed SDEC-08-039…042) |
| Section list | Product purpose and operating boundary · Initial startup configurations · Technology and execution principles · Engineering contracts · Commercial PostgreSQL entity register (001–147) · 148 growth_website_publication · Website and confidential Admin operating contract · 149 sales_external_access_grant · Data integrity and replaceable adapter persistence · Migration and recovery gate · Implementation, verification and delivery controls (Physical schema acceptance; Acceptance and evidence record) · Physical schema resolution and migration gates · Optimization engineering and acceptance (Cost, Stability, Database, AI Intelligence, Data Quality, Maintainability, Optimization Intelligence) · Implementation acceptance and verification (10 procedures) · Implementation acceptance and final decision controls (10 procedures + DEC-039…042) · Current multi-startup, omnichannel and automation scope (6 candidate entities) · Applicant draft boundary |
| Per-entity attribute lines | Physical design proposal (24 entities) · Exposure (149) · Logical entity · Build/reuse (New 78, New/shared 66, Reuse–verify 3) · Primary and common fields · Business fields · Foreign keys (DB-### references) · Constraints and indexes · Protection (5 classes) · Implementation · Modules · Interfaces · Operations · Integration · Licence · Free quota · Paid rate · Allocation (B01–B10) · Source URL · Verification date |
| What it is trying to tell | A logical (not executable) inventory of every table the product needs, in two naming families: the **original commercial baseline** `growth_*` (128 tables, FRD modules M02–M66) and the **independent platform extension** `sales_*` (16 tables: tenancy, SaaS billing, bids, orders, fulfilment, data transfer, action plan), plus existing identity reuse (3) and two late additions (website publication, external access grant). It insists that nothing is a migration until each field's type, nullability, ownership, retention and index plan is approved against the real Django schema |
| Pattern | Common core (purpose, boundary, startup configurations, engineering contracts, Website/Admin contract, optimization, acceptance procedures) + catalogue body + decision gates |
| Atomic aspects found | **71 prose aspects** + **155 tables** + **799 columns** + **276 constraint atoms** + **136 schema-resolution rows** = **1,437** |

### 3.6.1.2 Document 28: Database Migration, Data Governance, Backup and Disaster Recovery

| Item | Value |
|---|---|
| File | `28_Database_Migration_Data_Governance_Backup_Disaster_Recovery` (37,715 bytes, 759 lines) |
| Section list | Purpose and operating boundary · Data classification and ownership (5 classes) · Migration procedure (Inventory, Expand, Backfill, Validate and switch, Contract, Import and export) · Backup and restore (Critical data, Research data, Restore drill, External reconciliation, Retention) · Business controls (AppNAI, MedMaarg, EduVerse, OrganicSpec, Commercial campaigns) · Logical entity inventory for migration planning (149 rows) · Completion and approval · Implementation, verification and delivery controls (Migration and recovery execution; Safe nonproduction backup/recovery rehearsal script; Acceptance and evidence record) · Database rehearsal and integrity checks · Optimization (OPT-01-01, OPT-05-01, OPT-08-01…06, OPT-18-01…04, OPT-19-01) · Implementation acceptance and verification (9 procedures) · Final decision controls · Current scope: migration and recovery of candidate tables · Applicant draft boundary |
| What it is trying to tell | How to move from the logical catalogue to a running, recoverable database without losing ownership, money or consent integrity: a five-step expand/contract method with quarantine of unknown owners, **two recovery tiers** (critical RPO ≤ 15 min, RTO ≤ 4 h initial / ≤ 2 h growth; regenerable research RPO ≤ 24 h, RTO ≤ 8 h), restore drills that disable dispatch and reconcile external effects, and evidence-based sign-off |
| Pattern | Common core + governance taxonomy + procedures + a 149-row entity inventory that repeats doc 08's exposure classes |
| Atomic aspects found | **55 prose aspects** + **149 inventory rows** = **204** |

**Common core not re-listed.** Product boundary, startup configurations, engineering contracts, the Website/Admin contract and the business controls repeat documents 01/02 and are marked "Common core: see document 01/02 coverage" in the register.

## 3.6.2 Coverage register summary

| Document | Aspect type | Total | Covered | Partially covered | Not covered | Conflict | Not applicable |
|---|---|---|---|---|---|---|---|
| 08 | Prose aspects | 71 | 41 | 22 | 5 | 2 | 1 |
| 08 | Tables (149 + 6 candidates) | 155 | 77 | 73 | 2 | 3 | 0 |
| 08 | Columns | 799 | 666 | 0 | 124 | 6 | 3 |
| 08 | Constraints and indexes | 276 | 222 | 0 | 54 | 0 | 0 |
| 08 | Schema-resolution rows | 136 | 111 | 0 | 20 | 5 | 0 |
| 28 | Prose aspects | 55 | 34 | 17 | 4 | 0 | 0 |
| 28 | Inventory rows | 149 | 149 | 0 | 0 | 0 | 0 |
| **All** | | **1641** | **1300** | **112** | **209** | **16** | **4** |

**Reading the numbers.** (1) Of 155 source tables, **77 map fully**, **73 map with column gaps**, **3 carry a column conflict** (`growth_embedding`, `growth_sequence_step`, `sales_fulfillment`) and **2 have no blueprint entity** (`sales_business_template`, `sales_ui_service_request`). (2) Of 799 source columns, **666 are already in Part 3.3** (344 same name, 119 renamed, 200 semantically equivalent, 3 identity reuse), **124 are added by Part 3.6b** (113 column additions + 11 columns of the two new entities), **6 are conflicts** with proposed resolutions and **3 are not adopted** with a reason. (3) Of 276 constraint/index atoms, **222 are covered** and **54 are added** as named keys or indexes IX-ENH-E-01…54. (4) Document 28 adds no tables; its gaps are procedures (tiered recovery objectives, restore-drill completeness, reference SQL smoke tests, disposable databases, offboarding) written in Part 3.6b §3.6.5.4–§3.6.5.5.

## 3.6.3 Detailed coverage register (prose aspects)

Every prose aspect is listed individually. Catalogue aspects (tables, columns, constraints, resolution rows, inventory rows) are listed individually in §3.6.4 and in `E_coverage.csv`.

| ID | Section | Aspect | Status | Blueprint location | Action / new IDs |
|---|---|---|---|---|---|
| 08-A001 | Cover | Scope banner: 147 interfaces (34 Website, 113 Admin); candidate API/entity additions pending reuse and approval | Covered | Part 0 §0.1; Part 2.1; Part 3.3 §3.3.3.4 | Common core: see document 01/02 coverage |
| 08-A002 | Product purpose and operating boundary | Employee-operated commercial growth; no investor/fundraising functions; owners see summaries | Covered | Part 1; DEC-002 | Common core: see document 01/02 coverage |
| 08-A003 | Product purpose and operating boundary | Independent deployment: separate DB, storage, vector index, queues, credentials, budget, billing, audit, backup | Covered | NFR-031; Part 3.1 §3.1.13; Part 3.3 §3.3.1.2 | Common core: see document 01/02 coverage |
| 08-A004 | Product purpose and operating boundary | Two React frontends, separate origins/sessions/audiences; no Admin code in public bundle | Covered | Part 3.1; Part 2.5 | Common core: see document 01/02 coverage |
| 08-A005 | Product purpose and operating boundary | 25+ startups and external tenants; tenant = security/billing boundary; startup = legal workspace; group view read-only | Covered | DEC-009, DEC-065; Part 3.3 §3.3.9 | Common core: see document 01/02 coverage |
| 08-A006 | Initial startup configurations | Four seed startups and their commercial focus | Covered | Part 1; Part 3.3 §3.3.12.6 | Common core: see document 01/02 coverage |
| 08-A007 | Technology and execution principles | Stack, open-source-first, autonomy modes, simulation zero effect, recheck at execution | Covered | Part 3.1; BRL-AUT-04; NFR-038 | Common core: see document 01/02 coverage |
| 08-A008 | Engineering contracts | REST JSON, status codes, idempotency, outbox, callbacks, retries | Covered | FRD §5; Part 3.2 | Common core: see document 01/02 coverage |
| 08-A009 | Engineering contracts | DB contract: independent DB/role, creation order, UUID PK, UTC, composite scope FK, RLS, revision, immutable financial/audit, decimal + ISO currency, provider IDs unique within connection | Covered | Part 3.3 §3.3.1.2, §3.3.5 | Common core: see document 01/02 coverage |
| 08-A010 | Commercial PostgreSQL entity register | Register intro: 147 proposed items; tenant and startup dependency mandatory for operational entities | Covered | Part 3.3 §3.3.3; this part §3.6.4 | Catalogue reconciled programmatically (§3.6.4.3) |
| 08-A011 | Entity register attribute | Per-entity Exposure class (website-mapped bounded fields vs Admin/internal only; published DTO; own-object portal DTO) | Partially covered | Part 3.3 column Class (Pub/Int/Conf/Rest); no table-level surface register | Table exposure register added (§3.6.5.3); every table assigned a surface class · GAP-391 |
| 08-A012 | Entity register attribute | Per-entity Protection class (5 values) | Partially covered | RECOMMENDATION-004 classes; §3.3.16 | Protection-to-classification mapping and gaps (int_credential_ref) added (§3.6.4.9, §3.6.5.3) · RECOMMENDATION-399 |
| 08-A013 | Entity register attribute | Build/reuse: New (78), New/shared (66), Reuse-verify (3) | Partially covered | Part 3.3 Origin column F/D16/D | Build/reuse carried into the mapping CSV; shared entities built in W0 foundation · E_table_mapping.csv |
| 08-A014 | Entity register attribute | Per-entity Modules / Interfaces / Operations usage lists | Covered | Part 3.3 basis column; Part 3.2 (API catalogue, Group D mapping) | Operation counts per table carried into E_table_mapping.csv |
| 08-A015 | Entity register attribute | Per-entity integration, licence, free quota, paid rate, budget allocation (B01-B10), source URL and verification date | Not applicable (document 16 group) | Part 7.3; DEC-020; document 16 coverage | Provider economics are reconciled by the document 16 group; prices quoted in doc 08 (checked 24 Nov 2026) must be re-verified at implementation (as of 27 Nov 2026) · ASSUMPTION-397 |
| 08-A016 | Entity register | Creation order: identity → tenant → startup/membership → configuration → FK topological → deferred cyclic FKs → indexes/projections | Covered | Part 3.3 §3.3.5.11 |  |
| 08-A017 | Entity register | Backfill and validate scoped constraints on original growth_* tables before activation | Covered | Part 4.3 §4.37.2; Part 3.6 §3.6.5.4 | Migration gate checklist added · MG-01..MG-12 |
| 08-A018 | 148 growth_website_publication | Immutable website page revision + published pointer; partial unique on published; check published implies approved hash; atomic pointer swap; cache invalidation | Partially covered | ENT-112 mkt_publication, ENT-113 snapshot, ENT-114 preview grant | approved_asset_refs, page_type mapping, partial unique index and CHECK added (§3.6.5.1) · IX-ENH-E-58..59 |
| 08-A019 | 149 sales_external_access_grant | Identity-bound revocable external grant; single-use invite; default deny | Partially covered | ENT-009 ten_portal_grant; §3.3.9.4 | contact_id, invite_token_hash, redeemed_at, state added; single-use redemption rule · GAP-389 |
| 08-A020 | Website and confidential Admin operating contract | Surface table (Public, Portal, Admin, Internal/callback), routing namespaces, domain→tenant mapping, preview grants, publish swap | Covered | Part 2.4; Part 3.2; Part 3.3 §3.3.9.4 | Common core: see document 01/02 coverage |
| 08-A021 | Data integrity and replaceable adapter persistence | Adapter selection, policy version, entitlement/quota and credential ref stored in existing integration/config structures; no plaintext secrets; no migration of private records into paid vendor workspaces without approval | Partially covered | ENT-040..042; NFR-004 | Adapter persistence rules AP-1..AP-6 added (§3.6.5.2) · RECOMMENDATION-398 |
| 08-A022 | Data integrity and replaceable adapter persistence | Test list: FKs, uniqueness, scope constraints, rollback, outbox atomicity, concurrent reservations, immutable snapshots, receipt dedupe, retention, backup/restore | Partially covered | Part 3.3 §3.3.18; Part 6 | TC-ENH-E-001…030 added (§3.6.5.6) · TC-ENH-E-001..030 |
| 08-A023 | Migration and recovery gate | Expand/backfill/validate/switch/contract; FK and financial totals; separate product backups and restore drills; no production migration without approved recovery plan | Covered | Part 4.3 §4.37, §4.47 | Gate made explicit (MG-01..MG-12) |
| 08-A024 | Migration and recovery gate | Counts: 302 API ops, 149 entities, 624 tests; 19 candidate ops, 6 candidate entities, 175 tests | Covered | Part 0; Part 3.3 §3.3.3.4 |  |
| 08-A025 | Implementation controls | 149 entities retained; 136 unresolved field/reuse records; generated DDL is not a migration | Not covered | — | Schema decision register SDR-001..136 summarised (§3.6.4.8) · GAP-392 |
| 08-A026 | Physical schema acceptance | Ownership classification (reference, tenant, issuer/startup, private grant); NOT NULL scope; composite FK | Covered | Part 3.3 §3.3.3.1 scope classes S/T/X/P; ENT-009 | Mapping of source ownership classes added (§3.6.4.9) |
| 08-A027 | Physical schema acceptance | Existing identity: confirm AUTH_USER_MODEL and membership keys; map, do not recreate | Conflict | ENT-006 ten_user identity mirror; DEC-003, DEC-019 | See CONFLICT-382 · CONFLICT-382 |
| 08-A028 | Physical schema acceptance | Currency and money: numeric(p,s), currency code, immutable adjustments, no float | Covered | Part 3.3 §3.3.5.6; CK-02/03 |  |
| 08-A029 | Physical schema acceptance | Uniqueness: exact business keys per tenant/issuer/provider; unique indexes for idempotency and receipts | Covered | Part 3.3 §3.3.8.5 | 57 additional keys/indexes (§3.6.4.7) · GAP-390 |
| 08-A030 | Physical schema acceptance | Migration: dependency order, forward compatible, rollback plan, lock/timeout, restore rehearsal | Covered | Part 4.3 §4.37.2 |  |
| 08-A031 | Physical schema acceptance | Review of unknown fields before model migration (type, nullability, constraints, relation targets, retention, index, encryption) | Partially covered | Part 3.3 §3.3.6/§3.3.7 | Decision register + column gap DDL (§3.6.5.1) · GAP-392 |
| 08-A032 | Physical schema acceptance | Field review table (149 rows: source fields + constraint + dependency/ownership) | Covered | This part §3.6.4.3/§3.6.4.5 | Reconciled row by row (E_table_mapping.csv, E_coverage.csv) |
| 08-A033 | Acceptance and evidence record | Evidence fields: responsible/reviewer, artifact/test evidence, decision, remediation, business acceptance | Partially covered | Part 4.3 A090 release evidence | Data change evidence record DCE added (§3.6.5.2) · RECOMMENDATION-398 |
| 08-A034 | Physical schema resolution | 136 prior gaps: 132 proposed types, 4 blocked (3 identity, 1 embedding dimension); 35 candidate constraints | Covered | This part §3.6.4.8 | All 136 rows reconciled; blocked rows resolved by DEC-003/019 and DEC-088 subject to CONFLICT-382 · SDEC-08-039..042 |
| 08-A035 | Physical schema resolution | Classify shareable references vs tenant-owned vs issuer-owned; SQL FK not complete authorization; review RLS with actual models | Covered | Part 3.3 §3.3.9 |  |
| 08-A036 | Optimization | OPT-03-01 native vs paid plugins | Covered | Part 0/1; DEC-020 |  |
| 08-A037 | Optimization | OPT-05-01 transactional outbox | Covered (OPT ID not cited) | NFR-006; ENT-169 | OPT ID traced in §3.6.5.2 table · RECOMMENDATION-398 |
| 08-A038 | Optimization | OPT-08-01 normalization and ownership; validated JSONB | Covered (OPT ID not cited) | Part 3.3 §3.3.5 | Traced |
| 08-A039 | Optimization | OPT-08-02 query plans: EXPLAIN (ANALYZE, BUFFERS); index actual predicates | Partially covered | IX-R6 | Index evidence rule IX-ENH-R1 added |
| 08-A040 | Optimization | OPT-08-03 ORM and connections: select_related/prefetch, projected fields, pool sizing | Partially covered | Part 3.1 (connection pooling) | DB coding rules DBC-1..DBC-6 added |
| 08-A041 | Optimization | OPT-08-04 financial storage exactness | Covered (OPT ID not cited) | §3.3.5.6; DQ-011..016 | Traced |
| 08-A042 | Optimization | OPT-08-05 vector and cache lifecycle: scope before retrieval, version embeddings, invalidate on permission/knowledge change | Partially covered | §3.3.8.4 | Invalidation triggers VX-1..VX-5 added |
| 08-A043 | Optimization | OPT-08-06 migration and archive with legal hold; reconciled row counts | Covered (OPT ID not cited) | §3.3.11, §3.3.12; Part 4.3 §4.37 | Traced |
| 08-A044 | Optimization | OPT-10-01 rules-first model routing | Covered | Part 7.3 |  |
| 08-A045 | Optimization | OPT-11-01 provenance and source rights (100% permitted provenance; quarantine missing rights) | Covered | DQ-001; BRL-SRC; OPT-11-01 cited in Part 2.3 |  |
| 08-A046 | Optimization | OPT-11-02 per-source freshness SLA; reverify before action | Covered (OPT ID not cited) | DQ-005/006 | last_fetched_at column added |
| 08-A047 | Optimization | OPT-11-03 canonical keys; never merge by name alone | Covered (OPT ID not cited) | BRL-SRC-08; DQ-004 |  |
| 08-A048 | Optimization | OPT-11-04 stratified ground truth; precision >=90% | Covered (OPT ID not cited) | DQ-009; KPI-01 |  |
| 08-A049 | Optimization | OPT-11-05 corrections/deletion propagation to caches and embeddings | Partially covered | §3.3.11; §3.3.15.3 step 6 | VX rules + TC-ENH-E-021 |
| 08-A050 | Optimization | OPT-13-01 code health | Covered (OPT ID not cited) | Part 4.3 §4.33 |  |
| 08-A051 | Optimization Intelligence | Seven Admin dashboards with persistence sources; unassessed when no denominator; stale labelled | Partially covered | §3.3.17 KPI lineage; RPT-R1 | Dashboard → table lineage (§3.6.5.2) |
| 08-A052 | Implementation acceptance | Two-tenant two-startup isolation across API, worker, cache, storage, export | Covered | Part 6.1; §3.3.9.6 | TC-ENH-E-001 |
| 08-A053 | Implementation acceptance | Query and rendering efficiency (query count, EXPLAIN ANALYZE, React rerenders) | Partially covered | Part 4.2 performance NFRs | TC-ENH-E-002 |
| 08-A054 | Implementation acceptance | Outbox crash before/after commit | Covered | NFR-006 tests | TC-ENH-E-003 |
| 08-A055 | Implementation acceptance | Catalog integrity: 138 baseline UI IDs, 302 ops, 149 entities unique and preserved | Partially covered | Part 9.3 | Entity part closed by this mapping; TC-ENH-E-004 |
| 08-A056 | Implementation acceptance | Logical/physical field completeness: no unresolved mandatory contract at migration approval | Not covered | — | SDR gate MG-03; TC-ENH-E-005 · GAP-392 |
| 08-A057 | Implementation acceptance | Tenant ownership constraints: insert child referencing foreign scope is rejected | Covered | DQ-010; §3.3.5.3 | TC-ENH-E-006 |
| 08-A058 | Implementation acceptance | Migration backward compatibility in disposable restored DB | Partially covered | Part 4.3 §4.37.2 | TC-ENH-E-007 |
| 08-A059 | Implementation acceptance | Financial exactness: decimal, currency, duplicate, excess, partial receipts | Covered | DQ-011..016 | TC-ENH-E-008 |
| 08-A060 | Implementation acceptance | Retention and scoped vector indexing: no retained unauthorized derivative | Partially covered | §3.3.11 | TC-ENH-E-009 |
| 08-A061 | Implementation acceptance | Unresolved contract decision management: every blocker has a decision queue | Not covered | — | Decision queue fields in SDR (§3.6.4.8) · GAP-392 |
| 08-A062 | Outstanding approval gates | 38 exact API definitions outstanding; 0 partial; 4 DB confirmations; 138 UI semantic mappings pending | Not covered | — | Recorded in SDR summary; API/UI items handed to Groups D and B · GAP-392 |
| 08-A063 | Final decision controls | DEC-039..042 (source) decisions for identity tables and embedding dimension | Conflict | Blueprint DEC-039 = migration (different meaning) | Renamed SDEC-08-039..042; resolutions in §3.6.6 · CONFLICT-380; CONFLICT-381 |
| 08-A064 | Current scope: data design | Reuse existing tenant, startup, run, inbound events, billing, audit; candidate entities need physical review | Covered | DEC-016 entities |  |
| 08-A065 | Candidate entities | sales_ui_application (SaaS registration intake) | Partially covered | ENT-187 saas_application_draft | application_ref, country, industry, website, service_model, terms_revision added |
| 08-A066 | Candidate entities | sales_ui_config_revision | Partially covered | ENT-168 | schema_revision added |
| 08-A067 | Candidate entities | sales_ui_trigger_revision | Partially covered | ENT-161 | concurrency_limit added |
| 08-A068 | Candidate entities | sales_ui_conflict | Partially covered | ENT-165 | decision_reason, resolved_at added |
| 08-A069 | Candidate entities | sales_ui_template_revision | Covered | ENT-167 + ENT-166 |  |
| 08-A070 | Candidate entities | sales_ui_service_request (SaaS client service request) | Not covered | — | New entity saas_service_request · GAP-388; ENT-ENH-E-02; FR-ENH-E-002 |
| 08-A071 | Applicant draft boundary | Pre-tenant opaque expiring reference; draft JSON isolated; config revision post-provision only; idempotent handoff | Covered | ENT-187 scope P; UQ-IDEM-17; BRL-SVC-02 | application_ref opaque column added |
| 28-A001 | Cover/purpose | Purpose and operating boundary; separate data, credentials, workers, audit, billing, recovery per product | Covered | NFR-031 | Common core: see document 01/02 coverage |
| 28-A002 | Purpose | All thresholds/procedures require implementation and owner approval; none asserted complete | Covered | Part 9.3 quality report | Common core: see document 01/02 coverage |
| 28-A003 | Data classification | Public snapshot: approved publication only; CDN caches public projection only; unpublish invalidates cache | Covered | ENT-112/113; BRL-PUB; Part 3.1 CDN | TC-ENH-E-010 |
| 28-A004 | Data classification | Confidential operational: scoped contacts, opportunities, conversations, evidence, workflow events | Covered | §3.3.9; scope classes |  |
| 28-A005 | Data classification | Financial and regulated: authoritative amounts, approvals, contracts, receipts; immutable corrections; finance/legal access | Covered | §3.3.5.9; FIN/CTR classes; ABAC |  |
| 28-A006 | Data classification | Secrets and documents: vault refs; private object storage with short-lived scoped access, malware scan; secret not in DB dump | Partially covered | NFR-004; ENT-041; Part 3.1 C14 | "secret not in DB dump" check added to restore drill (RD-07) and TC-ENH-E-011 |
| 28-A007 | Data classification | Derived research and embeddings: regenerable with provenance and deletion propagation; rebuild from approved sources | Partially covered | §3.3.8.4; EVD class | Regenerable class R3 recovery objectives + rebuild procedure (§3.6.5.5) · GAP-393 |
| 28-A008 | Data classification | Five-class governance taxonomy vs blueprint four-level classification | Partially covered | RECOMMENDATION-004 | Two-axis model (sensitivity level × governance class) added (§3.6.5.3) · RECOMMENDATION-398 |
| 28-A009 | Migration procedure | Inventory: reconcile existing physical tables vs catalog; exact DDL and migration graph before implementation | Partially covered | §3.3.5.11 | Inventory step MG-01 with introspection queries |
| 28-A010 | Migration procedure | Expand: nullable fields/tables, safe indexes, composite FK prerequisites; rehearsed on empty and realistic synthetic DB | Covered | Part 4.3 §4.37.2 | MG-04 |
| 28-A011 | Migration procedure | Backfill: batch by stable PK, checkpoint, explicit owner mapping, quarantine unknown owners, verify counts and sums | Partially covered | Part 4.3 §4.37.2 (batched backfill) | Owner quarantine design ops_backfill_quarantine (§3.6.5.4) · RECOMMENDATION-398 |
| 28-A012 | Migration procedure | Validate and switch via approved feature flag; observe errors and locks | Covered | §4.37.2 (NOT VALID then VALIDATE); §4.36 flags |  |
| 28-A013 | Migration procedure | Contract only after compatibility window, backup and explicit approval; prefer forward fix | Covered | §4.37.2; §4.38 |  |
| 28-A014 | Migration procedure | Import/export: validate type, schema, ownership, duplicates, size; dry run; batched commit; encrypted export with expiring link | Covered | §3.3.12; ENT-189 (72 h link) |  |
| 28-A015 | Backup and restore | Critical data RPO ≤15 min; RTO ≤4 h initial / ≤2 h growth; PITR and encrypted backups | Partially covered | DEC-018, DEC-079; NFR-056/057 | Growth-stage 2 h RTO added as scale-gate target · CONFLICT-385 |
| 28-A016 | Backup and restore | Research data RPO ≤24 h, RTO ≤8 h; source references and approved knowledge separately durable | Not covered | — | Recovery tier R3 (§3.6.5.5) · GAP-393 |
| 28-A017 | Backup and restore | Restore drill: isolated restore, disable scheduler/dispatch, verify schema/scope/balances, compare object inventory, record timestamps | Partially covered | §3.3.15.2; Part 4.3 §4.47 | RD-01..RD-12 drill checklist (§3.6.5.5) · GAP-394 |
| 28-A018 | Backup and restore | External reconciliation after restore: pending outbox, callbacks, receipts; no duplicate messages/payments | Covered | RB-007 Reconcile step | Post-restore reconciliation checklist PR-1..PR-8 |
| 28-A019 | Backup and restore | Retention: purpose-specific, legal holds, deletion reviewed vs mandatory records, purge objects/cache/embeddings/backups by lifecycle | Covered | §3.3.11 |  |
| 28-A020 | Business controls | AppNAI: tender eligibility, deadline, budget, authorized submission; award/agreement separate | Covered | BRL-BID; ENT-133 | Common core: see document 01/02 coverage |
| 28-A021 | Business controls | MedMaarg: organization-level, approved claims, no patient data | Covered | BRL-ELG-14; CK-19 | Common core: see document 01/02 coverage |
| 28-A022 | Business controls | EduVerse: routing, safeguarding, consent; external AI projects belong to AppNAI | Covered | DEC-030 | Common core: see document 01/02 coverage |
| 28-A023 | Business controls | OrganicSpec: verify parties, SKU, unit, quantity, price; separate payable/receivable ledgers | Covered | ENT-145/146; BRL-ORD-06 | Common core: see document 01/02 coverage |
| 28-A024 | Business controls | Commercial campaigns: audience, claims, consent, spend, attribution validated before publishing/sending | Covered | BRL-MKT; PDP | Common core: see document 01/02 coverage |
| 28-A025 | Logical entity inventory | 149-row entity inventory with exposure classification (for migration planning, not alphabetical DDL) | Covered | This part §3.6.4.9 | Doc 28 classification matches doc 08 exposure for 149/149 (2 wording variants) |
| 28-A026 | Completion and approval | Approval table: responsible lead, independent reviewer/QA, product owner; critical defects close before activation | Partially covered | Part 4.3 A090; Part 8.2 go-live | Data change evidence record (DCE) with three sign-offs · RECOMMENDATION-398 |
| 28-A027 | Migration and recovery execution | Inventory: actual Django models, migration graph, row counts, FKs, ownership gaps | Partially covered | §3.3.5.11 | MG-01 introspection SQL |
| 28-A028 | Migration and recovery execution | Expand with bounded locks, validate on clone, deploy compatible code | Covered | §4.37.2 lock budget |  |
| 28-A029 | Migration and recovery execution | Backfill: batched idempotent, explicit owner mapping, quarantine ambiguous; reconcile counts and totals | Partially covered | §4.37.2 | ops_backfill_quarantine; MG-06 · RECOMMENDATION-398 |
| 28-A030 | Migration and recovery execution | Validate/contract: NOT NULL/unique/FK, scoped queries, finance totals, rollback window | Covered | §4.37.2 |  |
| 28-A031 | Migration and recovery execution | Backup: encrypted automated + PITR; verify archive checksum, retention and restore credentials | Partially covered | §3.3.15.1; Part 3.1 §3.1.13.2 | Checksum manifest + restore-credential check (RD-03, RD-04) · RECOMMENDATION-399 |
| 28-A032 | Migration and recovery execution | Restore rehearsal: new isolated instance, timestamps, smoke tests, reconcile critical data, verify isolation (Ops/finance) | Covered | Part 4.3 §4.47 monthly drill | Finance sign-off made explicit (RD-10) |
| 28-A033 | Safe nonproduction rehearsal | pg_dump custom format, pg_restore --list, sha256sum; restore into NEW empty DB, never --clean on live | Partially covered | Part 3.1 weekly pg_dump | Rehearsal script LB-1 with checksum manifest (§3.6.5.5) · RECOMMENDATION-399 |
| 28-A034 | Safe nonproduction rehearsal | Measure actual loss and recovery time; investigate before activation when a target is missed | Covered | Part 4.3 §4.47 (timed report) |  |
| 28-A035 | Safe nonproduction rehearsal | Reference schema demonstrates scoped ownership and atomic budget reservation | Partially covered | ENT-052 balance_reserved trigger | Reference SQL smoke RS-1..RS-5 (§3.6.5.4) · GAP-394 |
| 28-A036 | Database rehearsal | Before: backup, schema diff, FK/unique/nullability/retention plan, lock and runtime estimate | Covered | §4.37.2; PL-07 | MG-02 |
| 28-A037 | Database rehearsal | Disposable SQL: growth_catalog_review_ DB for candidate schema; growth_reference_ DB for SQL smoke | Not covered | — | Disposable DB conventions DDB-1..DDB-5 · GAP-394 |
| 28-A038 | Database rehearsal | Rehearsal: reserve 60 of 100, reject 41 more, reject foreign tenant reservation, reject duplicate provider receipt; rollback fixture | Not covered | — | RS-1..RS-5 SQL + TC-ENH-E-012..016 · GAP-394 |
| 28-A039 | Database rehearsal | Data migration dry run with checksum, rejected rows, ownership and currency totals; approve before commit | Covered | §3.3.12.3-§3.3.12.5 |  |
| 28-A040 | Database rehearsal | Recovery: encrypted backup/PITR, isolated restore, verify ledger, grants and counts; no live restore without approval | Covered | RB-007; §4.47 |  |
| 28-A041 | Optimization | Restore in isolated DB; compare ledger and event counts before reopening; do not replay unknown external actions | Covered | RB-007 |  |
| 28-A042 | Optimization | OPT-01-01 authentication and privileged sessions | Covered | Part 4.1 |  |
| 28-A043 | Optimization | OPT-18-01 independent CI/CD; build once, promote digest | Covered (OPT ID not cited) | Part 4.3 §4.33 |  |
| 28-A044 | Optimization | OPT-18-02 migration and rollback; pause risky workflows; reconcile before resume | Covered (OPT ID not cited) | §4.37, §4.38, RB-004 |  |
| 28-A045 | Optimization | OPT-18-03 backup and DR targets (critical 15m/4h/2h; regenerable 24h/8h) | Partially covered | NFR-056/057 | Tiered objectives (§3.6.5.5) · GAP-393 |
| 28-A046 | Optimization | OPT-18-04 alerts on errors, queue age, cost anomalies, scope denials, stale projections; drills | Covered (OPT ID not cited) | Part 4.3 §4.41 |  |
| 28-A047 | Optimization | OPT-19-01 data minimization and source eligibility | Covered (OPT ID not cited) | §3.3.16; BRL-SRC |  |
| 28-A048 | Implementation acceptance | Recovery and rollback procedure with measured integrity | Covered | §4.47 quarterly drill | TC-ENH-E-017 |
| 28-A049 | Implementation acceptance | Backup and restore proof: known synthetic fixture, compare hashes, counts, reconciliation; restore never overwrites live | Partially covered | §3.3.15.2 D-1 | Fixture hash manifest; TC-ENH-E-018 |
| 28-A050 | Implementation acceptance | Retention, portability and deletion of synthetic tenant data and derivatives | Partially covered | §3.3.11; ENT-189 | TC-ENH-E-019, -021 |
| 28-A051 | Implementation acceptance | Offboarding and client independence: export, revoke access, pause queued workflows, other tenant unaffected, billing closeout | Partially covered | WF-14; ENT-189; crypto-shredding §3.3.16.4 | Data-layer offboarding runbook OFB-1..OFB-10 · GAP-395 |
| 28-A052 | Boundary and acceptance | Revalidate permission, eligibility, budget and approved content at execution; two-tenant fixture with stale grants | Covered | PDP; Part 6.1 |  |
| 28-A053 | Current scope: migration and recovery | Candidate tables: reuse/DDL review, expand-contract, backfill scope, uniqueness, rollback | Covered | §4.37.2; §3.6.4 |  |
| 28-A054 | Current scope: migration and recovery | Restore template/config history and event dedupe keys in recovery exercise | Not covered | — | RD-08, RD-09 drill checks · GAP-394 |
| 28-A055 | Applicant draft boundary | Same as 08-A071 | Covered | ENT-187 | Common core: see document 01/02 coverage |

## 3.6.4 Catalogue reconciliation

### 3.6.4.1 Method

| Step | Script (in `assembly/source_pack/`) | What it does | Output |
|---|---|---|---|
| 1 | `E_parse_doc08.py` | Parses all 149 Heading2 entity blocks of document 08 (every attribute line), the 6 candidate Heading3 blocks, the 149-row field-review table, the 136-row physical-schema-resolution table and document 28's 149-row inventory. Typed fields come from "Physical design proposal" when present, otherwise from "Business fields" or "Fields" | `doc08.json` |
| 2 | `E_parse_part33.py` | Extracts the 199-entity catalogue of Part 3.3 §3.3.3.2, the standard column sets (STD-S, STD-SA, STD-T, STD-X, STD-V, STD-W), all column rows of §3.3.6 and key columns of §3.3.7, and the §3.3.8 index/constraint lines per table | `part33.json` |
| 3 | `E_mapping.py` | Curated source-table → ENT mapping (155 entries) with match type (Renamed, Merged, Split, Reuse-mapped, New) and secondary entities | — |
| 4 | `E_reconcile.py` + `E_overrides.py` | Name and synonym match of each of the 799 columns against the mapped entities; then a reviewed decision for every column not matched by name (S = semantic equivalent, G = add column, C = conflict, N = not adopted) | `columns.csv` |
| 5 | `E_constraints.py` + curated fixes in `E_build_data.py` | Splits "Constraints and indexes" and "Candidate constraints" into 276 atoms and checks each against Part 3.3 keys, CHECKs, immutability profiles and §3.3.8 | `constraints.csv` |
| 6 | `E_build_data.py`, `E_build_md_a.py`, `E_build_md_b.py` | Writes the coverage CSV, the mapping CSV and the tables in this part | CSVs, Markdown |

Re-run: `python3 -I E_parse_doc08.py <doc08.txt> <doc28.txt> <out>/doc08.json` → `E_parse_part33.py` → `E_reconcile.py` → `E_constraints.py` → `E_build_data.py` → `E_build_md_a.py` / `E_build_md_b.py`. Every number in this batch is produced by these scripts.

### 3.6.4.2 Entity-count reconciliation (closes the open question behind GAP-112 and DEC-087)

| Line | Item | Count | Basis |
|---|---|---|---|
| a | Source tables in document 08 (001–149) | 149 | Parsed |
| b | Candidate tables (`sales_ui_*`) | 6 | Parsed |
| c | Source tables mapped to an existing Part 3.3 entity as primary target | 153 | §3.6.4.3 |
| d | Source tables with no Part 3.3 entity (new entities ENT-ENH-E-01, ENT-ENH-E-02) | 2 | GAP-388 |
| e | Part 3.3 entities that are the primary target of at least one source table | 152 | Two source tables (`existing membership table`, `sales_membership`) share ENT-008 |
| f | Part 3.3 entities reached only as a secondary target (split or normalized parts of a source table) | 17 | ENT-017, ENT-019, ENT-043, ENT-081, ENT-083, ENT-113, ENT-114, ENT-134, ENT-141, ENT-143, ENT-157, ENT-160, ENT-166, ENT-180, ENT-183, ENT-186, ENT-190 |
| g | Part 3.3 entities with **no source table** (blueprint normalization, reference data or DEC-016 derivations) | 30 | §3.6.4.4 |
| h | Check: e + f + g | 199 | = 199 |
| i | New logical entities proposed by this batch | 4 | ENT-ENH-E-01 business template, ENT-ENH-E-02 service request, ENT-ENH-E-03 fulfilment milestone (CONFLICT-383), ENT-ENH-E-04 eval case result |
| j | Blueprint logical entities after this batch | 203 | 199 + 4 (final ENT numbers ENT-200…203 to be assigned by the coordinator) |

**Finding.** The "17 retained entities the FRD never names" (Part 3.3 §3.3.3.4 line 1) are now identified: they are the 16 `sales_*` platform-extension tables plus `growth_website_publication`/`sales_external_access_grant` (with `growth_feedback`'s second meaning). All of them map to DEC-016 or batch-derived entities except `sales_business_template`. The worst case in §3.3.3.4 item 4 ("up to 17 entities this blueprint does not model") is therefore **2 entities**, now added. [ASSUMPTION-396: document 08 is the "original entity catalogue" that GAP-112 and DEC-087 refer to; on that basis GAP-112 can be closed by the coordinator.]

### 3.6.4.3 Complete source-table → blueprint-entity mapping (155 rows)

Columns: **Exp.** exposure class (EXP-ADM Admin/internal only; EXP-WEB bounded fields for mapped website/portal operations; EXP-PUB published DTO only; EXP-PRT own-object portal DTO) · **Prot.** source protection (INT internal; SCOPE tenant/startup scope; PII-R restricted business PII; AUDFIN-R restricted audit/finance; SECRET secret reference) · **Build** source build/reuse · **Match** Renamed, Merged, Split, Reuse-mapped or New · **Cols** source columns / covered / added / conflict.

| # | Source table | Exp. | Prot. | Build | → ENT | Blueprint table (+ secondary) | Scope | Imm. | Ret. | Match | Cols | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 001 | `existing user table` | EXP-WEB | INT | Reuse — verify | ENT-006 | `ten_user` | P | M | BUS | Reuse-mapped | 1/1/0/0 | Covered |
| 002 | `existing role table` | EXP-WEB | INT | Reuse — verify | ENT-007 | `ten_role` | X | M | CFG | Reuse-mapped | 1/1/0/0 | Covered |
| 003 | `existing membership table` | EXP-WEB | INT | Reuse — verify | ENT-008 | `ten_membership` (+ten_membership_grant) | T | M | AUD | Reuse-mapped | 1/1/0/0 | Covered |
| 004 | `growth_product` | EXP-ADM | INT | New / shared | ENT-016 | `cat_offering` (+ENT-017) | S | M | BUS | Merged | 4/4/0/0 | Covered |
| 005 | `growth_capability` | EXP-ADM | INT | New / shared | ENT-018 | `cat_capability` (+ENT-019) | S | M | CFG | Renamed | 4/3/1/0 | Partially covered |
| 006 | `growth_claim` | EXP-ADM | INT | New / shared | ENT-020 | `cat_claim` | S | V | CTR-like: claim + 8 y after expiry | Renamed | 5/5/0/0 | Covered |
| 007 | `growth_price_version` | EXP-ADM | INT | New / shared | ENT-021 | `cat_price_version` | S | V | FIN | Renamed | 6/6/0/0 | Covered |
| 008 | `growth_document` | EXP-WEB | INT | New | ENT-024 | `cat_document` | S | V | CFG | Renamed | 6/6/0/0 | Covered |
| 009 | `growth_document_chunk` | EXP-ADM | INT | New | ENT-025 | `cat_chunk` | S | A | CFG | Renamed | 4/3/1/0 | Partially covered |
| 010 | `growth_embedding` | EXP-ADM | INT | New / shared | ENT-026 | `cat_embedding` | S | A | CFG | Renamed | 3/2/0/1 | Conflict |
| 011 | `growth_consent` | EXP-WEB | PII-R | New / shared | ENT-027 | `gov_consent` | S | A | AUD | Renamed | 6/6/0/0 | Covered |
| 012 | `growth_suppression` | EXP-WEB | PII-R | New / shared | ENT-028 | `gov_suppression` | T | A | SUP | Renamed | 4/4/0/0 | Covered |
| 013 | `growth_policy_version` | EXP-WEB | INT | New / shared | ENT-029 | `gov_policy_version` | X | V | AUD | Renamed | 4/4/0/0 | Covered |
| 014 | `growth_integration` | EXP-ADM | INT | New / shared | ENT-040 | `int_integration` | S | M | CFG | Renamed | 4/4/0/0 | Covered |
| 015 | `growth_credential_ref` | EXP-ADM | SECRET | New / shared | ENT-041 | `int_credential_ref` | S | M | CFG | Renamed | 3/3/0/0 | Covered |
| 016 | `growth_quota` | EXP-ADM | INT | New | ENT-042 | `int_quota` | S | M | CFG | Renamed | 4/4/0/0 | Covered |
| 017 | `growth_outbox` | EXP-WEB | INT | New / shared | ENT-169 | `ops_outbox` | S | F | OPS | Renamed | 5/5/0/0 | Covered |
| 018 | `growth_audit_event` | EXP-WEB | AUDFIN-R | New / shared | ENT-172 | `ops_audit_event` | X | A | AUD | Renamed | 5/5/0/0 | Covered |
| 019 | `growth_job_run` | EXP-ADM | INT | New / shared | ENT-173 | `ops_job_run` | X | M | OPS | Renamed | 5/3/2/0 | Partially covered |
| 020 | `growth_source` | EXP-ADM | INT | New / shared | ENT-053 | `intel_source` | S | M | CFG | Renamed | 4/3/1/0 | Partially covered |
| 021 | `growth_source_policy` | EXP-ADM | INT | New / shared | ENT-054 | `intel_source_policy` | S | V | AUD | Renamed | 4/4/0/0 | Covered |
| 022 | `growth_prompt_version` | EXP-ADM | INT | New / shared | ENT-045 | `ai_prompt_version` | X | V | CFG | Renamed | 4/3/1/0 | Partially covered |
| 023 | `growth_model_run` | EXP-ADM | INT | New / shared | ENT-046 | `ai_model_run` | S | A | AIL | Renamed | 7/7/0/0 | Covered |
| 024 | `growth_eval_case` | EXP-ADM | INT | New / shared | ENT-047 | `ai_eval_case` | X | V | CFG | Renamed | 4/3/1/0 | Partially covered |
| 025 | `growth_api_usage` | EXP-ADM | INT | New / shared | ENT-050 | `ai_usage` | S | A | FIN | Renamed | 5/4/1/0 | Partially covered |
| 026 | `growth_budget` | EXP-ADM | INT | New / shared | ENT-052 | `ai_budget` | X | V | FIN | Renamed | 5/5/0/0 | Covered |
| 027 | `growth_cost_ledger` | EXP-ADM | AUDFIN-R | New / shared | ENT-051 | `ai_cost_ledger` | S | A | FIN | Renamed | 5/3/2/0 | Partially covered |
| 028 | `growth_privacy_request` | EXP-WEB | PII-R | New | ENT-036 | `gov_privacy_request` | T | M | AUD | Renamed | 4/4/0/0 | Covered |
| 029 | `growth_retention_policy` | EXP-ADM | INT | New | ENT-037 | `gov_retention_policy` | X | V | AUD | Renamed | 4/4/0/0 | Covered |
| 030 | `growth_release` | EXP-ADM | INT | New / shared | ENT-177 | `ops_release` | P | M | AUD | Renamed | 4/3/1/0 | Partially covered |
| 031 | `growth_incident` | EXP-ADM | INT | New / shared | ENT-176 | `ops_incident` | X | M | AUD | Renamed | 4/2/2/0 | Partially covered |
| 032 | `growth_search_plan` | EXP-ADM | INT | New / shared | ENT-055 | `intel_search_plan` | S | V | CFG | Renamed | 7/6/1/0 | Partially covered |
| 033 | `growth_query_run` | EXP-ADM | INT | New / shared | ENT-056 | `intel_query_run` | S | A | OPS | Renamed | 4/4/0/0 | Covered |
| 034 | `growth_source_record` | EXP-ADM | INT | New / shared | ENT-057 | `intel_source_record` | S | M | EVD | Renamed | 6/3/3/0 | Partially covered |
| 035 | `growth_fetch_log` | EXP-ADM | INT | New / shared | ENT-058 | `intel_fetch_log` | S | A | OPS | Renamed | 5/3/2/0 | Partially covered |
| 036 | `growth_evidence` | EXP-ADM | INT | New / shared | ENT-059 | `intel_evidence` | S | F | EVD | Renamed | 5/3/2/0 | Partially covered |
| 037 | `growth_organization` | EXP-ADM | INT | New / shared | ENT-063 | `intel_organization` | S | M | BUS | Renamed | 4/4/0/0 | Covered |
| 038 | `growth_org_location` | EXP-ADM | INT | New | ENT-064 | `intel_location` | S | M | BUS | Renamed | 5/5/0/0 | Covered |
| 039 | `growth_org_alias` | EXP-ADM | INT | New | ENT-065 | `intel_alias` | S | M | BUS | Renamed | 3/2/1/0 | Partially covered |
| 040 | `growth_signal_type` | EXP-ADM | INT | New | ENT-066 | `intel_signal_type` | X | M | CFG | Renamed | 3/2/1/0 | Partially covered |
| 041 | `growth_signal` | EXP-ADM | INT | New / shared | ENT-067 | `intel_signal` | S | M | EVD | Renamed | 5/5/0/0 | Covered |
| 042 | `growth_need` | EXP-ADM | INT | New / shared | ENT-068 | `intel_need` | S | M | BUS | Renamed | 5/4/1/0 | Partially covered |
| 043 | `growth_need_evidence` | EXP-ADM | INT | New | ENT-069 | `intel_need_evidence` | S | A | EVD | Renamed | 2/2/0/0 | Covered |
| 044 | `growth_solution_match` | EXP-ADM | INT | New / shared | ENT-070 | `intel_match` | S | M | BUS | Renamed | 5/2/3/0 | Partially covered |
| 045 | `growth_opportunity` | EXP-ADM | INT | New / shared | ENT-072 | `intel_opportunity` | S | M | BUS / REJ when rejected | Renamed | 5/4/1/0 | Partially covered |
| 046 | `growth_score_version` | EXP-ADM | INT | New | ENT-073 | `intel_score_version` | S | A | BUS | Renamed | 4/4/0/0 | Covered |
| 047 | `growth_contact` | EXP-WEB | PII-R | New / shared | ENT-074 | `intel_contact` | S | M | MKT | Renamed | 6/6/0/0 | Covered |
| 048 | `growth_role_hypothesis` | EXP-ADM | INT | New | ENT-075 | `intel_role_hypothesis` | S | M | MKT | Renamed | 4/3/1/0 | Partially covered |
| 049 | `growth_contact_source` | EXP-ADM | PII-R | New / shared | ENT-076 | `intel_contact_source` | S | A | MKT | Renamed | 5/3/2/0 | Partially covered |
| 050 | `growth_contact_verification` | EXP-ADM | INT | New / shared | ENT-077 | `intel_contact_verification` | S | A | MKT | Renamed | 6/5/1/0 | Partially covered |
| 051 | `growth_review` | EXP-ADM | INT | New | ENT-078 | `intel_review` | S | A | AUD | Renamed | 4/4/0/0 | Covered |
| 052 | `growth_notification` | EXP-ADM | INT | New | ENT-174 | `ops_notification` | S | M | OPS | Renamed | 4/4/0/0 | Covered |
| 053 | `growth_stage` | EXP-ADM | INT | New | ENT-084 | `crm_stage` (+ENT-083) | S | V | CFG | Split | 4/4/0/0 | Covered |
| 054 | `growth_deal` | EXP-WEB | INT | New / shared | ENT-086 | `crm_deal` | S | M | BUS | Renamed | 6/5/1/0 | Partially covered |
| 055 | `growth_activity` | EXP-ADM | INT | New / shared | ENT-088 | `crm_activity` | S | A | BUS | Renamed | 5/5/0/0 | Covered |
| 056 | `growth_form` | EXP-WEB | INT | New / shared | ENT-080 | `crm_form` (+ENT-081) | S | M | CFG | Split | 4/4/0/0 | Covered |
| 057 | `growth_submission` | EXP-WEB | PII-R | New | ENT-082 | `crm_submission` | S | A | MKT | Renamed | 5/3/2/0 | Partially covered |
| 058 | `growth_lead` | EXP-WEB | PII-R | New / shared | ENT-079 | `crm_lead` | S | M | MKT / REJ | Renamed | 5/5/0/0 | Covered |
| 059 | `growth_account_projection` | EXP-ADM | INT | New | ENT-193 | `ana_account_projection` | S | M | PRJ | Renamed | 3/3/0/0 | Covered |
| 060 | `growth_eligibility_decision` | EXP-ADM | INT | New / shared | ENT-031 | `gov_eligibility_decision` | S | A | OPS+ | Renamed | 7/6/1/0 | Partially covered |
| 061 | `growth_workflow` | EXP-ADM | INT | New | ENT-159 | `aut_workflow` (+ENT-160) | S | M | CFG | Split | 4/4/0/0 | Covered |
| 062 | `growth_workflow_execution` | EXP-ADM | INT | New | ENT-162 | `aut_run` | S | M | OPS | Renamed | 4/4/0/0 | Covered |
| 063 | `growth_step_run` | EXP-ADM | INT | New | ENT-163 | `aut_step_run` | S | M | OPS | Renamed | 5/5/0/0 | Covered |
| 064 | `growth_message_template` | EXP-ADM | INT | New / shared | ENT-090 | `eng_message_template` | S | V | CFG | Renamed | 5/4/1/0 | Partially covered |
| 065 | `growth_message_draft` | EXP-ADM | PII-R | New / shared | ENT-091 | `eng_message_draft` | S | M | MKT | Renamed | 5/4/1/0 | Partially covered |
| 066 | `growth_thread` | EXP-WEB | INT | New / shared | ENT-092 | `eng_thread` | S | M | MKT | Renamed | 5/4/1/0 | Partially covered |
| 067 | `growth_message` | EXP-WEB | PII-R | New / shared | ENT-093 | `eng_message` | S | F | MKT | Renamed | 6/6/0/0 | Covered |
| 068 | `growth_delivery_event` | EXP-ADM | INT | New / shared | ENT-094 | `eng_delivery_event` | S | A | OPS+ | Renamed | 4/4/0/0 | Covered |
| 069 | `growth_inbound_event` | EXP-ADM | PII-R | New / shared | ENT-095 | `eng_inbound_event` (+ENT-043) | S | A | MKT | Renamed | 5/4/1/0 | Partially covered |
| 070 | `growth_intent` | EXP-ADM | INT | New | ENT-096 | `eng_intent` | S | A | MKT | Renamed | 5/4/1/0 | Partially covered |
| 071 | `growth_sequence` | EXP-ADM | INT | New | ENT-100 | `eng_sequence` | S | V | CFG | Renamed | 4/4/0/0 | Covered |
| 072 | `growth_sequence_step` | EXP-ADM | INT | New | ENT-101 | `eng_sequence_step` | S | V | CFG | Renamed | 4/3/0/1 | Conflict |
| 073 | `growth_enrollment` | EXP-WEB | INT | New / shared | ENT-102 | `eng_enrollment` | S | M | MKT | Renamed | 6/6/0/0 | Covered |
| 074 | `growth_calendar_link` | EXP-WEB | INT | New | ENT-104 | `eng_calendar_link` | S | M | CFG | Renamed | 4/3/1/0 | Partially covered |
| 075 | `growth_meeting` | EXP-WEB | INT | New / shared | ENT-103 | `eng_meeting` | S | M | BUS | Renamed | 6/6/0/0 | Covered |
| 076 | `growth_metric_snapshot` | EXP-ADM | INT | New / shared | ENT-192 | `ana_metric_snapshot` | S | A | FIN-like 8 y | Renamed | 5/5/0/0 | Covered |
| 077 | `growth_task` | EXP-WEB | INT | New / shared | ENT-148 | `lcy_task` | S | M | BUS | Renamed | 5/5/0/0 | Covered |
| 078 | `growth_approval` | EXP-ADM | INT | New / shared | ENT-034 | `gov_approval` | S | A | Same as governed object | Renamed | 6/6/0/0 | Covered |
| 079 | `growth_channel_account` | EXP-ADM | INT | New / shared | ENT-089 | `eng_channel_account` | S | M | CFG | Renamed | 4/3/1/0 | Partially covered |
| 080 | `growth_chat_session` | EXP-WEB | PII-R | New | ENT-099 | `eng_chat_session` | S | M | CHT | Renamed | 3/1/2/0 | Partially covered |
| 081 | `growth_identity_link` | EXP-ADM | INT | New | ENT-097 | `eng_identity_link` | S | M | MKT | Renamed | 4/3/1/0 | Partially covered |
| 082 | `growth_routing_rule` | EXP-ADM | INT | New | ENT-098 | `eng_routing_rule` | S | V | CFG | Renamed | 5/4/1/0 | Partially covered |
| 083 | `growth_policy_decision` | EXP-ADM | INT | New | ENT-032 | `gov_policy_decision` | S | A | OPS+ | Renamed | 4/3/1/0 | Partially covered |
| 084 | `growth_compliance_incident` | EXP-ADM | INT | New | ENT-039 | `gov_compliance_incident` | S | M | AUD | Renamed | 4/2/2/0 | Partially covered |
| 085 | `growth_social_post` | EXP-ADM | INT | New | ENT-060 | `intel_social_post` | S | M | EVD | Renamed | 4/2/2/0 | Partially covered |
| 086 | `growth_content_asset` | EXP-ADM | INT | New | ENT-105 | `mkt_content_asset` | S | M | BUS | Renamed | 4/2/2/0 | Partially covered |
| 087 | `growth_content_version` | EXP-WEB | INT | New / shared | ENT-106 | `mkt_content_version` | S | V | BUS | Renamed | 5/5/0/0 | Covered |
| 088 | `growth_social_publication` | EXP-ADM | INT | New | ENT-107 | `mkt_social_publication` | S | F | BUS | Renamed | 5/5/0/0 | Covered |
| 089 | `growth_keyword` | EXP-ADM | INT | New | ENT-108 | `mkt_keyword` | S | M | BUS | Renamed | 3/3/0/0 | Covered |
| 090 | `growth_seo_issue` | EXP-ADM | INT | New | ENT-109 | `mkt_seo_issue` | S | M | OPS | Renamed | 4/3/1/0 | Partially covered |
| 091 | `growth_page_metric` | EXP-ADM | INT | New | ENT-110 | `mkt_page_metric` | S | A | BUS | Renamed | 4/4/0/0 | Covered |
| 092 | `growth_landing_page` | EXP-WEB | INT | New | ENT-111 | `mkt_landing_page` | S | M | BUS | Renamed | 4/4/0/0 | Covered |
| 093 | `growth_attribution_event` | EXP-WEB | INT | New / shared | ENT-124 | `mkt_attribution_event` | S | A | BUS | Renamed | 6/4/2/0 | Partially covered |
| 094 | `growth_audience` | EXP-ADM | INT | New | ENT-117 | `mkt_audience` | S | V | MKT | Renamed | 3/2/1/0 | Partially covered |
| 095 | `growth_campaign` | EXP-ADM | INT | New / shared | ENT-115 | `mkt_campaign` | S | M | BUS | Renamed | 4/4/0/0 | Covered |
| 096 | `growth_campaign_version` | EXP-ADM | INT | New | ENT-116 | `mkt_campaign_version` | S | V | BUS | Renamed | 4/4/0/0 | Covered |
| 097 | `growth_ad_campaign` | EXP-ADM | INT | New | ENT-118 | `mkt_ad_campaign` | S | M | FIN | Renamed | 4/3/1/0 | Partially covered |
| 098 | `growth_ad_spend_event` | EXP-ADM | INT | New | ENT-119 | `mkt_spend_event` | S | A | FIN | Renamed | 4/3/1/0 | Partially covered |
| 099 | `growth_business_event` | EXP-WEB | INT | New | ENT-120 | `mkt_event` | S | M | BUS | Renamed | 4/3/1/0 | Partially covered |
| 100 | `growth_event_registration` | EXP-WEB | INT | New | ENT-121 | `mkt_registration` | S | M | MKT | Renamed | 4/3/1/0 | Partially covered |
| 101 | `growth_event_attendance` | EXP-ADM | INT | New | ENT-122 | `mkt_attendance` | S | A | MKT | Renamed | 3/2/1/0 | Partially covered |
| 102 | `growth_partner` | EXP-WEB | INT | New / shared | ENT-153 | `lcy_partner` | S | M | BUS | Renamed | 3/3/0/0 | Covered |
| 103 | `growth_referral` | EXP-WEB | INT | New | ENT-123 | `mkt_referral` | S | M | MKT | Renamed | 4/3/1/0 | Partially covered |
| 104 | `growth_proposal` | EXP-WEB | INT | New | ENT-125 | `com_proposal` | S | M | BUS / CTR if accepted | Renamed | 2/2/0/0 | Covered |
| 105 | `growth_proposal_version` | EXP-ADM | INT | New / shared | ENT-126 | `com_proposal_version` | S | V | BUS / CTR if accepted | Renamed | 4/4/0/0 | Covered |
| 106 | `growth_quote` | EXP-WEB | INT | New / shared | ENT-127 | `com_quote` | S | F | FIN if accepted, else BUS | Renamed | 5/5/0/0 | Covered |
| 107 | `growth_quote_line` | EXP-WEB | INT | New | ENT-128 | `com_quote_line` | S | F | As quote | Renamed | 5/5/0/0 | Covered |
| 108 | `growth_objection` | EXP-ADM | INT | New | ENT-129 | `com_objection` | S | M | BUS | Renamed | 5/4/1/0 | Partially covered |
| 109 | `growth_negotiation` | EXP-ADM | INT | New | ENT-130 | `com_negotiation` | S | M | BUS | Renamed | 5/3/2/0 | Partially covered |
| 110 | `growth_contract` | EXP-WEB | AUDFIN-R | New / shared | ENT-131 | `com_contract` | S | F | CTR | Renamed | 5/5/0/0 | Covered |
| 111 | `growth_signature_event` | EXP-WEB | AUDFIN-R | New / shared | ENT-132 | `com_signature_event` | S | A | CTR | Renamed | 4/4/0/0 | Covered |
| 112 | `growth_invoice` | EXP-WEB | AUDFIN-R | New / shared | ENT-140 | `com_invoice` (+ENT-141) | S | F | FIN | Split | 4/4/0/0 | Covered |
| 113 | `growth_payment` | EXP-WEB | AUDFIN-R | New / shared | ENT-142 | `com_payment` (+ENT-143) | S | F | FIN | Split | 5/5/0/0 | Covered |
| 114 | `growth_onboarding` | EXP-WEB | INT | New | ENT-147 | `lcy_onboarding` | S | M | BUS | Renamed | 3/2/1/0 | Partially covered |
| 115 | `growth_handoff` | EXP-WEB | INT | New | ENT-149 | `lcy_handoff` | S | A | BUS | Renamed | 4/2/2/0 | Partially covered |
| 116 | `growth_pilot` | EXP-ADM | INT | New / shared | ENT-154 | `lcy_pilot` | S | M | CTR | Renamed | 4/2/2/0 | Partially covered |
| 117 | `growth_deployment` | EXP-ADM | INT | New / shared | ENT-155 | `lcy_deployment` | S | M | CTR | Renamed | 5/5/0/0 | Covered |
| 118 | `growth_subscription` | EXP-ADM | INT | New | ENT-151 | `lcy_customer_subscription` | S | M | CTR | Renamed | 4/4/0/0 | Covered |
| 119 | `growth_renewal` | EXP-WEB | INT | New | ENT-150 | `lcy_renewal` | S | M | CTR | Renamed | 3/3/0/0 | Covered |
| 120 | `growth_account_metric` | EXP-ADM | INT | New | ENT-152 | `lcy_account_metric` | S | A | BUS | Renamed | 4/4/0/0 | Covered |
| 121 | `growth_deal_outcome` | EXP-ADM | INT | New | ENT-158 | `lcy_outcome` | S | A | BUS | Renamed | 4/4/0/0 | Covered |
| 122 | `growth_feedback` | EXP-ADM | INT | New / shared | ENT-049 | `ai_feedback` (+ENT-157) | S | A | OPS | Split | 4/3/1/0 | Partially covered |
| 123 | `growth_eval_run` | EXP-ADM | INT | New | ENT-048 | `ai_eval_run` | X | A | OPS | Renamed | 4/2/2/0 | Partially covered |
| 124 | `growth_competitor` | EXP-ADM | INT | New | ENT-061 | `intel_competitor` | S | M | BUS | Renamed | 3/3/0/0 | Covered |
| 125 | `growth_market_event` | EXP-ADM | INT | New | ENT-062 | `intel_market_event` | S | M | EVD | Renamed | 4/4/0/0 | Covered |
| 126 | `growth_stage_metric` | EXP-ADM | INT | New | ENT-197 | `ana_stage_metric` | S | A | BUS | Renamed | 4/4/0/0 | Covered |
| 127 | `growth_forecast` | EXP-ADM | INT | New | ENT-196 | `ana_forecast` | S | A | BUS | Renamed | 4/3/1/0 | Partially covered |
| 128 | `growth_admin_projection` | EXP-ADM | INT | New | ENT-194 | `ana_admin_projection` | T | M | PRJ | Renamed | 3/3/0/0 | Covered |
| 129 | `growth_test_run` | EXP-ADM | INT | New | ENT-178 | `ops_test_run` | P | A | OPS | Renamed | 4/4/0/0 | Covered |
| 130 | `growth_integration_deal` | EXP-ADM | INT | New | ENT-156 | `lcy_integration_deal` | S | M | CTR | Renamed | 4/3/1/0 | Partially covered |
| 131 | `growth_launch_approval` | EXP-ADM | INT | New | ENT-023 | `cat_launch_approval` | S | A | AUD | Renamed | 4/4/0/0 | Covered |
| 132 | `sales_tenant` | EXP-ADM | SCOPE | New | ENT-001 | `ten_tenant` | P (root) | M | BUS | Renamed | 5/4/1/0 | Partially covered |
| 133 | `sales_startup` | EXP-WEB | SCOPE | New | ENT-002 | `ten_startup` | T | M | BUS | Renamed | 9/5/4/0 | Partially covered |
| 134 | `sales_membership` | EXP-ADM | SCOPE | New | ENT-008 | `ten_membership` (+ten_membership_grant) | T | M | AUD | Merged | 6/6/0/0 | Covered |
| 135 | `sales_business_template` | EXP-ADM | SCOPE | New | ENT-ENH-E-01 | `ten_business_template` (new) (+ENT-002, ENT-167) |  |  |  | New (proposed) | 8/2/6/0 | Not covered (new entity) |
| 136 | `sales_brand_domain` | EXP-WEB | SCOPE | New | ENT-005 | `ten_domain` | S | M | BUS | Renamed | 7/6/1/0 | Partially covered |
| 137 | `sales_service_plan` | EXP-ADM | SCOPE | New | ENT-179 | `saas_plan` (+ENT-180) | P | M | FIN | Split | 6/6/0/0 | Covered |
| 138 | `sales_service_subscription` | EXP-ADM | SCOPE | New | ENT-182 | `saas_subscription` | T | M | FIN | Renamed | 7/7/0/0 | Covered |
| 139 | `sales_service_invoice` | EXP-ADM | SCOPE | New | ENT-184 | `saas_service_invoice` (+ENT-185) | T | F | FIN | Split | 7/6/1/0 | Partially covered |
| 140 | `sales_support_grant` | EXP-ADM | SCOPE | New | ENT-188 | `saas_support_access_grant` | T | F | AUD | Renamed | 7/7/0/0 | Covered |
| 141 | `sales_usage_charge` | EXP-ADM | SCOPE | New | ENT-185 | `saas_service_invoice_line` (+ENT-183, ENT-186) | T | F | FIN | Split | 13/11/2/0 | Partially covered |
| 142 | `sales_data_transfer` | EXP-ADM | SCOPE | New | ENT-189 | `saas_export_job` (+ENT-190) | T | M | AUD | Split | 10/8/2/0 | Partially covered |
| 143 | `sales_action_plan` | EXP-ADM | SCOPE | New | ENT-164 | `aut_autonomy_plan` | S | M | CFG | Renamed | 11/7/4/0 | Partially covered |
| 144 | `sales_bid` | EXP-ADM | SCOPE | New | ENT-133 | `com_bid` (+ENT-134) | S | M | CTR if awarded, else BUS | Renamed | 10/8/2/0 | Partially covered |
| 145 | `sales_order` | EXP-WEB | SCOPE | New | ENT-135 | `com_order` | S | F | FIN | Renamed | 9/7/2/0 | Partially covered |
| 146 | `sales_order_line` | EXP-WEB | SCOPE | New | ENT-136 | `com_order_line` | S | F | FIN | Renamed | 10/8/2/0 | Partially covered |
| 147 | `sales_fulfillment` | EXP-WEB | SCOPE | New | ENT-137 | `com_fulfillment_event` | S | A | FIN | Renamed | 10/6/0/4 | Conflict |
| 148 | `growth_website_publication` | EXP-PUB | SCOPE (candidate) | Candidate | ENT-112 | `mkt_publication` (+ENT-113, ENT-114) | S | M | BUS | Split | 17/16/1/0 | Partially covered |
| 149 | `sales_external_access_grant` | EXP-PRT | SCOPE (candidate) | Candidate | ENT-009 | `ten_portal_grant` | S | M | AUD | Renamed | 17/13/4/0 | Partially covered |
| C1 | `sales_ui_application` | EXP-ADM (candidate) | SCOPE (candidate) | Candidate | ENT-187 | `saas_application_draft` | P (pre-tenant) | M | APP | Renamed | 13/7/6/0 | Partially covered |
| C2 | `sales_ui_config_revision` | EXP-ADM (candidate) | SCOPE (candidate) | Candidate | ENT-168 | `aut_config_revision` | X | V | CFG | Renamed | 11/10/1/0 | Partially covered |
| C3 | `sales_ui_trigger_revision` | EXP-ADM (candidate) | SCOPE (candidate) | Candidate | ENT-161 | `aut_trigger` | S | M | CFG | Renamed | 11/10/1/0 | Partially covered |
| C4 | `sales_ui_conflict` | EXP-ADM (candidate) | SCOPE (candidate) | Candidate | ENT-165 | `aut_conflict_case` (+aut_run_conflict) | S | M | OPS | Renamed | 11/9/2/0 | Partially covered |
| C5 | `sales_ui_template_revision` | EXP-ADM (candidate) | SCOPE (candidate) | Candidate | ENT-167 | `aut_workflow_template` (+ENT-166) | X | V | CFG | Renamed | 10/10/0/0 | Covered |
| C6 | `sales_ui_service_request` | EXP-ADM (candidate) | SCOPE (candidate) | Candidate | ENT-ENH-E-02 | `saas_service_request` (new) |  |  |  | New (proposed) | 8/3/5/0 | Not covered (new entity) |

Notes on non-obvious mappings: `growth_product` is merged into Offering (DEC-003, DEC-107); `growth_feedback` splits by meaning into `ai_feedback` and `lcy_feedback` (CONFLICT-106, DEC-085 pattern); `growth_business_event` is the webinar/demo event `mkt_event` (Event homonym, CONFLICT-106); `growth_workflow_execution` is `aut_run`; `growth_api_usage` is `ai_usage` and provider usage feeds SaaS meters only through DEC-086 aggregation; `sales_usage_charge` spreads over `saas_usage_meter_reading`, `saas_service_invoice_line` and `saas_credit`; `sales_data_transfer` splits by direction into `saas_export_job` and `saas_import_job`; `growth_website_publication` splits into the pointer `mkt_publication`, the immutable `mkt_publication_snapshot` and `mkt_preview_grant`.

### 3.6.4.4 Blueprint entities with no source table (30)

These are blueprint normalizations or DEC-016 derivations. None conflicts with document 08; each is required by a rule the source states in prose (for example "decimal and ISO currency", "legal holds", "idempotency key/body hash").

| ENT | Table | Origin | Basis in Part 3.3 | Why document 08 has no table |
|---|---|---|---|---|
| ENT-003 | `ten_business_line` | D16 | FR-FLT-01; FR-A100 | Business lines are folded into startup profile JSON in doc 08 (`sales_startup.profile`) |
| ENT-004 | `ten_capability_profile` | D16 | DEC-052; ABAC-08 | Doc 08 keeps startup capabilities in `sales_startup.profile/autonomy` JSON |
| ENT-010 | `ten_saved_view` | D | FR-FLT-RULES (saved views scoped to user/product/tenant/startup) | UI convenience; doc 08 lists filters per interface, not persisted views |
| ENT-011 | `ref_dataset` | D | Part 2.4 §2.33.4; CFG-32 | Doc 08 uses enums inline; blueprint centralizes reference data |
| ENT-012 | `ref_value` | D | Part 2.4 §2.33.4 | As above |
| ENT-013 | `ref_currency` | D | DEC-027 ISO 4217; NFR-017 | Doc 08 says "ISO currency" without a table |
| ENT-014 | `ref_country` | D | ISO 3166; BRL-ELG-05 | Doc 08 uses char(2) codes without a table |
| ENT-015 | `ref_unit` | D | BRL-QTE-07; DEC-045 | Doc 08 uses free-text unit |
| ENT-022 | `cat_tax_profile` | D16 | DEC-027 | Doc 08 has only `tax decimal` on order lines |
| ENT-030 | `gov_jurisdiction_rule` | D16 | DEC-029; BRL-ELG-05 | Doc 08 keeps jurisdiction inside policy JSON |
| ENT-033 | `gov_approval_policy` | D16 | DEC-038; CFG-17 | Doc 08 keeps thresholds in tenant `policy` JSON |
| ENT-035 | `gov_approval_delegation` | D | BRL-APR-09 | Not in doc 08 (BRL-APR-09) |
| ENT-038 | `gov_legal_hold` | D | DEC-028; BRL-PRV-04 | Doc 28 requires legal holds but names no table |
| ENT-044 | `ai_agent_definition` | D | DEC-048; R20 | Doc 08 has prompt versions only |
| ENT-071 | `intel_scoring_model` | D | DEC-011; BRL-SCR-01; CFG-10 | Doc 08 keeps factors on `growth_score_version` |
| ENT-085 | `crm_closure_policy` | D | DEC-054; CFG-18 | Doc 08 keeps closure evidence on the deal |
| ENT-087 | `crm_stage_transition` | D | §2.27.3; "every transition is audited" | Doc 08 "terminal transitions service-guarded" without a history table |
| ENT-138 | `com_sku_availability` | D | DEC-045 | Doc 08 has no inventory table |
| ENT-139 | `com_inventory_reservation` | D | DEC-045; BRL-ORD-04 | As above (DEC-045) |
| ENT-144 | `com_discrepancy_case` | D | BRL-FIN-03; §2.27.7 Discrepancy | Doc 08 "reconciliation" without a case table |
| ENT-145 | `com_receivable_entry` | D16 | RECOMMENDATION-018; BRL-ORD-06 | Doc 08 "distinct payable/receivable" on orders only |
| ENT-146 | `com_payable_entry` | D16 | RECOMMENDATION-018; BRL-ORD-06 | As above |
| ENT-170 | `ops_domain_event` | D | Part 2.4 §2.31.1 | Doc 08 relies on outbox only |
| ENT-171 | `ops_idempotency_key` | D | NFR-015 "idempotency key + body hash"; CA-INTAKE | Doc 08 states the rule (idempotency key/body hash) without a table |
| ENT-175 | `ops_notification_preference` | D | DEC-036; CFG-30 | Not in doc 08 (DEC-036) |
| ENT-181 | `saas_entitlement` | D16 | DEC-047; BRL-SVC-03 | Doc 08 keeps entitlements as JSON on plan/subscription |
| ENT-191 | `ana_metric_definition` | D | Part 2.4 §2.31.1; CFG-21 | Doc 08 has metric_key strings only |
| ENT-195 | `ana_pipeline_projection` | D | RP-01, RP-02 (funnel and pipeline read models) | Doc 08 has two projections only |
| ENT-198 | `ana_fx_snapshot` | D16 | DEC-027 | Doc 08 has no FX table (DEC-027) |
| ENT-199 | `ana_report_subscription` | D | Part 2.4 §2.31.5 | Not in doc 08 (Part 2.4 §2.31.5) |

### 3.6.4.5 Column-level reconciliation

**Totals (799 columns).** Same name 344 · renamed (synonym rule) 119 · semantically equivalent structure 200 · identity reuse 3 · **added in Part 3.6b 113** · **new-entity columns 11** · **conflict 6** · not adopted 3.

#### (a) Column gaps, conflicts and non-adoptions (every item listed)

The "Proposed column / resolution" text is the exact DDL intent; the consolidated `ALTER TABLE` statements are in Part 3.6b §3.6.5.1. All additions carry tag GAP-389 unless another tag is shown.

| # | Source table.column | Source type | → Blueprint table | Decision | Proposed column / resolution |
|---|---|---|---|---|---|
| 1 | `growth_capability.limitations` | text | `cat_capability` | Add column | limitations text NULL (Pub after approval) |
| 2 | `growth_document_chunk.source_locator` | text | `cat_chunk` | Add column | source_locator text NULL (page/section/char offsets for citations) |
| 3 | `growth_embedding.vector` | vector(d) (Blocked — embedding model dimensions) | `cat_embedding` | Conflict | embedding vector(n): dimension fixed by DEC-042 (source) / RECOMMENDATION-039; see CONFLICT-381 |
| 4 | `growth_job_run.job_key` | text | `ops_job_run` | Add column | job_key text NOT NULL (deterministic run key); UQ (COALESCE(tenant_id), job_key) |
| 5 | `growth_job_run.next_retry` | timestamptz | `ops_job_run` | Add column | next_retry_at timestamptz NULL (A-screen retry queue) |
| 6 | `growth_source.name` | text | `intel_source` | Add column | name text NOT NULL |
| 7 | `growth_prompt_version.body` | text | `ai_prompt_version` | Add column | template_body text NOT NULL (hash = template_hash) |
| 8 | `growth_eval_case.case_key` | text | `ai_eval_case` | Add column | case_code text NOT NULL; UQ (COALESCE(tenant_id), suite_code, case_code, version_no) |
| 9 | `growth_api_usage.integration_id` | uuid | `ai_usage` | Add column | integration_id uuid NULL -> int_integration (non-model provider usage, B03) |
| 10 | `growth_cost_ledger.usage_id` | uuid nullable | `ai_cost_ledger` | Add column | usage_id uuid NULL -> ai_usage (in addition to source_type/source_id) |
| 11 | `growth_cost_ledger.entry_key` | text | `ai_cost_ledger` | Add column | entry_key text NOT NULL; UQ (tenant_id, entry_key) idempotent ledger post |
| 12 | `growth_release.environment` | text | `ops_release` | Add column | environment text NOT NULL CHECK IN (dev, staging, prod) |
| 13 | `growth_incident.job_run_id` | uuid nullable | `ops_incident` | Add column | job_run_id uuid NULL -> ops_job_run |
| 14 | `growth_incident.summary` | text | `ops_incident` | Add column | summary text NULL (Int, no personal data) |
| 15 | `growth_search_plan.product_id` | uuid | `intel_search_plan` | Add column | offering_id uuid NULL -> cat_offering |
| 16 | `growth_source_record.query_run_id` | uuid nullable | `intel_source_record` | Add column | query_run_id uuid NULL -> intel_query_run (lineage) |
| 17 | `growth_source_record.content_hash` | text | `intel_source_record` | Add column | content_hash char(64) NULL (change detection) |
| 18 | `growth_source_record.fetched_at` | timestamptz | `intel_source_record` | Add column | last_fetched_at timestamptz NULL (freshness SLA, OPT-11-02) |
| 19 | `growth_fetch_log.source_id` | uuid | `intel_fetch_log` | Add column | source_id uuid NOT NULL -> intel_source (failed fetch has no record) |
| 20 | `growth_fetch_log.query_run_id` | uuid | `intel_fetch_log` | Add column | query_run_id uuid NULL -> intel_query_run |
| 21 | `growth_evidence.locator` | text | `intel_evidence` | Add column | locator text NULL (citation anchor) |
| 22 | `growth_evidence.verified_at` | timestamptz | `intel_evidence` | Add column | verified_at timestamptz NULL + verified_by uuid NULL |
| 23 | `growth_org_alias.source_record_id` | uuid nullable | `intel_alias` | Add column | source_record_id uuid NULL -> intel_source_record (OPT-11-01 provenance) |
| 24 | `growth_signal_type.rules` | jsonb | `intel_signal_type` | Add column | detection_rules jsonb NULL (schema-validated, rules-first Tier 0) |
| 25 | `growth_need.confidence` | decimal | `intel_need` | Add column | confidence numeric(5,4) NULL CHECK 0-1 |
| 26 | `growth_solution_match.capability_id` | uuid | `intel_match` | Add column | capability_id uuid NULL -> cat_capability |
| 27 | `growth_solution_match.rationale` | text | `intel_match` | Add column | rationale text NULL (explainability, Int) |
| 28 | `growth_solution_match.state` | text | `intel_match` | Add column | state text NOT NULL DEFAULT proposed CHECK IN (proposed, accepted, rejected, superseded) |
| 29 | `growth_opportunity.expires_at` | timestamptz | `intel_opportunity` | Add column | expires_at timestamptz NULL (opportunity freshness) |
| 30 | `growth_role_hypothesis.opportunity_id` | uuid | `intel_role_hypothesis` | Add column | opportunity_id uuid NULL -> intel_opportunity |
| 31 | `growth_contact_source.source_record_id` | uuid nullable | `intel_contact_source` | Add column | source_record_id uuid NULL -> intel_source_record |
| 32 | `growth_contact_source.provider_ref` | text | `intel_contact_source` | Add column | provider_ref text NULL (licensed data provider record id) |
| 33 | `growth_contact_verification.contact_source_id` | uuid | `intel_contact_verification` | Add column | contact_source_id uuid NULL -> intel_contact_source |
| 34 | `growth_deal.closure_evidence_ref` | text nullable | `crm_deal` | Add column | closure_evidence_ref text NULL (DEC-054 closure evidence; required when closure_status = won) |
| 35 | `growth_submission.subject_key` | text | `crm_submission` | Add column | subject_hmac char(64) NULL (dedupe, Rest) |
| 36 | `growth_submission.consent_id` | uuid nullable | `crm_submission` | Add column | consent_id uuid NULL -> gov_consent |
| 37 | `growth_eligibility_decision.expires_at` | timestamptz | `gov_eligibility_decision` | Add column | valid_until timestamptz NULL (decision reuse window; dispatch rechecks) |
| 38 | `growth_message_template.template_key` | text | `eng_message_template` | Add column | template_code text NOT NULL; UQ (tenant_id, startup_id, template_code, version_no) |
| 39 | `growth_message_draft.eligibility_decision_id` | uuid | `eng_message_draft` | Add column | eligibility_decision_id uuid NULL -> gov_eligibility_decision (draft-time check) |
| 40 | `growth_thread.external_thread_ref` | text | `eng_thread` | Add column | external_thread_ref text NULL; UQ (channel_account_id, external_thread_ref) |
| 41 | `growth_inbound_event.state` | text | `eng_inbound_event` | Add column | processing_state text NOT NULL DEFAULT received CHECK IN (received, classified, routed, quarantined, failed) |
| 42 | `growth_intent.action` | text | `eng_intent` | Add column | action_taken text NULL CHECK IN (none, task, stop, route, escalate) |
| 43 | `growth_sequence_step.delay_seconds` | int | `eng_sequence_step` | Conflict | wait_business_days retained (BRL business-day cadence); see CONFLICT-382 |
| 44 | `growth_calendar_link.external_calendar_id` | text | `eng_calendar_link` | Add column | external_calendar_id text NULL |
| 45 | `growth_channel_account.state` | text | `eng_channel_account` | Add column | state text NOT NULL DEFAULT pending CHECK IN (pending, verified, active, paused, revoked) |
| 46 | `growth_chat_session.thread_id` | uuid | `eng_chat_session` | Add column | thread_id uuid NULL -> eng_thread |
| 47 | `growth_chat_session.opaque_token_hash` | text | `eng_chat_session` | Add column | session_token_hash char(64) NOT NULL UNIQUE (Rest) |
| 48 | `growth_identity_link.channel_account_id` | uuid | `eng_identity_link` | Add column | channel_account_id uuid NULL -> eng_channel_account |
| 49 | `growth_routing_rule.channel` | text | `eng_routing_rule` | Add column | channel text NULL (rule applies to channel) |
| 50 | `growth_policy_decision.policy_version_id` | uuid | `gov_policy_decision` | Add column | policy_version_id uuid NOT NULL -> gov_policy_version |
| 51 | `growth_compliance_incident.policy_decision_id` | uuid nullable | `gov_compliance_incident` | Add column | policy_decision_id uuid NULL -> gov_policy_decision |
| 52 | `growth_compliance_incident.message_id` | uuid nullable | `gov_compliance_incident` | Add column | message_id uuid NULL -> eng_message |
| 53 | `growth_social_post.source_record_id` | uuid | `intel_social_post` | Add column | source_record_id uuid NULL -> intel_source_record |
| 54 | `growth_social_post.permalink` | text | `intel_social_post` | Add column | permalink text NULL |
| 55 | `growth_content_asset.product_id` | uuid | `mkt_content_asset` | Add column | offering_id uuid NULL -> cat_offering |
| 56 | `growth_content_asset.state` | text | `mkt_content_asset` | Add column | state text NOT NULL DEFAULT draft CHECK IN (draft, in_review, approved, retired) |
| 57 | `growth_seo_issue.keyword_id` | uuid nullable | `mkt_seo_issue` | Add column | keyword_id uuid NULL -> mkt_keyword |
| 58 | `growth_attribution_event.landing_page_id` | uuid nullable | `mkt_attribution_event` | Add column | landing_page_id uuid NULL -> mkt_landing_page |
| 59 | `growth_attribution_event.event_key` | text | `mkt_attribution_event` | Add column | event_key text NOT NULL; UQ (tenant_id, startup_id, event_key) dedupe |
| 60 | `growth_audience.name` | text | `mkt_audience` | Add column | name text NOT NULL |
| 61 | `growth_ad_campaign.channel_account_id` | uuid | `mkt_ad_campaign` | Add column | channel_account_id uuid NULL -> eng_channel_account |
| 62 | `growth_ad_spend_event.event_key` | text | `mkt_spend_event` | Add column | event_key text NOT NULL; UQ (ad_campaign_id, event_key) |
| 63 | `growth_business_event.product_id` | uuid | `mkt_event` | Add column | offering_id uuid NULL -> cat_offering |
| 64 | `growth_event_registration.lead_id` | uuid | `mkt_registration` | Add column | lead_id uuid NULL -> crm_lead |
| 65 | `growth_event_attendance.provider_ref` | text | `mkt_attendance` | Add column | provider_ref text NULL; UQ (registration_id, provider_ref) |
| 66 | `growth_referral.lead_id` | uuid | `mkt_referral` | Add column | lead_id uuid NULL -> crm_lead |
| 67 | `growth_objection.thread_id` | uuid nullable | `com_objection` | Add column | thread_id uuid NULL -> eng_thread |
| 68 | `growth_negotiation.quote_id` | uuid | `com_negotiation` | Add column | quote_id uuid NULL -> com_quote |
| 69 | `growth_negotiation.proposed_terms` | jsonb | `com_negotiation` | Add column | proposed_terms jsonb NULL (schema-validated, Conf) |
| 70 | `growth_signature_event.state` | text | `com_signature_event` | Not adopted | append-only signature event; state derived from event type (method) |
| 71 | `growth_onboarding.owner_id` | user_fk | `lcy_onboarding` | Add column | owner_id uuid NOT NULL -> ten_user |
| 72 | `growth_handoff.task_id` | uuid | `lcy_handoff` | Add column | task_id uuid NULL -> lcy_task; UQ (onboarding_id, task_id) |
| 73 | `growth_handoff.target_team` | text | `lcy_handoff` | Add column | to_team text NULL |
| 74 | `growth_handoff.state` | text | `lcy_handoff` | Not adopted | handoff is append-only; acceptance recorded as new task/handoff row |
| 75 | `growth_pilot.deal_id` | uuid | `lcy_pilot` | Add column | deal_id uuid NULL -> crm_deal |
| 76 | `growth_pilot.scope` | jsonb | `lcy_pilot` | Add column | scope jsonb NULL (schema-validated) |
| 77 | `growth_feedback.correction` | jsonb | `ai_feedback` | Add column | correction jsonb NULL (structured human correction, Conf) |
| 78 | `growth_eval_run.eval_case_id` | uuid | `ai_eval_run` | Add column | ai_eval_case_result (new ENT-ENH-E-04) child rows (eval_run_id, eval_case_id, passed, result) |
| 79 | `growth_eval_run.result` | jsonb | `ai_eval_run` | Add column | ai_eval_case_result.result jsonb |
| 80 | `growth_forecast.model_version` | text | `ana_forecast` | Add column | model_version text NULL |
| 81 | `growth_integration_deal.deal_id` | uuid | `lcy_integration_deal` | Add column | deal_id uuid NULL -> crm_deal |
| 82 | `growth_launch_approval.state` | text | `cat_launch_approval` | Not adopted | append-only launch approval; from_readiness/to_readiness carry the transition |
| 83 | `sales_tenant.policy` | jsonb | `ten_tenant` | Add column | policy jsonb NOT NULL DEFAULT {} (tenant guardrails, schema-validated) |
| 84 | `sales_startup.industry` | text | `ten_startup` | Add column | industry_code text NULL |
| 85 | `sales_startup.profile` | jsonb | `ten_startup` | Add column | profile jsonb NOT NULL DEFAULT {} |
| 86 | `sales_startup.autonomy` | jsonb | `ten_startup` | Add column | autonomy_caps jsonb NOT NULL DEFAULT {} (DEC caps) |
| 87 | `sales_startup.approved_hash` | char(64) | `ten_startup` | Add column | approved_config_hash char(64) NULL |
| 88 | `sales_business_template.template_key` | text | `ten_business_template` | New entity | ENT-ENH-E-01 |
| 89 | `sales_business_template.schema` | jsonb | `ten_business_template` | New entity | ENT-ENH-E-01 |
| 90 | `sales_business_template.defaults` | jsonb | `ten_business_template` | New entity | ENT-ENH-E-01 |
| 91 | `sales_business_template.hash` | char(64) | `ten_business_template` | New entity | ENT-ENH-E-01 |
| 92 | `sales_business_template.approval_id` | uuid | `ten_business_template` | New entity | ENT-ENH-E-01 |
| 93 | `sales_business_template.state` | text | `ten_business_template` | New entity | ENT-ENH-E-01 |
| 94 | `sales_brand_domain.brand` | jsonb | `ten_domain` | Add column | brand jsonb NULL (logo/colour tokens; approved assets only) |
| 95 | `sales_service_invoice.payment_ref` | text | `saas_service_invoice` | Add column | payment_ref text NULL (provider receipt id; UQ with provider account) |
| 96 | `sales_usage_charge.cost` | numeric(18,2) | `saas_service_invoice_line` | Add column | cost_amount numeric(18,4) NULL (FinOps margin, Conf) |
| 97 | `sales_usage_charge.rate_snapshot` | jsonb | `saas_service_invoice_line` | Add column | rate_snapshot jsonb NOT NULL (plan version rates at rating time) |
| 98 | `sales_data_transfer.checksum` | char(64) | `saas_export_job` | Add column | file_sha256 char(64) NULL |
| 99 | `sales_data_transfer.manifest` | jsonb | `saas_export_job` | Add column | manifest jsonb NULL (entities, row counts, schema versions) |
| 100 | `sales_action_plan.input_hash` | char(64) | `aut_autonomy_plan` | Add column | input_hash char(64) NOT NULL |
| 101 | `sales_action_plan.policy_hash` | char(64) | `aut_autonomy_plan` | Add column | policy_hash char(64) NOT NULL |
| 102 | `sales_action_plan.actions` | jsonb | `aut_autonomy_plan` | Add column | planned_actions jsonb NOT NULL |
| 103 | `sales_action_plan.simulation` | jsonb | `aut_autonomy_plan` | Add column | simulation_result jsonb NULL |
| 104 | `sales_bid.opportunity_id` | uuid | `com_bid` | Add column | opportunity_id uuid NULL -> intel_opportunity |
| 105 | `sales_bid.proposal_id` | uuid | `com_bid` | Add column | proposal_id uuid NULL -> com_proposal |
| 106 | `sales_order.quote_id` | uuid | `com_order` | Add column | quote_id uuid NULL -> com_quote |
| 107 | `sales_order.external_ref` | text | `com_order` | Add column | external_ref text NULL (counterparty PO no.; UQ per counterparty) |
| 108 | `sales_order_line.description` | text | `com_order_line` | Add column | description text NULL |
| 109 | `sales_order_line.tax` | decimal | `com_order_line` | Add column | tax_amount numeric(18,2) NOT NULL DEFAULT 0 |
| 110 | `sales_fulfillment.order_id` | uuid | `com_fulfillment_event` | Conflict | com_fulfillment_milestone (new ENT-ENH-E-03) carries order_id; see CONFLICT-383 |
| 111 | `sales_fulfillment.due_at` | timestamptz | `com_fulfillment_event` | Conflict | com_fulfillment_milestone.due_at |
| 112 | `sales_fulfillment.accepted_at` | timestamptz | `com_fulfillment_event` | Conflict | com_fulfillment_milestone.accepted_at |
| 113 | `sales_fulfillment.state` | text | `com_fulfillment_event` | Conflict | com_fulfillment_milestone.state |
| 114 | `growth_website_publication.approved_asset_refs` | jsonb | `mkt_publication` | Add column | approved_asset_refs jsonb NOT NULL DEFAULT [] on mkt_publication_snapshot |
| 115 | `sales_external_access_grant.contact_id` | uuid | `ten_portal_grant` | Add column | contact_id uuid NULL -> intel_contact |
| 116 | `sales_external_access_grant.invite_secret_hash` | char(64) | `ten_portal_grant` | Add column | invite_token_hash char(64) NULL UNIQUE (Rest) |
| 117 | `sales_external_access_grant.redeemed_at` | timestamptz | `ten_portal_grant` | Add column | redeemed_at timestamptz NULL |
| 118 | `sales_external_access_grant.state` | text | `ten_portal_grant` | Add column | state text NOT NULL DEFAULT invited CHECK IN (invited, active, expired, revoked) |
| 119 | `sales_ui_application.application_ref` | uuid | `saas_application_draft` | Add column | application_ref uuid NOT NULL UNIQUE (opaque, separate from id) |
| 120 | `sales_ui_application.country` | char(2) | `saas_application_draft` | Add column | country_code char(2) NULL |
| 121 | `sales_ui_application.industry` | text | `saas_application_draft` | Add column | industry_code text NULL |
| 122 | `sales_ui_application.website` | text | `saas_application_draft` | Add column | website text NULL |
| 123 | `sales_ui_application.service_model` | text | `saas_application_draft` | Add column | service_model text NULL CHECK IN (owned, saas) |
| 124 | `sales_ui_application.terms_revision` | text | `saas_application_draft` | Add column | terms_revision text NOT NULL |
| 125 | `sales_ui_config_revision.schema_revision` | integer | `aut_config_revision` | Add column | schema_revision integer NOT NULL |
| 126 | `sales_ui_trigger_revision.concurrency_limit` | integer | `aut_trigger` | Add column | concurrency_limit integer NOT NULL DEFAULT 1 CHECK 1-20 |
| 127 | `sales_ui_conflict.reason` | text nullable | `aut_conflict_case` | Add column | decision_reason text NULL |
| 128 | `sales_ui_conflict.resolved_at` | timestamptz nullable | `aut_conflict_case` | Add column | resolved_at timestamptz NULL |
| 129 | `sales_ui_service_request.requester_ref` | text | `saas_service_request` | New entity | ENT-ENH-E-02 |
| 130 | `sales_ui_service_request.kind` | text | `saas_service_request` | New entity | ENT-ENH-E-02 |
| 131 | `sales_ui_service_request.description` | text | `saas_service_request` | New entity | ENT-ENH-E-02 |
| 132 | `sales_ui_service_request.status` | text | `saas_service_request` | New entity | ENT-ENH-E-02 |
| 133 | `sales_ui_service_request.resolved_at` | timestamptz nullable | `saas_service_request` | New entity | ENT-ENH-E-02 |

#### (b) Column crosswalk for renamed and semantically equivalent columns

Developers porting code or tests written against document 08 names use this crosswalk. Same-name columns are omitted.

| Source table | Source column → blueprint column (renamed or semantic) |
|---|---|
| `growth_product → cat_offering` | readiness → readiness_state; active → status |
| `growth_capability → cat_capability` | product_id → offering_version_id |
| `growth_claim → cat_claim` | product_id → offering_version_id; evidence_ref → cat_claim_evidence association + evidence_count; approved_by → approval_id |
| `growth_price_version → cat_price_version` | product_id → offering_version_id; amount → unit_price |
| `growth_document → cat_document` | product_id → cat_document_offering association; object_key → storage_key; version → version_no |
| `growth_embedding → cat_embedding` | model → model_id |
| `growth_consent → gov_consent` | subject_key → contact_id; state → action (grant/withdraw, append-only); occurred_at → effective_at |
| `growth_suppression → gov_suppression` | subject_key → identifier_hmac; active → expires_at / lifted_by_id (append-only lift rows) |
| `growth_policy_version → gov_policy_version` | policy_key → policy_code; version → version_no; rules → body |
| `growth_integration → int_integration` | provider → provider_code; channel → adapter_kind; status → state |
| `growth_credential_ref → int_credential_ref` | secret_ref → secret_arn; rotated_at → last_rotated_at |
| `growth_quota → int_quota` | limit → limit_value; used → consumed |
| `growth_outbox → ops_outbox` | event_key → dedup_key; event_type → topic; state → status |
| `growth_audit_event → ops_audit_event` | metadata → field_diff / reason_codes |
| `growth_job_run → ops_job_run` | status → state; attempts → attempt; error_code → error_class |
| `growth_source → intel_source` | base_url → host + path_prefix; category → source_kind; status → state |
| `growth_source_policy → intel_source_policy` | policy_version_id → STD-V version_no (source policy versioned in place); gov link via approval_id |
| `growth_prompt_version → ai_prompt_version` | prompt_key → prompt_code; version → version_no |
| `growth_model_run → ai_model_run` | job_run_id → correlation_id; model → model_id; result_ref → payload_storage_key; state → outcome |
| `growth_eval_case → ai_eval_case` | active → status |
| `growth_api_usage → ai_usage` | request_key → provider_call_ref; units → quantity; recorded_at → created_at |
| `growth_budget → ai_budget` | scope → scope_level + scope_ref; period_start → period; limit_inr → cap_amount + currency; reserved_inr → balance_reserved; spent_inr → balance_settled |
| `growth_cost_ledger → ai_cost_ledger` | amount_inr → amount; kind → entry_type |
| `growth_privacy_request → gov_privacy_request` | subject_key → subject_hmac; kind → request_type |
| `growth_retention_policy → gov_retention_policy` | retention_days → retention_period; version → version_no; active → status |
| `growth_release → ops_release` | version → revision |
| `growth_search_plan → intel_search_plan` | source_id → source_ids; query → query_spec; segment → query_spec.segment; geography → query_spec.geography; schedule → schedule_cron; active → status |
| `growth_query_run → intel_query_run` | job_run_id → correlation_id; started_at → created_at |
| `growth_fetch_log → intel_fetch_log` | fetched_at → created_at; error_code → outcome |
| `growth_evidence → intel_evidence` | excerpt → content_text |
| `growth_organization → intel_organization` | canonical_domain → primary_domain; sector → industry_code; status → merged_into_id / archived_at |
| `growth_org_location → intel_location` | region → subdivision_code; country → country_code |
| `growth_org_alias → intel_alias` | alias → alias_name |
| `growth_signal → intel_signal` | evidence_id → intel_signal_evidence association |
| `growth_need → intel_need` | signal_id → source_signal_id; description → statement; verification_state → state |
| `growth_solution_match → intel_match` | score → match_score |
| `growth_score_version → intel_score_version` | version → revision; factors → components |
| `growth_contact → intel_contact` | professional_name → full_name; work_email → email_enc; business_phone → phone_enc; role_title → job_title; state → verification_state |
| `growth_role_hypothesis → intel_role_hypothesis` | role_title → role_code |
| `growth_contact_source → intel_contact_source` | license_ref → licence_basis; retrieved_at → observed_at |
| `growth_contact_verification → intel_contact_verification` | state → result; verified_at → created_at (append-only row) |
| `growth_review → intel_review` | reason → reason_code (+ free text in Part 3.6 reason_text) |
| `growth_notification → ops_notification` | review_id → event_ref; type → category; read_at → acknowledged_at |
| `growth_stage → crm_stage` | pipeline_key → pipeline_id; terminal → is_terminal |
| `growth_deal → crm_deal` | value_inr → expected_value |
| `growth_activity → crm_activity` | deal_id → subject_type = deal + subject_id; actor_id → created_by; kind → activity_type |
| `growth_form → crm_form` | slug → form_code; schema → field_schema; version → version_no |
| `growth_submission → crm_submission` | form_id → form_version_id; submission_key → idempotency_key; payload → payload_min |
| `growth_account_projection → ana_account_projection` | last_event_key → last_event_seq |
| `growth_eligibility_decision → gov_eligibility_decision` | policy_version_id → policy_version_ids; subject_key → contact_id; channel → action_type; allowed → result; reason → reason_codes |
| `growth_workflow → aut_workflow` | workflow_key → workflow_code; version → version_no; definition → aut_workflow_revision.dag_spec; state → status |
| `growth_workflow_execution → aut_run` | workflow_id → workflow_revision_id; trigger_key → trigger_id |
| `growth_step_run → aut_step_run` | execution_id → run_id; step_key → node_key; attempts → attempt; result_ref → output_digest |
| `growth_message_template → eng_message_template` | version → version_no; state → status |
| `growth_thread → eng_thread` | channel → primary_channel |
| `growth_message → eng_message` | body → body_storage_key |
| `growth_delivery_event → eng_delivery_event` | provider_event_key → provider_event_id; state → event_type |
| `growth_inbound_event → eng_inbound_event` | provider_event_key → provider_event_id; payload_ref → body_storage_key |
| `growth_intent → eng_intent` | thread_id → via inbound_event_id; label → intent_code |
| `growth_sequence → eng_sequence` | sequence_key → code; version → version_no; state → status; stop_rules → stop_conditions |
| `growth_enrollment → eng_enrollment` | deal_id → relationship_key; next_step_id → current_step_ordinal; next_at → next_due_at |
| `growth_calendar_link → eng_calendar_link` | owner_id → user_id; timezone → ten_user.timezone + work_hours |
| `growth_meeting → eng_meeting` | start_at → starts_at; end_at → ends_at; external_ref → provider_event_ref |
| `growth_metric_snapshot → ana_metric_snapshot` | metric_key → metric_definition_id; dimensions → scope; computed_at → as_of |
| `growth_task → lcy_task` | deal_id → subject_type = deal + subject_id; owner_id → assignee_id |
| `growth_approval → gov_approval` | reviewer_id → approver_id; reason → reason_code / reason_text |
| `growth_channel_account → eng_channel_account` | external_account_id → sender_identity |
| `growth_identity_link → eng_identity_link` | external_subject_hash → address_hmac |
| `growth_routing_rule → eng_routing_rule` | conditions → condition; target → assign_to; active → status |
| `growth_policy_decision → gov_policy_decision` | action_key → action; allowed → decision; reason → rule_ids (+ reason_codes text[] added) |
| `growth_social_post → intel_social_post` | external_post_id → post_ref; published_at → posted_at |
| `growth_content_asset → mkt_content_asset` | kind → asset_type |
| `growth_content_version → mkt_content_version` | content_asset_id → asset_id; version → version_no; approved_by → approval_id |
| `growth_social_publication → mkt_social_publication` | provider_ref → provider_post_id |
| `growth_keyword → mkt_keyword` | term → phrase |
| `growth_seo_issue → mkt_seo_issue` | page_url → page_id; issue_type → issue_code |
| `growth_page_metric → mkt_page_metric` | page_url → page_id; date → metric_date; metric_key → wide columns impressions/clicks/avg_position/enquiries; value → wide columns |
| `growth_landing_page → mkt_landing_page` | content_version_id → blocks_version_id; state → mkt_publication.state |
| `growth_attribution_event → mkt_attribution_event` | source → utm; campaign_ref → campaign_id |
| `growth_audience → mkt_audience` | selection_rules → criteria; state → status |
| `growth_campaign → mkt_campaign` | audience_id → mkt_campaign_version.audience_id; budget_inr → budget_id |
| `growth_campaign_version → mkt_campaign_version` | content_version_id → content_version_ids; version → version_no |
| `growth_ad_campaign → mkt_ad_campaign` | provider_ref → provider_campaign_id |
| `growth_ad_spend_event → mkt_spend_event` | amount_inr → amount; occurred_at → spend_date |
| `growth_event_registration → mkt_registration` | registered_at → created_at |
| `growth_event_attendance → mkt_attendance` | attended_at → joined_at |
| `growth_partner → lcy_partner` | kind → partner_type; state → due_diligence_state |
| `growth_referral → mkt_referral` | referral_key → referral_code |
| `growth_proposal_version → com_proposal_version` | version → version_no; document_ref → body_storage_key |
| `growth_quote_line → com_quote_line` | discount → discount_pct |
| `growth_objection → com_objection` | category → category_code; summary → raised_text |
| `growth_negotiation → com_negotiation` | approval_id → exception_approval_id |
| `growth_contract → com_contract` | version → revision; document_ref → document_storage_key |
| `growth_signature_event → com_signature_event` | provider_event_key → provider_event_id |
| `growth_invoice → com_invoice` | amount_inr → total_amount |
| `growth_payment → com_payment` | provider_transaction_id → provider_payment_id; amount_inr → amount |
| `growth_deployment → lcy_deployment` | location_id → location_ref; readiness → readiness_checklist |
| `growth_subscription → lcy_customer_subscription` | deal_id → contract_id; starts_at → start_date; ends_at → end_date |
| `growth_renewal → lcy_renewal` | subscription_id → customer_subscription_id; due_at → due_date |
| `growth_account_metric → lcy_account_metric` | metric_key → metric_code; period_start → as_of_date |
| `growth_deal_outcome → lcy_outcome` | deal_id → subject_id; outcome → outcome_code; reason → loss_reason_code; occurred_at → recorded_at |
| `growth_feedback → ai_feedback` | outcome_id → lcy_feedback.subject_id |
| `growth_eval_run → ai_eval_run` | passed → gate_result |
| `growth_competitor → intel_competitor` | domain → website; state → internal_only / archived_at |
| `growth_market_event → intel_market_event` | occurred_at → event_date |
| `growth_stage_metric → ana_stage_metric` | stage_id → stage_code; period_start → period; probability → conversion_rate; sample_count → sample_size |
| `growth_forecast → ana_forecast` | period_start → period; forecast_inr → weighted_value |
| `growth_admin_projection → ana_admin_projection` | projection_key → panel_code; summary → payload; last_event_key → last_event_seq |
| `growth_test_run → ops_test_run` | status → result; report_ref → report_key |
| `growth_integration_deal → lcy_integration_deal` | technical_scope → api_capabilities |
| `growth_launch_approval → cat_launch_approval` | product_id → offering_id; readiness_snapshot → checklist_results |
| `sales_tenant → ten_tenant` | kind → ownership_type; state → lifecycle_state; region → home_region |
| `sales_startup → ten_startup` | brand → display_name; currency → base_currency; state → lifecycle_state |
| `sales_membership → ten_membership` | existing_user_id → user_id; role → role_id; permissions → approval_limits; state → status |
| `sales_brand_domain → ten_domain` | verification_hash → verification_token_hash; state → verification_state |
| `sales_service_plan → saas_plan` | plan_key → code; feature_limits → saas_entitlement rows via saas_plan_entitlement; rate_card → base_fee |
| `sales_service_subscription → saas_subscription` | plan_id → plan_version_id; plan_revision → plan_version_id; trial_end → trial_ends_at; period_end → current_period_end; entitlements → saas_entitlement via plan_version |
| `sales_service_invoice → saas_service_invoice` | period_key → period_start |
| `sales_support_grant → saas_support_access_grant` | granted_to → requested_by; actions → access_mode + module_scope; approval_id → approved_by |
| `sales_usage_charge → saas_service_invoice_line` | usage_id → readings_digest / saas_usage_meter_reading.invoice_line_id; invoice_id → service_invoice_id; charge_key → meter_code; units → quantity; state → frozen with parent invoice state |
| `sales_data_transfer → saas_export_job` | direction → request_type; dataset → entity_selection; object_ref → file_storage_key; expires_at → link_expires_at |
| `sales_action_plan → aut_autonomy_plan` | objective → objective_code; autonomy → mode; estimated_cost → simulation_cost |
| `sales_bid → com_bid` | deadline → deadline_utc; source → portal_code; eligibility → eligibility_result; requirements → com_bid_checklist_item rows |
| `sales_order → com_order` | total → total_amount |
| `sales_order_line → com_order_line` | product_id → offering_version_id; unit → unit_code; price → unit_price; total → line_total |
| `sales_fulfillment → com_fulfillment_event` | line_id → order_line_id; milestone_key → event_type |
| `growth_website_publication → mkt_publication` | slug → path; page_type → target_kind; blocks → mkt_publication_snapshot.storage_key (blocks JSON); content_hash → mkt_publication_snapshot.snapshot_hash; approval_ref → approval_id; published → current_snapshot_id; actor_ref → created_by |
| `sales_external_access_grant → ten_portal_grant` | external_identity_ref → subject_user_id; resource_type → object_type; resource_id → object_id; allowed_actions → actions; approved_by → granted_by |
| `sales_ui_application → saas_application_draft` | legal_name → organization_legal_name; business_email → applicant_email_enc / applicant_email_hmac; status → state; verified_principal_ref → applicant_user_id |
| `sales_ui_config_revision → aut_config_revision` | base_revision → supersedes_id; configuration → candidate / active_snapshot; configuration_hash → content_hash; approved_by_ref → approval_id |
| `sales_ui_trigger_revision → aut_trigger` | kind → trigger_kind; definition → condition + schedule_cron + event_type; status → state; next_due_at → next_fire_at |
| `sales_ui_conflict → aut_conflict_case` | action_key → duplicate_key; run_refs → run_id; status → state; decision → resolution |
| `sales_ui_template_revision → aut_workflow_template` | template_key → template_code; capability → business_capability; graph → node_types; approved_by_ref → approval_id |

### 3.6.4.6 Enumerated value reconciliation

| Source table.column | Source values | Part 3.3 column and values | Decision |
|---|---|---|---|
| `sales_tenant.kind` | owned, client | `ten_tenant.ownership_type` owner_portfolio, external_client | Covered: owned → owner_portfolio, client → external_client (DEC-065). Seed and import mapping table in MG-08 |
| `sales_tenant.state` | trial, active, suspended, offboarding, closed | `ten_tenant.lifecycle_state` adds applicant, under_verification, rejected, approved, provisioning (§2.27.16) | Covered: blueprint is a superset; pre-tenant states live in `saas_application_draft` in the source, which is consistent |
| `sales_order.direction` | buy, sell, service, training, project | `com_order.direction` sell, buy | **Conflict** (CONFLICT-386): keep direction = ledger side (sell → receivable, buy → payable) and add `order_kind` (goods, service, training, project) |
| `growth_product.readiness` | enum (values not stated) | `cat_offering.readiness_state` planned, draft, … (§3.3.6.3) | Covered |
| `sales_external_access_grant.resource_type` | enum (values not stated) | `ten_portal_grant.object_type` proposal, quote, contract, invoice, order, onboarding, renewal, ticket | Covered; `ticket` binds to the new `saas_service_request` (ENT-ENH-E-02) |
| `growth_website_publication.page_type` | enum (values not stated) | `mkt_publication.target_kind` | Covered |
| `growth_message.direction` | text | `eng_message.direction` outbound, inbound | Covered |
| `growth_payment` (receipt) | verified webhook/reconciliation | `com_payment.direction` inbound, outbound_record (DEC-064) | Covered |
| `sales_ui_service_request.kind` | "request kind allowlist" | — | New: CHECK IN (billing_question, access_request, data_export, configuration_change, incident, other) on ENT-ENH-E-02 |
| `sales_service_subscription.state` | not stated | `saas_subscription.state` (§2.27.18) | Covered |

### 3.6.4.7 Constraint and index reconciliation

**Totals (276 atoms).** Covered by a Part 3.3 key, CHECK, immutability profile or §3.3.8 index: **222** (of which 124 are service/PDP rules such as "check before every send", "approved before send", "fail closed", mapped to BRL/CK IDs, and 39 are source global unique keys that Part 3.3 already defines **scoped by tenant/startup**, CONFLICT-384) · **Added: 54** (IX-ENH-E-01…54).

| New ID | Source table | Source constraint | Proposed key / index (Part 3.6b §3.6.5.1 DDL) |
|---|---|---|---|
| IX-ENH-E-01 | `growth_capability` | unique(product_id,code) | uq_cat_capability__code (tenant_id, startup_id, code) WHERE archived_at IS NULL; offering link already UQ in cat_offering_capability |
| IX-ENH-E-02 | `growth_quota` | unique(integration_id,period) | uq_int_quota__period (tenant_id, startup_id, integration_id, unit, period) |
| IX-ENH-E-03 | `growth_job_run` | unique(job_key) | uq_ops_job_run__job_key (COALESCE(tenant_id, zero-uuid), job_key) on new column job_key |
| IX-ENH-E-04 | `growth_job_run` | index(status,next_retry) | ixp_ops_job_run__retry (next_retry_at) WHERE state IN ('failed','retry_scheduled') |
| IX-ENH-E-05 | `growth_eval_case` | unique(case_key) | uq_ai_eval_case__code (COALESCE(tenant_id, zero-uuid), suite_code, case_code, version_no) |
| IX-ENH-E-06 | `growth_budget` | unique(scope,period_start) | uq_ai_budget__scope_period (COALESCE(tenant_id, zero-uuid), scope_level, scope_ref, period) WHERE status = 'active' |
| IX-ENH-E-07 | `growth_cost_ledger` | unique(entry_key) | uq_ai_cost_ledger__entry_key (tenant_id, entry_key) on new column entry_key (complements UQ-IDEM-15) |
| IX-ENH-E-08 | `growth_privacy_request` | index(state,due_at) | ixp_gov_privacy_request__due (tenant_id, due_at) WHERE state NOT IN ('completed','rejected','withdrawn') |
| IX-ENH-E-09 | `growth_release` | unique(version,environment) | uq_ops_release__tag_env (version_tag, environment) on new column environment |
| IX-ENH-E-10 | `growth_incident` | index(state,severity) | ixp_ops_incident__open (severity, opened_at DESC) WHERE state <> 'closed' |
| IX-ENH-E-11 | `growth_query_run` | unique(job_run_id) | uq_intel_query_run__correlation (tenant_id, startup_id, correlation_id) WHERE correlation_id IS NOT NULL |
| IX-ENH-E-12 | `growth_source_record` | unique(source_id,canonical_url,content_hash) | uq_intel_source_record__version (tenant_id, startup_id, source_id, url_hash, content_hash) on new column content_hash |
| IX-ENH-E-13 | `growth_fetch_log` | index(source_id,fetched_at) | ix_intel_fetch_log__source_time (tenant_id, startup_id, source_id, created_at DESC) on new column source_id |
| IX-ENH-E-14 | `growth_org_location` | index(organization_id,country,region) | ix_intel_location__org_geo (tenant_id, startup_id, organization_id, country_code, subdivision_code) |
| IX-ENH-E-15 | `growth_signal` | unique(organization_id,evidence_id,signal_type_id) | uq_intel_signal__dedupe (tenant_id, startup_id, dedupe_key) WHERE state <> 'rejected'; dedupe_key = sha256(organization_id/signal_type_id/sorted evidence ids) |
| IX-ENH-E-16 | `growth_solution_match` | unique(need_id,capability_id) | uq_intel_match__need_target (tenant_id, startup_id, need_id, offering_version_id, COALESCE(capability_id, zero-uuid)) |
| IX-ENH-E-17 | `growth_score_version` | unique(opportunity_id,version) | uq_intel_score_version__seq (opportunity_id, version_no) on new column version_no integer NOT NULL |
| IX-ENH-E-18 | `growth_role_hypothesis` | unique(opportunity_id,role_title) | uq_intel_role_hypothesis__opp_role (tenant_id, startup_id, opportunity_id, role_code) WHERE opportunity_id IS NOT NULL |
| IX-ENH-E-19 | `growth_contact_verification` | index(contact_id,channel,expires_at) | ix_intel_contact_verification__expiry (tenant_id, startup_id, contact_id, channel, expires_at DESC) |
| IX-ENH-E-20 | `growth_form` | unique(slug,version) | uq_crm_form__code (tenant_id, startup_id, form_code) WHERE archived_at IS NULL; version uniqueness by STD-V on crm_form_version |
| IX-ENH-E-21 | `growth_lead` | index(state,owner_id) | ixp_crm_lead__queue (tenant_id, startup_id, state, owner_id) WHERE archived_at IS NULL |
| IX-ENH-E-22 | `growth_workflow` | unique(workflow_key,version) | uq_aut_workflow__code (tenant_id, startup_id, workflow_code); version uniqueness by STD-V on aut_workflow_revision |
| IX-ENH-E-23 | `growth_message_template` | unique(template_key,version,channel) | uq_eng_message_template__code (tenant_id, startup_id, template_code, channel, locale, version_no) |
| IX-ENH-E-24 | `growth_thread` | unique(channel,external_thread_ref) | uq_eng_thread__external (channel_account_id, external_thread_ref) WHERE external_thread_ref IS NOT NULL |
| IX-ENH-E-25 | `growth_intent` | unique(inbound_event_id) | uq_eng_intent__inbound (inbound_event_id) WHERE superseded_by IS NULL (one current intent per inbound event) |
| IX-ENH-E-26 | `growth_calendar_link` | unique(integration_id,external_calendar_id) | uq_eng_calendar_link__external (integration_id, external_calendar_id) on new column external_calendar_id |
| IX-ENH-E-27 | `growth_approval` | index(object_type,object_id) | ix_gov_approval__object (tenant_id, startup_id, object_type, object_id, created_at DESC) |
| IX-ENH-E-28 | `growth_identity_link` | unique(channel_account_id,external_subject_hash) | uq_eng_identity_link__address (tenant_id, startup_id, channel_account_id, address_hmac) |
| IX-ENH-E-29 | `growth_routing_rule` | unique(channel,priority) | uq_eng_routing_rule__priority (tenant_id, startup_id, COALESCE(channel,'*'), priority) WHERE status = 'active' |
| IX-ENH-E-30 | `growth_policy_decision` | index(action_key) | ix_gov_policy_decision__action (tenant_id, startup_id, action, created_at DESC) |
| IX-ENH-E-31 | `growth_compliance_incident` | index(state,severity) | ixp_gov_compliance_incident__open (tenant_id, severity, opened_at DESC) WHERE state <> 'closed' |
| IX-ENH-E-32 | `growth_social_post` | unique(source_record_id,external_post_id) | uq_intel_social_post__ref (tenant_id, startup_id, platform, post_ref) |
| IX-ENH-E-33 | `growth_content_asset` | index(product_id,state) | ix_mkt_content_asset__offering_state (tenant_id, startup_id, offering_id, state) |
| IX-ENH-E-34 | `growth_seo_issue` | index(state,page_url) | ixp_mkt_seo_issue__open (tenant_id, startup_id, page_id, severity) WHERE state <> 'resolved' |
| IX-ENH-E-35 | `growth_page_metric` | unique(page_url,date,metric_key) | uq_mkt_page_metric__day (tenant_id, startup_id, page_id, COALESCE(keyword_id, zero-uuid), metric_date, source) |
| IX-ENH-E-36 | `growth_attribution_event` | unique(event_key) | uq_mkt_attribution_event__key (tenant_id, startup_id, event_key) on new column event_key |
| IX-ENH-E-37 | `growth_campaign` | index(state) | ix_mkt_campaign__state (tenant_id, startup_id, state, starts_at) |
| IX-ENH-E-38 | `growth_ad_spend_event` | unique(event_key) | uq_mkt_spend_event__key (ad_campaign_id, event_key) for manual/CSV spend rows (UQ-IDEM-19 covers provider reports) |
| IX-ENH-E-39 | `growth_business_event` | index(starts_at,state) | ix_mkt_event__starts (tenant_id, startup_id, starts_at, state) |
| IX-ENH-E-40 | `growth_event_registration` | unique(event_id,lead_id) | uq_mkt_registration__event_contact (event_id, contact_id) |
| IX-ENH-E-41 | `growth_event_attendance` | unique(registration_id,provider_ref) | uq_mkt_attendance__provider (registration_id, provider_ref) WHERE provider_ref IS NOT NULL |
| IX-ENH-E-42 | `growth_proposal` | index(deal_id,state) | ix_com_proposal__deal_state (tenant_id, startup_id, deal_id, state) |
| IX-ENH-E-43 | `growth_quote` | index(deal_id,state) | ix_com_quote__deal_state (tenant_id, startup_id, deal_id, state) |
| IX-ENH-E-44 | `growth_objection` | index(deal_id,state) | ix_com_objection__deal_state (tenant_id, startup_id, deal_id, state) |
| IX-ENH-E-45 | `growth_onboarding` | unique(deal_id) | uq_lcy_onboarding__deal (tenant_id, startup_id, deal_id) WHERE archived_at IS NULL |
| IX-ENH-E-46 | `growth_handoff` | unique(onboarding_id,task_id) | uq_lcy_handoff__task (onboarding_id, task_id) WHERE task_id IS NOT NULL on new column task_id |
| IX-ENH-E-47 | `growth_eval_run` | index(prompt_version_id,passed) | ix_ai_eval_run__prompt_gate (prompt_version_id, gate_result, created_at DESC) |
| IX-ENH-E-48 | `growth_competitor` | unique(domain) | uq_intel_competitor__website (tenant_id, startup_id, lower(website)) WHERE website IS NOT NULL |
| IX-ENH-E-49 | `growth_market_event` | unique(competitor_id,evidence_id,event_type) | uq_intel_market_event__dedupe (tenant_id, startup_id, competitor_id, evidence_id, event_type) |
| IX-ENH-E-50 | `growth_stage_metric` | unique(stage_id,period_start) | uq_ana_stage_metric__period (tenant_id, startup_id, pipeline_id, stage_code, period) |
| IX-ENH-E-51 | `growth_forecast` | unique(period_start,model_version) | uq_ana_forecast__period (tenant_id, startup_id, period, scenario, model_version) on new column model_version |
| IX-ENH-E-52 | `growth_test_run` | index(release_id,status) | ix_ops_test_run__release (release_id, result, executed_at DESC) |
| IX-ENH-E-53 | `growth_integration_deal` | unique(deal_id) | uq_lcy_integration_deal__deal (tenant_id, startup_id, deal_id) WHERE deal_id IS NOT NULL |
| IX-ENH-E-54 | `sales_business_template` | Approved immutable revision | Imm. V on new ten_business_template (STD-V) |

**Global versus scoped keys [CONFLICT-384].** Document 08 writes most business keys as global (`unique(code)`, `unique(invoice_no)`, `unique(base_url)`). In a multi-tenant cluster (DEC-009) a global key would let one tenant's data block another's and would leak existence through 409 responses. Every key above is therefore scoped by `(tenant_id, startup_id)` or by the provider connection, as FRD §5 requires ("provider IDs unique within connection"). Exceptions that stay global by design: `ten_domain.hostname` (verified), `saas_service_invoice.invoice_no` (platform issuer), `ops_release.version_tag` + environment.

### 3.6.4.8 Physical schema resolution and the schema decision register (SDR)

Document 08 lists 136 field/reuse records that "require resolution" before any model migration (132 proposed type definitions, 4 blocked). Each row is assigned an SDR number in `E_coverage.csv` (`08-SDR-001…136`).

| Outcome | Rows | Meaning |
|---|---|---|
| Type confirmed against Part 3.3 | 111 | Part 3.3 column exists with a compatible or stricter type; Part 3.3 type governs (DEC-107) |
| Column added | 20 | Added in §3.6.5.1 with type, nullability, default and constraint |
| Conflict | 5 | Fulfilment milestone fields (CONFLICT-383) and embedding vector (CONFLICT-381) |
| **Total** | **136** | 16 `sales_*` tables, 2 late additions, 4 blocked rows |

**The four blocked rows** (document 08 "DEC-039…DEC-042", renamed SDEC-08-039…042 because blueprint DEC-039 means seed migration, CONFLICT-380):

| SDEC | Source record | Source proposed resolution | Blueprint decision that resolves it | Remaining action |
|---|---|---|---|---|
| SDEC-08-039 | existing user table / all | Resolve identity table and PK type from Django model metadata; no duplicate identity tables | DEC-003, DEC-019 (reuse AppNAI identity as library/IdP, new audience); Part 3.3 ENT-006 `ten_user` product-local mirror | CONFLICT-382: `ten_user` becomes a 1:1 profile keyed to the reused identity, not a second credential store; W0-A spike confirms PK type |
| SDEC-08-040 | existing role table / all | As above | ENT-007 `ten_role` system roles R01–R20 | Map Django groups → `ten_role.code` in MG-08; no group-based authorization at runtime (RBAC matrix governs) |
| SDEC-08-041 | existing membership table / all | As above | ENT-008 `ten_membership` + `ten_membership_grant` | Existing user-role rows imported once as grants; `sales_membership` semantics (nullable startup = portfolio scope) already match |
| SDEC-08-042 | growth_embedding / vector(d) | Select approved model, assert dimension before index | **DEC-088**: multilingual E5-large class, 1024 dimensions, `halfvec(1024)` HNSW (RECOMMENDATION-039) | CONFLICT-381 closed by DEC-088; migration asserts `vector_dims(embedding) = 1024` per `model_id` |

**Outstanding approval gates carried from document 08 (GAP-392).** 38 exact API definitions outstanding (handed to the API reconciliation group, see `D_api_mapping.csv`); 0 partial API proposals; 4 database reuse/field confirmations (the four SDEC rows above); 138 UI semantic-mapping approvals (UX group). The SDR process that keeps these as decision-queue items is specified in Part 3.6b §3.6.5.3.

### 3.6.4.9 Exposure and protection reconciliation (documents 08 and 28 versus Part 3.3)

| Source exposure class | Tables | Meaning (document 08 wording) | Part 3.3 mechanism | Status |
|---|---|---|---|---|
| EXP-ADM | 103 (+6 candidates) | Admin/internal service only; no website projection or public serialization | Admin API audience only; RLS; no `Pub` columns | Covered; register in 3.6b §3.6.5.3 makes it enforceable in CI |
| EXP-WEB | 44 | Authorized website/portal service may access bounded fields for mapped operations | Portal predicate §3.3.9.4; column Class | Partially covered: no per-table allowlist of portal-readable fields → serializer allowlist register (GAP-391) |
| EXP-PUB | 1 | Public API returns only validated published DTO | `mkt_publication_snapshot` + CDN (BRL-PUB) | Covered |
| EXP-PRT | 1 | Portal receives own authorized object DTO; never serialize invitation hashes | `ten_portal_grant`; ABAC-09 | Covered (+ invite hash columns added) |

Document 28's 149-row inventory repeats the same classes: **149 of 149 rows agree** with document 08 (two rows differ only in wording: "Published DTO only; drafts private" and "Confidential; own object-granted portal DTO only").

| Source protection class | Tables | Part 3.3 classification (RECOMMENDATION-004) | Finding |
|---|---|---|---|
| INT (internal business data; role-scoped; retention) | 113 | Int default, Conf for commercial terms | Covered |
| SCOPE (scope by tenant/startup; entitlement and retention) | 16 (+6 candidates) | STD-S/T scope columns + RLS | Covered |
| PII-R (restricted business PII; RBAC, encryption, retention; no clinical data) | 11 | Rest for `_enc`/`_hmac` columns; Conf for names | Covered for contact, submission, lead, message, inbound, consent, privacy request; **Partially** for `eng_message_draft`, `eng_chat_session`, `intel_contact_source` (no Rest columns: draft body and session token hash added as Rest in 3.6b) |
| AUDFIN-R (restricted audit/finance; immutable evidence) | 6 | Imm. A/F + FIN/CTR/AUD retention | Covered |
| SECRET (secret reference only; restricted admin access) | 1 | `int_credential_ref` columns are Int | **Partially covered**: table-level restriction to R01/R13 and audit-on-read added (RECOMMENDATION-399) |

**Source ownership classes (Physical schema acceptance, row "Ownership").** Reference → scope X/P; tenant → scope T; issuer/startup → scope S; private grant → `ten_portal_grant`/`saas_support_access_grant`. All four are covered by Part 3.3 §3.3.3.1.

---

## 3.6.4.10 Quality gate: Batch 3.6a

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | **Pass** | Every row cites the doc 08/28 section or table and the Part 3.3/4.x location |
| 2 | Assumptions, gaps, conflicts tagged and logged | **Pass** | Tags 380–399 only; register in Part 3.6b §3.6.8 |
| 3 | IDs unique and consistent | **Pass** | New families IX-ENH-E, SDR, SDEC-08, ENT-ENH-E are local; source "DEC-039…042" renamed (CONFLICT-380); pack KPIs referred to as OKPI |
| 4 | No story lacks AC; no requirement lacks a test | **Pass (see 3.6b)** | Tests and stories are in Part 3.6b §3.6.5.6–§3.6.5.7 |
| 5 | Negative, edge, security, accessibility | **Pass (accessibility N/A)** | Cross-scope keys, exposure, secret handling covered; no UI here |
| 6 | Agents have guardrail, fallback, KPI, cost | **N/A** | No agents |
| 7 | Time-sensitive facts flagged | **Pass** | Doc 08 provider prices not restated; see ASSUMPTION-397 |
| 8 | No restricted data to free-tier models | **Pass** | No routing change |
| 9 | Consistent with earlier parts | **Pass, with inconsistencies reported in 3.6b §3.6.6** | Part 3.3 governs names (DEC-107) |

**Status: Part 3 Batch 3.6a complete. 155 source tables, 799 columns, 276 constraint atoms and 136 schema-resolution rows reconciled programmatically; continue with Batch 3.6b.**
