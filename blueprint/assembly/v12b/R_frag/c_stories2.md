
##### US-18-ZR11 Connector framework and activation gate

| Field | Value |
|---|---|
| ID | US-18-ZR11 |
| Title | Connector framework and activation gate |
| Type | Compliance |
| Story | As a compliance lead (P09, R10), I want every connector to pass a documented gate (security review, DPA, transfer basis, channel registration, approved jurisdiction pack, second approver) before production use, so that no integration sends data unlawfully |
| Persona / roles | P09 (R10); P11 (R12); P10 (R11) |
| Traces | FR-V12-R-056…062, 079, 080; ENT-INT-01…05; CF-01…12; DEC-884; Part 11.15 |
| Priority | Must |
| Wave | Release 1 (S3) |
| Points | 5–8 |
| Dependencies | Jurisdiction pack table (Part 11.15) |
| Dimension profile | A1,A4,A5 · S1–S4 · D1–D4 · C1,C3 · T(IN, EU) · I1–I4 · La |
| Notes | Gate evaluated by AU-295; activation is human |

```gherkin
Feature: Connector framework and activation gate
  Background:
    Given tenant "Kestrel Analytics" (IN) installed "HubSpot" in sandbox and requests production for market "IN"

  @happy @ENT-INT-05
  Scenario: AC-18ZR11-01 Activation with complete evidence
    Given security review "SR-221", DPA "DPA-HS-2027", transfer entry "CJR15-044" and the IN pack approved by counsel
    When "dpo@kestrel.example.com" (R10) approves the request raised by Meera (R12)
    Then the installation becomes "Active" and its credential moves to the production secret

  @neg @ENT-INT-05
  Scenario: AC-18ZR11-02 Missing DPA blocks activation
    Given DPA is missing
    When activation is requested
    Then the API returns 409 "CONNECTOR_GATE_INCOMPLETE" listing "DPA missing" and no provider call is made

  @neg @DEC-785
  Scenario: AC-18ZR11-03 Unapproved market pack blocks activation
    Given the installation also serves market "AE" whose pack is not approved
    When R10 approves
    Then the database raises "CONNECTOR_MARKET_PACK_NOT_APPROVED" and the state stays "PendingGate"

  @perm
  Scenario: AC-18ZR11-04 Requester cannot approve
    When Meera approves her own request
    Then the API returns 403 "SAME_APPROVER"

  @obs
  Scenario: AC-18ZR11-05 Health degradation alert
    Given the HubSpot error rate is 60% over 20 calls
    Then the breaker opens, the installation is "Degraded" and "connector.degraded" is published within 5 minutes
```

##### US-07-ZR12 CRM bi-directional sync with Salesforce, HubSpot and Zoho CRM

| Field | Value |
|---|---|
| ID | US-07-ZR12 |
| Title | CRM bi-directional sync with Salesforce, HubSpot and Zoho CRM |
| Type | Feature |
| Story | As a growth manager (P03, R03), I want contacts, accounts and opportunities to stay in sync with our CRM, so that sales works in one place while the platform keeps consent and approvals |
| Persona / roles | P03 (R03); P11 (R12); P13 (R17) |
| Traces | FR-V12-R-063, 066…069; INT-01; DEC-884; ADR-259 |
| Priority | Must |
| Wave | Release 1 (S4–S7) |
| Points | 8–13 |
| Dependencies | US-18-ZR11 |
| Dimension profile | A1,A3,A4 · S1–S4 · D1–D5 · C3 · T(IN, EU) · I1–I4 · n/a locale |
| Notes | Provider order Zoho → HubSpot → Salesforce |

```gherkin
Feature: CRM bi-directional sync with Salesforce, HubSpot and Zoho CRM
  Background:
    Given an active production installation of the CRM for tenant "Kestrel Analytics" (IN) with mapping version 3

  @happy
  Scenario: AC-07ZR12-01 Inbound change applied by external ID
    When the CRM changes Opportunity "006xx01" stage to "Negotiation"
    Then the linked deal moves to stage "Negotiation" and sync_cursor advances

  @edge @I4
  Scenario: AC-07ZR12-02 Uncertain write is reconciled before retry
    Given the push of contact C-88 times out
    When the worker retries
    Then it first reads by external ID "GE_Id=C-88" and only writes if the record is absent or older

  @neg @sec
  Scenario: AC-07ZR12-03 Token revoked
    Given the CRM returns 401 three times
    Then the installation is "Disabled", R12 gets "Reconnect", and no further calls are made

  @sec @perm
  Scenario Outline: AC-07ZR12-04 Connector outcomes across connector, auth, failure, residency, environment and gate
    Given connector "<connector>" using "<auth>" in <env> for a <residency> tenant with gate "<gate>"
    When the provider behaves as "<failure>"
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M07}}
```

