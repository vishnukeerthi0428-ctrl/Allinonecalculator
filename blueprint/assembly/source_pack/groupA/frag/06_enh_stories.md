### 2.6.5.7 Part 5 enhancements: user stories with acceptance criteria

Format follows Part 5 (field table plus Gherkin). Points are estimates in the Part 5 scale. Every story names its persona, FR, rules and tests. Fixtures use GSE-SYN (Part 6.1) with clock control (CLK-0 = 2026-12-01 09:00 IST unless stated).

#### US-05-EA01 Research coverage ledger

| Field | Value |
|---|---|
| Type · Persona | Feature · P04 (R04); viewer P02, P01 |
| Story | As a research analyst, I want each scheduled source run to record attempted, succeeded, blocked and stale counts with cost and distinct qualified opportunities, so that I can see real coverage and gaps instead of assuming the web is covered. |
| Links | FR-ENH-A-001, FR-ENH-A-002; KPI-ENH-A-01; RP-ENH-A-01; BRL-SRC-01, BRL-ENH-A-02; SP-11 |
| Priority · Wave · Points | Must · W1 · 5–8 |
| Dependencies | A010 registry, WF-02, budget reservation (M53) |

```gherkin
Feature: US-05-EA01 Research coverage ledger
  Scenario: AC-05EA01-01 Happy path - counters per run
    Given source SRC-IN-TENDER-01 in family SPB-04 for AppNAI with TTL 7 days
    When the scheduled run fetches 12 items, 2 return HTTP 403 and 1 is older than 7 days
    Then the ledger entry shows attempted 12, succeeded 9, blocked 2 with reason "access denied", stale 1
    And cost INR 0.00 is recorded against B01 and qualified_distinct is computed after review

  Scenario: AC-05EA01-02 Negative - never "complete"
    Given every cell for India x SPB-01 succeeded this week
    Then the report shows "100% of due checks for known approved sources" and never the word "complete coverage"

  Scenario: AC-05EA01-03 Edge - unknown is not zero
    Given no run has been scheduled for Kenya x SPB-02
    Then the cell shows "Not covered" and is excluded from the KPI denominator with a listed reason

  Scenario: AC-05EA01-04 Permission - scope
    When R04 of MedMaarg opens the ledger Then only MedMaarg cells are returned and the AppNAI cells are absent (ABAC-01)
```

#### US-05-EA02 Source and segment playbook registry with launch checklist

| Field | Value |
|---|---|
| Type · Persona | Feature · P04 (R04) author; P09 (R10) approver |
| Story | As a research analyst, I want each source family and MedMaarg segment to have a versioned playbook with a launch checklist, so that no source runs before permission, URL, freshness, quota, owner and cost are recorded. |
| Links | FR-ENH-A-004; SPB-01…24; BRL-SRC-01; RECOMMENDATION-302 |
| Priority · Wave · Points | Must · W1 · 3–5 |

```gherkin
Feature: US-05-EA02 Playbook launch checklist
  Scenario: AC-05EA02-01 Happy path
    Given playbook SPB-03 Official directories with permission, URL, TTL 180, quota 500/day, owner and budget B03 recorded and approved by R10
    When R04 schedules source SRC-DIR-ODISHA under SPB-03 Then the schedule is accepted

  Scenario: AC-05EA02-02 Negative - incomplete checklist
    Given playbook SPB-05 LinkedIn has no approved API scope
    When R04 tries to schedule an automated run Then 422 "Launch checklist incomplete: permitted access method" is returned and only manual research tasks are allowed

  Scenario: AC-05EA02-03 Segment template drives pipeline
    Given SPB-17 IT / corporate is approved
    When an opportunity of segment IT / corporate is qualified Then the deal uses stages "Wellness pilot" then "Annual package" and the guardrail "aggregate nonclinical metrics only" is shown on the proposal editor
```

#### US-05-EA03 Discovery and provider benchmark

| Field | Value |
|---|---|
| Type · Persona | Feature · P04 (R04), data steward; approver R01 for paid providers |
| Story | As a data steward, I want a labelled benchmark per source family and per provider, so that we move sources to scheduled mode and enable paid data only on measured quality and cost. |
| Links | FR-ENH-A-005, FR-ENH-A-006; BRL-ENH-A-03, BRL-ENH-A-04; KPI-ENH-A-04; DEC-001; NFR-037 |
| Priority · Wave · Points | Must · W1 · 5–8 |

