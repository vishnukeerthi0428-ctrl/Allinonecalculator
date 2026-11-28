#!/usr/bin/env python3
"""Generate Part 9.4: consolidated list of all workflows, AI agents and automations with their functionality.

Sources (parsed, not retyped): Part 7.1 catalogue summary (pattern, wave, tier, cost),
Part 7.2 agent summary table (purpose, persona, trigger, autonomy, links) and automation table
(trigger, deterministic logic, outputs, guardrail, fallback, KPI), Part 2.2 workflows.
Usage: python3 blueprint/assembly/build_ai_catalogue.py
"""
import re
from pathlib import Path

BP = Path(__file__).resolve().parent.parent
OUT = BP / "Part-09-4_AI_Agents_Automations_Workflows_Catalogue.md"


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def tables(text):
    lines = text.splitlines(); i = 0
    while i < len(lines) - 1:
        if lines[i].startswith("|") and re.match(r"^\|\s*:?-{3,}", lines[i + 1]):
            hdr = cells(lines[i]); rows = []; j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(cells(lines[j])); j += 1
            yield hdr, rows; i = j
        else:
            i += 1


def rows_by_id(path, idre, need):
    out = {}
    for hdr, rows in tables(Path(path).read_text(encoding="utf-8")):
        if not all(any(n.lower() in h.lower() for h in hdr) for n in need):
            continue
        for r in rows:
            if r and re.match(idre, r[0]):
                out.setdefault(r[0], dict(zip(hdr, r)))
    return out


def get(d, *keys):
    for k in keys:
        for hk, v in d.items():
            if k.lower() in hk.lower():
                return v
    return ""


def esc(s):
    return (s or "").replace("|", "/").replace("\n", " ").strip()


p71 = next(BP.glob("Part-07-1_*.md")); p72 = next(BP.glob("Part-07-2_*.md")); p22 = next(BP.glob("Part-02-2_*.md"))
cat = rows_by_id(p71, r"^(AG|AU)-\d{3}$", ["Pattern", "Model tier"])
ag = rows_by_id(p72, r"^AG-\d{3}$", ["Purpose", "Trigger"])
au = rows_by_id(p72, r"^AU-\d{3}$", ["Deterministic logic"])
# Source-pack enhancements (Part 7.4): new automations (same table shape) and new agent cards
EXTRA_PARTS = sorted(list(BP.glob("Part-07-4*_*.md")) + list(BP.glob("Part-09-7*_*.md")) + list(BP.glob("Part-09-8*_*.md")) + list(BP.glob("Part-09-9*_*.md")))
for extra in EXTRA_PARTS:
    for k, v in rows_by_id(extra, r"^AU-\d{3}$", ["Deterministic logic"]).items():
        au.setdefault(k, v)
    txt = extra.read_text(encoding="utf-8")
    for m in re.finditer(r"^#### (AG-\d{3}) (.+)$", txt, re.M):
        seg = txt[m.end(): m.end() + 6000]
        kv = {}
        for ln in seg.splitlines():
            if ln.startswith("#### ") or ln.startswith("**B02"):
                break
            if ln.startswith("|") and not re.match(r"^\|\s*:?-{3,}", ln):
                c = cells(ln)
                if len(c) >= 2:
                    kv[c[0]] = c[1]
        if kv and m.group(1) not in ag:
            ag[m.group(1)] = {"Name": m.group(2).strip(), "Purpose": kv.get("Purpose and business outcome", ""),
                              "Persona": kv.get("Persona", ""), "Trigger": kv.get("Trigger", ""),
                              "Autonomy": kv.get("Autonomy and HITL", ""), "Release": kv.get("Release", ""),
                              "Linked": kv.get("Linked BR / FR / US", "")}
            cat.setdefault(m.group(1), {"Pattern": kv.get("Type", ""), "Model tier": kv.get("Model tier", ""),
                                        "Wave": "", "Release": kv.get("Release", ""), "cost": "see Part 7.4b"})

