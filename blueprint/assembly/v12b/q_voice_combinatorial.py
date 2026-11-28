#!/usr/bin/env python3
"""Group Q (Part 11.18) - AI voice, telephony and call recordings.

Generates the combinatorial test design for Part 11.18:
  * C3: 3-way covering array over the 8-parameter voice call model
        (jurisdiction x direction x consent state x language x recording mode
         x DND status x time of day x handoff trigger)
  * RX: exhaustive recording-consent matrix (jurisdiction x direction x recording mode = 56)
  * VM: exhaustive voicemail / answering-machine matrix (jurisdiction x AMD result x consent = 63)
  * NX: exhaustive caller-ID / number-series matrix (jurisdiction x purpose x number = 42)
  * CP: pairwise coaching-from-recordings model (SM-SVC-36-WF03)

Every row gets an expected result from a deterministic oracle that encodes the
policy of Part 11.18a (sections 11.18.5.2 - 11.18.5.9). The oracle is the
executable form of the specification: the same tables drive AU-280/AU-282.

Outputs Markdown fragments into the directory given as argv[1].
Deterministic: fixed seed, stable ordering. Re-running gives identical output.
"""
import itertools
import os
import random
import sys

SEED = 18_2026

# ---------------------------------------------------------------- parameters
JUR = ["IN", "EU-DE", "EU-FR", "UK", "US-1P", "US-AP", "AE"]
DIR = ["INB", "OUT"]
CONSENT = ["NONE", "CALLBACK_REQ", "EXPRESS", "PEWC", "WITHDRAWN"]
LANG = ["en", "hi", "ta", "de", "fr", "ar"]
REC = ["OFF", "NOTICE_ONLY", "CONSENT_GIVEN", "CONSENT_REFUSED"]
DND = ["NOT_REG", "REG_FULL", "REG_CATEGORY_OK", "SCRUB_DOWN"]
TOD = ["IN_WINDOW", "BEFORE", "AFTER", "RESTRICTED_DAY"]
HANDOFF = ["NONE", "CALLER_REQ", "LOW_CONF", "SENSITIVE", "DISCLOSURE_FAIL"]

PARAMS = [("Jurisdiction", JUR), ("Direction", DIR), ("Consent state", CONSENT),
          ("Language", LANG), ("Recording mode", REC), ("DND / registry status", DND),
          ("Time of day", TOD), ("Handoff trigger", HANDOFF)]

