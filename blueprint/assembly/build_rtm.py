#!/usr/bin/env python3
"""Build the requirement-to-test traceability matrix (Part 6.6) from the blueprint Markdown files.

Usage:
    python3 assembly/build_rtm.py                # writes Part-06-6 markdown and final/RTM.csv
    python3 assembly/build_rtm.py --check        # print coverage summary only

Sources parsed (regexes only, no manual data):
    Part 1   §1.12.1  primary business requirements BR-M##, BR-TENANT/WEB/AUTO/SVC/QA (+ BR-S for the summary)
    Part 2.1 §2.4     interface/operation FRs FR-W##, FR-A###, FR-OP### and cross-cutting FRs
    Part 2.3 §2.25    BRL-<family>-## business rules
    Part 4.2 §4.22/23 NFR-001…099 with test method; Part 6.1 §6.1.3/§6.1.14 non-functional plans
    Part 5.1–5.3      stories US-#### with their Traces/Links/Linked rows and AC-####-## scenarios
    Part 6.2–6.5      test cases TC-##-###, TC-AI-AG###-###, TC-AU-AU###-### (Links columns + coverage tables)
    Part 7.1          agent and automation catalogue AG-###, AU-###
"""
import csv
import glob
import os
import re
import sys
from collections import OrderedDict, defaultdict

BP = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
OUT_MD = BP + "Part-06-6_Requirements_Traceability_Matrix.md"
OUT_CSV = BP + "final/RTM.csv"

# ----------------------------------------------------------------------------- regexes
FR_IF = r"FR-(?:W\d{2}|A\d{3}|OP\d{3})"
FR_XC = r"FR-(?:FLT|STD|DM|UIS|ENG|PUB|ADP|CSM|COP|SRCH|NEG)-(?:\d{2}|RULES)"
BR_P = r"BR-(?:M\d{2}|TENANT|WEB|AUTO|SVC|QA)"
BR_S = r"BR-S\d{3}"
BRL = r"BRL-[A-Z]{2,4}-\d{2}"
NFR = r"NFR-\d{3}"
US = r"US-\d{4}"
AC = r"AC-\d{4}-\d{2}"
TC_E = r"TC-\d{2}-\d{3}"
TC_AI = r"TC-AI-AG\d{3}-\d{3}"
TC_AU = r"TC-AU-AU\d{3}-\d{3}"
TC_ANY = rf"(?:{TC_AI}|{TC_AU}|{TC_E})"
ELL = r"\s*(?:…|\.\.\.|–|-)\s*"   # range separators


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def expand_req_ranges(text):
    """BRL-ELG-01…09, BRL-PRV-01, -02, FR-A065–A072, BR-M10–BR-M16, NFR-001–004."""
    out = []
    for m in re.finditer(r"(BRL-[A-Z]{2,4}-)(\d{2})\s*[…–]\s*(?:BRL-[A-Z]{2,4}-)?(\d{2})\b", text):
        a, b = int(m.group(2)), int(m.group(3))
        if 0 < b - a < 30:
            out += [f"{m.group(1)}{i:02d}" for i in range(a, b + 1)]
    for m in re.finditer(r"(BRL-[A-Z]{2,4}-)(\d{2})((?:,\s*-\d{2})+)", text):
        out.append(m.group(1) + m.group(2))
        out += [m.group(1) + x for x in re.findall(r"-(\d{2})", m.group(3))]
    for m in re.finditer(r"(AC-\d{4}-)(\d{2})((?:,\s*-\d{2})+)", text):
        out.append(m.group(1) + m.group(2))
        out += [m.group(1) + x for x in re.findall(r"-(\d{2})", m.group(3))]
    for m in re.finditer(r"(AC-\d{4}-)(\d{2})\s*[…–]\s*(?:AC-\d{4}-|-)?(\d{2})\b", text):
        a, b = int(m.group(2)), int(m.group(3))
        if 0 < b - a < 15:
            out += [f"{m.group(1)}{i:02d}" for i in range(a, b + 1)]
    for m in re.finditer(r"FR-A(\d{3})\s*[–…]\s*(?:FR-)?A(\d{3})", text):
        a, b = int(m.group(1)), int(m.group(2))
        if 0 < b - a < 30:
            out += [f"FR-A{i:03d}" for i in range(a, b + 1)]
    for m in re.finditer(r"FR-W(\d{2})\s*[–…]\s*(?:FR-)?W(\d{2})", text):
        a, b = int(m.group(1)), int(m.group(2))
        if 0 < b - a < 35:
            out += [f"FR-W{i:02d}" for i in range(a, b + 1)]
    for m in re.finditer(r"BR-M(\d{2})\s*[–…]\s*(?:BR-)?M(\d{2})", text):
        a, b = int(m.group(1)), int(m.group(2))
        if 0 < b - a < 20:
            out += [f"BR-M{i:02d}" for i in range(a, b + 1)]
    for m in re.finditer(r"NFR-(\d{3})\s*[–…]\s*(?:NFR-)?(\d{3})", text):
        a, b = int(m.group(1)), int(m.group(2))
        if 0 < b - a < 40:
            out += [f"NFR-{i:03d}" for i in range(a, b + 1)]
    return out


def ids(pattern, text):
    return list(dict.fromkeys(re.findall(pattern, text)))


