# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 6 (Batch 6.3b), Test Scenarios and Test Cases: EP-19 to EP-21, Acceptance Procedures and Release Drills

| Field | Value |
|---|---|
| Document | Application Blueprint, Part 6 (Batch 6.3, file b of 2): test scenarios (TS), test cases (TC) and story-level AI evaluation cases (TC-AI) for **EP-19 Public website and external portal**, **EP-20 SaaS client lifecycle and portability** and **EP-21 Release readiness, QA and observability**, including the **release, restore (DR) and rollback drills** that are EP-21 stories; the consolidated **acceptance procedure scripts AP-01, AP-04, AP-06, AP-09 and AP-10**; and the **batch roll-up** (coverage, totals, tags, quality gate) for files a and b. File a (`Part-06-3a_Test_Cases_EP15-EP18.md`) covers EP-15 to EP-18 |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | Part 0, Part 0A (DEC-001…065), Part 1, Part 2.1–2.5, Part 4.1–4.3 (threats THR-, DR and pipeline design), **Part 5.3** (stories US-1901…US-2110 and their Gherkin AC), **Part 6.1** (conventions §6.1.12, techniques §6.1.11, GSE-SYN §6.1.7, environments §6.1.6, DR plan §6.1.14.4, AP register §6.1.13.6), Part 7.1/7.2 (agent IDs and specs) |
| Roles applied | QA Lead (primary), DevOps/SRE Lead, Security/Compliance/AI Governance Lead, Principal Engineer, Business Systems Analyst, Lead UX/UI Designer, Data Architect/DBA, FinOps Lead, Product Owner |
| Tag ranges used | RECOMMENDATION-077…078 · ASSUMPTION-188…190 (shared with file a; full register in §6.3.15) |

**Conventions.** This file uses the conventions, compact test case table, standard post-conditions and fixture keys defined in file a §6.3.1 (including the no-side-effect assertion for every denial and the two-tenant fixture on every IT/SYS/E2E case). Acronyms are as in file a, plus: ACM AWS Certificate Manager · CDN content delivery network · CSP Content-Security-Policy · HSTS HTTP Strict Transport Security · IDN internationalized domain name · LCP Largest Contentful Paint · RPO recovery point objective · RTO recovery time objective · SLO service level objective · TTFB time to first byte.

**Time-sensitive facts.** CDN and certificate behaviour (CloudFront, ACM), identity-provider features (passkeys, TOTP), browser versions, axe-core and Lighthouse rule sets, AWS RDS PITR behaviour, secondary-region availability and all prices are **unverified; verify at time of implementation (as of 27 Nov 2026)**.

---

## 6.3.9 EP-19 Public website and external portal

Risk areas: RA-14 (publication, hosts, CDN, previews; **P0, depth D4**), RA-15 (portal object grants and DTOs; **P0, D4**), RA-02 (identity reuse and audiences; P0), RA-30 (accessibility, performance; P1/P2). Waves W2 (US-1901…1906, 1909…1913), W3 (US-1907, 1908).

### 6.3.9.1 Scenarios

| TS ID | Title | Linked US / FR | Risk area · Priority | TCs |
|---|---|---|---|---|
| TS-19-01 | Verified domains map to exactly one startup; unknown hosts reveal nothing | US-1901; FR-A107, FR-W03 | RA-14 · P0 | TC-19-001…008 |
| TS-19-02 | Publication swaps an atomic pointer to an immutable snapshot and purges only tenant keys | US-1902; FR-A108, FR-PUB-01 | RA-14 · P0 | TC-19-009…017 |
| TS-19-03 | Site configuration uses only approved offerings and unexpired, labelled claims | US-1903; FR-A107 | RA-14 · P0 (claims) / P1 | TC-19-018…024 |
| TS-19-04 | Publication lifecycle: preview, approve by hash, schedule, publish, roll back | US-1904; FR-A108, FR-PUB-01 | RA-14 · P0 | TC-19-025…038 |
| TS-19-05 | Platform homepage and directory list only published, opted-in businesses | US-1905; FR-W01, FR-W02 | RA-14 · P1; exposure P0 | TC-19-039…045 |
| TS-19-06 | Startup site, catalogue and offering details show approved, evidence-backed content | US-1906; FR-W03, FR-W04, FR-W05 | RA-14 · P0 (planned/claims) / P1 | TC-19-046…052 |
| TS-19-07 | Public prices are approved and current; private prices only behind a grant | US-1907; FR-W06 | RA-15 · P0 | TC-19-053…058 |
| TS-19-08 | Industry pages publish only evidenced outcomes and route by capability | US-1908; FR-W07 | RA-28 · P2; draft exposure P0 | TC-19-059…062 |
| TS-19-09 | Portal identity uses the external audience, HttpOnly cookies, MFA and isolated recovery | US-1909; FR-W21 | RA-02 · P0 | TC-19-063…071 |
| TS-19-10 | Customer dashboard shows only granted, verified records per startup | US-1910; FR-W22 | RA-15 · P0 | TC-19-072…077 |
| TS-19-11 | Public pages and portal meet WCAG 2.2 AA and performance budgets | US-1911; FR-W01…W07, W21, W22, A108 | RA-30 · P1 | TC-19-078…086 |
| TS-19-12 | Surface separation, rate limits and cross-boundary tests | US-1912 | RA-01/RA-14 · P0 | TC-19-087…095 |
| TS-19-13 | Publication and public-site monitoring | US-1913; FR-A108 | RA-14 · P1 | TC-19-096…101 |

