# V12-B brief: Founder adopted V12 on every pending item — full-depth specification, implementation plan, tests and stories

Read `SHARED_BRIEF.md`, `V11_BRIEF.md` and `V12_BRIEF.md` first. This brief **overrides** them where they differ.

## What changed (Founder decisions of 28 Nov 2026, Part 11.14 DEC-770…791)
The Founder adopted V12 on every pending item, "irrespective of time and cost", and asked for "detailed implementation plan, test cases, test strategies, user stories, all using permutations and combinations, follow the exact template that we built in earlier blueprint". Read `Part-11-14_V12_Consolidation_and_Founder_Decisions.md` completely.

**Superseded safety caps.**
- Consequential actions are no longer always capped at L1. Bounded mandates (L3/L4) are allowed under V12's conditions (DEC-779).
- Also allowed: agentic commerce and payments (DEC-780), automatic bid submission (DEC-781), AI voice calling and recordings (DEC-782), and investor/fundraising with the Investment Automation product (DEC-783).

**Mandatory controls.** Every one of those capabilities must be specified with **V12's own conditions and full legal and operational controls**:
- mandate scope, limits, two-person approval, revocation and kill switch;
- PDP dispatch recheck, audit and reconciliation;
- jurisdiction rule packs signed off by counsel (Part 11.15);
- consent and identification rules.

"Where lawful" means the capability is **built, but activates per jurisdiction only when that jurisdiction's rule pack is approved**. Never describe a control as optional.

**Hosting and other decisions.**
- Hosting: Vercel + Supabase + AWS, in Mumbai and the EU (DEC-772), with RPO ≤ 15 min (DEC-787) and RTO ≤ 120 min (DEC-771).
- The API uses a least-privilege RLS-bound role, never `service_role` (DEC-778).
- Provider-neutral model registry, with Claude Sonnet approved as primary (DEC-788).
- 24×7 on-call (DEC-773), SLA tiers (DEC-774), certification sequence (DEC-775), global expansion (DEC-776), 09:00–21:00 messaging window (DEC-777).
- SSO/SCIM and the developer platform with CRM/SMS/voice connectors in Release 1 (DEC-784/785), personal data via Vercel (DEC-786), cross-tenant benchmarks (DEC-789).
- All change requests are funded (DEC-790). Dates follow the work (DEC-770).

## Templates you MUST follow exactly (read them first)
- **User stories:** `Part-05-1a_Epics_Stories_Foundation.md`. Copy the exact story block structure: heading, field table, story statement, Gherkin acceptance criteria, links, priority, wave, points, dependencies.
- **Test cases:** `Part-06-2a_Test_Cases_EP08-EP11.md` and `Part-06-4_AI_Evaluation_Test_Cases.md`. Copy the exact table columns.
- **Test strategy:** `Part-06-1_Test_Strategy.md`.
- **Implementation plan:** `Part-08-1_Roadmap_Releases_Sprints.md`. Also use `Part-08-2_*` for risks and go-live.
- **AI agents and automations:** the AG card and AU table formats in V11_BRIEF.
- **Service and workflow specifications:** the format of `Part-11-2b_*` (services) and `Part-11-3b_*` (workflows).

## Permutations and combinations (mandatory)
Use **combinatorial test and scenario design**:
1. **Declare the parameters and their values.** For example: tenant type; SKU/plan; jurisdiction; channel; autonomy level/mandate state; data class; residency region; locale; role; provider state; consent state.
2. **Generate all-pairs (pairwise) coverage** for every capability. Use **3-way coverage** for safety-, money- or law-critical capabilities (mandates, payments, bids, voice, investor, residency).
3. **Add an exhaustive enumeration** where the space is small (≤ 64 combinations).

Show the parameter model, the generation method, the combination count and the resulting cases. Generate them programmatically with a script saved in `assembly/v12b/`, so every combination appears as a real test case or Gherkin `Examples:` row, not as a description. Stories use **Scenario Outline + Examples** tables built from the same parameter models.

## Output rules
- Part files: `Part-11-<n>[a|b|c]_<Title>.md`, titled `## Application Blueprint: PART 11 (Batch 11.<n>), <Title>`, with numbered sections `11.<n>.x`. Each part ends with a decisions table, tags register, quality gate and status line.
- Coverage CSV (where you reconcile source material): `final/coverage_v12/<letter>_coverage.csv`, in the V12 format.
- Render with `make_pdf.sh` and get 0 diagram errors. Do not edit other files. Do not run git.
- Report back in ≤ 300 words.

## ID allocation
| Group | Part | Letter | DEC | Tags (all four types) | ADR | Other |
|---|---|---|---|---|---|---|
| P1a Investment product I: investor mode, INV-SVC-01…12 | 11.16a/b | N | 800–819 | 1000–1019 | 230–234 | FR-V12-N-###, US-<EP>-ZN<nn>, TC-V12-N-###; AG-160…179, AU-200…229; screens A205–A232, W55–W76; epics EP-30, EP-31 |
| P1b Investment product II: INV-SVC-13…24, securities rule packs | 11.16c/d | O | 820–839 | 1020–1039 | 235–239 | FR-V12-O-…; AG-180…199, AU-230…259; screens A233–A259, W77–W99; epics EP-32, EP-33 |
| P2 Mandates, agentic commerce and payments, automatic bids | 11.17 | P | 840–859 | 1040–1059 | 240–249 | FR-V12-P-…; AG-200…209, AU-260…279; WF-57…60 |
| P3 AI voice and recordings | 11.18 | Q | 860–879 | 1060–1079 | 250–254 | FR-V12-Q-…; AG-210…219, AU-280…289 |
| P4 Platform decisions (SSO/SCIM, developer platform and connectors, Vercel data path, RPO, model registry, benchmarks) | 11.19 | R | 880–899 | 1080–1099 | 255–264 | FR-V12-R-…; AU-290…299 |
| P5 Master implementation plan | 11.20 | S | 900–919 | 1100–1119 | 265–269 | — |
| P6 Master test strategy and combinatorial test design | 11.21 | T | 920–939 | 1120–1139 | 270–274 | TC-V12-T-… |
| P7 Master user stories with permutations | 11.22 | U | 940–959 | 1140–1159 | 275–279 | US-<EP>-ZU<nn> |

Tags with four digits (e.g. `[ASSUMPTION-1001]`) are allowed.
