#!/usr/bin/env python3
"""Part 11.17 (Group P) combinatorial model generator.

Generates t-way covering arrays (greedy, deterministic seed) for the three
safety-/money-/law-critical models of Part 11.17 and writes Markdown fragments:
  - 3-way test-case tables (TC-V12-P-###) with oracle-computed expected results
  - 2-way (pairwise) Gherkin Examples rows for the stories (Scenario Outline)
  - exhaustive enumeration for the small kill-switch x scope model (<= 64)
Usage: python3 -I p_combinatorial.py <out_dir>
"""
import itertools, random, sys, json, os

def covering_array(params, t, seed=17, candidates=60, valid=None):
    """Greedy t-way covering array. `valid(partial_dict)` returns False for a
    forbidden partial assignment (constraint handling: forbidden tuples are not
    required and no generated row contains one)."""
    names = list(params)
    doms = [params[n] for n in names]
    k = len(names)
    rng = random.Random(seed)
    ok = (lambda d: True) if valid is None else valid
    uncovered = set()
    for cols in itertools.combinations(range(k), t):
        for vals in itertools.product(*[range(len(doms[c])) for c in cols]):
            if ok({names[c]: doms[c][v] for c, v in zip(cols, vals)}):
                uncovered.add((cols, vals))
    rows = []
    def gain(row):
        g = 0
        for cols in itertools.combinations(range(k), t):
            if (cols, tuple(row[c] for c in cols)) in uncovered:
                g += 1
        return g
    while uncovered:
        # seed candidate from one uncovered tuple, fill rest greedily
        best, bestg = None, -1
        pool = list(uncovered)
        for _ in range(candidates):
            cols, vals = pool[rng.randrange(len(pool))]
            row = [None] * k
            for c, v in zip(cols, vals):
                row[c] = v
            order = [i for i in range(k) if row[i] is None]
            rng.shuffle(order)
            for i in order:
                bv, bg = None, -1
                for v in range(len(doms[i])):
                    row[i] = v
                    part = {names[j]: doms[j][row[j]] for j in range(k) if row[j] is not None}
                    if not ok(part):
                        continue
                    tmp = [x if x is not None else 0 for x in row]
                    g = gain(tmp)
                    if g > bg:
                        bv, bg = v, g
                row[i] = bv if bv is not None else 0
            g = gain(row)
            if g > bestg:
                best, bestg = list(row), g
        rows.append(best)
        for cols in itertools.combinations(range(k), t):
            uncovered.discard((cols, tuple(best[c] for c in cols)))
    return [{n: doms[i][r[i]] for i, n in enumerate(names)} for r in rows]

def total(params):
    p = 1
    for v in params.values():
        p *= len(v)
    return p

def tuples(params, t):
    s = 0
    for cols in itertools.combinations(list(params.values()), t):
        p = 1
        for c in cols:
            p *= len(c)
        s += p
    return s

# ---------------------------------------------------------------- Model M
M = {
    "AUT": ["L0", "L1", "L2", "L3", "L4"],
    "MST": ["Draft", "PendingSecondApproval", "Active", "Suspended", "Expired", "Revoked", "Exhausted"],
    "VAL": ["BelowCap", "AtCap", "AbovePerActionCap", "CrossesAggregateCap"],
    "CPT": ["AllowlistedVerified", "CredentialExpired", "NotAllowlisted", "CounterpartyRevoked"],
    "JUR": ["IN-Approved", "EU-Approved", "Pack-Draft", "Pack-Missing"],
    "PAY": ["UPI-AutoPay", "e-NACH", "Card-MIT-Token", "SEPA-DD", "No-Payment"],
    "WIN": ["Inside", "BeforeStart", "AfterEnd", "OutsideDailyHours"],
    "KS":  ["Off", "Mandate", "Tenant", "Platform"],
}
PAY_OK = {"IN-Approved": {"UPI-AutoPay", "e-NACH", "Card-MIT-Token", "No-Payment"},
          "EU-Approved": {"SEPA-DD", "Card-MIT-Token", "No-Payment"}}

