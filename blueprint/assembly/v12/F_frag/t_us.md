##### US-08-YF01 Inbound Voice Enquiry Router (AG-100, AGT-20)

**As** P14 caller (external), **I want** the platform to classify the text transcript of an inbound call (produced by the speech-to-text adapter, Group H) into intent, urgency and topic, answers only from approved FAQ entries read back by text-to-speech, and routes everything else to a human queue, **so that** callers reach the right person within the SLA and no AI improvises on the phone. Traces: FR-V12-F-051; SM-SVC-26-WF01; TC-V12-F-131.

```gherkin
Feature: Inbound Voice Enquiry Router
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-26-WF01 and the EVAL suite passes for the locale
    And the agent AG-100 is enabled with an approved PRM version
    When the trigger occurs: Event: `call.transcript_segment.ready` from the voice adapter (inbound only; outbound voice has no AI step, SM
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L3 only for verbatim approved-FAQ answers
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-12-YF02 Marketing Creative Brief and Image Drafter (AG-101, AGT-20)

**As** P05 marketing specialist (author), **I want** the platform to turn an approved campaign brief into a creative brief, layout specification and copy variants and requests a render, either from approved brand templates (Tier 0, open-source renderer) or, only after a Founder decision, from an approved image-generation provider, **so that** marketing gets on-brand draft creatives in minutes without unapproved claims or images. Traces: FR-V12-F-052; SM-SVC-27-WF01; TC-V12-F-132.

```gherkin
Feature: Marketing Creative Brief and Image Drafter
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-27-WF01 and the EVAL suite passes for the locale
    And the agent AG-101 is enabled with an approved PRM version
    When the trigger occurs: User action: 'Draft creatives' on an approved campaign brief (A056 family)
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L1
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-11-YF03 Audio, Subtitle and Creative Localization Agent (AG-102, AGT-20)

**As** P05, **I want** the platform to localize approved subtitle files, voice-over scripts and creative text into enabled locales (hi-IN first; ta-IN, or-IN per DEC-026; de/fr only after EU launch), reusing translation memory, **so that** localized creatives ship without meaning drift. Traces: FR-V12-F-053; SM-SVC-27-WF03; TC-V12-F-133.

```gherkin
Feature: Audio, Subtitle and Creative Localization Agent
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-27-WF03 and the EVAL suite passes for the locale
    And the agent AG-102 is enabled with an approved PRM version
    When the trigger occurs: User action: 'Localize' on an approved asset
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L1
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-11-YF04 Creative Brand, Rights and Claims Validator (AG-103, AGT-20)

**As** P09 legal/claims (reviewer), **I want** the platform to check every draft creative's text, alt text, OCR and image description against approved claims, brand rules, rights records and prohibited-content policies before a human approves it, **so that** no creative with an unapproved claim, unlicensed asset or prohibited depiction reaches approval. Traces: FR-V12-F-054; SM-SVC-27-WF04; TC-V12-F-134.

```gherkin
Feature: Creative Brand, Rights and Claims Validator
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-27-WF04 and the EVAL suite passes for the locale
    And the agent AG-103 is enabled with an approved PRM version
    When the trigger occurs: Event: `creative.draft.created` (AG-101 or uploaded asset)
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L2 for block/review flags
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-13-YF05 Agentic Commerce Counterparty Reader and Quotation Drafter (AG-104, AGT-20)

**As** P03, P07 (approvers), **I want** the platform to read signed requirement and quotation messages from an authorized counterparty AI agent as untrusted data, extracts a typed requirement, and drafts a quotation response whose prices and terms are inserted deterministically from the approved price book (AU-089/AU-035), **so that** AI-to-AI requests are answered faster without any binding commitment. Traces: FR-V12-F-055; SM-SVC-28-WF02; SM-SVC-28-WF03; TC-V12-F-135.

