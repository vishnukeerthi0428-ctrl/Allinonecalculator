#!/usr/bin/env python3
"""Builds the computed Markdown fragments of Part 11.20 from s_master_plan.py and
substitutes them into the hand-written templates s_part_a.tmpl.md / s_part_b.tmpl.md.

Run from blueprint/assembly/v12b:  python3 -I s_fragments.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s_master_plan as M  # noqa: E402

BP = os.path.abspath(os.path.join(HERE, "..", ".."))
RC, RL, RH = M.run(1), M.run(0), M.run(2)

REL_LABEL = {"R0": "R0 Foundation", "R1": "R1 Core + enterprise identity + developer platform",
             "R2A": "R2-A Full V12 service catalogue", "R2B": "R2-B Consequential capabilities (mandates, commerce, bids, voice)",
             "R3": "R3 EU region + SOC 2 Type II + ISO 27001", "R4": "R4 Global + ISO 27701/42001",
             "INV1": "INV-R1 Investment Automation I", "INV2": "INV-R2 Investment Automation II",
             "A1": "A1 Advanced foundations", "A2": "A2 Growth intelligence", "A3": "A3 Scale", "A4": "A4 AI improvement",
             "Sustain": "Sustain, hypercare and gate windows"}
RATE = (4545, 5682, 6818)


def f1(t):
    return " / ".join("%.0f" % x for x in t)


def d(k):
    e = M.gdate(k)
    return "%s (Day %d)" % (M.fmt(e), M.day(e))


def frag_rollup_group():
    o = ["| Group | Source part and change request | Gross pd L / C / H | Overlap removed L / C / H | Net L / C / H | Absorbed at refinement L / C / H | **Plan pd L / C / H** | Plan value ₹ L (low × ₹4,545 / central × ₹5,682 / high × ₹6,818) |",
         "|---|---|---|---|---|---|---|---|"]
    tot = [[0.0] * 3 for _ in range(5)]
    for g, v in M.NET.items():
        val = " / ".join("%.2f" % (v["plan"][i] * RATE[i] / 1e5) for i in range(3))
        o.append("| %s | %s | %s | %s | %s | %s | **%s** | %s |" % (g, M.GROSS[g][0], f1(v["gross"]), f1(v["removed"]), f1(v["net"]),
                                                                  " / ".join("%.1f" % x for x in v["absorbed"]), f1(v["plan"]), val))
        for j, key in enumerate(("gross", "removed", "net", "absorbed", "plan")):
            for i in range(3):
                tot[j][i] += v[key][i]
    val = " / ".join("%.2f" % (tot[4][i] * RATE[i] / 1e5) for i in range(3))
    o.append("| **Total** | | **%s** | **%s** | **%s** | **%s** | **%s** | **%s** |" % (f1(tot[0]), f1(tot[1]), f1(tot[2]), f1(tot[3]), f1(tot[4]), val))
    return "\n".join(o)


CAP = [
    ("C01", "Core growth engine, Release 1/2 baseline (Parts 0–9.5)", ["BASE"]),
    ("C02", "Literal alignment (V11, CR-ALN-01)", ["ALN"]),
    ("C03", "Service catalogue, 156 workflows, SKU build (39 SKUs)", ["A", "B", "C", "D", "J"]),
    ("C04", "Platform architecture, tenancy, billing and tax", ["E"]),
    ("C05", "AI engines, model registry, evaluation (111 suites)", ["F"]),
    ("C06", "Website, portal, Command Centre UX, i18n/RTL", ["G"]),
    ("C07", "Enterprise identity, developer platform, connectors, Vercel, RPO, DB roles", ["H", "R"]),
    ("C08", "Data, security, observability, SLA, traceability", ["I", "K", "L"]),
    ("C09", "Bounded mandates, agentic commerce, payments, automatic bids", ["P"]),
    ("C10", "AI voice calling and recordings", ["Q"]),
    ("C11", "Investment Automation INV-SVC-01…24", ["N", "O"]),
    ("C12", "Enterprise operations, certification, EU and global regions", ["ENT"]),
    ("C13", "Advanced intelligence A1–A4 (X1–X3 + AI improvement)", ["ADV", "M"]),
]


def frag_rollup_cap():
    o = ["| Cap. | Capability | Groups | Plan pd L / C / H | Share of central | Value ₹ L L / C / H |", "|---|---|---|---|---|---|"]
    tot = [0, 0, 0]
    for cid, nm, gs in CAP:
        v = [sum(M.NET[g]["plan"][i] for g in gs) for i in range(3)]
        for i in range(3):
            tot[i] += v[i]
        o.append("| %s | %s | %s | %s | %.1f%% | %s |" % (cid, nm, ", ".join(gs), f1(v), 100 * v[1] / 6374.455,
                                                         " / ".join("%.2f" % (v[i] * RATE[i] / 1e5) for i in range(3))))
    o.append("| | **Total** | | **%s** | 100%% | **%s** |" % (f1(tot), " / ".join("%.2f" % (tot[i] * RATE[i] / 1e5) for i in range(3))))
    return "\n".join(o)


def frag_overlap():
    o = ["| # | Removed from | Capability built twice (as the parts report it) | Owner kept (single-owner rule) | Removed pd L / C / H |", "|---|---|---|---|---|"]
    t = [0, 0, 0]
    for oid, g, what, owner, v in M.OVL:
        o.append("| %s | %s (%s) | %s | %s | %s |" % (oid, g, M.GROSS[g][0].split(" ")[0], what, owner, " / ".join("%.2f" % x if x % 1 else "%.0f" % x for x in v)))
        for i in range(3):
            t[i] += v[i]
    o.append("| | | **Total removed** | | **%s** |" % " / ".join("%.1f" % x for x in t))
    return "\n".join(o)


def frag_pkg():
    o = ["| Package | Release | Content | Plan pd L / C / H | Value ₹ L L / C / H | Squads (queue order) | Earliest start | Build complete (central) |", "|---|---|---|---|---|---|---|---|"]
    for p, v in M.PKG.items():
        rel = M.rel_of(p)
        sqs = ", ".join(s[0] for s in M.SQUADS if p in s[4])
        es = M.EARLIEST0.get(p)
        es_txt = "S%d" % es if es is not None else {"A1": "R2-A gate − 2 sprints (DEC-417)", "A2": "A1 build + 1", "A3": "A2 build + 1",
                                                     "A4": "A3 build + 1", "R4": "R3 build + 1"}.get(p, "—")
        o.append("| %s | %s | %s | %s | %s | %s | %s | S%d %s |" % (p, rel, M.PKG_NAMES[p], f1(v), " / ".join("%.2f" % (v[i] * RATE[i] / 1e5) for i in range(3)),
                                                              sqs, es_txt, RC["done"][p], M.fmt(M.gdate(RC["done"][p]))))
    return "\n".join(o)


def frag_gates():
    o = ["| Release | Workload pd L / C / H | Build complete (central) | **Gate of record (central)** | Low-effort gate | High-effort gate | Hardening sprints |", "|---|---|---|---|---|---|---|"]
    for rel, pk in M.REL_PKGS.items():
        v = [sum(M.PKG[p][i] for p in pk) for i in range(3)]
        o.append("| %s | %s | S%d %s | **S%d %s** | S%d %s | S%d %s | %d |" % (
            REL_LABEL[rel], f1(v), RC["build"][rel], M.fmt(M.gdate(RC["build"][rel])), RC["gates"][rel], d(RC["gates"][rel]),
            RL["gates"][rel], d(RL["gates"][rel]), RH["gates"][rel], d(RH["gates"][rel]), M.HARDEN[rel]))
    return "\n".join(o)


GOALS = {
    0: ("R0 W0-A foundation plus the V12 platform corrections: IaC for four environments, identity spike with check 13 (Okta, Entra ID, Google through the broker), CI gates, RLS, outbox, audit, flags, deny-by-default PDP, catalogue core; `app_rw` least-privilege role and Data API off (DEC-778); Vercel projects `web-in`, `admin-in`, `developers`", "—"),
    1: ("W0-B control set: BFF sign-in, integration registry, consent and suppression, model gateway, evaluation harness, hard cost caps, Command Centre shell; PITR on with `recovery_path` (DEC-787); registry seed rows; DDL-V12-R-01…04", "Gate W0-B control set Tue 5 Jan 2027 (Day 30)"),
    2: ("W0-B completion and discovery core: MFA step-up, claims approval, readiness gate, tier routing, injection guard, source register to signals board; first measured AI-built throughput", "**DEC-420 calibration gate: S2 review Fri 15 Jan 2027 (Day 40); decision by Thu 21 Jan 2027 (Day 46)**"),
    3: ("Close R0; start R1: SQ-02 onboarded (DEC-228 contract engineers); W1 qualification; SSO broker spike follow-up; standby + WAL-G design", "**R0 gate Fri 29 Jan 2027 (Day 54)**"),
    4: ("SQ-03 starts enterprise identity: SSO configuration and test login (US-01-ZR01), OAuth client credentials (US-20-ZR07); W0 admin tail, W1 imports, opt-out pages, SES adapter", "Staff-augmentation wave 2 onboarding"),
    5: ("SQ-04 starts AI platform: registry gates AU-150…153, prompt registry, scoped consent ledger AU-172; webhook engine (US-20-ZR08); connector framework and gate (US-18-ZR11); W2 engagement core", "—"),
    6: ("SCIM 2.0 (US-01-ZR03); SMS-DLT and Zoho CRM; first restore drill (RPO ≤ 15 min, RTO ≤ 120 min); EVAL-PRG-1 suites; W2 outreach and meetings", "First restore drill"),
    7: ("SQ-05 starts: tenancy re-model and portfolio grants, hierarchy, common workflow engine (D-1), catalogue registry (E9); custom roles and SoD (US-01-ZR04); HubSpot; website publication pipeline", "—"),
    8: ("IP sprint PI-1: PI-2 planning, hardening, DR drill; SIEM and audit export (US-01-ZR05); SDK 1.0 RC; i18n framework and pseudo-locale CI", "PI-2 planning Thu–Fri 8–9 Apr 2027"),
    9: ("SQ-06 starts; QA infrastructure TASK-V12-J-001…014 and first H-class SKUs; W3 omnichannel; Salesforce adapter; voice transport connector (US-22-ZR15)", "—"),
    10: ("W3 marketing close-out; Command Centre 14 views; SLA, SEV clocks and status page (K); regional Vercel and header allowlist (US-21-ZR16/17); pen-test vendor confirmed", "India marketing packs to counsel (RP-IN-*)"),
    11: ("SQ-07 starts mandate engine core (MND), two-person approval; R1 commercial core (W4 pricing, quotes); evaluation suites for R1 agents", "—"),
    12: ("SQ-08 starts voice gateway and ports; R1 scope freeze (start of S12, Day 169); R1 V12 core completion; W4 closure baseline (R2-A) starts", "R1 scope freeze Mon 24 May 2027"),
    13: ("R1 build complete: residency choice at onboarding (US-01-ZR28), DLT live, India pack approved, VD-01…12 green for 30 days; UAT and pen test 1 (incl. SSO, SCIM, developer host, webhooks)", "R1 build complete Fri 18 Jun 2027"),
    14: ("IP sprint PI-2 and R1 hardening: go/no-go evidence (GNG-R-01…10), restore drill at the gate, PI-3 planning; catalogue H-class SKUs continue", "**R1 go/no-go Fri 2 Jul 2027 (Day 208)**"),
    15: ("R1 hypercare; R2-A catalogue H-class SKUs at full flow; W4 closure (proposal, bids, orders, payments evidence); mandate PDP rules 0–14 and ledger", "R1 hypercare (4 weeks)"),
    16: ("SQ-09 starts Investment Automation boundary (`inv` schema, AU-200, R21/R10C); M-class SKUs; PSP adapters design; voice ASR/TTS ports", "INV counsel engagement opened (IN first)"),
    17: ("Catalogue M-class SKUs and billing (E14–E18); INV storefront W55–W74 and AU-228; voice agents AG-210…219; negotiation bound engine", "—"),
    18: ("SQ-10 starts R2-A enterprise operations (24×7 runbooks, NOC/SOC onboarding, 99.95% topology ADR) and the R3 EU stack (IaC second stamp, residency router); N-class SKUs", "NOC/SOC vendor contract signed"),
    19: ("SOC 2 readiness assessment; N-class SKUs; payments settlement sub-ledger; bid sealing and portal adapters; INV-SVC-01…03", "—"),
    20: ("IP sprint PI-3: PI-4 planning, DR drill, R2-A UAT preparation; catalogue completion", "PI-4 planning"),
    21: ("R2-A build complete (Fri 8 Oct 2027): 39 SKUs, 156 workflows, billing, screens; SQ-11 starts A1 (DEC-417); R2-A UAT; SOC 2 Type I fieldwork", "R2-A build complete"),
    22: ("R2-A hardening: pen test 2, 24×7 go-live rehearsal and paging test, Enterprise-tier failover test; R3 EU stack; A1 build; INV-SVC-04…08", "—"),
    23: ("R3 EU build complete; INV-R2 build (INV-SVC-13…16); A1 build; R2-B voice completion", "**R2-A gate Fri 5 Nov 2027 (Day 334)**: catalogue GA, 24×7 live, SOC 2 Type I report; SOC 2 Type II window opens"),
    24: ("R4 global build: four region stamps from the EU template, tax engine TX-04…09, de/fr/ar locales, BYOK multi-cloud (I D7); INV-SVC-09…12", "**R3-a EU region ready Fri 19 Nov 2027 (Day 348)**"),
    25: ("R2-B build complete (Fri 3 Dec 2027): mandates, commerce, payments, bids, voice; R4 build complete; SQ-03, SQ-07, SQ-08, SQ-10 released to sustain", "R2-B build complete"),
    26: ("IP sprint PI-4: R2-B UAT, agent-gateway and voice pen tests, counsel UAT per jurisdiction; PI-5 planning", "**R4-a global build ready Fri 17 Dec 2027 (Day 376)**"),
    27: ("Year-end change freeze 24 Dec–2 Jan (no production change); INV-R1 completion, INV-R2 and A1 build", "Change freeze"),
    28: ("INV-R1 build complete (Fri 14 Jan 2028); INV-R2 and A1 build", "**R2-B gate Fri 14 Jan 2028 (Day 404)**; activation per jurisdiction as packs are signed"),
    29: ("A1 build complete (Fri 28 Jan 2028); INV-R2 completion; SQ-02 released", "—"),
    30: ("INV-R2 build complete (Fri 11 Feb 2028); A2 build starts (DEC-905); SQ-06 and SQ-09 released", "**INV-R1 gate Fri 11 Feb 2028 (Day 432)** (IN activation only after RP-IN-SEC signed)"),
    31: ("A2 build: next-best action, deal risk, ABM, intent hub, AI improvement A2 items", "**A1 gate Fri 25 Feb 2028 (Day 446)**; G-A1 KPI window opens"),
    32: ("IP sprint PI-5: A2 build; INV-R2 hypercare; PI-6 planning", "**INV-R2 gate Fri 10 Mar 2028 (Day 460)**"),
    33: ("A2 build: deal rooms, partners, health and QBR, semantic layer", "—"),
    34: ("A2 build: NL analytics, FinOps, compliance evidence; G-A1 decision", "G-A1 (A1 KPIs met for 30 days)"),
    35: ("A2 build complete (Fri 21 Apr 2028); A3 preparation", "—"),
    36: ("A3 build: conversation intelligence, marketing mix, no-code builder, AI improvement A3 (swarm, SDR assistant)", "—"),
    37: ("A3 build; R3 certification close-out", "**A2 gate and R3 exit Fri 19 May 2028 (Day 530)**: SOC 2 Type II report and ISO 27001 certificate"),
    38: ("IP sprint PI-6: A3 build; independent red-team before A3 enablement (M-D5); PI-7 planning", "—"),
    39: ("A3 build: CDP streaming, enablement coach", "ISO 27701 / 42001 Stage 1 audits"),
    40: ("A3 build complete (Fri 30 Jun 2028); SQ-01 and SQ-05 move to the sustain team", "—"),
    41: ("A4 build complete (Fri 14 Jul 2028): AI improvement A4 (marketplace package format, gallery)", "Build of the programme complete"),
}
TAIL = {
    42: ("Sustain team: A3 hypercare, ISO 27701/42001 evidence; no new build", "**A3 gate Fri 28 Jul 2028 (Day 600)**"),
    43: ("Sustain team: ISO 27701/42001 Stage 2 audits; A4 KPI window", "—"),
    44: ("Sustain team: programme close-out pack, benefits review preparation", "**A4 gate Fri 25 Aug 2028 (Day 628)**"),
    45: ("Sustain team: R4 certification close; programme closure and benefits review", "**R4 exit Fri 8 Sep 2028 (Day 642)**: ISO 27701 and 42001 certificates; programme close"),
}
SHORT = {"R0": "R0", "R1_BASE": "R1-core", "R1_V12": "R1-V12", "R1_PD": "R1-PD", "R2A_BASE": "R2A-base", "R2A_CAT": "R2A-cat",
         "R2A_ENT": "R2A-ent", "R2B_P": "R2B-P", "R2B_Q": "R2B-Q", "R3": "R3", "R4": "R4", "INV1": "INV1", "INV2": "INV2",
         "A1": "A1", "A2": "A2", "A3": "A3", "A4": "A4"}


def frag_sprints():
    rows = M.people_cost(RC, 1)
    rm = {x["k"]: x for x in rows}
    o = ["| Sprint | Dates (Mon–Fri) | Days | WD | PI | Squads | FTE squads + roles | Gross capacity pd | Feature capacity SP | Committed SP | Backlog themes (package pd) | Sustain / idle pd | Sprint goal | Milestone |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    tc = tsp = tu = 0
    for row in RC["log"]:
        if not row["nsq"]:
            continue
        k = row["k"]
        x = rm[k]
        used = sum(row["used"].values())
        pk = ", ".join("%s %.0f" % (SHORT[p], v) for p, v in sorted(row["used"].items(), key=lambda z: -z[1]))
        g, ms = GOALS[k]
        tc += row["cap"] + row["baupd"]
        tsp += row["cap"] / 0.7
        tu += used / 0.7
        o.append("| S%d | %s – %s | %d–%d | %d | PI-%d%s | %d | %.1f + %.1f | %.0f | %.0f | %.0f | %s | %.0f | %s | %s |" % (
            k, row["s"].strftime("%d %b %Y"), row["e"].strftime("%d %b %Y"), M.day(row["s"]), M.day(row["e"]), row["wd"],
            row["pi"], " (IP)" if row["ip"] else "", row["nsq"], x["sq_fte"], x["oh_fte"], row["cap"] + row["baupd"],
            row["cap"] / 0.7, used / 0.7, pk, row["idle"] + row["baupd"], g, ms))
    for k in sorted(TAIL):
        s, e, wd = M.sprint_dates(k)
        pi, ip = M.pi_of(k)
        g, ms = TAIL[k]
        o.append("| S%d | %s – %s | %d–%d | %d | PI-%d%s | sustain | sustain team (running) | — | — | — | — | — | %s | %s |" % (
            k, s.strftime("%d %b %Y"), e.strftime("%d %b %Y"), M.day(s), M.day(e), wd, pi, " (IP)" if ip else "", g, ms))
    o.append("| **Total S0–S41** | | | | | | | **%.0f** | **%.0f** | **%.0f** | 6,374 pd central = 9,106 SP | | | |" % (tc, tsp, tu))
    return "\n".join(o)


def frag_squads():
    o = ["| Squad | Mission | Start (sprint, date) | Released to sustain (central) | Staffing | FTE in velocity | Queue (packages in order) | Composition (5.0 FTE standard) |", "|---|---|---|---|---|---|---|---|"]
    comp = {
        "SQ-01": "Team of record (DEC-005/232): BE, FS (Principal Engineer, AI lead), FE, QA 1.0, DevOps 0.5; becomes the sustain core",
        "SQ-02": "2 contract engineers (DEC-228) + 3 from wave 3: tech lead, 2 full-stack, 1 backend, 1 QA automation",
        "SQ-03": "IAM tech lead, 2 backend (SAML/OIDC, SCIM), 1 integration engineer, 1 QA automation",
        "SQ-04": "LLM platform lead, 2 AI/LLM engineers, 1 evaluation engineer, 1 backend",
        "SQ-05": "Tech lead, 2 backend (billing, ledgers), 1 frontend, 1 QA automation",
        "SQ-06": "Tech lead, 2 full-stack, 1 frontend, 1 QA automation",
        "SQ-07": "Payments tech lead, 2 backend (PSP, ledger), 1 security-minded backend, 1 QA automation",
        "SQ-08": "Real-time media lead, 2 backend (voice gateway, ports), 1 AI engineer, 1 QA automation",
        "SQ-09": "Tech lead, 2 full-stack, 1 backend (securities controls), 1 QA automation",
        "SQ-10": "SRE lead, 2 platform/SRE engineers, 1 security engineer, 1 backend (tax, regions)",
        "SQ-11": "AI lead, 2 AI/LLM engineers, 1 data engineer, 1 SRE/security engineer (ASSUMPTION-700, DEC-417)",
    }
    for sq in M.SQUADS:
        st = RC["start"][sq[0]]
        act = [r["k"] for r in RC["log"] if sq[0] in r["active"]]
        prof = ", ".join("%.1f from S%d" % (f, max(fs, st)) for fs, f in sq[3])
        o.append("| %s | %s | S%d %s | S%d %s | %s | %s | %s | %s |" % (sq[0], sq[1], st, M.fmt(M.sprint_dates(st)[0]), max(act),
                                                                    M.fmt(M.gdate(max(act))), sq[5], prof, ", ".join(SHORT[p] for p in sq[4]), comp[sq[0]]))
    return "\n".join(o)


def frag_fte_phase():
    rows = M.people_cost(RC, 1)
    phases = [("Phase 0 Foundation (R0)", 0, 2), ("PI-1", 3, 8), ("PI-2 (R1 gate)", 9, 14), ("PI-3", 15, 20), ("PI-4 (R2-A, R3-a, R4-a)", 21, 26),
              ("PI-5 (R2-B, INV, A1)", 27, 32), ("PI-6 (A2, R3 exit)", 33, 38), ("PI-7 (A3, A4)", 39, 41)]
    o = ["| Phase | Sprints | Calendar | Squads active | Average velocity FTE | Peak velocity FTE | Average programme roles FTE | Peak total FTE | FTE-months |", "|---|---|---|---|---|---|---|---|---|"]
    for nm, a, b in phases:
        xs = [x for x in rows if a <= x["k"] <= b]
        o.append("| %s | S%d–S%d | %s – %s | %d–%d | %.1f | %.1f | %.1f | %.1f | %.0f |" % (
            nm, a, b, M.sprint_dates(a)[0].strftime("%d %b %Y"), M.sprint_dates(b)[1].strftime("%d %b %Y"),
            min(x["nsq"] for x in xs), max(x["nsq"] for x in xs), sum(x["sq_fte"] for x in xs) / len(xs), max(x["sq_fte"] for x in xs),
            sum(x["oh_fte"] for x in xs) / len(xs), max(x["sq_fte"] + x["oh_fte"] for x in xs),
            sum(x["sq_fte"] + x["oh_fte"] for x in xs) * M.MONTH_PER_SPRINT))
    o.append("| **Programme** | S0–S41 | 07 Dec 2026 – 14 Jul 2028 | 1–11 | %.1f | **55.0** | %.1f | **%.2f (S22)** | **%.0f** |" % (
        sum(x["sq_fte"] for x in rows) / len(rows), sum(x["oh_fte"] for x in rows) / len(rows),
        max(x["sq_fte"] + x["oh_fte"] for x in rows), sum(x["sq_fte"] + x["oh_fte"] for x in rows) * M.MONTH_PER_SPRINT))
    return "\n".join(o)


def frag_roles_peak():
    o = ["| Programme role (outside velocity) | FTE at peak (S22) | Rate class | From sprint | Scaling rule |", "|---|---|---|---|---|"]
    rules = {
        "Growth/compliance lead (DEC-232)": ("S0", "0.5, 0.75 from S12 (DEC-232)"),
        "Programme Director": ("S2", "1.0 throughout"),
        "Release Train Engineer": ("S3", "1.0; 0.5 in the A-release tail"),
        "Principal / enterprise architects": ("S3", "1.0, 2.0 from S9; 1.0 in the tail"),
        "Delivery leads / scrum masters": ("S3", "one per three squads"),
        "Domain product owners": ("S4", "one per three squads; the Founder is chief PO (not charged)"),
        "Security engineering (AppSec, cloud, IAM)": ("S4", "1.0, 2.0 from S11, 3.0 from S18; 2.0 in the tail"),
        "DBRE / data architect": ("S5", "1.0; 0.5 in the tail"),
        "UX / product design": ("S5", "1.0, 2.0 from S9; 1.0 in the tail"),
        "QA lead / test architect": ("S7", "1.0"),
        "SRE / operations engineering": ("S9", "1.0, 2.0 from S18; after the R2-A gate paid through the DEC-773 running line"),
        "Technical writer / training": ("S9", "1.0; 0.5 in the tail"),
        "Compliance analysts (R10 delegates)": ("S11", "1.0, 2.0 from S16 (securities, payments, voice)"),
        "FinOps analyst": ("S12", "0.5"),
    }
    tot = 0
    for nm, f, c in M.overhead_roles(22, 11):
        tot += f
        o.append("| %s | %.2f | %s | %s | %s |" % (nm, f, c, rules[nm][0], rules[nm][1]))
    o.append("| **Total programme roles at peak** | **%.2f** | | | |" % tot)
    return "\n".join(o)


def frag_dev_release():
    allocs = []
    for i in range(3):
        rr = M.people_cost(RC, i)
        allocs.append(M.alloc_cost(rr)[0])
    ext = {}
    for nm, a, lo, ce, hi, s in M.EXT:
        e = ext.setdefault(a, [0.0, 0.0, 0.0])
        for i, v in enumerate((lo, ce, hi)):
            e[i] += v
    o = ["| Release | Gate of record | People cost ₹ L L / C / H | External one-time ₹ L L / C / H | **Development total ₹ L L / C / H** | Effort value ₹ L L / C / H (pd × rate) |", "|---|---|---|---|---|---|"]
    T = [[0.0] * 3 for _ in range(3)]
    for rel in list(M.REL_PKGS) + ["Sustain"]:
        pc = [allocs[i].get(rel, 0) for i in range(3)]
        ex = ext.get(rel, [0, 0, 0])
        tot = [pc[i] + ex[i] for i in range(3)]
        if rel in M.REL_PKGS:
            v = [sum(M.PKG[p][i] for p in M.REL_PKGS[rel]) * RATE[i] / 1e5 for i in range(3)]
            gate = d(RC["gates"][rel])
        else:
            v = [0, 0, 0]
            gate = "—"
        for i in range(3):
            T[0][i] += pc[i]; T[1][i] += ex[i]; T[2][i] += tot[i]
        o.append("| %s | %s | %s | %s | **%s** | %s |" % (REL_LABEL[rel], gate, " / ".join("%.1f" % x for x in pc), " / ".join("%.1f" % x for x in ex),
                                                     " / ".join("%.1f" % x for x in tot), " / ".join("%.1f" % x for x in v) if rel in M.REL_PKGS else "—"))
    o.append("| **Total** | | **%s** | **%s** | **%s** | **194.7 / 362.2 / 634.2** |" % tuple(" / ".join("%.1f" % x for x in t) for t in T))
    o.append("| **Total in ₹ crore** | | **%s** | **%s** | **%s** | **1.95 / 3.62 / 6.34** |" % tuple(" / ".join("%.2f" % (x / 100) for x in t) for t in T))
    return "\n".join(o)


def frag_dev_year():
    o = ["| Programme year | Dates | People cost ₹ L L / C / H | External one-time ₹ L L / C / H | **Development total ₹ L L / C / H** |", "|---|---|---|---|---|"]
    py = {"PY1": "Mon 7 Dec 2026 – Sun 5 Dec 2027 (Day 1–364)", "PY2": "Mon 6 Dec 2027 – Sun 3 Dec 2028 (Day 365–728)", "PY3": "Mon 4 Dec 2028 – (Day 729–)"}
    pcy = []
    for i in range(3):
        rr = M.people_cost(RC, i)
        pcy.append(M.alloc_cost(rr)[1])
    exy = [{}, {}, {}]
    for nm, a, lo, ce, hi, s in M.EXT:
        y = M.year_of(M.gdate(RC["gates"][a]))
        for i, v in enumerate((lo, ce, hi)):
            exy[i][y] = exy[i].get(y, 0) + v
    T = [[0.0] * 3 for _ in range(3)]
    for y in ("PY1", "PY2"):
        pc = [pcy[i].get(y, 0) for i in range(3)]
        ex = [exy[i].get(y, 0) for i in range(3)]
        tot = [pc[i] + ex[i] for i in range(3)]
        for i in range(3):
            T[0][i] += pc[i]; T[1][i] += ex[i]; T[2][i] += tot[i]
        o.append("| %s | %s | %s | %s | **%s** |" % (y, py[y], " / ".join("%.1f" % x for x in pc), " / ".join("%.1f" % x for x in ex), " / ".join("%.1f" % x for x in tot)))
    o.append("| **Total** | | **%s** | **%s** | **%s** |" % tuple(" / ".join("%.1f" % x for x in t) for t in T))
    return "\n".join(o)


def frag_ext():
    o = ["| # | One-time external item | Release | ₹ L low | ₹ L central | ₹ L high | Source |", "|---|---|---|---|---|---|---|"]
    t = [0, 0, 0]
    for n, (nm, a, lo, ce, hi, s) in enumerate(M.EXT, 1):
        o.append("| X-%02d | %s | %s | %.2f | %.2f | %.2f | %s |" % (n, nm, REL_LABEL[a].split(" ")[0], lo, ce, hi, s))
        t[0] += lo; t[1] += ce; t[2] += hi
    o.append("| | **Total external one-time** | | **%.2f** | **%.2f** | **%.2f** | |" % tuple(t))
    return "\n".join(o)


def frag_run_lines():
    ry, lines, tool = M.running_by_year(RC, 1)
    o = ["| # | Recurring line | Starts (anchor → central date) | ₹/month low | ₹/month central | ₹/month high | PY1 ₹ L (central) | PY2 ₹ L | PY3 ₹ L | Source |", "|---|---|---|---|---|---|---|---|---|---|"]
    for n, (nm, a, lo, ce, hi, s, intot) in enumerate(M.RUN, 1):
        k = M.anchor_sprint(RC, a)
        lab = {"S0": "Day 1", "S1": "S1", "R2A+6": "R2-A + 6 sprints", "R3a": "R3-a EU ready", "R4a": "R4-a global ready", "END": "end of build"}.get(a, a.replace("R2A", "R2-A gate").replace("R2B", "R2-B gate").replace("INV1", "INV-R1 gate").replace("INV2", "INV-R2 gate"))
        o.append("| B-S%02d | %s%s | %s → %s | %s | %s | %s | %.2f | %.2f | %.2f | %s |" % (
            n, nm, "" if intot else " *(optional; not in totals)*", lab, M.fmt(M.gdate(k)), "{:,}".format(lo), "{:,}".format(ce), "{:,}".format(hi),
            lines.get((nm, "PY1"), 0) / 1e5, lines.get((nm, "PY2"), 0) / 1e5, lines.get((nm, "PY3"), 0) / 1e5, s))
    return "\n".join(o)


def frag_run_year():
    o = ["| Programme year | Operational running ₹ L L / C / H | Build-time tooling (DEC-419/420, per active squad) ₹ L L / C / H | **Recurring total ₹ L L / C / H** |", "|---|---|---|---|"]
    res = [M.running_by_year(RC, i) for i in range(3)]
    T = [[0.0] * 3 for _ in range(3)]
    for y in ("PY1", "PY2", "PY3"):
        op = [res[i][0].get(y, 0) / 1e5 for i in range(3)]
        tl = [res[i][2].get(y, 0) / 1e5 for i in range(3)]
        tot = [op[i] + tl[i] for i in range(3)]
        for i in range(3):
            T[0][i] += op[i]; T[1][i] += tl[i]; T[2][i] += tot[i]
        o.append("| %s | %s | %s | **%s** |" % (y, " / ".join("%.1f" % x for x in op), " / ".join("%.1f" % x for x in tl), " / ".join("%.1f" % x for x in tot)))
    o.append("| **PY1–PY3** | **%s** | **%s** | **%s** |" % tuple(" / ".join("%.1f" % x for x in t) for t in T))
    return "\n".join(o)


def frag_run_rate():
    o = ["| Release | Monthly run-rate added ₹ L / C / H | Cumulative run-rate after the release ₹ L / C / H (per month) |", "|---|---|---|"]
    rr = [M.run_rate_by_release(i) for i in range(3)]
    order = ["R0", "R1", "R2A", "R2B", "R3", "R4", "INV1", "INV2", "A1", "A2", "Sustain"]
    cum = [0, 0, 0]
    for k in order:
        v = [rr[i].get(k, 0) for i in range(3)]
        for i in range(3):
            cum[i] += v[i]
        o.append("| %s | %s | %s |" % (REL_LABEL.get(k, k), " / ".join("{:,}".format(int(x)) for x in v), " / ".join("{:,}".format(int(x)) for x in cum)))
    return "\n".join(o)


def frag_scen():
    o = ["| Calibration result (DEC-420) | Productivity multiplier | R1 | R2-A | R2-B | INV-R2 | A4 | R4 exit | People cost ₹ L (central rates) | FTE-months |", "|---|---|---|---|---|---|---|---|---|---|"]
    for lab, p in (("Plan of record (no saving assumed)", 1.0), ("10–20% saving (keep plan, DEC-420)", 1.11), ("≥ 20% saving, option B (same team, earlier dates)", 1.25), ("30% saving, option B", 1.43)):
        r = M.run(1, prod=p)
        pc = M.people_cost(r, 1)
        g = r["gates"]
        o.append("| %s | %.2f | %s | %s | %s | %s | %s | %s | %.1f | %.0f |" % (lab, p, d(g["R1"]), d(g["R2A"]), d(g["R2B"]), d(g["INV2"]), d(g["A4"]), d(g["R4"]),
                                                                       sum(x["sq_cost"] + x["oh_cost"] for x in pc), sum(x["sq_fte"] + x["oh_fte"] for x in pc) * M.MONTH_PER_SPRINT))
    # option A: drop SQ-06, reassign its queue to SQ-05
    sq = [s for s in M.SQUADS if s[0] != "SQ-06"]
    sq = [(s[0], s[1], s[2], s[3], s[4] + [p for p in ("R2A_CAT", "INV1", "INV2") if p not in s[4]] if s[0] == "SQ-05" else s[4], s[5]) for s in sq]
    bak = M.SQUADS
    M.SQUADS = sq
    r = M.run(1, prod=1.25, squads=sq)
    pc = M.people_cost(r, 1)
    M.SQUADS = bak
    g = r["gates"]
    o.append("| ≥ 20%% saving, **option A (default)**: keep dates, SQ-06 not hired, its queue moves to SQ-05 | 1.25 | %s | %s | %s | %s | %s | %s | %.1f | %.0f |" % (
        d(g["R1"]), d(g["R2A"]), d(g["R2B"]), d(g["INV2"]), d(g["A4"]), d(g["R4"]), sum(x["sq_cost"] + x["oh_cost"] for x in pc), sum(x["sq_fte"] + x["oh_fte"] for x in pc) * M.MONTH_PER_SPRINT))
    return "\n".join(o)


FRAGS = {
    "F_ROLLUP_GROUP": frag_rollup_group, "F_ROLLUP_CAP": frag_rollup_cap, "F_OVERLAP": frag_overlap, "F_PKG": frag_pkg,
    "F_GATES": frag_gates, "F_SPRINTS": frag_sprints, "F_SQUADS": frag_squads, "F_FTE_PHASE": frag_fte_phase,
    "F_ROLES_PEAK": frag_roles_peak, "F_DEV_REL": frag_dev_release, "F_DEV_YEAR": frag_dev_year, "F_EXT": frag_ext,
    "F_RUN_LINES": frag_run_lines, "F_RUN_YEAR": frag_run_year, "F_RUN_RATE": frag_run_rate, "F_SCEN": frag_scen,
}

if __name__ == "__main__":
    import re
    cache = {}
    for tmpl, out in (("s_part_a.tmpl.md", "Part-11-20a_Master_Implementation_Plan_V12_Rollup_Releases_Gates_Calendar.md"),
                      ("s_part_b.tmpl.md", "Part-11-20b_Master_Implementation_Plan_V12_Sprints_Team_Budget_RAID.md")):
        p = os.path.join(HERE, tmpl)
        if not os.path.exists(p):
            continue
        txt = open(p, encoding="utf-8").read()

        def sub(m):
            k = m.group(1)
            if k not in cache:
                cache[k] = FRAGS[k]()
            return cache[k]
        txt = re.sub(r"\{\{(F_[A-Z_]+)\}\}", sub, txt)
        open(os.path.join(BP, out), "w", encoding="utf-8").write(txt)
        print("wrote", out)
    if len(sys.argv) > 1:
        for k in sys.argv[1:]:
            print(FRAGS[k]())
