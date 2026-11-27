# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 9 (Batch 9.1), Errata Register and Consolidated Decisions

| Field | Value |
|---|---|
| Document | Part 9, Batch 1 |
| Version | 1.0 · 27 Nov 2026 |
| Purpose | Resolve every inconsistency found between parts during cross-review. This register **overrides** conflicting text in earlier parts, under the same delegated authority as Part 0A (DEC-001…065) |
| Baseline | Parts 0–8 |
| Roles applied | Product Owner (lead), Solutions Architect, BSA, QA Lead, Security, FinOps |

**Precedence rule:** where an earlier part conflicts with a decision below, the decision governs. The full document (Part 10 assembly) carries this register so a reader always has the resolution next to the source. Decisions continue the Part 0A numbering (DEC-066 onwards).

---

## 9.1.1 Errata decisions

| DEC | Errata | Found in | Conflict | Decision (binding) | Affected parts |
|---|---|---|---|---|---|
| DEC-066 | E-01 | Part 5.2 | Part 0 §0.10.2 maps A046 to EP-08; Part 2.1 maps it to EP-10 | **Part 2.1 governs** for all screen-to-epic mappings. Part 0 §0.10.2 was preliminary | 0, 2.1, 5 |
| DEC-067 | E-02, E-08 | Parts 5.2, 5.3 | Part 0 places W08–W10 in EP-19 | W08/W09 → EP-11; W10 → EP-12 (Part 2.1) | 0, 2.1, 5 |
| DEC-068 | E-03 | Part 5.2 (CONFLICT-133) | The bid buffer (BRL-BID-01) blocks recording a human submission made before the real deadline | BRL-BID-01 amended: the **buffer is a warning and an internal readiness gate** (status turns red; Startup Head override with reason). The **hard block is the true deadline** (FR-DM-02). Recording evidence of a submission made before the deadline is always allowed | 2.3, 5.2, 6.2 |
| DEC-069 | E-04 | Part 5.2 (CONFLICT-134) | A fixed 15-minute slot hold (BRL-MTG-02) conflicts with WCAG 2.2.1 Timing Adjustable | BRL-MTG-02 amended: 15-minute default hold, a warning 60 s before expiry, **extendable once by 15 minutes** on request | 2.3, 2.5, 5.2 |
| DEC-070 | E-05 | Part 5.2 (ASSUMPTION-166) | The order state machine lacks reservation expiry (DEC-045) | Add transition **Approved → ReservationExpired → Draft** (stock released; owner notified) | 2.3, 3.3 |
| DEC-071 | E-06 | Part 5.2 (GAP-156) | DEC-064 sets no cap for first-touch outreach | **First-touch outreach = L1** (human approves the message) until a first-touch *template* is approved. Then **L2 dispatch** of that template with variables only. Never L3 | 0A, 2.3, 7 |
| DEC-072 | E-07 | Part 5.3 (CONFLICT-136) | BR-M09 epic placement differs between Part 0 and Part 1 | BR-M09 → **EP-21** (Part 1 governs); Sprint 0 pipeline enablers sit in EP-01 stories that trace to BR-M09 | 0, 1, 5 |
| DEC-073 | E-09 | Part 5.3 (CONFLICT-138), Part 5.1 (CONFLICT-132) | Import (FR-A103) is needed in W1 but traced only to BR-SVC (Should) | FR-A103 traces to **BR-TENANT (Must, W1) for import** and BR-SVC (Should, W5) for portability export | 1, 2.1, 5 |
| DEC-074 | E-10 | Part 5.3 | BR-M61 (Must) depends on BR-M60 (Could) | The dependency is **soft**: without M60 the Command Centre shows "Forecast not enabled" | 1, 5.3 |
| DEC-075 | E-11 | Part 5.3 | FR-W22 ships in W2 but its order and invoice data arrives in W4 | W22 cards are **progressively enabled** by capability flag: W2 enquiries, meetings, documents; W4 orders, invoices, onboarding | 2.1, 5.3 |
| DEC-076 | E-12 | Part 5.3 | No notification exists for loss of domain verification | Add **NT-046 Domain verification lost / certificate expiring in 14 days**: severity High; recipients R12, R05L; escalation to R02 after 1 business day | 2.4 |
| DEC-077 | E-14 | Part 4.1 (CONFLICT-114) | BRL-TEN-08 says WebAuthn is "recommended"; DEC-019 checks it | **Passkeys/WebAuthn required** for R01, R02, R08–R12 and all approver roles once the IdP supports them (Sprint 0 check). TOTP is the interim minimum, with a migration deadline at the end of W2 | 0A, 2.3, 4.1 |
| DEC-078 | E-15 | Part 4.1 (CONFLICT-111) | DEC-028 has no retention for security/application logs; 90-day AI logs may be too short | Amend DEC-028: **security and application logs 1 year** (meets the CERT-In 180-day minimum and DPDP log expectations; verify). **AI run metadata 1 year, AI payload bodies 90 days** (redacted) | 0A, 2.4, 3.3, 4 |
| DEC-079 | E-16, E-43 | Parts 4.1, 3.1 (CONFLICT-112/101) | A 4-hour RTO cannot cover a regional outage in the pilot | Amend DEC-018: RTO ≤ 4 h and RPO ≤ 15 min for **instance, AZ and database failures**. **Regional outage: RTO ≤ 24 h, RPO ≤ 15 min** (cross-region backups) in the pilot. Multi-region warm standby is a scale-gate option | 0A, 3.1, 4.2, 6.1 |
| DEC-080 | E-17 | Part 4.1 (CONFLICT-113) | Business-hours support (DEC-044) vs 24×7 SLOs and 30-minute Critical escalation | Monitoring and alerting are **24×7 automated**. Human out-of-hours response is limited to **S1 categories**: cross-tenant exposure, emergency stop, suppression breach, payment discrepancy > ₹1 lakh, production outage. Other Critical business notifications escalate in the next business window | 0A, 2.4, 4.3 |
| DEC-081 | E-18 | Part 4.1 (CONFLICT-110) | No budget for a WAF although public intake needs one | **AWS WAF on CloudFront from W2**. Budget line B21 CDN/WAF ≈ ₹800–1,500/month (estimate; verify) | 0A, 4, 8 |
| DEC-082 | E-19 | Part 4.1 | Object Lock mode unspecified | S3 Object Lock in **compliance mode** for audit anchors (§2.34.3) | 2.4, 4.1 |
| DEC-083 | E-20, E-48 | Parts 4, 3.1 (GAP-123) | Part 4 assumed compute/IaC/CI before Part 3 existed | **Part 3.1 ADRs govern** compute, IaC and CI. Part 4 pipeline stages apply unchanged | 3.1, 4.3 |
| DEC-084 | E-21 | Part 3.3 | Six DEC-016 entities are not mentioned in Part 2 | **Part 3.3 governs the data model**: BusinessLine, CapabilityProfile, PublicationSnapshot, PreviewGrant, BidChecklistItem and PlanVersion back FR-A003, A099/A100, A107/A108, A104 and A101 | 2.1, 3.3 |
| DEC-085 | E-22 | Part 3.3 | "Subscription" has two meanings | **CustomerSubscription** (M50 renewals) and **ServiceSubscription** (B-SVC billing). The Part 2.3 §2.27.18 Subscription states apply to ServiceSubscription | 2.1, 2.3, 3.3 |
| DEC-086 | E-23 | Part 3.3 | AI Usage vs SaaS UsageMeterReading | AI usage is recorded in **CostLedger** (M53). **UsageMeterReading** holds billable SaaS meters. A nightly job aggregates tenant AI cost into the "AI tasks" meter | 2.1, 3.3, 7 |
| DEC-087 | E-24 | Part 3.3 | Entity count of 199 vs the source's 155 | Accepted as a **DERIVED superset**. 17 FRD-retained entities cannot be identified (GAP-112); reconcile if the source catalogue is supplied | 0, 3.3 |
| DEC-088 | E-25, E-29 | Parts 3.3, 7 | Embedding dimension provisional | Embedding model = **open-source multilingual E5-large class (1024 dimensions)**, self-hosted on CPU workers (Part 7.3; licence verify). The vector column stays at 1024 | 3.3, 7 |
| DEC-089 | E-26 | Part 7 | Part 0 §0.2 says "about 3 FTE" and "pgvector optionally" | Superseded by DEC-005 (4.0 + 0.5 FTE) and the ADR adopting pgvector | 0 |
| DEC-090 | E-27 | Part 7 (CONFLICT-122) | No budget for delivery-lifecycle AI | New budget line **B23 Delivery AI reserve ≈ ₹1,000/month** (estimate), separate from runtime B02 | 0A, 7, 8 |
| DEC-091 | E-28 | Part 7 | BRL-AUT-06 cites Part 7 | Agent-level caps in Part 7.2 §7.2.9 **complement** the workflow-level caps in BRL-AUT-06; the stricter applies | 2.3, 7 |
| DEC-092 | E-30 | Part 6.1 | Part 4 cites LT-03/05/07 as "Batch 4.2" | **Part 6.1 owns LT-01…LT-12**; Part 4 references resolve to Part 6.1 | 4, 6.1 |
| DEC-093 | E-31 | Part 6.1 | Test ID formats differ (Part 1 §1.14 vs DEC-017) | Epic-based IDs govern: **TS-<EP>-##, TC-<EP>-###, TC-AI-AG###-##, TC-AU-AU###-##** | 1, 6 |
| DEC-094 | E-32 | Part 6.1 (GAP-167) | SM-UT-037/049/050 unused in the FRD | Retained as **unassigned aliases**; no test obligation | 6 |
| DEC-095 | E-33 | Part 6.1 (GAP-165) | QA capacity (0.5 FTE) vs 43–97 pd QA effort; business UAT unplanned | Resolved in Part 8 (staffing uplift and UAT plan); see Part 8 §8.x | 0A, 6.1, 8 |
| DEC-096 | E-34 | Part 5.1 (CONFLICT-130) | W0 does not fit Day 1–15 | **W0 split:** W0-A Day 1–15 (environments, identity spike, CI, RLS/outbox/PDP skeletons, catalogue core); W0-B Day 16–30 (remaining governance, AI gateway and eval harness, cost control, privacy, observability). W1 runs Day 24–45 with overlap; **100 reviewed signals by about Day 45** (was Day 30) | 0A (DEC-006/034), 1, 5, 8 |
| DEC-097 | E-35 | Part 5.1 (CONFLICT-131) | A003 and W14–W16 epic placement | A003 → EP-17; W14–W16 → EP-14 (Part 2.1) | 0, 5 |
| DEC-098 | E-36 | Part 5.1 | CA-PUB cites DEC-001 for WCAG | Correct citation is **RECOMMENDATION-001** (accepted) | 2.1 |
| DEC-099 | E-37 | Part 5.1 | The RBAC row for A004 lacks a Finance price approval | R08 gets **A(price)** on A004/A068 price versions (WF-01) | 2.3 |
| DEC-100 | E-38 | Part 5.1 (GAP-151) | Missing defaults | Contact verification expiry **180 days**. Privacy response deadline per DPDP Rules (verify); system default **30 days**, escalation at 70% | 2.3, 2.4 |
| DEC-101 | E-39 | Part 5.1 | FR-COP-01 and FR-SRCH-01 lack an epic | Both → **EP-17** | 2.1, 5.3 |
| DEC-102 | E-40 | Part 5.1 | Dimension code notation differs between batches | Mapping in Part 5.1a §5.6.6 is authoritative; both notations are valid | 5 |
| DEC-103 | E-41 | Part 5.1 | EP-21 overlaps EP-01 Sprint 0 enablers | EP-21 reduced by ≈ 5.5 pd in planning. **Programme central ≈ 416 pd** (inside 287–483) | 5, 8 |
| DEC-104 | E-42 | Part 3.2 (CONFLICT-103) | Named operation count | 102 unique FRD-named operations + 3 OP. API catalogue total **555** (DERIVED; approval actions merged into one Approval resource) | 0A (DEC-015), 3.2 |
| DEC-105 | E-44 | Part 3.1 (CONFLICT-102) | Hosting budget scope | **B01 = ₹5,000–7,000/month** estimate (prod + staging; staging scaled down out of hours). **B20 = ₹300–600/month** for cross-region backups (verify) | 0A, 3.1, 8 |
| DEC-106 | E-45 | Part 3.2 | Rate limits incomplete in Part 2.4 | **Part 3.2 rate-limit classes govern** (login, chat, portal, webhooks, heavy operations added) | 2.4, 3.2 |
| DEC-107 | E-46 | Part 3.1 | Entity names differ between Parts 2.1 and 3.3 | **Part 3.3 names govern** (e.g. Product → Offering) | 2.1, 3.3 |
| DEC-108 | E-47 | Part 3.1 | AI run volume vs the pilot cap | Gateway runs include Tier 0 cache/rules hits. The ₹3,000 cap applies to pilot volume only. Year 1 volume falls under the ₹12,000 growth ceiling (Part 7.3 estimate ≈ ₹4,600 at 4× pilot) | 3.3, 7 |

