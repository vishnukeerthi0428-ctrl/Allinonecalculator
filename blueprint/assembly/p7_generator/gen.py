import collections, re, sys
import funnel as F
from agents import A
from autos import U
import model as M

OVERHEAD = 1.25  # retries, schema repairs, guard re-checks, thinking-token variance (ASSUMPTION-140)

def fmt(x): return f"₹{x:,.0f}"
def fmt2(x): return f"₹{x:,.2f}"

frag = {}

# ---------------- 7.1 structural ----------------
raw, removed, valid = F.structural()
RAW = sum(raw.values())
frag["RAW_IN"] = f"{raw['in_product']:,}"
frag["RAW_DEL"] = f"{raw['delivery']:,}"
frag["RAW"] = f"{RAW:,}"
frag["VALID"] = f"{len(valid):,}"
rules = [("S1", "Persona does not work in that stage (participation matrix §7.1.3)", "Part 1 §1.8; Part 2.3 §2.26.1"),
         ("S2", "Approval stage: no Generator, Orchestrator or Autonomous pattern — AI never approves or authors the approved artefact at the approval step", "BRL-AI-07; DEC-064"),
         ("S3", "External/anonymous personas (P14, P15): no Orchestrator, Autonomous or Monitor agents acting for them", "BRD §2; BR-S106, BR-S107"),
         ("S4", "Service identity P16: no Assistant pattern (needs a human user)", "Part 1 P16"),
         ("S5", "Reporting stage: no Autonomous pattern (no external action from a report)", "PP-01; BRL-AI-07"),
         ("S6", "Coding and Deploy stages: no Autonomous pattern (no autonomous merge or production deploy)", "M62; DEC-063")]
rows = ["| Rule | Structural screen | Source | Cells removed |", "|---|---|---|---|"]
for r, t, s in rules:
    rows.append(f"| {r} | {t} | {s} | {removed[r]:,} |")
rows.append(f"| **Total** | | | **{sum(removed.values()):,}** |")
frag["STRUCT_RULES"] = "\n".join(rows)

def part_table(part, stages, names):
    hdr = "| Persona | " + " | ".join(names[s] for s in stages) + " | Active stages |"
    sep = "|---" * (len(stages) + 2) + "|"
    out = [hdr, sep]
    for p, d in part.items():
        out.append(f"| {p} | " + " | ".join("●" if d[s] else "·" for s in stages) + f" | {sum(d.values())} |")
    tot = sum(sum(d.values()) for d in part.values())
    out.append(f"| **Cells** | " + " | ".join(str(sum(part[p][s] for p in part)) for s in stages) + f" | **{tot}** |")
    return "\n".join(out), tot
frag["PART_IN"], tin = part_table(F.PPART, F.PSTAGES, F.PSTAGE_NAMES)
frag["PART_DEL"], tdl = part_table(F.DPART, F.DSTAGES, F.DSTAGE_NAMES)
frag["PART_IN_N"], frag["PART_DEL_N"] = str(tin), str(tdl)

anch = set()
for x in F.I: anch |= F.cells_of(x, valid)
frag["ANCHORED"] = str(len(anch))
frag["UNANCHORED"] = f"{len(valid) - len(anch):,}"
# coverage by pattern
rows = ["| Pattern | Valid cells | Cells with a concrete job (anchored by ≥ 1 candidate) | Cells with no concrete job | Kept agents using the pattern |", "|---|---|---|---|---|"]
for p in F.PATTERNS:
    v = sum(1 for c in valid if c[2] == p); a = sum(1 for c in anch if c[2] == p)
    k = sum(1 for x in F.I if x["disp"] == "KEEP" and p in x["pa"])
    rows.append(f"| {F.PATTERN_NAMES[p]} | {v} | {a} | {v - a} | {k} |")
rows.append(f"| **Total** | **{len(valid)}** | **{len(anch)}** | **{len(valid) - len(anch)}** | |")
frag["PATTERN_COV"] = "\n".join(rows)

