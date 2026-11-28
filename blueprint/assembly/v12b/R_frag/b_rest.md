
---

### 11.19.5.9 Automations AU-290…AU-299

No new AI agent is needed for these capabilities: every control is deterministic. The ten automations below are rules-only (Tier 0, no model call), run in the tenant's zone and write evidence to the audit store. They follow the AU table format of Part 7.4b / V11 brief.

| ID | Name | Wave / Release | Linked BR / FR / rule | Trigger | Deterministic logic | Outputs | Autonomy | Guardrail | Failure / fallback | KPI | Cost |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AU-290 | IdP federation health watcher | Release 1 | FR-V12-R-006, 027, 028; ENT-IDN-01/02; DEC-880 | Daily 02:00 zone time; metadata URL change; login-failure spike (> 20 in 5 min per connection) | Fetch metadata over https; compare certificate set and endpoints; certificate `not_after` vs 30/14/7/1-day thresholds; DNS TXT recheck for each verified domain; 2 misses → `verification_lost`; failure-spike detector per connection | Updated certificate list (only from signed metadata), `identity.certificate.expiring`, `identity.email_domain.verification_lost`, R12 notifications, SIEM events | L3 internal (no tenant-visible effect except alerts); never unenforces SSO | Only signed metadata is applied; unsigned metadata → alert, no change; never removes the last active certificate | Metadata fetch fails 3 days in a row → High alert to R12, configuration unchanged | 0 tenant lockouts caused by expired certificates; alerts ≥ 7 days before expiry in 100% of cases | ₹0 (shared worker); 2/3/4 pd |
| AU-291 | SCIM reconciler and de-provisioning SLA monitor | Release 1 | FR-V12-R-011…016; ENT-IDN-03 | Every 10 min; each `identity.scim.*` event | Compare SCIM-managed memberships with last IdP state (`meta.lastModified` and full list pull where the IdP supports it); detect orphans (active product user, inactive or missing in IdP); compute `product_ms` and `end_to_end_s`; breach when > 60 s or > 900 s | SLA ledger rows, orphan list, SEV2 incident on breach, revoke-all for confirmed orphans (R12 confirm unless the IdP states `active=false`) | L1 for revocation of orphans without IdP signal (R12 confirms); L3 for SLA measurement | Never deletes users; only revokes access; break-glass excluded | IdP list API unavailable → measure from events only and flag "partial evidence" | De-provisioning p95 ≤ 60 s product side; 100% ≤ 15 min end to end | ₹0; 3/4/6 pd |
| AU-292 | Access governance and database privilege drift guard | Release 1 (Sprint 1 for DB checks) | FR-V12-R-019…023, 143…155; ENT-ACC-02; DEC-778; DEC-898 | Quarterly campaign; nightly drift scan; every minute `pg_stat_activity` probe | Open recertification items for privileged memberships and custom roles; suspend unconfirmed privileged permissions at day 14; compare roles, memberships, grants, RLS flags, policies and Data API exposure with the Git snapshot; detect sessions of `service_role`/`postgres` from app subnets | Campaigns, suspensions, drift findings (`security_finding`), SEV2 on privileged-role session | L1 for suspension (R12 can reinstate immediately); L3 for detection | Suspends permissions, never accounts; never changes grants itself (finding + runbook) | Probe failure → finding "monitor blind" High | 100% privileged access recertified each quarter; drift MTTD ≤ 24 h; privileged session MTTD ≤ 2 min | ₹0; 3/5/7 pd |
| AU-293 | Credential hygiene | Release 1 | FR-V12-R-031…033, 052, 153; ENT-API-01/02; SB-09 | Daily; leak report webhook; key use from new ASN with 10× baseline | Expiry reminders (14/7/1 days) for API keys, OAuth secrets, SCIM tokens, webhook secrets, DB passwords; idle credentials (no use 90 days) flagged, 180 days revoked with notice; leak report → revoke within 60 s | Notifications, revocations, findings | L3 for leak revocation and idle revocation after notice (pre-approved policy); L1 for anomalies (R12 decides) | Never revokes break-glass or DB credentials automatically (runbook) | Notification failure → retry, then finding | 0 expired-credential outages; leak revocation p95 ≤ 60 s | ₹0; 2/3/4 pd |
| AU-294 | Webhook delivery scheduler and endpoint health | Release 1 | FR-V12-R-041…047; ENT-API-05 | Outbox events; schedule ticks | Sign and deliver; schedule retries 5 m/30 m/2 h/6 h/15 h ±10%; disable on 410; flag endpoints with 3 exhausted events in 24 h; SSRF re-check per delivery | Delivery rows, events, notifications | L3 (data delivery of tenant-subscribed references, no consequential effect) | References only; SSRF guard; no redirects | Worker crash → resume from `next_attempt_at`; duplicates prevented by unique (endpoint, event, attempt) | Delivery success ≥ 99% within 24 h for healthy endpoints; p95 first-attempt latency ≤ 5 s | Compute in existing workers; 2/3/4 pd |
| AU-295 | Connector gate, health and DLT registry sync | Release 1 | FR-V12-R-056…080; ENT-INT-03/04/05; GC-15 | Activation request; every 5 min health; daily DLT template sync; weekly idle scan | Evaluate gate evidence (incl. rule-pack approval per market); compute lag, error rate, breaker state; sync DLT template status from the aggregator; flag idle connectors | Gate checklist, health metrics, `connector.degraded`, template suspensions, FinOps findings | L3 for health and template suspension (blocks sends); activation itself is human-approved | Never activates a connector; never deletes idle connectors | Aggregator sync failure → templates keep last known state for 24 h, then HOLD promotional sends | 0 activations with incomplete evidence; MTTD of degradation ≤ 5 min | ₹0; 3/4/6 pd |
| AU-296 | Vercel data-path conformance monitor | Release 1 | FR-V12-R-081…095; DEC-786; VD-01…12 | Every deployment (CI) and daily | Read project settings and deployments through the Vercel API; assert regions, domains, env vars, analytics settings, rewrites, log drain fields; weekly sample of 1,000 log lines scanned for body/token patterns | `edge_conformance_check` rows, findings, deployment block | L3 (blocks non-conforming deployment; rollback runbook human-run) | Read-only on Vercel except deployment-check status | API unavailable → deployment blocked (fail closed) | 100% deployments checked; 0 production requests served from a non-zone region | ₹0; 2/3/4 pd |
| AU-297 | RPO monitor and restore-drill orchestrator | Release 1 | FR-V12-R-096…110; DEC-787; KPI-18/19/32 | Every 30 s sampling; drill schedule (release gates, quarterly) | Compute replication lag, WAL archive age, base-backup age, PITR status; thresholds 5/10/15 min; drill orchestration: create isolated restore target, run path steps, PRV pack, compute achieved RPO/RTO | `rpo_sample`, pages, `restore_drill` records, release-blocker flag | L3 for monitoring; drills run in isolated targets only; production failover is human-led | Never touches production during a drill; never deletes backups | Monitor failure → page "RPO monitor blind" | 100% of samples ≤ 15 min; drills pass at every gate | Restore-target compute ≈ ₹500–1,500 per drill; 3/5/7 pd |
| AU-298 | Model registry re-certification and eligibility guard | Release 1 | FR-V12-R-111…130; DEC-788; DEC-890; AIX-02 | Daily; provider notices; EVAL regression event; price change > 20% | Check `recert_due`, DPA validity, zone processing records, EVAL status per task/locale, red-team freshness (≤ 12 months), price vs recorded CPAR; suspend lapsed rows; recompute eligible-row cache for AU-151/152 | Row state changes, `ai.model.recert_due`, route-cache refresh, R10 tasks | L3 for suspension (policy-defined); approval and re-approval are human (two-person) | Never approves; never routes to a non-approved row; suspension of the only eligible row → HOLD/Tier 3, not fallback to unapproved | Data source unavailable → keep state, flag "evidence stale" after 7 days → suspend | 0 calls routed to rows with lapsed evidence | ₹0; 2/3/5 pd |
| AU-299 | Benchmark aggregator and privacy-budget accountant | Release 2 | FR-V12-R-131…142; DEC-789; DEC-893 | Monthly (day 3, zone time) | Per enrolled tenant call `bench_contribute`; per cohort apply exclusions, k ≥ 10, dominance ≤ 30%, merge-up rule, ε budget check, Laplace noise, rounding; publish zone cells; compose global cells from noised zone cells; ledger | `benchmark_cell`, `benchmark_privacy_ledger`, events | L3 (internal aggregate publication under fixed rules) | No tenant-level value leaves the tenant context except clipped contributions under a non-reversible hash; never publishes k < 10 | Any step failure → no publication this period (previous values remain) | 0 cells published with k < 10; 0 re-identification findings in annual privacy review | Compute ≈ ₹0–500/month; 3/5/7 pd (part of R-WP19) |

