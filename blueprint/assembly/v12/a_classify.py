#!/usr/bin/env python3
"""R1 / Group A: classify BRD V12 aspects against the blueprint and write
final/coverage_v12/A_coverage.csv.

Usage: python3 -I a_classify.py <aspects.json> <out.csv>
Rules are evaluated in order; the first match wins. Each rule records the
status before, the blueprint location, the action and new IDs, and the
status after (Matched / Pending Founder decision / Not applicable (reason)).
Rule content is the analyst judgement documented in Part 11.1 §11.1.3.
"""
import csv, json, re, sys
from collections import Counter

A = json.load(open(sys.argv[1]))
OUT = sys.argv[2]

M, PF = "Matched", "Pending Founder decision"
def NA(r): return f"Not applicable ({r})"
C, P, N, X = "Covered", "Partially covered", "Not covered", "Conflict"

# (chapter regex, key regex, text regex, before, location, action, new_ids, after)
R = []
def r(ch, key, txt, before, loc, action, new, after=M):
    R.append((re.compile(ch) if ch else None, re.compile(key) if key else None,
              re.compile(txt, re.I) if txt else None, before, loc, action, new, after))

# ---------- Conflicts pending the Founder (checked first) ----------
r(None, r"^(KPI-32)$", None, X, "Part 4.4a OKPI-32; CONFLICT-462 (RC-1)", "Adopt 2 h growth RTO as target; binding needs Topology B cost approval", "DEC-515; CONFLICT-765; FR-V12-A-147", PF)
r(None, r"^DEC-V9-01$", None, X, "DEC-018 RPO 15 min/RTO 4 h; CONFLICT-462", "Record customer approval DEC-V11-01; cost confirmation to Founder", "DEC-515; CONFLICT-765", PF)
r("21", None, r"Growth workload \(critical\)", X, "CONFLICT-462; NFR-057", "Growth RTO 2 h held as target pending cost", "DEC-515; CONFLICT-765", PF)
r(None, r"^(L[0-4])$", None, X, "DEC-064 autonomy cap; Part 9.2 glossary L0-L3", "Map V12 L0-L4 to L0-L3; consequential stays human-approved per action", "DEC-508; CONFLICT-762; FR-V12-A-110..112", PF)
r("18", None, r"^R3 financial/legal", X, "DEC-064; DEC-053", "V12-L2 equals blueprint L1 (exact human approval); mandates limited to routine class", "DEC-508; CONFLICT-762", PF)
r(None, r"^FL-09$", None, X, "DEC-064; Part 2.3 BRL-APR", "Mandate record adopted for routine class only", "DEC-508; CONFLICT-762; FR-V12-A-112", PF)
r("16", None, r"No autonomous commitment", X, "DEC-064; X-06", "Commitments stay human-approved; mandate only for routine non-binding actions", "DEC-508; CONFLICT-762", PF)
r(None, r"^BR-C09$", None, X, "DEC-064; BRL-APR-01", "Exact approval adopted; bounded mandate restricted to DEC-064 routine class", "DEC-508; CONFLICT-762", PF)
r(None, r"^(BR-V7-CJ-07|DEC-V7-03|DEC-V7-08|DEC-V12-06|DEC-V12-05|CJ-EU-10)$", None, X, "DEC-421 (Mumbai only); Part 2.4 §2.35.5", "India region through Release 2; EU/US region and tax provider at an approved R3/R5 gate", "DEC-514; CONFLICT-761", PF)
r(None, r"^(DEC-V12-01|DEC-V12-02|ENT-OPS-04)$", None, X, "DEC-228 staffing; DEC-422 budget; Part 9.9a CAP-X3-17", "Separately costed enterprise-readiness proposal", "DEC-513; CONFLICT-760; RECOMMENDATION-775", PF)
r(None, r"^(R1|R2|R4|R5)$", r"Phase|Scope|beta|availability|UK|Americas", X, "Part 8.1 waves; DEC-411 A1-A3; DEC-230/422", "Map phase to waves/A-releases; beyond-budget items costed separately", "DEC-512; CONFLICT-760; ASSUMPTION-770", PF)
r(None, r"^R3$", r"EU launch", X, "DEC-421; DEC-411", "EU launch needs EU region and budget", "DEC-512; DEC-514; CONFLICT-761", PF)
r(None, r"^R0$", r"Foundations", P, "Part 8.1 W0-W2; DEC-034", "R0 mapped to W0-W2", "DEC-512; ASSUMPTION-770; FR-V12-A-190")
r("01|24", None, r"^(Area|.*Specified).*(Identity: SSO|Custom roles|API platform|Data export, residency|Integrations / connectors|Security programme|Reliability: SLOs|Global readiness)", P, "Part 9.9a CAP-X3-12..27; Part 4.1", "Business requirement adopted (FR-V12-A-180..189); production delivery beyond approved budget", "FR-V12-A-180..189; CONFLICT-760", PF)
r(None, r"^ENT-OPS-01$", None, P, "Part 8.3c SLA-02; DEC-018; DEC-044", "Standard/Business tiers adopted as contract templates; 99.95% tier needs Multi-AZ and 24x7", "DEC-510; FR-V12-A-140; CONFLICT-760", PF)
r(None, r"^DEC-V12-03$", None, P, "Part 8.3c SLA-10; DEC-044", "SLA tiers and credits as templates; Enterprise tier pending", "DEC-510; CONFLICT-760", PF)
r(None, r"^BR-V12-(0[1-9]|10)$", None, P, "Part 9.9a CAP-X3; Part 4.1; Part 8.3c", "Adopted as business requirement with release mapping; funding beyond approved budget", "FR-V12-A-180..189; DEC-513; CONFLICT-760", PF)

