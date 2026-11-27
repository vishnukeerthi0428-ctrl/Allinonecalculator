#### 4.4.3.1 Document 18

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| I-18-023 | Threat model and governance controls | Unauthorized extraction: scope export, approve manifest hash, short-lived link, revoke | **Partially covered** | Part 2.4 exports; AL-35 | Export manifest hash approval added as rule | FR-ENH-I-012 |
| I-18-028 | Capacity, reliability and recovery acceptance | Owned startups / external tenants 25/10 initial, 50+/100 growth | **Conflict** | DEC-031 (40/10 Y1; 100/30 Y2) | Test workload profiles added; conflict raised | CONFLICT-461; WP-01, WP-02 |
| I-18-029 | Capacity, reliability and recovery acceptance | Concurrent staff sessions 50 / 250 | **Conflict** | DEC-031 internal users 60/200; Part 4.2 §4.25.3 | As above | CONFLICT-461; WP-01, WP-02 |
| I-18-030 | Capacity, reliability and recovery acceptance | Scoped opportunities 100,000 / 1,000,000 | **Not covered** | No opportunity-volume design point | Seeded volume added to workload profiles | WP-01, WP-02; LT-ENH-I-01 |
| I-18-031 | Capacity, reliability and recovery acceptance | Concurrent jobs 50/250; scheduled actions 10,000/100,000 per day | **Conflict** | Part 4.2 §4.25.3 (≈1,154 msgs/day Y1) | Adopted as stress workload; conflict raised | CONFLICT-461; LT-ENH-I-02 |
| I-18-034 | Capacity, reliability and recovery acceptance | Projection refresh ≤ 60 s | **Conflict** | NFR-008 (360 ≤ 60 s) vs NFR-047 (dashboards ≤ 15 min) | Conflict raised | CONFLICT-463 |
| I-18-035 | Capacity, reliability and recovery acceptance | Critical RPO ≤ 15 min; RTO ≤ 4 h initial, ≤ 2 h growth | **Conflict** | DEC-018; NFR-056/057 | Growth RTO conflict raised | CONFLICT-462 |
| I-18-036 | Capacity, reliability and recovery acceptance | Regenerable research data RPO ≤ 24 h / RTO ≤ 8 h | **Not covered** | No recovery class for regenerable data | Recovery class RC-2 added | GAP-462; FR-ENH-I-020 |
| I-18-043 | Website and confidential Admin operating contract | Emergency unpublish and revoke access without deleting authoritative evidence | **Partially covered** | RB-004; BRL-PUB | Public-content incident runbook added | RB-017 |
| I-18-044 | Open-source supply chain and external-service controls | SBOM, pinned versions, licence review incl. copyleft, network-use terms, separately licensed model weights | **Partially covered** | PL-09/PL-10; Part 4.1 §4.16.1; GL-L06 | Model-weight and network-use licence rule added | CS-DEP-04 |
| I-18-077 | Implementation acceptance and verification (15 procedures) | Authorization-safe cache key: product, tenant, startup, principal/grant fingerprint, permission, policy, model, knowledge revisions, normalized query | **Partially covered** | Part 3.1 §3.1.11 (scope + revision only) | Key composition standard added | CS-SEC-07; FR-ENH-I-010; RECOMMENDATION-467 |
| I-18-078 | Implementation acceptance and verification (15 procedures) | Numeric validation: reject invalid weights, non-finite inputs, negative counts, out-of-range ratios | **Not covered** | No numeric guardrail rule | Rule and tests added | CS-PY-09; FR-ENH-I-011; RECOMMENDATION-473 |

Covered and not-applicable aspects (grouped by section):

| Section | Aspect IDs | Status | Blueprint location (representative) |
|---|---|---|---|
| Purpose and operating boundary | 001 | Not applicable | Part 0 §0.1; Part 1; DEC-009 |
| Current design scope | 002 | Not applicable | Part 2.5; Part 3.2; Part 3.3 |
| Product-specific application / Business controls | 003 | Not applicable | Part 2.2 WF-08…WF-10; Part 2.3 BRL |
| Completion and approval / Acceptance and evidence record | 004 | Covered | Part 8.2 §8.2.4.2; Part 6.1 §6.1.5.4 EVR |
| Implementation, verification and delivery controls (preamble) | 005 | Not applicable | BRD §13.2, §16; BLK-11 |
| Initial startup configurations / technology principles | 006 | Not applicable | Part 1 §1.2; Part 3.1 §3.1.8 |
| Authority and data protection | 007, 008, 009, 010, 011, 012, 013, 014 | Covered | Part 2.3 R01, ABAC-01; DEC-065; Part 2.3 R02–R07; BRL-TEN-12; DEC-038; BRL-APR; DEC-064; Part 2.3 R12; SoD rules; DEC-056 SupportAccessGrant; BRL-TEN-09; Par… |
| Threat model and governance controls | 015, 016, 017, 018, 019, 020, 021, 022, 025, 026, 027 | Covered | Part 4.1 TB-09, NFR-031/032; Part 4.1 TB-04; Part 4.1 §4.15; NFR-005, ADR-023; Part 4.1 §4.6, RB-009, RB-013; BRL-AI-08, NFR-022, RB-005; Part 4.1 §4.11–4.12… |
| Threat model and governance controls | 024 | Not applicable | Investor product out of scope (DEC-009) |
| Capacity, reliability and recovery acceptance | 032, 033, 037 | Covered | Part 4.2 §4.24 C10 (800 ms p95, stricter); NFR-051, C6 (stricter); DEC-044; NFR-062 |
| Website and confidential Admin operating contract | 038, 039, 040, 041, 042 | Covered | NFR-001; Part 4.1 §4.1.3 trust zones; Part 3.2 namespaces; Part 4.1 §4.9; NFR-020; ADR-010; BRL-TEN-10; ARP-03/04; Part 3.1 §3.1.7.1; Part 4.1 TB-01, TB-02 |
| Open-source supply chain and external-service controls | 045, 046, 047, 048, 049 | Covered | PL-09/11; Part 4.1 §4.9; BRL-SRC; FR source policy; Part 4.1 §4.14; Part 4.1 §4.16; Part 6; BLK-1…BLK-4 |
| Product security and governance controls (table) | 050, 051, 052, 053, 054, 055 | Covered | Part 4.1 §4.1–4.4, §4.11, §4.17 |
| Threat-control implementation matrix | 056, 057, 058, 059, 060, 061 | Covered | Part 4.1 §4.8.2; NFR-001/032; Part 6 |
| Implementation acceptance and verification (15 procedures) | 062, 063, 064, 065, 066, 067, 068, 069, 070, 071, 072, 073, 074, 075, 076, 079 | Covered | NFR-003; AP-10; NFR-032; AP-10; NFR-050; DEC-064; BRL-AUT; EP-20; FR-W31…W34; NFR-015; ADR-022; Part 6.4 AIE; NFR-028; US-0101; BLK-9; NFR-001; NFR-095; DEC-… |
| Current scope: security and applicant draft | 080, 081 | Covered | DEC-019; ARP-05; Part 3.3 ENT-187 saas_application_draft; BRL-SVC-02; FRD §16.3 |

