"""Group F (R5): parse V12 FSD AI agent registry (ch15), EVAL suites (ch16.4) and
master traceability register (ch40 V8) so every AGT-/EVAL- row is counted."""
import re, json, sys, collections
FSD="/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad/v12/FSD/"
def tables(path):
    lines=open(path,encoding='utf-8').read().split('\n'); out=[]; cur=None; row=None
    for i,l in enumerate(lines):
        if l=='[TABLE]': cur=[]; row=None; continue
        if l=='[/TABLE]':
            if row is not None: cur.append(row)
            out.append(cur); cur=None; continue
        if cur is not None:
            if l=='---row':
                if row is not None: cur.append(row)
                row=[]
            else: row.append(l)
    return out
reg=[t for t in tables(FSD+"15_AI_Agent_Registry_Orchestration.txt") if t[0][0]=='Agent ID'][0][1:]
ev=[t for t in tables(FSD+"16_AI_Models_Prompts_Evaluation.txt") if t[0][0]=='Suite'][0][1:]
tr=[t for t in tables(FSD+"40_Master_Traceability_Decision_Register_S.txt") if t and t[0][:5]==['Workflow','SKU','Steps','Engine','Agent']][0][1:]
res={'registry':reg,'eval':ev,'trace':tr}
agents=collections.OrderedDict()
for r in reg: agents[r[0]]={'role':r[1],'wf_count':int(r[2].split(':')[0]),'reg_wfs':r[2],'allowed':r[3],'never':r[4],'trace_wfs':[],'eval':[],'engines':set(),'ai_steps':0,'svcs':set()}
for r in tr:
    wf,sku,steps,eng,ag=r[:5]
    m=re.search(r'AI (\d+)',steps); ai=int(m.group(1)) if m else 0
    if ag in agents:
        a=agents[ag]; a['trace_wfs'].append(wf); a['engines'].add(eng); a['ai_steps']+=ai; a['svcs'].add(sku)
    else: print('trace agent not in registry',wf,ag)
for r in ev:
    suite,name,sku,ai,ag,lang=r[:6]
    agents[ag]['eval'].append((suite,name,int(ai)))
tot_ai=0
for k,a in agents.items():
    tot_ai+=a['ai_steps']
    print(k,a['role'],'reg',a['wf_count'],'trace',len(a['trace_wfs']),'eval',len(a['eval']),'aisteps',a['ai_steps'],sorted(a['svcs']),sorted(a['engines']))
print('registry rows',len(reg),'eval rows',len(ev),'trace rows',len(tr),'AI steps total',tot_ai)
print('eval langs',collections.Counter(r[5] for r in ev))
print('eval suites without AI', [r[0] for r in ev if int(r[3])==0])
trwf=set(r[0] for r in tr); evwf=set(r[0].replace('EVAL-','') for r in ev)
print('wfs with no eval', sorted(trwf-evwf))
json.dump({k:{**v,'engines':sorted(v['engines']),'svcs':sorted(v['svcs'])} for k,v in agents.items()},open('/home/user/Allinonecalculator/blueprint/assembly/v12/F_agents.json','w'),indent=1)
json.dump({'eval':ev,'trace':tr},open('/home/user/Allinonecalculator/blueprint/assembly/v12/F_rows.json','w'))