### 6.3.9.2 Group TC-19-A: Equivalence partitions and boundaries – host resolution (techniques: EP, BVA) · TS-19-01

| Host class | Example | Expected | TC |
|---|---|---|---|
| Verified custom domain | `www.medmaarg.example` | T1/MedMaarg | TC-19-001 |
| Platform default subdomain | `medmaarg.{platform-domain}` | T1/MedMaarg (BRL-TEN-10 exception) | TC-19-005 |
| Unknown host | `unknown.example` | Generic 404, no identifiers | TC-19-002 |
| Upper case and trailing dot | `WWW.MEDMAARG.EXAMPLE.` | Same mapping | TC-19-004 |
| IDN / punycode | `www.मेडमार्ग.example` ↔ `xn--…` | Same mapping as its registered form | TC-19-004 |
| Pending (TXT absent) | newly added | 404 | TC-19-003 |
| Verified then TXT removed | 71 h 59 m / 72 h 0 m 1 s | Still Verified / Revoked | TC-19-006 |

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-001 | Verify a custom domain by TXT token, issue TLS and resolve to T1/MedMaarg | AC-1901-01; FR-A107; BRL-TEN-10 | Tara R12; `www.medmaarg.example`; simulator DNS returns TXT `gev-7f31c2`; ACM sandbox | 1. Add domain. 2. Run verification. 3. GET `https://www.medmaarg.example/` | Verified; certificate issued; response from MedMaarg published snapshot | P0 | T01 | EP | Y | SYS |
| TC-19-002 | Return a generic 404 for an unknown host with no identifiers in body or headers | AC-1901-02; NFR-020 | Host `unknown.example` | 1. GET with Host header. 2. Scan body and headers for tenant/startup IDs, platform name, `X-Tenant` | 404 generic page; 0 identifiers (regex corpus); identical body for 5 random unknown hosts | P0 | T07 | EP | Y | SYS |
| TC-19-003 | Refuse a domain already mapped to another tenant and keep the original mapping | AC-1901-03; BRL-TEN-10 | T1 MedMaarg verified; Priya R12 T2 | 1. T2 adds the same domain | 409 `DOMAIN_IN_USE`; T1 mapping and certificate unchanged; T2 learns no T1 detail beyond "in use" | P0 | T15 | EP | Y | SYS |
| TC-19-004 | Normalize upper case, trailing dot and punycode to the same mapping | AC-1901-04; EDGE-TEXT | Variants listed in the table | 1. GET each | All resolve to the same mapping; cache key identical | P1 | T01 | EP | Y | IT |
| TC-19-005 | Serve the platform default subdomain without custom-domain verification | AC-1901-01; BRL-TEN-10 exception | `medmaarg.{platform-domain}` | 1. GET | Served; canonical link points to the verified custom domain when one exists | P2 | T01 | EP | Y | IT |
| TC-19-006 | Revoke after 72 h without the TXT record and notify the Tenant Admin | AC-1901-05; ERRATA 12 (NT-046 proposed) | TXT removed at t; clock control | 1. Check at t + 71:59:59. 2. At t + 72:00:01. 3. Inspect A106 | 1: Verified (grace). 2: Revoked; traffic 404. 3: High "Domain verification lost" to Tara | P0 | T01 | BVA | Y | SYS |
| TC-19-007 | Deny domain changes to a Marketing Specialist | AC-1901-06; Part 2.3 RBAC | `U-MS1` R05 | 1. POST domain | 403; no DNS call | P1 | T07 | EP | Y | IT |
| TC-19-008 | Resolve a host spoofed through X-Forwarded-Host to the real Host only | AC-1901-02; EG-11 | Host `unknown.example`, `X-Forwarded-Host: www.medmaarg.example` from a non-trusted proxy | 1. GET | 404; forwarded header ignored unless from the CDN trust list | P0 | T07 | EG | Y | SYS |

