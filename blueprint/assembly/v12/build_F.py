"""Builds Group F (R5) generated fragments and the coverage CSV.
Run: python3 -I build_F.py  (reads parsed JSON written by parse_F_agents.py)"""
import json, csv, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import F_aspects_text as T, F_wfmap as WM, F_cards as CD, F_au as AUD
BP = os.path.abspath(os.path.join(HERE, "..", ".."))
FSD = "/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad/v12/FSD/"
OUT = os.path.join(HERE, "F_frag"); os.makedirs(OUT, exist_ok=True)
agents = json.load(open(os.path.join(HERE, "F_agents.json")))
rows = json.load(open(os.path.join(HERE, "F_rows.json")))
names = json.load(open(os.path.join(HERE, "F_wfnames.json")))
trace = {r[0]: r for r in rows["trace"]}
evals = rows["eval"]
M, PF = "Matched", "Pending Founder decision"
def w(name, s): open(os.path.join(OUT, name), "w").write(s)
def esc(s): return str(s).replace("|", "/").replace("\n", " ")

# ---------- workflow binding aspects ----------
wf_aspects = []
for wf, tr in trace.items():
    sb, bl, new, note = WM.W[wf]
    ai = re.search(r"AI (\d+)", tr[2]).group(1)
    sa = PF if "CONFLICT-854" in new else M
    if sb == "Covered":
        act = "Bind V12 workflow to AGT role and blueprint implementers (§11.6.4.4)"
    elif "GAP-858" in new:
        act = "Adopt V12 step class (0 AI steps); re-bind blueprint agent; GAP-858 to confirm"
    elif ai == "0":
        act = "Bind with model calls = 0 (AU-150, AU-179); deterministic logic per Groups C/D"
    else:
        act = "Enhance: " + ("new agent card " if "AG-1" in new else "task extension ") + new
    summ = f"{wf} {names[wf]} → {tr[4]}; {tr[2]} steps; engine {tr[3]}; policy {tr[8]}; tests {tr[9]}" + (f"; note: {note}" if note else "")
    wf_aspects.append(("FSD V12", "15 AI Agent Registry + 40 Master Traceability", "AGT registry / V8 traceability row", f"F15-WF-{wf[3:]}", summ, sb, bl if bl != "—" else "—", act, (new + "; DEC-600").strip("; "), sa))

# ---------- AGT aspects ----------
agt_impl = collections.OrderedDict()
for wf, tr in trace.items():
    ag = tr[4]; sb, bl, new, note = WM.W[wf]
    ids = set(re.findall(r"A[GU]-\d{3}", bl + " " + new))
    agt_impl.setdefault(ag, set()).update(ids)
agt_aspects = []
for k, a in agents.items():
    impl = sorted(agt_impl[k])
    ags = [x for x in impl if x.startswith("AG")]; aus = [x for x in impl if x.startswith("AU")]
    newag = [x for x in ags if int(x[3:]) >= 100]
    sb = "Partially covered" if any(WM.W[wf][0] != "Covered" for wf, tr in trace.items() if tr[4] == k) else "Covered"
    act = "Adopt AGT role as canonical; implemented by " + ", ".join(ags) + ("; RECOMMENDATION-860 sub-role prompts" if k == "AGT-20" else "")
    agt_aspects.append(("FSD V12", "15 AI Agent Registry & Orchestration", "V8 AGT table", f"F15-{k}", f"{k} {a['role']}: {a['wf_count']} workflows ({', '.join(a['svcs'])}); allowed: {a['allowed']}; never: {a['never']}", sb,
                        "Part 9.4 §9.4.3: " + ", ".join([x for x in ags if int(x[3:]) < 100]) or "—", act, "DEC-600; AU-179" + ("; " + ", ".join(newag) if newag else "") + ("; RECOMMENDATION-860" if k == "AGT-20" else ""), M))

