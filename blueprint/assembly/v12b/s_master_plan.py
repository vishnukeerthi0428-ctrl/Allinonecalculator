#!/usr/bin/env python3
"""Group S (Part 11.20) master implementation plan model.

Reproduces every number in Part 11.20: effort roll-up with overlap netting,
release allocation, capacity-driven calendar (2-week sprints from Mon 7 Dec 2026),
team scaling, and development / running budgets by release and by programme year.

Run:  python3 -I s_master_plan.py  > s_master_plan_out.md
All inputs are cited to the Part 11 / Part 9 effort tables in comments.
"""
import datetime as dt
import json
import math
import sys

D1 = dt.date(2026, 12, 7)  # Day 1 (ASSUMPTION-197, task instruction)
L, C, H = 0, 1, 2

# ---------------------------------------------------------------- 1. gross effort by group (pd low/central/high)
GROSS = {
    # programme baseline and V11
    "BASE": ("Baseline Parts 0-9.5 (DEC-228)", (532.0, 722.0, 921.0)),
    "ALN": ("V11 literal alignment CR-ALN-01 (DEC-416)", (61.25, 107.2, 170.8)),
    "ADV": ("V11 advanced A1-A3 X1+X2+X3 net of 9.10.4 (DEC-411/417)", (926.0, 1354.0, 1925.0)),
    # V12 review groups 11.1-11.13
    "A": ("11.1 Business requirements P-A", (119.0, 177.0, 254.0)),
    "B": ("11.2 Service catalogue CR-V12-B-01", (236.5, 349.5, 512.0)),
    "C": ("11.3 Workflows SVC-01..20", (155.0, 227.0, 299.0)),
    "D": ("11.4 Workflows SVC-21..39 D-1..D-4", (298.5, 437.75, 577.0)),
    "E": ("11.5 Platform architecture CR-V12-E-01..03", (200.0, 297.0, 455.0)),
    "F": ("11.6 AI engines CR-V12-F", (242.0, 357.0, 530.0)),
    "G": ("11.7 UI/UX DEC-633", (252.0, 353.0, 536.0)),
    "H": ("11.8 API and integrations CR-V12-H-01 (R1-R2 + later)", (130.0, 194.0, 272.0)),
    "I": ("11.9 Data, security, analytics D1-D7", (49.0, 67.5, 86.0)),
    "J": ("11.10 Backlog CR-V12-J-01 + J-02", (366.1, 597.8, 965.4)),
    "K": ("11.11 Observability CR-V12-K-01", (59.5, 83.25, 107.0)),
    "L": ("11.12 Historical annex", (25.0, 35.5, 46.0)),
    "M": ("11.13 AI improvement CR-AIM-01 (A2-A4)", (240.6, 367.8, 534.0)),
    # Founder-decision parts 11.16-11.19
    "N": ("11.16a/b/e Investment I CR-V12-N-01", (315.0, 496.0, 751.0)),
    "O": ("11.16c/d Investment II", (244.0, 358.0, 526.0)),
    "P": ("11.17 Mandates, commerce, bids CR-V12-P", (293.0, 435.0, 625.0)),
    "Q": ("11.18 Voice and recordings", (187.0, 269.0, 397.0)),
    "R": ("11.19 Platform decisions CR-V12-R-01 (gross)", (187.0, 275.0, 391.0)),  # 183/269/382 + EU zone 4/6/9
    # enterprise items estimated in this part (ASSUMPTION-1104)
    "ENT": ("11.20 Enterprise items ENT-01..10 (this part)", (228.0, 348.0, 521.0)),
}

# ---------------------------------------------------------------- 2. overlap register (removed pd)
OVL = [
    # id, removed-from group, what, owner kept, (l,c,h)
    ("OV-01", "C", "SVC-01..20 workflow binding, partial and not-covered enhancements, test automation", "J SKU build SVC-01..20 (higher central 169.3)", (109.0, 162.5, 216.0)),
    ("OV-02", "B", "WF04 and SKU deltas SVC-01..25", "J SKU build", (37.5, 62.5, 100.0)),
    ("OV-03", "D", "D-1 alignment of 19 workflows, D-2, D-3 (SVC-21..39 workflows and adapters)", "J SKU build SVC-21..39 (higher central 248.9)", (163.5, 243.75, 324.0)),
    ("OV-04", "B", "SKU wrappers, tabs, EP-23/25/26/27/28 new services", "J SKU build (classes M/N)", (106.0, 153.0, 222.0)),
    ("OV-05", "J", "SM-SVC-26 and SM-SVC-28 SKU builds", "Q (voice) and P (agentic commerce)", (32.2, 53.7, 85.3)),
    ("OV-06", "B", "EP-22 voice and EP-24 agentic commerce", "Q and P", (58.0, 82.0, 118.0)),
    ("OV-07", "D", "CR-V12-D-4 conflict workflows and voice/media adapters", "P, Q and J SVC-27", (86.0, 129.0, 172.0)),
    ("OV-08", "B", "EP-29 catalogue framework", "E9/E11/E13 + D common engine", (20.0, 30.0, 42.0)),
    ("OV-09", "C", "Contract registry, DTO validators, run API, step state", "D common engine", (21.0, 29.0, 37.0)),
    ("OV-10", "D", "Archetype test harness", "J TASK-V12-J-001/002", (8.0, 11.0, 14.0)),
    ("OV-11", "B", "Acceptance of 195 scenarios + 264 TC", "J per-SKU test packs", (15.0, 22.0, 30.0)),
    ("OV-12", "E", "CR-V12-E-02 enterprise identity E2-E6", "R-WP01..03 (DEC-784 owner)", (58.0, 86.0, 134.0)),
    ("OV-13", "E", "E12 plan change/proration; E21 backup Option A/B", "A WP-A3; R-WP16 (DEC-787)", (14.0, 21.0, 32.0)),
    ("OV-14", "A", "WP-A1 registry, half WP-A2, WP-A8 wizard, WP-A10 status/help, WP-A11 metrics", "E9/E13, E7+G14, K, I D3", (33.0, 49.5, 71.0)),
    ("OV-15", "G", "A089 delta, storefront calculators, investor-mode removal", "A WP-A9, A WP-A5, N (DEC-783)", (15.0, 22.0, 33.0)),
    ("OV-16", "F", "AG-100 voice router, AG-104 commerce counterparty", "Q AG-210..219, P AG-200..209", (12.0, 18.0, 26.0)),
    ("OV-17", "H", "H8 SIEM sink; later voice CPaaS, BYOK, Java SDK, US tax", "R-WP03, Q, I D7, R-WP06, ENT-06", (23.0, 35.0, 50.0)),
    ("OV-18", "I", "D5 audit sinks, D6 sandbox, half D4", "R-WP03, R-WP08, Part 9.5 I-1", (13.0, 17.75, 22.5)),
    ("OV-19", "R", "CR-V12-H-01 H1/H2/H3/H7 + CRM/SMS (R's own netting) and R-WP14 voice transport", "H and Q", (69.0, 102.0, 142.0)),
    ("OV-20", "ADV", "A3 developer platform, BYOK, status page; A1 registry canary and DR-drill automation", "H/R, I D7, K, R-WP16/17", (39.0, 58.0, 83.0)),
]

