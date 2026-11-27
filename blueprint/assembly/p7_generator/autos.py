"""Deterministic automations (AU). No LLM calls. Cost = compute on existing B01 infrastructure unless stated."""
U = []
def au(i, name, wave, links, trigger, logic, outputs, guard, failure, kpi, autonomy="L3 (deterministic, within policy)", cost="₹0 incremental (Celery/PostgreSQL on B01)"):
    U.append(dict(id=f"AU-{i:03d}", name=name, wave=wave, links=links, trigger=trigger, logic=logic,
                  outputs=outputs, guard=guard, failure=failure, kpi=kpi, autonomy=autonomy, cost=cost))

au(1, "Model gateway router, Tier 0 cache & template responder", "W0", "BR-M08; FR-OP001; DEC-007; BRL-AI-01; ADR-070, ADR-076",
   "Every AI request", "Routing decision table (§7.3.4); exact-match cache key = hash(agent, prompt version, model, normalized input, scope); semantic cache (pgvector cosine ≥ 0.92, same tenant/startup namespace, Public/Internal only); approved template responses",
   "Model call or cached/template result with route record", "No direct provider calls outside the gateway (BRL-AI-01); cache entries scoped and invalidated on knowledge/prompt version change",
   "Gateway down → callers receive Tier 3 status; queued work retained", "Cache hit rate ≥ 30% (target by agent); p95 gateway overhead ≤ 50 ms")
au(2, "Budget reservation, alerts & hard stop", "W0", "BR-M53; BRL-AI-08; NT-025; NFR-014; ADR-083",
   "Before every paid call; on reconciliation", "Reserve estimated ₹ (max_tokens × output price + input estimate) against agent, startup, tenant and global budgets; reconcile actual usage; 80% alert, 100% hard stop; founder top-up audited",
   "Reservation ID or denial with reason", "Fail closed: ledger unavailable → deny paid calls", "Paid calls queue (Tier 3) until budget resets", "0 overspend beyond cap; simulated cap stops requests (NFR-014)")
au(3, "Output schema validation & repair controller", "W0", "BRL-AI-02; CA-AI; ADR-072",
   "Every model response", "Validate JSON against versioned schema; up to 2 repair retries with the validation error; then route per §7.3.4 (Tier 2 only if data class allows) else Tier 3",
   "Valid object or failure record", "Invalid output never reaches business state", "Tier 3 human task", "Schema failure rate ≤ 1% per agent")
au(4, "Data classification & PII redaction", "W0", "BRL-AI-06; ABAC-05; SC-35; ADR-080; Part 4.1 §4.1.2",
   "Before prompt assembly and before any Tier 2 call", "Field-level classification from the data dictionary + Presidio analyzers (email, phone, Aadhaar/PAN patterns, names, health terms) with Indian recognizers; mask/pseudonymize; block Tier 2 if Restricted/Confidential remains",
   "Redacted prompt + classification label", "Highest class governs (fail closed)", "Redactor error → block Tier 2 and log; Tier 1 continues with minimized fields", "0 Restricted items reach Tier 2 (NFR-077 test); redaction recall ≥ 98% on fixture set")
au(5, "Untrusted-content sanitizer & injection pre-filter", "W0", "BR-M12; THR-051; SC-32",
   "Before any untrusted text (web page, inbound, upload) enters a prompt", "HTML-to-text cleaning, hidden-text removal, length caps, delimiter wrapping with provenance, injection heuristics (instruction verbs aimed at the model, tool-call syntax, canary probes) flagging `injection_suspected`",
   "Sanitized wrapped content + flags", "Flags never grant tools; suspected items forced to L1", "On error, content is excluded (fail closed)", "Injection corpus (≥ 200 cases) pass ≥ 98%")
au(6, "Eval regression CI gate", "W0", "BR-M54; NFR-033; DEC-061; BRL-AI-09; ADR-079",
   "Prompt, model, schema or routing change (PR)", "Run promptfoo/DeepEval suites per agent (deterministic graders + AG-002 judge); compare to thresholds in §7.6.9; block merge on failure",
   "Gate pass/fail with report", "Thresholds changed only via reviewed PR (R11 + AI lead)", "Judge unavailable → generative changes blocked", "100% of AI changes gated")
