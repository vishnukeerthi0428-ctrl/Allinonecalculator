"""Generate Part-06-5_Test_Cases_EP01-EP07.md from Part 5.1 stories plus hand-authored technique groups."""
import re
import sys
from collections import OrderedDict, defaultdict, Counter
from parse51 import parse, ids_in, BP
import hand65 as H

stories, order = parse()

# ---------------------------------------------------------------- FR ownership from Part 5.1 §5.9.2.1
cov = open(BP + "Part-05-1c_Epics_Stories_Foundation.md", encoding="utf-8").read()
sec = cov.split("#### 5.9.2.1 FR → stories")[1].split("**Partially covered")[0]
FR_OWN = OrderedDict()   # FR -> stories
STORY_FR = defaultdict(list)
for line in sec.split("\n"):
    m = re.match(r"\| (FR-(?:W\d{2}|A\d{3}|OP\d{3})) \| .*? \| (.*?) \| (.*?) \| (.*?) \| Covered", line)
    if m:
        uss = re.findall(r"US-\d{4}", m.group(4))
        FR_OWN[m.group(1)] = uss
        for u in uss:
            STORY_FR[u].append(m.group(1))

# ---------------------------------------------------------------- story metadata: risk area and default level
RA_PRI = {"RA-01": "P0", "RA-02": "P0", "RA-03": "P0", "RA-04": "P0", "RA-05": "P0", "RA-06": "P0", "RA-11": "P0",
          "RA-12": "P0", "RA-13": "P0", "RA-14": "P0", "RA-16": "P0", "RA-17": "P0", "RA-19": "P0", "RA-21": "P1",
          "RA-22": "P1", "RA-23": "P1", "RA-28": "P1", "RA-29": "P2", "RA-30": "P2"}
META = {
    "US-0101": ("RA-02", "SYS"), "US-0102": ("RA-16", "CT"), "US-0103": ("RA-16", "CT"), "US-0104": ("RA-02", "SYS"),
    "US-0105": ("RA-02", "SYS"), "US-0106": ("RA-02", "SYS"), "US-0107": ("RA-01", "IT"), "US-0108": ("RA-01", "SYS"),
    "US-0109": ("RA-01", "SYS"), "US-0110": ("RA-04", "IT"), "US-0111": ("RA-01", "IT"), "US-0112": ("RA-02", "SYS"),
    "US-0113": ("RA-01", "IT"), "US-0114": ("RA-01", "SYS"), "US-0115": ("RA-16", "IT"), "US-0116": ("RA-30", "E2E"),
    "US-0117": ("RA-19", "IT"),
    "US-0201": ("RA-28", "SYS"), "US-0202": ("RA-05", "SYS"), "US-0203": ("RA-13", "IT"), "US-0204": ("RA-01", "SYS"),
    "US-0205": ("RA-14", "SYS"), "US-0206": ("RA-29", "E2E"), "US-0207": ("RA-29", "SYS"), "US-0208": ("RA-06", "IT"),
    "US-0301": ("RA-03", "IT"), "US-0302": ("RA-03", "SYS"), "US-0303": ("RA-03", "UT"), "US-0304": ("RA-03", "UT"),
    "US-0305": ("RA-03", "E2E"), "US-0306": ("RA-17", "SYS"), "US-0307": ("RA-17", "SYS"), "US-0308": ("RA-17", "IT"),
    "US-0309": ("RA-03", "SYS"), "US-0310": ("RA-30", "E2E"), "US-0311": ("RA-03", "SYS"),
    "US-0401": ("RA-13", "IT"), "US-0402": ("RA-13", "CT"), "US-0403": ("RA-13", "UT"), "US-0404": ("RA-13", "IT"),
    "US-0405": ("RA-13", "E2E"), "US-0406": ("RA-13", "SYS"), "US-0407": ("RA-13", "SYS"), "US-0408": ("RA-13", "IT"),
    "US-0501": ("RA-22", "SYS"), "US-0502": ("RA-22", "SYS"), "US-0503": ("RA-22", "IT"), "US-0504": ("RA-22", "SYS"),
    "US-0505": ("RA-22", "SYS"), "US-0506": ("RA-22", "SYS"), "US-0507": ("RA-22", "SYS"), "US-0508": ("RA-22", "SYS"),
    "US-0509": ("RA-22", "SYS"), "US-0510": ("RA-22", "SYS"), "US-0511": ("RA-22", "IT"), "US-0512": ("RA-22", "SYS"),
    "US-0601": ("RA-21", "UT"), "US-0602": ("RA-21", "SYS"), "US-0603": ("RA-22", "SYS"), "US-0604": ("RA-22", "SYS"),
    "US-0605": ("RA-21", "SYS"), "US-0606": ("RA-21", "SYS"), "US-0607": ("RA-21", "SYS"), "US-0608": ("RA-30", "E2E"),
    "US-0701": ("RA-23", "SYS"), "US-0702": ("RA-23", "SYS"), "US-0703": ("RA-23", "SYS"), "US-0704": ("RA-23", "SYS"),
    "US-0705": ("RA-23", "SYS"), "US-0706": ("RA-11", "SYS"), "US-0707": ("RA-23", "SYS"), "US-0708": ("RA-23", "IT"),
    "US-0709": ("RA-23", "SYS"), "US-0710": ("RA-23", "SYS"),
}

