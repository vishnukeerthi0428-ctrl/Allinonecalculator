"""Group J (R9) mapping: status before/after, blueprint location, actions and new IDs for every
aspect; effort model for the new backlog; writes final/coverage_v12/J_coverage.csv, j_tables.json, j_nums.json."""
import sys,os,re,json,csv
from collections import Counter,defaultdict
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from j_sim import Index
d=json.load(open(os.path.join(HERE,'j_items.json')))
BP='/home/user/Allinonecalculator/blueprint/'
ix=Index()
A=[]   # aspects
def add(doc,chap,sec,aid,summ,sb,loc,act,new,sa='Matched'):
    A.append(dict(doc=doc,chapter=chap,section=sec,aspect_id=aid,aspect_summary=summ,status_before=sb,blueprint_location=loc,action=act,new_ids=new,status_after=sa))
T={}; N={}
def md(hdr,rows):
    s='| '+' | '.join(hdr)+' |\n|'+'---|'*len(hdr)+'\n'
    for r in rows: s+='| '+' | '.join(str(x).replace('|','/').replace('\n',' ') for x in r)+' |\n'
    return s
def simstat(text,hi=0.55,lo=0.30,k=3):
    tops=ix.top(text,k); s=tops[0][0] if tops else 0
    st='Covered' if s>=hi else ('Partially covered' if s>=lo else 'Not covered')
    return st,tops
def refs(tops,minscore=0.17): return ', '.join(i for s,i in tops if s>=minscore) or '—'
KW=[(r'router|routing|tier|escalation','Part 7.3 model routing (DEC-418 tiers)'),(r'cach','TC-ENH-I-010; TC-AI-AG003-002'),(r'budget|cost anomal|quota','TC-NFR-014; Part 7.3 budgets'),
(r'deterministic','TC-17-057; AI-01 rule-first (Part 7.3)'),(r'embedding|rag|retriev','Part 7.1 RAG; TC-20-096'),(r'batch','Part 7.3 batching'),(r'loop|termination','TC-AI-AG015-030 kill switch and caps'),
(r'authori[sz]ation|isolation|rls|tenant|company|organi[sz]ation|portfolio','NFR-001/002; TC-ENH-E-001; TC-ENH-G-001/002'),(r'mfa|step-up|credential|session','Part 4.1 identity controls; TC-01-025'),
(r'audit','Part 2.4 audit; NFR-024'),(r'injection|tool permission|exfil','Part 6.4 injection cases; TC-ADV-X1-008'),(r'loss prevention|dlp|file ingestion','Part 4.1 data protection'),(r'browser|csp|ssrf|egress','Part 4.1 web controls'),
(r'supply-chain|sbom|dependency','Part 4.3 PL gates (SBOM, scans)'),(r'slo|sli|error budget|availability','Part 4.3 SLOs; NFR-053/054'),(r'circuit|bulkhead|backpressure|degradation','Part 3.1 resilience patterns; NFR-016'),
(r'checkpoint|idempot|reconcil|retry|dead-letter|replay','TC-ENH-G-003; TC-ENH-K-071'),(r'probe|synthetic','Part 4.3 synthetic monitoring'),(r'canary|rollback','Part 4.3 §4.37 release and rollback'),(r'migration','CS-MIG-01; Part 4.3 §4.37.2'),
(r'chaos|fault','TC-ENH-K-071'),(r'backup|restore|recovery','NFR-056/057; Part 4.4b DR'),(r'workflow|dag|step|orchestrat|simulation|approval|mandate|cancel|template','Part 2.2 WF engine; TC-ENH-G-010; TC-18-111'),
(r'page|seo|crawl|website|landing|trust|resource|directory|comparison|sandbox|assessment|report','EP-19 website TCs (TC-19-*)'),(r'onboard|wizard|draft|saved','US-2004; TC-20-*'),(r'pric|quote|bundle|roi|cost of ownership','EP-13 quote TCs; TC-AI-AG014-003'),
(r'health|renewal|usage|consumption|value report|cancellation|plan change|success|adoption','EP-16 retention TCs; AG-038'),(r'help|support|escalat|notification|feedback|csat|nps|status|error|tour','AG-031; EP-16/EP-20 TCs'),
(r'mobile|touch|responsive|offline|pwa|navigation|filter|record|table','Part 2.5/2.7 responsive rules; NFR-088'),(r'currency|financial','TC-19-057; BRL-FIN'),(r'accessib','NFR-088/089'),(r'selector|switch|context','TC-FLT-011; MT scope selector'),
(r'brand|division|offering|master|customer type|lifecycle','Part 2.6 business configuration; US-2004')]
def kwanchor(text):
    for rx,loc in KW:
        if re.search(rx,text,re.I): return loc
    return None
# ---------------- SKU classes ----------------
SKU={}
H=dict(zip(range(1,26),['EP-05','EP-05','EP-06','EP-06','EP-07','EP-08','EP-10','EP-08','EP-08/EP-10','EP-09','EP-11','EP-11','EP-11','EP-12','EP-12/EP-19','EP-09/EP-12','EP-13','EP-13','EP-14','EP-14','EP-15','EP-16','EP-16','EP-15/EP-17','EP-02']))
M={27:('EP-11','AG-049, AG-050'),29:('EP-06','AG-061'),30:('EP-12','AG-052'),32:('EP-16','AG-069'),33:('EP-16','AG-031'),35:('EP-11','—'),36:('EP-17','AG-046, AG-070'),37:('EP-13','AG-048, AG-066 (recommend only; AI never sets prices)'),38:('EP-08','—'),39:('EP-14','AU-044; OrganicSpec payable ledger')}
NN={26:'EP-08',28:'EP-14',31:'EP-14',34:'EP-20'}
for r in d['sku']:
    n=int(r[0][-2:])
    if n in H: cls,ep,anc='H',H[n],'Release 1/2 capability'
    elif n in M: cls,ep,anc='M',M[n][0],M[n][1]
    else: cls,ep,anc='N',NN[n],'none'
    SKU[r[0]]=dict(name=r[1],family=r[2],bundle=r[3],meter=r[6],cls=cls,ep=ep,anchor=anc)
