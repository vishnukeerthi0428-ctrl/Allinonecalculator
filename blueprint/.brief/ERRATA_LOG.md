# Errata and cross-part inconsistencies (to resolve in Part 9)

## From Part 5.2
1. Part 0 §0.10.2 maps A046 to EP-08; Part 2.1 maps it to EP-10. Part 5.2 follows Part 2.1 (CONFLICT-135). Proposed resolution: Part 2.1 governs; correct Part 0's epic map.
2. Part 0's epic map omits W08/W09 from EP-11. Proposed resolution: add them.
3. BRL-BID-01 buffer vs DEC-053/FR-DM-02 (CONFLICT-133). Proposed resolution: the buffer is a soft warning, with a hard block at the true deadline; recording evidence of a submission made before the deadline is always allowed.
4. BRL-MTG-02 fixed 15-minute hold vs WCAG 2.2.1 (CONFLICT-134). Proposed resolution: a 15-minute default hold, extendable once by 15 minutes on user request, with a warning 60 s before expiry.
5. The order state machine lacks a reservation-expiry transition (ASSUMPTION-166). Proposed resolution: add Approved → ReservationExpired → Draft.
6. DEC-064 sets no cap for first-touch outreach (GAP-156). Proposed resolution: first-touch is L1 until the template is approved, then up to L2.

## From Part 5.3
7. CONFLICT-136: Part 0 puts BR-M09 in EP-01; Part 1 puts it in EP-21. Resolution: Part 1 governs (EP-21).
8. CONFLICT-137: Part 0 has W08–W10 under EP-19; Part 2.1 has W08/W09 under EP-11 and W10 under EP-12. Resolution: Part 2.1 governs.
9. CONFLICT-138: FR-A103 import is in W1 but traced to BR-SVC (Should). Resolution: trace the import capability to BR-TENANT (Must, W1) as well; the portability export stays with BR-SVC (W5).
10. BR-M61 (Must) depends on BR-M60 (Could). Resolution: M61 needs only M60's forecast *display slot*; without M60 the Command Centre shows "Forecast not enabled". The dependency is soft.
11. FR-W22 is a W2 screen whose order and invoice data arrives in W4. Resolution: in W2 it shows only enquiries, meetings and documents; its cards are enabled progressively.
12. Part 2.4 has no notification for losing custom-domain verification. Resolution: add NT-046 "Domain verification lost / certificate expiring" (High; R12, R05L).
13. Parts 5.2 and 5.3 cite "Part 5.1 §5.x" placeholders; resolve them after 5.1 lands.

## From Part 4
14. CONFLICT-114: BRL-TEN-08 says WebAuthn is "recommended"; DEC-019 checks it for privileged roles. Resolution: WebAuthn/passkey is required for R01, R08–R12 and approvers once the IdP supports it (Sprint 0 check); TOTP is the interim minimum.
15. CONFLICT-111: log retention. Resolution: security/application logs kept 1 year (DPDP Rules, CERT-In 180-day minimum; verify). AI run logs: redacted metadata 1 year, payload bodies 90 days. Amend DEC-028.
16. CONFLICT-112: the RTO of 4 h covers AZ/instance/DB failures only. A regional outage has RTO ≤ 24 h / RPO ≤ 15 min (cross-region backups) in the pilot; multi-region active-passive is a scale-gate option. Amend DEC-018.
17. CONFLICT-113: support hours vs 24×7 SLOs. Resolution: automated monitoring is 24×7. Human on-call is best-effort outside 10:00–18:00 IST for S1 platform incidents; Critical business escalations (§2.30.2) page out of hours only for S1 categories (cross-tenant exposure, emergency stop, suppression breach, payment discrepancy > ₹1 lakh).
18. CONFLICT-110: WAF is needed. Resolution: AWS WAF managed rules on CloudFront from W2 (public intake live); cost moves from B21 (estimate; verify) and B07 is revised.
19. Object Lock mode: compliance mode (per Part 4).
20. Part 4 assumptions on compute/IaC/CI must be reconciled with Part 3 ADRs (GAP-123).

## From Part 3.3
21. Six DEC-016 entities are not referenced in Part 2 (BusinessLine, CapabilityProfile, PublicationSnapshot, PreviewGrant, BidChecklistItem, PlanVersion). Resolution: Part 3.3 governs the data model; these entities back FR-A003 scope, A099/A100, A107/A108, A104 and A101.
22. "Subscription" is overloaded. Resolution: CustomerSubscription (M50, customer renewals) vs ServiceSubscription (B-SVC SaaS billing); the Part 2.3 §2.27.18 states apply to ServiceSubscription.
23. AI "Usage" vs SaaS "UsageMeterReading". Resolution: AI Usage → CostLedger entries (M53); UsageMeterReading = billable SaaS meters (B-SVC); a mapping job aggregates AI cost into tenant meters.
24. Entity count is 199 vs the source's 155 (17 FRD-retained names unidentifiable, GAP-112). Accepted as a DERIVED superset.
25. Embedding dimension of 1024 is provisional until Part 7 selects the embedding model (GAP-111).

## From Part 7
26. Part 0 §0.2 says "about 3 FTE" and "pgvector optionally"; both are superseded by DEC-005 (4.0 + 0.5 FTE) and ADRs (pgvector adopted).
27. CONFLICT-122: no budget line for delivery-lifecycle AI (CI review/eval agents). Resolution: add **B23 Delivery AI reserve ≈ ₹1,000/month** (estimate; RECOMMENDATION-061), separate from runtime B02.
28. BRL-AUT-06 cites Part 7: agent-level caps are defined in Part 7 §7.2.9 and complement the workflow caps.
29. The embedding model choice in Part 7 resolves GAP-111 of Part 3.3 (vector dimension to match).

