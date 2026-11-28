#### AG-100 Inbound Voice Enquiry Router

| Field | Specification |
|---|---|
| Type | Agent · Classifier and router (voice) · scope: Product (tenant-enabled) |
| Purpose and business outcome | Classifies the **text transcript** of an inbound call (produced by the speech-to-text adapter, Group H) into intent, urgency and topic, answers only from **approved FAQ entries** read back by text-to-speech, and routes everything else to a human queue, so callers reach the right person within the SLA and no AI improvises on the phone (SM-SVC-26-WF01). |
| Linked BR / FR / US | SM-FR (SVC-26) via Group B; CJ-EU-09, CJ-IN-07, CJ-GL-06; FR-V12-F-051; DEC-064 (approved-FAQ replies up to L3); BR-M25, BR-M27; V12 AGT-20 · SM-SVC-26-WF01; US-08-YF01; TC-V12-F-131 |
| Persona | P14 caller (external); P03 thread owner; P10 automation lead |
| Trigger | Event: `call.transcript_segment.ready` from the voice adapter (inbound only; outbound voice has no AI step, SM-SVC-26-WF02) |
| Inputs and data sources | Transcript segment (untrusted, delimited, NFKC-normalized by AU-169), caller number hash, startup, business hours, approved FAQ set, routing table |
| Tools / APIs (registry §7.2.4) | TL-V12-F-01 `transcript.read` (current call only); TL-01 `knowledge.search` (approved FAQ namespace only); TL-08 `classification.write` |
| Outputs | `{intent, urgency, topic, faq_id/null, handoff_reason, disclosure_given:bool, confidence}` |
| Autonomy and HITL | **L3 only for verbatim approved-FAQ answers** (DEC-064) after the mandatory AI disclosure at call start (CJ-EU-09, AU-177); everything else **L0** → human handoff; urgent or clinical → immediate human (CJ-GL-06) |
| Model tier | 1a Haiku-class; 10% escalation to 1b for long or mixed-language segments |
| Tier 2 eligibility · data class | No · Restricted (caller identity, voice-derived text) |
| Prompt / context strategy | PRM-AGT-20-inbound-voice-enquiry-router-v1. Cached policy prefix + intent taxonomy + 6 examples (≈ 1,200 tokens); segment ≤ 600 tokens; synchronous, p95 ≤ 1.5 s per segment budget |
| Guardrails | No free-form generation spoken to callers (FAQ text only); no prices, terms or medical statements (VP-01, VP-04); recording/transcription only with consent flag captured by the IVR (AU-172); outbound calls never use this agent; number-series rules CJ-IN-07 enforced by AU-173 |
| Failure modes and fallback | Low confidence (< 0.7), refusal or timeout → human queue with transcript; STT outage → IVR menu (Tier 3); budget stop → IVR menu |
| Success KPIs | ≥ 90% correct routing on labelled calls; 100% urgent/clinical handoff; 0 non-FAQ spoken answers; median time-to-human ≤ 60 s |
| Eval dimensions | intent F1 ≥ 0.90 (no class < 0.80); urgent recall 100%; disclosure 100%; AI-INJ-09 multilingual; latency; cost; suites EVAL-SM-SVC-26-WF01… (§11.6.5.5) |
| Tokens, calls, cost | 2,000 in (1,200 cacheable, hit 60%), 150 out; 300 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [800×0.10 + 1,200×(0.6×0.01 + 0.4×0.125) + 150×0.50] ÷ 10⁶ = **₹0.020**; Sonnet per call = 90 × [800×2 + 1,200×(0.6×0.10 + 0.4×2.50) + 150×10] ÷ 10⁶ = **₹0.393**; blended at e = 10% = **₹0.057**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹5 · base ₹17 · high ₹52** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | Voice/STT/TTS adapters (Group H, CONFLICT-853 for provider); AU-169, AU-172, AU-173, AU-177; AU-009 |
| Release | Phase 2 (W6+) · separately approvable CR-V12-F; tenant opt-in |

#### AG-101 Marketing Creative Brief and Image Drafter

| Field | Specification |
|---|---|
| Type | Agent · Generator (creative brief + render request) · scope: Product |
| Purpose and business outcome | Turns an approved campaign brief into a **creative brief, layout specification and copy variants** and requests a render, either from approved brand templates (Tier 0, open-source renderer) or, only after a Founder decision, from an approved image-generation provider, so marketing gets on-brand draft creatives in minutes without unapproved claims or images (SM-SVC-27-WF01). |
| Linked BR / FR / US | SM-SVC-27; CJ-GL-13, CJ-EU-09 (machine-readable marking); FR-V12-F-052; BR-M36, BR-M38; V12 AGT-20 · SM-SVC-27-WF01; US-12-YF02; TC-V12-F-132 |
| Persona | P05 marketing specialist (author); R05L approver; R10 claims |
| Trigger | User action: 'Draft creatives' on an approved campaign brief (A056 family) |
| Inputs and data sources | Approved brief, approved claims (TL-09), brand kit (colours, fonts, logo rules), template catalogue, segment (deterministic) |
| Tools / APIs (registry §7.2.4) | TL-09 `claims.lookup`; TL-01 `knowledge.search` (brand guide); TL-V12-F-03 `creative.render_request` (Draft asset only); TL-06 `draft.create` |
| Outputs | `{creative_brief, layout_spec, copy_variants[], alt_text, claim_ids[], render_requests[]}` |
| Autonomy and HITL | **L1** — creative approver ≠ author approves exact asset hash; publication via AU-029 with C2PA-style/metadata marking (AU-177) |
| Model tier | 1b Sonnet (copy and layout reasoning); image rendering is not a Claude capability — template renderer by default; external image model pending CONFLICT-853 |
| Tier 2 eligibility · data class | No · Internal (non-personal); no people's likeness |
| Prompt / context strategy | PRM-AGT-20-marketing-creative-brief-and-v1. Brand policy prefix cached (≈ 1,500 tokens); brief ≤ 1,500 tokens; 2–4 variants; asynchronous |
| Guardrails | Only approved claims; no real persons, minors or patients depicted; no competitor marks; AG-103 validation mandatory before approval; alt text required (NFR accessibility) |
| Failure modes and fallback | Render failure → template-only asset; schema failure → 2 repairs → Tier 3 manual brief; budget stop → queue |
| Success KPIs | ≥ 70% of drafts approved with ≤ 2 edits; 0 unapproved claims; time brief→approved asset −50% |
| Eval dimensions | rubric ≥ 4/5; claims 100%; brand compliance; toxicity 0; cost; suites EVAL-SM-SVC-27-WF01… (§11.6.5.5) |
| Tokens, calls, cost | 3,500 in (1,500 cacheable, hit 60%), 900 out; 60 calls/month at pilot design volume [ASSUMPTION-863]. Sonnet per call = 90 × [2,000×2 + 1,500×(0.6×0.10 + 0.4×2.50) + 900×10] ÷ 10⁶ = **₹1.313**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹24 · base ₹79 · high ₹236** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AG-103, AU-029, AU-168, AU-177; renderer (open-source); CONFLICT-853 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-102 Audio, Subtitle and Creative Localization Agent

