#!/usr/bin/env python3
"""Build the Part 9.2 appendices (glossary first-use, ID registry, consolidated registers,
duplicate-ID check, document map) from the blueprint Markdown parts.

Usage:  python3 blueprint/assembly/build_registers.py [--no-write]

Inputs : blueprint/Part-*.md (Part-09-2 itself is excluded from every scan) and the PDFs next to them
Outputs: blueprint/final/*.csv (one file per register) and the generated blocks of
         blueprint/Part-09-2_Glossary_and_Registers.md, replaced between
         <!-- GEN:<NAME>:BEGIN --> and <!-- GEN:<NAME>:END --> markers.
The glossary terms and definitions are hand-written in Part 9.2. This script fills only their
"First use" column, by searching the parts in reading order.
Deterministic: same inputs give the same output. Standard library only (+ pdfinfo for page counts).
"""
import csv
import difflib
import re
import subprocess
import sys
from collections import defaultdict, OrderedDict
from pathlib import Path

BP = Path(__file__).resolve().parent.parent
FINAL = BP / "final"
SELF = BP / "Part-09-2_Glossary_and_Registers.md"
TAGS = ("ASSUMPTION", "GAP", "CONFLICT", "RECOMMENDATION")
ELL = "…"


# ----------------------------------------------------------------------------------------------
# Loading parts
# ----------------------------------------------------------------------------------------------
def part_label(path):
    """Part-03-1_Architecture.md -> '3.1'; Part-00A_... -> '0A'; Part-05-1a_... -> '5.1a'."""
    m = re.match(r"Part-(\d+)([A-Z]?)(?:-(\d+)([a-z]?))?_", path.name)
    major, letter, minor, sub = m.groups()
    lab = str(int(major)) + letter
    if minor:
        lab += "." + str(int(minor)) + (sub or "")
    return lab


def part_key(path):
    m = re.match(r"Part-(\d+)([A-Z]?)(?:-(\d+)([a-z]?))?_", path.name)
    major, letter, minor, sub = m.groups()
    return (int(major), letter or "", int(minor or 0), sub or "")


def load_parts():
    files = sorted((p for p in BP.glob("Part-*.md") if p.name != SELF.name), key=part_key)
    parts = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()
        # Per-line section context and fence flag
        sec, fence, ctx = "", False, []
        for ln in lines:
            if ln.startswith("```"):
                fence = not fence
                ctx.append((sec, True))
                continue
            if not fence:
                h = re.match(r"^(#{2,6})\s+(.*)", ln)
                if h:
                    sec = section_ref(h.group(2))
            ctx.append((sec, fence))
        parts.append({"path": f, "label": part_label(f), "text": text, "lines": lines, "ctx": ctx})
    return parts


def section_ref(heading):
    h = clean(heading)
    if h.startswith("Application Blueprint"):
        return "front matter"
    m = re.match(r"^(\d+(?:\.\d+)*[a-z]?)\b", h)
    if m:
        return "§" + m.group(1)
    m = re.match(r"^([A-H])\.\s", h)  # Part 0A uses lettered sections
    if m:
        return "§" + m.group(1)
    return h[:40]


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = re.sub(r"\*\*|__|`", "", s)
    s = re.sub(r"\[(ASSUMPTION|GAP|CONFLICT|RECOMMENDATION)-(\d+)\]", r"\1-\2", s)
    return re.sub(r"\s+", " ", s).strip()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_table_row(line):
    return line.startswith("|") and not re.match(r"^\|\s*:?-{3,}", line)


def md_cell(s, n=None):
    s = clean(s).replace("|", "/")
    if n and len(s) > n:
        s = s[: n - 1].rsplit(" ", 1)[0] + " " + ELL
    return s


def nat_key(s):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