```gherkin
Feature: US-05-EA03 Discovery benchmark
  Scenario: AC-05EA03-01 Happy path - report with interval
    Given 50 labelled permitted records for SPB-01 of which the system proposed 30 eligible, 26 correct, and the known corpus holds 34 eligible
    Then precision is 0.867 with 95% Wilson interval 0.703 to 0.947 and recall is 0.765 with sample size shown
    And the family stays in Pilot because the precision lower bound 0.703 is below 0.80

  Scenario: AC-05EA03-02 Negative - paid provider without benchmark
    When R12I requests activation of a paid contact-data adapter with no benchmark Then activation is blocked with BRL-ENH-A-03

  Scenario: AC-05EA03-03 Edge - small sample
    Given only 18 permitted records exist for SPB-13 Then the report shows counts only and states "n < 30"
```

#### US-05-EA04 Coverage planner

| Field | Value |
|---|---|
| Type · Persona | Feature · P04 (R04); approver P02 in WAR |
| Story | As a research analyst, I want next week's coverage priorities ranked by objective fit, budget and source quality, so that we close the most valuable gaps first without collecting from prohibited sources. |
| Links | FR-ENH-A-003; AOP (FR-ENH-A-010); BRL-SRC-04 |
| Priority · Wave · Points | Should · W1 · 3–5 |

```gherkin
Feature: US-05-EA04 Coverage planner
  Scenario: AC-05EA04-01 Ranking explains factors
    Given AOP-02 prioritizes Odisha and Karnataka hospitals with research budget INR 1,500.00 remaining
    Then the top suggestion lists objective fit, remaining budget and historic qualified conversion for each cell
  Scenario: AC-05EA04-02 Negative - prohibited family never suggested
    Given SPB-05 LinkedIn is in manual-only mode Then no automated suggestion for SPB-05 is produced
```

#### US-06-EA01 Optional partnership-fit scoring version

| Field | Value |
|---|---|
| Type · Persona | Feature · P04 (R04) proposes; P02 (R02) and AI lead approve |
| Story | As a startup head, I want to trial the six-factor partnership-fit score on partnership opportunity types, so that we can compare it with the default score before adopting it. |
| Links | FR-ENH-A-007; BRL-ENH-A-01; CONFLICT-300; DEC-011; BRL-SCR-01…03 |
| Priority · Wave · Points | Could · W3 · 3–5 |

```gherkin
Feature: US-06-EA01 Partnership-fit scoring version
  Scenario: AC-06EA01-01 Computation
    Given components capability 0.80, need 0.70, qualification 0.60, geography 1.00, budget unknown, timing 0.50
    Then score = round(100 x (0.30x0.80 + 0.25x0.70 + 0.15x0.60 + 0.10x1.00 + 0.10x0.50) / 0.90) = 73
    And known weight 0.90 is at least 0.60 so a band is assigned
  Scenario: AC-06EA01-02 Review defaults
    Given fit 73 and coverage 65 Then the opportunity is routed to "research/nurture" because coverage is below 70
  Scenario: AC-06EA01-03 Negative - activation without benchmark
    When R02 activates the version for "Institutional partnership" without a benchmark Then 422 BRL-ENH-A-01
```

#### US-08-EA01 Reply taxonomy with deterministic effects

| Field | Value |
|---|---|
| Type · Persona | Feature · P03 (R03); AG-013 classifier |
| Story | As a sales executive, I want every inbound reply classified into one agreed class with a fixed effect on sequences, so that declines, meeting requests and opt-outs are handled the same way every time. |
| Links | FR-ENH-A-008; CONFLICT-303; BRL-SEQ-02; AG-013 |
| Priority · Wave · Points | Must · W2 · 3–5 |

