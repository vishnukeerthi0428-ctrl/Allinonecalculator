# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.20b), Master Implementation Plan V12: Sprints, Team Scaling, Budgets, Risks, RAID, Governance and Change Control

| Field | Value |
|---|---|
| Document | Part 11, Batch 11.20b of 11.20a–11.20b (Group P5, letter S). Holds §11.20.7–§11.20.17: cadence and capacity, Sprints 0–2 in detail, the sprint-by-sprint plan S0–S45, team scaling and hiring, DEC-420 calibration, UAT and RACI, development and running budgets by release and by year, risk register, RAID log, governance cadence, change control, decisions, ADRs, persona review, tags and the quality gate |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Part 11.20a (roll-up, releases, gates, calendar); Part 8.1 §8.1.4–§8.1.7 and Part 8.2 §8.2.1, §8.2.2.4, §8.2.7 (templates); Part 8.4 (ledgers, rates); Part 9.5 §9.5.2.5–§9.5.2.9; Part 9.10 §9.10.10 (DEC-416…422); Part 11.14 (DEC-770…791) |
| Roles applied | Programme Director, SAFe Release Train Engineer, Principal Architect, FinOps and budgeting lead, Risk manager |
| Model | `assembly/v12b/s_master_plan.py` (scheduler and cost model) and `assembly/v12b/s_fragments.py` (tables); every computed table below is generated, not typed |

---

## 11.20.7 Sprint plans

### 11.20.7.1 Cadence, ceremonies and working agreements

The programme runs as one agile release train (ART) with up to eleven squads. Part 8.1 §8.1.4.1 ceremonies stay for each squad; the train adds the SAFe events below (DEC-905).

| Ceremony | When (IST) | Length | Participants | Output |
|---|---|---|---|---|
| Squad sprint planning | Monday of sprint week 1, 10:30 | 2 h | Squad, domain PO | Sprint goal, committed stories (DoR met), capacity sheet |
| Squad stand-up | Every working day, 10:00 | 15 min | Squad | Blockers; on-call handover Monday |
| Scrum of scrums | Tuesday and Thursday, 11:00 | 30 min | Squad tech leads, RTE, Principal Architect | Cross-squad dependencies, integration risks |
| PO sync | Wednesday, 15:00 | 45 min | Domain POs, Founder (chief PO), RTE | Backlog order across squads; scope-to-release mapping |
| Backlog refinement | Wednesday of week 1, 16:00 | 1.5 h per squad | PO, tech lead, QA, UX when needed | Next sprint meets DoR |
| System demo (train) | Friday of week 2, 14:00 | 1.5 h | All squads, POs, startup heads, Founder | Integrated increment on staging; PO acceptance |
| Squad retrospective | Friday of week 2, 16:00 | 45 min | Squad | Two improvement actions |
| PI planning | IP sprint, two days (dates §11.20.7.7) | 2 × 6 h | Whole train, Founder, business owners, counsel liaison | PI objectives per squad, programme board, risks ROAMed |
| Inspect and adapt | Last day of each PI | 3 h | Whole train | PI metrics, problem-solving workshop, backlog items |
| Change control board | Thursday, 16:00 weekly | 45 min | Founder/PO, RTE, Principal Architect, QA lead, Finance, DPO as needed | CR decisions (§11.20.13) |
| Release gate review | Gate day (Part 11.20a §11.20.5) | 1–2 h | Gate votes and advisers | Gate decision in A090 |

**Working agreements (unchanged from Part 8.1 plus DEC-420).** WIP ≤ 2 stories per engineer; DoR and dependencies met before a story enters a sprint; every change is a human-reviewed pull request; agents cannot merge or deploy; agent sandboxes hold synthetic data only; SAST, licence, secret scans and the provenance log gate every merge; auth, RLS, PDP, money, mandates, residency and AI guardrail code needs a second human reviewer from the owning squad and the security engineer; no story is Done without its evidence record.

### 11.20.7.2 Capacity method [ASSUMPTION-1101] [ASSUMPTION-1102]

```text
capacity_pd(squad, sprint) = Σ new-FTE ramp × FTE × 7.53 pd × (working days ÷ 10) × 0.95 leave
                             × coordination (1.00 ≤ 4 squads; 0.95 ≤ 7; 0.92 above)
                             × 0.5 in IP sprints × (1 − sustain reserve)
7.53 pd per FTE per sprint     = 33.9 pd ÷ 4.5 FTE (Part 9.5 §9.5.2.5, measured basis of the plan of record)
new-FTE ramp                   = 0.5 in its first sprint, 0.85 in its second, 1.0 after (Part 9.5: 15% onboarding loss)
team-of-record ramp            = 0.7 in S0 and S1 (Part 8.1, ASSUMPTION-157)
sustain reserve                = 10% of active capacity after the R1 gate; 15% after the R2-A gate (production support, defects)
capacity_SP                    = capacity_pd ÷ 0.7  (1 SP ≈ 0.7 pd, Part 8.1 §8.1.6.1)
commitment rule                = committed SP ≤ capacity_SP × 1.03; no stretch goals in S0–S2
calibration                    = the 7.53 value is re-baselined at the S2 review (DEC-420) and every PI on the 3-sprint rolling average
```

### 11.20.7.3 Sprint 0 (Mon 7 Dec – Fri 18 Dec 2026; Day 1–12)

**Sprint goal.** Every later story can rely on IaC environments, a recorded identity decision including per-tenant SAML/OIDC brokering (check 13), CI quality and security gates, RLS enforced through the least-privilege `app_rw` role with the Data API off (DEC-778), the outbox, an append-only audit log, default-OFF flags and a deny-by-default PDP.

**Capacity.** SQ-01 4.5 FTE × 7.53 × 1.0 × 0.95 × 0.7 ramp = **22.5 pd ≈ 32 SP**. **Committed: 32.0 SP** (100%).

| Story | Title | Epic | Type | Priority | Points | SP mid | Owner (role) | Dependencies |
|---|---|---|---|---|---|---|---|---|
| US-0101 | Identity compatibility spike, 12 checks + check 13 (tenant SAML/OIDC through the broker for Okta, Entra ID, Google) | EP-01 | Spike | Must | 3–6 | 4.5 | Founder/CTO + BE | DP-01, DP-15, DP-V12-S-06 |
| US-0102 | AWS, Supabase and Vercel IaC baseline for dev, test, staging and prod | EP-01 | Enabler | Must | 3–5 | 4.0 | DevOps | DP-02 |
| US-0103 | CI pipeline with quality, security and policy gates | EP-01 | Enabler | Must | 2–3 | 2.5 | DevOps + QA | US-0102 |
| US-0107 + US-01-ZR26 | RLS framework through the `app_rw` role with per-transaction `app.tenant_id` / `app.company_ids`; CI assertion that no runtime path uses `service_role` | EP-01 | Enabler (Security) | Must | 4–7 | 5.5 | BE | US-0102 |
| US-01-ZR27 (part) | Data API disabled for application schemas; break-glass path for migrations only | EP-01 | Security | Must | 1 | 1.0 | DevOps | US-0102 |
| US-0110 | Transactional outbox, idempotent consumers, retry policy | EP-01 | Enabler | Must | 3–5 | 4.0 | BE | US-0107 |
| US-0111 | Append-only audit log and job activity | EP-01 | Feature | Must | 2–3 | 2.5 | BE | US-0110 |
| US-0113 | Synthetic seed data sets (two tenants, 26 startups, sensitive fixtures; IN and EU residency fixtures) | EP-01 | Enabler (Data) | Must | 2–3 | 2.5 | QA + BE | US-0107 |
| US-0117 | Feature-flag framework with default-OFF governance | EP-01 | Enabler | Must | 1–2 | 1.5 | FS | US-0102 |
| US-0303 | PDP skeleton (plan-time and dispatch-time) | EP-03 | Enabler | Must | 3–5 | 4.0 | BE | US-0107, US-0110 |

**Non-story work in Sprint 0 (outside velocity).**

| Task | Owner | Due | Link |
|---|---|---|---|
| Sign two staff-augmentation framework agreements; open requisitions for waves 1–2 (SQ-02 completion, SQ-03, SQ-04) | Programme Director | Day 15 | DP-V12-S-01; RECOMMENDATION-1111 |
| Appoint counsel panel (India first); send the 11 marketing packs (Part 11.15) for review | Growth/compliance lead | Day 30 | DP-V12-S-02; RECOMMENDATION-1113 |
| Open procurement track of Part 8.1 (SES, Anthropic terms, WABA, OAuth) plus IdP developer tenants, CRM developer orgs, DLT registrations | DevOps; IAM lead | Day 10 | DP-V12-S-06, S-07 |
| Record planned engineer-days per accepted story for the DEC-420 calibration | RTE | Every story from Day 1 | DEC-420 |
| Programme Director and RTE hired or contracted | Founder | Day 15 / Day 43 | §11.20.8.5 |

**Demo script (Fri 18 Dec) and acceptance.** (1) IaC plan applies to four environments with no drift. (2) A query through `app_rw` without `app.tenant_id` returns zero rows; a cross-tenant read is denied (two-tenant fixture). (3) The Data API returns 404 for application schemas; CI fails a branch that references `service_role` in runtime code. (4) Outbox delivers once under replay. (5) PDP denies by default. **Acceptance:** PO accepts each story with its evidence record; check 13 result recorded with ADR-255 fallback decision if it fails.

### 11.20.7.4 Sprint 1 (Mon 21 Dec 2026 – Fri 1 Jan 2027; Day 15–26)

**Sprint goal.** W0-B control set: BFF sign-in, secret references only, consent and suppression, model gateway with hard cost cap, point-in-time recovery switched on with its recovery path, and the catalogue core.

**Capacity.** 4.5 FTE × 7.53 × 0.8 × 0.95 × 0.7 = **18.0 pd ≈ 26 SP**. **Committed: 25.5 SP** (98%).

| Story | Title | Epic | Type | Priority | Points | SP mid | Owner (role) | Dependencies |
|---|---|---|---|---|---|---|---|---|
| US-0104 | Admin sign-in through the BFF | EP-01 | Feature (Security) | Must | 3–5 | 4.0 | FS + FE | US-0101 checks 1–3, 7, 12 |
| US-0112 | Integration registry with secret references | EP-01 | Feature (Security) | Must | 3–5 | 4.0 | BE + DevOps | US-0102, US-0110 |
| US-0301 | Consent ledger and suppression with immediate cancellation | EP-03 | Feature (Compliance) | Must | 3–5 | 4.0 | BE + FE | US-0107 |
| US-0401 | Model gateway skeleton and internal run API | EP-04 | Enabler | Must | 3–5 | 4.0 | FS (AI lead) | US-0112 |
| US-0404 | Cost reservation, hard caps, 80/100% alerts, emergency pause | EP-04 | Feature | Must | 3–5 | 4.0 | BE | US-0401 |
| US-0201 | Offering and capability editor with readiness lifecycle | EP-02 | Feature | Must | 3–5 | 4.0 | FS + FE | US-0107, US-0111 |
| US-21-ZR18 (part) | PITR enabled; `recovery_path` recorded; WAL archive bucket | EP-21 | Enabler (DR) | Must | 1–2 | 1.5 | DevOps | US-0102 |

**Demo (Thu 31 Dec, moved for the holiday).** BFF cookies only; registry never returns a secret; opt-out cancels queued items within 60 s; gateway rejects invalid output; simulated spend hits 100% and stops; PITR restore point listed. **Gate:** W0-B control set Tue 5 Jan 2027 (Day 30), as in Part 8.1.

### 11.20.7.5 Sprint 2 (Mon 4 Jan – Fri 15 Jan 2027; Day 29–40) and the DEC-420 calibration gate

**Sprint goal.** Complete W0-B: MFA step-up, claims approval, readiness gate, tier routing through the registry, injection guard, source register; place the Command Centre shell; seed the model registry (DEC-788) and the per-zone Vercel projects; **measure the AI-built net saving for the calibration gate.**

**Capacity.** 4.0 FTE × 7.53 × 1.0 × 0.95 = **28.6 pd ≈ 41 SP**. **Committed: 40.5 SP** (99%).

| Story | Title | Epic | Type | Priority | Points | SP mid | Owner (role) | Dependencies |
|---|---|---|---|---|---|---|---|---|
| US-0402 | Evaluation harness and CI regression gate | EP-04 | Enabler | Must | 3–5 | 4.0 | FS (AI lead) + QA | US-0401, US-0103 |
| US-1701 | Command Centre shell, seven-view navigation, scope selector | EP-17 | Feature | Must | 3–5 | 4.0 | FE | US-0104 |
| US-0105 | MFA step-up and session revocation | EP-01 | Security | Must | 2–3 | 2.5 | FS | US-0104 |
| US-0115 | Correlation IDs, structured logs, tracing | EP-01 | Observability | Must | 1–2 | 1.5 | DevOps + BE | US-0110 |
| US-0202 | Claim and price-version approval (hash-bound) | EP-02 | Feature | Must | 3–5 | 4.0 | FS + FE | US-0201, US-0105 |
| US-0205 | Readiness gate | EP-02 | Compliance | Must | 2–3 | 2.5 | FS | US-0202 |
| US-0403 + US-04-ZR22 (part) | Rules-first tier routing through registry-approved rows only | EP-04 | Security | Must | 3–5 | 4.0 | FS (AI lead) | US-0402 |
| US-0406 | Prompt-injection isolation and output guardrails | EP-04 | Security | Must | 2–3 | 2.5 | FS (AI lead) | US-0402 |
| US-0501 | Source permissions registry | EP-05 | Compliance | Must | 3–5 | 4.0 | BE + FE | US-0202 |
| US-0511 | Discovery fetcher sandbox (egress allowlist, SSRF) | EP-05 | Security | Must | 2–3 | 2.5 | DevOps + BE | US-0501 |
| US-04-ZR20 (part) | Model registry DDL, Claude Sonnet primary row (REG-002) with two-person approval | EP-04 | Enabler | Must | 2–3 | 2.5 | FS | US-0402 |
| US-21-ZR16 (part) | Per-zone Vercel projects `web-in`, `admin-in`, `developers`; functions pinned to Mumbai | EP-21 | Enabler | Must | 2–3 | 2.5 | DevOps | US-0102 |
| US-0502 | Research planner with scoped queries and budget | EP-05 | Feature | Must | 3–5 | 4.0 | BE | US-0501, US-0404 |

