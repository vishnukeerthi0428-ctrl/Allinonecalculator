#!/usr/bin/env python3
"""Group G: render Part 6.8a (documents, coverage summary, detailed register) and Part 6.8b (catalogue reconciliation
tables) from G_map.json, G_aspects.json and doc22.json. Part 6.8c (enhancements) is authored by hand.

Usage: python3 G_render.py <work_dir>
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(os.path.dirname(HERE)) + "/"
W = sys.argv[1]
M = json.load(open(os.path.join(W, "G_map.json")))
A = json.load(open(os.path.join(W, "G_aspects.json")))
S = {r["id"]: r for r in json.load(open(os.path.join(W, "doc22.json")))["records"]}
rows = M["rows"]


def esc(s):
    return (s or "").replace("|", "/").replace("\n", " ").strip()


def tbl(head, data):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for d in data:
        out.append("| " + " | ".join(esc(str(x)) for x in d) + " |")
    return "\n".join(out)


STL = {"E": "Equivalent", "A": "Alias-equivalent", "P": "Partial + ENH", "N": "New ENH", "M": "Class-mapped", "C": "Conflict"}

# ------------------------------------------------------------------ alias clusters from Part 6.1 §6.1.12.5
p61 = open(BP + "Part-06-1_Test_Strategy.md", encoding="utf-8").read()
seg = p61[p61.index("**SM-UT alias clusters"):p61.index("### 6.1.12.6")]
infer = {}
for line in seg.split("\n"):
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if len(c) < 5 or not re.match(r"^\d{3}", c[0]):
        continue
    ids = []
    for part in c[0].split(","):
        part = part.strip()
        m = re.match(r"(\d{3})\s*[–-]\s*(\d{3})", part)
        if m:
            ids += ["%03d" % i for i in range(int(m.group(1)), int(m.group(2)) + 1)]
        elif re.match(r"\d{3}$", part):
            ids.append(part)
    for i in ids:
        infer["SM-UT-" + i] = c[3]

HDR = """# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 6 (Batch 6.8{suffix}), Source Pack Test Specification Reconciliation{title}

