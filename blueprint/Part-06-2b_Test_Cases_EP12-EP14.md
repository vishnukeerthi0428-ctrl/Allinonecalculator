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
| Proposals and quotes | D-210 (MedMaarg deal, Sunrise Clinics, demo Completed), template MM-PILOT v2, offering "Scanner corporate pilot", PV-7 (valid until 2026-11-30 23:59:59 IST), P-55; OrganicSpec price list PL-OS-12 with SKU TUR-A "Turmeric finger, Grade A" INR 150.00/kg, units {kg}, min 1 max 5,000 kg, direct cost INR 100.00/kg; Q-88 rev 2 | Q-88 rev 2 = 2 kg × 150.00 × 0.90 = 270.00 + CGST 24.30 + SGST 24.30 = **318.60 INR**, valid until 2026-12-27 23:59:59 IST |
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