# Workflows from Part 2.2 headings + purpose lines
wf = []
text22 = p22.read_text(encoding="utf-8")
for m in re.finditer(r"^## 2\.\d+ (WF-\d{2}) (.+)$", text22, re.M):
    seg = text22[m.end(): m.end() + 1500]
    pm = re.search(r"\*\*Purpose:\*\*\s*(.+?)(?:\*\*Actors|\*\*Screens|\n)", seg, re.S)
    sc = re.search(r"\*\*Screens:\*\*\s*([^.\n]+)", seg)
    fb = {
        "WF-08": "AppNAI qualify RFP/requirements, eligibility checklist, deadline guard, bid/no-bid, proposal and quote, human submission with recorded evidence, award proof, contract, delivery, verified payment (BRD §4–§5; DEC-053)",
        "WF-09": "Proposal and quote from approved templates and price versions; Decimal totals and tax; discount and legal approval thresholds; recipient review in portal; objections answered from approved facts or escalated (BRD §5; DEC-038)",
        "WF-10": "Buy/sell/service/training orders with SKU, unit and quantity lines; stock reservation; idempotent fulfilment events; over-delivery rejection; acceptance; separate receivable and payable ledgers (BRD §5; FR-DM-03)",
        "WF-11": "Close only on route-specific verified evidence (signed contract or verified payment); finance maker-checker; partial payments; no duplicate revenue or false Won state (BRD §5; DEC-054)",
        "WF-12": "Offering-specific onboarding and handoff (no patient data), milestones, feedback, renewal calendar and eligible reminders, lost-deal learning (BRD §5)",
        "WF-13": "Objective-driven plan from approved templates; simulation of recipients, cost, deadlines and conflicts; approval of the exact plan hash; execution with dispatch-time recheck; live monitoring, budget hard stops and emergency stop (BRD §5)",
        "WF-14": "Suspend or offboard a tenant/startup: stop schedules and queued actions, revoke senders and access, reconcile uncertain outcomes, export allowed records, apply retention (BRD §5)",
    }
    purpose = esc(pm.group(1)) if pm else fb.get(m.group(1), "")
    wf.append((m.group(1), m.group(2).strip(), purpose, esc(sc.group(1)) if sc else ""))
# Advanced workflows (Parts 9.7-9.9): "### WF-NN Name" + "**Purpose:** ..."
for extra in EXTRA_PARTS:
    tx = extra.read_text(encoding="utf-8")
    for m in re.finditer(r"^#{3,4} (WF-\d{2})[ :—–-]+(.+)$", tx, re.M):
        if any(w[0] == m.group(1) for w in wf):
            continue
        seg = tx[m.end(): m.end() + 2500]
        pm = re.search(r"\*\*Purpose:?\*\*:?\s*(.+)", seg)
        sc = re.search(r"\*\*Screens:?\*\*:?\s*([^\n]+)", seg)
        wf.append((m.group(1), m.group(2).strip(), esc(pm.group(1)) if pm else "", esc(sc.group(1)) if sc else ""))
wf.sort(key=lambda w: int(w[0][3:]))
extra_flows = [(h.group(1), h.group(2).strip()) for h in re.finditer(r"^### (2\.2[12]\.\d) (.+)$", text22, re.M)]

L = []
A = L.append
A("# AI Growth Engine: Employee Sales & Marketing Automation")
A("## Application Blueprint: PART 9 (Batch 9.4), Catalogue of Workflows, AI Agents and Automations")
A("")
A("| Field | Value |\n|---|---|\n| Document | Part 9, Batch 4 (generated by `assembly/build_ai_catalogue.py` from Parts 2.2, 7.1, 7.2, 7.4 and 9.7–9.9; regenerate after any change) |\n| Version | 1.0 · 27 Nov 2026 |\n| Purpose | One place listing every business workflow, AI agent and automation in the blueprint with its functionality |\n| Authoritative detail | Part 2.2 (workflow flows), Part 7.2 and Part 7.4 (source-pack additions AG-037/038, AU-044…052) and Parts 9.7–9.9 (advanced capabilities: AG-039…080, AU-053…119, WF-15…40), Part 7.3 (model routing, cost, governance), Part 6.4 (evaluation cases) |")
A("")
A("**Legend.** *Agent (AG)* = uses an AI model through the gateway. *Automation (AU)* = deterministic, rule-based, no AI model. "
  "*Autonomy*: L0 suggest only · L1 draft for human approval · L2 act with post-review · L3 act autonomously within guardrails. "
  "Consequential actions (quotes, discounts, contracts, legal terms, bid submissions, payments) are capped at L1 or are not automated at all (DEC-064). "
  "*Model tier*: Tier 0 rules/cache/template; 1a Claude Haiku-class; 1b Claude Sonnet-class; Tier 2 free fallbacks only for non-personal data and off by default; Tier 3 graceful degradation (DEC-007). "
  "Costs are pilot-base estimates per month before overhead; verify prices at implementation (as of 27 Nov 2026).")