def oracle_m(r):
    """Returns (verdict, reason, provider_calls, ledger) per §11.17.5.9 PDP order."""
    if r["AUT"] == "L0":
        return ("RECORD_ONLY", "MANUAL_ACTION_L0", 0, "none")
    if r["KS"] != "Off":
        return ("BLOCKED", "KILL_SWITCH_" + r["KS"].upper(), 0, "none")
    if r["JUR"] in ("Pack-Draft", "Pack-Missing"):
        return ("HOLD", "JURISDICTION_PACK_NOT_APPROVED", 0, "none")
    if r["PAY"] not in PAY_OK[r["JUR"]]:
        return ("DENY", "PAYMENT_METHOD_NOT_PERMITTED", 0, "none")
    if r["CPT"] in ("NotAllowlisted", "CounterpartyRevoked"):
        return ("DENY", "COUNTERPARTY_NOT_TRUSTED", 0, "none")
    if r["CPT"] == "CredentialExpired":
        return ("HOLD", "COUNTERPARTY_CREDENTIAL_EXPIRED", 0, "none")
    if r["AUT"] == "L1":
        return ("HOLD", "DRAFT_AWAITS_HUMAN_DECISION_L1", 0, "none")
    if r["AUT"] == "L2":
        return ("ROUTE", "EXACT_ITEM_APPROVAL_REQUIRED_L2", 0, "none")
    m = {"Draft": ("HOLD", "MANDATE_NOT_ACTIVE"), "PendingSecondApproval": ("HOLD", "MANDATE_NOT_ACTIVE"),
         "Suspended": ("HOLD", "MANDATE_SUSPENDED"), "Expired": ("DENY", "MANDATE_EXPIRED"),
         "Revoked": ("DENY", "MANDATE_REVOKED"), "Exhausted": ("DENY", "MANDATE_EXHAUSTED")}
    if r["MST"] != "Active":
        v, why = m[r["MST"]]
        return (v, why, 0, "none")
    w = {"BeforeStart": ("HOLD", "MANDATE_NOT_YET_EFFECTIVE"), "AfterEnd": ("DENY", "MANDATE_WINDOW_ENDED"),
         "OutsideDailyHours": ("DEFER", "OUTSIDE_DAILY_WINDOW")}
    if r["WIN"] != "Inside":
        v, why = w[r["WIN"]]
        return (v, why, 0, "none")
    if r["VAL"] == "AbovePerActionCap":
        return ("ROUTE", "PER_ACTION_CAP_EXCEEDED_L2", 0, "none")
    if r["VAL"] == "CrossesAggregateCap":
        return ("ROUTE", "AGGREGATE_CAP_EXCEEDED_L2", 0, "none")
    led = "reserve+commit" if r["PAY"] != "No-Payment" else "count+commit"
    return ("ALLOW", "WITHIN_MANDATE_" + r["AUT"], 1, led)

# ---------------------------------------------------------------- Model C
C = {
    "VC":    ["Valid", "Expired", "StatusRevoked", "SignatureInvalid", "IssuerNotTrusted"],
    "OFFER": ["WithinBounds", "AtFloor", "BeyondBounds", "ForbiddenTerm"],
    "ROUND": ["UnderMaxRounds", "MaxRoundsReached"],
    "AMT":   ["BelowTxnCap", "AtTxnCap", "AboveTxnCap", "PeriodCapExceeded"],
    "PMT":   ["UPI-AutoPay", "e-NACH", "Card-MIT", "SEPA-DD", "NetworkAgentToken"],
    "AUTH":  ["ExemptOrPreAuthorised", "AFA-SCA-Completed", "AFA-SCA-Missing"],
    "PSP":   ["Success", "Pending", "Declined", "Timeout"],
    "JUR":   ["IN", "EU", "PackNotApproved"],
}
CPMT_OK = {"IN": {"UPI-AutoPay", "e-NACH", "Card-MIT", "NetworkAgentToken"},
           "EU": {"SEPA-DD", "Card-MIT", "NetworkAgentToken"}}