# ---------- EVAL aspects ----------
eval_aspects = []
for i, e in enumerate(evals):
    suite, nm, sku, ai, ag, lang = e[:6]
    wf = suite[5:]; sb, bl, new, note = WM.W[wf]
    impl = [x for x in re.findall(r"AG-\d{3}", bl + " " + new)]
    sa = PF if "CONFLICT-854" in new else M
    eval_aspects.append(("FSD V12", "16 AI Models, Prompts & Evaluation", "16.4 suite table", f"F16-{suite}", f"{suite} {nm}; {sku}; AI steps {ai}; {ag}; languages {lang}", "Partially covered" if impl and sb != "Not covered" else "Not covered",
                         "Per-agent eval sets §7.6.9 / AU-006: " + (", ".join(dict.fromkeys(impl)) or "none"), "Register EVAL suite bound to implementing agent(s); gates §11.6.5.5; min 50 + 20 cases; κ ≥ 0.7",
                         f"TC-V12-F-{201+i:03d}; AU-154; DEC-603; CONFLICT-855", PF if sa == PF else M))

ALL = T.A + agt_aspects + wf_aspects + eval_aspects
ids = [a[3] for a in ALL]; assert len(ids) == len(set(ids)), [i for i, c in collections.Counter(ids).items() if c > 1]
# CSV
os.makedirs(os.path.join(BP, "final", "coverage_v12"), exist_ok=True)
with open(os.path.join(BP, "final", "coverage_v12", "F_coverage.csv"), "w", newline="") as f:
    cw = csv.writer(f); cw.writerow(["doc", "chapter", "section", "aspect_id", "aspect_summary", "status_before", "blueprint_location", "action", "new_ids", "status_after"])
    for a in ALL: cw.writerow(a)

# ---------- 11.6.1 material ----------
mat = [("14_Shared_AI_Automation_Engines.txt", "V6 redundancy + MT-34; V5 FL-04; ENG-01…15 table"),
       ("15_AI_Agent_Registry_Orchestration.txt", "V8 AGT-01…20 registry; V6 MT-35; V5 AI-12, role table, per-run record"),
       ("16_AI_Models_Prompts_Evaluation.txt", "V10 REC-12; V8 16.1–16.8 (step classes, MDL registry, PRM, gates, 111 EVAL suites, AI-INJ, CTRL-AI, claims, cost, AIX-01…20); V5 AI-15"),
       ("17_RAG_Knowledge_Evidence_Engineering.txt", "V8 RAG addendum; V6 MT-12; V5 cache contract, AI-05/07/08/09, CS-02/07, evidence schema"),
       ("18_Policy_Approval_Human_in_the_Loop_Engin.txt", "V12 ENT-CMP + 10 draft packs; V10 REC-03/10/11; V9 CJ-GL-01…13; V8 18.1–18.4 (CJ-IN/EU, preflight, consent, CJ-R01…20); V7 MOB-09; V6 MT-15/20/24/32; V5 SEC-07, FL-09, R0–R3"),
       ("30_AI_Cost_Performance_Optimization.txt", "V7 MOB-13; V6 MT-40; V5 AI FinOps, AI-01/02/03/04/06/10/11/13")]
by_ch = collections.Counter()
for a in ALL: by_ch[a[1][:2]] += 1
lines = ["| File | Size (bytes) | Lines | Version sections and pattern | Aspects |", "|---|---|---|---|---|"]
for fn, desc in mat:
    p = FSD + fn; n = sum(1 for _ in open(p)); b = os.path.getsize(p)
    lines.append(f"| `FSD/{fn}` | {b:,} | {n:,} | {desc} | {by_ch[fn[:2]]} |")
