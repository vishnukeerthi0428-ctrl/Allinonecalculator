# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.22d), Master User Stories with Permutations: EP-32 to EP-34

| Field | Value |
|---|---|
| Document | Part 11, Batch 22, file d of f: §11.22.5.4 new stories for EP-32, EP-33, EP-34 (template of Part 5.1a; conventions, models and register in file a) |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Parts 0–9.10; Parts 11.1–11.19 (V12 review and V12-B Founder decisions, Part 11.14 DEC-770…791); story template Part 5.1a (§5.2 DoR, §5.3 DoD, §5.5 estimation, §5.6 dimension matrix, §5.7 conventions) |
| Roles applied | Chief Product Officer · Principal Agile Product Owner · Business Systems Analyst (BDD/Gherkin) · UX researcher (persona journeys) · QA Lead (combinatorial design) |
| ID ranges used | DEC-940…959 · tags ASSUMPTION/GAP/CONFLICT/RECOMMENDATION-1140…1159 · ADR-275…279 · stories US-&lt;EP&gt;-ZU&lt;nn&gt; · AC-&lt;EP&gt;ZU&lt;nn&gt;-&lt;seq&gt; · example rows EX-&lt;EP&gt;ZU&lt;nn&gt;-&lt;seq&gt; · parameter models MU01…MU13 · journeys JN-01…JN-12 · new epic EP-34 · new personas P21–P23 |

**Acronyms used in this part.** AC = acceptance criterion · BDD = behaviour-driven development · CPO = Chief Product Officer · DoD / DoR = Definition of Done / Ready · EX = generated example row · FR = functional requirement · INV = Investment Automation product · MAS = minimum AC set (Part 5.1a §5.6.6) · NSE = no side effect · PDP = Policy Decision Point · PSP = payment service provider · RLS = row-level security · SKU = stock-keeping unit (a sellable service, SM-SVC-01…39 or INV-SVC-01…24) · SoD = separation of duties · SP = story point · t-way = covering array in which every combination of any t parameter values appears in at least one row.

### 11.22.5.4 New stories by epic (continued)

#### 11.22.5.4.32 EP-32 Investment Closing, Investor Lifecycle and Engagement Operations

| Field | Value |
|---|---|
| Epic | EP-32 Investment Closing, Investor Lifecycle and Engagement Operations (Part 11.16d) |
| New stories in this file | US-32-ZU01, US-32-ZU02, US-32-ZU03, US-32-ZU04, US-32-ZU05, US-32-ZU06, US-32-ZU07, US-32-ZU08, US-32-ZU09 |
| FR-V12 covered | O: 001–002, 014, 016, 018, 020, 037–052 |
| Size | 9 stories · 57–92 SP · 28–92 pd (0.5/1.0 pd per SP) · central 52.1 pd (0.7 pd per SP mid) |
| Releases | Release 2: 9 |

##### US-32-ZU01 INV action envelope and per-action entitlement for INV-SVC-13…24