### 6.3.9.3 Group TC-19-B: Error guessing and boundaries – snapshots, pointer and cache keys (techniques: EG, BVA, EP) · TS-19-02

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-009 | Switch all 48 pages together with no mixed revisions | AC-1902-01; BRL-PUB-02; FR-PUB-01 | Approved `h-site-mm-12`, 48 pages en-IN; rev 11 live | 1. k6 crawls all 48 pages continuously at 20 req/s. 2. Swap pointer mid-crawl | Every crawl pass returns pages all from rev 11 or all from rev 12 (revision meta tag); 0 mixed passes | P0 | T01 | EG | Y | SYS |
| TC-19-010 | Purge only T1/MedMaarg keys and leave AppNAI and T2 hit ratios unchanged | AC-1902-02; NFR-020 | CDN hit ratios measured 10 min before | 1. Publish MedMaarg. 2. Inspect purge request and hit ratios | Purge paths all prefixed `T1/MedMaarg/`; AppNAI and T2 ratios within ± 2% | P0 | T15 | EP | Y | SYS |
| TC-19-011 | Serve the new revision from 3 edge locations within 5 minutes p95 | AC-1902-03; GAP-161; RECOMMENDATION-058 | 20 publishes; synthetic fetchers in 3 regions | 1. Publish. 2. Fetch every 10 s until rev matches | p95 ≤ 5 min over 20 publishes; result recorded in EVR | P1 | T03 | BVA | Y | SYS |
| TC-19-012 | Fail the snapshot build on a portal-only component | AC-1902-04; BRL-PUB-05 | Page includes `PortalInvoiceCard` | 1. Build snapshot | "Portal content cannot be published"; no snapshot object written | P0 | T07 | EP | Y | IT |
| TC-19-013 | Roll back the swap and keep revision 11 live when the CDN purge fails | AC-1902-05; NT-037 | CDN simulator returns 503 to purge | 1. Publish rev 12 | Pointer reverted to rev 11; all edges serve rev 11; NT-037 High | P0 | T18 | EG | Y | SYS |
| TC-19-014 | Serve approved en-IN content for a missing hi-IN page with correct lang attribute | AC-1902-06; DEC-026; I18N-08 | hi-IN not approved for `/offerings/scanner` | 1. GET with `Accept-Language: hi-IN` and `/hi-IN/offerings/scanner` | en-IN approved page; `lang="en-IN"`; no machine-translated draft content | P1 | T13 | EP | Y | SYS |
| TC-19-015 | Deny anonymous listing of the snapshot prefix | AC-1902-07 | S3 snapshot bucket | 1. Anonymous `ListObjectsV2` on prefix. 2. Direct GET object URL | Both AccessDenied; only CDN-signed origin requests succeed | P0 | T07 | EP | Y | SYS |
| TC-19-016 | Keep cache keys distinct per tenant, startup, locale and revision | AC-1902-02; EG-11 | Same slug `/about` on MedMaarg and Alpha Retail hosts | 1. Warm both. 2. Request each host | Each host returns its own page; key includes tenant/startup/locale/revision | P0 | T15 | EG | Y | SYS |
| TC-19-017 | Publish a 500-page site within the purge target | AC-1902-03 (Notes: large site) | 500 pages | 1. Publish | Snapshot build ≤ 10 min [ASSUMPTION-190]; pointer swap atomic; p95 edge freshness ≤ 5 min | P2 | T03 | BVA | Y | SYS |

### 6.3.9.4 Group TC-19-C: Decision table – page configuration validity (technique: DT, EP) · TS-19-03

| Condition | C1 | C2 | C3 | C4 | C5 |
|---|---|---|---|---|---|
| Referenced offering Approved and Available | N | Y | Y | Y | Y |
| Referenced claims approved and unexpired | – | N | Y | Y | Y |
| Management claims carry label and evidence link | – | – | N | Y | Y |
| Schema, links and automated WCAG checks pass | – | – | – | N | Y |
| **Action** | Picker disabled "Not available for promotion" | Validation fails naming claim and expiry | Label enforced at render (validation adds label) | Validation fails with check list | Validated |

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-018 | Validate a draft page with hero, offering grid and demo form | AC-1903-01; FR-A107; CFG-05 | `U-MS1` R05 MedMaarg; page `/hospitals` | 1. Build page. 2. Validate | Schema, links, claims, accessibility pass; Validated | P1 | T01 | DT (C5) | Y | SYS |
| TC-19-019 | Disable a Planned offering in the block picker and reject it via API | AC-1903-02; BRL-MKT-02 | "Doctor Connect" Planned | 1. Open picker. 2. PATCH block with its ID | 1: disabled "Not available for promotion". 2: 422 | P0 | T01 | DT (C1) | Y | IT |
| TC-19-020 | Fail validation on a claim expired at the boundary | AC-1903-03; BRL-MKT-01 | Claim "750+ users" expires 2027-05-31 23:59:59 IST | 1. Validate at 2027-05-31 23:59:58. 2. At 2027-06-01 00:00:00 | 1: passes. 2: fails naming claim and expiry | P0 | T01 | BVA | Y | UT |
| TC-19-021 | Render the Management claim label and evidence link | AC-1903-04; BRL-MKT-03; DEC-021 | Claim "~150 monthly users" management claim | 1. Render block | Label "Management claim" and evidence link present in HTML and accessible name | P0 | T01 | DT (C3) | Y | UT |
| TC-19-022 | Return 409 with block-level diff on concurrent edits | AC-1903-05; NFR-025 | Two authors on rev 7 | 1. Save A. 2. Save B with `If-Match: 7` | 409 with block diff | P1 | T01 | EG | Y | IT |
| TC-19-023 | Return 404 for another startup's site configuration | AC-1903-06; BRL-TEN-04 | Author with MedMaarg grant only | 1. GET EduVerse site config | 404 | P0 | T15 | EP | Y | SYS |
| TC-19-024 | Fail validation when a page block references a deleted offering ID | AC-1903-01 | Offering withdrawn after the block was added | 1. Validate | Fails naming the block; Withdrawn offering not rendered | P1 | T01 | EG | Y | UT |