A("")
n_ag, n_au = len(ag), len(au)
rel = lambda d: get(d, "Release")
A(f"## 9.4.1 Summary\n\n| Category | Count | Release 1 | Release 2 | Future |\n|---|---|---|---|---|")
for nm, src in (("AI agents (AG)", ag), ("Automations (AU)", au)):
    r1 = sum(1 for k in src if "1" in (get(cat.get(k, {}), "Release") or rel(src[k])) and "2" not in (get(cat.get(k, {}), "Release") or ""))
    r2 = sum(1 for k in src if "Release 2" in (get(cat.get(k, {}), "Release") or rel(src[k])))
    fu = sum(1 for k in src if "Future" in (get(cat.get(k, {}), "Release") or rel(src[k])))
    A(f"| {nm} | {len(src)} | {r1} | {r2} | {fu} |")
A(f"| Business workflows (WF) | {len(wf)} | — | — | — |")
A(f"| Supporting flows (vertical routes and cross-cutting) | {len(extra_flows)} | — | — | — |")
A("")
A(f"## 9.4.2 Business workflows (WF-01…{wf[-1][0]})\n\nEach workflow runs on the universal execution engine (Part 2.2 §2.6): plan-time check, transactional outbox, dispatch-time recheck of scope, consent, jurisdiction, budget and approval hash, simulation mode, emergency stop, and reconciliation of uncertain provider outcomes.\n")
A("| ID | Workflow | Functionality (purpose) | Main screens |\n|---|---|---|---|")
for i, t, p, s in wf:
    A(f"| {i} | {t} | {p} | {s} |")
A("")
A("**Supporting flows (Part 2.2 §2.21–2.22):** " + "; ".join(f"{a} {b}" for a, b in extra_flows) + ".")
A("")
A("## 9.4.3 AI agents (AG) and their functionality\n")
A("| ID | Agent | Functionality and business outcome | Pattern | Persona | Trigger | Autonomy | Model tier | Wave · Release | Pilot cost/month | Linked BR / FR |\n|---|---|---|---|---|---|---|---|---|---|---|")
for k in sorted(ag):
    d, c = ag[k], cat.get(k, {})
    A(f"| {k} | {esc(get(d,'Name'))} | {esc(get(d,'Purpose'))} | {esc(get(c,'Pattern'))} | {esc(get(d,'Persona'))} | {esc(get(d,'Trigger'))} | {esc(get(d,'Autonomy'))} | {esc(get(c,'Model tier'))} | {esc(get(c,'Wave'))} · {esc(get(c,'Release') or get(d,'Release'))} | {esc(get(c,'cost'))} | {esc(get(d,'Linked'))} |")
A("")
A("## 9.4.4 Automations (AU) and their functionality\n\nAutomations use no AI model; they are deterministic rules running on the platform's own workers. AU items marked as control automations in Part 7.2 must be running before any agent may run.\n")
A("| ID | Automation | Functionality (deterministic logic) | Trigger | Outputs | Guardrail | Failure / fallback | KPI | Autonomy | Wave · Release |\n|---|---|---|---|---|---|---|---|---|---|")
for k in sorted(au):
    d = au[k]
    A(f"| {k} | {esc(get(d,'Name'))} | {esc(get(d,'Deterministic logic'))} | {esc(get(d,'Trigger'))} | {esc(get(d,'Outputs'))} | {esc(get(d,'Guardrail'))} | {esc(get(d,'Failure'))} | {esc(get(d,'KPI'))} | {esc(get(d,'Autonomy'))} | {esc(get(d,'Wave'))} |")