for fn, desc, cnt in [("40_Master_Traceability_Decision_Register_S.txt", "V8 master traceability register: 156 rows parsed (Engine, Agent, Steps, Tests columns); V7 decisions DEC-V7-02/06/07", sum(1 for a in ALL if a[3].startswith("F40-")) + 156),
                      ("01_Specification_Control_Reading_Guide.txt", "ID family line 693: 20 agents AGT-01…AGT-20", 1), ("AP_Appendix_D_ID_index.txt", "AGT-01…20 index entry", 1)]:
    p = FSD + fn; n = sum(1 for _ in open(p)); b = os.path.getsize(p)
    lines.append(f"| `FSD/{fn}` (AGT/EVAL rows only) | {b:,} | {n:,} | {desc} | {cnt} |")
w("t_material.md", "\n".join(lines) + "\n")

# ---------- 11.6.2 summary ----------
def grp(a):
    c = a[1]
    if a[3].startswith("F15-WF"): return "AGT workflow bindings (ch15 + ch40, 156 rows)"
    if a[3].startswith("F15-AGT"): return "AGT roles (ch15, 20 rows)"
    if a[3].startswith("F16-EVAL"): return "EVAL suites (ch16.4, 111 rows)"
    return c
order = ["14 Shared AI & Automation Engines", "15 AI Agent Registry & Orchestration", "AGT roles (ch15, 20 rows)", "AGT workflow bindings (ch15 + ch40, 156 rows)",
         "16 AI Models, Prompts & Evaluation", "EVAL suites (ch16.4, 111 rows)", "17 RAG, Knowledge & Evidence Engineering", "18 Policy, Approval & Human-in-the-Loop Engine",
         "30 AI Cost & Performance Optimization", "40 Master Traceability", "01 Specification Control Reading Guide", "AP Appendix D ID index"]
cnt = collections.defaultdict(collections.Counter)
for a in ALL: cnt[grp(a)][a[5]] += 1; cnt[grp(a)]["after_" + a[9]] += 1; cnt[grp(a)]["n"] += 1
L = ["| Aspect group | Aspects | Covered | Partially covered | Not covered | Conflict | After: Matched | After: Pending Founder decision |", "|---|---|---|---|---|---|---|---|"]
tot = collections.Counter()
for g in order:
    c = cnt[g]; tot.update(c)
    L.append(f"| {g} | {c['n']} | {c['Covered']} | {c['Partially covered']} | {c['Not covered']} | {c['Conflict']} | {c['after_'+M]} | {c['after_'+PF]} |")
L.append(f"| **Total** | **{tot['n']}** | **{tot['Covered']}** | **{tot['Partially covered']}** | **{tot['Not covered']}** | **{tot['Conflict']}** | **{tot['after_'+M]}** | **{tot['after_'+PF]}** |")
w("t_summary.md", "\n".join(L) + "\n")
json.dump(dict(tot), open(os.path.join(OUT, "totals.json"), "w"))

# ---------- 11.6.3 detailed register ----------
L = ["| Aspect | Chapter · section | V12 aspect (summary) | Status before | Blueprint location | Action | New / mapped IDs | Status after |", "|---|---|---|---|---|---|---|---|"]
for a in T.A + agt_aspects:
    if a[5] != "Covered":
        L.append(f"| {a[3]} | {esc(a[1][:2])} · {esc(a[2])} | {esc(a[4])} | {a[5]} | {esc(a[6])} | {esc(a[7])} | {esc(a[8])} | {a[9]} |")
w("t_register.md", "\n".join(L) + "\n")
cov = collections.defaultdict(list)
for a in T.A + agt_aspects:
    if a[5] == "Covered": cov[a[1]].append(a[3])
L = ["| Chapter | Covered aspects (grouped; each mapped to its blueprint location in the CSV) | Count |", "|---|---|---|"]
for k, v in cov.items(): L.append(f"| {k} | {', '.join(v)} | {len(v)} |")
w("t_covered.md", "\n".join(L) + "\n")

