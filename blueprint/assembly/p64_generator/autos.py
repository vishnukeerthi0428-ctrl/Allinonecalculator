# AU functional test sets. case: (title, links, condition/data, expected, P, type, tech, level)
U = []
def au(id, name, ep, links, cases):
    U.append(dict(id=id, name=name, ep=ep, links=links, cases=cases))

au("AU-001", "Model gateway router, Tier 0 cache & template responder", "EP-04", "BR-M08; FR-OP001; DEC-007; BRL-AI-01; ADR-070, ADR-076", [
 ("Route every rule R1–R13 of the routing decision table", "§7.3.4; DEC-007", "13 parameterized requests, one per rule, provider simulator per rule condition", "Route record equals the table's route and reason code for each rule (first match wins)", "P0", "T14", "DT", "IT"),
 ("Keep exact-cache keys scoped by tenant and startup", "NFR-032; THR-058", "Same normalized input from T1/AppNAI then T2", "T2 request is a cache miss; 0 cross-tenant hits", "P0", "T15", "EG", "IT"),
 ("Apply the semantic-cache similarity boundary", "ADR-076", "Cosine 0.9200 and 0.9199 to an approved FAQ answer", "0.9200 hit; 0.9199 miss; Restricted outputs never written to the semantic cache", "P1", "T14", "BVA", "IT"),
 ("Invalidate cache on knowledge or prompt version change", "RSK-378", "Approve KR-14 v5; bump AG-014 prompt to v3", "Prior entries miss; new entries keyed with new versions", "P1", "T14", "ST", "IT"),
 ("Block provider calls outside the gateway", "BRL-AI-01", "Static import check; egress test from worker and web containers", "0 provider SDK imports outside ai.gateway; direct HTTPS to provider host denied by egress policy", "P0", "T07", "EG", "CT")])
au("AU-002", "Budget reservation, alerts & hard stop", "EP-04", "BR-M53; BRL-AI-08; NT-025; NFR-014; DEC-008; ADR-083", [
 ("Alert and stop at budget boundaries", "BRL-AI-08; NFR-014", "Agent budget used 79.99%, 80.00%, 99.99%, 100.00%; reservation that would cross 100%", "No alert; NT-025 alert; allowed; denied; crossing reservation denied before any provider call", "P0", "T20", "BVA", "IT"),
 ("Fail closed when the ledger is unavailable", "ADR-083", "Cost ledger DB connection error", "All paid calls denied; Tier 3; alert R11", "P0", "T20", "EG", "IT"),
 ("Reconcile actual cost to reservation", "NFR-035", "Call reserves ₹0.90, actual ₹0.82", "Ledger shows reserved 0.90, actual 0.82, released 0.08; Decimal only", "P1", "T20", "EP", "IT"),
 ("Isolate budgets per agent, startup, tenant and global", "DEC-008; §6.1.3.3 A", "T2 tenant budget 100%; T1 at 40%", "T2 calls denied; T1 unaffected; owned-portfolio ceiling not used by T2", "P0", "T15", "DT", "IT"),
 ("Prevent overshoot under concurrency", "NFR-014", "50 parallel reservations at 98% used (Hypothesis stateful)", "Σ reserved ≤ cap; no overshoot", "P0", "T20", "PBT", "IT"),
 ("Allow founder top-up only with audit", "BRL-AI-08", "R01 top-up ₹500; R11 attempts top-up", "R01 succeeds with audit event; R11 403", "P1", "T07", "DT", "SYS")])
au("AU-003", "Output schema validation & repair controller", "EP-04", "BRL-AI-02; CA-AI; ADR-072", [
 ("Accept valid output without repair", "BRL-AI-02", "Valid JSON per schema v2", "Accepted; repair_count 0", "P1", "T14", "EP", "UT"),
 ("Repair at most twice then route", "BRL-AI-02; §7.3.4 R8/R11", "Invalid ×2 then valid; invalid ×3", "First accepted with repair_count 2; second routed (1a → 1b, or Tier 2 if eligible, else Tier 3)", "P0", "T14", "BVA", "IT"),
 ("Never write invalid output to business state", "BRL-AI-02", "Invalid after repairs", "0 rows in target tables; failure record and human task", "P0", "T14", "EG", "IT"),
 ("Reject unknown schema versions and out-of-enum values", "§7.2.7", "envelope_version 3.0.0 against 2.x; enum value 'urgentish'", "Rejected; enum must be closed with other/unknown", "P1", "T14", "EP", "UT")])
