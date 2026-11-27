# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 6 (Batch 6.2, file b), Test Scenarios and Test Cases: EP-12 to EP-14

| Field | Value |
|---|---|
| Document | Application Blueprint, Part 6 (Batch 6.2, file b of 2): test scenarios (TS) and test cases (TC) for **EP-12 Campaigns, landing pages, ads and referrals**, **EP-13 Proposal, quote, negotiation and contract** and **EP-14 Bids, orders and fulfilment (vertical routes)**, plus the batch-wide coverage, totals, tag register and quality gate. File a (`Part-06-2a_Test_Cases_EP08-EP11.md`) covers EP-08 to EP-11 and defines the conventions used here (§6.2.1) |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | Part 6.1 (§6.1.11 techniques and worked examples BVA-D01…D14, §6.1.12 conventions), Part 6.2 file a (§6.2.1 conventions, precondition profiles PP-01…PP-07, adapter battery B1–B7, journey register), Part 5.2 (US-1201…US-1412 and AC-1201-01…AC-1412-05), Part 2.1 (FR register incl. FR-DM-01…04, FR-CSM-01), Part 2.3 (BRL-MKT, BRL-QTE, BRL-APR, BRL-CTR, BRL-BID, BRL-ORD, BRL-FIN; state machines §2.27.4–§2.27.8, §2.27.13), Part 0A (DEC-022, DEC-023, DEC-027, DEC-038, DEC-045, DEC-046, DEC-052, DEC-053, DEC-054, DEC-064) |
| Roles applied | QA Lead (primary), Business Systems Analyst, Principal Engineer, FinOps Lead, Security/Compliance/AI Governance Lead, Lead UX/UI Designer, Data Architect/DBA, Product Owner |
| Tag ranges used | RECOMMENDATION-075…076 · ASSUMPTION-185…187 (register in §6.2.13.3) |

**Acronyms used in this file.** As in file a, plus: FX foreign exchange · GST Goods and Services Tax (CGST central, SGST state, IGST integrated) · GSTIN GST identification number · HSN/SAC Harmonised System of Nomenclature / Services Accounting Code · LUT Letter of Undertaking (zero-rated export) · NPOP National Programme for Organic Production · RFQ request for quotation · SKU stock-keeping unit · UTR unique transaction reference.

**Time-sensitive facts.** GST rates (fixtures use an illustrative 18% = 9% + 9% for SAC 998314 and HSN 0910, ASSUMPTION-169), e-sign legal validity under the IT Act 2000, e-sign provider and ads provider sandboxes, Meta/Google Ads API behaviour and Indian tender-portal practice are **unverified; verify at time of implementation (as of 27 Nov 2026)** (DEC-042). Money values in TCs are fixtures computed with Decimal ROUND_HALF_UP (DEC-027); no price is stated as fact.

---

## 6.2.8 Inputs for file b

### 6.2.8.1 Story fixture pack EDGE-P52, part 2 [ASSUMPTION-187]

| Area | Keys (startup) | Values used by the TCs |
|---|---|---|
| Campaigns and pages | CMP-9 (MedMaarg email campaign), segment "Odisha clinics - HR heads" (1,200 contacts), C-777, landing page LP-14 "OrganicSpec bulk turmeric buyers" (offer ends 2026-12-31 23:59:59 IST), form schema F-RFQ v2, campaign code CMP-9-LI | Simulation fixture: 842 eligible; excluded 211 (BRL-ELG-02), 97 (BRL-ELG-05), 50 (BRL-ELG-09); estimated cost INR 412.50; MedMaarg campaign budget INR 2,000.00 available |
| Ads | AD-3 (OrganicSpec), ads account `ads-os` (currency INR), `ads-us` (currency USD) | Daily cap INR 500.00; reserved INR 10,000.00 monthly; expected daily spend INR 300.00 |
| Referrals | PRT-22 (active partner), PRT-99 (inactive), REF-101 "Lotus Hospitals, Cuttack" (MedMaarg) | Commission proposal 5.00% |
| Proposals and quotes | D-210 (MedMaarg deal, Sunrise Clinics, demo Completed), template MM-PILOT v2, offering "Scanner corporate pilot", PV-7 (valid until 2026-11-30 23:59:59 IST), P-55; OrganicSpec price list PL-OS-12 with SKU TUR-A "Turmeric finger, Grade A" INR 150.00/kg, units {kg}, min 1 max 5,000 kg, direct cost INR 80.00/kg; OS-RICE-25KG INR 2,400.00 per bag (cost 1,300.00); GIN-B ginger INR 120.00/kg (cost 60.00); USD list PL-OS-USD-2 (TUR-A USD 2.00/kg, OS-RICE-25KG USD 30.00, GIN-B USD 1.50/kg) for export quotes; Q-88 rev 2 | Q-88 rev 2 = 2 kg × 150.00 × 0.90 = 270.00 + CGST 24.30 + SGST 24.30 = **318.60 INR**, valid until 2026-12-27 23:59:59 IST |
| Contracts | CT-14 "EduVerse x Kalinga College" MoU from template EV-MOU v4, effective 2027-01-01, expiry 2027-12-31; signatory `registrar@kalinga.example` with authority evidence AL-3 | Legally approved hash `sha256:ct14a` |
| Bids | B-31 tender "GeM/2026/B/5501" (AppNAI), deadline 2030-06-01 09:00 UTC, buffer 24 h, budget INR 45,00,000.00; T2 startup "B-Tech" with capability `bid_desk` | Checklist template v3: ISO 27001, turnover ≥ INR 2 crore FY2025-26, India delivery, CMMI Level 3, local office in Delhi |
| Orders | SO-71 (Sell, buyer "Agro Traders", Odisha), PO-15 (Buy, supplier "Koraput Organic FPO"), SKU TUR-A available 50 kg; portal users `buyer@agro.example` (grant on SO-71), `cfo@agro.example` (no grant) | Tolerance policy default 0%; test policy 2% on a 100 kg line |

### 6.2.8.2 Test-oracle interpretations for EP-12 to EP-14 [ASSUMPTION-186]

| # | Topic | Interpretation used by the oracle | Affected TCs |
|---|---|---|---|
| O-12 | MFA freshness (ABAC-11 "within the last 12 h") | Fresh when age ≤ 12 h 00 m 00 s; step-up from 12 h 00 m 01 s | TC-13-102…104 |
| O-13 | Business day and approval SLA (BRL-APR-10) | Business days Monday–Saturday excluding India public holidays in CFG-32; business hours 10:00–18:00 IST (DEC-044); "1 business day" = the same business-clock time on the next business day; time outside business hours starts counting at the next 10:00 | TC-13-011, TC-13-071 |
| O-14 | Validity "until a date" (BRL-QTE-05) | Valid through 23:59:59 IST of that date; default validity = approval date + 30 calendar days | TC-13-029, TC-13-058 |
| O-15 | Inclusive limits | Commission 0.00–50.00% inclusive; concession limit inclusive (5.00% is within a 5.00% limit); contract value ≥ ₹10,00,000.00 inclusive (BRL-APR-06) | TC-12-070, TC-13-065, TC-13-081, TC-13-082 |
| O-16 | Ad spend thresholds (BRL-MKT-05) | Anomaly when daily spend is strictly greater than 150.00% of expected; monthly cap pause when spend ≥ 100.00% of the monthly cap | TC-12-051, TC-12-052, TC-12-057 |
| O-17 | Duplicate referral window (AC-1209-04) | 90 × 24 h from receipt of the first referral, boundary instant inside the window | TC-12-065 |
| O-18 | Renewal notice (BRL-CTR-05) | Notice date = expiry date − 60 days at 00:00 IST (expiry 2027-12-31 → 2027-11-01) | TC-13-077 |
| O-19 | Reservation expiry (ASSUMPTION-166) | Released when an Issued Sell order is not Acknowledged within 14 × 24 h of issue | TC-14-065 |
| O-20 | Holdout (AC-1204-04) | Holdout size = floor(eligible × percentage ÷ 100); members = contacts with the lowest SHA-256(contact ID + campaign salt); identical on re-simulation | TC-12-027 |
| O-21 | Tender deadline evidence (CONFLICT-133) | The portal timestamp on the evidence, not the recording time, is compared with the absolute deadline; Startup Head acknowledgement for inside-buffer evidence may be recorded after the deadline | TC-14-022…024 |

### 6.2.8.3 Risk mapping for file b

| Epic | Risk areas (§6.1.4.3) | Default scenario priority | Notes |
|---|---|---|---|
| EP-12 | RA-20 (P0), RA-14 (P0) for landing pages, RA-03 for execution-time eligibility | **P0** | BR-M39 (ads) and BR-M42 are Could/Should, but spend caps and consent rules keep their TCs at P0 (unapproved spend, BRD §11) |
| EP-13 | RA-05 (P0), RA-06 (P0), RA-10 (P0), RA-15 (P0) for portal review | **P0** | Depth D4 for pricing (mutation score ≥ 85%, §6.1.9.6) |
| EP-14 | RA-08 (P0), RA-09 (P0), RA-07 (P0) for postings, RA-18 for imports | **P0** | Full synthetic deal per route is a W4 exit criterion (§6.1.5.2) |

---

## 6.2.9 EP-12 Campaigns, landing pages, ads and referrals

Stories US-1201…US-1210 (49 AC). FRs: FR-A056…FR-A061, FR-A064, FR-W10, FR-W20; cross-cutting FR-PUB-01, FR-ADP-01, FR-STD-02. Agent exercised deterministically: AG-018 (landing copy mode). Campaign state machine Part 2.3 §2.27.13.

### 6.2.9.1 Test scenarios

| TS ID | Scenario | Linked stories / FR | Risk area · Priority | TCs |
|---|---|---|---|---|
| TS-12-01 | Landing pages built only from approved blocks, offerings and form schemas, with expiring noindex previews | US-1201 · FR-A056 | RA-20, RA-14 · **P0** | TC-12-001…007 |
| TS-12-02 | Landing pages approved after accessibility, privacy and claims checks; published and rolled back atomically | US-1202 · FR-A057, FR-PUB-01 | RA-14 · **P0** | TC-12-008…014 |
| TS-12-03 | Public campaign page captures consented, deduplicated leads with first-party attribution and no sensitive events to pixels | US-1203 · FR-W10 | RA-20, RA-12 · **P0** | TC-12-015…022 |
| TS-12-04 | Campaign builder simulates a lawful audience and cost before submission | US-1204 · FR-A058 | RA-20, RA-03, RA-11 · **P0** | TC-12-023…031 |
| TS-12-05 | Campaign approval binds the version and reserves budget; execution rechecks every recipient and auto-pauses | US-1205 · FR-A059 | RA-20, RA-03, RA-05 · **P0** | TC-12-032…041 |
| TS-12-06 | Ads adapter is disabled until the budget is approved and passes the conformance battery | US-1206 · FR-A060, FR-A061, FR-ADP-01 | RA-20 · **P0** | TC-12-042…049 |
| TS-12-07 | Ads dashboard shows spend against caps and pauses on anomalies | US-1207 · FR-A060 | RA-20 · **P0** | TC-12-050…054 |
| TS-12-08 | Ads launch only within the effective cap; 100% cap and emergency stop pause spend | US-1208 · FR-A061 | RA-20 · **P0** | TC-12-055…061 |
| TS-12-09 | Partner referral form collects minimum data and never enables outreach before the referred party's consent | US-1209 · FR-W20 | RA-03, RA-17 · **P0** | TC-12-062…067 |
| TS-12-10 | Referral approvals assign qualified opportunities and record commission without any payout path | US-1210 · FR-A064 | RA-05, RA-07 · **P0** | TC-12-068…073 |
| TS-12-11 | Campaign state machine, pairwise campaign matrix and end-to-end journeys | US-1203…US-1205 · §2.27.13 | RA-20 · **P0** | TC-12-074…083 |

### 6.2.9.2 Test cases

#### Group TC-12-A: Equivalence partitioning and boundary values – landing page builder (US-1201)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-12-001 | Build a draft page with offer, form schema, consent notice and a 24 h noindex preview | TS-12-01 · US-1201 AC-1201-01 · FR-A056; BRL-PUB-03 | Pre: PP-01, OrganicSpec, R05 of OrganicSpec. Data: LP-14 with hero, offer (ends 2026-12-31), F-RFQ v2, consent notice PN-5 | Save; generate preview | Page `Draft`; preview URL with grant expiring CLK-0 + 24 h; response header `X-Robots-Tag: noindex` and meta robots noindex | P1 | T01 | EP | Y | SYS |
| TC-12-002 | Block referencing a Planned offering fails validation | TS-12-01 · US-1201 AC-1201-02 · BRL-MKT-02 | Data: offer block bound to a Planned SKU | Validate | 422 BRL-MKT-02; not `Validated` | P1 | T19 | EP | Y | SYS |
| TC-12-003 | MedMaarg page cannot enable a third-party ad pixel | TS-12-01 · US-1201 AC-1201-03 · BRL-MKT-06; BRL-ELG-14 | Pre: MedMaarg R05. Data: tracking setting `third_party_pixel = meta` | Save | 422 "First-party analytics only for health-related pages (BRL-MKT-06)" | P0 | T19 | EP | Y | SYS |
| TC-12-004 | Preview valid at 23 h 59 m 59 s, expired at 24 h; anonymous access refused | TS-12-01 · US-1201 AC-1201-04 · BRL-PUB-03 | Data: preview created 2026-12-01 10:00:00 IST | Open as Admin at 2026-12-02 09:59:59 and 10:00:00; open without Admin session | 09:59:59 renders; 10:00:00 expired state; anonymous 401/404 with no content | P0 | T07 | BVA | Y | SYS |
| TC-12-005 | Growth manager cannot edit landing pages | TS-12-01 · US-1201 AC-1201-05 | Pre: R03 OrganicSpec | PATCH page | 403; NSE | P1 | T07 | EP | Y | SYS |
| TC-12-006 | Tracking-consent field is mandatory in every form schema used on a page | TS-12-01 · US-1201 Notes · CA-INTAKE | Data: form schema without the tracking consent field | Validate | 422 "Tracking consent field required" | P1 | T19 | EP | Y | SYS |
| TC-12-007 | or-IN page variant uses its own approved translation | TS-12-01 · US-1201 D8 · DEC-026 | Data: or-IN variant machine-translated, unapproved | Validate or-IN variant | Variant blocked until approved; en-IN variant unaffected | P3 | T13 | EP | Y | SYS |

#### Group TC-12-B: Decision table – landing page approval and publication (US-1202)

| Rule | Accessibility (0 critical) | Privacy review by R10 | Claims valid | Approver ≠ author | Publish hash = approved hash | Result | TC |
|---|---|---|---|---|---|---|---|
| L1 | Y | Y | Y | Y | Y | Approved → Published (pointer swap + purge) | TC-12-008 |
| L2 | N | – | – | – | – | Approve disabled, violations listed | TC-12-009 |
| L3 | Y | Y | Y | Y | N | 409 | TC-12-010 |
| L4 | Y | Y | Y | N | – | 403 | TC-12-012 |
| L5 | Y | N | Y | Y | – | Approve disabled "privacy review pending" | TC-12-014 |

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-12-008 | Approve exact hash and publish with atomic pointer swap and tenant-keyed purge (L1) | TS-12-02 · US-1202 AC-1202-01 · FR-A057; BRL-PUB-01, BRL-PUB-02, BRL-MKT-01 | Pre: PP-01, OrganicSpec, R05L. Data: LP-14 checks pass, hash `sha256:9a1b` | Approve; publish; GET public URL on `organicspec.example` | Pointer swapped once; purge request keyed by tenant/startup/locale/revision; page served at new revision | P0 | T01 | DT | Y | SYS |
| TC-12-009 | Two critical axe violations disable Approve (L2) | TS-12-02 · US-1202 AC-1202-02 · BRL-PUB-06 | Data: LP-14 with 2 critical violations | Open approval; POST approve | Button disabled with list; API 422 `ACCESSIBILITY_GATE` | P0 | T08 | DT | Y | SYS |
| TC-12-010 | Publish request with a mismatched hash returns 409 (L3) | TS-12-02 · US-1202 AC-1202-03 · BRL-PUB-01 | Data: hash `sha256:0000` | POST publish | 409; live page unchanged | P0 | T07 | DT | Y | SYS |
| TC-12-011 | Rollback to the prior approved hash with NT-037 | TS-12-02 · US-1202 AC-1202-04 · BRL-PUB-02; NT-037 | Data: LP-14 rev 2 published, rev 1 prior approved | Roll back | Visitors see rev 1 after purge; never mixed (revision header = body hash); NT-037 sent | P0 | T01 | EG | Y | SYS |
| TC-12-012 | Author cannot approve own page (L4) | TS-12-02 · US-1202 AC-1202-05 · BRL-APR-01 | Pre: R05 author | POST approve | 403; NSE | P0 | T07 | DT | Y | SYS |
| TC-12-013 | Approval expiry is the earlier of offer end and 90 days | TS-12-02 · US-1202 Notes · BRL-APR-03 | Data: approved 2026-12-01 10:00 IST; offer ends 2026-12-31 23:59:59 IST | Read approval; advance clock to 2027-01-01 00:00:00 IST | Expiry = 2026-12-31 23:59:59 IST (not 2027-03-01); page shows "Offer ended" state; approval `Expired` | P1 | T01 | BVA | Y | SYS |
| TC-12-014 | Approve disabled until R10 privacy review is recorded (L5) | TS-12-02 · US-1202 AC-1202-01 · DEC-038 | Data: no privacy review | POST approve | 422 `PRIVACY_REVIEW_PENDING` | P0 | T19 | DT | Y | SYS |

#### Group TC-12-C: Equivalence partitioning and error guessing – public campaign landing page (US-1203)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-12-015 | Enquiry with campaign code creates one attributed lead | TS-12-03 · US-1203 AC-1203-01 · FR-W10; CA-INTAKE; NX-01 | Pre: PP-02 `organicspec.example`. Data: URL `?utm_campaign=CMP-9-LI`; RFQ form; consent PN-5 | Submit | One lead; AttributionEvent CMP-9-LI (first-party); NX-01 queued only if eligible (PDP) | P1 | T01 | EP | Y | SYS |
| TC-12-016 | Double submit within 5 s with the same key creates one lead | TS-12-03 · US-1203 AC-1203-02 · NFR-005 | Data: same idempotency key twice, 2 s apart | Submit twice | One lead; second response returns the first reference | P0 | T16 | EG | Y | SYS |
| TC-12-017 | MedMaarg page makes no third-party pixel request on load or submit | TS-12-03 · US-1203 AC-1203-03 · BRL-MKT-06, BRL-ELG-14 | Pre: PP-06 with network capture | Load page; submit form | 0 requests to non-first-party hosts; only first-party events stored; CSP `connect-src` excludes ad hosts | P0 | T19, T07 | EP | Y | E2E |
| TC-12-018 | Offer end boundary shows "Offer ended" from the first second after expiry | TS-12-03 · US-1203 AC-1203-04 | Data: offer ends 2026-12-31 23:59:59 IST | GET at 23:59:59 and at 2027-01-01 00:00:00 IST | First: offer shown. Second: "Offer ended" with general enquiry link; form posts to general enquiry | P1 | T01 | BVA | Y | SYS |
| TC-12-019 | Page and API responses contain no internal metrics or other visitors' data | TS-12-03 · US-1203 AC-1203-05 · CA-PUB; NFR-020 | Data: page with lead counter fixture in Admin | Scan HTML, JSON and headers | 0 lead counts, internal IDs, other visitors' data | P0 | T07, T15 | EP | Y | SYS |
| TC-12-020 | No personal data in URLs or attribution parameters | TS-12-03 · US-1203 Notes · BRL-PRV-06 | Data: URL `?utm_content=asha%40corp.example` | Load and submit | Email-like and phone-like values in query parameters dropped from the stored AttributionEvent; not echoed in page | P0 | T19 | EG | Y | SYS |
| TC-12-021 | Invalid email or missing consent is rejected | TS-12-03 · US-1203 D4 · CA-INTAKE | Data: `buyer@` and consent unticked | Submit each | 422 with field errors; no lead | P1 | T01 | EP | Y | SYS |
| TC-12-022 | ta-IN page renders Tamil script and localized errors | TS-12-03 · US-1203 D8 · DEC-026 | Pre: approved ta-IN variant | Submit invalid form | Tamil labels and errors; `lang="ta"` | P3 | T13 | EP | Y | E2E |

