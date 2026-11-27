#!/usr/bin/env python3
"""Part 9.5 effort model: gross enhancement effort by group, de-duplication,
MoSCoW triage and release placement. Prints the tables used in Part 9.5 §9.5.2.

Units: person-days (pd). Conversions: SP x 0.7 = pd (Part 8.1 §8.1.6.1).
Ranges: low / high; central = midpoint.
"""
SPPD = 0.7

def sp(lo, hi):
    return (round(lo * SPPD, 2), round(hi * SPPD, 2))

# ---------------------------------------------------------------------------
# 1. Gross effort per group, as stated by the group or derived from its own
#    story tables (basis column). Non-engineering effort listed separately.
# ---------------------------------------------------------------------------
B_central = 88 * SPPD
GROSS = {
    # group: (low, high, basis)
    "A": (43.0, 72.0, "Part 2.6 §2.6.5.9.2 table (stated)"),
    "B": (round(B_central * 0.75, 2), round(B_central * 1.25, 2),
          "Part 3.4 §3.4.5.8: 88 SP = 61.6 pd central; band ±25% (Part 8.1 band width)"),
    "C": sp(23, 37) ,  # 8 stories, SP estimated in this part
    "D": sp(49, 60),   # Part 3.5b §3.5.5.11.2 points column
    "E": (17.2, 28.2, "6 stories 16-26 SP (estimated here) + schema delta 6-10 pd"),
    "F": (68.0, 110.0, "Part 7.4b §7.4.5.11 (stated: Must 30-48, Should/Could 38-62)"),
    "G": (16.0, 30.0, "estimated here: harness, screen template, UAT packs, 45 TCs"),
    "H": (round(sp(17, 27)[0] + 14.5 + 10, 2), round(sp(17, 27)[1] + 49.4 + 20, 2),
          "6 stories 17-27 SP + UX-TASK-FIELDS residual 14.5-49.4 + review effort 10-20"),
    "I": (29.5, 54.0, "Part 4.4b §4.4.5.10 (stated)"),
    "J": sp(63, 103),  # Part 8.3b/c story tables (22 stories)
}
GROSS["C"] = (GROSS["C"][0], GROSS["C"][1], "8 stories, 23-37 SP estimated here")
GROSS["D"] = (GROSS["D"][0], GROSS["D"][1], "16 stories, 49-60 SP (Part 3.5b)")
GROSS["J"] = (GROSS["J"][0], GROSS["J"][1], "22 stories, 63-103 SP (Part 8.3b/c tables)")

NON_ENG = {
    "A": (3, 5, "benchmark labelling (Part 2.6)"),
    "J": (14.5, 28, "training content and delivery, Year 1 (Part 8.3b §8.3.5.11)"),
    "H": (5, 10, "Founder/PO share of decision and trace approval (estimated here)"),
}

# ---------------------------------------------------------------------------
# 2. Package register (net of cross-group de-duplication).
#    (id, group, title, moscow, place, low, high, supports)
#    place: R1, R2, SG (scale gate, W6 window), W6
# ---------------------------------------------------------------------------
def spr(lo, hi):
    return sp(lo, hi)

def b(spv):  # group B single SP value with ±25% band
    return (round(spv * SPPD * 0.75, 2), round(spv * SPPD * 1.25, 2))

P = []
def add(pid, g, title, m, place, rng, sup):
    P.append((pid, g, title, m, place, rng[0], rng[1], sup))

