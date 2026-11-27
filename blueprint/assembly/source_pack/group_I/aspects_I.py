"""Group I atomic aspect inventory (docs 18, 25, 26, 27, 29, 30, 31, 32).
Each row: (doc, section, summary, status, blueprint_location, action, new_ids)
status: C Covered, P Partially covered, N Not covered, X Conflict, NA Not applicable.
Aspect IDs are generated as I-<doc>-<nnn>. The OPT optimisation controls and the
mandatory gates (OKPI) are inventoried once in OPT/OKPI rows (doc = all docs that carry them).
"""
CC = "Common core: see document 01/02 coverage"
A = []
def add(doc, sec, summ, st, loc, act, new=""):
    A.append((doc, sec, summ, st, loc, act, new))

# ---------------- common core (once per document) ----------------
for d in ["18", "25", "26", "27", "29", "30", "31", "32"]:
    add(d, "Purpose and operating boundary", "Product purpose, investor exclusion, independent deployment, 25+ startups, tenant vs startup, aggregate read-only", "NA", "Part 0 §0.1; Part 1; DEC-009", CC)
    add(d, "Current design scope", "147 interfaces (34 Website + 113 Admin), 302+19 API operations, 149+6 entities, 624+175 tests", "NA", "Part 2.5; Part 3.2; Part 3.3", CC + " (counts reconciled by groups owning docs 06/07/08/38)")
    add(d, "Product-specific application / Business controls", "AppNAI, MedMaarg, EduVerse, OrganicSpec, campaign business controls (5 rows)", "NA", "Part 2.2 WF-08…WF-10; Part 2.3 BRL", CC)
    add(d, "Completion and approval / Acceptance and evidence record", "Responsible lead, independent reviewer, PO sign-off; five evidence fields (BRD §12.2)", "C", "Part 8.2 §8.2.4.2; Part 6.1 §6.1.5.4 EVR", "None (BRD §12.2 already mapped)")
    add(d, "Implementation, verification and delivery controls (preamble)", "Proposed contracts are not production approval; actions subject to authorization, budget and approval", "NA", "BRD §13.2, §16; BLK-11", CC)

# ---------------- document 18 ----------------
s = "Initial startup configurations / technology principles"
add("18", s, "Four seed startup profiles and open-source-first technology principles", "NA", "Part 1 §1.2; Part 3.1 §3.1.8", CC)
s = "Authority and data protection"
add("18", s, "Owner/founder: portfolio view, selected-startup mutation, no other tenant by default", "C", "Part 2.3 R01, ABAC-01; DEC-065", "None")
add("18", s, "Employee/growth manager: assigned scope, no investor records", "C", "Part 2.3 R02–R07; BRL-TEN-12", "None")
add("18", s, "Finance/legal maker-checker; no autonomous financial transfer", "C", "DEC-038; BRL-APR; DEC-064", "None")
add("18", s, "Tenant administrator not automatically a business approver", "C", "Part 2.3 R12; SoD rules", "None")
add("18", s, "Platform support/billing: metadata only, bounded client-approved grant", "C", "DEC-056 SupportAccessGrant; BRL-TEN-09", "None")
add("18", s, "External prospect/customer: own invite/portal records only", "C", "Part 2.3 R16; portal grants", "None")
add("18", s, "Other application user denied by audience even with same SSO identity", "C", "DEC-019; NFR-003; ADR-033", "None")
add("18", s, "Server-side permission on every object, nested FK, search, vector, export, notification, worker, webhook", "C", "NFR-002; Part 4.1 §4.4", "None")
s = "Threat model and governance controls"
for t, loc in [("Cross-product / cross-tenant leak", "Part 4.1 TB-09, NFR-031/032"), ("Privilege escalation / confused deputy", "Part 4.1 TB-04"),
               ("Prompt injection / hallucination", "Part 4.1 §4.15"), ("Duplicate message / transaction", "NFR-005, ADR-023"),
               ("Secret or webhook compromise", "Part 4.1 §4.6, RB-009, RB-013"), ("Unexpected cost / abusive execution", "BRL-AI-08, NFR-022, RB-005"),
               ("Privacy / communications", "Part 4.1 §4.11–4.12"), ("Financial corruption", "DEC-038, NFR-018")]:
    add("18", s, t, "C", loc, "None")
add("18", s, "Unauthorized extraction: scope export, approve manifest hash, short-lived link, revoke", "P", "Part 2.4 exports; AL-35", "Export manifest hash approval added as rule", "FR-ENH-I-012")
add("18", s, "Regulatory controls are operational requirements, not legal advice; investor route text", "NA", "Investor product out of scope (DEC-009)", "None")
add("18", s, "Health and school data excluded from acquisition profiling; minors protected", "C", "DEC-010/011 (MedMaarg, EduVerse); BRL-ELG", "None")
add("18", s, "Incident: stop scope, revoke, preserve, notify, verify restore, reconcile, restart approval", "C", "Part 4.1 §4.17; RB-004 resume", "None")
add("18", s, "Independent backup and restore drills per product", "C", "Part 4.3 §4.47; NFR-031", "None")
s = "Capacity, reliability and recovery acceptance"
add("18", s, "Owned startups / external tenants 25/10 initial, 50+/100 growth", "X", "DEC-031 (40/10 Y1; 100/30 Y2)", "Test workload profiles added; conflict raised", "CONFLICT-461; WP-01, WP-02")
add("18", s, "Concurrent staff sessions 50 / 250", "X", "DEC-031 internal users 60/200; Part 4.2 §4.25.3", "As above", "CONFLICT-461; WP-01, WP-02")
add("18", s, "Scoped opportunities 100,000 / 1,000,000", "N", "No opportunity-volume design point", "Seeded volume added to workload profiles", "WP-01, WP-02; LT-ENH-I-01")
add("18", s, "Concurrent jobs 50/250; scheduled actions 10,000/100,000 per day", "X", "Part 4.2 §4.25.3 (≈1,154 msgs/day Y1)", "Adopted as stress workload; conflict raised", "CONFLICT-461; LT-ENH-I-02")
add("18", s, "Dashboard query p95 ≤ 2 s / ≤ 2.5 s", "C", "Part 4.2 §4.24 C10 (800 ms p95, stricter)", "Mapped to OKPI-05/26", "OKPI map")
add("18", s, "Async/webhook acknowledgement p95 ≤ 2 s", "C", "NFR-051, C6 (stricter)", "Mapped to OKPI-27", "OKPI map")
add("18", s, "Projection refresh ≤ 60 s", "X", "NFR-008 (360 ≤ 60 s) vs NFR-047 (dashboards ≤ 15 min)", "Conflict raised", "CONFLICT-463")
add("18", s, "Critical RPO ≤ 15 min; RTO ≤ 4 h initial, ≤ 2 h growth", "X", "DEC-018; NFR-056/057", "Growth RTO conflict raised", "CONFLICT-462")
add("18", s, "Regenerable research data RPO ≤ 24 h / RTO ≤ 8 h", "N", "No recovery class for regenerable data", "Recovery class RC-2 added", "GAP-462; FR-ENH-I-020")
add("18", s, "Targets are test targets, not SLA; fairness and independent budget/recovery on shared infra", "C", "DEC-044; NFR-062", "None")
s = "Website and confidential Admin operating contract"
add("18", s, "Surface table: Public, Portal, Admin, Internal/callback audiences and controls", "C", "NFR-001; Part 4.1 §4.1.3 trust zones", "None")
add("18", s, "Routing: canonical legacy paths retained; /public /portal /admin namespaces; default deny; CORS not authorization", "C", "Part 3.2 namespaces; Part 4.1 §4.9", "None")
add("18", s, "Verified custom domain → one tenant/startup; unknown host 404; immutable snapshot; preview grants; atomic swap", "C", "NFR-020; ADR-010; BRL-TEN-10", "None")
add("18", s, "Public intake → scoped durable event + outbox; workers recheck before acting", "C", "ARP-03/04; Part 3.1 §3.1.7.1", "None")
add("18", s, "Website/portal threat list (10 threats) and controls", "C", "Part 4.1 TB-01, TB-02", "None")
add("18", s, "Emergency unpublish and revoke access without deleting authoritative evidence", "P", "RB-004; BRL-PUB", "Public-content incident runbook added", "RB-017")
s = "Open-source supply chain and external-service controls"
add("18", s, "SBOM, pinned versions, licence review incl. copyleft, network-use terms, separately licensed model weights", "P", "PL-09/PL-10; Part 4.1 §4.16.1; GL-L06", "Model-weight and network-use licence rule added", "CS-DEP-04")
add("18", s, "Container/dependency scan, secret redaction, least privilege, approved egress", "C", "PL-09/11; Part 4.1 §4.9", "None")
add("18", s, "No unofficial channel automation, CAPTCHA/paywall bypass, private scraping", "C", "BRL-SRC; FR source policy", "None")
add("18", s, "Verify provider processing, retention, residency, deletion", "C", "Part 4.1 §4.14", "None")
add("18", s, "Security acceptance list incl. SSRF, forged callback, replay, exfiltration, cost exhaustion, recovery", "C", "Part 4.1 §4.16; Part 6", "Mapped in SVM", "SVM-01…12")
add("18", s, "Independent reviewer validates threat model, isolation, cache, RAG, replay, finance; critical defects block", "C", "BLK-1…BLK-4", "None")
s = "Product security and governance controls (table)"
for t in ["Product boundary (distinct audiences)", "Tenant/issuer isolation with composite constraints", "Public publication (verified host, snapshot)",
          "Data minimization (no wealth inference, no clinical/child data)", "Regulated route (approved claims/pricing)", "Security response (revoke, isolate, stop dispatch)"]:
    add("18", s, t, "C", "Part 4.1 §4.1–4.4, §4.11, §4.17", "None")
