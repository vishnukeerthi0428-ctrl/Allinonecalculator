#!/usr/bin/env python3
"""Group Q (Part 11.18): atomic aspect inventory for AI voice, telephony and recordings.

Reads the V12 text extraction (BRD/FSD chapters) and the earlier V12 coverage registers,
extracts every voice-related aspect (SM-SVC-26 all four workflows, SM-SVC-36-WF03, the
voice/telephony/recording/transcription rules), maps each to the Part 11.18 IDs and
writes final/coverage_v12/Q_coverage.csv in the V12 format.

Usage: python3 -I q_voice_coverage.py <v12_dir> <blueprint_dir>
"""
import csv
import glob
import os
import re
import sys

V12, BP = sys.argv[1], sys.argv[2]
rows = []
seen = set()


def add(doc, chap, sec, aid, summ, before, loc, action, new, after="Matched"):
    if aid in seen:
        return
    seen.add(aid)
    summ = re.sub(r"\s+", " ", summ).strip()[:300]
    rows.append([doc, chap, sec, aid, summ, before, loc, action, new, after])


def lines(path):
    return open(path, encoding="utf-8").read().split("\n")


def ch(doc, prefix):
    return glob.glob(os.path.join(V12, doc, prefix + "*.txt"))[0]


def table_pairs(ls, start, end):
    """Return (field, spec) pairs from a 2-column [TABLE] block between line indexes."""
    out, cells = [], []
    for ln in ls[start:end]:
        if ln.startswith("---row") or ln.startswith("[TABLE]") or ln.startswith("[/TABLE]") or ln.startswith("<Heading"):
            if len(cells) >= 2:
                out.append(cells[:])
            cells = []
            continue
        cells.append(ln)
    if len(cells) >= 2:
        out.append(cells)
    return out


# ------------------------------------------------------------ FR mapping
FRMAP = [
    (r"disclos|self-identif|Disclose AI", "FR-V12-Q-002; AU-283"),
    (r"handoff|handover|human specialist|escalat", "FR-V12-Q-003, 004; AG-215"),
    (r"consent|permission|call permission", "FR-V12-Q-012, 020; AU-282"),
    (r"quiet hours|calling hours|window|time", "FR-V12-Q-014; AU-281"),
    (r"DND|DLT|NCPR|preference regist|scrub|Do Not Call|TCPA", "FR-V12-Q-011; AU-280"),
    (r"140|160|number series|CPaaS|number", "FR-V12-Q-030, 031; AU-284"),
    (r"language|Multilingual|multilingual", "FR-V12-Q-017; AG-210"),
    (r"booking|appointment|calendar|slot", "FR-V12-Q-018; AG-212"),
    (r"transcri", "FR-V12-Q-019; AU-282"),
    (r"recording", "FR-V12-Q-020…025; AU-282, AU-285, AU-286"),
    (r"redact", "FR-V12-Q-024; AU-285, AG-214"),
    (r"CRM|summary|notes", "FR-V12-Q-026, 027; AG-213"),
    (r"coach|rubric|learner|employment", "FR-V12-Q-040…046; AG-216"),
    (r"minute|meter|cost|budget|price|INR", "FR-V12-Q-036; AU-287"),
    (r"intent|routing|route", "FR-V12-Q-001, 009; AG-210"),
    (r"outbound|initiate", "FR-V12-Q-010, 011; AU-280"),
    (r"entitle|SKU|revoke", "FR-V12-Q-053"),
    (r"idempot|replay|duplicate|reconcil", "FR-V12-Q-028; AU-287"),
    (r"tenant|company|scope|isolation", "FR-V12-Q-054, 055"),
]


def frs(text):
    hits = [ids for pat, ids in FRMAP if re.search(pat, text, re.I)]
    return "; ".join(hits[:3]) if hits else "FR-V12-Q-048; DEC-860"


SEC = "Part 11.18a §11.18.5"