#### 4.4.3.2 Document 25

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| I-25-007 | Repository and change discipline | Acceptance: dependency graph proves no cross-product runtime import | **Partially covered** | NFR-085 (module contracts only) | Cross-product import contract added | CS-GEN-03; TC-ENH-I-001 |
| I-25-009 | Repository and change discipline | Emergency fixes follow same audit trail with expedited reviewer | **Partially covered** | Part 4.3 hotfix row | Expedited-review rule added | CS-REV-09 |
| I-25-010 | Repository and change discipline | AI-assisted coding: treat generated code as untrusted; never paste secrets/real records; no invented APIs | **Not covered** | None (B09 seats only) | AI-assisted coding policy added | CS-AIC-01…08; GAP-460 |
| I-25-011 | Frontend engineering | TypeScript strict; validate server payloads at boundaries; no any for business/financial fields; generated contracts | **Partially covered** | Part 4.3 PL-03; Part 3.1 Zod | Full TS standard | CS-TS-01…10 |
| I-25-012 | Frontend engineering | React: separate presentation, query hooks, mutation services; no side effects during render; cancel stale requests | **Partially covered** | NFR-027; Part 3.1 TanStack Query | Full React standard | CS-RE-01…12 |
| I-25-013 | Frontend engineering | Component tests cover loading, error, denied and empty states | **Partially covered** | Part 2.5 UI states | Test rule added | CS-TEST-06 |
| I-25-014 | Frontend engineering | Scope-aware query keys (product, tenant, startup, audience, filters, identity); clear caches on switch/logout; no private payload in service worker | **Partially covered** | NFR-027; FR-UIS-01 | Query-key standard added | CS-RE-04…06 |
| I-25-015 | Frontend engineering | Forms: client validation for UX, server for authority; sanitize rich content; disable duplicate submit; show approval requirement | **Partially covered** | Part 2.5 forms | Form standard added | CS-RE-08…10 |
| I-25-017 | Backend and persistence | Python: type hints, explicit DTOs, narrow exceptions, Ruff; no silent catch-all | **Partially covered** | Part 4.3 tooling row | Python standard | CS-PY-01…10 |
| I-25-018 | Backend and persistence | Django: views authenticate/validate; service owns transaction and transition; selectors enforce scope; no logic only in UI or signals | **Not covered** | Not specified | Service/selector layering standard | CS-DJ-01…10 |
| I-25-019 | Backend and persistence | DRF: allowlist fields, deny by default, scope queryset before lookup, bounded pagination, validated sort/filter, safe error + correlation ID | **Partially covered** | NFR-015; PL-05 __all__ ban | DRF standard | CS-API-01…12 |
| I-25-027 | Review and definition of done | Reviewer examines acceptance, role, scope, finance, error paths, schema, tests, cost, rollback; record tradeoffs | **Partially covered** | Part 4.3 §4.32.2 checklist | Full review checklist by risk class | CR-CHK-01…40 |
| I-25-028 | Review and definition of done | Changed-line coverage ≥ 80% on eligible domain code; critical decision branches tested; generated code excluded only with approval | **Conflict** | NFR-082 (overall coverage) | Diff-coverage gate added; conflict raised | CONFLICT-468; CS-TEST-03 |
| I-25-029 | Review and definition of done | Completion: merge only after UI/API/table links updated, evidence attached, operational impact assessed | **Partially covered** | Part 5 DoD | DoD code addendum | CS-REV-12 |
| I-25-031 | Code review rules and repository layout (table) | Frontend lead: strict TS, accessible, scoped keys, abort stale, no browser credentials | **Partially covered** | As above | Standard | CS-TS, CS-RE |
| I-25-032 | Code review rules and repository layout (table) | Backend lead: small services, serializer validation, authorization in service, transaction/outbox, deterministic errors | **Partially covered** | As above | Standard | CS-DJ |
| I-25-034 | Code review rules and repository layout (table) | Tech lead review: scope, security, failure modes, migrations, unit/SIT, maintainability; no AI code merged without human review | **Partially covered** | Part 4.3 §4.32.2 | Standard | CS-REV, CS-AIC |
| I-25-036 | Reference code patterns | Correct scoped lookup pattern (membership check then filtered get) | **Partially covered** | ARP-02 principle only | Pattern P-01 with negative example | P-01 |
| I-25-037 | Reference code patterns | React stale-response protection with AbortController and live flag | **Not covered** | Not specified | Pattern P-02 | P-02 |
| I-25-038 | Reference code patterns | Safe financial arithmetic with Decimal; validate currency, entity, provider reference | **Partially covered** | ADR-030 | Pattern P-03 | P-03 |
| I-25-042 | Practical implementation rules (code acceptance table) | PostgreSQL: composite scoped FKs, unique idempotency keys, numeric money, no cascade deleting posted records | **Partially covered** | NFR-017/018 | No-cascade rule added | CS-SQL-07 |
| I-25-044 | Practical implementation rules (code acceptance table) | Review: run lint/type/unit/integration in actual repos; review generated code, deps, scope, concurrency, rollback | **Partially covered** | Part 4.3 §4.33 | Review checklist | CR-CHK |
| I-25-046 | Implementation acceptance procedures (9) | Query and rendering efficiency (query count, EXPLAIN ANALYZE, React profiler) | **Partially covered** | Part 3.1 lever 1 | Added | CS-PERF-01…08; TC-ENH-I-003 |
| I-25-048 | Implementation acceptance procedures (9) | Shared library boundaries (wrong product config) | **Partially covered** | NFR-031 | Added | TC-ENH-I-002 |
| I-25-049 | Implementation acceptance procedures (9) | Repository and modular boundaries (owner, tests, public interface) | **Partially covered** | NFR-085 | Added | CS-GEN-04 |
| I-25-053 | Implementation acceptance procedures (9) | AI-assisted coding quality | **Not covered** | — | Added | CS-AIC; TC-ENH-I-004 |
| I-25-054 | Current scope: coding standards | Typed dynamic forms and explicit capability predicates; no hardcoded startup position; safe rendering | **Partially covered** | FR config-driven forms (CFG) | Rule added | CS-RE-11; CS-GEN-06 |

Covered and not-applicable aspects (grouped by section):

| Section | Aspect IDs | Status | Blueprint location (representative) |
|---|---|---|---|
| Purpose and operating boundary | 001 | Not applicable | Part 0 §0.1; Part 1; DEC-009 |
| Current design scope | 002 | Not applicable | Part 2.5; Part 3.2; Part 3.3 |
| Product-specific application / Business controls | 003 | Not applicable | Part 2.2 WF-08…WF-10; Part 2.3 BRL |
| Completion and approval / Acceptance and evidence record | 004 | Covered | Part 8.2 §8.2.4.2; Part 6.1 §6.1.5.4 EVR |
| Implementation, verification and delivery controls (preamble) | 005 | Not applicable | BRD §13.2, §16; BLK-11 |
| Repository and change discipline | 006, 008 | Covered | Part 4.3 §4.32.1 ADR-060; import-linter; Part 4.3 §4.32.2 |
| Frontend engineering | 016 | Covered | NFR-088/089; Part 2.5 §2.46 |
| Backend and persistence | 020, 021, 022 | Covered | NFR-017; Part 3.3; ARP-03; NFR-006, NFR-025; ADR-023; NFR-016, NFR-026; DEC-050 |
| AI and integration engineering | 023, 024, 025, 026 | Covered | Part 7.2 agent specs; BRL-AI-09; ADR-041; Part 4.1 §4.15; ADR-009; ARP-06; Part 4.3 §4.39.1; NFR-078 |
| Code review rules and repository layout (table) | 030, 033, 035 | Covered | Part 4.3 §4.32.1 (equivalent monorepo layout); NFR-017; Part 4.3 §4.33.2 PL-02…PL-11 |
| Reference code patterns | 039 | Covered | BLK-6; FRD §12.1 worked example |
| Practical implementation rules (code acceptance table) | 040, 041, 043 | Covered | NFR-001; NFR-027; NFR-025; ARP-02/03; ARP-08; BRL-AI-07 |
| Implementation acceptance procedures (9) | 045, 047, 050, 051, 052 | Covered | NFR-021; PL-09; NFR-005; ADR-023; ADR-009, ADR-027; Part 2.5 §2.45; RECOMMENDATION-017 |