au("AU-004", "Data classification & PII redaction", "EP-04", "BRL-AI-06; ABAC-05; SC-35; NFR-077; ADR-080", [
 ("Detect Indian and multilingual PII at ≥ 98% recall", "SC-35; RECOMMENDATION-063", "DG-01 redaction set: 500 spans (emails, +91 phones, PAN ABCDE1234F, Verhoeff-valid synthetic Aadhaar, names in Devanagari/Tamil/Odia, addresses, health terms)", "Recall ≥ 98%; per-type recall reported", "P0", "T19", "EP", "IT"),
 ("Label mixed prompts with the highest class", "§7.3.6 rule 2", "Prompt with Public page + one Restricted contact field", "Label Restricted; Tier 2 blocked", "P0", "T19", "DT", "UT"),
 ("Re-scan the final prompt and block residual PII", "§7.3.6 rule 3", "Masked prompt where a phone survives in a URL query string", "Re-scan hit → Tier 2 blocked; event logged", "P0", "T19", "EG", "IT"),
 ("Block Tier 2 when the redactor fails", "§7.2.3 AU-004", "Presidio worker exception", "Tier 2 blocked; Tier 1 continues with minimized fields", "P0", "T19", "EG", "IT"),
 ("Keep false positives low on clean text", "[ASSUMPTION-192]", "300 clean business sentences", "False-positive rate ≤ 5%", "P2", "T14", "EP", "IT")])
au("AU-005", "Untrusted-content sanitizer & injection pre-filter", "EP-04", "BR-M12; THR-051; SC-32", [
 ("Remove hidden text", "THR-051; AIR-02", "display:none, font-size 0, white-on-white, HTML comments, aria-hidden, off-screen CSS", "Removed; visible evidence spans preserved", "P0", "T07", "EG", "UT"),
 ("Flag the injection corpus", "§7.6.3", "RT-CORE (≥ 200 cases)", "injection_suspected on ≥ 98%", "P0", "T07", "EG", "IT"),
 ("Never grant tools on flags; force L1", "§7.2.2 AU-005", "Flagged inbound used for a draft", "untrusted_input = true; draft capped at L1; no tool added", "P0", "T07", "DT", "IT"),
 ("Exclude content on sanitizer error", "§7.2.3", "Parser exception on malformed HTML", "Content excluded; page marked unextracted", "P1", "T14", "EG", "IT"),
 ("Cap length", "§7.2.2 AG-004", "Page of 40,000 tokens", "Trimmed to ≈ 2,500 tokens after boilerplate removal", "P2", "T14", "BVA", "UT")])
au("AU-006", "Eval regression CI gate", "EP-04", "BR-M54; NFR-033; DEC-061; BRL-AI-09; ADR-079", [
 ])
au("AU-007", "Source permission & expiry enforcer", "EP-05", "BR-M07; NT-003; OPT-04-01", [
 ("Deny unknown sources", "OPT-04-01", "URL on a host with no SourcePolicy", "Deny with rule ID; 0 fetches (spy)", "P0", "T19", "EP", "IT"),
 ("Stop collection at expiry", "BR-M07", "Source expires 2026-12-31 23:59:59 IST; clock to +1 s", "Fetch at expiry +1 s denied; NT-003", "P0", "T19", "BVA", "IT"),
 ("Honour robots and terms flags", "BR-M07", "robots disallow; terms flag false", "Deny", "P0", "T19", "DT", "IT"),
 ("Enforce quotas", "BR-M07", "Quota 100 fetches/day; 101st", "Denied; alert R04", "P1", "T20", "BVA", "IT")])