# absorption into existing stories at refinement (ASSUMPTION-1103): V12 groups A-L only
ABSORB_GROUPS = list("ABCDEFGHIJKL")
ABSORB = (0.10, 0.075, 0.05)


def net_by_group():
    out = {}
    for g, (_, v) in GROSS.items():
        rem = [0.0, 0.0, 0.0]
        for o in OVL:
            if o[1] == g:
                for i in range(3):
                    rem[i] += o[4][i]
        n = [v[i] - rem[i] for i in range(3)]
        ab = [n[i] * ABSORB[i] if g in ABSORB_GROUPS else 0.0 for i in range(3)]
        out[g] = dict(gross=v, removed=rem, net=n, absorbed=ab, plan=[n[i] - ab[i] for i in range(3)])
    return out


NET = net_by_group()

# ---------------------------------------------------------------- 3. allocation of each group's net central to release packages
# fractions per group (sum = 1). Release packages:
# R0, R1-BASE, R1-V12, R1-PD, R2A-BASE, R2A-CAT, R2A-ENT, R2B-P, R2B-Q, R3, R4, INV1, INV2, A1, A2, A3, A4
def frac(**kw):
    s = sum(kw.values())
    return {k: v / s for k, v in kw.items()}

ALLOC = {
    "BASE": frac(R0=73, R1_BASE=408, R2A_BASE=111, R3=130),
    "ALN": frac(R1_BASE=80.5, R2A_BASE=26.7),
    "ADV": frac(A1=538, A2=440.55, A3=317.45),  # after OV-20: A1 553-15, A2/A3 = 55/45 split of 801 less 43 on A3
    "A": frac(R1_V12=27, R2A_CAT=100.5),
    "B": frac(R2A_CAT=1),  # zero after netting
    "C": frac(R2A_CAT=1),
    "D": frac(R1_V12=1),
    "E": frac(R1_V12=72, R2A_CAT=118),
    "F": frac(R1_V12=149.5, R2A_CAT=189.5),
    "G": frac(R1_V12=132.4, R2A_CAT=198.6),
    "H": frac(R1_PD=95.4, R2A_CAT=63.6),
    "I": frac(R1_V12=33.75, R4=16),
    "J": frac(R2A_CAT=1),
    "K": frac(R1_V12=49.95, R2A_CAT=33.3),
    "L": frac(R1_V12=1),
    "M": frac(A2=151.8, A3=160.8, A4=55.2),
    "N": frac(INV1=1),
    "O": frac(INV2=1),
    "P": frac(R2B_P=1),
    "Q": frac(R2B_Q=1),
    "R": frac(R0=15, R1_PD=137, R2A_CAT=15, R3=6),
    "ENT": frac(R2A_ENT=67, R3=158, R4=123),
}

PKG_NAMES = {
    "R0": "R0 Foundation",
    "R1_BASE": "R1 core (baseline Release 1 + alignment Musts)",
    "R1_V12": "R1 V12 core platform, AI governance, UX, ops",
    "R1_PD": "R1 enterprise identity, developer platform, connectors, platform decisions",
    "R2A_BASE": "R2-A baseline Release 2 (closure, SaaS)",
    "R2A_CAT": "R2-A full V12 service catalogue (39 SKUs, billing, screens, agents)",
    "R2A_ENT": "R2-A enterprise operations (24x7, 99.95% topology, SOC 2 Type I)",
    "R2B_P": "R2-B bounded mandates, agentic commerce, payments, automatic bids",
    "R2B_Q": "R2-B AI voice and recordings",
    "R3": "R3 EU region, SOC 2 Type II, ISO 27001, managed Kubernetes, W6 backlog",
    "R4": "R4 global regions, tax engine, locales, BYOK, ISO 27701/42001",
    "INV1": "INV-R1 Investment Automation I (INV-SVC-01..12)",
    "INV2": "INV-R2 Investment Automation II (INV-SVC-13..24)",
    "A1": "A1 advanced foundations (X1-X3)",
    "A2": "A2 growth intelligence + AI improvement A2",
    "A3": "A3 scale + AI improvement A3",
    "A4": "A4 AI improvement A4",
}


def packages():
    pk = {k: [0.0, 0.0, 0.0] for k in PKG_NAMES}
    for g, fr in ALLOC.items():
        for p, f in fr.items():
            for i in range(3):
                pk[p][i] += NET[g]["plan"][i] * f
    return pk


PKG = packages()

# ---------------------------------------------------------------- 4. calendar
HOLIDAYS = {  # weekday national holidays and year-end leave; verify (as of 27 Nov 2026) - ASSUMPTION-1100
    "2026-12-25", "2027-01-01", "2027-01-26", "2027-03-22", "2027-03-26", "2027-10-29",
    "2028-01-26", "2028-04-14", "2028-08-15", "2028-10-02", "2028-10-17", "2028-12-25",
    "2029-01-01", "2029-01-26", "2029-03-01", "2029-03-30", "2029-08-15", "2029-10-02", "2029-11-05", "2029-12-25",
    "2030-01-01",
}
HOL = {dt.date.fromisoformat(x) for x in HOLIDAYS}
NSPR = 80


