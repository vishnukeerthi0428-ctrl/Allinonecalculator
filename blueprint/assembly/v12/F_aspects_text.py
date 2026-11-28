"""Group F (R5) atomic aspect inventory for the prose/table material of FSD V12
chapters 14, 15, 16, 17, 18 and 30 (row-scale AGT/EVAL/trace rows are generated
in build_F.py from the parsed tables). Each tuple:
(doc, chapter, section, aspect_id, summary, status_before, blueprint_location, action, new_ids, status_after)
"""
M = "Matched"
PF = "Pending Founder decision"
C, P, N, X = "Covered", "Partially covered", "Not covered", "Conflict"

A = []
def a(ch, sec, aid, summ, sb, loc, act, new, sa=M, doc="FSD V12"):
    A.append((doc, ch, sec, aid, summ, sb, loc, act, new, sa))

# ---------------- Chapter 14 Shared AI & Automation Engines ----------------
ch = "14 Shared AI & Automation Engines"
a(ch, "V6", "F14-001", "Redundancy strategy: 15 logical engines and 25 foundations; versioned child workflows, adapters, prompt/role registries, common contracts; isolate state, cache, credentials, retrieval by authorized context; reuse definitions not data; keep retries, fallback, backups, DR as intentional redundancy", P,
  "Part 3.1 modular monolith; Part 7.2 §7.2.5; Part 9.7 §9.7.4.1", "Engine map ENG-01…15 to Django apps and AG/AU (§11.6.5.1); AU-178 audit of duplicate definitions; ADR-169", "ADR-169; AU-178; DEC-615")
a(ch, "MT-34", "F14-002", "MT-34 (P0): one definition per stable workflow/version; child-step reuse via contracts; per-customer configuration only; MT-TC-MT-34 25 customer configs, no SKU/WF cloning, regression IDs stable", P,
  "Part 2.2 §2.6 execution engine; DEC-051 DAG publish", "AU-178 CI duplicate-definition scan; TC-V12-F-061", "AU-178; FR-V12-F-040; TC-V12-F-061")
a(ch, "V5 FL-04", "F14-003", "FL-04 (P1): reusable child workflows (research, evidence, validation, approval, reconciliation) with versioned interfaces; OPT-TC-FL-04 child called by two parents, no duplicate charge or unauthorized SKU access", P,
  "Part 9.7 §9.7.4.2 supervisor steps; AU-042 metering", "AU-167 artifact reuse + AU-158 metering by run lineage; child-workflow contract rows in §11.6.5.1", "AU-167; AU-158; FR-V12-F-041; TC-V12-F-062")
eng = [("ENG-01","Research and evidence","SM-SVC-01; 02; 13; 19; 35","M10–M16 discovery; AG-003/004/005/006/027/019/107/118; AU-007/014/052"),
       ("ENG-02","Contact intelligence","SM-SVC-03; 29","M18–M20; AG-008/060/061; AU-018/074/085"),
       ("ENG-03","AI knowledge and RAG","SM-SVC-09; 15; 25; 33","M03 knowledge, TL-01; AG-001/014/017/031/055; AU-046/069/164/165/166"),
       ("ENG-04","Multimodal AI","SM-SVC-26; 27; 36","Not in baseline; AG-100/101/102/103/114/121; AU-168"),
       ("ENG-05","Communication","SM-SVC-06; 07; 08; 12; 38","M25–M28, M31; AG-011/013/058/063/110/119/120; AU-008/022/024/086/173"),
       ("ENG-06","Calendar","SM-SVC-10; 16","M29, M40; AU-023/051/075; AG-059"),
       ("ENG-07","Identity and permission","SM-SVC-28","Part 2.3 RBAC/ABAC; R20; AU-072/110/175; AG-104"),
       ("ENG-08","Document generation","SM-SVC-11; 17; 18","M43–M46; AG-018/020/022/066/117; AU-035/036/089"),
       ("ENG-09","Financial calculation","SM-SVC-24; 37","AU-040/041/049/087/096; AG-054/109"),
       ("ENG-10","Transaction reconciliation","SM-SVC-21; 31","AU-026/037/038/048; AG-024/112/116"),
       ("ENG-11","Prediction","SM-SVC-04; 23; 34","AU-017/056/059; AG-042/067/105"),
       ("ENG-12","Experimentation","SM-SVC-14; 30","AU-065/098; AG-052"),
       ("ENG-13","Workflow orchestration","SM-SVC-05; 20; 22; 32; 39","M55 engine; AG-039; AU-053/060; AG-111/115/122"),
       ("ENG-14","Governance","Shared","PDP AU-009, AU-025, AU-170…177; Part 7.3 §7.6"),
       ("ENG-15","Optimization","Shared","AU-001/002/068/118, AU-152…163; AG-080")]
for i,(e,n,s,loc) in enumerate(eng):
    st = N if e=="ENG-04" else P
    a(ch, "Engine table", f"F14-{4+i:03d}", f"{e} {n} → {s}; constraint: private tenant/startup scope, entitlement, audit, policy, model/connector portability, acceptance required", st,
      loc, f"Adopt {e} as logical engine ID; map to implementing modules and AG/AU (§11.6.5.1)", f"DEC-615; ADR-169" + ("; AG-100…103; AU-168" if e=="ENG-04" else ""))
a(ch, "Engine table note", "F14-019", "Map scheduler, approval, policy, budget and recovery to governance/orchestration and shared SaaS infrastructure; do not create one microservice per engine unless justified", C,
  "Part 3.1 ADR modular monolith (DEC-018 family); Part 2.2 §2.6", "Confirm: engines are logical groupings inside the Django monolith (ADR-169)", "ADR-169")

# ---------------- Chapter 15 AI Agent Registry ----------------
ch = "15 AI Agent Registry & Orchestration"
a(ch, "V8", "F15-001", "One registered role per agent; prompts reference the role (PRM-<AGT>-<task>-vN)", N,
  "Part 7.2 AG cards; ai_agent_definition; PC- prompt contracts (Part 7.4b, 9.7)", "Two-level registry: AGT role (canonical, 20) → AG implementation agents (103) → PRM prompts; AU-179 conformance", "DEC-600; DEC-601; ADR-160; AU-179; FR-V12-F-039")
a(ch, "V8", "F15-002", "Agents never hold effect tools in steps that read untrusted content (AIX-09)", C,
  "Part 7.2 §7.2.4 registry rule 1; Part 7.3 §7.6.3 capability layer; TL-13 not granted", "Map AIX-09 → registry rule 1; AU-179 checks AGT 'never allowed' list against TL grants", "AU-179; TC-V12-F-009")
a(ch, "V8 table", "F15-003", "AGT registry columns: Agent ID, Role, Workflows (count + IDs), Allowed tools, Never allowed", N,
  "Part 9.4 §9.4.3 (AG columns differ)", "Registry table §11.6.4.1 with AGT columns plus AG mapping; ai_agent_definition.agt_role_id", "DEC-600")
a(ch, "V8 table", "F15-004", "Uniform allowed tools for all 20 roles: scoped read, retrieval (own tenant), draft/score output", P,
  "Part 7.2 §7.2.4 TL-01/02/03/06/08/09 (per agent, finer)", "Adopt as role ceiling; per-AG TL grants must be a subset (AU-179) [GAP-865]", "AU-179; GAP-865")
a(ch, "V8 table", "F15-005", "Uniform never-allowed list: send, publish, spend, change live state, read other tenants", C,
  "TL-13 not granted; DEC-064; RLS (Part 3.3); BRL-AUT-01", "Map to TL-13 denial, RLS and PDP; AU-179 static check", "AU-179")
a(ch, "V6 MT-35", "F15-006", "MT-35 (P1): central role and prompt version registry; policy and scope as typed inputs; no copied prompts per company; MT-TC-MT-35 two tenant configs reference same approved role/version, outputs and memory isolated", P,
  "ADR-084 prompt versioning; Part 7.3 §7.6.9 tenant overrides brand/tone only; ADR-112 memory scope", "AU-153 prompt registry gate (typed tenant fields only, no per-company copies) + TC-V12-F-063", "AU-153; TC-V12-F-063; FR-V12-F-004")