au(7, "Source permission & expiry enforcer", "W0", "BR-M07; NT-003",
   "Before every search/fetch; daily expiry scan", "Check purpose, licence, robots/terms flag, quotas and expiry per source; stop collection on expiry (M07 trigger)",
   "Allow/deny with rule ID", "Unknown source = deny", "Deny and alert R04/R10", "0 fetches from unapproved sources")
au(8, "STOP / opt-out handler & queued-send cancellation", "W0", "BR-M04; BRL-ELG; NT-008",
   "Inbound message, unsubscribe link, preference change", "Multilingual STOP lexicon, List-Unsubscribe, WhatsApp opt-out; suppression write; cancel queued sends in scope atomically",
   "Suppression record; cancelled outbox items", "Ambiguous opt-out treated as opt-out", "Retry; if cancellation uncertain, pause scope", "STOP recall 100%; cancellation ≤ 60 s")
au(9, "Policy Decision Point dispatch guard", "W0", "RECOMMENDATION-012; DEC-048; CA-DISPATCH; ADR-082",
   "Every external side effect, including any agent-originated item", "Recheck scope, role, consent, jurisdiction, quiet hours, caps, entitlement, budget reservation and approved hash at dispatch",
   "Allow/deny with rule IDs (audited)", "Agents never hold dispatch tools; only the engine calls the PDP", "Deny (fail closed)", "0 dispatches without PDP allow")
au(10, "Provider health checks & circuit breakers", "W0", "BR-M05, BR-M58; NT-033; §7.3.7",
   "Every 60 s per provider; on errors", "Synthetic health probe; error-rate/latency windows; open circuit after 5 consecutive failures or 50% errors in 60 s; half-open probe after 30 s",
   "Provider state open/half-open/closed", "Open circuit triggers routing to next tier", "Alert R11", "Fallback switch ≤ 60 s after outage onset")
au(11, "Privacy request locator & retention purge", "W0", "BR-M56; DEC-028",
   "Privacy request; nightly retention job", "Identifier search across tables incl. AI run logs and caches; purge AI payloads after 90 days; keep digests; legal hold respected",
   "Fulfilment report", "Suppression record never deleted", "Retry; escalate to R10 at 70% of deadline", "100% requests within legal deadline")
au(12, "FinOps cost attribution & anomaly alerts", "W0", "FR-A012; RP-20, RP-21; KPI-21, KPI-22",
   "Every reconciled call; hourly roll-up", "Cost per task/agent/startup/tenant/provider; z-score and >150% of 7-day baseline alerts; KPI anomaly thresholds",
   "Dashboards A012/RP-21; alerts", "Read-only", "Alert on missing data", "Cost visibility ≤ 1 h lag")
au(13, "Release pipeline gates", "W0", "BR-M09, BR-M62; NFR-012, NFR-013",
   "Every PR/release", "Secret scan, SAST, dependency update bot (Renovate-style), licence check, ID/trace lint, restore drill schedule, smoke test",
   "Gate results", "Protected branches", "Block release", "100% releases with complete evidence")
au(14, "URL normalization, blocked-host & duplicate-content filter", "W1", "BR-M11",
   "Search results", "Canonicalize URLs, strip tracking, reject blocked hosts, content-hash dedupe (saves AG-004 calls)", "Fetch queue", "Blocked hosts never fetched", "Skip and log", "Duplicate fetch rate ≤ 5%")
au(15, "Organization canonical upsert & safe merge", "W1", "BR-M13",
   "Evidence created", "Match by domain + location + alias; conflicting attributes → merge task", "Organization record / merge task", "No automatic merge across startups or tenants", "Merge task to R04", "Duplicate organizations ≤ 2%")
au(16, "Readiness-gated solution match ranking", "W1", "BR-M16; BRL-SCR-04; ADR-077",
   "Need created/changed; offering version change", "pgvector similarity between need and approved capability chunks + rule filters (readiness Approved and Available, geography, capability profile)",
   "Ranked matches with exclusion reasons", "Unavailable offerings excluded", "Ranking unavailable → match pending", "Top-3 contains reviewer-chosen offering ≥ 85%")
au(17, "Opportunity scoring", "W1", "BR-M17; DEC-011; BRL-SCR-01…09",
   "Match/evidence change", "score = round(100 × Σ wᵢcᵢ / Σ w_known); Unknown if known weight < 0.60; bands", "Score version", "Score never grants contact permission", "Recalculate on retry", "100% recalculation on trigger events")
