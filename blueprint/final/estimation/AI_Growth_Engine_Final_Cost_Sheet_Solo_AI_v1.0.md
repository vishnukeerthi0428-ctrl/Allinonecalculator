# AI Growth Engine: Final Cost Sheet
## Optimized, discounted all-inclusive package · Core platform + Advanced A1 · built by a solo builder with AI

| Field | Value |
|---|---|
| Prepared for | [Client name] |
| Prepared by | [Your name / company] |
| Version and date | Final cost sheet v1.0 · 28 Nov 2026 · approved for issue |
| Validity | 30 days |
| Basis | Application Blueprint v1.1 (346 decisions, incl. DEC-418 Claude Sonnet primary, DEC-421 Vercel + Supabase hosting, DEC-422 running budget); Final Solo-Builder Quotation v2.0 |
| Currency | INR; GST 18% shown separately |

# 1. Package price

|  | Amount |
|---|---|
| **All-inclusive package (excluding GST)** | **₹90,00,000** |
| GST 18% | ₹16,20,000 |
| **All-inclusive package (including GST)** | **₹1,06,20,000** |
| Period covered | Build (≈ 44 months) + first 12 months of operation after full go-live |
| Saving against the unoptimized package (≈ ₹1,12,98,000) | ₹22,98,000 (20%) |

# 2. Cost sheet