# ----------------------------------------------------------------------------------------------
# ID registry definition (curated: meaning and owner; ranges and counts are computed)
# ----------------------------------------------------------------------------------------------
# (label, regex with group 'n' = number and optional group 'f' = family, meaning, owning part)
REGISTRY = [
    ("BR-M##", r"\bBR-M(?P<n>\d{2})\b", "Business requirement derived from a BRD module line (M01–M66)", "1 (§1.12)"),
    ("BR-S###", r"\bBR-S(?P<n>\d{3})\b", "Business requirement derived from a source statement", "1 (§1.12)"),
    ("BR-{group}", r"\bBR-(?P<f>TENANT|WEB|AUTO|SVC|QA)\b", "Group-level business requirement (tenant, website, automation, service, QA)", "1 (§1.12)"),
    ("FR-W##", r"\bFR-W(?P<n>\d{2})\b", "Functional requirement for Website/Portal screen W01–W34", "2.1 (§2.4)"),
    ("FR-A###", r"\bFR-A(?P<n>\d{3})\b", "Functional requirement for Admin Command Centre screen A001–A113", "2.1 (§2.4)"),
    ("FR-OP###", r"\bFR-OP(?P<n>\d{3})\b", "Operational/platform functional requirement (health, readiness, config)", "2.1 (§2.4)"),
    ("FR-{area}-##", r"\bFR-(?P<f>STD|DM|UIS|FLT|PUB|ADP|ENG|COP|SRCH|NEG|CSM|SEC|AUD|NOT|RPT|I18N|CFG)-(?P<n>\d{2})\b", "Cross-cutting functional requirement by area (standards, data mgmt, UI states, filters, publication, adapters, …)", "2.1 (§2.4)"),
    ("NFR-###", r"\bNFR-(?P<n>\d{3})\b", "Non-functional requirement", "0 (§0.6); detailed in 4.2"),
    ("DEC-###", r"\bDEC-(?P<n>\d{3})\b", "Binding decision (DEC-001…065 Part 0A; DEC-066… Part 9.1)", "0A, 9.1"),
    ("BRL-{domain}-##", r"\bBRL-(?P<f>[A-Z]{2,4})-(?P<n>\d{2})\b", "Business rule, by rule domain", "2.3"),
    ("R##", r"(?<![-\w])R(?P<n>\d{2})(?P<f>L?)\b", "RBAC role (R01–R20; L suffix = startup-scoped lead variant)", "2.3 (§2.21)"),
    ("P##", r"(?<![-\w])P(?P<n>\d{2})\b", "Persona", "1 (§1.6)"),
    ("KPI-##", r"\bKPI-(?P<n>\d{2})\b", "Key performance indicator", "1 (§1.4)"),
    ("EP-##", r"\bEP-(?P<n>\d{2})\b", "Epic", "0 (§0.10.2); stories in 5"),
    ("US-####", r"\bUS-(?P<f>\d{2})(?P<n>\d{2})\b", "User story (first two digits = epic)", "5"),
    ("AC-####-##", r"\bAC-\d{4}-\d{2}\b", "Acceptance criterion of a user story", "5"),
    ("TS-##-##", r"\bTS-(?P<f>\d{2})-(?P<n>\d{2})\b", "Test scenario (epic-based, DEC-093)", "6"),
    ("TC-##-###", r"\bTC-(?P<f>\d{2})-(?P<n>\d{3})\b", "Test case (epic-based, DEC-093)", "6"),
    ("TC-AI-AG###-##", r"\bTC-AI-AG(?P<f>\d{3})-(?P<n>\d{2,3})\b", "AI agent test case (per agent)", "6"),
    ("TC-AU-AU###-##", r"\bTC-AU-AU(?P<f>\d{3})-(?P<n>\d{2,3})\b", "Automation test case (per automation)", "6"),
    ("AG-###", r"\bAG-(?P<n>\d{3})\b", "AI agent", "7.1/7.2"),
    ("AU-###", r"\bAU-(?P<n>\d{3})\b", "Deterministic or AI-assisted automation", "7.1/7.2"),
    ("ADR-###", r"\bADR-(?P<n>\d{3})\b", "Architecture decision record", "3.1 (001–043), 4.1/4.3 (050–069), 7.3 (070–085)"),
    ("RSK-###", r"\bRSK-(?P<n>\d{3})\b", "Risk (feeds the Part 8 risk register)", "8 (raised in 3–7)"),
    ("THR-###", r"\bTHR-(?P<n>\d{3})\b", "STRIDE threat", "4.1 (§4.2.2)"),
    ("SC-##", r"\bSC-(?P<n>\d{2})\b", "Security control", "4.1"),
    ("RB-###", r"\bRB-(?P<n>\d{3})\b", "Operational runbook", "4.3"),
    ("SLO-##", r"\bSLO-(?P<n>\d{2})\b", "Service level objective", "4.2/4.3"),
    ("AL-##", r"\bAL-(?P<n>\d{2})\b", "Alert rule", "4.1/4.3"),
    ("LT-##", r"\bLT-(?P<n>\d{2})\b", "Load/performance test (DEC-092: owned by 6.1)", "6.1"),
    ("DQ-###", r"\bDQ-(?P<n>\d{3})\b", "Data quality check", "3.3"),
    ("API-###", r"\bAPI-(?P<n>\d{3})\b", "API operation in the derived catalogue (555 ops, DEC-104)", "3.2"),
    ("NT-###", r"\bNT-(?P<n>\d{3})\b", "Internal notification type", "2.4"),
    ("NX-##", r"\bNX-(?P<n>\d{2})\b", "External (customer-facing) notification type", "2.4"),
    ("RP-##", r"\bRP-(?P<n>\d{2})\b", "Report/analytics view", "2.4"),
    ("SR-##", r"\bSR-(?P<n>\d{2})\b", "Search capability", "2.4"),
    ("CFG-##", r"\bCFG-(?P<n>\d{2})\b", "Configuration domain", "2.4"),
    ("WF-##", r"\bWF-(?P<n>\d{2})\b", "End-to-end workflow / process flow", "2.2"),
    ("AP-##", r"\bAP-(?P<n>\d{2})\b", "Acceptance procedure (DEC-014)", "0A; tests in 6"),
    ("CAP-##", r"\bCAP-(?P<n>\d{2})\b", "Business capability (capability map)", "2.1"),
    ("CA-{code}", r"\bCA-(?P<f>[A-Z]{2,9})\b", "Acceptance profile applied to FRs (e.g. CA-PUB, CA-FIN)", "2.1"),
    ("J-##", r"\bJ-(?P<n>\d{2})\b", "User journey", "1 (§1.11)"),
    ("SH-##", r"\bSH-(?P<n>\d{2})\b", "Stakeholder", "1"),
    ("CN-##", r"\bCN-(?P<n>\d{2})\b", "Constraint", "1"),
    ("DP-##", r"\bDP-(?P<n>\d{2})\b", "External dependency", "1"),
    ("X-##", r"\bX-(?P<n>\d{2})\b", "Explicit exclusion (out of scope)", "1"),
    ("L-##", r"\bL-(?P<n>\d{2})\b", "Later / future scope item (W6+)", "1"),
    ("VH-##", r"\bVH-(?P<n>\d{2})\b", "Value hypothesis", "1"),
    ("PP-##", r"\bPP-(?P<n>\d{2})\b", "Product principle", "1"),
    ("PR-##", r"\bPR-(?P<n>\d{2})\b", "Problem statement", "1"),
    ("G-##", r"\bG-(?P<n>\d{2})\b", "Business goal", "1"),
    ("OQ-###", r"\bOQ-(?P<n>\d{3})\b", "Open question (all answered in 0A)", "0, 0A"),
    ("AMB-#", r"\bAMB-(?P<n>\d{1,2})\b", "Ambiguity in the source (resolved DEC-049…058)", "0, 0A"),
    ("E-##", r"\bE-(?P<n>\d{2})\b", "Errata item (Part 9.1); note E-# (one digit) = engine invariant in 2.2", "9.1"),
    ("ABAC-##", r"\bABAC-(?P<n>\d{2})\b", "Attribute-based access control rule", "2.3"),
    ("ENT-###", r"\bENT-(?P<n>\d{3})\b", "Logical data entity", "3.3"),
    ("CK-##", r"\bCK-(?P<n>\d{2})\b", "Database check constraint pattern", "3.3"),
    ("UQ-{kind}-##", r"\bUQ-(?P<f>IDEM|DUP)-(?P<n>\d{2})\b", "Uniqueness/idempotency key or duplicate rule", "3.3"),
    ("AD-##", r"\bAD-(?P<n>\d{2})\b", "Architecture driver", "3.1"),
    ("ARP-##", r"\bARP-(?P<n>\d{2})\b", "Architecture principle", "3.1"),
    ("FM-##", r"\bFM-(?P<n>\d{2})\b", "Failure mode (resilience analysis)", "3.1"),
    ("IP-##", r"\bIP-(?P<n>\d{2})\b", "Integration pattern", "3.2"),
    ("CT-##", r"\bCT-(?P<n>\d{2})\b", "Contract-test gate", "3.2"),
    ("REC-##", r"\bREC-(?P<n>\d{2})\b", "Reconciliation job", "3.2"),
    ("XR-{role}-##", r"\bXR-(?P<f>[A-Z]{2,3})-(?P<n>\d{2})\b", "Cross-role review finding", "3.2"),
    ("TB-##", r"\bTB-(?P<n>\d{2})\b", "Trust boundary", "4.1"),
    ("AZ-##", r"\bAZ-(?P<n>\d{2})\b", "Authorization enforcement layer", "4.1"),
    ("SE-##", r"\bSE-(?P<n>\d{2})\b", "Security event (logged/alerted)", "4.1"),
    ("SO-#", r"\bSO-(?P<n>\d)\b", "Security objective", "4.1"),
    ("SI-#", r"\bSI-(?P<n>\d{1,2})\b", "Security incident class", "4.1"),
    ("AIR-##", r"\bAIR-(?P<n>\d{2})\b", "AI-specific risk (injection, leakage, …)", "4.1"),
    ("DPIA-T#", r"\bDPIA-T(?P<n>\d{1,2})\b", "DPIA trigger", "4.1"),
    ("{rule set}-R#", r"\b(?P<f>EU|IT|WA|PCI|TR|GST|CA|IX|RPT)-R(?P<n>\d{1,2})\b", "Regulatory or design rule set (EU/UK GDPR, IT Act, WhatsApp, PCI, TRAI, GST, Canada, index, reporting)", "4.1, 3.3, 2.4"),
    ("CH-##", r"\bCH-(?P<n>\d{2})\b", "Chaos/resilience experiment", "4.2"),
    ("PL-##", r"\bPL-(?P<n>\d{2})\b", "CI/CD pipeline stage", "4.3"),
    ("DB-##", r"\bDB-(?P<n>\d{2})\b", "Operational dashboard", "4.3"),
    ("DM-###", r"\bDM-(?P<n>\d{3})\b", "Story-dimension matrix row (Part 5.1a)", "5.1a"),
    ("MAS-# / RR-#", r"\b(?P<f>MAS|RR)-(?P<n>\d{1,2})\b", "Mandatory AC scenario / required-risk scenario (story template)", "5.1a"),
    ("TP-##", r"\bTP-(?P<n>\d{2})\b", "Test principle", "6.1"),
    ("QO-#", r"\bQO-(?P<n>\d{1,2})\b", "Quality objective", "6.1"),
    ("RA-##", r"\bRA-(?P<n>\d{2})\b", "Risk area (risk-based testing)", "6.1"),
    ("RBR-#", r"\bRBR-(?P<n>\d{1,2})\b", "Release-blocking rule", "6.1"),
    ("PW-##", r"\bPW-(?P<n>\d{2})\b", "Pairwise test combination", "6.1"),
    ("EG-##", r"\bEG-(?P<n>\d{2})\b", "Error-guessing test idea", "6.1"),
    ("BVA-D##", r"\bBVA-D(?P<n>\d{2})\b", "Boundary-value analysis datum", "6.1"),
    ("DR-#", r"\bDR-(?P<n>\d{1,2})\b", "Disaster-recovery drill", "6.1"),
    ("CI-###", r"\bCI-(?P<n>\d{3})\b", "Candidate AI idea (discovery register)", "7.1"),
    ("TL-##", r"\bTL-(?P<n>\d{2})\b", "Agent tool in the tool registry", "7.2"),
    ("D0#", r"(?<![-\w])D0(?P<n>\d)\b", "Delivery persona (delivery-lifecycle AI)", "7.1"),
    ("B##", r"(?<![-\w])B(?P<n>\d{2})\b", "Budget line (cost table; GAP-006, DEC-020)", "0, 0A, 8"),
    ("UX-##", r"\bUX-(?P<n>\d{2})\b", "UX principle", "2.5"),
    ("I18N-##", r"\bI18N-(?P<n>\d{2})\b", "Internationalization rule", "2.4"),
    ("OPT-##-##", r"\bOPT-(?P<f>\d{2})-(?P<n>\d{2})\b", "FRD optimisation item (source ID, cited)", "Source (FRD)"),
    ("SM-UT-###", r"\bSM-UT-(?P<n>\d{3})\b", "Source test alias (FRD; aliases only, DEC-094)", "Source (FRD); 6"),
    ("M##", r"(?<![-\w])M(?P<n>\d{2})\b", "Source module M01–M66 (BRD §7)", "Source (BRD)"),
    ("W## / A###", r"(?<![-\w])(?P<f>W)(?P<n>\d{2})\b|(?<![-\w])A(?P<n2>\d{3})\b", "Screen ID: Website/Portal W01–W34, Admin A001–A113", "Source (FRD §16.2); 2.5"),
]