---

### 11.19.5.10 Functional requirement register (FR-V12-R-001…155)

{{FR}}

---

### 11.19.5.11 Architecture decision records (ADR-255…264)

| ADR | Title | Context | Decision | Consequences | Status |
|---|---|---|---|---|---|
| ADR-255 | Tenant federation through the reused IdP as broker | DEC-003/019 reuse; DEC-784 SSO in R1 | Broker per tenant connection in the reused IdP; product stores connection metadata, policy and HRD; fallback in-product SP behind a flag if Sprint 0 check 13 fails | One token format and session model; dependency on the IdP team (DP-15) for connection provisioning automation | Accepted (DEC-880) |
| ADR-256 | In-product SCIM 2.0 server per zone | ENT-IDN-03 in R1 (DEC-881) | Thin SCIM service in `core.identity` (or django-scim2 if it passes conformance), zone-bound tokens, approval for group mappings | Small surface; conformance suite in CI; IdP-specific quirks handled in a compatibility layer | Accepted |
| ADR-257 | Developer credentials: zone-bound API keys and OAuth client credentials | ENT-API-01/02 in R1 | Key format with zone; JWT access tokens from `private_key_jwt`; no consequential scopes | No cross-zone lookups; tenants must use region host; client libraries handle both | Accepted (DEC-882/883) |
| ADR-258 | Native webhook engine on Celery | ENT-API-05 | Outbox-driven delivery with HMAC signatures, fixed schedule, verification challenge, SSRF guard | No extra service to run (Part 11.8b rejected Svix OSS for operations load); throughput within existing workers | Accepted |
| ADR-259 | Connector framework with platform-owned consent and per-field policies | DEC-785; X-09 withdrawn | CF-01…12 contract; CRM adapters for Zoho, HubSpot, Salesforce; protected fields platform-wins-stricter; DLT registry | Tenants keep their CRM; platform stays authoritative for consent/approvals; more simulators to maintain | Accepted (DEC-884/885) |
| ADR-260 | Regional Vercel projects with personal-data controls | DEC-786 | Project per surface per zone; function region pin; VD-01…12 enforced in CI and by AU-296 | Two more projects per new zone; clear residency evidence; edge transit documented (DEC-887) | Accepted (DEC-886) |
| ADR-261 | Dual-path recovery: Supabase PITR plus in-zone WAL-G standby | DEC-787, DEC-771 | P1 PITR, P2 logical replica with WAL-G 35 days, P3 dumps; drills per gate | Survives provider loss; extra AWS instance cost; logical replication limits (DDL, sequences) handled in CI and runbook | Accepted (DEC-888/889) |
| ADR-262 | Provider-neutral model registry as the only routing source | DEC-788 | Registry rows by provider × version × hosting × zone × modality; two-person approval; AU-298 re-certification; zone-aware routing | Any provider can be added by evidence, not code; DEC-418 primary preserved through approval | Accepted (DEC-890…892) |
| ADR-263 | Tenant-level differential privacy for benchmarks | DEC-789 | Clipped per-tenant contributions, k ≥ 10, dominance rule, Laplace ε = 0.5/month, zone-local computation | Stronger guarantee than k-anonymity alone; small cohorts suppressed; values noisy by design | Accepted (DEC-893) |
| ADR-264 | Canonical least-privilege database roles on Supabase | DEC-778 | `app_*` roles NOBYPASSRLS; Data API off; `service_role` only CI break-glass; CI assertions and drift detection | Closes RLS bypass; requires rename migration of Part 11.9b names | Accepted (DEC-894) |

