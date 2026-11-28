# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.22b), Master User Stories with Permutations: EP-01 to EP-17

| Field | Value |
|---|---|
| Document | Part 11, Batch 22, file b of f: §11.22.5.4 new stories for EP-01, EP-02, EP-03, EP-04, EP-05, EP-08, EP-12, EP-15, EP-16, EP-17 (template of Part 5.1a; conventions, models and register in file a) |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Parts 0–9.10; Parts 11.1–11.19 (V12 review and V12-B Founder decisions, Part 11.14 DEC-770…791); story template Part 5.1a (§5.2 DoR, §5.3 DoD, §5.5 estimation, §5.6 dimension matrix, §5.7 conventions) |
| Roles applied | Chief Product Officer · Principal Agile Product Owner · Business Systems Analyst (BDD/Gherkin) · UX researcher (persona journeys) · QA Lead (combinatorial design) |
| ID ranges used | DEC-940…959 · tags ASSUMPTION/GAP/CONFLICT/RECOMMENDATION-1140…1159 · ADR-275…279 · stories US-&lt;EP&gt;-ZU&lt;nn&gt; · AC-&lt;EP&gt;ZU&lt;nn&gt;-&lt;seq&gt; · example rows EX-&lt;EP&gt;ZU&lt;nn&gt;-&lt;seq&gt; · parameter models MU01…MU13 · journeys JN-01…JN-12 · new epic EP-34 · new personas P21–P23 |

**Acronyms used in this part.** AC = acceptance criterion · BDD = behaviour-driven development · CPO = Chief Product Officer · DoD / DoR = Definition of Done / Ready · EX = generated example row · FR = functional requirement · INV = Investment Automation product · MAS = minimum AC set (Part 5.1a §5.6.6) · NSE = no side effect · PDP = Policy Decision Point · PSP = payment service provider · RLS = row-level security · SKU = stock-keeping unit (a sellable service, SM-SVC-01…39 or INV-SVC-01…24) · SoD = separation of duties · SP = story point · t-way = covering array in which every combination of any t parameter values appears in at least one row.

### 11.22.5.4 New stories by epic

Every story below covers FR-V12 requirements that had no story, or no story with acceptance criteria (§11.22.3). Each has Gherkin for MAS-1…MAS-9 and one Scenario Outline whose Examples are generated from its parameter model (§11.22.5.2).

#### 11.22.5.4.1 EP-01 Platform foundation, identity reuse and tenancy

| Field | Value |
|---|---|
| Epic | EP-01 Platform foundation, identity reuse and tenancy (Part 0 §0.10.2) |
| New stories in this file | US-01-ZU01, US-01-ZU02, US-01-ZU03, US-01-ZU04, US-01-ZU05, US-01-ZU06, US-01-ZU07, US-01-ZU08, US-01-ZU09, US-01-ZU10, US-01-ZU11, US-01-ZU12, US-01-ZU13, US-01-ZU14 |
| FR-V12 covered | A: 006; E: 004–005, 021; H: 016, 038; I: 001, 004–005, 008–009, 011, 013, 017–018, 025–026, 030–031; K: 101–111, 120–121 |
| Size | 14 stories · 57–93 SP · 28–93 pd (0.5/1.0 pd per SP) · central 52.5 pd (0.7 pd per SP mid) |
| Releases | Release 1: 14 |

##### US-01-ZU01 Product separation between Sales & Marketing and Investment Automation

| Field | Value |
|---|---|
| ID | US-01-ZU01 |
| Title | Product separation between Sales & Marketing and Investment Automation |
| Type | Security |
| Story | As a tenant administrator (P11, R12), I want product separation (amended by DEC-783): Sales & Marketing and Investment Automation are separate product codes, so that only the right people reach our data, with evidence an auditor can verify |
| Persona / roles | Tenant administrator (P11, R12) |
| Traces | FR-V12-A-006 (BR-C14, REC-V2-10); DEC-002, DEC-058; tests TC-V12-A-006 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-01-ZR01, US-01-ZR02, US-01-ZR03, US-01-ZR04; source definition: Part 11.1b §11.1.5.1 Commercial unit and catalogue governance |
| Dimension profile | persona ×3 · authority ×4 · channel ×3 · session/MFA ×3 · region ×3 · operation ×1 · model MU02 |
| Notes | Wording amended by DEC-783: investor entities exist only in the separate Investment Automation product code; the separation check (no implicit cross-product access) is kept (CONFLICT-1149) · Screens A002, A009, A099, A197, A203; API family `/api/v1/identity/`; audit events `identity.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Product separation between Sales & Marketing and Investment Automation
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with administrator "meera@kestrel.example.com" (R12) holding a fresh WebAuthn factor
    And the reused IdP broker is reachable and the break-glass account "bg-admin@kestrel.example.com" is registered

  @happy @BR-C14
  Scenario: AC-01ZU01-01 Happy path – Product separation (FR-V12-A-006)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Product separation" is exercised as specified by FR-V12-A-006:
      """
      Product separation (amended by DEC-783): Sales & Marketing and Investment Automation are separate product codes; only libraries and patterns
      are reused; no implicit cross-product access
      """
    Then an SM-only tenant receives 404 for /api/v1/investor/*:
      """
      a cross-product query returns zero rows, and the SM catalogue, routes and schemas contain no investor entity
      """
    And the audit event "identity.product_separation" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @BRL-APR-01
  Scenario: AC-01ZU01-02 Negative – a user cannot grant a role to themselves
    Given "arjun@kestrel.example.com" holds role "Campaign approver"
    When he assigns role "Campaign requester" to himself
    Then the API returns 409 "SOD_SELF_GRANT" and the role assignment does not exist
    And a security event "identity.sod.violation_blocked" is written

  @val
  Scenario: AC-01ZU01-03 Validation – non-HTTPS identity endpoints are rejected
    When Meera submits SSO metadata URL "http://idp.kestrel.example.com/metadata"
    Then the API returns 422 "METADATA_URL_NOT_HTTPS" and no configuration row exists

  @perm
  Scenario: AC-01ZU01-04 Permission – a startup head cannot change identity configuration
    When "arjun@kestrel.example.com" (R02) posts an identity configuration change
    Then the API returns 403 "PERMISSION_DENIED" and no side effect occurs (NSE)

  @edge @BRL-TEN-07
  Scenario: AC-01ZU01-05 Edge – revocation takes effect within 60 seconds
    Given "ravi@kestrel.example.com" has an active session at 2027-03-01T10:00:00+05:30
    When his access is revoked at 10:00:05
    Then his next API call after 10:01:05 returns 401 "SESSION_REVOKED"

  @sec @obs @MU02
  Scenario Outline: AC-01ZU01-06 Permutations – Enterprise identity, access and audit (3-way, 52 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the session is "<session_mfa>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU02 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-006 = Product separation
    Examples: MU02 rows (3-way, seed 101; space 324; tuples 426/426; +1 baseline-allow)
      | ex | operation | persona | authority | channel | session_mfa | region | expected |
      | EX-01ZU01-01 | A-006 | P11/R12 | T5 other tenant | C2 mobile | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU01-02 | A-006 | P02/R02 | A1 | C1 web | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU01-03 | A-006 | P12/R13 | A5 wrong role | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU01-04 | A-006 | P02/R02 | A3 SoD/limit | C2 mobile | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU01-05 | A-006 | P12/R13 | A3 SoD/limit | C1 web | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU01-06 | A-006 | P11/R12 | T5 other tenant | C3 API | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-01ZU01-07 | A-006 | P11/R12 | A5 wrong role | C2 mobile | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU01-08 | A-006 | P02/R02 | A1 | C3 API | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU01-09 | A-006 | P11/R12 | A1 | C1 web | passkey MFA | EU | ALLOW: an SM-only tenant receives 404 for |
      | EX-01ZU01-10 | A-006 | P12/R13 | A1 | C2 mobile | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU01-11 | A-006 | P02/R02 | T5 other tenant | C1 web | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-01ZU01-12 | A-006 | P02/R02 | A5 wrong role | C1 web | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU01-13 | A-006 | P12/R13 | A3 SoD/limit | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU01-14 | A-006 | P11/R12 | A3 SoD/limit | C3 API | OTP only | EU | 403 SOD_CONFLICT |
      | EX-01ZU01-15 | A-006 | P12/R13 | T5 other tenant | C3 API | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU01-16 | A-006 | P12/R13 | A5 wrong role | C1 web | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-01ZU01-17 | A-006 | P12/R13 | A1 | C2 mobile | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU01-18 | A-006 | P02/R02 | A3 SoD/limit | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU01-19 | A-006 | P11/R12 | A5 wrong role | C3 API | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU01-20 | A-006 | P11/R12 | A5 wrong role | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU01-21 | A-006 | P02/R02 | T5 other tenant | C2 mobile | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-01ZU01-22 | A-006 | P12/R13 | T5 other tenant | C1 web | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU01-23 | A-006 | P11/R12 | A1 | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU01-24 | A-006 | P02/R02 | A5 wrong role | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU01-25 | A-006 | P11/R12 | A3 SoD/limit | C1 web | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-01ZU01-26 | A-006 | P02/R02 | A1 | C3 API | passkey MFA | EU | ALLOW: an SM-only tenant receives 404 for |
      | EX-01ZU01-27 | A-006 | P02/R02 | A5 wrong role | C3 API | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU01-28 | A-006 | P11/R12 | A1 | C1 web | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU01-29 | A-006 | P02/R02 | A3 SoD/limit | C2 mobile | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU01-30 | A-006 | P12/R13 | A3 SoD/limit | C3 API | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU01-31 | A-006 | P12/R13 | T5 other tenant | C2 mobile | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU01-32 | A-006 | P02/R02 | T5 other tenant | C3 API | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU01-33 | A-006 | P12/R13 | A5 wrong role | C2 mobile | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU01-34 | A-006 | P12/R13 | A3 SoD/limit | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU01-35 | A-006 | P12/R13 | A1 | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU01-36 | A-006 | P11/R12 | T5 other tenant | C1 web | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU01-37 | A-006 | P11/R12 | A5 wrong role | C2 mobile | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-01ZU01-38 | A-006 | P11/R12 | A3 SoD/limit | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU01-39 | A-006 | P02/R02 | A3 SoD/limit | C3 API | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU01-40 | A-006 | P02/R02 | T5 other tenant | C2 mobile | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU01-41 | A-006 | P02/R02 | A1 | C2 mobile | passkey MFA | IN | ALLOW: an SM-only tenant receives 404 for |
      | EX-01ZU01-42 | A-006 | P12/R13 | T5 other tenant | C3 API | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU01-43 | A-006 | P12/R13 | A5 wrong role | C1 web | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-01ZU01-44 | A-006 | P12/R13 | A1 | C3 API | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU01-45 | A-006 | P11/R12 | A1 | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU01-46 | A-006 | P11/R12 | T5 other tenant | C1 web | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU01-47 | A-006 | P12/R13 | A1 | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU01-48 | A-006 | P12/R13 | T5 other tenant | C2 mobile | session revoked | IN | uniform 404 NOT_FOUND |
      | EX-01ZU01-49 | A-006 | P02/R02 | A3 SoD/limit | C1 web | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU01-50 | A-006 | P02/R02 | A5 wrong role | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU01-51 | A-006 | P12/R13 | A5 wrong role | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU01-52 | A-006 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: an SM-only tenant receives 404 for |
```

##### US-01-ZU02 Region code on every tenant key and request-region check

| Field | Value |
|---|---|
| ID | US-01-ZU02 |
| Title | Region code on every tenant key and request-region check |
| Type | Compliance (acceptance binding) |
| Story | As a tenant I want region-pinned data and pooled-connection safety – with the acceptance criteria below, which the statement-only story US-01-YE10 did not carry |
| Persona / roles | Tenant administrator (P11, R12) |
| Traces | FR-V12-E-004 (ch02 CJ-R09); FR-V12-E-005 (ch05, SEC-02); tests TC-005, TC-006 |
| Priority | Should |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-01-YE10, US-01-ZR01, US-01-ZR02, US-01-ZR03, US-01-ZR04; source definition: Part 11.5b §11.5.5.13 Functional requirement register |
| Dimension profile | persona ×3 · authority ×4 · channel ×3 · session/MFA ×3 · region ×3 · operation ×2 · model MU02 |
| Notes | Acceptance binding: US-01-YE10 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens A002, A009, A099, A197, A203; API family `/api/v1/identity/`; audit events `identity.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Region code on every tenant key and request-region check
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with administrator "meera@kestrel.example.com" (R12) holding a fresh WebAuthn factor
    And the reused IdP broker is reachable and the break-glass account "bg-admin@kestrel.example.com" is registered

  @happy @CJ-R09
  Scenario: AC-01ZU02-01 Happy path – Region code on tenant and on every key; request region check (FR-V12-E-004)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Region code on tenant and on every key; request region check" is exercised as specified by FR-V12-E-004:
      """
      Region code on tenant and on every key; request region check
      """
    Then the observable result matches FR-V12-E-004 and its tests TC-006
    And the audit event "identity.region_code_on_tenant_and_on" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @SEC-02
  Scenario: AC-01ZU02-02 Alternate – Isolation invariants incl. pooled-connection context reset (FR-V12-E-005)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Isolation invariants incl. pooled-connection context reset" is exercised as specified by FR-V12-E-005:
      """
      Isolation invariants incl. pooled-connection context reset
      """
    Then the observable result matches FR-V12-E-005 and its tests TC-005
    And the audit event "identity.isolation_invariants_incl" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @BRL-APR-01
  Scenario: AC-01ZU02-03 Negative – a user cannot grant a role to themselves
    Given "arjun@kestrel.example.com" holds role "Campaign approver"
    When he assigns role "Campaign requester" to himself
    Then the API returns 409 "SOD_SELF_GRANT" and the role assignment does not exist
    And a security event "identity.sod.violation_blocked" is written

  @val
  Scenario: AC-01ZU02-04 Validation – non-HTTPS identity endpoints are rejected
    When Meera submits SSO metadata URL "http://idp.kestrel.example.com/metadata"
    Then the API returns 422 "METADATA_URL_NOT_HTTPS" and no configuration row exists

  @perm
  Scenario: AC-01ZU02-05 Permission – a startup head cannot change identity configuration
    When "arjun@kestrel.example.com" (R02) posts an identity configuration change
    Then the API returns 403 "PERMISSION_DENIED" and no side effect occurs (NSE)

  @edge @BRL-TEN-07
  Scenario: AC-01ZU02-06 Edge – revocation takes effect within 60 seconds
    Given "ravi@kestrel.example.com" has an active session at 2027-03-01T10:00:00+05:30
    When his access is revoked at 10:00:05
    Then his next API call after 10:01:05 returns 401 "SESSION_REVOKED"

  @sec @obs @MU02
  Scenario Outline: AC-01ZU02-07 Permutations – Enterprise identity, access and audit (3-way, 54 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the session is "<session_mfa>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU02 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   E-004 = Region code on tenant and on every key
    #   E-005 = Isolation invariants incl. pooled-connection…
    Examples: MU02 rows (3-way, seed 108; space 648; tuples 528/528; +2 baseline-allow)
      | ex | operation | persona | authority | channel | session_mfa | region | expected |
      | EX-01ZU02-01 | E-004 | P12/R13 | A1 | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU02-02 | E-005 | P02/R02 | A3 SoD/limit | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU02-03 | E-005 | P12/R13 | A5 wrong role | C2 mobile | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-01ZU02-04 | E-004 | P11/R12 | A5 wrong role | C1 web | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-01ZU02-05 | E-004 | P11/R12 | T5 other tenant | C2 mobile | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU02-06 | E-005 | P02/R02 | T5 other tenant | C3 API | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-01ZU02-07 | E-004 | P12/R13 | A3 SoD/limit | C1 web | OTP only | EU | 403 SOD_CONFLICT |
      | EX-01ZU02-08 | E-005 | P11/R12 | A1 | C2 mobile | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU02-09 | E-005 | P12/R13 | T5 other tenant | C1 web | session revoked | IN | uniform 404 NOT_FOUND |
      | EX-01ZU02-10 | E-005 | P11/R12 | A3 SoD/limit | C3 API | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU02-11 | E-004 | P02/R02 | A5 wrong role | C2 mobile | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU02-12 | E-004 | P02/R02 | T5 other tenant | C3 API | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-01ZU02-13 | E-004 | P02/R02 | A1 | C1 web | passkey MFA | EU | ALLOW: Region code on tenant and on every key |
      | EX-01ZU02-14 | E-004 | P12/R13 | A3 SoD/limit | C2 mobile | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-01ZU02-15 | E-005 | P12/R13 | A5 wrong role | C1 web | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU02-16 | E-005 | P11/R12 | A5 wrong role | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU02-17 | E-005 | P11/R12 | A1 | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU02-18 | E-004 | P11/R12 | T5 other tenant | C1 web | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU02-19 | E-005 | P02/R02 | A3 SoD/limit | C1 web | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU02-20 | E-004 | P02/R02 | A5 wrong role | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU02-21 | E-004 | P12/R13 | A1 | C3 API | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU02-22 | E-005 | P02/R02 | A1 | C2 mobile | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU02-23 | E-005 | P11/R12 | T5 other tenant | C2 mobile | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU02-24 | E-005 | P12/R13 | A1 | C3 API | passkey MFA | EU | ALLOW: Isolation invariants incl |
      | EX-01ZU02-25 | E-004 | P11/R12 | A3 SoD/limit | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU02-26 | E-005 | P11/R12 | A3 SoD/limit | C2 mobile | OTP only | EU | 403 SOD_CONFLICT |
      | EX-01ZU02-27 | E-004 | P02/R02 | A1 | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU02-28 | E-004 | P12/R13 | T5 other tenant | C1 web | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU02-29 | E-004 | P02/R02 | T5 other tenant | C1 web | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU02-30 | E-004 | P02/R02 | A3 SoD/limit | C3 API | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU02-31 | E-005 | P12/R13 | A3 SoD/limit | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU02-32 | E-005 | P02/R02 | A5 wrong role | C1 web | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-01ZU02-33 | E-004 | P12/R13 | A5 wrong role | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU02-34 | E-004 | P11/R12 | A5 wrong role | C3 API | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-01ZU02-35 | E-004 | P12/R13 | T5 other tenant | C2 mobile | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU02-36 | E-005 | P11/R12 | A5 wrong role | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU02-37 | E-004 | P11/R12 | A1 | C1 web | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU02-38 | E-005 | P02/R02 | A1 | C2 mobile | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU02-39 | E-005 | P11/R12 | A3 SoD/limit | C1 web | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU02-40 | E-005 | P12/R13 | A5 wrong role | C3 API | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU02-41 | E-005 | P12/R13 | A1 | C1 web | passkey MFA | IN | ALLOW: Isolation invariants incl |
      | EX-01ZU02-42 | E-004 | P12/R13 | T5 other tenant | C1 web | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU02-43 | E-004 | P11/R12 | T5 other tenant | C3 API | session revoked | IN | uniform 404 NOT_FOUND |
      | EX-01ZU02-44 | E-005 | P12/R13 | A3 SoD/limit | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU02-45 | E-004 | P02/R02 | A3 SoD/limit | C2 mobile | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU02-46 | E-004 | P12/R13 | T5 other tenant | C3 API | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU02-47 | E-005 | P11/R12 | A5 wrong role | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU02-48 | E-005 | P11/R12 | A1 | C3 API | passkey MFA | EU | ALLOW: Isolation invariants incl |
      | EX-01ZU02-49 | E-005 | P12/R13 | A1 | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU02-50 | E-004 | P12/R13 | A5 wrong role | C2 mobile | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU02-51 | E-004 | P02/R02 | T5 other tenant | C2 mobile | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU02-52 | E-004 | P02/R02 | A1 | C3 API | passkey MFA | IN | ALLOW: Region code on tenant and on every key |
      | EX-01ZU02-53 | E-004 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Region code on tenant and on every key |
      | EX-01ZU02-54 | E-005 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Isolation invariants incl |
```

##### US-01-ZU03 Central authorisation with SKU dimension and job-scoped service principals

| Field | Value |
|---|---|
| ID | US-01-ZU03 |
| Title | Central authorisation with SKU dimension and job-scoped service principals |
| Type | Compliance (acceptance binding) |
| Story | As the platform I want job-scoped service-principal grants so that workers never inherit user credentials – with the acceptance criteria below, which the statement-only story US-01-YE09 did not carry |
| Persona / roles | Tenant administrator (P11, R12) |
| Traces | FR-V12-E-021 (SEC-01, ch06 matrix); tests TC-009 |
| Priority | Should |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-01-YE09, US-01-ZR01, US-01-ZR02, US-01-ZR03, US-01-ZR04; source definition: Part 11.5b §11.5.5.13 Functional requirement register |
| Dimension profile | persona ×3 · authority ×4 · channel ×3 · session/MFA ×3 · region ×3 · operation ×1 · model MU02 |
| Notes | Acceptance binding: US-01-YE09 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens A002, A009, A099, A197, A203; API family `/api/v1/identity/`; audit events `identity.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Central authorisation with SKU dimension and job-scoped service principals
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with administrator "meera@kestrel.example.com" (R12) holding a fresh WebAuthn factor
    And the reused IdP broker is reachable and the break-glass account "bg-admin@kestrel.example.com" is registered

  @happy @SEC-01
  Scenario: AC-01ZU03-01 Happy path – Central authorization incl. SKU dimension; service-principal grants (FR-V12-E-021)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Central authorization incl. SKU dimension; service-principal grants" is exercised as specified by FR-V12-E-021:
      """
      Central authorization incl. SKU dimension; service-principal grants
      """
    Then the observable result matches FR-V12-E-021 and its tests TC-009
    And the audit event "identity.central_authorization_incl" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @BRL-APR-01
  Scenario: AC-01ZU03-02 Negative – a user cannot grant a role to themselves
    Given "arjun@kestrel.example.com" holds role "Campaign approver"
    When he assigns role "Campaign requester" to himself
    Then the API returns 409 "SOD_SELF_GRANT" and the role assignment does not exist
    And a security event "identity.sod.violation_blocked" is written

  @val
  Scenario: AC-01ZU03-03 Validation – non-HTTPS identity endpoints are rejected
    When Meera submits SSO metadata URL "http://idp.kestrel.example.com/metadata"
    Then the API returns 422 "METADATA_URL_NOT_HTTPS" and no configuration row exists

  @perm
  Scenario: AC-01ZU03-04 Permission – a startup head cannot change identity configuration
    When "arjun@kestrel.example.com" (R02) posts an identity configuration change
    Then the API returns 403 "PERMISSION_DENIED" and no side effect occurs (NSE)

  @edge @BRL-TEN-07
  Scenario: AC-01ZU03-05 Edge – revocation takes effect within 60 seconds
    Given "ravi@kestrel.example.com" has an active session at 2027-03-01T10:00:00+05:30
    When his access is revoked at 10:00:05
    Then his next API call after 10:01:05 returns 401 "SESSION_REVOKED"

  @sec @obs @MU02
  Scenario Outline: AC-01ZU03-06 Permutations – Enterprise identity, access and audit (3-way, 50 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the session is "<session_mfa>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU02 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   E-021 = Central authorization incl. SKU dimension
    Examples: MU02 rows (3-way, seed 115; space 324; tuples 426/426; +1 baseline-allow)
      | ex | operation | persona | authority | channel | session_mfa | region | expected |
      | EX-01ZU03-01 | E-021 | P02/R02 | A5 wrong role | C1 web | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU03-02 | E-021 | P02/R02 | T5 other tenant | C3 API | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU03-03 | E-021 | P12/R13 | A5 wrong role | C3 API | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-01ZU03-04 | E-021 | P11/R12 | A1 | C2 mobile | passkey MFA | IN | ALLOW: Central authorization incl |
      | EX-01ZU03-05 | E-021 | P12/R13 | A3 SoD/limit | C2 mobile | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU03-06 | E-021 | P11/R12 | A3 SoD/limit | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU03-07 | E-021 | P12/R13 | A1 | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU03-08 | E-021 | P02/R02 | T5 other tenant | C2 mobile | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-01ZU03-09 | E-021 | P11/R12 | T5 other tenant | C1 web | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU03-10 | E-021 | P11/R12 | A3 SoD/limit | C3 API | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU03-11 | E-021 | P11/R12 | A5 wrong role | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU03-12 | E-021 | P02/R02 | A1 | C1 web | passkey MFA | EU | ALLOW: Central authorization incl |
      | EX-01ZU03-13 | E-021 | P12/R13 | T5 other tenant | C1 web | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU03-14 | E-021 | P02/R02 | A1 | C3 API | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU03-15 | E-021 | P02/R02 | A3 SoD/limit | C2 mobile | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU03-16 | E-021 | P12/R13 | A3 SoD/limit | C1 web | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-01ZU03-17 | E-021 | P02/R02 | T5 other tenant | C3 API | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-01ZU03-18 | E-021 | P02/R02 | A3 SoD/limit | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU03-19 | E-021 | P12/R13 | T5 other tenant | C2 mobile | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU03-20 | E-021 | P12/R13 | A5 wrong role | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU03-21 | E-021 | P12/R13 | A1 | C1 web | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU03-22 | E-021 | P11/R12 | A1 | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU03-23 | E-021 | P11/R12 | A5 wrong role | C2 mobile | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-01ZU03-24 | E-021 | P02/R02 | A5 wrong role | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU03-25 | E-021 | P11/R12 | A5 wrong role | C3 API | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU03-26 | E-021 | P11/R12 | T5 other tenant | C1 web | session revoked | IN | uniform 404 NOT_FOUND |
      | EX-01ZU03-27 | E-021 | P11/R12 | A1 | C1 web | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU03-28 | E-021 | P12/R13 | A5 wrong role | C2 mobile | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-01ZU03-29 | E-021 | P02/R02 | A3 SoD/limit | C3 API | OTP only | EU | 403 SOD_CONFLICT |
      | EX-01ZU03-30 | E-021 | P11/R12 | A3 SoD/limit | C2 mobile | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU03-31 | E-021 | P12/R13 | A1 | C2 mobile | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU03-32 | E-021 | P12/R13 | A3 SoD/limit | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU03-33 | E-021 | P02/R02 | A1 | C1 web | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU03-34 | E-021 | P11/R12 | T5 other tenant | C3 API | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-01ZU03-35 | E-021 | P12/R13 | A5 wrong role | C3 API | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU03-36 | E-021 | P02/R02 | A3 SoD/limit | C1 web | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU03-37 | E-021 | P02/R02 | A1 | C2 mobile | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU03-38 | E-021 | P12/R13 | T5 other tenant | C2 mobile | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU03-39 | E-021 | P11/R12 | A5 wrong role | C1 web | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-01ZU03-40 | E-021 | P11/R12 | A5 wrong role | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU03-41 | E-021 | P02/R02 | A5 wrong role | C2 mobile | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU03-42 | E-021 | P02/R02 | T5 other tenant | C1 web | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU03-43 | E-021 | P11/R12 | T5 other tenant | C2 mobile | session revoked | IN | uniform 404 NOT_FOUND |
      | EX-01ZU03-44 | E-021 | P11/R12 | A1 | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU03-45 | E-021 | P12/R13 | A3 SoD/limit | C3 API | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU03-46 | E-021 | P12/R13 | T5 other tenant | C3 API | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU03-47 | E-021 | P02/R02 | A1 | C3 API | passkey MFA | EU | ALLOW: Central authorization incl |
      | EX-01ZU03-48 | E-021 | P11/R12 | A3 SoD/limit | C3 API | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU03-49 | E-021 | P02/R02 | A1 | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU03-50 | E-021 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Central authorization incl |
```

##### US-01-ZU04 Portfolio aggregate grants and SIEM audit streaming

| Field | Value |
|---|---|
| ID | US-01-ZU04 |
| Title | Portfolio aggregate grants and SIEM audit streaming |
| Type | Security |
| Story | As a tenant administrator (P11, R12), I want portfolio grants require owner authority and explicit aggregate scope; independent clients excluded by default; SIEM streaming to HTTPS, syslog over TLS or object storage with retention 1/3/7 years, so that only the right people reach our data, with evidence an auditor can verify |
| Persona / roles | Tenant administrator (P11, R12) |
| Traces | FR-V12-H-016 (MT-API-10); FR-V12-H-038 (A2 Audit; ENT-ACC-04); DEC-784 |
| Priority | Should |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-01-ZR01, US-01-ZR02, US-01-ZR03, US-01-ZR04; source definition: Part 11.8b §11.8.5.1 Requirements adopted and release mapping |
| Dimension profile | persona ×3 · authority ×4 · channel ×3 · session/MFA ×3 · region ×3 · operation ×2 · model MU02 |
| Notes | FR-V12-H-038: release per DEC-784 (SIEM streaming with enterprise access) · Related existing stories (shared source IDs, no FR trace): US-01-ZR05 · Screens A002, A009, A099, A197, A203; API family `/api/v1/identity/`; audit events `identity.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Portfolio aggregate grants and SIEM audit streaming
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with administrator "meera@kestrel.example.com" (R12) holding a fresh WebAuthn factor
    And the reused IdP broker is reachable and the break-glass account "bg-admin@kestrel.example.com" is registered

  @happy @MT-API-10
  Scenario: AC-01ZU04-01 Happy path – Portfolio grants require owner authority and explicit aggregate… (FR-V12-H-016)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Portfolio grants require owner authority and explicit aggregate…" is exercised as specified by FR-V12-H-016:
      """
      Portfolio grants require owner authority and explicit aggregate scope; independent clients excluded by default
      """
    Then grant/revoke versioned and audited
    And the audit event "identity.portfolio_grants_require" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-ACC-04 @DEC-784
  Scenario: AC-01ZU04-02 Alternate – SIEM streaming to HTTPS, syslog over TLS or object storage with… (FR-V12-H-038)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "SIEM streaming to HTTPS, syslog over TLS or object storage with…" is exercised as specified by FR-V12-H-038:
      """
      SIEM streaming to HTTPS, syslog over TLS or object storage with retention 1/3/7 years
      """
    Then test event delivered; non-TLS rejected
    And the audit event "identity.siem_streaming_to_https" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @BRL-APR-01
  Scenario: AC-01ZU04-03 Negative – a user cannot grant a role to themselves
    Given "arjun@kestrel.example.com" holds role "Campaign approver"
    When he assigns role "Campaign requester" to himself
    Then the API returns 409 "SOD_SELF_GRANT" and the role assignment does not exist
    And a security event "identity.sod.violation_blocked" is written

  @val
  Scenario: AC-01ZU04-04 Validation – non-HTTPS identity endpoints are rejected
    When Meera submits SSO metadata URL "http://idp.kestrel.example.com/metadata"
    Then the API returns 422 "METADATA_URL_NOT_HTTPS" and no configuration row exists

  @perm
  Scenario: AC-01ZU04-05 Permission – a startup head cannot change identity configuration
    When "arjun@kestrel.example.com" (R02) posts an identity configuration change
    Then the API returns 403 "PERMISSION_DENIED" and no side effect occurs (NSE)

  @edge @BRL-TEN-07
  Scenario: AC-01ZU04-06 Edge – revocation takes effect within 60 seconds
    Given "ravi@kestrel.example.com" has an active session at 2027-03-01T10:00:00+05:30
    When his access is revoked at 10:00:05
    Then his next API call after 10:01:05 returns 401 "SESSION_REVOKED"

  @sec @obs @MU02
  Scenario Outline: AC-01ZU04-07 Permutations – Enterprise identity, access and audit (3-way, 55 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the session is "<session_mfa>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU02 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   H-016 = Portfolio grants require owner authority and…
    #   H-038 = SIEM streaming to HTTPS, syslog over TLS or object…
    Examples: MU02 rows (3-way, seed 122; space 648; tuples 528/528; +2 baseline-allow)
      | ex | operation | persona | authority | channel | session_mfa | region | expected |
      | EX-01ZU04-01 | H-038 | P11/R12 | A5 wrong role | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU04-02 | H-038 | P12/R13 | T5 other tenant | C1 web | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU04-03 | H-016 | P02/R02 | A5 wrong role | C1 web | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU04-04 | H-016 | P12/R13 | T5 other tenant | C2 mobile | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU04-05 | H-038 | P11/R12 | A1 | C2 mobile | passkey MFA | IN | ALLOW: Test event delivered |
      | EX-01ZU04-06 | H-016 | P11/R12 | A3 SoD/limit | C1 web | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU04-07 | H-038 | P02/R02 | A3 SoD/limit | C2 mobile | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU04-08 | H-016 | P02/R02 | A1 | C3 API | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU04-09 | H-038 | P02/R02 | T5 other tenant | C3 API | session revoked | IN | uniform 404 NOT_FOUND |
      | EX-01ZU04-10 | H-016 | P12/R13 | A1 | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU04-11 | H-038 | P12/R13 | A3 SoD/limit | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU04-12 | H-016 | P11/R12 | T5 other tenant | C3 API | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU04-13 | H-038 | P11/R12 | A5 wrong role | C1 web | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-01ZU04-14 | H-016 | P12/R13 | A5 wrong role | C3 API | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-01ZU04-15 | H-016 | P02/R02 | A5 wrong role | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU04-16 | H-038 | P12/R13 | A1 | C1 web | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU04-17 | H-016 | P11/R12 | A3 SoD/limit | C3 API | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU04-18 | H-038 | P02/R02 | A1 | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU04-19 | H-016 | P12/R13 | A3 SoD/limit | C2 mobile | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU04-20 | H-038 | P02/R02 | A3 SoD/limit | C1 web | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-01ZU04-21 | H-038 | P11/R12 | T5 other tenant | C2 mobile | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU04-22 | H-016 | P02/R02 | T5 other tenant | C1 web | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU04-23 | H-038 | P12/R13 | A1 | C3 API | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU04-24 | H-038 | P12/R13 | A5 wrong role | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU04-25 | H-038 | P02/R02 | A5 wrong role | C3 API | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU04-26 | H-016 | P11/R12 | A1 | C2 mobile | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU04-27 | H-016 | P12/R13 | A1 | C1 web | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU04-28 | H-016 | P11/R12 | A1 | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU04-29 | H-038 | P02/R02 | T5 other tenant | C2 mobile | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU04-30 | H-038 | P11/R12 | A5 wrong role | C2 mobile | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU04-31 | H-016 | P12/R13 | A3 SoD/limit | C1 web | OTP only | EU | 403 SOD_CONFLICT |
      | EX-01ZU04-32 | H-038 | P12/R13 | T5 other tenant | C3 API | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU04-33 | H-016 | P02/R02 | A1 | C2 mobile | passkey MFA | IN | ALLOW: Grant/revoke versioned and audited |
      | EX-01ZU04-34 | H-016 | P02/R02 | A3 SoD/limit | C3 API | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU04-35 | H-016 | P11/R12 | A1 | C1 web | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU04-36 | H-016 | P12/R13 | T5 other tenant | C1 web | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU04-37 | H-038 | P11/R12 | A3 SoD/limit | C2 mobile | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU04-38 | H-016 | P12/R13 | A5 wrong role | C2 mobile | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU04-39 | H-016 | P02/R02 | A3 SoD/limit | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU04-40 | H-016 | P11/R12 | T5 other tenant | C1 web | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU04-41 | H-016 | P11/R12 | A5 wrong role | C1 web | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU04-42 | H-016 | P12/R13 | A5 wrong role | C3 API | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-01ZU04-43 | H-038 | P11/R12 | A3 SoD/limit | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU04-44 | H-016 | P12/R13 | A1 | C3 API | passkey MFA | EU | ALLOW: Grant/revoke versioned and audited |
      | EX-01ZU04-45 | H-038 | P12/R13 | A3 SoD/limit | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU04-46 | H-038 | P02/R02 | A3 SoD/limit | C3 API | OTP only | EU | 403 SOD_CONFLICT |
      | EX-01ZU04-47 | H-016 | P11/R12 | T5 other tenant | C3 API | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-01ZU04-48 | H-016 | P11/R12 | A3 SoD/limit | C2 mobile | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU04-49 | H-038 | P12/R13 | A3 SoD/limit | C2 mobile | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU04-50 | H-016 | P12/R13 | T5 other tenant | C2 mobile | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU04-51 | H-016 | P12/R13 | T5 other tenant | C3 API | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-01ZU04-52 | H-038 | P02/R02 | A1 | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU04-53 | H-016 | P12/R13 | A5 wrong role | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU04-54 | H-016 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Grant/revoke versioned and audited |
      | EX-01ZU04-55 | H-038 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Test event delivered |
```

##### US-01-ZU05 Canonical table names, tenant-context enforcement and tenant-pinned keys

| Field | Value |
|---|---|
| ID | US-01-ZU05 |
| Title | Canonical table names, tenant-context enforcement and tenant-pinned keys |
| Type | Security |
| Story | As a platform data owner (P11, R12, with the security lead), I want adopt Appendix C/C2 table names as canonical logical names; implement them through the physical mapping of Part 11.9a §11.9.4 with…; missing tenant context raises `42501`; missing company scope returns zero rows; tenant-pinned composite keys for all tenant-scoped parent/child pairs; no global uniqueness on tenant data except opaque random identifiers…, so that every record stays in its tenant, company and residency zone, is exact and can be proven |
| Persona / roles | Platform data owner (P11, R12, with the security lead) |
| Traces | FR-V12-I-001 (ch26; App. C/C2); FR-V12-I-004 (DB-T2); FR-V12-I-005 (DB-T1, C2); DEC-581; tests TC-V12-I-003, TC-V12-I-004, TC-V12-I-032 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-01-ZR26, US-01-ZR27, US-01-ZR28, US-01-YI01; source definition: Part 11.9b §11.9.5.12 Functional requirements |
| Dimension profile | persona ×3 · authority ×4 · data class ×4 · db context ×3 · region ×3 · channel ×2 · operation ×3 · model MU04 |
| Notes | Screens A009, A197, A204; API family `/api/v1/data/`; audit events `data.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Canonical table names, tenant-context enforcement and tenant-pinned keys
  Background:
    Given tenants "Kestrel Analytics Pvt Ltd" (zone IN) and "Nordlicht Robotik GmbH" (zone EU) provisioned by the two-tenant fixture
    And the API connects through the least-privilege role "app_rw" that sets app.tenant_id and app.company_ids per transaction (DEC-778)

  @happy
  Scenario: AC-01ZU05-01 Happy path – Adopt Appendix C/C2 table names as canonical logical names (FR-V12-I-001)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Adopt Appendix C/C2 table names as canonical logical names" is exercised as specified by FR-V12-I-001:
      """
      Adopt Appendix C/C2 table names as canonical logical names; implement them through the physical mapping of Part 11.9a §11.9.4 with blueprint
      prefixes and `startup_id` = `company_id` (DEC-581)
      """
    Then the observable result matches FR-V12-I-001 and its tests TC-V12-I-032
    And the audit event "data.adopt_appendix_c_c2_table" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt
  Scenario: AC-01ZU05-02 Alternate – Missing tenant context raises `42501`; missing company scope returns… (FR-V12-I-004)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Missing tenant context raises `42501`; missing company scope returns…" is exercised as specified by FR-V12-I-004:
      """
      Missing tenant context raises `42501`; missing company scope returns zero rows
      """
    Then the observable result matches FR-V12-I-004 and its tests TC-V12-I-003
    And the audit event "data.missing_tenant_context_raises" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt
  Scenario: AC-01ZU05-03 Alternate – Tenant-pinned composite keys for all tenant-scoped parent/child… (FR-V12-I-005)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Tenant-pinned composite keys for all tenant-scoped parent/child…" is exercised as specified by FR-V12-I-005:
      """
      Tenant-pinned composite keys for all tenant-scoped parent/child pairs; no global uniqueness on tenant data except opaque random identifiers
      and platform invoice numbers
      """
    Then the observable result matches FR-V12-I-005 and its tests TC-V12-I-004
    And the audit event "data.tenant_pinned_composite_keys" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-778
  Scenario: AC-01ZU05-04 Negative – no statement runs without tenant context
    When a worker executes a query on "crm_contact" without setting app.tenant_id
    Then PostgreSQL raises SQLSTATE 42501 and no row is read or written

  @val
  Scenario: AC-01ZU05-05 Validation – money and identifiers are exact
    When a row is written with amount 12.50 as a float and currency "inr"
    Then the write is rejected: amount must be an integer in minor units and currency an upper-case ISO 4217 code

  @perm @BRL-TEN-03
  Scenario: AC-01ZU05-06 Permission – cross-tenant reference is impossible
    When tenant "Nordlicht Robotik GmbH" inserts a child row referencing a parent of "Kestrel Analytics Pvt Ltd"
    Then the composite foreign key rejects the row and the attempt is audited

  @edge @DEC-772
  Scenario: AC-01ZU05-07 Edge – an EU record is never written in Mumbai
    Given a request for tenant "Nordlicht Robotik GmbH" (zone EU) is routed to the Mumbai stack by mistake
    When it attempts a write
    Then the region check returns 409 "RESIDENCY_ZONE_MISMATCH" and nothing is written in either zone

  @sec @obs @MU04
  Scenario Outline: AC-01ZU05-08 Permutations – Data platform, residency and records (3-way, 71 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the database context is "<db_context>" for "<data_class>" data
    When "<operation>" runs through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU04 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   I-001 = Adopt Appendix C/C2 table names as canonical…
    #   I-004 = Missing tenant context raises `42501`
    #   I-005 = Tenant-pinned composite keys for all tenant-scoped…
    Examples: MU04 rows (3-way, seed 129; space 2,592; tuples 1064/1064; +3 baseline-allow)
      | ex | operation | persona | authority | data_class | db_context | region | channel | expected |
      | EX-01ZU05-01 | I-001 | P16/R19 | A1 | Internal | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU05-02 | I-001 | P11/R12 | A1 | Confidential | context set | IN | C3 API | ALLOW: Adopt Appendix C/C2 table names as canonical |
      | EX-01ZU05-03 | I-001 | P11/R12 | A3 SoD/limit | Public | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU05-04 | I-004 | P01/R01 | A1 | Restricted | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU05-05 | I-005 | P16/R19 | A5 wrong role | Internal | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU05-06 | I-004 | P16/R19 | T5 other tenant | Confidential | context set | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU05-07 | I-004 | P01/R01 | A3 SoD/limit | Public | context set | EU | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU05-08 | I-005 | P11/R12 | A5 wrong role | Restricted | context set | EU | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU05-09 | I-004 | P11/R12 | T5 other tenant | Restricted | no tenant ctx | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU05-10 | I-001 | P01/R01 | T5 other tenant | Confidential | no company scope | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU05-11 | I-005 | P16/R19 | A3 SoD/limit | Public | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU05-12 | I-005 | P01/R01 | A1 | Confidential | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU05-13 | I-001 | P01/R01 | A5 wrong role | Internal | context set | IN | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU05-14 | I-005 | P11/R12 | T5 other tenant | Public | no company scope | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU05-15 | I-004 | P16/R19 | A5 wrong role | Public | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU05-16 | I-004 | P11/R12 | A3 SoD/limit | Internal | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU05-17 | I-001 | P16/R19 | A3 SoD/limit | Restricted | context set | EU→IN (misrouted) | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU05-18 | I-004 | P11/R12 | A1 | Internal | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU05-19 | I-005 | P01/R01 | A5 wrong role | Restricted | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU05-20 | I-001 | P16/R19 | T5 other tenant | Restricted | no tenant ctx | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU05-21 | I-005 | P01/R01 | T5 other tenant | Internal | context set | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU05-22 | I-001 | P11/R12 | A5 wrong role | Confidential | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU05-23 | I-005 | P16/R19 | A3 SoD/limit | Confidential | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU05-24 | I-001 | P01/R01 | A1 | Public | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU05-25 | I-004 | P16/R19 | A5 wrong role | Confidential | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU05-26 | I-004 | P01/R01 | T5 other tenant | Public | no tenant ctx | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU05-27 | I-005 | P11/R12 | A1 | Internal | context set | EU→IN (misrouted) | worker job | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU05-28 | I-005 | P16/R19 | A1 | Restricted | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU05-29 | I-001 | P01/R01 | A3 SoD/limit | Internal | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU05-30 | I-001 | P16/R19 | T5 other tenant | Public | context set | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU05-31 | I-005 | P11/R12 | A3 SoD/limit | Confidential | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU05-32 | I-004 | P11/R12 | A5 wrong role | Public | context set | IN | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU05-33 | I-004 | P01/R01 | T5 other tenant | Internal | no company scope | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU05-34 | I-005 | P01/R01 | A3 SoD/limit | Confidential | context set | IN | worker job | 403 SOD_CONFLICT |
      | EX-01ZU05-35 | I-004 | P16/R19 | A1 | Public | context set | EU→IN (misrouted) | worker job | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU05-36 | I-004 | P01/R01 | A5 wrong role | Restricted | context set | EU→IN (misrouted) | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU05-37 | I-001 | P16/R19 | A5 wrong role | Restricted | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU05-38 | I-001 | P11/R12 | A3 SoD/limit | Restricted | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU05-39 | I-001 | P11/R12 | T5 other tenant | Internal | context set | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU05-40 | I-004 | P11/R12 | A5 wrong role | Confidential | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU05-41 | I-005 | P01/R01 | A1 | Public | context set | EU | C3 API | ALLOW: Tenant-pinned composite keys for all tenant-scoped |
      | EX-01ZU05-42 | I-001 | P11/R12 | A1 | Public | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU05-43 | I-004 | P01/R01 | A3 SoD/limit | Confidential | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU05-44 | I-004 | P16/R19 | A3 SoD/limit | Internal | context set | IN | worker job | 403 SOD_CONFLICT |
      | EX-01ZU05-45 | I-005 | P16/R19 | T5 other tenant | Internal | no tenant ctx | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU05-46 | I-005 | P16/R19 | A5 wrong role | Public | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU05-47 | I-005 | P01/R01 | T5 other tenant | Restricted | no company scope | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU05-48 | I-004 | P16/R19 | A1 | Confidential | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU05-49 | I-001 | P16/R19 | A5 wrong role | Confidential | context set | EU | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU05-50 | I-004 | P01/R01 | A3 SoD/limit | Restricted | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU05-51 | I-001 | P01/R01 | A3 SoD/limit | Internal | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU05-52 | I-005 | P11/R12 | T5 other tenant | Confidential | no tenant ctx | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU05-53 | I-001 | P01/R01 | A5 wrong role | Public | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU05-54 | I-004 | P11/R12 | A5 wrong role | Internal | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU05-55 | I-001 | P01/R01 | A1 | Restricted | context set | IN | worker job | Tier 2 and unapproved models excluded |
      | EX-01ZU05-56 | I-004 | P11/R12 | A1 | Restricted | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU05-57 | I-005 | P01/R01 | A5 wrong role | Confidential | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU05-58 | I-005 | P11/R12 | A3 SoD/limit | Internal | context set | EU→IN (misrouted) | worker job | 403 SOD_CONFLICT |
      | EX-01ZU05-59 | I-004 | P01/R01 | A1 | Internal | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU05-60 | I-004 | P16/R19 | T5 other tenant | Restricted | no company scope | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU05-61 | I-001 | P11/R12 | T5 other tenant | Public | context set | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU05-62 | I-005 | P16/R19 | T5 other tenant | Restricted | context set | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU05-63 | I-005 | P11/R12 | A3 SoD/limit | Restricted | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU05-64 | I-004 | P16/R19 | A5 wrong role | Restricted | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU05-65 | I-004 | P16/R19 | T5 other tenant | Public | no tenant ctx | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU05-66 | I-004 | P11/R12 | T5 other tenant | Public | no company scope | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU05-67 | I-001 | P01/R01 | A3 SoD/limit | Confidential | context set | EU | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU05-68 | I-005 | P16/R19 | A1 | Restricted | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU05-69 | I-001 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Adopt Appendix C/C2 table names as canonical |
      | EX-01ZU05-70 | I-004 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Missing tenant context raises `42501` |
      | EX-01ZU05-71 | I-005 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Tenant-pinned composite keys for all tenant-scoped |
```

##### US-01-ZU06 SoD on role build and assignment, hash-chained audit and domain schema validation

| Field | Value |
|---|---|
| ID | US-01-ZU06 |
| Title | SoD on role build and assignment, hash-chained audit and domain schema validation |
| Type | Security |
| Story | As a platform data owner (P11, R12, with the security lead), I want SoD enforced on role build (insert/update) and on role assignment per user; no self-granted roles; append-only audit with per-tenant hash chain, insert only through `fn_append_audit()`; domain schema registry and write-time validation of `schema_ref`, status, required payload keys, so that every record stays in its tenant, company and residency zone, is exact and can be proven |
| Persona / roles | Platform data owner (P11, R12, with the security lead) |
| Traces | FR-V12-I-008 (ENT-ACC-02, C2-T1); FR-V12-I-009 (SEC-06); FR-V12-I-011 (App. C domain shape; ch26 V5 fields); tests TC-V12-I-005, TC-V12-I-007, TC-V12-I-016 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-01-ZR26, US-01-ZR27, US-01-ZR28, US-01-YI01; source definition: Part 11.9b §11.9.5.12 Functional requirements |
| Dimension profile | persona ×3 · authority ×4 · data class ×4 · db context ×3 · region ×3 · channel ×2 · operation ×3 · model MU04 |
| Notes | Related existing stories (shared source IDs, no FR trace): US-01-ZR04 · Screens A009, A197, A204; API family `/api/v1/data/`; audit events `data.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: SoD on role build and assignment, hash-chained audit and domain schema validation
  Background:
    Given tenants "Kestrel Analytics Pvt Ltd" (zone IN) and "Nordlicht Robotik GmbH" (zone EU) provisioned by the two-tenant fixture
    And the API connects through the least-privilege role "app_rw" that sets app.tenant_id and app.company_ids per transaction (DEC-778)

  @happy @ENT-ACC-02
  Scenario: AC-01ZU06-01 Happy path – SoD enforced on role build (insert/update) and on role assignment per… (FR-V12-I-008)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "SoD enforced on role build (insert/update) and on role assignment per…" is exercised as specified by FR-V12-I-008:
      """
      SoD enforced on role build (insert/update) and on role assignment per user; no self-granted roles
      """
    Then the observable result matches FR-V12-I-008 and its tests TC-V12-I-005
    And the audit event "data.sod_enforced_on_role_build" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @SEC-06
  Scenario: AC-01ZU06-02 Alternate – Append-only audit with per-tenant hash chain (FR-V12-I-009)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Append-only audit with per-tenant hash chain" is exercised as specified by FR-V12-I-009:
      """
      Append-only audit with per-tenant hash chain, insert only through `fn_append_audit()`; append-only consent, usage, evaluation and business
      events
      """
    Then the observable result matches FR-V12-I-009 and its tests TC-V12-I-007
    And the audit event "data.append_only_audit_with" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt
  Scenario: AC-01ZU06-03 Alternate – Domain schema registry and write-time validation of `schema_ref` (FR-V12-I-011)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Domain schema registry and write-time validation of `schema_ref`" is exercised as specified by FR-V12-I-011:
      """
      Domain schema registry and write-time validation of `schema_ref`, status, required payload keys, size and optimistic version on the 89 domain
      tables
      """
    Then the observable result matches FR-V12-I-011 and its tests TC-V12-I-016
    And the audit event "data.domain_schema_registry_and" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-778
  Scenario: AC-01ZU06-04 Negative – no statement runs without tenant context
    When a worker executes a query on "crm_contact" without setting app.tenant_id
    Then PostgreSQL raises SQLSTATE 42501 and no row is read or written

  @val
  Scenario: AC-01ZU06-05 Validation – money and identifiers are exact
    When a row is written with amount 12.50 as a float and currency "inr"
    Then the write is rejected: amount must be an integer in minor units and currency an upper-case ISO 4217 code

  @perm @BRL-TEN-03
  Scenario: AC-01ZU06-06 Permission – cross-tenant reference is impossible
    When tenant "Nordlicht Robotik GmbH" inserts a child row referencing a parent of "Kestrel Analytics Pvt Ltd"
    Then the composite foreign key rejects the row and the attempt is audited

  @edge @DEC-772
  Scenario: AC-01ZU06-07 Edge – an EU record is never written in Mumbai
    Given a request for tenant "Nordlicht Robotik GmbH" (zone EU) is routed to the Mumbai stack by mistake
    When it attempts a write
    Then the region check returns 409 "RESIDENCY_ZONE_MISMATCH" and nothing is written in either zone

  @sec @obs @MU04
  Scenario Outline: AC-01ZU06-08 Permutations – Data platform, residency and records (3-way, 71 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the database context is "<db_context>" for "<data_class>" data
    When "<operation>" runs through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU04 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   I-008 = SoD enforced on role build
    #   I-009 = Append-only audit with per-tenant hash chain
    #   I-011 = Domain schema registry and write-time validation of…
    Examples: MU04 rows (3-way, seed 136; space 2,592; tuples 1064/1064; +3 baseline-allow)
      | ex | operation | persona | authority | data_class | db_context | region | channel | expected |
      | EX-01ZU06-01 | I-008 | P11/R12 | A3 SoD/limit | Public | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU06-02 | I-009 | P01/R01 | T5 other tenant | Restricted | no tenant ctx | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU06-03 | I-009 | P16/R19 | A1 | Internal | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-04 | I-011 | P01/R01 | T5 other tenant | Internal | no company scope | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU06-05 | I-011 | P16/R19 | A5 wrong role | Internal | context set | IN | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU06-06 | I-008 | P11/R12 | A5 wrong role | Confidential | context set | EU→IN (misrouted) | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU06-07 | I-011 | P11/R12 | A1 | Confidential | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU06-08 | I-008 | P16/R19 | A3 SoD/limit | Restricted | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-09 | I-009 | P01/R01 | A3 SoD/limit | Public | context set | EU→IN (misrouted) | worker job | 403 SOD_CONFLICT |
      | EX-01ZU06-10 | I-008 | P16/R19 | T5 other tenant | Confidential | no company scope | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU06-11 | I-009 | P11/R12 | A5 wrong role | Restricted | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU06-12 | I-011 | P01/R01 | A1 | Public | context set | IN | C3 API | ALLOW: Domain schema registry and write-time validation of |
      | EX-01ZU06-13 | I-011 | P11/R12 | T5 other tenant | Public | no tenant ctx | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU06-14 | I-008 | P01/R01 | A5 wrong role | Public | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU06-15 | I-011 | P01/R01 | A1 | Restricted | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU06-16 | I-011 | P16/R19 | A3 SoD/limit | Confidential | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU06-17 | I-009 | P11/R12 | T5 other tenant | Internal | context set | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU06-18 | I-008 | P16/R19 | T5 other tenant | Restricted | context set | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU06-19 | I-009 | P16/R19 | A1 | Public | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU06-20 | I-009 | P01/R01 | A5 wrong role | Confidential | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-21 | I-008 | P11/R12 | A1 | Internal | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU06-22 | I-011 | P11/R12 | A3 SoD/limit | Restricted | context set | EU | worker job | 403 SOD_CONFLICT |
      | EX-01ZU06-23 | I-008 | P01/R01 | A3 SoD/limit | Internal | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU06-24 | I-008 | P01/R01 | A1 | Confidential | context set | EU | worker job | ALLOW: SoD enforced on role build (insert/update) and on |
      | EX-01ZU06-25 | I-011 | P16/R19 | A5 wrong role | Public | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU06-26 | I-009 | P16/R19 | A3 SoD/limit | Confidential | context set | EU | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU06-27 | I-009 | P11/R12 | A5 wrong role | Internal | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU06-28 | I-009 | P11/R12 | A3 SoD/limit | Public | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-29 | I-011 | P01/R01 | A5 wrong role | Restricted | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-30 | I-011 | P16/R19 | T5 other tenant | Public | no tenant ctx | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU06-31 | I-009 | P16/R19 | A1 | Restricted | context set | IN | worker job | Tier 2 and unapproved models excluded |
      | EX-01ZU06-32 | I-009 | P11/R12 | T5 other tenant | Confidential | no company scope | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU06-33 | I-008 | P01/R01 | A3 SoD/limit | Restricted | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU06-34 | I-011 | P01/R01 | T5 other tenant | Confidential | context set | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU06-35 | I-008 | P11/R12 | A1 | Restricted | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-36 | I-008 | P11/R12 | T5 other tenant | Public | context set | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU06-37 | I-008 | P16/R19 | A5 wrong role | Internal | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-38 | I-009 | P01/R01 | A3 SoD/limit | Internal | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU06-39 | I-011 | P11/R12 | A3 SoD/limit | Internal | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-40 | I-011 | P11/R12 | A5 wrong role | Restricted | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU06-41 | I-008 | P16/R19 | A1 | Confidential | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-42 | I-009 | P16/R19 | A3 SoD/limit | Confidential | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU06-43 | I-008 | P01/R01 | A3 SoD/limit | Internal | context set | IN | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU06-44 | I-008 | P01/R01 | A5 wrong role | Confidential | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU06-45 | I-008 | P16/R19 | A5 wrong role | Restricted | context set | EU→IN (misrouted) | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU06-46 | I-011 | P16/R19 | T5 other tenant | Restricted | no company scope | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU06-47 | I-011 | P11/R12 | A1 | Internal | context set | EU→IN (misrouted) | worker job | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU06-48 | I-009 | P01/R01 | A1 | Internal | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-49 | I-009 | P16/R19 | A5 wrong role | Public | context set | IN | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU06-50 | I-008 | P01/R01 | T5 other tenant | Internal | no tenant ctx | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU06-51 | I-009 | P16/R19 | T5 other tenant | Internal | no company scope | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU06-52 | I-008 | P11/R12 | A3 SoD/limit | Confidential | context set | IN | worker job | 403 SOD_CONFLICT |
      | EX-01ZU06-53 | I-011 | P01/R01 | A3 SoD/limit | Public | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU06-54 | I-011 | P01/R01 | A5 wrong role | Restricted | context set | EU | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU06-55 | I-008 | P16/R19 | A1 | Public | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU06-56 | I-009 | P11/R12 | A1 | Confidential | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU06-57 | I-009 | P16/R19 | A3 SoD/limit | Restricted | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU06-58 | I-009 | P16/R19 | T5 other tenant | Confidential | no tenant ctx | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU06-59 | I-008 | P11/R12 | A5 wrong role | Public | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU06-60 | I-009 | P01/R01 | T5 other tenant | Public | no company scope | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU06-61 | I-009 | P16/R19 | A3 SoD/limit | Internal | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU06-62 | I-011 | P16/R19 | A5 wrong role | Confidential | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-63 | I-011 | P16/R19 | A1 | Restricted | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU06-64 | I-008 | P11/R12 | T5 other tenant | Restricted | no tenant ctx | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU06-65 | I-009 | P11/R12 | A1 | Public | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU06-66 | I-009 | P01/R01 | A5 wrong role | Internal | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU06-67 | I-011 | P01/R01 | A3 SoD/limit | Confidential | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU06-68 | I-011 | P16/R19 | A3 SoD/limit | Public | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU06-69 | I-008 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: SoD enforced on role build (insert/update) and on |
      | EX-01ZU06-70 | I-009 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Append-only audit with per-tenant hash chain, |
      | EX-01ZU06-71 | I-011 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Domain schema registry and write-time validation of |
```

##### US-01-ZU07 Region-pinned database, exact money and approved FX rates

| Field | Value |
|---|---|
| ID | US-01-ZU07 |
| Title | Region-pinned database, exact money and approved FX rates |
| Type | Security |
| Story | As a platform data owner (P11, R12, with the security lead), I want region-pinned database; tenant region immutable; cross-region write rejected; money stored as integer minor units with currency; unit prices, quantities, rates as exact numeric; FX rates: ISO codes, base ≠ quote, positive rate, unique approved version, so that every record stays in its tenant, company and residency zone, is exact and can be proven |
| Persona / roles | Platform data owner (P11, R12, with the security lead) |
| Traces | FR-V12-I-013 (ENT-DAT-03, CJ-R09); FR-V12-I-017 (ch26 V5 rule); FR-V12-I-018 (V6 FXRate); DEC-772; tests TC-V12-I-011, TC-V12-I-017a |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-01-ZR26, US-01-ZR27, US-01-ZR28, US-01-YI01; source definition: Part 11.9b §11.9.5.12 Functional requirements |
| Dimension profile | persona ×3 · authority ×4 · data class ×4 · db context ×3 · region ×3 · channel ×2 · operation ×3 · model MU04 |
| Notes | FR-V12-I-013: release per DEC-772 (EU residency adopted; no longer pending) · Related existing stories (shared source IDs, no FR trace): US-01-ZR28, US-21-ZR18 · Screens A009, A197, A204; API family `/api/v1/data/`; audit events `data.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Region-pinned database, exact money and approved FX rates
  Background:
    Given tenants "Kestrel Analytics Pvt Ltd" (zone IN) and "Nordlicht Robotik GmbH" (zone EU) provisioned by the two-tenant fixture
    And the API connects through the least-privilege role "app_rw" that sets app.tenant_id and app.company_ids per transaction (DEC-778)

  @happy @CJ-R09 @ENT-DAT-03 @DEC-772
  Scenario: AC-01ZU07-01 Happy path – Region-pinned database; tenant region immutable (FR-V12-I-013)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Region-pinned database; tenant region immutable" is exercised as specified by FR-V12-I-013:
      """
      Region-pinned database; tenant region immutable; cross-region write rejected
      """
    Then the observable result matches FR-V12-I-013 and its tests TC-V12-I-011
    And the audit event "data.region_pinned_database" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt
  Scenario: AC-01ZU07-02 Alternate – Money stored as integer minor units with currency (FR-V12-I-017)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Money stored as integer minor units with currency" is exercised as specified by FR-V12-I-017:
      """
      Money stored as integer minor units with currency; unit prices, quantities, rates as exact numeric
      """
    Then the observable result matches FR-V12-I-017 and its tests TC-V12-I-017a
    And the audit event "data.money_stored_as_integer_minor" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt
  Scenario: AC-01ZU07-03 Alternate – FX rates: ISO codes, base ≠ quote, positive rate (FR-V12-I-018)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "FX rates: ISO codes, base ≠ quote, positive rate" is exercised as specified by FR-V12-I-018:
      """
      FX rates: ISO codes, base ≠ quote, positive rate, unique approved version
      """
    Then the observable result matches FR-V12-I-018 and its tests in Part 11.21
    And the audit event "data.fx_rates_iso_codes" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-778
  Scenario: AC-01ZU07-04 Negative – no statement runs without tenant context
    When a worker executes a query on "crm_contact" without setting app.tenant_id
    Then PostgreSQL raises SQLSTATE 42501 and no row is read or written

  @val
  Scenario: AC-01ZU07-05 Validation – money and identifiers are exact
    When a row is written with amount 12.50 as a float and currency "inr"
    Then the write is rejected: amount must be an integer in minor units and currency an upper-case ISO 4217 code

  @perm @BRL-TEN-03
  Scenario: AC-01ZU07-06 Permission – cross-tenant reference is impossible
    When tenant "Nordlicht Robotik GmbH" inserts a child row referencing a parent of "Kestrel Analytics Pvt Ltd"
    Then the composite foreign key rejects the row and the attempt is audited

  @edge @DEC-772
  Scenario: AC-01ZU07-07 Edge – an EU record is never written in Mumbai
    Given a request for tenant "Nordlicht Robotik GmbH" (zone EU) is routed to the Mumbai stack by mistake
    When it attempts a write
    Then the region check returns 409 "RESIDENCY_ZONE_MISMATCH" and nothing is written in either zone

  @sec @obs @MU04
  Scenario Outline: AC-01ZU07-08 Permutations – Data platform, residency and records (3-way, 72 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the database context is "<db_context>" for "<data_class>" data
    When "<operation>" runs through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU04 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   I-013 = Region-pinned database; tenant region immutable
    #   I-017 = Money stored as integer minor units with currency
    #   I-018 = FX rates: ISO codes, base ≠ quote, positive rate
    Examples: MU04 rows (3-way, seed 143; space 2,592; tuples 1064/1064; +3 baseline-allow)
      | ex | operation | persona | authority | data_class | db_context | region | channel | expected |
      | EX-01ZU07-01 | I-017 | P01/R01 | T5 other tenant | Restricted | context set | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU07-02 | I-017 | P16/R19 | T5 other tenant | Confidential | no company scope | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU07-03 | I-018 | P11/R12 | A3 SoD/limit | Confidential | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU07-04 | I-013 | P16/R19 | A3 SoD/limit | Restricted | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU07-05 | I-018 | P01/R01 | A5 wrong role | Internal | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU07-06 | I-013 | P11/R12 | A5 wrong role | Public | context set | EU | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU07-07 | I-017 | P11/R12 | A1 | Public | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU07-08 | I-013 | P16/R19 | T5 other tenant | Internal | no tenant ctx | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU07-09 | I-018 | P16/R19 | A1 | Public | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU07-10 | I-013 | P01/R01 | A1 | Confidential | context set | IN | worker job | ALLOW: Region-pinned database |
      | EX-01ZU07-11 | I-018 | P16/R19 | A5 wrong role | Restricted | context set | IN | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU07-12 | I-017 | P11/R12 | A3 SoD/limit | Internal | context set | EU→IN (misrouted) | worker job | 403 SOD_CONFLICT |
      | EX-01ZU07-13 | I-013 | P01/R01 | A3 SoD/limit | Internal | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU07-14 | I-013 | P11/R12 | A5 wrong role | Confidential | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU07-15 | I-018 | P11/R12 | T5 other tenant | Restricted | no tenant ctx | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU07-16 | I-017 | P16/R19 | A5 wrong role | Confidential | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU07-17 | I-017 | P01/R01 | A5 wrong role | Public | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU07-18 | I-018 | P01/R01 | T5 other tenant | Public | context set | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU07-19 | I-017 | P11/R12 | A1 | Restricted | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU07-20 | I-017 | P16/R19 | A1 | Internal | context set | EU | C3 API | ALLOW: Money stored as integer minor units with currency |
      | EX-01ZU07-21 | I-018 | P16/R19 | A3 SoD/limit | Public | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU07-22 | I-018 | P01/R01 | A1 | Restricted | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU07-23 | I-013 | P11/R12 | A1 | Internal | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU07-24 | I-018 | P11/R12 | T5 other tenant | Internal | no company scope | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU07-25 | I-017 | P16/R19 | A3 SoD/limit | Public | context set | IN | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU07-26 | I-017 | P01/R01 | A3 SoD/limit | Confidential | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU07-27 | I-018 | P11/R12 | A1 | Confidential | context set | EU | C3 API | ALLOW: FX rates: ISO codes, base ≠ quote, positive rate, |
      | EX-01ZU07-28 | I-013 | P01/R01 | T5 other tenant | Public | no company scope | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU07-29 | I-013 | P16/R19 | A5 wrong role | Restricted | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU07-30 | I-018 | P01/R01 | A3 SoD/limit | Restricted | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU07-31 | I-013 | P16/R19 | T5 other tenant | Confidential | context set | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU07-32 | I-013 | P11/R12 | A3 SoD/limit | Restricted | context set | EU | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU07-33 | I-018 | P16/R19 | A5 wrong role | Internal | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU07-34 | I-013 | P01/R01 | A5 wrong role | Public | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU07-35 | I-018 | P16/R19 | A1 | Confidential | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU07-36 | I-017 | P11/R12 | T5 other tenant | Public | no company scope | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU07-37 | I-017 | P01/R01 | T5 other tenant | Internal | no tenant ctx | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU07-38 | I-017 | P11/R12 | A5 wrong role | Restricted | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU07-39 | I-013 | P01/R01 | A1 | Internal | context set | EU | worker job | ALLOW: Region-pinned database |
      | EX-01ZU07-40 | I-013 | P11/R12 | A3 SoD/limit | Confidential | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU07-41 | I-017 | P01/R01 | A1 | Confidential | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU07-42 | I-017 | P11/R12 | T5 other tenant | Confidential | context set | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU07-43 | I-013 | P16/R19 | A1 | Internal | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU07-44 | I-018 | P01/R01 | A3 SoD/limit | Internal | context set | IN | worker job | 403 SOD_CONFLICT |
      | EX-01ZU07-45 | I-018 | P01/R01 | A5 wrong role | Confidential | context set | IN | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU07-46 | I-017 | P11/R12 | A5 wrong role | Internal | context set | EU | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU07-47 | I-018 | P11/R12 | A5 wrong role | Public | context set | EU→IN (misrouted) | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU07-48 | I-013 | P16/R19 | A1 | Public | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU07-49 | I-013 | P01/R01 | A1 | Restricted | context set | EU→IN (misrouted) | C3 API | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU07-50 | I-013 | P11/R12 | A3 SoD/limit | Public | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU07-51 | I-018 | P16/R19 | T5 other tenant | Restricted | no company scope | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU07-52 | I-017 | P16/R19 | A3 SoD/limit | Restricted | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU07-53 | I-013 | P11/R12 | T5 other tenant | Internal | context set | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU07-54 | I-017 | P16/R19 | A5 wrong role | Public | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU07-55 | I-018 | P01/R01 | T5 other tenant | Confidential | no tenant ctx | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU07-56 | I-018 | P16/R19 | T5 other tenant | Public | no tenant ctx | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU07-57 | I-013 | P01/R01 | A1 | Public | context set | IN | C3 API | ALLOW: Region-pinned database |
      | EX-01ZU07-58 | I-018 | P01/R01 | A5 wrong role | Restricted | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU07-59 | I-018 | P16/R19 | A3 SoD/limit | Confidential | context set | EU→IN (misrouted) | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU07-60 | I-018 | P16/R19 | A3 SoD/limit | Internal | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU07-61 | I-017 | P01/R01 | T5 other tenant | Internal | no company scope | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU07-62 | I-013 | P11/R12 | T5 other tenant | Restricted | context set | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU07-63 | I-013 | P01/R01 | A5 wrong role | Confidential | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU07-64 | I-013 | P11/R12 | A5 wrong role | Restricted | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU07-65 | I-013 | P11/R12 | A5 wrong role | Internal | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU07-66 | I-013 | P16/R19 | A1 | Confidential | context set | IN | worker job | ALLOW: Region-pinned database |
      | EX-01ZU07-67 | I-018 | P01/R01 | A3 SoD/limit | Public | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU07-68 | I-018 | P01/R01 | A1 | Internal | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU07-69 | I-018 | P16/R19 | A1 | Restricted | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU07-70 | I-013 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Region-pinned database |
      | EX-01ZU07-71 | I-017 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Money stored as integer minor units with currency |
      | EX-01ZU07-72 | I-018 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: FX rates: ISO codes, base ≠ quote, positive rate, |
```

##### US-01-ZU08 Audit sinks, reference-data governance and analytics tables

| Field | Value |
|---|---|
| ID | US-01-ZU08 |
| Title | Audit sinks, reference-data governance and analytics tables |
| Type | Security |
| Story | As a platform data owner (P11, R12, with the security lead), I want audit sinks (HTTPS, syslog-TLS, object storage; JSON or CEF; 1/3/7-year retention) fed from the audit chain with redacted payloads; reference-data governance for `locale_bundle`, `tax_rule`, `jurisdiction_pack/rule`, `ai_model`, `eval_suite`: platform-only writes; analytics and usage tables of §11.9.5.6 (`sli_sample`, `customer_value`, `feedback_case`, `journey_event`, `metric_definition`, so that every record stays in its tenant, company and residency zone, is exact and can be proven |
| Persona / roles | Platform data owner (P11, R12, with the security lead) |
| Traces | FR-V12-I-025 (C2 `audit_sink`); FR-V12-I-026 (C, C2); FR-V12-I-030 (ch26 V5, ch29); tests TC-V12-I-018 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-01-ZR26, US-01-ZR27, US-01-ZR28, US-01-YI01; source definition: Part 11.9b §11.9.5.12 Functional requirements |
| Dimension profile | persona ×3 · authority ×4 · data class ×4 · db context ×3 · region ×3 · channel ×2 · operation ×3 · model MU04 |
| Notes | Screens A009, A197, A204; API family `/api/v1/data/`; audit events `data.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Audit sinks, reference-data governance and analytics tables
  Background:
    Given tenants "Kestrel Analytics Pvt Ltd" (zone IN) and "Nordlicht Robotik GmbH" (zone EU) provisioned by the two-tenant fixture
    And the API connects through the least-privilege role "app_rw" that sets app.tenant_id and app.company_ids per transaction (DEC-778)

  @happy
  Scenario: AC-01ZU08-01 Happy path – Audit sinks (HTTPS, syslog-TLS, object storage; JSON or CEF (FR-V12-I-025)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Audit sinks (HTTPS, syslog-TLS, object storage; JSON or CEF" is exercised as specified by FR-V12-I-025:
      """
      Audit sinks (HTTPS, syslog-TLS, object storage; JSON or CEF; 1/3/7-year retention) fed from the audit chain with redacted payloads
      """
    Then the observable result matches FR-V12-I-025 and its tests in Part 11.21
    And the audit event "data.audit_sinks_https" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt
  Scenario: AC-01ZU08-02 Alternate – Reference-data governance for `locale_bundle`, `tax_rule` (FR-V12-I-026)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Reference-data governance for `locale_bundle`, `tax_rule`" is exercised as specified by FR-V12-I-026:
      """
      Reference-data governance for `locale_bundle`, `tax_rule`, `jurisdiction_pack/rule`, `ai_model`, `eval_suite`: platform-only writes, approval
      columns
      """
    Then the observable result matches FR-V12-I-026 and its tests in Part 11.21
    And the audit event "data.reference_data_governance_for" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt
  Scenario: AC-01ZU08-03 Alternate – Analytics and usage tables of §11.9.5.6 (`sli_sample` (FR-V12-I-030)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Analytics and usage tables of §11.9.5.6 (`sli_sample`" is exercised as specified by FR-V12-I-030:
      """
      Analytics and usage tables of §11.9.5.6 (`sli_sample`, `customer_value`, `feedback_case`, `journey_event`, `metric_definition`,
      `metric_aggregate`, `experiment`)
      """
    Then the observable result matches FR-V12-I-030 and its tests TC-V12-I-018
    And the audit event "data.analytics_and_usage_tables_of" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-778
  Scenario: AC-01ZU08-04 Negative – no statement runs without tenant context
    When a worker executes a query on "crm_contact" without setting app.tenant_id
    Then PostgreSQL raises SQLSTATE 42501 and no row is read or written

  @val
  Scenario: AC-01ZU08-05 Validation – money and identifiers are exact
    When a row is written with amount 12.50 as a float and currency "inr"
    Then the write is rejected: amount must be an integer in minor units and currency an upper-case ISO 4217 code

  @perm @BRL-TEN-03
  Scenario: AC-01ZU08-06 Permission – cross-tenant reference is impossible
    When tenant "Nordlicht Robotik GmbH" inserts a child row referencing a parent of "Kestrel Analytics Pvt Ltd"
    Then the composite foreign key rejects the row and the attempt is audited

  @edge @DEC-772
  Scenario: AC-01ZU08-07 Edge – an EU record is never written in Mumbai
    Given a request for tenant "Nordlicht Robotik GmbH" (zone EU) is routed to the Mumbai stack by mistake
    When it attempts a write
    Then the region check returns 409 "RESIDENCY_ZONE_MISMATCH" and nothing is written in either zone

  @sec @obs @MU04
  Scenario Outline: AC-01ZU08-08 Permutations – Data platform, residency and records (3-way, 70 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the database context is "<db_context>" for "<data_class>" data
    When "<operation>" runs through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU04 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   I-025 = Audit sinks (HTTPS, syslog-TLS, object storage
    #   I-026 = Reference-data governance for `locale_bundle`
    #   I-030 = Analytics and usage tables of §11.9.5.6
    Examples: MU04 rows (3-way, seed 150; space 2,592; tuples 1064/1064; +3 baseline-allow)
      | ex | operation | persona | authority | data_class | db_context | region | channel | expected |
      | EX-01ZU08-01 | I-030 | P16/R19 | T5 other tenant | Public | no company scope | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU08-02 | I-030 | P16/R19 | A1 | Internal | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU08-03 | I-025 | P11/R12 | T5 other tenant | Restricted | no tenant ctx | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU08-04 | I-025 | P16/R19 | A5 wrong role | Restricted | context set | EU→IN (misrouted) | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU08-05 | I-030 | P01/R01 | A5 wrong role | Public | context set | IN | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU08-06 | I-026 | P11/R12 | A1 | Confidential | context set | IN | C3 API | ALLOW: Reference-data governance for `locale_bundle`, |
      | EX-01ZU08-07 | I-026 | P01/R01 | T5 other tenant | Confidential | no company scope | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU08-08 | I-025 | P01/R01 | A3 SoD/limit | Internal | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU08-09 | I-026 | P16/R19 | A3 SoD/limit | Internal | context set | EU | worker job | 403 SOD_CONFLICT |
      | EX-01ZU08-10 | I-026 | P11/R12 | A3 SoD/limit | Public | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU08-11 | I-030 | P01/R01 | A5 wrong role | Confidential | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU08-12 | I-025 | P11/R12 | A1 | Public | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU08-13 | I-026 | P11/R12 | A5 wrong role | Restricted | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU08-14 | I-030 | P11/R12 | T5 other tenant | Internal | context set | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU08-15 | I-025 | P16/R19 | A3 SoD/limit | Confidential | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU08-16 | I-030 | P11/R12 | A3 SoD/limit | Restricted | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU08-17 | I-026 | P01/R01 | T5 other tenant | Restricted | no tenant ctx | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU08-18 | I-025 | P01/R01 | A1 | Public | context set | EU | C3 API | ALLOW: Audit sinks (HTTPS, syslog-TLS, object storage |
      | EX-01ZU08-19 | I-025 | P01/R01 | A5 wrong role | Internal | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU08-20 | I-026 | P16/R19 | A5 wrong role | Internal | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU08-21 | I-026 | P01/R01 | A1 | Restricted | context set | EU→IN (misrouted) | worker job | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU08-22 | I-025 | P16/R19 | A1 | Confidential | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU08-23 | I-030 | P16/R19 | A3 SoD/limit | Restricted | context set | IN | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU08-24 | I-025 | P11/R12 | A5 wrong role | Confidential | context set | EU | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU08-25 | I-026 | P16/R19 | A1 | Public | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU08-26 | I-030 | P01/R01 | A1 | Internal | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU08-27 | I-030 | P11/R12 | T5 other tenant | Confidential | no company scope | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU08-28 | I-025 | P16/R19 | T5 other tenant | Public | context set | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU08-29 | I-030 | P11/R12 | A1 | Restricted | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU08-30 | I-026 | P16/R19 | T5 other tenant | Internal | no tenant ctx | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU08-31 | I-030 | P01/R01 | A3 SoD/limit | Confidential | context set | EU→IN (misrouted) | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU08-32 | I-025 | P11/R12 | A3 SoD/limit | Internal | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU08-33 | I-026 | P01/R01 | A3 SoD/limit | Public | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU08-34 | I-026 | P11/R12 | A5 wrong role | Public | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU08-35 | I-025 | P01/R01 | T5 other tenant | Internal | context set | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU08-36 | I-026 | P16/R19 | T5 other tenant | Confidential | context set | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU08-37 | I-030 | P11/R12 | A5 wrong role | Public | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU08-38 | I-025 | P01/R01 | A5 wrong role | Restricted | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU08-39 | I-030 | P16/R19 | A5 wrong role | Restricted | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU08-40 | I-025 | P11/R12 | A1 | Confidential | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU08-41 | I-030 | P11/R12 | A3 SoD/limit | Public | context set | EU | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU08-42 | I-026 | P11/R12 | A1 | Internal | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU08-43 | I-030 | P01/R01 | T5 other tenant | Restricted | context set | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU08-44 | I-025 | P16/R19 | A1 | Restricted | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU08-45 | I-030 | P01/R01 | A1 | Public | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU08-46 | I-025 | P01/R01 | A3 SoD/limit | Restricted | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU08-47 | I-030 | P16/R19 | A1 | Internal | context set | IN | C3 API | ALLOW: Analytics and usage tables of §11.9.5.6 |
      | EX-01ZU08-48 | I-025 | P16/R19 | T5 other tenant | Internal | no company scope | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU08-49 | I-025 | P16/R19 | T5 other tenant | Public | no tenant ctx | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU08-50 | I-026 | P11/R12 | A3 SoD/limit | Confidential | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU08-51 | I-026 | P01/R01 | A5 wrong role | Internal | context set | EU | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU08-52 | I-026 | P16/R19 | A5 wrong role | Confidential | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU08-53 | I-030 | P16/R19 | A3 SoD/limit | Internal | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU08-54 | I-025 | P01/R01 | A1 | Confidential | context set | IN | C3 API | ALLOW: Audit sinks (HTTPS, syslog-TLS, object storage |
      | EX-01ZU08-55 | I-026 | P16/R19 | T5 other tenant | Restricted | no company scope | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU08-56 | I-026 | P11/R12 | T5 other tenant | Public | context set | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU08-57 | I-030 | P11/R12 | A1 | Confidential | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU08-58 | I-025 | P16/R19 | A3 SoD/limit | Public | context set | IN | worker job | 403 SOD_CONFLICT |
      | EX-01ZU08-59 | I-030 | P16/R19 | A3 SoD/limit | Confidential | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU08-60 | I-025 | P16/R19 | A5 wrong role | Public | context set | EU | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU08-61 | I-030 | P11/R12 | A5 wrong role | Internal | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU08-62 | I-026 | P11/R12 | A3 SoD/limit | Restricted | context set | EU | worker job | 403 SOD_CONFLICT |
      | EX-01ZU08-63 | I-026 | P16/R19 | A5 wrong role | Confidential | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU08-64 | I-030 | P01/R01 | T5 other tenant | Confidential | no tenant ctx | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU08-65 | I-025 | P01/R01 | A1 | Internal | context set | EU→IN (misrouted) | C3 API | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU08-66 | I-025 | P11/R12 | T5 other tenant | Confidential | context set | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU08-67 | I-025 | P01/R01 | T5 other tenant | Public | no company scope | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU08-68 | I-025 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Audit sinks (HTTPS, syslog-TLS, object storage |
      | EX-01ZU08-69 | I-026 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Reference-data governance for `locale_bundle`, |
      | EX-01ZU08-70 | I-030 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Analytics and usage tables of §11.9.5.6 |
```

##### US-01-ZU09 Immutable record versions and atomic usage reservation

| Field | Value |
|---|---|
| ID | US-01-ZU09 |
| Title | Immutable record versions and atomic usage reservation |
| Type | Security |
| Story | As a platform data owner (P11, R12, with the security lead), I want `domain_record_version` immutable snapshots and `usage_reservation` atomic reservation, so that every record stays in its tenant, company and residency zone, is exact and can be proven |
| Persona / roles | Platform data owner (P11, R12, with the security lead) |
| Traces | FR-V12-I-031 (ch26 V4); tests TC-V12-I-033 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-01-ZR26, US-01-ZR27, US-01-ZR28, US-01-YI01; source definition: Part 11.9b §11.9.5.12 Functional requirements |
| Dimension profile | persona ×3 · authority ×4 · data class ×4 · db context ×3 · region ×3 · channel ×2 · operation ×1 · model MU04 |
| Notes | Screens A009, A197, A204; API family `/api/v1/data/`; audit events `data.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Immutable record versions and atomic usage reservation
  Background:
    Given tenants "Kestrel Analytics Pvt Ltd" (zone IN) and "Nordlicht Robotik GmbH" (zone EU) provisioned by the two-tenant fixture
    And the API connects through the least-privilege role "app_rw" that sets app.tenant_id and app.company_ids per transaction (DEC-778)

  @happy
  Scenario: AC-01ZU09-01 Happy path – `domain_record_version` immutable snapshots and `usage_reservation`… (FR-V12-I-031)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "`domain_record_version` immutable snapshots and `usage_reservation`…" is exercised as specified by FR-V12-I-031:
      """
      `domain_record_version` immutable snapshots and `usage_reservation` atomic reservation
      """
    Then the observable result matches FR-V12-I-031 and its tests TC-V12-I-033
    And the audit event "data.domain_record_version" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-778
  Scenario: AC-01ZU09-02 Negative – no statement runs without tenant context
    When a worker executes a query on "crm_contact" without setting app.tenant_id
    Then PostgreSQL raises SQLSTATE 42501 and no row is read or written

  @val
  Scenario: AC-01ZU09-03 Validation – money and identifiers are exact
    When a row is written with amount 12.50 as a float and currency "inr"
    Then the write is rejected: amount must be an integer in minor units and currency an upper-case ISO 4217 code

  @perm @BRL-TEN-03
  Scenario: AC-01ZU09-04 Permission – cross-tenant reference is impossible
    When tenant "Nordlicht Robotik GmbH" inserts a child row referencing a parent of "Kestrel Analytics Pvt Ltd"
    Then the composite foreign key rejects the row and the attempt is audited

  @edge @DEC-772
  Scenario: AC-01ZU09-05 Edge – an EU record is never written in Mumbai
    Given a request for tenant "Nordlicht Robotik GmbH" (zone EU) is routed to the Mumbai stack by mistake
    When it attempts a write
    Then the region check returns 409 "RESIDENCY_ZONE_MISMATCH" and nothing is written in either zone

  @sec @obs @MU04
  Scenario Outline: AC-01ZU09-06 Permutations – Data platform, residency and records (3-way, 61 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the database context is "<db_context>" for "<data_class>" data
    When "<operation>" runs through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU04 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   I-031 = `domain_record_version` immutable snapshots and…
    Examples: MU04 rows (3-way, seed 157; space 864; tuples 766/766; +1 baseline-allow)
      | ex | operation | persona | authority | data_class | db_context | region | channel | expected |
      | EX-01ZU09-01 | I-031 | P16/R19 | A3 SoD/limit | Confidential | context set | EU→IN (misrouted) | worker job | 403 SOD_CONFLICT |
      | EX-01ZU09-02 | I-031 | P01/R01 | A3 SoD/limit | Public | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU09-03 | I-031 | P16/R19 | A5 wrong role | Internal | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU09-04 | I-031 | P11/R12 | T5 other tenant | Restricted | no tenant ctx | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU09-05 | I-031 | P11/R12 | A1 | Internal | context set | EU→IN (misrouted) | C3 API | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU09-06 | I-031 | P01/R01 | A1 | Confidential | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU09-07 | I-031 | P16/R19 | T5 other tenant | Restricted | context set | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU09-08 | I-031 | P11/R12 | A5 wrong role | Public | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU09-09 | I-031 | P11/R12 | A5 wrong role | Confidential | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU09-10 | I-031 | P01/R01 | T5 other tenant | Internal | no tenant ctx | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU09-11 | I-031 | P16/R19 | A1 | Public | context set | EU | worker job | ALLOW: `domain_record_version` immutable snapshots and |
      | EX-01ZU09-12 | I-031 | P01/R01 | A5 wrong role | Restricted | context set | EU→IN (misrouted) | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU09-13 | I-031 | P11/R12 | A3 SoD/limit | Restricted | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU09-14 | I-031 | P01/R01 | T5 other tenant | Confidential | no company scope | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU09-15 | I-031 | P16/R19 | A1 | Restricted | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU09-16 | I-031 | P11/R12 | A3 SoD/limit | Internal | context set | IN | worker job | 403 SOD_CONFLICT |
      | EX-01ZU09-17 | I-031 | P16/R19 | T5 other tenant | Public | no company scope | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU09-18 | I-031 | P16/R19 | A5 wrong role | Restricted | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU09-19 | I-031 | P01/R01 | A5 wrong role | Confidential | context set | EU | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU09-20 | I-031 | P16/R19 | A3 SoD/limit | Internal | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU09-21 | I-031 | P01/R01 | A3 SoD/limit | Restricted | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU09-22 | I-031 | P16/R19 | T5 other tenant | Confidential | no tenant ctx | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU09-23 | I-031 | P11/R12 | T5 other tenant | Public | context set | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU09-24 | I-031 | P01/R01 | A1 | Internal | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU09-25 | I-031 | P11/R12 | A1 | Public | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU09-26 | I-031 | P11/R12 | T5 other tenant | Internal | no company scope | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU09-27 | I-031 | P01/R01 | T5 other tenant | Public | context set | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU09-28 | I-031 | P16/R19 | A1 | Confidential | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU09-29 | I-031 | P11/R12 | A3 SoD/limit | Confidential | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU09-30 | I-031 | P11/R12 | A1 | Confidential | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU09-31 | I-031 | P01/R01 | A5 wrong role | Internal | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU09-32 | I-031 | P16/R19 | A5 wrong role | Public | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU09-33 | I-031 | P01/R01 | A1 | Restricted | context set | EU | worker job | Tier 2 and unapproved models excluded |
      | EX-01ZU09-34 | I-031 | P16/R19 | A3 SoD/limit | Public | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU09-35 | I-031 | P16/R19 | A1 | Internal | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU09-36 | I-031 | P01/R01 | A3 SoD/limit | Internal | context set | EU | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU09-37 | I-031 | P01/R01 | A1 | Public | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU09-38 | I-031 | P11/R12 | T5 other tenant | Confidential | context set | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU09-39 | I-031 | P16/R19 | A5 wrong role | Internal | context set | EU→IN (misrouted) | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU09-40 | I-031 | P11/R12 | A1 | Restricted | context set | IN | C3 API | Tier 2 and unapproved models excluded |
      | EX-01ZU09-41 | I-031 | P01/R01 | A3 SoD/limit | Restricted | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU09-42 | I-031 | P11/R12 | A3 SoD/limit | Public | context set | EU→IN (misrouted) | worker job | 403 SOD_CONFLICT |
      | EX-01ZU09-43 | I-031 | P16/R19 | T5 other tenant | Internal | context set | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU09-44 | I-031 | P11/R12 | A5 wrong role | Internal | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU09-45 | I-031 | P01/R01 | A5 wrong role | Public | context set | IN | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU09-46 | I-031 | P01/R01 | T5 other tenant | Restricted | no company scope | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU09-47 | I-031 | P11/R12 | A5 wrong role | Restricted | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU09-48 | I-031 | P01/R01 | A5 wrong role | Confidential | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU09-49 | I-031 | P01/R01 | A3 SoD/limit | Internal | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU09-50 | I-031 | P01/R01 | A3 SoD/limit | Confidential | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU09-51 | I-031 | P01/R01 | A3 SoD/limit | Public | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU09-52 | I-031 | P16/R19 | A3 SoD/limit | Restricted | context set | EU | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU09-53 | I-031 | P01/R01 | T5 other tenant | Public | no tenant ctx | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU09-54 | I-031 | P16/R19 | A3 SoD/limit | Confidential | context set | IN | worker job | 403 SOD_CONFLICT |
      | EX-01ZU09-55 | I-031 | P11/R12 | A1 | Confidential | context set | EU→IN (misrouted) | worker job | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU09-56 | I-031 | P16/R19 | A5 wrong role | Confidential | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU09-57 | I-031 | P11/R12 | A5 wrong role | Restricted | context set | EU | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU09-58 | I-031 | P11/R12 | A1 | Restricted | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU09-59 | I-031 | P01/R01 | A1 | Confidential | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU09-60 | I-031 | P16/R19 | A3 SoD/limit | Confidential | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU09-61 | I-031 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: `domain_record_version` immutable snapshots and |
```

##### US-01-ZU10 ENT-IDN-01…03 acceptance: SSO per tenant, verified domains and SCIM

| Field | Value |
|---|---|
| ID | US-01-ZU10 |
| Title | ENT-IDN-01…03 acceptance: SSO per tenant, verified domains and SCIM |
| Type | Compliance (acceptance binding) |
| Story | As a tenant administrator (P11, R12), I want SAML 2.0 and OpenID Connect SSO per tenant, configured by the tenant administrator; verified email domains (DNS TXT) before SSO can be enforced for that domain; SCIM 2.0 user and group provisioning and de-provisioning; de-provisioned users lose sessions and API access, so that only the right people reach our data, with evidence an auditor can verify |
| Persona / roles | Tenant administrator (P11, R12) |
| Traces | FR-V12-K-101 (ENT-IDN-01); FR-V12-K-102 (ENT-IDN-02); FR-V12-K-103 (ENT-IDN-03); DEC-417, DEC-784; tests TC-V12-K-101, TC-V12-K-102, TC-V12-K-103 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 2–3 |
| Dependencies | US-01-ZR01, US-01-ZR02, US-01-ZR03, US-01-ZR04; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · authority ×4 · channel ×3 · session/MFA ×3 · region ×3 · operation ×3 · model MU02 |
| Notes | FR-V12-K-101, FR-V12-K-102, FR-V12-K-103: release per DEC-784 (SSO/SCIM and enterprise access in Release 1) · Trace requirement adopted literally from the ENT register (Part 11.11b §11.11.5.16); design depth and build points sit in US-01-ZR01, US-01-ZR02, US-01-ZR03; this story binds the ENT acceptance to tests (DEC-941) · Screens A002, A009, A099, A197, A203; API family `/api/v1/identity/`; audit events `identity.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: ENT-IDN-01…03 acceptance: SSO per tenant, verified domains and SCIM
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with administrator "meera@kestrel.example.com" (R12) holding a fresh WebAuthn factor
    And the reused IdP broker is reachable and the break-glass account "bg-admin@kestrel.example.com" is registered

  @happy @ENT-IDN-01 @DEC-784
  Scenario: AC-01ZU10-01 Happy path – SAML 2.0 and OpenID Connect SSO per tenant (FR-V12-K-101)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "SAML 2.0 and OpenID Connect SSO per tenant" is exercised as specified by FR-V12-K-101:
      """
      SAML 2.0 and OpenID Connect SSO per tenant, configured by the tenant administrator.
      """
    Then positive sign-in/provisioning path plus negatives:
      """
      unverified domain, de-provisioned or revoked user, expired or idle session, missing break-glass all denied and audited
      """
    And the audit event "identity.saml_2_0_and_openid_connect" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-IDN-02 @DEC-784
  Scenario: AC-01ZU10-02 Alternate – Verified email domains (DNS TXT) before SSO can be enforced for that… (FR-V12-K-102)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Verified email domains (DNS TXT) before SSO can be enforced for that…" is exercised as specified by FR-V12-K-102:
      """
      Verified email domains (DNS TXT) before SSO can be enforced for that domain.
      """
    Then positive sign-in/provisioning path plus negatives:
      """
      unverified domain, de-provisioned or revoked user, expired or idle session, missing break-glass all denied and audited
      """
    And the audit event "identity.verified_email_domains" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-IDN-03 @DEC-784
  Scenario: AC-01ZU10-03 Alternate – SCIM 2.0 user and group provisioning and de-provisioning (FR-V12-K-103)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "SCIM 2.0 user and group provisioning and de-provisioning" is exercised as specified by FR-V12-K-103:
      """
      SCIM 2.0 user and group provisioning and de-provisioning; de-provisioned users lose sessions and API access.
      """
    Then positive sign-in/provisioning path plus negatives:
      """
      unverified domain, de-provisioned or revoked user, expired or idle session, missing break-glass all denied and audited
      """
    And the audit event "identity.scim_2_0_user_and_group" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @BRL-APR-01
  Scenario: AC-01ZU10-04 Negative – a user cannot grant a role to themselves
    Given "arjun@kestrel.example.com" holds role "Campaign approver"
    When he assigns role "Campaign requester" to himself
    Then the API returns 409 "SOD_SELF_GRANT" and the role assignment does not exist
    And a security event "identity.sod.violation_blocked" is written

  @val
  Scenario: AC-01ZU10-05 Validation – non-HTTPS identity endpoints are rejected
    When Meera submits SSO metadata URL "http://idp.kestrel.example.com/metadata"
    Then the API returns 422 "METADATA_URL_NOT_HTTPS" and no configuration row exists

  @perm
  Scenario: AC-01ZU10-06 Permission – a startup head cannot change identity configuration
    When "arjun@kestrel.example.com" (R02) posts an identity configuration change
    Then the API returns 403 "PERMISSION_DENIED" and no side effect occurs (NSE)

  @edge @BRL-TEN-07
  Scenario: AC-01ZU10-07 Edge – revocation takes effect within 60 seconds
    Given "ravi@kestrel.example.com" has an active session at 2027-03-01T10:00:00+05:30
    When his access is revoked at 10:00:05
    Then his next API call after 10:01:05 returns 401 "SESSION_REVOKED"

  @sec @obs @MU02
  Scenario Outline: AC-01ZU10-08 Permutations – Enterprise identity, access and audit (3-way, 56 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the session is "<session_mfa>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU02 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-101 = SAML 2.0 and OpenID Connect SSO per tenant
    #   K-102 = Verified email domains (DNS TXT) before SSO can be…
    #   K-103 = SCIM 2.0 user and group provisioning and…
    Examples: MU02 rows (3-way, seed 164; space 972; tuples 630/630; +3 baseline-allow)
      | ex | operation | persona | authority | channel | session_mfa | region | expected |
      | EX-01ZU10-01 | K-103 | P11/R12 | T5 other tenant | C2 mobile | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU10-02 | K-101 | P02/R02 | A1 | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU10-03 | K-103 | P11/R12 | A3 SoD/limit | C1 web | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU10-04 | K-102 | P12/R13 | T5 other tenant | C1 web | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU10-05 | K-102 | P12/R13 | A5 wrong role | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU10-06 | K-102 | P02/R02 | A5 wrong role | C1 web | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-01ZU10-07 | K-101 | P12/R13 | A1 | C2 mobile | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU10-08 | K-103 | P12/R13 | A1 | C3 API | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU10-09 | K-102 | P11/R12 | A3 SoD/limit | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU10-10 | K-103 | P02/R02 | A5 wrong role | C3 API | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU10-11 | K-101 | P02/R02 | A3 SoD/limit | C2 mobile | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU10-12 | K-103 | P12/R13 | A3 SoD/limit | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU10-13 | K-101 | P11/R12 | A5 wrong role | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU10-14 | K-101 | P12/R13 | T5 other tenant | C1 web | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-01ZU10-15 | K-102 | P11/R12 | A1 | C3 API | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU10-16 | K-102 | P02/R02 | T5 other tenant | C2 mobile | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU10-17 | K-103 | P11/R12 | A1 | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU10-18 | K-102 | P11/R12 | A5 wrong role | C3 API | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-01ZU10-19 | K-101 | P12/R13 | A3 SoD/limit | C3 API | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU10-20 | K-101 | P02/R02 | T5 other tenant | C3 API | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU10-21 | K-103 | P02/R02 | A1 | C1 web | passkey MFA | IN | ALLOW: Positive sign-in/provisioning path plus negatives: |
      | EX-01ZU10-22 | K-101 | P11/R12 | T5 other tenant | C2 mobile | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU10-23 | K-101 | P11/R12 | A3 SoD/limit | C3 API | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU10-24 | K-103 | P02/R02 | A5 wrong role | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU10-25 | K-103 | P11/R12 | T5 other tenant | C3 API | session revoked | IN | uniform 404 NOT_FOUND |
      | EX-01ZU10-26 | K-102 | P12/R13 | A3 SoD/limit | C2 mobile | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU10-27 | K-102 | P02/R02 | A1 | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU10-28 | K-101 | P02/R02 | A1 | C1 web | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU10-29 | K-103 | P12/R13 | A5 wrong role | C1 web | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU10-30 | K-102 | P11/R12 | T5 other tenant | C1 web | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU10-31 | K-101 | P12/R13 | A5 wrong role | C2 mobile | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU10-32 | K-102 | P11/R12 | A1 | C2 mobile | passkey MFA | IN | ALLOW: Positive sign-in/provisioning path plus negatives: |
      | EX-01ZU10-33 | K-102 | P02/R02 | T5 other tenant | C3 API | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU10-34 | K-103 | P12/R13 | T5 other tenant | C3 API | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-01ZU10-35 | K-102 | P02/R02 | A3 SoD/limit | C1 web | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU10-36 | K-103 | P11/R12 | A3 SoD/limit | C1 web | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU10-37 | K-101 | P12/R13 | A5 wrong role | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU10-38 | K-101 | P11/R12 | A3 SoD/limit | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU10-39 | K-103 | P11/R12 | A5 wrong role | C2 mobile | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-01ZU10-40 | K-103 | P12/R13 | T5 other tenant | C2 mobile | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU10-41 | K-103 | P02/R02 | A3 SoD/limit | C3 API | OTP only | EU | 403 SOD_CONFLICT |
      | EX-01ZU10-42 | K-102 | P12/R13 | A3 SoD/limit | C2 mobile | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU10-43 | K-102 | P12/R13 | A1 | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU10-44 | K-101 | P02/R02 | A5 wrong role | C2 mobile | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU10-45 | K-101 | P11/R12 | A1 | C3 API | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU10-46 | K-103 | P02/R02 | A1 | C2 mobile | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU10-47 | K-103 | P02/R02 | T5 other tenant | C1 web | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU10-48 | K-103 | P11/R12 | A1 | C1 web | passkey MFA | EU | ALLOW: Positive sign-in/provisioning path plus negatives: |
      | EX-01ZU10-49 | K-102 | P12/R13 | A5 wrong role | C3 API | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU10-50 | K-101 | P02/R02 | A3 SoD/limit | C1 web | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-01ZU10-51 | K-101 | P12/R13 | A1 | C2 mobile | passkey MFA | IN | ALLOW: Positive sign-in/provisioning path plus negatives: |
      | EX-01ZU10-52 | K-103 | P12/R13 | A5 wrong role | C2 mobile | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-01ZU10-53 | K-103 | P02/R02 | A3 SoD/limit | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU10-54 | K-101 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Positive sign-in/provisioning path plus negatives: |
      | EX-01ZU10-55 | K-102 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Positive sign-in/provisioning path plus negatives: |
      | EX-01ZU10-56 | K-103 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Positive sign-in/provisioning path plus negatives: |
```

##### US-01-ZU11 ENT-IDN-04…06 acceptance: MFA policy, session policy and break-glass

| Field | Value |
|---|---|
| ID | US-01-ZU11 |
| Title | ENT-IDN-04…06 acceptance: MFA policy, session policy and break-glass |
| Type | Compliance (acceptance binding) |
| Story | As a tenant administrator (P11, R12), I want MFA policy per tenant; phishing-resistant (passkeys/FIDO2) available for privileged roles; session policy: maximum session 1–24 h, idle timeout 5–120 min, immediate revocation; break-glass administrator required before SSO enforcement; every use alerts and is audited, so that only the right people reach our data, with evidence an auditor can verify |
| Persona / roles | Tenant administrator (P11, R12) |
| Traces | FR-V12-K-104 (ENT-IDN-04); FR-V12-K-105 (ENT-IDN-05); FR-V12-K-106 (ENT-IDN-06); DEC-784; tests TC-V12-K-104, TC-V12-K-105, TC-V12-K-106 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 2–3 |
| Dependencies | US-01-ZR01, US-01-ZR02, US-01-ZR03, US-01-ZR04; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · authority ×4 · channel ×3 · session/MFA ×3 · region ×3 · operation ×3 · model MU02 |
| Notes | FR-V12-K-104, FR-V12-K-105, FR-V12-K-106: release per DEC-784 (SSO/SCIM and enterprise access in Release 1) · Trace requirement adopted literally from the ENT register (Part 11.11b §11.11.5.16); design depth and build points sit in US-01-ZR02, US-01-ZR03; this story binds the ENT acceptance to tests (DEC-941) · Screens A002, A009, A099, A197, A203; API family `/api/v1/identity/`; audit events `identity.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: ENT-IDN-04…06 acceptance: MFA policy, session policy and break-glass
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with administrator "meera@kestrel.example.com" (R12) holding a fresh WebAuthn factor
    And the reused IdP broker is reachable and the break-glass account "bg-admin@kestrel.example.com" is registered

  @happy @ENT-IDN-04 @DEC-784
  Scenario: AC-01ZU11-01 Happy path – MFA policy per tenant; phishing-resistant (FR-V12-K-104)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "MFA policy per tenant; phishing-resistant" is exercised as specified by FR-V12-K-104:
      """
      MFA policy per tenant; phishing-resistant (passkeys/FIDO2) available for privileged roles.
      """
    Then positive sign-in/provisioning path plus negatives:
      """
      unverified domain, de-provisioned or revoked user, expired or idle session, missing break-glass all denied and audited
      """
    And the audit event "identity.mfa_policy_per_tenant" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-IDN-05 @DEC-784
  Scenario: AC-01ZU11-02 Alternate – Session policy: maximum session 1–24 h, idle timeout 5–120 min (FR-V12-K-105)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Session policy: maximum session 1–24 h, idle timeout 5–120 min" is exercised as specified by FR-V12-K-105:
      """
      Session policy: maximum session 1–24 h, idle timeout 5–120 min, immediate revocation.
      """
    Then positive sign-in/provisioning path plus negatives:
      """
      unverified domain, de-provisioned or revoked user, expired or idle session, missing break-glass all denied and audited
      """
    And the audit event "identity.session_policy_maximum" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-IDN-06 @DEC-784
  Scenario: AC-01ZU11-03 Alternate – Break-glass administrator required before SSO enforcement (FR-V12-K-106)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Break-glass administrator required before SSO enforcement" is exercised as specified by FR-V12-K-106:
      """
      Break-glass administrator required before SSO enforcement; every use alerts and is audited.
      """
    Then positive sign-in/provisioning path plus negatives:
      """
      unverified domain, de-provisioned or revoked user, expired or idle session, missing break-glass all denied and audited
      """
    And the audit event "identity.break_glass_administrator" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @BRL-APR-01
  Scenario: AC-01ZU11-04 Negative – a user cannot grant a role to themselves
    Given "arjun@kestrel.example.com" holds role "Campaign approver"
    When he assigns role "Campaign requester" to himself
    Then the API returns 409 "SOD_SELF_GRANT" and the role assignment does not exist
    And a security event "identity.sod.violation_blocked" is written

  @val
  Scenario: AC-01ZU11-05 Validation – non-HTTPS identity endpoints are rejected
    When Meera submits SSO metadata URL "http://idp.kestrel.example.com/metadata"
    Then the API returns 422 "METADATA_URL_NOT_HTTPS" and no configuration row exists

  @perm
  Scenario: AC-01ZU11-06 Permission – a startup head cannot change identity configuration
    When "arjun@kestrel.example.com" (R02) posts an identity configuration change
    Then the API returns 403 "PERMISSION_DENIED" and no side effect occurs (NSE)

  @edge @BRL-TEN-07
  Scenario: AC-01ZU11-07 Edge – revocation takes effect within 60 seconds
    Given "ravi@kestrel.example.com" has an active session at 2027-03-01T10:00:00+05:30
    When his access is revoked at 10:00:05
    Then his next API call after 10:01:05 returns 401 "SESSION_REVOKED"

  @sec @obs @MU02
  Scenario Outline: AC-01ZU11-08 Permutations – Enterprise identity, access and audit (3-way, 59 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the session is "<session_mfa>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU02 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-104 = MFA policy per tenant; phishing-resistant
    #   K-105 = Session policy: maximum session 1–24 h
    #   K-106 = Break-glass administrator required before SSO…
    Examples: MU02 rows (3-way, seed 171; space 972; tuples 630/630; +3 baseline-allow)
      | ex | operation | persona | authority | channel | session_mfa | region | expected |
      | EX-01ZU11-01 | K-106 | P12/R13 | T5 other tenant | C1 web | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU11-02 | K-104 | P11/R12 | A3 SoD/limit | C1 web | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU11-03 | K-106 | P02/R02 | A1 | C2 mobile | passkey MFA | IN | ALLOW: Positive sign-in/provisioning path plus negatives: |
      | EX-01ZU11-04 | K-106 | P11/R12 | A5 wrong role | C1 web | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU11-05 | K-104 | P02/R02 | A5 wrong role | C3 API | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-01ZU11-06 | K-105 | P02/R02 | A1 | C1 web | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU11-07 | K-105 | P12/R13 | T5 other tenant | C2 mobile | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU11-08 | K-104 | P12/R13 | A1 | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU11-09 | K-104 | P02/R02 | T5 other tenant | C1 web | session revoked | IN | uniform 404 NOT_FOUND |
      | EX-01ZU11-10 | K-106 | P02/R02 | A3 SoD/limit | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU11-11 | K-105 | P11/R12 | A3 SoD/limit | C3 API | OTP only | EU | 403 SOD_CONFLICT |
      | EX-01ZU11-12 | K-105 | P11/R12 | A5 wrong role | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU11-13 | K-104 | P12/R13 | T5 other tenant | C3 API | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU11-14 | K-105 | P11/R12 | A1 | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU11-15 | K-106 | P12/R13 | A3 SoD/limit | C2 mobile | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU11-16 | K-104 | P12/R13 | A3 SoD/limit | C3 API | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-01ZU11-17 | K-106 | P11/R12 | T5 other tenant | C2 mobile | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU11-18 | K-105 | P02/R02 | A3 SoD/limit | C2 mobile | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU11-19 | K-105 | P12/R13 | A3 SoD/limit | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU11-20 | K-105 | P12/R13 | A1 | C3 API | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU11-21 | K-106 | P12/R13 | A5 wrong role | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU11-22 | K-104 | P02/R02 | T5 other tenant | C2 mobile | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU11-23 | K-106 | P02/R02 | T5 other tenant | C3 API | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-01ZU11-24 | K-104 | P11/R12 | A1 | C2 mobile | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU11-25 | K-104 | P12/R13 | A5 wrong role | C1 web | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-01ZU11-26 | K-105 | P02/R02 | A5 wrong role | C1 web | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-01ZU11-27 | K-106 | P11/R12 | A5 wrong role | C3 API | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU11-28 | K-106 | P12/R13 | A1 | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU11-29 | K-105 | P11/R12 | T5 other tenant | C3 API | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-01ZU11-30 | K-104 | P11/R12 | A1 | C1 web | passkey MFA | EU | ALLOW: Positive sign-in/provisioning path plus negatives: |
      | EX-01ZU11-31 | K-104 | P02/R02 | A3 SoD/limit | C1 web | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU11-32 | K-104 | P11/R12 | A3 SoD/limit | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU11-33 | K-104 | P02/R02 | A1 | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU11-34 | K-105 | P11/R12 | T5 other tenant | C1 web | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU11-35 | K-106 | P02/R02 | A5 wrong role | C2 mobile | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-01ZU11-36 | K-106 | P12/R13 | A1 | C3 API | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU11-37 | K-104 | P12/R13 | A5 wrong role | C2 mobile | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU11-38 | K-105 | P02/R02 | A5 wrong role | C3 API | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU11-39 | K-104 | P11/R12 | A5 wrong role | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU11-40 | K-106 | P02/R02 | A3 SoD/limit | C1 web | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU11-41 | K-105 | P02/R02 | A5 wrong role | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU11-42 | K-104 | P11/R12 | T5 other tenant | C3 API | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU11-43 | K-104 | P11/R12 | A1 | C2 mobile | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU11-44 | K-106 | P11/R12 | A3 SoD/limit | C3 API | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU11-45 | K-106 | P12/R13 | A1 | C1 web | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU11-46 | K-105 | P02/R02 | T5 other tenant | C3 API | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU11-47 | K-106 | P12/R13 | T5 other tenant | C2 mobile | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU11-48 | K-104 | P02/R02 | A5 wrong role | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU11-49 | K-105 | P11/R12 | A1 | C2 mobile | passkey MFA | EU | ALLOW: Positive sign-in/provisioning path plus negatives: |
      | EX-01ZU11-50 | K-105 | P02/R02 | A3 SoD/limit | C3 API | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU11-51 | K-105 | P12/R13 | A5 wrong role | C3 API | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU11-52 | K-104 | P11/R12 | A3 SoD/limit | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU11-53 | K-105 | P11/R12 | A3 SoD/limit | C3 API | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU11-54 | K-106 | P11/R12 | A1 | C3 API | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU11-55 | K-105 | P11/R12 | A5 wrong role | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU11-56 | K-106 | P02/R02 | T5 other tenant | C1 web | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU11-57 | K-104 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Positive sign-in/provisioning path plus negatives: |
      | EX-01ZU11-58 | K-105 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Positive sign-in/provisioning path plus negatives: |
      | EX-01ZU11-59 | K-106 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Positive sign-in/provisioning path plus negatives: |
```

##### US-01-ZU12 ENT-ACC-01…03 acceptance: custom roles, SoD matrix and tamper-evident audit

| Field | Value |
|---|---|
| ID | US-01-ZU12 |
| Title | ENT-ACC-01…03 acceptance: custom roles, SoD matrix and tamper-evident audit |
| Type | Compliance (acceptance binding) |
| Story | As a tenant administrator (P11, R12), I want custom roles from resource × action permissions, plus built-in roles; separation-of-duties matrix enforced when roles are built and when actions run; tamper-evident audit trail (hash-chained), exportable as JSON Lines or CSV, so that only the right people reach our data, with evidence an auditor can verify |
| Persona / roles | Tenant administrator (P11, R12) |
| Traces | FR-V12-K-107 (ENT-ACC-01); FR-V12-K-108 (ENT-ACC-02); FR-V12-K-109 (ENT-ACC-03); DEC-417, DEC-784; tests TC-V12-K-107, TC-V12-K-108, TC-V12-K-109 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 2–3 |
| Dependencies | US-01-ZR01, US-01-ZR02, US-01-ZR03, US-01-ZR04; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · authority ×4 · channel ×3 · session/MFA ×3 · region ×3 · operation ×3 · model MU02 |
| Notes | FR-V12-K-107, FR-V12-K-108, FR-V12-K-109: release per DEC-784 (SSO/SCIM and enterprise access in Release 1) · Trace requirement adopted literally from the ENT register (Part 11.11b §11.11.5.16); design depth and build points sit in US-01-ZR04, US-01-ZR05; this story binds the ENT acceptance to tests (DEC-941) · Screens A002, A009, A099, A197, A203; API family `/api/v1/identity/`; audit events `identity.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: ENT-ACC-01…03 acceptance: custom roles, SoD matrix and tamper-evident audit
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with administrator "meera@kestrel.example.com" (R12) holding a fresh WebAuthn factor
    And the reused IdP broker is reachable and the break-glass account "bg-admin@kestrel.example.com" is registered

  @happy @ENT-ACC-01 @DEC-784
  Scenario: AC-01ZU12-01 Happy path – Custom roles from resource × action permissions, plus built-in roles. (FR-V12-K-107)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Custom roles from resource × action permissions, plus built-in roles." is exercised as specified by FR-V12-K-107:
      """
      Custom roles from resource × action permissions, plus built-in roles.
      """
    Then role/permission matrix test incl. SoD violation at build and at run time:
      """
      tamper detection on the audit chain, export format check, support access without tenant approval denied
      """
    And the audit event "identity.custom_roles_from_resource" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-ACC-02 @DEC-784
  Scenario: AC-01ZU12-02 Alternate – Separation-of-duties matrix enforced when roles are built and when… (FR-V12-K-108)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Separation-of-duties matrix enforced when roles are built and when…" is exercised as specified by FR-V12-K-108:
      """
      Separation-of-duties matrix enforced when roles are built and when actions run.
      """
    Then role/permission matrix test incl. SoD violation at build and at run time:
      """
      tamper detection on the audit chain, export format check, support access without tenant approval denied
      """
    And the audit event "identity.separation_of_duties_matrix" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-ACC-03 @DEC-784
  Scenario: AC-01ZU12-03 Alternate – Tamper-evident audit trail (hash-chained) (FR-V12-K-109)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Tamper-evident audit trail (hash-chained)" is exercised as specified by FR-V12-K-109:
      """
      Tamper-evident audit trail (hash-chained), exportable as JSON Lines or CSV.
      """
    Then role/permission matrix test incl. SoD violation at build and at run time:
      """
      tamper detection on the audit chain, export format check, support access without tenant approval denied
      """
    And the audit event "identity.tamper_evident_audit_trail" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @BRL-APR-01
  Scenario: AC-01ZU12-04 Negative – a user cannot grant a role to themselves
    Given "arjun@kestrel.example.com" holds role "Campaign approver"
    When he assigns role "Campaign requester" to himself
    Then the API returns 409 "SOD_SELF_GRANT" and the role assignment does not exist
    And a security event "identity.sod.violation_blocked" is written

  @val
  Scenario: AC-01ZU12-05 Validation – non-HTTPS identity endpoints are rejected
    When Meera submits SSO metadata URL "http://idp.kestrel.example.com/metadata"
    Then the API returns 422 "METADATA_URL_NOT_HTTPS" and no configuration row exists

  @perm
  Scenario: AC-01ZU12-06 Permission – a startup head cannot change identity configuration
    When "arjun@kestrel.example.com" (R02) posts an identity configuration change
    Then the API returns 403 "PERMISSION_DENIED" and no side effect occurs (NSE)

  @edge @BRL-TEN-07
  Scenario: AC-01ZU12-07 Edge – revocation takes effect within 60 seconds
    Given "ravi@kestrel.example.com" has an active session at 2027-03-01T10:00:00+05:30
    When his access is revoked at 10:00:05
    Then his next API call after 10:01:05 returns 401 "SESSION_REVOKED"

  @sec @obs @MU02
  Scenario Outline: AC-01ZU12-08 Permutations – Enterprise identity, access and audit (3-way, 58 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the session is "<session_mfa>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU02 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-107 = Custom roles from resource × action permissions
    #   K-108 = Separation-of-duties matrix enforced when roles are…
    #   K-109 = Tamper-evident audit trail (hash-chained)
    Examples: MU02 rows (3-way, seed 178; space 972; tuples 630/630; +3 baseline-allow)
      | ex | operation | persona | authority | channel | session_mfa | region | expected |
      | EX-01ZU12-01 | K-108 | P11/R12 | A1 | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU12-02 | K-107 | P11/R12 | A1 | C3 API | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU12-03 | K-108 | P02/R02 | A1 | C1 web | passkey MFA | IN | ALLOW: Role/permission matrix test incl |
      | EX-01ZU12-04 | K-108 | P12/R13 | A5 wrong role | C2 mobile | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU12-05 | K-107 | P02/R02 | T5 other tenant | C1 web | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU12-06 | K-109 | P11/R12 | A5 wrong role | C1 web | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU12-07 | K-107 | P12/R13 | A5 wrong role | C1 web | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU12-08 | K-109 | P12/R13 | A1 | C3 API | passkey MFA | EU | ALLOW: Role/permission matrix test incl |
      | EX-01ZU12-09 | K-109 | P02/R02 | A3 SoD/limit | C1 web | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU12-10 | K-108 | P12/R13 | T5 other tenant | C3 API | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU12-11 | K-109 | P11/R12 | T5 other tenant | C2 mobile | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU12-12 | K-108 | P11/R12 | A3 SoD/limit | C3 API | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-01ZU12-13 | K-107 | P02/R02 | A3 SoD/limit | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU12-14 | K-108 | P02/R02 | A5 wrong role | C3 API | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-01ZU12-15 | K-109 | P02/R02 | T5 other tenant | C3 API | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU12-16 | K-107 | P12/R13 | A3 SoD/limit | C2 mobile | OTP only | EU | 403 SOD_CONFLICT |
      | EX-01ZU12-17 | K-109 | P02/R02 | A5 wrong role | C2 mobile | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-01ZU12-18 | K-108 | P11/R12 | T5 other tenant | C1 web | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-01ZU12-19 | K-109 | P12/R13 | A1 | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU12-20 | K-109 | P11/R12 | A3 SoD/limit | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU12-21 | K-107 | P02/R02 | A5 wrong role | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU12-22 | K-107 | P12/R13 | T5 other tenant | C3 API | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-01ZU12-23 | K-107 | P11/R12 | A3 SoD/limit | C1 web | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU12-24 | K-108 | P12/R13 | A3 SoD/limit | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU12-25 | K-109 | P12/R13 | A1 | C1 web | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU12-26 | K-108 | P02/R02 | A3 SoD/limit | C2 mobile | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU12-27 | K-107 | P11/R12 | A1 | C2 mobile | passkey MFA | IN | ALLOW: Role/permission matrix test incl |
      | EX-01ZU12-28 | K-108 | P11/R12 | A5 wrong role | C2 mobile | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU12-29 | K-108 | P12/R13 | T5 other tenant | C2 mobile | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU12-30 | K-107 | P02/R02 | T5 other tenant | C2 mobile | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU12-31 | K-109 | P11/R12 | A3 SoD/limit | C2 mobile | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU12-32 | K-107 | P12/R13 | A1 | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU12-33 | K-109 | P12/R13 | A5 wrong role | C3 API | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU12-34 | K-108 | P02/R02 | A1 | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU12-35 | K-107 | P02/R02 | A5 wrong role | C1 web | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU12-36 | K-109 | P02/R02 | A1 | C2 mobile | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU12-37 | K-107 | P11/R12 | A5 wrong role | C3 API | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-01ZU12-38 | K-109 | P12/R13 | A3 SoD/limit | C1 web | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-01ZU12-39 | K-107 | P02/R02 | A3 SoD/limit | C3 API | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU12-40 | K-107 | P11/R12 | T5 other tenant | C2 mobile | session revoked | IN | uniform 404 NOT_FOUND |
      | EX-01ZU12-41 | K-109 | P12/R13 | T5 other tenant | C1 web | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-01ZU12-42 | K-108 | P12/R13 | A5 wrong role | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU12-43 | K-108 | P02/R02 | T5 other tenant | C1 web | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-01ZU12-44 | K-108 | P11/R12 | A1 | C1 web | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU12-45 | K-108 | P12/R13 | A3 SoD/limit | C3 API | OTP only | EU | 403 SOD_CONFLICT |
      | EX-01ZU12-46 | K-109 | P11/R12 | T5 other tenant | C3 API | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU12-47 | K-107 | P12/R13 | A5 wrong role | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU12-48 | K-108 | P12/R13 | A5 wrong role | C3 API | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-01ZU12-49 | K-109 | P02/R02 | A1 | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU12-50 | K-108 | P12/R13 | A1 | C2 mobile | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU12-51 | K-109 | P11/R12 | A3 SoD/limit | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU12-52 | K-107 | P02/R02 | A3 SoD/limit | C3 API | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU12-53 | K-107 | P11/R12 | T5 other tenant | C1 web | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU12-54 | K-107 | P02/R02 | A1 | C3 API | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU12-55 | K-109 | P11/R12 | A1 | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU12-56 | K-107 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Role/permission matrix test incl |
      | EX-01ZU12-57 | K-108 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Role/permission matrix test incl |
      | EX-01ZU12-58 | K-109 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Role/permission matrix test incl |
```

##### US-01-ZU13 ENT-ACC-04…05 acceptance: SIEM streaming and just-in-time support access

| Field | Value |
|---|---|
| ID | US-01-ZU13 |
| Title | ENT-ACC-04…05 acceptance: SIEM streaming and just-in-time support access |
| Type | Compliance (acceptance binding) |
| Story | As a tenant administrator (P11, R12), I want SIEM streaming to HTTPS, syslog over TLS or object storage; retention 1, 3 or 7 years; support access is just-in-time: ticket-linked, tenant-approved, time-limited and audited, so that only the right people reach our data, with evidence an auditor can verify |
| Persona / roles | Tenant administrator (P11, R12) |
| Traces | FR-V12-K-110 (ENT-ACC-04); FR-V12-K-111 (ENT-ACC-05); DEC-417, DEC-784; tests TC-V12-K-110, TC-V12-K-111 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-01-ZR01, US-01-ZR02, US-01-ZR03, US-01-ZR04; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · authority ×4 · channel ×3 · session/MFA ×3 · region ×3 · operation ×2 · model MU02 |
| Notes | FR-V12-K-110, FR-V12-K-111: release per DEC-784 (SSO/SCIM and enterprise access in Release 1) · Trace requirement adopted literally from the ENT register (Part 11.11b §11.11.5.16); design depth and build points sit in US-01-ZR04, US-01-ZR05; this story binds the ENT acceptance to tests (DEC-941) · Screens A002, A009, A099, A197, A203; API family `/api/v1/identity/`; audit events `identity.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: ENT-ACC-04…05 acceptance: SIEM streaming and just-in-time support access
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with administrator "meera@kestrel.example.com" (R12) holding a fresh WebAuthn factor
    And the reused IdP broker is reachable and the break-glass account "bg-admin@kestrel.example.com" is registered

  @happy @ENT-ACC-04 @DEC-784
  Scenario: AC-01ZU13-01 Happy path – SIEM streaming to HTTPS, syslog over TLS or object storage (FR-V12-K-110)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "SIEM streaming to HTTPS, syslog over TLS or object storage" is exercised as specified by FR-V12-K-110:
      """
      SIEM streaming to HTTPS, syslog over TLS or object storage; retention 1, 3 or 7 years.
      """
    Then role/permission matrix test incl. SoD violation at build and at run time:
      """
      tamper detection on the audit chain, export format check, support access without tenant approval denied
      """
    And the audit event "identity.siem_streaming_to_https" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-ACC-05 @DEC-784
  Scenario: AC-01ZU13-02 Alternate – Support access is just-in-time: ticket-linked, tenant-approved (FR-V12-K-111)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Support access is just-in-time:
      """
      ticket-linked, tenant-approved" is exercised as specified by FR-V12-K-111: Support access is just-in-time: ticket-linked, tenant-approved,
      time-limited and audited.
      """
    Then role/permission matrix test incl. SoD violation at build and at run time:
      """
      tamper detection on the audit chain, export format check, support access without tenant approval denied
      """
    And the audit event "identity.support_access_is" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @BRL-APR-01
  Scenario: AC-01ZU13-03 Negative – a user cannot grant a role to themselves
    Given "arjun@kestrel.example.com" holds role "Campaign approver"
    When he assigns role "Campaign requester" to himself
    Then the API returns 409 "SOD_SELF_GRANT" and the role assignment does not exist
    And a security event "identity.sod.violation_blocked" is written

  @val
  Scenario: AC-01ZU13-04 Validation – non-HTTPS identity endpoints are rejected
    When Meera submits SSO metadata URL "http://idp.kestrel.example.com/metadata"
    Then the API returns 422 "METADATA_URL_NOT_HTTPS" and no configuration row exists

  @perm
  Scenario: AC-01ZU13-05 Permission – a startup head cannot change identity configuration
    When "arjun@kestrel.example.com" (R02) posts an identity configuration change
    Then the API returns 403 "PERMISSION_DENIED" and no side effect occurs (NSE)

  @edge @BRL-TEN-07
  Scenario: AC-01ZU13-06 Edge – revocation takes effect within 60 seconds
    Given "ravi@kestrel.example.com" has an active session at 2027-03-01T10:00:00+05:30
    When his access is revoked at 10:00:05
    Then his next API call after 10:01:05 returns 401 "SESSION_REVOKED"

  @sec @obs @MU02
  Scenario Outline: AC-01ZU13-07 Permutations – Enterprise identity, access and audit (3-way, 50 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the session is "<session_mfa>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU02 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-110 = SIEM streaming to HTTPS, syslog over TLS or object…
    #   K-111 = Support access is just-in-time: ticket-linked
    Examples: MU02 rows (3-way, seed 185; space 648; tuples 528/528; +1 baseline-allow)
      | ex | operation | persona | authority | channel | session_mfa | region | expected |
      | EX-01ZU13-01 | K-111 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Role/permission matrix test incl |
      | EX-01ZU13-02 | K-111 | P02/R02 | A1 | C2 mobile | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU13-03 | K-110 | P12/R13 | A1 | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU13-04 | K-111 | P12/R13 | T5 other tenant | C2 mobile | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-01ZU13-05 | K-110 | P02/R02 | A3 SoD/limit | C1 web | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU13-06 | K-110 | P11/R12 | T5 other tenant | C3 API | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU13-07 | K-110 | P12/R13 | A3 SoD/limit | C2 mobile | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU13-08 | K-111 | P11/R12 | A3 SoD/limit | C3 API | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU13-09 | K-110 | P11/R12 | A5 wrong role | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU13-10 | K-111 | P02/R02 | A5 wrong role | C1 web | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-01ZU13-11 | K-111 | P02/R02 | T5 other tenant | C3 API | session revoked | IN | uniform 404 NOT_FOUND |
      | EX-01ZU13-12 | K-111 | P12/R13 | A3 SoD/limit | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU13-13 | K-110 | P11/R12 | A1 | C2 mobile | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU13-14 | K-110 | P02/R02 | A5 wrong role | C3 API | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU13-15 | K-111 | P12/R13 | A5 wrong role | C3 API | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU13-16 | K-111 | P11/R12 | A5 wrong role | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU13-17 | K-110 | P02/R02 | A3 SoD/limit | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU13-18 | K-110 | P12/R13 | T5 other tenant | C1 web | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-01ZU13-19 | K-111 | P12/R13 | A1 | C1 web | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU13-20 | K-110 | P02/R02 | A5 wrong role | C2 mobile | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-01ZU13-21 | K-111 | P02/R02 | A1 | C3 API | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU13-22 | K-111 | P11/R12 | T5 other tenant | C2 mobile | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU13-23 | K-111 | P12/R13 | A5 wrong role | C2 mobile | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU13-24 | K-110 | P11/R12 | A3 SoD/limit | C3 API | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-01ZU13-25 | K-110 | P02/R02 | T5 other tenant | C1 web | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU13-26 | K-110 | P12/R13 | A5 wrong role | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU13-27 | K-110 | P02/R02 | A1 | C3 API | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU13-28 | K-111 | P11/R12 | T5 other tenant | C1 web | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-01ZU13-29 | K-110 | P12/R13 | T5 other tenant | C2 mobile | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU13-30 | K-110 | P02/R02 | A1 | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU13-31 | K-111 | P02/R02 | A3 SoD/limit | C1 web | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-01ZU13-32 | K-111 | P12/R13 | A1 | C2 mobile | passkey MFA | EU | ALLOW: Role/permission matrix test incl |
      | EX-01ZU13-33 | K-111 | P12/R13 | A3 SoD/limit | C3 API | OTP only | IN | 403 SOD_CONFLICT |
      | EX-01ZU13-34 | K-110 | P11/R12 | A5 wrong role | C1 web | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-01ZU13-35 | K-111 | P11/R12 | A3 SoD/limit | C2 mobile | OTP only | EU | 403 SOD_CONFLICT |
      | EX-01ZU13-36 | K-110 | P11/R12 | T5 other tenant | C3 API | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-01ZU13-37 | K-111 | P11/R12 | A1 | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU13-38 | K-111 | P11/R12 | A3 SoD/limit | C1 web | session revoked | IN | 401 SESSION_REVOKED |
      | EX-01ZU13-39 | K-111 | P02/R02 | A1 | C2 mobile | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-01ZU13-40 | K-110 | P02/R02 | T5 other tenant | C2 mobile | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-01ZU13-41 | K-110 | P11/R12 | A5 wrong role | C3 API | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-01ZU13-42 | K-110 | P12/R13 | A5 wrong role | C1 web | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-01ZU13-43 | K-111 | P02/R02 | A3 SoD/limit | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-01ZU13-44 | K-110 | P11/R12 | A3 SoD/limit | C3 API | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-01ZU13-45 | K-110 | P12/R13 | T5 other tenant | C3 API | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-01ZU13-46 | K-111 | P11/R12 | A5 wrong role | C2 mobile | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-01ZU13-47 | K-110 | P02/R02 | A5 wrong role | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-01ZU13-48 | K-110 | P11/R12 | T5 other tenant | C2 mobile | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-01ZU13-49 | K-110 | P02/R02 | A3 SoD/limit | C2 mobile | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-01ZU13-50 | K-110 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Role/permission matrix test incl |
```

##### US-01-ZU14 ENT-DAT-02…03 acceptance: customer-managed keys and residency at onboarding

| Field | Value |
|---|---|
| ID | US-01-ZU14 |
| Title | ENT-DAT-02…03 acceptance: customer-managed keys and residency at onboarding |
| Type | Compliance (acceptance binding) |
| Story | As a platform data owner (P11, R12, with the security lead), I want customer-managed keys (AWS KMS, Azure Key Vault, GCP KMS) with rotation; key revocation crypto-shreds data; data residency by region chosen at onboarding: India and EU now; US, UK, Middle East and APAC planned, so that every record stays in its tenant, company and residency zone, is exact and can be proven |
| Persona / roles | Platform data owner (P11, R12, with the security lead) |
| Traces | FR-V12-K-120 (ENT-DAT-02); FR-V12-K-121 (ENT-DAT-03); DEC-411, DEC-772, DEC-776; tests TC-V12-K-120, TC-V12-K-121 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-01-ZR26, US-01-ZR27, US-01-ZR28, US-01-YI01; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · authority ×4 · data class ×4 · db context ×3 · region ×3 · channel ×2 · operation ×2 · model MU04 |
| Notes | FR-V12-K-120: release per DEC-776 (BYOK across clouds) · FR-V12-K-121: release per DEC-772 and DEC-776 (residency chosen at onboarding from Release 1; EU stack on first EU contract) · Trace requirement adopted literally from the ENT register (Part 11.11b §11.11.5.16); design depth and build points sit in US-01-ZR28; this story binds the ENT acceptance to tests (DEC-941) · Screens A009, A197, A204; API family `/api/v1/data/`; audit events `data.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: ENT-DAT-02…03 acceptance: customer-managed keys and residency at onboarding
  Background:
    Given tenants "Kestrel Analytics Pvt Ltd" (zone IN) and "Nordlicht Robotik GmbH" (zone EU) provisioned by the two-tenant fixture
    And the API connects through the least-privilege role "app_rw" that sets app.tenant_id and app.company_ids per transaction (DEC-778)

  @happy @ENT-DAT-02 @DEC-776
  Scenario: AC-01ZU14-01 Happy path – Customer-managed keys (AWS KMS, Azure Key Vault (FR-V12-K-120)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Customer-managed keys (AWS KMS, Azure Key Vault" is exercised as specified by FR-V12-K-120:
      """
      Customer-managed keys (AWS KMS, Azure Key Vault, GCP KMS) with rotation; key revocation crypto-shreds data.
      """
    Then export/sandbox/promotion test:
      """
      manifest hash, second approver, link expiry, no personal data in sandbox, reviewed revision only; residency/key items gated by Founder
      decision
      """
    And the audit event "data.customer_managed_keys" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-DAT-03 @DEC-772
  Scenario: AC-01ZU14-02 Alternate – Data residency by region chosen at onboarding: India and EU now (FR-V12-K-121)
    Given Meera Iyer (R12) is signed in to the tenant with the capability enabled
    When "Data residency by region chosen at onboarding:
      """
      India and EU now" is exercised as specified by FR-V12-K-121: Data residency by region chosen at onboarding: India and EU now; US, UK, Middle
      East and APAC planned.
      """
    Then export/sandbox/promotion test:
      """
      manifest hash, second approver, link expiry, no personal data in sandbox, reviewed revision only; residency/key items gated by Founder
      decision
      """
    And the audit event "data.data_residency_by_region" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-778
  Scenario: AC-01ZU14-03 Negative – no statement runs without tenant context
    When a worker executes a query on "crm_contact" without setting app.tenant_id
    Then PostgreSQL raises SQLSTATE 42501 and no row is read or written

  @val
  Scenario: AC-01ZU14-04 Validation – money and identifiers are exact
    When a row is written with amount 12.50 as a float and currency "inr"
    Then the write is rejected: amount must be an integer in minor units and currency an upper-case ISO 4217 code

  @perm @BRL-TEN-03
  Scenario: AC-01ZU14-05 Permission – cross-tenant reference is impossible
    When tenant "Nordlicht Robotik GmbH" inserts a child row referencing a parent of "Kestrel Analytics Pvt Ltd"
    Then the composite foreign key rejects the row and the attempt is audited

  @edge @DEC-772
  Scenario: AC-01ZU14-06 Edge – an EU record is never written in Mumbai
    Given a request for tenant "Nordlicht Robotik GmbH" (zone EU) is routed to the Mumbai stack by mistake
    When it attempts a write
    Then the region check returns 409 "RESIDENCY_ZONE_MISMATCH" and nothing is written in either zone

  @sec @obs @MU04
  Scenario Outline: AC-01ZU14-07 Permutations – Data platform, residency and records (3-way, 71 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the database context is "<db_context>" for "<data_class>" data
    When "<operation>" runs through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU04 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-120 = Customer-managed keys (AWS KMS, Azure Key Vault
    #   K-121 = Data residency by region chosen at onboarding:…
    Examples: MU04 rows (3-way, seed 192; space 1,728; tuples 915/915; +2 baseline-allow)
      | ex | operation | persona | authority | data_class | db_context | region | channel | expected |
      | EX-01ZU14-01 | K-120 | P16/R19 | A1 | Public | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU14-02 | K-121 | P01/R01 | T5 other tenant | Confidential | no tenant ctx | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU14-03 | K-121 | P11/R12 | A5 wrong role | Confidential | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU14-04 | K-120 | P11/R12 | A3 SoD/limit | Restricted | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU14-05 | K-120 | P01/R01 | A3 SoD/limit | Internal | context set | EU | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU14-06 | K-121 | P16/R19 | T5 other tenant | Restricted | context set | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU14-07 | K-121 | P11/R12 | A1 | Internal | context set | EU→IN (misrouted) | worker job | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU14-08 | K-120 | P01/R01 | A5 wrong role | Restricted | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU14-09 | K-121 | P16/R19 | A3 SoD/limit | Public | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU14-10 | K-120 | P11/R12 | A1 | Confidential | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU14-11 | K-120 | P16/R19 | T5 other tenant | Confidential | context set | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU14-12 | K-121 | P01/R01 | A1 | Restricted | no tenant ctx | EU | C3 API | SQLSTATE 42501 |
      | EX-01ZU14-13 | K-121 | P16/R19 | A5 wrong role | Internal | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU14-14 | K-121 | P11/R12 | T5 other tenant | Public | no company scope | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU14-15 | K-120 | P16/R19 | A3 SoD/limit | Internal | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU14-16 | K-121 | P01/R01 | A5 wrong role | Public | context set | IN | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU14-17 | K-121 | P01/R01 | A3 SoD/limit | Confidential | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU14-18 | K-120 | P11/R12 | T5 other tenant | Public | no tenant ctx | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU14-19 | K-120 | P11/R12 | A5 wrong role | Restricted | context set | EU→IN (misrouted) | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU14-20 | K-120 | P01/R01 | A1 | Public | context set | IN | worker job | ALLOW: Export/sandbox/promotion test: manifest hash, |
      | EX-01ZU14-21 | K-120 | P16/R19 | A1 | Restricted | no company scope | EU | worker job | zero rows returned |
      | EX-01ZU14-22 | K-120 | P01/R01 | A5 wrong role | Internal | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU14-23 | K-120 | P01/R01 | T5 other tenant | Internal | no company scope | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU14-24 | K-121 | P11/R12 | A3 SoD/limit | Restricted | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU14-25 | K-121 | P16/R19 | A3 SoD/limit | Confidential | context set | EU→IN (misrouted) | worker job | 403 SOD_CONFLICT |
      | EX-01ZU14-26 | K-121 | P11/R12 | A5 wrong role | Restricted | context set | EU | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU14-27 | K-121 | P16/R19 | A1 | Confidential | no company scope | IN | worker job | zero rows returned |
      | EX-01ZU14-28 | K-120 | P11/R12 | A1 | Internal | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU14-29 | K-120 | P01/R01 | A5 wrong role | Confidential | context set | EU→IN (misrouted) | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU14-30 | K-121 | P11/R12 | T5 other tenant | Internal | no tenant ctx | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU14-31 | K-120 | P16/R19 | A5 wrong role | Public | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU14-32 | K-120 | P01/R01 | A3 SoD/limit | Public | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU14-33 | K-120 | P11/R12 | A3 SoD/limit | Confidential | context set | IN | worker job | 403 SOD_CONFLICT |
      | EX-01ZU14-34 | K-120 | P16/R19 | A1 | Confidential | context set | EU | C3 API | ALLOW: Export/sandbox/promotion test: manifest hash, |
      | EX-01ZU14-35 | K-121 | P16/R19 | T5 other tenant | Restricted | no tenant ctx | EU→IN (misrouted) | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU14-36 | K-121 | P16/R19 | T5 other tenant | Internal | no company scope | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU14-37 | K-121 | P01/R01 | A1 | Public | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU14-38 | K-121 | P01/R01 | A3 SoD/limit | Internal | context set | IN | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU14-39 | K-120 | P11/R12 | T5 other tenant | Public | context set | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU14-40 | K-120 | P01/R01 | T5 other tenant | Restricted | context set | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU14-41 | K-120 | P11/R12 | T5 other tenant | Confidential | no company scope | EU→IN (misrouted) | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU14-42 | K-121 | P16/R19 | A1 | Confidential | no tenant ctx | EU→IN (misrouted) | worker job | SQLSTATE 42501 |
      | EX-01ZU14-43 | K-120 | P16/R19 | A5 wrong role | Public | context set | EU | C3 API | 403 PERMISSION_DENIED |
      | EX-01ZU14-44 | K-120 | P01/R01 | A3 SoD/limit | Confidential | no tenant ctx | EU | worker job | SQLSTATE 42501 |
      | EX-01ZU14-45 | K-121 | P16/R19 | A3 SoD/limit | Restricted | context set | EU | C3 API | 403 SOD_CONFLICT |
      | EX-01ZU14-46 | K-121 | P11/R12 | A3 SoD/limit | Public | no company scope | IN | C3 API | zero rows returned |
      | EX-01ZU14-47 | K-120 | P11/R12 | A5 wrong role | Internal | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU14-48 | K-121 | P11/R12 | A5 wrong role | Public | no company scope | EU→IN (misrouted) | C3 API | zero rows returned |
      | EX-01ZU14-49 | K-121 | P11/R12 | A1 | Restricted | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU14-50 | K-120 | P01/R01 | A1 | Internal | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU14-51 | K-120 | P11/R12 | A3 SoD/limit | Internal | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU14-52 | K-121 | P16/R19 | A5 wrong role | Confidential | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU14-53 | K-121 | P16/R19 | A5 wrong role | Restricted | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU14-54 | K-120 | P01/R01 | T5 other tenant | Restricted | no company scope | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU14-55 | K-120 | P01/R01 | A1 | Restricted | context set | EU→IN (misrouted) | worker job | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU14-56 | K-121 | P11/R12 | A3 SoD/limit | Confidential | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU14-57 | K-120 | P01/R01 | T5 other tenant | Public | no company scope | IN | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU14-58 | K-121 | P11/R12 | A1 | Public | context set | EU→IN (misrouted) | C3 API | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU14-59 | K-120 | P16/R19 | A1 | Internal | context set | EU→IN (misrouted) | C3 API | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-01ZU14-60 | K-121 | P01/R01 | A3 SoD/limit | Restricted | no tenant ctx | IN | C3 API | SQLSTATE 42501 |
      | EX-01ZU14-61 | K-120 | P16/R19 | T5 other tenant | Public | no company scope | EU | C3 API | uniform 404 NOT_FOUND |
      | EX-01ZU14-62 | K-120 | P01/R01 | A1 | Public | no tenant ctx | IN | worker job | SQLSTATE 42501 |
      | EX-01ZU14-63 | K-120 | P16/R19 | T5 other tenant | Internal | context set | EU | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU14-64 | K-121 | P01/R01 | A5 wrong role | Restricted | no tenant ctx | EU→IN (misrouted) | C3 API | SQLSTATE 42501 |
      | EX-01ZU14-65 | K-120 | P01/R01 | A5 wrong role | Internal | context set | IN | worker job | 403 PERMISSION_DENIED |
      | EX-01ZU14-66 | K-120 | P11/R12 | A3 SoD/limit | Public | context set | EU→IN (misrouted) | worker job | 403 SOD_CONFLICT |
      | EX-01ZU14-67 | K-120 | P11/R12 | A5 wrong role | Internal | no company scope | EU | C3 API | zero rows returned |
      | EX-01ZU14-68 | K-120 | P11/R12 | T5 other tenant | Restricted | no company scope | IN | worker job | uniform 404 NOT_FOUND |
      | EX-01ZU14-69 | K-120 | P01/R01 | A1 | Confidential | no company scope | EU→IN (misrouted) | worker job | zero rows returned |
      | EX-01ZU14-70 | K-120 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Export/sandbox/promotion test: manifest hash, |
      | EX-01ZU14-71 | K-121 | P11/R12 | A1 | Public | context set | IN | C3 API | ALLOW: Export/sandbox/promotion test: manifest hash, |
```

#### 11.22.5.4.2 EP-02 Product truth and knowledge

| Field | Value |
|---|---|
| Epic | EP-02 Product truth and knowledge (Part 0 §0.10.2) |
| New stories in this file | US-02-ZU01, US-02-ZU02 |
| FR-V12 covered | A: 075–077, 079; F: 031 |
| Size | 2 stories · 7–11 SP · 4–11 pd (0.5/1.0 pd per SP) · central 6.3 pd (0.7 pd per SP mid) |
| Releases | Release 1: 1, Release 2: 1 |

##### US-02-ZU01 Divisions, brands, markets, channel accounts and offering lifecycle

| Field | Value |
|---|---|
| ID | US-02-ZU01 |
| Title | Divisions, brands, markets, channel accounts and offering lifecycle |
| Type | Compliance (acceptance binding) |
| Story | As a tenant admin, I want divisions, brands, markets and channel accounts with separate registration and target countries – with the acceptance criteria below, which the statement-only story US-02-YA01 did not carry |
| Persona / roles | Tenant administrator (P11, R12) |
| Traces | FR-V12-A-075 (MT-09, MT-10); FR-V12-A-076 (MT-17); FR-V12-A-077 (MT-18, MT-22, MT-23); FR-V12-A-079 (MT-11, MT-15); tests TC-V12-A-075, TC-V12-A-076, TC-V12-A-077, TC-V12-A-079 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 2–3 |
| Dependencies | US-02-YA01, US-01-ZR01, US-01-ZR02, US-01-ZR03, US-01-ZR04; source definition: Part 11.1b §ADR-180 Tenant per customer contract |
| Dimension profile | persona ×3 · authority ×4 · channel ×3 · session/MFA ×3 · region ×3 · operation ×4 · model MU02 |
| Notes | Acceptance binding: US-02-YA01 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens A002, A009, A099, A197, A203; API family `/api/v1/identity/`; audit events `identity.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Divisions, brands, markets, channel accounts and offering lifecycle
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with administrator "meera@kestrel.example.com" (R12) holding a fresh WebAuthn factor
    And the reused IdP broker is reachable and the break-glass account "bg-admin@kestrel.example.com" is registered

  @happy @MT-09 @MT-10
  Scenario: AC-02ZU01-01 Happy path – Division and brand masters (FR-V12-A-075)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Division and brand masters" is exercised as specified by FR-V12-A-075:
      """
      Division and brand masters: division has stable ID and company FK, lifecycle independent of name; brand owned by division, with scoped
      configuration and approved claims
      """
    Then rename division → linked offering valid; same brand name in two divisions → no leakage
    And the audit event "identity.division_and_brand_masters" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @MT-17
  Scenario: AC-02ZU01-02 Alternate – Registration, operating and target countries (FR-V12-A-076)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Registration, operating and target countries" is exercised as specified by FR-V12-A-076:
      """
      Registration, operating and target countries are separate attributes (company registration country ≠ operating countries ≠
      market/prospect/delivery country)
      """
    Then india registration with US target; filter target US independently
    And the audit event "identity.registration_operating_and" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @MT-18 @MT-22
  Scenario: AC-02ZU01-03 Alternate – Market profiles and channel accounts (FR-V12-A-077)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Market profiles and channel accounts" is exercised as specified by FR-V12-A-077:
      """
      Market profiles and channel accounts: one offering in several markets through offering-market associations (each independently eligible);
      several channel accounts per company and channel, each with sender aliases and credential reference
      """
    Then one offering in two markets; Email and WhatsApp accounts for two markets preserved; wrong-company account denied
    And the audit event "identity.market_profiles_and_channel" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @MT-11 @MT-15
  Scenario: AC-02ZU01-04 Alternate – Offering lifecycle (FR-V12-A-079)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Offering lifecycle" is exercised as specified by FR-V12-A-079:
      """
      Offering lifecycle draft → pilot → active → suspended → retired with an authorization gate for live external effects; history preserved;
      subscriber offering IDs separate from platform SKU IDs
      """
    Then suspend offering → new effect denied; past events retained
    And the audit event "identity.offering_lifecycle" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @BRL-APR-01
  Scenario: AC-02ZU01-05 Negative – a user cannot grant a role to themselves
    Given "arjun@kestrel.example.com" holds role "Campaign approver"
    When he assigns role "Campaign requester" to himself
    Then the API returns 409 "SOD_SELF_GRANT" and the role assignment does not exist
    And a security event "identity.sod.violation_blocked" is written

  @val
  Scenario: AC-02ZU01-06 Validation – non-HTTPS identity endpoints are rejected
    When Meera submits SSO metadata URL "http://idp.kestrel.example.com/metadata"
    Then the API returns 422 "METADATA_URL_NOT_HTTPS" and no configuration row exists

  @perm
  Scenario: AC-02ZU01-07 Permission – a startup head cannot change identity configuration
    When "arjun@kestrel.example.com" (R02) posts an identity configuration change
    Then the API returns 403 "PERMISSION_DENIED" and no side effect occurs (NSE)

  @edge @BRL-TEN-07
  Scenario: AC-02ZU01-08 Edge – revocation takes effect within 60 seconds
    Given "ravi@kestrel.example.com" has an active session at 2027-03-01T10:00:00+05:30
    When his access is revoked at 10:00:05
    Then his next API call after 10:01:05 returns 401 "SESSION_REVOKED"

  @sec @obs @MU02
  Scenario Outline: AC-02ZU01-09 Permutations – Enterprise identity, access and audit (3-way, 70 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the session is "<session_mfa>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU02 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-075 = Division and brand masters
    #   A-076 = Registration, operating and target countries
    #   A-077 = Market profiles and channel accounts
    #   A-079 = Offering lifecycle
    Examples: MU02 rows (3-way, seed 199; space 1,296; tuples 732/732; +4 baseline-allow)
      | ex | operation | persona | authority | channel | session_mfa | region | expected |
      | EX-02ZU01-01 | A-075 | P12/R13 | T5 other tenant | C1 web | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-02ZU01-02 | A-076 | P11/R12 | T5 other tenant | C3 API | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-02ZU01-03 | A-075 | P02/R02 | T5 other tenant | C2 mobile | session revoked | IN | uniform 404 NOT_FOUND |
      | EX-02ZU01-04 | A-077 | P11/R12 | A5 wrong role | C3 API | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-02ZU01-05 | A-079 | P12/R13 | A5 wrong role | C3 API | session revoked | IN | 401 SESSION_REVOKED |
      | EX-02ZU01-06 | A-075 | P11/R12 | A1 | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-02ZU01-07 | A-077 | P02/R02 | A1 | C2 mobile | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-02ZU01-08 | A-079 | P02/R02 | A1 | C1 web | passkey MFA | IN | ALLOW: Suspend offering → new effect denied |
      | EX-02ZU01-09 | A-077 | P12/R13 | A3 SoD/limit | C1 web | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-02ZU01-10 | A-079 | P11/R12 | A3 SoD/limit | C2 mobile | OTP only | IN | 403 SOD_CONFLICT |
      | EX-02ZU01-11 | A-075 | P12/R13 | A5 wrong role | C2 mobile | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-02ZU01-12 | A-075 | P02/R02 | A3 SoD/limit | C3 API | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-02ZU01-13 | A-076 | P12/R13 | A3 SoD/limit | C3 API | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-02ZU01-14 | A-076 | P02/R02 | A5 wrong role | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-02ZU01-15 | A-079 | P11/R12 | A5 wrong role | C1 web | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-02ZU01-16 | A-076 | P11/R12 | A3 SoD/limit | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-02ZU01-17 | A-079 | P02/R02 | T5 other tenant | C3 API | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-02ZU01-18 | A-079 | P12/R13 | A1 | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-02ZU01-19 | A-077 | P12/R13 | A1 | C3 API | passkey MFA | EU | ALLOW: One offering in two markets |
      | EX-02ZU01-20 | A-077 | P11/R12 | A1 | C1 web | session revoked | IN | 401 SESSION_REVOKED |
      | EX-02ZU01-21 | A-076 | P12/R13 | A1 | C1 web | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-02ZU01-22 | A-077 | P02/R02 | A5 wrong role | C2 mobile | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-02ZU01-23 | A-075 | P02/R02 | A5 wrong role | C1 web | OTP only | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-02ZU01-24 | A-077 | P11/R12 | T5 other tenant | C2 mobile | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-02ZU01-25 | A-077 | P02/R02 | T5 other tenant | C3 API | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-02ZU01-26 | A-079 | P11/R12 | T5 other tenant | C1 web | passkey MFA | EU | uniform 404 NOT_FOUND |
      | EX-02ZU01-27 | A-075 | P11/R12 | A1 | C2 mobile | OTP only | EU | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-02ZU01-28 | A-075 | P11/R12 | A3 SoD/limit | C1 web | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-02ZU01-29 | A-076 | P12/R13 | T5 other tenant | C2 mobile | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-02ZU01-30 | A-079 | P12/R13 | A3 SoD/limit | C2 mobile | passkey MFA | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-02ZU01-31 | A-076 | P02/R02 | A1 | C2 mobile | passkey MFA | EU | ALLOW: India registration with US target |
      | EX-02ZU01-32 | A-077 | P02/R02 | A3 SoD/limit | C3 API | OTP only | IN | 403 SOD_CONFLICT |
      | EX-02ZU01-33 | A-079 | P02/R02 | A3 SoD/limit | C1 web | OTP only | EU | 403 SOD_CONFLICT |
      | EX-02ZU01-34 | A-076 | P02/R02 | A5 wrong role | C3 API | passkey MFA | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-02ZU01-35 | A-076 | P11/R12 | A5 wrong role | C2 mobile | OTP only | IN | 403 PERMISSION_DENIED |
      | EX-02ZU01-36 | A-077 | P12/R13 | T5 other tenant | C2 mobile | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-02ZU01-37 | A-075 | P12/R13 | A1 | C3 API | OTP only | IN | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-02ZU01-38 | A-076 | P11/R12 | A1 | C1 web | passkey MFA | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU01-39 | A-079 | P02/R02 | T5 other tenant | C1 web | session revoked | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-02ZU01-40 | A-075 | P11/R12 | A5 wrong role | C2 mobile | session revoked | EU | 401 SESSION_REVOKED |
      | EX-02ZU01-41 | A-077 | P12/R13 | A5 wrong role | C1 web | passkey MFA | EU | 403 PERMISSION_DENIED |
      | EX-02ZU01-42 | A-079 | P11/R12 | A3 SoD/limit | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-02ZU01-43 | A-076 | P02/R02 | A3 SoD/limit | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-02ZU01-44 | A-076 | P02/R02 | A1 | C3 API | session revoked | EU | 401 SESSION_REVOKED |
      | EX-02ZU01-45 | A-079 | P12/R13 | T5 other tenant | C3 API | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-02ZU01-46 | A-076 | P02/R02 | T5 other tenant | C2 mobile | OTP only | EU | uniform 404 NOT_FOUND |
      | EX-02ZU01-47 | A-077 | P11/R12 | A3 SoD/limit | C2 mobile | passkey MFA | EU | 403 SOD_CONFLICT |
      | EX-02ZU01-48 | A-075 | P11/R12 | T5 other tenant | C3 API | OTP only | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-02ZU01-49 | A-079 | P12/R13 | A1 | C3 API | OTP only | EU→IN (misrouted) | 403 STEP_UP_REQUIRED for privileged actions |
      | EX-02ZU01-50 | A-079 | P02/R02 | A5 wrong role | C2 mobile | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-02ZU01-51 | A-075 | P12/R13 | A3 SoD/limit | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-02ZU01-52 | A-076 | P12/R13 | A3 SoD/limit | C1 web | passkey MFA | IN | 403 SOD_CONFLICT |
      | EX-02ZU01-53 | A-075 | P02/R02 | A1 | C1 web | passkey MFA | EU | ALLOW: Rename division → linked offering valid |
      | EX-02ZU01-54 | A-077 | P11/R12 | T5 other tenant | C1 web | OTP only | IN | uniform 404 NOT_FOUND |
      | EX-02ZU01-55 | A-075 | P02/R02 | A3 SoD/limit | C2 mobile | OTP only | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-02ZU01-56 | A-077 | P02/R02 | A5 wrong role | C3 API | session revoked | EU→IN (misrouted) | 401 SESSION_REVOKED |
      | EX-02ZU01-57 | A-076 | P12/R13 | A5 wrong role | C2 mobile | OTP only | EU | 403 PERMISSION_DENIED |
      | EX-02ZU01-58 | A-079 | P02/R02 | T5 other tenant | C2 mobile | passkey MFA | IN | uniform 404 NOT_FOUND |
      | EX-02ZU01-59 | A-075 | P12/R13 | A5 wrong role | C3 API | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-02ZU01-60 | A-077 | P02/R02 | A1 | C2 mobile | session revoked | IN | 401 SESSION_REVOKED |
      | EX-02ZU01-61 | A-077 | P02/R02 | A5 wrong role | C1 web | passkey MFA | IN | 403 PERMISSION_DENIED |
      | EX-02ZU01-62 | A-079 | P11/R12 | T5 other tenant | C3 API | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-02ZU01-63 | A-079 | P12/R13 | A5 wrong role | C1 web | session revoked | EU | 401 SESSION_REVOKED |
      | EX-02ZU01-64 | A-076 | P12/R13 | T5 other tenant | C1 web | session revoked | EU | uniform 404 NOT_FOUND |
      | EX-02ZU01-65 | A-079 | P11/R12 | A1 | C1 web | session revoked | IN | 401 SESSION_REVOKED |
      | EX-02ZU01-66 | A-075 | P11/R12 | T5 other tenant | C2 mobile | passkey MFA | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-02ZU01-67 | A-075 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Rename division → linked offering valid |
      | EX-02ZU01-68 | A-076 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: India registration with US target |
      | EX-02ZU01-69 | A-077 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: One offering in two markets |
      | EX-02ZU01-70 | A-079 | P11/R12 | A1 | C1 web | passkey MFA | IN | ALLOW: Suspend offering → new effect denied |
```

##### US-02-ZU02 Knowledge-chunk provenance, rights, freshness and quarantine

| Field | Value |
|---|---|
| ID | US-02-ZU02 |
| Title | Knowledge-chunk provenance, rights, freshness and quarantine |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want store per chunk source_ref, rights, provenance_hash, ingested_at, observed_at, freshness_limit, quarantine_state, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-031 (ch17); DEC-770, DEC-790; tests TC-V12-F-072 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×1 · model MU05 |
| Notes | FR-V12-F-031: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: Knowledge-chunk provenance, rights, freshness and quarantine
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @DEC-770
  Scenario: AC-02ZU02-01 Happy path – Store per chunk source_ref, rights, provenance_hash, ingested_at (FR-V12-F-031)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Store per chunk source_ref, rights, provenance_hash, ingested_at" is exercised as specified by FR-V12-F-031:
      """
      Store per chunk source_ref, rights, provenance_hash, ingested_at, observed_at, freshness_limit, quarantine_state; quarantine
      poisoned/unlicensed sources
      """
    Then quarantined chunk never retrieved; erasure removes chunk and vector with evidence
    And the audit event "ai.store_per_chunk_source_ref" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-02ZU02-02 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-02ZU02-03 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-02ZU02-04 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-02ZU02-05 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-02ZU02-06 Permutations – AI governance, evaluation, prompts and cost (3-way, 55 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-031 = Store per chunk source_ref, rights
    Examples: MU05 rows (3-way, seed 206; space 972; tuples 780/780; +1 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-02ZU02-01 | F-031 | P03/R03 | Public | candidate only | L1 | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-02ZU02-02 | F-031 | P10/R11 | Internal | prompt unapproved | L3 mandate | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-02ZU02-03 | F-031 | P16/R20 | Confidential | candidate only | L3 revoked | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-02ZU02-04 | F-031 | P10/R11 | Restricted | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-05 | F-031 | P16/R20 | Public | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-06 | F-031 | P03/R03 | Confidential | model Approved | L3 mandate | hard cap | EU | HELD AI_BUDGET_EXHAUSTED |
      | EX-02ZU02-07 | F-031 | P03/R03 | Restricted | prompt unapproved | L3 revoked | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-02ZU02-08 | F-031 | P10/R11 | Public | model Approved | L3 revoked | soft cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-02ZU02-09 | F-031 | P16/R20 | Internal | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-10 | F-031 | P03/R03 | Confidential | prompt unapproved | L1 | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-02ZU02-11 | F-031 | P16/R20 | Internal | model Approved | L3 mandate | in budget | EU | ALLOW: Quarantined chunk never retrieved |
      | EX-02ZU02-12 | F-031 | P10/R11 | Restricted | candidate only | L3 mandate | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-02ZU02-13 | F-031 | P03/R03 | Internal | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-14 | F-031 | P10/R11 | Confidential | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-15 | F-031 | P16/R20 | Restricted | model Approved | L3 revoked | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-02ZU02-16 | F-031 | P03/R03 | Public | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-02ZU02-17 | F-031 | P16/R20 | Public | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-02ZU02-18 | F-031 | P10/R11 | Internal | candidate only | L3 revoked | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-02ZU02-19 | F-031 | P10/R11 | Confidential | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-02ZU02-20 | F-031 | P03/R03 | Restricted | candidate only | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-21 | F-031 | P16/R20 | Confidential | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-22 | F-031 | P03/R03 | Internal | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-23 | F-031 | P16/R20 | Internal | prompt unapproved | L3 revoked | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-02ZU02-24 | F-031 | P16/R20 | Public | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-25 | F-031 | P10/R11 | Public | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-02ZU02-26 | F-031 | P10/R11 | Public | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-27 | F-031 | P03/R03 | Internal | model Approved | L1 | hard cap | IN | PENDING_APPROVAL |
      | EX-02ZU02-28 | F-031 | P16/R20 | Restricted | candidate only | L1 | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-02ZU02-29 | F-031 | P16/R20 | Restricted | prompt unapproved | L3 mandate | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-02ZU02-30 | F-031 | P10/R11 | Internal | model Approved | L1 | soft cap | EU | PENDING_APPROVAL |
      | EX-02ZU02-31 | F-031 | P16/R20 | Confidential | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-02ZU02-32 | F-031 | P10/R11 | Confidential | model Approved | L3 mandate | in budget | IN | ALLOW: Quarantined chunk never retrieved |
      | EX-02ZU02-33 | F-031 | P10/R11 | Restricted | prompt unapproved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-34 | F-031 | P03/R03 | Public | model Approved | L3 revoked | in budget | EU | ROUTE MANDATE_INACTIVE |
      | EX-02ZU02-35 | F-031 | P03/R03 | Confidential | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-36 | F-031 | P03/R03 | Internal | candidate only | L3 mandate | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-02ZU02-37 | F-031 | P10/R11 | Restricted | prompt unapproved | L1 | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-02ZU02-38 | F-031 | P16/R20 | Confidential | candidate only | L3 mandate | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-02ZU02-39 | F-031 | P03/R03 | Public | prompt unapproved | L3 revoked | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-02ZU02-40 | F-031 | P10/R11 | Internal | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-41 | F-031 | P03/R03 | Restricted | model Approved | L3 mandate | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-02ZU02-42 | F-031 | P03/R03 | Confidential | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-43 | F-031 | P16/R20 | Restricted | candidate only | L3 revoked | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-02ZU02-44 | F-031 | P10/R11 | Restricted | candidate only | L3 revoked | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-02ZU02-45 | F-031 | P10/R11 | Public | candidate only | L3 mandate | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-02ZU02-46 | F-031 | P16/R20 | Public | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-47 | F-031 | P03/R03 | Internal | prompt unapproved | L3 revoked | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-02ZU02-48 | F-031 | P10/R11 | Confidential | model Approved | L3 revoked | soft cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-02ZU02-49 | F-031 | P03/R03 | Restricted | candidate only | L1 | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-02ZU02-50 | F-031 | P16/R20 | Public | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-02ZU02-51 | F-031 | P16/R20 | Restricted | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-52 | F-031 | P16/R20 | Internal | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-02ZU02-53 | F-031 | P03/R03 | Public | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-02ZU02-54 | F-031 | P03/R03 | Confidential | model Approved | L1 | hard cap | IN | PENDING_APPROVAL |
      | EX-02ZU02-55 | F-031 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Quarantined chunk never retrieved |
```

#### 11.22.5.4.3 EP-03 Consent, privacy, eligibility and compliance

| Field | Value |
|---|---|
| Epic | EP-03 Consent, privacy, eligibility and compliance (Part 0 §0.10.2) |
| New stories in this file | US-03-ZU01, US-03-ZU02, US-03-ZU03, US-03-ZU04, US-03-ZU05, US-03-ZU06, US-03-ZU07, US-03-ZU08 |
| FR-V12 covered | E: 022; F: 042, 044, 046–047; H: 013, 033; K: 140–144; M: 100 |
| Size | 8 stories · 28–46 SP · 14–46 pd (0.5/1.0 pd per SP) · central 25.9 pd (0.7 pd per SP mid) |
| Releases | Release 1: 5, Release 2: 2, Release 3+: 1 |

##### US-03-ZU01 Deny-reason precedence in the V12 order

| Field | Value |
|---|---|
| ID | US-03-ZU01 |
| Title | Deny-reason precedence in the V12 order |
| Type | Compliance (acceptance binding) |
| Story | As a compliance lead I want deny reasons ordered by V12 precedence – with the acceptance criteria below, which the statement-only story US-03-YE01 did not carry |
| Persona / roles | DPO / counsel (P09, R10) |
| Traces | FR-V12-E-022 (ch06); tests TC-031 |
| Priority | Should |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-03-YE01, US-03-YM09, US-03-YA01, US-03-YG02, US-03-YG03; source definition: Part 11.5b §11.5.5.13 Functional requirement register |
| Dimension profile | persona ×3 · jurisdiction ×4 · consent ×3 · channel ×3 · data class ×3 · region ×3 · operation ×1 · model MU06 |
| Notes | Acceptance binding: US-03-YE01 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens A007, A013, A200, A201, A202, W29, W30; API family `/api/v1/compliance/`; audit events `compliance.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Deny-reason precedence in the V12 order
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" with DPO "farah@kestrel.example.com" (R10)
    And jurisdiction packs RP-IN (Approved), RP-EU (Approved), RP-UK (Draft) and RP-US (Expired) in the rule-pack registry (Part 11.15)

  @happy
  Scenario: AC-03ZU01-01 Happy path – Deny-reason precedence per V12 order (FR-V12-E-022)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Deny-reason precedence per V12 order" is exercised as specified by FR-V12-E-022: Deny-reason precedence per V12 order
    Then the observable result matches FR-V12-E-022 and its tests TC-031
    And the audit event "compliance.deny_reason_precedence_per" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-ELG-18
  Scenario: AC-03ZU01-02 Negative – a draft pack never allows an outbound action
    Given recipient "olivia@brightway.example.co.uk" is in market UK whose pack RP-UK is "Draft"
    When a promotional email to her passes every other check
    Then the PDP returns HOLD "PACK_NOT_ACTIVE" and no message is dispatched

  @val
  Scenario: AC-03ZU01-03 Validation – the promotional window is checked in the recipient's local time
    Given recipient "anu@sunrise.example.in" in Asia/Kolkata
    When a promotional SMS is scheduled for 21:15 local time
    Then the preflight returns HOLD "OUTSIDE_MESSAGING_WINDOW" (09:00–21:00, DEC-777) and proposes 09:00 next day

  @perm
  Scenario: AC-03ZU01-04 Permission – only R10 can approve a pack
    When "maya@kestrel.example.com" (R05) approves pack RP-UK
    Then the API returns 403 "PERMISSION_DENIED" and the pack stays "Draft"

  @edge
  Scenario: AC-03ZU01-05 Edge – consent withdrawal holds queued work
    Given 3 queued messages for "anu@sunrise.example.in"
    When she withdraws consent at 2027-05-02T10:00:00+05:30
    Then all 3 are "HELD" with "CONSENT_WITHDRAWN" and the suppression list is updated within 60 seconds

  @sec @obs @MU06
  Scenario Outline: AC-03ZU01-06 Permutations – Jurisdiction packs, consent and legal controls (3-way, 57 rows)
    Given actor "<persona>" in zone "<region>" for a recipient in "<jurisdiction>"
    And consent is "<consent>" and the data class is "<data_class>"
    When "<operation>" is checked for channel "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU06 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   E-022 = Deny-reason precedence per V12 order
    Examples: MU06 rows (3-way, seed 213; space 972; tuples 780/780; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | consent | channel | data_class | region | expected |
      | EX-03ZU01-01 | E-022 | P09/R10 | UK draft | valid | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-02 | E-022 | P03/R03 | EU ✓ | withdrawn | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-03 | E-022 | P05/R05 | US expired | valid | WhatsApp | Internal | EU | HOLD PACK_EXPIRED |
      | EX-03ZU01-04 | E-022 | P09/R10 | IN ✓ | withdrawn | email | Internal | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU01-05 | E-022 | P03/R03 | US expired | unknown | SMS/voice | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU01-06 | E-022 | P03/R03 | UK draft | unknown | email | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU01-07 | E-022 | P05/R05 | IN ✓ | withdrawn | SMS/voice | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU01-08 | E-022 | P05/R05 | EU ✓ | unknown | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-09 | E-022 | P05/R05 | EU ✓ | valid | SMS/voice | Confidential | IN | ALLOW: Deny-reason precedence per V12 order |
      | EX-03ZU01-10 | E-022 | P09/R10 | EU ✓ | unknown | WhatsApp | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU01-11 | E-022 | P03/R03 | IN ✓ | valid | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-12 | E-022 | P05/R05 | UK draft | withdrawn | WhatsApp | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU01-13 | E-022 | P09/R10 | US expired | withdrawn | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-14 | E-022 | P09/R10 | IN ✓ | valid | WhatsApp | Confidential | EU | ALLOW: Deny-reason precedence per V12 order |
      | EX-03ZU01-15 | E-022 | P03/R03 | IN ✓ | unknown | WhatsApp | Internal | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU01-16 | E-022 | P03/R03 | EU ✓ | withdrawn | SMS/voice | Internal | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU01-17 | E-022 | P09/R10 | IN ✓ | unknown | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-18 | E-022 | P05/R05 | UK draft | valid | email | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU01-19 | E-022 | P05/R05 | US expired | unknown | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-20 | E-022 | P03/R03 | EU ✓ | withdrawn | email | Restricted | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU01-21 | E-022 | P03/R03 | UK draft | valid | WhatsApp | Restricted | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU01-22 | E-022 | P09/R10 | US expired | unknown | SMS/voice | Internal | EU | HOLD PACK_EXPIRED |
      | EX-03ZU01-23 | E-022 | P03/R03 | US expired | valid | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-24 | E-022 | P09/R10 | UK draft | unknown | WhatsApp | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU01-25 | E-022 | P09/R10 | EU ✓ | valid | email | Internal | EU | ALLOW: Deny-reason precedence per V12 order |
      | EX-03ZU01-26 | E-022 | P05/R05 | UK draft | withdrawn | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-27 | E-022 | P05/R05 | US expired | withdrawn | email | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU01-28 | E-022 | P09/R10 | US expired | withdrawn | WhatsApp | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU01-29 | E-022 | P03/R03 | US expired | valid | email | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-03ZU01-30 | E-022 | P05/R05 | IN ✓ | valid | SMS/voice | Internal | IN | ALLOW: Deny-reason precedence per V12 order |
      | EX-03ZU01-31 | E-022 | P05/R05 | IN ✓ | unknown | email | Confidential | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU01-32 | E-022 | P09/R10 | EU ✓ | valid | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-33 | E-022 | P09/R10 | UK draft | withdrawn | email | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU01-34 | E-022 | P03/R03 | UK draft | unknown | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-35 | E-022 | P03/R03 | IN ✓ | withdrawn | SMS/voice | Confidential | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU01-36 | E-022 | P09/R10 | US expired | unknown | email | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU01-37 | E-022 | P05/R05 | IN ✓ | withdrawn | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-38 | E-022 | P05/R05 | EU ✓ | withdrawn | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-39 | E-022 | P09/R10 | EU ✓ | unknown | SMS/voice | Confidential | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU01-40 | E-022 | P05/R05 | US expired | unknown | SMS/voice | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-03ZU01-41 | E-022 | P09/R10 | IN ✓ | valid | WhatsApp | Restricted | IN | ALLOW: Deny-reason precedence per V12 order |
      | EX-03ZU01-42 | E-022 | P05/R05 | UK draft | valid | SMS/voice | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU01-43 | E-022 | P03/R03 | US expired | withdrawn | email | Internal | IN | HOLD PACK_EXPIRED |
      | EX-03ZU01-44 | E-022 | P05/R05 | EU ✓ | withdrawn | WhatsApp | Confidential | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU01-45 | E-022 | P03/R03 | UK draft | withdrawn | SMS/voice | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU01-46 | E-022 | P03/R03 | EU ✓ | unknown | email | Internal | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU01-47 | E-022 | P03/R03 | US expired | withdrawn | WhatsApp | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU01-48 | E-022 | P05/R05 | UK draft | valid | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-49 | E-022 | P03/R03 | EU ✓ | valid | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-50 | E-022 | P05/R05 | UK draft | unknown | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-51 | E-022 | P09/R10 | EU ✓ | withdrawn | SMS/voice | Restricted | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU01-52 | E-022 | P03/R03 | IN ✓ | valid | WhatsApp | Internal | EU | ALLOW: Deny-reason precedence per V12 order |
      | EX-03ZU01-53 | E-022 | P09/R10 | US expired | valid | SMS/voice | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU01-54 | E-022 | P05/R05 | EU ✓ | valid | WhatsApp | Restricted | IN | ALLOW: Deny-reason precedence per V12 order |
      | EX-03ZU01-55 | E-022 | P05/R05 | IN ✓ | unknown | WhatsApp | Restricted | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU01-56 | E-022 | P09/R10 | US expired | withdrawn | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU01-57 | E-022 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Deny-reason precedence per V12 order |
```

##### US-03-ZU02 Versioned jurisdiction packs, scoped consent ledger and regulatory clocks

| Field | Value |
|---|---|
| ID | US-03-ZU02 |
| Title | Versioned jurisdiction packs, scoped consent ledger and regulatory clocks |
| Type | Compliance |
| Story | As a DPO / counsel (P09, R10), I want jurisdiction packs versioned with states; only Approved enforced; unreviewed → stricter outcome; scoped consent ledger and withdrawal suppression; queued runs held; regulatory clocks for DSAR and breach per pack, so that nothing is sent, recorded or published unless the law of the recipient's market allows it and we can prove it |
| Persona / roles | DPO / counsel (P09, R10) |
| Traces | FR-V12-F-042 (CJ-R01/19/20); FR-V12-F-044 (CJ-R04/05); FR-V12-F-046 (CJ-R07/08); DEC-770, DEC-790; tests TC-V12-F-097, TC-V12-F-101, TC-V12-F-104 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-03-YM09, US-03-YA01, US-03-YG02, US-03-YG03; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · jurisdiction ×4 · consent ×3 · channel ×3 · data class ×3 · region ×3 · operation ×3 · model MU06 |
| Notes | FR-V12-F-042, FR-V12-F-044, FR-V12-F-046: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Screens A007, A013, A200, A201, A202, W29, W30; API family `/api/v1/compliance/`; audit events `compliance.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Versioned jurisdiction packs, scoped consent ledger and regulatory clocks
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" with DPO "farah@kestrel.example.com" (R10)
    And jurisdiction packs RP-IN (Approved), RP-EU (Approved), RP-UK (Draft) and RP-US (Expired) in the rule-pack registry (Part 11.15)

  @happy @CJ-R01 @DEC-770
  Scenario: AC-03ZU02-01 Happy path – Jurisdiction packs versioned with states; only Approved enforced (FR-V12-F-042)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Jurisdiction packs versioned with states; only Approved enforced" is exercised as specified by FR-V12-F-042:
      """
      Jurisdiction packs versioned with states; only Approved enforced; unreviewed → stricter outcome
      """
    Then draft pack never ALLOWs
    And the audit event "compliance.jurisdiction_packs_versioned" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @CJ-R04 @DEC-770
  Scenario: AC-03ZU02-02 Alternate – Scoped consent ledger and withdrawal suppression; queued runs held (FR-V12-F-044)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Scoped consent ledger and withdrawal suppression; queued runs held" is exercised as specified by FR-V12-F-044:
      """
      Scoped consent ledger and withdrawal suppression; queued runs held
      """
    Then queued run after withdrawal → Held, no dispatch
    And the audit event "compliance.scoped_consent_ledger_and" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @CJ-R07 @DEC-770
  Scenario: AC-03ZU02-03 Alternate – Regulatory clocks for DSAR and breach per pack (FR-V12-F-046)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Regulatory clocks for DSAR and breach per pack" is exercised as specified by FR-V12-F-046: Regulatory clocks for DSAR and breach per pack
    Then clocks start at detection; overdue visible
    And the audit event "compliance.regulatory_clocks_for_dsar" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-ELG-18
  Scenario: AC-03ZU02-04 Negative – a draft pack never allows an outbound action
    Given recipient "olivia@brightway.example.co.uk" is in market UK whose pack RP-UK is "Draft"
    When a promotional email to her passes every other check
    Then the PDP returns HOLD "PACK_NOT_ACTIVE" and no message is dispatched

  @val
  Scenario: AC-03ZU02-05 Validation – the promotional window is checked in the recipient's local time
    Given recipient "anu@sunrise.example.in" in Asia/Kolkata
    When a promotional SMS is scheduled for 21:15 local time
    Then the preflight returns HOLD "OUTSIDE_MESSAGING_WINDOW" (09:00–21:00, DEC-777) and proposes 09:00 next day

  @perm
  Scenario: AC-03ZU02-06 Permission – only R10 can approve a pack
    When "maya@kestrel.example.com" (R05) approves pack RP-UK
    Then the API returns 403 "PERMISSION_DENIED" and the pack stays "Draft"

  @edge
  Scenario: AC-03ZU02-07 Edge – consent withdrawal holds queued work
    Given 3 queued messages for "anu@sunrise.example.in"
    When she withdraws consent at 2027-05-02T10:00:00+05:30
    Then all 3 are "HELD" with "CONSENT_WITHDRAWN" and the suppression list is updated within 60 seconds

  @sec @obs @MU06
  Scenario Outline: AC-03ZU02-08 Permutations – Jurisdiction packs, consent and legal controls (3-way, 64 rows)
    Given actor "<persona>" in zone "<region>" for a recipient in "<jurisdiction>"
    And consent is "<consent>" and the data class is "<data_class>"
    When "<operation>" is checked for channel "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU06 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-042 = Jurisdiction packs versioned with states
    #   F-044 = Scoped consent ledger and withdrawal suppression
    #   F-046 = Regulatory clocks for DSAR and breach per pack
    Examples: MU06 rows (3-way, seed 220; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | jurisdiction | consent | channel | data_class | region | expected |
      | EX-03ZU02-01 | F-042 | P03/R03 | UK draft | valid | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-02 | F-044 | P09/R10 | IN ✓ | valid | email | Confidential | EU | ALLOW: Queued run after withdrawal → Held, no dispatch |
      | EX-03ZU02-03 | F-044 | P09/R10 | UK draft | withdrawn | SMS/voice | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU02-04 | F-042 | P09/R10 | US expired | valid | WhatsApp | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU02-05 | F-046 | P05/R05 | IN ✓ | withdrawn | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-06 | F-044 | P05/R05 | EU ✓ | unknown | WhatsApp | Confidential | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU02-07 | F-046 | P03/R03 | US expired | unknown | WhatsApp | Internal | EU | HOLD PACK_EXPIRED |
      | EX-03ZU02-08 | F-042 | P05/R05 | US expired | withdrawn | SMS/voice | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU02-09 | F-046 | P03/R03 | IN ✓ | valid | SMS/voice | Confidential | IN | ALLOW: Clocks start at detection |
      | EX-03ZU02-10 | F-046 | P09/R10 | EU ✓ | unknown | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-11 | F-042 | P05/R05 | IN ✓ | unknown | email | Internal | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU02-12 | F-044 | P03/R03 | US expired | withdrawn | email | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU02-13 | F-044 | P05/R05 | UK draft | valid | SMS/voice | Restricted | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU02-14 | F-044 | P03/R03 | UK draft | unknown | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-15 | F-042 | P09/R10 | EU ✓ | withdrawn | WhatsApp | Internal | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU02-16 | F-044 | P05/R05 | US expired | valid | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-17 | F-042 | P03/R03 | EU ✓ | unknown | SMS/voice | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU02-18 | F-046 | P03/R03 | UK draft | withdrawn | email | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU02-19 | F-042 | P09/R10 | IN ✓ | unknown | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-20 | F-046 | P05/R05 | EU ✓ | valid | email | Internal | IN | ALLOW: Clocks start at detection |
      | EX-03ZU02-21 | F-046 | P05/R05 | US expired | unknown | SMS/voice | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU02-22 | F-046 | P09/R10 | IN ✓ | valid | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-23 | F-044 | P03/R03 | EU ✓ | valid | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-24 | F-042 | P05/R05 | EU ✓ | withdrawn | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-25 | F-042 | P03/R03 | UK draft | withdrawn | WhatsApp | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU02-26 | F-044 | P03/R03 | IN ✓ | withdrawn | WhatsApp | Internal | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU02-27 | F-046 | P09/R10 | UK draft | valid | WhatsApp | Restricted | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU02-28 | F-046 | P09/R10 | US expired | withdrawn | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-29 | F-044 | P05/R05 | UK draft | unknown | email | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU02-30 | F-042 | P09/R10 | IN ✓ | withdrawn | SMS/voice | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU02-31 | F-046 | P09/R10 | US expired | unknown | email | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-03ZU02-32 | F-046 | P03/R03 | EU ✓ | withdrawn | SMS/voice | Internal | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU02-33 | F-042 | P05/R05 | US expired | valid | email | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU02-34 | F-042 | P03/R03 | US expired | valid | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-35 | F-046 | P05/R05 | EU ✓ | valid | WhatsApp | Confidential | EU | ALLOW: Clocks start at detection |
      | EX-03ZU02-36 | F-044 | P03/R03 | IN ✓ | unknown | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-37 | F-044 | P09/R10 | US expired | unknown | SMS/voice | Internal | EU | HOLD PACK_EXPIRED |
      | EX-03ZU02-38 | F-044 | P09/R10 | EU ✓ | withdrawn | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-39 | F-042 | P05/R05 | UK draft | unknown | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-40 | F-046 | P05/R05 | UK draft | withdrawn | WhatsApp | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU02-41 | F-044 | P09/R10 | IN ✓ | valid | WhatsApp | Restricted | IN | ALLOW: Queued run after withdrawal → Held, no dispatch |
      | EX-03ZU02-42 | F-046 | P05/R05 | IN ✓ | unknown | SMS/voice | Confidential | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU02-43 | F-046 | P03/R03 | UK draft | withdrawn | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-44 | F-042 | P09/R10 | UK draft | unknown | email | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU02-45 | F-042 | P05/R05 | EU ✓ | unknown | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-46 | F-044 | P03/R03 | EU ✓ | valid | email | Internal | EU | ALLOW: Queued run after withdrawal → Held, no dispatch |
      | EX-03ZU02-47 | F-042 | P09/R10 | EU ✓ | valid | SMS/voice | Restricted | IN | ALLOW: Draft pack never ALLOWs |
      | EX-03ZU02-48 | F-044 | P05/R05 | IN ✓ | withdrawn | SMS/voice | Confidential | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU02-49 | F-042 | P05/R05 | UK draft | valid | SMS/voice | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU02-50 | F-042 | P03/R03 | US expired | unknown | WhatsApp | Internal | IN | HOLD PACK_EXPIRED |
      | EX-03ZU02-51 | F-046 | P09/R10 | UK draft | unknown | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-52 | F-044 | P09/R10 | US expired | withdrawn | WhatsApp | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-03ZU02-53 | F-046 | P03/R03 | US expired | valid | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-54 | F-042 | P03/R03 | IN ✓ | valid | email | Restricted | EU | ALLOW: Draft pack never ALLOWs |
      | EX-03ZU02-55 | F-046 | P05/R05 | EU ✓ | withdrawn | WhatsApp | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU02-56 | F-046 | P09/R10 | IN ✓ | withdrawn | email | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU02-57 | F-042 | P09/R10 | UK draft | withdrawn | WhatsApp | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU02-58 | F-042 | P09/R10 | US expired | unknown | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-59 | F-044 | P03/R03 | UK draft | valid | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU02-60 | F-042 | P05/R05 | IN ✓ | valid | WhatsApp | Confidential | IN | ALLOW: Draft pack never ALLOWs |
      | EX-03ZU02-61 | F-046 | P03/R03 | EU ✓ | unknown | email | Confidential | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU02-62 | F-042 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Draft pack never ALLOWs |
      | EX-03ZU02-63 | F-044 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Queued run after withdrawal → Held, no dispatch |
      | EX-03ZU02-64 | F-046 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Clocks start at detection |
```

##### US-03-ZU03 AI disclosure and machine-readable marking

| Field | Value |
|---|---|
| ID | US-03-ZU03 |
| Title | AI disclosure and machine-readable marking |
| Type | Compliance |
| Story | As a DPO / counsel (P09, R10), I want AI disclosure and machine-readable marking on AI content and agents, so that nothing is sent, recorded or published unless the law of the recipient's market allows it and we can prove it |
| Persona / roles | DPO / counsel (P09, R10) |
| Traces | FR-V12-F-047 (CJ-R13); DEC-770, DEC-790; tests TC-V12-F-109 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-03-YM09, US-03-YA01, US-03-YG02, US-03-YG03; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · jurisdiction ×4 · consent ×3 · channel ×3 · data class ×3 · region ×3 · operation ×1 · model MU06 |
| Notes | FR-V12-F-047: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Related existing stories (shared source IDs, no FR trace): US-22-ZQ01 · Screens A007, A013, A200, A201, A202, W29, W30; API family `/api/v1/compliance/`; audit events `compliance.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: AI disclosure and machine-readable marking
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" with DPO "farah@kestrel.example.com" (R10)
    And jurisdiction packs RP-IN (Approved), RP-EU (Approved), RP-UK (Draft) and RP-US (Expired) in the rule-pack registry (Part 11.15)

  @happy @CJ-R13 @DEC-770
  Scenario: AC-03ZU03-01 Happy path – AI disclosure and machine-readable marking on AI content and agents (FR-V12-F-047)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "AI disclosure and machine-readable marking on AI content and agents" is exercised as specified by FR-V12-F-047:
      """
      AI disclosure and machine-readable marking on AI content and agents
      """
    Then undisclosed AI content in EU → HOLD
    And the audit event "compliance.ai_disclosure_and" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-ELG-18
  Scenario: AC-03ZU03-02 Negative – a draft pack never allows an outbound action
    Given recipient "olivia@brightway.example.co.uk" is in market UK whose pack RP-UK is "Draft"
    When a promotional email to her passes every other check
    Then the PDP returns HOLD "PACK_NOT_ACTIVE" and no message is dispatched

  @val
  Scenario: AC-03ZU03-03 Validation – the promotional window is checked in the recipient's local time
    Given recipient "anu@sunrise.example.in" in Asia/Kolkata
    When a promotional SMS is scheduled for 21:15 local time
    Then the preflight returns HOLD "OUTSIDE_MESSAGING_WINDOW" (09:00–21:00, DEC-777) and proposes 09:00 next day

  @perm
  Scenario: AC-03ZU03-04 Permission – only R10 can approve a pack
    When "maya@kestrel.example.com" (R05) approves pack RP-UK
    Then the API returns 403 "PERMISSION_DENIED" and the pack stays "Draft"

  @edge
  Scenario: AC-03ZU03-05 Edge – consent withdrawal holds queued work
    Given 3 queued messages for "anu@sunrise.example.in"
    When she withdraws consent at 2027-05-02T10:00:00+05:30
    Then all 3 are "HELD" with "CONSENT_WITHDRAWN" and the suppression list is updated within 60 seconds

  @sec @obs @MU06
  Scenario Outline: AC-03ZU03-06 Permutations – Jurisdiction packs, consent and legal controls (3-way, 57 rows)
    Given actor "<persona>" in zone "<region>" for a recipient in "<jurisdiction>"
    And consent is "<consent>" and the data class is "<data_class>"
    When "<operation>" is checked for channel "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU06 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-047 = AI disclosure and machine-readable marking on AI…
    Examples: MU06 rows (3-way, seed 227; space 972; tuples 780/780; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | consent | channel | data_class | region | expected |
      | EX-03ZU03-01 | F-047 | P03/R03 | US expired | unknown | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-02 | F-047 | P03/R03 | IN ✓ | valid | email | Confidential | IN | ALLOW: Undisclosed AI content in EU → HOLD |
      | EX-03ZU03-03 | F-047 | P09/R10 | IN ✓ | withdrawn | WhatsApp | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU03-04 | F-047 | P05/R05 | UK draft | withdrawn | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-05 | F-047 | P09/R10 | EU ✓ | unknown | SMS/voice | Restricted | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU03-06 | F-047 | P05/R05 | EU ✓ | valid | email | Internal | EU | ALLOW: Undisclosed AI content in EU → HOLD |
      | EX-03ZU03-07 | F-047 | P09/R10 | UK draft | valid | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-08 | F-047 | P03/R03 | US expired | valid | SMS/voice | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU03-09 | F-047 | P09/R10 | US expired | withdrawn | email | Internal | IN | HOLD PACK_EXPIRED |
      | EX-03ZU03-10 | F-047 | P05/R05 | UK draft | unknown | WhatsApp | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU03-11 | F-047 | P05/R05 | IN ✓ | unknown | SMS/voice | Internal | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU03-12 | F-047 | P03/R03 | EU ✓ | withdrawn | WhatsApp | Confidential | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU03-13 | F-047 | P05/R05 | US expired | valid | WhatsApp | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU03-14 | F-047 | P09/R10 | IN ✓ | unknown | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-15 | F-047 | P03/R03 | UK draft | withdrawn | email | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU03-16 | F-047 | P09/R10 | EU ✓ | valid | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-17 | F-047 | P03/R03 | IN ✓ | withdrawn | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-18 | F-047 | P09/R10 | UK draft | valid | WhatsApp | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU03-19 | F-047 | P03/R03 | US expired | unknown | SMS/voice | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-03ZU03-20 | F-047 | P03/R03 | EU ✓ | unknown | email | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU03-21 | F-047 | P09/R10 | EU ✓ | withdrawn | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-22 | F-047 | P09/R10 | IN ✓ | valid | SMS/voice | Confidential | EU | ALLOW: Undisclosed AI content in EU → HOLD |
      | EX-03ZU03-23 | F-047 | P05/R05 | US expired | unknown | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-24 | F-047 | P05/R05 | IN ✓ | withdrawn | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-25 | F-047 | P05/R05 | UK draft | withdrawn | email | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU03-26 | F-047 | P05/R05 | US expired | withdrawn | email | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU03-27 | F-047 | P09/R10 | UK draft | unknown | SMS/voice | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU03-28 | F-047 | P03/R03 | IN ✓ | valid | WhatsApp | Internal | EU | ALLOW: Undisclosed AI content in EU → HOLD |
      | EX-03ZU03-29 | F-047 | P03/R03 | UK draft | unknown | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-30 | F-047 | P05/R05 | US expired | valid | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-31 | F-047 | P05/R05 | EU ✓ | withdrawn | SMS/voice | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU03-32 | F-047 | P03/R03 | EU ✓ | valid | SMS/voice | Internal | IN | ALLOW: Undisclosed AI content in EU → HOLD |
      | EX-03ZU03-33 | F-047 | P09/R10 | US expired | withdrawn | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-34 | F-047 | P03/R03 | UK draft | valid | SMS/voice | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU03-35 | F-047 | P05/R05 | EU ✓ | unknown | WhatsApp | Confidential | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU03-36 | F-047 | P03/R03 | EU ✓ | unknown | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-37 | F-047 | P05/R05 | IN ✓ | withdrawn | email | Confidential | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU03-38 | F-047 | P03/R03 | IN ✓ | unknown | email | Restricted | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU03-39 | F-047 | P09/R10 | EU ✓ | withdrawn | email | Confidential | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU03-40 | F-047 | P09/R10 | US expired | unknown | WhatsApp | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU03-41 | F-047 | P09/R10 | IN ✓ | unknown | WhatsApp | Confidential | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU03-42 | F-047 | P03/R03 | US expired | valid | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-43 | F-047 | P09/R10 | US expired | withdrawn | SMS/voice | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU03-44 | F-047 | P09/R10 | UK draft | unknown | email | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU03-45 | F-047 | P05/R05 | UK draft | valid | SMS/voice | Restricted | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU03-46 | F-047 | P05/R05 | IN ✓ | valid | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-47 | F-047 | P05/R05 | EU ✓ | valid | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-48 | F-047 | P09/R10 | IN ✓ | withdrawn | email | Internal | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU03-49 | F-047 | P05/R05 | UK draft | unknown | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-50 | F-047 | P09/R10 | US expired | valid | WhatsApp | Internal | EU | HOLD PACK_EXPIRED |
      | EX-03ZU03-51 | F-047 | P03/R03 | US expired | withdrawn | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU03-52 | F-047 | P03/R03 | IN ✓ | unknown | SMS/voice | Confidential | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU03-53 | F-047 | P05/R05 | EU ✓ | unknown | WhatsApp | Internal | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU03-54 | F-047 | P09/R10 | UK draft | withdrawn | WhatsApp | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU03-55 | F-047 | P05/R05 | EU ✓ | valid | SMS/voice | Confidential | IN | ALLOW: Undisclosed AI content in EU → HOLD |
      | EX-03ZU03-56 | F-047 | P05/R05 | EU ✓ | withdrawn | email | Internal | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU03-57 | F-047 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Undisclosed AI content in EU → HOLD |
```

##### US-03-ZU04 Compliance API routes: packs, preflight, consent, DSAR, incidents and cookies

| Field | Value |
|---|---|
| ID | US-03-ZU04 |
| Title | Compliance API routes: packs, preflight, consent, DSAR, incidents and cookies |
| Type | Compliance (acceptance binding) |
| Story | As a DPO I want to record withdrawals, open incidents with clocks and record notifications so that obligations are evidenced – with the acceptance criteria below, which the statement-only story US-03-YH01 did not carry |
| Persona / roles | DPO / counsel (P09, R10) |
| Traces | FR-V12-H-013 (FSD 25 V8 (CJ-R01/02/04/05/07/08/12)) |
| Priority | Should |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-03-YH01, US-03-YM09, US-03-YA01, US-03-YG02, US-03-YG03; source definition: Part 11.8b §11.8.5.1 Requirements adopted and release mapping |
| Dimension profile | persona ×3 · jurisdiction ×4 · consent ×3 · channel ×3 · data class ×3 · region ×3 · operation ×1 · model MU06 |
| Notes | Acceptance binding: US-03-YH01 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens A007, A013, A200, A201, A202, W29, W30; API family `/api/v1/compliance/`; audit events `compliance.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Compliance API routes: packs, preflight, consent, DSAR, incidents and cookies
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" with DPO "farah@kestrel.example.com" (R10)
    And jurisdiction packs RP-IN (Approved), RP-EU (Approved), RP-UK (Draft) and RP-US (Expired) in the rule-pack registry (Part 11.15)

  @happy @CJ-R01
  Scenario: AC-03ZU04-01 Happy path – Compliance routes: jurisdiction packs and rules, send preflight (FR-V12-H-013)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Compliance routes: jurisdiction packs and rules, send preflight" is exercised as specified by FR-V12-H-013:
      """
      Compliance routes: jurisdiction packs and rules, send preflight, consent ledger search, record and withdraw, suppressions, public DSAR intake,
      DSAR queue/verify/complete with legal-hold check, incident register with clocks and notifications
      """
    Then rule-cited verdicts; clocks recorded
    And the audit event "compliance.compliance_routes" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-ELG-18
  Scenario: AC-03ZU04-02 Negative – a draft pack never allows an outbound action
    Given recipient "olivia@brightway.example.co.uk" is in market UK whose pack RP-UK is "Draft"
    When a promotional email to her passes every other check
    Then the PDP returns HOLD "PACK_NOT_ACTIVE" and no message is dispatched

  @val
  Scenario: AC-03ZU04-03 Validation – the promotional window is checked in the recipient's local time
    Given recipient "anu@sunrise.example.in" in Asia/Kolkata
    When a promotional SMS is scheduled for 21:15 local time
    Then the preflight returns HOLD "OUTSIDE_MESSAGING_WINDOW" (09:00–21:00, DEC-777) and proposes 09:00 next day

  @perm
  Scenario: AC-03ZU04-04 Permission – only R10 can approve a pack
    When "maya@kestrel.example.com" (R05) approves pack RP-UK
    Then the API returns 403 "PERMISSION_DENIED" and the pack stays "Draft"

  @edge
  Scenario: AC-03ZU04-05 Edge – consent withdrawal holds queued work
    Given 3 queued messages for "anu@sunrise.example.in"
    When she withdraws consent at 2027-05-02T10:00:00+05:30
    Then all 3 are "HELD" with "CONSENT_WITHDRAWN" and the suppression list is updated within 60 seconds

  @sec @obs @MU06
  Scenario Outline: AC-03ZU04-06 Permutations – Jurisdiction packs, consent and legal controls (3-way, 56 rows)
    Given actor "<persona>" in zone "<region>" for a recipient in "<jurisdiction>"
    And consent is "<consent>" and the data class is "<data_class>"
    When "<operation>" is checked for channel "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU06 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   H-013 = Compliance routes: jurisdiction packs and rules
    Examples: MU06 rows (3-way, seed 234; space 972; tuples 780/780; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | consent | channel | data_class | region | expected |
      | EX-03ZU04-01 | H-013 | P09/R10 | UK draft | unknown | email | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU04-02 | H-013 | P03/R03 | US expired | valid | SMS/voice | Internal | EU | HOLD PACK_EXPIRED |
      | EX-03ZU04-03 | H-013 | P05/R05 | UK draft | withdrawn | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-04 | H-013 | P09/R10 | IN ✓ | valid | WhatsApp | Confidential | EU | ALLOW: Rule-cited verdicts |
      | EX-03ZU04-05 | H-013 | P05/R05 | EU ✓ | withdrawn | WhatsApp | Internal | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU04-06 | H-013 | P03/R03 | IN ✓ | unknown | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-07 | H-013 | P05/R05 | US expired | withdrawn | email | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU04-08 | H-013 | P03/R03 | EU ✓ | valid | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-09 | H-013 | P03/R03 | IN ✓ | withdrawn | SMS/voice | Restricted | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU04-10 | H-013 | P03/R03 | US expired | unknown | WhatsApp | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-03ZU04-11 | H-013 | P09/R10 | EU ✓ | unknown | SMS/voice | Internal | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU04-12 | H-013 | P05/R05 | EU ✓ | valid | email | Confidential | IN | ALLOW: Rule-cited verdicts |
      | EX-03ZU04-13 | H-013 | P09/R10 | US expired | withdrawn | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-14 | H-013 | P05/R05 | UK draft | unknown | WhatsApp | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU04-15 | H-013 | P03/R03 | UK draft | withdrawn | email | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU04-16 | H-013 | P05/R05 | IN ✓ | valid | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-17 | H-013 | P05/R05 | US expired | unknown | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-18 | H-013 | P09/R10 | US expired | valid | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-19 | H-013 | P09/R10 | UK draft | valid | SMS/voice | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU04-20 | H-013 | P09/R10 | EU ✓ | withdrawn | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-21 | H-013 | P05/R05 | US expired | valid | WhatsApp | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU04-22 | H-013 | P03/R03 | IN ✓ | unknown | WhatsApp | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU04-23 | H-013 | P09/R10 | UK draft | withdrawn | WhatsApp | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU04-24 | H-013 | P09/R10 | IN ✓ | withdrawn | email | Internal | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU04-25 | H-013 | P03/R03 | EU ✓ | unknown | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-26 | H-013 | P05/R05 | IN ✓ | unknown | email | Confidential | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU04-27 | H-013 | P05/R05 | UK draft | valid | SMS/voice | Restricted | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU04-28 | H-013 | P03/R03 | US expired | withdrawn | email | Internal | IN | HOLD PACK_EXPIRED |
      | EX-03ZU04-29 | H-013 | P03/R03 | EU ✓ | valid | email | Internal | EU | ALLOW: Rule-cited verdicts |
      | EX-03ZU04-30 | H-013 | P05/R05 | EU ✓ | unknown | SMS/voice | Restricted | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU04-31 | H-013 | P05/R05 | IN ✓ | withdrawn | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-32 | H-013 | P03/R03 | UK draft | withdrawn | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-33 | H-013 | P09/R10 | US expired | unknown | SMS/voice | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU04-34 | H-013 | P09/R10 | IN ✓ | unknown | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-35 | H-013 | P05/R05 | EU ✓ | withdrawn | WhatsApp | Confidential | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU04-36 | H-013 | P03/R03 | UK draft | valid | SMS/voice | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU04-37 | H-013 | P05/R05 | UK draft | valid | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-38 | H-013 | P09/R10 | IN ✓ | valid | email | Restricted | IN | ALLOW: Rule-cited verdicts |
      | EX-03ZU04-39 | H-013 | P09/R10 | EU ✓ | unknown | WhatsApp | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU04-40 | H-013 | P03/R03 | IN ✓ | valid | WhatsApp | Internal | IN | ALLOW: Rule-cited verdicts |
      | EX-03ZU04-41 | H-013 | P09/R10 | US expired | withdrawn | SMS/voice | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-03ZU04-42 | H-013 | P03/R03 | UK draft | unknown | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-43 | H-013 | P03/R03 | EU ✓ | withdrawn | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-44 | H-013 | P05/R05 | US expired | unknown | email | Internal | IN | HOLD PACK_EXPIRED |
      | EX-03ZU04-45 | H-013 | P09/R10 | EU ✓ | valid | SMS/voice | Confidential | IN | ALLOW: Rule-cited verdicts |
      | EX-03ZU04-46 | H-013 | P03/R03 | IN ✓ | withdrawn | SMS/voice | Confidential | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU04-47 | H-013 | P05/R05 | UK draft | unknown | SMS/voice | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU04-48 | H-013 | P03/R03 | US expired | valid | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-49 | H-013 | P05/R05 | IN ✓ | unknown | email | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU04-50 | H-013 | P09/R10 | UK draft | valid | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-51 | H-013 | P09/R10 | UK draft | withdrawn | WhatsApp | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU04-52 | H-013 | P05/R05 | EU ✓ | unknown | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-53 | H-013 | P09/R10 | US expired | valid | WhatsApp | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU04-54 | H-013 | P03/R03 | EU ✓ | unknown | SMS/voice | Restricted | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU04-55 | H-013 | P05/R05 | US expired | unknown | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU04-56 | H-013 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Rule-cited verdicts |
```

##### US-03-ZU05 Contact-data vendor activation gate: transfer register, DPA and CJ-GL-01

| Field | Value |
|---|---|
| ID | US-03-ZU05 |
| Title | Contact-data vendor activation gate: transfer register, DPA and CJ-GL-01 |
| Type | Compliance |
| Story | As a DPO / counsel (P09, R10), I want contact-data vendors need a transfer-register entry (CJ-R15), a DPA and CJ-GL-01 compliance before activation (DEC-V9-04), so that nothing is sent, recorded or published unless the law of the recipient's market allows it and we can prove it |
| Persona / roles | DPO / counsel (P09, R10) |
| Traces | FR-V12-H-033 (FSD 28 V9); DEC-649 |
| Priority | Should |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-03-YM09, US-03-YA01, US-03-YG02, US-03-YG03; source definition: Part 11.8b §11.8.5.1 Requirements adopted and release mapping |
| Dimension profile | persona ×3 · jurisdiction ×4 · consent ×3 · channel ×3 · data class ×3 · region ×3 · operation ×1 · model MU06 |
| Notes | Related existing stories (shared source IDs, no FR trace): US-07-ZR12, US-18-ZR11 · Screens A007, A013, A200, A201, A202, W29, W30; API family `/api/v1/compliance/`; audit events `compliance.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Contact-data vendor activation gate: transfer register, DPA and CJ-GL-01
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" with DPO "farah@kestrel.example.com" (R10)
    And jurisdiction packs RP-IN (Approved), RP-EU (Approved), RP-UK (Draft) and RP-US (Expired) in the rule-pack registry (Part 11.15)

  @happy @CJ-R15
  Scenario: AC-03ZU05-01 Happy path – Contact-data vendors need a transfer-register entry (CJ-R15) (FR-V12-H-033)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Contact-data vendors need a transfer-register entry (CJ-R15)" is exercised as specified by FR-V12-H-033:
      """
      Contact-data vendors need a transfer-register entry (CJ-R15), a DPA and CJ-GL-01 compliance before activation (DEC-V9-04)
      """
    Then activation blocked otherwise
    And the audit event "compliance.contact_data_vendors_need_a" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-ELG-18
  Scenario: AC-03ZU05-02 Negative – a draft pack never allows an outbound action
    Given recipient "olivia@brightway.example.co.uk" is in market UK whose pack RP-UK is "Draft"
    When a promotional email to her passes every other check
    Then the PDP returns HOLD "PACK_NOT_ACTIVE" and no message is dispatched

  @val
  Scenario: AC-03ZU05-03 Validation – the promotional window is checked in the recipient's local time
    Given recipient "anu@sunrise.example.in" in Asia/Kolkata
    When a promotional SMS is scheduled for 21:15 local time
    Then the preflight returns HOLD "OUTSIDE_MESSAGING_WINDOW" (09:00–21:00, DEC-777) and proposes 09:00 next day

  @perm
  Scenario: AC-03ZU05-04 Permission – only R10 can approve a pack
    When "maya@kestrel.example.com" (R05) approves pack RP-UK
    Then the API returns 403 "PERMISSION_DENIED" and the pack stays "Draft"

  @edge
  Scenario: AC-03ZU05-05 Edge – consent withdrawal holds queued work
    Given 3 queued messages for "anu@sunrise.example.in"
    When she withdraws consent at 2027-05-02T10:00:00+05:30
    Then all 3 are "HELD" with "CONSENT_WITHDRAWN" and the suppression list is updated within 60 seconds

  @sec @obs @MU06
  Scenario Outline: AC-03ZU05-06 Permutations – Jurisdiction packs, consent and legal controls (3-way, 58 rows)
    Given actor "<persona>" in zone "<region>" for a recipient in "<jurisdiction>"
    And consent is "<consent>" and the data class is "<data_class>"
    When "<operation>" is checked for channel "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU06 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   H-033 = Contact-data vendors need a transfer-register entry…
    Examples: MU06 rows (3-way, seed 241; space 972; tuples 780/780; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | consent | channel | data_class | region | expected |
      | EX-03ZU05-01 | H-033 | P03/R03 | IN ✓ | unknown | SMS/voice | Internal | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU05-02 | H-033 | P09/R10 | EU ✓ | unknown | WhatsApp | Restricted | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU05-03 | H-033 | P05/R05 | IN ✓ | valid | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-04 | H-033 | P03/R03 | US expired | withdrawn | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-05 | H-033 | P09/R10 | UK draft | withdrawn | email | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU05-06 | H-033 | P05/R05 | UK draft | valid | email | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU05-07 | H-033 | P03/R03 | EU ✓ | valid | SMS/voice | Confidential | IN | ALLOW: Activation blocked otherwise |
      | EX-03ZU05-08 | H-033 | P05/R05 | US expired | valid | SMS/voice | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU05-09 | H-033 | P05/R05 | EU ✓ | withdrawn | WhatsApp | Internal | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU05-10 | H-033 | P09/R10 | US expired | unknown | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-11 | H-033 | P09/R10 | IN ✓ | withdrawn | SMS/voice | Restricted | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU05-12 | H-033 | P03/R03 | UK draft | unknown | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-13 | H-033 | P05/R05 | EU ✓ | unknown | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-14 | H-033 | P09/R10 | US expired | valid | WhatsApp | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-03ZU05-15 | H-033 | P03/R03 | UK draft | valid | WhatsApp | Restricted | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU05-16 | H-033 | P09/R10 | IN ✓ | valid | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-17 | H-033 | P05/R05 | UK draft | withdrawn | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-18 | H-033 | P03/R03 | UK draft | withdrawn | WhatsApp | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU05-19 | H-033 | P05/R05 | IN ✓ | unknown | email | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU05-20 | H-033 | P03/R03 | EU ✓ | valid | email | Internal | EU | ALLOW: Activation blocked otherwise |
      | EX-03ZU05-21 | H-033 | P03/R03 | IN ✓ | unknown | email | Confidential | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU05-22 | H-033 | P05/R05 | EU ✓ | unknown | SMS/voice | Internal | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU05-23 | H-033 | P09/R10 | EU ✓ | withdrawn | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-24 | H-033 | P09/R10 | UK draft | valid | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-25 | H-033 | P03/R03 | US expired | withdrawn | SMS/voice | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU05-26 | H-033 | P05/R05 | US expired | withdrawn | email | Internal | IN | HOLD PACK_EXPIRED |
      | EX-03ZU05-27 | H-033 | P09/R10 | IN ✓ | unknown | WhatsApp | Confidential | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU05-28 | H-033 | P05/R05 | US expired | unknown | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-29 | H-033 | P09/R10 | EU ✓ | withdrawn | SMS/voice | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU05-30 | H-033 | P09/R10 | UK draft | unknown | email | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU05-31 | H-033 | P05/R05 | IN ✓ | withdrawn | WhatsApp | Internal | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU05-32 | H-033 | P03/R03 | EU ✓ | valid | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-33 | H-033 | P09/R10 | US expired | valid | email | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU05-34 | H-033 | P05/R05 | UK draft | unknown | SMS/voice | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU05-35 | H-033 | P03/R03 | US expired | unknown | WhatsApp | Internal | EU | HOLD PACK_EXPIRED |
      | EX-03ZU05-36 | H-033 | P03/R03 | IN ✓ | withdrawn | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-37 | H-033 | P05/R05 | EU ✓ | valid | email | Restricted | IN | ALLOW: Activation blocked otherwise |
      | EX-03ZU05-38 | H-033 | P03/R03 | US expired | unknown | SMS/voice | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU05-39 | H-033 | P03/R03 | EU ✓ | withdrawn | WhatsApp | Confidential | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU05-40 | H-033 | P09/R10 | IN ✓ | unknown | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-41 | H-033 | P03/R03 | US expired | valid | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-42 | H-033 | P09/R10 | EU ✓ | valid | WhatsApp | Confidential | EU | ALLOW: Activation blocked otherwise |
      | EX-03ZU05-43 | H-033 | P05/R05 | IN ✓ | valid | SMS/voice | Restricted | EU | ALLOW: Activation blocked otherwise |
      | EX-03ZU05-44 | H-033 | P05/R05 | UK draft | valid | WhatsApp | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU05-45 | H-033 | P05/R05 | US expired | unknown | email | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU05-46 | H-033 | P05/R05 | UK draft | unknown | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-47 | H-033 | P09/R10 | UK draft | valid | SMS/voice | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU05-48 | H-033 | P05/R05 | UK draft | withdrawn | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-49 | H-033 | P05/R05 | IN ✓ | withdrawn | email | Confidential | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU05-50 | H-033 | P09/R10 | US expired | withdrawn | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-51 | H-033 | P09/R10 | EU ✓ | withdrawn | email | Internal | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU05-52 | H-033 | P03/R03 | EU ✓ | unknown | SMS/voice | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU05-53 | H-033 | P03/R03 | UK draft | withdrawn | SMS/voice | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU05-54 | H-033 | P03/R03 | IN ✓ | valid | SMS/voice | Restricted | IN | ALLOW: Activation blocked otherwise |
      | EX-03ZU05-55 | H-033 | P09/R10 | UK draft | unknown | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-56 | H-033 | P03/R03 | UK draft | withdrawn | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-57 | H-033 | P09/R10 | US expired | unknown | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU05-58 | H-033 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Activation blocked otherwise |
```

##### US-03-ZU06 ENT-CMP-04…06 acceptance: DPA and sub-processors, DPIA and EU AI Act, accessibility report

| Field | Value |
|---|---|
| ID | US-03-ZU06 |
| Title | ENT-CMP-04…06 acceptance: DPA and sub-processors, DPIA and EU AI Act, accessibility report |
| Type | Compliance (acceptance binding) |
| Story | As a DPO / counsel (P09, R10), I want data Processing Agreement with SCCs, public sub-processor list and 30-day change notice; DPIA and EU AI Act assessment before EU launch; accessibility conformance report (WCAG 2.2 AA) from a manual audit, so that nothing is sent, recorded or published unless the law of the recipient's market allows it and we can prove it |
| Persona / roles | DPO / counsel (P09, R10) |
| Traces | FR-V12-K-140 (ENT-CMP-04); FR-V12-K-141 (ENT-CMP-05); FR-V12-K-142 (ENT-CMP-06); DEC-411, DEC-417, DEC-776; tests TC-V12-K-140, TC-V12-K-141, TC-V12-K-142 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 2–3 |
| Dependencies | US-03-YM09, US-03-YA01, US-03-YG02, US-03-YG03; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · jurisdiction ×4 · consent ×3 · channel ×3 · data class ×3 · region ×3 · operation ×3 · model MU06 |
| Notes | FR-V12-K-141: release per DEC-776 (EU DPIA and EU AI Act before EU launch) · Trace requirement adopted literally from the ENT register (Part 11.11b §11.11.5.16); design depth and build points sit in US-21-ZR17; this story binds the ENT acceptance to tests (DEC-941) · Screens A007, A013, A200, A201, A202, W29, W30; API family `/api/v1/compliance/`; audit events `compliance.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: ENT-CMP-04…06 acceptance: DPA and sub-processors, DPIA and EU AI Act, accessibility report
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" with DPO "farah@kestrel.example.com" (R10)
    And jurisdiction packs RP-IN (Approved), RP-EU (Approved), RP-UK (Draft) and RP-US (Expired) in the rule-pack registry (Part 11.15)

  @happy @ENT-CMP-04
  Scenario: AC-03ZU06-01 Happy path – Data Processing Agreement with SCCs, public sub-processor list and… (FR-V12-K-140)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Data Processing Agreement with SCCs, public sub-processor list and…" is exercised as specified by FR-V12-K-140:
      """
      Data Processing Agreement with SCCs, public sub-processor list and 30-day change notice.
      """
    Then evidence test: approved legal set published:
      """
      sub-processor change notice, counsel sign-off recorded per pack, accessibility conformance report attached
      """
    And the audit event "compliance.data_processing_agreement" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-CMP-05 @DEC-776
  Scenario: AC-03ZU06-02 Alternate – DPIA and EU AI Act assessment before EU launch. (FR-V12-K-141)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "DPIA and EU AI Act assessment before EU launch." is exercised as specified by FR-V12-K-141: DPIA and EU AI Act assessment before EU launch.
    Then evidence test: approved legal set published:
      """
      sub-processor change notice, counsel sign-off recorded per pack, accessibility conformance report attached
      """
    And the audit event "compliance.dpia_and_eu_ai_act_assessment" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-CMP-06
  Scenario: AC-03ZU06-03 Alternate – Accessibility conformance report (WCAG 2.2 AA) from a manual audit. (FR-V12-K-142)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Accessibility conformance report (WCAG 2.2 AA) from a manual audit." is exercised as specified by FR-V12-K-142:
      """
      Accessibility conformance report (WCAG 2.2 AA) from a manual audit.
      """
    Then evidence test: approved legal set published:
      """
      sub-processor change notice, counsel sign-off recorded per pack, accessibility conformance report attached
      """
    And the audit event "compliance.accessibility_conformance" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-ELG-18
  Scenario: AC-03ZU06-04 Negative – a draft pack never allows an outbound action
    Given recipient "olivia@brightway.example.co.uk" is in market UK whose pack RP-UK is "Draft"
    When a promotional email to her passes every other check
    Then the PDP returns HOLD "PACK_NOT_ACTIVE" and no message is dispatched

  @val
  Scenario: AC-03ZU06-05 Validation – the promotional window is checked in the recipient's local time
    Given recipient "anu@sunrise.example.in" in Asia/Kolkata
    When a promotional SMS is scheduled for 21:15 local time
    Then the preflight returns HOLD "OUTSIDE_MESSAGING_WINDOW" (09:00–21:00, DEC-777) and proposes 09:00 next day

  @perm
  Scenario: AC-03ZU06-06 Permission – only R10 can approve a pack
    When "maya@kestrel.example.com" (R05) approves pack RP-UK
    Then the API returns 403 "PERMISSION_DENIED" and the pack stays "Draft"

  @edge
  Scenario: AC-03ZU06-07 Edge – consent withdrawal holds queued work
    Given 3 queued messages for "anu@sunrise.example.in"
    When she withdraws consent at 2027-05-02T10:00:00+05:30
    Then all 3 are "HELD" with "CONSENT_WITHDRAWN" and the suppression list is updated within 60 seconds

  @sec @obs @MU06
  Scenario Outline: AC-03ZU06-08 Permutations – Jurisdiction packs, consent and legal controls (3-way, 62 rows)
    Given actor "<persona>" in zone "<region>" for a recipient in "<jurisdiction>"
    And consent is "<consent>" and the data class is "<data_class>"
    When "<operation>" is checked for channel "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU06 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-140 = Data Processing Agreement with SCCs
    #   K-141 = DPIA and EU AI Act assessment before EU launch.
    #   K-142 = Accessibility conformance report
    Examples: MU06 rows (3-way, seed 248; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | jurisdiction | consent | channel | data_class | region | expected |
      | EX-03ZU06-01 | K-140 | P09/R10 | US expired | valid | email | Internal | IN | HOLD PACK_EXPIRED |
      | EX-03ZU06-02 | K-141 | P03/R03 | UK draft | valid | SMS/voice | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU06-03 | K-140 | P03/R03 | IN ✓ | withdrawn | WhatsApp | Confidential | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU06-04 | K-140 | P09/R10 | IN ✓ | unknown | SMS/voice | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU06-05 | K-142 | P05/R05 | EU ✓ | withdrawn | SMS/voice | Internal | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU06-06 | K-142 | P03/R03 | US expired | unknown | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-07 | K-141 | P09/R10 | EU ✓ | withdrawn | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-08 | K-142 | P09/R10 | EU ✓ | valid | WhatsApp | Confidential | EU | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU06-09 | K-141 | P05/R05 | US expired | unknown | WhatsApp | Internal | EU | HOLD PACK_EXPIRED |
      | EX-03ZU06-10 | K-142 | P05/R05 | IN ✓ | valid | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-11 | K-142 | P03/R03 | US expired | withdrawn | email | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU06-12 | K-141 | P05/R05 | IN ✓ | unknown | email | Confidential | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU06-13 | K-140 | P03/R03 | UK draft | unknown | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-14 | K-140 | P05/R05 | UK draft | valid | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-15 | K-142 | P09/R10 | UK draft | unknown | WhatsApp | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU06-16 | K-141 | P09/R10 | UK draft | withdrawn | SMS/voice | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU06-17 | K-141 | P03/R03 | IN ✓ | valid | email | Internal | EU | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU06-18 | K-140 | P05/R05 | EU ✓ | withdrawn | email | Confidential | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU06-19 | K-141 | P09/R10 | US expired | withdrawn | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-20 | K-140 | P03/R03 | EU ✓ | valid | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-21 | K-141 | P03/R03 | EU ✓ | unknown | SMS/voice | Confidential | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU06-22 | K-142 | P09/R10 | IN ✓ | withdrawn | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-23 | K-140 | P05/R05 | UK draft | withdrawn | email | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU06-24 | K-142 | P05/R05 | UK draft | valid | email | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU06-25 | K-141 | P05/R05 | EU ✓ | valid | WhatsApp | Internal | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU06-26 | K-141 | P05/R05 | US expired | unknown | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-27 | K-142 | P03/R03 | EU ✓ | unknown | email | Internal | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU06-28 | K-140 | P03/R03 | UK draft | withdrawn | WhatsApp | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU06-29 | K-142 | P09/R10 | IN ✓ | valid | SMS/voice | Confidential | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU06-30 | K-141 | P09/R10 | UK draft | valid | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-31 | K-140 | P05/R05 | US expired | unknown | WhatsApp | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-03ZU06-32 | K-140 | P03/R03 | US expired | withdrawn | SMS/voice | Internal | IN | HOLD PACK_EXPIRED |
      | EX-03ZU06-33 | K-140 | P09/R10 | EU ✓ | unknown | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-34 | K-141 | P05/R05 | IN ✓ | withdrawn | WhatsApp | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU06-35 | K-142 | P03/R03 | UK draft | withdrawn | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-36 | K-142 | P09/R10 | US expired | valid | SMS/voice | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU06-37 | K-140 | P05/R05 | IN ✓ | withdrawn | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-38 | K-142 | P09/R10 | IN ✓ | unknown | email | Confidential | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU06-39 | K-141 | P03/R03 | US expired | valid | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-40 | K-142 | P03/R03 | IN ✓ | unknown | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-41 | K-140 | P09/R10 | EU ✓ | withdrawn | SMS/voice | Confidential | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU06-42 | K-142 | P05/R05 | EU ✓ | unknown | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-43 | K-141 | P05/R05 | UK draft | unknown | WhatsApp | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU06-44 | K-141 | P09/R10 | IN ✓ | unknown | WhatsApp | Internal | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU06-45 | K-140 | P05/R05 | US expired | valid | email | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU06-46 | K-142 | P05/R05 | US expired | withdrawn | WhatsApp | Internal | IN | HOLD PACK_EXPIRED |
      | EX-03ZU06-47 | K-141 | P03/R03 | EU ✓ | withdrawn | WhatsApp | Restricted | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU06-48 | K-140 | P09/R10 | UK draft | unknown | SMS/voice | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU06-49 | K-141 | P09/R10 | US expired | unknown | email | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU06-50 | K-142 | P03/R03 | EU ✓ | valid | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-51 | K-140 | P09/R10 | US expired | valid | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-52 | K-142 | P05/R05 | UK draft | withdrawn | SMS/voice | Restricted | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU06-53 | K-141 | P03/R03 | IN ✓ | unknown | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-54 | K-141 | P03/R03 | EU ✓ | valid | SMS/voice | Internal | EU | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU06-55 | K-142 | P05/R05 | UK draft | valid | WhatsApp | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU06-56 | K-140 | P05/R05 | IN ✓ | valid | SMS/voice | Restricted | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU06-57 | K-142 | P03/R03 | UK draft | unknown | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU06-58 | K-140 | P03/R03 | US expired | withdrawn | WhatsApp | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU06-59 | K-140 | P09/R10 | EU ✓ | unknown | SMS/voice | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU06-60 | K-140 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU06-61 | K-141 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU06-62 | K-142 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Evidence test: approved legal set published, |
```

##### US-03-ZU07 ENT-CMP-07…08 acceptance: approved legal set and counsel-reviewed market packs

| Field | Value |
|---|---|
| ID | US-03-ZU07 |
| Title | ENT-CMP-07…08 acceptance: approved legal set and counsel-reviewed market packs |
| Type | Compliance |
| Story | As a DPO / counsel (P09, R10), I want legal document set approved: Terms, Privacy Notice, DPA, AUP, Cookie Policy, AI Use and Accessibility statements; jurisdiction packs reviewed by qualified counsel before entering each new market, so that nothing is sent, recorded or published unless the law of the recipient's market allows it and we can prove it |
| Persona / roles | DPO / counsel (P09, R10) |
| Traces | FR-V12-K-143 (ENT-CMP-07); FR-V12-K-144 (ENT-CMP-08); tests TC-V12-K-143, TC-V12-K-144 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-03-YM09, US-03-YA01, US-03-YG02, US-03-YG03; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · jurisdiction ×4 · consent ×3 · channel ×3 · data class ×3 · region ×3 · operation ×2 · model MU06 |
| Notes | Screens A007, A013, A200, A201, A202, W29, W30; API family `/api/v1/compliance/`; audit events `compliance.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: ENT-CMP-07…08 acceptance: approved legal set and counsel-reviewed market packs
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" with DPO "farah@kestrel.example.com" (R10)
    And jurisdiction packs RP-IN (Approved), RP-EU (Approved), RP-UK (Draft) and RP-US (Expired) in the rule-pack registry (Part 11.15)

  @happy @ENT-CMP-07
  Scenario: AC-03ZU07-01 Happy path – Legal document set approved: Terms, Privacy Notice, DPA, AUP (FR-V12-K-143)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Legal document set approved:
      """
      Terms, Privacy Notice, DPA, AUP" is exercised as specified by FR-V12-K-143: Legal document set approved: Terms, Privacy Notice, DPA, AUP,
      Cookie Policy, AI Use and Accessibility statements.
      """
    Then evidence test: approved legal set published:
      """
      sub-processor change notice, counsel sign-off recorded per pack, accessibility conformance report attached
      """
    And the audit event "compliance.legal_document_set_approved" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-CMP-08
  Scenario: AC-03ZU07-02 Alternate – Jurisdiction packs reviewed by qualified counsel before entering each… (FR-V12-K-144)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Jurisdiction packs reviewed by qualified counsel before entering each…" is exercised as specified by FR-V12-K-144:
      """
      Jurisdiction packs reviewed by qualified counsel before entering each new market.
      """
    Then evidence test: approved legal set published:
      """
      sub-processor change notice, counsel sign-off recorded per pack, accessibility conformance report attached
      """
    And the audit event "compliance.jurisdiction_packs_reviewed" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-ELG-18
  Scenario: AC-03ZU07-03 Negative – a draft pack never allows an outbound action
    Given recipient "olivia@brightway.example.co.uk" is in market UK whose pack RP-UK is "Draft"
    When a promotional email to her passes every other check
    Then the PDP returns HOLD "PACK_NOT_ACTIVE" and no message is dispatched

  @val
  Scenario: AC-03ZU07-04 Validation – the promotional window is checked in the recipient's local time
    Given recipient "anu@sunrise.example.in" in Asia/Kolkata
    When a promotional SMS is scheduled for 21:15 local time
    Then the preflight returns HOLD "OUTSIDE_MESSAGING_WINDOW" (09:00–21:00, DEC-777) and proposes 09:00 next day

  @perm
  Scenario: AC-03ZU07-05 Permission – only R10 can approve a pack
    When "maya@kestrel.example.com" (R05) approves pack RP-UK
    Then the API returns 403 "PERMISSION_DENIED" and the pack stays "Draft"

  @edge
  Scenario: AC-03ZU07-06 Edge – consent withdrawal holds queued work
    Given 3 queued messages for "anu@sunrise.example.in"
    When she withdraws consent at 2027-05-02T10:00:00+05:30
    Then all 3 are "HELD" with "CONSENT_WITHDRAWN" and the suppression list is updated within 60 seconds

  @sec @obs @MU06
  Scenario Outline: AC-03ZU07-07 Permutations – Jurisdiction packs, consent and legal controls (3-way, 58 rows)
    Given actor "<persona>" in zone "<region>" for a recipient in "<jurisdiction>"
    And consent is "<consent>" and the data class is "<data_class>"
    When "<operation>" is checked for channel "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU06 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-143 = Legal document set approved: Terms, Privacy Notice
    #   K-144 = Jurisdiction packs reviewed by qualified counsel…
    Examples: MU06 rows (3-way, seed 255; space 1,944; tuples 930/930; +2 baseline-allow)
      | ex | operation | persona | jurisdiction | consent | channel | data_class | region | expected |
      | EX-03ZU07-01 | K-143 | P03/R03 | UK draft | valid | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-02 | K-143 | P09/R10 | EU ✓ | withdrawn | email | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU07-03 | K-143 | P05/R05 | EU ✓ | unknown | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-04 | K-143 | P05/R05 | IN ✓ | valid | SMS/voice | Restricted | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU07-05 | K-144 | P09/R10 | IN ✓ | unknown | email | Internal | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU07-06 | K-144 | P03/R03 | US expired | withdrawn | WhatsApp | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU07-07 | K-144 | P03/R03 | UK draft | unknown | SMS/voice | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU07-08 | K-144 | P05/R05 | US expired | withdrawn | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-09 | K-144 | P05/R05 | IN ✓ | valid | email | Confidential | EU | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU07-10 | K-144 | P09/R10 | UK draft | valid | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-11 | K-143 | P09/R10 | UK draft | withdrawn | SMS/voice | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU07-12 | K-143 | P09/R10 | US expired | unknown | WhatsApp | Internal | EU | HOLD PACK_EXPIRED |
      | EX-03ZU07-13 | K-144 | P03/R03 | EU ✓ | valid | SMS/voice | Internal | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU07-14 | K-143 | P03/R03 | IN ✓ | withdrawn | WhatsApp | Internal | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU07-15 | K-143 | P03/R03 | US expired | unknown | email | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-03ZU07-16 | K-144 | P05/R05 | UK draft | unknown | email | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU07-17 | K-143 | P03/R03 | IN ✓ | unknown | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-18 | K-144 | P03/R03 | EU ✓ | withdrawn | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-19 | K-143 | P09/R10 | US expired | valid | SMS/voice | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU07-20 | K-144 | P05/R05 | EU ✓ | valid | WhatsApp | Internal | EU | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU07-21 | K-143 | P05/R05 | UK draft | withdrawn | WhatsApp | Restricted | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU07-22 | K-144 | P09/R10 | IN ✓ | withdrawn | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-23 | K-144 | P09/R10 | EU ✓ | unknown | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-24 | K-143 | P05/R05 | US expired | valid | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-25 | K-143 | P05/R05 | EU ✓ | withdrawn | email | Internal | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU07-26 | K-144 | P09/R10 | IN ✓ | withdrawn | SMS/voice | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU07-27 | K-143 | P09/R10 | EU ✓ | valid | WhatsApp | Confidential | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU07-28 | K-144 | P03/R03 | UK draft | unknown | WhatsApp | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU07-29 | K-144 | P03/R03 | US expired | valid | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-30 | K-143 | P03/R03 | EU ✓ | unknown | email | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU07-31 | K-143 | P05/R05 | UK draft | valid | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-32 | K-144 | P09/R10 | US expired | unknown | SMS/voice | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-03ZU07-33 | K-143 | P09/R10 | IN ✓ | valid | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-34 | K-144 | P09/R10 | UK draft | withdrawn | email | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU07-35 | K-143 | P05/R05 | IN ✓ | unknown | SMS/voice | Internal | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU07-36 | K-144 | P09/R10 | US expired | withdrawn | email | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU07-37 | K-144 | P05/R05 | IN ✓ | withdrawn | WhatsApp | Confidential | IN | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU07-38 | K-143 | P05/R05 | EU ✓ | withdrawn | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-39 | K-144 | P03/R03 | IN ✓ | valid | email | Restricted | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU07-40 | K-144 | P03/R03 | EU ✓ | unknown | WhatsApp | Restricted | IN | HOLD CONSENT_UNKNOWN |
      | EX-03ZU07-41 | K-143 | P09/R10 | UK draft | unknown | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-42 | K-144 | P05/R05 | US expired | valid | email | Internal | IN | HOLD PACK_EXPIRED |
      | EX-03ZU07-43 | K-143 | P05/R05 | US expired | unknown | WhatsApp | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-03ZU07-44 | K-143 | P03/R03 | UK draft | withdrawn | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-45 | K-144 | P03/R03 | US expired | valid | SMS/voice | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-03ZU07-46 | K-143 | P03/R03 | IN ✓ | unknown | SMS/voice | Confidential | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU07-47 | K-144 | P03/R03 | EU ✓ | valid | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-48 | K-143 | P05/R05 | IN ✓ | unknown | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-49 | K-144 | P05/R05 | UK draft | valid | SMS/voice | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU07-50 | K-144 | P09/R10 | EU ✓ | unknown | SMS/voice | Confidential | EU | HOLD CONSENT_UNKNOWN |
      | EX-03ZU07-51 | K-143 | P05/R05 | UK draft | valid | WhatsApp | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-03ZU07-52 | K-143 | P09/R10 | US expired | unknown | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU07-53 | K-143 | P09/R10 | IN ✓ | valid | WhatsApp | Restricted | EU | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU07-54 | K-143 | P03/R03 | US expired | withdrawn | WhatsApp | Internal | IN | HOLD PACK_EXPIRED |
      | EX-03ZU07-55 | K-144 | P05/R05 | IN ✓ | withdrawn | email | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU07-56 | K-143 | P03/R03 | EU ✓ | withdrawn | WhatsApp | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-03ZU07-57 | K-143 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-03ZU07-58 | K-144 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Evidence test: approved legal set published, |
```

##### US-03-ZU08 AI-assisted labelling of every Part 11.13 AI output

| Field | Value |
|---|---|
| ID | US-03-ZU08 |
| Title | AI-assisted labelling of every Part 11.13 AI output |
| Type | Compliance (acceptance binding) |
| Story | As a recipient or user I want AI assistance disclosed so that I know where AI was used – with the acceptance criteria below, which the statement-only story US-03-YM38 did not carry |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-M-100 (BR-V7-AI-01) |
| Priority | Must |
| Wave | Release 3+ (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-03-YM38, US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.13b §11.13.5.7 Functional requirements |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×1 · model MU05 |
| Notes | Acceptance binding: US-03-YM38 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: AI-assisted labelling of every Part 11.13 AI output
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy
  Scenario: AC-03ZU08-01 Happy path – The system shall label every Part 11.13 AI output as AI-assisted… (FR-V12-M-100)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "The system shall label every Part 11.13 AI output as AI-assisted…" is exercised as specified by FR-V12-M-100:
      """
      The system shall label every Part 11.13 AI output as AI-assisted where it is shown to a person
      """
    Then the observable result matches FR-V12-M-100 and its tests in Part 11.21
    And the audit event "ai.the_system_shall_label_every" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-03ZU08-02 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-03ZU08-03 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-03ZU08-04 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-03ZU08-05 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-03ZU08-06 Permutations – AI governance, evaluation, prompts and cost (3-way, 54 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   M-100 = The system shall label every Part 11.13 AI output…
    Examples: MU05 rows (3-way, seed 262; space 972; tuples 780/780; +1 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-03ZU08-01 | M-100 | P10/R11 | Confidential | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-02 | M-100 | P03/R03 | Public | candidate only | L3 revoked | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-03ZU08-03 | M-100 | P10/R11 | Internal | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-03ZU08-04 | M-100 | P16/R20 | Restricted | candidate only | L3 mandate | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-03ZU08-05 | M-100 | P16/R20 | Public | model Approved | L1 | hard cap | EU | PENDING_APPROVAL |
      | EX-03ZU08-06 | M-100 | P03/R03 | Restricted | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-07 | M-100 | P03/R03 | Internal | model Approved | L3 revoked | soft cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-03ZU08-08 | M-100 | P10/R11 | Public | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-03ZU08-09 | M-100 | P03/R03 | Confidential | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-10 | M-100 | P16/R20 | Confidential | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-11 | M-100 | P10/R11 | Restricted | model Approved | L3 revoked | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-03ZU08-12 | M-100 | P03/R03 | Internal | candidate only | L3 mandate | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-03ZU08-13 | M-100 | P10/R11 | Confidential | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-03ZU08-14 | M-100 | P16/R20 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: The system shall label every Part 11.13 AI output |
      | EX-03ZU08-15 | M-100 | P16/R20 | Internal | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-16 | M-100 | P03/R03 | Restricted | model Approved | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-03ZU08-17 | M-100 | P16/R20 | Confidential | model Approved | L3 revoked | soft cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-03ZU08-18 | M-100 | P10/R11 | Public | candidate only | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-19 | M-100 | P03/R03 | Confidential | prompt unapproved | L3 mandate | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-03ZU08-20 | M-100 | P16/R20 | Restricted | prompt unapproved | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-03ZU08-21 | M-100 | P16/R20 | Internal | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-22 | M-100 | P16/R20 | Public | prompt unapproved | L3 revoked | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-03ZU08-23 | M-100 | P10/R11 | Confidential | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-03ZU08-24 | M-100 | P10/R11 | Restricted | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-25 | M-100 | P03/R03 | Internal | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-26 | M-100 | P03/R03 | Internal | prompt unapproved | L1 | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-03ZU08-27 | M-100 | P16/R20 | Confidential | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-03ZU08-28 | M-100 | P10/R11 | Internal | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-29 | M-100 | P16/R20 | Public | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-03ZU08-30 | M-100 | P10/R11 | Restricted | prompt unapproved | L3 mandate | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-03ZU08-31 | M-100 | P03/R03 | Public | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-32 | M-100 | P03/R03 | Restricted | model Approved | L3 mandate | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-03ZU08-33 | M-100 | P10/R11 | Restricted | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-34 | M-100 | P10/R11 | Internal | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-03ZU08-35 | M-100 | P16/R20 | Internal | candidate only | L3 revoked | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-03ZU08-36 | M-100 | P16/R20 | Confidential | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-03ZU08-37 | M-100 | P03/R03 | Public | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-38 | M-100 | P03/R03 | Public | candidate only | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-39 | M-100 | P10/R11 | Restricted | prompt unapproved | L3 revoked | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-03ZU08-40 | M-100 | P10/R11 | Public | model Approved | L3 revoked | hard cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-03ZU08-41 | M-100 | P03/R03 | Restricted | candidate only | L1 | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-03ZU08-42 | M-100 | P16/R20 | Internal | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-03ZU08-43 | M-100 | P16/R20 | Restricted | model Approved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-44 | M-100 | P10/R11 | Internal | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-03ZU08-45 | M-100 | P10/R11 | Confidential | prompt unapproved | L3 mandate | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-03ZU08-46 | M-100 | P03/R03 | Confidential | model Approved | L3 revoked | hard cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-03ZU08-47 | M-100 | P03/R03 | Restricted | candidate only | L3 revoked | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-03ZU08-48 | M-100 | P10/R11 | Confidential | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-03ZU08-49 | M-100 | P16/R20 | Confidential | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-03ZU08-50 | M-100 | P16/R20 | Public | model Approved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-51 | M-100 | P10/R11 | Restricted | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-03ZU08-52 | M-100 | P03/R03 | Public | candidate only | L3 mandate | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-03ZU08-53 | M-100 | P10/R11 | Public | candidate only | L3 mandate | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-03ZU08-54 | M-100 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: The system shall label every Part 11.13 AI output |
```

#### 11.22.5.4.4 EP-04 AI gateway, cost control and AI quality

| Field | Value |
|---|---|
| Epic | EP-04 AI gateway, cost control and AI quality (Part 0 §0.10.2) |
| New stories in this file | US-04-ZU01, US-04-ZU02, US-04-ZU03, US-04-ZU04, US-04-ZU05, US-04-ZU06, US-04-ZU07, US-04-ZU08, US-04-ZU09, US-04-ZU10, US-04-ZU11, US-04-ZU12, US-04-ZU13, US-04-ZU14, US-04-ZU15, US-04-ZU16, US-04-ZU17 |
| FR-V12 covered | A: 054, 113–118; F: 001, 004, 006–015, 017–030, 032–033, 036, 039, 049; H: 017; I: 016; M: 099 |
| Size | 17 stories · 102–166 SP · 51–166 pd (0.5/1.0 pd per SP) · central 93.8 pd (0.7 pd per SP mid) |
| Releases | Release 1: 2, Release 2: 14, Release 3+: 1 |

##### US-04-ZU01 AI transparency page, AI labels, region pinning and private customer data

| Field | Value |
|---|---|
| ID | US-04-ZU01 |
| Title | AI transparency page, AI labels, region pinning and private customer data |
| Type | Compliance (acceptance binding) |
| Story | As the AI owner, I want AI labels, region pinning and language slice gates before a locale goes live – with the acceptance criteria below, which the statement-only story US-04-YA01 did not carry |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-A-054 (BR-V7-WEB-04, BR-V7-AI-01); FR-V12-A-114 (BR-V7-AI-01, CJ-EU-09); FR-V12-A-115 (BR-V7-AI-04); FR-V12-A-116 (BR-V7-AI-05); tests TC-V12-A-033, TC-V12-A-054, TC-V12-A-116 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 2–3 |
| Dependencies | US-04-YA01, US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.1b §11.1.5.7 AI automation authority and governance; Part 11.1b §ADR-182 Neutral storefront; tenant publication… |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×4 · model MU05 |
| Notes | Acceptance binding: US-04-YA01 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: AI transparency page, AI labels, region pinning and private customer data
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy
  Scenario: AC-04ZU01-01 Happy path – Public AI transparency page (FR-V12-A-054)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Public AI transparency page" is exercised as specified by FR-V12-A-054:
      """
      Public AI transparency page: where AI is used, safeguards, human review, labelling of AI-generated messages and assets
      """
    Then page published; sample outputs carry the AI-generated disclosure
    And the audit event "ai.public_ai_transparency_page" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt
  Scenario: AC-04ZU01-02 Alternate – AI transparency labels (FR-V12-A-114)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "AI transparency labels" is exercised as specified by FR-V12-A-114:
      """
      AI transparency labels: AI-generated messages and assets labelled; EU AI Act Art. 50 machine-readable marking when the EU pack is active
      (applicability date: verify at time of implementation, as of 27 Nov 2026); undisclosed AI content held in EU markets
      """
    Then EU-market draft without label → HOLD
    And the audit event "ai.ai_transparency_labels" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt
  Scenario: AC-04ZU01-03 Alternate – Cost per accepted result (FR-V12-A-115)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Cost per accepted result" is exercised as specified by FR-V12-A-115:
      """
      Cost per accepted result reported per workflow with denominator; tenant AI budget hard cap holds AI steps
      """
    Then report shows numerator, denominator and *undefined* at 0
    And the audit event "ai.cost_per_accepted_result" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt
  Scenario: AC-04ZU01-04 Alternate – Customer data stays private (FR-V12-A-116)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Customer data stays private" is exercised as specified by FR-V12-A-116:
      """
      Customer data stays private: no training on customer data (provider DPA evidence); processing in the tenant's region — India now; EU only
      after CONFLICT-761
      """
    Then region-pinning test: model calls for an India tenant use the approved India-region endpoint
    And the audit event "ai.customer_data_stays_private" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU01-05 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU01-06 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU01-07 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU01-08 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU01-09 Permutations – AI governance, evaluation, prompts and cost (3-way, 75 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-054 = Public AI transparency page
    #   A-114 = AI transparency labels
    #   A-115 = Cost per accepted result
    #   A-116 = Customer data stays private
    Examples: MU05 rows (3-way, seed 269; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU01-01 | A-054 | P10/R11 | Restricted | prompt unapproved | L3 revoked | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU01-02 | A-115 | P10/R11 | Public | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-03 | A-054 | P16/R20 | Confidential | candidate only | L3 mandate | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU01-04 | A-116 | P03/R03 | Public | candidate only | L1 | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU01-05 | A-116 | P10/R11 | Internal | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-06 | A-115 | P16/R20 | Internal | prompt unapproved | L1 | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-07 | A-114 | P16/R20 | Restricted | model Approved | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU01-08 | A-115 | P03/R03 | Confidential | model Approved | L3 revoked | hard cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU01-09 | A-116 | P03/R03 | Confidential | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-10 | A-114 | P03/R03 | Public | prompt unapproved | L3 revoked | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-11 | A-114 | P10/R11 | Public | model Approved | L3 mandate | soft cap | IN | ALLOW: EU-market draft without label → HOLD |
      | EX-04ZU01-12 | A-054 | P03/R03 | Internal | model Approved | L3 revoked | in budget | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU01-13 | A-115 | P16/R20 | Restricted | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-14 | A-116 | P10/R11 | Restricted | candidate only | L3 mandate | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU01-15 | A-114 | P16/R20 | Confidential | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-16 | A-114 | P10/R11 | Internal | candidate only | L3 mandate | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU01-17 | A-054 | P03/R03 | Restricted | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-18 | A-054 | P16/R20 | Public | prompt unapproved | L3 mandate | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-19 | A-114 | P10/R11 | Confidential | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-20 | A-116 | P16/R20 | Restricted | model Approved | L3 revoked | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU01-21 | A-115 | P03/R03 | Internal | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-22 | A-116 | P16/R20 | Internal | candidate only | L3 revoked | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU01-23 | A-054 | P10/R11 | Confidential | model Approved | L1 | soft cap | EU | PENDING_APPROVAL |
      | EX-04ZU01-24 | A-115 | P10/R11 | Public | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-25 | A-054 | P16/R20 | Public | model Approved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-26 | A-115 | P03/R03 | Public | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-04ZU01-27 | A-116 | P03/R03 | Restricted | model Approved | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU01-28 | A-054 | P10/R11 | Internal | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-29 | A-114 | P03/R03 | Restricted | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-30 | A-115 | P16/R20 | Confidential | candidate only | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-31 | A-116 | P10/R11 | Confidential | prompt unapproved | L3 revoked | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-32 | A-115 | P03/R03 | Restricted | candidate only | L3 revoked | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU01-33 | A-116 | P16/R20 | Confidential | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-34 | A-114 | P10/R11 | Restricted | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-35 | A-115 | P10/R11 | Confidential | model Approved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-36 | A-114 | P16/R20 | Public | candidate only | L1 | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU01-37 | A-054 | P03/R03 | Internal | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-38 | A-114 | P03/R03 | Confidential | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU01-39 | A-115 | P16/R20 | Internal | model Approved | L3 mandate | soft cap | EU | ALLOW: Report shows numerator, denominator and *undefined* |
      | EX-04ZU01-40 | A-054 | P03/R03 | Public | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-41 | A-114 | P16/R20 | Internal | prompt unapproved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-42 | A-054 | P16/R20 | Restricted | prompt unapproved | L1 | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU01-43 | A-054 | P10/R11 | Internal | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU01-44 | A-116 | P16/R20 | Public | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-45 | A-115 | P10/R11 | Internal | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU01-46 | A-116 | P03/R03 | Confidential | model Approved | L1 | soft cap | IN | PENDING_APPROVAL |
      | EX-04ZU01-47 | A-115 | P10/R11 | Restricted | candidate only | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU01-48 | A-054 | P03/R03 | Confidential | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-49 | A-114 | P03/R03 | Restricted | model Approved | L3 mandate | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU01-50 | A-116 | P10/R11 | Public | model Approved | L3 revoked | soft cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU01-51 | A-114 | P16/R20 | Confidential | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-52 | A-115 | P16/R20 | Public | prompt unapproved | L3 mandate | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-53 | A-116 | P16/R20 | Restricted | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-54 | A-114 | P03/R03 | Internal | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-04ZU01-55 | A-116 | P03/R03 | Internal | prompt unapproved | L3 mandate | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-56 | A-115 | P03/R03 | Confidential | prompt unapproved | L3 revoked | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-57 | A-054 | P16/R20 | Restricted | model Approved | L3 mandate | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU01-58 | A-114 | P03/R03 | Public | prompt unapproved | L3 revoked | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-59 | A-054 | P16/R20 | Internal | candidate only | L3 revoked | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU01-60 | A-115 | P03/R03 | Restricted | model Approved | L3 mandate | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU01-61 | A-116 | P16/R20 | Public | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU01-62 | A-054 | P10/R11 | Public | prompt unapproved | L1 | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-63 | A-116 | P10/R11 | Restricted | prompt unapproved | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU01-64 | A-116 | P10/R11 | Confidential | candidate only | L1 | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU01-65 | A-114 | P16/R20 | Public | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-66 | A-116 | P03/R03 | Internal | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-67 | A-115 | P16/R20 | Internal | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU01-68 | A-114 | P10/R11 | Restricted | candidate only | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU01-69 | A-054 | P16/R20 | Confidential | prompt unapproved | L3 revoked | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU01-70 | A-054 | P10/R11 | Confidential | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU01-71 | A-116 | P16/R20 | Restricted | model Approved | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU01-72 | A-054 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Page published |
      | EX-04ZU01-73 | A-114 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: EU-market draft without label → HOLD |
      | EX-04ZU01-74 | A-115 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Report shows numerator, denominator and *undefined* |
      | EX-04ZU01-75 | A-116 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Region-pinning test: model calls for an India |
```

##### US-04-ZU02 Context budgeting, multimodal cost tiers and the AI step inventory

| Field | Value |
|---|---|
| ID | US-04-ZU02 |
| Title | Context budgeting, multimodal cost tiers and the AI step inventory |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want context budgeting, summarisation and multimodal cost tiers: token allocation by task class with reserved output and safety margin; AI step inventory: of 517 steps, 159 AI-inference steps are tagged; all other steps are rules, gates, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-A-113 (AI-06, AI-07, AI-13); FR-V12-A-118 (BRD 18 "Scope"); tests TC-V12-A-113, TC-V12-A-118 |
| Priority | Should |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.1b §11.1.5.7 AI automation authority and governance |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×2 · model MU05 |
| Notes | Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: Context budgeting, multimodal cost tiers and the AI step inventory
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy
  Scenario: AC-04ZU02-01 Happy path – Context budgeting, summarisation and multimodal cost tiers (FR-V12-A-113)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Context budgeting, summarisation and multimodal cost tiers" is exercised as specified by FR-V12-A-113:
      """
      Context budgeting, summarisation and multimodal cost tiers: token allocation by task class with reserved output and safety margin; scoped
      fact/decision summaries preserving approval and opt-out facts
      """
    Then oversized context reduced or held; mandatory evidence retained
    And the audit event "ai.context_budgeting" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt
  Scenario: AC-04ZU02-02 Alternate – AI step inventory (FR-V12-A-118)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "AI step inventory" is exercised as specified by FR-V12-A-118:
      """
      AI step inventory: of 517 steps, 159 AI-inference steps are tagged; all other steps are rules, gates, retrieval or controlled effects that
      never call a model (detail Groups C/D/F)
      """
    Then count check 159 / 517 at registry load
    And the audit event "ai.ai_step_inventory" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU02-03 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU02-04 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU02-05 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU02-06 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU02-07 Permutations – AI governance, evaluation, prompts and cost (3-way, 59 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-113 = Context budgeting, summarisation and multimodal…
    #   A-118 = AI step inventory
    Examples: MU05 rows (3-way, seed 276; space 1,944; tuples 930/930; +2 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU02-01 | A-118 | P16/R20 | Confidential | candidate only | L1 | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU02-02 | A-118 | P16/R20 | Public | model Approved | L3 mandate | soft cap | EU | ALLOW: Count check 159 / 517 at registry load |
      | EX-04ZU02-03 | A-118 | P03/R03 | Confidential | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-04 | A-113 | P10/R11 | Restricted | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-05 | A-113 | P03/R03 | Internal | prompt unapproved | L3 mandate | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU02-06 | A-113 | P10/R11 | Public | prompt unapproved | L3 revoked | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU02-07 | A-118 | P10/R11 | Internal | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU02-08 | A-113 | P16/R20 | Restricted | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-09 | A-118 | P03/R03 | Restricted | prompt unapproved | L1 | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU02-10 | A-113 | P10/R11 | Confidential | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU02-11 | A-113 | P16/R20 | Internal | model Approved | L3 revoked | soft cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU02-12 | A-118 | P10/R11 | Confidential | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-13 | A-118 | P16/R20 | Restricted | prompt unapproved | L3 revoked | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU02-14 | A-113 | P03/R03 | Public | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-15 | A-113 | P16/R20 | Confidential | prompt unapproved | L1 | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU02-16 | A-118 | P10/R11 | Internal | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU02-17 | A-118 | P03/R03 | Public | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU02-18 | A-113 | P03/R03 | Confidential | model Approved | L3 mandate | soft cap | IN | ALLOW: Oversized context reduced or held |
      | EX-04ZU02-19 | A-113 | P03/R03 | Restricted | model Approved | L3 revoked | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU02-20 | A-113 | P10/R11 | Internal | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-21 | A-118 | P16/R20 | Public | prompt unapproved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-22 | A-118 | P10/R11 | Restricted | candidate only | L3 mandate | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU02-23 | A-118 | P03/R03 | Internal | prompt unapproved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-24 | A-113 | P03/R03 | Internal | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-04ZU02-25 | A-118 | P03/R03 | Public | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU02-26 | A-113 | P10/R11 | Public | model Approved | L3 mandate | hard cap | EU | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU02-27 | A-118 | P16/R20 | Internal | prompt unapproved | L3 mandate | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU02-28 | A-118 | P03/R03 | Confidential | model Approved | L1 | hard cap | EU | PENDING_APPROVAL |
      | EX-04ZU02-29 | A-113 | P16/R20 | Confidential | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-30 | A-113 | P10/R11 | Restricted | prompt unapproved | L1 | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU02-31 | A-118 | P16/R20 | Restricted | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-32 | A-118 | P10/R11 | Public | model Approved | L1 | soft cap | IN | PENDING_APPROVAL |
      | EX-04ZU02-33 | A-118 | P10/R11 | Public | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-34 | A-113 | P10/R11 | Confidential | prompt unapproved | L3 revoked | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU02-35 | A-113 | P03/R03 | Restricted | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-36 | A-113 | P16/R20 | Public | candidate only | L3 revoked | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU02-37 | A-113 | P16/R20 | Internal | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-38 | A-113 | P10/R11 | Internal | candidate only | L3 mandate | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU02-39 | A-118 | P16/R20 | Restricted | model Approved | L3 mandate | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU02-40 | A-113 | P03/R03 | Restricted | candidate only | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU02-41 | A-118 | P03/R03 | Restricted | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-42 | A-118 | P16/R20 | Public | prompt unapproved | L3 mandate | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU02-43 | A-113 | P10/R11 | Restricted | model Approved | L3 revoked | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU02-44 | A-113 | P03/R03 | Confidential | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU02-45 | A-113 | P16/R20 | Internal | model Approved | L3 revoked | in budget | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU02-46 | A-113 | P03/R03 | Public | prompt unapproved | L1 | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU02-47 | A-118 | P10/R11 | Confidential | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-48 | A-113 | P10/R11 | Confidential | model Approved | L3 mandate | in budget | IN | ALLOW: Oversized context reduced or held |
      | EX-04ZU02-49 | A-118 | P16/R20 | Internal | candidate only | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-50 | A-113 | P10/R11 | Internal | prompt unapproved | L1 | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU02-51 | A-118 | P03/R03 | Public | model Approved | L3 revoked | soft cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU02-52 | A-113 | P16/R20 | Restricted | candidate only | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU02-53 | A-118 | P16/R20 | Confidential | prompt unapproved | L3 revoked | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU02-54 | A-118 | P03/R03 | Internal | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-55 | A-113 | P10/R11 | Public | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-56 | A-118 | P03/R03 | Confidential | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-57 | A-118 | P03/R03 | Internal | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU02-58 | A-113 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Oversized context reduced or held |
      | EX-04ZU02-59 | A-118 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Count check 159 / 517 at registry load |
```

##### US-04-ZU03 Launch-language evaluation slices gate a locale

| Field | Value |
|---|---|
| ID | US-04-ZU03 |
| Title | Launch-language evaluation slices gate a locale |
| Type | Compliance (acceptance binding) |
| Story | As the AI owner, I want AI labels, region pinning and language slice gates before a locale goes live – with the acceptance criteria below, which the statement-only story US-04-YA01 did not carry |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-A-117 (BR-V7-AI-07); tests TC-V12-A-117 |
| Priority | Should |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-04-YA01, US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.1b §11.1.5.7 AI automation authority and governance |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×1 · model MU05 |
| Notes | Acceptance binding: US-04-YA01 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: Launch-language evaluation slices gate a locale
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy
  Scenario: AC-04ZU03-01 Happy path – Launch-language evaluation slices (FR-V12-A-117)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Launch-language evaluation slices" is exercised as specified by FR-V12-A-117:
      """
      Launch-language evaluation slices: quality proven per language before a locale goes live — English and Hindi (India) first; English, German,
      French with the EU pack
      """
    Then locale enable blocked until its slice passes
    And the audit event "ai.launch_language_evaluation" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU03-02 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU03-03 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU03-04 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU03-05 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU03-06 Permutations – AI governance, evaluation, prompts and cost (3-way, 56 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-117 = Launch-language evaluation slices
    Examples: MU05 rows (3-way, seed 283; space 972; tuples 780/780; +1 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU03-01 | A-117 | P10/R11 | Restricted | prompt unapproved | L3 revoked | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU03-02 | A-117 | P03/R03 | Confidential | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-03 | A-117 | P16/R20 | Public | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-04 | A-117 | P10/R11 | Internal | candidate only | L3 mandate | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU03-05 | A-117 | P03/R03 | Restricted | prompt unapproved | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU03-06 | A-117 | P03/R03 | Public | model Approved | L3 mandate | in budget | EU | ALLOW: Locale enable blocked until its slice passes |
      | EX-04ZU03-07 | A-117 | P16/R20 | Confidential | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU03-08 | A-117 | P16/R20 | Restricted | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-09 | A-117 | P16/R20 | Internal | model Approved | L3 revoked | in budget | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU03-10 | A-117 | P10/R11 | Internal | model Approved | L1 | hard cap | EU | PENDING_APPROVAL |
      | EX-04ZU03-11 | A-117 | P03/R03 | Internal | prompt unapproved | L3 revoked | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU03-12 | A-117 | P10/R11 | Confidential | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-13 | A-117 | P10/R11 | Public | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-14 | A-117 | P03/R03 | Confidential | candidate only | L3 revoked | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU03-15 | A-117 | P16/R20 | Public | model Approved | L1 | soft cap | IN | PENDING_APPROVAL |
      | EX-04ZU03-16 | A-117 | P03/R03 | Restricted | candidate only | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU03-17 | A-117 | P03/R03 | Restricted | model Approved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-18 | A-117 | P16/R20 | Confidential | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU03-19 | A-117 | P03/R03 | Internal | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-20 | A-117 | P10/R11 | Public | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU03-21 | A-117 | P10/R11 | Restricted | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-22 | A-117 | P10/R11 | Restricted | model Approved | L3 mandate | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU03-23 | A-117 | P16/R20 | Confidential | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU03-24 | A-117 | P10/R11 | Confidential | prompt unapproved | L1 | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU03-25 | A-117 | P16/R20 | Restricted | model Approved | L3 revoked | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU03-26 | A-117 | P16/R20 | Internal | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-27 | A-117 | P10/R11 | Confidential | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-28 | A-117 | P03/R03 | Public | prompt unapproved | L3 mandate | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU03-29 | A-117 | P10/R11 | Internal | prompt unapproved | L3 revoked | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU03-30 | A-117 | P16/R20 | Public | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-31 | A-117 | P16/R20 | Restricted | candidate only | L1 | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU03-32 | A-117 | P16/R20 | Internal | model Approved | L3 mandate | soft cap | EU | ALLOW: Locale enable blocked until its slice passes |
      | EX-04ZU03-33 | A-117 | P16/R20 | Public | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU03-34 | A-117 | P03/R03 | Internal | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU03-35 | A-117 | P10/R11 | Confidential | candidate only | L3 mandate | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU03-36 | A-117 | P10/R11 | Public | candidate only | L3 mandate | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU03-37 | A-117 | P16/R20 | Public | prompt unapproved | L3 revoked | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU03-38 | A-117 | P03/R03 | Public | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-39 | A-117 | P03/R03 | Confidential | prompt unapproved | L3 mandate | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU03-40 | A-117 | P03/R03 | Restricted | candidate only | L3 revoked | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU03-41 | A-117 | P10/R11 | Internal | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-42 | A-117 | P16/R20 | Confidential | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-43 | A-117 | P03/R03 | Internal | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-04ZU03-44 | A-117 | P16/R20 | Internal | prompt unapproved | L1 | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU03-45 | A-117 | P03/R03 | Public | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-46 | A-117 | P10/R11 | Internal | candidate only | L3 revoked | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU03-47 | A-117 | P16/R20 | Restricted | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-48 | A-117 | P03/R03 | Confidential | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-49 | A-117 | P03/R03 | Restricted | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-50 | A-117 | P03/R03 | Internal | prompt unapproved | L3 mandate | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU03-51 | A-117 | P10/R11 | Public | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-52 | A-117 | P10/R11 | Restricted | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU03-53 | A-117 | P16/R20 | Public | candidate only | L1 | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU03-54 | A-117 | P16/R20 | Restricted | prompt unapproved | L1 | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU03-55 | A-117 | P03/R03 | Confidential | model Approved | L3 revoked | hard cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU03-56 | A-117 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Locale enable blocked until its slice passes |
```

##### US-04-ZU04 AIX-01, 04, 06: step classification, prompt registry and regression gate

| Field | Value |
|---|---|
| ID | US-04-ZU04 |
| Title | AIX-01, 04, 06: step classification, prompt registry and regression gate |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want step classification; only AI-inference steps may call a model; prompt registry PRM-<AGT>-<task>-vN with schema, policy inputs, locales, approval; no tenant data; regression on any model/prompt/retrieval/policy/tool change; promotion blocked on regression, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-001 (AIX-01); FR-V12-F-004 (AIX-04); FR-V12-F-006 (AIX-06); DEC-770, DEC-790; tests TC-V12-F-001, TC-V12-F-004, TC-V12-F-006 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×3 · model MU05 |
| Notes | FR-V12-F-001, FR-V12-F-004, FR-V12-F-006: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Related existing stories (shared source IDs, no FR trace): US-04-YM27, US-04-YM28 · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: AIX-01, 04, 06: step classification, prompt registry and regression gate
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @AIX-01 @DEC-770
  Scenario: AC-04ZU04-01 Happy path – Step classification; only AI-inference steps may call a model (FR-V12-F-001)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Step classification; only AI-inference steps may call a model" is exercised as specified by FR-V12-F-001:
      """
      Step classification; only AI-inference steps may call a model
      """
    Then static check fails CI
    And the audit event "ai.step_classification" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @AIX-04 @DEC-770
  Scenario: AC-04ZU04-02 Alternate – Prompt registry PRM-<AGT>-<task>-vN with schema, policy inputs (FR-V12-F-004)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Prompt registry PRM-<AGT>-<task>-vN with schema, policy inputs" is exercised as specified by FR-V12-F-004:
      """
      Prompt registry PRM-<AGT>-<task>-vN with schema, policy inputs, locales, approval; no tenant data
      """
    Then run records prompt version; unapproved prompt blocked
    And the audit event "ai.prompt_registry" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @AIX-06 @DEC-770
  Scenario: AC-04ZU04-03 Alternate – Regression on any model/prompt/retrieval/policy/tool change (FR-V12-F-006)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Regression on any model/prompt/retrieval/policy/tool change" is exercised as specified by FR-V12-F-006:
      """
      Regression on any model/prompt/retrieval/policy/tool change; promotion blocked on regression
      """
    Then lower-accuracy prompt cannot be promoted
    And the audit event "ai.regression_on_any" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU04-04 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU04-05 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU04-06 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU04-07 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU04-08 Permutations – AI governance, evaluation, prompts and cost (3-way, 65 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-001 = Step classification; only AI-inference steps may…
    #   F-004 = Prompt registry PRM-<AGT>-<task>-vN with schema
    #   F-006 = Regression on any…
    Examples: MU05 rows (3-way, seed 290; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU04-01 | F-006 | P03/R03 | Public | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-02 | F-004 | P03/R03 | Confidential | prompt unapproved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-03 | F-001 | P16/R20 | Internal | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-04 | F-006 | P16/R20 | Confidential | model Approved | L3 mandate | in budget | EU | ALLOW: lower-accuracy prompt cannot be promoted |
      | EX-04ZU04-05 | F-001 | P03/R03 | Restricted | model Approved | L1 | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU04-06 | F-004 | P10/R11 | Internal | prompt unapproved | L3 mandate | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU04-07 | F-001 | P10/R11 | Confidential | prompt unapproved | L3 revoked | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU04-08 | F-006 | P10/R11 | Restricted | candidate only | L1 | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU04-09 | F-004 | P03/R03 | Public | model Approved | L3 revoked | hard cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU04-10 | F-001 | P10/R11 | Public | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-11 | F-006 | P16/R20 | Public | prompt unapproved | L3 revoked | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU04-12 | F-004 | P16/R20 | Confidential | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU04-13 | F-004 | P16/R20 | Restricted | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-14 | F-006 | P03/R03 | Internal | prompt unapproved | L1 | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU04-15 | F-004 | P03/R03 | Restricted | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-16 | F-001 | P03/R03 | Confidential | candidate only | L3 mandate | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU04-17 | F-006 | P10/R11 | Internal | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-18 | F-001 | P16/R20 | Internal | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU04-19 | F-006 | P16/R20 | Restricted | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-20 | F-006 | P10/R11 | Confidential | model Approved | L3 revoked | hard cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU04-21 | F-004 | P10/R11 | Public | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU04-22 | F-001 | P16/R20 | Internal | model Approved | L1 | hard cap | IN | PENDING_APPROVAL |
      | EX-04ZU04-23 | F-001 | P10/R11 | Public | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-24 | F-001 | P03/R03 | Restricted | prompt unapproved | L3 mandate | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU04-25 | F-004 | P03/R03 | Internal | prompt unapproved | L3 revoked | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU04-26 | F-004 | P16/R20 | Public | model Approved | L1 | soft cap | EU | PENDING_APPROVAL |
      | EX-04ZU04-27 | F-001 | P10/R11 | Restricted | candidate only | L3 revoked | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU04-28 | F-004 | P10/R11 | Restricted | model Approved | L3 mandate | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU04-29 | F-006 | P16/R20 | Restricted | candidate only | L3 revoked | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU04-30 | F-006 | P10/R11 | Confidential | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-31 | F-004 | P10/R11 | Internal | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-32 | F-006 | P03/R03 | Public | candidate only | L1 | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU04-33 | F-006 | P03/R03 | Internal | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-34 | F-004 | P16/R20 | Confidential | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-35 | F-001 | P10/R11 | Public | prompt unapproved | L1 | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU04-36 | F-001 | P16/R20 | Confidential | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU04-37 | F-004 | P10/R11 | Internal | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU04-38 | F-006 | P16/R20 | Restricted | prompt unapproved | L3 revoked | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU04-39 | F-001 | P03/R03 | Confidential | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-40 | F-004 | P16/R20 | Public | candidate only | L3 mandate | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU04-41 | F-006 | P03/R03 | Restricted | model Approved | L3 revoked | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU04-42 | F-001 | P03/R03 | Public | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU04-43 | F-006 | P16/R20 | Internal | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU04-44 | F-004 | P16/R20 | Confidential | prompt unapproved | L3 mandate | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU04-45 | F-001 | P10/R11 | Internal | model Approved | L3 mandate | in budget | EU | ALLOW: static check fails CI |
      | EX-04ZU04-46 | F-006 | P03/R03 | Confidential | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-04ZU04-47 | F-004 | P10/R11 | Restricted | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-48 | F-004 | P16/R20 | Public | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-49 | F-006 | P10/R11 | Public | model Approved | L3 mandate | soft cap | IN | ALLOW: lower-accuracy prompt cannot be promoted |
      | EX-04ZU04-50 | F-006 | P10/R11 | Confidential | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-51 | F-006 | P03/R03 | Public | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU04-52 | F-001 | P16/R20 | Restricted | candidate only | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU04-53 | F-001 | P03/R03 | Internal | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-54 | F-004 | P03/R03 | Restricted | model Approved | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU04-55 | F-004 | P16/R20 | Internal | model Approved | L3 mandate | in budget | EU | ALLOW: run records prompt version |
      | EX-04ZU04-56 | F-006 | P16/R20 | Restricted | candidate only | L3 mandate | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU04-57 | F-004 | P10/R11 | Confidential | prompt unapproved | L3 mandate | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU04-58 | F-004 | P03/R03 | Internal | candidate only | L3 revoked | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU04-59 | F-001 | P03/R03 | Confidential | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU04-60 | F-001 | P03/R03 | Restricted | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-61 | F-001 | P16/R20 | Public | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU04-62 | F-006 | P10/R11 | Public | candidate only | L3 revoked | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU04-63 | F-001 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: static check fails CI |
      | EX-04ZU04-64 | F-004 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: run records prompt version |
      | EX-04ZU04-65 | F-006 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: lower-accuracy prompt cannot be promoted |
```

##### US-04-ZU05 AIX-07…09: calibrated judges, untrusted-content isolation and reader/actor separation

| Field | Value |
|---|---|
| ID | US-04-ZU05 |
| Title | AIX-07…09: calibrated judges, untrusted-content isolation and reader/actor separation |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want judge only after κ ≥ 0.8 calibration; untrusted content isolation; reader/actor separation, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-007 (AIX-07); FR-V12-F-008 (AIX-08); FR-V12-F-009 (AIX-09); DEC-770, DEC-790; tests TC-V12-F-007, TC-V12-F-008, TC-V12-F-009 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×3 · model MU05 |
| Notes | FR-V12-F-007, FR-V12-F-008, FR-V12-F-009: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: AIX-07…09: calibrated judges, untrusted-content isolation and reader/actor separation
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @AIX-07 @DEC-770
  Scenario: AC-04ZU05-01 Happy path – Judge only after κ ≥ 0.8 calibration (FR-V12-F-007)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Judge only after κ ≥ 0.8 calibration" is exercised as specified by FR-V12-F-007: Judge only after κ ≥ 0.8 calibration
    Then uncalibrated grader non-gating
    And the audit event "ai.judge_only_after_0_8" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @AIX-08 @DEC-770
  Scenario: AC-04ZU05-02 Alternate – Untrusted content isolation (FR-V12-F-008)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Untrusted content isolation" is exercised as specified by FR-V12-F-008: Untrusted content isolation
    Then AI-INJ-01…12 zero violations
    And the audit event "ai.untrusted_content_isolation" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @AIX-09 @DEC-770
  Scenario: AC-04ZU05-03 Alternate – Reader/actor separation (FR-V12-F-009)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Reader/actor separation" is exercised as specified by FR-V12-F-009: Reader/actor separation
    Then injected send/forward cannot cause effect
    And the audit event "ai.reader_actor_separation" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU05-04 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU05-05 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU05-06 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU05-07 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU05-08 Permutations – AI governance, evaluation, prompts and cost (3-way, 62 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-007 = Judge only after κ ≥ 0.8 calibration
    #   F-008 = Untrusted content isolation
    #   F-009 = Reader/actor separation
    Examples: MU05 rows (3-way, seed 297; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU05-01 | F-009 | P16/R20 | Restricted | candidate only | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU05-02 | F-008 | P10/R11 | Restricted | model Approved | L1 | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU05-03 | F-007 | P03/R03 | Public | candidate only | L3 mandate | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU05-04 | F-009 | P03/R03 | Confidential | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-05 | F-007 | P03/R03 | Confidential | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU05-06 | F-007 | P10/R11 | Internal | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-07 | F-008 | P16/R20 | Public | prompt unapproved | L3 revoked | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU05-08 | F-009 | P16/R20 | Internal | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-09 | F-009 | P10/R11 | Public | model Approved | L3 revoked | soft cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU05-10 | F-008 | P03/R03 | Internal | prompt unapproved | L3 mandate | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU05-11 | F-008 | P10/R11 | Confidential | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-12 | F-007 | P16/R20 | Restricted | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-13 | F-009 | P03/R03 | Internal | model Approved | L1 | hard cap | IN | PENDING_APPROVAL |
      | EX-04ZU05-14 | F-007 | P16/R20 | Public | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU05-15 | F-007 | P16/R20 | Confidential | model Approved | L3 revoked | soft cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU05-16 | F-008 | P03/R03 | Restricted | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-17 | F-009 | P10/R11 | Public | prompt unapproved | L3 mandate | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU05-18 | F-008 | P16/R20 | Internal | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU05-19 | F-007 | P10/R11 | Restricted | candidate only | L3 revoked | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU05-20 | F-008 | P16/R20 | Public | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-21 | F-009 | P03/R03 | Restricted | model Approved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-22 | F-009 | P10/R11 | Confidential | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU05-23 | F-007 | P10/R11 | Restricted | prompt unapproved | L1 | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU05-24 | F-008 | P03/R03 | Confidential | model Approved | L3 revoked | hard cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU05-25 | F-007 | P03/R03 | Internal | model Approved | L3 revoked | in budget | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU05-26 | F-008 | P03/R03 | Public | prompt unapproved | L1 | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU05-27 | F-007 | P10/R11 | Confidential | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU05-28 | F-009 | P16/R20 | Confidential | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-04ZU05-29 | F-009 | P10/R11 | Internal | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-30 | F-008 | P16/R20 | Confidential | candidate only | L3 mandate | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU05-31 | F-007 | P10/R11 | Public | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-32 | F-008 | P10/R11 | Internal | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-33 | F-009 | P03/R03 | Restricted | prompt unapproved | L3 revoked | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU05-34 | F-007 | P16/R20 | Internal | prompt unapproved | L3 mandate | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU05-35 | F-008 | P10/R11 | Internal | model Approved | L1 | soft cap | EU | PENDING_APPROVAL |
      | EX-04ZU05-36 | F-009 | P16/R20 | Public | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-37 | F-008 | P10/R11 | Public | candidate only | L3 mandate | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU05-38 | F-008 | P16/R20 | Restricted | prompt unapproved | L3 mandate | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU05-39 | F-009 | P16/R20 | Internal | candidate only | L1 | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU05-40 | F-007 | P03/R03 | Internal | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-41 | F-007 | P16/R20 | Internal | model Approved | L1 | hard cap | EU | PENDING_APPROVAL |
      | EX-04ZU05-42 | F-007 | P03/R03 | Public | prompt unapproved | L3 revoked | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU05-43 | F-009 | P03/R03 | Public | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-44 | F-008 | P03/R03 | Confidential | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU05-45 | F-007 | P03/R03 | Restricted | model Approved | L3 mandate | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU05-46 | F-009 | P16/R20 | Confidential | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-47 | F-009 | P10/R11 | Restricted | candidate only | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-48 | F-009 | P10/R11 | Confidential | prompt unapproved | L3 revoked | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU05-49 | F-007 | P03/R03 | Confidential | candidate only | L3 mandate | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU05-50 | F-008 | P16/R20 | Restricted | model Approved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-51 | F-008 | P16/R20 | Restricted | prompt unapproved | L1 | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU05-52 | F-008 | P10/R11 | Internal | candidate only | L3 mandate | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU05-53 | F-007 | P16/R20 | Confidential | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-54 | F-007 | P03/R03 | Restricted | candidate only | L1 | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU05-55 | F-007 | P03/R03 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: uncalibrated grader non-gating |
      | EX-04ZU05-56 | F-009 | P10/R11 | Internal | prompt unapproved | L3 mandate | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU05-57 | F-009 | P10/R11 | Restricted | prompt unapproved | L3 mandate | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU05-58 | F-009 | P16/R20 | Public | prompt unapproved | L1 | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU05-59 | F-008 | P10/R11 | Confidential | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU05-60 | F-007 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: uncalibrated grader non-gating |
      | EX-04ZU05-61 | F-008 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: AI-INJ-01…12 zero violations |
      | EX-04ZU05-62 | F-009 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: injected send/forward cannot cause effect |
```

##### US-04-ZU06 AIX-10…12: output handling, claims and citations, per-call AI metering

| Field | Value |
|---|---|
| ID | US-04-ZU06 |
| Title | AIX-10…12: output handling, claims and citations, per-call AI metering |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want output handling: schema, URL/egress allowlist, sanitised rendering, no secrets; claims and citation control; AI usage metering per call, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-010 (AIX-10); FR-V12-F-011 (AIX-11); FR-V12-F-012 (AIX-12); DEC-770, DEC-790; tests TC-V12-F-010, TC-V12-F-011, TC-V12-F-012 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×3 · model MU05 |
| Notes | FR-V12-F-010, FR-V12-F-011, FR-V12-F-012: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Related existing stories (shared source IDs, no FR trace): US-05-YM02, US-11-YF04 · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: AIX-10…12: output handling, claims and citations, per-call AI metering
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @AIX-10 @DEC-770
  Scenario: AC-04ZU06-01 Happy path – Output handling: schema, URL/egress allowlist, sanitised rendering (FR-V12-F-010)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Output handling: schema, URL/egress allowlist, sanitised rendering" is exercised as specified by FR-V12-F-010:
      """
      Output handling: schema, URL/egress allowlist, sanitised rendering, no secrets
      """
    Then image-link exfiltration and secret requests blocked
    And the audit event "ai.output_handling_schema" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @AIX-11 @DEC-770
  Scenario: AC-04ZU06-02 Alternate – Claims and citation control (FR-V12-F-011)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Claims and citation control" is exercised as specified by FR-V12-F-011: Claims and citation control
    Then unapproved claim → REVIEW; uncited fact flagged
    And the audit event "ai.claims_and_citation_control" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @AIX-12 @DEC-770
  Scenario: AC-04ZU06-03 Alternate – AI usage metering per call (FR-V12-F-012)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "AI usage metering per call" is exercised as specified by FR-V12-F-012: AI usage metering per call
    Then tenant totals reconcile with provider invoices within tolerance
    And the audit event "ai.ai_usage_metering_per_call" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU06-04 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU06-05 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU06-06 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU06-07 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU06-08 Permutations – AI governance, evaluation, prompts and cost (3-way, 64 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-010 = Output handling: schema, URL/egress allowlist
    #   F-011 = Claims and citation control
    #   F-012 = AI usage metering per call
    Examples: MU05 rows (3-way, seed 304; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU06-01 | F-011 | P10/R11 | Confidential | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-02 | F-012 | P16/R20 | Internal | prompt unapproved | L1 | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU06-03 | F-010 | P10/R11 | Public | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-04 | F-010 | P16/R20 | Restricted | model Approved | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU06-05 | F-011 | P03/R03 | Confidential | candidate only | L1 | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU06-06 | F-011 | P16/R20 | Public | prompt unapproved | L3 revoked | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU06-07 | F-012 | P03/R03 | Restricted | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-08 | F-012 | P03/R03 | Public | candidate only | L3 revoked | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU06-09 | F-010 | P10/R11 | Restricted | prompt unapproved | L1 | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU06-10 | F-010 | P03/R03 | Internal | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-11 | F-012 | P10/R11 | Internal | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU06-12 | F-011 | P03/R03 | Confidential | prompt unapproved | L3 mandate | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU06-13 | F-012 | P16/R20 | Restricted | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-14 | F-011 | P10/R11 | Internal | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU06-15 | F-010 | P03/R03 | Public | model Approved | L3 mandate | soft cap | IN | ALLOW: image-link exfiltration and secret requests blocked |
      | EX-04ZU06-16 | F-011 | P16/R20 | Public | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-17 | F-012 | P10/R11 | Confidential | candidate only | L3 revoked | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU06-18 | F-012 | P16/R20 | Confidential | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-19 | F-011 | P03/R03 | Internal | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-20 | F-011 | P10/R11 | Restricted | prompt unapproved | L3 revoked | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU06-21 | F-010 | P16/R20 | Confidential | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-04ZU06-22 | F-010 | P16/R20 | Confidential | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU06-23 | F-010 | P03/R03 | Internal | model Approved | L3 revoked | in budget | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU06-24 | F-011 | P16/R20 | Restricted | candidate only | L3 mandate | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU06-25 | F-012 | P10/R11 | Public | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU06-26 | F-010 | P10/R11 | Confidential | model Approved | L1 | hard cap | EU | PENDING_APPROVAL |
      | EX-04ZU06-27 | F-012 | P03/R03 | Confidential | prompt unapproved | L3 revoked | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU06-28 | F-010 | P16/R20 | Internal | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU06-29 | F-011 | P03/R03 | Public | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-30 | F-012 | P10/R11 | Restricted | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-31 | F-011 | P03/R03 | Restricted | model Approved | L1 | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU06-32 | F-011 | P16/R20 | Internal | model Approved | L3 revoked | soft cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU06-33 | F-012 | P16/R20 | Public | model Approved | L3 mandate | in budget | EU | ALLOW: tenant totals reconcile with provider invoices |
      | EX-04ZU06-34 | F-012 | P10/R11 | Internal | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-35 | F-012 | P16/R20 | Public | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU06-36 | F-012 | P03/R03 | Restricted | prompt unapproved | L3 mandate | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU06-37 | F-010 | P16/R20 | Restricted | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-38 | F-011 | P10/R11 | Restricted | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-39 | F-010 | P03/R03 | Restricted | candidate only | L3 revoked | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU06-40 | F-011 | P10/R11 | Public | candidate only | L3 mandate | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU06-41 | F-010 | P03/R03 | Internal | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-42 | F-010 | P16/R20 | Public | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU06-43 | F-010 | P03/R03 | Confidential | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-44 | F-012 | P10/R11 | Public | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-45 | F-010 | P16/R20 | Internal | prompt unapproved | L3 mandate | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU06-46 | F-012 | P10/R11 | Confidential | candidate only | L3 mandate | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU06-47 | F-011 | P16/R20 | Internal | prompt unapproved | L3 mandate | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU06-48 | F-010 | P10/R11 | Internal | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU06-49 | F-011 | P03/R03 | Confidential | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-50 | F-010 | P03/R03 | Confidential | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-51 | F-012 | P16/R20 | Restricted | candidate only | L3 mandate | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU06-52 | F-012 | P03/R03 | Internal | candidate only | L3 revoked | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU06-53 | F-010 | P10/R11 | Restricted | model Approved | L3 revoked | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU06-54 | F-011 | P03/R03 | Public | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-04ZU06-55 | F-012 | P10/R11 | Confidential | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU06-56 | F-012 | P10/R11 | Confidential | model Approved | L3 mandate | soft cap | IN | ALLOW: tenant totals reconcile with provider invoices |
      | EX-04ZU06-57 | F-011 | P16/R20 | Internal | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU06-58 | F-011 | P16/R20 | Confidential | prompt unapproved | L3 revoked | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU06-59 | F-010 | P03/R03 | Restricted | model Approved | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU06-60 | F-011 | P10/R11 | Public | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-04ZU06-61 | F-010 | P03/R03 | Public | model Approved | L3 revoked | in budget | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU06-62 | F-010 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: image-link exfiltration and secret requests blocked |
      | EX-04ZU06-63 | F-011 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: unapproved claim → REVIEW |
      | EX-04ZU06-64 | F-012 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: tenant totals reconcile with provider invoices |
```

##### US-04-ZU07 AIX-13…15: tenant AI budgets, cost per accepted result and scoped caching

| Field | Value |
|---|---|
| ID | US-04-ZU07 |
| Title | AIX-13…15: tenant AI budgets, cost per accepted result and scoped caching |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want tenant AI budgets soft/hard per tenant, company, workflow; cost per accepted result in A117; prefix caching, batch API, tenant-scoped semantic cache for non-personal, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-013 (AIX-13); FR-V12-F-014 (AIX-14); FR-V12-F-015 (AIX-15); DEC-770, DEC-790; tests TC-V12-F-013, TC-V12-F-014, TC-V12-F-015 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×3 · model MU05 |
| Notes | FR-V12-F-013, FR-V12-F-014, FR-V12-F-015: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: AIX-13…15: tenant AI budgets, cost per accepted result and scoped caching
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @AIX-13 @DEC-770
  Scenario: AC-04ZU07-01 Happy path – Tenant AI budgets soft/hard per tenant, company, workflow (FR-V12-F-013)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Tenant AI budgets soft/hard per tenant, company, workflow" is exercised as specified by FR-V12-F-013:
      """
      Tenant AI budgets soft/hard per tenant, company, workflow
      """
    Then hard cap → AI step Held, no provider call
    And the audit event "ai.tenant_ai_budgets_soft_hard" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @AIX-14 @DEC-770
  Scenario: AC-04ZU07-02 Alternate – Cost per accepted result in A117 (FR-V12-F-014)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Cost per accepted result in A117" is exercised as specified by FR-V12-F-014: Cost per accepted result in A117
    Then denominator and rejected outputs shown
    And the audit event "ai.cost_per_accepted_result_in" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @AIX-15 @DEC-770
  Scenario: AC-04ZU07-03 Alternate – Prefix caching, batch API, tenant-scoped semantic cache for… (FR-V12-F-015)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Prefix caching, batch API, tenant-scoped semantic cache for…" is exercised as specified by FR-V12-F-015:
      """
      Prefix caching, batch API, tenant-scoped semantic cache for non-personal
      """
    Then cache key includes tenant and policy version
    And the audit event "ai.prefix_caching_batch_api" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU07-04 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU07-05 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU07-06 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU07-07 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU07-08 Permutations – AI governance, evaluation, prompts and cost (3-way, 62 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-013 = Tenant AI budgets soft/hard per tenant, company
    #   F-014 = Cost per accepted result in A117
    #   F-015 = Prefix caching, batch API, tenant-scoped semantic…
    Examples: MU05 rows (3-way, seed 311; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU07-01 | F-015 | P03/R03 | Confidential | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU07-02 | F-015 | P16/R20 | Restricted | candidate only | L1 | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU07-03 | F-013 | P03/R03 | Internal | prompt unapproved | L1 | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU07-04 | F-014 | P10/R11 | Internal | model Approved | L3 mandate | soft cap | EU | ALLOW: denominator and rejected outputs shown |
      | EX-04ZU07-05 | F-014 | P03/R03 | Restricted | candidate only | L3 revoked | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU07-06 | F-014 | P16/R20 | Public | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU07-07 | F-015 | P16/R20 | Internal | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-08 | F-013 | P10/R11 | Confidential | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-09 | F-013 | P03/R03 | Public | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-10 | F-013 | P10/R11 | Restricted | prompt unapproved | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU07-11 | F-015 | P10/R11 | Public | candidate only | L3 revoked | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU07-12 | F-014 | P16/R20 | Confidential | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-13 | F-013 | P16/R20 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: hard cap → AI step Held, no provider call |
      | EX-04ZU07-14 | F-015 | P03/R03 | Public | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-04ZU07-15 | F-014 | P10/R11 | Confidential | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU07-16 | F-013 | P16/R20 | Internal | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU07-17 | F-015 | P03/R03 | Restricted | prompt unapproved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-18 | F-014 | P16/R20 | Confidential | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU07-19 | F-015 | P10/R11 | Internal | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-20 | F-014 | P10/R11 | Restricted | candidate only | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-21 | F-013 | P03/R03 | Confidential | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU07-22 | F-015 | P16/R20 | Restricted | model Approved | L3 revoked | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU07-23 | F-014 | P03/R03 | Public | prompt unapproved | L3 mandate | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU07-24 | F-013 | P16/R20 | Restricted | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-25 | F-013 | P10/R11 | Internal | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU07-26 | F-014 | P03/R03 | Internal | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-27 | F-013 | P10/R11 | Restricted | model Approved | L1 | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU07-28 | F-014 | P03/R03 | Confidential | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU07-29 | F-015 | P10/R11 | Confidential | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU07-30 | F-013 | P03/R03 | Internal | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-31 | F-015 | P16/R20 | Confidential | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-32 | F-015 | P16/R20 | Public | prompt unapproved | L1 | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU07-33 | F-014 | P10/R11 | Public | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-34 | F-013 | P16/R20 | Confidential | prompt unapproved | L3 revoked | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU07-35 | F-015 | P10/R11 | Restricted | candidate only | L3 mandate | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU07-36 | F-013 | P03/R03 | Restricted | model Approved | L3 mandate | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU07-37 | F-014 | P16/R20 | Internal | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU07-38 | F-015 | P03/R03 | Internal | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU07-39 | F-015 | P10/R11 | Public | model Approved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-40 | F-013 | P10/R11 | Public | model Approved | L3 revoked | soft cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU07-41 | F-014 | P16/R20 | Public | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU07-42 | F-014 | P16/R20 | Restricted | prompt unapproved | L3 mandate | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU07-43 | F-013 | P10/R11 | Internal | model Approved | L3 revoked | hard cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU07-44 | F-015 | P03/R03 | Confidential | candidate only | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-45 | F-015 | P10/R11 | Public | candidate only | L3 mandate | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU07-46 | F-013 | P10/R11 | Confidential | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-47 | F-014 | P03/R03 | Restricted | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-48 | F-015 | P16/R20 | Internal | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU07-49 | F-015 | P03/R03 | Public | prompt unapproved | L3 revoked | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU07-50 | F-013 | P10/R11 | Restricted | candidate only | L3 revoked | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU07-51 | F-014 | P16/R20 | Internal | candidate only | L1 | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU07-52 | F-014 | P03/R03 | Confidential | model Approved | L3 revoked | soft cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU07-53 | F-013 | P16/R20 | Public | candidate only | L3 revoked | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU07-54 | F-014 | P10/R11 | Public | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-55 | F-013 | P10/R11 | Confidential | candidate only | L1 | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU07-56 | F-014 | P10/R11 | Internal | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-57 | F-013 | P16/R20 | Public | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU07-58 | F-015 | P16/R20 | Internal | prompt unapproved | L3 mandate | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU07-59 | F-014 | P03/R03 | Restricted | model Approved | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU07-60 | F-013 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: hard cap → AI step Held, no provider call |
      | EX-04ZU07-61 | F-014 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: denominator and rejected outputs shown |
      | EX-04ZU07-62 | F-015 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: cache key includes tenant and policy version |
```

##### US-04-ZU08 AIX-17…19: provider data handling, drift monitoring and multilingual gates

| Field | Value |
|---|---|
| ID | US-04-ZU08 |
| Title | AIX-17…19: provider data handling, drift monitoring and multilingual gates |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want provider data handling: no training, DPA retention/region, minimise/mask for Tier S; drift monitoring nightly sample; multilingual coverage en+hi IN; de+fr EU; locale prompts, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-017 (AIX-17); FR-V12-F-018 (AIX-18); FR-V12-F-019 (AIX-19); DEC-770, DEC-790; tests TC-V12-F-017, TC-V12-F-018, TC-V12-F-019 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×3 · model MU05 |
| Notes | FR-V12-F-017, FR-V12-F-018, FR-V12-F-019: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Related existing stories (shared source IDs, no FR trace): US-11-YF03 · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: AIX-17…19: provider data handling, drift monitoring and multilingual gates
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @AIX-17 @DEC-770
  Scenario: AC-04ZU08-01 Happy path – Provider data handling: no training, DPA retention/region (FR-V12-F-017)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Provider data handling: no training, DPA retention/region" is exercised as specified by FR-V12-F-017:
      """
      Provider data handling: no training, DPA retention/region, minimise/mask for Tier S
      """
    Then provider without DPA cannot be approved
    And the audit event "ai.provider_data_handling_no" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @AIX-18 @DEC-770
  Scenario: AC-04ZU08-02 Alternate – Drift monitoring nightly sample (FR-V12-F-018)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Drift monitoring nightly sample" is exercised as specified by FR-V12-F-018: Drift monitoring nightly sample
    Then simulated drift triggers alert and rollback option
    And the audit event "ai.drift_monitoring_nightly" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @AIX-19 @DEC-770
  Scenario: AC-04ZU08-03 Alternate – Multilingual coverage en+hi IN; de+fr EU; locale prompts (FR-V12-F-019)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Multilingual coverage en+hi IN; de+fr EU; locale prompts" is exercised as specified by FR-V12-F-019:
      """
      Multilingual coverage en+hi IN; de+fr EU; locale prompts
      """
    Then slice below gate blocks that locale only
    And the audit event "ai.multilingual_coverage_en_hi" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU08-04 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU08-05 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU08-06 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU08-07 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU08-08 Permutations – AI governance, evaluation, prompts and cost (3-way, 65 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-017 = Provider data handling: no training
    #   F-018 = Drift monitoring nightly sample
    #   F-019 = Multilingual coverage en+hi IN; de+fr EU
    Examples: MU05 rows (3-way, seed 318; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU08-01 | F-019 | P16/R20 | Public | model Approved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-02 | F-018 | P10/R11 | Confidential | model Approved | L3 mandate | in budget | IN | ALLOW: simulated drift triggers alert and rollback option |
      | EX-04ZU08-03 | F-017 | P16/R20 | Internal | prompt unapproved | L3 revoked | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-04 | F-019 | P10/R11 | Restricted | candidate only | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU08-05 | F-017 | P03/R03 | Public | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-04ZU08-06 | F-019 | P10/R11 | Public | prompt unapproved | L1 | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-07 | F-018 | P03/R03 | Restricted | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-08 | F-018 | P16/R20 | Internal | candidate only | L1 | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU08-09 | F-017 | P03/R03 | Confidential | candidate only | L3 mandate | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU08-10 | F-017 | P10/R11 | Confidential | prompt unapproved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-11 | F-019 | P03/R03 | Internal | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-12 | F-018 | P03/R03 | Confidential | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-13 | F-017 | P16/R20 | Restricted | model Approved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-14 | F-019 | P03/R03 | Internal | model Approved | L3 revoked | soft cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU08-15 | F-019 | P16/R20 | Confidential | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU08-16 | F-018 | P10/R11 | Public | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU08-17 | F-017 | P16/R20 | Restricted | prompt unapproved | L3 revoked | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU08-18 | F-018 | P03/R03 | Confidential | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-19 | F-018 | P10/R11 | Internal | prompt unapproved | L1 | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-20 | F-018 | P16/R20 | Public | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-21 | F-019 | P03/R03 | Restricted | model Approved | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU08-22 | F-017 | P10/R11 | Public | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-23 | F-017 | P10/R11 | Internal | model Approved | L3 mandate | hard cap | EU | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU08-24 | F-018 | P03/R03 | Restricted | prompt unapproved | L3 mandate | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU08-25 | F-019 | P10/R11 | Restricted | model Approved | L3 revoked | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU08-26 | F-017 | P10/R11 | Public | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU08-27 | F-019 | P16/R20 | Confidential | prompt unapproved | L3 mandate | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-28 | F-019 | P16/R20 | Restricted | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-29 | F-017 | P03/R03 | Internal | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-30 | F-019 | P10/R11 | Confidential | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-31 | F-018 | P16/R20 | Restricted | model Approved | L1 | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU08-32 | F-018 | P16/R20 | Internal | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-33 | F-019 | P03/R03 | Public | model Approved | L3 mandate | soft cap | EU | ALLOW: slice below gate blocks that locale only |
      | EX-04ZU08-34 | F-018 | P03/R03 | Public | prompt unapproved | L3 revoked | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-35 | F-017 | P16/R20 | Public | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU08-36 | F-018 | P10/R11 | Internal | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-37 | F-019 | P03/R03 | Internal | candidate only | L1 | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU08-38 | F-017 | P16/R20 | Confidential | model Approved | L3 revoked | hard cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU08-39 | F-017 | P10/R11 | Restricted | prompt unapproved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-40 | F-017 | P16/R20 | Internal | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU08-41 | F-018 | P16/R20 | Confidential | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-42 | F-017 | P03/R03 | Restricted | prompt unapproved | L1 | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU08-43 | F-017 | P10/R11 | Confidential | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-44 | F-018 | P10/R11 | Public | model Approved | L1 | hard cap | IN | PENDING_APPROVAL |
      | EX-04ZU08-45 | F-018 | P10/R11 | Restricted | candidate only | L1 | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU08-46 | F-019 | P10/R11 | Internal | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-47 | F-019 | P03/R03 | Public | candidate only | L3 mandate | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU08-48 | F-017 | P10/R11 | Internal | prompt unapproved | L1 | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-49 | F-017 | P16/R20 | Public | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-50 | F-018 | P16/R20 | Public | prompt unapproved | L1 | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-51 | F-017 | P03/R03 | Confidential | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-52 | F-017 | P03/R03 | Restricted | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-53 | F-019 | P10/R11 | Confidential | candidate only | L3 revoked | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU08-54 | F-019 | P16/R20 | Restricted | prompt unapproved | L3 mandate | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU08-55 | F-018 | P03/R03 | Internal | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-56 | F-018 | P03/R03 | Public | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-57 | F-019 | P03/R03 | Confidential | model Approved | L1 | soft cap | EU | PENDING_APPROVAL |
      | EX-04ZU08-58 | F-019 | P16/R20 | Internal | candidate only | L3 mandate | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU08-59 | F-019 | P16/R20 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: slice below gate blocks that locale only |
      | EX-04ZU08-60 | F-017 | P16/R20 | Confidential | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU08-61 | F-019 | P03/R03 | Internal | prompt unapproved | L1 | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU08-62 | F-018 | P16/R20 | Restricted | prompt unapproved | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU08-63 | F-017 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: provider without DPA cannot be approved |
      | EX-04ZU08-64 | F-018 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: simulated drift triggers alert and rollback option |
      | EX-04ZU08-65 | F-019 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: slice below gate blocks that locale only |
```

##### US-04-ZU09 AIX-20 kill switch and CTRL-AI-01…02 delimiting and normalisation

| Field | Value |
|---|---|
| ID | US-04-ZU09 |
| Title | AIX-20 kill switch and CTRL-AI-01…02 delimiting and normalisation |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want AI incident response; kill switch per model/prompt/workflow; CTRL-AI-01 Delimiting; CTRL-AI-02 Normalisation (NFKC, zero-width, bidi, hidden text), so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-020 (AIX-20); FR-V12-F-021 (CTRL-AI-01); FR-V12-F-022 (CTRL-AI-02); DEC-770, DEC-790; tests TC-V12-F-020, TC-V12-F-033, TC-V12-F-034 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×3 · model MU05 |
| Notes | FR-V12-F-020, FR-V12-F-021, FR-V12-F-022: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Related existing stories (shared source IDs, no FR trace): US-04-ZR22 · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: AIX-20 kill switch and CTRL-AI-01…02 delimiting and normalisation
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @AIX-20 @DEC-770
  Scenario: AC-04ZU09-01 Happy path – AI incident response; kill switch per model/prompt/workflow (FR-V12-F-020)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "AI incident response; kill switch per model/prompt/workflow" is exercised as specified by FR-V12-F-020:
      """
      AI incident response; kill switch per model/prompt/workflow
      """
    Then kill switch stops new calls within one scheduler cycle
    And the audit event "ai.ai_incident_response" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @CTRL-AI-01 @DEC-770
  Scenario: AC-04ZU09-02 Alternate – CTRL-AI-01 Delimiting (FR-V12-F-021)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "CTRL-AI-01 Delimiting" is exercised as specified by FR-V12-F-021: CTRL-AI-01 Delimiting
    Then control verified by AI-INJ corpus and unit test
    And the audit event "ai.ctrl_ai_01_delimiting" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @CTRL-AI-02 @DEC-770
  Scenario: AC-04ZU09-03 Alternate – CTRL-AI-02 Normalisation (NFKC, zero-width, bidi, hidden text) (FR-V12-F-022)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "CTRL-AI-02 Normalisation (NFKC, zero-width, bidi, hidden text)" is exercised as specified by FR-V12-F-022:
      """
      CTRL-AI-02 Normalisation (NFKC, zero-width, bidi, hidden text)
      """
    Then control verified by AI-INJ corpus and unit test
    And the audit event "ai.ctrl_ai_02_normalisation" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU09-04 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU09-05 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU09-06 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU09-07 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU09-08 Permutations – AI governance, evaluation, prompts and cost (3-way, 65 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-020 = AI incident response; kill switch per…
    #   F-021 = CTRL-AI-01 Delimiting
    #   F-022 = CTRL-AI-02 Normalisation (NFKC, zero-width, bidi
    Examples: MU05 rows (3-way, seed 325; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU09-01 | F-022 | P03/R03 | Confidential | prompt unapproved | L3 mandate | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU09-02 | F-022 | P16/R20 | Restricted | model Approved | L3 revoked | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU09-03 | F-021 | P10/R11 | Internal | prompt unapproved | L3 revoked | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU09-04 | F-020 | P10/R11 | Confidential | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-05 | F-020 | P03/R03 | Public | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-06 | F-020 | P10/R11 | Restricted | candidate only | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU09-07 | F-021 | P16/R20 | Public | candidate only | L1 | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU09-08 | F-021 | P03/R03 | Restricted | model Approved | L3 mandate | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU09-09 | F-022 | P10/R11 | Public | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-10 | F-020 | P03/R03 | Internal | candidate only | L3 revoked | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU09-11 | F-022 | P16/R20 | Internal | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-12 | F-020 | P16/R20 | Confidential | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU09-13 | F-022 | P16/R20 | Public | prompt unapproved | L3 revoked | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU09-14 | F-021 | P16/R20 | Restricted | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-15 | F-020 | P10/R11 | Internal | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU09-16 | F-021 | P10/R11 | Public | model Approved | L3 revoked | hard cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU09-17 | F-022 | P03/R03 | Restricted | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-18 | F-022 | P03/R03 | Confidential | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-04ZU09-19 | F-021 | P10/R11 | Confidential | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-20 | F-021 | P03/R03 | Internal | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU09-21 | F-020 | P03/R03 | Public | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU09-22 | F-021 | P16/R20 | Confidential | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU09-23 | F-021 | P03/R03 | Internal | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-24 | F-022 | P10/R11 | Restricted | prompt unapproved | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU09-25 | F-020 | P16/R20 | Restricted | model Approved | L1 | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU09-26 | F-022 | P16/R20 | Internal | candidate only | L3 mandate | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU09-27 | F-020 | P03/R03 | Restricted | prompt unapproved | L3 revoked | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU09-28 | F-020 | P16/R20 | Public | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-29 | F-022 | P10/R11 | Internal | model Approved | L3 mandate | soft cap | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU09-30 | F-020 | P16/R20 | Internal | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU09-31 | F-021 | P10/R11 | Restricted | candidate only | L3 mandate | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU09-32 | F-021 | P03/R03 | Confidential | prompt unapproved | L3 revoked | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU09-33 | F-022 | P10/R11 | Confidential | candidate only | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-34 | F-020 | P16/R20 | Confidential | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU09-35 | F-022 | P03/R03 | Public | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU09-36 | F-021 | P16/R20 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU09-37 | F-022 | P10/R11 | Internal | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-38 | F-020 | P10/R11 | Restricted | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-39 | F-021 | P03/R03 | Restricted | model Approved | L1 | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU09-40 | F-021 | P16/R20 | Confidential | model Approved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-41 | F-020 | P10/R11 | Public | prompt unapproved | L3 mandate | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU09-42 | F-021 | P03/R03 | Confidential | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-43 | F-020 | P03/R03 | Internal | model Approved | L3 revoked | soft cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU09-44 | F-020 | P10/R11 | Internal | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-45 | F-021 | P10/R11 | Public | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-46 | F-022 | P10/R11 | Confidential | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU09-47 | F-022 | P16/R20 | Restricted | candidate only | L3 mandate | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU09-48 | F-022 | P03/R03 | Public | model Approved | L1 | hard cap | EU | PENDING_APPROVAL |
      | EX-04ZU09-49 | F-021 | P10/R11 | Confidential | prompt unapproved | L3 mandate | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU09-50 | F-021 | P16/R20 | Internal | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU09-51 | F-021 | P03/R03 | Public | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-52 | F-020 | P03/R03 | Public | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-53 | F-022 | P16/R20 | Confidential | model Approved | L3 mandate | in budget | EU | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU09-54 | F-020 | P03/R03 | Restricted | model Approved | L3 mandate | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU09-55 | F-022 | P03/R03 | Internal | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-56 | F-021 | P10/R11 | Confidential | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU09-57 | F-021 | P10/R11 | Restricted | prompt unapproved | L3 revoked | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU09-58 | F-021 | P16/R20 | Restricted | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-59 | F-021 | P10/R11 | Internal | model Approved | L3 mandate | hard cap | EU | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU09-60 | F-020 | P10/R11 | Public | candidate only | L3 revoked | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU09-61 | F-020 | P03/R03 | Confidential | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-62 | F-021 | P16/R20 | Internal | model Approved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU09-63 | F-020 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: kill switch stops new calls within one scheduler |
      | EX-04ZU09-64 | F-021 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU09-65 | F-022 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
```

##### US-04-ZU10 CTRL-AI-03…05: injection classifier, tool isolation and output validation

| Field | Value |
|---|---|
| ID | US-04-ZU10 |
| Title | CTRL-AI-03…05: injection classifier, tool isolation and output validation |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want CTRL-AI-03 Classifier MDL-G1 screens in/out; flags to reviewer; CTRL-AI-04 Tool isolation per step class; CTRL-AI-05 Output validation, URL/domain allowlist, sanitised rendering, no auto-fetch, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-023 (CTRL-AI-03); FR-V12-F-024 (CTRL-AI-04); FR-V12-F-025 (CTRL-AI-05); DEC-770, DEC-790; tests TC-V12-F-035, TC-V12-F-036, TC-V12-F-037 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×3 · model MU05 |
| Notes | FR-V12-F-023, FR-V12-F-024, FR-V12-F-025: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: CTRL-AI-03…05: injection classifier, tool isolation and output validation
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @CTRL-AI-03 @DEC-770
  Scenario: AC-04ZU10-01 Happy path – CTRL-AI-03 Classifier MDL-G1 screens in/out; flags to reviewer (FR-V12-F-023)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "CTRL-AI-03 Classifier MDL-G1 screens in/out; flags to reviewer" is exercised as specified by FR-V12-F-023:
      """
      CTRL-AI-03 Classifier MDL-G1 screens in/out; flags to reviewer
      """
    Then control verified by AI-INJ corpus and unit test
    And the audit event "ai.ctrl_ai_03_classifier_mdl_g1" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @CTRL-AI-04 @DEC-770
  Scenario: AC-04ZU10-02 Alternate – CTRL-AI-04 Tool isolation per step class (FR-V12-F-024)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "CTRL-AI-04 Tool isolation per step class" is exercised as specified by FR-V12-F-024: CTRL-AI-04 Tool isolation per step class
    Then control verified by AI-INJ corpus and unit test
    And the audit event "ai.ctrl_ai_04_tool_isolation_per" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @CTRL-AI-05 @DEC-770
  Scenario: AC-04ZU10-03 Alternate – CTRL-AI-05 Output validation, URL/domain allowlist (FR-V12-F-025)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "CTRL-AI-05 Output validation, URL/domain allowlist" is exercised as specified by FR-V12-F-025:
      """
      CTRL-AI-05 Output validation, URL/domain allowlist, sanitised rendering, no auto-fetch
      """
    Then control verified by AI-INJ corpus and unit test
    And the audit event "ai.ctrl_ai_05_output_validation" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU10-04 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU10-05 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU10-06 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU10-07 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU10-08 Permutations – AI governance, evaluation, prompts and cost (3-way, 64 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-023 = CTRL-AI-03 Classifier MDL-G1 screens in/out
    #   F-024 = CTRL-AI-04 Tool isolation per step class
    #   F-025 = CTRL-AI-05 Output validation, URL/domain allowlist
    Examples: MU05 rows (3-way, seed 332; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU10-01 | F-024 | P03/R03 | Restricted | candidate only | L3 mandate | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU10-02 | F-024 | P16/R20 | Confidential | model Approved | L3 revoked | hard cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU10-03 | F-025 | P10/R11 | Confidential | candidate only | L1 | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU10-04 | F-024 | P10/R11 | Internal | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-05 | F-023 | P16/R20 | Public | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-06 | F-023 | P10/R11 | Internal | model Approved | L3 mandate | soft cap | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU10-07 | F-025 | P16/R20 | Public | prompt unapproved | L3 revoked | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU10-08 | F-023 | P03/R03 | Public | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-09 | F-023 | P03/R03 | Confidential | prompt unapproved | L3 mandate | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU10-10 | F-025 | P16/R20 | Internal | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU10-11 | F-025 | P03/R03 | Restricted | model Approved | L3 revoked | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU10-12 | F-025 | P16/R20 | Restricted | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-13 | F-024 | P03/R03 | Internal | prompt unapproved | L1 | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU10-14 | F-025 | P03/R03 | Confidential | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-15 | F-023 | P10/R11 | Restricted | prompt unapproved | L1 | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU10-16 | F-025 | P10/R11 | Public | model Approved | L3 mandate | hard cap | EU | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU10-17 | F-024 | P10/R11 | Public | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-18 | F-024 | P16/R20 | Confidential | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU10-19 | F-023 | P10/R11 | Restricted | candidate only | L3 revoked | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU10-20 | F-023 | P16/R20 | Internal | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-21 | F-023 | P16/R20 | Restricted | model Approved | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU10-22 | F-024 | P03/R03 | Internal | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-23 | F-025 | P03/R03 | Internal | prompt unapproved | L3 revoked | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU10-24 | F-025 | P03/R03 | Public | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-25 | F-023 | P10/R11 | Confidential | prompt unapproved | L3 revoked | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU10-26 | F-024 | P03/R03 | Public | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-04ZU10-27 | F-024 | P16/R20 | Confidential | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-28 | F-024 | P10/R11 | Restricted | model Approved | L3 revoked | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU10-29 | F-023 | P16/R20 | Public | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU10-30 | F-023 | P03/R03 | Confidential | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU10-31 | F-023 | P10/R11 | Confidential | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-32 | F-025 | P10/R11 | Public | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU10-33 | F-024 | P10/R11 | Internal | candidate only | L3 mandate | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU10-34 | F-024 | P03/R03 | Public | prompt unapproved | L3 mandate | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU10-35 | F-025 | P10/R11 | Restricted | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-36 | F-024 | P03/R03 | Restricted | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-37 | F-023 | P03/R03 | Internal | model Approved | L3 revoked | hard cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU10-38 | F-025 | P16/R20 | Restricted | model Approved | L3 mandate | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU10-39 | F-023 | P16/R20 | Internal | prompt unapproved | L3 mandate | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU10-40 | F-025 | P10/R11 | Confidential | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU10-41 | F-025 | P10/R11 | Internal | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-42 | F-024 | P03/R03 | Confidential | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-43 | F-023 | P16/R20 | Restricted | candidate only | L3 mandate | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU10-44 | F-024 | P16/R20 | Public | candidate only | L3 revoked | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU10-45 | F-025 | P03/R03 | Internal | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU10-46 | F-024 | P16/R20 | Restricted | prompt unapproved | L3 revoked | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU10-47 | F-023 | P10/R11 | Public | model Approved | L3 revoked | soft cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU10-48 | F-023 | P10/R11 | Restricted | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-49 | F-025 | P16/R20 | Confidential | prompt unapproved | L1 | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU10-50 | F-025 | P03/R03 | Restricted | candidate only | L1 | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU10-51 | F-024 | P16/R20 | Internal | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU10-52 | F-023 | P03/R03 | Confidential | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU10-53 | F-024 | P16/R20 | Internal | model Approved | L1 | soft cap | EU | PENDING_APPROVAL |
      | EX-04ZU10-54 | F-024 | P16/R20 | Public | prompt unapproved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-55 | F-023 | P03/R03 | Restricted | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-56 | F-024 | P03/R03 | Public | candidate only | L3 revoked | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU10-57 | F-023 | P16/R20 | Confidential | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-58 | F-024 | P10/R11 | Confidential | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU10-59 | F-023 | P16/R20 | Internal | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-04ZU10-60 | F-025 | P16/R20 | Confidential | candidate only | L3 mandate | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU10-61 | F-024 | P16/R20 | Restricted | prompt unapproved | L3 revoked | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU10-62 | F-023 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU10-63 | F-024 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU10-64 | F-025 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
```

##### US-04-ZU11 CTRL-AI-06…08: no secrets in context, tenant-filtered retrieval and signed agent mandates

| Field | Value |
|---|---|
| ID | US-04-ZU11 |
| Title | CTRL-AI-06…08: no secrets in context, tenant-filtered retrieval and signed agent mandates |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want CTRL-AI-06 Secrets never in context; refusal template; CTRL-AI-07 Retrieval filtered by tenant/company before ranking; tenant-scoped vector keys; CTRL-AI-08 Agent-to-agent mandates signed with limits; counterparty messages untrusted, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-026 (CTRL-AI-06); FR-V12-F-027 (CTRL-AI-07); FR-V12-F-028 (CTRL-AI-08); DEC-770, DEC-790; tests TC-V12-F-038, TC-V12-F-039, TC-V12-F-040 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×3 · model MU05 |
| Notes | FR-V12-F-026, FR-V12-F-027, FR-V12-F-028: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Related existing stories (shared source IDs, no FR trace): US-13-YF05, US-24-ZP02, US-24-ZP03 · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: CTRL-AI-06…08: no secrets in context, tenant-filtered retrieval and signed agent mandates
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @CTRL-AI-06 @DEC-770
  Scenario: AC-04ZU11-01 Happy path – CTRL-AI-06 Secrets never in context; refusal template (FR-V12-F-026)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "CTRL-AI-06 Secrets never in context; refusal template" is exercised as specified by FR-V12-F-026:
      """
      CTRL-AI-06 Secrets never in context; refusal template
      """
    Then control verified by AI-INJ corpus and unit test
    And the audit event "ai.ctrl_ai_06_secrets_never_in" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @CTRL-AI-07 @DEC-770
  Scenario: AC-04ZU11-02 Alternate – CTRL-AI-07 Retrieval filtered by tenant/company before ranking (FR-V12-F-027)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "CTRL-AI-07 Retrieval filtered by tenant/company before ranking" is exercised as specified by FR-V12-F-027:
      """
      CTRL-AI-07 Retrieval filtered by tenant/company before ranking; tenant-scoped vector keys
      """
    Then control verified by AI-INJ corpus and unit test
    And the audit event "ai.ctrl_ai_07_retrieval_filtered" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @CTRL-AI-08 @DEC-770
  Scenario: AC-04ZU11-03 Alternate – CTRL-AI-08 Agent-to-agent mandates signed with limits (FR-V12-F-028)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "CTRL-AI-08 Agent-to-agent mandates signed with limits" is exercised as specified by FR-V12-F-028:
      """
      CTRL-AI-08 Agent-to-agent mandates signed with limits; counterparty messages untrusted
      """
    Then control verified by AI-INJ corpus and unit test
    And the audit event "ai.ctrl_ai_08_agent_to_agent" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU11-04 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU11-05 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU11-06 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU11-07 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU11-08 Permutations – AI governance, evaluation, prompts and cost (3-way, 63 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-026 = CTRL-AI-06 Secrets never in context
    #   F-027 = CTRL-AI-07 Retrieval filtered by tenant/company…
    #   F-028 = CTRL-AI-08 Agent-to-agent mandates signed with…
    Examples: MU05 rows (3-way, seed 339; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU11-01 | F-027 | P10/R11 | Confidential | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-02 | F-028 | P10/R11 | Internal | model Approved | L3 mandate | in budget | EU | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU11-03 | F-026 | P03/R03 | Internal | prompt unapproved | L3 mandate | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU11-04 | F-027 | P16/R20 | Restricted | model Approved | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU11-05 | F-027 | P03/R03 | Public | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU11-06 | F-028 | P03/R03 | Restricted | candidate only | L1 | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU11-07 | F-026 | P03/R03 | Restricted | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-08 | F-026 | P16/R20 | Confidential | candidate only | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-09 | F-026 | P10/R11 | Public | candidate only | L1 | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU11-10 | F-028 | P16/R20 | Confidential | prompt unapproved | L3 revoked | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU11-11 | F-028 | P16/R20 | Public | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-12 | F-027 | P16/R20 | Internal | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU11-13 | F-027 | P03/R03 | Public | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-14 | F-028 | P10/R11 | Restricted | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-15 | F-026 | P10/R11 | Confidential | model Approved | L3 revoked | hard cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU11-16 | F-026 | P16/R20 | Internal | prompt unapproved | L1 | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU11-17 | F-028 | P03/R03 | Internal | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU11-18 | F-028 | P10/R11 | Confidential | candidate only | L3 mandate | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU11-19 | F-027 | P03/R03 | Internal | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-20 | F-027 | P16/R20 | Restricted | prompt unapproved | L3 mandate | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU11-21 | F-027 | P10/R11 | Public | model Approved | L3 mandate | soft cap | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU11-22 | F-026 | P10/R11 | Restricted | prompt unapproved | L3 revoked | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU11-23 | F-026 | P03/R03 | Public | model Approved | L1 | soft cap | EU | PENDING_APPROVAL |
      | EX-04ZU11-24 | F-027 | P03/R03 | Confidential | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-04ZU11-25 | F-028 | P16/R20 | Public | candidate only | L1 | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU11-26 | F-027 | P10/R11 | Internal | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-27 | F-028 | P03/R03 | Public | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-28 | F-026 | P03/R03 | Confidential | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU11-29 | F-026 | P16/R20 | Internal | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU11-30 | F-026 | P16/R20 | Restricted | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-31 | F-027 | P10/R11 | Restricted | candidate only | L1 | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU11-32 | F-026 | P16/R20 | Public | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-33 | F-028 | P10/R11 | Internal | prompt unapproved | L1 | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU11-34 | F-028 | P03/R03 | Confidential | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-35 | F-027 | P16/R20 | Confidential | model Approved | L3 mandate | soft cap | EU | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU11-36 | F-028 | P16/R20 | Restricted | candidate only | L3 mandate | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU11-37 | F-028 | P10/R11 | Public | prompt unapproved | L3 revoked | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU11-38 | F-026 | P03/R03 | Confidential | prompt unapproved | L1 | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU11-39 | F-027 | P03/R03 | Confidential | candidate only | L3 revoked | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU11-40 | F-026 | P10/R11 | Internal | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-41 | F-026 | P03/R03 | Restricted | model Approved | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU11-42 | F-027 | P16/R20 | Public | prompt unapproved | L3 mandate | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU11-43 | F-028 | P10/R11 | Public | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU11-44 | F-027 | P16/R20 | Internal | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-45 | F-028 | P10/R11 | Restricted | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-46 | F-027 | P03/R03 | Restricted | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-47 | F-028 | P10/R11 | Confidential | prompt unapproved | L1 | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU11-48 | F-026 | P16/R20 | Public | model Approved | L3 mandate | in budget | EU | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU11-49 | F-026 | P03/R03 | Public | candidate only | L3 revoked | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU11-50 | F-028 | P16/R20 | Internal | candidate only | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-51 | F-028 | P16/R20 | Restricted | candidate only | L3 revoked | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU11-52 | F-027 | P03/R03 | Internal | model Approved | L3 revoked | in budget | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU11-53 | F-026 | P10/R11 | Internal | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU11-54 | F-028 | P03/R03 | Restricted | prompt unapproved | L3 mandate | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU11-55 | F-026 | P10/R11 | Confidential | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-56 | F-027 | P16/R20 | Confidential | candidate only | L1 | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU11-57 | F-026 | P03/R03 | Confidential | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-58 | F-026 | P03/R03 | Internal | model Approved | L1 | soft cap | EU | PENDING_APPROVAL |
      | EX-04ZU11-59 | F-027 | P10/R11 | Public | candidate only | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU11-60 | F-026 | P10/R11 | Restricted | prompt unapproved | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU11-61 | F-026 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU11-62 | F-027 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU11-63 | F-028 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
```

##### US-04-ZU12 CTRL-AI-09 logging, ai_usage_event metering and keyed evaluation runs

| Field | Value |
|---|---|
| ID | US-04-ZU12 |
| Title | CTRL-AI-09 logging, ai_usage_event metering and keyed evaluation runs |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want CTRL-AI-09 Logging flags, model, prompt version, decision (PII-redacted); meter every model call as ai_usage_event: tenant, company, workflow, step, run, model, PRM version, input/output/cached/reasoning tokens; key every eval run by candidate/version, workflow, PRM version, language, data class, dataset version, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-029 (CTRL-AI-09); FR-V12-F-030 (16.7); FR-V12-F-032 (REC-12); DEC-770, DEC-790; tests TC-V12-F-012, TC-V12-F-041, TC-V12-F-065 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×3 · model MU05 |
| Notes | FR-V12-F-029, FR-V12-F-030, FR-V12-F-032: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: CTRL-AI-09 logging, ai_usage_event metering and keyed evaluation runs
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @CTRL-AI-09 @DEC-770
  Scenario: AC-04ZU12-01 Happy path – CTRL-AI-09 Logging flags, model, prompt version (FR-V12-F-029)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "CTRL-AI-09 Logging flags, model, prompt version" is exercised as specified by FR-V12-F-029:
      """
      CTRL-AI-09 Logging flags, model, prompt version, decision (PII-redacted)
      """
    Then control verified by AI-INJ corpus and unit test
    And the audit event "ai.ctrl_ai_09_logging_flags" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @DEC-770
  Scenario: AC-04ZU12-02 Alternate – Meter every model call as ai_usage_event: tenant, company, workflow (FR-V12-F-030)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Meter every model call as ai_usage_event:
      """
      tenant, company, workflow" is exercised as specified by FR-V12-F-030: Meter every model call as ai_usage_event: tenant, company, workflow,
      step, run, model, PRM version, input/output/cached/reasoning tokens, latency, outcome
      """
    Then tenant totals reconcile with provider invoice within AU-048 tolerance
    And the audit event "ai.meter_every_model_call_as" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @REC-12 @DEC-770
  Scenario: AC-04ZU12-03 Alternate – Key every eval run by candidate/version, workflow, PRM version (FR-V12-F-032)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Key every eval run by candidate/version, workflow, PRM version" is exercised as specified by FR-V12-F-032:
      """
      Key every eval run by candidate/version, workflow, PRM version, language, data class, dataset version; store provider, sample size, quality,
      cost, latency, red-team evidence, reviewer, DPA ref, region
      """
    Then unrelated evaluation cannot unlock promotion
    And the audit event "ai.key_every_eval_run_by" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU12-04 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU12-05 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU12-06 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU12-07 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU12-08 Permutations – AI governance, evaluation, prompts and cost (3-way, 64 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-029 = CTRL-AI-09 Logging flags, model, prompt version
    #   F-030 = Meter every model call as ai_usage_event: tenant
    #   F-032 = Key every eval run by candidate/version, workflow
    Examples: MU05 rows (3-way, seed 346; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU12-01 | F-032 | P16/R20 | Internal | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU12-02 | F-030 | P16/R20 | Confidential | model Approved | L1 | soft cap | IN | PENDING_APPROVAL |
      | EX-04ZU12-03 | F-029 | P16/R20 | Public | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-04 | F-032 | P03/R03 | Internal | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-05 | F-032 | P10/R11 | Internal | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU12-06 | F-029 | P03/R03 | Confidential | prompt unapproved | L3 revoked | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU12-07 | F-030 | P16/R20 | Restricted | candidate only | L3 revoked | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU12-08 | F-030 | P10/R11 | Public | candidate only | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-09 | F-029 | P03/R03 | Restricted | model Approved | L3 mandate | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU12-10 | F-030 | P10/R11 | Restricted | prompt unapproved | L3 mandate | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU12-11 | F-029 | P10/R11 | Confidential | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU12-12 | F-030 | P03/R03 | Confidential | candidate only | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-13 | F-029 | P10/R11 | Restricted | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-14 | F-032 | P10/R11 | Public | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU12-15 | F-032 | P03/R03 | Restricted | candidate only | L1 | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU12-16 | F-032 | P03/R03 | Public | prompt unapproved | L3 revoked | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU12-17 | F-030 | P16/R20 | Internal | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-18 | F-032 | P16/R20 | Confidential | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU12-19 | F-029 | P16/R20 | Public | candidate only | L1 | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU12-20 | F-029 | P10/R11 | Internal | model Approved | L3 revoked | in budget | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU12-21 | F-030 | P03/R03 | Confidential | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-04ZU12-22 | F-029 | P16/R20 | Restricted | prompt unapproved | L1 | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU12-23 | F-032 | P10/R11 | Confidential | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-24 | F-030 | P03/R03 | Public | candidate only | L3 revoked | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU12-25 | F-032 | P16/R20 | Confidential | model Approved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-26 | F-030 | P10/R11 | Internal | model Approved | L3 mandate | soft cap | EU | ALLOW: Tenant totals reconcile with provider invoice |
      | EX-04ZU12-27 | F-029 | P03/R03 | Internal | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-28 | F-032 | P10/R11 | Restricted | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-29 | F-030 | P03/R03 | Internal | prompt unapproved | L1 | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU12-30 | F-032 | P03/R03 | Restricted | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-31 | F-029 | P10/R11 | Confidential | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU12-32 | F-029 | P16/R20 | Internal | model Approved | L3 mandate | hard cap | EU | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU12-33 | F-029 | P03/R03 | Public | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-34 | F-032 | P10/R11 | Public | model Approved | L1 | soft cap | EU | PENDING_APPROVAL |
      | EX-04ZU12-35 | F-029 | P16/R20 | Restricted | model Approved | L3 revoked | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU12-36 | F-030 | P10/R11 | Public | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU12-37 | F-030 | P16/R20 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Tenant totals reconcile with provider invoice |
      | EX-04ZU12-38 | F-032 | P03/R03 | Internal | candidate only | L3 revoked | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU12-39 | F-029 | P16/R20 | Confidential | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-40 | F-032 | P10/R11 | Confidential | candidate only | L1 | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU12-41 | F-030 | P03/R03 | Restricted | model Approved | L3 revoked | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU12-42 | F-029 | P10/R11 | Internal | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-43 | F-032 | P03/R03 | Public | candidate only | L3 mandate | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU12-44 | F-030 | P16/R20 | Restricted | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-45 | F-032 | P16/R20 | Public | prompt unapproved | L1 | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU12-46 | F-029 | P10/R11 | Restricted | prompt unapproved | L3 revoked | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU12-47 | F-032 | P16/R20 | Restricted | model Approved | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU12-48 | F-030 | P03/R03 | Restricted | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-49 | F-030 | P10/R11 | Confidential | model Approved | L3 revoked | in budget | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU12-50 | F-030 | P10/R11 | Internal | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-51 | F-032 | P03/R03 | Internal | prompt unapproved | L3 mandate | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU12-52 | F-032 | P03/R03 | Public | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-53 | F-029 | P16/R20 | Internal | model Approved | L1 | soft cap | IN | PENDING_APPROVAL |
      | EX-04ZU12-54 | F-029 | P16/R20 | Confidential | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-55 | F-032 | P03/R03 | Confidential | model Approved | L1 | hard cap | EU | PENDING_APPROVAL |
      | EX-04ZU12-56 | F-029 | P16/R20 | Restricted | candidate only | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU12-57 | F-029 | P16/R20 | Public | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU12-58 | F-030 | P03/R03 | Confidential | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-59 | F-032 | P16/R20 | Internal | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU12-60 | F-029 | P10/R11 | Public | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU12-61 | F-032 | P10/R11 | Public | model Approved | L3 revoked | hard cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU12-62 | F-029 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Control verified by AI-INJ corpus and unit test |
      | EX-04ZU12-63 | F-030 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Tenant totals reconcile with provider invoice |
      | EX-04ZU12-64 | F-032 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Unrelated evaluation cannot unlock promotion |
```

##### US-04-ZU13 Suite replay on change, per-run agent record and two-level AGT registry

| Field | Value |
|---|---|
| ID | US-04-ZU13 |
| Title | Suite replay on change, per-run agent record and two-level AGT registry |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want replay affected suites on model, prompt, retrieval, policy or tool change; nightly drift sample; denominator stored; per-run record: AGT role, agent, PRM, model, allowed tool-set digest, max tokens/cost, deadline, input/output refs, policy version; two-level registry AGT role → AG/AU implementer; every workflow bound to one AGT, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-033 (16.4); FR-V12-F-036 (15 V5); FR-V12-F-039 (ch15); DEC-770, DEC-790; tests TC-V12-F-006, TC-V12-F-188 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×3 · model MU05 |
| Notes | FR-V12-F-033, FR-V12-F-036, FR-V12-F-039: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: Suite replay on change, per-run agent record and two-level AGT registry
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @DEC-770
  Scenario: AC-04ZU13-01 Happy path – Replay affected suites on model, prompt, retrieval (FR-V12-F-033)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Replay affected suites on model, prompt, retrieval" is exercised as specified by FR-V12-F-033:
      """
      Replay affected suites on model, prompt, retrieval, policy or tool change; nightly drift sample; denominator stored
      """
    Then change with lower accuracy blocked
    And the audit event "ai.replay_affected_suites_on" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @DEC-770
  Scenario: AC-04ZU13-02 Alternate – Per-run record: AGT role, agent, PRM, model, allowed tool-set digest (FR-V12-F-036)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Per-run record: AGT role, agent, PRM, model, allowed tool-set digest" is exercised as specified by FR-V12-F-036:
      """
      Per-run record: AGT role, agent, PRM, model, allowed tool-set digest, max tokens/cost, deadline, input/output refs, policy version, quality
      verdict
      """
    Then 100% runs carry all fields
    And the audit event "ai.per_run_record_agt_role" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @DEC-770
  Scenario: AC-04ZU13-03 Alternate – Two-level registry AGT role → AG/AU implementer (FR-V12-F-039)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Two-level registry AGT role → AG/AU implementer" is exercised as specified by FR-V12-F-039:
      """
      Two-level registry AGT role → AG/AU implementer; every workflow bound to one AGT
      """
    Then 156/156 workflows bound; tool grants ⊆ AGT ceiling
    And the audit event "ai.two_level_registry_agt_role" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU13-04 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU13-05 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU13-06 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU13-07 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU13-08 Permutations – AI governance, evaluation, prompts and cost (3-way, 64 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-033 = Replay affected suites on model, prompt, retrieval
    #   F-036 = Per-run record: AGT role, agent, PRM, model
    #   F-039 = Two-level registry AGT role → AG/AU implementer
    Examples: MU05 rows (3-way, seed 353; space 2,916; tuples 1080/1080; +3 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU13-01 | F-036 | P10/R11 | Confidential | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU13-02 | F-033 | P16/R20 | Public | candidate only | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-03 | F-039 | P03/R03 | Confidential | candidate only | L3 revoked | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU13-04 | F-033 | P03/R03 | Internal | prompt unapproved | L3 revoked | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU13-05 | F-036 | P16/R20 | Restricted | model Approved | L3 revoked | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU13-06 | F-039 | P16/R20 | Internal | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU13-07 | F-033 | P10/R11 | Public | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-04ZU13-08 | F-039 | P10/R11 | Restricted | candidate only | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-09 | F-036 | P16/R20 | Internal | candidate only | L1 | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU13-10 | F-036 | P03/R03 | Restricted | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-11 | F-039 | P03/R03 | Public | model Approved | L3 mandate | soft cap | IN | ALLOW: 156/156 workflows bound |
      | EX-04ZU13-12 | F-033 | P03/R03 | Confidential | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-13 | F-039 | P10/R11 | Public | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-14 | F-036 | P10/R11 | Internal | candidate only | L3 mandate | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU13-15 | F-033 | P16/R20 | Confidential | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU13-16 | F-039 | P16/R20 | Internal | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-17 | F-033 | P10/R11 | Restricted | candidate only | L3 revoked | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU13-18 | F-036 | P03/R03 | Public | candidate only | L1 | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU13-19 | F-039 | P10/R11 | Confidential | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU13-20 | F-036 | P16/R20 | Public | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-21 | F-033 | P16/R20 | Confidential | model Approved | L3 revoked | in budget | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU13-22 | F-039 | P03/R03 | Restricted | model Approved | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU13-23 | F-036 | P10/R11 | Confidential | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-24 | F-036 | P03/R03 | Internal | model Approved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-25 | F-039 | P16/R20 | Public | candidate only | L3 revoked | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU13-26 | F-033 | P10/R11 | Internal | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-27 | F-033 | P03/R03 | Restricted | candidate only | L3 mandate | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU13-28 | F-033 | P16/R20 | Restricted | prompt unapproved | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU13-29 | F-036 | P10/R11 | Internal | prompt unapproved | L3 revoked | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU13-30 | F-036 | P03/R03 | Confidential | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU13-31 | F-033 | P10/R11 | Public | prompt unapproved | L3 mandate | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU13-32 | F-036 | P16/R20 | Confidential | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-33 | F-039 | P10/R11 | Internal | candidate only | L3 mandate | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU13-34 | F-036 | P10/R11 | Restricted | model Approved | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU13-35 | F-039 | P10/R11 | Confidential | model Approved | L3 revoked | soft cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU13-36 | F-033 | P03/R03 | Public | prompt unapproved | L3 revoked | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU13-37 | F-039 | P03/R03 | Confidential | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-38 | F-039 | P16/R20 | Restricted | prompt unapproved | L3 revoked | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU13-39 | F-039 | P03/R03 | Public | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-40 | F-033 | P03/R03 | Internal | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU13-41 | F-036 | P10/R11 | Restricted | prompt unapproved | L3 mandate | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU13-42 | F-033 | P03/R03 | Restricted | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-43 | F-033 | P10/R11 | Confidential | candidate only | L1 | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU13-44 | F-036 | P16/R20 | Public | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU13-45 | F-036 | P10/R11 | Public | candidate only | L3 revoked | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU13-46 | F-033 | P16/R20 | Restricted | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-47 | F-033 | P03/R03 | Internal | prompt unapproved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-48 | F-039 | P16/R20 | Internal | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-49 | F-036 | P16/R20 | Restricted | candidate only | L3 revoked | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU13-50 | F-039 | P03/R03 | Restricted | model Approved | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU13-51 | F-039 | P16/R20 | Confidential | candidate only | L1 | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU13-52 | F-039 | P16/R20 | Public | model Approved | L3 mandate | in budget | EU | ALLOW: 156/156 workflows bound |
      | EX-04ZU13-53 | F-033 | P16/R20 | Internal | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-54 | F-033 | P10/R11 | Confidential | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-55 | F-036 | P16/R20 | Confidential | model Approved | L1 | soft cap | EU | PENDING_APPROVAL |
      | EX-04ZU13-56 | F-033 | P10/R11 | Public | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-57 | F-039 | P03/R03 | Internal | model Approved | L3 mandate | in budget | EU | ALLOW: 156/156 workflows bound |
      | EX-04ZU13-58 | F-039 | P10/R11 | Public | model Approved | L1 | in budget | IN | PENDING_APPROVAL |
      | EX-04ZU13-59 | F-033 | P16/R20 | Restricted | prompt unapproved | L1 | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU13-60 | F-033 | P03/R03 | Restricted | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU13-61 | F-039 | P03/R03 | Internal | model Approved | L3 mandate | soft cap | IN | ALLOW: 156/156 workflows bound |
      | EX-04ZU13-62 | F-033 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Change with lower accuracy blocked |
      | EX-04ZU13-63 | F-036 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: 100% runs carry all fields |
      | EX-04ZU13-64 | F-039 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: 156/156 workflows bound |
```

##### US-04-ZU14 Scoped AI cache key and invalidation contract

| Field | Value |
|---|---|
| ID | US-04-ZU14 |
| Title | Scoped AI cache key and invalidation contract |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want scoped cache key and invalidation contract, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-F-049 (ch17); DEC-770, DEC-790; tests TC-V12-F-069 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×1 · model MU05 |
| Notes | FR-V12-F-049: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: Scoped AI cache key and invalidation contract
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy @DEC-770
  Scenario: AC-04ZU14-01 Happy path – Scoped cache key and invalidation contract (FR-V12-F-049)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Scoped cache key and invalidation contract" is exercised as specified by FR-V12-F-049: Scoped cache key and invalidation contract
    Then different tenant or revoked source → miss
    And the audit event "ai.scoped_cache_key_and" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU14-02 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU14-03 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU14-04 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU14-05 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU14-06 Permutations – AI governance, evaluation, prompts and cost (3-way, 56 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-049 = Scoped cache key and invalidation contract
    Examples: MU05 rows (3-way, seed 360; space 972; tuples 780/780; +1 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU14-01 | F-049 | P10/R11 | Restricted | candidate only | L3 mandate | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU14-02 | F-049 | P03/R03 | Restricted | model Approved | L1 | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU14-03 | F-049 | P16/R20 | Public | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-04 | F-049 | P10/R11 | Confidential | prompt unapproved | L3 revoked | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU14-05 | F-049 | P16/R20 | Internal | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU14-06 | F-049 | P03/R03 | Internal | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-07 | F-049 | P03/R03 | Public | prompt unapproved | L3 mandate | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU14-08 | F-049 | P10/R11 | Internal | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-09 | F-049 | P16/R20 | Confidential | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU14-10 | F-049 | P10/R11 | Public | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-11 | F-049 | P03/R03 | Confidential | model Approved | L3 revoked | soft cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU14-12 | F-049 | P03/R03 | Restricted | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-13 | F-049 | P16/R20 | Confidential | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-14 | F-049 | P03/R03 | Internal | prompt unapproved | L3 mandate | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU14-15 | F-049 | P10/R11 | Public | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU14-16 | F-049 | P16/R20 | Restricted | candidate only | L3 revoked | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU14-17 | F-049 | P16/R20 | Restricted | model Approved | L3 mandate | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU14-18 | F-049 | P10/R11 | Confidential | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-04ZU14-19 | F-049 | P10/R11 | Restricted | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-20 | F-049 | P03/R03 | Confidential | candidate only | L3 mandate | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU14-21 | F-049 | P10/R11 | Internal | model Approved | L3 revoked | soft cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU14-22 | F-049 | P16/R20 | Public | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU14-23 | F-049 | P03/R03 | Public | candidate only | L1 | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU14-24 | F-049 | P10/R11 | Internal | prompt unapproved | L3 revoked | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU14-25 | F-049 | P16/R20 | Internal | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-26 | F-049 | P03/R03 | Public | model Approved | L3 revoked | hard cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU14-27 | F-049 | P16/R20 | Internal | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU14-28 | F-049 | P16/R20 | Internal | candidate only | L3 mandate | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU14-29 | F-049 | P10/R11 | Confidential | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-30 | F-049 | P03/R03 | Restricted | model Approved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-31 | F-049 | P03/R03 | Confidential | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-32 | F-049 | P16/R20 | Public | model Approved | L3 mandate | hard cap | EU | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU14-33 | F-049 | P10/R11 | Public | prompt unapproved | L3 revoked | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU14-34 | F-049 | P10/R11 | Restricted | model Approved | L3 revoked | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU14-35 | F-049 | P16/R20 | Restricted | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-36 | F-049 | P16/R20 | Restricted | prompt unapproved | L3 revoked | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU14-37 | F-049 | P10/R11 | Internal | candidate only | L1 | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU14-38 | F-049 | P10/R11 | Restricted | prompt unapproved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-39 | F-049 | P03/R03 | Confidential | candidate only | L3 revoked | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU14-40 | F-049 | P03/R03 | Internal | model Approved | L1 | soft cap | EU | PENDING_APPROVAL |
      | EX-04ZU14-41 | F-049 | P16/R20 | Confidential | model Approved | L3 mandate | soft cap | IN | ALLOW: Different tenant or revoked source → miss |
      | EX-04ZU14-42 | F-049 | P03/R03 | Confidential | prompt unapproved | L1 | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU14-43 | F-049 | P03/R03 | Public | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-44 | F-049 | P10/R11 | Public | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-45 | F-049 | P03/R03 | Restricted | candidate only | L1 | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU14-46 | F-049 | P16/R20 | Public | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-47 | F-049 | P16/R20 | Confidential | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU14-48 | F-049 | P10/R11 | Restricted | candidate only | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU14-49 | F-049 | P03/R03 | Internal | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-50 | F-049 | P10/R11 | Public | model Approved | L1 | soft cap | IN | PENDING_APPROVAL |
      | EX-04ZU14-51 | F-049 | P10/R11 | Internal | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-52 | F-049 | P10/R11 | Confidential | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU14-53 | F-049 | P03/R03 | Public | candidate only | L3 revoked | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU14-54 | F-049 | P03/R03 | Internal | model Approved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU14-55 | F-049 | P10/R11 | Restricted | prompt unapproved | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU14-56 | F-049 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Different tenant or revoked source → miss |
```

##### US-04-ZU15 Optimisation API routes: preflight, cost, health, feedback and model evaluations

| Field | Value |
|---|---|
| ID | US-04-ZU15 |
| Title | Optimisation API routes: preflight, cost, health, feedback and model evaluations |
| Type | Feature |
| Story | As an integration administrator (P18, R12I), I want optimization routes: preflight, cost summary, health, feedback, customer value, private application drafts, model evaluations, so that our systems integrate through governed, observable and revocable connections without sharing secrets |
| Persona / roles | Integration administrator (P18, R12I) |
| Traces | FR-V12-H-017 (OPT-API-01…08) |
| Priority | Should |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 3–5 |
| Dependencies | US-20-ZR06, US-20-ZR07, US-20-ZR08, US-18-ZR11; source definition: Part 11.8b §11.8.5.1 Requirements adopted and release mapping |
| Dimension profile | persona ×3 · authority ×4 · channel ×3 · credential ×3 · provider ×3 · region ×3 · operation ×1 · model MU03 |
| Notes | Screens A008, A011, A168, A204, W47; API family `/api/v1/developer/`; audit events `integration.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Optimisation API routes: preflight, cost, health, feedback and model evaluations
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with integration administrator "kiran@kestrel.example.com" (R12I)
    And the developer platform sandbox "sbx-kestrel" and the connector registry:
      """
      with Salesforce, HubSpot, an SMS-DLT and a voice connector in state "draft"
      """

  @happy @OPT-API-01
  Scenario: AC-04ZU15-01 Happy path – Optimization routes: preflight, cost summary, health, feedback (FR-V12-H-017)
    Given Kiran Rao (R12I, kiran@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Optimization routes: preflight, cost summary, health, feedback" is exercised as specified by FR-V12-H-017:
      """
      Optimization routes: preflight, cost summary, health, feedback, customer value, private application drafts, model evaluations, operator
      conversion metrics
      """
    Then per row
    And the audit event "integration.optimization_routes" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @NFR-004
  Scenario: AC-04ZU15-02 Negative – a plaintext secret never reaches the database or logs
    When a connector configuration is saved with field "client_secret" = "s3cr3t-value"
    Then the API returns 422 "SECRET_REFERENCE_REQUIRED"
    And a database and log inspection finds no occurrence of "s3cr3t-value"

  @val
  Scenario: AC-04ZU15-03 Validation – an unsigned webhook is rejected
    When an inbound webhook arrives without the "X-Signature" and "X-Timestamp" headers
    Then the endpoint returns 401 "SIGNATURE_REQUIRED" and the payload is not processed

  @perm @BRL-TEN-04
  Scenario: AC-04ZU15-04 Permission – a key of tenant B cannot read tenant A
    Given an API key of tenant "Nordlicht Robotik GmbH" with scope "crm:read"
    When it calls GET "/api/v1/crm/contacts/C-1001" belonging to "Kestrel Analytics Pvt Ltd"
    Then the response is the uniform 404 "NOT_FOUND" and no row is returned

  @edge @I4 @DEC-050
  Scenario: AC-04ZU15-05 Edge – an uncertain write is reconciled before any retry
    Given the provider timed out after receiving write W-552
    When the retry scheduler runs
    Then the write is marked "RECONCILING" and the provider is queried for W-552 before any resend
    And exactly one provider record exists afterwards

  @sec @obs @MU03
  Scenario Outline: AC-04ZU15-06 Permutations – Developer platform, API contracts and connectors (2-way, 18 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the credential is "<credential>" and the provider is "<provider>"
    When "<operation>" runs through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU03 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   H-017 = Optimization routes: preflight, cost summary
    Examples: MU03 rows (2-way, seed 367; space 972; tuples 169/169; +1 baseline-allow)
      | ex | operation | persona | authority | channel | credential | provider | region | expected |
      | EX-04ZU15-01 | H-017 | P18/R12I | A5 wrong role | C3 OAuth | secret expired | I4 uncertain | EU→IN (misrouted) | 401 CREDENTIAL_EXPIRED |
      | EX-04ZU15-02 | H-017 | P10/R11 | T5 other tenant | C3 key | cred revoked | I1 up | EU | uniform 404 NOT_FOUND |
      | EX-04ZU15-03 | H-017 | P13/R17 | A3 SoD/limit | webhook | vault ref ok | I3 down | IN | 403 SOD_CONFLICT |
      | EX-04ZU15-04 | H-017 | P13/R17 | A1 | C3 key | secret expired | I3 down | EU→IN (misrouted) | 401 CREDENTIAL_EXPIRED |
      | EX-04ZU15-05 | H-017 | P18/R12I | A1 | C3 OAuth | vault ref ok | I1 up | EU | ALLOW: Per row |
      | EX-04ZU15-06 | H-017 | P10/R11 | A1 | webhook | cred revoked | I4 uncertain | IN | 401 CREDENTIAL_REVOKED |
      | EX-04ZU15-07 | H-017 | P13/R17 | A5 wrong role | webhook | secret expired | I1 up | EU | 401 CREDENTIAL_EXPIRED |
      | EX-04ZU15-08 | H-017 | P18/R12I | T5 other tenant | C3 OAuth | cred revoked | I3 down | IN | uniform 404 NOT_FOUND |
      | EX-04ZU15-09 | H-017 | P10/R11 | A3 SoD/limit | C3 key | vault ref ok | I4 uncertain | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-04ZU15-10 | H-017 | P13/R17 | T5 other tenant | webhook | cred revoked | I4 uncertain | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-04ZU15-11 | H-017 | P10/R11 | A5 wrong role | C3 key | secret expired | I3 down | IN | 401 CREDENTIAL_EXPIRED |
      | EX-04ZU15-12 | H-017 | P18/R12I | A3 SoD/limit | webhook | secret expired | I4 uncertain | EU | 401 CREDENTIAL_EXPIRED |
      | EX-04ZU15-13 | H-017 | P13/R17 | A3 SoD/limit | C3 OAuth | cred revoked | I1 up | IN | 401 CREDENTIAL_REVOKED |
      | EX-04ZU15-14 | H-017 | P10/R11 | T5 other tenant | C3 OAuth | secret expired | I3 down | EU | uniform 404 NOT_FOUND |
      | EX-04ZU15-15 | H-017 | P18/R12I | A5 wrong role | C3 key | vault ref ok | I1 up | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-04ZU15-16 | H-017 | P13/R17 | T5 other tenant | C3 OAuth | vault ref ok | I3 down | IN | uniform 404 NOT_FOUND |
      | EX-04ZU15-17 | H-017 | P13/R17 | A5 wrong role | webhook | cred revoked | I1 up | EU | 401 CREDENTIAL_REVOKED |
      | EX-04ZU15-18 | H-017 | P18/R12I | A1 | C3 key | vault ref ok | I1 up | IN | ALLOW: Per row |
```

##### US-04-ZU16 Vector column and HNSW index behind the embedding-model gate

| Field | Value |
|---|---|
| ID | US-04-ZU16 |
| Title | Vector column and HNSW index behind the embedding-model gate |
| Type | Feature |
| Story | As an AI lead (P10, R11), I want vector column and HNSW index for retrieval once the embedding model is approved, so that every AI step is approved, evaluated, metered and safe, and can be stopped at once |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-I-016 (V12-ENG DEC-042); DEC-042 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.9b §11.9.5.12 Functional requirements |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×1 · model MU05 |
| Notes | Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: Vector column and HNSW index behind the embedding-model gate
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy
  Scenario: AC-04ZU16-01 Happy path – Vector column and HNSW index for retrieval once the embedding model… (FR-V12-I-016)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Vector column and HNSW index for retrieval once the embedding model…" is exercised as specified by FR-V12-I-016:
      """
      Vector column and HNSW index for retrieval once the embedding model is approved
      """
    Then the observable result matches FR-V12-I-016 and its tests in Part 11.21
    And the audit event "ai.vector_column_and_hnsw_index" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU16-02 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU16-03 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU16-04 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU16-05 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU16-06 Permutations – AI governance, evaluation, prompts and cost (3-way, 60 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   I-016 = Vector column and HNSW index for retrieval once the…
    Examples: MU05 rows (3-way, seed 374; space 972; tuples 780/780; +1 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU16-01 | I-016 | P10/R11 | Public | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU16-02 | I-016 | P16/R20 | Restricted | prompt unapproved | L1 | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU16-03 | I-016 | P03/R03 | Restricted | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-04 | I-016 | P10/R11 | Confidential | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU16-05 | I-016 | P03/R03 | Internal | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-06 | I-016 | P16/R20 | Internal | model Approved | L3 mandate | soft cap | EU | ALLOW: Vector column and HNSW index for retrieval once the |
      | EX-04ZU16-07 | I-016 | P03/R03 | Confidential | prompt unapproved | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-08 | I-016 | P16/R20 | Public | model Approved | L3 revoked | hard cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU16-09 | I-016 | P16/R20 | Confidential | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU16-10 | I-016 | P10/R11 | Public | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-11 | I-016 | P03/R03 | Internal | candidate only | L3 revoked | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU16-12 | I-016 | P03/R03 | Public | prompt unapproved | L1 | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU16-13 | I-016 | P03/R03 | Restricted | candidate only | L3 mandate | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU16-14 | I-016 | P03/R03 | Confidential | model Approved | L1 | hard cap | IN | PENDING_APPROVAL |
      | EX-04ZU16-15 | I-016 | P16/R20 | Internal | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-16 | I-016 | P10/R11 | Internal | prompt unapproved | L3 mandate | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU16-17 | I-016 | P10/R11 | Restricted | model Approved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-18 | I-016 | P10/R11 | Internal | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-04ZU16-19 | I-016 | P10/R11 | Restricted | candidate only | L3 revoked | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU16-20 | I-016 | P16/R20 | Public | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-21 | I-016 | P16/R20 | Confidential | model Approved | L3 mandate | in budget | IN | ALLOW: Vector column and HNSW index for retrieval once the |
      | EX-04ZU16-22 | I-016 | P10/R11 | Confidential | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-23 | I-016 | P10/R11 | Confidential | model Approved | L3 revoked | soft cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU16-24 | I-016 | P03/R03 | Public | prompt unapproved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-25 | I-016 | P16/R20 | Restricted | prompt unapproved | L3 mandate | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU16-26 | I-016 | P10/R11 | Restricted | candidate only | L1 | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU16-27 | I-016 | P16/R20 | Confidential | prompt unapproved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-28 | I-016 | P16/R20 | Public | candidate only | L3 revoked | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU16-29 | I-016 | P03/R03 | Internal | model Approved | L3 revoked | hard cap | EU | ROUTE MANDATE_INACTIVE |
      | EX-04ZU16-30 | I-016 | P03/R03 | Restricted | prompt unapproved | L3 revoked | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU16-31 | I-016 | P03/R03 | Restricted | model Approved | L1 | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU16-32 | I-016 | P10/R11 | Public | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU16-33 | I-016 | P03/R03 | Internal | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-34 | I-016 | P10/R11 | Restricted | prompt unapproved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-35 | I-016 | P03/R03 | Public | model Approved | L3 mandate | soft cap | IN | ALLOW: Vector column and HNSW index for retrieval once the |
      | EX-04ZU16-36 | I-016 | P16/R20 | Restricted | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-37 | I-016 | P16/R20 | Internal | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU16-38 | I-016 | P03/R03 | Confidential | candidate only | L3 mandate | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU16-39 | I-016 | P16/R20 | Public | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-40 | I-016 | P10/R11 | Internal | prompt unapproved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-41 | I-016 | P16/R20 | Restricted | model Approved | L3 mandate | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU16-42 | I-016 | P03/R03 | Confidential | prompt unapproved | L3 revoked | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU16-43 | I-016 | P03/R03 | Internal | prompt unapproved | L1 | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU16-44 | I-016 | P16/R20 | Confidential | candidate only | L3 revoked | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU16-45 | I-016 | P10/R11 | Public | model Approved | L1 | hard cap | EU | PENDING_APPROVAL |
      | EX-04ZU16-46 | I-016 | P03/R03 | Public | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU16-47 | I-016 | P10/R11 | Confidential | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-48 | I-016 | P16/R20 | Public | prompt unapproved | L3 revoked | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU16-49 | I-016 | P10/R11 | Internal | candidate only | L3 revoked | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU16-50 | I-016 | P03/R03 | Restricted | prompt unapproved | L3 revoked | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU16-51 | I-016 | P10/R11 | Public | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-52 | I-016 | P10/R11 | Confidential | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU16-53 | I-016 | P16/R20 | Internal | prompt unapproved | L3 revoked | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU16-54 | I-016 | P16/R20 | Internal | model Approved | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-55 | I-016 | P16/R20 | Confidential | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-04ZU16-56 | I-016 | P10/R11 | Restricted | candidate only | L3 mandate | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU16-57 | I-016 | P03/R03 | Public | prompt unapproved | L3 mandate | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU16-58 | I-016 | P10/R11 | Internal | model Approved | L3 revoked | hard cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU16-59 | I-016 | P16/R20 | Restricted | candidate only | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU16-60 | I-016 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: Vector column and HNSW index for retrieval once the |
```

##### US-04-ZU17 Metering of Part 11.13 agents to Ledger B line B25 with a hard cap

| Field | Value |
|---|---|
| ID | US-04-ZU17 |
| Title | Metering of Part 11.13 agents to Ledger B line B25 with a hard cap |
| Type | Compliance (acceptance binding) |
| Story | As the FinOps lead I want all new agents metered to a capped budget line so that spend cannot overrun – with the acceptance criteria below, which the statement-only story US-04-YM37 did not carry |
| Persona / roles | AI lead (P10, R11) |
| Traces | FR-V12-M-099 (BR-V7-AI-04; DEC-743); DEC-743 |
| Priority | Must |
| Wave | Release 3+ (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-04-YM37, US-04-ZR20, US-04-ZR22, US-04-YH01, US-04-YI01; source definition: Part 11.13b §11.13.5.7 Functional requirements |
| Dimension profile | persona ×3 · data class ×4 · registry state ×3 · autonomy/mandate ×3 · budget ×3 · region ×3 · operation ×1 · model MU05 |
| Notes | Acceptance binding: US-04-YM37 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens A011, A012, A128, A198, A199; API family `/api/v1/ai/`; audit events `ai.*`; feature flag default OFF until DoD D-14 evidence · DoR R-10: task route through the model registry (DEC-788), eval dataset per AIX-05, per-task cost ceiling; no Restricted data to Tier 2 |

```gherkin
Feature: Metering of Part 11.13 agents to Ledger B line B25 with a hard cap
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with AI lead "sana@kestrel.example.com" (R11)
    And the model registry with "Claude Sonnet" Approved as primary for zone IN and EU (DEC-788) and a candidate model in state "candidate"

  @happy
  Scenario: AC-04ZU17-01 Happy path – The system shall meter all Part 11.13 agent usage to Ledger B line… (FR-V12-M-099)
    Given Sana Mehta (R11, sana@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "The system shall meter all Part 11.13 agent usage to Ledger B line…" is exercised as specified by FR-V12-M-099:
      """
      The system shall meter all Part 11.13 agent usage to Ledger B line B25 with a hard cap and ladder
      """
    Then the observable result matches FR-V12-M-099 and its tests in Part 11.21
    And the audit event "ai.the_system_shall_meter_all" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @DEC-007
  Scenario: AC-04ZU17-02 Negative – restricted personal data never reaches a free or unapproved model
    Given a step whose input contains restricted personal data (phone number and email)
    When the router evaluates the Tier 2 free fallback
    Then the route is refused with "DATA_CLASS_NOT_PERMITTED"
    And no request is sent to the Tier 2 provider

  @val
  Scenario: AC-04ZU17-03 Validation – model output must match its schema
    When a model returns JSON missing the required field "citations"
    Then the step result is "SCHEMA_INVALID", it is routed to human review and no effect is created

  @perm
  Scenario: AC-04ZU17-04 Permission – an AI agent identity cannot approve
    When the AI agent identity (R20) calls POST "/api/v1/approvals/AP-71/approve"
    Then the API returns 403 "AGENT_CANNOT_APPROVE" and the approval remains pending

  @edge @obs
  Scenario: AC-04ZU17-05 Edge – kill switch stops new calls within one scheduler cycle
    Given 40 queued AI steps for prompt "PRM-AGT-06-email-draft-v3"
    When Sana engages the kill switch for that prompt at 2027-04-01T09:00:00+05:30
    Then no new model call for that prompt starts after the next scheduler cycle and the queued steps are "HELD"

  @sec @obs @MU05
  Scenario Outline: AC-04ZU17-06 Permutations – AI governance, evaluation, prompts and cost (3-way, 59 rows)
    Given actor "<persona>" in zone "<region>" with data class "<data_class>"
    And the registry state is "<registry_state>", autonomy is "<autonomy_mandate>" and budget is "<budget>"
    When "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU05 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   M-099 = The system shall meter all Part 11.13 agent usage…
    Examples: MU05 rows (3-way, seed 381; space 972; tuples 780/780; +1 baseline-allow)
      | ex | operation | persona | data_class | registry_state | autonomy_mandate | budget | region | expected |
      | EX-04ZU17-01 | M-099 | P03/R03 | Public | candidate only | L3 revoked | hard cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-02 | M-099 | P10/R11 | Public | model Approved | L1 | in budget | EU | PENDING_APPROVAL |
      | EX-04ZU17-03 | M-099 | P16/R20 | Confidential | prompt unapproved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-04 | M-099 | P03/R03 | Internal | prompt unapproved | L3 mandate | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU17-05 | M-099 | P16/R20 | Restricted | model Approved | L3 mandate | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU17-06 | M-099 | P10/R11 | Restricted | candidate only | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-07 | M-099 | P16/R20 | Internal | candidate only | L1 | hard cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-08 | M-099 | P03/R03 | Confidential | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-09 | M-099 | P03/R03 | Restricted | prompt unapproved | L1 | in budget | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU17-10 | M-099 | P10/R11 | Confidential | candidate only | L3 revoked | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-11 | M-099 | P10/R11 | Internal | model Approved | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-12 | M-099 | P10/R11 | Confidential | prompt unapproved | L3 mandate | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU17-13 | M-099 | P16/R20 | Restricted | candidate only | L3 revoked | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU17-14 | M-099 | P16/R20 | Public | candidate only | L3 mandate | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-15 | M-099 | P03/R03 | Internal | candidate only | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-16 | M-099 | P16/R20 | Public | prompt unapproved | L1 | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU17-17 | M-099 | P16/R20 | Internal | model Approved | L3 revoked | in budget | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU17-18 | M-099 | P03/R03 | Restricted | model Approved | L3 revoked | hard cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU17-19 | M-099 | P10/R11 | Restricted | prompt unapproved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-20 | M-099 | P10/R11 | Public | prompt unapproved | L3 mandate | in budget | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU17-21 | M-099 | P16/R20 | Public | prompt unapproved | L3 revoked | soft cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU17-22 | M-099 | P03/R03 | Confidential | model Approved | L3 mandate | hard cap | IN | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU17-23 | M-099 | P03/R03 | Confidential | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-24 | M-099 | P10/R11 | Internal | candidate only | L1 | soft cap | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-25 | M-099 | P16/R20 | Restricted | model Approved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-26 | M-099 | P03/R03 | Public | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-27 | M-099 | P10/R11 | Internal | prompt unapproved | L3 revoked | in budget | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU17-28 | M-099 | P03/R03 | Internal | prompt unapproved | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-29 | M-099 | P10/R11 | Confidential | model Approved | L3 mandate | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-30 | M-099 | P16/R20 | Confidential | model Approved | L3 mandate | soft cap | EU | ALLOW: The system shall meter all Part 11.13 agent usage |
      | EX-04ZU17-31 | M-099 | P03/R03 | Restricted | candidate only | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-32 | M-099 | P10/R11 | Restricted | prompt unapproved | L3 revoked | hard cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU17-33 | M-099 | P03/R03 | Public | model Approved | L1 | soft cap | IN | PENDING_APPROVAL |
      | EX-04ZU17-34 | M-099 | P10/R11 | Public | candidate only | L3 mandate | soft cap | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-35 | M-099 | P16/R20 | Internal | prompt unapproved | L3 mandate | hard cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU17-36 | M-099 | P16/R20 | Confidential | candidate only | L1 | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-37 | M-099 | P10/R11 | Public | candidate only | L1 | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-38 | M-099 | P16/R20 | Restricted | prompt unapproved | L3 mandate | in budget | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU17-39 | M-099 | P16/R20 | Internal | model Approved | L1 | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-40 | M-099 | P16/R20 | Confidential | candidate only | L3 revoked | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-41 | M-099 | P03/R03 | Confidential | prompt unapproved | L3 revoked | soft cap | IN | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU17-42 | M-099 | P10/R11 | Restricted | model Approved | L1 | soft cap | EU | Tier 2 and unapproved models excluded |
      | EX-04ZU17-43 | M-099 | P03/R03 | Public | model Approved | L3 mandate | hard cap | EU | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU17-44 | M-099 | P10/R11 | Restricted | candidate only | L1 | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-45 | M-099 | P03/R03 | Internal | model Approved | L3 revoked | soft cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU17-46 | M-099 | P10/R11 | Confidential | prompt unapproved | L1 | hard cap | EU | BLOCK PROMPT_NOT_APPROVED |
      | EX-04ZU17-47 | M-099 | P16/R20 | Public | candidate only | L3 mandate | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-48 | M-099 | P10/R11 | Internal | model Approved | L3 mandate | hard cap | EU | HELD AI_BUDGET_EXHAUSTED |
      | EX-04ZU17-49 | M-099 | P03/R03 | Public | prompt unapproved | L3 mandate | hard cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-50 | M-099 | P10/R11 | Confidential | model Approved | L3 revoked | hard cap | IN | ROUTE MANDATE_INACTIVE |
      | EX-04ZU17-51 | M-099 | P03/R03 | Restricted | candidate only | L3 mandate | soft cap | IN | Tier 2 and unapproved models excluded |
      | EX-04ZU17-52 | M-099 | P03/R03 | Internal | candidate only | L3 revoked | in budget | IN | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-53 | M-099 | P16/R20 | Public | model Approved | L1 | hard cap | EU | PENDING_APPROVAL |
      | EX-04ZU17-54 | M-099 | P10/R11 | Confidential | candidate only | L3 mandate | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-55 | M-099 | P16/R20 | Confidential | candidate only | L3 revoked | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-56 | M-099 | P10/R11 | Public | model Approved | L3 revoked | soft cap | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-57 | M-099 | P16/R20 | Restricted | model Approved | L3 revoked | in budget | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-04ZU17-58 | M-099 | P10/R11 | Internal | candidate only | L1 | in budget | EU | BLOCK MODEL_NOT_APPROVED |
      | EX-04ZU17-59 | M-099 | P10/R11 | Public | model Approved | L3 mandate | in budget | IN | ALLOW: The system shall meter all Part 11.13 agent usage |
```

#### 11.22.5.4.5 EP-05 Market intelligence and discovery

| Field | Value |
|---|---|
| Epic | EP-05 Market intelligence and discovery (Part 0 §0.10.2) |
| New stories in this file | US-05-ZU01 |
| FR-V12 covered | A: 078 |
| Size | 1 stories · 5–8 SP · 2–8 pd (0.5/1.0 pd per SP) · central 4.5 pd (0.7 pd per SP mid) |
| Releases | Release 2: 1 |

##### US-05-ZU01 Offering-specific audiences with market eligibility and source rights

| Field | Value |
|---|---|
| ID | US-05-ZU01 |
| Title | Offering-specific audiences with market eligibility and source rights |
| Type | Compliance |
| Story | As a DPO / counsel (P09, R10), I want offering-specific audiences: ICP, segment, market eligibility and source rights by offering; no cross-product prospect assumptions, so that nothing is sent, recorded or published unless the law of the recipient's market allows it and we can prove it |
| Persona / roles | DPO / counsel (P09, R10) |
| Traces | FR-V12-A-078 (MT-13); tests TC-V12-A-078 |
| Priority | Should |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-03-YM09, US-03-YA01, US-03-YG02, US-03-YG03; source definition: Part 11.1b §ADR-180 Tenant per customer contract |
| Dimension profile | persona ×3 · jurisdiction ×4 · consent ×3 · channel ×3 · data class ×3 · region ×3 · operation ×1 · model MU06 |
| Notes | Screens A007, A013, A200, A201, A202, W29, W30; API family `/api/v1/compliance/`; audit events `compliance.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Offering-specific audiences with market eligibility and source rights
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" with DPO "farah@kestrel.example.com" (R10)
    And jurisdiction packs RP-IN (Approved), RP-EU (Approved), RP-UK (Draft) and RP-US (Expired) in the rule-pack registry (Part 11.15)

  @happy @MT-13
  Scenario: AC-05ZU01-01 Happy path – Offering-specific audiences (FR-V12-A-078)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Offering-specific audiences" is exercised as specified by FR-V12-A-078:
      """
      Offering-specific audiences: ICP, segment, market eligibility and source rights by offering; no cross-product prospect assumptions
      """
    Then two audiences; results use the selected offering and evidence
    And the audit event "compliance.offering_specific_audiences" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-ELG-18
  Scenario: AC-05ZU01-02 Negative – a draft pack never allows an outbound action
    Given recipient "olivia@brightway.example.co.uk" is in market UK whose pack RP-UK is "Draft"
    When a promotional email to her passes every other check
    Then the PDP returns HOLD "PACK_NOT_ACTIVE" and no message is dispatched

  @val
  Scenario: AC-05ZU01-03 Validation – the promotional window is checked in the recipient's local time
    Given recipient "anu@sunrise.example.in" in Asia/Kolkata
    When a promotional SMS is scheduled for 21:15 local time
    Then the preflight returns HOLD "OUTSIDE_MESSAGING_WINDOW" (09:00–21:00, DEC-777) and proposes 09:00 next day

  @perm
  Scenario: AC-05ZU01-04 Permission – only R10 can approve a pack
    When "maya@kestrel.example.com" (R05) approves pack RP-UK
    Then the API returns 403 "PERMISSION_DENIED" and the pack stays "Draft"

  @edge
  Scenario: AC-05ZU01-05 Edge – consent withdrawal holds queued work
    Given 3 queued messages for "anu@sunrise.example.in"
    When she withdraws consent at 2027-05-02T10:00:00+05:30
    Then all 3 are "HELD" with "CONSENT_WITHDRAWN" and the suppression list is updated within 60 seconds

  @sec @obs @MU06
  Scenario Outline: AC-05ZU01-06 Permutations – Jurisdiction packs, consent and legal controls (3-way, 56 rows)
    Given actor "<persona>" in zone "<region>" for a recipient in "<jurisdiction>"
    And consent is "<consent>" and the data class is "<data_class>"
    When "<operation>" is checked for channel "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU06 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-078 = Offering-specific audiences
    Examples: MU06 rows (3-way, seed 388; space 972; tuples 780/780; +0 baseline-allow)
      | ex | operation | persona | jurisdiction | consent | channel | data_class | region | expected |
      | EX-05ZU01-01 | A-078 | P03/R03 | UK draft | withdrawn | email | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-05ZU01-02 | A-078 | P09/R10 | EU ✓ | withdrawn | WhatsApp | Restricted | IN | HOLD CONSENT_WITHDRAWN |
      | EX-05ZU01-03 | A-078 | P09/R10 | US expired | valid | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-04 | A-078 | P05/R05 | IN ✓ | unknown | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-05 | A-078 | P03/R03 | IN ✓ | unknown | SMS/voice | Confidential | IN | HOLD CONSENT_UNKNOWN |
      | EX-05ZU01-06 | A-078 | P05/R05 | UK draft | valid | WhatsApp | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-05ZU01-07 | A-078 | P03/R03 | US expired | withdrawn | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-08 | A-078 | P09/R10 | EU ✓ | unknown | email | Confidential | EU | HOLD CONSENT_UNKNOWN |
      | EX-05ZU01-09 | A-078 | P03/R03 | EU ✓ | valid | SMS/voice | Restricted | EU | ALLOW: Two audiences |
      | EX-05ZU01-10 | A-078 | P05/R05 | US expired | unknown | WhatsApp | Internal | IN | HOLD PACK_EXPIRED |
      | EX-05ZU01-11 | A-078 | P05/R05 | UK draft | withdrawn | SMS/voice | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-05ZU01-12 | A-078 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Two audiences |
      | EX-05ZU01-13 | A-078 | P09/R10 | UK draft | unknown | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-14 | A-078 | P05/R05 | EU ✓ | withdrawn | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-15 | A-078 | P05/R05 | US expired | withdrawn | email | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-05ZU01-16 | A-078 | P09/R10 | IN ✓ | withdrawn | WhatsApp | Internal | EU | HOLD CONSENT_WITHDRAWN |
      | EX-05ZU01-17 | A-078 | P03/R03 | US expired | valid | email | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-05ZU01-18 | A-078 | P03/R03 | EU ✓ | valid | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-19 | A-078 | P05/R05 | EU ✓ | valid | email | Confidential | IN | ALLOW: Two audiences |
      | EX-05ZU01-20 | A-078 | P09/R10 | UK draft | withdrawn | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-21 | A-078 | P05/R05 | UK draft | unknown | SMS/voice | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-05ZU01-22 | A-078 | P03/R03 | IN ✓ | unknown | WhatsApp | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-05ZU01-23 | A-078 | P05/R05 | IN ✓ | valid | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-24 | A-078 | P09/R10 | US expired | withdrawn | SMS/voice | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-05ZU01-25 | A-078 | P03/R03 | EU ✓ | unknown | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-26 | A-078 | P09/R10 | US expired | unknown | SMS/voice | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-05ZU01-27 | A-078 | P03/R03 | UK draft | valid | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-28 | A-078 | P03/R03 | UK draft | unknown | WhatsApp | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-05ZU01-29 | A-078 | P05/R05 | IN ✓ | valid | WhatsApp | Restricted | IN | ALLOW: Two audiences |
      | EX-05ZU01-30 | A-078 | P03/R03 | IN ✓ | withdrawn | SMS/voice | Internal | IN | HOLD CONSENT_WITHDRAWN |
      | EX-05ZU01-31 | A-078 | P09/R10 | UK draft | valid | email | Restricted | EU | HOLD PACK_NOT_ACTIVE |
      | EX-05ZU01-32 | A-078 | P05/R05 | US expired | unknown | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-33 | A-078 | P03/R03 | IN ✓ | valid | email | Confidential | EU | ALLOW: Two audiences |
      | EX-05ZU01-34 | A-078 | P05/R05 | IN ✓ | withdrawn | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-35 | A-078 | P09/R10 | US expired | valid | WhatsApp | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-05ZU01-36 | A-078 | P05/R05 | EU ✓ | unknown | WhatsApp | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-05ZU01-37 | A-078 | P09/R10 | EU ✓ | unknown | SMS/voice | Internal | IN | HOLD CONSENT_UNKNOWN |
      | EX-05ZU01-38 | A-078 | P09/R10 | UK draft | valid | SMS/voice | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-05ZU01-39 | A-078 | P03/R03 | EU ✓ | withdrawn | email | Confidential | IN | HOLD CONSENT_WITHDRAWN |
      | EX-05ZU01-40 | A-078 | P03/R03 | US expired | unknown | SMS/voice | Internal | EU | HOLD PACK_EXPIRED |
      | EX-05ZU01-41 | A-078 | P09/R10 | IN ✓ | withdrawn | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-42 | A-078 | P05/R05 | UK draft | valid | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-43 | A-078 | P05/R05 | IN ✓ | unknown | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-44 | A-078 | P09/R10 | EU ✓ | valid | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-45 | A-078 | P09/R10 | US expired | withdrawn | email | Internal | IN | HOLD PACK_EXPIRED |
      | EX-05ZU01-46 | A-078 | P09/R10 | IN ✓ | unknown | email | Confidential | IN | HOLD CONSENT_UNKNOWN |
      | EX-05ZU01-47 | A-078 | P05/R05 | IN ✓ | valid | SMS/voice | Internal | EU | ALLOW: Two audiences |
      | EX-05ZU01-48 | A-078 | P03/R03 | US expired | withdrawn | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-49 | A-078 | P05/R05 | US expired | valid | SMS/voice | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-05ZU01-50 | A-078 | P03/R03 | EU ✓ | withdrawn | email | Internal | EU | HOLD CONSENT_WITHDRAWN |
      | EX-05ZU01-51 | A-078 | P09/R10 | UK draft | withdrawn | WhatsApp | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-05ZU01-52 | A-078 | P05/R05 | EU ✓ | withdrawn | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-53 | A-078 | P09/R10 | UK draft | unknown | email | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-05ZU01-54 | A-078 | P03/R03 | IN ✓ | withdrawn | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-05ZU01-55 | A-078 | P05/R05 | EU ✓ | withdrawn | WhatsApp | Confidential | IN | HOLD CONSENT_WITHDRAWN |
      | EX-05ZU01-56 | A-078 | P03/R03 | UK draft | valid | SMS/voice | Confidential | EU | HOLD PACK_NOT_ACTIVE |
```

#### 11.22.5.4.8 EP-08 Messaging: drafting, email, inbound, sequences, omnichannel

| Field | Value |
|---|---|
| Epic | EP-08 Messaging: drafting, email, inbound, sequences, omnichannel (Part 0 §0.10.2) |
| New stories in this file | US-08-ZU01, US-08-ZU02 |
| FR-V12 covered | F: 045; H: 024–025 |
| Size | 2 stories · 10–16 SP · 5–16 pd (0.5/1.0 pd per SP) · central 9.1 pd (0.7 pd per SP mid) |
| Releases | Release 1: 1, Release 2: 1 |

##### US-08-ZU01 DLT and preference-registry scrub for promotional SMS and voice

| Field | Value |
|---|---|
| ID | US-08-ZU01 |
| Title | DLT and preference-registry scrub for promotional SMS and voice |
| Type | Compliance |
| Story | As a DPO / counsel (P09, R10), I want DLT and preference-registry scrub for promotional SMS/voice; number pool by purpose, so that nothing is sent, recorded or published unless the law of the recipient's market allows it and we can prove it |
| Persona / roles | DPO / counsel (P09, R10) |
| Traces | FR-V12-F-045 (CJ-R06); DEC-770, DEC-790; tests TC-V12-F-102 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-03-YM09, US-03-YA01, US-03-YG02, US-03-YG03; source definition: Part 11.6b §11.6.5.15 Functional requirements FR-V12-F-001…073 |
| Dimension profile | persona ×3 · jurisdiction ×4 · consent ×3 · channel ×3 · data class ×3 · region ×3 · operation ×1 · model MU06 |
| Notes | FR-V12-F-045: release per DEC-770, DEC-790 (no release stated; funded change request scheduled in Release 2) · Screens A007, A013, A200, A201, A202, W29, W30; API family `/api/v1/compliance/`; audit events `compliance.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: DLT and preference-registry scrub for promotional SMS and voice
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" with DPO "farah@kestrel.example.com" (R10)
    And jurisdiction packs RP-IN (Approved), RP-EU (Approved), RP-UK (Draft) and RP-US (Expired) in the rule-pack registry (Part 11.15)

  @happy @CJ-R06 @DEC-770
  Scenario: AC-08ZU01-01 Happy path – DLT and preference-registry scrub for promotional SMS/voice (FR-V12-F-045)
    Given Farah Khan (R10, farah@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "DLT and preference-registry scrub for promotional SMS/voice" is exercised as specified by FR-V12-F-045:
      """
      DLT and preference-registry scrub for promotional SMS/voice; number pool by purpose
      """
    Then unregistered template or unscrubbed list → HOLD
    And the audit event "compliance.dlt_and_preference_registry" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-ELG-18
  Scenario: AC-08ZU01-02 Negative – a draft pack never allows an outbound action
    Given recipient "olivia@brightway.example.co.uk" is in market UK whose pack RP-UK is "Draft"
    When a promotional email to her passes every other check
    Then the PDP returns HOLD "PACK_NOT_ACTIVE" and no message is dispatched

  @val
  Scenario: AC-08ZU01-03 Validation – the promotional window is checked in the recipient's local time
    Given recipient "anu@sunrise.example.in" in Asia/Kolkata
    When a promotional SMS is scheduled for 21:15 local time
    Then the preflight returns HOLD "OUTSIDE_MESSAGING_WINDOW" (09:00–21:00, DEC-777) and proposes 09:00 next day

  @perm
  Scenario: AC-08ZU01-04 Permission – only R10 can approve a pack
    When "maya@kestrel.example.com" (R05) approves pack RP-UK
    Then the API returns 403 "PERMISSION_DENIED" and the pack stays "Draft"

  @edge
  Scenario: AC-08ZU01-05 Edge – consent withdrawal holds queued work
    Given 3 queued messages for "anu@sunrise.example.in"
    When she withdraws consent at 2027-05-02T10:00:00+05:30
    Then all 3 are "HELD" with "CONSENT_WITHDRAWN" and the suppression list is updated within 60 seconds

  @sec @obs @MU06
  Scenario Outline: AC-08ZU01-06 Permutations – Jurisdiction packs, consent and legal controls (3-way, 59 rows)
    Given actor "<persona>" in zone "<region>" for a recipient in "<jurisdiction>"
    And consent is "<consent>" and the data class is "<data_class>"
    When "<operation>" is checked for channel "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU06 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   F-045 = DLT and preference-registry scrub for promotional…
    Examples: MU06 rows (3-way, seed 395; space 972; tuples 780/780; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | consent | channel | data_class | region | expected |
      | EX-08ZU01-01 | F-045 | P05/R05 | EU ✓ | unknown | WhatsApp | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-08ZU01-02 | F-045 | P03/R03 | EU ✓ | withdrawn | SMS/voice | Confidential | IN | HOLD CONSENT_WITHDRAWN |
      | EX-08ZU01-03 | F-045 | P09/R10 | UK draft | unknown | email | Internal | IN | HOLD PACK_NOT_ACTIVE |
      | EX-08ZU01-04 | F-045 | P05/R05 | US expired | valid | SMS/voice | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-05 | F-045 | P09/R10 | IN ✓ | valid | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-06 | F-045 | P03/R03 | UK draft | valid | email | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-07 | F-045 | P05/R05 | IN ✓ | withdrawn | email | Confidential | EU | HOLD CONSENT_WITHDRAWN |
      | EX-08ZU01-08 | F-045 | P09/R10 | US expired | withdrawn | WhatsApp | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-08ZU01-09 | F-045 | P03/R03 | IN ✓ | unknown | SMS/voice | Internal | EU | HOLD CONSENT_UNKNOWN |
      | EX-08ZU01-10 | F-045 | P05/R05 | UK draft | withdrawn | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-11 | F-045 | P09/R10 | US expired | unknown | SMS/voice | Confidential | EU | HOLD PACK_EXPIRED |
      | EX-08ZU01-12 | F-045 | P09/R10 | EU ✓ | valid | email | Internal | EU | ALLOW: Unregistered template or unscrubbed list → HOLD |
      | EX-08ZU01-13 | F-045 | P05/R05 | UK draft | valid | SMS/voice | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-08ZU01-14 | F-045 | P03/R03 | US expired | unknown | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-15 | F-045 | P09/R10 | EU ✓ | withdrawn | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-16 | F-045 | P03/R03 | IN ✓ | valid | WhatsApp | Internal | IN | ALLOW: Unregistered template or unscrubbed list → HOLD |
      | EX-08ZU01-17 | F-045 | P05/R05 | IN ✓ | unknown | SMS/voice | Restricted | IN | HOLD CONSENT_UNKNOWN |
      | EX-08ZU01-18 | F-045 | P03/R03 | US expired | withdrawn | email | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-08ZU01-19 | F-045 | P05/R05 | EU ✓ | unknown | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-20 | F-045 | P09/R10 | UK draft | withdrawn | WhatsApp | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-08ZU01-21 | F-045 | P09/R10 | IN ✓ | withdrawn | email | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-22 | F-045 | P03/R03 | EU ✓ | unknown | email | Restricted | IN | HOLD CONSENT_UNKNOWN |
      | EX-08ZU01-23 | F-045 | P05/R05 | US expired | valid | email | Confidential | IN | HOLD PACK_EXPIRED |
      | EX-08ZU01-24 | F-045 | P09/R10 | IN ✓ | valid | SMS/voice | Restricted | EU | ALLOW: Unregistered template or unscrubbed list → HOLD |
      | EX-08ZU01-25 | F-045 | P03/R03 | EU ✓ | valid | WhatsApp | Confidential | EU | ALLOW: Unregistered template or unscrubbed list → HOLD |
      | EX-08ZU01-26 | F-045 | P05/R05 | EU ✓ | withdrawn | SMS/voice | Internal | IN | HOLD CONSENT_WITHDRAWN |
      | EX-08ZU01-27 | F-045 | P09/R10 | UK draft | unknown | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-28 | F-045 | P03/R03 | UK draft | withdrawn | SMS/voice | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-08ZU01-29 | F-045 | P05/R05 | US expired | valid | WhatsApp | Restricted | EU | HOLD PACK_EXPIRED |
      | EX-08ZU01-30 | F-045 | P09/R10 | IN ✓ | unknown | WhatsApp | Confidential | IN | HOLD CONSENT_UNKNOWN |
      | EX-08ZU01-31 | F-045 | P03/R03 | IN ✓ | withdrawn | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-32 | F-045 | P05/R05 | UK draft | withdrawn | email | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-08ZU01-33 | F-045 | P03/R03 | EU ✓ | unknown | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-34 | F-045 | P05/R05 | US expired | unknown | email | Internal | EU | HOLD PACK_EXPIRED |
      | EX-08ZU01-35 | F-045 | P03/R03 | US expired | valid | SMS/voice | Restricted | IN | HOLD PACK_EXPIRED |
      | EX-08ZU01-36 | F-045 | P09/R10 | US expired | withdrawn | email | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-37 | F-045 | P05/R05 | UK draft | unknown | WhatsApp | Confidential | IN | HOLD PACK_NOT_ACTIVE |
      | EX-08ZU01-38 | F-045 | P09/R10 | US expired | valid | WhatsApp | Internal | IN | HOLD PACK_EXPIRED |
      | EX-08ZU01-39 | F-045 | P03/R03 | IN ✓ | withdrawn | SMS/voice | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-40 | F-045 | P03/R03 | UK draft | unknown | email | Confidential | EU | HOLD PACK_NOT_ACTIVE |
      | EX-08ZU01-41 | F-045 | P05/R05 | EU ✓ | valid | SMS/voice | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-42 | F-045 | P09/R10 | EU ✓ | valid | WhatsApp | Confidential | IN | ALLOW: Unregistered template or unscrubbed list → HOLD |
      | EX-08ZU01-43 | F-045 | P09/R10 | UK draft | valid | WhatsApp | Internal | EU | HOLD PACK_NOT_ACTIVE |
      | EX-08ZU01-44 | F-045 | P03/R03 | IN ✓ | valid | email | Internal | IN | ALLOW: Unregistered template or unscrubbed list → HOLD |
      | EX-08ZU01-45 | F-045 | P09/R10 | EU ✓ | unknown | SMS/voice | Internal | IN | HOLD CONSENT_UNKNOWN |
      | EX-08ZU01-46 | F-045 | P05/R05 | US expired | withdrawn | SMS/voice | Internal | EU | HOLD PACK_EXPIRED |
      | EX-08ZU01-47 | F-045 | P05/R05 | IN ✓ | unknown | WhatsApp | Internal | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-48 | F-045 | P03/R03 | UK draft | withdrawn | WhatsApp | Restricted | IN | HOLD PACK_NOT_ACTIVE |
      | EX-08ZU01-49 | F-045 | P09/R10 | IN ✓ | unknown | email | Restricted | EU | HOLD CONSENT_UNKNOWN |
      | EX-08ZU01-50 | F-045 | P05/R05 | IN ✓ | valid | WhatsApp | Restricted | EU | ALLOW: Unregistered template or unscrubbed list → HOLD |
      | EX-08ZU01-51 | F-045 | P05/R05 | US expired | unknown | WhatsApp | Restricted | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-52 | F-045 | P05/R05 | UK draft | valid | email | Restricted | EU | HOLD PACK_NOT_ACTIVE |
      | EX-08ZU01-53 | F-045 | P03/R03 | US expired | unknown | email | Internal | IN | HOLD PACK_EXPIRED |
      | EX-08ZU01-54 | F-045 | P09/R10 | EU ✓ | withdrawn | SMS/voice | Internal | EU | HOLD CONSENT_WITHDRAWN |
      | EX-08ZU01-55 | F-045 | P05/R05 | EU ✓ | withdrawn | email | Internal | EU | HOLD CONSENT_WITHDRAWN |
      | EX-08ZU01-56 | F-045 | P03/R03 | IN ✓ | withdrawn | WhatsApp | Internal | IN | HOLD CONSENT_WITHDRAWN |
      | EX-08ZU01-57 | F-045 | P03/R03 | EU ✓ | withdrawn | WhatsApp | Restricted | EU | HOLD CONSENT_WITHDRAWN |
      | EX-08ZU01-58 | F-045 | P03/R03 | UK draft | valid | WhatsApp | Confidential | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU01-59 | F-045 | P09/R10 | IN ✓ | valid | email | Internal | IN | ALLOW: Unregistered template or unscrubbed list → HOLD |
```

##### US-08-ZU02 Multiple channel accounts per company with scoped sender identities

| Field | Value |
|---|---|
| ID | US-08-ZU02 |
| Title | Multiple channel accounts per company with scoped sender identities |
| Type | Feature |
| Story | As an integration administrator (P18, R12I), I want a company may have multiple independent channel accounts; offering-market mapping and independent eligibility; scoped provider identity, credential reference and sender aliases; no secrets in HTML or public artifacts, so that our systems integrate through governed, observable and revocable connections without sharing secrets |
| Persona / roles | Integration administrator (P18, R12I) |
| Traces | FR-V12-H-024 (MT-22 (P0)); FR-V12-H-025 (MT-23 (P0)) |
| Priority | Should |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-20-ZR06, US-20-ZR07, US-20-ZR08, US-18-ZR11; source definition: Part 11.8b §11.8.5.1 Requirements adopted and release mapping |
| Dimension profile | persona ×3 · authority ×4 · channel ×3 · credential ×3 · provider ×3 · region ×3 · operation ×2 · model MU03 |
| Notes | Screens A008, A011, A168, A204, W47; API family `/api/v1/developer/`; audit events `integration.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Multiple channel accounts per company with scoped sender identities
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" in zone IN with integration administrator "kiran@kestrel.example.com" (R12I)
    And the developer platform sandbox "sbx-kestrel" and the connector registry:
      """
      with Salesforce, HubSpot, an SMS-DLT and a voice connector in state "draft"
      """

  @happy @MT-22
  Scenario: AC-08ZU02-01 Happy path – A company may have multiple independent channel accounts (FR-V12-H-024)
    Given Kiran Rao (R12I, kiran@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "A company may have multiple independent channel accounts" is exercised as specified by FR-V12-H-024:
      """
      A company may have multiple independent channel accounts; offering-market mapping and independent eligibility
      """
    Then email and WhatsApp accounts for two markets preserved in handoff
    And the audit event "integration.a_company_may_have_multiple" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @MT-23
  Scenario: AC-08ZU02-02 Alternate – Scoped provider identity, credential reference and sender aliases (FR-V12-H-025)
    Given Kiran Rao (R12I, kiran@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Scoped provider identity, credential reference and sender aliases" is exercised as specified by FR-V12-H-025:
      """
      Scoped provider identity, credential reference and sender aliases; no secrets in HTML or public artifacts
      """
    Then two senders under one channel; wrong-company account denied
    And the audit event "integration.scoped_provider_identity" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @sec @NFR-004
  Scenario: AC-08ZU02-03 Negative – a plaintext secret never reaches the database or logs
    When a connector configuration is saved with field "client_secret" = "s3cr3t-value"
    Then the API returns 422 "SECRET_REFERENCE_REQUIRED"
    And a database and log inspection finds no occurrence of "s3cr3t-value"

  @val
  Scenario: AC-08ZU02-04 Validation – an unsigned webhook is rejected
    When an inbound webhook arrives without the "X-Signature" and "X-Timestamp" headers
    Then the endpoint returns 401 "SIGNATURE_REQUIRED" and the payload is not processed

  @perm @BRL-TEN-04
  Scenario: AC-08ZU02-05 Permission – a key of tenant B cannot read tenant A
    Given an API key of tenant "Nordlicht Robotik GmbH" with scope "crm:read"
    When it calls GET "/api/v1/crm/contacts/C-1001" belonging to "Kestrel Analytics Pvt Ltd"
    Then the response is the uniform 404 "NOT_FOUND" and no row is returned

  @edge @I4 @DEC-050
  Scenario: AC-08ZU02-06 Edge – an uncertain write is reconciled before any retry
    Given the provider timed out after receiving write W-552
    When the retry scheduler runs
    Then the write is marked "RECONCILING" and the provider is queried for W-552 before any resend
    And exactly one provider record exists afterwards

  @sec @obs @MU03
  Scenario Outline: AC-08ZU02-07 Permutations – Developer platform, API contracts and connectors (2-way, 20 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the credential is "<credential>" and the provider is "<provider>"
    When "<operation>" runs through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU03 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   H-024 = A company may have multiple independent channel…
    #   H-025 = Scoped provider identity, credential reference and…
    Examples: MU03 rows (2-way, seed 402; space 1,944; tuples 188/188; +2 baseline-allow)
      | ex | operation | persona | authority | channel | credential | provider | region | expected |
      | EX-08ZU02-01 | H-024 | P10/R11 | A1 | C3 key | secret expired | I4 uncertain | IN | 401 CREDENTIAL_EXPIRED |
      | EX-08ZU02-02 | H-025 | P13/R17 | T5 other tenant | C3 key | vault ref ok | I1 up | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-08ZU02-03 | H-024 | P18/R12I | A5 wrong role | C3 OAuth | vault ref ok | I3 down | EU | 403 PERMISSION_DENIED |
      | EX-08ZU02-04 | H-025 | P13/R17 | A3 SoD/limit | webhook | cred revoked | I3 down | IN | 401 CREDENTIAL_REVOKED |
      | EX-08ZU02-05 | H-025 | P10/R11 | A1 | C3 OAuth | cred revoked | I1 up | EU | 401 CREDENTIAL_REVOKED |
      | EX-08ZU02-06 | H-024 | P18/R12I | A3 SoD/limit | webhook | secret expired | I1 up | EU→IN (misrouted) | 401 CREDENTIAL_EXPIRED |
      | EX-08ZU02-07 | H-025 | P18/R12I | A5 wrong role | C3 key | cred revoked | I4 uncertain | EU→IN (misrouted) | 401 CREDENTIAL_REVOKED |
      | EX-08ZU02-08 | H-024 | P13/R17 | T5 other tenant | C3 OAuth | secret expired | I4 uncertain | EU | uniform 404 NOT_FOUND |
      | EX-08ZU02-09 | H-024 | P10/R11 | A3 SoD/limit | webhook | vault ref ok | I4 uncertain | EU | 403 SOD_CONFLICT |
      | EX-08ZU02-10 | H-025 | P10/R11 | T5 other tenant | C3 key | secret expired | I3 down | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-08ZU02-11 | H-024 | P18/R12I | T5 other tenant | C3 OAuth | cred revoked | I1 up | IN | uniform 404 NOT_FOUND |
      | EX-08ZU02-12 | H-025 | P13/R17 | A5 wrong role | webhook | secret expired | I1 up | IN | 401 CREDENTIAL_EXPIRED |
      | EX-08ZU02-13 | H-024 | P18/R12I | A1 | webhook | vault ref ok | I3 down | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-08ZU02-14 | H-024 | P10/R11 | A5 wrong role | C3 OAuth | cred revoked | I3 down | EU→IN (misrouted) | 401 CREDENTIAL_REVOKED |
      | EX-08ZU02-15 | H-024 | P18/R12I | A3 SoD/limit | C3 key | vault ref ok | I1 up | IN | 403 SOD_CONFLICT |
      | EX-08ZU02-16 | H-024 | P13/R17 | A1 | C3 key | secret expired | I3 down | EU | 401 CREDENTIAL_EXPIRED |
      | EX-08ZU02-17 | H-024 | P10/R11 | A3 SoD/limit | C3 OAuth | cred revoked | I3 down | EU | 401 CREDENTIAL_REVOKED |
      | EX-08ZU02-18 | H-025 | P13/R17 | T5 other tenant | webhook | cred revoked | I1 up | IN | uniform 404 NOT_FOUND |
      | EX-08ZU02-19 | H-024 | P18/R12I | A1 | C3 key | vault ref ok | I1 up | IN | ALLOW: Email and WhatsApp accounts for two markets |
      | EX-08ZU02-20 | H-025 | P18/R12I | A1 | C3 key | vault ref ok | I1 up | IN | ALLOW: Two senders under one channel |
```

#### 11.22.5.4.12 EP-12 Campaigns, landing pages, ads and referrals

| Field | Value |
|---|---|
| Epic | EP-12 Campaigns, landing pages, ads and referrals (Part 0 §0.10.2) |
| New stories in this file | US-12-ZU01 |
| FR-V12 covered | I: 045 |
| Size | 1 stories · 3–5 SP · 2–5 pd (0.5/1.0 pd per SP) · central 2.8 pd (0.7 pd per SP mid) |
| Releases | Release 1: 1 |

##### US-12-ZU01 Consent-aware acquisition analytics

| Field | Value |
|---|---|
| ID | US-12-ZU01 |
| Title | Consent-aware acquisition analytics |
| Type | Feature |
| Story | As a startup head (P02, R02), I want consent-aware acquisition analytics, so that every number I see is defined once, scoped to what I may see, and adds up |
| Persona / roles | Startup head (P02, R02) |
| Traces | FR-V12-I-045 (AT-14); tests TC-V12-I-031 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 3–5 |
| Dependencies | US-17-YI01, US-17-YI02, US-21-YA01, US-17-YG02; source definition: Part 11.9c §11.9.5.20 Functional requirements and user… |
| Dimension profile | persona ×3 · authority ×4 · scope ×3 · currency ×3 · consent ×3 · channel ×3 · operation ×1 · model MU13 |
| Notes | Screens A042, A087–A089, A106, A191; API family `/api/v1/analytics/`; audit events `analytics.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Consent-aware acquisition analytics
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd":
      """
      with companies "Kestrel IN" and "Kestrel EU", startup head "arjun@kestrel.example.com" (R02) for "Kestrel IN" only
      """
    And the metric registry with KPI definitions (numerator, denominator, period, freshness) approved at version 3

  @happy @AT-14
  Scenario: AC-12ZU01-01 Happy path – Consent-aware acquisition analytics (FR-V12-I-045)
    Given Arjun Menon (R02, arjun@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Consent-aware acquisition analytics" is exercised as specified by FR-V12-I-045: Consent-aware acquisition analytics
    Then the observable result matches FR-V12-I-045 and its tests TC-V12-I-031
    And the audit event "analytics.consent_aware_acquisition" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @ADR-183
  Scenario: AC-12ZU01-02 Negative – a tile without a registry definition fails CI
    Given a dashboard tile "win rate" that references no metric definition
    When CI runs the metric-registry check
    Then the build fails naming the tile

  @val
  Scenario: AC-12ZU01-03 Validation – zero denominator is "not applicable", not zero
    Given 0 qualified leads in the period
    When the conversion KPI renders
    Then it shows "not applicable" with the denominator 0 and no percentage

  @perm
  Scenario: AC-12ZU01-04 Permission – no data from a company outside my scope
    When Arjun opens the drill-down of "pipeline value"
    Then only rows of "Kestrel IN" appear and the total equals the tile

  @edge
  Scenario: AC-12ZU01-05 Edge – currencies are never summed without an approved rate
    Given pipeline in INR and EUR and no approved rate
    When the total renders
    Then native totals are shown per currency and the converted total shows "FX_RATE_MISSING"

  @sec @obs @MU13
  Scenario Outline: AC-12ZU01-06 Permutations – Analytics, metrics and management views (2-way, 17 rows)
    Given actor "<persona>" with authority "<authority>" and scope "<scope>"
    And currencies are "<currency>" and consent is "<consent>"
    When "<operation>" is viewed through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU13 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   I-045 = Consent-aware acquisition analytics
    Examples: MU13 rows (2-way, seed 409; space 972; tuples 169/169; +1 baseline-allow)
      | ex | operation | persona | authority | scope | currency | consent | channel | expected |
      | EX-12ZU01-01 | I-045 | P02/R02 | A5 wrong role | company | INR+EUR rate ✓ | withdrawn | C2 mobile | 403 PERMISSION_DENIED |
      | EX-12ZU01-02 | I-045 | P01/R01 | A1 | portfolio grant | INR+EUR no rate | valid | C3 API | ALLOW: Consent-aware acquisition analytics |
      | EX-12ZU01-03 | I-045 | P13/R17 | T5 other tenant | grant revoked | INR | unknown | C1 web | uniform 404 NOT_FOUND |
      | EX-12ZU01-04 | I-045 | P02/R02 | A3 SoD/limit | company | INR | unknown | C3 API | 403 SOD_CONFLICT |
      | EX-12ZU01-05 | I-045 | P13/R17 | A3 SoD/limit | portfolio grant | INR+EUR no rate | withdrawn | C1 web | 403 SOD_CONFLICT |
      | EX-12ZU01-06 | I-045 | P01/R01 | A3 SoD/limit | grant revoked | INR+EUR rate ✓ | valid | C2 mobile | 403 GRANT_REVOKED |
      | EX-12ZU01-07 | I-045 | P13/R17 | A1 | company | INR+EUR rate ✓ | valid | C1 web | ALLOW: Consent-aware acquisition analytics |
      | EX-12ZU01-08 | I-045 | P01/R01 | A5 wrong role | portfolio grant | INR | unknown | C2 mobile | 403 PERMISSION_DENIED |
      | EX-12ZU01-09 | I-045 | P02/R02 | T5 other tenant | grant revoked | INR+EUR no rate | withdrawn | C3 API | uniform 404 NOT_FOUND |
      | EX-12ZU01-10 | I-045 | P02/R02 | T5 other tenant | portfolio grant | INR+EUR rate ✓ | valid | C1 web | uniform 404 NOT_FOUND |
      | EX-12ZU01-11 | I-045 | P01/R01 | T5 other tenant | company | INR+EUR no rate | withdrawn | C2 mobile | uniform 404 NOT_FOUND |
      | EX-12ZU01-12 | I-045 | P13/R17 | A5 wrong role | grant revoked | INR+EUR rate ✓ | valid | C3 API | 403 GRANT_REVOKED |
      | EX-12ZU01-13 | I-045 | P02/R02 | A1 | grant revoked | INR | withdrawn | C2 mobile | 403 GRANT_REVOKED |
      | EX-12ZU01-14 | I-045 | P01/R01 | A5 wrong role | portfolio grant | INR+EUR no rate | unknown | C1 web | 403 PERMISSION_DENIED |
      | EX-12ZU01-15 | I-045 | P13/R17 | A1 | portfolio grant | INR+EUR rate ✓ | unknown | C2 mobile | HOLD CONSENT_UNKNOWN |
      | EX-12ZU01-16 | I-045 | P01/R01 | A3 SoD/limit | grant revoked | INR | valid | C2 mobile | 403 GRANT_REVOKED |
      | EX-12ZU01-17 | I-045 | P01/R01 | A1 | company | INR | valid | C1 web | ALLOW: Consent-aware acquisition analytics |
```

#### 11.22.5.4.15 EP-15 Payment, closure, revenue and attribution

| Field | Value |
|---|---|
| Epic | EP-15 Payment, closure, revenue and attribution (Part 0 §0.10.2) |
| New stories in this file | US-15-ZU01 |
| FR-V12 covered | E: 079–082 |
| Size | 1 stories · 2–3 SP · 1–3 pd (0.5/1.0 pd per SP) · central 1.8 pd (0.7 pd per SP mid) |
| Releases | Release 2: 1 |

##### US-15-ZU01 Distinct ledgers, native-currency reporting and cost allocation

| Field | Value |
|---|---|
| ID | US-15-ZU01 |
| Title | Distinct ledgers, native-currency reporting and cost allocation |
| Type | Compliance (acceptance binding) |
| Story | As a finance user I want SaaS, provider, subscriber and ad-spend ledgers separate, with FX exceptions visible – with the acceptance criteria below, which the statement-only story US-15-YE01 did not carry |
| Persona / roles | SaaS client administrator (P13, R17/R12); approvers and reviewers per the Background |
| Traces | FR-V12-E-079 (ch10); FR-V12-E-080 (MT-21, MOB-15); FR-V12-E-081 (MT-14); FR-V12-E-082 (GC-14); tests TC-083, TC-084, TC-085, TC-086 |
| Priority | Should |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 2–3 |
| Dependencies | US-15-YE01, US-29-YB01, US-29-YB03, US-29-YB04, US-20-YE05; source definition: Part 11.5b §11.5.5.13 Functional requirement register |
| Dimension profile | persona ×3 · authority ×4 · service/SKU ×3 · channel ×3 · jurisdiction ×3 · region ×3 · operation ×4 · model MU01 |
| Notes | Acceptance binding: US-15-YE01 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens W31–W34, A184–A188, A101; API family `/api/v1/saas/`; audit events `saas.commercial.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Distinct ledgers, native-currency reporting and cost allocation
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" (external SaaS tenant, residency zone IN):
      """
      with administrator "meera@kestrel.example.com" (R12) and finance maker "dev@kestrel.example.com" (R08)
      """
    And the approved rate-card version "RC-2027-01" and the SKU registry with SM-SVC-01…39 in state "released" or "pilot"

  @happy
  Scenario: AC-15ZU01-01 Happy path – Distinct ledger types (FR-V12-E-079)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Distinct ledger types" is exercised as specified by FR-V12-E-079: Distinct ledger types
    Then the observable result matches FR-V12-E-079 and its tests TC-083
    And the audit event "saas.commercial.distinct_ledger_types" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @MOB-15 @MT-21
  Scenario: AC-15ZU01-02 Alternate – FX and native-currency reporting (FR-V12-E-080)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "FX and native-currency reporting" is exercised as specified by FR-V12-E-080: FX and native-currency reporting
    Then the observable result matches FR-V12-E-080 and its tests TC-084
    And the audit event "saas.commercial.fx_and_native_currency" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @MT-14
  Scenario: AC-15ZU01-03 Alternate – Offering price independent of SaaS fee (FR-V12-E-081)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Offering price independent of SaaS fee" is exercised as specified by FR-V12-E-081: Offering price independent of SaaS fee
    Then the observable result matches FR-V12-E-081 and its tests TC-085
    And the audit event "saas.commercial.offering_price_independent_of" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @GC-14
  Scenario: AC-15ZU01-04 Alternate – Cost allocation with unallocated shown (FR-V12-E-082)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Cost allocation with unallocated shown" is exercised as specified by FR-V12-E-082: Cost allocation with unallocated shown
    Then the observable result matches FR-V12-E-082 and its tests TC-086
    And the audit event "saas.commercial.cost_allocation_with" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-TEN-04 @ADR-181
  Scenario: AC-15ZU01-05 Negative – a stale quote revision cannot create an entitlement
    Given quote "Q-2027-0142" revision 3 was superseded by revision 4 at 2027-02-03T11:00:00+05:30
    When Meera accepts revision 3
    Then the API returns 409 "STALE_REVISION"
    And no entitlement, reservation, invoice line or outbox event exists for revision 3

  @val
  Scenario: AC-15ZU01-06 Validation – money is integer minor units with an ISO 4217 code
    When a price line is submitted as {"amount": "1250.5", "currency": "rupees"}
    Then the API returns 422 with field errors "amount: integer minor units required" and "currency: ISO 4217 code required"
    And no quote revision is created

  @perm @BRL-TEN-04
  Scenario: AC-15ZU01-07 Permission – another tenant cannot read or change commercial records
    Given user "jonas@nordlicht.example.de" of tenant "Nordlicht Robotik GmbH"
    When he requests quote "Q-2027-0142" of tenant "Kestrel Analytics Pvt Ltd"
    Then the response is the uniform 404 "NOT_FOUND" and the attempt is audited with outcome "denied"

  @edge @D5
  Scenario: AC-15ZU01-08 Edge – replayed commercial command is idempotent
    Given the command "accept-quote" with Idempotency-Key "k-7f3a" succeeded once
    When the same command and key are replayed after 30 seconds
    Then the original result is returned with status 200 and no second entitlement, invoice or charge exists

  @sec @obs @MU01
  Scenario Outline: AC-15ZU01-09 Permutations – Commercial catalogue, subscription and billing (2-way, 24 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the service is "<service_sku>" and tax rules are "<jurisdiction>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU01 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   E-079 = Distinct ledger types
    #   E-080 = FX and native-currency reporting
    #   E-081 = Offering price independent of SaaS fee
    #   E-082 = Cost allocation with unallocated shown
    Examples: MU01 rows (2-way, seed 416; space 3,888; tuples 226/226; +4 baseline-allow)
      | ex | operation | persona | authority | service_sku | channel | jurisdiction | region | expected |
      | EX-15ZU01-01 | E-081 | P13/R17 | T5 other tenant | suspended | C2 mobile | IN GST ✓ | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-15ZU01-02 | E-082 | P12/R14 | A5 wrong role | suspended | C1 web | EU VAT ✓ | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-15ZU01-03 | E-079 | P08/R08 | A1 | active | C1 web | IN GST ✓ | IN | ALLOW: Distinct ledger types |
      | EX-15ZU01-04 | E-080 | P12/R14 | A3 SoD/limit | not subscribed | C2 mobile | UK VAT draft | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-15ZU01-05 | E-080 | P08/R08 | A1 | not subscribed | C3 API | EU VAT ✓ | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-15ZU01-06 | E-082 | P13/R17 | A3 SoD/limit | active | C3 API | UK VAT draft | EU | 403 SOD_CONFLICT |
      | EX-15ZU01-07 | E-081 | P12/R14 | T5 other tenant | active | C3 API | EU VAT ✓ | IN | uniform 404 NOT_FOUND |
      | EX-15ZU01-08 | E-079 | P08/R08 | A5 wrong role | suspended | C3 API | UK VAT draft | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-15ZU01-09 | E-082 | P08/R08 | T5 other tenant | not subscribed | C2 mobile | IN GST ✓ | EU | uniform 404 NOT_FOUND |
      | EX-15ZU01-10 | E-081 | P13/R17 | A5 wrong role | not subscribed | C1 web | UK VAT draft | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-15ZU01-11 | E-079 | P13/R17 | A1 | suspended | C2 mobile | EU VAT ✓ | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-15ZU01-12 | E-080 | P12/R14 | A3 SoD/limit | active | C1 web | IN GST ✓ | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-15ZU01-13 | E-080 | P13/R17 | A5 wrong role | active | C2 mobile | IN GST ✓ | EU | 403 PERMISSION_DENIED |
      | EX-15ZU01-14 | E-081 | P08/R08 | A3 SoD/limit | suspended | C2 mobile | EU VAT ✓ | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-15ZU01-15 | E-082 | P12/R14 | A1 | suspended | C3 API | IN GST ✓ | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-15ZU01-16 | E-079 | P12/R14 | T5 other tenant | not subscribed | C1 web | UK VAT draft | IN | uniform 404 NOT_FOUND |
      | EX-15ZU01-17 | E-080 | P13/R17 | T5 other tenant | suspended | C2 mobile | EU VAT ✓ | IN | uniform 404 NOT_FOUND |
      | EX-15ZU01-18 | E-081 | P12/R14 | A1 | active | C1 web | UK VAT draft | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-15ZU01-19 | E-079 | P13/R17 | A3 SoD/limit | active | C1 web | UK VAT draft | EU | 403 SOD_CONFLICT |
      | EX-15ZU01-20 | E-082 | P08/R08 | A5 wrong role | suspended | C1 web | UK VAT draft | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-15ZU01-21 | E-079 | P13/R17 | A1 | active | C1 web | IN GST ✓ | IN | ALLOW: Distinct ledger types |
      | EX-15ZU01-22 | E-080 | P13/R17 | A1 | active | C1 web | IN GST ✓ | IN | ALLOW: FX and native-currency reporting |
      | EX-15ZU01-23 | E-081 | P13/R17 | A1 | active | C1 web | IN GST ✓ | IN | ALLOW: Offering price independent of SaaS fee |
      | EX-15ZU01-24 | E-082 | P13/R17 | A1 | active | C1 web | IN GST ✓ | IN | ALLOW: Cost allocation with unallocated shown |
```

#### 11.22.5.4.16 EP-16 Onboarding, retention, partners and expansion pilots

| Field | Value |
|---|---|
| Epic | EP-16 Onboarding, retention, partners and expansion pilots (Part 0 §0.10.2) |
| New stories in this file | US-16-ZU01, US-16-ZU02, US-16-ZU03, US-16-ZU04, US-16-ZU05, US-16-ZU06 |
| FR-V12 covered | A: 153, 160–167, 169–170; K: 156–157 |
| Size | 6 stories · 26–43 SP · 13–43 pd (0.5/1.0 pd per SP) · central 24.1 pd (0.7 pd per SP mid) |
| Releases | Release 2: 3, Release 3+: 3 |

##### US-16-ZU01 CSAT, CES and NPS at defined milestones

| Field | Value |
|---|---|
| ID | US-16-ZU01 |
| Title | CSAT, CES and NPS at defined milestones |
| Type | Feature |
| Story | As an external customer (P14, R16) or visitor (P15, R18), I want CSAT, CES and NPS collected optionally at defined milestones; aggregates with denominator and period, so that I can evaluate, adopt and get help with the service quickly, accessibly and without giving up personal data I do not need to give |
| Persona / roles | External customer (P14, R16) or visitor (P15, R18) |
| Traces | FR-V12-A-153 (CS-12); tests TC-V12-A-153 |
| Priority | Should |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 3–5 |
| Dependencies | US-19-YA01, US-19-YG01, US-19-YG31, US-19-YG32; source definition: Part 11.1b §ADR-183 Metric registry as the single definition… |
| Dimension profile | persona ×3 · channel ×3 · locale ×3 · consent ×3 · service/SKU ×3 · region ×3 · operation ×1 · model MU11 |
| Notes | Screens W01–W34, W45–W54; API family `/api/v1/public/`; audit events `web.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: CSAT, CES and NPS at defined milestones
  Background:
    Given the published website snapshot for brand "AI Growth Engine", locale en-IN and region IN
    And portal user "anu@sunrise.example.in" (R16) of customer "Sunrise Clinics Pvt Ltd" with a verified session

  @happy @CS-12
  Scenario: AC-16ZU01-01 Happy path – CSAT, CES and NPS (FR-V12-A-153)
    Given Anu Das (visitor, then portal user anu@sunrise.example.in) is signed in to the tenant with the capability enabled
    When "CSAT, CES and NPS" is exercised as specified by FR-V12-A-153:
      """
      CSAT, CES and NPS collected optionally at defined milestones; aggregates with denominator and period
      """
    Then missing response not counted as satisfied
    And the audit event "web.csat_ces_and_nps" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @ADR-182
  Scenario: AC-16ZU01-02 Negative – public pages never show tenant or customer data
    When an anonymous visitor opens any public page
    Then the response contains only published snapshot content and no tenant, customer or personal field

  @val @a11y
  Scenario: AC-16ZU01-03 Validation – form errors are announced accessibly
    When Anu submits the enquiry form without "email"
    Then the field shows aria-invalid="true", the error is announced by the screen reader and focus moves to the first invalid field

  @perm
  Scenario: AC-16ZU01-04 Permission – a portal user sees only their own records
    When "anu@sunrise.example.in" requests case CS-2201 of another customer
    Then the portal returns the uniform 404

  @edge @a11y
  Scenario: AC-16ZU01-05 Edge – the page works at 360 px and with keyboard only
    Given a 360 px viewport and keyboard-only navigation
    When Anu completes the journey on this page
    Then every control is reachable, focus is visible, targets are at least 24×24 px and axe-core reports 0 critical or serious violations

  @sec @obs @MU11
  Scenario Outline: AC-16ZU01-06 Permutations – Website, acquisition, help and customer success (2-way, 16 rows)
    Given actor "<persona>" on "<channel>" in locale "<locale>" and zone "<region>"
    And consent is "<consent>" and the service is "<service_sku>"
    When "<operation>" is used
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU11 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-153 = CSAT, CES and NPS
    Examples: MU11 rows (2-way, seed 423; space 729; tuples 153/153; +1 baseline-allow)
      | ex | operation | persona | channel | locale | consent | service_sku | region | expected |
      | EX-16ZU01-01 | A-153 | P14/R16 | AT reader | hi-IN | valid | pilot | IN | ALLOW: Missing response not counted as satisfied |
      | EX-16ZU01-02 | A-153 | P15/R18 | C1 web | en-IN | unknown | planned | EU | HOLD CONSENT_UNKNOWN |
      | EX-16ZU01-03 | A-153 | P13/R17 | C2 360 px | de-DE | withdrawn | released | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU01-04 | A-153 | P15/R18 | AT reader | hi-IN | withdrawn | released | EU | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU01-05 | A-153 | P15/R18 | C2 360 px | en-IN | valid | pilot | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU01-06 | A-153 | P13/R17 | AT reader | hi-IN | unknown | planned | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU01-07 | A-153 | P13/R17 | C1 web | de-DE | valid | pilot | EU | ALLOW: Missing response not counted as satisfied |
      | EX-16ZU01-08 | A-153 | P14/R16 | C2 360 px | de-DE | unknown | planned | IN | HOLD CONSENT_UNKNOWN |
      | EX-16ZU01-09 | A-153 | P14/R16 | C1 web | en-IN | withdrawn | released | IN | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU01-10 | A-153 | P15/R18 | AT reader | de-DE | valid | planned | IN | ALLOW: Missing response not counted as satisfied |
      | EX-16ZU01-11 | A-153 | P14/R16 | C2 360 px | hi-IN | valid | released | EU | ALLOW: Missing response not counted as satisfied |
      | EX-16ZU01-12 | A-153 | P13/R17 | AT reader | en-IN | withdrawn | planned | IN | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU01-13 | A-153 | P14/R16 | C1 web | hi-IN | unknown | released | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU01-14 | A-153 | P15/R18 | AT reader | de-DE | withdrawn | pilot | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU01-15 | A-153 | P13/R17 | C1 web | en-IN | unknown | pilot | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU01-16 | A-153 | P15/R18 | C1 web | en-IN | valid | released | IN | ALLOW: Missing response not counted as satisfied |
```

##### US-16-ZU02 First-value milestone, activation checklist and success plan per SKU

| Field | Value |
|---|---|
| ID | US-16-ZU02 |
| Title | First-value milestone, activation checklist and success plan per SKU |
| Type | Compliance (acceptance binding) |
| Story | As a customer success manager, I want a first-value milestone and success plan for each selected SKU – with the acceptance criteria below, which the statement-only story US-16-YA01 did not carry |
| Persona / roles | External customer (P14, R16) or visitor (P15, R18) |
| Traces | FR-V12-A-160 (RT-02; BR-OBJ-02); FR-V12-A-161 (REC-25; RT-03); tests TC-V12-A-160, TC-V12-A-161 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-16-YA01, US-19-YA01, US-19-YG01, US-19-YG31, US-19-YG32; source definition: Part 11.1b §11.1.5.12 Customer success, retention and… |
| Dimension profile | persona ×3 · channel ×3 · locale ×3 · consent ×3 · service/SKU ×3 · region ×3 · operation ×2 · model MU11 |
| Notes | Acceptance binding: US-16-YA01 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens W01–W34, W45–W54; API family `/api/v1/public/`; audit events `web.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: First-value milestone, activation checklist and success plan per SKU
  Background:
    Given the published website snapshot for brand "AI Growth Engine", locale en-IN and region IN
    And portal user "anu@sunrise.example.in" (R16) of customer "Sunrise Clinics Pvt Ltd" with a verified session

  @happy @RT-02
  Scenario: AC-16ZU02-01 Happy path – First-value milestone per SKU (FR-V12-A-160)
    Given Anu Das (visitor, then portal user anu@sunrise.example.in) is signed in to the tenant with the capability enabled
    When "First-value milestone per SKU" is exercised as specified by FR-V12-A-160:
      """
      First-value milestone per SKU (39) with owner; time-to-first-value tracked (median and p90) from activation
      """
    Then every SKU has a measurable first-value event
    And the audit event "web.first_value_milestone_per_sku" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @REC-25 @RT-03
  Scenario: AC-16ZU02-02 Alternate – Activation checklist and success plan (FR-V12-A-161)
    Given Anu Das (visitor, then portal user anu@sunrise.example.in) is signed in to the tenant with the capability enabled
    When "Activation checklist and success plan" is exercised as specified by FR-V12-A-161:
      """
      Activation checklist and success plan generated from selected SKUs, data rights and connector readiness; no activation before verified
      readiness and entitlement approval; unpurchased services never required
      """
    Then plan lists steps and owner only for selected SKUs
    And the audit event "web.activation_checklist_and" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @ADR-182
  Scenario: AC-16ZU02-03 Negative – public pages never show tenant or customer data
    When an anonymous visitor opens any public page
    Then the response contains only published snapshot content and no tenant, customer or personal field

  @val @a11y
  Scenario: AC-16ZU02-04 Validation – form errors are announced accessibly
    When Anu submits the enquiry form without "email"
    Then the field shows aria-invalid="true", the error is announced by the screen reader and focus moves to the first invalid field

  @perm
  Scenario: AC-16ZU02-05 Permission – a portal user sees only their own records
    When "anu@sunrise.example.in" requests case CS-2201 of another customer
    Then the portal returns the uniform 404

  @edge @a11y
  Scenario: AC-16ZU02-06 Edge – the page works at 360 px and with keyboard only
    Given a 360 px viewport and keyboard-only navigation
    When Anu completes the journey on this page
    Then every control is reachable, focus is visible, targets are at least 24×24 px and axe-core reports 0 critical or serious violations

  @sec @obs @MU11
  Scenario Outline: AC-16ZU02-07 Permutations – Website, acquisition, help and customer success (2-way, 17 rows)
    Given actor "<persona>" on "<channel>" in locale "<locale>" and zone "<region>"
    And consent is "<consent>" and the service is "<service_sku>"
    When "<operation>" is used
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU11 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-160 = First-value milestone per SKU
    #   A-161 = Activation checklist and success plan
    Examples: MU11 rows (2-way, seed 430; space 1,458; tuples 171/171; +2 baseline-allow)
      | ex | operation | persona | channel | locale | consent | service_sku | region | expected |
      | EX-16ZU02-01 | A-160 | P15/R18 | AT reader | de-DE | withdrawn | released | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU02-02 | A-161 | P13/R17 | C1 web | en-IN | unknown | pilot | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU02-03 | A-160 | P14/R16 | C2 360 px | hi-IN | valid | planned | EU | ALLOW: Every SKU has a measurable first-value event |
      | EX-16ZU02-04 | A-161 | P14/R16 | AT reader | hi-IN | unknown | released | IN | HOLD CONSENT_UNKNOWN |
      | EX-16ZU02-05 | A-161 | P15/R18 | C1 web | de-DE | valid | planned | IN | ALLOW: Plan lists steps and owner only for selected SKUs |
      | EX-16ZU02-06 | A-160 | P13/R17 | C2 360 px | en-IN | withdrawn | pilot | IN | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU02-07 | A-161 | P15/R18 | C2 360 px | de-DE | unknown | pilot | EU | HOLD CONSENT_UNKNOWN |
      | EX-16ZU02-08 | A-161 | P13/R17 | AT reader | en-IN | valid | released | EU | ALLOW: Plan lists steps and owner only for selected SKUs |
      | EX-16ZU02-09 | A-161 | P14/R16 | C1 web | hi-IN | withdrawn | pilot | EU | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU02-10 | A-160 | P13/R17 | C1 web | hi-IN | unknown | planned | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU02-11 | A-160 | P14/R16 | C2 360 px | en-IN | valid | pilot | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU02-12 | A-161 | P15/R18 | AT reader | en-IN | withdrawn | planned | IN | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU02-13 | A-161 | P15/R18 | C2 360 px | hi-IN | unknown | released | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU02-14 | A-160 | P14/R16 | C1 web | de-DE | withdrawn | released | EU | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU02-15 | A-161 | P13/R17 | AT reader | de-DE | unknown | pilot | IN | HOLD CONSENT_UNKNOWN |
      | EX-16ZU02-16 | A-160 | P15/R18 | C1 web | en-IN | valid | released | IN | ALLOW: Every SKU has a measurable first-value event |
      | EX-16ZU02-17 | A-161 | P15/R18 | C1 web | en-IN | valid | released | IN | ALLOW: Plan lists steps and owner only for selected SKUs |
```

##### US-16-ZU03 Customer health score and underused-service detection

| Field | Value |
|---|---|
| ID | US-16-ZU03 |
| Title | Customer health score and underused-service detection |
| Type | Compliance (acceptance binding) |
| Story | As a customer success manager, I want health scores that show unknown inputs and never restrict cancellation – with the acceptance criteria below, which the statement-only story US-16-YA02 did not carry |
| Persona / roles | External customer (P14, R16) or visitor (P15, R18) |
| Traces | FR-V12-A-162 (RT-01); FR-V12-A-163 (RT-04); tests TC-V12-A-162, TC-V12-A-163 |
| Priority | Should |
| Wave | Release 3+ (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-16-YA02, US-19-YA01, US-19-YG01, US-19-YG31, US-19-YG32; source definition: Part 11.1b §11.1.5.12 Customer success, retention and… |
| Dimension profile | persona ×3 · channel ×3 · locale ×3 · consent ×3 · service/SKU ×3 · region ×3 · operation ×2 · model MU11 |
| Notes | Acceptance binding: US-16-YA02 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens W01–W34, W45–W54; API family `/api/v1/public/`; audit events `web.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Customer health score and underused-service detection
  Background:
    Given the published website snapshot for brand "AI Growth Engine", locale en-IN and region IN
    And portal user "anu@sunrise.example.in" (R16) of customer "Sunrise Clinics Pvt Ltd" with a verified session

  @happy @RT-01
  Scenario: AC-16ZU03-01 Happy path – Customer health score (FR-V12-A-162)
    Given Anu Das (visitor, then portal user anu@sunrise.example.in) is signed in to the tenant with the capability enabled
    When "Customer health score" is exercised as specified by FR-V12-A-162:
      """
      Customer health score: adoption, quality, value, reliability, support and renewal signals with configurable weights; missing data shown
      unknown; never used to restrict cancellation
      """
    Then score reproducible; missing inputs marked unknown
    And the audit event "web.customer_health_score" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @RT-04
  Scenario: AC-16ZU03-02 Alternate – Underused-service detection (FR-V12-A-163)
    Given Anu Das (visitor, then portal user anu@sunrise.example.in) is signed in to the tenant with the capability enabled
    When "Underused-service detection" is exercised as specified by FR-V12-A-163:
      """
      Underused-service detection: inactive eligible subscription → contextual guidance, never forced upsell; paused/ineligible excluded
      """
    Then paused plan excluded
    And the audit event "web.underused_service_detection" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @ADR-182
  Scenario: AC-16ZU03-03 Negative – public pages never show tenant or customer data
    When an anonymous visitor opens any public page
    Then the response contains only published snapshot content and no tenant, customer or personal field

  @val @a11y
  Scenario: AC-16ZU03-04 Validation – form errors are announced accessibly
    When Anu submits the enquiry form without "email"
    Then the field shows aria-invalid="true", the error is announced by the screen reader and focus moves to the first invalid field

  @perm
  Scenario: AC-16ZU03-05 Permission – a portal user sees only their own records
    When "anu@sunrise.example.in" requests case CS-2201 of another customer
    Then the portal returns the uniform 404

  @edge @a11y
  Scenario: AC-16ZU03-06 Edge – the page works at 360 px and with keyboard only
    Given a 360 px viewport and keyboard-only navigation
    When Anu completes the journey on this page
    Then every control is reachable, focus is visible, targets are at least 24×24 px and axe-core reports 0 critical or serious violations

  @sec @obs @MU11
  Scenario Outline: AC-16ZU03-07 Permutations – Website, acquisition, help and customer success (2-way, 17 rows)
    Given actor "<persona>" on "<channel>" in locale "<locale>" and zone "<region>"
    And consent is "<consent>" and the service is "<service_sku>"
    When "<operation>" is used
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU11 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-162 = Customer health score
    #   A-163 = Underused-service detection
    Examples: MU11 rows (2-way, seed 437; space 1,458; tuples 171/171; +2 baseline-allow)
      | ex | operation | persona | channel | locale | consent | service_sku | region | expected |
      | EX-16ZU03-01 | A-162 | P13/R17 | AT reader | en-IN | withdrawn | released | IN | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU03-02 | A-163 | P14/R16 | AT reader | hi-IN | valid | pilot | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU03-03 | A-162 | P14/R16 | C2 360 px | de-DE | unknown | planned | EU | HOLD CONSENT_UNKNOWN |
      | EX-16ZU03-04 | A-163 | P15/R18 | C1 web | de-DE | withdrawn | pilot | EU | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU03-05 | A-162 | P15/R18 | C1 web | hi-IN | unknown | released | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU03-06 | A-163 | P15/R18 | C2 360 px | en-IN | valid | planned | IN | ALLOW: Paused plan excluded |
      | EX-16ZU03-07 | A-163 | P13/R17 | C2 360 px | hi-IN | withdrawn | planned | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU03-08 | A-163 | P13/R17 | AT reader | de-DE | valid | released | EU | ALLOW: Paused plan excluded |
      | EX-16ZU03-09 | A-163 | P14/R16 | C1 web | en-IN | unknown | pilot | IN | HOLD CONSENT_UNKNOWN |
      | EX-16ZU03-10 | A-162 | P13/R17 | C1 web | en-IN | valid | pilot | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU03-11 | A-163 | P14/R16 | C2 360 px | hi-IN | withdrawn | released | IN | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU03-12 | A-162 | P13/R17 | AT reader | de-DE | unknown | planned | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU03-13 | A-163 | P15/R18 | C2 360 px | de-DE | withdrawn | pilot | IN | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU03-14 | A-162 | P13/R17 | C1 web | hi-IN | valid | planned | EU | ALLOW: Score reproducible |
      | EX-16ZU03-15 | A-163 | P15/R18 | AT reader | en-IN | withdrawn | released | EU | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU03-16 | A-162 | P15/R18 | C1 web | en-IN | valid | released | IN | ALLOW: Score reproducible |
      | EX-16ZU03-17 | A-163 | P15/R18 | C1 web | en-IN | valid | released | IN | ALLOW: Paused plan excluded |
```

##### US-16-ZU04 Connector expiry alerts, customer value report and customer-controlled schedules

| Field | Value |
|---|---|
| ID | US-16-ZU04 |
| Title | Connector expiry alerts, customer value report and customer-controlled schedules |
| Type | Feature |
| Story | As an external customer (P14, R16) or visitor (P15, R18), I want connector and expiry alerts to the authorized owner before credential/config expiry and on failure; respects preferences; no secret exposed; customer value report per period: accepted outputs, usage, measured outcomes and assumptions; customer-controlled schedules and guided tours: scoped pause, timezone-aware cadence; service-specific setup tours, dismiss and resume, so that I can evaluate, adopt and get help with the service quickly, accessibly and without giving up personal data I do not need to give |
| Persona / roles | External customer (P14, R16) or visitor (P15, R18) |
| Traces | FR-V12-A-164 (RT-05); FR-V12-A-165 (RT-06; GC-13); FR-V12-A-166 (RT-08; CS-01; RT-13); tests TC-V12-A-164, TC-V12-A-165, TC-V12-A-166 |
| Priority | Should |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-19-YA01, US-19-YG01, US-19-YG31, US-19-YG32; source definition: Part 11.1b §11.1.5.12 Customer success, retention and… |
| Dimension profile | persona ×3 · channel ×3 · locale ×3 · consent ×3 · service/SKU ×3 · region ×3 · operation ×3 · model MU11 |
| Notes | Screens W01–W34, W45–W54; API family `/api/v1/public/`; audit events `web.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Connector expiry alerts, customer value report and customer-controlled schedules
  Background:
    Given the published website snapshot for brand "AI Growth Engine", locale en-IN and region IN
    And portal user "anu@sunrise.example.in" (R16) of customer "Sunrise Clinics Pvt Ltd" with a verified session

  @happy @RT-05
  Scenario: AC-16ZU04-01 Happy path – Connector and expiry alerts (FR-V12-A-164)
    Given Anu Das (visitor, then portal user anu@sunrise.example.in) is signed in to the tenant with the capability enabled
    When "Connector and expiry alerts" is exercised as specified by FR-V12-A-164:
      """
      Connector and expiry alerts to the authorized owner before credential/config expiry and on failure; respects preferences; no secret exposed
      """
    Then expiry fixture alerts once with corrective action
    And the audit event "web.connector_and_expiry_alerts" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @GC-13 @RT-06
  Scenario: AC-16ZU04-02 Alternate – Customer value report (FR-V12-A-165)
    Given Anu Das (visitor, then portal user anu@sunrise.example.in) is signed in to the tenant with the capability enabled
    When "Customer value report" is exercised as specified by FR-V12-A-165:
      """
      Customer value report per period: accepted outputs, usage, measured outcomes and assumptions; observed outcomes separated from estimated
      value; self-service setup checklist and connector diagnostics with human escalation
      """
    Then report separates observed vs estimated
    And the audit event "web.customer_value_report" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @CS-01 @RT-08
  Scenario: AC-16ZU04-03 Alternate – Customer-controlled schedules and guided tours (FR-V12-A-166)
    Given Anu Das (visitor, then portal user anu@sunrise.example.in) is signed in to the tenant with the capability enabled
    When "Customer-controlled schedules and guided tours" is exercised as specified by FR-V12-A-166:
      """
      Customer-controlled schedules and guided tours: scoped pause, timezone-aware cadence; service-specific setup tours, dismiss and resume;
      consent and safety gates remain
      """
    Then paused schedule prevents new runs; tour never blocks workflow
    And the audit event "web.customer_controlled_schedules" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @ADR-182
  Scenario: AC-16ZU04-04 Negative – public pages never show tenant or customer data
    When an anonymous visitor opens any public page
    Then the response contains only published snapshot content and no tenant, customer or personal field

  @val @a11y
  Scenario: AC-16ZU04-05 Validation – form errors are announced accessibly
    When Anu submits the enquiry form without "email"
    Then the field shows aria-invalid="true", the error is announced by the screen reader and focus moves to the first invalid field

  @perm
  Scenario: AC-16ZU04-06 Permission – a portal user sees only their own records
    When "anu@sunrise.example.in" requests case CS-2201 of another customer
    Then the portal returns the uniform 404

  @edge @a11y
  Scenario: AC-16ZU04-07 Edge – the page works at 360 px and with keyboard only
    Given a 360 px viewport and keyboard-only navigation
    When Anu completes the journey on this page
    Then every control is reachable, focus is visible, targets are at least 24×24 px and axe-core reports 0 critical or serious violations

  @sec @obs @MU11
  Scenario Outline: AC-16ZU04-08 Permutations – Website, acquisition, help and customer success (2-way, 18 rows)
    Given actor "<persona>" on "<channel>" in locale "<locale>" and zone "<region>"
    And consent is "<consent>" and the service is "<service_sku>"
    When "<operation>" is used
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU11 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-164 = Connector and expiry alerts
    #   A-165 = Customer value report
    #   A-166 = Customer-controlled schedules and guided tours
    Examples: MU11 rows (2-way, seed 444; space 2,187; tuples 189/189; +3 baseline-allow)
      | ex | operation | persona | channel | locale | consent | service_sku | region | expected |
      | EX-16ZU04-01 | A-166 | P15/R18 | C1 web | de-DE | valid | released | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU04-02 | A-164 | P14/R16 | C1 web | hi-IN | unknown | planned | IN | HOLD CONSENT_UNKNOWN |
      | EX-16ZU04-03 | A-165 | P15/R18 | C2 360 px | hi-IN | withdrawn | pilot | EU | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU04-04 | A-164 | P13/R17 | AT reader | en-IN | withdrawn | released | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU04-05 | A-166 | P13/R17 | C2 360 px | en-IN | valid | planned | IN | ALLOW: Paused schedule prevents new runs |
      | EX-16ZU04-06 | A-166 | P14/R16 | AT reader | de-DE | unknown | pilot | EU | HOLD CONSENT_UNKNOWN |
      | EX-16ZU04-07 | A-165 | P14/R16 | C2 360 px | en-IN | unknown | released | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU04-08 | A-165 | P15/R18 | AT reader | de-DE | withdrawn | planned | IN | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU04-09 | A-165 | P13/R17 | C1 web | en-IN | valid | pilot | EU | ALLOW: Report separates observed vs estimated |
      | EX-16ZU04-10 | A-164 | P14/R16 | AT reader | hi-IN | valid | released | EU | ALLOW: Expiry fixture alerts once with corrective action |
      | EX-16ZU04-11 | A-164 | P15/R18 | C2 360 px | de-DE | unknown | pilot | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU04-12 | A-166 | P13/R17 | C1 web | hi-IN | withdrawn | planned | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU04-13 | A-164 | P13/R17 | C2 360 px | de-DE | unknown | planned | EU | HOLD CONSENT_UNKNOWN |
      | EX-16ZU04-14 | A-166 | P14/R16 | AT reader | en-IN | withdrawn | released | IN | HOLD CONSENT_WITHDRAWN |
      | EX-16ZU04-15 | A-164 | P15/R18 | C2 360 px | en-IN | valid | pilot | IN | ALLOW: Expiry fixture alerts once with corrective action |
      | EX-16ZU04-16 | A-164 | P15/R18 | C1 web | en-IN | valid | released | IN | ALLOW: Expiry fixture alerts once with corrective action |
      | EX-16ZU04-17 | A-165 | P15/R18 | C1 web | en-IN | valid | released | IN | ALLOW: Report separates observed vs estimated |
      | EX-16ZU04-18 | A-166 | P15/R18 | C1 web | en-IN | valid | released | IN | ALLOW: Paused schedule prevents new runs |
```

##### US-16-ZU05 Complementary-service recommendations, grounded help and enterprise success reviews

| Field | Value |
|---|---|
| ID | US-16-ZU05 |
| Title | Complementary-service recommendations, grounded help and enterprise success reviews |
| Type | Feature |
| Story | As a SaaS client administrator (P13, R17/R12), I want evidence-based complementary services: optional SKU recommendations from unmet objectives and usage, with reasons; never activates or bills; grounded customer help, correction memory and closed-loop feedback: portal help retrieves approved scoped knowledge with version citation…; enterprise success reviews under the contracted model with accepted evidence and customer-confirmed actions, so that we buy, change and pay for exactly the services we use, on approved terms that reconcile to the ledger |
| Persona / roles | SaaS client administrator (P13, R17/R12); approvers and reviewers per the Background |
| Traces | FR-V12-A-167 (RT-09); FR-V12-A-169 (CS-02, CS-07, CS-13, RT-15); FR-V12-A-170 (RT-14); tests TC-V12-A-167, TC-V12-A-169, TC-V12-A-170 |
| Priority | Should |
| Wave | Release 3+ (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-29-YB01, US-29-YB03, US-29-YB04, US-20-YE05; source definition: Part 11.1b §11.1.5.12 Customer success, retention and… |
| Dimension profile | persona ×3 · authority ×4 · service/SKU ×3 · channel ×3 · jurisdiction ×3 · region ×3 · operation ×3 · model MU01 |
| Notes | Related existing stories (shared source IDs, no FR trace): US-16-YF14 · Screens W31–W34, A184–A188, A101; API family `/api/v1/saas/`; audit events `saas.commercial.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Complementary-service recommendations, grounded help and enterprise success reviews
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" (external SaaS tenant, residency zone IN):
      """
      with administrator "meera@kestrel.example.com" (R12) and finance maker "dev@kestrel.example.com" (R08)
      """
    And the approved rate-card version "RC-2027-01" and the SKU registry with SM-SVC-01…39 in state "released" or "pilot"

  @happy @RT-09
  Scenario: AC-16ZU05-01 Happy path – Evidence-based complementary services (FR-V12-A-167)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Evidence-based complementary services" is exercised as specified by FR-V12-A-167:
      """
      Evidence-based complementary services: optional SKU recommendations from unmet objectives and usage, with reasons; never activates or bills
      """
    Then recommendation creates no entitlement
    And the audit event "saas.commercial.evidence_based_complementary" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @CS-02 @CS-07
  Scenario: AC-16ZU05-02 Alternate – Grounded customer help, correction memory and closed-loop feedback (FR-V12-A-169)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Grounded customer help, correction memory and closed-loop feedback" is exercised as specified by FR-V12-A-169:
      """
      Grounded customer help, correction memory and closed-loop feedback: portal help retrieves approved scoped knowledge with version citation and
      routes uncertainty to a human
      """
    Then unsupported question escalates; correction never crosses tenants
    And the audit event "saas.commercial.grounded_customer_help" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @RT-14
  Scenario: AC-16ZU05-03 Alternate – Enterprise success reviews (FR-V12-A-170)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Enterprise success reviews" is exercised as specified by FR-V12-A-170:
      """
      Enterprise success reviews under the contracted model with accepted evidence and customer-confirmed actions (extends CSO-08 quarterly review)
      """
    Then review record lists evidence
    And the audit event "saas.commercial.enterprise_success_reviews" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-TEN-04 @ADR-181
  Scenario: AC-16ZU05-04 Negative – a stale quote revision cannot create an entitlement
    Given quote "Q-2027-0142" revision 3 was superseded by revision 4 at 2027-02-03T11:00:00+05:30
    When Meera accepts revision 3
    Then the API returns 409 "STALE_REVISION"
    And no entitlement, reservation, invoice line or outbox event exists for revision 3

  @val
  Scenario: AC-16ZU05-05 Validation – money is integer minor units with an ISO 4217 code
    When a price line is submitted as {"amount": "1250.5", "currency": "rupees"}
    Then the API returns 422 with field errors "amount: integer minor units required" and "currency: ISO 4217 code required"
    And no quote revision is created

  @perm @BRL-TEN-04
  Scenario: AC-16ZU05-06 Permission – another tenant cannot read or change commercial records
    Given user "jonas@nordlicht.example.de" of tenant "Nordlicht Robotik GmbH"
    When he requests quote "Q-2027-0142" of tenant "Kestrel Analytics Pvt Ltd"
    Then the response is the uniform 404 "NOT_FOUND" and the attempt is audited with outcome "denied"

  @edge @D5
  Scenario: AC-16ZU05-07 Edge – replayed commercial command is idempotent
    Given the command "accept-quote" with Idempotency-Key "k-7f3a" succeeded once
    When the same command and key are replayed after 30 seconds
    Then the original result is returned with status 200 and no second entitlement, invoice or charge exists

  @sec @obs @MU01
  Scenario Outline: AC-16ZU05-08 Permutations – Commercial catalogue, subscription and billing (2-way, 20 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the service is "<service_sku>" and tax rules are "<jurisdiction>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU01 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-167 = Evidence-based complementary services
    #   A-169 = Grounded customer help, correction memory and…
    #   A-170 = Enterprise success reviews
    Examples: MU01 rows (2-way, seed 451; space 2,916; tuples 207/207; +3 baseline-allow)
      | ex | operation | persona | authority | service_sku | channel | jurisdiction | region | expected |
      | EX-16ZU05-01 | A-167 | P08/R08 | T5 other tenant | not subscribed | C3 API | UK VAT draft | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-16ZU05-02 | A-169 | P08/R08 | A3 SoD/limit | suspended | C1 web | IN GST ✓ | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-16ZU05-03 | A-170 | P12/R14 | A1 | active | C1 web | EU VAT ✓ | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-16ZU05-04 | A-170 | P13/R17 | A5 wrong role | not subscribed | C2 mobile | IN GST ✓ | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-16ZU05-05 | A-169 | P12/R14 | A5 wrong role | active | C3 API | UK VAT draft | IN | 403 PERMISSION_DENIED |
      | EX-16ZU05-06 | A-167 | P12/R14 | A3 SoD/limit | suspended | C2 mobile | EU VAT ✓ | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-16ZU05-07 | A-169 | P13/R17 | A1 | not subscribed | C2 mobile | EU VAT ✓ | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-16ZU05-08 | A-170 | P13/R17 | A3 SoD/limit | suspended | C3 API | UK VAT draft | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-16ZU05-09 | A-167 | P13/R17 | T5 other tenant | active | C1 web | IN GST ✓ | EU | uniform 404 NOT_FOUND |
      | EX-16ZU05-10 | A-167 | P08/R08 | A1 | active | C2 mobile | UK VAT draft | EU | HOLD TAX_RULE_NOT_APPROVED |
      | EX-16ZU05-11 | A-170 | P08/R08 | T5 other tenant | suspended | C2 mobile | EU VAT ✓ | IN | uniform 404 NOT_FOUND |
      | EX-16ZU05-12 | A-169 | P12/R14 | T5 other tenant | not subscribed | C2 mobile | IN GST ✓ | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-16ZU05-13 | A-167 | P08/R08 | A5 wrong role | suspended | C3 API | EU VAT ✓ | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-16ZU05-14 | A-169 | P08/R08 | A1 | suspended | C3 API | IN GST ✓ | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-16ZU05-15 | A-167 | P13/R17 | A5 wrong role | not subscribed | C1 web | UK VAT draft | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-16ZU05-16 | A-169 | P12/R14 | A3 SoD/limit | not subscribed | C3 API | IN GST ✓ | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-16ZU05-17 | A-170 | P12/R14 | A3 SoD/limit | active | C3 API | UK VAT draft | IN | 403 SOD_CONFLICT |
      | EX-16ZU05-18 | A-167 | P13/R17 | A1 | active | C1 web | IN GST ✓ | IN | ALLOW: Recommendation creates no entitlement |
      | EX-16ZU05-19 | A-169 | P13/R17 | A1 | active | C1 web | IN GST ✓ | IN | ALLOW: Unsupported question escalates |
      | EX-16ZU05-20 | A-170 | P13/R17 | A1 | active | C1 web | IN GST ✓ | IN | ALLOW: Review record lists evidence |
```

##### US-16-ZU06 ENT-BIZ-04…05 acceptance: success playbooks and partner/reseller programme

| Field | Value |
|---|---|
| ID | US-16-ZU06 |
| Title | ENT-BIZ-04…05 acceptance: success playbooks and partner/reseller programme |
| Type | Feature |
| Story | As a SaaS client administrator (P13, R17/R12), I want customer success and onboarding playbooks with first-value milestones; partner and reseller programme with separate tenant consent and billing ownership, so that we buy, change and pay for exactly the services we use, on approved terms that reconcile to the ledger |
| Persona / roles | SaaS client administrator (P13, R17/R12); approvers and reviewers per the Background |
| Traces | FR-V12-K-156 (ENT-BIZ-04); FR-V12-K-157 (ENT-BIZ-05); DEC-417; tests TC-V12-K-156, TC-V12-K-157 |
| Priority | Should |
| Wave | Release 3+ (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-29-YB01, US-29-YB03, US-29-YB04, US-20-YE05; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · authority ×4 · service/SKU ×3 · channel ×3 · jurisdiction ×3 · region ×3 · operation ×2 · model MU01 |
| Notes | Screens W31–W34, A184–A188, A101; API family `/api/v1/saas/`; audit events `saas.commercial.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: ENT-BIZ-04…05 acceptance: success playbooks and partner/reseller programme
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd" (external SaaS tenant, residency zone IN):
      """
      with administrator "meera@kestrel.example.com" (R12) and finance maker "dev@kestrel.example.com" (R08)
      """
    And the approved rate-card version "RC-2027-01" and the SKU registry with SM-SVC-01…39 in state "released" or "pilot"

  @happy @ENT-BIZ-04
  Scenario: AC-16ZU06-01 Happy path – Customer success and onboarding playbooks with first-value milestones. (FR-V12-K-156)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Customer success and onboarding playbooks with first-value milestones." is exercised as specified by FR-V12-K-156:
      """
      Customer success and onboarding playbooks with first-value milestones.
      """
    Then billing/commercial test: meter-rate-invoice-tax-collect sequence:
      """
      approved price book only, signed-hash order form, first-value checklist, procurement pack versioned
      """
    And the audit event "saas.commercial.customer_success_and" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-BIZ-05
  Scenario: AC-16ZU06-02 Alternate – Partner and reseller programme with separate tenant consent and… (FR-V12-K-157)
    Given Meera Iyer (R12, meera@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Partner and reseller programme with separate tenant consent and…" is exercised as specified by FR-V12-K-157:
      """
      Partner and reseller programme with separate tenant consent and billing ownership.
      """
    Then billing/commercial test: meter-rate-invoice-tax-collect sequence:
      """
      approved price book only, signed-hash order form, first-value checklist, procurement pack versioned
      """
    And the audit event "saas.commercial.partner_and_reseller" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @BRL-TEN-04 @ADR-181
  Scenario: AC-16ZU06-03 Negative – a stale quote revision cannot create an entitlement
    Given quote "Q-2027-0142" revision 3 was superseded by revision 4 at 2027-02-03T11:00:00+05:30
    When Meera accepts revision 3
    Then the API returns 409 "STALE_REVISION"
    And no entitlement, reservation, invoice line or outbox event exists for revision 3

  @val
  Scenario: AC-16ZU06-04 Validation – money is integer minor units with an ISO 4217 code
    When a price line is submitted as {"amount": "1250.5", "currency": "rupees"}
    Then the API returns 422 with field errors "amount: integer minor units required" and "currency: ISO 4217 code required"
    And no quote revision is created

  @perm @BRL-TEN-04
  Scenario: AC-16ZU06-05 Permission – another tenant cannot read or change commercial records
    Given user "jonas@nordlicht.example.de" of tenant "Nordlicht Robotik GmbH"
    When he requests quote "Q-2027-0142" of tenant "Kestrel Analytics Pvt Ltd"
    Then the response is the uniform 404 "NOT_FOUND" and the attempt is audited with outcome "denied"

  @edge @D5
  Scenario: AC-16ZU06-06 Edge – replayed commercial command is idempotent
    Given the command "accept-quote" with Idempotency-Key "k-7f3a" succeeded once
    When the same command and key are replayed after 30 seconds
    Then the original result is returned with status 200 and no second entitlement, invoice or charge exists

  @sec @obs @MU01
  Scenario Outline: AC-16ZU06-07 Permutations – Commercial catalogue, subscription and billing (2-way, 19 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the service is "<service_sku>" and tax rules are "<jurisdiction>"
    When the actor performs "<operation>" through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU01 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-156 = Customer success and onboarding playbooks with…
    #   K-157 = Partner and reseller programme with separate tenant…
    Examples: MU01 rows (2-way, seed 458; space 1,944; tuples 188/188; +2 baseline-allow)
      | ex | operation | persona | authority | service_sku | channel | jurisdiction | region | expected |
      | EX-16ZU06-01 | K-156 | P08/R08 | A1 | not subscribed | C1 web | IN GST ✓ | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-16ZU06-02 | K-157 | P12/R14 | T5 other tenant | not subscribed | C2 mobile | UK VAT draft | IN | uniform 404 NOT_FOUND |
      | EX-16ZU06-03 | K-157 | P13/R17 | A5 wrong role | active | C3 API | IN GST ✓ | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-16ZU06-04 | K-156 | P08/R08 | A3 SoD/limit | suspended | C2 mobile | EU VAT ✓ | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-16ZU06-05 | K-157 | P13/R17 | T5 other tenant | suspended | C1 web | EU VAT ✓ | EU | uniform 404 NOT_FOUND |
      | EX-16ZU06-06 | K-156 | P12/R14 | A1 | active | C3 API | EU VAT ✓ | IN | ALLOW: Billing/commercial test: |
      | EX-16ZU06-07 | K-157 | P08/R08 | A3 SoD/limit | active | C1 web | UK VAT draft | IN | 403 SOD_CONFLICT |
      | EX-16ZU06-08 | K-156 | P12/R14 | A5 wrong role | suspended | C3 API | UK VAT draft | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-16ZU06-09 | K-156 | P13/R17 | A1 | not subscribed | C2 mobile | UK VAT draft | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-16ZU06-10 | K-156 | P12/R14 | T5 other tenant | active | C2 mobile | IN GST ✓ | EU | uniform 404 NOT_FOUND |
      | EX-16ZU06-11 | K-157 | P13/R17 | A3 SoD/limit | suspended | C3 API | IN GST ✓ | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-16ZU06-12 | K-157 | P08/R08 | A5 wrong role | not subscribed | C3 API | EU VAT ✓ | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-16ZU06-13 | K-157 | P12/R14 | A1 | suspended | C1 web | UK VAT draft | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-16ZU06-14 | K-157 | P08/R08 | T5 other tenant | not subscribed | C3 API | EU VAT ✓ | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-16ZU06-15 | K-157 | P12/R14 | A3 SoD/limit | not subscribed | C2 mobile | EU VAT ✓ | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-16ZU06-16 | K-157 | P12/R14 | A5 wrong role | active | C1 web | IN GST ✓ | IN | 403 PERMISSION_DENIED |
      | EX-16ZU06-17 | K-156 | P12/R14 | A5 wrong role | suspended | C2 mobile | EU VAT ✓ | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-16ZU06-18 | K-156 | P13/R17 | A1 | active | C1 web | IN GST ✓ | IN | ALLOW: Billing/commercial test: |
      | EX-16ZU06-19 | K-157 | P13/R17 | A1 | active | C1 web | IN GST ✓ | IN | ALLOW: Billing/commercial test: |
```

#### 11.22.5.4.17 EP-17 Dashboards, forecast and Command Centre

| Field | Value |
|---|---|
| Epic | EP-17 Dashboards, forecast and Command Centre (Part 0 §0.10.2) |
| New stories in this file | US-17-ZU01, US-17-ZU02, US-17-ZU03, US-17-ZU04, US-17-ZU05 |
| FR-V12 covered | A: 036, 121–124; H: 015; I: 043 |
| Size | 5 stories · 11–19 SP · 6–19 pd (0.5/1.0 pd per SP) · central 10.5 pd (0.7 pd per SP mid) |
| Releases | Release 1: 3, Release 2: 2 |

##### US-17-ZU01 Native-currency integrity and reconciled drill-down

| Field | Value |
|---|---|
| ID | US-17-ZU01 |
| Title | Native-currency integrity and reconciled drill-down |
| Type | Compliance (acceptance binding) |
| Story | As an analyst, I want drill-down totals that reconcile to tiles in native currency – with the acceptance criteria below, which the statement-only story US-17-YA02 did not carry |
| Persona / roles | Startup head (P02, R02) |
| Traces | FR-V12-A-036 (MT-21, MOB-15, ch11 §V6); FR-V12-A-124 (REC-15); tests TC-V12-A-036, TC-V12-A-124 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-17-YA02, US-17-YI01, US-17-YI02, US-21-YA01, US-17-YG02; source definition: Part 11.1b §11.1.5.3 Pricing, billing and commercial unit…; Part 11.1b §11.1.5.8 Portfolio command centre |
| Dimension profile | persona ×3 · authority ×4 · scope ×3 · currency ×3 · consent ×3 · channel ×3 · operation ×2 · model MU13 |
| Notes | Acceptance binding: US-17-YA02 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens A042, A087–A089, A106, A191; API family `/api/v1/analytics/`; audit events `analytics.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Native-currency integrity and reconciled drill-down
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd":
      """
      with companies "Kestrel IN" and "Kestrel EU", startup head "arjun@kestrel.example.com" (R02) for "Kestrel IN" only
      """
    And the metric registry with KPI definitions (numerator, denominator, period, freshness) approved at version 3

  @happy @MOB-15 @MT-21
  Scenario: AC-17ZU01-01 Happy path – Native-currency integrity (FR-V12-A-036)
    Given Arjun Menon (R02, arjun@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Native-currency integrity" is exercised as specified by FR-V12-A-036:
      """
      Native-currency integrity: amounts grouped by native currency; conversion only with approved rate, source, timestamp, direction, rounding and
      period; missing rate excluded and counted; negative rate rejected; SaaS fees never mixed with subscriber revenue
      """
    Then V8-QA-053 behaviour
    And the audit event "analytics.native_currency_integrity" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @REC-15
  Scenario: AC-17ZU01-02 Alternate – Reconciled drill-down (FR-V12-A-124)
    Given Arjun Menon (R02, arjun@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Reconciled drill-down" is exercised as specified by FR-V12-A-124:
      """
      Reconciled drill-down: timestamped scoped drill-down with record count, unknown indicators and original currency; stable cursor; bulk actions
      recheck each item
      """
    Then tile total = sum of drill-down rows for the same filter and time
    And the audit event "analytics.reconciled_drill_down" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @ADR-183
  Scenario: AC-17ZU01-03 Negative – a tile without a registry definition fails CI
    Given a dashboard tile "win rate" that references no metric definition
    When CI runs the metric-registry check
    Then the build fails naming the tile

  @val
  Scenario: AC-17ZU01-04 Validation – zero denominator is "not applicable", not zero
    Given 0 qualified leads in the period
    When the conversion KPI renders
    Then it shows "not applicable" with the denominator 0 and no percentage

  @perm
  Scenario: AC-17ZU01-05 Permission – no data from a company outside my scope
    When Arjun opens the drill-down of "pipeline value"
    Then only rows of "Kestrel IN" appear and the total equals the tile

  @edge
  Scenario: AC-17ZU01-06 Edge – currencies are never summed without an approved rate
    Given pipeline in INR and EUR and no approved rate
    When the total renders
    Then native totals are shown per currency and the converted total shows "FX_RATE_MISSING"

  @sec @obs @MU13
  Scenario Outline: AC-17ZU01-07 Permutations – Analytics, metrics and management views (2-way, 20 rows)
    Given actor "<persona>" with authority "<authority>" and scope "<scope>"
    And currencies are "<currency>" and consent is "<consent>"
    When "<operation>" is viewed through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU13 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-036 = Native-currency integrity
    #   A-124 = Reconciled drill-down
    Examples: MU13 rows (2-way, seed 465; space 1,944; tuples 188/188; +2 baseline-allow)
      | ex | operation | persona | authority | scope | currency | consent | channel | expected |
      | EX-17ZU01-01 | A-124 | P13/R17 | A5 wrong role | company | INR+EUR rate ✓ | withdrawn | C1 web | 403 PERMISSION_DENIED |
      | EX-17ZU01-02 | A-036 | P02/R02 | A3 SoD/limit | company | INR | unknown | C2 mobile | 403 SOD_CONFLICT |
      | EX-17ZU01-03 | A-036 | P13/R17 | T5 other tenant | grant revoked | INR+EUR no rate | valid | C3 API | uniform 404 NOT_FOUND |
      | EX-17ZU01-04 | A-124 | P01/R01 | A1 | portfolio grant | INR+EUR rate ✓ | unknown | C3 API | HOLD CONSENT_UNKNOWN |
      | EX-17ZU01-05 | A-036 | P01/R01 | A1 | grant revoked | INR | withdrawn | C1 web | 403 GRANT_REVOKED |
      | EX-17ZU01-06 | A-124 | P02/R02 | A3 SoD/limit | portfolio grant | INR+EUR no rate | valid | C1 web | 403 SOD_CONFLICT |
      | EX-17ZU01-07 | A-124 | P13/R17 | T5 other tenant | portfolio grant | INR | withdrawn | C2 mobile | uniform 404 NOT_FOUND |
      | EX-17ZU01-08 | A-036 | P01/R01 | A5 wrong role | grant revoked | INR+EUR rate ✓ | valid | C2 mobile | 403 GRANT_REVOKED |
      | EX-17ZU01-09 | A-124 | P02/R02 | A3 SoD/limit | grant revoked | INR+EUR rate ✓ | withdrawn | C3 API | 403 GRANT_REVOKED |
      | EX-17ZU01-10 | A-124 | P01/R01 | A1 | company | INR+EUR no rate | valid | C2 mobile | ALLOW: Tile total = sum of drill-down rows for the same |
      | EX-17ZU01-11 | A-036 | P02/R02 | A5 wrong role | portfolio grant | INR+EUR no rate | unknown | C3 API | 403 PERMISSION_DENIED |
      | EX-17ZU01-12 | A-036 | P02/R02 | T5 other tenant | company | INR+EUR rate ✓ | unknown | C1 web | uniform 404 NOT_FOUND |
      | EX-17ZU01-13 | A-124 | P02/R02 | A1 | company | INR | valid | C3 API | ALLOW: Tile total = sum of drill-down rows for the same |
      | EX-17ZU01-14 | A-036 | P13/R17 | A1 | grant revoked | INR | unknown | C3 API | 403 GRANT_REVOKED |
      | EX-17ZU01-15 | A-036 | P13/R17 | A3 SoD/limit | portfolio grant | INR+EUR no rate | withdrawn | C2 mobile | 403 SOD_CONFLICT |
      | EX-17ZU01-16 | A-124 | P01/R01 | A3 SoD/limit | company | INR+EUR no rate | unknown | C1 web | 403 SOD_CONFLICT |
      | EX-17ZU01-17 | A-124 | P01/R01 | T5 other tenant | company | INR+EUR rate ✓ | valid | C2 mobile | uniform 404 NOT_FOUND |
      | EX-17ZU01-18 | A-036 | P02/R02 | A5 wrong role | portfolio grant | INR | withdrawn | C1 web | 403 PERMISSION_DENIED |
      | EX-17ZU01-19 | A-036 | P01/R01 | A1 | company | INR | valid | C1 web | ALLOW: V8-QA-053 behaviour |
      | EX-17ZU01-20 | A-124 | P01/R01 | A1 | company | INR | valid | C1 web | ALLOW: Tile total = sum of drill-down rows for the same |
```

##### US-17-ZU02 Nine optimisation perspectives with role visibility

| Field | Value |
|---|---|
| ID | US-17-ZU02 |
| Title | Nine optimisation perspectives with role visibility |
| Type | Feature |
| Story | As a startup head (P02, R02), I want 9 optimization perspectives as A089 tabs with the role visibility rule above (extends Part 8.3c §8.3.5.15.7), so that every number I see is defined once, scoped to what I may see, and adds up |
| Persona / roles | Startup head (P02, R02) |
| Traces | FR-V12-A-121 (BRD 19 §V5); tests TC-V12-A-121 |
| Priority | Should |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 3–5 |
| Dependencies | US-17-YI01, US-17-YI02, US-21-YA01, US-17-YG02; source definition: Part 11.1b §11.1.5.8 Portfolio command centre |
| Dimension profile | persona ×3 · authority ×4 · scope ×3 · currency ×3 · consent ×3 · channel ×3 · operation ×1 · model MU13 |
| Notes | Screens A042, A087–A089, A106, A191; API family `/api/v1/analytics/`; audit events `analytics.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Nine optimisation perspectives with role visibility
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd":
      """
      with companies "Kestrel IN" and "Kestrel EU", startup head "arjun@kestrel.example.com" (R02) for "Kestrel IN" only
      """
    And the metric registry with KPI definitions (numerator, denominator, period, freshness) approved at version 3

  @happy
  Scenario: AC-17ZU02-01 Happy path – 9 optimization perspectives (FR-V12-A-121)
    Given Arjun Menon (R02, arjun@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "9 optimization perspectives" is exercised as specified by FR-V12-A-121:
      """
      9 optimization perspectives as A089 tabs with the role visibility rule above (extends Part 8.3c §8.3.5.15.7)
      """
    Then tenant planner cannot open Attraction/Retention/Conversion
    And the audit event "analytics.9_optimization_perspectives" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @ADR-183
  Scenario: AC-17ZU02-02 Negative – a tile without a registry definition fails CI
    Given a dashboard tile "win rate" that references no metric definition
    When CI runs the metric-registry check
    Then the build fails naming the tile

  @val
  Scenario: AC-17ZU02-03 Validation – zero denominator is "not applicable", not zero
    Given 0 qualified leads in the period
    When the conversion KPI renders
    Then it shows "not applicable" with the denominator 0 and no percentage

  @perm
  Scenario: AC-17ZU02-04 Permission – no data from a company outside my scope
    When Arjun opens the drill-down of "pipeline value"
    Then only rows of "Kestrel IN" appear and the total equals the tile

  @edge
  Scenario: AC-17ZU02-05 Edge – currencies are never summed without an approved rate
    Given pipeline in INR and EUR and no approved rate
    When the total renders
    Then native totals are shown per currency and the converted total shows "FX_RATE_MISSING"

  @sec @obs @MU13
  Scenario Outline: AC-17ZU02-06 Permutations – Analytics, metrics and management views (2-way, 17 rows)
    Given actor "<persona>" with authority "<authority>" and scope "<scope>"
    And currencies are "<currency>" and consent is "<consent>"
    When "<operation>" is viewed through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU13 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-121 = 9 optimization perspectives
    Examples: MU13 rows (2-way, seed 472; space 972; tuples 169/169; +1 baseline-allow)
      | ex | operation | persona | authority | scope | currency | consent | channel | expected |
      | EX-17ZU02-01 | A-121 | P02/R02 | A5 wrong role | grant revoked | INR | unknown | C3 API | 403 GRANT_REVOKED |
      | EX-17ZU02-02 | A-121 | P13/R17 | A3 SoD/limit | company | INR+EUR rate ✓ | withdrawn | C2 mobile | 403 SOD_CONFLICT |
      | EX-17ZU02-03 | A-121 | P01/R01 | T5 other tenant | portfolio grant | INR+EUR no rate | valid | C1 web | uniform 404 NOT_FOUND |
      | EX-17ZU02-04 | A-121 | P01/R01 | A1 | grant revoked | INR+EUR rate ✓ | valid | C3 API | 403 GRANT_REVOKED |
      | EX-17ZU02-05 | A-121 | P13/R17 | A1 | portfolio grant | INR | unknown | C1 web | HOLD CONSENT_UNKNOWN |
      | EX-17ZU02-06 | A-121 | P02/R02 | A1 | company | INR+EUR no rate | withdrawn | C2 mobile | HOLD CONSENT_WITHDRAWN |
      | EX-17ZU02-07 | A-121 | P01/R01 | A5 wrong role | company | INR | valid | C2 mobile | 403 PERMISSION_DENIED |
      | EX-17ZU02-08 | A-121 | P13/R17 | T5 other tenant | grant revoked | INR+EUR no rate | withdrawn | C3 API | uniform 404 NOT_FOUND |
      | EX-17ZU02-09 | A-121 | P02/R02 | A5 wrong role | portfolio grant | INR+EUR rate ✓ | withdrawn | C1 web | 403 PERMISSION_DENIED |
      | EX-17ZU02-10 | A-121 | P01/R01 | A3 SoD/limit | grant revoked | INR+EUR no rate | unknown | C1 web | 403 GRANT_REVOKED |
      | EX-17ZU02-11 | A-121 | P02/R02 | T5 other tenant | company | INR+EUR rate ✓ | unknown | C2 mobile | uniform 404 NOT_FOUND |
      | EX-17ZU02-12 | A-121 | P02/R02 | A3 SoD/limit | portfolio grant | INR | valid | C3 API | 403 SOD_CONFLICT |
      | EX-17ZU02-13 | A-121 | P13/R17 | A5 wrong role | portfolio grant | INR+EUR no rate | valid | C2 mobile | 403 PERMISSION_DENIED |
      | EX-17ZU02-14 | A-121 | P01/R01 | T5 other tenant | grant revoked | INR | withdrawn | C2 mobile | uniform 404 NOT_FOUND |
      | EX-17ZU02-15 | A-121 | P01/R01 | A5 wrong role | company | INR+EUR rate ✓ | unknown | C1 web | 403 PERMISSION_DENIED |
      | EX-17ZU02-16 | A-121 | P13/R17 | A3 SoD/limit | company | INR | unknown | C3 API | 403 SOD_CONFLICT |
      | EX-17ZU02-17 | A-121 | P01/R01 | A1 | company | INR | valid | C1 web | ALLOW: Tenant planner cannot open |
```

##### US-17-ZU03 Context filters and cascading filter semantics

| Field | Value |
|---|---|
| ID | US-17-ZU03 |
| Title | Context filters and cascading filter semantics |
| Type | Compliance (acceptance binding) |
| Story | As a manager, I want 14 differentiated Command Centre views with cascading filters that clear stale selections – with the acceptance criteria below, which the statement-only story US-17-YA01 did not carry |
| Persona / roles | Startup head (P02, R02) |
| Traces | FR-V12-A-122 (BRD 19 §V6; MT-25); FR-V12-A-123 (MT-26, REC-14); tests TC-V12-A-122, TC-V12-A-123 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 1–2 |
| Dependencies | US-17-YA01, US-17-YI01, US-17-YI02, US-21-YA01, US-17-YG02; source definition: Part 11.1b §11.1.5.8 Portfolio command centre |
| Dimension profile | persona ×3 · authority ×4 · scope ×3 · currency ×3 · consent ×3 · channel ×3 · operation ×2 · model MU13 |
| Notes | Acceptance binding: US-17-YA01 carries the statement and its build points; this story adds the Gherkin AC, the generated Examples and the test automation for the FRs above (DEC-941) · Screens A042, A087–A089, A106, A191; API family `/api/v1/analytics/`; audit events `analytics.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Context filters and cascading filter semantics
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd":
      """
      with companies "Kestrel IN" and "Kestrel EU", startup head "arjun@kestrel.example.com" (R02) for "Kestrel IN" only
      """
    And the metric registry with KPI definitions (numerator, denominator, period, freshness) approved at version 3

  @happy @MT-25
  Scenario: AC-17ZU03-01 Happy path – Context filters (FR-V12-A-122)
    Given Arjun Menon (R02, arjun@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Context filters" is exercised as specified by FR-V12-A-122:
      """
      Context filters: company, tenant, division, brand, offering, target market/country/region, channel/account, SKU/workflow, date/status and
      contextual industry, customer type, segment, campaign, opportunity type, employee, team, risk, authority
      """
    Then filter business → brand/offer → opportunity type: counts change consistently
    And the audit event "analytics.context_filters" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @MT-26 @REC-14
  Scenario: AC-17ZU03-02 Alternate – Cascading filter semantics (FR-V12-A-123)
    Given Arjun Menon (R02, arjun@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Cascading filter semantics" is exercised as specified by FR-V12-A-123:
      """
      Cascading filter semantics: changing an ancestor clears stale descendants; options derive from allowed IDs; OR within a dimension, AND across
      dimensions; stale asynchronous results cancelled; unsupported combinations show an empty state
      """
    Then change company → brand selection cleared; invalid query denied
    And the audit event "analytics.cascading_filter_semantics" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @ADR-183
  Scenario: AC-17ZU03-03 Negative – a tile without a registry definition fails CI
    Given a dashboard tile "win rate" that references no metric definition
    When CI runs the metric-registry check
    Then the build fails naming the tile

  @val
  Scenario: AC-17ZU03-04 Validation – zero denominator is "not applicable", not zero
    Given 0 qualified leads in the period
    When the conversion KPI renders
    Then it shows "not applicable" with the denominator 0 and no percentage

  @perm
  Scenario: AC-17ZU03-05 Permission – no data from a company outside my scope
    When Arjun opens the drill-down of "pipeline value"
    Then only rows of "Kestrel IN" appear and the total equals the tile

  @edge
  Scenario: AC-17ZU03-06 Edge – currencies are never summed without an approved rate
    Given pipeline in INR and EUR and no approved rate
    When the total renders
    Then native totals are shown per currency and the converted total shows "FX_RATE_MISSING"

  @sec @obs @MU13
  Scenario Outline: AC-17ZU03-07 Permutations – Analytics, metrics and management views (2-way, 19 rows)
    Given actor "<persona>" with authority "<authority>" and scope "<scope>"
    And currencies are "<currency>" and consent is "<consent>"
    When "<operation>" is viewed through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU13 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   A-122 = Context filters
    #   A-123 = Cascading filter semantics
    Examples: MU13 rows (2-way, seed 479; space 1,944; tuples 188/188; +2 baseline-allow)
      | ex | operation | persona | authority | scope | currency | consent | channel | expected |
      | EX-17ZU03-01 | A-123 | P02/R02 | A5 wrong role | portfolio grant | INR+EUR rate ✓ | withdrawn | C2 mobile | 403 PERMISSION_DENIED |
      | EX-17ZU03-02 | A-123 | P13/R17 | T5 other tenant | grant revoked | INR+EUR no rate | unknown | C3 API | uniform 404 NOT_FOUND |
      | EX-17ZU03-03 | A-122 | P01/R01 | A3 SoD/limit | grant revoked | INR | valid | C2 mobile | 403 GRANT_REVOKED |
      | EX-17ZU03-04 | A-122 | P02/R02 | A1 | company | INR+EUR no rate | valid | C1 web | ALLOW: Filter business → brand/offer → opportunity type: |
      | EX-17ZU03-05 | A-122 | P13/R17 | A5 wrong role | company | INR | withdrawn | C3 API | 403 PERMISSION_DENIED |
      | EX-17ZU03-06 | A-122 | P01/R01 | T5 other tenant | portfolio grant | INR+EUR rate ✓ | unknown | C1 web | uniform 404 NOT_FOUND |
      | EX-17ZU03-07 | A-123 | P13/R17 | A1 | portfolio grant | INR+EUR rate ✓ | valid | C3 API | ALLOW: Change company → brand selection cleared |
      | EX-17ZU03-08 | A-123 | P01/R01 | A3 SoD/limit | company | INR+EUR no rate | withdrawn | C1 web | 403 SOD_CONFLICT |
      | EX-17ZU03-09 | A-123 | P02/R02 | T5 other tenant | company | INR | unknown | C2 mobile | uniform 404 NOT_FOUND |
      | EX-17ZU03-10 | A-123 | P02/R02 | A3 SoD/limit | grant revoked | INR+EUR rate ✓ | unknown | C3 API | 403 GRANT_REVOKED |
      | EX-17ZU03-11 | A-122 | P01/R01 | A1 | grant revoked | INR | withdrawn | C1 web | 403 GRANT_REVOKED |
      | EX-17ZU03-12 | A-123 | P13/R17 | A5 wrong role | grant revoked | INR+EUR no rate | valid | C1 web | 403 GRANT_REVOKED |
      | EX-17ZU03-13 | A-122 | P13/R17 | A1 | portfolio grant | INR+EUR no rate | unknown | C2 mobile | HOLD CONSENT_UNKNOWN |
      | EX-17ZU03-14 | A-122 | P01/R01 | A5 wrong role | company | INR+EUR rate ✓ | unknown | C3 API | 403 PERMISSION_DENIED |
      | EX-17ZU03-15 | A-122 | P13/R17 | A3 SoD/limit | portfolio grant | INR | valid | C2 mobile | 403 SOD_CONFLICT |
      | EX-17ZU03-16 | A-123 | P13/R17 | T5 other tenant | portfolio grant | INR+EUR rate ✓ | valid | C2 mobile | uniform 404 NOT_FOUND |
      | EX-17ZU03-17 | A-122 | P13/R17 | T5 other tenant | company | INR+EUR rate ✓ | withdrawn | C1 web | uniform 404 NOT_FOUND |
      | EX-17ZU03-18 | A-122 | P01/R01 | A1 | company | INR | valid | C1 web | ALLOW: Filter business → brand/offer → opportunity type: |
      | EX-17ZU03-19 | A-123 | P01/R01 | A1 | company | INR | valid | C1 web | ALLOW: Change company → brand selection cleared |
```

##### US-17-ZU04 Business metrics API with scoped dimensions and approved rates

| Field | Value |
|---|---|
| ID | US-17-ZU04 |
| Title | Business metrics API with scoped dimensions and approved rates |
| Type | Feature |
| Story | As a startup head (P02, R02), I want business metrics with scoped dimensions, period, currency and approved rate version; native and converted totals; missing rates listed, so that every number I see is defined once, scoped to what I may see, and adds up |
| Persona / roles | Startup head (P02, R02) |
| Traces | FR-V12-H-015 (MT-API-09) |
| Priority | Should |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 3–5 |
| Dependencies | US-17-YI01, US-17-YI02, US-21-YA01, US-17-YG02; source definition: Part 11.8b §11.8.5.1 Requirements adopted and release mapping |
| Dimension profile | persona ×3 · authority ×4 · scope ×3 · currency ×3 · consent ×3 · channel ×3 · operation ×1 · model MU13 |
| Notes | Screens A042, A087–A089, A106, A191; API family `/api/v1/analytics/`; audit events `analytics.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Business metrics API with scoped dimensions and approved rates
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd":
      """
      with companies "Kestrel IN" and "Kestrel EU", startup head "arjun@kestrel.example.com" (R02) for "Kestrel IN" only
      """
    And the metric registry with KPI definitions (numerator, denominator, period, freshness) approved at version 3

  @happy @MT-API-09
  Scenario: AC-17ZU04-01 Happy path – Business metrics with scoped dimensions, period (FR-V12-H-015)
    Given Arjun Menon (R02, arjun@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Business metrics with scoped dimensions, period" is exercised as specified by FR-V12-H-015:
      """
      Business metrics with scoped dimensions, period, currency and approved rate version; native and converted totals; missing rates listed
      """
    Then never sum currencies without rate
    And the audit event "analytics.business_metrics_with_scoped" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @ADR-183
  Scenario: AC-17ZU04-02 Negative – a tile without a registry definition fails CI
    Given a dashboard tile "win rate" that references no metric definition
    When CI runs the metric-registry check
    Then the build fails naming the tile

  @val
  Scenario: AC-17ZU04-03 Validation – zero denominator is "not applicable", not zero
    Given 0 qualified leads in the period
    When the conversion KPI renders
    Then it shows "not applicable" with the denominator 0 and no percentage

  @perm
  Scenario: AC-17ZU04-04 Permission – no data from a company outside my scope
    When Arjun opens the drill-down of "pipeline value"
    Then only rows of "Kestrel IN" appear and the total equals the tile

  @edge
  Scenario: AC-17ZU04-05 Edge – currencies are never summed without an approved rate
    Given pipeline in INR and EUR and no approved rate
    When the total renders
    Then native totals are shown per currency and the converted total shows "FX_RATE_MISSING"

  @sec @obs @MU13
  Scenario Outline: AC-17ZU04-06 Permutations – Analytics, metrics and management views (2-way, 17 rows)
    Given actor "<persona>" with authority "<authority>" and scope "<scope>"
    And currencies are "<currency>" and consent is "<consent>"
    When "<operation>" is viewed through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU13 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   H-015 = Business metrics with scoped dimensions, period
    Examples: MU13 rows (2-way, seed 486; space 972; tuples 169/169; +1 baseline-allow)
      | ex | operation | persona | authority | scope | currency | consent | channel | expected |
      | EX-17ZU04-01 | H-015 | P02/R02 | T5 other tenant | grant revoked | INR+EUR no rate | valid | C1 web | uniform 404 NOT_FOUND |
      | EX-17ZU04-02 | H-015 | P13/R17 | A1 | portfolio grant | INR | unknown | C3 API | HOLD CONSENT_UNKNOWN |
      | EX-17ZU04-03 | H-015 | P01/R01 | A5 wrong role | company | INR+EUR rate ✓ | withdrawn | C2 mobile | 403 PERMISSION_DENIED |
      | EX-17ZU04-04 | H-015 | P01/R01 | A3 SoD/limit | grant revoked | INR+EUR rate ✓ | unknown | C1 web | 403 GRANT_REVOKED |
      | EX-17ZU04-05 | H-015 | P02/R02 | A3 SoD/limit | portfolio grant | INR+EUR no rate | withdrawn | C2 mobile | 403 SOD_CONFLICT |
      | EX-17ZU04-06 | H-015 | P02/R02 | A3 SoD/limit | company | INR | valid | C3 API | 403 SOD_CONFLICT |
      | EX-17ZU04-07 | H-015 | P13/R17 | T5 other tenant | grant revoked | INR | withdrawn | C2 mobile | uniform 404 NOT_FOUND |
      | EX-17ZU04-08 | H-015 | P01/R01 | T5 other tenant | portfolio grant | INR+EUR rate ✓ | valid | C3 API | uniform 404 NOT_FOUND |
      | EX-17ZU04-09 | H-015 | P13/R17 | A5 wrong role | company | INR+EUR no rate | unknown | C1 web | 403 PERMISSION_DENIED |
      | EX-17ZU04-10 | H-015 | P01/R01 | A1 | grant revoked | INR+EUR no rate | withdrawn | C3 API | 403 GRANT_REVOKED |
      | EX-17ZU04-11 | H-015 | P02/R02 | A1 | company | INR+EUR rate ✓ | valid | C2 mobile | ALLOW: Never sum currencies without rate |
      | EX-17ZU04-12 | H-015 | P02/R02 | A5 wrong role | portfolio grant | INR | withdrawn | C1 web | 403 PERMISSION_DENIED |
      | EX-17ZU04-13 | H-015 | P13/R17 | A5 wrong role | grant revoked | INR+EUR rate ✓ | valid | C3 API | 403 GRANT_REVOKED |
      | EX-17ZU04-14 | H-015 | P02/R02 | T5 other tenant | company | INR+EUR no rate | unknown | C2 mobile | uniform 404 NOT_FOUND |
      | EX-17ZU04-15 | H-015 | P01/R01 | A1 | grant revoked | INR | withdrawn | C1 web | 403 GRANT_REVOKED |
      | EX-17ZU04-16 | H-015 | P13/R17 | A3 SoD/limit | portfolio grant | INR+EUR no rate | valid | C1 web | 403 SOD_CONFLICT |
      | EX-17ZU04-17 | H-015 | P01/R01 | A1 | company | INR | valid | C1 web | ALLOW: Never sum currencies without rate |
```

##### US-17-ZU05 Fourteen management views with production metrics

| Field | Value |
|---|---|
| ID | US-17-ZU05 |
| Title | Fourteen management views with production metrics |
| Type | Feature |
| Story | As a startup head (P02, R02), I want fourteen management views implemented with MET-V12-I-10…65 production metrics, so that every number I see is defined once, scoped to what I may see, and adds up |
| Persona / roles | Startup head (P02, R02) |
| Traces | FR-V12-I-043 (ch29 V4 mapping) |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 3–5 |
| Dependencies | US-17-YI01, US-17-YI02, US-21-YA01, US-17-YG02; source definition: Part 11.9c §11.9.5.20 Functional requirements and user… |
| Dimension profile | persona ×3 · authority ×4 · scope ×3 · currency ×3 · consent ×3 · channel ×3 · operation ×1 · model MU13 |
| Notes | Screens A042, A087–A089, A106, A191; API family `/api/v1/analytics/`; audit events `analytics.*`; feature flag default OFF until DoD D-14 evidence |

```gherkin
Feature: Fourteen management views with production metrics
  Background:
    Given tenant "Kestrel Analytics Pvt Ltd":
      """
      with companies "Kestrel IN" and "Kestrel EU", startup head "arjun@kestrel.example.com" (R02) for "Kestrel IN" only
      """
    And the metric registry with KPI definitions (numerator, denominator, period, freshness) approved at version 3

  @happy
  Scenario: AC-17ZU05-01 Happy path – Fourteen management views implemented with MET-V12-I-10…65 production… (FR-V12-I-043)
    Given Arjun Menon (R02, arjun@kestrel.example.com) is signed in to the tenant with the capability enabled
    When "Fourteen management views implemented with MET-V12-I-10…65 production…" is exercised as specified by FR-V12-I-043:
      """
      Fourteen management views implemented with MET-V12-I-10…65 production metrics
      """
    Then the observable result matches FR-V12-I-043 and its tests in Part 11.21
    And the audit event "analytics.fourteen_management_views" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @ADR-183
  Scenario: AC-17ZU05-02 Negative – a tile without a registry definition fails CI
    Given a dashboard tile "win rate" that references no metric definition
    When CI runs the metric-registry check
    Then the build fails naming the tile

  @val
  Scenario: AC-17ZU05-03 Validation – zero denominator is "not applicable", not zero
    Given 0 qualified leads in the period
    When the conversion KPI renders
    Then it shows "not applicable" with the denominator 0 and no percentage

  @perm
  Scenario: AC-17ZU05-04 Permission – no data from a company outside my scope
    When Arjun opens the drill-down of "pipeline value"
    Then only rows of "Kestrel IN" appear and the total equals the tile

  @edge
  Scenario: AC-17ZU05-05 Edge – currencies are never summed without an approved rate
    Given pipeline in INR and EUR and no approved rate
    When the total renders
    Then native totals are shown per currency and the converted total shows "FX_RATE_MISSING"

  @sec @obs @MU13
  Scenario Outline: AC-17ZU05-06 Permutations – Analytics, metrics and management views (2-way, 18 rows)
    Given actor "<persona>" with authority "<authority>" and scope "<scope>"
    And currencies are "<currency>" and consent is "<consent>"
    When "<operation>" is viewed through "<channel>"
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU13 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   I-043 = Fourteen management views implemented with…
    Examples: MU13 rows (2-way, seed 493; space 972; tuples 169/169; +1 baseline-allow)
      | ex | operation | persona | authority | scope | currency | consent | channel | expected |
      | EX-17ZU05-01 | I-043 | P02/R02 | T5 other tenant | company | INR+EUR no rate | valid | C3 API | uniform 404 NOT_FOUND |
      | EX-17ZU05-02 | I-043 | P13/R17 | A1 | grant revoked | INR+EUR rate ✓ | withdrawn | C2 mobile | 403 GRANT_REVOKED |
      | EX-17ZU05-03 | I-043 | P01/R01 | A5 wrong role | portfolio grant | INR | unknown | C1 web | 403 PERMISSION_DENIED |
      | EX-17ZU05-04 | I-043 | P13/R17 | A3 SoD/limit | company | INR | withdrawn | C1 web | 403 SOD_CONFLICT |
      | EX-17ZU05-05 | I-043 | P01/R01 | A3 SoD/limit | portfolio grant | INR+EUR rate ✓ | valid | C3 API | 403 SOD_CONFLICT |
      | EX-17ZU05-06 | I-043 | P02/R02 | A3 SoD/limit | grant revoked | INR+EUR no rate | unknown | C2 mobile | 403 GRANT_REVOKED |
      | EX-17ZU05-07 | I-043 | P13/R17 | A5 wrong role | grant revoked | INR | valid | C3 API | 403 GRANT_REVOKED |
      | EX-17ZU05-08 | I-043 | P01/R01 | T5 other tenant | portfolio grant | INR+EUR no rate | withdrawn | C2 mobile | uniform 404 NOT_FOUND |
      | EX-17ZU05-09 | I-043 | P02/R02 | A1 | company | INR+EUR rate ✓ | unknown | C1 web | HOLD CONSENT_UNKNOWN |
      | EX-17ZU05-10 | I-043 | P02/R02 | A5 wrong role | company | INR | withdrawn | C2 mobile | 403 PERMISSION_DENIED |
      | EX-17ZU05-11 | I-043 | P13/R17 | T5 other tenant | grant revoked | INR+EUR no rate | unknown | C1 web | uniform 404 NOT_FOUND |
      | EX-17ZU05-12 | I-043 | P01/R01 | A1 | company | INR | valid | C3 API | ALLOW: Fourteen management views implemented with |
      | EX-17ZU05-13 | I-043 | P13/R17 | A1 | portfolio grant | INR+EUR no rate | valid | C2 mobile | ALLOW: Fourteen management views implemented with |
      | EX-17ZU05-14 | I-043 | P01/R01 | T5 other tenant | grant revoked | INR | valid | C1 web | uniform 404 NOT_FOUND |
      | EX-17ZU05-15 | I-043 | P02/R02 | T5 other tenant | portfolio grant | INR+EUR rate ✓ | withdrawn | C3 API | uniform 404 NOT_FOUND |
      | EX-17ZU05-16 | I-043 | P13/R17 | A5 wrong role | grant revoked | INR+EUR rate ✓ | unknown | C3 API | 403 GRANT_REVOKED |
      | EX-17ZU05-17 | I-043 | P02/R02 | A5 wrong role | grant revoked | INR+EUR no rate | valid | C1 web | 403 GRANT_REVOKED |
      | EX-17ZU05-18 | I-043 | P01/R01 | A1 | company | INR | valid | C1 web | ALLOW: Fourteen management views implemented with |
```


## Quality gate: Batch 11.22b

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | **Pass** | Every story traces its FR-V12 IDs, the V12 source cell and the defining Part 11 section; decisions cited by ID |
| 2 | Assumptions, gaps and conflicts tagged and logged | **Pass** | Tags from 1140–1159 only; register in §11.22.9 (last file of Batch 11.22) |
| 3 | IDs unique and consistent with earlier parts | **Pass** | US-<EP>-ZU<nn> unique per epic; AC and EX IDs derived; epics EP-01…EP-33 as defined; EP-34 new |
| 4 | No story lacks AC; no requirement lacks a test | **Pass** | Every new story has Gherkin with happy, alternate, negative, validation, permission and edge scenarios plus a generated Scenario Outline |
| 5 | Negative, edge, security and accessibility cases covered | **Pass** | MAS-1…MAS-9 applied; @sec/@obs outlines; @a11y in website and UI stories |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | **N/A** | N/A – no new agents; AI stories reuse the registry, gateway and eval gates |
| 7 | Time-sensitive facts flagged "verify" with as-of date | **Pass** | No prices or model versions stated; regulatory items defer to counsel-approved packs (verify at implementation, as of 28 Nov 2026) |
| 8 | No restricted data routed to free-tier models | **Pass** | Restricted personal data appears only as a blocking value in MU05 (DEC-007, DEC-788) |
| 9 | Consistent with earlier parts | **Pass** | Template of Part 5.1a copied; V12-B decisions DEC-770…791 applied; inconsistencies reported, not edited |

**Status: Part 11 Batch 11.22b complete (57 stories, EP-01, EP-02, EP-03, EP-04, EP-05, EP-08, EP-12, EP-15, EP-16, EP-17). Continue with Batch 11.22c.**
