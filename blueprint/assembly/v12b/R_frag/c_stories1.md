# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.19c), Platform Decisions Implementation: Epics, User Stories with Permutations, Combinatorial Test Design, Test Cases, Conflicts, Decisions, Tags and Quality Gate

| Field | Value |
|---|---|
| Document | Part 11.19c: epic cards and 29 user stories (Part 5.1a/b template, Scenario Outline + Examples from the combinatorial models), the test strategy delta and the combinatorial test design (13 parameter models, pairwise, 3-way and exhaustive), 13 + 8 test scenarios, 86 full-form test cases and 1,072 generated test cases (Part 6.2a template), conflicts, decisions DEC-880…899, persona review, tags register and quality gate for Part 11.19 |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Parts 11.19a/b; Part 5.1a §5.6–5.7 (dimension matrix and conventions); Part 6.1 (strategy), Part 6.2a §6.2.1 (conventions, profiles PP-01…07); Part 6.4 (AI evaluation) |
| Roles applied | Product Owner · Business Systems Analyst · QA Lead · Identity architect · Developer-platform lead · Integration architect · Privacy and cloud-security lead · DBRE · LLM platform lead · Privacy-preserving analytics scientist |

---

### 11.19.5.14 Epics and user stories

**Conventions (Part 5.1a §5.7 applied).** Story ID `US-<EP>-ZR<nn>` (nn unique across this part); AC ID `AC-<EP>ZR<nn>-<seq>`; Gherkin tag lines `@happy @alt @neg @val @perm @edge @sec @a11y @obs` plus rule/decision tags; denials assert status, error code, NSE and the denial audit event. Every story with a parameter model carries a **Scenario Outline** whose `Examples:` rows are generated from that model by `assembly/v12b/R_02_combinatorics.py` (first 12 rows shown in the story; all rows are test cases in §11.19.5.17). Points are Fibonacci ranges ≤ 13; person-days per Part 5.1a §5.5.1 (central 0.7 pd per SP is used by Part 5; this part's costing uses the work-package estimate of Part 11.19b §11.19.5.13).

#### 11.19.5.14.1 Epic placement

No new epic is needed: each capability belongs to an existing epic's domain (Part 0 §0.10.2; EP-22/EP-23 from Part 11.2a).

| Epic | Title (baseline) | P4 scope added | Stories | SP range |
|---|---|---|---|---|
| EP-01 | Platform foundation, identity reuse and tenancy | C1 identity (SSO, SCIM, roles, SoD, recertification), C8 database roles, residency routing | US-01-ZR01…05, ZR26…28 | 38–63 |
| EP-04 | AI gateway, cost control and AI quality | C6 model registry | US-04-ZR20…23 | 18–31 |
| EP-07 | CRM, lead capture and Customer 360 | C3 CRM connectors | US-07-ZR12, ZR13 | 13–21 |
| EP-17 | Dashboards, forecast and Command Centre | C7 benchmarks | US-17-ZR24, ZR25 | 10–16 |
| EP-18 | Workflow, autonomy and automation engine | C3 connector framework and gate | US-18-ZR11 | 5–8 |
| EP-20 | SaaS client lifecycle and portability | C2 developer platform | US-20-ZR06…10 | 26–42 |
| EP-21 | Release readiness, QA and observability | C4 Vercel path, C5 RPO, automations | US-21-ZR16…19, ZR29 | 23–37 |
| EP-22 | Voice and intelligent telephony | C3 voice transport | US-22-ZR15 | 5–8 |
| EP-23 | SMS, RCS and business messaging | C3 SMS-DLT | US-23-ZR14 | 5–8 |
| **Total** | | | **29 stories** | **143–234 SP** |

#### 11.19.5.14.2 Epic card: P4 platform decisions (cross-epic view)

| Field | Value |
|---|---|
| ID | P4 slice of EP-01, EP-04, EP-07, EP-17, EP-18, EP-20, EP-21, EP-22, EP-23 |
| Title | Platform decisions: enterprise identity, developer platform and connectors, regional data path, recovery, model registry, benchmarks, database access |
| Business value | Enterprise buyers can adopt the platform with their IdP and provisioning (DEC-784); developers and existing CRMs integrate without custom work (DEC-785); personal data stays in the customer's residency zone on every hop (DEC-772/786); data loss is bounded to 15 minutes and growth work recovers in 2 hours (DEC-771/787); any AI provider can be adopted by evidence, with Claude Sonnet as the approved primary (DEC-788); tenants gain peer benchmarks without exposing their data (DEC-789); and the database cannot be read across tenants by the application (DEC-778) |
| Linked BRs | BR-V12-05 (ecosystem), BR-V7-AI-05 (private customer data), BR-M01, BR-M05, BR-S119…S126 (security), BR-TENANT |
| Linked FRs | FR-V12-R-001…155 |
| Linked NFRs | NFR-001…006, NFR-015…018, NFR-027, NFR-029, NFR-031, NFR-032, NFR-037; KPI-18, KPI-19, KPI-32 |
| Key rules and decisions | DEC-772, 778, 784…789; DEC-880…899; ENT-IDN-01…06, ENT-ACC-01…05, ENT-API-01…07, ENT-DAT-03…05, ENT-INT-01…05; MDL-R0…G1; AIX-02/03/20; BRL-TEN-01…12; ABAC-03, ABAC-11 |
| In scope | Everything in Part 11.19a/b §11.19.5.1–§11.19.5.9 |
| Out of scope | AI voice agent behaviour (Part 11.18); mandate engine (Part 11.17); jurisdiction pack wording (Part 11.15); calendar dates (Part 11.20) |
| Dependencies | DP-01 identity service (broker); Supabase PITR availability; Vercel plan features; provider developer accounts; counsel sign-off for packs |
| Priority | Must (C7 Must for Release 2) |
| Wave(s) | Release 1 (W0–W3 equivalent sprints S0–S7), C7 in Release 2 |
| Size | 29 stories · **143–234 SP** · work-package estimate 183 / 269 / 382 pd gross (Part 11.19b) |

#### 11.19.5.14.3 Stories

##### US-01-ZR01 Tenant SSO connection with SAML 2.0 and OIDC through the broker

| Field | Value |
|---|---|
| ID | US-01-ZR01 |
| Title | Tenant SSO connection with SAML 2.0 and OIDC through the broker |
| Type | Feature |
| Story | As a tenant administrator (P11, R12), I want to configure SAML 2.0 or OIDC sign-in with our IdP (Okta, Entra ID, Google Workspace or any conformant IdP), test it and activate it, so that our staff sign in with corporate credentials and leave access when they leave |
| Persona / roles | P11 (R12); P02, P03 (R02, R03 as signing-in users); P13 (R17) for external tenants |
| Traces | FR-V12-R-001…005, 028, 029; ENT-IDN-01; DEC-784, DEC-880; ADR-255 |
| Priority | Must |
| Wave | Release 1 (S2) |
| Points | 8–13 |
| Dependencies | Identity spike check 13 (S0); DDL-V12-R-01 |
| Dimension profile | A1,A2,A5 · S1–S3 · D1–D5 · C1,C3 · T(owned startup, external tenant IN, external tenant EU) · I1,I3 · La |
| Notes | IdP simulators replay vendor-specific payloads; certificate and metadata handling by AU-290 |

```gherkin
Feature: Tenant SSO connection with SAML 2.0 and OIDC through the broker
  Background:
    Given tenant "Kestrel Analytics" in zone IN with administrator "meera@kestrel.example.com" (R12) holding a fresh WebAuthn factor
    And the reused IdP broker is reachable and the IdP simulator "okta-sim" publishes signed metadata

  @happy @DEC-784
  Scenario: AC-01ZR01-01 Happy path – create, test and activate a SAML connection
    When Meera creates a connection with vendor "okta", protocol "SAML 2.0" and metadata URL "https://okta-sim.test/app/kestrel/sso/saml/metadata"
    And she runs a test login that returns a valid signed assertion for "ravi@kestrel.example.com"
    And she activates the connection
    Then the connection state is "active" with last_test_ok_at set and event "identity.sso_config.activated" is written in zone IN

  @val @ENT-IDN-01
  Scenario: AC-01ZR01-02 Validation – http metadata URL is rejected
    When Meera submits metadata URL "http://okta-sim.test/metadata"
    Then the API returns 422 "METADATA_URL_NOT_HTTPS" and no connection row exists

  @neg @sec @ENT-IDN-01
  Scenario: AC-01ZR01-03 Negative – assertion for another audience is rejected
    Given the connection is active
    When the IdP simulator returns an assertion with Audience "https://other-sp.test"
    Then sign-in fails with 401 "SSO_AUDIENCE_MISMATCH", no session cookie is set and an audit event with outcome "denied" is written

  @edge
  Scenario: AC-01ZR01-04 Edge – activation without a successful test login
    Given a connection in state "testing" with no successful test
    When Meera activates it
    Then the API returns 409 "TEST_LOGIN_REQUIRED" and the state stays "testing"

  @perm
  Scenario: AC-01ZR01-05 Permission – a startup head cannot create connections
    When "arjun@kestrel.example.com" (R02) posts a new connection
    Then the API returns 403 and NSE

  @sec @obs
  Scenario Outline: AC-01ZR01-06 Sign-in outcome across IdP, protocol, role, region, domain, enforcement, MFA and assertion
    Given an IdP connection for <idp> using <protocol> in zone <region> with domain state "<domain>" and enforcement <enforcement>
    And the user holds role "<role>" and the IdP asserts MFA "<mfa>"
    When the IdP returns a "<assertion>" response
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M01}}
```

##### US-01-ZR02 Verified domains, enforcement, break-glass, MFA and session policy

| Field | Value |
|---|---|
| ID | US-01-ZR02 |
| Title | Verified domains, enforcement, break-glass, MFA and session policy |
| Type | Security |
| Story | As a tenant administrator (P11, R12), I want to verify our email domains, keep a break-glass account and set MFA and session policy before enforcing SSO, so that nobody bypasses the IdP and we can never lock ourselves out |
| Persona / roles | P11 (R12); P09 (R10) as second approver; P01 (R01) for owned startups |
| Traces | FR-V12-R-006…010, 030; ENT-IDN-02, 04, 05, 06; SEC-03; DEC-077; ABAC-11 |
| Priority | Must |
| Wave | Release 1 (S3) |
| Points | 5–8 |
| Dependencies | US-01-ZR01 |
| Dimension profile | A1,A2,A5 · S1–S4 · D1–D4 · C1,C3 · T(IN, EU) · I1,I3 · La |
| Notes | Platform floor: privileged roles need phishing-resistant factors (DEC-077) |

```gherkin
Feature: Verified domains, enforcement, break-glass, MFA and session policy
  Background:
    Given tenant "Kestrel Analytics" (IN) with an active SAML connection and administrator "meera@kestrel.example.com" (R12)

  @happy @ENT-IDN-02
  Scenario: AC-01ZR02-01 Happy path – verify domain, add break-glass, enforce
    Given the DNS TXT record "growth-verify=7Qm2v" exists for "kestrel.example.com"
    And break-glass account "bg1@kestrel.example.com" has a registered hardware key
    When Meera verifies the domain and requests enforcement and "dpo@kestrel.example.com" (R10) approves
    Then the connection is enforced and local sign-in for "@kestrel.example.com" users returns 403 "SSO_ENFORCED"

  @neg @ENT-IDN-06
  Scenario: AC-01ZR02-02 Negative – enforcement blocked without break-glass
    Given the domain is verified and no break-glass account exists
    When Meera requests enforcement
    Then the API returns 409 "SSO_ENFORCEMENT_REQUIRES_BREAKGLASS" and a direct UPDATE by app_rw raises the same error from the trigger

  @edge @ENT-IDN-02
  Scenario: AC-01ZR02-03 Edge – TXT record missing twice does not lock users out
    Given the connection is enforced
    When AU-290 finds the TXT record missing at 2027-02-01T02:00:00+05:30 and 2027-02-02T02:00:00+05:30
    Then the domain state is "verification_lost", Meera receives a High notification and enforced sign-in continues to work

  @sec @ENT-IDN-06
  Scenario: AC-01ZR02-04 Security – break-glass use raises SEV3
    When "bg1@kestrel.example.com" signs in with the hardware key
    Then a SEV3 security event is raised and every R12 and R10 of the tenant is notified within 5 minutes

  @val @ENT-IDN-05
  Scenario Outline: AC-01ZR02-05 Validation – session policy boundaries
    When Meera sets max_session_hours to <max> and idle_minutes to <idle>
    Then the result is <result>
    Examples:
      | max | idle | result |
      | 0   | 30   | 422 OUT_OF_RANGE |
      | 1   | 5    | 200 |
      | 24  | 120  | 200 for non-privileged roles; privileged sessions capped at 12 h / 30 min |
      | 25  | 30   | 422 OUT_OF_RANGE |
      | 12  | 4    | 422 OUT_OF_RANGE |
      | 12  | 121  | 422 OUT_OF_RANGE |

  @perm @ABAC-11
  Scenario: AC-01ZR02-06 Permission – MFA mode cannot go below the platform floor
    When Meera tries to set privileged_factor to "any"
    Then the API returns 422 "BELOW_PLATFORM_FLOOR" and the policy version is unchanged
```

##### US-01-ZR03 SCIM 2.0 provisioning and de-provisioning in Release 1

| Field | Value |
|---|---|
| ID | US-01-ZR03 |
| Title | SCIM 2.0 provisioning and de-provisioning in Release 1 |
| Type | Feature |
| Story | As a tenant administrator (P11, R12), I want our IdP to create, update and remove users and groups through SCIM, so that joiners get the right access and leavers lose every session and key within 15 minutes |
| Persona / roles | P11 (R12); P16 (R19 SCIM client identity) |
| Traces | FR-V12-R-011…016, 030; ENT-IDN-03; DEC-881; ADR-256; RFC 7643/7644 |
| Priority | Must |
| Wave | Release 1 (S4) |
| Points | 8–13 |
| Dependencies | US-01-ZR01, US-01-ZR04 (group mappings to roles) |
| Dimension profile | A1,A5,A8 · S1–S4 · D1–D5 · C3 · T(IN, EU) · I1–I3 · n/a locale |
| Notes | De-provisioning SLA measured by AU-291 |

```gherkin
Feature: SCIM 2.0 provisioning and de-provisioning in Release 1
  Background:
    Given tenant "Kestrel Analytics" (IN) has SCIM enabled with token prefix "scim_in_8f2a" and group "Sales-India" mapped to role R03 (approved)

  @happy @DEC-881
  Scenario: AC-01ZR03-01 Happy path – create user then add to a mapped group
    When the IdP posts a SCIM User with userName "lata@kestrel.example.com" and externalId "00u9x"
    And patches group "Sales-India" to add her
    Then the membership is "provisioned" with role R03 and events "identity.scim.user_provisioned" and "identity.scim.group_changed" are written

  @happy @sec
  Scenario: AC-01ZR03-02 De-provisioning revokes access within 60 seconds
    Given Lata has 2 open sessions and 1 API key
    When the IdP patches her User with active=false at 2027-02-03T10:00:00+05:30
    Then before 2027-02-03T10:01:00+05:30 both sessions are revoked, the key returns 401 "API_KEY_REVOKED" and her pending approvals are re-queued to R12

  @neg @sec
  Scenario: AC-01ZR03-03 Negative – unmapped group grants nothing
    When the IdP adds Lata to group "All-Staff" that has no approved mapping
    Then the group membership is stored, no role is granted and R12 gets the task "Map group"

  @neg
  Scenario: AC-01ZR03-04 Negative – break-glass accounts are not SCIM-managed
    When the IdP sends DELETE for the break-glass user
    Then the response is 409 with scimType "mutability" and the account is unchanged

  @edge @obs
  Scenario: AC-01ZR03-05 Edge – SLA breach detection
    Given the IdP changed Lata at 2027-02-03T09:40:00+05:30 but the SCIM call arrived at 09:58
    When AU-291 computes the SLA
    Then end_to_end_s is 1080, a SEV2 incident is opened and runbook RB-ID-04 is linked

  @sec @perm
  Scenario Outline: AC-01ZR03-06 SCIM behaviour across IdP, operation, user state, mapping, token and endpoint
    Given SCIM client <idp> with token "<token>" calls the <endpoint>
    And the target user is "<user>" and the group mapping is "<mapping>"
    When it sends "<op>"
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M02}}
```

##### US-01-ZR04 Custom roles and separation of duties

| Field | Value |
|---|---|
| ID | US-01-ZR04 |
| Title | Custom roles and separation of duties |
| Type | Security |
| Story | As a tenant administrator (P11, R12), I want to build roles from resource × action permissions with separation of duties enforced everywhere, so that we match our org chart without letting anyone request and approve the same thing |
| Persona / roles | P11 (R12); P09 (R10) co-approver for consequential permissions; P01 (R01) |
| Traces | FR-V12-R-017…022; ENT-ACC-01/02; C2-T1; DEC-881, DEC-898; ABAC-03 |
| Priority | Must |
| Wave | Release 1 (S5) |
| Points | 5–8 |
| Dependencies | Permission catalogue generator; DDL-V12-R-04 |
| Dimension profile | A1,A2,A5,A6 · S1–S3 · D1–D3 · C1,C3 · T(owned, external) · I n/a (no external dependency) · La |
| Notes | SoD matrix of record §11.19.5.1.F |

```gherkin
Feature: Custom roles and separation of duties
  Background:
    Given tenant "Kestrel Analytics" (IN) and administrator "meera@kestrel.example.com" (R12) holding all tenant permissions

  @happy
  Scenario: AC-01ZR04-01 Happy path – company-scoped custom role
    When Meera creates role "Regional Sales Lead" scoped to company "Kestrel South" with permissions "Leads:read, Leads:write, Deals:read"
    Then the role is saved, permissions_hash is stored and "access.role.created" is emitted

  @neg @DEC-898
  Scenario: AC-01ZR04-02 Negative – request and approve in one role
    When Meera creates role "Ops" with "Runs:create" and "Runs:approve"
    Then the API returns 422 "SOD_CONFLICT" naming both permissions and NSE

  @neg @sec @C2-T1
  Scenario: AC-01ZR04-03 Negative – direct database insert is blocked by the trigger
    Given role "Ops2" with "Runs:create" exists
    When app_rw inserts permission "Runs:approve" for "Ops2"
    Then PostgreSQL raises "separation of duties violation" and the transaction rolls back

  @perm
  Scenario: AC-01ZR04-04 Permission – cannot grant a permission you do not hold
    Given "lead@kestrel.example.com" holds a custom admin role without "Billing:approve"
    When she creates a role with "Billing:approve"
    Then the API returns 403 "PERMISSION_NOT_HELD"

  @sec @perm
  Scenario Outline: AC-01ZR04-05 SoD across permission pair, path, scope and actor
    Given actor "<actor>" works at scope "<scope>"
    When the pair "<pair>" is attempted through "<path>"
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M03}}
```

##### US-01-ZR05 SIEM streaming, audit export, JIT support and quarterly recertification

| Field | Value |
|---|---|
| ID | US-01-ZR05 |
| Title | SIEM streaming, audit export, JIT support and quarterly recertification |
| Type | Compliance |
| Story | As a compliance lead (P09, R10), I want identity and audit events streamed to our SIEM, exportable with chain verification, support access bound to tickets, and privileged access recertified quarterly, so that we can evidence access control to auditors (SOC 2, DEC-775) |
| Persona / roles | P09 (R10); P11 (R12); P12 (R13) support |
| Traces | FR-V12-R-023…026; ENT-ACC-03/04/05; DEC-898; AU-292 |
| Priority | Must |
| Wave | Release 1 (S6) |
| Points | 5–8 |
| Dependencies | US-01-ZR04 |
| Dimension profile | A1,A5,A7 · S1–S4 · D1–D3 · C1,C3 · T(IN, EU) · I1,I3 · La |
| Notes | Platform audit retention floor 7 years (DEC-028) |

```gherkin
Feature: SIEM streaming, audit export, JIT support and quarterly recertification
  Background:
    Given tenant "Kestrel Analytics" (IN) with compliance lead "dpo@kestrel.example.com" (R10)

  @happy
  Scenario: AC-01ZR05-01 SIEM sink receives a test event
    When R10 creates an https sink "https://siem.kestrel.example.com/ingest" with format "CEF" and retention 3 years and sends a test
    Then the test event is delivered with sequence number 1 and the sink state is "active"

  @val
  Scenario: AC-01ZR05-02 Non-TLS sink rejected
    When R10 creates a sink "syslog://10.0.0.5:514"
    Then the API returns 422 "NON_TLS_ENDPOINT"

  @happy @sec
  Scenario: AC-01ZR05-03 Audit export with chain verification
    When R10 exports audit events for 2027-01 as JSON Lines
    Then the manifest row count equals the filtered count and POST /audit/verify returns "valid"

  @neg @sec
  Scenario: AC-01ZR05-04 Support access needs a ticket and expires
    Given support user "s.k@platform.example.com" (R13) has a grant with ticket "SUP-4411" that expired at 2027-02-01T12:00:00+05:30
    When he reads a lead at 2027-02-01T12:05:00+05:30
    Then the API returns 403 and the tenant's support-session list shows the expired grant

  @edge @obs
  Scenario: AC-01ZR05-05 Recertification suspends unconfirmed privileged permissions
    Given campaign Q1-2027 opened 2027-01-05 with item "arjun R02 Startup Head"
    When no decision is recorded by 2027-01-19
    Then Arjun's privileged permissions are suspended, his account stays active, and R12 can reinstate in one action

  @neg
  Scenario: AC-01ZR05-06 Nobody recertifies themself
    When Meera decides her own recertification item
    Then the API returns 403 "SELF_REVIEW"
```

##### US-20-ZR06 Scoped, zone-bound API keys

| Field | Value |
|---|---|
| ID | US-20-ZR06 |
| Title | Scoped, zone-bound API keys |
| Type | Feature |
| Story | As a tenant developer acting for the tenant administrator (P13/P11, R17/R12), I want scoped, expiring API keys that work only in our residency zone and cannot trigger consequential actions, so that our systems integrate safely |
| Persona / roles | P11 (R12); P13 (R17); P16 (R19) |
| Traces | FR-V12-R-031…034, 038, 039, 052; ENT-API-01, 03; DEC-882, DEC-883 |
| Priority | Must |
| Wave | Release 1 (S1–S2) |
| Points | 5–8 |
| Dependencies | Developer host per zone |
| Dimension profile | A1,A5,A8 · S1–S4 · D1–D5 · C3 · T(IN, EU) · I1,I2 · n/a locale |
| Notes | Format `gek_<env>_<zone>_<prefix8>_<secret43>` |

```gherkin
Feature: Scoped, zone-bound API keys
  Background:
    Given tenant "Kestrel Analytics" (IN) and administrator "meera@kestrel.example.com" (R12) with step-up done

  @happy
  Scenario: AC-20ZR06-01 Create a key and see it once
    When Meera creates key "crm-bridge" with scopes "leads:read, leads:write" expiring 2027-05-01
    Then the response shows a key starting "gek_live_in_" once with Cache-Control "no-store" and the database holds only prefix, last4 and hash

  @neg @DEC-883
  Scenario: AC-20ZR06-02 Consequential scopes do not exist
    When Meera requests scope "send"
    Then the API returns 422 "SCOPE_NOT_GRANTABLE" and no key is created

  @neg @sec
  Scenario: AC-20ZR06-03 Revocation within 60 seconds
    Given key "crm-bridge" is revoked at 2027-02-04T09:00:00+05:30
    When it calls GET /api/v1/leads at 09:01:00
    Then the response is 401 "API_KEY_REVOKED"

  @val @edge
  Scenario: AC-20ZR06-04 Lifetime boundary
    When Meera sets expiry 366 days ahead
    Then the API returns 422 "LIFETIME_TOO_LONG"

  @sec @perm
  Scenario Outline: AC-20ZR06-05 Credential outcomes across credential, state, scope, region, host and rate
    Given a "<cred>" credential in state "<state>" with scope "<scope>"
    When it calls the "<host>" on the "<region>" at "<rate>"
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M04}}
```

##### US-20-ZR07 OAuth 2.0 client credentials

| Field | Value |
|---|---|
| ID | US-20-ZR07 |
| Title | OAuth 2.0 client credentials |
| Type | Feature |
| Story | As a tenant developer (P13, R17), I want OAuth client credentials with private_key_jwt so that our servers authenticate with short-lived tokens and no shared secret |
| Persona / roles | P13 (R17); P11 (R12) |
| Traces | FR-V12-R-035…037; ENT-API-02; DEC-882; RFC 6749, 7523, 7009 |
| Priority | Must |
| Wave | Release 1 (S2) |
| Points | 5–8 |
| Dependencies | US-20-ZR06 |
| Dimension profile | A1,A5 · S1–S4 · D1–D5 · C3 · T(IN, EU) · I1 · n/a locale |
| Notes | Access tokens 15 min, ES256 |

```gherkin
Feature: OAuth 2.0 client credentials
  Background:
    Given OAuth client "gec_7h2k9q0w1e3r5t6y8u0p" of tenant "Kestrel Analytics" (IN) with auth method "private_key_jwt" and scopes "leads:read"

  @happy
  Scenario: AC-20ZR07-01 Token from a signed client assertion
    When the client posts a client assertion with aud "https://api.in.platform.example.com/oauth/token", jti "a1" and exp 60 s ahead
    Then a Bearer token valid for 15 minutes with scope "leads:read" and aud "api.in" is returned

  @neg @sec
  Scenario: AC-20ZR07-02 Replayed jti rejected
    When the same assertion with jti "a1" is posted again
    Then the response is 400 "invalid_client" and no token is issued

  @neg
  Scenario: AC-20ZR07-03 Scope outside registration
    When the client asks for scope "leads:write"
    Then the response is 400 "invalid_scope"

  @edge
  Scenario: AC-20ZR07-04 Assertion expiry too far ahead
    When exp is 300 s ahead
    Then the response is 400 "invalid_client"

  @happy
  Scenario: AC-20ZR07-05 Revocation
    When R12 revokes the token via /oauth/revoke
    Then the next API call with it returns 401
```

##### US-20-ZR08 Signed webhooks with delivery log and replay

| Field | Value |
|---|---|
| ID | US-20-ZR08 |
| Title | Signed webhooks with delivery log and replay |
| Type | Feature |
| Story | As a tenant developer (P13, R17), I want signed webhooks with retries, a delivery log and replay, so that our systems react to events reliably and can prove they came from the platform |
| Persona / roles | P13 (R17); P11 (R12) |
| Traces | FR-V12-R-041…047; ENT-API-05; ADR-258; AU-294 |
| Priority | Must |
| Wave | Release 1 (S3–S4) |
| Points | 8–13 |
| Dependencies | Outbox (US-0110) |
| Dimension profile | A1,A5 · S1–S4 · D1–D5 · C3 · T(IN, EU) · I1–I4 · n/a locale |
| Notes | Schedule 0, 5 m, 30 m, 2 h, 6 h, 15 h |

```gherkin
Feature: Signed webhooks with delivery log and replay
  Background:
    Given endpoint "https://hooks.kestrel.example.com/ge" of tenant "Kestrel Analytics" (IN) is verified and subscribed to "lead.created"

  @happy
  Scenario: AC-20ZR08-01 Delivery with signature
    When lead "L-1001" is created
    Then the endpoint receives a POST with headers GE-Signature, GE-Event-Id and GE-Delivery-Attempt 1 and the body contains lead_id and no contact fields

  @neg @sec
  Scenario: AC-20ZR08-02 SSRF target rejected
    When R12 registers "https://169.254.169.254/latest"
    Then the API returns 422 "URL_NOT_ALLOWED"

  @edge
  Scenario: AC-20ZR08-03 Exhaustion after attempt 6
    Given the endpoint returns 503 for every attempt
    Then attempts are made at about T, T+5 m, T+35 m, T+2 h 35 m, T+8 h 35 m and T+23 h 35 m and the delivery is "exhausted"

  @happy
  Scenario: AC-20ZR08-04 Replay from the log
    When R12 replays delivery D-55 within 30 days
    Then a new attempt is sent with the same event id and outcome "replayed"

  @sec
  Scenario Outline: AC-20ZR08-05 Delivery outcomes across event, response, attempt, endpoint state and region
    Given event "<event>" for an endpoint that is "<endpoint>" in zone <region>
    When attempt <attempt> receives "<response>"
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M05}}

  @sec
  Scenario Outline: AC-20ZR08-06 SDK signature verification (exhaustive)
    Given a delivery with timestamp "<timestamp>", signature "<signature>" and "<replay>"
    When the receiver calls verify()
    Then the outcome matches test case <tc>: "<expected>"
{{EX:M06}}
```

##### US-20-ZR09 Developer portal, versioning policy and sandbox with promotion

| Field | Value |
|---|---|
| ID | US-20-ZR09 |
| Title | Developer portal, versioning policy and sandbox with promotion |
| Type | Feature |
| Story | As a tenant developer (P13, R17), I want a portal with reference, guides and a sandbox with synthetic data, and a reviewed path to promote configuration to production, so that we build and test without touching real data |
| Persona / roles | P13 (R17); P11 (R12); P15 (R18) reading the public portal |
| Traces | FR-V12-R-040, 051, 053…055; ENT-API-04, 07; ENT-DAT-04/05; DEC-899 |
| Priority | Must |
| Wave | Release 1 (S5) |
| Points | 5–8 |
| Dependencies | US-20-ZR06 |
| Dimension profile | A1,A2,A5 · S1–S4 · D1–D4 · C1,C2,C3 · T(IN, EU) · I1 · La |
| Notes | Portal W47 meets WCAG 2.2 AA |

```gherkin
Feature: Developer portal, versioning policy and sandbox with promotion
  Background:
    Given tenant "Kestrel Analytics" (IN) with sandbox "kestrel-sbx-1" (synthetic dataset gse_syn 1.4.0)

  @happy
  Scenario: AC-20ZR09-01 Try-it hits only the sandbox
    When a visitor uses Try-it on "GET /api/v1/leads" in the portal
    Then the request goes to the sandbox host and returns synthetic records

  @neg @sec
  Scenario: AC-20ZR09-02 Personal data cannot enter a sandbox
    When a developer imports a CSV with a real-looking phone number into the sandbox
    Then the import is rejected "SANDBOX_SYNTHETIC_ONLY"

  @perm
  Scenario: AC-20ZR09-03 Promotion needs another approver
    Given developer "dev@kestrel.example.com" requested promotion P-12
    When he approves P-12 himself
    Then the API returns 403 "SAME_APPROVER"

  @happy
  Scenario: AC-20ZR09-04 Deprecation headers
    Given operation "GET /api/v1/old-report" is deprecated with sunset 2028-03-01
    When a key calls it
    Then the response carries Deprecation and Sunset headers and a Link rel="deprecation"

  @a11y
  Scenario: AC-20ZR09-05 Portal accessibility
    When the portal is checked with axe and a screen reader pass
    Then there are 0 serious or critical violations and all code samples have accessible names
```

##### US-20-ZR10 SDKs for TypeScript, Python and Java

| Field | Value |
|---|---|
| ID | US-20-ZR10 |
| Title | SDKs for TypeScript, Python and Java |
| Type | Feature |
| Story | As a tenant developer (P13, R17), I want official SDKs in TypeScript, Python and Java with auth, pagination, retries and webhook verification, so that integration takes hours, not weeks |
| Persona / roles | P13 (R17) |
| Traces | FR-V12-R-048…050; ENT-API-06; DEC-882; RECOMMENDATION-1097 |
| Priority | Must |
| Wave | Release 1 (S4–S6) |
| Points | 5–8 |
| Dependencies | US-20-ZR06…08 |
| Dimension profile | A n/a (library) · S n/a · D1–D5 · C3 · T(IN, EU) · I1–I3 · n/a locale |
| Notes | Contract tests against the sandbox in CI |

```gherkin
Feature: SDKs for TypeScript, Python and Java
  @happy
  Scenario Outline: AC-20ZR10-01 Same contract behaviour in each language
    Given the <language> SDK version 1.0.0 configured with a sandbox key for zone <zone>
    When the contract suite runs list, create, paginate and verify-webhook
    Then all calls succeed against "https://api.<zone_host>.platform.example.com" and the results equal the reference fixtures
    Examples:
      | language   | zone | zone_host |
      | TypeScript | IN   | in        |
      | Python     | IN   | in        |
      | Java       | IN   | in        |
      | TypeScript | EU   | eu        |
      | Python     | EU   | eu        |
      | Java       | EU   | eu        |

  @edge
  Scenario: AC-20ZR10-02 Retry honours Retry-After
    Given the sandbox returns 429 with Retry-After 2
    When the SDK retries
    Then it waits at least 2 s and retries at most 3 times

  @sec
  Scenario: AC-20ZR10-03 Release provenance
    When release 1.0.0 is published
    Then npm, PyPI and Maven Central artefacts carry signatures/provenance that verify in CI
```
