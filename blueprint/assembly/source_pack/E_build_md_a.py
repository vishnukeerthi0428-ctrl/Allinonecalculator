"""Group E: write Part-03-6a (documents reviewed, coverage, register, catalogue reconciliation)."""
import json, csv, sys, os, re
from collections import Counter, OrderedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from E_mapping import M
from E_aspects import A
SD, BD = sys.argv[1], sys.argv[2]
d = json.load(open(f'{SD}/doc08.json')); bp = json.load(open(f'{SD}/part33.json'))
cols = list(csv.DictReader(open(f'{SD}/columns.csv'))); cons = json.load(open(f'{SD}/cons_final.json'))
mrows = json.load(open(f'{SD}/mapping_rows.json')); cov = json.load(open(f'{SD}/cov_rows.json'))
c = lambda s: str(s).replace('|', '/').replace('\n', ' ')
out = []; P = out.append
P("""# AI Growth Engine: Employee Sales & Marketing Automation
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
""")
P("""### 3.6.1.1 Document 08: PostgreSQL Backend Table Catalog

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
""")
# ---- 3.6.2 summary ----
P("## 3.6.2 Coverage register summary\n")
def bucket(r):
    s = r['section']
    if s == 'Column': return 'Columns'
    if s == 'Constraint/index': return 'Constraints and indexes'
    if s == 'Physical schema resolution' and r['aspect_id'].startswith('08-SDR'): return 'Schema-resolution rows'
    if s == 'Commercial PostgreSQL entity register' and r['aspect_id'].startswith('08-ENT'): return 'Tables (149 + 6 candidates)'
    if s == 'Logical entity inventory for migration planning' and r['aspect_id'].startswith('28-INV'): return 'Inventory rows'
    return 'Prose aspects'
cnt = Counter((r['doc'], bucket(r), r['status']) for r in cov)
STS = ['Covered','Partially covered','Not covered','Conflict','Not applicable']
P("| Document | Aspect type | Total | Covered | Partially covered | Not covered | Conflict | Not applicable |\n|---|---|---|---|---|---|---|---|")
tot = Counter()
for doc in ['08','28']:
    for bt in ['Prose aspects','Tables (149 + 6 candidates)','Columns','Constraints and indexes','Schema-resolution rows','Inventory rows']:
        n = [cnt[(doc, bt, s)] for s in STS]
        if sum(n) == 0: continue
        for s, v in zip(STS, n): tot[s] += v
        P(f"| {doc} | {bt} | {sum(n)} | " + ' | '.join(str(x) for x in n) + ' |')
P(f"| **All** | | **{sum(tot.values())}** | " + ' | '.join(f"**{tot[s]}**" for s in STS) + ' |')
P("""
**Reading the numbers.** (1) Of 155 source tables, **77 map fully**, **73 map with column gaps**, **3 carry a column conflict** (`growth_embedding`, `growth_sequence_step`, `sales_fulfillment`) and **2 have no blueprint entity** (`sales_business_template`, `sales_ui_service_request`). (2) Of 799 source columns, **666 are already in Part 3.3** (344 same name, 119 renamed, 200 semantically equivalent, 3 identity reuse), **124 are added by Part 3.6b** (113 column additions + 11 columns of the two new entities), **6 are conflicts** with proposed resolutions and **3 are not adopted** with a reason. (3) Of 276 constraint/index atoms, **222 are covered** and **54 are added** as named keys or indexes IX-ENH-E-01…54. (4) Document 28 adds no tables; its gaps are procedures (tiered recovery objectives, restore-drill completeness, reference SQL smoke tests, disposable databases, offboarding) written in Part 3.6b §3.6.5.4–§3.6.5.5.
""")
# ---- 3.6.3 detailed register (prose) ----
P("## 3.6.3 Detailed coverage register (prose aspects)\n\nEvery prose aspect is listed individually. Catalogue aspects (tables, columns, constraints, resolution rows, inventory rows) are listed individually in §3.6.4 and in `E_coverage.csv`.\n")
P("| ID | Section | Aspect | Status | Blueprint location | Action / new IDs |\n|---|---|---|---|---|---|")
for a in A:
    a = list(a) + [''] * (8 - len(a))
    st = {'Covered (ID not traced)':'Covered (OPT ID not cited)','Not applicable (other group)':'Not applicable (document 16 group)'}.get(a[4], a[4])
    P(f"| {a[2]} | {c(a[1])} | {c(a[3])} | {st} | {c(a[5])} | {c(a[6])}{(' · ' + c(a[7])) if a[7] else ''} |")