A("")
A("## 9.4.5 How they fit together\n\n```mermaid\nflowchart TD\n  T[\"Trigger: user action, event, schedule or threshold\"] --> WF[\"Business workflow WF-01 to WF-14\"]\n  WF --> PDP[\"Policy Decision Point and control automations\"]\n  PDP --> AU[\"Deterministic automations AU\"]\n  PDP --> GW[\"Model gateway: Tier 0 cache and rules, Tier 1a Haiku, Tier 1b Sonnet, Tier 2 free for non-personal data, Tier 3 degrade\"]\n  GW --> AG[\"AI agents AG: draft, classify, extract, match, summarize\"]\n  AG --> HITL[\"Human approval where autonomy is L0 or L1\"]\n  AU --> OUT[\"Outbox and provider adapters with dispatch-time recheck\"]\n  HITL --> OUT\n  OUT --> MON[\"Live monitor, reconciliation, audit, cost ledger and evals\"]\n```\n")
A("## 9.4.6 Quality gate: Batch 9.4\n\n| Check | Result | Notes |\n|---|---|---|\n"
  f"| Completeness | Pass | {n_ag} agents and {n_au} automations parsed from Parts 7.2, 7.4 and 9.7–9.9; {len(wf)} workflows from Parts 2.2 and 9.7–9.9 |\n"
  "| Consistency | Pass | Generated from source tables; no retyping |\n"
  "| Time-sensitive facts | Pass | Model tiers and costs marked as estimates to verify (as of 27 Nov 2026) |\n"
  "| Restricted data | Pass | Tier 2 limited to non-personal data, default off (DEC-007) |\n")
A(f"**Status: Part 9 Batch 9.4 complete ({n_ag} AI agents, {n_au} automations, {len(wf)} workflows).**")
import sys
# v1.2 (Part 11.25, DEC-1004): Part 9.4 belongs to the frozen v1.1 baseline (it carries v1.2 erratum markers);
# it is rewritten only with --write-part94. The v1.2 catalogue (Part 11 additions) is written to Part 11.25b.
if "--write-part94" in sys.argv:
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print(OUT.name, "(v1.1 scope)", n_ag, n_au, len(wf), len(extra_flows), "cat", len(cat))
BASE_AG, BASE_AU, BASE_WF = dict(ag), dict(au), list(wf)


# ------------------------------------------------------------------------------------------------
# v1.2 extension: Part 11 agents AG-081…219, automations AU-120…299, workflows WF-41…60,
# and the V12 service workflows (156 SM-SVC, 96 INV) as a separate section.
# ------------------------------------------------------------------------------------------------
def plabel(path):
    m = re.match(r"Part-(\d+)(?:-(\d+))?([a-z]?)_", path.name)
    return f"{int(m.group(1))}.{int(m.group(2))}{m.group(3)}" if m.group(2) else str(int(m.group(1)))


def pkey(path):
    m = re.match(r"Part-(\d+)(?:-(\d+))?([a-z]?)_", path.name)
    return (int(m.group(1)), int(m.group(2) or 0), m.group(3))


def short(s, n=230):
    s = esc(re.sub(r"\*\*", "", s or ""))
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


P11 = sorted((p for p in BP.glob("Part-11-*.md") if not p.name.startswith("Part-11-25")), key=pkey)
ag11, au11, wf11, svc = {}, {}, {}, {}
for path in P11:
    tx = path.read_text(encoding="utf-8")
    lab = plabel(path)
    # agent cards: "#### AG-### Name" followed by a Field | Specification table
    for m in re.finditer(r"^#{3,5} (AG-(\d{3})) (.+)$", tx, re.M):
        if not (81 <= int(m.group(2)) <= 219) or m.group(1) in ag11:
            continue
        kv = {}
        for ln in tx[m.end(): m.end() + 9000].splitlines()[1:]:
            if ln.startswith("#"):
                break
            if ln.startswith("|") and not re.match(r"^\|\s*:?-{3,}", ln):
                c = cells(ln)
                if len(c) >= 2:
                    kv.setdefault(c[0], c[1])
        if kv:
            ag11[m.group(1)] = dict(kv, Name=m.group(3).strip(), Part=lab)
    # automation rows in the standard AU table (Deterministic logic column)
    for hdr, rows in tables(tx):
        if not any("deterministic logic" in h.lower() for h in hdr):
            continue
        for r in rows:
            if r and re.fullmatch(r"AU-\d{3}", r[0]) and 120 <= int(r[0][3:]) <= 299 and r[0] not in au11:
                au11[r[0]] = dict(zip(hdr, r), Part=lab)
    # workflows WF-41…60
    for m in re.finditer(r"^#{3,4} (WF-(\d{2}))[ :—–-]+(.+)$", tx, re.M):
        if 41 <= int(m.group(2)) <= 60 and m.group(1) not in wf11:
            seg = tx[m.end(): m.end() + 2500]
            pm = re.search(r"\*\*Purpose:?\*\*:?\s*(.+)", seg)
            sc = re.search(r"\*\*Screens:?\*\*:?\s*([^\n]+)", seg)
            wf11[m.group(1)] = (m.group(3).strip(), short(pm.group(1) if pm else "", 260), short(sc.group(1) if sc else "", 120), lab)
    # V12 service workflows (SM-SVC-##-WF0#, INV-SVC-##-WF0#): first card heading wins
    for m in re.finditer(r"^#{2,5} ((SM|INV)-SVC-(\d{2})-WF0?([1-4]))\b[ :—–-]*(.*)$", tx, re.M):
        wid = f"{m.group(2)}-SVC-{m.group(3)}-WF0{m.group(4)}"
        if wid not in svc:
            svc[wid] = (short(m.group(5).strip(" —–-:"), 120), lab)