| Field | Specification |
|---|---|
| Type | Agent · Generator (localization) · scope: Product |
| Purpose and business outcome | Localizes **approved** subtitle files, voice-over scripts and creative text into enabled locales (hi-IN first; ta-IN, or-IN per DEC-026; de/fr only after EU launch), reusing translation memory, so localized creatives ship without meaning drift (SM-SVC-27-WF03; extends AG-050 to time-coded media text). |
| Linked BR / FR / US | SM-SVC-27; AIX-19; DEC-026; FR-V12-F-053; V12 AGT-20 · SM-SVC-27-WF03; US-11-YF03; TC-V12-F-133 |
| Persona | P05; locale reviewer |
| Trigger | User action: 'Localize' on an approved asset |
| Inputs and data sources | Approved source text with time codes, glossary, TM (TL-28), locale |
| Tools / APIs (registry §7.2.4) | TL-28 `tm.lookup`; TL-06 `draft.create` |
| Outputs | `{segments[{start,end,text}], glossary_hits[], back_translation, qa_flags[]}` |
| Autonomy and HITL | **L1** — locale reviewer approves |
| Model tier | 1a Haiku-class with 30% escalation to 1b for creative copy |
| Tier 2 eligibility · data class | Yes for Public approved text only (opt-in, default off) · Public / Internal |
| Prompt / context strategy | PRM-AGT-20-audio-subtitle-and-creative--v1. TM exact match first (AU-076, Tier 0); glossary prefix cached; ≤ 2,000 tokens per batch; Batch API |
| Guardrails | Placeholder/time-code equality check; glossary enforcement (AU-076); claim text must map to approved claim translation; no new claims |
| Failure modes and fallback | QA flag → human translator task; budget stop → queue |
| Success KPIs | ≥ 4/5 adequacy per locale (AIX-19); TM reuse ≥ 40%; 0 time-code errors |
| Eval dimensions | adequacy/fluency per locale; glossary; time-code validity; cost; suites EVAL-SM-SVC-27-WF03… (§11.6.5.5) |
| Tokens, calls, cost | 2,500 in (1,000 cacheable, hit 60%), 1,200 out; 80 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [1,500×0.10 + 1,000×(0.6×0.01 + 0.4×0.125) + 1,200×0.50] ÷ 10⁶ = **₹0.073**; Sonnet per call = 90 × [1,500×2 + 1,000×(0.6×0.10 + 0.4×2.50) + 1,200×10] ÷ 10⁶ = **₹1.445**; blended at e = 30% = **₹0.484**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹12 · base ₹39 · high ₹116** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AG-050, AU-076; TTS adapter (Group H) |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-103 Creative Brand, Rights and Claims Validator

| Field | Specification |
|---|---|
| Type | Agent · Validator (multimodal QA) · scope: Product |
| Purpose and business outcome | Checks every draft creative's **text, alt text, OCR and image description** against approved claims, brand rules, rights records and prohibited-content policies before a human approves it, so no creative with an unapproved claim, unlicensed asset or prohibited depiction reaches approval (SM-SVC-27-WF04; extends AG-012 to images). |
| Linked BR / FR / US | SM-SVC-27; CJ-GL-13; AIX-11; FR-V12-F-054; V12 AGT-20 · SM-SVC-27-WF04; US-11-YF04; TC-V12-F-134 |
| Persona | P09 legal/claims (reviewer); P05 author |
| Trigger | Event: `creative.draft.created` (AG-101 or uploaded asset) |
| Inputs and data sources | Asset preview (thumbnail, OCR text, alt text; AU-168 preview-first), rights record, claims registry, brand rules |
| Tools / APIs (registry §7.2.4) | TL-V12-F-02 `media.preview.read`; TL-09 `claims.lookup`; TL-08 `classification.write` |
| Outputs | `{verdict: pass/review/block, issues[{type, evidence, rule_id}], claim_ids[]}` |
| Autonomy and HITL | **L2** for block/review flags (stricter only); never approves; human approves the asset |
| Model tier | 1b Sonnet (vision on preview); full-resolution analysis only on justified escalation (AI-13) |
| Tier 2 eligibility · data class | No · Internal |
| Prompt / context strategy | PRM-AGT-20-creative-brand-rights-and-cl-v1. Rule prefix cached (≈ 1,800 tokens); preview image + OCR ≤ 2,500 tokens |
| Guardrails | Fails closed: any uncertainty → review; rights record missing → block; depictions of minors/patients → block |
| Failure modes and fallback | Model unavailable → mandatory human review (Tier 3) |
| Success KPIs | Seeded violation recall ≥ 95%; false-block ≤ 10%; 0 published creatives with unapproved claims |
| Eval dimensions | recall on seeded violations; precision; claim accuracy 100%; cost; suites EVAL-SM-SVC-27-WF04… (§11.6.5.5) |
| Tokens, calls, cost | 4,300 in (1,800 cacheable, hit 60%), 400 out; 80 calls/month at pilot design volume [ASSUMPTION-863]. Sonnet per call = 90 × [2,500×2 + 1,800×(0.6×0.10 + 0.4×2.50) + 400×10] ÷ 10⁶ = **₹0.982**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹24 · base ₹79 · high ₹236** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AG-012, AU-168, AU-177 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-104 Agentic Commerce Counterparty Reader and Quotation Drafter

| Field | Specification |
|---|---|
| Type | Agent · Extractor + Generator (reader step only) · scope: Product (default OFF) |
| Purpose and business outcome | Reads **signed** requirement and quotation messages from an authorized counterparty AI agent as untrusted data, extracts a typed requirement, and drafts a quotation response whose **prices and terms are inserted deterministically** from the approved price book (AU-089/AU-035), so AI-to-AI requests are answered faster without any binding commitment (SM-SVC-28-WF02/WF03). |
| Linked BR / FR / US | SM-SVC-28; AI-INJ-06; CTRL-AI-08; X-06; DEC-064; CONFLICT-854; FR-V12-F-055; V12 AGT-20 · SM-SVC-28-WF02; SM-SVC-28-WF03; US-13-YF05; TC-V12-F-135 |
| Persona | P03, P07 (approvers); counterparty agent (external) |
| Trigger | Event: `counterparty.message.verified` (signature and mandate scope verified by AU-175) |
| Inputs and data sources | Signed message (untrusted), mandate record (limits), approved offerings, price-book references (TL-27) |
| Tools / APIs (registry §7.2.4) | TL-V12-F-04 `counterparty_message.read`; TL-27 `pricebook.lookup` (references only); TL-06 `draft.create` |
| Outputs | `{requirement{items[], qty, delivery, constraints}, draft_response, price_refs[], out_of_mandate:bool}` |
| Autonomy and HITL | **L1** — every quotation or negotiation response is approved by R03/R07 under DEC-038 thresholds; **no mandate-based auto-acceptance** until CONFLICT-854 is decided; payments never (X-06) |
| Model tier | 1b Sonnet |
| Tier 2 eligibility · data class | No · Confidential |
| Prompt / context strategy | PRM-AGT-20-agentic-commerce-counterpart-v1. Policy prefix cached; message ≤ 3,000 tokens; reader step has no effect tools (AIX-09) |
| Guardrails | Counterparty text treated as data (CTRL-AI-01/08); request beyond mandate → HOLD; VP-01 no-price in free text; counterparty identity verified before read |
| Failure modes and fallback | Signature/mandate invalid → reject with reason; schema failure → Tier 3 manual |
| Success KPIs | Response draft within 15 min; 0 commitments without approval; 100% out-of-mandate requests held |
| Eval dimensions | extraction exact match ≥ 95%; AI-INJ-06 0 violations; schema 100%; suites EVAL-SM-SVC-28-WF02… (§11.6.5.5) |
| Tokens, calls, cost | 5,000 in (1,500 cacheable, hit 60%), 900 out; 30 calls/month at pilot design volume [ASSUMPTION-863]. Sonnet per call = 90 × [3,500×2 + 1,500×(0.6×0.10 + 0.4×2.50) + 900×10] ÷ 10⁶ = **₹1.583**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹14 · base ₹47 · high ₹142** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-175, AU-089, AU-035, AU-171; CONFLICT-854 |
| Release | Not before Founder decision (CONFLICT-854); earliest Phase 2 |