CLSNAME={'H':'High overlap','M':'Partial overlap','N':'New domain'}
# ---------------- workflow scenario tests ----------------
CAT=['POS','INPUT','SCOPE','ENT','DUP','QUALITY','BUDGET','RECOVERY','APPROVAL','EFFECT']
CATTC={c:'TC-V12-J-%03d'%(k+1) for k,c in enumerate(CAT)}
ANCH={'POS':'epic functional TCs','INPUT':'TC-ENH-K-051, TC-ENH-G-006, TC-03-034','SCOPE':'TC-ENH-G-002, TC-ENH-E-001, TC-ENH-E-006','ENT':'TC-16-062, TC-20-054, TC-20-086','DUP':'TC-ENH-G-003, TC-ENH-J-028, TC-AU-AU020-001','QUALITY':'TC-AI-AG011-002, TC-ADV-X1-057, TC-04-038','BUDGET':'TC-NFR-014, TC-ENH-A-045, TC-03-024','RECOVERY':'TC-ENH-K-071, TC-01-071, TC-16-038','APPROVAL':'TC-ENH-G-004, TC-18-111, TC-15-020','EFFECT':'TC-04-003, TC-ENH-A-022, TC-ENH-G-016'}
STEPC=['Evidence retrieval','AI inference','Deterministic calculation','Deterministic domain logic','Policy gate / human review','Deterministic identity / reconciliation','External effect']
STEPTC={c:'TC-V12-J-%03d'%(k+11) for k,c in enumerate(STEPC)}
STEPANCH={'Evidence retrieval':'TC-05-021, TC-AI-AG004-003, TC-ENH-G-007','AI inference':'TC-ENH-G-006, TC-AI-AG020-002, TC-ADV-X1-008','Deterministic calculation':'TC-15-081, TC-ENH-G-011','Deterministic domain logic':'TC-17-057, TC-ENH-F-008','Policy gate / human review':'TC-NFR-095, TC-ENH-G-008, TC-02-015','Deterministic identity / reconciliation':'TC-ADV-X1-077, TC-06-032, TC-15-041','External effect':'TC-ENH-G-008, TC-04-003, TC-ENH-G-016'}
wf=defaultdict(dict); 
for r in d['wf_tests']:
    w=r[1]; c=r[0].split('-TC-')[1]; wf[w][c]=r
    sk=w[:9]; cls=SKU[sk]['cls']
    sb='Partially covered' if cls=='H' else 'Not covered'
    summ=(f'{c}: {r[2]} → {r[3]}')
    add('FSD V12','33','V5 optimization requirements and controls (1,342 workflow scenarios)',r[0],summ,sb,
        f"{SKU[sk]['ep']}; generic class {ANCH[c]}" if cls=='H' else f"No {sk} workflow in blueprint; generic class {ANCH[c]}",
        f'Adopt V12 ID; instantiate parameterized class {CATTC[c]} for {w}',CATTC[c])
steps=defaultdict(list)
for r in d['steps']:
    w=r[0].split('-STEP')[0]; steps[w].append(r); sk=w[:9]; cls=SKU[sk]['cls']
    sb='Partially covered' if cls=='H' else 'Not covered'
    add('FSD V12','33','33.3 Step-level tests (517)',r[0],f'{r[1]}: {r[2]} — {r[3]}',sb,
        f"{SKU[sk]['ep']}; {STEPANCH[r[1]]}",f'Adopt V12 ID; instantiate step class {STEPTC[r[1]]}',STEPTC[r[1]])
ev={r[0].replace('EVAL-',''):r for r in d['eval']}
for r in d['eval']:
    w=r[0].replace('EVAL-',''); sk=r[2]
    add('FSD V12','16 (bound by 33.3)','16.4 Evaluation sets (gate for AI-inference step tests)',r[0],f'EVAL suite for {w} ({r[1]}); {r[3]} AI step(s); {r[4]}; languages {r[5]}',
        'Partially covered' if SKU[sk]['cls']=='H' else 'Not covered','Part 6.4 AI evaluation; Part 7.3 eval gates; TC-04-032',
        'Bind every AI-inference step test of the workflow to this suite; suite pass is a precondition of TC-V12-J-012','TC-V12-J-012; QC-V12-J-011')
# approval gap: steps mention approval/review but no APPROVAL scenario
apr_gap=[]
for w in sorted(steps):
    if 'APPROVAL' in wf[w]: continue
    acts='; '.join(s[2] for s in steps[w])
    at=[x for x in d['wb_at'] if x[2]==w][0]
    if re.search(r'approv|submission|legal review|route review|freeze',acts+' '+at[6],re.I) and any(s[1]=='Policy gate / human review' for s in steps[w]):
        apr_gap.append(w)
APRTC={w:'TC-V12-J-%03d'%(201+k) for k,w in enumerate(apr_gap)}
N['apr_gap']=len(apr_gap)
# workbook acceptance tests
for r in d['wb_at']:
    ent=('ENT' in r[0])
    sk=r[1]; cls=SKU[sk]['cls']
    add('Workbook 39 Services 156 Workflows','Acceptance_Tests','Service & workflow acceptance' ,r[0],
        (f'{r[3]}: {r[6]} → {r[7]}' if not ent else f'Single-SKU entitlement: {r[6]} → {r[7]}'),
        'Partially covered' if (cls=='H' and not ent) else ('Partially covered' if ent else 'Not covered'),
        ('Part 6.1 §6.1.13 UAT packs; '+SKU[sk]['ep']) if not ent else 'TC-16-062, TC-20-054 (plan entitlements; no per-SKU purchase)',
        'Adopt as workflow UAT acceptance; KPI target recorded' if not ent else 'Adopt as SKU entitlement acceptance; sign-off before SKU sale (QC-V12-J-012)',
        'TC-V12-J-018' if not ent else 'TC-V12-J-019')