a(ch, "V5 AI-12", "F15-007", "AI-12 (P0): agent-loop termination: max steps, tool calls, elapsed time, token spend; detect repeated equivalent actions; OPT-TC-AI-12 loop fixture terminates and records hold reason", P,
  "Part 7.2 §7.2.9 caps (50 steps, 8 LLM calls, 5 tool calls, deadline, token budget, duplicate-call suppression)", "AU-157 adds semantic-equivalence detector (normalized action digest repeat ≥ 2) and HELD reason; numbers stay §7.2.9 [GAP-867]", "AU-157; GAP-867; TC-V12-F-064")
roles = [("Research agent","Permitted search/read only; evidence set with source and timestamp","AG-003/004/040; TL-03/04/05; evidence provenance (M07)",C),
         ("Qualification agent","Read scoped evidence; score candidate; no automatic commitment","AG-009 brief; AU-017 deterministic score (DEC-011); DEC-001 gates",C),
         ("Content/conversation agent","Approved RAG and draft; no direct dispatch; typed draft and confidence","AG-011/014/018; TL-06 draft only; TL-13 denied",C),
         ("Finance/rules engine","Deterministic calculation and reconciliation; model cannot authorize money","AU-035/037/040; X-06; DEC-064",C),
         ("Orchestrator","Schedule registered step; no arbitrary tools; cannot override policy","M55 engine; AG-039 supervisor + AU-053 plan validator",C),
         ("Reviewer/evaluator","Validate schema, evidence, claims and rubric; route human review","AU-003, AG-012, AG-002, AU-006",C)]
for i,(r,t,l,s) in enumerate(roles):
    a(ch, "V5 role table", f"F15-{8+i:03d}", f"Role class '{r}': {t}", s, l, "Map role class to AG/AU (§11.6.4.3); no change", "—")
a(ch, "V5", "F15-014", "Per-run record: agent identity, prompt/model version, allowed tool set, max tokens/cost, deadline, input/output refs, policy version, quality verdict", P,
  "Part 7.3 §7.6.7 AI decision audit; ai_agent_run; envelope v3 (ADR-114)", "Add allowed_tool_set digest, max_cost_inr, deadline_utc, policy_version, quality_verdict columns (§11.6.5.6); AU-179 writes", "AU-179; FR-V12-F-036")
a(ch, "V5", "F15-015", "External agent interoperability off until validated signed mandate and scoped contract", P,
  "Not in baseline (no external agent interop); CI-list rejects", "Default OFF flag; enable only after CONFLICT-854 decision; AG-104 card gated", "AG-104; CONFLICT-854", PF)

# ---------------- Chapter 16 AI Models, Prompts & Evaluation ----------------
ch = "16 AI Models, Prompts & Evaluation"
a(ch, "V10 REC-12", "F16-001", "REC-12 (P0): bind evaluation and red-team evidence to candidate tier/version, workflow, prompt, language and data class; search all 156 workflows; unrelated evaluation cannot unlock promotion; request only, security and provider approval pending", P,
  "ADR-084; ADR-117 harness v2; AU-006 per agent", "AU-154 composite evidence key; promotion request ≠ activation", "AU-154; DEC-603; TC-V12-F-065")
a(ch, "V10", "F16-002", "Evaluation evidence composite key: candidate ID/version, workflow, prompt version, language, classification, dataset version; plus actual provider, sample size, quality, cost, latency, red-team evidence, separate reviewer, DPA, region", N,
  "ai_eval_run (Part 3.3) keyed by agent + prompt version", "Extend ai_eval_run with workflow_id, language, data_class, dataset_version, provider, sample_n, reviewer_id, dpa_ref, region (§11.6.5.6)", "AU-154; FR-V12-F-032")
a(ch, "V10", "F16-003", "Local fixture passes only validate control logic, not actual model quality; promotion request is distinct from activation", P,
  "Part 6.4 eval cases; WF-21 canary", "Rule in AU-154: fixture-only runs flagged non-gating for quality", "AU-154")
a(ch, "V8", "F16-004", "Controlling AI specification; no provider or model is approved; candidates evaluated under DEC-V7-02", X,
  "DEC-007, DEC-418 (Claude Sonnet primary, Haiku-class lighter tier)", "Raise CONFLICT-850; propose DEC-418 as the answer to DEC-V7-02", "CONFLICT-850; DEC-605", PF)
steps = [("Domain agent","AI inference",159,"Yes","schema; claims registry; citations; EVAL gate; untrusted input cannot invoke tools"),
         ("Domain service","Deterministic domain logic",129,"No","golden fixture exact, zero model calls; invalid state → HELD"),
         ("Rules/analytics engine","Deterministic calculation",53,"No","golden fixture exact; units/denominator validated; no invented value"),
         ("Identity/reconciliation engine","Deterministic identity / reconciliation",42,"No","duplicates per rule; uncertain → REVIEW"),
         ("Policy/validation engine","Policy gate / human review",93,"No","missing consent/entitlement/budget/jurisdiction → HOLD; requester ≠ reviewer"),
         ("Evidence/ingestion engine","Evidence retrieval",25,"No","unauthorised or stale source rejected; provenance hash and rights stored"),
         ("Effect adapter","External effect",16,"No","CJ preflight; idempotency; uncertain → RECONCILING; no effect without approval")]
for i,(e,c,n,m,t) in enumerate(steps):
    a(ch, "16.1", f"F16-{5+i:03d}", f"Step class {c} ({e}): {n} steps; model allowed {m}; test: {t}", P,
      "Part 2.2 §2.6 node types; Tier 0 first (DEC-007); Part 7.2 §7.2.3 AU", "AU-150 step-class registry + CI check; counts adopted literally", "AU-150; DEC-604; TC-V12-F-001")
a(ch, "16.1", "F16-012", "Total 517 steps; 159 AI-inference steps (31%)", N, "—", "Adopted; verified by parser (517 / 159)", "DEC-604")
mdl = [("MDL-R0","Rules engine, no model; arithmetic, dedup, filters, state changes; all classes; approved design pattern",C,"Tier 0 (DEC-007; §7.3.1)"),
       ("MDL-S1","Tier S small/fast, hosted or open-weight; classification, extraction, routing, short drafts; Public, Internal, Personal (masked); IN/EU per tenant; candidate",X,"Tier 1a Claude Haiku-class (§7.3.1); open-weight only Tier 2/2e non-personal"),
       ("MDL-M1","Tier M standard hosted LLM; drafting, summarisation, qualification reasoning; Public, Internal, Personal; IN/EU; candidate",P,"Tier 1b Claude Sonnet (primary, DEC-418)"),
       ("MDL-L1","Tier L advanced hosted LLM; complex research synthesis, proposals, escalations; candidate",X,"No separate tier: Sonnet at higher effort (§7.3.2 rule 2)"),
       ("MDL-E1","Embedding model; RAG indexing and retrieval; Internal, Personal (masked); same region as data; candidate",P,"pgvector + embedding model (Part 3.3; ADR-076)"),
       ("MDL-G1","Safety classifier (moderation/injection) for input and output screening; all classes; same region; candidate",P,"AU-005 heuristics + AG-012 guard + Presidio (AU-004)")]
for i,(m,t,s,l) in enumerate(mdl):
    conf = {"MDL-S1":"CONFLICT-851; CONFLICT-852","MDL-L1":"CONFLICT-853","MDL-E1":"CONFLICT-852","MDL-M1":"CONFLICT-852"}.get(m,"")
    a(ch, "16.2", f"F16-{13+i:03d}", f"{m}: {t}", s, l, f"Map {m} to gateway tier (§11.6.5.3)" + (f"; {conf}" if conf else ""), "DEC-605; ADR-161; AU-151" + (f"; {conf}" if conf else ""), PF if conf else M)