#### AG-105 Product Usage and Activation Analyst

| Field | Specification |
|---|---|
| Type | Agent · Analyst (narrative over deterministic metrics) · scope: Product |
| Purpose and business outcome | Explains **account-level** activation and feature-adoption metrics computed deterministically from authorized product-usage events, and lists expansion hypotheses limited to approved offerings, so customer-success staff act on real usage without reading raw logs (SM-SVC-34-WF01/WF03). |
| Linked BR / FR / US | SM-SVC-34; BR-SVC; CJ-GL-07; FR-V12-F-056; V12 AGT-20 · SM-SVC-34-WF01; SM-SVC-34-WF03; US-16-YF06; TC-V12-F-136 |
| Persona | P03 (CSM role), P02 |
| Trigger | Schedule: weekly per account; event: activation milestone missed |
| Inputs and data sources | Usage aggregates (TL-V12-F-05), plan/entitlement, health score (AU-093) |
| Tools / APIs (registry §7.2.4) | TL-V12-F-05 `usage.metrics.read` (aggregates); TL-12 `metrics.query`; TL-32 `finding.create` |
| Outputs | `{activation_state, drivers[], adoption_gaps[], hypotheses[{offering_id, evidence}]}` |
| Autonomy and HITL | **L0** |
| Model tier | 1a Haiku-class; 15% escalation |
| Tier 2 eligibility · data class | No · Confidential (tenant business data); no individual end-user profiling |
| Prompt / context strategy | PRM-AGT-20-product-usage-and-activation-v1. Metrics as typed JSON; numbers never generated (placeholders) |
| Guardrails | Account level only; no person-level behavioural profiling; no health/minor data; numbers from systems only |
| Failure modes and fallback | Metrics stale → skip with reason |
| Success KPIs | ≥ 80% of narratives rated useful; 0 invented numbers |
| Eval dimensions | groundedness ≥ 95%; numeric fidelity 100%; cost; suites EVAL-SM-SVC-34-WF01… (§11.6.5.5) |
| Tokens, calls, cost | 3,000 in (1,000 cacheable, hit 60%), 500 out; 200 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [2,000×0.10 + 1,000×(0.6×0.01 + 0.4×0.125) + 500×0.50] ÷ 10⁶ = **₹0.046**; Sonnet per call = 90 × [2,000×2 + 1,000×(0.6×0.10 + 0.4×2.50) + 500×10] ÷ 10⁶ = **₹0.905**; blended at e = 15% = **₹0.175**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹10 · base ₹35 · high ₹105** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-093, AU-102 semantic metrics; usage event adapter (Group H) |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-106 Trial Conversion and Upgrade Recommendation Drafter

| Field | Specification |
|---|---|
| Type | Agent · Generator (journey step and message drafts) · scope: Product |
| Purpose and business outcome | Drafts trial-to-paid and usage-based upgrade nudges (in-app message, email) from approved templates, triggered by deterministic usage thresholds, so conversions rise without pressure tactics or unapproved offers (SM-SVC-34-WF02/WF04). |
| Linked BR / FR / US | SM-SVC-34; DEC-047 plans; CJ-EU-02; FR-V12-F-057; V12 AGT-20 · SM-SVC-34-WF02; SM-SVC-34-WF04; US-20-YF07; TC-V12-F-137 |
| Persona | P13 SaaS client admin (recipient); P10 (approver of templates) |
| Trigger | Event: AU-042 entitlement 80% or trial day N |
| Inputs and data sources | Usage aggregates, plan catalogue (approved), template library |
| Tools / APIs (registry §7.2.4) | TL-06 `draft.create`; TL-V12-F-05 |
| Outputs | `{template_id, variables{}, channel, rationale}` |
| Autonomy and HITL | **L1** for new copy; **L2 dispatch** of approved templates via PDP (DEC-064) |
| Model tier | 1a Haiku-class; 20% escalation |
| Tier 2 eligibility · data class | No · Confidential |
| Prompt / context strategy | PRM-AGT-20-trial-conversion-and-upgrade-v1. Template-first; free text only in approved variable slots |
| Guardrails | No price or discount generation (VP-01); consent/preflight via AU-171; frequency caps |
| Failure modes and fallback | Template missing → task to P10 |
| Success KPIs | Trial conversion uplift measured by AU-065 holdout; 0 unapproved offers |
| Eval dimensions | rubric ≥ 4/5; claims 100%; cost; suites EVAL-SM-SVC-34-WF02… (§11.6.5.5) |
| Tokens, calls, cost | 2,200 in (900 cacheable, hit 60%), 400 out; 150 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [1,300×0.10 + 900×(0.6×0.01 + 0.4×0.125) + 400×0.50] ÷ 10⁶ = **₹0.034**; Sonnet per call = 90 × [1,300×2 + 900×(0.6×0.10 + 0.4×2.50) + 400×10] ÷ 10⁶ = **₹0.680**; blended at e = 20% = **₹0.163**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹7 · base ₹25 · high ₹74** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-042, AU-065, AU-171 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-107 Review and Reputation Monitor