---

### 11.19.5.12 Cut-over into Release 1 (implementation plan in the Part 8.1 format)

Dates follow the work (DEC-770); the master plan (Part 11.20) places these sprints on the calendar. Sprint numbers below are **relative Release 1 build sprints** (2-week cadence, Part 8.1 §8.1.4.1).

**Sprint-by-sprint allocation (P4 capabilities only).**

| Sprint | C1 Identity | C2 Developer platform | C3 Connectors | C4 Vercel | C5 RPO | C6 Registry | C8 DB roles | Gate / exit evidence |
|---|---|---|---|---|---|---|---|---|
| S0 | Identity spike check 13 (Okta, Entra, Google) | — | Provider sandboxes requested (Zoho, HubSpot, Salesforce dev orgs; aggregator and CPaaS test accounts) | Projects `web-in`, `admin-in`, `developers`; VD policy as code | — | — | Canonical roles, Data API off, CI assertions | Spike report; SA checks green |
| S1 | DDL-V12-R-01…04 | Developer host, key format | — | DPA signed; sub-processor list | PITR on; `recovery_path` | DDL-V12-R-14; seed rows | Rename migration; AU-292 DB probes | Migrations green |
| S2 | SSO config, test login, HRD | OAuth CC, token endpoint | — | BFF allowlist, origin verify, lint | Standby + WAL-G | Two-person approval UI | — | TC-V12-R-001…010, 021…026 |
| S3 | Enforcement, break-glass, policy | Webhooks engine | Framework + gate (CN-C1) | AU-296 | AU-297 monitor | AU-151/152 zone routing | — | M04, M05, M06 rows green |
| S4 | SCIM server | Webhook UI, replay; SDK pipeline | SMS-DLT; Zoho | — | First drill (P1, P2) | AU-298 | — | M02 rows; drill passed |
| S5 | Custom roles, SoD, recert | Sandbox + promotion; portal | HubSpot | — | — | EVAL-PRG-1 suites | — | M03 rows; TC-V12-R-034…036 |
| S6 | SIEM, audit export, JIT | SDK 1.0 RC (TS, Python, Java) | Salesforce; Voice transport | — | — | Candidate REG-005 evaluation | — | M07 rows (all connectors) |
| S7 (hardening) | Pen test scope SSO/SCIM | Pen test scope developer host | DLT live; India pack approved | 30 days of passing checks | Gate drill | Founder approval record attached | Blocking suites | Release 1 go/no-go items below |