def sprint_dates(k):
    s = D1 + dt.timedelta(days=14 * k)
    e = s + dt.timedelta(days=11)
    wd = sum(1 for i in range(12) if (s + dt.timedelta(days=i)).weekday() < 5 and (s + dt.timedelta(days=i)) not in HOL)
    return s, e, wd


def day(d):
    return (d - D1).days + 1


def fmt(d):
    return d.strftime("%a %d %b %Y").replace(" 0", " ")


def pi_of(k):
    """PI-0 = S0-S2; PI-n = 6 sprints from S3; 6th sprint of a PI is the IP sprint (50% feature capacity)."""
    if k <= 2:
        return 0, False
    return (k - 3) // 6 + 1, (k - 3) % 6 == 5


PD_PER_FTE = 7.53   # Part 9.5 9.5.2.5: 33.9 pd per 4.5 engineering FTE per 10-day sprint
LEAVE = 0.95        # annual-leave allowance (ASSUMPTION-1101)
NEW_FTE_RAMP = (0.5, 0.85)  # first and second sprint of a newly added FTE (ASSUMPTION-1101)


def coord_factor(nsq):  # cross-squad coordination loss (ASSUMPTION-1101)
    return 1.0 if nsq <= 4 else (0.95 if nsq <= 7 else 0.92)


# squads: id, name, start sprint, FTE profile [(from_sprint, fte)], queue, staffing type
SQUADS = [
    ("SQ-01", "Core Platform (team of record)", 0, [(0, 4.5), (2, 4.0), (3, 4.5), (9, 5.0)],
     ["R0", "R1_BASE", "R2A_BASE", "R3", "A2", "A3"], "employee"),
    ("SQ-02", "Core Delivery (DEC-228 contract engineers, extended)", 3, [(3, 2.0), (6, 5.0)],
     ["R0", "R1_BASE", "R1_V12", "R2A_CAT", "R3", "A1"], "contract"),
    ("SQ-03", "Identity and Developer Platform", 4, [(4, 5.0)],
     ["R0", "R1_PD", "R2A_CAT", "R3", "R4"], "contract"),
    ("SQ-04", "AI Platform and Evaluation", 5, [(5, 5.0)],
     ["R1_V12", "R2A_CAT", "A1", "A2", "A3", "A4"], "contract"),
    ("SQ-05", "Catalogue and Billing I", 7, [(7, 5.0)],
     ["R1_V12", "R2A_CAT", "INV2", "A2", "A3"], "contract"),
    ("SQ-06", "Catalogue Services II", 9, [(9, 5.0)],
     ["R2A_CAT", "INV1", "INV2"], "contract"),
    ("SQ-07", "Autonomy, Commerce and Bids", 11, [(11, 5.0)],
     ["R2B_P", "R4"], "contract"),
    ("SQ-08", "Voice and Recordings", 12, [(12, 5.0)],
     ["R2B_Q", "R2B_P", "R4"], "contract"),
    ("SQ-09", "Investment Automation", 16, [(16, 5.0)],
     ["INV1", "INV2"], "contract"),
    ("SQ-10", "Regions, Resilience and Compliance", 18, [(18, 5.0)],
     ["R2A_ENT", "R3", "R4"], "contract"),
    ("SQ-11", "Advanced Intelligence (DEC-417 A1 team)", None, [(0, 5.0)],
     ["A1", "A2", "A3", "A4"], "contract"),
]

EARLIEST0 = {"R0": 0, "R1_BASE": 0, "R1_V12": 3, "R1_PD": 1, "R2A_BASE": 12, "R2A_CAT": 9, "R2A_ENT": 18,
             "R2B_P": 11, "R2B_Q": 12, "R3": 18, "R4": None, "INV1": 16, "INV2": 22,
             "A1": None, "A2": None, "A3": None, "A4": None}
REL_PKGS = {"R0": ["R0"], "R1": ["R1_BASE", "R1_V12", "R1_PD"], "R2A": ["R2A_BASE", "R2A_CAT", "R2A_ENT"],
            "R2B": ["R2B_P", "R2B_Q"], "R3": ["R3"], "R4": ["R4"], "INV1": ["INV1"], "INV2": ["INV2"],
            "A1": ["A1"], "A2": ["A2"], "A3": ["A3"], "A4": ["A4"]}
HARDEN = {"R0": 0, "R1": 1, "R2A": 2, "R2B": 2, "R3": 1, "R4": 1, "INV1": 2, "INV2": 2,
          "A1": 2, "A2": 2, "A3": 2, "A4": 2}   # hardening/UAT/pen-test/KPI-window sprints (ASSUMPTION-1105)
BAU_AFTER_R1, BAU_AFTER_R2 = 0.10, 0.15      # sustain reserve on active squads (ASSUMPTION-1102)