#### 4.4.3.3 Document 26

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| I-26-008 | Deployment topology | Separate research, AI, communication, financial and priority control queues; one scheduler per scope; prefetch/limits; bounded retries | **Conflict** | ADR-021 (no finance or control queue; prefetch not set) | Queue additions proposed | CONFLICT-473; FR-ENH-I-030 |
| I-26-012 | Continuous integration | SIT: ephemeral PostgreSQL/Valkey, migrations, synthetic fixtures, API contracts, workflow/browser integration, stub providers | **Partially covered** | PL-06/07/15 (named CI/test) | SIT stage mapping added | §4.4.5.2 table; CONFLICT-471 |
| I-26-014 | Continuous delivery and rollback | Pre-deploy: capacity, compatibility, backup point, migration plan, flags, on-call, approval; freeze conflicting changes; signed go/no-go | **Partially covered** | PL-17 (no freeze, no on-call check) | Pre-deploy checklist added | DPL-PRE-01…10 |
| I-26-015 | Continuous delivery and rollback | Deploy order: expand schema, validate, API, workers/scheduler, Admin and website separately, smoke before automation | **Partially covered** | PL-18 (order not stated) | Ordered deployment runbook | DPL-SEQ-01…09 |
| I-26-016 | Continuous delivery and rollback | Canary: limited internal/approved cohort; compare error, latency, queue lag, invariants; operator approves widening | **Partially covered** | ADR-053 blue/green at scale only | Cohort canary for activation | RECOMMENDATION-461; DPL-CAN |
| I-26-018 | Continuous delivery and rollback | Post-deploy: role-based smoke, publication check, queue drain, reconciliation, budget verification, observation window | **Partially covered** | PL-19 (30 min SLO watch) | Smoke catalogue added | SMK-01…14 |
| I-26-021 | Infrastructure controls | Capacity: requests/limits; autoscale on latency and queue age; protect priority queues; per-tenant caps | **Partially covered** | Part 4.2 §4.27 (manual triggers) | Queue-age scaling rule added | FR-ENH-I-031 |
| I-26-024 | Pipeline outline and delivery table | Activation stage: explicit owner/CTO approval; enable gradually within approved budgets; stop on gate failure | **Partially covered** | Part 8.2 GL-B04 (charter) | Activation stage added | DPL-ACT-01…06 |
| I-26-032 | Implementation acceptance procedures (7) | Load test reproducibility (pin dataset, commit, mix, ramp, warmup, error budget) | **Partially covered** | Part 4.2 §4.26 | Load-test record template | LTR-01…14 |
| I-26-037 | Implementation acceptance procedures (7) | Fail-closed evidence inventory (required-ID list, reject missing/extra/duplicate, mandatory N/A) | **Not covered** | A090 evidence assembly (no validator rules) | Release gate validator specified | RGV-01…14; GAP-463 |
| I-26-038 | Implementation acceptance procedures (7) | Resource and deployment approval: incremental effort estimate per change; approval before cost/SLA promise | **Partially covered** | Part 8.2 §8.2.2.4 change control | Rule restated | DPL-PRE-10 |

Covered and not-applicable aspects (grouped by section):

| Section | Aspect IDs | Status | Blueprint location (representative) |
|---|---|---|---|
| Purpose and operating boundary | 001 | Not applicable | Part 0 §0.1; Part 1; DEC-009 |
| Current design scope | 002 | Not applicable | Part 2.5; Part 3.2; Part 3.3 |
| Product-specific application / Business controls | 003 | Not applicable | Part 2.2 WF-08…WF-10; Part 2.3 BRL |
| Completion and approval / Acceptance and evidence record | 004 | Covered | Part 8.2 §8.2.4.2; Part 6.1 §6.1.5.4 EVR |
| Implementation, verification and delivery controls (preamble) | 005 | Not applicable | BRD §13.2, §16; BLK-11 |
| Deployment topology | 006, 007, 009 | Covered | NFR-001; ADR-006; Part 3.1 §3.1.6; Part 4.3 §4.34; ADR-012/051 |
| Continuous integration | 010, 011, 013 | Covered | PL-02…PL-09; PL-10/11; Part 3.1 §3.1.14; PL-14 |
| Continuous delivery and rollback | 017 | Covered | Part 4.3 §4.38; RB-012 |
| Infrastructure controls | 019, 020, 022 | Covered | Part 4.1 §4.9; GL-S07; ADR-026/050; PL-17; Part 4.3 §4.47 |
| Pipeline outline and delivery table | 023 | Covered | Part 4.3 §4.33.3 |
| Pipeline outline and delivery table | 025, 026 | Not applicable | Pack reference asset only; Pack assets |
| Reproducible CI and isolated rehearsal (table) | 027 | Not applicable | Part 4.3 §4.33–4.38 |
| Reproducible CI and isolated rehearsal (table) | 028, 029, 030, 031 | Covered | Part 4.3 §4.33–4.38 |
| Implementation acceptance procedures (7) | 033, 034, 035, 036, 039 | Covered | DEC-040; Part 3.1 §3.1.12; Part 4.3 §4.37.2; PL-07; PL-10/11/14; Part 4.3 §4.34; PL-15; Part 8.2 |