##### US-07-ZR13 CRM field ownership, conflicts and protected consent

| Field | Value |
|---|---|
| ID | US-07-ZR13 |
| Title | CRM field ownership, conflicts and protected consent |
| Type | Compliance |
| Story | As a compliance lead (P09, R10), I want consent, suppression and approvals to stay owned by the platform and other field conflicts queued by policy, so that a CRM can never re-enable outreach someone has refused |
| Persona / roles | P09 (R10); P03 (R03L); P11 (R12) |
| Traces | FR-V12-R-064, 065; DEC-885 |
| Priority | Must |
| Wave | Release 1 (S5) |
| Points | 3–5 |
| Dependencies | US-07-ZR12 |
| Dimension profile | A1,A4 · S1–S3 · D1–D5 · C1,C3 · T(IN) · I1 · La |
| Notes | DDL check `crm_field_mapping` protected fields |

```gherkin
Feature: CRM field ownership, conflicts and protected consent
  @neg @sec
  Scenario: AC-07ZR13-01 CRM cannot re-enable a suppressed contact
    Given contact C-90 is suppressed for email in the platform
    When the CRM sends HasOptedOutOfEmail=false for C-90
    Then the platform keeps the suppression and logs a conflict "consent_state platform_wins_stricter"

  @happy
  Scenario: AC-07ZR13-02 CRM opt-out imports as suppression
    When the CRM sends HasOptedOutOfEmail=true for C-91
    Then C-91 is suppressed for email in the platform within one sync cycle

  @val
  Scenario: AC-07ZR13-03 Protected field policy cannot be changed
    When R12 sets the policy of "consent_state" to "crm_wins"
    Then the API returns 422 "PROTECTED_FIELD_POLICY"

  @alt
  Scenario: AC-07ZR13-04 newest_wins conflict queued
    Given field "deal.amount" uses newest_wins and both sides changed within the same second
    Then a conflict is queued for R03L with both value hashes and no value is overwritten until resolved
```

##### US-23-ZR14 SMS via DLT with registry scrubbing

| Field | Value |
|---|---|
| ID | US-23-ZR14 |
| Title | SMS via DLT with registry scrubbing |
| Type | Compliance |
| Story | As a marketing specialist (P05, R05), I want to send approved SMS only through registered DLT entities, headers and templates and only to numbers that pass registry scrubbing in the permitted window, so that we comply with TRAI rules |
| Persona / roles | P05 (R05); P09 (R10); P14 (R16 recipient) |
| Traces | FR-V12-R-070…074; INT-04; CJ-IN-06; DEC-777; DEC-884 |
| Priority | Must |
| Wave | Release 1 (S4–S5) |
| Points | 5–8 |
| Dependencies | US-18-ZR11; India pack approved |
| Dimension profile | A1,A5,A6 · S1–S4 · D1–D5 · C3 · T(owned startups IN) · I1–I4 · Lb (hi-IN template) |
| Notes | V12 R1 exit "DLT live" |