#### Group TC-12-D: Equivalence partitioning and boundary values – campaign builder and simulation (US-1204)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-12-023 | Simulation shows eligible count, exclusions by rule and cost; nothing queued | TS-12-04 · US-1204 AC-1204-01 · FR-A058; BRL-AUT-04; RECOMMENDATION-056 | Pre: PP-01, MedMaarg, `priya`. Data: segment of 1,200; email; cap INR 2,000.00 | POST simulate | 842 eligible; excluded 211 BRL-ELG-02, 97 BRL-ELG-05, 50 BRL-ELG-09; estimate INR 412.50; 0 messages, 0 outbox rows, 0 reservations | P0 | T17, T19 | EP | Y | SYS |
| TC-12-024 | Health-condition audience filter cannot be saved | TS-12-04 · US-1204 AC-1204-02 · BRL-ELG-14 | Data: filter `condition = diabetic` | Save | 422 BRL-ELG-14 | P0 | T19 | EP | Y | SYS |
| TC-12-025 | EduVerse learners under 18 are excluded with BRL-ELG-13 | TS-12-04 · US-1204 AC-1204-02 · BRL-ELG-13; DEC-030 | Pre: EduVerse. Data: segment of 300 incl. 40 learners < 18 and 12 school-learner flags without age | Simulate | 52 excluded with BRL-ELG-13; guardians included only with verified consent | P0 | T19 | EP | Y | SYS |
| TC-12-026 | Hard spend cap required: empty and 0.00 rejected, 0.01 accepted | TS-12-04 · US-1204 AC-1204-03 · BRL-MKT-04 | Data: cap empty, INR 0.00, INR 0.01 | Save | Empty and 0.00 → 422 "Hard spend cap required"; 0.01 accepted | P1 | T01 | BVA | Y | SYS |
| TC-12-027 | 10% holdout selects 84 of 842 deterministically | TS-12-04 · US-1204 AC-1204-04 · BRL-MKT-10; O-20 | Data: holdout 10% | Simulate twice | 84 held out both times, identical IDs | P1 | T01 | BVA | Y | SYS |
| TC-12-028 | Growth manager cannot edit campaigns | TS-12-04 · US-1204 AC-1204-05 | Pre: `asha` | PATCH campaign | 403; NSE | P1 | T07 | EP | Y | SYS |
| TC-12-029 | Rejected opportunities are excluded from every campaign | TS-12-04 · US-1204 Links · BRL-ELG-15 | Data: 9 contacts linked to rejected opportunities | Simulate | 9 excluded BRL-ELG-15 | P0 | T19 | EP | Y | SYS |
| TC-12-030 | Empty audience cannot be submitted | TS-12-04 · US-1204 D4 | Data: segment with 0 eligible after exclusions | Simulate; submit | Simulation shows 0; submit 422 "No eligible recipients" | P2 | T01 | BVA | Y | SYS |
| TC-12-031 | Experiment stops when opt-out rate exceeds baseline + 50% | TS-12-04 · US-1204 Links · BRL-MKT-10 | Data: baseline opt-out 0.40%; variant reaches 0.61% (> 0.60%) | Run experiment (simulator) | Variant stopped; holdout unchanged; owner notified | P1 | T19 | BVA | Y | SYS |

#### Group TC-12-E: Decision table – campaign approval, reservation and execution (US-1205)

| Rule | Approved campaign hash current | Claims approved by R10 | Budget reservation succeeds | Recipient eligible at execution | Complaint threshold reached | Result | TC |
|---|---|---|---|---|---|---|---|
| K1 | Y | Y | Y | Y | N | Send | TC-12-032 |
| K2 | Y | Y | Y | N | N | Skip recipient, count "excluded at execution" | TC-12-033 |
| K3 | Y | Y | Y | – | Y | Pause campaign | TC-12-034 |
| K4 | Y | Y | N | – | – | Approval fails | TC-12-035 |
| K5 | N | – | – | – | – | Approval void, back to Draft | TC-12-036 |
| K6 | Y | N | – | – | – | Not Approved, awaiting R10 | TC-12-039 |

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-12-032 | Approve hash and reserve INR 2,000.00 (K1) | TS-12-05 · US-1205 AC-1205-01 · FR-A059; BRL-MKT-04; DEC-038 | Pre: PP-01, MedMaarg, `farah` R05L; R10 claims approval present. Data: CMP-9 hash `sha256:aa11` | POST approve | CMP-9 `Approved`; reservation INR 2,000.00 in the MedMaarg campaign budget ledger; approval expiry = campaign end date | P0 | T01, T20 | DT | Y | SYS |
| TC-12-033 | Recipient who opted out after approval is skipped at execution (K2) | TS-12-05 · US-1205 AC-1205-02 · BRL-ELG-02, BRL-ELG-18 | Data: C-777 opted out after approval | Run CMP-9 | C-777 skipped with BRL-ELG-02; counted under "excluded at execution"; 0 provider calls for C-777 | P0 | T19 | DT | Y | SYS |
| TC-12-034 | Third complaint in 24 h pauses the campaign (K3) | TS-12-05 · US-1205 AC-1205-03 · BRL-ELG-11; NT-027 | Data: 2 complaints in 24 h | Inject 3rd | CMP-9 `Paused`; NT-027; no further sends | P0 | T19 | DT | Y | SYS |
| TC-12-035 | Insufficient budget fails approval at the boundary (K4) | TS-12-05 · US-1205 AC-1205-04 · BRL-AI-08 pattern; NFR-014 | Data: remaining budget INR 1,500.00; then INR 1,999.99; then INR 2,000.00 | POST approve each | 1,500.00 and 1,999.99 → 422 "Budget reservation failed"; 2,000.00 → Approved | P0 | T20 | BVA | Y | SYS |
| TC-12-036 | Editing the audience after approval voids it (K5) | TS-12-05 · US-1205 AC-1205-04 · BRL-APR-02 | Data: CMP-9 Approved | `priya` edits audience | Approval void; CMP-9 `Draft`; reservation released | P0 | T19 | DT | Y | SYS |
| TC-12-037 | Author cannot approve own campaign | TS-12-05 · US-1205 AC-1205-05 · BRL-APR-01 | Pre: `priya` | POST approve | 403; NSE | P0 | T07 | EP | Y | SYS |
| TC-12-038 | Finance sees spend and reservation but no Approve | TS-12-05 · US-1205 AC-1205-05 | Pre: `lata` R08 | Open CMP-9; POST approve | Spend and reservation visible; action absent; API 403 | P1 | T07 | EP | Y | SYS |
| TC-12-039 | Campaign without R10 claims approval stays pending (K6) | TS-12-05 · US-1205 Links · DEC-038 | Data: claims approval missing | `farah` approves | State remains `PendingApproval` "awaiting claims approval (R10)" | P0 | T19 | DT | Y | SYS |
| TC-12-040 | Approval expires at the campaign end date | TS-12-05 · US-1205 Notes · BRL-APR-03 | Data: end date 2026-12-20 23:59:59 IST; send batch due 2026-12-21 09:00 | Advance clock | Campaign `Completed` at end date; 0 sends on 12-21 | P1 | T01 | BVA | Y | SYS |
| TC-12-041 | Resume after pause rechecks approval validity and policy | TS-12-05 · US-1205 · §2.27.13 Paused→Running; BRL-MKT-01 | Data: CMP-9 Paused; claim CL-12 expired meanwhile | POST resume | 409 "approval no longer valid"; stays `Paused` | P0 | T19 | ST | Y | SYS |

#### Group TC-12-F: Contract and decision table – ads provider adapter (US-1206; battery B1–B7)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-12-042 | Ads adapter disabled while B12 is not approved (battery B7) | TS-12-06 · US-1206 AC-1206-01 · NFR-037; DEC-020 | Pre: PP-01, OrganicSpec, B12 not approved | POST launch AD-3 | 403 `PAID_ADAPTER_DISABLED`; 0 provider calls | P0 | T20, T07 | EP | Y | SYS |
| TC-12-043 | Contract: pause, spend report and timeout normalised (battery B1) | TS-12-06 · US-1206 AC-1206-02 · FR-ADP-01; ASSUMPTION-168 | Pre: PP-04 + recorded sandbox fixtures | Replay | `paused`; spend {amount "812.40", currency INR, as_of}; `uncertain` | P1 | T01 | EP | Y | CT |
| TC-12-044 | Account currency differs from cap currency | TS-12-06 · US-1206 AC-1206-03 · DEC-027 | Data: account `ads-us` (USD) with INR cap | Enable | 422 "Currency mismatch: caps must be in account currency"; no FX conversion performed | P1 | T01 | EP | Y | SYS |
| TC-12-045 | Pause timeout marked "pause uncertain", spend polled every 5 min and pause reissued (battery B3) | TS-12-06 · US-1206 AC-1206-04 · FR-STD-02; BRL-AUT-07 | Data: pause call times out | Run; advance clock 15 min | Status "pause uncertain"; spend checks at +5, +10, +15 min; pause reissued with same key (idempotent); confirmed paused | P0 | T18 | ST | Y | SYS |
| TC-12-046 | Enabling the paid adapter by R11 alone stays pending Founder approval | TS-12-06 · US-1206 AC-1206-05 · CFG-24; BRL-APR-11 | Pre: `arjun` R11 | Enable | Change pending R01; adapter still disabled; after `vikram` approval enabled | P0 | T19 | EP | Y | SYS |
| TC-12-047 | Ads credentials stored as references only (battery B5) | TS-12-06 · US-1206 · NFR-004 | Data: developer token reference | GET config; scan logs | No token value in API, UI or logs | P0 | T07 | EP | Y | SYS |
| TC-12-048 | Launch request re-submitted after worker crash creates one campaign (battery B2) | TS-12-06 · US-1206 · NFR-005 | Pre: PP-05; kill worker after provider accept | Restart | 1 provider campaign; key `AD-3:launch:1` | P0 | T16 | EG | Y | IT |
| TC-12-049 | No health events or minors' data sent to ad platform conversion APIs | TS-12-06 · US-1206 Links · BRL-MKT-06 | Data: MedMaarg lead events; EduVerse learner lead | Run conversion export (simulator) | 0 MedMaarg health-related events and 0 learner records in the payload; export blocked for MedMaarg pages | P0 | T19 | EP | Y | SYS |

#### Group TC-12-G: Boundary values – ads dashboard and anomaly detection (US-1207)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-12-050 | Spend versus caps with as-of time | TS-12-07 · US-1207 AC-1207-01 · FR-A060; KPI-10 | Pre: PP-01, `priya`. Data: daily INR 312.00 of 500.00; monthly INR 4,120.00 of 10,000.00 | Open dashboard | Values and as-of shown read-only | P2 | T01 | EP | Y | SYS |
| TC-12-051 | Spend at 150.3% of expected pauses and alerts | TS-12-07 · US-1207 AC-1207-02 · BRL-MKT-05; NT-026; O-16 | Data: expected INR 300.00; spend reaches INR 451.00 | Spend poll | AD-3 paused via adapter; NT-026 to owner and `lata` R08 | P0 | T20 | BVA | Y | SYS |
| TC-12-052 | Anomaly boundary: 450.00 (150.00%) no pause; 450.01 pause | TS-12-07 · US-1207 · BRL-MKT-05; O-16 | Data: two runs | Spend poll | 450.00 → running; 450.01 → paused | P0 | T20 | BVA | Y | UT |
| TC-12-053 | Metrics 3 hours late are labelled stale and not used to resume | TS-12-07 · US-1207 AC-1207-03 | Data: provider lag 3 h; AD-3 paused for anomaly | Attempt auto-resume | Stale indicator; resume refused "metrics stale" | P1 | T01 | EP | Y | SYS |
| TC-12-054 | Conversion counts cannot be edited | TS-12-07 · US-1207 AC-1207-04 | Pre: `vikram` R01 | PATCH conversions | 403 (measured, read-only) | P1 | T07 | EP | Y | SYS |

#### Group TC-12-H: Boundary values – ad spend caps, launch and pause (US-1208)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-12-055 | Launch within cap with two-step confirmation pushes the effective cap | TS-12-08 · US-1208 AC-1208-01 · FR-A061; CA-DISPATCH | Pre: PP-01, OrganicSpec, R05; B12 approved. Data: AD-3 approved, daily cap 500.00, reserved 10,000.00 | Confirm, confirm again | AD-3 `Running`; provider daily budget = INR 500.00 | P0 | T20 | UC | Y | SYS |
| TC-12-056 | Effective cap is the minimum of daily cap, remaining monthly and reserved | TS-12-08 · US-1208 Notes · BRL-MKT-05 | Data: monthly remaining INR 300.00 | Launch | Provider daily budget INR 300.00 | P0 | T20 | BVA | Y | UT |
| TC-12-057 | Monthly cap boundary: 9,999.99 runs; 10,000.00 pauses with NT-025 Critical | TS-12-08 · US-1208 AC-1208-02 · BRL-MKT-05; O-16 | Data: spend polls 9,999.99 then 10,000.00 | Spend poll | First: running; second: paused via provider; NT-025 Critical | P0 | T20 | BVA | Y | SYS |
| TC-12-058 | Raising the monthly cap stays pending Founder approval | TS-12-08 · US-1208 AC-1208-03 · BRL-APR-11 | Pre: R05L. Data: 10,000.00 → 15,000.00 | Save | Pending R01; provider cap unchanged | P0 | T19 | EP | Y | SYS |
| TC-12-059 | Emergency stop pauses all running ad campaigns within 60 s | TS-12-08 · US-1208 AC-1208-04 · BRL-AUT-05 | Data: 3 running campaigns | `gopal` R02 activates stop at T | Pause calls for all 3 issued by T + 60 s; 0 launch calls after T | P0 | T19 | BVA | Y | SYS |
| TC-12-060 | Growth manager cannot launch | TS-12-08 · US-1208 AC-1208-05 | Pre: R03 OrganicSpec | POST launch | 403; NSE | P1 | T07 | EP | Y | SYS |
| TC-12-061 | A single confirmation does not launch | TS-12-08 · US-1208 Story · CA-DISPATCH | Data: confirm once, close dialog | Check state | `Approved`, not Running; 0 provider calls | P1 | T01 | EP | Y | E2E |

#### Group TC-12-I: Equivalence partitioning – partner referral form (US-1209)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-12-062 | Referral recorded with partner attribution | TS-12-09 · US-1209 AC-1209-01 · FR-W20 | Pre: PP-02 `medmaarg.example`. Data: code PRT-22, "Lotus Hospitals, Cuttack", role "Admin head", attestation ticked | Submit | REF-101 `Received` with attribution PRT-22 | P2 | T01 | EP | Y | SYS |
| TC-12-063 | Referred contact is not eligible for any outreach before own consent | TS-12-09 · US-1209 AC-1209-02 · BRL-ELG-17 | Data: REF-101 contact | Enrol in a sequence; simulate a campaign including it | Enrol 422 BRL-ELG-17; campaign simulation excludes it with BRL-ELG-17 | P0 | T19 | EP | Y | SYS |
| TC-12-064 | Unnecessary personal data redacted with a minimisation warning | TS-12-09 · US-1209 AC-1209-03 · BRL-PRV-06 | Data: notes with "+91 98xxxxxx10" and "DOB 12/03/1980" | Submit | Stored notes show redaction markers; referrer sees the warning | P0 | T19 | EG | Y | SYS |
| TC-12-065 | Duplicate referral within 90 days is linked; attribution follows the first | TS-12-09 · US-1209 AC-1209-04 · O-17 | Data: second partner refers the same organisation at +90 d exactly and at +90 d + 1 s | Submit | +90 d: linked as duplicate, attribution PRT-22; +90 d + 1 s: new referral | P2 | T01 | BVA | Y | SYS |
| TC-12-066 | Inactive partner code accepted without attribution and flagged | TS-12-09 · US-1209 AC-1209-05 | Data: PRT-99 | Submit | Referral created, attribution empty, review flag | P2 | T01 | EP | Y | SYS |
| TC-12-067 | Referral status is not readable without an object grant | TS-12-09 · US-1209 AC-1209-05 · CA-PORTAL; ABAC-09 | Data: anonymous; partner R16 with grant on REF-101; other partner without grant | GET `/referrals/REF-101` | Anonymous 404; granted partner sees status only; other partner U404 | P0 | T07, T15 | EP | Y | SYS |

#### Group TC-12-J: Boundary values – referral approvals and commission record (US-1210)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-12-068 | Approve referral with commission recorded only and assign opportunity | TS-12-10 · US-1210 AC-1210-01 · FR-A064; DEC-046 | Pre: PP-01, MedMaarg, `meera` R02; review by `priya`. Data: REF-101, 5.00%, reason "verified partner" | POST approve | Qualified opportunity assigned to the MedMaarg owner; commission record "approved – record only", Decimal 5.00 | P1 | T01 | EP | Y | SYS |
| TC-12-069 | No payable, payment instruction or payout exists for a commission | TS-12-10 · US-1210 AC-1210-02 · DEC-046; BRL-FIN-08 | Data: approved commission | Query ledgers, payment instructions, actions API | 0 payable entries; 0 payout actions; API has no payout endpoint (route inventory) | P0 | T19, T07 | EP | Y | SYS |
| TC-12-070 | Commission range 0.00–50.00 inclusive | TS-12-10 · US-1210 AC-1210-03 · O-15 | Data: −0.01, 0.00, 50.00, 50.01, 150.00 | Save each | 0.00 and 50.00 accepted; others 422 "0.00 to 50.00%" | P1 | T01 | BVA | Y | SYS |
| TC-12-071 | Rejection requires a reason | TS-12-10 · US-1210 AC-1210-04 · BRL-APR-08 | Pre: `meera` | POST reject {} | 400 | P2 | T01 | EP | Y | SYS |
| TC-12-072 | Reviewer who submitted the referral cannot approve | TS-12-10 · US-1210 AC-1210-05 · BRL-APR-01 | Pre: `priya` | POST approve | 403; NSE | P0 | T07 | EP | Y | SYS |
| TC-12-073 | Approval does not make the referred contact eligible | TS-12-10 · US-1210 Links · BRL-ELG-17 | Data: REF-101 approved, no consent recorded | Enrol contact | 422 BRL-ELG-17 | P0 | T19 | EP | Y | SYS |

#### Group TC-12-K: State transition, pairwise and use case – campaign machine, matrix and journeys

**Common for TC-12-074 and TC-12-075:** Pre: PP-01, MedMaarg campaign; Part 2.3 §2.27.13 (12 transitions). Steps: drive each transition through the API.

| ID | Data (transitions) | Expected | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-12-074 | Valid: Draft→Simulated; Simulated→PendingApproval; PendingApproval→Draft (reject with reason); PendingApproval→Approved (TC-12-032); Approved→Running at start date; Running→Paused (manual); Paused→Running (TC-12-041 positive variant); Running→Completed (end date, TC-12-040); Paused→Cancelled; Approved→Cancelled (reservation released) | Each transition once with audit; cancellation releases the reservation in the budget ledger | TS-12-11 · US-1204, US-1205 · §2.27.13 | P1 | T01 | ST | Y | SYS |
| TC-12-075 | Sneak paths: Draft→Running; Simulated→Approved; PendingApproval→Running; Completed→Running | 409 `INVALID_TRANSITION`; 0 sends; 0 reservations | TS-12-11 · US-1205 · BRL-MKT-04 | P0 | T01 | ST | Y | UT |

Pairwise set (factor file `ff_12_campaign.yaml`): Startup {MedMaarg, OrganicSpec} × Channel {email, WhatsApp template} × Segment {IN B2B consented, EU role-based with LIA, mixed with suppressed and minors} × Budget {sufficient, insufficient} × Mode {live, simulation}. Full factorial 48; all-pairs 6 rows. **Common:** approve and run the campaign; read results and simulator log.