# ------------------------------------------------------------ BRD 08 SVC-26 and SVC-36 service tables
b08 = lines(ch("BRD", "08_"))
for name, svc in (("SM-SVC-26", "26"), ("SM-SVC-36", "36")):
    i = next(k for k, l in enumerate(b08) if l.startswith("<Heading2> " + name + " "))
    j = next(k for k in range(i + 1, len(b08)) if b08[k].startswith("<Heading2>"))
    for f, *spec in table_pairs(b08, i, j):
        if f == "Requirement / field":
            continue
        s = " ".join(spec)
        if svc == "36" and not re.search(r"record|coach|privacy|employment|permitted|rubric|WF03", s + f, re.I):
            continue
        before = "Conflict (Pending Founder decision: CONFLICT-779/815/818)" if svc == "26" or re.search("record", s, re.I) else "Partially covered"
        add("BRD", "08 Master Automation Service Catalogue", name, "Q-B08-%s-%s" % (svc, re.sub(r"\W", "", f)[:18]),
            "%s: %s" % (f, s), before, "Part 11.2c §11.2.5.36/46; Part 11.4c §11.4.5.15", "Adopted per DEC-782; specified in " + SEC,
            frs(f + " " + s))

# ------------------------------------------------------------ BRD 09 workflow rows
b09 = lines(ch("BRD", "09_"))
for k, l in enumerate(b09):
    if re.fullmatch(r"SM-SVC-26-WF0[1-4]|SM-SVC-36-WF03", l):
        outcome, io, kpi, risk = b09[k + 1:k + 5]
        for tag, val in (("outcome", outcome), ("io", io), ("kpi", kpi), ("risk", risk)):
            add("BRD", "09 Business Workflow Catalogue", l, "Q-B09-%s-%s" % (l[3:], tag), "%s %s: %s" % (l, tag, val),
                "Conflict (Pending Founder decision: CONFLICT-815/818)", "Part 11.4c §11.4.5.15; Part 11.4d §11.4.5.25",
                "Workflow enabled per jurisdiction pack (DEC-782, DEC-860)", frs(val) + "; " + ("US-22-ZQ01…14" if "26" in l else "US-08-ZQ01…03"))

# ------------------------------------------------------------ BRD single rows
b11 = lines(ch("BRD", "11_"))
k = b11.index("SM-SVC-26")
add("BRD", "11 Pricing Billing Unit Economics", "SKU meter table", "Q-B11-26-meter", "SM-SVC-26 meter %s; illustrative %s; %s" % tuple(b11[k + 1:k + 4]),
    "Partially covered", "Part 11.2c §11.2.5.36 commercial", "Call-minute meter and cost model §11.18.5.12, §11.18.9", "FR-V12-Q-036; AU-287")
b14 = lines(ch("BRD", "14_"))
k = b14.index("SM-SVC-26")
add("BRD", "14 Digital Marketing Omnichannel", "Service map", "Q-B14-26", "SM-SVC-26 %s: %s" % (b14[k + 1], b14[k + 2]), "Covered", "Part 11.2c", "Reconfirmed", "EP-22")
b14x = [l for l in b14 if "Voice/media require rights and disclosure" in l]
if b14x:
    add("BRD", "14 Digital Marketing Omnichannel", "Channel controls", "Q-B14-voicerights", b14x[0], "Partially covered", "Part 11.6b AU-177", "Disclosure and voice rights §11.18.5.2, §11.18.5.11", "FR-V12-Q-002, 039")
b24 = lines(ch("BRD", "24_"))
k = b24.index("SM-SVC-26-ENT-AT01")
add("BRD", "24 Business Acceptance", "Entitlement acceptance", "Q-B24-26-ENT", "SM-SVC-26-ENT-AT01: %s; %s" % (b24[k + 1], b24[k + 2]), "Partially covered", "Part 11.2c TC-V12-B-236", "Entitlement test kept; voice activation gate added", "FR-V12-Q-053; TC-V12-Q-090")
b20 = lines(ch("BRD", "20_"))
for rid in ("CJ-US-03", "CJ-AU-01", "CJ-SG-01", "CJ-AE-01", "CJ-UK-02", "CJ-IN-06", "CJ-IN-07", "CJ-US-01", "BR-V7-CJ-04", "BR-V7-CJ-03"):
    for k, l in enumerate(b20):
        if l == rid:
            txt = " ".join(b20[k + 1:k + 5])
            add("BRD", "20 Security Privacy Compliance", "Jurisdiction rules", "Q-B20-" + rid, rid + ": " + txt,
                "Partially covered", "Part 11.6a F18-*; Part 11.15a RP-IN-SMS", "Voice rule in jurisdiction matrix §11.18.5.3", "FR-V12-Q-011, 014, 020; AU-280")
            break
for l in b20:
    if l.startswith("Legal sign-off matrix by country/channel/industry"):
        add("BRD", "20 Security Privacy Compliance", "Legal sign-off", "Q-B20-legalmatrix", l, "Partially covered", "Part 11.15a", "Voice counsel sign-off checklist §11.18.5.3.4", "FR-V12-Q-048; DEC-861")

