from h_ep01 import R

INTRO = """Risk area RA-22 discovery, source permissions and provenance: P1 overall because discovery has no outbound effect, but **"prohibited source never fetched"** cases are P0 (Part 6.1 §6.1.4.3; OPT-04-01; W1 exit). SSRF and egress cases are P0 security. Waves W0 (US-0501), W1 (US-0502…0508, 0511, 0512; W1 exit: ≥ 100 reviewed signals at ≥ 80% precision, DEC-001; slips to ≈ Day 45 under CONFLICT-130), W3 (US-0509, Could), W5 (US-0510, Could). Signal classification quality itself (AG agent precision) is a TC-AI concern in Batch 6.4; the gate tracker that consumes it is tested here."""

EXTRA_TS = []

GROUPS = [
    dict(ts="US-0501", heading="Decision table – may this URL be fetched? (BRL-SRC-01, -02, -04)", tech="DT",
         intro="""Evaluated by the fetcher's allowlist check before any network call (US-0501, US-0511). Host match = exact host or approved path prefix; wildcard only for subdomains of an approved registrable domain.

| Condition / Rule | F1 | F2 | F3 | F4 | F5 | F6 | F7 |
|---|---|---|---|---|---|---|---|
| Host or path matches a registered source of the plan's startup | N | Y | Y | Y | Y | Y | Y |
| Source state Active | – | N | Y | Y | Y | Y | Y |
| Now < source expiry | – | – | N | Y | Y | Y | Y |
| Host not on the blocked list | – | – | – | N | Y | Y | Y |
| robots/terms review recorded and allows the path | – | – | – | – | N | Y | Y |
| Each redirect target re-validated as F7 (≤ 3 hops) | – | – | – | – | – | N | Y |
| **Action** | block `SOURCE_NOT_APPROVED` | block `SOURCE_NOT_ACTIVE` | skip; evidence marked "source expired" | discard; count "blocked host" | block `ROBOTS_DISALLOWED` | stop `REDIRECT_NOT_APPROVED` | fetch |""",
         rows=[
        R("F1: block an unregistered host before any network call", "AC-0501-02; FR-A010; BRL-SRC-01; NFR-028", "Run for MedMaarg; URL https://unlisted-directory.example.net/hospitals", "1. Fetch. 2. Inspect egress proxy log", "1: `SOURCE_NOT_APPROVED`. 2: 0 outbound connections", "P0", "T19", "DT", "Y", "IT"),
        R("F2: block a source still in PendingApproval", "US-0501; BRL-SRC-01", "Source gem.example.gov.in PendingApproval", "1. Fetch a listing URL", "`SOURCE_NOT_ACTIVE`; 0 connections", "P0", "T19", "DT", "Y", "IT"),
        R("F3: skip an expired source and mark its evidence", "AC-0501-03, AC-0510-05; BRL-SRC-02", "Source kims-hospital.example.com news expires 2027-03-31T23:59:59+05:30", "1. Scheduled run 2027-04-01T07:00 IST", "Source skipped; evidence \"source expired\"; run log counts skipped", "P0", "T19", "DT", "Y", "SYS"),
        R("F4: discard results from a blocked host", "AC-0503-03; BRL-SRC-01", "patient-forum.example.org on blocked list", "1. Search returns 3 results from it", "Discarded; \"rejected: blocked host\" = 3", "P0", "T19", "DT", "Y", "IT"),
        R("F5: refuse a path disallowed by the recorded robots review", "US-0501; BRL-SRC-04", "Source review disallows /private/*", "1. Fetch https://gem.example.gov.in/private/list", "`ROBOTS_DISALLOWED`; 0 connections", "P0", "T19", "DT", "Y", "IT"),
        R("F6: stop at a redirect to an unapproved host", "AC-0511-03; BRL-SRC-01", "Approved URL 302 → https://unapproved.example.net/page", "1. Fetch", "Redirect not followed; `REDIRECT_NOT_APPROVED`", "P0", "T07", "DT", "Y", "IT"),
        R("F6: stop at the 4th redirect even within approved hosts", "US-0511; BRL-SRC-01", "Chain of 4 redirects inside gem.example.gov.in", "1. Fetch", "Stops after 3 hops `TOO_MANY_REDIRECTS`", "P0", "T07", "BVA", "Y", "IT"),
        R("Refuse registration of login-walled or personal-profile sources", "AC-0501-04, AC-0509-02; BRL-SRC-04", "R04 AppNAI", "1. Register access method \"logged-in scraping\". 2. Register a personal social profile URL", "Both fail \"Private or login-walled collection is not permitted (BRL-SRC-04)\"", "P0", "T19", "DT", "Y", "SYS"),
    ]),
    dict(ts="US-0501", heading="State transition and boundaries – source permission lifecycle", tech="ST, BVA",
         intro="""```mermaid
stateDiagram-v2
  [*] --> Proposed
  Proposed --> PendingApproval : submit
  PendingApproval --> Active : approve by R10 or R02, not author
  PendingApproval --> Proposed : reject with reason
  Active --> Expired : expiry reached
  Active --> Revoked : revoke
  Expired --> PendingApproval : renew
  Revoked --> [*]
```

Expiry: at most 12 months after registration (AC-0501-06); NT-003 warning 14 days before expiry (2027-03-17 for 2027-03-31).""",
         rows=[
        R("Approve a tender portal: Proposed → PendingApproval → Active", "AC-0501-01; FR-A010; KPI-27", "R04 AppNAI registers gem.example.gov.in (public web, purpose tender discovery, daily 07:00 IST, expiry 2027-12-31)", "1. Submit. 2. R10 approves. 3. Reference it in a plan", "Active; plan saves with the source", "P1", "T01", "ST", "Y", "SYS"),
        R("Refuse approval by the proposing analyst", "AC-0501-05; BRL-APR-01", "R04 proposed the source", "1. R04 POST approve", "403 `APPROVER_IS_AUTHOR`; state PendingApproval", "P0", "T07", "ST", "Y", "SYS"),
        R("Accept expiry exactly 12 months ahead and refuse 12 months + 1 day", "AC-0501-06; BRL-SRC-02", "Registered 2027-01-10", "1. Expiry 2028-01-10. 2. Expiry 2028-01-11. 3. Expiry 2028-06-30", "1: accepted. 2–3: \"Approval expiry may be at most 12 months ahead\"", "P1", "T01", "BVA", "Y", "SYS"),
        R("Warn 14 days before expiry and expire at the expiry instant", "AC-0501-03; BRL-SRC-02; NT-003", "Expiry 2027-03-31T23:59:59+05:30; clock control", "1. Clock 2027-03-16T23:59. 2. Clock 2027-03-17T00:00. 3. Clock 2027-04-01T00:00:00", "1: no NT-003. 2: NT-003 to R04 and R10. 3: Expired; next scheduled run skips it", "P1", "T19", "BVA", "Y", "SYS"),
        R("Point a duplicate host proposal to the existing source", "AC-0501-07; NFR-005", "gem.example.gov.in Active in AppNAI", "1. Propose same host in AppNAI. 2. Propose same host in MedMaarg", "1: pointer to existing source; no new row. 2: allowed (startup-scoped registry)", "P1", "T16", "EG", "Y", "SYS"),
    ]),
    dict(ts="US-0511", heading="Equivalence classes and boundaries – fetcher sandbox, SSRF and limits", tech="EP, BVA",
         intro="""| Class | Representatives (resolved after DNS) | Expected |
|---|---|---|
| Public approved | kims-hospital.example.com → 93.184.216.34 | fetch |
| Link-local metadata | 169.254.169.254; IPv6 fd00:ec2::254 | `PRIVATE_ADDRESS_BLOCKED` |
| Private ranges | 10.0.3.7; 172.16.0.5; 192.168.1.1 | blocked |
| Loopback and encodings | localhost; 127.0.0.1; ::1; 2130706433 (decimal); 0x7f000001 | blocked |
| DNS rebinding | approved host resolves public at check, private at connect | blocked (pin resolved IP; re-check at connect) |
| Size | 8 MB exactly → fetch; 8 MB + 1 B → `SIZE_LIMIT`; 9 MB → `SIZE_LIMIT` | US-0511 notes |
| Processed text | 2 MB cleaned text kept; remainder truncated, evidence marked "truncated" | AC-0504-08 |
| Type | text/html, application/pdf, text/plain → fetch; application/x-msdownload → `TYPE_NOT_ALLOWED` | |
| Time | response complete at 14.9 s → fetch; at 15 s → timeout, next URL | |""",
         rows=[
        R("Block metadata, private and loopback addresses including encoded forms", "AC-0511-02; BRL-SRC-01; NFR-022", "Approved host patterns pointing (via test DNS) to each blocked class", "1. Fetch each", "`PRIVATE_ADDRESS_BLOCKED`; security event; 0 connections to the target", "P0", "T07", "EP", "Y", "IT"),
        R("Defeat DNS rebinding by pinning the resolved IP", "US-0511; BRL-SRC-01", "Test DNS answers 93.184.216.34 then 10.0.3.7 (TTL 0)", "1. Fetch", "Connection uses the checked IP or is refused; never reaches 10.0.3.7", "P0", "T07", "EG", "Y", "IT"),
        R("Fetch 8 MB and abort at 8 MB + 1 byte", "AC-0511-04; NFR-022", "Simulated pages of 8,388,608 B and 8,388,609 B", "1. Fetch each", "1st fetched; 2nd aborted `SIZE_LIMIT`; run continues", "P0", "T07", "BVA", "Y", "IT"),
        R("Process only the first 2 MB of cleaned text and mark evidence truncated", "AC-0504-08; BRL-SRC-03", "Page of 8 MB HTML", "1. Fetch and extract", "Only 2 MB cleaned text processed; evidence \"truncated\"", "P1", "T01", "BVA", "Y", "IT"),
        R("Refuse application/x-msdownload content", "AC-0511-04; NFR-021", "Response with that content type", "1. Fetch", "`TYPE_NOT_ALLOWED`", "P0", "T07", "EP", "Y", "IT"),
        R("Complete at 14.9 s and time out at 15 s", "AC-0511-05; NFR-022", "Server dribbling 1 byte/s; finishing at 14.9 s vs 20 s", "1. Fetch each", "1st completes; 2nd times out at 15 s; next URL processed", "P1", "T01", "BVA", "Y", "IT"),
        R("Deny the fetcher role access to PostgreSQL and tenant S3 prefixes", "AC-0511-06; NFR-032", "Fetcher task role in `test` account", "1. Connect to DB endpoint. 2. ListObjects on `t1/`", "Both denied by IAM/network; CloudTrail event", "P0", "T07", "EP", "Y", "IT"),
    ]),
    dict(ts="US-0504", heading="Boundary values – evidence freshness and provenance (BRL-SRC-03, -06)", tech="BVA",
         intro="Freshness SLA: tenders 7 days, other evidence 90 days by default (US-0504 notes). Interpretation [ASSUMPTION-196]: evidence observed on date d is fresh through d + SLA − 1 and stale from d + SLA at 00:00 IST.",
         rows=[
        R("Keep tender evidence fresh on day 7 and mark it stale on day 8", "AC-0504-03; BRL-SRC-06; NT-004", "EV-902 tender observed 2027-02-01", "1. Clock 2027-02-07T23:59:59 IST. 2. Clock 2027-02-08T00:00:00 IST", "1: fresh. 2: stale; dependent score flagged for recompute; NT-004 to owner", "P1", "T01", "BVA", "Y", "SYS"),
        R("Keep news evidence fresh through day 90 and stale on day 91", "US-0504; BRL-SRC-06", "EV-881 observed 2027-02-15", "1. Clock 2027-05-15T23:59:59. 2. 2027-05-16T00:00:00", "1: fresh. 2: stale", "P1", "T01", "BVA", "Y", "SYS"),
        R("Store full provenance on evidence EV-881", "AC-0504-01; FR-A017; NFR-028", "Page published 2027-02-02, fetched 2027-02-15", "1. Extract", "URL, retrieved 2027-02-15T07:04:12+05:30, published date, source permission revision, SHA-256, excerpt, event type new_facility, confidence 0.86", "P0", "T19", "UC", "Y", "SYS"),
        R("Quarantine evidence whose source licence revision cannot be resolved", "AC-0504-02; BRL-SRC-03", "Permission revision lookup returns none", "1. Extract", "Quarantined; excluded from signals and scoring", "P0", "T19", "DT", "Y", "SYS"),
    ]),
    dict(ts="US-0506", heading="Boundary values – Wave 1 signal precision gate (DEC-001)", tech="BVA",
         intro="Gate: ≥ 100 human-reviewed signals **and** precision (confirmed ÷ reviewed) ≥ 80.0% (DEC-001; KPI-02).",
         rows=[
        R("Show gate met at 80/100 and not met at 79/100", "AC-0506-03; DEC-001; NFR-011; KPI-02", "Reviewed signals in the W1 period", "1. Load 100 reviewed with 80 confirmed. 2. 100 with 79", "1: \"Precision 80.0% (80/100) – W1 gate met\". 2: \"Not met\"", "P1", "T14", "BVA", "Y", "SYS"),
        R("Show gate not met at 99 reviewed even with 100% precision", "AC-0506-03; DEC-001", "99 reviewed, 99 confirmed", "1. Open tracker", "\"Not met – 99 of 100 reviews\"", "P1", "T14", "BVA", "Y", "SYS"),
        R("Keep a 0.52-confidence signal in review below the 0.70 threshold", "AC-0506-04; BRL-AI-04", "Signal with confidence 0.52", "1. Process", "In review; no opportunity created until confirmed", "P0", "T14", "BVA", "Y", "SYS"),
    ]),
]

TS_TITLE = {
    "US-0501": "Sources registered, approved and expired; unapproved sources never fetched",
    "US-0502": "Research plans generate only safe queries",
    "US-0503": "Discovery adapter stores results with provenance and handles provider faults",
    "US-0504": "Evidence extracted with provenance, freshness and injection quarantine",
    "US-0505": "Organizations upserted and merged safely within a tenant",
    "US-0506": "Signals classified, reviewed and counted toward the W1 gate",
    "US-0507": "Business needs confirmed only with evidence",
    "US-0508": "Solution matching uses only available offerings",
    "US-0509": "Social listening limited to permitted organizational sources",
    "US-0510": "Competitor watch for internal alerts only",
    "US-0511": "Fetcher sandbox blocks SSRF, oversize and slow responses",
    "US-0512": "Research run metrics and source coverage",
}