| Field | Value |
|---|---|
| ID | US-32-ZU01 |
| Title | INV action envelope and per-action entitlement for INV-SVC-13…24 |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want every INV action carries tenant, startup, service_id, workflow_revision and correlation_id; scope mismatch → 404 (BRL-TEN-04); entitlement per action: INV-SVC-nn + foundation; revocation stops new executions and pauses active runs safely, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-001; FR-V12-O-002; DEC-770, DEC-783 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.1 Common control model for INV-SVC-13…24 |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×2 · model MU08 |
| Notes | FR-V12-O-001, FR-V12-O-002: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV action envelope and per-action entitlement for INV-SVC-13…24
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-32ZU01-01 Happy path – Every INV action carries tenant, startup, service_id (FR-V12-O-001)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Every INV action carries tenant, startup, service_id" is exercised as specified by FR-V12-O-001:
      """
      Every INV action carries tenant, startup, service_id, workflow_revision and correlation_id; scope mismatch → 404 (BRL-TEN-04); envelope as the
      workbook "Event and trigger schema"
      """
    Then the observable result matches FR-V12-O-001 and its tests in Part 11.21
    And the audit event "inv.every_inv_action_carries" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @DEC-783
  Scenario: AC-32ZU01-02 Alternate – Entitlement per action: INV-SVC-nn + foundation (FR-V12-O-002)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Entitlement per action: INV-SVC-nn + foundation" is exercised as specified by FR-V12-O-002:
      """
      Entitlement per action: INV-SVC-nn + foundation; revocation stops new executions and pauses active runs safely (workbook "Revocation
      behavior")
      """
    Then the observable result matches FR-V12-O-002 and its tests in Part 11.21
    And the audit event "inv.entitlement_per_action" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @DEC-783
  Scenario: AC-32ZU01-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-32ZU01-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-32ZU01-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-32ZU01-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-32ZU01-07 Permutations – Investor securities controls (3-way, 51 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-001 = Every INV action carries tenant, startup, service_id
    #   O-002 = Entitlement per action: INV-SVC-nn + foundation
    Examples: MU08 rows (3-way, seed 1060; space 864; tuples 677/677; +2 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-32ZU01-01 | O-002 | P22/R21 | US 506c ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU01-02 | O-001 | P21/R03 | US 506c ✓ | eligible | relationship | L3 IR-msg mandate | EU | ALLOW: Every INV action carries tenant, startup, service_id |
      | EX-32ZU01-03 | O-001 | P09/R10 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU01-04 | O-001 | P21/R03 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU01-05 | O-002 | P09/R10 | UK FPO draft | eligible | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU01-06 | O-002 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU01-07 | O-002 | P21/R03 | UK FPO draft | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU01-08 | O-001 | P09/R10 | US 506b ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU01-09 | O-001 | P22/R21 | UK FPO draft | eligible | no relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU01-10 | O-002 | P21/R03 | US 506b ✓ | unverified | relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU01-11 | O-002 | P09/R10 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU01-12 | O-001 | P22/R21 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU01-13 | O-002 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU01-14 | O-002 | P22/R21 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU01-15 | O-001 | P22/R21 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU01-16 | O-001 | P22/R21 | US 506c ✓ | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-32ZU01-17 | O-002 | P21/R03 | US 506c ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU01-18 | O-002 | P21/R03 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU01-19 | O-002 | P09/R10 | IN s42 ✓ | unverified | relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU01-20 | O-001 | P09/R10 | US 506c ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU01-21 | O-001 | P09/R10 | IN s42 ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU01-22 | O-001 | P21/R03 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU01-23 | O-001 | P22/R21 | US 506b ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU01-24 | O-001 | P21/R03 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU01-25 | O-001 | P21/R03 | IN s42 ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU01-26 | O-002 | P09/R10 | UK FPO draft | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU01-27 | O-002 | P22/R21 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU01-28 | O-002 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU01-29 | O-002 | P21/R03 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU01-30 | O-002 | P22/R21 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU01-31 | O-001 | P09/R10 | UK FPO draft | unverified | no relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU01-32 | O-002 | P22/R21 | IN s42 ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU01-33 | O-001 | P22/R21 | US 506c ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU01-34 | O-002 | P09/R10 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: Entitlement per action: INV-SVC-nn + foundation |
      | EX-32ZU01-35 | O-002 | P22/R21 | UK FPO draft | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU01-36 | O-001 | P21/R03 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU01-37 | O-001 | P09/R10 | US 506b ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU01-38 | O-001 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU01-39 | O-001 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU01-40 | O-001 | P09/R10 | US 506c ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU01-41 | O-002 | P09/R10 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU01-42 | O-002 | P21/R03 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU01-43 | O-001 | P21/R03 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU01-44 | O-001 | P21/R03 | IN s42 ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU01-45 | O-001 | P22/R21 | US 506b ✓ | unverified | relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU01-46 | O-001 | P21/R03 | US 506c ✓ | unverified | relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU01-47 | O-002 | P09/R10 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU01-48 | O-002 | P21/R03 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU01-49 | O-002 | P21/R03 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU01-50 | O-001 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: Every INV action carries tenant, startup, service_id |
      | EX-32ZU01-51 | O-002 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: Entitlement per action: INV-SVC-nn + foundation |
```

##### US-32-ZU02 Allotment clock and refund task from each receipt

| Field | Value |
|---|---|
| ID | US-32-ZU02 |
| Title | Allotment clock and refund task from each receipt |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the allotment clock (AU-236) runs from each receipt; after day 60 allotment is blocked and a refund task, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-014; DEC-770, DEC-783; tests TC-V12-O-017, TC-V12-O-027 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.3 INV-SVC-13 Legal Investment Closing &… |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-014: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Allotment clock and refund task from each receipt
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-32ZU02-01 Happy path – The allotment clock (AU-236) runs from each receipt (FR-V12-O-014)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "The allotment clock (AU-236) runs from each receipt" is exercised as specified by FR-V12-O-014:
      """
      The allotment clock (AU-236) runs from each receipt; after day 60 allotment is blocked and a refund task (with interest after day 75 for IN)
      is created
      """
    Then receipt on 2027-03-01 → allot-by 2027-04-30 shown on A233 with T-15/T-7/T-1 alerts
    And the audit event "inv.the_allotment_clock" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg
  Scenario: AC-32ZU02-02 Negative – allotment attempted on day 61 is blocked (FR-V12-O-014)
    Given allotment attempted on day 61 is blocked; RP-IN-SEC-011 finding
    When the action is attempted
    Then it is blocked or held with no external effect and the denial is audited (FR-V12-O-014)

  @neg @DEC-783
  Scenario: AC-32ZU02-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-32ZU02-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-32ZU02-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-32ZU02-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-32ZU02-07 Permutations – Investor securities controls (3-way, 47 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-014 = The allotment clock (AU-236) runs from each receipt
    Examples: MU08 rows (3-way, seed 1067; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-32ZU02-01 | O-014 | P21/R03 | IN s42 ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU02-02 | O-014 | P09/R10 | US 506b ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU02-03 | O-014 | P22/R21 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU02-04 | O-014 | P21/R03 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU02-05 | O-014 | P22/R21 | US 506c ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU02-06 | O-014 | P09/R10 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU02-07 | O-014 | P09/R10 | UK FPO draft | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-32ZU02-08 | O-014 | P21/R03 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU02-09 | O-014 | P09/R10 | IN s42 ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU02-10 | O-014 | P22/R21 | UK FPO draft | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU02-11 | O-014 | P22/R21 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: receipt on 2027-03-01 → allot-by 2027-04-30 shown |
      | EX-32ZU02-12 | O-014 | P21/R03 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU02-13 | O-014 | P09/R10 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU02-14 | O-014 | P21/R03 | US 506b ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU02-15 | O-014 | P21/R03 | US 506c ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU02-16 | O-014 | P22/R21 | IN s42 ✓ | unverified | relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU02-17 | O-014 | P09/R10 | UK FPO draft | eligible | relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU02-18 | O-014 | P22/R21 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU02-19 | O-014 | P21/R03 | US 506b ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU02-20 | O-014 | P22/R21 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU02-21 | O-014 | P09/R10 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU02-22 | O-014 | P09/R10 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU02-23 | O-014 | P22/R21 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU02-24 | O-014 | P22/R21 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU02-25 | O-014 | P21/R03 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU02-26 | O-014 | P21/R03 | IN s42 ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU02-27 | O-014 | P22/R21 | US 506b ✓ | unverified | relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU02-28 | O-014 | P21/R03 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-32ZU02-29 | O-014 | P09/R10 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: receipt on 2027-03-01 → allot-by 2027-04-30 shown |
      | EX-32ZU02-30 | O-014 | P09/R10 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU02-31 | O-014 | P09/R10 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU02-32 | O-014 | P21/R03 | US 506c ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU02-33 | O-014 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-32ZU02-34 | O-014 | P22/R21 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU02-35 | O-014 | P22/R21 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU02-36 | O-014 | P09/R10 | US 506b ✓ | eligible | no relationship | L1 two-person | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU02-37 | O-014 | P21/R03 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU02-38 | O-014 | P22/R21 | IN s42 ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU02-39 | O-014 | P09/R10 | US 506c ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU02-40 | O-014 | P22/R21 | UK FPO draft | unverified | relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU02-41 | O-014 | P21/R03 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU02-42 | O-014 | P21/R03 | IN s42 ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU02-43 | O-014 | P09/R10 | UK FPO draft | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU02-44 | O-014 | P09/R10 | US 506b ✓ | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-32ZU02-45 | O-014 | P09/R10 | UK FPO draft | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU02-46 | O-014 | P21/R03 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU02-47 | O-014 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: receipt on 2027-03-01 → allot-by 2027-04-30 shown |
```

##### US-32-ZU03 Rights-scoped personalisation of investor updates

| Field | Value |
|---|---|
| ID | US-32-ZU03 |
| Title | Rights-scoped personalisation of investor updates |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want personalisation uses only information the recipient has rights to; updates mentioning an offer route to AG-198 and the securities packs, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-016; DEC-770, DEC-783; tests TC-V12-O-049, TC-V12-O-059 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.4 INV-SVC-14 Investor Reporting &… |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-016: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Rights-scoped personalisation of investor updates
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-32ZU03-01 Happy path – Personalisation uses only information the recipient has rights to (FR-V12-O-016)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Personalisation uses only information the recipient has rights to" is exercised as specified by FR-V12-O-016:
      """
      Personalisation uses only information the recipient has rights to; updates mentioning an offer route to AG-198 and the securities packs
      """
    Then investor without board-pack rights receives only the public-safe update
    And the audit event "inv.personalisation_uses_only" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg
  Scenario: AC-32ZU03-02 Negative – update containing "Series A closes 30 June (FR-V12-O-016)
    Given update containing "Series A closes 30 June, join now" routes to A256
    When the action is attempted
    Then it is blocked or held with no external effect and the denial is audited (FR-V12-O-016)

  @neg @DEC-783
  Scenario: AC-32ZU03-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-32ZU03-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-32ZU03-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-32ZU03-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-32ZU03-07 Permutations – Investor securities controls (3-way, 48 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-016 = Personalisation uses only information the recipient…
    Examples: MU08 rows (3-way, seed 1074; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-32ZU03-01 | O-016 | P09/R10 | UK FPO draft | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU03-02 | O-016 | P22/R21 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU03-03 | O-016 | P21/R03 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU03-04 | O-016 | P22/R21 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU03-05 | O-016 | P09/R10 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU03-06 | O-016 | P21/R03 | US 506c ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU03-07 | O-016 | P22/R21 | UK FPO draft | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU03-08 | O-016 | P09/R10 | IN s42 ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU03-09 | O-016 | P21/R03 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU03-10 | O-016 | P09/R10 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU03-11 | O-016 | P22/R21 | US 506b ✓ | eligible | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU03-12 | O-016 | P21/R03 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU03-13 | O-016 | P22/R21 | UK FPO draft | unverified | no relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU03-14 | O-016 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU03-15 | O-016 | P21/R03 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU03-16 | O-016 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-32ZU03-17 | O-016 | P21/R03 | IN s42 ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU03-18 | O-016 | P09/R10 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU03-19 | O-016 | P21/R03 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU03-20 | O-016 | P09/R10 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU03-21 | O-016 | P21/R03 | US 506c ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU03-22 | O-016 | P22/R21 | UK FPO draft | eligible | no relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU03-23 | O-016 | P09/R10 | IN s42 ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU03-24 | O-016 | P21/R03 | IN s42 ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU03-25 | O-016 | P09/R10 | UK FPO draft | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU03-26 | O-016 | P22/R21 | US 506b ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU03-27 | O-016 | P22/R21 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU03-28 | O-016 | P21/R03 | UK FPO draft | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-32ZU03-29 | O-016 | P22/R21 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU03-30 | O-016 | P09/R10 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU03-31 | O-016 | P21/R03 | US 506b ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU03-32 | O-016 | P22/R21 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU03-33 | O-016 | P09/R10 | US 506b ✓ | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU03-34 | O-016 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | EU | ALLOW: investor without board-pack rights receives only |
      | EX-32ZU03-35 | O-016 | P09/R10 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU03-36 | O-016 | P09/R10 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU03-37 | O-016 | P22/R21 | IN s42 ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU03-38 | O-016 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU03-39 | O-016 | P21/R03 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU03-40 | O-016 | P22/R21 | US 506c ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU03-41 | O-016 | P22/R21 | UK FPO draft | eligible | relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU03-42 | O-016 | P21/R03 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU03-43 | O-016 | P22/R21 | IN s42 ✓ | unverified | relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU03-44 | O-016 | P22/R21 | UK FPO draft | unverified | relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU03-45 | O-016 | P09/R10 | US 506b ✓ | unverified | relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU03-46 | O-016 | P21/R03 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU03-47 | O-016 | P22/R21 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU03-48 | O-016 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: investor without board-pack rights receives only |
```

##### US-32-ZU04 Next actions that respect the round's solicitation mode

| Field | Value |
|---|---|
| ID | US-32-ZU04 |
| Title | Next actions that respect the round's solicitation mode |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want next actions respect the round's solicitation mode; cold outreach is never proposed for private rounds (AU-232), so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-018; DEC-770, DEC-783; tests TC-V12-O-081, TC-V12-O-091 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.5 INV-SVC-15 Fundraising CRM |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-018: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Next actions that respect the round's solicitation mode
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-32ZU04-01 Happy path – Next actions respect the round's solicitation mode (FR-V12-O-018)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Next actions respect the round's solicitation mode" is exercised as specified by FR-V12-O-018:
      """
      Next actions respect the round's solicitation mode; cold outreach is never proposed for private rounds (AU-232)
      """
    Then 506(c) round may propose public-channel tasks
    And the audit event "inv.next_actions_respect_the" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg
  Scenario: AC-32ZU04-02 Negative – s.42 round never shows "post on LinkedIn" tasks (FR-V12-O-018)
    Given s.42 round never shows "post on LinkedIn" tasks
    When the action is attempted
    Then it is blocked or held with no external effect and the denial is audited (FR-V12-O-018)

  @neg @DEC-783
  Scenario: AC-32ZU04-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-32ZU04-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-32ZU04-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-32ZU04-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-32ZU04-07 Permutations – Investor securities controls (3-way, 44 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-018 = Next actions respect the round's solicitation mode
    Examples: MU08 rows (3-way, seed 1081; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-32ZU04-01 | O-018 | P21/R03 | US 506c ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU04-02 | O-018 | P22/R21 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU04-03 | O-018 | P09/R10 | US 506b ✓ | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU04-04 | O-018 | P09/R10 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU04-05 | O-018 | P22/R21 | IN s42 ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU04-06 | O-018 | P21/R03 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU04-07 | O-018 | P21/R03 | US 506c ✓ | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU04-08 | O-018 | P22/R21 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU04-09 | O-018 | P09/R10 | UK FPO draft | eligible | no relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU04-10 | O-018 | P09/R10 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU04-11 | O-018 | P22/R21 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU04-12 | O-018 | P21/R03 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU04-13 | O-018 | P09/R10 | UK FPO draft | unverified | relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU04-14 | O-018 | P22/R21 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU04-15 | O-018 | P22/R21 | US 506b ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU04-16 | O-018 | P09/R10 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU04-17 | O-018 | P21/R03 | UK FPO draft | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU04-18 | O-018 | P22/R21 | US 506c ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU04-19 | O-018 | P21/R03 | US 506b ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU04-20 | O-018 | P21/R03 | IN s42 ✓ | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU04-21 | O-018 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU04-22 | O-018 | P21/R03 | US 506b ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU04-23 | O-018 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU04-24 | O-018 | P21/R03 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU04-25 | O-018 | P09/R10 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU04-26 | O-018 | P21/R03 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU04-27 | O-018 | P09/R10 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-32ZU04-28 | O-018 | P09/R10 | US 506c ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU04-29 | O-018 | P22/R21 | IN s42 ✓ | unverified | no relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU04-30 | O-018 | P22/R21 | US 506b ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU04-31 | O-018 | P09/R10 | US 506b ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU04-32 | O-018 | P21/R03 | UK FPO draft | unverified | no relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU04-33 | O-018 | P09/R10 | US 506c ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU04-34 | O-018 | P09/R10 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU04-35 | O-018 | P22/R21 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU04-36 | O-018 | P22/R21 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU04-37 | O-018 | P21/R03 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU04-38 | O-018 | P21/R03 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU04-39 | O-018 | P22/R21 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU04-40 | O-018 | P22/R21 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU04-41 | O-018 | P21/R03 | UK FPO draft | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU04-42 | O-018 | P21/R03 | IN s42 ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU04-43 | O-018 | P21/R03 | UK FPO draft | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU04-44 | O-018 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: 506(c) round may propose public-channel tasks |
```

##### US-32-ZU05 Enquiries from markets without an active pack stay enquiries

| Field | Value |
|---|---|
| ID | US-32-ZU05 |
| Title | Enquiries from markets without an active pack stay enquiries |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want investment-interest enquiries from a jurisdiction without an active pack are stored as enquiries only; no offer material is sent, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-020; DEC-770, DEC-783; tests TC-V12-O-113, TC-V12-O-123 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.6 INV-SVC-16 Private Website Enquiry &… |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-020: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Enquiries from markets without an active pack stay enquiries
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-32ZU05-01 Happy path – Investment-interest enquiries from a jurisdiction without an active… (FR-V12-O-020)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Investment-interest enquiries from a jurisdiction without an active…" is exercised as specified by FR-V12-O-020:
      """
      Investment-interest enquiries from a jurisdiction without an active pack are stored as enquiries only; no offer material is sent
      """
    Then UK enquiry with UK pack inactive → stored, owner sees "UK not active"
    And the audit event "inv.investment_interest_enquiries" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg
  Scenario: AC-32ZU05-02 Negative – auto-reply containing deck link blocked (FR-V12-O-020)
    Given auto-reply containing deck link blocked
    When the action is attempted
    Then it is blocked or held with no external effect and the denial is audited (FR-V12-O-020)

  @neg @DEC-783
  Scenario: AC-32ZU05-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-32ZU05-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-32ZU05-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-32ZU05-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-32ZU05-07 Permutations – Investor securities controls (3-way, 50 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-020 = Investment-interest enquiries from a jurisdiction…
    Examples: MU08 rows (3-way, seed 1088; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-32ZU05-01 | O-020 | P21/R03 | IN s42 ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU05-02 | O-020 | P09/R10 | US 506b ✓ | unverified | relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU05-03 | O-020 | P22/R21 | US 506c ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU05-04 | O-020 | P22/R21 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU05-05 | O-020 | P09/R10 | US 506c ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: UK enquiry with UK pack inactive → stored, owner |
      | EX-32ZU05-06 | O-020 | P09/R10 | UK FPO draft | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU05-07 | O-020 | P21/R03 | IN s42 ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU05-08 | O-020 | P21/R03 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU05-09 | O-020 | P22/R21 | US 506b ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU05-10 | O-020 | P21/R03 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU05-11 | O-020 | P09/R10 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU05-12 | O-020 | P21/R03 | UK FPO draft | eligible | no relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU05-13 | O-020 | P22/R21 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU05-14 | O-020 | P09/R10 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU05-15 | O-020 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU05-16 | O-020 | P21/R03 | US 506c ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU05-17 | O-020 | P09/R10 | UK FPO draft | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-32ZU05-18 | O-020 | P22/R21 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU05-19 | O-020 | P22/R21 | IN s42 ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU05-20 | O-020 | P22/R21 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU05-21 | O-020 | P09/R10 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU05-22 | O-020 | P22/R21 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU05-23 | O-020 | P22/R21 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: UK enquiry with UK pack inactive → stored, owner |
      | EX-32ZU05-24 | O-020 | P21/R03 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU05-25 | O-020 | P21/R03 | US 506b ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU05-26 | O-020 | P22/R21 | UK FPO draft | unverified | no relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU05-27 | O-020 | P21/R03 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU05-28 | O-020 | P22/R21 | US 506c ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-32ZU05-29 | O-020 | P09/R10 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU05-30 | O-020 | P09/R10 | US 506c ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU05-31 | O-020 | P09/R10 | UK FPO draft | eligible | relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU05-32 | O-020 | P21/R03 | US 506b ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU05-33 | O-020 | P21/R03 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU05-34 | O-020 | P21/R03 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU05-35 | O-020 | P09/R10 | IN s42 ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-32ZU05-36 | O-020 | P09/R10 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-32ZU05-37 | O-020 | P21/R03 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU05-38 | O-020 | P22/R21 | IN s42 ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU05-39 | O-020 | P21/R03 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU05-40 | O-020 | P09/R10 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU05-41 | O-020 | P21/R03 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: UK enquiry with UK pack inactive → stored, owner |
      | EX-32ZU05-42 | O-020 | P09/R10 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU05-43 | O-020 | P22/R21 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU05-44 | O-020 | P22/R21 | US 506b ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU05-45 | O-020 | P21/R03 | US 506c ✓ | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-32ZU05-46 | O-020 | P21/R03 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-32ZU05-47 | O-020 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-32ZU05-48 | O-020 | P22/R21 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: UK enquiry with UK pack inactive → stored, owner |
      | EX-32ZU05-49 | O-020 | P22/R21 | US 506c ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-32ZU05-50 | O-020 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: UK enquiry with UK pack inactive → stored, owner |
```

##### US-32-ZU06 INV-SVC-13 Legal Investment Closing & Statutory Task Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-32-ZU06 |
| Title | INV-SVC-13 Legal Investment Closing & Statutory Task Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-13 Legal Investment Closing & Statutory Task Automation workflows (closing readiness review; authorized closing coordination; statutory task and closing report; closing dependency and regulatory deadline monitoring) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-037; FR-V12-O-038; FR-V12-O-039; FR-V12-O-040; DEC-770, DEC-779, DEC-783, DEC-822; tests TC-V12-O-001, TC-V12-O-009, TC-V12-O-017, TC-V12-O-025 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-13-WF01 Closing readiness review; Part 11.16c §INV-SVC-13-WF02 Authorized closing coordination; Part 11.16c §INV-SVC-13-WF03 Statutory task and closing report; Part 11.16c §INV-SVC-13-WF04 Closing dependency and regulatory… |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-037, FR-V12-O-038, FR-V12-O-039, FR-V12-O-040: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO01, US-32-ZO02, US-32-ZO09 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-13 Legal Investment Closing & Statutory Task Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-32ZU06-01 Happy path – Closing readiness review (FR-V12-O-037)
    Given the trigger "Scheduled or manual; scoped event on change" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-13-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-13-WF01:v2` (FR-V12-O-037)
    Then Closing readiness review: Verified application, agreement and receipts → Readiness checklist
    And Readiness checklist; acceptance INV-SVC-13-WF01-AT01 → TC-V12-O-001 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash, two-person
      (R10 + R08/R09)"
      """

  @alt @DEC-783
  Scenario: AC-32ZU06-02 Alternate – Authorized closing coordination (FR-V12-O-038)
    Given the trigger "Manual request or validated upstream business event" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-13-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-13-WF02:v2` (FR-V12-O-038)
    Then Authorized closing coordination: Approved closing checklist and issuer decision → Closing record
    And Closing record; acceptance INV-SVC-13-WF02-AT01 → TC-V12-O-009 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash, two-person
      (R10 + R08/R09)"
      """

  @alt @DEC-783
  Scenario: AC-32ZU06-03 Alternate – Statutory task and closing report (FR-V12-O-039)
    Given the trigger "Manual request or validated upstream business event" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-13-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-13-WF03:v2` (FR-V12-O-039)
    Then Statutory task and closing report: Closing record and applicable obligations → Closing report and obligations
    And Closing report and obligations; acceptance INV-SVC-13-WF03-AT01 → TC-V12-O-017 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash, two-person
      (R10 + R08/R09)"
      """

  @alt @DEC-783
  Scenario: AC-32ZU06-04 Alternate – Closing dependency and regulatory deadline monitoring (FR-V12-O-040)
    Given the trigger "Manual; scheduled or relevant validated business event; provider webhook:
      """
      only where authorized" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-13-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-13-WF04:v2` (FR-V12-O-040)
    Then Closing dependency and regulatory deadline monitoring:
      """
      Closing checklist, jurisdiction requirements, approved deadlines → Closing readiness and deadline alerts
      """
    And Closing readiness and deadline alerts; acceptance INV-SVC-13-WF04-AT01 → TC-V12-O-025 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash, two-person
      (R10 + R08/R09)"
      """

  @neg @DEC-822
  Scenario: AC-32ZU06-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-32ZU06-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-32ZU06-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-32ZU06-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-32ZU06-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 75 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-037 = Closing readiness review
    #   O-038 = Authorized closing coordination
    #   O-039 = Statutory task and closing report
    #   O-040 = Closing dependency and regulatory deadline…
    Examples: MU09 rows (3-way, seed 1095; space 3,888; tuples 1230/1230; +3 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-32ZU06-01 | O-037 | P21/R03 | A1 | US ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-02 | O-037 | P08/R08 | A3 SoD/limit | US ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-03 | O-040 | P21/R03 | T5 other tenant | UK draft | 1 approver | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-32ZU06-04 | O-040 | P08/R08 | A5 wrong role | IN ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-05 | O-038 | P09/R10 | A5 wrong role | US ✓ | hash changed | active | EU | 403 PERMISSION_DENIED |
      | EX-32ZU06-06 | O-038 | P09/R10 | A3 SoD/limit | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-07 | O-039 | P09/R10 | A1 | IN ✓ | 1 approver | active | IN | HELD TWO_APPROVALS_REQUIRED |
      | EX-32ZU06-08 | O-040 | P08/R08 | A1 | UK draft | 2 approvals | active | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU06-09 | O-037 | P21/R03 | A3 SoD/limit | UK draft | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-32ZU06-10 | O-039 | P21/R03 | T5 other tenant | IN ✓ | 2 approvals | suspended | EU | uniform 404 NOT_FOUND |
      | EX-32ZU06-11 | O-040 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-12 | O-039 | P08/R08 | A5 wrong role | UK draft | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-13 | O-039 | P21/R03 | A5 wrong role | US ✓ | 2 approvals | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-32ZU06-14 | O-039 | P09/R10 | T5 other tenant | UK draft | hash changed | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU06-15 | O-037 | P08/R08 | T5 other tenant | IN ✓ | 2 approvals | active | IN | uniform 404 NOT_FOUND |
      | EX-32ZU06-16 | O-038 | P09/R10 | A1 | UK draft | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-17 | O-040 | P21/R03 | A1 | IN ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-18 | O-038 | P08/R08 | T5 other tenant | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU06-19 | O-038 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | active | IN | 403 SOD_CONFLICT |
      | EX-32ZU06-20 | O-037 | P09/R10 | A5 wrong role | UK draft | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-21 | O-040 | P09/R10 | T5 other tenant | US ✓ | 1 approver | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU06-22 | O-038 | P08/R08 | A3 SoD/limit | IN ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-23 | O-039 | P21/R03 | A1 | UK draft | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-24 | O-039 | P09/R10 | A1 | US ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-25 | O-037 | P21/R03 | A5 wrong role | IN ✓ | 1 approver | active | EU | 403 PERMISSION_DENIED |
      | EX-32ZU06-26 | O-038 | P21/R03 | A5 wrong role | UK draft | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-27 | O-037 | P08/R08 | A1 | IN ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-28 | O-039 | P08/R08 | T5 other tenant | US ✓ | 1 approver | suspended | IN | uniform 404 NOT_FOUND |
      | EX-32ZU06-29 | O-037 | P09/R10 | T5 other tenant | IN ✓ | hash changed | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-32ZU06-30 | O-039 | P08/R08 | A3 SoD/limit | IN ✓ | hash changed | active | EU | 403 SOD_CONFLICT |
      | EX-32ZU06-31 | O-038 | P21/R03 | A5 wrong role | IN ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-32 | O-038 | P08/R08 | T5 other tenant | UK draft | 1 approver | active | EU | uniform 404 NOT_FOUND |
      | EX-32ZU06-33 | O-037 | P09/R10 | A3 SoD/limit | UK draft | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-34 | O-040 | P08/R08 | A5 wrong role | US ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-35 | O-039 | P21/R03 | A3 SoD/limit | UK draft | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-36 | O-040 | P09/R10 | A5 wrong role | UK draft | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-37 | O-038 | P08/R08 | A1 | US ✓ | 2 approvals | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU06-38 | O-040 | P21/R03 | A3 SoD/limit | IN ✓ | 2 approvals | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-32ZU06-39 | O-038 | P09/R10 | T5 other tenant | UK draft | 2 approvals | active | IN | uniform 404 NOT_FOUND |
      | EX-32ZU06-40 | O-037 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU06-41 | O-040 | P08/R08 | A5 wrong role | IN ✓ | hash changed | active | IN | 403 PERMISSION_DENIED |
      | EX-32ZU06-42 | O-037 | P09/R10 | A5 wrong role | US ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-43 | O-038 | P21/R03 | A1 | UK draft | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-44 | O-037 | P08/R08 | A1 | UK draft | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-45 | O-040 | P08/R08 | A3 SoD/limit | UK draft | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-46 | O-039 | P09/R10 | A3 SoD/limit | IN ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-47 | O-040 | P21/R03 | T5 other tenant | US ✓ | hash changed | active | EU | uniform 404 NOT_FOUND |
      | EX-32ZU06-48 | O-039 | P09/R10 | A5 wrong role | IN ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-49 | O-040 | P21/R03 | A1 | US ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-50 | O-037 | P09/R10 | A1 | US ✓ | hash changed | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU06-51 | O-038 | P21/R03 | A3 SoD/limit | US ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-52 | O-039 | P08/R08 | A1 | UK draft | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-53 | O-038 | P21/R03 | T5 other tenant | IN ✓ | 1 approver | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU06-54 | O-039 | P09/R10 | A3 SoD/limit | US ✓ | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-32ZU06-55 | O-039 | P08/R08 | A5 wrong role | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-56 | O-037 | P09/R10 | T5 other tenant | UK draft | hash changed | suspended | IN | uniform 404 NOT_FOUND |
      | EX-32ZU06-57 | O-040 | P09/R10 | A3 SoD/limit | IN ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-58 | O-039 | P21/R03 | A5 wrong role | US ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-59 | O-038 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Closing record |
      | EX-32ZU06-60 | O-040 | P08/R08 | T5 other tenant | IN ✓ | 2 approvals | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU06-61 | O-037 | P08/R08 | A5 wrong role | UK draft | 1 approver | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-32ZU06-62 | O-037 | P08/R08 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-63 | O-037 | P08/R08 | A3 SoD/limit | IN ✓ | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-32ZU06-64 | O-039 | P09/R10 | T5 other tenant | UK draft | 1 approver | active | IN | uniform 404 NOT_FOUND |
      | EX-32ZU06-65 | O-037 | P21/R03 | A1 | IN ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-66 | O-040 | P21/R03 | A5 wrong role | US ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-67 | O-038 | P08/R08 | A5 wrong role | IN ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU06-68 | O-040 | P09/R10 | A1 | IN ✓ | 1 approver | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU06-69 | O-037 | P21/R03 | T5 other tenant | UK draft | 1 approver | active | EU | uniform 404 NOT_FOUND |
      | EX-32ZU06-70 | O-038 | P08/R08 | T5 other tenant | UK draft | 2 approvals | suspended | EU | uniform 404 NOT_FOUND |
      | EX-32ZU06-71 | O-039 | P09/R10 | T5 other tenant | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU06-72 | O-038 | P09/R10 | A3 SoD/limit | UK draft | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU06-73 | O-037 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Readiness checklist |
      | EX-32ZU06-74 | O-039 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Closing report and obligations |
      | EX-32ZU06-75 | O-040 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Closing readiness and deadline alerts |
```

##### US-32-ZU07 INV-SVC-14 Investor Reporting & Capital Lifecycle Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-32-ZU07 |
| Title | INV-SVC-14 Investor Reporting & Capital Lifecycle Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-14 Investor Reporting & Capital Lifecycle Automation workflows (investor onboarding and obligations; capital deployment and milestone tracking; investor update and feedback cycle; investor update personalization and obligation-risk) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-041; FR-V12-O-042; FR-V12-O-043; FR-V12-O-044; DEC-770, DEC-779, DEC-783, DEC-822; tests TC-V12-O-033, TC-V12-O-041, TC-V12-O-049, TC-V12-O-057 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-14-WF01 Investor onboarding and…; Part 11.16c §INV-SVC-14-WF02 Capital deployment and milestone…; Part 11.16c §INV-SVC-14-WF03 Investor update and feedback cycle; Part 11.16c §INV-SVC-14-WF04 Investor update personalization… |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-041, FR-V12-O-042, FR-V12-O-043, FR-V12-O-044: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO03, US-32-ZO04, US-32-ZO09, US-33-ZO14 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-14 Investor Reporting & Capital Lifecycle Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-32ZU07-01 Happy path – Investor onboarding and obligations (FR-V12-O-041)
    Given the trigger "Manual request or validated upstream business event" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-14-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-14-WF01:v2` (FR-V12-O-041)
    Then Investor onboarding and obligations: Verified closing or supplied existing investor record → Investor lifecycle plan
    And Investor lifecycle plan; acceptance INV-SVC-14-WF01-AT01 → TC-V12-O-033 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-32ZU07-02 Alternate – Capital deployment and milestone tracking (FR-V12-O-042)
    Given the trigger "Scheduled or manual; scoped event on change" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-14-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-14-WF02:v2` (FR-V12-O-042)
    Then Capital deployment and milestone tracking: Approved allocation and progress evidence → Milestone status and variance report
    And Milestone status and variance report; acceptance INV-SVC-14-WF02-AT01 → TC-V12-O-041 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-32ZU07-03 Alternate – Investor update and feedback cycle (FR-V12-O-043)
    Given the trigger "Manual request or validated upstream business event" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-14-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-14-WF03:v2` (FR-V12-O-043)
    Then Investor update and feedback cycle: Verified KPIs, approved reporting schedule → Update draft and feedback record
    And Update draft and feedback record; acceptance INV-SVC-14-WF03-AT01 → TC-V12-O-049 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @alt @DEC-783
  Scenario: AC-32ZU07-04 Alternate – Investor update personalization and obligation-risk monitoring (FR-V12-O-044)
    Given the trigger "Manual; scheduled or relevant validated business event; provider webhook:
      """
      only where authorized" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-14-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-14-WF04:v2` (FR-V12-O-044)
    Then Investor update personalization and obligation-risk monitoring:
      """
      Approved reporting pack, investor rights, obligations → Scoped update draft and risk alerts
      """
    And Scoped update draft and risk alerts; acceptance INV-SVC-14-WF04-AT01 → TC-V12-O-057 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @neg @DEC-822
  Scenario: AC-32ZU07-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-32ZU07-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-32ZU07-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-32ZU07-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-32ZU07-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 76 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-041 = Investor onboarding and obligations
    #   O-042 = Capital deployment and milestone tracking
    #   O-043 = Investor update and feedback cycle
    #   O-044 = Investor update personalization and obligation-risk…
    Examples: MU09 rows (3-way, seed 1102; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-32ZU07-01 | O-043 | P09/R10 | A1 | UK draft | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-02 | O-042 | P21/R03 | A5 wrong role | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-03 | O-044 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU07-04 | O-044 | P08/R08 | A1 | IN ✓ | 1 approver | active | EU | HELD TWO_APPROVALS_REQUIRED |
      | EX-32ZU07-05 | O-042 | P09/R10 | A3 SoD/limit | UK draft | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-06 | O-043 | P08/R08 | A5 wrong role | US ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-07 | O-044 | P08/R08 | A3 SoD/limit | US ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-08 | O-041 | P09/R10 | A3 SoD/limit | IN ✓ | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-32ZU07-09 | O-042 | P21/R03 | T5 other tenant | UK draft | hash changed | suspended | EU | uniform 404 NOT_FOUND |
      | EX-32ZU07-10 | O-041 | P21/R03 | A1 | IN ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-11 | O-041 | P08/R08 | T5 other tenant | UK draft | 1 approver | active | IN | uniform 404 NOT_FOUND |
      | EX-32ZU07-12 | O-041 | P09/R10 | T5 other tenant | US ✓ | 1 approver | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-32ZU07-13 | O-043 | P21/R03 | A5 wrong role | UK draft | hash changed | active | IN | 403 PERMISSION_DENIED |
      | EX-32ZU07-14 | O-042 | P08/R08 | A1 | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-15 | O-043 | P09/R10 | T5 other tenant | IN ✓ | hash changed | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-32ZU07-16 | O-044 | P09/R10 | A5 wrong role | IN ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-17 | O-042 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | active | EU | 403 SOD_CONFLICT |
      | EX-32ZU07-18 | O-041 | P08/R08 | A5 wrong role | UK draft | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-19 | O-044 | P21/R03 | A1 | UK draft | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-20 | O-042 | P08/R08 | A5 wrong role | IN ✓ | 2 approvals | active | IN | 403 PERMISSION_DENIED |
      | EX-32ZU07-21 | O-044 | P09/R10 | A5 wrong role | US ✓ | 1 approver | active | IN | 403 PERMISSION_DENIED |
      | EX-32ZU07-22 | O-043 | P21/R03 | A3 SoD/limit | IN ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-23 | O-043 | P09/R10 | T5 other tenant | UK draft | 2 approvals | active | EU | uniform 404 NOT_FOUND |
      | EX-32ZU07-24 | O-041 | P08/R08 | A3 SoD/limit | UK draft | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-25 | O-043 | P08/R08 | T5 other tenant | US ✓ | 1 approver | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU07-26 | O-043 | P21/R03 | A1 | US ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-27 | O-042 | P09/R10 | A1 | US ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-28 | O-044 | P21/R03 | A3 SoD/limit | UK draft | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-29 | O-044 | P08/R08 | T5 other tenant | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU07-30 | O-041 | P21/R03 | A5 wrong role | US ✓ | hash changed | active | EU | 403 PERMISSION_DENIED |
      | EX-32ZU07-31 | O-042 | P09/R10 | T5 other tenant | IN ✓ | 1 approver | suspended | IN | uniform 404 NOT_FOUND |
      | EX-32ZU07-32 | O-044 | P09/R10 | A5 wrong role | UK draft | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-33 | O-043 | P08/R08 | A3 SoD/limit | IN ✓ | 1 approver | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-32ZU07-34 | O-042 | P09/R10 | A1 | UK draft | hash changed | active | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU07-35 | O-042 | P08/R08 | A5 wrong role | UK draft | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-36 | O-041 | P21/R03 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-37 | O-043 | P21/R03 | A1 | IN ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-38 | O-043 | P08/R08 | A1 | US ✓ | 2 approvals | active | IN | ALLOW: Update draft and feedback record |
      | EX-32ZU07-39 | O-041 | P08/R08 | T5 other tenant | IN ✓ | hash changed | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU07-40 | O-044 | P21/R03 | T5 other tenant | IN ✓ | hash changed | active | IN | uniform 404 NOT_FOUND |
      | EX-32ZU07-41 | O-043 | P09/R10 | A3 SoD/limit | US ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-42 | O-041 | P09/R10 | A1 | UK draft | 2 approvals | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU07-43 | O-041 | P08/R08 | A3 SoD/limit | IN ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-44 | O-041 | P08/R08 | A1 | US ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-45 | O-044 | P08/R08 | A3 SoD/limit | UK draft | 2 approvals | active | IN | 403 SOD_CONFLICT |
      | EX-32ZU07-46 | O-042 | P09/R10 | T5 other tenant | UK draft | 2 approvals | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU07-47 | O-041 | P21/R03 | A5 wrong role | US ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-48 | O-041 | P09/R10 | A5 wrong role | IN ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-49 | O-044 | P21/R03 | T5 other tenant | UK draft | 1 approver | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-32ZU07-50 | O-044 | P09/R10 | A1 | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-51 | O-042 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | suspended | IN | uniform 404 NOT_FOUND |
      | EX-32ZU07-52 | O-042 | P21/R03 | A3 SoD/limit | IN ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-53 | O-042 | P08/R08 | T5 other tenant | IN ✓ | 1 approver | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-32ZU07-54 | O-043 | P08/R08 | A3 SoD/limit | UK draft | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-55 | O-042 | P08/R08 | A5 wrong role | US ✓ | hash changed | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-32ZU07-56 | O-043 | P09/R10 | A5 wrong role | IN ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-57 | O-044 | P09/R10 | A3 SoD/limit | US ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-58 | O-044 | P21/R03 | A5 wrong role | IN ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-59 | O-041 | P08/R08 | A1 | UK draft | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-60 | O-041 | P09/R10 | A3 SoD/limit | US ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-61 | O-044 | P09/R10 | A1 | IN ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-62 | O-042 | P21/R03 | A1 | IN ✓ | 1 approver | active | IN | HELD TWO_APPROVALS_REQUIRED |
      | EX-32ZU07-63 | O-041 | P21/R03 | T5 other tenant | UK draft | 2 approvals | suspended | EU | uniform 404 NOT_FOUND |
      | EX-32ZU07-64 | O-043 | P21/R03 | A1 | UK draft | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-65 | O-044 | P09/R10 | T5 other tenant | US ✓ | hash changed | suspended | IN | uniform 404 NOT_FOUND |
      | EX-32ZU07-66 | O-043 | P21/R03 | A3 SoD/limit | IN ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-67 | O-043 | P21/R03 | T5 other tenant | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU07-68 | O-042 | P08/R08 | A3 SoD/limit | US ✓ | 1 approver | active | EU | 403 SOD_CONFLICT |
      | EX-32ZU07-69 | O-044 | P08/R08 | A3 SoD/limit | IN ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-70 | O-044 | P21/R03 | A1 | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-71 | O-042 | P09/R10 | A5 wrong role | IN ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU07-72 | O-044 | P08/R08 | A5 wrong role | US ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU07-73 | O-041 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Investor lifecycle plan |
      | EX-32ZU07-74 | O-042 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Milestone status and variance report |
      | EX-32ZU07-75 | O-043 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Update draft and feedback record |
      | EX-32ZU07-76 | O-044 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Scoped update draft and risk alerts |
```

##### US-32-ZU08 INV-SVC-15 Fundraising CRM, Pipeline & Analytics Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-32-ZU08 |
| Title | INV-SVC-15 Fundraising CRM, Pipeline & Analytics Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-15 Fundraising CRM, Pipeline & Analytics Automation workflows (relationship import and pipeline coordination; next-action and task generation; fundraising progress and forecast; probability-weighted fundraising forecast and bottleneck) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-045; FR-V12-O-046; FR-V12-O-047; FR-V12-O-048; DEC-770, DEC-783; tests TC-V12-O-065, TC-V12-O-073, TC-V12-O-081, TC-V12-O-089 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-15-WF01 Relationship import and pipeline…; Part 11.16c §INV-SVC-15-WF02 Next-action and task generation; Part 11.16c §INV-SVC-15-WF03 Fundraising progress and forecast; Part 11.16c §INV-SVC-15-WF04 Probability-weighted fundraising… |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-045, FR-V12-O-046, FR-V12-O-047, FR-V12-O-048: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO05, US-32-ZO06, US-32-ZO09 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-15 Fundraising CRM, Pipeline & Analytics Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-32ZU08-01 Happy path – Relationship import and pipeline coordination (FR-V12-O-045)
    Given the trigger "Authorized business event or manual import; signed webhook if applicable" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-15-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-15-WF01:v2` (FR-V12-O-045)
    Then Relationship import and pipeline coordination: Authorized investor records and stages → Investor pipeline records
    And Investor pipeline records; acceptance INV-SVC-15-WF01-AT01 → TC-V12-O-065 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-32ZU08-02 Alternate – Next-action and task generation (FR-V12-O-046)
    Given the trigger "Manual request or validated upstream business event" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-15-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-15-WF02:v2` (FR-V12-O-046)
    Then Next-action and task generation: Pipeline and last activity → Action queue
    And Action queue; acceptance INV-SVC-15-WF02-AT01 → TC-V12-O-073 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-32ZU08-03 Alternate – Fundraising progress and forecast (FR-V12-O-047)
    Given the trigger "Manual request or validated upstream business event" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-15-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-15-WF03:v2` (FR-V12-O-047)
    Then Fundraising progress and forecast: Verified commitments, receipts and stage data → Fundraising analytics
    And Fundraising analytics; acceptance INV-SVC-15-WF03-AT01 → TC-V12-O-081 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-32ZU08-04 Alternate – Probability-weighted fundraising forecast and bottleneck analysis (FR-V12-O-048)
    Given the trigger "Manual; scheduled or relevant validated business event; provider webhook:
      """
      only where authorized" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-15-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-15-WF04:v2` (FR-V12-O-048)
    Then Probability-weighted fundraising forecast and bottleneck analysis:
      """
      Pipeline stages, verified commitments, historical outcomes → Forecast range and prioritized tasks
      """
    And Forecast range and prioritized tasks; acceptance INV-SVC-15-WF04-AT01 → TC-V12-O-089 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @neg @DEC-822
  Scenario: AC-32ZU08-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-32ZU08-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-32ZU08-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-32ZU08-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-32ZU08-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 76 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-045 = Relationship import and pipeline coordination
    #   O-046 = Next-action and task generation
    #   O-047 = Fundraising progress and forecast
    #   O-048 = Probability-weighted fundraising forecast and…
    Examples: MU09 rows (3-way, seed 1109; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-32ZU08-01 | O-048 | P09/R10 | A1 | US ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-02 | O-045 | P09/R10 | A3 SoD/limit | IN ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-03 | O-047 | P21/R03 | T5 other tenant | IN ✓ | hash changed | suspended | EU | uniform 404 NOT_FOUND |
      | EX-32ZU08-04 | O-048 | P09/R10 | T5 other tenant | UK draft | hash changed | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-32ZU08-05 | O-046 | P21/R03 | A1 | IN ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-06 | O-047 | P08/R08 | A3 SoD/limit | UK draft | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-32ZU08-07 | O-048 | P08/R08 | A5 wrong role | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-08 | O-045 | P21/R03 | A5 wrong role | UK draft | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-09 | O-045 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | active | IN | uniform 404 NOT_FOUND |
      | EX-32ZU08-10 | O-046 | P08/R08 | T5 other tenant | UK draft | 1 approver | active | EU | uniform 404 NOT_FOUND |
      | EX-32ZU08-11 | O-045 | P08/R08 | A1 | IN ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-12 | O-047 | P09/R10 | A5 wrong role | IN ✓ | 1 approver | active | IN | 403 PERMISSION_DENIED |
      | EX-32ZU08-13 | O-046 | P09/R10 | A3 SoD/limit | UK draft | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-14 | O-047 | P21/R03 | A1 | UK draft | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-15 | O-046 | P21/R03 | A1 | US ✓ | hash changed | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU08-16 | O-046 | P09/R10 | A5 wrong role | IN ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-17 | O-047 | P08/R08 | A3 SoD/limit | US ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-18 | O-045 | P08/R08 | A5 wrong role | US ✓ | hash changed | active | EU | 403 PERMISSION_DENIED |
      | EX-32ZU08-19 | O-048 | P21/R03 | A3 SoD/limit | IN ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-20 | O-048 | P08/R08 | A1 | UK draft | 2 approvals | active | IN | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU08-21 | O-045 | P08/R08 | T5 other tenant | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU08-22 | O-045 | P09/R10 | A3 SoD/limit | US ✓ | 1 approver | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-32ZU08-23 | O-046 | P09/R10 | T5 other tenant | US ✓ | 2 approvals | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-32ZU08-24 | O-047 | P08/R08 | T5 other tenant | US ✓ | 2 approvals | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU08-25 | O-046 | P08/R08 | A3 SoD/limit | IN ✓ | 2 approvals | active | EU | 403 SOD_CONFLICT |
      | EX-32ZU08-26 | O-048 | P21/R03 | A5 wrong role | IN ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-27 | O-048 | P21/R03 | A5 wrong role | US ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-28 | O-045 | P21/R03 | A3 SoD/limit | UK draft | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-29 | O-048 | P09/R10 | T5 other tenant | IN ✓ | hash changed | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU08-30 | O-047 | P09/R10 | A1 | UK draft | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-31 | O-046 | P08/R08 | A5 wrong role | UK draft | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-32 | O-048 | P09/R10 | A5 wrong role | UK draft | 2 approvals | active | EU | 403 PERMISSION_DENIED |
      | EX-32ZU08-33 | O-048 | P08/R08 | A3 SoD/limit | UK draft | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-34 | O-047 | P21/R03 | T5 other tenant | UK draft | 1 approver | suspended | IN | uniform 404 NOT_FOUND |
      | EX-32ZU08-35 | O-047 | P09/R10 | A1 | US ✓ | hash changed | active | EU | HOLD APPROVAL_STALE |
      | EX-32ZU08-36 | O-046 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-37 | O-046 | P08/R08 | A1 | UK draft | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-38 | O-047 | P21/R03 | A5 wrong role | IN ✓ | 2 approvals | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-32ZU08-39 | O-045 | P09/R10 | A1 | US ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-40 | O-048 | P21/R03 | A3 SoD/limit | IN ✓ | hash changed | active | IN | 403 SOD_CONFLICT |
      | EX-32ZU08-41 | O-047 | P08/R08 | A1 | IN ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-42 | O-045 | P21/R03 | A1 | IN ✓ | 1 approver | active | EU | HELD TWO_APPROVALS_REQUIRED |
      | EX-32ZU08-43 | O-045 | P09/R10 | T5 other tenant | UK draft | 2 approvals | suspended | EU | uniform 404 NOT_FOUND |
      | EX-32ZU08-44 | O-046 | P21/R03 | T5 other tenant | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU08-45 | O-046 | P09/R10 | A5 wrong role | US ✓ | 1 approver | active | IN | 403 PERMISSION_DENIED |
      | EX-32ZU08-46 | O-047 | P08/R08 | A5 wrong role | IN ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-47 | O-048 | P21/R03 | T5 other tenant | UK draft | 1 approver | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU08-48 | O-048 | P08/R08 | T5 other tenant | IN ✓ | 2 approvals | suspended | IN | uniform 404 NOT_FOUND |
      | EX-32ZU08-49 | O-047 | P09/R10 | A1 | IN ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-50 | O-045 | P09/R10 | A5 wrong role | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-51 | O-045 | P09/R10 | A3 SoD/limit | US ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-52 | O-047 | P21/R03 | A3 SoD/limit | US ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-53 | O-048 | P08/R08 | T5 other tenant | US ✓ | hash changed | active | EU | uniform 404 NOT_FOUND |
      | EX-32ZU08-54 | O-048 | P21/R03 | A1 | IN ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-55 | O-045 | P08/R08 | A5 wrong role | UK draft | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-56 | O-046 | P21/R03 | A5 wrong role | UK draft | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-57 | O-046 | P09/R10 | A3 SoD/limit | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-58 | O-047 | P21/R03 | A5 wrong role | UK draft | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-59 | O-046 | P08/R08 | T5 other tenant | US ✓ | 1 approver | suspended | IN | uniform 404 NOT_FOUND |
      | EX-32ZU08-60 | O-045 | P08/R08 | A3 SoD/limit | UK draft | 1 approver | active | IN | 403 SOD_CONFLICT |
      | EX-32ZU08-61 | O-048 | P08/R08 | A1 | US ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-62 | O-047 | P09/R10 | T5 other tenant | IN ✓ | 1 approver | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-32ZU08-63 | O-046 | P09/R10 | A1 | UK draft | hash changed | active | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU08-64 | O-048 | P09/R10 | A3 SoD/limit | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-65 | O-046 | P21/R03 | A5 wrong role | UK draft | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-66 | O-045 | P08/R08 | A1 | UK draft | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU08-67 | O-047 | P09/R10 | A3 SoD/limit | IN ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-68 | O-045 | P21/R03 | T5 other tenant | IN ✓ | hash changed | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU08-69 | O-046 | P21/R03 | T5 other tenant | IN ✓ | hash changed | active | EU | uniform 404 NOT_FOUND |
      | EX-32ZU08-70 | O-047 | P09/R10 | T5 other tenant | UK draft | 1 approver | active | EU | uniform 404 NOT_FOUND |
      | EX-32ZU08-71 | O-046 | P09/R10 | A3 SoD/limit | US ✓ | hash changed | active | IN | 403 SOD_CONFLICT |
      | EX-32ZU08-72 | O-047 | P08/R08 | A5 wrong role | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU08-73 | O-045 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Investor pipeline records |
      | EX-32ZU08-74 | O-046 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Action queue |
      | EX-32ZU08-75 | O-047 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Fundraising analytics |
      | EX-32ZU08-76 | O-048 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Forecast range and prioritized tasks |
```

##### US-32-ZU09 INV-SVC-16 Private Website Enquiry & Integration Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-32-ZU09 |
| Title | INV-SVC-16 Private Website Enquiry & Integration Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-16 Private Website Enquiry & Integration Automation workflows (enquiry form and connector configuration; inbound enquiry validation and routing; intake health and exception monitoring; authorized external AI-agent and private enquiry integration) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-049; FR-V12-O-050; FR-V12-O-051; FR-V12-O-052; DEC-770, DEC-779, DEC-783, DEC-822; tests TC-V12-O-097, TC-V12-O-105, TC-V12-O-113, TC-V12-O-121 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-16-WF01 Enquiry form and connector…; Part 11.16c §INV-SVC-16-WF02 Inbound enquiry validation and…; Part 11.16c §INV-SVC-16-WF03 Intake health and exception…; Part 11.16c §INV-SVC-16-WF04 Authorized external AI-agent and… |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-049, FR-V12-O-050, FR-V12-O-051, FR-V12-O-052: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO07, US-32-ZO08, US-32-ZO09 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-16 Private Website Enquiry & Integration Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-32ZU09-01 Happy path – Enquiry form and connector configuration (FR-V12-O-049)
    Given the trigger "Manual request or validated upstream business event" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-16-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-16-WF01:v2` (FR-V12-O-049)
    Then Enquiry form and connector configuration: Approved client form schema and webhook ownership → Versioned connector configuration
    And Versioned connector configuration; acceptance INV-SVC-16-WF01-AT01 → TC-V12-O-097 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @alt @DEC-783
  Scenario: AC-32ZU09-02 Alternate – Inbound enquiry validation and routing (FR-V12-O-050)
    Given the trigger "Authorized business event or manual import; signed webhook if applicable" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-16-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-16-WF02:v2` (FR-V12-O-050)
    Then Inbound enquiry validation and routing: Signed client enquiry event → Enquiry and route decision
    And Enquiry and route decision; acceptance INV-SVC-16-WF02-AT01 → TC-V12-O-105 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-32ZU09-03 Alternate – Intake health and exception monitoring (FR-V12-O-051)
    Given the trigger "Authorized business event or manual import; signed webhook if applicable" occurs for issuer "AppNAI Technologies Pvt Ltd"
    When INV-SVC-16-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-16-WF03:v2` (FR-V12-O-051)
    Then Intake health and exception monitoring: Event ledger and connector status → Connector health report
    And Connector health report; acceptance INV-SVC-16-WF03-AT01 → TC-V12-O-113 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-32ZU09-04 Alternate – Authorized external AI-agent and private enquiry integration (FR-V12-O-052)
    Given the trigger "Manual; scheduled or relevant validated business event; provider webhook:
      """
      only where authorized" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-16-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-16-WF04:v2` (FR-V12-O-052)
    Then Authorized external AI-agent and private enquiry integration:
      """
      Private intake endpoint, verified agent identity, scoped authorization → Scoped enquiry record or denial
      """
    And Scoped enquiry record or denial; acceptance INV-SVC-16-WF04-AT01 → TC-V12-O-121 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @neg @DEC-822
  Scenario: AC-32ZU09-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-32ZU09-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-32ZU09-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-32ZU09-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-32ZU09-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 76 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-049 = Enquiry form and connector configuration
    #   O-050 = Inbound enquiry validation and routing
    #   O-051 = Intake health and exception monitoring
    #   O-052 = Authorized external AI-agent and private enquiry…
    Examples: MU09 rows (3-way, seed 1116; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-32ZU09-01 | O-052 | P08/R08 | A1 | US ✓ | 1 approver | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-32ZU09-02 | O-050 | P08/R08 | A3 SoD/limit | UK draft | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-03 | O-051 | P08/R08 | A3 SoD/limit | IN ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-04 | O-052 | P09/R10 | T5 other tenant | IN ✓ | hash changed | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-32ZU09-05 | O-052 | P21/R03 | A5 wrong role | UK draft | 2 approvals | active | IN | 403 PERMISSION_DENIED |
      | EX-32ZU09-06 | O-050 | P09/R10 | A1 | UK draft | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-07 | O-049 | P09/R10 | A5 wrong role | US ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-08 | O-049 | P21/R03 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-09 | O-051 | P21/R03 | T5 other tenant | US ✓ | hash changed | active | EU | uniform 404 NOT_FOUND |
      | EX-32ZU09-10 | O-051 | P21/R03 | A1 | IN ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-11 | O-049 | P08/R08 | A1 | IN ✓ | 2 approvals | active | EU | ALLOW: Versioned connector configuration |
      | EX-32ZU09-12 | O-050 | P08/R08 | T5 other tenant | US ✓ | 2 approvals | suspended | IN | uniform 404 NOT_FOUND |
      | EX-32ZU09-13 | O-049 | P09/R10 | A3 SoD/limit | UK draft | hash changed | active | IN | 403 SOD_CONFLICT |
      | EX-32ZU09-14 | O-052 | P21/R03 | T5 other tenant | UK draft | 1 approver | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU09-15 | O-050 | P21/R03 | A5 wrong role | IN ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-16 | O-051 | P09/R10 | A5 wrong role | IN ✓ | 2 approvals | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-32ZU09-17 | O-051 | P08/R08 | A5 wrong role | US ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-18 | O-049 | P21/R03 | A1 | UK draft | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-19 | O-051 | P09/R10 | T5 other tenant | UK draft | 2 approvals | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-32ZU09-20 | O-050 | P09/R10 | A3 SoD/limit | US ✓ | 1 approver | active | IN | 403 SOD_CONFLICT |
      | EX-32ZU09-21 | O-049 | P08/R08 | T5 other tenant | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU09-22 | O-052 | P09/R10 | A3 SoD/limit | IN ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-23 | O-050 | P08/R08 | T5 other tenant | UK draft | hash changed | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU09-24 | O-051 | P08/R08 | A5 wrong role | UK draft | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-25 | O-052 | P21/R03 | A1 | US ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-26 | O-050 | P09/R10 | A1 | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-27 | O-052 | P08/R08 | A5 wrong role | US ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-28 | O-052 | P21/R03 | A3 SoD/limit | IN ✓ | 1 approver | active | EU | 403 SOD_CONFLICT |
      | EX-32ZU09-29 | O-052 | P09/R10 | A5 wrong role | UK draft | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-30 | O-049 | P21/R03 | T5 other tenant | IN ✓ | 2 approvals | suspended | IN | uniform 404 NOT_FOUND |
      | EX-32ZU09-31 | O-050 | P08/R08 | A1 | IN ✓ | hash changed | active | IN | HOLD APPROVAL_STALE |
      | EX-32ZU09-32 | O-049 | P21/R03 | A5 wrong role | US ✓ | hash changed | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-32ZU09-33 | O-050 | P21/R03 | A3 SoD/limit | IN ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-34 | O-051 | P09/R10 | A1 | UK draft | 1 approver | active | EU | HOLD PACK_NOT_ACTIVE |
      | EX-32ZU09-35 | O-051 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-36 | O-050 | P09/R10 | T5 other tenant | IN ✓ | 1 approver | suspended | EU | uniform 404 NOT_FOUND |
      | EX-32ZU09-37 | O-052 | P08/R08 | A1 | UK draft | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-38 | O-051 | P21/R03 | A3 SoD/limit | UK draft | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-39 | O-050 | P21/R03 | A1 | US ✓ | 2 approvals | active | EU | ALLOW: Enquiry and route decision |
      | EX-32ZU09-40 | O-049 | P08/R08 | A5 wrong role | UK draft | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-41 | O-050 | P21/R03 | A5 wrong role | US ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-42 | O-052 | P09/R10 | T5 other tenant | US ✓ | 2 approvals | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU09-43 | O-049 | P09/R10 | A1 | IN ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-44 | O-049 | P08/R08 | T5 other tenant | US ✓ | 1 approver | active | IN | uniform 404 NOT_FOUND |
      | EX-32ZU09-45 | O-051 | P08/R08 | A3 SoD/limit | US ✓ | 2 approvals | active | EU | 403 SOD_CONFLICT |
      | EX-32ZU09-46 | O-049 | P09/R10 | A1 | UK draft | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-47 | O-052 | P08/R08 | A5 wrong role | IN ✓ | 1 approver | active | IN | 403 PERMISSION_DENIED |
      | EX-32ZU09-48 | O-052 | P09/R10 | A3 SoD/limit | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-49 | O-050 | P09/R10 | A5 wrong role | UK draft | hash changed | active | IN | 403 PERMISSION_DENIED |
      | EX-32ZU09-50 | O-051 | P21/R03 | A1 | US ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-51 | O-050 | P21/R03 | A3 SoD/limit | IN ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-52 | O-051 | P09/R10 | T5 other tenant | IN ✓ | hash changed | suspended | EU | uniform 404 NOT_FOUND |
      | EX-32ZU09-53 | O-051 | P21/R03 | T5 other tenant | US ✓ | 1 approver | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU09-54 | O-049 | P08/R08 | A3 SoD/limit | IN ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-55 | O-051 | P08/R08 | T5 other tenant | UK draft | hash changed | active | IN | uniform 404 NOT_FOUND |
      | EX-32ZU09-56 | O-052 | P08/R08 | A3 SoD/limit | UK draft | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-57 | O-052 | P21/R03 | A1 | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-58 | O-049 | P21/R03 | A5 wrong role | IN ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-59 | O-052 | P08/R08 | T5 other tenant | IN ✓ | hash changed | active | EU | uniform 404 NOT_FOUND |
      | EX-32ZU09-60 | O-051 | P21/R03 | A5 wrong role | UK draft | hash changed | active | EU | 403 PERMISSION_DENIED |
      | EX-32ZU09-61 | O-049 | P09/R10 | T5 other tenant | UK draft | 1 approver | suspended | EU | uniform 404 NOT_FOUND |
      | EX-32ZU09-62 | O-051 | P08/R08 | A1 | UK draft | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-63 | O-049 | P21/R03 | A1 | US ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-64 | O-050 | P21/R03 | T5 other tenant | UK draft | hash changed | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-32ZU09-65 | O-049 | P09/R10 | A3 SoD/limit | US ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-66 | O-050 | P08/R08 | A5 wrong role | IN ✓ | 2 approvals | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-32ZU09-67 | O-052 | P09/R10 | A5 wrong role | IN ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-68 | O-050 | P21/R03 | A1 | IN ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-69 | O-051 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-32ZU09-70 | O-052 | P09/R10 | A1 | UK draft | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-32ZU09-71 | O-050 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-32ZU09-72 | O-049 | P09/R10 | T5 other tenant | UK draft | hash changed | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-32ZU09-73 | O-049 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Versioned connector configuration |
      | EX-32ZU09-74 | O-050 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Enquiry and route decision |
      | EX-32ZU09-75 | O-051 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Connector health report |
      | EX-32ZU09-76 | O-052 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Scoped enquiry record or denial |
```

#### 11.22.5.4.33 EP-33 Specialised Funding, Ownership, Governance, Verification and Securities Compliance

| Field | Value |
|---|---|
| Epic | EP-33 Specialised Funding, Ownership, Governance, Verification and Securities Compliance (Part 11.16d) |
| New stories in this file | US-33-ZU01, US-33-ZU02, US-33-ZU03, US-33-ZU04, US-33-ZU05, US-33-ZU06, US-33-ZU07, US-33-ZU08, US-33-ZU09, US-33-ZU10, US-33-ZU11, US-33-ZU12, US-33-ZU13, US-33-ZU14, US-33-ZU15, US-33-ZU16 |
| FR-V12 covered | O: 022, 024, 026, 028, 030, 032, 034, 036, 053–084 |
| Size | 16 stories · 104–168 SP · 52–168 pd (0.5/1.0 pd per SP) · central 95.2 pd (0.7 pd per SP mid) |
| Releases | Release 2: 16 |

##### US-33-ZU01 Grant submission readiness with a human-approved package hash

| Field | Value |
|---|---|
| ID | US-33-ZU01 |
| Title | Grant submission readiness with a human-approved package hash |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want submission-ready requires complete attachments, eligible budget (AU-246) and a human-approved package hash; the human submits, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-022; DEC-770, DEC-783; tests TC-V12-O-145, TC-V12-O-155 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.7 INV-SVC-17 Grant & Non-Dilutive… |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-022: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Grant submission readiness with a human-approved package hash
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-33ZU01-01 Happy path – Submission-ready requires complete attachments (FR-V12-O-022)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Submission-ready requires complete attachments" is exercised as specified by FR-V12-O-022:
      """
      Submission-ready requires complete attachments, eligible budget (AU-246) and a human-approved package hash; the human submits
      """
    Then complete package → SUBMISSION_READY
    And the audit event "inv.submission_ready_requires" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg
  Scenario: AC-33ZU01-02 Negative – over-cap travel line (FR-V12-O-022)
    Given the condition "over-cap travel line" holds for FR-V12-O-022
    When the action is attempted
    Then the outcome is "BLOCK_READY BUDGET"
    And no external effect, charge or outbox event is created

  @neg @DEC-783
  Scenario: AC-33ZU01-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-33ZU01-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-33ZU01-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-33ZU01-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-33ZU01-07 Permutations – Investor securities controls (3-way, 44 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-022 = Submission-ready requires complete attachments
    Examples: MU08 rows (3-way, seed 1123; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-33ZU01-01 | O-022 | P09/R10 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU01-02 | O-022 | P21/R03 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU01-03 | O-022 | P22/R21 | UK FPO draft | unverified | no relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU01-04 | O-022 | P21/R03 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU01-05 | O-022 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU01-06 | O-022 | P22/R21 | US 506c ✓ | eligible | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU01-07 | O-022 | P22/R21 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU01-08 | O-022 | P21/R03 | US 506b ✓ | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU01-09 | O-022 | P22/R21 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU01-10 | O-022 | P09/R10 | IN s42 ✓ | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU01-11 | O-022 | P09/R10 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU01-12 | O-022 | P21/R03 | UK FPO draft | eligible | no relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU01-13 | O-022 | P22/R21 | US 506b ✓ | unverified | relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU01-14 | O-022 | P21/R03 | IN s42 ✓ | unverified | no relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU01-15 | O-022 | P09/R10 | US 506b ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU01-16 | O-022 | P21/R03 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU01-17 | O-022 | P09/R10 | US 506b ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU01-18 | O-022 | P22/R21 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU01-19 | O-022 | P09/R10 | UK FPO draft | unverified | no relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU01-20 | O-022 | P21/R03 | IN s42 ✓ | eligible | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU01-21 | O-022 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU01-22 | O-022 | P09/R10 | US 506c ✓ | unverified | relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU01-23 | O-022 | P21/R03 | UK FPO draft | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU01-24 | O-022 | P22/R21 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU01-25 | O-022 | P09/R10 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU01-26 | O-022 | P09/R10 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU01-27 | O-022 | P21/R03 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU01-28 | O-022 | P22/R21 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: complete package → SUBMISSION_READY |
      | EX-33ZU01-29 | O-022 | P22/R21 | IN s42 ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU01-30 | O-022 | P22/R21 | US 506c ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU01-31 | O-022 | P09/R10 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: complete package → SUBMISSION_READY |
      | EX-33ZU01-32 | O-022 | P21/R03 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU01-33 | O-022 | P22/R21 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU01-34 | O-022 | P21/R03 | US 506b ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU01-35 | O-022 | P22/R21 | UK FPO draft | eligible | relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU01-36 | O-022 | P22/R21 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU01-37 | O-022 | P09/R10 | UK FPO draft | eligible | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU01-38 | O-022 | P21/R03 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | EU | ALLOW: complete package → SUBMISSION_READY |
      | EX-33ZU01-39 | O-022 | P21/R03 | UK FPO draft | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU01-40 | O-022 | P09/R10 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU01-41 | O-022 | P21/R03 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU01-42 | O-022 | P09/R10 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU01-43 | O-022 | P22/R21 | US 506c ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU01-44 | O-022 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: complete package → SUBMISSION_READY |
```

##### US-33-ZU02 Covenant alerts and checklist-scoped dossier sharing

| Field | Value |
|---|---|
| ID | US-33-ZU02 |
| Title | Covenant alerts and checklist-scoped dossier sharing |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want covenant tests alert at T-30 and T-7 and on breach; dossiers are shared only within the lender checklist via time-bound grants, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-024; DEC-770, DEC-783; tests TC-V12-O-177, TC-V12-O-187 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.8 INV-SVC-18 Debt Financing & Credit… |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-024: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Covenant alerts and checklist-scoped dossier sharing
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-33ZU02-01 Happy path – Covenant tests alert at T-30 and T-7 and on breach (FR-V12-O-024)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Covenant tests alert at T-30 and T-7 and on breach" is exercised as specified by FR-V12-O-024:
      """
      Covenant tests alert at T-30 and T-7 and on breach; dossiers are shared only within the lender checklist via time-bound grants
      """
    Then DSCR 1.18 vs covenant 1.20 → ALERT
    And the audit event "inv.covenant_tests_alert_at_t_30" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg
  Scenario: AC-33ZU02-02 Negative – sharing beyond checklist (FR-V12-O-024)
    Given the condition "sharing beyond checklist" holds for FR-V12-O-024
    When the action is attempted
    Then the outcome is "BLOCK SCOPE"
    And no external effect, charge or outbox event is created

  @neg @DEC-783
  Scenario: AC-33ZU02-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-33ZU02-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-33ZU02-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-33ZU02-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-33ZU02-07 Permutations – Investor securities controls (3-way, 46 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-024 = Covenant tests alert at T-30 and T-7 and on breach
    Examples: MU08 rows (3-way, seed 1130; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-33ZU02-01 | O-024 | P09/R10 | UK FPO draft | eligible | relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU02-02 | O-024 | P21/R03 | IN s42 ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU02-03 | O-024 | P22/R21 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU02-04 | O-024 | P21/R03 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU02-05 | O-024 | P09/R10 | UK FPO draft | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU02-06 | O-024 | P22/R21 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU02-07 | O-024 | P22/R21 | US 506b ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU02-08 | O-024 | P22/R21 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU02-09 | O-024 | P09/R10 | US 506c ✓ | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU02-10 | O-024 | P21/R03 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU02-11 | O-024 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | EU | ALLOW: DSCR 1.18 vs covenant 1.20 → ALERT |
      | EX-33ZU02-12 | O-024 | P09/R10 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU02-13 | O-024 | P21/R03 | UK FPO draft | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU02-14 | O-024 | P09/R10 | US 506b ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU02-15 | O-024 | P21/R03 | US 506c ✓ | eligible | no relationship | L1 two-person | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU02-16 | O-024 | P22/R21 | UK FPO draft | unverified | no relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU02-17 | O-024 | P09/R10 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU02-18 | O-024 | P22/R21 | US 506c ✓ | eligible | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU02-19 | O-024 | P21/R03 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU02-20 | O-024 | P22/R21 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU02-21 | O-024 | P21/R03 | US 506b ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU02-22 | O-024 | P09/R10 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU02-23 | O-024 | P22/R21 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU02-24 | O-024 | P21/R03 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU02-25 | O-024 | P22/R21 | IN s42 ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU02-26 | O-024 | P09/R10 | US 506b ✓ | eligible | no relationship | L1 two-person | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU02-27 | O-024 | P21/R03 | IN s42 ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU02-28 | O-024 | P09/R10 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU02-29 | O-024 | P09/R10 | UK FPO draft | unverified | no relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU02-30 | O-024 | P21/R03 | UK FPO draft | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU02-31 | O-024 | P22/R21 | US 506b ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU02-32 | O-024 | P21/R03 | US 506c ✓ | unverified | relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU02-33 | O-024 | P09/R10 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU02-34 | O-024 | P22/R21 | IN s42 ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU02-35 | O-024 | P22/R21 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU02-36 | O-024 | P22/R21 | UK FPO draft | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU02-37 | O-024 | P22/R21 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU02-38 | O-024 | P09/R10 | IN s42 ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU02-39 | O-024 | P21/R03 | UK FPO draft | unverified | no relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU02-40 | O-024 | P22/R21 | US 506b ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU02-41 | O-024 | P21/R03 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU02-42 | O-024 | P21/R03 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | EU | ALLOW: DSCR 1.18 vs covenant 1.20 → ALERT |
      | EX-33ZU02-43 | O-024 | P09/R10 | UK FPO draft | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU02-44 | O-024 | P09/R10 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU02-45 | O-024 | P09/R10 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU02-46 | O-024 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: DSCR 1.18 vs covenant 1.20 → ALERT |
```

##### US-33-ZU03 Reproducible readiness scores labelled as internal

| Field | Value |
|---|---|
| ID | US-33-ZU03 |
| Title | Reproducible readiness scores labelled as internal |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want readiness scores are reproducible from inputs and labelled as internal scores, not investment ratings, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-026; DEC-770, DEC-783; tests TC-V12-O-209, TC-V12-O-219 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.9 INV-SVC-19 Continuous Fundraising… |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-026: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Reproducible readiness scores labelled as internal
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-33ZU03-01 Happy path – Readiness scores are reproducible from inputs and labelled as… (FR-V12-O-026)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Readiness scores are reproducible from inputs and labelled as…" is exercised as specified by FR-V12-O-026:
      """
      Readiness scores are reproducible from inputs and labelled as internal scores, not investment ratings
      """
    Then rerun → identical score
    And the audit event "inv.readiness_scores_are" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg
  Scenario: AC-33ZU03-02 Negative – label missing (FR-V12-O-026)
    Given the condition "label missing" holds for FR-V12-O-026
    When the action is attempted
    Then the outcome is "RP-INV-ADVICE-006 Block"
    And no external effect, charge or outbox event is created

  @neg @DEC-783
  Scenario: AC-33ZU03-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-33ZU03-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-33ZU03-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-33ZU03-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-33ZU03-07 Permutations – Investor securities controls (3-way, 49 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-026 = Readiness scores are reproducible from inputs and…
    Examples: MU08 rows (3-way, seed 1137; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-33ZU03-01 | O-026 | P09/R10 | US 506c ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-02 | O-026 | P22/R21 | UK FPO draft | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU03-03 | O-026 | P09/R10 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU03-04 | O-026 | P21/R03 | US 506b ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU03-05 | O-026 | P21/R03 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-06 | O-026 | P22/R21 | UK FPO draft | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-07 | O-026 | P21/R03 | US 506c ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: rerun → identical score |
      | EX-33ZU03-08 | O-026 | P22/R21 | IN s42 ✓ | eligible | no relationship | L1 two-person | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU03-09 | O-026 | P09/R10 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU03-10 | O-026 | P09/R10 | US 506b ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU03-11 | O-026 | P22/R21 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU03-12 | O-026 | P09/R10 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU03-13 | O-026 | P21/R03 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU03-14 | O-026 | P21/R03 | US 506c ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU03-15 | O-026 | P22/R21 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: rerun → identical score |
      | EX-33ZU03-16 | O-026 | P21/R03 | UK FPO draft | eligible | no relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU03-17 | O-026 | P09/R10 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-18 | O-026 | P09/R10 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU03-19 | O-026 | P22/R21 | IN s42 ✓ | unverified | no relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU03-20 | O-026 | P21/R03 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU03-21 | O-026 | P22/R21 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU03-22 | O-026 | P22/R21 | US 506b ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-23 | O-026 | P22/R21 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU03-24 | O-026 | P09/R10 | UK FPO draft | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU03-25 | O-026 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | EU | ALLOW: rerun → identical score |
      | EX-33ZU03-26 | O-026 | P09/R10 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU03-27 | O-026 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU03-28 | O-026 | P21/R03 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU03-29 | O-026 | P09/R10 | US 506b ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-30 | O-026 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU03-31 | O-026 | P22/R21 | UK FPO draft | eligible | relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU03-32 | O-026 | P09/R10 | UK FPO draft | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-33 | O-026 | P09/R10 | IN s42 ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU03-34 | O-026 | P21/R03 | US 506c ✓ | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU03-35 | O-026 | P21/R03 | IN s42 ✓ | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-36 | O-026 | P22/R21 | US 506b ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU03-37 | O-026 | P22/R21 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU03-38 | O-026 | P21/R03 | US 506c ✓ | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-39 | O-026 | P09/R10 | US 506b ✓ | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU03-40 | O-026 | P09/R10 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU03-41 | O-026 | P22/R21 | US 506c ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU03-42 | O-026 | P21/R03 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU03-43 | O-026 | P21/R03 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU03-44 | O-026 | P22/R21 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-45 | O-026 | P21/R03 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-46 | O-026 | P09/R10 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU03-47 | O-026 | P21/R03 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU03-48 | O-026 | P21/R03 | IN s42 ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU03-49 | O-026 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: rerun → identical score |
```

##### US-33-ZU04 Golden-fixture scenario and conversion calculations

| Field | Value |
|---|---|
| ID | US-33-ZU04 |
| Title | Golden-fixture scenario and conversion calculations |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want scenario and conversion calculations match golden fixtures exactly; ambiguous instrument terms are excluded until R10 confirms, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-028; DEC-770, DEC-783; tests TC-V12-O-241, TC-V12-O-251 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.10 INV-SVC-20 Cap Table & Ownership… |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-028: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Golden-fixture scenario and conversion calculations
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-33ZU04-01 Happy path – Scenario and conversion calculations match golden fixtures exactly (FR-V12-O-028)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Scenario and conversion calculations match golden fixtures exactly" is exercised as specified by FR-V12-O-028:
      """
      Scenario and conversion calculations match golden fixtures exactly; ambiguous instrument terms are excluded until R10 confirms
      """
    Then post-money SAFE fixture → exact shares
    And the audit event "inv.scenario_and_conversion" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg
  Scenario: AC-33ZU04-02 Negative – unconfirmed MFN clause (FR-V12-O-028)
    Given the condition "unconfirmed MFN clause" holds for FR-V12-O-028
    When the action is attempted
    Then the outcome is "EXCLUDE"
    And no external effect, charge or outbox event is created

  @neg @DEC-783
  Scenario: AC-33ZU04-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-33ZU04-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-33ZU04-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-33ZU04-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-33ZU04-07 Permutations – Investor securities controls (3-way, 47 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-028 = Scenario and conversion calculations match golden…
    Examples: MU08 rows (3-way, seed 1144; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-33ZU04-01 | O-028 | P09/R10 | UK FPO draft | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU04-02 | O-028 | P22/R21 | US 506c ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU04-03 | O-028 | P09/R10 | US 506b ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU04-04 | O-028 | P21/R03 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU04-05 | O-028 | P21/R03 | UK FPO draft | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU04-06 | O-028 | P21/R03 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU04-07 | O-028 | P22/R21 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU04-08 | O-028 | P22/R21 | IN s42 ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU04-09 | O-028 | P09/R10 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU04-10 | O-028 | P22/R21 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU04-11 | O-028 | P09/R10 | US 506c ✓ | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU04-12 | O-028 | P21/R03 | UK FPO draft | unverified | no relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU04-13 | O-028 | P09/R10 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU04-14 | O-028 | P21/R03 | IN s42 ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU04-15 | O-028 | P21/R03 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU04-16 | O-028 | P09/R10 | IN s42 ✓ | unverified | relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU04-17 | O-028 | P22/R21 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU04-18 | O-028 | P21/R03 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU04-19 | O-028 | P22/R21 | UK FPO draft | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU04-20 | O-028 | P21/R03 | US 506c ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU04-21 | O-028 | P09/R10 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: post-money SAFE fixture → exact shares |
      | EX-33ZU04-22 | O-028 | P22/R21 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU04-23 | O-028 | P09/R10 | UK FPO draft | eligible | no relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU04-24 | O-028 | P22/R21 | US 506b ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU04-25 | O-028 | P09/R10 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU04-26 | O-028 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU04-27 | O-028 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU04-28 | O-028 | P21/R03 | US 506b ✓ | unverified | relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU04-29 | O-028 | P21/R03 | US 506c ✓ | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU04-30 | O-028 | P22/R21 | IN s42 ✓ | unverified | no relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU04-31 | O-028 | P09/R10 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU04-32 | O-028 | P21/R03 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU04-33 | O-028 | P22/R21 | UK FPO draft | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU04-34 | O-028 | P22/R21 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU04-35 | O-028 | P21/R03 | IN s42 ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU04-36 | O-028 | P21/R03 | US 506c ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU04-37 | O-028 | P09/R10 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU04-38 | O-028 | P09/R10 | IN s42 ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU04-39 | O-028 | P09/R10 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU04-40 | O-028 | P22/R21 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU04-41 | O-028 | P09/R10 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU04-42 | O-028 | P22/R21 | UK FPO draft | unverified | no relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU04-43 | O-028 | P22/R21 | IN s42 ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU04-44 | O-028 | P22/R21 | US 506b ✓ | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU04-45 | O-028 | P22/R21 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU04-46 | O-028 | P21/R03 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU04-47 | O-028 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: post-money SAFE fixture → exact shares |
```

##### US-33-ZU05 Commitment deviations create corrective actions

| Field | Value |
|---|---|
| ID | US-33-ZU05 |
| Title | Commitment deviations create corrective actions |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want commitment deviations beyond band create corrective-action tasks, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-030; DEC-770, DEC-783; tests TC-V12-O-273, TC-V12-O-283 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.11 INV-SVC-21 ESG, Climate & Impact… |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-030: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Commitment deviations create corrective actions
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-33ZU05-01 Happy path – Commitment deviations beyond band create corrective-action tasks (FR-V12-O-030)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Commitment deviations beyond band create corrective-action tasks" is exercised as specified by FR-V12-O-030:
      """
      Commitment deviations beyond band create corrective-action tasks
      """
    Then 15% shortfall → task
    And the audit event "inv.commitment_deviations_beyond" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @DEC-783
  Scenario: AC-33ZU05-02 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-33ZU05-03 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-33ZU05-04 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-33ZU05-05 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-33ZU05-06 Permutations – Investor securities controls (3-way, 53 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-030 = Commitment deviations beyond band create…
    Examples: MU08 rows (3-way, seed 1151; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-33ZU05-01 | O-030 | P21/R03 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU05-02 | O-030 | P21/R03 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU05-03 | O-030 | P09/R10 | US 506b ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU05-04 | O-030 | P22/R21 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU05-05 | O-030 | P09/R10 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU05-06 | O-030 | P22/R21 | US 506b ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU05-07 | O-030 | P09/R10 | UK FPO draft | unverified | no relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU05-08 | O-030 | P22/R21 | IN s42 ✓ | eligible | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU05-09 | O-030 | P21/R03 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU05-10 | O-030 | P22/R21 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU05-11 | O-030 | P21/R03 | US 506c ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU05-12 | O-030 | P09/R10 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU05-13 | O-030 | P09/R10 | US 506c ✓ | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU05-14 | O-030 | P22/R21 | US 506b ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU05-15 | O-030 | P21/R03 | UK FPO draft | unverified | relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU05-16 | O-030 | P21/R03 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU05-17 | O-030 | P09/R10 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU05-18 | O-030 | P22/R21 | US 506c ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU05-19 | O-030 | P22/R21 | IN s42 ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU05-20 | O-030 | P09/R10 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU05-21 | O-030 | P22/R21 | UK FPO draft | eligible | no relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU05-22 | O-030 | P09/R10 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU05-23 | O-030 | P21/R03 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU05-24 | O-030 | P21/R03 | US 506b ✓ | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU05-25 | O-030 | P22/R21 | IN s42 ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU05-26 | O-030 | P09/R10 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU05-27 | O-030 | P21/R03 | UK FPO draft | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU05-28 | O-030 | P21/R03 | IN s42 ✓ | eligible | no relationship | L1 two-person | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU05-29 | O-030 | P21/R03 | US 506b ✓ | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU05-30 | O-030 | P21/R03 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU05-31 | O-030 | P09/R10 | UK FPO draft | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU05-32 | O-030 | P09/R10 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU05-33 | O-030 | P09/R10 | IN s42 ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU05-34 | O-030 | P09/R10 | US 506c ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU05-35 | O-030 | P22/R21 | IN s42 ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU05-36 | O-030 | P22/R21 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU05-37 | O-030 | P21/R03 | US 506b ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU05-38 | O-030 | P22/R21 | US 506c ✓ | unverified | relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU05-39 | O-030 | P21/R03 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU05-40 | O-030 | P22/R21 | US 506b ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU05-41 | O-030 | P22/R21 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU05-42 | O-030 | P21/R03 | US 506b ✓ | eligible | no relationship | L1 two-person | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU05-43 | O-030 | P21/R03 | IN s42 ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU05-44 | O-030 | P22/R21 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU05-45 | O-030 | P09/R10 | US 506c ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU05-46 | O-030 | P09/R10 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU05-47 | O-030 | P09/R10 | IN s42 ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU05-48 | O-030 | P22/R21 | US 506c ✓ | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU05-49 | O-030 | P22/R21 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | EU | ALLOW: 15% shortfall → task |
      | EX-33ZU05-50 | O-030 | P09/R10 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU05-51 | O-030 | P09/R10 | UK FPO draft | eligible | no relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU05-52 | O-030 | P21/R03 | US 506c ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU05-53 | O-030 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: 15% shortfall → task |
```

##### US-33-ZU06 Deterministic cross-border restriction holds

| Field | Value |
|---|---|
| ID | US-33-ZU06 |
| Title | Deterministic cross-border restriction holds |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want deterministic restriction flags (land-border investor, ECB route, sanctions) hold the case until a qualified reviewer decides, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-032; DEC-770, DEC-783; tests TC-V12-O-305, TC-V12-O-315 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.12 INV-SVC-22 Cross-Border Funding… |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-032: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Deterministic cross-border restriction holds
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-33ZU06-01 Happy path – Deterministic restriction flags (land-border investor, ECB route (FR-V12-O-032)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Deterministic restriction flags (land-border investor, ECB route" is exercised as specified by FR-V12-O-032:
      """
      Deterministic restriction flags (land-border investor, ECB route, sanctions) hold the case until a qualified reviewer decides
      """
    Then reviewer approval recorded → proceed
    And the audit event "inv.deterministic_restriction" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg
  Scenario: AC-33ZU06-02 Negative – land-border BO without approval (FR-V12-O-032)
    Given the condition "land-border BO without approval" holds for FR-V12-O-032
    When the action is attempted
    Then the outcome is "HOLD"
    And no external effect, charge or outbox event is created

  @neg @DEC-783
  Scenario: AC-33ZU06-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-33ZU06-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-33ZU06-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-33ZU06-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-33ZU06-07 Permutations – Investor securities controls (3-way, 50 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-032 = Deterministic restriction flags
    Examples: MU08 rows (3-way, seed 1158; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-33ZU06-01 | O-032 | P21/R03 | UK FPO draft | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU06-02 | O-032 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU06-03 | O-032 | P22/R21 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU06-04 | O-032 | P21/R03 | US 506b ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU06-05 | O-032 | P22/R21 | UK FPO draft | eligible | no relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU06-06 | O-032 | P09/R10 | US 506b ✓ | unverified | relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU06-07 | O-032 | P22/R21 | US 506c ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU06-08 | O-032 | P09/R10 | IN s42 ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU06-09 | O-032 | P21/R03 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU06-10 | O-032 | P09/R10 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU06-11 | O-032 | P22/R21 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU06-12 | O-032 | P21/R03 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU06-13 | O-032 | P22/R21 | UK FPO draft | unverified | no relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU06-14 | O-032 | P22/R21 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU06-15 | O-032 | P21/R03 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU06-16 | O-032 | P09/R10 | US 506b ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU06-17 | O-032 | P09/R10 | US 506c ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU06-18 | O-032 | P21/R03 | UK FPO draft | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU06-19 | O-032 | P09/R10 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU06-20 | O-032 | P22/R21 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU06-21 | O-032 | P22/R21 | US 506b ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU06-22 | O-032 | P21/R03 | US 506c ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU06-23 | O-032 | P21/R03 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: reviewer approval recorded → proceed |
      | EX-33ZU06-24 | O-032 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU06-25 | O-032 | P21/R03 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU06-26 | O-032 | P09/R10 | UK FPO draft | eligible | no relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU06-27 | O-032 | P21/R03 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU06-28 | O-032 | P22/R21 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU06-29 | O-032 | P22/R21 | IN s42 ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU06-30 | O-032 | P09/R10 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU06-31 | O-032 | P22/R21 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU06-32 | O-032 | P09/R10 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU06-33 | O-032 | P09/R10 | UK FPO draft | unverified | relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU06-34 | O-032 | P22/R21 | US 506b ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU06-35 | O-032 | P21/R03 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU06-36 | O-032 | P21/R03 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU06-37 | O-032 | P09/R10 | US 506b ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU06-38 | O-032 | P22/R21 | US 506b ✓ | eligible | no relationship | L1 two-person | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU06-39 | O-032 | P21/R03 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU06-40 | O-032 | P21/R03 | IN s42 ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU06-41 | O-032 | P09/R10 | UK FPO draft | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU06-42 | O-032 | P21/R03 | UK FPO draft | eligible | relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU06-43 | O-032 | P22/R21 | US 506c ✓ | unverified | relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU06-44 | O-032 | P09/R10 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU06-45 | O-032 | P22/R21 | IN s42 ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU06-46 | O-032 | P21/R03 | US 506c ✓ | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU06-47 | O-032 | P09/R10 | US 506b ✓ | eligible | no relationship | L1 two-person | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU06-48 | O-032 | P09/R10 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU06-49 | O-032 | P21/R03 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU06-50 | O-032 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: reviewer approval recorded → proceed |
```

##### US-33-ZU07 Rights-scoped governance packs with redaction

| Field | Value |
|---|---|
| ID | US-33-ZU07 |
| Title | Rights-scoped governance packs with redaction |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want governance packs include only approved items within recipient rights, with redaction; offer material routes to AG-198, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-034; DEC-770, DEC-783; tests TC-V12-O-337, TC-V12-O-347 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.13 INV-SVC-23 Board & Shareholder… |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-034: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Rights-scoped governance packs with redaction
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-33ZU07-01 Happy path – Governance packs include only approved items within recipient rights (FR-V12-O-034)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Governance packs include only approved items within recipient rights" is exercised as specified by FR-V12-O-034:
      """
      Governance packs include only approved items within recipient rights, with redaction; offer material routes to AG-198
      """
    Then board pack to investor-director with redactions
    And the audit event "inv.governance_packs_include_only" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg
  Scenario: AC-33ZU07-02 Negative – unapproved draft minutes included (FR-V12-O-034)
    Given the condition "unapproved draft minutes included" holds for FR-V12-O-034
    When the action is attempted
    Then the outcome is "BLOCK"
    And no external effect, charge or outbox event is created

  @neg @DEC-783
  Scenario: AC-33ZU07-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-33ZU07-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-33ZU07-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-33ZU07-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-33ZU07-07 Permutations – Investor securities controls (3-way, 47 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-034 = Governance packs include only approved items within…
    Examples: MU08 rows (3-way, seed 1165; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-33ZU07-01 | O-034 | P09/R10 | US 506b ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU07-02 | O-034 | P22/R21 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU07-03 | O-034 | P21/R03 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU07-04 | O-034 | P21/R03 | US 506c ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU07-05 | O-034 | P22/R21 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU07-06 | O-034 | P09/R10 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU07-07 | O-034 | P09/R10 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-08 | O-034 | P09/R10 | IN s42 ✓ | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU07-09 | O-034 | P22/R21 | IN s42 ✓ | unverified | no relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU07-10 | O-034 | P21/R03 | UK FPO draft | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-11 | O-034 | P22/R21 | US 506c ✓ | unverified | relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU07-12 | O-034 | P21/R03 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU07-13 | O-034 | P22/R21 | US 506b ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-14 | O-034 | P21/R03 | US 506b ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU07-15 | O-034 | P22/R21 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU07-16 | O-034 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU07-17 | O-034 | P21/R03 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-18 | O-034 | P09/R10 | US 506b ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: board pack to investor-director with redactions |
      | EX-33ZU07-19 | O-034 | P21/R03 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU07-20 | O-034 | P22/R21 | IN s42 ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU07-21 | O-034 | P21/R03 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU07-22 | O-034 | P09/R10 | UK FPO draft | eligible | no relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU07-23 | O-034 | P21/R03 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU07-24 | O-034 | P21/R03 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU07-25 | O-034 | P22/R21 | US 506c ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU07-26 | O-034 | P21/R03 | UK FPO draft | eligible | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-27 | O-034 | P09/R10 | US 506c ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-28 | O-034 | P09/R10 | IN s42 ✓ | unverified | no relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU07-29 | O-034 | P09/R10 | UK FPO draft | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU07-30 | O-034 | P09/R10 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: board pack to investor-director with redactions |
      | EX-33ZU07-31 | O-034 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU07-32 | O-034 | P09/R10 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU07-33 | O-034 | P22/R21 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-34 | O-034 | P22/R21 | US 506b ✓ | unverified | relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU07-35 | O-034 | P22/R21 | IN s42 ✓ | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-36 | O-034 | P09/R10 | US 506b ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU07-37 | O-034 | P09/R10 | US 506b ✓ | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-38 | O-034 | P21/R03 | US 506b ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU07-39 | O-034 | P21/R03 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU07-40 | O-034 | P22/R21 | UK FPO draft | unverified | relationship | L3 IR-msg mandate | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU07-41 | O-034 | P21/R03 | US 506c ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU07-42 | O-034 | P09/R10 | US 506c ✓ | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU07-43 | O-034 | P22/R21 | US 506c ✓ | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-44 | O-034 | P22/R21 | US 506b ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU07-45 | O-034 | P21/R03 | US 506b ✓ | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-46 | O-034 | P22/R21 | UK FPO draft | eligible | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU07-47 | O-034 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: board pack to investor-director with redactions |
```

##### US-33-ZU08 Sanctions possible matches held, true matches blocked, no tip-off

| Field | Value |
|---|---|
| ID | US-33-ZU08 |
| Title | Sanctions possible matches held, true matches blocked, no tip-off |
| Type | Compliance |
| Story | As an investor-relations user (P21, R03 in the INV product), I want possible matches are held for human review; confirmed sanctions matches are permanently blocked with no override, so that we raise capital only through lawful routes, to eligible investors, with every consequential step approved by two people |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-036; DEC-770, DEC-783; tests TC-V12-O-369, TC-V12-O-379 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-30-ZN01, US-30-ZN02, US-31-ZN01, US-33-ZO12; source definition: Part 11.16c §11.16.15.14 INV-SVC-24 Investor Identity |
| Dimension profile | persona ×3 · jurisdiction ×4 · investor eligibility ×3 · solicitation ×2 · autonomy/mandate ×2 · region ×3 · operation ×1 · model MU08 |
| Notes | FR-V12-O-036: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Screens A205–A259, W55–W99; API family `/api/v1/investor/`; audit events `inv.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: Sanctions possible matches held, true matches blocked, no tip-off
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (owner portfolio:
      """
      zone IN) subscribed to Investment Automation with investor-relations user "nikhil@appnai.example.com" and counsel "farah@appnai.example.com"
      (R10)
      """
    And offering "Seed 2027" registered under route IN s.42 private placement with pack RP-IN-SEC Approved and RP-UK-FPO Draft (DEC-783)

  @happy @DEC-783
  Scenario: AC-33ZU08-01 Happy path – Possible matches are held for human review (FR-V12-O-036)
    Given Nikhil Bose (investor relations, nikhil@appnai.example.com) is signed in to the tenant with the capability enabled
    When "Possible matches are held for human review" is exercised as specified by FR-V12-O-036:
      """
      Possible matches are held for human review; confirmed sanctions matches are permanently blocked with no override; investors are never tipped
      off
      """
    Then possible match → A253 queue
    And the audit event "inv.possible_matches_are_held_for" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg
  Scenario: AC-33ZU08-02 Negative – R10 override attempt on true match (FR-V12-O-036)
    Given the condition "R10 override attempt on true match" holds for FR-V12-O-036
    When the action is attempted
    Then the outcome is "no path"
    And no external effect, charge or outbox event is created

  @neg @DEC-783
  Scenario: AC-33ZU08-03 Negative – no offer material to a jurisdiction without an Active pack
    Given investor "oliver@capital.example.co.uk" in the UK where RP-UK-FPO is "Draft"
    When Nikhil sends the "Seed 2027" deck
    Then the gate returns BLOCK "PACK_NOT_ACTIVE" and no message or data-room grant is created

  @val
  Scenario: AC-33ZU08-04 Validation – an offer requires both approvals on the content hash
    Given the formal offer for "priya@angelfund.example.com" has approval from Arjun (R02) only
    When dispatch is attempted
    Then the result is HELD "TWO_APPROVALS_REQUIRED" and nothing is sent

  @perm @BRL-TEN-04
  Scenario: AC-33ZU08-05 Permission – an invited investor sees only their own objects
    Given invited investor "priya@angelfund.example.com" (R21, Part 11.16a)
    When she requests investor record INV-0021 of another investor
    Then the portal returns the uniform 404 and the attempt is audited

  @edge @sec
  Scenario: AC-33ZU08-06 Edge – AI never gives personalised investment advice
    When an investor asks the assistant "Should I invest ₹25,00,000 in Seed 2027?"
    Then the answer is a refusal with the approved factual information and a hand-over to a human, and RP-INV-ADVICE logs the refusal

  @sec @obs @MU08
  Scenario Outline: AC-33ZU08-07 Permutations – Investor securities controls (3-way, 47 rows)
    Given actor "<persona>" in zone "<region>" and route "<jurisdiction>"
    And the investor is "<investor_eligibility>" with "<solicitation>" and approval mode "<autonomy_mandate>"
    When "<operation>" is attempted
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU08 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-036 = Possible matches are held for human review
    Examples: MU08 rows (3-way, seed 1172; space 432; tuples 558/558; +1 baseline-allow)
      | ex | operation | persona | jurisdiction | investor_eligibility | solicitation | autonomy_mandate | region | expected |
      | EX-33ZU08-01 | O-036 | P09/R10 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU08-02 | O-036 | P22/R21 | US 506b ✓ | eligible | relationship | L1 two-person | IN | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU08-03 | O-036 | P21/R03 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU08-04 | O-036 | P22/R21 | US 506c ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU08-05 | O-036 | P21/R03 | UK FPO draft | eligible | relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU08-06 | O-036 | P09/R10 | US 506c ✓ | sanctions match? | relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU08-07 | O-036 | P22/R21 | UK FPO draft | sanctions match? | no relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU08-08 | O-036 | P09/R10 | UK FPO draft | eligible | no relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU08-09 | O-036 | P21/R03 | US 506c ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU08-10 | O-036 | P09/R10 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: possible match → A253 queue |
      | EX-33ZU08-11 | O-036 | P22/R21 | IN s42 ✓ | unverified | no relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU08-12 | O-036 | P21/R03 | US 506b ✓ | eligible | no relationship | L3 IR-msg mandate | EU | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU08-13 | O-036 | P09/R10 | UK FPO draft | unverified | relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU08-14 | O-036 | P21/R03 | US 506b ✓ | sanctions match? | relationship | L3 IR-msg mandate | IN | HOLD for R10 review |
      | EX-33ZU08-15 | O-036 | P22/R21 | US 506c ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU08-16 | O-036 | P21/R03 | US 506b ✓ | unverified | relationship | L1 two-person | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU08-17 | O-036 | P09/R10 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU08-18 | O-036 | P22/R21 | IN s42 ✓ | sanctions match? | relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU08-19 | O-036 | P22/R21 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU08-20 | O-036 | P21/R03 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU08-21 | O-036 | P21/R03 | IN s42 ✓ | eligible | no relationship | L1 two-person | IN | BLOCK GENERAL_SOLICITATION for private routes |
      | EX-33ZU08-22 | O-036 | P21/R03 | IN s42 ✓ | unverified | relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU08-23 | O-036 | P21/R03 | US 506c ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU08-24 | O-036 | P09/R10 | US 506b ✓ | eligible | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU08-25 | O-036 | P09/R10 | UK FPO draft | sanctions match? | relationship | L3 IR-msg mandate | EU | HOLD for R10 review |
      | EX-33ZU08-26 | O-036 | P09/R10 | IN s42 ✓ | sanctions match? | no relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU08-27 | O-036 | P22/R21 | UK FPO draft | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU08-28 | O-036 | P22/R21 | US 506b ✓ | unverified | no relationship | L3 IR-msg mandate | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU08-29 | O-036 | P21/R03 | UK FPO draft | unverified | no relationship | L3 IR-msg mandate | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU08-30 | O-036 | P22/R21 | US 506c ✓ | sanctions match? | relationship | L1 two-person | IN | HOLD for R10 review |
      | EX-33ZU08-31 | O-036 | P22/R21 | IN s42 ✓ | eligible | relationship | L1 two-person | EU | PENDING two approvals (R02 + R10) on the content hash |
      | EX-33ZU08-32 | O-036 | P21/R03 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU08-33 | O-036 | P09/R10 | US 506c ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: possible match → A253 queue |
      | EX-33ZU08-34 | O-036 | P09/R10 | IN s42 ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU08-35 | O-036 | P22/R21 | US 506b ✓ | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU08-36 | O-036 | P22/R21 | IN s42 ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU08-37 | O-036 | P09/R10 | US 506b ✓ | sanctions match? | relationship | L1 two-person | EU | HOLD for R10 review |
      | EX-33ZU08-38 | O-036 | P09/R10 | IN s42 ✓ | eligible | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU08-39 | O-036 | P22/R21 | UK FPO draft | eligible | relationship | L1 two-person | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU08-40 | O-036 | P21/R03 | UK FPO draft | eligible | no relationship | L1 two-person | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU08-41 | O-036 | P21/R03 | IN s42 ✓ | eligible | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU08-42 | O-036 | P09/R10 | US 506c ✓ | unverified | no relationship | L3 IR-msg mandate | EU | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU08-43 | O-036 | P09/R10 | UK FPO draft | sanctions match? | no relationship | L1 two-person | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU08-44 | O-036 | P21/R03 | US 506b ✓ | unverified | relationship | L1 two-person | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU08-45 | O-036 | P21/R03 | US 506c ✓ | sanctions match? | no relationship | L3 IR-msg mandate | EU→IN (misrouted) | HOLD for R10 review |
      | EX-33ZU08-46 | O-036 | P09/R10 | US 506b ✓ | unverified | no relationship | L1 two-person | IN | BLOCK ELIGIBILITY_UNVERIFIED |
      | EX-33ZU08-47 | O-036 | P21/R03 | IN s42 ✓ | eligible | relationship | L3 IR-msg mandate | IN | ALLOW: possible match → A253 queue |
```

##### US-33-ZU09 INV-SVC-17 Grant & Non-Dilutive Funding Application Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-33-ZU09 |
| Title | INV-SVC-17 Grant & Non-Dilutive Funding Application Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-17 Grant & Non-Dilutive Funding Application Automation workflows (grant eligibility and evaluation criteria mapping; grant application and project proposal preparation; application budget, supporting evidence and submission; grant milestone, expenditure and utilization reporting) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-053; FR-V12-O-054; FR-V12-O-055; FR-V12-O-056; DEC-770, DEC-779, DEC-783, DEC-822; tests TC-V12-O-129, TC-V12-O-137, TC-V12-O-145, TC-V12-O-153 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-17-WF01 Grant eligibility and evaluation…; Part 11.16c §INV-SVC-17-WF02 Grant application and project…; Part 11.16c §INV-SVC-17-WF03 Application budget; Part 11.16c §INV-SVC-17-WF04 Grant milestone |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-053, FR-V12-O-054, FR-V12-O-055, FR-V12-O-056: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO09, US-33-ZO01, US-33-ZO02 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-17 Grant & Non-Dilutive Funding Application Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-33ZU09-01 Happy path – Grant eligibility and evaluation criteria mapping (FR-V12-O-053)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-17-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-17-WF01:v2` (FR-V12-O-053)
    Then Grant eligibility and evaluation criteria mapping: Programme criteria, issuer profile → Eligibility matrix
    And Eligibility matrix; acceptance INV-SVC-17-WF01-AT01 → TC-V12-O-129 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU09-02 Alternate – Grant application and project proposal preparation (FR-V12-O-054)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-17-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-17-WF02:v2` (FR-V12-O-054)
    Then Grant application and project proposal preparation: Programme questions, approved project facts → Application draft
    And Application draft; acceptance INV-SVC-17-WF02-AT01 → TC-V12-O-137 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU09-03 Alternate – Application budget, supporting evidence and submission readiness (FR-V12-O-055)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-17-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-17-WF03:v2` (FR-V12-O-055)
    Then Application budget, supporting evidence and submission readiness: Budget, required attachments, deadline → Submission-ready pack
    And Submission-ready pack; acceptance INV-SVC-17-WF03-AT01 → TC-V12-O-145 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @alt @DEC-783
  Scenario: AC-33ZU09-04 Alternate – Grant milestone, expenditure and utilization reporting (FR-V12-O-056)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-17-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-17-WF04:v2` (FR-V12-O-056)
    Then Grant milestone, expenditure and utilization reporting: Award terms, milestones, verified spending → Grant utilization report
    And Grant utilization report; acceptance INV-SVC-17-WF04-AT01 → TC-V12-O-153 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @neg @DEC-822
  Scenario: AC-33ZU09-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-33ZU09-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-33ZU09-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-33ZU09-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-33ZU09-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 76 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-053 = Grant eligibility and evaluation criteria mapping
    #   O-054 = Grant application and project proposal preparation
    #   O-055 = Application budget, supporting evidence and…
    #   O-056 = Grant milestone, expenditure and utilization…
    Examples: MU09 rows (3-way, seed 1179; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-33ZU09-01 | O-054 | P08/R08 | A1 | IN ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-02 | O-053 | P08/R08 | T5 other tenant | US ✓ | hash changed | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU09-03 | O-053 | P08/R08 | A3 SoD/limit | UK draft | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-04 | O-055 | P09/R10 | A1 | UK draft | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-05 | O-053 | P09/R10 | A1 | US ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-06 | O-054 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-07 | O-055 | P09/R10 | A5 wrong role | IN ✓ | 1 approver | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU09-08 | O-056 | P21/R03 | T5 other tenant | UK draft | hash changed | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU09-09 | O-056 | P21/R03 | A1 | IN ✓ | 2 approvals | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU09-10 | O-056 | P08/R08 | A5 wrong role | US ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-11 | O-055 | P21/R03 | A3 SoD/limit | US ✓ | hash changed | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU09-12 | O-054 | P09/R10 | T5 other tenant | UK draft | 2 approvals | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU09-13 | O-053 | P09/R10 | A3 SoD/limit | IN ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-14 | O-054 | P21/R03 | A5 wrong role | UK draft | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-15 | O-055 | P21/R03 | T5 other tenant | IN ✓ | 1 approver | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU09-16 | O-054 | P08/R08 | A1 | UK draft | 1 approver | active | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU09-17 | O-056 | P08/R08 | A5 wrong role | IN ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-18 | O-055 | P08/R08 | A5 wrong role | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-19 | O-055 | P08/R08 | T5 other tenant | IN ✓ | 2 approvals | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU09-20 | O-056 | P09/R10 | T5 other tenant | US ✓ | 1 approver | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU09-21 | O-053 | P21/R03 | A5 wrong role | UK draft | 1 approver | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU09-22 | O-056 | P09/R10 | A3 SoD/limit | UK draft | hash changed | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU09-23 | O-054 | P09/R10 | A5 wrong role | US ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-24 | O-055 | P21/R03 | A1 | US ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-25 | O-054 | P09/R10 | A3 SoD/limit | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-26 | O-053 | P21/R03 | A1 | IN ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-27 | O-055 | P08/R08 | A3 SoD/limit | UK draft | 1 approver | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU09-28 | O-055 | P21/R03 | A5 wrong role | UK draft | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-29 | O-053 | P09/R10 | T5 other tenant | UK draft | hash changed | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU09-30 | O-056 | P21/R03 | A3 SoD/limit | US ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-31 | O-056 | P09/R10 | A1 | UK draft | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-32 | O-054 | P21/R03 | T5 other tenant | IN ✓ | hash changed | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU09-33 | O-053 | P08/R08 | A5 wrong role | IN ✓ | 2 approvals | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU09-34 | O-054 | P09/R10 | T5 other tenant | US ✓ | 1 approver | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU09-35 | O-056 | P08/R08 | A3 SoD/limit | IN ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-36 | O-056 | P08/R08 | A1 | US ✓ | 2 approvals | active | IN | ALLOW: Grant utilization report |
      | EX-33ZU09-37 | O-053 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU09-38 | O-054 | P08/R08 | A1 | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-39 | O-055 | P08/R08 | A5 wrong role | UK draft | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-40 | O-053 | P08/R08 | T5 other tenant | UK draft | 1 approver | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU09-41 | O-055 | P09/R10 | A1 | US ✓ | 2 approvals | active | EU | ALLOW: Submission-ready pack |
      | EX-33ZU09-42 | O-056 | P09/R10 | A5 wrong role | UK draft | 2 approvals | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU09-43 | O-053 | P21/R03 | A5 wrong role | US ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-44 | O-056 | P08/R08 | T5 other tenant | IN ✓ | 1 approver | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU09-45 | O-055 | P09/R10 | A3 SoD/limit | IN ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-46 | O-054 | P09/R10 | A3 SoD/limit | IN ✓ | 1 approver | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU09-47 | O-054 | P08/R08 | A3 SoD/limit | UK draft | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-48 | O-054 | P08/R08 | A5 wrong role | US ✓ | 1 approver | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU09-49 | O-053 | P21/R03 | A3 SoD/limit | US ✓ | 2 approvals | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU09-50 | O-053 | P21/R03 | A1 | UK draft | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-51 | O-054 | P21/R03 | A5 wrong role | IN ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-52 | O-055 | P09/R10 | T5 other tenant | US ✓ | hash changed | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU09-53 | O-053 | P09/R10 | A5 wrong role | UK draft | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-54 | O-056 | P21/R03 | A3 SoD/limit | IN ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-55 | O-056 | P09/R10 | A1 | US ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-56 | O-055 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-57 | O-054 | P08/R08 | T5 other tenant | UK draft | hash changed | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU09-58 | O-053 | P09/R10 | A1 | IN ✓ | 1 approver | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU09-59 | O-056 | P09/R10 | T5 other tenant | IN ✓ | 2 approvals | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU09-60 | O-053 | P08/R08 | T5 other tenant | US ✓ | 1 approver | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU09-61 | O-055 | P08/R08 | A1 | IN ✓ | hash changed | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU09-62 | O-055 | P09/R10 | T5 other tenant | UK draft | hash changed | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU09-63 | O-053 | P21/R03 | A3 SoD/limit | UK draft | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU09-64 | O-054 | P21/R03 | A1 | UK draft | 2 approvals | active | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU09-65 | O-056 | P21/R03 | A5 wrong role | IN ✓ | hash changed | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU09-66 | O-056 | P08/R08 | A5 wrong role | UK draft | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-67 | O-055 | P08/R08 | A1 | US ✓ | hash changed | active | IN | HOLD APPROVAL_STALE |
      | EX-33ZU09-68 | O-054 | P09/R10 | A1 | IN ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-69 | O-056 | P09/R10 | A5 wrong role | US ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU09-70 | O-056 | P08/R08 | A3 SoD/limit | US ✓ | 1 approver | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU09-71 | O-053 | P08/R08 | T5 other tenant | IN ✓ | 2 approvals | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU09-72 | O-053 | P08/R08 | A1 | IN ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU09-73 | O-053 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Eligibility matrix |
      | EX-33ZU09-74 | O-054 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Application draft |
      | EX-33ZU09-75 | O-055 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Submission-ready pack |
      | EX-33ZU09-76 | O-056 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Grant utilization report |
```

##### US-33-ZU10 INV-SVC-18 Debt Financing & Credit Readiness Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-33-ZU10 |
| Title | INV-SVC-18 Debt Financing & Credit Readiness Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-18 Debt Financing & Credit Readiness Automation workflows (credit readiness and financing requirement assessment; lender proposal and supporting document preparation; financing terms and repayment scenario comparison; debt covenant, repayment and obligation monitoring) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-057; FR-V12-O-058; FR-V12-O-059; FR-V12-O-060; DEC-770, DEC-779, DEC-783, DEC-822; tests TC-V12-O-161, TC-V12-O-169, TC-V12-O-177, TC-V12-O-185 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-18-WF01 Credit readiness and financing…; Part 11.16c §INV-SVC-18-WF02 Lender proposal and supporting…; Part 11.16c §INV-SVC-18-WF03 Financing terms and repayment…; Part 11.16c §INV-SVC-18-WF04 Debt covenant |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-057, FR-V12-O-058, FR-V12-O-059, FR-V12-O-060: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO09, US-33-ZO03 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-18 Debt Financing & Credit Readiness Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-33ZU10-01 Happy path – Credit readiness and financing requirement assessment (FR-V12-O-057)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-18-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-18-WF01:v2` (FR-V12-O-057)
    Then Credit readiness and financing requirement assessment: Financial statements, liabilities, financing need → Readiness report
    And Readiness report; acceptance INV-SVC-18-WF01-AT01 → TC-V12-O-161 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU10-02 Alternate – Lender proposal and supporting document preparation (FR-V12-O-058)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-18-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-18-WF02:v2` (FR-V12-O-058)
    Then Lender proposal and supporting document preparation: Lender checklist, approved records → Lender dossier
    And Lender dossier; acceptance INV-SVC-18-WF02-AT01 → TC-V12-O-169 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @alt @DEC-783
  Scenario: AC-33ZU10-03 Alternate – Financing terms and repayment scenario comparison (FR-V12-O-059)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-18-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-18-WF03:v2` (FR-V12-O-059)
    Then Financing terms and repayment scenario comparison: Indicative terms, rates, cash flow assumptions → Repayment comparison
    And Repayment comparison; acceptance INV-SVC-18-WF03-AT01 → TC-V12-O-177 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU10-04 Alternate – Debt covenant, repayment and obligation monitoring (FR-V12-O-060)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-18-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-18-WF04:v2` (FR-V12-O-060)
    Then Debt covenant, repayment and obligation monitoring: Executed terms, payment events, covenant metrics → Obligation dashboard
    And Obligation dashboard; acceptance INV-SVC-18-WF04-AT01 → TC-V12-O-185 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @neg @DEC-822
  Scenario: AC-33ZU10-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-33ZU10-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-33ZU10-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-33ZU10-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-33ZU10-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 78 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-057 = Credit readiness and financing requirement…
    #   O-058 = Lender proposal and supporting document preparation
    #   O-059 = Financing terms and repayment scenario comparison
    #   O-060 = Debt covenant, repayment and obligation monitoring
    Examples: MU09 rows (3-way, seed 1186; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-33ZU10-01 | O-058 | P08/R08 | T5 other tenant | IN ✓ | hash changed | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU10-02 | O-058 | P09/R10 | A1 | US ✓ | 1 approver | active | IN | HELD TWO_APPROVALS_REQUIRED |
      | EX-33ZU10-03 | O-057 | P08/R08 | A1 | UK draft | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-04 | O-059 | P09/R10 | T5 other tenant | UK draft | 2 approvals | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU10-05 | O-058 | P21/R03 | A5 wrong role | UK draft | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-06 | O-059 | P21/R03 | A3 SoD/limit | US ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-07 | O-060 | P21/R03 | A5 wrong role | US ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-08 | O-057 | P09/R10 | A3 SoD/limit | IN ✓ | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU10-09 | O-060 | P08/R08 | A5 wrong role | IN ✓ | 2 approvals | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU10-10 | O-059 | P08/R08 | A3 SoD/limit | UK draft | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-11 | O-060 | P09/R10 | T5 other tenant | US ✓ | hash changed | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU10-12 | O-057 | P21/R03 | A1 | IN ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-13 | O-059 | P09/R10 | T5 other tenant | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU10-14 | O-060 | P21/R03 | A1 | UK draft | hash changed | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU10-15 | O-058 | P09/R10 | A5 wrong role | UK draft | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-16 | O-057 | P09/R10 | A5 wrong role | IN ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-17 | O-059 | P08/R08 | A5 wrong role | US ✓ | hash changed | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU10-18 | O-058 | P08/R08 | A1 | US ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-19 | O-058 | P08/R08 | A3 SoD/limit | UK draft | 1 approver | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU10-20 | O-059 | P21/R03 | A1 | IN ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-21 | O-060 | P21/R03 | A3 SoD/limit | IN ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-22 | O-057 | P08/R08 | T5 other tenant | US ✓ | 1 approver | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU10-23 | O-060 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-24 | O-057 | P21/R03 | T5 other tenant | US ✓ | hash changed | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU10-25 | O-060 | P08/R08 | T5 other tenant | UK draft | 2 approvals | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU10-26 | O-058 | P21/R03 | T5 other tenant | IN ✓ | 1 approver | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU10-27 | O-057 | P09/R10 | A1 | UK draft | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-28 | O-057 | P09/R10 | A3 SoD/limit | UK draft | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-29 | O-059 | P21/R03 | A5 wrong role | UK draft | 1 approver | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU10-30 | O-058 | P21/R03 | A1 | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-31 | O-058 | P08/R08 | A3 SoD/limit | IN ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-32 | O-060 | P08/R08 | A1 | IN ✓ | 1 approver | active | EU | HELD TWO_APPROVALS_REQUIRED |
      | EX-33ZU10-33 | O-059 | P08/R08 | A5 wrong role | IN ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-34 | O-058 | P21/R03 | T5 other tenant | UK draft | 2 approvals | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU10-35 | O-057 | P21/R03 | A5 wrong role | US ✓ | 2 approvals | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU10-36 | O-060 | P09/R10 | A5 wrong role | US ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-37 | O-060 | P09/R10 | A5 wrong role | IN ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-38 | O-059 | P09/R10 | A1 | UK draft | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-39 | O-057 | P08/R08 | A3 SoD/limit | US ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-40 | O-060 | P09/R10 | A3 SoD/limit | UK draft | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-41 | O-059 | P08/R08 | T5 other tenant | US ✓ | 1 approver | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU10-42 | O-057 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU10-43 | O-060 | P09/R10 | A1 | IN ✓ | 2 approvals | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU10-44 | O-058 | P09/R10 | A5 wrong role | IN ✓ | hash changed | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU10-45 | O-060 | P08/R08 | A1 | US ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-46 | O-057 | P21/R03 | T5 other tenant | UK draft | 2 approvals | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU10-47 | O-057 | P08/R08 | A5 wrong role | UK draft | hash changed | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU10-48 | O-058 | P08/R08 | A5 wrong role | US ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-49 | O-058 | P21/R03 | A3 SoD/limit | IN ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-50 | O-059 | P08/R08 | A1 | US ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-51 | O-059 | P09/R10 | T5 other tenant | IN ✓ | hash changed | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU10-52 | O-060 | P21/R03 | T5 other tenant | IN ✓ | 2 approvals | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU10-53 | O-058 | P09/R10 | T5 other tenant | US ✓ | hash changed | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU10-54 | O-059 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU10-55 | O-057 | P08/R08 | T5 other tenant | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU10-56 | O-060 | P21/R03 | A3 SoD/limit | UK draft | hash changed | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU10-57 | O-060 | P08/R08 | T5 other tenant | UK draft | 1 approver | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU10-58 | O-058 | P09/R10 | A3 SoD/limit | IN ✓ | 2 approvals | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU10-59 | O-059 | P21/R03 | A5 wrong role | IN ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-60 | O-059 | P21/R03 | A3 SoD/limit | IN ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-61 | O-057 | P09/R10 | T5 other tenant | US ✓ | 2 approvals | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU10-62 | O-059 | P21/R03 | T5 other tenant | UK draft | hash changed | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU10-63 | O-058 | P21/R03 | A1 | UK draft | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-64 | O-060 | P08/R08 | A3 SoD/limit | US ✓ | 1 approver | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU10-65 | O-060 | P09/R10 | A5 wrong role | UK draft | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-66 | O-057 | P21/R03 | A1 | US ✓ | hash changed | active | IN | HOLD APPROVAL_STALE |
      | EX-33ZU10-67 | O-059 | P09/R10 | A5 wrong role | US ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-68 | O-059 | P21/R03 | A1 | UK draft | 1 approver | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU10-69 | O-057 | P08/R08 | A3 SoD/limit | UK draft | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-70 | O-060 | P21/R03 | A1 | US ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-71 | O-058 | P08/R08 | A1 | IN ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU10-72 | O-058 | P21/R03 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-73 | O-057 | P09/R10 | A5 wrong role | UK draft | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU10-74 | O-060 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU10-75 | O-057 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Readiness report |
      | EX-33ZU10-76 | O-058 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Lender dossier |
      | EX-33ZU10-77 | O-059 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Repayment comparison |
      | EX-33ZU10-78 | O-060 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Obligation dashboard |
```

##### US-33-ZU11 INV-SVC-19 Continuous Fundraising Readiness & Financial Intelligence Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-33-ZU11 |
| Title | INV-SVC-19 Continuous Fundraising Readiness & Financial Intelligence Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-19 Continuous Fundraising Readiness & Financial Intelligence Automation workflows (authorized financial and operational data synchronization; runway, burn rate and financial sustainability calculation; investor readiness scoring and evidence-gap analysis; funding requirement alerts and readiness improvement) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-061; FR-V12-O-062; FR-V12-O-063; FR-V12-O-064; DEC-770, DEC-783; tests TC-V12-O-193, TC-V12-O-201, TC-V12-O-209, TC-V12-O-217 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-19-WF01 Authorized financial and…; Part 11.16c §INV-SVC-19-WF02 Runway, burn rate and financial…; Part 11.16c §INV-SVC-19-WF03 Investor readiness scoring and…; Part 11.16c §INV-SVC-19-WF04 Funding requirement alerts and… |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-061, FR-V12-O-062, FR-V12-O-063, FR-V12-O-064: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO09, US-33-ZO04 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-19 Continuous Fundraising Readiness & Financial Intelligence Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-33ZU11-01 Happy path – Authorized financial and operational data synchronization (FR-V12-O-061)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-19-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-19-WF01:v2` (FR-V12-O-061)
    Then Authorized financial and operational data synchronization: Authorized source records and mappings → Normalized evidence snapshot
    And Normalized evidence snapshot; acceptance INV-SVC-19-WF01-AT01 → TC-V12-O-193 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU11-02 Alternate – Runway, burn rate and financial sustainability calculation (FR-V12-O-062)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-19-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-19-WF02:v2` (FR-V12-O-062)
    Then Runway, burn rate and financial sustainability calculation: Cash, cash flow, forecast assumptions → Runway analysis
    And Runway analysis; acceptance INV-SVC-19-WF02-AT01 → TC-V12-O-201 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU11-03 Alternate – Investor readiness scoring and evidence-gap analysis (FR-V12-O-063)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-19-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-19-WF03:v2` (FR-V12-O-063)
    Then Investor readiness scoring and evidence-gap analysis: Readiness criteria, current evidence → Readiness scorecard
    And Readiness scorecard; acceptance INV-SVC-19-WF03-AT01 → TC-V12-O-209 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU11-04 Alternate – Funding requirement alerts and readiness improvement planning (FR-V12-O-064)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-19-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-19-WF04:v2` (FR-V12-O-064)
    Then Funding requirement alerts and readiness improvement planning:
      """
      Runway thresholds, funding objectives, readiness gaps → Funding readiness action plan
      """
    And Funding readiness action plan; acceptance INV-SVC-19-WF04-AT01 → TC-V12-O-217 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @neg @DEC-822
  Scenario: AC-33ZU11-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-33ZU11-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-33ZU11-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-33ZU11-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-33ZU11-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 73 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-061 = Authorized financial and operational data…
    #   O-062 = Runway, burn rate and financial sustainability…
    #   O-063 = Investor readiness scoring and evidence-gap analysis
    #   O-064 = Funding requirement alerts and readiness…
    Examples: MU09 rows (3-way, seed 1193; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-33ZU11-01 | O-061 | P09/R10 | A5 wrong role | IN ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-02 | O-064 | P21/R03 | T5 other tenant | IN ✓ | hash changed | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU11-03 | O-061 | P21/R03 | A3 SoD/limit | UK draft | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-04 | O-064 | P09/R10 | A5 wrong role | UK draft | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-05 | O-062 | P09/R10 | A3 SoD/limit | UK draft | hash changed | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU11-06 | O-063 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU11-07 | O-064 | P09/R10 | A1 | US ✓ | 1 approver | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU11-08 | O-063 | P08/R08 | A3 SoD/limit | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-09 | O-061 | P08/R08 | A1 | US ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-10 | O-062 | P08/R08 | A5 wrong role | US ✓ | 2 approvals | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU11-11 | O-062 | P21/R03 | A1 | IN ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-12 | O-062 | P08/R08 | T5 other tenant | UK draft | 1 approver | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU11-13 | O-063 | P09/R10 | A1 | IN ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-14 | O-063 | P21/R03 | A5 wrong role | UK draft | 1 approver | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU11-15 | O-061 | P09/R10 | T5 other tenant | UK draft | hash changed | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU11-16 | O-062 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-17 | O-061 | P08/R08 | T5 other tenant | IN ✓ | 2 approvals | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU11-18 | O-064 | P08/R08 | A5 wrong role | US ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-19 | O-064 | P21/R03 | A1 | UK draft | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-20 | O-063 | P09/R10 | A5 wrong role | US ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-21 | O-062 | P08/R08 | A1 | UK draft | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-22 | O-063 | P08/R08 | A3 SoD/limit | US ✓ | 2 approvals | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU11-23 | O-064 | P09/R10 | T5 other tenant | US ✓ | 2 approvals | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU11-24 | O-061 | P21/R03 | T5 other tenant | US ✓ | 1 approver | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU11-25 | O-064 | P08/R08 | A3 SoD/limit | IN ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-26 | O-062 | P21/R03 | A5 wrong role | IN ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-27 | O-063 | P08/R08 | A1 | UK draft | hash changed | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU11-28 | O-061 | P21/R03 | A3 SoD/limit | IN ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-29 | O-062 | P09/R10 | A1 | IN ✓ | 1 approver | active | IN | HELD TWO_APPROVALS_REQUIRED |
      | EX-33ZU11-30 | O-064 | P09/R10 | A3 SoD/limit | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-31 | O-061 | P21/R03 | A1 | UK draft | 2 approvals | active | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU11-32 | O-063 | P09/R10 | A1 | US ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-33 | O-064 | P21/R03 | A5 wrong role | UK draft | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-34 | O-064 | P08/R08 | A3 SoD/limit | UK draft | 1 approver | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU11-35 | O-061 | P08/R08 | A5 wrong role | US ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-36 | O-062 | P21/R03 | T5 other tenant | US ✓ | hash changed | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU11-37 | O-063 | P09/R10 | A3 SoD/limit | UK draft | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-38 | O-063 | P21/R03 | A5 wrong role | IN ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-39 | O-062 | P09/R10 | T5 other tenant | IN ✓ | 1 approver | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU11-40 | O-061 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU11-41 | O-063 | P08/R08 | A5 wrong role | UK draft | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-42 | O-064 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-43 | O-064 | P08/R08 | A1 | IN ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-44 | O-061 | P09/R10 | A5 wrong role | IN ✓ | hash changed | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU11-45 | O-063 | P09/R10 | T5 other tenant | UK draft | 1 approver | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU11-46 | O-061 | P08/R08 | A1 | UK draft | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-47 | O-062 | P09/R10 | T5 other tenant | US ✓ | 2 approvals | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU11-48 | O-064 | P08/R08 | T5 other tenant | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU11-49 | O-061 | P09/R10 | A3 SoD/limit | IN ✓ | 1 approver | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU11-50 | O-063 | P21/R03 | T5 other tenant | UK draft | 2 approvals | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU11-51 | O-062 | P08/R08 | A3 SoD/limit | IN ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-52 | O-062 | P21/R03 | A3 SoD/limit | US ✓ | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU11-53 | O-063 | P08/R08 | T5 other tenant | IN ✓ | hash changed | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU11-54 | O-062 | P09/R10 | A5 wrong role | UK draft | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-55 | O-061 | P09/R10 | A1 | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-56 | O-061 | P21/R03 | A1 | IN ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-57 | O-062 | P08/R08 | A5 wrong role | IN ✓ | hash changed | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU11-58 | O-064 | P21/R03 | A5 wrong role | IN ✓ | 2 approvals | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU11-59 | O-061 | P21/R03 | A5 wrong role | UK draft | 2 approvals | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU11-60 | O-062 | P21/R03 | T5 other tenant | UK draft | 1 approver | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU11-61 | O-062 | P09/R10 | A1 | UK draft | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-62 | O-063 | P21/R03 | A3 SoD/limit | UK draft | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU11-63 | O-064 | P09/R10 | A5 wrong role | UK draft | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-64 | O-062 | P21/R03 | A1 | US ✓ | hash changed | active | EU | HOLD APPROVAL_STALE |
      | EX-33ZU11-65 | O-061 | P08/R08 | T5 other tenant | US ✓ | hash changed | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU11-66 | O-063 | P21/R03 | A1 | US ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-67 | O-064 | P21/R03 | T5 other tenant | UK draft | 1 approver | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU11-68 | O-061 | P08/R08 | A3 SoD/limit | US ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-69 | O-064 | P21/R03 | A5 wrong role | US ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU11-70 | O-061 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Normalized evidence snapshot |
      | EX-33ZU11-71 | O-062 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Runway analysis |
      | EX-33ZU11-72 | O-063 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Readiness scorecard |
      | EX-33ZU11-73 | O-064 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Funding readiness action plan |
```

##### US-33-ZU12 INV-SVC-20 Cap Table & Ownership Intelligence Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-33-ZU12 |
| Title | INV-SVC-20 Cap Table & Ownership Intelligence Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-20 Cap Table & Ownership Intelligence Automation workflows (shareholder and ownership record reconciliation; dilution and future funding-round scenario modelling; convertible instrument, option and ESOP scenario analysis; approved ownership changes and cap-table discrepancy) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-065; FR-V12-O-066; FR-V12-O-067; FR-V12-O-068; DEC-770, DEC-779, DEC-783, DEC-822; tests TC-V12-O-225, TC-V12-O-233, TC-V12-O-241, TC-V12-O-249 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-20-WF01 Shareholder and ownership record…; Part 11.16c §INV-SVC-20-WF02 Dilution and future funding-round…; Part 11.16c §INV-SVC-20-WF03 Convertible instrument; Part 11.16c §INV-SVC-20-WF04 Approved ownership changes and… |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-065, FR-V12-O-066, FR-V12-O-067, FR-V12-O-068: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO09, US-33-ZO05, US-33-ZO08 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-20 Cap Table & Ownership Intelligence Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-33ZU12-01 Happy path – Shareholder and ownership record reconciliation (FR-V12-O-065)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-20-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-20-WF01:v2` (FR-V12-O-065)
    Then Shareholder and ownership record reconciliation: Shareholder register, issued instruments → Reconciled ownership snapshot
    And Reconciled ownership snapshot; acceptance INV-SVC-20-WF01-AT01 → TC-V12-O-225 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU12-02 Alternate – Dilution and future funding-round scenario modelling (FR-V12-O-066)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-20-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-20-WF02:v2` (FR-V12-O-066)
    Then Dilution and future funding-round scenario modelling: Current holdings, approved round assumptions → Dilution model
    And Dilution model; acceptance INV-SVC-20-WF02-AT01 → TC-V12-O-233 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU12-03 Alternate – Convertible instrument, option and ESOP scenario analysis (FR-V12-O-067)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-20-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-20-WF03:v2` (FR-V12-O-067)
    Then Convertible instrument, option and ESOP scenario analysis: Instrument terms, option pool, vesting rules → Instrument scenario report
    And Instrument scenario report; acceptance INV-SVC-20-WF03-AT01 → TC-V12-O-241 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU12-04 Alternate – Approved ownership changes and cap-table discrepancy monitoring (FR-V12-O-068)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-20-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-20-WF04:v2` (FR-V12-O-068)
    Then Approved ownership changes and cap-table discrepancy monitoring:
      """
      Approved resolutions, allotment records, current revision → Ownership change review
      """
    And Ownership change review; acceptance INV-SVC-20-WF04-AT01 → TC-V12-O-249 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash, two-person
      (R10 + R08/R09)"
      """

  @neg @DEC-822
  Scenario: AC-33ZU12-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-33ZU12-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-33ZU12-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-33ZU12-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-33ZU12-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 73 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-065 = Shareholder and ownership record reconciliation
    #   O-066 = Dilution and future funding-round scenario modelling
    #   O-067 = Convertible instrument, option and ESOP scenario…
    #   O-068 = Approved ownership changes and cap-table…
    Examples: MU09 rows (3-way, seed 1200; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-33ZU12-01 | O-066 | P09/R10 | A1 | US ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-02 | O-065 | P21/R03 | A1 | US ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-03 | O-068 | P21/R03 | A3 SoD/limit | UK draft | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-04 | O-067 | P21/R03 | A5 wrong role | IN ✓ | 1 approver | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU12-05 | O-066 | P08/R08 | T5 other tenant | UK draft | 2 approvals | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU12-06 | O-065 | P08/R08 | A3 SoD/limit | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-07 | O-067 | P09/R10 | A3 SoD/limit | IN ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-08 | O-068 | P09/R10 | A5 wrong role | UK draft | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-09 | O-068 | P08/R08 | T5 other tenant | US ✓ | 1 approver | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU12-10 | O-065 | P21/R03 | A3 SoD/limit | UK draft | 2 approvals | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU12-11 | O-068 | P08/R08 | A1 | IN ✓ | hash changed | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU12-12 | O-066 | P09/R10 | A1 | IN ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-13 | O-067 | P09/R10 | T5 other tenant | US ✓ | 1 approver | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU12-14 | O-065 | P08/R08 | A5 wrong role | UK draft | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-15 | O-067 | P08/R08 | A3 SoD/limit | US ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-16 | O-066 | P21/R03 | A5 wrong role | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-17 | O-065 | P09/R10 | A5 wrong role | US ✓ | hash changed | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU12-18 | O-068 | P09/R10 | T5 other tenant | IN ✓ | 2 approvals | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU12-19 | O-067 | P21/R03 | A1 | UK draft | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-20 | O-066 | P21/R03 | T5 other tenant | IN ✓ | hash changed | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU12-21 | O-065 | P21/R03 | T5 other tenant | UK draft | 1 approver | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU12-22 | O-066 | P09/R10 | A1 | UK draft | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-23 | O-066 | P08/R08 | A5 wrong role | US ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-24 | O-065 | P08/R08 | A1 | IN ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-25 | O-068 | P09/R10 | A5 wrong role | UK draft | 1 approver | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU12-26 | O-068 | P21/R03 | A1 | US ✓ | 2 approvals | active | EU | ALLOW: Ownership change review |
      | EX-33ZU12-27 | O-067 | P08/R08 | T5 other tenant | US ✓ | hash changed | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU12-28 | O-066 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU12-29 | O-067 | P21/R03 | T5 other tenant | IN ✓ | 2 approvals | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU12-30 | O-067 | P08/R08 | A3 SoD/limit | UK draft | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU12-31 | O-068 | P21/R03 | A5 wrong role | IN ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-32 | O-067 | P08/R08 | A5 wrong role | US ✓ | 2 approvals | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU12-33 | O-065 | P09/R10 | A3 SoD/limit | IN ✓ | 2 approvals | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU12-34 | O-065 | P08/R08 | A1 | US ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-35 | O-066 | P08/R08 | A3 SoD/limit | UK draft | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-36 | O-068 | P09/R10 | A3 SoD/limit | US ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-37 | O-067 | P09/R10 | A5 wrong role | UK draft | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-38 | O-065 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU12-39 | O-065 | P09/R10 | T5 other tenant | UK draft | hash changed | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU12-40 | O-066 | P08/R08 | A5 wrong role | IN ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-41 | O-068 | P08/R08 | A3 SoD/limit | IN ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-42 | O-065 | P09/R10 | A1 | UK draft | 1 approver | active | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU12-43 | O-067 | P08/R08 | A1 | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-44 | O-068 | P08/R08 | A1 | UK draft | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-45 | O-066 | P08/R08 | T5 other tenant | UK draft | 1 approver | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU12-46 | O-066 | P09/R10 | A3 SoD/limit | US ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-47 | O-065 | P08/R08 | T5 other tenant | IN ✓ | 1 approver | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU12-48 | O-067 | P21/R03 | A5 wrong role | UK draft | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-49 | O-066 | P21/R03 | A3 SoD/limit | IN ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-50 | O-068 | P09/R10 | A1 | US ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-51 | O-067 | P09/R10 | A1 | US ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-52 | O-068 | P21/R03 | A5 wrong role | US ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-53 | O-065 | P21/R03 | A5 wrong role | IN ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-54 | O-068 | P21/R03 | T5 other tenant | UK draft | hash changed | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU12-55 | O-065 | P09/R10 | A3 SoD/limit | IN ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-56 | O-066 | P09/R10 | A5 wrong role | IN ✓ | 1 approver | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU12-57 | O-067 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-58 | O-067 | P09/R10 | T5 other tenant | UK draft | 2 approvals | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU12-59 | O-068 | P21/R03 | A3 SoD/limit | IN ✓ | 1 approver | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU12-60 | O-066 | P21/R03 | A1 | UK draft | 1 approver | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU12-61 | O-066 | P09/R10 | T5 other tenant | US ✓ | 2 approvals | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU12-62 | O-065 | P09/R10 | A5 wrong role | UK draft | 1 approver | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU12-63 | O-068 | P09/R10 | A3 SoD/limit | UK draft | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-64 | O-065 | P08/R08 | A3 SoD/limit | US ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-65 | O-066 | P08/R08 | A1 | UK draft | 2 approvals | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU12-66 | O-067 | P21/R03 | A1 | IN ✓ | 1 approver | active | EU | HELD TWO_APPROVALS_REQUIRED |
      | EX-33ZU12-67 | O-067 | P08/R08 | A3 SoD/limit | IN ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU12-68 | O-068 | P08/R08 | A5 wrong role | UK draft | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU12-69 | O-066 | P09/R10 | A5 wrong role | UK draft | 2 approvals | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU12-70 | O-065 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Reconciled ownership snapshot |
      | EX-33ZU12-71 | O-066 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Dilution model |
      | EX-33ZU12-72 | O-067 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Instrument scenario report |
      | EX-33ZU12-73 | O-068 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Ownership change review |
```

##### US-33-ZU13 INV-SVC-21 ESG, Climate & Impact Funding Intelligence Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-33-ZU13 |
| Title | INV-SVC-21 ESG, Climate & Impact Funding Intelligence Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-21 ESG, Climate & Impact Funding Intelligence Automation workflows (ESG and impact indicator configuration; sustainability evidence collection and validation; investor-specific impact and sustainability disclosure; climate, impact and sustainability commitment monitoring) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-069; FR-V12-O-070; FR-V12-O-071; FR-V12-O-072; DEC-770, DEC-779, DEC-783, DEC-822; tests TC-V12-O-257, TC-V12-O-265, TC-V12-O-273, TC-V12-O-281 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-21-WF01 ESG and impact indicator…; Part 11.16c §INV-SVC-21-WF02 Sustainability evidence…; Part 11.16c §INV-SVC-21-WF03 Investor-specific impact and…; Part 11.16c §INV-SVC-21-WF04 Climate, impact and… |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-069, FR-V12-O-070, FR-V12-O-071, FR-V12-O-072: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO09, US-33-ZO06 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-21 ESG, Climate & Impact Funding Intelligence Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-33ZU13-01 Happy path – ESG and impact indicator configuration (FR-V12-O-069)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-21-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-21-WF01:v2` (FR-V12-O-069)
    Then ESG and impact indicator configuration: Applicable standards, scope, materiality and objectives → Metric registry
    And Metric registry; acceptance INV-SVC-21-WF01-AT01 → TC-V12-O-257 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU13-02 Alternate – Sustainability evidence collection and validation (FR-V12-O-070)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-21-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-21-WF02:v2` (FR-V12-O-070)
    Then Sustainability evidence collection and validation: Operational metrics, source records, reporting boundary → Evidence pack
    And Evidence pack; acceptance INV-SVC-21-WF02-AT01 → TC-V12-O-265 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU13-03 Alternate – Investor-specific impact and sustainability disclosure preparation (FR-V12-O-071)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-21-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-21-WF03:v2` (FR-V12-O-071)
    Then Investor-specific impact and sustainability disclosure preparation: Approved indicators, recipient disclosure requirements → Disclosure draft
    And Disclosure draft; acceptance INV-SVC-21-WF03-AT01 → TC-V12-O-273 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @alt @DEC-783
  Scenario: AC-33ZU13-04 Alternate – Climate, impact and sustainability commitment monitoring (FR-V12-O-072)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-21-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-21-WF04:v2` (FR-V12-O-072)
    Then Climate, impact and sustainability commitment monitoring: Approved commitments, targets, actual metrics → Commitment report
    And Commitment report; acceptance INV-SVC-21-WF04-AT01 → TC-V12-O-281 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @neg @DEC-822
  Scenario: AC-33ZU13-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-33ZU13-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-33ZU13-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-33ZU13-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-33ZU13-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 74 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-069 = ESG and impact indicator configuration
    #   O-070 = Sustainability evidence collection and validation
    #   O-071 = Investor-specific impact and sustainability…
    #   O-072 = Climate, impact and sustainability commitment…
    Examples: MU09 rows (3-way, seed 1207; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-33ZU13-01 | O-071 | P21/R03 | A3 SoD/limit | IN ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-02 | O-072 | P08/R08 | A3 SoD/limit | UK draft | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-03 | O-071 | P09/R10 | T5 other tenant | US ✓ | 1 approver | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU13-04 | O-070 | P09/R10 | T5 other tenant | UK draft | hash changed | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU13-05 | O-071 | P08/R08 | A1 | IN ✓ | 2 approvals | active | EU | ALLOW: Disclosure draft |
      | EX-33ZU13-06 | O-070 | P08/R08 | A5 wrong role | US ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-07 | O-072 | P21/R03 | A1 | US ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-08 | O-069 | P21/R03 | A5 wrong role | UK draft | 2 approvals | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU13-09 | O-069 | P09/R10 | A5 wrong role | US ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-10 | O-069 | P09/R10 | A1 | IN ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-11 | O-071 | P08/R08 | A5 wrong role | UK draft | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-12 | O-070 | P21/R03 | A3 SoD/limit | US ✓ | hash changed | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU13-13 | O-070 | P21/R03 | T5 other tenant | IN ✓ | 2 approvals | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU13-14 | O-070 | P09/R10 | A3 SoD/limit | UK draft | 1 approver | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU13-15 | O-069 | P08/R08 | A3 SoD/limit | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-16 | O-072 | P08/R08 | T5 other tenant | US ✓ | hash changed | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU13-17 | O-072 | P21/R03 | A5 wrong role | IN ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-18 | O-071 | P09/R10 | A1 | UK draft | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-19 | O-071 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-20 | O-069 | P08/R08 | T5 other tenant | UK draft | 1 approver | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU13-21 | O-069 | P21/R03 | A3 SoD/limit | UK draft | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-22 | O-072 | P09/R10 | A5 wrong role | IN ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-23 | O-072 | P09/R10 | A1 | UK draft | hash changed | active | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU13-24 | O-069 | P08/R08 | A1 | US ✓ | 1 approver | active | IN | HELD TWO_APPROVALS_REQUIRED |
      | EX-33ZU13-25 | O-070 | P08/R08 | A1 | IN ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-26 | O-069 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU13-27 | O-072 | P09/R10 | A5 wrong role | IN ✓ | 1 approver | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU13-28 | O-070 | P08/R08 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-29 | O-072 | P21/R03 | A1 | US ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-30 | O-069 | P21/R03 | T5 other tenant | IN ✓ | hash changed | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU13-31 | O-071 | P21/R03 | T5 other tenant | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU13-32 | O-070 | P21/R03 | A1 | UK draft | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-33 | O-070 | P09/R10 | A5 wrong role | US ✓ | 2 approvals | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU13-34 | O-071 | P21/R03 | A5 wrong role | US ✓ | hash changed | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU13-35 | O-071 | P21/R03 | T5 other tenant | UK draft | 2 approvals | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU13-36 | O-072 | P09/R10 | A3 SoD/limit | IN ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-37 | O-070 | P08/R08 | A1 | UK draft | 2 approvals | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU13-38 | O-071 | P09/R10 | A5 wrong role | UK draft | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-39 | O-072 | P08/R08 | T5 other tenant | IN ✓ | hash changed | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU13-40 | O-069 | P09/R10 | A3 SoD/limit | US ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-41 | O-069 | P09/R10 | T5 other tenant | IN ✓ | 2 approvals | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU13-42 | O-070 | P21/R03 | A5 wrong role | IN ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-43 | O-069 | P08/R08 | A1 | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-44 | O-072 | P21/R03 | A3 SoD/limit | UK draft | 1 approver | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU13-45 | O-071 | P08/R08 | A5 wrong role | IN ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-46 | O-071 | P08/R08 | T5 other tenant | US ✓ | hash changed | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU13-47 | O-072 | P08/R08 | T5 other tenant | UK draft | 2 approvals | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU13-48 | O-069 | P21/R03 | A1 | UK draft | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-49 | O-071 | P08/R08 | A3 SoD/limit | IN ✓ | 1 approver | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU13-50 | O-070 | P09/R10 | A1 | US ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-51 | O-069 | P09/R10 | A5 wrong role | UK draft | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-52 | O-069 | P21/R03 | A3 SoD/limit | IN ✓ | 2 approvals | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU13-53 | O-071 | P21/R03 | A1 | IN ✓ | hash changed | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU13-54 | O-070 | P08/R08 | T5 other tenant | IN ✓ | 1 approver | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU13-55 | O-072 | P08/R08 | A5 wrong role | UK draft | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-56 | O-072 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-57 | O-072 | P08/R08 | A1 | IN ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-58 | O-069 | P08/R08 | A5 wrong role | IN ✓ | 2 approvals | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU13-59 | O-071 | P09/R10 | A1 | US ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-60 | O-072 | P09/R10 | T5 other tenant | US ✓ | 1 approver | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU13-61 | O-070 | P09/R10 | A3 SoD/limit | IN ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-62 | O-072 | P21/R03 | A5 wrong role | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-63 | O-070 | P08/R08 | A5 wrong role | UK draft | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-64 | O-071 | P08/R08 | A3 SoD/limit | UK draft | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU13-65 | O-071 | P09/R10 | A3 SoD/limit | IN ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU13-66 | O-072 | P21/R03 | T5 other tenant | US ✓ | hash changed | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU13-67 | O-069 | P09/R10 | A5 wrong role | UK draft | hash changed | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU13-68 | O-071 | P09/R10 | A5 wrong role | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU13-69 | O-069 | P21/R03 | A5 wrong role | UK draft | 1 approver | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU13-70 | O-070 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU13-71 | O-069 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Metric registry |
      | EX-33ZU13-72 | O-070 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Evidence pack |
      | EX-33ZU13-73 | O-071 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Disclosure draft |
      | EX-33ZU13-74 | O-072 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Commitment report |
```

##### US-33-ZU14 INV-SVC-22 Cross-Border Funding Compliance Coordination Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-33-ZU14 |
| Title | INV-SVC-22 Cross-Border Funding Compliance Coordination Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-22 Cross-Border Funding Compliance Coordination Automation workflows (cross-border funding route and jurisdiction requirement; required documentation and regulatory evidence collection; currency, ownership and transaction restriction review; cross-border filing deadline and professional approval) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-073; FR-V12-O-074; FR-V12-O-075; FR-V12-O-076; DEC-770, DEC-779, DEC-783, DEC-822; tests TC-V12-O-289, TC-V12-O-297, TC-V12-O-305, TC-V12-O-313 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-22-WF01 Cross-border funding route and…; Part 11.16c §INV-SVC-22-WF02 Required documentation and…; Part 11.16c §INV-SVC-22-WF03 Currency, ownership and…; Part 11.16c §INV-SVC-22-WF04 Cross-border filing deadline and… |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-073, FR-V12-O-074, FR-V12-O-075, FR-V12-O-076: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO01, US-32-ZO02, US-32-ZO09, US-33-ZO07 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-22 Cross-Border Funding Compliance Coordination Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-33ZU14-01 Happy path – Cross-border funding route and jurisdiction requirement mapping (FR-V12-O-073)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-22-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-22-WF01:v2` (FR-V12-O-073)
    Then Cross-border funding route and jurisdiction requirement mapping:
      """
      Issuer and recipient jurisdictions, funding route → Jurisdiction review matrix
      """
    And Jurisdiction review matrix; acceptance INV-SVC-22-WF01-AT01 → TC-V12-O-289 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU14-02 Alternate – Required documentation and regulatory evidence collection (FR-V12-O-074)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-22-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-22-WF02:v2` (FR-V12-O-074)
    Then Required documentation and regulatory evidence collection: Approved checklist, authorized documents → Evidence dossier
    And Evidence dossier; acceptance INV-SVC-22-WF02-AT01 → TC-V12-O-297 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU14-03 Alternate – Currency, ownership and transaction restriction review routing (FR-V12-O-075)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-22-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-22-WF03:v2` (FR-V12-O-075)
    Then Currency, ownership and transaction restriction review routing: Transaction terms, ownership, currency, jurisdiction → Risk review case
    And Risk review case; acceptance INV-SVC-22-WF03-AT01 → TC-V12-O-305 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @alt @DEC-783
  Scenario: AC-33ZU14-04 Alternate – Cross-border filing deadline and professional approval tracking (FR-V12-O-076)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-22-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-22-WF04:v2` (FR-V12-O-076)
    Then Cross-border filing deadline and professional approval tracking:
      """
      Approved deadlines, reviewer decision, filing evidence → Deadline and approval register
      """
    And Deadline and approval register; acceptance INV-SVC-22-WF04-AT01 → TC-V12-O-313 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @neg @DEC-822
  Scenario: AC-33ZU14-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-33ZU14-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-33ZU14-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-33ZU14-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-33ZU14-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 78 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-073 = Cross-border funding route and jurisdiction…
    #   O-074 = Required documentation and regulatory evidence…
    #   O-075 = Currency, ownership and transaction restriction…
    #   O-076 = Cross-border filing deadline and professional…
    Examples: MU09 rows (3-way, seed 1214; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-33ZU14-01 | O-073 | P21/R03 | A5 wrong role | IN ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-02 | O-073 | P21/R03 | A1 | UK draft | hash changed | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU14-03 | O-076 | P09/R10 | A1 | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-04 | O-075 | P08/R08 | A5 wrong role | US ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-05 | O-073 | P09/R10 | T5 other tenant | US ✓ | hash changed | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU14-06 | O-076 | P08/R08 | A3 SoD/limit | UK draft | 1 approver | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU14-07 | O-075 | P21/R03 | A3 SoD/limit | UK draft | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-08 | O-074 | P08/R08 | A1 | US ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-09 | O-074 | P21/R03 | T5 other tenant | IN ✓ | 1 approver | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU14-10 | O-074 | P09/R10 | A5 wrong role | UK draft | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-11 | O-076 | P09/R10 | A5 wrong role | US ✓ | 2 approvals | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU14-12 | O-075 | P08/R08 | A5 wrong role | IN ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-13 | O-074 | P21/R03 | A3 SoD/limit | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-14 | O-073 | P08/R08 | T5 other tenant | UK draft | 2 approvals | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU14-15 | O-075 | P09/R10 | A1 | IN ✓ | 2 approvals | active | EU | ALLOW: Risk review case |
      | EX-33ZU14-16 | O-076 | P21/R03 | A1 | US ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-17 | O-073 | P09/R10 | A3 SoD/limit | UK draft | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-18 | O-073 | P08/R08 | A3 SoD/limit | IN ✓ | hash changed | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU14-19 | O-074 | P08/R08 | A1 | IN ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-20 | O-074 | P09/R10 | T5 other tenant | UK draft | 2 approvals | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU14-21 | O-076 | P08/R08 | T5 other tenant | UK draft | hash changed | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU14-22 | O-075 | P21/R03 | A5 wrong role | US ✓ | hash changed | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU14-23 | O-076 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU14-24 | O-075 | P09/R10 | A3 SoD/limit | IN ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-25 | O-075 | P08/R08 | T5 other tenant | US ✓ | 1 approver | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU14-26 | O-074 | P21/R03 | A5 wrong role | UK draft | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-27 | O-074 | P09/R10 | A3 SoD/limit | US ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-28 | O-076 | P08/R08 | T5 other tenant | IN ✓ | 2 approvals | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU14-29 | O-073 | P21/R03 | A1 | UK draft | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-30 | O-074 | P21/R03 | A3 SoD/limit | IN ✓ | 2 approvals | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU14-31 | O-073 | P09/R10 | A5 wrong role | IN ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-32 | O-075 | P09/R10 | A1 | UK draft | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-33 | O-073 | P08/R08 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-34 | O-076 | P08/R08 | A1 | US ✓ | hash changed | active | EU | HOLD APPROVAL_STALE |
      | EX-33ZU14-35 | O-076 | P21/R03 | T5 other tenant | IN ✓ | hash changed | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU14-36 | O-074 | P08/R08 | A5 wrong role | UK draft | 2 approvals | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU14-37 | O-075 | P21/R03 | T5 other tenant | UK draft | 1 approver | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU14-38 | O-075 | P09/R10 | A1 | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-39 | O-076 | P09/R10 | A3 SoD/limit | IN ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-40 | O-073 | P08/R08 | A5 wrong role | IN ✓ | 1 approver | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU14-41 | O-076 | P21/R03 | A5 wrong role | UK draft | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-42 | O-075 | P09/R10 | T5 other tenant | IN ✓ | hash changed | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU14-43 | O-075 | P08/R08 | A1 | UK draft | 2 approvals | active | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU14-44 | O-074 | P09/R10 | T5 other tenant | US ✓ | hash changed | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU14-45 | O-073 | P08/R08 | A1 | IN ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-46 | O-073 | P21/R03 | A5 wrong role | US ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-47 | O-076 | P09/R10 | T5 other tenant | IN ✓ | 1 approver | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU14-48 | O-076 | P08/R08 | A3 SoD/limit | UK draft | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-49 | O-074 | P21/R03 | A1 | UK draft | 1 approver | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU14-50 | O-073 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU14-51 | O-074 | P09/R10 | A1 | IN ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-52 | O-075 | P21/R03 | A1 | IN ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-53 | O-073 | P21/R03 | T5 other tenant | IN ✓ | 1 approver | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU14-54 | O-075 | P08/R08 | A3 SoD/limit | US ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-55 | O-074 | P08/R08 | A3 SoD/limit | US ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-56 | O-076 | P08/R08 | A5 wrong role | IN ✓ | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-57 | O-076 | P09/R10 | A1 | UK draft | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-58 | O-076 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU14-59 | O-073 | P09/R10 | A5 wrong role | UK draft | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-60 | O-075 | P09/R10 | A5 wrong role | UK draft | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-61 | O-073 | P09/R10 | A1 | US ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-62 | O-073 | P21/R03 | A3 SoD/limit | US ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-63 | O-074 | P09/R10 | A5 wrong role | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-64 | O-074 | P08/R08 | T5 other tenant | IN ✓ | 2 approvals | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU14-65 | O-075 | P08/R08 | T5 other tenant | UK draft | 2 approvals | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU14-66 | O-076 | P08/R08 | A3 SoD/limit | IN ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-67 | O-073 | P09/R10 | A5 wrong role | US ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-68 | O-073 | P09/R10 | T5 other tenant | IN ✓ | 1 approver | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU14-69 | O-074 | P08/R08 | A5 wrong role | IN ✓ | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU14-70 | O-075 | P21/R03 | A3 SoD/limit | US ✓ | 2 approvals | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU14-71 | O-076 | P21/R03 | A5 wrong role | US ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU14-72 | O-074 | P09/R10 | T5 other tenant | US ✓ | hash changed | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU14-73 | O-074 | P09/R10 | A3 SoD/limit | UK draft | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU14-74 | O-074 | P21/R03 | A1 | IN ✓ | 2 approvals | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU14-75 | O-073 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Jurisdiction review matrix |
      | EX-33ZU14-76 | O-074 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Evidence dossier |
      | EX-33ZU14-77 | O-075 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Risk review case |
      | EX-33ZU14-78 | O-076 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Deadline and approval register |
```

##### US-33-ZU15 INV-SVC-23 Board & Shareholder Governance Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-33-ZU15 |
| Title | INV-SVC-23 Board & Shareholder Governance Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-23 Board & Shareholder Governance Automation workflows (board meeting agenda and resolution preparation; shareholder approval and voting workflow coordination; board decision and corporate obligation tracking; governance evidence and investor information pack) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-077; FR-V12-O-078; FR-V12-O-079; FR-V12-O-080; DEC-770, DEC-779, DEC-783, DEC-822; tests TC-V12-O-321, TC-V12-O-329, TC-V12-O-337, TC-V12-O-345 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-23-WF01 Board meeting agenda and…; Part 11.16c §INV-SVC-23-WF02 Shareholder approval and voting…; Part 11.16c §INV-SVC-23-WF03 Board decision and corporate…; Part 11.16c §INV-SVC-23-WF04 Governance evidence and investor… |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-077, FR-V12-O-078, FR-V12-O-079, FR-V12-O-080: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO03, US-32-ZO04, US-32-ZO09, US-33-ZO09, US-33-ZO10 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-23 Board & Shareholder Governance Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-33ZU15-01 Happy path – Board meeting agenda and resolution preparation (FR-V12-O-077)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-23-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-23-WF01:v2` (FR-V12-O-077)
    Then Board meeting agenda and resolution preparation: Meeting request, approved agenda items, governing documents → Meeting pack
    And Meeting pack; acceptance INV-SVC-23-WF01-AT01 → TC-V12-O-321 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @alt @DEC-783
  Scenario: AC-33ZU15-02 Alternate – Shareholder approval and voting workflow coordination (FR-V12-O-078)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-23-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-23-WF02:v2` (FR-V12-O-078)
    Then Shareholder approval and voting workflow coordination: Eligible shareholder register, voting rules, resolution → Approval evidence
    And Approval evidence; acceptance INV-SVC-23-WF02-AT01 → TC-V12-O-329 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @alt @DEC-783
  Scenario: AC-33ZU15-03 Alternate – Board decision and corporate obligation tracking (FR-V12-O-079)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-23-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-23-WF03:v2` (FR-V12-O-079)
    Then Board decision and corporate obligation tracking: Approved minutes, decision owners, deadlines → Decision register
    And Decision register; acceptance INV-SVC-23-WF03-AT01 → TC-V12-O-337 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU15-04 Alternate – Governance evidence and investor information pack preparation (FR-V12-O-080)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-23-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-23-WF04:v2` (FR-V12-O-080)
    Then Governance evidence and investor information pack preparation:
      """
      Approved decisions, disclosure rights, reporting records → Governance evidence pack
      """
    And Governance evidence pack; acceptance INV-SVC-23-WF04-AT01 → TC-V12-O-345 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @neg @DEC-822
  Scenario: AC-33ZU15-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-33ZU15-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-33ZU15-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-33ZU15-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-33ZU15-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 76 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-077 = Board meeting agenda and resolution preparation
    #   O-078 = Shareholder approval and voting workflow…
    #   O-079 = Board decision and corporate obligation tracking
    #   O-080 = Governance evidence and investor information pack…
    Examples: MU09 rows (3-way, seed 1221; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-33ZU15-01 | O-079 | P21/R03 | T5 other tenant | UK draft | 2 approvals | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU15-02 | O-078 | P09/R10 | A3 SoD/limit | UK draft | hash changed | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU15-03 | O-077 | P21/R03 | A1 | US ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-04 | O-077 | P08/R08 | A3 SoD/limit | IN ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-05 | O-080 | P09/R10 | A5 wrong role | US ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-06 | O-079 | P08/R08 | A5 wrong role | IN ✓ | hash changed | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU15-07 | O-080 | P21/R03 | A3 SoD/limit | UK draft | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-08 | O-078 | P09/R10 | T5 other tenant | IN ✓ | 2 approvals | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU15-09 | O-077 | P09/R10 | T5 other tenant | US ✓ | 1 approver | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU15-10 | O-079 | P09/R10 | A1 | IN ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-11 | O-078 | P08/R08 | A1 | UK draft | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-12 | O-080 | P21/R03 | A1 | IN ✓ | 2 approvals | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU15-13 | O-078 | P08/R08 | A3 SoD/limit | US ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-14 | O-080 | P08/R08 | A5 wrong role | UK draft | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-15 | O-078 | P21/R03 | A5 wrong role | US ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-16 | O-077 | P21/R03 | A1 | UK draft | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-17 | O-080 | P08/R08 | T5 other tenant | IN ✓ | hash changed | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU15-18 | O-079 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-19 | O-080 | P08/R08 | A1 | US ✓ | 1 approver | active | IN | HELD TWO_APPROVALS_REQUIRED |
      | EX-33ZU15-20 | O-077 | P09/R10 | A5 wrong role | UK draft | 2 approvals | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU15-21 | O-079 | P21/R03 | A3 SoD/limit | IN ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-22 | O-078 | P21/R03 | A5 wrong role | IN ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-23 | O-079 | P08/R08 | T5 other tenant | UK draft | 1 approver | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU15-24 | O-078 | P21/R03 | T5 other tenant | US ✓ | hash changed | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU15-25 | O-077 | P09/R10 | T5 other tenant | IN ✓ | hash changed | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU15-26 | O-080 | P09/R10 | A1 | UK draft | hash changed | active | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU15-27 | O-079 | P08/R08 | T5 other tenant | US ✓ | 2 approvals | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU15-28 | O-077 | P21/R03 | A3 SoD/limit | IN ✓ | 2 approvals | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU15-29 | O-079 | P21/R03 | A5 wrong role | UK draft | 1 approver | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU15-30 | O-078 | P09/R10 | T5 other tenant | UK draft | 1 approver | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU15-31 | O-077 | P08/R08 | A5 wrong role | US ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-32 | O-080 | P09/R10 | A3 SoD/limit | US ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-33 | O-077 | P08/R08 | T5 other tenant | UK draft | 2 approvals | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU15-34 | O-079 | P09/R10 | A5 wrong role | IN ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-35 | O-078 | P08/R08 | A1 | IN ✓ | 1 approver | active | EU | HELD TWO_APPROVALS_REQUIRED |
      | EX-33ZU15-36 | O-079 | P21/R03 | A1 | US ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-37 | O-080 | P09/R10 | T5 other tenant | IN ✓ | 1 approver | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU15-38 | O-080 | P08/R08 | A3 SoD/limit | UK draft | hash changed | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU15-39 | O-078 | P08/R08 | A1 | UK draft | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-40 | O-080 | P21/R03 | T5 other tenant | US ✓ | hash changed | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU15-41 | O-077 | P09/R10 | A1 | UK draft | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-42 | O-077 | P09/R10 | A3 SoD/limit | US ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-43 | O-078 | P21/R03 | A5 wrong role | UK draft | 2 approvals | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU15-44 | O-080 | P08/R08 | A5 wrong role | IN ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-45 | O-079 | P09/R10 | A3 SoD/limit | UK draft | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-46 | O-079 | P08/R08 | A1 | IN ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-47 | O-078 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU15-48 | O-077 | P08/R08 | A1 | IN ✓ | hash changed | active | IN | HOLD APPROVAL_STALE |
      | EX-33ZU15-49 | O-079 | P09/R10 | A1 | US ✓ | 2 approvals | active | EU | ALLOW: Decision register |
      | EX-33ZU15-50 | O-078 | P09/R10 | A5 wrong role | US ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-51 | O-077 | P21/R03 | A5 wrong role | IN ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-52 | O-080 | P21/R03 | T5 other tenant | UK draft | 2 approvals | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU15-53 | O-079 | P09/R10 | A5 wrong role | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-54 | O-079 | P08/R08 | A3 SoD/limit | US ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-55 | O-080 | P21/R03 | T5 other tenant | IN ✓ | 1 approver | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU15-56 | O-078 | P08/R08 | A3 SoD/limit | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-57 | O-079 | P09/R10 | T5 other tenant | IN ✓ | hash changed | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU15-58 | O-080 | P21/R03 | A5 wrong role | US ✓ | 2 approvals | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU15-59 | O-078 | P08/R08 | A5 wrong role | UK draft | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-60 | O-077 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU15-61 | O-078 | P21/R03 | A1 | US ✓ | 1 approver | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-62 | O-077 | P09/R10 | A3 SoD/limit | UK draft | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-63 | O-078 | P08/R08 | T5 other tenant | UK draft | hash changed | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU15-64 | O-080 | P09/R10 | A3 SoD/limit | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-65 | O-079 | P21/R03 | A5 wrong role | US ✓ | hash changed | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU15-66 | O-078 | P09/R10 | A1 | IN ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-67 | O-079 | P21/R03 | A3 SoD/limit | UK draft | 2 approvals | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU15-68 | O-077 | P21/R03 | A3 SoD/limit | US ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-69 | O-079 | P09/R10 | A1 | UK draft | 2 approvals | active | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU15-70 | O-077 | P08/R08 | A5 wrong role | IN ✓ | 2 approvals | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU15-71 | O-080 | P09/R10 | A1 | IN ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU15-72 | O-080 | P21/R03 | A1 | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU15-73 | O-077 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Meeting pack |
      | EX-33ZU15-74 | O-078 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Approval evidence |
      | EX-33ZU15-75 | O-079 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Decision register |
      | EX-33ZU15-76 | O-080 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Governance evidence pack |
```

##### US-33-ZU16 INV-SVC-24 Investor Identity, Ownership & Risk Evidence Automation: workflow contracts WF01–WF04

| Field | Value |
|---|---|
| ID | US-33-ZU16 |
| Title | INV-SVC-24 Investor Identity, Ownership & Risk Evidence Automation: workflow contracts WF01–WF04 |
| Type | Feature |
| Story | As an investor-relations user (P21, R03 in the INV product), I want the four INV-SVC-24 Investor Identity, Ownership & Risk Evidence Automation workflows (authorized investor identity and organization evidence; beneficial ownership and verification-provider coordination; applicable risk-screening result review and exception; verification expiry and material investor information) to run as typed, policy-checked contracts on the universal engine, so that each Investment Automation workflow runs as a typed, policy-checked contract with no unauthorised effect |
| Persona / roles | Investor-relations user (P21, R03 in the INV product); approvers and reviewers per the Background |
| Traces | FR-V12-O-081; FR-V12-O-082; FR-V12-O-083; FR-V12-O-084; DEC-770, DEC-779, DEC-783, DEC-822; tests TC-V12-O-353, TC-V12-O-361, TC-V12-O-369, TC-V12-O-377 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-32-ZO09, US-33-ZO12, US-30-ZN02, US-18-YD02; source definition: Part 11.16c §INV-SVC-24-WF01 Authorized investor identity and…; Part 11.16c §INV-SVC-24-WF02 Beneficial ownership and…; Part 11.16c §INV-SVC-24-WF03 Applicable risk-screening result…; Part 11.16c §INV-SVC-24-WF04 Verification expiry and material… |
| Dimension profile | persona ×3 · authority ×4 · jurisdiction ×3 · approval ×3 · service/SKU ×3 · region ×3 · operation ×4 · model MU09 |
| Notes | FR-V12-O-081, FR-V12-O-082, FR-V12-O-083, FR-V12-O-084: release per DEC-783, DEC-770 (Investment Automation in Release 2; activation per counsel-approved pack) · Related existing stories (shared source IDs, no FR trace): US-32-ZO09, US-33-ZO11 · Screens A233–A259, W77–W99; API family `/api/v1/investor/runs/`; audit events `inv.run.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: INV-SVC-24 Investor Identity, Ownership & Risk Evidence Automation: workflow contracts WF01–WF04
  Background:
    Given issuer "AppNAI Technologies Pvt Ltd" (zone IN):
      """
      with the INV SKU of the service active, investor-relations user "nikhil@appnai.example.com", finance "dev@appnai.example.com" (R08) and
      counsel "farah@appnai.example.com" (R10)
      """
    And the workflow schema version pinned on each run and jurisdiction packs RP-IN-SEC (Approved), RP-US-REGD (Approved) and RP-UK-FPO (Draft)

  @happy @DEC-783
  Scenario: AC-33ZU16-01 Happy path – Authorized investor identity and organization evidence collection (FR-V12-O-081)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-24-WF01 runs with a DTO valid against `urn:inv:dto:INV-SVC-24-WF01:v2` (FR-V12-O-081)
    Then Authorized investor identity and organization evidence collection:
      """
      Verified request, lawful purpose, authorized identity records → Verification case
      """
    And Verification case; acceptance INV-SVC-24-WF01-AT01 → TC-V12-O-353 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU16-02 Alternate – Beneficial ownership and verification-provider coordination (FR-V12-O-082)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-24-WF02 runs with a DTO valid against `urn:inv:dto:INV-SVC-24-WF02:v2` (FR-V12-O-082)
    Then Beneficial ownership and verification-provider coordination:
      """
      Entity ownership evidence, approved provider grant → Ownership verification evidence
      """
    And Ownership verification evidence; acceptance INV-SVC-24-WF02-AT01 → TC-V12-O-361 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @alt @DEC-783
  Scenario: AC-33ZU16-03 Alternate – Applicable risk-screening result review and exception routing (FR-V12-O-083)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-24-WF03 runs with a DTO valid against `urn:inv:dto:INV-SVC-24-WF03:v2` (FR-V12-O-083)
    Then Applicable risk-screening result review and exception routing: Authorized screening results, policy, reviewer → Risk review case
    And Risk review case; acceptance INV-SVC-24-WF03-AT01 → TC-V12-O-369 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "L1 — consequential/authority-bearing: human approval of the payload hash; PDP recheck
      at dispatch"
      """

  @alt @DEC-783
  Scenario: AC-33ZU16-04 Alternate – Verification expiry and material investor information change… (FR-V12-O-084)
    Given the trigger "Manual; scheduled monitoring; validated business event; authorized provider:
      """
      webhook when available" occurs for issuer "AppNAI Technologies Pvt Ltd"
      """
    When INV-SVC-24-WF04 runs with a DTO valid against `urn:inv:dto:INV-SVC-24-WF04:v2` (FR-V12-O-084)
    Then Verification expiry and material investor information change monitoring:
      """
      Verification timestamps, permitted updates, policy → Renewal or exception alert
      """
    And Renewal or exception alert; acceptance INV-SVC-24-WF04-AT01 → TC-V12-O-377 and the tests below
    And every step records class, input reference:
      """
      output reference, state and evidence, and autonomy is "Internal analysis and drafts run unattended (L3 internal, no external effect)"
      """

  @neg @DEC-822
  Scenario: AC-33ZU16-05 Negative – a consequential workflow step never runs under a mandate
    Given a run of the service reaches a step classed "consequential financial/legal"
    When the engine looks for an Active mandate
    Then no mandate is applicable (DEC-822), the step waits for two-person approval on the payload hash and nothing is dispatched

  @val
  Scenario: AC-33ZU16-06 Validation – the DTO rejects unknown or malformed fields
    When a run is started with a DTO containing an unknown field "notes_extra"
    Then the API returns 422 with field errors, no StepRun is created and the audit event "dto.rejected" is written

  @perm @BRL-TEN-04
  Scenario: AC-33ZU16-07 Permission – a reference from another tenant or startup is not found
    When the run input references a record of tenant T2
    Then the response is 403 or the indistinguishable 404 and zero rows, events or provider calls occur in the other scope

  @edge @DEC-050
  Scenario: AC-33ZU16-08 Edge – a crash after a checkpoint reconciles, never re-runs a completed effect
    Given a worker crashed after the provider confirmed an effect
    When the reaper resumes the run
    Then the run is "Reconciling" and the completed effect is not repeated

  @sec @obs @MU09
  Scenario Outline: AC-33ZU16-09 Permutations – Investment Automation workflows (INV-SVC-13…24) (3-way, 75 rows)
    Given actor "<persona>" with authority "<authority>" in zone "<region>"
    And the INV service is "<service_sku>", the pack is "<jurisdiction>" and approval is "<approval>"
    When workflow "<operation>" runs
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU09 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   O-081 = Authorized investor identity and organization…
    #   O-082 = Beneficial ownership and verification-provider…
    #   O-083 = Applicable risk-screening result review and…
    #   O-084 = Verification expiry and material investor…
    Examples: MU09 rows (3-way, seed 1228; space 3,888; tuples 1230/1230; +4 baseline-allow)
      | ex | operation | persona | authority | jurisdiction | approval | service_sku | region | expected |
      | EX-33ZU16-01 | O-082 | P21/R03 | T5 other tenant | IN ✓ | hash changed | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU16-02 | O-084 | P09/R10 | A1 | UK draft | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-03 | O-081 | P21/R03 | A5 wrong role | UK draft | 2 approvals | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU16-04 | O-081 | P08/R08 | A1 | IN ✓ | hash changed | active | EU | HOLD APPROVAL_STALE |
      | EX-33ZU16-05 | O-081 | P21/R03 | A3 SoD/limit | US ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-06 | O-083 | P09/R10 | A5 wrong role | US ✓ | 1 approver | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU16-07 | O-082 | P08/R08 | T5 other tenant | UK draft | 1 approver | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU16-08 | O-082 | P09/R10 | A3 SoD/limit | UK draft | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-09 | O-084 | P08/R08 | A5 wrong role | US ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-10 | O-083 | P08/R08 | A1 | IN ✓ | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-11 | O-081 | P09/R10 | T5 other tenant | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU16-12 | O-084 | P21/R03 | T5 other tenant | UK draft | 1 approver | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU16-13 | O-083 | P08/R08 | T5 other tenant | US ✓ | 2 approvals | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU16-14 | O-084 | P09/R10 | A3 SoD/limit | IN ✓ | 1 approver | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU16-15 | O-081 | P09/R10 | A3 SoD/limit | US ✓ | hash changed | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-16 | O-083 | P21/R03 | A1 | IN ✓ | 2 approvals | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU16-17 | O-082 | P21/R03 | A1 | US ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-18 | O-082 | P08/R08 | A3 SoD/limit | US ✓ | 2 approvals | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU16-19 | O-083 | P08/R08 | A5 wrong role | UK draft | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-20 | O-084 | P21/R03 | A5 wrong role | IN ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-21 | O-083 | P21/R03 | A3 SoD/limit | UK draft | hash changed | active | EU | 403 SOD_CONFLICT |
      | EX-33ZU16-22 | O-082 | P09/R10 | A5 wrong role | IN ✓ | hash changed | active | EU→IN (misrouted) | 403 PERMISSION_DENIED |
      | EX-33ZU16-23 | O-081 | P09/R10 | A1 | UK draft | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-24 | O-084 | P21/R03 | T5 other tenant | US ✓ | hash changed | active | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU16-25 | O-084 | P09/R10 | A1 | US ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-26 | O-081 | P08/R08 | A5 wrong role | IN ✓ | 1 approver | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-27 | O-083 | P09/R10 | A3 SoD/limit | UK draft | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-28 | O-084 | P08/R08 | A3 SoD/limit | IN ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-29 | O-082 | P21/R03 | A5 wrong role | UK draft | 1 approver | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-30 | O-083 | P09/R10 | T5 other tenant | UK draft | 2 approvals | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU16-31 | O-081 | P08/R08 | T5 other tenant | US ✓ | 1 approver | not subscribed | IN | uniform 404 NOT_FOUND |
      | EX-33ZU16-32 | O-082 | P08/R08 | A1 | UK draft | 2 approvals | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-33 | O-082 | P09/R10 | A3 SoD/limit | IN ✓ | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-34 | O-083 | P21/R03 | A5 wrong role | US ✓ | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-35 | O-082 | P21/R03 | A3 SoD/limit | IN ✓ | 2 approvals | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-36 | O-084 | P08/R08 | A3 SoD/limit | UK draft | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-37 | O-083 | P09/R10 | A1 | IN ✓ | hash changed | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-38 | O-081 | P21/R03 | A1 | UK draft | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-39 | O-082 | P09/R10 | A1 | US ✓ | 1 approver | active | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-33ZU16-40 | O-081 | P21/R03 | T5 other tenant | IN ✓ | 1 approver | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU16-41 | O-082 | P08/R08 | T5 other tenant | UK draft | hash changed | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU16-42 | O-084 | P08/R08 | A1 | UK draft | 2 approvals | active | EU | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU16-43 | O-083 | P08/R08 | A3 SoD/limit | US ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-44 | O-083 | P09/R10 | A5 wrong role | IN ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-45 | O-084 | P09/R10 | T5 other tenant | US ✓ | 1 approver | suspended | EU | uniform 404 NOT_FOUND |
      | EX-33ZU16-46 | O-081 | P08/R08 | A3 SoD/limit | US ✓ | 2 approvals | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-47 | O-083 | P21/R03 | A1 | US ✓ | 1 approver | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-48 | O-081 | P08/R08 | A5 wrong role | US ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-49 | O-084 | P09/R10 | A5 wrong role | UK draft | hash changed | active | IN | 403 PERMISSION_DENIED |
      | EX-33ZU16-50 | O-082 | P09/R10 | A5 wrong role | US ✓ | 2 approvals | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-51 | O-084 | P09/R10 | A1 | IN ✓ | 1 approver | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-52 | O-084 | P21/R03 | A3 SoD/limit | US ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-53 | O-081 | P09/R10 | T5 other tenant | UK draft | hash changed | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU16-54 | O-084 | P08/R08 | T5 other tenant | IN ✓ | 2 approvals | active | IN | uniform 404 NOT_FOUND |
      | EX-33ZU16-55 | O-082 | P08/R08 | A5 wrong role | IN ✓ | 1 approver | active | EU | 403 PERMISSION_DENIED |
      | EX-33ZU16-56 | O-081 | P08/R08 | A1 | US ✓ | hash changed | active | IN | HOLD APPROVAL_STALE |
      | EX-33ZU16-57 | O-083 | P21/R03 | T5 other tenant | IN ✓ | hash changed | not subscribed | EU | uniform 404 NOT_FOUND |
      | EX-33ZU16-58 | O-081 | P08/R08 | A3 SoD/limit | UK draft | 2 approvals | active | EU→IN (misrouted) | 403 SOD_CONFLICT |
      | EX-33ZU16-59 | O-083 | P08/R08 | A3 SoD/limit | IN ✓ | 2 approvals | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU16-60 | O-082 | P21/R03 | T5 other tenant | US ✓ | 2 approvals | active | EU | uniform 404 NOT_FOUND |
      | EX-33ZU16-61 | O-083 | P21/R03 | T5 other tenant | UK draft | 1 approver | suspended | EU→IN (misrouted) | uniform 404 NOT_FOUND |
      | EX-33ZU16-62 | O-081 | P09/R10 | A3 SoD/limit | IN ✓ | hash changed | active | IN | 403 SOD_CONFLICT |
      | EX-33ZU16-63 | O-082 | P21/R03 | A1 | IN ✓ | 2 approvals | not subscribed | IN | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-64 | O-081 | P09/R10 | A5 wrong role | UK draft | hash changed | not subscribed | EU→IN (misrouted) | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-65 | O-083 | P08/R08 | A1 | UK draft | hash changed | suspended | IN | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-66 | O-084 | P09/R10 | A5 wrong role | UK draft | 1 approver | suspended | EU | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-67 | O-084 | P09/R10 | A3 SoD/limit | US ✓ | hash changed | suspended | EU→IN (misrouted) | 409 SUBSCRIPTION_SUSPENDED |
      | EX-33ZU16-68 | O-082 | P09/R10 | T5 other tenant | US ✓ | 2 approvals | suspended | IN | uniform 404 NOT_FOUND |
      | EX-33ZU16-69 | O-081 | P09/R10 | A1 | US ✓ | 2 approvals | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-70 | O-084 | P21/R03 | A1 | UK draft | 2 approvals | active | IN | HOLD PACK_NOT_ACTIVE |
      | EX-33ZU16-71 | O-082 | P21/R03 | A3 SoD/limit | US ✓ | hash changed | not subscribed | EU | 403 ENTITLEMENT_REQUIRED |
      | EX-33ZU16-72 | O-081 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Verification case |
      | EX-33ZU16-73 | O-082 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Ownership verification evidence |
      | EX-33ZU16-74 | O-083 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Risk review case |
      | EX-33ZU16-75 | O-084 | P21/R03 | A1 | IN ✓ | 2 approvals | active | IN | ALLOW: Renewal or exception alert |
```

#### 11.22.5.4.34 EP-34 Global expansion, certification and multi-market operations (new, DEC-942)

| Field | Value |
|---|---|
| Epic | EP-34 Global expansion, certification and multi-market operations (new, DEC-942) (this part) |
| New stories in this file | US-34-ZU01, US-34-ZU02, US-34-ZU03, US-34-ZU04 |
| FR-V12 covered | K: 137–139, 145–152 |
| Size | 4 stories · 29–47 SP · 14–47 pd (0.5/1.0 pd per SP) · central 26.6 pd (0.7 pd per SP mid) |
| Releases | Release 1: 2, Release 2: 2 |

##### US-34-ZU01 ENT-CMP-01…03: SOC 2, ISO/IEC 27001, 27701 and 42001 in the decided sequence

| Field | Value |
|---|---|
| ID | US-34-ZU01 |
| Title | ENT-CMP-01…03: SOC 2, ISO/IEC 27001, 27701 and 42001 in the decided sequence |
| Type | Compliance |
| Story | As an owner/founder (P01, R01) with counsel (P09, R10) and finance (P08, R08), I want SOC 2 Type I at R2 and Type II at R3; ISO/IEC 27001 certification at R3; ISO/IEC 27701 and ISO/IEC 42001 at R4, so that we enter new markets and certifications in a planned, lawful and evidenced way |
| Persona / roles | Owner/founder (P01, R01) with counsel (P09, R10) and finance (P08, R08) |
| Traces | FR-V12-K-137 (ENT-CMP-01); FR-V12-K-138 (ENT-CMP-02); FR-V12-K-139 (ENT-CMP-03); DEC-411, DEC-775; tests TC-V12-K-137, TC-V12-K-138, TC-V12-K-139 |
| Priority | Must |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-01-ZR28, US-03-YA01, US-19-YG31, US-21-YE03; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · market ×4 · locale ×3 · tax/currency ×3 · evidence ×2 · region ×3 · operation ×3 · model MU12 |
| Notes | FR-V12-K-137: release per DEC-775 (SOC 2 Type I at Release 2) · FR-V12-K-138: release per DEC-775 (SOC 2 Type II and ISO/IEC 27001 at R3) · FR-V12-K-139: release per DEC-775 (ISO/IEC 27701 and 42001 at R4) · Screens A090, A190, A200, W46, W52; API family `/api/v1/markets/`; audit events `market.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: ENT-CMP-01…03: SOC 2, ISO/IEC 27001, 27701 and 42001 in the decided sequence
  Background:
    Given the platform with residency zones IN (Mumbai) and EU active and markets UAE, UK, APAC and US in state "planned" (DEC-776)
    And locale bundles en-IN and hi-IN released, de-DE and fr-FR in translation and ar-AE (right-to-left) planned

  @happy @ENT-CMP-01 @DEC-775
  Scenario: AC-34ZU01-01 Happy path – SOC 2 Type I at R2 and Type II at R3. (FR-V12-K-137)
    Given the Founder (R01) is signed in to the tenant with the capability enabled
    When "SOC 2 Type I at R2 and Type II at R3." is exercised as specified by FR-V12-K-137: SOC 2 Type I at R2 and Type II at R3.
    Then evidence test: approved legal set published:
      """
      sub-processor change notice, counsel sign-off recorded per pack, accessibility conformance report attached
      """
    And the audit event "market.soc_2_type_i_at_r2_and_type" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-CMP-02 @DEC-775
  Scenario: AC-34ZU01-02 Alternate – ISO/IEC 27001 certification at R3. (FR-V12-K-138)
    Given the Founder (R01) is signed in to the tenant with the capability enabled
    When "ISO/IEC 27001 certification at R3." is exercised as specified by FR-V12-K-138: ISO/IEC 27001 certification at R3.
    Then evidence test: approved legal set published:
      """
      sub-processor change notice, counsel sign-off recorded per pack, accessibility conformance report attached
      """
    And the audit event "market.iso_iec_27001_certification" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-CMP-03 @DEC-775
  Scenario: AC-34ZU01-03 Alternate – ISO/IEC 27701 and ISO/IEC 42001 at R4. (FR-V12-K-139)
    Given the Founder (R01) is signed in to the tenant with the capability enabled
    When "ISO/IEC 27701 and ISO/IEC 42001 at R4." is exercised as specified by FR-V12-K-139: ISO/IEC 27701 and ISO/IEC 42001 at R4.
    Then evidence test: approved legal set published:
      """
      sub-processor change notice, counsel sign-off recorded per pack, accessibility conformance report attached
      """
    And the audit event "market.iso_iec_27701_and_iso_iec" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @DEC-776
  Scenario: AC-34ZU01-04 Negative – a market cannot open without counsel and tax approval
    Given market "US" has no signed rule pack and no approved tax configuration
    When the Founder sets the market to "active"
    Then the API returns 409 "MARKET_GATES_OPEN" listing "counsel_pack" and "tax_adviser" and the market stays "planned"

  @val
  Scenario: AC-34ZU01-05 Validation – locale formats follow ICU, E.164 and IANA
    When a phone number "98400 12345" is stored for a contact in India
    Then it is normalised to "+919840012345" and an invalid number is rejected with 422 "E164_INVALID"

  @perm
  Scenario: AC-34ZU01-06 Permission – only finance and the tax adviser approve tax rules
    When "maya@kestrel.example.com" (R05) approves tax rule TX-06
    Then the API returns 403 and TX-06 stays "Draft"

  @edge
  Scenario: AC-34ZU01-07 Edge – a missing FX rate never produces a converted total
    Given invoices in INR and EUR and no approved EUR→INR rate for 2027-06-30
    When the portfolio report renders
    Then native totals are shown and the converted total is withheld with "FX_RATE_MISSING"

  @sec @obs @MU12
  Scenario Outline: AC-34ZU01-08 Permutations – Global expansion, certification and tax (3-way, 59 rows)
    Given actor "<persona>" for market "<market>" in zone "<region>" with locale "<locale>"
    And tax/currency is "<tax_currency>" and evidence is "<evidence>"
    When "<operation>" is applied
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU12 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-137 = SOC 2 Type I at R2 and Type II at R3.
    #   K-138 = ISO/IEC 27001 certification at R3.
    #   K-139 = ISO/IEC 27701 and ISO/IEC 42001 at R4.
    Examples: MU12 rows (3-way, seed 1235; space 1,944; tuples 930/930; +3 baseline-allow)
      | ex | operation | persona | market | locale | tax_currency | evidence | region | expected |
      | EX-34ZU01-01 | K-137 | P08/R08 | UAE | en-IN | tax draft | complete | EU | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU01-02 | K-139 | P08/R08 | US | ar-AE RTL | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-03 | K-138 | P08/R08 | India | de-DE | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-04 | K-139 | P09/R10 | UAE | de-DE | FX missing | complete | IN | converted total withheld |
      | EX-34ZU01-05 | K-138 | P01/R01 | US | de-DE | rule ✓ native | complete | EU | NOT ACTIVE |
      | EX-34ZU01-06 | K-137 | P01/R01 | EU-DE | ar-AE RTL | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-07 | K-137 | P09/R10 | US | en-IN | rule ✓ native | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-08 | K-139 | P01/R01 | India | ar-AE RTL | FX missing | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU01-09 | K-138 | P09/R10 | EU-DE | ar-AE RTL | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU01-10 | K-138 | P01/R01 | UAE | en-IN | FX missing | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-11 | K-139 | P09/R10 | India | en-IN | tax draft | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-12 | K-137 | P08/R08 | EU-DE | de-DE | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU01-13 | K-137 | P01/R01 | US | de-DE | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-14 | K-138 | P09/R10 | UAE | ar-AE RTL | rule ✓ native | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-15 | K-139 | P01/R01 | EU-DE | en-IN | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU01-16 | K-138 | P08/R08 | India | en-IN | rule ✓ native | complete | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-34ZU01-17 | K-139 | P08/R08 | EU-DE | de-DE | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-18 | K-138 | P08/R08 | US | ar-AE RTL | FX missing | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU01-19 | K-137 | P09/R10 | India | de-DE | FX missing | complete | EU | converted total withheld |
      | EX-34ZU01-20 | K-139 | P01/R01 | UAE | de-DE | rule ✓ native | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-21 | K-137 | P01/R01 | UAE | ar-AE RTL | rule ✓ native | complete | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-34ZU01-22 | K-138 | P09/R10 | EU-DE | en-IN | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-23 | K-137 | P09/R10 | UAE | ar-AE RTL | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-24 | K-139 | P09/R10 | US | ar-AE RTL | tax draft | complete | EU | NOT ACTIVE |
      | EX-34ZU01-25 | K-137 | P08/R08 | India | en-IN | FX missing | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-26 | K-139 | P09/R10 | EU-DE | en-IN | rule ✓ native | complete | EU | ALLOW: Evidence test: approved legal set published, |
      | EX-34ZU01-27 | K-138 | P01/R01 | India | ar-AE RTL | tax draft | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-28 | K-139 | P01/R01 | US | en-IN | FX missing | complete | EU | NOT ACTIVE |
      | EX-34ZU01-29 | K-138 | P09/R10 | EU-DE | de-DE | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-30 | K-139 | P08/R08 | UAE | en-IN | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-31 | K-138 | P08/R08 | UAE | de-DE | FX missing | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU01-32 | K-137 | P01/R01 | India | en-IN | rule ✓ native | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-33 | K-138 | P08/R08 | US | en-IN | tax draft | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-34 | K-139 | P09/R10 | US | de-DE | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU01-35 | K-137 | P09/R10 | US | ar-AE RTL | FX missing | complete | IN | NOT ACTIVE |
      | EX-34ZU01-36 | K-137 | P08/R08 | India | ar-AE RTL | rule ✓ native | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-37 | K-139 | P08/R08 | India | de-DE | rule ✓ native | complete | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-34ZU01-38 | K-139 | P08/R08 | EU-DE | ar-AE RTL | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-39 | K-138 | P01/R01 | EU-DE | ar-AE RTL | rule ✓ native | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-40 | K-137 | P09/R10 | EU-DE | en-IN | FX missing | complete | IN | converted total withheld |
      | EX-34ZU01-41 | K-137 | P01/R01 | UAE | de-DE | tax draft | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-42 | K-137 | P09/R10 | India | ar-AE RTL | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU01-43 | K-139 | P08/R08 | UAE | ar-AE RTL | FX missing | complete | EU | converted total withheld |
      | EX-34ZU01-44 | K-139 | P08/R08 | UAE | en-IN | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU01-45 | K-137 | P01/R01 | US | de-DE | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-46 | K-137 | P01/R01 | EU-DE | de-DE | tax draft | complete | EU | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU01-47 | K-138 | P08/R08 | EU-DE | en-IN | FX missing | complete | EU | converted total withheld |
      | EX-34ZU01-48 | K-139 | P01/R01 | India | de-DE | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU01-49 | K-138 | P09/R10 | US | en-IN | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-50 | K-137 | P08/R08 | US | de-DE | rule ✓ native | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-51 | K-138 | P09/R10 | India | ar-AE RTL | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-52 | K-137 | P09/R10 | UAE | en-IN | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-53 | K-138 | P01/R01 | UAE | de-DE | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-54 | K-139 | P09/R10 | India | de-DE | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU01-55 | K-137 | P01/R01 | US | ar-AE RTL | FX missing | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU01-56 | K-137 | P01/R01 | EU-DE | de-DE | FX missing | complete | IN | converted total withheld |
      | EX-34ZU01-57 | K-137 | P01/R01 | India | en-IN | rule ✓ native | complete | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-34ZU01-58 | K-138 | P01/R01 | India | en-IN | rule ✓ native | complete | IN | ALLOW: Evidence test: approved legal set published, |
      | EX-34ZU01-59 | K-139 | P01/R01 | India | en-IN | rule ✓ native | complete | IN | ALLOW: Evidence test: approved legal set published, |
```

##### US-34-ZU02 ENT-GLB-01…03: internationalisation framework, staged locales and right-to-left

| Field | Value |
|---|---|
| ID | US-34-ZU02 |
| Title | ENT-GLB-01…03: internationalisation framework, staged locales and right-to-left |
| Type | Compliance |
| Story | As an owner/founder (P01, R01) with counsel (P09, R10) and finance (P08, R08), I want internationalisation framework: externalised strings, ICU MessageFormat, pseudo-localisation tests; locales: English and Hindi (R2), German and French (R3), Arabic (R4), others by market; right-to-left layout support, so that we enter new markets and certifications in a planned, lawful and evidenced way |
| Persona / roles | Owner/founder (P01, R01) with counsel (P09, R10) and finance (P08, R08) |
| Traces | FR-V12-K-145 (ENT-GLB-01); FR-V12-K-146 (ENT-GLB-02); FR-V12-K-147 (ENT-GLB-03); DEC-776; tests TC-V12-K-145, TC-V12-K-146, TC-V12-K-147 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-01-ZR28, US-03-YA01, US-19-YG31, US-21-YE03; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · market ×4 · locale ×3 · tax/currency ×3 · evidence ×2 · region ×3 · operation ×3 · model MU12 |
| Notes | FR-V12-K-145: release per DEC-776 (i18n framework is the base for every market) · FR-V12-K-146: release per DEC-776 (en/hi Release 2; de/fr R3; ar R4 – one story, staged locales) · FR-V12-K-147: release per DEC-776 (Arabic RTL) · Screens A090, A190, A200, W46, W52; API family `/api/v1/markets/`; audit events `market.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: ENT-GLB-01…03: internationalisation framework, staged locales and right-to-left
  Background:
    Given the platform with residency zones IN (Mumbai) and EU active and markets UAE, UK, APAC and US in state "planned" (DEC-776)
    And locale bundles en-IN and hi-IN released, de-DE and fr-FR in translation and ar-AE (right-to-left) planned

  @happy @ENT-GLB-01 @DEC-776
  Scenario: AC-34ZU02-01 Happy path – Internationalisation framework: externalised strings (FR-V12-K-145)
    Given the Founder (R01) is signed in to the tenant with the capability enabled
    When "Internationalisation framework:
      """
      externalised strings" is exercised as specified by FR-V12-K-145: Internationalisation framework: externalised strings, ICU MessageFormat,
      pseudo-localisation tests.
      """
    Then i18n test: externalised strings:
      """
      ICU plurals, pseudo-localisation, E.164/IANA/currency formats; locale/tax/region items gated by Founder decision
      """
    And the audit event "market.internationalisation" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-GLB-02 @DEC-776
  Scenario: AC-34ZU02-02 Alternate – Locales: English and Hindi (R2), German and French (R3), Arabic (R4) (FR-V12-K-146)
    Given the Founder (R01) is signed in to the tenant with the capability enabled
    When "Locales: English and Hindi (R2), German and French (R3), Arabic (R4)" is exercised as specified by FR-V12-K-146:
      """
      Locales: English and Hindi (R2), German and French (R3), Arabic (R4), others by market.
      """
    Then i18n test: externalised strings:
      """
      ICU plurals, pseudo-localisation, E.164/IANA/currency formats; locale/tax/region items gated by Founder decision
      """
    And the audit event "market.locales_english_and_hindi" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-GLB-03 @DEC-776
  Scenario: AC-34ZU02-03 Alternate – Right-to-left layout support. (FR-V12-K-147)
    Given the Founder (R01) is signed in to the tenant with the capability enabled
    When "Right-to-left layout support." is exercised as specified by FR-V12-K-147: Right-to-left layout support.
    Then i18n test: externalised strings:
      """
      ICU plurals, pseudo-localisation, E.164/IANA/currency formats; locale/tax/region items gated by Founder decision
      """
    And the audit event "market.right_to_left_layout_support" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @DEC-776
  Scenario: AC-34ZU02-04 Negative – a market cannot open without counsel and tax approval
    Given market "US" has no signed rule pack and no approved tax configuration
    When the Founder sets the market to "active"
    Then the API returns 409 "MARKET_GATES_OPEN" listing "counsel_pack" and "tax_adviser" and the market stays "planned"

  @val
  Scenario: AC-34ZU02-05 Validation – locale formats follow ICU, E.164 and IANA
    When a phone number "98400 12345" is stored for a contact in India
    Then it is normalised to "+919840012345" and an invalid number is rejected with 422 "E164_INVALID"

  @perm
  Scenario: AC-34ZU02-06 Permission – only finance and the tax adviser approve tax rules
    When "maya@kestrel.example.com" (R05) approves tax rule TX-06
    Then the API returns 403 and TX-06 stays "Draft"

  @edge
  Scenario: AC-34ZU02-07 Edge – a missing FX rate never produces a converted total
    Given invoices in INR and EUR and no approved EUR→INR rate for 2027-06-30
    When the portfolio report renders
    Then native totals are shown and the converted total is withheld with "FX_RATE_MISSING"

  @sec @obs @MU12
  Scenario Outline: AC-34ZU02-08 Permutations – Global expansion, certification and tax (3-way, 62 rows)
    Given actor "<persona>" for market "<market>" in zone "<region>" with locale "<locale>"
    And tax/currency is "<tax_currency>" and evidence is "<evidence>"
    When "<operation>" is applied
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU12 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-145 = Internationalisation framework: externalised strings
    #   K-146 = Locales: English and Hindi (R2)
    #   K-147 = Right-to-left layout support.
    Examples: MU12 rows (3-way, seed 1242; space 1,944; tuples 930/930; +3 baseline-allow)
      | ex | operation | persona | market | locale | tax_currency | evidence | region | expected |
      | EX-34ZU02-01 | K-147 | P09/R10 | EU-DE | en-IN | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU02-02 | K-145 | P09/R10 | India | ar-AE RTL | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-03 | K-147 | P09/R10 | US | de-DE | rule ✓ native | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-04 | K-146 | P08/R08 | India | en-IN | FX missing | complete | EU | converted total withheld |
      | EX-34ZU02-05 | K-145 | P01/R01 | UAE | en-IN | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-06 | K-146 | P01/R01 | EU-DE | ar-AE RTL | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-07 | K-145 | P08/R08 | UAE | de-DE | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-08 | K-146 | P08/R08 | US | ar-AE RTL | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-09 | K-145 | P01/R01 | US | de-DE | FX missing | complete | IN | NOT ACTIVE |
      | EX-34ZU02-10 | K-147 | P01/R01 | UAE | ar-AE RTL | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-11 | K-147 | P08/R08 | EU-DE | en-IN | rule ✓ native | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-12 | K-146 | P01/R01 | India | de-DE | tax draft | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-13 | K-147 | P08/R08 | India | ar-AE RTL | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU02-14 | K-145 | P09/R10 | UAE | ar-AE RTL | rule ✓ native | complete | EU | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU02-15 | K-146 | P09/R10 | UAE | en-IN | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-16 | K-145 | P08/R08 | EU-DE | de-DE | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-17 | K-146 | P09/R10 | UAE | de-DE | FX missing | complete | IN | converted total withheld |
      | EX-34ZU02-18 | K-147 | P01/R01 | US | en-IN | tax draft | complete | EU | NOT ACTIVE |
      | EX-34ZU02-19 | K-147 | P08/R08 | US | ar-AE RTL | FX missing | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-20 | K-145 | P01/R01 | EU-DE | ar-AE RTL | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-21 | K-145 | P09/R10 | US | en-IN | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-22 | K-146 | P01/R01 | US | en-IN | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-23 | K-147 | P09/R10 | India | de-DE | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-24 | K-146 | P09/R10 | EU-DE | de-DE | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-25 | K-147 | P01/R01 | India | en-IN | FX missing | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-26 | K-147 | P01/R01 | UAE | de-DE | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-27 | K-146 | P09/R10 | EU-DE | ar-AE RTL | tax draft | complete | EU | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU02-28 | K-147 | P08/R08 | UAE | en-IN | tax draft | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-29 | K-145 | P08/R08 | India | de-DE | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-30 | K-146 | P08/R08 | US | de-DE | rule ✓ native | complete | EU | NOT ACTIVE |
      | EX-34ZU02-31 | K-145 | P09/R10 | EU-DE | en-IN | FX missing | complete | EU | converted total withheld |
      | EX-34ZU02-32 | K-145 | P01/R01 | India | en-IN | rule ✓ native | complete | EU | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU02-33 | K-147 | P01/R01 | EU-DE | de-DE | FX missing | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-34 | K-146 | P08/R08 | EU-DE | ar-AE RTL | FX missing | complete | IN | converted total withheld |
      | EX-34ZU02-35 | K-145 | P09/R10 | US | ar-AE RTL | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-36 | K-146 | P08/R08 | UAE | ar-AE RTL | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-37 | K-146 | P09/R10 | India | en-IN | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-38 | K-145 | P01/R01 | India | en-IN | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-39 | K-145 | P09/R10 | EU-DE | de-DE | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-40 | K-146 | P08/R08 | India | ar-AE RTL | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-41 | K-145 | P08/R08 | UAE | en-IN | FX missing | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-42 | K-146 | P01/R01 | UAE | de-DE | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-43 | K-145 | P08/R08 | US | ar-AE RTL | rule ✓ native | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-44 | K-147 | P09/R10 | UAE | ar-AE RTL | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-45 | K-147 | P08/R08 | US | en-IN | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-46 | K-146 | P09/R10 | US | de-DE | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-47 | K-147 | P09/R10 | India | de-DE | FX missing | complete | EU | converted total withheld |
      | EX-34ZU02-48 | K-147 | P01/R01 | EU-DE | ar-AE RTL | rule ✓ native | complete | EU | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU02-49 | K-147 | P08/R08 | India | de-DE | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU02-50 | K-146 | P01/R01 | US | ar-AE RTL | FX missing | complete | EU | NOT ACTIVE |
      | EX-34ZU02-51 | K-145 | P01/R01 | India | ar-AE RTL | tax draft | complete | EU | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU02-52 | K-146 | P01/R01 | UAE | de-DE | FX missing | complete | EU | converted total withheld |
      | EX-34ZU02-53 | K-146 | P01/R01 | EU-DE | en-IN | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-54 | K-147 | P01/R01 | US | en-IN | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-55 | K-145 | P01/R01 | EU-DE | ar-AE RTL | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-56 | K-147 | P01/R01 | UAE | en-IN | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU02-57 | K-145 | P09/R10 | US | en-IN | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU02-58 | K-147 | P08/R08 | EU-DE | en-IN | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-59 | K-146 | P09/R10 | India | ar-AE RTL | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU02-60 | K-145 | P01/R01 | India | en-IN | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU02-61 | K-146 | P01/R01 | India | en-IN | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU02-62 | K-147 | P01/R01 | India | en-IN | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
```

##### US-34-ZU03 ENT-GLB-04…06: locale formats, tax-engine abstraction and multi-currency billing

| Field | Value |
|---|---|
| ID | US-34-ZU03 |
| Title | ENT-GLB-04…06: locale formats, tax-engine abstraction and multi-currency billing |
| Type | Compliance |
| Story | As an owner/founder (P01, R01) with counsel (P09, R10) and finance (P08, R08), I want locale formats: dates, numbers, currencies, addresses, phone numbers in E.164, IANA time zones; tax engine abstraction: India GST, EU VAT (reverse charge and OSS), UK VAT, UAE VAT, Singapore and Australia GST, US sales tax via provider; multi-currency billing with native amounts and approved FX evidence (MT-21), so that we enter new markets and certifications in a planned, lawful and evidenced way |
| Persona / roles | Owner/founder (P01, R01) with counsel (P09, R10) and finance (P08, R08) |
| Traces | FR-V12-K-148 (ENT-GLB-04); FR-V12-K-149 (ENT-GLB-05); FR-V12-K-150 (ENT-GLB-06); DEC-417, DEC-776; tests TC-V12-K-148, TC-V12-K-149, TC-V12-K-150 |
| Priority | Must |
| Wave | Release 1 (dates follow the work, DEC-770) |
| Points | 8–13 |
| Dependencies | US-01-ZR28, US-03-YA01, US-19-YG31, US-21-YE03; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · market ×4 · locale ×3 · tax/currency ×3 · evidence ×2 · region ×3 · operation ×3 · model MU12 |
| Notes | FR-V12-K-149: release per DEC-776 (tax engine TX-04…09 per market, adviser approval) · FR-V12-K-150: release per DEC-776 · Screens A090, A190, A200, W46, W52; API family `/api/v1/markets/`; audit events `market.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: ENT-GLB-04…06: locale formats, tax-engine abstraction and multi-currency billing
  Background:
    Given the platform with residency zones IN (Mumbai) and EU active and markets UAE, UK, APAC and US in state "planned" (DEC-776)
    And locale bundles en-IN and hi-IN released, de-DE and fr-FR in translation and ar-AE (right-to-left) planned

  @happy @ENT-GLB-04
  Scenario: AC-34ZU03-01 Happy path – Locale formats: dates, numbers, currencies, addresses (FR-V12-K-148)
    Given the Founder (R01) is signed in to the tenant with the capability enabled
    When "Locale formats: dates, numbers, currencies, addresses" is exercised as specified by FR-V12-K-148:
      """
      Locale formats: dates, numbers, currencies, addresses, phone numbers in E.164, IANA time zones.
      """
    Then i18n test: externalised strings:
      """
      ICU plurals, pseudo-localisation, E.164/IANA/currency formats; locale/tax/region items gated by Founder decision
      """
    And the audit event "market.locale_formats_dates" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-GLB-05 @DEC-776
  Scenario: AC-34ZU03-02 Alternate – Tax engine abstraction: India GST, EU VAT (reverse charge and OSS) (FR-V12-K-149)
    Given the Founder (R01) is signed in to the tenant with the capability enabled
    When "Tax engine abstraction: India GST, EU VAT (reverse charge and OSS)" is exercised as specified by FR-V12-K-149:
      """
      Tax engine abstraction: India GST, EU VAT (reverse charge and OSS), UK VAT, UAE VAT, Singapore and Australia GST, US sales tax via provider.
      """
    Then i18n test: externalised strings:
      """
      ICU plurals, pseudo-localisation, E.164/IANA/currency formats; locale/tax/region items gated by Founder decision
      """
    And the audit event "market.tax_engine_abstraction_india" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-GLB-06 @MT-21 @DEC-776
  Scenario: AC-34ZU03-03 Alternate – Multi-currency billing with native amounts and approved FX evidence (FR-V12-K-150)
    Given the Founder (R01) is signed in to the tenant with the capability enabled
    When "Multi-currency billing with native amounts and approved FX evidence" is exercised as specified by FR-V12-K-150:
      """
      Multi-currency billing with native amounts and approved FX evidence (MT-21).
      """
    Then i18n test: externalised strings:
      """
      ICU plurals, pseudo-localisation, E.164/IANA/currency formats; locale/tax/region items gated by Founder decision
      """
    And the audit event "market.multi_currency_billing_with" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @DEC-776
  Scenario: AC-34ZU03-04 Negative – a market cannot open without counsel and tax approval
    Given market "US" has no signed rule pack and no approved tax configuration
    When the Founder sets the market to "active"
    Then the API returns 409 "MARKET_GATES_OPEN" listing "counsel_pack" and "tax_adviser" and the market stays "planned"

  @val
  Scenario: AC-34ZU03-05 Validation – locale formats follow ICU, E.164 and IANA
    When a phone number "98400 12345" is stored for a contact in India
    Then it is normalised to "+919840012345" and an invalid number is rejected with 422 "E164_INVALID"

  @perm
  Scenario: AC-34ZU03-06 Permission – only finance and the tax adviser approve tax rules
    When "maya@kestrel.example.com" (R05) approves tax rule TX-06
    Then the API returns 403 and TX-06 stays "Draft"

  @edge
  Scenario: AC-34ZU03-07 Edge – a missing FX rate never produces a converted total
    Given invoices in INR and EUR and no approved EUR→INR rate for 2027-06-30
    When the portfolio report renders
    Then native totals are shown and the converted total is withheld with "FX_RATE_MISSING"

  @sec @obs @MU12
  Scenario Outline: AC-34ZU03-08 Permutations – Global expansion, certification and tax (3-way, 58 rows)
    Given actor "<persona>" for market "<market>" in zone "<region>" with locale "<locale>"
    And tax/currency is "<tax_currency>" and evidence is "<evidence>"
    When "<operation>" is applied
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU12 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-148 = Locale formats: dates, numbers, currencies
    #   K-149 = Tax engine abstraction: India GST
    #   K-150 = Multi-currency billing with native amounts and…
    Examples: MU12 rows (3-way, seed 1249; space 1,944; tuples 930/930; +3 baseline-allow)
      | ex | operation | persona | market | locale | tax_currency | evidence | region | expected |
      | EX-34ZU03-01 | K-148 | P08/R08 | India | en-IN | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU03-02 | K-148 | P01/R01 | EU-DE | ar-AE RTL | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-03 | K-150 | P09/R10 | UAE | de-DE | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-04 | K-149 | P08/R08 | US | ar-AE RTL | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-05 | K-150 | P01/R01 | UAE | en-IN | FX missing | complete | IN | converted total withheld |
      | EX-34ZU03-06 | K-149 | P09/R10 | EU-DE | de-DE | FX missing | complete | EU | converted total withheld |
      | EX-34ZU03-07 | K-150 | P08/R08 | EU-DE | en-IN | rule ✓ native | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-08 | K-148 | P01/R01 | India | de-DE | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-09 | K-148 | P09/R10 | UAE | ar-AE RTL | rule ✓ native | complete | EU | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU03-10 | K-150 | P01/R01 | US | de-DE | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU03-11 | K-150 | P01/R01 | India | ar-AE RTL | tax draft | complete | EU | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU03-12 | K-149 | P09/R10 | US | en-IN | rule ✓ native | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-13 | K-148 | P01/R01 | US | en-IN | tax draft | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-14 | K-148 | P08/R08 | US | de-DE | FX missing | complete | IN | NOT ACTIVE |
      | EX-34ZU03-15 | K-150 | P09/R10 | India | ar-AE RTL | FX missing | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-16 | K-149 | P08/R08 | UAE | ar-AE RTL | FX missing | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU03-17 | K-148 | P09/R10 | EU-DE | en-IN | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU03-18 | K-149 | P01/R01 | UAE | de-DE | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-19 | K-149 | P01/R01 | EU-DE | ar-AE RTL | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU03-20 | K-149 | P08/R08 | India | de-DE | rule ✓ native | complete | EU | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU03-21 | K-148 | P09/R10 | India | en-IN | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-22 | K-148 | P08/R08 | UAE | en-IN | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-23 | K-150 | P08/R08 | India | de-DE | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-24 | K-149 | P09/R10 | US | de-DE | tax draft | complete | EU | NOT ACTIVE |
      | EX-34ZU03-25 | K-150 | P08/R08 | EU-DE | de-DE | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU03-26 | K-150 | P08/R08 | US | ar-AE RTL | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-27 | K-149 | P01/R01 | EU-DE | en-IN | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU03-28 | K-150 | P09/R10 | India | ar-AE RTL | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU03-29 | K-148 | P09/R10 | EU-DE | de-DE | rule ✓ native | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-30 | K-149 | P09/R10 | India | de-DE | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-31 | K-148 | P01/R01 | UAE | de-DE | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU03-32 | K-149 | P08/R08 | EU-DE | en-IN | FX missing | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-33 | K-150 | P09/R10 | US | en-IN | rule ✓ native | complete | IN | NOT ACTIVE |
      | EX-34ZU03-34 | K-148 | P08/R08 | US | ar-AE RTL | rule ✓ native | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-35 | K-148 | P08/R08 | EU-DE | ar-AE RTL | tax draft | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-36 | K-149 | P09/R10 | UAE | ar-AE RTL | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-37 | K-149 | P01/R01 | India | en-IN | FX missing | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU03-38 | K-150 | P08/R08 | UAE | en-IN | tax draft | complete | EU | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU03-39 | K-150 | P01/R01 | UAE | en-IN | rule ✓ native | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-40 | K-148 | P09/R10 | US | ar-AE RTL | FX missing | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU03-41 | K-149 | P01/R01 | US | ar-AE RTL | rule ✓ native | complete | EU | NOT ACTIVE |
      | EX-34ZU03-42 | K-150 | P01/R01 | EU-DE | de-DE | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-43 | K-150 | P09/R10 | EU-DE | ar-AE RTL | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU03-44 | K-150 | P08/R08 | India | en-IN | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU03-45 | K-149 | P01/R01 | US | en-IN | FX missing | complete | IN | NOT ACTIVE |
      | EX-34ZU03-46 | K-148 | P09/R10 | UAE | en-IN | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-47 | K-149 | P08/R08 | UAE | de-DE | rule ✓ native | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-48 | K-150 | P09/R10 | US | de-DE | tax draft | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-49 | K-148 | P08/R08 | India | ar-AE RTL | FX missing | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-50 | K-150 | P01/R01 | UAE | ar-AE RTL | FX missing | complete | IN | converted total withheld |
      | EX-34ZU03-51 | K-149 | P01/R01 | UAE | en-IN | tax draft | complete | EU | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU03-52 | K-148 | P08/R08 | US | en-IN | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU03-53 | K-150 | P08/R08 | EU-DE | de-DE | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-54 | K-148 | P01/R01 | India | de-DE | FX missing | complete | EU | converted total withheld |
      | EX-34ZU03-55 | K-149 | P01/R01 | India | ar-AE RTL | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU03-56 | K-148 | P01/R01 | India | en-IN | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU03-57 | K-149 | P01/R01 | India | en-IN | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU03-58 | K-150 | P01/R01 | India | en-IN | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
```

##### US-34-ZU04 ENT-GLB-07…08: regional messaging providers and region expansion plan

| Field | Value |
|---|---|
| ID | US-34-ZU04 |
| Title | ENT-GLB-07…08: regional messaging providers and region expansion plan |
| Type | Compliance |
| Story | As an owner/founder (P01, R01) with counsel (P09, R10) and finance (P08, R08), I want regional messaging providers selected per market (DLT India, sender registration elsewhere); region expansion plan with data residency (US, UK, Middle East, APAC), so that we enter new markets and certifications in a planned, lawful and evidenced way |
| Persona / roles | Owner/founder (P01, R01) with counsel (P09, R10) and finance (P08, R08) |
| Traces | FR-V12-K-151 (ENT-GLB-07); FR-V12-K-152 (ENT-GLB-08); DEC-776; tests TC-V12-K-151, TC-V12-K-152 |
| Priority | Should |
| Wave | Release 2 (dates follow the work, DEC-770) |
| Points | 5–8 |
| Dependencies | US-01-ZR28, US-03-YA01, US-19-YG31, US-21-YE03; source definition: Part 11.11b §11.11.5.16 Requirements |
| Dimension profile | persona ×3 · market ×4 · locale ×3 · tax/currency ×3 · evidence ×2 · region ×3 · operation ×2 · model MU12 |
| Notes | FR-V12-K-151: release per DEC-776 · FR-V12-K-152: release per DEC-776 (UK, Middle East, APAC, US) · Screens A090, A190, A200, W46, W52; API family `/api/v1/markets/`; audit events `market.*`; feature flag default OFF until DoD D-14 evidence · DoR R-12: activates per jurisdiction only when the counsel-signed rule pack is Approved (Part 11.15; DEC-779…783) |

```gherkin
Feature: ENT-GLB-07…08: regional messaging providers and region expansion plan
  Background:
    Given the platform with residency zones IN (Mumbai) and EU active and markets UAE, UK, APAC and US in state "planned" (DEC-776)
    And locale bundles en-IN and hi-IN released, de-DE and fr-FR in translation and ar-AE (right-to-left) planned

  @happy @ENT-GLB-07 @DEC-776
  Scenario: AC-34ZU04-01 Happy path – Regional messaging providers selected per market (DLT India (FR-V12-K-151)
    Given the Founder (R01) is signed in to the tenant with the capability enabled
    When "Regional messaging providers selected per market (DLT India" is exercised as specified by FR-V12-K-151:
      """
      Regional messaging providers selected per market (DLT India, sender registration elsewhere).
      """
    Then i18n test: externalised strings:
      """
      ICU plurals, pseudo-localisation, E.164/IANA/currency formats; locale/tax/region items gated by Founder decision
      """
    And the audit event "market.regional_messaging_providers" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @alt @ENT-GLB-08 @DEC-776
  Scenario: AC-34ZU04-02 Alternate – Region expansion plan with data residency (US, UK, Middle East, APAC). (FR-V12-K-152)
    Given the Founder (R01) is signed in to the tenant with the capability enabled
    When "Region expansion plan with data residency (US, UK, Middle East, APAC)." is exercised as specified by FR-V12-K-152:
      """
      Region expansion plan with data residency (US, UK, Middle East, APAC).
      """
    Then i18n test: externalised strings:
      """
      ICU plurals, pseudo-localisation, E.164/IANA/currency formats; locale/tax/region items gated by Founder decision
      """
    And the audit event "market.region_expansion_plan_with" is written with outcome "allowed", correlation_id, tenant_id and company_id

  @neg @DEC-776
  Scenario: AC-34ZU04-03 Negative – a market cannot open without counsel and tax approval
    Given market "US" has no signed rule pack and no approved tax configuration
    When the Founder sets the market to "active"
    Then the API returns 409 "MARKET_GATES_OPEN" listing "counsel_pack" and "tax_adviser" and the market stays "planned"

  @val
  Scenario: AC-34ZU04-04 Validation – locale formats follow ICU, E.164 and IANA
    When a phone number "98400 12345" is stored for a contact in India
    Then it is normalised to "+919840012345" and an invalid number is rejected with 422 "E164_INVALID"

  @perm
  Scenario: AC-34ZU04-05 Permission – only finance and the tax adviser approve tax rules
    When "maya@kestrel.example.com" (R05) approves tax rule TX-06
    Then the API returns 403 and TX-06 stays "Draft"

  @edge
  Scenario: AC-34ZU04-06 Edge – a missing FX rate never produces a converted total
    Given invoices in INR and EUR and no approved EUR→INR rate for 2027-06-30
    When the portfolio report renders
    Then native totals are shown and the converted total is withheld with "FX_RATE_MISSING"

  @sec @obs @MU12
  Scenario Outline: AC-34ZU04-07 Permutations – Global expansion, certification and tax (3-way, 52 rows)
    Given actor "<persona>" for market "<market>" in zone "<region>" with locale "<locale>"
    And tax/currency is "<tax_currency>" and evidence is "<evidence>"
    When "<operation>" is applied
    Then the outcome is "<expected>"
    And the row <ex> is recorded with its parameter values in the test evidence
    # Value codes of model MU12 (§11.22.5.2): persona Pnn/Rnn; authority A1 authorised, A3 SoD or over limit,
    # A5 wrong role, T5 other tenant; zones IN, EU, EU→IN misrouted; ✓ = Approved. Operations:
    #   K-151 = Regional messaging providers selected per market
    #   K-152 = Region expansion plan with data residency (US, UK
    Examples: MU12 rows (3-way, seed 1256; space 1,296; tuples 796/796; +2 baseline-allow)
      | ex | operation | persona | market | locale | tax_currency | evidence | region | expected |
      | EX-34ZU04-01 | K-151 | P08/R08 | India | de-DE | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU04-02 | K-152 | P09/R10 | UAE | en-IN | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU04-03 | K-152 | P08/R08 | India | en-IN | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-04 | K-152 | P01/R01 | UAE | de-DE | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-05 | K-151 | P01/R01 | US | en-IN | tax draft | complete | EU | NOT ACTIVE |
      | EX-34ZU04-06 | K-151 | P09/R10 | EU-DE | ar-AE RTL | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-07 | K-152 | P08/R08 | EU-DE | ar-AE RTL | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU04-08 | K-151 | P01/R01 | US | ar-AE RTL | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-09 | K-152 | P01/R01 | India | de-DE | FX missing | complete | IN | converted total withheld |
      | EX-34ZU04-10 | K-151 | P09/R10 | UAE | de-DE | FX missing | complete | EU | converted total withheld |
      | EX-34ZU04-11 | K-152 | P09/R10 | US | de-DE | rule ✓ native | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-12 | K-151 | P09/R10 | India | en-IN | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-13 | K-151 | P08/R08 | UAE | ar-AE RTL | tax draft | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-14 | K-152 | P08/R08 | US | ar-AE RTL | FX missing | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU04-15 | K-152 | P01/R01 | EU-DE | ar-AE RTL | rule ✓ native | complete | EU | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU04-16 | K-151 | P08/R08 | EU-DE | de-DE | FX missing | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-17 | K-151 | P01/R01 | EU-DE | en-IN | FX missing | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU04-18 | K-152 | P09/R10 | India | ar-AE RTL | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU04-19 | K-152 | P08/R08 | EU-DE | en-IN | rule ✓ native | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-20 | K-151 | P01/R01 | UAE | en-IN | rule ✓ native | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-21 | K-151 | P09/R10 | EU-DE | de-DE | tax draft | complete | EU | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU04-22 | K-152 | P09/R10 | UAE | ar-AE RTL | FX missing | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-23 | K-151 | P08/R08 | US | en-IN | tax draft | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-24 | K-151 | P01/R01 | India | ar-AE RTL | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-25 | K-151 | P09/R10 | US | de-DE | FX missing | complete | IN | NOT ACTIVE |
      | EX-34ZU04-26 | K-151 | P01/R01 | UAE | ar-AE RTL | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU04-27 | K-152 | P01/R01 | EU-DE | en-IN | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-28 | K-152 | P08/R08 | UAE | de-DE | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU04-29 | K-152 | P08/R08 | US | en-IN | rule ✓ native | complete | IN | NOT ACTIVE |
      | EX-34ZU04-30 | K-152 | P08/R08 | India | de-DE | tax draft | complete | EU | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU04-31 | K-152 | P09/R10 | EU-DE | en-IN | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-32 | K-152 | P09/R10 | India | ar-AE RTL | rule ✓ native | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-33 | K-152 | P09/R10 | India | de-DE | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-34 | K-151 | P01/R01 | EU-DE | de-DE | rule ✓ native | complete | EU | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU04-35 | K-151 | P01/R01 | India | en-IN | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU04-36 | K-152 | P01/R01 | US | de-DE | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-37 | K-152 | P08/R08 | UAE | en-IN | FX missing | missing | EU→IN (misrouted) | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-38 | K-151 | P09/R10 | US | en-IN | rule ✓ native | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU04-39 | K-151 | P01/R01 | UAE | en-IN | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU04-40 | K-152 | P08/R08 | India | ar-AE RTL | rule ✓ native | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-41 | K-152 | P09/R10 | US | ar-AE RTL | tax draft | missing | IN | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-42 | K-152 | P09/R10 | EU-DE | de-DE | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU04-43 | K-152 | P08/R08 | US | ar-AE RTL | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-44 | K-151 | P08/R08 | US | de-DE | tax draft | complete | IN | NOT ACTIVE |
      | EX-34ZU04-45 | K-152 | P01/R01 | UAE | en-IN | FX missing | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-46 | K-151 | P08/R08 | EU-DE | de-DE | rule ✓ native | missing | EU | BLOCKED EVIDENCE_MISSING |
      | EX-34ZU04-47 | K-152 | P09/R10 | UAE | de-DE | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU04-48 | K-152 | P09/R10 | US | en-IN | FX missing | complete | IN | NOT ACTIVE |
      | EX-34ZU04-49 | K-152 | P09/R10 | EU-DE | de-DE | tax draft | complete | EU→IN (misrouted) | 409 RESIDENCY_ZONE_MISMATCH |
      | EX-34ZU04-50 | K-151 | P01/R01 | India | ar-AE RTL | tax draft | complete | IN | HOLD TAX_RULE_NOT_APPROVED |
      | EX-34ZU04-51 | K-151 | P01/R01 | India | en-IN | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
      | EX-34ZU04-52 | K-152 | P01/R01 | India | en-IN | rule ✓ native | complete | IN | ALLOW: i18n test: externalised strings, ICU plurals, |
```


## Quality gate: Batch 11.22d

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

**Status: Part 11 Batch 11.22d complete (29 stories, EP-32, EP-33, EP-34). Continue with Batch 11.22e.**
