#!/usr/bin/env python3
"""Group F: atomic aspect inventory for source documents 15, 16, 21 (+ automation library in 38 §09),
coverage status against the blueprint, and generation of:
  final/coverage/F_coverage.csv  (aspects + one row per integration candidate IC-001..IC-538)
  <scratch>/F_register.md         (markdown fragment for Part 7.4a §7.4.3)
  <scratch>/F_counts.md           (markdown fragment for Part 7.4a §7.4.2)
Usage: python3 -I F_build_coverage.py <blueprint_dir> <scratch_dir>
"""
import csv, os, sys, collections

BP, SCR = sys.argv[1], sys.argv[2]
C, P, N, X, NA = "Covered", "Partially covered", "Not covered", "Conflict", "Not applicable"
CORE = "Common core: see document 01/02 coverage"

A = []  # (doc, section, id, summary, status, location, action, new_ids)
def a(doc, sec, i, s, st, loc, act="", new=""):
    A.append((doc, sec, i, s, st, loc, act or ("None (already covered)" if st == C else ""), new))

# ---------------- Document 15 ----------------
D = "15"
a(D, "Product purpose and operating boundary", "F15-001", "Commercial growth only; no investor/fundraising; independent deployment", NA, "Part 0 §0.2; DEC-002", CORE)
a(D, "Initial startup configurations", "F15-002", "Four seeded startups and commercial focus", NA, "Part 1 §1.3", CORE)
a(D, "Technology and execution principles", "F15-003", "Stack, open-source-first, autonomy modes, recheck at execution", NA, "Part 3.1; DEC-064", CORE)
contracts = [
 ("Knowledge", "Approved claims, documents, offering -> approved facts, citations, unknowns", "AG-001; TL-09; AU-029", C, "PC-01"),
 ("Research", "Permitted sources, geography -> queries, evidence, source IDs, freshness", "AG-003, AG-004; AU-007, AU-014", C, "PC-02"),
 ("Signal", "Source records -> signal type, evidence, confidence", "AG-005", C, "PC-03"),
 ("Matching", "Verified evidence + approved scoring -> score factors, missing evidence, explanation", "AU-016, AU-017 (rules); AG-007", P, "PC-04; FR-ENH-F-001 (missing_fields)"),
 ("Contact", "Org/person professional source -> role, channel, provenance, verification status", "AG-008; AU-018", C, "PC-05"),
 ("Engagement", "Eligible contact, approved facts, channel -> draft, claims, source IDs, escalation", "AG-011; AG-012; TL-10", C, "PC-06"),
 ("Response", "Inbound + thread -> intent, objection, next action, stop flag", "AG-013, AG-014; AU-008", C, "PC-07"),
 ("Objection", "Concern + approved evidence -> answer draft or specialist escalation", "AG-021", C, "PC-08"),
 ("Planner", "Objective, scope, budget, state, deadlines -> actions, cost, dependencies, approval", "AG-016; TL-18", P, "PC-09; FR-ENH-F-001 (cost_estimate, requires_approval)"),
 ("Meeting", "Authorized transcript/notes -> summary, actions, confirmed vs unconfirmed", "GAP-143 (excluded in Part 7.1)", N, "PC-10; AG-037 (new); FR-ENH-F-026"),
 ("Forecast", "Actual pipeline + evidence -> scenario, assumptions, uncertainty", "AU-041 (rules) + AG-029 narrative", P, "PC-11; AG-029 forecast mode (FR-ENH-F-002)"),
 ("Quality", "Candidate output, gold case, policy -> pass/fail, reason, severity", "AG-002; AG-012; AU-006", C, "PC-12"),
 ("Cost routing", "Token estimate, models, caps -> selected model, reserve, fallback", "AU-001, AU-002 (deterministic by design)", X, "PC-13; CONFLICT-411"),
 ("Copilot", "Authorized scoped request -> read/draft/action proposal, confirmation", "AG-015; DEC-035", C, "PC-14"),
 ("Business need", "Organization requirement + source -> need and offering match", "AG-006; AU-016", C, "PC-15"),
 ("Content and SEO", "Approved offering + audience -> draft content, claims, review", "AG-018; AG-012; AU-033", C, "PC-16"),
 ("Proposal", "Approved prices + bid/order requirements -> draft quote/proposal, assumptions", "AG-020; AU-035", C, "PC-17"),
 ("Retention", "Delivery, feedback, contract -> renewal opportunity and next action", "AU-039; AG-011 renewal mode; AG-026", P, "PC-18; AG-038 (new); FR-ENH-F-027"),
]
for k, (n, s, loc, st, new) in enumerate(contracts, 1):
    a(D, "Logical AI responsibilities and typed prompt contracts", f"F15-{9+k:03d}", f"Prompt contract '{n}': {s}", st,
      f"Part 7.2 §7.2.2 ({loc})", "Bound to prompt contract registry; envelope v2" if st != C else "Mapped in prompt contract registry", new)
