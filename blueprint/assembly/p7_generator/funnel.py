"""Part 7.1 discovery funnel: structural screen of the stage x persona x pattern matrix
and the candidate-idea register with dispositions. Outputs markdown fragments."""
import itertools, collections

PATTERNS = ["AS", "CL", "EXT", "GEN", "VAL", "MON", "ORC", "AUT"]
PATTERN_NAMES = {
    "AS": "Assistant / copilot", "CL": "Classifier / router", "EXT": "Extractor",
    "GEN": "Generator", "VAL": "Validator / QA", "MON": "Monitor / anomaly detector",
    "ORC": "Orchestrator", "AUT": "Autonomous workflow agent"}

# In-product stages (spec dimension B) and delivery stages
PSTAGES = ["IN", "ON", "PR", "AP", "EX", "RE", "SU", "AD"]
PSTAGE_NAMES = {"IN": "Intake", "ON": "Onboarding", "PR": "Processing", "AP": "Approval",
                "EX": "Exception handling", "RE": "Reporting", "SU": "Support", "AD": "Administration"}
DSTAGES = ["RQ", "DS", "CD", "TS", "DP", "OP"]
DSTAGE_NAMES = {"RQ": "Requirements", "DS": "Design", "CD": "Coding", "TS": "Testing",
                "DP": "Deploy", "OP": "Operate"}

# Persona participation (1 = persona performs work in that stage). Source: Part 1 §1.8, §1.8.1; Part 2.3 roles.
PPART = {
 "P01": dict(IN=0, ON=0, PR=0, AP=1, EX=1, RE=1, SU=0, AD=1),
 "P02": dict(IN=0, ON=1, PR=1, AP=1, EX=1, RE=1, SU=0, AD=1),
 "P03": dict(IN=1, ON=1, PR=1, AP=1, EX=1, RE=1, SU=1, AD=0),
 "P04": dict(IN=1, ON=0, PR=1, AP=1, EX=1, RE=1, SU=0, AD=0),
 "P05": dict(IN=1, ON=0, PR=1, AP=1, EX=1, RE=1, SU=0, AD=0),
 "P06": dict(IN=1, ON=0, PR=1, AP=0, EX=1, RE=1, SU=0, AD=0),
 "P07": dict(IN=1, ON=1, PR=1, AP=0, EX=1, RE=1, SU=1, AD=0),
 "P08": dict(IN=0, ON=0, PR=1, AP=1, EX=1, RE=1, SU=0, AD=0),
 "P09": dict(IN=0, ON=0, PR=1, AP=1, EX=1, RE=1, SU=1, AD=1),
 "P10": dict(IN=0, ON=0, PR=1, AP=0, EX=1, RE=1, SU=0, AD=1),
 "P11": dict(IN=0, ON=1, PR=0, AP=0, EX=0, RE=1, SU=1, AD=1),
 "P12": dict(IN=0, ON=1, PR=0, AP=0, EX=1, RE=1, SU=1, AD=1),
 "P13": dict(IN=1, ON=1, PR=0, AP=0, EX=0, RE=1, SU=1, AD=1),
 "P14": dict(IN=1, ON=1, PR=0, AP=1, EX=0, RE=0, SU=1, AD=0),
 "P15": dict(IN=1, ON=0, PR=0, AP=0, EX=0, RE=0, SU=1, AD=0),
 "P16": dict(IN=1, ON=0, PR=1, AP=0, EX=1, RE=1, SU=0, AD=0),
}
# Delivery personas D01-D06 (ASSUMPTION-146, from DEC-005 team)
DPART = {
 "D01": dict(RQ=1, DS=1, CD=0, TS=1, DP=1, OP=1),  # Product Owner / founder-CTO
 "D02": dict(RQ=0, DS=1, CD=1, TS=1, DP=1, OP=1),  # Backend engineer
 "D03": dict(RQ=0, DS=1, CD=1, TS=1, DP=0, OP=0),  # Frontend engineer
 "D04": dict(RQ=1, DS=0, CD=1, TS=1, DP=1, OP=0),  # QA automation
 "D05": dict(RQ=0, DS=1, CD=1, TS=0, DP=1, OP=1),  # DevOps / SRE
 "D06": dict(RQ=1, DS=0, CD=0, TS=1, DP=0, OP=1),  # Growth / compliance / support lead
}
EXTERNAL = {"P14", "P15"}