# ---------- 11.6.4.1 AGT registry ----------
L = ["| AGT | Role (V12) | Workflows | Services | AI steps | Engines (ch40) | EVAL suites | Blueprint implementers (AG) | Deterministic implementers (AU) | Status before → after |", "|---|---|---|---|---|---|---|---|---|---|"]
for k, a in agents.items():
    impl = sorted(agt_impl[k]); ags = ", ".join(x for x in impl if x.startswith("AG")); aus = ", ".join(x for x in impl if x.startswith("AU"))
    sb = next(x[5] for x in agt_aspects if x[3] == f"F15-{k}")
    L.append(f"| {k} | {a['role']} | {a['wf_count']} | {', '.join(s.replace('SM-SVC-','') for s in a['svcs'])} | {a['ai_steps']} | {'; '.join(a['engines'])} | {len(a['eval'])} | {ags} | {aus} | {sb} → Matched |")
w("t_agt.md", "\n".join(L) + "\n")

# ---------- 11.6.4.2 workflow binding ----------
L = ["| V12 workflow | Name | AGT | Steps | Engine | EVAL suite | Blueprint implementers | Status before | V12 enhancement | After |", "|---|---|---|---|---|---|---|---|---|---|"]
evset = {e[0][5:] for e in evals}
for wf, tr in trace.items():
    sb, bl, new, note = WM.W[wf]
    sa = PF if "CONFLICT-854" in new else M
    L.append(f"| {wf} | {esc(names[wf])} | {tr[4]} | {tr[2]} | {tr[3]} | {'EVAL-'+wf if wf in evset else '— (no AI step)'} | {esc(bl)} | {sb} | {esc(new) or '—'}{(' · ' + esc(note)) if note else ''} | {sa} |")
w("t_wf.md", "\n".join(L) + "\n")

# ---------- 11.6.5.5 EVAL suite table ----------
gate_of = lambda nm: ("C" if re.search(r"scor|classif|qualif|detect|routing|monitor|selection|intake|capture|propensity|anomaly", nm, re.I) else "") + \
                     ("E" if re.search(r"extract|import|reconcil|order|verification|document", nm, re.I) else "") + \
                     ("G" if re.search(r"draft|content|generat|response|proposal|report|plan|prep|reply|brief|training|playbook|quotation|creative|localization|recommend", nm, re.I) else "") + \
                     ("R" if re.search(r"prioriti|next-best|matching|ranking|recommend", nm, re.I) else "") + \
                     ("T" if re.search(r"multilingual|locali|subtitle", nm, re.I) else "")
L = ["| TC | Suite | Workflow | AI steps | AGT | Implementing agent(s) | Gate families | Minimum cases (labelled + adversarial) | Languages (pilot → EU) |", "|---|---|---|---|---|---|---|---|---|"]
fam = collections.Counter()
for i, e in enumerate(evals):
    suite, nm, sku, ai, ag, lang = e[:6]; wf = suite[5:]; sb, bl, new, note = WM.W[wf]
    impl = ", ".join(dict.fromkeys(re.findall(r"AG-\d{3}", bl + " " + new))) or "—"
    g = gate_of(nm) or "G"; g = "".join(dict.fromkeys(g)) + "A"
    for ch_ in g: fam[ch_] += 1
    L.append(f"| TC-V12-F-{201+i:03d} | {suite} | {esc(nm)} | {ai} | {ag} | {impl} | {g} | 50 + 20 | en, hi → + de, fr |")
w("t_eval.md", "\n".join(L) + "\n")
json.dump(fam, open(os.path.join(OUT, "fam.json"), "w"))

# ---------- cards ----------
F = [("Type", "type"), ("Purpose and business outcome", "purpose"), ("Linked BR / FR / US", "links"), ("Persona", "persona"), ("Trigger", "trigger"),
     ("Inputs and data sources", "inputs"), ("Tools / APIs (registry §7.2.4)", "tools"), ("Outputs", "outputs"), ("Autonomy and HITL", "autonomy"), ("Model tier", "tier")]