| Field | Specification |
|---|---|
| Type | Agent · Classifier (reviews) · scope: Product |
| Purpose and business outcome | Classifies reviews and brand mentions from **authorized** review sources into sentiment, topic, severity and incident candidates, so reputation incidents are escalated within hours (SM-SVC-35-WF01/WF03). |
| Linked BR / FR / US | SM-SVC-35; CJ-GL-08; CJ-GL-06; FR-V12-F-058; V12 AGT-20 · SM-SVC-35-WF01; SM-SVC-35-WF03; US-11-YF08; TC-V12-F-138 |
| Persona | P05, P02; R10 for incidents |
| Trigger | Schedule: hourly fetch via review adapter; event: new review |
| Inputs and data sources | Review text (untrusted), rating, source, product/offering mapping |
| Tools / APIs (registry §7.2.4) | TL-V12-F-06 `reviews.read`; TL-08 `classification.write`; TL-32 `finding.create` |
| Outputs | `{sentiment, topics[], severity, incident_candidate:bool, clinical_or_safety:bool}` |
| Autonomy and HITL | **L2** labels; incident escalation automatic to humans (no external action) |
| Model tier | 1a Haiku-class; 10% escalation |
| Tier 2 eligibility · data class | No (reviews may name people) · Internal with personal data |
| Prompt / context strategy | PRM-AGT-20-review-and-reputation-monito-v1. Batch API for non-urgent; taxonomy prefix cached |
| Guardrails | Authorized sources only (AU-007); no reviewer profiling; clinical/safety mentions → human (CJ-GL-06) |
| Failure modes and fallback | Low confidence → review queue |
| Success KPIs | Incident detection ≤ 2 h; severity F1 ≥ 0.90 |
| Eval dimensions | F1 per class; calibration; AI-INJ-01; cost; suites EVAL-SM-SVC-35-WF01… (§11.6.5.5) |
| Tokens, calls, cost | 1,200 in (700 cacheable, hit 60%), 150 out; 900 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [500×0.10 + 700×(0.6×0.01 + 0.4×0.125) + 150×0.50] ÷ 10⁶ = **₹0.015**; Sonnet per call = 90 × [500×2 + 700×(0.6×0.10 + 0.4×2.50) + 150×10] ÷ 10⁶ = **₹0.292**; blended at e = 10% = **₹0.042**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹11 · base ₹38 · high ₹115** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | Review adapter (Group H); AU-007 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-108 Review Response Drafter

| Field | Specification |
|---|---|
| Type | Agent · Generator · scope: Product |
| Purpose and business outcome | Drafts evidence-grounded public replies to reviews from approved response templates and facts, so responses are prompt, consistent and never argumentative or misleading (SM-SVC-35-WF02). |
| Linked BR / FR / US | SM-SVC-35; CJ-GL-13; FR-V12-F-059; V12 AGT-20 · SM-SVC-35-WF02; US-11-YF09; TC-V12-F-139 |
| Persona | P05 author; R05L approver |
| Trigger | Event: AG-107 label = needs_response |
| Inputs and data sources | Review (untrusted), approved FAQ/claims, order/ticket facts the user can see |
| Tools / APIs (registry §7.2.4) | TL-01; TL-09; TL-06 `draft.create` |
| Outputs | `{reply_text, claim_ids[], escalate:bool}` |
| Autonomy and HITL | **L1** (public post) |
| Model tier | 1b Sonnet |
| Tier 2 eligibility · data class | No · Internal with personal data |
| Prompt / context strategy | PRM-AGT-20-review-response-drafter-v1. Policy prefix cached; ≤ 2,000 tokens |
| Guardrails | No personal data of the reviewer in replies; no admission of liability or medical statements; complaints → R10 |
| Failure modes and fallback | Guard fail → human |
| Success KPIs | Median response ≤ 24 h; ≥ 80% approved with ≤ 1 edit |
| Eval dimensions | rubric ≥ 4/5; claims 100%; toxicity 0; suites EVAL-SM-SVC-35-WF02… (§11.6.5.5) |
| Tokens, calls, cost | 2,500 in (1,200 cacheable, hit 60%), 250 out; 120 calls/month at pilot design volume [ASSUMPTION-863]. Sonnet per call = 90 × [1,300×2 + 1,200×(0.6×0.10 + 0.4×2.50) + 250×10] ÷ 10⁶ = **₹0.573**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹21 · base ₹69 · high ₹206** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AG-107, AG-012 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-109 Pricing and Margin Insight Analyst

| Field | Specification |
|---|---|
| Type | Agent · Analyst (L0) · scope: Product |
| Purpose and business outcome | Explains deterministic bundle-profitability and margin-anomaly results (AU-049, AU-089) in plain language with drivers and policy references, so finance and startup heads review pricing on evidence; **it never proposes or sets a price** (SM-SVC-37-WF01/WF04). |
| Linked BR / FR / US | SM-SVC-37; X-06; DEC-038; FR-V12-F-060; V12 AGT-20 · SM-SVC-37-WF01; SM-SVC-37-WF04; US-15-YF10; TC-V12-F-140 |
| Persona | P02, P08, P01 |
| Trigger | Schedule: monthly; event: margin anomaly from AU-089/AU-049 |
| Inputs and data sources | Deterministic margin tables, approved price-book references, DEC-038 thresholds |
| Tools / APIs (registry §7.2.4) | TL-12 `metrics.query`; TL-27 `pricebook.lookup` |
| Outputs | `{findings[{driver, metric_ref, policy_ref}], questions_for_owner[]}` |
| Autonomy and HITL | **L0** |
| Model tier | 1b Sonnet |
| Tier 2 eligibility · data class | No · Confidential |
| Prompt / context strategy | PRM-AGT-20-pricing-and-margin-insight-a-v1. Numbers as placeholders only |
| Guardrails | VP-01 no-price: digits/currency outside placeholders → block; no recommendation text containing price values |
| Failure modes and fallback | Data stale → skip |
| Success KPIs | Anomaly review within 2 business days; 0 generated prices |
| Eval dimensions | numeric fidelity 100%; groundedness; cost; suites EVAL-SM-SVC-37-WF01… (§11.6.5.5) |
| Tokens, calls, cost | 3,500 in (1,200 cacheable, hit 60%), 600 out; 40 calls/month at pilot design volume [ASSUMPTION-863]. Sonnet per call = 90 × [2,300×2 + 1,200×(0.6×0.10 + 0.4×2.50) + 600×10] ÷ 10⁶ = **₹1.068**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹13 · base ₹43 · high ₹128** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-049, AU-089 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-110 SMS and RCS Inbound Triage and Fallback Planner