**Calibration gate (S2 review Fri 15 Jan 2027; decision by Thu 21 Jan 2027, Day 46).** Measured on accepted Sprint 1–2 scope: net saving = 1 − actual ÷ planned engineer-days; defects escaping to SIT ≤ plan + 20%; no unresolved critical or high security finding; review backlog < 2 days. The result selects the hiring path of §11.20.8.6 and is recorded as a new decision (DEC-420 requirement; template DEC-904).

### 11.20.7.6 Sprint-by-sprint plan S0–S45 (central effort; generated)

Columns: *Gross capacity* includes the sustain reserve; *Feature capacity* is after the IP-sprint halving and the sustain reserve; *Committed* is the package effort the scheduler places (pd ÷ 0.7). Package codes: R1-core = baseline Release 1 + CR-ALN-01 Musts; R1-V12 = V12 core platform, AI governance, UX and operations; R1-PD = identity, developer platform, connectors and platform decisions; R2A-cat = catalogue; R2A-ent = enterprise operations; R2B-P = mandates, commerce, payments, bids; R2B-Q = voice. Story allocation inside each package follows the release placement of the source part (for example Part 11.19b §11.19.5.12 for R1-PD, Part 11.16e §11.16.5.16.3 for INV-R1) and is fixed at each PI planning.

| Sprint | Dates (Mon–Fri) | Days | WD | PI | Squads | FTE squads + roles | Gross capacity pd | Feature capacity SP | Committed SP | Backlog themes (package pd) | Sustain / idle pd | Sprint goal | Milestone |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S0 | 07 Dec 2026 – 18 Dec 2026 | 1–12 | 10 | PI-0 | 1 | 4.5 + 0.5 | 23 | 32 | 32 | R0 23 | 0 | R0 W0-A foundation plus the V12 platform corrections: IaC for four environments, identity spike with check 13 (Okta, Entra ID, Google through the broker), CI gates, RLS, outbox, audit, flags, deny-by-default PDP, catalogue core; `app_rw` least-privilege role and Data API off (DEC-778); Vercel projects `web-in`, `admin-in`, `developers` | — |
| S1 | 21 Dec 2026 – 01 Jan 2027 | 15–26 | 8 | PI-0 | 1 | 4.5 + 0.5 | 18 | 26 | 26 | R0 18 | 0 | W0-B control set: BFF sign-in, integration registry, consent and suppression, model gateway, evaluation harness, hard cost caps, Command Centre shell; PITR on with `recovery_path` (DEC-787); registry seed rows; DDL-V12-R-01…04 | Gate W0-B control set Tue 5 Jan 2027 (Day 30) |
| S2 | 04 Jan 2027 – 15 Jan 2027 | 29–40 | 10 | PI-0 | 1 | 4.0 + 1.5 | 29 | 41 | 41 | R0 29 | 0 | W0-B completion and discovery core: MFA step-up, claims approval, readiness gate, tier routing, injection guard, source register to signals board; first measured AI-built throughput | **DEC-420 calibration gate: S2 review Fri 15 Jan 2027 (Day 40); decision by Thu 21 Jan 2027 (Day 46)** |
| S3 | 18 Jan 2027 – 29 Jan 2027 | 43–54 | 9 | PI-1 | 2 | 6.5 + 4.5 | 35 | 51 | 51 | R0 19, R1-core 17 | 0 | Close R0; start R1: SQ-02 onboarded (DEC-228 contract engineers); W1 qualification; SSO broker spike follow-up; standby + WAL-G design | **R0 gate Fri 29 Jan 2027 (Day 54)** |
| S4 | 01 Feb 2027 – 12 Feb 2027 | 57–68 | 10 | PI-1 | 3 | 11.5 + 6.5 | 62 | 89 | 89 | R1-core 44, R1-PD 18 | 0 | SQ-03 starts enterprise identity: SSO configuration and test login (US-01-ZR01), OAuth client credentials (US-20-ZR07); W0 admin tail, W1 imports, opt-out pages, SES adapter | Staff-augmentation wave 2 onboarding |
| S5 | 15 Feb 2027 – 26 Feb 2027 | 71–82 | 10 | PI-1 | 4 | 16.5 + 10.5 | 95 | 135 | 135 | R1-core 46, R1-PD 30, R1-V12 18 | 0 | SQ-04 starts AI platform: registry gates AU-150…153, prompt registry, scoped consent ledger AU-172; webhook engine (US-20-ZR08); connector framework and gate (US-18-ZR11); W2 engagement core | — |
| S6 | 01 Mar 2027 – 12 Mar 2027 | 85–96 | 10 | PI-1 | 4 | 19.5 + 10.5 | 123 | 176 | 176 | R1-core 57, R1-PD 36, R1-V12 30 | 0 | SCIM 2.0 (US-01-ZR03); SMS-DLT and Zoho CRM; first restore drill (RPO ≤ 15 min, RTO ≤ 120 min); EVAL-PRG-1 suites; W2 outreach and meetings | First restore drill |
| S7 | 15 Mar 2027 – 26 Mar 2027 | 99–110 | 8 | PI-1 | 5 | 24.5 + 11.5 | 117 | 167 | 167 | R1-core 49, R1-V12 41, R1-PD 27 | 0 | SQ-05 starts: tenancy re-model and portfolio grants, hierarchy, common workflow engine (D-1), catalogue registry (E9); custom roles and SoD (US-01-ZR04); HubSpot; website publication pipeline | — |
| S8 | 29 Mar 2027 – 09 Apr 2027 | 113–124 | 10 | PI-1 (IP) | 5 | 24.5 + 11.5 | 81 | 115 | 115 | R1-core 32, R1-V12 31, R1-PD 17 | 0 | IP sprint PI-1: PI-2 planning, hardening, DR drill; SIEM and audit export (US-01-ZR05); SDK 1.0 RC; i18n framework and pseudo-locale CI | PI-2 planning Thu–Fri 8–9 Apr 2027 |
| S9 | 12 Apr 2027 – 23 Apr 2027 | 127–138 | 10 | PI-2 | 6 | 30.0 + 15.5 | 187 | 267 | 267 | R1-core 68, R1-V12 68, R1-PD 34, R2A-cat 17 | 0 | SQ-06 starts; QA infrastructure TASK-V12-J-001…014 and first H-class SKUs; W3 omnichannel; Salesforce adapter; voice transport connector (US-22-ZR15) | — |
| S10 | 26 Apr 2027 – 07 May 2027 | 141–152 | 10 | PI-2 | 6 | 30.0 + 15.5 | 199 | 284 | 284 | R1-core 68, R1-V12 68, R1-PD 34, R2A-cat 29 | 0 | W3 marketing close-out; Command Centre 14 views; SLA, SEV clocks and status page (K); regional Vercel and header allowlist (US-21-ZR16/17); pen-test vendor confirmed | India marketing packs to counsel (RP-IN-*) |
| S11 | 10 May 2027 – 21 May 2027 | 155–166 | 10 | PI-2 | 7 | 35.0 + 19.5 | 221 | 316 | 316 | R1-core 68, R1-V12 68, R2A-cat 39, R1-PD 29, R2B-P 17 | 0 | SQ-07 starts mandate engine core (MND), two-person approval; R1 commercial core (W4 pricing, quotes); evaluation suites for R1 agents | — |
| S12 | 24 May 2027 – 04 Jun 2027 | 169–180 | 10 | PI-2 | 8 | 40.0 + 20.2 | 242 | 346 | 346 | R1-V12 93, R2A-cat 66, R1-core 38, R2B-P 28, R2B-Q 16 | 0 | SQ-08 starts voice gateway and ports; R1 scope freeze (start of S12, Day 169); R1 V12 core completion; W4 closure baseline (R2-A) starts | R1 scope freeze Mon 24 May 2027 |
| S13 | 07 Jun 2027 – 18 Jun 2027 | 183–194 | 10 | PI-2 | 8 | 40.0 + 20.2 | 258 | 369 | 369 | R1-V12 95, R2A-cat 69, R2A-base 33, R2B-P 33, R2B-Q 28 | 0 | R1 build complete: residency choice at onboarding (US-01-ZR28), DLT live, India pack approved, VD-01…12 green for 30 days; UAT and pen test 1 (incl. SSO, SCIM, developer host, webhooks) | R1 build complete Fri 18 Jun 2027 |
| S14 | 21 Jun 2027 – 02 Jul 2027 | 197–208 | 10 | PI-2 (IP) | 8 | 40.0 + 20.2 | 132 | 169 | 169 | R2A-cat 74, R2A-base 15, R2B-P 15, R2B-Q 15 | 13 | IP sprint PI-2 and R1 hardening: go/no-go evidence (GNG-R-01…10), restore drill at the gate, PI-3 planning; catalogue H-class SKUs continue | **R1 go/no-go Fri 2 Jul 2027 (Day 208)** |
| S15 | 05 Jul 2027 – 16 Jul 2027 | 211–222 | 10 | PI-3 | 8 | 40.0 + 20.2 | 263 | 338 | 338 | R2A-cat 148, R2A-base 30, R2B-P 30, R2B-Q 30 | 26 | R1 hypercare; R2-A catalogue H-class SKUs at full flow; W4 closure (proposal, bids, orders, payments evidence); mandate PDP rules 0–14 and ledger | R1 hypercare (4 weeks) |
| S16 | 19 Jul 2027 – 30 Jul 2027 | 225–236 | 10 | PI-3 | 9 | 45.0 + 21.2 | 280 | 360 | 360 | R2A-cat 148, R2A-base 30, R2B-P 30, R2B-Q 30, INV1 15 | 28 | SQ-09 starts Investment Automation boundary (`inv` schema, AU-200, R21/R10C); M-class SKUs; PSP adapters design; voice ASR/TTS ports | INV counsel engagement opened (IN first) |
| S17 | 02 Aug 2027 – 13 Aug 2027 | 239–250 | 10 | PI-3 | 9 | 45.0 + 21.2 | 291 | 374 | 374 | R2A-cat 148, R2A-base 30, R2B-P 30, R2B-Q 30, INV1 25 | 29 | Catalogue M-class SKUs and billing (E14–E18); INV storefront W55–W74 and AU-228; voice agents AG-210…219; negotiation bound engine | — |
| S18 | 16 Aug 2027 – 27 Aug 2027 | 253–264 | 10 | PI-3 | 10 | 50.0 + 25.2 | 313 | 402 | 402 | R2A-cat 148, R2B-P 30, R2B-Q 30, INV1 30, R3 28, R2A-ent 15, R2A-base 1 | 31 | SQ-10 starts R2-A enterprise operations (24×7 runbooks, NOC/SOC onboarding, 99.95% topology ADR) and the R3 EU stack (IaC second stamp, residency router); N-class SKUs | NOC/SOC vendor contract signed |
| S19 | 30 Aug 2027 – 10 Sep 2027 | 267–278 | 10 | PI-3 | 10 | 50.0 + 25.2 | 324 | 417 | 417 | R2A-cat 148, R3 30, R2B-P 30, R2B-Q 30, INV1 30, R2A-ent 25 | 32 | SOC 2 readiness assessment; N-class SKUs; payments settlement sub-ledger; bid sealing and portal adapters; INV-SVC-01…03 | — |
| S20 | 13 Sep 2027 – 24 Sep 2027 | 281–292 | 10 | PI-3 (IP) | 10 | 50.0 + 25.2 | 165 | 212 | 212 | R2A-cat 74, R3 15, R2B-P 15, R2B-Q 15, INV1 15, R2A-ent 15 | 16 | IP sprint PI-3: PI-4 planning, DR drill, R2-A UAT preparation; catalogue completion | PI-4 planning |
| S21 | 27 Sep 2027 – 08 Oct 2027 | 295–306 | 10 | PI-4 | 10 | 50.0 + 25.2 | 329 | 423 | 387 | R2A-cat 93, INV1 59, R3 47, R2B-P 30, R2B-Q 30, R2A-ent 12 | 58 | R2-A build complete (Fri 8 Oct 2027): 39 SKUs, 156 workflows, billing, screens; SQ-11 starts A1 (DEC-417); R2-A UAT; SOC 2 Type I fieldwork | R2-A build complete |
| S22 | 11 Oct 2027 – 22 Oct 2027 | 309–320 | 10 | PI-4 | 11 | 55.0 + 25.2 | 357 | 434 | 434 | R3 112, INV1 56, A1 52, R2B-P 39, INV2 28, R2B-Q 17 | 54 | R2-A hardening: pen test 2, 24×7 go-live rehearsal and paging test, Enterprise-tier failover test; R3 EU stack; A1 build; INV-SVC-04…08 | — |
| S23 | 25 Oct 2027 – 05 Nov 2027 | 323–334 | 9 | PI-4 | 11 | 55.0 + 25.2 | 326 | 396 | 341 | R3 62, A1 50, INV1 50, R2B-P 50, INV2 25 | 87 | R3 EU build complete; INV-R2 build (INV-SVC-13…16); A1 build; R2-B voice completion | **R2-A gate Fri 5 Nov 2027 (Day 334)**: catalogue GA, 24×7 live, SOC 2 Type I report; SOC 2 Type II window opens |
| S24 | 08 Nov 2027 – 19 Nov 2027 | 337–348 | 10 | PI-4 | 11 | 55.0 + 23.2 | 362 | 440 | 400 | A1 84, R4 56, INV1 56, R2B-P 56, INV2 28 | 82 | R4 global build: four region stamps from the EU template, tax engine TX-04…09, de/fr/ar locales, BYOK multi-cloud (I D7); INV-SVC-09…12 | **R3-a EU region ready Fri 19 Nov 2027 (Day 348)** |
| S25 | 22 Nov 2027 – 03 Dec 2027 | 351–362 | 10 | PI-4 | 11 | 55.0 + 23.2 | 362 | 440 | 364 | A1 84, R4 82, INV1 56, INV2 28, R2B-P 5 | 107 | R2-B build complete (Fri 3 Dec 2027): mandates, commerce, payments, bids, voice; R4 build complete; SQ-03, SQ-07, SQ-08, SQ-10 released to sustain | R2-B build complete |
| S26 | 06 Dec 2027 – 17 Dec 2027 | 365–376 | 10 | PI-4 (IP) | 7 | 35.0 + 21.2 | 119 | 144 | 124 | A1 43, INV1 29, INV2 14 | 32 | IP sprint PI-4: R2-B UAT, agent-gateway and voice pen tests, counsel UAT per jurisdiction; PI-5 planning | **R4-a global build ready Fri 17 Dec 2027 (Day 376)** |
| S27 | 20 Dec 2027 – 31 Dec 2027 | 379–390 | 10 | PI-5 | 7 | 35.0 + 21.2 | 238 | 289 | 248 | A1 87, INV1 58, INV2 29 | 65 | Year-end change freeze 24 Dec–2 Jan (no production change); INV-R1 completion, INV-R2 and A1 build | Change freeze |
| S28 | 03 Jan 2028 – 14 Jan 2028 | 393–404 | 10 | PI-5 | 7 | 35.0 + 21.2 | 238 | 289 | 248 | A1 87, INV2 69, INV1 18 | 65 | INV-R1 build complete (Fri 14 Jan 2028); INV-R2 and A1 build | **R2-B gate Fri 14 Jan 2028 (Day 404)**; activation per jurisdiction as packs are signed |
| S29 | 17 Jan 2028 – 28 Jan 2028 | 407–418 | 9 | PI-5 | 7 | 35.0 + 21.2 | 214 | 260 | 185 | INV2 78, A1 51 | 85 | A1 build complete (Fri 28 Jan 2028); INV-R2 completion; SQ-02 released | — |
| S30 | 31 Jan 2028 – 11 Feb 2028 | 421–432 | 10 | PI-5 | 6 | 30.0 + 19.2 | 204 | 248 | 208 | A2 87, INV2 59 | 58 | INV-R2 build complete (Fri 11 Feb 2028); A2 build starts (DEC-905); SQ-06 and SQ-09 released | **INV-R1 gate Fri 11 Feb 2028 (Day 432)** (IN activation only after RP-IN-SEC signed) |
| S31 | 14 Feb 2028 – 25 Feb 2028 | 435–446 | 10 | PI-5 | 4 | 20.0 + 14.8 | 143 | 174 | 174 | A2 122 | 21 | A2 build: next-best action, deal risk, ABM, intent hub, AI improvement A2 items | **A1 gate Fri 25 Feb 2028 (Day 446)**; G-A1 KPI window opens |
| S32 | 28 Feb 2028 – 10 Mar 2028 | 449–460 | 10 | PI-5 (IP) | 4 | 20.0 + 14.8 | 72 | 87 | 87 | A2 61 | 11 | IP sprint PI-5: A2 build; INV-R2 hypercare; PI-6 planning | **INV-R2 gate Fri 10 Mar 2028 (Day 460)** |
| S33 | 13 Mar 2028 – 24 Mar 2028 | 463–474 | 10 | PI-6 | 4 | 20.0 + 14.8 | 143 | 174 | 174 | A2 122 | 21 | A2 build: deal rooms, partners, health and QBR, semantic layer | — |
| S34 | 27 Mar 2028 – 07 Apr 2028 | 477–488 | 10 | PI-6 | 4 | 20.0 + 14.8 | 143 | 174 | 174 | A2 122 | 21 | A2 build: NL analytics, FinOps, compliance evidence; G-A1 decision | G-A1 (A1 KPIs met for 30 days) |
| S35 | 10 Apr 2028 – 21 Apr 2028 | 491–502 | 9 | PI-6 | 4 | 20.0 + 14.8 | 129 | 156 | 114 | A2 80 | 49 | A2 build complete (Fri 21 Apr 2028); A3 preparation | — |
| S36 | 24 Apr 2028 – 05 May 2028 | 505–516 | 10 | PI-6 | 4 | 20.0 + 14.8 | 143 | 174 | 174 | A3 122 | 21 | A3 build: conversation intelligence, marketing mix, no-code builder, AI improvement A3 (swarm, SDR assistant) | — |
| S37 | 08 May 2028 – 19 May 2028 | 519–530 | 10 | PI-6 | 4 | 20.0 + 14.8 | 143 | 174 | 174 | A3 122 | 21 | A3 build; R3 certification close-out | **A2 gate and R3 exit Fri 19 May 2028 (Day 530)**: SOC 2 Type II report and ISO 27001 certificate |
| S38 | 22 May 2028 – 02 Jun 2028 | 533–544 | 10 | PI-6 (IP) | 4 | 20.0 + 14.8 | 72 | 87 | 87 | A3 61 | 11 | IP sprint PI-6: A3 build; independent red-team before A3 enablement (M-D5); PI-7 planning | — |
| S39 | 05 Jun 2028 – 16 Jun 2028 | 547–558 | 10 | PI-7 | 4 | 20.0 + 14.8 | 143 | 174 | 174 | A3 122 | 21 | A3 build: CDP streaming, enablement coach | ISO 27701 / 42001 Stage 1 audits |
| S40 | 19 Jun 2028 – 30 Jun 2028 | 561–572 | 10 | PI-7 | 4 | 20.0 + 14.8 | 143 | 174 | 75 | A3 53 | 90 | A3 build complete (Fri 30 Jun 2028); SQ-01 and SQ-05 move to the sustain team | — |
| S41 | 03 Jul 2028 – 14 Jul 2028 | 575–586 | 10 | PI-7 | 2 | 10.0 + 12.8 | 72 | 87 | 79 | A4 55 | 16 | A4 build complete (Fri 14 Jul 2028): AI improvement A4 (marketplace package format, gallery) | Build of the programme complete |
| S42 | 17 Jul 2028 – 28 Jul 2028 | 589–600 | 10 | PI-7 | sustain | sustain team (running) | — | — | — | — | — | Sustain team: A3 hypercare, ISO 27701/42001 evidence; no new build | **A3 gate Fri 28 Jul 2028 (Day 600)** |
| S43 | 31 Jul 2028 – 11 Aug 2028 | 603–614 | 10 | PI-7 | sustain | sustain team (running) | — | — | — | — | — | Sustain team: ISO 27701/42001 Stage 2 audits; A4 KPI window | — |
| S44 | 14 Aug 2028 – 25 Aug 2028 | 617–628 | 9 | PI-7 (IP) | sustain | sustain team (running) | — | — | — | — | — | Sustain team: programme close-out pack, benefits review preparation | **A4 gate Fri 25 Aug 2028 (Day 628)** |
| S45 | 28 Aug 2028 – 08 Sep 2028 | 631–642 | 10 | PI-8 | sustain | sustain team (running) | — | — | — | — | — | Sustain team: R4 certification close; programme closure and benefits review | **R4 exit Fri 8 Sep 2028 (Day 642)**: ISO 27701 and 42001 certificates; programme close |
| **Total S0–S41** | | | | | | | **7550** | **9679** | **9106** | 6,374 pd central = 9,106 SP | | | |