### 6.3.9.5 Group TC-19-D: State transition – publication lifecycle (technique: ST, BVA) · TS-19-04

Machine: Part 2.3 §2.27.12 (FR-PUB-01). Transition coverage (0-switch) and sneak paths.

| # | From → To | Event / guard | TC |
|---|---|---|---|
| 1 | Draft → Validated | checks pass | TC-19-018 |
| 2 | Validated → Draft | edit | TC-19-034 |
| 3 | Validated → ApprovalPending | submitted | TC-19-025 |
| 4 | ApprovalPending → Draft | rejected | TC-19-034 |
| 5 | ApprovalPending → Approved | approver ≠ author, hash bound | TC-19-025 |
| 6 | Approved → Scheduled | publish time set | TC-19-025 |
| 7 | Scheduled → Published | pointer swap at time | TC-19-025 |
| 8 | Approved → Published | publish now | TC-19-035 |
| 9 | Published → RolledBack | rollback to prior approved hash | TC-19-029 |
| 10 | RolledBack → Published | republish | TC-19-029 |
| 11 | Published → Retired | unpublish | TC-19-036 |
| 12 | Approved → Expired | approval or claim expired | TC-19-037 |
| 13 | Expired → Draft | renew | TC-19-037 |
| ✗ | Draft → Published; Validated → Approved; Retired → Published | sneak paths | TC-19-038 |

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-025 | Preview, approve the exact hash, schedule and publish at 09:00 IST | AC-1904-01; FR-A108; BRL-PUB-01, -03 | Rev 12 ApprovalPending; Ravi R02; clock 2027-06-30 | 1. Open preview (Admin auth + grant). 2. Approve `h-site-mm-12`, schedule 2027-07-01 09:00 IST. 3. Advance to 08:59:59, then 09:00:00 | Preview has `X-Robots-Tag: noindex`; 08:59:59 rev 11 live; 09:00 pointer swaps; NT-037 to author and approver | P0 | T01 | ST | Y | SYS |
| TC-19-026 | Deny the author approving own revision | AC-1904-02; BRL-APR-01 | `U-MS1` authored rev 12 | 1. Approve | 403 `AUTHOR_CANNOT_APPROVE` | P0 | T07 | DT | Y | IT |
| TC-19-027 | Show the expired-grant state to anonymous users and after 24 h | AC-1904-03; BRL-PUB-03 | Preview grant issued 2027-06-30 10:00 IST | 1. Anonymous open. 2. Ravi at 2027-07-01 09:59:59. 3. At 10:00:01 | 1: expired-grant state, `noindex`. 2: preview. 3: expired-grant state | P0 | T07 | BVA | Y | SYS |
| TC-19-028 | Refuse publishing content of revision 13 with the approval of 12 | AC-1904-04; BRL-PUB-01 | Rev 13 created after approval of 12 | 1. Publish | 409 `APPROVAL_HASH_MISMATCH`; pointer unchanged | P0 | T01 | ST | Y | SYS |
| TC-19-029 | Roll back to revision 11 within the purge target and republish 12 later | AC-1904-05; BRL-PUB-02 | Rev 12 live | 1. Rollback to 11. 2. Synthetic fetch. 3. Republish 12 | 11 live ≤ 5 min p95; audited; rev 12 remains Approved (not live); republish → Published | P0 | T01 | ST | Y | SYS |
| TC-19-030 | Block approval on a critical WCAG violation unless an approved waiver exists | AC-1904-06; BRL-PUB-06 | Form field without label | 1. Submit. 2. Add waiver approved by R10 with owner and expiry 2027-08-31. 3. Submit | 1: blocked. 3: approval allowed; waiver listed on the revision | P1 | T08 | DT | Y | SYS |
| TC-19-031 | Show scoped first-party analytics with KPI-26 for MedMaarg only | AC-1904-07; KPI-26; RP-09 | Ravi | 1. Open analytics | Page views, enquiries per page, portal completion for MedMaarg; no other startup; no third-party health pixels (BRL-MKT-06) | P1 | T01 | EP | Y | SYS |
| TC-19-032 | Publish only through the L2 dispatch of the approved hash (DEC-064) | AC-1904-01; AC-1805-04 | Scheduled publish step in a workflow | 1. Run step with approved hash. 2. With another hash | 1: published. 2: Deny `HASH_MISMATCH` | P0 | T01 | DT | Y | SYS |
| TC-19-033 | Publish the same approved hash twice concurrently with one pointer swap | AC-1904-01; Part 6.1 §6.1.3.3 B | Two publish requests within 50 ms | 1. Fire both | One swap; second returns the original result or 409; one audit `publish` | P0 | T16 | EG | Y | IT |
| TC-19-034 | Return to Draft on edit after validation and on rejection | AC-1904-01 | Validated rev; ApprovalPending rev | 1. Edit. 2. Reject | Both → Draft; approval hash cleared | P2 | T01 | ST | Y | UT |
| TC-19-035 | Publish immediately from Approved | AC-1904-01 | Approved rev | 1. Publish now | Published; NT-037 | P1 | T01 | ST | Y | IT |
| TC-19-036 | Retire a published site and serve 404 afterwards | AC-1904-05 | Published landing page | 1. Unpublish | Retired; 404; purge of its keys only | P1 | T01 | ST | Y | SYS |
| TC-19-037 | Expire an approval when a referenced claim expires and renew to Draft | AC-1903-03, AC-1904-04; BRL-APR-03 | Approved rev referencing claim expiring 2027-06-30 | 1. Advance to 2027-07-01. 2. Renew | 1: Expired; cannot publish. 2: Draft | P0 | T01 | ST | Y | SYS |
| TC-19-038 | Reject sneak paths Draft → Published, Validated → Approved, Retired → Published | AC-1904-04 | Revisions in each state | 1. Attempt | 409 `INVALID_TRANSITION`; no pointer change | P0 | T01 | ST | Y | UT |