#### 4.4.3.4 Document 27

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| I-27-007 | Environment matrix | Shared development: integration branch, separate identities, limited quotas | **Conflict** | Not provided (trunk-based) | Environment mapping added | CONFLICT-471; ENV matrix |
| I-27-008 | Environment matrix | SIT: pinned artifact, isolated DB, fake/sandbox callbacks, repeatable reset | **Partially covered** | test/CI env | Environment mapping added | CONFLICT-471; ENV matrix |
| I-27-009 | Environment matrix | UAT: business users, sandbox channels, approved test identities | **Partially covered** | staging | Environment mapping added | CONFLICT-471; ENV matrix |
| I-27-012 | Environment matrix | Recovery: isolated recovery environment; no dispatch until reconciliation and restart | **Partially covered** | Part 4.3 backup restore sandbox | Environment mapping added | CONFLICT-471; ENV matrix |
| I-27-013 | Configuration contract | Identity config: PRODUCT_ID, APP_ENV, WEBSITE_ORIGIN, ADMIN_ORIGIN, OAUTH_ISSUER, WEBSITE_AUDIENCE, ADMIN_AUDIENCE; fail closed | **Not covered** | Parameter Store paths only | Config contract catalogue | ENV-01…07; GAP-461 |
| I-27-014 | Configuration contract | Persistence refs: DATABASE_URL, BROKER_URL, OBJECT_BUCKET, VECTOR_NAMESPACE as secret refs/scoped IDs, never frontend | **Partially covered** | Part 4.1 §4.6.1 | Catalogue | ENV-08…11 |
| I-27-015 | Configuration contract | Execution: AUTOMATION_ENABLED false in nonprod; PAID_FALLBACK_ENABLED false; timeout, retry, budget ceilings | **Partially covered** | Flags (Part 4.3 §4.36) OFF by default | Catalogue | ENV-12…16 |
| I-27-017 | Configuration contract | Observability config: LOG_LEVEL, OTEL endpoint, redaction rules, alert destination | **Partially covered** | Part 4.3 §4.39 | Catalogue | ENV-17…20 |
| I-27-020 | Secrets and dependencies | Developer access: temporary env-specific with MFA; no shared credentials; revoke on departure; monthly review | **Partially covered** | SC-48 (no standing DB access) | Access review procedure | GAP-469; ACC-01…07 |
| I-27-021 | Secrets and dependencies | Dependency locking incl. container digest, migration compatibility, model/prompt revision; licence and vuln at change | **Partially covered** | uv/pnpm lockfiles; PL-09 | Model/prompt revision pinned in release manifest | CS-DEP-01…08 |
| I-27-022 | Secrets and dependencies | Config drift: schema validation at startup; deployed non-secret config hash vs approved manifest | **Partially covered** | IaC drift only (AL-47) | Config-hash drift check | FR-ENH-I-040; AL-55; RECOMMENDATION-468 |
| I-27-023 | Secrets and dependencies | Recovery: restore secret references and config from protected inventory; no secrets in backup notes | **Partially covered** | Part 3.1 §3.1.13.2 secrets row | Recovery step added | ENV recovery rule |
| I-27-024 | Configuration table (15 variables) | APP_PRODUCT=commercial immutable | **Not covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-025 | Configuration table (15 variables) | APP_ENV local/dev/SIT/UAT/staging/prod | **Not covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-026 | Configuration table (15 variables) | DATABASE_URL secret reference | **Partially covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-027 | Configuration table (15 variables) | SECRET_MANAGER_REF | **Not covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-028 | Configuration table (15 variables) | ADMIN_AUDIENCE rejects external identity | **Partially covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-029 | Configuration table (15 variables) | PORTAL_AUDIENCE rejects staff privileges | **Partially covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-030 | Configuration table (15 variables) | ALLOWED_HOSTS verified, no wildcard | **Partially covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-031 | Configuration table (15 variables) | EXTERNAL_DISPATCH_ENABLED false | **Partially covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-032 | Configuration table (15 variables) | PAID_FALLBACK_ENABLED false | **Partially covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-033 | Configuration table (15 variables) | WORKER_QUEUE_PREFIX per product/env | **Not covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-034 | Configuration table (15 variables) | OBJECT_STORE_REF / VECTOR_STORE_REF | **Partially covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-035 | Configuration table (15 variables) | PROVIDER_SECRET_REF | **Partially covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-036 | Configuration table (15 variables) | MAX_REQUEST_BYTES / RATE_LIMIT | **Partially covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-037 | Configuration table (15 variables) | LOG_REDACTION_POLICY | **Not covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-038 | Configuration table (15 variables) | RECOVERY_TARGETS | **Not covered** | Part 4.1 §4.6; Part 3.1 §3.1.14 | Catalogue row | ENV-01…24 |
| I-27-039 | Configuration table (15 variables) | Rotation procedure (inventory → issue → stage/test → atomic switch → revoke → verify; compromise → disable dispatch) | **Partially covered** | Part 4.1 §4.6.2 (cadence only) | Step procedure | SEC-ROT-01…08 |
| I-27-040 | Environment manifest and rotation (table) | Required config incl. automation_enabled=false | **Partially covered** | ABAC-12; Part 4.1 §4.6 | Covered by ENV/SEC-ROT | ENV, SEC-ROT |
| I-27-042 | Environment manifest and rotation (table) | Dependency control incl. model artefacts | **Partially covered** | ABAC-12; Part 4.1 §4.6 | Covered by ENV/SEC-ROT | ENV, SEC-ROT |
| I-27-043 | Environment manifest and rotation (table) | Rotation create/validate/deploy/verify/revoke/audit | **Partially covered** | ABAC-12; Part 4.1 §4.6 | Covered by ENV/SEC-ROT | ENV, SEC-ROT |
| I-27-045 | Implementation acceptance procedures (5) | Dependency and technical debt inventory (owner, remediation date) | **Not covered** | No tech-debt register | Tech-debt register | CS-DOC-05; TDR fields; RECOMMENDATION-472 |

Covered and not-applicable aspects (grouped by section):

| Section | Aspect IDs | Status | Blueprint location (representative) |
|---|---|---|---|
| Purpose and operating boundary | 001 | Not applicable | Part 0 §0.1; Part 1; DEC-009 |
| Current design scope | 002 | Not applicable | Part 2.5; Part 3.2; Part 3.3 |
| Product-specific application / Business controls | 003 | Not applicable | Part 2.2 WF-08…WF-10; Part 2.3 BRL |
| Completion and approval / Acceptance and evidence record | 004 | Covered | Part 8.2 §8.2.4.2; Part 6.1 §6.1.5.4 EVR |
| Implementation, verification and delivery controls (preamble) | 005 | Not applicable | BRD §13.2, §16; BLK-11 |
| Environment matrix | 006, 010, 011 | Covered | Part 3.1 §3.1.14 local; staging; prod |
| Configuration contract | 016, 018 | Covered | Part 4.1 §4.6; Part 4.3 §4.36 |
| Secrets and dependencies | 019 | Covered | Part 4.1 §4.6.2 |
| Environment manifest and rotation (table) | 041, 044 | Covered | ABAC-12; Part 4.1 §4.6 |
| Implementation acceptance procedures (5) | 046, 047, 048, 049, 050 | Covered | NFR-050; NFR-021; BLK-9; PL-10; Part 4.1 §4.6.1; A112 |

#### 4.4.3.5 Document 29

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| I-29-006 | Workload and measurement | Initial capacity workload (25+10, 50 staff, 100k opps, 50 jobs, 10k actions/day) | **Conflict** | DEC-031 | Workload profile WP-01 | CONFLICT-461; WP-01 |
| I-29-007 | Workload and measurement | Growth capacity workload (50+/100, 250 staff, 1m opps, 250 jobs, 100k/day) | **Conflict** | DEC-031 | Workload profile WP-02 | CONFLICT-461; WP-02 |
| I-29-008 | Workload and measurement | Measurement conditions: indexed dashboard excludes live research; ACK after durable acceptance; record dataset, hardware, cache, mix, stubs | **Partially covered** | Part 4.2 §4.21 | Load-test record template | LTR-01…14 |
| I-29-009 | Workload and measurement | Traffic mix 60% list/filter, 20% details, 10% safe writes, 10% background status; public separate | **Conflict** | Part 4.2 LT-01 70/15/10/5 | Profile adopted for dashboard test | CONFLICT-466; WP-03 |
| I-29-010 | Test scenarios | Baseline: single user, one worker, cold/warm cache, SQL and trace | **Not covered** | No baseline scenario | Added | LT-ENH-I-03 |
| I-29-011 | Test scenarios | Load: ramp to initial then growth, hold 30 min each | **Partially covered** | LT-01 30 min at Y1 | Added | LT-ENH-I-01, -02 |
| I-29-013 | Test scenarios | Spike: 3× baseline public enquiries and callbacks | **Conflict** | Burst 2× in same doc; LT-05/07 | Conflict raised | CONFLICT-465; LT-ENH-I-04 |
| I-29-014 | Test scenarios | Endurance: 8-hour soak at initial target; memory, connections, bloat, queue age | **Conflict** | LT-02 4 h; GL-T04 24 h/72 h | Conflict raised | CONFLICT-467; LT-ENH-I-05 |
| I-29-017 | Test scenarios | Recovery: restore DB, replay outbox in dispatch-off mode; RPO/RTO and reconciliation | **Partially covered** | CH-03; RB-007 (no dispatch-off replay) | Dispatch-off replay step | LT-ENH-I-06; RB-007 addendum |
| I-29-019 | Optimization and capacity | Database: EXPLAIN ANALYZE, index tenant/startup/stage/time/cursor, N+1, lock waits | **Partially covered** | Part 3.3 indexes; lever 1 | Perf coding rules | CS-PERF-01…08 |
| I-29-020 | Optimization and capacity | Workers: queue age, throughput, retry, latency, per-tenant fairness; tune concurrency/prefetch | **Partially covered** | Part 4.3 metrics | Prefetch rule and queue-age metric | CS-WRK-08; AL-51 |
| I-29-023 | Delivery-control scenario table (7 rows) | Burst: 2× approved short burst; bounded 429/queue; recover to baseline | **Partially covered** | LT-05, LT-07 | Burst acceptance | LT-ENH-I-04 |
| I-29-024 | Delivery-control scenario table (7 rows) | Endurance 8 h; no leak, no backlog; budgets reconcile | **Conflict** | LT-02 4 h | See CONFLICT-467 | LT-ENH-I-05 |
| I-29-025 | Delivery-control scenario table (7 rows) | Projection: committed event to visible timestamp ≤ 60 s | **Conflict** | NFR-047 | See CONFLICT-463 |  |
| I-29-030 | Workload and performance test execution (table) | k6 staging read-only script with explicit nonprod URL and synthetic token; never production | **Partially covered** | Part 4.2 load tooling | Safety guard rules | LT-SAFE-01…05 |
| I-29-031 | Workload and performance test execution (table) | Evidence: workload, DB row count, latency distribution, errors, resources, config digest | **Partially covered** | Release record | Load-test record template | LTR-01…14 |
| I-29-032 | Mandatory measurable gates (25 rows) | Gate table of 25 metrics with target and verification context | **Partially covered** | Spread across NFR/KPI/SLO; no single OKPI register | OKPI register mapped | §4.4.4.2; RECOMMENDATION-470 |
| I-29-033 | Implementation acceptance procedures (11) | Dashboard latency at 50/250 staff, 100k/1m opportunities | **Conflict** | C10 | Added | LT-ENH-I-01/02 |
| I-29-036 | Implementation acceptance procedures (11) | Query and rendering efficiency | **Partially covered** | — | Added | CS-PERF |
| I-29-037 | Implementation acceptance procedures (11) | Load test reproducibility | **Partially covered** | §4.26 | Added | LTR |
| I-29-038 | Implementation acceptance procedures (11) | Availability and error budget: eligible minutes, exclusions, zero denominator unassessed | **Partially covered** | Part 4.2 §4.21 | Added | FR-ENH-I-050 |
| I-29-039 | Implementation acceptance procedures (11) | Numeric guardrail validation (NaN, infinity, negatives) | **Not covered** | — | Added | FR-ENH-I-011; TC-ENH-I-020 |
| I-29-040 | Implementation acceptance procedures (11) | Growth workload matrix | **Conflict** | DEC-031 | Added | WP-02 |

