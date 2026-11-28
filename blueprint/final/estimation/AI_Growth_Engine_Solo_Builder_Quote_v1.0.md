# AI Growth Engine: Solo-Builder Quotation
## Fixed-price quotation for building the application single-handedly with AI models and AI agents (INR)

| Field | Value |
|---|---|
| Quotation | AI Growth Engine – Employee Sales & Marketing Automation platform |
| Prepared for | [Client name] |
| Prepared by | [Your name / company] |
| Date | 28 Nov 2026 |
| Validity | 30 days from the date above |
| Basis | Application Blueprint v1.1 (Parts 0–9.10, 344 decisions) and Cost Estimates v1.0 and v1.1 |
| Currency | Indian Rupees (INR). GST at 18% is added to every fee |

# 1. Summary of the quotation

| Item | Fee (excl. GST) | GST 18% | Fee (incl. GST) | Duration |
|---|---|---|---|---|
| **Core platform: Releases 1 and 2, 100% aligned with the 38-document specification** | **₹49,00,000** | ₹8,82,000 | **₹57,82,000** | ≈ 27 months |
| Optional: Advanced release A1 (advanced AI agents, revenue-growth and platform capabilities) | ₹31,00,000 | ₹5,58,000 | ₹36,58,000 | ≈ 18 further months |
| Maintenance and support retainer after go-live | ₹55,000 per month | ₹9,900 per month | ₹64,900 per month | Monthly, from go-live |
| Pass-through costs (at actuals, see §5) | Security testing ₹4–10 lakh; running costs ≈ ₹15,000–30,475 per month | As invoiced | As invoiced | — |

**Headline: core platform for ₹49,00,000 + GST, fixed price, delivered by one builder using AI agents in about 27 months.**

# 2. What the client receives (scope)

The core platform as specified in the Application Blueprint v1.1:

- Public Website/Portal (34 screens) and the confidential Admin Command Centre (113 screens), as separate React/TypeScript applications.
- Multi-tenant backend (Django REST Framework, PostgreSQL with row-level security and pgvector, Celery/Valkey, S3) on AWS ap-south-1.
- Owner Portfolio tenant with the four launch startups (AppNAI, MedMaarg, EduVerse, OrganicSpec) and onboarding of external SaaS tenants.
- Workflows WF-01 to WF-14: catalogue, discovery, outreach under consent, inbound handling, qualification, meetings, bids, proposals and quotes, orders, verified close, onboarding, plans and offboarding.
- The release-1 and release-2 AI agents and automations, using Claude Sonnet as the primary model through the model gateway, with hard cost caps and human approval for consequential actions.
- Literal alignment with all 38 source documents (99.98% literal match; the two remaining items are the approved Claude-primary decision).
- Tests and evidence: automated unit, integration and UI tests, AI evaluation sets, UAT support, and release evidence packs.
- Deployment, monitoring, backups, disaster-recovery drill, runbooks, training task cards and handover documentation.

The advanced capabilities in Parts 9.7–9.9 (42 further AI agents, revenue-growth and platform features) are **not** in the core fee. Release A1 is quoted as an option (§6).

# 3. How the price is built

| Component | Basis | Core platform | Advanced A1 (option) |
|---|---|---|---|
| Builder's time | 557 days (core) and 372 days (A1) at ₹5,682 per day (senior rate, ₹1.25 lakh per month) | ₹31.66 L | ₹21.11 L |
| AI and build tools | Claude Max 20x, GitHub, Figma, BrowserStack, CI sandboxes, domains: ≈ $300 per month × duration | ₹7.16 L | ₹4.78 L |
| Claude API tokens for coding agents | ≈ $6.78 per agent-executed day; 48% of the work executed by agents | ₹2.43 L | ₹1.62 L |
| Contingency | 15% of time and tokens | ₹5.11 L | ₹3.41 L |
| **Cost basis** |  | **₹46.37 L** | **₹30.92 L** |
| **Quoted fee** | Rounded, small margin | **₹49.00 L** | **₹31.00 L** |

**Effort basis.** A traditional team would need about 829 person-days for the core platform and 553 for A1. Building with AI agents saves about 29% (central case of Cost Estimate v1.1). A single builder saves about 4% more, because there is no team to coordinate. That leaves about 557 and 372 days of the builder's own work: specifying, reviewing every AI-generated change, testing and releasing.

# 4. Payment milestones (core platform)