# ideas table
rows = ["| ID | Candidate idea | Stage | Persona | Pattern | Disposition | Target | Reason / merge note |", "|---|---|---|---|---|---|---|---|"]
NAMES = {**F.PSTAGE_NAMES, **F.DSTAGE_NAMES}
for x in F.I:
    rows.append(f"| {x['id']} | {x['idea']} | {', '.join(NAMES[s] for s in x['st'])} | {', '.join(x['pe'])} | {', '.join(F.PATTERN_NAMES[p].split(' /')[0] for p in x['pa'])} | {F.DISP_LABEL[x['disp']]} | {x['target'] or '—'} | {x['reason'] or 'Primary job of the agent'} |")
frag["IDEAS"] = "\n".join(rows)

cnt = collections.Counter(x["disp"] for x in F.I)
N = len(F.I)
excl = sum(cnt[k] for k in ("F1", "F2", "F3", "F4", "F6"))
after_filter = N - excl
au_from_ideas = sorted({x["target"] for x in F.I if x["target"].startswith("AU")})
ag_ids = sorted({x["target"] for x in F.I if x["disp"] == "KEEP"})
assert len(ag_ids) == len(A) == cnt["KEEP"], (len(ag_ids), len(A))
enablers = [u["id"] for u in U if u["id"] not in au_from_ideas]
after_merge = len(ag_ids) + len(au_from_ideas)
final = len(A) + len(U)
frag.update(N_IDEAS=str(N), N_EXCL=str(excl), N_AFTER_FILTER=str(after_filter), N_KEEP=str(cnt["KEEP"]),
            N_MERGE=str(cnt["MERGE"]), N_F5=str(cnt["F5"]), N_AU_IDEAS=str(len(au_from_ideas)),
            N_AFTER_MERGE=str(after_merge), N_ENABLERS=str(len(enablers)), N_AG=str(len(A)), N_AU=str(len(U)),
            N_FINAL=str(final), ENABLER_IDS=", ".join(enablers), AU_IDEA_IDS=", ".join(au_from_ideas),
            N_F1=str(cnt["F1"]), N_F2=str(cnt["F2"]), N_F3=str(cnt["F3"]), N_F4=str(cnt["F4"]), N_F6=str(cnt["F6"]),
            N_STRUCT_REMOVED=f"{sum(removed.values()):,}")
# exclusion table
rows = ["| Filter | Meaning | Ideas excluded | IDs |", "|---|---|---|---|"]
FL = {"F1": "Business value too low for the cost/complexity at pilot and Year-1 volume",
      "F2": "Feasibility: required data does not exist in scope",
      "F3": "Risk: error or misuse impact unacceptable even with human review",
      "F4": "Regulatory or binding policy prohibits it (DPDP, DEC-030, DEC-053, DEC-064, BR acceptance)",
      "F6": "Cost exceeds value; no source requirement"}
for f in ("F1", "F2", "F3", "F4", "F6"):
    ids = [x["id"] for x in F.I if x["disp"] == f]
    rows.append(f"| {f} | {FL[f]} | {len(ids)} | {', '.join(ids)} |")
rows.append(f"| F5 | Deterministic logic, rules, search or classical statistics work better than an LLM → **re-classified as automation (AU), not discarded** | {cnt['F5']} (re-classified) | {', '.join(x['id'] for x in F.I if x['disp']=='F5')} |")
frag["EXCL"] = "\n".join(rows)

# ---------------- catalogue summary ----------------
rel_counts = collections.Counter(M.release(a["wave"]) for a in A)
urel = lambda w: M.release(w)
urel_counts = collections.Counter(urel(u["wave"]) for u in U)
frag.update(AG_R1=str(rel_counts["R1"]), AG_R2=str(rel_counts["R2"]), AG_FUT=str(rel_counts["Future"]),
            AU_R1=str(urel_counts["R1"]), AU_R2=str(urel_counts["R2"]), AU_FUT=str(urel_counts["Future"]))
RELNAME = {"R1": "Release 1", "R2": "Release 2", "Future": "Future"}
rows = ["| ID | Name | Type | Scope | Pattern | Wave | Release | Autonomy | Model tier | Base pilot cost / month |", "|---|---|---|---|---|---|---|---|---|---|"]
for a in A:
    c = M.agent_cost(a)
    rows.append(f"| {a['id']} | {a['name']} | Agent | {a['scope']} | {a['pattern']} | {a['wave']} | {RELNAME[M.release(a['wave'])]} | {a['autonomy'].split(' (')[0].split(' for')[0]} | {a['tier'].split(';')[0].split('(')[0].strip()} | {fmt(c) if a['cost'] else 'within B09 seats'} |")