# Group A (net 39.5-66)
add("A-1", "A", "Coverage ledger and geography triple (FR-ENH-A-001, -002)", "Should", "W6", (4, 6.5), "BR-M07; DEC-001 provenance")
add("A-2", "A", "Coverage planner and playbook registry SPB (FR-ENH-A-003, -004)", "Should", "W6", (4, 6.5), "BR-M07, BR-M08")
add("A-3", "A", "Discovery benchmark (FR-ENH-A-005)", "Should", "W6", (2, 3.5), "DEC-001; OKPI-15")
add("A-4", "A", "Reply taxonomy union and publication proof (FR-ENH-A-008, -009)", "Must", "R1", (4, 7), "BRL-SEQ-02 stop; OKPI-35")
add("A-5", "A", "Governance rules: sub-roles, bulk preview, hold record (BRL-ENH-A-07…12, FR-ENH-A-019, -020)", "Must", "R1", (4.5, 7.5), "isolation; OKPI-08, OKPI-35")
add("A-6", "A", "Managed-service delegation R21 (FR-ENH-A-015)", "Should", "W6", (3, 5), "BR-SVC (Should)")
add("A-7", "A", "Jurisdiction activation record (FR-ENH-A-014)", "Must", "R1", (1.5, 2.5), "compliance; OKPI-35")
add("A-8", "A", "AOP, experiments, weekly review, outcome economics (FR-ENH-A-010…013)", "Should", "W6", (7.5, 12.5), "BR-M30, BR-M61")
add("A-9", "A", "Website legal disclosure block (FR-ENH-A-017)", "Must", "R1", (1, 2), "compliance; BR-WEB")
add("A-10", "A", "Relationship timeline projection (FR-ENH-A-016)", "Should", "W6", (3, 5), "BR-M23")
add("A-11", "A", "Partnership-fit scoring version (FR-ENH-A-007)", "Could", "W6", (1, 2), "DEC-011")
add("A-12", "A", "UAT packs and fixtures FX-A-01…06", "Must", "R1", (4, 6), "BR-QA; OKPI-17")

# Group B (net 56 SP of 88)
add("B-1", "B", "Recovery classes RC-1…3, class-ordered restore (US-21-EB02)", "Must", "R1", b(5), "OKPI-18, -19, -32")
add("B-2", "B", "Dashboard first render ≤ 2 s (US-17-EB01)", "Must", "R1", b(3), "OKPI-05")
add("B-3", "B", "Adapter port v2: estimate/execute/reconcile/health (US-01-EB01)", "Must", "R1", b(5), "OKPI-11, -12")
add("B-4", "B", "Four DRF permission base classes (US-01-EB02)", "Must", "R1", b(3), "OKPI-01, -02")
add("B-5", "B", "Stable public route map (US-19-EB01)", "Should", "W6", b(3), "BR-WEB")
add("B-6", "B", "Reply event without raw text (US-08-EB01 remainder)", "Must", "R1", b(2), "privacy; NFR-078")
add("B-7", "B", "Outbound intent expiry (US-08-EB02)", "Must", "R1", b(3), "OKPI-35")
add("B-8", "B", "Product-event allowlist (US-03-EB01)", "Could", "W6", b(5), "ADR-105 (off by default)")
add("B-9", "B", "Workflow execution policy and 12 activation gates (US-18-EB01, -EB02)", "Must", "R1", b(10), "OKPI-08, -35")
add("B-10", "B", "Regression matrix: zero-tolerance scenarios S2/S3/S5/S7 (US-18-EB03 part)", "Must", "R1", b(4), "OKPI-16")
add("B-11", "B", "Regression matrix: remaining scenarios (US-18-EB03 part)", "Should", "W6", b(4), "BR-QA")
add("B-12", "B", "Daily and data-incident runbooks (US-21-EB03 remainder)", "Must", "R1", b(2), "operations")
add("B-13", "B", "Critical-branch coverage gate (US-21-EB04)", "Must", "R1", b(3), "DEC-178")
add("B-14", "B", "Product-isolation tests with investor tokens (US-01-EB04)", "Must", "R1", b(3), "OKPI-01, NFR-031")
add("B-15", "B", "PD actual-vs-estimate tracking in tool (US-21-EB06 part)", "Should", "W6", b(1), "delivery control")