```gherkin
Feature: Agentic Commerce Counterparty Reader and Quotation Drafter
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-28-WF02 and the EVAL suite passes for the locale
    And the agent AG-104 is enabled with an approved PRM version
    When the trigger occurs: Event: `counterparty.message.verified` (signature and mandate scope verified by AU-175)
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L1
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-16-YF06 Product Usage and Activation Analyst (AG-105, AGT-20)

**As** P03 (CSM role), P02, **I want** the platform to explain account-level activation and feature-adoption metrics computed deterministically from authorized product-usage events, and lists expansion hypotheses limited to approved offerings, **so that** customer-success staff act on real usage without reading raw logs. Traces: FR-V12-F-056; SM-SVC-34-WF01; SM-SVC-34-WF03; TC-V12-F-136.

```gherkin
Feature: Product Usage and Activation Analyst
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-34-WF01 and the EVAL suite passes for the locale
    And the agent AG-105 is enabled with an approved PRM version
    When the trigger occurs: Schedule: weekly per account; event: activation milestone missed
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L0
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-20-YF07 Trial Conversion and Upgrade Recommendation Drafter (AG-106, AGT-20)

**As** P13 SaaS client admin (recipient), **I want** the platform to draft trial-to-paid and usage-based upgrade nudges (in-app message, email) from approved templates, triggered by deterministic usage thresholds, **so that** conversions rise without pressure tactics or unapproved offers. Traces: FR-V12-F-057; SM-SVC-34-WF02; SM-SVC-34-WF04; TC-V12-F-137.

```gherkin
Feature: Trial Conversion and Upgrade Recommendation Drafter
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-34-WF02 and the EVAL suite passes for the locale
    And the agent AG-106 is enabled with an approved PRM version
    When the trigger occurs: Event: AU-042 entitlement 80% or trial day N
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L1 for new copy
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-11-YF08 Review and Reputation Monitor (AG-107, AGT-20)

**As** P05, P02, **I want** the platform to classify reviews and brand mentions from authorized review sources into sentiment, topic, severity and incident candidates, **so that** reputation incidents are escalated within hours. Traces: FR-V12-F-058; SM-SVC-35-WF01; SM-SVC-35-WF03; TC-V12-F-138.

```gherkin
Feature: Review and Reputation Monitor
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-35-WF01 and the EVAL suite passes for the locale
    And the agent AG-107 is enabled with an approved PRM version
    When the trigger occurs: Schedule: hourly fetch via review adapter; event: new review
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L2 labels
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-11-YF09 Review Response Drafter (AG-108, AGT-20)

**As** P05 author, **I want** the platform to draft evidence-grounded public replies to reviews from approved response templates and facts, **so that** responses are prompt, consistent and never argumentative or misleading. Traces: FR-V12-F-059; SM-SVC-35-WF02; TC-V12-F-139.

```gherkin
Feature: Review Response Drafter
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-35-WF02 and the EVAL suite passes for the locale
    And the agent AG-108 is enabled with an approved PRM version
    When the trigger occurs: Event: AG-107 label = needs_response
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L1
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-15-YF10 Pricing and Margin Insight Analyst (AG-109, AGT-20)

**As** P02, P08, P01, **I want** the platform to explain deterministic bundle-profitability and margin-anomaly results (AU-049, AU-089) in plain language with drivers and policy references, **so that** finance and startup heads review pricing on evidence; **it never proposes or sets a price**. Traces: FR-V12-F-060; SM-SVC-37-WF01; SM-SVC-37-WF04; TC-V12-F-140.

```gherkin
Feature: Pricing and Margin Insight Analyst
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-37-WF01 and the EVAL suite passes for the locale
    And the agent AG-109 is enabled with an approved PRM version
    When the trigger occurs: Schedule: monthly; event: margin anomaly from AU-089/AU-049
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L0
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-08-YF11 SMS and RCS Inbound Triage and Fallback Planner (AG-110, AGT-20)

**As** P03, **I want** the platform to classify inbound SMS/RCS replies (STOP variants, question, complaint, wrong person) with AG-013's taxonomy and writes the weekly messaging-performance narrative, **so that** opt-outs are honoured instantly and fallbacks use only approved channels. Traces: FR-V12-F-061; SM-SVC-38-WF03; SM-SVC-38-WF04; TC-V12-F-141.