```gherkin
Feature: SMS via DLT with registry scrubbing
  Background:
    Given channel account "MM-SMS-1" with entity "1201159000000012345", header "MMAARG" (service_explicit) and template "1207161000000098765" with 2 variables

  @happy
  Scenario: AC-23ZR14-01 Registered template sent and reconciled
    When an approved message with 2 variables is dispatched at 2027-02-05T11:00:00+05:30
    Then the aggregator receives PE-ID, header and template IDs and the delivery report sets "Delivered"

  @neg @CJ-IN-06
  Scenario: AC-23ZR14-02 Template variable mismatch held
    When a message with 3 variables is dispatched
    Then the PDP returns HOLD "DLT_TEMPLATE_MISMATCH" and no SMS is sent

  @neg
  Scenario: AC-23ZR14-03 Promotional SMS to a DND number held
    Given the recipient is registered in the full-block DND category
    When a promotional message is dispatched
    Then the PDP returns HOLD "REGISTRY_SCRUB_BLOCKED"

  @edge @DEC-777
  Scenario Outline: AC-23ZR14-04 Promotional window (stricter of law and DEC-777)
    When a promotional SMS is dispatched at <time> IST
    Then the decision is <decision>
    Examples:
      | time  | decision |
      | 08:59 | HOLD OUTSIDE_WINDOW |
      | 09:00 | HOLD OUTSIDE_WINDOW (TRAI window starts 10:00, verify) |
      | 10:00 | ALLOW |
      | 20:59 | ALLOW |
      | 21:00 | HOLD OUTSIDE_WINDOW |

  @happy
  Scenario: AC-23ZR14-05 STOP keyword
    When the recipient replies "STOP"
    Then the number is suppressed for SMS within 60 s and a confirmation is sent on the service header
```

##### US-22-ZR15 Voice transport connector with number series and recording consent

| Field | Value |
|---|---|
| ID | US-22-ZR15 |
| Title | Voice transport connector with number series and recording consent |
| Type | Feature |
| Story | As a growth manager (P03, R03), I want click-to-call and approved voice notifications through a CPaaS with the correct number series and recording only with consent, so that calls are compliant and ready for the AI voice workflows of Part 11.18 |
| Persona / roles | P03 (R03); P09 (R10); P14 (R16) |
| Traces | FR-V12-R-075…078; INT-05; CJ-IN-07; DEC-782, DEC-884 |
| Priority | Must |
| Wave | Release 1 (S6–S7) |
| Points | 5–8 |
| Dependencies | US-18-ZR11 |
| Dimension profile | A1,A5 · S1–S4 · D1–D4 · C3 · T(IN) · I1–I4 · La |
| Notes | AI voice behaviour is out of scope here (Part 11.18) |

```gherkin
Feature: Voice transport connector with number series and recording consent
  @happy
  Scenario: AC-22ZR15-01 Click-to-call from a service number
    Given number "+91 160xxxxxxx" with series 160 and purpose "service" (format verify)
    When Asha starts click-to-call to a customer with a service purpose
    Then the CPaaS bridges both legs and the call status is reconciled to "completed"

  @neg @CJ-IN-07
  Scenario: AC-22ZR15-02 Promotional call from a service number refused
    When a promotional notification is attempted from the 160-series number
    Then the PDP returns HOLD "SERIES_PURPOSE_MISMATCH"

  @neg @DEC-782
  Scenario: AC-22ZR15-03 No recording without consent
    Given the jurisdiction requires all-party consent and the callee did not consent
    When the call connects
    Then recording is not started and the call record says "recording_not_permitted"

  @edge
  Scenario: AC-22ZR15-04 Uncertain status
    Given the CPaaS times out after accepting the call request
    Then the action is "Uncertain" and is reconciled by call reference before any retry
```

##### US-21-ZR16 Regional Vercel projects with pinned functions

| Field | Value |
|---|---|
| ID | US-21-ZR16 |
| Title | Regional Vercel projects with pinned functions |
| Type | Compliance |
| Story | As the privacy lead (P09, R10), I want every Vercel function that touches personal data to run only in the tenant's residency region and every non-conforming deployment blocked, so that personal data is processed in-zone (DEC-772/786) |
| Persona / roles | P09 (R10); platform SRE |
| Traces | FR-V12-R-081…084, 093, 094; DEC-786, DEC-886; VD-01…04, 11 |
| Priority | Must |
| Wave | Release 1 (S0–S3) |
| Points | 3–5 |
| Dependencies | Tenant directory |
| Dimension profile | A n/a (platform) · S n/a · D1–D3 · C1,C2 · T(IN, EU) · I1,I3 · n/a locale |
| Notes | AU-296 |

```gherkin
Feature: Regional Vercel projects with pinned functions
  @neg @DEC-786
  Scenario: AC-21ZR16-01 Deployment without region pin is blocked
    Given a change sets regions ["iad1"] on project "admin-in"
    When CI runs the VD-02 check
    Then the deployment is blocked and production stays on the last compliant deployment

  @happy
  Scenario: AC-21ZR16-02 Custom domain bound to its zone project
    Given startup domain "medmaarg.example" belongs to an IN tenant
    Then it is attached to project "web-in" only and AU-296 VD-11 passes

  @sec @perm
  Scenario Outline: AC-21ZR16-03 Data-path outcomes across surface, region, request, header, logging and function region
    Given surface "<surface>" for a <region> tenant
    When a "<request>" arrives with "<header>", logging "<logging>" and functions "<function_region>"
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M08}}
```