| # | Item | Basis | Rate per month | Months | Amount (excl. GST) | GST 18% | Amount (incl. GST) |
|---|----------------------------------------|---------|--------|-----|----------|--------|----------|
| A | **Fixed development fee**: Core platform (Releases 1 and 2, aligned with the 38-document specification) + Advanced release A1 | Fixed | — | — | **₹65,33,132** | ₹11,75,964 | ₹77,09,095 |
| B | **Maintenance and support retainer**, first 12 months (includes the maintainer's Claude seat) | Fixed monthly | ₹55,000 | 12 | **₹6,60,000** | ₹1,18,800 | ₹7,78,800 |
| C1 | Independent penetration tests: 2 engagements (before Release 1; combined before Release 2 + A1), CERT-In-empanelled vendor (Range ₹4,00,000 – ₹9,00,000) | At actuals | — | — | ₹6,50,000 | ₹1,17,000 | ₹7,67,000 |
| C2 | Client hosting while building (staging only): Vercel Pro, Supabase Pro, small AWS Mumbai server, domains (≈ $65 per month) | Months 1–15 | ₹5,850 | 15.0 | ₹87,750 | ₹15,795 | ₹1,03,545 |
| C3 | Pilot running from Release 1 go-live to A1 go-live (Vercel, Supabase, AWS, Claude API with hard caps, email, WhatsApp, search, extraction, DR storage, 15% contingency) (₹19,665 – ₹27,427 per month) | Months 15–44 | ₹23,546 | 29.2 | ₹6,87,551 | ₹1,23,759 | ₹8,11,310 |
| C4 | Running cost, first 12 months after full go-live (C3 lines + A1 feature additions) (Growth-gate step-ups only if the gate passes) | 12 months | ₹31,797 | 12.0 | ₹3,81,568 | ₹68,682 | ₹4,50,250 |
|  | **Total** |  |  |  | **₹90,00,000** | **₹16,20,000** | **₹1,06,20,000** |

A and B are fixed prices. C1–C4 are client-owned costs paid at actuals: the figures are the estimates inside the package. The client owns the Vercel, Supabase, AWS, Anthropic and Meta accounts from day one.

# 3. How the development fee is arrived at

| Component | Basis | Amount |
|---|---|---|
| Builder's effort with AI | 929 days (traditional 1,382 days × (1 − 32.8% AI-built saving)) | — |
| Builder's time | 929 days × ₹5,682 per day (₹710 per hour; ₹1.25 lakh per month) | ₹52,78,409 |
| Builder's tools | Claude Max 20x $200 + GitHub $4 for 44 months; Figma $16 for 12 months; BrowserStack $29 for 6 months; at ₹90/$ | ₹8,44,452 |
| Claude API tokens for coding agents | ≈ 663 agent-executed days × $6.78, less 20% with prompt caching and the Haiku model | ₹3,24,000 |
| Contingency | 10% of time and tokens | ₹5,60,241 |
| **Optimized fee** | Cost basis rounded up | **₹70,10,000** |
| Package discount | Applied to reach the ₹90,00,000 package | − ₹4,76,868 |
| **Fixed development fee (A)** |  | **₹65,33,132** |

**Effect of the discount.** It uses about 85% of the contingency. The remaining contingency is ₹83,373. Scope is therefore frozen at the blueprint and changed only by written change request at the day rate.

# 4. How the package was optimized

| Lever | Saving |
|---|---|
| Builder tools trimmed (BrowserStack 6 months, Figma 12 months, client's own Workspace) | ₹2,06,000 |
| Claude tokens cut ≈ 20% (prompt caching, Haiku for simple tasks) | ₹81,000 |
| Contingency 15% → 10% (fully specified scope, change control) | ₹2,84,000 |
| Penetration tests 3 → 2 (combined Release 2 + A1 test) | ₹3,25,000 |
| Staging-only hosting until Release 1 | ₹3,06,000 |
| Pilot running without team seats, delivery AI line and integration reserve; free monitoring tiers | ₹2,10,000 |
| Year 1: point-in-time recovery deferred to the growth gate; maintainer seat inside the retainer | ₹2,70,000 |
| Retainer ₹65,000 → ₹55,000 per month | ₹1,20,000 |
| Package discount on the development fee | ₹4,76,868 |
| **Total reduction from ≈ ₹1,12,98,000** | **₹22,98,000** |

# 5. What is included

| Item | Detail |
|---|---|
| Applications | Public Website/Portal (34 screens) and Admin Command Centre (113 screens), plus the A1 screens; React/TypeScript on Vercel |
| Platform | Multi-tenant Django REST backend, PostgreSQL on Supabase (RLS, pgvector), Celery/Valkey on AWS Mumbai, policy engine, outbox, audit |
| AI agents, automations, workflows | 170 in scope: 50 AI agents, 85 automations, 35 workflows. 88 fully automated, 7 mostly automated, 63 partially automated (human approval), 12 assistive. AI never signs, pays, submits bids or sets prices |
| AI model | Claude, through a gateway with hard monthly caps: Haiku-class for simple tasks, Sonnet-class as the primary model |
| Quality | Automated tests, AI evaluation sets, UAT support, release evidence packs, two independent penetration tests |
| Handover | Source code, infrastructure code, documentation, runbooks, training task cards; IP to the client on full payment |
| Support | 12-month retainer: fixes, patches, upgrades, Claude model migrations, monitoring, quarterly DR drill, up to 6 days of small changes per month |

Full lists of agents, automations, workflows, technology and skills: Final Solo-Builder Quotation v2.0.

# 6. Subscriptions

| Subscription | While building | While using the application | Paid by |
|---|---|---|---|
| Claude Max 20x (Claude Code) | $200 per month | Maintainer seat inside the retainer | Builder (in fee / retainer) |
| Claude API (coding agents) | ≈ $82 per month average, capped | — | Builder (in fee) |
| Claude API (application's AI agents) | Within C3 once live | Hard caps ₹3,000 core + ₹2,000 advanced per month | Client (C3/C4) |
| Vercel Pro | $20 per month | $20–40 per month | Client |
| Supabase Pro (Mumbai) | $25 per month (staging) | $40–60 per month (production compute) | Client |
| AWS ap-south-1 (API, workers, Valkey, S3, SES, DR) | ≈ $15 per month (staging) | ≈ ₹3,000–4,650 per month | Client |
| WhatsApp (Meta), search API, extraction | From Release 1 | ≈ ₹4,500 per month | Client |
| GitHub | $4 per month | Inside the retainer | Builder |
| Figma, BrowserStack | 12 months / 6 months only | — | Builder (in fee) |
| Domains (≈ 5) | ≈ $5–8 per month | ≈ $5–8 per month | Client |
| Monitoring (Sentry, uptime) | Free tiers | Free tiers | — |

# 7. Payment schedule

| Milestone (fee A) | Indicative month | Share | Amount (excl. GST) | Amount (incl. GST) |
|---|---|---|---|---|
| Contract signing | Month 0 | 10% | ₹6,53,313 | ₹7,70,910 |
| Foundation gate | Month 3 | 10% | ₹6,53,313 | ₹7,70,910 |
| Release 1 functional complete | Month 12 | 15% | ₹9,79,970 | ₹11,56,364 |
| Release 1 go/no-go | Month 15 | 15% | ₹9,79,970 | ₹11,56,364 |
| Release 2 build gate | Month 26 | 15% | ₹9,79,970 | ₹11,56,364 |
| 30-day pilot completed | Month 28 | 10% | ₹6,53,313 | ₹7,70,910 |
| Advanced A1 mid-point demo | Month 35 | 10% | ₹6,53,313 | ₹7,70,910 |
| Advanced A1 go-live and acceptance | Month 44 | 15% | ₹9,79,970 | ₹11,56,364 |
| **Total fee A** |  | **100%** | **₹65,33,132** | **₹77,09,095** |

The retainer (B) is billed monthly from go-live at ₹55,000 + GST. Items C1–C4 are paid by the client to the providers as incurred.

# 8. After the first year

The ongoing cost is about **₹31,797 per month for running plus ₹55,000 per month for maintenance** (plus GST). Running costs rise only if the business passes the growth gate (≈ ₹59,000–79,000 per month, DEC-422). External SaaS tenants pay for their own usage.

# 9. Assumptions and terms

1. Scope is the Application Blueprint v1.1 (Core + Advanced A1) as of 28 Nov 2026; changes by written change request at the day rate.
2. One builder with AI agents; about 44 months to A1 go-live. AI productivity follows Cost Estimate v1.1 (central case) plus 4% for solo working; progress is reported monthly.
3. Items C1–C4 are estimates at list prices as of 28 Nov 2026 and are paid at actuals; changes in provider prices pass through.
4. The client provides timely approvals, UAT users, provider accounts and legal confirmations. External legal counsel, paid data and advertising are not included.
5. Build agents use synthetic data only; no production personal data is shared with them.
6. Fixed price for A and B; IP transfers to the client on full payment; 60-day warranty after each go-live; invoices payable within 15 days of milestone acceptance.

**Acceptance**

| For the client | For the builder |
|---|---|
| Name: ______________________ | Name: ______________________ |
| Signature: __________________ | Signature: __________________ |
| Date: ______________________ | Date: ______________________ |

