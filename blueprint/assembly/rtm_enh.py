#!/usr/bin/env python3
"""Source-pack enhancement layer of the RTM (Part 6.6 sections h, i, j).

Imported by build_rtm.py. Parses every Part-*.md file (except the generated Part 6.6 and Part 9.2) for the
enhancement IDs added by the ten source-pack parts (2.6, 2.7, 3.4, 3.5, 3.6, 4.4, 6.8, 6.9, 7.4, 8.3) and by
the closure batch 6.10, and the coverage CSVs in final/coverage/ for the source-pack aliases.

Link rule (generic, no hand-entered data): a table row "belongs to" the IDs in its first cell (its subject; in
grid tables with several TC columns every TC cell is a subject). Every other ID in the row is a link of the
subject, with range and list expansion (TC-ENH-B-011…014, TC-ENH-F-007, 008, FR-ENH-I-001…003,
FR-ENH-D-001, -002). Story headings (US-<EP>-E<G><nn>) contribute the IDs in their field table and their
AC-…-E… scenarios. A requirement is covered by a test when (1) a test row (TC/LT/VER) cites it, or (2) one of
the requirement's own rows cites a defined test.
"""
import csv
import glob
import os
import re
from collections import OrderedDict, defaultdict

FR_ENH = r"FR-ENH-[A-Z]-\d{3}"
NFR_ENH = r"NFR-ENH-[A-Z]-\d{2}"
US_E = r"US-\d{2}-E[A-Z]\d{2}"
AC_E = r"AC-\d{2}-?E[A-Z]\d{2}-\d{2}"
TC_ENH = r"TC-ENH-[A-Z]-[A-Z]?\d{2,3}"
LT_ENH = r"LT-ENH-[A-Z]-\d{2}"
VER_ENH = r"VER-ENH-[A-Z]-\d{3}"
OKPI = r"OKPI-\d{2}"
AG_N = r"AG-03[78]"
AU_N = r"AU-0(?:4[4-9]|5[0-2])"
QC = r"QC-\d{2,3}"
SM_SIT = r"SM-SIT-[AFM]\d{3}"
SM_UAT = r"SM-UAT-[SF]\d{3}"
SM_UT = r"SM-UT-\d{3}"
SM_OP = r"SM-OP-\d{3}"
SM_UXAPI = r"SM-UX-API-\d{2}"
# tests already defined in the baseline batches (6.2–6.5, 6.7) and the Part 6.1 plan items
TC_OLD = r"TC-(?:AI-AG\d{3}|AU-AU\d{3}|NFR|FLT|BRS|\d{2})-\d{3}"
LT_OLD = r"LT-\d{2}(?![\d-])"
VER_OLD = r"VER-\d{3}"
TEST_ANY = rf"(?:{TC_ENH}|{LT_ENH}|{VER_ENH}|{TC_OLD}|{VER_OLD})"

ENH_FAMILIES = [FR_ENH, NFR_ENH, US_E, AC_E, TC_ENH, LT_ENH, VER_ENH, OKPI, AG_N, AU_N, QC, SM_SIT, SM_UAT, SM_UT,
                SM_OP, SM_UXAPI, TC_OLD, VER_OLD, r"(?<!TC-)(?<!-)NFR-\d{3}", r"(?<![A-Z-])KPI-\d{2}\b",
                r"FR-(?:W\d{2}|A\d{3}|OP\d{3})", r"US-\d{4}", r"BRL-[A-Z]{2,4}-\d{2}", LT_OLD]
ANY = re.compile("|".join(f"(?:{p})" for p in ENH_FAMILIES))

# range / list expansion for the enhancement families with a numeric tail
_EXP = re.compile(r"((?:TC-ENH|FR-ENH|NFR-ENH|LT-ENH|VER-ENH)-[A-Z]-[A-Z]?|OKPI-|US-\d{2}-E[A-Z]|QC-|AU-0|SM-SIT-[AFM]|SM-UAT-[SF]|SM-UT-)"
                  r"(\d{2,3})((?:\s*(?:…|–|\.\.\.|,\s*-?|/\s*-?|\s+and\s+|\s+to\s+)\s*(?:\1)?\d{2,3}\b)+)")


def expand(text):
    out = []
    for m in _EXP.finditer(text):
        pref, first, tail = m.group(1), m.group(2), m.group(3)
        width = len(first)
        prev = int(first)
        out.append(pref + first)
        for sm in re.finditer(r"(…|–|\.\.\.|,|/|and|to)\s*-?\s*(?:" + re.escape(pref) + r")?(\d{2,3})\b", tail):
            sep, n = sm.group(1), sm.group(2)
            if len(n) != width:
                break
            n = int(n)
            if sep in ("…", "–", "...", "to"):
                if 0 < n - prev <= 400:
                    out += [f"{pref}{i:0{width}d}" for i in range(prev + 1, n + 1)]
            else:
                out.append(f"{pref}{n:0{width}d}")
            prev = n
    return out


def all_ids(text):
    return list(dict.fromkeys(ANY.findall(text) + expand(text)))


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _clean(s):
    return re.sub(r"\*\*|`", "", s).strip()


def ac_story(ac):
    m = re.match(r"AC-(\d{2})-?(E[A-Z]\d{2})-\d{2}$", ac)
    return f"US-{m.group(1)}-{m.group(2)}" if m else None


