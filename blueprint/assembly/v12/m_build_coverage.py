# Builds final/coverage_v12/M_coverage.csv for Part 11.13 (Group R12, letter M)
import csv
A='Part 11.13a §11.13.5.3'; U='Part 11.13b §11.13.5.4'; W='Part 11.13b §11.13.5.5'
# id, name, capability, chapter, V12 section, release, FRs, stories, tests
rows=[
('AG-081','Research Swarm Coordinator','M01','BRD 08 / FSD 15','SM-SVC-01, 02, 19, 29; ENG-01','A3','FR-V12-M-001…006','US-05-YM01','TC-V12-M-001…010'),
('AG-082','Evidence Cross-Verifier','M01','FSD 16','AIX-11; ENG-01','A3','FR-V12-M-003, 004','US-05-YM02','TC-V12-M-007, 008'),
('AG-083','Human-Gated AI SDR Assistant','M02','BRD 08 / FSD 11','SM-SVC-06, 07, 08, 38; ENG-05','A3','FR-V12-M-007…013','US-08-YM03, YM04','TC-V12-M-011…019'),
('AG-084','Approval Reviewer Copilot','M04','BRD 18','BR-V7-AI-02; MOB-09; REC-03','A2','FR-V12-M-014…019','US-18-YM05, YM06','TC-V12-M-020…028'),
('AG-085','Service Outcome Tuning Advisor','M05','FSD 30 / FSD 14','ENG-15; FL-01','A3','FR-V12-M-020…026','US-18-YM07, US-21-YM08','TC-V12-M-029…037'),
('AG-086','Regulatory Rule-Pack Compliance Reviewer','M06','BRD 18','REC-11; MT-12; BR-V7-AI-01','A2','FR-V12-M-027…033','US-03-YM09, YM10','TC-V12-M-038…047'),
('AG-087','Revenue Leakage Analyst','M07','BRD 08 / FSD 10','SM-SVC-17, 18, 20, 21, 24, 31, 32, 37; ENG-09, ENG-10','A2','FR-V12-M-034…040','US-15-YM11, YM12','TC-V12-M-048…057'),
('AG-088','Integration Self-Healing Advisor','M08','FSD 27 / FSD 32','ENG-13','A2','FR-V12-M-041…047','US-21-YM13, YM14','TC-V12-M-058…066'),
('AG-089','Campaign Digital-Twin Analyst','M09','BRD 08','SM-SVC-14, 08, 38; ENG-12','A3','FR-V12-M-048…053','US-12-YM15, YM16','TC-V12-M-067…071'),
('AG-090','Procurement Negotiation Prep Assistant','M10','BRD 08','SM-SVC-39-WF01…03','A3','FR-V12-M-054…058','US-14-YM17, YM18','TC-V12-M-072…076'),
('AG-091','Knowledge Graph Relation Extractor','M11','FSD 17 / BRD 18','SM-SVC-02, 03, 25, 29, 32; MT-10','A3','FR-V12-M-059…064','US-02-YM19, YM20','TC-V12-M-077…082'),
('AG-092','Executive Decision Briefing Agent','M12','FSD 23','Authorized portfolio command centre','A2','FR-V12-M-065…069','US-17-YM21, YM22','TC-V12-M-083…086'),
('AG-093','Tenant Go-Live Copilot','M13','FSD 07 / FSD 09','Tenant provisioning; entitlement','A2','FR-V12-M-070…075','US-20-YM23, YM24','TC-V12-M-087…092'),
('AG-094','Template Certification Assistant','M14','FSD 14 / FSD 15','MT-34, MT-35; A113','A4','FR-V12-M-076…080','US-20-YM25, US-18-YM26','TC-V12-M-093…096'),
('AG-095','Prompt Improvement Proposer','M15','FSD 16','AIX-04, AIX-06','A3','FR-V12-M-081…085','US-04-YM27, YM28','TC-V12-M-097…099'),
('AG-096','Synthetic Buyer Panel','M09b','BRD 08','SM-SVC-11, 14, 30','A4','FR-V12-M-086…089','US-12-YM29, YM30','TC-V12-M-100'),
('AU-120','Swarm fan-out budgeter and quorum checker','M01','FSD 15','AIX-09; AI-12','A3','FR-V12-M-001…004','US-05-YM01','TC-V12-M-001…006, 008'),
('AU-121','SDR capacity governor and mailbox-health gate','M02','BRD 08','SM-SVC-06; BR-M24','A3','FR-V12-M-008…010, 013','US-08-YM04','TC-V12-M-011…016, 019'),
('AU-122','Grouped approval packager with per-item hash binding','M04','BRD 18','BR-V7-AI-02','A2','FR-V12-M-012, 014…016','US-18-YM05','TC-V12-M-018, 020, 021, 023'),
('AU-123','Cross-service buying-signal router','M03','BRD 08 / BRD 18','SM-SVC-02-WF04; REC-03','A2','FR-V12-M-090…092','US-05-YM31, YM32','TC-V12-M-013; Gherkin US-05-YM31/32'),
('AU-124','Approval risk scorer and SLA predictor','M04','BRD 18','BRL-AUT-01','A2','FR-V12-M-017…019','US-18-YM06','TC-V12-M-022, 024, 028'),
('AU-125','Service outcome SLO tracker','M05','BRD 22 / FSD 30','Service KPIs','A3','FR-V12-M-020, 021','US-18-YM07','TC-V12-M-029, 030'),
('AU-126','Bounded parameter auto-tuner with auto-revert','M05','FSD 30','Optimization','A3','FR-V12-M-022…024','US-21-YM08','TC-V12-M-031…034'),
('AU-127','Workflow process-mining analyzer','M05','FSD 12 / FSD 13','FL-01, FL-03','A3','FR-V12-M-025','US-21-YM08','TC-V12-M-035, 036'),
('AU-128','Regulatory rule-pack registry and deterministic checks','M06','BRD 18','REC-11','A2','FR-V12-M-027…030','US-03-YM09','TC-V12-M-038…042, 047'),
('AU-129','Revenue leakage rule engine','M07','FSD 10 / BRD 08','SM-SVC-21, 31, 32, 37','A2','FR-V12-M-034…037, 040','US-15-YM11','TC-V12-M-048…053, 056, 057'),
('AU-130','Integration health prober and schema-drift detector','M08','FSD 27','Provider adapters','A2','FR-V12-M-041…043','US-21-YM13','TC-V12-M-058…060'),
('AU-131','Safe auto-remediation executor','M08','FSD 32','Retry and recovery','A2','FR-V12-M-044, 045','US-21-YM13','TC-V12-M-061…063'),
('AU-132','Campaign digital-twin Monte Carlo simulator','M09','BRD 08','SM-SVC-14-WF01/02','A3','FR-V12-M-048…051','US-12-YM15','TC-V12-M-067…070'),
('AU-133','Synthetic-panel calibration tracker','M09b','BRD 08','SM-SVC-30-WF02','A4','FR-V12-M-087…089','US-12-YM30','TC-V12-M-100'),
('AU-134','Should-cost and supplier quote normalizer','M10','BRD 08','SM-SVC-39-WF02','A3','FR-V12-M-054, 055','US-14-YM17','TC-V12-M-072, 073'),
('AU-135','Knowledge-graph write gate and provenance store','M11','BRD 18','MT-10, MT-12','A3','FR-V12-M-059…062, 064','US-02-YM19, YM20','TC-V12-M-077…080, 082'),
('AU-136','Executive briefing assembler','M12','FSD 23','Portfolio command centre','A2','FR-V12-M-065, 066','US-17-YM21','TC-V12-M-083, 084'),
('AU-137','Go-live readiness evaluator and time-to-first-value clock','M13','FSD 07','Tenant provisioning','A2','FR-V12-M-070…073','US-20-YM23','TC-V12-M-087…090'),
('AU-138','Template sanitizer and packager','M14','FSD 14','MT-34','A4','FR-V12-M-076, 077','US-20-YM25','TC-V12-M-093'),
('AU-139','Template certification pipeline','M14','FSD 16','AIX-05','A4','FR-V12-M-078, 079','US-20-YM25, US-18-YM26','TC-V12-M-094, 095'),
('AU-140','Offline replay comparator for prompt candidates','M15','FSD 16','AIX-06','A3','FR-V12-M-082…084','US-04-YM28','TC-V12-M-097, 098'),
('AU-141','Agent tool-call behaviour firewall','M16','FSD 15 / FSD 16','AI-12; AIX-09; AIX-20','A2','FR-V12-M-093…096','US-04-YM33, YM34','TC-V12-M-005, 101, 102'),
('AU-142','AI content provenance signer and label enforcer','M17','BRD 18','BR-V7-AI-01; SM-SVC-27','A2','FR-V12-M-097','US-11-YM35','TC-V12-M-103'),
('AU-143','Privacy-preserving cross-tenant benchmark aggregator','M18','BRD 18','BR-V7-AI-05 (conflict)','A4','FR-V12-M-098','US-17-YM36','N/A until DEC-747'),
('WF-41','Supervised research swarm with cross-verification','M01','BRD 09 / FSD 12','SM-SVC-01, 02, 19, 29','A3','FR-V12-M-001…006','US-05-YM01, YM02','TC-V12-M-001…010'),
('WF-42','Human-gated AI SDR working day','M02','BRD 09 / FSD 12','SM-SVC-06, 07, 08, 38','A3','FR-V12-M-007…013','US-08-YM03, YM04','TC-V12-M-011…019'),
('WF-43','Cross-service buying-signal orchestration','M03','BRD 09 / BRD 18','SM-SVC-02-WF04; REC-03','A2','FR-V12-M-090…092','US-05-YM31, YM32','Gherkin US-05-YM31/32'),
('WF-44','Approval packet and grouped review','M04','BRD 18','BR-V7-AI-02; MOB-09','A2','FR-V12-M-014…019','US-18-YM05, YM06','TC-V12-M-020…028'),
('WF-45','Service outcome SLO and bounded tuning loop','M05','FSD 30','Optimization','A3','FR-V12-M-020…026','US-18-YM07, US-21-YM08','TC-V12-M-029…037'),
('WF-46','Regulatory rule-pack pre-flight compliance','M06','BRD 18','REC-11','A2','FR-V12-M-027…033','US-03-YM09, YM10','TC-V12-M-038…047'),
('WF-47','Revenue leakage detection to recovery','M07','FSD 10','SM-SVC-21, 37','A2','FR-V12-M-034…040','US-15-YM11, YM12','TC-V12-M-048…057'),
('WF-48','Integration self-healing','M08','FSD 27 / FSD 32','Provider adapters','A2','FR-V12-M-041…047','US-21-YM13, YM14','TC-V12-M-058…066'),
('WF-49','Campaign digital-twin pre-flight','M09','BRD 09','SM-SVC-14-WF01/02','A3','FR-V12-M-048…053','US-12-YM15, YM16','TC-V12-M-067…071'),
('WF-50','Procurement negotiation preparation','M10','BRD 09','SM-SVC-39-WF02/03','A3','FR-V12-M-054…058','US-14-YM17, YM18','TC-V12-M-072…076'),
('WF-51','Knowledge graph build and governance','M11','FSD 17','MT-10, MT-12','A3','FR-V12-M-059…064','US-02-YM19, YM20','TC-V12-M-077…082'),
('WF-52','Executive decision briefing','M12','FSD 23','Portfolio command centre','A2','FR-V12-M-065…069','US-17-YM21, YM22','TC-V12-M-083…086'),
('WF-53','Tenant go-live copilot journey','M13','FSD 07 / FSD 09','Tenant provisioning','A2','FR-V12-M-070…075','US-20-YM23, YM24','TC-V12-M-087…092'),
('WF-54','Agent template submission, certification and install','M14','FSD 14','MT-34, MT-35','A4','FR-V12-M-076…080','US-20-YM25, US-18-YM26','TC-V12-M-093…096'),
('WF-55','Prompt improvement loop','M15','FSD 16','AIX-04, AIX-06','A3','FR-V12-M-081…085','US-04-YM27, YM28','TC-V12-M-097…099'),
('WF-56','Agent behaviour firewall containment','M16','FSD 15 / FSD 16','AI-12; AIX-20','A2','FR-V12-M-093…096','US-04-YM33, YM34','TC-V12-M-101, 102'),
]
out='/home/user/Allinonecalculator/blueprint/final/coverage_v12/M_coverage.csv'
with open(out,'w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['doc','chapter','section','aspect_id','aspect_summary','status_before','blueprint_location','action','new_ids','status_after'])
    for n,(i,name,cap,ch,sec,rel,fr,us,tc) in enumerate(rows,1):
        loc = A if i.startswith('AG') else (U if i.startswith('AU') else W)
        kind = 'agent card' if i.startswith('AG') else ('automation row' if i.startswith('AU') else 'workflow')
        pend = i=='AU-143'
        action=f"Added {kind} {i} (capability {cap}) with FRs, stories, tests, effort and separate development/running cost; release {rel}" + ("; enablement pending Founder decision DEC-747 (CONFLICT-983)" if pend else "")
        w.writerow(['Panel R12 AI improvement (new idea)',ch,f'{cap}: {sec}',f'M-NEW-{n:03d}',f'{i} {name}','Not covered (new idea)',f'{loc}; {i}',action,f'{i}; {fr}; {us}; {tc}','Pending Founder decision' if pend else 'Matched'])
print(len(rows))