s = "Threat-control implementation matrix"
for t in ["Broken object authorization (tenant A/B same ID shape)", "Cross-product identity", "Confidential public data (DTO and bundle inspection)",
          "Workflow attack surface", "AI and knowledge (vector namespaces, metadata filters)", "Finance and consent"]:
    add("18", s, t, "C", "Part 4.1 §4.8.2; NFR-001/032; Part 6", "Mapped to SVM", "SVM map")
s = "Implementation acceptance and verification (15 procedures)"
for t, loc in [("Product and audience isolation", "NFR-003; AP-10"), ("Tenant and startup isolation", "NFR-032; AP-10"), ("Privileged identity and revocation", "NFR-050"),
               ("Autonomy and approval at all levels", "DEC-064; BRL-AUT"), ("Independent client tenant lifecycle", "EP-20; FR-W31…W34"),
               ("Authorization and error contract", "NFR-015; ADR-022"), ("RAG scope and evidence", "Part 6.4 AIE"), ("Source permission and provenance", "NFR-028"),
               ("Existing identity reuse", "US-0101; BLK-9"), ("Public/portal/Admin separation", "NFR-001"), ("Communication eligibility", "NFR-095"),
               ("Public offer and claims restrictions", "DEC-060; GL-C06"), ("Cross-border and regional decision", "GL-C02"),
               ("Retention, portability and deletion", "NFR-075/076, NFR-086"), ("Sensitive data exclusions", "DEC-010/011")]:
    add("18", s, t, "C", loc, "Mapped to acceptance-procedure table", "§4.4.4.6")
add("18", s, "Authorization-safe cache key: product, tenant, startup, principal/grant fingerprint, permission, policy, model, knowledge revisions, normalized query", "P", "Part 3.1 §3.1.11 (scope + revision only)", "Key composition standard added", "CS-SEC-07; FR-ENH-I-010; RECOMMENDATION-467")
add("18", s, "Numeric validation: reject invalid weights, non-finite inputs, negative counts, out-of-range ratios", "N", "No numeric guardrail rule", "Rule and tests added", "CS-PY-09; FR-ENH-I-011; RECOMMENDATION-473")
add("18", s, "Boundary conditions: revalidate permission, eligibility, budget, content at execution", "C", "ARP-04; PDP dispatch recheck", "None")
s = "Current scope: security and applicant draft"
add("18", s, "Separate product, portal, applicant, Admin audiences; MFA Admin; consent/jurisdiction fail closed", "C", "DEC-019; ARP-05", "None")
add("18", s, "Applicant draft boundary: opaque expiring reference, isolated draft storage, idempotent provisioning after authority", "C", "Part 3.3 ENT-187 saas_application_draft; BRL-SVC-02; FRD §16.3", "None")

# ---------------- document 25 ----------------
s = "Repository and change discipline"
add("25", s, "Separate website React, Admin React, Django domain, deployment configs; shared libs without data/credentials", "C", "Part 4.3 §4.32.1 ADR-060; import-linter", "None")
add("25", s, "Acceptance: dependency graph proves no cross-product runtime import", "P", "NFR-085 (module contracts only)", "Cross-product import contract added", "CS-GEN-03; TC-ENH-I-001")
add("25", s, "Git workflow: issue-linked branches, focused commits, protected main, independent approval, green CI", "C", "Part 4.3 §4.32.2", "Expanded in coding standard", "CS-GIT-01…08")
add("25", s, "Emergency fixes follow same audit trail with expedited reviewer", "P", "Part 4.3 hotfix row", "Expedited-review rule added", "CS-REV-09")
add("25", s, "AI-assisted coding: treat generated code as untrusted; never paste secrets/real records; no invented APIs", "N", "None (B09 seats only)", "AI-assisted coding policy added", "CS-AIC-01…08; GAP-460")
s = "Frontend engineering"
add("25", s, "TypeScript strict; validate server payloads at boundaries; no any for business/financial fields; generated contracts", "P", "Part 4.3 PL-03; Part 3.1 Zod", "Full TS standard", "CS-TS-01…10")
add("25", s, "React: separate presentation, query hooks, mutation services; no side effects during render; cancel stale requests", "P", "NFR-027; Part 3.1 TanStack Query", "Full React standard", "CS-RE-01…12")
add("25", s, "Component tests cover loading, error, denied and empty states", "P", "Part 2.5 UI states", "Test rule added", "CS-TEST-06")
add("25", s, "Scope-aware query keys (product, tenant, startup, audience, filters, identity); clear caches on switch/logout; no private payload in service worker", "P", "NFR-027; FR-UIS-01", "Query-key standard added", "CS-RE-04…06")
add("25", s, "Forms: client validation for UX, server for authority; sanitize rich content; disable duplicate submit; show approval requirement", "P", "Part 2.5 forms", "Form standard added", "CS-RE-08…10")
add("25", s, "Accessibility: keyboard, focus, labelled errors, responsive; WCAG 2.2 AA; documented exceptions", "C", "NFR-088/089; Part 2.5 §2.46", "Coding rules restated", "CS-A11Y-01…06")
s = "Backend and persistence"
add("25", s, "Python: type hints, explicit DTOs, narrow exceptions, Ruff; no silent catch-all", "P", "Part 4.3 tooling row", "Python standard", "CS-PY-01…10")
add("25", s, "Django: views authenticate/validate; service owns transaction and transition; selectors enforce scope; no logic only in UI or signals", "N", "Not specified", "Service/selector layering standard", "CS-DJ-01…10")
add("25", s, "DRF: allowlist fields, deny by default, scope queryset before lookup, bounded pagination, validated sort/filter, safe error + correlation ID", "P", "NFR-015; PL-05 __all__ ban", "DRF standard", "CS-API-01…12")
add("25", s, "PostgreSQL: UUID, UTC, Decimal, FK/unique/check, composite ownership, RLS, parameterized queries; query plans reviewed", "C", "NFR-017; Part 3.3", "SQL standard restated with checks", "CS-SQL-01…09")
add("25", s, "Outbox and concurrency: atomic commit, async dispatch, lock or revision compare, unique action key", "C", "ARP-03; NFR-006, NFR-025; ADR-023", "Code pattern added", "CS-DJ-07; pattern P-04")
add("25", s, "Failure semantics: retry 429/5xx with backoff, jitter, Retry-After; no retry on permanent denial; unknown → reconcile", "C", "NFR-016, NFR-026; DEC-050", "Code rule added", "CS-WRK-04…06")
s = "AI and integration engineering"
add("25", s, "Prompt contract: schema, purpose, allowed evidence, prohibited disclosure, abstention, tool limits; approved revision and eval results", "C", "Part 7.2 agent specs; BRL-AI-09", "Coding rule restated", "CS-AI-01…06")
add("25", s, "Retrieval: filter before nearest-neighbour; approved, non-revoked sources; content as data", "C", "ADR-041; Part 4.1 §4.15", "Restated", "CS-AI-04")
add("25", s, "Adapters: typed interface with timeout, retry, quota reservation, signature verification, sandbox mode; no vendor SDK in domain", "C", "ADR-009; ARP-06", "Restated", "CS-ADP-01…07")
add("25", s, "Telemetry: structured event with correlation, scope ref, duration, outcome; redact tokens and content", "C", "Part 4.3 §4.39.1; NFR-078", "Restated", "CS-OBS-01…06")
s = "Review and definition of done"
add("25", s, "Reviewer examines acceptance, role, scope, finance, error paths, schema, tests, cost, rollback; record tradeoffs", "P", "Part 4.3 §4.32.2 checklist", "Full review checklist by risk class", "CR-CHK-01…40")
add("25", s, "Changed-line coverage ≥ 80% on eligible domain code; critical decision branches tested; generated code excluded only with approval", "X", "NFR-082 (overall coverage)", "Diff-coverage gate added; conflict raised", "CONFLICT-468; CS-TEST-03")
add("25", s, "Completion: merge only after UI/API/table links updated, evidence attached, operational impact assessed", "P", "Part 5 DoD", "DoD code addendum", "CS-REV-12")
s = "Code review rules and repository layout (table)"
add("25", s, "Per-product layout website-react/, admin-react/, backend/, tests/, infra/, docs/", "C", "Part 4.3 §4.32.1 (equivalent monorepo layout)", "Mapping noted", "CS-GEN-02")
add("25", s, "Frontend lead: strict TS, accessible, scoped keys, abort stale, no browser credentials", "P", "As above", "Standard", "CS-TS, CS-RE")
add("25", s, "Backend lead: small services, serializer validation, authorization in service, transaction/outbox, deterministic errors", "P", "As above", "Standard", "CS-DJ")
add("25", s, "Database lead: tenant ownership, composite FKs, fixed precision, uniqueness, measured query plans", "C", "NFR-017", "Standard", "CS-SQL")
add("25", s, "Tech lead review: scope, security, failure modes, migrations, unit/SIT, maintainability; no AI code merged without human review", "P", "Part 4.3 §4.32.2", "Standard", "CS-REV, CS-AIC")
add("25", s, "CI: lint/type, tests, secret/dependency scans, digest, approved migration, review evidence", "C", "Part 4.3 §4.33.2 PL-02…PL-11", "None")
s = "Reference code patterns"
add("25", s, "Correct scoped lookup pattern (membership check then filtered get)", "P", "ARP-02 principle only", "Pattern P-01 with negative example", "P-01")
add("25", s, "React stale-response protection with AbortController and live flag", "N", "Not specified", "Pattern P-02", "P-02")
add("25", s, "Safe financial arithmetic with Decimal; validate currency, entity, provider reference", "P", "ADR-030", "Pattern P-03", "P-03")
add("25", s, "Executable reference: commercial_quote('2','150.00','10') = 270.00", "C", "BLK-6; FRD §12.1 worked example", "Pattern P-03 test", "P-03")
s = "Practical implementation rules (code acceptance table)"
add("25", s, "React/TS: server-authorized data; scope switch invalidates; no secret/internal DTO in Website bundle", "C", "NFR-001; NFR-027", "None")
add("25", s, "Django: serializer allowlist; membership, object grant, permission, expected revision; transaction and outbox", "C", "NFR-025; ARP-02/03", "None")
add("25", s, "PostgreSQL: composite scoped FKs, unique idempotency keys, numeric money, no cascade deleting posted records", "P", "NFR-017/018", "No-cascade rule added", "CS-SQL-07")
add("25", s, "Python AI: schema- and evidence-check; AI never decides authorization, legal or payment truth", "C", "ARP-08; BRL-AI-07", "None")
add("25", s, "Review: run lint/type/unit/integration in actual repos; review generated code, deps, scope, concurrency, rollback", "P", "Part 4.3 §4.33", "Review checklist", "CR-CHK")
s = "Implementation acceptance procedures (9)"
for t, st, loc, new in [("Upload and dependency safety", "C", "NFR-021; PL-09", ""), ("Query and rendering efficiency (query count, EXPLAIN ANALYZE, React profiler)", "P", "Part 3.1 lever 1", "CS-PERF-01…08; TC-ENH-I-003"),
                        ("Idempotency and duplicate delivery (same key changed payload rejected)", "C", "NFR-005; ADR-023", ""), ("Shared library boundaries (wrong product config)", "P", "NFR-031", "TC-ENH-I-002"),
                        ("Repository and modular boundaries (owner, tests, public interface)", "P", "NFR-085", "CS-GEN-04"), ("Shared workflow and adapter code", "C", "ADR-009, ADR-027", ""),
                        ("UI component reuse with distinct business settings", "C", "Part 2.5 §2.45", ""), ("Test fixture reuse without leakage; deterministic", "C", "RECOMMENDATION-017", ""),
                        ("AI-assisted coding quality", "N", "—", "CS-AIC; TC-ENH-I-004")]:
    add("25", s, t, st, loc, "Covered" if st == "C" else "Added", new)