| ID | Startup · Channel · Segment · Budget · Mode | Expected | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-12-076 | MedMaarg · email · IN consented · sufficient · live | Approved; all eligible sent; reservation consumed by actual cost | TS-12-11 · US-1205 · BRL-MKT-04 | P0 | T19 | PW | Y | SYS |
| TC-12-077 | MedMaarg · WhatsApp · EU role-based · insufficient · simulation | Simulation lists all EU recipients excluded `EU_NO_WHATSAPP_COLD`; approval would fail on budget; 0 calls | TS-12-11 · US-1204 · BRL-ELG-06 | P0 | T19, T17 | PW | Y | SYS |
| TC-12-078 | MedMaarg · email · mixed · sufficient · simulation | Suppressed and minors excluded by rule; 0 calls | TS-12-11 · US-1204 · BRL-ELG-02, BRL-ELG-13 | P0 | T17 | PW | Y | SYS |
| TC-12-079 | OrganicSpec · WhatsApp · IN consented · sufficient · live | Only opted-in contacts with usable template sent | TS-12-11 · US-1205 · BRL-ELG-07 | P0 | T19 | PW | Y | SYS |
| TC-12-080 | OrganicSpec · email · EU role-based · insufficient · live | Approval fails "Budget reservation failed"; 0 sends | TS-12-11 · US-1205 · NFR-014 | P0 | T20 | PW | Y | SYS |
| TC-12-081 | OrganicSpec · WhatsApp · mixed · insufficient · simulation | Simulation shows exclusions; submit blocked on budget | TS-12-11 · US-1204 · BRL-MKT-04 | P1 | T17 | PW | Y | SYS |

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-12-082 | J-12-01: campaign landing page to attributed lead | TS-12-11 · US-1203 · FR-W10 | Pre: PP-06 (Chromium, WebKit), 360 px | Open `?utm_campaign=CMP-9-LI` → submit RFQ with consent → Admin opens lead | Lead with attribution and consent; 0 third-party requests; axe 0 critical/serious | P0 | T01, T19 | UC | Y | E2E |
| TC-12-083 | J-12-02: simulate, approve with reservation, run with execution-time suppression | TS-12-11 · US-1204, US-1205 · FR-A058, FR-A059 | Pre: PP-06, `priya` and `farah` lanes | Build → simulate → submit → approve → C-777 opts out → run | Reservation shown; C-777 skipped; KPI-17 = 0; axe 0 critical/serious | P0 | T01, T19 | UC | Y | E2E |

### 6.2.9.3 EP-12 coverage

| Story | AC → TC |
|---|---|
| US-1201 | 01→001 · 02→002 · 03→003 · 04→004 · 05→005 · extra→006, 007 |
| US-1202 | 01→008, 014 · 02→009 · 03→010 · 04→011 · 05→012 · extra→013 |
| US-1203 | 01→015 · 02→016 · 03→017 · 04→018 · 05→019 · extra→020, 021, 022, 082 |
| US-1204 | 01→023 · 02→024, 025 · 03→026 · 04→027 · 05→028 · extra→029, 030, 031, 077, 078, 081 |
| US-1205 | 01→032 · 02→033 · 03→034 · 04→035, 036 · 05→037, 038 · extra→039, 040, 041, 074, 075, 083 |
| US-1206 | 01→042 · 02→043 · 03→044 · 04→045 · 05→046 · extra→047, 048, 049 |
| US-1207 | 01→050 · 02→051, 052 · 03→053 · 04→054 |
| US-1208 | 01→055 · 02→057 · 03→058 · 04→059 · 05→060 · extra→056, 061 |
| US-1209 | 01→062 · 02→063 · 03→064 · 04→065 · 05→066, 067 |
| US-1210 | 01→068 · 02→069 · 03→070 · 04→071 · 05→072 · extra→073 |

All 49 EP-12 AC covered.

---

## 6.2.10 EP-13 Proposal, quote, negotiation and contract

Stories US-1301…US-1313 (67 AC). FRs: FR-A065…FR-A072, FR-W23, FR-W24; cross-cutting FR-DM-01, FR-ADP-01, FR-STD-02. Agents exercised deterministically: AG-020 Proposal & Bid Response Drafter, AG-021 Objection & Negotiation Assistant, AG-012 guard. State machines Part 2.3 §2.27.5 (proposal and quote) and §2.27.6 (contract). Pricing modules carry mutation score ≥ 85% (§6.1.9.6).

### 6.2.10.1 Test scenarios

| TS ID | Scenario | Linked stories / FR | Risk area · Priority | TCs |
|---|---|---|---|---|
| TS-13-01 | Proposal drafts use approved templates, current price versions and read-only computed amounts; AI promises removed | US-1301 · FR-A065 | RA-06, RA-13 · **P0** | TC-13-001…008 |
| TS-13-02 | Proposal approval binds the exact revision, adds Legal for non-standard terms, escalates and supersedes | US-1302 · FR-A066 | RA-05 · **P0** | TC-13-009…015 |
| TS-13-03 | Decimal pricing library computes lines, tax and totals exactly and deterministically | US-1303 · FR-DM-01, FR-A067, FR-A105 | RA-06 · **P0** | TC-13-016…028 |
| TS-13-04 | Quotation builder validates units, quantities, currency and price-list freshness with live totals | US-1304 · FR-A067 | RA-06 · **P0** | TC-13-029…035 |
| TS-13-05 | Discount and margin thresholds route each quote to exactly the required approvers | US-1305 · FR-A068 | RA-05, RA-06 · **P0** | TC-13-036…055 |
| TS-13-06 | Portal review lets the grantee accept or request changes only on a valid, current revision | US-1306 · FR-W23 | RA-15, RA-06 · **P0** | TC-13-056…063 |
| TS-13-07 | Objections get approved answers; concessions beyond limit escalate; AI never offers price or terms | US-1307 · FR-A069 | RA-13, RA-05 · **P0** | TC-13-064…068 |
| TS-13-08 | Negotiation exceptions are decided with risk class, Legal where needed and SLA escalation | US-1308 · FR-A070 | RA-05 · **P0** | TC-13-069…072 |
| TS-13-09 | Contracts generated from approved templates are sent only after legal approval and executed only on matching hashes | US-1309 · FR-A071 | RA-10 · **P0** | TC-13-073…079 |
| TS-13-10 | Legal approval binds the contract hash and adds the Founder at value or cross-border thresholds | US-1310 · FR-A072 | RA-10, RA-05 · **P0** | TC-13-080…085 |
| TS-13-11 | E-sign adapter records consistent signature evidence on the signed-PDF and provider paths | US-1311 · FR-A071, FR-W24, FR-ADP-01 | RA-10, RA-04 · **P0** | TC-13-086…094 |
| TS-13-12 | Portal signatory reviews, declares authority and signs only the current version | US-1312 · FR-W24 | RA-10, RA-15 · **P0** | TC-13-095…101 |
| TS-13-13 | Step-up MFA, delegation, replay protection and separation of duties on every commercial approval | US-1313 · FR-A066, FR-A068, FR-A070, FR-A072 | RA-05, RA-02 · **P0** | TC-13-102…110 |
| TS-13-14 | Proposal/quote and contract state machines; pairwise pricing matrix; journeys J-13-01 and J-13-02 | US-1302…US-1312 · §2.27.5, §2.27.6 | RA-06, RA-10 · **P0** | TC-13-111…128 |

### 6.2.10.2 Test cases

#### Group TC-13-A: Equivalence partitioning and error guessing – proposal builder (US-1301)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-001 | Proposal draft from template with frozen price snapshot and read-only amount | TS-13-01 · US-1301 AC-1301-01 · FR-A065; BRL-QTE-01, BRL-AI-03 | Pre: PP-01, MedMaarg, `asha`; clock 2026-11-27 11:00 IST. Data: D-210 with Completed demo; MM-PILOT v2; "Scanner corporate pilot" PV-7 (2 units × INR 150.00, 10% pilot discount); replay fixture `ag020_mm_pilot` | Generate | P-55 v1 `Draft` with scope sections, evidence links; amount INR 270.00 computed by the pricing library from PV-7; snapshot ID stored; amount field read-only in A065 | P0 | T01 | UC | Y | SYS |
| TC-13-002 | Guarantee sentence removed and flagged | TS-13-01 · US-1301 AC-1301-02 · BRL-AI-05 | Data: replay output contains "guaranteed 30% reduction in sick days" | Generate | Sentence removed; note "unsupported promise removed"; audit entry | P0 | T14, T19 | EG | Y | SYS |
| TC-13-003 | Planned offering refused | TS-13-01 · US-1301 AC-1301-03 · BRL-MKT-02 | Data: "Doctor Connect" Planned | Generate | 422 BRL-MKT-02; no proposal | P1 | T19 | EP | Y | SYS |
| TC-13-004 | Price version validity boundary | TS-13-01 · US-1301 AC-1301-03 · BRL-QTE-01 | Data: PV-7 valid until 2026-11-30 23:59:59 IST | Generate at 2026-11-30 23:59:59 and 2026-12-01 00:00:00 IST | First succeeds; second 422 "Current price version required" | P0 | T01 | BVA | Y | SYS |
| TC-13-005 | Gateway down inserts template sections and still computes the amount | TS-13-01 · US-1301 AC-1301-04 · DEC-007 | Data: gateway 503 | Generate | Unpersonalised sections; amount INR 270.00; draft saved | P1 | T01 | EG | Y | SYS |
| TC-13-006 | Marketing cannot create proposals | TS-13-01 · US-1301 AC-1301-05 | Pre: `priya` R05 | POST proposal on D-210 | 403; NSE | P1 | T07 | EP | Y | SYS |
| TC-13-007 | Client-side change to a computed amount is ignored | TS-13-01 · US-1301 Notes · BRL-QTE-01; NFR-017 | Data: PATCH amount "100.00" | PATCH | Amount stays 270.00; tamper warning audited | P0 | T07 | EG | Y | SYS |
| TC-13-008 | T2 user cannot draft against a T1 deal | TS-13-01 · US-1301 · BRL-TEN-03 | Pre: T2 `b-r03` | POST proposal with D-210 ID | U404 | P0 | T15 | EP | Y | SYS |

#### Group TC-13-B: Decision table and boundary values – proposal approval (US-1302)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-009 | Approve exact revision, publish to the portal grant and queue NX-04 | TS-13-02 · US-1302 AC-1302-01 · FR-A066; BRL-APR-02 | Pre: PP-01, `meera` R02, MFA 1 h. Data: P-55 v1 hash `sha256:p55v1`, standard terms | POST approve; publish | `Approved` then `Sent` to the grantee; NX-04 queued (transactional) | P0 | T01 | DT | Y | SYS |
| TC-13-010 | Changed liability clause requires Legal in addition | TS-13-02 · US-1302 AC-1302-02 · BRL-APR-05 | Data: liability clause differs from template | `meera` approves; then `dev` R10 | After R02: still `PendingApproval` "awaiting Legal"; after R10: `Approved` | P0 | T19 | DT | Y | SYS |
| TC-13-011 | SLA escalation after 1 business day; never auto-approved | TS-13-02 · US-1302 AC-1302-03 · BRL-APR-10; O-13 | Data: submitted Sat 2026-12-05 11:00 IST | Advance to Mon 2026-12-07 10:59:59 and 11:00:00 IST | No escalation at 10:59:59; escalation to `vikram` R01 at 11:00:00; state stays `PendingApproval` indefinitely | P1 | T01 | BVA | Y | SYS |
| TC-13-012 | New revision supersedes v1 in the portal | TS-13-02 · US-1302 AC-1302-04 · BRL-QTE-06 | Data: v1 Sent; Asha creates v2 | Create v2; open v1 in portal; POST accept v1 | v1 `Superseded`; banner "A newer version exists"; accept 409 | P0 | T01 | ST | Y | SYS |
| TC-13-013 | Author cannot approve | TS-13-02 · US-1302 AC-1302-05 · BRL-APR-01 | Pre: `asha` | POST approve P-55 v1 | 403; NSE | P0 | T07 | EP | Y | SYS |
| TC-13-014 | A lower role that is not the author cannot approve | TS-13-02 · US-1302 AC-1302-05 · ABAC-04 | Pre: `kiran` R03 | POST approve | 403 `ABOVE_APPROVAL_LIMIT` | P0 | T07 | EP | Y | SYS |
| TC-13-015 | Approving a stale revision returns 409 | TS-13-02 · US-1302 · NFR-025 | Data: R02 opened v1; v2 saved | Approve v1 | 409 `STALE_REVISION` | P1 | T01 | EG | Y | SYS |

#### Group TC-13-C: Worked examples, boundary values and property-based tests – Decimal pricing library (US-1303)

**Common:** Pre: PP-04 (library only), Decimal context precision 28, ROUND_HALF_UP; TaxProfile fixture with illustrative 18% (ASSUMPTION-169).

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-016 | Worked example FR-DM-01: 2 × 150.00 at 10% = 270.00 | TS-13-03 · US-1303 AC-1303-01 · FR-DM-01; BRL-QTE-02 | Data: qty 2, unit INR 150.00, discount 10.00 | `line_total()` | `Decimal("270.00")` INR exactly (type Decimal, exponent −2) | P0 | T01 | BVA | Y | UT |
| TC-13-017 | HALF_UP per line; subtotal = Σ rounded lines | TS-13-03 · US-1303 AC-1303-02 · BRL-QTE-02 | Data: A = 1 × 5.33 at 50% (2.665); B = 3 × 10.05 at 15% (25.6275) | Compute document | A 2.67; B 25.63; subtotal 28.30 (not 28.29 from rounding 28.2925) | P0 | T01 | BVA | Y | UT |
| TC-13-018 | Intra-state: CGST 24.30 + SGST 24.30 on 270.00 = 318.60 | TS-13-03 · US-1303 AC-1303-03 · BRL-QTE-03; DEC-027 | Data: supplier Odisha (21), buyer Odisha, SAC 998314 | Compute | CGST 24.30; SGST 24.30; total 318.60 | P0 | T01 | EP | Y | UT |
| TC-13-019 | Inter-state: IGST 48.60, total 318.60 | TS-13-03 · US-1303 AC-1303-03 · BRL-QTE-03 | Data: buyer Tamil Nadu (33) | Compute | IGST 48.60; total 318.60 | P0 | T01 | EP | Y | UT |
| TC-13-020 | Export with active LUT is zero-rated | TS-13-03 · US-1303 AC-1303-03 · BRL-QTE-03 | Data: buyer abroad; LUT active for the financial year | Compute | Tax 0.00; LUT reference on the document | P0 | T01, T19 | EP | Y | UT |

**Common for TC-13-021…024 (invalid inputs, AC-1303-04):** Steps: call the library through the quote API. Expected: validation error, nothing persisted, no revision created.

| ID | Data | Expected | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-13-021 | Discount 100.01% | 400 `DISCOUNT_OUT_OF_RANGE` | TS-13-03 · US-1303 AC-1303-04 · BRL-QTE-04 | P0 | T01 | BVA | Y | UT, SYS |
| TC-13-022 | Discount −0.01% | 400 `DISCOUNT_OUT_OF_RANGE` | TS-13-03 · US-1303 AC-1303-04 | P0 | T01 | BVA | Y | UT |
| TC-13-023 | Quantity 0 | 400 `QUANTITY_OUT_OF_RANGE` | TS-13-03 · US-1303 AC-1303-04 · BRL-QTE-07 | P0 | T01 | BVA | Y | UT |
| TC-13-024 | Line currencies INR and USD in one document | 400 `CURRENCY_MIXED` (BRL-QTE-04) | TS-13-03 · US-1303 AC-1303-04 · BRL-QTE-04 | P0 | T01 | EP | Y | UT |

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-025 | Property: invariants hold over 10,000 generated documents | TS-13-03 · US-1303 AC-1303-05 · RECOMMENDATION-055; §6.1.11.7 | Data: Hypothesis `release` profile; 1–200 lines, quantities per unit rules, discounts 0.00–100.00 step 0.01, mixed tax cases | Run | No float type anywhere; total = Σ rounded lines + Σ rounded tax lines; 0 ≤ line ≤ qty × unit; recomputation identical; mutation score ≥ 85% on the module | P0 | T01 | PBT | Y | UT |
| TC-13-026 | Client-supplied total is ignored and a tamper warning recorded | TS-13-03 · US-1303 AC-1303-06 · NFR-017 | Pre: PP-01. Data: request body `"total": "1.00"` for a 270.00 quote | POST quote | Stored total 270.00; tamper warning in audit | P0 | T07 | EG | Y | SYS |
| TC-13-027 | Extreme values: ₹99,99,99,999.99 and ₹0.01 lines compute without overflow or precision loss | TS-13-03 · US-1303 D4 · EDGE-MONEY | Data: unit 99,99,99,999.99 × qty 1; unit 0.01 × qty 1 at 50% (0.005 → 0.01) | Compute | Exact Decimal results; 0.005 rounds to 0.01 | P1 | T01 | BVA | Y | UT |
| TC-13-028 | Static check: no float in money paths | TS-13-03 · US-1303 Notes · TP-09; EG-01 | Data: lint rule over `money`, `pricing`, `ledger` packages; seeded violation `float(price)` | Run lint in CI | Seeded violation fails G0/G1; clean tree passes | P0 | T01 | EG | Y | CT |

#### Group TC-13-D: Equivalence partitioning and boundary values – quotation builder (US-1304)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-029 | OrganicSpec quote with live totals, validity and approver chip | TS-13-04 · US-1304 AC-1304-01 · FR-A067; BRL-QTE-02, BRL-QTE-05 | Pre: PP-01, OrganicSpec, `sunil` R07; clock 2026-11-27 11:00 IST. Data: PL-OS-12, TUR-A 2 kg, 10%, buyer Odisha | Build quote in A067 | Line 270.00; CGST 24.30; SGST 24.30; total INR 318.60; validity 2026-12-27 (O-14); chip "Sales Lead (≤ 10%)" | P0 | T01 | EP | Y | SYS |
| TC-13-030 | Unit not allowed for the SKU | TS-13-04 · US-1304 AC-1304-02 · BRL-QTE-07 | Data: 2 quintal | Add line | "Unit not allowed for SKU"; API 422 | P1 | T01 | EP | Y | SYS |
| TC-13-031 | Quantity boundaries 1…5,000 kg | TS-13-04 · US-1304 AC-1304-02 · BRL-QTE-07 | Data: 0, 1, 5,000, 5,001, 6,000 kg | Add each | 1 and 5,000 accepted; 0, 5,001 and 6,000 → "Quantity must be between 1 and 5,000 kg" | P1 | T01 | BVA | Y | SYS |
| TC-13-032 | Manual unit price becomes a 20.00% discount needing the Startup Head | TS-13-04 · US-1304 AC-1304-03 · BRL-QTE-01; BRL-APR-04 | Data: unit price overridden to 120.00 | Save | Recorded as discount 20.00%; chip "Startup Head"; margin (240.00 − 160.00) ÷ 240.00 = 33.33% above floor | P0 | T01 | EP | Y | SYS |
| TC-13-033 | USD line on an INR quote is refused | TS-13-04 · US-1304 AC-1304-04 · BRL-QTE-04 | Data: line from PL-OS-USD-2 | Add | 422 `CURRENCY_MIXED` | P0 | T01 | EP | Y | SYS |
| TC-13-034 | Price list changed during edit returns 409 on submit | TS-13-04 · US-1304 AC-1304-05 · NFR-025 | Data: PL-OS-13 approved while the quote is open | Submit | 409 "Price list changed - review lines" | P1 | T01 | EG | Y | SYS |
| TC-13-035 | Another startup's price list is not offered and its ID returns 404 | TS-13-04 · US-1304 AC-1304-06 · BRL-TEN-04 | Data: MedMaarg price list ID | Open picker; POST line with the ID | Not listed; API U404 | P0 | T15 | EP | Y | SYS |

#### Group TC-13-E: Boundary values and decision table – discount and margin approval routing (US-1305; converted from Part 6.1 BVA-D01…D14)

**Common for TC-13-036…049:** Pre: PP-01, OrganicSpec; quote QTE-220, 1 line OS-RICE-25KG, qty 40, unit INR 2,400.00 from PV-9; margin fixtures built by the helper `margin_fixture()` (§6.1.12.4); author `sunil` R07. Steps: set discount (and margin fixture), submit for approval, read the computed approval chain. Interpretations per ASSUMPTION-184 (two-decimal percentages; floor strictly below 25.00%).