| Milestone | Share | Amount (excl. GST) | Amount (incl. GST) |
|---|---|---|---|
| On signing (mobilisation) | 15% | ₹7,35,000 | ₹8,67,300 |
| Foundation gate passed (environments, identity, tenancy, gateway) | 20% | ₹9,80,000 | ₹11,56,400 |
| Release 1 go/no-go passed | 25% | ₹12,25,000 | ₹14,45,500 |
| Release 2 build gate passed | 25% | ₹12,25,000 | ₹14,45,500 |
| 30-day monitored pilot completed | 15% | ₹7,35,000 | ₹8,67,300 |
| **Total** | **100%** | **₹49,00,000** | **₹57,82,000** |

Invoices are payable within 15 days. Each milestone is accepted against the evidence defined in the blueprint's release gates.

# 5. Pass-through costs (billed at actuals, not included in the fee)

| Item | Estimate | Why it is separate |
|---|---|---|
| Two external penetration tests and scope uplift | ₹4,00,000 – ₹10,00,000 | Independent security testing; a solo builder must not certify their own security |
| Cloud, AI inference and providers during the build | ≈ ₹15,000 – ₹30,000 per month (ramps up) | Client-owned accounts (AWS, Anthropic, Meta WhatsApp, Amazon SES) |
| Running cost after go-live (pilot) | ₹24,035 – ₹30,475 per month | Client-owned; hard caps on AI spend |
| External legal counsel (data protection, contracts) | As quoted by counsel | Legal advice is outside the builder's scope |
| Paid data, advertising media, payment-gateway fees | As used | Business costs, not platform build costs |

# 6. Option: Advanced release A1

**₹31,00,000 + GST** (₹36,58,000 incl. GST), about 18 further months after the core platform. Scope as defined for A1 in Parts 9.7–9.10. Highlights:

- the supervisor/planner over existing agents;
- the RFP response co-pilot and account research;
- predictive scoring with explanations;
- pipeline inspection and forecasting;
- multichannel cadences under consent and CPQ guardrails;
- AI observability, passkeys, just-in-time admin access, secrets rotation, the DPDP rights workflow and the trust centre.

Releases A2 and A3 can be quoted separately later.

# 7. Maintenance and support retainer

**₹55,000 + GST per month** from go-live, renewable yearly. It covers:

- bug fixes, security patches and dependency upgrades;
- model-version migrations with re-evaluation;
- monitoring and incident response in business hours;
- up to 6 days of small changes per month.

Larger changes are quoted separately.

# 8. Timeline

| Phase | Indicative duration (solo) | With a team (for reference) |
|---|---|---|
| Foundation (environments, identity, tenancy, gateway) | ≈ 3 months | 1 month |
| Release 1 build and go/no-go | ≈ 15 months from start | ≈ 6 months (4 Jun 2027) |
| Release 2 build and pilot | ≈ 27 months from start, plus the 30-day pilot | ≈ 7.5 months (23 Jul 2027) |
| Advanced A1 (option) | ≈ 18 further months | ≈ 5 months |

**Important:** a single builder cannot meet the team plan's June 2027 date. If an earlier date is essential, the scope can be phased further, or contract engineers added under a revised quotation.

# 9. Comparison with other ways of building it

| Approach | Core + alignment (excl. GST) | Duration |
|---|---|---|
| Traditional team | ≈ ₹74.5 lakh | ≈ 7 months |
| AI-assisted team (approved approach, DEC-420) | ≈ ₹55.4 lakh | ≈ 7 months |
| **This quotation: solo builder with AI** | **₹49.00 L + security tests at actuals** | **≈ 27 months** |

# 10. Assumptions

1. Scope is the Application Blueprint v1.1 as of 28 Nov 2026; changes go through written change requests priced at the day rate above.
2. The builder's time is valued at ₹1.25 lakh per month (₹5,682 per day), with 21 productive days per month.
3. AI productivity: 29% net saving (central case) plus 4% for solo working. These are planning assumptions. Plausible outcomes range from about 7% to 44%, and the builder will report measured progress monthly.
4. Claude Sonnet is the primary production model (DEC-418). Tool and token prices are list prices as of the date and may change.
5. The client provides timely approvals, test users for UAT, provider accounts (AWS, Anthropic, Meta, payment gateway) and legal confirmations.
6. Agents work on synthetic data only; no production personal data is shared with build agents.
7. GST at 18% is added to all fees. Pass-through costs are invoiced at actuals with receipts.

# 11. Terms

- **Price type:** fixed price for the defined scope; change requests are priced separately.
- **Intellectual property:** transferred to the client on full payment, including source code, infrastructure code, documentation and test assets.
- **Warranty:** 60 days after the pilot completes for defects against the agreed acceptance criteria.
- **Confidentiality:** all client data and documents are treated as confidential.
- **Validity:** 30 days.

**Acceptance**

| For the client | For the builder |
|---|---|
| Name: ______________________ | Name: ______________________ |
| Signature: __________________ | Signature: __________________ |
| Date: ______________________ | Date: ______________________ |