# Families whose short IDs also occur as synthetic fixture values in test rows (e.g. "portal grant G-55",
# "contract CT-58"): lines that describe fixtures are skipped for these families only.
FIXTURE_SENSITIVE = {"G-##", "CT-##", "J-##", "P##", "R##", "W## / A###", "D0#", "SH-##", "X-##", "L-##", "DP-##", "PR-##"}
FIXTURE_RX = re.compile(r"fixture|gse_syn|GSE-SYN|replay|Pre: |Given |\bWhen |\bThen ", re.I)


# Lines where a short family token is really part of another family's shorthand (e.g. "DM-R01…R40").
LINE_EXCLUDE = {"R##": r"DM-R\d", "G-##": r"grant G-\d", "D0#": r"BVA-D\d"}


def scan_registry(parts):
    rows, csv_rows = [], []
    for label, rx, meaning, owner in REGISTRY:
        r = re.compile(rx)
        ids, fams, nums, in_parts, defs = set(), defaultdict(list), [], OrderedDict(), defaultdict(int)
        for p in parts:
            hit = False
            for i, ln in enumerate(p["lines"]):
                if NOT_ISSUED_RX.search(ln) or (label in FIXTURE_SENSITIVE and FIXTURE_RX.search(ln)) \
                        or (label in LINE_EXCLUDE and re.search(LINE_EXCLUDE[label], ln)):
                    continue
                for m in r.finditer(ln):
                    ids.add(m.group(0))
                    gd = m.groupdict()
                    n = gd.get("n") or gd.get("n2")
                    f = gd.get("f") or ""
                    if label == "W## / A###":
                        f = "W" if gd.get("n") else "A"
                    if n is not None:
                        fams[f].append(int(n))
                    else:
                        fams[f].append(None)
                    hit = True
                first = cells(ln)[0] if is_table_row(ln) else ""
                hm = re.match(r"^#{2,6}\s+(\S+)", ln)
                head_tok = clean(hm.group(1)) if hm else ""
                if r.fullmatch(clean(first).strip("[]")) or (head_tok and r.fullmatch(head_tok)):
                    defs[p["label"]] += 1
            if hit:
                in_parts[p["label"]] = True
        if not ids:
            continue
        rng = []
        if label == "AC-####-##":
            srt = sorted(ids, key=nat_key)
            fams = {}
            rng.append(f"{srt[0]} {ELL} {srt[-1]} (story-scoped; numbering restarts per story)")
        for f in sorted(fams, key=nat_key):
            vals = sorted({v for v in fams[f] if v is not None})
            if vals:
                width = max(len(str(v)) for v in vals)
                sample = next(i for i in ids if re.fullmatch(rx, i))
                pad = len(re.search(r"\d+$", sample).group(0)) if re.search(r"\d+$", sample) else width
                lo, hi = str(vals[0]).zfill(pad), str(vals[-1]).zfill(pad)
                missing = (vals[-1] - vals[0] + 1) - len(vals)
                txt = (f + " " if f else "") + (f"{lo}–{hi}" if lo != hi else lo)
                if missing > 0:
                    txt += f" ({missing} unused)"
                rng.append(txt)
            else:
                rng.append(f)
        rng_s = "; ".join(rng)
        if len(rng_s) > 260:
            rng_s = rng_s[:255].rsplit(";", 1)[0] + f"; {ELL} ({len(rng)} families)"
        defined_in = ", ".join(k for k, _ in sorted(defs.items(), key=lambda kv: -kv[1])[:4]) or "referenced only"
        rows.append([label, meaning, rng_s, str(len(ids)), owner, defined_in, str(len(in_parts))])
        csv_rows.append([label, meaning, rng_s, len(ids), owner, defined_in, ";".join(in_parts)])
    return rows, csv_rows