au("AU-008", "STOP / opt-out handler & queued-send cancellation", "EP-03", "BR-M04; BRL-ELG-02; NT-008", [
 ("Recognize multilingual STOP", "BRL-ELG-02; DEC-026", "ML-03 lexicon (en/hi/ta/or, transliterated, emoji)", "100% recognized before AI classification", "P0", "T19", "EG", "IT"),
 ("Process List-Unsubscribe one-click", "BRL-ELG-02", "RFC 8058 POST", "Suppression written; 200", "P0", "T19", "EP", "IT"),
 ("Cancel queued sends within 60 s", "NFR-036", "5 queued and 2 scheduled items in scope", "All cancelled ≤ 60 s; outbox shows cancelled", "P0", "T19", "BVA", "SYS"),
 ("Pause scope if cancellation is uncertain", "§7.2.3 AU-008", "Outbox lock timeout during cancel", "Scope paused; alert; no send", "P0", "T19", "EG", "IT")])
au("AU-009", "Policy Decision Point dispatch guard", "EP-03", "RECOMMENDATION-012; DEC-048; CA-DISPATCH; ADR-082", [
 ("Deny agent-originated items without an approved hash", "BRL-APR-02; E-8", "Draft from AG-011 not approved", "Deny APPROVAL_STALE; 0 provider calls", "P0", "T19", "DT", "IT"),
 ("Deny dispatch requests from agent identity", "ADR-082; LLM06", "R20 token calls dispatch.request", "403; TL-13 granted to none", "P0", "T07", "DT", "IT"),
 ("Recheck all conditions at dispatch", "§6.1.11.3", "Approved message; recipient suppressed between approval and dispatch", "Deny SUPPRESSED (full decision table in EP-03 TCs)", "P0", "T19", "DT", "SYS")])
au("AU-010", "Provider health checks & circuit breakers", "EP-04", "BR-M05, BR-M58; NT-033; §7.3.7", [
 ("Open after 5 consecutive failures", "§7.3.7", "4 then 5 consecutive 503s", "Closed after 4; open after 5", "P1", "T14", "BVA", "IT"),
 ("Open at ≥ 50% errors over 60 s with ≥ 10 calls", "§7.3.7", "9 calls 100% errors; 10 calls 50%; 10 calls 49%", "Closed; open; closed", "P1", "T14", "BVA", "IT"),
 ("Half-open after 30 s with one probe", "§7.3.7", "Circuit open at t; probe at t + 30 s succeeds", "One probe only; closes on success; reopens on failure", "P1", "T14", "ST", "IT"),
 ("Share state across workers", "§7.3.7", "Two worker processes; one opens circuit", "Second worker routes to fallback ≤ 60 s", "P1", "T14", "EG", "IT"),
 ("Alert R11 on circuit open", "NT-033", "Circuit open", "NT-033 raised once per incident", "P2", "T21", "EP", "IT")])
au("AU-011", "Privacy request locator & retention purge", "EP-03", "BR-M56; DEC-028; BRL-AI-10; NFR-075, NFR-076", [
 ("Find personal data in AI logs and caches", "BR-M56", "Data principal with entries in ai_model_call bodies, copilot_turn, semantic cache", "All located in the fulfilment report", "P0", "T19", "EP", "IT"),
 ("Purge AI payload bodies at 90 days", "DEC-028; BRL-AI-10", "Bodies aged 89, 90, 91 days", "Kept; purged at boundary per policy; purged; digests kept", "P0", "T19", "BVA", "IT"),
 ("Keep suppression on erasure", "BRL-PRV-03", "Erasure of a suppressed contact", "Suppression hash kept; no re-contact", "P0", "T19", "DT", "IT"),
 ("Respect legal hold", "BRL-PRV-05", "AI logs under legal hold at day 91", "Not purged; report notes hold", "P1", "T19", "DT", "IT")])