**Feature flags (per release, default off until the activation gate passes).**

| Flag | Scope | Default | Turned on by | Gate |
|---|---|---|---|---|
| `sso.enabled` | tenant | off | R12 after test login | ENT-IDN-01 acceptance |
| `sso.enforced` | connection | off | R12 + second approver | Verified domain + break-glass |
| `scim.enabled` | tenant | off | R12 | Token issued; mapping approved |
| `roles.custom.enabled` | tenant | on (R1) | — | SoD suite green |
| `developer.api.enabled` | tenant | off | R12 | Entitlement (SKU) |
| `webhooks.enabled` | tenant | off | R12 | Endpoint verified |
| `connector.<provider>.enabled` | installation | off | R10 approval | CF-11 + rule pack |
| `benchmarks.enabled` | platform | off until Release 2 | Platform owner | DPIA + legal clause |
| `ai.registry.row.<REG>` | platform | per state | Two-person approval | Evidence complete |
| `idp_broker_fallback` | platform | off | Platform owner | Spike check 13 failed |

**Release 1 go/no-go items added by this part.**

| # | Item | Evidence | Owner |
|---|---|---|---|
| GNG-R-01 | SSO works with Okta, Entra ID, Google and one generic SAML and one generic OIDC IdP; enforcement and break-glass verified | TC-V12-R-001…010; M01 3-way rows green | IAM lead |
| GNG-R-02 | SCIM conformance and de-provisioning SLA (≤ 60 s product, ≤ 15 min end to end) | TC-V12-R-011…016; AU-291 ledger | IAM lead |
| GNG-R-03 | SoD enforced at API, DB, assignment and SCIM paths | M03 rows | Security lead |
| GNG-R-04 | Developer platform: keys, OAuth, webhooks, SDK 1.0 in three languages, portal, sandbox | TC-V12-R-021…036; M04–M06 | Platform lead |
| GNG-R-05 | Connectors activated only through the gate; DLT live; India pack approved | M07 rows; activation log | Integration lead + Legal |
| GNG-R-06 | VD-01…12 green for 30 days; Vercel DPA and sub-processor notice | AU-296 evidence | Privacy lead |
| GNG-R-07 | Restore drill at the gate: RPO ≤ 15 min, growth RTO ≤ 120 min (KPI-32 blocking) | `restore_drill` record | DBRE / SRE |
| GNG-R-08 | Registry: only approved rows routable; REG-002 approval record; zone routing tests | M10, M13 rows | LLM platform lead |
| GNG-R-09 | Supabase access model: no app role can bypass RLS; Data API off; no `service_role` in runtime | M12 rows; CI assertions | DBRE |
| GNG-R-10 | Pen test #1 (incl. SSO, SCIM, developer host, webhooks) with no open critical/high | Report | Security lead |