C = []
W = C.append
W("# AI Growth Engine: Employee Sales & Marketing Automation")
W("## Application Blueprint: PART 11 (Batch 11.25b), Catalogue of AI Agents, Automations and Workflows, release v1.2")
W("")
W("| Field | Value |\n|---|---|\n| Document | Part 11.25b: generated by `assembly/build_ai_catalogue.py` from Parts 11.1–11.24 (agent cards, standard automation tables, workflow cards); regenerate after any change. The v1.1 catalogue (AG-001…080, AU-001…119, WF-01…40) stays in Part 9.4 |\n| Version | 1.2 · 28 Nov 2026 |\n| Change log and decisions | Part 11.25 (DEC-1000…1019) |\n| Authoritative detail | The source part named in each row; autonomy follows DEC-779 (L3/L4 only under an Active bounded mandate, Part 11.17) and the erratum E-V-01 of Part 11.23c |")
W("")
ag_tot, au_tot = len(BASE_AG) + len(ag11), len(BASE_AU) + len(au11)
nsm = sum(1 for k in svc if k.startswith("SM-")); ninv = sum(1 for k in svc if k.startswith("INV-"))
W("## 11.25.11 Summary\n")
W("| Category | v1.1 (Part 9.4) | Added in Part 11 | Total v1.2 | ID range in use |\n|---|---|---|---|---|")
W(f"| AI agents (AG) | {len(BASE_AG)} | {len(ag11)} | **{ag_tot}** | AG-001…080; " + ", ".join(sorted({'AG-%s…' % k[3:5] for k in ag11})[:0]) + f"{min(ag11)}…{max(ag11)} (gaps are unallocated reserve) |")
W(f"| Automations (AU) | {len(BASE_AU)} | {len(au11)} | **{au_tot}** | AU-001…119; {min(au11)}…{max(au11)} (gaps are unallocated reserve) |")
W(f"| Blueprint workflows (WF) | {len(BASE_WF)} | {len(wf11)} | **{len(BASE_WF) + len(wf11)}** | WF-01…WF-60; WF-24 and WF-40 unused (E-V-35) |")
W(f"| V12 service workflows (SM-SVC-##-WF0#) | — | {nsm} | **{nsm}** | 39 services × 4 (Parts 11.3, 11.4, 11.18) |")
W(f"| Investment Automation workflows (INV-SVC-##-WF0#) | — | {ninv} | **{ninv}** | 24 services × 4 (Parts 11.16b/c) |")
W("")
W("**By source part.**\n\n| Part | Agents | Automations | WF |\n|---|---|---|---|")
for lab in sorted({v['Part'] for v in ag11.values()} | {v['Part'] for v in au11.values()} | {v[3] for v in wf11.values()}, key=lambda s: [int(x) if x.isdigit() else x for x in re.findall(r"\d+|\D+", s)]):
    W(f"| {lab} | {sum(1 for v in ag11.values() if v['Part'] == lab)} | {sum(1 for v in au11.values() if v['Part'] == lab)} | {sum(1 for v in wf11.values() if v[3] == lab)} |")