PARAM_DESC = {
    "Jurisdiction": {
        "IN": "India (TRAI TCCCPR, DLT, NCPR, DPDP); RP-IN-SMS, RP-IN-DPDP",
        "EU-DE": "Germany (GDPR, ePrivacy Art. 13, UWG s.7, StGB s.201, TKG CLI rules)",
        "EU-FR": "France (GDPR, ePrivacy, Code de la consommation L.223-1 ff., Bloctel, Decree 2022-1313 hours)",
        "UK": "United Kingdom (UK GDPR, PECR regs 19/21, TPS, IPR 2018 recording)",
        "US-1P": "US one-party-consent state (TCPA, FCC 24-17 AI voice ruling, National DNC, 18 USC 2511(2)(d))",
        "US-AP": "US all-party-consent state, e.g. California Penal Code s.632 (plus TCPA, DNC)",
        "AE": "UAE (PDPL Decree-Law 45/2021, Cabinet Resolution 56/2024 telemarketing, DNCR)",
    },
    "Direction": {"INB": "Inbound: caller dials a tenant number answered by the AI agent",
                  "OUT": "Outbound: platform places an AI call for a sales-engagement (promotional) purpose"},
    "Consent state": {
        "NONE": "No lawful basis or calling consent on record",
        "CALLBACK_REQ": "Documented callback request (web form or chat) whose notice said an AI assistant may call",
        "EXPRESS": "Express consent to be called (verbal or form), not in the jurisdiction's written/registry-grade form",
        "PEWC": "Prior express written consent (US E-SIGN grade) / DLT digital consent (IN) / documented opt-in (EU, UK, AE)",
        "WITHDRAWN": "Consent withdrawn or opt-out received on any channel",
    },
    "Language": {"en": "English", "hi": "Hindi", "ta": "Tamil (Indic set representative)",
                 "de": "German", "fr": "French", "ar": "Arabic"},
    "Recording mode": {
        "OFF": "Campaign or line configured not to record",
        "NOTICE_ONLY": "Recording notice played; no affirmative consent captured",
        "CONSENT_GIVEN": "Every party affirmatively consented (DTMF 1 or verbal yes captured and verified)",
        "CONSENT_REFUSED": "A party refused or did not answer the recording-consent prompt",
    },
    "DND / registry status": {
        "NOT_REG": "Number not on the national do-not-call / preference registry",
        "REG_FULL": "Number fully registered (NCPR full block, US National DNC, UK TPS, Bloctel, UAE DNCR)",
        "REG_CATEGORY_OK": "Registered with a category preference that allows this category (India NCPR partial); elsewhere treated as registered",
        "SCRUB_DOWN": "Registry scrub service unavailable or scrub older than the allowed age",
    },
    "Time of day": {
        "IN_WINDOW": "Weekday 11:00 recipient local time (inside every effective window)",
        "BEFORE": "08:30 recipient local time",
        "AFTER": "21:30 recipient local time",
        "RESTRICTED_DAY": "Sunday or public holiday, 11:00 recipient local time",
    },
    "Handoff trigger": {
        "NONE": "No trigger; AI completes the task",
        "CALLER_REQ": "Caller asks for a person ('agent', 'human', 0 key)",
        "LOW_CONF": "Intent or answer confidence below the floor (0.70) twice in a row",
        "SENSITIVE": "Price, discount, payment, contract, complaint, legal, clinical or emergency topic",
        "DISCLOSURE_FAIL": "The AI disclosure audio failed to play or ASR did not confirm it within 2 s",
    },
}

# ------------------------------------------------------------- policy tables
# Consent standard needed for an outbound AI (artificial-voice) sales call
CONSENT_OK = {
    "IN": {"CALLBACK_REQ", "EXPRESS", "PEWC"},
    "EU-DE": {"CALLBACK_REQ", "EXPRESS", "PEWC"},
    "EU-FR": {"CALLBACK_REQ", "EXPRESS", "PEWC"},
    "UK": {"CALLBACK_REQ", "EXPRESS", "PEWC"},
    "US-1P": {"PEWC"},
    "US-AP": {"PEWC"},
    "AE": {"CALLBACK_REQ", "EXPRESS", "PEWC"},
}
CONSENT_REASON = {"US-1P": "TCPA_PEWC_REQUIRED", "US-AP": "TCPA_PEWC_REQUIRED"}
# Consent that overrides a registry registration
REG_OVERRIDE = {
    "IN": {"PEWC"},  # DLT digital consent only
    "EU-DE": None,   # no statutory registry: registry check not applicable
    "EU-FR": {"CALLBACK_REQ", "EXPRESS", "PEWC"},  # Bloctel: consent / relationship exemption
    "UK": {"CALLBACK_REQ", "EXPRESS", "PEWC"},     # TPS: specific consent to the caller
    "US-1P": {"PEWC"}, "US-AP": {"PEWC"},          # National DNC: signed written agreement
    "AE": {"PEWC"},
}
REGISTRY_NAME = {"IN": "NCPR", "EU-DE": "none (no statutory registry)", "EU-FR": "Bloctel",
                 "UK": "TPS", "US-1P": "National DNC", "US-AP": "National DNC", "AE": "DNCR"}
WINDOW = {"IN": "09:00-21:00", "EU-DE": "09:00-21:00", "EU-FR": "Mon-Fri 10:00-13:00, 14:00-20:00",
          "UK": "09:00-21:00", "US-1P": "09:00-21:00", "US-AP": "09:00-21:00", "AE": "09:00-18:00"}