for u in U:
    rows.append(f"| {u['id']} | {u['name']} | Automation | Product{' + Delivery' if u['id'] in ('AU-013',) else ''} | Deterministic | {u['wave']} | {RELNAME[urel(u['wave'])]} | L3 rules | Tier 0 (no LLM) | ₹0 incremental |")
frag["CATALOGUE"] = "\n".join(rows)
frag["R1_T"]=str(rel_counts["R1"]+urel_counts["R1"]); frag["R2_T"]=str(rel_counts["R2"]+urel_counts["R2"]); frag["FUT_T"]=str(rel_counts["Future"]+urel_counts["Future"])

# ---------------- 7.2 spec tables & cards ----------------
rows = ["| ID | Name | Type | Purpose and business outcome (short) | Linked BR / FR / US | Persona | Trigger | Autonomy | Release |", "|---|---|---|---|---|---|---|---|---|"]
for a in A:
    rows.append(f"| {a['id']} | {a['name']} | Agent | {a['purpose'].split('. Outcome:')[0].split('.')[0]}. | {a['links']} | {a['persona']} | {a['trigger']} | {a['autonomy']} | {RELNAME[M.release(a['wave'])]} ({a['wave']}) |")
frag["SPEC_A"] = "\n".join(rows)
rows = ["| ID | Model tier | Tier 2 eligible | Data class | Tokens per call | Calls / month (pilot base) | Cost low / base / high (₹/month, pilot) | Budget line | Key dependencies |", "|---|---|---|---|---|---|---|---|---|"]
for a in A:
    if a["cost"]:
        cst = " / ".join(fmt(M.agent_cost(a, s)) for s in ("low", "base", "high"))
    else:
        cst = f"{fmt(M.SEAT_INR * a['seat_share'])} seat share (B09)"
    if a["cost"] and a.get("seat_share"):
        cst += f" + {fmt(M.SEAT_INR * a['seat_share'])} seat share"
    rows.append(f"| {a['id']} | {a['tier']} | {a['t2']} | {a['dclass']} | {M.tokens_per_call(a)} | {M.calls_base(a) if a['cost'] else 'n/a'} | {cst} | {M.lines(a)} | {a['deps']} |")
frag["SPEC_B"] = "\n".join(rows)

EVALN = {"G": "groundedness", "A": "accuracy", "B": "bias/fairness", "R": "refusal correctness", "J": "injection resistance",
         "S": "schema compliance", "L": "latency", "C": "cost per task", "F": "fallback behaviour"}