def run(idx, prod=1.0, squads=None, sq11_start=None):
    squads = squads or SQUADS
    rem = {p: PKG[p][idx] for p in PKG}
    done, gates, build = {}, {}, {}
    earliest = dict(EARLIEST0)
    log = []
    sq_start = {}
    last_work = {}
    for sq in squads:
        sq_start[sq[0]] = sq[2]
    for k in range(NSPR):
        s, e, wd = sprint_dates(k)
        pi, ip = pi_of(k)
        if sq_start.get("SQ-11") is None and "R2A" in gates:
            sq_start["SQ-11"] = (sq11_start if sq11_start is not None else gates["R2A"] - 2)
        active = []
        for sq in squads:
            st = sq_start[sq[0]]
            if st is None or k < st:
                continue
            if all(p in done for p in sq[4]):
                continue  # squad released
            active.append(sq)
        cf = coord_factor(len(active))
        bau = BAU_AFTER_R2 if "R2A" in gates else (BAU_AFTER_R1 if "R1" in gates else 0.0)
        tot_fte = tot_cap = 0.0
        used = {}
        idle = 0.0
        for sq in active:
            st = sq_start[sq[0]]
            fte = 0.0
            eff = 0.0
            prev = 0.0
            for (fs, f) in sq[3]:
                fs = max(fs, st)
                if k < fs:
                    break
                inc = f - prev
                age = k - fs
                r = 1.0
                if inc > 0 and sq[0] != "SQ-01" and age < len(NEW_FTE_RAMP):
                    r = NEW_FTE_RAMP[age]
                eff += inc * r if inc > 0 else inc
                fte = f
                prev = f
            if sq[0] == "SQ-01" and k <= 1:
                eff *= 0.7   # Part 8.1 ramp in S0-S1 (ASSUMPTION-157)
            cap = eff * prod * PD_PER_FTE * (wd / 10.0) * LEAVE * cf * (0.5 if ip else 1.0) * (1 - bau)
            tot_fte += fte
            tot_cap += cap
            worked = False
            for p in sq[4]:
                if p in done or rem[p] <= 1e-9:
                    continue
                if earliest.get(p) is None or earliest[p] > k:
                    continue
                take = min(cap, rem[p])
                rem[p] -= take
                cap -= take
                used[p] = used.get(p, 0) + take
                worked = True
                if rem[p] <= 1e-9:
                    done[p] = k
                if cap <= 1e-9:
                    break
            idle += cap
            if worked:
                last_work[sq[0]] = k
        log.append(dict(k=k, s=s, e=e, wd=wd, pi=pi, ip=ip, nsq=len(active), fte=tot_fte, cap=tot_cap,
                        used=used, idle=idle, bau=bau, baupd=(tot_cap * bau / (1 - bau)) if bau < 1 else 0.0,
                        active=[x[0] for x in active]))
        for rel, pk in REL_PKGS.items():
            if rel not in build and all(p in done for p in pk):
                build[rel] = max(done[p] for p in pk)
                gk = build[rel] + HARDEN[rel]
                while in_freeze(gk):
                    gk += 1   # year-end change freeze (RECOMMENDATION-1112)
                gates[rel] = gk
        if "R2A" in gates and earliest["A1"] is None:
            earliest["A1"] = gates["R2A"] - 2  # DEC-417: A1 build starts at the Release 2 build gate
        for a, b in (("A1", "A2"), ("A2", "A3"), ("A3", "A4")):
            if a in build and earliest[b] is None:
                earliest[b] = build[a] + 1      # DEC-9xx: next A-build overlaps the KPI window; activation still gated
        if "R3" in build and earliest["R4"] is None:
            earliest["R4"] = build["R3"] + 1
    for a, b in (("A1", "A2"), ("A2", "A3"), ("A3", "A4")):
        if a in gates and b in gates and gates[b] < gates[a] + 2:
            gates[b] = gates[a] + 2
            while in_freeze(gates[b]):
                gates[b] += 1
    cert = {}
    if "R2A" in gates and "R3" in gates:
        cert["R3"] = gates["R2A"] + 14   # SOC 2 Type II window 6 months + report (ASSUMPTION-1105)
        gates["R3"] = max(gates["R3"], cert["R3"])
    if "R3" in gates and "R4" in gates:
        cert["R4"] = gates["R3"] + 8     # ISO 27701 / 42001 after the ISO 27001 certificate
        gates["R4"] = max(gates["R4"], cert["R4"])
    for g_ in ("R3", "R4"):
        while g_ in gates and in_freeze(gates[g_]):
            gates[g_] += 1
    return dict(gates=gates, build=build, done=done, log=log, rem=rem, last=last_work, start=sq_start)


def in_freeze(k):
    s, e, wd = sprint_dates(k)
    return any((s + dt.timedelta(days=i)).month == 12 and (s + dt.timedelta(days=i)).day in (24, 25, 26, 27, 28, 29, 30, 31) for i in range(12))


def gdate(k):
    return sprint_dates(k)[1]


# ---------------------------------------------------------------- 5. people cost model
MONTH_PER_SPRINT = 14 / 30.4
RATE = {  # ₹ lakh per FTE-month: low, central, high
    "employee": (1.0, 1.25, 1.5),        # BRD §6
    "contract": (1.2, 1.5, 1.8),         # ASSUMPTION-202
    "lead": (2.0, 2.5, 3.0),             # ASSUMPTION-1107
    "mid": (1.2, 1.5, 1.8),
}


def overhead_roles(k, nsq, r2_live=False):
    """Non-velocity roles by sprint (FTE, rate class). Founder/PO time excluded (ASSUMPTION-205).
    After the R2-A gate the second-line SRE rota is paid through the DEC-773 running line, not here.
    When four or fewer squads remain (A-release tail) the programme roles scale down."""
    third = math.ceil(nsq / 3)
    tail = k >= 26 and nsq <= 4
    r = [("Growth/compliance lead (DEC-232)", 0.5 if k < 12 else 0.75, "employee")]
    if k >= 2: r.append(("Programme Director", 1.0, "lead"))
    if k >= 3: r.append(("Release Train Engineer", 0.5 if tail else 1.0, "lead"))
    if k >= 3: r.append(("Principal / enterprise architects", 1.0 if (k < 9 or tail) else 2.0, "lead"))
    if k >= 3: r.append(("Delivery leads / scrum masters", float(third), "mid"))
    if k >= 4: r.append(("Domain product owners", float(third), "lead"))
    if k >= 4: r.append(("Security engineering (AppSec, cloud, IAM)", 1.0 if k < 11 else (2.0 if (k < 18 or tail) else 3.0), "lead"))
    if k >= 5: r.append(("DBRE / data architect", 0.5 if tail else 1.0, "lead"))
    if k >= 5: r.append(("UX / product design", 1.0 if (k < 9 or tail) else 2.0, "mid"))
    if k >= 7: r.append(("QA lead / test architect", 1.0, "lead"))
    if k >= 9 and not r2_live: r.append(("SRE / operations engineering", 1.0 if k < 18 else 2.0, "lead"))
    if k >= 9: r.append(("Technical writer / training", 0.5 if tail else 1.0, "mid"))
    if k >= 11: r.append(("Compliance analysts (R10 delegates)", 1.0 if k < 16 else 2.0, "mid"))
    if k >= 12: r.append(("FinOps analyst", 0.5, "mid"))
    return r


