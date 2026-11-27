from h_ep01 import R

INTRO = """Risk areas: RA-03 PDP, consent, suppression, jurisdiction, quiet hours and caps (P0, D4), RA-11 children (P0, D4), RA-12 health-data exclusion (P0, D4), RA-17 privacy requests and retention (P0, D3), RA-30 accessible public pages (P1 for WCAG cases). Waves W0 (US-0301, 0302, 0303, 0307, 0308), W2 (US-0304, 0305, 0306, 0310), W3 (US-0309, 0311). EP-03 owns the eligibility, privacy, retention, jurisdiction, children and health-data batteries (Part 6.1 §6.1.12.1); dispatch-engine behaviour around the PDP (outbox, uncertain outcomes, simulation, emergency stop) is owned by EP-18 (Batch 6.3) and only the PDP's own decisions are tested here. Every case asserts KPI-17 = 0 (no send to a suppressed or ineligible recipient)."""

EXTRA_TS = []

PDP_TABLE = """The oracle is Part 6.1 §6.1.11.3, reproduced here because this batch owns it. First-match in precedence order (deny-before-defer, compliance-before-commercial, ASSUMPTION-184); "–" = don't care. The PDP returns the primary reason and the list of all failed checks.

| Condition / Rule | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 | R12 | R13 | R14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 Same tenant/startup scope | N | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| C2 Emergency stop active | – | Y | N | N | N | N | N | N | N | N | N | N | N | N |
| C3 Suppressed (channel × purpose × startup or global) | – | – | Y | Y | N | N | N | N | N | N | N | N | N | N |
| C4 Lawful transactional notice | – | – | N | Y | – | – | – | – | – | – | – | – | Y | – |
| C5 Minor or learner-flagged | – | – | – | – | Y | N | N | N | N | N | N | N | N | N |
| C6 Health attributes in content/audience | – | – | – | – | – | Y | N | N | N | N | N | N | N | N |
| C7 Jurisdiction enabled (or reply in inbound thread) | – | – | – | – | – | – | N | Y | Y | Y | Y | Y | Y | Y |
| C8 Lawful basis recorded and known | – | – | – | – | – | – | – | N | Y | Y | Y | Y | Y | Y |
| C9 Approved hash = content hash, unexpired | – | – | – | – | – | – | – | – | N | Y | Y | Y | Y | Y |
| C10 Budget reservation succeeds | – | – | – | – | – | – | – | – | – | N | Y | Y | Y | Y |
| C11 Frequency cap would be exceeded | – | – | – | – | – | – | – | – | – | – | Y | N | N | N |
| C12 Inside recipient quiet hours | – | – | – | – | – | – | – | – | – | – | – | Y | Y | N |
| **Action** | 404 `SCOPE` | Deny `STOPPED` | Deny `SUPPRESSED`; cancel queued | Waived for transactional; continue | Deny `MINOR` | Deny `HEALTH_DATA` | Deny `JURISDICTION` | Deny `NO_LAWFUL_BASIS`; task | Deny `APPROVAL_STALE` | Deny `BUDGET` | Deny `FREQ_CAP` | Defer `QUIET_HOURS` | Allow (transactional) | **Allow** |

Each rule is one TC (TC rows R1…R14 below), plus four precedence pairs and a Hypothesis property test that compares the PDP with an independent implementation of this table (12 booleans + context, `release` profile 10,000 examples)."""