| ID | Data: discount · margin | Expected approval chain | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-13-036 | −0.01% | 400 validation; no revision (BVA-D01) | TS-13-05 · US-1305 · BRL-QTE-04 | P0 | T01 | BVA | Y | UT, SYS |
| TC-13-037 | 0.00% · 40.00% (line 96,000.00) | No discount approval; standard quote approval only (BVA-D02) | TS-13-05 · US-1305 · BRL-APR-04 | P0 | T01 | BVA | Y | UT |
| TC-13-038 | 0.01% · 39.99% (95,990.40) | R03L or R02 (BVA-D03) | TS-13-05 · US-1305 · BRL-APR-04 | P0 | T01 | BVA | Y | UT |
| TC-13-039 | 9.99% (86,409.60) | R03L or R02 (BVA-D04) | TS-13-05 · US-1305 · BRL-APR-04 | P0 | T01 | BVA | Y | UT |
| TC-13-040 | **10.00%** (86,400.00) | R03L (AC-1305-01) or R02 (BVA-D05) | TS-13-05 · US-1305 AC-1305-01 · BRL-APR-04 | P0 | T01 | BVA | Y | UT, SYS |
| TC-13-041 | 10.01% (86,390.40) | R02 (BVA-D06) | TS-13-05 · US-1305 AC-1305-01 · BRL-APR-04 | P0 | T01 | BVA | Y | UT, SYS |
| TC-13-042 | 19.99% (76,809.60) | R02 (BVA-D07) | TS-13-05 · US-1305 · BRL-APR-04 | P0 | T01 | BVA | Y | UT |
| TC-13-043 | **20.00%** · 25.00% (76,800.00) | R02; margin exactly at floor is not below (BVA-D08) | TS-13-05 · US-1305 AC-1305-01 · BRL-APR-04 | P0 | T01 | BVA | Y | UT, SYS |
| TC-13-044 | 20.01% · 24.99% (76,790.40) | R01 + R08 in one chain, not two (BVA-D09; Part 6.1 worked example "TC-13-008") | TS-13-05 · US-1305 AC-1305-01 · BRL-APR-04; DEC-038 | P0 | T01 | BVA, DT | Y | UT, SYS |
| TC-13-045 | 5.00% · **25.00%** (91,200.00) | R03L or R02 (BVA-D10) | TS-13-05 · US-1305 · BRL-APR-04 | P0 | T01 | BVA | Y | UT |
| TC-13-046 | 5.00% · **24.99%** (91,200.00) | R01 + R08: margin floor overrides the band (BVA-D11) | TS-13-05 · US-1305 AC-1305-02 · BRL-APR-04 | P0 | T01 | BVA, DT | Y | UT, SYS |
| TC-13-047 | 100.00% · negative (0.00) | R01 + R08; warning "price zero" (BVA-D12) | TS-13-05 · US-1305 · BRL-APR-04 | P0 | T01 | BVA | Y | UT |
| TC-13-048 | 100.01% | 400 validation (BVA-D13) | TS-13-05 · US-1305 · BRL-QTE-04 | P0 | T01 | BVA | Y | UT |
| TC-13-049 | 10.00% submitted, then approval attempted by the R03L who authored the quote | 403 author ≠ approver (BVA-D14) | TS-13-05 · US-1305 · BRL-APR-01 | P0 | T07 | BVA, DT | Y | SYS |

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-050 | High-value or cross-border quote adds Founder and Legal | TS-13-05 · US-1305 AC-1305-03 · BRL-APR-06; O-15 | Data: quote totals INR 9,99,999.99 and INR 10,00,000.00 (domestic, 5% discount); and a UAE buyer quote of INR 1.00 | Submit each | 9,99,999.99 → band approver only; 10,00,000.00 → + R01 + R10; UAE → + R01 + R10 regardless of value | P0 | T01 | BVA | Y | SYS |
| TC-13-051 | Any line change after approval creates a new revision and voids approval | TS-13-05 · US-1305 AC-1305-04 · BRL-QTE-06 | Data: approved rev 3; change quantity 40 → 41 | PATCH | Rev 4 `Draft`; rev 3 approval void; portal still shows rev 3 only if Sent and not superseded | P0 | T01 | ST | Y | SYS |
| TC-13-052 | Sales Lead cannot approve a 12.00% discount | TS-13-05 · US-1305 AC-1305-05 · ABAC-04 | Pre: `neha`-equivalent R03L of OrganicSpec | POST approve | 403 `ABOVE_APPROVAL_LIMIT` | P0 | T07 | EP | Y | SYS |
| TC-13-053 | Finance user who prepared the margin analysis cannot approve as Finance | TS-13-05 · US-1305 AC-1305-05 · ABAC-03; BRL-APR-07 | Data: `lata` R08 prepared margin analysis on QTE-220 (20.01%) | `lata` approves as Finance | 403; another R08 user's approval accepted | P0 | T07 | EP | Y | SYS |
| TC-13-054 | Margin = (net − attributable direct cost) ÷ net from the price-version cost | TS-13-05 · US-1305 Notes · BRL-APR-04 | Pre: PP-04. Data: net 76,790.40; cost 40 × 1,300.00 = 52,000.00 | Compute | 32.28% (Part 6.1 §6.1.12.4); cost read from PV-9, not from the request | P0 | T01 | EP | Y | UT |
| TC-13-055 | Tighter startup override routes 6.00% to the Startup Head | TS-13-05 · US-1305 D6 · CFG-17; BRL-APR-11 (tightening immediate) | Data: OrganicSpec policy: Sales Lead limit 5.00% | Submit 6.00% | Chain = R02; policy change applied immediately without Founder approval (tightening) | P1 | T01 | DT | Y | SYS |

#### Group TC-13-F: State transition and boundary values – portal proposal and quote review (US-1306)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-056 | Grantee views and accepts a valid quote | TS-13-06 · US-1306 AC-1306-01 · FR-W23; NT-014 | Pre: PP-03, `buyer@agro.example` with grant on Q-88. Data: Q-88 rev 2 INR 318.60 valid until 2026-12-27 | Open; accept | Viewed (NT-014 to owner); Accepted with identity, timestamp, revision 2 and hash `sha256:q88r2` | P0 | T01 | ST | Y | SYS |
| TC-13-057 | Request change keeps terms unchanged | TS-13-06 · US-1306 AC-1306-02 | Data: comment "need delivery to Kolkata" | POST request-change | `ChangeRequested`; owner notified; lines and totals unchanged | P1 | T01 | ST | Y | SYS |
| TC-13-058 | Validity boundary: accept at 23:59:59 on 27 Dec; disabled from 00:00:00 on 28 Dec | TS-13-06 · US-1306 AC-1306-03 · BRL-QTE-05; O-14 | Data: Q-88 rev 2 | Accept at 2026-12-27 23:59:59 IST (case a, fresh fixture) and 2026-12-28 00:00:00 IST (case b) | a: Accepted. b: Accept disabled with "This quote expired on 27 Dec 2026"; API 409 `QUOTE_EXPIRED`; state `Expired` | P0 | T01 | BVA | Y | SYS |
| TC-13-059 | Superseded revision cannot be accepted | TS-13-06 · US-1306 AC-1306-03 · BRL-QTE-06 | Data: rev 3 exists | Open rev 2; accept | Banner "A newer version exists"; 409 | P0 | T01 | ST | Y | SYS |
| TC-13-060 | Double accept is idempotent | TS-13-06 · US-1306 AC-1306-04 · NFR-005 | Data: two accept requests 300 ms apart | POST twice | One acceptance record | P0 | T16 | EG | Y | SYS |
| TC-13-061 | Forwarded link without a grant shows the denied state and no data | TS-13-06 · US-1306 AC-1306-05 · CA-PORTAL; BRL-CTR-03 | Pre: `cfo@agro.example` signed in, no grant | Open forwarded link; call API | Denied state; API U404; response contains no quote fields; not cached (`Cache-Control: private, no-store`, BRL-PUB-05) | P0 | T07, T15 | EP | Y | SYS |
| TC-13-062 | Acceptance creates no invoice and no payment | TS-13-06 · US-1306 Notes · DEC-022 | Data: accepted Q-88 | Query invoices, payment links, ledgers | 0 invoice, 0 payment link, 0 ledger entries | P0 | T19 | EP | Y | SYS |
| TC-13-063 | Mobile and hi-IN review | TS-13-06 · US-1306 D5, D8 · NFR-023 | Pre: PP-06 WebKit 360 px, locale hi-IN | Open and accept | No horizontal scroll; totals with ₹ and Indian digit grouping; axe 0 critical/serious | P2 | T08, T13 | EP | Y | E2E |

#### Group TC-13-G: Equivalence partitioning and boundary values – objections and exceptions (US-1307, US-1308)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-064 | Approved answer suggested and objection resolved with time recorded | TS-13-07 · US-1307 AC-1307-01 · FR-A069; BRL-AI-03; KPI-28 | Pre: PP-01, MedMaarg, `asha`. Data: objection "data privacy concern" on D-210; FAQ-31 citing KR-9 | Record; use answer | FAQ-31 suggested with KR-9; objection `Resolved`; time-to-resolution stored | P1 | T01 | EP | Y | SYS |
| TC-13-065 | Concession limit: 5.00% within, 5.01% and 8.00% escalate | TS-13-07 · US-1307 AC-1307-02 · O-15 | Data: MedMaarg limit 5.00% | Propose 5.00, 5.01, 8.00 | 5.00 allowed as a quote revision draft; 5.01 and 8.00 create exceptions in A070; nothing promised to the customer | P0 | T19 | BVA | Y | SYS |
| TC-13-066 | No evidence: no comparative answer | TS-13-07 · US-1307 AC-1307-03 · BRL-SRC-10, BRL-AI-04 | Data: "your competitor is cheaper by 40%" | Request suggestion | Abstains; no comparative claim generated | P0 | T14, T19 | EP | Y | SYS |
| TC-13-067 | AI output offering a discount is blocked | TS-13-07 · US-1307 AC-1307-04 · BRL-AI-07; DEC-064 | Data: replay output "we can offer 15% off" | Request suggestion | Blocked; audit event; no quote revision created | P0 | T14, T19 | EG | Y | SYS |
| TC-13-068 | Marketing cannot record objections | TS-13-07 · US-1307 AC-1307-05 | Pre: `priya` | POST objection | 403 | P1 | T07 | EP | Y | SYS |
| TC-13-069 | Counter-proposal drafts a new quote revision for approval, not sent | TS-13-08 · US-1308 AC-1308-01 · FR-A070; BRL-AUT-01 | Pre: `meera` R02. Data: exception 8.00% | Counter-propose 6.00% | New quote revision at 6.00% `Draft` routed per US-1305 (R02); no portal publication; L1 | P0 | T01 | EP | Y | SYS |
| TC-13-070 | 120-day payment term exception needs Legal | TS-13-08 · US-1308 AC-1308-02 · BRL-APR-05 | Data: payment term 120 days | `meera` approves | Pending R10; resolved only after `dev` approves | P0 | T19 | DT | Y | SYS |
| TC-13-071 | Exception SLA breach escalates to the Founder and stays open | TS-13-08 · US-1308 AC-1308-03 · BRL-APR-10; O-13 | Data: opened Tue 2026-12-01 17:00 IST | Advance to Wed 2026-12-02 16:59:59 and 17:00:00 | Escalation at 17:00:00 only; exception `Open` | P1 | T01 | BVA | Y | SYS |
| TC-13-072 | Requester cannot approve own exception | TS-13-08 · US-1308 AC-1308-04 · BRL-APR-01 | Pre: `asha` | POST approve | 403 | P0 | T07 | EP | Y | SYS |

#### Group TC-13-H: Decision table and state transition – contracts, legal approval and e-sign (US-1309…US-1311)

| Rule | Contract value | Cross-border | Template deviation | Required approvers | TC |
|---|---|---|---|---|---|
| C1 | < ₹10,00,000.00 | N | N | R10 | TC-13-080, TC-13-081 |
| C2 | ≥ ₹10,00,000.00 | N | N | R10 + R01 | TC-13-082 |
| C3 | any | Y | – | R10 + R01 | TC-13-083 |
| C4 | any | – | Y | R10 (deviation reviewed) + per C1–C3 | TC-13-074 |

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-073 | Generate MoU from approved template with hash, dates and signer slots | TS-13-09 · US-1309 AC-1309-01 · FR-A071; BRL-CTR-01 | Pre: PP-01, EduVerse, `asha`-equivalent R03. Data: accepted quote; EV-MOU v4 | Generate | CT-14 rev 1 `Drafting`; SHA-256 hash; effective 2027-01-01; signer slots for both parties | P1 | T01 | EP | Y | SYS |
| TC-13-074 | Clause deviation highlighted and routed to Legal (C4) | TS-13-09 · US-1309 AC-1309-02 · BRL-CTR-01, BRL-APR-05 | Data: clause 7 edited | Submit | Deviation highlighted; review task for R10 | P0 | T19 | DT | Y | SYS |
| TC-13-075 | Send for signature before legal approval is blocked | TS-13-09 · US-1309 AC-1309-03 · BRL-CTR-04 | Data: CT-14 `Drafting` | `dev` POST send | 409 BRL-CTR-04; 0 e-sign calls | P0 | T19 | ST | Y | SYS |
| TC-13-076 | Signed PDF whose hash differs stays OutForSignature | TS-13-09 · US-1309 AC-1309-04 · BRL-CTR-02 | Data: approved `sha256:ct14a`; upload hashes `sha256:ct14x` | Upload | State `OutForSignature`; message "Signed document differs from approved version"; no Executed | P0 | T19 | EP | Y | SYS |
| TC-13-077 | Executed contract notifies the closure gate and sets the renewal notice date | TS-13-09 · US-1309 AC-1309-05 · BRL-CTR-05; DEC-054; O-18 | Data: all signatures verified, hashes equal; expiry 2027-12-31 | Complete | `Executed`; closure gate event (DEC-054); renewal notice 2027-11-01 00:00 IST; at 2027-10-31 23:59:59 no notice | P0 | T01 | BVA | Y | SYS |
| TC-13-078 | Growth manager cannot dispatch e-sign; only Legal | TS-13-09 · US-1309 AC-1309-06 · RBAC A071 | Pre: R03 | POST send | 403 | P0 | T07 | EP | Y | SYS |
| TC-13-079 | Sending needs recorded signer authority for both parties | TS-13-09 · US-1309 · BRL-CTR-03; GAP-159 | Data: LegallyApproved, counterparty authority missing | `dev` POST send | 422 "Signer authority required"; state `LegallyApproved` | P0 | T19 | ST | Y | SYS |
| TC-13-080 | Legal approves the exact hash; approval expiry 30 days (C1) | TS-13-10 · US-1310 AC-1310-01 · FR-A072; BRL-APR-02 | Pre: `dev` R10 (not the drafter), MFA 1 h. Data: CT-14 rev 1 `sha256:ct14a`, value INR 4,50,000.00 domestic | POST approve | `LegallyApproved`; approval expiry 2026-12-31 10:00 IST (from CLK-0) | P0 | T01 | DT | Y | SYS |

**Common for TC-13-081 and TC-13-082 (value boundary, AC-1310-02):** Pre: domestic counterparty; R10 approval recorded. Steps: submit; read required approvers.

| ID | Data | Expected | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-13-081 | Value INR 9,99,999.99 | R10 alone suffices → LegallyApproved | TS-13-10 · US-1310 AC-1310-02 · BRL-APR-06 | P0 | T01 | BVA | Y | SYS |
| TC-13-082 | Value INR 10,00,000.00 | R01 also required; stays LegalReview until R01 approves | TS-13-10 · US-1310 AC-1310-02 · BRL-APR-06; O-15 | P0 | T01 | BVA | Y | SYS |

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-083 | Cross-border counterparty needs R01 and R10 regardless of value (C3) | TS-13-10 · US-1310 AC-1310-03 · BRL-APR-06 | Data: counterparty Dubai, UAE; value INR 50,000.00 | Submit | Required approvers R10 + R01 | P0 | T01 | DT | Y | SYS |
| TC-13-084 | Drafter of the deviation cannot approve; rejection needs a reason | TS-13-10 · US-1310 AC-1310-04 · BRL-APR-01, BRL-APR-08 | Data: deviation drafted by `dev` | `dev` approves; second R10 rejects without reason | 403; 400 | P0 | T07 | EP | Y | SYS |
| TC-13-085 | Expired legal approval blocks sending | TS-13-10 · US-1310 AC-1310-01 · BRL-APR-03 | Data: approval 2026-12-01 10:00 IST (30 days) | Send at 2026-12-31 09:59:59 and 10:00:00 IST | First allowed; second 409 "Legal approval expired" | P1 | T01 | BVA | Y | SYS |
| TC-13-086 | Signed-PDF path: scan, hash, compare and record method | TS-13-11 · US-1311 AC-1311-01 · FR-W24; BRL-CTR-02; DEC-023 | Pre: PP-03 counterparty upload in W24 | Upload signed PDF (hash `sha256:ct14a`); confirm | Malware scan clean; SHA-256 computed and equal; signature event method `signed_pdf` | P0 | T01, T19 | EP | Y | SYS |
| TC-13-087 | Malware test file is rejected and not stored | TS-13-11 · US-1311 AC-1311-01 · NFR-021 | Data: EICAR test file renamed `.pdf` | Upload | Rejected with reason; object not retained; incident logged | P0 | T07 | EG | Y | SYS |
| TC-13-088 | Provider path stores the envelope with idempotency key (battery B2) | TS-13-11 · US-1311 AC-1311-02 · NFR-005 | Pre: W5 build, provider sandbox (verify). Data: key `CT-14:rev1`; worker restart after accept | Send; restart | One envelope; ID stored; "completed" webhook → signed document fetched, hashed, compared before Executed | P0 | T16 | EG | Y | IT |
| TC-13-089 | Replayed completion webhook creates no second signature event (battery B4) | TS-13-11 · US-1311 AC-1311-03 · BRL-AUT-08 | Data: "completed" event twice; one with invalid HMAC | Inject | One signature event; invalid HMAC → 401 | P0 | T16, T07 | EG | Y | IT |
| TC-13-090 | Send timeout is Uncertain and reconciled by envelope lookup (battery B3) | TS-13-11 · US-1311 AC-1311-03 · FR-STD-02; NFR-026 | Data: simulator `accept_then_timeout` | Send; advance 5 min | `Uncertain` → lookup finds envelope → OutForSignature; 0 resends | P0 | T18 | ST | Y | SYS |
| TC-13-091 | Declined or expired signature window | TS-13-11 · US-1311 AC-1311-04 · NT-015 | Data: provider "declined"; second contract with window expiry | Inject | `Declined` with NT-015 High; second `Expired` | P1 | T01 | ST | Y | SYS |
| TC-13-092 | AI agent identity cannot call the e-sign tool | TS-13-11 · US-1311 AC-1311-05 · BRL-AI-07, BRL-CTR-04 | Pre: R20 token for AG-020 | Call e-sign tool | Tool registry denies; audit; 0 provider calls | P0 | T07 | EP | Y | SYS |
| TC-13-093 | Contract: provider responses normalised (battery B1) | TS-13-11 · US-1311 · FR-ADP-01; RECOMMENDATION-054 | Pre: PP-04 + recorded fixtures (sent, declined, rate limited, timeout) | Replay | sent / permanent / retryable / uncertain | P1 | T01 | EP | Y | CT |
| TC-13-094 | E-sign credentials are references; sandbox only outside prod (batteries B5, B6) | TS-13-11 · US-1311 · NFR-004; ABAC-12 | Pre: `staging` with a live key configured | Start service; scan responses and logs | Start-up check fails on the live key; no secret in responses or logs | P0 | T07 | EG | Y | SYS |

#### Group TC-13-I: Equivalence partitioning – portal agreement review and e-signature (US-1312)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-095 | Authorised signatory re-verifies with OTP and signs via the provider | TS-13-12 · US-1312 AC-1312-01 · FR-W24; NX-05 | Pre: PP-03, `registrar@kalinga.example` with grant on CT-14; authority evidence AL-3 | Open; declare authority; OTP; sign | Status "Signed by Kalinga College"; after all parties sign and hashes match, Executed and NX-05 sends the signed copy | P0 | T01 | UC | Y | SYS |
| TC-13-096 | Old revision link is refused when rev 2 exists | TS-13-12 · US-1312 AC-1312-02 · BRL-CTR-02 | Data: rev 2 created; open rev 1 link | Attempt sign | "This version is no longer valid"; no signature | P0 | T19 | EP | Y | SYS |
| TC-13-097 | Sign stays disabled without the authority declaration | TS-13-12 · US-1312 AC-1312-03 · BRL-CTR-03 | Data: declaration unticked | Click Sign; call API | Button disabled; API 422 `AUTHORITY_REQUIRED` | P0 | T19 | EP | Y | SYS |
| TC-13-098 | Provider down: signed-PDF path offered only if Legal enabled it | TS-13-12 · US-1312 AC-1312-04 · DEC-023 | Data: provider 503; CT-14 with signed-PDF fallback enabled; CT-15 without | Open both | CT-14 offers upload path; CT-15 shows "Signing temporarily unavailable" | P1 | T01 | EP | Y | SYS |
| TC-13-099 | Agreement viewer is real text, navigable by headings, with labelled declaration and error summary | TS-13-12 · US-1312 AC-1312-05 · NFR-023 | Pre: PP-06 plus PP-07 pass | Navigate by headings; submit without declaration | Headings present; checkbox labelled; error summary focused; axe 0 critical/serious | P1 | T08 | EP | Y | E2E |
| TC-13-100 | Colleague without a grant sees the denied state | TS-13-12 · US-1312 AC-1312-06 · CA-PORTAL; BRL-CTR-03 | Pre: another Kalinga user without grant | Open the link | Denied state; no contract text in the response | P0 | T07, T15 | EP | Y | SYS |
| TC-13-101 | Wrong or expired OTP prevents signing | TS-13-12 · US-1312 Notes · NFR-003 | Data: wrong OTP ×3; OTP older than its validity | Submit | No signature; lockout after configured attempts; audit | P0 | T07 | BVA | Y | SYS |