class Enh:
    def __init__(self, bp):
        self.bp = bp
        self.files = [f for f in sorted(glob.glob(bp + "Part-*.md"))
                      if not re.search(r"Part-06-6_|Part-09-2_|Part-09-3_", os.path.basename(f))]
        self.rows = []                    # (file, header, cells, subjects, ids)
        self.subj_rows = defaultdict(list)  # id -> row indexes where it is the subject
        self.cited_by = defaultdict(set)   # id -> subject ids of rows that cite it
        self.defs = defaultdict(OrderedDict)  # family -> id -> dict(title, file)
        self.story_links = defaultdict(set)
        self.story_acs = defaultdict(list)
        self.family_users = defaultdict(set)   # negative-family code (N01…) -> operation tests applying it
        self.parse()

    # ------------------------------------------------------------------ parsing
    def parse(self):
        fams = dict(FR=FR_ENH, NFR=NFR_ENH, US=US_E, TC=TC_ENH, LT=LT_ENH, VER=VER_ENH, OKPI=OKPI, AG=AG_N, AU=AU_N)
        for f in self.files:
            base = os.path.basename(f)
            text = open(f, encoding="utf-8").read()
            lines = text.split("\n")
            header = None
            for i, line in enumerate(lines):
                if not line.startswith("|"):
                    header = None if not line.strip() else header
                    continue
                if re.match(r"^\|\s*:?-{3,}", line):
                    continue
                c = _cells(line)
                if i + 1 < len(lines) and re.match(r"^\|\s*:?-{3,}", lines[i + 1]):
                    header = c
                    continue
                if not c:
                    continue
                first = _clean(c[0])
                grid = header and sum(1 for h in header if h.strip().upper() == "TC") >= 2
                if grid:
                    subj = [x for x in (_clean(y) for y in c) if re.fullmatch(TC_ENH, x)]
                else:
                    subj = all_ids(first)
                    if not subj and len(c) > 1 and re.fullmatch(TC_ENH, _clean(c[1])):
                        subj = [_clean(c[1])]     # rows keyed by a family code (N01 | TC-ENH-D-N01 | …)
                ids = all_ids(line)
                if header and subj:
                    for j, h in enumerate(header):
                        if h.lower().startswith("negative famil") and j < len(c):
                            for code in re.findall(r"N\d{2}", c[j]):
                                self.family_users[code].update(subj)
                idx = len(self.rows)
                self.rows.append((base, header, c, subj, ids))
                for s in subj:
                    self.subj_rows[s].append(idx)
                    for x in ids:
                        if x != s:
                            self.cited_by[x].add(s)
                # definitions: the first cell is exactly one ID (or a TC range) of a family
                for fam, pat in fams.items():
                    if fam == "TC":
                        cand = subj if (grid or re.fullmatch(rf"{TC_ENH}(?:\s*(?:…|–)\s*\d{{3}})?", first)
                                        or (subj and re.fullmatch(TC_ENH, _clean(c[1]) if len(c) > 1 else ""))) else []
                    elif fam == "LT":
                        cand = re.findall(LT_ENH, first) if len(re.findall(LT_ENH, first)) == 1 else []
                    else:
                        cand = [first] if re.fullmatch(pat, first) else []
                    for s in cand:
                        if s not in self.defs[fam]:
                            title = _clean(c[1]) if len(c) > 1 and not grid else ("screen " + _clean(c[c.index(next(y for y in c if _clean(y) == s)) + 1]) if grid else "")
                            self.defs[fam][s] = dict(title=re.sub(r"\s+", " ", title)[:110], file=base, row=line)
            # story headings
            for m in re.finditer(rf"^(#{{3,6}}) ({US_E})\b([^\n]*)\n(.*?)(?=^#{{2,6}} |\Z)", text, re.S | re.M):
                sid, title, body = m.group(2), m.group(3).strip(" ·-:"), m.group(4)
                field_rows = "\n".join(ln for ln in body.split("\n") if ln.startswith("|"))
                self.story_links[sid].update(x for x in all_ids(field_rows) if x != sid)
                acs = re.findall(rf"Scenario(?: Outline)?: ({AC_E})", body)
                self.story_acs[sid] += [a for a in acs if a not in self.story_acs[sid]]
                if sid not in self.defs["US"]:
                    self.defs["US"][sid] = dict(title=_clean(title)[:110], file=base, row="")
            # Gherkin features named after a story (Part 2.7a style)
            for m in re.finditer(rf"^Feature: ({US_E})\b([^\n]*)\n(.*?)(?=^```)", text, re.S | re.M):
                sid = m.group(1)
                self.story_links[sid].update(x for x in all_ids(m.group(3)) if x != sid)
                if sid not in self.defs["US"]:
                    self.defs["US"][sid] = dict(title=_clean(m.group(2))[:110], file=base, row="")
            # AG-037/038 headings (Part 7.4b spec cards)
            for m in re.finditer(rf"^#{{3,6}} ({AG_N}) ([^\n]+)", text, re.M):
                if m.group(1) not in self.defs["AG"]:
                    self.defs["AG"][m.group(1)] = dict(title=_clean(m.group(2))[:110], file=base, row="")
        # story table rows also count as story links
        for sid in list(self.defs["US"]):
            for i in self.subj_rows.get(sid, []):
                self.story_links[sid].update(x for x in self.rows[i][4] if x != sid)
        # Gherkin AC also count when cited
        self.ac_of = {a: s for s, lst in self.story_acs.items() for a in lst}

    # ------------------------------------------------------------------ queries
    def own_ids(self, x):
        out = set()
        for i in self.subj_rows.get(x, []):
            out.update(self.rows[i][4])
        out.discard(x)
        return out

    def tests_of(self, x, defined_tests):
        """Tests that cite x, plus defined tests cited in x's own rows."""
        t = {s for s in self.cited_by.get(x, ()) if s in defined_tests}
        t |= {y for y in self.own_ids(x) if y in defined_tests}
        return t