# ----------------------------------------------------------------------------------------------
# Tag registers
# ----------------------------------------------------------------------------------------------
TAG_RX = re.compile(r"\b(ASSUMPTION|GAP|CONFLICT|RECOMMENDATION)-(\d{3})\b")
RANGE_RX = re.compile(r"\b(ASSUMPTION|GAP|CONFLICT|RECOMMENDATION|DEC)-(\d{3})\s*(?:…|\.\.\.?|–|to)\s*(?:\1-)?(\d{3})\b")
SHORT_RX = re.compile(r"\b(ASSUMPTION|GAP|CONFLICT|RECOMMENDATION|DEC)-(\d{3})((?:\s*(?:/|,)\s*-?\d{3})+)")


def expand_ids(text, kinds=TAGS + ("DEC",)):
    """All IDs referenced in text, with ranges (X-001…014) and short lists (X-112/101, X-101, -102) expanded."""
    out = set()
    for m in RANGE_RX.finditer(text):
        k, a, b = m.group(1), int(m.group(2)), int(m.group(3))
        if k in kinds and 0 < b - a <= 120:
            out.update(f"{k}-{n:03d}" for n in range(a, b + 1))
    for m in SHORT_RX.finditer(text):
        k = m.group(1)
        if k in kinds:
            out.add(f"{k}-{m.group(2)}")
            for n in re.findall(r"\d{3}", m.group(3)):
                out.add(f"{k}-{n}")
    for m in re.finditer(r"\b(ASSUMPTION|GAP|CONFLICT|RECOMMENDATION|DEC)-(\d{3})\b", text):
        if m.group(1) in kinds:
            out.add(m.group(0))
    return out


def context_statement(line, tag):
    if is_table_row(line):
        cs = [clean(c) for c in cells(line)]
        cs = [c for c in cs if c and not re.fullmatch(r"\[?" + tag + r"\]?", c)]
        s = " · ".join(cs)
    else:
        s = clean(re.sub(r"^#+\s*|^[-*]\s+|^>\s*", "", line))
    return s


NOT_ISSUED_RX = re.compile(r"not used|unused|not issued|reserved,? not|left unissued|not needed|were not required", re.I)


def scan_tags(parts):
    occ = defaultdict(list)          # id -> [(part, lineno, section)]
    regdefs = defaultdict(list)      # id -> [(part, statement, status, header)]
    for p in parts:
        hdr = None
        for i, ln in enumerate(p["lines"]):
            sec, fence = p["ctx"][i]
            if is_table_row(ln) and i + 1 < len(p["lines"]) and re.match(r"^\|\s*:?-{3,}", p["lines"][i + 1]):
                hdr = [clean(c).lower() for c in cells(ln)]
                continue
            if not ln.startswith("|"):
                hdr = None if ln.strip() == "" else hdr
            if not NOT_ISSUED_RX.search(ln):
                for m in TAG_RX.finditer(ln):
                    occ[m.group(0)].append((p["label"], i, sec))
            if is_table_row(ln):
                cs = cells(ln)
                first = clean(cs[0]).strip("[]").strip()
                if TAG_RX.fullmatch(first) and len(cs) >= 2:
                    status = ""
                    if hdr:
                        for j, h in enumerate(hdr):
                            if j < len(cs) and re.search(r"status|resolution|closure|disposition", h):
                                status = clean(cs[j])
                    stmt = next((clean(c) for c in cs[1:] if clean(c).lower().rstrip("s") not in
                                 ("assumption", "gap", "conflict", "recommendation", "type", "") and len(clean(c)) > 3), clean(cs[1]))
                    regdefs[first].append((p["label"], stmt, status, hdr or [], clean(" | ".join(cs[1:]))))
    return occ, regdefs