a(ch, "16.2", "F16-019", "Routing: rules first; cheapest tier whose evaluation suite passes for this workflow, language and data class; escalate once within remaining budget; otherwise HOLD for reviewer", P,
  "§7.3.4 R1–R13 (agent-level parity, escalation 1a→1b)", "AU-152 adds workflow × language × data-class eval lookup and single escalation; HOLD replaces Tier 2 when not eligible", "AU-152; DEC-606; TC-V12-F-003")
a(ch, "16.2", "F16-020", "Candidates to evaluate: hosted frontier families (Anthropic Claude, OpenAI GPT, Google Gemini) small/standard/advanced and open-weight (Llama, Mistral, Qwen) self-hosted in region", X,
  "DEC-418 Claude primary; §7.3.3 Tier 2 chain; AU-045 benchmark harness", "Other vendors allowed only as offline benchmark comparators (AI-15/AU-045); CONFLICT-850", "CONFLICT-850", PF)
a(ch, "16.2", "F16-021", "Approval evidence: passing suites (16.4), red-team pass (16.5), signed DPA with no-training clause, retention and region, cost per accepted result, latency p95, security review", P,
  "§7.3.2 verify DPA (GAP-141); AU-044 procurement gate PG-01…10", "AU-151 model registry eligibility requires all 7 evidence items", "AU-151; FR-V12-F-037")
a(ch, "16.2", "F16-022", "Fallback: same output schema, same data region, same or stricter data class; never silently to an unapproved model", X,
  "§7.3.3 Tier 2 free providers (US/EU-hosted, some train on data) default off", "CONFLICT-857: V12 stricter than DEC-418 Tier 2 retention", "CONFLICT-857", PF)
a(ch, "16.2", "F16-023", "Rollback: each workflow pins model and prompt versions; rollback pointer ai_model.rollback_to; kill switch AIX-20", P,
  "ADR-084 re-pin ≤ 5 min; AU-054 auto-rollback; ADR-085 kill switch", "Add workflow-level pin + rollback_to column (§11.6.5.6)", "AU-151; FR-V12-F-038")
a(ch, "16.3", "F16-024", "Prompt ID format PRM-<AGT>-<task>-vN; stored with template hash, output schema ref, locale variants (en, hi; de, fr for EU), approver", N,
  "ai_prompt_version; PC-01…40 contracts", "Adopt PRM IDs as canonical; alias table PC-→PRM (§11.6.5.4)", "DEC-601; AU-153")
a(ch, "16.3", "F16-025", "Prompt structure: fixed policy block (cacheable prefix) → task instruction → typed output schema → delimited untrusted inputs → tenant configuration as typed fields", C,
  "§7.2 cards 'static prefix cached'; ADR-084; §7.6.3 delimiting", "Confirm order; AU-153 lint enforces section order", "AU-153")
a(ch, "16.3", "F16-026", "No tenant data, secrets or personal data inside templates; prompt changes trigger suite replay (AIX-06)", C,
  "§7.6.8; AU-006 on prompt change", "Map; AU-153 static scan", "AU-153; AU-154")
gates = [("Classification / qualification","Precision, recall, F1 per class; calibration error","F1 ≥ 0.90 on labelled set; no class below 0.80","macro-F1 ≥ 0.85; qualification precision ≥ 90% (DEC-001)"),
         ("Extraction","Field-level exact match; schema validity","Exact match ≥ 95%; schema 100%","field accuracy ≥ 95% (≥ 97% payment); schema 99% first pass, 100% after repair"),
         ("Generation","Rubric; claim accuracy vs registry; citation coverage; tone/brand; toxicity","Claims 100%; citations ≥ 95%; rubric ≥ 4/5; toxicity 0","groundedness ≥ 95%; seeded unsupported claims recall ≥ 95%"),
         ("Ranking / recommendation","NDCG@k; coverage","NDCG@10 ≥ agreed baseline","none"),
         ("Translation / localisation","Human adequacy and fluency","≥ 4/5 per language slice","AG-050 back-translation checks (Part 9.7)"),
         ("Adversarial (all)","AI-INJ pass rate; policy violations","0 violations","≥ 98% pass; 0 tool misuse; 0 canary leaks")]
for i,(t,m,g,b) in enumerate(gates):
    a(ch, "16.4", f"F16-{27+i:03d}", f"Gate {t}: metric {m}; proposed gate {g} (owner approval DEC-V7-06)", P,
      f"§7.6.9 thresholds: {b}", "Adopt V12 gate where stricter; keep stricter blueprint gates (§11.6.5.5)", "DEC-602; TC-V12-F-201…311")
a(ch, "16.4", "F16-033", "Suite per workflow EVAL-<workflow ID>; minimum 50 labelled + 20 adversarial cases per AI-inference workflow, sliced by language, sector, channel, edge case; synthetic or lawfully authorised data only", P,
  "§7.6.9 per-agent golden sets (≥ 50 generators, ≥ 100 classifiers, ≥ 200 qualification); GAP-142", "111 EVAL suites registered (§11.6.5.5); cost CONFLICT-855", "DEC-603; AU-154; CONFLICT-855", PF)
a(ch, "16.4", "F16-034", "Labelling: two annotators, adjudication, Cohen's κ ≥ 0.7 before a case enters the gold set", N,
  "AU-078 label queue (single reviewer)", "AU-155 agreement controller", "AU-155; TC-V12-F-066")
a(ch, "16.4", "F16-035", "AI grader: LLM-as-judge only after calibration (AIX-07); otherwise human review", P,
  "§7.6.6 judge human agreement ≥ 85%", "AU-156 κ ≥ 0.8 gate (stricter, adopted)", "AU-156")
a(ch, "16.4", "F16-036", "When run: every model, prompt, retrieval, policy or tool change; nightly drift sample (AIX-18); results stored in eval_run with denominator", P,
  "AU-006 on prompt/model/schema change; AU-057 drift; AU-070 nightly", "Add retrieval, policy and tool changes as triggers; eval_run denominator column", "AU-154; FR-V12-F-033")
a(ch, "16.4", "F16-037", "Suite table columns: Suite, Workflow, SKU, AI steps, Agent, Languages (IN en, hi / EU en, de, fr) — 111 suites", N,
  "—", "Generated table §11.6.5.5 (all 111 rows)", "TC-V12-F-201…311")
a(ch, "16.5", "F16-038", "Principle: content outside approved configuration is data, never instructions; reader steps (untrusted content, no effect tools) vs actor steps (effects on schema-validated fields after policy recheck and approval)", C,
  "§7.6.3; §7.2.4 rule 1; ADR-082", "Map; AIX-09", "—")
inj = [("AI-INJ-01","Scraped web page — hidden instruction text","THR-051; AU-005; §7.6.3 input layer"),
       ("AI-INJ-02","Inbound email — forward records externally","§7.2.4 rule 1 (no tools); egress allowlist (Part 4.1)"),
       ("AI-INJ-03","WhatsApp/SMS reply — change pricing or claims","AG-012 claims guard; VP-01 no-price; reviewer"),
       ("AI-INJ-04","Uploaded document — invisible Unicode/white text","AU-005 hidden-text removal; NFKC not explicit"),
       ("AI-INJ-05","CRM free-text field instruction","§7.6.3 delimiting; schema output"),
       ("AI-INJ-06","Agent-to-agent (SM-SVC-28) — exceed mandate","not in baseline (no agent interop)"),
       ("AI-INJ-07","RAG poisoned document","AU-007 source permission; AU-046; citations BRL-AI-03"),
       ("AI-INJ-08","Tool output containing instructions","envelope v3 (ADR-114) data typing"),
       ("AI-INJ-09","Multilingual payload (Hindi / mixed script)","AG-056 language-switch mutations"),
       ("AI-INJ-10","System prompt extraction","canary strings SC-33; secrets never in prompts §7.6.8"),
       ("AI-INJ-11","Cross-tenant probe","RLS; TL-01 namespace; uniform 404 (FR-ENG-01)"),
       ("AI-INJ-12","Link/image exfiltration via Markdown URL","§7.6.3 URL allowlist; render sanitiser not explicit")]