s = "Current scope: coding standards"
add("25", s, "Typed dynamic forms and explicit capability predicates; no hardcoded startup position; safe rendering", "P", "FR config-driven forms (CFG)", "Rule added", "CS-RE-11; CS-GEN-06")

# ---------------- document 26 ----------------
s = "Deployment topology"
add("26", s, "Separately built frontends with distinct origins and audiences; public ingress allowlist", "C", "NFR-001; ADR-006", "None")
add("26", s, "Stateless Django behind LB; private PostgreSQL, storage, Valkey; separate Celery pools", "C", "Part 3.1 §3.1.6", "None")
add("26", s, "Separate research, AI, communication, financial and priority control queues; one scheduler per scope; prefetch/limits; bounded retries", "X", "ADR-021 (no finance or control queue; prefetch not set)", "Queue additions proposed", "CONFLICT-473; FR-ENH-I-030")
add("26", s, "IaC OpenTofu/Terraform; separate product/env state; encrypted backend, locking; plan review", "C", "Part 4.3 §4.34; ADR-012/051", "None")
s = "Continuous integration"
add("26", s, "PR: locked deps, lint/type, unit, secret, dependency and container scan; synthetic data", "C", "PL-02…PL-09", "None")
add("26", s, "Build: env-specific public values only; non-root pinned base; SBOM; immutable digests", "C", "PL-10/11", "None")
add("26", s, "SIT: ephemeral PostgreSQL/Valkey, migrations, synthetic fixtures, API contracts, workflow/browser integration, stub providers", "P", "PL-06/07/15 (named CI/test)", "SIT stage mapping added", "§4.4.5.2 table; CONFLICT-471")
add("26", s, "Staging/UAT: promote exact digest; sanitized or synthetic data; sandbox credentials; independent test audiences", "C", "Part 3.1 §3.1.14; PL-14", "None")
s = "Continuous delivery and rollback"
add("26", s, "Pre-deploy: capacity, compatibility, backup point, migration plan, flags, on-call, approval; freeze conflicting changes; signed go/no-go", "P", "PL-17 (no freeze, no on-call check)", "Pre-deploy checklist added", "DPL-PRE-01…10")
add("26", s, "Deploy order: expand schema, validate, API, workers/scheduler, Admin and website separately, smoke before automation", "P", "PL-18 (order not stated)", "Ordered deployment runbook", "DPL-SEQ-01…09")
add("26", s, "Canary: limited internal/approved cohort; compare error, latency, queue lag, invariants; operator approves widening", "P", "ADR-053 blue/green at scale only", "Cohort canary for activation", "RECOMMENDATION-461; DPL-CAN")
add("26", s, "Rollback: disable automation first; preserve receipts and outbox; revert compatible artifact; no blind schema reversal; reconcile", "C", "Part 4.3 §4.38; RB-012", "None")
add("26", s, "Post-deploy: role-based smoke, publication check, queue drain, reconciliation, budget verification, observation window", "P", "PL-19 (30 min SLO watch)", "Smoke catalogue added", "SMK-01…14")
s = "Infrastructure controls"
add("26", s, "Network: private DB/broker, restricted ports, WAF/rate limit, Admin MFA, optional access gateway", "C", "Part 4.1 §4.9; GL-S07", "None")
add("26", s, "Identity: short-lived CI credentials via workload identity; least-privilege deploy roles; approver ≠ developer", "C", "ADR-026/050; PL-17", "None")
add("26", s, "Capacity: requests/limits; autoscale on latency and queue age; protect priority queues; per-tenant caps", "P", "Part 4.2 §4.27 (manual triggers)", "Queue-age scaling rule added", "FR-ENH-I-031")
add("26", s, "Recovery: automated encrypted backups and isolated restore rehearsal; no shared resources across trust boundary", "C", "Part 4.3 §4.47", "None")
s = "Pipeline outline and delivery table"
add("26", s, "Pipeline outline PR→SIT→staging→production→controlled activation", "C", "Part 4.3 §4.33.3", "Activation stage made explicit", "DPL-SEQ-09")
add("26", s, "Activation stage: explicit owner/CTO approval; enable gradually within approved budgets; stop on gate failure", "P", "Part 8.2 GL-B04 (charter)", "Activation stage added", "DPL-ACT-01…06")
add("26", s, "Reference CI workflow (offline starter: unittest, compileall, verify_catalogs)", "NA", "Pack reference asset only", "Noted; product CI is Part 4.3")
add("26", s, "Companion root CI command and PostgreSQL compose/AWS blueprint are review assets", "NA", "Pack assets", "Noted")
s = "Reproducible CI and isolated rehearsal (table)"
for t, st in [("Offline CI with archived artifacts, no deployment step", "NA"), ("Product CI incl. browser tests, migration checks, SBOM, signed image", "C"),
              ("Staging independent Website/Admin/API/workers/DB/cache via approved IaC; no live dispatch", "C"), ("Release reviews Terraform plan, migration/recovery, evidence gate, security and load", "C"),
              ("Rollback with compatible previous image, pause workers, reconcile, reviewed restore", "C")]:
    add("26", s, t, st, "Part 4.3 §4.33–4.38", "None")
