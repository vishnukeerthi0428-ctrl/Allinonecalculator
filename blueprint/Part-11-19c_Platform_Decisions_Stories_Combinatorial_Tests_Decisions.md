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
    Examples: M01 generated rows (see TC-V12-R-101…)
      | idp | protocol | role | region | domain | enforcement | mfa | assertion | tc | expected |
      | Okta | SAML 2.0 | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | valid | TC-V12-R-101 | session created with `acr`/`amr` recorded |
      | Okta | SAML 2.0 | R02 startup head | EU | verification lost (TXT missing twice) | on | OTP (amr otp) | wrong audience | TC-V12-R-102 | 401 `SSO_AUDIENCE_MISMATCH` |
      | Okta | OIDC | R03 executive | EU | unverified | off | none | wrong issuer | TC-V12-R-103 | 401 `SSO_ISSUER_MISMATCH` |
      | Microsoft Entra ID | OIDC | R12 tenant admin | IN | verification lost (TXT missing twice) | on | none | expired (NotOnOrAfter + 60 s skew passed) | TC-V12-R-104 | 401 `SSO_ASSERTION_EXPIRED` |
      | Google Workspace | OIDC | R15 auditor | EU | verified | on | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | TC-V12-R-105 | 401 `SSO_REPLAY_DETECTED` |
      | Microsoft Entra ID | SAML 2.0 | R15 auditor | IN | unverified | off | OTP (amr otp) | replayed assertion or code | TC-V12-R-106 | 401 `SSO_REPLAY_DETECTED` |
      | Google Workspace | SAML 2.0 | Custom privileged role | IN | verification lost (TXT missing twice) | off | none | unsigned or alg none | TC-V12-R-107 | 401 `SSO_SIGNATURE_INVALID` |
      | Generic OIDC IdP | OIDC | R03 executive | IN | verified | on | OTP (amr otp) | unsigned or alg none | TC-V12-R-108 | 401 `SSO_SIGNATURE_INVALID` |
      | Generic SAML IdP | SAML 2.0 | R02 startup head | EU | verified | off | none | expired (NotOnOrAfter + 60 s skew passed) | TC-V12-R-109 | 401 `SSO_ASSERTION_EXPIRED` |
      | Generic OIDC IdP | OIDC | R02 startup head | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | TC-V12-R-110 | 401 `SSO_AUDIENCE_MISMATCH` |
      | Microsoft Entra ID | OIDC | Custom privileged role | EU | verification lost (TXT missing twice) | off | OTP (amr otp) | valid | TC-V12-R-111 | session limited to step-up: WebAuthn ceremony required before any privileged API (403 `STEP_UP_REQUIRED` until |
      | Generic SAML IdP | SAML 2.0 | R03 executive | IN | verification lost (TXT missing twice) | on | phishing-resistant (amr hwk/webauthn) | wrong issuer | TC-V12-R-112 | 401 `SSO_ISSUER_MISMATCH` |
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
    Examples: M02 generated rows (see TC-V12-R-265…)
      | idp | op | user | mapping | token | endpoint | tc | expected |
      | Okta | POST create | not yet provisioned | mapped to built-in role | valid | home-region host | TC-V12-R-265 | 201 |
      | Okta | POST create | active member | mapped to custom role | revoked | other-region host | TC-V12-R-266 | 401 `invalidToken` (tokens are region-bound |
      | Okta | PUT replace | not yet provisioned | unmapped group | expired | other-region host | TC-V12-R-267 | 401 `invalidToken` (tokens are region-bound |
      | Okta | PUT replace | deprovisioned | mapped to custom role | other tenant | home-region host | TC-V12-R-268 | 401 SCIM error `invalidToken` (other tenant) |
      | Okta | PATCH active=false | break-glass account | mapped to built-in role | other tenant | other-region host | TC-V12-R-269 | 401 `invalidToken` (tokens are region-bound |
      | Okta | DELETE | break-glass account | unmapped group | revoked | home-region host | TC-V12-R-270 | 401 SCIM error `invalidToken` (revoked) |
      | Okta | PATCH group add | active member | mapped to conflicting custom role | expired | home-region host | TC-V12-R-271 | 401 SCIM error `invalidToken` (expired) |
      | Microsoft Entra ID | POST create | active member | unmapped group | other tenant | home-region host | TC-V12-R-272 | 401 SCIM error `invalidToken` (other tenant) |
      | Microsoft Entra ID | POST create | deprovisioned | mapped to built-in role | expired | other-region host | TC-V12-R-273 | 401 `invalidToken` (tokens are region-bound |
      | Microsoft Entra ID | PUT replace | break-glass account | mapped to custom role | valid | other-region host | TC-V12-R-274 | 401 `invalidToken` (tokens are region-bound |
      | Microsoft Entra ID | PATCH active=false | not yet provisioned | mapped to custom role | revoked | home-region host | TC-V12-R-275 | 401 SCIM error `invalidToken` (revoked) |
      | Microsoft Entra ID | PATCH group add | not yet provisioned | mapped to conflicting custom role | other tenant | other-region host | TC-V12-R-276 | 401 `invalidToken` (tokens are region-bound |
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
    Examples: M03 generated rows (see TC-V12-R-383…)
      | pair | path | scope | actor | tc | expected |
      | Runs:create + Runs:approve | API role save | tenant-wide | R12 tenant admin | TC-V12-R-383 | 422 `SOD_CONFLICT` naming both permissions |
      | Runs:create + Runs:approve | Direct DB insert as app_rw | company-scoped | R01 founder (owned tenant) | TC-V12-R-384 | PostgreSQL exception "separation of duties violation" from trigger `role_permission_sod` (C2-T1) |
      | Configuration:edit + Configuration:approve | API role save | company-scoped | R13 operator support (no JIT grant) | TC-V12-R-385 | 403 `TENANT_SCOPE_REQUIRED` (operator has no default tenant access, ENT-ACC-05) |
      | Configuration:edit + Configuration:approve | Direct DB insert as app_rw | tenant-wide | Custom admin lacking billing.approve | TC-V12-R-386 | PostgreSQL exception "separation of duties violation" from trigger `role_permission_sod` (C2-T1) |
      | Billing:view + Billing:approve | Membership assignment of two roles | tenant-wide | R01 founder (owned tenant) | TC-V12-R-387 | 409 `SOD_CONFLICT_ON_ASSIGNMENT` from the `membership_role` trigger and API check |
      | Billing:view + Billing:approve | SCIM group mapping | company-scoped | R12 tenant admin | TC-V12-R-388 | 409 `SOD_CONFLICT_ON_ASSIGNMENT` |
      | Runs:approve + Runs:dispatch | Membership assignment of two roles | company-scoped | Custom admin lacking billing.approve | TC-V12-R-389 | 409 `SOD_CONFLICT_ON_ASSIGNMENT` from the `membership_role` trigger and API check |
      | Runs:approve + Runs:dispatch | SCIM group mapping | tenant-wide | R13 operator support (no JIT grant) | TC-V12-R-390 | 403 `TENANT_SCOPE_REQUIRED` (operator has no default tenant access, ENT-ACC-05) |
      | Finance:verify_first + Finance:verify_second | API role save | tenant-wide | R01 founder (owned tenant) | TC-V12-R-391 | 422 `SOD_CONFLICT` naming both permissions |
      | Finance:verify_first + Finance:verify_second | Direct DB insert as app_rw | company-scoped | R12 tenant admin | TC-V12-R-392 | PostgreSQL exception "separation of duties violation" from trigger `role_permission_sod` (C2-T1) |
      | Leads:read + Leads:write (no conflict) | API role save | tenant-wide | Custom admin lacking billing.approve | TC-V12-R-393 | 201/200 |
      | Leads:read + Leads:write (no conflict) | Direct DB insert as app_rw | company-scoped | R13 operator support (no JIT grant) | TC-V12-R-394 | 403 `TENANT_SCOPE_REQUIRED` (operator has no default tenant access, ENT-ACC-05) |
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
    Examples: M04 generated rows (see TC-V12-R-407…)
      | cred | state | scope | region | host | rate | tc | expected |
      | API key gek_ | active | leads:read | home region host | developer host | under limit | TC-V12-R-407 | 200 with masked contact fields |
      | API key gek_ | active | leads:write | other region host | browser host (admin/web origin) | at limit | TC-V12-R-408 | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST` |
      | API key gek_ | expired | runs:create | home region host | browser host (admin/web origin) | over limit | TC-V12-R-409 | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST` |
      | API key gek_ | revoked (≤ 60 s ago) | missing scope | other region host | developer host | over limit | TC-V12-R-410 | 401 `INVALID_CREDENTIAL` (credential registry is per region |
      | OAuth client private_key_jwt | expired | leads:read | other region host | developer host | at limit | TC-V12-R-411 | 401 `INVALID_CREDENTIAL` (credential registry is per region |
      | OAuth client private_key_jwt | revoked (≤ 60 s ago) | leads:write | home region host | browser host (admin/web origin) | under limit | TC-V12-R-412 | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST` |
      | OAuth client private_key_jwt | IP not in allowlist | approve/send/pay (non-existent scope) | home region host | developer host | over limit | TC-V12-R-413 | 403 `IP_NOT_ALLOWED` |
      | OAuth client client_secret_basic | expired | missing scope | other region host | browser host (admin/web origin) | under limit | TC-V12-R-414 | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST` |
      | OAuth client client_secret_basic | revoked (≤ 60 s ago) | runs:create | home region host | developer host | at limit | TC-V12-R-415 | 401 `API_KEY_REVOKED` |
      | OAuth client client_secret_basic | IP not in allowlist | leads:read | home region host | browser host (admin/web origin) | at limit | TC-V12-R-416 | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST` |
      | OAuth client client_secret_basic | IP not in allowlist | leads:write | other region host | developer host | under limit | TC-V12-R-417 | 401 `INVALID_CREDENTIAL` (credential registry is per region |
      | OAuth client private_key_jwt | active | leads:read | other region host | browser host (admin/web origin) | over limit | TC-V12-R-418 | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST` |
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
    Examples: M05 generated rows (see TC-V12-R-474…)
      | event | response | attempt | endpoint | region | tc | expected |
      | lead.created | 2xx within 10 s | 1 | verified | IN | TC-V12-R-474 | `developer.webhook_delivery.succeeded` |
      | lead.created | 5xx | 3 | unverified (challenge not passed) | EU | TC-V12-R-475 | No delivery |
      | run.awaiting_approval | timeout > 10 s | 6 | verified | EU | TC-V12-R-476 | `developer.webhook_delivery.exhausted` after attempt 6 (≤ 24 h after first) |
      | invoice.issued | 410 Gone | 6 | unverified (challenge not passed) | IN | TC-V12-R-477 | No delivery |
      | connector.degraded | TLS failure | 1 | unverified (challenge not passed) | EU | TC-V12-R-478 | No delivery |
      | connector.degraded | 3xx redirect | 3 | verified | IN | TC-V12-R-479 | `developer.webhook_delivery.failed` |
      | run.awaiting_approval | 2xx within 10 s | 3 | unverified (challenge not passed) | IN | TC-V12-R-480 | No delivery |
      | invoice.issued | 5xx | 1 | verified | IN | TC-V12-R-481 | `developer.webhook_delivery.failed` |
      | lead.created | TLS failure | 6 | verified | IN | TC-V12-R-482 | `developer.webhook_delivery.exhausted` after attempt 6 (≤ 24 h after first) |
      | run.awaiting_approval | 410 Gone | 1 | verified | EU | TC-V12-R-483 | Endpoint disabled immediately (`developer.webhook_endpoint.disabled`, reason 410) |
      | invoice.issued | timeout > 10 s | 3 | unverified (challenge not passed) | IN | TC-V12-R-484 | No delivery |
      | invoice.issued | 3xx redirect | 1 | unverified (challenge not passed) | EU | TC-V12-R-485 | No delivery |

  @sec
  Scenario Outline: AC-20ZR08-06 SDK signature verification (exhaustive)
    Given a delivery with timestamp "<timestamp>", signature "<signature>" and "<replay>"
    When the receiver calls verify()
    Then the outcome matches test case <tc>: "<expected>"
    Examples: M06 generated rows (see TC-V12-R-498…)
      | timestamp | signature | replay | tc | expected |
      | fresh | valid current secret | first delivery | TC-V12-R-498 | SDK `verify()` returns the parsed event |
      | fresh | valid current secret | duplicate event_id | TC-V12-R-499 | SDK verifies |
      | fresh | valid previous secret within 24 h overlap | first delivery | TC-V12-R-500 | SDK `verify()` returns the parsed event |
      | fresh | valid previous secret within 24 h overlap | duplicate event_id | TC-V12-R-501 | SDK verifies |
      | fresh | previous secret after 24 h overlap | first delivery | TC-V12-R-502 | SDK `verify()` raises `SignatureInvalid` |
      | fresh | previous secret after 24 h overlap | duplicate event_id | TC-V12-R-503 | SDK `verify()` raises `SignatureInvalid` |
      | fresh | tampered body | first delivery | TC-V12-R-504 | SDK `verify()` raises `SignatureInvalid` |
      | fresh | tampered body | duplicate event_id | TC-V12-R-505 | SDK `verify()` raises `SignatureInvalid` |
      | fresh | wrong secret | first delivery | TC-V12-R-506 | SDK `verify()` raises `SignatureInvalid` |
      | fresh | wrong secret | duplicate event_id | TC-V12-R-507 | SDK `verify()` raises `SignatureInvalid` |
      | 299 s old | valid current secret | first delivery | TC-V12-R-508 | SDK `verify()` returns the parsed event |
      | 299 s old | valid current secret | duplicate event_id | TC-V12-R-509 | SDK verifies |
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
    Examples: M07 generated rows (see TC-V12-R-538…)
      | connector | auth | failure | residency | env | gate | tc | expected |
      | Salesforce | OAuth 2.0 auth code + PKCE | none | IN | sandbox | complete | TC-V12-R-538 | Sandbox adapter and provider test account only |
      | Salesforce | OAuth 2.0 auth code + PKCE | 429 throttled | EU | production | DPA missing | TC-V12-R-539 | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing" |
      | Salesforce | OAuth 2.0 client credentials / JWT bearer | 5xx | IN | production | transfer basis CJ-R15 missing | TC-V12-R-540 | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing" |
      | HubSpot | OAuth 2.0 auth code + PKCE | 401 token revoked | IN | production | security review missing | TC-V12-R-541 | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing" |
      | HubSpot | OAuth 2.0 client credentials / JWT bearer | none | EU | production | complete | TC-V12-R-542 | upsert by external ID |
      | SMS-DLT aggregator | API key in vault | none | IN | production | DPA missing | TC-V12-R-543 | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing" |
      | SMS-DLT aggregator | API key in vault | 429 throttled | EU | sandbox | complete | TC-V12-R-544 | Sandbox adapter and provider test account only |
      | Voice CPaaS (140/160 series) | API key in vault | 5xx | EU | production | DLT registration missing | TC-V12-R-545 | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing" |
      | Zoho CRM | OAuth 2.0 auth code + PKCE | timeout on write (uncertain) | EU | production | transfer basis CJ-R15 missing | TC-V12-R-546 | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing" |
      | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | 401 token revoked | IN | sandbox | complete | TC-V12-R-547 | Sandbox adapter and provider test account only |
      | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | validation 4xx | EU | production | security review missing | TC-V12-R-548 | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing" |
      | Voice CPaaS (140/160 series) | API key in vault | timeout on write (uncertain) | IN | sandbox | complete | TC-V12-R-549 | Sandbox adapter and provider test account only |
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
    Examples: M08 generated rows (see TC-V12-R-722…)
      | surface | region | request | header | logging | function_region | tc | expected |
      | Website (startup domain) | IN | page GET (no personal data) | allowlisted only | metadata only | pinned to home region | TC-V12-R-722 | Served by the `website-in` Vercel project |
      | Website (startup domain) | IN | API POST with personal data | non-allowlisted header added | body capture attempted | deployed to a non-home region | TC-V12-R-723 | Deployment rejected by the CI region-pin check (AU-296 rule VD-02) |
      | Website (startup domain) | EU | auth callback | X-Origin-Verify missing (direct-to-origin) | metadata only | deployed to a non-home region | TC-V12-R-724 | Deployment rejected by the CI region-pin check (AU-296 rule VD-02) |
      | Portal (customer) | IN | file upload (portal document) | X-Origin-Verify missing (direct-to-origin) | body capture attempted | pinned to home region | TC-V12-R-725 | 403 at AWS WAF (rule `origin-verify`) |
      | Portal (customer) | EU | page GET (no personal data) | allowlisted only | body capture attempted | deployed to a non-home region | TC-V12-R-726 | Deployment rejected by the CI region-pin check (AU-296 rule VD-02) |
      | Portal (customer) | EU | API POST with personal data | non-allowlisted header added | metadata only | pinned to home region | TC-V12-R-727 | Served by the `portal-eu` Vercel project |
      | Admin | IN | file upload (portal document) | allowlisted only | metadata only | deployed to a non-home region | TC-V12-R-728 | Deployment rejected by the CI region-pin check (AU-296 rule VD-02) |
      | Admin | EU | auth callback | allowlisted only | body capture attempted | pinned to home region | TC-V12-R-729 | Served by the `admin-eu` Vercel project |
      | Developer portal | IN | page GET (no personal data) | non-allowlisted header added | metadata only | deployed to a non-home region | TC-V12-R-730 | Deployment rejected by the CI region-pin check (AU-296 rule VD-02) |
      | Developer portal | EU | page GET (no personal data) | X-Origin-Verify missing (direct-to-origin) | body capture attempted | pinned to home region | TC-V12-R-731 | 403 at AWS WAF (rule `origin-verify`) |
      | Admin | IN | API POST with personal data | X-Origin-Verify missing (direct-to-origin) | metadata only | pinned to home region | TC-V12-R-732 | 403 at AWS WAF (rule `origin-verify`) |
      | Admin | EU | file upload (portal document) | non-allowlisted header added | body capture attempted | deployed to a non-home region | TC-V12-R-733 | Deployment rejected by the CI region-pin check (AU-296 rule VD-02) |
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
    Examples: M09 generated rows (see TC-V12-R-768…)
      | region | failure | wal_age | path | gate | tc | expected |
      | IN | row corruption by bug | 1 min | Supabase PITR to new project | Release 1 gate | TC-V12-R-768 | Restore to T−1 min via Supabase PITR to new project |
      | IN | row corruption by bug | 5 min | AWS WAL-G archive restore | Release 2 gate | TC-V12-R-769 | Restore to T−5 min via AWS WAL-G archive restore |
      | IN | row corruption by bug | 14 min | AWS WAL-G archive restore (in-zone secondary region) | Quarterly drill | TC-V12-R-770 | Restore to T−14 min via AWS WAL-G archive restore (in-zone secondary region) |
      | IN | bad migration | 1 min | AWS WAL-G archive restore | Quarterly drill | TC-V12-R-771 | Restore to T−1 min via AWS WAL-G archive restore |
      | IN | bad migration | 5 min | AWS WAL-G archive restore (in-zone secondary region) | Release 1 gate | TC-V12-R-772 | Restore to T−5 min via AWS WAL-G archive restore (in-zone secondary region) |
      | IN | bad migration | 14 min | Supabase PITR to new project | Release 2 gate | TC-V12-R-773 | Restore to T−14 min via Supabase PITR to new project |
      | IN | accidental tenant delete | 1 min | AWS WAL-G archive restore (in-zone secondary region) | Release 2 gate | TC-V12-R-774 | Restore to T−1 min via AWS WAL-G archive restore (in-zone secondary region) |
      | IN | accidental tenant delete | 5 min | Supabase PITR to new project | Quarterly drill | TC-V12-R-775 | Restore to T−5 min via Supabase PITR to new project |
      | IN | accidental tenant delete | 14 min | AWS WAL-G archive restore | Release 1 gate | TC-V12-R-776 | Restore to T−14 min via AWS WAL-G archive restore |
      | EU | row corruption by bug | 16 min | Supabase PITR to new project | Release 2 gate | TC-V12-R-777 | Restore to T−16 min via Supabase PITR to new project |
      | EU | bad migration | 16 min | AWS WAL-G archive restore | Release 1 gate | TC-V12-R-778 | Restore to T−16 min via AWS WAL-G archive restore |
      | EU | accidental tenant delete | 1 min | Nightly logical dump | Release 1 gate | TC-V12-R-779 | Restore to T−1 min via Nightly logical dump |
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
    Examples: M13 generated rows (see TC-V12-R-1128…)
      | modality | evidence | approvers | tc | expected |
      | text LLM | complete | two distinct approvers | TC-V12-R-1128 | Row `approved` for text LLM with a 12-month re-certification date |
      | text LLM | complete | one approver | TC-V12-R-1129 | Approval refused: two distinct authorised approvers required (R10 AI governance + R01 or delegate) |
      | text LLM | complete | same person twice | TC-V12-R-1130 | Second approval rejected `SAME_APPROVER` |
      | text LLM | DPA no-training clause | two distinct approvers | TC-V12-R-1131 | Approval refused: evidence missing "DPA no-training clause" |
      | text LLM | region/processing location | two distinct approvers | TC-V12-R-1132 | Approval refused: evidence missing "region/processing location" |
      | text LLM | EVAL suites | two distinct approvers | TC-V12-R-1133 | Approval refused: evidence missing "EVAL suites" |
      | text LLM | red-team pass | two distinct approvers | TC-V12-R-1134 | Approval refused: evidence missing "red-team pass" |
      | text LLM | security review | two distinct approvers | TC-V12-R-1135 | Approval refused: evidence missing "security review" |
      | text LLM | cost per accepted result | two distinct approvers | TC-V12-R-1136 | Approval refused: evidence missing "cost per accepted result" |
      | embedding | complete | two distinct approvers | TC-V12-R-1137 | Row `approved` for embedding with a 12-month re-certification date |
      | embedding | complete | one approver | TC-V12-R-1138 | Approval refused: two distinct authorised approvers required (R10 AI governance + R01 or delegate) |
      | embedding | complete | same person twice | TC-V12-R-1139 | Second approval rejected `SAME_APPROVER` |

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
    Examples: M10 generated rows (see TC-V12-R-859…)
      | task | data | region | candidate | state | availability | tc | expected |
      | classification | Public | IN | Claude Sonnet (approved primary) | approved | ok | TC-V12-R-859 | Routed to Claude Sonnet (approved primary) in IN |
      | classification | Public | EU | Claude Haiku-class | candidate | 5xx / timeout | TC-V12-R-860 | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class,  |
      | classification | Internal (non-personal) | IN | Claude larger model (MDL-L1) | suspended | 5xx / timeout | TC-V12-R-861 | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class,  |
      | classification | Internal (non-personal) | EU | OpenAI GPT family | DPA expired | ok | TC-V12-R-862 | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class |
      | drafting | Public | IN | OpenAI GPT family | DPA expired | 5xx / timeout | TC-V12-R-863 | Not routed: registry state `DPA expired` |
      | drafting | Public | EU | Claude larger model (MDL-L1) | suspended | ok | TC-V12-R-864 | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class,  |
      | drafting | Internal (non-personal) | IN | Claude Haiku-class | candidate | ok | TC-V12-R-865 | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class,  |
      | drafting | Internal (non-personal) | EU | Claude Sonnet (approved primary) | approved | 5xx / timeout | TC-V12-R-866 | Routed to Claude Sonnet (approved primary) in EU |
      | complex synthesis | Personal (masked) | IN | Claude Sonnet (approved primary) | candidate | 5xx / timeout | TC-V12-R-867 | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class,  |
      | complex synthesis | Personal (masked) | EU | Google Gemini | approved | ok | TC-V12-R-868 | Routed to Google Gemini in EU |
      | complex synthesis | Personal (unmasked) | IN | Claude larger model (MDL-L1) | DPA expired | ok | TC-V12-R-869 | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class |
      | complex synthesis | Personal (unmasked) | EU | OpenAI GPT family | suspended | 5xx / timeout | TC-V12-R-870 | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class,  |

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
    Examples: M11 generated rows (see TC-V12-R-1056…)
      | cohort | dominance | participant | metric | scope | owner | budget | tc | expected |
      | 9 tenants | no tenant > 30% | opted in | reply rate | IN zone | external tenant | ε budget available | TC-V12-R-1056 | Cell suppressed: "Not enough peers" (k = 9 < 10) |
      | 9 tenants | no tenant > 30% | not opted in | lead-to-meeting cycle time | EU zone | Owner Portfolio startup without R01 opt-in | ε budget exhausted for the period | TC-V12-R-1057 | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04) |
      | 9 tenants | one tenant > 30% of events | opted in | win rate | global | Owner Portfolio startup with R01 opt-in | ε budget exhausted for the period | TC-V12-R-1058 | Cell suppressed: "Not enough peers" (k = 9 < 10) |
      | 10 tenants | no tenant > 30% | withdrawn | lead-to-meeting cycle time | global | Owner Portfolio startup with R01 opt-in | ε budget available | TC-V12-R-1059 | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04) |
      | 10 tenants | one tenant > 30% of events | not opted in | win rate | IN zone | Owner Portfolio startup without R01 opt-in | ε budget available | TC-V12-R-1060 | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04) |
      | 10 tenants | one tenant > 30% of events | withdrawn | reply rate | EU zone | external tenant | ε budget exhausted for the period | TC-V12-R-1061 | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04) |
      | 25 tenants | no tenant > 30% | not opted in | reply rate | IN zone | Owner Portfolio startup with R01 opt-in | ε budget exhausted for the period | TC-V12-R-1062 | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04) |
      | 25 tenants | one tenant > 30% of events | opted in | lead-to-meeting cycle time | EU zone | external tenant | ε budget available | TC-V12-R-1063 | Cell suppressed (dominance rule BM-03) |
      | 25 tenants | no tenant > 30% | withdrawn | win rate | EU zone | Owner Portfolio startup without R01 opt-in | ε budget available | TC-V12-R-1064 | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04) |
      | 10 tenants | no tenant > 30% | not opted in | win rate | global | external tenant | ε budget exhausted for the period | TC-V12-R-1065 | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04) |
      | 9 tenants | one tenant > 30% of events | withdrawn | reply rate | global | Owner Portfolio startup without R01 opt-in | ε budget available | TC-V12-R-1066 | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04) |
      | 25 tenants | one tenant > 30% of events | withdrawn | lead-to-meeting cycle time | IN zone | Owner Portfolio startup without R01 opt-in | ε budget exhausted for the period | TC-V12-R-1067 | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04) |
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
    Examples: M12 generated rows (see TC-V12-R-1100…)
      | role | context | op | path | tc | expected |
      | app_rw | tenant and companies set | SELECT own rows | Django API | TC-V12-R-1100 | rows of the tenant and permitted companies only |
      | app_rw | app.tenant_id not set | INSERT own row | Celery worker | TC-V12-R-1101 | RLS denies: SELECT returns 0 rows, INSERT/UPDATE fail `WITH CHECK` |
      | app_rw | company not in app.company_ids | UPDATE row of another tenant | CI migration (normal) | TC-V12-R-1102 | app_rw used by the migration job: refused by the pipeline policy (migrations run as app_migrator) |
      | app_worker | tenant and companies set | INSERT own row | CI migration (normal) | TC-V12-R-1103 | app_worker used by the migration job: refused by the pipeline policy (migrations run as app_migrator) |
      | app_worker | app.tenant_id not set | SELECT own rows | CI migration with break-glass approval | TC-V12-R-1104 | app_worker used by the migration job: refused by the pipeline policy (migrations run as app_migrator) |
      | app_worker | company not in app.company_ids | DELETE own row | Django API | TC-V12-R-1105 | 0 rows for SELECT |
      | app_migrator | tenant and companies set | UPDATE row of another tenant | Celery worker | TC-V12-R-1106 | Login refused: `app_migrator` may connect only from the CI runner IP set |
      | app_migrator | app.tenant_id not set | DELETE own row | CI migration (normal) | TC-V12-R-1107 | DDL allowed (`SET ROLE app_owner`) |
      | app_migrator | company not in app.company_ids | INSERT own row | CI migration with break-glass approval | TC-V12-R-1108 | DDL allowed (`SET ROLE app_owner`) |
      | service_role | tenant and companies set | DELETE own row | CI migration with break-glass approval | TC-V12-R-1109 | Allowed only for the migration job |
      | service_role | app.tenant_id not set | UPDATE row of another tenant | Django API | TC-V12-R-1110 | Blocked: secret not present in API/worker task definitions (VD/SB policy check fails the deploy) |
      | service_role | company not in app.company_ids | SELECT own rows | Celery worker | TC-V12-R-1111 | Blocked: secret not present in API/worker task definitions (VD/SB policy check fails the deploy) |

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

---

### 11.19.5.15 Test strategy delta (Part 6.1 applied to P4)

| Aspect | Rule for P4 | Source |
|---|---|---|
| Risk areas | Confidentiality across tenants and zones (RA-01), unauthorized external action (RA-03/04), regulatory eligibility (RA-03), recoverability (RA-21), AI routing compliance (RA-13) — all **P0** where the row decides access, residency, money, law or recovery | Part 6.1 §6.1.4 |
| Levels | UT (oracles, SDK verify), IT (PP-05 with real PostgreSQL + RLS + simulators), SYS (PP-01 per zone), E2E (drills, browser SSO), UAT (tenant IdP pilot with an owned startup) | Part 6.1 §6.1.2 |
| Simulators | IdP (Okta, Entra ID, Google, generic SAML/OIDC payload shapes), SCIM client (vendor quirks), CRM (three providers), SMS aggregator (DLT, DND, DLR), CPaaS, webhook receiver, model gateway (registry fixture REG-FIX-3), Vercel API mock for AU-296 | Part 6.1 §6.1.6 |
| Zones | Every SYS suite runs in the IN cell; EU suites run in the EU cell when provisioned and in an EU-configured test cell before (CJ-TC-09 both directions) | DEC-772 |
| Combinatorial design | Parameters and values declared per capability (§11.19.5.16); **3-way** for identity, credentials, connectors (law), residency path, recovery, model routing and benchmarks; **pairwise** for SoD, webhook delivery and DB access; **exhaustive** where ≤ 64 valid combinations (signature verification, registry approval) | V12-B brief |
| Oracle | Each generated row's expected result is computed by the model's oracle function in `R_02_combinatorics.py` from the rules in Part 11.19a/b; disagreements between the system and the oracle are triaged as defects in either | Part 6.1 §6.1.11 |
| Blocking suites | M01, M02, M03, M04, M07 (gate rows), M08, M09, M10, M12 P0 rows; TC-V12-R-001…086 P0 rows; KPI-32 drill | Release 1 gate (GNG-R-01…10) |
| Conformance | SCIM RFC 7644 conformance suite; SAML XSW corpus (12 variants); OIDC conformance profile checks for RP (OpenID Foundation suite, verify availability) | ADR-255/256 |
| Performance | RL-KEY fairness (k6, 2 tenants, one noisy); SCIM bulk 100 ops ≤ 5 s p95; webhook first attempt ≤ 5 s p95; replication lag < 60 s at load profile `m` | Part 6.1 §6.1.3 |
| Accessibility | A203, A002 Roles tab, A168, A204, A008, A011 Registry tab, A042 Benchmarks tab, W47 portal: WCAG 2.2 AA (axe + manual AT pass PP-07) | Part 2.5 |
| Evidence | Each test run exports results per TC ID to the release evidence store; drills write `restore_drill` | Part 6.1 §6.1.12 |

### 11.19.5.16 Combinatorial test design (parameter models, method, counts)

**Generation method.** For each model the script enumerates every combination of the declared values, removes the combinations forbidden by the model's constraints (for example, a generic SAML IdP cannot speak OIDC; sandbox installations cannot have an incomplete gate; Tier 2 rows cannot be chosen for embedding), lists every valid t-tuple (t = 2 or 3) that occurs in at least one valid row, and then repeatedly selects the valid row covering the largest number of still-uncovered t-tuples until all are covered (a deterministic greedy covering-array construction in the AETG family). Spaces with ≤ 64 valid rows are enumerated exhaustively. The oracle then computes each row's expected result. Re-running the script reproduces the same rows and IDs.

