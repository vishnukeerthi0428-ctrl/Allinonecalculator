"""Group J: render Part-11-10b (catalogue reconciliation)."""
import json,os,csv,re,sys
from collections import Counter,defaultdict
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from j_render_lib import tbl,esc,rng
d=json.load(open(HERE+'/j_items.json')); T=json.load(open(HERE+'/j_tables.json')); IDS=json.load(open(HERE+'/j_ids.json'))
BP='/home/user/Allinonecalculator/blueprint/'
SKU=IDS['SKU']; APR=IDS['APRTC']
G={r['source_id']:r for r in csv.DictReader(open(BP+'final/coverage/G_test_mapping.csv'))}
Q={r['qc_id']:r for r in csv.DictReader(open(BP+'final/coverage/H_qc_map.csv'))}
W={r['work_item']:r for r in csv.DictReader(open(BP+'final/coverage/H_workitem_story_map.csv'))}
# legacy tests
ids=sorted({r['id'] for r in d['d_test']})
fam=lambda i: re.sub(r'\d+[A-Z]?$','',i)
lt=defaultdict(Counter); rowsper=Counter(fam(r['id']) for r in d['d_test']); pend=Counter(fam(r['id']) for r in d['d_test'] if r['disposition'].startswith('Pending'))
for i in ids: lt[fam(i)][G[i]['status']]+=1
STAT={'E':'Equivalent','A':'Alias-equivalent','M':'Class-mapped','P':'Partial + ENH','N':'New ENH'}
ltrows=[[f,rowsper[f],sum(lt[f].values()),pend[f]]+[lt[f][k] for k in 'EAMPN'] for f in sorted(lt)]
ltrows.append(['**Total**',sum(rowsper.values()),len(ids),sum(pend.values())]+[sum(lt[f][k] for f in lt) for k in 'EAMPN'])
qc=Counter((Q[r['id']]['layer_id'] if r['id'].startswith('QC') else 'UX-QC', Q[r['id']]['status'].split(':')[0]) for r in d['d_qc'])
qcl=defaultdict(Counter)
for (l,s),n in qc.items(): qcl[l][s]+=n
qcrows=[[l,sum(c.values()),c['Covered'],c['Partially covered'],', '.join(i['id'] for i in d['d_qc'] if (Q[i['id']]['layer_id'] if i['id'].startswith('QC') else 'UX-QC')==l and Q[i['id']]['status'].startswith('Partially'))] for l,c in sorted(qcl.items())]
tf=defaultdict(lambda:[0,0.0,0.0,0.0])
for r in d['d_task']:
    w=W[r['id']]; f=re.sub(r'\d+$','',r['id']); tf[f][0]+=1
    for k,c in enumerate(['low_pd','base_pd','high_pd']):
        try: tf[f][k+1]+=float(w[c] or 0)
        except: pass
trows=[[f,v[0],'%.1f / %.1f / %.1f'%tuple(v[1:])] for f,v in sorted(tf.items())]
trows.append(['**Total**',sum(v[0] for v in tf.values()),'%.1f / %.1f / %.1f'%tuple(sum(v[k] for v in tf.values()) for k in (1,2,3))])
# workflow register
steps=defaultdict(list)
for r in d['steps']: steps[r[0].split('-STEP')[0]].append(r)
wft=defaultdict(dict)
for r in d['wf_tests']: wft[r[1]][r[0].split('-TC-')[1]]=r
at={r[2]:r for r in d['wb_at'] if 'WF' in r[2]}
ev={r[0].replace('EVAL-',''):r for r in d['eval']}
CODE={'Evidence retrieval':'ER','AI inference':'AI','Deterministic calculation':'DC','Deterministic domain logic':'DL','Policy gate / human review':'PG','Deterministic identity / reconciliation':'IR','External effect':'EX'}
wrows=[]
for w in sorted(wft):
    sk=w[:9]; s=SKU[sk]; t=wft[w]; a=at[w]
    cats='POS, INPUT, SCOPE, ENT, DUP, QUALITY, BUDGET, RECOVERY'+(', APPROVAL, EFFECT' if 'APPROVAL' in t else '')
    st='; '.join(f"{x[0].split('-STEP-')[1][:2]} {CODE[x[1]]}: {x[2]}" for x in steps[w])
    e=ev.get(w); evs=f"{e[0]} ({e[3]} AI; {e[4]}; {e[5]})" if e else '— (no AI step)'
    extra=f"; +{APR[w]}" if w in APR else ''
    wrows.append([w,a[3],s['cls'],cats+extra,f"{t['POS'][2]} → {t['POS'][3]}",st,evs,a[10],a[11].replace('SM-UX-UAT-',''),'Partially covered' if s['cls']=='H' else 'Not covered'])