def people_cost(res, idx):
    """Return per-sprint cost (₹ lakh) of squads + overhead, and allocation by package."""
    rows = []
    for row in res["log"]:
        k = row["k"]
        nsq = row["nsq"]
        if nsq == 0:
            continue
        sq_cost = 0.0
        sq_fte = 0.0
        for sq in SQUADS:
            if sq[0] not in row["active"]:
                continue
            fte = 0.0
            st = res["start"][sq[0]]
            for fs, f in sq[3]:
                if k >= max(fs, st):
                    fte = f
            if sq[5] == "employee":
                c = fte * RATE["employee"][idx]
            else:
                lead = 1.0 if fte >= 4 else 0.0
                c = (fte - lead) * RATE["contract"][idx] + lead * RATE["lead"][idx]
            sq_cost += c * MONTH_PER_SPRINT
            sq_fte += fte
        oh = overhead_roles(k, nsq, r2_live=("R2A" in res["gates"] and k > res["gates"]["R2A"]))
        oh_fte = sum(f for _, f, _ in oh)
        oh_cost = sum(f * RATE[c][idx] for _, f, c in oh) * MONTH_PER_SPRINT
        rows.append(dict(k=k, sq_fte=sq_fte, oh_fte=oh_fte, sq_cost=sq_cost, oh_cost=oh_cost, used=row["used"],
                         idle=row["idle"] + row["baupd"], cap=row["cap"], e=row["e"], s=row["s"], nsq=nsq))
    return rows


def rel_of(p):
    for r, pk in REL_PKGS.items():
        if p in pk:
            return r
    return p


def year_of(d):
    dd = day(d)
    return "PY1" if dd <= 365 else ("PY2" if dd <= 730 else ("PY3" if dd <= 1095 else "PY4"))


def alloc_cost(rows):
    by_rel, by_year, by_rel_year = {}, {}, {}
    for r in rows:
        tot = r["sq_cost"] + r["oh_cost"]
        used = sum(r["used"].values())
        base = used + r["idle"]
        y = year_of(r["e"])
        by_year[y] = by_year.get(y, 0) + tot
        if base <= 0:
            by_rel["Sustain"] = by_rel.get("Sustain", 0) + tot
            continue
        for p, v in r["used"].items():
            rl = rel_of(p)
            by_rel[rl] = by_rel.get(rl, 0) + tot * v / base
            by_rel_year[(rl, y)] = by_rel_year.get((rl, y), 0) + tot * v / base
        if r["idle"] > 0:
            by_rel["Sustain"] = by_rel.get("Sustain", 0) + tot * r["idle"] / base
            by_rel_year[("Sustain", y)] = by_rel_year.get(("Sustain", y), 0) + tot * r["idle"] / base
    return by_rel, by_year, by_rel_year


# ---------------------------------------------------------------- 6. external one-time and running lines (₹ lakh / ₹ per month)
# (name, release anchor, low, central, high, source)
EXT = [
    ("Counsel review and sign-off of the 11 marketing rule packs (M-D4)", "R1", 1.0, 1.75, 2.75, "11.13b; 11.15c"),
    ("Platform-decision legal: Vercel DPA, CRM transfers, BM-CL-1, edge-transit opinion", "R1", 2.0, 3.5, 5.0, "11.19b"),
    ("Pen-test scope extension: SSO, SCIM, developer host, webhooks, connectors", "R1", 2.0, 3.25, 4.5, "11.19b; 11.8b"),
    ("Independent differential-privacy review; DLT registrations", "R1", 1.1, 1.95, 2.8, "11.19b"),
    ("Hindi chrome translation", "R1", 0.38, 0.5, 0.75, "11.7b item 16"),
    ("Tax adviser and legal review: order form, e-sign, refunds", "R2A", 1.0, 2.25, 3.5, "11.5b"),
    ("SOC 2 readiness assessment", "R2A", 3.0, 5.5, 8.0, "11.5b; Part 9.9 GAP-714"),
    ("SOC 2 Type I audit", "R2A", 9.0, 18.0, 27.0, "DEC-775"),
    ("Counsel: 8 payment, agent-commerce and procurement packs; portal terms", "R2B", 8.0, 16.0, 27.0, "11.17b"),
    ("Pen test: agent gateway, PSP webhooks, approval flows; PSP certification", "R2B", 3.0, 5.5, 9.5, "11.17b"),
    ("Voice: counsel per country (6), DPIA, voice pen test, telecom registrations, brand voice", "R2B", 9.2, 20.1, 41.5, "11.18c"),
    ("Investment I: regulatory-characterisation opinions IN/US/EU/UK, counsel UAT, DPIA, data-room pen test", "INV1", 27.5, 49.75, 72.0, "11.16e"),
    ("Investment II: counsel for 7 securities packs (IN, US, EU, UK, AML/KYC, advice perimeter), KYC sandbox", "INV2", 48.8, 76.4, 104.0, "11.16d"),
    ("EU: DPIA, EU AI Act conformity file, member-state counsel for EU packs, Art. 27 representative", "R3", 5.0, 9.0, 15.0, "ASSUMPTION-1104; DEC-776"),
    ("ISO/IEC 27001 certification", "R3", 8.0, 14.0, 20.0, "DEC-775"),
    ("EU-stack penetration test", "R3", 1.5, 2.75, 4.0, "ASSUMPTION-1104"),
    ("German and French translation of chrome and public pages", "R3", 0.75, 1.25, 2.0, "11.7b item 16"),
    ("ISO/IEC 27701 and ISO/IEC 42001 certification", "R4", 10.0, 20.0, 30.0, "DEC-775"),
    ("Per-market counsel for UK, UAE, Singapore, Australia, US marketing and voice packs", "R4", 20.0, 35.0, 50.0, "ASSUMPTION-1104; DEC-776"),
    ("Tax adviser per market for TX-04…09 (6 markets)", "R4", 6.0, 12.0, 18.0, "ASSUMPTION-1104; DEC-776"),
    ("Multi-region and BYOK penetration test", "R4", 1.5, 2.75, 4.0, "ASSUMPTION-1104"),
    ("Arabic translation and RTL legal templates", "R4", 0.38, 0.75, 1.25, "11.7b item 16"),
    ("Independent red-team before A3 enablement (M-D5)", "A3", 0.75, 1.25, 2.0, "11.13b"),
]