for i,(t,d,l) in enumerate(inj):
    st = N if t=="AI-INJ-06" else (P if t in ("AI-INJ-04","AI-INJ-12") else C)
    a(ch, "16.5", f"F16-{39+i:03d}", f"{t}: {d}", st, l,
      "Adopt test ID; map to SC-/THR- and corpus family" + ("; AU-169" if st==P else "") + ("; AG-104 gated by CONFLICT-854" if t=="AI-INJ-06" else ""),
      f"TC-V12-F-{21+i:03d}" + ("; AU-169" if st==P else ""), PF if t=="AI-INJ-06" else M)
ctrl = [("CTRL-AI-01 Delimiting","§7.6.3 input layer",C),("CTRL-AI-02 Normalisation (NFKC, zero-width, bidi, hidden text)","AU-005 hidden text only",P),
        ("CTRL-AI-03 Classifier MDL-G1 screens in/out; flags to reviewer","AU-005 + AG-012; flags to R10",P),("CTRL-AI-04 Tool isolation per step class","§7.2.4 rule 1",C),
        ("CTRL-AI-05 Output validation, URL/domain allowlist, sanitised rendering, no auto-fetch","§7.6.4 + §7.6.3",P),("CTRL-AI-06 Secrets never in context; refusal template","§7.6.8; SC-33",C),
        ("CTRL-AI-07 Retrieval filtered by tenant/company before ranking; tenant-scoped vector keys","TL-01 namespace (tenant, startup); SR-04",C),
        ("CTRL-AI-08 Agent-to-agent mandates signed with limits; counterparty messages untrusted","not in baseline",N),
        ("CTRL-AI-09 Logging flags, model, prompt version, decision (PII-redacted)","§7.6.7; AU-105",C)]
for i,(t,l,s) in enumerate(ctrl):
    a(ch, "16.5", f"F16-{51+i:03d}", t, s, l, "Adopt control ID; map" + ("; extend via AU-169/AU-152" if s==P else "") + ("; AG-104 + AU-175, CONFLICT-854" if s==N else ""),
      "FR-V12-F-0%02d; TC-V12-F-0%02d" % (21+i, 33+i), PF if s==N else M)
a(ch, "16.6", "F16-060", "Every factual statement cites an evidence ID from the run's evidence set; uncited facts flagged", C, "BRL-AI-03; §7.6.5 mandatory citations", "Map", "—")
a(ch, "16.6", "F16-061", "Marketing claims matched against tenant approved claims registry; unmatched → REVIEW (AIX-11)", C, "AG-012; TL-09 claims.lookup; CJ-GL-13", "Map", "—")
a(ch, "16.6", "F16-062", "Missing values never invented: INVALID_METRIC / HELD", C, "§7.6.5 numbers from systems; Part 2.2 failure contract", "Map", "—")
a(ch, "16.7", "F16-063", "Metering ai_usage_event per call: tenant, company, run, step, model, prompt version, input/output/cached tokens, latency, outcome", P,
  "ai_usage / ai_cost_ledger (Part 3.3; AU-012)", "Add step_id, workflow_id, cached_tokens, outcome (§11.6.5.6)", "FR-V12-F-030")
a(ch, "16.7", "F16-064", "Cost per accepted result = (model + retrieval + retry + provider) ÷ accepted outputs, per workflow and tenant; rejected outputs in denominator", N,
  "cost per task (§7.2 cards); AU-012", "AU-158 calculator; KPI 'cost per accepted result' [RECOMMENDATION-864]", "AU-158; RECOMMENDATION-864")
a(ch, "16.7", "F16-065", "Budgets: soft cap (default 80%) alerts; hard cap holds new AI steps while deterministic steps continue; caps per tenant, company and workflow (AIX-13)", P,
  "AU-002 (agent, startup, tenant, global); §7.5.7 ladder; DEC-008; B02/B23/B24", "AU-159 adds workflow dimension and 'deterministic continue' rule; DEC-008 ceilings unchanged", "AU-159; DEC-607")
a(ch, "16.7", "F16-066", "Savings levers: rules-first, cheapest passing tier, cached policy prefixes, batch for non-interactive bulk, tenant-scoped semantic cache for non-personal outputs, agent-loop caps", C,
  "§7.4.2 technique catalogue; ADR-076", "Map", "—")
a(ch, "16.7", "F16-067", "Fairness: per-tenant token-rate quotas and weighted queues (AIX-16)", N, "Concurrency caps only (§7.2.9)", "AU-160", "AU-160; ADR-168")
a(ch, "16.7", "F16-068", "Prices: none invented; A117 shows tokens and user-entered illustrative rate until provider prices approved", P,
  "§7.3.2 list prices 'verify'; DEC-418 Claude priced estimates", "Keep blueprint estimates labelled 'verify'; A117 V12 screen shows price version (§11.6.5.7)", "DEC-607")
aix = [("AIX-01","P0","Step classification; only AI-inference steps may call a model","static check fails CI","AU-150",N),
       ("AIX-02","P0","Model registry (tier, provider, version, region, data classes, context, DPA/retention, eval status, rollback)","unregistered/unapproved model cannot be routed","AU-151",P),
       ("AIX-03","P0","Routing Rules → S → M → L → human; cheapest passing tier; one escalation within budget, else hold","cheaper passing tier chosen; failing output escalates once","AU-152",P),
       ("AIX-04","P0","Prompt registry PRM-<AGT>-<task>-vN with schema, policy inputs, locales, approval; no tenant data","run records prompt version; unapproved prompt blocked","AU-153",P),
       ("AIX-05","P0","EVAL-<WF> suite per AI workflow, thresholds owner-approved","suite exists and passes before AI step enabled","AU-154",P),
       ("AIX-06","P0","Regression on any model/prompt/retrieval/policy/tool change; promotion blocked on regression","lower-accuracy prompt cannot be promoted","AU-154",P),
       ("AIX-07","P1","Judge only after κ ≥ 0.8 calibration","uncalibrated grader non-gating","AU-156",P),
       ("AIX-08","P0","Untrusted content isolation","AI-INJ-01…12 zero violations","AU-005; AU-169",C),
       ("AIX-09","P0","Reader/actor separation","injected send/forward cannot cause effect","AU-179",C),
       ("AIX-10","P0","Output handling: schema, URL/egress allowlist, sanitised rendering, no secrets","image-link exfiltration and secret requests blocked","AU-169",P),
       ("AIX-11","P0","Claims and citation control","unapproved claim → REVIEW; uncited fact flagged","AG-012",C),
       ("AIX-12","P0","AI usage metering per call","tenant totals reconcile with provider invoices within tolerance","AU-048",P),
       ("AIX-13","P0","Tenant AI budgets soft/hard per tenant, company, workflow","hard cap → AI step Held, no provider call","AU-159",P),
       ("AIX-14","P1","Cost per accepted result in A117","denominator and rejected outputs shown","AU-158",N),
       ("AIX-15","P1","Prefix caching, batch API, tenant-scoped semantic cache for non-personal","cache key includes tenant and policy version","AU-162; AU-161; AU-164",P),
       ("AIX-16","P1","Fair scheduling quotas and weighted queues","noisy tenant does not raise others' p95","AU-160",N),
       ("AIX-17","P0","Provider data handling: no training, DPA retention/region, minimise/mask for Tier S","provider without DPA cannot be approved","AU-151",P),
       ("AIX-18","P1","Drift monitoring nightly sample","simulated drift triggers alert and rollback option","AU-057",C),
       ("AIX-19","P1","Multilingual coverage en+hi IN; de+fr EU; locale prompts","slice below gate blocks that locale only","AU-154",P),
       ("AIX-20","P0","AI incident response; kill switch per model/prompt/workflow","kill switch stops new calls within one scheduler cycle","AU-025",C)]