def oracle_c(r):
    if r["JUR"] == "PackNotApproved":
        return ("HOLD", "JURISDICTION_PACK_NOT_APPROVED", 0, "none")
    if r["PMT"] not in CPMT_OK[r["JUR"]]:
        return ("DENY", "PAYMENT_METHOD_NOT_PERMITTED", 0, "none")
    vc = {"Expired": "VC_EXPIRED", "StatusRevoked": "VC_REVOKED", "SignatureInvalid": "VC_SIGNATURE_INVALID",
          "IssuerNotTrusted": "VC_ISSUER_NOT_TRUSTED"}
    if r["VC"] != "Valid":
        return ("DENY", vc[r["VC"]], 0, "none")
    if r["OFFER"] == "ForbiddenTerm":
        return ("ESCALATE", "FORBIDDEN_TERM_HUMAN", 0, "none")
    if r["OFFER"] == "BeyondBounds":
        if r["ROUND"] == "MaxRoundsReached":
            return ("ESCALATE", "BOUNDS_AND_ROUNDS_EXHAUSTED", 0, "none")
        return ("COUNTER", "COUNTER_AT_BOUND", 0, "none")
    if r["AMT"] == "AboveTxnCap":
        return ("ESCALATE", "TXN_CAP_EXCEEDED_L2", 0, "none")
    if r["AMT"] == "PeriodCapExceeded":
        return ("HOLD", "PERIOD_CAP_EXCEEDED", 0, "none")
    if r["AUTH"] == "AFA-SCA-Missing":
        return ("HOLD", "CUSTOMER_AUTH_REQUIRED", 0, "reserve->release")
    psp = {"Success": ("CAPTURED", "PSP_SUCCESS", 1, "reserve->commit; post J-02"),
           "Pending": ("AWAIT", "PSP_PENDING_WEBHOOK", 1, "reserve held"),
           "Declined": ("FAILED", "PSP_DECLINED", 1, "reserve->release"),
           "Timeout": ("RECONCILING", "PSP_OUTCOME_UNKNOWN", 1, "reserve held; no retry")}
    return psp[r["PSP"]]

# ---------------------------------------------------------------- Model B
B = {
    "AUT":      ["L1", "L2", "L3"],
    "MST":      ["Active", "PendingSecondApproval", "Revoked", "Expired"],
    "HASH":     ["Match", "PackageChanged", "ApprovalMissing"],
    "PORTAL":   ["API-Permitted", "Automation-Permitted", "AssistedOnly", "ManualOnly"],
    "DEADLINE": ["BeforeBuffer", "InsideBuffer", "AfterDeadline"],
    "SIGN":     ["OrgSignerAvailable", "HumanDSCOnly", "NotRequired"],
    "RECEIPT":  ["ReceiptOK", "TimeoutUnknown", "RejectedValidation"],
    "KS":       ["Off", "On"],
    "JUR":      ["PackApproved", "PackNotApproved"],
}