RESTRICTED_DAY_HOLD = {"EU-FR", "AE"}
REC_REQ = {"IN": "NOTICE", "UK": "NOTICE", "US-1P": "NOTICE", "US-AP": "ALL_PARTY",
           "EU-DE": "ALL_PARTY", "EU-FR": "ALL_PARTY", "AE": "ALL_PARTY"}
LANG_TIER = {"en": "A", "hi": "A", "de": "A", "fr": "A", "ta": "B", "ar": "B"}
CALLER_ID = {
    "IN": "140-series promotional pool (RP-IN-SMS-011)",
    "EU-DE": "German DID, CLI presented and callable (TKG)",
    "EU-FR": "ARCEP telemarketing-prefix number (verify)",
    "UK": "UK CLI that is valid and dialable (Ofcom)",
    "US-1P": "US DID with STIR/SHAKEN A attestation and registered CNAM",
    "US-AP": "US DID with STIR/SHAKEN A attestation and registered CNAM",
    "AE": "UAE registered telemarketing number (verify)",
}


def outbound_preflight(j, c, d, t):
    """Return (verdict, [reasons]) for an outbound AI call. Precedence as AU-171/AU-280:
    suppression > consent standard > registry > window."""
    reasons = []
    if c == "WITHDRAWN":
        reasons.append("CONSENT_WITHDRAWN")
    elif c not in CONSENT_OK[j]:
        reasons.append(CONSENT_REASON.get(j, "NO_CALL_CONSENT"))
    hold = []
    if REG_OVERRIDE[j] is not None:
        if d == "SCRUB_DOWN":
            hold.append("REGISTRY_SCRUB_UNAVAILABLE")
        elif d == "REG_FULL" or (d == "REG_CATEGORY_OK" and j != "IN"):
            if c not in REG_OVERRIDE[j]:
                reasons.append("REGISTRY_BLOCKED_" + REGISTRY_NAME[j].replace(" ", "_").upper())
    if t in ("BEFORE", "AFTER") or (t == "RESTRICTED_DAY" and j in RESTRICTED_DAY_HOLD):
        hold.append("OUTSIDE_CALLING_WINDOW")
    if reasons:
        return "BLOCK", reasons + hold
    if hold:
        return "HOLD", hold
    return "ALLOW", []


def recording_outcome(j, r):
    req = REC_REQ[j]
    if r == "OFF":
        return "NOT_RECORDED", "No audio, no verbatim transcript stored; transient ASR only; disposition and field-level summary kept"
    if r == "NOTICE_ONLY":
        if req == "NOTICE":
            return "RECORDED_NOTICE", "Recording starts after TPL-VO-REC-01 notice; objection at any time stops it and deletes the partial audio"
        return "NOT_RECORDED", "Recording refused by AU-282: ALL_PARTY_CONSENT_REQUIRED; call continues; metadata only"
    if r == "CONSENT_GIVEN":
        return "RECORDED_CONSENT", "Recording from the consent timestamp; consent event with DTMF/verbal evidence and prompt version stored"
    return "NOT_RECORDED", "Recording not started; refusal stored in consent ledger; call continues; metadata only"


def handoff_outcome(direction, h, t, lang):
    staffed = (t == "IN_WINDOW")
    if h == "DISCLOSURE_FAIL":
        if direction == "OUT":
            return "TERMINATE", "Call ended before any other AI speech; attempt logged DISCLOSURE_FAILED; campaign auto-paused after 3 in 15 min (AU-283)"
        return "ROUTE_HUMAN_OR_MESSAGE", ("Transfer to human queue with recorded human-voice greeting" if staffed else
                                          "Recorded human-voice after-hours greeting; message capture; callback task (no AI speech)")
    if h == "NONE":
        if LANG_TIER[lang] == "A":
            return "AI_RESOLVES", "AI answers from approved knowledge or books the slot after verbal read-back; disposition written"
        return "AI_RESOLVES_VERBATIM", "Language tier B: AI speaks only verbatim approved answers and runs the booking script; anything else goes to a human"
    if h == "SENSITIVE":
        txt = "AI speaks the approved bridge line, stops answering the topic and transfers"
    elif h == "CALLER_REQ":
        txt = "AI confirms and starts a warm transfer"
    else:
        txt = "AI states it will connect a colleague and transfers"
    if staffed:
        return "WARM_TRANSFER", txt + " with an AG-215 handoff brief; target answer by a human <= 30 s (p90 <= 60 s)"
    return "CALLBACK_TASK", txt.split(" and ")[0] + "; no human on shift: callback task due next staffed hour, caller told the time"