### 6.3.9.6 Group TC-19-E: Equivalence partitions – homepage and directory (techniques: EP, BVA) · TS-19-05

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-039 | Render the homepage from the approved snapshot within LCP 2.5 s on 360 px 4G | AC-1905-01; FR-W01; RECOMMENDATION-028 | Lighthouse CI mobile profile; 360 px | 1. Load homepage 5 runs | Hero, search, featured startups, "For businesses (SaaS)" band; LCP p75 ≤ 2.5 s | P1 | T03 | BVA | Y | SYS |
| TC-19-040 | Filter the directory by sector and country with accurate facet counts | AC-1905-02; FR-W02; SR-06 | Healthcare + India | 1. Apply filters | MedMaarg listed; counts include only published businesses | P1 | T01 | EP | Y | E2E |
| TC-19-041 | Show the empty state with reset | AC-1905-03 | Filter "Mining" + "Iceland" | 1. Apply | "No published businesses match" + reset | P2 | T01 | EP | Y | E2E |
| TC-19-042 | Hide unpublished and non-opted-in tenants from directory and search index | AC-1905-04; BR-S130 | AgriNova unpublished; Alpha Retail not opted in | 1. Search names. 2. Query the directory index directly | Neither appears in UI, API or index | P0 | T15 | EP | Y | SYS |
| TC-19-043 | Return 429 at the 31st search per IP per minute | AC-1905-05; NFR-022; Part 2.4 §2.35.3 | One IP | 1. 30 searches in 60 s. 2. 31st | 30 × 200; 31st 429 with `Retry-After`; no stack trace | P1 | T07 | BVA | Y | SYS |
| TC-19-044 | Expose no internal metrics, owner names or Admin routes in public responses | AC-1905-06; NFR-001 | Directory and homepage APIs | 1. Diff responses against the public schema allowlist | 0 fields outside allowlist; 0 `/admin` strings | P0 | T07 | EP | Y | CT |
| TC-19-045 | List an opted-in, verified external tenant | AC-1905-04; BR-S130 | T3 opts in and has a verified site | 1. Search | T3 listed with its own branding | P2 | T01 | EP | Y | SYS |

### 6.3.9.7 Group TC-19-F: Equivalence partitions – startup site, catalogue and offering details (technique: EP) · TS-19-06

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-046 | Show brand, units, featured offerings, locations and last-updated date | AC-1906-01; FR-W03 | `www.medmaarg.example` | 1. Open | Elements present; "Last updated 2027-07-01" | P1 | T01 | EP | Y | E2E |
| TC-19-047 | Filter the catalogue by delivery model and availability with badges | AC-1906-02; FR-W04 | On-site + Available | 1. Filter | Only Approved and Available offerings with badges | P1 | T01 | EP | Y | E2E |
| TC-19-048 | Exclude Planned offerings from catalogue, search and sitemap | AC-1906-03; BRL-MKT-02 | "Doctor Connect" Planned | 1. Catalogue. 2. Site search. 3. `/sitemap.xml` | Absent in all three | P0 | T01 | EP | Y | SYS |
| TC-19-049 | Show offering details with claims, evidence links and management-claim label | AC-1906-04; FR-W05; DEC-021 | "Wellness Scanner" | 1. Open details | Specs, eligibility, delivery, claims with evidence; "750+ users" labelled "Management claim" | P0 | T01 | EP | Y | E2E |
| TC-19-050 | Contain no diagnostic claim on wellness offering pages | AC-1906-05; BR-S066; BRL-AI-05 | Scanner, Planner, Advisor pages | 1. Run the diagnostic-claim lexicon scan on rendered text | "Wellness guidance" statement present; 0 lexicon hits ("diagnose", "cure", "treat" …) | P0 | T19 | EG | Y | CT |
| TC-19-051 | Return 404 for an AppNAI offering URL on the MedMaarg host | AC-1906-06; BRL-TEN-10 | AppNAI slug | 1. GET on MedMaarg host | 404 | P0 | T15 | EP | Y | SYS |
| TC-19-052 | Hide an offering within the purge target when it is withdrawn | AC-1906-02; BRL-SCR-04 | Offering moves Available → Withdrawn | 1. Republish snapshot. 2. Fetch | Removed from catalogue ≤ 5 min p95 | P1 | T01 | BVA | Y | SYS |