# ---------------- 233 register acceptance ----------------
reg={r[0]:r for r in d['reqreg']}
aix={r[1]:r for r in d['aix_cj']}
CUR={'AIX-TC-01':('Partially covered','CS-AI-01 (gateway only); TC-ENH-B-036'),'AIX-TC-02':('Partially covered','TC-ADV-X1-089; Part 7.3 model registry'),
'AIX-TC-03':('Partially covered','TC-ADV-X2-016; DEC-418 tier order'),'AIX-TC-04':('Partially covered','TC-04-032; TC-AU-AU001-004'),
'AIX-TC-05':('Partially covered','Part 6.4 agent eval gates (per agent, not per workflow)'),'AIX-TC-06':('Covered','TC-04-032; TC-AU-AU006-003'),
'AIX-TC-07':('Partially covered','TC-ADV-X1-018; TC-AI-AG002-001'),'AIX-TC-08':('Partially covered','Part 6.4 injection cases (no AI-INJ-01…12 set)'),
'AIX-TC-09':('Covered','TC-AI-AG013-009'),'AIX-TC-10':('Not covered','—'),'AIX-TC-11':('Covered','TC-04-038; TC-17-082'),
'AIX-TC-12':('Covered','TC-ENH-F-019; TC-AU-AU042-003'),'AIX-TC-13':('Covered','TC-AI-AG015-030; TC-NFR-014'),'AIX-TC-14':('Partially covered','KPI-24 cost per accepted result (Part 7.3)'),
'AIX-TC-15':('Covered','TC-ENH-I-010; TC-AU-AU030-003'),'AIX-TC-16':('Partially covered','TC-ENH-A-044 (20 concurrent runs; no noisy-tenant p95 assertion)'),
'AIX-TC-17':('Partially covered','AU-044 integration procurement gate'),'AIX-TC-18':('Partially covered','TC-04-050; TC-ADV-X1-064 (no rollback option assertion)'),
'AIX-TC-19':('Partially covered','TC-ADV-X1-020 (fairness slice, not locale slice)'),'AIX-TC-20':('Partially covered','TC-AI-AG015-030 kill switch (no one-cycle timing)'),
'CJ-TC-01':('Covered','TC-ENH-A-030; TC-03-014'),'CJ-TC-02':('Partially covered','TC-03-035 PDP decisions (not the 13-case table)'),'CJ-TC-03':('Partially covered','TC-AU-AU030-002; TC-13-055'),
'CJ-TC-04':('Partially covered','TC-ADV-X2-071; TC-NFR-095'),'CJ-TC-05':('Covered','TC-ENH-G-008; TC-14-037'),'CJ-TC-06':('Not covered','— (no India DLT registry check)'),
'CJ-TC-07':('Partially covered','TC-03-073; TC-AU-AU011-004 (no per-pack due date)'),'CJ-TC-08':('Partially covered','TC-ADV-X3-018; Part 4.1 incident response'),
'CJ-TC-09':('Conflict','TC-01-017 (single approved region, DEC-421)'),'CJ-TC-10':('Covered','TC-ENH-G-045; DEC-030 no outreach to minors'),
'CJ-TC-11':('Covered','TC-NFR-076; TC-ENH-E-019'),'CJ-TC-12':('Partially covered','TC-ALN-A-046 (DEC-263); W29/W30'),'CJ-TC-13':('Partially covered','TC-ADV-X1-075'),
'CJ-TC-14':('Partially covered','TC-12-071; BRL-AI (AI never decides alone)'),'CJ-TC-15':('Not covered','—'),'CJ-TC-16':('Covered','TC-15-022; TC-02-002'),
'CJ-TC-17':('Not covered','—'),'CJ-TC-18':('Partially covered','TC-ADV-X2-071 (consent version, not notice version)'),'CJ-TC-19':('Partially covered','TC-03-014; TC-ENH-A-030'),
'CJ-TC-20':('Partially covered','Fail-closed PDP default (NFR-016); no unreviewed-rule case')}
ACC=[]  # rows for register table
def okpi_note(i): return ''
for rid,r in reg.items():
    fam=re.sub(r'-?\d+$','',rid)
    if fam in('AIX','CJ-R'):
        tid=[x for x in aix.values() if x[1]==rid][0][0]; acc=aix[rid][2]; title=r[2]
        sb,loc=CUR[tid]
    else:
        tid=r[5].split(';')[0].strip()
        a=d['acc'].get(tid,{}); acc=a.get('acc',''); title=r[2]
        sb,tops=simstat(title+' '+a.get('req','')+' '+acc,0.45,0.17)
        loc=refs(tops)
        ka=kwanchor(title+' '+a.get('req',''))
        if ka:
            loc=ka+('; candidates '+loc if loc!='—' else '')
            if sb=='Not covered': sb='Partially covered'
    sa='Pending Founder decision' if sb=='Conflict' else 'Matched'
    act={'Covered':'Adopt V12 ID as alias of the listed blueprint TCs; no new assertion','Partially covered':'Adopt V12 ID; add the missing assertion as a canonical test row (§11.10.5.3)','Not covered':'Adopt V12 ID; new canonical test row (§11.10.5.3)','Conflict':'Test written region-conditional; CONFLICT-924'}[sb]
    add('FSD V12','34 (register) / 33, 05–36 (acceptance text)','V8 requirement status register (233)',tid,f'{rid} {title} [{r[1]}; {r[3]}]: {acc}',sb,loc,act,tid+(' (canonical)' if sb!='Covered' else ' (alias)'),sa)
    ACC.append([tid,rid,r[1],title,r[3],acc,sb,loc,sa])
T['acc_register']=ACC
# ---------------- XS, E2E, EXC, REC ----------------
for r in d['xs']:
    sb,tops=simstat(' '.join(r[1:]),0.6,0.3)
    add('FSD V12','33','V9 Release scenarios XS-01…10',r[0],f'{r[1]}: {r[2]} → {r[3]}',sb,refs(tops),'Adopt XS ID as alias of UX-QC/TC-ENH-J scenario' if sb=='Covered' else 'Adopt; new row',r[0]+' (alias)')
    T.setdefault('xs',[]).append([r[0],r[1],r[2],r[3],sb,refs(tops)])
E2E=[]
for src,key in [('V10 Source-derived lifecycle event sequence','v10_events'),('V9 UAT-E2E-01 Enquiry to verified payment','e2e_events')]:
    for r in d[key]:
        sb,tops=simstat(' '.join(r),0.55,0.30)
        aid=('V10-' if key=='v10_events' else 'UAT-E2E-01/')+r[0]
        add('FSD V12','33',src,aid,f'{r[1]} ({r[2]}, {r[3]}) → {r[4]}',sb,refs(tops),'Step of TC-V12-J-020 (UAT-E2E-01 relationship ledger journey)','TC-V12-J-020')
        if key=='e2e_events': E2E.append([r[0],r[1],r[3],r[4],sb,refs(tops)])