cards = []
for a in A:
    if a["cost"]:
        comp = []
        for c in a["cost"]:
            per = M.comp_cost_inr(c)[1]
            comp.append(f"{M.PRICES[c['model']]['name'].split(' (')[0]}{' + ' + str(int(c['esc']*100)) + '% Sonnet escalation' if c['esc'] else ''}; {c['I']:,} input tokens ({c['S']:,} cacheable, hit {int(c['hit']*100)}%, TTL {c['ttl']}), {c['O']:,} output; {'Batch API; ' if c['batch'] else ''}{c['calls']:,} calls/month; ≈ {fmt2(per)} per call; line {c['line']}{' (' + c['note'] + ')' if c['note'] else ''}")
        costtxt = "<br/>".join(comp) + f"<br/>**Monthly (pilot): low {fmt(M.agent_cost(a,'low'))} · base {fmt(M.agent_cost(a))} · high {fmt(M.agent_cost(a,'high'))}** (before the {int((OVERHEAD-1)*100)}% overhead allowance in §7.5.5)"
        if a.get("seat_share"):
            costtxt += f"<br/>Plus {fmt(M.SEAT_INR*a['seat_share'])}/month allocated share of B09 developer seats"
    else:
        costtxt = f"No API tokens; allocated share of B09 Claude Code seats = {fmt(M.SEAT_INR*a['seat_share'])}/month (2 seats × $20 × ₹90, BRD §6; verify plan price and usage caps)"
    evals = ", ".join(EVALN[e.strip()] for e in a["evals"].split(","))
    fields = [("Type", f"Agent · {a['pattern']} · scope: {a['scope']}"),
              ("Purpose and business outcome", a["purpose"]),
              ("Linked BR / FR / US", a["links"]),
              ("Persona", a["persona"]),
              ("Trigger", a["trigger"]),
              ("Inputs and data sources", a["inputs"]),
              ("Tools / APIs it can call (registry §7.2.4)", a["tools"]),
              ("Outputs", a["outputs"]),
              ("Autonomy level and human-in-the-loop checkpoints", f"**{a['autonomy']}.** {a['hitl']}"),
              ("Model tier used", a["tier"]),
              ("Tier 2 (free fallback) eligibility · data class", f"{a['t2']} · {a['dclass']}"),
              ("Prompt / context strategy", a["prompt"]),
              ("Guardrails", a["guardrails"]),
              ("Failure modes and fallback", a["failure"]),
              ("Success KPIs", a["kpis"]),
              ("Eval dimensions (cases written in Part 6)", evals),
              ("Estimated tokens, calls and monthly cost", costtxt),
              ("Dependencies", a["deps"]),
              ("Release", f"{RELNAME[M.release(a['wave'])]} · {a['wave']} (DEC-006)")]
    for k, v in fields:
        assert v and str(v).strip(), (a["id"], k)
    t = [f"#### {a['id']} {a['name']}", "", "| Field | Specification |", "|---|---|"]
    t += [f"| {k} | {v} |" for k, v in fields]
    cards.append("\n".join(t))
frag["CARDS"] = "\n\n".join(cards)