### 6.3.9.8 Group TC-19-G: Boundary values – public and private pricing (techniques: BVA, EP) · TS-19-07

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-053 | Show approved public price with tax basis and validity | AC-1907-01; FR-W06; BRL-QTE-01 | `pv-12` "INR 150.00 per kg, excl. GST, valid until 2027-09-30" | 1. Open pricing 2027-09-30 23:59:59 IST | Text exact incl. price revision | P1 | T01 | BVA | Y | E2E |
| TC-19-054 | Replace an expired price with "Contact us" at the boundary | AC-1907-02; BRL-QTE-05 | Clock 2027-10-01 00:00:00 IST | 1. Open page | "Contact us for current pricing" + request-quote CTA; expired price absent from HTML and snapshot | P0 | T01 | BVA | Y | SYS |
| TC-19-055 | Show negotiated price only after sign-in with a grant and never in the CDN | AC-1907-03; BRL-PUB-05; CA-PORTAL | Neha grant `PL-GreenMart` | 1. Sign in; open price list. 2. Inspect response cache headers and CDN logs | Negotiated price shown; `Cache-Control: private, no-store`; 0 CDN cache entries for the path | P0 | T07 | EP | Y | SYS |
| TC-19-056 | Return 404 for another buyer's price list | AC-1907-04; BRL-TEN-04 | `PL-FreshCo` | 1. GET | 404 | P0 | T15 | EP | Y | SYS |
| TC-19-057 | Show each price in its own currency with no FX conversion | AC-1907-05; BRL-QTE-04; DEC-027 | INR and USD price lists | 1. Render | Own currencies; no converted amount | P1 | T01 | EP | Y | UT |
| TC-19-058 | Never include private prices in the public snapshot build | AC-1907-03; BRL-PUB-05 | Snapshot build with price block | 1. Build; scan artefacts for private price values | 0 private values | P0 | T07 | EG | Y | CT |

### 6.3.9.9 Group TC-19-H: Industry and solution pages (techniques: EP, DT) · TS-19-08

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-059 | Render an industry page with matched offerings, evidence references and CTA | AC-1908-01; FR-W07 | `/industries/corporate-hr` | 1. Open | Use cases, matched approved offerings, outcome evidence refs, enquiry CTA | P2 | T01 | EP | Y | E2E |
| TC-19-060 | Block a page revision whose outcome statement lacks evidence | AC-1908-02; BRL-MKT-01 | Outcome text without evidence ID | 1. Validate | Validation blocks | P1 | T01 | DT | Y | UT |
| TC-19-061 | Route EduVerse school CTAs only to EduVerse education enquiry | AC-1908-03; DEC-052; FR-DM-04 | EduVerse "Schools" page | 1. Inspect CTA targets; submit | Target is EduVerse intake; never AppNAI project intake | P1 | T01 | DT | Y | E2E |
| TC-19-062 | Return 404 for a draft industry slug | AC-1908-04; BRL-PUB-01 | Draft slug `/industries/mining` | 1. GET | 404 | P0 | T07 | EP | Y | SYS |

### 6.3.9.10 Group TC-19-I: Equivalence partitions and boundaries – portal identity (techniques: EP, BVA, EG) · TS-19-09

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-063 | Register by invitation, enrol TOTP and receive only an HttpOnly session cookie | AC-1909-01; FR-W21; DEC-019 | Invite `INV-PT-0117` valid 7 days | 1. Register. 2. Enrol TOTP. 3. Inspect cookies and `window` storage | Cookie `HttpOnly; Secure; SameSite=Strict`; no token in localStorage, sessionStorage or JS-readable cookies | P0 | T07 | EP | Y | E2E |
| TC-19-064 | Reject an investor-audience token at the portal | AC-1909-02; DEC-058; BRL-TEN-02 | Valid token for investor audience | 1. Call portal BFF | 401; no records | P0 | T07 | EP | Y | SYS |
| TC-19-065 | Recover access through the portal client flow without granting Admin access | AC-1909-03 | Dr Rao | 1. Recovery. 2. Call Admin BFF with the new session | Recovery succeeds; Admin 401 | P0 | T07 | EP | Y | SYS |
| TC-19-066 | Reject an expired invitation at the 7-day boundary | AC-1909-04 | Invite issued 2027-06-01 10:00 IST | 1. Register at 2027-06-08 09:59:59. 2. Fresh invite: at 10:00:01 | 1: allowed. 2: "This invitation has expired. Ask your contact for a new one." | P1 | T01 | BVA | Y | SYS |
| TC-19-067 | Lock the account at the 10th failed sign-in in 10 minutes, not the 9th | AC-1909-05 | 9 failures then 1 more within 10 min; separate run with 10th at 10:01 | 1. Attempt sign-ins | 9: not locked. 10 within window: locked, accessible message, audit. 10th outside window: not locked | P1 | T07 | BVA | Y | SYS |
| TC-19-068 | Show the empty state to a registered user without grants | AC-1909-06; ABAC-09 | Self-registered user | 1. Sign in | Empty state; 0 records from any tenant | P0 | T15 | EP | Y | E2E |
| TC-19-069 | Accept passkey sign-in and password-manager autofill (no cognitive test) | AC-1909-01; WCAG 3.3.8 | IdP passkey support (verify at Sprint 0) | 1. Sign in with passkey. 2. With autofill | Both succeed; no CAPTCHA puzzle in the flow | P1 | T08 | EP | Y | E2E |
| TC-19-070 | Revoke the portal session within 60 s of membership/grant expiry | AC-1909-01; BRL-TEN-07 | Contact deactivated at t | 1. API call at t + 61 s | 401 | P0 | T07 | BVA | Y | SYS |
| TC-19-071 | Show an accessible timeout warning 60 s before session expiry with extension | AC-1909-01; WCAG 2.2.1 | Playwright clock | 1. Idle until warning | Warning ≥ 60 s before expiry; "Stay signed in" extends | P1 | T08 | BVA | Y | E2E |

