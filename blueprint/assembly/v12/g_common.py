"""Group G (R6) shared data: loaders, ID crosswalks and screen master for Part 11.7.
All source content is treated as data. Run with python3 -I."""
import json, os, re, glob, csv

BP = "/home/user/Allinonecalculator/blueprint"
S = "/tmp/claude-0/-home-user-Allinonecalculator/233b6551-af93-57f5-8f0b-015057ecee11/scratchpad"
V12 = S + "/v12"
G = S + "/g"
SRC = V12 + "/src"
PROTO = S + "/rev_zip/Re_ Sales and Marketing Automation Platform"
WB = SRC + "/Others/Others/Sales_Marketing_Automation_147_Screen_Field_csv"
WEBPACK = SRC + "/Sales_Marketing_Automation_34_Neutral_SaaS_Website(1)"


def load():
    fsd = json.load(open(G + "/fsd.json", encoding="utf-8"))
    crawl = json.load(open(G + "/crawl.json", encoding="utf-8"))
    consts = json.load(open(G + "/admin_consts.json", encoding="utf-8"))
    return fsd, crawl, consts


def corpus():
    out = {}
    for f in sorted(glob.glob(BP + "/Part-*.md")):
        if "Part-11" in f:
            continue
        out[os.path.basename(f)] = open(f, encoding="utf-8").read()
    return out


def cards_27b():
    t = open(BP + "/Part-02-7b_Source_Pack_UI_Catalog_and_UX_Enhancements.md", encoding="utf-8").read()
    parts = re.split(r"\n(### 2\.7\.[0-9.]+ ([AW]\d+)[^:\n]*: [^\n]*)\n", t)
    cards = {}
    for i in range(1, len(parts), 3):
        cards[parts[i + 1]] = parts[i] + "\n" + parts[i + 2]
    return cards


def csv_rows(path, skip=2):
    rows = list(csv.reader(open(path, encoding="utf-8-sig")))
    return rows[skip:]


STOP = set("a an the and or of to for in on by with / & - per · ( ) , : ; id no".split())


def toks(s):
    return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 1]


def cover(label, text):
    """Covered if all tokens appear, Partial if half, else Not covered."""
    t = toks(label)
    if not t:
        return "Covered"
    low = text.lower()
    hit = sum(1 for w in t if w in low)
    if hit == len(t):
        return "Covered"
    if hit * 2 >= len(t):
        return "Partially covered"
    return "Not covered"


# ---------------------------------------------------------------- ID crosswalks
# V12 website IDs -> blueprint screen IDs (DEC-620 dual-ID namespace)
WEB_X = {f"W{i:02d}": f"W{i:02d}" for i in range(1, 35)}
WEB_X.update({"W35": "W49", "W36": "W50", "W37": "W51", "W38": "W46", "W39": "W47",
              "W40": "W45", "W41": "W52", "W99X": "W53"})
WEB_KIND = {"W35": "alias", "W36": "new", "W37": "new", "W38": "alias", "W39": "alias", "W40": "alias",
            "W41": "new", "W99X": "new"}
# Admin: V12 ID -> (blueprint ID(s), kind)
ADM_X = {f"A{i:03d}": (f"A{i:03d}", "same") for i in range(1, 114)}
for k, n in zip(range(26, 40), range(170, 184)):
    ADM_X[f"X{k}"] = (f"A{n}", "new")
for k, n in zip(range(1, 9), range(184, 192)):
    ADM_X[f"O{k:02d}"] = (f"A{n}", "new")
ADM_X.update({
    "SERVICES": ("A192", "new-utility"), "SVC-*": ("A193", "new-utility"), "WORKFLOWS": ("A194", "new-utility"),
    "WF-*": ("A195", "new-utility"), "INDEX": ("A196", "new-utility"), "ORG": ("A197", "new-utility"),
    "RUNS": ("A110", "alias"), "A089": ("A089", "same"),
    "A114": ("A198", "new"), "A115": ("A128", "alias"), "A116": ("A199", "new"), "A117": ("A012", "alias"),
    "A118": ("A200", "new"), "A119": ("A201", "new"), "A120": ("A163", "alias"), "A121": ("A202", "new"),
    "A122": ("A203", "new"), "A123": ("A002", "alias"), "A124": ("A009", "alias"), "A125": ("A168", "alias"),
    "A126": ("A103", "alias"), "A127": ("A204", "new"), "A128": ("A008", "alias"), "A129": ("A159", "alias"),
    "A130": ("A156", "alias"), "A131": ("A101", "alias"),
})
# secondary blueprint screens that also receive part of an aliased V12 screen
ADM_ALSO = {"A120": "A013", "A126": "A162", "A129": "A165", "A130": "A014", "A117": "A167", "A115": "A011",
            "A131": "A187"}

AUD_ROLE = {
    "Platform operator": "R01 acting as Service Owner (DEC-047), R13 Platform Support, R14 Platform Billing",
    "Tenant workspace": "R02–R12, R15 within own tenant and granted startups",
    "Automation operations": "R11 Automation Lead, R13 Platform Support (grant-scoped)",
    "Portfolio oversight": "R01 Founder / Portfolio Owner via explicit portfolio grants (aggregate only)",
}
AUD_SHORT = {"Platform operator": "OP", "Tenant workspace": "TW", "Automation operations": "AO",
             "Portfolio oversight": "PO", "Platform": "OP", "Tenant": "TW", "Automation": "AO", "Portfolio": "PO"}

FR_BASE = "FR-V12-G-"
TC_BASE = "TC-V12-G-"