def req_ids(text):
    """All requirement IDs in a text, with range expansion."""
    found = re.findall(rf"{FR_IF}|{FR_XC}|{BR_P}|{BR_S}|{BRL}|{NFR}|{US}|{AC}|AP-\d{{2}}", text)
    return list(dict.fromkeys(found + expand_req_ranges(text)))


def expand_tc_ranges(text, defined):
    """TC-08-001…025, TC-08-001…TC-08-025, TC-AI-AG024-001…006 → list of defined TC IDs."""
    out = []
    for m in re.finditer(rf"({TC_ANY}){ELL}(?:(TC-(?:AI-AG\d{{3}}|AU-AU\d{{3}}|\d{{2}})-)?(\d{{3}}))", text):
        start = m.group(1)
        pref, a = start.rsplit("-", 1)
        b = m.group(3)
        if m.group(2) and m.group(2).rstrip("-") != pref:
            continue
        a, b = int(a), int(b)
        if 0 < b - a <= 400:
            for i in range(a, b + 1):
                x = f"{pref}-{i:03d}"
                if x in defined:
                    out.append(x)
    out += [x for x in re.findall(TC_ANY, text) if x in defined]
    return list(dict.fromkeys(out))


def tc_sort_key(t):
    if t.startswith("TC-AI-"):
        return (2, t)
    if t.startswith("TC-AU-"):
        return (3, t)
    return (1, t)


def compress(tcs, limit=None):
    tcs = sorted(set(tcs), key=tc_sort_key)
    if not tcs:
        return "—"
    runs = []
    for t in tcs:
        pref, n = t.rsplit("-", 1)
        if runs and runs[-1][0] == pref and int(n) == runs[-1][2] + 1:
            runs[-1][2] = int(n)
        else:
            runs.append([pref, int(n), int(n)])
    parts = [f"{p}-{a:03d}" if a == b else f"{p}-{a:03d}…{b:03d}" for p, a, b in runs]
    if limit and len(parts) > limit:
        return ", ".join(parts[:limit]) + f", … (+{len(parts) - limit} runs)"
    return ", ".join(parts)


def pct(a, b):
    return f"{100.0 * a / b:.1f}%" if b else "n/a"


# ----------------------------------------------------------------------------- Part 1: BR
def load_br():
    t = read(BP + "Part-01_Product_and_Business_Foundation.md")
    prim = OrderedDict()
    sec = t.split("### 1.12.1")[1].split("### 1.12.2")[0]
    for line in sec.split("\n"):
        m = re.match(rf"\| ({BR_P}) \|", line)
        if m:
            c = cells(line)
            prim[m.group(1)] = dict(title=c[1], moscow=c[6], wave=c[7], epic=c[8])
    sup = OrderedDict()
    sec2 = t.split("### 1.12.2")[1].split("### 1.12.3")[0]
    for line in sec2.split("\n"):
        m = re.match(rf"\| ({BR_S}) \|", line)
        if m:
            c = cells(line)
            sup[m.group(1)] = dict(title=c[1][:90], traces=c[-1])
    return prim, sup


# ----------------------------------------------------------------------------- Part 2.1: FR
def load_fr():
    t = read(BP + "Part-02-1_Functional_Design_Modules_and_FR_Register.md")
    frs = OrderedDict()
    xfr = OrderedDict()
    sec = t.split("## 2.4 Functional requirement register")[1].split("## 2.5")[0]
    for line in sec.split("\n"):
        m = re.match(rf"\| ({FR_IF}) \|", line)
        if m:
            c = cells(line)
            fid = m.group(1)
            if fid.startswith("FR-OP"):
                wave, epic = c[-1], ("EP-04" if fid == "FR-OP001" else "EP-21")
                title = c[1]
            else:
                we = c[-1]
                mm = re.match(r"(W\d(?:[^·]*)?)\s*·\s*(EP-\d{2})", we)
                wave, epic = (mm.group(1).strip(), mm.group(2)) if mm else (we, "")
                title = c[1]
            frs[fid] = dict(title=title, br=ids(rf"{BR_P}|{BR_S}", line), wave=wave, epic=epic,
                            surface=c[2] if not fid.startswith("FR-OP") else "Operation")
            continue
        m = re.match(rf"\| ({FR_XC}) \|", line)
        if m:
            c = cells(line)
            xfr[m.group(1)] = dict(title=re.sub(r"\*\*", "", c[1])[:80], br=ids(rf"{BR_P}|{BR_S}", line))
    return frs, xfr


def sm_alias(fid):
    m = re.match(r"FR-W(\d{2})$", fid)
    if m:
        n = int(m.group(1))
        return (f"SM-UAT-S{n:03d}" if n <= 30 else "—") + f" · SM-UX-UAT-W{n:02d}"
    m = re.match(r"FR-A(\d{3})$", fid)
    if m:
        n = int(m.group(1))
        return (f"SM-UAT-S{30 + n:03d}" if n <= 108 else "—") + f" · SM-UX-UAT-A{n:03d}"
    return "—"