T['e2e']=E2E
for k,r in enumerate(d['exc']):
    sb,tops=simstat(' '.join(r),0.55,0.30)
    add('FSD V12','33','UAT-E2E-01 automation exceptions',r[0],f'{r[1]}: {r[2]} Hold: {r[3]}',sb,refs(tops),'New canonical exception test','TC-V12-J-%03d'%(21+k))
    T.setdefault('exc',[]).append([r[0],r[1],r[2],r[3],sb,refs(tops),'TC-V12-J-%03d'%(21+k)])
for r in d['rec33']+d['rec34']+d['rec35']:
    rid=r[0].split(' ')[0]
    m={'REC-19':('Partially covered','Part 6.8 (799-test mapping); Part 6.10 closure','QC-V12-J-005; TASK-V12-J-009'),'REC-28':('Partially covered','TC-ENH-A-044; WF-02/WF-10','TC-V12-J-020; QC-V12-J-006'),
       'REC-16':('Not covered','—','QC-V12-J-002'),'REC-20':('Covered','Part 6.9a §6.9.4.5 (162 items, PD L/B/H, predecessors; DAG valid)','— (confirmed)')}[rid]
    add('FSD V12',{'REC-19':'33','REC-28':'33','REC-16':'34','REC-20':'35'}[rid],'V10 Historical reconciliation controls',rid,f'{r[0]}: {r[1]} Acceptance: {r[2]}',m[0],m[1],'Adopt as quality control' if m[0]!='Covered' else 'Confirm',m[2])
    T.setdefault('rec',[]).append([r[0],r[1],r[2],m[0],m[1],m[2]])
# ---------------- prototype evidence ----------------
THEMES=[('TC-V12-J-105','No runtime or page errors',r'runtime error|js error|page error|no .*errors'),
('TC-V12-J-104','Localisation, RTL and translation',r'arabic|hindi|rtl|ltr|translat|locale|language|german|french|localisation'),
('TC-V12-J-103','Accessibility (axe, keyboard, focus, ARIA)',r'axe|aria|keyboard|focus|screen.?reader|accessib|wcag|modal'),
('TC-V12-J-106','Consent, cookies and privacy requests',r'cookie|consent|dsar|erasure|legal hold|opt-?in|opt-?out|privacy|withdraw'),
('TC-V12-J-108','Security input handling and identity controls',r'html in|injection|exfiltrat|invisible char|sso|api key|byok|siem|https|secret|xss|password|mfa|session'),
('TC-V12-J-111','Trust, transparency and AI disclosure',r'trust|status page|transparen|ai-generated|disclos|synthetic|certif|not measured'),
('TC-V12-J-107','Approval, maker-checker and run lifecycle',r'approv|reviewer|self-approve|\brun|held|reconcil|complete|gateway|preflight|\bhold|dispatch'),
('TC-V12-J-110','Commerce, entitlement, metering and currency',r'usage|units?\b|currency|invoice|plan|subscription|entitle|price|bundle|quote|billing|meter|checkout|payment'),
('TC-V12-J-109','Catalogue parity and counts',r'\b39\b|\b156\b|\b517\b|parity|inventory|count|catalog|services|workflows'),
('TC-V12-J-112','Role, persona and scope switching',r'persona|role|scope|switch|tenant|company|portfolio|audience|owned'),
('TC-V12-J-114','Cross-device handoff and session continuity',r'cross-device|handoff|import|export|transfer|reload|persist'),
('TC-V12-J-113','Forms, registration and validation',r'registration|form|wizard|invalid|required|field|validation|reject'),
('TC-V12-J-102','Responsive layout and navigation',r'overflow|width|\b390\b|menu|\bnav|bottom|viewport'),
('TC-V12-J-101','Route and screen inventory renders',r'.')]
THEME_NAME={t:n for t,n,_ in THEMES}
def theme(text):
    for t,n,rx in THEMES:
        if re.search(rx,text,re.I): return t
    return 'TC-V12-J-101'
PROTO=[]
def proto(src,sec,aid,text,res):
    t=theme(text); sb,tops=simstat(text,0.55,0.20)
    add('FSD V12',src,sec,aid,f'{text} [prototype result: {res}]',sb,refs(tops),f'Adopt as production parity regression check in class {t} ({THEME_NAME[t]}); prototype result is not production acceptance (DEC-682)',t)
    PROTO.append(dict(src=sec,id=aid,text=text,theme=t,sb=sb,refs=refs(tops)))
for r in d['v12_ent']: proto('33','V12 Verification evidence (enterprise W37–W41)',r[0],f'{r[1]}: {r[2]}',r[3])
for r in d['v12_qa']: proto('33','V12 Verification evidence',r[0],f'{r[1]}: {r[2]}',r[3])
for k,r in enumerate(d['v12_loc'],1): proto('33','V12 Localisation audit','V12-LOC-%02d'%k,f'Localisation audit {r[0]}: violations {r[1]}, overflow {r[2]}, direction {r[3]}','Pass')
for r in d['v11_qa']: proto('33','V11 Verification evidence',r[0],f'{r[1]}: {r[2]}',r[3])
for k,r in enumerate(d['v10_tpe'],1): proto('33','V10 Targeted prototype test evidence','V10-TPE-%02d'%k,f'{r[0]}: {r[1]}',r[2])
for r in d['v9_qa']: proto('33','V9 prototype verification (75 checks)',r[0],f'{r[1]}: {r[2]}',r[3])
for k,r in enumerate(d['v8_axe'],1): proto('33','V8 Verification evidence (axe-core)','V8-AXE-%02d'%k,f'axe-core WCAG 2.1 A/AA on {r[0]} ({r[1]}): {r[2]}','see text')
for k,r in enumerate(d['v8_evid'],1): proto('33','V8 Verification evidence summary','V8-EVD-%02d'%k,f'{r[0]}',r[1])
for r in d['v8_qa']: proto('33','33.2 V8 prototype verification',r[0],f'{r[1]}: {r[2]}',r[3])
for k,r in enumerate(d['v7_groups'],1): proto('34','V7 Verification test groups','V7-GRP-%02d'%k,f'{r[0]}: {r[1]}',r[2])
for r in d['v7_qa']: proto('34','V7 targeted browser check register',r[0],r[1],r[2])
for k,r in enumerate(d['v6_checks'],1): proto('34','V6 browser verification','V6-CHK-%02d'%k,r[0],r[1])
for k,r in enumerate(d['v5_checks'],1): proto('34','V5 browser regression evidence','V5-CHK-%02d'%k,f'{r[0]}: {r[2]}',r[1])
for r in d['v3_qa']: proto('34','Historical V3 QA results',r[0],r[1],'Passed (historical)')
for k,r in enumerate(d['v4_checks'],1): proto('34','V4 targeted browser acceptance record','V4-CHK-%02d'%k,f'{r[0]} = {r[1]}',r[2])
T['proto']=PROTO
# ---------------- ch34 scorecards / KPIs / gates ----------------
def sc(key,sec,qc,prefix):
    for k,r in enumerate(d[key],1):
        add('FSD V12','34',sec,f'{prefix}-%02d'%k,' · '.join(r),'Not covered','Part 9.3 final quality report (no RCTCFE rubric); Part 6.9b QC layers','Adopt as review instrument; never overrides an open gate',qc)
