# Part 11.13 effort model. Unit sizes as Part 9.7b §9.7.13.1; rates ₹4,545 / 5,682 / 6,818 per pd (Part 8.4).
U={'AS':(2,3,5),'AM':(4,6,8),'AC':(6,9,13),'US':(1.5,2.5,4),'UM':(3,4,6),'UC':(4,6,9),'WF':(1,2,3),'SX':(1,2,3),'SN':(3,4,6)}
R=(4545,5682,6818)
items=[
# release, id, desc, unit or explicit tuple
('A2','AU-141','Agent tool-call behaviour firewall','UC'),('A2','PU-M1','Behaviour profile store, sequence baselines, quarantine hook in gateway',(4,6,8)),('A2','WF-56','wiring','WF'),
('A2','AG-084','Approval Reviewer Copilot','AM'),('A2','AU-122','Grouped approval packager','UM'),('A2','AU-124','Approval risk scorer and SLA predictor','UM'),('A2','WF-44','wiring','WF'),('A2','SX-A033','A033/A035/A066/A068 approval drawer extension','SX'),
('A2','AG-087','Revenue Leakage Analyst','AM'),('A2','AU-129','Revenue leakage rule engine (LK-01…LK-14)','UC'),('A2','WF-47','wiring','WF'),('A2','SX-A083','A083 leakage tab','SN'),
('A2','AG-086','Regulatory Rule-Pack Compliance Reviewer','AC'),('A2','AU-128','Rule-pack registry and deterministic checks','UC'),('A2','WF-46','wiring','WF'),('A2','SX-A047','A047/A051 rule-pack findings panel','SX'),
('A2','AG-088','Integration Self-Healing Advisor','AM'),('A2','AU-130','Integration health prober and schema-drift detector','UC'),('A2','AU-131','Safe auto-remediation executor','UC'),('A2','WF-48','wiring','WF'),('A2','SX-A008','A008 health and remediation tab','SX'),
('A2','AU-123','Cross-service buying-signal router (39 services)','UC'),('A2','WF-43','wiring','WF'),('A2','SX-A019','A019 routing view','SX'),
('A2','AG-092','Executive Decision Briefing Agent','AS'),('A2','AU-136','Executive briefing assembler','US'),('A2','WF-52','wiring','WF'),
('A2','AG-093','Tenant Go-Live Copilot','AM'),('A2','AU-137','Go-live readiness evaluator and TTFV clock','UM'),('A2','WF-53','wiring','WF'),('A2','SX-A099','A099/A101 go-live panel; W-portal checklist','SX'),
('A3','AG-081','Research Swarm Coordinator','AC'),('A3','AG-082','Evidence Cross-Verifier','AM'),('A3','AU-120','Swarm fan-out budgeter and quorum checker','UM'),('A3','WF-41','wiring','WF'),('A3','SX-A116','A116/A114 swarm run view','SX'),
('A3','AG-083','Human-Gated AI SDR Assistant','AC'),('A3','AU-121','SDR capacity governor and mailbox-health gate','UM'),('A3','WF-42','wiring','WF'),('A3','SN-SDR','SDR worklist view inside A037/A119','SN'),
('A3','AG-085','Service Outcome Tuning Advisor','AM'),('A3','AU-125','Service outcome SLO tracker','UM'),('A3','AU-126','Bounded parameter auto-tuner','UC'),('A3','AU-127','Workflow process-mining analyzer','UC'),('A3','WF-45','wiring','WF'),('A3','SX-A089','A089/A110 outcome SLO tab','SX'),
('A3','AG-089','Campaign Digital-Twin Analyst','AM'),('A3','AU-132','Campaign Monte Carlo simulator','UC'),('A3','WF-49','wiring','WF'),('A3','SX-A058','A058/A059 pre-flight tab','SX'),
('A3','AG-090','Procurement Negotiation Prep Assistant','AM'),('A3','AU-134','Should-cost and quote normalizer','UM'),('A3','WF-50','wiring','WF'),('A3','SX-A105','A105 negotiation prep panel','SX'),
('A3','AG-091','Knowledge Graph Relation Extractor','AM'),('A3','AU-135','KG write gate and provenance store','UC'),('A3','PU-M2','Graph tables, RLS, recursive path queries',(4,6,8)),('A3','WF-51','wiring','WF'),('A3','SX-A032','A032/A116 relationship graph view','SN'),
('A3','AG-095','Prompt Improvement Proposer','AM'),('A3','AU-140','Offline replay comparator','UM'),('A3','WF-55','wiring','WF'),
('A2','AU-142','AI content provenance signer and label enforcer','UM'),
('A4','AG-096','Synthetic Buyer Panel','AS'),('A4','AU-133','Synthetic-panel calibration tracker','UM'),
('A4','AG-094','Template Certification Assistant','AM'),('A4','AU-138','Template sanitizer and packager','UC'),('A4','AU-139','Template certification pipeline','UC'),('A4','PU-M3','Template package format, gallery and install engine',(6,9,12)),('A4','WF-54','wiring','WF'),('A4','SN-A113','A113 gallery extension and tenant install flow','SN'),
('A4','AU-143','Privacy-preserving cross-tenant benchmark aggregator','UC'),
]
def val(u): return U[u] if isinstance(u,str) else u
tot={};
for r,i,d,u in items:
    v=val(u); t=tot.setdefault(r,[0,0,0]); 
    for k in range(3): t[k]+=v[k]
# QA/eval/red-team uplift 15% and PM/design 5%
print("ITEMS")
for r,i,d,u in items: print(r,i,d,val(u))
g=[0,0,0]
for r in sorted(tot):
    b=tot[r]; up=[x*1.20 for x in b]
    cost=[up[k]*R[k]/1e5 for k in range(3)]
    print(r,'raw',b,'with20%',[round(x,1) for x in up],'cost L',[round(c,2) for c in cost])
    for k in range(3): g[k]+=up[k]
print('TOTAL pd',[round(x,1) for x in g],'L',[round(g[k]*R[k]/1e5,2) for k in range(3)])