# ---------- Conflicts adopted (customer V12 governs) ----------
r(None, r"^(BR-C02|MT-07|MT-01|MT-05)$", None, X, "DEC-065 one Owner Portfolio tenant; DEC-055; Part 2.4 §2.35.1", "Each owned company becomes its own tenant; portfolio = revocable grant", "DEC-504; CONFLICT-763; ADR-180; FR-V12-A-070..074")
r("06", None, r"Contract and portfolio separation|Tenant is the contractual customer", X, "DEC-065; Part 2.4 §2.35", "Adopt tenant/company/portfolio-grant model", "DEC-504; CONFLICT-763; ADR-180")
r(None, r"^(BR-C01|REC-01/05)$", None, X, "FR-W02 directory; FR-W03 startup site; API-497; US-1905", "Neutral storefront; platform directory retired; startup sites only on tenant-verified property (SM-SVC-15)", "DEC-505; CONFLICT-764; FR-V12-A-050..052")
r("12", None, r"^34 route baseline", X, "Part 2.1 FR-W01..W34; Part 2.5 §2.x", "Adopt neutral storefront routes; route remap by Group G", "DEC-505; CONFLICT-764; RECOMMENDATION-773")
r("12", r"^W(0[1-9]|[12][0-9]|3[0-4])$", None, X, "Part 2.5 screen inventory (same ID, different purpose)", "V12 route purpose adopted; ID namespacing V12-Wnn by Group G", "DEC-505; CONFLICT-764; RECOMMENDATION-773")
r(None, r"^(BR-V7-CJ-01|DEC-V7-01|DEC-V12-07|CJ-UK-01|CJ-US-01)$", None, X, "DEC-029 Year-1 outbound allowlist", "Market opens only after counsel approves its pack; IN first, EU second", "DEC-507; CONFLICT-766; RECOMMENDATION-774")
r("20", r"^CJ-(US|UK|CA|AU|SG|AE|BR)-\d+$", None, P, "DEC-029 (US/UK/AE/SG/AU summary)", "Draft pack recorded, disabled until counsel approval", "DEC-507; CONFLICT-766; FR-V12-A-131")
r("20", None, r"^Each market opens only", X, "DEC-029", "Adopted", "DEC-507; CONFLICT-766")
r(None, r"^(DEC-V12-04|AT-13)$", None, X, "DEC-026 locales", "en+hi at Release 2 Website chrome; de/fr/ar with market packs", "DEC-516; CONFLICT-777")
r(None, r"^(BR-C04|BR-V3-01)$", None, X, "DEC-047 plan archetypes", "39 SKUs independently purchasable; archetypes become bundles", "DEC-501; CONFLICT-767; FR-V12-A-001..006")
r("01", None, r"Commercial unit rule", X, "DEC-047", "39 SKUs sold; 156 workflows included", "DEC-501; CONFLICT-767")
r("05", r"^Partner / reseller", None, P, "DEC-046; X-09", "Future option recorded; white-label never weakens isolation", "FR-V12-A-020")
r(None, r"^BR-V12-05$", None, X, "X-09 (CRM integration deferred)", "Connectors adopted at A-release", "CONFLICT-776; FR-V12-A-184", PF)

# ---------- Subscription, bundle, entitlement (ch10) ----------
r("10", None, r"^Independent purchase and scoped use", N, "BRL-SVC-03; US-2001", "SKU entitlement scoped by company/offering/market", "FR-V12-A-010..012")
r(None, r"^MT-06$", None, C, "BRL-SVC-06; CSO-11/12; WF-14", "States pending/active/suspended/offboarding/retired aligned", "FR-V12-A-013")
r(None, r"^MT-16$", None, N, "BRL-SVC-03", "Entitlement-scoped configuration", "FR-V12-A-011")
r(None, r"^MT-30$", None, P, "DEC-008; M53 budgets per startup", "Company/offering/workflow budgets + tenant cap", "FR-V12-A-014")
r(None, r"^RT-07$", None, P, "BRL-SVC-03; A101", "Forecast and threshold alerts", "FR-V12-A-015")
r(None, r"^RT-11$", None, N, "None (no proration)", "Plan change preview, effective date, proration", "FR-V12-A-016")
r(None, r"^CV-12$", None, P, "DEC-023 hash-bound e-sign (subscriber quotes)", "SaaS quote/agreement bound to signer and digest", "FR-V12-A-017")
r(None, r"^CV-13$", None, C, "DEC-022 payment adapter; webhook verification", "Idempotent provisioning confirmed", "FR-V12-A-018")
r("10", r"^(Trial)$", None, C, "BRL-SVC-05", "Retained", "FR-V12-A-019")
r("10", r"^(Quote)$", None, P, "US-2005", "Quote binds application revision", "FR-V12-A-017")
r("10", r"^(Active)$", None, C, "CSO-03..07", "Retained", "—")
r("10", r"^(Upgrade/downgrade)$", None, N, "None", "Proration rules", "FR-V12-A-016")
r("10", r"^(Failed payment|Suspension and renewal)$", None, P, "BRL-SVC-06; CSO-12", "Grace/retry/notice policy", "FR-V12-A-021")
r("10", r"^(Cancel / renew|Refund/cancellation)$", None, P, "CSO-09..11; BRL-SVC-07", "Cancellation, final settlement, credit note", "FR-V12-A-022")
r("10", r"^(Overage)$", None, C, "BRL-SVC-03", "Hard stop default retained; atomic reservation", "FR-V12-A-014")
r("10", r"^(Refund)$", None, P, "BRL-SVC-07", "Credit note linked to refund", "FR-V12-A-022")
r("10", r"^(New SKU)$", None, N, "None", "Expansion only by signed version", "FR-V12-A-012")
r("10", r"^(BYO provider)$", None, P, "CSO-05 credential model", "Retained; responsibility quoted", "FR-V12-A-023")
r("10", r"^(Pricing)$", None, P, "Part 8.3c §8.3.5.13.2", "Price composition adopted", "FR-V12-A-030")
r("10", None, r"^Keep pricing, usage", C, "BRL-FIN-08", "Retained", "—")