# ----------------------------------------------------------------------------- Part 2.3: BRL
def load_brl():
    t = read(BP + "Part-02-3_Business_Rules_RBAC_State_Machines.md")
    brl = OrderedDict()
    for line in t.split("\n"):
        m = re.match(rf"\| ({BRL}) \| (.*?) \|", line)
        if m and m.group(1) not in brl:
            brl[m.group(1)] = m.group(2)[:70]
    stated = re.search(r"= \*\*(\d+) business rules\*\*", t)
    return brl, int(stated.group(1)) if stated else None


# ----------------------------------------------------------------------------- Part 4.2 / 6.1: NFR
def load_nfr():
    t = read(BP + "Part-04-2_Non_Functional_Requirements.md")
    nfr = OrderedDict()
    for line in t.split("\n"):
        m = re.match(rf"\| ({NFR}) \|", line)
        if m and m.group(1) not in nfr:
            c = cells(line)
            if len(c) >= 9:
                nfr[m.group(1)] = dict(cat=c[1], req=re.sub(r"\*\*", "", c[2])[:80], method=c[5][:90], epic=c[-1])
    s61 = read(BP + "Part-06-1_Test_Strategy.md")
    plan = defaultdict(set)
    for secname in ("### 6.1.3.1", "### 6.1.3.2", "### 6.1.14.1", "### 6.1.14.2", "### 6.1.14.3", "### 6.1.14.4",
                    "### 6.1.14.5", "### 6.1.14.6", "### 6.1.9.6"):
        if secname not in s61:
            continue
        body = s61.split(secname, 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]
        for line in body.split("\n"):
            if not line.startswith("| "):
                continue
            c = cells(line)
            key = c[0] if re.match(r"(T\d{2}|LT-\d{2}|DR-\d|M-\d{2})$", c[0]) else f"§{secname[4:]} {c[0][:28]}"
            for n in set(re.findall(NFR, line) + expand_req_ranges(line)):
                plan[n].add(key)
    return nfr, plan


# ----------------------------------------------------------------------------- Part 5: stories
def load_stories():
    files = sorted(glob.glob(BP + "Part-05-1[bc]_*.md")) + sorted(glob.glob(BP + "Part-05-[23]_*.md"))
    stories = OrderedDict()
    for f in files:
        t = read(f)
        for m in re.finditer(rf"^#{{4,5}} ({US})\b[^\n]*\n(.*?)(?=^#{{2,5}} |\Z)", t, re.S | re.M):
            sid, body = m.group(1), m.group(2)
            link_rows = [ln for ln in body.split("\n") if re.match(r"\| (?:Traces|Links|Linked)\b", ln)]
            lt = " ".join(link_rows)
            acs = ids(rf"(?:Scenario(?: Outline)?: )({AC})", body)
            acs = [a for a in acs if a[3:7] == sid[3:]]
            st = stories.setdefault(sid, dict(epic="EP-" + sid[3:5], links=set(), acs=[], file=os.path.basename(f)))
            st["links"].update(req_ids(lt))
            st["acs"] += [a for a in acs if a not in st["acs"]]
    return stories


# ----------------------------------------------------------------------------- Part 6: test cases
BATCHES = [
    ("6.2a", "Part-06-2a_*.md", "EP-08…EP-11"), ("6.2b", "Part-06-2b_*.md", "EP-12…EP-14"),
    ("6.3a", "Part-06-3a_*.md", "EP-15…EP-18"), ("6.3b", "Part-06-3b_*.md", "EP-19…EP-21"),
    ("6.4", "Part-06-4_*.md", "AI agents AG-001…036 and automations AU-001…043"),
    ("6.5", "Part-06-5_*.md", "EP-01…EP-07"),
]


def batch_status():
    st = []
    for code, pat, scope in BATCHES:
        fs = sorted(glob.glob(BP + pat))
        if not fs:
            st.append((code, "—", scope, "Missing"))
            continue
        tail = read(fs[0])[-3000:]
        done = bool(re.search(r"\*\*Status: Part 6 Batch [^*]*complete", tail))
        st.append((code, os.path.basename(fs[0]), scope, "Complete" if done else "Incomplete (no status line)"))
    return st


def load_tcs(status):
    tcs = OrderedDict()
    cov_links = defaultdict(set)   # req -> TCs (coverage tables)
    files = [BP + s[1] for s in status if s[1] != "—"]
    for f in files:
        t = read(f)
        lines = t.split("\n")
        header = None
        for line in lines:
            if line.startswith("| ") and not re.match(rf"\| {TC_ANY} \|", line):
                c = cells(line)
                if c and c[0] in ("ID", "TC ID", "Case ID", "Test case"):
                    header = c
                continue
            m = re.match(rf"\| ({TC_ANY}) \|", line)
            if not m:
                continue
            c = cells(line)
            tid = m.group(1)
            li = 2
            tech_i = None
            pr_i = None
            if header:
                for i, h in enumerate(header):
                    hl = h.lower()
                    if "link" in hl:
                        li = i
                    if hl.startswith("tech"):
                        tech_i = i
                    if hl in ("p", "priority", "pri"):
                        pr_i = i
            links = c[li] if li < len(c) else ""
            row_ids = req_ids(links)
            tech = c[tech_i] if tech_i is not None and tech_i < len(c) else ""
            prio = c[pr_i] if pr_i is not None and pr_i < len(c) else next((x for x in c if re.fullmatch(r"P[0-3]", x)), "")
            if tid in tcs:          # same ID listed twice (e.g. summary table): merge
                tcs[tid]["links"].update(row_ids)
                continue
            tcs[tid] = dict(file=os.path.basename(f), links=set(row_ids), tech=tech, prio=prio, row=line)
        # coverage tables: rows whose first cell is a requirement ID and that mention TC IDs
        for line in lines:
            if not line.startswith("| ") or re.match(rf"\| {TC_ANY} \|", line):
                continue
            c = cells(line)
            first = re.match(rf"^\*?\*?({FR_IF}|{FR_XC}|{BR_P}|{BRL}|{NFR}|{US}|{AC})\b", c[0]) if c else None
            if not first or "TC-" not in line:
                continue
            cov_links[first.group(1)].add(line)
    defined = set(tcs)
    resolved = defaultdict(set)
    for req, vals in cov_links.items():
        for v in vals:
            resolved[req].update(expand_tc_ranges(v, defined))
    return tcs, resolved


