"""Group J: render Part-11-10c (enhancements, effort, conflicts, decisions, review, tags, gate)."""
import json,os,csv,re,sys
from collections import Counter,defaultdict
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from j_render_lib import tbl,esc,rng
from j_render_c1 import HDR,SCEN,STEP,E2E,PAR,GAP,FAM,QCS,CSV12
d=json.load(open(HERE+'/j_items.json')); T=json.load(open(HERE+'/j_tables.json')); IDS=json.load(open(HERE+'/j_ids.json')); C=json.load(open(HERE+'/j_counts.json'))
BP='/home/user/Allinonecalculator/blueprint/'
SKU=IDS['SKU']; APR=IDS['APRTC']
RATE=(4545,5682,6818)
steps=defaultdict(list)
for r in d['steps']: steps[r[0].split('-STEP')[0]].append(r)
at={r[2]:r for r in d['wb_at'] if 'WF' in r[2]}
# approval-gap instances
aprrows=[]
for w,t in APR.items():
    pg=[s for s in steps[w] if s[1]=='Policy gate / human review']
    aprrows.append([t,f'APPROVAL binding for {w} ({at[w][3]})',f'{w}; panel finding GAP-924; class TC-V12-J-009','Approval bound to the payload hash of the step "'+(pg[0][2] if pg else steps[w][-1][2])+'"; requester R04, approver R05; expiry 24 h','1. Change the payload after approval and continue. 2. Continue after expiry. 3. Self-approve','Blocked; new approval required; self-approval refused; 0 downstream effects','P0','Security','DT','Y','SIT'])
# canonical register rows
reg={r[0]:r for r in d['reqreg']}
canon=[]
covl=[r[0] for r in T['acc_register'] if r[6]=='Covered']
for r in T['acc_register']:
    tid,rid,pri,title,owner,acc,sb,loc,sa=r
    if sb=='Covered': continue
    fam=re.sub(r'-?\d+$','',rid).replace('CJ-R','CJ')
    pre,neg,typ,lvl,ep=FAM[fam]
    a=d['acc'].get(tid,{})
    req=a.get('req') or a.get('func') or title
    p=pri if pri in('P0','P1','P2') else 'P1'
    canon.append([tid,f'{rid} {title}',f'{rid}; {ep}; blueprint: {loc}',pre,f'1. Prepare the family fixture. 2. Exercise: {req} 3. Assert the V12 acceptance. 4. Negative: {neg.split(":")[0]}',f'{acc} Negative: {neg}.'+(' Region-conditional until CONFLICT-924 is decided.' if sb=='Conflict' else ''),p,typ,'EP','Y',lvl])
# effort
build=T['build']
def tup(s): return tuple(float(x) for x in s.split('/'))
cls_tot=defaultdict(lambda:[0,0,0]); cls_n=Counter()
for r in build:
    c=r[2]; cls_n[c]+=1
    for k in range(3): cls_tot[c][k]+=r[10][k]