a(D, "Prompt contracts", "F15-030", "Common instruction: retrieved docs are untrusted data; authorized scope; JSON; unknown when unsupported; cite evidence IDs; no invented claims; no direct external execution", C, "Part 7.3 §7.6.3, §7.6.5; BRL-AI-03/04; ADR-082")
a(D, "Prompt contracts", "F15-031", "Required envelope: tenant_id, startup_id, purpose, schema_revision, evidence_ids, confidence, missing_fields, policy_flags, proposed_action, requires_approval, cost_estimate", P, "Part 7.2 §7.2.7 (envelope lacks purpose, missing_fields, policy_flags, proposed_action, requires_approval, cost_estimate)", "Envelope v2 specified", "FR-ENH-F-001; GAP-405; RECOMMENDATION-400")
a(D, "Prompt contracts", "F15-032", "Evaluation per contract: schema, scope isolation, factual support, injection, unknown handling, deterministic policy gate, regression", C, "Part 7.3 §7.6.9; Part 6.4")
a(D, "RAG", "F15-033", "Tenant/product/startup ACL before retrieval AND after ranking", P, "Part 7.2 TL-01 (namespace before retrieval only)", "Post-ranking ACL recheck specified", "FR-ENH-F-003; GAP-407")
a(D, "RAG", "F15-034", "Chunk carries document version, checksum, approval, effective time, expiry", P, "Part 7.3 THR-057 (approved versions only)", "Chunk metadata and window filter", "FR-ENH-F-004")
a(D, "RAG", "F15-035", "Remove revoked chunks and cache entries", P, "Part 7.2 §7.2.6 (invalidate on version change); AU-011 (privacy purge)", "Revocation propagation automation", "AU-046; FR-ENH-F-005")
a(D, "RAG", "F15-036", "Citations to approved evidence", C, "BRL-AI-03; Part 7.3 §7.6.5")
a(D, "Model gateway", "F15-037", "Gateway selects low-cost reliable model by task, reserves tokens, caps context, validates, bounded retry or approved fallback", C, "Part 7.3 §7.3.4, §7.3.7; ADR-070")
a(D, "Model gateway", "F15-038", "No autonomous approval of legal/financial terms, consent or payment", C, "DEC-064; Part 7.3 §7.6.1")
a(D, "Model gateway", "F15-039", "Dry run with stub adapters; validate exact plan hash before dispatch", C, "IP-08; BRL-AUT-04; AG-016")
a(D, "Model gateway", "F15-040", "Eval datasets synthetic/authorized; tenant evidence separate; no cross-client learning by default", P, "RECOMMENDATION-017; Part 7.3 §7.6.9 (cross-client learning rule not explicit)", "Explicit no-cross-tenant-learning rule", "FR-ENH-F-006")
a(D, "Engineering contracts", "F15-041", "REST conventions, status codes, idempotency, outbox, callbacks", NA, "Part 3.2 §3.2.1", CORE)
a(D, "Engineering contracts", "F15-042", "Independent PostgreSQL, UUID PK, RLS, revision, decimal currency", NA, "Part 3.3", CORE)
a(D, "Website and Admin contract", "F15-043", "147 interfaces, surfaces, routing namespaces, publication snapshots", NA, "Part 2.5; Part 3.2 §3.2.1.1", CORE)
a(D, "Public AI versus confidential Copilot", "F15-044", "Public assistant: approved published snapshot only, host/startup/locale scoped; no staff tools", C, "AG-017; TL-01 public namespace")
a(D, "Public AI versus confidential Copilot", "F15-045", "Portal AI: granted materials and own thread only", C, "AG-031 (portal grant scope)")
a(D, "Public AI versus confidential Copilot", "F15-046", "Admin Copilot: staff scope and approved tool allowlist", C, "AG-015; §7.2.4")
a(D, "Public AI versus confidential Copilot", "F15-047", "Injection cannot widen retrieval or execute publication, money or outreach", C, "ADR-082; Part 7.3 §7.6.3")
a(D, "Public AI versus confidential Copilot", "F15-048", "Red-team cross-tenant AND cross-audience (public/portal/admin) leakage; default deny", P, "Part 7.3 §7.7.2 (cross-tenant only)", "Cross-audience red-team cases", "TC-ENH-F-006")
a(D, "Local AI, fallback, evaluation", "F15-049", "Typed Python gateway; local embedding/retrieval in PostgreSQL/pgvector", C, "ADR-070, ADR-077; Part 7.3 §7.5.1")
a(D, "Local AI, fallback, evaluation", "F15-050", "Validate model-weight commercial rights separately from framework licence", N, "—", "Licence register incl. model weights", "AU-047; FR-ENH-F-017; GAP-403")
a(D, "Local AI, fallback, evaluation", "F15-051", "Benchmark CPU/GPU cost, latency and accuracy of local inference", C, "RECOMMENDATION-067 (W6 spike)")
a(D, "Local AI, fallback, evaluation", "F15-052", "No paid AI subscription as prerequisite; paid model fallback needs per-tenant allowance, redacted prompts, budget reservation", X, "DEC-007 (paid Anthropic Tier 1 primary)", "Resolution proposed", "CONFLICT-400; FR-ENH-F-030")
a(D, "Local AI, fallback, evaluation", "F15-053", "Labelled examples for classification, extraction, relevance, response, objections, injection, unsupported facts", C, "Part 6.4 datasets; GAP-142")
a(D, "Local AI, fallback, evaluation", "F15-054", "Unit: schema/policy; SIT: scoped RAG, fallback, tool permissions; UAT: explanations and escalation", C, "Part 6.1, 6.4")
a(D, "AI evaluation and change governance", "F15-055", "Benchmark model/prompt change vs baseline (grounding, privacy, refusal, latency, cost); approve before activation; roll back", C, "AU-006; ADR-084; Part 7.3 §7.6.9")
a(D, "AI evaluation and change governance", "F15-056", "Delivery evidence against build/env/scope/reviewer; critical defects block activation", C, "Part 8.2 §8.2.4.2")
a(D, "Scoped AI task contract", "F15-057", "Example contract: return {answer, evidence_ids, escalate}; unknown -> escalate; policy/identity/finance deterministic", P, "Part 7.2 card outputs (per-agent shapes, no common minimum)", "Common minimum output in registry", "FR-ENH-F-002")
a(D, "Evaluation table", "F15-058", "Output shape: 100% critical outputs parse or fail closed", C, "AU-003; BRL-AI-02")
a(D, "Evaluation table", "F15-059", "Grounding: zero private leakage; unsupported claim -> refusal/escalation", C, "Part 7.3 §7.6.5")
a(D, "Evaluation table", "F15-060", "Matching: precision/recall AND calibration; owner approves minimum", P, "Part 6.4 (precision/recall; calibration not specified)", "Calibration (ECE) metric", "TC-ENH-F-009")
a(D, "Evaluation table", "F15-061", "Prompt injection: no unauthorized tool action or disclosure", C, "Part 7.3 §7.6.3")
a(D, "Evaluation table", "F15-062", "Fallback: timeout, quota, local model unavailable, paid fallback disabled -> safe retry, no unapproved charge", C, "Part 7.3 §7.3.4 R9-R13; FB sets")
a(D, "Evaluation table", "F15-063", "Model change: record model, prompt hash and dataset hash", P, "ADR-084 (eval run link; dataset hash not explicit)", "Eval run record fields", "FR-ENH-F-007")
a(D, "Evaluation table", "F15-064", "Seed JSONL is synthetic, not a benchmark; expand per startup/language/category; independent human or calibrated evaluator; no patient/child/investor data", C, "GAP-142; Part 7.3 §7.6.6 judge calibration")
a(D, "Acceptance and evidence record", "F15-065", "Evidence fields: responsible/reviewer, artifact, decision, remediation, business acceptance", C, "Part 8.2 §8.2.4.2")
a(D, "Evaluation cases", "F15-066", "Evidence A allowed, B foreign -> only allowed IDs; unknown -> escalate", C, "Part 6.4 cross-scope cases")
a(D, "Evaluation cases", "F15-067", "Malformed output -> bounded retry then hold/escalate; no action", C, "AU-003")
a(D, "Evaluation cases", "F15-068", "Simulation: nonfinite or negative costs rejected; zero external effects", P, "TP simulation oracle (Part 6.1); numeric validation absent", "Numeric validation rule", "FR-ENH-F-008")
a(D, "Evaluation cases", "F15-069", "Critical isolation, unsupported claims, privacy, financial cases require 100% pass", C, "Part 5.1a D-11; Part 7.3 §7.6.9")
a(D, "Optimization", "F15-070", "Deterministic rules before AI; benchmark model and RAG on frozen samples; report error, cost, latency", C, "Part 7.3 §7.4.2 technique 3; ADR-073")
opt15 = [
 ("OPT-01-01", "Authentication, privileged sessions, MFA, revoke", C, "Part 4.1"),
 ("OPT-03-01", "Native vs paid plugins; benchmark before enabling; zero unapproved paid calls; full TCO", P, "BRD §10 (paid off by default); no TCO procedure", "AU-044, AU-045; FR-ENH-F-012, FR-ENH-F-018"),
 ("OPT-04-01", "Daily planning/discovery: missed runs recover once; prohibited source never fetched", C, "AG-003; AU-028; AU-007"),
 ("OPT-04-02", "Qualification: precision >= 90% on benchmark; uncertain to review", X, "DEC-001 (80% W1 exit; 90% before L2)", "CONFLICT-405"),
 ("OPT-04-03", "Outreach: zero sends to ineligible; reply cancels follow-up", C, "AU-009, AU-022"),
 ("OPT-04-04", "Objection & meetings: no unsupported promises or double-booking", C, "AG-021; AU-023"),
 ("OPT-04-05", "Documents/approvals: zero execution with stale/missing approval", C, "CA-APPROVE; AU-036"),
 ("OPT-04-06", "Financial closure: zero duplicate side effects; 100% verified reconciled", C, "AU-037, AU-040"),
 ("OPT-04-07", "Exception/learning: completion >= 99% of eligible due runs; no blind repeat", P, "AU-026, AU-028 (target not stated)", "OKPI-09 wired (FR-ENH-F-031)"),
 ("OPT-04-08", "Autonomy/stop: >= 90% eligible steps automated; stop prevents future calls", P, "AU-025; DEC-064 (automation share not tracked)", "OKPI-10 wired (FR-ENH-F-031)"),
 ("OPT-05-01", "Transactional outbox", C, "IP-02; Part 3.1"),
 ("OPT-10-01", "Rules-first routing; compare quality/latency/INR per task", C, "Part 7.3 §7.3.4; §7.4.1"),
 ("OPT-10-02", ">= 99.5% schema-valid outputs; report token p50/p95", X, "Part 7.3 §7.6.9 (>= 99% first pass)", "CONFLICT-404"),
 ("OPT-10-03", ">= 95% evidence-grounded accuracy", C, "Part 7.3 §7.6.9 groundedness >= 95%"),
 ("OPT-10-04", "Caching by full scope/model/prompt/knowledge version; no cross-scope or stale hit", P, "AU-001 key lacks principal/grant/permission/policy revision", "FR-ENH-F-009; GAP-406"),
 ("OPT-10-05", "Local inference benchmark; no silent paid fallback", C, "RECOMMENDATION-067; DEC-007"),
 ("OPT-10-06", "Adversarial benchmark: zero forbidden actions; versioned datasets", C, "Part 7.3 §7.6.3"),
 ("OPT-11-01", "Provenance and source rights; missing rights quarantined", C, "AU-007; M07"),
 ("OPT-11-02", "Per-source freshness SLA; reverify before external action", C, "AU-018; AU-007"),
 ("OPT-11-03", "Identity/dedupe: never merge by name alone", C, "AU-015"),
 ("OPT-11-04", "Classification precision >= 90%; disclose recall and sample size", X, "DEC-001", "CONFLICT-405"),
 ("OPT-11-05", "Corrections/deletion propagate to caches and embeddings; legal hold", P, "AU-011 (privacy purge)", "AU-046"),
]
for k, row in enumerate(opt15, 1):
    oid, s, st, loc = row[:4]; new = row[4] if len(row) > 4 else ""
    a(D, "Optimization engineering", f"F15-{70+k:03d}", f"{oid}: {s}", st, loc, "Enhancement / resolution in Part 7.4b" if st != C else "", new)