##### US-21-ZR17 Vercel logging, header allowlist, origin verification and sub-processor controls

| Field | Value |
|---|---|
| ID | US-21-ZR17 |
| Title | Vercel logging, header allowlist, origin verification and sub-processor controls |
| Type | Security |
| Story | As the privacy lead (P09, R10), I want no bodies or tokens in Vercel logs, only allowlisted headers forwarded, origin bypass impossible and Vercel listed as a sub-processor, so that the personal-data path meets DEC-786 |
| Persona / roles | P09 (R10); platform SRE |
| Traces | FR-V12-R-085…092, 095; DEC-786, DEC-887; VD-05…10 |
| Priority | Must |
| Wave | Release 1 (S1–S2) |
| Points | 3–5 |
| Dependencies | US-21-ZR16 |
| Dimension profile | A n/a · S n/a · D1–D5 · C1,C2 · T(IN, EU) · I1 · n/a locale |
| Notes | Edge transit position documented in rule packs |

```gherkin
Feature: Vercel logging, header allowlist, origin verification and sub-processor controls
  @neg @sec
  Scenario: AC-21ZR17-01 Code that logs a request body fails the build
    Given a function contains "console.log(await req.json())"
    When CI runs lint rule VD-07
    Then the build fails

  @sec
  Scenario: AC-21ZR17-02 Direct-to-origin request blocked
    When a client calls "https://admin-origin.in.platform.example.com/api/v1/leads" without X-Origin-Verify
    Then AWS WAF returns 403 and Django receives nothing

  @sec
  Scenario: AC-21ZR17-03 Non-allowlisted header stripped
    When a request includes header "X-Debug-User: 42"
    Then the origin access log shows the request without that header

  @happy
  Scenario: AC-21ZR17-04 Sub-processor notice
    Given Vercel is listed on 2027-01-01 after a notice sent on 2026-12-01
    Then the subprocessor row passes the 30-day notice check
```

##### US-21-ZR18 Continuous WAL archiving, standby and RPO monitoring

| Field | Value |
|---|---|
| ID | US-21-ZR18 |
| Title | Continuous WAL archiving, standby and RPO monitoring |
| Type | Enabler |
| Story | As the DBRE (platform team), we need Supabase PITR plus an in-zone WAL-G standby with 35-day archives and a 30-second RPO monitor, so that no more than 15 minutes of data can be lost in any zone |
| Persona / roles | Platform team; P01 (R01) as risk owner |
| Traces | FR-V12-R-096…101, 110; DEC-787, DEC-888, DEC-889; ADR-261; AU-297 |
| Priority | Must |
| Wave | Release 1 (S1–S3) |
| Points | 8–13 |
| Dependencies | C8 roles; IaC |
| Dimension profile | A n/a · S n/a · D1,D3,D6 · C3 · T(IN, EU) · I1–I3 · n/a locale |
| Notes | Copies stay in-zone |

```gherkin
Feature: Continuous WAL archiving, standby and RPO monitoring
  @happy
  Scenario: AC-21ZR18-01 Steady state lag
    Given the IN standby subscribes to publication "ge_all"
    Then replication lag stays below 60 s for 24 hours of synthetic load profile "m"

  @obs
  Scenario: AC-21ZR18-02 Paging thresholds
    When the WAL archive age reaches 10 minutes
    Then on-call is paged; at 15 minutes a SEV1 is opened

  @neg @DEC-772
  Scenario: AC-21ZR18-03 Archive replication only in-zone
    When an operator adds a replication rule from the IN bucket to "eu-central-1"
    Then the bucket policy denies it

  @sec
  Scenario: AC-21ZR18-04 Object Lock prevents early deletion
    When an operator deletes a 10-day-old WAL segment
    Then the request is denied
```

##### US-21-ZR19 Restore drills at every release gate and per zone

