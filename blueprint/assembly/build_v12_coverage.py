#!/usr/bin/env python3
"""Part 11.0: V12 customer-revision coverage report, generated from final/coverage_v12/*.csv.

Applies the Founder decisions recorded in Part 11.14 (resolved conflicts) as an overlay, and lists the
conflicts still pending. Usage: python3 blueprint/assembly/build_v12_coverage.py
"""
import collections
import csv
import re
from pathlib import Path

BP = Path(__file__).resolve().parent.parent
COV = BP / "final" / "coverage_v12"
OUT = BP / "Part-11-0_V12_Coverage_Report.md"

GROUPS = {
    "A": ("BRD business chapters 00–07, 10–25", "Part 11.1a/b"),
    "B": ("39 services: BRD 08, FSD 08/11, catalogue workbook", "Part 11.2a–c"),
    "C": ("Workflows SM-SVC-01…20 (FSD 12, Appendix B)", "Part 11.3a–c"),
    "D": ("Workflows SM-SVC-21…39, step/trigger/event registry, scheduler, DTOs", "Part 11.4a–d"),
    "E": ("Platform architecture: tenancy, identity, provisioning, subscription, billing, infra, release", "Part 11.5a/b"),
    "F": ("AI engines, agent registry, models, prompts, evaluation, RAG, HITL, AI cost", "Part 11.6a/b"),
    "G": ("Website, tenant portal, operator admin, portfolio, UI master, 4 HTML prototypes", "Part 11.7a–c"),
    "H": ("REST API, OpenAPI A/A2, events, integrations, plugins", "Part 11.8a/b"),
    "I": ("Database schema, DDL/RLS (Appendix C/C2), security, privacy, analytics, KPIs", "Part 11.9a–c"),
    "J": ("Unit/SIT/UAT/AI tests, QC, coding standards, backlog", "Part 11.10a–c"),
    "K": ("Observability, incidents, support, master traceability, customer decision register", "Part 11.11a/b"),
    "L": ("Historical annex (V1), embedded source archive (11 files, 248 files expanded)", "Part 11.12"),
    "M": ("AI improvement panel: new agents, automations, workflows", "Part 11.13a/b"),
}

# Founder decisions of 28 Nov 2026 (Part 11.14): conflicts and pending decisions they resolve
RESOLVED = {
    "CONFLICT-922": "DEC-770", "DEC-686": "DEC-770",
    "CONFLICT-923": "DEC-771", "CONFLICT-765": "DEC-771", "DEC-687": "DEC-771",
    "CONFLICT-924": "DEC-772", "CONFLICT-761": "DEC-772", "CONFLICT-832": "DEC-772", "CONFLICT-852": "DEC-772", "DEC-688": "DEC-772", "DEC-678": "DEC-772",
    "CONFLICT-943": "DEC-773", "CONFLICT-905": "DEC-773", "DEC-715": "DEC-773", "DEC-679": "DEC-773",
    "CONFLICT-944": "DEC-774", "DEC-716": "DEC-774",
    "CONFLICT-945": "DEC-775", "CONFLICT-856": "DEC-775", "CONFLICT-874": "DEC-775", "DEC-717": "DEC-775",
    "CONFLICT-946": "DEC-776", "CONFLICT-835": "DEC-776", "DEC-718": "DEC-776", "DEC-596": "DEC-776",
    "CONFLICT-947": "DEC-777", "DEC-719": "DEC-777",
    # Founder decisions DEC-779…791 ("go with V12 for all pending items")
    **{f"CONFLICT-{n}": "DEC-779" for n in (762, 798, 799, 814, 854)},
    **{"DEC-548": "DEC-779", "DEC-549": "DEC-779", "DEC-562": "DEC-779", "DEC-572": "DEC-779"},
    "CONFLICT-778": "DEC-780",
    "CONFLICT-800": "DEC-781", "CONFLICT-781": "DEC-781",
    "CONFLICT-779": "DEC-782", "CONFLICT-815": "DEC-782",
    "CONFLICT-958": "DEC-783", "CONFLICT-868": "DEC-783", "DEC-517": "DEC-783",
    "CONFLICT-760": "DEC-784", "CONFLICT-834": "DEC-784", "CONFLICT-887": "DEC-784", "DEC-597": "DEC-784", "DEC-644": "DEC-784",
    "CONFLICT-886": "DEC-785", "CONFLICT-888": "DEC-785", "CONFLICT-776": "DEC-785",
    "CONFLICT-889": "DEC-786",
    "CONFLICT-833": "DEC-787",
    **{f"CONFLICT-{n}": "DEC-788" for n in (850, 851, 853, 855, 857, 819)},
    "CONFLICT-983": "DEC-789",
    **{f"CONFLICT-{n}": "DEC-790" for n in (780, 869, 552, 657, 462, 113)},
}
# DEC-791: every other row still marked pending is adopted as V12 specifies
CATCH_ALL = "DEC-791"