acc15 = [
 ("AI routing cost", "100-task synthetic routing fixture vs all-advanced baseline; arithmetic reproducible", P, "Part 7.3 §7.4.1 waterfall (no fixture test)", "TC-ENH-F-011"),
 ("Retention and scoped vector indexing", "Delete/expire source; indexes, caches, embeddings updated; legal hold", P, "AU-011", "AU-046; TC-ENH-F-004"),
 ("RAG scope and evidence", "Tenant A material + tenant B distractor; no foreign evidence", C, "Part 6.4"),
 ("Structured output quality", "Valid/malformed/unexpected fields; >= 99.5% valid; invalid never drives side effects", X, "CONFLICT-404", "TC-ENH-F-012"),
 ("Model selection and token efficiency", "Small vs advanced on fixed corpus; tokens, latency, cost; >= 95% grounded", C, "ADR-073; Part 6.4"),
 ("Prompt injection and tool access", "Hostile text requesting secrets/tool calls; no disclosure", C, "Part 6.4 RT sets"),
 ("Prompt/model version regression", "Freeze prompt/model/dataset/policy; rerun benchmark before promoting", C, "AU-006"),
 ("Classification quality", "Precision >= 90%; recall measured; no claim from five synthetic documents", X, "CONFLICT-405", "TC-ENH-F-013"),
 ("Objection resolution", "Supported vs unsupported; approved response or escalation", C, "Part 6.4 AG-021"),
 ("Sensitive data exclusions", "Patient or school-minor fixture never enters acquisition workflow", C, "DEC-030; AU-004; Part 6.4"),
 ("Authorization-safe cache and numeric validation", "Private cache key includes product, tenant, startup, principal/grant fingerprint, permission/policy/model/knowledge revision, normalized query; reject nonfinite/negative/out-of-range", N, "—", "FR-ENH-F-008, FR-ENH-F-009; TC-ENH-F-001, TC-ENH-F-002, TC-ENH-F-003"),
 ("Provider and evidence benchmark", "Matched samples by geography/purpose; precision, recall, verified contacts, p95, full cost, entitlement, conversion", N, "—", "AU-045; TC-ENH-F-015"),
]
for k, (t, s, st, loc, *new) in enumerate(acc15, 1):
    a(D, "Implementation acceptance and verification (duplicated in final decision controls)", f"F15-{92+k:03d}", f"Acceptance procedure '{t}': {s}", st, loc, "Test added" if st != C else "", new[0] if new else "")