P0_TAG = re.compile(r"^(T5|BRL-TEN-\d\d|BRL-ELG-\d\d|BRL-PRV-\d\d|BRL-AI-0[678]|BRL-APR-0[12]|BRL-SRC-0[1347]|"
                    r"NFR-014|NFR-004|NFR-005|NFR-006|NFR-021|DEC-029|DEC-030|DEC-058|DEC-002|DEC-007|BRL-AUT-0[5-8]|sec|I4|BRL-MKT-0[12]|DEC-060)$")
PATHS = ["happy", "alt", "neg", "val", "perm", "edge", "a11y"]


def path_of(sc):
    for p in ["perm", "neg", "val", "happy", "alt", "edge", "a11y"]:
        if p in sc["tags"]:
            return p
    t = sc["title"].lower()
    if t.startswith("ci gate") or "axe" in t:
        return "a11y"
    if t.startswith("security") or t.startswith("observability"):
        return "edge"
    return "edge"


def text_of(sc):
    return " ".join(sc["given"] + sc["when"] + sc["then"])


def priority(us, sc, p):
    st = stories[us]
    ra, _ = META[us]
    rap = RA_PRI[ra]
    tags = sc["tags"]
    txt = text_of(sc).lower()
    xt = "T5" in tags or "another tenant" in txt or "external-a" in txt and p == "perm"
    p0t = any(P0_TAG.match(t) for t in tags) or xt
    if st["priority"] in ("Should", "Could"):
        return "P0" if xt else ("P3" if p in ("a11y",) or "C2" in tags else "P2")
    if "a11y" in tags or st["type"].startswith("Accessibility"):
        return "P1"
    if p0t and p in ("neg", "perm", "edge", "val"):
        return "P0"
    if rap == "P0":
        if p in ("neg", "perm"):
            return "P0"
        if p == "happy" and any(k in st["type"] for k in ("Enabler", "Security", "Spike", "Compliance")):
            return "P0"
        return "P1"
    if rap == "P1":
        return "P2" if p == "alt" or "obs" in tags else "P1"
    return "P2"


def ttype(us, sc, p):
    st = stories[us]
    tags = sc["tags"]
    txt = (sc["title"] + " " + text_of(sc)).lower()
    if "a11y" in tags or st["type"].startswith("Accessibility") or "screen reader" in txt or "wcag" in txt:
        return "T08"
    if "T5" in tags or "BRL-TEN-03" in tags or "BRL-TEN-04" in tags or "another tenant" in txt or "cross tenants" in txt:
        return "T15"
    if "T3" in tags and p == "perm":
        return "T15"
    if "sec" in tags:
        return "T07"
    if "obs" in tags or st["type"].startswith("Observability"):
        return "T21"
    if "I4" in tags or "uncertain" in txt:
        return "T18"
    if "D5" in tags or "duplicate" in txt or "twice" in txt or "idempot" in txt:
        return "T16"
    if "E-6" in tags or "simulat" in txt:
        return "T17"
    if any(t.startswith(("BRL-ELG", "BRL-PRV", "DEC-029", "DEC-030", "BRL-SRC-01", "BRL-SRC-04")) for t in tags) or \
            us in ("US-0301", "US-0304", "US-0307", "US-0308", "US-0305"):
        return "T19"
    if us in ("US-0404",) or "BRL-AI-08" in tags or "NFR-014" in tags or "budget" in txt and us.startswith("US-04"):
        return "T20"
    if us in ("US-0402", "US-0405", "US-0406", "US-0407", "US-0403"):
        return "T14"
    if us in ("US-0208", "US-0708"):
        return "T11"
    if "D6" in tags and ("p95" in txt or "latency" in txt or "≤ 500 ms" in txt):
        return "T03"
    if "Lb" in tags or "Lc" in tags:
        return "T13"
    return "T01"