### 11.20.7.7 Programme increment calendar

| PI | Sprints | Dates | PI planning (in the preceding IP sprint) | Main PI objectives |
|---|---|---|---|---|
| PI-0 | S0–S2 | 7 Dec 2026 – 15 Jan 2027 | Sprint 0 planning Mon 7 Dec 2026 | R0 controls; calibration |
| PI-1 | S3–S8 | 18 Jan – 9 Apr 2027 | Thu–Fri 14–15 Jan 2027 | R0 gate; R1 identity, developer platform, connectors; V12 core; W1–W2 |
| PI-2 | S9–S14 | 12 Apr – 2 Jul 2027 | Thu–Fri 8–9 Apr 2027 | R1 build complete and gate; catalogue start; mandate and voice engines start |
| PI-3 | S15–S20 | 5 Jul – 24 Sep 2027 | Wed–Thu 30 Jun – 1 Jul 2027 | Catalogue at full flow; INV boundary; 24×7 set-up; EU stack |
| PI-4 | S21–S26 | 27 Sep – 17 Dec 2027 | Thu–Fri 23–24 Sep 2027 | R2-A gate; R3-a; R4-a; R2-B build; A1 start |
| PI-5 | S27–S32 | 20 Dec 2027 – 10 Mar 2028 | Wed–Thu 15–16 Dec 2027 | R2-B gate; INV-R1, INV-R2; A1 gate; A2 build |
| PI-6 | S33–S38 | 13 Mar – 2 Jun 2028 | Wed–Thu 8–9 Mar 2028 | A2 gate; R3 exit; A3 build |
| PI-7 | S39–S44 | 5 Jun – 25 Aug 2028 | Thu–Fri 1–2 Jun 2028 | A3, A4; ISO 27701/42001; R4 exit (S45) |

### 11.20.7.8 If capacity is short: the no-scope-cut ladder (DEC-770, DEC-912)

| Step | Trigger | Action | Approver |
|---|---|---|---|
| 1 | 3-sprint rolling capacity < 90% of plan for any squad | Rebalance queues across squads at the next PI planning; move non-gating stories within the release | RTE |
| 2 | Release forecast slips ≥ 1 sprint | Add contract FTE to the constrained squad (up to 7 per squad) | Founder via CCB |
| 3 | Slip ≥ 2 sprints or a new release package | Add a squad (≈ ₹8.5 L per month central, §11.20.9.1) | Founder via CCB; change request under DEC-790 |
| 4 | Capacity cannot be bought in time | Move the gate date; re-forecast budgets; inform stakeholders (§11.20.12) | Founder (DEC-770) |
| — | Never | Remove a Must, compliance, security, mandate, residency or rule-pack control from a release | — |

---

## 11.20.8 Team scaling plan

### 11.20.8.1 Delivery model (DEC-420 AI-built squads)

| Element | Rule in this plan |
|---|---|
| Squad | Five engineering FTE in velocity (tech lead, three engineers, one QA automation engineer), stream-aligned to one release package family; SRE and security as enabling teams (ADR-265) |
| AI-built practice | Every squad works with AI models and agents for drafting code, tests, fixtures and documentation under the DEC-420 operating model; humans own architecture, security, PDP, money, mandates, residency and AI guardrails |
| Quality guard | Second human reviewer from the owning squad for protected areas; provenance log per merge; agent sandboxes with synthetic data only |
| Ownership | One owner per capability (overlap register, ADR-268); shared components (PDP, MND, registry, entitlement ledger) have a single owning squad and published contracts |
| Staffing source | SQ-01 employed (team of record); all other squads from two staff-augmentation vendors at contract rates, with knowledge transfer to SQ-01 before release to sustain |
| Sustain | From the end of the build (S42), SQ-01 plus one contract squad (10 FTE) run maintenance and minor enhancements (running line B-S33) alongside the 24×7 rota |

### 11.20.8.2 Squads

| Squad | Mission | Start (sprint, date) | Released to sustain (central) | Staffing | FTE in velocity | Queue (packages in order) | Composition (5.0 FTE standard) |
|---|---|---|---|---|---|---|---|
| SQ-01 | Core Platform (team of record) | S0 Mon 7 Dec 2026 | S40 Fri 30 Jun 2028 | employee | 4.5 from S0, 4.0 from S2, 4.5 from S3, 5.0 from S9 | R0, R1-core, R2A-base, R3, A2, A3 | Team of record (DEC-005/232): BE, FS (Principal Engineer, AI lead), FE, QA 1.0, DevOps 0.5; becomes the sustain core |
| SQ-02 | Core Delivery (DEC-228 contract engineers, extended) | S3 Mon 18 Jan 2027 | S29 Fri 28 Jan 2028 | contract | 2.0 from S3, 5.0 from S6 | R0, R1-core, R1-V12, R2A-cat, R3, A1 | 2 contract engineers (DEC-228) + 3 from wave 3: tech lead, 2 full-stack, 1 backend, 1 QA automation |
| SQ-03 | Identity and Developer Platform | S4 Mon 1 Feb 2027 | S25 Fri 3 Dec 2027 | contract | 5.0 from S4 | R0, R1-PD, R2A-cat, R3, R4 | IAM tech lead, 2 backend (SAML/OIDC, SCIM), 1 integration engineer, 1 QA automation |
| SQ-04 | AI Platform and Evaluation | S5 Mon 15 Feb 2027 | S41 Fri 14 Jul 2028 | contract | 5.0 from S5 | R1-V12, R2A-cat, A1, A2, A3, A4 | LLM platform lead, 2 AI/LLM engineers, 1 evaluation engineer, 1 backend |
| SQ-05 | Catalogue and Billing I | S7 Mon 15 Mar 2027 | S40 Fri 30 Jun 2028 | contract | 5.0 from S7 | R1-V12, R2A-cat, INV2, A2, A3 | Tech lead, 2 backend (billing, ledgers), 1 frontend, 1 QA automation |
| SQ-06 | Catalogue Services II | S9 Mon 12 Apr 2027 | S30 Fri 11 Feb 2028 | contract | 5.0 from S9 | R2A-cat, INV1, INV2 | Tech lead, 2 full-stack, 1 frontend, 1 QA automation |
| SQ-07 | Autonomy, Commerce and Bids | S11 Mon 10 May 2027 | S25 Fri 3 Dec 2027 | contract | 5.0 from S11 | R2B-P, R4 | Payments tech lead, 2 backend (PSP, ledger), 1 security-minded backend, 1 QA automation |
| SQ-08 | Voice and Recordings | S12 Mon 24 May 2027 | S25 Fri 3 Dec 2027 | contract | 5.0 from S12 | R2B-Q, R2B-P, R4 | Real-time media lead, 2 backend (voice gateway, ports), 1 AI engineer, 1 QA automation |
| SQ-09 | Investment Automation | S16 Mon 19 Jul 2027 | S30 Fri 11 Feb 2028 | contract | 5.0 from S16 | INV1, INV2 | Tech lead, 2 full-stack, 1 backend (securities controls), 1 QA automation |
| SQ-10 | Regions, Resilience and Compliance | S18 Mon 16 Aug 2027 | S25 Fri 3 Dec 2027 | contract | 5.0 from S18 | R2A-ent, R3, R4 | SRE lead, 2 platform/SRE engineers, 1 security engineer, 1 backend (tax, regions) |
| SQ-11 | Advanced Intelligence (DEC-417 A1 team) | S21 Mon 27 Sep 2027 | S41 Fri 14 Jul 2028 | contract | 5.0 from S21 | A1, A2, A3, A4 | AI lead, 2 AI/LLM engineers, 1 data engineer, 1 SRE/security engineer (ASSUMPTION-700, DEC-417) |

### 11.20.8.3 Programme roles outside velocity