def pattern_rule(stage, persona, pattern):
    """Return the rule ID that removes the cell, or None if structurally valid."""
    if stage == "AP" and pattern in ("GEN", "ORC", "AUT"):
        return "S2"  # AI never approves or produces the approved artefact at the approval step (BRL-AI-07, DEC-064)
    if persona in EXTERNAL and pattern in ("ORC", "AUT", "MON"):
        return "S3"  # external/anonymous actors get no orchestration, autonomy or monitoring agents (BRD §2, BR-S106/107)
    if persona == "P16" and pattern == "AS":
        return "S4"  # an assistant needs a human user
    if stage == "RE" and pattern == "AUT":
        return "S5"  # reporting has no autonomous external action
    if stage in ("CD", "DP") and pattern == "AUT":
        return "S6"  # no autonomous merge or production deploy (M62, DEC-063)
    return None

def structural():
    raw = {"in_product": len(PSTAGES) * len(PPART) * len(PATTERNS),
           "delivery": len(DSTAGES) * len(DPART) * len(PATTERNS)}
    removed = collections.Counter(); valid = set()
    for st, pe, pa in itertools.product(PSTAGES, PPART, PATTERNS):
        if not PPART[pe][st]:
            removed["S1"] += 1; continue
        r = pattern_rule(st, pe, pa)
        if r: removed[r] += 1; continue
        valid.add((st, pe, pa))
    for st, pe, pa in itertools.product(DSTAGES, DPART, PATTERNS):
        if not DPART[pe][st]:
            removed["S1"] += 1; continue
        r = pattern_rule(st, pe, pa)
        if r: removed[r] += 1; continue
        valid.add((st, pe, pa))
    return raw, removed, valid

# Candidate ideas. Fields: id, idea, stages, personas, patterns, disposition, target, reason
# disposition: KEEP (primary idea of an AG), MERGE (folded into target AG/AU), F5 (deterministic-first -> AU target),
#              F1 value, F2 data feasibility, F3 risk, F4 regulatory/policy, F6 cost
I = []
def idea(i, text, st, pe, pa, disp, target="", reason=""):
    I.append(dict(id=f"CI-{i:03d}", idea=text, st=st.split(), pe=pe.split(), pa=pa.split(),
                  disp=disp, target=target, reason=reason))