## From Part 6.1
30. Part 4.1 cites LT-03/05/07 as "Batch 4.2"; they are defined in Part 6.1. Resolution: Part 6.1 owns LT-01…LT-12.
31. Part 1 §1.14 lists TS-###/TC-###. Resolution: the epic-based format (TS-<EP>-##, TC-<EP>-###, TC-AI-…) per Part 6.1 governs.
32. SM-UT-037/049/050 are unused in the FRD (GAP-167); retained as unassigned aliases.
33. GAP-165: QA capacity of 0.5 FTE vs 43–97 pd QA effort, and business UAT time (60–120 participant-days) unplanned. To be resolved in Part 8 (staffing and UAT plan).

## From Part 5.1
34. CONFLICT-130: the W0 scope (113.5 SP) does not fit Day 1–15. Resolution: adopt RECOMMENDATION-050, splitting W0 into **W0-A (Day 1–15: environments, identity spike, CI, RLS/outbox/PDP skeletons, catalogue core)** and **W0-B (Day 16–30: remaining governance controls, AI gateway and eval harness, cost control, privacy, observability)**. W1 shifts to Day 24–45 with overlap; the "100 reviewed signals" target moves to about Day 45. Part 8 plans accordingly.
35. CONFLICT-131: Part 0 epic map for A003 and W14–W16 is superseded by Part 2.1 (A003 → EP-17, W14–W16 → EP-14).
36. CA-PUB cites DEC-001 for WCAG; the correct citation is RECOMMENDATION-001.
37. The A004 RBAC row should give R08 (Finance) "A(price)" to match WF-01.
38. GAP-151: defaults. Contact verification expiry is 180 days. The privacy request response deadline is set per the DPDP Rules (verify; system default 30 days, escalation at 70%).
39. FR-COP-01 and FR-SRCH-01 → EP-17 (covered in Part 5.3).
40. Dimension code notation differs between 5.1 (value codes) and 5.2/5.3 (D1–D8); the mapping note is in Part 5.1a §5.6.6.
41. EP-21 overlaps EP-01 Sprint 0 enablers by about 5–6 pd. Programme central ≈ 421.5 − 5.5 ≈ 416 pd (inside 287–483).

## From Part 3.1/3.2
42. CONFLICT-103: DEC-015 says 105 named operations; actually 102 unique (3 duplicate spellings) + 3 OP = 105 FR operations. API catalogue total = 555 operations (DERIVED superset of the BRD's 302+19; approval actions merged into one Approval resource).
43. CONFLICT-101 (same as item 16): RTO is scoped by failure type (AZ/instance ≤ 4 h; region ≤ 24 h in pilot).
44. CONFLICT-102 / GAP-101/102: **B01 revised to ₹5,000–7,000/month estimate** (prod + staging, with 1-yr commitments at the low end; verify). Staging may be scaled to zero outside working hours to stay near ₹5,000. **B20 backup/DR ≈ ₹300–600/month** for cross-region backup copies (verify).
45. Part 2.4 §2.35.3 rate limits extended by Part 3.2 rate-limit classes (login, chat, portal, webhooks, heavy ops); Part 3.2 governs.
46. Entity names: Part 3.3 names govern over Part 2.1 names (e.g. Product → Offering, CustomerSubscription/ServiceSubscription).
47. AI run volume: the Part 3.3 projection of ≈ 45,000 AI runs/month (Year 1) counts all gateway runs including Tier 0 cache/rules; paid calls are a fraction. Part 7 Year 1 scale estimate (≈ ₹4,600 at 4× pilot) applies under the ₹12,000 growth ceiling; the ₹3,000 cap applies only to the pilot volume.
48. Part 4 compute/IaC/CI assumptions (GAP-123) reconcile to Part 3.1 ADRs; Part 3.1 governs.

## From Part 6.4 (to append to Part 9.1 as DEC-109+)
49. Injection threshold: Part 7 "≥98% clean" vs Part 4.1 "0 violations". Resolution: RECOMMENDATION-079 two-tier gate. V1–V6 (data leak, unauthorized action, restricted data to Tier 2, etc.) are zero tolerance; V7 counts toward the ≥98% pass rule.
50. AG-026/AG-032 are marked Tier 2 eligible, but the §7.3.3 chain lists no Tier 2 provider for them. Resolution: Tier 2 is **not enabled** for these agents until a provider is listed and evaluated; fallback goes to Tier 3.
51. US-1707 says "Tier 1b for answers", but Part 7 routes about 70% of Copilot turns to Haiku. Resolution: Part 7 routing governs (Tier 1a for retrieval answers with citations, Tier 1b for synthesis/drafting).
52. US-1004 confidence gate of 0.75 vs Part 7 default of 0.7. Resolution: the per-agent threshold table in Part 6.4/7 governs; the chat FAQ gate is 0.75 (stricter, customer-facing).
53. TC-AI format: Part 6.4 TC-AI-AG###-### and TC-AU-AU###-### govern (supersedes the Part 6.1 example).
54. AU-006 gate tooling: the pytest harness is the CI gate; promptfoo/DeepEval are optional dataset runners invoked by it.
55. GAP-169: there is no approved crisis/self-harm response for the public assistant. Resolution: add a fixed, Legal-approved safe-response template with helpline references (verify India helplines) and immediate human handover. Never generated.
56. GAP-168: no bilingual labelling resource. Resolution: budget part-time bilingual reviewers per locale in W5 (Part 8).