| Programme role (outside velocity) | FTE at peak (S22) | Rate class | From sprint | Scaling rule |
|---|---|---|---|---|
| Growth/compliance lead (DEC-232) | 0.75 | employee | S0 | 0.5, 0.75 from S12 (DEC-232) |
| Programme Director | 1.00 | lead | S2 | 1.0 throughout |
| Release Train Engineer | 1.00 | lead | S3 | 1.0; 0.5 in the A-release tail |
| Principal / enterprise architects | 2.00 | lead | S3 | 1.0, 2.0 from S9; 1.0 in the tail |
| Delivery leads / scrum masters | 4.00 | mid | S3 | one per three squads |
| Domain product owners | 4.00 | lead | S4 | one per three squads; the Founder is chief PO (not charged) |
| Security engineering (AppSec, cloud, IAM) | 3.00 | lead | S4 | 1.0, 2.0 from S11, 3.0 from S18; 2.0 in the tail |
| DBRE / data architect | 1.00 | lead | S5 | 1.0; 0.5 in the tail |
| UX / product design | 2.00 | mid | S5 | 1.0, 2.0 from S9; 1.0 in the tail |
| QA lead / test architect | 1.00 | lead | S7 | 1.0 |
| SRE / operations engineering | 2.00 | lead | S9 | 1.0, 2.0 from S18; after the R2-A gate paid through the DEC-773 running line |
| Technical writer / training | 1.00 | mid | S9 | 1.0; 0.5 in the tail |
| Compliance analysts (R10 delegates) | 2.00 | mid | S11 | 1.0, 2.0 from S16 (securities, payments, voice) |
| FinOps analyst | 0.50 | mid | S12 | 0.5 |
| **Total programme roles at peak** | **25.25** | | | |

### 11.20.8.4 FTE per phase

| Phase | Sprints | Calendar | Squads active | Average velocity FTE | Peak velocity FTE | Average programme roles FTE | Peak total FTE | FTE-months |
|---|---|---|---|---|---|---|---|---|
| Phase 0 Foundation (R0) | S0–S2 | 07 Dec 2026 – 15 Jan 2027 | 1–1 | 4.3 | 4.5 | 0.8 | 5.5 | 7 |
| PI-1 | S3–S8 | 18 Jan 2027 – 09 Apr 2027 | 2–5 | 17.2 | 24.5 | 9.2 | 36.0 | 73 |
| PI-2 (R1 gate) | S9–S14 | 12 Apr 2027 – 02 Jul 2027 | 6–8 | 35.8 | 40.0 | 18.5 | 60.2 | 150 |
| PI-3 | S15–S20 | 05 Jul 2027 – 24 Sep 2027 | 8–10 | 46.7 | 50.0 | 23.1 | 75.2 | 193 |
| PI-4 (R2-A, R3-a, R4-a) | S21–S26 | 27 Sep 2027 – 17 Dec 2027 | 7–11 | 50.8 | 55.0 | 23.9 | 80.2 | 207 |
| PI-5 (R2-B, INV, A1) | S27–S32 | 20 Dec 2027 – 10 Mar 2028 | 4–7 | 29.2 | 35.0 | 18.8 | 56.2 | 132 |
| PI-6 (A2, R3 exit) | S33–S38 | 13 Mar 2028 – 02 Jun 2028 | 4–4 | 20.0 | 20.0 | 14.8 | 34.8 | 96 |
| PI-7 (A3, A4) | S39–S41 | 05 Jun 2028 – 14 Jul 2028 | 2–4 | 16.7 | 20.0 | 14.1 | 34.8 | 42 |
| **Programme** | S0–S41 | 07 Dec 2026 – 14 Jul 2028 | 1–11 | 30.0 | **55.0** | 16.5 | **80.25 (S22)** | **900** |

**Team peak: 80.25 FTE in Sprint 22 (11–22 Oct 2027)** = 55 engineering FTE in eleven squads + 25.25 programme roles, plus the contracted NOC/SOC first line, counsel and auditors outside the headcount.

### 11.20.8.5 Hiring sequence

Lead times assume staff augmentation (2–6 weeks per profile after the framework agreements) [ASSUMPTION-1109]; each wave is requested one PI ahead.

| Wave | Who | FTE | Start (sprint, date) | Requisition by | Gated by |
|---|---|---|---|---|---|
| 0 | Team of record SQ-01; growth/compliance lead | 4.5 + 0.5 | S0 Mon 7 Dec 2026 | In place | DEC-228/232 |
| 0 | Programme Director | 1.0 | S2 Mon 4 Jan 2027 | Day 1 | DEC-903 |
| 1 | SQ-02 first two contract engineers (DEC-228); RTE; principal architect; first scrum master | 2.0 + 3.0 | S3 Mon 18 Jan 2027 | Day 1 | DEC-228 |
| 2 | SQ-03 identity and developer platform | 5.0 | S4 Mon 1 Feb 2027 | Day 1 | DEC-784/785 (Release 1) |
| 2 | SQ-04 AI platform; domain POs; security engineer; DBRE; UX designer | 5.0 + 4.0 | S4–S5 | Day 15 | DEC-788 |
| **Gate** | **DEC-420 calibration** | — | Decision Thu 21 Jan 2027 | — | Confirms waves 3–6 (§11.20.8.6) |
| 3 | SQ-02 to 5 FTE; SQ-05 catalogue and billing; QA lead | 3.0 + 5.0 + 1.0 | S6–S7 | Day 40 | Calibration result |
| 3 | SQ-06 catalogue services II; second architect; second UX; SRE; technical writer | 5.0 + 4.0 | S9 Mon 12 Apr 2027 | Day 60 | Calibration result (not hired under option A) |
| 4 | SQ-07 autonomy and commerce; SQ-08 voice; compliance analyst; second security engineer; FinOps analyst | 10.0 + 2.5 | S11–S12 | Day 100 | DEC-779…782 |
| 5 | SQ-09 investment; SQ-10 regions and compliance; second compliance analyst; third security engineer; second SRE | 10.0 + 3.0 | S16–S18 | Day 170 | DEC-772…776, DEC-783 |
| 5 | NOC/SOC vendor contract | vendor | S18 | Day 170 | DEC-773 |
| 6 | SQ-11 advanced intelligence (A1 team, ASSUMPTION-700) | 5.0 | S21 Mon 27 Sep 2027 | Day 240 | DEC-417; R2-A gate − 2 sprints |
| Ramp-down | SQ-03, SQ-07, SQ-08, SQ-10 → sustain or release | −20.0 | after S25 (Fri 3 Dec 2027) | — | Queues complete |
| Ramp-down | SQ-02 after S29; SQ-06, SQ-09 after S30; SQ-01, SQ-05 after S40; SQ-04, SQ-11 after S41 | — | Jan–Jul 2028 | — | Queues complete; SQ-01 + one squad stay as sustain |

### 11.20.8.6 DEC-420 calibration gate in the scaling plan

```mermaid
flowchart TD
  A["Sprint 1 and 2 accepted scope<br/>planned vs actual engineer-days"] --> B{"Quality guards hold<br/>defects, security, review backlog"}
  B -- "No" --> C["Plan of record<br/>fix the guard, re-measure at S5"]
  B -- "Yes" --> D{"Net saving"}
  D -- "below 10 percent" --> E["Plan of record<br/>revert to DEC-419 tooling"]
  D -- "10 to 20 percent" --> F["Plan of record<br/>keep AI tooling"]
  D -- "20 percent or more" --> G{"Founder chooses"}
  G -- "Option A, default" --> H["Keep dates<br/>do not hire SQ-06"]
  G -- "Option B" --> I["Keep team<br/>bring gates forward"]
  H --> J["Record the decision<br/>update Ledger A by change control"]
  I --> J
  C --> J
  E --> J
  F --> J
```

| Outcome | Hiring effect | Dates (model) | People cost ₹ L (central rates) |
|---|---|---|---|
| < 20% or guards fail | Waves 3–6 as planned | Plan of record (R1 Day 208, R2-A Day 334, close Day 642) | 1,607.9 |
| ≥ 20%, option A | SQ-06 not hired; its queue moves to SQ-05 | R1 Day 194; R2-A Day 320; INV-R2 Day 474 (+2 weeks); close Day 628 | 1,424.4 |
| ≥ 20%, option B | All waves | R1 Fri 18 Jun 2027 (Day 194); R2-A Fri 22 Oct 2027 (Day 320); close Fri 25 Aug 2028 (Day 628) | 1,384.0 |

The calibration is repeated at each Inspect-and-Adapt; a later result can only release capacity in the next wave, never remove a control.

### 11.20.8.7 Business UAT participants per release [GAP-1117]

| Release | UAT window (central) | Packs | Participants (persona) | Participant-days high / low |
|---|---|---|---|---|
| R1 | S12–S13 | Part 8.1 W0–W3 packs; SSO/SCIM with two enterprise IT administrators; developer pilot with two integrators; CRM and SMS connector pilots | Part 8.1 §8.1.5.4 participants + R12 IT admins (2), developer partners (2) | 130 / 65 |
| R2-A | S21–S22 | UAT-PK-SC, UAT-PK-FIN, 39 SKU acceptance (Service Owner 0.5 day per SKU), billing and credits | Tenant admins (4), finance maker and checker (2), Service Owner, DPO | 60 / 30 |
| R2-B | S25–S26 | Mandates, payments, bids, voice packs per jurisdiction | Finance (2), bid manager, voice supervisors (2), DPO, counsel (advisory) | 35 / 18 |
| INV-R1 / INV-R2 | S28–S29; S30–S31 | Issuer admin, R21, R10C, counsel UAT per jurisdiction | Issuer admins (2), compliance (2), counsel | 30 / 15 |
| R3-a / R4-a | S24; S26 | EU tenant pilot; one market pilot per region | EU tenant admins (2), market leads (4) | 24 / 12 |
| A1–A4 | Each A build end | Agent evaluation packs | Startup heads, growth managers | 40 / 20 |
| **Total** | | | | **319 / 160** |

### 11.20.8.8 RACI across the train

R = responsible, A = accountable (one per row), C = consulted, I = informed.

| Activity | Founder/PO | Programme Director | RTE | Principal Architect | Domain POs | Squad tech leads | QA lead | Security lead | SRE lead | Legal/DPO and counsel | Finance/FinOps |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Release scope and gate decision | A | R | C | C | R | C | R | R | R | R | C |
| PI planning and programme board | C | A | R | C | R | R | C | C | C | I | I |
| Architecture runway, ADRs, sequencing | A | C | C | R | C | R | C | C | C | I | I |
| Capacity, hiring waves, vendors | A | R | C | C | I | C | C | I | C | I | R |
| DEC-420 calibration and tooling | A | R | R | C | I | R | R | C | I | I | C |
| Counsel rule-pack sign-off and activation | C | I | I | I | C | I | C | C | I | A / R | I |
| Certification (SOC 2, ISO) | A | C | I | C | I | C | C | R | R | C | C |
| 24×7 operations and incidents | A | I | I | C | I | C | I | R | R | C | I |
| Budget re-forecast per sprint | A | R | C | I | I | I | I | I | C | I | R |
| Change control (CCB) | A | R | R | C | C | C | C | C | C | C | C |
| Risk register and RAID | A | R | R | C | C | C | C | R | C | C | C |

---

## 11.20.9 Budget

### 11.20.9.1 Rates and conventions

| Parameter | Value | Source |
|---|---|---|
| Employee engineer | ₹1.0 / 1.25 / 1.5 L per FTE-month (L / C / H) | BRD §6; Part 8.4 |
| Contract engineer | ₹1.2 / 1.5 / 1.8 L | ASSUMPTION-202 |
| Lead, architect, security, PO, programme roles | ₹2.0 / 2.5 / 3.0 L [ASSUMPTION-1107] | Market practice; verify quotes |
| Mid programme roles (scrum master, UX, writer, compliance analyst, FinOps) | ₹1.2 / 1.5 / 1.8 L | As contract |
| Contract squad (4 engineers + 1 lead) | ₹6.8 / 8.5 / 10.2 L per month | Formula |
| Sprint | 14 ÷ 30.4 = 0.46 month | Part 8.4 convention |
| Effort value | pd × ₹4,545 / 5,682 / 6,818 | Part 8.4 |
| Budget bands | **Rate band** on the plan-of-record schedule (low / central / high rates); **effort risk** shown separately (§11.20.9.9) | DEC-910 |
| Excluded | GST, Founder time, recruitment fees beyond the contract-rate premium, customer-funded tenant usage, PSP and marketplace pass-through fees | Part 8.4 |
| Prices | All provider, auditor, counsel and tool prices: **estimates; verify at time of implementation (as of 27 Nov 2026)** | — |

### 11.20.9.2 Development cost (one-time) by release

People cost is allocated to a release in proportion to the package effort each squad delivered in each sprint; capacity held for production support, gate windows and hypercare is shown as its own line, because it is real cash that belongs to no single release.