s = "Implementation acceptance procedures (7)"
add("26", s, "Load test reproducibility (pin dataset, commit, mix, ramp, warmup, error budget)", "P", "Part 4.2 §4.26", "Load-test record template", "LTR-01…14")
add("26", s, "Capacity and region decisions (residency, saturation, scale limits)", "C", "DEC-040; Part 3.1 §3.1.12", "None")
add("26", s, "Migration backward compatibility in disposable restored DB; row counts reconciled", "C", "Part 4.3 §4.37.2; PL-07", "None")
add("26", s, "Independent CI and environment (digest, config, scoped identity)", "C", "PL-10/11/14", "None")
add("26", s, "IaC completeness with cost estimate; no prod apply without approval", "C", "Part 4.3 §4.34", "None")
add("26", s, "Fail-closed evidence inventory (required-ID list, reject missing/extra/duplicate, mandatory N/A)", "N", "A090 evidence assembly (no validator rules)", "Release gate validator specified", "RGV-01…14; GAP-463")
add("26", s, "Resource and deployment approval: incremental effort estimate per change; approval before cost/SLA promise", "P", "Part 8.2 §8.2.2.4 change control", "Rule restated", "DPL-PRE-10")
add("26", s, "Current scope: browser route/interaction checks per product; deploy only after migration, QA, release sign-off", "C", "PL-15; Part 8.2", "None")

# ---------------- document 27 ----------------
s = "Environment matrix"
for t, st, loc in [("Local: disposable DB/broker, mock providers, developer credentials, no production data", "C", "Part 3.1 §3.1.14 local"),
                   ("Shared development: integration branch, separate identities, limited quotas", "X", "Not provided (trunk-based)"),
                   ("SIT: pinned artifact, isolated DB, fake/sandbox callbacks, repeatable reset", "P", "test/CI env"),
                   ("UAT: business users, sandbox channels, approved test identities", "P", "staging"),
                   ("Staging: production-like, masked/synthetic data, recovery rehearsal", "C", "staging"),
                   ("Production: separate credentials, real channels only after activation, audited access", "C", "prod"),
                   ("Recovery: isolated recovery environment; no dispatch until reconciliation and restart", "P", "Part 4.3 backup restore sandbox")]:
    add("27", s, t, st, loc, "Environment mapping added", "CONFLICT-471; ENV matrix")
s = "Configuration contract"
add("27", s, "Identity config: PRODUCT_ID, APP_ENV, WEBSITE_ORIGIN, ADMIN_ORIGIN, OAUTH_ISSUER, WEBSITE_AUDIENCE, ADMIN_AUDIENCE; fail closed", "N", "Parameter Store paths only", "Config contract catalogue", "ENV-01…07; GAP-461")
add("27", s, "Persistence refs: DATABASE_URL, BROKER_URL, OBJECT_BUCKET, VECTOR_NAMESPACE as secret refs/scoped IDs, never frontend", "P", "Part 4.1 §4.6.1", "Catalogue", "ENV-08…11")
add("27", s, "Execution: AUTOMATION_ENABLED false in nonprod; PAID_FALLBACK_ENABLED false; timeout, retry, budget ceilings", "P", "Flags (Part 4.3 §4.36) OFF by default", "Catalogue", "ENV-12…16")
add("27", s, "Provider config references connection, sender, entitlement, purpose, scope; vault secrets server-side", "C", "Part 4.1 §4.6", "None")
add("27", s, "Observability config: LOG_LEVEL, OTEL endpoint, redaction rules, alert destination", "P", "Part 4.3 §4.39", "Catalogue", "ENV-17…20")
add("27", s, "Feature flags typed, scoped, time-bounded; owner approval for external dispatch; default off; audited, reversible", "C", "Part 4.3 §4.36", "None")
s = "Secrets and dependencies"
add("27", s, "Secret lifecycle: generate in vault, store reference, rotate with overlap, revoke, test; emergency revocation stops job", "C", "Part 4.1 §4.6.2", "Procedure detailed", "SEC-ROT-01…08")
add("27", s, "Developer access: temporary env-specific with MFA; no shared credentials; revoke on departure; monthly review", "P", "SC-48 (no standing DB access)", "Access review procedure", "GAP-469; ACC-01…07")
add("27", s, "Dependency locking incl. container digest, migration compatibility, model/prompt revision; licence and vuln at change", "P", "uv/pnpm lockfiles; PL-09", "Model/prompt revision pinned in release manifest", "CS-DEP-01…08")
add("27", s, "Config drift: schema validation at startup; deployed non-secret config hash vs approved manifest", "P", "IaC drift only (AL-47)", "Config-hash drift check", "FR-ENH-I-040; AL-55; RECOMMENDATION-468")
add("27", s, "Recovery: restore secret references and config from protected inventory; no secrets in backup notes", "P", "Part 3.1 §3.1.13.2 secrets row", "Recovery step added", "ENV recovery rule")
s = "Configuration table (15 variables)"
for v in ["APP_PRODUCT=commercial immutable", "APP_ENV local/dev/SIT/UAT/staging/prod", "DATABASE_URL secret reference", "SECRET_MANAGER_REF", "ADMIN_AUDIENCE rejects external identity",
          "PORTAL_AUDIENCE rejects staff privileges", "ALLOWED_HOSTS verified, no wildcard", "EXTERNAL_DISPATCH_ENABLED false", "PAID_FALLBACK_ENABLED false",
          "WORKER_QUEUE_PREFIX per product/env", "OBJECT_STORE_REF / VECTOR_STORE_REF", "PROVIDER_SECRET_REF", "MAX_REQUEST_BYTES / RATE_LIMIT", "LOG_REDACTION_POLICY", "RECOVERY_TARGETS"]:
    add("27", s, v, "N" if v.split()[0] in ("APP_PRODUCT=commercial", "APP_ENV", "WORKER_QUEUE_PREFIX", "RECOVERY_TARGETS", "LOG_REDACTION_POLICY", "SECRET_MANAGER_REF") else "P",
        "Part 4.1 §4.6; Part 3.1 §3.1.14", "Catalogue row", "ENV-01…24")
add("27", s, "Rotation procedure (inventory → issue → stage/test → atomic switch → revoke → verify; compromise → disable dispatch)", "P", "Part 4.1 §4.6.2 (cadence only)", "Step procedure", "SEC-ROT-01…08")
s = "Environment manifest and rotation (table)"
for t in ["Required config incl. automation_enabled=false", "Secret handling: no secrets in bundle, Git, logs, fixtures, workbook", "Dependency control incl. model artefacts",
          "Rotation create/validate/deploy/verify/revoke/audit", "Nonproduction never points at production accounts"]:
    add("27", s, t, "C" if "Nonproduction" in t or "Secret handling" in t else "P", "ABAC-12; Part 4.1 §4.6", "Covered by ENV/SEC-ROT", "ENV, SEC-ROT")
s = "Implementation acceptance procedures (5)"
add("27", s, "Dependency and technical debt inventory (owner, remediation date)", "N", "No tech-debt register", "Tech-debt register", "CS-DOC-05; TDR fields; RECOMMENDATION-472")
for t in ["Privileged identity and revocation", "Upload and dependency safety", "Existing identity reuse", "Independent CI and environment"]:
    add("27", s, t, "C", "NFR-050; NFR-021; BLK-9; PL-10", "None (duplicate of docs 18/25/26)")
add("27", s, "Current scope: connection references only in UI; per-product/tenant secret store; pinned config revision", "C", "Part 4.1 §4.6.1; A112", "None")