# ------------------------------------------------------------ FSD 11 SVC-26 and SVC-36
f11 = lines(ch("FSD", "11_"))
for name, svc in (("SM-SVC-26", "26"), ("SM-SVC-36", "36")):
    i = next(k for k, l in enumerate(f11) if l.startswith("<Heading2> " + name + " "))
    j = next(k for k in range(i + 1, len(f11)) if f11[k].startswith("<Heading2>"))
    for f, *spec in table_pairs(f11, i, j):
        if f == "Requirement / field":
            continue
        s = " ".join(spec)
        if svc == "36" and not re.search(r"record|coach|privacy|employment|permitted|meeting", s, re.I):
            continue
        add("FSD", "11 Master Functional Specification", name, "Q-F11-%s-%s" % (svc, re.sub(r"\W", "", f)[:18]), "%s: %s" % (f, s),
            "Conflict (Pending Founder decision: CONFLICT-779/815/818)", "Part 11.2c §11.2.5.36", "Adopted per DEC-782; " + SEC, frs(f + " " + s))

# ------------------------------------------------------------ FSD 12 workflow specs
f12 = lines(ch("FSD", "12_"))
for wf in ("SM-SVC-26-WF01", "SM-SVC-26-WF02", "SM-SVC-26-WF03", "SM-SVC-26-WF04", "SM-SVC-36-WF03"):
    i = next(k for k, l in enumerate(f12) if l.startswith("<Heading3> " + wf + " "))
    j = next(k for k in range(i + 1, len(f12)) if f12[k].startswith("<Heading"))
    for cells in table_pairs(f12, i, j):
        f = cells[0]
        if f in ("Requirement / field", "Proposed DTO field", "Step ID"):
            continue
        s = " ".join(cells[1:])
        if f.startswith(wf + "-STEP"):
            aid = "Q-F12-%s" % f[3:]
            summ = "%s %s; executor %s; output %s; failure %s" % (f, cells[1], cells[2], cells[3], cells[4] if len(cells) > 4 else "")
        elif re.fullmatch(r"[a-z_]+", f):
            aid = "Q-F12-%s-dto-%s" % (wf[3:], f)
            summ = "%s DTO field %s: %s" % (wf, f, s)
        else:
            aid = "Q-F12-%s-%s" % (wf[3:], re.sub(r"\W", "", f)[:18])
            summ = "%s %s: %s" % (wf, f, s)
        add("FSD", "12 Executable Workflow Specification", wf, aid, summ,
            "Conflict (Pending Founder decision: CONFLICT-815/818)", "Part 11.4c §11.4.5.15; Part 11.4d §11.4.5.25",
            "Executable spec with voice controls §11.18.5.13", frs(summ))
    for l in f12[i:j]:
        if l.startswith("Acceptance IDs:"):
            for tid in re.findall(r"SM-SVC-\d\d-WF0\d-TC-[A-Z]+", l):
                add("FSD", "12 Executable Workflow Specification", wf, "Q-F12-" + tid[3:], "Acceptance ID " + tid,
                    "Partially covered (mapped TC-V12-D-101…110, disabled)", "Part 11.4c", "Executed as TC-V12-Q-1xx (§11.18b)", "TC-V12-Q-101…146")
        if l.startswith("Common contract: FSD-POL-V6-PRECHECK"):
            add("FSD", "12 Executable Workflow Specification", wf, "Q-F12-%s-precheck" % wf[3:], wf + " " + l, "Covered", "Part 11.4b §11.4b.5", "AU-280 extends precheck for voice", "AU-280")

# ------------------------------------------------------------ FSD 13 registry rows
f13 = lines(ch("FSD", "13_"))
for k, l in enumerate(f13):
    if re.fullmatch(r"SM-SVC-26-WF0[1-4]|SM-SVC-36-WF03", l):
        add("FSD", "13 Step Trigger Event Registry", "Step registry", "Q-F13-" + l[3:], "%s steps %s; %s; controls %s" % (l, f13[k + 1], f13[k + 2], f13[k + 3]),
            "Partially covered", "Part 11.4b", "Step classes and events §11.18.6.4", "FR-V12-Q-052; events voice.*")