| Field | Value |
|---|---|
| ID | US-21-ZR19 |
| Title | Restore drills at every release gate and per zone |
| Type | Enabler |
| Story | As the SRE lead (platform team), we need scripted restores on every path with measured RPO/RTO and the PRV verification pack at each release gate and quarterly, so that recovery claims are evidence, not estimates |
| Persona / roles | Platform team; P01 (R01) |
| Traces | FR-V12-R-102…109; DEC-771, DEC-787; KPI-18/19/32; OPT-TC-ST-14 |
| Priority | Must |
| Wave | Release 1 (S4, S7) |
| Points | 5–8 |
| Dependencies | US-21-ZR18 |
| Dimension profile | A n/a · S n/a · D1,D3,D6 · C3 · T(IN, EU) · I1–I4 · n/a locale |
| Notes | KPI-32 is release-blocking |

```gherkin
Feature: Restore drills at every release gate and per zone
  @happy @DEC-771
  Scenario: AC-21ZR19-01 Growth recovery within 120 minutes
    Given a drill at the Release 1 gate in zone IN starts at 2027-05-10T10:00:00+05:30
    When the standby is promoted and PRV-01…08 pass
    Then service_restored_at is no later than 12:00:00+05:30 and achieved RPO is at most 900 s

  @neg
  Scenario: AC-21ZR19-02 Missed objective blocks the release
    Given achieved RPO is 1,020 s
    Then the drill record has passed=false and the release gate shows a blocker

  @sec
  Scenario: AC-21ZR19-03 Erasure replay after restore
    Given subject S-77 was erased after the restore point
    When the restore completes
    Then the erasure log replay deletes S-77 again before traffic resumes

  @edge
  Scenario Outline: AC-21ZR19-04 Recovery outcomes across region, failure, WAL age, path and gate
    Given zone <region> suffers "<failure>" with WAL archive age "<wal_age>" during "<gate>"
    When the team restores through "<path>"
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M09}}
```

##### US-04-ZR20 Model registry data model and two-person approval

| Field | Value |
|---|---|
| ID | US-04-ZR20 |
| Title | Model registry data model and two-person approval |
| Type | Feature |
| Story | As the AI governance lead (P09, R10), I want every model recorded with provider, version, hosting, zones, data classes, task classes and evidence, and approved by two people, so that no model is used without proof |
| Persona / roles | P09 (R10); P01 (R01) |
| Traces | FR-V12-R-112, 114, 130; AIX-02; DEC-788, DEC-890 |
| Priority | Must |
| Wave | Release 1 (S1–S2) |
| Points | 5–8 |
| Dependencies | DDL-V12-R-14 |
| Dimension profile | A1,A4,A5 · S1–S4 · D1–D4 · C1,C3 · T(platform) · I n/a · La |
| Notes | A011 Registry tab and Part 9.7 A115 |

```gherkin
Feature: Model registry data model and two-person approval
  @happy
  Scenario: AC-04ZR20-01 Two approvers approve a complete row
    Given row REG-005 has all evidence references
    When "ai.gov@ownerportfolio.example.com" (R10) approves and the Founder's delegate approves
    Then REG-005 is "approved" for task "classification" with recert_due one year later

  @neg
  Scenario: AC-04ZR20-02 Same approver twice
    When R10 tries to record the second approval
    Then the API returns 403 "SAME_APPROVER"

  @neg @sec
  Scenario: AC-04ZR20-03 Database refuses approved state without evidence
    When app_registry sets status "approved" on a row with no DPA reference
    Then the check constraint "ai_model_approved_evidence_ck" fails
```

##### US-04-ZR21 Approval evidence, multimodal rows and re-certification

| Field | Value |
|---|---|
| ID | US-04-ZR21 |
| Title | Approval evidence, multimodal rows and re-certification |
| Type | Compliance |
| Story | As the AI governance lead (P09, R10), I want the seven V12 evidence items enforced for text, embedding, image, video and voice rows and rows re-certified yearly or on change, so that approvals stay valid |
| Persona / roles | P09 (R10) |
| Traces | FR-V12-R-113, 124, 125, 129; V12 16.2; DEC-890, DEC-892; AU-298 |
| Priority | Must |
| Wave | Release 1 (S3) |
| Points | 3–5 |
| Dependencies | US-04-ZR20 |
| Dimension profile | A1,A4 · S2–S4 · D1–D4 · C1 · T(platform) · I1,I3 · La |
| Notes | — |