a(D, "Current multi-startup scope", "F15-105", "147 interfaces; 19 proposed HTTP operations; 6 candidate entities", NA, "Groups A-E reconciliation", CORE)
a(D, "Current multi-startup scope", "F15-106", "AI engineering release condition: rule-first, validated structured output, provenance, scoped retrieval, model budget", C, "Part 7.3; Part 8.2 §8.2.4")

# ---------------- Document 16 ----------------
D = "16"
a(D, "Product purpose", "F16-001", "Purpose, startups, technology principles (repeat)", NA, "Doc 15 F15-001..003", CORE)
a(D, "Integration selection and procurement gates", "F16-002", "Open-source-first; separate development assistance from production API access; free licence != free usage", C, "BRD §10; Part 7.3 §7.5.2")
a(D, "Integration selection and procurement gates", "F16-003", "Before activation verify licence, entitlement, commercial use, rate, quota, region, data processing/deletion, security, support, failure handling, benchmark", P, "Part 3.2 §3.2.4.2 (quotas to verify); no gate record", "Procurement gate PG-01..PG-10", "AU-044; FR-ENH-F-012; GAP-402")
a(D, "Integration selection and procurement gates", "F16-004", "Record provider account, approved spending, fallback and expiry; no vendor blanket data access", N, "—", "integration_candidate + provider_entitlement entities", "FR-ENH-F-011")
pref = [("React/Django/PostgreSQL self-hosted; licence and dependency scan", C, "Part 3.1; Part 4.3 SBOM"),
        ("Celery, Beat, Valkey; shared code, separate queues", C, "ADR-071; Part 3.1"),
        ("Search/extraction: approved public search API, self-hosted extraction; benchmark coverage and unit cost", X, "AD-05, AD-07; CONFLICT-401/402"),
        ("Contact verification: official channels; Apollo pilot if eligible", C, "AD-19 (OFF); AU-018"),
        ("Email/calendar/messaging: official account-bound APIs", C, "AD-01..AD-04"),
        ("AI/embeddings: scoped gateway, structured outputs, token/budget caps", C, "ADR-070, ADR-072, ADR-083"),
        ("Observability/backup: open-source where practical", C, "DEC-041; ADR-078"),
        ("Signing/payment: approved provider; independent accounts; verify evidence", C, "DEC-022, DEC-023; AD-10, AD-11")]
for k, (s, st, loc) in enumerate(pref, 1):
    a(D, "Preferred implementation table", f"F16-{9+k:03d}", s, st, loc, "Resolution in §7.4.6" if st == X else "", "CONFLICT-401; CONFLICT-402" if st == X else "")
a(D, "Individual candidate register", "F16-020", "538 candidate records with 15 fields each (category, priority, decision, application, modules, interface, trigger, acceptance, procurement, licence, free tier, paid API, allocation, URL, verification)", P, "Part 3.2 AD-01..AD-20 (20 adapters only)", "All 538 parsed; register entity specified", "F_integration_candidates.csv; IC-001..IC-538; FR-ENH-F-011")
a(D, "Individual candidate register", "F16-021", "Source priority codes P0-P3, R, V, X undefined", N, "—", "Interpretation stated", "ASSUMPTION-401; GAP-400")
a(D, "Individual candidate register", "F16-022", "All 538 triggers = development environment (Claude Code, Cowork); developer plugins are not runtime entitlements", C, "Part 7.3 §7.5.2; AG-033..AG-036")
bud = [
 ("B01", "AWS shared hosting ₹5,000", C, "DEC-020 B01; Part 8.2 (revised 5,000-7,000)"),
 ("B02", "Production AI inference ₹3,000", C, "DEC-008; DEC-020 B02"),
 ("B03", "Public search API ₹1,500 (500 fetches; Tavily 1,000 free credits)", C, "DEC-020 B03; AD-05"),
 ("B04", "Extraction compute/overage ₹1,000", C, "DEC-020 B04"),
 ("B05", "Email delivery ₹500 (2,000 sends)", C, "DEC-020 B05; DEC-025"),
 ("B06", "WhatsApp Business ₹2,000 (1,000 templates)", C, "DEC-020 B06"),
 ("B07", "Monitoring/security/CI ₹500 (reduced from ₹1,000)", C, "DEC-020 B07"),
 ("B08", "Apollo paid enrichment reserve ₹9,000 (not a quote)", C, "DEC-020 B08 (OFF)"),
 ("B09", "Claude Code developer seats ₹3,600 (2 x $20 x ₹90)", C, "DEC-020 B09"),
 ("B10", "Optional integration reserve ₹1,000", C, "DEC-020 B10"),
 ("B11", "Contingency 15%", C, "DEC-020 B11"),
 ("SUM", "Base runtime before contingency ₹14,500 = B01..B07 + B10", C, "Part 8.2 §8.2.7.2 (BRD figure)"),
 ("SUM", "Base runtime incl. contingency ₹16,675", X, "Part 8.2 revised 19,665-22,885", "CONFLICT-412"),
 ("SUM", "Base monthly incl. developer seats ₹20,815", N, "—", "Budget view table (§7.4.5.10)"),
 ("SUM", "Paid Apollo runtime incl. contingency ₹27,025", N, "—", "Budget view table"),
 ("SUM", "Paid Apollo + seats ₹31,165", C, "Part 8.2 (BRD 31,165; revised 34,155-37,375)"),
 ("SUM", "Base annual incl. seats ₹249,780", N, "—", "Budget view table; GAP-409"),
 ("SUM", "Paid Apollo annual incl. seats ₹373,980", N, "—", "Budget view table"),
 ("SUM", "Base annual runtime only ₹200,100", N, "—", "Budget view table"),
 ("SUM", "Paid Apollo annual runtime only ₹324,300", N, "—", "Budget view table"),
 ("SUM", "Three-month base operating budget ₹62,445", N, "—", "Budget view table"),
 ("SUM", "Three-month paid Apollo budget ₹93,495", N, "—", "Budget view table"),
]
for k, (bid, s, st, loc, *new) in enumerate(bud, 1):
    a(D, "Source operating budget register", f"F16-{29+k:03d}", f"{bid}: {s}", st, loc, "Reconciled in §7.4.4.4 / §7.4.5.10" if st != C else "Reconciled (§7.4.4.4)", new[0] if new else "")