def status_rules(parts):
    """Resolution evidence from the decision logs (Part 0A, Part 9.1): id -> list of DEC IDs / notes."""
    res = defaultdict(set)
    accepted = set()
    for p in parts:
        if p["label"] not in ("0A", "9.1"):
            continue
        for ln in p["lines"]:
            if not is_table_row(ln):
                continue
            cs = cells(ln)
            first = clean(cs[0])
            ids = expand_ids(" ".join(cs[1:]), TAGS)
            m = re.fullmatch(r"DEC-(\d{3})", first)
            if m:
                for t in ids:
                    res[t].add(first)
                for t in re.findall(r"RECOMMENDATION-\d{3}\]?\)?\s*(?:\(|is\s+)?accepted", " ".join(cs)):
                    pass
                for mm in re.finditer(r"(RECOMMENDATION-\d{3})\]?\s*\)?\s*(?:accepted|\(accepted\))", clean(" ".join(cs))):
                    accepted.add(mm.group(1))
                if re.search(r"RECOMMENDATION-\d{3}[^|]{0,20}\(accepted\)|\baccepted\b", clean(" ".join(cs))):
                    for t in ids:
                        if t.startswith("RECOMMENDATION"):
                            accepted.add(t)
            else:
                # Summary rows such as "| CONFLICT-001…014 | Open | All resolved (DEC-001…014) |"
                tags_here = sorted(expand_ids(first, TAGS), key=nat_key)
                decs = sorted(expand_ids(" ".join(cs[1:]), ("DEC",)), key=nat_key)
                body = clean(" ".join(cs[1:])).lower()
                if tags_here and ("resolved" in body or "accepted" in body or "retained" in body):
                    for k, t in enumerate(tags_here):
                        if "accepted" in body and t.startswith("RECOMMENDATION"):
                            accepted.add(t)
                        if decs and len(decs) == len(tags_here):
                            res[t].add(decs[k])
                        elif "resolved" in body or "retained" in body:
                            res[t].add("Part " + p["label"] + " §G summary")
    return res, accepted


def build_tag_registers(parts):
    occ, regdefs = scan_tags(parts)
    res, accepted = status_rules(parts)
    order = {p["label"]: k for k, p in enumerate(parts)}
    by_kind = {k: [] for k in TAGS}
    dups = []
    for tid in sorted(set(occ) | set(regdefs), key=nat_key):
        kind = tid.split("-")[0]
        oc = sorted(occ.get(tid, []), key=lambda o: (order[o[0]], o[1]))
        first_part = oc[0][0] if oc else (regdefs[tid][0][0] if regdefs.get(tid) else "")
        first_sec = oc[0][2] if oc else ""
        defs = sorted(regdefs.get(tid, []), key=lambda d: order[d[0]])
        if defs:
            # prefer the first register row that is not merely a cross-reference
            stmt = defs[0][1]
            owner = defs[0][0]
            status_cell = defs[0][2]
            full = defs[0][4]
        else:
            p = next(pp for pp in parts if pp["label"] == first_part)
            stmt = context_statement(p["lines"][oc[0][1]], tid)
            owner, status_cell, full = first_part, "", stmt
        used_in = sorted({o[0] for o in oc}, key=lambda l: order[l])
        # duplicate check: same tag defined with materially different statements in different parts
        seen_parts = {}
        for d in defs:
            seen_parts.setdefault(d[0], d[1])
        if len(seen_parts) > 1:
            items = list(seen_parts.items())
            base = items[0][1]
            for lab, txt in items[1:]:
                ratio = difflib.SequenceMatcher(None, base.lower()[:200], txt.lower()[:200]).ratio()
                if ratio < 0.25:
                    dups.append([tid, f"Part {items[0][0]}", base, f"Part {lab}", txt, f"{ratio:.2f}"])
        rec = {"id": tid, "first": f"{first_part} {first_sec}".strip(), "owner": owner, "stmt": stmt,
               "used": ", ".join(used_in), "n": len(oc), "status_cell": status_cell, "full": full}
        # status / resolution
        if kind == "CONFLICT":
            decs = sorted(res.get(tid, []), key=nat_key)
            if decs:
                src = "Part 0A" if any(re.match(r"DEC-0[0-5]\d|DEC-06[0-5]", d) for d in decs) else "Part 9.1"
                if any(re.match(r"DEC-0[0-5]\d|DEC-06[0-5]", d) for d in decs) and any(re.match(r"DEC-(06[6-9]|0[7-9]\d|1\d\d)", d) for d in decs):
                    src = "Parts 0A + 9.1"
                rec["status"] = f"Resolved — {src} ({', '.join(decs)})"
            else:
                low = (status_cell + " " + full).lower()
                if re.search(r"resolved|resolution|decided|adopt|governs|use |rule:|default|follow|precedence|wins|applies|apply", low):
                    rec["status"] = f"Resolved locally in Part {owner}"
                else:
                    rec["status"] = "Open — owner per source part"
        elif kind == "RECOMMENDATION":
            low = (status_cell + " " + full).lower()
            if tid in accepted or res.get(tid):
                decs = sorted(res.get(tid, []), key=nat_key)
                rec["status"] = "Accepted" + (f" ({', '.join(decs)})" if decs else "")
            elif re.search(r"\baccepted\b|\badopted\b", low):
                rec["status"] = f"Accepted (Part {owner})"
            else:
                rec["status"] = "Proposed"
        elif kind == "GAP":
            decs = sorted(res.get(tid, []), key=nat_key)
            if decs:
                rec["status"] = "Closed by " + ", ".join(d.replace(" summary", "") for d in decs)
            else:
                rec["status"] = md_cell(status_cell, 90) if status_cell else "Open — handling per source part"
        else:
            decs = sorted(res.get(tid, []), key=nat_key)
            real = [d for d in decs if d.startswith("DEC-")]
            rec["status"] = ("Cited by " + ", ".join(real)) if real else ("Retained (Part 0A §G)" if decs else None)
            rec["status"] = rec["status"] or (md_cell(status_cell, 90) if status_cell else "Open — validate per source part")
        by_kind[kind].append(rec)
    return by_kind, dups