# Group C (net)
add("C-1", "C", "Optimization Intelligence panel as the UI of the J scorecard (US-17-EC01, half)", "Should", "W6", spr(2.5, 4), "OKPI reporting")
add("C-2", "C", "Legacy screen identity labels (US-01-EC01 part; alias work moved to X-3)", "Should", "W6", spr(1, 2), "traceability")
add("C-3", "C", "Related-screen navigation with scope carry and re-authorization (US-17-EC02)", "Should", "W6", spr(3, 5), "OKPI-01")
add("C-4", "C", "Status footer and focus restoration (US-17-EC03)", "Must", "R1", spr(2, 3), "OKPI-23")
add("C-5", "C", "Honest adapter and cost display (US-04-EC01)", "Should", "W6", spr(3, 5), "BR-M53")
add("C-6", "C", "Design and delivery evidence pack per wave (US-21-EC01)", "Should", "W6", spr(2, 3), "OKPI-17")
add("C-7", "C", "Responsive and viewport matrix (US-17-EC04)", "Must", "R1", spr(3, 5), "OKPI-23")

# Group D (net)
add("D-1", "D", "Contract approval gate and evidence (US-21-ED01, merged with H-2)", "Must", "R1", spr(4, 6), "no unapproved contract; OKPI-17")
add("D-2", "D", "Catalogue integrity and source traceability (US-21-ED02)", "Must", "R1", spr(3, 5), "OKPI-20")
add("D-3", "D", "Idempotent replay audit and error codes (US-01-ED01)", "Must", "R1", spr(2, 3), "OKPI-07, -08")
add("D-4", "D", "Per-operation performance budgets (US-21-ED03)", "Should", "W6", spr(3, 5), "NFR-039")
add("D-5", "D", "Adapter command/result envelope with budget reservation (US-01-ED02)", "Must", "R1", spr(5, 5), "OKPI-11, -12")
add("D-6", "D", "External portal grants (US-19-ED01)", "Must", "R1", spr(3, 3), "OKPI-01, ABAC-09")
add("D-7", "D", "Portal upload with checksum (US-19-ED02)", "Must", "R1", spr(2, 2), "integrity; NFR-021")
add("D-8", "D", "Website ingress allowlist and domain disable (US-19-ED03)", "Must", "R1", spr(3, 3), "OKPI-02")
add("D-9", "D", "Service finance completeness (US-20-ED01)", "Must", "R2", spr(5, 5), "OKPI-22")
add("D-10", "D", "Applicant draft read and offboarding request (US-20-ED02)", "Should", "W6", spr(2, 2), "BR-SVC")
add("D-11", "D", "Intelligence configuration revisions (US-05-ED01)", "Should", "W6", spr(3, 5), "BR-M07")
add("D-12", "D", "Message status, WABA list, assistant settings (US-08-ED01)", "Should", "W6", spr(3, 3), "BR-M28")
add("D-13", "D", "Resume workflow with PDP recheck; create template (US-18-ED01)", "Must", "R1", spr(3, 3), "OKPI-35; BRL-AUT-05")
add("D-14", "D", "Pilot list and buy-order acceptance (US-16-ED01)", "Must", "R2", spr(3, 3), "OKPI-22; BRL-ORD")
add("D-15", "D", "Offline privacy request intake; eval cases (US-03-ED01)", "Must", "R1", spr(2, 3), "DPDP; NFR-075")
add("D-16", "D", "Forecast assumption revision (US-17-ED01)", "Could", "W6", spr(2, 2), "BR-M60 (Could)")

# Group E
add("E-1", "E", "Startup provisioning from approved business template (US-01-EE01)", "Must", "R1", spr(3, 5), "BR-TENANT; fixes dangling template_ref")
add("E-2", "E", "Service request entity and flow (US-20-EE01; replaces H story)", "Must", "R2", spr(3, 5), "fixes FR-W34/API-440 defect")
add("E-3", "E", "Fulfilment milestones (US-14-EE01)", "Should", "W6", spr(3, 5), "BR-M46")
add("E-4", "E", "No-dispatch restore drill and RD checklist (US-21-EE01)", "Must", "R1", spr(2, 3), "OKPI-18, -19")
add("E-5", "E", "Migration gate on open schema decisions (US-21-EE02)", "Must", "R1", spr(2, 3), "data integrity")
add("E-6", "E", "Tenant offboarding runbook OFB-1…10 (US-20-EE02)", "Must", "R2", spr(3, 5), "OKPI-01; DPDP erasure")
add("E-7", "E", "Schema delta: 113 columns, 54 keys, 12 checks, exposure class CI, order_kind", "Must", "R1", (6, 10), "OKPI-02; integrity")

