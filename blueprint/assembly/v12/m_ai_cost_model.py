# Part 11.13 (Group R12, letter M) cost model for new agents. Prices: Part 7.3 §7.3.2 (verify at implementation, as of 27 Nov 2026).
FX=90
P={'H':dict(i=0.10,o=0.50,cr=0.01,cw=0.125),'S':dict(i=2.00,o=10.00,cr=0.10,cw=2.50)}
H_RATE=0.7  # cache hit rate
# id, name, base tier, esc share to Sonnet, uncached_in, cached_in, out, calls/month, batch factor
A=[('AG-081','Research Swarm Coordinator','S',0,4000,2000,1500,120,1),
('AG-082','Evidence Cross-Verifier','H',0.10,3000,1000,400,1600,0.5),
('AG-083','Human-Gated AI SDR Assistant','S',0,3000,2000,700,1500,0.5),
('AG-084','Approval Reviewer Copilot','H',0.15,2000,1500,350,2000,1),
('AG-085','Service Outcome Tuning Advisor','S',0,10000,2000,2000,40,0.5),
('AG-086','Regulatory Rule-Pack Compliance Reviewer','H',0.20,1500,2500,400,2500,1),
('AG-087','Revenue Leakage Analyst','S',0,4500,1500,900,60,0.5),
('AG-088','Integration Self-Healing Advisor','H',0.25,3500,1500,600,150,1),
('AG-089','Campaign Digital-Twin Analyst','S',0,5500,1500,1200,30,1),
('AG-090','Procurement Negotiation Prep Assistant','S',0,7500,1500,1500,40,1),
('AG-091','Knowledge Graph Relation Extractor','H',0.05,2000,1000,500,4000,0.5),
('AG-092','Executive Decision Briefing Agent','S',0,8000,2000,1500,45,0.5),
('AG-093','Tenant Go-Live Copilot','H',0.20,2000,2000,600,600,1),
('AG-094','Template Certification Assistant','S',0,6000,2000,1200,20,0.5),
('AG-095','Prompt Improvement Proposer','S',0,12000,3000,3000,30,0.5),
('AG-096','Synthetic Buyer Panel','H',0,1000,1500,300,3000,0.5)]
def call(t,u,c,o,b):
    p=P[t]; return FX*b*(u*p['i']+c*(H_RATE*p['cr']+(1-H_RATE)*p['cw'])+o*p['o'])/1e6
tot=0;rows=[]
for a in A:
    i,n,t,e,u,c,o,k,b=a
    h=call('H',u,c,o,b); s=call('S',u,c,o,b)
    bl = s if t=='S' else (1-e)*h+e*s
    base=k*bl; tot+=base
    rows.append((i,n,t,e,u,c,o,k,b,h,s,bl,base))
    print(f"{i}|{n}|tier {t}|e={e}|in {u+c} ({c} cache)|out {o}|calls {k}|b {b}|H {h:.3f}|S {s:.3f}|blend {bl:.3f}|base {base:.0f}|low {0.3*base:.0f}|high {3*base:.0f}")
print('TOTAL base',round(tot),'low',round(0.3*tot),'high',round(3*tot),'with 25% overhead',round(tot*1.25))