### 6.3.9.11 Group TC-19-J: Equivalence partitions – customer dashboard (technique: EP) · TS-19-10

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-072 | Show own summary cards with last-updated time | AC-1910-01; FR-W22; RP-29 | Neha; 1 offering, 1 task, milestone 2027-07-12, unpaid verified INR 200.00 | 1. Sign in | Cards exact; last-updated time | P1 | T01 | EP | Y | E2E |
| TC-19-073 | Never present unverified items as facts | AC-1910-02 | Proof pending | 1. View card | "Proof received – verification pending" | P0 | T01 | EP | Y | E2E |
| TC-19-074 | Separate relationships with two startups | AC-1910-03; ABAC-09 | Neha's company is also a MedMaarg customer | 1. View dashboard | Two sections; no merged totals | P0 | T15 | EP | Y | SYS |
| TC-19-075 | Exclude staff fields from the dashboard DTO | AC-1910-04; CA-PORTAL | — | 1. Inspect DTO vs schema | No deal stage, owner notes, margins, internal tasks | P0 | T07 | EP | Y | CT |
| TC-19-076 | Remove a revoked order at the next request and 404 on direct access | AC-1910-05; BRL-TEN-04 | Grant on `SO-2027-0310` revoked | 1. Refresh. 2. GET order | Not listed; 404 | P0 | T15 | EP | Y | SYS |
| TC-19-077 | Render 200 items with mobile bottom tab bar at 360 px | AC-1910-01 (Notes) | 200 tasks/invoices | 1. Load at 360 px | Paginated; no horizontal scroll; bottom tab bar operable | P2 | T10 | BVA | Y | E2E |

### 6.3.9.12 Group TC-19-K: Accessibility and performance budgets (techniques: EP, BVA) · TS-19-11

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-078 | Show an accessibility statement per startup with target, limitations, review date and contact | AC-1911-01; GAP-164 | MedMaarg footer link | 1. Open | All four elements; statement approved by R10 | P1 | T08 | EP | Y | E2E |
| TC-19-079 | Reach every interactive element by keyboard with visible, unobscured focus and 24×24 targets | AC-1911-02; NFR-023 | W01–W07, W21, W22 | 1. Keyboard script per page. 2. Target-size script | All pass | P1 | T08 | EP | Y | E2E |
| TC-19-080 | Reflow at 320 CSS px and remain usable at 200% text | AC-1911-03 | Same pages | 1. Viewport 320; text zoom 200% | No horizontal scroll except tables in containers | P1 | T08 | BVA | Y | E2E |
| TC-19-081 | Block publication of an image without alt text unless waived | AC-1911-04; BRL-PUB-06 | Offering image without alt | 1. Validate | Fails; approval blocked | P1 | T08 | DT | Y | UT |
| TC-19-082 | Fail CI when a route exceeds 150 KB gzip or LCP 2.5 s | AC-1911-05; RECOMMENDATION-028; LT-12 | Test branch adds 160 KB library to `/offerings` | 1. Run Lighthouse CI and bundle budget | Job fails naming `/offerings`; 150 KB exactly passes | P1 | T03 | BVA | Y | CT |
| TC-19-083 | Attach NVDA + Chrome and VoiceOver + Safari passes to release evidence | AC-1911-06 | Top public journeys | 1. Execute scripted passes | Results attached to EVR | P1 | T08 | UC | N (assistive technology) | E2E |
| TC-19-084 | Deny the page author approving own accessibility waiver | AC-1911-07; BRL-APR-01 | Author requests contrast waiver | 1. Author approves. 2. R10 non-author approves | 1: 403. 2: approved with owner and expiry | P1 | T07 | DT | Y | IT |
| TC-19-085 | Keep CLS ≤ 0.1 and INP proxy within budget on top routes | AC-1911-05; Part 2.5 §2.48 | Top 10 routes per seed startup | 1. Lighthouse CI | CLS ≤ 0.1; TBT within budget | P2 | T03 | BVA | Y | CT |
| TC-19-086 | Set correct lang attributes for en-IN and hi-IN content | AC-1911-03 (LOC); DEC-026 | hi-IN approved page | 1. Render | `lang="hi-IN"` on html; mixed-language spans marked | P2 | T13 | EP | Y | UT |