# ---------- Pricing, billing, unit economics (ch11) ----------
r("11", r"^(Replace|Retain OSS|Conditional external service|Defer / exclude)$", None, C, "Part 7.4a plugin register; X-10", "Vocabulary aligned", "—")
r("11", None, r"^Decision: (Replace|Self-host|Defer|Retain)", C, "Part 7.4a/b paid-plugin register", "Counts reconciled in Part 7.4", "—")
r("11", None, r"^Paid tools are replaced", C, "Part 7.4a; DEC open-source first", "Retained", "—")
r(None, r"^MOB-13$", None, C, "OKPI-29..31; NFR web vitals", "Retained", "—")
r(None, r"^MOB-15$", None, C, "DEC-027; MT-21", "Retained", "—")
r("11", None, r"^Commercial and subscriber financial separation", C, "BRL-FIN-08; DEC-027", "Retained", "—")
r(None, r"^(MT-14|MT-21)$", None, C, "DEC-027; offering version (Part 2.1)", "Retained", "—")
r("11", None, r"^Commercial economics", P, "Part 8.3c §8.3.5.13.7", "TCO and contribution formula adopted", "FR-V12-A-031")
r(None, r"^AI-(0[1-5]|0[89]|1[0-2]|1[45])$", None, C, "Part 7.3 routing/cache/eval; DEC-418 tier order", "Cheapest eligible = DEC-418 tier order; detail Group F", "—")
r(None, r"^AI-(0[67]|13)$", None, P, "Part 7.3 token budgets", "Context budget and summarisation rule adopted; detail Group F", "FR-V12-A-113")
r(None, r"^GC-(0[3-9]|11|14)$", None, C, "Part 3.1; Part 4.2; Part 8.4; DEC-421", "Retained", "—")
r(None, r"^GC-10$", None, P, "CSO-05", "BYO charges separated", "FR-V12-A-023")
r(None, r"^GC-1[35]$", None, P, "Part 8.3b help; Part 9.9a CAP-X3-21", "Self-service ops checklist and idle detection", "FR-V12-A-165")
r(None, r"^CV-05$", None, C, "DEC-047 price on request", "Itemised quote or pending", "FR-V12-A-030")
r(None, r"^CS-14$", None, N, "None", "Billing dispute workflow", "FR-V12-A-034")
r("11", None, r"^For every SKU, model actual", N, "Part 8.4 ledger (not per SKU)", "Per-SKU cost model", "FR-V12-A-032; GAP-769")
r("11", r"^(Cost formula|Accepted result cost|Price floor|Meter policy)$", None, N, "None", "Formula adopted", "FR-V12-A-032..033")
r("11", r"^(Approval)$", None, C, "DEC-047", "Retained", "—")
r("11", r"^SM-SVC-\d+$", None, N, "None (no SKU meters)", "SKU meter and pilot cap registry", "FR-V12-A-035; GAP-769")

# ---------- Website and acquisition (ch12) ----------
r(None, r"^BR-V7-WEB-0[12]$", None, C, "Part 2.5 UI states; WCAG 2.2 AA", "Retained", "TC-V12-A-090")
r(None, r"^BR-V7-WEB-0[34]$", None, P, "W30 privacy; BRL-PRV-01", "Data-rights and AI-transparency public pages", "FR-V12-A-053..054")
r(None, r"^BR-V7-ADM-0[1-3]$", None, C, "BRL-APR-01; DEC-050; Part 2.5", "Retained", "—")
r(None, r"^MOB-0[23]$", None, C, "DEC-043; Part 2.5 responsive", "Retained", "—")
r("12", None, r"^Public storefront V5", P, "W06/W11/W31", "Storefront tools adopted", "FR-V12-A-055..061")
r(None, r"^AT-0[29]$", None, C, "W07; W08", "Retained", "—")
r(None, r"^AT-10$", None, C, "DEC-046; W20", "Retained", "—")
r(None, r"^AT-14$", None, C, "Cookie consent; Part 2.4 §2.31", "Retained", "—")
r(None, r"^AT-(01|03|04|05|06|07|08|11|12)$", None, P, "Sitemap; W31; W08; CAP-X3-12", "Storefront capability adopted", "FR-V12-A-055..061")
r(None, r"^CV-(03|04|06|07|08|15)$", None, P, "W11; W31; KPI-26", "Selection, TCO/ROI and conversion intelligence", "FR-V12-A-056..060")
r(None, r"^CV-(09|10|11|14)$", None, C, "W18; DEC-024; sequences; experiments", "Retained", "—")
r("12", None, r"^W05 displays the four workflow", P, "None", "Workflow output previews for 156 workflows", "FR-V12-A-058")
r("12", None, r"^V4 chapter guidance", NA("navigation note"), "—", "—", "—", NA("navigation note"))

# ---------- Multi-tenant architecture, configuration (ch04, 06, 07) ----------
r(None, r"^MOB-01$", None, C, "DEC-043", "Retained", "—")
r("06", None, r"^Logical hierarchy", P, "Tenant/Startup/BusinessLine/Offering (DEC-016)", "Organization, division, brand, market, channel account added", "DEC-506; FR-V12-A-075..080")
r(None, r"^MT-(09|10|17|18)$", None, N, "Part 3.3 (division partial)", "Hierarchy and country model", "FR-V12-A-075..078")
r(None, r"^MT-(11|15)$", None, P, "Offering version; DEC-060 readiness gate", "Lifecycle states adopted", "FR-V12-A-079")
r(None, r"^MT-33$", None, C, "Part 3.3 master data", "Retained", "—")
r(None, r"^GC-(01|02|12)$", None, C, "Part 3.1 modular monolith; design system", "Retained", "—")
r(None, r"^MT-04$", None, N, "None (startup legal entity assumed)", "14 customer types", "FR-V12-A-080")
r("04", None, r"^Customer profiles", N, "None", "14 customer types", "FR-V12-A-080")
r("04", r"^(Platform catalogue manager|Operator support|Tenant owner|Tenant employee|Finance/legal approver|External customer / contact|Provider)$", None, C, "Part 1 personas; Part 2.3 roles R01-R20", "Retained", "—")
r("04", r"^(Portfolio owner)$", None, P, "DEC-055", "Explicit grant", "FR-V12-A-072")
r("04", None, r"^ICP:", C, "Part 2.4 CFG; W33", "Retained", "—")
r("04", r"^P-0[1-6]$", None, C, "Part 1 P01-P16; Part 8.3b TRN", "Journeys mapped", "ASSUMPTION-771")
r("04", r"^(AppNAI|MedMaarg|EduVerse|OrganicSpec|New independent)", None, C, "DEC-052 capability routing", "Retained", "ASSUMPTION-771")
r(None, r"^REC-07$", None, C, "Part 8.3b journeys; BRL-TEN-11 templates", "Retained", "—")
r(None, r"^REC-04$", None, C, "A112; Part 2.4 §2.33.3", "Retained", "—")
r(None, r"^MOB-(04|11)$", None, P, "W32/W33; BRL-SVC-02", "Eight-stage wizard", "FR-V12-A-090..092")
r(None, r"^MOB-16$", None, N, "None", "Cross-device signed handoff", "FR-V12-A-095")
r("07", None, r"^Private onboarding and organization manager", P, "W32/W33; A099/A100/A112", "Organization management centre", "FR-V12-A-090..093")
r("07", None, r"^Portfolio scalability", C, "DEC-031; AP-01", "Retained", "—")
r(None, r"^MT-03$", None, C, "BRL-TEN-11; AP-01", "Retained", "—")
r(None, r"^MT-08$", None, P, "W33 wizard", "Eight stages", "FR-V12-A-090")
r(None, r"^MT-19$", None, C, "IANA time zones (Part 3.3)", "Retained", "—")
r(None, r"^MT-29$", None, P, "BRL-TEN-11 templates", "Template references canonical workflow", "FR-V12-A-094")
r(None, r"^(SEC-05)$", None, P, "US-2004 import; BRL-SVC-01", "Signed identity + canonical digest", "FR-V12-A-096")
r(None, r"^FL-12$", None, C, "BRL-TEN-11", "Retained", "FR-V12-A-094")
r(None, r"^CV-01$", None, P, "W33", "Minimal-first onboarding", "FR-V12-A-091")
r(None, r"^CV-02$", None, C, "BRL-SVC-02", "Retained", "—")
r("07", r"^(Discovery|Selection|Private intake|Review and export|Operator review|Commercial lifecycle)$", None, P, "W01-W06, W32-W34, A099-A101", "Journey stages adopted", "FR-V12-A-090..097")
r("07", r"^(Renewal / changes)$", None, N, "None", "Proration/grace/offboarding", "FR-V12-A-016; FR-V12-A-021..022")
r("07", r"^(Identity|Business model|ICP / sales|Channels|Governance|Commercial|Activation)$", None, P, "Part 2.4 CFG-01..32; W33", "Configuration groups adopted", "FR-V12-A-090")
r("07", r"^(Envelope|Operating configuration|Usage|Fingerprint|Replay and revision)$", None, N, "US-2004 (no canonical envelope)", "Canonical application envelope", "FR-V12-A-096..097")
r("07", None, r"^The same contract governs|^V4 chapter guidance", P, "US-2004", "Envelope parity", "FR-V12-A-096")