| Field | Specification |
|---|---|
| Type | Agent · Classifier (SMS/RCS) + narrative · scope: Product |
| Purpose and business outcome | Classifies inbound SMS/RCS replies (STOP variants, question, complaint, wrong person) with AG-013's taxonomy and writes the weekly messaging-performance narrative, so opt-outs are honoured instantly and fallbacks use only approved channels (SM-SVC-38-WF03/WF04). |
| Linked BR / FR / US | SM-SVC-38; CJ-IN-06; CJ-GL-05; FR-V12-F-061; V12 AGT-20 · SM-SVC-38-WF03; SM-SVC-38-WF04; US-08-YF11; TC-V12-F-141 |
| Persona | P03; P10 |
| Trigger | Event: inbound SMS/RCS; schedule: weekly |
| Inputs and data sources | Message text (untrusted), DLT template ID, delivery receipts aggregates |
| Tools / APIs (registry §7.2.4) | TL-08; TL-12 |
| Outputs | `{intent, stop:bool, summary}`; weekly `{findings[]}` |
| Autonomy and HITL | **L3** classification (STOP lexicon first, AU-008); narrative L3 internal |
| Model tier | 1a Haiku-class |
| Tier 2 eligibility · data class | No · Restricted (phone numbers hashed before prompt) |
| Prompt / context strategy | PRM-AGT-20-sms-and-rcs-inbound-triage-a-v1. STOP lexicon at Tier 0 first; model only for non-lexicon text |
| Guardrails | Any STOP-like ambiguity → treat as STOP (fail closed); no outbound text generated |
| Failure modes and fallback | Model unavailable → lexicon only + human queue |
| Success KPIs | STOP recall 100%; intent F1 ≥ 0.90 |
| Eval dimensions | STOP recall; F1; AI-INJ-03; suites EVAL-SM-SVC-38-WF03… (§11.6.5.5) |
| Tokens, calls, cost | 900 in (600 cacheable, hit 60%), 80 out; 600 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [300×0.10 + 600×(0.6×0.01 + 0.4×0.125) + 80×0.50] ÷ 10⁶ = **₹0.009**; Sonnet per call = 90 × [300×2 + 600×(0.6×0.10 + 0.4×2.50) + 80×10] ÷ 10⁶ = **₹0.183**; blended at e = 5% = **₹0.018**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹3 · base ₹11 · high ₹32** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-008, AU-173, AG-013 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-111 Supplier Qualification and RFQ Analyst

| Field | Specification |
|---|---|
| Type | Agent · Extractor + Generator · scope: Product (OrganicSpec first) |
| Purpose and business outcome | Prepares supplier qualification checklists from evidence and drafts RFQs from approved requirement templates, then extracts and normalizes supplier quotations into a comparison table whose **arithmetic is deterministic**, so procurement decisions are faster and evidenced; it never awards, orders or commits (SM-SVC-39-WF01/WF02). |
| Linked BR / FR / US | SM-SVC-39; X-06; DEC-038; FR-V12-F-062; V12 AGT-20 · SM-SVC-39-WF01; SM-SVC-39-WF02; US-14-YF12; TC-V12-F-142 |
| Persona | P07 order coordinator; P08 |
| Trigger | User action: 'Prepare RFQ' / quotation uploaded |
| Inputs and data sources | Requirement, supplier records (TL-V12-F-08), uploaded quotations (untrusted, malware-scanned) |
| Tools / APIs (registry §7.2.4) | TL-V12-F-08 `supplier.read`; TL-14 `document.parse`; TL-06 `draft.create` |
| Outputs | `{checklist[], rfq_draft, quote_lines[{sku, unit, qty, price_ref, delivery}], gaps[]}` |
| Autonomy and HITL | **L1** for RFQ send (approver); comparison L0; PO commitment human-only (SM-SVC-39-WF03) |
| Model tier | 1a Haiku-class extraction; 1b for RFQ text (30%) |
| Tier 2 eligibility · data class | No · Confidential |
| Prompt / context strategy | PRM-AGT-20-supplier-qualification-and-r-v1. Extraction schema with quote-span check |
| Guardrails | Unit/currency normalization deterministic; quote substring verification; no award recommendation phrased as decision |
| Failure modes and fallback | Extraction confidence < 0.8 → manual entry task |
| Success KPIs | Field accuracy ≥ 95%; RFQ prep time −50% |
| Eval dimensions | extraction exact match ≥ 95%; schema 100%; cost; suites EVAL-SM-SVC-39-WF01… (§11.6.5.5) |
| Tokens, calls, cost | 4,000 in (1,000 cacheable, hit 60%), 800 out; 60 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [3,000×0.10 + 1,000×(0.6×0.01 + 0.4×0.125) + 800×0.50] ÷ 10⁶ = **₹0.068**; Sonnet per call = 90 × [3,000×2 + 1,000×(0.6×0.10 + 0.4×2.50) + 800×10] ÷ 10⁶ = **₹1.355**; blended at e = 30% = **₹0.454**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹8 · base ₹27 · high ₹82** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AG-023, AU-038 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-112 Marketplace Order-Event Classifier

| Field | Specification |
|---|---|
| Type | Agent · Classifier · scope: Product |
| Purpose and business outcome | Classifies free-text reasons on marketplace cancellations and returns, and drafts the internal handling note, so exceptions are routed correctly; stock and refunds are decided by rules and people (SM-SVC-31-WF03). |
| Linked BR / FR / US | SM-SVC-31; FR-V12-F-063; V12 AGT-20 · SM-SVC-31-WF03; US-14-YF13; TC-V12-F-143 |
| Persona | P07 |
| Trigger | Event: marketplace order event with free text |
| Inputs and data sources | Event payload (untrusted), order record |
| Tools / APIs (registry §7.2.4) | TL-V12-F-07 `marketplace.event.read`; TL-08 |
| Outputs | `{reason_code, severity, note}` |
| Autonomy and HITL | **L2** labels; refunds/inventory never |
| Model tier | 1a Haiku-class |
| Tier 2 eligibility · data class | No · Confidential |
| Prompt / context strategy | PRM-AGT-20-marketplace-order-event-clas-v1. Taxonomy prefix cached; Batch API |
| Guardrails | No refund or price action; fraud signals → AU-116 |
| Failure modes and fallback | Low confidence → queue |
| Success KPIs | Reason F1 ≥ 0.90 |
| Eval dimensions | F1; schema; cost; suites EVAL-SM-SVC-31-WF03… (§11.6.5.5) |
| Tokens, calls, cost | 800 in (500 cacheable, hit 60%), 100 out; 400 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [300×0.10 + 500×(0.6×0.01 + 0.4×0.125) + 100×0.50] ÷ 10⁶ = **₹0.010**; Sonnet per call = 90 × [300×2 + 500×(0.6×0.10 + 0.4×2.50) + 100×10] ÷ 10⁶ = **₹0.192**; blended at e = 5% = **₹0.019**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹2 · base ₹8 · high ₹23** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | Marketplace adapters (Group H); AU-116 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-113 Support Recovery and Recurring-Issue Analyst