#### Group TC-13-J: Boundary values and decision table – step-up MFA, delegation and separation of duties (US-1313)

**Common for TC-13-102…104 (MFA freshness, O-12):** Pre: PP-01, `meera` R02 approving P-55 v1. Steps: set session `mfa_at` to the stated age; POST approve.

| ID | Data: MFA age | Expected | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-13-102 | 11 h 59 m 59 s | Approval succeeds | TS-13-13 · US-1313 AC-1313-01 · ABAC-11; BRL-TEN-08 | P0 | T07 | BVA | Y | SYS |
| TC-13-103 | 12 h 00 m 00 s | Approval succeeds (O-12) | TS-13-13 · US-1313 AC-1313-01 · ABAC-11 | P0 | T07 | BVA | Y | SYS |
| TC-13-104 | 12 h 00 m 01 s and 12 h 01 m | 401 `STEP_UP_REQUIRED`; after MFA the same request succeeds | TS-13-13 · US-1313 AC-1313-01 · ABAC-11 | P0 | T07 | BVA | Y | SYS |

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-105 | Delegation to an equal role for 7 days is recorded "on behalf of" | TS-13-13 · US-1313 AC-1313-02 · BRL-APR-09; ABAC-07 | Data: `meera` delegates to another MedMaarg R02 from CLK-0 for 7 days | Delegate approves on day 3 | Approved; audit "on behalf of meera" | P0 | T07 | EP | Y | SYS |
| TC-13-106 | Delegation length boundary 14 days | TS-13-13 · US-1313 AC-1313-02 · BRL-APR-09 | Data: delegation from 2026-12-01 10:00 IST for 14 days; attempt to create 15 days | Approve at 2026-12-15 09:59:59 and 10:00:00 IST; create 15-day delegation | 09:59:59 allowed; 10:00:00 denied (expired, day 15); 15-day creation 422 | P0 | T07 | BVA | Y | SYS |
| TC-13-107 | Delegation to a lower role or another startup is refused | TS-13-13 · US-1313 · BRL-APR-09 | Data: R02 → R03; R02 MedMaarg → R02 OrganicSpec | Create | 422 for both | P0 | T07 | EP | Y | SYS |
| TC-13-108 | Replayed approval with the same nonce returns 409 | TS-13-13 · US-1313 AC-1313-03 · NFR-018 | Data: captured approval request | Replay | 409; one approval record | P0 | T07, T16 | EG | Y | SYS |
| TC-13-109 | Identity provider unavailable: approvals fail closed | TS-13-13 · US-1313 AC-1313-04 · TP-01 | Data: IdP step-up endpoint 503; MFA age 13 h | Approve | Denied with retry message; no fallback without MFA | P0 | T07 | EG | Y | SYS |
| TC-13-110 | Quote author denied; portfolio scope denied | TS-13-13 · US-1313 AC-1313-05 · BRL-APR-01, BRL-TEN-05 | Data: author `sunil`; `vikram` in All startups | Approve each | 403; 409 SSS | P0 | T07, T15 | EP | Y | SYS |

#### Group TC-13-K: State transition – proposal/quote and contract machines (Part 2.3 §2.27.5, §2.27.6)

0-switch map, proposal/quote (17 transitions): Draft→Validating, Validating→PendingApproval (TC-13-029, TC-13-111) · Validating→Draft (TC-13-030) · PendingApproval→Draft (TC-13-111) · PendingApproval→Approved (TC-13-009) · Approved→Sent (TC-13-009) · Sent→Viewed, Viewed→Accepted (TC-13-056) · Viewed→ChangeRequested (TC-13-057) · Sent→Expired, Viewed→Expired (TC-13-058, TC-13-111) · ChangeRequested→Superseded, Approved→Superseded (TC-13-012, TC-13-111) · Sent→Withdrawn (TC-13-111). Contract (16 transitions): Drafting→LegalReview, LegalReview→Drafting (TC-13-113) · LegalReview→LegallyApproved (TC-13-080) · LegallyApproved→OutForSignature (TC-13-095) · OutForSignature→PartiallySigned→Executed (TC-13-095) · OutForSignature→Executed (TC-13-077) · OutForSignature→Declined/Expired (TC-13-091) · Executed→Active, Active→RenewalDue, RenewalDue→Renewed/Terminated, Active→Terminated (TC-13-113).

**Common for TC-13-111…114:** Pre: PP-01; drive each transition through the API with clock control.

| ID | Data (transitions) | Expected | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-13-111 | Quote valid set: Validating→PendingApproval; PendingApproval→Draft (reject with reason); Sent→Expired at validity end without view; Approved→Superseded on new revision; Sent→Withdrawn by sender with reason | Each succeeds once; portal reflects state; withdrawn quote not acceptable | TS-13-14 · US-1302, US-1306 · §2.27.5 | P1 | T01 | ST | Y | SYS |
| TC-13-112 | Quote sneak paths: Draft→Approved; PendingApproval→Sent; Expired→Accepted; Superseded→Accepted; Accepted→ChangeRequested | 409 `INVALID_TRANSITION`; NSE | TS-13-14 · US-1305, US-1306 · BRL-APR-02, BRL-QTE-05 | P0 | T01 | ST | Y | UT |
| TC-13-113 | Contract valid set: Drafting→LegalReview→Drafting (changes required); Executed→Active on 2027-01-01; Active→RenewalDue on 2027-11-01; RenewalDue→Renewed (new contract executed); RenewalDue→Terminated; Active→Terminated (early termination with reason) | Each succeeds once with audit; renewal notice NT raised at RenewalDue | TS-13-14 · US-1309 · §2.27.6; BRL-CTR-05 | P1 | T01 | ST | Y | SYS |
| TC-13-114 | Contract sneak paths: Drafting→OutForSignature; LegalReview→Executed; Declined→Executed; Executed→Drafting | 409; 0 e-sign calls | TS-13-14 · US-1309 · BRL-CTR-04 | P0 | T01 | ST | Y | UT |

#### Group TC-13-L: Pairwise – pricing, tax and approval matrix (factor file `ff_13_quote.yaml`)

Factors: Tax case {intra-state Odisha, inter-state Tamil Nadu, export with LUT} × Discount {0.00, 10.00, 15.00, 20.01} × Lines {1, 3 mixed SKUs, 200} × Creator role {R03, R07}. Constraint: export quotes use PL-OS-USD-2 (USD), domestic quotes PL-OS-12 (INR). Full factorial 72; all-pairs **12 rows** (each tax × discount pair once; other pairs verified). Fixture costs (§6.2.8.1) keep every row above the 25% margin floor except the 20.01% rows, so the discount band alone drives the approver. Mixed lines = TUR-A 2 kg, OS-RICE-25KG 1 bag, GIN-B 3 kg. Tax at the illustrative 18% (ASSUMPTION-169), rounded per line. **Common:** build the quote via API; read lines, tax, total and approval chain; recompute independently in the test with the reference oracle.

| ID | Tax · Discount · Lines · Role | Expected (subtotal; tax; total; approvers) | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-13-115 | Intra · 0.00 · 1 · R07 | 300.00; CGST 27.00 + SGST 27.00; INR 354.00; standard approval only | TS-13-14 · US-1303, US-1304 · BRL-QTE-02, BRL-QTE-03 | P0 | T01 | PW | Y | SYS |
| TC-13-116 | Intra · 10.00 · 200 (TUR-A 2 kg each) · R03 | 54,000.00; CGST 4,860.00 + SGST 4,860.00; INR 63,720.00; R03L | TS-13-14 · US-1304, US-1305 · BRL-APR-04 | P0 | T01 | PW | Y | SYS |
| TC-13-117 | Intra · 15.00 · 3 mixed · R03 | 255.00 + 2,040.00 + 306.00 = 2,601.00; CGST 22.95 + 183.60 + 27.54 = 234.09 and SGST 234.09; INR 3,069.18; R02 | TS-13-14 · US-1303 · BRL-QTE-02 | P0 | T01 | PW | Y | SYS |
| TC-13-118 | Intra · 20.01 · 1 · R03 | 239.97; CGST 21.60 + SGST 21.60; INR 283.17; R01 + R08 | TS-13-14 · US-1305 · BRL-APR-04 | P0 | T01 | PW | Y | SYS |
| TC-13-119 | Inter · 0.00 · 3 mixed · R03 | 300.00 + 2,400.00 + 360.00 = 3,060.00; IGST 54.00 + 432.00 + 64.80 = 550.80; INR 3,610.80; standard | TS-13-14 · US-1303 · BRL-QTE-03 | P0 | T01 | PW | Y | SYS |
| TC-13-120 | Inter · 10.00 · 1 · R07 | 270.00; IGST 48.60; INR 318.60; R03L | TS-13-14 · US-1303 · FR-DM-01 | P0 | T01 | PW | Y | SYS |
| TC-13-121 | Inter · 15.00 · 200 · R07 | 51,000.00; IGST 45.90 × 200 = 9,180.00; INR 60,180.00; R02 | TS-13-14 · US-1304 · BRL-QTE-02 | P0 | T01 | PW | Y | SYS |
| TC-13-122 | Inter · 20.01 · 200 · R03 | 47,994.00; IGST 43.19 × 200 = 8,638.00 (not 8,638.92 from rounding the subtotal); INR 56,632.00; R01 + R08 | TS-13-14 · US-1303 · BRL-QTE-02; EG-02 | P0 | T01 | PW, EG | Y | SYS |
| TC-13-123 | Export LUT · 0.00 · 200 · R03 | USD 800.00; tax 0.00; USD 800.00; standard; no FX applied (DEC-027) | TS-13-14 · US-1303 · BRL-QTE-03, BRL-QTE-04 | P0 | T01 | PW | Y | SYS |
| TC-13-124 | Export LUT · 10.00 · 3 mixed · R07 | 3.60 + 27.00 + 4.05 = USD 34.65; tax 0.00; R03L | TS-13-14 · US-1303 · BRL-QTE-03 | P0 | T01 | PW | Y | SYS |
| TC-13-125 | Export LUT · 15.00 · 1 · R07 | USD 3.40; tax 0.00; R02 | TS-13-14 · US-1304 · BRL-APR-04 | P0 | T01 | PW | Y | SYS |
| TC-13-126 | Export LUT · 20.01 · 3 mixed · R07 | 3.20 + 24.00 + 3.60 = USD 30.80; tax 0.00; R01 + R08 | TS-13-14 · US-1305 · BRL-APR-04 | P0 | T01 | PW | Y | SYS |

#### Group TC-13-M: Use case – commercial journeys

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-13-127 | J-13-01: quote, approval and portal acceptance | TS-13-14 · US-1304, US-1305, US-1306 · FR-A067, FR-A068, FR-W23 | Pre: PP-06 (Chromium, WebKit); lanes `sunil` R07, R03L, `buyer@agro.example`; clock 2026-11-27 | Build Q-88 (10%) → R03L approves with MFA → publish → buyer accepts on 360 px | Accepted rev with hash; NT-014; no invoice; axe 0 critical/serious on A067, A068, W23 | P0 | T01 | UC | Y | E2E |
| TC-13-128 | J-13-02: contract to execution on the signed-PDF path | TS-13-14 · US-1309…US-1312 · FR-A071, FR-A072, FR-W24 | Pre: PP-06; lanes `dev` R10, registrar | Generate CT-14 → legal approval → send → registrar declares authority, OTP, uploads signed PDF with matching hash → countersign | `Executed`; renewal notice date set; closure gate event; NX-05 | P0 | T01 | UC | Y | E2E |

### 6.2.10.3 EP-13 coverage

| Story | AC → TC |
|---|---|
| US-1301 | 01→001 · 02→002 · 03→003, 004 · 04→005 · 05→006 · extra→007, 008 |
| US-1302 | 01→009 · 02→010 · 03→011 · 04→012 · 05→013, 014 · extra→015, 111 |
| US-1303 | 01→016 · 02→017 · 03→018, 019, 020 · 04→021…024 · 05→025 · 06→026 · extra→027, 028, 115…126 |
| US-1304 | 01→029 · 02→030, 031 · 03→032 · 04→033 · 05→034 · 06→035 · extra→127 |
| US-1305 | 01→040, 041, 043, 044 · 02→046 · 03→050 · 04→051 · 05→052, 053 · extra→036…039, 042, 045, 047, 048, 049, 054, 055 |
| US-1306 | 01→056 · 02→057 · 03→058, 059 · 04→060 · 05→061 · extra→062, 063 |
| US-1307 | 01→064 · 02→065 · 03→066 · 04→067 · 05→068 |
| US-1308 | 01→069 · 02→070 · 03→071 · 04→072 |
| US-1309 | 01→073 · 02→074 · 03→075 · 04→076 · 05→077 · 06→078 · extra→079, 113, 114 |
| US-1310 | 01→080, 085 · 02→081, 082 · 03→083 · 04→084 |
| US-1311 | 01→086, 087 · 02→088 · 03→089, 090 · 04→091 · 05→092 · extra→093, 094 |
| US-1312 | 01→095 · 02→096 · 03→097 · 04→098 · 05→099 · 06→100 · extra→101, 128 |
| US-1313 | 01→102, 103, 104 · 02→105, 106 · 03→108 · 04→109 · 05→110 · extra→107 |

All 67 EP-13 AC covered.

---

## 6.2.11 EP-14 Bids, orders and fulfilment (vertical routes)

Stories US-1401…US-1412 (62 AC). FRs: FR-A104, FR-A105, FR-W14, FR-W15, FR-W16, FR-W25; cross-cutting FR-DM-02, FR-DM-03, FR-DM-04, FR-CSM-01. State machines Part 2.3 §2.27.4 (bid) and §2.27.8 (order and fulfilment). Agent exercised deterministically: AG-019 Bid / RFP Analyzer (checklist suggestions only, L1).

### 6.2.11.1 Test scenarios

| TS ID | Scenario | Linked stories / FR | Risk area · Priority | TCs |
|---|---|---|---|---|
| TS-14-01 | Bid desk creates tenders with UTC deadlines and routes them by capability profile | US-1401 · FR-A104, FR-DM-04, FR-CSM-01 | RA-09, RA-01 · **P0** | TC-14-001…011 |
| TS-14-02 | Mandatory eligibility checklist gates the Startup Head's bid/no-bid decision | US-1402 · FR-A104 | RA-09 · **P0** | TC-14-012…018 |
| TS-14-03 | Deadline guard warns, locks approval at deadline − buffer and rejects evidence at or after the deadline | US-1403 · FR-DM-02, FR-A104 | RA-09 · **P0** | TC-14-019…030 |
| TS-14-04 | Human submission evidence, award proof, clarification and withdrawal; the system never submits | US-1404 · FR-A104 | RA-09, RA-19 · **P0** | TC-14-031…039 |
| TS-14-05 | Project requirement intake routes securely with scanned uploads | US-1405 · FR-W15, FR-DM-04 | RA-23, RA-12 · **P0** | TC-14-040…046 |
| TS-14-06 | RFQ intake creates a scoped draft quote that no service identity can approve | US-1406 · FR-W14 | RA-06, RA-15 · **P0** | TC-14-047…052 |
| TS-14-07 | Supplier registration with certificate checks and no self-verification | US-1407 · FR-W16 | RA-08, RA-15 · **P0** | TC-14-053…057 |
| TS-14-08 | Sell and Buy orders with exact reservations, capability checks and separation of duties | US-1408 · FR-A105, FR-CSM-01 | RA-08 · **P0** | TC-14-058…065 |
| TS-14-09 | Fulfilment events are idempotent and never exceed ordered quantity beyond policy tolerance | US-1409 · FR-DM-03, FR-A105 | RA-08 · **P0** | TC-14-066…072 |
| TS-14-10 | Acceptance posts receivables and payables to separate append-only ledgers | US-1410 · FR-A105 | RA-07, RA-08 · **P0** | TC-14-073…079 |
| TS-14-11 | Portal status shows granted orders only, with units and accessible timelines | US-1411 · FR-W25 | RA-15 · **P0** | TC-14-080…085 |
| TS-14-12 | Imports of price lists, availability and open deals are dry-run first, idempotent and consent-safe | US-1412 · FR-A104, FR-A105 (via A103) | RA-18, RA-17 · **P0** | TC-14-086…094, TC-14-101 |
| TS-14-13 | Bid and order state machines; full synthetic deal journeys for AppNAI and OrganicSpec | US-1401…US-1411 · §2.27.4, §2.27.8 | RA-08, RA-09 · **P0** | TC-14-095…100 |

### 6.2.11.2 Test cases

#### Group TC-14-A: Decision table and equivalence partitioning – bid desk and capability routing (US-1401)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-14-001 | Create an AppNAI tender with UTC deadline and dual-zone display | TS-14-01 · US-1401 AC-1401-01 · FR-A104; BRL-BID-01 | Pre: PP-01, AppNAI, `imran` R06. Data: "GeM/2026/B/5501" "AI document classification platform", deadline 2030-06-01 09:00 UTC (portal zone Asia/Kolkata), budget INR 45,00,000.00 | POST bid; open A104 | B-31 `Identified` → `EligibilityCheck`; stored `2030-06-01T09:00:00Z` with portal zone; display "01 Jun 2030 14:30 IST / 09:00 UTC" | P1 | T01 | EP | Y | SYS |
| TC-14-002 | School AI curriculum request proposes EduVerse and blocks AppNAI | TS-14-01 · US-1401 AC-1401-02 · FR-DM-04; DEC-052 | Data: opportunity "AI curriculum for a school" | Convert to bid in AppNAI | Blocked "Education requests route to EduVerse (DEC-052, FR-DM-04)"; EduVerse proposed | P0 | T01 | DT | Y | SYS |
| TC-14-003 | Deadline without time zone fails validation | TS-14-01 · US-1401 AC-1401-03 · BRL-BID-01 | Data: "2030-06-01 09:00" without zone | POST | 422 zone required | P1 | T01 | EP | Y | SYS |
| TC-14-004 | Duplicate tender ID opens the existing bid | TS-14-01 · US-1401 AC-1401-03 · NFR-005 | Data: "GeM/2026/B/5501" again in AppNAI | POST | 200 with existing B-31 (no new row) | P1 | T16 | EG | Y | SYS |
| TC-14-005 | Client tenant with bid_desk creates bids and sees no T1 bids | TS-14-01 · US-1401 AC-1401-04 · NFR-032; DEC-052 | Pre: T2 `b-r06` R06 in "B-Tech" with `bid_desk` | Create bid; list; GET B-31 ID | Bid created in T2; list has 0 T1 rows; B-31 → U404 | P0 | T15 | EP | Y | SYS |
| TC-14-006 | No bid_desk capability or wrong role cannot create bids | TS-14-01 · US-1401 AC-1401-05 · ABAC-08 | Data: `imran`-equivalent R06 in OrganicSpec (no `bid_desk`); `sunil` R07 in AppNAI | POST bid each | 403 both; NSE | P0 | T07 | EP | Y | SYS |

**Routing decision table (BRL-BID-06, FR-DM-04, DEC-052).** Common for TC-14-007…011: Pre: PP-01, T1 portfolio defaults; Steps: submit the intake or conversion; read the proposed startup and the result.

| ID | Request category · entry point · capability state | Expected routing | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-14-007 | External AI/software project · AppNAI site or Admin · AppNAI has `bid_desk` | AppNAI bid desk | TS-14-01 · US-1401 · BRL-BID-06; FR-DM-04, FR-CSM-01 | P0 | T01 | DT | Y | SYS |
| TC-14-008 | External AI development request · entered on the EduVerse site | Routed to AppNAI (FR-DM-04) | TS-14-01 · US-1401 · FR-DM-04 | P0 | T01 | DT | Y | SYS |
| TC-14-009 | Institutional wellness tender · MedMaarg without `bid_desk` grant | Refused "capability required (BRL-BID-06)"; no bid | TS-14-01 · US-1401 · BRL-BID-06; ABAC-08 | P0 | T01 | DT | Y | SYS |
| TC-14-010 | Same tender · MedMaarg after R12 grants `bid_desk` (configuration, no code change) | MedMaarg bid created | TS-14-01 · US-1401 · DEC-052; BRL-TEN-11 | P1 | T01 | DT | Y | SYS |
| TC-14-011 | Category not determinable | Not auto-routed; triage task to the portfolio owner (TP-01) | TS-14-01 · US-1401 · FR-DM-04; BRL-ELG-01 pattern | P1 | T01 | DT | Y | SYS |