Covered and not-applicable aspects (grouped by section):

| Section | Aspect IDs | Status | Blueprint location (representative) |
|---|---|---|---|
| Purpose and operating boundary | 001 | Not applicable | Part 0 §0.1; Part 1; DEC-009 |
| Current design scope | 002 | Not applicable | Part 2.5; Part 3.2; Part 3.3 |
| Product-specific application / Business controls | 003 | Not applicable | Part 2.2 WF-08…WF-10; Part 2.3 BRL |
| Completion and approval / Acceptance and evidence record | 004 | Covered | Part 8.2 §8.2.4.2; Part 6.1 §6.1.5.4 EVR |
| Implementation, verification and delivery controls (preamble) | 005 | Not applicable | BRD §13.2, §16; BLK-11 |
| Test scenarios | 012, 015, 016 | Covered | Part 6.1 LT-08; LT-11; NFR-062; CH-01; RB-001 |
| Optimization and capacity | 018, 021, 022 | Covered | NFR-042/043; Part 7.3; NFR-030; Part 4.3 §4.46.6; Part 4.2 §4.27 |
| Delivery-control scenario table (7 rows) | 026, 027, 028 | Covered | CH-02; NFR-007; Part 4.3 §4.39.2; PL-16; Part 6.1 |
| Workload and performance test execution (table) | 029 | Covered | LT-01 < 0.5% (stricter) |
| Implementation acceptance procedures (11) | 034, 035, 041, 042, 043, 044, 045 | Covered | NFR-042; C6; NFR-051; LT-11; NFR-089; Part 4.3 §4.41; NFR-078; Part 8.2 §8.2.2.4; RECOMMENDATION-017 seeds; NFR-015 |

#### 4.4.3.6 Document 30

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| I-30-006 | Authorization and test rules | Written authorization: hosts, environments, identities, techniques, time window; staging/synthetic only | **Not covered** | Part 4.1 §4.16.2 scope only | Rules of engagement | PT-ROE-01…12; GAP-466 |
| I-30-008 | Authorization and test rules | Severity: Critical = confidential disclosure, financial integrity, production credential, uncontrolled dispatch | **Conflict** | Part 4.1 §4.16.3 CVSS-based | Business-impact overlay | CONFLICT-472 |
| I-30-009 | Authorization and test rules | Evidence: minimal redacted request/response, build, env, role, expected/observed; no secrets | **Partially covered** | EVR (Part 6.1) | Finding record template | PT-FND-01…14 |
| I-30-022 | Assessment and remediation | Tooling: ZAP in staging, dependency scanners, secret scan, SAST, manual role/object tests; record tool version, scope, false positives | **Partially covered** | Part 4.1 §4.16.1 (no false-positive review record) | Finding record fields | PT-FND |
| I-30-033 | Threat/asset verification table (8 rows) | Testing only in nonproduction or scoped pen-test; never attack third parties or use real records | **Partially covered** | Part 4.1 §4.16.2 out-of-scope list | RoE rules | PT-ROE |
| I-30-034 | Authorized security test evidence matrix (5 rows) | Scope documented (date, tester, exclusions) | **Not covered** | Part 4.1 §4.8.2 | RoE / SVM | PT-ROE; SVM |
| I-30-044 | Implementation acceptance procedures (6) | Evidence integrity: reject missing controls, duplicates, mandatory N/A, blank evidence, executor = reviewer; verify hashes | **Not covered** | EVR independence rule only | Validator rules | RGV-01…14 |
| I-30-045 | Current scope: cybersecurity scenario table (UX-QC-01…10 duplicate) | Ten scenario rows (scope onboarding … accessibility navigation) | **Partially covered** | Part 6 TCs (partial) | See doc 32 UX-QC mapping | §4.4.4.5 |

Covered and not-applicable aspects (grouped by section):

| Section | Aspect IDs | Status | Blueprint location (representative) |
|---|---|---|---|
| Purpose and operating boundary | 001 | Not applicable | Part 0 §0.1; Part 1; DEC-009 |
| Current design scope | 002 | Not applicable | Part 2.5; Part 3.2; Part 3.3 |
| Product-specific application / Business controls | 003 | Not applicable | Part 2.2 WF-08…WF-10; Part 2.3 BRL |
| Completion and approval / Acceptance and evidence record | 004 | Covered | Part 8.2 §8.2.4.2; Part 6.1 §6.1.5.4 EVR |
| Implementation, verification and delivery controls (preamble) | 005 | Not applicable | BRD §13.2, §16; BLK-11 |
| Authorization and test rules | 007 | Covered | Part 4.1 §4.2 |
| Security verification matrix (12 rows) | 010, 011, 012, 013, 014, 015, 016, 017, 018, 019, 020, 021 | Covered | Part 4.1 §4.8, §4.16; Part 6 TCs |
| Assessment and remediation | 023, 024 | Covered | BLK-1/4; Part 6.1; BLK rows; GL-S03 |
| Threat/asset verification table (8 rows) | 025, 026, 027, 028, 029, 030, 031, 032 | Covered | Part 4.1; BLK-1…5; Part 4.3 §4.47 tabletop; RB-004/008/013 |
| Authorized security test evidence matrix (5 rows) | 035, 036, 037, 038 | Covered | Part 4.1 §4.8.2; NFR-072; GL-S03 |
| Implementation acceptance procedures (6) | 039, 040, 041, 042, 043 | Covered | Part 6.4; NFR-003/032/050 |