| Release | Gate of record | People cost ₹ L L / C / H | External one-time ₹ L L / C / H | **Development total ₹ L L / C / H** | Effort value ₹ L L / C / H (pd × rate) |
|---|---|---|---|---|---|
| R0 Foundation | Fri 29 Jan 2027 (Day 54) | 11.2 / 14.0 / 16.8 | 0.0 / 0.0 / 0.0 | **11.2 / 14.0 / 16.8** | 2.9 / 5.0 / 7.8 |
| R1 Core + enterprise identity + developer platform | Fri 2 Jul 2027 (Day 208) | 216.7 / 270.9 / 325.0 | 6.5 / 10.9 / 15.8 | **223.2 / 281.8 / 340.8** | 38.5 / 69.7 / 117.6 |
| R2-A Full V12 service catalogue | Fri 5 Nov 2027 (Day 334) | 243.7 / 304.6 / 365.5 | 13.0 / 25.8 / 38.5 | **256.7 / 330.4 / 404.0** | 41.4 / 79.9 / 148.1 |
| R2-B Consequential capabilities (mandates, commerce, bids, voice) | Fri 14 Jan 2028 (Day 404) | 117.0 / 146.3 / 175.6 | 20.2 / 41.6 / 78.0 | **137.2 / 187.9 / 253.6** | 21.8 / 40.0 / 69.7 |
| R3 EU region + SOC 2 Type II + ISO 27001 | Fri 19 May 2028 (Day 530) | 47.5 / 59.3 / 71.2 | 15.2 / 27.0 / 41.0 | **62.7 / 86.3 / 112.2** | 9.2 / 16.7 / 28.0 |
| R4 Global + ISO 27701/42001 | Fri 8 Sep 2028 (Day 642) | 19.5 / 24.4 / 29.2 | 37.9 / 70.5 / 103.2 | **57.4 / 94.9 / 132.5** | 4.1 / 7.8 / 13.9 |
| INV-R1 Investment Automation I | Fri 11 Feb 2028 (Day 432) | 82.0 / 102.5 / 123.0 | 27.5 / 49.8 / 72.0 | **109.5 / 152.3 / 195.0** | 14.3 / 28.2 / 51.2 |
| INV-R2 Investment Automation II | Fri 10 Mar 2028 (Day 460) | 58.9 / 73.6 / 88.3 | 48.8 / 76.4 / 104.0 | **107.7 / 150.0 / 192.3** | 11.1 / 20.3 / 35.9 |
| A1 Advanced foundations | Fri 25 Feb 2028 (Day 446) | 89.2 / 111.5 / 133.8 | 0.0 / 0.0 / 0.0 | **89.2 / 111.5 / 133.8** | 16.7 / 30.6 / 52.1 |
| A2 Growth intelligence | Fri 19 May 2028 (Day 530) | 105.3 / 131.6 / 157.9 | 0.0 / 0.0 / 0.0 | **105.3 / 131.6 / 157.9** | 18.2 / 33.7 / 57.7 |
| A3 Scale | Fri 28 Jul 2028 (Day 600) | 85.6 / 107.0 / 128.4 | 0.8 / 1.2 / 2.0 | **86.4 / 108.3 / 130.4** | 14.7 / 27.2 / 46.7 |
| A4 AI improvement | Fri 25 Aug 2028 (Day 628) | 12.2 / 15.3 / 18.3 | 0.0 / 0.0 / 0.0 | **12.2 / 15.3 / 18.3** | 1.6 / 3.1 / 5.5 |
| Sustain, hypercare and gate windows | — | 197.6 / 247.0 / 296.3 | 0.0 / 0.0 / 0.0 | **197.6 / 247.0 / 296.3** | — |
| **Total** | | **1286.3 / 1607.9 / 1929.4** | **169.9 / 303.2 / 454.6** | **1456.2 / 1911.1 / 2384.0** | **194.7 / 362.2 / 634.2** |
| **Total in ₹ crore** | | **12.86 / 16.08 / 19.29** | **1.70 / 3.03 / 4.55** | **14.56 / 19.11 / 23.84** | **1.95 / 3.62 / 6.34** |

**Why cash is ≈ 5× the effort value.** The effort value prices only story effort at the BRD day rate. Cash pays for calendar time of a 55–80 person train: programme roles outside velocity (≈ 35% of FTE-months), sustain and gate windows (≈ 15% of people cost), leave, IP sprints, coordination and onboarding, and contract and lead rates above the BRD rate. Part 8.4 showed the same effect at small scale (ratio ≈ 1.7); it grows with team size.

### 11.20.9.3 Development cost by programme year

| Programme year | Dates | People cost ₹ L L / C / H | External one-time ₹ L L / C / H | **Development total ₹ L L / C / H** |
|---|---|---|---|---|
| PY1 | Mon 7 Dec 2026 – Sun 5 Dec 2027 (Day 1–364) | 861.9 / 1077.3 / 1292.8 | 19.5 / 36.7 / 54.3 | **881.4 / 1114.0 / 1347.1** |
| PY2 | Mon 6 Dec 2027 – Sun 3 Dec 2028 (Day 365–728) | 424.4 / 530.5 / 636.6 | 150.4 / 266.5 / 400.2 | **574.8 / 797.0 / 1036.9** |
| **Total** | | **1286.3 / 1607.9 / 1929.4** | **169.9 / 303.2 / 454.6** | **1456.2 / 1911.1 / 2384.0** |

### 11.20.9.4 One-time external items

| # | One-time external item | Release | ₹ L low | ₹ L central | ₹ L high | Source |
|---|---|---|---|---|---|---|
| X-01 | Counsel review and sign-off of the 11 marketing rule packs (M-D4) | R1 | 1.00 | 1.75 | 2.75 | 11.13b; 11.15c |
| X-02 | Platform-decision legal: Vercel DPA, CRM transfers, BM-CL-1, edge-transit opinion | R1 | 2.00 | 3.50 | 5.00 | 11.19b |
| X-03 | Pen-test scope extension: SSO, SCIM, developer host, webhooks, connectors | R1 | 2.00 | 3.25 | 4.50 | 11.19b; 11.8b |
| X-04 | Independent differential-privacy review; DLT registrations | R1 | 1.10 | 1.95 | 2.80 | 11.19b |
| X-05 | Hindi chrome translation | R1 | 0.38 | 0.50 | 0.75 | 11.7b item 16 |
| X-06 | Tax adviser and legal review: order form, e-sign, refunds | R2-A | 1.00 | 2.25 | 3.50 | 11.5b |
| X-07 | SOC 2 readiness assessment | R2-A | 3.00 | 5.50 | 8.00 | 11.5b; Part 9.9 GAP-714 |
| X-08 | SOC 2 Type I audit | R2-A | 9.00 | 18.00 | 27.00 | DEC-775 |
| X-09 | Counsel: 8 payment, agent-commerce and procurement packs; portal terms | R2-B | 8.00 | 16.00 | 27.00 | 11.17b |
| X-10 | Pen test: agent gateway, PSP webhooks, approval flows; PSP certification | R2-B | 3.00 | 5.50 | 9.50 | 11.17b |
| X-11 | Voice: counsel per country (6), DPIA, voice pen test, telecom registrations, brand voice | R2-B | 9.20 | 20.10 | 41.50 | 11.18c |
| X-12 | Investment I: regulatory-characterisation opinions IN/US/EU/UK, counsel UAT, DPIA, data-room pen test | INV-R1 | 27.50 | 49.75 | 72.00 | 11.16e |
| X-13 | Investment II: counsel for 7 securities packs (IN, US, EU, UK, AML/KYC, advice perimeter), KYC sandbox | INV-R2 | 48.80 | 76.40 | 104.00 | 11.16d |
| X-14 | EU: DPIA, EU AI Act conformity file, member-state counsel for EU packs, Art. 27 representative | R3 | 5.00 | 9.00 | 15.00 | ASSUMPTION-1104; DEC-776 |
| X-15 | ISO/IEC 27001 certification | R3 | 8.00 | 14.00 | 20.00 | DEC-775 |
| X-16 | EU-stack penetration test | R3 | 1.50 | 2.75 | 4.00 | ASSUMPTION-1104 |
| X-17 | German and French translation of chrome and public pages | R3 | 0.75 | 1.25 | 2.00 | 11.7b item 16 |
| X-18 | ISO/IEC 27701 and ISO/IEC 42001 certification | R4 | 10.00 | 20.00 | 30.00 | DEC-775 |
| X-19 | Per-market counsel for UK, UAE, Singapore, Australia, US marketing and voice packs | R4 | 20.00 | 35.00 | 50.00 | ASSUMPTION-1104; DEC-776 |
| X-20 | Tax adviser per market for TX-04…09 (6 markets) | R4 | 6.00 | 12.00 | 18.00 | ASSUMPTION-1104; DEC-776 |
| X-21 | Multi-region and BYOK penetration test | R4 | 1.50 | 2.75 | 4.00 | ASSUMPTION-1104 |
| X-22 | Arabic translation and RTL legal templates | R4 | 0.38 | 0.75 | 1.25 | 11.7b item 16 |
| X-23 | Independent red-team before A3 enablement (M-D5) | A3 | 0.75 | 1.25 | 2.00 | 11.13b |
| | **Total external one-time** | | **169.86** | **303.20** | **454.55** | |

### 11.20.9.5 Reconciliation with approved budgets

| Approved item | Amount | Where it sits in this plan |
|---|---|---|
| Ledger A to the Release 2 build gate (DEC-230) | ₹52.7–84.1 L | SQ-01, SQ-02 (first two contract engineers), QA uplift, UX, independent reviewer, pen tests 1–2: inside R0, R1 and part of R2-A people cost |
| CR-ALN-01 (DEC-416) | ₹2.79–11.64 L | R1-core and R2-A baseline packages |
| A1 (DEC-417) | ≈ ₹28.0–55.4 L | A1 people cost (₹89.2 / 111.5 / 133.8 L in this plan: higher because the A1 team runs as a full squad with programme roles) |
| CR-V12-J-01 (DEC-770) | ₹9.4–37.3 L | R2-A catalogue package |
| **Total approved one-time** | **₹92.9–188.4 L** | |
| **Plan development total (rate band)** | **₹14.56 / 19.11 / 23.84 Cr** | §11.20.9.2 |
| **Increment funded under DEC-790** | **₹13.63 / 17.76 / 21.96 Cr** | Low − approved low; central − approved midpoint ₹1.35 Cr; high − approved high |
| Running approved (DEC-422) | ₹26,105–35,362 per month | Line B-S01 |
| Running plan at steady state (all releases live, incl. sustain team) | ₹20.0 / 31.5 / 46.6 L per month | §11.20.9.8 |
| Build tooling approved (DEC-419/420) | ≈ ₹1.20–1.37 L per month + build-agent API cap ₹1.35 L for the team of record | Scaled per active squad (§11.20.9.7) |

### 11.20.9.6 Subscription and running cost (recurring) lines

Monthly values are per the source part (central = stated base or midpoint). Year values are computed month by month from the line's start on the central calendar. Lines already inside the DEC-008 AI ceilings (for example Part 11.3 workflow AI per tenant, ₹1,247–12,467) are not added again.

| # | Recurring line | Starts (anchor → central date) | ₹/month low | ₹/month central | ₹/month high | PY1 ₹ L (central) | PY2 ₹ L | PY3 ₹ L | Source |
|---|---|---|---|---|---|---|---|---|---|
| B-S01 | Ledger B base (DEC-422: pilot running incl. 15% contingency and 2 seats) | Day 1 → Fri 18 Dec 2026 | 26,105 | 30,734 | 35,362 | 3.69 | 3.69 | 4.00 | DEC-422 |
| B-S02 | PITR add-on (DEC-771/787) | S1 → Fri 1 Jan 2027 | 8,500 | 9,150 | 9,800 | 1.10 | 1.10 | 1.10 | DEC-771; 11.5b RB-E1a |
| B-S03 | Platform decisions IN cell: standby, WAL archive, log drains, WAF, registry evaluations, benchmarks | R1 → Fri 2 Jul 2027 | 13,800 | 30,900 | 48,000 | 1.85 | 3.71 | 3.71 | 11.19b (SMS in B25 once; voice in 11.18) |
| B-S04 | AI evaluation lines and new-agent tokens (CR-V12-F-R) | R1 → Fri 2 Jul 2027 | 580 | 1,676 | 4,586 | 0.10 | 0.20 | 0.20 | 11.6b |
| B-S05 | Translation maintenance and parity CI | R1 → Fri 2 Jul 2027 | 750 | 2,625 | 4,500 | 0.16 | 0.32 | 0.32 | 11.7b |
| B-S06 | Webhook workers, SMS-DLT (B25), status host | R1 → Fri 2 Jul 2027 | 300 | 2,000 | 3,700 | 0.12 | 0.24 | 0.24 | 11.8b |
| B-S07 | SLA, status, paging tool, game days, help maintenance | R1 → Fri 2 Jul 2027 | 5,030 | 9,924 | 14,818 | 0.60 | 1.19 | 1.19 | 11.11b |
| B-S08 | Literal-alignment running CR-ALN-02 (upper bound) | R1 → Fri 2 Jul 2027 | 1,495 | 5,808 | 10,120 | 0.35 | 0.70 | 0.70 | DEC-416 |
| B-S09 | Business-requirement items: status host, help, metric projections | R2-A gate → Fri 5 Nov 2027 | 300 | 3,050 | 5,800 | 0.06 | 0.37 | 0.37 | 11.1b |
| B-S10 | V12 workflow AI sub-line, SMS/RCS, agent gateway, workers | R2-A gate → Fri 5 Nov 2027 | 2,589 | 3,725 | 4,860 | 0.07 | 0.45 | 0.45 | 11.4d |
| B-S11 | Logical dumps, SIEM sinks, e-sign envelopes | R2-A gate → Fri 5 Nov 2027 | 150 | 1,050 | 1,950 | 0.02 | 0.13 | 0.13 | 11.5b |
| B-S12 | Annual pen test, bug bounty, audit-sink egress | R2-A gate → Fri 5 Nov 2027 | 12,500 | 35,667 | 58,833 | 0.71 | 4.28 | 4.28 | 11.9c |
| B-S13 | CI and provider sandboxes for the SKU test catalogue | R2-A gate → Fri 5 Nov 2027 | 0 | 3,250 | 6,500 | 0.07 | 0.39 | 0.39 | 11.10c |
| B-S14 | 24x7 on-call: contracted NOC/SOC first line + internal rota (DEC-773) | R2-A gate → Fri 5 Nov 2027 | 110,000 | 185,000 | 260,000 | 3.70 | 22.20 | 22.20 | DEC-773 |
| B-S15 | SOC 2 Type II annual audit (₹18-45 L per year) from the observation start | R2-A gate → Fri 5 Nov 2027 | 150,000 | 262,500 | 375,000 | 5.25 | 31.50 | 31.50 | DEC-775 |
| B-S16 | Enterprise-tier SLA topology uplift (recovered through Enterprise pricing) | R2-A + 6 sprints → Fri 28 Jan 2028 | 55,000 | 102,500 | 150,000 | 0.00 | 11.28 | 12.30 | DEC-774 |
| B-S17 | Mandates, agentic commerce, payments, bids (IN region) | R2-B gate → Fri 14 Jan 2028 | 33,774 | 73,314 | 114,540 | 0.00 | 8.06 | 9.53 | 11.17b |
| B-S18 | Voice and recordings at 20,000 minutes per month | R2-B gate → Fri 14 Jan 2028 | 62,734 | 136,184 | 279,725 | 0.00 | 14.98 | 17.70 | 11.18c |
| B-S19 | Voice annual items (counsel review, relabelling, QA sample) per month | R2-B gate → Fri 14 Jan 2028 | 57,500 | 115,000 | 230,000 | 0.00 | 12.65 | 14.95 | 11.18c |
| B-S20 | Investment Automation I (KYC, e-sign, counsel retainer, AI) | INV-R1 gate → Fri 11 Feb 2028 | 59,377 | 121,691 | 234,472 | 0.00 | 12.17 | 15.82 | 11.16e |
| B-S21 | Investment Automation II (KYC/KYB, screening, counsel reviews, R10 reviewer, AI) | INV-R2 gate → Fri 10 Mar 2028 | 95,787 | 238,957 | 562,871 | 0.00 | 23.90 | 28.67 | 11.16d |
| B-S22 | EU stack hosting copy (DEC-772) | R3-a EU ready → Fri 19 Nov 2027 | 8,400 | 11,025 | 13,650 | 0.11 | 1.32 | 1.32 | DEC-772 |
| B-S23 | EU cell of the platform-decision lines | R3-a EU ready → Fri 19 Nov 2027 | 11,500 | 25,000 | 38,500 | 0.25 | 3.00 | 3.00 | 11.19b |
| B-S24 | EU increment for mandates and commerce | R3-a EU ready → Fri 19 Nov 2027 | 2,500 | 4,650 | 7,300 | 0.05 | 0.56 | 0.56 | 11.17b |
| B-S25 | Managed Kubernetes for IN and EU regional stacks | R3-a EU ready → Fri 19 Nov 2027 | 20,000 | 40,000 | 60,000 | 0.40 | 4.80 | 4.80 | ASSUMPTION-1106; DEC-776 |
| B-S26 | ISO 27001 surveillance audits (annual, per month) | R3 → Fri 19 May 2028 | 25,000 | 45,833 | 66,667 | 0.00 | 3.21 | 5.50 | ASSUMPTION-1106; DEC-775 |
| B-S27 | Four further regions UK, Middle East, APAC, US: hosting copy + managed Kubernetes | R4-a global ready → Fri 17 Dec 2027 | 73,600 | 123,250 | 174,600 | 0.00 | 14.79 | 14.79 | DEC-776; ASSUMPTION-1106 |
| B-S28 | Global tax-engine subscription | R4-a global ready → Fri 17 Dec 2027 | 15,000 | 37,500 | 60,000 | 0.00 | 4.50 | 4.50 | ASSUMPTION-1106; DEC-776 |
| B-S29 | Translation maintenance de, fr, ar | R4-a global ready → Fri 17 Dec 2027 | 2,250 | 5,625 | 9,000 | 0.00 | 0.68 | 0.68 | 11.7b R1 pattern |
| B-S30 | ISO 27701 and 42001 surveillance audits (per month) | R4 → Fri 8 Sep 2028 | 33,333 | 66,667 | 100,000 | 0.00 | 2.00 | 8.67 | ASSUMPTION-1106; DEC-775 |
| B-S31 | V11 advanced running X1-X3 at steady state | A1 → Fri 25 Feb 2028 | 12,546 | 29,382 | 46,218 | 0.00 | 2.94 | 3.53 | Part 9.10 9.10.7.2 |
| B-S32 | AI improvement running A2-A4 (CR-AIM-01) | A2 → Fri 19 May 2028 | 4,364 | 12,986 | 21,965 | 0.00 | 0.91 | 1.56 | 11.13b |
| B-S33 | Sustain engineering team after the build: SQ-01 (employed) + one contract squad, 10 FTE (maintenance, Part 8.3) | end of build → Fri 28 Jul 2028 | 1,100,000 | 1,375,000 | 1,650,000 | 0.00 | 68.75 | 165.00 | ASSUMPTION-1106 |
| B-S34 | Compliance-automation tooling (optional; open-source evidence pipeline first) *(optional; not in totals)* | R2-A gate → Fri 5 Nov 2027 | 0 | 87,500 | 125,000 | 1.75 | 10.50 | 10.50 | DEC-775 |