#### Group TC-14-B: Decision table – eligibility checklist and bid/no-bid (US-1402)

| Rule | All mandatory items | Waiver approved by R02 | Decider | Result | TC |
|---|---|---|---|---|---|
| E1 | Pass with evidence | – | R02 | Bid available → Preparing | TC-14-012 |
| E2 | One failed | N | R02 | Bid disabled; No-bid only | TC-14-013 |
| E3 | One failed | Y (with reason) | R02 | Bid available | TC-14-014 |
| E4 | Any | – | R06 | 403 | TC-14-016 |
| E5 | Evidence missing on an item | N | R02 | Bid disabled | TC-14-013 |

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-14-012 | All checks evidenced; Startup Head decides Bid (E1) | TS-14-02 · US-1402 AC-1402-01 · FR-A104; BRL-BID-02, BRL-BID-03 | Pre: PP-01, AppNAI, `rhea` R02. Data: B-31 items ISO 27001, turnover ≥ INR 2 crore FY2025-26, India delivery with evidence | POST decision Bid | B-31 `BidDecision` → `Preparing`; decision audited with checklist snapshot | P0 | T01 | DT | Y | SYS |
| TC-14-013 | Failed mandatory item or missing evidence leaves only No-bid (E2, E5) | TS-14-02 · US-1402 AC-1402-02 · BRL-BID-02 | Data: "CMMI Level 3" failed; "India delivery" without evidence | Open decision; POST Bid | Bid option disabled; API 409 `CHECKLIST_INCOMPLETE` | P0 | T19 | DT | Y | SYS |
| TC-14-014 | Approved waiver makes Bid available (E3) | TS-14-02 · US-1402 AC-1402-03 · BRL-BID-02 | Data: waive "local office in Delhi", reason "consortium partner office" | `rhea` waives; decides Bid | Item `Waived`; Bid accepted | P1 | T01 | DT | Y | SYS |
| TC-14-015 | No-bid requires a reason | TS-14-02 · US-1402 AC-1402-04 · BRL-APR-08 | Data: No-bid without reason | POST | 400 | P2 | T01 | EP | Y | SYS |
| TC-14-016 | Bid manager cannot decide (E4) | TS-14-02 · US-1402 AC-1402-05 · BRL-BID-03 | Pre: `imran` R06 | POST Bid | 403 | P0 | T07 | DT | Y | SYS |
| TC-14-017 | Bid manager cannot waive a checklist item | TS-14-02 · US-1402 Notes · BRL-BID-02 | Pre: `imran` | POST waiver | 403 | P0 | T07 | EP | Y | SYS |
| TC-14-018 | AI pre-fill is suggestion only; the agent cannot mark items passed | TS-14-02 · US-1402 Notes · BRL-AI-07; DEC-064 | Data: AG-019 suggestions for 5 items; R20 token | Call checklist update as R20 | Suggestions stored as `suggested`; R20 update 403; items change state only by R06/R02 action | P0 | T07, T14 | EP | Y | SYS |

#### Group TC-14-C: Boundary values – tender deadline guard (US-1403; FR-DM-02; CONFLICT-133)

**Common for TC-14-019…030:** Pre: PP-01, AppNAI; B-31 deadline 2030-06-01 09:00:00 UTC, buffer 24 h (lock instant 2030-05-31 09:00:00 UTC) unless stated; trusted server clock via clock control. Steps: advance the clock and perform the action. Expected as listed.

| ID | Data (instant · action) | Expected | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-14-019 | 2030-05-25, 05-29 and 05-31 at 09:00:00 UTC with 2 checklist items open; repeat with all items closed | NT-020 Normal, High, Critical at those instants; no NT-020 when no item is open | TS-14-03 · US-1403 AC-1403-01 · NT-020; O-21 | P1 | T01 | BVA | Y | SYS |
| TC-14-020 | 2030-05-31 08:59:59 UTC · R02 approves submission | Accepted; `ReadyToSubmit` | TS-14-03 · US-1403 AC-1403-02 · BRL-BID-01 | P0 | T01 | BVA | Y | SYS |
| TC-14-021 | 2030-05-31 09:00:00 UTC · R02 approves submission | Rejected "Within submission buffer (BRL-BID-01)"; exception created; state unchanged | TS-14-03 · US-1403 AC-1403-02 · BRL-BID-01 | P0 | T01 | BVA | Y | SYS |
| TC-14-022 | Evidence with portal timestamp 2030-06-01 09:00:00 UTC | Rejected; B-31 `Expired`; award cannot be recorded; 0 external calls (FR-DM-02) | TS-14-03 · US-1403 AC-1403-03 · FR-DM-02; DEC-053 | P0 | T19 | BVA | Y | SYS |
| TC-14-023 | Evidence with portal timestamp 2030-06-01 08:59:59 UTC recorded at 2030-06-01 11:00 UTC after the buffer lock, with R02 acknowledgement | Accepted, flagged "inside buffer"; `Submitted` (O-21) | TS-14-03 · US-1403 AC-1403-03 · CONFLICT-133 | P0 | T19 | BVA | Y | SYS |
| TC-14-024 | Same evidence without R02 acknowledgement | Held pending acknowledgement; state not Submitted; R02 task created | TS-14-03 · US-1403 AC-1403-03 · CONFLICT-133 | P0 | T19 | DT | Y | SYS |
| TC-14-025 | Viewer zone America/Los_Angeles | "01 Jun 2030 02:00 PDT / 09:00 UTC" | TS-14-03 · US-1403 AC-1403-04 · BRL-MTG-03 pattern | P2 | T13 | EP | Y | E2E |
| TC-14-026 | Scheduler down 2030-05-31 08:00–10:00 UTC | On recovery the lock and the Critical warning are applied once; NT-021; no duplicate notifications (BRL-AUT-10) | TS-14-03 · US-1403 AC-1403-05 · BRL-AUT-10; NT-021 | P0 | T12, T16 | EG | Y | SYS |
| TC-14-027 | `imran` R06 changes the buffer | 403 | TS-14-03 · US-1403 AC-1403-06 | P1 | T07 | EP | Y | SYS |
| TC-14-028 | `rhea` R02 sets buffer 1 h, 1 h 59 m, 2 h | 1 h and 1 h 59 m → 422 "minimum 2 h"; 2 h accepted | TS-14-03 · US-1403 AC-1403-06 · BRL-BID-01 | P1 | T01 | BVA | Y | SYS |
| TC-14-029 | Request carries client timestamp `2030-05-31T08:00:00Z` while server clock is 09:00:01 | Server time used; approval rejected; client value ignored and logged | TS-14-03 · US-1403 Notes · BRL-BID-01 | P0 | T07 | EG | Y | SYS |
| TC-14-030 | Buffer 2 h: approval at 2030-06-01 06:59:59 and 07:00:00 UTC | First accepted; second rejected | TS-14-03 · US-1403 D6 · BRL-BID-01 | P0 | T01 | BVA | Y | SYS |

#### Group TC-14-D: State transition and equivalence partitioning – submission evidence, award and withdrawal (US-1404)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-14-031 | Record a human portal submission with receipt hash | TS-14-04 · US-1404 AC-1404-01 · FR-A104; BRL-BID-04 | Pre: PP-01, AppNAI, `imran`; B-31 `ReadyToSubmit`. Data: reference "GEM-SUB-88812", timestamp 2030-05-30 11:20 UTC, receipt PDF | POST evidence | Receipt SHA-256 stored; B-31 `Submitted`; KPI-11 counts the submission | P0 | T01 | ST | Y | SYS |
| TC-14-032 | Evidence without receipt or reference is refused | TS-14-04 · US-1404 D4 · BRL-BID-04 | Data: missing receipt; then missing reference | POST each | 422; state unchanged | P0 | T01 | EP | Y | SYS |
| TC-14-033 | Award without a document is refused | TS-14-04 · US-1404 AC-1404-02 · BRL-BID-05 | Data: "Awarded" with no attachment | POST | 422 BRL-BID-05 | P0 | T19 | EP | Y | SYS |
| TC-14-034 | Award with letter verified by R02 is tracked separately from Signed and Paid | TS-14-04 · US-1404 AC-1404-02 · BRL-BID-05; DEC-054; BR-S045 | Data: award letter PDF | `imran` attaches; `rhea` verifies | B-31 `Awarded`; deal shows Awarded, Signed = No, Paid = No; deal not Won-Contracted | P0 | T01 | ST | Y | SYS |
| TC-14-035 | Clarification loop returns to Submitted | TS-14-04 · US-1404 AC-1404-03 · §2.27.4 | Data: buyer query; response evidence | Record query; record response | `Clarification` → `Submitted` | P1 | T01 | ST | Y | SYS |
| TC-14-036 | AI agent cannot use any portal submission tool | TS-14-04 · US-1404 AC-1404-04 · DEC-053; BRL-AI-07 | Pre: R20 token for AG-019/AG-020 | Call submission tool | Registry denies; audit entry; 0 external calls | P0 | T07 | EP | Y | SYS |
| TC-14-037 | Withdrawal is pending Startup Head approval with reason | TS-14-04 · US-1404 AC-1404-05 · §2.27.4 | Pre: `imran` | POST withdraw {reason} | Pending R02; on `rhea` approval → `Withdrawn` | P1 | T01 | ST | Y | SYS |
| TC-14-038 | Duplicate evidence with the same receipt hash creates no second record | TS-14-04 · US-1404 D4 · NFR-005 | Data: same receipt uploaded twice | POST twice | One evidence record | P1 | T16 | EG | Y | SYS |
| TC-14-039 | Submission evidence before ReadyToSubmit is refused | TS-14-04 · US-1404 · BRL-BID-03 | Data: B-32 `Preparing` | POST evidence | 409 `INVALID_TRANSITION` | P0 | T01 | ST | Y | SYS |

#### Group TC-14-E: Equivalence partitioning – project requirement, RFQ and supplier intake (US-1405, US-1406, US-1407)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-14-040 | AI project requirement creates one lead routed to AppNAI | TS-14-05 · US-1405 AC-1405-01 · FR-W15; FR-DM-04 | Pre: PP-02 `appnai.example`. Data: "Computer vision QA for a factory line", deadline 2027-02-15 17:00 IST, INR 25,00,000.00, consent | Submit | One lead routed to AppNAI | P1 | T01 | EP | Y | SYS |
| TC-14-041 | Anonymous visitor is asked to sign in before uploading | TS-14-05 · US-1405 AC-1405-02 · NFR-021 | Pre: PP-02 anonymous | Attach file | "Sign in to upload"; upload API 401 | P1 | T07 | EP | Y | E2E |
| TC-14-042 | Infected file is rejected and not stored | TS-14-05 · US-1405 AC-1405-02 · NFR-021 | Pre: PP-03 signed in. Data: EICAR file | Upload | Rejected with reason; no object in storage | P0 | T07 | EG | Y | SYS |
| TC-14-043 | Budget without currency or past deadline fails | TS-14-05 · US-1405 AC-1405-03 | Data: budget "2500000"; deadline 2026-11-30 | Submit | 422 for each | P2 | T01 | EP | Y | SYS |
| TC-14-044 | Scanner down: uploads quarantined until clean | TS-14-05 · US-1405 AC-1405-04 | Data: scanner 503 then clean | Upload; restore scanner | Quarantined, not attached; attached after clean result | P1 | T12 | EG | Y | SYS |
| TC-14-045 | Submitter cannot read another enquiry | TS-14-05 · US-1405 AC-1405-05 · CA-PORTAL | Data: other enquiry ID | GET | 404 | P0 | T15 | EP | Y | SYS |
| TC-14-046 | Sensitive identifiers in free text are redacted at intake | TS-14-05 · US-1405 Links · BRL-PRV-06 | Data: description containing a PAN-like number | Submit | Stored redacted; lead created | P0 | T19 | EG | Y | SYS |
| TC-14-047 | RFQ creates a draft quote with price-list values and sends nothing | TS-14-06 · US-1406 AC-1406-01 · FR-W14; DEC-064 | Pre: PP-02 `organicspec.example`. Data: 2 kg TUR-A to Kolkata by 2026-12-20 | Submit | One RFQ; quote draft for R07 with 150.00/kg; 0 outbound messages to the buyer except NX acknowledgement if eligible | P0 | T01 | EP | Y | SYS |
| TC-14-048 | Unit not allowed for the SKU | TS-14-06 · US-1406 AC-1406-02 · BRL-QTE-07 | Data: unit "litre" | UI list; API | Not offered; API 400 | P1 | T01 | EP | Y | SYS |
| TC-14-049 | Duplicate RFQ with the same key | TS-14-06 · US-1406 AC-1406-03 · CA-INTAKE | Data: same idempotency key twice | Submit twice | One RFQ | P0 | T16 | EG | Y | SYS |
| TC-14-050 | No service identity can approve the draft quote | TS-14-06 · US-1406 AC-1406-04 · BRL-AUT-01; BRL-AI-07 | Pre: R19 and R20 tokens | POST approve | 403 both; approval only by humans per US-1305 | P0 | T07 | EP | Y | SYS |
| TC-14-051 | Portal buyer lists only her own RFQs | TS-14-06 · US-1406 AC-1406-05 · ABAC-09 | Pre: PP-03 `buyer@agro.example` | GET RFQs | Only RFQs under her grants | P0 | T15 | EP | Y | SYS |
| TC-14-052 | Quantity 0 rejected | TS-14-06 · US-1406 D4 · BRL-QTE-07 | Data: qty 0 | Submit | 422 | P2 | T01 | BVA | Y | SYS |
| TC-14-053 | Supplier registration creates a review task | TS-14-07 · US-1407 AC-1407-01 · FR-W16 | Pre: PP-02. Data: "Koraput Organic FPO", turmeric Grade A, 500 kg/month, lead time 10 days, NPOP certificate valid to 2027-08-31 | Submit | Review task for R07; status `Received` | P2 | T01 | EP | Y | SYS |
| TC-14-054 | Expired certificate flags the product line | TS-14-07 · US-1407 AC-1407-02 · BRL-QTE-07 | Data: expiry 2026-10-31 (and boundary 2026-12-01 at CLK-0: valid through the day) | Submit; R07 verifies | 2026-10-31 → "certificate expired", cannot verify; 2026-12-01 → verifiable today | P1 | T01 | BVA | Y | SYS |
| TC-14-055 | Same legal name and GSTIN updates the existing application | TS-14-07 · US-1407 AC-1407-03 · NFR-005 | Data: same GSTIN `21AAAAA0000A1Z5` (synthetic) | Submit again | Existing application updated; no duplicate | P1 | T16 | EG | Y | SYS |
| TC-14-056 | Supplier cannot set itself Verified | TS-14-07 · US-1407 AC-1407-04 · CA-PORTAL | Pre: PP-03 supplier | PATCH status Verified | 403 | P0 | T07 | EP | Y | SYS |
| TC-14-057 | or-IN supplier form | TS-14-07 · US-1407 D8 · DEC-026 | Pre: approved or-IN form | Submit with Odia text | Stored NFC; labels and errors in Odia | P3 | T13 | EP | Y | E2E |

#### Group TC-14-F: Boundary values and error guessing – order desk with reservation (US-1408)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-14-058 | Sell order approved, priced and reserved | TS-14-08 · US-1408 AC-1408-01 · FR-A105, FR-CSM-01; BRL-ORD-01, BRL-ORD-04 | Pre: PP-01, OrganicSpec, `sunil` creates, `gopal` approves. Data: TUR-A available 50 kg; SO-71 2 kg at 150.00 with 10% | Create; approve | Total INR 270.00 before tax; 2 kg reserved; available 48 kg; SO-71 `Approved` | P0 | T01 | BVA | Y | SYS |
| TC-14-059 | Quantity equal to availability succeeds; one more kilogram fails | TS-14-08 · US-1408 AC-1408-02 · BRL-ORD-04 | Data: SO-72 48 kg, then SO-73 1 kg | Approve each | SO-72 approved, available 0; SO-73 409 "Insufficient available quantity" | P0 | T01 | BVA | Y | SYS |
| TC-14-060 | Two concurrent approvals for the last 2 kg: exactly one succeeds | TS-14-08 · US-1408 AC-1408-03 · NFR-005 | Pre: PP-05. Data: available 2 kg; SO-74 and SO-75 each 2 kg | Approve concurrently (20 repetitions) | Exactly one approved each time; the other 409; availability never negative | P0 | T16 | EG | Y | IT |
| TC-14-061 | Cancellation releases the reservation and is audited | TS-14-08 · US-1408 AC-1408-04 · BRL-ORD-04 | Data: SO-71 Approved | Cancel with reason | 2 kg back to availability; `Cancelled`; audit | P0 | T01 | ST | Y | SYS |
| TC-14-062 | Buy order reserves nothing and targets the payable ledger | TS-14-08 · US-1408 AC-1408-05 · BRL-ORD-01, BRL-ORD-06 | Data: PO-15 500 kg from Koraput Organic FPO | Create; approve | No reservation change; ledger target `Payable` | P0 | T01 | EP | Y | SYS |
| TC-14-063 | Creator cannot approve own order | TS-14-08 · US-1408 AC-1408-06 · BRL-APR-01 | Pre: `sunil` | Approve SO-71 | 403 | P0 | T07 | EP | Y | SYS |
| TC-14-064 | No order_desk capability, no order | TS-14-08 · US-1408 AC-1408-06 · ABAC-08 | Pre: R07 in AppNAI | POST order | 403 | P0 | T07 | EP | Y | SYS |
| TC-14-065 | Issued Sell order not acknowledged within 14 days releases its reservation | TS-14-08 · US-1408 Notes · ASSUMPTION-166; DEC-045; O-19 | Data: SO-76 issued 2026-12-01 10:00 IST | Check at 2026-12-15 09:59:59 and 10:00:00 IST | Reserved at first; released and flagged at second; order owner notified | P1 | T01 | BVA | Y | SYS |

#### Group TC-14-G: Boundary values and property-based tests – fulfilment idempotency (US-1409; FR-DM-03)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-14-066 | Worked example FR-DM-03 | TS-14-09 · US-1409 AC-1409-01 · FR-DM-03; BRL-ORD-02, BRL-ORD-03; NT-022 | Pre: PP-01, SO-71 line 2 kg `Acknowledged` | Record 1 kg `DLV-71-1`; again `DLV-71-1`; 1 kg `DLV-71-2`; 2 kg `DLV-71-3` | PartiallyFulfilled 1/2 kg; duplicate no effect; Fulfilled 2/2 kg; over-delivery rejected and NT-022 sent | P0 | T16, T01 | BVA | Y | SYS |
| TC-14-067 | Tolerance 2% on 100 kg: 102.00 accepted, 102.01 rejected | TS-14-09 · US-1409 AC-1409-02 · BRL-ORD-02 | Data: policy 2%; cumulative 101.00 then +1.00, then +0.01 | Record | 102.00 accepted; 102.01 rejected | P0 | T01 | BVA | Y | SYS |
| TC-14-068 | Default tolerance 0%: 100.00 accepted, 100.01 rejected | TS-14-09 · US-1409 · BRL-ORD-02 | Data: policy default | Record | As stated | P0 | T01 | BVA | Y | SYS |
| TC-14-069 | Concurrent duplicate events keep one row | TS-14-09 · US-1409 AC-1409-03 · NFR-005; BRL-ORD-03 | Pre: PP-05. Data: same key from two workers | Submit simultaneously | Unique constraint keeps one row; both callers get success; one effect | P0 | T16 | EG | Y | IT |
| TC-14-070 | Unit mismatch without approved conversion is rejected | TS-14-09 · US-1409 AC-1409-04 · BRL-QTE-07 | Data: delivery 0.02 quintal on a kg line | Record | 422 unit mismatch | P1 | T01 | EP | Y | SYS |
| TC-14-071 | Finance cannot record fulfilment | TS-14-09 · US-1409 AC-1409-05 | Pre: `lata` R08 | POST delivery | 403 | P1 | T07 | EP | Y | SYS |
| TC-14-072 | Property: cumulative fulfilled ≤ ordered × (1 + tolerance) for any event sequence | TS-14-09 · US-1409 · BRL-ORD-02, BRL-ORD-03; §6.1.11.7 | Pre: PP-04 Hypothesis `release` | Random sequences with duplicates and reorderings | Invariant holds; duplicates never change totals | P0 | T16 | PBT | Y | UT |