```gherkin
Feature: SMS and RCS Inbound Triage and Fallback Planner
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-38-WF03 and the EVAL suite passes for the locale
    And the agent AG-110 is enabled with an approved PRM version
    When the trigger occurs: Event: inbound SMS/RCS; schedule: weekly
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L3 classification
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-14-YF12 Supplier Qualification and RFQ Analyst (AG-111, AGT-20)

**As** P07 order coordinator, **I want** the platform to prepare supplier qualification checklists from evidence and drafts RFQs from approved requirement templates, then extracts and normalizes supplier quotations into a comparison table whose arithmetic is deterministic, **so that** procurement decisions are faster and evidenced; it never awards, orders or commits. Traces: FR-V12-F-062; SM-SVC-39-WF01; SM-SVC-39-WF02; TC-V12-F-142.

```gherkin
Feature: Supplier Qualification and RFQ Analyst
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-39-WF01 and the EVAL suite passes for the locale
    And the agent AG-111 is enabled with an approved PRM version
    When the trigger occurs: User action: 'Prepare RFQ' / quotation uploaded
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L1 for RFQ send
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-14-YF13 Marketplace Order-Event Classifier (AG-112, AGT-20)

**As** P07, **I want** the platform to classify free-text reasons on marketplace cancellations and returns, and drafts the internal handling note, **so that** exceptions are routed correctly; stock and refunds are decided by rules and people. Traces: FR-V12-F-063; SM-SVC-31-WF03; TC-V12-F-143.

```gherkin
Feature: Marketplace Order-Event Classifier
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-31-WF03 and the EVAL suite passes for the locale
    And the agent AG-112 is enabled with an approved PRM version
    When the trigger occurs: Event: marketplace order event with free text
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L2 labels
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-16-YF14 Support Recovery and Recurring-Issue Analyst (AG-113, AGT-20)

**As** P12 support, **I want** the platform to draft service-recovery messages for SLA breaches (AU-027 flags) and clusters resolved tickets into recurring issues with KB-gap proposals, **so that** customers hear from a human quickly and root causes are fixed. Traces: FR-V12-F-064; SM-SVC-33-WF03; SM-SVC-33-WF04; TC-V12-F-144.

```gherkin
Feature: Support Recovery and Recurring-Issue Analyst
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-33-WF03 and the EVAL suite passes for the locale
    And the agent AG-113 is enabled with an approved PRM version
    When the trigger occurs: Event: SLA breach; schedule: weekly clustering
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L1 recovery messages
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-16-YF15 Sales Capability-Gap and Training Recommender (AG-114, AGT-20)

**As** P02 manager, **I want** the platform to turn team-level enablement metrics (asset use, stage conversion, objection themes) into training recommendations from the approved enablement catalogue, **so that** managers coach on evidence without individual surveillance. Traces: FR-V12-F-065; SM-SVC-36-WF04; TC-V12-F-145.

```gherkin
Feature: Sales Capability-Gap and Training Recommender
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-36-WF04 and the EVAL suite passes for the locale
    And the agent AG-114 is enabled with an approved PRM version
    When the trigger occurs: Schedule: monthly
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L0
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-14-YF16 Order Fulfilment Exception Analyst (AG-115, AGT-13)

**As** P07, **I want** the platform to explain milestone slips and acceptance/delivery exceptions from the fulfilment ledger and drafts the customer update and internal task, **so that** order coordinators resolve exceptions the same day. Traces: FR-V12-F-066; SM-SVC-20-WF02; SM-SVC-20-WF03; SM-SVC-20-WF04; TC-V12-F-146.

```gherkin
Feature: Order Fulfilment Exception Analyst
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-20-WF02 and the EVAL suite passes for the locale
    And the agent AG-115 is enabled with an approved PRM version
    When the trigger occurs: Event: AU-038 exception or milestone overdue
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L1 customer update
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-15-YF17 Receivable Discrepancy and Overdue-Risk Explainer (AG-116, AGT-16)

**As** P08, **I want** the platform to explain reconciliation discrepancies and overdue-risk flags computed by rules (AU-037, AU-116) for Finance makers, **so that** investigations start with the likely cause; it never matches, verifies or moves money. Traces: FR-V12-F-067; SM-SVC-21-WF03; SM-SVC-21-WF04; TC-V12-F-147.