au(18, "Contact verification & freshness expiry", "W1", "BR-M19",
   "Contact created; expiry date", "Provenance check (published on official page), channel syntax/MX check, freshness expiry and recheck", "Verification status", "Verified ≠ consent", "Mark unverified", "Verified contact rate tracked (KPI-03)")
au(19, "Research review assignment & alerts", "W1", "BR-M20; NT-001",
   "Opportunity ready for review", "Round-robin/owner rules; SLA timers", "Assignment, notifications", "Rejected leads never sent to channel", "Escalate per SLA", "Owner action ≤ 2 business days")
au(20, "Lead dedupe, consent capture & form routing", "W2", "BR-M22; DEC-030; CA-INTAKE",
   "Form submission", "Idempotency key; dedupe; consent with policy revision; route by typed fields; age band < 18 → guardian/institution path with no minor data beyond grade band",
   "Lead + routing", "No direct approval from public intake", "Queue on failure", "One lead per duplicate submission")
au(21, "Customer 360 projection", "W2", "BR-M23; NFR-008", "Domain events", "Event-sourced projection", "Account view", "RLS", "Rebuild from events", "Visible ≤ 60 s")
au(22, "Sequence scheduler with stop-on-reply", "W2", "BR-M28; BRL-SEQ", "Schedule tick; reply/opt-out events",
   "Eligibility recheck, quiet hours, caps; stop on any substantive reply (AG-013) or STOP (AU-008)", "Due steps to outbox", "No follow-up after reply/stop", "Pause enrolment", "0 follow-ups after reply")
au(23, "Meeting slot offer & booking conflict check", "W2", "BR-M29; DEC-024", "Positive intent with proposed times (AG-013)",
   "Free/busy query, buffers, time-zone conversion, hold-and-confirm", "Slot offer / booking", "No invented availability", "Manual scheduling task", "0 double bookings")
au(24, "Bounce/complaint suppression", "W2", "BR-M26; DEC-025", "SES SNS webhooks", "Hard bounce/complaint → suppression; soft bounce counters", "Suppression", "Signature verified", "Retry webhook processing", "Complaint rate < 0.1% (KPI-18)")
au(25, "Emergency stop & runaway guard", "W2", "BRL-AUT-05, BRL-AUT-06; NT-032; ADR-085", "Operator stop; cap breach",
   "Kill switch at platform/tenant/startup/workflow/agent/tier/channel scope; caps on steps, retries, concurrency, actions per relationship, LLM calls and tokens per run",
   "Blocked calls/runs with reason", "Effective ≤ 60 s", "Fail closed", "Stop effective ≤ 60 s in drills")
au(26, "Uncertain-outcome reconciliation", "W2", "RECOMMENDATION-015; FR-STD-02; DEC-050", "Provider timeout after submission",
   "Query provider by reference; mark reconciled_confirmed/failed; block retry until reconciled", "Reconciled outcome", "No blind retries", "Human task after 3 attempts", "Uncertain items reconciled ≤ 1 business day")
au(27, "Notification digest & approval SLA escalation", "W2", "DEC-036; NT-009", "Notification events; SLA timers", "Severity routing, digests, escalation ladders", "In-app/email notifications", "Dedup keys", "Retry delivery", "Approval SLA breach alerts 100%")
au(28, "Missed-schedule recovery", "W2", "BRL-AUT-10; OPT-04-01", "Scheduler start / missed run detection", "Recover once; further misses alert", "Recovered run", "No duplicate side effects (idempotency)", "Alert R11", "≥ 99% scheduled runs within window (DEC-032)")
au(29, "Publication pipeline & expiry monitor", "W2", "FR-PUB-01; NT-036, NT-037", "Approve/publish/rollback; daily expiry scan",
   "Approved-hash check, atomic pointer swap, tenant-keyed cache invalidation; claim/knowledge expiry notifications", "Published snapshot; alerts", "Only approved hash publishes", "Rollback", "0 unapproved publications")
au(30, "Automation conflict resolution by priority rules", "W3", "FR-A111; BRL-AUT-09", "Two runs target the same relationship",
   "Hold both; priority compliance > transactional > sales > marketing; merge or escalate", "ConflictCase decision", "No cross-tenant context", "Escalate to owner", "0 duplicate contacts from conflicting runs")
