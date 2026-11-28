"""Parse the AI catalogue (Part 9.4 and the agent cards) and attach build and run estimates.

Every number produced here is an estimate. Run costs come from the blueprint's own per-agent cost
formulas (Parts 7.2, 7.4b, 9.7b, 9.8b, 9.9b). Build effort is a parametric estimate by complexity
class (see COMPLEXITY), which is an allocation inside the programme effort, not an addition to it.
"""
import re
from pathlib import Path

BP = Path(__file__).resolve().parent.parent

RELEASES = {
    "Release 1": ("Release 1", "Day 1–180", "Dec 2026 – 4 Jun 2027"),
    "Release 2": ("Release 2", "Day 181–208 (W5 exit Day 229)", "Jun – 23 Jul 2027"),
    "W6": ("W6 / Phase 2", "Day 237–365", "Aug – Dec 2027"),
    "A1": ("Advanced A1", "Day ≈ 239–365", "Aug – Dec 2027"),
    "A2": ("Advanced A2", "Day ≈ 366–480", "Dec 2027 – Mar 2028"),
    "A3": ("Advanced A3 (after scale gate)", "Day ≈ 481–600", "Apr – Jul 2028"),
}

# Parametric build effort (person-days) by class: (low, high)
COMPLEXITY = {
    ("AG", "Simple"): (2, 3), ("AG", "Medium"): (4, 6), ("AG", "Complex"): (7, 10),
    ("AU", "Simple"): (0.5, 1), ("AU", "Medium"): (1, 2), ("AU", "Complex"): (2.5, 4),
    ("WF", "Simple"): (3, 5), ("WF", "Medium"): (5, 8), ("WF", "Complex"): (8, 12),
}

SKILLS = {
    "AG": "AI/LLM engineer (prompt contracts, RAG, evals); Python/Django backend engineer; QA (AI evaluation); UX for review screens",
    "AU": "Python/Django backend engineer; data/DBA for rules and indexes; QA (unit and SIT)",
    "WF": "Backend engineer (execution engine, outbox, PDP); React/TypeScript frontend engineer; QA (SIT/UAT); UX designer; product owner for approval gates",
}
TECH = {
    "AG": "Claude via model gateway (Tier 0 cache → Haiku-class → Sonnet-class primary; DEC-418); Pydantic schemas; pgvector RAG; prompt registry; eval harness (promptfoo/deepeval-style, OSS); Celery workers",
    "AU": "Django REST Framework; Celery + Celery Beat on Valkey; PostgreSQL with RLS; transactional outbox; Policy Decision Point; no AI model",
    "WF": "Universal execution engine; transactional outbox; PDP dispatch recheck; React/TypeScript Admin and Website screens; audit and live monitor",
}


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def plain(s, n=None):
    s = re.sub(r"\*\*|`|\*", "", s or "")
    s = re.sub(r"\s+", " ", s).strip()
    return (s[: n - 1] + "…") if n and len(s) > n else s


def table_rows(text, id_re):
    out = {}
    hdr = None
    for ln in text.splitlines():
        if not ln.startswith("|"):
            hdr = None
            continue
        c = cells(ln)
        if re.match(r"^:?-{3,}", c[0]):
            continue
        if hdr is None:
            hdr = c
            continue
        if re.fullmatch(id_re, c[0]):
            out.setdefault(c[0], dict(zip(hdr, c)))
    return out


def release_key(s):
    s = s or ""
    for k in ("A3", "A2", "A1"):
        if re.search(rf"\b{k}\b", s):
            return k
    if "Release 2" in s or re.search(r"\bW[45]\b", s):
        return "Release 2"
    if "W6" in s or "Future" in s or "Phase 2" in s:
        return "W6"
    return "Release 1"


def agent_costs():
    """low/base/high ₹/month from the agent cards; fallback from the Part 9.4 cost column."""
    res = {}
    files = sorted(BP.glob("Part-07-2_*.md")) + sorted(BP.glob("Part-07-4b*.md")) + sorted(BP.glob("Part-09-[789]*.md"))
    for f in files:
        tx = f.read_text(encoding="utf-8")
        for m in re.finditer(r"^#{3,4} (AG-0\d\d)\b", tx, re.M):
            seg = tx[m.end(): m.end() + 9000]
            r = re.search(r"low ₹\s?([\d.,]+)\s*·\s*base ₹\s?([\d.,]+)\s*·\s*high ₹\s?([\d.,]+)", seg)
            if r and m.group(1) not in res:
                res[m.group(1)] = tuple(float(x.replace(",", "")) for x in r.groups())
    return res


def complexity(kind, d):
    blob = " ".join(d.values()).lower()
    if kind == "AG":
        score = 0
        score += 2 if "sonnet" in blob or "1b" in blob else 0
        score += 1 if "rag" in blob or "knowledge.search" in blob or "retriev" in blob else 0
        score += 1 if "supervisor" in blob or "planner" in blob or "multi" in blob else 0
        score += 1 if "predict" in blob or "model" in blob and "score" in blob else 0
        score += 1 if "whatsapp" in blob or "concierge" in blob or "portal" in blob else 0
        return "Complex" if score >= 3 else ("Medium" if score >= 1 else "Simple")
    if kind == "AU":
        n = len(d.get("Functionality (deterministic logic)", "") or d.get("Deterministic logic", ""))
        return "Complex" if n > 380 else ("Medium" if n > 180 else "Simple")
    n = len(d.get("Functionality (purpose)", ""))
    return "Complex" if n > 260 else ("Medium" if n > 140 else "Simple")