| Model | Capability | Parameters (values) | Raw product | Valid | Method | t-tuples | Cases | Pairwise-only size | TC range |
|---|---|---|---|---|---|---|---|---|---|
| M01 | C1 | 8 (28) | 10,800 | 7,200 | 3-way | 2151 | 164 | 36 | TC-V12-R-101…TC-V12-R-264 |
| M02 | C1 | 6 (23) | 2,304 | 1,824 | 3-way | 995 | 118 | 29 | TC-V12-R-265…TC-V12-R-382 |
| M03 | C1 | 4 (16) | 192 | 192 | 2-way | 92 | 24 | — | TC-V12-R-383…TC-V12-R-406 |
| M04 | C2 | 6 (19) | 720 | 720 | 3-way | 593 | 67 | 22 | TC-V12-R-407…TC-V12-R-473 |
| M05 | C2 | 5 (17) | 288 | 288 | 2-way | 110 | 24 | — | TC-V12-R-474…TC-V12-R-497 |
| M06 | C2 | 3 (11) | 40 | 40 | exhaustive | — | 40 | — | TC-V12-R-498…TC-V12-R-537 |
| M07 | C3 | 6 (26) | 2,700 | 624 | 3-way | 976 | 184 | 47 | TC-V12-R-538…TC-V12-R-721 |
| M08 | C4 | 6 (17) | 384 | 288 | 3-way | 392 | 46 | 17 | TC-V12-R-722…TC-V12-R-767 |
| M09 | C5 | 5 (19) | 576 | 456 | 3-way | 455 | 91 | 28 | TC-V12-R-768…TC-V12-R-858 |
| M10 | C6 | 6 (26) | 3,500 | 2,400 | 3-way | 1304 | 197 | 38 | TC-V12-R-859…TC-V12-R-1055 |
| M11 | C7 | 7 (19) | 972 | 972 | 3-way | 690 | 44 | 15 | TC-V12-R-1056…TC-V12-R-1099 |
| M12 | C8 | 4 (19) | 420 | 264 | 2-way | 118 | 28 | — | TC-V12-R-1100…TC-V12-R-1127 |
| M13 | C6 | 3 (15) | 105 | 45 | exhaustive | — | 45 | — | TC-V12-R-1128…TC-V12-R-1172 |
| **Total** | | | | | | | **1072** | | TC-V12-R-101…1172 |

#### M01 Tenant SSO sign-in: IdP × protocol × role × region × domain × enforcement × MFA × assertion

Capability C1 · stories US-01-ZR01, US-01-ZR02 · traces FR-V12-R-001…010; ENT-IDN-01/02/04/05/06; DEC-784; DEC-772

| Parameter | Values | Count |
|---|---|---|
| `idp` | Okta · Microsoft Entra ID · Google Workspace · Generic SAML IdP · Generic OIDC IdP | 5 |
| `protocol` | SAML 2.0 · OIDC | 2 |
| `role` | R12 tenant admin · R02 startup head · R03 executive · R15 auditor · Custom privileged role | 5 |
| `region` | IN · EU | 2 |
| `domain` | verified · unverified · verification lost (TXT missing twice) | 3 |
| `enforcement` | off · on | 2 |
| `mfa` | phishing-resistant (amr hwk/webauthn) · OTP (amr otp) · none | 3 |
| `assertion` | valid · wrong audience · wrong issuer · expired (NotOnOrAfter + 60 s skew passed) · replayed assertion or code · unsigned or alg none | 6 |

Raw product 10,800 · valid after constraints 7,200 · method **3-way** · 2,151 valid 3-tuples · **164 cases** (TC-V12-R-101…TC-V12-R-264) · pairwise alone would need 36

#### M02 SCIM 2.0 provisioning: IdP × operation × user state × group mapping × token × region endpoint

Capability C1 · stories US-01-ZR03 · traces FR-V12-R-011…016; ENT-IDN-03; RFC 7643/7644; DEC-784

| Parameter | Values | Count |
|---|---|---|
| `idp` | Okta · Microsoft Entra ID · Google Workspace | 3 |
| `op` | POST create · PUT replace · PATCH active=false · DELETE · PATCH group add · PATCH group remove | 6 |
| `user` | not yet provisioned · active member · deprovisioned · break-glass account | 4 |
| `mapping` | mapped to built-in role · mapped to custom role · mapped to conflicting custom role · unmapped group | 4 |
| `token` | valid · revoked · expired · other tenant | 4 |
| `endpoint` | home-region host · other-region host | 2 |

Raw product 2,304 · valid after constraints 1,824 · method **3-way** · 995 valid 3-tuples · **118 cases** (TC-V12-R-265…TC-V12-R-382) · pairwise alone would need 29

#### M03 Custom roles and separation of duties: permission pair × path × scope × actor

Capability C1 · stories US-01-ZR04 · traces FR-V12-R-017…022; ENT-ACC-01/02; C2-T1; DEC-784

| Parameter | Values | Count |
|---|---|---|
| `pair` | Runs:create + Runs:approve · Configuration:edit + Configuration:approve · Billing:view + Billing:approve · Runs:approve + Runs:dispatch · Finance:verify_first + Finance:verify_second · Leads:read + Leads:write (no conflict) | 6 |
| `path` | API role save · Direct DB insert as app_rw · Membership assignment of two roles · SCIM group mapping | 4 |
| `scope` | tenant-wide · company-scoped | 2 |
| `actor` | R12 tenant admin · R01 founder (owned tenant) · R13 operator support (no JIT grant) · Custom admin lacking billing.approve | 4 |

Raw product 192 · valid after constraints 192 · method **2-way** · 92 valid 2-tuples · **24 cases** (TC-V12-R-383…TC-V12-R-406)

#### M04 Developer API credentials: credential × state × scope × region × host × rate

Capability C2 · stories US-20-ZR06, US-20-ZR07 · traces FR-V12-R-031…040; ENT-API-01/02/03; DEC-785

| Parameter | Values | Count |
|---|---|---|
| `cred` | API key gek_ · OAuth client private_key_jwt · OAuth client client_secret_basic | 3 |
| `state` | active · expired · revoked (≤ 60 s ago) · IP not in allowlist | 4 |
| `scope` | leads:read · leads:write · runs:create · missing scope · approve/send/pay (non-existent scope) | 5 |
| `region` | home region host · other region host | 2 |
| `host` | developer host · browser host (admin/web origin) | 2 |
| `rate` | under limit · at limit · over limit | 3 |

Raw product 720 · valid after constraints 720 · method **3-way** · 593 valid 3-tuples · **67 cases** (TC-V12-R-407…TC-V12-R-473) · pairwise alone would need 22

#### M05 Outbound webhook delivery: event × endpoint response × attempt × endpoint state × region

Capability C2 · stories US-20-ZR08 · traces FR-V12-R-041…046; ENT-API-05; DEC-785

| Parameter | Values | Count |
|---|---|---|
| `event` | lead.created · run.awaiting_approval · invoice.issued · connector.degraded | 4 |
| `response` | 2xx within 10 s · 5xx · timeout > 10 s · 410 Gone · TLS failure · 3xx redirect | 6 |
| `attempt` | 1 · 3 · 6 | 3 |
| `endpoint` | verified · unverified (challenge not passed) | 2 |
| `region` | IN · EU | 2 |

Raw product 288 · valid after constraints 288 · method **2-way** · 110 valid 2-tuples · **24 cases** (TC-V12-R-474…TC-V12-R-497)

#### M06 Webhook signature verification in the SDKs: timestamp × signature × replay (exhaustive)

Capability C2 · stories US-20-ZR08, US-20-ZR10 · traces FR-V12-R-042, 052; ENT-API-05/06

| Parameter | Values | Count |
|---|---|---|
| `timestamp` | fresh · 299 s old · 301 s old · 301 s in the future | 4 |
| `signature` | valid current secret · valid previous secret within 24 h overlap · previous secret after 24 h overlap · tampered body · wrong secret | 5 |
| `replay` | first delivery · duplicate event_id | 2 |

Raw product 40 · valid after constraints 40 · method **exhaustive** · **40 cases** (TC-V12-R-498…TC-V12-R-537)

#### M07 Connectors: connector × auth × failure mode × residency × environment × activation gate

Capability C3 · stories US-18-ZR11, US-07-ZR12, US-07-ZR13, US-23-ZR14, US-22-ZR15 · traces FR-V12-R-056…080; ENT-INT-01…05; INT-01/04/05; CJ-IN-06/07; DEC-785

| Parameter | Values | Count |
|---|---|---|
| `connector` | Salesforce · HubSpot · Zoho CRM · SMS-DLT aggregator · Voice CPaaS (140/160 series) | 5 |
| `auth` | OAuth 2.0 auth code + PKCE · OAuth 2.0 client credentials / JWT bearer · API key in vault | 3 |
| `failure` | none · 429 throttled · 5xx · 401 token revoked · timeout on write (uncertain) · validation 4xx · DLT template mismatch · DND/preference-registry hit · missed provider event (gap) | 9 |
| `residency` | IN · EU | 2 |
| `env` | sandbox · production | 2 |
| `gate` | complete · DPA missing · transfer basis CJ-R15 missing · DLT registration missing · security review missing | 5 |

Raw product 2,700 · valid after constraints 624 · method **3-way** · 976 valid 3-tuples · **184 cases** (TC-V12-R-538…TC-V12-R-721) · pairwise alone would need 47

#### M08 Vercel personal-data path: surface × tenant region × request × header × logging × function region

Capability C4 · stories US-21-ZR16, US-21-ZR17 · traces FR-V12-R-081…095; DEC-786; DEC-772

| Parameter | Values | Count |
|---|---|---|
| `surface` | Website (startup domain) · Portal (customer) · Admin · Developer portal | 4 |
| `region` | IN · EU | 2 |
| `request` | page GET (no personal data) · API POST with personal data · file upload (portal document) · auth callback | 4 |
| `header` | allowlisted only · non-allowlisted header added · X-Origin-Verify missing (direct-to-origin) | 3 |
| `logging` | metadata only · body capture attempted | 2 |
| `function_region` | pinned to home region · deployed to a non-home region | 2 |

Raw product 384 · valid after constraints 288 · method **3-way** · 392 valid 3-tuples · **46 cases** (TC-V12-R-722…TC-V12-R-767) · pairwise alone would need 17

#### M09 Recovery: region × failure × WAL archive age × restore path × release gate

Capability C5 · stories US-21-ZR18, US-21-ZR19 · traces FR-V12-R-096…110; DEC-787; DEC-771; KPI-18/19/32; OPT-TC-ST-14

| Parameter | Values | Count |
|---|---|---|
| `region` | IN · EU | 2 |
| `failure` | row corruption by bug · bad migration · accidental tenant delete · Supabase project unavailable · AZ loss · region loss | 6 |
| `wal_age` | 1 min · 5 min · 14 min · 16 min | 4 |
| `path` | Supabase PITR to new project · AWS WAL-G archive restore · AWS WAL-G archive restore (in-zone secondary region) · Nightly logical dump | 4 |
| `gate` | Release 1 gate · Release 2 gate · Quarterly drill | 3 |

Raw product 576 · valid after constraints 456 · method **3-way** · 455 valid 3-tuples · **91 cases** (TC-V12-R-768…TC-V12-R-858) · pairwise alone would need 28

#### M10 Model registry routing: task × data class × region × candidate × registry state × availability

Capability C6 · stories US-04-ZR22, US-04-ZR23 · traces FR-V12-R-111…130; DEC-788; AIX-02/03; AU-151/152/298

| Parameter | Values | Count |
|---|---|---|
| `task` | classification · drafting · complex synthesis · embedding · safety screening | 5 |
| `data` | Public · Internal (non-personal) · Personal (masked) · Personal (unmasked) · Restricted | 5 |
| `region` | IN · EU | 2 |
| `candidate` | Claude Sonnet (approved primary) · Claude Haiku-class · Claude larger model (MDL-L1) · OpenAI GPT family · Google Gemini · Open-weight in region (Llama/Mistral/Qwen) · Free Tier 2 provider | 7 |
| `state` | approved · candidate · suspended · DPA expired · eval suite failed | 5 |
| `availability` | ok · 5xx / timeout | 2 |

Raw product 3,500 · valid after constraints 2,400 · method **3-way** · 1,304 valid 3-tuples · **197 cases** (TC-V12-R-859…TC-V12-R-1055) · pairwise alone would need 38

#### M11 Cross-tenant benchmarks: cohort size × dominance × participation × metric × scope × owner flag × budget

Capability C7 · stories US-17-ZR24, US-17-ZR25 · traces FR-V12-R-131…142; DEC-789; CONFLICT-983 resolution

| Parameter | Values | Count |
|---|---|---|
| `cohort` | 9 tenants · 10 tenants · 25 tenants | 3 |
| `dominance` | no tenant > 30% · one tenant > 30% of events | 2 |
| `participant` | opted in · not opted in · withdrawn | 3 |
| `metric` | reply rate · lead-to-meeting cycle time · win rate | 3 |
| `scope` | IN zone · EU zone · global | 3 |
| `owner` | external tenant · Owner Portfolio startup without R01 opt-in · Owner Portfolio startup with R01 opt-in | 3 |
| `budget` | ε budget available · ε budget exhausted for the period | 2 |

Raw product 972 · valid after constraints 972 · method **3-way** · 690 valid 3-tuples · **44 cases** (TC-V12-R-1056…TC-V12-R-1099) · pairwise alone would need 15

#### M12 Supabase access model: database role × context × operation × path

Capability C8 · stories US-01-ZR26, US-01-ZR27 · traces FR-V12-R-143…155; DEC-778; SB-01…SB-10

| Parameter | Values | Count |
|---|---|---|
| `role` | app_rw · app_worker · app_migrator · service_role · postgres · anon via Data API · authenticated via Data API | 7 |
| `context` | tenant and companies set · app.tenant_id not set · company not in app.company_ids | 3 |
| `op` | SELECT own rows · INSERT own row · UPDATE row of another tenant · DELETE own row | 4 |
| `path` | Django API · Celery worker · CI migration (normal) · CI migration with break-glass approval · Browser | 5 |

Raw product 420 · valid after constraints 264 · method **2-way** · 118 valid 2-tuples · **28 cases** (TC-V12-R-1100…TC-V12-R-1127)

#### M13 Registry approval: modality × evidence × approvers (exhaustive)

Capability C6 · stories US-04-ZR21 · traces FR-V12-R-111…118; DEC-788

| Parameter | Values | Count |
|---|---|---|
| `modality` | text LLM · embedding · image generation · video generation · voice (TTS/ASR) | 5 |
| `evidence` | complete · DPA no-training clause · region/processing location · EVAL suites · red-team pass · security review · cost per accepted result | 7 |
| `approvers` | two distinct approvers · one approver · same person twice | 3 |

Raw product 105 · valid after constraints 45 · method **exhaustive** · **45 cases** (TC-V12-R-1128…TC-V12-R-1172)


### 11.19.5.17 Test scenarios

| TS ID | Scenario | Linked stories / FR | Risk area · Priority | TCs |
|---|---|---|---|---|
| TS-V12-R-21 | SSO configuration, enforcement, break-glass, MFA and session policy behave as specified and fail closed | US-01-ZR01, ZR02 · FR-V12-R-001…010 | RA-01 · **P0** | TC-V12-R-001…010 |
| TS-V12-R-22 | SCIM provisioning, mapping, de-provisioning and SLA; custom roles, SoD, SIEM, audit export, JIT, recertification | US-01-ZR03…05 · FR-V12-R-011…026 | RA-01 · **P0** | TC-V12-R-011…020 |
| TS-V12-R-23 | Developer credentials, webhooks, SDKs, portal and sandbox | US-20-ZR06…10 · FR-V12-R-031…055 | RA-01, RA-04 · **P0** | TC-V12-R-021…036 |
| TS-V12-R-24 | Connector gate, CRM sync and ownership, SMS-DLT, voice transport | US-18-ZR11, US-07-ZR12/13, US-23-ZR14, US-22-ZR15 · FR-V12-R-056…080 | RA-03, RA-04 · **P0** | TC-V12-R-037…050 |
| TS-V12-R-25 | Vercel personal-data path controls | US-21-ZR16/17 · FR-V12-R-081…095 | RA-01 · **P0** | TC-V12-R-051…058 |
| TS-V12-R-26 | Recovery paths, monitor and drills | US-21-ZR18/19 · FR-V12-R-096…110 | RA-21 · **P0** | TC-V12-R-059…066 |
| TS-V12-R-27 | Model registry approval, routing, fallback, kill switch, re-certification | US-04-ZR20…23 · FR-V12-R-111…130 | RA-13 · **P0** | TC-V12-R-067…074 |
| TS-V12-R-28 | Benchmarks and database access model | US-17-ZR24/25, US-01-ZR26/27 · FR-V12-R-131…155 | RA-01 · **P0** | TC-V12-R-075…086 |
| TS-V12-R-01…13 | Generated combinatorial suites M01…M13 (one TS per model) | per model (§11.19.5.16) | per model · **P0** | TC-V12-R-101…1172 |

### 11.19.5.18 Test cases (full form)

#### Group TC-V12-R-A: Equivalence partitioning and error guessing – enterprise identity (US-01-ZR01…05)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-001 | Create, test and activate an Okta SAML connection | TS-V12-R-21 · US-01-ZR01 AC-01ZR01-01 · FR-V12-R-001, 004, 029; ENT-IDN-01 | Pre: PP-01 IN; R12 `meera` with WebAuthn age 1 h. Data: okta-sim metadata with 2 signing certificates | 1. POST connection. 2. POST test-login; complete with valid assertion. 3. POST activate. 4. SELECT from `ge.identity_provider` view | 1: 201 `draft`. 2: 202 then event `tested` ok. 3: 200 `active`, `last_test_ok_at` set. 4: one row with protocol `SAML 2.0` | P0 | T01 | UC | Y | SYS |
| TC-V12-R-002 | Reject http metadata and weak algorithms; bind issuer to connection | TS-V12-R-21 · AC-01ZR01-02 · FR-V12-R-002, 003 | Pre: PP-01. Data: `http://…/metadata`; metadata signed RSA-SHA1; assertion from issuer of another tenant | Submit each | 422 `METADATA_URL_NOT_HTTPS`; 422 `UNSUPPORTED_ALG`; sign-in 401 `SSO_ISSUER_MISMATCH`; NSE | P0 | T07 | EP | Y | SYS |
| TC-V12-R-003 | XML signature wrapping corpus is rejected | TS-V12-R-21 · FR-V12-R-003; ADR-255 | Pre: PP-05 broker adapter. Data: XSW-1…XSW-8, comment-in-NameID, duplicate assertion, unsigned assertion in signed response (12 variants) | Post each to the ACS | 12/12 rejected with `SSO_SIGNATURE_INVALID` or `SSO_SCHEMA_INVALID`; SEV3 events; no session | P0 | T07 | EG | Y | IT |
| TC-V12-R-004 | Activation needs a successful test; AU-290 warns before certificate expiry | TS-V12-R-21 · AC-01ZR01-04 · FR-V12-R-004, 027 | Pre: PP-01. Data: certificate `not_after` = CLK-0 + 14 days | 1. Activate untested. 2. Run AU-290 | 1: 409 `TEST_LOGIN_REQUIRED`. 2: `identity.certificate.expiring` (14-day threshold) and R12 notification | P1 | T01 | EP | Y | SYS |
| TC-V12-R-005 | Zone resolution before personal data | TS-V12-R-21 · FR-V12-R-005; DEC-895 | Pre: IN and EU test cells. Data: email `anna@nordlicht.example.de` (EU tenant) entered on `admin.in` | Discover; follow redirect | Redirect to `admin.eu`; IN cell logs contain only the domain hash; no IN session row | P0 | T15 | EP | Y | SYS |
| TC-V12-R-006 | Domain verification and loss after two misses | TS-V12-R-21 · AC-01ZR02-01/03 · FR-V12-R-006 | Pre: DNS simulator. Data: TXT present, then absent on 2 daily checks | Verify; run AU-290 twice | `verified`; after miss 1 still `verified` (misses=1); after miss 2 `verification_lost`, High notice; enforced sign-in still works | P0 | T01 | ST | Y | SYS |
| TC-V12-R-007 | Enforcement guard in API and trigger | TS-V12-R-21 · AC-01ZR02-02 · FR-V12-R-007 | Pre: PP-05. Data: verified domain, no break-glass | 1. POST enforce. 2. `UPDATE ge.idp_connection SET enforced = true` as app_rw | 1: 409 `SSO_ENFORCEMENT_REQUIRES_BREAKGLASS`. 2: exception same code; NSE | P0 | T07 | DT | Y | IT |
| TC-V12-R-008 | Break-glass requires hardware key; use raises SEV3 | TS-V12-R-21 · AC-01ZR02-04 · FR-V12-R-008 | Pre: PP-01. Data: account without hardware key; then with | 1. Create without key. 2. Create with key. 3. Sign in | 1: 422 `HARDWARE_KEY_REQUIRED`. 2: 201. 3: SEV3, notifications to all R12/R10 ≤ 5 min | P0 | T07 | EP | Y | SYS |
| TC-V12-R-009 | Step-up for privileged role when IdP amr lacks phishing-resistant factor | TS-V12-R-21 · FR-V12-R-009; DEC-077 | Pre: PP-01. Data: R02 sign-in with `amr=["pwd","otp"]` | Sign in; call privileged API; complete WebAuthn; call again | First call 403 `STEP_UP_REQUIRED`; after WebAuthn 200; session `amr` updated | P0 | T07 | DT | Y | SYS |
| TC-V12-R-010 | Session policy boundaries and revocation ≤ 60 s | TS-V12-R-21 · AC-01ZR02-05 · FR-V12-R-010 | Pre: PP-01. Data: values 0/1/24/25 h and 4/5/120/121 min | PATCH each; revoke a session; call API at +59 s and +61 s | Out-of-range 422; in-range 200 (privileged capped 12 h/30 min); revoked call 401 by +60 s | P1 | T07 | BVA | Y | SYS |
| TC-V12-R-011 | SCIM conformance suite | TS-V12-R-22 · FR-V12-R-011 | Pre: PP-01 SCIM base IN. Data: RFC 7644 conformance suite run against tenant T1 | Run suite | All mandatory checks pass (Users, Groups, filter, PATCH, ETag, errors) | P0 | T10 | EP | Y | SYS |
| TC-V12-R-012 | Unmapped group grants nothing; mapping needs second approver | TS-V12-R-22 · AC-01ZR03-03 · FR-V12-R-013 | Pre: PP-01. Data: group `All-Staff` | Add user; request mapping; approve by requester; approve by another R12 | No role; 403 `SAME_APPROVER`; after approval role granted ≤ 60 s | P0 | T07 | DT | Y | SYS |
| TC-V12-R-013 | SCIM token shown once, hashed, zone-bound | TS-V12-R-22 · FR-V12-R-012 | Pre: PP-01. Data: lifetime 398 days; then 365 | Create; read DB; use on EU host | 422 for 398; 201 token once; DB has hash only; EU host 401 | P0 | T07 | BVA | Y | SYS |
| TC-V12-R-014 | RL-SCIM and Bulk limits | TS-V12-R-22 · FR-V12-R-016 | Pre: PP-01. Data: 61 requests in 60 s; Bulk with 101 ops | Send | 61st → 429 `tooMany`; Bulk 101 → 413/`tooMany` with no partial apply | P1 | T03 | BVA | Y | SYS |
| TC-V12-R-015 | De-provisioning revokes sessions, keys, clients; re-queues approvals | TS-V12-R-22 · AC-01ZR03-02 · FR-V12-R-014 | Pre: PP-05. Data: user with 2 sessions, 1 key, 1 OAuth client, 2 pending approvals | PATCH active=false; observe for 60 s | All revoked ≤ 60 s; approvals assigned to R12 queue; scheduled jobs re-assigned; `identity.revocation.completed` with `product_ms` ≤ 60,000 | P0 | T07 | UC | Y | IT |
| TC-V12-R-016 | End-to-end SLA breach detection | TS-V12-R-22 · AC-01ZR03-05 · FR-V12-R-015 | Pre: PP-05. Data: `idp_changed_at` 18 min before receipt | Run AU-291 | `end_to_end_s` = 1,080; SEV2; RB-ID-04 linked | P0 | T21 | EP | Y | IT |
| TC-V12-R-017 | Permission catalogue generated and flagged | TS-V12-R-22 · FR-V12-R-017 | Pre: CI. Data: RBAC YAML v12 | Generate; diff | Every permission `Resource:action`, flags set; catalogue_version increments; unknown permission in role → 422 `UNKNOWN_PERMISSION` | P1 | T01 | EP | Y | UT |
| TC-V12-R-018 | Consequential permission in custom role needs R10 co-approval | TS-V12-R-22 · FR-V12-R-018, 022 | Pre: PP-01. Data: role with `Mandates:request` | Create as R12; approve as R10 | Pending until R10 approves; then active | P0 | T07 | DT | Y | SYS |
| TC-V12-R-019 | SoD matrix of record, SIEM sink and audit export | TS-V12-R-22 · FR-V12-R-020, 024, 025 | Pre: PP-05. Data: 12 pairs; sink https test collector; 1,000 audit rows, one edited | Query matrix; send test; export; verify | 12 pairs present; test delivered; export count = filter count; verify reports break at edited row | P0 | T19 | EP | Y | IT |
| TC-V12-R-020 | Role applies at API, worker and UI; JIT ticket; recertification suspension | TS-V12-R-22 · FR-V12-R-021, 023, 026 | Pre: PP-01/06. Data: custom role without `Leads:write` | Try write via API, via worker task, via UI; JIT grant without ticket; let recert lapse | 403 / task denied / control hidden; JIT 422 `TICKET_REQUIRED`; privileged permissions suspended day 14 | P0 | T15 | EP | Y | SYS |

#### Group TC-V12-R-B: Developer platform (US-20-ZR06…10)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-021 | Key created once, stored as hash with zone | TS-V12-R-23 · AC-20ZR06-01 · FR-V12-R-031 | Pre: PP-01 IN | Create; GET key list; SELECT row | Plaintext only in create response, `no-store`; list shows prefix+last4; row has hash, `zone=IN` | P0 | T07 | EP | Y | SYS |
| TC-V12-R-022 | Rotation overlap, revocation ≤ 60 s and leak response | TS-V12-R-23 · FR-V12-R-033, 052 | Pre: PP-01. Data: overlap 24 h; leak report webhook | Rotate; call with old at +23 h and +25 h; post leak report | Old works at +23 h, 401 at +25 h; leaked key 401 ≤ 60 s; R12 notified | P0 | T07 | BVA | Y | SYS |
| TC-V12-R-023 | No consequential scope possible (API and DB) | TS-V12-R-23 · AC-20ZR06-02 · FR-V12-R-034 | Pre: PP-05. Data: scopes `send`, `pay`, `bids:submit` | API create; direct INSERT | 422 `SCOPE_NOT_GRANTABLE`; check violation `api_key_no_consequential_scope_ck` | P0 | T07 | EP | Y | IT |
| TC-V12-R-024 | Client credentials with private_key_jwt | TS-V12-R-23 · AC-20ZR07-01 · FR-V12-R-035 | Pre: PP-01. Data: ES256 key pair, JWKS URL | Token request; API call | 200 token, 15 min, aud `api.in`; API 200 | P0 | T01 | UC | Y | SYS |
| TC-V12-R-025 | Assertion replay and exp window | TS-V12-R-23 · AC-20ZR07-02/04 · FR-V12-R-036 | Pre: PP-01. Data: same jti twice; exp +300 s | Post | 400 `invalid_client` both; no token | P0 | T07 | EG | Y | SYS |
| TC-V12-R-026 | Token revocation and client suspension | TS-V12-R-23 · AC-20ZR07-05 · FR-V12-R-037 | Pre: PP-01 | Revoke; call; suspend client; request token | 401; 400 `invalid_client` | P1 | T07 | EP | Y | SYS |
| TC-V12-R-027 | Signature format and dual signatures during rotation | TS-V12-R-23 · FR-V12-R-041 | Pre: PP-05 receiver simulator | Rotate secret; deliver event | Header has two `v1` values for 24 h; one after | P0 | T07 | EP | Y | IT |
| TC-V12-R-028 | Retry schedule and exhaustion | TS-V12-R-23 · AC-20ZR08-03 · FR-V12-R-042 | Pre: PP-05 virtual clock. Data: receiver 503 always | Deliver | Attempts at T, +5 m, +35 m, +2 h 35 m, +8 h 35 m, +23 h 35 m (±10%); `exhausted` | P1 | T18 | BVA | Y | IT |
| TC-V12-R-029 | Delivery log and replay window | TS-V12-R-23 · AC-20ZR08-04 · FR-V12-R-044 | Pre: PP-01. Data: deliveries 29 and 31 days old | Replay each | 202 for 29 days; 409 `OUTSIDE_REPLAY_WINDOW` for 31 | P2 | T01 | BVA | Y | SYS |
| TC-V12-R-030 | SSRF guard at registration and delivery (DNS rebinding) | TS-V12-R-23 · AC-20ZR08-02 · FR-V12-R-045 | Pre: PP-05 DNS simulator. Data: `169.254.169.254`, `10.0.0.5`, `[::1]`, host that resolves public then private | Register; deliver after re-resolution | 422 at registration; delivery refused when resolution turns private; no redirect followed | P0 | T07 | EG | Y | IT |
| TC-V12-R-031 | Payloads carry references only | TS-V12-R-23 · FR-V12-R-046, 047 | Pre: PP-05. Data: lead with phone and email | Emit `lead.created`; `consent.withdrawn` | Payload has IDs and changed field names only; withdrawn uses subject hash | P0 | T19 | EP | Y | IT |
| TC-V12-R-032 | Portal, changelog and deprecation headers | TS-V12-R-23 · AC-20ZR09-04 · FR-V12-R-040, 051 | Pre: portal build. Data: deprecated op with sunset | Build; call op | Portal lists region base URLs; headers `Deprecation`, `Sunset`, `Link` present | P1 | T01 | EP | Y | SYS |
| TC-V12-R-033 | SDK contract suites in three languages | TS-V12-R-23 · AC-20ZR10-01 · FR-V12-R-048…050 | Pre: sandbox IN and EU | Run suite per language and zone | 6/6 green; artefacts verified signatures | P1 | T10 | PW | Y | CT |
| TC-V12-R-034 | Sandbox synthetic-only and simulator-only | TS-V12-R-23 · AC-20ZR09-02 · FR-V12-R-053 | Pre: sandbox tenant. Data: CSV with a real-format number not in generator pattern; request for production adapter | Import; dispatch | Import 422 `SANDBOX_SYNTHETIC_ONLY`; adapter registry returns simulator only | P0 | T17 | EG | Y | SYS |
| TC-V12-R-035 | Promotion review with requester ≠ approver | TS-V12-R-23 · AC-20ZR09-03 · FR-V12-R-054 | Pre: PP-01 | Request; self-approve; approve by other | 403 `SAME_APPROVER`; then revision Active with diff hash | P0 | T07 | DT | Y | SYS |
| TC-V12-R-036 | Promotion refused with sandbox credential | TS-V12-R-23 · FR-V12-R-055 | Pre: PP-01. Data: revision referencing `gek_test_` | Request promotion | 422 `CONTAINS_SANDBOX_CREDENTIAL` | P1 | T07 | EP | Y | SYS |