sc('rct_v12','V12 RCTCFE evaluation','QC-V12-J-001','RCT-V12'); sc('art_v12','V12 artifact scores','QC-V12-J-008','ART-V12')
sc('dim_v12','V12 20-dimension scorecard','QC-V12-J-002','DIM-V12'); sc('rct_v11','V11 RCTCFE evaluation','QC-V12-J-001','RCT-V11')
sc('art_v11','V11 artifact scores','QC-V12-J-008','ART-V11'); sc('dim_v11','V11 20-dimension scorecard','QC-V12-J-002','DIM-V11')
sc('gate_v11','V11 gates','QC-V12-J-003','GATE-V11'); sc('weights_v10','V10 historical engineering weights','QC-V12-J-002','WGT-V10')
sc('rct_v9','V9 RCTCFE evaluation','QC-V12-J-001','RCT-V9'); sc('rct_v8','V8 RCTCFE evaluation','QC-V12-J-001','RCT-V8')
sc('art_v8','V8 artifact scores','QC-V12-J-008','ART-V8'); sc('gate_v8','V8 gates','QC-V12-J-003','GATE-V8')
KPIS=[]
for r in d['kpi_v9']:
    n=int(r[0][-2:]); conf= n==32
    note={6:'DEC-157 (CONFLICT-460): 99.5% pilot; 99.9% non-blocking objective — V12 also marks it Review target: consistent',13:'Runtime ≥ 99.5%; gold-set gate 100% schema-valid (AIX-05) adopted',14:'≥ 95% (supersedes V7 90%); OKPI-14 already 95%',15:'F1 ≥ 0.90 adopted with recall reported; OKPI-15 precision ≥ 90% kept',18:'Matches NFR-056',19:'Matches NFR-057 (4 h)',28:'DEC-160 freshness class F-1 (≤ 60 s) for projections',32:'V12 Blocking ≤ 120 min vs DEC-158 staged (4 h pilot; 2 h after Topology B) → CONFLICT-923',33:'FR-ENH-I-020',34:'FR-ENH-I-020',35:'CJ preflight = blueprint PDP; DB constraint effect.preflight_verdict → TC-V12-J-121'}.get(n,'Same metric, target and gate')
    add('FSD V12','34','V9 Release KPIs',r[0]+' (V12)',f'{r[1]} {r[2]} — {r[3]} — {r[4]}; V9 reconciliation: {r[5] or "—"}','Conflict' if conf else 'Covered',f'OKPI-{n:02d} (Part 4.4a §4.4.4; Part 6.6 RTM)','Alias V12 KPI-%02d ≡ OKPI-%02d; %s'%(n,n,note),'OKPI-%02d (alias)'%n,'Pending Founder decision' if conf else 'Matched')
    KPIS.append([r[0],r[1],r[2],r[4],'OKPI-%02d'%n,note])
T['kpis']=KPIS
# requirement register status columns (meta aspects)
for rid,r in reg.items():
    add('FSD V12','34','V8 requirement status register (233) — status columns',rid+'-STATUS',f'{rid} spec/prototype status "{r[4][:120]}"; production "{r[6]}"','Not covered','—','Carry the three status columns (specification, prototype, production) in the V12 acceptance register (FR-V12-J-004)','FR-V12-J-004')
# ---------------- ch35 ----------------
CODE={'Repository structure':'CS-GEN-02 (Part 4.4a §4.4.5.1.2)','Frontend':'CS-TS-01…, CS-RE-01…, CS-A11Y (Part 4.4a)','Python/Django':'CS-PY, CS-DJ-01…, CS-API (Part 4.4a)','SQL':'CS-SQL-01…, CS-MIG-01… (Part 4.4a)','Review':'CS-AIC-01; CR-CHK-01…40; Part 4.3 §4.32.2','CI':'Part 4.3 PL-01…17; §4.4.5.1.25'}
for k,r in enumerate(d['coding'],1):
    add('FSD V12','35','V10 Source coding and review controls','CODE-%02d'%k,f'{r[0]}: {r[1]} (owner {r[2]})','Covered',CODE[r[0]],'Confirm; V12 wording retained as alias','— (confirmed)')
BUILD=[]
for r in d['build']:
    sk=r[0][:9]; s=SKU[sk]
    add('FSD V12','35','V8 Prototype code is not production code (backlog)',r[0],f'{r[1]}; {r[2]}','Partially covered' if s['cls']=='H' else 'Not covered',
        f"{s['ep']} stories and Part 8.1 sprints" if s['cls']=='H' else f"{s['ep']}; {s['anchor']}",'Adopt V12 task ID; estimate, owner, acceptance IDs and dependencies added (§11.10.5.7)',r[0]+' (canonical)','Pending Founder decision')