# ----------------------------------------------------------------------------- Part 7: AG / AU
def load_ai():
    t = read(BP + "Part-07-1_AI_Discovery_and_Catalogue.md")
    ag, au = OrderedDict(), OrderedDict()
    for line in t.split("\n"):
        m = re.match(r"\| (AG-\d{3}) \| (.*?) \|", line)
        if m and m.group(1) not in ag:
            ag[m.group(1)] = cells(line)[1]
        m = re.match(r"\| (AU-\d{3}) \| (.*?) \|", line)
        if m and m.group(1) not in au:
            au[m.group(1)] = cells(line)[1]
    return ag, au


# ----------------------------------------------------------------------------- build
def build():
    status = batch_status()
    br, brs = load_br()
    frs, xfr = load_fr()
    brl, brl_stated = load_brl()
    nfr, nfr_plan = load_nfr()
    stories = load_stories()
    tcs, cov = load_tcs(status)
    ag, au = load_ai()

    ac_story = {a: s for s, st in stories.items() for a in st["acs"]}
    # requirement -> TCs (direct link in Links column)
    direct = defaultdict(set)
    for tid, t in tcs.items():
        for r in t["links"]:
            direct[r].add(tid)
            if re.fullmatch(AC, r):
                direct["US-" + r[3:7]].add(tid)
    for req, s in cov.items():          # coverage-table links
        for tid in s:
            direct[req].add(tid)
            if re.fullmatch(AC, req):
                direct["US-" + req[3:7]].add(tid)
    # story -> TCs
    us_tc = {s: set(direct.get(s, set())) for s in stories}
    for s, st in stories.items():
        for a in st["acs"]:
            us_tc[s] |= direct.get(a, set())
    # FR -> stories, FR -> TCs (explicit + via story)
    fr_us = defaultdict(set)
    for s, st in stories.items():
        for r in st["links"]:
            if re.fullmatch(rf"{FR_IF}|{FR_XC}", r):
                fr_us[r].add(s)
    fr_tc = {}
    fr_tc_explicit = {}
    for f in list(frs) + list(xfr):
        ex = set(direct.get(f, set()))
        via = set()
        for s in fr_us.get(f, ()):
            via |= us_tc[s]
        fr_tc_explicit[f] = ex
        fr_tc[f] = ex | via
    # BR -> FR -> US -> TC
    br_fr = defaultdict(set)
    for f, d in list(frs.items()) + list(xfr.items()):
        for b in d["br"]:
            br_fr[b].add(f)
    br_us = defaultdict(set)
    for s, st in stories.items():
        for r in st["links"]:
            if re.fullmatch(rf"{BR_P}|{BR_S}", r):
                br_us[r].add(s)
    br_tc = {}
    for b in list(br) + list(brs):
        t = set(direct.get(b, set()))
        for f in br_fr.get(b, ()):
            t |= fr_tc.get(f, set())
        for s in br_us.get(b, ()):
            t |= us_tc[s]
        br_tc[b] = t
    # BRL
    brl_tc = {r: set(direct.get(r, set())) for r in brl}
    for tid, t in tcs.items():          # rule cited anywhere in the row (data, expected) also counts
        for r in set(re.findall(BRL, t["row"])):
            if r in brl_tc:
                brl_tc[r].add(tid)
    # NFR
    nfr_tc = {n: set(direct.get(n, set())) for n in nfr}
    for tid, t in tcs.items():
        for n in set(re.findall(NFR, t["row"])):
            if n in nfr_tc:
                nfr_tc[n].add(tid)
    # AG / AU
    ag_tc = defaultdict(set)
    au_tc = defaultdict(set)
    for tid in tcs:
        m = re.match(r"TC-AI-AG(\d{3})-", tid)
        if m:
            ag_tc["AG-" + m.group(1)].add(tid)
        m = re.match(r"TC-AU-AU(\d{3})-", tid)
        if m:
            au_tc["AU-" + m.group(1)].add(tid)
    # ACs
    all_acs = [a for st in stories.values() for a in st["acs"]]
    ac_cov = {a: direct.get(a, set()) for a in all_acs}
    return locals()