au("AU-012", "FinOps cost attribution & anomaly alerts", "EP-04", "FR-A012; RP-20, RP-21; KPI-21, KPI-22", [
 ("Attribute cost per task, agent, startup, tenant and provider", "FR-A012", "100 reconciled calls across 3 agents, 2 tenants", "Totals equal ledger Σ; Decimal; visible ≤ 1 h", "P1", "T20", "EP", "IT"),
 ("Alert at > 150% of 7-day baseline", "§7.2.3 AU-012", "Daily cost 149% and 151% of baseline", "No alert; alert", "P1", "T21", "BVA", "IT"),
 ("Alert on missing cost data", "§7.2.3", "Reconciliation job skipped 2 h", "Alert 'cost data missing'", "P2", "T21", "EG", "IT")])
au("AU-013", "Release pipeline gates", "EP-21", "BR-M09, BR-M62; NFR-012, NFR-013", [
 ("Block release on secret, SAST high or ID-lint failure", "§6.1.9.5", "PR with seeded secret; SAST high; invented FR ID", "G1 fails each", "P0", "T07", "EP", "CT"),
 ("Require eval gate for AI changes", "BRL-AI-09", "PR touching prompts/", "AU-006 job required check", "P0", "T14", "DT", "CT"),
 ("Block release without restore drill evidence", "NFR-012", "Missing EVR for restore drill", "A090 Approve disabled", "P0", "T01", "DT", "SYS")])
au("AU-014", "URL normalization, blocked-host & duplicate-content filter", "EP-05", "BR-M11", [
 ("Canonicalize and strip tracking", "BR-M11", "URLs with utm_*, fbclid, mixed case host, trailing slash", "One canonical URL", "P2", "T01", "EP", "UT"),
 ("Never fetch blocked hosts", "BR-M11", "Blocked host list", "0 fetches", "P0", "T19", "EP", "IT"),
 ("Dedupe by content hash", "§7.4.2 technique 9", "Same content at 2 URLs", "One AG-004 call; duplicate rate ≤ 5%", "P2", "T20", "EG", "IT"),
 ("Reject SSRF targets", "THR-048", "http://169.254.169.254/, file://, internal hostnames", "Rejected before fetch", "P0", "T07", "EG", "IT")])
au("AU-015", "Organization canonical upsert & safe merge", "EP-05", "BR-M13", [
 ("Match by domain, location and alias", "BR-M13", "'Sunrise Clinics Pvt Ltd' vs 'Sunrise Clinics Private Limited', same domain", "Single organization", "P1", "T01", "EP", "IT"),
 ("Never merge across startups or tenants", "NFR-032", "Same domain in T1/AppNAI and T2", "Two records; no merge", "P0", "T15", "DT", "IT"),
 ("Create merge tasks on conflicts", "BR-M13", "Same name, different domains", "Merge task to R04", "P1", "T01", "DT", "IT"),
 ("Normalize Unicode before matching", "EG-08", "NFC vs NFD names", "Matched", "P2", "T01", "EG", "UT")])
au("AU-016", "Readiness-gated solution match ranking", "EP-05", "BR-M16; BRL-SCR-04; ADR-077", [
 ("Exclude non-Available offerings", "BRL-SCR-04; DEC-060", "Doctor Connect Planned", "Excluded with reason", "P0", "T19", "DT", "IT"),
 ("Apply geography and capability filters", "BRL-SCR-04", "Need in DE; offering IN-only", "Excluded with rule ID", "P1", "T01", "DT", "IT"),
 ("Rank reviewer-chosen offering in top 3", "§7.2.3 KPI", "DS-07 needs", "≥ 85% contain reviewer choice", "P2", "T14", "EP", "SYS"),
 ("Search only the scoped vector namespace", "THR-058; LLM08", "Need in T2", "0 T1 chunks", "P0", "T15", "EG", "IT")])
