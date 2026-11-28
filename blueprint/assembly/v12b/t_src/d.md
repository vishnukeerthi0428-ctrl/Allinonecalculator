# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.21d), Master Test Strategy and Combinatorial Test Design (V12): Generated Cases for Localization and RTL, Accessibility, Performance and AI Evaluation

| Field | Value |
|---|---|
| Document | Part 11.21d: pairwise cases for localization and right-to-left (PM-T06), accessibility WCAG 2.2 AA (PM-T07) and performance, load, stress, spike and soak profiles (PM-T08); the AI-evaluation gate cases of the 111 V12 suites (PM-T16) in the Part 6.4 template |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Part 11.21a/b; Part 6.1 §6.1.14; Part 6.4 §6.4.1.3; Part 11.6b (EVAL-SM-SVC suites TC-V12-F-201…311); Part 11.7c; DEC-776, DEC-788 |
| Roles applied | Accessibility test lead, localization lead, performance and resilience architect, AI evaluation lead, combinatorial test design expert |

---

## 11.21.6 Generated test cases (part 3: quality attributes and AI evaluation)

### 11.21.6.10 PM-T06 Localization and right-to-left

Locales follow DEC-776: en-IN and en-GB from R1; hi-IN, ta-IN, or-IN from R2; de-DE, fr-FR (and bn-IN, en-US as extension values) from R3; ar-AE (RTL) from R4. Each case's release is the locale's release.

{{HDR_PM-T06}}

#### Group TC-V12-T-M06: Pairwise combinatorial cases – localization and RTL

{{TAB_PM-T06}}

### 11.21.6.11 PM-T07 Accessibility (WCAG 2.2 AA)

Rows with a screen reader or voice control are manual assistive-technology passes (PP-07, `Auto = N (AT pass)`, level SYS-M); keyboard-only rows are automated in Playwright with axe.

{{HDR_PM-T07}}

#### Group TC-V12-T-M07: Pairwise combinatorial cases – accessibility

{{TAB_PM-T07}}

### 11.21.6.12 PM-T08 Performance, load, stress, spike and soak

Each case schedules one run of the matching load test (LT-01…12 of Part 6.1 or LT-V12-T-01…12 of Part 11.21a §11.21.3.6) with the row's profile, zone, tenant mix, cache state and SLA tier.

{{HDR_PM-T08}}

#### Group TC-V12-T-M08: Pairwise combinatorial cases – performance profiles

{{TAB_PM-T08}}

### 11.21.6.13 PM-T16 AI evaluation gates of the 111 V12 suites

**What these cases test.** The quality of each workflow's AI step is measured by its EVAL suite (Part 11.6b). The cases below test the **gate machinery around the suites**: that every suite is selected by its triggers, runs in the tenant's zone on the right registry row and locale slice, uses human review while the judge is not calibrated, blocks promotion on adversarial violations and cost overruns, blocks only the failing locale, and never makes a candidate model routable before registry approval. Every one of the 111 suites appears exactly once; the other six parameters are covered pairwise.

{{HDR_PM-T16}}

#### Group TC-V12-T-A16: AI evaluation cases – gate machinery of the 111 suites (Part 6.4 template)

{{TAB_PM-T16}}

---

### Quality gate: Part 11.21d

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Locales DEC-776; WCAG criteria per screen group; LT thresholds; EVAL rows link TC-V12-F-2xx |
| 2 | Tags logged | Pass | ASSUMPTION-1125 (proposed performance targets) |
| 3 | IDs unique and consistent | Pass | |
| 4 | No requirement without a test | Pass | All 111 suites; all locales; all screen groups and AT |
| 5 | Negative, edge, security, accessibility | Pass | Expansion +100%, 320 CSS px reflow, forced colors, injected gate failures |
| 6 | Agents: guardrail, fallback, KPI, cost | Pass | Gate, fallback (registry, Tier 3), FinOps block asserted per suite |
| 7 | Time-sensitive facts flagged | Pass | AT and browser versions, CLDR data, model rows "verify" |
| 8 | No restricted data to free tiers | Pass | Open-weight rows assert masking; Tier 2 absent from PM-T16 by design |
| 9 | Consistent with earlier parts | Pass | Gate families and thresholds as Part 11.6b |

**Status: Part 11 Batch 11.21 file d complete. Quality-attribute and AI-evaluation cases are published.**