def oracle_b(r):
    if r["DEADLINE"] == "AfterDeadline":
        return ("EXPIRED", "DEADLINE_PASSED", 0)
    if r["KS"] == "On":
        return ("BLOCKED", "KILL_SWITCH", 0)
    if r["HASH"] == "ApprovalMissing":
        return ("HOLD", "PACKAGE_APPROVAL_MISSING", 0)
    if r["HASH"] == "PackageChanged":
        return ("HOLD", "PACKAGE_HASH_CHANGED_APPROVAL_VOID", 0)
    if r["AUT"] == "L1":
        return ("MANUAL", "HUMAN_SUBMITS_EVIDENCE_RECORDED", 0)
    if r["AUT"] == "L2" or r["JUR"] == "PackNotApproved" or r["PORTAL"] == "AssistedOnly" or r["SIGN"] == "HumanDSCOnly":
        if r["PORTAL"] == "ManualOnly":
            return ("MANUAL", "PORTAL_MANUAL_ONLY", 0)
        why = ("ASSISTED_L2" if r["AUT"] == "L2" else "PACK_NOT_APPROVED_ASSISTED" if r["JUR"] == "PackNotApproved"
               else "PORTAL_ASSISTED_ONLY" if r["PORTAL"] == "AssistedOnly" else "HUMAN_DSC_REQUIRED")
        return ("ASSISTED", why, 0)
    if r["PORTAL"] == "ManualOnly":
        return ("MANUAL", "PORTAL_MANUAL_ONLY", 0)
    if r["MST"] in ("PendingSecondApproval",):
        return ("HOLD", "MANDATE_NOT_ACTIVE", 0)
    if r["MST"] in ("Revoked", "Expired"):
        return ("DENY", "MANDATE_" + r["MST"].upper(), 0)
    if r["DEADLINE"] == "InsideBuffer":
        return ("ESCALATE", "INSIDE_DEADLINE_BUFFER_HUMAN", 0)
    rc = {"ReceiptOK": ("SUBMITTED", "RECEIPT_VERIFIED", 1),
          "TimeoutUnknown": ("RECONCILING", "SUBMISSION_OUTCOME_UNKNOWN", 1),
          "RejectedValidation": ("FAILED", "PORTAL_VALIDATION_REJECTED", 1)}
    return rc[r["RECEIPT"]]

# --------------------------------------------------------------- Model K (exhaustive)
K = {"SCOPE": ["Platform", "Tenant", "Company", "Agent", "Mandate", "Counterparty", "Portal", "PaymentMethod"],
     "PHASE": ["NotStarted", "Reserved", "DispatchedAwaitingProvider", "CompletedUnreconciled"],
     "ACTOR": ["R01", "R10"]}
# 8*4*2 = 64 -> exhaustive

def oracle_k(r):
    ph = {"NotStarted": ("BLOCKED", "no provider call; run Paused", "none"),
          "Reserved": ("BLOCKED", "reservation released; run Paused", "release"),
          "DispatchedAwaitingProvider": ("RECONCILING", "no new call; await provider/query by idempotency key", "held"),
          "CompletedUnreconciled": ("RECONCILE", "effect not hidden; reconciliation task opened", "commit stays")}
    return ph[r["PHASE"]]

# Positive (gate-passing) values per model. Every other value is a "fault"
# value: it is exercised in the full 3-way layer (precedence interactions) and
# once per positive context in the single-fault layer (deep-path robustness).
M_POS = {"AUT": ["L3", "L4"], "MST": ["Active"], "VAL": ["BelowCap", "AtCap"], "CPT": ["AllowlistedVerified"],
         "JUR": ["IN-Approved", "EU-Approved"], "PAY": M["PAY"], "WIN": ["Inside"], "KS": ["Off"]}
C_POS = {"VC": ["Valid"], "OFFER": ["WithinBounds", "AtFloor"], "ROUND": C["ROUND"], "AMT": ["BelowTxnCap", "AtTxnCap"],
         "PMT": C["PMT"], "AUTH": ["ExemptOrPreAuthorised", "AFA-SCA-Completed"], "PSP": C["PSP"], "JUR": ["IN", "EU"]}
B_POS = {"AUT": ["L3"], "MST": ["Active"], "HASH": ["Match"], "PORTAL": ["API-Permitted", "Automation-Permitted"],
         "DEADLINE": ["BeforeBuffer"], "SIGN": ["OrgSignerAvailable", "NotRequired"], "RECEIPT": B["RECEIPT"],
         "KS": ["Off"], "JUR": ["PackApproved"]}

def m_valid(d):
    if "JUR" in d and "PAY" in d and d["JUR"] in PAY_OK:
        return d["PAY"] in PAY_OK[d["JUR"]]
    return True

def c_valid(d):
    if "JUR" in d and "PMT" in d and d["JUR"] in CPMT_OK:
        return d["PMT"] in CPMT_OK[d["JUR"]]
    return True