def main():
    rows = []
    for g in GROUPS:
        f = COV / f"{g}_coverage.csv"
        if f.exists():
            for r in csv.DictReader(f.open(encoding="utf-8")):
                r["group"] = g
                rows.append(r)
    before = collections.defaultdict(collections.Counter)
    after = collections.defaultdict(collections.Counter)
    unresolved = collections.Counter()
    resolved_by = collections.Counter()
    for r in rows:
        g = r["group"]
        sb = (r.get("status_before") or "").split(" (")[0].strip() or "Unstated"
        sa = (r.get("status_after") or "").strip()
        before[g][sb] += 1
        if sa.lower().startswith("pending"):
            refs = set(re.findall(r"CONFLICT-\d{3}|DEC-\d{3}", " ".join(str(v) for v in r.values())))
            hit = [RESOLVED[x] for x in refs if x in RESOLVED]
            open_conf = [x for x in refs if x.startswith("CONFLICT-") and x not in RESOLVED]
            if not hit or open_conf:
                hit = hit + [CATCH_ALL]
                open_conf = []
            if hit and not open_conf:
                after[g]["Matched (Founder decision)"] += 1
                for h in set(hit):
                    resolved_by[h] += 1
                continue
            after[g]["Pending Founder decision"] += 1
            for x in open_conf or ["(no conflict ID)"]:
                unresolved[x] += 1
        elif sa.lower().startswith("not applicable"):
            after[g]["Not applicable"] += 1
        elif sa.lower().startswith("matched"):
            after[g]["Matched"] += 1
        else:
            after[g]["Cross-reference row"] += 1

    # conflict descriptions from the parts
    desc = {}
    for p in sorted(BP.glob("Part-11-*.md")):
        for ln in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\|\s*\**(CONFLICT-\d{3})\**\s*\|\s*([^|]+)\|", ln)
            if m and m.group(1) not in desc:
                desc[m.group(1)] = (re.sub(r"\*\*", "", m.group(2)).strip()[:160], p.name.split("_")[0].replace("Part-", "Part ").replace("-", "."))

    L = []
    A = L.append
    A("# AI Growth Engine: Employee Sales & Marketing Automation")
    A("## Application Blueprint: PART 11 (Batch 11.0), Customer Revision V12: Coverage Report")
    A("")
    A("| Field | Value |\n|---|---|\n| Document | Part 11.0, generated by `assembly/build_v12_coverage.py` from the 13 review registers in `final/coverage_v12/` |\n| Version | 1.1 · 28 Nov 2026 (DEC-779…791 overlay) |\n| Input | Customer revision of 28 Nov 2026: BRD V12, FSD V12 (40 chapters + Appendices A, A2, B, C, C2, D), 4 HTML prototypes (website and Admin, desktop and mobile), the V1 historical annexes and the FSD's embedded source archive (11 files) |\n| Method | Every line read by 13 expert review groups; catalogue-scale material (156 workflows, 517 steps, 330 OpenAPI operations, 137 DDL tables, 6,000+ test rows, 1,912 traceability rows) parsed row by row with scripts in `assembly/v12/` |")
    A("")
    A("## 11.0.1 What the revision is\n")
    A("V12 is a new, much larger specification of the same product. Only about 3% of the BRD's and 11% of the FSD's normative text overlaps with the original 38-document pack. It turns the platform into a SaaS catalogue of **39 automation services (SM-SVC-01…39), each with four executable workflows (156 workflows, `SM-SVC-##-WF#`)**, sold per service through a subscription, bundle and entitlement engine, with billing and metering, a service registry, platform operator administration and an authorized portfolio command centre. It adds voice and telephony, SMS/RCS, agentic commerce, marketplace and procurement services, enterprise readiness (SSO/SCIM, SLA tiers, certifications, 24×7 operations), India/EU residency and global expansion. The historical annexes are the V1 baseline, declared non-normative; the embedded archive includes the original 38 documents (byte-identical to the pack already covered) and a separate \"Investment Automation\" product.\n")
    A("## 11.0.2 Coverage by review group\n")
    A("| Group | Material | Part | Aspects | Covered before | Partial before | Not covered before | Conflict before | Matched after | Matched by Founder decision | Pending Founder | Not applicable |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    T = collections.Counter()
    for g, (mat, part) in GROUPS.items():
        b, a = before[g], after[g]
        n = sum(b.values())
        vals = [n, b["Covered"], b["Partially covered"], b["Not covered"], b["Conflict"], a["Matched"], a["Matched (Founder decision)"], a["Pending Founder decision"], a["Not applicable"]]
        for k, v in zip(["n", "cov", "par", "not", "con", "m", "mf", "p", "na"], vals):
            T[k] += v
        A(f"| {g} | {mat} | {part} | " + " | ".join(f"{v:,}" for v in vals) + " |")
    A("| **Total** | | | " + " | ".join(f"**{T[k]:,}**" for k in ["n", "cov", "par", "not", "con", "m", "mf", "p", "na"]) + " |")
    A("")
    appl = T["n"] - T["na"] - sum(after[g]["Cross-reference row"] for g in GROUPS)
    inv = unresolved.get("CONFLICT-958", 0) + unresolved.get("CONFLICT-868", 0)
    A("Group L's \"Not applicable\" rows are V1/archive statements that V12 supersedes (each with its V12 citation) or that are out of scope. Group L's investor/fundraising rows (the Investment Automation product, formerly CONFLICT-958) are matched by DEC-783 and specified in Part 11.16.\n")
    A("## 11.0.3 Overall result\n")
    A(f"| Measure | Value |\n|---|---|\n| Aspects reviewed | {T['n']:,} |\n| Applicable aspects | {appl:,} |\n| Matched (V12 adopted literally, or already equivalent) | {T['m']:,} |\n| Matched by the Founder decisions of 28 Nov 2026 (DEC-770…791) | {T['mf']:,} |\n| **Literal match with V12** | **{(T['m'] + T['mf']) / appl * 100:.2f}%** ({T['m'] + T['mf']:,} / {appl:,}) |\n| Pending a Founder decision | {T['p']:,} |\n")
    A("Every applicable aspect is matched: either V12 is adopted literally, or a Founder decision of 28 Nov 2026 adopts it (DEC-779…791 adopted V12 on every item that was pending, including the investor/fundraising product, DEC-783). Each adopted capability is specified in Parts 11.15–11.19 with V12's own conditions and legal gates.\n")
    A("## 11.0.4 Founder decisions applied as an overlay\n")
    A("| Decision | Rows matched |\n|---|---|")
    for k, v in sorted(resolved_by.items()):
        A(f"| {k} | {v:,} |")
    A("")
    A("## 11.0.5 Conflicts still pending a Founder decision\n")
    if not unresolved:
        A("None. All conflicts raised by the review groups are resolved by Founder decisions DEC-770…791 (Part 11.14).\n")
    A("| Conflict | Subject | Raised in | Aspect rows |\n|---|---|---|---|") if unresolved else None
    for k, v in sorted(unresolved.items(), key=lambda x: (-x[1], x[0])):
        d, part = desc.get(k, ("See the raising part", "—"))
        A(f"| {k} | {d.replace('|', '/')} | {part} | {v:,} |")
    A("")
    if unresolved:
        A("Part 11.14 §11.14.2 groups these into the decisions the Founder needs to take, with the expert recommendation for each.\n")
    A("## 11.0.6 Registers\n")
    A("The aspect-level registers (one row per aspect, with blueprint location, action, new IDs and status before/after) are `final/coverage_v12/A_coverage.csv` … `M_coverage.csv`; the parsing scripts are in `assembly/v12/`.\n")
    A("**Status: Part 11 Batch 11.0 complete.**")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(OUT, dict(T), "applicable", appl, "resolved_by", dict(resolved_by), "open", len(unresolved))


if __name__ == "__main__":
    main()
