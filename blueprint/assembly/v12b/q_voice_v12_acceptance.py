#!/usr/bin/env python3
"""Group Q (Part 11.18): turn every V12 acceptance test of SM-SVC-26 WF01-WF04 and
SM-SVC-36-WF03 (FSD chapter 33) into an executable test case in the Part 6.2a format.

Usage: python3 -I q_voice_v12_acceptance.py <v12_dir> <out_dir>
Writes <out_dir>/v12acc_tests.md (workflow tests TC-V12-Q-101..146, step tests TC-V12-Q-151..165).
"""
import glob
import os
import re
import sys

V12, OUT = sys.argv[1], sys.argv[2]
f33 = open(glob.glob(os.path.join(V12, "FSD", "33_*.txt"))[0], encoding="utf-8").read().split("\n")

# Voice-specific concretisation of the V12 generic test kinds
VOICE = {
    "POS": ("Happy path with a consented caller/contact in IN (pack Approved), language en, recording consent given",
            "Expected V12 output produced; disclosure event first; recording from consent time; disposition written; meter committed; no unapproved effect"),
    "INPUT": ("Malformed DTO (missing `contact_ref` for outbound / missing number mapping for inbound; invalid `script_ref` hash)",
              "400 with JSON-pointer errors or HELD before any provider request; audit `INPUT_INVALID`; 0 minutes metered"),
    "SCOPE": ("Same `call_ref`/`contact_ref` presented from tenant B / other startup",
              "Uniform 404 (BRL-TEN-04); RLS denies under `app_rw`; no session data leaked; provider not called"),
    "ENT": ("Revoke SKU SM-SVC-26 (or pack moves to Retired) after enqueue, before dial / mid-call",
            "Queued: no new dial (`ENTITLEMENT_REVOKED`); active call: AI finishes the current sentence, offers human or ends gracefully; no new effects"),
    "DUP": ("Replay identical provider webhook / identical dial request with same idempotency key",
            "Single session, single dial, single meter event (unique `event_key`); duplicate acknowledged without effect"),
    "QUALITY": ("Stale or conflicting knowledge entry; ASR confidence < 0.60 for 3 turns",
                "AI does not answer from stale/conflicting source (bridge + handoff H-2); claim check drops uncited sentences; QA finding raised"),
    "BUDGET": ("Minute budget exhausted at reservation (AU-287)",
               "Outbound: BLOCK `BUDGET_EXHAUSTED`, no dial; inbound: AI not engaged, route to human/IVR (ladder L3); 0 provider AI cost"),
    "RECOVERY": ("Provider timeout after dial request; worker crash mid-call",
                 "Session RECONCILING; CDR queried by idempotency key; no redial until reconciled; call state restored from checkpoint; audit"),
    "APPROVAL": ("Campaign digest or script changed after approval / approval expired before dial",
                 "409 `DIGEST_CHANGED` / `APPROVAL_EXPIRED`; no dial; new approval required (AU-175)"),
    "EFFECT": ("Provider accepts the call but the response is lost",
               "Query provider by idempotency key / call reference; never place a second call; meter once"),
}
WF_CTX = {
    "26-WF01": ("US-22-ZQ01", "FR-V12-Q-001, 002, 009", "inbound"),
    "26-WF02": ("US-22-ZQ03", "FR-V12-Q-010, 011, 014", "outbound"),
    "26-WF03": ("US-22-ZQ07", "FR-V12-Q-017, 018", "booking"),
    "26-WF04": ("US-22-ZQ11", "FR-V12-Q-019, 024, 026, 027", "post-call"),
    "36-WF03": ("US-08-ZQ01", "FR-V12-Q-040, 043, 046", "coaching"),
}
COACH = {
    "POS": ("Learner requests feedback on a call recorded with coaching consent from all parties (UK)", "Feedback with timestamped observations visible only to the learner"),
    "INPUT": ("Missing `authorized_session_ref` or rubric version", "Rejected before model call; reason shown"),
    "SCOPE": ("Coach from another startup requests the feedback", "Uniform 404"),
    "ENT": ("SM-SVC-36 revoked after request", "No new feedback; existing items stay for the learner until retention"),
    "DUP": ("Same request replayed", "One feedback item"),
    "QUALITY": ("Transcript confidence low or rubric item unsupported", "Observation omitted; no invented quotes"),
    "BUDGET": ("Coaching-session meter exhausted", "Request held with reason; no model call"),
    "RECOVERY": ("Worker crash during Batch run", "Run resumed from checkpoint; no duplicate feedback"),
}

rows = ["| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |",
        "|---|---|---|---|---|---|---|---|---|---|---|"]
n = 100
srows = ["| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
m = 150
for k, l in enumerate(f33):
    mt = re.fullmatch(r"SM-SVC-(26-WF0[1-4]|36-WF03)-TC-([A-Z]+)", l)
    if mt:
        wf, kind = mt.group(1), mt.group(2)
        cond, exp = f33[k + 2], f33[k + 3]
        story, frs, flavour = WF_CTX[wf]
        vc, ve = (COACH if wf.startswith("36") else VOICE)[kind]
        n += 1
        rows.append("| TC-V12-Q-%03d | %s %s (%s) | TS-V12-Q-09 · %s · %s; V12 %s | PP-Q-01; V12 condition: %s. Voice data: %s | 1. Arrange the condition. 2. Execute the %s workflow through API-V12-Q-* or the simulator. 3. Inspect session, outbox, provider simulator log, meter and audit | V12 expectation: %s. Voice expectation: %s | %s | T01, T19%s | EG | Y | SYS |" % (
            n, l, kind.title(), flavour, story, frs, l, cond, vc, flavour, exp, ve,
            "P0" if kind in ("SCOPE", "ENT", "DUP", "BUDGET", "RECOVERY", "APPROVAL", "EFFECT") else "P1",
            ", T15" if kind == "SCOPE" else ", T16" if kind in ("DUP", "EFFECT") else ", T18" if kind == "RECOVERY" else ", T20" if kind == "BUDGET" else ""))
    ms = re.fullmatch(r"SM-SVC-(26-WF0[1-4]|36-WF03)-(STEP-0\d)-TC", l)
    if ms:
        m += 1
        kind, action, check = f33[k + 1], f33[k + 2], f33[k + 3]
        story, frs, flavour = WF_CTX[ms.group(1)]
        srows.append("| TC-V12-Q-%03d | %s %s | TS-V12-Q-09 · %s · %s | PP-Q-01 golden fixture for %s; step class %s | Run the step in isolation with the golden fixture and with an invalid-state fixture | V12: %s. Voice: model calls = 0 unless the step is an AI-inference step (AU-150); invalid state → HELD with reason code; output validates against the step contract | P1 | T01 | UC | Y | UT |" % (
            m, l, action, story, frs, action, kind, check))

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "v12acc_tests.md"), "w").write("\n".join(rows) + "\n\n**Step tests (V12 `…-STEP-0n-TC`).**\n\n" + "\n".join(srows) + "\n")
print(n - 100, m - 150)