### 11.20.9.7 Running cost by programme year

| Programme year | Operational running ₹ L L / C / H | Build-time tooling (DEC-419/420, per active squad) ₹ L L / C / H | **Recurring total ₹ L L / C / H** |
|---|---|---|---|
| PY1 | 11.4 / 18.7 / 26.0 | 94.8 / 118.7 / 142.6 | **106.2 / 137.4 / 168.6** |
| PY2 | 153.7 / 260.9 / 406.1 | 40.2 / 50.4 / 60.5 | **193.9 / 311.3 / 466.6** |
| PY3 | 243.3 / 383.6 / 569.5 | 0.0 / 0.0 / 0.0 | **243.3 / 383.6 / 569.5** |
| **PY1–PY3** | **408.4 / 663.2 / 1001.6** | **135.0 / 169.1 / 203.2** | **543.4 / 832.3 / 1204.8** |

Build-time tooling = ₹1.15 / 1.44 / 1.73 L per active squad-month (Claude Max seats for five engineers, CI sandboxes, agent observability, and the build-agent API at 25–50% of the DEC-420 cap per squad) [ASSUMPTION-1106]. It ends with the build.

### 11.20.9.8 Run-rate added by each release

| Release | Monthly run-rate added ₹ L / C / H | Cumulative run-rate after the release ₹ L / C / H (per month) |
|---|---|---|
| R0 Foundation | 34,605 / 39,884 / 45,162 | 34,605 / 39,884 / 45,162 |
| R1 Core + enterprise identity + developer platform | 21,955 / 52,933 / 85,724 | 56,560 / 92,817 / 130,886 |
| R2-A Full V12 service catalogue | 330,539 / 596,742 / 862,943 | 387,099 / 689,559 / 993,829 |
| R2-B Consequential capabilities (mandates, commerce, bids, voice) | 154,008 / 324,498 / 624,265 | 541,107 / 1,014,057 / 1,618,094 |
| R3 EU region + SOC 2 Type II + ISO 27001 | 67,400 / 126,508 / 186,117 | 608,507 / 1,140,565 / 1,804,211 |
| R4 Global + ISO 27701/42001 | 124,183 / 233,042 / 343,600 | 732,690 / 1,373,607 / 2,147,811 |
| INV-R1 Investment Automation I | 59,377 / 121,691 / 234,472 | 792,067 / 1,495,298 / 2,382,283 |
| INV-R2 Investment Automation II | 95,787 / 238,957 / 562,871 | 887,854 / 1,734,255 / 2,945,154 |
| A1 Advanced foundations | 12,546 / 29,382 / 46,218 | 900,400 / 1,763,637 / 2,991,372 |
| A2 Growth intelligence | 4,364 / 12,986 / 21,965 | 904,764 / 1,776,623 / 3,013,337 |
| Sustain, hypercare and gate windows | 1,100,000 / 1,375,000 / 1,650,000 | 2,004,764 / 3,151,623 / 4,663,337 |

### 11.20.9.9 Contingency, management reserve and effort risk

| Item | Size | Held by | Released when |
|---|---|---|---|
| Management reserve on development | 10% of the central development total = **₹1.91 Cr** (outside the totals) | Founder / Finance | CCB-approved draw (§11.20.13) |
| Effort risk (high effort at central rates) | People cost ₹23.80 Cr instead of ₹16.08 Cr (+₹7.72 Cr); programme close Fri 12 Jan 2029 | Founder | Re-forecast each PI; DEC-770 (dates and budget follow the work) |
| Effort risk (low effort at central rates) | People cost ₹12.56 Cr (−₹3.52 Cr) | Finance | Hiring waves reduced at PI boundaries |
| Running contingency | 15% (B11) inside the lines that include it; otherwise applied by the FinOps review | FinOps | Monthly |
| AI ceilings | DEC-008 caps and the hard-capped lines B02, B23, B24, B25 unchanged | FinOps | Degradation ladder |

### 11.20.9.10 Programme budget summary (estimates)

**Development (one-time).**

| Block | Low | Central | High | Notes |
|---|---|---|---|---|
| People (squads + programme roles), plan-of-record schedule | ₹12.86 Cr | ₹16.08 Cr | ₹19.29 Cr | §11.20.9.2 |
| External one-time (counsel, audits, certifications, pen tests, translation, DPIA) | ₹1.70 Cr | ₹3.03 Cr | ₹4.55 Cr | §11.20.9.4 |
| **Development total** | **₹14.56 Cr** | **₹19.11 Cr** | **₹23.84 Cr** | of which PY1 ₹8.81 / 11.14 / 13.47 Cr; PY2 ₹5.75 / 7.97 / 10.37 Cr |
| Management reserve (outside) | — | ₹1.91 Cr | — | 10% |
| Effort-risk view (high effort, central rates, + external central) | — | — | ₹26.83 Cr | §11.20.9.9 |

**Subscription and running (recurring).**

| Block | Low | Central | High | Notes |
|---|---|---|---|---|
| Operational running PY1 / PY2 / PY3 | ₹0.11 / 1.54 / 2.43 Cr | ₹0.19 / 2.61 / 3.84 Cr | ₹0.26 / 4.06 / 5.70 Cr | §11.20.9.7 |
| Build-time tooling PY1 / PY2 | ₹0.95 / 0.40 Cr | ₹1.19 / 0.50 Cr | ₹1.43 / 0.61 Cr | Ends with the build |
| **Steady-state run-rate (all releases, sustain team)** | **₹20.0 L / month** | **₹31.5 L / month** | **₹46.6 L / month** | §11.20.9.8; ₹17.8 L central without the sustain team |

---

## 11.20.10 Risk register

Method of Part 8.2 §8.2.1.1 (P and I on 1–5; score ≥ 15 red, reviewed weekly by the Founder; 9–14 amber; ≤ 8 green). RSK-001…092 and the part-level risks (RSK-V12-R-01…10, Part 11.16/11.17/11.18 risk tables) remain open in their parts; the programme-level risks are added here.

| ID | Risk | Source | P | I | Score | Mitigation | Contingency | Owner | Trigger | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| RSK-V12-S-01 | Staff augmentation cannot supply ≈ 45 contract engineers on the wave dates | §11.20.8.5 | 4 | 4 | **16** | Two vendors, framework agreements by Day 15; requisitions one PI ahead; profile specs per squad | Later squad start; dates move (DEC-770); internal referral bonus | Programme Director | Any wave < 80% staffed two weeks before start | Open |
| RSK-V12-S-02 | Coordination overhead of 11 squads lowers velocity below the model | §11.20.7.2 | 3 | 4 | **12** | ART events, single-owner register, contracts between squads, coordination factor already 0.92 | Pause a wave; merge squads | RTE | Train velocity < 90% of plan for 2 sprints | Open |
| RSK-V12-S-03 | Counsel sign-offs late for payment, voice, securities packs | Parts 11.15–11.18 | 4 | 3 | **12** | Engagement 10 weeks ahead (RECOMMENDATION-1113); drafts already written; one reviewer per pack | Activation waits; release gates unaffected (DEC-906) | Growth/compliance lead | Pack not signed 4 weeks before its earliest date | Open |
| RSK-V12-S-04 | SOC 2 Type II window longer than 6 months or a qualified opinion | DEC-775 | 3 | 4 | **12** | Controls operating from R1; continuous evidence; readiness assessment | R3/R4 exits move; claims withheld | Security lead | Auditor requires > 6 months | Open |
| RSK-V12-S-05 | Effort underestimated (several parts sized by analogy; catalogue N-class) | §11.20.2 | 3 | 4 | **12** | Actual/estimate tracking from Sprint 0; re-estimate at each PI | Effort-risk band (close Jan 2029); management reserve | RTE + Finance | Actual/estimate > 1.25 for 2 sprints | Open |
| RSK-V12-S-06 | AI-built saving below 10% or quality guards fail | DEC-420 | 3 | 3 | 9 | Plan of record assumes no saving | Revert tooling; plan unchanged | RTE | Calibration result | Open |
| RSK-V12-S-07 | Founder as chief PO and approver becomes a bottleneck across 12 releases | RSK-012 | 4 | 4 | **16** | Domain POs; written delegations; 48 h decision SLA; Programme Director | Delegate gate votes per release | Founder | Decision backlog > 5 items or > 48 h | Open |
| RSK-V12-S-08 | Security incident in a consequential capability (mandate, payment, voice) | DEC-779…782 | 2 | 5 | 10 | Two-person mandates, kill switch, PDP recheck, pen tests, 3-way suites | Kill switch; incident process; regulator notification per pack | Security lead | Any SEV1 in R2-B scope | Open |
| RSK-V12-S-09 | Residency breach (EU data written to India or vice versa) | DEC-772 | 2 | 5 | 10 | CJ-TC-09 blocking both ways; region router; in-zone DR | Stop EU onboarding; notify; remediate | DPO | Any CJ-TC-09 failure | Open |
| RSK-V12-S-10 | Anthropic EU regional processing not available for EU tenants | DEC-772; RSK-V12-R-06 | 3 | 3 | 9 | Confirm by S12; registry rows per zone | EU AI routes HOLD / Tier 3 | Founder | No confirmation by S20 | Open |
| RSK-V12-S-11 | Running costs above estimates (counsel retainers, KYC, voice minutes) | §11.20.9.6 | 3 | 3 | 9 | Per-line alerts 70/90/100%; pass-through pricing for voice and KYC | Reduce pilot volumes; renegotiate retainers | FinOps | Line > high estimate for a month | Open |
| RSK-V12-S-12 | Scope keeps growing because every CR is funded (DEC-790) | DEC-790 | 4 | 3 | **12** | CR impact record and capacity rule (§11.20.13); release freezes | New CRs to the next release | Founder + RTE | Approved CR volume > 10% of PI capacity | Open |
| RSK-V12-S-13 | Business UAT participants unavailable for new products | GAP-1117 | 3 | 3 | 9 | Book blocks one PI ahead | Proxy users for non-vertical packs | Founder | < 75% of booked days delivered | Open |
| RSK-V12-S-14 | NOC/SOC vendor not live at the R2-A gate | DEC-773 | 2 | 4 | 8 | RFP at S12; contract S18 | Internal rota (option A, ₹2.5–4.0 L/month) | SRE lead | Contract not signed by S18 | Open |
| RSK-V12-S-15 | PSP or portal terms forbid automation in a market | Part 11.17 | 3 | 3 | 9 | Portal capability registry; ASSISTED/MANUAL modes | Manual path | Payments lead | Counsel finds a prohibition | Open |
| RSK-V12-S-16 | Knowledge loss when contract squads ramp down | §11.20.8.5 | 3 | 3 | 9 | Pairing with SQ-01; runbooks; two-sprint overlap; ADRs | Retain one engineer per squad for 1 month | Principal Architect | Defect rate up 25% after a release-to-sustain | Open |
| RSK-V12-S-17 | Certification scope creep (ISO 42001 AI system inventory larger than planned) | DEC-775 | 2 | 3 | 6 | AI registry as the inventory (DEC-788) | Extend ENT-04c | Security lead | Stage 1 findings | Open |
| RSK-V12-S-18 | Regional stack drift between IN, EU and later regions | ENT-05/07 | 3 | 3 | 9 | One IaC template; per-zone pipelines; drift job | Freeze region changes | SRE lead | Drift alert > 24 h | Open |
| RSK-V12-S-19 | Year-end freeze and holidays reduce capacity more than modelled | ASSUMPTION-1100 | 3 | 2 | 6 | Holiday list per sprint; freeze rule | Gate +1 sprint | RTE | Working days < plan by 10% | Open |
| RSK-V12-S-20 | FX moves raise USD-priced tools, audits and counsel | Part 8.4 | 3 | 2 | 6 | ₹90/USD planning rate; quarterly review | Re-forecast | Finance | ₹/USD > 95 | Open |
| RSK-V12-S-21 | Integration of the investor product exposes Sales & Marketing tenants to INV data | DEC-800 | 2 | 5 | 10 | Separate product boundary, schema `inv`, RLS, AU-200 | Disable INV entitlements | Security lead | Any cross-product read in tests | Open |
| RSK-V12-S-22 | Release 1 scope (≈ 1,226 pd) too large for one gate | §11.20.3 | 3 | 3 | 9 | Progressive activation from Feb 2027; R1 freeze at S12 | Split R1 activation by capability | Founder | R1 forecast > 2 sprints late at S9 | Open |
| RSK-V12-S-23 | Double counting or gaps remain after the overlap register | §11.20.2.3 | 2 | 3 | 6 | Single-owner register maintained in the backlog tool (ADR-268) | Re-run the roll-up at PI planning | RTE | Two stories with the same capability in different squads | Open |
| RSK-V12-S-24 | Supabase/Vercel EU plans or SLAs not available as assumed | DEC-772/774 | 2 | 3 | 6 | Verify at S16; alternatives in ADR-267 | AWS-native EU fallback | SRE lead | Provider quote lacks EU region or SLA | Open |