def technique(us, sc, p):
    tags = sc["tags"]
    title = sc["title"].lower()
    txt = text_of(sc).lower()
    rule = [t for t in tags if t.startswith(("BRL-", "DEC-", "ABAC-", "BR-S"))]
    if sc["outline"] or "D3" in tags or "boundary" in title:
        return "BVA"
    if "transition" in title or ("S5" in tags and ("expir" in txt or "stale" in txt)) or "S4" in tags or "S6" in tags:
        return "ST"
    if p == "val":
        return "EP"
    if p == "neg":
        return "DT" if rule else "EG"
    if p == "perm":
        return "EP"
    if p in ("happy", "alt"):
        return "UC"
    if p == "a11y":
        return "UC"
    if any(t in tags for t in ("D5", "I2", "I3", "I4", "D6", "D4")):
        return "EG"
    return "EG"


def level(us, sc, p, tt):
    _, lv = META[us]
    tags = sc["tags"]
    txt = (sc["title"] + " " + text_of(sc)).lower()
    if "C2" in tags or "360 px" in txt or tt == "T08" or "keyboard" in txt:
        return "E2E"
    if tt == "T03":
        return "SYS"
    if "ci " in txt or txt.startswith("ci") or "pull request" in txt or "ci fails" in txt or "ci gate" in txt:
        return "CT"
    return lv


def automation(us, sc):
    txt = (sc["title"] + " " + text_of(sc)).lower()
    if "screen reader" in txt or "nvda" in txt or "voiceover" in txt:
        return "N (assistive-technology pass)"
    if "product owner decides" in txt:
        return "N (PO decision step)"
    return "Y"


# ---------------------------------------------------------------- DM row selection (Part 5.1a §5.6.4/§5.6.5)
DM = {}
for line in open(BP + "Part-05-1a_Epics_Stories_Foundation.md", encoding="utf-8"):
    m = re.match(r"\| (DM-\d{3}) \| (A\d) \| (S\d) \| (D\d) \| (C\d) \| (T\d)(?: \([^)]*\))? \| (I\d) \| (L[a-d]) \|", line)
    if m:
        DM[m.group(1)] = m.groups()[1:]


def dims(us, sc, p):
    tags = sc["tags"]
    txt = (sc["title"] + " " + text_of(sc)).lower()
    a = next((t for t in tags if re.fullmatch(r"A\d", t)), None)
    if not a:
        if p == "perm":
            a = "A3" if any(k in txt for k in ("own ", "author", "requester", "maker", "himself", "proposer")) else "A5"
        elif any(k in txt for k in ("worker", "agent", "job", "celery", "service")):
            a = "A8"
        elif "approve" in txt:
            a = "A2"
        elif "visitor" in txt or "anonymous" in txt:
            a = "A7"
        else:
            a = "A1"
    s_ = next((t for t in tags if re.fullmatch(r"S\d", t)), None) or (
        "S5" if ("expir" in txt or "stale" in txt) else "S7" if "uncertain" in txt else "S2" if "pending" in txt
        else "S1" if ("draft" in txt or "creates" in txt) else "S3")
    d = next((t for t in tags if re.fullmatch(r"D\d", t)), None) or (
        "D3" if "boundary" in txt else "D2" if p == "val" else "D5" if ("duplicate" in txt or "twice" in txt)
        else "D6" if any(k in txt for k in ("000 ", "large", "volume")) else "D4" if "unknown" in txt else "D1")
    c = next((t for t in tags if re.fullmatch(r"C\d", t)), None) or (
        "C2" if "360 px" in txt else "C3" if any(k in txt for k in ("api", "get /", "post /", "worker", "job", "ci ")) else "C1")
    tn = next((t for t in tags if re.fullmatch(r"T\d", t)), None) or ("T5" if "external-a" in txt and p == "perm" else "T1")
    i = next((t for t in tags if re.fullmatch(r"I\d", t)), None) or ("I4" if "uncertain" in txt else "I1")
    l = next((t for t in tags if re.fullmatch(r"L[a-d]", t)), None) or ("Ld" if c == "C3" else "La")
    return a, s_, d, c, tn, i, l


RR1 = [(a, c) for a in ["A1", "A2", "A3", "A4", "A5", "A6"] for c in ["C1", "C2", "C3"]] + [("A8", "C3")]


def dm_row(us, sc, p):
    a, s_, d, c, tn, i, l = dims(us, sc, p)
    txt = (sc["title"] + " " + text_of(sc)).lower()
    if tn == "T5":
        aa = a if a in ("A1", "A2", "A3", "A4", "A5", "A6", "A8") else "A5"
        cc = "C3" if aa == "A8" else c
        k = RR1.index((aa, cc)) if (aa, cc) in RR1 else RR1.index(("A5", "C3"))
        return f"DM-R{k + 1:02d}"
    if tn == "T3" and p in ("perm", "neg"):
        aa = a if a in ("A1", "A2") else "A1"
        return f"DM-R{20 + ['A1', 'A2'].index(aa) * 3 + ['C1', 'C2', 'C3'].index(c):02d}"
    if i == "I4" and d == "D5":
        return "DM-R26"
    if "health" in txt or "clinical" in txt:
        if a == "A7":
            return "DM-R32" if c != "C2" else "DM-R33"
    if ("minor" in txt or "under 18" in txt or "guardian" in txt) and a == "A7":
        return "DM-R30" if c != "C2" else "DM-R31"
    if a == "A3" and c == "C2":
        return "DM-R34"
    if l == "Lc" and d == "D3":
        return "DM-R35"
    if tn == "T6":
        return "DM-R38" if c == "C3" else "DM-R37"
    if d == "D6" and c == "C2":
        return "DM-R39"
    best, bs = None, -1
    want = (a, s_, d, c, tn, i, l)
    w = (2, 1, 1, 1, 2, 1, 1)
    for k, v in DM.items():
        sc_ = sum(w[j] for j in range(7) if v[j] == want[j])
        if sc_ > bs:
            best, bs = k, sc_
    return best