#### Group TC-14-H: Boundary values – acceptance and ledger postings (US-1410)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-14-073 | Buyer acceptance posts a receivable of INR 318.60 | TS-14-10 · US-1410 AC-1410-01 · FR-A105; BRL-ORD-05; KPI-12 | Pre: PP-03 buyer; SO-71 `Fulfilled` | Accept in W25 | ReceivableEntry 318.60 (270.00 + CGST 24.30 + SGST 24.30); SO-71 `LedgerPosted`; no payment record (DEC-022) | P0 | T01 | EP | Y | SYS |
| TC-14-074 | Buy receipt posts a payable and never nets the receivable | TS-14-10 · US-1410 AC-1410-02 · BRL-ORD-06; KPI-14 | Data: counterparty is both buyer (SO-77, receivable 1,000.00) and supplier (PO-15) | Accept PO-15 receipt | PayableEntry posted; receivable balance unchanged at 1,000.00; no netting entry | P0 | T01, T19 | EP | Y | SYS |
| TC-14-075 | Deemed acceptance at exactly 7 days | TS-14-10 · US-1410 AC-1410-03 · BRL-ORD-05 | Data: fulfilled 2026-12-01 10:00 IST | Check at 2026-12-08 09:59 and 10:00 IST | No posting at 09:59; deemed acceptance posts at 10:00 | P0 | T01 | BVA | Y | SYS |
| TC-14-076 | Partial acceptance posts 1 kg and opens a dispute | TS-14-10 · US-1410 AC-1410-04 · GAP-158 | Data: accept 1 of 2 kg; dispute 1 kg | Accept partially | Receivable 135.00 + CGST 12.15 + SGST 12.15 = 159.30; dispute case; state `PartiallyAccepted` → `LedgerPosted` | P0 | T01 | EP | Y | SYS |
| TC-14-077 | Corrections are reversing entries; edits refused | TS-14-10 · US-1410 AC-1410-05 · BRL-FIN-05 | Pre: `lata` R08 | PATCH amount; POST reversal with reason | PATCH 405/409; reversal entry with reason; balance correct; original unchanged | P0 | T01 | EG | Y | SYS |
| TC-14-078 | External user cannot settle a receivable | TS-14-10 · US-1410 AC-1410-06 · CA-PORTAL | Pre: PP-03 buyer | POST settle | 403 | P0 | T07 | EP | Y | SYS |
| TC-14-079 | Replayed acceptance event posts once | TS-14-10 · US-1410 · NFR-005 | Data: acceptance event delivered twice | Process | One ReceivableEntry | P0 | T16 | EG | Y | IT |

#### Group TC-14-I: Equivalence partitioning – portal order status (US-1411)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-14-080 | Partial delivery shown with units, ETA and last update | TS-14-11 · US-1411 AC-1411-01 · FR-W25 | Pre: PP-03 buyer; SO-71 1 of 2 kg | Open W25 | "1 of 2 kg delivered", ETA, last update time | P1 | T01 | EP | Y | SYS |
| TC-14-081 | Discrepancy moves the order to Disputed and notifies the coordinator | TS-14-11 · US-1411 AC-1411-02 · BRL-ORD-05 | Data: "0.2 kg short" | Raise discrepancy | `Disputed`; R07 notified | P1 | T01 | ST | Y | SYS |
| TC-14-082 | Empty state and 200-order pagination of 20 per page | TS-14-11 · US-1411 AC-1411-03 | Data: user with 0 orders; user with 200 | Open list | Empty-state text; 10 pages of 20 with stable order | P2 | T01 | BVA | Y | E2E |
| TC-14-083 | Milestone timeline is an ordered list with text status | TS-14-11 · US-1411 AC-1411-04 · NFR-023 | Pre: PP-06 | Inspect DOM and axe | `<ol>` with text statuses; no colour-only meaning; axe 0 critical/serious | P1 | T08 | EP | Y | E2E |
| TC-14-084 | Another buyer's order returns 404 and is never cached | TS-14-11 · US-1411 AC-1411-05 · CA-PORTAL; BRL-PUB-05 | Data: request PO-15 (not granted) | GET via portal and CDN | 404; `Cache-Control: private, no-store`; no CDN hit | P0 | T15 | EP | Y | SYS |
| TC-14-085 | Accept and dispute actions only on granted orders | TS-14-11 · US-1411 Notes · ABAC-09 | Data: buyer POST accept on PO-15 | POST | U404; NSE | P0 | T07 | EP | Y | SYS |

#### Group TC-14-J: Equivalence partitioning and boundary values – data migration imports (US-1412; T11)

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-14-086 | Dry run reports 117 valid and 3 invalid rows and writes nothing | TS-14-12 · US-1412 AC-1412-01 · DEC-039; BRL-QTE-07 | Pre: PP-01, OrganicSpec, `sana` R12. Data: `organicspec_pricelist_v1.csv` 120 rows, 3 invalid units | Upload dry run | Report with row numbers; 0 rows written (DB row counts unchanged) | P1 | T11 | EP | Y | SYS |
| TC-14-087 | Commit creates a Draft price version needing Finance approval | TS-14-12 · US-1412 AC-1412-02 · BRL-QTE-01 | Data: 117 valid rows | Commit | PV-OS-13 `Draft`; not usable by quotes until `lata` R08 approves | P0 | T11 | EP | Y | SYS |
| TC-14-088 | Open bids keep UTC deadlines; past-deadline bids import as Expired | TS-14-12 · US-1412 AC-1412-03 · BRL-BID-01 | Data: 4 AppNAI bids, one with deadline 2026-11-30 09:00 UTC | Import at CLK-0 | 3 in `EligibilityCheck` with exact UTC deadlines; 1 `Expired` | P0 | T11 | BVA | Y | SYS |
| TC-14-089 | Repeated order reference rejected as duplicate | TS-14-12 · US-1412 AC-1412-04 · BRL-ORD-01 | Data: file repeats "SO-IMP-9" | Import | Second row rejected "duplicate" | P1 | T11, T16 | EG | Y | SYS |
| TC-14-090 | 10,000 availability rows import asynchronously with progress and audit | TS-14-12 · US-1412 AC-1412-04 · NFR-028 | Data: 10,000 rows | Import | Job progress visible; completes; audit with counts; API stays within p95 targets during the job | P2 | T11, T03 | BVA | Y | SYS |
| TC-14-091 | Growth manager cannot import price lists | TS-14-12 · US-1412 AC-1412-05 | Pre: R03 | Upload | 403 | P1 | T07 | EP | Y | SYS |
| TC-14-092 | Re-running the same file creates no duplicates | TS-14-12 · US-1412 · NFR-005; §6.1.14.5 | Data: same committed file again | Commit | Run report all "unchanged"; 0 new rows | P0 | T11, T16 | EG | Y | SYS |
| TC-14-093 | Imported deal contacts stay ineligible until consent is verified | TS-14-12 · US-1412 Notes · DEC-039; BRL-ELG-03 | Data: open deals with 25 contacts | Import; enrol a contact | Enrol refused (no verified lawful basis) | P0 | T19 | EP | Y | SYS |
| TC-14-094 | A T2 import never writes T1 rows | TS-14-12 · US-1412 D6 · BRL-TEN-03 | Pre: `b-admin` R12. Data: file containing a T1 startup code | Import | Rows scoped to T2; foreign scope codes rejected; 0 T1 rows changed | P0 | T15 | EG | Y | SYS |
| TC-14-101 | Import error report link is classification-redacted and expires after 72 h | TS-14-12 · US-1412 Links · BRL-PRV-07; DEC-039 | Data: dry-run report for a file containing supplier contact emails; link created 2026-12-01 10:00 IST | Download at 2026-12-04 09:59:59 and 10:00:00 IST; inspect content | First download works with contact emails masked; second returns expired (410/404); access logged | P1 | T19 | BVA | Y | SYS |

#### Group TC-14-K: State transition and use case – bid and order machines; full synthetic deals

0-switch map, bid (16 transitions): Identified→EligibilityCheck (TC-14-001) · EligibilityCheck→BidDecision, BidDecision→Preparing (TC-14-012) · EligibilityCheck→NoBid, BidDecision→NoBid (TC-14-095) · Preparing→ReadyToSubmit (TC-14-020) · ReadyToSubmit→Expired, Preparing→Expired (TC-14-022, TC-14-095) · ReadyToSubmit→Submitted (TC-14-031) · Submitted→Clarification→Submitted (TC-14-035) · Submitted→Awarded (TC-14-034) · Submitted→NotAwarded (TC-14-095) · Submitted→Withdrawn (TC-14-037). Order (20 transitions): Draft→PendingApproval→Approved (TC-14-058) · PendingApproval→Draft (TC-14-097) · Approved→Issued→Acknowledged (TC-14-097) · Acknowledged→PartiallyFulfilled→Fulfilled (TC-14-066) · Acknowledged→Fulfilled (TC-14-097) · Fulfilled→Accepted→LedgerPosted (TC-14-073) · Fulfilled→Disputed (TC-14-081) · Disputed→Accepted, Disputed→PartiallyAccepted→LedgerPosted (TC-14-076, TC-14-097) · LedgerPosted→Closed (TC-14-097) · Draft→Cancelled, Issued→Cancelled (TC-14-097) · Approved→Cancelled (TC-14-061).

**Common for TC-14-095…098:** Pre: PP-01; drive transitions through the API with clock control.

| ID | Data (transitions) | Expected | Links | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|
| TC-14-095 | Bid valid set: EligibilityCheck→NoBid (mandatory failed, decision No-bid with reason); BidDecision→NoBid; Preparing→Expired (deadline passed before ReadyToSubmit); Submitted→NotAwarded (result recorded with evidence) | Each once with audit; terminal states accept no further event | TS-14-13 · US-1402…US-1404 · §2.27.4 | P1 | T01 | ST | Y | SYS |
| TC-14-096 | Bid sneak paths: Identified→Submitted; Preparing→Submitted; Expired→Submitted; NoBid→Preparing; Awarded→Withdrawn | 409 `INVALID_TRANSITION`; NSE | TS-14-13 · US-1403, US-1404 · BRL-BID-01, BRL-BID-04; DEC-053 | P0 | T01 | ST | Y | UT |
| TC-14-097 | Order valid set: PendingApproval→Draft (rejected); Approved→Issued; Issued→Acknowledged; Acknowledged→Fulfilled (single full event); Disputed→Accepted (resolved); LedgerPosted→Closed (settled per EP-15 signal); Draft→Cancelled; Issued→Cancelled (mutual, reservation released) | Each once with audit; reservations correct after each | TS-14-13 · US-1408…US-1410 · §2.27.8 | P1 | T01 | ST | Y | SYS |
| TC-14-098 | Order sneak paths: Draft→Fulfilled; Cancelled→Approved; Fulfilled→PartiallyFulfilled; LedgerPosted→Disputed; Closed→Accepted | 409; no ledger or reservation change | TS-14-13 · US-1409, US-1410 · BRL-ORD-02, BRL-FIN-05 | P0 | T01 | ST | Y | UT |

| ID | Title | Links | Preconditions · Test data | Steps | Expected result | P | Type | Tech | Auto | Lvl |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-14-099 | J-14-01: AppNAI full synthetic bid route (W4 exit evidence) | TS-14-13 · US-1401…US-1404 · FR-A104; UAT-PK-AN; AP-03 | Pre: PP-06; lanes `imran`, `rhea`, `dev`; clock control | Create B-31 → checklist → Bid → proposal and quote approvals (EP-13) → ReadyToSubmit before lock → record human submission → clarification → award verified | B-31 Awarded; deal shows Awarded ≠ Signed ≠ Paid; 0 automated submissions; axe 0 critical/serious on A104 | P0 | T01 | UC | Y | E2E |
| TC-14-100 | J-14-02: OrganicSpec full synthetic order route (W4 exit evidence) | TS-14-13 · US-1406…US-1411 · FR-W14, FR-A105, FR-W25; UAT-PK-OS; AP-04 | Pre: PP-06; lanes buyer, `sunil`, `gopal`, `lata` | W14 RFQ → quote → approval → buyer accepts → SO-71 approved and reserved → issued → partial then full delivery (with a duplicate event) → W25 acceptance → receivable posted | Exact quantities; duplicate no effect; ReceivableEntry 318.60; PO-15 payable separate; KPI-12 updated | P0 | T01 | UC | Y | E2E |

### 6.2.11.3 EP-14 coverage

| Story | AC → TC |
|---|---|
| US-1401 | 01→001 · 02→002 · 03→003, 004 · 04→005 · 05→006 · extra→007…011 |
| US-1402 | 01→012 · 02→013 · 03→014 · 04→015 · 05→016 · extra→017, 018 |
| US-1403 | 01→019 · 02→020, 021 · 03→022, 023, 024 · 04→025 · 05→026 · 06→027, 028 · extra→029, 030 |
| US-1404 | 01→031 · 02→033, 034 · 03→035 · 04→036 · 05→037 · extra→032, 038, 039 |
| US-1405 | 01→040 · 02→041, 042 · 03→043 · 04→044 · 05→045 · extra→046 |
| US-1406 | 01→047 · 02→048 · 03→049 · 04→050 · 05→051 · extra→052 |
| US-1407 | 01→053 · 02→054 · 03→055 · 04→056 · extra→057 |
| US-1408 | 01→058 · 02→059 · 03→060 · 04→061 · 05→062 · 06→063, 064 · extra→065 |
| US-1409 | 01→066 · 02→067 · 03→069 · 04→070 · 05→071 · extra→068, 072 |
| US-1410 | 01→073 · 02→074 · 03→075 · 04→076 · 05→077 · 06→078 · extra→079 |
| US-1411 | 01→080 · 02→081 · 03→082 · 04→083 · 05→084 · extra→085 |
| US-1412 | 01→086 · 02→087 · 03→088 · 04→089, 090 · 05→091 · extra→092, 093, 094, 101 |

All 62 EP-14 AC covered.

---

## 6.2.12 Coverage and totals for file b (EP-12 to EP-14)

### 6.2.12.1 Acceptance-criteria coverage

All **178 of 178** acceptance criteria of US-1201…US-1412 have at least one TC (per-story maps in §6.2.9.3, §6.2.10.3, §6.2.11.3), checked mechanically as in file a §6.2.6.1. **Uncovered AC: none.**

### 6.2.12.2 FR → test cases (FRs whose Part 2.1 epic is EP-12…EP-14)

TC count = explicit FR links plus TCs of the stories mapped to the FR in Part 5.2 §5.2.10.1. **25 of 25 FRs covered (100%).** FR-A105 also counts US-1303 because Part 5.2 maps the pricing library to it.

| FR | Aliases (DEC-017) | Stories | TCs (explicit + via story) | TC IDs |
|---|---|---|---|---|
| FR-A056 | SM-UAT-S086 · SM-UX-UAT-A056 | US-1201 | 7 | TC-12-001…007 |
| FR-A057 | SM-UAT-S087 · SM-UX-UAT-A057 | US-1202 | 7 | TC-12-008…014 |
| FR-A058 | SM-UAT-S088 · SM-UX-UAT-A058 | US-1204 | 14 | TC-12-023…031, TC-12-074, TC-12-077…078, TC-12-081, TC-12-083 |
| FR-A059 | SM-UAT-S089 · SM-UX-UAT-A059 | US-1205 | 16 | TC-12-032…041, TC-12-074…076, TC-12-079…080, TC-12-083 |
| FR-A060 | SM-UAT-S090 · SM-UX-UAT-A060 | US-1206, US-1207 | 13 | TC-12-042…054 |
| FR-A061 | SM-UAT-S091 · SM-UX-UAT-A061 | US-1206, US-1208 | 15 | TC-12-042…049, TC-12-055…061 |
| FR-A064 | SM-UAT-S094 · SM-UX-UAT-A064 | US-1210 | 6 | TC-12-068…073 |
| FR-A065 | SM-UAT-S095 · SM-UX-UAT-A065 | US-1301 | 8 | TC-13-001…008 |
| FR-A066 | SM-UAT-S096 · SM-UX-UAT-A066 | US-1302, US-1313 | 17 | TC-13-009…015, TC-13-102…111 |
| FR-A067 | SM-UAT-S097 · SM-UX-UAT-A067 | US-1303, US-1304 | 31 | TC-13-016…035, TC-13-115…117, TC-13-119…125, TC-13-127 |
| FR-A068 | SM-UAT-S098 · SM-UX-UAT-A068 | US-1305, US-1313 | 34 | TC-13-036…055, TC-13-102…110, TC-13-112, TC-13-116, TC-13-118, TC-13-126…127 |
| FR-A069 | SM-UAT-S099 · SM-UX-UAT-A069 | US-1307 | 5 | TC-13-064…068 |
| FR-A070 | SM-UAT-S100 · SM-UX-UAT-A070 | US-1308, US-1313 | 13 | TC-13-069…072, TC-13-102…110 |
| FR-A071 | SM-UAT-S101 · SM-UX-UAT-A071 | US-1309, US-1311 | 19 | TC-13-073…079, TC-13-086…094, TC-13-113…114, TC-13-128 |
| FR-A072 | SM-UAT-S102 · SM-UX-UAT-A072 | US-1310, US-1313 | 16 | TC-13-080…085, TC-13-102…110, TC-13-128 |
| FR-A104 | SM-UAT-S134 · SM-UX-UAT-A104 | US-1401, US-1402, US-1403, US-1404, US-1412 | 52 | TC-14-001…039, TC-14-086…096, TC-14-099, TC-14-101 |
| FR-A105 | SM-UAT-S135 · SM-UX-UAT-A105 | US-1303, US-1408, US-1409, US-1410, US-1412 | 55 | TC-13-016…028, TC-13-115, TC-13-117, TC-13-119…120, TC-13-122…124, TC-14-058…079, TC-14-086…094, TC-14-097…098, TC-14-100…101 |
| FR-W10 | SM-UAT-S010 · SM-UX-UAT-W10 | US-1203 | 9 | TC-12-015…022, TC-12-082 |
| FR-W14 | SM-UAT-S014 · SM-UX-UAT-W14 | US-1406 | 7 | TC-14-047…052, TC-14-100 |
| FR-W15 | SM-UAT-S015 · SM-UX-UAT-W15 | US-1405 | 7 | TC-14-040…046 |
| FR-W16 | SM-UAT-S016 · SM-UX-UAT-W16 | US-1407 | 5 | TC-14-053…057 |
| FR-W20 | SM-UAT-S020 · SM-UX-UAT-W20 | US-1209 | 6 | TC-12-062…067 |
| FR-W23 | SM-UAT-S023 · SM-UX-UAT-W23 | US-1306 | 11 | TC-13-056…063, TC-13-111…112, TC-13-127 |
| FR-W24 | SM-UAT-S024 · SM-UX-UAT-W24 | US-1311, US-1312 | 17 | TC-13-086…101, TC-13-128 |
| FR-W25 | SM-UAT-S025 · SM-UX-UAT-W25 | US-1411 | 7 | TC-14-080…085, TC-14-100 |

### 6.2.12.3 Cross-cutting FRs exercised (explicit links)

| Cross-cutting FR | TCs (count) | TC IDs |
|---|---|---|
| FR-STD-02 | 2 | TC-12-045, TC-13-090 |
| FR-ADP-01 | 2 | TC-12-043, TC-13-093 |
| FR-DM-01 | 2 | TC-13-016, TC-13-120 |
| FR-DM-02 | 1 | TC-14-022 |
| FR-DM-03 | 1 | TC-14-066 |
| FR-DM-04 | 5 | TC-14-002, TC-14-007…008, TC-14-011, TC-14-040 |
| FR-CSM-01 | 2 | TC-14-007, TC-14-058 |

### 6.2.12.4 BRL rules cited by EP-12…EP-14 stories → test cases (explicit links)

**70 of 70 cited rules have at least one TC (100%).** Ranges written in Part 5.2 as "BRL-QTE-01…BRL-QTE-07" are expanded rule by rule.