# ------------------------------------------------------------ single-line FSD rows
singles = [
    ("02_", "Email, SMS (DLT), voice (140/160 series)", "02 System Context", "Q-F02-voice", "FR-V12-Q-030; AU-284"),
    ("08_", "SM-SVC-26; SM-SVC-27; SM-SVC-36", "08 Service Registry", "Q-F08-ENG04", "§11.18.5.10 ENG-04 voice implementation"),
    ("14_", "SM-SVC-26; SM-SVC-27; SM-SVC-36", "14 Shared Engines", "Q-F14-ENG04", "§11.18.5.10"),
    ("15_", "56: SM-SVC-26-WF01", "15 Agent Registry", "Q-F15-AGT20", "AG-210…219 bound to AGT-20"),
]
for pre, needle, chap, aid, new in singles:
    ls = lines(ch("FSD", pre))
    for k, l in enumerate(ls):
        if needle in l:
            ctx = " ".join(ls[max(0, k - 2):k + 3])
            add("FSD", chap, "Voice row", aid, ctx, "Partially covered", "Part 11.6a/b", "Mapped in " + SEC, new)
            break
f16 = lines(ch("FSD", "16_"))
k = f16.index("EVAL-SM-SVC-26-WF01")
add("FSD", "16 AI Models Prompts Evaluation", "Evaluation suites", "Q-F16-EVAL26", "EVAL-SM-SVC-26-WF01 %s; %s; cases %s; %s; languages %s" % tuple(f16[k + 1:k + 6]),
    "Partially covered (TC-V12-F-278, disabled)", "Part 11.6b §11.6.5.5", "Suite extended to six languages and WF02–WF04 (§11.18b AI eval)", "TC-V12-Q-401…448")
f20 = lines(ch("FSD", "20_"))
for k, l in enumerate(f20):
    if re.fullmatch(r"SM-SVC-26-WF0[1-4]|SM-SVC-36-WF03", l):
        add("FSD", "20 Public SaaS Website", "Service demo fixtures", "Q-F20-" + l[3:], "%s %s: %s" % (l, f20[k + 1], f20[k + 2]),
            "Covered (simulation only)", "Part 11.7a", "Fixture kept; production path gated (FR-V12-Q-052)", "FR-V12-Q-052")
f21 = lines(ch("FSD", "21_"))
for k, l in enumerate(f21):
    if l.startswith("SM-SVC-26 — Voice campaign") or l.startswith("SM-SVC-36 — Sales coaching") or l == "SM-SVC-26":
        add("FSD", "21 Tenant Portal Workspace", "Domain panel", "Q-F21-%d" % k, " ".join(f21[k:k + 4]), "Covered (A170/A180 cards)", "Part 11.7b A170, A180",
            "Tabs A170-Q1…Q8, A180-Q1…Q3 (§11.18.6.1)", "FR-V12-Q-001…055 screens")
f24 = lines(ch("FSD", "24_"))
for k, l in enumerate(f24):
    if l.startswith("X26 ") or l.startswith("X36 "):
        add("FSD", "24 UI UX Components", "Workspace", "Q-F24-" + l[:3], " ".join(f24[k:k + 3]), "Covered", "Part 11.7a FR-V12-G-040", "Extended §11.18.6.1", "A170-Q1…Q8")
f26 = lines(ch("FSD", "26_"))
i = next(k for k, l in enumerate(f26) if "Domain schema voice_session" in l)
j = next(k for k in range(i + 1, len(f26)) if f26[k].startswith("<Heading"))
for cells in table_pairs(f26, i, j):
    if cells[0] == "Field":
        continue
    add("FSD", "26 PostgreSQL Schema", "voice_session", "Q-F26-" + cells[0], "voice_session.%s: %s" % (cells[0], " ".join(cells[1:])),
        "Partially covered (eng_call disabled)", "Part 11.4d eng_call", "Entity voice_session and children §11.18.6.2", "voice_session; FR-V12-Q-054")
f33 = lines(ch("FSD", "33_"))
for k, l in enumerate(f33):
    if re.fullmatch(r"SM-SVC-(26-WF0[1-4]|36-WF03)-(STEP-0\d-TC|TC-[A-Z]+)", l):
        add("FSD", "33 Test Specifications", "Workflow and step tests", "Q-F33-" + l[3:], "%s: %s" % (l, " | ".join(f33[k + 1:k + 5])),
            "Partially covered (not run; disabled)", "Part 11.4c TC-V12-D-101…111", "Executable case in Part 11.18b §11.18.11", "TC-V12-Q-101…146")
