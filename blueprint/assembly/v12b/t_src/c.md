# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.21c), Master Test Strategy and Combinatorial Test Design (V12): Generated Cases for Money-, Law- and Safety-critical Effects, Residency, Isolation, Resilience and Exhaustive Spaces

| Field | Value |
|---|---|
| Document | Part 11.21c: Investment Automation SKU invocation (PM-T02 pairwise and PM-T02N single fault); the cross-capability consequential-effect gateway in three layers (PM-T03 full space, PM-T03P positive sub-space, PM-T03N single fault × effect), data residency (PM-T04), multi-tenant isolation and RLS (PM-T05), resilience with work in flight (PM-T09) and the exhaustive models XT-10…XT-15, every case in the Part 6.2a parameterized form |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Part 11.21a/b; Part 11.17a §11.17.5.12 (PDP order) and §11.17.5.14 (eligibility register); Parts 11.15, 11.16, 11.18, 11.19; DEC-771, 772, 777, 778, 779…783, 787, 789 |
| Roles applied | Combinatorial test design expert, security test lead, performance and resilience architect, Head of Quality Engineering, Security/Compliance/AI Governance Lead |

---

## 11.21.6 Generated test cases (part 2: investment, money, law, safety, residency, isolation, resilience)

### 11.21.6.3 PM-T02 Investment Automation SKU invocation (valid set, pairwise)

{{HDR_PM-T02}}

#### Group TC-V12-T-M02: Pairwise combinatorial cases – Investment Automation SKU invocation (valid set)

{{TAB_PM-T02}}

### 11.21.6.4 PM-T02N Investment Automation invocation (invalid values, single fault)

{{NEG02_TABLE}}

{{HDR_PM-T02N}}

#### Group TC-V12-T-M02N: Single-fault cases – Investment Automation (invalid values)

{{TAB_PM-T02N}}

### 11.21.6.5 PM-T03 Consequential-effect gateway

**Purpose.** One dispatcher, one PDP and one consumption ledger decide every external effect of the platform (Part 11.17a). PM-T03 tests that decision for **15 effect types** across all money-, law- and safety-critical capabilities under the same control values, so that a fix in one capability cannot silently weaken another.

**Effects and their allow outcomes.**

{{EFFECTS_TABLE}}

**Oracle decision order** (implements §11.17.5.12 and the capability rules): 1 kill switch → 2 jurisdiction enabled → 3 pack Approved → 4 effect has a mandate path for L3/L4 → 5 level ≤ the register maximum → 6 approval or mandate state → 7 consent (personal-recipient effects only; registry scrub for SMS and voice) → 8 data class (Restricted never in an external payload; payments carry tokens only; personal data in public content needs publication consent) → 9 bid package/price equals the approved hash → 10 per-action cap → 11 aggregate cap → ALLOW. Caps are inclusive (ASSUMPTION-1121). For L1/L2 a value above the approver's threshold holds for a higher approver instead of blocking (DEC-038).

#### Layer L1: full space (variable strength)

{{HDR_PM-T03}} {{VERDICT_PM-T03}}

#### Group TC-V12-T-M03: Variable-strength combinatorial cases – consequential-effect gateway (full space)

{{TAB_PM-T03}}

#### Layer L2: positive sub-space (3-way)

Values: authorization ∈ {L1, L2 valid hash, L3 Active mandate, L4 step in graph}; value ∈ {below cap, exactly at cap}; pack ∈ {IN Approved, EU Approved}; both zones; kill switch off; consent valid; data ∈ {Public/Internal, Personal}. Rows that still deny show capability rules that hold even on the positive side (no mandate path for SMS, voice and securities offers; L4 only for MT-OUT and SVC-28 negotiation; bids only at the exact approved price; personal data in published content).

{{HDR_PM-T03P}} {{VERDICT_PM-T03P}}

#### Group TC-V12-T-M03P: 3-way combinatorial cases – consequential-effect gateway (positive sub-space)