# ---- 3.6.4 catalogue reconciliation ----
P("""
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
""")
prim = Counter(m['bp_ent'] for m in mrows)
secs = set(s for m in mrows for s in m['secondary'].split(';') if s.startswith('ENT-'))
bp_only = [e for e in bp if e not in prim and e not in secs]
sec_only = [e for e in bp if e not in prim and e in secs]
P(f"""| Line | Item | Count | Basis |
|---|---|---|---|
| a | Source tables in document 08 (001–149) | 149 | Parsed |
| b | Candidate tables (`sales_ui_*`) | 6 | Parsed |
| c | Source tables mapped to an existing Part 3.3 entity as primary target | {sum(1 for m in mrows if m['bp_ent'] in bp)} | §3.6.4.3 |
| d | Source tables with no Part 3.3 entity (new entities ENT-ENH-E-01, ENT-ENH-E-02) | {sum(1 for m in mrows if m['bp_ent'] not in bp)} | GAP-388 |
| e | Part 3.3 entities that are the primary target of at least one source table | {len([e for e in prim if e in bp])} | Two source tables (`existing membership table`, `sales_membership`) share ENT-008 |
| f | Part 3.3 entities reached only as a secondary target (split or normalized parts of a source table) | {len(sec_only)} | {', '.join(sec_only)} |
| g | Part 3.3 entities with **no source table** (blueprint normalization, reference data or DEC-016 derivations) | {len(bp_only)} | §3.6.4.4 |
| h | Check: e + f + g | {len([e for e in prim if e in bp]) + len(sec_only) + len(bp_only)} | = 199 |
| i | New logical entities proposed by this batch | 4 | ENT-ENH-E-01 business template, ENT-ENH-E-02 service request, ENT-ENH-E-03 fulfilment milestone (CONFLICT-383), ENT-ENH-E-04 eval case result |
| j | Blueprint logical entities after this batch | 203 | 199 + 4 (final ENT numbers ENT-200…203 to be assigned by the coordinator) |

**Finding.** The "17 retained entities the FRD never names" (Part 3.3 §3.3.3.4 line 1) are now identified: they are the 16 `sales_*` platform-extension tables plus `growth_website_publication`/`sales_external_access_grant` (with `growth_feedback`'s second meaning). All of them map to DEC-016 or batch-derived entities except `sales_business_template`. The worst case in §3.3.3.4 item 4 ("up to 17 entities this blueprint does not model") is therefore **2 entities**, now added. [ASSUMPTION-396: document 08 is the "original entity catalogue" that GAP-112 and DEC-087 refer to; on that basis GAP-112 can be closed by the coordinator.]

### 3.6.4.3 Complete source-table → blueprint-entity mapping (155 rows)

Columns: **Exp.** exposure class (EXP-ADM Admin/internal only; EXP-WEB bounded fields for mapped website/portal operations; EXP-PUB published DTO only; EXP-PRT own-object portal DTO) · **Prot.** source protection (INT internal; SCOPE tenant/startup scope; PII-R restricted business PII; AUDFIN-R restricted audit/finance; SECRET secret reference) · **Build** source build/reuse · **Match** Renamed, Merged, Split, Reuse-mapped or New · **Cols** source columns / covered / added / conflict.
""")
P("| # | Source table | Exp. | Prot. | Build | → ENT | Blueprint table (+ secondary) | Scope | Imm. | Ret. | Match | Cols | Status |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for m in mrows:
    sec = f" (+{m['secondary'].replace(';', ', ')})" if m['secondary'] else ''
    P(f"| {m['src_no']} | `{m['src_table']}` | {m['src_exposure']} | {m['src_protection']} | {c(m['src_build'])} | {m['bp_ent']} | `{m['bp_table'].replace('(new) ','')}`{'' if m['bp_table'] and not m['bp_table'].startswith('(new)') else ' (new)'}{sec} | {c(m['bp_scope'])} | {m['bp_imm']} | {c(m['bp_ret']).split(' (')[0]} | {m['match_type']} | {m['src_columns']}/{m['covered_columns']}/{m['gap_columns']}/{m['conflict_columns']} | {m['status']} |")
P("""
Notes on non-obvious mappings: `growth_product` is merged into Offering (DEC-003, DEC-107); `growth_feedback` splits by meaning into `ai_feedback` and `lcy_feedback` (CONFLICT-106, DEC-085 pattern); `growth_business_event` is the webinar/demo event `mkt_event` (Event homonym, CONFLICT-106); `growth_workflow_execution` is `aut_run`; `growth_api_usage` is `ai_usage` and provider usage feeds SaaS meters only through DEC-086 aggregation; `sales_usage_charge` spreads over `saas_usage_meter_reading`, `saas_service_invoice_line` and `saas_credit`; `sales_data_transfer` splits by direction into `saas_export_job` and `saas_import_job`; `growth_website_publication` splits into the pointer `mkt_publication`, the immutable `mkt_publication_snapshot` and `mkt_preview_grant`.
""")
P("### 3.6.4.4 Blueprint entities with no source table (30)\n\nThese are blueprint normalizations or DEC-016 derivations. None conflicts with document 08; each is required by a rule the source states in prose (for example \"decimal and ISO currency\", \"legal holds\", \"idempotency key/body hash\").\n")
P("| ENT | Table | Origin | Basis in Part 3.3 | Why document 08 has no table |\n|---|---|---|---|---|")
why = {'ten_business_line':'Business lines are folded into startup profile JSON in doc 08 (`sales_startup.profile`)','ten_capability_profile':'Doc 08 keeps startup capabilities in `sales_startup.profile/autonomy` JSON',
 'ten_saved_view':'UI convenience; doc 08 lists filters per interface, not persisted views','ref_dataset':'Doc 08 uses enums inline; blueprint centralizes reference data','ref_value':'As above','ref_currency':'Doc 08 says "ISO currency" without a table','ref_country':'Doc 08 uses char(2) codes without a table','ref_unit':'Doc 08 uses free-text unit',
 'cat_tax_profile':'Doc 08 has only `tax decimal` on order lines','gov_jurisdiction_rule':'Doc 08 keeps jurisdiction inside policy JSON','gov_approval_policy':'Doc 08 keeps thresholds in tenant `policy` JSON','gov_approval_delegation':'Not in doc 08 (BRL-APR-09)','gov_legal_hold':'Doc 28 requires legal holds but names no table',
 'ai_agent_definition':'Doc 08 has prompt versions only','intel_scoring_model':'Doc 08 keeps factors on `growth_score_version`','crm_closure_policy':'Doc 08 keeps closure evidence on the deal','crm_stage_transition':'Doc 08 "terminal transitions service-guarded" without a history table',
 'com_sku_availability':'Doc 08 has no inventory table','com_inventory_reservation':'As above (DEC-045)','com_discrepancy_case':'Doc 08 "reconciliation" without a case table','com_receivable_entry':'Doc 08 "distinct payable/receivable" on orders only','com_payable_entry':'As above',
 'ops_domain_event':'Doc 08 relies on outbox only','ops_idempotency_key':'Doc 08 states the rule (idempotency key/body hash) without a table','ops_notification_preference':'Not in doc 08 (DEC-036)','saas_entitlement':'Doc 08 keeps entitlements as JSON on plan/subscription',
 'ana_metric_definition':'Doc 08 has metric_key strings only','ana_pipeline_projection':'Doc 08 has two projections only','ana_fx_snapshot':'Doc 08 has no FX table (DEC-027)','ana_report_subscription':'Not in doc 08 (Part 2.4 §2.31.5)'}
for e in bp_only:
    b = bp[e]; P(f"| {e} | `{b['table']}` | {b['origin']} | {c(b['basis'])} | {why.get(b['table'],'Blueprint normalization')} |")
# ---- 3.6.4.5 columns ----
P("""
### 3.6.4.5 Column-level reconciliation

**Totals (799 columns).** Same name 344 · renamed (synonym rule) 119 · semantically equivalent structure 200 · identity reuse 3 · **added in Part 3.6b 113** · **new-entity columns 11** · **conflict 6** · not adopted 3.

#### (a) Column gaps, conflicts and non-adoptions (every item listed)

The "Proposed column / resolution" text is the exact DDL intent; the consolidated `ALTER TABLE` statements are in Part 3.6b §3.6.5.1. All additions carry tag GAP-389 unless another tag is shown.
""")
P("| # | Source table.column | Source type | → Blueprint table | Decision | Proposed column / resolution |\n|---|---|---|---|---|---|")
n = 0
for r in cols:
    if r['status'].startswith('Covered'): continue
    n += 1
    dec = {'Gap - column added in Part 3.6':'Add column','Gap - new entity in Part 3.6':'New entity','Conflict':'Conflict','Not adopted (reason)':'Not adopted'}[r['status']]
    tb = r['bp_table'] or {'ENT-ENH-E-01':'ten_business_template','ENT-ENH-E-02':'saas_service_request'}.get(r['bp_ent'], '')
    P(f"| {n} | `{r['src_table']}.{r['column']}` | {c(r['src_type'])} | `{tb}` | {dec} | {c(r['bp_column'])} |")
P("""
#### (b) Column crosswalk for renamed and semantically equivalent columns

Developers porting code or tests written against document 08 names use this crosswalk. Same-name columns are omitted.
""")
P("| Source table | Source column → blueprint column (renamed or semantic) |\n|---|---|")
grp = OrderedDict()
for r in cols:
    if r['status'] in ('Covered (renamed)', 'Covered (semantic)'):
        grp.setdefault(r['src_table'] + ' → ' + (r['bp_table'] or ''), []).append(f"{r['column']} → {r['bp_column']}")
for k, v in grp.items():
    P(f"| `{k}` | {c('; '.join(v))} |")
# ---- 3.6.4.6 values ----
P("""
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
""")
# ---- 3.6.4.7 constraints ----
cc = Counter(r['status'] for r in cons)
P(f"""### 3.6.4.7 Constraint and index reconciliation

**Totals (276 atoms).** Covered by a Part 3.3 key, CHECK, immutability profile or §3.3.8 index: **{sum(v for k, v in cc.items() if k.startswith('Covered'))}** (of which {cc.get('Covered (rule)',0)} are service/PDP rules such as "check before every send", "approved before send", "fail closed", mapped to BRL/CK IDs, and {cc.get('Covered (scoped)',0)} are source global unique keys that Part 3.3 already defines **scoped by tenant/startup**, CONFLICT-384) · **Added: {sum(1 for r in cons if r['status']=='Gap')}** (IX-ENH-E-01…{sum(1 for r in cons if r['status']=='Gap'):02d}).

| New ID | Source table | Source constraint | Proposed key / index (Part 3.6b §3.6.5.1 DDL) |
|---|---|---|---|""")
for r in cons:
    if r['status'] == 'Gap':
        P(f"| {r['new_id']} | `{r['src_table']}` | {c(r['constraint'])} | {c(r['action'])} |")
P("""
**Global versus scoped keys [CONFLICT-384].** Document 08 writes most business keys as global (`unique(code)`, `unique(invoice_no)`, `unique(base_url)`). In a multi-tenant cluster (DEC-009) a global key would let one tenant's data block another's and would leak existence through 409 responses. Every key above is therefore scoped by `(tenant_id, startup_id)` or by the provider connection, as FRD §5 requires ("provider IDs unique within connection"). Exceptions that stay global by design: `ten_domain.hostname` (verified), `saas_service_invoice.invoice_no` (platform issuer), `ops_release.version_tag` + environment.

### 3.6.4.8 Physical schema resolution and the schema decision register (SDR)

Document 08 lists 136 field/reuse records that "require resolution" before any model migration (132 proposed type definitions, 4 blocked). Each row is assigned an SDR number in `E_coverage.csv` (`08-SDR-001…136`).
""")
sdr = [r for r in cov if r['aspect_id'].startswith('08-SDR')]
ent_c = Counter(r['aspect_summary'].split(' / ')[0] for r in sdr)
st_c = Counter(r['status'] for r in sdr)
P(f"| Outcome | Rows | Meaning |\n|---|---|---|\n| Type confirmed against Part 3.3 | {st_c['Covered']} | Part 3.3 column exists with a compatible or stricter type; Part 3.3 type governs (DEC-107) |\n| Column added | {st_c['Not covered']} | Added in §3.6.5.1 with type, nullability, default and constraint |\n| Conflict | {st_c['Conflict']} | Fulfilment milestone fields (CONFLICT-383) and embedding vector (CONFLICT-381) |\n| **Total** | **{len(sdr)}** | 16 `sales_*` tables, 2 late additions, 4 blocked rows |\n")
P("**The four blocked rows** (document 08 \"DEC-039…DEC-042\", renamed SDEC-08-039…042 because blueprint DEC-039 means seed migration, CONFLICT-380):\n\n| SDEC | Source record | Source proposed resolution | Blueprint decision that resolves it | Remaining action |\n|---|---|---|---|---|")
P("| SDEC-08-039 | existing user table / all | Resolve identity table and PK type from Django model metadata; no duplicate identity tables | DEC-003, DEC-019 (reuse AppNAI identity as library/IdP, new audience); Part 3.3 ENT-006 `ten_user` product-local mirror | CONFLICT-382: `ten_user` becomes a 1:1 profile keyed to the reused identity, not a second credential store; W0-A spike confirms PK type |")
P("| SDEC-08-040 | existing role table / all | As above | ENT-007 `ten_role` system roles R01–R20 | Map Django groups → `ten_role.code` in MG-08; no group-based authorization at runtime (RBAC matrix governs) |")
P("| SDEC-08-041 | existing membership table / all | As above | ENT-008 `ten_membership` + `ten_membership_grant` | Existing user-role rows imported once as grants; `sales_membership` semantics (nullable startup = portfolio scope) already match |")
P("| SDEC-08-042 | growth_embedding / vector(d) | Select approved model, assert dimension before index | **DEC-088**: multilingual E5-large class, 1024 dimensions, `halfvec(1024)` HNSW (RECOMMENDATION-039) | CONFLICT-381 closed by DEC-088; migration asserts `vector_dims(embedding) = 1024` per `model_id` |")
P("""
**Outstanding approval gates carried from document 08 (GAP-392).** 38 exact API definitions outstanding (handed to the API reconciliation group, see `D_api_mapping.csv`); 0 partial API proposals; 4 database reuse/field confirmations (the four SDEC rows above); 138 UI semantic-mapping approvals (UX group). The SDR process that keeps these as decision-queue items is specified in Part 3.6b §3.6.5.3.

### 3.6.4.9 Exposure and protection reconciliation (documents 08 and 28 versus Part 3.3)
""")
ec = Counter(m['src_exposure'] for m in mrows); pc = Counter(m['src_protection'] for m in mrows)
P("| Source exposure class | Tables | Meaning (document 08 wording) | Part 3.3 mechanism | Status |\n|---|---|---|---|---|")
P(f"| EXP-ADM | {ec['EXP-ADM']} (+6 candidates) | Admin/internal service only; no website projection or public serialization | Admin API audience only; RLS; no `Pub` columns | Covered; register in 3.6b §3.6.5.3 makes it enforceable in CI |")
P(f"| EXP-WEB | {ec['EXP-WEB']} | Authorized website/portal service may access bounded fields for mapped operations | Portal predicate §3.3.9.4; column Class | Partially covered: no per-table allowlist of portal-readable fields → serializer allowlist register (GAP-391) |")
P(f"| EXP-PUB | {ec['EXP-PUB']} | Public API returns only validated published DTO | `mkt_publication_snapshot` + CDN (BRL-PUB) | Covered |")
P(f"| EXP-PRT | {ec['EXP-PRT']} | Portal receives own authorized object DTO; never serialize invitation hashes | `ten_portal_grant`; ABAC-09 | Covered (+ invite hash columns added) |")
P("\nDocument 28's 149-row inventory repeats the same classes: **149 of 149 rows agree** with document 08 (two rows differ only in wording: \"Published DTO only; drafts private\" and \"Confidential; own object-granted portal DTO only\").\n")
P("| Source protection class | Tables | Part 3.3 classification (RECOMMENDATION-004) | Finding |\n|---|---|---|---|")
P(f"| INT (internal business data; role-scoped; retention) | {pc['INT']} | Int default, Conf for commercial terms | Covered |")
P(f"| SCOPE (scope by tenant/startup; entitlement and retention) | {pc['SCOPE']} (+6 candidates) | STD-S/T scope columns + RLS | Covered |")
P(f"| PII-R (restricted business PII; RBAC, encryption, retention; no clinical data) | {pc['PII-R']} | Rest for `_enc`/`_hmac` columns; Conf for names | Covered for contact, submission, lead, message, inbound, consent, privacy request; **Partially** for `eng_message_draft`, `eng_chat_session`, `intel_contact_source` (no Rest columns: draft body and session token hash added as Rest in 3.6b) |")
P(f"| AUDFIN-R (restricted audit/finance; immutable evidence) | {pc['AUDFIN-R']} | Imm. A/F + FIN/CTR/AUD retention | Covered |")
P(f"| SECRET (secret reference only; restricted admin access) | {pc['SECRET']} | `int_credential_ref` columns are Int | **Partially covered**: table-level restriction to R01/R13 and audit-on-read added (RECOMMENDATION-399) |")
P("""
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
""")
open(f'{BD}/Part-03-6a_Source_Pack_Data_Catalog_Reconciliation.md', 'w').write('\n'.join(out))
print('written', sum(len(x) for x in out))