```gherkin
Feature: Receivable Discrepancy and Overdue-Risk Explainer
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-21-WF03 and the EVAL suite passes for the locale
    And the agent AG-116 is enabled with an approved PRM version
    When the trigger occurs: Event: discrepancy/overdue flag
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L0
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-13-YF18 Contract Drafting and Obligation Extractor (AG-117, AGT-14)

**As** P09 legal, **I want** the platform to fill approved contract/MoU templates with deal facts (AU-036 assembles) and extracts obligations, dates and renewal terms from executed agreements into a register, **so that** Legal drafts faster and obligations are tracked; it never signs or alters approved clauses. Traces: FR-V12-F-068; SM-SVC-18-WF02; SM-SVC-18-WF04; TC-V12-F-148.

```gherkin
Feature: Contract Drafting and Obligation Extractor
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-18-WF02 and the EVAL suite passes for the locale
    And the agent AG-117 is enabled with an approved PRM version
    When the trigger occurs: User action: 'Draft MoU'; event: signed document stored
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L1 drafts
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-11-YF19 Search and Answer-Engine Visibility Analyst (AG-118, AGT-11)

**As** P05, **I want** the platform to interpret authorized Search Console data, AU-033 audit findings and answer-engine visibility probes (how AI search summarizes the startup, from approved queries), and drafts prioritized fixes and content briefs, **so that** organic and AI-search visibility improve without fabricated rankings. Traces: FR-V12-F-069; SM-SVC-13-WF01…WF04; TC-V12-F-149.

```gherkin
Feature: Search and Answer-Engine Visibility Analyst
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-13-WF01 and the EVAL suite passes for the locale
    And the agent AG-118 is enabled with an approved PRM version
    When the trigger occurs: Schedule: weekly
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L0
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-11-YF20 Social Listening and Community Response Drafter (AG-119, AGT-11)

**As** P05, **I want** the platform to classify engagement on the startup's own published posts and permitted public mentions, and drafts public community replies, **so that** the brand responds in hours; no private-group scraping or automated DMs. Traces: FR-V12-F-070; SM-SVC-12-WF02; SM-SVC-12-WF03; SM-SVC-12-WF04; TC-V12-F-150.

```gherkin
Feature: Social Listening and Community Response Drafter
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-12-WF02 and the EVAL suite passes for the locale
    And the agent AG-119 is enabled with an approved PRM version
    When the trigger occurs: Event: engagement on own post; schedule: daily listening
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L2 labels
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-08-YF21 Deliverability Diagnostics Advisor (AG-120, AGT-06)

**As** P10, **I want** the platform to explain sender-reputation and deliverability signals (bounces, complaints, authentication results, AU-024 counters) and lists checklist fixes, **so that** senders avoid blocklisting; it never changes DNS, volumes or sends. Traces: FR-V12-F-071; SM-SVC-06-WF04; TC-V12-F-151.

```gherkin
Feature: Deliverability Diagnostics Advisor
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-06-WF04 and the EVAL suite passes for the locale
    And the agent AG-120 is enabled with an approved PRM version
    When the trigger occurs: Schedule: weekly; event: complaint/bounce threshold
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L0
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-10-YF22 Multimodal Enquiry Interpreter (AG-121, AGT-08)

**As** P14 (sender), **I want** the platform to extract the business question from an inbound image, document photo or voice-note transcript (text-first, preview-first, AI-13) and hands a typed enquiry to AG-013/AG-014, **so that** multilingual multimodal enquiries are answered from approved knowledge. Traces: FR-V12-F-072; SM-SVC-09-WF04; TC-V12-F-152.

```gherkin
Feature: Multimodal Enquiry Interpreter
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-09-WF04 and the EVAL suite passes for the locale
    And the agent AG-121 is enabled with an approved PRM version
    When the trigger occurs: Event: inbound attachment on an enquiry thread
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L2 extraction
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-16-YF23 Onboarding and Pilot Readiness Planner (AG-122, AGT-17)

**As** P02, P03, **I want** the platform to draft institutional pilot and deployment-readiness plans from templates, milestone history and checklist gaps (AU-043), and adapts them when readiness signals change, **so that** pilots start on time with explicit owners. Traces: FR-V12-F-073; SM-SVC-22-WF02; SM-SVC-22-WF04; TC-V12-F-153.

