# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 8 (Batch 8.4), Cost Model: Development Cost Separated from Subscription and Running Costs

| Field | Value |
|---|---|
| Document | Part 8, Batch 4 |
| Version | 1.0 · 27 Nov 2026 |
| Purpose | Present the programme budget as **two separate ledgers**, at the Founder's request: (A) **development cost**, the one-time cost to design, build, test and launch, and (B) **subscription and running cost**, the recurring monthly cost of cloud, AI usage, providers and software subscriptions |
| Baseline | Part 8.1 (team and rates), Part 8.2 §8.2.7 (budget lines B01–B23), Part 9.5 §9.5.2.6 (re-plan budget), DEC-228 (Option 2b approved) |
| Roles applied | FinOps Lead (lead), Product Owner, Delivery Lead, Solutions Architect |
| Authority | DEC-229 (below) makes this ledger split the authoritative presentation of the budget. **Both ledgers approved by the Founder on 27 Nov 2026: Ledger A by DEC-230, Ledger B by DEC-231 (Part 9.5 §9.5.2.9).** Figures are **estimates**; every provider price is "verify at time of implementation (as of 27 Nov 2026)" |

**Rates and conventions used throughout**

| Parameter | Value | Source |
|---|---|---|
| Loaded rate per person-month | ₹1.0–1.5 lakh | BRD §6 |
| Working days per month | 22 → ₹4,545–6,818 per person-day | BRD §6 |
| Calendar month for staffing | 30.4 days | Part 9.5 |
| FX | ₹90 / USD (verify) | BRD §6 |
| Contingency on running costs | 15% (line B11) | BRD §6; DEC-004 |
| Plan of record | Option 2b: Release 1 go/no-go Day 180 (4 Jun 2027); Release 2 build gate Day 208 (2 Jul 2027) | DEC-228 |
| Excluded everywhere | Taxes (GST), Founder time, external legal counsel (not estimated, GAP-174), paid ad media (B12), customer-funded SaaS tenant usage | Part 8.2 |

---

## 8.4.1 The two ledgers at a glance

| Ledger | What it contains | Nature | Estimate |
|---|---|---|---|
| **A. Development cost** | Core engineering team, QA, DevOps, UX, growth/compliance lead, two contract engineers (Option 2b), independent reviewer, training content, external penetration tests, load-test windows | **One-time** (project), to the Release 2 build gate (Day 208) | **₹52.7–84.1 lakh** |
| A2. Phase-2 development (W6, Day 209–365), optional | Should/Could scope deferred to W6 (~100 pd) and selective expansion | One-time, separately approved | **₹25.8–38.7 lakh** (if the core team stays to Day 365) |
| **B. Subscription and running cost** | Cloud hosting, backups, CDN/WAF, AI model usage, data and communication providers, software subscriptions and developer seats | **Recurring**, monthly | **₹19,895–26,335 per month** (base, with contingency); **₹24,035–30,475** including developer seats; ₹34,385–40,825 with the optional Apollo enrichment as well |
| B (cumulative to Day 208) | Ramp-up of B during development | Recurring, paid during the build | **₹1.5–1.9 lakh** |
| B (first 12 months after launch) | Steady pilot run cost | Recurring | **₹2.4–3.2 lakh per year** (₹2.9–3.7 L including seats) |

**Key message:** at pilot scale about **97% of the money to reach Release 2 is development** (people). The recurring subscription and running cost is small: roughly ₹20–26 thousand a month, about ₹2.4–3.2 lakh a year. It grows only when the business passes the scale gates (§8.4.4.6).

---

## 8.4.2 Ledger A: development cost (one-time)

### 8.4.2.1 Development cost to the Release 2 build gate (Day 1–208, Option 2b)