skrows=[[k,v['name'],v['family'],v['bundle'],v['meter'],v['cls']+' · '+{'H':'High overlap','M':'Partial overlap','N':'New domain'}[v['cls']],v['ep'],v['anchor']] for k,v in SKU.items()]
ent=[[r[0],r[3],r[4],r[6],r[7],r[8],r[10],'Partially covered','TC-V12-J-019'] for r in d['wb_at'] if 'ENT' in r[0]]
# counts
N=json.load(open(HERE+'/j_nums.json'))
ACC=T['acc_register']; cov=sum(1 for r in ACC if r[6]=='Covered'); newacc=len(ACC)-cov
add=[('Workflow scenario tests (SM-SVC-##-WF##-TC-*)',1342,'TC-V12-J-001…010'),('Step-level tests (…-STEP-##-TC)',517,'TC-V12-J-011…017'),('Workflow acceptance (…-AT01)',156,'TC-V12-J-018'),('SKU entitlement acceptance (…-ENT-AT01)',39,'TC-V12-J-019'),
     ('V12 acceptance register rows not already covered (AIX/CJ/MT/MOB/OPT-TC)',newacc,'canonical rows §11.10.5.3'),('UAT-E2E-01 relationship journey',1,'TC-V12-J-020'),('Automation exceptions EXC-01…07',7,'TC-V12-J-021…027'),
     ('Approval-binding instances (panel finding)',N['apr_gap'],'TC-V12-J-201…%03d'%(200+N['apr_gap'])),('Prototype-parity regression classes',14,'TC-V12-J-101…114'),('Gap tests (numeric KPI domain, benchmark, CI rules, scorecards, gates)',10,'TC-V12-J-121…130')]