# ----------------------------------------------------------------------------- render
def render(D):
    frs, xfr, br, brs, brl, nfr, stories, tcs, ag, au = (D[k] for k in ("frs", "xfr", "br", "brs", "brl", "nfr", "stories", "tcs", "ag", "au"))
    fr_tc, fr_us, br_fr, br_us, br_tc, us_tc = (D[k] for k in ("fr_tc", "fr_us", "br_fr", "br_us", "br_tc", "us_tc"))
    brl_tc, nfr_tc, nfr_plan, ag_tc, au_tc, ac_cov = (D[k] for k in ("brl_tc", "nfr_tc", "nfr_plan", "ag_tc", "au_tc", "ac_cov"))
    status = D["status"]
    S = {}
    L = []
    W = L.append

    # ---- (0) sources
    W("| Batch | File | Scope | Status at build time |")
    W("|---|---|---|---|")
    for code, f, scope, stt in status:
        n = sum(1 for t in tcs.values() if t["file"] == f)
        W(f"| {code} | `{f}` | {scope} | {stt}; {n} TC rows parsed |")
    S["sources"] = "\n".join(L)
    L.clear()

    # ---- coverage per level
    epics = [f"EP-{i:02d}" for i in range(1, 22)]
    n_tc = len(tcs)
    n_e = sum(1 for t in tcs if re.fullmatch(TC_E, t))
    n_ai = sum(1 for t in tcs if t.startswith("TC-AI-"))
    n_au = sum(1 for t in tcs if t.startswith("TC-AU-"))
    cov_br = sum(1 for b in br if br_tc[b])
    cov_brs = sum(1 for b in brs if br_tc[b])
    cov_fr = sum(1 for f in frs if fr_tc[f])
    cov_fr_ex = sum(1 for f in frs if D["fr_tc_explicit"][f])
    cov_xfr = sum(1 for f in xfr if fr_tc[f])
    cov_us = sum(1 for s in stories if us_tc[s])
    acs = list(ac_cov)
    cov_ac = sum(1 for a in acs if ac_cov[a])
    cov_brl = sum(1 for r in brl if brl_tc[r])
    cov_nfr_tc = sum(1 for n in nfr if nfr_tc[n])
    cov_nfr_any = sum(1 for n in nfr if nfr_tc[n] or nfr_plan.get(n))
    cov_ag = sum(1 for a in ag if ag_tc.get(a))
    cov_au = sum(1 for a in au if au_tc.get(a))
    W("| Level | Items in scope | Covered (≥ 1 TC) | Coverage | Basis of the count |")
    W("|---|---|---|---|---|")
    W(f"| Primary business requirements (BR-M, BR-TENANT/WEB/AUTO/SVC/QA) | {len(br)} | {cov_br} | **{pct(cov_br, len(br))}** | TC links the BR, or covers an FR or story that traces to it |")
    W(f"| Supplementary business requirements (BR-S) | {len(brs)} | {cov_brs} | {pct(cov_brs, len(brs))} | Same rule; BR-S trace to stories and FRs |")
    W(f"| Interface and operation FRs (FR-W, FR-A, FR-OP) | {len(frs)} | {cov_fr} | **{pct(cov_fr, len(frs))}** | TC links the FR, or covers a story whose links include it ({cov_fr_ex} with an explicit FR link) |")
    W(f"| Cross-cutting FRs (FLT, STD, DM, UIS, ENG, PUB, ADP, CSM, COP, SRCH, NEG) | {len(xfr)} | {cov_xfr} | {pct(cov_xfr, len(xfr))} | Same rule |")
    W(f"| User stories (Part 5.1–5.3) | {len(stories)} | {cov_us} | **{pct(cov_us, len(stories))}** | TC links the story or one of its AC |")
    W(f"| Acceptance criteria (Gherkin AC) | {len(acs)} | {cov_ac} | **{pct(cov_ac, len(acs))}** | TC links the AC (Links column or coverage table) |")
    W(f"| Business rules (BRL, Part 2.3) | {len(brl)} defined ({D['brl_stated']} stated) | {cov_brl} | **{pct(cov_brl, len(brl))}** | Rule ID in a TC row (links, data or expected) |")
    W(f"| NFRs with ≥ 1 test case (Part 4.2, NFR-001…099) | {len(nfr)} | {cov_nfr_tc} | {pct(cov_nfr_tc, len(nfr))} | TC row cites the NFR |")
    W(f"| NFRs with a test case or a Part 6.1 non-functional plan item | {len(nfr)} | {cov_nfr_any} | **{pct(cov_nfr_any, len(nfr))}** | Adds LT-, DR-, M-, T-type and §6.1.14 plan rows that cite the NFR |")
    W(f"| AI agents (AG, Part 7.1) | {len(ag)} | {cov_ag} | **{pct(cov_ag, len(ag))}** | ≥ 1 TC-AI case |")
    W(f"| Automations (AU, Part 7.1) | {len(au)} | {cov_au} | **{pct(cov_au, len(au))}** | ≥ 1 TC-AU case |")
    W(f"| Test cases parsed | {n_tc} | — | — | {n_e} epic TCs · {n_ai} TC-AI · {n_au} TC-AU |")
    S["levels"] = "\n".join(L)
    L.clear()
    D["summary"] = dict(br=(cov_br, len(br)), fr=(cov_fr, len(frs)), xfr=(cov_xfr, len(xfr)), us=(cov_us, len(stories)),
                        ac=(cov_ac, len(acs)), brl=(cov_brl, len(brl)), nfr=(cov_nfr_tc, cov_nfr_any, len(nfr)),
                        ag=(cov_ag, len(ag)), au=(cov_au, len(au)), tc=(n_tc, n_e, n_ai, n_au), brs=(cov_brs, len(brs)))

    # ---- per epic
    W("| Epic | FRs (Part 2.1) | FRs covered | FR % | Stories | Stories covered | AC | AC covered | AC % | Epic TCs |")
    W("|---|---|---|---|---|---|---|---|---|---|")
    for e in epics:
        efr = [f for f, d in frs.items() if d["epic"] == e]
        efc = sum(1 for f in efr if fr_tc[f])
        eus = [s for s, st in stories.items() if st["epic"] == e]
        euc = sum(1 for s in eus if us_tc[s])
        eac = [a for s in eus for a in stories[s]["acs"]]
        eacc = sum(1 for a in eac if ac_cov[a])
        etc = sum(1 for t in tcs if re.fullmatch(TC_E, t) and t[3:5] == e[3:])
        W(f"| {e} | {len(efr)} | {efc} | {pct(efc, len(efr))} | {len(eus)} | {euc} | {len(eac)} | {eacc} | {pct(eacc, len(eac))} | {etc} |")
    S["epics"] = "\n".join(L)
    L.clear()

    # ---- (a) BR → FR → US → TC
    W("| BR | Title | MoSCoW · Wave | Epic (Part 1) | FRs | # FR | Stories | # US | # TC | TC IDs (sample runs) | Status |")
    W("|---|---|---|---|---|---|---|---|---|---|---|")
    for b, d in br.items():
        f = sorted(x for x in br_fr.get(b, ()) if re.fullmatch(FR_IF, x))
        u = sorted(br_us.get(b, ()))
        t = br_tc[b]
        fs = ", ".join(f) if len(f) <= 6 else ", ".join(f[:6]) + f" (+{len(f) - 6})"
        us = ", ".join(u) if len(u) <= 5 else ", ".join(u[:5]) + f" (+{len(u) - 5})"
        W(f"| {b} | {d['title']} | {d['moscow']} · {d['wave']} | {d['epic']} | {fs or '—'} | {len(f)} | {us or '—'} | {len(u)} | {len(t)} | {compress(t, 3)} | {'Covered' if t else '**Not covered**'} |")
    S["a"] = "\n".join(L)
    L.clear()

    # ---- (b) FR → US → TC
    W("| FR | Interface / operation | Wave · Epic | Aliases (DEC-017) | Stories | # TC (explicit) | # TC (total) | TC IDs (sample runs) | Status |")
    W("|---|---|---|---|---|---|---|---|---|")
    for f, d in frs.items():
        u = sorted(fr_us.get(f, ()))
        us = ", ".join(u) if len(u) <= 5 else ", ".join(u[:5]) + f" (+{len(u) - 5})"
        t = fr_tc[f]
        W(f"| {f} | {d['title']} | {d['wave']} · {d['epic'] or '—'} | {sm_alias(f)} | {us or '—'} | {len(D['fr_tc_explicit'][f])} | {len(t)} | {compress(t, 3)} | {'Covered' if t else '**Not covered**'} |")
    S["b"] = "\n".join(L)
    L.clear()
    W("| Cross-cutting FR | Requirement | Stories | # TC | TC IDs (sample runs) | Status |")
    W("|---|---|---|---|---|---|")
    for f, d in xfr.items():
        u = sorted(fr_us.get(f, ()))
        us = ", ".join(u) if len(u) <= 5 else ", ".join(u[:5]) + f" (+{len(u) - 5})"
        t = fr_tc[f]
        W(f"| {f} | {d['title']} | {us or '—'} | {len(t)} | {compress(t, 3)} | {'Covered' if t else '**Not covered**'} |")
    S["b2"] = "\n".join(L)
    L.clear()

    # ---- (d) NFR → test
    W("| NFR | Category | Requirement (Part 4.2) | Part 4.2 test method | Part 6.1 plan items | # TC | TC IDs (sample runs) | Status |")
    W("|---|---|---|---|---|---|---|---|")
    for n, d in nfr.items():
        plan = sorted(nfr_plan.get(n, ()))
        ps = ", ".join(plan[:5]) + (f" (+{len(plan) - 5})" if len(plan) > 5 else "") if plan else "—"
        t = nfr_tc[n]
        stt = "Covered (TC)" if t else ("Planned (Part 6.1), no TC" if plan else "**Method only (Part 4.2), no TC**")
        W(f"| {n} | {d['cat']} | {d['req']} | {d['method']} | {ps} | {len(t)} | {compress(t, 2)} | {stt} |")
    S["d"] = "\n".join(L)
    L.clear()

    # ---- (e) BRL
    fam = OrderedDict()
    for r in brl:
        fam.setdefault(r.rsplit("-", 1)[0], []).append(r)
    W("| Family | Rules defined | Covered | Coverage | Rules with a DT or BVA case | Uncovered rules | TCs citing the family |")
    W("|---|---|---|---|---|---|---|")
    tot_dt = 0
    for f, rules in fam.items():
        cv = [r for r in rules if brl_tc[r]]
        dtb = [r for r in rules if any(re.search(r"\b(DT|BVA)\b", tcs[x]["tech"]) for x in brl_tc[r])]
        tot_dt += len(dtb)
        unc = [r for r in rules if not brl_tc[r]]
        n_t = len(set().union(*[brl_tc[r] for r in rules]))
        W(f"| {f} | {len(rules)} | {len(cv)} | {pct(len(cv), len(rules))} | {len(dtb)} | {', '.join(unc) or '—'} | {n_t} |")
    W(f"| **Total** | **{len(brl)}** | **{cov_brl}** | **{pct(cov_brl, len(brl))}** | **{tot_dt}** | | |")
    S["e"] = "\n".join(L)
    D["summary"]["brl_dt"] = tot_dt
    L.clear()

    # ---- (f) AG/AU
    W("| Agent | Name | # TC-AI | Case IDs | Status |")
    W("|---|---|---|---|---|")
    for a, nm in ag.items():
        t = ag_tc.get(a, set())
        W(f"| {a} | {nm} | {len(t)} | {compress(t, 2)} | {'Covered' if t else '**Not covered**'} |")
    S["f1"] = "\n".join(L)
    L.clear()
    W("| Automation | Name | # TC-AU | Case IDs | Status |")
    W("|---|---|---|---|---|")
    for a, nm in au.items():
        t = au_tc.get(a, set())
        W(f"| {a} | {nm} | {len(t)} | {compress(t, 2)} | {'Covered' if t else '**Not covered**'} |")
    S["f2"] = "\n".join(L)
    L.clear()

    # ---- (g) uncovered
    unc = []
    for code, f, scope, stt in status:
        if stt != "Complete":
            unc.append(("Batch", code, f"{scope}: {stt}", "Complete the batch and re-run `build_rtm.py`", "Batch author"))
    for b in br:
        if not br_tc[b]:
            unc.append(("BR", b, br[b]["title"], "Add a story/TC or confirm the BR is realized only by non-test evidence (business milestone)", br[b]["epic"]))
    for f, d in frs.items():
        if not fr_tc[f]:
            unc.append(("FR", f, d["title"], f"Add ≥ 1 TC in the {d['epic'] or 'owning'} batch, or link existing TCs explicitly", d["epic"] or "—"))
    for f, d in xfr.items():
        if not fr_tc[f]:
            unc.append(("Cross-cutting FR", f, d["title"], "Link existing TCs that exercise it or add a TC", "EP-17 / owning epic"))
    for s, st in stories.items():
        if not us_tc[s]:
            unc.append(("Story", s, f"{len(st['acs'])} AC; {st['file']}", "Add TCs for every AC", st["epic"]))
    miss_ac = defaultdict(list)
    for a in acs:
        if not ac_cov[a]:
            miss_ac[D["ac_story"][a]].append(a)
    for s, lst in miss_ac.items():
        if us_tc.get(s):
            unc.append(("AC", f"{s}: " + ", ".join(lst), f"{len(lst)} AC without a TC", "Add a TC per AC or link the covering TC", stories[s]["epic"]))
    for r in brl:
        if not brl_tc[r]:
            unc.append(("BRL", r, brl[r], "Add a decision-table or BVA TC citing the rule", "Owner of the rule's epic"))
    for n, d in nfr.items():
        if not nfr_tc[n]:
            how = "Part 6.1 plan item exists" if nfr_plan.get(n) else "only the Part 4.2 test method exists"
            unc.append(("NFR", n, f"{d['req']} ({how})", f"Add a TC that cites {n} and executes: {d['method'][:70]}", d["epic"]))
    for a in ag:
        if not ag_tc.get(a):
            unc.append(("AG", a, ag[a], "Add TC-AI cases in Batch 6.4", "Batch 6.4"))
    for a in au:
        if not au_tc.get(a):
            unc.append(("AU", a, au[a], "Add TC-AU cases in Batch 6.4", "Batch 6.4"))
    W("| # | Type | Item | Detail | Remediation | Owner |")
    W("|---|---|---|---|---|---|")
    for i, u in enumerate(unc, 1):
        W(f"| U-{i:02d} | {u[0]} | {u[1]} | {u[2]} | {u[3]} | {u[4]} |")
    if not unc:
        W("| — | — | None | All items covered | — | — |")
    S["g"] = "\n".join(L)
    L.clear()
    D["uncovered"] = unc
    D["nfr_plan_only"] = [n for n in nfr if not nfr_tc[n] and nfr_plan.get(n)]
    return S