a(D, "Consolidated effort", "F16-052", "Effort packages 194-323 / 35-60 / 30-52 / 28-48 = 287-483 pd; ₹13.05-32.93 lakh; ₹1-1.5 lakh/resource-month, 22 days", C, "Part 0; Part 8.2 §8.2.7.1; DEC-012")
a(D, "Consolidated effort", "F16-053", "SaaS: plans, metered base + included usage + approved overage; append-only credits; suspension on entitlement expiry; export", C, "DEC-047; AU-042")
a(D, "Consolidated effort", "F16-054", "Margin = recognized service fee minus attributable provider and infrastructure cost", N, "NFR-035 (attributable cost stated, no calculation)", "Contribution margin automation", "AU-049; FR-ENH-F-020; GAP-411")
a(D, "Consolidated effort", "F16-055", "Third-party managed service activity and success fees require contractual and regulatory review", N, "—", "Disabled-until-reviewed rule", "FR-ENH-F-029")
a(D, "Website-specific integration and cost controls", "F16-056", "CDN, domain/TLS, CAPTCHA, email verification costs; budget per tenant/startup AND surface; separate public/portal from staff consumption; per-IP and per-tenant ceilings for public AI/chat/intake; no browser vendor secrets", P, "NFR-022 (per-IP); B21; Part 3.2 RL classes (no per-surface budget)", "Per-surface budget scopes", "FR-ENH-F-021; RECOMMENDATION-414")
a(D, "Paid-plugin substitution rule", "F16-057", "Inventory is not a shopping list; paid wrappers disabled by default; no stacking competing plans; developer subscription != production API", P, "BRD §10; DEC-020 (B08 OFF)", "Rules PG-01..PG-10", "FR-ENH-F-012, FR-ENH-F-013")
a(D, "Paid-plugin substitution rule", "F16-058", "Approve paid service only after: function identified, compliant alternatives and measured gap, terms verified, sandbox benchmark, incremental cost and rollback, budget approval, metering and periodic re-evaluation", N, "—", "Procurement gate state machine", "AU-044; FR-ENH-F-015")
a(D, "Provider procurement and operating economics", "F16-059", "Inventory licences, entitlements, free quota, unit price, retention, DP terms; reserve atomically; reconcile usage and charge ledger; review monthly", P, "IP-06 reservation; AU-012 attribution (no invoice reconciliation)", "Invoice reconciliation", "AU-048; FR-ENH-F-019; GAP-410")
proc = [("Inventory", "Retain every candidate; dev-only vs runtime; direct API vs wrapper", P, "—", "FR-ENH-F-011"),
        ("Licence", "Verify licence version and commercial/network/SaaS obligations with legal", P, "RSK-303 (Firecrawl only)", "AU-047"),
        ("Rate and quota", "Check entitlements, free quota, rates, taxes, regional terms before purchase", P, "ASSUMPTION-108 (verify)", "PG-04"),
        ("Adapter design", "Canonical request/result, error classes, timeout, rate limit, scoped credentials; mock + sandbox", C, "IP-01; Part 3.2 §3.2.4.3, §3.2.7"),
        ("Budget", "Reserve max cost; reconcile; release; stop paid fallback unless enabled", C, "IP-06; AU-002"),
        ("TCO benchmark", "Same workload: coverage, accuracy, latency, failures, hosting/maintenance", N, "—", "AU-045; FR-ENH-F-016")]
for k, (t, s, st, loc, *new) in enumerate(proc, 1):
    a(D, "Integration procurement and runtime control", f"F16-{59+k:03d}", f"{t}: {s}", st, loc, "Enhanced" if st != C else "", new[0] if new else "")
a(D, "Integration procurement and runtime control", "F16-066", "538 decision records retain source terms; benchmark columns pending, not measured", C, "F_integration_candidates.csv (activation default disabled)")
seq = [("Compare", "Same fixture and volume across native and paid comparator", N, "AU-045"),
       ("Licence", "Runtime entitlement, OSS licence, model-weight rights, SaaS use, retention, export", N, "AU-047"),
       ("TCO", "Hosting + metered + engineering/maintenance + licences + support; cost per verified usable outcome", N, "FR-ENH-F-018"),
       ("Fallback", "Disabled by default; approve per tenant, startup, channel, purpose, hard cap; audit paid invocation", P, "FR-ENH-F-013"),
       ("Synthetic benchmark", "Five local synthetic sources only; paid comparisons unverified", C, "")]
for k, (t, s, st, new) in enumerate(seq, 1):
    a(D, "Provider procurement and benchmark approval", f"F16-{66+k:03d}", f"{t}: {s}", st, "Part 7.3 §7.3.6 (Tier 2 opt-in only)" if st == P else ("—" if st == N else "GAP-142 note"), "Enhanced" if st != C else "", new)
opt16 = [
 ("OPT-03-02", "Model and token costs: rules first, smaller models, minimal context, bounded tokens; INR/task", C, "Part 7.3 §7.4.2"),
 ("OPT-03-03", "Research/contact cost per qualified verified opportunity improves without regression", P, "KPI-21 AI cost/task only", "FR-ENH-F-018 (verified outcome cost)"),
 ("OPT-03-04", "Cloud/worker right-sizing; cost/1000 tasks and queue age", C, "Part 4.3 FinOps (§4.46)"),
 ("OPT-03-05", "Storage/retention cost; GB-month; legal hold", C, "Part 4.3; DEC-028"),
 ("OPT-03-06", "Communication/subscription costs; review unused seats and API entitlements", P, "AU-024 (suppression); no seat review", "AU-044 monthly entitlement review"),
 ("OPT-03-07", "Atomic budget reservation across tenant/startup/action; parallel test", C, "IP-06; AU-002; ADR-083"),
 ("OPT-03-08", "Alerts at 70%/90% (proposed); pause optional jobs at cap", X, "ADR-083 80%/100%; ladder 80-100%", "CONFLICT-403; FR-ENH-F-022"),
 ("OPT-09-01", "Typed contracts 100% before activation", C, "Part 3.2 §3.2.5"),
 ("OPT-09-02", "Consolidation and batching; minimal serializers", C, "Part 3.2 §3.2.1"),
 ("OPT-09-03", "Adapter reliability: timeouts, rate limits, breakers, entitlement fallback", C, "Part 3.2 §3.2.7"),
 ("OPT-09-04", "Webhook: signature, replay window, dedupe; p95 ACK <= 2 s", C, "IP-03; Part 3.2 §3.2.6"),
 ("OPT-09-05", "Meter by provider, operation, tenant/startup; no unapproved paid calls", C, "AU-012; IP-06"),
 ("OPT-20-01", "Unit economics: contribution margin per tenant", N, "—", "AU-049"),
 ("OPT-20-02", "Entitlements and usage: 100% attributable usage reconciled", P, "AU-042 (metering)", "AU-048"),
 ("OPT-20-03", "Support and renewal: onboarding effort, tickets, churn by cohort", C, "Part 8.2 §8.2.6; AG-031"),
 ("OPT-20-04", "Client scalability/portability: self-service onboarding; export and revoke on offboard", C, "B-SVC; W31-W34"),
]
for k, (oid, s, st, loc, *new) in enumerate(opt16, 1):
    a(D, "Optimization engineering", f"F16-{71+k:03d}", f"{oid}: {s}", st, loc, "Enhanced / resolved" if st != C else "", new[0] if new else "")