#### Group TC-V12-R-C: Connectors (US-18-ZR11, US-07-ZR12/13, US-23-ZR14, US-22-ZR15)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-037 | Manifest completeness for every connector | TS-V12-R-24 · FR-V12-R-056 | Pre: CI | Validate manifests against schema | All 5 R1 connectors have auth, scopes, data classes, events, limits, failure classes, sandbox, owner | P1 | T01 | EP | Y | UT |
| TC-V12-R-038 | Secrets only in vault; workers refresh | TS-V12-R-24 · FR-V12-R-057 | Pre: PP-05 | OAuth connect; grep DB, logs, HTML for token | Only `credential_ref` stored; 0 matches; browser never receives refresh token | P0 | T07 | EG | Y | IT |
| TC-V12-R-039 | Gate checklist and SoD on activation | TS-V12-R-24 · AC-18ZR11-01…04 · FR-V12-R-058, 059 | Pre: PP-01. Data: evidence sets complete / missing each item / unapproved pack | Request; approve | Matches AC rows; DB guard raises for unapproved pack | P0 | T19 | DT | Y | SYS |
| TC-V12-R-040 | CRM consent protection and opt-out import | TS-V12-R-24 · AC-07ZR13-01/02 · FR-V12-R-063, 064 | Pre: PP-05 CRM simulator (each provider) | Send opt-in over suppression; send opt-out | Suppression kept; conflict logged; opt-out imported | P0 | T19 | DT | Y | IT |
| TC-V12-R-041 | Field policy conflicts and webhook authenticity | TS-V12-R-24 · AC-07ZR13-04 · FR-V12-R-065, 068 | Pre: PP-05. Data: simultaneous edits; forged HubSpot signature | Sync; post forged event | Conflict queued; forged event 401, not persisted | P0 | T07 | EG | Y | IT |
| TC-V12-R-042 | Change capture gap repair | TS-V12-R-24 · FR-V12-R-067 | Pre: PP-05. Data: 3 events dropped by simulator | Run sync | Gap detected; repair fetch; no duplicates | P1 | T16 | EG | Y | IT |
| TC-V12-R-043 | Health metrics and alert | TS-V12-R-24 · AC-18ZR11-05 · FR-V12-R-062 | Pre: PP-05 | Inject 60% errors | Breaker open, `Degraded`, alert ≤ 5 min | P1 | T21 | EP | Y | IT |
| TC-V12-R-044 | DLT registration formats and template match | TS-V12-R-24 · AC-23ZR14-01/02 · FR-V12-R-070, 074 | Pre: PP-05 aggregator simulator. Data: entity ID 18 digits; template with 2 vars; message with 3 | Register; dispatch | 422 `ENTITY_ID_FORMAT`; HOLD `DLT_TEMPLATE_MISMATCH` | P0 | T19 | BVA | Y | IT |
| TC-V12-R-045 | Promotional window boundaries and variable injection | TS-V12-R-24 · AC-23ZR14-04 · FR-V12-R-072 | Pre: PP-04 engine. Data: times 08:59…21:00; variable with a URL not in pattern | Evaluate | Per AC table; variable rejected `TEMPLATE_VARIABLES` | P0 | T19 | BVA | Y | UT |
| TC-V12-R-046 | DLR reconciliation and STOP | TS-V12-R-24 · AC-23ZR14-05 · FR-V12-R-073 | Pre: PP-05 | Send; DLR; inbound STOP | Delivered state; suppression ≤ 60 s; confirmation on service header | P0 | T19 | UC | Y | IT |
| TC-V12-R-047 | Transfer entry for out-of-zone provider (EU tenant, US-hosted CRM) | TS-V12-R-24 · FR-V12-R-079 | Pre: EU test cell. Data: no CJ-R15 entry | Request activation | 409 gate incomplete "transfer basis CJ-R15 missing" | P0 | T19 | EP | Y | SYS |
| TC-V12-R-048 | Number series vs purpose | TS-V12-R-24 · AC-22ZR15-02 · FR-V12-R-075 | Pre: PP-05 | Register 140 as service; promotional from 160 | 422 `SERIES_PURPOSE_MISMATCH`; HOLD | P0 | T19 | DT | Y | IT |
| TC-V12-R-049 | Click-to-call and uncertain status | TS-V12-R-24 · AC-22ZR15-01/04 · FR-V12-R-076 | Pre: PP-05 CPaaS simulator | Call; timeout after accept | Completed; second case `Uncertain` reconciled before retry | P1 | T18 | UC | Y | IT |
| TC-V12-R-050 | Recording consent and Part 11.18 interface | TS-V12-R-24 · AC-22ZR15-03 · FR-V12-R-077, 078 | Pre: PP-05; pack all-party consent | Call without consent; AI voice workflow call via VoicePort | No recording; AI workflow call carries Part 11.18 disclosure/consent fields or is refused | P0 | T19 | DT | Y | IT |

#### Group TC-V12-R-D: Vercel path, recovery, registry, benchmarks, database roles

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-051 | Project-zone and domain binding | TS-V12-R-25 · AC-21ZR16-02 · FR-V12-R-081 | Pre: Vercel API mock. Data: IN domain attached to `web-eu` | Run AU-296 | VD-11 fail; finding; deployment block | P0 | T19 | EP | Y | SYS |
| TC-V12-R-052 | Region pin check and fallback | TS-V12-R-25 · AC-21ZR16-01 · FR-V12-R-082, 094 | Pre: CI | Deploy with `iad1`; simulate Vercel outage | Blocked; DNS fallback runbook serves from S3/CloudFront in zone | P0 | T19 | EP | Y | SYS |
| TC-V12-R-053 | No bodies or tokens in logs | TS-V12-R-25 · AC-21ZR17-01 · FR-V12-R-085, 086 | Pre: staging. Data: 1,000 requests with bodies and `?token=` | Send; scan drain | 0 bodies, 0 tokens; lint fails on body logging | P0 | T19 | EG | Y | SYS |
| TC-V12-R-054 | Origin bypass blocked | TS-V12-R-25 · AC-21ZR17-02 · FR-V12-R-088 | Pre: staging | Direct call without header; with stale secret after overlap | 403 both | P0 | T07 | EP | Y | SYS |
| TC-V12-R-055 | Header allowlist | TS-V12-R-25 · AC-21ZR17-03 · FR-V12-R-087 | Pre: staging. Data: 20 headers | Send | Only VD-05 headers reach origin | P0 | T07 | EP | Y | SYS |
| TC-V12-R-056 | No caching of personal responses | TS-V12-R-25 · FR-V12-R-089 | Pre: staging | Two users fetch the same portal URL | `no-store`; no `x-vercel-cache: HIT` | P0 | T07 | EG | Y | SYS |
| TC-V12-R-057 | Sub-processor list and notice | TS-V12-R-25 · AC-21ZR17-04 · FR-V12-R-091 | Pre: DB | Insert row with notice 20 days | Check violation | P1 | T19 | BVA | Y | UT |
| TC-V12-R-058 | Edge-transit position in IN and EU packs | TS-V12-R-25 · FR-V12-R-095; DEC-887 | Pre: Part 11.15 packs | Document check | Both packs contain the approved wording and counsel reference | P0 | T19 | EP | N (document review) | UAT |
| TC-V12-R-059 | PITR enabled at maximum retention per zone | TS-V12-R-26 · FR-V12-R-096 | Pre: management API | Read status | Enabled; retention recorded in `recovery_path` | P0 | T21 | EP | Y | SYS |
| TC-V12-R-060 | Standby replicates with schema parity | TS-V12-R-26 · FR-V12-R-097, 101 | Pre: staging | Apply migration; write rows | Subscriber has the same schema; lag < 60 s | P0 | T21 | EP | Y | IT |
| TC-V12-R-061 | Encryption, Object Lock and two-holder restore credentials | TS-V12-R-26 · FR-V12-R-098, 110 | Pre: AWS | Attempt delete; read with one holder | Denied; restore needs both | P0 | T07 | EG | Y | SYS |
| TC-V12-R-062 | Monitor thresholds | TS-V12-R-26 · AC-21ZR18-02 · FR-V12-R-100 | Pre: stop subscriber | Wait | Warn 5, page 10, SEV1 15 min | P0 | T21 | BVA | Y | SYS |
| TC-V12-R-063 | Growth RTO ≤ 120 min drill | TS-V12-R-26 · AC-21ZR19-01 · FR-V12-R-103; KPI-32 | Pre: drill env | Run DR-R2 | `achieved_rto_min` ≤ 120 | P0 | T21 | UC | Y | E2E |
| TC-V12-R-064 | Drill cadence enforced | TS-V12-R-26 · FR-V12-R-104 | Pre: release record without drill | Open gate | Gate blocked "drill missing" | P0 | T21 | EP | Y | SYS |
| TC-V12-R-065 | PRV pack and erasure replay | TS-V12-R-26 · AC-21ZR19-03 · FR-V12-R-105, 106 | Pre: drill | Restore | PRV-01…08 pass; erased subject absent | P0 | T19 | UC | Y | E2E |
| TC-V12-R-066 | Missed RPO blocks release | TS-V12-R-26 · AC-21ZR19-02 · FR-V12-R-108 | Pre: drill with lag 17 min | Restore | `passed=false`; blocker | P0 | T21 | BVA | Y | E2E |
| TC-V12-R-067 | Registry constraints | TS-V12-R-27 · AC-04ZR20-03 · FR-V12-R-111, 112, 130 | Pre: PP-05 | Insert free-tier row with Personal; open-weight with Restricted; approved without DPA | Three check violations | P0 | T14 | EP | Y | IT |
| TC-V12-R-068 | Evidence completeness gate | TS-V12-R-27 · FR-V12-R-113 | Pre: PP-01 | Approve with each evidence item missing | 422 `EVIDENCE_INCOMPLETE` naming the item | P0 | T19 | EP | Y | SYS |
| TC-V12-R-069 | Two distinct approvers | TS-V12-R-27 · AC-04ZR20-01/02 · FR-V12-R-114 | Pre: PP-01 | Approve twice by same; then by R01 delegate | 403; then approved | P0 | T19 | DT | Y | SYS |
| TC-V12-R-070 | REG-002 Founder approval record | TS-V12-R-27 · AC-04ZR23-01 · FR-V12-R-115 | Pre: seeded registry | Read REG-002 | Approval cites DEC-788; default for MDL-M1 | P1 | T19 | EP | Y | SYS |
| TC-V12-R-071 | Fallback rule and route explanation | TS-V12-R-27 · FR-V12-R-121, 122, 128 | Pre: PP-05; primary 503 | Run step | Fallback to same-schema same-zone row or HOLD; explanation lists reasons | P0 | T14 | DT | Y | IT |
| TC-V12-R-072 | Re-certification suspension | TS-V12-R-27 · AC-04ZR21-02 · FR-V12-R-124 | Pre: row with `recert_due` yesterday | Run AU-298 | Suspended; routing updated ≤ 60 s | P0 | T19 | EP | Y | IT |
| TC-V12-R-073 | Kill switch ≤ 60 s | TS-V12-R-27 · AC-04ZR22-02 · FR-V12-R-123 | Pre: PP-05 | Set switch; run steps | No calls after 60 s; HOLD | P0 | T14 | BVA | Y | IT |
| TC-V12-R-074 | Canary promotion criteria | TS-V12-R-27 · AC-04ZR23-02 · FR-V12-R-127 | Pre: replay traffic | Run 7-day canary (accelerated) | 5% share; promoted only if not worse | P2 | T14 | EP | Y | SYS |
| TC-V12-R-075 | Opt-in and withdrawal | TS-V12-R-28 · AC-17ZR24-01 · FR-V12-R-131, 132 | Pre: PP-01 | Opt in; withdraw mid-period | Contributions from next period; withdrawal effective next period | P0 | T19 | ST | Y | SYS |
| TC-V12-R-076 | Contributions only inside tenant context | TS-V12-R-28 · FR-V12-R-135 | Pre: PP-05 | Call `bench_contribute` without context; as app_bench SELECT lead | `CONTEXT_MISSING`; permission denied | P0 | T15 | EG | Y | IT |
| TC-V12-R-077 | k = 9 suppressed, k = 10 published | TS-V12-R-28 · FR-V12-R-136 | Pre: BM-FIX-1 | Aggregate | Suppressed / published with band 10–24 | P0 | T19 | BVA | Y | IT |
| TC-V12-R-078 | Noise distribution and ledger | TS-V12-R-28 · FR-V12-R-138 | Pre: PP-04 | 10,000 draws with fixed seed | Empirical scale within 5% of Δ/ε; ledger adds 0.5 per release; 13th release in a year refused | P0 | T19 | PBT | Y | UT |
| TC-V12-R-079 | Only rates and durations, rounded | TS-V12-R-28 · FR-V12-R-140 | Pre: PP-01 | Read cells | No counts or amounts; rounding applied | P1 | T19 | EP | Y | SYS |
| TC-V12-R-080 | Merge-up and DPIA gate | TS-V12-R-28 · FR-V12-R-141, 142 | Pre: cohort with 6 in band, 11 overall | Aggregate; publish without DPIA ref | Published at merged level; publication blocked until DPIA ref present | P0 | T19 | DT | Y | SYS |
| TC-V12-R-081 | Data API closed | TS-V12-R-28 · AC-01ZR27-01 · FR-V12-R-145 | Pre: Supabase branch | Call REST/GraphQL for `ge` tables | 404 / permission denied | P0 | T07 | EP | Y | IT |
| TC-V12-R-082 | No service_role in runtime; detector | TS-V12-R-28 · AC-01ZR27-02 · FR-V12-R-144, 155 | Pre: CI and staging | Add env var to task def; open session as service_role from app subnet | Deploy fails; SEV2 ≤ 2 min | P0 | T07 | EG | Y | SYS |
| TC-V12-R-083 | Break-glass migration record | TS-V12-R-28 · AC-01ZR27-03 · FR-V12-R-146 | Pre: CI | Run with and without approvals | Without: blocked; with: audit has two approvers, expiry | P0 | T07 | DT | Y | SYS |
| TC-V12-R-084 | Context per transaction under pooling | TS-V12-R-28 · FR-V12-R-143, 148 | Pre: PP-05 Supavisor transaction mode | 1,000 interleaved requests for two tenants | 0 cross-tenant rows; missing context → `CONTEXT_MISSING` | P0 | T15 | PBT | Y | IT |
| TC-V12-R-085 | Forced RLS and no-bypass assertions; drift | TS-V12-R-28 · AC-01ZR26-02 · FR-V12-R-149, 150, 154 | Pre: branch | Create table without RLS; alter role BYPASSRLS; run AU-292 | CI raises both errors; drift finding | P0 | T07 | EG | Y | IT |
| TC-V12-R-086 | Idempotent role rename | TS-V12-R-28 · FR-V12-R-151 | Pre: DB with `ge_*` roles | Run DDL-V12-R-16 twice | Roles renamed once; second run no-op; grants intact | P1 | T16 | EP | Y | IT |

### 11.19.5.19 Test cases (generated, parameterized form)

#### Group TC-V12-R-M01: 3-way combinatorial cases – Tenant SSO sign-in: IdP × protocol × role × region × domain × enforcement × MFA × assertion

**Common for TC-V12-R-101…TC-V12-R-264:** Pre: PP-01 per region stack (IN = Mumbai, EU = Frankfurt); tenant "Kestrel Analytics" (IN) or "Nordlicht GmbH" (EU); IdP simulator with signed metadata, two active signing certificates; clock CLK-0. Steps: 1. POST `/bff/admin/sso/discover` {email}. 2. Follow redirect to the IdP simulator, which returns the assertion/code variant in the row. 3. Callback to the BFF; read session, audit and security-event tables in the tenant region; call one privileged API (`PATCH /api/v1/tenants/{id}/security-policy`). Links for every row: TS-V12-R-01 · US-01-ZR01, US-01-ZR02 · FR-V12-R-001…010; ENT-IDN-01/02/04/05/06; DEC-784; DEC-772. Technique PW (3-way); generated by `assembly/v12b/R_02_combinatorics.py` (model M01).

| ID | idp | protocol | role | region | domain | enforcement | mfa | assertion | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-101 | Okta | SAML 2.0 | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | valid | session created with `acr`/`amr` recorded; no step-up for 12 h (ABAC-11); session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-102 | Okta | SAML 2.0 | R02 startup head | EU | verification lost (TXT missing twice) | on | OTP (amr otp) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-103 | Okta | OIDC | R03 executive | EU | unverified | off | none | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-104 | Microsoft Entra ID | OIDC | R12 tenant admin | IN | verification lost (TXT missing twice) | on | none | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-105 | Google Workspace | OIDC | R15 auditor | EU | verified | on | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-106 | Microsoft Entra ID | SAML 2.0 | R15 auditor | IN | unverified | off | OTP (amr otp) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-107 | Google Workspace | SAML 2.0 | Custom privileged role | IN | verification lost (TXT missing twice) | off | none | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-108 | Generic OIDC IdP | OIDC | R03 executive | IN | verified | on | OTP (amr otp) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-109 | Generic SAML IdP | SAML 2.0 | R02 startup head | EU | verified | off | none | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-110 | Generic OIDC IdP | OIDC | R02 startup head | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-111 | Microsoft Entra ID | OIDC | Custom privileged role | EU | verification lost (TXT missing twice) | off | OTP (amr otp) | valid | session limited to step-up: WebAuthn ceremony required before any privileged API (403 `STEP_UP_REQUIRED` until done); banner "Domain verification lost" for R12 and High notification; enforcement continues until R12 confirms (no surprise lockout); session issued by the EU stack only (cookie `__Host-ge_eu`), audit and session rows written in EU | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-112 | Generic SAML IdP | SAML 2.0 | R03 executive | IN | verification lost (TXT missing twice) | on | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-113 | Microsoft Entra ID | SAML 2.0 | Custom privileged role | EU | verified | on | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-114 | Google Workspace | OIDC | R12 tenant admin | EU | unverified | off | OTP (amr otp) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-115 | Okta | OIDC | Custom privileged role | IN | verified | on | none | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-116 | Google Workspace | SAML 2.0 | R15 auditor | EU | verification lost (TXT missing twice) | on | none | valid | session created; MFA satisfied by platform policy `required_privileged` (non-privileged role); sensitive exports still step-up; banner "Domain verification lost" for R12 and High notification; enforcement continues until R12 confirms (no surprise lockout); local password sign-in for this domain returns 403 `SSO_ENFORCED`; session issued by the EU stack only (cookie `__Host-ge_eu`), audit and session rows written in EU | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-117 | Generic OIDC IdP | OIDC | R15 auditor | EU | verification lost (TXT missing twice) | off | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-118 | Google Workspace | OIDC | R02 startup head | IN | verified | on | OTP (amr otp) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-119 | Generic SAML IdP | SAML 2.0 | R12 tenant admin | EU | verified | on | OTP (amr otp) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-120 | Microsoft Entra ID | SAML 2.0 | R03 executive | EU | verified | off | none | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-121 | Generic SAML IdP | SAML 2.0 | Custom privileged role | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-122 | Generic OIDC IdP | OIDC | R02 startup head | IN | verification lost (TXT missing twice) | on | none | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-123 | Okta | OIDC | R15 auditor | IN | verified | off | OTP (amr otp) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-124 | Microsoft Entra ID | SAML 2.0 | R02 startup head | EU | unverified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-125 | Google Workspace | OIDC | R03 executive | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | valid | Home-realm discovery does not route to the tenant IdP; user is offered the local sign-in of the reused IdP only; `SSO_DOMAIN_UNVERIFIED` shown to tenant admin on A122 | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-126 | Okta | OIDC | R12 tenant admin | EU | verification lost (TXT missing twice) | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-127 | Generic SAML IdP | SAML 2.0 | R03 executive | EU | unverified | off | OTP (amr otp) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-128 | Generic OIDC IdP | OIDC | R12 tenant admin | EU | verified | off | none | valid | session limited to step-up: WebAuthn ceremony required before any privileged API (403 `STEP_UP_REQUIRED` until done); session issued by the EU stack only (cookie `__Host-ge_eu`), audit and session rows written in EU | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-129 | Generic SAML IdP | SAML 2.0 | R15 auditor | IN | verification lost (TXT missing twice) | off | OTP (amr otp) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-130 | Okta | SAML 2.0 | R03 executive | EU | verification lost (TXT missing twice) | on | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-131 | Generic OIDC IdP | OIDC | Custom privileged role | EU | unverified | off | OTP (amr otp) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-132 | Google Workspace | SAML 2.0 | R12 tenant admin | IN | unverified | off | none | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-133 | Microsoft Entra ID | SAML 2.0 | R02 startup head | IN | verified | on | OTP (amr otp) | valid | session limited to step-up: WebAuthn ceremony required before any privileged API (403 `STEP_UP_REQUIRED` until done); local password sign-in for this domain returns 403 `SSO_ENFORCED`; session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-134 | Google Workspace | OIDC | Custom privileged role | EU | verification lost (TXT missing twice) | on | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-135 | Okta | SAML 2.0 | R15 auditor | EU | verified | on | none | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-136 | Okta | OIDC | R02 startup head | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-137 | Google Workspace | SAML 2.0 | R03 executive | IN | verified | off | none | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-138 | Microsoft Entra ID | OIDC | R15 auditor | IN | unverified | off | none | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-139 | Generic OIDC IdP | OIDC | R02 startup head | EU | verified | on | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-140 | Okta | SAML 2.0 | Custom privileged role | IN | verification lost (TXT missing twice) | on | OTP (amr otp) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-141 | Microsoft Entra ID | OIDC | R03 executive | IN | verification lost (TXT missing twice) | on | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-142 | Generic SAML IdP | SAML 2.0 | R12 tenant admin | IN | verification lost (TXT missing twice) | on | none | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-143 | Generic SAML IdP | SAML 2.0 | R15 auditor | EU | unverified | off | phishing-resistant (amr hwk/webauthn) | valid | Home-realm discovery does not route to the tenant IdP; user is offered the local sign-in of the reused IdP only; `SSO_DOMAIN_UNVERIFIED` shown to tenant admin on A122 | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-144 | Microsoft Entra ID | SAML 2.0 | R15 auditor | EU | verification lost (TXT missing twice) | on | OTP (amr otp) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-145 | Microsoft Entra ID | OIDC | Custom privileged role | EU | unverified | off | none | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-146 | Generic OIDC IdP | OIDC | R12 tenant admin | IN | verification lost (TXT missing twice) | on | OTP (amr otp) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-147 | Microsoft Entra ID | SAML 2.0 | R12 tenant admin | EU | unverified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-148 | Google Workspace | SAML 2.0 | R02 startup head | EU | verification lost (TXT missing twice) | off | OTP (amr otp) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-149 | Generic OIDC IdP | OIDC | Custom privileged role | IN | verification lost (TXT missing twice) | on | phishing-resistant (amr hwk/webauthn) | valid | session created with `acr`/`amr` recorded; no step-up for 12 h (ABAC-11); banner "Domain verification lost" for R12 and High notification; enforcement continues until R12 confirms (no surprise lockout); local password sign-in for this domain returns 403 `SSO_ENFORCED`; session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-150 | Microsoft Entra ID | OIDC | R15 auditor | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-151 | Generic SAML IdP | SAML 2.0 | R02 startup head | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-152 | Generic OIDC IdP | OIDC | R03 executive | IN | unverified | off | none | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-153 | Google Workspace | OIDC | R12 tenant admin | EU | verification lost (TXT missing twice) | on | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-154 | Generic SAML IdP | SAML 2.0 | R03 executive | IN | verified | on | none | valid | session created; MFA satisfied by platform policy `required_privileged` (non-privileged role); sensitive exports still step-up; local password sign-in for this domain returns 403 `SSO_ENFORCED`; session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-155 | Okta | OIDC | R02 startup head | EU | unverified | off | none | valid | Home-realm discovery does not route to the tenant IdP; user is offered the local sign-in of the reused IdP only; `SSO_DOMAIN_UNVERIFIED` shown to tenant admin on A122 | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-156 | Google Workspace | SAML 2.0 | Custom privileged role | IN | verified | off | OTP (amr otp) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-157 | Google Workspace | OIDC | R03 executive | EU | verification lost (TXT missing twice) | on | OTP (amr otp) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-158 | Generic SAML IdP | SAML 2.0 | Custom privileged role | EU | verification lost (TXT missing twice) | off | OTP (amr otp) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-159 | Okta | SAML 2.0 | R12 tenant admin | EU | verified | off | none | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-160 | Generic SAML IdP | SAML 2.0 | R15 auditor | EU | verified | on | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-161 | Google Workspace | SAML 2.0 | R02 startup head | IN | verification lost (TXT missing twice) | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-162 | Google Workspace | OIDC | R15 auditor | IN | unverified | off | none | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-163 | Generic OIDC IdP | OIDC | R15 auditor | IN | verified | on | OTP (amr otp) | valid | session created with `acr`/`amr` recorded; no step-up for 12 h (ABAC-11); local password sign-in for this domain returns 403 `SSO_ENFORCED`; session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-164 | Okta | SAML 2.0 | R03 executive | IN | unverified | off | OTP (amr otp) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-165 | Generic OIDC IdP | OIDC | Custom privileged role | IN | verified | on | none | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-166 | Okta | OIDC | Custom privileged role | EU | unverified | off | none | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-167 | Microsoft Entra ID | OIDC | R02 startup head | IN | verification lost (TXT missing twice) | on | none | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-168 | Generic OIDC IdP | OIDC | R03 executive | EU | verified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-169 | Okta | SAML 2.0 | R12 tenant admin | IN | verification lost (TXT missing twice) | on | OTP (amr otp) | valid | session limited to step-up: WebAuthn ceremony required before any privileged API (403 `STEP_UP_REQUIRED` until done); banner "Domain verification lost" for R12 and High notification; enforcement continues until R12 confirms (no surprise lockout); session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-170 | Okta | SAML 2.0 | R15 auditor | IN | verification lost (TXT missing twice) | on | OTP (amr otp) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-171 | Google Workspace | OIDC | R12 tenant admin | IN | verified | on | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-172 | Microsoft Entra ID | SAML 2.0 | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-173 | Microsoft Entra ID | SAML 2.0 | R03 executive | EU | unverified | off | OTP (amr otp) | valid | Home-realm discovery does not route to the tenant IdP; user is offered the local sign-in of the reused IdP only; `SSO_DOMAIN_UNVERIFIED` shown to tenant admin on A122 | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-174 | Generic SAML IdP | SAML 2.0 | R12 tenant admin | IN | unverified | off | none | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-175 | Generic SAML IdP | SAML 2.0 | R02 startup head | IN | verification lost (TXT missing twice) | on | OTP (amr otp) | valid | session limited to step-up: WebAuthn ceremony required before any privileged API (403 `STEP_UP_REQUIRED` until done); banner "Domain verification lost" for R12 and High notification; enforcement continues until R12 confirms (no surprise lockout); local password sign-in for this domain returns 403 `SSO_ENFORCED`; session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-176 | Generic SAML IdP | SAML 2.0 | Custom privileged role | IN | verified | on | OTP (amr otp) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-177 | Generic OIDC IdP | OIDC | R03 executive | EU | verification lost (TXT missing twice) | off | none | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-178 | Okta | SAML 2.0 | R12 tenant admin | IN | unverified | off | none | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-179 | Okta | SAML 2.0 | R02 startup head | EU | verified | off | OTP (amr otp) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the EU region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-180 | Okta | SAML 2.0 | Custom privileged role | IN | verification lost (TXT missing twice) | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-181 | Microsoft Entra ID | SAML 2.0 | Custom privileged role | IN | verified | on | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-182 | Generic SAML IdP | SAML 2.0 | R15 auditor | IN | verification lost (TXT missing twice) | off | none | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-183 | Microsoft Entra ID | SAML 2.0 | R12 tenant admin | IN | verified | off | OTP (amr otp) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-184 | Microsoft Entra ID | SAML 2.0 | R02 startup head | IN | unverified | off | OTP (amr otp) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-185 | Google Workspace | SAML 2.0 | R03 executive | IN | verified | on | OTP (amr otp) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-186 | Google Workspace | SAML 2.0 | Custom privileged role | IN | verified | off | OTP (amr otp) | valid | session limited to step-up: WebAuthn ceremony required before any privileged API (403 `STEP_UP_REQUIRED` until done); session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-187 | Google Workspace | OIDC | Custom privileged role | IN | unverified | off | OTP (amr otp) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-188 | Generic SAML IdP | SAML 2.0 | R02 startup head | IN | verified | on | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-189 | Generic OIDC IdP | OIDC | R12 tenant admin | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-190 | Generic OIDC IdP | OIDC | R15 auditor | IN | unverified | off | none | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-191 | Okta | SAML 2.0 | R03 executive | IN | verified | off | OTP (amr otp) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-192 | Okta | SAML 2.0 | R03 executive | IN | verification lost (TXT missing twice) | off | none | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-193 | Okta | SAML 2.0 | R15 auditor | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-194 | Microsoft Entra ID | SAML 2.0 | R12 tenant admin | IN | verification lost (TXT missing twice) | off | OTP (amr otp) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-195 | Google Workspace | SAML 2.0 | R02 startup head | IN | verified | off | none | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-196 | Google Workspace | SAML 2.0 | R15 auditor | IN | unverified | off | OTP (amr otp) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-197 | Generic SAML IdP | SAML 2.0 | Custom privileged role | IN | unverified | off | none | valid | Home-realm discovery does not route to the tenant IdP; user is offered the local sign-in of the reused IdP only; `SSO_DOMAIN_UNVERIFIED` shown to tenant admin on A122 | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-198 | Generic OIDC IdP | OIDC | R15 auditor | IN | verification lost (TXT missing twice) | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-199 | Generic OIDC IdP | OIDC | Custom privileged role | IN | verification lost (TXT missing twice) | off | OTP (amr otp) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-200 | Microsoft Entra ID | SAML 2.0 | R12 tenant admin | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | valid | Home-realm discovery does not route to the tenant IdP; user is offered the local sign-in of the reused IdP only; `SSO_DOMAIN_UNVERIFIED` shown to tenant admin on A122 | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-201 | Microsoft Entra ID | SAML 2.0 | Custom privileged role | IN | unverified | off | OTP (amr otp) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-202 | Google Workspace | SAML 2.0 | R02 startup head | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | valid | Home-realm discovery does not route to the tenant IdP; user is offered the local sign-in of the reused IdP only; `SSO_DOMAIN_UNVERIFIED` shown to tenant admin on A122 | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-203 | Generic SAML IdP | SAML 2.0 | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-204 | Generic SAML IdP | SAML 2.0 | R02 startup head | IN | unverified | off | none | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-205 | Generic SAML IdP | SAML 2.0 | R15 auditor | IN | verification lost (TXT missing twice) | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-206 | Generic OIDC IdP | OIDC | R12 tenant admin | IN | unverified | off | OTP (amr otp) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-207 | Generic OIDC IdP | OIDC | R02 startup head | IN | verified | off | none | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-208 | Generic OIDC IdP | OIDC | R02 startup head | IN | unverified | off | OTP (amr otp) | valid | Home-realm discovery does not route to the tenant IdP; user is offered the local sign-in of the reused IdP only; `SSO_DOMAIN_UNVERIFIED` shown to tenant admin on A122 | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-209 | Okta | SAML 2.0 | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-210 | Okta | SAML 2.0 | R03 executive | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-211 | Okta | SAML 2.0 | R03 executive | IN | verification lost (TXT missing twice) | off | phishing-resistant (amr hwk/webauthn) | valid | session created with `acr`/`amr` recorded; no step-up for 12 h (ABAC-11); banner "Domain verification lost" for R12 and High notification; enforcement continues until R12 confirms (no surprise lockout); session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-212 | Microsoft Entra ID | SAML 2.0 | R12 tenant admin | IN | verification lost (TXT missing twice) | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-213 | Microsoft Entra ID | SAML 2.0 | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-214 | Microsoft Entra ID | SAML 2.0 | R15 auditor | IN | verified | off | none | valid | session created; MFA satisfied by platform policy `required_privileged` (non-privileged role); sensitive exports still step-up; session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-215 | Google Workspace | SAML 2.0 | R12 tenant admin | IN | unverified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-216 | Google Workspace | SAML 2.0 | R15 auditor | IN | verified | off | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-217 | Google Workspace | SAML 2.0 | R15 auditor | IN | verified | off | none | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-218 | Generic OIDC IdP | OIDC | R15 auditor | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-219 | Okta | SAML 2.0 | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-220 | Okta | SAML 2.0 | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-221 | Okta | SAML 2.0 | R02 startup head | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-222 | Okta | SAML 2.0 | R02 startup head | IN | verified | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-223 | Okta | SAML 2.0 | R15 auditor | IN | verified | off | phishing-resistant (amr hwk/webauthn) | valid | session created with `acr`/`amr` recorded; no step-up for 12 h (ABAC-11); session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-224 | Okta | SAML 2.0 | R15 auditor | IN | verified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-225 | Okta | SAML 2.0 | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | valid | session created with `acr`/`amr` recorded; no step-up for 12 h (ABAC-11); session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-226 | Okta | SAML 2.0 | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-227 | Microsoft Entra ID | SAML 2.0 | R02 startup head | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-228 | Microsoft Entra ID | SAML 2.0 | R02 startup head | IN | verified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-229 | Microsoft Entra ID | SAML 2.0 | R02 startup head | IN | verified | off | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-230 | Microsoft Entra ID | SAML 2.0 | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-231 | Microsoft Entra ID | SAML 2.0 | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-232 | Microsoft Entra ID | SAML 2.0 | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-233 | Microsoft Entra ID | SAML 2.0 | R15 auditor | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-234 | Microsoft Entra ID | SAML 2.0 | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-235 | Microsoft Entra ID | SAML 2.0 | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-236 | Google Workspace | SAML 2.0 | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | valid | session created with `acr`/`amr` recorded; no step-up for 12 h (ABAC-11); session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-237 | Google Workspace | SAML 2.0 | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-238 | Google Workspace | SAML 2.0 | R02 startup head | IN | verified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-239 | Google Workspace | SAML 2.0 | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-240 | Google Workspace | SAML 2.0 | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-241 | Google Workspace | SAML 2.0 | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-242 | Google Workspace | SAML 2.0 | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-243 | Google Workspace | SAML 2.0 | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-244 | Google Workspace | SAML 2.0 | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-245 | Generic SAML IdP | SAML 2.0 | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | valid | session created with `acr`/`amr` recorded; no step-up for 12 h (ABAC-11); session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-246 | Generic SAML IdP | SAML 2.0 | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-247 | Generic SAML IdP | SAML 2.0 | R02 startup head | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-248 | Generic SAML IdP | SAML 2.0 | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-249 | Generic SAML IdP | SAML 2.0 | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-250 | Generic SAML IdP | SAML 2.0 | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-251 | Generic SAML IdP | SAML 2.0 | R15 auditor | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-252 | Generic SAML IdP | SAML 2.0 | R15 auditor | IN | verified | off | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-253 | Generic SAML IdP | SAML 2.0 | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-254 | Generic SAML IdP | SAML 2.0 | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-255 | Generic SAML IdP | SAML 2.0 | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-256 | Generic OIDC IdP | OIDC | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-257 | Generic OIDC IdP | OIDC | R12 tenant admin | IN | verified | off | phishing-resistant (amr hwk/webauthn) | expired (NotOnOrAfter + 60 s skew passed) | 401 `SSO_ASSERTION_EXPIRED`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-258 | Generic OIDC IdP | OIDC | R02 startup head | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-259 | Generic OIDC IdP | OIDC | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | valid | session created with `acr`/`amr` recorded; no step-up for 12 h (ABAC-11); session issued by the IN stack only (cookie `__Host-ge_in`), audit and session rows written in IN | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-260 | Generic OIDC IdP | OIDC | R03 executive | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong issuer | 401 `SSO_ISSUER_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-261 | Generic OIDC IdP | OIDC | R15 auditor | IN | verified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-262 | Generic OIDC IdP | OIDC | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | wrong audience | 401 `SSO_AUDIENCE_MISMATCH`; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-263 | Generic OIDC IdP | OIDC | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | replayed assertion or code | 401 `SSO_REPLAY_DETECTED`; `identity.sso.replay` SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-264 | Generic OIDC IdP | OIDC | Custom privileged role | IN | verified | off | phishing-resistant (amr hwk/webauthn) | unsigned or alg none | 401 `SSO_SIGNATURE_INVALID`; SEV3 security event; no session cookie; audit `outcome=denied` in the IN region store; NSE | P0 | T07 | PW3 | Y | SYS |

#### Group TC-V12-R-M02: 3-way combinatorial cases – SCIM 2.0 provisioning: IdP × operation × user state × group mapping × token × region endpoint

**Common for TC-V12-R-265…TC-V12-R-382:** Pre: PP-01; SCIM base `https://api.<region>.<platform-domain>/scim/v2`; tenant token issued for the home region; IdP simulator replays the provider-specific payload shapes (Okta, Entra ID, Google). Steps: send the SCIM request in the row; read membership, session, API-key, approval-queue and outbox tables; read the AU-291 SLA record. Links for every row: TS-V12-R-02 · US-01-ZR03 · FR-V12-R-011…016; ENT-IDN-03; RFC 7643/7644; DEC-784. Technique PW (3-way); generated by `assembly/v12b/R_02_combinatorics.py` (model M02).