GROUPS = [
    dict(ts="US-0303", heading="Decision table – Policy Decision Point at dispatch (R1…R14, precedence pairs, PBT oracle)", tech="DT, PBT", intro=PDP_TABLE, rows=[
        R("R1: deny a decision for an object in another scope with uniform 404 and no decision record", "AC-0304-09; BRL-TEN-03, BRL-TEN-04; DM-R03",
          "T1 caller (R19 worker scoped AppNAI); contact ID belongs to T2",
          "1. `decide(action_type=email.send, scope=T1/AppNAI, subject=T2 contact, mode=dispatch)`",
          "404; 0 decision rows; audit outcome=denied rule BRL-TEN-04",
          "P0", "T15", "DT", "Y", "UT"),
        R("R2: deny every external action within 60 s of an emergency stop", "AC-0303-06; BRL-AUT-05; DM-R38",
          "Emergency stop OrganicSpec at 2027-03-02T10:12:00+05:30; clock control",
          "1. decide at 10:12:59 (stop propagating). 2. decide at 10:13:00 and 10:13:01",
          "1: may allow only if issued before propagation (recorded). 2: deny `EMERGENCY_STOP` (STOPPED) for every external action type",
          "P0", "T19", "DT", "Y", "IT"),
        R("R3: deny a suppressed recipient at dispatch even after a plan-time allow and release the reservation", "AC-0303-03; BRL-ELG-02, BRL-ELG-18; E-3",
          "decide(plan) allow at 10:00; opt-out at 10:05; budget reservation RSV-1",
          "1. decide(dispatch) at 10:06",
          "deny `SUPPRESSED` rule BRL-ELG-02; step cancelled; RSV-1 released; 0 provider calls",
          "P0", "T19", "DT", "Y", "IT"),
        R("R4 → R13: allow a lawful transactional invoice notice to a marketing-suppressed customer, also in quiet hours", "AC-0301-05; BRL-ELG-02, BRL-ELG-08",
          "Subject suppressed for marketing email; invoice notice flagged transactional; clock 20:30 recipient local",
          "1. decide(dispatch)",
          "allow with reasons `TRANSACTIONAL_EXEMPT` and quiet-hours exception; decision lists the waived checks",
          "P0", "T19", "DT", "Y", "UT"),
        R("R5: deny outbound to a learner aged 13–17 on every channel", "AC-0304-07; BRL-ELG-13; DEC-030",
          "EduVerse contact Learner-U18-01, age band 13–17",
          "1. decide for email, WhatsApp, SMS-like channel and portal message",
          "Each deny `MINOR`; only the verified guardian channel may be evaluated",
          "P0", "T19", "DT", "Y", "UT"),
        R("R6: deny content or audience carrying health attributes", "US-0304; BRL-ELG-14; BRL-PRV-06; AP-05",
          "MedMaarg message body contains a synthetic diagnosis from EDGE-HEALTH; audience filter on `condition=diabetes`",
          "1. decide for the message. 2. decide for the audience build",
          "1–2: deny `HEALTH_DATA`; nothing queued",
          "P0", "T19", "DT", "Y", "UT"),
        R("R7: unresolvable jurisdiction returns unknown, treated as no send, and creates a task", "AC-0303-02; BRL-ELG-01, BRL-ELG-05",
          "Contact and organization country null",
          "1. decide(dispatch)",
          "decision `unknown`; dispatcher treats as deny; task \"Resolve jurisdiction\" created; 0 provider calls",
          "P0", "T19", "DT", "Y", "UT"),
        R("R8: deny when no lawful basis is recorded for purpose and channel", "AC-0301-03; BRL-ELG-03",
          "`cfo@lnt-infra.example.com` Verified, no consent or lawful basis",
          "1. decide(email, purpose=marketing)",
          "deny `NO_LAWFUL_BASIS`; task to record basis; Verified ≠ consent",
          "P0", "T19", "DT", "Y", "UT"),
        R("R9: deny when the content hash differs from the approved hash", "AC-0303-04; BRL-APR-02",
          "Approved hash `sha256:ab12…`; content hashes to `sha256:cd34…`",
          "1. decide(dispatch, approval_hash=ab12…)",
          "deny `APPROVAL_HASH_MISMATCH`",
          "P0", "T19", "DT", "Y", "UT"),
        R("R10: deny when the budget reservation fails", "US-0303; BRL-AI-08; BRL-SVC-03",
          "Channel budget exhausted for AppNAI",
          "1. decide(dispatch)",
          "deny `BUDGET`; 0 provider calls",
          "P0", "T20", "DT", "Y", "UT"),
        R("R11: deny the third marketing touch within 7 days", "AC-0304-06; BRL-ELG-09",
          "2 marketing emails on 2027-02-10 and 2027-02-13",
          "1. decide for 2027-02-16",
          "deny `FREQ_CAP` \"Frequency cap reached: 2 per 7 days\"",
          "P0", "T19", "DT", "Y", "UT"),
        R("R12: defer a marketing email planned inside quiet hours to the next window", "AC-0304-05; BRL-ELG-08",
          "US contact America/New_York; planned 2027-03-15T06:30:00+05:30 (21:00 EDT 14 Mar)",
          "1. decide(dispatch)",
          "defer `QUIET_HOURS` to 2027-03-15T09:00:00-04:00",
          "P0", "T19", "DT", "Y", "UT"),
        R("R14: allow an eligible India B2B recipient with a complete, immutable decision record", "AC-0303-01, AC-0304-01; BRL-ELG-01…09; E-1",
          "`it.head@infra-co.example.in` India, lawful basis recorded, 0 touches, approved hash matches; 2027-02-15T11:00:00+05:30",
          "1. decide(dispatch). 2. Attempt UPDATE of the decision row",
          "1: allow; rule IDs evaluated, policy versions, decision ID linked to correlation ID. 2: refused (immutable)",
          "P0", "T19", "DT", "Y", "IT"),
        R("Precedence C3+C7: suppressed recipient in a non-enabled jurisdiction reports SUPPRESSED first and lists both", "AC-0303-03; BRL-ELG-02, BRL-ELG-05",
          "Suppressed contact in BR",
          "1. decide(dispatch)",
          "primary `SUPPRESSED`; failed checks [SUPPRESSED, JURISDICTION]",
          "P0", "T19", "DT", "Y", "UT"),
        R("Precedence C2+C3 and C5+C8: STOPPED outranks SUPPRESSED; MINOR outranks NO_LAWFUL_BASIS", "AC-0303-06, AC-0304-07; BRL-AUT-05, BRL-ELG-13",
          "Two condition vectors",
          "1. decide each",
          "primary `STOPPED` then `MINOR`; all failed checks listed",
          "P0", "T19", "DT", "Y", "UT"),
        R("Precedence C11+C12: frequency cap denies instead of deferring into the next quiet-hours window", "AC-0304-06; BRL-ELG-09, BRL-ELG-08",
          "Cap reached and planned at 20:00 local",
          "1. decide",
          "deny `FREQ_CAP` (not defer)",
          "P0", "T19", "DT", "Y", "UT"),
        R("Property: PDP equals the independent decision-table oracle for random condition vectors", "AC-0303-08; BRL-ELG-01, BRL-ELG-18; Part 6.1 §6.1.11.7",
          "Hypothesis strategy: 12 booleans + channel + mode; profiles ci 100, nightly 2,000, release 10,000",
          "1. Generate vectors; call PDP and oracle",
          "Decision and primary reason identical for all examples; failing examples stored and promoted to explicit regression tests",
          "P0", "T19", "PBT", "Y", "UT"),
        R("Deny AI-initiated consequential actions above the autonomy cap", "AC-0303-05; BRL-AI-07; DEC-064",
          "Agent identity AG-negotiation (R20)",
          "1. decide(action quote.send, autonomy L2). 2. decide(action quote.draft, L1)",
          "1: deny `AUTONOMY_CAP_L1`. 2: allow draft only",
          "P0", "T19", "DT", "Y", "UT"),
        R("Mark simulate-mode allows as simulated so the dispatcher refuses a provider call", "AC-0303-07; NFR-038; E-6",
          "decide(mode=simulate) for an eligible send",
          "1. Pass the result to the dispatcher",
          "result `simulated=true`; dispatcher refuses; provider simulator call log empty; 0 budget rows",
          "P0", "T17", "DT", "Y", "IT"),
        R("Reject a malformed decision request and write no decision record", "AC-0303-09; BRL-ELG-01",
          "Requests without action_type; with channel `fax`",
          "1. decide each",
          "400 `INVALID_DECISION_REQUEST` listing fields; no decision row; caller treats as deny",
          "P0", "T19", "EP", "Y", "UT"),
        R("Return identical decisions 1,000 times with p95 ≤ 100 ms", "AC-0303-08; ASSUMPTION-156; NFR-039",
          "Fixed policy versions",
          "1. Same request 1,000 times under 20 concurrent callers",
          "1,000 identical decisions; p95 ≤ 100 ms",
          "P1", "T03", "EG", "Y", "IT"),
    ]),
    dict(ts="US-0304", heading="Equivalence partitioning – recipient jurisdiction for first-touch email (DEC-029)", tech="EP",
         intro="""Partitions from Part 6.1 §6.1.11.1 (10 classes replace 200+ country values). A data test asserts every enabled country maps to exactly one pack.

| Class | Representative | Expected |
|---|---|---|
| EP-J1 India, basis recorded | IN | Eligible |
| EP-J2 EU/EEA/UK role-based address, LIA, one-click opt-out | DE `procurement@stadtwerke.example.de` | Eligible |
| EP-J3 EU/EEA/UK personal address or no LIA | NL `jan.devries@gmail.example.com` | Ineligible `EU_LIA_OR_ROLE_ADDRESS_REQUIRED` |
| EP-J4 US with identification, address, opt-out | US | Eligible |
| EP-J5 US template missing physical address | US | Denied at template validation |
| EP-J6 UAE/SG/AU with opt-in | AE | Eligible |
| EP-J7 UAE/SG/AU without opt-in | SG | `OPT_IN_REQUIRED` |
| EP-J8 Listed but not enabled | BR | `JURISDICTION_NOT_ENABLED` |
| EP-J9 Unknown | null | `unknown` → no send |
| EP-J10 Reply in inbound thread | BR reply | Eligible (exception) |""",
         rows=[
        R("EP-J1: India recipient with recorded lawful basis is eligible", "AC-0304-01; BRL-ELG-05; DEC-029", "Policy Outbound – AppNAI v2; IN contact", "1. Eligibility check for email", "Eligible; rules ELG-01…09 passed", "P0", "T19", "EP", "Y", "UT"),
        R("EP-J2: EU role-based address with LIA-2027-004 is eligible and requires one-click opt-out", "AC-0304-04; BRL-ELG-06", "DE contact published on the tender page", "1. Check. 2. Validate template without List-Unsubscribe", "1: Eligible. 2: template validation fails \"one-click opt-out required\"", "P0", "T19", "EP", "Y", "UT"),
        R("EP-J3: EU personal address without LIA is ineligible", "AC-0304-03; BRL-ELG-06", "NL contact `jan.devries@gmail.example.com`", "1. Check", "Ineligible with the EU/UK reason text; nothing queued", "P0", "T19", "EP", "Y", "UT"),
        R("EP-J4/J5: US recipient allowed only with a template carrying physical address and opt-out", "US-0304; BRL-ELG-05; DEC-029", "US contact; templates T-US-ok and T-US-noaddr", "1. Check with T-US-ok. 2. With T-US-noaddr", "1: Eligible. 2: denied at template validation (CAN-SPAM pack; verify with counsel)", "P0", "T19", "EP", "Y", "UT"),
        R("EP-J6/J7: UAE with opt-in allowed; Singapore without opt-in denied", "US-0304; BRL-ELG-05; DEC-029", "AE contact with opt-in; SG contact without", "1. Check each", "AE Eligible; SG `OPT_IN_REQUIRED`", "P0", "T19", "EP", "Y", "UT"),
        R("EP-J8: Brazil first-touch denied with the UI reason text", "AC-0304-02; BRL-ELG-05", "Contact country Brazil", "1. Check. 2. Render BlockedReason in A034 preview", "1: Ineligible. 2: \"Blocked: recipient's jurisdiction (Brazil) is not enabled for outbound email (BRL-ELG-05)\"", "P0", "T19", "EP", "Y", "SYS"),
        R("EP-J10: reply inside an inbound thread from Brazil is allowed", "US-0304; BRL-ELG-05", "Inbound email from BR contact on 2027-02-15", "1. Check reply in that thread", "Eligible (inbound-reply exception); first-touch to the same contact still denied", "P0", "T19", "EP", "Y", "UT"),
    ]),
    dict(ts="US-0304", heading="Boundary values – quiet hours, frequency cap and age (BRL-ELG-08, -09, -13)", tech="BVA",
         intro="""Window [09:00, 19:00) recipient local time, Monday–Saturday, India public holidays excluded for IN recipients (ASSUMPTION-184). Cap: 2 marketing touches per rolling 7 days per channel. Age: 17 years 364 days → minor; 18 years 0 days → adult; birthday evaluated at IST midnight for IN learners (ASSUMPTION-196).

| Variable | Values (expected) |
|---|---|
| IST local time | 08:59:59 defer · 09:00:00 allow · 18:59:59 allow · 19:00:00 defer · Sunday 10:00 defer · 2027-01-26 (Republic Day) 10:00 defer |
| New York across DST (14 Mar 2027) | 08:59:59 EDT defer · 09:00:00 EDT allow |
| Touch at t + Δ after first of 2 touches (t = 2027-02-10T10:00 IST) | Δ = 6 d 23 h 59 m 59 s deny · Δ = 7 d allow |
| Age at evaluation | 17 y 364 d minor · 18 y 0 d adult · unknown age with learner flag minor (fail closed) |""",
         rows=[
        R("Quiet hours IST: defer at 08:59:59 and 19:00:00, allow at 09:00:00 and 18:59:59", "AC-0304-05; BRL-ELG-08; ASSUMPTION-184", "IN contact eligible otherwise; clock control", "1. decide at each instant on Monday 2027-02-15", "Defer, allow, allow, defer respectively; deferral target = next 09:00 IST", "P0", "T19", "BVA", "Y", "UT"),
        R("Quiet hours: Sunday and an India public holiday defer to the next allowed day", "AC-0304-05; BRL-ELG-08", "IN contact; holiday calendar CFG with 2027-01-26", "1. decide Sunday 2027-02-14 10:00. 2. decide 2027-01-26 10:00", "1: defer to Mon 2027-02-15 09:00. 2: defer to 2027-01-27 09:00", "P0", "T19", "BVA", "Y", "UT"),
        R("Quiet hours in New York on the DST change day", "AC-0304-05; BRL-ELG-08; I18N-03; DM-R35", "US contact America/New_York; 2027-03-14 is DST start", "1. decide 2027-03-15 08:59:59 EDT and 09:00:00 EDT. 2. decide 2027-03-15T20:30:00+05:30", "1: defer, allow. 2: allow (11:00 EDT)", "P0", "T13", "BVA", "Y", "UT"),
        R("Frequency cap: deny at 6 d 23 h 59 m 59 s and allow at exactly 7 days after the first touch", "AC-0304-06; BRL-ELG-09", "Touches 2027-02-10T10:00 and 2027-02-13T10:00 IST", "1. decide 2027-02-17T09:59:59. 2. decide 2027-02-17T10:00:00", "1: deny FREQ_CAP. 2: allow", "P0", "T19", "BVA", "Y", "UT"),
        R("Frequency cap is per channel and excludes replies to the recipient's own inbound", "AC-0304-06; BRL-ELG-09", "2 marketing emails in 7 days", "1. decide a WhatsApp template touch. 2. decide an email reply to an inbound message", "1: evaluated against the WhatsApp counter (allow if 0 touches). 2: allow (reply not counted)", "P0", "T19", "EP", "Y", "UT"),
        R("Age boundary: 17 y 364 d is a minor, 18 y 0 d an adult; unknown age with learner flag is a minor", "AC-0304-07; BRL-ELG-13; DEC-030", "EDGE-MINORS: born 2009-02-16 and 2009-02-15, evaluated 2027-02-15 IST; school-learner flag without age", "1. decide outbound for each", "deny MINOR · allow (adult rules) · deny MINOR", "P0", "T19", "BVA", "Y", "UT"),
        R("Halt a generic follow-up after a substantive reply unless the owner chose to continue", "AC-0304-10; BRL-ELG-10", "Reply \"Please send a proposal\" at 10:00; generic step due 10:30", "1. decide at 10:30. 2. Owner records continue; decide again", "1: deny `REPLY_RECEIVED`. 2: allow", "P0", "T19", "DT", "Y", "UT"),
        R("A rejected opportunity blocks its contacts while a score of 92 changes nothing for another contact", "AC-0304-08; BRL-ELG-15, BRL-ELG-04", "OPP rejected; other contact with score 92 but no lawful basis", "1. decide both", "Rejected: Ineligible (BRL-ELG-15). Score 92 contact: still `NO_LAWFUL_BASIS`", "P0", "T19", "DT", "Y", "UT"),
    ]),
    dict(ts="US-0301", heading="Error guessing and replay – suppression keys, propagation and duplicates", tech="EG",
         intro="Suppression is keyed by a normalized address hash (email lower-cased and Unicode-NFC normalized; phone E.164) so it survives deletion (BRL-PRV-03). Error-guessing items EG-08 and EG-03 from Part 6.1 §6.1.11.6.", rows=[
        R("Cancel 2 queued emails and 1 scheduled step in the same transaction as the opt-out", "AC-0301-01; BRL-ELG-02; NFR-036", "Background of US-0301 (dr.nair@kims-hospital.example.com, MedMaarg)", "1. Record email opt-out purpose marketing at 2027-02-10T11:00:00+05:30. 2. Inspect queue, outbox and simulator", "Suppression row (hash, email, marketing, MedMaarg); 3 items cancelled `SUPPRESSED`; NT-008 logged; 0 provider calls", "P0", "T19", "UC", "Y", "IT"),
        R("Match suppression across case and Unicode variants of the same address", "AC-0301-01; BRL-ELG-02; EG-08", "Suppressed `dr.nair@kims-hospital.example.com`", "1. decide for `Dr.Nair@KIMS-Hospital.example.com`. 2. For an NFD-composed variant of the local part", "1–2: deny SUPPRESSED (same hash)", "P0", "T19", "EG", "Y", "UT"),
        R("Match phone suppression across +91 98765 43210, 09876543210 and +919876543210", "US-0301; BRL-ELG-02; EG-08", "Phone suppressed in E.164 form", "1. decide for each input form", "All deny SUPPRESSED", "P0", "T19", "EG", "Y", "UT"),
        R("Apply a tenant-global opt-out to all four seed startups", "AC-0301-02; BRL-ELG-02", "Opt-out \"from all communications\" in T1", "1. decide for AppNAI, MedMaarg, EduVerse, OrganicSpec. 2. decide for T2 with the same address", "1: all deny SUPPRESSED. 2: not affected (tenant scope)", "P0", "T19", "EP", "Y", "UT"),
        R("Record one suppression for three deliveries of ses-evt-77", "AC-0301-04; NFR-005", "Provider event ID ses-evt-77", "1. Deliver 3 times", "1 suppression; 2 deliveries `duplicate – no effect`", "P0", "T16", "EG", "Y", "IT"),
        R("Cancel all queued messages for 1,200 suppressed recipients within 60 s", "AC-0301-08; NFR-036", "Campaign with 5,000 queued messages", "1. Bulk import 1,200 opt-outs. 2. Poll queue", "All affected messages cancelled ≤ 60 s; 0 dispatched", "P0", "T19", "EG", "Y", "SYS"),
    ]),
    dict(ts="US-0307", heading="State transition and boundaries – privacy request lifecycle", tech="ST, BVA",
         intro="""```mermaid
stateDiagram-v2
  [*] --> Received
  Received --> IdentityVerification : verification sent
  IdentityVerification --> InProgress : identity verified
  IdentityVerification --> Rejected : not verified by deadline
  InProgress --> OnLegalHold : held category found
  OnLegalHold --> Restricted : restrict processing
  InProgress --> Fulfilled : executed
  Restricted --> Fulfilled : remaining categories executed
  Fulfilled --> Closed : response sent
  Rejected --> Closed : response sent
  Closed --> [*]
```

| From \\ Event | verify identity | execute (R10) | execute (other role) | legal hold found | close |
|---|---|---|---|---|---|
| Received | → IdentityVerification | disabled "Verify the requester's identity first" | 403 | — | 409 |
| IdentityVerification | → InProgress | disabled | 403 | — | 409 |
| InProgress | 409 | → Fulfilled | 403 | → OnLegalHold | 409 |
| OnLegalHold / Restricted | 409 | restrict, then → Fulfilled | 403 | — | 409 |
| Fulfilled | 409 | idempotent (one job) | 403 | — | → Closed |

Deadline: `privacy_response_days` = 30 (test value, GAP-151); request PRV-2027-0042 received 2027-02-01T10:00:00+05:30 → deadline 2027-03-03T10:00:00+05:30; 70% = 21 days → 2027-02-22T10:00:00+05:30.""",
         rows=[
        R("Disable execution before identity verification", "AC-0307-03; FR-A013; BRL-PRV-01", "PRV-2027-0042 Received", "1. R10 clicks Fulfil. 2. POST execute via API", "1: disabled \"Verify the requester's identity first\". 2: 409 `IDENTITY_NOT_VERIFIED`; no deletion job", "P0", "T19", "ST", "Y", "SYS"),
        R("Delete after verification and keep a hashed all-channel suppression tombstone", "AC-0307-01; FR-A013; BRL-PRV-03", "Identity verified by OTP to the address on record", "1. R10 executes deletion for parent.k@example.com. 2. Import a CSV containing the address", "1: contact and lead deleted/anonymized; suppression hash for all channels; Fulfilled. 2: row flagged suppressed; contact never eligible", "P0", "T19", "ST", "Y", "SYS"),
        R("Restrict the held invoice instead of deleting it under legal hold until 2034-03-31", "AC-0307-02; BRL-PRV-04; DEC-028", "Invoice for the subject under legal hold", "1. Execute deletion", "OnLegalHold → Restricted: invoice access limited to R10/R08, no processing; response explains retained category; other categories deleted", "P0", "T19", "ST", "Y", "SYS"),
        R("Escalate at 70% of the deadline and not one second earlier", "AC-0307-04; BRL-PRV-02; NT-029", "Clock control", "1. Clock 2027-02-22T09:59:59+05:30. 2. Clock 10:00:00", "1: no NT-029. 2: NT-029 High to R10 once", "P0", "T19", "BVA", "Y", "SYS"),
        R("Reject an unverified request at the deadline and close it", "US-0307; BRL-PRV-01, BRL-PRV-02", "Verification never completed", "1. Clock 2027-03-03T10:00:00+05:30", "Rejected with reason \"identity not verified\"; response sent; Closed; no data disclosed", "P0", "T19", "ST", "Y", "SYS"),
        R("Run one deletion job when Execute is submitted twice", "AC-0307-07; NFR-005", "Verified request", "1. POST execute twice with the same idempotency key, then with a new key", "One deletion job; audit shows one fulfilment; second key returns 409 `ALREADY_FULFILLED`", "P0", "T16", "EG", "Y", "IT"),
        R("Produce an access export with classification-aware redaction and a link valid for 72 h", "AC-0307-06; BRL-PRV-07", "Access request verified; export at 2027-02-05T12:00:00+05:30", "1. Fulfil. 2. Open link at +71 h 59 m. 3. Open at +72 h", "1: export with redaction. 2: download. 3: expired page", "P0", "T19", "BVA", "Y", "SYS"),
    ]),
    dict(ts="US-0308", heading="Boundary values and decision table – retention purge by data class (DEC-028)", tech="BVA, DT",
         intro="""Interpretation [ASSUMPTION-196]: a record becomes purge-eligible at the first nightly run whose IST date is ≥ the anchor date plus the retention period in calendar months or days; the run at 02:00 IST on that date purges it.

| Data class (DEC-028) | Anchor | Period | Last retained run | First purge run |
|---|---|---|---|---|
| Rejected/withdrawn lead | rejected 2027-01-10 | 6 months | 2027-07-09 02:00 | 2027-07-10 02:00 |
| AI run payload (redacted) | logged 2027-01-01 | 90 days | 2027-03-31 02:00 | 2027-04-01 02:00 |
| Application draft | created 2027-03-01 | 30 days | 2027-03-30 02:00 | 2027-03-31 02:00 |
| Suppression hash | any | indefinite | always | never |

| Rule | Legal hold | Class suppression | Eligible by date | Action |
|---|---|---|---|---|
| P1 | Y | – | – | skip; report "held" |
| P2 | N | Y | – | keep (never purged) |
| P3 | N | N | N | keep |
| P4 | N | N | Y | purge personal fields; keep aggregate; audit with policy version |""",
         rows=[
        R("Retain the rejected lead on 2027-07-09 and purge it on 2027-07-10", "AC-0308-01, AC-0308-02; FR-A013; BRL-PRV-05; DEC-028", "Lead L-3381 rejected 2027-01-10", "1. Run purge 2027-07-09T02:00 IST. 2. Run 2027-07-10T02:00 IST", "1: retained. 2: personal fields deleted; aggregate count kept; audit `retention.purged` with policy version", "P0", "T19", "BVA", "Y", "IT"),
        R("P1: skip a contact under legal hold and report it", "AC-0308-03; BRL-PRV-04", "C-2201 under legal hold, eligible by date", "1. Run purge", "C-2201 retained; report \"held: 1\"", "P0", "T19", "DT", "Y", "IT"),
        R("P2: never purge suppression hashes older than 24 months", "AC-0308-04; BRL-PRV-03", "Suppression rows dated 2024-01-01", "1. Run purge", "All suppression rows remain", "P0", "T19", "DT", "Y", "IT"),
        R("Purge application drafts at 30 days and AI payloads at 90 days", "US-0308; BRL-PRV-05; DEC-028; BRL-SVC-02", "Draft created 2027-03-01; run MR-1001 logged 2027-01-01", "1. Runs on 2027-03-30, 03-31, 04-01", "Draft: retained 03-30, purged 03-31. Payload: retained 03-31, purged 04-01; digests and aggregates kept", "P0", "T19", "BVA", "Y", "IT"),
        R("Accept a stricter override and refuse a looser one", "AC-0308-05; BRL-APR-11; CFG-28", "Approved schedule: marketing contacts 24 months", "1. R10 sets 18 months. 2. R10 sets 36 months", "1: accepted, audited. 2: rejected \"Overrides may only be stricter than the approved schedule\"", "P0", "T19", "BVA", "Y", "SYS"),
        R("Process 100,000 eligible rows in batches of 5,000 inside the 02:00–04:00 window and resume next night", "AC-0308-06; NFR-036", "100,000 eligible rows; throttled DB to force overflow", "1. Run purge; stop at 04:00. 2. Next night", "Batches of 5,000; stops by 04:00; resumes; total purged 100,000; no row purged twice", "P1", "T19", "EG", "Y", "IT"),
    ]),
    dict(ts="US-0309", heading="Boundary values – complaint and bounce containment (BRL-ELG-11, -12)", tech="BVA",
         intro="""Pause when the campaign's 24 h complaint rate exceeds 0.10% **or** 3 complaints occur within a rolling 24 h. Bounce rules (BRL-ELG-12, containment contract consumed by EP-08): hard bounce → suppress immediately; 3 soft bounces in 7 days → suppress.

| Deliveries in 24 h | Complaints | Rate | Expected |
|---|---|---|---|
| 2,000 | 2 | 0.10% (not exceeded) | continue |
| 2,000 | 3 | 0.15% | pause (count rule) |
| 1,000 | 2 | 0.20% | pause (rate rule) |
| 2,001 | 2 | 0.0999% | continue |""",
         rows=[
        R("Continue at 2 complaints on 2,000 deliveries and suppress the complainants", "AC-0309-05; BRL-ELG-11", "Campaign MM-Clinics-Feb, 2,000 deliveries from 2027-02-20T09:00 IST", "1. Deliver 2 complaint events", "Campaign continues; both complainants suppressed", "P0", "T19", "BVA", "Y", "SYS"),
        R("Pause on the 3rd complaint within 24 h and open incident CI-0007 within 60 s", "AC-0309-01; BRL-ELG-11; BRL-AUT-05", "As above", "1. 3rd complaint at 2027-02-20T15:10 IST", "Pause ≤ 60 s; incident Contained; NT-027 Critical to R10, R05L, R02; queued steps get `CONTAINMENT_PAUSE`", "P0", "T19", "BVA", "Y", "SYS"),
        R("Pause on rate: 2 complaints on 1,000 deliveries", "US-0309; BRL-ELG-11", "Campaign with 1,000 deliveries", "1. Deliver 2 complaints", "Pause (0.20% > 0.10%)", "P0", "T19", "BVA", "Y", "SYS"),
        R("Do not count a complaint that falls outside the rolling 24 h window", "US-0309; BRL-ELG-11", "Complaints at 2027-02-20T09:00, 2027-02-21T08:59:59 and 2027-02-21T09:00:01 IST on 5,000 deliveries", "1. Evaluate after each", "Never 3 in any 24 h window → continue; all three complainants suppressed", "P0", "T19", "BVA", "Y", "SYS"),
        R("Suppress on a hard bounce and on the 3rd soft bounce in 7 days, not the 2nd", "US-0309; BRL-ELG-12", "Address A hard-bounces; address B soft-bounces on days 1, 3, 6", "1. Process bounce events", "A suppressed immediately; B suppressed after the 3rd soft bounce only; NT to R05L", "P0", "T19", "BVA", "Y", "IT"),
        R("Count a re-sent complaint event once", "AC-0309-06; NFR-005", "Event cmp-55 delivered twice", "1. Deliver twice", "Complaint count +1", "P0", "T16", "EG", "Y", "IT"),
    ]),
]

TS_TITLE = {
    "US-0301": "Opt-outs suppress across queued and scheduled work, by normalized address",
    "US-0302": "Policy versions: tightening is immediate, loosening needs approval",
    "US-0303": "PDP decides plan-time and dispatch-time with immutable records",
    "US-0304": "Eligibility rules: consent, jurisdiction, quiet hours, caps, minors, health",
    "US-0305": "Public opt-out and preferences without enumeration",
    "US-0306": "Contact, privacy and help intake with minimization",
    "US-0307": "Privacy requests verified, fulfilled or restricted under legal hold",
    "US-0308": "Retention purge at the right boundary, never purging suppression",
    "US-0309": "Complaint thresholds pause campaigns and open incidents",
    "US-0310": "Opt-out, preference and privacy pages meet WCAG 2.2 AA",
    "US-0311": "Compliance metrics and alerts per startup and channel",
}