f35 = lines(ch("FSD", "35_"))
k = f35.index("SM-SVC-26-BUILD")
add("FSD", "35 Coding Standards Backlog", "Build tasks", "Q-F35-26BUILD", "SM-SVC-26-BUILD: %s; %s" % (f35[k + 1], f35[k + 2]), "Partially covered", "Part 11.10c",
    "Build plan and effort §11.18.14", "EP-22 stories US-22-ZQ01…14")
f40 = lines(ch("FSD", "40_"))
for k, l in enumerate(f40):
    if re.fullmatch(r"SM-SVC-26-WF0[1-4]|SM-SVC-36-WF03", l):
        add("FSD", "40 Traceability", "Trace row", "Q-F40-%s-%d" % (l[3:], k), " | ".join(f40[k:k + 10]), "Partially covered", "Part 11.11a/b",
            "Trace extended to FR-V12-Q / TC-V12-Q", "RTM rows §11.18.13")
fa = lines(ch("FSD", "AP_Appendix_A_"))
for k, l in enumerate(fa):
    if 'tags: ["SM-SVC-26"]' in l:
        op = next((fa[m].strip() for m in range(k, max(0, k - 6), -1) if re.match(r"\s+(get|post|put|patch|delete):", fa[m])), "op")
        path = next((fa[m].strip() for m in range(k, max(0, k - 12), -1) if re.match(r"\s+/api/", fa[m])), "path")
        add("FSD", "Appendix A OpenAPI", "SM-SVC-26 tagged operation", "Q-FAA-%d" % k, "%s %s used by SM-SVC-26-WF01" % (op, path), "Covered (candidate reuse)", "Part 11.8a",
            "Kept; voice API family API-V12-Q-001…040 added", "API-V12-Q-001…040")
fb = lines(ch("FSD", "AP_Appendix_B_"))
for l in fb:
    m = re.search(r'"\$id":"urn:sm:dto:(SM-SVC-(26-WF0\d|36-WF03)):v2"', l)
    if m:
        add("FSD", "Appendix B DTO schemas", m.group(1), "Q-FAB-" + m.group(1)[3:], "DTO urn:sm:dto:%s:v2 (%d chars)" % (m.group(1), len(l)), "Covered (Part 11.4c table)", "Part 11.4c",
            "v3 voice projection adds consent, disclosure, language, recording fields (§11.18.6.3)", "voice DTO v3")
fc = lines(ch("FSD", "AP_Appendix_C_"))
for k, l in enumerate(fc):
    if "SM-SVC-26-WF0" in l or "SM-SVC-36-WF03" in l:
        tname = next((fc[m] for m in range(k, max(0, k - 40), -1) if fc[m].startswith("CREATE TABLE")), "CREATE TABLE ?")
        add("FSD", "Appendix C DDL", "Table used by voice workflows", "Q-FAC-%d" % k, tname.strip()[:120] + " (used by SM-SVC-26/36 workflows)", "Covered", "Part 11.9b",
            "Reused; voice tables added with RLS (§11.18.6.2)", "voice_* tables")

# ------------------------------------------------------------ earlier pending rows
pat = re.compile(r"SVC-26|SVC-36-WF03|CONFLICT-779|CONFLICT-815|CONFLICT-818|INT-05|AI voice|recording", re.I)
for f in sorted(glob.glob(os.path.join(BP, "final/coverage_v12/[A-M]_coverage.csv"))):
    for r in csv.DictReader(open(f, encoding="utf-8")):
        if r["status_after"].startswith("Pending Founder") and pat.search(" ".join(r.values())) and "CONFLICT-958" not in r["status_after"]:
            add(r["doc"], r["chapter"], r["section"], "Q-PRIOR-" + r["aspect_id"], "[from %s] %s" % (os.path.basename(f), r["aspect_summary"]),
                "Pending Founder decision", r["blueprint_location"], "Founder adopted V12 (DEC-782); specified in " + SEC, frs(r["aspect_summary"]) + "; DEC-860")

out = os.path.join(BP, "final/coverage_v12/Q_coverage.csv")
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["doc", "chapter", "section", "aspect_id", "aspect_summary", "status_before", "blueprint_location", "action", "new_ids", "status_after"])
    w.writerows(rows)
from collections import Counter
cb = Counter(r[5].split(" (")[0] for r in rows)
cd = Counter(r[0] for r in rows)
print(len(rows), dict(cb), dict(cd))
cc = Counter(r[1] for r in rows)
for k_, v in cc.most_common():
    print(v, k_)