def single_fault(full, pos, valid, ctx):
    """One row per (fault value x positive value of context parameter ctx); all
    other parameters take positive values, rotated so each positive value is used."""
    rows, rot = [], 0
    keys = list(full)
    for p in keys:
        for fv in full[p]:
            if fv in pos[p]:
                continue
            for cv in (pos[ctx] if p != ctx else [None]):
                tries = 0
                while True:
                    r = {}
                    for q in keys:
                        if q == p:
                            r[q] = fv
                        elif q == ctx:
                            r[q] = cv
                        else:
                            vals = pos[q]
                            r[q] = vals[(rot + tries) % len(vals)]
                    tries += 1
                    if valid(r) or tries > 12:
                        break
                rot += 1
                rows.append(r)
    return rows

def write(path, txt):
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)

def main(out):
    os.makedirs(out, exist_ok=True)
    stats, seq = {}, [0]
    def tc():
        seq[0] += 1
        return "TC-V12-P-%03d" % seq[0]
    HDR = "| ID | Data ({cols}) | Expected | Links | P | Type | Tech | Auto | Lvl |\n|---|---|---|---|---|---|---|---|---|\n"
    def emit(fname, rows, keys, fmt, layer, stat):
        lines, ids, verdicts = [], [], {}
        for r in rows:
            exp, prio, typ, links, tech = fmt(r)
            v = exp.split(" ")[0].rstrip(":")
            verdicts[v] = verdicts.get(v, 0) + 1
            i = tc(); ids.append(i)
            lines.append("| %s | %s | %s | %s | %s | %s | %s | Y | %s |" % (
                i, " · ".join(r[k] for k in keys), exp, links, prio, typ, tech[0], tech[1]))
        write(os.path.join(out, fname), HDR.format(cols=" · ".join(keys)) + "\n".join(lines) + "\n")
        stat[layer] = dict(rows=len(rows), ids=[ids[0], ids[-1]], verdicts=verdicts)
    def fm(tech):
        def f(r):
            v, why, calls, led = oracle_m(r)
            prio = "P0" if v in ("ALLOW", "BLOCKED", "DENY") or r["KS"] != "Off" else "P1"
            typ = "T07, T21" if v == "BLOCKED" else ("T01, T16" if v == "ALLOW" else "T01, T19")
            exp = "%s `%s`; provider calls = %d; mandate ledger: %s; audit `mandate.decision` outcome=%s%s" % (
                v, why, calls, led, v.lower(), "" if calls else "; NSE")
            return exp, prio, typ, "TS-18-ZP01 · US-18-ZP03 · FR-V12-P-040…052; DEC-779", tech
        return f
    sm = stats["M"] = dict(params=len(M), domain=[len(v) for v in M.values()], total=total(M), triples=tuples(M, 3))
    emit("M_L1_3way.md", covering_array(M, 3, seed=840), list(M), fm(("PW3", "IT")), "L1_3way", sm)
    pos = [r for r in (dict(zip(M_POS, p)) for p in itertools.product(*M_POS.values())) if m_valid(r)]
    emit("M_L2_positive.md", pos, list(M), fm(("EX", "IT")), "L2_positive_exhaustive", sm)
    emit("M_L3_singlefault.md", single_fault(M, M_POS, m_valid, "AUT"), list(M), fm(("EP", "IT")), "L3_single_fault", sm)
    def fc(tech):
        def f(r):
            v, why, calls, led = oracle_c(r)
            prio = "P0" if v in ("CAPTURED", "RECONCILING", "DENY", "ESCALATE", "HOLD") else "P1"
            typ = "T01, T18" if v == "RECONCILING" else ("T07, T19" if v == "DENY" else "T01, T19")
            exp = "%s `%s`; PSP calls = %d; mandate ledger: %s%s" % (v, why, calls, led, "" if calls else "; NSE")
            return exp, prio, typ, "TS-24-ZP02 · US-24-ZP04, US-15-ZP01 · FR-V12-P-070…098; DEC-780", tech
        return f
    sc = stats["C"] = dict(params=len(C), domain=[len(v) for v in C.values()], total=total(C), triples=tuples(C, 3))
    emit("C_L1_3way.md", covering_array(C, 3, seed=841), list(C), fc(("PW3", "IT")), "L1_3way", sc)
    sc["positive_space"] = sum(1 for p in itertools.product(*C_POS.values()) if c_valid(dict(zip(C_POS, p))))
    emit("C_L2_positive.md", covering_array(C_POS, 3, seed=845, valid=c_valid), list(C), fc(("PW3", "IT")), "L2_positive_3way", sc)
    emit("C_L3_singlefault.md", single_fault(C, C_POS, c_valid, "PSP"), list(C), fc(("EP", "IT")), "L3_single_fault", sc)
    def fb(tech):
        def f(r):
            v, why, calls = oracle_b(r)
            prio = "P0" if v in ("SUBMITTED", "RECONCILING", "BLOCKED", "EXPIRED", "HOLD", "DENY", "ESCALATE") else "P1"
            typ = "T01, T18" if v == "RECONCILING" else "T01, T19"
            exp = "%s `%s`; portal submit calls = %d%s" % (v, why, calls, "" if calls else "; NSE")
            return exp, prio, typ, "TS-14-ZP01 · US-14-ZP02 · FR-V12-P-110…135; DEC-781", tech
        return f
    sb = stats["B"] = dict(params=len(B), domain=[len(v) for v in B.values()], total=total(B), triples=tuples(B, 3))
    emit("B_L1_3way.md", covering_array(B, 3, seed=842), list(B), fb(("PW3", "IT")), "L1_3way", sb)
    pos = [dict(zip(B_POS, p)) for p in itertools.product(*B_POS.values())]
    emit("B_L2_positive.md", pos, list(B), fb(("EX", "IT")), "L2_positive_exhaustive", sb)
    emit("B_L3_singlefault.md", single_fault(B, B_POS, lambda d: True, "RECEIPT"), list(B), fb(("EP", "IT")), "L3_single_fault", sb)
    rows = [dict(zip(K, p)) for p in itertools.product(*K.values())]
    def fk(r):
        v, eff, led = oracle_k(r)
        return ("%s: %s; reservation %s; propagation ≤ 60 s; event `killswitch.engaged` scope=%s; resume needs two-person approval + PDP recheck" % (
            v, eff, led, r["SCOPE"].lower()), "P0", "T07, T21", "TS-18-ZP02 · US-18-ZP06 · FR-V12-P-053…058; BRL-AUT-05", ("EX", "IT"))
    sk = stats["K"] = dict(params=len(K), total=total(K))
    emit("K_exhaustive.md", rows, list(K), fk, "exhaustive", sk)
    for key, model, orc in (("M", M, oracle_m), ("C", C, oracle_c), ("B", B, oracle_b)):
        rows = covering_array(model, 2, seed=850)
        stats[key]["pairwise_rows"] = len(rows)
        stats[key]["pairs"] = tuples(model, 2)
        cols = list(model)
        out_l = ["      | " + " | ".join(c.lower() for c in cols) + " | verdict | reason |"]
        for r in rows:
            o = orc(r)
            out_l.append("      | " + " | ".join(r[c] for c in cols) + " | %s | %s |" % (o[0], o[1]))
        write(os.path.join(out, key + "_pairwise_examples.txt"), "\n".join(out_l) + "\n")
    stats["last_tc"] = seq[0]
    write(os.path.join(out, "stats.json"), json.dumps(stats, indent=1))
    print(json.dumps(stats, indent=1))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "p_frag2")

def verify(model, rows, t, valid=None):
    """Independent check: every (valid) t-tuple of the model occurs in some row."""
    ok = (lambda d: True) if valid is None else valid
    names = list(model)
    missing = 0
    for cols in itertools.combinations(names, t):
        need = {vals for vals in itertools.product(*[model[c] for c in cols]) if ok(dict(zip(cols, vals)))}
        have = {tuple(r[c] for c in cols) for r in rows}
        missing += len(need - have)
    return missing