total_new=sum(x[1] for x in add)
cnt_rows=[[a,b,c] for a,b,c in add]+[['**New executable tests**',total_new,''],['Blueprint baseline (V12 brief)',4156,'Parts 6.x, 6.8–6.10, 9.6–9.10'],['**Blueprint total after Part 11.10**',4156+total_new,''],['Aliases only (no new row)',cov+10,'12 register tests already covered + 10 XS = TC-ENH-J-025…034'],['Evaluation suites bound as gates (not counted as tests)',111,'EVAL-SM-SVC-##-WF##']]
json.dump({'total_new':total_new,'newacc':newacc,'cov':cov},open(HERE+'/j_counts.json','w'))
OUT=BP+'Part-11-10b_V12_Tests_QC_Coding_Backlog.md'
Hd=f'''# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.10b), V12 Tests (Unit/SIT/UAT/AI), Quality Control and Acceptance Evidence, Coding Standards and Development Backlog: Catalogue Reconciliation

| Field | Value |
|---|---|
| Document | Application Blueprint · Part 11.10b. Catalogue reconciliation for Group R9 (J): the archived test, QC and task registers of FSD V12 chapter 40; the 156-workflow test catalogue (1,342 scenarios, 517 step tests, 111 EVAL suites, 156 AT01); the 39-SKU classification and entitlement tests; the count reconciliation. Part 11.10a holds §11.10.1–3; Part 11.10c holds §11.10.5–10 |
| Version | 1.2 · 28 Nov 2026 |
| Baseline | `final/coverage/G_test_mapping.csv`, `H_qc_map.csv`, `H_workitem_story_map.csv` (Parts 6.8, 6.9); epics EP-01…21 (Part 0 §0.10.2); Parts 6.1, 6.4, 6.10; Parts 9.7–9.9 advanced agents (AG-039…080) |
| Roles applied | Test Architect (lead), Head of Quality Engineering, Agile Delivery Lead, Principal Engineer |
| ID ranges used | As Part 11.10a |

---

## 11.10.4 Catalogue reconciliation

### 11.10.4.1 Archived registers in FSD V12 chapter 40 (tests, QCs, work items)

Chapter 40 lists every archived row of source documents D22 (tests), D23 (QCs) and D20 (work items) with the disposition "pending semantic mapping", "map to current gate" or "retain predecessor/estimate; not approved". The blueprint mapped all of them in Parts 6.8 and 6.9; the semantic approval of each mapping is FR-ENH-H-006 (Part 6.9b §6.9.5.3.5). Result: **Matched, no change** (DEC-685).

**Tests (1,029 rows, 589 distinct IDs).** 880 rows say "ID referenced; compare fixture/outcome" (the same ID referenced again by another source table); 149 say "Pending semantic mapping".

{tbl(['Family','Rows in ch40','Distinct IDs','Rows pending semantic mapping','Equivalent','Alias-equivalent','Class-mapped','Partial + ENH','New ENH'],ltrows)}
**Quality controls (245).** Layer and blueprint status from `H_qc_map.csv` (Part 6.9b §6.9.5.1.8). The partially covered QCs were closed by Part 6.9b §6.9.5.1.6 and Part 6.10 §6.10.5.

{tbl(['Layer','QCs','Covered','Partially covered (closed in 6.9b/6.10)','Partial QC IDs'],qcrows)}
**Work items (162).** Predecessors and low/base/high estimates in chapter 40 are identical to `H_workitem_story_map.csv` (0 differences).

{tbl(['Family','Items','PD low / base / high'],trows)}
### 11.10.4.2 Workflow test catalogue (156 workflows)

One row per workflow. **Scenario tests** lists the suffixes of the V12 tests `<workflow>-TC-<suffix>` (each executes through class TC-V12-J-001…010, Part 11.10c §11.10.5.2); "+TC-V12-J-2##" marks an approval-binding test added by the panel. **POS** is the V12 positive fixture → expected output; INPUT uses the same input "missing or malformed"; the other suffixes use the class fixtures. **Step tests** lists `<workflow>-STEP-<nn>-TC` with class code (ER evidence retrieval, AI inference, DC deterministic calculation, DL deterministic domain logic, PG policy gate / human review, IR identity / reconciliation, EX external effect; classes TC-V12-J-011…017). **EVAL** is the suite that must pass before any AI step test counts (QC-V12-J-011). **AT01 KPI** and **UI refs** are from the workbook acceptance test (UI refs are SM-UX-UAT screen acceptance IDs, i.e. blueprint A###/W## via the Part 6.1 §6.1.12.5 alias rule). **Class** is the SKU overlap class of §11.10.4.3.

{tbl(['Workflow','Name','Class','Scenario tests','POS fixture → output','Step tests','EVAL suite','AT01 KPI','UI refs (SM-UX-UAT-)','Before'],wrows)}
### 11.10.4.3 SKU classification (39 services) and entitlement acceptance

The class measures how much of the SKU the approved blueprint already builds; it drives the status before of every workflow, step and AT test and the build effort (Part 11.10c §11.10.5.12).

| Class | Meaning | Reuse factor on step build | SKUs |
|---|---|---|---|
| H · High overlap | The capability is built in Release 1/2 (epic named); V12 adds the SKU packaging, workflow DTO, step registry entries and entitlement binding | 0.20 | 25 (SM-SVC-01…25) |
| M · Partial overlap | Partly designed in the blueprint (an advanced agent card in Parts 9.7–9.9 or an adjacent module) but not built in Release 1/2 | 0.55 | 10 (27, 29, 30, 32, 33, 35, 36, 37, 38, 39) |
| N · New domain | No blueprint design: voice and telephony, agentic commerce, marketplace operations, product-led usage intelligence | 1.00 | 4 (26, 28, 31, 34) |

{tbl(['SKU','Service','Family','Bundle','Meter unit','Class','Epic','Blueprint anchor'],skrows)}
**Single-SKU entitlement acceptance (39 tests, SM-SVC-##-ENT-AT01).** Each test buys only this SKU and proves that the selected service runs, an unpurchased service is blocked, no paid upstream SKU is compulsory and revocation stops new execution. The blueprint enforces plan entitlements (TC-16-062, TC-20-054) but has no per-SKU purchase; class TC-V12-J-019.

{tbl(['Test','Scenario','Preconditions','Execution steps','Expected','Negative and boundary','Target KPI','Before','Class'],ent)}
### 11.10.4.4 How the V12 test levels map to the blueprint levels

| V12 family | V12 level wording | Blueprint level (Part 6.1) | Where it runs | Gate |
|---|---|---|---|---|
| …-STEP-##-TC (DL, DC, IR) | Step-level, deterministic | UT (unit) | CI on every PR (PL-04) | Merge |
| …-STEP-##-TC (ER, AI, PG, EX) | Step-level with adapter or gateway | IT (integration, stubs and sandboxes) | CI nightly + staging | G2 |
| …-TC-POS/INPUT/QUALITY | Workflow scenario | SIT (system integration) | Staging, fictional fixtures | G3 |
| …-TC-SCOPE/ENT/DUP/BUDGET/RECOVERY/APPROVAL/EFFECT | Workflow negative and recovery | SIT + security / chaos | Staging with fault injector | G3, BLK-1/2/5 |
| …-AT01, …-ENT-AT01 | Acceptance | UAT (UAT packs §6.1.13.3) | UAT environment, business users | G4 |
| AIX-TC, EVAL-SM-SVC | AI acceptance and evaluation | AI evaluation (Part 6.4) | Eval runner AG-002 | Prompt promotion and G3 |
| CJ-TC | Compliance acceptance | SIT + legal review | Staging; legal sign-off | G4 |
| MT-TC, MOB-AT, OPT-TC | Architecture, mobile and optimization acceptance | SIT / SYS / E2E per family | Staging | G3/G4 |
| XS, UAT-E2E-01, EXC | Release and journey | E2E + UAT | Staging and UAT | Release go/no-go |
| V#-QA, V12-ENT, V12-LOC | Prototype checks | Parity regression (Playwright) | CI nightly on both apps, four viewports | G3 (UI) |

### 11.10.4.5 Count reconciliation

{tbl(['Item','Count','Blueprint IDs'],cnt_rows)}
| Register | Before | Added | After | Note |
|---|---|---|---|---|
| Test cases | 4,156 | {total_new:,} | {4156+total_new:,} | Executable tests; templates TC-V12-J-001…019 are class definitions, counted through their instances |
| Quality controls | 245 | 17 | 262 | QC-V12-J-001…017 (Part 11.10c §11.10.5.7) |
| Work items | 162 | 53 | 215 | 39 SM-SVC-##-BUILD + 14 TASK-V12-J-001…014 |
| Coding standards | CS-* families of Part 4.4a | 4 | — | CS-V12-J-01…04 |
| KPIs | OKPI-01…35 | 0 | OKPI-01…35 | V12 KPI-01…35 are aliases |

### Quality gate: Part 11.10b

| # | Item | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every workflow row cites its V12 IDs, workbook AT01 and EVAL suite |
| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | SKU classes are ASSUMPTION-923; approval gaps GAP-924 |
| 3 | IDs unique and consistent | Pass | V12 IDs kept literally; TC-V12-J classes only |
| 4 | No requirement lacks a test | Pass | 156/156 workflows have ≥ 8 scenarios, 1–4 step tests and AT01; 39/39 SKUs have an entitlement test |
| 5 | Negative, edge, security, accessibility | Pass | SCOPE, ENT, DUP, BUDGET, RECOVERY on every workflow; APPROVAL and EFFECT on 47 + 9 |
| 6 | Agents complete | N/A | No agent added |
| 7 | Time-sensitive facts flagged | Pass | Sandboxes and tools flagged in Part 11.10c |
| 8 | No restricted data to free tiers | Pass | AI step class asserts Tier 2 is never used for personal or restricted data |
| 9 | Consistent with earlier parts | Pass | Legacy mappings unchanged; 0 estimate differences |

**Status: Part 11 Batch 11.10b complete. 589 archived test IDs, 245 QCs and 162 work items confirmed; 156 workflows, 39 SKUs and {total_new:,} new executable tests reconciled; test total {4156+total_new:,}.**
'''
open(OUT,'w').write(Hd); print(OUT,len(Hd),total_new)