```gherkin
Feature: US-08-EA01 Reply taxonomy
  Scenario Outline: AC-08EA01-01 Effects by class
    Given contact C-17 enrolled in generic sequence SEQ-4 step 2
    When a reply classified as <class> arrives
    Then the sequence state is <sequence> and <effect>
    Examples:
      | class           | sequence | effect                                   |
      | decline         | stopped  | stage "Declined", no re-engagement task   |
      | meeting request | stopped  | slot offer drafted from free/busy         |
      | out-of-office   | paused   | resumes one business day after return date|
      | unsubscribe     | stopped  | suppression entry with evidence           |
      | unknown         | paused   | human classification task created        |
  Scenario: AC-08EA01-02 Negative - low confidence
    When AG-013 returns confidence 0.42 Then class "unknown" is stored and no automatic effect except pause is applied
```

#### US-08-EA02 Deliverability stop thresholds and opt-out race

| Field | Value |
|---|---|
| Type · Persona | Feature · P05 (R05), P09 (R10) |
| Story | As a compliance officer, I want campaign sending to pause automatically when bounce or complaint rates cross the policy threshold, and an opt-out received after queueing to always win, so that sender reputation and consent are protected. |
| Links | BRL-ENH-A-06; Part 2.2 §2.6.1; DEC-025; KPI-17, KPI-18 |
| Priority · Wave · Points | Must · W2 · 3–5 |

```gherkin
Feature: US-08-EA02 Deliverability and opt-out race
  Scenario: AC-08EA02-01 Pause at threshold
    Given sender S-ORG-1 sent 1,000 campaign emails in 7 days with 21 hard bounces
    Then campaign sends from S-ORG-1 are paused, R10 is alerted and transactional sends continue
  Scenario: AC-08EA02-02 Opt-out after enqueue
    Given step M-1 is queued at 10:00:00 and the contact opts out at 10:00:05 before lease at 10:00:09
    Then no provider call is made, one "suppressed" outcome and one audit event exist, and the INR 0.20 reservation is released
```

#### US-09-EA01 Recording consent for meetings and webinars

| Field | Value |
|---|---|
| Type · Persona | Feature · P03, P05 |
| Story | As an organizer, I want recording and transcription to require prior notice and recorded permission, so that sessions are never recorded without consent. |
| Links | BRL-ENH-A-05; BRL-MTG; GAP-308 |
| Priority · Wave · Points | Must · W2 · 2–3 |

```gherkin
Feature: US-09-EA01 Recording consent
  Scenario: AC-09EA01-01 Negative - no permission
    Given meeting MTG-8 has no recorded permission Then the "Record" and "Transcribe" actions are disabled with reason BRL-ENH-A-05
  Scenario: AC-09EA01-02 MedMaarg
    Given a MedMaarg demo Then platform recording is unavailable regardless of permission
```

#### US-11-EA01 Social publication proof

| Field | Value |
|---|---|
| Type · Persona | Feature · P05 (R05L) |
| Story | As a marketing lead, I want a post marked Published only when the platform returns its external post ID, so that we never report posts that were not actually published. |
| Links | FR-ENH-A-009; BR-M35; DEC-050 |
| Priority · Wave · Points | Should · W3 · 2–3 |

```gherkin
Feature: US-11-EA01 Social publication proof
  Scenario: AC-11EA01-01 Provider timeout
    Given the provider times out after the publish request Then the post is "uncertain" and the reconciler lists recent posts before any retry
  Scenario: AC-11EA01-02 Duplicate retry
    When the job is retried with the same idempotency key after success Then no second post is created
```

#### US-12-EA01 Experiment registry with stop triggers

| Field | Value |
|---|---|
| Type · Persona | Feature · P05 (R05), P02 (R02) |
| Story | As a growth marketer, I want each acquisition experiment to change one variable on a bounded eligible cohort with a holdout and automatic stop triggers, so that we learn safely and comparably. |
| Links | FR-ENH-A-011; BRL-MKT-10, BRL-ENH-A-13; RP-ENH-A-04; KPI-ENH-A-05; OPT-12-04 |
| Priority · Wave · Points | Should · W3 · 5–8 |

```gherkin
Feature: US-12-EA01 Experiment registry
  Scenario: AC-12EA01-01 One variable at a time
    Given experiment EXP-7 changes "subject line" on segment SEG-3 from 2026-12-01 to 2026-12-14
    When R05 creates EXP-8 changing "send time" on an overlapping cohort Then creation is blocked "Overlapping cohort with running experiment EXP-7"
  Scenario: AC-12EA01-02 Stop trigger
    Given arm B baseline complaint rate 0.04% and arm B reaches 0.07% Then arm B pauses, NT-ENH-A-01 is sent and the scorecard logs the trigger
  Scenario: AC-12EA01-03 No causal claim without comparison
    Given EXP-9 has no holdout and no comparable baseline Then the scorecard shows "No comparison: result descriptive only"
```