# (name, anchor, low ₹/month, central, high, source, in_total)
RUN = [
    ("Ledger B base (DEC-422: pilot running incl. 15% contingency and 2 seats)", "S0", 26105, 30734, 35362, "DEC-422", True),
    ("PITR add-on (DEC-771/787)", "S1", 8500, 9150, 9800, "DEC-771; 11.5b RB-E1a", True),
    ("Platform decisions IN cell: standby, WAL archive, log drains, WAF, registry evaluations, benchmarks", "R1", 13800, 30900, 48000, "11.19b (SMS in B25 once; voice in 11.18)", True),
    ("AI evaluation lines and new-agent tokens (CR-V12-F-R)", "R1", 580, 1676, 4586, "11.6b", True),
    ("Translation maintenance and parity CI", "R1", 750, 2625, 4500, "11.7b", True),
    ("Webhook workers, SMS-DLT (B25), status host", "R1", 300, 2000, 3700, "11.8b", True),
    ("SLA, status, paging tool, game days, help maintenance", "R1", 5030, 9924, 14818, "11.11b", True),
    ("Literal-alignment running CR-ALN-02 (upper bound)", "R1", 1495, 5808, 10120, "DEC-416", True),
    ("Business-requirement items: status host, help, metric projections", "R2A", 300, 3050, 5800, "11.1b", True),
    ("V12 workflow AI sub-line, SMS/RCS, agent gateway, workers", "R2A", 2589, 3725, 4860, "11.4d", True),
    ("Logical dumps, SIEM sinks, e-sign envelopes", "R2A", 150, 1050, 1950, "11.5b", True),
    ("Annual pen test, bug bounty, audit-sink egress", "R2A", 12500, 35667, 58833, "11.9c", True),
    ("CI and provider sandboxes for the SKU test catalogue", "R2A", 0, 3250, 6500, "11.10c", True),
    ("24x7 on-call: contracted NOC/SOC first line + internal rota (DEC-773)", "R2A", 110000, 185000, 260000, "DEC-773", True),
    ("SOC 2 Type II annual audit (₹18-45 L per year) from the observation start", "R2A", 150000, 262500, 375000, "DEC-775", True),
    ("Enterprise-tier SLA topology uplift (recovered through Enterprise pricing)", "R2A+6", 55000, 102500, 150000, "DEC-774", True),
    ("Mandates, agentic commerce, payments, bids (IN region)", "R2B", 33774, 73314, 114540, "11.17b", True),
    ("Voice and recordings at 20,000 minutes per month", "R2B", 62734, 136184, 279725, "11.18c", True),
    ("Voice annual items (counsel review, relabelling, QA sample) per month", "R2B", 57500, 115000, 230000, "11.18c", True),
    ("Investment Automation I (KYC, e-sign, counsel retainer, AI)", "INV1", 59377, 121691, 234472, "11.16e", True),
    ("Investment Automation II (KYC/KYB, screening, counsel reviews, R10 reviewer, AI)", "INV2", 95787, 238957, 562871, "11.16d", True),
    ("EU stack hosting copy (DEC-772)", "R3a", 8400, 11025, 13650, "DEC-772", True),
    ("EU cell of the platform-decision lines", "R3a", 11500, 25000, 38500, "11.19b", True),
    ("EU increment for mandates and commerce", "R3a", 2500, 4650, 7300, "11.17b", True),
    ("Managed Kubernetes for IN and EU regional stacks", "R3a", 20000, 40000, 60000, "ASSUMPTION-1106; DEC-776", True),
    ("ISO 27001 surveillance audits (annual, per month)", "R3", 25000, 45833, 66667, "ASSUMPTION-1106; DEC-775", True),
    ("Four further regions UK, Middle East, APAC, US: hosting copy + managed Kubernetes", "R4a", 73600, 123250, 174600, "DEC-776; ASSUMPTION-1106", True),
    ("Global tax-engine subscription", "R4a", 15000, 37500, 60000, "ASSUMPTION-1106; DEC-776", True),
    ("Translation maintenance de, fr, ar", "R4a", 2250, 5625, 9000, "11.7b R1 pattern", True),
    ("ISO 27701 and 42001 surveillance audits (per month)", "R4", 33333, 66667, 100000, "ASSUMPTION-1106; DEC-775", True),
    ("V11 advanced running X1-X3 at steady state", "A1", 12546, 29382, 46218, "Part 9.10 9.10.7.2", True),
    ("AI improvement running A2-A4 (CR-AIM-01)", "A2", 4364, 12986, 21965, "11.13b", True),
    ("Sustain engineering team after the build: SQ-01 (employed) + one contract squad, 10 FTE (maintenance, Part 8.3)", "END", 1100000, 1375000, 1650000, "ASSUMPTION-1106", True),
    ("Compliance-automation tooling (optional; open-source evidence pipeline first)", "R2A", 0, 87500, 125000, "DEC-775", False),
]


def anchor_sprint(res, a):
    if a.startswith("S"):
        return int(a[1:])
    if a == "R2A+6":
        return res["gates"]["R2A"] + 6
    if a == "R3a":
        return res["build"]["R3"] + 1
    if a == "R4a":
        return res["build"]["R4"] + 1
    if a == "END":
        return max(row["k"] for row in res["log"] if row["nsq"]) + 1
    return res["gates"][a]


TOOL_PER_SQUAD = (115000, 144000, 173000)  # DEC-419/420 seats + build-agent API per active squad-month (ASSUMPTION-1106)


def running_by_year(res, idx, horizon_day=1095):
    """₹ per programme year of the recurring lines, month by month from the anchor sprint end."""
    out = {}
    lines = {}
    for nm, a, lo, ce, hi, src_, intot in RUN:
        v = (lo, ce, hi)[idx]
        st = sprint_dates(anchor_sprint(res, a))[1]
        d = st
        while day(d) <= horizon_day:
            y = year_of(d)
            if intot:
                out[y] = out.get(y, 0) + v
            lines[(nm, y)] = lines.get((nm, y), 0) + v
            d = d + dt.timedelta(days=30.4)
    # build tooling from the sprint log
    tool = {}
    for row in res["log"]:
        if row["nsq"]:
            y = year_of(row["e"])
            tool[y] = tool.get(y, 0) + row["nsq"] * TOOL_PER_SQUAD[idx] * MONTH_PER_SPRINT
    return out, lines, tool