```gherkin
Feature: Onboarding and Pilot Readiness Planner
  Scenario: Happy path within scope
    Given the tenant has entitlement for SM-SVC-22-WF02 and the EVAL suite passes for the locale
    And the agent AG-122 is enabled with an approved PRM version
    When the trigger occurs: Event: deal won with pilot flag; readiness change
    Then a schema-valid output is produced with evidence IDs
    And the output is handled at autonomy L1
  Scenario: Guardrail and fallback
    Given the input contains an injected instruction or out-of-policy content
    When the agent runs
    Then no effect tool is available and the output is held or routed to a human with a reason code
    And when the budget hard cap is reached the step is HELD and deterministic steps continue
```

##### US-04-YF24

**As** AI platform owner, **I want** to route each AI step to the cheapest Claude tier whose EVAL suite passes for the workflow, language and data class, escalating at most once, **so that** cost stays inside DEC-008 without quality regression. Traces: AU-152; FR-V12-F-003; TC-V12-F-003.

```gherkin
Feature: US-04-YF24
  Scenario: One escalation then hold
    Given Tier 1a and Tier 1b both pass the suite for SM-SVC-06-WF01 in en
    When a draft is requested
    Then Tier 1a is chosen
    When the Tier 1a draft fails schema validation and the remaining run budget covers a Tier 1b call
    Then exactly one escalation to Tier 1b occurs
    When the Tier 1b draft also fails
    Then the step is HELD for a reviewer and no further model call is made
```

##### US-04-YF25

**As** AI evaluation lead, **I want** to block any AI step whose EVAL suite is missing or below gate for that locale, **so that** only evidenced AI runs in production. Traces: AU-154; FR-V12-F-005; TC-V12-F-005.

```gherkin
Feature: US-04-YF25
  Scenario: Locale-specific block
    Given EVAL-SM-SVC-09-WF02 passes for en and fails the rubric gate for hi
    When an hi enquiry reaches the AI step
    Then the AI step is disabled for hi only and the enquiry goes to the human queue
    And en enquiries continue to use the agent
```

##### US-04-YF26

**As** finance lead, **I want** to see cost per accepted result per workflow and tenant with the rejected outputs in the denominator, **so that** AI spend is judged by accepted output, not by calls. Traces: AU-158; FR-V12-F-050; TC-V12-F-014.

```gherkin
Feature: US-04-YF26
  Scenario: Denominator shown
    Given 100 drafts were produced for SM-SVC-06-WF01 in a month and 80 were accepted
    When the CPAR report is opened in A117
    Then CPAR equals total attributable cost divided by 80
    And the 20 rejected outputs and their cost are shown
    And any unpriced unit is shown in tokens, not rupees
```

##### US-03-YF27

**As** compliance lead (R10), **I want** to have every external effect pass the send preflight decision table with fixed precedence, **so that** no tenant setting can override a jurisdiction hold. Traces: AU-171; FR-V12-F-043; TC-V12-F-098.

```gherkin
Feature: US-03-YF27
  Scenario: Tenant grant cannot override a pack HOLD
    Given the IN pack returns HOLD for a promotional SMS outside 09:00-21:00 recipient time
    And the tenant has an action grant allowing the send
    When the effect adapter requests dispatch
    Then the verdict is HOLD with reason CJ-IN-06
    And effect.preflight_verdict is not ALLOW and no provider call occurs
```

##### US-18-YF28

**As** startup head (R02), **I want** to approve an exact action and have any later change to it rejected, **so that** approvals cannot be reused for a different payload. Traces: AU-175; FR-V12-F-035; TC-V12-F-184.

```gherkin
Feature: US-18-YF28
  Scenario: Stale approval rejected
    Given an approval bound to payload digest D1 and policy version P3
    When the payload changes to digest D2 before execution
    Then execution is rejected with reason approval_stale
    And a new approval is requested
    And no mandate can substitute for an R3 financial or legal approval
```

##### US-04-YF29

**As** tenant administrator, **I want** to have my tenant's AI jobs protected from another tenant's bulk jobs, **so that** interactive latency stays within target. Traces: AU-160; FR-V12-F-016; TC-V12-F-016.

```gherkin
Feature: US-04-YF29
  Scenario: Noisy neighbour
    Given tenant A submits 5,000 batch jobs
    When tenant B makes an interactive request
    Then tenant B's request is scheduled ahead of tenant A's batch jobs
    And tenant B's p95 latency stays within the agent card target
```