# ----------------------------------------------------------------------------------------------
# ADR and DEC indexes
# ----------------------------------------------------------------------------------------------
def build_adr(parts):
    out = OrderedDict()
    for p in parts:
        lines = p["lines"]
        hdr = None
        for i, ln in enumerate(lines):
            h = re.match(r"^#{2,6}\s+(ADR-\d{3})\s+(.*)", ln)
            if h:
                status = ""
                for ln2 in lines[i + 1 : i + 8]:
                    sm = re.match(r"^\|\s*Status\s*\|\s*(.*?)\s*\|\s*$", ln2)
                    if sm:
                        status = clean(sm.group(1))
                        break
                out.setdefault(h.group(1), []).append([h.group(1), clean(h.group(2)), status or "See part", p["label"]])
                continue
            if is_table_row(ln) and i + 1 < len(lines) and re.match(r"^\|\s*:?-{3,}", lines[i + 1]):
                hdr = [clean(c).lower() for c in cells(ln)]
                continue
            if is_table_row(ln):
                cs = cells(ln)
                first = clean(cs[0])
                if re.fullmatch(r"ADR-\d{3}", first) and len(cs) >= 2:
                    status = ""
                    if hdr and "status" in hdr:
                        j = hdr.index("status")
                        status = clean(cs[j]) if j < len(cs) else ""
                    out.setdefault(first, []).append([first, clean(cs[1]), status or "Accepted in part (no status column)", p["label"]])
            elif not ln.strip():
                hdr = hdr
    rows, dups = [], []
    for k in sorted(out, key=nat_key):
        defs = out[k]
        rows.append(defs[0])
        for d in defs[1:]:
            if d[3] != defs[0][3]:
                r = difflib.SequenceMatcher(None, defs[0][1].lower(), d[1].lower()).ratio()
                if r < 0.45:
                    dups.append([k, f"Part {defs[0][3]}", defs[0][1], f"Part {d[3]}", d[1], f"{r:.2f}"])
    return rows, dups


def build_dec(parts):
    rows = OrderedDict()
    for p in parts:
        if p["label"] not in ("0A", "9.1"):
            continue
        hdr = None
        section = ""
        for i, ln in enumerate(p["lines"]):
            h = re.match(r"^##\s+(.*)", ln)
            if h:
                section = clean(h.group(1))
            if is_table_row(ln) and i + 1 < len(p["lines"]) and re.match(r"^\|\s*:?-{3,}", p["lines"][i + 1]):
                hdr = [clean(c).lower() for c in cells(ln)]
                continue
            if not is_table_row(ln):
                continue
            cs = cells(ln)
            first = clean(cs[0])
            if not re.fullmatch(r"DEC-\d{3}", first) or first in rows:
                continue
            if p["label"] == "9.1":
                subject = clean(cs[3]) if len(cs) > 3 else ""
                decision = clean(cs[4]) if len(cs) > 4 else ""
                src = "Errata " + clean(cs[1]) if len(cs) > 1 else ""
            else:
                subject = clean(cs[1])
                decision = clean(cs[-1])
                src = section.split(".")[0] if section else ""
            rows[first] = [first, "0A" if p["label"] == "0A" else "9.1", md_cell(subject, 90), md_cell(decision, 230)]
    return list(rows.values())


# ----------------------------------------------------------------------------------------------
# Duplicate IDs across registry families (same ID defined with different meaning in different parts)
# ----------------------------------------------------------------------------------------------
DEF_FAMILIES = ["RSK", "THR", "SC", "RB", "SLO", "AL", "LT", "DQ", "NT", "NX", "RP", "SR", "CFG", "WF", "AP",
                "CAP", "AG", "AU", "KPI", "EP", "CK", "AD", "ARP", "FM", "IP", "CT", "TB", "AZ", "SE", "AIR",
                "CH", "PL", "DB", "TP", "RA", "PW", "EG", "TL", "CI", "J", "SH", "CN", "DP", "X", "L", "VH",
                "PP", "PR", "G", "OQ", "ABAC", "UX", "I18N", "E", "B", "P", "M", "D", "C", "S", "T", "O", "V",
                "R-REC", "DR", "QO", "RBR", "SO", "SI", "MAS", "RR", "DM", "REC", "N", "DV", "TS"]


def build_id_dups(parts):
    rx = re.compile(r"^(?:" + "|".join(re.escape(f) for f in sorted(DEF_FAMILIES, key=len, reverse=True)) + r")-[A-Z]?\d{1,4}$")
    defs = defaultdict(list)
    for p in parts:
        for ln in p["lines"]:
            if not is_table_row(ln):
                continue
            cs = cells(ln)
            if len(cs) < 2:
                continue
            first = clean(cs[0]).strip("[]")
            tok = first.split(" ")[0]
            if rx.match(tok):
                rest = (first[len(tok):] + " " + clean(cs[1])).strip()
                defs[tok].append((p["label"], rest))
    raw = []
    for tid in sorted(defs, key=nat_key):
        per = OrderedDict()
        for lab, txt in defs[tid]:
            per.setdefault(lab, txt)
        if len(per) < 2:
            continue
        items = list(per.items())
        base_lab, base = items[0]
        for lab, txt in items[1:]:
            a = set(re.findall(r"[a-z]{4,}", base.lower()))
            b = set(re.findall(r"[a-z]{4,}", txt.lower()))
            if not a or not b:
                continue
            jac = len(a & b) / max(1, len(a | b))
            fam = tid.rsplit("-", 1)[0]
            if (fam, base_lab, lab) in NOT_DUPLICATE:
                continue
            if jac < 0.12:
                raw.append((fam, base_lab, lab, tid, base, txt, jac))
    # aggregate per (family, part A, part B) so a whole colliding range is one finding
    agg = OrderedDict()
    for fam, pa, pb, tid, a, b, jac in raw:
        agg.setdefault((fam, pa, pb), []).append((tid, a, b))
    out = []
    for (fam, pa, pb), lst in agg.items():
        ids = [x[0] for x in lst]
        rng = ids[0] if len(ids) == 1 else f"{ids[0]}{ELL}{ids[-1]} ({len(ids)} IDs)"
        out.append([rng, f"Part {pa}", f"e.g. {lst[0][0]} = {lst[0][1]}", f"Part {pb}", f"e.g. {lst[0][0]} = {lst[0][2]}", "low"])
    return out


# Family/part pairs the script flags but that are the same meaning in a shorter form (verified by reading):
NOT_DUPLICATE = {
    ("OQ", "0", "0A"),    # Part 0A answers the same open questions under short labels
    ("EP", "0", "6.2a"),  # Part 6.2a epic coverage table: second cell lists risk areas for the same epic
}


# ----------------------------------------------------------------------------------------------
# Document map
# ----------------------------------------------------------------------------------------------
def pdf_pages(md_path):
    pdf = md_path.with_suffix(".pdf")
    if not pdf.exists():
        return None
    try:
        outp = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=60).stdout
        m = re.search(r"^Pages:\s+(\d+)", outp, re.M)
        return int(m.group(1)) if m else None
    except Exception:
        return None