# Group F
add("F-1", "F", "AI Must bundle: envelope v2, contracts, ACL pre/post retrieval, revocation, cache key, procurement and licence gates, budget per surface, paid fallback off (19 FRs)", "Must", "R1", (30, 48), "OKPI-01, -11, -12, -13, -14; DEC-007")
add("F-2", "F", "Adapter lifecycle incl. Retire (FR-ENH-F-015)", "Should", "W6", (3, 5), "BR-M54")
add("F-3", "F", "Replacement economics on A012 (FR-ENH-F-018)", "Should", "W6", (2, 4), "BR-M53")
add("F-4", "F", "Provider invoice reconciliation AU-048 (FR-ENH-F-019)", "Should", "W6", (4, 6), "OKPI-21 (not mandatory)")
add("F-5", "F", "Tender amendment detection AU-052 (FR-ENH-F-024)", "Should", "W6", (3, 5), "BR-M44")
add("F-6", "F", "Event registration AU-051 (FR-ENH-F-025)", "Should", "W6", (3, 5), "BR-M40 (Could; spilled)")
add("F-7", "F", "Meeting-notes summarizer AG-037 (FR-ENH-F-026)", "Should", "W6", (5, 8), "BR-M37")
add("F-8", "F", "Retention next-best-action AG-038 (FR-ENH-F-027)", "Could", "W6", (4, 7), "BR-M50")
add("F-9", "F", "A113 seed library: 100 use cases, 20 templates, 13 node types (FR-ENH-F-028)", "Should", "W6", (7, 11), "FR-A113")

# Group G
add("G-1", "G", "Operation-contract class harness (17 classes), execution-status field, SM-UT-037/049/050", "Must", "R1", (6, 10), "OKPI-16")
add("G-2", "G", "Screen contract test template and 3-viewport route crawl", "Must", "R1", (4, 8), "OKPI-23")
add("G-3", "G", "UAT packs UAT-PK-MKT (R1) and UAT-PK-CS (R2)", "Must", "R1", (2, 4), "BR-QA")
add("G-4", "G", "Automation of TC-ENH-G-001…045", "Must", "R1", (4, 8), "OKPI-16")

# Group H
add("H-1", "H", "QC register and layer sign-off (US-21-EH04, register part)", "Must", "R1", (1.05, 1.75), "OKPI-17")
add("H-2", "H", "SPDEC decision queue (US-21-EH03)", "Must", "R1", spr(3, 5), "no unapproved contract")
add("H-3", "H", "Go-live handover and access inventory (US-21-EH02)", "Must", "R1", spr(2, 3), "security; GL checklist")
add("H-4", "H", "Shared field components and read-only enforcement (US-17-EH01)", "Must", "R1", spr(5, 8), "integrity of computed fields")
add("H-5", "H", "Decision and trace approval effort, engineering and QA share (100% trace approval)", "Must", "R1", (10, 20), "OKPI-20")