### 6.3.9.13 Group TC-19-L: Cross-boundary and abuse controls (techniques: EP, BVA, EG) · TS-19-12

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-087 | Fail the build if Admin routes, API paths or components appear in public or portal bundles | AC-1912-01; NFR-001 | Built bundles | 1. Scan with route manifest and string patterns. 2. Inject `/admin/` import in a test branch | 1: 0 matches. 2: build fails | P0 | T07 | EG | Y | CT |
| TC-19-088 | Deny Admin API calls from a portal session regardless of CORS | AC-1912-02 | Neha session | 1. GET `/api/v1/commercial/admin/deals` with forged `Origin` | 401/403; CORS headers irrelevant | P0 | T07 | EP | Y | SYS |
| TC-19-089 | Return 404 for a T1 order requested by a T2 customer and log both tenant IDs | AC-1912-03; AP-10; NFR-032 | FX-TEN-2; T2 customer with T2 order grant | 1. GET T1 order ID | 404; security log with both tenant IDs | P0 | T15 | EP | Y | SYS |
| TC-19-090 | Reject a replayed cached request 30 s after grant revocation | AC-1912-04; AP-10 | Dr Rao grant revoked at t | 1. Replay at t + 30 s | 404; no data | P0 | T15 | BVA | Y | SYS |
| TC-19-091 | Apply 30/min per IP and 600/min per site limits with bot challenge on forms | AC-1912-05; NFR-022; LT-07 | One IP 30 then 31 req/min; 60 IPs × 10 req/min then 601st request | 1. Send | 31st per IP → 429; site total 601st → 429; form submissions challenged; abuse metric increments | P0 | T07 | BVA | Y | SYS |
| TC-19-092 | Send strict security headers on public responses | AC-1912-06 | All public routes | 1. Inspect headers | CSP (no `unsafe-inline` scripts), HSTS ≥ 1 year with includeSubDomains, `nosniff`, `frame-ancestors 'none'` | P0 | T07 | EP | Y | CT |
| TC-19-093 | Block provider calls from browser code via CSP connect-src | AC-1912-06; NFR-004 | CSP and bundle scan | 1. Attempt fetch to a provider host from public page | Blocked by CSP; no provider key patterns in bundles | P0 | T07 | EG | Y | CT |
| TC-19-094 | Serve no portal response from the CDN cache | AC-1912-02; BRL-PUB-05; NFR-020 | Portal routes behind CDN | 1. Request twice; inspect `X-Cache` | `Miss` always; `Cache-Control: private, no-store` | P0 | T07 | EP | Y | SYS |
| TC-19-095 | Run the public surface through an authenticated and anonymous ZAP scan | AC-1912-01…06; Part 6.1 §6.1.14.2 | ZAP baseline (G3), full (G4) | 1. Scan | 0 high/critical | P0 | T07 | EG | Y | SYS |

### 6.3.9.14 Group TC-19-M: Monitoring (techniques: EP, BVA) · TS-19-13

| ID | Title | Links | Pre-conditions and data | Steps | Expected | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-19-096 | Detect served-hash drift within one 5-minute synthetic cycle | AC-1913-01; FR-A108 | Edge serving stale rev 11 after rev 12 published | 1. Run synthetic checks | High alert within ≤ 5 min | P1 | T21 | BVA | Y | SYS |
| TC-19-097 | Chart TTFB p95 per host against 800 ms origin and 200 ms cached with burn alerts | AC-1913-02; DEC-018 | LT-02 run | 1. Inspect A014 | Both series per host; burn alert fires when injected latency 900 ms | P1 | T21 | BVA | Y | SYS |
| TC-19-098 | Send NT-037 High with the failing step on pointer-swap failure | AC-1913-03; NT-037 | Fault injection at pointer swap | 1. Publish | NT-037 to author and approver naming step "pointer_swap" | P1 | T21 | EG | Y | IT |
| TC-19-099 | Compute KPI-26 from public/portal events, not CRM stages | AC-1913-04; KPI-26 | Events with CRM pipeline disabled | 1. Compute | KPI-26 unchanged by CRM outage | P2 | T01 | EP | Y | UT |
| TC-19-100 | Scope monitoring to the Startup Head's hosts | AC-1913-05 | Ravi | 1. Open monitoring | MedMaarg hosts only | P1 | T15 | EP | Y | SYS |
| TC-19-101 | Alert when a verified host's certificate is within 14 days of expiry | AC-1913-01; ERRATA 12 [ASSUMPTION-190] | Certificate expiry in 14 d 0 h vs 14 d + 1 h | 1. Run check | Alert at ≤ 14 days only | P2 | T21 | BVA | Y | SYS |

---