au("AU-017", "Opportunity scoring", "EP-06", "BR-M17; DEC-011; BRL-SCR-01…09", [
 ("Return Unknown below 0.60 known weight", "DEC-011", "Known weight 0.59 and 0.60", "Unknown; numeric score", "P1", "T01", "BVA", "UT"),
 ("Round half up", "EG-02", "Score 74.5", "75 (band ≥ 75)", "P1", "T01", "BVA", "UT"),
 ("Hold score bounds and monotonicity", "§6.1.11.7", "Hypothesis components", "0 ≤ score ≤ 100; monotonic", "P1", "T01", "PBT", "UT"),
 ("Never grant contact permission", "DEC-011", "Score 95, no consent", "PDP denies NO_LAWFUL_BASIS", "P0", "T19", "DT", "IT")])
au("AU-018", "Contact verification & freshness expiry", "EP-06", "BR-M19", [
 ("Verify by provenance and channel checks", "BR-M19", "Published email on official page; MX valid", "Verified", "P1", "T01", "DT", "IT"),
 ("Keep verified separate from consent", "BR-M19", "Verified contact without consent", "Not eligible for outreach", "P0", "T19", "DT", "IT"),
 ("Expire stale verification", "BR-M19", "Freshness expiry date + 1 day", "Unverified; recheck task", "P1", "T01", "BVA", "IT")])
au("AU-019", "Research review assignment & alerts", "EP-06", "BR-M20; NT-001", [
 ("Assign by round-robin or owner rules", "BR-M20", "6 opportunities, 3 reviewers", "2 each", "P2", "T01", "EP", "IT"),
 ("Escalate after 2 business days", "§7.2.3", "Assignment Friday 17:00 IST; Tuesday 17:00", "Escalation at the business-day boundary", "P2", "T01", "BVA", "IT"),
 ("Never send rejected leads to a channel", "BR-M20", "Rejected opportunity", "0 enrolments", "P0", "T19", "DT", "IT")])
au("AU-020", "Lead dedupe, consent capture & form routing", "EP-07", "BR-M22; DEC-030; CA-INTAKE", [
 ("Create one lead per duplicate submission", "NFR-005", "Same idempotency key twice", "One lead", "P0", "T16", "EP", "IT"),
 ("Record consent with policy revision", "CA-INTAKE", "Consent PN-5", "Consent row with revision PN-5", "P0", "T19", "EP", "IT"),
 ("Route by typed fields", "FR-DM-04", "EduVerse form selecting 'AI development project'", "Routed to AppNAI", "P1", "T01", "DT", "IT"),
 ("Send under-18 to guardian path with grade band only", "DEC-030", "Age band 13–17", "Guardian path; learner fields name, grade band, programme only", "P0", "T19", "BVA", "IT")])
au("AU-021", "Customer 360 projection", "EP-07", "BR-M23; NFR-008", [
 ("Show events within 60 s", "NFR-008", "Inbound reply event", "Visible ≤ 60 s", "P1", "T03", "BVA", "SYS"),
 ("Rebuild from events identically", "§7.2.3", "Drop and rebuild projection", "Identical view", "P1", "T01", "EP", "IT"),
 ("Enforce RLS on the projection", "NFR-032", "T2 user query", "0 T1 rows", "P0", "T15", "DT", "IT")])
au("AU-022", "Sequence scheduler with stop-on-reply", "EP-08", "BR-M28; BRL-SEQ", [
 ("Stop on any substantive reply", "BR-M28", "AG-013 intent question", "0 further steps", "P0", "T19", "ST", "IT"),
 ("Stop on STOP", "BRL-ELG-02", "AU-008 suppression", "Enrolment stopped", "P0", "T19", "ST", "IT"),
 ("Defer in quiet hours", "BRL-ELG-08", "Step due 19:00:00 recipient time", "Deferred to 09:00", "P1", "T19", "BVA", "IT"),
 ("Keep sequence running on out-of-office", "BR-M28", "Intent out-of-office", "Paused to return date per template, not stopped", "P2", "T01", "DT", "IT")])
au("AU-023", "Meeting slot offer & booking conflict check", "EP-09", "BR-M29; DEC-024", [
 ("Offer only free slots", "DEC-024", "Free/busy with 3 busy blocks", "No invented availability", "P1", "T01", "EP", "IT"),
 ("Convert time zones across DST", "I18N-03", "CET slot on 2027-03-28", "Correct IST conversion", "P1", "T13", "BVA", "IT"),
 ("Book once under concurrency", "§6.1.6.3", "Two confirmations for one slot", "One booking; second gets alternatives", "P0", "T16", "EG", "IT")])