# ---------------- document 29 ----------------
s = "Workload and measurement"
add("29", s, "Initial capacity workload (25+10, 50 staff, 100k opps, 50 jobs, 10k actions/day)", "X", "DEC-031", "Workload profile WP-01", "CONFLICT-461; WP-01")
add("29", s, "Growth capacity workload (50+/100, 250 staff, 1m opps, 250 jobs, 100k/day)", "X", "DEC-031", "Workload profile WP-02", "CONFLICT-461; WP-02")
add("29", s, "Measurement conditions: indexed dashboard excludes live research; ACK after durable acceptance; record dataset, hardware, cache, mix, stubs", "P", "Part 4.2 §4.21", "Load-test record template", "LTR-01…14")
add("29", s, "Traffic mix 60% list/filter, 20% details, 10% safe writes, 10% background status; public separate", "X", "Part 4.2 LT-01 70/15/10/5", "Profile adopted for dashboard test", "CONFLICT-466; WP-03")
s = "Test scenarios"
add("29", s, "Baseline: single user, one worker, cold/warm cache, SQL and trace", "N", "No baseline scenario", "Added", "LT-ENH-I-03")
add("29", s, "Load: ramp to initial then growth, hold 30 min each", "P", "LT-01 30 min at Y1", "Added", "LT-ENH-I-01, -02")
add("29", s, "Stress beyond target until saturation; stop on resource/correctness threshold", "C", "Part 6.1 LT-08", "None")
add("29", s, "Spike: 3× baseline public enquiries and callbacks", "X", "Burst 2× in same doc; LT-05/07", "Conflict raised", "CONFLICT-465; LT-ENH-I-04")
add("29", s, "Endurance: 8-hour soak at initial target; memory, connections, bloat, queue age", "X", "LT-02 4 h; GL-T04 24 h/72 h", "Conflict raised", "CONFLICT-467; LT-ENH-I-05")
add("29", s, "Noisy neighbour: one tenant at quota while another uses dashboard", "C", "LT-11; NFR-062", "None")
add("29", s, "Provider outage: timeout/429/5xx/unknown; retry budget, circuit, recovery", "C", "CH-01; RB-001", "None")
add("29", s, "Recovery: restore DB, replay outbox in dispatch-off mode; RPO/RTO and reconciliation", "P", "CH-03; RB-007 (no dispatch-off replay)", "Dispatch-off replay step", "LT-ENH-I-06; RB-007 addendum")
s = "Optimization and capacity"
add("29", s, "Frontend: bundle, LCP/INP/CLS p75 targets; Lighthouse plus RUM after consent", "C", "NFR-042/043", "None")
add("29", s, "Database: EXPLAIN ANALYZE, index tenant/startup/stage/time/cursor, N+1, lock waits", "P", "Part 3.3 indexes; lever 1", "Perf coding rules", "CS-PERF-01…08")
add("29", s, "Workers: queue age, throughput, retry, latency, per-tenant fairness; tune concurrency/prefetch", "P", "Part 4.3 metrics", "Prefetch rule and queue-age metric", "CS-WRK-08; AL-51")
add("29", s, "AI: tokens, latency, cache hit, abstention; local vs paid benchmark on fixed set", "C", "Part 7.3; NFR-030", "None")
add("29", s, "Capacity plan: resource cost per workload; autoscale ceiling; budget alert; monthly review", "C", "Part 4.3 §4.46.6; Part 4.2 §4.27", "None")
s = "Delivery-control scenario table (7 rows)"
add("29", s, "Burst: 2× approved short burst; bounded 429/queue; recover to baseline", "P", "LT-05, LT-07", "Burst acceptance", "LT-ENH-I-04")
add("29", s, "Endurance 8 h; no leak, no backlog; budgets reconcile", "X", "LT-02 4 h", "See CONFLICT-467", "LT-ENH-I-05")
add("29", s, "Projection: committed event to visible timestamp ≤ 60 s", "X", "NFR-047", "See CONFLICT-463", "")
add("29", s, "Recovery: stop worker/provider, restart, replay; no duplicates; backlog drains within window", "C", "CH-02; NFR-007", "None")
add("29", s, "Instrumentation list (histograms, saturation, pool, plans, queue age, provider failure)", "C", "Part 4.3 §4.39.2", "None")
add("29", s, "Mock-health k6 script is a smoke only; authenticated tests need approved contract and synthetic identity", "C", "PL-16; Part 6.1", "None")
s = "Workload and performance test execution (table)"
add("29", s, "Acceptance: proposed error rate < 1% during valid read-only test", "C", "LT-01 < 0.5% (stricter)", "None")
add("29", s, "k6 staging read-only script with explicit nonprod URL and synthetic token; never production", "P", "Part 4.2 load tooling", "Safety guard rules", "LT-SAFE-01…05")
add("29", s, "Evidence: workload, DB row count, latency distribution, errors, resources, config digest", "P", "Release record", "Load-test record template", "LTR-01…14")
s = "Mandatory measurable gates (25 rows)"
add("29", s, "Gate table of 25 metrics with target and verification context", "P", "Spread across NFR/KPI/SLO; no single OKPI register", "OKPI register mapped", "§4.4.4.2; RECOMMENDATION-470")
s = "Implementation acceptance procedures (11)"
for t, st, loc, new in [("Dashboard latency at 50/250 staff, 100k/1m opportunities", "X", "C10", "LT-ENH-I-01/02"), ("Public website responsiveness, lab proxy labelled", "C", "NFR-042", ""),
                        ("Async acknowledgement measured separately from completion", "C", "C6; NFR-051", ""), ("Query and rendering efficiency", "P", "—", "CS-PERF"),
                        ("Load test reproducibility", "P", "§4.26", "LTR"), ("Availability and error budget: eligible minutes, exclusions, zero denominator unassessed", "P", "Part 4.2 §4.21", "FR-ENH-I-050"),
                        ("Numeric guardrail validation (NaN, infinity, negatives)", "N", "—", "FR-ENH-I-011; TC-ENH-I-020"), ("Growth workload matrix", "X", "DEC-031", "WP-02"),
                        ("Noisy neighbour protection (tenant B progresses)", "C", "LT-11", ""), ("Accessibility keyboard/screen reader", "C", "NFR-089", ""),
                        ("Observability and incident recovery (inject failure; alert reaches owner; no PII)", "C", "Part 4.3 §4.41; NFR-078", "")]:
    add("29", s, t, st, loc, "Mapped" if st == "C" else "Added", new)
add("29", s, "Resource and deployment approval (incremental estimate, approval before SLA)", "C", "Part 8.2 §8.2.2.4", "None")
add("29", s, "Current scope: 26 owned startups, ten tenants, 20 simulated runs; indexed lists, cursor, fair scheduling, budget reservation", "C", "RECOMMENDATION-017 seeds; NFR-015", "None")

# ---------------- document 30 ----------------
s = "Authorization and test rules"
add("30", s, "Written authorization: hosts, environments, identities, techniques, time window; staging/synthetic only", "N", "Part 4.1 §4.16.2 scope only", "Rules of engagement", "PT-ROE-01…12; GAP-466")
add("30", s, "Threat model mapping all boundaries; threat register with mitigation owner", "C", "Part 4.1 §4.2", "None")
add("30", s, "Severity: Critical = confidential disclosure, financial integrity, production credential, uncontrolled dispatch", "X", "Part 4.1 §4.16.3 CVSS-based", "Business-impact overlay", "CONFLICT-472")
add("30", s, "Evidence: minimal redacted request/response, build, env, role, expected/observed; no secrets", "P", "EVR (Part 6.1)", "Finding record template", "PT-FND-01…14")
s = "Security verification matrix (12 rows)"
for t, st in [("Public exposure (draft, unknown host, Admin endpoint, cache variants)", "C"), ("Portal object scope (two invitees, expired grant, revoked invite)", "C"),
              ("Admin role and audience (external token, owner-only op, cross-product token)", "C"), ("Tenant isolation in query, export, worker, object URL, cache", "C"),
              ("Input safety (injection fixtures, malformed JSON, oversized upload, rich text, URL)", "C"), ("CSRF/CORS/CSP", "C"), ("Session and recovery (expiry, rotation, MFA, invitation replay)", "C"),
              ("Webhook replay (signature, wrong connection, stale timestamp, duplicate)", "C"), ("AI and RAG (embedded instruction, cross-startup evidence)", "C"),
              ("Workflow authority (unapproved template, budget, stale hash, cancelled job, duplicate)", "C"), ("Financial integrity (wrong issuer, currency, duplicate receipt/refund, premature closure)", "C"),
              ("Dependencies and infrastructure (SBOM, images, IaC, exposure, vault)", "C")]:
    add("30", s, t, st, "Part 4.1 §4.8, §4.16; Part 6 TCs", "Consolidated in SVM with TC-ENH-I", "SVM-01…12")