def run_rate_by_release(idx):
    rr = {}
    for nm, a, lo, ce, hi, src_, intot in RUN:
        if not intot:
            continue
        key = {"S0": "R0", "S1": "R0", "R2A+6": "R2A", "R3a": "R3", "R4a": "R4", "END": "Sustain"}.get(a, a)
        rr[key] = rr.get(key, 0) + (lo, ce, hi)[idx]
    return rr


def lakh(x):
    return "₹%.2f L" % x


def cr(x):
    return "₹%.2f Cr" % (x / 100.0)


def md_tables():
    R = {nm: run(i) for nm, i in (("low", 0), ("central", 1), ("high", 2))}
    o = []
    P = lambda *a: o.append(" ".join(str(x) for x in a))
    # group roll-up
    P("### T1 group roll-up")
    P("| Group | Source | Gross L / C / H | Overlap removed L / C / H | Net L / C / H | Absorbed at refinement L / C / H | **Plan L / C / H** |")
    P("|---|---|---|---|---|---|---|")
    tot = [[0.0] * 3 for _ in range(5)]
    for g, v in NET.items():
        f = lambda t: " / ".join("%.1f" % x for x in t)
        P("| %s | %s | %s | %s | %s | %s | **%s** |" % (g, GROSS[g][0], f(v["gross"]), f(v["removed"]), f(v["net"]), f(v["absorbed"]), f(v["plan"])))
        for j, key in enumerate(("gross", "removed", "net", "absorbed", "plan")):
            for i in range(3):
                tot[j][i] += v[key][i]
    f = lambda t: " / ".join("%.0f" % x for x in t)
    P("| **Total** | | **%s** | **%s** | **%s** | **%s** | **%s** |" % tuple(f(t) for t in tot))
    # packages
    P("### T2 packages")
    for p, v in PKG.items():
        P("|", p, "|", PKG_NAMES[p], "|", " / ".join("%.0f" % x for x in v), "|")
    # gates
    P("### T3 gates")
    for rel in REL_PKGS:
        row = [rel]
        for nm in ("low", "central", "high"):
            r = R[nm]
            k = r["gates"][rel]
            row.append("S%d %s (Day %d)" % (k, fmt(gdate(k)), day(gdate(k))))
        row.append("build S%d %s" % (R["central"]["build"][rel], fmt(gdate(R["central"]["build"][rel]))))
        P("| " + " | ".join(row) + " |")
    # sprint table central
    P("### T4 sprints central")
    r = R["central"]
    rows = people_cost(r, 1)
    rowmap = {x["k"]: x for x in rows}
    for row in r["log"]:
        if not row["nsq"]:
            continue
        k = row["k"]
        used = sum(row["used"].values())
        pk = ", ".join("%s %.0f" % (p, v) for p, v in sorted(row["used"].items(), key=lambda x: -x[1]))
        x = rowmap[k]
        P("| S%d | %s – %s | %d–%d | %d | PI-%d%s | %d | %.1f + %.1f | %.0f | %.0f | %.0f | %s | %.0f |" % (
            k, row["s"].strftime("%d %b %Y"), row["e"].strftime("%d %b %Y"), day(row["s"]), day(row["e"]), row["wd"],
            row["pi"], " IP" if row["ip"] else "", row["nsq"], x["sq_fte"], x["oh_fte"], row["cap"] + row["baupd"],
            (row["cap"]) / 0.7, used / 0.7, pk, row["idle"] + row["baupd"]))
    # squads
    P("### T5 squads central")
    for sq in SQUADS:
        st = r["start"][sq[0]]
        lw = r["last"].get(sq[0])
        actives = [row["k"] for row in r["log"] if sq[0] in row["active"]]
        P("|", sq[0], "|", sq[1], "| S%d %s |" % (st, fmt(sprint_dates(st)[0])), "S%d %s |" % (max(actives), fmt(gdate(max(actives)))), sq[5], "|", ", ".join(sq[4]), "|")
    # fte by phase: per sprint summary
    P("### T6 fte per sprint central")
    peak = max(rows, key=lambda x: x["sq_fte"] + x["oh_fte"])
    P("peak", peak["k"], peak["sq_fte"], peak["oh_fte"])
    # costs
    P("### T7 people cost by release (₹ lakh) L/C/H")
    alloc = {}
    for nm, i in (("low", 0), ("central", 1), ("high", 2)):
        rr = people_cost(R[nm], i)
        br, by, bry = alloc_cost(rr)
        alloc[nm] = (br, by, bry, rr)
    keys = list(REL_PKGS) + ["Sustain"]
    for kk in keys:
        P("|", kk, "|", " | ".join("%.1f" % alloc[nm][0].get(kk, 0) for nm in ("low", "central", "high")), "|")
    P("| total |", " | ".join("%.1f" % sum(alloc[nm][0].values()) for nm in ("low", "central", "high")), "|")
    P("### T8 people cost by year")
    for y in ("PY1", "PY2", "PY3"):
        P("|", y, "|", " | ".join("%.1f" % alloc[nm][1].get(y, 0) for nm in ("low", "central", "high")), "|")
    P("### T8b fte-months")
    for nm in ("low", "central", "high"):
        rr = alloc[nm][3]
        P(nm, "squad FTE-months %.1f overhead FTE-months %.1f" % (sum(x["sq_fte"] for x in rr) * MONTH_PER_SPRINT, sum(x["oh_fte"] for x in rr) * MONTH_PER_SPRINT))
    # external
    P("### T9 external by release")
    ext = {}
    for nm_, a, lo, ce, hi, s_ in EXT:
        e = ext.setdefault(a, [0, 0, 0])
        e[0] += lo; e[1] += ce; e[2] += hi
    for a, v in ext.items():
        P("|", a, "|", " / ".join("%.2f" % x for x in v), "|")
    P("ext total", [round(sum(v[i] for v in ext.values()), 2) for i in range(3)])
    P("### T9b external by year")
    for nm, i in (("low", 0), ("central", 1), ("high", 2)):
        ey = {}
        for nm_, a, lo, ce, hi, s_ in EXT:
            y = year_of(gdate(R[nm]["gates"][a]))
            ey[y] = ey.get(y, 0) + (lo, ce, hi)[i]
        P(nm, {k: round(v, 2) for k, v in ey.items()})
    # running
    P("### T10 running by year")
    for nm, i in (("low", 0), ("central", 1), ("high", 2)):
        ry, lines, tool = running_by_year(R[nm], i)
        P(nm, {k: round(v / 1e5, 2) for k, v in ry.items()}, "tooling", {k: round(v / 1e5, 2) for k, v in tool.items()})
    P("### T11 run-rate by release (₹/month)")
    for nm, i in (("low", 0), ("central", 1), ("high", 2)):
        P(nm, run_rate_by_release(i), "steady total", sum(run_rate_by_release(i).values()))
    P("### T12 activation sprint of running anchors (central)")
    for a in ("R1", "R2A", "R2A+6", "R2B", "INV1", "INV2", "R3a", "R3", "R4a", "R4", "A1", "A2"):
        k = anchor_sprint(R["central"], a)
        P(a, "S%d" % k, fmt(gdate(k)))
    # scenarios
    P("### T13 DEC-420 scenarios")
    for prod in (1.0, 1.11, 1.25, 1.43):
        rr = run(1, prod=prod)
        P("prod", prod, " | ".join("%s %s" % (k, fmt(gdate(v))) for k, v in sorted(rr["gates"].items(), key=lambda x: x[1])))
        pc = people_cost(rr, 1)
        P("   people cost central", round(sum(x["sq_cost"] + x["oh_cost"] for x in pc), 1))
    return "\n".join(o)