# ---------------------------------------------------------------- text helpers
def esc(s):
    s = s.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")
    return s


def num(lines, start=1):
    return "; ".join(f"{k + start}. {esc(x[0].upper() + x[1:])}" for k, x in enumerate(lines) if x)


NOSIDE = "No side effect: state, outbox, simulator log and ledger unchanged; one audit event with outcome=denied (SPC-2)"


def convert(us, sc):
    st = stories[us]
    p = path_of(sc)
    pr = priority(us, sc, p)
    tt = ttype(us, sc, p)
    tech = technique(us, sc, p)
    lv = level(us, sc, p, tt)
    title = sc["title"].split(" – ", 1)[-1]
    title = title[0].upper() + title[1:]
    tags = sc["tags"]
    rules = [t for t in tags if re.match(r"(BRL-|DEC-|NFR-|ABAC-|BR-S|CA-|AP-|RECOMMENDATION-|FR-)", t)]
    frs = STORY_FR.get(us) or [x for x in st["trace_ids"] if re.match(r"FR-(W\d|A\d|OP)", x)]
    xfr = [x for x in st["trace_ids"] if re.match(r"FR-(ENG|STD|ADP|NEG|UIS|DM|CSM|FLT|PUB)", x)]
    links = [sc["ac"]] + frs[:3] + [x for x in xfr[:2] if x not in frs] + [r for r in rules if r not in frs]
    if pr == "P0" and not any(x.startswith(("BRL-", "NFR-")) for x in links):
        extra = [x for x in st["trace_ids"] if x.startswith(("BRL-", "NFR-"))][:1]
        links += extra
    dm = dm_row(us, sc, p)
    pre = []
    if st["background"]:
        pre.append("Background: " + "; ".join(st["background"]))
    if sc["given"]:
        g = "; ".join(sc["given"])
        pre.append(g[0].upper() + g[1:])
    if not pre:
        pre.append("Role and scope as named in the steps; two-tenant fixture loaded")
    pre_s = esc(". ".join(pre)) + f" · `gse_syn 1.4.0`; {dm}"
    if sc["outline"] and sc["examples"]:
        hdr = sc["examples"][0]
        rows = sc["examples"][1:]
        steps = "For each Examples row: " + "; ".join(", ".join(f"{h}={v}" for h, v in zip(hdr, r)) for r in rows)
        steps = esc(steps)
    elif sc["when"]:
        steps = num(sc["when"])
    else:
        steps = "1. Trigger the evaluation under test (API call, job or page load) with the preconditions above"
    exp = num(sc["then"]) if sc["then"] else ""
    if p in ("neg", "perm") and "no side" not in exp.lower() and level(us, sc, p, tt) != "CT":
        exp += ". " + NOSIDE if exp else NOSIDE
    auto = automation(us, sc)
    return dict(title=esc(title), links="; ".join(dict.fromkeys(links)), pre=pre_s, steps=steps, exp=exp, P=pr,
                type=tt, tech=tech, auto=auto, lvl=lv, acs=[sc["ac"]], dm=dm, src="conv", us=us)


# ---------------------------------------------------------------- build epics
AC_RX = re.compile(r"AC-\d{4}-\d{2}")
EPICS = [f"EP-0{i}" for i in range(1, 8)]
EP_TITLES = {"EP-01": "Platform foundation, identity reuse and tenancy", "EP-02": "Product truth and knowledge",
             "EP-03": "Consent, privacy, eligibility and compliance", "EP-04": "AI gateway, cost control and AI quality",
             "EP-05": "Market intelligence and discovery", "EP-06": "Opportunity scoring, contacts and research review",
             "EP-07": "CRM, lead capture and Customer 360"}

all_tcs = []          # final list in order
ts_rows = defaultdict(list)
group_blocks = defaultdict(list)


def letters(n):
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