for i,(x,p,r,t,au,s) in enumerate(aix):
    extra = "; CONFLICT-852" if x in ("AIX-17","AIX-02") else ""
    a(ch, "16.8", f"F16-{69+i:03d}", f"{x} ({p}) {r}; acceptance: {t}", s,
      {"AIX-08":"§7.6.3; AU-005","AIX-09":"§7.2.4 rule 1","AIX-11":"AG-012; BRL-AI-03","AIX-18":"AU-057; §9.7.4.5","AIX-20":"ADR-085 kill switch ≤ 60 s; §7.6.10"}.get(x, "Part 7.3 §7.3–7.6; Part 9.7 §9.7.4"),
      f"Adopt {x}; implement/extend via {au}", f"{au}; TC-V12-F-{1+i:03d}; FR-V12-F-{1+i:03d}{extra}", M)
a(ch, "16.8", "F16-089", "UI mapping: Admin A114 model registry, A115 evaluation, A116 injection defence, A117 cost per tenant; Website W36 AI transparency; AI-generated samples labelled", X,
  "Blueprint A114–A128 already used by Part 9.7 screens (A114 Orchestration Console, A115 Agent and Prompt Registry, A128 Eval Observatory)", "V12 IDs canonical; content mapped (§11.6.5.7); renumbering of Part 9.7 screens referred to Group G [GAP-859]", "GAP-859; DEC-619")
a(ch, "V5", "F16-090", "Routing and evaluation registry: version capability, price, locale, residency, context, schema, evaluated quality, latency, provider, data classes; choose eligible cheapest quality-adjusted cost on fixed benchmark; escalate once or hold; illustrative rates approve nothing", P,
  "AU-045 matched-sample benchmark; AU-068 cost optimizer", "AU-151 + AU-152 fields", "AU-151; AU-152")
a(ch, "V5 AI-15", "F16-091", "AI-15 (P1) quality-adjusted provider benchmarking: replay fixed eval set, compare cost per accepted result, latency, risk; OPT-TC-AI-15 denominator, rejected results, no promotion below floor", P,
  "AU-045 benchmark harness (Part 7.4)", "AU-045 reports cost per accepted result (AU-158) and denominator", "AU-158; TC-V12-F-067")

# ---------------- Chapter 17 RAG ----------------
ch = "17 RAG, Knowledge & Evidence Engineering"
a(ch, "V8", "F17-001", "Indexes per tenant and region; retrieval filters by tenant and company before similarity ranking (CTRL-AI-07)", P,
  "TL-01 namespace (tenant, startup); single region ap-south-1", "AU-166 pre-filter assertion; region dimension pending CONFLICT-852", "AU-166; CONFLICT-852", PF)
a(ch, "V8", "F17-002", "Each chunk stores source, rights, provenance hash, ingestion time; poisoned/unlicensed sources quarantined (AI-INJ-07)", P,
  "knowledge chunk + AU-007 source rights; AU-046 revocation", "Add rights, provenance_hash, quarantine_state (§11.6.5.8)", "FR-V12-F-031; AU-165")
a(ch, "V8", "F17-003", "Erasure (CJ-R07) deletes source documents, chunks and embeddings with deletion evidence", C, "AU-011 locator; AU-046; AU-112", "Map", "—")
a(ch, "V6 MT-12", "F17-004", "MT-12 (P0): versioned approved claims and knowledge references by offering; revoke stale evidence and scoped cache; MT-TC-MT-12 revoked claim excluded, wrong-offering retrieval denied", P,
  "claims registry (M03), AU-029 expiry, AU-046 purge", "AU-164 offering-scoped invalidation + TC", "AU-164; TC-V12-F-068")
a(ch, "V5", "F17-005", "Cache contract: key by tenant/company, purpose, versioned prompt/model/policy, evidence hashes, normalized input; store validation result, expiry, permitted use, invalidation reason; exact and semantic matches need authorization equivalence; invalidate on deletion, revocation, policy change, rights expiry; prefix caching only with measured billing", P,
  "AU-001 exact key (agent, prompt version, model, input, scope); ADR-076 semantic cache", "AU-164 key extension (purpose, policy version, evidence hashes) and invalidation reasons", "AU-164; ADR-167")
a(ch, "V5 AI-05", "F17-006", "AI-05 (P1) tenant-scoped semantic caching with similarity + exact business constraints; OPT-TC-AI-05 different tenant/revoked source → miss", P, "ADR-076 cosine ≥ 0.92 Public/Internal", "AU-164", "AU-164; TC-V12-F-069")
a(ch, "V5 AI-07", "F17-007", "AI-07 (P1) scoped fact/decision summaries with evidence and corrections; preserve unresolved tasks and consent; OPT-TC-AI-07 bounded prompt, approval and opt-out facts retained", P,
  "conversation memory last 6 turns + summary (ADR-112)", "Pinned-fact rule: approval, opt-out, consent facts never summarized away (AU-163)", "AU-163; TC-V12-F-070")
a(ch, "V5 AI-08", "F17-008", "AI-08 (P1) adaptive RAG: tune top-k and rerank against evaluated relevance; scope before ranking; cite; OPT-TC-AI-08: relevant fixture retrieved within token cap; unrelated or forbidden chunks excluded", P, "TL-01 top-k ≤ 8 fixed", "AU-166 tuner within token cap", "AU-166; TC-V12-F-071")
a(ch, "V5 AI-09", "F17-009", "AI-09 (P1) incremental embedding: hash chunks, re-embed changed only, tombstone removed; OPT-TC-AI-09: one changed chunk triggers one update; deleted evidence no longer retrievable", P, "AU-046 deletes embeddings on revoke", "AU-165", "AU-165; TC-V12-F-072")
a(ch, "V5 CS-02", "F17-010", "CS-02 (P1) searchable help and grounded AI support; cite version; route uncertainty to human; OPT-TC-CS-02: unsupported question escalates; no fabricated claims", C, "AG-031; AG-017; abstention BRL-AI-04", "Map", "TC-V12-F-073")
a(ch, "V5 CS-07", "F17-011", "CS-07 (P1) scoped correction memory with provenance, expiry, revocation; never crosses tenants; OPT-TC-CS-07: correction improves evaluated same-scope fixture; never crosses tenants", P, "AU-078 feedback; ADR-112 memory", "Correction items as procedural memory with expiry (AU-164 invalidation)", "TC-V12-F-074")
a(ch, "V5", "F17-012", "Evidence schema: source_ref, source policy/right, object version, observed_at, fetched_at, hash, quotation/location, confidence, freshness limit", P, "evidence entity (Part 3.3; AG-004 quotes)", "Field mapping §11.6.5.8; add observed_at, freshness_limit", "FR-V12-F-031")
a(ch, "V5", "F17-013", "Ingest only authorised docs; scan, classify, redact restricted content; index scoped by tenant/company/document permission; stale/conflicting claims held; deletion revokes chunks and caches; citations with answers; no cross-tenant embedding retrieval", C,
  "AU-004; AU-007; AU-069; AU-046; TL-01", "Map", "—")

# ---------------- Chapter 18 Policy, Approval & HITL ----------------
ch = "18 Policy, Approval & Human-in-the-Loop Engine"
cmp = [("ENT-CMP-01","P0","SOC 2 Type I at R2 and Type II at R3","AG-075 SOC 2-aligned narratives; no audit commitment"),
       ("ENT-CMP-02","P1","ISO/IEC 27001 certification at R3","AG-075 ISO-mapped controls; no certification"),
       ("ENT-CMP-03","P2","ISO/IEC 27701 and ISO/IEC 42001 at R4","not in baseline"),
       ("ENT-CMP-04","P0","DPA with SCCs, public sub-processor list, 30-day change notice","Part 4.1 vendor register; DPA per tenant (CJ-R17)"),
       ("ENT-CMP-05","P0","DPIA and EU AI Act assessment before EU launch","§7.6.12; DPIA (Part 4.1)"),
       ("ENT-CMP-06","P1","Accessibility conformance report (WCAG 2.2 AA) manual audit","Part 2.5 WCAG 2.2 AA; ACR"),
       ("ENT-CMP-07","P0","Legal document set (Terms, Privacy, DPA, AUP, Cookie, AI Use, Accessibility)","Part 2.4 legal pages"),
       ("ENT-CMP-08","P0","Jurisdiction packs reviewed by counsel before each market","DEC-029 verify with counsel")]