#### US-12-EA02 Acquisition operating plan

| Field | Value |
|---|---|
| Type · Persona | Feature · P02 (R02) author; P01 (R01) approver |
| Story | As a startup head, I want one approved quarterly acquisition plan with segments, propositions, coverage priorities, budget split, experiments and denominators, so that campaigns and research align to an approved objective. |
| Links | FR-ENH-A-010; AOP-01…05; DEC-008; DEC-038 |
| Priority · Wave · Points | Should · W3 · 5–8 |

```gherkin
Feature: US-12-EA02 Acquisition operating plan
  Scenario: AC-12EA02-01 Single active revision
    Given AOP-04 Q1-2027 revision 2 is active When revision 3 is approved Then revision 2 becomes superseded and running campaigns keep their own approved revisions
  Scenario: AC-12EA02-02 Budget within caps
    When the plan allocates INR 9,000.00 to ads while the startup's approved ads cap is INR 6,000.00 Then approval routes to R01 per DEC-038
  Scenario: AC-12EA02-03 Planned offering
    When the plan lists RamVan while it is Planned Then validation fails BRL-MKT-02
```

#### US-12-EA03 Weekly acquisition review

| Field | Value |
|---|---|
| Type · Persona | Feature · P02 chair; P03, P04, P05 attendees |
| Story | As a startup head, I want a generated weekly review pack and a decision record, so that priorities, budget shifts and experiment decisions are made on evidence and tracked. |
| Links | FR-ENH-A-012; CFG-ENH-A-04; NT-ENH-A-02 |
| Priority · Wave · Points | Should · W3 · 3–5 |

```gherkin
Feature: US-12-EA03 Weekly acquisition review
  Scenario: AC-12EA03-01 Pack generation
    Given CFG-ENH-A-04 Monday 09:00 IST When the clock reaches Monday 09:00 IST Then the WAR pack contains the seven agenda sections with as-of times
  Scenario: AC-12EA03-02 No direct execution
    When the chair records "increase SEG-3 daily send cap" Then a change request is created for approval and no cap changes until approved
```

#### US-15-EA01 Outcome economics

| Field | Value |
|---|---|
| Type · Persona | Report · P01, P02, FinOps |
| Story | As a founder, I want cost per qualified opportunity and per verified outcome by segment and channel for matched cohorts, so that I fund what works without counting forecasts as results. |
| Links | FR-ENH-A-013; KPI-ENH-A-03; BRL-ENH-A-14; RP-ENH-A-02 |
| Priority · Wave · Points | Should · W5 · 3–5 |

```gherkin
Feature: US-15-EA01 Outcome economics
  Scenario: AC-15EA01-01 Computation
    Given November cohort costs INR 12,400.00 and 4 verified closures Then cost per verified outcome is INR 3,100.00 with currency INR and as-of time
  Scenario: AC-15EA01-02 Zero denominator
    Given December has 0 verified closures Then the cell shows "Not assessed" not INR 0.00 or infinity
  Scenario: AC-15EA01-03 Synthetic excluded
    Given synthetic fixture closures exist in staging Then production reports exclude them
```

#### US-03-EA01 Jurisdiction activation decision record

| Field | Value |
|---|---|
| Type · Persona | Feature · P09 (R10) |
| Story | As a compliance officer, I want a recorded and approved activation decision before a startup acts in a new country, so that cross-border sources, messages and commercial routes are lawful. |
| Links | FR-ENH-A-014; DEC-029; OPT-19-02 |
| Priority · Wave · Points | Must · W3 · 3–5 |

```gherkin
Feature: US-03-EA01 Jurisdiction activation
  Scenario: AC-03EA01-01 Negative - no record
    Given AppNAI has no activation record for Germany When a campaign step targets a German contact Then PDP denies with JURISDICTION_NOT_ACTIVATED
  Scenario: AC-03EA01-02 Approved
    Given R10 approves the Germany record with expiry 2027-12-01 Then eligible German contacts pass the jurisdiction check
```