for ep in EPICS:
    epn = ep[3:]
    hand = H.EPIC.get(ep, {})
    hgroups = hand.get("groups", [])
    # TS list: one per story, then extra batteries
    ts_list = []
    for us in order:
        if stories[us]["epic"] == ep:
            ts_list.append(us)
    for k in hand.get("extra_ts", []):
        ts_list.append(k[0])
    ts_id = {key: f"TS-{epn}-{i + 1:02d}" for i, key in enumerate(ts_list)}
    hand_acs = set()
    for g in hgroups:
        for r in g["rows"]:
            hand_acs.update(AC_RX.findall(r[1]))
    seq = 0
    gi = 0
    blocks = []
    ts_tc = defaultdict(list)
    for key in ts_list:
        # hand groups for this key
        for g in [g for g in hgroups if g["ts"] == key]:
            letter = letters(gi)
            gi += 1
            rows = []
            for r in g["rows"]:
                seq += 1
                tid = f"TC-{epn}-{seq:03d}"
                tc = dict(id=tid, title=r[0], links=r[1], pre=r[2], steps=r[3], exp=r[4], P=r[5], type=r[6],
                          tech=r[7], auto=r[8], lvl=r[9], acs=AC_RX.findall(r[1]), src="hand", ts=ts_id[key], ep=ep,
                          us=key if key.startswith("US-") else None)
                dmm = re.findall(r"DM-R?\d{2,3}", r[1] + " " + r[2])
                tc["dm"] = dmm[0] if dmm else None
                rows.append(tc)
                all_tcs.append(tc)
                ts_tc[key].append(tid)
            blocks.append(dict(kind="hand", letter=letter, g=g, rows=rows, ts=ts_id[key], key=key))
        # conversion group for remaining ACs
        if key.startswith("US-"):
            rem = [sc for sc in stories[key]["scenarios"] if sc["ac"] not in hand_acs]
            if rem:
                letter = letters(gi)
                gi += 1
                rows = []
                for sc in rem:
                    seq += 1
                    tc = convert(key, sc)
                    tc.update(id=f"TC-{epn}-{seq:03d}", ts=ts_id[key], ep=ep)
                    rows.append(tc)
                    all_tcs.append(tc)
                    ts_tc[key].append(tc["id"])
                techs = sorted(set(t["tech"] for t in rows), key=lambda x: ["UC", "EP", "BVA", "DT", "ST", "PW", "EG", "PBT", "EXP"].index(x))
                blocks.append(dict(kind="conv", letter=letter, rows=rows, ts=ts_id[key], key=key, techs=techs))
    group_blocks[ep] = blocks
    # TS table rows
    for key in ts_list:
        if key.startswith("US-"):
            st = stories[key]
            ra, _ = META[key]
            frs = STORY_FR.get(key) or [x for x in st["trace_ids"] if re.match(r"FR-(W\d|A\d|OP)", x)][:4]
            acs_k = {sc["ac"] for sc in st["scenarios"]}
            extra = [x["id"] for x in all_tcs if x["ep"] == ep and set(x["acs"]) & acs_k and x["id"] not in ts_tc[key]]
            ts_tc[key] = sorted(set(ts_tc[key] + extra), key=lambda x: int(x[6:]))
            pr = "P0" if any(all_tcs_t["P"] == "P0" for all_tcs_t in all_tcs if all_tcs_t["id"] in ts_tc[key]) else RA_PRI[ra]
            ts_rows[ep].append((ts_id[key], H.TS_TITLE.get(key, st["long_title"] or st["title"]), key + ("; " + ", ".join(frs) if frs else ""),
                                f"{ra} · {pr}", ts_tc[key]))
        else:
            k = next(x for x in hand["extra_ts"] if x[0] == key)
            pr = "P0" if any(t["P"] == "P0" for t in all_tcs if t["id"] in ts_tc[key]) else "P1"
            ts_rows[ep].append((ts_id[key], k[1], k[2], f"{k[3]} · {pr}", ts_tc[key]))


def rng(ids):
    """Compress a list of TC IDs into ranges TC-01-001…005."""
    if not ids:
        return "—"
    out = []
    pref = lambda x: x.rsplit("-", 1)
    run = [ids[0]]
    for x in ids[1:]:
        p0, n0 = pref(run[-1])
        p1, n1 = pref(x)
        if p0 == p1 and int(n1) == int(n0) + 1:
            run.append(x)
        else:
            out.append(run)
            run = [x]
    out.append(run)
    return ", ".join(r[0] if len(r) == 1 else f"{r[0]}…{r[-1].rsplit('-', 1)[1]}" for r in out)


# ---------------------------------------------------------------- render
TECH_NAME = {"UC": "use case", "EP": "equivalence partitioning", "BVA": "boundary value analysis", "DT": "decision table",
             "ST": "state transition", "PW": "pairwise", "EG": "error guessing", "PBT": "property-based", "EXP": "exploratory"}
