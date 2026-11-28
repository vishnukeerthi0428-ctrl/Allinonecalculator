"""Group J (R9) extraction: every test, QC, backlog and evidence row of FSD V12 ch33/34/35,
ch40 Test/QC/Task dispositions, workbook Acceptance_Tests, ch16 EVAL suites, and the
engineering test files (read as data, never executed). Writes j_items.json."""
import sys,re,json,csv,glob,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from j_parse_tables import parse
S='/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad/v12/'
F=S+'FSD/'
WB=glob.glob(S+'src/Sales_Marketing_Automation_Master_Automation_Service_Catalog_2031_39_Services_156_Workflows*_csv')[0]
ENG=S+'src/engineering/engineering/'
def ch(n): return glob.glob(F+n+'_*.txt')[0]
out={}
t33=parse(ch('33')); t34=parse(ch('34')); t35=parse(ch('35')); t40=parse(ch('40')); t16=parse(ch('16'))
def rows(t): return [r for r in t['data'] if r]
# ---- ch33
out['v12_ent']=rows(t33[0]); out['v12_qa']=rows(t33[1]); out['v12_loc']=rows(t33[2]); out['v11_qa']=rows(t33[3])
out['rec33']=rows(t33[4]); out['v10_tpe']=rows(t33[5]); out['v10_events']=rows(t33[6]); out['e2e_events']=rows(t33[7])
out['exc']=rows(t33[8]); out['xs']=rows(t33[9]); out['v9_qa']=rows(t33[10]); out['v8_axe']=rows(t33[11]); out['v8_evid']=rows(t33[12])
out['aix_cj']=rows(t33[13]); out['v8_qa']=rows(t33[14]); out['steps']=rows(t33[15]); out['wf_tests']=rows(t33[16])
# ---- ch34
names34=['rct_v12','art_v12','dim_v12','rct_v11','art_v11','dim_v11','gate_v11','rec34','weights_v10','kpi_v9','rct_v9','rct_v8','art_v8','gate_v8','reqreg','v7_groups','v7_qa','v6_checks','v5_checks','v3_qa','v4_checks']
for n,t in zip(names34,t34): out[n]=rows(t)
# ---- ch35
out['rec35']=rows(t35[0]); out['coding']=rows(t35[1]); out['build']=rows(t35[2])
# ---- ch40 dispositions
def disp(t):
    res=[]
    for r in rows(t):
        src,sid=r[0].split(' / ',1); i=sid.split(' ')[0]
        res.append({'src':src,'id':i,'title':sid[len(i):].strip(),'context':r[1],'disposition':r[2]})
    return res
out['d_test']=disp(t40[8]); out['d_qc']=disp(t40[9]); out['d_task']=disp(t40[10])
# ---- ch16 EVAL suites
out['eval']=rows(t16[4]); out['eval_gates']=rows(t16[3])
# ---- acceptance text for 233 register rows
acc={}
txt=''.join(open(p,encoding='utf-8').read()+'\n' for p in sorted(glob.glob(F+'[0-4]*_*.txt')))
L=txt.split('\n')
for k,l in enumerate(L):
    m=re.match(r'Acceptance:? (OPT-TC-[A-Z]+-\d+):\s*(.*)',l)
    if m and m.group(1) not in acc:
        title=req=''
        for j in range(k-1,max(k-4,0),-1):
            if L[j].startswith('Requirement:'): req=L[j][12:].strip()
            mm=re.match(r'([A-Z]+-\d+) · (P\d) · (.*)',L[j])
            if mm: title=mm.group(3); break
        acc[m.group(1)]={'acc':m.group(2).strip(),'req':req,'title':title}
    m=re.match(r'Acceptance: (MT-TC-MT-\d+) — (.*)',l)
    if m and m.group(1) not in acc:
        req=L[k-1][12:].strip() if L[k-1].startswith('Requirement:') else ''
        tl=L[k-2] if L[k-2].startswith('<Heading') else ''
        acc[m.group(1)]={'acc':m.group(2).strip(),'req':req,'title':re.sub(r'<Heading\d>\s*MT-\d+\s*—\s*','',tl)}
    m=re.match(r'Acceptance (MOB-\d+-AT\d+) — (.*)',l)
    if m and m.group(1) not in acc:
        blk={'acc':m.group(2).strip()}
        for j in range(k-1,max(k-8,0),-1):
            for key,pre in [('scope','Scope / UI mapping — '),('func','Functional contract — '),('req','Business requirement — '),('owner','Owner — ')]:
                if L[j].startswith(pre): blk[key]=L[j][len(pre):]
            mm=re.match(r'<Heading\d>\s*(MOB-\d+)\s+(.*)',L[j])
            if mm: blk['title']=mm.group(2).strip(); break
        acc[m.group(1)]=blk
out['acc']=acc
# ---- workbook acceptance tests
wb=list(csv.reader(open(WB+'/Acceptance_Tests.csv',encoding='utf-8-sig')))
out['wb_hdr']=wb[3]; out['wb_at']=[r for r in wb[4:] if r and r[0]]
si=list(csv.reader(open(WB+'/Service_Index.csv',encoding='utf-8-sig')))
out['sku']=[r for r in si if r and r[0].startswith('SM-SVC-')]
# ---- engineering test files (read as text only)
eng={}
for p in ['closure/test_acceptance.py','closure/test_closure.py','starter/test_completeness_gate.py','starter/test_reference_extended.py','starter/test_contract_fixtures.py','optimization/test_optimization_reference.py','optimization/test_completeness_optimizer.py']:
    eng[p]=re.findall(r'def (test[a-z_0-9]*)',open(ENG+p,encoding='utf-8').read())
out['eng_tests']=eng
out['opt_scen']=[r for r in csv.reader(open(ENG+'optimization/optimization_acceptance_scenarios.csv',encoding='utf-8-sig'))][1:]
out['effort_review']=[r for r in csv.reader(open(ENG+'closure/closure_effort_review.csv',encoding='utf-8-sig'))]
out['acc_groups']={k:{'register':v['register'],'n':len(v['required_ids'])} for k,v in json.load(open(ENG+'closure/acceptance_required_ids.json')).items()}
out['eval_seed']=[json.loads(l) for l in open(ENG+'starter/ai_eval_seed.jsonl') if l.strip()]
json.dump(out,open('j_items.json','w'),indent=0,ensure_ascii=False)
for k,v in out.items(): print(k, len(v))