s = "Assessment and remediation"
add("30", s, "Tooling: ZAP in staging, dependency scanners, secret scan, SAST, manual role/object tests; record tool version, scope, false positives", "P", "Part 4.1 §4.16.1 (no false-positive review record)", "Finding record fields", "PT-FND")
add("30", s, "Independent reviewer verifies findings and fixes; retest evidence per defect", "C", "BLK-1/4; Part 6.1", "None")
add("30", s, "Go-live: security lead and owner accept residual risk within policy; never waive critical isolation/financial defect", "C", "BLK rows; GL-S03", "None")
s = "Threat/asset verification table (8 rows)"
for t in ["Admin identity", "Tenant/issuer data", "Website publication", "Portal invitations", "Workflow/financial", "AI", "Supply chain"]:
    add("30", s, t, "C", "Part 4.1; BLK-1…5", "Mapped to SVM", "SVM")
add("30", s, "Incident readiness: exercise containment, revoke, stop dispatch, preserve logs, recover", "C", "Part 4.3 §4.47 tabletop; RB-004/008/013", "None")
add("30", s, "Testing only in nonproduction or scoped pen-test; never attack third parties or use real records", "P", "Part 4.1 §4.16.2 out-of-scope list", "RoE rules", "PT-ROE")
s = "Authorized security test evidence matrix (5 rows)"
for t in ["Scope documented (date, tester, exclusions)", "IDOR/BOLA read/update/download", "Public security (publish, host, URL, input, rate)", "AI/worker (untrusted text, tool, retrieval, duplicate webhook, budget, stop)"]:
    add("30", s, t, "C" if "Scope" not in t else "N", "Part 4.1 §4.8.2", "RoE / SVM", "PT-ROE; SVM")
add("30", s, "Remediation: critical/high confidentiality/auth/financial/regulated findings block go-live; actual pen test not performed", "C", "NFR-072; GL-S03", "None")
s = "Implementation acceptance procedures (6)"
for t in ["Product and audience isolation", "Tenant and startup isolation", "Privileged identity and revocation", "Upload and dependency safety", "Prompt injection and tool access"]:
    add("30", s, t, "C", "Part 6.4; NFR-003/032/050", "None (duplicate)")
add("30", s, "Evidence integrity: reject missing controls, duplicates, mandatory N/A, blank evidence, executor = reviewer; verify hashes", "N", "EVR independence rule only", "Validator rules", "RGV-01…14")
s = "Current scope: cybersecurity scenario table (UX-QC-01…10 duplicate)"
add("30", s, "Ten scenario rows (scope onboarding … accessibility navigation)", "P", "Part 6 TCs (partial)", "See doc 32 UX-QC mapping", "§4.4.4.5")

# ---------------- document 31 ----------------
s = "Observability design"
add("31", s, "Metrics: request count/error/latency by surface; queue age, retries, DLQ, scheduler, DB connections, locks, replication/backup", "C", "Part 4.3 §4.39.2", "Add lock-wait and scheduler metrics", "MET-01…06")
add("31", s, "Business signals: eligible opportunities, dispatch outcome, follow-up due, objection escalation, approvals, verified closure", "P", "RP-xx reports; metrics catalogue", "Business signal metrics", "MET-07…12")
add("31", s, "AI metrics: model, prompt revision, tokens, latency, schema failure, abstention, cost; no raw prompts", "C", "§4.39.2 ai_* metrics", "None")
add("31", s, "Tracing correlation across browser/API/outbox/worker/adapter", "C", "§4.39.1; NFR-079", "None")
add("31", s, "Tools: OpenTelemetry, Prometheus, Grafana, structured logs; monitoring works when business UI fails", "C", "ADR-058/025 (CloudWatch; Grafana optional)", "Independent monitoring path test", "TC-ENH-I-030")
s = "Alerts and triage"
add("31", s, "P1 critical: leak, financial mismatch, unapproved dispatch, outage; ack 15 min; pause and page", "C", "§4.43.1 Sev1", "P-to-Sev map", "§4.4.5.6")
add("31", s, "P2 high: persistent errors, backlog, provider degradation, missed business deadline; ack 1 h", "C", "Sev2 ack ≤ 30 min (stricter)", "Missed business deadline alert added", "AL-54")
add("31", s, "P3 medium: noncritical UI, isolated failed job, quality decline; next business day", "C", "Sev3", "None")
add("31", s, "Thresholds: p95 over target 10 min; 5xx > 2% 5 min; projection lag > 60 s; integrity event immediate", "P", "AL-04/05 (15 min), AL-06", "Projection-lag alert added", "AL-52")
add("31", s, "Budget warn 80%, deny/pause at hard cap, paid fallback needs authorization", "C", "AL-14; BRL-AI-08", "None")
s = "Incident runbooks"
add("31", s, "Provider outage runbook", "C", "RB-001", "None")
add("31", s, "Data isolation incident runbook", "C", "RB-008", "None")
add("31", s, "Queue backlog runbook", "C", "RB-002", "None")
add("31", s, "Financial exception runbook (quarantine, stop closure, finance verifies, append correction)", "N", "No RB for financial mismatch", "RB-016 added", "RB-016; GAP-465")
add("31", s, "Public content incident runbook (unpublish, purge, retain audit, approve replacement)", "N", "No RB", "RB-017 added", "RB-017; GAP-465")
add("31", s, "Postmortem: impact, timeline, root cause, contributing factors, actions, owners, dates; regression case", "C", "§4.43.5", "None")
s = "Support operations"
add("31", s, "Intake: ticket with product, tenant, role, issue, severity, redacted evidence; verify caller authority", "P", "§4.45 (caller authority not stated)", "Caller verification step", "SUP-01…05")
add("31", s, "Support grants client-authorized, time-limited, purpose-scoped, audited, revoked on completion", "C", "DEC-056", "None")
add("31", s, "Communication: status and workaround without confidential details; escalate finance/legal/security", "C", "§4.43.4", "None")
add("31", s, "Review cadence: daily critical queue, weekly incident trends, monthly SLA/cost/quality", "P", "Monthly ops review; FinOps cadence", "Cadence table", "SUP-06…08")
s = "Metric/alert table (8 rows)"
add("31", s, "HTTP p95 dashboard > 2 s / 2.5 s; ACK > 2 s", "C", "AL-04/05 (stricter)", "None")
add("31", s, "Error ratio 5xx > 1% for 10 min", "X", "AL-06 > 2% for 5 min", "Two-tier alert", "CONFLICT-464; AL-50")
add("31", s, "Queue age: oldest eligible ready job > 5 min for 5 min", "P", "AL-07 outbox oldest > 5 min; AL-27", "Per-queue age alert", "AL-51")
add("31", s, "Budget hard limit breached or negative remaining → immediate dispatch stop", "P", "AL-14 (no negative-remaining check)", "Negative remaining alert", "AL-53")
add("31", s, "Isolation/credential: unauthorized success, suspicious token, secret exposure", "C", "AL-31/33/41", "None")
add("31", s, "Financial mismatch: duplicate/unmatched/wrong issuer/currency/unreconciled callback → freeze", "N", "No alert rule", "AL-56 + RB-016", "AL-56")
add("31", s, "AI quality: critical leakage or unsupported action → disable, revert prompt, regression", "C", "AL-39/49; RB-015", "None")
add("31", s, "Backup missing or restore not verified by cadence → block unsafe deployment", "C", "AL-23, AL-46; PL-17", "None")
add("31", s, "Incident lifecycle (detect → classify → commander → contain → preserve → diagnose → remediate → verify → communicate → RCA)", "C", "§4.43.3; Part 4.1 §4.17", "None")
s = "Operating signals table (5 rows)"
for t, st, new in [("Dashboard/ACK p95 alert with slow query, queue lag, projection", "C", ""), ("Queue/outbox: oldest age, repeated failure, uncertain, duplicate event, exhausted budget", "P", "AL-57"),
                   ("Confidentiality: foreign access or secret/PII in logs → stop feature", "P", "AL-58"), ("Financial mismatch hold closing", "N", "AL-56; RB-016"),
                   ("Operational record: detected/contained/restored times, correlation IDs, root cause, retest; no unsupported SLA claim", "P", "INC-REC")]:
    add("31", s, t, st, "Part 4.3 §4.41, §4.43", "Added" if st != "C" else "None", new)