| Field | Specification |
|---|---|
| Type | Agent · Generator + Analyst · scope: Product |
| Purpose and business outcome | Drafts service-recovery messages for SLA breaches (AU-027 flags) and clusters resolved tickets into recurring issues with KB-gap proposals, so customers hear from a human quickly and root causes are fixed (SM-SVC-33-WF03/WF04). |
| Linked BR / FR / US | SM-SVC-33; CS-02; FR-V12-F-064; V12 AGT-20 · SM-SVC-33-WF03; SM-SVC-33-WF04; US-16-YF14; TC-V12-F-144 |
| Persona | P12 support; P03 |
| Trigger | Event: SLA breach; schedule: weekly clustering |
| Inputs and data sources | Ticket thread (untrusted), SLA state, KB |
| Tools / APIs (registry §7.2.4) | TL-01; TL-02; TL-06; TL-32 |
| Outputs | `{recovery_draft}`; `{clusters[{theme, count, examples[]}], kb_gaps[]}` |
| Autonomy and HITL | **L1** recovery messages; L0 insights |
| Model tier | 1b drafts; 1a clustering |
| Tier 2 eligibility · data class | No · Internal with personal data |
| Prompt / context strategy | PRM-AGT-20-support-recovery-and-recurri-v1. Redacted ticket text; ≤ 3,000 tokens |
| Guardrails | No compensation/discount offers (VP-01); complaints → R10 |
| Failure modes and fallback | Guard fail → human |
| Success KPIs | Breach-to-contact ≤ 4 business hours; recurring-issue recall ≥ 80% |
| Eval dimensions | rubric; groundedness; cluster purity; suites EVAL-SM-SVC-33-WF03… (§11.6.5.5) |
| Tokens, calls, cost | 3,000 in (1,000 cacheable, hit 60%), 500 out; 200 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [2,000×0.10 + 1,000×(0.6×0.01 + 0.4×0.125) + 500×0.50] ÷ 10⁶ = **₹0.046**; Sonnet per call = 90 × [2,000×2 + 1,000×(0.6×0.10 + 0.4×2.50) + 500×10] ÷ 10⁶ = **₹0.905**; blended at e = 40% = **₹0.389**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹23 · base ₹78 · high ₹234** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AG-031, AU-027, AG-068 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-114 Sales Capability-Gap and Training Recommender

| Field | Specification |
|---|---|
| Type | Agent · Analyst · scope: Product |
| Purpose and business outcome | Turns **team-level** enablement metrics (asset use, stage conversion, objection themes) into training recommendations from the approved enablement catalogue, so managers coach on evidence without individual surveillance (SM-SVC-36-WF04). |
| Linked BR / FR / US | SM-SVC-36; AG-070; FR-V12-F-065; V12 AGT-20 · SM-SVC-36-WF04; US-16-YF15; TC-V12-F-145 |
| Persona | P02 manager |
| Trigger | Schedule: monthly |
| Inputs and data sources | Team aggregates (AU-083, AU-085), catalogue |
| Tools / APIs (registry §7.2.4) | TL-12; TL-01 |
| Outputs | `{gaps[], recommended_modules[]}` |
| Autonomy and HITL | **L0** |
| Model tier | 1a Haiku-class |
| Tier 2 eligibility · data class | No · Internal (aggregates; individuals only if opted in, AU-099 rule) |
| Prompt / context strategy | PRM-AGT-20-sales-capability-gap-and-tra-v1. Aggregates only |
| Guardrails | No ranking or scoring of named employees; no HR decisions |
| Failure modes and fallback | Insufficient data → 'insufficient data' |
| Success KPIs | ≥ 70% recommendations accepted |
| Eval dimensions | groundedness; fairness; suites EVAL-SM-SVC-36-WF04… (§11.6.5.5) |
| Tokens, calls, cost | 2,500 in (900 cacheable, hit 60%), 500 out; 20 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [1,600×0.10 + 900×(0.6×0.01 + 0.4×0.125) + 500×0.50] ÷ 10⁶ = **₹0.041**; Sonnet per call = 90 × [1,600×2 + 900×(0.6×0.10 + 0.4×2.50) + 500×10] ÷ 10⁶ = **₹0.824**; blended at e = 15% = **₹0.159**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹1 · base ₹3 · high ₹10** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-083, AG-070 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-115 Order Fulfilment Exception Analyst

| Field | Specification |
|---|---|
| Type | Agent · Analyst + Generator · scope: Product |
| Purpose and business outcome | Explains milestone slips and acceptance/delivery exceptions from the fulfilment ledger and drafts the customer update and internal task, so order coordinators resolve exceptions the same day (SM-SVC-20-WF02…04). |
| Linked BR / FR / US | SM-SVC-20; WF-10; FR-V12-F-066; V12 AGT-13 · SM-SVC-20-WF02; SM-SVC-20-WF03; SM-SVC-20-WF04; US-14-YF16; TC-V12-F-146 |
| Persona | P07 |
| Trigger | Event: AU-038 exception or milestone overdue |
| Inputs and data sources | Ledger entries, milestones, customer thread |
| Tools / APIs (registry §7.2.4) | TL-02; TL-06; TL-07 |
| Outputs | `{cause_hypotheses[], customer_update_draft, tasks[]}` |
| Autonomy and HITL | **L1** customer update; L0 analysis |
| Model tier | 1a; 25% escalation |
| Tier 2 eligibility · data class | No · Confidential |
| Prompt / context strategy | PRM-AGT-13-order-fulfilment-exception-a-v1. Ledger facts as typed fields |
| Guardrails | No delivery/date commitments beyond ledger; no refunds |
| Failure modes and fallback | Tier 3 task |
| Success KPIs | Exception closure ≤ 1 business day |
| Eval dimensions | groundedness; rubric; suites EVAL-SM-SVC-20-WF02… (§11.6.5.5) |
| Tokens, calls, cost | 2,500 in (900 cacheable, hit 60%), 500 out; 100 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [1,600×0.10 + 900×(0.6×0.01 + 0.4×0.125) + 500×0.50] ÷ 10⁶ = **₹0.041**; Sonnet per call = 90 × [1,600×2 + 900×(0.6×0.10 + 0.4×2.50) + 500×10] ÷ 10⁶ = **₹0.824**; blended at e = 25% = **₹0.237**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹7 · base ₹24 · high ₹71** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-038, AU-090 |
| Release | Release 2 candidate (W5) or Phase 2 · CR-V12-F |

#### AG-116 Receivable Discrepancy and Overdue-Risk Explainer

| Field | Specification |
|---|---|
| Type | Agent · Analyst (L0) · scope: Product |
| Purpose and business outcome | Explains reconciliation discrepancies and overdue-risk flags computed by rules (AU-037, AU-116) for Finance makers, so investigations start with the likely cause; it never matches, verifies or moves money (SM-SVC-21-WF03/WF04). |
| Linked BR / FR / US | SM-SVC-21; X-06; FR-V12-F-067; V12 AGT-16 · SM-SVC-21-WF03; SM-SVC-21-WF04; US-15-YF17; TC-V12-F-147 |
| Persona | P08 |
| Trigger | Event: discrepancy/overdue flag |
| Inputs and data sources | Match proposal, ledger lines, flags |
| Tools / APIs (registry §7.2.4) | TL-02; TL-12 |
| Outputs | `{explanation, evidence_refs[], next_check}` |
| Autonomy and HITL | **L0** |
| Model tier | 1a Haiku-class |
| Tier 2 eligibility · data class | No · Restricted (financial evidence) |
| Prompt / context strategy | PRM-AGT-16-receivable-discrepancy-and-o-v1. Typed fields only; no bank identifiers beyond last 4 |
| Guardrails | Numbers from systems only; maker-checker untouched |
| Failure modes and fallback | Skip; manual |
| Success KPIs | Investigation time −30% |
| Eval dimensions | numeric fidelity 100%; groundedness; suites EVAL-SM-SVC-21-WF03… (§11.6.5.5) |
| Tokens, calls, cost | 1,800 in (700 cacheable, hit 60%), 300 out; 80 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [1,100×0.10 + 700×(0.6×0.01 + 0.4×0.125) + 300×0.50] ÷ 10⁶ = **₹0.027**; Sonnet per call = 90 × [1,100×2 + 700×(0.6×0.10 + 0.4×2.50) + 300×10] ÷ 10⁶ = **₹0.535**; blended at e = 10% = **₹0.078**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹2 · base ₹6 · high ₹19** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-037, AU-116 |
| Release | Release 2 candidate · CR-V12-F |