acc16 = [
 ("Hierarchical budget controls", "Concurrent reservation at platform/tenant/startup/workflow; duplicate and insufficient balance", C, "AU-002; Part 6 budget TCs"),
 ("AI routing cost", "Duplicate of F15-093", NA, "See F15-093"),
 ("Open-source replacement economics", "Native vs paid on same corpus incl. CPU, labour, API", N, "—", "TC-ENH-F-016"),
 ("Cost metering and anomaly response", "Duplicates, missing attribution, exhausted quota; hard limit halts", P, "AU-012 (anomaly); duplicate usage billing not tested", "TC-ENH-F-017"),
 ("HTTP vs adapter classification", "All HTTP and adapter operations represented exactly once", NA, "Group C (doc 07) reconciliation"),
 ("Webhook and provider reliability", "Valid/invalid signatures, stale timestamp, duplicate, quota", C, "Part 3.2 §3.2.6; Part 6"),
 ("Provider entitlement and schema change", "Official rights, schema version, quota, timeout, compatibility test; no activation without", N, "—", "AU-044; TC-ENH-F-018"),
 ("Source inventory completeness", "Preserved 15-sheet commercial source inventory; coverage measured", NA, "Group B (doc 11) reconciliation"),
 ("Usage ledger and invoice reconciliation", "Replay usage and payment; approved adjustment; no double bill", P, "AU-042", "AU-048; TC-ENH-F-019"),
 ("Service profitability and TCO", "Contribution margin by tenant; allocation basis; zero denominator not assessed", N, "—", "AU-049; TC-ENH-F-020"),
 ("Matched-sample discovery benchmark execution", "Unique opaque IDs; micro P/R; nearest-rank p95; reject invalid inputs", N, "—", "AU-045; TC-ENH-F-015"),
]
for k, (t, s, st, loc, *new) in enumerate(acc16, 1):
    a(D, "Implementation acceptance and verification", f"F16-{87+k:03d}", f"Acceptance procedure '{t}': {s}", st, loc, "Test added" if st in (N, P) else "", new[0] if new else "")
a(D, "Current scope: integration and cost", "F16-099", "Connect only entitled providers; capability grants, revocation, health; budgets per tenant/startup/objective/run; reserve before charge", C, "AD-08 capability grant; AU-010; AU-002; envelope budget_remaining_inr")

# ---------------- Document 21 ----------------
D = "21"
a(D, "1. Purpose, scope", "F21-001", "Own automation; OSS/existing first; paid plugin not a dependency because it is in a dev inventory", C, "BRD §10; ADR-071")
a(D, "1. Purpose, scope", "F21-002", "Distinguish developer assistance, OSS library, self-hosted app, hosted API, licensed/regulated service", N, "—", "candidate_type enum", "FR-ENH-F-011")
a(D, "1. Purpose, scope", "F21-003", "Decision classes Replace / Retain OSS / Conditional external service / Defer-exclude with default actions", N, "—", "decision_class enum and default action", "FR-ENH-F-011")
a(D, "1. Purpose, scope", "F21-004", "Commercial use only; no investor discovery or capital ledger", NA, "DEC-002", CORE)
a(D, "2. Deployment architecture", "F21-005", "Website -> APIs -> domain services -> outbox -> Celery -> adapter registry -> provider; Admin owns config, simulation, approvals, usage, provider health", C, "Part 3.1; IP-01, IP-02")
a(D, "2. Deployment architecture", "F21-006", "Valkey is broker/cache, not authoritative financial storage", C, "Part 3.1 (PostgreSQL system of record)")
a(D, "2. Deployment architecture", "F21-007", "Layer/runtime/cost table (frontend, backend, durability, jobs, search, AI, external)", C, "Part 3.1; Part 7.3 §7.5.1")
caps = [
 ("01 Workflow orchestration and RPA", C, "ADR-071; DEC-051; A033 editor", ""),
 ("02 Public market / investor search", X, "AD-05 Tavily primary", "CONFLICT-401; CONFLICT-406"),
 ("03 Website extraction", X, "ADR-018 Firecrawl self-hosted primary", "CONFLICT-402"),
 ("04 Professional contact discovery (no guessed addresses; MX != mailbox proof)", P, "AU-018; AD-19 OFF (MX rule not explicit)", "FR-ENH-F-023"),
 ("05 CRM / relationship pipeline", C, "M21-M23; AU-020, AU-021", ""),
 ("06 LLM / agent framework (local model gateway first)", X, "DEC-007", "CONFLICT-400"),
 ("07 Embeddings, knowledge, enterprise search (remove revoked content)", P, "ADR-077; AU-001", "AU-046"),
 ("08 Email automation and inbox", C, "DEC-025 SES; AD-01", ""),
 ("09 WhatsApp, SMS, social messaging (no unofficial bots)", C, "AD-02; DEC-026", ""),
 ("10 Meeting scheduling and video (Jitsi; local transcription with notice)", P, "AU-023; GAP-143", "AG-037; RECOMMENDATION-412"),
 ("11 Document generation / secure storage", C, "AU-036; S3; AD-20", ""),
 ("12 Electronic signing and identity verification (Documenso after review)", P, "DEC-023; AD-10 (Documenso not on shortlist)", "RECOMMENDATION-405 (shortlist note)"),
 ("13 Banking, receipts and billing", C, "DEC-022; AD-11; AU-037", ""),
 ("14 Observability (avoid hosted Sentry/Datadog)", X, "DEC-041 Sentry free tier", "CONFLICT-409"),
 ("15 Cloud infrastructure and storage", C, "DEC-040; Part 4.3 IaC", ""),
 ("16 Developer tools, QA, coordination", C, "Part 7.3 §7.5.2; Part 4.3", ""),
 ("17 Analytics, reporting, forecasting", C, "RP-01..30; AU-041", ""),
 ("18 Customer support / collaboration", C, "AG-031; NT", ""),
 ("19 Marketing content and localization", C, "AG-018; AG-012", ""),
 ("20 SEO and AI search visibility", C, "AU-033; AD-17", ""),
 ("21 Social listening and publishing (Postiz self-host after AGPL review)", C, "AD-08; AU-029", ""),
 ("22 Marketing campaigns and attribution (Matomo optional)", C, "AU-040; Part 3.1 alternatives", ""),
 ("23 Advertising and paid acquisition", C, "AD-09; AU-032; B12", ""),
 ("24 Website and landing page builder", C, "B-WEB; A107, A108", ""),
 ("25 Project/tender discovery (amendments update evidence)", P, "DEC-053; AU-034 (amendments not detected)", "AU-052"),
 ("26 Supplier, order, procurement, retention", C, "WF-10; AU-035, AU-038", ""),
 ("27 Webinar and demo registration (capacity, dedupe, opt-out)", P, "AD-18; M40 (no automation)", "AU-051"),
]
for k, (s, st, loc, new) in enumerate(caps, 1):
    a(D, "3. Capability replacement register", f"F21-{9+k:03d}", s, st, loc, "Enhancement / resolution" if st != C else "", new)