reg_part=sum(1 for r in T['acc_register'] if r[6]=='Partially covered'); reg_not=sum(1 for r in T['acc_register'] if r[6] in('Not covered','Conflict'))
t4=tuple(round(b+reg_part*p+reg_not*n,1) for b,p,n in zip((2,3,5),(0.15,0.25,0.4),(0.3,0.5,0.8)))
QA=[
['TASK-V12-J-001','Parameterized workflow-scenario harness: 10 classes, fixture loader, provider stub modes (success, timeout, 429, lost response), fault injector hooks, evidence capture','QA lead + backend lead','Workflow registry (FL-01), DTO schemas (FSD Appendix B), entitlement engine','TC-V12-J-001…010 green on pilot SM-SVC-01-WF01; QC-V12-J-011',(6,9,14)],
['TASK-V12-J-002','Step-level harness: 7 classes, golden fixtures, model-call counter, EVAL precondition','QA lead + AI lead','TASK-V12-J-001; gateway test double','TC-V12-J-011…017 green on SM-SVC-01',(4,6,9)],
['TASK-V12-J-003','EVAL gate wiring: bind 111 EVAL-SM-SVC suites as preconditions of AI step tests and prompt promotion (datasets are produced under Group R5)','AI lead + QA','Eval runner AG-002; suites from R5','QC-V12-J-011/013; TC-V12-J-129',(5.6,11.1,22.2)],
['TASK-V12-J-004',f'V12 acceptance register in A090 and automation of {reg_part+reg_not} canonical rows ({reg_part} partial × 0.15/0.25/0.4 pd + {reg_not} new × 0.3/0.5/0.8 pd + register 2/3/5 pd)','Test Architect + squads','FR-V12-J-004; family fixtures','All canonical rows executable; QC-V12-J-009',t4],
['TASK-V12-J-005','RCTCFE scorecard, 20-dimension scorecard and five-gate status in A090 (FR-V12-J-001…003)','Frontend + backend','A090 release record','TC-V12-J-126…128; US-21-YJ02/03',(3,5,8)],
['TASK-V12-J-006','Prototype-parity regression suite: 14 Playwright classes on both apps at four viewports','QA automation','Production builds of Website and Admin','TC-V12-J-101…114 nightly green',(7,10.5,17.5)],
['TASK-V12-J-007','Localisation audit automation (ar, hi, de, fr × desktop and mobile)','Frontend lead + QA','i18n bundles','TC-V12-J-104; QC-V12-J-016',(1.5,2.5,4)],
['TASK-V12-J-008','Release and journey pack: UAT-E2E-01, EXC-01…07, XS-01…10 execution scripts and UAT sheets','QA + Product Owner','TASK-V12-J-001','TC-V12-J-020…027; TC-ENH-J-025…034',(3,5,8)],
['TASK-V12-J-009','Historical test index deduplication (REC-19): 799 archived + 1,342 workflow scenarios; equivalence review list','Test Architect','G_test_mapping.csv','TC-V12-J-130; QC-V12-J-005',(3,5,8)],
['TASK-V12-J-010','CI rules CS-V12-J-01…04 (lint, static step-class check, test markers, fixture registry)','Principal Engineer + DevOps','PL-04, PL-05','TC-V12-J-123/124; QC-V12-J-015',(2,3,5)],
['TASK-V12-J-011','Preflight extension: KPI numeric-domain validation, benchmark validation, five new groups (FR-V12-J-005)','Backend + QA','FR-ENH-H-005 preflight','TC-V12-J-121/122; US-21-YJ05',(2,3,5)],
['TASK-V12-J-012','SKU entitlement sign-off process: UAT sheet per SKU, Finance and Product Owner signatures','Product Owner + QA','Subscription engine','QC-V12-J-012; TC-V12-J-019',(1,1.5,2.5)],
['TASK-V12-J-013',f'Approval-binding instances for {len(APR)} workflows (TC-V12-J-201…{200+len(APR)})','QA','TASK-V12-J-001','QC-V12-J-017',(round(0.2*len(APR),1),round(0.3*len(APR),1),round(0.5*len(APR),1))],
['TASK-V12-J-014','Evidence record field extension (tenant fixture, fixture version, input, environment) and validator rules','Backend + QA','EVR validator (Part 6.9b)','TC-V12-J-125; QC-V12-J-007',(1,1.5,2.5)],
]
qa_tot=[round(sum(x[5][k] for x in QA),1) for k in range(3)]
b_tot=[round(sum(cls_tot[c][k] for c in cls_tot),1) for k in range(3)]
grand=[round(b_tot[k]+qa_tot[k],1) for k in range(3)]
def lakh(pd,k): return pd*RATE[k]/1e5
pkgA=[round(cls_tot['H'][k]+qa_tot[k],1) for k in range(3)]
pkgB=[round(cls_tot['M'][k]+cls_tot['N'][k],1) for k in range(3)]
json.dump({'b_tot':b_tot,'qa_tot':qa_tot,'grand':grand,'pkgA':pkgA,'pkgB':pkgB},open(HERE+'/j_effort.json','w'))
brows=[]
for r in build:
    sk=r[0][:9]; s=SKU[sk]; c=r[2]
    rel='Release 2 candidate (W4–W5) under CR-V12-J-01' if c=='H' else 'W6 Phase 2 under CR-V12-J-02'
    deps='Foundation; subscription/entitlement engine; workflow registry; DTO schemas (Appendix B); TASK-V12-J-001/002'+('; provider adapter and outbox for EX steps' if any(st[1]=='External effect' for w in steps if w.startswith(sk) for st in steps[w]) else '')
    acc=f'{sk}-WF01…04-TC-*, {sk}-WF0#-STEP-##-TC, {sk}-WF0#-AT01, {sk}-ENT-AT01, EVAL suites; QC-V12-J-011/012'
    owner={'H':'Vertical squad (backend + frontend) + QA','M':'Backend lead + AI lead + QA','N':'Contract engineer pair + Principal Engineer + QA'}[c]
    note={'SM-SVC-26':'Voice: consent and call-recording law per jurisdiction (verify); AI never places consequential calls without L1 approval','SM-SVC-28':'Agentic commerce: AI-to-AI offers are drafts; signing, paying and committing stay human (L1)','SM-SVC-37':'Pricing: recommendations only; AI never sets prices','SM-SVC-31':'Marketplace: listing and order effects human-approved','SM-SVC-38':'SMS/RCS: India DLT registration (CJ-TC-06)','SM-SVC-39':'Procurement: purchase orders human-approved'}.get(sk,'')
    brows.append([r[0],s['name'],c,r[4],r[5],r[6],owner,deps,acc,r[7],r[8],r[9],rel+('; '+note if note else '')])
clsrows=[[c,{'H':'High overlap','M':'Partial overlap','N':'New domain'}[c],cls_n[c]]+['%.1f'%cls_tot[c][k] for k in range(3)] for c in 'HMN']
clsrows.append(['**All**','',sum(cls_n.values())]+['%.1f'%b_tot[k] for k in range(3)])
qarows=[[x[0],x[1],x[2],x[3],x[4],'%.1f / %.1f / %.1f'%x[5]] for x in QA]
qarows.append(['**Total**','','','','','%.1f / %.1f / %.1f'%tuple(qa_tot)])
costrows=[]
for name,v in [('A. SKU packaging, High overlap (25 SKUs)',[round(cls_tot['H'][k],1) for k in range(3)]),('B. QA, QC and test infrastructure (TASK-V12-J-001…014)',qa_tot),('**CR-V12-J-01 = A + B (Release 2 candidate)**',pkgA),('C. Partial-overlap SKUs (10)',[round(cls_tot['M'][k],1) for k in range(3)]),('D. New-domain SKUs (4)',[round(cls_tot['N'][k],1) for k in range(3)]),('**CR-V12-J-02 = C + D (W6 Phase 2)**',pkgB),('**Total new backlog**',grand)]:
    costrows.append([name,'%.1f / %.1f / %.1f'%tuple(v),'₹%.2f L / ₹%.2f L / ₹%.2f L'%tuple(lakh(v[k],k) for k in range(3))])