## 9.1.2 Effect on earlier decisions

| Earlier decision | Status after Part 9.1 |
|---|---|
| DEC-006 / DEC-034 (waves) | Amended by DEC-096 (W0-A/W0-B) |
| DEC-015 (API catalogue) | Clarified by DEC-104 |
| DEC-018 (SLOs, RTO/RPO) | Amended by DEC-079 |
| DEC-019 (identity) | Strengthened by DEC-077 |
| DEC-020 (budget lines) | Amended by DEC-081 (B21), DEC-090 (B23), DEC-105 (B01, B20) |
| DEC-028 (retention) | Amended by DEC-078 |
| DEC-044 (support) | Clarified by DEC-080 |
| DEC-064 (autonomy caps) | Extended by DEC-071 |
| BRL-BID-01, BRL-MTG-02, BRL-TEN-08 | Amended by DEC-068, DEC-069, DEC-077 |

## 9.1.3 Quality gate: Batch 9.1

| Check | Result | Notes |
|---|---|---|
| Every inconsistency reported by contributors resolved | Pass | 48 logged items → DEC-066…108 (some items merged) |
| Decisions traceable to the finding and affected parts | Pass | Columns "Found in" and "Affected parts" |
| Time-sensitive items flagged | Pass | CERT-In/DPDP log rules, WAF and backup costs, model licence marked verify |
| Consistency | Pass | Precedence rule stated; Part 10 assembly includes this register |

**Status: Part 9 Batch 9.1 complete.**