au(31, "Compliance auto-pause on complaint threshold", "W3", "BR-M57; NT-027", "Complaint events", "Threshold per channel/campaign → pause + incident", "Paused campaign, incident", "Resume needs R10", "Pause anyway on error", "Pause ≤ 5 min after threshold")
au(32, "Ad spend cap & anomaly pause", "W3", "BR-M39; BRL-MKT-05; NT-026", "Spend events", "Cap check and >150% anomaly → pause via provider API", "Paused ad set", "Spend within approved cap only", "Pause on uncertainty", "0 spend beyond cap")
au(33, "SEO technical audit", "W3", "BR-M36", "Weekly", "Crawl checks (status, canonical, sitemap, metadata length), Search Console metrics from authorized source", "Prioritized fix list (A055)", "No fabricated ranking data", "Skip run", "Audit weekly 100%")
au(34, "Bid deadline & mandatory-checklist tracker", "W4", "BRL-BID; NT-020, NT-021; DEC-053", "Bid created; timers", "Deadline countdown (UTC, FR-DM-02), checklist completeness gate before human submission", "Alerts, gate", "Submission at/after deadline rejected", "Escalate", "100% on-time submissions for approved bids")
au(35, "Quote calculator, invoice generation & approval routing", "W4", "BR-M44; DEC-027, DEC-038; FR-DM-01", "Quote/invoice change",
   "Decimal lines, ROUND_HALF_UP, tax profile; threshold routing to approvers", "Quote/invoice totals; approval tasks", "Server recompute; no client totals", "Reject invalid", "0 total mismatches")
au(36, "Document assembly, hashing & diff", "W4", "BR-M43, BR-M46; CA-APPROVE; CFG-19", "Template merge; new revision",
   "Assemble from approved templates and onboarding checklists; SHA-256 hash; deterministic diff between revisions for approvers", "Document revision + hash + diff", "Changed revision voids approval", "Block share", "0 shares of unapproved hash")
au(37, "Payment matching proposal & maker-checker routing", "W4", "BR-M47; BRL-FIN; DEC-038", "Payment evidence/bank entry",
   "Match on amount, reference, date window, payer; propose to maker; checker ≠ maker", "Match proposal, tasks", "AI/automation never verifies", "Manual matching", "Reconciliation 100% (KPI-13)")
au(38, "Fulfilment ledger & over-delivery guard", "W4", "WF-10; BRL-ORD; FR-DM-03; DEC-045", "Fulfilment events", "Idempotent event keys; over-delivery rejection; reservation/release", "Ledger entries", "Duplicate event no effect", "Dispute task", "Fulfilment accuracy ≥ 98% (KPI-12)")
au(39, "Renewal calendar & rule-based account health score", "W4", "BR-M50; NT-024", "Daily", "Rules on usage, tickets, payments, engagement (no medical data)", "Renewal tasks; health band", "No medical data in scoring", "Skip and alert", "Renewal reminders 90/60/30 days 100%")
au(40, "Revenue attribution & reconciliation", "W5", "BR-M52; RPT-R9", "Payment verified", "Last non-direct touch default + alternative models with caveat", "Attribution records", "Revenue only from verified ledgers", "Recompute", "Revenue reconciles with finance 100%")
au(41, "Stage-weighted forecast & backtest", "W5", "BR-M60; CFG-22", "Weekly", "Stage probabilities from history; MAPE backtest (KPI-29); labelled estimate", "Forecast snapshot", "Never mixed with actuals", "Show last forecast", "Forecast labelled 100%")
au(42, "Usage metering & entitlement enforcement", "W5", "BR-SVC; BRL-SVC-03; DEC-047; RECOMMENDATION-064", "Each metered action incl. AI tasks",
   "Meter AI tasks per tenant (definition §7.5.4), messages, fetches, storage; 80/100% alerts; deny beyond entitlement", "Usage readings; statements", "Tenant budgets separate (DEC-008)", "Deny metered action", "Usage reconciliation 100% (KPI-24)")
au(43, "Expansion readiness gates", "W6", "BR-M63…M66; DEC-060", "Pilot/launch status change", "Checklist completion and approvals before promotion or rollout", "Gate status", "Planned offerings never promoted", "Block", "0 promotions without approval")