OUT=BP+'Part-11-10c_V12_Tests_QC_Coding_Backlog.md'
gh=lambda s: '```gherkin\n'+s.strip()+'\n```\n'
H=f'''# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.10c), V12 Tests (Unit/SIT/UAT/AI), Quality Control and Acceptance Evidence, Coding Standards and Development Backlog: Enhancements, Effort, Conflicts and Decisions

| Field | Value |
|---|---|
| Document | Application Blueprint · Part 11.10c. Enhancements written for Group R9 (J): canonical test rules, 30 parameterized and specific test classes, the canonical rows of the V12 acceptance register, 17 quality controls, the scorecard instruments, 4 coding standards, 6 functional requirements and 5 stories, the backlog of 53 work items with estimates, the effort impact, conflicts, decisions, panel review, tags register and quality gate (§11.10.5–§11.10.10) |
| Version | 1.2 · 28 Nov 2026 |
| Baseline | Part 6.1 test template (§6.1.12.2) and levels; Part 6.9b QC register and evidence validator; Part 4.4a §4.4.5.1 coding standard; Part 8.1 plan; DEC-228, DEC-230, DEC-231, DEC-418, DEC-421, DEC-422; rates ₹4,545 / ₹5,682 / ₹6,818 per pd (Part 9.10 §9.10.6) |
| Roles applied | Head of Quality Engineering, Test Architect, Principal Engineer, Agile Delivery Lead |
| ID ranges used | As Part 11.10a |

---

## 11.10.5 Enhancements

### 11.10.5.1 Canonical test IDs and execution rules (DEC-680, DEC-682, DEC-684, DEC-690)

| Rule | Statement | Source |
|---|---|---|
| R-1 | A V12 test ID is the canonical ID of the test. The blueprint executes it through a parameterized class (TC-V12-J-001…019) or a canonical row (§11.10.5.3); where a blueprint TC already asserts the same thing, the V12 ID is an alias of that TC | V12 brief; DEC-680 |
| R-2 | Class tests are parameterized by workflow and step (pytest `parametrize`, Playwright projects). They are never copied per workflow (CS-V12-J-03) | Panel |
| R-3 | Status of every V12 test is "Not run" until executed in staging or UAT with fictional, scoped fixtures and authorized sandboxes. Prototype or local HTML checks never make a production test pass | FSD 33 V8, V5; DEC-682 |
| R-4 | Each execution writes an evidence record with build, tenant fixture, fixture version, input, expected, actual, status, evidence link, environment, executor, reviewer and date; executor ≠ reviewer | FSD 33 V5; FSD 34 V3; QC-V12-J-007 |
| R-5 | A workflow is test-complete when its scenario set, one test per step, AT01 and (for each AI step) a green EVAL suite exist and pass; "Skipped" and "Not run" count as missing | QC-V12-J-011; DEC-684 |
| R-6 | An AI-inference step test counts only after its EVAL-SM-SVC suite passes the task-type gate of FSD 16.4 (classification F1 ≥ 0.90 and no class < 0.80; extraction exact match ≥ 95%, schema 100%; generation claims 100%, citations ≥ 95%, rubric ≥ 4/5, toxicity 0; ranking NDCG@10 ≥ baseline; translation ≥ 4/5 per language; adversarial 0 violations) | FSD 16.4; AIX-05 |
| R-7 | Archived tests (799) and V12 scenarios are deduplicated by equivalence review before execution; unique records are never deleted | FSD 33 V5; REC-19 |
| R-8 | Consequential effects in any test (send, publish, order, booking, payment instruction, submission) require a human approval bound to the payload hash; autonomy stays L1. No test may assert an AI-executed signature, payment, bid submission or price | Safety invariants (V11 brief) |
| R-9 | Tier 2 free fallbacks are off in every fixture that holds personal or restricted data; the AI step class asserts this | DEC-418; safety invariants |
| R-10 | Execution sequence: UT and IT on every PR; SIT nightly and per release candidate; UAT and E2E per release; parity regression nightly | Part 6.1 levels; §11.10.4.4 |

```mermaid
flowchart TD
  REG["Workflow registry<br/>156 workflows, 517 steps"] --> GEN["Parameterized classes<br/>TC-V12-J-001 to 019"]
  FX["Versioned fictional fixtures<br/>FX-workflow-v1"] --> GEN
  EV["EVAL-SM-SVC suites<br/>111 gates"] --> GEN
  GEN --> RUN["Execution in CI, staging, UAT"]
  RUN --> EVR["Evidence record<br/>build, fixture, input, expected, actual, reviewer"]
  EVR --> VAL["Validator V-01 to V-14<br/>plus TC-V12-J-125"]
  VAL --> CMP["Completeness gate<br/>QC-V12-J-011"]
  CMP --> PRE["Combined preflight<br/>FR-ENH-H-005 plus V12 groups"]
  PRE --> GATE["Five-gate release status<br/>QC-V12-J-003"]
```

### 11.10.5.2 Workflow scenario classes TC-V12-J-001…010 and approval-binding instances

Template of Part 6.1 §6.1.12.2. `<wf>` is the workflow ID (Part 11.10b §11.10.4.2); the fixture pack FX-`<wf>`-v1 holds the V12 input of the workflow. Classes 001–008 run for all 156 workflows (1,248 tests); 009 and 010 run for the 47 workflows where V12 defines APPROVAL and EFFECT (94 tests) and 009 also for the 9 panel instances below.

{tbl(HDR,SCEN)}
**Approval-binding instances added by the panel (GAP-924).** These workflows route approval, legal review or submission readiness in their steps, but V12 gives them no APPROVAL scenario.

{tbl(HDR,aprrows)}
### 11.10.5.3 Step classes, acceptance classes and the canonical V12 acceptance rows

**Step classes TC-V12-J-011…017 and acceptance classes TC-V12-J-018/019.**

{tbl(HDR,STEP)}
**Family fixtures used by the canonical rows.**

{tbl(['Family','Pre-conditions and fixture','Negative variant','Type','Level','Epic'],[[k]+list(v) for k,v in FAM.items()])}
**Canonical rows for the {len(canon)} V12 acceptance tests that were not already covered.** The V12 acceptance is the expected result, unchanged. The {len(covl)} covered tests ({', '.join(covl)}) are aliases of the blueprint TCs listed in Part 11.10a §11.10.3.

{tbl(HDR,canon)}
### 11.10.5.4 UAT-E2E-01 and automation exceptions

{tbl(HDR,E2E)}
### 11.10.5.5 Prototype-parity regression classes TC-V12-J-101…114

Every prototype check of V3–V12 is assigned to one class (Part 11.10a §11.10.3.10). The class runs on the production React builds, on the Website and the Admin, at 1366 × 768 and 390 × 844 (plus the widths in 102), nightly and on each release candidate.

{tbl(HDR,PAR)}
### 11.10.5.6 Gap tests TC-V12-J-121…130

{tbl(HDR,GAP)}
### 11.10.5.7 New quality controls QC-V12-J-001…017

They extend the QC register of Part 6.9b §6.9.5.1.8 (245 → 262) and use its layers, evidence manifest and sign-off sequence.

{tbl(['QC','Layer','Check','Procedure','Evidence','Gate','Signatory','Source'],QCS)}
### 11.10.5.8 Scorecard instruments adopted (QC-V12-J-001, -002, -003, -008)

**RCTCFE criteria and weights (V12).** Scores are on actual evidence; 12/10 is not awarded; a high score never overrides an open gate.

{tbl(['Criterion','Weight','V12 score /10','V11 score /10'],[[a[0],a[1],a[2],b[2]] for a,b in zip(d['rct_v12'],d['rct_v11'])])}
**Artifact scores (V12 / V11).** For the blueprint, QC-V12-J-008 applies the same scale to each Part.

{tbl(['Artifact','V12','V11'],[[a[0],a[1],b[1]] for a,b in zip(d['art_v12'],d['art_v11'])])}
**20-dimension engineering scorecard (weights from document 36; V12 scores).** "Unscored" means no production measurement; the normalised score uses the 69 scored weight points only.

{tbl(['Dimension','Weight','Owner','V12 score','Basis'],d['dim_v12'])}
**Release gates (V11; V8 identical in structure).**

{tbl(['Gate','Status','Evidence / blocker'],d['gate_v11'])}
### 11.10.5.9 Coding standard additions CS-V12-J-01…04

They extend Part 4.4a §4.4.5.1 (owner: Principal Engineer) and follow its MUST/SHOULD and waiver rules. The six chapter 35 controls (repository structure, frontend, Python/Django, SQL, review, CI) are already covered (Part 11.10a §11.10.3.9).

{tbl(['ID','Rule','Level','Check'],CSV12)}
### 11.10.5.10 Functional requirements and stories

| FR | Requirement | Epic | Wave | Source | Tests |
|---|---|---|---|---|---|
| FR-V12-J-001 | A090 computes and shows the RCTCFE score per release from criterion scores with evidence links; score is labelled "review input" and cannot change a gate | EP-21 | W4 | FSD 34 RCTCFE | TC-V12-J-126 |
| FR-V12-J-002 | A090 shows the 20-dimension scorecard; dimensions without measurement show "Unscored"; normalised score over scored weight; weights must total 100 | EP-21 | W4 | FSD 34; REC-16 | TC-V12-J-127 |
| FR-V12-J-003 | A090 shows the five gates (Source, Prototype, Documentation, Production, Optimization) with status and blockers, and blocks release while Production is not satisfied | EP-21 | W4 | FSD 34 gates | TC-V12-J-128 |
| FR-V12-J-004 | A090 holds the V12 acceptance register: requirement, priority, owner, specification status, prototype status, production status, canonical test and evidence; production status changes only with production evidence | EP-21 | W4 | FSD 34 register (233) | TC-V12-J-129; QC-V12-J-009 |
| FR-V12-J-005 | The combined preflight adds the groups Workflow scenario tests, Step tests, SKU entitlement acceptance, V12 acceptance register and Parity regression, and validates KPI evidence on its numeric domain | EP-21 | W4 | closure preflight; FSD 34 KPIs | TC-V12-J-121, -122 |
| FR-V12-J-006 | The RTM adds the levels SKU → workflow → step → test → task → release (release evidence matrix) | EP-21 | W4 | FSD 34 V3 | Part 6.6 generator; TC-V12-J-109 |

#### US-21-YJ01 Run the V12 workflow tests of a SKU as one parameterized suite

As the QA lead (R19), I want to run all scenario, step and acceptance tests of a SKU from the workflow registry, so that a SKU can be certified without writing tests per workflow. Story points: 8. Links: FR-V12-J-005, TASK-V12-J-001/002, QC-V12-J-011.

{gh("""
Feature: Parameterized V12 workflow tests
  Scenario: AC-21-YJ01-01 All scenario classes run for every workflow of the SKU
    Given SKU SM-SVC-07 with workflows WF01 to WF04 in the registry
    When the QA lead runs the suite for SM-SVC-07
    Then 36 scenario tests, 13 step tests and 4 AT01 tests are executed
    And each result carries its V12 ID and an evidence record

  Scenario: AC-21-YJ01-02 Missing EVAL suite blocks the AI step test
    Given the EVAL suite of SM-SVC-07-WF02 has not passed
    When the suite runs
    Then every AI step test of SM-SVC-07-WF02 reports Blocked with reason EVAL_GATE
    And the SKU is not test-complete
""")}
#### US-21-YJ02 See the RCTCFE and 20-dimension scorecards for a release

As the Product Owner, I want the evidence-based scorecards on the release record, so that reviewers see quality without any score overriding a gate. Story points: 5. Links: FR-V12-J-001/002, QC-V12-J-001/002.

{gh("""
Feature: Release scorecards
  Scenario: AC-21-YJ02-01 Weighted RCTCFE total
    Given criterion scores 9.0, 8.9, 8.8, 9.2, 7.6, 8.6, 7.2, 8.7 with weights 15, 15, 15, 15, 15, 10, 10, 5
    When the scorecard is computed
    Then the weighted total is 8.54

  Scenario: AC-21-YJ02-02 Unscored dimensions are not estimated
    Given 31 weight points have no production measurement
    When the 20-dimension scorecard is computed
    Then those dimensions show Unscored
    And the normalised score uses 69 weight points only
""")}
#### US-21-YJ03 Block a release while a gate is not satisfied

As the delivery owner, I want the five-gate status on A090, so that prototype or documentation passes cannot release the product. Story points: 3. Links: FR-V12-J-003, QC-V12-J-003.

{gh("""
Feature: Five-gate release status
  Scenario: AC-21-YJ03-01 Production gate open
    Given Source, Prototype and Documentation are Pass and Production is Not satisfied
    When the delivery owner requests go-live approval
    Then the request is refused with the blocker list of the Production gate
""")}
#### US-21-YJ04 Maintain the V12 acceptance register

As the Test Architect, I want each V12 requirement with its specification, prototype and production status and canonical test, so that production status only moves with production evidence. Story points: 5. Links: FR-V12-J-004, QC-V12-J-009.

{gh("""
Feature: V12 acceptance register
  Scenario: AC-21-YJ04-01 Prototype pass does not change production status
    Given requirement MOB-02 with prototype status Demonstrated
    When a prototype check result is attached
    Then the production status stays Production pending

  Scenario: AC-21-YJ04-02 Production evidence moves the status
    Given MOB-02-AT01 passed in staging with a reviewed evidence record
    When the reviewer approves the evidence
    Then the production status becomes Passed with the evidence link
""")}
#### US-21-YJ05 Reject invalid KPI evidence in the preflight

As the Head of Quality Engineering, I want the preflight to recompute KPI evidence on its numeric domain, so that an entered "Pass" cannot hide an invalid value. Story points: 3. Links: FR-V12-J-005, TC-V12-J-121.

{gh("""
Feature: KPI evidence validation
  Scenario Outline: AC-21-YJ05-01 Invalid values fail
    Given KPI evidence with unit <unit>, observed <observed>, numerator <n> and denominator <d>
    When the preflight validates it against target <op> <target>
    Then the KPI result is <result>
    Examples:
      | unit  | observed | n  | d   | op | target | result |
      | count | 0        |    |     | <= | 0      | Pass   |
      | count | -1       |    |     | <= | 0      | Fail   |
      | count | 0.5      |    |     | <= | 1      | Fail   |
      | ratio | 1        | 0  | 0   | >= | 1      | Fail   |
      | ratio | 1        | 1  | 2   | >= | 1      | Fail   |
      | ratio | 0.95     | 95 | 100 | >= | 0.95   | Pass   |
""")}
### 11.10.5.11 Development backlog additions

**SKU build tasks SM-SVC-01…39-BUILD (V12 IDs adopted).** V12 gives deliverable ("<domain> domain + four workflows + UI/adapter") and acceptance ("Foundation; approved DTO/schema/provider; all SM-SVC-## tests and entitlement sign-off") but says "estimate after contract". The panel adds owner, dependencies, acceptance IDs, estimate and release. Estimates use the step-class norms of §11.10.5.12.

{tbl(['Task','Service','Class','WF','Steps','Scenario tests','Owner','Dependencies','Acceptance IDs','Build pd L/C/H','Test pd L/C/H','Total pd L/C/H','Release and notes'],brows)}
**QA, QC and test-infrastructure tasks TASK-V12-J-001…014.**

{tbl(['Task','Deliverable','Owner','Dependencies','Acceptance','pd L / C / H'],qarows)}
Work items: 162 (Part 6.9a) + 39 + 14 = **215**. Each task has an owner, estimate, acceptance IDs and dependencies, as V12 chapter 35 requires.

### 11.10.5.12 Effort impact of the new backlog (recomputed)

**Basis of estimate.** Build effort per SKU = fixed SKU effort (catalogue entry, meter unit, domain model, migrations, Admin and portal screens, adapter shell) + per workflow packaging (DTO, registry entry, entitlement binding, docs: 0.25 / 0.5 / 0.75 pd) + Σ steps × step-class norm × reuse factor. Test effort per SKU = per workflow fixture pack covering all scenario and step tests (0.2 / 0.3 / 0.5 pd) + AT01 script (0.1 / 0.15 / 0.25 pd) + one entitlement test (0.15 / 0.25 / 0.4 pd); the class harnesses are in TASK-V12-J-001/002. [ASSUMPTION-922] [ASSUMPTION-923]

| Step class | New-build norm pd L / C / H | Basis |
|---|---|---|
| Evidence retrieval (ER) | 0.75 / 1.0 / 1.5 | Source registry check, provenance, rights |
| AI inference (AI) | 1.0 / 1.5 / 2.5 | Prompt, schema, guard, eval hook (datasets under R5) |
| Deterministic calculation (DC) | 0.5 / 0.75 / 1.25 | Decimal rules, golden fixtures |
| Deterministic domain logic (DL) | 0.5 / 0.75 / 1.25 | State rules, golden fixtures |
| Policy gate / human review (PG) | 0.25 / 0.5 / 0.75 | Reuses PDP and approval engine |
| Identity / reconciliation (IR) | 0.75 / 1.25 / 2.0 | Matching rules, review queue |
| External effect (EX) | 1.0 / 2.0 / 3.0 | Adapter port, outbox, reconciliation |
| Fixed per SKU, by class H / M / N | 1.0–2.5 / 3–8 / 6–16 | Low–high range; central 1.5 / 5 / 10 |
| Reuse factor on steps, H / M / N | 0.20 / 0.55 / 1.00 | Share of step build not already in Release 1/2 or in an advanced card |

**Build tasks by class (pd).**

{tbl(['Class','Meaning','SKUs','Low','Central','High'],clsrows)}
**Development (one-time) cost of the new backlog.** pd × ₹4,545 / ₹5,682 / ₹6,818 (Part 9.10 §9.10.6 blended rates; estimates). Outside the approved Ledger A (DEC-230) and the Phase-2 envelope; separately approvable (CONFLICT-922).

{tbl(['Package','pd low / central / high','₹ lakh low / central / high'],costrows)}
**Subscription and running (recurring) cost.** Shown separately, as required.

| Item | Monthly estimate | Basis |
|---|---|---|
| CI and nightly test compute for ≈ 2,300 additional tests (parameterized; parity suite on 2 apps × 4 viewports) | ₹0–2,500 | Within the existing CI line of Ledger B if self-hosted runners have spare capacity; otherwise hosted runner minutes (price verify, as of 27 Nov 2026) |
| Provider sandboxes for EX and ER steps (telephony, SMS/RCS, marketplace) | ₹0–4,000 | Most sandboxes are free tiers; telephony and SMS test numbers may charge (verify, as of 27 Nov 2026); only for SKUs approved under CR-V12-J-02 |
| Evaluation runs for 111 EVAL suites | Within DEC-008 AI ceilings | Gold-set runs on Tier 1a/1b are counted in the AI budget lines of Ledger B (DEC-231/DEC-422); no new line |

**Staffing and schedule impact.** CR-V12-J-01 central {pkgA[1]:.0f} pd equals about {pkgA[1]/18:.0f} person-months at 18 productive pd per month [ASSUMPTION-924]. With QA 1.0 FTE and the contract engineers already committed to Release 1/2 (DEC-228, DEC-416), it does not fit the Release 2 build window (Fri 2 Jul 2027) without extra capacity. Option: two contract engineers and one contract QA automation engineer for about {pkgA[1]/18/3:.0f} months from Release 1 go/no-go (Fri 4 Jun 2027); the Release 2 date of record stays unchanged only if CR-V12-J-01 is reduced to the QA infrastructure plus the SKUs sold first. CR-V12-J-02 central {pkgB[1]:.0f} pd belongs in W6 (Day ≈ 237–365) after a gate on Release 2 actuals.

**Single-count rule [RECOMMENDATION-924].** Groups R2–R5 may also estimate the build of the same services, workflows and AI steps. The coordinator keeps, per SKU, one build figure (the higher, never the sum); the QA infrastructure package (TASK-V12-J-001…014) is owned by this group only. The closure review-effort model (32.55 / 62.85 / 123.70 pd, Part 6.9b GAP-450) is not added again.

---

## 11.10.6 Conflicts and proposed resolutions

| Tag | Conflict | V12 | Blueprint / Founder decision | Proposed resolution | Status |
|---|---|---|---|---|---|
| CONFLICT-922 | Funding and staffing of the V12 backlog | 39 SKU build tasks and the full V12 test catalogue; "estimate after contract" | Ledger A approved budget (DEC-230), Option 2b staffing (DEC-228), Phase-2 envelope separate | Approve CR-V12-J-01 ({pkgA[0]:.0f} / {pkgA[1]:.0f} / {pkgA[2]:.0f} pd; ₹{lakh(pkgA[0],0):.1f} / {lakh(pkgA[1],1):.1f} / {lakh(pkgA[2],2):.1f} L) for Release 2 with extra contract capacity, or reduce it to the QA infrastructure plus the first SKUs to be sold; decide CR-V12-J-02 ({pkgB[1]:.0f} pd central) at the W6 gate. Until decided, the V12 tests are specified (Matched) and SKU build tasks are "Proposed" | Pending Founder decision |
| CONFLICT-923 | Growth critical RTO | KPI-32 ≤ 120 min, Blocking (DEC-V9-01 adopted) | DEC-158 (CONFLICT-462): RTO 4 h at pilot; 2 h binding only after Topology B and two passed drills; hosting DEC-421; running budget DEC-231/422 | Keep DEC-158 staging: KPI-32 is a review target until Topology B is funded, then blocking. Alternative: make it blocking at Release 2 and fund warm standby (running-cost delta to be priced by R4/R8) | Pending Founder decision |
| CONFLICT-924 | Data residency tests | CJ-TC-09: EU tenant data never written to IN region storage, and vice versa | Single region AWS Mumbai + Vercel + Supabase (DEC-421); TC-01-017 refuses non-approved regions | Test written region-conditional: in the current topology it asserts that EU-resident tenants cannot be onboarded (refusal); the dual-region assertion activates only if the Founder approves an EU region | Pending Founder decision |

No conflict with a safety invariant was found: the V12 EFFECT and APPROVAL scenarios already require approval before any effect, and the panel tests assert L1 for consequential actions of SM-SVC-26, 28, 31, 37, 38 and 39 (R-8). The scope questions of those services (voice, agentic commerce, pricing) are owned by Group R2.

---

## 11.10.7 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-680 | V12 test IDs are canonical (workflow scenarios, step tests, AT01, ENT-AT01, AIX-TC, CJ-TC, MT-TC, MOB-AT, OPT-TC, XS, UAT-E2E-01, EXC); the blueprint executes them through TC-V12-J classes or canonical rows and keeps earlier TCs as mappings | Customer revision V12 (28 Nov 2026) | +{C['total_new']:,} executable tests; test total 6,472 |
| DEC-681 | V12 KPI-01…35 are aliases of OKPI-01…35; the V9 reconciliation column is adopted (KPI-13 gold-set 100% schema, KPI-14 ≥ 95%, KPI-15 F1 ≥ 0.90 with recall reported) except KPI-32 | Customer revision V12 (28 Nov 2026) | Amends Part 4.4a OKPI notes; no ID change |
| DEC-682 | Prototype evidence (V3–V12 checks) is recorded but never counts as production acceptance; the checks become production parity regression classes TC-V12-J-101…114 | Customer revision V12 (28 Nov 2026) | 954 prototype checks mapped to 14 classes |
| DEC-683 | RCTCFE, the 20-dimension scorecard and artifact scores are adopted as release review instruments; they never override a gate; unmeasured dimensions stay unscored | Customer revision V12 (28 Nov 2026) | QC-V12-J-001/002/008; FR-V12-J-001/002 |
| DEC-684 | Workflow test completeness gate (QC-V12-J-011) is blocking per SKU before activation | Customer revision V12 (28 Nov 2026) | TC-V12-J-129 |
| DEC-685 | The chapter 40 dispositions of the archived 589 test IDs, 245 QCs and 162 work items are closed by the existing blueprint mappings (Parts 6.8, 6.9); semantic approval stays under FR-ENH-H-006 | Customer revision V12 (28 Nov 2026) | No change to Parts 6.8/6.9 |
| DEC-686 | The 39 SKU build tasks and TASK-V12-J-001…014 are added to the backlog with the estimates of §11.10.5.12; funding as CR-V12-J-01 (Release 2 candidate) and CR-V12-J-02 (W6) | Pending Founder decision | CONFLICT-922 |
| DEC-687 | KPI-32 growth RTO stays staged per DEC-158 (review target until Topology B) | Pending Founder decision | CONFLICT-923 |
| DEC-688 | CJ-TC-09 runs region-conditional; EU-resident tenants are refused while a single region is in force | Pending Founder decision | CONFLICT-924 |
| DEC-689 | Coding standards CS-V12-J-01…04 are added to Part 4.4a §4.4.5.1; chapter 35 controls confirmed | Customer revision V12 (28 Nov 2026) | QC-V12-J-015; TASK-V12-J-010 |
| DEC-690 | Evidence records gain tenant fixture, fixture version, input and environment fields; status of every V12 test is "Not run" until executed | Customer revision V12 (28 Nov 2026) | QC-V12-J-007; TC-V12-J-125 |
| DEC-691 | 17 quality controls QC-V12-J-001…017 are added to the QC register (245 → 262) | Customer revision V12 (28 Nov 2026) | Part 6.9b register extended |

---

## 11.10.8 Expert persona review

| Persona | Finding | Change made |
|---|---|---|
| Head of Quality Engineering | V12 piles up prototype passes (954 checks) next to "Not run" production tests; risk that a reader counts them as acceptance | DEC-682, QC-V12-J-007 and R-3; parity classes re-run every check on the production build |
| Head of Quality Engineering | KPI evidence status was trusted as entered in the blueprint preflight | TC-V12-J-121 and FR-V12-J-005 recompute on the numeric domain |
| Test Architect | 1,342 scenarios are 10 templates; writing them per workflow would create 1,342 copies to maintain | Ten parameterized classes, one fixture pack per workflow, CS-V12-J-03 forbids copies |
| Test Architect | 9 workflows route approval or legal review without an APPROVAL scenario | TC-V12-J-201…209 and QC-V12-J-017 |
| Test Architect | AI step tests have no meaning without the EVAL suite gate | R-6 and QC-V12-J-011; TASK-V12-J-003 |
| Principal Engineer | Chapter 35 controls are already stricter in Part 4.4a; the real risk is porting prototype layering and demo identity | CS-V12-J-01/02 enforced in CI (TC-V12-J-123/124) |
| Agile Delivery Lead | V12 backlog lacks estimates; 39 SKU tasks would otherwise enter sprints unsized | Step-class estimation model; two change requests; single-count rule with R2–R5 |
| Agile Delivery Lead | The new work does not fit Release 2 with current capacity | Staffing option and reduced CR-V12-J-01 offered (CONFLICT-922) |

---

## 11.10.9 Tags register

| Tag | Type | Statement | Status |
|---|---|---|---|
| ASSUMPTION-922 | Assumption | Step-class effort norms and per-SKU fixed effort of §11.10.5.12 | Validate on the pilot SKU SM-SVC-01 actuals |
| ASSUMPTION-923 | Assumption | SKU overlap classes H/M/N and reuse factors 0.20 / 0.55 / 1.00 (Part 11.10b §11.10.4.3) | Validate with Group R2 service mapping |
| ASSUMPTION-924 | Assumption | 18 productive pd per person-month; blended rates ₹4,545 / ₹5,682 / ₹6,818 per pd (Part 9.10) | Open |
| ASSUMPTION-925 | Assumption | Status before of non-curated V12 acceptance tests and prototype checks was proposed by TF-IDF similarity (≥ 0.45 / ≥ 0.17; ≥ 0.55 / ≥ 0.20) and reviewed by sampling; the 40 AIX/CJ tests were curated individually | Open; semantic approval under FR-ENH-H-006 |
| GAP-922 | Gap | V12 SKU build tasks have no estimates ("estimate after contract") | Closed by §11.10.5.11–12 |
| GAP-923 | Gap | V12 scenario fixtures are boilerplate without data values | Closed by class fixtures (§11.10.5.2) and family fixtures (§11.10.5.3) |
| GAP-924 | Gap | 9 approval-routed workflows lack an APPROVAL scenario | Closed by TC-V12-J-201…209 |
| GAP-925 | Gap | Every V12 test is "Not run"; only prototype evidence exists | Open until execution; DEC-682 |
| GAP-926 | Gap | EVAL suite datasets (size, labels, languages) are not supplied | Owned by Group R5; gate wiring here (TASK-V12-J-003) |
| GAP-927 | Gap | Blueprint preflight did not define the numeric domain of KPI evidence | Closed by TC-V12-J-121 |
| CONFLICT-922 | Conflict | V12 backlog funding and staffing vs DEC-230/DEC-228 | Pending Founder decision |
| CONFLICT-923 | Conflict | KPI-32 blocking 120 min vs DEC-158 staging | Pending Founder decision |
| CONFLICT-924 | Conflict | CJ-TC-09 dual-region residency vs DEC-421 single region | Pending Founder decision |
| RECOMMENDATION-922 | Recommendation | Release 1 runs the legacy suite; V12 suites start with Release 2 SKUs | Proposed |
| RECOMMENDATION-923 | Recommendation | Pilot the harness on SM-SVC-01 (4 workflows) before scaling to 156 | Proposed |
| RECOMMENDATION-924 | Recommendation | Single-count rule for build estimates across R2–R5 and J | Proposed |
| RECOMMENDATION-925 | Recommendation | Treat RCTCFE and 20-dimension scores as review inputs only | Adopted (DEC-683) |

**Inconsistencies found in earlier parts (reported, not edited).** (1) Part 6.10 states 245 QCs at 100% traced, while Part 6.9a lists 54 QCs with section-only references (GAP-513); chapter 40 re-opens them as "evidence pending" — consistent with the blueprint once evidence exists, no edit needed. (2) The blueprint business KPIs KPI-01…31 (Part 1) and the V12 KPI-01…35 share a prefix; Part 4.4a already renamed the source KPIs to OKPI, which this part keeps. (3) The V12 brief quotes 4,156 tests; the TC rows indexable in `Part-*.md` number 4,077 (the rest are written as ranges or in other row formats); the count of record stays 4,156.

---

## 11.10.10 Quality gate

| # | Item | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Each class, QC, standard, FR, story and task cites its V12 source |
| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | 4 ASSUMPTION, 6 GAP, 3 CONFLICT, 4 RECOMMENDATION in range 922…939 |
| 3 | IDs unique and consistent with earlier parts | Pass | DEC-680…691; TC-V12-J, QC-V12-J, CS-V12-J, FR-V12-J, US-21-YJ, TASK-V12-J; V12 IDs kept |
| 4 | No story lacks AC and no requirement lacks a test | Pass | 5 stories with Gherkin; 6 FRs with tests; 233/233 register tests adopted |
| 5 | Negative, edge, security, accessibility | Pass | Classes 002–010, 015–017, 103, 108, 121, 125 |
| 6 | Agents complete | N/A | No agent added |
| 7 | Time-sensitive facts flagged | Pass | Tool versions, sandbox and runner prices, tax rates flagged "verify (as of 27 Nov 2026)" |
| 8 | No restricted data to free tiers | Pass | R-9 and TC-V12-J-012 |
| 9 | Consistent with earlier parts | Pass | Budgets untouched; additions costed outside DEC-230/231 in separate one-time and recurring tables |

**Status: Part 11 Batch 11.10c complete. {C['total_new']:,} new executable tests (4,156 → {4156+C['total_new']:,}), 17 QCs (245 → 262), 4 coding standards, 6 FRs, 5 stories, 53 work items (162 → 215); new-backlog effort {grand[0]:.0f} / {grand[1]:.0f} / {grand[2]:.0f} pd (₹{lakh(grand[0],0):.1f} / {lakh(grand[1],1):.1f} / {lakh(grand[2],2):.1f} lakh), pending Founder decision.**
'''
open(OUT,'w').write(H); print(OUT,len(H),b_tot,qa_tot,grand,pkgA,pkgB,len(canon))