# ---------- Domain chapters 13-16 (SKU outcome lines; service specs by Group B) ----------
r("1[3-7]", r"^SM-SVC-\d+$", None, P, "Part 2.1 modules M07-M66 (see §11.1.4 SKU crosswalk)", "SKU mapped; service specification by Group B", "FR-V12-A-001")
r(None, r"^MT-13$", None, P, "Offering/ICP config", "Offering-scoped audiences", "FR-V12-A-078")
r(None, r"^MT-2[23]$", None, P, "Sender identities (Part 2.4)", "Multiple accounts per channel/market", "FR-V12-A-077")
r("13|14", None, r"^Require source rights|^Omnichannel scope|^Control channel eligibility", C, "BR-M18/M19; DEC-029; PDP", "Retained", "—")
r(None, r"^REC-28$", None, C, "E-001..E-007 (Part 2.6)", "Retained", "—")
r("15", None, r"^Quotes use approved", C, "DEC-038; DEC-053; KPI-29", "Retained", "—")

# ---------- Customer success (ch17) ----------
r(None, r"^REC-25$", None, N, "None", "First-value checklist", "FR-V12-A-160..161")
r(None, r"^REC-27$", None, C, "CSO-11/12", "Retained", "—")
r("17", r"^(Contract / trial|Provision|Configure / import|Activation|Billing|SLA|Support|Renew/offboard)$", None, C, "Part 8.3c CSO-01..12", "Retained", "—")
r(None, r"^MOB-(05|14|17)$", None, C, "W21-W29 guard; Part 2.4 §2.30", "Retained", "—")
r("17", None, r"^Customer success: First value", N, "None", "First value = first accepted output", "DEC-519; FR-V12-A-160")
r(None, r"^RT-(10|14)$", None, C, "CSO-08/09; Part 9.8 QBR", "Retained", "—")
r(None, r"^RT-(01|02|03|04|05|06|08|09|12|13|15)$", None, P, "Part 9.8a health v2; Part 8.3c report", "Customer success capability", "FR-V12-A-160..170")
r(None, r"^CS-(04|05|06|08|09)$", None, C, "A110; certainty badges; A084; Part 2.4 §2.30.5", "Retained", "—")
r(None, r"^CS-(01|02|07|13)$", None, P, "CAP-X3-30; DEC-035", "Portal guidance and grounded help", "FR-V12-A-166..169")
r("17", None, r"^Define onboarding readiness", P, "CSO-06/07", "Activation metrics", "FR-V12-A-161")

# ---------- AI authority and governance (ch18) ----------
r(None, r"^REC-(01|03|09|11|12)$", None, C, "A109; A111; DEC-051; PDP; DEC-061", "Retained", "—")
r(None, r"^BR-V7-AI-0[2368]$", None, C, "PDP; DEC-061; Part 6.4 injection; kill switch", "Retained", "—")
r(None, r"^BR-V7-AI-01$", None, P, "AI disclosure labels", "AI transparency page and labels", "FR-V12-A-054; FR-V12-A-114")
r(None, r"^BR-V7-AI-04$", None, P, "DEC-008 hard caps", "Cost per accepted result report", "FR-V12-A-033; FR-V12-A-115")
r(None, r"^BR-V7-AI-05$", None, P, "Provider DPA no-training; DEC-421", "India region now; EU with CONFLICT-761", "FR-V12-A-116")
r(None, r"^BR-V7-AI-07$", None, P, "Part 6.4 eval sets (en)", "Language slice gates", "FR-V12-A-117")
r("18", None, r"^Scope\. Where AI may run", P, "Part 7.1 AI inventory", "159 of 517 steps AI; step detail Groups C/D/F", "FR-V12-A-118")
r("18", None, r"^AI is a means", C, "Part 1 §1.2.3 principles", "Retained", "—")
r(None, r"^MOB-09$", None, C, "Step-up; no approval from notification", "Retained", "—")
r(None, r"^MT-(12|28|32|35)$", None, C, "M02 claims; Part 2.35.3; A112; Part 7 registry", "Retained", "—")
r(None, r"^FL-(01|02|03|04|10)$", None, P, "WF-01..14; DEC-051", "156-workflow registry; detail Groups C/D/E", "FR-V12-A-002")
r(None, r"^FL-(05|06|07|08|11|13|14|15)$", None, C, "Outbox; DEC-051; dry-run; Part 7.3; A113", "Retained", "—")