au("AU-024", "Bounce/complaint suppression", "EP-08", "BR-M26; DEC-025; BRL-ELG-11, BRL-ELG-12", [
 ("Suppress on hard bounce and complaint", "BRL-ELG-11", "SNS hard bounce; complaint", "Suppressed", "P0", "T19", "EP", "IT"),
 ("Suppress after third soft bounce in 7 days", "BRL-ELG-12", "2 and 3 soft bounces", "Not suppressed; suppressed", "P0", "T19", "BVA", "IT"),
 ("Reject invalid signatures and dedupe", "NFR-005", "Mis-signed event; duplicate message ID", "Rejected; one effect", "P0", "T16", "EG", "IT")])
au("AU-025", "Emergency stop & runaway guard", "EP-18", "BRL-AUT-05, BRL-AUT-06; NT-032; ADR-085", [
 ])
au("AU-026", "Uncertain-outcome reconciliation", "EP-18", "RECOMMENDATION-015; FR-STD-02; DEC-050", [
 ("Block retry until reconciled", "FR-STD-02", "Timeout after submit", "uncertain; retry blocked", "P0", "T18", "ST", "IT"),
 ("Create a human task after 3 failed queries", "DEC-050", "Query unavailable ×3", "Task in A110", "P1", "T18", "BVA", "IT"),
 ("Keep reconciling during emergency stop", "§6.1.3.3 D", "Kill switch on", "Read-only queries continue; no dispatch", "P1", "T18", "DT", "IT")])
au("AU-027", "Notification digest & approval SLA escalation", "EP-17", "DEC-036; NT-009", [
 ("Escalate approvals pending > 1 business day", "BRL-APR-10", "Across weekend and an India public holiday", "Escalation at correct business-day boundary", "P1", "T01", "BVA", "IT"),
 ("Dedupe notifications", "§7.2.3", "Same event twice", "One notification", "P2", "T16", "EP", "IT"),
 ("Keep digests within scope", "NFR-032", "T2 digest", "0 T1 items", "P0", "T15", "DT", "IT")])
au("AU-028", "Missed-schedule recovery", "EP-18", "BRL-AUT-10; DEC-032", [
 ("Recover a missed run once", "BRL-AUT-10", "Scheduler down for one slot", "One recovered run", "P1", "T01", "ST", "IT"),
 ("Alert on further misses", "BRL-AUT-10", "Second consecutive miss", "Alert R11; no duplicate", "P1", "T21", "ST", "IT"),
 ("Produce no duplicate side effect on recovery", "NFR-005", "Recovered run after partial execution", "Exactly one effect", "P0", "T16", "EG", "IT")])
au("AU-029", "Publication pipeline & expiry monitor", "EP-19", "FR-PUB-01; NT-036, NT-037", [
 ("Publish only the approved hash", "FR-PUB-01", "Edited revision after approval", "Publish denied", "P0", "T07", "DT", "IT"),
 ("Swap pointer atomically and invalidate tenant-keyed cache", "NFR-020", "Publish v5", "Single swap; T2 host unaffected", "P0", "T15", "EG", "SYS"),
 ("Notify claim expiry", "NT-036", "Claim CL-12 expires 2027-03-31", "Notice at configured lead time; expired claim unusable by AG-011", "P1", "T01", "BVA", "IT")])
au("AU-030", "Automation conflict resolution by priority rules", "EP-18", "FR-A111; BRL-AUT-09", [
 ("Resolve by priority compliance > transactional > sales > marketing", "BRL-AUT-09", "Campaign step and transactional reminder to one contact", "Transactional wins; campaign held", "P0", "T19", "DT", "IT"),
 ("Hold both and open a conflict case when equal", "NT-031", "Two sales sequences", "ConflictCase; escalate to owner", "P1", "T01", "DT", "IT"),
 ("Use no cross-tenant context", "NFR-032", "Same email in T1 and T2", "No conflict across tenants", "P0", "T15", "DT", "IT")])