| # | Item | Formula | Low | High | Source |
|---|---|---|---|---|---|
| A1 | Core engineering team, Day 1–180 | 4.0 FTE × 6 months × ₹1.0–1.5 L | ₹24.00 L | ₹36.00 L | Part 8.2 §8.2.7.1; DEC-005 |
| A2 | Core team extension, Day 181–208 | 5.0 FTE (4 engineers + QA uplift + growth/compliance) × 0.92 month × ₹1.0–1.5 L | ₹4.60 L | ₹6.90 L | Part 9.5 §9.5.2.6(b), staff portion only (run cost moved to Ledger B) |
| A3 | Recommended uplifts | QA to 1.0 FTE from Sprint 3 (₹2.75–4.13 L) + DevOps front-load (₹0.60–0.90 L) + UX contractor (₹0.87–1.31 L) + independent reviewer (₹0.55–0.82 L) | ₹4.77 L | ₹7.16 L | Part 8.1 §8.1.6.5 |
| A4 | Growth/compliance lead, Day 1–180 | 0.5 FTE × 6 × ₹1.0–1.5 L | ₹3.00 L | ₹4.50 L | Part 8.2 §8.2.7.6 |
| A5 | **Two contract engineers (Option 2b)** | 2 × 5.46 months (Day 43 → Day 208) × ₹1.0–1.5 L | ₹10.92 L | ₹16.38 L | Part 9.5; **DEC-228** |
| A6 | Source-pack one-offs | QA extension (₹0.46–0.69 L) + UX extension (₹0.22–0.33 L) + pen-test scope uplift (₹1.00–2.00 L) + training content, 147 task cards (₹0.66–1.91 L) + load-test staging windows (₹0.05–0.21 L) | ₹2.39 L | ₹5.14 L | Part 9.5 §9.5.2.6(a) |
| A7 | External penetration tests (two engagements: before Release 1 and before Release 2) | 2 × ₹1.5–4.0 L (quotes to verify) | ₹3.00 L | ₹8.00 L | Part 8.2 §8.2.7.4; DEC-126 |
| | **Ledger A total to Release 2 gate** | A1 + … + A7 | **₹52.68 L** | **₹84.08 L** | |
| R | Management reserve (not in the total; released only through the change-control board) | 10% of central effort value + field-standardization residual | ₹3.94 L | ₹8.29 L | Part 8.2 (₹1.89–2.84 L) + Part 9.5 DEC-225 (₹2.05–5.45 L) |

**Reconciliation with Part 9.5.** Part 9.5 reported **₹53.6–85.1 lakh** "cash to the Release 2 gate", which mixed people and running costs. Splitting that same total gives **Ledger A ₹52.7–84.1 L** plus **Ledger B to Day 208 ₹1.5–1.9 L** (§8.4.3.4), i.e. ₹54.2–86.0 L. The ≈ ₹0.6–0.9 L difference comes from Part 9.5's rounded "common one-offs" line. The itemized figures in this part govern (DEC-229).

### 8.4.2.2 Development cost by phase (Option 2b)

| Phase | Days | Main cost drivers | Low | High |
|---|---|---|---|---|
| Sprint 0 and foundation (W0-A, W0-B) | 1–30 | Core team, DevOps front-load, identity spike | ₹5.4 L | ₹8.2 L |
| Release 1 build (W1–W3 plus Must enhancements) | 31–180 | Core team, contract engineers from Day 43, QA uplift, UX, training content, pen test 1 | ₹37.3 L | ₹59.0 L |
| Release 2 build to gate (W4–W5) | 181–208 | Core team extension, contract engineers, pen test 2 | ₹10.0 L | ₹16.9 L |
| **Total** | 1–208 | | **₹52.7 L** | **₹84.1 L** |

*(Phase split is pro-rata by calendar and by when each item is incurred; totals match §8.4.2.1.)*

### 8.4.2.3 Development effort value (how much work, independent of who is paid)

This view shows the **value of the effort** at the BRD rate. It is used to compare against the BRD envelope, not as the cash figure (cash is §8.4.2.1).

| Basis | Low | Central | High | Formula |
|---|---|---|---|---|
| Effort (person-days) | 532 | 722 | 921 | Part 9.5 (original 314/416/518 + net source-pack 218/306/403) |
| Effort value | ₹24.18 L | ₹32.81–49.23 L | ₹62.79 L | pd × ₹4,545 (low) … pd × ₹6,818 (high) |
| BRD §6 envelope | ₹13.05 L (287 pd) | — | ₹32.93 L (483 pd) | BRD §6 |

The cash in §8.4.2.1 is higher than the low effort value because people are paid for calendar time, which includes meetings, reviews, onboarding, hypercare and focus-factor losses, not only story points (Part 5.1a §5.5).