# ---------- Command Centre (ch19) ----------
r(None, r"^REC-(02|06|13)$", None, C, "A110; A106; saved views", "Retained", "—")
r(None, r"^REC-1[45]$", None, P, "Part 2.4 §2.31 rules", "Cascading filters and reconciled drill-down", "FR-V12-A-123..124")
r(None, r"^MOB-0[678]$", None, C, "Part 2.5 responsive", "Retained", "—")
r("19", r"^(Website|Admin|Total)$", None, NA("presentation inventory; screens owned by Group G"), "Part 2.5", "—", "—", NA("presentation inventory; screens owned by Group G"))
r("19", None, r"^Dynamic service and workflow detail", NA("navigation rule; Group G"), "Part 2.5", "—", "—", NA("navigation rule; Group G"))
r(None, r"^MT-02$", None, C, "Startup switcher (Part 2.5)", "Retained", "—")
r(None, r"^MT-2[56]$", None, P, "Part 2.4 filters", "Context filters", "FR-V12-A-122..123")
r("19", None, r"^Universal Command Centre|^Nine optimization views|^V4 chapter guidance|^Each KPI is a labeled", P, "A089; Part 8.3c §8.3.5.15.7", "14 views + 9 perspectives", "DEC-509; FR-V12-A-120..121")
r("19", None, r"^Private Command Centre", P, "DEC-055", "Object-level drill-down grant", "DEC-509; FR-V12-A-125")
r("19", None, r"^View within A089", P, "A089", "14 views", "FR-V12-A-120")
r("19", r"^(Executive Overview|Market Intelligence|Lead & Contact|Digital Marketing|Omnichannel|Follow-up|Objection|Sales Pipeline|Revenue & Financial|Customer Success|Partner & Procurement|AI & Automation|Governance & Risk|Optimization Intelligence)", None, P, "A089 seven-view IA; RP-01..30", "View adopted", "FR-V12-A-120")
r("19", r"^\d+$", None, P, "A089; RP-01..30", "View KPI labels", "FR-V12-A-121")

# ---------- Security, privacy, compliance (ch20) ----------
r(None, r"^REC-10$", None, C, "Consent withdrawal scoped (Part 2.3)", "Retained", "—")
r(None, r"^CJ-GL-\d+$", None, C, "BR-M18/M19/M56/M02/M04/M25/M10/M31/M57/M51/M42/M43/M36", "Data-ethics rules mapped", "DEC-507")
r("20", None, r"^Business rules from the original", C, "BR-M rules", "Retained", "—")
r(None, r"^BR-V7-CJ-(02|03|06|08|09|11|12)$", None, C, "PDP; consent ledger; Part 4.1 breach; DEC-030; DPA", "Retained", "—")
r(None, r"^BR-V7-CJ-(04|05|10)$", None, P, "DLT; BRL-PRV; DEC-027", "DLT number series, nomination/grievance, EU VAT", "FR-V12-A-132..134")
r(None, r"^CJ-IN-(01|02|03|04|05|06|08|09|10|11)$", None, C, "Part 4.1 DPDP/TRAI/CERT-In; DEC-027; DEC-030", "Retained (legal review pending)", "—")
r(None, r"^CJ-IN-07$", None, N, "None", "140/160 number series rule", "FR-V12-A-133")
r(None, r"^CJ-EU-(0[1-8])$", None, P, "DEC-029 EU rules", "EU pack disabled until counsel approval", "DEC-507; FR-V12-A-131")
r(None, r"^CJ-EU-09$", None, P, "AI disclosure", "AI Act Art. 50 labels", "FR-V12-A-114")
r("20", None, r"^The platform sends commercial|^Subscriber \(tenant\)|^Platform operator:|^Legal owner|^Security owner|^Legal sign-off matrix", C, "Part 4.1 roles; DEC-029", "Retained; sign-off matrix", "FR-V12-A-135")
r(None, r"^MOB-10$", None, C, "ADR-139 PWA offline drafts only", "Retained", "—")
r(None, r"^MT-(20|24)$", None, C, "Jurisdiction rule pack; consent ledger", "Retained", "—")
r(None, r"^SEC-(0[1-46-9]|1[0-5])$", None, C, "Part 4.1; Part 4.4a", "Retained", "—")
r(None, r"^CS-15$", None, C, "CSO-10/11", "Retained", "—")
r("20", r"^BR-C(01|05|06|09|11|14)$", None, C, "See BR-C rows (chapter 01)", "Restated control", "—")

# ---------- SLA and support (ch21) ----------
r(None, r"^ENT-OPS-0[235]$", None, P, "Part 8.3c SLA-05/09; CAP-X3-12", "Severity, status page, tiered support", "DEC-510; FR-V12-A-141..143")
r(None, r"^ENT-OPS-06$", None, P, "Part 8.3b help; DEC-026", "Help centre top-50 tasks", "FR-V12-A-144")
r(None, r"^ENT-OPS-07$", None, C, "SLA-09 post-incident ≤ 5 business days", "Retained", "—")
r(None, r"^REC-2[234]$", None, C, "Part 3.6; Part 4.3; MNT calendar", "Retained", "—")
r(None, r"^REC-26$", None, P, "SLA framework", "Per-SKU workflow SLA matrix", "FR-V12-A-145")
r("21", r"^(HTTP p95|Error ratio|Queue age|Budget|Isolation / credential|Financial mismatch|AI quality|Backup)$", None, C, "Part 4.3 alerts; Part 4.4a", "Retained", "—")
r("21", r"^(Critical transactional data|Regenerable research data)$", None, C, "DEC-018; RC-2", "Retained", "—")
r(None, r"^MOB-12$", None, C, "WCAG 2.2 AA", "Retained", "—")
r(None, r"^ST-\d+$", None, C, "Part 4.2; Part 4.3; Part 4.4a", "Retained", "—")
r(None, r"^CS-(03|10)$", None, C, "Support escalation; WCAG", "Retained", "—")
r(None, r"^CS-11$", None, P, "CAP-X3-12", "Public neutral status + private incident detail", "FR-V12-A-142")
r("21", r"^(Availability)$", None, C, "SLA-02", "Retained", "DEC-510")
r("21", r"^(Support)$", None, P, "SLA-05", "P1 1 h / P2 4 h / P3 NBD as contract option", "DEC-510")
r("21", r"^(Workflow SLA)$", None, N, "None", "Per-SKU turnaround p50/p95 excl. held", "FR-V12-A-145")
r("21", r"^(Customer responsibilities)$", None, N, "None", "Customer responsibility schedule", "FR-V12-A-146")
r("21", r"^(Support access|Exit)$", None, C, "DEC-056; CSO-10/11", "Retained", "—")