#### US-19-EA01 Legal disclosure block

| Field | Value |
|---|---|
| Type · Persona | Feature · P05 (R05) edits; P09 (R10) approves |
| Story | As a compliance officer, I want every public site to show an approved legal disclosure for its legal entity and locale, so that visitors know who they deal with. |
| Links | FR-ENH-A-017; GAP-303; ASSUMPTION-306; CFG-ENH-A-08 |
| Priority · Wave · Points | Must · W3 · 2–3 |

```gherkin
Feature: US-19-EA01 Legal disclosure
  Scenario: AC-19EA01-01 Negative - incomplete
    Given the OrganicSpec en-IN disclosure lacks the grievance contact When R05L publishes the home page Then publication is blocked "Legal disclosure incomplete"
  Scenario: AC-19EA01-02 Display
    Then every public page footer shows legal name, registration identifiers, registered address and privacy contact from the approved revision
```

#### US-19-EA02 Website publisher segregation of duties

| Field | Value |
|---|---|
| Type · Persona | Feature · P05w-A, P05w-P, P09w-R |
| Story | As a compliance officer, I want sensitive-claim pages to be published by someone other than their author, so that no one approves their own claim. |
| Links | BRL-ENH-A-09; ABAC-ENH-A-04; BRL-APR |
| Priority · Wave · Points | Must · W3 · 1–2 |

```gherkin
Feature: US-19-EA02 Publisher SoD
  Scenario: AC-19EA02-01 Negative
    Given R05L authored page P-9 containing a price claim When R05L publishes P-9 Then 403 BRL-ENH-A-09
```

#### US-20-EA01 Service arrangement selection

| Field | Value |
|---|---|
| Type · Persona | Feature · P13a, P13 |
| Story | As a SaaS applicant, I want to choose self-service, managed or hybrid service, so that the provider knows whether its operators will work inside my tenant. |
| Links | FR-ENH-A-015; GAP-302; CFG-ENH-A-07; W31, W33 |
| Priority · Wave · Points | Should · W5 · 2–3 |

```gherkin
Feature: US-20-EA01 Service arrangement
  Scenario: AC-20EA01-01 Default
    Given an approved application without a choice Then the tenant is provisioned as self_service and no delegation grant can be created
```

#### US-20-EA02 Managed-service delegation grant

| Field | Value |
|---|---|
| Type · Persona | Feature · P17 (R21); P13 (client admin) |
| Story | As a client administrator, I want to grant a managed-service operator scoped, time-limited access to selected modules, sender identities and budgets, and revoke it at once, so that delegated work never exceeds what I approved. |
| Links | FR-ENH-A-015; ABAC-ENH-A-01…03; R21; NT-ENH-A-05; GAP-301 |
| Priority · Wave · Points | Should · W5 · 5–8 |

```gherkin
Feature: US-20-EA02 Delegation grant
  Scenario: AC-20EA02-01 Happy path
    Given client Nova Industrial (demo) approves grant G-1 for modules Discovery and Outreach, sender S-NOVA-1, budget BUD-NOVA-ADS, expiry 90 days
    When operator O-1 with R21 dispatches a step from S-NOVA-1 Then PDP allows after normal eligibility checks and the audit event carries grant G-1
  Scenario: AC-20EA02-02 Negative - outside scope
    When O-1 opens Closure quotes or uses sender S-OWNER-1 Then 403 DELEGATION_SCOPE
  Scenario: AC-20EA02-03 Revocation
    When the client revokes G-1 Then O-1's session is terminated within 60 seconds and queued steps created by O-1 are held for client review
  Scenario: AC-20EA02-04 No cross-client
    Given O-1 also holds grant G-2 for client Acme (demo) Then O-1 can act in only one client tenant per session and search never returns the other client's records
```

#### US-20-EA03 External tenant founder workspace

| Field | Value |
|---|---|
| Type · Persona | Feature · P13b |
| Story | As an external tenant founder, I want to set my own acquisition goals, review usage and cost, invite users and export my data, so that I run my business independently. |
| Links | FR-W34; FR-ENH-A-010 (own AOP); A101; A103; OPT-19-03 |
| Priority · Wave · Points | Should · W5 · 3–5 |