def oracle(row):
    j, di, c, lang, r, d, t, h = row
    out = {}
    if di == "OUT":
        verdict, reasons = outbound_preflight(j, c, d, t)
        out["dispatch"] = verdict
        out["reasons"] = reasons
        if verdict != "ALLOW":
            out["call"] = "No call placed; no provider request; 0 minutes metered; run state " + ("BLOCKED" if verdict == "BLOCK" else "HELD (rescheduled to next window)" if "OUTSIDE_CALLING_WINDOW" in reasons and len(reasons) == 1 else "HELD")
            out["disclosure"] = "n/a"
            out["recording"] = ("n/a", "n/a")
            out["handoff"] = ("n/a", "n/a")
            return out
        out["call"] = "Call placed from " + CALLER_ID[j]
    else:
        out["dispatch"] = "ANSWER"
        out["reasons"] = []
        out["call"] = "AI answers on the tenant number" + ("; marketing content suppressed (consent withdrawn)" if c == "WITHDRAWN" else "")
    out["disclosure"] = "TPL-VO-DISC-01 in " + lang + " within 2 s of answer; ASR confirms; disclosure_played = true" if h != "DISCLOSURE_FAIL" else "Disclosure failed (not confirmed)"
    out["recording"] = recording_outcome(j, r) if h != "DISCLOSURE_FAIL" or di == "INB" else ("NOT_RECORDED", "Call terminated before recording prompt")
    out["handoff"] = handoff_outcome(di, h, t, lang)
    return out


# --------------------------------------------------------------- generator
def covering_array(domains, t, seed, candidates=60):
    """Greedy AETG-style t-way covering array. Deterministic for a given seed."""
    rnd = random.Random(seed)
    n = len(domains)
    combos = list(itertools.combinations(range(n), t))
    uncovered = set()
    for cols in combos:
        for vals in itertools.product(*[range(len(domains[c])) for c in cols]):
            uncovered.add((cols, vals))
    total = len(uncovered)
    rows = []

    def gain(row):
        g = 0
        for cols in combos:
            if (cols, tuple(row[c] for c in cols)) in uncovered:
                g += 1
        return g

    while uncovered:
        best, best_g = None, -1
        seed_item = sorted(uncovered)[rnd.randrange(len(uncovered))] if len(uncovered) < 50 else rnd.choice(tuple(uncovered))
        for _ in range(candidates):
            row = [None] * n
            cols, vals = seed_item
            for c, v in zip(cols, vals):
                row[c] = v
            order = [i for i in range(n) if row[i] is None]
            rnd.shuffle(order)
            for i in order:
                bestv, bestvg = 0, -1
                vs = list(range(len(domains[i])))
                rnd.shuffle(vs)
                for v in vs:
                    row[i] = v
                    g = 0
                    for cc in combos:
                        if i in cc and all(row[k] is not None for k in cc):
                            if (cc, tuple(row[k] for k in cc)) in uncovered:
                                g += 1
                    if g > bestvg:
                        bestv, bestvg = v, g
                row[i] = bestv
            g = gain(row)
            if g > best_g:
                best, best_g = list(row), g
        rows.append(best)
        for cols in combos:
            uncovered.discard((cols, tuple(best[c] for c in cols)))
    return rows, total