# Group I
add("I-1", "I", "Coding-standard tooling: Semgrep SG-01…12, ESLint scope rule, diff coverage, PR template", "Must", "R1", (4, 7), "OKPI-01, -03")
add("I-2", "I", "Typed configuration, fail-closed start, manifest drift (AL-55)", "Must", "R1", (3, 5), "safety")
add("I-3", "I", "Reserved control and finance queues", "Must", "R1", (2, 4), "emergency stop ≤ 60 s; OKPI-07")
add("I-4", "I", "Ordered deploy, smoke SMK-01…14, activation canary", "Must", "R1", (3, 5), "OKPI-16")
add("I-5", "I", "Release-gate validator RGV (also replaces J manifest validator)", "Must", "R1", (4, 7), "OKPI-16, -17")
add("I-6", "I", "Alerts AL-50…58, metrics, runbooks RB-016…018", "Must", "R1", (3, 6), "OKPI-22")
add("I-7", "I", "Workload profiles WP-01/03 and LT-ENH-I runs for R1/R2", "Must", "R1", (3, 5), "OKPI-05, -27")
add("I-8", "I", "Growth profile WP-02 (250 sessions, 1 M opportunities) and growth drill", "Must", "SG", (2, 4), "OKPI-26, -32 (scale gate)")
add("I-9", "I", "Budget pause/resume API-ENH-I-01/02", "Should", "W6", (1.5, 3), "BR-M53")
add("I-10", "I", "Export manifest hash", "Must", "R1", (1, 2), "DPDP; OKPI-04")
add("I-11", "I", "Pen-test rules of engagement and severity overlay", "Must", "R1", (1, 2), "OKPI-03")

# Group J
add("J-1", "J", "Training-gated permissions, training record, training tenant (US-01-EJ01, -EJ02, US-21-EJ01)", "Must", "R1", spr(9, 15), "safety; GL-B03")
add("J-2", "J", "Contextual help links and training banner (US-17-EJ01)", "Should", "W6", spr(2, 3), "adoption")
add("J-3", "J", "Technical-debt register (US-21-EJ02)", "Should", "W6", spr(2, 3), "maintainability")
add("J-4", "J", "Feature retirement checks (US-21-EJ03)", "Could", "W6", spr(3, 5), "lifecycle")
add("J-5", "J", "Change-impact record in CI (US-21-EJ09)", "Must", "R1", spr(3, 5), "OKPI-20")
add("J-6", "J", "Optimization register and scorecard (US-21-EJ04)", "Should", "W6", spr(5, 8), "optimization model")
add("J-7", "J", "OKPI registry and measurements (US-17-EJ02)", "Must", "R1", spr(3, 5), "21 mandatory OKPIs")
add("J-8", "J", "Operational projection freshness ≤ 60 s (US-17-EJ03)", "Must", "R1", spr(3, 5), "OKPI-28")
add("J-9", "J", "Spend alerts 70/90/100 (US-04-EJ01)", "Must", "R1", spr(2, 3), "OKPI-12")
add("J-10", "J", "SLA schedule (US-20-EJ01)", "Should", "W6", spr(3, 5), "DEC-044 / paid support")
add("J-11", "J", "Monthly service report (US-20-EJ02)", "Should", "W6", spr(3, 5), "BR-SVC")
add("J-12", "J", "Managed-service scope, merged with A-6 (US-20-EJ03, half)", "Should", "W6", spr(1.5, 2.5), "BR-SVC")
add("J-13", "J", "Onboarding checklist, due diligence and timer (US-20-EJ04)", "Must", "R2", spr(3, 5), "KPI-25; compliance")
add("J-14", "J", "Offboarding verification job (US-20-EJ05, half; merged with E-6)", "Must", "R2", spr(1.5, 2.5), "OKPI-01")
add("J-15", "J", "Tenant economics and cohorts (US-20-EJ06)", "Should", "W6", spr(3, 5), "KPI-23")

# Cross-cutting packages created by the Part 9.5 decisions
add("X-1", "X", "Absolute discounts with effective-% approval routing (DEC-180)", "Must", "R2", (1, 2), "financial integrity; DEC-038")
add("X-2", "X", "Investor/fundraising wording scrub and negative regression strings (DEC-177)", "Must", "R1", (0.5, 1), "DEC-002")
add("X-3", "X", "API path canon: mount source paths, rename derived paths, /control dispatcher, header/body compatibility (DEC-170…173)", "Must", "R1", (3, 6), "BRD §9")

F_NORM = 0.7  # Part 7.4b used 1 pd = 1 SP; Part 8.1 converts 1 SP = 0.7 pd
P = [ (r[0],r[1],r[2],r[3],r[4],round(r[5]*F_NORM,2),round(r[6]*F_NORM,2),r[7]) if r[1]=="F" else r for r in P]
ABSORB = (0.20, 0.15, 0.10)  # share absorbed into baseline stories at refinement: low, central, high