au("AU-031", "Compliance auto-pause on complaint threshold", "EP-03", "BR-M57; NT-027; BRL-ELG-11", [
 ("Pause at 0.11% complaint rate or 3 complaints in 24 h", "BRL-ELG-11", "0.10% and 0.11%; 2 and 3 complaints", "No pause; pause; no pause; pause", "P0", "T19", "BVA", "IT"),
 ("Pause within 5 minutes", "§7.2.3", "Threshold event", "Campaign paused ≤ 5 min; incident", "P0", "T19", "BVA", "SYS"),
 ("Require R10 to resume", "§7.2.3", "R05L resume attempt", "403; R10 succeeds", "P1", "T07", "DT", "SYS")])
au("AU-032", "Ad spend cap & anomaly pause", "EP-12", "BR-M39; BRL-MKT-05; NT-026", [
 ("Stop spend at the approved cap", "BRL-MKT-05", "Spend reaching cap", "Pause via provider API; 0 spend beyond cap", "P0", "T20", "BVA", "IT"),
 ("Pause at > 150% anomaly", "§7.2.3", "Hourly spend 151% of baseline", "Paused; NT-026", "P1", "T20", "BVA", "IT"),
 ("Pause on uncertainty", "§7.2.3", "Spend API timeout", "Pause issued; uncertain reconciled", "P1", "T18", "EG", "IT")])
au("AU-033", "SEO technical audit", "EP-11", "BR-M36", [
 ("Report crawl defects", "BR-M36", "Pages with 404, missing canonical, meta 200 characters", "Prioritized fix list in A055", "P2", "T01", "EP", "IT"),
 ("Fabricate no ranking data", "§7.2.3", "Search Console not authorized", "Skip with reason; no ranking numbers", "P1", "T01", "EG", "IT")])
au("AU-034", "Bid deadline & mandatory-checklist tracker", "EP-14", "BRL-BID; NT-020, NT-021; DEC-053", [
 ("Apply the deadline buffer boundary", "BRL-BID-01; FR-DM-02", "Approval at deadline − 24 h − 1 s and − 24 h", "Allowed; blocked (soft warning then hard block at true deadline per errata #3)", "P0", "T01", "BVA", "IT"),
 ("Gate on mandatory checklist completeness", "BR-S034", "One mandatory item missing", "Bid decision blocked without approved waiver", "P0", "T01", "DT", "IT"),
 ("Reject evidence recorded after the deadline", "DEC-053", "Submission timestamp after deadline", "Rejected", "P0", "T01", "BVA", "IT")])
au("AU-035", "Quote calculator, invoice generation & approval routing", "EP-13", "BR-M44; DEC-027, DEC-038; FR-DM-01", [
 ("Compute the FR-DM-01 worked example", "FR-DM-01", "2 × ₹150.00 × (1 − 0.10)", "₹270.00", "P0", "T01", "EP", "UT"),
 ("Route discounts at 10.00/10.01/20.00/20.01%", "DEC-038", "BVA-D05…D09", "Approvers per §6.1.11.2", "P0", "T01", "BVA", "IT"),
 ("Recompute server-side, ignoring client totals", "§7.2.3", "Client posts total 1.00", "Server total used", "P0", "T07", "EG", "IT"),
 ("Hold money properties", "NFR-017", "Hypothesis line money", "Half-up; bounds", "P0", "T01", "PBT", "UT")])
au("AU-036", "Document assembly, hashing & diff", "EP-13", "BR-M43, BR-M46; CA-APPROVE; CFG-19", [
 ("Void approval on any change", "CA-APPROVE", "One character edited after approval", "Hash differs; approval void", "P0", "T19", "ST", "IT"),
 ("Produce an exact diff", "CI-108", "Two revisions with 3 changes", "All 3 listed; no omissions", "P1", "T01", "EP", "UT"),
 ("Block sharing an unapproved hash", "§7.2.3", "Share request for draft", "Blocked", "P0", "T07", "DT", "IT")])