#### 4.4.3.7 Document 31

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| I-31-007 | Observability design | Business signals: eligible opportunities, dispatch outcome, follow-up due, objection escalation, approvals, verified closure | **Partially covered** | RP-xx reports; metrics catalogue | Business signal metrics | MET-07…12 |
| I-31-014 | Alerts and triage | Thresholds: p95 over target 10 min; 5xx > 2% 5 min; projection lag > 60 s; integrity event immediate | **Partially covered** | AL-04/05 (15 min), AL-06 | Projection-lag alert added | AL-52 |
| I-31-019 | Incident runbooks | Financial exception runbook (quarantine, stop closure, finance verifies, append correction) | **Not covered** | No RB for financial mismatch | RB-016 added | RB-016; GAP-465 |
| I-31-020 | Incident runbooks | Public content incident runbook (unpublish, purge, retain audit, approve replacement) | **Not covered** | No RB | RB-017 added | RB-017; GAP-465 |
| I-31-022 | Support operations | Intake: ticket with product, tenant, role, issue, severity, redacted evidence; verify caller authority | **Partially covered** | §4.45 (caller authority not stated) | Caller verification step | SUP-01…05 |
| I-31-025 | Support operations | Review cadence: daily critical queue, weekly incident trends, monthly SLA/cost/quality | **Partially covered** | Monthly ops review; FinOps cadence | Cadence table | SUP-06…08 |
| I-31-027 | Metric/alert table (8 rows) | Error ratio 5xx > 1% for 10 min | **Conflict** | AL-06 > 2% for 5 min | Two-tier alert | CONFLICT-464; AL-50 |
| I-31-028 | Metric/alert table (8 rows) | Queue age: oldest eligible ready job > 5 min for 5 min | **Partially covered** | AL-07 outbox oldest > 5 min; AL-27 | Per-queue age alert | AL-51 |
| I-31-029 | Metric/alert table (8 rows) | Budget hard limit breached or negative remaining → immediate dispatch stop | **Partially covered** | AL-14 (no negative-remaining check) | Negative remaining alert | AL-53 |
| I-31-031 | Metric/alert table (8 rows) | Financial mismatch: duplicate/unmatched/wrong issuer/currency/unreconciled callback → freeze | **Not covered** | No alert rule | AL-56 + RB-016 | AL-56 |
| I-31-036 | Operating signals table (5 rows) | Queue/outbox: oldest age, repeated failure, uncertain, duplicate event, exhausted budget | **Partially covered** | Part 4.3 §4.41, §4.43 | Added | AL-57 |
| I-31-037 | Operating signals table (5 rows) | Confidentiality: foreign access or secret/PII in logs → stop feature | **Partially covered** | Part 4.3 §4.41, §4.43 | Added | AL-58 |
| I-31-038 | Operating signals table (5 rows) | Financial mismatch hold closing | **Not covered** | Part 4.3 §4.41, §4.43 | Added | AL-56; RB-016 |
| I-31-039 | Operating signals table (5 rows) | Operational record: detected/contained/restored times, correlation IDs, root cause, retest; no unsupported SLA claim | **Partially covered** | Part 4.3 §4.41, §4.43 | Added | INC-REC |
| I-31-040 | Optimization intelligence (reuse Admin interfaces) | No public/portal access; scoped filters; show 'unassessed' when no denominator; label stale metrics | **Partially covered** | RPT-R1 numerator/denominator; as-of | Unassessed rule added | FR-ENH-I-050 |
| I-31-041 | Optimization intelligence (reuse Admin interfaces) | Seven dashboards: command centre, audit/jobs, cost/budget, health/incidents, AI quality, growth, revenue (19 API ops, 25 persistence sources) | **Partially covered** | Part 3.2 (14 of 19 ops); Part 3.3 equivalents | Catalogue reconciled | §4.4.4.3; CONFLICT-469; GAP-467 |
| I-31-044 | Implementation acceptance procedures (6) | Availability and error budget (zero denominator unassessed) | **Partially covered** | §4.40 | FR-ENH-I-050 |  |
| I-31-045 | Implementation acceptance procedures (6) | Numeric guardrail validation | **Not covered** | — | FR-ENH-I-011 |  |
| I-31-048 | Implementation acceptance procedures (6) | Current scope: trace trigger/event/run/action IDs; step latency, cost, conflict, suppression; alert stale runs, unknown outcome, budget anomaly | **Partially covered** | run_id in logs; AL-10/14/15 | Stale-run alert | AL-57 |

Covered and not-applicable aspects (grouped by section):

| Section | Aspect IDs | Status | Blueprint location (representative) |
|---|---|---|---|
| Purpose and operating boundary | 001 | Not applicable | Part 0 §0.1; Part 1; DEC-009 |
| Current design scope | 002 | Not applicable | Part 2.5; Part 3.2; Part 3.3 |
| Product-specific application / Business controls | 003 | Not applicable | Part 2.2 WF-08…WF-10; Part 2.3 BRL |
| Completion and approval / Acceptance and evidence record | 004 | Covered | Part 8.2 §8.2.4.2; Part 6.1 §6.1.5.4 EVR |
| Implementation, verification and delivery controls (preamble) | 005 | Not applicable | BRD §13.2, §16; BLK-11 |
| Observability design | 006, 008, 009, 010 | Covered | Part 4.3 §4.39.2; §4.39.2 ai_* metrics; §4.39.1; NFR-079; ADR-058/025 (CloudWatch; Grafana optional) |
| Alerts and triage | 011, 012, 013, 015 | Covered | §4.43.1 Sev1; Sev2 ack ≤ 30 min (stricter); Sev3; AL-14; BRL-AI-08 |
| Incident runbooks | 016, 017, 018, 021 | Covered | RB-001; RB-008; RB-002; §4.43.5 |
| Support operations | 023, 024 | Covered | DEC-056; §4.43.4 |
| Metric/alert table (8 rows) | 026, 030, 032, 033, 034 | Covered | AL-04/05 (stricter); AL-31/33/41; AL-39/49; RB-015; AL-23, AL-46; PL-17; §4.43.3; Part 4.1 §4.17 |
| Operating signals table (5 rows) | 035 | Covered | Part 4.3 §4.41, §4.43 |
| Implementation acceptance procedures (6) | 042, 043, 046, 047 | Covered | NFR-014, NFR-035; KPI-24; NFR-026/065; RB-003; §4.41; DEC-044; OPT-20-03 |