```gherkin
Feature: Approval evidence, multimodal rows and re-certification
  @neg
  Scenario Outline: AC-04ZR21-01 Approval outcomes across modality, evidence and approvers (exhaustive)
    Given a "<modality>" candidate whose evidence is "<evidence>"
    When it is approved by "<approvers>"
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M13}}

  @edge
  Scenario: AC-04ZR21-02 DPA change suspends a row
    Given the provider of REG-008 changes its DPA effective 2027-03-01
    When AU-298 runs on 2027-03-01
    Then REG-008 is "suspended" and routing uses the next eligible row or HOLD
```

##### US-04-ZR22 Zone- and class-aware routing through the registry

| Field | Value |
|---|---|
| ID | US-04-ZR22 |
| Title | Zone- and class-aware routing through the registry |
| Type | Feature |
| Story | As the LLM platform lead (platform team, for P10/R11), I want the gateway to choose only approved rows that match the tenant's zone, data class, task and locale, with V12 fallback and kill switch, so that AI is cheap, compliant and never silently unapproved |
| Persona / roles | P10 (R11); P09 (R10) |
| Traces | FR-V12-R-111, 116…123, 128; AIX-03; DEC-788, DEC-891 |
| Priority | Must |
| Wave | Release 1 (S2–S3) |
| Points | 8–13 |
| Dependencies | US-04-ZR20; AU-151/152 |
| Dimension profile | A n/a · S n/a · D1–D5 · C3 · T(IN, EU) · I1–I4 · La,Lb |
| Notes | Restricted data never to free or open-weight rows |

```gherkin
Feature: Zone- and class-aware routing through the registry
  @sec @perm
  Scenario Outline: AC-04ZR22-01 Routing outcomes across task, data class, region, candidate, state and availability
    Given an AI step "<task>" on "<data>" data for a <region> tenant and candidate row "<candidate>" in state "<state>"
    When the provider availability is "<availability>"
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M10}}

  @edge
  Scenario: AC-04ZR22-02 Kill switch within 60 seconds
    When R10 sets the kill switch for task "drafting" at 10:00:00
    Then no drafting call is made after 10:01:00 and steps HOLD with reason "kill_switch"
```

##### US-04-ZR23 Claude Sonnet primary record, advanced tier and candidate onboarding

| Field | Value |
|---|---|
| ID | US-04-ZR23 |
| Title | Claude Sonnet primary record, advanced tier and candidate onboarding |
| Type | Feature |
| Story | As the Founder (P01, R01), I want my approval of Claude Sonnet as primary recorded in the registry and other candidates (advanced tier, other providers, open-weight) onboarded through evidence and a canary, so that provider choice stays evidence-based |
| Persona / roles | P01 (R01); P09 (R10) |
| Traces | FR-V12-R-115, 126, 127; DEC-788, DEC-892 |
| Priority | Must |
| Wave | Release 1 (S6–S7) |
| Points | 3–5 |
| Dependencies | US-04-ZR22 |
| Dimension profile | A1,A4 · S2,S3 · D1,D3 · C1 · T(platform) · I1 · La |
| Notes | Model IDs verify at implementation |

```gherkin
Feature: Claude Sonnet primary record, advanced tier and candidate onboarding
  @happy @DEC-788
  Scenario: AC-04ZR23-01 Founder approval recorded
    Then REG-002 shows approval "DEC-788, Founder, 28 Nov 2026" and is the default row for MDL-M1 tasks in zones IN and EU where processing is available

  @alt
  Scenario: AC-04ZR23-02 Canary for a new candidate
    Given REG-005 is approved for "classification"
    Then it receives 5% of eligible classification traffic for 7 days and is promoted only if its EVAL and cost per accepted result are not worse than REG-003

  @neg
  Scenario: AC-04ZR23-03 Advanced tier not used until approved
    Given REG-004 is "candidate"
    When a complex synthesis step runs
    Then it routes to REG-002 at higher effort, not to REG-004
```

##### US-17-ZR24 Benchmark participation under contract clause