for i,(e,p,r,l) in enumerate(cmp):
    st = {"ENT-CMP-01":X,"ENT-CMP-02":X,"ENT-CMP-03":X}.get(e, C if e in ("ENT-CMP-06","ENT-CMP-07","ENT-CMP-08","ENT-CMP-05") else P)
    a(ch, "V12 compliance", f"F18-{1+i:03d}", f"{e} ({p}): {r}", st, l,
      "Adopt; AI-governance items (42001, AI Act) in §11.6.5.9" + ("; cost CONFLICT-856" if st==X else ""), "DEC-618" + ("; CONFLICT-856" if st==X else ""), PF if st==X else M)
jp = [("CJ-US-02","US Email CAN-SPAM"),("CJ-US-03","US SMS/Voice TCPA consent, 8am–9pm, DNC"),("CJ-US-04","US state privacy CCPA/CPRA incl. GPC"),
      ("CJ-UK-02","UK PECR consent/soft opt-in"),("CJ-UK-03","UK GDPR DSAR 1 month; ICO 72 h"),("CJ-CA-01","CA CASL consent, unsubscribe 10 business days"),
      ("CJ-AU-01","AU Spam Act consent, unsubscribe 5 business days, DNC Register"),("CJ-SG-01","SG DNC Registry, PDPA, unsubscribe"),
      ("CJ-AE-01","AE PDPL lawful basis, rights, transfers"),("CJ-BR-01","BR LGPD legal basis, rights, ANPD breach")]
for i,(j,d) in enumerate(jp):
    a(ch, "V12 packs", f"F18-{9+i:03d}", f"{j}: {d}; status Draft · disabled until counsel review", P if j[:5] in ("CJ-US","CJ-UK","CJ-AU","CJ-SG","CJ-AE") else N,
      "DEC-029 Year-1 allowlist (EU/UK, US, UAE/SG/AU enabled after counsel)", "Add as Draft pack rows; disabled by AU-170 until Approved; amends DEC-029", "AU-170; DEC-611")
a(ch, "V10 REC-03", "F18-019", "REC-03 (P0): group competing actions by relationship and purpose; hold duplicates; reviewer disposition; opt-out and budget override", P, "AU-030 conflict resolution by priority", "AU-176", "AU-176; TC-V12-F-075")
a(ch, "V10 REC-10", "F18-020", "REC-10 (P0): consent withdrawal matched by contact, channel, purpose, market; unrelated purposes unaffected; missing scope fails closed", P, "AU-008 STOP scope; consent model Part 2.4", "AU-172 scoped suppression", "AU-172; TC-V12-F-076")
a(ch, "V10 REC-11", "F18-021", "REC-11 (P0): all dispatch invokes canonical effect preflight (scope, consent, configuration, entitlement, cap, approval, duplicates); missing evidence/stale approval/withdrawn consent/unknown jurisdiction/paused tenant holds", C, "AU-009 PDP dispatch guard", "Map; AU-171 decision table", "AU-171")
a(ch, "V10", "F18-022", "Canonical effect contract: immutable intent (tenant, company, recipient, relationship, purpose, market, channel, config version, payload digest, consent version, reviewer, expiry, budget, idempotency key); atomic re-read; missing → HOLD; unknown write → reconcile", P, "outbox intent + approved hash (CA-APPROVE); AU-026", "Add consent_version, config_version, relationship, expiry fields (§11.6.5.10)", "AU-175; FR-V12-F-034")
gl = [("CJ-GL-01","legitimate published professional channels only; no guessed/pattern emails","X-05; AU-018; BR-M18",C),
      ("CJ-GL-02","verified contact is not consent","BRL (score ≠ permission); AU-009",C),
      ("CJ-GL-03","deletion/correction never re-enables outreach; hashed suppression survives erasure","DEC-028 suppression indefinite hashed",C),
      ("CJ-GL-04","planned/unavailable offerings cannot be promoted, matched or quoted","AU-016 readiness; AU-043",C),
      ("CJ-GL-05","STOP/opt-out/reply cancels scoped follow-ups across linked channels","AU-008; AU-022",C),
      ("CJ-GL-06","urgent/clinical enquiries to human; no medical advice","AG-013 urgent/clinical; X-02",C),
      ("CJ-GL-07","no health targeting, no health events to pixels, no medical data in scoring","X-02; BR-M50",C),
      ("CJ-GL-08","no private-group scraping, restricted profiles or automated DMs","X-05",C),
      ("CJ-GL-09","complaints above threshold pause campaign","AU-031",C),
      ("CJ-GL-10","no automatic re-contact after lost deal without policy","BR-M51; AG-038",C),
      ("CJ-GL-11","referral/partner leads need own basis","BR-M42; AU-020",C),
      ("CJ-GL-12","AI never signs; only approved versions shared; signed hash stored","X-06; AU-036",C),
      ("CJ-GL-13","no fabricated rankings/comparisons; forecasts labelled estimates","AU-033; AU-041; AG-012",C)]
for i,(g,d,l,s) in enumerate(gl):
    a(ch, "V9 CJ-GL", f"F18-{23+i:03d}", f"{g}: {d}; non-relaxable by tenant", s, l, "Adopt ID as platform rule above tenant config; map to BR/BRL (§11.6.5.10)", "DEC-612; AU-171")
pf9 = ["Contact source guessed/private → HOLD CJ-GL-01","Verified contact only → HOLD CJ-GL-02","Previously erased/suppressed → HOLD CJ-GL-03","Offering planned/unavailable → HOLD CJ-GL-04",
       "STOP/opt-out/reply received → HOLD CJ-GL-05","Health attributes in targeting → HOLD CJ-GL-07","Urgent/clinical enquiry → REVIEW CJ-GL-06"]
for i,t in enumerate(pf9):
    a(ch, "V9 preflight", f"F18-{36+i:03d}", f"Preflight input: {t}", C, "AU-009 PDP checks", "Encode row in AU-171 decision table", "AU-171; TC-V12-F-0%02d" % (77+i))
a(ch, "V8", "F18-043", "Launch jurisdictions India (primary) and EU (recommended second, DEC-V7-01); UK/US disabled drafts; rules as configuration; unreviewed rules default to stricter (CJ-R20); not legal advice", P,
  "DEC-029 (India, EU/UK, US, UAE/SG/AU)", "Adopt; DEC-611 amends DEC-029; EU launch remains a Founder/legal decision (CONFLICT-852 for AI region)", "DEC-611; AU-170")
inr = ["CJ-IN-01 DPDP consent free/specific/informed + itemised notice","CJ-IN-02 withdrawal as easy as consent; stop within period","CJ-IN-03 children <18 parental consent; no tracking/targeting",
       "CJ-IN-04 breach intimation to Board and principals","CJ-IN-05 data-principal rights incl. nomination","CJ-IN-06 TRAI DLT entity/header/template; scrub; time window",
       "CJ-IN-07 140-series promotional / 160-series service calls","CJ-IN-08 WhatsApp opt-in, templates, service window","CJ-IN-09 CERT-In 6 h; logs 180 days",
       "CJ-IN-10 GST; e-invoice IRN","CJ-IN-11 DPDP s.16 cross-border transfer"]