```gherkin
Feature: US-20-EA03 Founder workspace
  Scenario: AC-20EA03-01 Own data only
    When the founder exports contacts Then the export contains only the founder's tenant records and the job is audited
```

#### US-21-EA01 Training and competence record

| Field | Value |
|---|---|
| Type · Persona | Feature · P11 (R12) trainer/admin; all internal personas |
| Story | As a tenant administrator, I want training completion, competence and acknowledgement recorded per user and module, so that gated actions are unlocked only for trained users without training ever granting a permission. |
| Links | FR-ENH-A-018; BRL-ENH-A-10; RSK-024; Part 8.2 §8.2.2.2 |
| Priority · Wave · Points | Should · W0 · 2–3 |

```gherkin
Feature: US-21-EA01 Training record
  Scenario: AC-21EA01-01 Training never grants
    Given user U-5 has a valid "Outreach sending" training record but no R03 role Then the Send action is not available and the API returns 403
  Scenario: AC-21EA01-02 Expiry
    Given U-6 holds R03 and the training record expired yesterday Then the Send affordance is hidden with reason "Training expired" and the role remains
  Scenario: AC-21EA01-03 Assessor SoD
    When U-6 records their own competence Then 422 "Assessor must differ from trainee"
```

#### US-21-EA02 User-productivity study

| Field | Value |
|---|---|
| Type · Persona | Enabler · UX researcher; P03, P04, P05, P06, P08 participants |
| Story | As the UX lead, I want baseline and candidate task time and error rates measured with representative users, so that navigation improvements are proven without weakening safeguards. |
| Links | §2.6.5.1.4; NFR-034; OPT-15-01; GAP-306 |
| Priority · Wave · Points | Should · W2 and W5 · 3–5 |

```gherkin
Feature: US-21-EA02 Productivity study
  Scenario: AC-21EA02-01 Evidence
    When the study for P04 "review 10 signals" completes Then an EVR records participants, median and p90 time, error count and build digest
  Scenario: AC-21EA02-02 Guardrail
    Given a candidate design removes the evidence panel to save time Then the candidate is rejected as a safeguard reduction
```

#### US-18-EA01 Template reviewer segregation of duties

| Field | Value |
|---|---|
| Type · Persona | Feature · P19 (R11T), P10 (R11) |
| Story | As a template reviewer, I want to approve only templates I did not author, after seeing the diff and simulation, so that published templates are independently checked and immutable. |
| Links | BRL-ENH-A-11; FR-A113; DEC-051 |
| Priority · Wave · Points | Must · W3 · 2–3 |

```gherkin
Feature: US-18-EA01 Template review
  Scenario: AC-18EA01-01 Negative - own template
    Given R11T user T-1 authored template TPL-3 v4 When T-1 approves TPL-3 v4 Then 403 BRL-ENH-A-11
  Scenario: AC-18EA01-02 Immutable
    Given TPL-3 v4 is published When anyone edits v4 Then the edit creates v5 draft and v4 is unchanged
```

#### US-18-EA02 Hold record visibility

| Field | Value |
|---|---|
| Type · Persona | Feature · P10a (R11), P03 |
| Story | As an automation operator, I want every policy hold stored with scope, relationship, evidence, rule IDs, revision and run, so that I can resolve it in the right workspace. |
| Links | FR-ENH-A-020; A110, A111, A072 |
| Priority · Wave · Points | Must · W2 · 2–3 |

```gherkin
Feature: US-18-EA02 Hold record
  Scenario: AC-18EA02-01 Stale data hold
    Given evidence EV-4 for REL-COM-001 expired at CLK-0 minus 1 day When the follow-up step is due Then a hold record with rule BRL-ENH-A-02, workflow revision and run ID appears in A110 and no message is sent
```

#### US-01-EA01 Integration administrator

| Field | Value |
|---|---|
| Type · Persona | Feature · P18 (R12I) |
| Story | As an integration administrator, I want to register, test and rotate provider credentials and see adapter health and benchmarks without seeing business content, so that integrations are reliable and least-privilege. |
| Links | R12I; FR-ENH-A-006; NT-ENH-A-04; NFR-037 |
| Priority · Wave · Points | Should · W1 · 3–5 |