### 8.4.2.4 Phase-2 development (W6, Day 209–365), separately approved

| Item | Formula | Low | High |
|---|---|---|---|
| Core team continues (4 engineers + QA 0.5 + growth/compliance 0.5) | 5.0 FTE × 5.16 months × ₹1.0–1.5 L | ₹25.8 L | ₹38.7 L |
| Scope | ~100 pd Should/Could deferred items (Part 9.5 §9.5.2.3), expansion pilots M63–M66, regional-language UI, paid adapters | | |
| Decision point | Release 2 go/no-go review; fund only items with measured value (BRD §8 scale gate) | | |

### 8.4.2.5 Development costs explicitly excluded

| Item | Why excluded | Where tracked |
|---|---|---|
| External legal counsel (DPDP, children's consent, jurisdictions, e-sign, GST) | Not estimated in the baseline; obtain quotes | GAP-174; Part 8 legal backlog |
| Founder / Product Owner time | Internal | — |
| Taxes (GST) on services | Outside scope of estimates | — |
| Hypercare after Day 208 | Part of Phase 2 / operations | §8.4.2.4 |

---

## 8.4.3 Ledger B: subscription and running cost (recurring)

### 8.4.3.1 Monthly cost by category (pilot scale)

| Category | Line | Item | Billing model | ₹/month (estimate; verify) | Active from |
|---|---|---|---|---|---|
| **1. Cloud infrastructure** | B01 | AWS hosting: production + scheduled staging (ECS on EC2, RDS PostgreSQL, Valkey, S3) | Usage / 1-year commitment | 5,000–7,000 | Day 1 |
| | B20 | Cross-region backup and DR storage | Usage | 300–600 | Day 1 |
| | B21 | CloudFront CDN + AWS WAF | Fixed per rule + usage | 1,300–1,800 | Day 68 (public intake) |
| | B01/B20 | Source-pack additions: restore-check sandbox, control/finance worker slot, drift job, training tenant | Usage | 200–1,700 | From Release 1 |
| | | **Subtotal: cloud** | | **6,800–11,100** | |
| **2. AI model usage** | B02 | Production AI inference (Claude Haiku/Sonnet via the gateway) | Pay-as-you-go, **hard cap** | 3,000 cap (expected ≈ 1,150) | Day 15 |
| | B23 | Delivery-team AI (CI review, eval judge, fixture generation) | Pay-as-you-go, capped | ≈ 1,000 | Day 15 |
| | | **Subtotal: AI** | | **4,000** (expected ≈ 2,150) | |
| **3. Data and communication providers** | B03 | Public search API (500 fetches/month) | Free credits, then usage | 1,500 | Day 36 |
| | B04 | Extraction compute / overage (self-hosted first) | Usage | 1,000 | Day 36 |
| | B05 | Email delivery (Amazon SES, ~2,000 sends) | Usage | 500 | Day 56 |
| | B06 | WhatsApp Business (Meta Cloud API, ~1,000 chargeable templates) | Per conversation/template | 2,000 | Day 113 |
| | B10 | Optional integration reserve (calendar/social/validation pilots) | Per approval | 1,000 | Day 82 |
| | | **Subtotal: providers** | | **6,000** | |
| **4. Software subscriptions and tools** | B07 | Monitoring, security and CI (Sentry developer tier, CI minutes, paging) | Subscription / usage | 500 | Day 1 |
| | B07 | Source-pack additions: synthetic availability probes, extra CI gates | Subscription / usage | 0–1,300 | From Release 1 |
| | | **Subtotal: tools** | | **500–1,800** | |
| | | **Base subtotal (categories 1–4)** | | **17,300–22,900** | |
| | B11 | Contingency 15% | | 2,595–3,435 | |
| | | **Base monthly running cost** | | **₹19,895–26,335** | |
| **5. Developer seats (development-period subscription)** | B09 | Claude Code seats (2 × $20, verify plan) × 1.15 | Fixed subscription | 4,140 | Day 1 |
| | | **Base + developer seats** | | **₹24,035–30,475** | |
| **6. Optional / conditional** | B08 | Apollo paid enrichment reserve (OFF until the scale gate) × 1.15 | Subscription / credits | 10,350 | Scale gate only |
| | B22 | LLM observability (self-hosted Langfuse) at growth | Hosting | 2,250–2,700 | Growth gate |
| | B13 | E-signature provider | Per envelope | Per use (pilot uses the signed-PDF path: ₹0) | W5/W6 |
| | B14 | Payment gateway fees | % of amount collected (pass-through) | Per transaction | Day 140+ |
| | B12 | Paid ads media | Per approved campaign | Not a platform cost (per startup budget) | W6 |
| | B15–B19 | Calendar, social APIs, SEO data, contact verification, vector overage | Free tiers / off | 0 in pilot | — |
| | | **Base + seats + Apollo** | | **₹34,385–40,825** | |

**Expected (not ceiling) monthly spend.** With AI at its expected ₹1,150 instead of the ₹3,000 cap: **₹17,768–24,208** base, or ₹21,908–28,348 with seats.

### 8.4.3.2 Fixed subscriptions vs usage-based costs

| Type | Lines | Monthly ₹ (ceiling) | Behaviour |
|---|---|---|---|
| **Fixed subscriptions** (pay regardless of use) | B09 seats, B21 WAF rules, B07 Sentry/paging plan, domain names (annual) | ≈ 6,000–7,500 | Change only by plan decision |
| **Infrastructure** (mostly fixed at pilot) | B01, B20 | 5,300–7,600 + additions | Steps up at scale gates (§8.4.4.6) |
| **Usage-based, hard-capped** | B02 AI, B23 delivery AI | 4,000 cap | Cannot exceed cap (M53 hard stop) |
| **Usage-based, volume-driven** | B03, B04, B05, B06, B10, B14 | ≈ 6,000 + payment fees | Scales with business volume; alerts at 70/90/100% (DEC-175) |

### 8.4.3.3 Annual view (after launch, pilot scale)

| View | Monthly | 12 months |
|---|---|---|
| Base running cost (ceiling) | ₹19,895–26,335 | **₹2.39–3.16 lakh** |
| Base + developer seats | ₹24,035–30,475 | **₹2.88–3.66 lakh** |
| Expected spend (AI at expected level), with seats | ₹21,908–28,348 | ₹2.63–3.40 lakh |
| With optional Apollo (only after scale gate) | ₹34,385–40,825 | ₹4.13–4.90 lakh |
| Plus annual items | Domain names per startup site (verify registrar prices) | Per domain per year |

### 8.4.3.4 Running cost incurred during development (Day 1–208)

| Month | Lines active | Ceiling before contingency (₹) | With 15% + seats (₹) |
|---|---|---|---|
| Dec 2026 | B01, B02 cap, B07, B20, B23 | 9,800–12,100 | 15,410–18,055 |
| Jan 2027 | + B03, B04 | 12,300–14,600 | 18,285–20,930 |
| Feb 2027 | + B05, B21 | 14,100–16,900 | 20,355–23,575 |
| Mar 2027 | + B10 | 15,100–17,900 | 21,505–24,725 |
| Apr 2027 | + B06 | 17,100–19,900 | 23,805–27,025 |
| May 2027 | All lines + source-pack additions | 17,300–22,900 | 24,035–30,475 |
| Jun 2027 (to Day 208) | All lines | 17,300–22,900 | 24,035–30,475 |
| **Total Day 1–208** | | | **≈ ₹1.47–1.75 lakh** (≈ ₹1.5–1.9 L allowing for usage variance) |

### 8.4.3.5 Who pays for SaaS client usage

| Cost | Paid by | Mechanism |
|---|---|---|
| AI usage, messages, storage of **external SaaS tenants** | The tenant, through its plan and metered overage | DEC-008, DEC-047, AU-042 metering; never charged to B02 |
| Payment gateway fees on customer receipts | Pass-through on collected amounts | B14 |
| Paid ad media | Each startup's approved campaign budget | B12; not a platform subscription |

---

## 8.4.4 Combined view and scale

### 8.4.4.1 Total cost of ownership: first 12 months of operation after Release 2

| Component | Ledger | Low | High |
|---|---|---|---|
| Development to Release 2 gate | A | ₹52.7 L | ₹84.1 L |
| Running cost during development (Day 1–208) | B | ₹1.5 L | ₹1.9 L |
| Running cost, 12 months after launch (with seats) | B | ₹2.9 L | ₹3.7 L |
| **TCO excluding Phase 2 development** | | **₹57.1 L** | **₹89.7 L** |
| Phase 2 development (W6), if approved | A2 | ₹25.8 L | ₹38.7 L |
| **TCO including Phase 2** | | **₹82.9 L** | **₹128.4 L** |

### 8.4.4.2 Share of cost (to the Release 2 gate, central values)

| Component | Central ₹ | Share | Formula |
|---|---|---|---|
| People (A1–A5: core team, extension, uplifts, growth/compliance, contract engineers) | ≈ ₹59.1 L | ≈ 84% | midpoints 30.0 + 5.75 + 5.97 + 3.75 + 13.65 |
| External services (A6–A7: pen tests, training content, load-test windows, extensions) | ≈ ₹9.3 L | ≈ 13% | midpoints 3.77 + 5.50 |
| Subscriptions and running costs during development (Ledger B, Day 1–208) | ≈ ₹1.7 L | ≈ 2–3% | §8.4.3.4 |
| **Total** | **≈ ₹70.1 L** | 100% | |

### 8.4.4.3 Running cost at scale gates (recurring; only after the gates pass)

| Stage | Hosting (B01 equivalent) | AI ceiling (B02) | Typical monthly total (estimate) | Gate |
|---|---|---|---|---|
| Pilot (now) | ₹5,000–7,000 | ₹3,000 | ₹20–26 thousand | — |
| Year-1 design point (growth gate) | ≈ ₹21,000 | ₹12,000 | ≈ ₹50–70 thousand (+ Apollo/Langfuse if enabled) | BRD §8 scale gate: measured cost per qualified opportunity, consent compliance, conversion |
| Year-2 design point (scale) | ≈ ₹66,600 | ₹40,000 | ≈ ₹1.3–1.7 lakh | Revenue and tenant plans carry attributable cost (NFR-035) |

### 8.4.4.4 How to read and govern the two ledgers

| Rule | Detail |
|---|---|
| Separate approval | Ledger A is approved once (with change control via the CCB). Ledger B is approved as a monthly budget per line, with hard caps (AI) and alerts at 70/90/100% (DEC-175) |
| Separate reporting | Monthly FinOps report shows Ledger A burn vs plan (people, contractors, one-offs) and Ledger B actual vs ceiling per line (B01–B23) |
| Capitalization (for the finance advisor) | Ledger A development may be eligible for capitalization as an intangible asset under applicable accounting standards. Ledger B is an operating expense. Confirm the treatment with the finance advisor (verify) |
| No cross-subsidy | Unused Ledger B budget never funds development, and the management reserve never funds subscriptions, without a CCB decision |

---

## 8.4.5 Decision

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-229 | **Budget is presented and governed as two ledgers:** (A) development cost, one-time, to the Release 2 gate, with Phase-2 development separately approved; (B) subscription and running cost, recurring, per line B01–B23 with contingency. This part's itemized figures govern; the Part 9.5 "cash to Release 2 gate" figure is superseded by Ledger A + Ledger B (to Day 208) | Founder request (27 Nov 2026), "subscription costs separated from the development cost" | Ledger A **₹52.7–84.1 L** to Day 208; Ledger B **₹19,895–26,335/month** base (₹24,035–30,475 with seats); TCO to 12 months after launch **₹57.1–89.7 L** excluding Phase 2 |

## 8.4.6 Quality gate: Batch 8.4

| Check | Result | Notes |
|---|---|---|
| Traced to source | Pass | Every line cites Part 8.1/8.2/9.5, BRD §6 or a DEC |
| Arithmetic reconciles | Pass | Ledger B base 17,300–22,900 × 1.15 = 19,895–26,335 (matches Part 9.5); Ledger A items sum to ₹52.68–84.08 L |
| Time-sensitive facts | Pass | All provider prices, AWS rates, FX and pen-test quotes marked estimate / verify (as of 27 Nov 2026) |
| Consistency | Pass | Supersedes Part 9.5's combined figure through DEC-229; line IDs unchanged |

**Status: Part 8 Batch 8.4 complete.**