inloc = ["Part 4.1 DPDP; consent ledger","AU-008; DEC-028","DEC-030 no outreach to minors","Part 4.1 DP-R6; RB-008","Part 4.1; AU-112","DEC-029 TRAI; DLT partial (no voice/SMS channel in baseline)",
         "not in baseline (no voice channel)","AU-073; DEC-029 no WhatsApp cold outreach","Part 4.1 CERT-In 6 h","DEC-027 GST; L-01 IRN W6+","§7.6.8 disclose processing outside India"]
for i,(t,l) in enumerate(zip(inr,inloc)):
    st = N if "CJ-IN-07" in t else (P if any(k in t for k in ("CJ-IN-06","CJ-IN-11")) else C)
    a(ch, "18.1", f"F18-{44+i:03d}", t + "; status pending qualified legal review", st, l,
      "Adopt rule ID into IN pack (AU-170)" + ("; AU-173" if any(k in t for k in ("CJ-IN-06","CJ-IN-07")) else "") + ("; CONFLICT-852" if "CJ-IN-11" in t else ""),
      "AU-170" + ("; AU-173" if any(k in t for k in ("CJ-IN-06","CJ-IN-07")) else ""), M)
eur = ["CJ-EU-01 documented lawful basis per purpose","CJ-EU-02 ePrivacy consent/soft opt-in; opt-out each message","CJ-EU-03 objection to direct marketing absolute",
       "CJ-EU-04 DSAR one month (+2)","CJ-EU-05 72 h authority notification","CJ-EU-06 Art. 22 safeguards; DPIA for profiling","CJ-EU-07 Chapter V transfers (SCC)",
       "CJ-EU-08 cookie consent before non-essential tracking","CJ-EU-09 AI Act Art. 50 disclosure and machine-readable marking","CJ-EU-10 VAT OSS / reverse charge",
       "CJ-UK-01 UK pack draft/disabled","CJ-US-01 US pack draft/disabled"]
for i,t in enumerate(eur):
    st = C if any(k in t for k in ("EU-01","EU-03","EU-04","EU-05","EU-08")) else P
    a(ch, "18.1", f"F18-{55+i:03d}", t, st, "DEC-029 EU/UK B2B rules; §7.6.12 AI Act; Part 4.1 GDPR",
      "Adopt rule ID into pack (AU-170)" + ("; AU-177" if "EU-09" in t else "") + ("; CJ-R14 human review" if "EU-06" in t else ""), "AU-170" + ("; AU-177" if "EU-09" in t else ""))
pf8 = ["Consent withdrawn/objection → HOLD (IN, EU)","Promotional, consent ≠ express (IN) → HOLD","SMS/Voice DLT not registered → HOLD","Promotional SMS/Voice not scrubbed → HOLD",
       "Promotional SMS/Voice outside window (default 09:00–21:00) → HOLD","WhatsApp business-initiated without opt-in → HOLD","Promotional targeting of known minor → HOLD",
       "Promotional targeting, age unknown → REVIEW","Promotional voice → 140-series pool INFO","EU email/SMS without consent or soft opt-in → HOLD","EU soft opt-in → opt-out link INFO",
       "EU voice/WhatsApp → member-state REVIEW","AI content/agent not disclosed → HOLD (EU) / REVIEW (IN)"]
for i,t in enumerate(pf8):
    a(ch, "18.2", f"F18-{67+i:03d}", f"Send preflight case {i+1}: {t}", P if any(k in t for k in ("DLT","scrubbed","window","140","disclosed","voice/WhatsApp")) else C,
      "AU-009 PDP; DEC-029; DEC-030", "Encode in AU-171 (13 cases, reason codes)", "AU-171; TC-V12-F-%03d" % (84+i))
a(ch, "18.2", "F18-080", "Preflight called by every effect adapter step and A118; effect.preflight_verdict must be ALLOW", C, "AU-009 every external side effect", "Add preflight_verdict column", "AU-171")
a(ch, "18.2", "F18-081", "Policy precedence: emergency stop > revocation/suppression > jurisdiction pack > tenant cap > action grant (CJ-R03)", P, "PDP order (Part 2.3/2.4) not stated as a total order", "Adopt total order in AU-171", "AU-171; DEC-613")
dsr = [("Consent capture","Granted → Withdrawn/Expired append-only; notice version, timestamp, source, evidence hash",C),
       ("Withdrawal/objection","Requested → Suppressed → Runs held; IN configured period, EU immediate",P),
       ("DSAR","Received → Identity verified → In progress → Completed/Refused; EU 1 month (+2)",C),
       ("Breach","Detected → Assessed → Notified → Closed; CERT-In 6 h; GDPR 72 h; DPDP per Rules",P)]
for i,(p_,d,s) in enumerate(dsr):
    a(ch, "18.3", f"F18-{82+i:03d}", f"{p_}: {d}", s, "Part 2.3 state machines; AU-112; Part 4.1", "Map; AU-172/AU-174 timers", "AU-172; AU-174")
cjr = [("CJ-R01","Jurisdiction pack entity; only Approved packs enforced; history immutable",P,"AU-170"),("CJ-R02","Send preflight at effect time with 13 cases",P,"AU-171"),
       ("CJ-R03","Policy precedence",P,"AU-171"),("CJ-R04","Consent ledger purpose/channel/market, append-only",C,"AU-172"),("CJ-R05","Withdrawal → suppression; queued runs Held",P,"AU-172"),
       ("CJ-R06","DLT and preference registry (IN)",N,"AU-173"),("CJ-R07","DSAR workflow",C,"AU-174"),("CJ-R08","Breach and incident clocks",P,"AU-174"),
       ("CJ-R09","Data residency and region pinning IN or EU",X,"CONFLICT-852"),("CJ-R10","Children's data",C,"—"),("CJ-R11","Retention schedule",C,"—"),
       ("CJ-R12","Cookie consent",C,"—"),("CJ-R13","AI disclosure and content marking",P,"AU-177"),("CJ-R14","Automated decision safeguards; DPIA",C,"—"),
       ("CJ-R15","Transfer register",P,"AU-151"),("CJ-R16","Tax configuration",C,"—"),("CJ-R17","Controller/processor role mapping; DPA accepted before outbound",C,"—"),
       ("CJ-R18","Privacy notices versioned",C,"—"),("CJ-R19","Additional jurisdictions by configuration",P,"AU-170"),("CJ-R20","Unverified rule → stricter outcome",N,"AU-170")]
for i,(r,d,s,au) in enumerate(cjr):
    a(ch, "18.4", f"F18-{86+i:03d}", f"{r}: {d}", s, "Part 4.1; DEC-028/029/030; Part 2.4 §2.35", f"Adopt {r}; {au}", f"{au}; TC-V12-F-{97+i:03d}", PF if s==X else M)
a(ch, "18.4", "F18-106", "UI mapping Admin A118–A121; Website W30, W35, cookie banner", X, "Blueprint A118–A121 used by Part 9.7 screens", "GAP-859 referral to Group G", "GAP-859; DEC-619")
a(ch, "V7 MOB-09", "F18-107", "MOB-09 sensitive approvals on mobile: same verified actor, entitlement, scope, payload version, spend limits; no approval from a notification; step-up auth", C, "CA-APPROVE; step-up (Part 4.1); DEC-043 PWA", "Map; AU-175", "AU-175")
a(ch, "V6", "F18-108", "Configuration and effect approval: draft graph base version, diff, requester; reviewer ≠ requester; approval binds exact version and scope; reject stale; revoke on suspension; rollback as new revision; recheck at effect", C, "DEC-051; CA-APPROVE; BRL-AUT", "Map; AU-175", "AU-175")
for i,(m,d) in enumerate([("MT-15","Offering lifecycle draft/pilot/active/suspended/retired; live effect gate"),("MT-20","Jurisdiction policy profiles; unknown policy holds effects"),
                           ("MT-24","Unified consent, suppression, frequency ledger at effect time"),("MT-32","Configuration change approval and rollback; no stale approval")]):
    a(ch, "V6", f"F18-{109+i:03d}", f"{m}: {d}", C if m in ("MT-15","MT-32") else P, "AU-043; DEC-029; AU-008/AU-009; DEC-051",
      "Map" + ("; AU-170" if m=="MT-20" else "") + ("; AU-172" if m=="MT-24" else ""), "TC-V12-F-%03d" % (117+i))