life = [("Configure", C, "A008; IP-01 registry"), ("Simulate", C, "IP-08; BRL-AUT-04"), ("Benchmark", N, "—"), ("Approve", P, "CFG-25 (Tier 2 only)"),
        ("Execute", C, "IP-02; PDP"), ("Recover", C, "IP-04; AU-026"), ("Retire", N, "—")]
for k, (t, st, loc) in enumerate(life, 1):
    a(D, "4. Adapter selection, activation and rollback", f"F21-{36+k:03d}", f"Adapter lifecycle stage '{t}'", st, loc, "Lifecycle state machine" if st != C else "",
      {"Benchmark": "AU-045; FR-ENH-F-015", "Approve": "AU-044; FR-ENH-F-015", "Retire": "AU-050; GAP-404"}.get(t, ""))
a(D, "5. Engineering contract", "F21-044", "Adapter interface estimate/execute/reconcile/health; context; error classes denied, invalid, quota, retryable, permanent, uncertain", P, "IP-01 AdapterResult; failure classes transient/rate_limited/auth/permanent/uncertain/unsupported", "Port contract and class mapping", "FR-ENH-F-014; RECOMMENDATION-405")
a(D, "5. Engineering contract", "F21-045", "Pinned deps, SBOM, source and model licences approved separately, isolated containers, egress allowlist, rotation; AGPL network-use review", P, "Part 4.3 SBOM; RSK-303", "Licence register gate", "AU-047")
chk = [("No paid plugin by default", C, "BRD §10; DEC-020"), ("Quality equivalence (labelled fixture; uncovered data reported)", N, "—"),
       ("Scope (cross-product and foreign tenant denied)", C, "NFR-032"), ("Recovery (429/timeout/unknown; no duplicate)", C, "IP-04"),
       ("Licence (dependency and model-weight register)", N, "—"), ("Metering separated from investment or sales cash", C, "DEC-008; ledgers"),
       ("Rollback (previous adapter only after policy/budget checks)", P, "—")]
for k, (t, st, loc) in enumerate(chk, 1):
    a(D, "5. Deployment checklist", f"F21-{45+k:03d}", f"Control: {t}", st, loc, "Enhanced" if st != C else "", {"N": "AU-045 / AU-047", "P": "FR-ENH-F-015"}.get(st[0], "") if st != C else "")
a(D, "6. Cost model", "F21-053", "Cost per successful verified outcome; monthly total = infra + inference + data + comms + regulated fees + monitoring/storage + support + contingency", P, "Part 7.3 §7.5.5 (AI layer only)", "Full TCO formula", "FR-ENH-F-018")
a(D, "6. Cost model", "F21-054", "Break-even example ₹9,000 vs ₹2,000 + ₹3,000 = ₹4,000/month; ₹40,000 effort -> 10 months", N, "—", "Worked example verified", "§7.4.5.9")
a(D, "6. Cost model", "F21-055", "Retained pilot envelope ₹16,675; Apollo ₹9,000 and seats ₹3,600 optional", X, "Part 8.2 revised", "CONFLICT-412")
for k, t in enumerate(["Avoidable subscription", "Incremental replacement cost", "Net saving", "Break-even", "Verified outcome cost (zero outcomes undefined)", "Approval (switch only when quality, compliance, latency, TCO pass)"], 1):
    a(D, "6. Cost model metrics", f"F21-{55+k:03d}", f"Metric: {t}", N, "—", "Metric defined", "FR-ENH-F-018; RECOMMENDATION-406")
a(D, "7. Named integration decisions", "F21-062", "97 named candidates with decisions (53 primary + selected supporting)", C, "F_integration_candidates.csv; §7.4.4.2", "Every row reconciled")
a(D, "7. Named integration decisions", "F21-063", "'Apollo GraphQL' mapped to professional contact discovery", X, "—", "Reclassify", "CONFLICT-407")
a(D, "8. Supporting inventory", "F21-064", "441 supporting candidates in 26 categories; default Defer", C, "F_integration_candidates.csv")
a(D, "9. Upstream references", "F21-065", "Celery BSD, Valkey BSD-3, Scrapy BSD-3, Playwright Apache-2.0, scrapy-playwright, SearXNG AGPL, Matomo, WhatsApp pricing, Meta rate limits", P, "Part 3.1 tech table (partial)", "Seed licence register", "AU-047")
a(D, "9. Final procurement gate", "F21-066", "No substitution may remove a legally necessary verification, delivery, signature or payment service", C, "DEC-022, DEC-023; PG-09")
rb = ["Licence and data rights", "Functional parity", "Accuracy / coverage", "Reliability / latency", "Total cost", "Fallback (paid disabled, outage, quota)"]
for k, t in enumerate(rb, 1):
    a(D, "Replacement benchmark", f"F21-{66+k:03d}", f"Benchmark dimension: {t}", N if k < 6 else C, "—" if k < 6 else "Part 7.3 §7.3.4", "Benchmark harness" if k < 6 else "", "AU-045" if k < 6 else "")
