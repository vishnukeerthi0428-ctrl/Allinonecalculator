"""Parse Part 5.1 stories (files 1b, 1c) into structured stories and AC scenarios."""
import re

BP = "/home/user/Allinonecalculator/blueprint/"
FILES = [BP + "Part-05-1b_Epics_Stories_Foundation.md", BP + "Part-05-1c_Epics_Stories_Foundation.md"]

ID_RX = re.compile(r"\b(?:FR-(?:W\d{2}|A\d{3}|OP\d{3}|[A-Z]{2,4}-(?:\d{2}|RULES))|BR-(?:M\d{2}|S\d{3}|TENANT|WEB|AUTO|SVC|QA)|"
                   r"BRL-[A-Z]{2,4}-\d{2}|NFR-\d{3}|DEC-\d{3}|ABAC-\d{2}|AP-\d{2}|KPI-\d{2}|CA-[A-Z]+|NT-\d{3}|CFG-\d{2})\b")


def expand_ranges(text):
    """Expand BRL-ELG-01…18, BRL-PRV-01, -02, -03 and BR-M10–BR-M16 style ranges."""
    out = []
    for m in re.finditer(r"(BRL-[A-Z]{2,4}-)(\d{2})\s*[…–-]\s*(?:BRL-[A-Z]{2,4}-)?(\d{2})\b", text):
        a, b = int(m.group(2)), int(m.group(3))
        if b > a:
            out += [f"{m.group(1)}{i:02d}" for i in range(a, b + 1)]
    for m in re.finditer(r"(BRL-[A-Z]{2,4}-)(\d{2})((?:,\s*-\d{2})+)", text):
        out.append(m.group(1) + m.group(2))
        out += [m.group(1) + x for x in re.findall(r"-(\d{2})", m.group(3))]
    for m in re.finditer(r"BR-M(\d{2})\s*[–…]\s*BR-M(\d{2})", text):
        out += [f"BR-M{i:02d}" for i in range(int(m.group(1)), int(m.group(2)) + 1)]
    return out


def ids_in(text):
    s = list(dict.fromkeys(ID_RX.findall(text) + expand_ranges(text)))
    return s


def parse():
    stories = {}
    order = []
    for f in FILES:
        t = open(f, encoding="utf-8").read()
        for m in re.finditer(r"^##### (US-\d{4}) (.*?)\n(.*?)(?=^#{3,5} |\Z)", t, re.S | re.M):
            us, title, body = m.group(1), m.group(2).strip(), m.group(3)

            def g(k):
                mm = re.search(r"^\| " + k + r" \| (.*?) \|$", body, re.M)
                return mm.group(1).strip() if mm else ""
            st = dict(us=us, title=title, long_title=g("Title"), type=g("Type"), traces=g("Traces"),
                      priority=g("Priority").split(" ")[0], wave=g("Wave"), dims=g("Dimension profile"),
                      notes=g("Notes"), persona=g("Persona / roles"))
            st["trace_ids"] = ids_in(st["traces"])
            st["epic"] = "EP-" + us[3:5]
            gm = re.search(r"```gherkin\n(.*?)```", body, re.S)
            gh = gm.group(1) if gm else ""
            st["background"] = []
            st["scenarios"] = []
            cur = None
            pending_tags = []
            in_bg = False
            kw_ctx = None
            for line in gh.split("\n"):
                s = line.strip()
                if not s or s.startswith("Feature:"):
                    continue
                if s.startswith("Background:"):
                    in_bg = True
                    continue
                if s.startswith("@"):
                    pending_tags = s.split()
                    in_bg = False
                    continue
                sm = re.match(r"Scenario(?: Outline)?: (AC-\d{4}-\d{2}) (.*)", s)
                if sm:
                    in_bg = False
                    cur = dict(ac=sm.group(1), title=sm.group(2).strip(), tags=[x[1:] for x in pending_tags],
                               given=[], when=[], then=[], examples=[], outline="Outline" in s)
                    pending_tags = []
                    st["scenarios"].append(cur)
                    kw_ctx = None
                    continue
                km = re.match(r"(Given|When|Then|And|But)\s+(.*)", s)
                if in_bg and km:
                    st["background"].append(km.group(2))
                    continue
                if cur is None:
                    continue
                if s.startswith("Examples:"):
                    kw_ctx = "ex"
                    continue
                if kw_ctx == "ex" and s.startswith("|"):
                    cells = [c.strip() for c in s.strip("|").split("|")]
                    cur["examples"].append(cells)
                    continue
                if km:
                    k = km.group(1)
                    if k in ("Given", "When", "Then"):
                        kw_ctx = k.lower()
                    cur.setdefault(kw_ctx or "then", []).append(km.group(2))
                else:
                    cur["then"].append(s)
            stories[us] = st
            order.append(us)
    return stories, order


if __name__ == "__main__":
    s, o = parse()
    n = sum(len(s[u]["scenarios"]) for u in o)
    print(len(o), "stories", n, "ACs")
    print(s["US-0601"]["scenarios"][3])
    print(s["US-0304"]["trace_ids"])