**Heat summary.** Red (≥ 15): RSK-V12-S-01, S-07. Amber (9–14): S-02, S-03, S-04, S-05, S-06, S-08, S-09, S-10, S-11, S-12, S-13, S-15, S-16, S-18, S-21, S-22. Green (≤ 8): S-14, S-17, S-19, S-20, S-23, S-24.

---

## 11.20.11 RAID log

### 11.20.11.1 Assumptions

| ID | Assumption | Tag | Validate by | Owner |
|---|---|---|---|---|
| A-01 | Holidays and year-end leave per §11.20.1.3 (Part 11.20a) | ASSUMPTION-1100 | Sprint 0 planning | RTE |
| A-02 | 7.53 pd per FTE-sprint, ramp 0.5/0.85, leave 0.95, coordination 1.00/0.95/0.92 | ASSUMPTION-1101 | DEC-420 gate; every PI | RTE |
| A-03 | Sustain reserve 10% after R1, 15% after R2-A | ASSUMPTION-1102 | PI-3 inspect and adapt | SRE lead |
| A-04 | Absorption 10 / 7.5 / 5% of V12 groups A–L at refinement | ASSUMPTION-1103 | PI-2 re-estimate | RTE |
| A-05 | Enterprise items and their external costs per §11.20.2.8 and §11.20.9.4 | ASSUMPTION-1104 | Quotes by S16 | Programme Director |
| A-06 | Hardening sprints per release; SOC 2 Type II window 6 months; ISO 27701/42001 ≈ 4 months after ISO 27001 | ASSUMPTION-1105 | Auditor contract | Security lead |
| A-07 | Running assumptions (managed Kubernetes, tax engine, surveillance audits, build tooling per squad, sustain team) | ASSUMPTION-1106 | Quotes | FinOps |
| A-08 | Lead and programme-role rates ₹2.0–3.0 L per month | ASSUMPTION-1107 | Contracts | Finance |
| A-09 | V11 A2/A3 remainder split 55 / 45% | ASSUMPTION-1108 | A1 actuals | AI lead |
| A-10 | Staff-augmentation lead time 2–6 weeks per profile | ASSUMPTION-1109 | Vendor SLAs | Programme Director |

### 11.20.11.2 Issues (open now)

| ID | Issue | Impact | Action | Owner | Due |
|---|---|---|---|---|---|
| I-01 | No counsel panel, auditors, NOC/SOC vendor or staff-augmentation vendors named [GAP-1115] | Waves and activations cannot be contracted | RFPs in Sprint 0 | Programme Director | Day 15 / Day 30 |
| I-02 | No quotes for managed Kubernetes, tax engine, per-market counsel and certification bodies [GAP-1116] | Running and external lines are estimates | Obtain quotes | FinOps | S16 |
| I-03 | Part 11.14 §11.14.2 (pending conflicts list) is not yet completed | Some V12 rows may still read "Pending" | Consolidation owner to close (DEC-791 adopts all) | Founder | S2 |
| I-04 | DEC-790 increment (₹13.6–22.0 Cr) needs a ledger entry and cash plan | Commitments beyond Ledger A | Approve DEC-910/911 | Founder + Finance | Day 15 |
| I-05 | Parts 11.16d/e use DEC-770-derived day rates (₹4,519/5,697/6,807) while other parts use Part 8.4 rates | ≤ 0.6% value difference | This plan revalues at Part 8.4 rates | FinOps | Done here |
| I-06 | Payment packs for UK and US and voice packs for some markets not drafted | Those activations cannot start | Draft at R4-a with counsel | Growth/compliance lead | S24 |

### 11.20.11.3 Dependencies

The external dependencies are DP-01…DP-15 (Part 8.1 §8.1.7.3) and DP-V12-S-01…22 (Part 11.20a §11.20.4.6). Internal dependencies between packages are the earliest-start rules of Part 11.20a §11.20.2.6 and the graphs of §11.20.4. **Decisions** are logged in §11.20.14 and in A090.

---

## 11.20.12 Governance cadence

| Forum | Cadence | Chair | Members | Inputs | Outputs |
|---|---|---|---|---|---|
| Founder decision forum | Weekly (Monday) | Founder | Programme Director, RTE, Finance | Decision backlog, red risks | Decisions in the log within 48 h |
| Programme steering | Fortnightly (sprint review Friday) | Founder | Programme Director, RTE, architects, domain POs, security, DPO, Finance | Burn-up per release, forecast dates, budget re-forecast, top risks | Gate readiness, re-forecast approval |
| ART sync (scrum of scrums + PO sync) | Twice weekly | RTE | Tech leads, POs | Programme board | Dependency resolution |
| PI planning / Inspect and adapt | Every six sprints | RTE | Whole train | Vision, PI objectives | Committed PI objectives |
| Change control board | Weekly | Founder/PO | §11.20.13 | CRs with impact records | Approved / deferred CRs |
| Risk and RAID review | Fortnightly (steering) + weekly for red | Programme Director | Risk owners | Register | Actions, escalations |
| FinOps review | Monthly + per-sprint burn | Finance | FinOps, SRE, AI lead | Ledger lines, alerts | Re-forecast, line approvals |
| Security and AI governance board | Monthly | Security lead | AI lead, DPO, Principal Architect | Findings, registry rows, evaluations | Approvals, waivers (expiring) |
| Counsel pack board | Fortnightly | Growth/compliance lead | Counsel panel, DPO, domain POs | Pack status, C-01…C-12 questions | Sign-offs, Q-REV schedule |
| Certification steering | Monthly from S12 | Security lead | Auditors (as needed), SRE, DPO | Control evidence | Readiness decisions |
| Vendor management | Monthly | Programme Director | Vendors | Staffing, SLAs | Corrective actions |
| Release gate | Per gate | Founder/PO | Part 11.20a §11.20.5.3 | Evidence pack | Go / no-go in A090 |
| Quarterly business review | Quarterly | Founder | Startup heads, Finance | KPIs, benefits | Priorities for next PIs |

**Reporting.** One-page status per sprint (burn-up per release, forecast gate dates low/central/high, budget actual versus plan per ledger line, top five risks, decisions needed); monthly FinOps pack; gate packs per Part 8.2 §8.2.4.

---

## 11.20.13 Change control (extends Part 8.2 §8.2.2.4; DEC-912)

```mermaid
flowchart TD
  A["Change request raised"] --> B["Impact record<br/>journey, UI, API, data, cost, tests,<br/>release, squad, rule pack"]
  B --> C{"Class"}
  C -- "Minor: 5 SP or less, no rule, money, consent or AI scope" --> D["Domain PO decides in the sprint"]
  C -- "Major or funded scope addition" --> E["CCB weekly"]
  C -- "Emergency: incident or legal order" --> F["Founder within 1 business day"]
  E --> G{"Capacity available<br/>in the target release"}
  G -- "Yes" --> H["Add to release backlog"]
  G -- "No" --> I["Add capacity or move the date<br/>never remove scope  DEC-770"]
  I --> J["Re-forecast dates and ledgers"]
  D --> H
  F --> H
  H --> K["Traceability, estimate, overlap register updated"]
  J --> K
  K --> L["Built under DoD, evidence links the CR"]
```

| Element | Rule |
|---|---|
| Classes | Minor, Major, Emergency (Part 8.2) plus **Funded scope addition** (DEC-790): any new V12 or Founder scope; always Major |
| Impact record | Part 8.2 fields plus: target release and squad; overlap check against the single-owner register (ADR-268); rule packs and jurisdictions affected; residency zones affected; certification controls affected; running-cost lines |
| Capacity rule | **Replaces the Part 8.2 spill rule:** an approved CR adds capacity (FTE or squad) or moves the gate date; nothing is removed from a release (DEC-770) |
| Freeze points | R1 scope freeze start of S12 (Mon 24 May 2027); R2-A start of S20 (Mon 13 Sep 2027); R2-B start of S24 (Mon 8 Nov 2027); INV-R1 start of S27 (Mon 20 Dec 2027); A-releases two sprints before each build end. After a freeze only Must, compliance, security and defect CRs enter |
| Re-forecast | Every sprint review: dates (scheduler re-run with actual velocity), development and running ledgers; any forecast above the high band of a release goes to the Founder forum |
| Management reserve | Draws only through the CCB with an impact record; balance reported monthly |
| DEC changes | Only the Founder/PO through a CR that cites the DEC (Part 8.2 rule unchanged) |
| Metrics | CR count and SP per PI; approval lead time; share of CRs that are compliance-driven; RSK-V12-S-12 trigger |

---

## 11.20.14 Decisions and architecture decision records

### 11.20.14.1 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-900 | Adopt Part 11.20 as the master implementation plan of record for the entire revised scope (Parts 0–9, V11, V12 groups, Founder decisions, enterprise items) | Founder decisions DEC-770 and DEC-790 (28 Nov 2026); P5 planning panel | Supersedes the calendar parts of Part 8.1 §8.1.2 and Part 9.5 §9.5.2.7 as the plan of record; their scope remains |
| DEC-901 | Effort baseline of record **4,283 / 6,374 / 9,302 pd** (plan), from 7,908 pd central gross, with the single-owner overlap register OV-01…OV-20 and the 10 / 7.5 / 5% absorption on groups A–L | DEC-790; Part 11.10 RECOMMENDATION-924 | Replaces 532 / 722 / 921 pd (DEC-228) as the programme estimate |
| DEC-902 | Release structure R0, R1, R2-A, R2-B, R3 (R3-a), R4 (R4-a), INV-R1, INV-R2, A1–A4 with gate dates of record from the central schedule: R0 Fri 29 Jan 2027; **R1 Fri 2 Jul 2027**; **R2-A Fri 5 Nov 2027**; **R2-B Fri 14 Jan 2028**; INV-R1 Fri 11 Feb 2028; A1 Fri 25 Feb 2028; INV-R2 Fri 10 Mar 2028; R3-a Fri 19 Nov 2027; R3 exit Fri 19 May 2028; A2 Fri 19 May 2028; A3 Fri 28 Jul 2028; A4 Fri 25 Aug 2028; R4-a Fri 17 Dec 2027; **R4 exit and programme close Fri 8 Sep 2028** | DEC-770 (dates follow the work) | DEC-228 dates become indicative (CONFLICT-1118 resolved); low and high bands published with every re-forecast |
| DEC-903 | Team scaling to eleven squads (peak 55 engineering FTE + 25.25 programme roles = 80.25 FTE in S22) through two staff-augmentation vendors, in waves 0–6 | DEC-770 ("team extended by change request") | Extends DEC-228 staffing; hiring waves of §11.20.8.5 |
| DEC-904 | DEC-420 calibration in the plan: plan of record assumes no saving; at ≥ 20% option A (default) does not hire SQ-06; option B keeps the team and brings gates forward; the result is recorded as a new decision | DEC-420 | Calibration applied to waves 3–6 only |
| DEC-905 | SAFe cadence: PI-0 (S0–S2) then PIs of six sprints with an IP sprint at 50% feature capacity; PI calendar of §11.20.7.7; A-release builds may start when the previous A build completes, while activation gates G-A1…G-A3 stay | P5 RTE; amends the sequencing of DEC-411 | Removes idle capacity between A gates; CONFLICT-1119 resolved |
| DEC-906 | Build everywhere, activate per jurisdiction: release gates certify build and test; activation needs the jurisdiction's counsel-signed pack active in AU-128, region readiness and the flag approver; missing sign-off never delays a gate | DEC-779…783; DEC-761 | Activation matrix of Part 11.20a §11.20.5.2; flag names proposed in §11.20.3.6 |
| DEC-907 | Certification chain: SOC 2 Type I at the R2-A gate; Type II observation from R2-A; Type II report and ISO 27001 at the R3 exit; ISO 27701 and ISO 42001 at the R4 exit | DEC-775 | Fixes R3/R4 exits by calendar, not effort |
| DEC-908 | EU stack built in the R3 window and ready at R3-a (Fri 19 Nov 2027); provisioned in production at the first EU contract (DEC-772); global stamps ready at R4-a | DEC-772, DEC-776 | Region flags of §11.20.3.6 |
| DEC-909 | Year-end change freeze 24 Dec – 2 Jan: no gate in a sprint containing 24–31 December | P5 Programme Director | R2-B gate moved from S27 to S28 |
| DEC-910 | Development (one-time) budget of record ₹14.56 / 19.11 / 23.84 Cr (rate band, plan-of-record schedule), of which external ₹1.70 / 3.03 / 4.55 Cr; management reserve ₹1.91 Cr outside; DEC-790 increment over approved items ₹13.63 / 17.76 / 21.96 Cr | DEC-790 | Ledger A extended by change request; reported by release and year |
| DEC-911 | Running (recurring) budget of record by line and release (§11.20.9.6–9.8): PY1 ₹0.19 Cr, PY2 ₹2.61 Cr, PY3 ₹3.84 Cr operational (central), build tooling PY1 ₹1.19 Cr, PY2 ₹0.50 Cr; steady state ₹31.5 L per month central including the sustain team | DEC-790; extends DEC-422 | Ledger B lines opened as each release reaches them; alerts 70/90/100% per line |
| DEC-912 | Change control under DEC-770/790: no scope removal; capacity or date moves; freeze points; per-sprint re-forecast; management-reserve draws via CCB | DEC-770, DEC-790 | Replaces the Part 8.2 spill rule |
| DEC-913 | Governance cadence of §11.20.12, including the counsel pack board and certification steering | P5 Programme Director | Forums and reporting of record |
| DEC-914 | Sustain model after the build: SQ-01 plus one contract squad (10 FTE) and the 24×7 rota; contract squads release to sustain after a two-sprint knowledge-transfer overlap | P5 Programme Director | Running line B-S33 |
| DEC-915 | The plan is regenerated by `s_master_plan.py` at every PI planning with actual velocity, start dates and estimates; the published tables are its output | P5 RTE | Single source for dates and budgets |