def automation_level(kind, autonomy):
    a = (autonomy or "").upper()
    if kind == "AU":
        if "L1" in a or "L0" in a:
            return "Partially automated (rule engine prepares; human confirms)"
        return "Fully automated (deterministic rules within policy guardrails)"
    if kind == "WF":
        return "Partially automated (orchestrated end to end; human approval at consequential steps)"
    if "L3" in a:
        return "Fully automated within guardrails (post-hoc review)"
    if "L2" in a:
        return "Mostly automated (acts; human reviews after)"
    if "L0" in a:
        return "Assistive only (suggests; human acts)"
    return "Partially automated (AI drafts; human approves before use)"


def load(rate_pd=(4545, 6818)):
    p94 = next(BP.glob("Part-09-4_*.md")).read_text(encoding="utf-8")
    ag = table_rows(p94, r"AG-\d{3}")
    au = table_rows(p94, r"AU-\d{3}")
    wf = table_rows(p94, r"WF-\d{2}")
    costs = agent_costs()
    items = []
    for kind, src in (("AG", ag), ("AU", au), ("WF", wf)):
        for k in sorted(src, key=lambda x: int(x.split("-")[1])):
            d = src[k]
            name = plain(d.get("Agent") or d.get("Automation") or d.get("Workflow"))
            what = plain(d.get("Functionality and business outcome") or d.get("Functionality (deterministic logic)") or d.get("Functionality (purpose)"), 420)
            autonomy = plain(d.get("Autonomy", ""), 60) if kind != "WF" else "L1 at consequential steps"
            rel = plain(d.get("Wave · Release", "")) if kind != "WF" else ""
            if kind == "WF":
                n = int(k[3:])
                rel = "Release 1" if n <= 10 else ("Release 2" if n <= 14 else ("A1" if n in (15, 18, 21, 22, 26, 27, 29, 33, 35, 36, 39) else ("A3" if n in (37, 38) else "A2")))
            rk = release_key(rel)
            cx = complexity(kind, d)
            lo, hi = COMPLEXITY[(kind, cx)]
            if kind == "AG":
                c = costs.get(k)
                if not c:
                    m = re.search(r"₹\s?([\d.,]+)", d.get("Pilot cost/month", ""))
                    b = float(m.group(1).replace(",", "")) if m else 0.0
                    c = (round(b * 0.4, 1), b, round(b * 2.5, 1))
                run = c
                run_note = "AI tokens via gateway (line B02/B23/B24), pilot volumes; before 25% overhead"
            elif kind == "AU":
                run = (0.0, 0.0, 0.0)
                run_note = "No model cost; runs on shared workers inside hosting line B01"
            else:
                run = (0.0, 0.0, 0.0)
                run_note = "Orchestration cost inside hosting (B01) plus the agents/automations it calls"
            merged = " (merged into AG-066, DEC-410)" if k == "AG-048" else ""
            items.append(dict(
                id=k, kind=kind, name=name + merged, what=what, autonomy=autonomy,
                level=automation_level(kind, autonomy), tier=plain(d.get("Model tier", "")) if kind == "AG" else "None (deterministic)",
                release=RELEASES[rk][0], window=RELEASES[rk][1], dates=RELEASES[rk][2], rk=rk,
                complexity=cx, pd_lo=lo, pd_hi=hi, cost_lo=lo * rate_pd[0], cost_hi=hi * rate_pd[1],
                run_lo=run[0], run_base=run[1], run_hi=run[2], run_note=run_note,
                skills=SKILLS[kind], tech=TECH[kind], origin=("v1.0 baseline" if (kind == "AG" and int(k[3:]) <= 38) or (kind == "AU" and int(k[3:]) <= 52) or (kind == "WF" and int(k[3:]) <= 14) else "v1.1 advanced"),
            ))
    # Advanced workflows: release = earliest release of the agents/automations the workflow uses
    order = ["Release 1", "Release 2", "W6", "A1", "A2", "A3"]
    rk_of = {i["id"]: i["rk"] for i in items}
    for f in sorted(BP.glob("Part-09-[789]*_*.md")):
        tx = f.read_text(encoding="utf-8")
        hs = list(re.finditer(r"^#{3,4} (WF-\d\d) ", tx, re.M))
        for j, m in enumerate(hs):
            seg = tx[m.end(): hs[j + 1].start() if j + 1 < len(hs) else m.end() + 6000]
            refs = [rk_of[x] for x in set(re.findall(r"\b(?:AG|AU)-\d{3}\b", seg)) if x in rk_of and rk_of[x] in ("A1", "A2", "A3", "W6")]
            for it in items:
                if it["id"] == m.group(1) and refs:
                    rk = min(refs, key=order.index)
                    it.update(rk=rk, release=RELEASES[rk][0], window=RELEASES[rk][1], dates=RELEASES[rk][2])
    return items


if __name__ == "__main__":
    it = load()
    import collections
    print(collections.Counter((i["kind"], i["release"]) for i in it))
    print(collections.Counter((i["kind"], i["complexity"]) for i in it))
    print(collections.Counter(i["level"] for i in it))
    for k in ("AG", "AU", "WF"):
        s = [i for i in it if i["kind"] == k]
        print(k, len(s), sum(i["pd_lo"] for i in s), sum(i["pd_hi"] for i in s), round(sum(i["run_base"] for i in s)))