def verify(rows, domains, t):
    need = 0
    for cols in itertools.combinations(range(len(domains)), t):
        seen = {tuple(r[c] for c in cols) for r in rows}
        need += len(list(itertools.product(*[range(len(domains[c])) for c in cols])))
        assert len(seen) == len(list(itertools.product(*[range(len(domains[c])) for c in cols]))), cols
    return need


def md_escape(s):
    return str(s).replace("|", "\\|")


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    domains = [p[1] for p in PARAMS]
    idx_rows, total3 = covering_array(domains, 3, SEED)
    verify(idx_rows, domains, 3)
    rows = [tuple(domains[i][v] for i, v in enumerate(r)) for r in idx_rows]
    # stable sort for readability: jurisdiction, direction
    rows.sort(key=lambda r: (JUR.index(r[0]), DIR.index(r[1]), CONSENT.index(r[2]), LANG.index(r[3])))
    full_space = 1
    for d_ in domains:
        full_space *= len(d_)
    pair_total = sum(len(domains[a]) * len(domains[b]) for a, b in itertools.combinations(range(8), 2))

    # ---------------- C3 test table
    lines = []
    lines.append("| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    stats = {"ALLOW": 0, "BLOCK": 0, "HOLD": 0, "ANSWER": 0}
    ex_out, ex_in = [], []
    for k, row in enumerate(rows, 1):
        j, di, c, lang, r, d, t, h = row
        o = oracle(row)
        stats[o["dispatch"]] += 1
        tid = "TC-V12-Q-C3-%03d" % k
        title = "%s %s call, consent %s, %s, rec %s, %s, %s, handoff %s" % (j, "outbound" if di == "OUT" else "inbound", c, lang, r, d, t, h)
        links = "TS-V12-Q-03 · US-22-ZQ%s · FR-V12-Q-%s; DEC-782; DEC-777" % ("03" if di == "OUT" else "01", "010" if di == "OUT" else "001")
        if di == "OUT":
            clock = "virtual clock %s (effective window %s)" % (PARAM_DESC["Time of day"][t].split(" (")[0], WINDOW[j])
            reg = "registry %s (%s)" % (d, REGISTRY_NAME[j])
        else:
            clock = "virtual clock %s; human handoff desk %s" % (PARAM_DESC["Time of day"][t].split(" (")[0], "on shift" if t == "IN_WINDOW" else "closed")
            reg = "registry %s (not evaluated: caller-initiated)" % d
        pre = ("PP-Q-01 voice simulator; %s; packs for %s Approved in test; contact fixture CT-Q-%s with consent %s, %s; script SC-Q-%s v3 approved (hash pinned); recording mode %s; handoff fixture %s" %
               (clock, j, j.replace("-", ""), c, reg, lang, r, h))
        if di == "OUT":
            steps = "1. POST `/api/v2/voice/calls` (outbound, campaign VC-Q-01). 2. Simulator answers as a person and plays the %s caller fixture. 3. Read call record, consent ledger, recording store, meter and audit." % h
        else:
            steps = "1. Simulator places an inbound call to the tenant number in %s. 2. Caller fixture speaks %s and triggers %s. 3. Read call record, recording store, handoff queue, meter and audit." % (j, lang, h)
        exp = ["Dispatch: **%s**" % o["dispatch"]]
        if o["reasons"]:
            exp.append("reasons " + ", ".join("`%s`" % x for x in o["reasons"]))
        exp.append(o["call"])
        if o["disclosure"] != "n/a":
            exp.append("Disclosure: " + o["disclosure"])
            exp.append("Recording: %s (%s)" % o["recording"])
            exp.append("Handoff: %s (%s)" % o["handoff"])
        exp.append("audit event per decision; PDP verdict stored on effect.preflight_verdict")
        prio = "P0" if (o["dispatch"] in ("BLOCK", "HOLD") or h in ("SENSITIVE", "DISCLOSURE_FAIL") or o["recording"][0] == "NOT_RECORDED" and r in ("NOTICE_ONLY", "CONSENT_REFUSED")) else "P1"
        types = "T19, T01" + (", T13" if lang in ("hi", "ta", "ar", "de", "fr") else "")
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | PW (3-way) | Y | SYS |" % (
            tid, md_escape(title), links, md_escape(pre), md_escape(steps), md_escape("; ".join(exp)), prio, types))
        if di == "OUT":
            ex_out.append((tid, j, c, d, t, o["dispatch"], ",".join(o["reasons"]) or "-"))
        else:
            ex_in.append((tid, j, lang, r, t, h, o["recording"][0], o["handoff"][0]))
    open(os.path.join(outdir, "c3_tests.md"), "w").write("\n".join(lines) + "\n")

    # ---------------- parameter model fragment
    pm = []
    pm.append("| # | Parameter | Values (count) | Value meanings |")
    pm.append("|---|---|---|---|")
    for i, (name, vals) in enumerate(PARAMS, 1):
        meaning = "; ".join("`%s` %s" % (v, PARAM_DESC[name][v]) for v in vals)
        pm.append("| %d | %s | %s (%d) | %s |" % (i, name, ", ".join("`%s`" % v for v in vals), len(vals), md_escape(meaning)))
    open(os.path.join(outdir, "param_model.md"), "w").write("\n".join(pm) + "\n")
    counts = {"full": full_space, "triples": total3, "pairs": pair_total, "rows": len(rows),
              "lower": 7 * 6 * 5, "stats": stats}

    # ---------------- Examples for stories
    eo = ["      | case | jurisdiction | consent | registry | time | verdict | reasons |"]
    for e in ex_out:
        eo.append("      | %s | %s | %s | %s | %s | %s | %s |" % e)
    open(os.path.join(outdir, "ex_outbound.md"), "w").write("\n".join(eo) + "\n")
    ei = ["      | case | jurisdiction | language | recording_mode | time | trigger | recording | handoff |"]
    for e in ex_in:
        ei.append("      | %s | %s | %s | %s | %s | %s | %s | %s |" % e)
    open(os.path.join(outdir, "ex_inbound.md"), "w").write("\n".join(ei) + "\n")

    # ---------------- RX exhaustive recording matrix
    rx = ["| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    rx_ex = ["      | case | jurisdiction | direction | mode | requirement | outcome |"]
    k = 0
    for j in JUR:
        for di in DIR:
            for r in REC:
                k += 1
                res, txt = recording_outcome(j, r)
                tid = "TC-V12-Q-RX-%02d" % k
                rx.append("| %s | Recording %s for %s %s call | TS-V12-Q-05 · US-22-ZQ05 · FR-V12-Q-020…024; DEC-782 | PP-Q-01; pack %s Approved; requirement %s; campaign recording mode %s; caller fixture answers the prompt accordingly | 1. Place the %s call. 2. Let the recording prompt run. 3. Inspect recording store, consent ledger and AU-282 decision log | **%s**: %s; transcript persisted only if recorded; audit `voice.recording.%s` | P0 | T19, T07 | DT (exhaustive) | Y | SYS |" % (
                    tid, r, j, "outbound" if di == "OUT" else "inbound", j, REC_REQ[j], r, "outbound" if di == "OUT" else "inbound", res, txt, "started" if res.startswith("RECORDED") else "declined"))
                rx_ex.append("      | %s | %s | %s | %s | %s | %s |" % (tid, j, di, r, REC_REQ[j], res))
    open(os.path.join(outdir, "rx_tests.md"), "w").write("\n".join(rx) + "\n")
    open(os.path.join(outdir, "ex_recording.md"), "w").write("\n".join(rx_ex) + "\n")

    # ---------------- VM exhaustive voicemail matrix
    AMD = ["HUMAN", "MACHINE", "UNKNOWN"]
    VMC = ["PEWC", "EXPRESS", "CALLBACK_REQ"]
    vm = ["| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    k = 0
    for j in JUR:
        for a in AMD:
            for c in VMC:
                k += 1
                ok_consent = c in CONSENT_OK[j]
                if not ok_consent:
                    exp = "Preflight BLOCK `%s`; no call, no voicemail" % CONSENT_REASON.get(j, "NO_CALL_CONSENT")
                elif a == "HUMAN":
                    exp = "Conversation proceeds with disclosure TPL-VO-DISC-01; no voicemail"
                elif a == "UNKNOWN":
                    exp = "Treated as a person: disclosure plays first; if no speech in 4 s the call ends silently; no message left; attempt counted"
                else:
                    if j in ("EU-DE", "EU-FR", "AE") and c != "PEWC":
                        exp = "No voicemail (`VOICEMAIL_NEEDS_DOCUMENTED_OPT_IN`); hang up; callback task or next attempt within cap"
                    else:
                        exp = "One voicemail TPL-VO-VM-01 (brand, AI-voice disclosure, purpose without personal detail, callback number, opt-out route); max 1 per contact per campaign per 7 days; no ringless drop"
                vm.append("| TC-V12-Q-VM-%02d | Voicemail rule %s, AMD %s, consent %s | TS-V12-Q-06 · US-22-ZQ06 · FR-V12-Q-016; RP-IN-SMS-012 | PP-Q-01; outbound campaign VC-Q-02 with voicemail allowed; AMD fixture %s | 1. Dispatch. 2. Simulator returns AMD %s. 3. Inspect call record and voicemail log | %s | P0 | T19 | DT (exhaustive) | Y | SYS |" % (k, j, a, c, a, a, exp))
    open(os.path.join(outdir, "vm_tests.md"), "w").write("\n".join(vm) + "\n")

    # ---------------- NX exhaustive number-series matrix
    PURPOSE = ["PROMOTIONAL", "SERVICE"]
    NUM = ["COMPLIANT_POOL", "WRONG_SERIES", "UNREGISTERED"]
    nx = ["| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    k = 0
    for j in JUR:
        for p in PURPOSE:
            for n in NUM:
                k += 1
                if n == "COMPLIANT_POOL":
                    pool = CALLER_ID[j] if p == "PROMOTIONAL" else ("1600-series service pool (RP-IN-SMS-011)" if j == "IN" else CALLER_ID[j])
                    exp = "AU-284 selects %s; caller ID attested; call allowed to proceed to preflight" % pool
                elif n == "WRONG_SERIES":
                    if j == "IN":
                        exp = "BLOCK `NUMBER_SERIES_MISMATCH` (%s purpose needs %s series)" % (p.lower(), "140" if p == "PROMOTIONAL" else "1600")
                    else:
                        exp = "BLOCK `CLI_NOT_VALID_FOR_MARKET` (number not provisioned for %s)" % j
                else:
                    exp = "BLOCK `NUMBER_NOT_REGISTERED` (no regulatory bundle / DLT header / CNAM record); R11 alerted"
                nx.append("| TC-V12-Q-NX-%02d | Caller-ID rule %s, %s purpose, %s | TS-V12-Q-07 · US-22-ZQ08 · FR-V12-Q-030…033; CJ-IN-07 | PP-Q-01; number inventory fixture NI-Q-%02d | 1. Request outbound call with purpose %s. 2. Inspect AU-284 selection and preflight verdict | %s | P0 | T19 | DT (exhaustive) | Y | IT |" % (k, j, p.lower(), n, k, p, exp))
    open(os.path.join(outdir, "nx_tests.md"), "w").write("\n".join(nx) + "\n")

    # ---------------- CP pairwise coaching model
    CJUR = ["IN", "EU-DE", "EU-FR", "UK", "US-1P", "US-AP", "AE"]
    SRC = ["REC_CONSENT_COACHING", "REC_NOTICE", "STAFF_NOTES", "THREAD_TEXT"]
    ROLE = ["LEARNER", "COACH", "HR", "AUDITOR"]
    OUTP = ["LEARNER_FEEDBACK", "TEAM_AGGREGATE", "HR_EXPORT"]
    WORKS = ["IN_PLACE", "ABSENT"]
    cdom = [CJUR, SRC, ROLE, OUTP, WORKS]
    cidx, ctot = covering_array(cdom, 2, SEED + 1)
    verify(cidx, cdom, 2)
    crow = sorted([tuple(cdom[i][v] for i, v in enumerate(r)) for r in cidx], key=lambda r: (CJUR.index(r[0]), SRC.index(r[1])))
    cp = ["| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    cp_ex = ["      | case | jurisdiction | source | role | output | works_agreement | verdict |"]
    for k, (j, s, ro, op, w) in enumerate(crow, 1):
        if op == "HR_EXPORT":
            v, e = "DENY", "`NO_EMPLOYMENT_DECISION_USE`: coaching output never exported to HR, performance or pay views (V12 SVC-36 'no automated employment decision'; DEC-386 retained part)"
        elif s == "REC_NOTICE" and REC_REQ[j] == "ALL_PARTY":
            v, e = "BLOCK", "`RECORDING_NOT_LAWFUL_FOR_COACHING`: notice-only recording in an all-party jurisdiction cannot be used"
        elif s.startswith("REC") and j == "EU-DE" and w == "ABSENT":
            v, e = "BLOCK", "`WORKS_AGREEMENT_REQUIRED` (BetrVG s.87(1) no.6, verify): no coaching analytics on recordings of employees"
        elif op == "TEAM_AGGREGATE":
            v, e = "ALLOW", "Team aggregate with k >= 5 learners and >= 20 calls; no per-person value; groups below k suppressed"
        elif ro == "LEARNER":
            v, e = "ALLOW", "Learner sees own rubric feedback with cited timestamps; no score ranking"
        elif ro == "COACH":
            v, e = "ALLOW_IF_SHARED", "Coach sees the item only if the learner pressed Share (logged, revocable); otherwise 404"
        elif ro == "AUDITOR":
            v, e = "ALLOW_METADATA", "R15 sees processing metadata, lawful-basis evidence and access logs, not feedback content"
        else:
            v, e = "DENY", "HR role has no coaching read permission"
        tid = "TC-V12-Q-CP-%02d" % k
        cp.append("| %s | Coaching %s, %s, %s requests %s, works agreement %s | TS-V12-Q-08 · US-08-ZQ01 · FR-V12-Q-040…046; SM-SVC-36-WF03 | PP-Q-02 coaching fixture; source %s; rubric RB-Q-01 v2 | 1. Request coaching run / view as %s. 2. Inspect result, access log | **%s**: %s | P0 | T19, T07 | PW (2-way) | Y | SYS |" % (tid, j, s, ro, op, w, s, ro, v, e))
        cp_ex.append("      | %s | %s | %s | %s | %s | %s | %s |" % (tid, j, s, ro, op, w, v))
    open(os.path.join(outdir, "cp_tests.md"), "w").write("\n".join(cp) + "\n")
    open(os.path.join(outdir, "ex_coaching.md"), "w").write("\n".join(cp_ex) + "\n")
    cfull = 1
    for d_ in cdom:
        cfull *= len(d_)

    with open(os.path.join(outdir, "counts.txt"), "w") as f:
        f.write("C3_full_space=%d\nC3_triples=%d\nC3_pairs=%d\nC3_rows=%d\nC3_lower_bound=%d\nC3_stats=%s\n" % (
            full_space, total3, pair_total, len(rows), 7 * 6 * 5, stats))
        f.write("RX=56\nVM=63\nNX=42\nCP_full=%d\nCP_pairs=%d\nCP_rows=%d\n" % (cfull, ctot, len(crow)))
        f.write("OUT_rows=%d\nIN_rows=%d\n" % (len(ex_out), len(ex_in)))
    print(open(os.path.join(outdir, "counts.txt")).read())


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "q_out")