def write_csv(D):
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    frs, xfr, br, brs, brl, nfr, stories = (D[k] for k in ("frs", "xfr", "br", "brs", "brl", "nfr", "stories"))
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["requirement_type", "requirement_id", "title", "epic", "wave", "linked_fr", "linked_us", "aliases",
                    "tc_count", "tc_ids", "coverage_flag"])
        for b, d in br.items():
            t = D["br_tc"][b]
            w.writerow(["BR", b, d["title"], d["epic"], d["wave"], " ".join(sorted(D["br_fr"].get(b, ()))),
                        " ".join(sorted(D["br_us"].get(b, ()))), "", len(t), compress(t), "Covered" if t else "Not covered"])
        for b, d in brs.items():
            t = D["br_tc"][b]
            w.writerow(["BR-S", b, d["title"], "", "", " ".join(sorted(D["br_fr"].get(b, ()))),
                        " ".join(sorted(D["br_us"].get(b, ()))), "", len(t), compress(t), "Covered" if t else "Not covered"])
        for f, d in frs.items():
            t = D["fr_tc"][f]
            w.writerow(["FR", f, d["title"], d["epic"], d["wave"], "", " ".join(sorted(D["fr_us"].get(f, ()))), sm_alias(f),
                        len(t), compress(t), "Covered" if t else "Not covered"])
        for f, d in xfr.items():
            t = D["fr_tc"][f]
            w.writerow(["FR-XC", f, d["title"], "", "", "", " ".join(sorted(D["fr_us"].get(f, ()))), "", len(t), compress(t),
                        "Covered" if t else "Not covered"])
        for s, st in stories.items():
            t = D["us_tc"][s]
            fr = " ".join(sorted(x for x in st["links"] if re.fullmatch(rf"{FR_IF}|{FR_XC}", x)))
            w.writerow(["US", s, f"{len(st['acs'])} AC", st["epic"], "", fr, "", "", len(t), compress(t), "Covered" if t else "Not covered"])
            for a in st["acs"]:
                ta = D["ac_cov"][a]
                w.writerow(["AC", a, "", st["epic"], "", "", s, "", len(ta), compress(ta), "Covered" if ta else "Not covered"])
        for r, title in brl.items():
            t = D["brl_tc"][r]
            w.writerow(["BRL", r, title, "", "", "", "", "", len(t), compress(t), "Covered" if t else "Not covered"])
        for n, d in nfr.items():
            t = D["nfr_tc"][n]
            plan = sorted(D["nfr_plan"].get(n, ()))
            flag = "Covered" if t else ("Plan only" if plan else "Not covered")
            w.writerow(["NFR", n, d["req"], d["epic"], "", "", "", "; ".join(plan), len(t), compress(t), flag])
        for a, nm in D["ag"].items():
            t = D["ag_tc"].get(a, set())
            w.writerow(["AG", a, nm, "", "", "", "", "", len(t), compress(t), "Covered" if t else "Not covered"])
        for a, nm in D["au"].items():
            t = D["au_tc"].get(a, set())
            w.writerow(["AU", a, nm, "", "", "", "", "", len(t), compress(t), "Covered" if t else "Not covered"])