**Risks (Part 8.2 format).**

| ID | Risk | Likelihood | Impact | Mitigation | Owner | Trigger |
|---|---|---|---|---|---|---|
| RSK-V12-R-01 | Reused IdP cannot broker per-tenant SAML/OIDC | Medium | High (C1 slips) | Fallback in-product SP behind flag (ADR-255) | IAM lead | Spike check 13 fails |
| RSK-V12-R-02 | Salesforce edition limits (API access, CDC) block some tenants | Medium | Medium | Polling fallback; edition check in gate; document requirements | Integration lead | Tenant edition lacks API |
| RSK-V12-R-03 | DLT registration delays for owned startups | High | Medium | Start registration in S0; transactional first | Growth/compliance | Registration > 3 weeks |
| RSK-V12-R-04 | Supabase PITR retention < 35 days | Medium | Low (P2 covers) | P2 WAL-G 35 days | DBRE | Plan options at implementation |
| RSK-V12-R-05 | Logical replication lag under bulk loads | Medium | Medium | Batch sizes, monitor, slot sizing | DBRE | Lag > 5 min |
| RSK-V12-R-06 | No EU processing location for a needed model | Medium | Medium | HOLD/Tier 3 for EU; alternative approved rows | LLM platform lead | Before first EU tenant |
| RSK-V12-R-07 | Edge transit position not accepted by EU counsel | Low | High | Vercel enterprise options or EU-only AWS CloudFront fallback for EU surfaces | Privacy lead | Counsel opinion |
| RSK-V12-R-08 | Fewer than 10 opted-in tenants per cohort for long | High | Low | Merge-up rule; communicate; no publication | Product | — |
| RSK-V12-R-09 | Scope added to Release 1 extends dates | High | Medium | Funded and dates follow work (DEC-770/790); parallel streams | Delivery lead | Re-plan |
| RSK-V12-R-10 | Three SDK languages increase maintenance | Medium | Low | Generated core, thin helpers, contract tests | Platform lead | — |

---

### 11.19.5.13 Effort and cost (proposal CR-V12-R-01; funded under DEC-790; development and running in separate tables)

Rates ₹4,545 / 5,682 / 6,818 per person-day (Part 8.4 §8.4.2.1), low × low rate, central × central, high × high. Estimates; AI-built delivery (DEC-420) may reduce effort after calibration; not assumed. **Overlap:** CR-V12-H-01 (Part 11.8b §11.8.5.15) already estimated H1 developer platform, H2 identity APIs, H3 access/audit, H7 connector framework and part of H8 (one CRM + SMS-DLT); AU-151/152 were estimated in Part 11.6b. The net column removes that overlap so the same work is not funded twice.

**Development (one-time).**