| BRL rule | TCs (count) | TC IDs | BRL rule | TCs (count) | TC IDs |
|---|---|---|---|---|---|
| BRL-AI-03 | 2 | TC-13-001, TC-13-064 | BRL-ELG-13 | 2 | TC-12-025, TC-12-078 |
| BRL-AI-04 | 1 | TC-13-066 | BRL-ELG-14 | 3 | TC-12-003, TC-12-017, TC-12-024 |
| BRL-AI-05 | 1 | TC-13-002 | BRL-ELG-15 | 1 | TC-12-029 |
| BRL-AI-07 | 5 | TC-13-067, TC-13-092, TC-14-018, TC-14-036, TC-14-050 | BRL-ELG-17 | 2 | TC-12-063, TC-12-073 |
| BRL-APR-01 | 9 | TC-12-012, TC-12-037, TC-12-072, TC-13-013, TC-13-049, TC-13-072, TC-13-084, TC-13-110, TC-14-063 | BRL-ELG-18 | 1 | TC-12-033 |
| BRL-APR-02 | 4 | TC-12-036, TC-13-009, TC-13-080, TC-13-112 | BRL-FIN-05 | 2 | TC-14-077, TC-14-098 |
| BRL-APR-03 | 3 | TC-12-013, TC-12-040, TC-13-085 | BRL-MKT-01 | 2 | TC-12-008, TC-12-041 |
| BRL-APR-04 | 17 | TC-13-032, TC-13-037…047, TC-13-054, TC-13-116, TC-13-118, TC-13-125…126 | BRL-MKT-02 | 2 | TC-12-002, TC-13-003 |
| BRL-APR-05 | 3 | TC-13-010, TC-13-070, TC-13-074 | BRL-MKT-04 | 5 | TC-12-026, TC-12-032, TC-12-075…076, TC-12-081 |
| BRL-APR-06 | 4 | TC-13-050, TC-13-081…083 | BRL-MKT-05 | 4 | TC-12-051…052, TC-12-056…057 |
| BRL-APR-07 | 1 | TC-13-053 | BRL-MKT-06 | 3 | TC-12-003, TC-12-017, TC-12-049 |
| BRL-APR-08 | 3 | TC-12-071, TC-13-084, TC-14-015 | BRL-MKT-10 | 2 | TC-12-027, TC-12-031 |
| BRL-APR-09 | 3 | TC-13-105…107 | BRL-ORD-01 | 3 | TC-14-058, TC-14-062, TC-14-089 |
| BRL-APR-10 | 2 | TC-13-011, TC-13-071 | BRL-ORD-02 | 5 | TC-14-066…068, TC-14-072, TC-14-098 |
| BRL-APR-11 | 3 | TC-12-046, TC-12-058, TC-13-055 | BRL-ORD-03 | 3 | TC-14-066, TC-14-069, TC-14-072 |
| BRL-AUT-01 | 2 | TC-13-069, TC-14-050 | BRL-ORD-04 | 3 | TC-14-058…059, TC-14-061 |
| BRL-AUT-04 | 1 | TC-12-023 | BRL-ORD-05 | 3 | TC-14-073, TC-14-075, TC-14-081 |
| BRL-AUT-05 | 1 | TC-12-059 | BRL-ORD-06 | 2 | TC-14-062, TC-14-074 |
| BRL-AUT-08 | 1 | TC-13-089 | BRL-PRV-06 | 3 | TC-12-020, TC-12-064, TC-14-046 |
| BRL-AUT-10 | 1 | TC-14-026 | BRL-PRV-07 | 1 | TC-14-101 |
| BRL-BID-01 | 9 | TC-14-001, TC-14-003, TC-14-020…021, TC-14-028…030, TC-14-088, TC-14-096 | BRL-PUB-01 | 2 | TC-12-008, TC-12-010 |
| BRL-BID-02 | 4 | TC-14-012…014, TC-14-017 | BRL-PUB-02 | 2 | TC-12-008, TC-12-011 |
| BRL-BID-03 | 3 | TC-14-012, TC-14-016, TC-14-039 | BRL-PUB-03 | 2 | TC-12-001, TC-12-004 |
| BRL-BID-04 | 3 | TC-14-031…032, TC-14-096 | BRL-PUB-05 | 2 | TC-13-061, TC-14-084 |
| BRL-BID-05 | 2 | TC-14-033…034 | BRL-PUB-06 | 1 | TC-12-009 |
| BRL-BID-06 | 2 | TC-14-007, TC-14-009 | BRL-QTE-01 | 5 | TC-13-001, TC-13-004, TC-13-007, TC-13-032, TC-14-087 |
| BRL-CTR-01 | 2 | TC-13-073…074 | BRL-QTE-02 | 7 | TC-13-016…017, TC-13-029, TC-13-115, TC-13-117, TC-13-121…122 |
| BRL-CTR-02 | 3 | TC-13-076, TC-13-086, TC-13-096 | BRL-QTE-03 | 7 | TC-13-018…020, TC-13-115, TC-13-119, TC-13-123…124 |
| BRL-CTR-03 | 4 | TC-13-061, TC-13-079, TC-13-097, TC-13-100 | BRL-QTE-04 | 6 | TC-13-021, TC-13-024, TC-13-033, TC-13-036, TC-13-048, TC-13-123 |
| BRL-CTR-04 | 3 | TC-13-075, TC-13-092, TC-13-114 | BRL-QTE-05 | 3 | TC-13-029, TC-13-058, TC-13-112 |
| BRL-CTR-05 | 2 | TC-13-077, TC-13-113 | BRL-QTE-06 | 3 | TC-13-012, TC-13-051, TC-13-059 |
| BRL-ELG-01 | 1 | TC-14-011 | BRL-QTE-07 | 8 | TC-13-023, TC-13-030…031, TC-14-048, TC-14-052, TC-14-054, TC-14-070, TC-14-086 |
| BRL-ELG-05 | 1 | TC-12-023 | BRL-TEN-03 | 2 | TC-13-008, TC-14-094 |
| BRL-ELG-09 | 1 | TC-12-023 | BRL-TEN-05 | 1 | TC-13-110 |
| BRL-ELG-11 | 1 | TC-12-034 | BRL-TEN-08 | 1 | TC-13-102 |

### 6.2.12.5 Totals for file b

| Epic | Scenarios | TCs | P0 | P1 | P2 | P3 | Automated (Y) | Manual (N) | AC covered |
|---|---|---|---|---|---|---|---|---|---|
| EP-12 | 11 | 83 | 51 | 24 | 6 | 2 | 83 | 0 | 49 / 49 |
| EP-13 | 14 | 128 | 105 | 22 | 1 | 0 | 128 | 0 | 67 / 67 |
| EP-14 | 13 | 101 | 63 | 30 | 7 | 1 | 101 | 0 | 62 / 62 |
| **Total** | **38** | **312** | **219** | **76** | **14** | **3** | **312** | **0** | **178 / 178** |

**By type:**

| Type | Name | TCs tagged |
|---|---|---|
| T01 | Functional | 158 |
| T03 | Performance (load) | 1 |
| T07 | Security | 61 |
| T08 | Accessibility | 4 |
| T11 | Data migration | 6 |
| T12 | DR / resilience | 2 |
| T13 | Localization | 5 |
| T14 | AI (deterministic gateway/guardrail) | 4 |
| T15 | Multi-tenant isolation | 12 |
| T16 | Idempotency and replay | 18 |
| T17 | Simulation zero-effect | 4 |
| T18 | Uncertain outcome | 2 |
| T19 | Compliance | 54 |
| T20 | Cost control | 9 |

**By technique:**

| Technique | Name | TCs tagged |
|---|---|---|
| EP | Equivalence partitioning | 119 |
| BVA | Boundary value analysis | 72 |
| DT | Decision table | 31 |
| ST | State transition | 28 |
| PW | Pairwise | 18 |
| EG | Error guessing | 37 |
| PBT | Property-based | 2 |
| UC | Use case / journey | 9 |

**By level:**

| Level | TCs tagged |
|---|---|
| UT | 33 |
| IT | 6 |
| CT | 3 |
| SYS | 261 |
| E2E | 16 |


---

## 6.2.13 Batch 6.2 totals, register and inconsistencies (files a and b)

### 6.2.13.1 Batch totals

| Epic | Scenarios | TCs | P0 | P1 | P2 | P3 | Automated (Y) | Manual (N) | AC covered |
|---|---|---|---|---|---|---|---|---|---|
| EP-08 | 18 | 191 | 110 | 66 | 15 | 0 | 189 | 2 | 78 / 78 |
| EP-09 | 7 | 47 | 15 | 21 | 10 | 1 | 47 | 0 | 31 / 31 |
| EP-10 | 8 | 60 | 37 | 18 | 5 | 0 | 59 | 1 | 36 / 36 |
| EP-11 | 11 | 75 | 38 | 26 | 10 | 1 | 73 | 2 | 47 / 47 |
| EP-12 | 11 | 83 | 51 | 24 | 6 | 2 | 83 | 0 | 49 / 49 |
| EP-13 | 14 | 128 | 105 | 22 | 1 | 0 | 128 | 0 | 67 / 67 |
| EP-14 | 13 | 101 | 63 | 30 | 7 | 1 | 101 | 0 | 62 / 62 |
| **Total** | **82** | **685** | **419** | **207** | **54** | **5** | **680** | **5** | **370 / 370** |

| Coverage measure | Result | Method |
|---|---|---|
| Stories with ≥ 1 TC | **73 / 73 (100%)** | Story ID in TC Links |
| Acceptance criteria with ≥ 1 TC | **370 / 370 (100%)** | Every `AC-xxxx-yy` of Part 5.2 found in a TC row |
| FRs in scope (Part 2.1 epics EP-08…EP-14) with ≥ 1 TC | **49 / 49 (100%)** | §6.2.6.2 and §6.2.12.2 |
| Cross-cutting FRs cited by the stories (FR-ENG-01, FR-STD-02, FR-UIS-04, FR-ADP-01, FR-DM-01…04, FR-PUB-01, FR-CSM-01, FR-A109, FR-OP001) | **11 / 11 explicitly linked** | §6.2.6.3 and §6.2.12.3 |
| Distinct BRL rules cited by the stories with ≥ 1 TC | **104 / 104 (100%)** | Union of §6.2.6.4 and §6.2.12.4 |
| State machines exercised with a 0-switch map and sneak paths | **9** (outbound message, sequence enrolment, meeting, content/publication, campaign, proposal/quote, contract, bid, order) | Groups TC-08-I, TC-08-P, TC-09-G, TC-11-J, TC-12-K, TC-13-K, TC-14-K |
| Uncovered items | **None** | — |

**By type (both files):**

| Type | Name | TCs tagged |
|---|---|---|
| T01 | Functional | 272 |
| T03 | Performance (load) | 3 |
| T07 | Security | 117 |
| T08 | Accessibility | 27 |
| T10 | Compatibility | 2 |
| T11 | Data migration | 6 |
| T12 | DR / resilience | 4 |
| T13 | Localization | 18 |
| T14 | AI (deterministic gateway/guardrail) | 18 |
| T15 | Multi-tenant isolation | 32 |
| T16 | Idempotency and replay | 41 |
| T17 | Simulation zero-effect | 12 |
| T18 | Uncertain outcome | 27 |
| T19 | Compliance | 168 |
| T20 | Cost control | 15 |
| T21 | Operability | 5 |

**By technique (both files):**

| Technique | Name | TCs tagged |
|---|---|---|
| EP | Equivalence partitioning | 266 |
| BVA | Boundary value analysis | 144 |
| DT | Decision table | 78 |
| ST | State transition | 64 |
| PW | Pairwise | 30 |
| EG | Error guessing | 89 |
| PBT | Property-based | 4 |
| UC | Use case / journey | 31 |
| EXP | Exploratory / review | 2 |

**By level (both files):**

| Level | TCs tagged |
|---|---|
| UT | 63 |
| IT | 32 |
| CT | 9 |
| SYS | 544 |
| E2E | 44 |
| SYS-M | 3 |
| UAT | 2 |


**Priority profile.** 61% of the designs are P0 because six of the seven epics sit in P0 risk areas of §6.1.4.3 (RA-03, RA-04, RA-05, RA-06, RA-07, RA-08, RA-09, RA-10, RA-14, RA-20, RA-26) and P0 includes every denial, scope, duplicate-effect and money check. P0 designs are parameterized wherever possible (one test function, many rows), so the P0 suite remains inside the G3 nightly budget (§6.1.9.5); 99% are automation candidates (the 5 manual items are assistive-technology passes and spike document reviews).

**Effort check (estimate).** At 0.15–0.35 person-day per automated TC design for implementation and first green run (parameterized rows at the low end), the 680 automated designs need about **100–240 person-days** across developers and QA automation, inside the 287–483 pd delivery envelope only if developers own SYS tests for their modules (Part 6.1 §6.1.15.1 RACI; GAP-165 remains the capacity risk). Basis: the per-TC factor is a planning estimate, not a measured rate.

### 6.2.13.2 Techniques: where each required technique is shown

| Technique (client specification) | Representative groups with the table or matrix shown |
|---|---|
| Equivalence partitioning | TC-08-A (evidence partitions), TC-10-D (visitor question partitions), TC-14-E (intake partitions) |
| Boundary value analysis | TC-08-K (quiet hours and caps), TC-08-F (bounces, complaints), TC-13-E (discount 0/10/20% and margin floor, from §6.1.11.2), TC-14-C (tender deadline), TC-14-G (fulfilment tolerance), TC-13-J (MFA freshness) |
| Decision tables | TC-08-B (queue path), TC-08-G (inbound), TC-10-B (template usability), TC-10-C (WhatsApp send gate), TC-11-B, TC-11-F, TC-12-B, TC-12-E, TC-13-H (contract approvers), TC-14-A (routing), TC-14-B (checklist) |
| State-transition testing | TC-08-I, TC-08-P (message machine incl. PBT 1-switch), TC-09-G, TC-11-J, TC-12-K, TC-13-K, TC-14-K |
| Pairwise / combinatorial | TC-08-Q (dispatch, 12 rows of 108), TC-12-K (campaign, 6 of 48), TC-13-L (pricing and tax, 12 of 72) |
| Error guessing, property-based, use case | EG-01…EG-20 applied throughout; PBT in TC-08-136, TC-08-175, TC-13-025, TC-14-072; journeys J-08-01…J-14-02 |

### 6.2.13.3 Register of tags issued in Batch 6.2

| Tag | Statement (short) | Defined in | Used in |
|---|---|---|---|
| [RECOMMENDATION-075] | Adapter conformance battery B1–B7, one parameterized suite per adapter; channel flag stays OFF until the battery row is green | File a §6.2.1.6 | Both files (SES, Calendar, WhatsApp, social, ads, e-sign TCs) |
| [RECOMMENDATION-076] | E2E journey register J-08-01…J-14-02 with ★ candidates for the per-wave top-20 manual accessibility audit | File a §6.2.1.7 | TC-08-188, 189; TC-09-045, 046; TC-10-059, 060; TC-11-074; TC-12-082, 083; TC-13-127, 128; TC-14-099, 100 |
| [ASSUMPTION-185] | Oracle interpretations O-1…O-11 (EP-08…EP-11) | File a §6.2.1.8 | File a |
| [ASSUMPTION-186] | Oracle interpretations O-12…O-21 (EP-12…EP-14) | §6.2.8.2 | File b |
| [ASSUMPTION-187] | Story fixture pack EDGE-P52 in GSE-SYN with stable keys | File a §6.2.1.4; §6.2.8.1 | Both files |

Tags consumed from earlier parts (not issued here): ASSUMPTION-161…169, GAP-155…159, CONFLICT-133…135, RECOMMENDATION-054…056 (Part 5.2); ASSUMPTION-180…184, RECOMMENDATION-070…074, GAP-165…167 (Part 6.1).

### 6.2.13.4 Inconsistencies observed in earlier parts (reported, not edited)

Items 1–5 are listed in file a §6.2.7.3 (AC-0810-03 loosening approver; AC-0811-05 Sunday DST date; AC-0801-06 role choice; A046/W08/W09 epic mapping; TC-AI ownership after Part 7). Additional items from file b:

| # | Where | Observation | Handling in the tests | Suggested owner action |
|---|---|---|---|---|
| 6 | Part 6.1 §6.1.12.4 worked example | Names TS-13-02 as "Quote discount approval routing" with TC-13-004…017 for BVA-D01…D14, and TC-13-008 for the 20.01% case; with that range TC-13-008 would be BVA-D05, so the example is internally inconsistent | Batch 6.2 numbers scenarios by story order: discount routing is **TS-13-05** with **TC-13-036…049**; the worked example corresponds to **TC-13-044** (BVA-D09) and its companion to TC-13-046 (BVA-D11) | Part 6.1 author / Part 9: mark the §6.1.12.4 IDs as illustrative and point to TC-13-044 |
| 7 | Part 5.2 AC-1206-05 | Scenario title says enabling a paid adapter "needs R12 and R01", while the step and Part 2.3 BRL-APR-11 describe R11 requesting and R01 approving | TC-12-046 tests R11 request → R01 approval; R12's role is not asserted | Part 5.2 author: align the title |
| 8 | Part 5.2 AC-1304-01 / AC-1303-03 | GST examples apply 18% (9% + 9%) to turmeric (HSN 0910) and to SAC 998314; both are illustrative per ASSUMPTION-169 and real rates differ by item | Fixtures carry the illustrative rate from a TaxProfile fixture, so a rate change edits data, not tests | Finance advisor to confirm rates before W4 (verify, as of 27 Nov 2026) |

---

## 6.2.14 Quality gate: Batch 6.2 (files a and b)

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | **Pass** | Every TC row links its TS, story/AC and ≥ 1 FR, BRL, NFR, DEC or ABAC; P0 rows link a BRL, NFR or DEC; scenarios link stories and FRs |
| 2 | Assumptions, gaps, conflicts tagged and logged | **Pass** | Only allocated tags used (RECOMMENDATION-075…076, ASSUMPTION-185…187), all registered (§6.2.13.3); 8 inconsistencies in earlier parts reported, none edited |
| 3 | IDs unique and consistent with earlier parts | **Pass** | 82 scenarios and 685 TCs; script check: no duplicate and no gap in any epic sequence (TC-08-001…191, TC-09-001…047, TC-10-001…060, TC-11-001…075, TC-12-001…083, TC-13-001…128, TC-14-001…101); formats per §6.1.12.1; cross-file references (battery, journeys) verified after renumbering |
| 4 | No story lacks AC and no requirement lacks a test | **Pass** | 73/73 stories, 370/370 AC, 49/49 FRs, 104/104 cited BRL rules covered. *Fixes applied in self-check:* added TC-08-190, TC-08-191, TC-11-075, TC-14-101 and explicit links for FR-A063, FR-A109, FR-W09, FR-CSM-01, BRL-AI-03, BRL-MKT-01 |
| 5 | Negative, edge, security and accessibility cases covered | **Pass** | Each story has ≥ 1 denial; cross-tenant TCs in all seven epics; duplicate/replay, uncertain outcome, simulation and emergency stop per dispatching adapter (battery B1–B7); localization rows for hi-IN, ta-IN, or-IN; accessibility TCs plus 5 manual AT passes; money boundaries from EDGE-MONEY |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | **N/A** | Agents are specified in Part 7. This batch tests their deterministic guardrails (BRL-AI-02…07, -11), Tier 3 fallbacks, budget stops and tool-registry denials (R20); statistical metrics belong to TC-AI families |
| 7 | Time-sensitive facts flagged "verify" with an as-of date | **Pass** | Provider sandboxes, error codes, windows, scopes, e-sign legal validity, GST rates and tool versions marked "verify at implementation (as of 27 Nov 2026)"; effort figure labelled estimate with basis |
| 8 | No restricted data routed to free-tier models | **Pass** | TC-08-012, TC-08-076, TC-10-037 assert 0 Restricted data to Tier 2; health, minors and identifier redaction TCs (TC-10-031, TC-10-043, TC-12-064, TC-14-046) |
| 9 | Consistent with earlier parts | **Pass, with 8 reported observations** | All worked numbers recomputed with Decimal HALF_UP (270.00; 318.60; 28.30; 76,790.40; 159.30; 8,638.00 vs 8,638.92) and all dates checked for weekday and zone (15:00 IST = 09:30 UTC; 02:00 PDT = 09:00 UTC; 2027-03-28 Sunday) |

**Status: Part 6 Batch 6.2 complete. EP-08 to EP-14: 82 test scenarios and 685 test cases (419 P0, 207 P1, 54 P2, 5 P3; 680 automation candidates) covering 73/73 stories, 370/370 acceptance criteria, 49/49 FRs and 104/104 cited BRL rules, with decision tables, state-transition maps, pairwise sets and 13 E2E journeys. Continue with Batch 6.3 (EP-15 to EP-21 and AI evaluation cases).**
