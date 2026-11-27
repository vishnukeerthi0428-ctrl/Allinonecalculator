from h_ep01 import R

INTRO = """Risk areas RA-23 CRM, lead capture and Customer 360 (P1, D3), RA-11 children and guardian consent for the EduVerse intake (P0, D4), RA-12 health-data minimization at intake (P0), RA-17 import consent gating (P0 for eligibility), RA-01 for cross-tenant intake. Waves W1 (US-0708 import), W2 (US-0701…0705, 0707, 0709, 0710), W3 (US-0706). Public intake cases run against the Website/Portal BFF with the abuse controls of Part 2.4 §2.35.3; deal stages owned by EP-13/EP-15 (Committed → WonContracted/Fulfilment → Paid) are tested there and appear here only as sneak paths."""

EXTRA_TS = []

GROUPS = [
    dict(ts="US-0701", heading="State transition – deal stages executable in EP-07 (0-switch and sneak paths)", tech="ST",
         intro="""Default commercial template (Part 2.3 §2.27.3; Part 6.1 §6.1.11.4). Transitions executable in the EP-07 board are 1–7 and 15–23 of the 23-transition machine; 8–14 need EP-13/EP-15 evidence and are exercised in Batches 6.2/6.3.

| # | From → To | Guard | Executable here |
|---|---|---|---|
| 1 | Qualified → Engaged | next action set; eligible contact | Yes |
| 2 | Engaged → MeetingScheduled | meeting booked (EP-09) | Yes (event) |
| 3 | MeetingScheduled → Discovery | meeting held | Yes |
| 4 | Discovery → ProposalDraft | scope agreed | Yes |
| 15–20 | Qualified, Engaged, Discovery, ProposalSent, Negotiation, Committed → Lost | reason code required | Yes |
| 21 | Lost → Qualified | new evidence, outside 90-day cooling (BRL-ELG-16) | Yes |
| 22–23 | Qualified ↔ OnHold | hold reason | Yes |
| S | Qualified → Paid; ProposalDraft → Committed; Lost → Qualified inside cooling | — | Sneak paths: 409 |""",
         rows=[
        R("Create deal D-9001 from the qualified event with amount ₹1,35,000.00", "AC-0701-01; FR-A029; BRL-SCR-06; FR-CSM-01", "OPP-7001 qualified, owner Ravi (R03 MedMaarg)", "1. Process `opportunity.qualified`", "D-9001 Qualified; KIMS Hospital; Wellness Scanner – Institutional; ₹1,35,000.00 INR (3 × ₹45,000.00); timeline \"Created from OPP-7001\"", "P1", "T01", "ST", "Y", "SYS"),
        R("Walk transitions 1, 2, 3 and 4 with next actions and outbox events", "AC-0701-02; FR-A029; NFR-006", "D-9001 Qualified", "1. Qualified → Engaged (next action \"Send introduction\" due 2027-02-20 17:00 IST). 2. → MeetingScheduled. 3. → Discovery. 4. → ProposalDraft", "Each: actor, time, revision recorded; one `deal.transitioned` outbox row per step", "P1", "T01", "ST", "Y", "SYS"),
        R("Lose a deal only with a reason code and reopen only outside the cooling period", "US-0701; BRL-APR-08; BRL-ELG-16", "D-9002 Engaged; clock control", "1. → Lost without reason. 2. With reason \"budget\" on 2027-02-01. 3. Reopen on 2027-04-01 with new evidence. 4. Reopen on 2027-05-02", "1: 400 `REASON_REQUIRED`. 2: Lost. 3: 409 cooling period (90 days). 4: Qualified", "P1", "T01", "ST", "Y", "SYS"),
        R("Hold and resume a deal", "US-0701; FR-CSM-01", "D-9003 Qualified", "1. → OnHold reason \"customer fiscal freeze\". 2. → Qualified", "Both recorded; OnHold excluded from active pipeline value", "P2", "T01", "ST", "Y", "SYS"),
        R("Reject sneak paths Qualified → Paid and ProposalDraft → Committed", "AC-0701-03; DEC-054; KPI-31", "D-9001 Qualified; D-9004 ProposalDraft", "1. Drag D-9001 to Paid. 2. PATCH D-9004 to Committed", "1: 409 `INVALID_TRANSITION`; card returns; toast \"Paid requires verified payment evidence (DEC-054)\". 2: 409; KPI-31 unaffected", "P0", "T01", "ST", "Y", "SYS"),
        R("Let one of two concurrent transitions from revision 4 win", "AC-0701-07; NFR-025; FR-STD-03", "Two sessions on D-9001 revision 4", "1. Both PATCH stage concurrently", "One 200; other 409 \"This deal changed since you opened it\"; one outbox row", "P1", "T16", "EG", "Y", "IT"),
    ]),
    dict(ts="US-0704", heading="Equivalence classes and decision table – public enquiry intake and routing (FR-DM-04)", tech="EP, DT",
         intro="""| Field | Valid class | Invalid classes |
|---|---|---|
| Email | RFC-valid business or personal address | `sunita@`; empty; > 254 chars |
| Message | 1–5,000 chars | 0; 5,001 |
| Consent | ticked with notice revision | unticked |
| Host | verified startup host | unknown host → 404 |
| Free text content | business content | clinical detail → minimized and human-only (BRL-PRV-06, BRL-ELG-14) |

Routing (DEC-052; FR-DM-04): external AI development project → AppNAI; school/college AI education → EduVerse; healthcare institutional partnership → MedMaarg; organic trade → OrganicSpec; otherwise the host's startup.""",
         rows=[
        R("Route a valid enquiry to a lead with consent revision and reference within 2 s", "AC-0704-01; FR-W12; CA-INTAKE; NFR-008", "Host medmaarg.example.com; form Institutional enquiry v3", "1. Submit Sunita Das / Bright Clinics (IN, email, consent ticked)", "Reference ENQ-MM-000412 ≤ 2 s; lead L-4120 Routed (CN-MM-4, organic/website); Customer 360 shows it ≤ 60 s", "P1", "T01", "EP", "Y", "E2E"),
        R("Reject 5,001-character message, invalid email and missing consent; accept 5,000 characters", "AC-0704-04; FR-W12", "Same form", "1. Submit invalid set. 2. Submit message of exactly 5,000 characters", "1: three inline errors; nothing stored. 2: accepted", "P1", "T01", "BVA", "Y", "E2E"),
        R("Strip clinical detail, flag human-only and send no health-related acknowledgement", "AC-0704-03; BRL-PRV-06, BRL-ELG-14; AP-05; DM-R32", "Message \"My father has stage 2 CKD, which plan suits him?\"", "1. Submit. 2. Inspect stored lead and outbox", "Stored \"[clinical detail removed]\"; flag \"clinical – human only\"; acknowledgement contains no health content", "P0", "T19", "DT", "Y", "SYS"),
        R("Route four request types to the right startup regardless of entry site", "AC-0704-06, AC-0706-05; FR-DM-04; DEC-052", "Enquiries entered on the EduVerse site", "1. \"We need an AI vision system built for our factory\". 2. \"AI curriculum for our school\". 3. \"Corporate wellness pilot for our hospital\". 4. \"We buy organic turmeric\"", "AppNAI (reason recorded) · EduVerse · MedMaarg · OrganicSpec", "P1", "T01", "DT", "Y", "SYS"),
        R("Return 404 for an unknown host and store nothing", "AC-0704-05; BRL-TEN-10", "Host unknown-startup.example.com", "1. POST form", "404; 0 rows; 0 outbox", "P0", "T15", "EP", "Y", "SYS"),
        R("Ignore a tenant_id in the payload and scope by host", "AC-0704-08; BRL-TEN-01; DM-R03", "Payload adds T2 tenant_id", "1. Submit", "Lead in T1/MedMaarg; attempt logged; 0 T2 rows", "P0", "T15", "EP", "Y", "SYS"),
    ]),
    dict(ts="US-0706", heading="Decision table and boundaries – EduVerse audience, age band, guardian OTP and DPIA flag (DEC-030)", tech="DT, BVA",
         intro="""| Condition / Rule | E1 | E2 | E3 | E4 | E5 | E6 |
|---|---|---|---|---|---|---|
| Flag `eduverse.minor_intake` ON (DPIA signed) | – | N | Y | Y | Y | – |
| Audience | Institution | Learner < 18 or guardian | Learner < 18 entering own contact | Guardian | Guardian | Adult learner (age band 18–24) |
| Guardian OTP verified within 10 min (≤ 3 resends) | – | – | – | N | Y | – |
| **Action** | Institutional queue; no learner data | "Please contact the school…"; store nothing | Guardian details required; learner phone not stored | No lead; minimal audit; never message learner | Routed; consent record; learner data = name, grade band, programme; guardian-only channels | Adult branch; no guardian |

OTP boundary: entered at 9 min 59 s → valid; at 10 min 00 s → expired [ASSUMPTION-196].""",
         rows=[
        R("E5: route a guardian-verified enquiry for a 15-year-old with minimal learner data", "AC-0706-01; FR-W17; BRL-ELG-13; DEC-030; AP-05", "Flag ON; guardian Kavita Rao kavita.rao@example.com; learner Arjun, Class 9–10, AI Foundations (weekend)", "1. Submit as Parent or guardian. 2. Enter OTP at 9 min 59 s", "Lead Routed; consent record; learner fields only name, grade band, programme; all channels to guardian only", "P0", "T19", "DT", "Y", "E2E"),
        R("E4: OTP at 10 min 00 s is expired; after 3 resends no lead is routed", "AC-0706-03; BRL-ELG-13", "As above; clock control", "1. Enter OTP at 10:00. 2. Use 3 resends without entering a valid code", "No lead; minimal audit record; 0 messages to learner", "P0", "T19", "BVA", "Y", "SYS"),
        R("E3: refuse a learner's own phone and require guardian details", "AC-0706-02; BRL-ELG-13; DM-R31", "Flag ON; mobile 360 px", "1. Choose Learner under 18; enter own phone +91 98765 43210", "Guardian details required; learner phone not stored (DB and logs)", "P0", "T19", "DT", "Y", "E2E"),
        R("E2: flag OFF shows the helpline message and stores nothing", "AC-0706-07; RECOMMENDATION-007; DM-R37", "Flag OFF", "1. Choose Learner under 18. 2. Choose Parent or guardian", "\"Please contact the school or call our helpline\"; 0 rows", "P0", "T19", "DT", "Y", "E2E"),
        R("E6: age band 18–24 takes the adult branch", "AC-0706-06; DEC-030", "Flag ON", "1. Choose age band 18–24", "Adult-learner branch; no guardian fields", "P0", "T19", "BVA", "Y", "E2E"),
        R("E1: institutional enquiry requests no learner data", "AC-0706-04; FR-W17", "coordinator@dps-school.example.edu.in, 120-student cohort", "1. Submit as Institution", "EduVerse institutional queue; type MoU/educational order; no learner fields", "P1", "T01", "DT", "Y", "SYS"),
        R("Keep learner data out of AI prompts beyond grade band", "US-0706; DEC-030; BRL-AI-06; AP-05", "Routed EduVerse lead from E5; drafting agent run", "1. Capture gateway prompt (redacted test capture)", "Prompt contains grade band only; no learner name, guardian contact or age", "P0", "T19", "EP", "Y", "IT"),
    ]),
    dict(ts="US-0707", heading="Boundary values – Customer 360 freshness (NFR-008)", tech="BVA",
         intro="Target: event visible ≤ 60 s from commit (p95 95% ≤ 60 s, 100% ≤ 120 s per Part 6.1 LT-10). Indicator: green ≤ 60 s, amber > 60 s.",
         rows=[
        R("Show a committed reply on the timeline within 60 s and keep the indicator green", "AC-0707-02; FR-A032; NFR-008", "Reply event committed 2027-02-21T10:00:00+05:30", "1. Poll timeline", "Visible by 10:01:00; indicator green", "P1", "T03", "BVA", "Y", "SYS"),
        R("Turn the indicator amber at lag 61 s and show 4 min lag truthfully", "AC-0707-07; NFR-008", "Consumer paused to create lag", "1. Lag 60 s. 2. Lag 61 s. 3. Lag 4 min", "1: green. 2: amber. 3: \"Data last updated 4 min ago\"; High alert (US-0709)", "P1", "T21", "BVA", "Y", "SYS"),
        R("Keep identity links within a tenant for the same email hash", "AC-0707-05; BRL-TEN-03; DM-R03", "T2 contact with the same email hash as a T1 contact", "1. Rebuild projection", "No cross-tenant link; T1 users see nothing from T2", "P0", "T15", "EP", "Y", "IT"),
    ]),
    dict(ts="US-0710", heading="Boundary values – public intake abuse limits (NFR-022)", tech="BVA",
         intro="Defaults (Part 2.4 §2.35.3; US-0710 notes): 30 req/min per IP; 600 req/min per startup site; text form body ≤ 64 KB. Bot check: honeypot + timing + risk score; never a cognitive test (WCAG 3.3.8; GAP-153).",
         rows=[
        R("Accept the 30th submission and throttle the 31st within 60 s from one IP", "AC-0710-03; FR-W12; NFR-022", "One IP; clock control", "1. 30 submissions in 59 s. 2. 31st", "1: accepted. 2: 429 with Retry-After; throttled UI state", "P1", "T07", "BVA", "Y", "SYS"),
        R("Accept 600 and throttle 601 submissions per minute for one site while other sites continue", "AC-0710-06; NFR-022; BRL-TEN-10", "100 IPs against the MedMaarg site; AppNAI site in parallel", "1. 600 then 601 in one minute on MedMaarg. 2. Submit on AppNAI", "601st on MedMaarg 429; AppNAI unaffected", "P1", "T07", "BVA", "Y", "SYS"),
        R("Accept a 64 KB body and refuse 64 KB + 1 B and 70 KB", "AC-0710-04; NFR-022", "Form posts of 65,536 B, 65,537 B and 71,680 B", "1. Post each", "64 KB accepted; others 413; nothing stored", "P1", "T07", "BVA", "Y", "SYS"),
        R("Silently drop a honeypot submission", "AC-0710-02; NFR-022", "Hidden field company_website_confirm filled", "1. Submit", "Client sees success; no lead; counted \"bot\"", "P1", "T07", "EG", "Y", "SYS"),
    ]),
    dict(ts="US-0708", heading="Decision table – import consent gating (DEC-039)", tech="DT",
         intro="""| Rule | Suppression hash exists | consent_basis present | consent_evidence_ref present | Result |
|---|---|---|---|---|
| I1 | Y | – | – | Import flagged "suppressed"; can never become eligible |
| I2 | N | N | – | "Not eligible – consent/lawful basis to verify" |
| I3 | N | Y | N | "consent evidence missing"; ineligible |
| I4 | N | Y | Y | Ineligible until R10/R04 verifies the evidence (DEC-039); then PDP evaluates normally |""",
         rows=[
        R("I1: keep a previously deleted address suppressed on import", "AC-0708-02; BRL-ELG-02, BRL-PRV-03", "old.buyer@freshmart.example.com has a suppression hash", "1. Dry run and import", "Row flagged suppressed; PDP always denies", "P0", "T19", "DT", "Y", "IT"),
        R("I3: refuse eligibility for consent_basis without evidence", "AC-0708-03; BRL-ELG-03", "Row consent_basis opt-in, no evidence ref", "1. Import", "\"consent evidence missing\"; ineligible", "P0", "T19", "DT", "Y", "IT"),
        R("I2/I4: every imported contact is not eligible until verified", "AC-0708-01; DEC-039; BRL-ELG-01", "buyers-2026.csv (340 orgs, 610 contacts, 45 deals; template crm-1.0)", "1. Dry run. 2. R10 approves. 3. Import. 4. PDP check for 10 sampled contacts", "1: 338/340, 596/610, 12 merges, 45 deals valid. 3: created. 4: all deny until evidence verified", "P0", "T11", "DT", "Y", "IT"),
        R("Re-running the same file creates no duplicates", "US-0708; NFR-005; M-12", "Same content hash as the previous job", "1. Import again", "Rejected as duplicate job, points to the earlier job ID; 0 new rows", "P1", "T16", "EG", "Y", "IT"),
    ]),
]

TS_TITLE = {
    "US-0701": "Deals move only through valid stages, with concurrency control",
    "US-0702": "Pipeline variants and closure policy configured safely",
    "US-0703": "Lead forms approved, with no sensitive fields",
    "US-0704": "Public enquiries become routed leads exactly once",
    "US-0705": "Demo and partnership requests routed and deduplicated",
    "US-0706": "EduVerse intake protects minors through guardian verification",
    "US-0707": "Customer 360 is fresh, scoped and masked",
    "US-0708": "CRM imports are consent-gated and idempotent",
    "US-0709": "Intake funnel and freshness observability",
    "US-0710": "Public intake abuse controls without cognitive challenges",
}