| ID | idp | op | user | mapping | token | endpoint | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-265 | Okta | POST create | not yet provisioned | mapped to built-in role | valid | home-region host | 201; membership `provisioned`; `identity.scim.user_provisioned` event; no role until a mapped group arrives | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-266 | Okta | POST create | active member | mapped to custom role | revoked | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-267 | Okta | PUT replace | not yet provisioned | unmapped group | expired | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-268 | Okta | PUT replace | deprovisioned | mapped to custom role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-269 | Okta | PATCH active=false | break-glass account | mapped to built-in role | other tenant | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-270 | Okta | DELETE | break-glass account | unmapped group | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-271 | Okta | PATCH group add | active member | mapped to conflicting custom role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-272 | Microsoft Entra ID | POST create | active member | unmapped group | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-273 | Microsoft Entra ID | POST create | deprovisioned | mapped to built-in role | expired | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-274 | Microsoft Entra ID | PUT replace | break-glass account | mapped to custom role | valid | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-275 | Microsoft Entra ID | PATCH active=false | not yet provisioned | mapped to custom role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-276 | Microsoft Entra ID | PATCH group add | not yet provisioned | mapped to conflicting custom role | other tenant | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-277 | Google Workspace | POST create | break-glass account | mapped to custom role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-278 | Google Workspace | PUT replace | active member | mapped to built-in role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-279 | Google Workspace | PATCH active=false | active member | unmapped group | valid | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-280 | Microsoft Entra ID | PATCH group add | deprovisioned | unmapped group | valid | home-region host | 200; group membership stored; **no role granted**; task "Map group" for R12 on A122 | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-281 | Google Workspace | DELETE | not yet provisioned | mapped to built-in role | revoked | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-282 | Google Workspace | PATCH group remove | not yet provisioned | unmapped group | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-283 | Microsoft Entra ID | PATCH group remove | deprovisioned | unmapped group | revoked | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-284 | Microsoft Entra ID | PATCH group remove | break-glass account | mapped to built-in role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-285 | Google Workspace | DELETE | deprovisioned | mapped to custom role | other tenant | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-286 | Google Workspace | PATCH group add | break-glass account | mapped to conflicting custom role | revoked | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-287 | Okta | PATCH group add | deprovisioned | mapped to conflicting custom role | valid | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-288 | Okta | PATCH group remove | active member | mapped to custom role | valid | home-region host | 200; role removed; open sessions re-evaluated within 60 s; privileged session demoted | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-289 | Microsoft Entra ID | DELETE | active member | mapped to built-in role | valid | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-290 | Google Workspace | PATCH active=false | deprovisioned | mapped to built-in role | valid | home-region host | 200/204 idempotent; no new event; nothing changes | P1 | T16 | PW3 | Y | SYS |
| TC-V12-R-291 | Google Workspace | PATCH group remove | not yet provisioned | mapped to custom role | expired | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-292 | Okta | PATCH active=false | deprovisioned | unmapped group | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-293 | Google Workspace | PATCH group add | break-glass account | mapped to built-in role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-294 | Okta | PATCH group remove | active member | mapped to built-in role | other tenant | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-295 | Microsoft Entra ID | PATCH active=false | active member | mapped to custom role | expired | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-296 | Microsoft Entra ID | DELETE | not yet provisioned | unmapped group | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-297 | Google Workspace | POST create | break-glass account | unmapped group | valid | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-298 | Okta | DELETE | break-glass account | mapped to custom role | expired | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-299 | Okta | PUT replace | deprovisioned | mapped to built-in role | revoked | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-300 | Okta | PATCH group add | not yet provisioned | mapped to custom role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-301 | Microsoft Entra ID | PUT replace | not yet provisioned | mapped to built-in role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-302 | Google Workspace | POST create | deprovisioned | unmapped group | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-303 | Google Workspace | PATCH group add | active member | unmapped group | expired | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-304 | Okta | PUT replace | break-glass account | unmapped group | valid | home-region host | 409 `mutability` "break-glass accounts are not SCIM-managed"; account unchanged; audit | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-305 | Microsoft Entra ID | PATCH active=false | break-glass account | unmapped group | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-306 | Google Workspace | PUT replace | not yet provisioned | mapped to custom role | valid | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-307 | Google Workspace | DELETE | active member | mapped to custom role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-308 | Okta | POST create | not yet provisioned | unmapped group | other tenant | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-309 | Microsoft Entra ID | PATCH group add | active member | mapped to built-in role | revoked | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-310 | Microsoft Entra ID | PATCH group remove | deprovisioned | mapped to custom role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-311 | Google Workspace | PATCH group add | not yet provisioned | mapped to conflicting custom role | valid | home-region host | 404 SCIM `noTarget`; NSE | P2 | T01 | PW3 | Y | SYS |
| TC-V12-R-312 | Okta | DELETE | deprovisioned | mapped to built-in role | valid | home-region host | 200/204 idempotent; no new event; nothing changes | P1 | T16 | PW3 | Y | SYS |
| TC-V12-R-313 | Microsoft Entra ID | PATCH group add | break-glass account | mapped to conflicting custom role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-314 | Google Workspace | PATCH active=false | not yet provisioned | mapped to built-in role | expired | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-315 | Google Workspace | PATCH active=false | deprovisioned | mapped to custom role | revoked | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-316 | Google Workspace | PATCH group add | deprovisioned | mapped to custom role | expired | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-317 | Google Workspace | PATCH group remove | break-glass account | mapped to built-in role | valid | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-318 | Okta | PUT replace | active member | unmapped group | other tenant | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-319 | Okta | PATCH group remove | break-glass account | mapped to custom role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-320 | Microsoft Entra ID | POST create | break-glass account | mapped to built-in role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-321 | Okta | PATCH active=false | active member | mapped to built-in role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-322 | Okta | PATCH group add | deprovisioned | mapped to conflicting custom role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-323 | Microsoft Entra ID | POST create | not yet provisioned | mapped to custom role | valid | home-region host | 201; membership `provisioned`; `identity.scim.user_provisioned` event; no role until a mapped group arrives | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-324 | Microsoft Entra ID | PUT replace | active member | mapped to built-in role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-325 | Microsoft Entra ID | DELETE | deprovisioned | unmapped group | other tenant | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-326 | Okta | PATCH active=false | not yet provisioned | mapped to custom role | valid | home-region host | 404 SCIM `noTarget`; NSE | P2 | T01 | PW3 | Y | SYS |
| TC-V12-R-327 | Okta | DELETE | not yet provisioned | mapped to custom role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-328 | Okta | PATCH group add | not yet provisioned | mapped to built-in role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-329 | Okta | PATCH group remove | not yet provisioned | unmapped group | valid | home-region host | 404 SCIM `noTarget`; NSE | P2 | T01 | PW3 | Y | SYS |
| TC-V12-R-330 | Microsoft Entra ID | PUT replace | not yet provisioned | unmapped group | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-331 | Microsoft Entra ID | PATCH group add | active member | mapped to conflicting custom role | valid | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-332 | Microsoft Entra ID | PATCH group add | deprovisioned | mapped to conflicting custom role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-333 | Google Workspace | POST create | active member | mapped to built-in role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-334 | Google Workspace | PUT replace | deprovisioned | unmapped group | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-335 | Google Workspace | PATCH active=false | break-glass account | mapped to custom role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-336 | Google Workspace | DELETE | break-glass account | unmapped group | valid | home-region host | 409 `mutability` "break-glass accounts are not SCIM-managed"; account unchanged; audit | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-337 | Google Workspace | PATCH group remove | active member | unmapped group | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-338 | Okta | POST create | deprovisioned | mapped to custom role | valid | home-region host | 201; membership re-activated in state `provisioned` with **no roles** until a mapped group is assigned; old API keys stay revoked | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-339 | Okta | POST create | break-glass account | unmapped group | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-340 | Okta | PATCH group add | break-glass account | mapped to custom role | valid | home-region host | 200; role from mapped to custom role granted; permission cache invalidated ≤ 60 s | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-341 | Okta | PATCH group remove | deprovisioned | mapped to built-in role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-342 | Microsoft Entra ID | PATCH active=false | deprovisioned | mapped to built-in role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-343 | Microsoft Entra ID | DELETE | active member | mapped to custom role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-344 | Microsoft Entra ID | DELETE | break-glass account | mapped to built-in role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-345 | Microsoft Entra ID | PATCH group add | active member | mapped to custom role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-346 | Microsoft Entra ID | PATCH group remove | not yet provisioned | mapped to built-in role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-347 | Google Workspace | PUT replace | break-glass account | mapped to built-in role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-348 | Google Workspace | PATCH group add | deprovisioned | mapped to conflicting custom role | expired | other-region host | 401 `invalidToken` (tokens are region-bound; lookup in the other region misses); no row read or written in either region; NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-349 | Okta | DELETE | active member | mapped to built-in role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-350 | Okta | PATCH group add | not yet provisioned | mapped to conflicting custom role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-351 | Okta | PATCH group add | not yet provisioned | unmapped group | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-352 | Microsoft Entra ID | PUT replace | deprovisioned | mapped to built-in role | valid | home-region host | 200; attributes replaced; `active` honoured; role set recomputed from mapped groups; SoD re-checked | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-353 | Microsoft Entra ID | PATCH group remove | active member | unmapped group | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-354 | Google Workspace | PATCH group add | active member | mapped to conflicting custom role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-355 | Okta | POST create | deprovisioned | mapped to custom role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-356 | Okta | PUT replace | active member | mapped to custom role | valid | home-region host | 200; attributes replaced; `active` honoured; role set recomputed from mapped groups; SoD re-checked | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-357 | Okta | PUT replace | break-glass account | mapped to custom role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-358 | Okta | PUT replace | break-glass account | mapped to custom role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-359 | Okta | PATCH active=false | not yet provisioned | unmapped group | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-360 | Okta | DELETE | not yet provisioned | mapped to custom role | valid | home-region host | 404 SCIM `noTarget`; NSE | P2 | T01 | PW3 | Y | SYS |
| TC-V12-R-361 | Okta | PATCH group add | deprovisioned | mapped to built-in role | valid | home-region host | 200; role from mapped to built-in role granted; permission cache invalidated ≤ 60 s | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-362 | Okta | PATCH group add | break-glass account | mapped to conflicting custom role | valid | home-region host | 409 `SOD_CONFLICT_ON_ASSIGNMENT`; group stored, role not granted; SoD violation event to R10 | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-363 | Okta | PATCH group add | break-glass account | unmapped group | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-364 | Okta | PATCH group remove | break-glass account | unmapped group | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-365 | Microsoft Entra ID | PATCH active=false | break-glass account | mapped to built-in role | valid | home-region host | 409 `mutability` "break-glass accounts are not SCIM-managed"; account unchanged; audit | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-366 | Microsoft Entra ID | PATCH group remove | deprovisioned | mapped to built-in role | valid | home-region host | 200; role removed; open sessions re-evaluated within 60 s; privileged session demoted | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-367 | Google Workspace | POST create | not yet provisioned | mapped to built-in role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-368 | Google Workspace | DELETE | active member | unmapped group | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-369 | Okta | POST create | not yet provisioned | mapped to built-in role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-370 | Okta | POST create | active member | mapped to built-in role | valid | home-region host | 409 SCIM `uniqueness`; no duplicate membership | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-371 | Okta | POST create | active member | mapped to built-in role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-372 | Okta | POST create | break-glass account | mapped to built-in role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-373 | Okta | PATCH active=false | not yet provisioned | mapped to built-in role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-374 | Okta | PATCH active=false | active member | mapped to built-in role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-375 | Okta | PATCH active=false | break-glass account | mapped to built-in role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-376 | Okta | PATCH active=false | break-glass account | mapped to built-in role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-377 | Okta | DELETE | deprovisioned | mapped to built-in role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-378 | Okta | DELETE | deprovisioned | mapped to built-in role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-379 | Okta | PATCH group add | not yet provisioned | mapped to conflicting custom role | expired | home-region host | 401 SCIM error `invalidToken` (expired); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-380 | Okta | PATCH group add | active member | mapped to conflicting custom role | revoked | home-region host | 401 SCIM error `invalidToken` (revoked); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-381 | Okta | PATCH group add | break-glass account | mapped to conflicting custom role | other tenant | home-region host | 401 SCIM error `invalidToken` (other tenant); NSE; `identity.scim.auth_failed` counter +1; 5 failures in 10 min → R12 notification | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-382 | Google Workspace | PATCH group remove | deprovisioned | mapped to built-in role | valid | home-region host | 200; role removed; open sessions re-evaluated within 60 s; privileged session demoted | P1 | T07 | PW3 | Y | SYS |

#### Group TC-V12-R-M03: Pairwise combinatorial cases – Custom roles and separation of duties: permission pair × path × scope × actor

**Common for TC-V12-R-383…TC-V12-R-406:** Pre: PP-01 / PP-05 (direct DB path uses the IT profile with role `app_rw` and `app.tenant_id` set). Steps: attempt the save or assignment through the path in the row; read `custom_role`, `role_permission`, `membership_role`, audit. Links for every row: TS-V12-R-03 · US-01-ZR04 · FR-V12-R-017…022; ENT-ACC-01/02; C2-T1; DEC-784. Technique PW; generated by `assembly/v12b/R_02_combinatorics.py` (model M03).

| ID | pair | path | scope | actor | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-383 | Runs:create + Runs:approve | API role save | tenant-wide | R12 tenant admin | 422 `SOD_CONFLICT` naming both permissions; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-384 | Runs:create + Runs:approve | Direct DB insert as app_rw | company-scoped | R01 founder (owned tenant) | PostgreSQL exception "separation of duties violation" from trigger `role_permission_sod` (C2-T1); transaction rolled back; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-385 | Configuration:edit + Configuration:approve | API role save | company-scoped | R13 operator support (no JIT grant) | 403 `TENANT_SCOPE_REQUIRED` (operator has no default tenant access, ENT-ACC-05); NSE | P0 | T15 | PW | Y | SYS |
| TC-V12-R-386 | Configuration:edit + Configuration:approve | Direct DB insert as app_rw | tenant-wide | Custom admin lacking billing.approve | PostgreSQL exception "separation of duties violation" from trigger `role_permission_sod` (C2-T1); transaction rolled back; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-387 | Billing:view + Billing:approve | Membership assignment of two roles | tenant-wide | R01 founder (owned tenant) | 409 `SOD_CONFLICT_ON_ASSIGNMENT` from the `membership_role` trigger and API check; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-388 | Billing:view + Billing:approve | SCIM group mapping | company-scoped | R12 tenant admin | 409 `SOD_CONFLICT_ON_ASSIGNMENT`; mapping saved as `blocked`; R10 notified; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-389 | Runs:approve + Runs:dispatch | Membership assignment of two roles | company-scoped | Custom admin lacking billing.approve | 409 `SOD_CONFLICT_ON_ASSIGNMENT` from the `membership_role` trigger and API check; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-390 | Runs:approve + Runs:dispatch | SCIM group mapping | tenant-wide | R13 operator support (no JIT grant) | 403 `TENANT_SCOPE_REQUIRED` (operator has no default tenant access, ENT-ACC-05); NSE | P0 | T15 | PW | Y | SYS |
| TC-V12-R-391 | Finance:verify_first + Finance:verify_second | API role save | tenant-wide | R01 founder (owned tenant) | 422 `SOD_CONFLICT` naming both permissions; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-392 | Finance:verify_first + Finance:verify_second | Direct DB insert as app_rw | company-scoped | R12 tenant admin | PostgreSQL exception "separation of duties violation" from trigger `role_permission_sod` (C2-T1); transaction rolled back; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-393 | Leads:read + Leads:write (no conflict) | API role save | tenant-wide | Custom admin lacking billing.approve | 201/200; role or assignment saved; `access.role.created`/`.updated`; permission cache invalidated ≤ 60 s | P1 | T01 | PW | Y | SYS |
| TC-V12-R-394 | Leads:read + Leads:write (no conflict) | Direct DB insert as app_rw | company-scoped | R13 operator support (no JIT grant) | 403 `TENANT_SCOPE_REQUIRED` (operator has no default tenant access, ENT-ACC-05); NSE | P0 | T15 | PW | Y | SYS |
| TC-V12-R-395 | Runs:create + Runs:approve | Membership assignment of two roles | tenant-wide | R13 operator support (no JIT grant) | 403 `TENANT_SCOPE_REQUIRED` (operator has no default tenant access, ENT-ACC-05); NSE | P0 | T15 | PW | Y | SYS |
| TC-V12-R-396 | Runs:create + Runs:approve | SCIM group mapping | tenant-wide | Custom admin lacking billing.approve | 409 `SOD_CONFLICT_ON_ASSIGNMENT`; mapping saved as `blocked`; R10 notified; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-397 | Configuration:edit + Configuration:approve | Membership assignment of two roles | tenant-wide | R12 tenant admin | 409 `SOD_CONFLICT_ON_ASSIGNMENT` from the `membership_role` trigger and API check; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-398 | Configuration:edit + Configuration:approve | SCIM group mapping | tenant-wide | R01 founder (owned tenant) | 409 `SOD_CONFLICT_ON_ASSIGNMENT`; mapping saved as `blocked`; R10 notified; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-399 | Billing:view + Billing:approve | API role save | tenant-wide | R13 operator support (no JIT grant) | 403 `TENANT_SCOPE_REQUIRED` (operator has no default tenant access, ENT-ACC-05); NSE | P0 | T15 | PW | Y | SYS |
| TC-V12-R-400 | Billing:view + Billing:approve | Direct DB insert as app_rw | tenant-wide | Custom admin lacking billing.approve | 403 `PERMISSION_NOT_HELD` (a role cannot grant a permission its creator lacks); NSE | P0 | T07 | PW | Y | SYS |
| TC-V12-R-401 | Runs:approve + Runs:dispatch | API role save | tenant-wide | R12 tenant admin | 422 `SOD_CONFLICT` naming both permissions; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-402 | Runs:approve + Runs:dispatch | Direct DB insert as app_rw | tenant-wide | R01 founder (owned tenant) | PostgreSQL exception "separation of duties violation" from trigger `role_permission_sod` (C2-T1); transaction rolled back; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-403 | Finance:verify_first + Finance:verify_second | Membership assignment of two roles | tenant-wide | R13 operator support (no JIT grant) | 403 `TENANT_SCOPE_REQUIRED` (operator has no default tenant access, ENT-ACC-05); NSE | P0 | T15 | PW | Y | SYS |
| TC-V12-R-404 | Finance:verify_first + Finance:verify_second | SCIM group mapping | tenant-wide | Custom admin lacking billing.approve | 409 `SOD_CONFLICT_ON_ASSIGNMENT`; mapping saved as `blocked`; R10 notified; NSE; audit `outcome=denied` rule ENT-ACC-02 | P0 | T07 | PW | Y | SYS |
| TC-V12-R-405 | Leads:read + Leads:write (no conflict) | Membership assignment of two roles | tenant-wide | R12 tenant admin | 201/200; role or assignment saved; `access.role.created`/`.updated`; permission cache invalidated ≤ 60 s | P1 | T01 | PW | Y | SYS |
| TC-V12-R-406 | Leads:read + Leads:write (no conflict) | SCIM group mapping | tenant-wide | R01 founder (owned tenant) | 201/200; role or assignment saved; `access.role.created`/`.updated`; permission cache invalidated ≤ 60 s | P1 | T01 | PW | Y | SYS |

#### Group TC-V12-R-M04: 3-way combinatorial cases – Developer API credentials: credential × state × scope × region × host × rate

**Common for TC-V12-R-407…TC-V12-R-473:** Pre: PP-01 developer host; tenant with one API key and two OAuth clients (one per auth method); RL-KEY 300/min per key. Steps: call `GET /api/v1/leads`, `POST /api/v1/leads` or `POST /api/v2/workflow-runs` as the scope column implies; read audit, rate-limit counters and outbox. Links for every row: TS-V12-R-04 · US-20-ZR06, US-20-ZR07 · FR-V12-R-031…040; ENT-API-01/02/03; DEC-785. Technique PW (3-way); generated by `assembly/v12b/R_02_combinatorics.py` (model M04).