```gherkin
Feature: US-01-EA01 Integration administrator
  Scenario: AC-01EA01-01 Metadata only
    When R12I opens the SES adapter Then health, quotas and error counts are visible and message bodies or recipient lists are not
  Scenario: AC-01EA01-02 Paid adapter
    When R12I enables a paid search adapter Then an approval request is created and the adapter stays disabled
```

#### US-15-EA02 No cross-entity allocation

| Field | Value |
|---|---|
| Type · Persona | Feature · P08 (R08/R09) |
| Story | As a finance controller, I want receipts allocated only within the receiving legal entity and currency, so that one startup's cash never closes another's invoice. |
| Links | BRL-ENH-A-07; BRL-FIN; KPI-13 |
| Priority · Wave · Points | Must · W4 · 1–2 |

```gherkin
Feature: US-15-EA02 Cross-entity allocation
  Scenario: AC-15EA02-01 Negative
    Given receipt RC-1 INR 50,000.00 received in the OrganicSpec account When R08 allocates it to MedMaarg invoice INV-77 Then 422 BRL-ENH-A-07 and a finance exception is created
```

#### US-16-EA01 No renewal after cancellation or suppression

| Field | Value |
|---|---|
| Type · Persona | Feature · P03c |
| Story | As a customer success manager, I want renewal outreach blocked for cancelled subscriptions and suppressed contacts, so that we never contact people who left or opted out. |
| Links | BRL-ENH-A-12; WF-12 |
| Priority · Wave · Points | Must · W5 · 1–2 |

```gherkin
Feature: US-16-EA01 Renewal block
  Scenario: AC-16EA01-01 Cancelled
    Given contract CT-5 is Cancelled When the renewal scheduler runs Then no renewal case or outreach is created
  Scenario: AC-16EA01-02 Customer-initiated
    Given the customer requests renewal through W28 Then a renewal case is created for review
```

#### US-14-EA01 Buy-side segregation of duties

| Field | Value |
|---|---|
| Type · Persona | Feature · P07a |
| Story | As a procurement manager, I want PO approval and goods-receipt verification split between people when policy requires it, so that purchases are independently checked. |
| Links | BRL-ENH-A-08; ABAC-ENH-A-05; CFG-ENH-A-06 |
| Priority · Wave · Points | Should · W4 · 1–2 |

```gherkin
Feature: US-14-EA01 Buy-side SoD
  Scenario: AC-14EA01-01 Negative
    Given buy_side_sod is on and U-8 approved PO-12 When U-8 verifies the goods receipt for PO-12 Then 403 BRL-ENH-A-08
```

#### US-17-EA01 Relationship timeline

| Field | Value |
|---|---|
| Type · Persona | Feature · P03, P10a |
| Story | As a sales executive, I want one relationship timeline with a derived stage across lead, deal, quote, contract, order and receipt, so that every screen shows the same business object consistently. |
| Links | FR-ENH-A-016; CONFLICT-304; BR-M23 |
| Priority · Wave · Points | Should · W2 · 3–5 |

```gherkin
Feature: US-17-EA01 Relationship timeline
  Scenario: AC-17EA01-01 Derived only
    When a user or AI tries to set relationship stage "Contracted" directly Then 405 "Derived field"
  Scenario: AC-17EA01-02 Hold overlay
    Given REL-COM-001 is Engaged with an open hold Then the stage shows "Engaged" with a "Held" badge and a link to the hold record
```

#### US-17-EA02 Bulk action preview

| Field | Value |
|---|---|
| Type · Persona | Feature · P03, P04, P05 |
| Story | As an operator, I want a bulk action to preview the selected, eligible and excluded counts and cost before I confirm, so that I never trigger an unintended batch. |
| Links | FR-ENH-A-019; OPT-15-04; FR-FLT-RULES |
| Priority · Wave · Points | Should · W2 · 2–3 |

```gherkin
Feature: US-17-EA02 Bulk preview
  Scenario: AC-17EA02-01 Preview hash
    Given 120 contacts are selected and the preview shows 104 eligible, 16 excluded (BRL-ELG-02 x 9, BRL-ELG-05 x 7), cost INR 20.80
    When 3 more contacts opt out before confirmation Then confirm returns 409 PREVIEW_STALE and a new preview shows 101 eligible
```