out = []; costrows = []; tb = tl = th = 0
for c in CD.CARDS:
    prim, tin, cache, tout, calls, e = c["tok"]
    blend, base, form = CD.econ(prim, tin, cache, tout, calls, e)
    lo, hi = base * 0.3, base * 3
    tb += base; tl += lo; th += hi
    costrows.append((c["id"], c["name"], c["agt"], calls, blend, lo, base, hi, c["release"]))
    us = f"US-{c['ep'][3:]}-YF{int(c['id'][3:])-99:02d}"
    out.append(f"#### {c['id']} {c['name']}\n\n| Field | Specification |\n|---|---|")
    for lab, key in F:
        v = c[key]
        if key == "links": v = f"{v}; V12 {c['agt']} · {c['wfs']}; {us}; TC-V12-F-{131 + int(c['id'][3:]) - 100:03d}"
        out.append(f"| {lab} | {esc(v)} |")
    out.append(f"| Tier 2 eligibility · data class | {esc(c['tier2'])} · {esc(c['dclass'])} |")
    out.append(f"| Prompt / context strategy | PRM-{c['agt']}-{re.sub('[^a-z0-9]+','-',c['name'].lower()).strip('-')[:28]}-v1. {esc(c['prompt'])} |")
    out.append(f"| Guardrails | {esc(c['guard'])} |")
    out.append(f"| Failure modes and fallback | {esc(c['fail'])} |")
    out.append(f"| Success KPIs | {esc(c['kpi'])} |")
    out.append(f"| Eval dimensions | {esc(c['evals'])}; suites EVAL-{c['wfs'].split(';')[0].strip()}… (§11.6.5.5) |")
    out.append(f"| Tokens, calls, cost | {tin:,} in ({cache:,} cacheable, hit 60%), {tout:,} out; {calls} calls/month at pilot design volume [ASSUMPTION-863]. {form}; proposed line CR-V12-F-R (not B02). **Monthly: low ₹{lo:,.0f} · base ₹{base:,.0f} · high ₹{hi:,.0f}** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |")
    out.append(f"| Dependencies | {esc(c['deps'])} |")
    out.append(f"| Release | {esc(c['release'])} |\n")
w("t_cards.md", "\n".join(out))
L = ["| Agent | Name | AGT | Calls/month | ₹ per call (blended) | Low ₹/month | Base ₹/month | High ₹/month | Release |", "|---|---|---|---|---|---|---|---|---|"]
for r in costrows: L.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]:.3f} | {r[5]:,.0f} | {r[6]:,.0f} | {r[7]:,.0f} | {esc(r[8])} |")
L.append(f"| **Total** | 23 agents | | {sum(r[3] for r in costrows):,} | | **{tl:,.0f}** | **{tb:,.0f}** | **{th:,.0f}** | |")
L.append(f"| **With 25% overhead** | | | | | **{tl*1.25:,.0f}** | **{tb*1.25:,.0f}** | **{th*1.25:,.0f}** | |")
w("t_cardcost.md", "\n".join(L) + "\n")
json.dump(dict(lo=tl, base=tb, hi=th), open(os.path.join(OUT, "cardcost.json"), "w"))