s = "Optimization intelligence (reuse Admin interfaces)"
add("31", s, "No public/portal access; scoped filters; show 'unassessed' when no denominator; label stale metrics", "P", "RPT-R1 numerator/denominator; as-of", "Unassessed rule added", "FR-ENH-I-050")
add("31", s, "Seven dashboards: command centre, audit/jobs, cost/budget, health/incidents, AI quality, growth, revenue (19 API ops, 25 persistence sources)", "P", "Part 3.2 (14 of 19 ops); Part 3.3 equivalents", "Catalogue reconciled", "§4.4.4.3; CONFLICT-469; GAP-467")
s = "Implementation acceptance procedures (6)"
add("31", s, "Cost metering and anomaly response (duplicate usage not billed; hard limit halts)", "C", "NFR-014, NFR-035; KPI-24", "None")
add("31", s, "Workflow failure orchestration (timeout before/after unknown outcome)", "C", "NFR-026/065; RB-003", "None")
add("31", s, "Availability and error budget (zero denominator unassessed)", "P", "§4.40", "FR-ENH-I-050")
add("31", s, "Numeric guardrail validation", "N", "—", "FR-ENH-I-011")
add("31", s, "Observability and incident recovery", "C", "§4.41", "None")
add("31", s, "SLA and support commitments: no contractual claim before measured validation and signed terms", "C", "DEC-044; OPT-20-03", "None")
add("31", s, "Current scope: trace trigger/event/run/action IDs; step latency, cost, conflict, suppression; alert stale runs, unknown outcome, budget anomaly", "P", "run_id in logs; AL-10/14/15", "Stale-run alert", "AL-57")

# ---------------- document 32 ----------------
s = "Pre-go-live gates (9)"
for t, loc in [("Business acceptance (PO signs)", "GL-B01"), ("UI and API smoke; all catalogued items implemented or dispositioned", "GL-T02; BLK-10"), ("Data: migration rehearsal, counts, constraints, balances, backup/restore", "GL-D04, GL-T05"),
               ("AI/workflow: eval, dry-run, suppression, approvals, budget, kill switch", "GL-A01…A04"), ("Test completion (critical paths, defects closed, exceptions accepted)", "GL-T02; BLK-10"),
               ("Security: negative tests, vulnerability remediation, pen test", "GL-S01…S04"), ("Performance: initial targets tested; growth documented; capacity approved", "GL-T04"),
               ("Operations: monitoring, roster, alert drill, recovery, escalation", "GL-T06, GL-P02"), ("Compliance: route/channel/financial/legal and public claims", "GL-C01…C08")]:
    add("32", s, t, "C", "Part 8.2 §8.2.4.3 " + loc, "None")
s = "Deployment sequence"
add("32", s, "Prepare: immutable artifact record, window, communication plan, backup point, rollback owner, freeze", "P", "PL-17", "DPL-PRE", "DPL-PRE-01…10")
add("32", s, "Execute: disable dispatch, migrate compatible schema, deploy API, workers, website/Admin separately, verify health", "P", "PL-18", "DPL-SEQ", "DPL-SEQ-01…09")
add("32", s, "Smoke: anonymous page, external own record, unauthorized denial, Admin scoped query, synthetic intake, outbox, verified callback", "P", "PL-19 smoke set", "Smoke catalogue", "SMK-01…14")
add("32", s, "Activate: approved scopes/routes only; low-volume monitored execution", "C", "GL-B04 activation charter", "DPL-ACT", "DPL-ACT-01…06")
add("32", s, "Observe: agreed observation period: error, latency, queue, cost, financial consistency; formal acceptance", "C", "Part 8.2 §8.2.5 hypercare", "None")
s = "Rollback decision"
add("32", s, "Triggers: cross-tenant disclosure, invalid funds/receipt, duplicate effect, critical smoke failure, sustained severe error", "P", "RB-012 (deploy-caused only)", "Rollback trigger matrix", "RBK-T01…T08")
add("32", s, "Contain: pause automation, revoke access, preserve event and financial records", "C", "RB-004; RB-012", "None")
add("32", s, "Restore: revert compatible artifact; roll-forward or restore only after approved reconciliation", "C", "§4.38", "None")
add("32", s, "Reconcile provider/bank records, outbox, commitments before resume; finance and ops approve", "P", "RB-003 (no finance/ops dual approval)", "Resume approval rule", "RBK-R01…R05")
add("32", s, "Resume: rerun critical smoke and security tests; explicit owner approval for live dispatch; restart audit", "C", "RB-004 resume", "None")
s = "Delivery package"
add("32", s, "Technical handover: repos, artifacts, API/schema contracts, config refs, SBOM, test evidence, dashboards, recovery", "N", "No delivery package", "Handover checklist", "HO-T01…T10; GAP-464")
add("32", s, "Business handover: training, operating instructions, scope, contacts, exceptions, acceptance", "P", "Part 8.2 §8.2.2 training; hypercare exit 8", "Handover checklist", "HO-B01…B06")
add("32", s, "Access handover: transfer account/vault ownership, rotate temporary credentials, remove developer production access", "N", "—", "Handover checklist", "HO-A01…A06")
add("32", s, "Acceptance record left unsigned until actual delivery", "C", "BRD §12.2 EVR; BLK-11", "None")
s = "Checkpoint table (8 rows) and no-go criteria"
for t, st in [("Preparation: freeze scope, verify contracts, migration graph, environment, digest, support roles", "P"), ("Before deployment: restore rehearsal, deploy identity, config, cost limits, rollback package", "P"),
              ("Deploy schema: approved expand migration, lock/timeout, integrity", "C"), ("Deploy application independently; dispatch disabled", "P"), ("Verify business: synthetic E2E, portal, financial sandbox", "C"),
              ("Activate gradually; CTO/owner decision; monitoring active", "C"), ("Rollback: stop external actions, revert, reconcile, approved DR", "C"), ("Handover: access, manuals, support, training, residual risk", "N")]:
    add("32", s, t, st, "Part 4.3 §4.37–4.38; Part 8.2 §8.2.4", "DPL / HO", "DPL, HO")
add("32", s, "No-go list (authorization leak, financial discrepancy, mandatory test failure, missing backup, unapproved schema/API change, unsupported regulated op, unverified sender or paid fallback, absent monitoring/owner)", "P", "BLK-1…11 (sender verification and paid fallback not explicit)", "No-go rows added", "GL-E01…E06")
add("32", s, "Rollback does not undo an external payment, offer or message; reconcile instead of replaying", "C", "DEC-050; §4.38", "None")
s = "Go-live execution and hard-blocking gates"
add("32", s, "Preflight: all mandatory evidence approved; backup and rollback rehearsed", "C", "GL-T05; BLK-8", "None")
add("32", s, "Evidence check: release_gate.py against signed QC/acceptance register and manifests; pending returns non-zero", "N", "A090 manual assembly", "Release gate validator", "RGV-01…14; RECOMMENDATION-462")
add("32", s, "Deploy with automation disabled; confirm no public Admin data", "C", "NFR-001; SMK", "None")
add("32", s, "Activate eligible bounded workflows; monitor replies, spend, duplicates, finance", "C", "§8.2.5.3", "None")
add("32", s, "Rollback on critical isolation/finance/security/availability failure", "C", "RB-012; BLK", "None")
s = "Mandatory measurable gates (21 rows)"
add("32", s, "21 mandatory OKPI gates (see doc 38 OKPI-01…35)", "P", "Spread across NFR/KPI/SLO", "OKPI register mapping", "§4.4.4.2")
s = "Implementation acceptance procedures (7) and approval gates"
add("32", s, "Evidence gate fail-closed (delete QC row, duplicate ID, mandatory N/A)", "N", "—", "RGV + TC", "RGV; TC-ENH-I-040…042")
add("32", s, "Recovery and rollback: RPO 15 min, RTO 4 h / 2 h growth", "X", "DEC-018", "See CONFLICT-462", "")
add("32", s, "Granular QC and evidence (all QC IDs, owners, evidence; required ID baseline)", "P", "Part 6.6 RTM; A090", "RGV", "RGV")
add("32", s, "Backup and restore proof (hashes, counts; restore does not overwrite live)", "C", "§4.47", "None")
add("32", s, "Go-live and rollback gate rehearsal with incomplete evidence: no activation", "P", "BLK-11", "TC added", "TC-ENH-I-043")
add("32", s, "Outstanding approval gates: 38 exact API definitions, 0 partial, 4 DB confirmations, 138 UI semantic mappings", "N", "Pack-baseline counts not reconciled", "Gap raised to coordinator", "GAP-468")
add("32", s, "Fail-closed evidence inventory (authoritative required-ID list from immutable baseline)", "N", "—", "RGV-01…05", "RGV")
add("32", s, "Evidence integrity and final acceptance (executor ≠ reviewer after normalization; non-blank approval; artifact hashes)", "P", "EVR independence", "RGV-06…14", "RGV")
add("32", s, "Combined preflight: 1,188 records across six groups incl. 21 mandatory KPIs; CTO and PO authenticate and sign", "N", "No combined preflight", "Blueprint-equivalent preflight defined", "RGV-15; GAP-468")
s = "Current scope: release gates and UX-QC"
add("32", s, "Original evidence preflight plus expansion gate; field mapping, contract/DB decisions, new tests, independent review", "P", "BLK-10/11", "RGV", "RGV")
for i, t in enumerate(["Scope and onboarding (26 owned startups, ten client tenants)", "Capability-based routing (EduVerse blocked from external AI projects)", "Concurrent workflows (20 runs, revision pinning)",
                       "Event replay and conflict (E1 twice; competing action held)", "Omnichannel suppression (email and WhatsApp opt-out)", "Budget and recovery (below estimate; unknown outcome)",
                       "Shared closure state (consistent opportunity/quote/order IDs)", "Website and Admin handoff (SaaS application import, snapshot)", "Configuration lifecycle (revision 2, suspend, rollback)",
                       "Accessibility and navigation (every route, keyboard, widths)"], 1):
    add("32", s, f"UX-QC-{i:02d} {t}", "C" if i in (2, 3, 4, 5, 6, 9) else "P", "Part 6 TCs; see §4.4.4.5", "Mapped; gaps get TC-ENH-I", f"UX-QC-{i:02d}")