# ---------------------------------------------------------------------------
def tot(rows):
    lo = sum(r[5] for r in rows); hi = sum(r[6] for r in rows)
    return round(lo, 1), round((lo + hi) / 2, 1), round(hi, 1)

import datetime, math
DAY1 = datetime.date(2026, 12, 7)
def day(n): return (DAY1 + datetime.timedelta(n - 1)).strftime("%a %d %b %Y")

C0 = 48.4 * SPPD            # pd per sprint at 4.5 engineering FTE (Part 8.1 §8.1.4.6)
PER_FTE = C0 / 4.5          # 7.53 pd per FTE per sprint
ONBOARD = 0.85              # 15% onboarding/coordination loss for added engineers
SPRINTS_TO_R1 = 8           # S3…S10 inclusive: sprints in which added engineers work before Day 152

def absorbed(t):
    return tuple(round(t[i] * (1 - ABSORB[i]), 1) for i in range(3))

def slip_days(delta_pd, extra_fte, sprints_avail):
    e = extra_fte * PER_FTE * ONBOARD
    k = max(0.0, (delta_pd - sprints_avail * e) / (C0 + e))
    return k, int(math.ceil(k * 14 / 7.0) * 7)   # weekly granularity, Friday gates

if __name__ == "__main__":
    print("== Gross by group")
    gl = gh = 0
    for g, v in GROSS.items():
        lo, hi = v[0], v[1]
        if g == "F": lo, hi = lo * 0.7, hi * 0.7
        print(g, round(v[0], 1), round(v[1], 1), "normalised", round(lo,1), round((lo+hi)/2,1), round(hi,1), v[2])
        gl += lo; gh += hi
    print("GROSS(normalised)", round(gl, 1), round((gl + gh) / 2, 1), round(gh, 1))
    print("== Net by group")
    nl = nh = 0
    for g in "ABCDEFGHIJX":
        rows = [r for r in P if r[1] == g]
        t = tot(rows); gr = GROSS.get(g, (0, 0, ""))
        glo, ghi = gr[0], gr[1]
        if g == "F": glo, ghi = glo*0.7, ghi*0.7
        print(g, t, "removed", round(glo - t[0], 1), round(ghi - t[2], 1))
        nl += t[0]; nh += t[2]
    net = (round(nl,1), round((nl+nh)/2,1), round(nh,1))
    print("NET", net, "after absorption", absorbed(net))
    res = {}
    for m in ("Must", "Should", "Could"):
        for pl in ("R1", "R2", "SG", "W6"):
            rows = [r for r in P if r[3] == m and r[4] == pl]
            if rows:
                res[(m,pl)] = tot(rows)
                print(m, pl, len(rows), tot(rows), "absorbed", absorbed(tot(rows)))
    mr1 = absorbed(res[("Must","R1")]); mr2 = absorbed(res[("Must","R2")])
    print("== Options (central and high)")
    for name, fte in (("Option 1", 0), ("Option 2a", 1), ("Option 2b", 2)):
        for idx, lab in ((1, "central"), (2, "high"), (0, "low")):
            k1, d1 = slip_days(mr1[idx], fte, SPRINTS_TO_R1)
            # R2: two sprints S11-S12 between R1 and R2 in the plan
            k2, d2 = slip_days(mr2[idx], fte, 2)
            r1 = 152 + d1; r2 = 180 + d1 + d2; w5 = r2 + 21
            print(name, lab, "R1 slip", round(k1,2), d1, "R1", r1, day(r1), "R2", r2, day(r2), "W5", w5, day(w5))
    import sys
    if len(sys.argv) > 1:
        for r in P:
            print("| {} | {} | {} | {} | {:.1f}–{:.1f} | {:.1f} | {} |".format(r[0], r[2], r[3], r[4], r[5], r[6], (r[5]+r[6])/2, r[7]))