| WP | Cap. | Scope | pd low / central / high | ₹ low / central / high |
|---|---|---|---|---|
| R-WP01 | C1 | SSO broker integration, IdP connections, domains, policy, break-glass, A203 tabs | 14 / 20 / 28 | 0.64 / 1.14 / 1.91 L |
| R-WP02 | C1 | SCIM 2.0 server, tokens, group mapping, revocation worker, conformance runs | 12 / 17 / 24 | 0.55 / 0.97 / 1.64 L |
| R-WP03 | C1 | Custom roles, permission catalogue, SoD triggers, recertification, SIEM and audit export, JIT ticket | 10 / 15 / 21 | 0.45 / 0.85 / 1.43 L |
| R-WP04 | C2 | API keys with zone, OAuth client credentials, token and revocation endpoints, rate limits | 8 / 12 / 17 | 0.36 / 0.68 / 1.16 L |
| R-WP05 | C2 | Webhook engine, signing, schedule, verification, SSRF guard, log and replay | 7 / 10 / 14 | 0.32 / 0.57 / 0.95 L |
| R-WP06 | C2 | SDKs TypeScript, Python, Java: generation, helpers, signing, publishing | 9 / 13 / 19 | 0.41 / 0.74 / 1.30 L |
| R-WP07 | C2 | Developer portal W47, changelog, deprecation tooling | 4 / 6 / 9 | 0.18 / 0.34 / 0.61 L |
| R-WP08 | C2 | Sandbox tenants, synthetic guards, promotion workflow A204 | 7 / 10 / 14 | 0.32 / 0.57 / 0.95 L |
| R-WP09 | C3 | Connector framework base, gate service with rule-pack check, A008 tab, health | 6 / 9 / 13 | 0.27 / 0.51 / 0.89 L |
| R-WP10 | C3 | Zoho CRM adapter | 7 / 10 / 14 | 0.32 / 0.57 / 0.95 L |
| R-WP11 | C3 | HubSpot adapter | 7 / 10 / 14 | 0.32 / 0.57 / 0.95 L |
| R-WP12 | C3 | Salesforce adapter incl. CDC/JWT bearer | 9 / 13 / 18 | 0.41 / 0.74 / 1.23 L |
| R-WP13 | C3 | SMS-DLT adapter, DLT registry, PDP rules, STOP | 7 / 10 / 14 | 0.32 / 0.57 / 0.95 L |
| R-WP14 | C3 | Voice CPaaS transport, number series, status reconciliation | 6 / 9 / 13 | 0.27 / 0.51 / 0.89 L |
| R-WP15 | C4 | Vercel per-zone projects, VD-01…12 policy as code, BFF header allowlist, lint, log drain | 5 / 8 / 11 | 0.23 / 0.45 / 0.75 L |
| R-WP16 | C5 | WAL-G standby, logical replication, CRR, monitor, PRV pack, runbooks, first drills | 9 / 13 / 18 | 0.41 / 0.74 / 1.23 L |
| R-WP17 | C6 | Registry DDL, two-person approval, zone routing, pins, kill switch, canary | 9 / 13 / 18 | 0.41 / 0.74 / 1.23 L |
| R-WP18 | C6 | Candidate evaluations (4 candidates × EVAL subsets, red-team) | 8 / 12 / 20 | 0.36 / 0.68 / 1.36 L |
| R-WP19 | C7 | Benchmarks: contribution function, aggregator, DP noise, ledger, A042 tab | 10 / 15 / 21 | 0.45 / 0.85 / 1.43 L |
| R-WP20 | C8 | Canonical roles, rename migration, CI assertions, drift detection | 3 / 5 / 7 | 0.14 / 0.28 / 0.48 L |
| R-WP21 | All | Automations AU-290…299 wiring, dashboards, alerts | 6 / 9 / 13 | 0.27 / 0.51 / 0.89 L |
| R-WP22 | All | Tests: 86 full-form + 1,072 generated cases, harnesses, simulators (IdP, SCIM, CRM, SMS, voice, webhook receiver) | 20 / 30 / 42 | 0.91 / 1.70 / 2.86 L |
| **Gross** | | | **183 / 269 / 382** | **₹8.32 / 15.28 / 26.04 L** |
| Less overlap | | CR-V12-H-01 H1, H2, H3, H7 and the CRM + SMS lines of H8 | −63 / −93 / −129 | −₹2.86 / −5.28 / −8.80 L |
| **Net new (CR-V12-R-01)** | | | **120 / 176 / 253** | **₹5.45 / 10.00 / 17.25 L** |
| Per-zone repeat (EU) | C4, C5 | EU projects, standby, drills, EU counsel items | 4 / 6 / 9 | ₹0.18 / 0.34 / 0.61 L |

**External one-time costs (verify quotes).**