def build_docmap(parts, include_self=True):
    rows = []
    allp = list(parts)
    if include_self and SELF.exists():
        t = SELF.read_text(encoding="utf-8")
        allp.append({"path": SELF, "label": "9.2", "text": t, "lines": t.splitlines()})
    for p in allp:
        lines = p["lines"]
        title = next((clean(l[3:]) for l in lines if l.startswith("## Application Blueprint")), p["path"].stem)
        title = re.sub(r"^Application Blueprint:\s*", "", title)
        tops = [clean(l[3:]) for l in lines if l.startswith("## ") and not l.startswith("## Application Blueprint")]
        tops = [re.sub(r"^\d+(\.\d+)*[a-z]?\s*", "", t) for t in tops]
        tops = [t for t in tops if not re.search(r"quality gate|register of tags|tags issued|tag register", t, re.I)]
        contents = "; ".join(tops[:7]) + (f"; {ELL} (+{len(tops) - 7})" if len(tops) > 7 else "")
        diagrams = len(re.findall(r"^```mermaid", p["text"], re.M))
        status = next((clean(l) for l in reversed(lines) if l.startswith("**Status:")), "")
        pages = pdf_pages(p["path"])
        rows.append([p["label"], p["path"].name, title, contents, str(pages) if pages is not None else "not rendered",
                     str(diagrams), f"{len(p['text'].split()):,}", "Complete" if status else "In progress (no Status line)"])
    return rows


# ----------------------------------------------------------------------------------------------
# Glossary first-use
# ----------------------------------------------------------------------------------------------
GLOSS_SEARCH = {  # term key -> regex when the bold key itself is not the searchable form
    "Tier 0–3": r"Tier 0", "L0–L3": r"\bL[0-3]\b", "HSN/SAC": r"HSN|SAC\b", "RPO/RTO": r"\bRPO\b|\bRTO\b",
    "DoR/DoD": r"Definition of Ready|\bDoR\b", "CI/CD": r"CI/CD", "W0–W6": r"\bW0\b", "R01–R20": r"\bR01\b",
    "P01–P16": r"\bP01\b", "B01–B23": r"\bB01\b", "S1–S4": r"\bS1\b", "M01–M66": r"\bM01\b",
    "W01–W34": r"\bW01\b", "A001–A113": r"\bA001\b", "Release 1 / 2 / Future": r"Release 1",
    "Manual / Assisted / Supervised / Controlled Autonomous": r"Controlled Autonomous",
    "Public / Internal / Confidential / Restricted": r"Restricted",
    "MoSCoW": r"MoSCoW", "OKR": r"\bOKRs?\b", "first-touch template": r"(?i)first-touch",
    "autonomy L0–L3": r"\bL[0-3]\b", "receivable / payable ledger": r"(?i)receivable",
    "CustomerSubscription / ServiceSubscription": r"CustomerSubscription|ServiceSubscription",
    "rights request": r"(?i)rights request|data principal rights|privacy request", "EU AI Act risk class": r"EU AI Act",
    "Meta WhatsApp Business policy": r"WhatsApp Business", "story point": r"(?i)story points?\b",
    "receipt": r"(?i)\breceipts?\b", "reservation": r"(?i)\breservations?\b", "claim": r"(?i)\bclaims?\b",
    "signal": r"(?i)\bsignals?\b", "sequence": r"(?i)\bsequences?\b", "tenant": r"(?i)\btenants?\b", "INVEST": r"\bINVEST\b", "p95": r"\bp95\b",
}


def glossary_first_use(parts, md_text):
    order_lines = []
    for p in parts:
        for i, ln in enumerate(p["lines"]):
            sec, fence = p["ctx"][i]
            if not fence:
                order_lines.append((p["label"], sec, ln))
    found = {}
    out_lines = []
    in_g = False
    csv_rows = []
    for ln in md_text.splitlines():
        if ln.strip() == "<!-- GLOSSARY:BEGIN -->":
            in_g = True
        elif ln.strip() == "<!-- GLOSSARY:END -->":
            in_g = False
        if in_g and is_table_row(ln):
            cs = cells(ln)
            m = re.search(r"\*\*(.+?)\*\*", cs[0])
            if m and len(cs) >= 3:
                key = m.group(1)
                rx = GLOSS_SEARCH.get(key)
                if rx is None:
                    if re.search(r"[a-z]", key) and not re.match(r"^[A-Z][a-z]?[A-Z]", key):
                        rx = r"(?i)\b" + re.escape(key) + r"\b"
                    else:
                        rx = r"\b" + re.escape(key) + r"(?![A-Za-z0-9])"
                r = re.compile(rx)
                fu = "not found in Parts 0–9.1"
                for lab, sec, l2 in order_lines:
                    if r.search(l2):
                        fu = f"Part {lab} {sec}".strip()
                        break
                cs[2] = md_cell(fu, 60)
                ln = "| " + " | ".join(cs) + " |"
                csv_rows.append([clean(cs[0]), clean(cs[1]), fu])
        out_lines.append(ln)
    return "\n".join(out_lines) + ("\n" if md_text.endswith("\n") else ""), csv_rows


# ----------------------------------------------------------------------------------------------
# Markdown rendering helpers
# ----------------------------------------------------------------------------------------------
def compress(nums):
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"{nums[i]:03d}" if i == j else f"{nums[i]:03d}–{nums[j]:03d}")
        i = j + 1
    return ", ".join(out)


def build_alloc(tags, parts):
    order = [p["label"] for p in parts]
    per = defaultdict(lambda: defaultdict(list))
    for k, recs in tags.items():
        for r in recs:
            per[r["owner"]][k].append(int(r["id"].split("-")[1]))
    rows = []
    for lab in order:
        if lab in per:
            rows.append([f"Part {lab}"] + [compress(per[lab][k]) or "—" for k in TAGS] + [str(sum(len(per[lab][k]) for k in TAGS))])
    return rows


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(md_cell(str(c)) for c in r) + " |")
    return "\n".join(out)


def replace_block(text, name, body):
    b, e = f"<!-- GEN:{name}:BEGIN -->", f"<!-- GEN:{name}:END -->"
    pat = re.compile(re.escape(b) + r".*?" + re.escape(e), re.S)
    if not pat.search(text):
        print(f"WARNING: marker {name} not found", file=sys.stderr)
        return text
    return pat.sub(lambda _m: b + "\n\n" + body.strip() + "\n\n" + e, text)