# ---------- KPI framework (ch22) ----------
r(None, r"^REC-16$", None, C, "Part 8.3c §8.3.5.15.1", "Retained", "—")
r("22", r"^(Security|Performance|Cost|Automation|Stability|Scalability|Architecture|Database|API & Integration|AI Intelligence|Data Quality|Business Conversion|Maintainability|Reusability|UI/UX|Development Productivity|Testing & QC|Deployment & Recovery|Privacy & Compliance|SaaS Profitability)$", None, C, "Part 8.3c OPT-01..20 weights", "Retained", "—")
r("22", None, r"^Weight total", C, "Part 8.3c §8.3.5.15.1", "Retained", "—")
r(None, r"^KPI-\d+$", None, C, "Part 8.3c §8.3.5.15.4 OKPI-nn (alias of V12 KPI-nn)", "Alias recorded (V12 KPI-nn = OKPI-nn)", "DEC-500; DEC-511")
r("22", r"^(AI evaluation pass rate|Cost per accepted result|Injection red-team|Preflight hold rate|DSAR on-time|Breach notification|Consent coverage)", None, P, "Part 6.4; Part 4.1", "AI/compliance KPI registered", "DEC-511; FR-V12-A-150; ASSUMPTION-772")
r(None, r"^MT-(27|31|40)$", None, C, "Part 2.4 §2.31; Part 9.3 duplicate-ID scan", "Retained", "—")
r("22", None, r"^Business attribution", C, "Part 2.4 §2.31.2", "Retained", "—")
r("22", None, r"^Metric definitions|^Metric owner, approved denominator", P, "Part 1 §1.4.2 rules; CAP-X3-04", "Metric registry", "DEC-511; FR-V12-A-151..152")
r(None, r"^CS-12$", None, P, "Part 9.8 NPS/CSAT", "CSAT/CES/NPS definitions", "FR-V12-A-153")
r("22", r"^(NRR|Gross margin|Win rate|Verified revenue|Churn|Forecast error)$", None, C, "8.3c cohort metrics; KPI-09/13/16/29", "Retained", "DEC-511")
r("22", r"^(MRR|Activation|Accepted result rate|Lead-to-opportunity|ROAS|CAC / LTV)$", None, P, "KPI-10; KPI-25", "Business KPI registered", "DEC-511; FR-V12-A-150")

# ---------- Roadmap (ch23) ----------
r("23", None, r"^Note\. Durations", C, "Part 8.1 estimates", "Retained", "ASSUMPTION-770")
r(None, r"^REC-2[01]$", None, C, "Part 6.9 backlog; Part 4.3 pipeline", "Retained", "—")
r(None, r"^GO-0[1-8]$", None, C, "Part 8.2 go-live", "Retained", "—")
r(None, r"^MT-39$", None, C, "DEC-031; AP-01; Part 6.7", "Retained", "—")
r("23", None, r"^Execution order|^Release tags", P, "Part 8.1 waves", "P0/P1/P2 gating", "FR-V12-A-191")
r("23", r"^(P0|P1|P2)$", None, P, "Part 8.1 MoSCoW", "Priority gates", "FR-V12-A-191")
r("23", r"^(Foundation|R1 intelligence|R2 engagement|R3 conversion|R4 advanced)$", None, P, "Part 8.1 waves", "SKU release groups mapped", "FR-V12-A-192")

# ---------- Acceptance and traceability (ch24) ----------
r("24", r"^(Business/domain|Cross-artifact|UI/UX|Multi-tenant/issuer|AI workflow|Security & privacy|Reliability & perf|Test evidence|Weighted total|BRD V|FSD V|Website desktop|Website mobile|Admin desktop|Admin mobile|Criterion)", None, NA("customer's RCTCFE self-scores of its own artifacts"), "—", "Recorded in §11.1.1", "—", NA("customer's RCTCFE self-scores of its own artifacts"))
r("24", r"^(Document-implemented|Done|Prototype-implemented|Specified)$", None, NA("customer REC status counts"), "—", "Recorded", "—", NA("customer REC status counts"))
r(None, r"^REC-1[789]$", None, C, "Parts 3.5, 3.6, 6.8, 6.9", "Retained", "—")
r("24", r"^(API|Entity|Test|QC|Task)$", None, C, "Parts 3.5/3.6/6.8/6.9 reconciliation", "Retained", "—")
r(None, r"^E-00[1-7]$", None, C, "Part 2.6 E-001..E-007", "Retained", "—")
r(None, r"^XS-(0[1-9]|10)$", None, C, "AP-01..09; Part 6", "Retained", "TC-V12-A-201..210")
r(None, r"^V8-QA-\d+$", None, C, "Part 6 regression (see §11.1.4 V8-QA map)", "Alias to blueprint tests", "TC-V12-A-090")
r(None, r"^MOB-18$", None, C, "DEC-043 one codebase", "Retained", "—")
r("24", r"^MOB-\d+$", None, NA("prototype change log"), "—", "—", "—", NA("prototype change log"))
r("24", r"^BR-V7-", None, P, "See BR rows", "RTM rows added", "FR-V12-A-200")
r(None, r"^MT-3[678]$", None, C, "Part 3.5; design system; Part 6.8", "Retained", "—")
r(None, r"^SM-SVC-\d+-ENT-AT01$", None, N, "None (no SKU entitlement test)", "Parameterised SKU entitlement test", "TC-V12-A-020")
r("24", r"^(no_activation|fingerprint_reject|duplicate_import|new_revision_updates_pending|application_invalidation|quota_and_trace|budget_hold|reviewer_approval)$", None, P, "US-2004; BRL-SVC-03", "Behaviour covered by TC-V12-A", "TC-V12-A-095..099")
r("24", r"^(Test group|Website route shells|Admin registered|Home overflow|Cross-device|Other targeted)", None, NA("prototype test evidence"), "—", "—", "—", NA("prototype test evidence"))
r("24", r"^[a-z_]+$", None, NA("prototype browser evidence"), "—", "—", "—", NA("prototype browser evidence"))
r("24", None, r"^Acceptance and traceability: All 135", P, "None", "OPT-TC alias to TC-V12-A", "FR-V12-A-201")
r("24", None, r"^Business acceptance owner signs", N, "Part 8.2 sign-off (not per SKU)", "Per-SKU acceptance record", "FR-V12-A-202")
r("24", None, r"^(430/430|The RCTCFE review|Local Chromium|Score basis|Note\. 12/10|V3 remains)", NA("prototype evidence statement"), "—", "Recorded", "—", NA("prototype evidence statement"))
r("24", None, r"^•|^V6 business acceptance|^The FSD chapter 40|^Each V7 business", C, "Part 8.2 release gates; Part 6.6 RTM", "Retained", "—")