| Item | ₹ estimate | Basis |
|---|---|---|
| Pen-test scope extension (SSO, SCIM, developer host, webhooks, connectors) | 1.5–3.0 L | Added days on the R1 pen test |
| Independent review of the differential-privacy implementation | 1.0–2.5 L | Privacy scientist, 3–6 days |
| Legal: Vercel DPA review, CRM transfer entries, contract clause BM-CL-1, edge-transit opinion (IN, EU) | 2.0–5.0 L | Counsel hours |
| DLT entity/header/template registration per owned startup | 0.1–0.3 L | Operator portal fees (verify) |
| IdP developer tenants, CRM developer orgs, aggregator/CPaaS test accounts | 0 | Free developer programmes (verify) |
| **Total external** | **₹4.6–10.8 L** | |

**Running (recurring, per month, IN cell; verify at implementation, as of 27 Nov 2026).**

| Line | Item | ₹ / month | Basis |
|---|---|---|---|
| B-R01 | AWS standby PostgreSQL (memory-optimised instance + gp3 storage, multi-AZ storage) | 9,000–18,000 | Replaces the DEC-771 standby line (₹3,600–5,400) → net +5,400–12,600 |
| B-R02 | S3 WAL archive + base backups (35 days, delta backups) + CRR to Hyderabad | 1,500–4,500 | 0.5–1.5 TB-month × S3 price + replication transfer |
| B-R03 | Supabase PITR at maximum retention | 0–9,000 | 7-day PITR already in DEC-771; longer retention option uplift (verify) |
| B-R04 | Vercel log drains and per-zone projects | 0–4,000 | Plan feature pricing (verify); projects within plan |
| B-R05 | Developer host WAF rules and webhook egress NAT | 1,000–3,000 | WAF rule/request charges; NAT data |
| B25 (from 11.8b) | SMS-DLT pilot volume | 300–1,000 | Unchanged |
| B-R06 | Voice CPaaS: numbers (140 and 160 series) + minutes at pilot volume | 1,500–6,000 | Number rental and per-minute (verify) |
| B-R07 | Registry: candidate evaluation calls | 2,000–8,000 | EVAL replays for candidates (B23 extension) |
| B-R08 | Open-weight self-hosted row (only if REG-005 approved): CPU small model / GPU | 5,000–12,000 CPU · 35,000–90,000 GPU | Conditional; only after approval and cost-per-accepted-result comparison |
| B-R09 | Benchmarks compute | 0–500 | Monthly batch |
| — | CRM, SIEM, warehouse | 0 | Tenant-owned (BYO) |
| **Total (without B-R08)** | | **₹15,300–54,000** | Net of DEC-771 standby: ₹11,700–48,600 |
| EU cell (at first EU contract) | B-R01…B-R05 again | ₹11,500–38,500 | DEC-772 adds the hosting copy; these lines are additional |

---

## Quality gate: Batch 11.19b

| # | Item | Result | Notes |
|---|---|---|---|
| 1 | Every requirement traced to a source | **Pass** | 155 FRs with source column |
| 2 | Assumptions, gaps and conflicts tagged | **Pass** | Registered in Part 11.19c §11.19.9 |
| 3 | IDs unique and consistent | **Pass** | FR-V12-R-001…155, AU-290…299, ADR-255…264, RSK-V12-R-01…10, DDL-V12-R-13…16, API-V12-R-043…052 |
| 4 | No story lacks AC; no requirement lacks a test | **Pass** | Every FR names a test or model; stories in Part 11.19c |
| 5 | Negative, edge, security, accessibility | **Pass** | Runbooks, threat tables, generated models M09–M13 |
| 6 | No automation lacks guardrail, fallback, KPI, cost | **Pass** | AU-290…299 table complete; no new agents |
| 7 | Time-sensitive facts flagged | **Pass** | Supabase options, provider regions, prices marked verify (as of 27 Nov 2026) |
| 8 | No restricted data to free-tier models | **Pass** | `ai_model_free_tier_data_ck`; open-weight masked only; M10 oracle |
| 9 | Consistent with earlier parts | **Pass with reported items** | CONFLICT-1092/1094/1095 resolved here; Part 11.9b and 11.13b not edited |

**Status: Part 11 Batch 11.19b complete. C5–C8, automations, FR register, ADRs, cut-over and costs written; continued in Part 11.19c.**