def report():
    Rc = run(1)
    Rl, Rh = run(0), run(2)
    o = []
    P = lambda *a: o.append(" ".join(str(x) for x in a))
    P("### B1 people cost, plan-of-record schedule, rates L/C/H (₹ lakh)")
    allocs = []
    for i in range(3):
        rr = people_cost(Rc, i)
        allocs.append((alloc_cost(rr), rr))
    keys = list(REL_PKGS) + ["Sustain"]
    for kk in keys:
        P("|", kk, "|", " | ".join("%.1f" % allocs[i][0][0].get(kk, 0) for i in range(3)), "|")
    P("| total |", " | ".join("%.1f" % sum(allocs[i][0][0].values()) for i in range(3)), "|")
    for y in ("PY1", "PY2", "PY3"):
        P("| year", y, "|", " | ".join("%.1f" % allocs[i][0][1].get(y, 0) for i in range(3)), "|")
    for i in range(3):
        rr = allocs[i][1]
        P("rate", i, "squad FTE-months %.1f overhead FTE-months %.1f sq cost %.1f oh cost %.1f" % (
            sum(x["sq_fte"] for x in rr) * MONTH_PER_SPRINT, sum(x["oh_fte"] for x in rr) * MONTH_PER_SPRINT,
            sum(x["sq_cost"] for x in rr), sum(x["oh_cost"] for x in rr)))
    rr = allocs[1][1]
    peak = max(rr, key=lambda x: x["sq_fte"] + x["oh_fte"])
    P("peak S%d squads %.1f overhead %.2f" % (peak["k"], peak["sq_fte"], peak["oh_fte"]))
    # by phase
    P("### B2 FTE by phase (central schedule)")
    phases = [("P0 Foundation", 0, 2), ("PI-1", 3, 8), ("PI-2", 9, 14), ("PI-3", 15, 20), ("PI-4", 21, 26),
              ("PI-5", 27, 32), ("PI-6", 33, 38), ("PI-7", 39, 44)]
    for nm, a, b in phases:
        xs = [x for x in rr if a <= x["k"] <= b]
        if not xs:
            continue
        P("|", nm, "| S%d–S%d |" % (a, min(b, max(x["k"] for x in xs))), "%.1f | %.1f | %.1f | %.1f | %d–%d |" % (
            sum(x["sq_fte"] for x in xs) / len(xs), max(x["sq_fte"] for x in xs),
            sum(x["oh_fte"] for x in xs) / len(xs), max(x["sq_fte"] + x["oh_fte"] for x in xs),
            min(x["nsq"] for x in xs), max(x["nsq"] for x in xs)))
    P("### B2b overhead roles at S22")
    for nm_, f, c in overhead_roles(22, 11):
        P("|", nm_, "|", f, "|", c, "|")
    P("### B3 effort-risk view at central rates")
    for nm, R in (("low", Rl), ("high", Rh)):
        x = people_cost(R, 1)
        P(nm, "%.1f" % sum(y["sq_cost"] + y["oh_cost"] for y in x))
    P("### B4 external by year on central dates")
    for i in range(3):
        ey = {}
        for nm_, a, lo, ce, hi, s_ in EXT:
            y = year_of(gdate(Rc["gates"][a] if a != "A3" else Rc["gates"]["A3"]))
            ey[y] = ey.get(y, 0) + (lo, ce, hi)[i]
        P(i, {k: round(v, 2) for k, v in sorted(ey.items())})
    P("### B5 running by year on central dates (₹ lakh)")
    for i in range(3):
        ry, lines, tool = running_by_year(Rc, i)
        P(i, {k: round(v / 1e5, 2) for k, v in sorted(ry.items())}, "tooling", {k: round(v / 1e5, 2) for k, v in sorted(tool.items())})
    P("### B6 running lines PY1/PY2/PY3 central (₹ lakh)")
    ry, lines, tool = running_by_year(Rc, 1)
    for nm, a, lo, ce, hi, s_, intot in RUN:
        P("|", nm, "|", a, "|", " | ".join("%.2f" % (lines.get((nm, y), 0) / 1e5) for y in ("PY1", "PY2", "PY3")), "|")
    P("### B7 scenarios")
    for prod in (1.0, 1.11, 1.25, 1.43):
        r = run(1, prod=prod)
        pc = people_cost(r, 1)
        P(prod, " ; ".join("%s %s (Day %d)" % (k, fmt(gdate(v)), day(gdate(v))) for k, v in sorted(r["gates"].items(), key=lambda x: x[1])),
          "| cost %.1f" % sum(x["sq_cost"] + x["oh_cost"] for x in pc),
          "| FTE-months %.1f" % (sum(x["sq_fte"] + x["oh_fte"] for x in pc) * MONTH_PER_SPRINT))
    return "\n".join(o)


if __name__ == "__main__":
    print(md_tables())
    print(report())