# ---------------- OPT controls (inventoried once) ----------------
OPT = [
 ("OPT-01-01", "18,25,27,30,32", "Authentication and privileged sessions", "C", "NFR-003; NFR-050"),
 ("OPT-01-02", "18,25,30", "Authorization and product isolation", "C", "NFR-002; NFR-031"),
 ("OPT-01-03", "18,25,30", "Tenant and startup isolation", "C", "NFR-032"),
 ("OPT-01-04", "18,25,30", "Public/portal/Admin boundary", "C", "NFR-001"),
 ("OPT-01-05", "18,25,30", "API and network security (bounded input, private network, egress allowlist)", "C", "Part 4.1 §4.9; NFR-022"),
 ("OPT-01-06", "18,25,30", "Secrets and supply chain", "C", "Part 4.1 §4.6; NFR-068"),
 ("OPT-01-07", "18,25,30", "AI and uploaded files", "C", "NFR-021; Part 4.1 §4.15"),
 ("OPT-01-08", "18,25,30", "Financial and audit security", "C", "NFR-018; DEC-038"),
 ("OPT-02-01", "25,26,29,31", "Public website assets (LCP/INP/CLS)", "C", "NFR-042/043"),
 ("OPT-02-02", "29", "React rendering and filters (debounce, cancel, virtualize, scope cache)", "P", "NFR-027, NFR-044"),
 ("OPT-02-03", "29", "API payload and pagination", "C", "NFR-015; C3"),
 ("OPT-02-04", "29", "Read projections cached by permission revision", "P", "Part 3.1 §3.1.11"),
 ("OPT-02-05", "29", "Async processing: durable ACK then enqueue; progress, cancel, timeout", "C", "ARP-09; C6"),
 ("OPT-02-06", "29", "Database and network: plans, N+1, pooling, streaming", "P", "Part 3.1 lever 1"),
 ("OPT-02-07", "29", "Parallel and batch operations bounded by tenant/provider", "P", "ADR-021"),
 ("OPT-03-01", "26,27,31", "Native versus paid plugins (zero unapproved paid calls)", "C", "NFR-037"),
 ("OPT-04-01", "31", "Daily planning and discovery", "C", "FR register (BRD OPT-04-01)"),
 ("OPT-05-01", "all", "Transactional outbox", "C", "NFR-006, NFR-063"),
 ("OPT-05-02", "26,31", "Idempotency and concurrency (key + payload fingerprint)", "C", "NFR-005, NFR-066"),
 ("OPT-05-03", "26,31", "Timeout and retry, circuit breaker, DLQ", "C", "NFR-016, NFR-064"),
 ("OPT-05-04", "26,31", "Durable workflow state, lease fencing", "C", "ADR-027"),
 ("OPT-05-05", "26,31", "Backpressure and fair scheduling; reserve urgent capacity", "P", "ADR-021 (no reserved control capacity)"),
 ("OPT-05-06", "26,31", "Config and AI failures: fail startup on missing config", "N", "No config validation at startup"),
 ("OPT-05-07", "26,31", "Availability 99.9% and reconciliation", "X", "DEC-018 99.5%"),
 ("OPT-06-01", "26,29,31", "Startup templates and tenants 25+10 / 50+ +100", "X", "DEC-031"),
 ("OPT-06-02", "26,29", "Concurrent users and jobs 50/250", "X", "DEC-031"),
 ("OPT-06-03", "26,29", "Data and scheduling volume 100k/1m; 10k/100k", "X", "DEC-031"),
 ("OPT-06-04", "26,29", "Regional expansion: locale, time zone, currency, residence", "C", "DEC-026; NFR-096/097"),
 ("OPT-06-05", "26,29", "Noisy neighbour and capacity", "C", "NFR-062"),
 ("OPT-07-01", "25,26", "Modular monolith", "C", "ADR-001; NFR-029"),
 ("OPT-07-02", "25", "Four frontends and two backends (investment + commercial)", "NA", "Investor product out of scope (DEC-009); isolation via NFR-031"),
 ("OPT-07-03", "25", "Domain and adapter boundaries; external calls outside DB transaction", "C", "ARP-06; ADR-009"),
 ("OPT-07-04", "25", "Configuration-driven design; invalid config rejected", "C", "Part 2.4 CFG"),
 ("OPT-07-05", "25", "Complexity and reuse review", "P", "No reuse review procedure"),
 ("OPT-08-01", "25,29", "Normalization and ownership; validated JSONB", "C", "Part 3.3"),
 ("OPT-09-01", "25,29", "Typed contracts 100% before activation", "C", "NFR-015; BLK-10"),
 ("OPT-10-01", "25,29,30,31", "Rules-first model routing", "C", "DEC-007; NFR-030"),
 ("OPT-12-01", "31", "Qualified funnel numerator/denominator", "C", "KPI register (BRD OPT-12-01)"),
 ("OPT-13-01", "25,27", "Code health", "P", "PL gates; no coding standard"),
 ("OPT-13-02", "25", "Technical debt register, monthly review", "N", "None"),
 ("OPT-13-03", "25", "Documentation and debugging runbooks synchronized", "P", "Runbooks RB-###"),
 ("OPT-13-04", "25", "Dependencies and compatibility, isolated upgrade branch", "C", "NFR-084"),
 ("OPT-14-01", "25", "Shared code libraries with independent runtime config", "C", "ADR-006/060"),
 ("OPT-14-02", "25", "Template reuse versioned and approved", "C", "Part 2.4 CFG; DEC"),
 ("OPT-14-03", "25", "Component contracts, no fork per tenant", "C", "Part 2.5 §2.45"),
 ("OPT-16-01", "25,26", "Standard setup: reproducible local env", "P", "Part 3.1 local env; no onboarding procedure"),
 ("OPT-16-02", "25,26", "Vertical slices and estimates (actual vs estimate)", "C", "Part 8.1"),
 ("OPT-16-03", "25,26", "AI-assisted development review", "N", "None"),
 ("OPT-17-01", "25,32", "Risk-based tests; 100% mandatory regression", "C", "Part 6.1"),
 ("OPT-18-01", "26,27,31,32", "Independent CI/CD; build once, promote digest", "C", "§4.33"),
 ("OPT-18-02", "26,27,32", "Migration and rollback expand/backfill/contract", "C", "§4.37.2"),
 ("OPT-18-03", "26,27,32", "Backup and DR RPO/RTO incl. growth 2 h and regenerable 24 h/8 h", "X", "DEC-018"),
 ("OPT-18-04", "26,27,32", "Observability and incident drills (scope denials, stale projections)", "P", "§4.41 (no stale-projection alert)"),
 ("OPT-19-01", "18,27,30,32", "Minimize data and source eligibility", "C", "NFR-028; DEC-010/011"),
 ("OPT-19-02", "18,30", "Communications and jurisdiction", "C", "NFR-095"),
 ("OPT-19-03", "18,30", "Rights and exports", "C", "NFR-075/076"),
 ("OPT-19-04", "18,30", "Clinical and education boundaries", "C", "DEC-010/011"),
]
for oid, docs, t, st, loc in OPT:
    add(docs, "Optimization engineering (" + oid + ")", oid + " " + t, st, loc, "Mapped in §4.4.4.1" + ("" if st == "C" else "; enhancement added"), oid)