# ---------------- ch40 legacy dispositions ----------------
G={r['source_id']:r for r in csv.DictReader(open(BP+'final/coverage/G_test_mapping.csv'))}
Q={r['qc_id']:r for r in csv.DictReader(open(BP+'final/coverage/H_qc_map.csv'))}
W={r['work_item']:r for r in csv.DictReader(open(BP+'final/coverage/H_workitem_story_map.csv'))}
STAT={'E':'Equivalent','A':'Alias-equivalent','M':'Class-mapped','P':'Partial + ENH','N':'New ENH'}
for r in d['d_test']:
    g=G[r['id']]; tcs=(g['primary_tcs']+' '+g['tc_enh']).strip()
    add('FSD V12','40','Source disposition candidates — Test',f"{r['src']}/{r['id']}",f"{r['id']} {r['title']} ({r['context']}; {r['disposition']})",'Covered',f"Part 6.8b; G_test_mapping.csv ({STAT.get(g['status'],g['status'])}); {tcs[:120] or g['uat_pack']}",'Confirm existing mapping; semantic approval via FR-ENH-H-006','— (existing)')
for r in d['d_qc']:
    q=Q[r['id']]
    add('FSD V12','40','Source disposition candidates — QC',f"{r['src']}/{r['id']}",f"{r['id']} {r['title'][:140]}",'Covered',f"Part 6.9b §6.9.5.1.8; {q['blueprint_gate']}; {q['blueprint_verification_refs'][:100]}",'Confirm existing QC mapping (status %s)'%q['status'],'— (existing)')
for r in d['d_task']:
    w=W[r['id']]
    add('FSD V12','40','Source disposition candidates — Task',f"{r['src']}/{r['id']}",f"{r['id']} {r['context'][:150]}",'Covered',f"Part 6.9a §6.9.4.5; FR {w['blueprint_fr']}; stories {w['blueprint_stories'][:60]}; {w['sprints']}",'Confirm; estimate and predecessors identical (0 differences)','— (existing)')
# ---------------- engineering ----------------
ENGMAP={
 'closure/test_acceptance.py':{'test_pending_release':('Covered','Part 6.9b V-01…V-14; exit code 2'),'test_benchmark':('Partially covered','Part 7.3 benchmark (no matched-sample validator)')},
 'closure/test_closure.py':{},'starter/test_completeness_gate.py':{},'starter/test_reference_extended.py':{},'starter/test_contract_fixtures.py':{},
 'optimization/test_optimization_reference.py':{},'optimization/test_completeness_optimizer.py':{}}
KPIPASS={'test_zero_valid','test_negative_invalid','test_nonfinite','test_fractional_count','test_zero_denom','test_ratio_mismatch','test_ratio_correct','test_invalid_operator'}
BENCH={'test_benchmark','test_benchmark_empty','test_benchmark_duplicate','test_benchmark_negative_cost'}
for f,tests in d['eng_tests'].items():
    for t in tests:
        if f.endswith('test_acceptance.py') and t in KPIPASS: sb,loc,new='Partially covered','Part 6.9b G-6 "recomputed from measured values" (no numeric-domain rules)','TC-V12-J-121'
        elif f.endswith('test_acceptance.py') and t in BENCH: sb,loc,new='Partially covered','Part 7.3 W1 benchmark; RECOMMENDATION-441','TC-V12-J-122'
        elif f.endswith('test_acceptance.py'): sb,loc,new='Covered','Part 6.9b V-01…V-14; exit code 2; FR-ENH-H-005','— (confirmed)'
        elif 'test_gate' in t: sb,loc,new='Covered','Part 6.9b V-05, V-06; TC-ENH-H-006','— (confirmed)'
        elif f.endswith('test_closure.py'): sb,loc,new='Covered','Part 3.5a/b candidate contracts; Part 6.9b FR-ENH-H-006 semantic approval; additionalProperties false','— (confirmed)'
        elif 'optimization' in f and t in ('test_nan','test_ratio_negative','test_ratio_excess','test_bool_score','test_candidate_nan','test_retry_negative'): sb,loc,new='Partially covered','Part 8.3 OKPI scoring (no numeric-domain rules)','TC-V12-J-121'
        else: sb,loc,new='Covered','Parts 6.8c/6.9b/8.3 (source-pack engineering reference, already reconciled)','— (confirmed)'
        add('src/engineering (read as data)',f.split('/')[0],f,f'{f}::{t}',f'Offline reference test {t}',sb,loc,'Confirm' if new.startswith('—') else 'Add numeric-domain assertions',new)
for r in d['opt_scen']:
    add('src/engineering (read as data)','optimization','optimization_acceptance_scenarios.csv',r[0],f'{r[1]}: {r[2]} → {r[3]} ({r[4]})','Covered','Part 8.3 (OPT-TEST-01…24 reconciled); Part 6.9b preflight group "Optimization scenarios"','Confirm','— (confirmed)')
for r in d['effort_review'][1:]:
    add('src/engineering (read as data)','closure','closure_effort_review.csv','EFF-'+r[0][:24].replace(' ','_'),f'{r[0]}: {r[1]} × {r[2]}/{r[3]}/{r[4]} = {r[5]}/{r[6]}/{r[7]} PD; {r[10]}','Covered','Part 6.9b §6.9.5.4.2 [GAP-450] 32.55 / 62.85 / 123.70 PD','Confirm; not added (overlap rule kept)','— (confirmed)')
for k,v in d['acc_groups'].items():
    add('src/engineering (read as data)','closure','acceptance_required_ids.json','ACCGRP-'+k.replace(' ','_'),f'Preflight group "{k}": {v["n"]} required IDs from {v["register"]}','Covered','FR-ENH-H-005 combined preflight (Part 6.9b §6.9.5.6)','Extend with V12 groups (FR-V12-J-005)','FR-V12-J-005')
for r in d['eval_seed']:
    add('src/engineering (read as data)','starter','ai_eval_seed.jsonl',r['id']+' (seed)',f"{r['case']} → {r['expected']}",'Covered','Part 6.4 AI evaluation (grounding, cross-tenant, abstain, injection)','Confirm','— (confirmed)')
for rep,ran,ok in [('starter_regression.txt',529,'528 passed, 1 skipped'),('optimization_regression.txt',34,'34 passed'),('closure_tests.txt',237,'237 passed')]:
    add('src/engineering (read as data)','closure',rep,'REG-'+rep.split('.')[0],f'Offline regression report: {ran} ran, {ok}; synthetic only','Not applicable','—','Not applicable: offline reference-code results are not product test evidence (V12 ch33 rule; DEC-682)','—','Not applicable (reference-code result, not product evidence)')