{{TAB_PM-T03P}}

#### Layer L3: single fault × effect (exhaustive pairing)

Each of the 16 invalid control values is applied to each of the 15 effects with every other control valid. ALLOW rows in this layer are expected where the faulted control does not apply to the effect (for example consent on a supplier pay-out, or Restricted bank details that travel only as PSP tokens); the expected text states why.

{{HDR_PM-T03N}} {{VERDICT_PM-T03N}}

#### Group TC-V12-T-M03N: Single-fault cases – consequential-effect gateway

{{TAB_PM-T03N}}

### 11.21.6.6 PM-T04 Data residency (India and EU)

{{HDR_PM-T04}}

#### Group TC-V12-T-M04: 3-way combinatorial cases – data residency

{{TAB_PM-T04}}

### 11.21.6.7 PM-T05 Multi-tenant isolation and RLS

{{HDR_PM-T05}}

#### Group TC-V12-T-M05: Variable-strength combinatorial cases – isolation and RLS

{{TAB_PM-T05}}

### 11.21.6.8 PM-T09 Resilience and DR with consequential work in flight

{{HDR_PM-T09}}

#### Group TC-V12-T-M09: 3-way combinatorial cases – resilience with work in flight

{{TAB_PM-T09}}

### 11.21.6.9 Exhaustive models

#### XT-10 Rule-pack state × capability activation

{{HDR_XT-10}}

#### Group TC-V12-T-X10: Exhaustive cases – rule-pack state × capability

{{TAB_XT-10}}

#### XT-11 Subscription × entitlement state × meter usage

{{HDR_XT-11}}

#### Group TC-V12-T-X11: Exhaustive cases – subscription, entitlement and metering

{{TAB_XT-11}}

#### XT-12 Messaging window (DEC-777)

The platform window is the half-open interval [09:00:00, 21:00:00) in the recipient's local time; a stricter pack wins; transactional messages follow their own rules (DEC-931).

{{HDR_XT-12}}

#### Group TC-V12-T-X12: Exhaustive cases – messaging window

{{TAB_XT-12}}

#### XT-13 On-call and incident communication

{{HDR_XT-13}}

#### Group TC-V12-T-X13: Exhaustive cases – on-call by SLA tier, severity and time

{{TAB_XT-13}}

#### XT-14 Service-credit ladder boundaries

Boundary set per tier: 100%, exactly the target, 0.01 point below each of the three thresholds, and 97.00%. Credits follow the placeholder ladder of Part 11.11b (pending Legal and Finance wording).

{{HDR_XT-14}}

#### Group TC-V12-T-X14: Exhaustive boundary cases – service credits

{{TAB_XT-14}}

#### XT-15 Two-person approval and SoD for mandates

{{HDR_XT-15}}

#### Group TC-V12-T-X15: Exhaustive cases – mandate approvals

{{TAB_XT-15}}

---

### Quality gate: Part 11.21c

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Each model's Common block lists its links; each row its workflow and release |
| 2 | Tags logged | Pass | ASSUMPTION-1121 (inclusive caps), GAP-1126 (missing packs) |
| 3 | IDs unique and consistent | Pass | Continuous TC-V12-T range |
| 4 | No requirement without a test | Pass | Every effect × every control value (L3 exhaustive pairing) |
| 5 | Negative, edge, security, accessibility | Pass | Denials dominate L1/L3; boundaries in XT-12/14 |
| 6 | Agents | N/A | |
| 7 | Time-sensitive facts flagged | Pass | Pack contents and statutory clocks "verify" in source parts |
| 8 | No restricted data to free tiers | Pass | Restricted never in external payloads; Tier 2 never with personal data (PM-T09 provider outage rows) |
| 9 | Consistent with earlier parts | Pass | PDP order of Part 11.17a; eligibility register; DEC-777 window |

**Status: Part 11 Batch 11.21 file c complete. 3-way, single-fault and exhaustive cases for the critical areas are published.**