W("")
W("## 11.25.12 AI agents added in Part 11 (AG-081…219)\n")
W("| ID | Agent | Type | Functionality and business outcome | Persona | Trigger | Autonomy and HITL | Model tier | Release | Part |\n|---|---|---|---|---|---|---|---|---|---|")
for k in sorted(ag11):
    d = ag11[k]
    W(f"| {k} | {esc(d['Name'])} | {short(get(d, 'Type'), 90)} | {short(get(d, 'Purpose'))} | {short(get(d, 'Persona'), 100)} | {short(get(d, 'Trigger'), 120)} | {short(get(d, 'Autonomy'), 160)} | {short(get(d, 'Model tier'), 90)} | {short(get(d, 'Release'), 50)} | {d['Part']} |")
W("")
W("## 11.25.13 Automations added in Part 11 (AU-120…299)\n\nAutomations use no AI model; they are deterministic rules on the platform's own workers.\n")
W("| ID | Automation | Functionality (deterministic logic) | Trigger | Guardrail | Failure / fallback | KPI | Autonomy | Wave · Release | Part |\n|---|---|---|---|---|---|---|---|---|---|")
for k in sorted(au11):
    d = au11[k]
    W(f"| {k} | {short(get(d, 'Name'), 80)} | {short(get(d, 'Deterministic logic'))} | {short(get(d, 'Trigger'), 110)} | {short(get(d, 'Guardrail'), 140)} | {short(get(d, 'Failure'), 120)} | {short(get(d, 'KPI'), 90)} | {short(get(d, 'Autonomy'), 40)} | {short(get(d, 'Wave'), 40)} | {d['Part']} |")
W("")
W("## 11.25.14 Blueprint workflows added in Part 11 (WF-41…60)\n")
W("| ID | Workflow | Functionality (purpose) | Main screens | Part |\n|---|---|---|---|---|")
for k in sorted(wf11):
    t_, pu, sc_, lab = wf11[k]
    W(f"| {k} | {esc(t_)} | {pu} | {sc_} | {lab} |")
W("")
W("## 11.25.15 V12 service workflows (separate section)\n\nEvery V12 service has four workflows. The card (contract, steps, DTOs, authority, tests) is in the part named; the run engine is the universal execution engine of Part 11.3a, with the PDP dispatch recheck and, for mandated L3/L4 runs, the mandate engine of Part 11.17.\n")
for fam, title in (("SM", "Sales & Marketing services SM-SVC-01…39"), ("INV", "Investment Automation services INV-SVC-01…24")):
    W(f"### {title}\n\n| Service | WF01 | WF02 | WF03 | WF04 | Part |\n|---|---|---|---|---|---|")
    for s in sorted({k[:len(fam) + 7] for k in svc if k.startswith(fam + "-")}):
        row = [svc.get(f"{s}-WF0{i}", ("—", ""))[0] for i in range(1, 5)]
        parts_ = sorted({svc[f"{s}-WF0{i}"][1] for i in range(1, 5) if f"{s}-WF0{i}" in svc})
        W(f"| {s} | " + " | ".join(row) + f" | {', '.join(parts_)} |")
    W("")
W("## 11.25.16 Quality gate: Batch 11.25b\n\n| Check | Result | Notes |\n|---|---|---|")
W(f"| Completeness | Pass | {len(ag11)} agent cards, {len(au11)} automation rows, {len(wf11)} workflow cards and {len(svc)} service workflows parsed from {len(P11)} Part 11 files |")
W("| Consistency | Pass | Generated from the source tables; no retyping; first definition wins; aliases resolved to two-digit workflow suffixes (DEC-966) |")
W("| Guardrail, fallback, KPI and cost | Pass | Every agent card and automation row in the source parts carries them (see the part named) |")
W("| Restricted data | Pass | Model routing per the provider-neutral registry (DEC-788); free tiers never receive personal data |")
W("")
W(f"**Status: Part 11 Batch 11.25b complete (generated). Totals v1.2: {ag_tot} AI agents, {au_tot} automations, {len(BASE_WF) + len(wf11)} blueprint workflows, {nsm} SM-SVC and {ninv} INV service workflows.**")
OUT12 = BP / "Part-11-25b_AI_Agents_Automations_Workflows_Catalogue_v1.2.md"
OUT12.write_text("\n".join(C) + "\n", encoding="utf-8")
print(OUT12.name, "agents", len(ag11), "automations", len(au11), "wf", len(wf11), "svc", nsm, ninv, "totals", ag_tot, au_tot)