# ---------------- prose aspects ----------------
PROSE=[('33','V12','P33-01','V12 checks executed with Playwright + Chromium; axe-core 4.10; PostgreSQL 16 for Appendix C2','Partially covered','Part 6.1 tooling (Playwright, axe-core)','Tool versions verify at implementation; QC-V12-J-007','QC-V12-J-007'),
('33','V11','P33-02','REC-10 scoped withdrawal and REC-12 candidate-specific promotion supersede V9 checks; full compliant run "Load compliant example" → Completed (A-E2E)','Partially covered','TC-ENH-G-008; TC-04-032','Covered by parity class TC-V12-J-107','TC-V12-J-107'),
('33','V10','P33-03','Targeted tests limited to listed paths; observed page errors 0; production, real-device, exhaustive route, accessibility and load tests remain required','Covered','Part 6.1 levels; NFR-088; LT-01…','Confirm','— (confirmed)'),
('33','V8','P33-04','Status of all specified tests is "Not run" until staging execution; prototype evidence listed separately, not production acceptance','Partially covered','Part 6.1 §6.1.5.5 certification levels','DEC-682; QC-V12-J-007','QC-V12-J-007'),
('33','V6','P33-05','MT-38 consolidate recurring documentation policies/tests: common precheck/DTO policy IDs reused; no lost coverage','Partially covered','Part 6.10 closure','MT-TC-MT-38 canonical row','MT-TC-MT-38'),
('33','V5','P33-06','OPT-TC-{ID} per 135 V5 requirements; staging with scoped fictional fixtures and real sandboxes where authorized; negative, boundary, concurrency, cost, quality, security and recovery evidence','Not covered','—','Adopt; §11.10.5.3','OPT-TC-* (135)'),
('33','V5','P33-07','Each executed test records build, tenant fixture, input, expected, actual, status, evidence link, reviewer and date','Partially covered','Part 6.9b evidence manifest (no tenant-fixture/input fields)','Add fields to EVR (QC-V12-J-007)','QC-V12-J-007'),
('33','V5','P33-08','Never mark production tests passed based on local HTML checks','Covered','Part 6.1 §6.1.5.5 (L-P only from prod)','Confirm (DEC-682)','DEC-682'),
('33','V5','P33-09','1,342 proposed workflow scenarios plus 39 independent entitlement tests; implementation code and real sandboxes pending','Not covered','—','Adopt all (§11.10.4.2)','TC-V12-J-001…010, -019'),
('33','V5','P33-10','Historic 624 Unit/SIT/UAT and 175 expansion scenarios archived; deduplicate with current IDs before executing','Covered','Part 6.8 (799 tests mapped)','Confirm; dedupe rule QC-V12-J-005','QC-V12-J-005'),
('34','V12','P34-01','Score basis: production evidence unchanged, so 12/10 not awarded','Not covered','—','QC-V12-J-001','QC-V12-J-001'),
('34','V11','P34-02','20-dimension weights (doc 36, total 100); unscored dimensions not estimated; normalised over scored weight (69/100)','Not covered','—','QC-V12-J-002','QC-V12-J-002'),
('34','V10','P34-03','Weights sum to 100; unknown evidence unscored; blocking gates cannot be waived by weighted averages','Partially covered','Part 4.4a CS precedence (security overrides score)','QC-V12-J-002','QC-V12-J-002'),
('34','V9','P34-04','Blocking KPIs need production evidence before release; review targets need owner approval and measurement; V9 reconciliation column controls','Covered','Part 4.4a OKPI table; Part 6.9b G-6','Confirm (DEC-681)','DEC-681'),
('34','V8','P34-05','RCTCFE 100-point rubric on actual evidence; 12/10 aspirational; high score never overrides an open gate; 100 independent agents not executed','Not covered','—','QC-V12-J-001','QC-V12-J-001'),
('34','V7','P34-06','MOB-18 release/regression/traceability: SHA-256 of four HTMLs; 179 logical routes mapped to both device presentations','Partially covered','Part 2.7 responsive rules','QC-V12-J-010','QC-V12-J-010'),
('34','V7','P34-07','430/430 targeted checks; route-shell rendering only; no real services or provider effects','Not applicable','—','Prototype evidence (DEC-682)','—'),
('34','V7','P34-08','RCTCFE specialist perspectives; no 100 agents executed; no production certification or outcome claims','Covered','Part 9.3 quality report wording','Confirm','— (confirmed)'),
('34','V7','P34-09','Outstanding: production React/TS with one route/DTO/state definition per application','Covered','Part 3.1; CS-RE; DEC-270','Confirm','— (confirmed)'),
('34','V7','P34-10','Outstanding: approve API/physical schema, role/tenant/portfolio policies, provider and commercial contracts','Covered','Part 6.9b SPDEC queue; Part 3.5/3.6','Confirm','— (confirmed)'),
('34','V7','P34-11','Outstanding: server-authenticated cross-device session/draft storage and signed idempotent application handoff','Partially covered','DEC-270; Part 4.1 sessions','Parity class TC-V12-J-114','TC-V12-J-114'),
('34','V7','P34-12','Outstanding: PWA, notification permission and cache policy only after privacy/security review','Covered','CS-RE-07; Part 4.4a','Confirm','— (confirmed)'),
('34','V7','P34-13','Outstanding: mobile accessibility, real-device performance, security, concurrency, integration, load, recovery and operational UAT','Covered','Part 6.1; NFR-088; LT-ENH','Confirm','— (confirmed)'),
('34','V7','P34-14','Outstanding: reconcile inherited candidate decisions; V6 simulations and 430 checks are not implementation evidence','Covered','Part 6.9b SPDEC; DEC-682','Confirm','DEC-682'),
('34','V6','P34-15','V6 boundaries: targeted tests do not prove tenant isolation, financial accuracy, provider access, concurrency; 40 MT production tests pending','Covered','Part 6.1 certification levels','Confirm; MT-TC rows adopted','MT-TC-MT-01…40'),
('34','V5','P34-16','V5 browser regression: 34 route shells, inventory counts, 9 scenario calculations, sample cap, negative fixtures, loop cap, demo persona; not exhaustive','Not applicable','—','Prototype evidence (DEC-682)','—'),
('34','V3','P34-17','Release evidence matrix requirement→SKU→workflow→step→engine→UI/API/DB→test→task→release','Partially covered','Part 6.6 RTM (no SKU/workflow/step levels)','FR-V12-J-006 RTM levels','FR-V12-J-006'),
('34','V3','P34-18','QA independent of implementer; all critical positive/negative/security, consent, financial and tenant tests pass','Covered','Part 6.9b V-06; BLK-1…10','Confirm','— (confirmed)'),
('34','V3','P34-19','Evidence includes build hash, fixture version, environment, actual outputs, timestamp, reviewer','Partially covered','Part 6.9b manifest (no fixture version)','QC-V12-J-007','QC-V12-J-007'),
('34','V3','P34-20','No release on unresolved critical/high risk without approved remediation; legal/security gates cannot be waived by AI','Covered','Part 8.2 go/no-go; DEC safety invariants','Confirm','— (confirmed)'),
('34','V4','P34-21','V4: local Chromium rendering; no live systems, formal accessibility or production security evidence','Not applicable','—','Prototype evidence (DEC-682)','—'),
('35','V8','P35-01','Prototype keeps layered V3–V8 functions; production implements each behaviour once from Appendices A–C; must not port layering, demo identity switching or localStorage','Partially covered','DEC-270; CS-RE-07 (no layering/demo-identity rule)','CS-V12-J-01, CS-V12-J-02','CS-V12-J-01; CS-V12-J-02'),
('35','V8','P35-02','Coding: typed DTOs, domain services, narrow serializers, scoped managers, parameterized SQL, migration review, no secret in repo, structured errors and audit','Covered','CS-DJ, CS-API, CS-SQL, CS-SEC (Part 4.4a)','Confirm','— (confirmed)'),
('35','V8','P35-03','PR requires tests, schema changes, authorization checks, performance impact and rollback plan','Covered','CR-CHK-01…40; Part 4.3 §4.32.2 item 11','Confirm','— (confirmed)'),
('35','V8','P35-04','Backlog grouped by foundation and SKU; each task has owner, estimate after contract, acceptance ID and dependency','Partially covered','Part 6.9b work-item layer (no SKU grouping)','39 BUILD tasks detailed (§11.10.5.7)','SM-SVC-01…39-BUILD'),
('35','V10','P35-05','Historical source D25 table 2 controls are candidate controls, not execution evidence; superseded public exposure and provider prices excluded from runtime','Covered','Part 4.4a §4.4.5.1','Confirm','— (confirmed)'),
]
for p in PROSE: add('FSD V12',p[0],p[1]+' prose',p[2],p[3],p[4],p[5],p[6],p[7],'Not applicable (prototype evidence boundary)' if p[4]=='Not applicable' else 'Matched')
# approval-gap aspects (blueprint-originated additions, recorded for traceability)
for w,t in APRTC.items():
    add('FSD V12','33 / workbook','Panel finding: approval-routed workflow without APPROVAL scenario',w+'-APPROVAL-GAP',f'{w} steps route approval/review but V12 defines no -TC-APPROVAL scenario','Not covered','—','Add approval-binding test instance',t)