TEMPLATE_MARK = re.compile(r"<!--RTM:(\w+)-->")


def main():
    D = build()
    S = render(D)
    sm = D["summary"]
    if "--check" in sys.argv:
        print({k: v for k, v in sm.items()})
        print("uncovered:", len(D["uncovered"]))
        for u in D["uncovered"][:80]:
            print("  ", u[:3])
        return
    write_csv(D)
    tpl = TEMPLATE
    if "--template" in sys.argv:
        tpl = read(sys.argv[sys.argv.index("--template") + 1])
    vals = dict(S)
    vals.update({
        "BR_PCT": pct(*sm["br"]), "BR_N": f"{sm['br'][0]} of {sm['br'][1]}",
        "FR_PCT": pct(*sm["fr"]), "FR_N": f"{sm['fr'][0]} of {sm['fr'][1]}",
        "XFR_N": f"{sm['xfr'][0]} of {sm['xfr'][1]}", "XFR_PCT": pct(*sm["xfr"]),
        "US_PCT": pct(*sm["us"]), "US_N": f"{sm['us'][0]} of {sm['us'][1]}",
        "AC_PCT": pct(*sm["ac"]), "AC_N": f"{sm['ac'][0]} of {sm['ac'][1]}",
        "BRL_PCT": pct(*sm["brl"]), "BRL_N": f"{sm['brl'][0]} of {sm['brl'][1]}", "BRL_DT": str(sm["brl_dt"]),
        "NFR_TC_PCT": pct(sm["nfr"][0], sm["nfr"][2]), "NFR_ANY_PCT": pct(sm["nfr"][1], sm["nfr"][2]),
        "NFR_TC_N": f"{sm['nfr'][0]} of {sm['nfr'][2]}", "NFR_ANY_N": f"{sm['nfr'][1]} of {sm['nfr'][2]}",
        "AG_N": f"{sm['ag'][0]} of {sm['ag'][1]}", "AU_N": f"{sm['au'][0]} of {sm['au'][1]}",
        "TC_N": str(sm["tc"][0]), "TC_E": str(sm["tc"][1]), "TC_AI": str(sm["tc"][2]), "TC_AU": str(sm["tc"][3]),
        "UNC_N": str(len(D["uncovered"])), "BRS_N": f"{sm['brs'][0]} of {sm['brs'][1]}",
        "NFR_PLAN_ONLY": ", ".join(D["nfr_plan_only"]) or "none",
        "BRL_STATED": str(D["brl_stated"]), "BRL_DEFINED": str(len(D["brl"])),
    })
    out = TEMPLATE_MARK.sub(lambda m: vals.get(m.group(1), m.group(0)), tpl)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {OUT_MD} and {OUT_CSV}")
    print({k: v for k, v in sm.items()}, "uncovered", len(D["uncovered"]))


from rtm_template_text import TEMPLATE  # noqa: E402  (narrative kept next to the script)

if __name__ == "__main__":
    main()