a(ch, "V5 SEC-07", "F18-113", "SEC-07 (P0) AI tool permission gateway: typed authorized tool ops; independent recheck at execution; disallowed tool denied despite prompt", C, "§7.2.4 tool executor; R20", "Map", "TC-V12-F-121")
a(ch, "V5 FL-09", "F18-114", "FL-09 (P0) persistent approval mandates binding actor, resource, digest, action, amount, policy, expiry, revocation; changed payload/expired/revoked blocks", X, "Approved hash per item (CA-APPROVE); DEC-064 L1 cap", "CONFLICT-854; AU-175 mandate table limited to R2 bounded mandates", "CONFLICT-854; AU-175", PF)
for i,(r,d,s) in enumerate([("R0","Read/draft with source rights; no external action",C),("R1","Scoped internal record update; version lock and audit",C),
                              ("R2","External write: explicit approval or eligible bounded mandate",P),("R3","Financial/legal/commitment: exact approval + finance/legal gate; mandate only if expressly approved",X)]):
    a(ch, "V5 effect classes", f"F18-{115+i:03d}", f"Effect class {r}: {d}", s, "TL side-effect classes R0/W1/X2 (§7.2.4); DEC-064", "Map R-classes to TL classes (§11.6.5.10)" + ("; CONFLICT-854" if s==X else ""), "DEC-614" + ("; CONFLICT-854" if s==X else ""), PF if s==X else M)
a(ch, "V5", "F18-119", "Approval record binds tenant/company, workflow version, action digest, recipient, budget, currency, actor authority, expiry, policy version; prepare/approve/execute/reconcile; recheck before adapter; emergency stop; cancellation never hides completed action", P, "CA-APPROVE; AU-009; AU-026; AU-025", "AU-175 record fields", "AU-175; FR-V12-F-035")

# ---------------- Chapter 30 AI Cost & Performance ----------------
ch = "30 AI Cost & Performance Optimization"
a(ch, "V7 MOB-13", "F30-001", "MOB-13 mobile performance and cost: code splitting, cached assets, optimized images, paginated data, debounced requests; one backend/AI router; LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 p75 (measure before commitment)", C, "NFR (Part 4.2) Core Web Vitals; DEC-043 PWA", "Map (frontend aspects owned by Group G)", "—")
a(ch, "V6", "F30-002", "Continuous redundancy and cost controls: MT-33–40 + AI/GC/FL; measure duplicate definitions, stale deps, cache reuse, accepted-result cost, per-tenant expense; retain approved redundancy; 156/39 references traceable", P, "AU-068; AU-117; AU-118", "AU-178", "AU-178")
a(ch, "V6 MT-40", "F30-003", "MT-40 (P1) continuous redundancy, dependency and cost auditing; MT-TC-MT-40 CI duplicate-ID scan, cost benchmark, dependency audit", P, "AU-013 ID lint; AU-047; AU-118", "AU-178", "AU-178; TC-V12-F-122")
a(ch, "V5", "F30-004", "AI FinOps: actual cost per accepted result and per workflow from receipts + compute, retries, retrieval, media, human review; raw unit and price version; unallocated shown; compare to pilot baseline; laboratory proves nothing", P, "AU-012; AU-048; AU-049", "AU-158 incl. human review minutes and price_version", "AU-158; DEC-608")
aiq = [("AI-01","P0","Deterministic-first execution; golden fixtures zero model calls",C,"Tier 0 (DEC-007); AU-001","AU-150"),
       ("AI-02","P0","Multi-tier model router: cheapest eligible evaluated model subject to latency and policy",P,"§7.3.4","AU-152"),
       ("AI-03","P0","Conditional escalation once within remaining budget; else hold without external effect",P,"§7.3.4 R8","AU-152"),
       ("AI-04","P1","Prompt prefix caching; record provider hit/miss and billed tokens; never assume support",P,"§7.4.2 prompt caching","AU-162"),
       ("AI-06","P0","Dynamic context budgeting; reserve output and safety margin; trim irrelevant evidence",P,"§7.2 cards token caps","AU-163"),
       ("AI-10","P1","Asynchronous batching by compatible model and scope; deadline, cancellation, unit price",P,"Batch API use per card","AU-161"),
       ("AI-11","P1","Shared research artifact reuse via authorized references",P,"AU-014 content-hash dedupe; AG-040 brief","AU-167"),
       ("AI-13","P1","Multimodal cost tiers: thumbnail/text/transcript first",N,"not in baseline","AU-168")]
for i,(x,p,d,s,l,au) in enumerate(aiq):
    acc = {"AI-01":"golden deterministic fixtures yield exact results with zero model calls","AI-02":"given two eligible models select lowest accepted-result cost; reject model below quality floor",
           "AI-03":"low-quality draft escalates once if budget permits; otherwise hold without external effect","AI-04":"repeated identical approved prefix records measured cache hit or explicit unsupported state",
           "AI-06":"oversized context reduced or held; mandatory evidence retained and cap respected","AI-10":"batch results correlate to each job; expired or incompatible jobs stay separate",
           "AI-11":"two entitled workflows reuse current permitted evidence; stale evidence refreshed or held","AI-13":"preview meets acceptance without full rendering; failure escalates within cap only"}[x]
    a(ch, "V5", f"F30-{5+i:03d}", f"{x} ({p}) {d}; OPT-TC-{x}: {acc}", s, l, f"Adopt; {au}", f"{au}; TC-V12-F-{123+i:03d}")
a(ch, "V5", "F30-013", "Per-run budget reserve before execution; meter model input/output/reasoning, embeddings, tool calls, retries, storage, provider fees, labour; cache only scoped permitted inputs; batch low-risk; cheapest evaluated model; cap context/tool calls; no quality regression for cost; record cost per accepted result", P, "AU-002 reservation; AU-012", "AU-158/159; reasoning tokens metered as output (§7.3.2 rule 2)", "AU-158; AU-159")

# ---------------- other chapters referencing AGT / EVAL ----------------
a("01 Specification Control Reading Guide", "ID families", "F01-001", "ID index: 20 agents (AGT-01…AGT-20), ch15", N, "—", "Adopted (§11.6.4.1)", "DEC-600")
a("AP Appendix D ID index", "ID index", "FAD-001", "AGT-01…20 listed in Appendix D ID index", N, "—", "Adopted (§11.6.4.1)", "DEC-600")
a("40 Master Traceability", "V8 register", "F40-001", "Master traceability register columns Workflow, SKU, Steps (AI n), Engine, Agent, UI, API, DB, Policy (POL-V6-PRECHECK; CJ preflight on 15 rows), Tests (TC-*; EVAL-*) — 156 rows", N, "Part 6.6 RTM (blueprint IDs)", "F-scope columns (engine, agent, steps, EVAL) reconciled per row in §11.6.4.2; UI/API/DB columns owned by Groups G/H/I", "DEC-600")
a("40 Master Traceability", "V7 decisions", "F40-002", "DEC-V7-02 AI providers and models per tier — Open", X, "DEC-418", "Answered by DEC-418, pending Founder confirmation (CONFLICT-850)", "CONFLICT-850", PF)
a("40 Master Traceability", "V7 decisions", "F40-003", "DEC-V7-06 Evaluation thresholds need owner approval per workflow — Open", P, "§7.6.9", "DEC-602 adopts V12 gates as defaults; per-workflow owner sign-off recorded in AU-154", "DEC-602")
a("40 Master Traceability", "V7 decisions", "F40-004", "DEC-V7-07 Tenant AI budget defaults: soft 80%, hard per plan, units in tokens until prices approved — Open", P, "DEC-008; DEC-047 AI tasks", "DEC-607", "DEC-607")