| ID | cred | state | scope | region | host | rate | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-407 | API key gek_ | active | leads:read | home region host | developer host | under limit | 200 with masked contact fields; audit attributes `credential_id`, `API key gek_` | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-408 | API key gek_ | active | leads:write | other region host | browser host (admin/web origin) | at limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-409 | API key gek_ | expired | runs:create | home region host | browser host (admin/web origin) | over limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-410 | API key gek_ | revoked (≤ 60 s ago) | missing scope | other region host | developer host | over limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-411 | OAuth client private_key_jwt | expired | leads:read | other region host | developer host | at limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-412 | OAuth client private_key_jwt | revoked (≤ 60 s ago) | leads:write | home region host | browser host (admin/web origin) | under limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-413 | OAuth client private_key_jwt | IP not in allowlist | approve/send/pay (non-existent scope) | home region host | developer host | over limit | 403 `IP_NOT_ALLOWED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-414 | OAuth client client_secret_basic | expired | missing scope | other region host | browser host (admin/web origin) | under limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-415 | OAuth client client_secret_basic | revoked (≤ 60 s ago) | runs:create | home region host | developer host | at limit | 401 `API_KEY_REVOKED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-416 | OAuth client client_secret_basic | IP not in allowlist | leads:read | home region host | browser host (admin/web origin) | at limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-417 | OAuth client client_secret_basic | IP not in allowlist | leads:write | other region host | developer host | under limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-418 | OAuth client private_key_jwt | active | leads:read | other region host | browser host (admin/web origin) | over limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-419 | API key gek_ | IP not in allowlist | approve/send/pay (non-existent scope) | other region host | browser host (admin/web origin) | under limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-420 | OAuth client private_key_jwt | active | runs:create | other region host | developer host | under limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-421 | OAuth client private_key_jwt | active | missing scope | home region host | browser host (admin/web origin) | at limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-422 | OAuth client client_secret_basic | active | leads:write | home region host | developer host | over limit | 429 `RATE_LIMITED` + `Retry-After` + `RateLimit-Policy`; NSE; other tenants unaffected | P1 | T03 | PW3 | Y | SYS |
| TC-V12-R-423 | OAuth client client_secret_basic | revoked (≤ 60 s ago) | approve/send/pay (non-existent scope) | other region host | browser host (admin/web origin) | over limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-424 | API key gek_ | expired | approve/send/pay (non-existent scope) | home region host | developer host | at limit | 401 `API_KEY_EXPIRED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-425 | OAuth client private_key_jwt | IP not in allowlist | runs:create | other region host | browser host (admin/web origin) | at limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-426 | API key gek_ | IP not in allowlist | missing scope | home region host | developer host | under limit | 403 `IP_NOT_ALLOWED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-427 | OAuth client client_secret_basic | active | approve/send/pay (non-existent scope) | home region host | browser host (admin/web origin) | under limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-428 | API key gek_ | revoked (≤ 60 s ago) | leads:read | other region host | browser host (admin/web origin) | under limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-429 | OAuth client private_key_jwt | expired | leads:write | other region host | developer host | over limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-430 | OAuth client private_key_jwt | revoked (≤ 60 s ago) | approve/send/pay (non-existent scope) | other region host | developer host | at limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-431 | OAuth client client_secret_basic | active | missing scope | other region host | developer host | at limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-432 | OAuth client client_secret_basic | expired | leads:read | home region host | developer host | over limit | 401 `API_KEY_EXPIRED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-433 | API key gek_ | expired | leads:write | home region host | developer host | under limit | 401 `API_KEY_EXPIRED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-434 | API key gek_ | IP not in allowlist | runs:create | other region host | developer host | over limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-435 | OAuth client client_secret_basic | IP not in allowlist | missing scope | home region host | browser host (admin/web origin) | over limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-436 | API key gek_ | revoked (≤ 60 s ago) | missing scope | home region host | browser host (admin/web origin) | at limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-437 | OAuth client private_key_jwt | expired | runs:create | home region host | browser host (admin/web origin) | under limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-438 | OAuth client client_secret_basic | expired | leads:write | home region host | browser host (admin/web origin) | at limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-439 | OAuth client private_key_jwt | revoked (≤ 60 s ago) | leads:read | home region host | developer host | over limit | 401 `API_KEY_REVOKED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-440 | OAuth client client_secret_basic | revoked (≤ 60 s ago) | runs:create | other region host | browser host (admin/web origin) | under limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-441 | API key gek_ | active | approve/send/pay (non-existent scope) | other region host | developer host | over limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-442 | API key gek_ | IP not in allowlist | leads:read | other region host | developer host | at limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-443 | API key gek_ | IP not in allowlist | leads:write | home region host | browser host (admin/web origin) | over limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-444 | OAuth client private_key_jwt | expired | missing scope | home region host | developer host | over limit | 401 `API_KEY_EXPIRED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-445 | OAuth client private_key_jwt | expired | approve/send/pay (non-existent scope) | other region host | browser host (admin/web origin) | under limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-446 | API key gek_ | active | runs:create | home region host | browser host (admin/web origin) | at limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-447 | API key gek_ | revoked (≤ 60 s ago) | leads:write | other region host | developer host | at limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-448 | API key gek_ | revoked (≤ 60 s ago) | approve/send/pay (non-existent scope) | home region host | developer host | under limit | 401 `API_KEY_REVOKED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-449 | OAuth client private_key_jwt | IP not in allowlist | missing scope | other region host | developer host | under limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-450 | API key gek_ | expired | leads:read | other region host | browser host (admin/web origin) | under limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-451 | OAuth client client_secret_basic | expired | runs:create | other region host | developer host | at limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-452 | OAuth client client_secret_basic | IP not in allowlist | approve/send/pay (non-existent scope) | home region host | developer host | at limit | 403 `IP_NOT_ALLOWED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-453 | API key gek_ | IP not in allowlist | runs:create | home region host | developer host | under limit | 403 `IP_NOT_ALLOWED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-454 | OAuth client private_key_jwt | active | approve/send/pay (non-existent scope) | home region host | browser host (admin/web origin) | at limit | 401 `TOKEN_NOT_ACCEPTED_ON_BROWSER_HOST`; bearer credentials are accepted only on `api.<region>.<platform-domain>`; NSE | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-455 | OAuth client private_key_jwt | revoked (≤ 60 s ago) | runs:create | home region host | developer host | over limit | 401 `API_KEY_REVOKED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-456 | OAuth client private_key_jwt | IP not in allowlist | leads:read | home region host | developer host | under limit | 403 `IP_NOT_ALLOWED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-457 | OAuth client private_key_jwt | IP not in allowlist | leads:write | home region host | developer host | at limit | 403 `IP_NOT_ALLOWED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-458 | OAuth client client_secret_basic | active | leads:read | other region host | developer host | under limit | 401 `INVALID_CREDENTIAL` (credential registry is per region; no cross-region lookup); NSE | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-459 | OAuth client client_secret_basic | active | runs:create | home region host | developer host | over limit | 429 `RATE_LIMITED` + `Retry-After` + `RateLimit-Policy`; NSE; other tenants unaffected | P1 | T03 | PW3 | Y | SYS |
| TC-V12-R-460 | API key gek_ | active | missing scope | home region host | developer host | under limit | 403 `INSUFFICIENT_SCOPE` with `required_scope`; NSE | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-461 | API key gek_ | expired | missing scope | home region host | developer host | at limit | 401 `API_KEY_EXPIRED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-462 | API key gek_ | IP not in allowlist | leads:read | home region host | developer host | over limit | 403 `IP_NOT_ALLOWED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-463 | OAuth client private_key_jwt | active | leads:write | home region host | developer host | under limit | 201 draft record; no send; audit attributes `credential_id`, `OAuth client private_key_jwt` | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-464 | OAuth client private_key_jwt | revoked (≤ 60 s ago) | missing scope | home region host | developer host | under limit | 401 `API_KEY_REVOKED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-465 | OAuth client client_secret_basic | expired | approve/send/pay (non-existent scope) | home region host | developer host | over limit | 401 `API_KEY_EXPIRED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-466 | OAuth client client_secret_basic | revoked (≤ 60 s ago) | leads:read | home region host | developer host | at limit | 401 `API_KEY_REVOKED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-467 | OAuth client client_secret_basic | revoked (≤ 60 s ago) | leads:write | home region host | developer host | over limit | 401 `API_KEY_REVOKED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-468 | API key gek_ | active | leads:read | home region host | developer host | at limit | 200 with masked contact fields; `RateLimit: remaining=0`; audit attributes `credential_id`, `API key gek_` | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-469 | API key gek_ | active | missing scope | home region host | developer host | over limit | 403 `INSUFFICIENT_SCOPE` with `required_scope`; NSE | P1 | T07 | PW3 | Y | SYS |
| TC-V12-R-470 | API key gek_ | revoked (≤ 60 s ago) | runs:create | home region host | developer host | under limit | 401 `API_KEY_REVOKED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-471 | API key gek_ | IP not in allowlist | missing scope | home region host | developer host | at limit | 403 `IP_NOT_ALLOWED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-472 | OAuth client client_secret_basic | revoked (≤ 60 s ago) | missing scope | home region host | developer host | under limit | 401 `API_KEY_REVOKED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-473 | OAuth client client_secret_basic | IP not in allowlist | runs:create | home region host | developer host | under limit | 403 `IP_NOT_ALLOWED`; NSE; `developer.auth_failed` metric | P0 | T07 | PW3 | Y | SYS |

#### Group TC-V12-R-M05: Pairwise combinatorial cases – Outbound webhook delivery: event × endpoint response × attempt × endpoint state × region

**Common for TC-V12-R-474…TC-V12-R-497:** Pre: PP-05 with the webhook receiver simulator; endpoint secret v2 active; virtual clock. Steps: emit the event in the row; let the delivery worker run; drive the simulator response; read `webhook_delivery` rows and events. Links for every row: TS-V12-R-05 · US-20-ZR08 · FR-V12-R-041…046; ENT-API-05; DEC-785. Technique PW; generated by `assembly/v12b/R_02_combinatorics.py` (model M05).

| ID | event | response | attempt | endpoint | region | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-474 | lead.created | 2xx within 10 s | 1 | verified | IN | `developer.webhook_delivery.succeeded`; attempt 1 recorded with signature timestamp; no further attempts | P1 | T16 | PW | Y | SYS |
| TC-V12-R-475 | lead.created | 5xx | 3 | unverified (challenge not passed) | EU | No delivery; event retained 7 days in the outbox projection; endpoint shows "Verify endpoint"; NSE at the receiver | P1 | T01 | PW | Y | SYS |
| TC-V12-R-476 | run.awaiting_approval | timeout > 10 s | 6 | verified | EU | `developer.webhook_delivery.exhausted` after attempt 6 (≤ 24 h after first); endpoint flagged; replay available from A125 for 30 days | P1 | T18 | PW | Y | SYS |
| TC-V12-R-477 | invoice.issued | 410 Gone | 6 | unverified (challenge not passed) | IN | No delivery; event retained 7 days in the outbox projection; endpoint shows "Verify endpoint"; NSE at the receiver | P1 | T01 | PW | Y | SYS |
| TC-V12-R-478 | connector.degraded | TLS failure | 1 | unverified (challenge not passed) | EU | No delivery; event retained 7 days in the outbox projection; endpoint shows "Verify endpoint"; NSE at the receiver | P1 | T01 | PW | Y | SYS |
| TC-V12-R-479 | connector.degraded | 3xx redirect | 3 | verified | IN | `developer.webhook_delivery.failed`; next attempt 4 at T+2 h ±10% jitter; redirects not followed; same `event_id`, new signature timestamp | P1 | T18 | PW | Y | SYS |
| TC-V12-R-480 | run.awaiting_approval | 2xx within 10 s | 3 | unverified (challenge not passed) | IN | No delivery; event retained 7 days in the outbox projection; endpoint shows "Verify endpoint"; NSE at the receiver | P1 | T01 | PW | Y | SYS |
| TC-V12-R-481 | invoice.issued | 5xx | 1 | verified | IN | `developer.webhook_delivery.failed`; next attempt 2 at T+5 min ±10% jitter; redirects not followed; same `event_id`, new signature timestamp | P1 | T18 | PW | Y | SYS |
| TC-V12-R-482 | lead.created | TLS failure | 6 | verified | IN | `developer.webhook_delivery.exhausted` after attempt 6 (≤ 24 h after first); endpoint flagged; replay available from A125 for 30 days | P1 | T18 | PW | Y | SYS |
| TC-V12-R-483 | run.awaiting_approval | 410 Gone | 1 | verified | EU | Endpoint disabled immediately (`developer.webhook_endpoint.disabled`, reason 410); no retry; R12 notified | P1 | T01 | PW | Y | SYS |
| TC-V12-R-484 | invoice.issued | timeout > 10 s | 3 | unverified (challenge not passed) | IN | No delivery; event retained 7 days in the outbox projection; endpoint shows "Verify endpoint"; NSE at the receiver | P1 | T01 | PW | Y | SYS |
| TC-V12-R-485 | invoice.issued | 3xx redirect | 1 | unverified (challenge not passed) | EU | No delivery; event retained 7 days in the outbox projection; endpoint shows "Verify endpoint"; NSE at the receiver | P1 | T01 | PW | Y | SYS |
| TC-V12-R-486 | connector.degraded | 2xx within 10 s | 6 | verified | EU | `developer.webhook_delivery.succeeded`; attempt 6 recorded with signature timestamp; no further attempts | P1 | T16 | PW | Y | SYS |
| TC-V12-R-487 | lead.created | timeout > 10 s | 1 | verified | IN | `developer.webhook_delivery.failed`; next attempt 2 at T+5 min ±10% jitter; redirects not followed; same `event_id`, new signature timestamp | P1 | T18 | PW | Y | SYS |
| TC-V12-R-488 | lead.created | 410 Gone | 3 | verified | IN | Endpoint disabled immediately (`developer.webhook_endpoint.disabled`, reason 410); no retry; R12 notified | P1 | T01 | PW | Y | SYS |
| TC-V12-R-489 | lead.created | 3xx redirect | 6 | verified | IN | `developer.webhook_delivery.exhausted` after attempt 6 (≤ 24 h after first); endpoint flagged; replay available from A125 for 30 days | P1 | T18 | PW | Y | SYS |
| TC-V12-R-490 | run.awaiting_approval | 5xx | 6 | verified | IN | `developer.webhook_delivery.exhausted` after attempt 6 (≤ 24 h after first); endpoint flagged; replay available from A125 for 30 days | P1 | T18 | PW | Y | SYS |
| TC-V12-R-491 | run.awaiting_approval | TLS failure | 3 | verified | IN | `developer.webhook_delivery.failed`; next attempt 4 at T+2 h ±10% jitter; redirects not followed; same `event_id`, new signature timestamp | P1 | T18 | PW | Y | SYS |
| TC-V12-R-492 | run.awaiting_approval | 3xx redirect | 1 | verified | IN | `developer.webhook_delivery.failed`; next attempt 2 at T+5 min ±10% jitter; redirects not followed; same `event_id`, new signature timestamp | P1 | T18 | PW | Y | SYS |
| TC-V12-R-493 | invoice.issued | 2xx within 10 s | 1 | verified | IN | `developer.webhook_delivery.succeeded`; attempt 1 recorded with signature timestamp; no further attempts | P1 | T16 | PW | Y | SYS |
| TC-V12-R-494 | invoice.issued | TLS failure | 1 | verified | IN | `developer.webhook_delivery.failed`; next attempt 2 at T+5 min ±10% jitter; redirects not followed; same `event_id`, new signature timestamp | P1 | T18 | PW | Y | SYS |
| TC-V12-R-495 | connector.degraded | 5xx | 1 | verified | IN | `developer.webhook_delivery.failed`; next attempt 2 at T+5 min ±10% jitter; redirects not followed; same `event_id`, new signature timestamp | P1 | T18 | PW | Y | SYS |
| TC-V12-R-496 | connector.degraded | timeout > 10 s | 1 | verified | IN | `developer.webhook_delivery.failed`; next attempt 2 at T+5 min ±10% jitter; redirects not followed; same `event_id`, new signature timestamp | P1 | T18 | PW | Y | SYS |
| TC-V12-R-497 | connector.degraded | 410 Gone | 1 | verified | IN | Endpoint disabled immediately (`developer.webhook_endpoint.disabled`, reason 410); no retry; R12 notified | P1 | T01 | PW | Y | SYS |

#### Group TC-V12-R-M06: Pairwise combinatorial cases – Webhook signature verification in the SDKs: timestamp × signature × replay (exhaustive)

**Common for TC-V12-R-498…TC-V12-R-537:** Pre: PP-04 unit profile; SDK under test (TypeScript, Python and Java each run the same table); header `GE-Signature: t=<unix>,v1=<hex HMAC-SHA256(secret, t + "." + body)>`. Steps: call `verify(headers, body, secrets)`; then the sample receiver. Links for every row: TS-V12-R-06 · US-20-ZR08, US-20-ZR10 · FR-V12-R-042, 052; ENT-API-05/06. Technique PW and exhaustive; generated by `assembly/v12b/R_02_combinatorics.py` (model M06).

| ID | timestamp | signature | replay | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-498 | fresh | valid current secret | first delivery | SDK `verify()` returns the parsed event; receiver processes once | P1 | T01 | EXH | Y | UT |
| TC-V12-R-499 | fresh | valid current secret | duplicate event_id | SDK verifies; receiver idempotency store returns 200 "already processed"; no second effect | P0 | T16 | EXH | Y | UT |
| TC-V12-R-500 | fresh | valid previous secret within 24 h overlap | first delivery | SDK `verify()` returns the parsed event; receiver processes once | P1 | T01 | EXH | Y | UT |
| TC-V12-R-501 | fresh | valid previous secret within 24 h overlap | duplicate event_id | SDK verifies; receiver idempotency store returns 200 "already processed"; no second effect | P0 | T16 | EXH | Y | UT |
| TC-V12-R-502 | fresh | previous secret after 24 h overlap | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-503 | fresh | previous secret after 24 h overlap | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-504 | fresh | tampered body | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-505 | fresh | tampered body | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-506 | fresh | wrong secret | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-507 | fresh | wrong secret | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-508 | 299 s old | valid current secret | first delivery | SDK `verify()` returns the parsed event; receiver processes once | P1 | T01 | EXH | Y | UT |
| TC-V12-R-509 | 299 s old | valid current secret | duplicate event_id | SDK verifies; receiver idempotency store returns 200 "already processed"; no second effect | P0 | T16 | EXH | Y | UT |
| TC-V12-R-510 | 299 s old | valid previous secret within 24 h overlap | first delivery | SDK `verify()` returns the parsed event; receiver processes once | P1 | T01 | EXH | Y | UT |
| TC-V12-R-511 | 299 s old | valid previous secret within 24 h overlap | duplicate event_id | SDK verifies; receiver idempotency store returns 200 "already processed"; no second effect | P0 | T16 | EXH | Y | UT |
| TC-V12-R-512 | 299 s old | previous secret after 24 h overlap | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-513 | 299 s old | previous secret after 24 h overlap | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-514 | 299 s old | tampered body | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-515 | 299 s old | tampered body | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-516 | 299 s old | wrong secret | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-517 | 299 s old | wrong secret | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-518 | 301 s old | valid current secret | first delivery | SDK `verify()` raises `TimestampOutsideTolerance` (±300 s) | P0 | T07 | EXH | Y | UT |
| TC-V12-R-519 | 301 s old | valid current secret | duplicate event_id | SDK `verify()` raises `TimestampOutsideTolerance` (±300 s) | P0 | T07 | EXH | Y | UT |
| TC-V12-R-520 | 301 s old | valid previous secret within 24 h overlap | first delivery | SDK `verify()` raises `TimestampOutsideTolerance` (±300 s) | P0 | T07 | EXH | Y | UT |
| TC-V12-R-521 | 301 s old | valid previous secret within 24 h overlap | duplicate event_id | SDK `verify()` raises `TimestampOutsideTolerance` (±300 s) | P0 | T07 | EXH | Y | UT |
| TC-V12-R-522 | 301 s old | previous secret after 24 h overlap | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-523 | 301 s old | previous secret after 24 h overlap | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-524 | 301 s old | tampered body | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-525 | 301 s old | tampered body | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-526 | 301 s old | wrong secret | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-527 | 301 s old | wrong secret | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-528 | 301 s in the future | valid current secret | first delivery | SDK `verify()` raises `TimestampOutsideTolerance` (±300 s) | P0 | T07 | EXH | Y | UT |
| TC-V12-R-529 | 301 s in the future | valid current secret | duplicate event_id | SDK `verify()` raises `TimestampOutsideTolerance` (±300 s) | P0 | T07 | EXH | Y | UT |
| TC-V12-R-530 | 301 s in the future | valid previous secret within 24 h overlap | first delivery | SDK `verify()` raises `TimestampOutsideTolerance` (±300 s) | P0 | T07 | EXH | Y | UT |
| TC-V12-R-531 | 301 s in the future | valid previous secret within 24 h overlap | duplicate event_id | SDK `verify()` raises `TimestampOutsideTolerance` (±300 s) | P0 | T07 | EXH | Y | UT |
| TC-V12-R-532 | 301 s in the future | previous secret after 24 h overlap | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-533 | 301 s in the future | previous secret after 24 h overlap | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-534 | 301 s in the future | tampered body | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-535 | 301 s in the future | tampered body | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-536 | 301 s in the future | wrong secret | first delivery | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |
| TC-V12-R-537 | 301 s in the future | wrong secret | duplicate event_id | SDK `verify()` raises `SignatureInvalid`; receiver returns 400; sender counts a failure | P0 | T07 | EXH | Y | UT |

#### Group TC-V12-R-M07: 3-way combinatorial cases – Connectors: connector × auth × failure mode × residency × environment × activation gate

**Common for TC-V12-R-538…TC-V12-R-721:** Pre: PP-05 with provider simulators for Salesforce, HubSpot, Zoho CRM, the SMS-DLT aggregator and the voice CPaaS; installation in the row environment; credential reference in Secrets Manager (region of the tenant). Steps: request activation (production rows) then trigger one sync or send; drive the failure mode from the simulator; read installation state, effect ledger, exception queue and events. Links for every row: TS-V12-R-07 · US-18-ZR11, US-07-ZR12, US-07-ZR13, US-23-ZR14, US-22-ZR15 · FR-V12-R-056…080; ENT-INT-01…05; INT-01/04/05; CJ-IN-06/07; DEC-785. Technique PW (3-way); generated by `assembly/v12b/R_02_combinatorics.py` (model M07).

| ID | connector | auth | failure | residency | env | gate | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-538 | Salesforce | OAuth 2.0 auth code + PKCE | none | IN | sandbox | complete | Sandbox adapter and provider test account only; upsert by external ID; sync cursor advanced; consent and approvals remain platform-owned; data stays in the IN zone except fields listed in the transfer entry | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-539 | Salesforce | OAuth 2.0 auth code + PKCE | 429 throttled | EU | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-540 | Salesforce | OAuth 2.0 client credentials / JWT bearer | 5xx | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-541 | HubSpot | OAuth 2.0 auth code + PKCE | 401 token revoked | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-542 | HubSpot | OAuth 2.0 client credentials / JWT bearer | none | EU | production | complete | upsert by external ID; sync cursor advanced; consent and approvals remain platform-owned; data stays in the EU zone except fields listed in the transfer entry | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-543 | SMS-DLT aggregator | API key in vault | none | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-544 | SMS-DLT aggregator | API key in vault | 429 throttled | EU | sandbox | complete | Sandbox adapter and provider test account only; retry with backoff and jitter within the per-connector budget; breaker stays closed | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-545 | Voice CPaaS (140/160 series) | API key in vault | 5xx | EU | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-546 | Zoho CRM | OAuth 2.0 auth code + PKCE | timeout on write (uncertain) | EU | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-547 | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | 401 token revoked | IN | sandbox | complete | Sandbox adapter and provider test account only; installation `Disabled` after 3 consecutive 401; R12 task "Reconnect"; no further calls | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-548 | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | validation 4xx | EU | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-549 | Voice CPaaS (140/160 series) | API key in vault | timeout on write (uncertain) | IN | sandbox | complete | Sandbox adapter and provider test account only; effect marked `Uncertain`; reconcile by external ID/message reference before any retry; never a duplicate write | P0 | T18 | PW3 | Y | SYS |
| TC-V12-R-550 | HubSpot | OAuth 2.0 auth code + PKCE | 5xx | EU | sandbox | complete | Sandbox adapter and provider test account only; retry 3 times; breaker opens at 50% errors over 20 calls; connector `Degraded`; AU-295 alert | P1 | T21 | PW3 | Y | SYS |
| TC-V12-R-551 | Salesforce | OAuth 2.0 client credentials / JWT bearer | missed provider event (gap) | EU | sandbox | complete | Sandbox adapter and provider test account only; gap detected by cursor/sequence; repair fetch; no duplicate record | P1 | T16 | PW3 | Y | SYS |
| TC-V12-R-552 | HubSpot | OAuth 2.0 client credentials / JWT bearer | timeout on write (uncertain) | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-553 | Zoho CRM | OAuth 2.0 auth code + PKCE | missed provider event (gap) | IN | production | complete | gap detected by cursor/sequence; repair fetch; no duplicate record | P1 | T16 | PW3 | Y | SYS |
| TC-V12-R-554 | SMS-DLT aggregator | API key in vault | 401 token revoked | EU | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-555 | Voice CPaaS (140/160 series) | API key in vault | 429 throttled | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-556 | SMS-DLT aggregator | API key in vault | validation 4xx | IN | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-557 | SMS-DLT aggregator | API key in vault | DLT template mismatch | EU | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-558 | Voice CPaaS (140/160 series) | API key in vault | DND/preference-registry hit | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-559 | Voice CPaaS (140/160 series) | API key in vault | missed provider event (gap) | EU | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-560 | HubSpot | OAuth 2.0 auth code + PKCE | validation 4xx | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-561 | Zoho CRM | OAuth 2.0 auth code + PKCE | 5xx | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-562 | Salesforce | OAuth 2.0 auth code + PKCE | none | EU | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-563 | HubSpot | OAuth 2.0 client credentials / JWT bearer | 429 throttled | IN | sandbox | complete | Sandbox adapter and provider test account only; retry with backoff and jitter within the per-connector budget; breaker stays closed | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-564 | Zoho CRM | OAuth 2.0 auth code + PKCE | validation 4xx | EU | sandbox | complete | Sandbox adapter and provider test account only; permanent failure; record to exception queue with field errors; no retry | P2 | T01 | PW3 | Y | SYS |
| TC-V12-R-565 | Salesforce | OAuth 2.0 client credentials / JWT bearer | 401 token revoked | EU | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-566 | Salesforce | OAuth 2.0 client credentials / JWT bearer | missed provider event (gap) | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-567 | HubSpot | OAuth 2.0 client credentials / JWT bearer | 429 throttled | EU | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-568 | SMS-DLT aggregator | API key in vault | 5xx | IN | sandbox | complete | Sandbox adapter and provider test account only; retry 3 times; breaker opens at 50% errors over 20 calls; connector `Degraded`; AU-295 alert | P1 | T21 | PW3 | Y | SYS |
| TC-V12-R-569 | SMS-DLT aggregator | API key in vault | DND/preference-registry hit | EU | production | complete | HOLD `REGISTRY_SCRUB_BLOCKED`; promotional message not sent; transactional allowed only on service series | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-570 | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | none | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-571 | SMS-DLT aggregator | API key in vault | timeout on write (uncertain) | EU | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-572 | Voice CPaaS (140/160 series) | API key in vault | none | EU | sandbox | complete | Sandbox adapter and provider test account only; call placed from the correct number series; status webhook reconciled; data stays in the EU zone except fields listed in the transfer entry | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-573 | Salesforce | OAuth 2.0 client credentials / JWT bearer | timeout on write (uncertain) | EU | sandbox | complete | Sandbox adapter and provider test account only; effect marked `Uncertain`; reconcile by external ID/message reference before any retry; never a duplicate write | P0 | T18 | PW3 | Y | SYS |
| TC-V12-R-574 | Salesforce | OAuth 2.0 client credentials / JWT bearer | validation 4xx | IN | sandbox | complete | Sandbox adapter and provider test account only; permanent failure; record to exception queue with field errors; no retry | P2 | T01 | PW3 | Y | SYS |
| TC-V12-R-575 | HubSpot | OAuth 2.0 client credentials / JWT bearer | 5xx | EU | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-576 | SMS-DLT aggregator | API key in vault | DLT template mismatch | IN | sandbox | complete | Sandbox adapter and provider test account only; HOLD `DLT_TEMPLATE_MISMATCH` before dispatch (PDP); no SMS sent; template task to R10 | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-577 | SMS-DLT aggregator | API key in vault | missed provider event (gap) | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-578 | Voice CPaaS (140/160 series) | API key in vault | 401 token revoked | IN | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-579 | Salesforce | OAuth 2.0 auth code + PKCE | 401 token revoked | EU | sandbox | complete | Sandbox adapter and provider test account only; installation `Disabled` after 3 consecutive 401; R12 task "Reconnect"; no further calls | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-580 | Salesforce | OAuth 2.0 auth code + PKCE | timeout on write (uncertain) | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-581 | HubSpot | OAuth 2.0 auth code + PKCE | missed provider event (gap) | EU | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-582 | Zoho CRM | OAuth 2.0 auth code + PKCE | 429 throttled | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-583 | Voice CPaaS (140/160 series) | API key in vault | validation 4xx | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-584 | Salesforce | OAuth 2.0 auth code + PKCE | validation 4xx | EU | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-585 | HubSpot | OAuth 2.0 auth code + PKCE | timeout on write (uncertain) | EU | sandbox | complete | Sandbox adapter and provider test account only; effect marked `Uncertain`; reconcile by external ID/message reference before any retry; never a duplicate write | P0 | T18 | PW3 | Y | SYS |
| TC-V12-R-586 | Zoho CRM | OAuth 2.0 auth code + PKCE | none | EU | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-587 | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | 5xx | EU | sandbox | complete | Sandbox adapter and provider test account only; retry 3 times; breaker opens at 50% errors over 20 calls; connector `Degraded`; AU-295 alert | P1 | T21 | PW3 | Y | SYS |
| TC-V12-R-588 | SMS-DLT aggregator | API key in vault | 429 throttled | IN | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-589 | SMS-DLT aggregator | API key in vault | 5xx | EU | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-590 | SMS-DLT aggregator | API key in vault | validation 4xx | EU | sandbox | complete | Sandbox adapter and provider test account only; permanent failure; record to exception queue with field errors; no retry | P2 | T01 | PW3 | Y | SYS |
| TC-V12-R-591 | SMS-DLT aggregator | API key in vault | DND/preference-registry hit | IN | sandbox | complete | Sandbox adapter and provider test account only; HOLD `REGISTRY_SCRUB_BLOCKED`; promotional message not sent; transactional allowed only on service series | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-592 | Voice CPaaS (140/160 series) | API key in vault | none | IN | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-593 | Voice CPaaS (140/160 series) | API key in vault | timeout on write (uncertain) | EU | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-594 | Voice CPaaS (140/160 series) | API key in vault | missed provider event (gap) | IN | sandbox | complete | Sandbox adapter and provider test account only; gap detected by cursor/sequence; repair fetch; no duplicate record | P1 | T16 | PW3 | Y | SYS |
| TC-V12-R-595 | Salesforce | OAuth 2.0 auth code + PKCE | 429 throttled | IN | sandbox | complete | Sandbox adapter and provider test account only; retry with backoff and jitter within the per-connector budget; breaker stays closed | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-596 | Salesforce | OAuth 2.0 auth code + PKCE | 5xx | EU | production | complete | retry 3 times; breaker opens at 50% errors over 20 calls; connector `Degraded`; AU-295 alert | P1 | T21 | PW3 | Y | SYS |
| TC-V12-R-597 | HubSpot | OAuth 2.0 client credentials / JWT bearer | validation 4xx | EU | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-598 | Zoho CRM | OAuth 2.0 auth code + PKCE | 401 token revoked | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-599 | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | 429 throttled | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-600 | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | missed provider event (gap) | EU | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-601 | SMS-DLT aggregator | API key in vault | 401 token revoked | IN | sandbox | complete | Sandbox adapter and provider test account only; installation `Disabled` after 3 consecutive 401; R12 task "Reconnect"; no further calls | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-602 | SMS-DLT aggregator | API key in vault | DLT template mismatch | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-603 | SMS-DLT aggregator | API key in vault | DND/preference-registry hit | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-604 | SMS-DLT aggregator | API key in vault | missed provider event (gap) | EU | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-605 | Voice CPaaS (140/160 series) | API key in vault | DND/preference-registry hit | EU | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-606 | Salesforce | OAuth 2.0 auth code + PKCE | 401 token revoked | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-607 | Salesforce | OAuth 2.0 auth code + PKCE | missed provider event (gap) | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-608 | Salesforce | OAuth 2.0 client credentials / JWT bearer | 429 throttled | EU | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-609 | HubSpot | OAuth 2.0 auth code + PKCE | none | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-610 | HubSpot | OAuth 2.0 auth code + PKCE | missed provider event (gap) | IN | sandbox | complete | Sandbox adapter and provider test account only; gap detected by cursor/sequence; repair fetch; no duplicate record | P1 | T16 | PW3 | Y | SYS |
| TC-V12-R-611 | HubSpot | OAuth 2.0 client credentials / JWT bearer | 401 token revoked | EU | sandbox | complete | Sandbox adapter and provider test account only; installation `Disabled` after 3 consecutive 401; R12 task "Reconnect"; no further calls | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-612 | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | 401 token revoked | EU | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-613 | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | timeout on write (uncertain) | IN | sandbox | complete | Sandbox adapter and provider test account only; effect marked `Uncertain`; reconcile by external ID/message reference before any retry; never a duplicate write | P0 | T18 | PW3 | Y | SYS |
| TC-V12-R-614 | SMS-DLT aggregator | API key in vault | none | EU | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-615 | SMS-DLT aggregator | API key in vault | timeout on write (uncertain) | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-616 | SMS-DLT aggregator | API key in vault | DLT template mismatch | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-617 | SMS-DLT aggregator | API key in vault | DLT template mismatch | IN | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-618 | SMS-DLT aggregator | API key in vault | DND/preference-registry hit | IN | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-619 | Voice CPaaS (140/160 series) | API key in vault | 429 throttled | EU | production | complete | retry with backoff and jitter within the per-connector budget; breaker stays closed | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-620 | Voice CPaaS (140/160 series) | API key in vault | 5xx | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-621 | Voice CPaaS (140/160 series) | API key in vault | 5xx | EU | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-622 | Salesforce | OAuth 2.0 auth code + PKCE | 429 throttled | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-623 | Salesforce | OAuth 2.0 auth code + PKCE | timeout on write (uncertain) | EU | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-624 | Salesforce | OAuth 2.0 auth code + PKCE | validation 4xx | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-625 | Salesforce | OAuth 2.0 client credentials / JWT bearer | none | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-626 | HubSpot | OAuth 2.0 auth code + PKCE | 5xx | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-627 | HubSpot | OAuth 2.0 auth code + PKCE | missed provider event (gap) | EU | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-628 | HubSpot | OAuth 2.0 client credentials / JWT bearer | none | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-629 | Zoho CRM | OAuth 2.0 auth code + PKCE | 429 throttled | EU | sandbox | complete | Sandbox adapter and provider test account only; retry with backoff and jitter within the per-connector budget; breaker stays closed | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-630 | Zoho CRM | OAuth 2.0 auth code + PKCE | validation 4xx | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-631 | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | none | IN | sandbox | complete | Sandbox adapter and provider test account only; upsert by external ID; sync cursor advanced; consent and approvals remain platform-owned; data stays in the IN zone except fields listed in the transfer entry | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-632 | Voice CPaaS (140/160 series) | API key in vault | 401 token revoked | EU | sandbox | complete | Sandbox adapter and provider test account only; installation `Disabled` after 3 consecutive 401; R12 task "Reconnect"; no further calls | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-633 | Voice CPaaS (140/160 series) | API key in vault | validation 4xx | EU | sandbox | complete | Sandbox adapter and provider test account only; permanent failure; record to exception queue with field errors; no retry | P2 | T01 | PW3 | Y | SYS |
| TC-V12-R-634 | Voice CPaaS (140/160 series) | API key in vault | DND/preference-registry hit | EU | sandbox | complete | Sandbox adapter and provider test account only; HOLD `REGISTRY_SCRUB_BLOCKED`; promotional message not sent; transactional allowed only on service series | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-635 | Salesforce | OAuth 2.0 auth code + PKCE | 5xx | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-636 | Salesforce | OAuth 2.0 auth code + PKCE | missed provider event (gap) | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-637 | Salesforce | OAuth 2.0 client credentials / JWT bearer | 5xx | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-638 | Salesforce | OAuth 2.0 client credentials / JWT bearer | timeout on write (uncertain) | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-639 | HubSpot | OAuth 2.0 auth code + PKCE | 429 throttled | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-640 | HubSpot | OAuth 2.0 auth code + PKCE | validation 4xx | IN | sandbox | complete | Sandbox adapter and provider test account only; permanent failure; record to exception queue with field errors; no retry | P2 | T01 | PW3 | Y | SYS |
| TC-V12-R-641 | HubSpot | OAuth 2.0 client credentials / JWT bearer | 401 token revoked | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-642 | HubSpot | OAuth 2.0 client credentials / JWT bearer | timeout on write (uncertain) | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-643 | HubSpot | OAuth 2.0 client credentials / JWT bearer | missed provider event (gap) | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-644 | Zoho CRM | OAuth 2.0 client credentials / JWT bearer | validation 4xx | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-645 | SMS-DLT aggregator | API key in vault | none | IN | sandbox | complete | Sandbox adapter and provider test account only; SMS submitted with entity, header and template IDs; delivery report reconciled; data stays in the IN zone except fields listed in the transfer entry | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-646 | SMS-DLT aggregator | API key in vault | none | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-647 | SMS-DLT aggregator | API key in vault | none | EU | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-648 | SMS-DLT aggregator | API key in vault | 429 throttled | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-649 | SMS-DLT aggregator | API key in vault | 429 throttled | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-650 | SMS-DLT aggregator | API key in vault | 5xx | IN | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-651 | SMS-DLT aggregator | API key in vault | 401 token revoked | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-652 | SMS-DLT aggregator | API key in vault | 401 token revoked | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-653 | SMS-DLT aggregator | API key in vault | 401 token revoked | EU | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-654 | SMS-DLT aggregator | API key in vault | timeout on write (uncertain) | IN | sandbox | complete | Sandbox adapter and provider test account only; effect marked `Uncertain`; reconcile by external ID/message reference before any retry; never a duplicate write | P0 | T18 | PW3 | Y | SYS |
| TC-V12-R-655 | SMS-DLT aggregator | API key in vault | timeout on write (uncertain) | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-656 | SMS-DLT aggregator | API key in vault | validation 4xx | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-657 | SMS-DLT aggregator | API key in vault | validation 4xx | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-658 | SMS-DLT aggregator | API key in vault | DLT template mismatch | EU | sandbox | complete | Sandbox adapter and provider test account only; HOLD `DLT_TEMPLATE_MISMATCH` before dispatch (PDP); no SMS sent; template task to R10 | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-659 | SMS-DLT aggregator | API key in vault | DND/preference-registry hit | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-660 | SMS-DLT aggregator | API key in vault | DND/preference-registry hit | EU | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-661 | SMS-DLT aggregator | API key in vault | missed provider event (gap) | IN | sandbox | complete | Sandbox adapter and provider test account only; gap detected by cursor/sequence; repair fetch; no duplicate record | P1 | T16 | PW3 | Y | SYS |
| TC-V12-R-662 | SMS-DLT aggregator | API key in vault | missed provider event (gap) | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-663 | Voice CPaaS (140/160 series) | API key in vault | 429 throttled | EU | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-664 | Voice CPaaS (140/160 series) | API key in vault | 5xx | IN | sandbox | complete | Sandbox adapter and provider test account only; retry 3 times; breaker opens at 50% errors over 20 calls; connector `Degraded`; AU-295 alert | P1 | T21 | PW3 | Y | SYS |
| TC-V12-R-665 | Voice CPaaS (140/160 series) | API key in vault | timeout on write (uncertain) | IN | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-666 | Voice CPaaS (140/160 series) | API key in vault | validation 4xx | EU | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-667 | Voice CPaaS (140/160 series) | API key in vault | DND/preference-registry hit | EU | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-668 | Voice CPaaS (140/160 series) | API key in vault | DND/preference-registry hit | EU | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-669 | Voice CPaaS (140/160 series) | API key in vault | missed provider event (gap) | IN | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-670 | Salesforce | OAuth 2.0 auth code + PKCE | none | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-671 | Salesforce | OAuth 2.0 auth code + PKCE | 5xx | IN | sandbox | complete | Sandbox adapter and provider test account only; retry 3 times; breaker opens at 50% errors over 20 calls; connector `Degraded`; AU-295 alert | P1 | T21 | PW3 | Y | SYS |
| TC-V12-R-672 | Salesforce | OAuth 2.0 auth code + PKCE | 401 token revoked | IN | production | complete | installation `Disabled` after 3 consecutive 401; R12 task "Reconnect"; no further calls | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-673 | Salesforce | OAuth 2.0 auth code + PKCE | 401 token revoked | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-674 | Salesforce | OAuth 2.0 auth code + PKCE | timeout on write (uncertain) | IN | production | complete | effect marked `Uncertain`; reconcile by external ID/message reference before any retry; never a duplicate write | P0 | T18 | PW3 | Y | SYS |
| TC-V12-R-675 | Salesforce | OAuth 2.0 auth code + PKCE | validation 4xx | IN | production | complete | permanent failure; record to exception queue with field errors; no retry | P2 | T01 | PW3 | Y | SYS |
| TC-V12-R-676 | Salesforce | OAuth 2.0 auth code + PKCE | validation 4xx | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-677 | HubSpot | OAuth 2.0 auth code + PKCE | none | IN | sandbox | complete | Sandbox adapter and provider test account only; upsert by external ID; sync cursor advanced; consent and approvals remain platform-owned; data stays in the IN zone except fields listed in the transfer entry | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-678 | HubSpot | OAuth 2.0 auth code + PKCE | none | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-679 | HubSpot | OAuth 2.0 auth code + PKCE | 429 throttled | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-680 | HubSpot | OAuth 2.0 auth code + PKCE | 5xx | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-681 | HubSpot | OAuth 2.0 auth code + PKCE | 401 token revoked | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-682 | HubSpot | OAuth 2.0 auth code + PKCE | timeout on write (uncertain) | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-683 | HubSpot | OAuth 2.0 auth code + PKCE | validation 4xx | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-684 | HubSpot | OAuth 2.0 auth code + PKCE | missed provider event (gap) | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-685 | Zoho CRM | OAuth 2.0 auth code + PKCE | none | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-686 | Zoho CRM | OAuth 2.0 auth code + PKCE | 429 throttled | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-687 | Zoho CRM | OAuth 2.0 auth code + PKCE | 5xx | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-688 | Zoho CRM | OAuth 2.0 auth code + PKCE | 5xx | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-689 | Zoho CRM | OAuth 2.0 auth code + PKCE | 401 token revoked | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-690 | Zoho CRM | OAuth 2.0 auth code + PKCE | timeout on write (uncertain) | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-691 | Zoho CRM | OAuth 2.0 auth code + PKCE | timeout on write (uncertain) | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-692 | Zoho CRM | OAuth 2.0 auth code + PKCE | missed provider event (gap) | IN | sandbox | complete | Sandbox adapter and provider test account only; gap detected by cursor/sequence; repair fetch; no duplicate record | P1 | T16 | PW3 | Y | SYS |
| TC-V12-R-693 | Zoho CRM | OAuth 2.0 auth code + PKCE | missed provider event (gap) | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-694 | Zoho CRM | OAuth 2.0 auth code + PKCE | missed provider event (gap) | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-695 | SMS-DLT aggregator | API key in vault | 429 throttled | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-696 | SMS-DLT aggregator | API key in vault | 5xx | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-697 | SMS-DLT aggregator | API key in vault | 5xx | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-698 | SMS-DLT aggregator | API key in vault | timeout on write (uncertain) | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-699 | SMS-DLT aggregator | API key in vault | validation 4xx | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-700 | SMS-DLT aggregator | API key in vault | DLT template mismatch | IN | production | complete | HOLD `DLT_TEMPLATE_MISMATCH` before dispatch (PDP); no SMS sent; template task to R10 | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-701 | SMS-DLT aggregator | API key in vault | DLT template mismatch | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-702 | SMS-DLT aggregator | API key in vault | DLT template mismatch | EU | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-703 | SMS-DLT aggregator | API key in vault | DLT template mismatch | EU | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-704 | SMS-DLT aggregator | API key in vault | DLT template mismatch | EU | production | DLT registration missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DLT registration missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-705 | SMS-DLT aggregator | API key in vault | missed provider event (gap) | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-706 | Voice CPaaS (140/160 series) | API key in vault | none | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-707 | Voice CPaaS (140/160 series) | API key in vault | none | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-708 | Voice CPaaS (140/160 series) | API key in vault | none | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-709 | Voice CPaaS (140/160 series) | API key in vault | 429 throttled | IN | sandbox | complete | Sandbox adapter and provider test account only; retry with backoff and jitter within the per-connector budget; breaker stays closed | P1 | T01 | PW3 | Y | SYS |
| TC-V12-R-710 | Voice CPaaS (140/160 series) | API key in vault | 429 throttled | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-711 | Voice CPaaS (140/160 series) | API key in vault | 429 throttled | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-712 | Voice CPaaS (140/160 series) | API key in vault | 5xx | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-713 | Voice CPaaS (140/160 series) | API key in vault | 401 token revoked | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-714 | Voice CPaaS (140/160 series) | API key in vault | 401 token revoked | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-715 | Voice CPaaS (140/160 series) | API key in vault | 401 token revoked | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-716 | Voice CPaaS (140/160 series) | API key in vault | timeout on write (uncertain) | IN | production | DPA missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "DPA missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-717 | Voice CPaaS (140/160 series) | API key in vault | timeout on write (uncertain) | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-718 | Voice CPaaS (140/160 series) | API key in vault | validation 4xx | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-719 | Voice CPaaS (140/160 series) | API key in vault | validation 4xx | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-720 | Voice CPaaS (140/160 series) | API key in vault | missed provider event (gap) | IN | production | transfer basis CJ-R15 missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "transfer basis CJ-R15 missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-721 | Voice CPaaS (140/160 series) | API key in vault | missed provider event (gap) | IN | production | security review missing | Activation refused: 409 `CONNECTOR_GATE_INCOMPLETE` listing "security review missing"; installation stays `PendingGate`; no provider call; NSE | P0 | T19 | PW3 | Y | SYS |

#### Group TC-V12-R-M08: 3-way combinatorial cases – Vercel personal-data path: surface × tenant region × request × header × logging × function region

**Common for TC-V12-R-722…TC-V12-R-767:** Pre: PP-02/PP-03/PP-01 on the region stack; Vercel preview deployment plus production alias; WAF rule set v3; log drain to the in-region collector. Steps: deploy (for the function-region rows) or send the request; inspect the response headers, the Vercel log drain, the WAF log and the origin access log. Links for every row: TS-V12-R-08 · US-21-ZR16, US-21-ZR17 · FR-V12-R-081…095; DEC-786; DEC-772. Technique PW (3-way); generated by `assembly/v12b/R_02_combinatorics.py` (model M08).

| ID | surface | region | request | header | logging | function_region | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-722 | Website (startup domain) | IN | page GET (no personal data) | allowlisted only | metadata only | pinned to home region | Served by the `website-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; log record has no body, query string or cookie | P1 | T19 | PW3 | Y | SYS |
| TC-V12-R-723 | Website (startup domain) | IN | API POST with personal data | non-allowlisted header added | body capture attempted | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-724 | Website (startup domain) | EU | auth callback | X-Origin-Verify missing (direct-to-origin) | metadata only | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-725 | Portal (customer) | IN | file upload (portal document) | X-Origin-Verify missing (direct-to-origin) | body capture attempted | pinned to home region | 403 at AWS WAF (rule `origin-verify`); request never reaches Django; WAF log only | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-726 | Portal (customer) | EU | page GET (no personal data) | allowlisted only | body capture attempted | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-727 | Portal (customer) | EU | API POST with personal data | non-allowlisted header added | metadata only | pinned to home region | Served by the `portal-eu` Vercel project; function region fra1 (verify); upstream origin in eu-central-1; non-allowlisted header stripped before forwarding (allowlist VD-05); log record has no body, query string or cookie; response `Cache-Control: no-store`; no edge cache entry | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-728 | Admin | IN | file upload (portal document) | allowlisted only | metadata only | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-729 | Admin | EU | auth callback | allowlisted only | body capture attempted | pinned to home region | Served by the `admin-eu` Vercel project; function region fra1 (verify); upstream origin in eu-central-1; lint rule VD-07 blocks the build if code logs bodies; runtime log drain shows metadata only (method, path template, status, duration, region) | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-730 | Developer portal | IN | page GET (no personal data) | non-allowlisted header added | metadata only | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-731 | Developer portal | EU | page GET (no personal data) | X-Origin-Verify missing (direct-to-origin) | body capture attempted | pinned to home region | 403 at AWS WAF (rule `origin-verify`); request never reaches Django; WAF log only | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-732 | Admin | IN | API POST with personal data | X-Origin-Verify missing (direct-to-origin) | metadata only | pinned to home region | 403 at AWS WAF (rule `origin-verify`); request never reaches Django; WAF log only | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-733 | Admin | EU | file upload (portal document) | non-allowlisted header added | body capture attempted | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-734 | Portal (customer) | IN | auth callback | allowlisted only | metadata only | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-735 | Website (startup domain) | IN | auth callback | non-allowlisted header added | body capture attempted | pinned to home region | Served by the `website-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; non-allowlisted header stripped before forwarding (allowlist VD-05); lint rule VD-07 blocks the build if code logs bodies; runtime log drain shows metadata only (method, path template, status, duration, region) | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-736 | Website (startup domain) | EU | API POST with personal data | allowlisted only | body capture attempted | pinned to home region | Served by the `website-eu` Vercel project; function region fra1 (verify); upstream origin in eu-central-1; lint rule VD-07 blocks the build if code logs bodies; runtime log drain shows metadata only (method, path template, status, duration, region); response `Cache-Control: no-store`; no edge cache entry | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-737 | Admin | IN | page GET (no personal data) | X-Origin-Verify missing (direct-to-origin) | body capture attempted | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-738 | Portal (customer) | EU | file upload (portal document) | allowlisted only | metadata only | pinned to home region | Served by the `portal-eu` Vercel project; function region fra1 (verify); upstream origin in eu-central-1; log record has no body, query string or cookie; response `Cache-Control: no-store`; no edge cache entry | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-739 | Admin | EU | page GET (no personal data) | non-allowlisted header added | metadata only | pinned to home region | Served by the `admin-eu` Vercel project; function region fra1 (verify); upstream origin in eu-central-1; non-allowlisted header stripped before forwarding (allowlist VD-05); log record has no body, query string or cookie | P1 | T19 | PW3 | Y | SYS |
| TC-V12-R-740 | Portal (customer) | EU | API POST with personal data | X-Origin-Verify missing (direct-to-origin) | metadata only | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-741 | Portal (customer) | EU | auth callback | non-allowlisted header added | body capture attempted | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-742 | Developer portal | IN | page GET (no personal data) | allowlisted only | body capture attempted | pinned to home region | Served by the `developer-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; lint rule VD-07 blocks the build if code logs bodies; runtime log drain shows metadata only (method, path template, status, duration, region) | P1 | T19 | PW3 | Y | SYS |
| TC-V12-R-743 | Website (startup domain) | IN | auth callback | X-Origin-Verify missing (direct-to-origin) | body capture attempted | pinned to home region | 403 at AWS WAF (rule `origin-verify`); request never reaches Django; WAF log only | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-744 | Website (startup domain) | EU | page GET (no personal data) | non-allowlisted header added | body capture attempted | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-745 | Admin | IN | auth callback | non-allowlisted header added | metadata only | pinned to home region | Served by the `admin-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; non-allowlisted header stripped before forwarding (allowlist VD-05); log record has no body, query string or cookie | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-746 | Website (startup domain) | IN | API POST with personal data | allowlisted only | metadata only | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-747 | Portal (customer) | IN | page GET (no personal data) | non-allowlisted header added | metadata only | pinned to home region | Served by the `portal-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; non-allowlisted header stripped before forwarding (allowlist VD-05); log record has no body, query string or cookie | P1 | T19 | PW3 | Y | SYS |
| TC-V12-R-748 | Admin | EU | API POST with personal data | X-Origin-Verify missing (direct-to-origin) | body capture attempted | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-749 | Developer portal | EU | page GET (no personal data) | allowlisted only | metadata only | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-750 | Portal (customer) | IN | file upload (portal document) | non-allowlisted header added | metadata only | pinned to home region | Served by the `portal-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; non-allowlisted header stripped before forwarding (allowlist VD-05); log record has no body, query string or cookie; response `Cache-Control: no-store`; no edge cache entry | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-751 | Portal (customer) | EU | file upload (portal document) | X-Origin-Verify missing (direct-to-origin) | metadata only | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-752 | Developer portal | IN | page GET (no personal data) | X-Origin-Verify missing (direct-to-origin) | metadata only | pinned to home region | 403 at AWS WAF (rule `origin-verify`); request never reaches Django; WAF log only | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-753 | Portal (customer) | IN | API POST with personal data | allowlisted only | body capture attempted | pinned to home region | Served by the `portal-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; lint rule VD-07 blocks the build if code logs bodies; runtime log drain shows metadata only (method, path template, status, duration, region); response `Cache-Control: no-store`; no edge cache entry | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-754 | Developer portal | EU | page GET (no personal data) | non-allowlisted header added | body capture attempted | pinned to home region | Served by the `developer-eu` Vercel project; function region fra1 (verify); upstream origin in eu-central-1; non-allowlisted header stripped before forwarding (allowlist VD-05); lint rule VD-07 blocks the build if code logs bodies; runtime log drain shows metadata only (method, path template, status, duration, region) | P1 | T19 | PW3 | Y | SYS |
| TC-V12-R-755 | Portal (customer) | IN | auth callback | X-Origin-Verify missing (direct-to-origin) | metadata only | pinned to home region | 403 at AWS WAF (rule `origin-verify`); request never reaches Django; WAF log only | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-756 | Admin | IN | file upload (portal document) | allowlisted only | body capture attempted | pinned to home region | Served by the `admin-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; lint rule VD-07 blocks the build if code logs bodies; runtime log drain shows metadata only (method, path template, status, duration, region); response `Cache-Control: no-store`; no edge cache entry | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-757 | Admin | IN | auth callback | X-Origin-Verify missing (direct-to-origin) | metadata only | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-758 | Developer portal | IN | page GET (no personal data) | X-Origin-Verify missing (direct-to-origin) | body capture attempted | deployed to a non-home region | Deployment rejected by the CI region-pin check (AU-296 rule VD-02); production alias stays on the last compliant deployment; request served by it | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-759 | Website (startup domain) | IN | page GET (no personal data) | non-allowlisted header added | metadata only | pinned to home region | Served by the `website-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; non-allowlisted header stripped before forwarding (allowlist VD-05); log record has no body, query string or cookie | P1 | T19 | PW3 | Y | SYS |
| TC-V12-R-760 | Website (startup domain) | IN | page GET (no personal data) | X-Origin-Verify missing (direct-to-origin) | metadata only | pinned to home region | 403 at AWS WAF (rule `origin-verify`); request never reaches Django; WAF log only | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-761 | Website (startup domain) | IN | API POST with personal data | X-Origin-Verify missing (direct-to-origin) | metadata only | pinned to home region | 403 at AWS WAF (rule `origin-verify`); request never reaches Django; WAF log only | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-762 | Website (startup domain) | IN | auth callback | allowlisted only | metadata only | pinned to home region | Served by the `website-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; log record has no body, query string or cookie | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-763 | Portal (customer) | IN | page GET (no personal data) | X-Origin-Verify missing (direct-to-origin) | metadata only | pinned to home region | 403 at AWS WAF (rule `origin-verify`); request never reaches Django; WAF log only | P0 | T07 | PW3 | Y | SYS |
| TC-V12-R-764 | Admin | IN | page GET (no personal data) | allowlisted only | metadata only | pinned to home region | Served by the `admin-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; log record has no body, query string or cookie | P1 | T19 | PW3 | Y | SYS |
| TC-V12-R-765 | Admin | IN | API POST with personal data | allowlisted only | metadata only | pinned to home region | Served by the `admin-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; log record has no body, query string or cookie; response `Cache-Control: no-store`; no edge cache entry | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-766 | Admin | IN | API POST with personal data | non-allowlisted header added | metadata only | pinned to home region | Served by the `admin-in` Vercel project; function region bom1 (verify); upstream origin in ap-south-1; non-allowlisted header stripped before forwarding (allowlist VD-05); log record has no body, query string or cookie; response `Cache-Control: no-store`; no edge cache entry | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-767 | Admin | IN | file upload (portal document) | X-Origin-Verify missing (direct-to-origin) | metadata only | pinned to home region | 403 at AWS WAF (rule `origin-verify`); request never reaches Django; WAF log only | P0 | T07 | PW3 | Y | SYS |

#### Group TC-V12-R-M09: 3-way combinatorial cases – Recovery: region × failure × WAL archive age × restore path × release gate

**Common for TC-V12-R-768…TC-V12-R-858:** Pre: drill environment cloned from production topology per region (synthetic data volume profile `l`); AU-297 monitors running; virtual incident clock. Steps: inject the failure; execute the runbook in the row path; record timestamps; run the post-restore verification pack PRV-01…08. Links for every row: TS-V12-R-09 · US-21-ZR18, US-21-ZR19 · FR-V12-R-096…110; DEC-787; DEC-771; KPI-18/19/32; OPT-TC-ST-14. Technique PW (3-way); generated by `assembly/v12b/R_02_combinatorics.py` (model M09).

| ID | region | failure | wal_age | path | gate | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-768 | IN | row corruption by bug | 1 min | Supabase PITR to new project | Release 1 gate | Restore to T−1 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-769 | IN | row corruption by bug | 5 min | AWS WAL-G archive restore | Release 2 gate | Restore to T−5 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-770 | IN | row corruption by bug | 14 min | AWS WAL-G archive restore (in-zone secondary region) | Quarterly drill | Restore to T−14 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-771 | IN | bad migration | 1 min | AWS WAL-G archive restore | Quarterly drill | Restore to T−1 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-772 | IN | bad migration | 5 min | AWS WAL-G archive restore (in-zone secondary region) | Release 1 gate | Restore to T−5 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-773 | IN | bad migration | 14 min | Supabase PITR to new project | Release 2 gate | Restore to T−14 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-774 | IN | accidental tenant delete | 1 min | AWS WAL-G archive restore (in-zone secondary region) | Release 2 gate | Restore to T−1 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-775 | IN | accidental tenant delete | 5 min | Supabase PITR to new project | Quarterly drill | Restore to T−5 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-776 | IN | accidental tenant delete | 14 min | AWS WAL-G archive restore | Release 1 gate | Restore to T−14 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-777 | EU | row corruption by bug | 16 min | Supabase PITR to new project | Release 2 gate | Restore to T−16 min via Supabase PITR to new project; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-778 | EU | bad migration | 16 min | AWS WAL-G archive restore | Release 1 gate | Restore to T−16 min via AWS WAL-G archive restore; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-779 | EU | accidental tenant delete | 1 min | Nightly logical dump | Release 1 gate | Restore to T−1 min via Nightly logical dump; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-780 | EU | accidental tenant delete | 16 min | AWS WAL-G archive restore (in-zone secondary region) | Quarterly drill | Restore to T−16 min via AWS WAL-G archive restore (in-zone secondary region); RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-781 | EU | Supabase project unavailable | 1 min | Supabase PITR to new project | Quarterly drill | Path not available (provider control plane unreachable); runbook DR-R2 switches to the AWS WAL-G replica path; decision logged within 10 min | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-782 | EU | Supabase project unavailable | 5 min | AWS WAL-G archive restore (in-zone secondary region) | Release 2 gate | Restore to T−5 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-783 | EU | AZ loss | 1 min | AWS WAL-G archive restore | Release 2 gate | Restore to T−1 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-784 | EU | AZ loss | 5 min | Supabase PITR to new project | Release 1 gate | Restore to T−5 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-785 | EU | region loss | 5 min | AWS WAL-G archive restore | Quarterly drill | Path refused: in-region copies are lost; runbook DR-R5 uses the in-zone secondary-region WAL-G archive (IN→IN, EU→EU only) | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-786 | EU | region loss | 14 min | AWS WAL-G archive restore (in-zone secondary region) | Release 1 gate | Restore to T−14 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-787 | IN | accidental tenant delete | 16 min | Nightly logical dump | Release 2 gate | Restore to T−16 min via Nightly logical dump; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-788 | IN | Supabase project unavailable | 16 min | Supabase PITR to new project | Release 1 gate | Path not available (provider control plane unreachable); runbook DR-R2 switches to the AWS WAL-G replica path; decision logged within 10 min | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-789 | IN | AZ loss | 16 min | AWS WAL-G archive restore | Quarterly drill | Restore to T−16 min via AWS WAL-G archive restore; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-790 | IN | region loss | 16 min | AWS WAL-G archive restore (in-zone secondary region) | Release 2 gate | Restore to T−16 min via AWS WAL-G archive restore (in-zone secondary region); RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-791 | EU | row corruption by bug | 14 min | AWS WAL-G archive restore | Quarterly drill | Restore to T−14 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-792 | EU | accidental tenant delete | 14 min | Supabase PITR to new project | Release 2 gate | Restore to T−14 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-793 | IN | Supabase project unavailable | 14 min | AWS WAL-G archive restore | Release 2 gate | Restore to T−14 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-794 | IN | AZ loss | 1 min | AWS WAL-G archive restore (in-zone secondary region) | Release 1 gate | Restore to T−1 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-795 | IN | region loss | 1 min | AWS WAL-G archive restore | Release 1 gate | Path refused: in-region copies are lost; runbook DR-R5 uses the in-zone secondary-region WAL-G archive (IN→IN, EU→EU only) | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-796 | IN | region loss | 14 min | Supabase PITR to new project | Quarterly drill | Path refused: in-region copies are lost; runbook DR-R5 uses the in-zone secondary-region WAL-G archive (IN→IN, EU→EU only) | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-797 | EU | bad migration | 1 min | AWS WAL-G archive restore (in-zone secondary region) | Release 2 gate | Restore to T−1 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-798 | EU | region loss | 1 min | Supabase PITR to new project | Release 2 gate | Path refused: in-region copies are lost; runbook DR-R5 uses the in-zone secondary-region WAL-G archive (IN→IN, EU→EU only) | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-799 | IN | accidental tenant delete | 14 min | Nightly logical dump | Quarterly drill | Restore to T−14 min via Nightly logical dump; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-800 | IN | Supabase project unavailable | 1 min | AWS WAL-G archive restore (in-zone secondary region) | Quarterly drill | Restore to T−1 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-801 | IN | AZ loss | 5 min | Supabase PITR to new project | Release 2 gate | Restore to T−5 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-802 | EU | row corruption by bug | 5 min | AWS WAL-G archive restore (in-zone secondary region) | Release 1 gate | Restore to T−5 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-803 | EU | bad migration | 5 min | Supabase PITR to new project | Quarterly drill | Restore to T−5 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-804 | EU | accidental tenant delete | 5 min | Nightly logical dump | Release 2 gate | Restore to T−5 min via Nightly logical dump; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-805 | EU | Supabase project unavailable | 5 min | AWS WAL-G archive restore | Release 1 gate | Restore to T−5 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-806 | EU | AZ loss | 5 min | AWS WAL-G archive restore (in-zone secondary region) | Quarterly drill | Restore to T−5 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-807 | IN | AZ loss | 14 min | AWS WAL-G archive restore (in-zone secondary region) | Release 2 gate | Restore to T−14 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-808 | IN | row corruption by bug | 16 min | Supabase PITR to new project | Quarterly drill | Restore to T−16 min via Supabase PITR to new project; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-809 | IN | bad migration | 16 min | AWS WAL-G archive restore | Release 2 gate | Restore to T−16 min via AWS WAL-G archive restore; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-810 | IN | accidental tenant delete | 5 min | Nightly logical dump | Release 1 gate | Restore to T−5 min via Nightly logical dump; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-811 | IN | region loss | 5 min | Supabase PITR to new project | Release 1 gate | Path refused: in-region copies are lost; runbook DR-R5 uses the in-zone secondary-region WAL-G archive (IN→IN, EU→EU only) | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-812 | EU | row corruption by bug | 1 min | AWS WAL-G archive restore (in-zone secondary region) | Release 2 gate | Restore to T−1 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-813 | EU | bad migration | 14 min | Supabase PITR to new project | Release 1 gate | Restore to T−14 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-814 | EU | accidental tenant delete | 1 min | AWS WAL-G archive restore | Quarterly drill | Restore to T−1 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-815 | EU | Supabase project unavailable | 14 min | AWS WAL-G archive restore (in-zone secondary region) | Release 1 gate | Restore to T−14 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-816 | EU | Supabase project unavailable | 16 min | AWS WAL-G archive restore | Quarterly drill | Restore to T−16 min via AWS WAL-G archive restore; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-817 | EU | AZ loss | 14 min | Supabase PITR to new project | Quarterly drill | Restore to T−14 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-818 | EU | AZ loss | 16 min | AWS WAL-G archive restore (in-zone secondary region) | Release 1 gate | Restore to T−16 min via AWS WAL-G archive restore (in-zone secondary region); RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-819 | IN | row corruption by bug | 16 min | AWS WAL-G archive restore | Release 1 gate | Restore to T−16 min via AWS WAL-G archive restore; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-820 | IN | bad migration | 14 min | AWS WAL-G archive restore (in-zone secondary region) | Quarterly drill | Restore to T−14 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-821 | IN | accidental tenant delete | 16 min | Supabase PITR to new project | Release 1 gate | Restore to T−16 min via Supabase PITR to new project; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-822 | IN | Supabase project unavailable | 5 min | Supabase PITR to new project | Release 2 gate | Path not available (provider control plane unreachable); runbook DR-R2 switches to the AWS WAL-G replica path; decision logged within 10 min | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-823 | IN | AZ loss | 14 min | AWS WAL-G archive restore | Release 1 gate | Restore to T−14 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-824 | IN | region loss | 1 min | AWS WAL-G archive restore (in-zone secondary region) | Quarterly drill | Restore to T−1 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-825 | IN | region loss | 14 min | AWS WAL-G archive restore | Release 2 gate | Path refused: in-region copies are lost; runbook DR-R5 uses the in-zone secondary-region WAL-G archive (IN→IN, EU→EU only) | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-826 | EU | accidental tenant delete | 16 min | Nightly logical dump | Quarterly drill | Restore to T−16 min via Nightly logical dump; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-827 | EU | region loss | 16 min | Supabase PITR to new project | Release 1 gate | Path refused: in-region copies are lost; runbook DR-R5 uses the in-zone secondary-region WAL-G archive (IN→IN, EU→EU only) | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-828 | IN | row corruption by bug | 1 min | AWS WAL-G archive restore | Quarterly drill | Restore to T−1 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-829 | IN | row corruption by bug | 5 min | Supabase PITR to new project | Quarterly drill | Restore to T−5 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-830 | IN | row corruption by bug | 14 min | Supabase PITR to new project | Release 1 gate | Restore to T−14 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-831 | IN | bad migration | 1 min | Supabase PITR to new project | Release 1 gate | Restore to T−1 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-832 | IN | bad migration | 5 min | AWS WAL-G archive restore | Release 2 gate | Restore to T−5 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-833 | IN | bad migration | 16 min | Supabase PITR to new project | Quarterly drill | Restore to T−16 min via Supabase PITR to new project; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-834 | IN | accidental tenant delete | 1 min | Nightly logical dump | Release 2 gate | Restore to T−1 min via Nightly logical dump; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-835 | IN | accidental tenant delete | 5 min | AWS WAL-G archive restore | Release 2 gate | Restore to T−5 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-836 | IN | accidental tenant delete | 5 min | AWS WAL-G archive restore (in-zone secondary region) | Release 1 gate | Restore to T−5 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-837 | IN | Supabase project unavailable | 1 min | AWS WAL-G archive restore | Release 1 gate | Restore to T−1 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-838 | IN | Supabase project unavailable | 14 min | Supabase PITR to new project | Quarterly drill | Path not available (provider control plane unreachable); runbook DR-R2 switches to the AWS WAL-G replica path; decision logged within 10 min | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-839 | IN | Supabase project unavailable | 16 min | AWS WAL-G archive restore (in-zone secondary region) | Release 2 gate | Restore to T−16 min via AWS WAL-G archive restore (in-zone secondary region); RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-840 | IN | AZ loss | 1 min | Supabase PITR to new project | Quarterly drill | Restore to T−1 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-841 | IN | AZ loss | 16 min | Supabase PITR to new project | Release 2 gate | Restore to T−16 min via Supabase PITR to new project; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-842 | IN | region loss | 5 min | AWS WAL-G archive restore (in-zone secondary region) | Release 2 gate | Restore to T−5 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-843 | IN | region loss | 16 min | AWS WAL-G archive restore | Quarterly drill | Path refused: in-region copies are lost; runbook DR-R5 uses the in-zone secondary-region WAL-G archive (IN→IN, EU→EU only) | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-844 | EU | accidental tenant delete | 14 min | Nightly logical dump | Release 1 gate | Restore to T−14 min via Nightly logical dump; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Frankfurt or another EU region (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-845 | IN | row corruption by bug | 14 min | Supabase PITR to new project | Release 2 gate | Restore to T−14 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-846 | IN | row corruption by bug | 16 min | AWS WAL-G archive restore (in-zone secondary region) | Release 1 gate | Restore to T−16 min via AWS WAL-G archive restore (in-zone secondary region); RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-847 | IN | bad migration | 14 min | AWS WAL-G archive restore | Release 1 gate | Restore to T−14 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-848 | IN | bad migration | 16 min | AWS WAL-G archive restore (in-zone secondary region) | Release 1 gate | Restore to T−16 min via AWS WAL-G archive restore (in-zone secondary region); RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-849 | IN | accidental tenant delete | 1 min | Supabase PITR to new project | Release 1 gate | Restore to T−1 min via Supabase PITR to new project; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-850 | IN | accidental tenant delete | 1 min | Nightly logical dump | Quarterly drill | Restore to T−1 min via Nightly logical dump; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-851 | IN | accidental tenant delete | 5 min | Nightly logical dump | Quarterly drill | Restore to T−5 min via Nightly logical dump; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-852 | IN | accidental tenant delete | 14 min | AWS WAL-G archive restore (in-zone secondary region) | Release 1 gate | Restore to T−14 min via AWS WAL-G archive restore (in-zone secondary region); RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-853 | IN | accidental tenant delete | 14 min | Nightly logical dump | Release 2 gate | Restore to T−14 min via Nightly logical dump; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-854 | IN | accidental tenant delete | 16 min | AWS WAL-G archive restore | Release 1 gate | Restore to T−16 min via AWS WAL-G archive restore; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-855 | IN | accidental tenant delete | 16 min | Nightly logical dump | Release 1 gate | Restore to T−16 min via Nightly logical dump; RPO **breached**: SEV1, release blocker if in a drill; AU-297 had paged at 10 min; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-856 | IN | Supabase project unavailable | 1 min | Supabase PITR to new project | Release 2 gate | Path not available (provider control plane unreachable); runbook DR-R2 switches to the AWS WAL-G replica path; decision logged within 10 min | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-857 | IN | Supabase project unavailable | 5 min | Supabase PITR to new project | Quarterly drill | Path not available (provider control plane unreachable); runbook DR-R2 switches to the AWS WAL-G replica path; decision logged within 10 min | P0 | T21 | PW3 | Y | E2E |
| TC-V12-R-858 | IN | AZ loss | 5 min | AWS WAL-G archive restore | Release 1 gate | Restore to T−5 min via AWS WAL-G archive restore; RPO met; growth workload RTO ≤ 120 min, critical ≤ 4 h measured; RLS smoke, audit-chain verify, ledger reconciliation, erasure replay; target location Mumbai or Hyderabad (in zone); effects paused until reconciled | P0 | T21 | PW3 | Y | E2E |

#### Group TC-V12-R-M10: 3-way combinatorial cases – Model registry routing: task × data class × region × candidate × registry state × availability

**Common for TC-V12-R-859…TC-V12-R-1055:** Pre: PP-05 with the gateway simulator; registry fixture `REG-FIX-3` (all candidates in all states, regions per §11.19.5.6.C); EVAL suites marked passing for the task and locale unless the state says otherwise. Steps: submit one AI-inference step with the task, data class and tenant region in the row; read the route decision, run record and fallback log. Links for every row: TS-V12-R-10 · US-04-ZR22, US-04-ZR23 · FR-V12-R-111…130; DEC-788; AIX-02/03; AU-151/152/298. Technique PW (3-way); generated by `assembly/v12b/R_02_combinatorics.py` (model M10).

| ID | task | data | region | candidate | state | availability | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-859 | classification | Public | IN | Claude Sonnet (approved primary) | approved | ok | Routed to Claude Sonnet (approved primary) in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-860 | classification | Public | EU | Claude Haiku-class | candidate | 5xx / timeout | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-861 | classification | Internal (non-personal) | IN | Claude larger model (MDL-L1) | suspended | 5xx / timeout | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-862 | classification | Internal (non-personal) | EU | OpenAI GPT family | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-863 | drafting | Public | IN | OpenAI GPT family | DPA expired | 5xx / timeout | Not routed: registry state `DPA expired`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-864 | drafting | Public | EU | Claude larger model (MDL-L1) | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-865 | drafting | Internal (non-personal) | IN | Claude Haiku-class | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-866 | drafting | Internal (non-personal) | EU | Claude Sonnet (approved primary) | approved | 5xx / timeout | Routed to Claude Sonnet (approved primary) in EU; run record stores `mdl_id`, version, region, prompt version; on failure: fallback only to a row with the same output schema, same region and same-or-stricter class (AU-298 eligibility); else HOLD | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-867 | complex synthesis | Personal (masked) | IN | Claude Sonnet (approved primary) | candidate | 5xx / timeout | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-868 | complex synthesis | Personal (masked) | EU | Google Gemini | approved | ok | Routed to Google Gemini in EU; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-869 | complex synthesis | Personal (unmasked) | IN | Claude larger model (MDL-L1) | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-870 | complex synthesis | Personal (unmasked) | EU | OpenAI GPT family | suspended | 5xx / timeout | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-871 | embedding | Personal (masked) | IN | OpenAI GPT family | suspended | ok | Not routed: registry state `suspended`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-872 | embedding | Personal (masked) | EU | Open-weight in region (Llama/Mistral/Qwen) | DPA expired | 5xx / timeout | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-873 | embedding | Personal (unmasked) | IN | Google Gemini | approved | 5xx / timeout | Routed to Google Gemini in IN; run record stores `mdl_id`, version, region, prompt version; on failure: fallback only to a row with the same output schema, same region and same-or-stricter class (AU-298 eligibility); else HOLD | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-874 | safety screening | Personal (unmasked) | EU | Claude Haiku-class | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-875 | safety screening | Restricted | IN | Open-weight in region (Llama/Mistral/Qwen) | eval suite failed | 5xx / timeout | Not routed: registry state `eval suite failed`; open-weight rows accept Personal only when masked (MDL-S1); Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-876 | complex synthesis | Restricted | EU | Open-weight in region (Llama/Mistral/Qwen) | candidate | ok | Not routed: registry state `candidate`; open-weight rows accept Personal only when masked (MDL-S1); Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-877 | classification | Personal (masked) | IN | Free Tier 2 provider | eval suite failed | ok | Not routed: registry state `eval suite failed`; no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-878 | classification | Restricted | EU | Google Gemini | eval suite failed | 5xx / timeout | Not routed: registry state `eval suite failed`; Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-879 | drafting | Personal (unmasked) | EU | Free Tier 2 provider | candidate | 5xx / timeout | Not routed: registry state `candidate`; no approved EU processing location; Tier 2 accepts Public/Internal-non-personal only (invariant). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-880 | drafting | Restricted | IN | Google Gemini | suspended | ok | Not routed: registry state `suspended`; Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-881 | safety screening | Internal (non-personal) | IN | Open-weight in region (Llama/Mistral/Qwen) | approved | ok | Routed to Open-weight in region (Llama/Mistral/Qwen) in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-882 | drafting | Personal (masked) | EU | Claude larger model (MDL-L1) | eval suite failed | 5xx / timeout | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-883 | complex synthesis | Public | EU | Claude Sonnet (approved primary) | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-884 | embedding | Public | EU | Google Gemini | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-885 | safety screening | Public | IN | Claude Haiku-class | suspended | 5xx / timeout | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-886 | classification | Personal (unmasked) | IN | OpenAI GPT family | candidate | ok | Not routed: registry state `candidate`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-887 | classification | Personal (unmasked) | EU | Claude Sonnet (approved primary) | DPA expired | 5xx / timeout | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-888 | classification | Restricted | IN | Claude Haiku-class | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-889 | complex synthesis | Internal (non-personal) | IN | OpenAI GPT family | eval suite failed | 5xx / timeout | Not routed: registry state `eval suite failed`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-890 | complex synthesis | Restricted | IN | Claude larger model (MDL-L1) | approved | 5xx / timeout | Routed to Claude larger model (MDL-L1) in IN; run record stores `mdl_id`, version, region, prompt version; on failure: fallback only to a row with the same output schema, same region and same-or-stricter class (AU-298 eligibility); else HOLD | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-891 | embedding | Restricted | EU | OpenAI GPT family | approved | ok | Not routed: Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-892 | classification | Personal (masked) | EU | Free Tier 2 provider | approved | 5xx / timeout | Not routed: no approved EU processing location; Tier 2 accepts Public/Internal-non-personal only (invariant). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-893 | drafting | Personal (masked) | IN | Claude Sonnet (approved primary) | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-894 | drafting | Personal (unmasked) | IN | Open-weight in region (Llama/Mistral/Qwen) | suspended | ok | Not routed: registry state `suspended`; open-weight rows accept Personal only when masked (MDL-S1). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-895 | drafting | Restricted | EU | Claude Haiku-class | DPA expired | 5xx / timeout | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-896 | embedding | Internal (non-personal) | EU | Open-weight in region (Llama/Mistral/Qwen) | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-897 | safety screening | Public | EU | Open-weight in region (Llama/Mistral/Qwen) | approved | 5xx / timeout | Routed to Open-weight in region (Llama/Mistral/Qwen) in EU; run record stores `mdl_id`, version, region, prompt version; on failure: fallback only to a row with the same output schema, same region and same-or-stricter class (AU-298 eligibility); else HOLD | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-898 | complex synthesis | Public | IN | Google Gemini | DPA expired | 5xx / timeout | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-899 | embedding | Restricted | IN | OpenAI GPT family | candidate | 5xx / timeout | Not routed: registry state `candidate`; no approved IN processing location; Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-900 | classification | Internal (non-personal) | EU | Free Tier 2 provider | suspended | ok | Not routed: registry state `suspended`; no approved EU processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-901 | drafting | Public | IN | Free Tier 2 provider | approved | ok | Not routed: no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-902 | complex synthesis | Internal (non-personal) | EU | Claude larger model (MDL-L1) | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-903 | embedding | Public | IN | Open-weight in region (Llama/Mistral/Qwen) | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-904 | safety screening | Personal (masked) | IN | Open-weight in region (Llama/Mistral/Qwen) | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-905 | classification | Personal (unmasked) | EU | Claude larger model (MDL-L1) | approved | ok | Routed to Claude larger model (MDL-L1) in EU; run record stores `mdl_id`, version, region, prompt version | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-906 | drafting | Internal (non-personal) | IN | Free Tier 2 provider | DPA expired | 5xx / timeout | Not routed: registry state `DPA expired`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-907 | drafting | Personal (masked) | EU | Google Gemini | suspended | 5xx / timeout | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-908 | classification | Internal (non-personal) | IN | Google Gemini | candidate | 5xx / timeout | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-909 | classification | Restricted | EU | Claude Sonnet (approved primary) | suspended | 5xx / timeout | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-910 | drafting | Public | EU | OpenAI GPT family | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-911 | drafting | Personal (unmasked) | IN | Claude Sonnet (approved primary) | eval suite failed | 5xx / timeout | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-912 | complex synthesis | Internal (non-personal) | IN | Claude Sonnet (approved primary) | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-913 | embedding | Personal (unmasked) | EU | Open-weight in region (Llama/Mistral/Qwen) | suspended | 5xx / timeout | Not routed: registry state `suspended`; open-weight rows accept Personal only when masked (MDL-S1). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-914 | safety screening | Internal (non-personal) | EU | Claude Haiku-class | DPA expired | 5xx / timeout | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-915 | safety screening | Personal (masked) | IN | Claude Haiku-class | approved | 5xx / timeout | Routed to Claude Haiku-class in IN; run record stores `mdl_id`, version, region, prompt version; on failure: fallback only to a row with the same output schema, same region and same-or-stricter class (AU-298 eligibility); else HOLD | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-916 | classification | Public | IN | Claude larger model (MDL-L1) | eval suite failed | 5xx / timeout | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-917 | safety screening | Personal (masked) | EU | Claude Haiku-class | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-918 | classification | Public | EU | Free Tier 2 provider | DPA expired | ok | Not routed: registry state `DPA expired`; no approved EU processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-919 | classification | Personal (masked) | EU | OpenAI GPT family | candidate | 5xx / timeout | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-920 | classification | Personal (unmasked) | EU | Google Gemini | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-921 | classification | Restricted | IN | Free Tier 2 provider | candidate | ok | Not routed: registry state `candidate`; no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant); Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-922 | drafting | Restricted | EU | Free Tier 2 provider | eval suite failed | 5xx / timeout | Not routed: registry state `eval suite failed`; no approved EU processing location; Tier 2 accepts Public/Internal-non-personal only (invariant); Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-923 | embedding | Internal (non-personal) | IN | Google Gemini | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-924 | safety screening | Personal (unmasked) | IN | Claude Haiku-class | candidate | 5xx / timeout | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-925 | classification | Public | IN | Open-weight in region (Llama/Mistral/Qwen) | candidate | 5xx / timeout | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-926 | drafting | Personal (masked) | IN | Claude larger model (MDL-L1) | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-927 | drafting | Restricted | IN | Claude Sonnet (approved primary) | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-928 | complex synthesis | Internal (non-personal) | IN | Open-weight in region (Llama/Mistral/Qwen) | DPA expired | 5xx / timeout | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-929 | complex synthesis | Restricted | EU | Claude larger model (MDL-L1) | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-930 | safety screening | Restricted | EU | Claude Haiku-class | approved | ok | Routed to Claude Haiku-class in EU; run record stores `mdl_id`, version, region, prompt version | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-931 | classification | Internal (non-personal) | IN | Claude Haiku-class | eval suite failed | 5xx / timeout | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-932 | classification | Personal (masked) | EU | Claude larger model (MDL-L1) | DPA expired | 5xx / timeout | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-933 | classification | Personal (masked) | EU | Open-weight in region (Llama/Mistral/Qwen) | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-934 | classification | Personal (unmasked) | IN | Free Tier 2 provider | suspended | ok | Not routed: registry state `suspended`; no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-935 | drafting | Personal (masked) | IN | OpenAI GPT family | approved | 5xx / timeout | Not routed: no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-936 | drafting | Restricted | EU | Open-weight in region (Llama/Mistral/Qwen) | approved | 5xx / timeout | Not routed: open-weight rows accept Personal only when masked (MDL-S1); Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-937 | complex synthesis | Personal (masked) | EU | OpenAI GPT family | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-938 | safety screening | Public | IN | Claude Haiku-class | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-939 | drafting | Public | EU | Claude Sonnet (approved primary) | candidate | 5xx / timeout | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-940 | complex synthesis | Personal (unmasked) | IN | Claude Sonnet (approved primary) | approved | ok | Routed to Claude Sonnet (approved primary) in IN; run record stores `mdl_id`, version, region, prompt version | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-941 | embedding | Public | IN | OpenAI GPT family | eval suite failed | 5xx / timeout | Not routed: registry state `eval suite failed`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-942 | embedding | Internal (non-personal) | EU | Google Gemini | suspended | 5xx / timeout | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-943 | embedding | Personal (unmasked) | IN | OpenAI GPT family | DPA expired | ok | Not routed: registry state `DPA expired`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-944 | classification | Public | IN | OpenAI GPT family | suspended | ok | Not routed: registry state `suspended`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-945 | classification | Personal (masked) | EU | Claude Sonnet (approved primary) | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-946 | classification | Personal (unmasked) | IN | Claude larger model (MDL-L1) | candidate | 5xx / timeout | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-947 | classification | Personal (unmasked) | IN | Open-weight in region (Llama/Mistral/Qwen) | eval suite failed | ok | Not routed: registry state `eval suite failed`; open-weight rows accept Personal only when masked (MDL-S1). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-948 | drafting | Public | IN | Free Tier 2 provider | suspended | 5xx / timeout | Not routed: registry state `suspended`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-949 | drafting | Internal (non-personal) | IN | OpenAI GPT family | suspended | ok | Not routed: registry state `suspended`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-950 | drafting | Personal (unmasked) | IN | Claude Haiku-class | approved | ok | Routed to Claude Haiku-class in IN; run record stores `mdl_id`, version, region, prompt version | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-951 | complex synthesis | Public | IN | OpenAI GPT family | approved | ok | Not routed: no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-952 | complex synthesis | Public | IN | Open-weight in region (Llama/Mistral/Qwen) | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-953 | complex synthesis | Personal (masked) | IN | Claude larger model (MDL-L1) | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-954 | complex synthesis | Personal (masked) | IN | Google Gemini | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-955 | complex synthesis | Personal (unmasked) | IN | Google Gemini | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-956 | complex synthesis | Restricted | IN | Claude Sonnet (approved primary) | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-957 | embedding | Restricted | IN | Google Gemini | DPA expired | ok | Not routed: registry state `DPA expired`; Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-958 | safety screening | Personal (unmasked) | IN | Open-weight in region (Llama/Mistral/Qwen) | DPA expired | ok | Not routed: registry state `DPA expired`; open-weight rows accept Personal only when masked (MDL-S1). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-959 | classification | Public | IN | Google Gemini | approved | ok | Routed to Google Gemini in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-960 | classification | Internal (non-personal) | IN | Claude Sonnet (approved primary) | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-961 | classification | Internal (non-personal) | IN | Claude Haiku-class | approved | ok | Routed to Claude Haiku-class in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-962 | classification | Personal (unmasked) | IN | Claude Haiku-class | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-963 | classification | Restricted | IN | OpenAI GPT family | approved | ok | Not routed: no approved IN processing location; Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-964 | classification | Restricted | IN | Open-weight in region (Llama/Mistral/Qwen) | DPA expired | ok | Not routed: registry state `DPA expired`; open-weight rows accept Personal only when masked (MDL-S1); Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-965 | drafting | Public | IN | Claude Haiku-class | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-966 | drafting | Public | IN | Google Gemini | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-967 | drafting | Public | IN | Open-weight in region (Llama/Mistral/Qwen) | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-968 | drafting | Internal (non-personal) | IN | Claude larger model (MDL-L1) | approved | ok | Routed to Claude larger model (MDL-L1) in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-969 | drafting | Internal (non-personal) | IN | Google Gemini | approved | ok | Routed to Google Gemini in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-970 | drafting | Internal (non-personal) | IN | Open-weight in region (Llama/Mistral/Qwen) | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-971 | drafting | Personal (unmasked) | IN | Claude larger model (MDL-L1) | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-972 | complex synthesis | Public | IN | Claude larger model (MDL-L1) | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-973 | complex synthesis | Personal (masked) | IN | Open-weight in region (Llama/Mistral/Qwen) | approved | ok | Routed to Open-weight in region (Llama/Mistral/Qwen) in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-974 | complex synthesis | Personal (unmasked) | IN | Open-weight in region (Llama/Mistral/Qwen) | eval suite failed | ok | Not routed: registry state `eval suite failed`; open-weight rows accept Personal only when masked (MDL-S1). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-975 | complex synthesis | Restricted | IN | OpenAI GPT family | suspended | ok | Not routed: registry state `suspended`; no approved IN processing location; Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-976 | embedding | Internal (non-personal) | IN | OpenAI GPT family | approved | ok | Not routed: no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-977 | embedding | Personal (masked) | IN | Google Gemini | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-978 | embedding | Personal (unmasked) | IN | Open-weight in region (Llama/Mistral/Qwen) | candidate | ok | Not routed: registry state `candidate`; open-weight rows accept Personal only when masked (MDL-S1). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-979 | embedding | Restricted | IN | Open-weight in region (Llama/Mistral/Qwen) | suspended | ok | Not routed: registry state `suspended`; open-weight rows accept Personal only when masked (MDL-S1); Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-980 | safety screening | Internal (non-personal) | IN | Open-weight in region (Llama/Mistral/Qwen) | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-981 | safety screening | Restricted | EU | Claude Haiku-class | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-982 | classification | Public | IN | Google Gemini | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-983 | classification | Internal (non-personal) | IN | Open-weight in region (Llama/Mistral/Qwen) | approved | ok | Routed to Open-weight in region (Llama/Mistral/Qwen) in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-984 | classification | Personal (masked) | IN | Claude Haiku-class | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-985 | classification | Personal (masked) | IN | OpenAI GPT family | eval suite failed | ok | Not routed: registry state `eval suite failed`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-986 | classification | Personal (masked) | IN | Google Gemini | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-987 | classification | Restricted | IN | Claude larger model (MDL-L1) | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-988 | drafting | Public | IN | Claude Sonnet (approved primary) | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-989 | drafting | Public | IN | OpenAI GPT family | candidate | ok | Not routed: registry state `candidate`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-990 | drafting | Internal (non-personal) | IN | Claude Sonnet (approved primary) | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-991 | drafting | Internal (non-personal) | IN | Claude Haiku-class | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-992 | drafting | Internal (non-personal) | IN | Google Gemini | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-993 | drafting | Personal (masked) | IN | Claude Haiku-class | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-994 | drafting | Personal (masked) | IN | Open-weight in region (Llama/Mistral/Qwen) | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-995 | drafting | Personal (masked) | IN | Free Tier 2 provider | candidate | ok | Not routed: registry state `candidate`; no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-996 | drafting | Personal (unmasked) | IN | OpenAI GPT family | approved | ok | Not routed: no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-997 | drafting | Personal (unmasked) | IN | Google Gemini | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-998 | drafting | Restricted | IN | Claude larger model (MDL-L1) | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-999 | drafting | Restricted | IN | OpenAI GPT family | DPA expired | ok | Not routed: registry state `DPA expired`; no approved IN processing location; Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1000 | complex synthesis | Internal (non-personal) | IN | OpenAI GPT family | candidate | ok | Not routed: registry state `candidate`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1001 | complex synthesis | Internal (non-personal) | IN | Google Gemini | approved | ok | Routed to Google Gemini in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-1002 | complex synthesis | Personal (unmasked) | IN | Google Gemini | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1003 | complex synthesis | Restricted | IN | Google Gemini | approved | ok | Not routed: Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1004 | embedding | Public | IN | Open-weight in region (Llama/Mistral/Qwen) | approved | ok | Routed to Open-weight in region (Llama/Mistral/Qwen) in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-1005 | embedding | Personal (masked) | IN | Open-weight in region (Llama/Mistral/Qwen) | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1006 | embedding | Personal (unmasked) | IN | OpenAI GPT family | eval suite failed | ok | Not routed: registry state `eval suite failed`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1007 | embedding | Restricted | IN | OpenAI GPT family | eval suite failed | ok | Not routed: registry state `eval suite failed`; no approved IN processing location; Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1008 | safety screening | Personal (masked) | IN | Claude Haiku-class | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1009 | safety screening | Personal (unmasked) | IN | Open-weight in region (Llama/Mistral/Qwen) | approved | ok | Not routed: open-weight rows accept Personal only when masked (MDL-S1). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1010 | safety screening | Restricted | IN | Claude Haiku-class | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1011 | classification | Public | IN | Claude Sonnet (approved primary) | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1012 | classification | Public | IN | Claude Haiku-class | approved | ok | Routed to Claude Haiku-class in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-1013 | classification | Public | IN | Claude larger model (MDL-L1) | approved | ok | Routed to Claude larger model (MDL-L1) in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-1014 | classification | Public | IN | Claude larger model (MDL-L1) | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1015 | classification | Public | IN | Free Tier 2 provider | candidate | ok | Not routed: registry state `candidate`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1016 | classification | Public | IN | Free Tier 2 provider | eval suite failed | ok | Not routed: registry state `eval suite failed`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1017 | classification | Internal (non-personal) | IN | Claude Sonnet (approved primary) | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1018 | classification | Internal (non-personal) | IN | Claude larger model (MDL-L1) | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1019 | classification | Internal (non-personal) | IN | Claude larger model (MDL-L1) | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1020 | classification | Internal (non-personal) | IN | Free Tier 2 provider | approved | ok | Not routed: no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1021 | classification | Internal (non-personal) | IN | Free Tier 2 provider | candidate | ok | Not routed: registry state `candidate`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1022 | classification | Internal (non-personal) | IN | Free Tier 2 provider | eval suite failed | ok | Not routed: registry state `eval suite failed`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1023 | classification | Personal (masked) | IN | Claude Sonnet (approved primary) | approved | ok | Routed to Claude Sonnet (approved primary) in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-1024 | classification | Personal (masked) | IN | Claude Sonnet (approved primary) | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1025 | classification | Personal (masked) | IN | Claude larger model (MDL-L1) | approved | ok | Routed to Claude larger model (MDL-L1) in IN; run record stores `mdl_id`, version, region, prompt version | P1 | T14 | PW3 | Y | SYS |
| TC-V12-R-1026 | classification | Personal (masked) | IN | Free Tier 2 provider | suspended | ok | Not routed: registry state `suspended`; no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1027 | classification | Personal (masked) | IN | Free Tier 2 provider | DPA expired | ok | Not routed: registry state `DPA expired`; no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1028 | classification | Personal (unmasked) | IN | Claude Sonnet (approved primary) | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1029 | classification | Personal (unmasked) | IN | Claude Sonnet (approved primary) | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1030 | classification | Personal (unmasked) | IN | Claude Haiku-class | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1031 | classification | Personal (unmasked) | IN | Claude larger model (MDL-L1) | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1032 | classification | Personal (unmasked) | IN | Claude larger model (MDL-L1) | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1033 | classification | Personal (unmasked) | IN | Google Gemini | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1034 | classification | Personal (unmasked) | IN | Free Tier 2 provider | approved | ok | Not routed: no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1035 | classification | Personal (unmasked) | IN | Free Tier 2 provider | DPA expired | ok | Not routed: registry state `DPA expired`; no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1036 | classification | Personal (unmasked) | IN | Free Tier 2 provider | eval suite failed | ok | Not routed: registry state `eval suite failed`; no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant). Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1037 | classification | Restricted | IN | Claude Sonnet (approved primary) | approved | ok | Routed to Claude Sonnet (approved primary) in IN; run record stores `mdl_id`, version, region, prompt version | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1038 | classification | Restricted | IN | Claude Sonnet (approved primary) | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1039 | classification | Restricted | IN | Claude Haiku-class | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1040 | classification | Restricted | IN | Claude larger model (MDL-L1) | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1041 | classification | Restricted | IN | Google Gemini | candidate | ok | Not routed: registry state `candidate`; Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1042 | classification | Restricted | IN | Free Tier 2 provider | approved | ok | Not routed: no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant); Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1043 | classification | Restricted | IN | Free Tier 2 provider | suspended | ok | Not routed: registry state `suspended`; no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant); Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1044 | classification | Restricted | IN | Free Tier 2 provider | DPA expired | ok | Not routed: registry state `DPA expired`; no approved IN processing location; Tier 2 accepts Public/Internal-non-personal only (invariant); Restricted data only to rows with a signed DPA, no-training, in-zone processing and a Restricted approval. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1045 | embedding | Public | IN | OpenAI GPT family | suspended | ok | Not routed: registry state `suspended`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1046 | embedding | Internal (non-personal) | IN | OpenAI GPT family | candidate | ok | Not routed: registry state `candidate`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1047 | embedding | Internal (non-personal) | IN | OpenAI GPT family | DPA expired | ok | Not routed: registry state `DPA expired`; no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1048 | embedding | Personal (masked) | IN | OpenAI GPT family | approved | ok | Not routed: no approved IN processing location. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1049 | safety screening | Public | IN | Claude Haiku-class | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1050 | safety screening | Public | IN | Claude Haiku-class | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1051 | safety screening | Internal (non-personal) | IN | Claude Haiku-class | candidate | ok | Not routed: registry state `candidate`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1052 | safety screening | Internal (non-personal) | IN | Claude Haiku-class | eval suite failed | ok | Not routed: registry state `eval suite failed`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1053 | safety screening | Personal (masked) | IN | Claude Haiku-class | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1054 | safety screening | Personal (unmasked) | IN | Claude Haiku-class | suspended | ok | Not routed: registry state `suspended`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |
| TC-V12-R-1055 | safety screening | Restricted | IN | Claude Haiku-class | DPA expired | ok | Not routed: registry state `DPA expired`. Router takes the next eligible approved row for (task, locale, class, region); if none: `HELD_FOR_REVIEWER` (quality) or Tier 3 template (availability). Never silently to an unapproved model | P0 | T14 | PW3 | Y | SYS |

#### Group TC-V12-R-M11: 3-way combinatorial cases – Cross-tenant benchmarks: cohort size × dominance × participation × metric × scope × owner flag × budget

**Common for TC-V12-R-1056…TC-V12-R-1099:** Pre: PP-05 benchmark pipeline (AU-299) with synthetic tenant set BM-FIX-1 in both zones; cohort industry "B2B software", size band "11–50". Steps: run the monthly aggregation for the period; open A042 dashboards, Benchmarks tab, as R12 of the viewer tenant; read `benchmark_cell`, `benchmark_privacy_ledger`. Links for every row: TS-V12-R-11 · US-17-ZR24, US-17-ZR25 · FR-V12-R-131…142; DEC-789; CONFLICT-983 resolution. Technique PW (3-way); generated by `assembly/v12b/R_02_combinatorics.py` (model M11).

| ID | cohort | dominance | participant | metric | scope | owner | budget | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-1056 | 9 tenants | no tenant > 30% | opted in | reply rate | IN zone | external tenant | ε budget available | Cell suppressed: "Not enough peers" (k = 9 < 10); no value, no count shown | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1057 | 9 tenants | no tenant > 30% | not opted in | lead-to-meeting cycle time | EU zone | Owner Portfolio startup without R01 opt-in | ε budget exhausted for the period | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1058 | 9 tenants | one tenant > 30% of events | opted in | win rate | global | Owner Portfolio startup with R01 opt-in | ε budget exhausted for the period | Cell suppressed: "Not enough peers" (k = 9 < 10); no value, no count shown | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1059 | 10 tenants | no tenant > 30% | withdrawn | lead-to-meeting cycle time | global | Owner Portfolio startup with R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1060 | 10 tenants | one tenant > 30% of events | not opted in | win rate | IN zone | Owner Portfolio startup without R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1061 | 10 tenants | one tenant > 30% of events | withdrawn | reply rate | EU zone | external tenant | ε budget exhausted for the period | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1062 | 25 tenants | no tenant > 30% | not opted in | reply rate | IN zone | Owner Portfolio startup with R01 opt-in | ε budget exhausted for the period | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1063 | 25 tenants | one tenant > 30% of events | opted in | lead-to-meeting cycle time | EU zone | external tenant | ε budget available | Cell suppressed (dominance rule BM-03); no value shown | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1064 | 25 tenants | no tenant > 30% | withdrawn | win rate | EU zone | Owner Portfolio startup without R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1065 | 10 tenants | no tenant > 30% | not opted in | win rate | global | external tenant | ε budget exhausted for the period | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1066 | 9 tenants | one tenant > 30% of events | withdrawn | reply rate | global | Owner Portfolio startup without R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1067 | 25 tenants | one tenant > 30% of events | withdrawn | lead-to-meeting cycle time | IN zone | Owner Portfolio startup without R01 opt-in | ε budget exhausted for the period | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1068 | 9 tenants | one tenant > 30% of events | not opted in | reply rate | EU zone | Owner Portfolio startup with R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1069 | 10 tenants | no tenant > 30% | opted in | reply rate | global | Owner Portfolio startup without R01 opt-in | ε budget exhausted for the period | Owned startup excluded (BM-06); viewer sees benchmark built without its data | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-1070 | 9 tenants | no tenant > 30% | withdrawn | win rate | IN zone | external tenant | ε budget exhausted for the period | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1071 | 10 tenants | one tenant > 30% of events | opted in | lead-to-meeting cycle time | IN zone | Owner Portfolio startup with R01 opt-in | ε budget exhausted for the period | Cell suppressed (dominance rule BM-03); no value shown | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1072 | 25 tenants | one tenant > 30% of events | not opted in | lead-to-meeting cycle time | global | external tenant | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1073 | 10 tenants | no tenant > 30% | opted in | win rate | EU zone | Owner Portfolio startup with R01 opt-in | ε budget available | Published: win rate cell with Laplace noise (ε = 0.5 per metric per period), clipped contributions, rounded; computed in Frankfurt from EU tenants only; shows k band (10–24 / 25+) not exact n | P1 | T19 | PW3 | Y | SYS |
| TC-V12-R-1074 | 25 tenants | no tenant > 30% | opted in | lead-to-meeting cycle time | global | external tenant | ε budget exhausted for the period | No new release this period; last published value shown with its period label; ledger entry `budget_exhausted` | P1 | T19 | PW3 | Y | SYS |
| TC-V12-R-1075 | 25 tenants | one tenant > 30% of events | withdrawn | win rate | EU zone | Owner Portfolio startup with R01 opt-in | ε budget exhausted for the period | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1076 | 9 tenants | one tenant > 30% of events | opted in | lead-to-meeting cycle time | IN zone | Owner Portfolio startup without R01 opt-in | ε budget available | Owned startup excluded (BM-06); viewer sees benchmark built without its data | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-1077 | 25 tenants | one tenant > 30% of events | withdrawn | reply rate | IN zone | external tenant | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1078 | 9 tenants | no tenant > 30% | not opted in | win rate | EU zone | external tenant | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1079 | 25 tenants | one tenant > 30% of events | opted in | reply rate | EU zone | Owner Portfolio startup without R01 opt-in | ε budget exhausted for the period | Owned startup excluded (BM-06); viewer sees benchmark built without its data | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-1080 | 10 tenants | no tenant > 30% | not opted in | lead-to-meeting cycle time | IN zone | external tenant | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1081 | 9 tenants | no tenant > 30% | withdrawn | reply rate | global | Owner Portfolio startup with R01 opt-in | ε budget exhausted for the period | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1082 | 25 tenants | no tenant > 30% | opted in | win rate | IN zone | Owner Portfolio startup with R01 opt-in | ε budget available | Published: win rate cell with Laplace noise (ε = 0.5 per metric per period), clipped contributions, rounded; computed in Mumbai from IN tenants only; shows k band (10–24 / 25+) not exact n | P1 | T19 | PW3 | Y | SYS |
| TC-V12-R-1083 | 25 tenants | one tenant > 30% of events | not opted in | win rate | global | Owner Portfolio startup without R01 opt-in | ε budget exhausted for the period | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1084 | 9 tenants | one tenant > 30% of events | withdrawn | lead-to-meeting cycle time | global | external tenant | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1085 | 10 tenants | one tenant > 30% of events | not opted in | reply rate | global | Owner Portfolio startup with R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1086 | 10 tenants | no tenant > 30% | withdrawn | reply rate | IN zone | Owner Portfolio startup without R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1087 | 10 tenants | one tenant > 30% of events | opted in | win rate | global | external tenant | ε budget available | Cell suppressed (dominance rule BM-03); no value shown | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1088 | 9 tenants | no tenant > 30% | not opted in | lead-to-meeting cycle time | IN zone | Owner Portfolio startup with R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1089 | 10 tenants | no tenant > 30% | not opted in | reply rate | EU zone | Owner Portfolio startup without R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1090 | 9 tenants | no tenant > 30% | opted in | win rate | EU zone | Owner Portfolio startup without R01 opt-in | ε budget available | Owned startup excluded (BM-06); viewer sees benchmark built without its data | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-1091 | 9 tenants | no tenant > 30% | not opted in | reply rate | global | external tenant | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1092 | 9 tenants | no tenant > 30% | withdrawn | lead-to-meeting cycle time | EU zone | Owner Portfolio startup with R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1093 | 25 tenants | no tenant > 30% | opted in | reply rate | global | Owner Portfolio startup with R01 opt-in | ε budget available | Published: reply rate cell with Laplace noise (ε = 0.5 per metric per period), clipped contributions, rounded; composed from the two noised regional cells only (no raw data crosses zones); shows k band (10–24 / 25+) not exact n | P1 | T19 | PW3 | Y | SYS |
| TC-V12-R-1094 | 25 tenants | no tenant > 30% | withdrawn | win rate | global | external tenant | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1095 | 10 tenants | no tenant > 30% | opted in | lead-to-meeting cycle time | EU zone | Owner Portfolio startup without R01 opt-in | ε budget available | Owned startup excluded (BM-06); viewer sees benchmark built without its data | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-1096 | 10 tenants | no tenant > 30% | withdrawn | win rate | IN zone | Owner Portfolio startup with R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); withdrawal applies from the next period; published cells are not recomputed | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1097 | 25 tenants | no tenant > 30% | not opted in | lead-to-meeting cycle time | EU zone | Owner Portfolio startup with R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |
| TC-V12-R-1098 | 9 tenants | no tenant > 30% | opted in | lead-to-meeting cycle time | global | Owner Portfolio startup without R01 opt-in | ε budget available | Owned startup excluded (BM-06); viewer sees benchmark built without its data | P0 | T15 | PW3 | Y | SYS |
| TC-V12-R-1099 | 9 tenants | no tenant > 30% | not opted in | win rate | IN zone | Owner Portfolio startup with R01 opt-in | ε budget available | Tenant excluded from contributions and **cannot view** benchmarks (reciprocity rule BM-04); A042 Benchmarks tab shows the opt-in explanation | P0 | T19 | PW3 | Y | SYS |

#### Group TC-V12-R-M12: Pairwise combinatorial cases – Supabase access model: database role × context × operation × path

**Common for TC-V12-R-1100…TC-V12-R-1127:** Pre: PP-05 against a Supabase branch project per region with DDL-V12-I + DDL-V12-R applied; Data API settings as production. Steps: connect as the role through the path in the row, set the context, run the operation; read results, `pg_stat_activity` detector output and audit. Links for every row: TS-V12-R-12 · US-01-ZR26, US-01-ZR27 · FR-V12-R-143…155; DEC-778; SB-01…SB-10. Technique PW; generated by `assembly/v12b/R_02_combinatorics.py` (model M12).

| ID | role | context | op | path | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-1100 | app_rw | tenant and companies set | SELECT own rows | Django API | rows of the tenant and permitted companies only | P1 | T15 | PW | Y | IT |
| TC-V12-R-1101 | app_rw | app.tenant_id not set | INSERT own row | Celery worker | RLS denies: SELECT returns 0 rows, INSERT/UPDATE fail `WITH CHECK`; `ge.require_ctx()` raises `CONTEXT_MISSING` | P0 | T15 | PW | Y | IT |
| TC-V12-R-1102 | app_rw | company not in app.company_ids | UPDATE row of another tenant | CI migration (normal) | app_rw used by the migration job: refused by the pipeline policy (migrations run as app_migrator) | P1 | T07 | PW | Y | IT |
| TC-V12-R-1103 | app_worker | tenant and companies set | INSERT own row | CI migration (normal) | app_worker used by the migration job: refused by the pipeline policy (migrations run as app_migrator) | P1 | T07 | PW | Y | IT |
| TC-V12-R-1104 | app_worker | app.tenant_id not set | SELECT own rows | CI migration with break-glass approval | app_worker used by the migration job: refused by the pipeline policy (migrations run as app_migrator) | P1 | T07 | PW | Y | IT |
| TC-V12-R-1105 | app_worker | company not in app.company_ids | DELETE own row | Django API | 0 rows for SELECT; INSERT rejected by WITH CHECK on company scope | P0 | T15 | PW | Y | IT |
| TC-V12-R-1106 | app_migrator | tenant and companies set | UPDATE row of another tenant | Celery worker | Login refused: `app_migrator` may connect only from the CI runner IP set | P0 | T07 | PW | Y | IT |
| TC-V12-R-1107 | app_migrator | app.tenant_id not set | DELETE own row | CI migration (normal) | DDL allowed (`SET ROLE app_owner`); no DML on tenant rows except reviewed backfills | P1 | T07 | PW | Y | IT |
| TC-V12-R-1108 | app_migrator | company not in app.company_ids | INSERT own row | CI migration with break-glass approval | DDL allowed (`SET ROLE app_owner`); no DML on tenant rows except reviewed backfills | P1 | T07 | PW | Y | IT |
| TC-V12-R-1109 | service_role | tenant and companies set | DELETE own row | CI migration with break-glass approval | Allowed only for the migration job; audit `db.break_glass.used` with approver, ticket and expiry ≤ 2 h; SEV3 notice to R10 | P0 | T07 | PW | Y | IT |
| TC-V12-R-1110 | service_role | app.tenant_id not set | UPDATE row of another tenant | Django API | Blocked: secret not present in API/worker task definitions (VD/SB policy check fails the deploy); runtime detector AU-292 raises SEV2 if a session with this role appears from an app subnet | P0 | T07 | PW | Y | IT |
| TC-V12-R-1111 | service_role | company not in app.company_ids | SELECT own rows | Celery worker | Blocked: secret not present in API/worker task definitions (VD/SB policy check fails the deploy); runtime detector AU-292 raises SEV2 if a session with this role appears from an app subnet | P0 | T07 | PW | Y | IT |
| TC-V12-R-1112 | anon via Data API | tenant and companies set | SELECT own rows | Browser | Data API disabled for application schemas: 404 from the Data API; even if re-enabled, `permission denied` (no grants on schema `ge`); NSE | P0 | T07 | PW | Y | IT |
| TC-V12-R-1113 | authenticated via Data API | app.tenant_id not set | INSERT own row | Browser | Data API disabled for application schemas: 404 from the Data API; even if re-enabled, `permission denied` (no grants on schema `ge`); NSE | P0 | T07 | PW | Y | IT |
| TC-V12-R-1114 | postgres | tenant and companies set | SELECT own rows | CI migration (normal) | Blocked: secret not present in API/worker task definitions (VD/SB policy check fails the deploy); runtime detector AU-292 raises SEV2 if a session with this role appears from an app subnet | P0 | T07 | PW | Y | IT |
| TC-V12-R-1115 | postgres | app.tenant_id not set | INSERT own row | Django API | Blocked: secret not present in API/worker task definitions (VD/SB policy check fails the deploy); runtime detector AU-292 raises SEV2 if a session with this role appears from an app subnet | P0 | T07 | PW | Y | IT |
| TC-V12-R-1116 | postgres | company not in app.company_ids | UPDATE row of another tenant | CI migration with break-glass approval | Allowed only for the migration job; audit `db.break_glass.used` with approver, ticket and expiry ≤ 2 h; SEV3 notice to R10 | P0 | T07 | PW | Y | IT |
| TC-V12-R-1117 | anon via Data API | company not in app.company_ids | UPDATE row of another tenant | Browser | Data API disabled for application schemas: 404 from the Data API; even if re-enabled, `permission denied` (no grants on schema `ge`); NSE | P0 | T07 | PW | Y | IT |
| TC-V12-R-1118 | postgres | tenant and companies set | DELETE own row | Celery worker | Blocked: secret not present in API/worker task definitions (VD/SB policy check fails the deploy); runtime detector AU-292 raises SEV2 if a session with this role appears from an app subnet | P0 | T07 | PW | Y | IT |
| TC-V12-R-1119 | anon via Data API | app.tenant_id not set | DELETE own row | Browser | Data API disabled for application schemas: 404 from the Data API; even if re-enabled, `permission denied` (no grants on schema `ge`); NSE | P0 | T07 | PW | Y | IT |
| TC-V12-R-1120 | app_rw | tenant and companies set | DELETE own row | CI migration with break-glass approval | app_rw used by the migration job: refused by the pipeline policy (migrations run as app_migrator) | P1 | T07 | PW | Y | IT |
| TC-V12-R-1121 | app_worker | tenant and companies set | UPDATE row of another tenant | Celery worker | 0 rows affected (RLS USING); audit anomaly counter if the API expected 1 | P0 | T15 | PW | Y | IT |
| TC-V12-R-1122 | app_migrator | tenant and companies set | SELECT own rows | Django API | Login refused: `app_migrator` may connect only from the CI runner IP set | P0 | T07 | PW | Y | IT |
| TC-V12-R-1123 | service_role | tenant and companies set | INSERT own row | CI migration (normal) | Blocked: secret not present in API/worker task definitions (VD/SB policy check fails the deploy); runtime detector AU-292 raises SEV2 if a session with this role appears from an app subnet | P0 | T07 | PW | Y | IT |
| TC-V12-R-1124 | authenticated via Data API | tenant and companies set | SELECT own rows | Browser | Data API disabled for application schemas: 404 from the Data API; even if re-enabled, `permission denied` (no grants on schema `ge`); NSE | P0 | T07 | PW | Y | IT |
| TC-V12-R-1125 | authenticated via Data API | company not in app.company_ids | UPDATE row of another tenant | Browser | Data API disabled for application schemas: 404 from the Data API; even if re-enabled, `permission denied` (no grants on schema `ge`); NSE | P0 | T07 | PW | Y | IT |
| TC-V12-R-1126 | anon via Data API | tenant and companies set | INSERT own row | Browser | Data API disabled for application schemas: 404 from the Data API; even if re-enabled, `permission denied` (no grants on schema `ge`); NSE | P0 | T07 | PW | Y | IT |
| TC-V12-R-1127 | authenticated via Data API | tenant and companies set | DELETE own row | Browser | Data API disabled for application schemas: 404 from the Data API; even if re-enabled, `permission denied` (no grants on schema `ge`); NSE | P0 | T07 | PW | Y | IT |

#### Group TC-V12-R-M13: Pairwise combinatorial cases – Registry approval: modality × evidence × approvers (exhaustive)

**Common for TC-V12-R-1128…TC-V12-R-1172:** Pre: PP-01 A114 model registry; candidate row with the evidence set in the row. Steps: R10 approves, then the second approver approves; read row state and audit. Links for every row: TS-V12-R-13 · US-04-ZR21 · FR-V12-R-111…118; DEC-788. Technique PW and exhaustive; generated by `assembly/v12b/R_02_combinatorics.py` (model M13).

| ID | modality | evidence | approvers | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|
| TC-V12-R-1128 | text LLM | complete | two distinct approvers | Row `approved` for text LLM with a 12-month re-certification date; routable only for listed task classes | P1 | T19 | EXH | Y | SYS |
| TC-V12-R-1129 | text LLM | complete | one approver | Approval refused: two distinct authorised approvers required (R10 AI governance + R01 or delegate); row stays `candidate` | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1130 | text LLM | complete | same person twice | Second approval rejected `SAME_APPROVER`; row stays `candidate` | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1131 | text LLM | DPA no-training clause | two distinct approvers | Approval refused: evidence missing "DPA no-training clause"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1132 | text LLM | region/processing location | two distinct approvers | Approval refused: evidence missing "region/processing location"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1133 | text LLM | EVAL suites | two distinct approvers | Approval refused: evidence missing "EVAL suites"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1134 | text LLM | red-team pass | two distinct approvers | Approval refused: evidence missing "red-team pass"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1135 | text LLM | security review | two distinct approvers | Approval refused: evidence missing "security review"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1136 | text LLM | cost per accepted result | two distinct approvers | Approval refused: evidence missing "cost per accepted result"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1137 | embedding | complete | two distinct approvers | Row `approved` for embedding with a 12-month re-certification date; routable only for listed task classes | P1 | T19 | EXH | Y | SYS |
| TC-V12-R-1138 | embedding | complete | one approver | Approval refused: two distinct authorised approvers required (R10 AI governance + R01 or delegate); row stays `candidate` | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1139 | embedding | complete | same person twice | Second approval rejected `SAME_APPROVER`; row stays `candidate` | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1140 | embedding | DPA no-training clause | two distinct approvers | Approval refused: evidence missing "DPA no-training clause"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1141 | embedding | region/processing location | two distinct approvers | Approval refused: evidence missing "region/processing location"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1142 | embedding | EVAL suites | two distinct approvers | Approval refused: evidence missing "EVAL suites"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1143 | embedding | red-team pass | two distinct approvers | Approval refused: evidence missing "red-team pass"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1144 | embedding | security review | two distinct approvers | Approval refused: evidence missing "security review"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1145 | embedding | cost per accepted result | two distinct approvers | Approval refused: evidence missing "cost per accepted result"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1146 | image generation | complete | two distinct approvers | Row `approved` for image generation with a 12-month re-certification date; routable only for listed task classes | P1 | T19 | EXH | Y | SYS |
| TC-V12-R-1147 | image generation | complete | one approver | Approval refused: two distinct authorised approvers required (R10 AI governance + R01 or delegate); row stays `candidate` | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1148 | image generation | complete | same person twice | Second approval rejected `SAME_APPROVER`; row stays `candidate` | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1149 | image generation | DPA no-training clause | two distinct approvers | Approval refused: evidence missing "DPA no-training clause"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1150 | image generation | region/processing location | two distinct approvers | Approval refused: evidence missing "region/processing location"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1151 | image generation | EVAL suites | two distinct approvers | Approval refused: evidence missing "EVAL suites"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1152 | image generation | red-team pass | two distinct approvers | Approval refused: evidence missing "red-team pass"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1153 | image generation | security review | two distinct approvers | Approval refused: evidence missing "security review"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1154 | image generation | cost per accepted result | two distinct approvers | Approval refused: evidence missing "cost per accepted result"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1155 | video generation | complete | two distinct approvers | Row `approved` for video generation with a 12-month re-certification date; routable only for listed task classes | P1 | T19 | EXH | Y | SYS |
| TC-V12-R-1156 | video generation | complete | one approver | Approval refused: two distinct authorised approvers required (R10 AI governance + R01 or delegate); row stays `candidate` | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1157 | video generation | complete | same person twice | Second approval rejected `SAME_APPROVER`; row stays `candidate` | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1158 | video generation | DPA no-training clause | two distinct approvers | Approval refused: evidence missing "DPA no-training clause"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1159 | video generation | region/processing location | two distinct approvers | Approval refused: evidence missing "region/processing location"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1160 | video generation | EVAL suites | two distinct approvers | Approval refused: evidence missing "EVAL suites"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1161 | video generation | red-team pass | two distinct approvers | Approval refused: evidence missing "red-team pass"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1162 | video generation | security review | two distinct approvers | Approval refused: evidence missing "security review"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1163 | video generation | cost per accepted result | two distinct approvers | Approval refused: evidence missing "cost per accepted result"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1164 | voice (TTS/ASR) | complete | two distinct approvers | Row `approved` for voice (TTS/ASR) with a 12-month re-certification date; routable only for listed task classes | P1 | T19 | EXH | Y | SYS |
| TC-V12-R-1165 | voice (TTS/ASR) | complete | one approver | Approval refused: two distinct authorised approvers required (R10 AI governance + R01 or delegate); row stays `candidate` | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1166 | voice (TTS/ASR) | complete | same person twice | Second approval rejected `SAME_APPROVER`; row stays `candidate` | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1167 | voice (TTS/ASR) | DPA no-training clause | two distinct approvers | Approval refused: evidence missing "DPA no-training clause"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1168 | voice (TTS/ASR) | region/processing location | two distinct approvers | Approval refused: evidence missing "region/processing location"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1169 | voice (TTS/ASR) | EVAL suites | two distinct approvers | Approval refused: evidence missing "EVAL suites"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1170 | voice (TTS/ASR) | red-team pass | two distinct approvers | Approval refused: evidence missing "red-team pass"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1171 | voice (TTS/ASR) | security review | two distinct approvers | Approval refused: evidence missing "security review"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |
| TC-V12-R-1172 | voice (TTS/ASR) | cost per accepted result | two distinct approvers | Approval refused: evidence missing "cost per accepted result"; AU-298 checklist shows the gap | P0 | T19 | EXH | Y | SYS |


---

## 11.19.6 Conflicts and proposed resolutions

All conflicts that earlier groups raised on these topics are closed by the Founder decisions; this part records how each is implemented. The new conflicts (1091–1095) are differences between earlier blueprint text and the decisions; each is resolved here, none is pending.

| Conflict | Subject | Earlier position | Resolution implemented | Status |
|---|---|---|---|---|
| CONFLICT-760 / 834 / 887 | Enterprise identity scope and timing | Specified; SCIM and custom roles R2; Release 1 budget fixed | DEC-784 → all in Release 1 (DEC-880, 881, 898); §11.19.5.1 | Resolved |
| CONFLICT-886 | Developer platform timing | ENT-API R1/R2/R3 | DEC-785 → all in Release 1 (DEC-882, 883, 899); §11.19.5.2 | Resolved |
| CONFLICT-888 / 776 | Connector kinds; X-09 CRM exclusion | One CRM in R1 pending; SMS pending; voice W6 | DEC-785 → three CRMs, SMS-DLT, voice transport in Release 1 (DEC-884, 885); §11.19.5.3 | Resolved |
| CONFLICT-889 | Personal data through Vercel | DEC-421 "no personal data in functions"; option A recommended | DEC-786 → regional projects, controls VD-01…12, DEC-886/887; §11.19.5.4 | Resolved |
| CONFLICT-833 | RPO 15 min, WAL, PITR 35 days | Daily backups; PITR at growth gate | DEC-787 → dual path P1 + P2 (DEC-888/889); §11.19.5.5 | Resolved |
| CONFLICT-850, 851, 853, 855, 857 (852 via DEC-772) | Provider-neutral registry; MDL-S1 open-weight; MDL-L1 and multimodal; 111 suites; fallback rule | DEC-418 Claude-only routing; Tier 2 free | DEC-788 → registry with zone routing and Claude Sonnet approved primary (DEC-890…892); §11.19.5.6 | Resolved |
| CONFLICT-983 | Cross-tenant benchmarks | AU-143 proposal, pending | DEC-789 → C7 with DP (DEC-893); §11.19.5.7 | Resolved |
| [CONFLICT-1091] | V12 phases SCIM, custom roles, SIEM, JIT (R2), OAuth CC, portal, sandbox, versioning (R2), SDKs (R3) vs DEC-784/785 "Release 1" | V12 phase column | Founder decision prevails; phase column amended for the blueprint (§11.19.4.1); V12 IDs and acceptance unchanged | Resolved (DEC-881, 882) |
| [CONFLICT-1092] | Database role names: DEC-778 "one canonical name `app_rw`" vs Part 11.9b DDL `ge_app`/`ge_worker`/`ge_owner` | Part 11.9b SB-04 | Canonical `app_*` names; idempotent rename DDL-V12-R-16; Part 11.9b not edited (reported) | Resolved (DEC-894) |
| [CONFLICT-1093] | Part 11.8b scope registry text "consequential actions stay capped at L1" vs DEC-779 bounded mandates | Part 11.8b §11.8.5.4 | API still has no consequential scope; consequential execution only through the Part 11.17 mandate engine, never by API scope | Resolved (DEC-883) |
| [CONFLICT-1094] | Part 11.9b `ai_model_t2_data_ck` (tier T2 non-personal) cannot express DEC-788 open-weight masked personal | Part 11.9b C3 | Hosting-based checks replace tier-based check (DDL-V12-R-14); free third-party still non-personal only | Resolved (DEC-890) |
| [CONFLICT-1095] | AU-143 parameters (ε = 1, W6+/A4, k ≥ 10) vs DEC-789 implementation | Part 11.13b | AU-299 supersedes AU-143: ε = 0.5 per metric per month, yearly cap 6, reciprocity, zone-local computation, Release 2 | Resolved (DEC-893) |

---

## 11.19.7 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-880 | Tenant federation uses the reused IdP as broker per connection; Okta, Entra ID, Google Workspace certified plus generic SAML 2.0 and OIDC; up to 5 connections per tenant; fallback in-product SP behind a flag if Sprint 0 check 13 fails | Customer revision V12 (28 Nov 2026); implements Founder DEC-784 | ADR-255; §11.19.5.1 |
| DEC-881 | SCIM 2.0, custom roles, SIEM streaming and JIT support access move into Release 1; de-provisioning ≤ 60 s product side and ≤ 15 min end to end (binding); group-to-role mappings need a second approver | Customer revision V12 (28 Nov 2026); implements Founder DEC-784 | Amends the V12 phase column (CONFLICT-1091) |
| DEC-882 | Developer platform fully in Release 1: zone-bound API keys, OAuth client credentials (private_key_jwt preferred), rate limits, URL versioning with 12-month notice, signed webhooks with fixed 24 h schedule, portal, SDKs in TypeScript, Python and Java | Customer revision V12 (28 Nov 2026); implements Founder DEC-785 | ADR-257/258 |
| DEC-883 | No API scope exists for consequential actions; consequential execution happens only by a human with step-up or under a Part 11.17 bounded mandate | Customer revision V12 (28 Nov 2026); consistent with DEC-779 | Closes CONFLICT-1093 |
| DEC-884 | Connectors in Release 1: framework and gate (with counsel-approved rule pack per market), CRM adapters for Zoho CRM, HubSpot and Salesforce (all BYO), SMS via a DLT-registered aggregator, voice CPaaS transport (140/160 series) | Customer revision V12 (28 Nov 2026); implements Founder DEC-785 | Supersedes RECOMMENDATION-902; ADR-259 |
| DEC-885 | Platform is system of record for consent, suppression, approvals, mandates, audit and AI outputs; CRM opt-outs import as suppression; other fields by per-field policy with a conflict queue | Customer revision V12 (28 Nov 2026) | DDL protected-field check |
| DEC-886 | Vercel: one project per surface per zone, functions pinned to bom1/fra1 (verify), Edge Middleware non-personal only, header allowlist, origin verify, metadata-only logs, no caching of personal responses, VD-01…12 enforced by CI and AU-296 | Customer revision V12 (28 Nov 2026); implements Founder DEC-786 | Amends DEC-421 hosting statement; ADR-260 |
| DEC-887 | TLS termination at a Vercel edge location outside the zone is treated as transit; storage and processing stay in-zone; the position is written into the IN and EU rule packs and needs counsel sign-off before the first EU tenant | Customer revision V12 (28 Nov 2026); legal gate per Part 11.15 | GAP-1088 |
| DEC-888 | RPO ≤ 15 min through two independent paths per zone: Supabase PITR and an in-zone AWS standby with WAL-G continuous archiving and daily base backups; drills at each release gate and quarterly | Customer revision V12 (28 Nov 2026); implements Founder DEC-787 (and DEC-771) | ADR-261 |
| DEC-889 | The 35-day PITR window is guaranteed by the WAL-G archive when the Supabase option is shorter; archives replicate only inside the zone | Customer revision V12 (28 Nov 2026) | ASSUMPTION-1081 |
| DEC-890 | Registry rows by provider × version × hosting × zone × modality; seven evidence items; two distinct approvers; 12-month re-certification and event triggers (AU-298); Tier 2 free rows only if they pass the same gate and only for non-personal data | Customer revision V12 (28 Nov 2026); implements Founder DEC-788 | Resolves CONFLICT-857/1094; ADR-262 |
| DEC-891 | Model routing is zone-aware: EU tenants only to rows with EU processing; India tenants only to rows permitted for India; otherwise HOLD/Tier 3, never cross-zone | Customer revision V12 (28 Nov 2026); DEC-772 | ASSUMPTION-1083 |
| DEC-892 | Advanced tier (MDL-L1) and multimodal rows (image, video, voice) are registered and activate on approval; Claude Sonnet remains primary for MDL-M1 by Founder approval | Customer revision V12 (28 Nov 2026); implements Founder DEC-788 | — |
| DEC-893 | Benchmarks: opt-in under clause BM-CL-1, reciprocity, k ≥ 10, dominance ≤ 30%, tenant-level DP with Laplace ε = 0.5 per metric per cell per month (yearly cap 6), zone-local computation, Owner Portfolio excluded unless R01 opts in; built in Release 2 | Customer revision V12 (28 Nov 2026); implements Founder DEC-789 | Supersedes AU-143 parameters; ADR-263 |
| DEC-894 | Canonical database roles `app_owner`, `app_migrator`, `app_rw`, `app_worker`, `app_readonly`, `app_retention`, `app_platform_sec`, `app_bench`, `app_registry`; all NOBYPASSRLS; Data API off; `service_role` only for CI migrations under two-person, time-boxed break-glass | Customer revision V12 (28 Nov 2026); implements DEC-778 | Resolves CONFLICT-1092; ADR-264 |
| DEC-895 | A global, non-personal tenant directory resolves the zone before any personal data is processed; misdirected requests get 421 and are never proxied across zones; residency is chosen at onboarding | Customer revision V12 (28 Nov 2026); DEC-772/776 | §11.19.5.0 |
| DEC-896 | Feature flags per capability default off until each activation gate passes; owned startups adopt SSO and connectors first | Customer revision V12 (28 Nov 2026) | §11.19.5.12 |
| DEC-897 | Proposal CR-V12-R-01: net development 120 / 176 / 253 pd (₹5.45 / 10.00 / 17.25 L), external ₹4.6–10.8 L, running ₹15,300–54,000 per month per zone (excluding the conditional open-weight line); funded under DEC-790 | Customer revision V12 (28 Nov 2026); funding by Founder DEC-790 | Development and running in separate tables (§11.19.5.13) |
| DEC-898 | SoD matrix extended by eight pairs (finance dual verification, billing, roles, mandates, connectors, models, benchmarks, unmasked scopes); quarterly access recertification | Customer revision V12 (28 Nov 2026); implements Founder DEC-784 | §11.19.5.1.F |
| DEC-899 | Sandbox tenants (synthetic only) and configuration promotion in Release 1 | Customer revision V12 (28 Nov 2026); implements Founder DEC-785 | ENT-DAT-04/05 |

---

## 11.19.8 Expert persona review

| Persona | Verdict | Findings and how they were addressed |
|---|---|---|
| Identity architect (SAML/OIDC, SCIM, SoD) | Approve | Insisted on XSW corpus testing, assertion-ID replay cache, `amr`-based MFA acceptance and step-up, break-glass with hardware keys, no auto-unenforce on DNS loss, group mappings with second approver, SoD at four enforcement points including the DB trigger. All present (§11.19.5.1, TC-V12-R-001…020, M01–M03). Residual risk: broker capability (RSK-V12-R-01) with flagged fallback |
| Developer-platform product lead | Approve | Zone in key format avoids cross-region lookup; private_key_jwt preferred; webhook verification challenge and SSRF re-check per delivery; SDKs generated with thin helpers to keep three languages maintainable; deprecation 12 months. Asked for SDK provenance (RECOMMENDATION-1097) and leak-response partner registration (RECOMMENDATION-1098) |
| Integration architect (CRM, SMS-DLT, voice) | Approve with conditions | Platform must stay authoritative for consent (DEC-885, DDL check); Salesforce edition limits are real (ASSUMPTION-1086); DLT IDs and scrubbing must be enforced in the PDP, not only in the adapter (done); voice series/purpose check in DDL. Condition: DLT registration starts in Sprint 0 (RSK-V12-R-03) |
| Privacy and cloud-security lead | Approve with condition | Per-zone projects and VD rules make DEC-786 enforceable; condition: counsel opinion on edge transit before the first EU tenant (DEC-887, GAP-1088), and Vercel analytics features kept off on authenticated surfaces |
| Database reliability engineer | Approve | Dual path removes single-provider dependence; logical replication caveats (DDL, sequences) handled; RPO measured every 30 s; drills produce evidence; canonical roles with CI assertions close the RLS bypass (DEC-778) |
| LLM platform lead | Approve | Registry rows include hosting and zone, so open-weight masked personal and free-tier non-personal are expressible as DB checks; zone-aware routing prevents silent transfer; Claude Sonnet primary recorded as an approval, not hard-coded |
| Privacy-preserving analytics scientist | Approve with condition | Tenant-level DP with clipping is stronger than k-anonymity alone; ε = 0.5 monthly with a yearly cap is conservative for 5 metrics; global cells by post-processing; condition: independent re-derivation before first publication (budgeted) |

---

## 11.19.9 Tags register

### 11.19.9.1 Tags issued in Part 11.19 (range 1080–1099, all used)

| Tag | Type | Statement | Where |
|---|---|---|---|
| [ASSUMPTION-1080] | Assumption | The reused AppNAI IdP can broker per-tenant SAML/OIDC with issuer/audience binding and `amr` passthrough; verified by Sprint 0 check 13; otherwise in-product SP | §11.19.5.1.A |
| [ASSUMPTION-1081] | Assumption | Supabase PITR retention options and granularity (possibly < 35 days); verify at time of implementation (as of 27 Nov 2026) | §11.19.5.5 |
| [ASSUMPTION-1082] | Assumption | Vercel function region identifiers `bom1`/`fra1`, region-pinning mechanism and log-content behaviour; verify (as of 27 Nov 2026) | §11.19.5.4 |
| [ASSUMPTION-1083] | Assumption | Model providers offer EU and/or India processing locations (directly or via cloud marketplaces); verify per row | §11.19.5.6 |
| [ASSUMPTION-1084] | Assumption | "Opt-in default" in DEC-789 means participation is off until the tenant opts in under the clause | §11.19.5.7 |
| [ASSUMPTION-1085] | Assumption | Benchmarks are built in Release 2 because cohorts of 10 tenants cannot exist before external tenants onboard | §11.19.0 |
| [ASSUMPTION-1086] | Assumption | CRM API access, change capture and limits depend on the tenant's edition (e.g. Salesforce API-enabled editions); verify | §11.19.5.3 |
| [ASSUMPTION-1087] | Assumption | The DLT aggregator offers scrubbing and template validation APIs; TRAI promotional window 10:00–21:00 IST; verify current regulations | §11.19.5.3 |
| [GAP-1088] | Gap | Legal position on TLS termination at out-of-zone edge locations needs counsel opinion (IN, EU) | DEC-887 |
| [GAP-1089] | Gap | AI voice behaviour on top of VoicePort is specified by Part 11.18; this part supplies the transport contract only | §11.19.5.3 |
| [GAP-1090] | Gap | Supabase dashboard SSO/MFA and organisation roles depend on the plan; confirm at implementation | SA-10 |
| [CONFLICT-1091] | Conflict | V12 phases vs Release 1 decisions | §11.19.6 (resolved) |
| [CONFLICT-1092] | Conflict | Role names `app_rw` vs `ge_app` | §11.19.6 (resolved) |
| [CONFLICT-1093] | Conflict | Part 11.8b "L1 cap" wording vs DEC-779 | §11.19.6 (resolved) |
| [CONFLICT-1094] | Conflict | `ai_model_t2_data_ck` vs DEC-788 open-weight masked personal | §11.19.6 (resolved) |
| [CONFLICT-1095] | Conflict | AU-143 parameters vs DEC-789 implementation | §11.19.6 (resolved) |
| [RECOMMENDATION-1096] | Recommendation | Hardware security keys for break-glass accounts | §11.19.5.1.A |
| [RECOMMENDATION-1097] | Recommendation | Signed SDK releases with registry provenance (npm provenance, PyPI trusted publishing, Maven Central signing; verify) | §11.19.5.2.A |
| [RECOMMENDATION-1098] | Recommendation | Register the `gek_` prefix with secret-scanning partner programmes (verify availability) | §11.19.5.2.A |
| [RECOMMENDATION-1099] | Recommendation | Use a vetted open-source DP library (e.g. OpenDP or Google's differential-privacy library; licence verify) for noise and accounting | §11.19.5.7 |

### 11.19.9.2 Inconsistencies found in earlier parts (reported, not edited)

| # | Part | Inconsistency | Handling here |
|---|---|---|---|
| 1 | Part 11.9b SB-04 and DDL | Role names `ge_app`/`ge_worker`/`ge_owner` vs DEC-778 canonical `app_rw` | Rename migration DDL-V12-R-16 (CONFLICT-1092) |
| 2 | Part 11.8b §11.8.5.4 | "Consequential actions stay capped at L1" predates DEC-779 | DEC-883 wording (CONFLICT-1093) |
| 3 | Part 11.9b C3 | `ai_model_t2_data_ck` tier-based | Replaced by hosting-based checks (CONFLICT-1094) |
| 4 | Part 11.8b §11.8.5.10 | Database row "service key server-side" | Superseded by DEC-778/894 |
| 5 | Part 11.13b AU-143, API-V12-M-24 | Benchmarks "disabled until DEC-747", ε = 1 | Superseded by AU-299, API-V12-R-051 |
| 6 | Part 11.8b AD-V12-H-03 | Voice "R3+ → W6" | Release 1 transport (DEC-884) |
| 7 | Part 11.5a ENT-IDN-01 data model | One `IdpConnection` per tenant in V12 C2 vs multi-connection | Compatibility view (FR-V12-R-029) |

---

## 11.19.10 Quality gate: Batch 11.19 (files a, b and c)

| # | Item | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | **Pass** | 662 V12 aspects in `final/coverage_v12/R_coverage.csv`; 155 FRs with source; every story and TC links FR/ENT/DEC |
| 2 | Assumptions/gaps/conflicts tagged and logged | **Pass** | 20 tags 1080–1099, all registered §11.19.9.1 |
| 3 | IDs unique and consistent with earlier parts | **Pass** | DEC-880…899, ADR-255…264, AU-290…299, FR-V12-R-001…155, US-<EP>-ZR01…29, TC-V12-R-001…086 and 101…1172; screen IDs per Part 11.7a mapping |
| 4 | No story lacks AC; no requirement lacks a test | **Pass** | 29 stories with Gherkin; every FR names a TC or model |
| 5 | Negative, edge, security and accessibility cases | **Pass** | 1,158 test cases; P0 negative and security rows in every model; accessibility AC-20ZR09-05 and strategy row |
| 6 | No agent lacks guardrail, fallback, KPI, cost | **Pass / N/A** | No new agents; AU-290…299 complete |
| 7 | Time-sensitive facts flagged "verify" | **Pass** | Provider features, regions, prices, TRAI windows, model IDs (as of 27 Nov 2026) |
| 8 | No restricted data routed to free-tier models | **Pass** | DDL `ai_model_free_tier_data_ck`; M10 oracle rows for Restricted/Personal never route to free or open-weight unmasked |
| 9 | Consistent with earlier parts | **Pass with reported items** | §11.19.9.2 |
| 10 | V12-B combinatorial rule (pairwise for all; 3-way for safety/money/law; exhaustive ≤ 64) | **Pass** | 13 models: 8 × 3-way, 3 × pairwise, 2 × exhaustive; script `assembly/v12b/R_02_combinatorics.py` |
| 11 | Mermaid renders | **Pass** | All Mermaid blocks render (15 in files a and b; file c has none); renderer check returns zero failures |

**Status: Part 11 Batch 11.19 (files a, b, c) complete. Founder decisions DEC-778 and DEC-784…789 implemented at full depth: 662 V12 aspects Matched, 155 FRs, 29 stories, 1,158 test cases (86 full form + 1,072 generated from 13 combinatorial models), 10 automations, 20 decisions, 10 ADRs; no item pending.**