def write_csv(name, header, rows):
    FINAL.mkdir(parents=True, exist_ok=True)
    with open(FINAL / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in rows:
            w.writerow([clean(str(c)) for c in r])


# ----------------------------------------------------------------------------------------------
def main():
    write = "--no-write" not in sys.argv
    parts = load_parts()
    print(f"Scanned {len(parts)} part files: " + ", ".join(p["label"] for p in parts))

    reg_rows, reg_csv = scan_registry(parts)
    tags, tag_dups = build_tag_registers(parts)
    adr_rows, adr_dups = build_adr(parts)
    dec_rows = build_dec(parts)
    id_dups = build_id_dups(parts)
    docmap = build_docmap(parts)

    # CSVs
    write_csv("id_registry.csv", ["Prefix", "Meaning", "Range found", "Distinct IDs", "Owning part", "Defined in (top)", "Parts referencing"], reg_csv)
    names = {"ASSUMPTION": "assumptions", "GAP": "gaps", "CONFLICT": "conflicts", "RECOMMENDATION": "recommendations"}
    for k, recs in tags.items():
        write_csv(f"register_{names[k]}.csv", ["ID", "First seen", "Issuing part", "Statement", "Status / resolution", "Parts referencing", "Occurrences"],
                  [[r["id"], r["first"], r["owner"], r["stmt"], r["status"], r["used"], r["n"]] for r in recs])
    write_csv("adr_index.csv", ["ADR", "Title / decision", "Status", "Part"], adr_rows)
    write_csv("dec_index.csv", ["DEC", "Log", "Subject", "Decision (one line)"], dec_rows)
    all_dups = [["Tag"] + d for d in tag_dups] + [["ADR"] + d for d in adr_dups] + [["Registry"] + d for d in id_dups]
    write_csv("duplicate_ids.csv", ["Kind", "ID", "Part A", "Meaning A", "Part B", "Meaning B", "Similarity"], all_dups)
    write_csv("document_map.csv", ["Part", "File", "Title", "Contents", "Pages", "Diagrams", "Words", "State"], docmap)

    counts = {k: len(v) for k, v in tags.items()}
    print("Counts:", counts, "ADR:", len(adr_rows), "DEC:", len(dec_rows), "dups:", len(tag_dups), len(adr_dups), len(id_dups))
    for k in ("CONFLICT", "RECOMMENDATION"):
        st = defaultdict(int)
        for r in tags[k]:
            st[r["status"].split(" ")[0].split("—")[0].strip()] += 1
        print(k, dict(st))

    if not write or not SELF.exists():
        return
    text = SELF.read_text(encoding="utf-8")
    text, gl_csv = glossary_first_use(parts, text)
    write_csv("glossary.csv", ["Term", "Definition", "First use"], gl_csv)

    text = replace_block(text, "IDREG", md_table(["Prefix", "Meaning", "Actual range found", "Distinct IDs", "Owning part", "Defined in (most rows)", "Parts citing"], reg_rows))
    summary = [[k.title(), counts[k],
                sum(1 for r in tags[k] if r["status"].startswith(("Resolved", "Accepted", "Closed", "Cited"))),
                sum(1 for r in tags[k] if not r["status"].startswith(("Resolved", "Accepted", "Closed", "Cited")))]
               for k in TAGS]
    text = replace_block(text, "TAGSUMMARY", md_table(["Register", "Tags found", "Resolved / accepted / closed / cited by DEC", "Other status"], summary)
                         + f"\n\nADR index: **{len(adr_rows)}** ADRs. DEC index: **{len(dec_rows)}** decisions. Parts scanned: **{len(parts)}** ({parts[0]['label']}–{parts[-1]['label']}).")
    text = replace_block(text, "ALLOC", md_table(["Issuing part", "ASSUMPTION", "GAP", "CONFLICT", "RECOMMENDATION", "Tags"], build_alloc(tags, parts)))
    text = replace_block(text, "ASSUMPTION", md_table(["ID", "First seen", "Statement (from the issuing register, else text near the tag)", "Status"],
                         [[r["id"], r["first"], md_cell(r["stmt"], 260), md_cell(r["status"], 70)] for r in tags["ASSUMPTION"]]))
    text = replace_block(text, "GAP", md_table(["ID", "First seen", "Gap (statement)", "Status / handling"],
                         [[r["id"], r["first"], md_cell(r["stmt"], 260), md_cell(r["status"], 90)] for r in tags["GAP"]]))
    text = replace_block(text, "CONFLICT", md_table(["ID", "First seen", "Conflict (statement)", "Resolution status"],
                         [[r["id"], r["first"], md_cell(r["stmt"], 240), md_cell(r["status"], 110)] for r in tags["CONFLICT"]]))
    text = replace_block(text, "RECOMMENDATION", md_table(["ID", "First seen", "Recommendation (statement)", "Status"],
                         [[r["id"], r["first"], md_cell(r["stmt"], 240), md_cell(r["status"], 70)] for r in tags["RECOMMENDATION"]]))
    text = replace_block(text, "ADR", md_table(["ADR", "Title / decision", "Status", "Part"], [[a, md_cell(b, 150), md_cell(c, 80), d] for a, b, c, d in adr_rows]))
    text = replace_block(text, "DEC", md_table(["DEC", "Log", "Subject", "Decision (one line)"], dec_rows))
    dup_rows = [[k, d[0], d[1], md_cell(d[2], 110), d[3], md_cell(d[4], 110)] for k, d in
                [("Tag", d) for d in tag_dups] + [("ADR", d) for d in adr_dups] + [("Registry", d) for d in id_dups]]
    text = replace_block(text, "DUPS", md_table(["Kind", "ID", "Part A", "Meaning in A", "Part B", "Meaning in B"], dup_rows) if dup_rows else "_No exact-ID duplicates detected by the script._")
    # document map (self row pages are filled after the render; the script is re-run once after rendering)
    docmap = build_docmap(parts)
    text = replace_block(text, "DOCMAP", md_table(["Part", "File", "Title", "Contents (top-level sections)", "Pages", "Diagrams", "Words", "State"], docmap)
                         + f"\n\n**Totals:** {sum(int(r[4]) for r in docmap if r[4].isdigit()):,} pages across {sum(1 for r in docmap if r[4].isdigit())} rendered PDFs; "
                         f"{sum(int(r[5]) for r in docmap)} Mermaid diagrams; {sum(int(r[6].replace(',', '')) for r in docmap):,} words.")
    SELF.write_text(text, encoding="utf-8")
    print("Updated", SELF.name)


if __name__ == "__main__":
    main()