# ====================================================================== build (h), (i), (j)
def _first(pat, text, default=""):
    m = re.search(pat, text)
    return m.group(0) if m else default


def _short(ids, n=4):
    ids = sorted(ids)
    return (", ".join(ids[:n]) + (f" (+{len(ids) - n})" if len(ids) > n else "")) if ids else "—"


def build_enh(D, bp):
    """Compute the source-pack enhancement layer; D is the dict returned by build_rtm.build()."""
    import build_rtm as B
    E = Enh(bp)
    tests = (set(D["tcs"]) | set(D["ver"]) | set(E.defs["TC"]) | set(E.defs["LT"]) | set(E.defs["VER"])
             | {f"LT-{i:02d}" for i in range(1, 13)})
    X = dict(E=E, tests=tests)

    # ---------------- FR-ENH -> US -> TC
    fr = E.defs["FR"]
    fr_us = defaultdict(set)
    for s in E.defs["US"]:
        for r in E.story_links[s]:
            if re.fullmatch(FR_ENH, r):
                fr_us[r].add(s)
    for f in fr:                                   # FR rows that name their story
        for y in E.own_ids(f):
            if re.fullmatch(US_E, y) and y in E.defs["US"]:
                fr_us[f].add(y)
    fr_tc_direct = {f: E.tests_of(f, tests) for f in fr}
    us_tc_direct = {}
    for s in E.defs["US"]:
        t = E.tests_of(s, tests) | {y for y in E.story_links[s] if y in tests}
        for a in E.story_acs.get(s, []):
            t |= E.tests_of(a, tests)
        us_tc_direct[s] = t
    fr_tc = {f: fr_tc_direct[f] | set().union(*[us_tc_direct[s] for s in fr_us[f]] or [set()]) for f in fr}
    us_fr = {s: {r for r in E.story_links[s] if re.fullmatch(FR_ENH, r)} | {f for f in fr if s in fr_us[f]}
             for s in E.defs["US"]}
    us_tc_via = {s: set().union(*[fr_tc_direct.get(f, set()) for f in us_fr[s]] or [set()]) for s in E.defs["US"]}
    us_tc = {s: us_tc_direct[s] | us_tc_via[s] for s in E.defs["US"]}
    fr_meta = {}
    for f, d in fr.items():
        row = " ".join(E.rows[i][2] and "|".join(E.rows[i][2]) for i in E.subj_rows[f][:1]) or d["row"]
        fr_meta[f] = dict(wave=_first(r"\bW\d(?:–W\d)?\b", d["row"], "—"), epic=_first(r"EP-\d{2}", d["row"], "—"),
                          group=f[7])
    X.update(fr=fr, fr_us=fr_us, fr_tc=fr_tc, fr_tc_direct=fr_tc_direct, us_tc=us_tc, us_tc_direct=us_tc_direct,
             us_tc_via=us_tc_via, us_fr=us_fr, fr_meta=fr_meta)

    # ---------------- NFR-ENH and LT-ENH
    nfr_e = E.defs["NFR"]
    nfr_e_tc = {}
    for n in nfr_e:
        t = E.tests_of(n, tests)
        via = set()
        for r in E.own_ids(n):
            if re.fullmatch(FR_ENH, r):
                via |= fr_tc.get(r, set())
        nfr_e_tc[n] = (t, via)
    lt_req = {l: {y for y in E.own_ids(l) | E.cited_by.get(l, set())
                  if re.fullmatch(rf"{NFR_ENH}|(?<!TC-)NFR-\d{{3}}|{OKPI}|{FR_ENH}|SLO-\d{{2}}", y)} for l in E.defs["LT"]}
    lt_req = {l: v | {y for y in re.findall(rf"{NFR_ENH}|NFR-\d{{3}}|{OKPI}|{FR_ENH}", " ".join(
        "|".join(E.rows[i][2]) for i in E.subj_rows.get(l, [])))} for l, v in lt_req.items()}
    X.update(nfr_e=nfr_e, nfr_e_tc=nfr_e_tc, lt_req=lt_req)

    # ---------------- OKPI -> NFR / KPI / TC
    ok = E.defs["OKPI"]
    ok_info = {}
    mand = set()
    for o in ok:
        own = E.own_ids(o)
        txt = " ".join("|".join(E.rows[i][2]) for i in E.subj_rows[o])
        for i in E.subj_rows[o]:
            hdr = [h.lower() for h in (E.rows[i][1] or [])]
            for j, h in enumerate(hdr):
                if h.startswith("mandatory") and j < len(E.rows[i][2]) and E.rows[i][2][j].strip().lower().startswith("yes"):
                    mand.add(o)
        nfrs = sorted(set(re.findall(r"(?<!TC-)NFR-\d{3}", txt)) | set(B.expand_req_ranges(txt)) & set(D["nfr"]))
        nfrs = [n for n in nfrs if n in D["nfr"]]
        nfre = sorted({y for y in own if re.fullmatch(NFR_ENH, y)})
        kpis = sorted(set(re.findall(r"(?<![A-Z-])KPI-\d{2}\b", txt)))
        slos = sorted(set(re.findall(r"SLO-\d{2}", txt)))
        direct = E.tests_of(o, tests)
        via = set()
        for n in nfrs:
            via |= D["nfr_tc"].get(n, set()) | D["nfr_ver"].get(n, set())
        for n in nfre:
            via |= nfr_e_tc[n][0] | nfr_e_tc[n][1]
        ok_info[o] = dict(metric=ok[o]["title"], nfr=nfrs, nfre=nfre, kpi=kpis, slo=slos, direct=direct, via=via)
    X.update(ok=ok, ok_info=ok_info, ok_mand=mand)

    # ---------------- AG-037/038, AU-044…052
    agau = OrderedDict(list(E.defs["AG"].items()) + list(E.defs["AU"].items()))
    agau_tc = {}
    for a in agau:
        t = E.tests_of(a, tests)
        via = set()
        frs = {y for y in E.own_ids(a) if re.fullmatch(FR_ENH, y)} | {f for f in fr if a in E.own_ids(f)}
        for f in frs:
            via |= fr_tc.get(f, set())
        agau_tc[a] = (t, via, frs)
    X.update(agau=agau, agau_tc=agau_tc)

    # ---------------- (j) source-pack aliases
    C = bp + "final/coverage/"

    def rcsv(n):
        with open(C + n, encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    g = rcsv("G_test_mapping.csv")
    src = OrderedDict()
    for r in g:
        refs = " ".join([r["primary_tcs"], r["supporting_tcs"], r["tc_enh"]])
        t = {x for x in re.findall(TEST_ANY, refs) if x in tests}
        t |= {s for s in E.cited_by.get(r["source_id"], ()) if s in tests}
        undefined = sorted({x for x in re.findall(TEST_ANY, refs) if x not in tests})
        src[r["source_id"]] = dict(level=r["level"], title=r["title"], req=r["bp_requirement"], status=r["status"],
                                   tests=t, undefined=undefined)
    d = rcsv("D_api_mapping.csv")
    api = OrderedDict()
    sit_api = {}
    for r in d:
        t = {x for x in re.findall(TEST_ANY, r["test"]) if x in tests} | {s for s in E.cited_by.get(r["source_id"], ()) if s in tests}
        api[r["source_id"]] = dict(sit=r["sit_id"], method=r["method"], path=r["path"], bp=r["blueprint_ops"],
                                   status=r["status"], tests=t)
        if r["sit_id"]:
            sit_api[r["sit_id"]] = t
    s = rcsv("H_sit_alias_map.csv")
    sit = OrderedDict()
    for r in s:
        frs = [x for x in r["blueprint_frs"].split(";") if x]
        sts = [x.strip() for x in r["blueprint_stories"].split(",") if x.strip()]
        rule = set()
        for u in sts:
            for tc in D["us_tc"].get(u, ()):
                if tc in D["tcs"] and set(frs) & D["tcs"][tc]["links"]:
                    rule.add(tc)
        sit[r["sm_sit_id"]] = dict(frs=frs, stories=sts, rule=rule, api=sit_api.get(r["sm_sit_id"], set()),
                                   src=src.get(r["sm_sit_id"], {}).get("tests", set()))
    q = rcsv("H_qc_map.csv")

    def req_tests(rid):
        out = set()
        for key in ("br_tc", "fr_tc", "us_tc", "brl_tc", "nfr_tc", "ac_cov"):
            out |= set(D[key].get(rid, set()) or set())
        out |= D["ver_req"].get(rid, set())
        out |= fr_tc.get(rid, set()) | us_tc.get(rid, set())
        if rid in nfr_e_tc:
            out |= nfr_e_tc[rid][0] | nfr_e_tc[rid][1]
        if rid in ok_info:
            out |= ok_info[rid]["direct"] | ok_info[rid]["via"]
        if rid in tests:
            out.add(rid)
        return out
    qc = OrderedDict()
    for r in q:
        refs = r["blueprint_verification_refs"] + " ; " + r["layer_anchor_refs"]
        direct = {x for x in E.cited_by.get(r["qc_id"], ()) if x in tests} | {x for x in re.findall(TEST_ANY, refs) if x in tests}
        ref_ids = [x for x in dict.fromkeys(B.req_ids(r["blueprint_verification_refs"]) + all_ids(r["blueprint_verification_refs"]))]
        via = set()
        via_refs = []
        for x in ref_ids:
            t = req_tests(x)
            if t:
                via |= t
                via_refs.append(x)
        qc[r["qc_id"]] = dict(layer=r["layer_id"], check=r["check"], priority=r["priority"], gate=r["blueprint_gate"],
                              status=r["status"], direct=direct, via=via, via_refs=via_refs)
    X.update(src=src, api=api, sit=sit, qc=qc, req_tests=req_tests)
    return X


# ====================================================================== render
def _pct(a, b):
    return f"{100.0 * a / b:.1f}%" if b else "n/a"


def render_enh(D, X, compress):
    E = X["E"]
    S = {}
    L = []
    W = L.append
    fr, fr_tc, fr_us, us_tc = X["fr"], X["fr_tc"], X["fr_us"], X["us_tc"]
    unc = []

    # -------- levels
    n_fr = len(fr); c_fr = sum(1 for f in fr if fr_tc[f])
    c_fr_d = sum(1 for f in fr if X["fr_tc_direct"][f])
    us = E.defs["US"]; n_us = len(us); c_us = sum(1 for s in us if us_tc[s])
    c_us_d = sum(1 for s in us if X["us_tc_direct"][s])
    acs = [a for s in us for a in E.story_acs.get(s, [])]
    ac_cov = {a: E.tests_of(a, X["tests"]) | X["us_tc"][E.ac_of[a]] for a in acs}
    c_ac = sum(1 for a in acs if ac_cov[a])
    ne = X["nfr_e"]; c_ne = sum(1 for n in ne if X["nfr_e_tc"][n][0] | X["nfr_e_tc"][n][1])
    lt = E.defs["LT"]; c_lt = sum(1 for l in lt if X["lt_req"][l])
    tce = E.defs["TC"]
    tce_req = {t: {y for y in E.own_ids(t) if re.fullmatch(rf"{FR_ENH}|{US_E}|{NFR_ENH}|{OKPI}|{AG_N}|{AU_N}|{QC}|{SM_SIT}|{SM_UAT}|{SM_UT}|{SM_OP}|{SM_UXAPI}|FR-(?:W\d{{2}}|A\d{{3}}|OP\d{{3}})|(?<!TC-)NFR-\d{{3}}|BRL-[A-Z]{{2,4}}-\d{{2}}|US-\d{{4}}", y)} for t in tce}
    # grid rows (Part 2.7b) link a TC to its screen: count the screen as its requirement anchor
    for t in tce:
        if not tce_req[t] and re.match(r"screen [AW]\d", E.defs["TC"][t]["title"]):
            tce_req[t] = {E.defs["TC"][t]["title"][7:]}
        if not tce_req[t]:                # any other requirement, rule or source-aspect ID in the row (AP-, ABAC-, V-05, F15-060, …)
            row = " ".join("|".join(E.rows[k][2][1:]) for k in E.subj_rows.get(t, []))
            tce_req[t] = {y for y in re.findall(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b", row)
                          if not re.fullmatch(TEST_ANY, y) and y != t and not y.startswith("TC-")}
            tce_req[t] |= set(re.findall(r"\b[Dd]oc(?:ument)?s? \d{2}\b", row))
        tce_req[t] |= {y for y in E.own_ids(t) if y in X["lt_req"] and X["lt_req"][y]}   # executes a traced load test
        m = re.fullmatch(r"TC-ENH-D-(N\d{2})", t)
        if m and E.family_users.get(m.group(1)):   # negative family applied by the operation tests (Part 3.5 §3.5.5.12.1)
            tce_req[t] |= {f"{len(E.family_users[m.group(1)])} operation tests"}
    c_tce = sum(1 for t in tce if tce_req[t])
    ok = X["ok"]; oi = X["ok_info"]
    c_ok = sum(1 for o in ok if oi[o]["direct"] or oi[o]["via"])
    c_ok_d = sum(1 for o in ok if oi[o]["direct"])
    mand = X["ok_mand"]; c_mand = sum(1 for o in mand if oi[o]["direct"] or oi[o]["via"])
    agau = X["agau"]; c_agau = sum(1 for a in agau if X["agau_tc"][a][0] | X["agau_tc"][a][1])
    src = X["src"]
    lv = OrderedDict((k, [x for x in src if src[x]["level"] == k]) for k in ("Unit", "SIT", "UAT"))
    c_src = {k: sum(1 for x in v if src[x]["tests"]) for k, v in lv.items()}
    api = X["api"]; c_api = sum(1 for a in api if api[a]["tests"])
    sit = X["sit"]; c_sit = sum(1 for a in sit if sit[a]["rule"] | sit[a]["api"] | sit[a]["src"])
    qc = X["qc"]; c_qc = sum(1 for a in qc if qc[a]["direct"] | qc[a]["via"])
    c_qc_d = sum(1 for a in qc if qc[a]["direct"])
    n_k = sum(1 for t in tce if t.startswith("TC-ENH-K-"))
    n_verk = len(E.defs["VER"])
    W("| Level | Items in scope | Covered (direct) | Covered (total) | Coverage | Basis of the count |")
    W("|---|---|---|---|---|---|")
    W(f"| (h) Source-pack FRs (FR-ENH-A…J) | {n_fr} | {c_fr_d} | {c_fr} | **{_pct(c_fr, n_fr)}** | Direct = a test row cites the FR or the FR row names a defined test; total adds tests of the FR's enhancement stories |")
    W(f"| (h) Source-pack stories (US-<EP>-E<G><nn>) | {n_us} | {c_us_d} | {c_us} | **{_pct(c_us, n_us)}** | Direct = a test cites the story or one of its AC; total adds the tests of the FR-ENH the story realizes |")
    W(f"| (h) Source-pack acceptance criteria (AC-…-E…) | {len(acs)} | {sum(1 for a in acs if E.tests_of(a, X['tests']))} | {c_ac} | **{_pct(c_ac, len(acs))}** | Direct = a test cites the AC; total = AC of a covered story |")
    W(f"| (h) Source-pack NFRs (NFR-ENH) | {len(ne)} | {sum(1 for n in ne if X['nfr_e_tc'][n][0])} | {c_ne} | **{_pct(c_ne, len(ne))}** | Test or load test cites the NFR, or the NFR row names one; total adds tests of the FR-ENH it points to |")
    W(f"| (h) Source-pack load tests (LT-ENH) traced to a requirement | {len(lt)} | {c_lt} | {c_lt} | **{_pct(c_lt, len(lt))}** | LT row or a citing row names an NFR, NFR-ENH, OKPI or FR-ENH |")
    W(f"| (h) Source-pack test cases (TC-ENH) traced to a requirement | {len(tce)} | {c_tce} | {c_tce} | **{_pct(c_tce, len(tce))}** | TC row names a requirement, story, source alias or screen ({n_k} closure TC-ENH-K in Part 6.10) |")
    W(f"| (i) Optimization KPIs (OKPI-01…35) | {len(ok)} | {c_ok_d} | {c_ok} | **{_pct(c_ok, len(ok))}** | Direct = a test cites the OKPI or an OKPI row names a test; total adds the TC-NFR/VER of its NFRs and the tests of its NFR-ENH |")
    W(f"| (i) of which mandatory (blocking) OKPIs | {len(mand)} | {sum(1 for o in mand if oi[o]['direct'])} | {c_mand} | **{_pct(c_mand, len(mand))}** | As above; mandatory = 'Yes' in a Mandatory column |")
    W(f"| (h) New agents and automations (AG-037/038, AU-044…052) | {len(agau)} | {sum(1 for a in agau if X['agau_tc'][a][0])} | {c_agau} | **{_pct(c_agau, len(agau))}** | Direct = a test cites the AG/AU; total adds tests of the FR-ENH that specifies it |")
    for k, v in lv.items():
        W(f"| (j) Source tests SM-{'UT' if k == 'Unit' else k} ({k}) | {len(v)} | {c_src[k]} | {c_src[k]} | **{_pct(c_src[k], len(v))}** | Primary, supporting or TC-ENH test of `G_test_mapping.csv` that is defined in the blueprint, or a test row citing the alias |")
    W(f"| (j) **All source tests** (document 38: 799) | {len(src)} | {sum(c_src.values())} | {sum(c_src.values())} | **{_pct(sum(c_src.values()), len(src))}** | Sum of the three rows above |")
    W(f"| (j) SIT aliases SM-SIT-A### (operation SIT) | {len(sit)} | {c_sit} | {c_sit} | **{_pct(c_sit, len(sit))}** | Alias rule of `H_sit_alias_map.csv` (TCs of the listed stories carrying the FR), the TC-ENH-D operation test or the source-test mapping |")
    W(f"| (j) Source API operations (SM-OP, SM-UX-API) | {len(api)} | {c_api} | {c_api} | **{_pct(c_api, len(api))}** | Operation test of `D_api_mapping.csv` defined in Part 3.5 |")
    W(f"| (j) Quality controls (QC) | {len(qc)} | {c_qc_d} | {c_qc} | **{_pct(c_qc, len(qc))}** | Direct = a test or VER row cites the QC; total adds the tests and VER of the requirements in its blueprint verification references (`H_qc_map.csv`) |")
    W(f"| Closure items parsed (Part 6.10) | {n_k + n_verk} | — | — | — | {n_k} TC-ENH-K test cases · {n_verk} VER-ENH-K verification items |")
    S["levels_enh"] = "\n".join(L); L.clear()
    X["summary"] = dict(fr=(c_fr, n_fr), us=(c_us, n_us), ac=(c_ac, len(acs)), nfre=(c_ne, len(ne)), lt=(c_lt, len(lt)),
                        tce=(c_tce, len(tce)), ok=(c_ok, len(ok)), mand=(c_mand, len(mand)), agau=(c_agau, len(agau)),
                        src=(sum(c_src.values()), len(src)), src_lv={k: (c_src[k], len(v)) for k, v in lv.items()},
                        sit=(c_sit, len(sit)), api=(c_api, len(api)), qc=(c_qc, len(qc)), k=(n_k, n_verk))

    # -------- per group
    W("| Group (enhancement part) | FR-ENH | Covered | Stories | Covered | TC-ENH defined |")
    W("|---|---|---|---|---|---|")
    grp_part = dict(A="2.6", B="3.4", C="2.7", D="3.5", E="3.6", F="7.4", G="6.8", H="6.9", I="4.4", J="8.3", K="6.10")
    for gl in sorted({f[7] for f in fr} | {t[7] for t in tce}):
        gf = [f for f in fr if f[7] == gl]
        gu = [s for s in us if re.match(rf"US-\d{{2}}-E{gl}", s)]
        W(f"| {gl} (Part {grp_part.get(gl, '?')}) | {len(gf)} | {sum(1 for f in gf if fr_tc[f])} | {len(gu)} | {sum(1 for s in gu if us_tc[s])} | {sum(1 for t in tce if t[7] == gl)} |")
    S["groups_enh"] = "\n".join(L); L.clear()

    # -------- (h) FR-ENH -> US -> TC
    W("| FR-ENH | Requirement (condensed) | Wave · Epic | Defined in | Stories | # TC (direct) | # TC (total) | Test IDs (sample runs) | Status |")
    W("|---|---|---|---|---|---|---|---|---|")
    for f, d in fr.items():
        m = X["fr_meta"][f]
        t = fr_tc[f]
        W(f"| {f} | {d['title'][:90]} | {m['wave']} · {m['epic']} | {d['file'][5:12]} | {_short(fr_us[f], 3)} | {len(X['fr_tc_direct'][f])} | {len(t)} | {compress(t, 3)} | {'Covered' if t else '**Not covered**'} |")
        if not t:
            unc.append(("FR-ENH", f, d["title"][:80], "Add a TC-ENH-K test case in Part 6.10 that cites the FR", m["epic"]))
    S["h"] = "\n".join(L); L.clear()
    W("| Story | Title | Defined in | FR-ENH realized | # AC | # TC (direct) | # TC (via FR) | Test IDs (sample runs) | Status |")
    W("|---|---|---|---|---|---|---|---|---|")
    for s, d in us.items():
        t = us_tc[s]
        W(f"| {s} | {d['title'][:70] or '—'} | {d['file'][5:12]} | {_short(X['us_fr'][s], 3)} | {len(E.story_acs.get(s, []))} | {len(X['us_tc_direct'][s])} | {len(X['us_tc_via'][s])} | {compress(t, 3)} | {'Covered' if t else '**Not covered**'} |")
        if not t:
            unc.append(("Story", s, d["title"][:80], "Add a TC-ENH-K test case per acceptance scenario in Part 6.10 citing the story", "EP-" + s[3:5]))
    S["h2"] = "\n".join(L); L.clear()
    W("| NFR-ENH | Requirement | # tests (direct) | # tests (via FR-ENH) | Tests | Status |")
    W("|---|---|---|---|---|---|")
    for n, d in ne.items():
        a, b = X["nfr_e_tc"][n]
        W(f"| {n} | {d['title']} | {len(a)} | {len(b)} | {compress(a | b, 3)} | {'Covered' if a | b else '**Not covered**'} |")
        if not a | b:
            unc.append(("NFR-ENH", n, d["title"], "Add a TC-ENH-K or VER-ENH-K item in Part 6.10 that cites the NFR", "EP-21"))
    S["h3"] = "\n".join(L); L.clear()
    W("| LT-ENH | Scenario | Requirements verified | Status |")
    W("|---|---|---|---|")
    for l, d in lt.items():
        r = X["lt_req"][l]
        W(f"| {l} | {d['title'][:90]} | {_short(r, 6)} | {'Traced' if r else '**Untraced**'} |")
        if not r:
            unc.append(("LT-ENH", l, d["title"][:80], "Cite the NFR/OKPI the load test verifies", "SRE"))
    S["h4"] = "\n".join(L); L.clear()
    W("| ID | Name | # tests (direct) | # tests (via FR-ENH) | FR-ENH | Tests (sample runs) | Status |")
    W("|---|---|---|---|---|---|---|")
    for a, d in agau.items():
        t, v, frs = X["agau_tc"][a]
        W(f"| {a} | {d['title'][:70]} | {len(t)} | {len(v)} | {_short(frs, 3)} | {compress(t | v, 3)} | {'Covered' if t | v else '**Not covered**'} |")
        if not t | v:
            unc.append(("AG/AU", a, d["title"][:80], "Add a TC-ENH-K test case in Part 6.10 that cites the agent or automation", "Batch 7.4 owner"))
    S["h5"] = "\n".join(L); L.clear()
    for t in tce:
        if not tce_req[t]:
            unc.append(("TC-ENH", t, E.defs["TC"][t]["title"][:80], "Add the requirement or alias the test verifies", "Batch owner"))

    # -------- (i) OKPI
    W("| OKPI | Metric | Mandatory | NFR (Part 4.2) | NFR-ENH | KPI / SLO | # tests (direct) | # TC/VER via NFR | Tests (sample runs) | Status |")
    W("|---|---|---|---|---|---|---|---|---|---|")
    for o in ok:
        i = oi[o]
        allt = i["direct"] | i["via"]
        W(f"| {o} | {i['metric'][:60]} | {'Yes' if o in mand else 'No'} | {_short(i['nfr'], 4)} | {_short(i['nfre'], 3)} | {_short(i['kpi'] + i['slo'], 4)} | {len(i['direct'])} | {len(i['via'])} | {compress(allt, 3)} | {'Covered' if allt else '**Not covered**'} |")
        if not allt:
            unc.append(("OKPI", o, i["metric"][:80], "Add a TC-ENH-K measurement test in Part 6.10 that cites the OKPI", "QA Lead"))
    S["i"] = "\n".join(L); L.clear()

    # -------- (j) aliases
    W("| Level | Family | Items | Covered | Coverage | Mapping status in the source CSV |")
    W("|---|---|---|---|---|---|")
    from collections import Counter
    for k, v in lv.items():
        fams = Counter(re.sub(r"\d+$", "", x) for x in v)
        for fm, n in sorted(fams.items()):
            items = [x for x in v if x.startswith(fm)]
            cc = sum(1 for x in items if src[x]["tests"])
            st = Counter(src[x]["status"] for x in items)
            W(f"| {k} | {fm}### | {n} | {cc} | {_pct(cc, n)} | {', '.join(f'{a} {b}' for a, b in sorted(st.items()))} |")
    S["j1"] = "\n".join(L); L.clear()
    W("| SM-SIT alias | Blueprint FRs | Stories | # TC (alias rule) | Operation test | Status |")
    W("|---|---|---|---|---|---|")
    for a, d in sit.items():
        t = d["rule"] | d["api"] | d["src"]
        W(f"| {a} | {', '.join(d['frs'])} | {_short(d['stories'], 3)} | {len(d['rule'])} | {compress(d['api'], 2)} | {'Covered' if t else '**Not covered**'} |")
        if not t:
            unc.append(("SIT alias", a, ", ".join(d["frs"]), "Add a TC-ENH-K test citing the alias", "QA Lead"))
    S["j2"] = "\n".join(L); L.clear()
    W("| QC layer | QCs | Covered (direct) | Covered (total) | Coverage | Uncovered |")
    W("|---|---|---|---|---|---|")
    layers = OrderedDict()
    for a, d in qc.items():
        layers.setdefault(d["layer"], []).append(a)
    for ly, items in sorted(layers.items()):
        cd = sum(1 for x in items if qc[x]["direct"])
        ct = [x for x in items if qc[x]["direct"] | qc[x]["via"]]
        un = [x for x in items if x not in ct]
        W(f"| {ly} | {len(items)} | {cd} | {len(ct)} | {_pct(len(ct), len(items))} | {', '.join(un) or '—'} |")
        for x in un:
            unc.append(("QC", x, qc[x]["check"][:80], "Add a TC-ENH-K or VER-ENH-K item in Part 6.10 that cites the QC", "QC owner"))
    S["j3"] = "\n".join(L); L.clear()
    W("| QC | Layer | Check (condensed) | Priority | Gate | Verified through | # tests/VER | Sample | Status |")
    W("|---|---|---|---|---|---|---|---|---|")
    for a, d in qc.items():
        t = d["direct"] | d["via"]
        thr = ("cited by " + _short({x for x in d["direct"]}, 2)) if d["direct"] else ("refs " + _short(d["via_refs"], 3))
        W(f"| {a} | {d['layer']} | {d['check'][:70]} | {d['priority']} | {d['gate'][:40]} | {thr if t else '—'} | {len(t)} | {compress(t, 2)} | {'Covered' if t else '**Not covered**'} |")
    S["j4"] = "\n".join(L); L.clear()
    for a, d in src.items():
        if not d["tests"]:
            unc.append(("Source test", a, d["title"][:80], "Map to a defined blueprint test or add a TC-ENH-K", "QA Lead"))
    for a, d in api.items():
        if not d["tests"]:
            unc.append(("Source API", a, f"{d['method']} {d['path']}", "Add the operation test (Part 3.5) or a TC-ENH-K", "Backend lead"))
    undef = sorted({u for d in src.values() for u in d["undefined"]})
    X["undef_src_refs"] = undef

    W("| # | Type | Item | Detail | Remediation | Owner |")
    W("|---|---|---|---|---|---|")
    for i, u in enumerate(unc, 1):
        W(f"| UE-{i:02d} | {u[0]} | {u[1]} | {u[2]} | {u[3]} | {u[4]} |")
    if not unc:
        W("| — | — | None | Every source-pack item at every level (h), (i), (j) has at least one designed test case or verification item | — | — |")
    S["k"] = "\n".join(L); L.clear()
    X["uncovered"] = unc
    X["ac_cov"] = ac_cov
    X["tce_req"] = tce_req
    return S


def csv_rows_enh(D, X, compress):
    E = X["E"]
    out = []

    def row(typ, rid, title, epic, wave, lfr, lus, alias, t, ver=()):
        tt = sorted(x for x in t if not x.startswith("VER"))
        vv = sorted(set(x for x in t if x.startswith("VER")) | set(ver))
        basis = "Test case + VER" if tt and vv else "Test case" if tt else "Verification item" if vv else "None"
        out.append([typ, rid, title, epic, wave, lfr, lus, alias, len(tt), compress(tt), "Covered" if tt or vv else "Not covered",
                    len(vv), " ".join(vv), basis])
    for f, d in X["fr"].items():
        m = X["fr_meta"][f]
        row("FR-ENH", f, d["title"][:120], m["epic"], m["wave"], "", " ".join(sorted(X["fr_us"][f])), "", X["fr_tc"][f])
    for s, d in E.defs["US"].items():
        row("US-ENH", s, d["title"][:120], "EP-" + s[3:5], "", " ".join(sorted(X["us_fr"][s])), "", "", X["us_tc"][s])
        for a in E.story_acs.get(s, []):
            row("AC-ENH", a, "", "EP-" + s[3:5], "", "", s, "", X["ac_cov"][a])
    for n, d in X["nfr_e"].items():
        a, b = X["nfr_e_tc"][n]
        row("NFR-ENH", n, d["title"], "", "", "", "", "", a | b)
    for l, d in E.defs["LT"].items():
        out.append(["LT-ENH", l, d["title"][:120], "", "", "", "", " ".join(sorted(X["lt_req"][l])), 0, "",
                    "Traced" if X["lt_req"][l] else "Untraced", 0, "", "Load test"])
    for o, i in X["ok_info"].items():
        row("OKPI", o, i["metric"][:120], "", "", "", "", " ".join(i["nfr"] + i["nfre"] + i["kpi"]), i["direct"] | i["via"])
    for a, d in X["agau"].items():
        t, v, frs = X["agau_tc"][a]
        row("AG" if a.startswith("AG") else "AU", a, d["title"][:120], "", "", " ".join(sorted(frs)), "", "", t | v)
    for a, d in X["src"].items():
        row("SM-" + ("UT" if d["level"] == "Unit" else d["level"]), a, d["title"], "", "", d["req"], "", "", d["tests"])
    for a, d in X["sit"].items():
        row("SIT-ALIAS", a, "", "", "", " ".join(d["frs"]), " ".join(d["stories"]), "", d["rule"] | d["api"] | d["src"])
    for a, d in X["api"].items():
        row("SRC-API", a, f"{d['method']} {d['path']}", "", "", "", "", d["bp"], d["tests"])
    for a, d in X["qc"].items():
        row("QC", a, d["check"][:120], "", "", " ".join(d["via_refs"]), "", d["layer"], d["direct"] | d["via"])
    for t, d in E.defs["TC"].items():
        if t.startswith("TC-ENH-K-"):
            out.append(["TC-ENH-K", t, d["title"][:120], "", "", " ".join(sorted(X["tce_req"][t])), "", "", 1, t, "Closure test", 0, "", "Test case"])
    for v, d in E.defs["VER"].items():
        out.append(["VER-ENH-K", v, d["title"][:120], "", "", " ".join(sorted(E.own_ids(v))), "", "", 0, "", "Closure VER", 1, v, "Verification item"])
    return out