### 11.20.14.2 Architecture decision records

| ADR | Title | Decision | Alternatives rejected | Consequences | Status |
|---|---|---|---|---|---|
| ADR-265 | Squad topology and ownership | Stream-aligned squads per package family (identity/developer, AI platform, catalogue ×2, commerce, voice, investment, regions, advanced); SRE and security as enabling teams; platform components (PDP, MND, registry, entitlement ledger, region router) each owned by one squad with published contracts | Component teams per layer (hand-offs on every story); one large pool (no ownership of controls) | + clear ownership of fail-closed controls; − inter-squad contracts must be maintained | Proposed (P5) |
| ADR-266 | Activation control plane | Activation = feature flag AND pack state (AU-128/AU-170) AND region readiness, evaluated at configuration time and again by the PDP at dispatch; flags never bypass a pack | Flags alone (lets a capability run without a signed pack); per-tenant code branches | + one fail-closed rule for every jurisdiction; − flag approvers need pack visibility in A090 | Proposed (P5) |
| ADR-267 | Region promotion path | One IaC template per zone stamp; IN first, EU second (R3-a), then UK, ME, APAC, US (R4-a); managed Kubernetes from R3 for regional stacks; per-zone pipelines with promotion IN → EU → others for the same artefact; in-zone DR only | Region-specific forks; multi-region active-active database (not needed for residency) | + residency by construction; − n× running cost per zone | Proposed (P5) |
| ADR-268 | Single-owner work-package register | The overlap register OV-01…20 becomes a backlog-tool field: each capability ID has one owning squad and package; CI fails a story that duplicates an owned capability ID | Ad hoc dedupe at refinement | + no double build; − register upkeep at each PI | Proposed (P5) |
| ADR-269 | Continuous certification evidence | Evidence for SOC 2, ISO 27001/27701/42001 collected by the existing pipeline (AU-079/151/154) from R1, mapped to control IDs; auditors read from the evidence store | Point-in-time evidence before each audit | + Type II window starts with operating evidence; − control mapping effort in ENT-04a | Proposed (P5) |

---

## 11.20.15 Expert persona review

| Persona | Question | Finding | Action taken |
|---|---|---|---|
| Programme Director | Is the 80-person peak achievable from a 6.5-FTE start in ten months? | Only with two vendors and requisitions one PI ahead; wave 2 at S4 is the tightest | RECOMMENDATION-1111; RSK-V12-S-01 red; dates move rather than scope (DEC-770) |
| SAFe RTE | Do squads idle while waiting for gates? | First schedule left ≈ ₹4 Cr of idle cash between A gates | DEC-905 build overlap; squads released when queues end; sustain shown as its own line |
| Principal Architect | Is sequencing technically sound? | Identity, `app_rw`, registry and connector framework precede every R1 and R2 consumer; catalogue waits for QA infrastructure and the common engine | Earliest-start rules §11.20.2.6; dependency graphs §11.20.4 |
| Principal Architect | Are fail-closed controls on the scaling path? | No: they stay with owning squads and human review (DEC-420) | Principle P5 |
| FinOps lead | Are development and running costs separated and complete? | Yes; build tooling, which DEC-420 keeps separate from Ledger B, is shown as its own recurring block; lines already inside AI ceilings are not double counted | §11.20.9 |
| FinOps lead | Why is cash ≈ 5× the effort value? | Programme roles, sustain, leave, IP sprints, rates above the BRD rate | Explained in §11.20.9.2; effort value kept as the comparison measure |
| Risk manager | Which risk can stop the programme? | None stops it (all funded); the date risks are hiring (S-01), the Founder bottleneck (S-07) and the Type II window (S-04) | Red risks reviewed weekly |
| Risk manager | Can a missing counsel sign-off delay a release? | No: DEC-906 separates build gates from activation | Activation matrix §11.20.5.2 |

---

## 11.20.16 Registers

### 11.20.16.1 Tags issued in Part 11.20 (range 1100–1119)

| Tag | Statement | Basis | Validate by / owner |
|---|---|---|---|
| [ASSUMPTION-1100] | Calendar: Day 1 Mon 7 Dec 2026; holiday and leave list of §11.20.1.3; programme years PY1–PY3 | Task instruction; Indian holidays (verify) | Sprint 0 / RTE |
| [ASSUMPTION-1101] | Capacity: 7.53 pd per FTE-sprint; new-FTE ramp 0.5 / 0.85; leave 0.95; coordination 1.00 / 0.95 / 0.92; IP sprints at 50% | Part 9.5 §9.5.2.5; SAFe practice | DEC-420 gate; each PI / RTE |
| [ASSUMPTION-1102] | Sustain reserve 10% of active capacity after R1 and 15% after R2-A | Part 8.3 maintenance practice | PI-3 / SRE lead |
| [ASSUMPTION-1103] | Absorption of 10 / 7.5 / 5% of V12 groups A–L at refinement | Part 9.5 ASSUMPTION-502 at half strength | PI-2 / RTE |
| [ASSUMPTION-1104] | Enterprise engineering ENT-01…10 (228 / 348 / 521 pd) and enterprise external costs (EU and per-market counsel, tax advisers, pen tests, translation) | DEC-771…776 | Quotes by S16 / Programme Director |
| [ASSUMPTION-1105] | Hardening sprints per release (0–2); SOC 2 Type II window 6 months + report (≈ 14 sprints after R2-A); ISO 27701/42001 ≈ 8 sprints after ISO 27001 | Common audit practice (verify with the auditor) | Auditor contract / Security lead |
| [ASSUMPTION-1106] | Running: managed Kubernetes ₹10–30k per region-month; tax engine ₹15–60k/month; ISO surveillance; build tooling ₹1.15–1.73 L per squad-month; sustain team 10 FTE ₹11–16.5 L/month | Provider list prices (verify, 27 Nov 2026) | Quotes / FinOps |
| [ASSUMPTION-1107] | Lead and programme-role rate ₹2.0–3.0 L per FTE-month | Market practice (verify) | Contracts / Finance |
| [ASSUMPTION-1108] | V11 A2/A3 remainder split 55 / 45% | Part 9.10 gives A1 only | A1 actuals / AI lead |
| [ASSUMPTION-1109] | Staff augmentation delivers a profile in 2–6 weeks after the framework agreement | Vendor practice (verify) | Vendor SLAs / Programme Director |
| [RECOMMENDATION-1110] | Adopt the twelve-release structure with build-everywhere, activate-per-jurisdiction gating | DEC-770…790 | Founder, Day 1 |
| [RECOMMENDATION-1111] | Sign two staff-augmentation framework agreements by Day 15 | RSK-V12-S-01 | Founder, Day 15 |
| [RECOMMENDATION-1112] | Year-end change freeze 24 Dec – 2 Jan | Operational practice | Founder, Day 1 |
| [RECOMMENDATION-1113] | Engage counsel for each pack 10 weeks before its earliest technical date | RSK-V12-S-03 | Growth/compliance lead, Day 30 |
| [RECOMMENDATION-1114] | At the calibration gate, choose option A (do not hire SQ-06) if net saving ≥ 20% | DEC-420; §11.20.6.4 | Founder, Day 46 |
| [GAP-1115] | No named counsel panel, auditors, NOC/SOC vendor or staff-augmentation vendors; UK/US payment packs not drafted | Parts 11.15–11.17 | Day 30 / Programme Director |
| [GAP-1116] | No quotes for managed Kubernetes, tax engine, per-market counsel, certification bodies | DEC-775/776 | S16 / FinOps |
| [GAP-1117] | Business UAT participants for the new products not named | §11.20.8.7 | S8 / Founder |
| [CONFLICT-1118] | DEC-228 dates (Release 1 Day 180, Release 2 Day 208) versus the capacity-derived plan (R1 Day 208, R2-A Day 334). **Resolution:** DEC-770 makes dates follow the work; DEC-902 records the new dates | DEC-228 vs DEC-770 | Resolved (DEC-902) |
| [CONFLICT-1119] | DEC-411/DEC-417 sequence A2 after gate G-A1 (A1 "Day ≈ 239–365") versus the plan (A1 Day 446; A2 build overlapping the G-A1 window). **Resolution:** builds overlap, activation gates unchanged (DEC-905) | DEC-411/417 vs this plan | Resolved (DEC-905) |

### 11.20.16.2 Inconsistencies found in earlier parts (reported, not changed)

| # | Location | Finding | Handling here |
|---|---|---|---|
| 1 | Parts 11.2, 11.3, 11.4 vs 11.10c | The same SKU and workflow builds are estimated in four parts | Single-count rule; OV-01…OV-04 |
| 2 | Part 11.4d D-4 vs Parts 11.17, 11.18 | D-4 conflict workflows and voice/media adapters duplicated by the Founder-decision parts; 11.18 supersedes only the voice share | OV-07 removes all of D-4 (media in J SVC-27) |
| 3 | Part 11.5b E-02 vs Part 11.19b R-WP01…03 vs Part 11.8b H2 | Enterprise identity engine estimated twice; H2 says the "identity owner group" counts it | OV-12; R is the owner (DEC-784) |
| 4 | Part 11.9c R3 (24×7 security monitoring ₹40k–1.5 L/month) vs DEC-773 | Same service | Counted once in DEC-773 line |
| 5 | Part 11.8b B25 SMS-DLT vs Part 11.19b running table | Line repeated | Counted once |
| 6 | Part 11.19b B-R06 voice CPaaS vs Part 11.18c telephony lines | Same numbers and minutes | Counted in 11.18 only |
| 7 | Parts 11.16d/e rates (₹4,519/5,697/6,807) vs Part 8.4 (₹4,545/5,682/6,818) | Different day rates | Revalued at Part 8.4 rates |
| 8 | Part 11.16d running includes a "workbook cross-check" line | Not additive | Excluded from totals |
| 9 | Part 9.10 DEC-417 "A1 runs W6, Day ≈ 239–365"; Part 11.13b A2 "Day ≈ 366–480" | Superseded by the capacity calendar | CONFLICT-1119 |
| 10 | Part 11.1b CONFLICT-761 and others still read "Pending Founder decision" | DEC-772/776/790/791 adopted them | Treated as adopted (I-03) |
| 11 | Part 11.11b 24×7 option table (A/B/C) vs DEC-773 (hybrid) | DEC-773 chose the hybrid | Running line uses ₹1.1–2.6 L |
| 12 | Part 11.5b RB-E1a PITR line vs DEC-771 PITR | Same add-on | One line (B-S02) |

---

## 11.20.17 Quality gate: Batch 11.20b

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | **Pass** | Budget lines cite their parts and DECs; risks cite sources; sprint goals cite story families |
| 2 | Assumptions, gaps and conflicts tagged and logged | **Pass** | Twenty tags 1100–1119 in §11.20.16.1 (10 assumptions, 5 recommendations, 3 gaps, 2 conflicts) |
| 3 | IDs unique and consistent with earlier parts | **Pass** | DEC-900…915, ADR-265…269, RSK-V12-S-01…24, DP-V12-S-01…22 within allocation; story IDs from Parts 5, 11.16–11.19 |
| 4 | No story lacks AC; no requirement lacks a test | **N/A** | Planning part; Sprint 0–2 stories carry AC in their source parts |
| 5 | Negative, edge, security and accessibility cases covered | **Pass** | Demo scripts include denial cases; gates require security, residency and kill-switch evidence |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | **N/A** | Agents specified in their parts |
| 7 | Time-sensitive facts flagged "verify" with as-of date | **Pass** | Rates, quotes, lead times and certification windows flagged (27 Nov 2026) |
| 8 | No restricted data routed to free-tier models | **Pass** | Unchanged; Tier 2 stays off |
| 9 | Consistent with earlier parts | **Pass with findings** | Twelve inconsistencies in §11.20.16.2 |

**Self-review corrections.** (1) The first schedule kept every squad until all A-releases ended and showed ≈ ₹4.3 Cr of idle cost; queues were narrowed and squads released when their queues end (DEC-914). (2) A2 build originally waited for the G-A1 KPI window; overlapping builds removed three idle sprints (DEC-905). (3) The R2-B gate fell on Fri 31 Dec 2027; the year-end freeze moved it to Fri 14 Jan 2028 (DEC-909). (4) After the R2-A gate the second-line SRE rota was counted twice (programme role and DEC-773); it now sits only in the running line. (5) V12 subtotal rows in Part 11.20a §11.20.2.7 were recomputed from the group table.

**Status: Part 11 Batch 11.20b complete. Part 11.20 complete: plan 4,283 / 6,374 / 9,302 pd; twelve releases from R0 (Fri 29 Jan 2027) to programme close (Fri 8 Sep 2028); peak 80.25 FTE (S22); development ₹14.56 / 19.11 / 23.84 Cr one-time; running ₹31.5 L per month central at steady state.**