au("AU-037", "Payment matching proposal & maker-checker routing", "EP-15", "BR-M47; BRL-FIN; DEC-038", [
 ("Propose matches on amount, reference, date window and payer", "BR-M47", "Evidence UTR matches INV-2207", "Proposal to maker", "P1", "T01", "DT", "IT"),
 ("Require checker different from maker", "BRL-APR-07", "Same user", "403", "P0", "T07", "DT", "IT"),
 ("Never verify automatically", "BRL-AI-07", "Exact match", "State MakerVerified only after human action", "P0", "T19", "ST", "IT")])
au("AU-038", "Fulfilment ledger & over-delivery guard", "EP-14", "WF-10; BRL-ORD; FR-DM-03; DEC-045", [
 ("Ignore duplicate delivery events", "FR-DM-03", "1 kg twice with same key", "One entry", "P0", "T16", "EG", "IT"),
 ("Reject over-delivery", "BRL-ORD-02", "102.00% and 102.01% with 2% policy", "Allowed; rejected", "P0", "T01", "BVA", "IT"),
 ("Release reservation on cancel", "DEC-045", "Approved order cancelled", "Availability restored", "P1", "T01", "ST", "IT")])
au("AU-039", "Renewal calendar & rule-based account health score", "EP-16", "BR-M50; NT-024", [
 ("Send reminders at 90/60/30 days", "BR-M50", "Expiry 2027-03-31", "Reminders on 2026-12-31, 2027-01-30, 2027-03-01", "P1", "T01", "BVA", "IT"),
 ("Use no medical data in scoring", "BR-M50", "Account with EDGE-HEALTH notes", "Notes not read by the score", "P0", "T19", "EG", "IT")])
au("AU-040", "Revenue attribution & reconciliation", "EP-15", "BR-M52; RPT-R9", [
 ("Attribute only verified revenue", "BR-M52", "Unverified payment", "Not attributed", "P0", "T01", "DT", "IT"),
 ("Apply last non-direct touch by default", "BR-M52", "Touches: email, direct, WhatsApp", "WhatsApp credited; alternative models carry caveat", "P2", "T01", "EP", "IT"),
 ("Reconcile 100% with finance", "KPI-13", "Month of payments", "Revenue equals verified ledger", "P0", "T01", "EP", "IT")])
au("AU-041", "Stage-weighted forecast & backtest", "EP-17", "BR-M60; CFG-22", [
 ("Label forecasts as estimates and never mix with actuals", "BRL-FIN-06", "Dashboard with both", "Separate series; 'estimate' label", "P1", "T01", "EP", "E2E"),
 ("Compute MAPE backtest", "KPI-29", "12 weeks history", "MAPE reported", "P2", "T01", "EP", "IT")])
au("AU-042", "Usage metering & entitlement enforcement", "EP-20", "BR-SVC; BRL-SVC-03; DEC-047; RECOMMENDATION-064", [
 ("Count AI tasks per the §7.5.4 definition", "RECOMMENDATION-064", "Run with 2 repairs + escalation; Tier 0 cache hit; Tier 3 failure", "1 task; 1 task; 0 tasks", "P0", "T20", "DT", "IT"),
 ("Deny beyond entitlement with alerts", "DEC-047", "Starter 1,000 tasks: 800, 1,000, 1,001", "80% alert; 100% alert; denied", "P0", "T20", "BVA", "IT"),
 ("Reconcile usage to invoice lines", "NFR-035; KPI-24", "Month of T2 usage", "100% reconciled", "P0", "T20", "EP", "IT")])
au("AU-043", "Expansion readiness gates", "EP-16", "BR-M63…M66; DEC-060", [
 ("Block promotion without approvals", "DEC-060", "Checklist incomplete", "Blocked", "P1", "T01", "DT", "IT"),
 ("Never promote Planned offerings", "BR-M66", "Planned offering", "Blocked", "P0", "T19", "DT", "IT")])