#### AG-117 Contract Drafting and Obligation Extractor

| Field | Specification |
|---|---|
| Type | Agent · Generator + Extractor · scope: Product |
| Purpose and business outcome | Fills approved contract/MoU templates with deal facts (AU-036 assembles) and extracts obligations, dates and renewal terms from executed agreements into a register, so Legal drafts faster and obligations are tracked; it never signs or alters approved clauses (SM-SVC-18-WF02/WF04). |
| Linked BR / FR / US | SM-SVC-18; CJ-GL-12; X-06; FR-V12-F-068; V12 AGT-14 · SM-SVC-18-WF02; SM-SVC-18-WF04; US-13-YF18; TC-V12-F-148 |
| Persona | P09 legal; P02 |
| Trigger | User action: 'Draft MoU'; event: signed document stored |
| Inputs and data sources | Template + clause library, deal record, signed document (hash-verified) |
| Tools / APIs (registry §7.2.4) | TL-14; TL-02; TL-06 |
| Outputs | `{draft_fields{}, deviations[]}`; `{obligations[{party, text_span, due, recurrence}]}` |
| Autonomy and HITL | **L1** drafts (Legal approves); **L0** obligations register entries confirmed by Legal |
| Model tier | 1b Sonnet |
| Tier 2 eligibility · data class | No · Confidential |
| Prompt / context strategy | PRM-AGT-14-contract-drafting-and-obliga-v1. Clause IDs, not free text; span-cited extraction |
| Guardrails | Approved clauses immutable; any non-standard request → Legal (DEC-038); scenario analysis labelled estimates |
| Failure modes and fallback | Tier 3 manual |
| Success KPIs | Obligation extraction exact match ≥ 95%; draft time −40% |
| Eval dimensions | extraction; deviation recall; schema; suites EVAL-SM-SVC-18-WF02… (§11.6.5.5) |
| Tokens, calls, cost | 6,000 in (2,000 cacheable, hit 60%), 1,000 out; 40 calls/month at pilot design volume [ASSUMPTION-863]. Sonnet per call = 90 × [4,000×2 + 2,000×(0.6×0.10 + 0.4×2.50) + 1,000×10] ÷ 10⁶ = **₹1.811**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹22 · base ₹72 · high ₹217** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-036, AG-022 |
| Release | Release 2 candidate · CR-V12-F |

#### AG-118 Search and Answer-Engine Visibility Analyst

| Field | Specification |
|---|---|
| Type | Agent · Analyst + Generator · scope: Product |
| Purpose and business outcome | Interprets authorized Search Console data, AU-033 audit findings and **answer-engine visibility probes** (how AI search summarizes the startup, from approved queries), and drafts prioritized fixes and content briefs, so organic and AI-search visibility improve without fabricated rankings (SM-SVC-13-WF01…04). |
| Linked BR / FR / US | SM-SVC-13; CJ-GL-13; FR-V12-F-069; V12 AGT-11 · SM-SVC-13-WF01…WF04; US-11-YF19; TC-V12-F-149 |
| Persona | P05 |
| Trigger | Schedule: weekly |
| Inputs and data sources | Search metrics (authorized), audit findings, probe results (public) |
| Tools / APIs (registry §7.2.4) | TL-V12-F-09 `seo.metrics.read`; TL-06 |
| Outputs | `{issues[], opportunities[], briefs[]}` |
| Autonomy and HITL | **L0** (changes go through AG-018/L1) |
| Model tier | 1a; 20% escalation |
| Tier 2 eligibility · data class | Yes — Public data only, opt-in, default off · Public |
| Prompt / context strategy | PRM-AGT-11-search-and-answer-engine-vis-v1. Batch API |
| Guardrails | No ranking claims without source; probes use approved query lists only |
| Failure modes and fallback | Skip week |
| Success KPIs | Fix adoption ≥ 50%; visibility trend reported with source |
| Eval dimensions | groundedness; ranking NDCG vs analyst; cost; suites EVAL-SM-SVC-13-WF01…WF04… (§11.6.5.5) |
| Tokens, calls, cost | 3,000 in (1,000 cacheable, hit 60%), 700 out; 40 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [2,000×0.10 + 1,000×(0.6×0.01 + 0.4×0.125) + 700×0.50] ÷ 10⁶ = **₹0.055**; Sonnet per call = 90 × [2,000×2 + 1,000×(0.6×0.10 + 0.4×2.50) + 700×10] ÷ 10⁶ = **₹1.085**; blended at e = 20% = **₹0.261**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹3 · base ₹10 · high ₹31** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-033 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-119 Social Listening and Community Response Drafter

| Field | Specification |
|---|---|
| Type | Agent · Classifier + Generator · scope: Product |
| Purpose and business outcome | Classifies engagement on the startup's **own** published posts and permitted public mentions, and drafts public community replies, so the brand responds in hours; no private-group scraping or automated DMs (SM-SVC-12-WF02…04). |
| Linked BR / FR / US | SM-SVC-12; CJ-GL-08; X-05; FR-V12-F-070; V12 AGT-11 · SM-SVC-12-WF02; SM-SVC-12-WF03; SM-SVC-12-WF04; US-11-YF20; TC-V12-F-150 |
| Persona | P05 |
| Trigger | Event: engagement on own post; schedule: daily listening |
| Inputs and data sources | Own-post comments and permitted public mentions (untrusted) |
| Tools / APIs (registry §7.2.4) | TL-V12-F-10 `social.read_permitted`; TL-08; TL-06 |
| Outputs | `{labels}`; `{reply_draft, escalate}` |
| Autonomy and HITL | **L2** labels; **L1** replies |
| Model tier | 1a labels; 1b replies |
| Tier 2 eligibility · data class | No · Internal with personal data |
| Prompt / context strategy | PRM-AGT-11-social-listening-and-communi-v1. Batch for listening |
| Guardrails | CJ-GL-08 adapter blocks DMs and private sources; complaints → R10 |
| Failure modes and fallback | Queue |
| Success KPIs | Response ≤ 8 business hours; label F1 ≥ 0.90 |
| Eval dimensions | F1; rubric; toxicity 0; suites EVAL-SM-SVC-12-WF02… (§11.6.5.5) |
| Tokens, calls, cost | 1,200 in (700 cacheable, hit 60%), 200 out; 500 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [500×0.10 + 700×(0.6×0.01 + 0.4×0.125) + 200×0.50] ÷ 10⁶ = **₹0.017**; Sonnet per call = 90 × [500×2 + 700×(0.6×0.10 + 0.4×2.50) + 200×10] ÷ 10⁶ = **₹0.337**; blended at e = 15% = **₹0.065**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹10 · base ₹32 · high ₹97** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-007; social adapters (Group H) |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-120 Deliverability Diagnostics Advisor