out = []
W = out.append
W(H.FRONT)
sec_no = {ep: i + 2 for i, ep in enumerate(EPICS)}
for ep in EPICS:
    n = sec_no[ep]
    epn = ep[3:]
    W(f"\n## 6.5.{n} {ep} {EP_TITLES[ep]}\n")
    W(H.EPIC[ep]["intro"] + "\n")
    W(f"### 6.5.{n}.1 Scenarios\n")
    W("| TS ID | Title | Linked US / FR | Risk area · Priority | TCs |")
    W("|---|---|---|---|---|")
    for r in ts_rows[ep]:
        W(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {rng(r[4])} |")
    k = 2
    for b in group_blocks[ep]:
        ids = [t["id"] for t in b["rows"]]
        if b["kind"] == "hand":
            g = b["g"]
            W(f"\n### 6.5.{n}.{k} Group TC-{epn}-{b['letter']}: {g['heading']} (technique: {g['tech']}) · {b['ts']}\n")
            if g.get("intro"):
                W(g["intro"].strip() + "\n")
        else:
            st = stories[b["key"]]
            tl = ", ".join(b["techs"])
            W(f"\n### 6.5.{n}.{k} Group TC-{epn}-{b['letter']}: Specification by example – {b['key']} {st['title']}, remaining AC (techniques: {tl}) · {b['ts']}\n")
            W(f"Each row realizes one Part 5.1 Gherkin scenario not already exercised above; the technique column states how its condition was classified (§6.5.1.3).\n")
        k += 1
        W("| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |")
        W("|---|---|---|---|---|---|---|---|---|---|---|")
        for t in b["rows"]:
            W(f"| {t['id']} | {t['title']} | {t['links']} | {t['pre']} | {t['steps']} | {t['exp']} | {t['P']} | {t['type']} | {t['tech']} | {t['auto']} | {t['lvl']} |")

# ---------------------------------------------------------------- coverage section
ac_map = defaultdict(list)
for t in all_tcs:
    for a in t["acs"]:
        ac_map[a].append(t["id"])
all_acs = [sc["ac"] for us in order for sc in stories[us]["scenarios"]]
missing_ac = [a for a in all_acs if not ac_map.get(a)]
story_tc = defaultdict(list)
for t in all_tcs:
    for a in t["acs"]:
        story_tc["US-" + a[3:7]].append(t["id"])
    if t.get("us"):
        story_tc[t["us"]].append(t["id"])
for k in story_tc:
    story_tc[k] = sorted(set(story_tc[k]), key=lambda x: (x[3:5], int(x[6:])))

fr_tc = OrderedDict()
for fr, uss in FR_OWN.items():
    ids = set()
    for t in all_tcs:
        if fr in re.findall(r"FR-(?:W\d{2}|A\d{3}|OP\d{3})", t["links"]):
            ids.add(t["id"])
        elif any(("US-" + a[3:7]) in uss for a in t["acs"]) and t["src"] == "conv" and fr in STORY_FR.get(t["us"], []):
            ids.add(t["id"])
    fr_tc[fr] = sorted(ids, key=lambda x: (x[3:5], int(x[6:])))

brl_all = sorted(set(re.findall(r"BRL-[A-Z]{2,4}-\d{2}", open(BP + "Part-05-1c_Epics_Stories_Foundation.md").read().split("#### 5.9.2.4")[1].split("#### 5.9.2.5")[0])))
# expand ranges in 5.9.2.4 text (e.g. "01–03")
brl_sec = open(BP + "Part-05-1c_Epics_Stories_Foundation.md").read().split("#### 5.9.2.4")[1].split("#### 5.9.2.5")[0]
brl_set = set()
for line in brl_sec.split("\n"):
    m = re.match(r"\| (BRL-[A-Z]+) \| (.*?) \| (.*?) \|$", line)
    if m:
        fam = m.group(1)
        for a, b in re.findall(r"(?<![\d(])(\d{2})(?:[–…](\d{2}))? \(", m.group(2)):
            for x in range(int(a), int(b or a) + 1):
                brl_set.add(f"{fam}-{x:02d}")
    m2 = re.match(r"\| Other \| (.*?) \|", line)
    if m2:
        brl_set.update(re.findall(r"BRL-[A-Z]+-\d{2}", m2.group(1)))
brl_tc = OrderedDict()
for b in sorted(brl_set):
    brl_tc[b] = sorted({t["id"] for t in all_tcs if b in t["links"] or b in t["pre"] or b in t["exp"]}, key=lambda x: (x[3:5], int(x[6:])))

n = 9
W(f"\n## 6.5.{n} Coverage for EP-01 to EP-07\n")
W(H.COVERAGE_INTRO)
W(f"### 6.5.{n}.1 Story → test cases (74 stories)\n")
W("| Story | Title | ACs | ACs covered | TCs | TC count |")
W("|---|---|---|---|---|---|")
tot_ac = tot_cov = 0
for us in order:
    acs = [sc["ac"] for sc in stories[us]["scenarios"]]
    c = sum(1 for a in acs if ac_map.get(a))
    tot_ac += len(acs)
    tot_cov += c
    W(f"| {us} | {stories[us]['title']} | {len(acs)} | {c} | {rng(story_tc[us])} | {len(story_tc[us])} |")
W(f"| **Total** | 74 stories | **{tot_ac}** | **{tot_cov} ({100 * tot_cov / tot_ac:.1f}%)** | | **{len(all_tcs)}** |")
W(f"\n### 6.5.{n}.2 FR → test cases (45 FRs owned by EP-01…EP-07, incl. FR-OP001)\n")
W("| FR | Stories (Part 5.1 §5.9.2.1) | TCs | Count | Status |")
W("|---|---|---|---|---|")
for fr, ids in fr_tc.items():
    W(f"| {fr} | {', '.join(FR_OWN[fr])} | {rng(ids)} | {len(ids)} | {'Covered' if ids else '**Not covered**'} |")
nfr_cov = sum(1 for v in fr_tc.values() if v)
W(f"| **Total** | | | | **{nfr_cov} of {len(fr_tc)} covered ({100 * nfr_cov / len(fr_tc):.0f}%)** |")
W(H.XFR_TABLE)
W(f"\n### 6.5.{n}.3 AC → test cases (505 Part 5.1 scenarios)\n")
W("Format: AC suffix → TC IDs. Every AC has at least one TC; ACs realized by a hand-designed technique group show that group's TC(s), the rest show the specification-by-example TC.\n")
W("| Story | AC → TC |")
W("|---|---|")
for us in order:
    parts = []
    for sc in stories[us]["scenarios"]:
        parts.append(f"{sc['ac'][8:]} → {rng(ac_map.get(sc['ac'], []))}")
    W(f"| {us} | {'; '.join(parts)} |")
W(f"\nUncovered ACs: **{len(missing_ac)}**{(' (' + ', '.join(missing_ac) + ')') if missing_ac else ''}.\n")
W(f"### 6.5.{n}.4 Business rules (BRL) enforced in batch 5.1 → test cases\n")
W("Rule set = Part 5.1 §5.9.2.4 (rules enforced by EP-01…EP-07 stories). A TC counts when the rule ID appears in its links, data or expected result.\n")
W("| BRL | TCs | Count | DT/BVA present |")
W("|---|---|---|---|")
tc_by_id = {t["id"]: t for t in all_tcs}
brl_ok = 0
for b, ids in brl_tc.items():
    dtb = any(tc_by_id[i]["tech"].split(",")[0].strip() in ("DT", "BVA") or "DT" in tc_by_id[i]["tech"] or "BVA" in tc_by_id[i]["tech"] for i in ids)
    brl_ok += 1 if ids else 0
    W(f"| {b} | {rng(ids)} | {len(ids)} | {'Yes' if dtb else 'No (other technique)'} |")
W(f"| **Total** | | **{brl_ok} of {len(brl_tc)} rules covered** | |")

# DM coverage
dm_used = Counter(t["dm"] for t in all_tcs if t.get("dm"))
pw_used = sorted(k for k in dm_used if re.fullmatch(r"DM-\d{3}", k))
rr_used = sorted(k for k in dm_used if k.startswith("DM-R"))
W(f"\n### 6.5.{n}.5 Dimension-matrix rows realized (Part 5.1a §5.6.4–§5.6.5)\n")
W(f"| Set | Rows defined | Rows realized by ≥ 1 TC in this batch | Not realized here |")
W("|---|---|---|---|")
allpw = [f"DM-{i:03d}" for i in range(1, 58)]
allrr = [f"DM-R{i:02d}" for i in range(1, 41)]
W(f"| Pairwise DM-001…057 | 57 | {len(pw_used)} | {', '.join(x for x in allpw if x not in dm_used) or '—'} |")
W(f"| Risk rows DM-R01…R40 | 40 | {len(rr_used)} | {', '.join(x for x in allrr if x not in dm_used) or '—'} |")
W(H.DM_NOTE)

# Totals
W(f"\n### 6.5.{n}.6 Totals\n")
pc = Counter(t["P"] for t in all_tcs)
W("**By epic and priority**\n")
W("| Epic | Scenarios | TCs | P0 | P1 | P2 | P3 | Hand-designed | Spec-by-example |")
W("|---|---|---|---|---|---|---|---|---|")
for ep in EPICS:
    tcs = [t for t in all_tcs if t["ep"] == ep]
    c = Counter(t["P"] for t in tcs)
    W(f"| {ep} | {len(ts_rows[ep])} | {len(tcs)} | {c['P0']} | {c['P1']} | {c['P2']} | {c['P3']} | {sum(1 for t in tcs if t['src'] == 'hand')} | {sum(1 for t in tcs if t['src'] == 'conv')} |")
W(f"| **Total** | **{sum(len(v) for v in ts_rows.values())}** | **{len(all_tcs)}** | **{pc['P0']}** | **{pc['P1']}** | **{pc['P2']}** | **{pc['P3']}** | **{sum(1 for t in all_tcs if t['src'] == 'hand')}** | **{sum(1 for t in all_tcs if t['src'] == 'conv')}** |")
TYPE_NAME = {"T01": "Functional", "T03": "Performance: load", "T07": "Security", "T08": "Accessibility", "T11": "Data migration",
             "T13": "Localization", "T14": "AI evaluation", "T15": "Multi-tenant isolation", "T16": "Idempotency and replay",
             "T17": "Simulation zero-effect", "T18": "Uncertain-outcome reconciliation", "T19": "Compliance", "T20": "Cost control",
             "T21": "Operability and observability", "T12": "DR / failover", "T02": "Regression", "T10": "Compatibility", "T04": "Performance: stress"}
tc_type = Counter(t["type"].split(",")[0].strip() for t in all_tcs)
W("\n**By test type (primary type, Part 6.1 §6.1.3.1)**\n")
W("| Type | Name | TCs |")
W("|---|---|---|")
for k, v in sorted(tc_type.items()):
    W(f"| {k} | {TYPE_NAME.get(k, '')} | {v} |")
tech_c = Counter()
for t in all_tcs:
    for x in re.split(r"[,+ ]+", t["tech"]):
        if x in TECH_NAME:
            tech_c[x] += 1
W("\n**By technique (a TC using two techniques counts under both)**\n")
W("| Technique | Name | TCs |")
W("|---|---|---|")
for k in ["UC", "EP", "BVA", "DT", "ST", "PW", "EG", "PBT", "EXP"]:
    W(f"| {k} | {TECH_NAME[k]} | {tech_c[k]} |")
auto_y = sum(1 for t in all_tcs if t["auto"].startswith("Y"))
p0 = [t for t in all_tcs if t["P"] == "P0"]
p0y = sum(1 for t in p0 if t["auto"].startswith("Y"))
lv_c = Counter(t["lvl"].split(",")[0].strip() for t in all_tcs)
W("\n**By automation candidate and level**\n")
W("| Measure | Value |")
W("|---|---|")
W(f"| Automation candidates (Y) | {auto_y} of {len(all_tcs)} ({100 * auto_y / len(all_tcs):.1f}%) |")
W(f"| P0 automation candidates | {p0y} of {len(p0)} ({100 * p0y / len(p0):.1f}%) |")
W(f"| Manual (N) with reason | {len(all_tcs) - auto_y} |")
for k in ["UT", "IT", "CT", "SYS", "E2E", "UAT"]:
    W(f"| Level {k} | {lv_c.get(k, 0)} |")

W(H.TAIL)
txt = "\n".join(out)
txt = txt.replace("{{TOTAL_TC}}", str(len(all_tcs))).replace("{{P0}}", str(pc["P0"])).replace("{{P1}}", str(pc["P1"])) \
    .replace("{{P2}}", str(pc["P2"])).replace("{{P3}}", str(pc["P3"])).replace("{{TS}}", str(sum(len(v) for v in ts_rows.values()))) \
    .replace("{{HAND}}", str(sum(1 for t in all_tcs if t['src'] == 'hand'))).replace("{{CONV}}", str(sum(1 for t in all_tcs if t['src'] == 'conv'))) \
    .replace("{{AUTO}}", f"{100 * auto_y / len(all_tcs):.1f}%").replace("{{MISSING_AC}}", str(len(missing_ac))) \
    .replace("{{BRL_OK}}", f"{brl_ok} of {len(brl_tc)}").replace("{{FR_OK}}", f"{nfr_cov} of {len(fr_tc)}") \
    .replace("{{LAST7}}", [x["id"] for x in all_tcs if x["ep"]=="EP-07"][-1][-3:]).replace("{{DM_PW}}", str(len(pw_used))).replace("{{DM_RR}}", str(len(rr_used)))
open(BP + "Part-06-5_Test_Cases_EP01-EP07.md", "w", encoding="utf-8").write(txt + "\n")
print("TCs", len(all_tcs), dict(pc), "missing AC", len(missing_ac), "FR", nfr_cov, len(fr_tc), "BRL", brl_ok, len(brl_tc),
      "DM", len(pw_used), len(rr_used), "hand", sum(1 for t in all_tcs if t['src'] == 'hand'))