# ---------------- effort model ----------------
STEPPD={'Evidence retrieval':(0.75,1.0,1.5),'AI inference':(1.0,1.5,2.5),'Deterministic calculation':(0.5,0.75,1.25),'Deterministic domain logic':(0.5,0.75,1.25),'Policy gate / human review':(0.25,0.5,0.75),'Deterministic identity / reconciliation':(0.75,1.25,2.0),'External effect':(1.0,2.0,3.0)}
REUSE={'H':0.2,'M':0.55,'N':1.0}
FIX={'H':(1.0,1.5,2.5),'M':(3.0,5.0,8.0),'N':(6.0,10.0,16.0)}
WFPACK=(0.25,0.5,0.75)
FIXP=(0.2,0.3,0.5); ATU=(0.1,0.15,0.25); ENTU=(0.15,0.25,0.4)
def addv(a,b,f=1): return tuple(x+y*f for x,y in zip(a,b))
BROWS=[]; tot={'H':(0,0,0),'M':(0,0,0),'N':(0,0,0)}
for r in d['build']:
    sk=r[0][:9]; s=SKU[sk]; c=s['cls']; e=FIX[c]
    wfs=sorted(w for w in steps if w.startswith(sk))
    nsteps=0; nscen=0
    for w in wfs:
        e=addv(e,WFPACK)
        for st in steps[w]: e=addv(e,STEPPD[st[1]],REUSE[c]); nsteps+=1
        nscen+=len(wf[w])
    build=e
    test=addv(addv(addv((0,0,0),FIXP,len(wfs)),ATU,len(wfs)),ENTU,1)
    total=addv(build,test)
    tot[c]=addv(tot[c],total)
    BROWS.append([r[0],s['name'],c,s['ep'],len(wfs),nsteps,nscen,'%.1f/%.1f/%.1f'%build,'%.1f/%.1f/%.1f'%test,'%.1f/%.1f/%.1f'%total,total])
T['build']=BROWS
N['build_tot']={k:[round(x,1) for x in v] for k,v in tot.items()}
N['build_all']=[round(sum(tot[k][i] for k in tot),1) for i in range(3)]
json.dump({'SKU':SKU,'CATTC':CATTC,'STEPTC':STEPTC,'APRTC':APRTC,'ANCH':ANCH,'STEPANCH':STEPANCH},open(os.path.join(HERE,'j_ids.json'),'w'),indent=1)
# ---------------- write CSV ----------------
os.makedirs(BP+'final/coverage_v12',exist_ok=True)
with open(BP+'final/coverage_v12/J_coverage.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['doc','chapter','section','aspect_id','aspect_summary','status_before','blueprint_location','action','new_ids','status_after'])
    w.writeheader(); [w.writerow(a) for a in A]
ids=Counter(a['aspect_id'] for a in A); dup=[k for k,v in ids.items() if v>1]
N['aspects']=len(A); N['dups']=dup[:10]
N['by_before']=Counter(a['status_before'] for a in A); N['by_after']=Counter(a['status_after'] for a in A)
fam=defaultdict(Counter)
for a in A: fam[a['section']][a['status_before']]+=1
N['by_section']={k:dict(v) for k,v in fam.items()}
json.dump(T,open(os.path.join(HERE,'j_tables.json'),'w'),indent=0,ensure_ascii=False)
json.dump(N,open(os.path.join(HERE,'j_nums.json'),'w'),indent=1,default=list)
print(json.dumps(N,indent=1,default=list)[:3500])