#### 4.4.3.8 Document 32

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| I-32-015 | Deployment sequence | Prepare: immutable artifact record, window, communication plan, backup point, rollback owner, freeze | **Partially covered** | PL-17 | DPL-PRE | DPL-PRE-01…10 |
| I-32-016 | Deployment sequence | Execute: disable dispatch, migrate compatible schema, deploy API, workers, website/Admin separately, verify health | **Partially covered** | PL-18 | DPL-SEQ | DPL-SEQ-01…09 |
| I-32-017 | Deployment sequence | Smoke: anonymous page, external own record, unauthorized denial, Admin scoped query, synthetic intake, outbox, verified callback | **Partially covered** | PL-19 smoke set | Smoke catalogue | SMK-01…14 |
| I-32-020 | Rollback decision | Triggers: cross-tenant disclosure, invalid funds/receipt, duplicate effect, critical smoke failure, sustained severe error | **Partially covered** | RB-012 (deploy-caused only) | Rollback trigger matrix | RBK-T01…T08 |
| I-32-023 | Rollback decision | Reconcile provider/bank records, outbox, commitments before resume; finance and ops approve | **Partially covered** | RB-003 (no finance/ops dual approval) | Resume approval rule | RBK-R01…R05 |
| I-32-025 | Delivery package | Technical handover: repos, artifacts, API/schema contracts, config refs, SBOM, test evidence, dashboards, recovery | **Not covered** | No delivery package | Handover checklist | HO-T01…T10; GAP-464 |
| I-32-026 | Delivery package | Business handover: training, operating instructions, scope, contacts, exceptions, acceptance | **Partially covered** | Part 8.2 §8.2.2 training; hypercare exit 8 | Handover checklist | HO-B01…B06 |
| I-32-027 | Delivery package | Access handover: transfer account/vault ownership, rotate temporary credentials, remove developer production access | **Not covered** | — | Handover checklist | HO-A01…A06 |
| I-32-029 | Checkpoint table (8 rows) and no-go criteria | Preparation: freeze scope, verify contracts, migration graph, environment, digest, support roles | **Partially covered** | Part 4.3 §4.37–4.38; Part 8.2 §8.2.4 | DPL / HO | DPL, HO |
| I-32-030 | Checkpoint table (8 rows) and no-go criteria | Before deployment: restore rehearsal, deploy identity, config, cost limits, rollback package | **Partially covered** | Part 4.3 §4.37–4.38; Part 8.2 §8.2.4 | DPL / HO | DPL, HO |
| I-32-032 | Checkpoint table (8 rows) and no-go criteria | Deploy application independently; dispatch disabled | **Partially covered** | Part 4.3 §4.37–4.38; Part 8.2 §8.2.4 | DPL / HO | DPL, HO |
| I-32-036 | Checkpoint table (8 rows) and no-go criteria | Handover: access, manuals, support, training, residual risk | **Not covered** | Part 4.3 §4.37–4.38; Part 8.2 §8.2.4 | DPL / HO | DPL, HO |
| I-32-037 | Checkpoint table (8 rows) and no-go criteria | No-go list (authorization leak, financial discrepancy, mandatory test failure, missing backup, unapproved schema/API change, unsupported regulated op, unverified sender or paid fallback, absent monitoring/owner) | **Partially covered** | BLK-1…11 (sender verification and paid fallback not explicit) | No-go rows added | GL-E01…E06 |
| I-32-040 | Go-live execution and hard-blocking gates | Evidence check: release_gate.py against signed QC/acceptance register and manifests; pending returns non-zero | **Not covered** | A090 manual assembly | Release gate validator | RGV-01…14; RECOMMENDATION-462 |
| I-32-044 | Mandatory measurable gates (21 rows) | 21 mandatory OKPI gates (see doc 38 OKPI-01…35) | **Partially covered** | Spread across NFR/KPI/SLO | OKPI register mapping | §4.4.4.2 |
| I-32-045 | Implementation acceptance procedures (7) and approval gates | Evidence gate fail-closed (delete QC row, duplicate ID, mandatory N/A) | **Not covered** | — | RGV + TC | RGV; TC-ENH-I-040…042 |
| I-32-046 | Implementation acceptance procedures (7) and approval gates | Recovery and rollback: RPO 15 min, RTO 4 h / 2 h growth | **Conflict** | DEC-018 | See CONFLICT-462 |  |
| I-32-047 | Implementation acceptance procedures (7) and approval gates | Granular QC and evidence (all QC IDs, owners, evidence; required ID baseline) | **Partially covered** | Part 6.6 RTM; A090 | RGV | RGV |
| I-32-049 | Implementation acceptance procedures (7) and approval gates | Go-live and rollback gate rehearsal with incomplete evidence: no activation | **Partially covered** | BLK-11 | TC added | TC-ENH-I-043 |
| I-32-050 | Implementation acceptance procedures (7) and approval gates | Outstanding approval gates: 38 exact API definitions, 0 partial, 4 DB confirmations, 138 UI semantic mappings | **Not covered** | Pack-baseline counts not reconciled | Gap raised to coordinator | GAP-468 |
| I-32-051 | Implementation acceptance procedures (7) and approval gates | Fail-closed evidence inventory (authoritative required-ID list from immutable baseline) | **Not covered** | — | RGV-01…05 | RGV |
| I-32-052 | Implementation acceptance procedures (7) and approval gates | Evidence integrity and final acceptance (executor ≠ reviewer after normalization; non-blank approval; artifact hashes) | **Partially covered** | EVR independence | RGV-06…14 | RGV |
| I-32-053 | Implementation acceptance procedures (7) and approval gates | Combined preflight: 1,188 records across six groups incl. 21 mandatory KPIs; CTO and PO authenticate and sign | **Not covered** | No combined preflight | Blueprint-equivalent preflight defined | RGV-15; GAP-468 |
| I-32-054 | Current scope: release gates and UX-QC | Original evidence preflight plus expansion gate; field mapping, contract/DB decisions, new tests, independent review | **Partially covered** | BLK-10/11 | RGV | RGV |
| I-32-055 | Current scope: release gates and UX-QC | UX-QC-01 Scope and onboarding (26 owned startups, ten client tenants) | **Partially covered** | Part 6 TCs; see §4.4.4.5 | Mapped; gaps get TC-ENH-I | UX-QC-01 |
| I-32-061 | Current scope: release gates and UX-QC | UX-QC-07 Shared closure state (consistent opportunity/quote/order IDs) | **Partially covered** | Part 6 TCs; see §4.4.4.5 | Mapped; gaps get TC-ENH-I | UX-QC-07 |
| I-32-062 | Current scope: release gates and UX-QC | UX-QC-08 Website and Admin handoff (SaaS application import, snapshot) | **Partially covered** | Part 6 TCs; see §4.4.4.5 | Mapped; gaps get TC-ENH-I | UX-QC-08 |
| I-32-064 | Current scope: release gates and UX-QC | UX-QC-10 Accessibility and navigation (every route, keyboard, widths) | **Partially covered** | Part 6 TCs; see §4.4.4.5 | Mapped; gaps get TC-ENH-I | UX-QC-10 |

Covered and not-applicable aspects (grouped by section):

| Section | Aspect IDs | Status | Blueprint location (representative) |
|---|---|---|---|
| Purpose and operating boundary | 001 | Not applicable | Part 0 §0.1; Part 1; DEC-009 |
| Current design scope | 002 | Not applicable | Part 2.5; Part 3.2; Part 3.3 |
| Product-specific application / Business controls | 003 | Not applicable | Part 2.2 WF-08…WF-10; Part 2.3 BRL |
| Completion and approval / Acceptance and evidence record | 004 | Covered | Part 8.2 §8.2.4.2; Part 6.1 §6.1.5.4 EVR |
| Implementation, verification and delivery controls (preamble) | 005 | Not applicable | BRD §13.2, §16; BLK-11 |
| Pre-go-live gates (9) | 006, 007, 008, 009, 010, 011, 012, 013, 014 | Covered | Part 8.2 §8.2.4.3 GL-B01; Part 8.2 §8.2.4.3 GL-T02; BLK-10; Part 8.2 §8.2.4.3 GL-D04, GL-T05; Part 8.2 §8.2.4.3 GL-A01…A04; Part 8.2 §8.2.4.3 GL-S01…S04; Par… |
| Deployment sequence | 018, 019 | Covered | GL-B04 activation charter; Part 8.2 §8.2.5 hypercare |
| Rollback decision | 021, 022, 024 | Covered | RB-004; RB-012; §4.38; RB-004 resume |
| Delivery package | 028 | Covered | BRD §12.2 EVR; BLK-11 |
| Checkpoint table (8 rows) and no-go criteria | 031, 033, 034, 035, 038 | Covered | Part 4.3 §4.37–4.38; Part 8.2 §8.2.4; DEC-050; §4.38 |
| Go-live execution and hard-blocking gates | 039, 041, 042, 043 | Covered | GL-T05; BLK-8; NFR-001; SMK; §8.2.5.3; RB-012; BLK |
| Implementation acceptance procedures (7) and approval gates | 048 | Covered | §4.47 |
| Current scope: release gates and UX-QC | 056, 057, 058, 059, 060, 063 | Covered | Part 6 TCs; see §4.4.4.5 |

#### 4.4.3.9 Optimization controls OPT-xx-yy (inventoried once across the eight documents)

| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |
|---|---|---|---|---|---|---|
| I-OPT-010 | Optimization engineering (OPT-02-02) | OPT-02-02 React rendering and filters (debounce, cancel, virtualize, scope cache) | **Partially covered** | NFR-027, NFR-044 | Mapped in §4.4.4.1; enhancement added | OPT-02-02 |
| I-OPT-012 | Optimization engineering (OPT-02-04) | OPT-02-04 Read projections cached by permission revision | **Partially covered** | Part 3.1 §3.1.11 | Mapped in §4.4.4.1; enhancement added | OPT-02-04 |
| I-OPT-014 | Optimization engineering (OPT-02-06) | OPT-02-06 Database and network: plans, N+1, pooling, streaming | **Partially covered** | Part 3.1 lever 1 | Mapped in §4.4.4.1; enhancement added | OPT-02-06 |
| I-OPT-015 | Optimization engineering (OPT-02-07) | OPT-02-07 Parallel and batch operations bounded by tenant/provider | **Partially covered** | ADR-021 | Mapped in §4.4.4.1; enhancement added | OPT-02-07 |
| I-OPT-022 | Optimization engineering (OPT-05-05) | OPT-05-05 Backpressure and fair scheduling; reserve urgent capacity | **Partially covered** | ADR-021 (no reserved control capacity) | Mapped in §4.4.4.1; enhancement added | OPT-05-05 |
| I-OPT-023 | Optimization engineering (OPT-05-06) | OPT-05-06 Config and AI failures: fail startup on missing config | **Not covered** | No config validation at startup | Mapped in §4.4.4.1; enhancement added | OPT-05-06 |
| I-OPT-024 | Optimization engineering (OPT-05-07) | OPT-05-07 Availability 99.9% and reconciliation | **Conflict** | DEC-018 99.5% | Mapped in §4.4.4.1; enhancement added | OPT-05-07 |
| I-OPT-025 | Optimization engineering (OPT-06-01) | OPT-06-01 Startup templates and tenants 25+10 / 50+ +100 | **Conflict** | DEC-031 | Mapped in §4.4.4.1; enhancement added | OPT-06-01 |
| I-OPT-026 | Optimization engineering (OPT-06-02) | OPT-06-02 Concurrent users and jobs 50/250 | **Conflict** | DEC-031 | Mapped in §4.4.4.1; enhancement added | OPT-06-02 |
| I-OPT-027 | Optimization engineering (OPT-06-03) | OPT-06-03 Data and scheduling volume 100k/1m; 10k/100k | **Conflict** | DEC-031 | Mapped in §4.4.4.1; enhancement added | OPT-06-03 |
| I-OPT-034 | Optimization engineering (OPT-07-05) | OPT-07-05 Complexity and reuse review | **Partially covered** | No reuse review procedure | Mapped in §4.4.4.1; enhancement added | OPT-07-05 |
| I-OPT-039 | Optimization engineering (OPT-13-01) | OPT-13-01 Code health | **Partially covered** | PL gates; no coding standard | Mapped in §4.4.4.1; enhancement added | OPT-13-01 |
| I-OPT-040 | Optimization engineering (OPT-13-02) | OPT-13-02 Technical debt register, monthly review | **Not covered** | None | Mapped in §4.4.4.1; enhancement added | OPT-13-02 |
| I-OPT-041 | Optimization engineering (OPT-13-03) | OPT-13-03 Documentation and debugging runbooks synchronized | **Partially covered** | Runbooks RB-### | Mapped in §4.4.4.1; enhancement added | OPT-13-03 |
| I-OPT-046 | Optimization engineering (OPT-16-01) | OPT-16-01 Standard setup: reproducible local env | **Partially covered** | Part 3.1 local env; no onboarding procedure | Mapped in §4.4.4.1; enhancement added | OPT-16-01 |
| I-OPT-048 | Optimization engineering (OPT-16-03) | OPT-16-03 AI-assisted development review | **Not covered** | None | Mapped in §4.4.4.1; enhancement added | OPT-16-03 |
| I-OPT-052 | Optimization engineering (OPT-18-03) | OPT-18-03 Backup and DR RPO/RTO incl. growth 2 h and regenerable 24 h/8 h | **Conflict** | DEC-018 | Mapped in §4.4.4.1; enhancement added | OPT-18-03 |
| I-OPT-053 | Optimization engineering (OPT-18-04) | OPT-18-04 Observability and incident drills (scope denials, stale projections) | **Partially covered** | §4.41 (no stale-projection alert) | Mapped in §4.4.4.1; enhancement added | OPT-18-04 |

Covered and not-applicable aspects (grouped by section):

| Section | Aspect IDs | Status | Blueprint location (representative) |
|---|---|---|---|
| Optimization engineering (OPT-01-01) | 001 | Covered | NFR-003; NFR-050 |
| Optimization engineering (OPT-01-02) | 002 | Covered | NFR-002; NFR-031 |
| Optimization engineering (OPT-01-03) | 003 | Covered | NFR-032 |
| Optimization engineering (OPT-01-04) | 004 | Covered | NFR-001 |
| Optimization engineering (OPT-01-05) | 005 | Covered | Part 4.1 §4.9; NFR-022 |
| Optimization engineering (OPT-01-06) | 006 | Covered | Part 4.1 §4.6; NFR-068 |
| Optimization engineering (OPT-01-07) | 007 | Covered | NFR-021; Part 4.1 §4.15 |
| Optimization engineering (OPT-01-08) | 008 | Covered | NFR-018; DEC-038 |
| Optimization engineering (OPT-02-01) | 009 | Covered | NFR-042/043 |
| Optimization engineering (OPT-02-03) | 011 | Covered | NFR-015; C3 |
| Optimization engineering (OPT-02-05) | 013 | Covered | ARP-09; C6 |
| Optimization engineering (OPT-03-01) | 016 | Covered | NFR-037 |
| Optimization engineering (OPT-04-01) | 017 | Covered | FR register (BRD OPT-04-01) |
| Optimization engineering (OPT-05-01) | 018 | Covered | NFR-006, NFR-063 |
| Optimization engineering (OPT-05-02) | 019 | Covered | NFR-005, NFR-066 |
| Optimization engineering (OPT-05-03) | 020 | Covered | NFR-016, NFR-064 |
| Optimization engineering (OPT-05-04) | 021 | Covered | ADR-027 |
| Optimization engineering (OPT-06-04) | 028 | Covered | DEC-026; NFR-096/097 |
| Optimization engineering (OPT-06-05) | 029 | Covered | NFR-062 |
| Optimization engineering (OPT-07-01) | 030 | Covered | ADR-001; NFR-029 |
| Optimization engineering (OPT-07-02) | 031 | Not applicable | Investor product out of scope (DEC-009); isolation via NFR-031 |
| Optimization engineering (OPT-07-03) | 032 | Covered | ARP-06; ADR-009 |
| Optimization engineering (OPT-07-04) | 033 | Covered | Part 2.4 CFG |
| Optimization engineering (OPT-08-01) | 035 | Covered | Part 3.3 |
| Optimization engineering (OPT-09-01) | 036 | Covered | NFR-015; BLK-10 |
| Optimization engineering (OPT-10-01) | 037 | Covered | DEC-007; NFR-030 |
| Optimization engineering (OPT-12-01) | 038 | Covered | KPI register (BRD OPT-12-01) |
| Optimization engineering (OPT-13-04) | 042 | Covered | NFR-084 |
| Optimization engineering (OPT-14-01) | 043 | Covered | ADR-006/060 |
| Optimization engineering (OPT-14-02) | 044 | Covered | Part 2.4 CFG; DEC |
| Optimization engineering (OPT-14-03) | 045 | Covered | Part 2.5 §2.45 |
| Optimization engineering (OPT-16-02) | 047 | Covered | Part 8.1 |
| Optimization engineering (OPT-17-01) | 049 | Covered | Part 6.1 |
| Optimization engineering (OPT-18-01) | 050 | Covered | §4.33 |
| Optimization engineering (OPT-18-02) | 051 | Covered | §4.37.2 |
| Optimization engineering (OPT-19-01) | 054 | Covered | NFR-028; DEC-010/011 |
| Optimization engineering (OPT-19-02) | 055 | Covered | NFR-095 |
| Optimization engineering (OPT-19-03) | 056 | Covered | NFR-075/076 |
| Optimization engineering (OPT-19-04) | 057 | Covered | DEC-010/011 |