idea(1, "Answer anonymous visitors' product questions from approved public knowledge", "SU IN", "P15", "AS", "KEEP", "AG-017")
idea(2, "Classify public enquiry type and route to the owning startup", "IN", "P15 P16", "CL", "F5", "AU-020", "Typed form fields and routing rules decide deterministically (M22)")
idea(3, "Summarize free-text enquiries for the owner", "IN", "P03", "EXT", "MERGE", "AG-013", "Same inbound call returns a summary field")
idea(4, "Classify intent of inbound email, WhatsApp and web replies", "IN", "P16", "CL", "KEEP", "AG-013")
idea(5, "Detect STOP / opt-out in inbound text", "IN", "P16", "CL", "F5", "AU-008", "Keyword and List-Unsubscribe handling must be deterministic and instant (M04)")
idea(6, "Detect complaints in inbound messages", "EX", "P09", "CL", "MERGE", "AG-013", "Complaint is one intent class; deterministic threshold handling is AU-031")
idea(7, "Extract proposed meeting times from replies", "PR", "P03", "EXT", "MERGE", "AG-013", "Entity extraction in the same intent call; slots computed by AU-023")
idea(8, "Extract RFQ / purchase-order lines from documents and emails", "IN PR", "P07", "EXT", "KEEP", "AG-023")
idea(9, "Summarize submitted project requirements (W15) for AppNAI", "IN", "P06", "EXT", "MERGE", "AG-019", "Same document-analysis capability as RFP analysis")
idea(10, "AI verification of supplier registration documents", "IN", "P07", "VAL", "F3", "", "False verification risk; legal documents need human verification; format checks are field validation")
idea(11, "Triage student / guardian intake with AI", "IN", "P15", "CL", "F4", "", "Children's data (DEC-030): no minor data in AI beyond grade band; age-band routing is deterministic in AU-020")
idea(12, "Extract claim candidates and summaries from uploaded knowledge documents", "IN", "P05 P09", "EXT", "KEEP", "AG-001")
idea(13, "Map import file columns to versioned templates", "AD ON", "P11", "CL", "KEEP", "AG-010")
idea(14, "Infer consent from imported contact lists", "AD", "P09", "EXT", "F4", "", "Consent must be explicit recorded evidence (BRL-ELG, DEC-039); inference prohibited")
idea(15, "Generate research search queries from approved capabilities", "PR", "P04", "GEN", "KEEP", "AG-003")
idea(16, "Extract structured evidence from permitted web pages", "PR", "P16", "EXT", "KEEP", "AG-004")
idea(17, "Extract evidence from permitted social posts", "PR", "P04", "EXT", "MERGE", "AG-004", "Same extraction schema with source type = social (M33)")
idea(18, "Classify buying signals with confidence", "PR", "P04", "CL", "KEEP", "AG-005")
idea(19, "Derive explicit vs inferred business needs", "PR", "P04", "EXT", "KEEP", "AG-006")
idea(20, "Rank offerings against needs", "PR", "P04", "CL", "F5", "AU-016", "pgvector similarity + readiness gate is deterministic and cheaper (M16, BRL-SCR-04)")
idea(21, "Explain matches and exclusions in plain language", "PR", "P04", "GEN", "KEEP", "AG-007")
idea(22, "Score opportunities with an LLM", "PR", "P04", "CL", "F5", "AU-017", "Scoring formula is fixed by DEC-011; an LLM would add variance and cost")
idea(23, "Deduplicate and merge organizations", "PR", "P04", "VAL", "F5", "AU-015", "Domain + location + alias rules; ambiguous cases become human merge tasks (M13)")
idea(24, "Extract decision-maker roles and published work channels", "PR", "P04", "EXT", "KEEP", "AG-008")
idea(25, "Guess email addresses from name patterns", "PR", "P04", "GEN", "F4", "", "Prohibited: no guessed emails (BR-M18)")
idea(26, "Verify contacts with an LLM", "PR", "P04", "VAL", "F5", "AU-018", "Verification is provenance + channel checks, not language understanding (M19)")
idea(27, "Prepare cited qualification brief for the reviewer", "AP PR", "P04 P03", "EXT AS", "KEEP", "AG-009")
idea(28, "Accept qualification automatically once the 90% gate is met", "PR", "P16", "CL", "MERGE", "AG-009", "Same agent at L2 after DEC-001 benchmark gate (BRL-SCR-07)")
idea(29, "Generate queries targeting personal health conditions", "PR", "P04", "GEN", "F4", "", "Prohibited (BR-M10, PP-11)")
idea(30, "Draft personalized first-touch emails with evidence citations", "PR", "P03", "GEN", "KEEP", "AG-011")
idea(31, "Draft WhatsApp template messages", "PR", "P03", "GEN", "MERGE", "AG-011", "Same drafter, channel = WhatsApp, template constraints")
idea(32, "Draft follow-up sequence steps", "PR", "P03", "GEN", "MERGE", "AG-011", "Same drafter, mode = follow-up")
idea(33, "Draft renewal reminders", "PR", "P03", "GEN", "MERGE", "AG-011", "Same drafter, mode = renewal (M50)")
idea(34, "Draft webinar invitations and follow-ups", "PR", "P05", "GEN", "MERGE", "AG-011", "Same drafter, mode = event (M40)")
idea(35, "Optimize send time with an LLM", "PR", "P16", "CL", "F1", "", "Low value at pilot volume; quiet hours and time zones are rules (BRL-ELG); revisit with classical statistics after 6 months of data")
idea(36, "Check drafts for unsupported claims and prohibited content", "PR", "P09", "VAL", "KEEP", "AG-012")
idea(37, "Check tone and brand voice", "PR", "P05", "VAL", "MERGE", "AG-012", "Same validator call with brand rubric")
idea(38, "Suggest replies to inbound questions from approved knowledge", "SU", "P03", "GEN", "KEEP", "AG-014")
idea(39, "Send approved-FAQ answers autonomously", "PR", "P16", "AUT", "MERGE", "AG-014", "Same agent at L3 limited to approved FAQ (DEC-064)")
idea(40, "Auto-reply to objections with price concessions", "PR", "P03", "AUT", "F4", "", "Prices, discounts and terms are capped at L1 (DEC-064, BRL-AI-07)")
idea(41, "Classify objections and draft approved responses", "PR", "P03", "CL GEN", "KEEP", "AG-021")
idea(42, "Prepare meeting briefs from Customer 360", "PR", "P03", "GEN", "MERGE", "AG-015", "Copilot skill 'brief me on this account'")
idea(43, "Summarize meeting recordings / transcripts", "PR", "P03", "EXT", "F2", "", "No recording or transcript source in scope; calendar is free/busy only (DEC-024)")
idea(44, "Summarize Customer 360 timelines", "RE", "P03", "EXT", "MERGE", "AG-015", "Copilot skill over the same scoped records")
idea(45, "Answer staff questions over permitted records and knowledge", "SU", "P01 P02 P03", "AS", "KEEP", "AG-015")
idea(46, "Turn natural-language questions into saved-view filters", "SU", "P03", "CL", "MERGE", "AG-015", "Copilot proposes a filter draft; keyword search stays deterministic (DEC-037)")
idea(47, "Propose a commercial plan for simulation", "PR", "P10", "ORC", "KEEP", "AG-016")
idea(48, "Narrate simulation results", "RE", "P10", "GEN", "MERGE", "AG-016", "Planner returns the narrative with the plan")
idea(49, "Draft workflow DAGs from a description", "AD", "P10", "GEN", "MERGE", "AG-016", "Planner 'workflow draft' mode using approved node types only (DEC-051)")
idea(50, "Resolve conflicting automation actions", "EX", "P10", "CL", "F5", "AU-030", "Priority rules compliance > transactional > sales > marketing (BRL-AUT-09)")
idea(51, "Capture consented leads inside website chat", "IN", "P15", "EXT", "MERGE", "AG-017", "Website assistant hands a structured lead to M22")
idea(52, "Detect clinical questions in chat", "SU", "P15", "CL", "MERGE", "AG-017", "Keyword pre-filter plus the assistant's handover classifier (BRL-AI-11)")
idea(53, "Converse with minors in chat", "SU", "P15", "AS", "F4", "", "No profiling or data collection from minors (DEC-030); becomes a guardrail of AG-017")
idea(54, "Draft blog articles and knowledge-centre content", "PR", "P05", "GEN", "KEEP", "AG-018")
idea(55, "Draft social post variants", "PR", "P05", "GEN", "MERGE", "AG-018", "Content studio mode = social (M35)")
idea(56, "Draft landing-page copy", "PR", "P05", "GEN", "MERGE", "AG-018", "Content studio mode = landing (M37)")
idea(57, "Draft ad copy variants", "PR", "P05", "GEN", "MERGE", "AG-018", "Content studio mode = ad (M39); launch stays human")
idea(58, "Suggest SEO titles and meta descriptions", "PR", "P05", "GEN", "MERGE", "AG-018", "Content studio mode = SEO metadata (M36)")
idea(59, "Run technical SEO audits", "RE", "P05", "MON", "F5", "AU-033", "Crawl checks and Search Console metrics are deterministic (M36)")
idea(60, "Draft translations to hi-IN, ta-IN, or-IN", "PR", "P05", "GEN", "MERGE", "AG-018", "Content studio mode = translate; draft only (DEC-026)")
idea(61, "Generate images for creatives", "PR", "P05", "GEN", "F6", "", "Not in BRD; image generation adds cost and likeness/claims risk; approved brand assets suffice")
idea(62, "Optimize ad budgets autonomously", "PR", "P05", "AUT", "F4", "", "Spend only within approved caps (DEC-038); budget moves are human decisions")
idea(63, "Select campaign audiences with an LLM", "PR", "P05", "CL", "F4", "", "Audience = deterministic eligibility (M38); LLM profiling raises DPDP/fairness risk")
idea(64, "Classify permitted social posts into signals", "PR", "P04", "CL", "MERGE", "AG-005", "Same signal taxonomy (M33)")
idea(65, "Send automated social DMs", "PR", "P05", "AUT", "F4", "", "Prohibited (BR-M33, BR-M35)")
idea(66, "Analyse RFP / tender documents into a compliance matrix", "PR", "P06", "EXT", "KEEP", "AG-019")
idea(67, "Recommend bid / no-bid", "PR", "P06 P02", "AS", "MERGE", "AG-019", "Analyzer produces an L0 bid/no-bid brief; decision stays human")
idea(68, "Submit tenders autonomously", "PR", "P06", "AUT", "F4", "", "Never automated (DEC-053)")
idea(69, "Draft bid response sections", "PR", "P06", "GEN", "MERGE", "AG-020", "Proposal drafter mode = bid response")
idea(70, "Draft proposals from approved templates", "PR", "P03", "GEN", "KEEP", "AG-020")
idea(71, "Recommend prices or discounts", "PR", "P03", "GEN", "F4", "", "Prices come from approved price versions; AI never sets prices (DEC-064)")
idea(72, "Calculate quote lines", "PR", "P07", "VAL", "F5", "AU-035", "Decimal arithmetic with ROUND_HALF_UP (DEC-027)")
idea(73, "Assemble contracts from templates", "PR", "P09", "GEN", "F5", "AU-036", "Template merge + hash is deterministic (M46)")
idea(74, "Review counterparty redlines against the approved template", "AP PR", "P09", "VAL", "KEEP", "AG-022")
idea(75, "Sign agreements on behalf of the business", "PR", "P09", "AUT", "F4", "", "AI never signs (M46, BRL-AI-07)")
idea(76, "Extract fields from payment evidence for the maker", "PR", "P08", "EXT", "KEEP", "AG-024")
idea(77, "Verify payments with AI", "AP", "P08", "VAL", "F4", "", "Maker-checker by two humans (DEC-038, BRL-FIN)")
idea(78, "Match bank receipts to invoices", "PR", "P08", "CL", "F5", "AU-037", "Amount/reference/date matching rules")
idea(79, "Generate invoices", "PR", "P08", "GEN", "F5", "AU-035", "Deterministic from approved quote and tax profile")
idea(80, "Explain fulfilment discrepancies", "EX", "P07", "AS", "F1", "", "Ledger already shows the exact discrepancy (AU-038); narrative adds little")
idea(81, "Summarize the deal for onboarding handoff", "ON", "P03 P02", "GEN", "KEEP", "AG-025")
idea(82, "Generate onboarding checklists", "ON", "P02", "GEN", "F5", "AU-036", "Offering onboarding templates (CFG-19)")
idea(83, "Answer authenticated customers' portal questions", "ON SU", "P14", "AS", "MERGE", "AG-031", "Support desk assistant, portal mode, own records only")
idea(84, "Predict churn / account health with an LLM", "RE", "P02", "CL", "F5", "AU-039", "Rule-based health score; classical ML later; no medical data (M50)")
idea(85, "Classify loss reasons and aggregate themes", "RE", "P02 P03", "CL", "KEEP", "AG-026")
idea(86, "Re-contact lost deals automatically", "PR", "P03", "AUT", "F4", "", "No auto-recontact after loss without policy (BR-M51)")
idea(87, "Attribute revenue to channels", "RE", "P01", "CL", "F5", "AU-040", "Attribution models are deterministic (M52)")
idea(88, "Forecast pipeline with an LLM", "RE", "P01", "GEN", "F5", "AU-041", "Stage-weighted forecast with backtests (M60); LLMs are not forecasting models")
idea(89, "Narrate dashboards: what changed and why", "RE", "P01 P02", "GEN", "KEEP", "AG-029")
idea(90, "Detect KPI anomalies", "RE", "P01", "MON", "F5", "AU-012", "Statistical thresholds on metric snapshots")
idea(91, "Summarize competitor and market changes", "RE", "P04 P02", "GEN", "KEEP", "AG-027")
idea(92, "Generate comparative claims against competitors", "PR", "P05", "GEN", "F4", "", "No unverified comparative claims (BR-M59, BRL-AI-05)")
idea(93, "Triage failed runs, DLQ items and incidents", "EX", "P12 P10", "EXT", "KEEP", "AG-028")
idea(94, "Self-heal by letting an LLM retry steps", "EX", "P16", "CL", "F3", "", "Retries are deterministic and uncertain outcomes reconcile first (BRL-AUT-07)")
idea(95, "Write the founder's weekly insight digest", "RE", "P01", "GEN", "MERGE", "AG-029", "Narrative agent, portfolio mode (read-only aggregates, DEC-055)")
idea(96, "Propose SaaS client configuration from a business description", "ON", "P13", "GEN", "KEEP", "AG-030")
idea(97, "Verify SaaS applicant authority", "ON", "P12", "VAL", "F3", "", "Authority proof is a human/document check (BR-S111)")
idea(98, "Triage support tickets", "SU", "P12 P13", "CL", "KEEP", "AG-031")
idea(99, "Draft support replies", "SU", "P12", "GEN", "MERGE", "AG-031", "Same agent drafts the reply")
idea(100, "Explain billing disputes to clients", "SU", "P13", "AS", "F5", "AU-042", "Deterministic usage statement from metering; financial data stays out of prompts")
idea(101, "Handle privacy requests", "AD", "P09", "AS", "F5", "AU-011", "Identifier search and purge are deterministic (M56)")
idea(102, "Draft DPIAs", "AD", "P09", "GEN", "MERGE", "AG-033", "Delivery requirements assistant drafts compliance documents for legal review")
idea(103, "Recommend policy configuration", "AD", "P11", "GEN", "F3", "", "Loosening requires founder approval; low value; risk of unsafe defaults (DEC-038)")
idea(104, "Recommend roles and permissions", "AD", "P11", "CL", "F3", "", "Authorization expansion risk (BR-S117)")
idea(105, "Prepare partner due-diligence briefs", "PR", "P02", "EXT", "KEEP", "AG-032")
idea(106, "Profile individuals for insurance underwriting", "PR", "P02", "CL", "F4", "", "No underwriting or personal profiling (BR-M63)")
idea(107, "Monitor approval SLAs and escalate", "AP", "P01", "MON", "F5", "AU-027", "Timers and notifications (NT-009)")
idea(108, "Summarize changes for approvers", "AP", "P02", "EXT", "F5", "AU-036", "Deterministic diff between hashed revisions is exact; an LLM summary could omit a change")
idea(109, "Forecast AI spend and stop at cap", "AD", "P01", "MON", "F5", "AU-002", "Reserve-before-call and caps (M53)")
idea(110, "Judge AI outputs against eval rubrics", "AD", "P10", "VAL", "KEEP", "AG-002")
idea(111, "Sample production outputs for hallucination drift", "RE", "P10", "MON", "MERGE", "AG-002", "Same judge, production sampling mode")
idea(112, "Monitor claim and knowledge expiry", "RE", "P09", "MON", "F5", "AU-029", "Expiry dates and notifications (NT-036)")
idea(113, "Draft user stories and Gherkin acceptance criteria", "RQ", "D01", "GEN", "KEEP", "AG-033")
idea(114, "Check requirement-to-test traceability gaps", "RQ", "D04", "VAL", "MERGE", "AG-033", "Assistant proposes; the trace matrix check itself is a script in AU-013")
idea(115, "Draft architecture decision records", "DS", "D02", "GEN", "MERGE", "AG-033", "Same assistant, ADR template")
idea(116, "Draft threat models", "DS", "D05", "GEN", "MERGE", "AG-035", "Security review agent, design mode")
idea(117, "Suggest UI microcopy and accessibility fixes", "DS", "D03", "GEN", "MERGE", "AG-034", "Coding assistant in the IDE")
idea(118, "Generate and refactor code", "CD", "D02 D03", "AS", "KEEP", "AG-034")
idea(119, "Generate infrastructure-as-code", "CD", "D05", "GEN", "MERGE", "AG-034", "Coding assistant; plan reviewed in PR")
idea(120, "Review pull requests", "TS", "D02", "VAL", "KEEP", "AG-035")
idea(121, "Triage SAST and dependency findings", "TS", "D02", "VAL", "MERGE", "AG-035", "Same review agent")
idea(122, "Generate test cases from acceptance criteria", "TS", "D04", "GEN", "KEEP", "AG-036")
idea(123, "Generate synthetic fixtures (two tenants, 26 startups)", "TS", "D04", "GEN", "MERGE", "AG-036", "RECOMMENDATION-017 data sets")
idea(124, "Triage flaky tests and CI failures", "TS", "D04", "CL", "MERGE", "AG-035", "Review agent, CI-failure mode")
idea(125, "Write release notes", "DP", "D01", "GEN", "MERGE", "AG-035", "Review agent, release mode")
idea(126, "Summarize go/no-go risk for a release", "DP", "D01", "AS", "MERGE", "AG-035", "Review agent, release mode")
idea(127, "Triage production logs and alerts", "OP", "D05", "MON", "MERGE", "AG-028", "Same ops triage agent")
idea(128, "Remediate production autonomously (restart, scale, roll back)", "OP", "D05", "AUT", "F3", "", "Runbooks executed by humans; infrastructure changes via reviewed PRs (M09)")
idea(129, "Detect cost anomalies", "OP", "D05", "MON", "F5", "AU-012", "Cost ledger thresholds (A012)")
idea(130, "Draft help-centre articles from resolved tickets", "OP", "D06", "GEN", "MERGE", "AG-031", "Support desk assistant, KB mode; publish via approval")
idea(131, "Upgrade dependencies automatically", "CD", "D05", "GEN", "F5", "AU-013", "Renovate/Dependabot-style bot with CI gates")
idea(132, "Curate eval datasets from feedback", "TS", "D04", "GEN", "MERGE", "AG-036", "Redacted feedback becomes eval cases after review")
idea(133, "Analyse impact of a requirement change", "RQ", "D01", "AS", "MERGE", "AG-033", "Same assistant over the traceability matrix")
idea(134, "Write cited answers for reviewers about evidence freshness", "PR", "P04", "AS", "F1", "", "Freshness is a date field; the evidence panel already shows it (A017)")
idea(135, "Draft negotiation summaries for the Startup Head", "AP", "P02", "EXT", "MERGE", "AG-021", "Objection assistant produces the exception summary for A070")

DISP_LABEL = {"KEEP": "Kept (primary)", "MERGE": "Merged", "F5": "Deterministic first → AU",
              "F1": "Excluded: low value", "F2": "Excluded: data not available", "F3": "Excluded: risk",
              "F4": "Excluded: regulatory / policy", "F6": "Excluded: cost"}

def cells_of(idea, valid):
    return {(s, p, a) for s in idea["st"] for p in idea["pe"] for a in idea["pa"] if (s, p, a) in valid}

if __name__ == "__main__":
    raw, removed, valid = structural()
    print(raw, sum(raw.values()), removed, len(valid))
    anchored = set()
    for x in I:
        c = cells_of(x, valid)
        if not c: print("NO VALID CELL", x["id"], x["st"], x["pe"], x["pa"])
        anchored |= c
    print("anchored", len(anchored))
    print(collections.Counter(x["disp"] for x in I))