# ---------- AU table ----------
L = ["| ID | Name | Wave / Release | Linked BR / FR / rule | Trigger | Deterministic logic | Outputs | Autonomy | Guardrail | Failure / fallback | KPI | Cost |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for r in AUD.AU: L.append("| " + " | ".join(esc(x) for x in r[:12]) + " |")
w("t_au.md", "\n".join(L) + "\n")

# ---------- extension table ----------
L = ["| Ext | Existing agent | V12 workflow | Prompt (PRM) | Added task | Autonomy | Tier |", "|---|---|---|---|---|---|---|"]
for e in WM.EXT: L.append("| " + " | ".join(esc(x) for x in e) + " |")
w("t_ext.md", "\n".join(L) + "\n")

# ---------- effort ----------
rows_e = []
for c in CD.CARDS: rows_e.append((c["id"], c["name"], "Agent " + c["size"], *CD.SIZE[c["size"]], "R2-CR" if "Release 2" in c["release"] else "P2"))
for r in AUD.AU: rows_e.append((r[0], r[1], "Automation " + r[12], *AUD.SZ[r[12]], r[2].split("· ")[-1]))
rows_e.append(("EXT-01…12", "12 task extensions to existing agents (prompt, schema, suite wiring)", "12 × 1/1.5/2.5", 12, 18, 30, "R2-CR"))
rows_e.append(("EVAL-PRG-1", "EVAL suites for workflows served by Release 1 agents (≈ 55 suites; 3,850 cases) [ASSUMPTION-862]", "Programme share 50%", 27.5, 40, 60, "R1-CR"))
rows_e.append(("EVAL-PRG-2", "EVAL suites for Release 2 agents and extensions (≈ 33 suites; 2,310 cases)", "Programme share 30%", 16.5, 24, 36, "R2-CR"))
rows_e.append(("EVAL-PRG-3", "EVAL suites for Phase-2 agents AG-100…114, 118, 119, 121 (≈ 23 suites; 1,610 cases)", "Programme share 20%", 11, 16, 24, "P2"))
rows_e.append(("REG-UI", "V12 screens A114–A121 content deltas (model registry, evaluation, injection defence, CPAR, rule register) on existing patterns", "5 screens × 3/4/6", 15, 20, 30, "R1-CR"))
rows_e.append(("PACKS", "Jurisdiction pack configuration: 10 V12 draft packs + IN/EU rule rows + 20-case preflight fixtures (counsel review excluded)", "Config + tests", 4, 6, 9, "R1-CR"))
L = ["| Item | Description | Size basis | Release | Low pd | Central pd | High pd |", "|---|---|---|---|---|---|---|"]
s = [0, 0, 0]; byrel = collections.defaultdict(lambda: [0, 0, 0])
for r in rows_e:
    L.append(f"| {r[0]} | {esc(r[1])} | {r[2]} | {r[6]} | {r[3]:g} | {r[4]:g} | {r[5]:g} |"); s[0] += r[3]; s[1] += r[4]; s[2] += r[5]
    for k in range(3): byrel[r[6]][k] += r[3 + k]
L.append(f"| **Total** | | | | **{s[0]:g}** | **{s[1]:g}** | **{s[2]:g}** |")
R = ["| Release window | Low pd | Central pd | High pd | Low ₹ (× ₹4,545) | Central ₹ (× ₹4,545 … ₹6,818) | High ₹ (× ₹6,818) |", "|---|---|---|---|---|---|---|"]
for k in ("R1-CR", "R2-CR", "P2"):
    v = byrel[k]; R.append(f"| {k} | {v[0]:g} | {v[1]:g} | {v[2]:g} | ₹{v[0]*4545/1e5:.2f} L | ₹{v[1]*4545/1e5:.2f}–{v[1]*6818/1e5:.2f} L | ₹{v[2]*6818/1e5:.2f} L |")
R.append(f"| **Total** | **{s[0]:g}** | **{s[1]:g}** | **{s[2]:g}** | **₹{s[0]*4545/1e5:.2f} L** | **₹{s[1]*4545/1e5:.2f}–{s[1]*6818/1e5:.2f} L** | **₹{s[2]*6818/1e5:.2f} L** |")
w("t_effrel.md", "\n".join(R) + "\n")
L.append(f"| **₹ at ₹4,545–6,818 per pd (Part 8.4)** | low pd × ₹4,545 … high pd × ₹6,818 | | | **₹{s[0]*4545/1e5:.2f} L** | **₹{s[1]*4545/1e5:.2f}–{s[1]*6818/1e5:.2f} L** | **₹{s[2]*6818/1e5:.2f} L** |")
w("t_effort.md", "\n".join(L) + "\n")
json.dump(dict(pd=s), open(os.path.join(OUT, "effort.json"), "w"))
print("aspects", len(ALL), dict(tot)); print("card cost", round(tl), round(tb), round(th)); print("effort", s)