| Field | Value |
|---|---|
| Document | Application Blueprint · Part 6.8{suffix}. {doc} |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | Part 6.1 (test strategy, template §6.1.12.2, alias rules §6.1.12.5, UAT packs §6.1.13.3, EVR §6.1.5.4, severity §6.1.8.2), Batches 6.2–6.5 and 6.7 (2,912 TCs), Part 6.6 RTM and `final/RTM.csv`, Part 3.2 API catalogue (API-001…555, AD-01…20), Part 2.1 module and FR register, DEC-015, DEC-017, DEC-018, DEC-093, DEC-094; source pack documents 19 and 22 (DOCX extractions), document 38 counts |
| Roles applied | QA Lead / Test Architect (primary), UAT Manager, Business Systems Analyst (journey acceptance), Principal Engineer (operation contracts), Security/Compliance Lead (negative fixtures), FinOps Lead (budget and billing cases), Product Owner (sign-off model) |
| Tag ranges used | ASSUMPTION-420…424, GAP-420…425, CONFLICT-420…424, RECOMMENDATION-420…425 (register in Part 6.8c §6.8.8) |
"""


def counts_by_family():
    c = Counter((r["family"], r["status"]) for r in rows)
    fams = ["UT", "UX-UNIT", "SIT-F", "SIT-M", "SIT-A", "UX-SIT", "UAT-F", "UAT-S", "UX-UAT"]
    lvl = {"UT": "Unit", "UX-UNIT": "Unit", "SIT-F": "SIT", "SIT-M": "SIT", "SIT-A": "SIT", "UX-SIT": "SIT",
           "UAT-F": "UAT", "UAT-S": "UAT", "UX-UAT": "UAT"}
    out = []
    for f in fams:
        n = sum(v for (ff, s), v in c.items() if ff == f)
        out.append([f, lvl[f], n, c[(f, "E")], c[(f, "A")], c[(f, "M")], c[(f, "P")], c[(f, "N")]])
    out.append(["**Total**", "", sum(x[2] for x in out), sum(x[3] for x in out), sum(x[4] for x in out),
                sum(x[5] for x in out), sum(x[6] for x in out), sum(x[7] for x in out)])
    return out


# ================================================================== PART 6.8a
a = [HDR.format(suffix="a", title=": Documents, Coverage Summary and Detailed Register",
                doc="Reconciles source documents 19 (Testing, QA and UAT) and 22 (Unit, SIT and UAT Test Case Specification, 799 tests) against Part 6. This file: §6.8.1 documents reviewed, §6.8.2 coverage summary, §6.8.3 detailed coverage register. Part 6.8b holds the catalogue reconciliation (§6.8.4); Part 6.8c holds the new test cases and decisions (§6.8.5–§6.8.9)")]
a.append("""
**Acronyms used in this part.** API application programming interface · BR business requirement · CT contract test · DTO data transfer object · E2E end-to-end · ENH enhancement test case (TC-ENH-G-###) · EVR evidence record · FR functional requirement · IT integration test · OKPI optimization KPI of the source pack (document 38, renamed to avoid the Part 1 KPI collision) · RTM requirements traceability matrix · SIT system integration testing · SYS system test · TC test case · UAT user acceptance testing · UT unit test.

**How to read Part 6.8.** Every one of the 799 source tests has exactly one row in `final/coverage/G_test_mapping.csv` and in the tables of Part 6.8b. The mapping status is one of: **Equivalent** (a blueprint TC asserts the same condition and outcome), **Alias-equivalent** (DEC-017 alias rule maps the source ID to a requirement whose TCs and UAT pack cover it; an execution template TC-ENH-G-036/037 makes the per-screen steps explicit), **Class-mapped** (operation-level SIT contract case mapped to a parameterized operation-contract TC plus the functional TCs of the operation's FR), **Partial + ENH** (blueprint TCs cover the requirement; the missing assertion is written as a TC-ENH-G case in Part 6.8c) and **New ENH** (no equivalent; a new TC-ENH-G case is written). Source IDs are retained as aliases (RECOMMENDATION-423).

**Time-sensitive facts.** Tool names and versions (pytest, Vitest, Playwright, schemathesis, k6, axe-core), provider sandbox behaviour and API limits are design intent: verify at time of implementation (as of 27 Nov 2026).

---

## 6.8.1 Documents reviewed
""")
a.append(tbl(["Item", "Document 19: Testing, Quality Assurance and User Acceptance", "Document 22: Unit, SIT and UAT Test Case Specification"], [
    ["Size (plain-text extraction)", "35,265 bytes; 603 lines; 13 tables", "1,015,801 bytes; 5,670 lines; 45 tables; 799 test records"],
    ["Sections", "Product purpose and boundary; initial startup configurations; technology principles; acceptance and regression test matrix (21 rows); capacity, reliability and recovery acceptance (9 metrics); original commercial module acceptance gates (66); Website/Admin operating contract; cross-interface acceptance; executable test design and gates; exit criteria and traceability; implementation, verification and delivery controls (5 layer gates); evidence record; test execution evidence and blocking rules; optimization engineering (OPT-01-01, 02-01, 05-01, 10-01, 17-01…04, 18-01); implementation acceptance procedures; final decision controls incl. combined preflight; current scope testing strategy (10 scenarios)",
     "§1 purpose and scope (level table); §2 environment and reusable fixtures (11 fixture families); §3 tooling and execution rules and gates; §4 unit catalogue SM-UT-001…066 in 19 groups; §5 SIT end-to-end SM-SIT-F001…F035; §6 commercial module acceptance SM-SIT-M001…M066; §7 SIT operation-level contracts SM-SIT-A001…A302 in 8 audiences; §8 UAT journeys SM-UAT-F001…F017; §9 UAT screen acceptance SM-UAT-S001…S138; §10 defect management and sign-off; execution sign-off; implementation controls with positive/negative/boundary variants for 302 operations and 155 journeys/screens; acceptance and evidence record; SM-CORE-01…04 fixtures; optimization controls; implementation acceptance procedures; current scope: SM-UX-UAT ×147, SM-UX-UNIT ×9, SM-UX-SIT ×9 + X01…X10"],
    ["What it is trying to tell", "The quality contract: what must be proven, at which layer, with which evidence, before any external activation; it is the policy layer above document 22 and repeats the common core",
     "The executable test design: every case with fixture, action and expected result, so that it can be converted to pytest/Playwright and to managed QA execution records; nothing is claimed as executed"],
    ["Pattern", "Common core (product boundary, operating contract, vertical statements, optimization block) + QA policy", "Common core blocks + the full 799-case catalogue (document 38: Unit 75, SIT 422, UAT 302)"],
    ["Atomic aspects found", str(sum(1 for x in A if x["doc"].startswith("19"))), str(sum(1 for x in A if x["doc"].startswith("22"))) + " (799 test records + " + str(sum(1 for x in A if x["doc"].startswith("22")) - 799) + " prose aspects)"],
]))
a.append("""

**Programmatic parsing.** `assembly/source_pack/G_parse_doc22.py` parses every table row and heading block of document 22 into 799 records (ID, level, family, group, title, linked FR/screen/module/method+path, preconditions/setup, steps, expected result, negative and boundary variants, fixture data, inspected entities) and asserts the document 38 totals: **Unit 75 (66 SM-UT + 9 SM-UX-UNIT), SIT 422 (35 SM-SIT-F + 66 SM-SIT-M + 302 SM-SIT-A + 9 SM-UX-SIT screen + 10 SM-UX-SIT-X), UAT 302 (17 SM-UAT-F + 138 SM-UAT-S + 147 SM-UX-UAT)**. The 302 operation cases are asserted per audience group (Authentication 3, Admin 242, Internal adapter 17, Portal 14, Portal + Admin 5, Public 10, Internal worker 3, Provider callback 8). `G_blueprint_index.py` indexes the 2,912 blueprint TCs (through `assembly/build_rtm.py`), `final/RTM.csv`, the 555 Part 3.2 operations and 20 adapters. `G_similarity.py` proposes candidates (TF-IDF); `G_curated.py` holds the reviewed equivalences; `G_map.py` writes the mapping; `G_aspects.py` the coverage register; `G_render.py` the generated tables in this file and Part 6.8b.

---

## 6.8.2 Coverage register summary

### 6.8.2.1 Aspects by status per document
""")
st_order = ["Covered", "Partially covered", "Not covered", "Conflict", "Not applicable", "Common core"]
c = Counter((x["doc"][:2], x["status"]) for x in A)
a.append(tbl(["Document"] + st_order + ["Total"],
             [[d] + [c[(d[:2], s)] for s in st_order] + [sum(c[(d[:2], s)] for s in st_order)] for d in ("19 Testing QA and UAT", "22 Unit SIT UAT catalogue")] +
             [["**Total**"] + [c[("19", s)] + c[("22", s)] for s in st_order] + [len(A)]]))
a.append("""

"Partially covered" for the 302 operation cases means that the blueprint verifies the behaviour through the operation's FR test cases and the generic contract layers CT-03/CT-05 (Part 3.2 §3.2.5), which have no TC IDs; Part 6.8c closes this with the operation-class cases TC-ENH-G-001…017 (GAP-420).

### 6.8.2.2 Source tests by family and mapping status
""")
a.append(tbl(["Family", "Level", "Tests", "Equivalent", "Alias-equivalent", "Class-mapped", "Partial + ENH", "New ENH"], counts_by_family()))
opc = Counter(r["op_match"].split(" (")[0] for r in rows if r["family"] == "SIT-A")
a.append("""

### 6.8.2.3 Headline results

| # | Result | Evidence |
|---|---|---|
| 1 | All 799 source tests are mapped: %d Equivalent, %d Alias-equivalent, %d Class-mapped, %d Partial + ENH, %d New ENH | `final/coverage/G_test_mapping.csv` |
| 2 | 45 new blueprint test cases TC-ENH-G-001…045 written at template depth: 17 parameterized operation-contract classes, 2 parameterized screen templates, 26 specific cases | Part 6.8c §6.8.5.2 |
| 3 | The SM-UAT-S alias rule of Part 6.1 §6.1.12.5 (S001–S030 = W01–W30; S031–S138 = A001–A108) is **confirmed for all 138 rows** by the screen code printed in each source row | §6.8.4.9 |
| 4 | SM-UT-037, -049 and -050 do exist in the source (webhook signature, offering publication, need matching); DEC-094 ("unassigned, no obligation") is superseded | CONFLICT-420 |
| 5 | The inferred SM-UT family labels (ASSUMPTION-180) are replaced by the source titles; coverage stays FR-based | §6.8.4.3 |
| 6 | SM-SIT-M numbers follow document 22's table order: %d of 66 differ from the BRD module number used by BR-M##; mapping is by module name | ASSUMPTION-420; §6.8.4.6 |
| 7 | Operations: %d exact path, %d normalized namespace match, %d nearest, %d consolidated into the Approval resource, %d adapter ports, **%d with no Part 3.2 counterpart** | GAP-421; §6.8.4.7 |
| 8 | Two UAT packs are missing for source journeys (marketing; renewals/customer success) | GAP-422; UAT-PK-MKT, UAT-PK-CS proposed |
""" % (sum(1 for r in rows if r["status"] == "E"), sum(1 for r in rows if r["status"] == "A"),
       sum(1 for r in rows if r["status"] == "M"), sum(1 for r in rows if r["status"] == "P"),
       sum(1 for r in rows if r["status"] == "N"),
       sum(1 for r in rows if r.get("note_num", "").startswith("renumbered")),
       opc["exact"], opc["normalized"], opc["nearest"], opc["consolidated"], opc["adapter port"], opc["no blueprint operation"]))

a.append("""
---

## 6.8.3 Detailed coverage register

Every Not covered, Partial and Conflict aspect is listed individually. Covered test records are listed in Part 6.8b; covered prose aspects are listed here so the register is complete for both documents.

### 6.8.3.1 Document 19 aspects
""")
a.append(tbl(["ID", "Section", "Aspect", "Status", "Blueprint location", "Action", "New IDs"],
             [[x["aspect_id"], x["section"][:40], x["aspect_summary"], x["status"], x["blueprint_location"], x["action"], x["new_ids"]]
              for x in A if x["doc"].startswith("19")]))
a.append("\n\n### 6.8.3.2 Document 22 prose aspects (fixtures, rules, gates, evidence)\n\n")
a.append(tbl(["ID", "Section", "Aspect", "Status", "Blueprint location", "Action", "New IDs"],
             [[x["aspect_id"], x["section"][:30], x["aspect_summary"], x["status"], x["blueprint_location"], x["action"], x["new_ids"]]
              for x in A if x["doc"].startswith("22") and x["aspect_id"].startswith("G22")]))
a.append("\n\n### 6.8.3.3 Document 22 test records that are Partial or New (listed individually)\n\nThe 302 class-mapped operation cases are listed in §6.8.4.7 (all are Partial by definition and closed by TC-ENH-G-001…017).\n\n")
a.append(tbl(["Source test", "Level", "Title", "Gap found", "Blueprint TCs kept", "Added"],
             [[r["source_id"], r["level"], r["title"], r["note"], r["primary_tcs"], r["tc_enh"]]
              for r in rows if r["status"] in ("P", "N")]))
a.append("""

### 6.8.3.4 Source operations with no Part 3.2 catalogue counterpart (GAP-421)

These operations are still fully covered by their operation-class TC and nearest functional TCs (§6.8.4.7). The catalogue gap itself is routed to the API catalogue owner (Part 3.2; source document 07 reconciliation) for an alias row or a candidate operation under DEC-015.

""")
nb = [r for r in rows if r["family"] == "SIT-A" and r["op_match"] == "no blueprint operation"]
a.append(tbl(["Source test", "Method and path", "Purpose", "Class TC", "Functional TCs"],
             [[r["source_id"], r["link"], r["title"][:70], r["tc_enh"], r["primary_tcs"]] for r in nb]))
a.append("""

---

### Quality gate: Part 6.8a

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every aspect row cites its document section and blueprint location |
| 2 | Assumptions/gaps/conflicts tagged and logged | Pass | Tags referenced here are registered in Part 6.8c §6.8.8 |
| 3 | IDs unique and consistent | Pass | G19-/G22- aspect IDs are local to the coverage CSV; TC IDs resolved against the 2,912 defined TCs (script check: 0 undefined) |
| 4 | No requirement lacks a test | Pass | 799/799 source tests mapped |
| 5 | Negative, edge, security, accessibility | Pass | See Part 6.8c |
| 6 | Agents: guardrail, fallback, KPI, cost | N/A | No agents defined in this part |
| 7 | Time-sensitive facts flagged | Pass | Tooling marked verify (as of 27 Nov 2026) |
| 8 | No restricted data to free-tier models | Pass | Not applicable to the register; Part 6.8c cases assert DEC-007 where relevant |
| 9 | Consistent with earlier parts | Pass, with findings | CONFLICT-420…424 and GAP-420…425 (Part 6.8c) |

**Status: Part 6 Batch 6.8a complete. %d aspects registered for documents 19 and 22; every Partial, Not covered and Conflict item listed individually.**
""" % len(A))
open(BP + "Part-06-8a_Source_Pack_Test_Specification_Reconciliation.md", "w", encoding="utf-8").write("\n".join(a))

# ================================================================== PART 6.8b
b = [HDR.format(suffix="b", title=": Catalogue Reconciliation (799 Source Tests → Blueprint TCs)",
                doc="Complete source-test → blueprint-TC mapping for document 22: method, counts, SM-UT alias realignment, and one row per source test for all nine families (§6.8.4). Generated by `assembly/source_pack/G_render.py` from `final/coverage/G_test_mapping.csv`")]
b.append("""
**Acronyms.** See Part 6.8a. ENH = TC-ENH-G-### (Part 6.8c). Status abbreviations: **Eq** Equivalent · **Al** Alias-equivalent · **Cl** Class-mapped · **P+** Partial + ENH · **New** New ENH.

---

## 6.8.4 Catalogue reconciliation

### 6.8.4.1 Method

```mermaid
flowchart TD
  A["Document 22 extraction<br/>5,670 lines"] --> B["G_parse_doc22.py<br/>799 records, counts asserted"]
  C["Blueprint Part 6.2-6.7<br/>2,912 TCs via build_rtm.py"] --> D["G_blueprint_index.py"]
  E["RTM.csv, Part 3.2 API-001-555, AD-01-20"] --> D
  B --> F["G_similarity.py<br/>TF-IDF candidates"]
  D --> F
  F --> G["G_curated.py<br/>reviewed equivalences"]
  B --> H["G_map.py<br/>rules per family"]
  D --> H
  G --> H
  H --> I["G_test_mapping.csv<br/>799 rows"]
  H --> J["G_aspects.py<br/>G_coverage.csv"]
  I --> K["Part 6.8b tables"]
  J --> L["Part 6.8a register"]
```

| Family | Count | Mapping rule |
|---|---|---|
| SM-UT (unit) | 66 | Hand-reviewed against TF-IDF candidates; equivalence requires the same condition and the same expected outcome |
| SM-UX-UNIT | 9 | FR of the screen (W31–W34, A109–A113) → RTM TCs at level UT/CT ranked by similarity |
| SM-SIT-F (end-to-end) | 35 | Hand-reviewed; journey TCs TC-21-054…064 preferred |
| SM-SIT-M (module gates) | 66 | Module **name** → BR-M## (ASSUMPTION-420) → RTM TCs; best gate TC by similarity to the gate text; overrides where the gate needs an added assertion |
| SM-SIT-A (operations) | 302 | Method + path → Part 3.2 operation (exact, namespace-normalized, nearest with last-segment containment and Jaccard ≥ 0.5 [ASSUMPTION-422], or Approval consolidation) → FR → RTM TCs; adapters → AD-##; negative-fixture sentence → operation class TC-ENH-G-001…017 |
| SM-UX-SIT (screen + X) | 19 | Screens: FR → TCs at IT/SYS/E2E; X01…X10 hand-reviewed |
| SM-UAT-F (journeys) | 17 | Hand-reviewed to UAT packs (Part 6.1 §6.1.13.3) and E2E journeys |
| SM-UAT-S (screens) | 138 | DEC-017 alias rule, verified against the screen code in each row → FR → TCs at E2E/UAT/SYS; UAT pack by epic; template TC-ENH-G-036 |
| SM-UX-UAT | 147 | Screen → FR / FR-UX-<screen>; TCs that already cite the alias (Part 6.2–6.5) first; template TC-ENH-G-037 |

### 6.8.4.2 Counts
""")
b.append(tbl(["Family", "Level", "Tests", "Equivalent", "Alias-equivalent", "Class-mapped", "Partial + ENH", "New ENH"], counts_by_family()))
b.append("\n\nOperation match results (302 SIT operation cases):\n\n")
b.append(tbl(["Match type", "Count", "Meaning"], [
    ["exact", opc["exact"], "Same method and identical path (FRD-named ★ operations, DEC-015)"],
    ["normalized", opc["normalized"], "Same method; path equal after removing `/api/v1`, `/commercial`, `/workspace` and namespace prefixes, with the namespace compatible (admin ↔ admin; portal/public ↔ portal/public)"],
    ["nearest", opc["nearest"], "Same method and namespace; last path segment contained; token Jaccard ≥ 0.5 (ASSUMPTION-422: to be confirmed by the API owner)"],
    ["consolidated", opc["consolidated"], "Per-object approve/review/decide merged into the Approval resource API-541 (Part 3.2 §3.2.2.1 step 4)"],
    ["adapter port", opc["adapter port"], "Internal adapter contract → AD-## (Part 3.2 §3.2.4)"],
    ["no blueprint operation", opc["no blueprint operation"], "GAP-421; still covered by class TC and nearest functional TCs"],
]))

# alias realignment
b.append("""

### 6.8.4.3 SM-UT alias realignment (supersedes the inferred family labels of ASSUMPTION-180)

Part 6.1 inferred a "control family" for each SM-UT ID from the FRD co-occurrence pattern. Document 22 now gives each ID its actual unit under test. The table keeps the inferred label for traceability and records the source meaning that governs from now on (CONFLICT-420 for 037/049/050). Coverage in the RTM stays FR-based, so no existing coverage figure changes; the equivalent TCs below are added to the alias column.

""")
b.append(tbl(["Alias", "Source unit under test (doc 22 §4)", "Part 6.1 inferred family", "Status", "Equivalent blueprint TCs", "ENH"],
             [[r["source_id"], S[r["source_id"]]["group"] + ": " + r["title"], infer.get(r["source_id"], "— (DEC-094: unassigned)"),
               STL[r["status"]], r["primary_tcs"], r["tc_enh"]] for r in rows if r["family"] == "UT"]))


def fam_table(fam, head, fn):
    return tbl(head, [fn(r) for r in rows if r["family"] == fam])


b.append("\n\n### 6.8.4.4 Unit: SM-UX-UNIT (9)\n\n")
b.append(fam_table("UX-UNIT", ["Source test", "Screen", "Expected (source)", "FR", "Status", "Blueprint TCs (UT/CT)"],
                   lambda r: [r["source_id"], r["link"], S[r["source_id"]]["expected"][:90], r["bp_requirement"], STL[r["status"]], r["primary_tcs"]]))
b.append("\n\n### 6.8.4.5 SIT end-to-end SM-SIT-F (35), SM-UX-SIT screens (9) and cross-cutting X01…X10 (10)\n\n")
b.append(fam_table("SIT-F", ["Source test", "Title", "Expected (source)", "Status", "Blueprint TCs", "ENH"],
                   lambda r: [r["source_id"], r["title"], S[r["source_id"]]["expected"][:110], STL[r["status"]], r["primary_tcs"], r["tc_enh"]]))
b.append("\n\n")
b.append(fam_table("UX-SIT", ["Source test", "Title", "Expected (source)", "Status", "Blueprint TCs", "ENH"],
                   lambda r: [r["source_id"], r["title"][:60], S[r["source_id"]]["expected"][:110], STL[r["status"]], r["primary_tcs"], r["tc_enh"]]))
b.append("""

### 6.8.4.6 SIT module acceptance SM-SIT-M (66)

The source numbers modules in its own table order. For 50 modules the number differs from the BRD module number used by BR-M## (for example SM-SIT-M009 "Cost and usage control" = BR-M53, SM-SIT-M013 "Search query planner" = BR-M10). Mapping is by module name (ASSUMPTION-420); the alias column of the RTM must carry both numbers.

""")
b.append(fam_table("SIT-M", ["Source test", "Module", "Expected business gate (source)", "BR (renumbering)", "Status", "Gate TCs", "ENH"],
                   lambda r: [r["source_id"], r["title"], S[r["source_id"]]["expected"], r["bp_requirement"].split(" (")[0] + (" · " + r["note_num"] if r.get("note_num", "").startswith("renum") else ""),
                              STL[r["status"]], r["primary_tcs"], r["tc_enh"]]))
b.append("""

### 6.8.4.7 SIT operation-level contracts SM-SIT-A (302)

Class key (Part 6.8c §6.8.5.2.1): G-001 audience/auth · G-002 scoped list/read · G-003 revisioned or idempotent write · G-004 hash-bound approval · G-005 publication snapshot · G-006 AI evidence/output · G-007 discovery source and cap · G-008 messaging eligibility and dispatch · G-009 portal object grant · G-010 workflow simulation · G-011 financial allocation · G-012 self-service/privacy request · G-013 fulfilment quantity · G-014 bid deadline · G-015 adapter port · G-016 provider callback · G-017 health/readiness.

""")
b.append(fam_table("SIT-A", ["Source test", "Audience", "Method and path", "Blueprint operation", "Match", "FR", "Class TC", "Functional TCs"],
                   lambda r: [r["source_id"], r["group"].split(" (")[0], r["link"], r["bp_operation"], r["op_match"].split(" (")[0],
                              r["bp_requirement"], r["tc_enh"].replace("TC-ENH-", ""), r["primary_tcs"]]))
b.append("\n\n### 6.8.4.8 UAT business journeys SM-UAT-F (17)\n\n")
b.append(fam_table("UAT-F", ["Source test", "Journey", "Acceptance user", "Business acceptance (source)", "UAT pack", "Status", "Blueprint TCs", "ENH"],
                   lambda r: [r["source_id"], r["title"], S[r["source_id"]]["pre"], S[r["source_id"]]["expected"][:120], r["uat_pack"], STL[r["status"]], r["primary_tcs"], r["tc_enh"]]))
b.append("\n\n### 6.8.4.9 UAT screen acceptance SM-UAT-S (138)\n\nAlias rule check: the screen code printed in every source row equals the FR given by the Part 6.1 rule (138/138). Execution template: TC-ENH-G-036.\n\n")
b.append(fam_table("UAT-S", ["Source test", "Screen", "Title", "Alias FR", "UAT pack", "Blueprint TCs (E2E/UAT/SYS)", "FR TC count"],
                   lambda r: [r["source_id"], r["link"], r["title"], r["bp_requirement"], r["uat_pack"], r["primary_tcs"], r["supporting_tcs"].split(" TCs")[0]]))
b.append("\n\n### 6.8.4.10 Field and journey acceptance SM-UX-UAT (147)\n\nExecution template: TC-ENH-G-037. \"Cites\" counts blueprint TCs that already carry the SM-UX-UAT alias.\n\n")
b.append(fam_table("UX-UAT", ["Source test", "Screen", "Exercise (source)", "Requirement", "Blueprint TCs", "Cites / FR TCs", "UAT pack"],
                   lambda r: [r["source_id"], r["link"], S[r["source_id"]]["steps"].split("exercise ")[-1][:80], r["bp_requirement"], r["primary_tcs"],
                              re.sub(r"(\d+) TCs cite \S+; (\d+) TCs on \S+", r"\1 / \2", r["supporting_tcs"]), r["uat_pack"]]))
b.append("""

---

### Quality gate: Part 6.8b

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Each row cites the source ID; each blueprint TC is a defined ID (script check) |
| 2 | Tags logged | Pass | ASSUMPTION-420, -422; GAP-421; CONFLICT-420 (register in Part 6.8c) |
| 3 | IDs unique and consistent | Pass | 799 unique source IDs; TC IDs resolved against Parts 6.2–6.7 |
| 4 | No requirement lacks a test | Pass | 799/799 rows carry at least one blueprint TC or TC-ENH-G |
| 5 | Negative, edge, security, accessibility | Pass | Negative fixture class recorded per operation |
| 6 | Agents | N/A | — |
| 7 | Time-sensitive facts | Pass | No prices or provider limits stated here |
| 8 | No restricted data to free-tier models | N/A | — |
| 9 | Consistent with earlier parts | Pass, with findings | Module renumbering and catalogue gaps reported, not fixed |

**Status: Part 6 Batch 6.8b complete. 799 source tests mapped one-to-one: %s.**
""" % ", ".join("%s %d" % (STL[k], v) for k, v in sorted(Counter(r["status"] for r in rows).items())))
open(BP + "Part-06-8b_Source_Pack_Test_Specification_Reconciliation.md", "w", encoding="utf-8").write("\n".join(b))
print("written a, b")