rows = ["| ID | Name | Wave / Release | Linked BR / FR / rule | Trigger | Deterministic logic | Outputs | Autonomy | Guardrail | Failure / fallback | KPI | Cost |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for u in U:
    for k in ("guard", "failure", "kpi", "cost"):
        assert u[k]
    rows.append(f"| {u['id']} | {u['name']} | {u['wave']} · {RELNAME[urel(u['wave'])]} | {u['links']} | {u['trigger']} | {u['logic']} | {u['outputs']} | {u['autonomy']} | {u['guard']} | {u['failure']} | {u['kpi']} | {u['cost']} |")
frag["AU_TABLE"] = "\n".join(rows)

# eval matrix
rows = ["| Agent | " + " | ".join(EVALN[e].split('/')[0].split(' ')[0].capitalize() for e in "GABRJSLCF") + " |", "|---" * 10 + "|"]
for a in A:
    es = {e.strip() for e in a["evals"].split(",")}
    rows.append(f"| {a['id']} | " + " | ".join("●" if e in es else "·" for e in "GABRJSLCF") + " |")
frag["EVAL_MATRIX"] = "\n".join(rows)

# ---------------- 7.5 cost tables ----------------
cur = [a for a in A if M.release(a["wave"]) != "Future"]
def tot(scen="base", vol=1.0, line="B02", agents=cur, stress=False):
    t = 0.0
    for a in agents:
        for c in a["cost"]:
            if c["line"] != line: continue
            if stress:
                s = M.SCEN["high"]; hit = max(0, c["hit"] - 0.2); esc = min(1, c["esc"] * 1.5)
                if c["model"] == "H":
                    per = (1 - esc) * M.per_call_usd("H", c, hit, 1.25) + esc * M.per_call_usd("S", c, hit, 1.25)
                else:
                    per = M.per_call_usd("S", c, hit, 1.25)
                t += per * M.FX * c["calls"] * vol
            else:
                t += M.comp_cost_inr(c, scen, vol)[0]
    return t
rows = ["| ID | Agent | Release | Low | Base | High | Share of base B02 |", "|---|---|---|---|---|---|---|"]
b02base = tot()
for a in cur:
    b = M.agent_cost(a, line="B02")
    if not any(c["line"] == "B02" for c in a["cost"]): continue
    rows.append(f"| {a['id']} | {a['name']} | {RELNAME[M.release(a['wave'])]} | {fmt(M.agent_cost(a,'low',line='B02'))} | {fmt(b)} | {fmt(M.agent_cost(a,'high',line='B02'))} | {b/b02base*100:.1f}% |")
L, B, H = tot("low"), tot("base"), tot("high")
rows.append(f"| | **Subtotal, model tokens (B02)** | | **{fmt(L)}** | **{fmt(B)}** | **{fmt(H)}** | 100% |")
rows.append(f"| | **+ {int((OVERHEAD-1)*100)}% overhead allowance** (retries, repairs, guard re-checks, thinking variance) | | **{fmt(L*OVERHEAD)}** | **{fmt(B*OVERHEAD)}** | **{fmt(H*OVERHEAD)}** | |")
rows.append(f"| | **Headroom vs ₹3,000 pilot ceiling (DEC-008)** | | {fmt(3000-L*OVERHEAD)} ({(L*OVERHEAD)/30:.0f}% used) | {fmt(3000-B*OVERHEAD)} ({(B*OVERHEAD)/30:.0f}% used) | {fmt(3000-H*OVERHEAD)} ({(H*OVERHEAD)/30:.0f}% used) | |")
frag["PILOT_TABLE"] = "\n".join(rows)
frag["B02_LOW"], frag["B02_BASE"], frag["B02_HIGH"] = fmt(L*OVERHEAD), fmt(B*OVERHEAD), fmt(H*OVERHEAD)
frag["B02_BASE_PCT"] = f"{B*OVERHEAD/30:.0f}%"; frag["B02_HIGH_PCT"] = f"{H*OVERHEAD/30:.0f}%"
frag["B02_BASE_RAW"], frag["B02_HIGH_RAW"], frag["B02_LOW_RAW"] = fmt(B), fmt(H), fmt(L)
r1 = [a for a in cur if M.release(a["wave"]) == "R1"]
frag["B02_R1_BASE"] = fmt(tot(agents=r1) * OVERHEAD)
frag["B02_R1_HIGH"] = fmt(tot("high", agents=r1) * OVERHEAD)

# Scenario TCO
def scen_row(vol, stress):
    return tot(vol=vol, stress=stress) * OVERHEAD
vols = [("Pilot (BR-S089 volumes)", 1, 3000), ("Growth gate (4× pilot; DEC-031 Year-1 design point)", 4, 12000), ("Scale (12× pilot; toward DEC-031 Year-2 design point)", 12, 40000)]
rows = ["| Volume level | Multiplier | B02 inference, base mix | B02 inference, stress mix | Ceiling (DEC-008) | Base fits? | Stress fits? | Max volume multiple at base mix within the ceiling |", "|---|---|---|---|---|---|---|---|"]
per1 = tot() * OVERHEAD
per1s = tot(stress=True) * OVERHEAD
for n, v, ceil in vols:
    b, s = scen_row(v, False), scen_row(v, True)
    rows.append(f"| {n} | {v}× | {fmt(b)} | {fmt(s)} | {fmt(ceil)} | {'Yes' if b <= ceil else 'No'} ({b/ceil*100:.0f}%) | {'Yes' if s <= ceil else '**No**'} ({s/ceil*100:.0f}%) | {ceil/per1:.1f}× |")
frag["SCEN_TABLE"] = "\n".join(rows)
frag["MAX12"] = f"{12000/per1:.1f}×"; frag["MAX40"] = f"{40000/per1:.1f}×"; frag["MAX3"] = f"{3000/per1:.1f}×"
frag["MAX3S"] = f"{3000/per1s:.1f}×"
frag["DEL_BASE"], frag["DEL_HIGH"], frag["DEL_LOW"] = fmt(tot(line="DEL")), fmt(tot("high", line="DEL")), fmt(tot("low", line="DEL"))
frag["SVC_BASE"], frag["SVC_HIGH"], frag["SVC_LOW"] = fmt(tot(line="SVC")), fmt(tot("high", line="SVC")), fmt(tot("low", line="SVC"))
frag["SEATS"] = fmt(M.SEAT_INR)
# full TCO pilot low/base/high
tool = {"low": 216, "base": 716, "high": 1216}  # secrets + presidio/embedding worker increment (see §7.5.2)
rows = ["| Cost element (monthly) | Formula | Low | Base | High |", "|---|---|---|---|---|"]
rows.append(f"| B02 production inference (owned portfolio) | Σ agents (I−S)·p_in + S·(h·p_cr + (1−h)·p_cw) + O·p_out, ×0.5 if batch, × calls × ₹90, × {OVERHEAD} | {fmt(L*OVERHEAD)} | {fmt(B*OVERHEAD)} | {fmt(H*OVERHEAD)} |")
dl, db, dh = tot("low", line="DEL"), tot(line="DEL"), tot("high", line="DEL")
rows.append(f"| Delivery AI reserve (CI review + eval judge + fixtures; RECOMMENDATION-061) | same formula, line DEL | {fmt(dl)} | {fmt(db)} | {fmt(dh)} → capped at ₹1,000 by halving review runs |")
rows.append(f"| B09 Claude Code developer seats | 2 × $20 × ₹90 (BRD §6) | ₹0 (existing seats) | {fmt(M.SEAT_INR)} | {fmt(M.SEAT_INR)} |")
rows.append("| Tier 2 free fallbacks | free tiers; default OFF (DEC-007) | ₹0 | ₹0 | ₹0 (optional one-time OpenRouter credit ≈ ₹900, not monthly; verify) |")
rows.append("| AI tooling increments (secrets ≈ 6 × $0.40; Presidio + embedding CPU in existing workers; LLM traces in PostgreSQL) | see §7.5.2 | ₹216 | ₹716 | ₹1,216 |")
sl, sb, sh = tot("low", line="SVC"), tot(line="SVC"), tot("high", line="SVC")
rows.append(f"| SaaS-client AI (AG-030, AG-031 client share) | charged to tenant plans (DEC-008), shown for completeness | {fmt(sl)} | {fmt(sb)} | {fmt(sh)} |")
tl = L*OVERHEAD + dl + 0 + 216
tb = B*OVERHEAD + db + M.SEAT_INR + 716
th = H*OVERHEAD + 1000 + M.SEAT_INR + 1216
rows.append(f"| **AI-layer TCO, owned portfolio (excl. tenant-billed)** | sum of rows 1–5 | **{fmt(tl)}** | **{fmt(tb)}** | **{fmt(th)}** |")
rows.append(f"| of which against the ₹3,000 B02 ceiling | row 1 only | {fmt(L*OVERHEAD)} ✔ | {fmt(B*OVERHEAD)} ✔ | {fmt(H*OVERHEAD)} {'✔' if H*OVERHEAD <= 3000 else '✘'} |")
frag["TCO_PILOT"] = "\n".join(rows)
frag["TCO_L"], frag["TCO_B"], frag["TCO_H"] = fmt(tl), fmt(tb), fmt(th)

# scenario TCO full
rows = ["| Element | Pilot (1×) | Growth gate (4×) | Scale (12×) | Notes |", "|---|---|---|---|---|"]
rows.append(f"| B02 inference, base mix (with overhead) | {fmt(scen_row(1,False))} | {fmt(scen_row(4,False))} | {fmt(scen_row(12,False))} | Hard cap ₹3,000 / ₹12,000 / ₹40,000 |")
rows.append(f"| B02 inference, stress mix | {fmt(scen_row(1,True))} | {fmt(scen_row(4,True))} | {fmt(scen_row(12,True))} | Cache −20 pp, escalation ×1.5, output ×1.25 |")
rows.append(f"| Delivery AI reserve | {fmt(db)} | {fmt(db)} | {fmt(db*1.5)} | Scales with PR volume, not business volume |")
rows.append(f"| B09 seats | {fmt(M.SEAT_INR)} | {fmt(M.SEAT_INR*2)} | {fmt(M.SEAT_INR*2)} | 4 seats from growth gate if team grows (verify) |")
rows.append("| LLM observability | ₹0 (traces in PostgreSQL + OpenTelemetry) | ₹2,250–2,700 (Langfuse self-host on one small instance, verify) | ₹2,700–4,500 | ADR-078 |")
rows.append("| Redaction, embeddings, secrets | ₹216–1,216 | ₹700–1,500 | ₹1,500–3,000 | CPU workers; Secrets Manager per secret (verify) |")
rows.append("| Tier 2 | ₹0 | ₹0 | ₹0–4,500 (optional self-hosted small model, Future) | RECOMMENDATION-067 |")
frag["TCO_SCEN"] = "\n".join(rows)

# Pricing table
rows = ["| Model (tier) | API model ID | Context | Input $/MTok | Output $/MTok | Cache read | Cache write 5 min / 1 h | Batch | Notes (verify) |", "|---|---|---|---|---|---|---|---|---|"]
rows.append("| Claude Sonnet 5.5 (Tier 1b, primary, latest GA Sonnet) | `claude-sonnet-5-5` | 1M tokens; 128K output | $2.00 | $10.00 | $0.10 (0.05×) | $2.50 (1.25×) / $4.00 (2×) | 50% off all tokens | Adaptive thinking on by default; `thinking: {type: \"disabled\"}` returns 400 — use effort `low` or `{type: \"between_tools\"}`; forced `tool_choice` returns 400 — use `output_config.format` structured outputs; handle `stop_reason: \"refusal\"`; server-side `fallbacks` (beta) available |")
rows.append("| Claude Haiku 5.5 (Tier 1a, lighter) | `claude-haiku-5-5` | 1M tokens; 128K output | $0.10 (≤ 100K-token prompts; $0.50 above) | $0.50 ($2.50 above 100K) | $0.01 (0.1×) | $0.125 / $0.20 | 50% off | Default effort `medium` (set `low`); thinking can be disabled at effort ≤ high; tokenizer counts ≈ 30% more tokens than Haiku 4.5; **no server-side refusal fallback** — gateway escalates to Sonnet |")
frag["PRICE_TABLE"] = "\n".join(rows)


# ---------------- extra fragments ----------------
grp = collections.OrderedDict()
for x in F.I:
    if x["disp"] in ("KEEP", "MERGE", "F5"):
        grp.setdefault(x["target"], []).append(x)
rows = ["| Consolidated into | Name | Ideas consolidated | Count | Merge rationale |", "|---|---|---|---|---|"]
NM = {a["id"]: a["name"] for a in A}; NM.update({u["id"]: u["name"] for u in U})
for t in sorted(grp, key=lambda k: (k[:2], k)):
    xs = grp[t]
    if len(xs) < 2: continue
    rows.append(f"| {t} | {NM[t]} | {', '.join(x['id'] for x in xs)} | {len(xs)} | {'; '.join(x['reason'] for x in xs if x['reason'] and x['disp']=='MERGE') or 'Same deterministic capability'} |")
frag["MERGE_TABLE"] = "\n".join(rows)
frag["N_MERGE_GROUPS"] = str(sum(1 for t in grp if len(grp[t]) > 1))
aut = collections.Counter(a["autonomy"][:2] for a in A)
frag["AUT_DIST"] = " · ".join(f"{k}: {aut[k]}" for k in ("L0", "L1", "L2", "L3"))
pat = collections.Counter(a["pattern"] for a in A)
frag["PAT_DIST"] = " · ".join(f"{k}: {v}" for k, v in sorted(pat.items()))
trig = collections.Counter()
for a in A:
    t = a["trigger"].lower()
    for k, lab in (("user action", "User action"), ("event", "Event"), ("schedule", "Schedule"), ("ci", "CI event")):
        if k in t: trig[lab] += 1
frag["TRIG_DIST"] = " · ".join(f"{k}: {v}" for k, v in trig.items())
# naive vs optimized
def naive():
    t = 0.0
    T0 = {"AG-013": 1/0.7, "AG-017": 1/0.6, "AG-003": 2.5, "AG-011": 13.0}  # calls avoided by Tier 0 rules/cache/templates
    for a in cur:
        for c in a["cost"]:
            if c["line"] != "B02": continue
            p = M.PRICES["S"]
            per = (c["I"] * p["inp"] + c["O"] * p["out"]) / 1e6
            t += per * M.FX * c["calls"] * T0.get(a["id"], 1.0)
    return t
nv = naive()
frag["NAIVE"] = fmt(nv); frag["NAIVE_X"] = f"{nv/(B):.0f}×"
frag["NAIVE_PCT"] = f"{(1-B/nv)*100:.0f}%"

# savings waterfall
T0 = {"AG-013": 1/0.7, "AG-017": 1/0.6, "AG-003": 2.5, "AG-011": 13.0}
def wf(step):
    t = 0.0
    for a in cur:
        for c in a["cost"]:
            if c["line"] != "B02": continue
            calls = c["calls"] * (T0.get(a["id"], 1.0) if step < 1 else 1.0)
            cc = dict(c)
            if step < 3: cc["S"] = 0  # no caching -> all input at full price
            if step < 4: cc["batch"] = False
            if step < 2:
                per = M.per_call_usd("S", cc, 0.0)
            elif c["model"] == "H":
                per = (1 - c["esc"]) * M.per_call_usd("H", cc, c["hit"]) + c["esc"] * M.per_call_usd("S", cc, c["hit"])
            else:
                per = M.per_call_usd("S", cc, c["hit"])
            t += per * M.FX * calls
    return t
labels = ["Naive: every call on Sonnet 5.5, no Tier 0, no caching, no batch", "+ Tier 0 rules, templates and caches remove avoidable calls",
          "+ Model tiering: Haiku 5.5 for classification/extraction (with escalation)", "+ Prompt caching of static prefixes", "+ Batch API for non-interactive agents"]
vals = [wf(i) for i in range(5)]
rows = ["| Step | Monthly B02 tokens cost (pilot base) | Saving vs previous step | Cumulative saving |", "|---|---|---|---|"]
for i, (l, v) in enumerate(zip(labels, vals)):
    prev = vals[i-1] if i else v
    rows.append(f"| {l} | {fmt(v)} | {('−' + fmt(prev - v) + f' ({(prev-v)/prev*100:.0f}%)') if i else '—'} | {('−' + f'{(vals[0]-v)/vals[0]*100:.0f}%') if i else '—'} |")
frag["WATERFALL"] = "\n".join(rows)
frag["WF_T0"] = f"{(vals[0]-vals[1])/vals[0]*100:.0f}%"; frag["WF_TIER"] = f"{(vals[1]-vals[2])/vals[1]*100:.0f}%"
frag["WF_CACHE"] = f"{(vals[2]-vals[3])/vals[2]*100:.0f}%"; frag["WF_BATCH"] = f"{(vals[3]-vals[4])/vals[3]*100:.0f}%"
frag["WF_TOTAL"] = f"{(vals[0]-vals[4])/vals[0]*100:.0f}%"

def render(tpl, out):
    s = open(tpl).read()
    missing = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", s)) - set(frag)
    if missing: sys.exit(f"missing fragments in {tpl}: {missing}")
    s = re.sub(r"\{\{([A-Z0-9_]+)\}\}", lambda m: frag[m.group(1)], s)
    open(out, "w").write(s)

if __name__ == "__main__":
    for k in ("RAW", "VALID", "ANCHORED", "N_IDEAS", "N_EXCL", "N_AFTER_FILTER", "N_AFTER_MERGE", "N_ENABLERS", "N_FINAL",
              "AG_R1", "AG_R2", "AG_FUT", "AU_R1", "AU_R2", "AU_FUT", "B02_LOW", "B02_BASE", "B02_HIGH", "B02_R1_BASE", "MAX3", "MAX3S", "MAX12", "MAX40",
              "DEL_BASE", "NAIVE", "NAIVE_X", "NAIVE_PCT", "AUT_DIST", "PAT_DIST", "TRIG_DIST", "N_MERGE_GROUPS", "WF_T0", "WF_TIER", "WF_CACHE", "WF_BATCH", "WF_TOTAL", "TCO_L", "TCO_B", "TCO_H", "N_AU_IDEAS"):
        print(k, frag[k])
    print(frag["SCEN_TABLE"])
    if len(sys.argv) > 1:
        for t, o in zip(sys.argv[1::2], sys.argv[2::2]):
            render(t, o)