| Field | Value |
|---|---|
| ID | US-17-ZR24 |
| Title | Benchmark participation under contract clause |
| Type | Compliance |
| Story | As an external SaaS client administrator (P13, R17), I want to opt in to peer benchmarks under a contract clause and withdraw at any time, so that we gain insight without giving up our data |
| Persona / roles | P13 (R17); P11 (R12); P01 (R01) for owned startups |
| Traces | FR-V12-R-131…134, 142; DEC-789, DEC-893 |
| Priority | Must |
| Wave | Release 2 |
| Points | 3–5 |
| Dependencies | Contract clause BM-CL-1 |
| Dimension profile | A1,A5 · S1–S4 · D1–D4 · C1 · T(external IN, external EU, owned) · I n/a · La |
| Notes | Opt-in default (ASSUMPTION-1084) |

```gherkin
Feature: Benchmark participation under contract clause
  @happy
  Scenario: AC-17ZR24-01 Opt in
    When R12 of "Nordlicht GmbH" (EU) opts in with clause "BM-CL-1 v1" and step-up
    Then an enrolment row exists and contributions start next period

  @neg
  Scenario: AC-17ZR24-02 Owned startup excluded without R01 opt-in
    Given "MedMaarg" is an Owner Portfolio startup without R01 opt-in
    Then it contributes nothing and cannot view benchmarks

  @perm
  Scenario: AC-17ZR24-03 Reciprocity
    Given tenant "Kestrel Analytics" has not opted in
    When R12 calls GET /api/v1/benchmarks
    Then the API returns 403 "BENCHMARKS_NOT_ENROLLED"
```

##### US-17-ZR25 Differentially private benchmark computation and publication

| Field | Value |
|---|---|
| ID | US-17-ZR25 |
| Title | Differentially private benchmark computation and publication |
| Type | Feature |
| Story | As a tenant administrator (P11, R12), I want benchmarks published only for cohorts of at least 10 tenants with noise, per zone, so that our data cannot be inferred |
| Persona / roles | P11 (R12); P02 (R02) |
| Traces | FR-V12-R-135…141; DEC-789, DEC-893; ADR-263; AU-299 |
| Priority | Must |
| Wave | Release 2 |
| Points | 8–13 |
| Dependencies | US-17-ZR24 |
| Dimension profile | A1 · S n/a · D1–D6 · C1,C3 · T(IN, EU, global) · I n/a · La |
| Notes | Independent DP review before first publication |

```gherkin
Feature: Differentially private benchmark computation and publication
  @sec @perm
  Scenario Outline: AC-17ZR25-01 Publication outcomes across cohort, dominance, participation, metric, scope, owner and budget
    Given a cohort of <cohort> with "<dominance>" and viewer participation "<participant>" and owner flag "<owner>"
    When the "<metric>" cell for "<scope>" is computed with "<budget>"
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M11}}
```

##### US-01-ZR26 Least-privilege database role app_rw with per-transaction context

| Field | Value |
|---|---|
| ID | US-01-ZR26 |
| Title | Least-privilege database role app_rw with per-transaction context |
| Type | Security |
| Story | As the DBRE (platform team), we need Django and Celery to use only NOBYPASSRLS roles that set tenant, company, actor and zone context per transaction, so that RLS protects every query (DEC-778) |
| Persona / roles | Platform team |
| Traces | FR-V12-R-143, 147…151, 153; DEC-778, DEC-894; SB-02, SB-03 |
| Priority | Must |
| Wave | Release 1 (S0–S1) |
| Points | 3–5 |
| Dependencies | Part 11.9b DDL |
| Dimension profile | A n/a · S n/a · D1,D4 · C3 · T(two tenants) · I n/a · n/a |
| Notes | Rename migration DDL-V12-R-16 |

```gherkin
Feature: Least-privilege database role app_rw with per-transaction context
  @sec @perm
  Scenario Outline: AC-01ZR26-01 Access outcomes across role, context, operation and path
    Given a connection as "<role>" through "<path>" with context "<context>"
    When it runs "<op>"
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M12}}

  @neg
  Scenario: AC-01ZR26-02 CI fails if an app role can bypass RLS
    Given someone altered app_worker to BYPASSRLS on a branch
    When CI runs the assertion block
    Then it raises "APP_ROLE_CAN_BYPASS_RLS" and the pipeline fails
```

##### US-01-ZR27 Data API disabled and service_role only through break-glass