| Field | Specification |
|---|---|
| Type | Agent · Analyst (L0) · scope: Product |
| Purpose and business outcome | Explains sender-reputation and deliverability signals (bounces, complaints, authentication results, AU-024 counters) and lists checklist fixes, so senders avoid blocklisting; it never changes DNS, volumes or sends (SM-SVC-06-WF04). |
| Linked BR / FR / US | SM-SVC-06; CJ-GL-09; FR-V12-F-071; V12 AGT-06 · SM-SVC-06-WF04; US-08-YF21; TC-V12-F-151 |
| Persona | P10; P03 |
| Trigger | Schedule: weekly; event: complaint/bounce threshold |
| Inputs and data sources | Aggregated delivery metrics |
| Tools / APIs (registry §7.2.4) | TL-12 |
| Outputs | `{findings[], fixes[]}` |
| Autonomy and HITL | **L0** |
| Model tier | 1a |
| Tier 2 eligibility · data class | Yes — aggregates only, opt-in · Internal-non-personal |
| Prompt / context strategy | PRM-AGT-06-deliverability-diagnostics-a-v1. Aggregates |
| Guardrails | No sending; AU-031 still pauses campaigns |
| Failure modes and fallback | Skip |
| Success KPIs | Complaint rate below threshold; bounce ≤ 2% |
| Eval dimensions | groundedness; suites EVAL-SM-SVC-06-WF04… (§11.6.5.5) |
| Tokens, calls, cost | 2,000 in (800 cacheable, hit 60%), 400 out; 20 calls/month at pilot design volume [ASSUMPTION-863]. Haiku per call = 90 × [1,200×0.10 + 800×(0.6×0.01 + 0.4×0.125) + 400×0.50] ÷ 10⁶ = **₹0.033**; Sonnet per call = 90 × [1,200×2 + 800×(0.6×0.10 + 0.4×2.50) + 400×10] ÷ 10⁶ = **₹0.652**; blended at e = 10% = **₹0.095**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹1 · base ₹2 · high ₹6** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-024, AU-031 |
| Release | Release 2 candidate · CR-V12-F |

#### AG-121 Multimodal Enquiry Interpreter

| Field | Specification |
|---|---|
| Type | Agent · Extractor (images, document photos, voice-note transcripts) · scope: Product |
| Purpose and business outcome | Extracts the business question from an inbound image, document photo or voice-note transcript (text-first, preview-first, AI-13) and hands a typed enquiry to AG-013/AG-014, so multilingual multimodal enquiries are answered from approved knowledge (SM-SVC-09-WF04). |
| Linked BR / FR / US | SM-SVC-09; AI-13; CJ-GL-06; FR-V12-F-072; V12 AGT-08 · SM-SVC-09-WF04; US-10-YF22; TC-V12-F-152 |
| Persona | P14 (sender); P03 |
| Trigger | Event: inbound attachment on an enquiry thread |
| Inputs and data sources | Attachment preview/OCR/transcript (untrusted) |
| Tools / APIs (registry §7.2.4) | TL-V12-F-02; TL-08 |
| Outputs | `{extracted_question, language, contains_health_or_minor:bool, confidence}` |
| Autonomy and HITL | **L2** extraction; replies follow AG-014 rules |
| Model tier | 1b (vision) on preview; full media only with justification |
| Tier 2 eligibility · data class | No · Restricted (may contain personal data) |
| Prompt / context strategy | PRM-AGT-08-multimodal-enquiry-interpret-v1. Preview-first |
| Guardrails | Health/minor content → human (CJ-GL-06); prescriptions/medical images never interpreted |
| Failure modes and fallback | Human queue |
| Success KPIs | Extraction accuracy ≥ 95% |
| Eval dimensions | exact match; AI-INJ-04; cost; suites EVAL-SM-SVC-09-WF04… (§11.6.5.5) |
| Tokens, calls, cost | 2,500 in (800 cacheable, hit 60%), 200 out; 150 calls/month at pilot design volume [ASSUMPTION-863]. Sonnet per call = 90 × [1,700×2 + 800×(0.6×0.10 + 0.4×2.50) + 200×10] ÷ 10⁶ = **₹0.562**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹25 · base ₹84 · high ₹253** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AU-168, AG-013, AG-014 |
| Release | Phase 2 (W6+) · CR-V12-F |

#### AG-122 Onboarding and Pilot Readiness Planner

| Field | Specification |
|---|---|
| Type | Agent · Planner (draft plans) · scope: Product |
| Purpose and business outcome | Drafts institutional pilot and deployment-readiness plans from templates, milestone history and checklist gaps (AU-043), and adapts them when readiness signals change, so pilots start on time with explicit owners (SM-SVC-22-WF02/WF04). |
| Linked BR / FR / US | SM-SVC-22; BR-M48; FR-V12-F-073; V12 AGT-17 · SM-SVC-22-WF02; SM-SVC-22-WF04; US-16-YF23; TC-V12-F-153 |
| Persona | P02, P03 |
| Trigger | Event: deal won with pilot flag; readiness change |
| Inputs and data sources | Template, milestones, checklist |
| Tools / APIs (registry §7.2.4) | TL-02; TL-06 |
| Outputs | `{plan_draft{milestones[], owners[], risks[]}}` |
| Autonomy and HITL | **L1** |
| Model tier | 1b Sonnet |
| Tier 2 eligibility · data class | No · Confidential |
| Prompt / context strategy | PRM-AGT-17-onboarding-and-pilot-readine-v1. Template-first |
| Guardrails | No commitments to dates beyond approved plan; MedMaarg: no patient data; EduVerse: institution level |
| Failure modes and fallback | Tier 3 template |
| Success KPIs | Pilot start on planned date ≥ 80% |
| Eval dimensions | rubric; groundedness; suites EVAL-SM-SVC-22-WF02… (§11.6.5.5) |
| Tokens, calls, cost | 3,000 in (1,200 cacheable, hit 60%), 800 out; 15 calls/month at pilot design volume [ASSUMPTION-863]. Sonnet per call = 90 × [1,800×2 + 1,200×(0.6×0.10 + 0.4×2.50) + 800×10] ÷ 10⁶ = **₹1.158**; proposed line CR-V12-F-R (not B02). **Monthly: low ₹5 · base ₹17 · high ₹52** (before the 25% overhead allowance; verify prices at implementation, as of 27 Nov 2026) |
| Dependencies | AG-025, AU-043, AU-090 |
| Release | Release 2 candidate · CR-V12-F |