# ---------- Decisions (ch25) ----------
r(None, r"^DEC-V11-0[12]$", None, N, "None", "Recorded in V12 decision import", "DEC-518")
r(None, r"^REC-30$", None, C, "CONFLICT-462", "Recorded", "DEC-515")
r(None, r"^DEC-V9-0[234]$", None, C, "Part 0B coverage; BR-M rules; DEC-004 Apollo reserve", "Recorded", "DEC-518")
r(None, r"^DEC-V7-0[24567]$", None, C, "DEC-418; quiet hours; DLT; DEC-001/OKPI-13; DEC-008", "Answered by blueprint decision", "DEC-518")
r("25", r"^REC-\d", None, P, "Old REC series (V2) reused IDs", "Disambiguated as REC-V2-nn", "GAP-768; DEC-518")
r("25", r"^(Product owner / finance|Backend / database|Security / privacy / legal|Integrations / FinOps|AI / QA|Delivery owner)", None, P, "Part 8.2 RACI", "Decision ownership register", "FR-V12-A-210")
r("25", None, r"^Retain original 38|^The 180 inherited", C, "Part 0B; Part 9.1", "Retained (archive owned by Group L)", "—")

# ---------- Chapter 01 baseline and history ----------
r(None, r"^BR-V3-(0[2-4])$", None, P, "W04/W05/W11/W31", "Storefront discovery/selection", "FR-V12-A-055..057")
r(None, r"^BR-V3-(0[5-7])$", None, P, "W32/W33/US-2004", "Onboarding envelope", "FR-V12-A-090..097")
r(None, r"^BR-V3-08$", None, X, "DEC-065", "Customer parity", "DEC-504; CONFLICT-763")
r(None, r"^BR-V3-09$", None, P, "BRL-SVC-03", "Reservation at pending/queued/running", "FR-V12-A-014")
r(None, r"^BR-V3-10$", None, P, "A089", "14 views", "FR-V12-A-120")
r(None, r"^BR-V3-11$", None, P, "Part 2.1 modules", "39 service workspaces (Group B)", "FR-V12-A-003")
r(None, r"^BR-V3-12$", None, P, "A101; CSO", "Lifecycle controls", "FR-V12-A-016..022")
r(None, r"^BR-V3-13$", None, P, "A033/A110", "156 previews/517 walkthroughs (Groups C/D)", "FR-V12-A-002")
r(None, r"^BR-V3-14$", None, C, "Part 8.2 gates", "Retained", "—")
r(None, r"^BR-C(05|06|11|13|14)$", None, C, "PDP; RLS; BR-M18/19; Part 8.2; DEC-058", "Retained", "—")
r(None, r"^BR-C03$", None, P, "Part 1 scope", "39/156/25/15 inventory", "FR-V12-A-001")
r(None, r"^BR-C07$", None, P, "DEC-055", "Revocable grants", "FR-V12-A-072")
r(None, r"^BR-C08$", None, C, "DEC-052", "Retained; MedMaarg no patient data", "ASSUMPTION-771")
r(None, r"^BR-C10$", None, P, "Part 8.3c §8.3.5.13.2", "Versioned SaaS quote", "FR-V12-A-017; FR-V12-A-030")
r(None, r"^BR-C12$", None, P, "Part 3 migration", "Catalogue versioning and alias map", "FR-V12-A-004")
r(None, r"^BR-C15$", None, N, "DEC-415 precedence", "V12 precedence", "DEC-500")
r("01", None, r"^Purpose: a neutral SaaS", X, "BR-WEB (startup publication)", "Neutral storefront", "DEC-505; CONFLICT-764")
r("01", r"^(C3|C7)$", None, C, "DEC-518", "Recorded", "DEC-518")
r("01", r"^C[1-8]$", None, NA("prototype defect fixed by customer"), "—", "—", "—", NA("prototype defect fixed by customer"))
r("01", r"^(D10|D11|D14|D15|A11Y|CJ|AI)$", None, C, "BRL-APR-01; UI states; WCAG; DEC-027; Part 4.1; Part 7", "Behaviour retained", "—")
r("01", r"^(D\d+|M1|EVD)$", None, NA("customer document/prototype change history"), "—", "—", "—", NA("customer document/prototype change history"))
r("01", r"^P[1-8]$", None, C, "OKPI; PERF; BR-M; Part 8.2 GO; PEN; Part 7.4 VND; E-001; TRN", "Promoted items already covered from the 38-document pack", "—")
r("01", r"^P9$", None, X, "DEC-018; CONFLICT-462", "Growth RTO", "DEC-515; CONFLICT-765", PF)
r("01", r"^(Sales_Marketing|commercial_|Investment_Automation)", None, NA("provenance record"), "—", "Recorded in §11.1.1", "—", NA("provenance record"))
r("01", r"^Artifact$|^commercial_", None, NA("artifact checksum"), "—", "—", "—", NA("artifact checksum"))
r("01|24", r"^(Area|Product functionality|Multi-tenant isolation|AI governance|Compliance: jurisdictions|Business operations|Accessibility)", None, P, "Part 9.3 quality report", "Readiness register adopted", "FR-V12-A-200")
r("01", r"^(AI cost optimization|General cost optimization|Application security|Application stability|AI flow automation|Customer attraction|Customer retention|Customer conversion|Customer satisfaction|Total)$", None, N, "None (OPT taxonomy differs)", "135-OPT crosswalk §11.1.4", "DEC-500")
r("01", None, r"^(V11 inventory|V9 inventory|V8 inventory|Inventory:)", NA("superseded historical inventory; V12 inventory governs"), "—", "Recorded", "—", NA("superseded historical inventory; V12 inventory governs"))
r("01", None, r"inventory|Verified count|count", P, "Part 0B; §11.1.4", "Inventory reconciled", "DEC-500")
r("01", None, r"SHA-256|Prototype:|baseline: commercial", NA("artifact checksum"), "—", "Recorded", "—", NA("artifact checksum"))
r("01", None, r"Investment|not the Investment", C, "DEC-002; DEC-058; X-01", "Reaffirmed", "DEC-517")
r("01", None, r"^(V12 adds|Honest boundary|V11 is|V10 is|V11 verification|V9 reviews|Not promoted|V8 merges|V8 keeps|V6 handoff|V6 product vision|Requirement precedence|V5 scope|Status and precedence|Source precedence|Current prototype|V7 is)", P, "DEC-415 precedence; Part 0B", "V12 precedence and inventory", "DEC-500")