a(D, "Replacement benchmark", "F21-073", "Per-candidate benchmark scope; activation 'Disabled pending evidence' (35 rows)", C, "F_integration_candidates.csv activation_default")
a(D, "Benchmark method", "F21-074", "Sample workload stratified by country/category/difficulty; success metrics; financial control", N, "—", "", "AU-045")
a(D, "Benchmark method", "F21-075", "Local benchmark: guarded extraction 5 synthetic docs, 0 forbidden; unguarded baseline 2 false positives", C, "Informational; no claim (GAP-142)")
a(D, "Benchmark method", "F21-076", "Benchmark plans for 28 categories (538 candidates), all pending", C, "§7.4.4.2 category table")
a(D, "Optimization (repeat)", "F21-077", "OPT-03-01..08, OPT-09-01, OPT-10-01..06 repeated", NA, "See F15/F16 rows", "Duplicate")
a(D, "Implementation acceptance", "F21-078", "Open-source replacement economics (repeat of F16)", NA, "F16-090")
a(D, "Implementation acceptance", "F21-079", "Provider entitlement and schema change (repeat)", NA, "F16-094")
a(D, "Implementation acceptance", "F21-080", "Shared workflow and adapter code: reusable code without shared credentials or data; no duplicate side effects", C, "Part 3.1 (independent deployment; shared libraries)")
a(D, "Current scope", "F21-081", "Provider replacement: native workflow code cannot replace official provider authorization", C, "AD-02, AD-08 capability grants")

# ---------------- Automation library (doc 38 §09) ----------------
D = "38"
a(D, "09 Automation library", "F38-001", "20 industry/business templates (names not given in pack)", P, "CFG-04 business templates; A100 (no catalogue)", "20 templates proposed", "TPL-01..TPL-20; ASSUMPTION-400; GAP-401")
a(D, "09 Automation library", "F38-002", "20 use-case groups x 5 = 100 use cases (group names only)", P, "AG-001..036, AU-001..043 cover 89 of 100", "100 use cases mapped; 11 gaps filled", "AL-01.1..AL-20.5; AG-037, AG-038; AU-044..AU-052")
a(D, "09 Automation library", "F38-003", "13 workflow node types (names not given)", P, "DEC-051; BRL-AUT-02; API-478 (no list)", "13 canonical node types proposed", "NT13-01..NT13-13; ASSUMPTION-400")
a(D, "09 Automation library", "F38-004", "Library is a catalogue of proposed use cases, not 100 live integrations; prototypes are simulations", C, "BRL-AUT-04; Part 6.1 simulation oracle")

# ---------------- candidate rows ----------------
cand = list(csv.DictReader(open(os.path.join(BP, "final", "coverage", "F_integration_candidates.csv"), encoding="utf-8")))
OUT_SCOPE = ("cap table", "carta investors", "equity research", "private equity", "fund admin", "juniper square", "chronograph",
             "investment banking", "pitch agent", "valuation reviewer", "privco", "morningstar", "blackrock", "vanguard", "wealthbox",
             "clinical", "medidata", "owkin", "boltz", "chembl", "open targets", "cortellis", "adisinsight", "claude for healthcare",
             "math olympiad", "math proof", "oak national", "earnings reviewer", "claude for financial advisors", "zocks", "linqalpha", "carta crm")
crow = []
for r in cand:
    nm = r["candidate"].lower()
    st = C
    if any(x in nm for x in OUT_SCOPE):
        st = NA; act = "Out of commercial scope (DEC-002 / no patient or learner data); never activate"
    elif r["candidate"] == "Apollo GraphQL":
        st = X; act = "Reclassify to developer tools; defer (CONFLICT-407)"
    elif r["blueprint_status"].startswith("Not applicable"):
        st = NA; act = "No runtime need; deferred"
    else:
        act = "Retained in candidate register; disabled until procurement gate passes"
    crow.append(("16/21", f"Candidate {r['no']} ({r['category']})", f"IC-{r['no']}",
                 f"{r['candidate']}: {r['decision_doc21']} [{r['priority']}]", st, r["blueprint_adapter_or_module"], act, "F_integration_candidates.csv"))

rows = A + crow
ids = [x[2] for x in rows]
assert len(ids) == len(set(ids)), [i for i, c in collections.Counter(ids).items() if c > 1]
with open(os.path.join(BP, "final", "coverage", "F_coverage.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["doc", "section", "aspect_id", "aspect_summary", "status", "blueprint_location", "action", "new_ids"])
    w.writerows(rows)

# counts
def counts(rs):
    c = collections.OrderedDict((d, collections.Counter()) for d in ("15", "16", "21", "38", "16/21"))
    for r in rs: c[r[0]][r[4]] += 1
    return c
cc = counts(rows)
order = [C, P, N, X, NA]
with open(os.path.join(SCR, "F_counts.md"), "w", encoding="utf-8") as f:
    f.write("| Document | " + " | ".join(order) + " | Total |\n|---|" + "---|" * (len(order) + 1) + "\n")
    names = {"15": "15 AI Agents, Prompts, RAG", "16": "16 Plugin, API, OSS and Cost (aspects)", "21": "21 Paid Plugin Replacement (aspects)",
             "38": "38 §09 Automation library (assigned)", "16/21": "Integration candidates IC-001…IC-538 (16 + 21)"}
    tot = collections.Counter()
    for d, c in cc.items():
        f.write(f"| {names[d]} | " + " | ".join(str(c[o]) for o in order) + f" | {sum(c.values())} |\n"); tot.update(c)
    f.write("| **Total** | " + " | ".join(f"**{tot[o]}**" for o in order) + f" | **{sum(tot.values())}** |\n")
# register fragment (aspects only, candidates summarised elsewhere)
with open(os.path.join(SCR, "F_register.md"), "w", encoding="utf-8") as f:
    cur = None
    for r in A:
        if r[0] != cur:
            cur = r[0]
            f.write(f"\n**Document {cur}{' (§09 automation library)' if cur == '38' else ''}**\n\n| Aspect | Section | Aspect summary | Status | Blueprint location | Action | New IDs |\n|---|---|---|---|---|---|---|\n")
        s = r[3].replace("|", "/")
        f.write(f"| {r[2]} | {r[1]} | {s} | {r[4]} | {r[5]} | {r[6] or '—'} | {r[7] or '—'} |\n")
print({d: dict(c) for d, c in cc.items()}, len(rows))