| Field | Value |
|---|---|
| ID | US-01-ZR27 |
| Title | Data API disabled and service_role only through break-glass |
| Type | Security |
| Story | As the security lead (platform team), we need the Supabase Data API closed for application schemas and the service_role key confined to audited, time-boxed CI migrations, so that nothing bypasses RLS |
| Persona / roles | Platform team; P09 (R10) |
| Traces | FR-V12-R-144…146, 152, 154, 155; DEC-778; SA-01…03, 09 |
| Priority | Must |
| Wave | Release 1 (S0) |
| Points | 2–3 |
| Dependencies | — |
| Dimension profile | A n/a · S n/a · D1 · C3 · T(IN, EU) · I n/a · n/a |
| Notes | AU-292 detector |

```gherkin
Feature: Data API disabled and service_role only through break-glass
  @neg @sec
  Scenario: AC-01ZR27-01 Data API returns nothing
    When an anonymous client calls the Supabase REST endpoint for table "lead"
    Then the response is 404 and no data is returned

  @sec
  Scenario: AC-01ZR27-02 service_role session from an app subnet raises SEV2
    Given a session of service_role appears from subnet "app-a" at 10:00
    Then AU-292 opens a SEV2 by 10:02 and RB-SA-02 is linked

  @happy
  Scenario: AC-01ZR27-03 Break-glass migration
    Given ticket "CHG-301" approved by DBRE and Security with expiry 2 h
    When CI runs the migration with service_role
    Then the audit event "db.break_glass.used" records both approvers and expiry, and access is revoked at expiry
```

##### US-01-ZR28 Residency choice at onboarding and region routing

| Field | Value |
|---|---|
| ID | US-01-ZR28 |
| Title | Residency choice at onboarding and region routing |
| Type | Feature |
| Story | As a SaaS client applicant (P13, R17), I want to choose India or EU residency at onboarding and have every request routed to that zone, so that our data never leaves it |
| Persona / roles | P13 (R17); P12 (R13) |
| Traces | FR-V12-R-005; ENT-DAT-03; DEC-772, DEC-776, DEC-895 |
| Priority | Must |
| Wave | Release 1 (S1) |
| Points | 3–5 |
| Dependencies | Tenant directory |
| Dimension profile | A1 · S1,S3 · D1–D4 · C1,C3 · T(IN, EU) · I1,I3 · La |
| Notes | EU cell provisioned at first EU contract |

```gherkin
Feature: Residency choice at onboarding and region routing
  @happy
  Scenario: AC-01ZR28-01 EU residency chosen
    When applicant "Nordlicht GmbH" selects residency "EU" in the onboarding wizard
    Then the tenant directory records zone "EU" and the tenant is created only in the EU cell

  @neg @DEC-772
  Scenario: AC-01ZR28-02 Misdirected request is not proxied
    When a request for an EU tenant arrives at "api.in.platform.example.com"
    Then the response is 421 and no lookup of personal data is attempted

  @edge
  Scenario: AC-01ZR28-03 EU cell not yet provisioned
    Given the EU cell is not provisioned
    When an applicant chooses EU
    Then the application is accepted as "awaiting EU provisioning" and no personal data beyond the applicant contact (stored per the onboarding notice) is processed until the cell exists
```

##### US-21-ZR29 Operability of automations AU-290…299

| Field | Value |
|---|---|
| ID | US-21-ZR29 |
| Title | Operability of automations AU-290…299 |
| Type | Observability |
| Story | As the SRE lead (platform team), we need dashboards, alerts and evidence exports for AU-290…299, so that every control is visibly running and auditable |
| Persona / roles | Platform team; P09 (R10) |
| Traces | FR-V12-R-027, 078, 093, 100, 124, 137; AU-290…299 |
| Priority | Must |
| Wave | Release 1 (S3–S7) |
| Points | 3–5 |
| Dependencies | Observability stack (Part 11.11) |
| Dimension profile | A n/a · S n/a · D1,D4 · C1 · T(IN, EU) · I1,I3 · n/a |
| Notes | Monitor-blind alerts are High |

```gherkin
Feature: Operability of automations AU-290…299
  @obs
  Scenario: AC-21ZR29-01 Every automation reports a heartbeat
    Then each of AU-290…299 writes a heartbeat at least once per expected cycle and a missed heartbeat raises "monitor blind" High

  @obs
  Scenario: AC-21ZR29-02 Evidence export for audit
    When R10 exports control evidence for 2027-Q1
    Then the export contains AU-290…298 records with counts, failures and links to findings
```