# ---------- Objectives, positioning (ch02, 03, 05) ----------
r(None, r"^BR-OBJ-0[1-5]$", None, P, "Part 1 §1.4.1 goals; KPI-01..31", "Objectives adopted with KPI-V12-A", "FR-V12-A-220; DEC-511")
r("02", None, r"^Proposed pilot outcomes", P, "Part 1 §1.13 hypotheses", "Hypotheses registered (not targets)", "FR-V12-A-221")
r("03", None, None, P, "Part 1 §1.3; §1.13", "Positioning and segment evidence", "FR-V12-A-222")
r(None, r"^AT-15$", None, P, "A108 operator enquiries", "Operator acquisition tenant", "FR-V12-A-073")
r("05", r"^(Operator|Subscriber)$", None, C, "CSO-01..12; WF-01..14", "Retained", "—")
r("05", r"^(Delivery models)$", None, P, "Part 8.3c service model", "Assisted and enterprise models added", "FR-V12-A-024")
r("05", r"^(Data ownership)$", None, C, "Part 4.1; DPA", "Retained", "—")

r("04|17|21", None, r"^Historical source:", C, "Part 8.3c; Part 4.3; Part 8.3b (38-document pack coverage)", "Provenance of retained candidate controls", "—")
r("11", r"^SKU$", None, NA("table header row"), "—", "—", "—", NA("table header row"))
r("21", r"^AI quality", None, C, "Part 4.3 alerts; kill switch", "Retained", "—")
r("22", r"^AI Intelligence$", None, C, "Part 8.3c weights", "Retained", "—")
r("23", None, r"Release gate: R3 conversion", P, "Part 8.1 waves", "SKU release groups mapped", "FR-V12-A-192")
r("24", r"^AI workflow quality", None, NA("customer's RCTCFE self-scores of its own artifacts"), "—", "Recorded in §11.1.1", "—", NA("customer's RCTCFE self-scores of its own artifacts"))
r("24", r"^AI governance and evaluation", None, P, "Part 9.3; Part 6.4", "Readiness register adopted", "FR-V12-A-200")
r("25", r"^AI / QA", None, P, "Part 8.2 RACI", "Decision ownership register", "FR-V12-A-210")
# ---------- Front matter / navigation / ID index ----------
r("00", None, r"^\d\d ", NA("chapter navigation"), "—", "—", "—", NA("chapter navigation"))
r("00", None, r"^(AI GROWTH ENGINE|SALES & MARKETING|AUTOMATION|Master Business|Contents|Table of contents)", NA("title page"), "—", "—", "—", NA("title page"))
r("00", None, r".", P, "DEC-415; Part 0B", "V12 inventory and reading order", "DEC-500")
r("AP", None, r".", N, "None (V12 ID families absent)", "ID family alias map §11.1.4", "DEC-500")
r("06", None, r"^MOB-01|Owner — Product", C, "DEC-043", "Retained", "—")

def classify(a):
    for ch, key, txt, before, loc, action, new, after in R:
        if ch and not ch.fullmatch(a["chapter"]): continue
        if key and not key.search(a["key"] or ""): continue
        if txt and not txt.search(a["text"]): continue
        return before, loc, action, new, after
    return None

rows, miss = [], []
for i, a in enumerate(A, 1):
    res = classify(a)
    if not res:
        miss.append(a); continue
    before, loc, action, new, after = res
    aid = a["key"] if re.fullmatch(r"[A-Z][A-Za-z0-9/-]*\d[A-Za-z0-9/-]*", a["key"] or "") else f"A-{a['chapter']}-{i:04d}"
    rows.append(dict(doc="BRD V12", chapter=a["chapter"], section=a["section"][:90], aspect_id=aid,
                     aspect_summary=a["text"][:300], status_before=before, blueprint_location=loc,
                     action=action, new_ids=new, status_after=after))

cnt = Counter(r_["aspect_id"] for r_ in rows); seen_ids = Counter()
for r_ in rows:
    if cnt[r_["aspect_id"]] > 1:
        base = f'{r_["aspect_id"]}@{r_["chapter"]}'
        seen_ids[base] += 1
        r_["aspect_id"] = base if seen_ids[base] == 1 else f"{base}.{seen_ids[base]}"
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["doc","chapter","section","aspect_id","aspect_summary","status_before","blueprint_location","action","new_ids","status_after"])
    w.writeheader(); w.writerows(rows)

print("classified", len(rows), "unclassified", len(miss))
for m in miss[:80]:
    print("MISS", m["chapter"], repr(m["key"]), m["text"][:120])
sb = Counter(r_["status_before"] for r_ in rows)
sa = Counter(r_["status_after"].split(" (")[0] for r_ in rows)
print("before", dict(sb)); print("after", dict(sa))
bych = {}
for r_ in rows:
    bych.setdefault(r_["chapter"], Counter())[r_["status_before"]] += 1
for k in sorted(bych): print(k, dict(bych[k]))
