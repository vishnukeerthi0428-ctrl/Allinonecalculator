# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.15), Regulatory Rule Packs: Draft Legal Wording for Counsel Review

| Field | Value |
|---|---|
| Document | Part 11, Batch 11.15b of 11.15a–11.15c. Holds §11.15.8 to §11.15.11: **RP-EU-AI, RP-EU-MKT, RP-US-EMAIL and RP-PLAT-ADS**. The common framework (schema, severity, precedence rule CP-01…07, jurisdiction detection J1–J7, versioning and quarterly review Q-REV, AG-086 contract G-1…G-9) and the verification register VR-01…40 are in Batch 11.15a §11.15.2–§11.15.3 and apply here unchanged |
| Version | 1.0 · 28 Nov 2026 (document). Every rule pack inside is **v0.1-draft** |
| Baseline | As Batch 11.15a; in particular ADR-184 / DEC-507 (EU, UK and US packs remain disabled drafts until counsel approval), DEC-029, BRL-ELG-06, BR-V7-AI-01, CJ-EU-01…10, Part 4.1 §4.12.5–§4.12.9 |
| Roles applied | As Batch 11.15a |

> **DISCLAIMER: DRAFT FOR REVIEW BY QUALIFIED COUNSEL. THIS IS NOT LEGAL ADVICE.** Nothing in this batch may be published, activated or relied on until counsel admitted in the relevant jurisdiction has signed the pack's sign-off block and R10 has approved it in AU-128 (FR-V12-M-028; ADR-184). Until then the EU and US markets stay closed to outbound (fail closed, CP-05). EU-facing and US-facing packs are given in English; the launch languages German and French (BR-V7-AI-07) need certified translations before the EU pack is activated [GAP-996].

---

## 11.15.8 RP-EU-AI: EU AI Act transparency (Article 50) and related AI obligations

### 11.15.8.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-EU-AI |
| Title | EU AI Act transparency for AI interaction and AI-generated content, prohibited manipulative practices, AI literacy, and GDPR Art. 22 for automated decisions |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | EU/EEA (recipients, website visitors or targeted markets in the Union; AI Act Art. 2(1)(c) also reaches providers and deployers outside the Union where the output is used in the Union) |
| Channels | CH, EM, WA, VO, SO, AD, LP, MD, DOC |
| Audiences | ALL |
| Startups | ALL; Tenant |
| Legal sources | Regulation (EU) 2024/1689 (AI Act) Art. 3 (definitions), Art. 4 (AI literacy), Art. 5(1)(a), (b), (f), (g) (prohibited practices), Art. 50(1)–(5), Art. 99(4) (fines) (VR-22, VR-23); Commission guidelines on Art. 50 (20 Jul 2026) and any Code of Practice on marking and labelling (verify); Digital Omnibus on AI (verify citation, VR-22); GDPR Art. 22 and Art. 35 (VR-24); CJ-EU-06, CJ-EU-09; BR-V7-AI-01; FR-V12-A-114; AU-142; DEC-751 |
| Effective dates | Art. 4 and Art. 5 since 2 Feb 2025 (verify); **Art. 50 from 2 Aug 2026** (verified, VR-22); Art. 50(2) marking: systems placed on the market before 2 Aug 2026 have until **2 Dec 2026** (verified, VR-22); this platform's generation features are treated as placed on the market on activation of this pack, so no transition is relied on |
| Owner | R10 Legal/Compliance (with the AI safety and governance lead) |
| Review cadence | Quarterly + event-driven (Commission guidelines, Codes of Practice, AI Office Q&A, harmonised standards) |
| Expiry / fail-closed | 120 days; suspended → EU-market drafts with AI content held (FR-V12-A-114: "undisclosed AI content held in EU markets") |
| Depends on | RP-EU-MKT, RP-PLAT-ADS |

### 11.15.8.2 Plain-language summary

1. Tell people in the EU when they are talking to an AI system (chat, voice, automated replies), at the first interaction, unless it is obvious.
2. AI-generated images, audio, video and text produced by the platform carry a machine-readable mark that a detector can read.
3. Deep fakes (realistic content resembling real people, places or events) carry a visible "AI-generated" disclosure; the platform does not create deep fakes of real people without their written consent.
4. Disclosures are clear, distinguishable, accessible and given no later than first exposure.
5. No manipulative or subliminal techniques, no exploitation of vulnerabilities, no emotion recognition or biometric categorisation of recipients.
6. Staff who approve AI content have AI-literacy training.
7. No solely automated decision with legal or similarly significant effects on a person.

### 11.15.8.3 Definitions

| Term | Definition |
|---|---|
| AI system | A machine-based system as defined in AI Act Art. 3(1) |
| Provider | The entity that develops an AI system or has one developed and places it on the market or puts it into service under its own name (Art. 3(3)); the platform operator for its generation features (counsel to confirm role allocation with the model provider, a GPAI provider) |
| Deployer | The entity using an AI system under its authority (Art. 3(4)); the startup or tenant that publishes content |
| Deep fake | AI-generated or manipulated image, audio or video content that resembles existing persons, objects, places, entities or events and would falsely appear authentic or truthful (Art. 3(60)) |
| Machine-readable marking | Metadata, watermark or equivalent technical solution that allows detection of artificial generation (Art. 50(2)); the platform uses C2PA manifests (AU-142) plus an `X-AI-Generated` content attribute for text where feasible (counsel and the Code of Practice to confirm sufficiency) |
| Interaction | Any exchange in which a natural person communicates directly with an AI system (chatbot, voice bot, automated reply) |

### 11.15.8.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-EU-AI-001 | An AI system that interacts directly with natural persons in the Union shall inform them, in a clear and distinguishable manner and at the latest at the first interaction, that they are interacting with an AI system, unless this is obvious to a reasonably well-informed, observant and circumspect person in the circumstances | AI Act Art. 50(1), 50(5); CJ-EU-09 | CH, VO, WA, EM (AI auto-replies) · ALL | DET | Conversation with `ai_generated_reply = true` and EU jurisdiction → first AI turn contains TPL-EU-AI-01 (text) or TPL-EU-AI-02 (voice) | Block | Conversation transcript of first turn | "Tell the person at the start that they are talking to an AI assistant." |
| RP-EU-AI-002 | Synthetic image, audio, video and text outputs generated by the platform's AI features shall be marked in a machine-readable format and be detectable as artificially generated or manipulated, using technically feasible, effective, interoperable and robust solutions | AI Act Art. 50(2); AU-142; DEC-751 | MD, AD, SO, LP, DOC, EM · ALL | DET | `asset.ai_generated` → C2PA manifest verified (media); `content.ai_generated` attribute in rendered HTML/metadata (text); verification after export | Block | Manifest verification record | "This AI output has no machine-readable AI mark. Re-export through the provenance signer." |
| RP-EU-AI-003 | Image, audio or video content that constitutes a deep fake shall disclose that it has been artificially generated or manipulated, by a visible label for the whole exposure (audio: spoken disclosure at the start) | AI Act Art. 50(4) first subparagraph | MD, AD, SO, LP · ALL | DET+AI | DET: `asset.realistic = true` or `depicts_real_person` or `depicts_real_place_event` → TPL-EU-AI-03 overlay; AI: realism classification of media without flags | Block | Label placement record | "Add the 'AI-generated' label to this realistic content." |
| RP-EU-AI-004 | The platform shall not generate a deep fake of an identifiable real person without that person's prior written consent, and shall never generate one of a public figure, competitor, customer or child | AI Act Art. 50(4); GDPR Art. 6 and Art. 9; RP-IN-ADV-017; DEC-030 | MD · ALL | DET | `depicts_real_person` → `likeness_consent_id`; person ∈ protected list (public figures, minors) → Block | Block | Consent record | "Realistic depictions of real people need their written consent; public figures and children are not permitted." |
| RP-EU-AI-005 | AI-generated or manipulated text published with the purpose of informing the public on matters of public interest shall disclose that it is AI-generated unless it has undergone human review or editorial control and a natural or legal person holds editorial responsibility; on this platform every published AI text is human-approved (L1) and **additionally** labelled under platform policy | AI Act Art. 50(4) second subparagraph; BR-V7-AI-01 | SO, LP, DOC · ALL | DET | `content.ai_generated` and channel public → approval record with named editor AND TPL-EU-AI-04 label | Warn (Block if no approval record) | Approval record | "Record the human editor and add the AI-assisted label." |
| RP-EU-AI-006 | Disclosures under rules 001–005 shall be clear and distinguishable, given at the latest at the time of first interaction or exposure, and conform to applicable accessibility requirements (text alternative, contrast, screen-reader readable) | AI Act Art. 50(5); WCAG 2.2 AA (Part 2.5) | ALL · ALL | DET | Label in first viewport/first frame/first 10 s; `aria-label` or alt text contains disclosure; contrast ≥ 4.5:1 | Block | Rendering metadata | "Place the AI disclosure where people see it first and make it accessible." |
| RP-EU-AI-007 | Disclosures shall be in the language of the content and of the recipient's locale (launch languages English, German, French) | AI Act Art. 50(5); BR-V7-AI-07; FR-V12-A-117 | ALL · ALL | DET | Label locale = content locale; locale ∈ approved label translations | Block | Locale record | "Use the approved AI disclosure in this language." |
| RP-EU-AI-008 | Content and conversational flows shall not deploy subliminal, purposefully manipulative or deceptive techniques that materially distort behaviour by impairing informed decision-making in a manner that causes or is reasonably likely to cause significant harm | AI Act Art. 5(1)(a) | ALL · ALL | AI | AG-086 checks for exploitative pressure, deception about AI nature, fabricated authority, hidden persuasion techniques | Block | — | "Remove manipulative techniques from this content." |
| RP-EU-AI-009 | Content and targeting shall not exploit vulnerabilities due to age, disability or a specific social or economic situation with the object or effect of materially distorting behaviour in a harmful way | AI Act Art. 5(1)(b); BRL-ELG-13/14 | ALL · ALL | DET+AI | DET: audience segments using age < 18, disability, financial-distress attributes → Block; AI: copy targeting distress ("drowning in debt?") | Block | Segment definition | "Do not target or exploit vulnerable groups." |
| RP-EU-AI-010 | No emotion-recognition or biometric-categorisation system shall be applied to recipients, website visitors or call participants | AI Act Art. 5(1)(f)–(g), Art. 50(3) | CH, VO, LP · ALL | DET | Feature flags `emotion_recognition`, `biometric_categorisation` = false for EU tenants and startups | Block | Config snapshot | "Emotion recognition and biometric categorisation are not permitted." |
| RP-EU-AI-011 | Persons who review and approve AI-generated content for EU markets shall have completed AI-literacy training appropriate to their role | AI Act Art. 4 | ALL · ALL | DET | Approver's `ai_literacy_training_date` ≤ 12 months | Warn | Training record | "The approver needs current AI-literacy training." |
| RP-EU-AI-012 | No decision producing legal or similarly significant effects on a natural person (e.g. refusal of a contract, price individualisation, credit terms) shall be taken solely by automated processing; human review is required and the person shall be informed of the right to obtain human intervention | GDPR Art. 22; CJ-EU-06; DEC-064 | ALL · B2C, B2B individuals | DET | Workflow steps tagged `significant_effect` must be L1 with a named approver | Block | Approval record | "This decision needs human review before it affects the person." |
| RP-EU-AI-013 | Synthetic voices used in calls or voice notes shall be disclosed at the start of the call or note | AI Act Art. 50(1) and 50(4); TPL-EU-AI-02 | VO, WA (voice notes) · ALL | DET | `voice.synthetic` → disclosure in first 10 s | Block | Script | "Disclose the AI voice at the start." |
| RP-EU-AI-014 | Undisclosed AI content shall not be dispatched or published to EU markets; where a disclosure or mark is missing the item is held | BR-V7-AI-01; FR-V12-A-114 | ALL · ALL | DET | Aggregate of 001–007 failure → HOLD state | Block | Hold log | "Held: AI disclosure missing for an EU recipient." |
| RP-EU-AI-015 | The AI chat assistant shall hand over to a human on request and shall not claim to be human or deny being an AI when asked | AI Act Art. 50(1); Art. 5(1)(a); RP-IN-WA-012 | CH, VO · ALL | DET+AI | Handoff intent route configured; AI checks replies to "are you a bot?" | Block | Bot config; transcript sample | "The assistant must admit it is AI and offer a person." |
| RP-EU-AI-016 | A DPIA covering AI-assisted personalisation and profiling for EU markets shall be completed before activation | GDPR Art. 35; CJ-EU-06 | ALL · ALL | DET | `dpia.eu_ai_personalisation.status = approved` | Block | DPIA record | "Complete the DPIA before activating AI personalisation in the EU." |
| RP-EU-AI-017 | Marks and labels shall not be removed or degraded in downstream exports, resizing or re-encoding performed by the platform | AI Act Art. 50(2) (robustness) | MD · ALL | DET | Post-export manifest verification passes | Block | Verification log | "The AI mark was lost on export; re-export with the signer." |

### 11.15.8.5 Required disclosures and approved template wording

| Template | Use | English (approved draft wording) | Placement |
|---|---|---|---|
| TPL-EU-AI-01 | Chat assistant first message | "Hello, I am an AI assistant for {Startup}. I can answer questions about {scope}. You can ask for a person at any time by typing 'human'." | First message; persistent "AI assistant" badge next to the name |
| TPL-EU-AI-02 | Voice assistant / synthetic voice | "You are speaking with an automated AI voice assistant on behalf of {Startup}. Say 'person' at any time to speak to a member of our team." | First sentence |
| TPL-EU-AI-03 | Deep-fake / realistic media label | "AI-generated" (image/video overlay); "This content was generated using artificial intelligence." (caption) | Visible for whole exposure; first frame; alt text |
| TPL-EU-AI-04 | AI-assisted text | "This text was drafted with the help of AI and reviewed by {Editor role} at {Startup}." | End of article/post, or byline |
| TPL-EU-AI-05 | Email drafted with AI (platform policy) | "This message was prepared with AI assistance and approved by {Sender name}." | Footer above unsubscribe |
| TPL-EU-AI-06 | Right to human intervention | "You can ask for a person to review any decision about you by contacting {contact}." | Notices for decisions |

### 11.15.8.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-EU-AI-01 | AI-nature denial | "I am a real person"; "I'm human"; "not a bot"; "ich bin ein Mensch"; "je suis une vraie personne" | phrase (multilingual) | Block | 015 |
| PL-EU-AI-02 | Vulnerability exploitation | "drowning in debt"; "desperate"; "lonely?"; "only you can save"; "act now or lose everything" | phrase + AI | Block | 008, 009 |
| PL-EU-AI-03 | Prohibited features | emotion detection; sentiment of caller face; voice stress analysis; biometric categorisation | config key names | Block | 010 |

### 11.15.8.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | AI use is obvious (e.g. a clearly labelled "AI writing assistant" inside the admin app) | Art. 50(1) exception may apply; platform still labels (stricter, CP-03) |
| E-2 | Assistive editing that does not substantially alter input (spelling, formatting) | Art. 50(2) exception for standard editing functions (verify scope); no mark required; platform records `ai_edit_minor` |
| E-3 | Evidently artistic, creative, satirical or fictional work | Art. 50(4) allows limited disclosure; marketing content is not treated as artistic; exception not used |
| E-4 | Text under human editorial responsibility | Art. 50(4) exception; platform labels anyway (rule 005) |
| E-5 | Recipient in UK | UK not under the AI Act; UK pack disabled (ADR-184) |
| E-6 | Role of model provider (GPAI) vs platform | Counsel to confirm provider/deployer allocation and contract terms [GAP-999] |

### 11.15.8.8 AG-086 review prompt guidance (RP-EU-AI)

- **Look for:** AI-generated realistic people, voices or scenes; chat replies that sound human or deny being AI; manipulative urgency, false authority, fear appeals; targeting cues tied to age, disability, financial distress.
- **Cite:** `RP-EU-AI-0NN`, and the Article in `reason`.
- **Escalate:** whether content is a deep fake; whether an exception (E-1 to E-4) applies; any political or public-interest content (not expected; Block under RP-PLAT-ADS-011 too).
- **Never:** decide on marking robustness (deterministic verification only).

### 11.15.8.9 Test cases

| ID | Rule | Type | Input | Expected |
|---|---|---|---|---|
| TC-RP-EU-AI-01 | 001 | Negative | EU web chat, AI replies, no disclosure | Block 001 |
| TC-RP-EU-AI-02 | 001 | Positive | First message TPL-EU-AI-01 | Pass |
| TC-RP-EU-AI-03 | 002 | Negative | AI image exported without C2PA manifest | Block 002 |
| TC-RP-EU-AI-04 | 003 | Negative | Realistic AI video of a "customer" without label | Block 003 (and RP-IN-ADV-018) |
| TC-RP-EU-AI-05 | 004 | Negative | AI likeness of a named competitor CEO | Block 004 |
| TC-RP-EU-AI-06 | 006 | Negative | Label only in the last frame | Block 006 |
| TC-RP-EU-AI-07 | 007 | Negative | German post with English-only label | Block 007 |
| TC-RP-EU-AI-08 | 010 | Negative | Voice-stress analytics enabled for EU calls | Block 010 |
| TC-RP-EU-AI-09 | 015 | Negative | Bot answers "Yes, I'm a real person" | Block 015 |
| TC-RP-EU-AI-10 | 014 | Negative | Email to FR recipient missing TPL-EU-AI-05 | Held |
| TC-RP-EU-AI-11 | 009 | Negative | Segment "users with financial distress score" | Block 009 |

### 11.15.8.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-EU-AI
  title: "EU AI Act transparency for AI interaction and AI-generated content, prohibited manipulative practices, AI literacy, and GDPR Art. 22 for automated decisions"
  version: "0.1-draft"
  state: draft
  jurisdictions: "EU/EEA (recipients, website visitors or targeted markets in the Union; AI Act Art. 2(1)(c) also reaches providers and deployers outside the Union where the output is used in the Union)"
  channels: "CH, EM, WA, VO, SO, AD, LP, MD, DOC"
  audiences: "ALL"
  startups: "ALL; Tenant"
  effective_dates: "Art. 4 and Art. 5 since 2 Feb 2025 (verify); Art. 50 from 2 Aug 2026 (verified, VR-22); Art. 50(2) marking: systems placed on the market before 2 Aug 2026 have until 2 Dec 2026 (verified, VR-22); this platform's generation features are treated as placed on the market on activation of this pack, so no transition is relied on"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
rules:
  - id: RP-EU-AI-001
    obligation: "An AI system that interacts directly with natural persons in the Union shall inform them, in a clear and distinguishable manner and at the latest at the first interaction, that they are interacting with an AI system, unless this is obvious to a reasonably well-informed, observant and circumspect person in the circumstances"
    citation: "AI Act Art. 50(1), 50(5); CJ-EU-09"
    applies_to: "CH, VO, WA, EM (AI auto-replies) · ALL"
    check: "deterministic"
    detection: "Conversation with ai_generated_reply = true and EU jurisdiction → first AI turn contains TPL-EU-AI-01 (text) or TPL-EU-AI-02 (voice)"
    severity: "Block"
    override: none
    evidence: "Conversation transcript of first turn"
    remediation_message: "\"Tell the person at the start that they are talking to an AI assistant.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-002
    obligation: "Synthetic image, audio, video and text outputs generated by the platform's AI features shall be marked in a machine-readable format and be detectable as artificially generated or manipulated, using technically feasible, effective, interoperable and robust solutions"
    citation: "AI Act Art. 50(2); AU-142; DEC-751"
    applies_to: "MD, AD, SO, LP, DOC, EM · ALL"
    check: "deterministic"
    detection: "asset.ai_generated → C2PA manifest verified (media); content.ai_generated attribute in rendered HTML/metadata (text); verification after export"
    severity: "Block"
    override: none
    evidence: "Manifest verification record"
    remediation_message: "\"This AI output has no machine-readable AI mark. Re-export through the provenance signer.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-003
    obligation: "Image, audio or video content that constitutes a deep fake shall disclose that it has been artificially generated or manipulated, by a visible label for the whole exposure (audio: spoken disclosure at the start)"
    citation: "AI Act Art. 50(4) first subparagraph"
    applies_to: "MD, AD, SO, LP · ALL"
    check: "deterministic_then_ai_review"
    detection: "DET: asset.realistic = true or depicts_real_person or depicts_real_place_event → TPL-EU-AI-03 overlay; AI: realism classification of media without flags"
    severity: "Block"
    override: r10_with_reason
    evidence: "Label placement record"
    remediation_message: "\"Add the 'AI-generated' label to this realistic content.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-004
    obligation: "The platform shall not generate a deep fake of an identifiable real person without that person's prior written consent, and shall never generate one of a public figure, competitor, customer or child"
    citation: "AI Act Art. 50(4); GDPR Art. 6 and Art. 9; RP-IN-ADV-017; DEC-030"
    applies_to: "MD · ALL"
    check: "deterministic"
    detection: "depicts_real_person → likeness_consent_id; person ∈ protected list (public figures, minors) → Block"
    severity: "Block"
    override: none
    evidence: "Consent record"
    remediation_message: "\"Realistic depictions of real people need their written consent; public figures and children are not permitted.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-005
    obligation: "AI-generated or manipulated text published with the purpose of informing the public on matters of public interest shall disclose that it is AI-generated unless it has undergone human review or editorial control and a natural or legal person holds editorial responsibility; on this platform every published AI text is human-approved (L1) and additionally labelled under platform policy"
    citation: "AI Act Art. 50(4) second subparagraph; BR-V7-AI-01"
    applies_to: "SO, LP, DOC · ALL"
    check: "deterministic"
    detection: "content.ai_generated and channel public → approval record with named editor AND TPL-EU-AI-04 label"
    severity: "Warn (Block if no approval record)"
    override: none
    evidence: "Approval record"
    remediation_message: "\"Record the human editor and add the AI-assisted label.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-006
    obligation: "Disclosures under rules 001–005 shall be clear and distinguishable, given at the latest at the time of first interaction or exposure, and conform to applicable accessibility requirements (text alternative, contrast, screen-reader readable)"
    citation: "AI Act Art. 50(5); WCAG 2.2 AA (Part 2.5)"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Label in first viewport/first frame/first 10 s; aria-label or alt text contains disclosure; contrast ≥ 4.5:1"
    severity: "Block"
    override: none
    evidence: "Rendering metadata"
    remediation_message: "\"Place the AI disclosure where people see it first and make it accessible.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-007
    obligation: "Disclosures shall be in the language of the content and of the recipient's locale (launch languages English, German, French)"
    citation: "AI Act Art. 50(5); BR-V7-AI-07; FR-V12-A-117"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Label locale = content locale; locale ∈ approved label translations"
    severity: "Block"
    override: none
    evidence: "Locale record"
    remediation_message: "\"Use the approved AI disclosure in this language.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-008
    obligation: "Content and conversational flows shall not deploy subliminal, purposefully manipulative or deceptive techniques that materially distort behaviour by impairing informed decision-making in a manner that causes or is reasonably likely to cause significant harm"
    citation: "AI Act Art. 5(1)(a)"
    applies_to: "ALL · ALL"
    check: "ai_review"
    detection: "AG-086 checks for exploitative pressure, deception about AI nature, fabricated authority, hidden persuasion techniques"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Remove manipulative techniques from this content.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-009
    obligation: "Content and targeting shall not exploit vulnerabilities due to age, disability or a specific social or economic situation with the object or effect of materially distorting behaviour in a harmful way"
    citation: "AI Act Art. 5(1)(b); BRL-ELG-13/14"
    applies_to: "ALL · ALL"
    check: "deterministic_then_ai_review"
    detection: "DET: audience segments using age < 18, disability, financial-distress attributes → Block; AI: copy targeting distress (\"drowning in debt?\")"
    severity: "Block"
    override: r10_with_reason
    evidence: "Segment definition"
    remediation_message: "\"Do not target or exploit vulnerable groups.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-010
    obligation: "No emotion-recognition or biometric-categorisation system shall be applied to recipients, website visitors or call participants"
    citation: "AI Act Art. 5(1)(f)–(g), Art. 50(3)"
    applies_to: "CH, VO, LP · ALL"
    check: "deterministic"
    detection: "Feature flags emotion_recognition, biometric_categorisation = false for EU tenants and startups"
    severity: "Block"
    override: none
    evidence: "Config snapshot"
    remediation_message: "\"Emotion recognition and biometric categorisation are not permitted.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-011
    obligation: "Persons who review and approve AI-generated content for EU markets shall have completed AI-literacy training appropriate to their role"
    citation: "AI Act Art. 4"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Approver's ai_literacy_training_date ≤ 12 months"
    severity: "Warn"
    override: none
    evidence: "Training record"
    remediation_message: "\"The approver needs current AI-literacy training.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-012
    obligation: "No decision producing legal or similarly significant effects on a natural person (e.g. refusal of a contract, price individualisation, credit terms) shall be taken solely by automated processing; human review is required and the person shall be informed of the right to obtain human intervention"
    citation: "GDPR Art. 22; CJ-EU-06; DEC-064"
    applies_to: "ALL · B2C, B2B individuals"
    check: "deterministic"
    detection: "Workflow steps tagged significant_effect must be L1 with a named approver"
    severity: "Block"
    override: none
    evidence: "Approval record"
    remediation_message: "\"This decision needs human review before it affects the person.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-013
    obligation: "Synthetic voices used in calls or voice notes shall be disclosed at the start of the call or note"
    citation: "AI Act Art. 50(1) and 50(4); TPL-EU-AI-02"
    applies_to: "VO, WA (voice notes) · ALL"
    check: "deterministic"
    detection: "voice.synthetic → disclosure in first 10 s"
    severity: "Block"
    override: none
    evidence: "Script"
    remediation_message: "\"Disclose the AI voice at the start.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-014
    obligation: "Undisclosed AI content shall not be dispatched or published to EU markets; where a disclosure or mark is missing the item is held"
    citation: "BR-V7-AI-01; FR-V12-A-114"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Aggregate of 001–007 failure → HOLD state"
    severity: "Block"
    override: none
    evidence: "Hold log"
    remediation_message: "\"Held: AI disclosure missing for an EU recipient.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-015
    obligation: "The AI chat assistant shall hand over to a human on request and shall not claim to be human or deny being an AI when asked"
    citation: "AI Act Art. 50(1); Art. 5(1)(a); RP-IN-WA-012"
    applies_to: "CH, VO · ALL"
    check: "deterministic_then_ai_review"
    detection: "Handoff intent route configured; AI checks replies to \"are you a bot?\""
    severity: "Block"
    override: r10_with_reason
    evidence: "Bot config; transcript sample"
    remediation_message: "\"The assistant must admit it is AI and offer a person.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-016
    obligation: "A DPIA covering AI-assisted personalisation and profiling for EU markets shall be completed before activation"
    citation: "GDPR Art. 35; CJ-EU-06"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "dpia.eu_ai_personalisation.status = approved"
    severity: "Block"
    override: none
    evidence: "DPIA record"
    remediation_message: "\"Complete the DPIA before activating AI personalisation in the EU.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-AI-017
    obligation: "Marks and labels shall not be removed or degraded in downstream exports, resizing or re-encoding performed by the platform"
    citation: "AI Act Art. 50(2) (robustness)"
    applies_to: "MD · ALL"
    check: "deterministic"
    detection: "Post-export manifest verification passes"
    severity: "Block"
    override: none
    evidence: "Verification log"
    remediation_message: "\"The AI mark was lost on export; re-export with the signer.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-EU-AI-01
    name: "AI-nature denial"
    match: "phrase (multilingual)"
    severity: "Block"
    used_by: "015"
    terms:
      - "\"I am a real person\""
      - "\"I'm human\""
      - "\"not a bot\""
      - "\"ich bin ein Mensch\""
      - "\"je suis une vraie personne\""
  - id: PL-EU-AI-02
    name: "Vulnerability exploitation"
    match: "phrase + AI"
    severity: "Block"
    used_by: "008, 009"
    terms:
      - "\"drowning in debt\""
      - "\"desperate\""
      - "\"lonely?\""
      - "\"only you can save\""
      - "\"act now or lose everything\""
  - id: PL-EU-AI-03
    name: "Prohibited features"
    match: "config key names"
    severity: "Block"
    used_by: "010"
    terms:
      - "emotion detection"
      - "sentiment of caller face"
      - "voice stress analysis"
      - "biometric categorisation"
```

### 11.15.8.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-EU-AI v0.1-draft → proposed v1.0 |
| Reviewer (name, bar admission, member state) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Official Journal check of Art. 50 dates and Digital Omnibus citation (VR-22) | ☐ |
| Provider/deployer role allocation opinion (E-6) | _______________________ |
| Sufficiency of C2PA and text marking under Art. 50(2) and the Code of Practice | ☐ Sufficient ☐ Conditions: ______ |
| German and French label translations approved by | _______________________ |
| Conditions | _______________________ |
| Next review due | ____ / ____ / ______ |
| R10 approval / signatures | _______________ / _______________ |

---

## 11.15.9 RP-EU-MKT: EU direct marketing (GDPR, ePrivacy, e-Commerce Directive, UCPD)

### 11.15.9.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-EU-MKT |
| Title | EU/EEA direct electronic marketing: lawful basis, consent and soft opt-in, B2B rules per member state, transparency, right to object, commercial-communication identification and fair commercial practices |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | EU/EEA, with a member-state profile table (§11.15.9.4 rule 018); UK excluded (UK pack disabled, ADR-184) |
| Channels | EM, LP, FM, SO, AD, DOC; WA/SMS/VO only with prior opt-in |
| Audiences | B2B (role-based or professionally published business addresses); B2C only with opt-in |
| Startups | ALL; Tenant |
| Legal sources | GDPR Arts 4(11), 5(1), 6(1)(a) and (f), 7, 9, 12, 13, 14, 21(2)–(4), 27, 30, Chapter V (VR-24); ePrivacy Directive 2002/58/EC Arts 5(3), 13(1), 13(2), 13(4) and national implementations, e.g. Germany UWG §7 (VR-25); e-Commerce Directive 2000/31/EC Art. 6 (VR-26); UCPD 2005/29/EC Arts 6, 7 and Annex I (VR-26); CJEU C-673/17 *Planet49* (pre-ticked boxes); CJ-EU-01…05, 07, 08; BRL-ELG-06; DEC-029; Part 4.1 EU-R1…R11 |
| Effective dates | GDPR since 25 May 2018; ePrivacy national laws in force (verify per member state); a proposed ePrivacy Regulation was withdrawn (verify) |
| Owner | R10 Legal/Compliance (EU counsel) |
| Review cadence | Quarterly + event-driven (EDPB guidelines, CJEU rulings, national DPA guidance on tracking pixels) |
| Expiry / fail-closed | 120 days; member state unknown → strictest profile; EU data region not available → outbound held (CONFLICT-761 in Part 11.1b) |
| Depends on | RP-EU-AI, RP-COMMIT, RP-PLAT-ADS |

### 11.15.9.2 Plain-language summary

1. Record a lawful basis for every purpose; B2B cold email relies on legitimate interests only after a written assessment, and only to role-based or professionally published business addresses.
2. Consumers and, in stricter member states such as Germany, business recipients too, need prior consent for marketing email.
3. Existing customers may receive emails about similar own products (soft opt-in) if they were offered an opt-out when their details were collected and in every message.
4. Every message identifies the sender, offers a free, easy opt-out, and tells the person at the first contact about their right to object and where their data came from.
5. An objection or opt-out stops marketing at once and permanently.
6. No WhatsApp, SMS or calls without prior opt-in; no tracking pixels without consent.
7. Commercial messages must be recognisable as such and must not mislead or omit material information.

### 11.15.9.3 Definitions

| Term | Definition |
|---|---|
| Direct marketing | Communication of advertising or marketing material directed at particular individuals |
| Electronic mail | Any text, voice, sound or image message sent over a public network stored until collected (ePrivacy Art. 2(h)); includes email and SMS |
| Natural-person subscriber | An individual (including, in some member states, sole traders and partnerships) |
| Role-based address | A function address such as `sales@`, `procurement@` not identifying an individual |
| Professionally published address | A business address the person publishes in a professional context (company website, professional profile) |
| Soft opt-in | ePrivacy Art. 13(2): contact details obtained in the context of a sale, used for similar own products, with opt-out at collection and in each message |
| LIA | Legitimate-interest assessment: purpose test, necessity test, balancing test, recorded before reliance on Art. 6(1)(f) |
| Strictest member-state profile | The profile applied when the member state is unknown: B2B and B2C email require prior consent; tracking requires consent |

### 11.15.9.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-EU-MKT-001 | Personal data shall be processed for direct marketing only on a recorded lawful basis per purpose: consent (Art. 6(1)(a)) or legitimate interests (Art. 6(1)(f)) supported by a documented LIA completed before first contact | GDPR Art. 5(2), 6(1); CJ-EU-01; BRL-ELG-06; EU-R2 | ALL outbound · ALL | DET | `lawful_basis` ∈ {consent, legitimate_interest}; if LI → `lia_id` approved before `first_touch_at` | Block | Basis record; LIA | "Record consent or an approved legitimate-interest assessment before contacting this person." |
| RP-EU-MKT-002 | Unsolicited marketing email or SMS to a natural-person subscriber requires prior consent; for business recipients the national rule of the recipient's member state applies (rule 018) | ePrivacy Art. 13(1), 13(5); national laws; CJ-EU-02; EU-R5 | EM, SMS · ALL | DET | Address class: consumer domain (PL-EU-MKT-01) → natural person; member-state profile lookup → consent required? → `consent_id` | Block | Consent or profile record | "This recipient needs prior consent under the rules of their country." |
| RP-EU-MKT-003 | Soft opt-in may be relied on only where the address was obtained from the recipient in the context of a sale of a product or service, the marketing concerns the sender's own similar products or services, and the recipient was given a clear, free and easy opportunity to object at collection and is given one in every message | ePrivacy Art. 13(2) | EM · B2C, B2B | DET | `basis = soft_opt_in` → `sale_id`, `collection_optout_shown = true`, offering category similar (same product family) | Block | Sale and collection record | "Soft opt-in needs a previous sale, similar products and an opt-out shown at collection." |
| RP-EU-MKT-004 | Every marketing message shall contain a clear, free-of-charge and easy means to opt out (one click, no login), and the opt-out shall be effective immediately on the platform | ePrivacy Art. 13(2); GDPR Art. 21(2)–(3); CJ-EU-03; EU-R4 | EM, WA, SMS · ALL | DET | TPL-EU-MKT-01 link present, one-click (RFC 8058 `List-Unsubscribe-Post` header for email), no auth required | Block | Template; header log | "Add a one-click unsubscribe that needs no login." |
| RP-EU-MKT-005 | The identity of the sender on whose behalf the communication is made shall not be disguised or concealed, and a valid address shall be provided to which the recipient may send an opt-out request | ePrivacy Art. 13(4); e-Commerce Directive Art. 6(b) | EM, WA, SMS · ALL | DET | From name = startup legal/brand name; `Reply-To` valid; footer contains legal entity name and postal address | Block | Sender profile | "Show the real sender name and a valid contact address." |
| RP-EU-MKT-006 | At the latest at the first communication, the right to object to direct marketing shall be explicitly brought to the recipient's attention and presented clearly and separately from any other information | GDPR Art. 21(4) | EM, WA · ALL | DET | First-touch template contains TPL-EU-MKT-02 as a separate paragraph | Block | Template | "State the right to object clearly and separately in the first message." |
| RP-EU-MKT-007 | Where personal data were not obtained from the recipient, the information required by Art. 14 (controller identity and contact, DPO contact, purposes and legal basis, legitimate interests pursued, categories of data, recipients, transfers outside the EEA, retention, rights, right to complain to a supervisory authority, source of the data) shall be provided at the latest at the first communication, by a short notice in the message and a link to the full notice | GDPR Art. 14(1)–(3); EU-R3 | EM, WA · ALL | DET | TPL-EU-MKT-03 present with `{source}` resolved; full notice URL returns 200 and contains required sections | Block | Notice version | "Add the short privacy notice with the data source and link to the full notice." |
| RP-EU-MKT-008 | Upon objection or opt-out, direct marketing processing for that purpose shall stop without undue delay and the person shall be added to the suppression list, which shall survive erasure as a hashed token | GDPR Art. 21(3); BRL-ELG-02; BRL-PRV-03 | ALL · ALL | DET | Suppression at dispatch; latency ≤ 60 s | Block | Suppression record | "This person objected to marketing; the message was cancelled." |
| RP-EU-MKT-009 | No WhatsApp, SMS or voice marketing shall be sent to EU/EEA recipients without prior opt-in consent for that channel | BRL-ELG-06; DEC-029; ePrivacy Art. 13(1) | WA, SMS, VO · ALL | DET | EEA E.164 prefix and channel ∈ {WA, SMS, VO} → `consent.channel` = channel | Block | Consent record | "Messaging or calling EU recipients needs their prior opt-in." |
| RP-EU-MKT-010 | Commercial communications shall be clearly identifiable as such, shall identify the person on whose behalf they are made, and promotional offers, competitions and their conditions shall be clearly identifiable, easily accessible and presented clearly | e-Commerce Directive 2000/31/EC Art. 6(a)–(d) | EM, LP, SO · ALL | DET+AI | DET: offer tokens → conditions link present; AI: advertorial framing | Warn (Block for disguised advertorial) | Template | "Make it clear this is a commercial message and show the offer conditions." |
| RP-EU-MKT-011 | Content shall not contain misleading actions or misleading omissions, nor any practice listed in Annex I of the UCPD, including advertorials not identified as paid, bait advertising, false limited-time offers and falsely claiming a code-of-conduct endorsement | UCPD Arts 6, 7 and Annex I (e.g. nos. 1, 5, 7, 11) | ALL · B2C (applied to B2B by platform policy) | AI | AG-086 net-impression review; PL-IN-ADV-03 urgency list applies | Block | — | "This content may mislead or omit material information; revise it." |
| RP-EU-MKT-012 | Consent shall be freely given, specific, informed and unambiguous, given by a clear affirmative action, separate per purpose, never by pre-ticked boxes or silence, demonstrable, and as easy to withdraw as to give | GDPR Arts 4(11), 7(1)–(4); *Planet49* C-673/17; CJ-EU-01 | FM, LP · ALL | DET | Purpose checkboxes unticked; consent record with text version, timestamp, IP | Block | Consent record | "Use separate unticked checkboxes and record the consent." |
| RP-EU-MKT-013 | Special categories of personal data (health, religion, political opinions, sexual orientation, ethnicity, trade union membership, biometrics) shall not be used for targeting, personalisation or segmentation | GDPR Art. 9; BRL-ELG-14 | ALL · ALL | DET | Segment and merge-field schema contains no Art. 9 attribute (PL-EU-MKT-02) | Block | Segment definition | "Sensitive data cannot be used for marketing." |
| RP-EU-MKT-014 | Tracking pixels, link tracking that identifies individuals, and other non-essential storage or access on the recipient's terminal shall be used only with prior consent | ePrivacy Art. 5(3); CJ-EU-08; national DPA guidance (verify) | EM, LP · ALL | DET | EU recipient without `tracking_consent` → open-pixel and personal link tracking disabled | Block | Config log | "Tracking is disabled for this recipient because no consent is recorded." |
| RP-EU-MKT-015 | Recipients located in the United Kingdom shall not receive outbound marketing until the UK pack is active | ADR-184; DEC-507; VR-38 | ALL · ALL | DET | +44 or UK country → Block | Block | — | "UK outreach is not yet enabled." |
| RP-EU-MKT-016 | Where processing involves transfer of EEA personal data outside the EEA, the notice shall say so and an approved transfer mechanism shall be in place | GDPR Chapter V; CJ-EU-07; EU-R9 | ALL · ALL | DET | `transfer_mechanism` recorded for each processor; notice section present | Block | Transfer register | "Record the transfer safeguard and mention it in the notice." |
| RP-EU-MKT-017 | Where the startup is not established in the Union and Art. 3(2) applies, an EU representative shall be designated (or an exemption recorded) before outreach | GDPR Art. 27; EU-R10; GAP-125 | ALL · ALL | DET | `eu_representative` or `art27_exemption_memo` present | Block | Appointment or memo | "Designate an EU representative before contacting EU residents." |
| RP-EU-MKT-018 | The member-state profile of the recipient shall be applied; where the member state is unknown, the strictest profile applies (prior consent for all marketing email, consent for tracking). Profiles (verify each): DE: prior express consent also for B2B email (UWG §7(2), verify no.); AT, IT, FR, ES, NL, IE, others: as configured by EU counsel | ePrivacy Art. 13(5) and national law; CP-03 | EM · B2B | DET | `member_state` → profile table lookup; null → strictest | Block | Profile version | "This country requires prior consent for business email too." |
| RP-EU-MKT-019 | Marketing content shall be in a language the recipient understands; machine translations require approval | BR-V7-AI-07; FR-V12-A-117 | ALL · ALL | DET | `content.locale` ∈ approved locales for EU pack; `translation.approved_by` | Warn | Translation approval | "Use an approved translation for this recipient." |
| RP-EU-MKT-020 | Contact details shall not be obtained by guessing or generating addresses from patterns, nor from sources where the person did not publish them professionally | CJ-GL-01; GDPR Art. 5(1)(a), 14 | EM · B2B | DET | `email.source_type` ∈ {pattern_generated, guessed} → Block | Block | Provenance | "Guessed or pattern-generated addresses cannot be contacted." |

### 11.15.9.5 Required disclosures and approved template wording

| Template | Use | English (approved draft wording) |
|---|---|---|
| TPL-EU-MKT-01 | Unsubscribe | "Unsubscribe: {one_click_link}. One click, no login. We will stop immediately." |
| TPL-EU-MKT-02 | Right to object (first contact, separate paragraph) | "You have the right to object at any time to our use of your data for direct marketing. If you object, we will stop. Reply 'object' or click {link}." |
| TPL-EU-MKT-03 | Art. 14 short notice (first contact) | "Why you are receiving this: we found your business contact details on {source} and we contact professionals in {role/sector} about {topic} on the basis of our legitimate interest in business development (Art. 6(1)(f) GDPR). Controller: {legal entity}, {address}. Contact: {privacy_email}. We keep your data for {period}. Your rights (access, rectification, erasure, restriction, objection, complaint to a supervisory authority) and full details, including transfers outside the EEA: {notice_link}." |
| TPL-EU-MKT-04 | Sender identity footer | "{Legal entity name}, {registered address}, {company registration no.}. Sent on behalf of {Brand}." |
| TPL-EU-MKT-05 | Consent checkbox (unticked) | "☐ I agree that {Startup} may send me emails about {topic}. I can withdraw at any time via the link in each email." |
| TPL-EU-MKT-06 | Soft opt-in collection notice | "We will send you occasional emails about similar {products/services}. ☐ Tick here if you do not want to receive them." (opt-out at collection, per Art. 13(2); counsel to confirm national form) |

### 11.15.9.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-EU-MKT-01 | Consumer email domains (natural persons) | gmail.com; googlemail.com; yahoo.*; hotmail.*; outlook.com; live.*; gmx.de; gmx.net; web.de; t-online.de; orange.fr; free.fr; libero.it; icloud.com; proton.me | domain list | Classifies as natural person (rule 002) | 002 |
| PL-EU-MKT-02 | Art. 9 attributes | health; diagnosis; religion; political; sexual orientation; ethnicity; race; trade union; biometric; genetic | field-name and value match | Block | 013 |
| PL-EU-MKT-03 | Opt-out friction | "log in to unsubscribe"; "reply with your account number"; "allow 30 days"; "unsubscribe fee" | phrase | Block | 004 |

### 11.15.9.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Role-based address (`info@`) | Not personal data in itself in many cases, but treated as personal for safety; ePrivacy B2B rule of member state applies |
| E-2 | Sole trader using a business address | Treated as natural person (consent required) |
| E-3 | Reply to the recipient's own enquiry | Not unsolicited; marketing follow-up beyond the enquiry still needs a basis |
| E-4 | Event attendees who opted in at the event | Consent; record collection proof |
| E-5 | Member state profile missing in config | Strictest profile (rule 018) |
| E-6 | EU SaaS tenant processing its own customers | Tenant is controller; platform processor (DPA with SCCs, EU-R9) |

### 11.15.9.8 AG-086 review prompt guidance (RP-EU-MKT)

- **Look for:** missing or buried Art. 14 information; right to object merged into small print; advertorials; urgency and bait offers; sensitive inferences in personalisation ("as a parent", "given your health").
- **Cite:** `RP-EU-MKT-0NN` with Article in `reason`.
- **Escalate:** soft opt-in similarity judgments; member-state-specific B2B questions; legitimate-interest balancing doubts.
- **Never:** decide the LIA outcome; it is a human record.

### 11.15.9.9 Test cases

| ID | Rule | Type | Input | Expected |
|---|---|---|---|---|
| TC-RP-EU-MKT-01 | 001 | Negative | B2B first touch to FR contact, LI basis without LIA | Block 001 |
| TC-RP-EU-MKT-02 | 002 | Negative | Cold email to `name@gmail.com` in NL | Block 002 |
| TC-RP-EU-MKT-03 | 018 | Negative | Cold B2B email to DE `procurement@firm.de` without consent | Block 018 |
| TC-RP-EU-MKT-04 | 018 | Edge | EU recipient, member state unknown | Strictest profile; Block without consent |
| TC-RP-EU-MKT-05 | 006 | Negative | First touch without right-to-object paragraph | Block 006 |
| TC-RP-EU-MKT-06 | 007 | Negative | First touch without data source | Block 007 |
| TC-RP-EU-MKT-07 | 004 | Negative | Unsubscribe requires login | Block 004 |
| TC-RP-EU-MKT-08 | 009 | Negative | WhatsApp cold message to +33 number | Block 009 |
| TC-RP-EU-MKT-09 | 014 | Negative | Open pixel on email to IT recipient without consent | Pixel disabled; Block if forced |
| TC-RP-EU-MKT-10 | 015 | Negative | +44 recipient | Block 015 |
| TC-RP-EU-MKT-11 | 003 | Positive | Existing customer, similar product, opt-out shown at collection and in email | Pass |

### 11.15.9.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-EU-MKT
  title: "EU/EEA direct electronic marketing: lawful basis, consent and soft opt-in, B2B rules per member state, transparency, right to object, commercial-communication identification and fair commercial practices"
  version: "0.1-draft"
  state: draft
  jurisdictions: "EU/EEA, with a member-state profile table (§11.15.9.4 rule 018); UK excluded (UK pack disabled, ADR-184)"
  channels: "EM, LP, FM, SO, AD, DOC; WA/SMS/VO only with prior opt-in"
  audiences: "B2B (role-based or professionally published business addresses); B2C only with opt-in"
  startups: "ALL; Tenant"
  effective_dates: "GDPR since 25 May 2018; ePrivacy national laws in force (verify per member state); a proposed ePrivacy Regulation was withdrawn (verify)"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
rules:
  - id: RP-EU-MKT-001
    obligation: "Personal data shall be processed for direct marketing only on a recorded lawful basis per purpose: consent (Art. 6(1)(a)) or legitimate interests (Art. 6(1)(f)) supported by a documented LIA completed before first contact"
    citation: "GDPR Art. 5(2), 6(1); CJ-EU-01; BRL-ELG-06; EU-R2"
    applies_to: "ALL outbound · ALL"
    check: "deterministic"
    detection: "lawful_basis ∈ {consent, legitimate_interest}; if LI → lia_id approved before first_touch_at"
    severity: "Block"
    override: none
    evidence: "Basis record; LIA"
    remediation_message: "\"Record consent or an approved legitimate-interest assessment before contacting this person.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-002
    obligation: "Unsolicited marketing email or SMS to a natural-person subscriber requires prior consent; for business recipients the national rule of the recipient's member state applies (rule 018)"
    citation: "ePrivacy Art. 13(1), 13(5); national laws; CJ-EU-02; EU-R5"
    applies_to: "EM, SMS · ALL"
    check: "deterministic"
    detection: "Address class: consumer domain (PL-EU-MKT-01) → natural person; member-state profile lookup → consent required? → consent_id"
    severity: "Block"
    override: none
    evidence: "Consent or profile record"
    remediation_message: "\"This recipient needs prior consent under the rules of their country.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-003
    obligation: "Soft opt-in may be relied on only where the address was obtained from the recipient in the context of a sale of a product or service, the marketing concerns the sender's own similar products or services, and the recipient was given a clear, free and easy opportunity to object at collection and is given one in every message"
    citation: "ePrivacy Art. 13(2)"
    applies_to: "EM · B2C, B2B"
    check: "deterministic"
    detection: "basis = soft_opt_in → sale_id, collection_optout_shown = true, offering category similar (same product family)"
    severity: "Block"
    override: none
    evidence: "Sale and collection record"
    remediation_message: "\"Soft opt-in needs a previous sale, similar products and an opt-out shown at collection.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-004
    obligation: "Every marketing message shall contain a clear, free-of-charge and easy means to opt out (one click, no login), and the opt-out shall be effective immediately on the platform"
    citation: "ePrivacy Art. 13(2); GDPR Art. 21(2)–(3); CJ-EU-03; EU-R4"
    applies_to: "EM, WA, SMS · ALL"
    check: "deterministic"
    detection: "TPL-EU-MKT-01 link present, one-click (RFC 8058 List-Unsubscribe-Post header for email), no auth required"
    severity: "Block"
    override: none
    evidence: "Template; header log"
    remediation_message: "\"Add a one-click unsubscribe that needs no login.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-005
    obligation: "The identity of the sender on whose behalf the communication is made shall not be disguised or concealed, and a valid address shall be provided to which the recipient may send an opt-out request"
    citation: "ePrivacy Art. 13(4); e-Commerce Directive Art. 6(b)"
    applies_to: "EM, WA, SMS · ALL"
    check: "deterministic"
    detection: "From name = startup legal/brand name; Reply-To valid; footer contains legal entity name and postal address"
    severity: "Block"
    override: none
    evidence: "Sender profile"
    remediation_message: "\"Show the real sender name and a valid contact address.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-006
    obligation: "At the latest at the first communication, the right to object to direct marketing shall be explicitly brought to the recipient's attention and presented clearly and separately from any other information"
    citation: "GDPR Art. 21(4)"
    applies_to: "EM, WA · ALL"
    check: "deterministic"
    detection: "First-touch template contains TPL-EU-MKT-02 as a separate paragraph"
    severity: "Block"
    override: none
    evidence: "Template"
    remediation_message: "\"State the right to object clearly and separately in the first message.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-007
    obligation: "Where personal data were not obtained from the recipient, the information required by Art. 14 (controller identity and contact, DPO contact, purposes and legal basis, legitimate interests pursued, categories of data, recipients, transfers outside the EEA, retention, rights, right to complain to a supervisory authority, source of the data) shall be provided at the latest at the first communication, by a short notice in the message and a link to the full notice"
    citation: "GDPR Art. 14(1)–(3); EU-R3"
    applies_to: "EM, WA · ALL"
    check: "deterministic"
    detection: "TPL-EU-MKT-03 present with {source} resolved; full notice URL returns 200 and contains required sections"
    severity: "Block"
    override: none
    evidence: "Notice version"
    remediation_message: "\"Add the short privacy notice with the data source and link to the full notice.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-008
    obligation: "Upon objection or opt-out, direct marketing processing for that purpose shall stop without undue delay and the person shall be added to the suppression list, which shall survive erasure as a hashed token"
    citation: "GDPR Art. 21(3); BRL-ELG-02; BRL-PRV-03"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Suppression at dispatch; latency ≤ 60 s"
    severity: "Block"
    override: none
    evidence: "Suppression record"
    remediation_message: "\"This person objected to marketing; the message was cancelled.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-009
    obligation: "No WhatsApp, SMS or voice marketing shall be sent to EU/EEA recipients without prior opt-in consent for that channel"
    citation: "BRL-ELG-06; DEC-029; ePrivacy Art. 13(1)"
    applies_to: "WA, SMS, VO · ALL"
    check: "deterministic"
    detection: "EEA E.164 prefix and channel ∈ {WA, SMS, VO} → consent.channel = channel"
    severity: "Block"
    override: none
    evidence: "Consent record"
    remediation_message: "\"Messaging or calling EU recipients needs their prior opt-in.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-010
    obligation: "Commercial communications shall be clearly identifiable as such, shall identify the person on whose behalf they are made, and promotional offers, competitions and their conditions shall be clearly identifiable, easily accessible and presented clearly"
    citation: "e-Commerce Directive 2000/31/EC Art. 6(a)–(d)"
    applies_to: "EM, LP, SO · ALL"
    check: "deterministic_then_ai_review"
    detection: "DET: offer tokens → conditions link present; AI: advertorial framing"
    severity: "Warn (Block for disguised advertorial)"
    override: r10_with_reason
    evidence: "Template"
    remediation_message: "\"Make it clear this is a commercial message and show the offer conditions.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-011
    obligation: "Content shall not contain misleading actions or misleading omissions, nor any practice listed in Annex I of the UCPD, including advertorials not identified as paid, bait advertising, false limited-time offers and falsely claiming a code-of-conduct endorsement"
    citation: "UCPD Arts 6, 7 and Annex I (e.g. nos. 1, 5, 7, 11)"
    applies_to: "ALL · B2C (applied to B2B by platform policy)"
    check: "ai_review"
    detection: "AG-086 net-impression review; PL-IN-ADV-03 urgency list applies"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"This content may mislead or omit material information; revise it.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-012
    obligation: "Consent shall be freely given, specific, informed and unambiguous, given by a clear affirmative action, separate per purpose, never by pre-ticked boxes or silence, demonstrable, and as easy to withdraw as to give"
    citation: "GDPR Arts 4(11), 7(1)–(4); *Planet49* C-673/17; CJ-EU-01"
    applies_to: "FM, LP · ALL"
    check: "deterministic"
    detection: "Purpose checkboxes unticked; consent record with text version, timestamp, IP"
    severity: "Block"
    override: none
    evidence: "Consent record"
    remediation_message: "\"Use separate unticked checkboxes and record the consent.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-013
    obligation: "Special categories of personal data (health, religion, political opinions, sexual orientation, ethnicity, trade union membership, biometrics) shall not be used for targeting, personalisation or segmentation"
    citation: "GDPR Art. 9; BRL-ELG-14"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Segment and merge-field schema contains no Art. 9 attribute (PL-EU-MKT-02)"
    severity: "Block"
    override: none
    evidence: "Segment definition"
    remediation_message: "\"Sensitive data cannot be used for marketing.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-014
    obligation: "Tracking pixels, link tracking that identifies individuals, and other non-essential storage or access on the recipient's terminal shall be used only with prior consent"
    citation: "ePrivacy Art. 5(3); CJ-EU-08; national DPA guidance (verify)"
    applies_to: "EM, LP · ALL"
    check: "deterministic"
    detection: "EU recipient without tracking_consent → open-pixel and personal link tracking disabled"
    severity: "Block"
    override: none
    evidence: "Config log"
    remediation_message: "\"Tracking is disabled for this recipient because no consent is recorded.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-015
    obligation: "Recipients located in the United Kingdom shall not receive outbound marketing until the UK pack is active"
    citation: "ADR-184; DEC-507; VR-38"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "+44 or UK country → Block"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"UK outreach is not yet enabled.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-016
    obligation: "Where processing involves transfer of EEA personal data outside the EEA, the notice shall say so and an approved transfer mechanism shall be in place"
    citation: "GDPR Chapter V; CJ-EU-07; EU-R9"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "transfer_mechanism recorded for each processor; notice section present"
    severity: "Block"
    override: none
    evidence: "Transfer register"
    remediation_message: "\"Record the transfer safeguard and mention it in the notice.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-017
    obligation: "Where the startup is not established in the Union and Art. 3(2) applies, an EU representative shall be designated (or an exemption recorded) before outreach"
    citation: "GDPR Art. 27; EU-R10; GAP-125"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "eu_representative or art27_exemption_memo present"
    severity: "Block"
    override: none
    evidence: "Appointment or memo"
    remediation_message: "\"Designate an EU representative before contacting EU residents.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-018
    obligation: "The member-state profile of the recipient shall be applied; where the member state is unknown, the strictest profile applies (prior consent for all marketing email, consent for tracking). Profiles (verify each): DE: prior express consent also for B2B email (UWG §7(2), verify no.); AT, IT, FR, ES, NL, IE, others: as configured by EU counsel"
    citation: "ePrivacy Art. 13(5) and national law; CP-03"
    applies_to: "EM · B2B"
    check: "deterministic"
    detection: "member_state → profile table lookup; null → strictest"
    severity: "Block"
    override: none
    evidence: "Profile version"
    remediation_message: "\"This country requires prior consent for business email too.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-019
    obligation: "Marketing content shall be in a language the recipient understands; machine translations require approval"
    citation: "BR-V7-AI-07; FR-V12-A-117"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "content.locale ∈ approved locales for EU pack; translation.approved_by"
    severity: "Warn"
    override: none
    evidence: "Translation approval"
    remediation_message: "\"Use an approved translation for this recipient.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-MKT-020
    obligation: "Contact details shall not be obtained by guessing or generating addresses from patterns, nor from sources where the person did not publish them professionally"
    citation: "CJ-GL-01; GDPR Art. 5(1)(a), 14"
    applies_to: "EM · B2B"
    check: "deterministic"
    detection: "email.source_type ∈ {pattern_generated, guessed} → Block"
    severity: "Block"
    override: none
    evidence: "Provenance"
    remediation_message: "\"Guessed or pattern-generated addresses cannot be contacted.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-EU-MKT-01
    name: "Consumer email domains (natural persons)"
    match: "domain list"
    severity: "Classifies as natural person (rule 002)"
    used_by: "002"
    terms:
      - "gmail.com"
      - "googlemail.com"
      - "yahoo.*"
      - "hotmail.*"
      - "outlook.com"
      - "live.*"
      - "gmx.de"
      - "gmx.net"
      - "web.de"
      - "t-online.de"
      - "orange.fr"
      - "free.fr"
      - "libero.it"
      - "icloud.com"
      - "proton.me"
  - id: PL-EU-MKT-02
    name: "Art. 9 attributes"
    match: "field-name and value match"
    severity: "Block"
    used_by: "013"
    terms:
      - "health"
      - "diagnosis"
      - "religion"
      - "political"
      - "sexual orientation"
      - "ethnicity"
      - "race"
      - "trade union"
      - "biometric"
      - "genetic"
  - id: PL-EU-MKT-03
    name: "Opt-out friction"
    match: "phrase"
    severity: "Block"
    used_by: "004"
    terms:
      - "\"log in to unsubscribe\""
      - "\"reply with your account number\""
      - "\"allow 30 days\""
      - "\"unsubscribe fee\""
```

### 11.15.9.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-EU-MKT v0.1-draft → proposed v1.0 |
| Reviewer (name, admission, member state) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Member-state profile table approved (list states) | _______________________ |
| Tracking-pixel position confirmed per member state | ☐ |
| Art. 27 representative decision | _______________________ |
| Translations (DE, FR) approved by | _______________________ |
| Conditions | _______________________ |
| Next review due | ____ / ____ / ______ |
| R10 approval / signatures | _______________ / _______________ |

---

## 11.15.10 RP-US-EMAIL: US commercial email (CAN-SPAM), endorsements, reviews and TCPA boundary

### 11.15.10.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-US-EMAIL |
| Title | US commercial electronic mail (CAN-SPAM and 16 CFR Part 316), FTC endorsement and review rules, and the TCPA boundary for texts and calls |
| Version / state | v0.1-draft · `draft` (US pack disabled until counsel approval: ADR-184, CJ-US-01) |
| Jurisdiction(s) | US (recipient in the US, US phone number, or targeted US market) |
| Channels | EM (primary); SMS and VO only as blocks (rule 016); LP, SO, AD for endorsement and review rules |
| Audiences | B2B only at launch (US-R7); B2C blocked |
| Startups | ALL (mainly AppNAI); Tenant |
| Legal sources | CAN-SPAM Act 15 U.S.C. §§7701–7713, esp. §7704(a)(1)–(5), §7704(b) (VR-27); 16 CFR Part 316 (§316.2 definitions, §316.3 primary purpose, §316.4 sexually explicit, §316.5 opt-out restrictions) (VR-27); FTC Act §5 (15 U.S.C. §45); FTC Endorsement Guides 16 CFR Part 255 (2023) (VR-28); Consumer Reviews and Testimonials Rule 16 CFR Part 465 (VR-29); TCPA 47 U.S.C. §227 and 47 CFR §64.1200 (VR-30); ROSCA 15 U.S.C. §8401 et seq. (VR-40); CJ-US-02/03; Part 4.1 US-R1…R7 |
| Effective dates | CAN-SPAM since 1 Jan 2004 (verify); Endorsement Guides revision 26 Jul 2023 (verified, VR-28); Part 465 effective 21 Oct 2024 (verified, VR-29); TCPA consent definition rule 29 Aug 2025; revocation rule waived to 31 Jan 2027 and revised by the FCC Sept 2026 Report and Order (verified, VR-30/VR-67; updated v1.2) |
| Owner | R10 Legal/Compliance (US counsel) |
| Review cadence | Quarterly + event-driven (FTC rules, state laws, FCC orders) |
| Expiry / fail-closed | 120 days; US B2C and US SMS/VO always Block in this version |
| Depends on | RP-COMMIT, RP-PLAT-ADS, RP-EU-AI (platform AI labelling policy) |

### 11.15.10.2 Plain-language summary

1. Use honest headers and subject lines; identify the message as an advertisement; include a valid physical postal address; include a working opt-out.
2. Honour opt-outs immediately on the platform (law: within 10 business days); keep the opt-out working for at least 30 days after sending (platform: 24 months).
3. Do not charge, ask for more than the email address, or require more than one page visit to opt out; never sell opted-out addresses.
4. Do not harvest or guess addresses.
5. Endorsements must reflect honest opinions and disclose material connections; no fake, bought or AI-fabricated reviews or testimonials.
6. No marketing texts or calls to US numbers in this version (TCPA requires prior express written consent; the channel is disabled).

### 11.15.10.3 Definitions

| Term | Definition |
|---|---|
| Commercial electronic mail message | Email whose primary purpose is the commercial advertisement or promotion of a product or service (15 U.S.C. §7702(2); 16 CFR §316.3) |
| Transactional or relationship message | Email whose primary purpose is to facilitate an agreed transaction, give warranty or account information, etc. (§7702(17)) |
| Sender / initiator | The person who initiates the message and whose product is advertised (§7702(9), (16); 16 CFR §316.2) |
| Valid physical postal address | Current street address, a USPS-registered PO box, or a registered private mailbox (16 CFR §316.2) |
| Material connection | Any relationship that might materially affect the weight or credibility of an endorsement (16 CFR §255.0, §255.5) |
| Fake review | A review or testimonial that materially misrepresents that it is by a consumer who does not exist, or who did not have actual experience (16 CFR §465.2, verify wording) |
| Prior express written consent | Signed written agreement authorising telemarketing calls or texts to a number (47 CFR §64.1200(f)) |

### 11.15.10.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-US-EMAIL-001 | Header information (From, Reply-To, routing, originating domain) shall be accurate and identify the person who initiated the message; no false or misleading header information | 15 U.S.C. §7704(a)(1); US-R1 | EM · ALL | DET | From domain ∈ startup verified domains; SPF/DKIM pass; DMARC aligned; From display name = brand | Block | Domain auth log | "Send only from the startup's verified domain with accurate sender name." |
| RP-US-EMAIL-002 | The subject line shall not be likely to mislead a recipient about a material fact regarding the contents or subject matter of the message | §7704(a)(2); US-R2 | EM · ALL | DET+AI | DET: PL-US-EMAIL-01 ("Re:", "Fwd:" without prior thread; "Your invoice", "Account alert" on promotional); AI: subject vs body consistency | Block | Thread ID if Re: | "Make the subject line match the content; do not fake replies or alerts." |
| RP-US-EMAIL-003 | A commercial message shall include a clear and conspicuous identification that it is an advertisement or solicitation, unless the recipient has given prior affirmative consent | §7704(a)(5)(A)(i) | EM · ALL | DET | No `affirmative_consent` → TPL-US-EMAIL-01 present | Block | Consent or template | "Identify this email as an advertisement." |
| RP-US-EMAIL-004 | A commercial message shall include clear and conspicuous notice of the opportunity to decline further commercial messages and a functioning return email address or internet-based mechanism to do so | §7704(a)(3), (a)(5)(A)(ii) | EM · ALL | DET | TPL-US-EMAIL-02 present; unsubscribe URL returns 200 | Block | Link check | "Add a visible, working unsubscribe link." |
| RP-US-EMAIL-005 | A commercial message shall include the sender's valid physical postal address | §7704(a)(5)(A)(iii); 16 CFR §316.2; US-R4 | EM · ALL | DET | Footer contains `postal_address` from verified startup profile (street, PO box registered, or registered PMB) | Block | Address verification | "Add the startup's valid postal address." |
| RP-US-EMAIL-006 | The opt-out mechanism shall remain capable of receiving requests for no less than 30 days after transmission (platform: 24 months) | §7704(a)(3)(A); US-R5 | EM · ALL | DET | Unsubscribe token TTL ≥ 24 months | Block | Token config | "Unsubscribe links must keep working for at least 30 days (platform: 24 months)." |
| RP-US-EMAIL-007 | Opt-out requests shall be honoured within 10 business days (platform: immediately), and no further commercial email shall be sent to that address | §7704(a)(4); US-R5; BRL-ELG-02 | EM · ALL | DET | Suppression check at dispatch | Block | Suppression record | "This address opted out." |
| RP-US-EMAIL-008 | The sender shall not require a fee, information other than the email address and opt-out preferences, or any step other than replying or visiting a single web page, as a condition of honouring an opt-out | 16 CFR §316.5 | EM · ALL | DET | Unsubscribe flow: no login, no fields besides preferences, ≤ 1 page | Block | Flow test | "Make unsubscribe a single page with no login or extra data." |
| RP-US-EMAIL-009 | Opted-out addresses shall not be sold, leased, exchanged or transferred, except to a party helping comply with CAN-SPAM | §7704(a)(4)(A)(iv) | EM · ALL | DET | Export jobs exclude suppression list | Block | Export audit | "Opted-out addresses cannot be shared." |
| RP-US-EMAIL-010 | Addresses shall not be obtained by harvesting, dictionary attacks or pattern generation | §7704(b)(1); CJ-GL-01 | EM · ALL | DET | `email.source_type` ∈ {harvested, pattern_generated} → Block | Block | Provenance | "Harvested or guessed addresses cannot be used." |
| RP-US-EMAIL-011 | The primary purpose of a dual-content message shall be determined under 16 CFR §316.3; where commercial content is the primary purpose (or the subject line and body would lead a recipient to so conclude), all commercial-message requirements apply | 16 CFR §316.3 | EM · ALL | AI | AG-086 classifies primary purpose; dual-purpose → treat as commercial | Warn | — | "This email counts as commercial; add the commercial requirements." |
| RP-US-EMAIL-012 | Sexually explicit content shall not be sent | 16 CFR §316.4; platform policy | EM · ALL | DET | Content classifier flag | Block | — | "This content is not permitted." |
| RP-US-EMAIL-013 | Endorsements and testimonials shall reflect the honest opinions, findings, beliefs or experience of the endorser; material connections shall be clearly and conspicuously disclosed; results claims shall be typical or the generally expected results disclosed | 16 CFR §§255.1, 255.2, 255.5 (2023) (VR-28) | EM, LP, SO, AD · ALL | DET+AI | Endorsement block → `endorsement_record` + disclosure token; AI: atypical results | Block | Endorsement record | "Disclose the endorser's connection and make sure results claims are typical." |
| RP-US-EMAIL-014 | Fake or false consumer reviews or testimonials (including those generated by AI and attributed to people who do not exist or lack actual experience), purchased reviews, insider reviews without disclosure, company-controlled review sites presented as independent, review suppression and fake social-media indicators shall not be created, procured or disseminated | 16 CFR §§465.2–465.8 (VR-29) | ALL · ALL | DET+AI | Testimonial must reference real `consent_record_id`; AI: synthetic reviewer personas, "independent review" framing | Block | Source records | "Use only genuine, consented reviews; never AI-written ones." |
| RP-US-EMAIL-015 | Advertising claims shall be truthful, not misleading and substantiated before dissemination; material terms of any offer (price, recurring charges, cancellation) shall be disclosed clearly and conspicuously | FTC Act §5; ROSCA (VR-40); RP-COMMIT | ALL · ALL | AI | AG-086 net-impression review; RP-COMMIT applies | Block | Claim IDs | "Substantiate the claim and state all material terms." |
| RP-US-EMAIL-016 | No marketing text message or marketing call (including AI or pre-recorded voice) shall be made to a US number in this version; future activation requires prior express written consent, National Do Not Call scrub, calling hours 08:00–21:00 recipient local time, and counsel approval of a US telecom pack | TCPA 47 U.S.C. §227; 47 CFR §64.1200 (VR-30); CJ-US-03 | SMS, VO, WA · ALL | DET | +1 US number and channel ∈ {SMS, VO} → Block | Block | — | "Texts and calls to US numbers are not enabled." |
| RP-US-EMAIL-017 | Outbound to US consumers (B2C) is not enabled; only business contacts at business addresses may be emailed | US-R7; state consumer privacy laws (CPRA and others, verify) | EM · B2C | DET | Address class consumer (PL-EU-MKT-01 domains) or `contact.type = consumer` → Block | Block | Contact class | "Emailing US consumers is not enabled." |
| RP-US-EMAIL-018 | Each startup shall be identified as the sender; when a vendor or the platform sends on a startup's behalf, the startup remains responsible and is named in From and footer | 16 CFR §316.2 (sender); US-R6 | EM · ALL | DET | Footer TPL-US-EMAIL-03 with startup legal name | Block | Sender profile | "Name the startup as the sender." |
| RP-US-EMAIL-019 | Promotional content in a transactional or relationship message shall not be so prominent as to change its primary purpose | 16 CFR §316.3(a)(2)–(3) | EM · ALL | DET+AI | DET: transactional template contains PL-IN-SMS-01 markers above the transactional content → finding | Warn | — | "Keep the transactional content first and promotional content minor." |
| RP-US-EMAIL-020 | The US pack shall not allow any outbound until counsel approval; drafts addressed to the US are held | ADR-184; CJ-US-01 | ALL · ALL | DET | Pack state ≠ active → Block | Block | Pack state | "US outreach is not yet enabled." |

### 11.15.10.5 Required disclosures and approved template wording

| Template | Use | English (approved draft wording) |
|---|---|---|
| TPL-US-EMAIL-01 | Advertisement identification | "This is a commercial message from {Brand}." (top or footer, clear and conspicuous) |
| TPL-US-EMAIL-02 | Opt-out notice | "You can stop receiving marketing emails from {Brand} at any time: unsubscribe here {link} (one click, no login)." |
| TPL-US-EMAIL-03 | Sender identity and postal address | "{Legal entity name}, {street address or registered PO box}, {city}, {state/country}, {postal code}." |
| TPL-US-EMAIL-04 | Material connection | "{Endorser} is a paid partner of {Brand}." / "{Brand} provided {Endorser} with free access to {product}." |
| TPL-US-EMAIL-05 | Results disclosure | "Results vary. Typical customers see {generally expected result} over {period}." (only with substantiation) |
| TPL-US-EMAIL-06 | AI assistance (platform policy) | "Prepared with AI assistance and approved by {Sender name}." |

### 11.15.10.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-US-EMAIL-01 | Deceptive subject patterns | Re:; RE:; Fwd:; FW:; "Your invoice"; "Payment received"; "Account suspended"; "Action required: account"; "Final notice"; "You've won" | prefix and phrase (only when no matching thread or transaction) | Block | 002 |
| PL-US-EMAIL-02 | Review fabrication cues | "as rated by our customers" (no source); "5-star reviews from" (no source); "verified buyer" (no record); "independent review site" (owned) | phrase + AI | Block | 014 |
| PL-US-EMAIL-03 | Opt-out friction | "reply with your password"; "log in to manage preferences" (only route); "allow 10 business days" (platform immediate) | phrase | Block / Warn | 008 |

### 11.15.10.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Transactional/relationship messages | Only header accuracy (001) and subject truthfulness apply under CAN-SPAM; platform keeps footer anyway |
| E-2 | Prior affirmative consent | Advertisement identification (003) may be omitted; all other requirements apply |
| E-3 | Several advertisers in one email | Designate a single "sender" per 16 CFR §316.2 rules; counsel to confirm |
| E-4 | State laws on commercial email (preempted by CAN-SPAM except falsity/deception) | Counsel to confirm any state-specific rules still applicable |
| E-5 | Canada recipients | CASL pack disabled (Part 4.1 CA-R1) → Block |

### 11.15.10.8 AG-086 review prompt guidance (RP-US-EMAIL)

- **Look for:** subject lines that imply a relationship or alert; primary-purpose ambiguity; endorsements without disclosure; atypical results; reviews or quotes without real sources; hidden recurring charges.
- **Cite:** `RP-US-EMAIL-0NN` with the U.S.C. or CFR section in `reason`.
- **Escalate:** primary-purpose determinations; multiple-advertiser emails; anything touching texts or calls.
- **Never:** treat a B2B context as exempt from CAN-SPAM (it is not).

### 11.15.10.9 Test cases

| ID | Rule | Type | Input | Expected |
|---|---|---|---|---|
| TC-RP-US-EMAIL-01 | 001 | Negative | From domain not verified | Block 001 |
| TC-RP-US-EMAIL-02 | 002 | Negative | Subject "Re: our call" with no prior thread | Block 002 |
| TC-RP-US-EMAIL-03 | 005 | Negative | Footer without postal address (Part 11.13b US gap) | Block 005 |
| TC-RP-US-EMAIL-04 | 005 | Positive | Registered PO box in footer | Pass |
| TC-RP-US-EMAIL-05 | 008 | Negative | Unsubscribe requires login | Block 008 |
| TC-RP-US-EMAIL-06 | 014 | Negative | Testimonial from AI persona "Jane D., CTO" | Block 014 |
| TC-RP-US-EMAIL-07 | 016 | Negative | SMS to +1 number | Block 016 |
| TC-RP-US-EMAIL-08 | 017 | Negative | Email to US `@yahoo.com` consumer | Block 017 |
| TC-RP-US-EMAIL-09 | 020 | Negative | Pack in `draft` | Block 020 |
| TC-RP-US-EMAIL-10 | 013 | Negative | Partner quote without connection disclosure | Block 013 |

### 11.15.10.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-US-EMAIL
  title: "US commercial electronic mail (CAN-SPAM and 16 CFR Part 316), FTC endorsement and review rules, and the TCPA boundary for texts and calls"
  version: "0.1-draft"
  state: draft
  jurisdictions: "US (recipient in the US, US phone number, or targeted US market)"
  channels: "EM (primary); SMS and VO only as blocks (rule 016); LP, SO, AD for endorsement and review rules"
  audiences: "B2B only at launch (US-R7); B2C blocked"
  startups: "ALL (mainly AppNAI); Tenant"
  effective_dates: "CAN-SPAM since 1 Jan 2004 (verify); Endorsement Guides revision 26 Jul 2023 (verified, VR-28); Part 465 effective 21 Oct 2024 (verified, VR-29); TCPA consent definition rule 29 Aug 2025; revocation rule waived to 31 Jan 2027 and revised by the FCC Sept 2026 Report and Order (verified, VR-30/VR-67; updated v1.2)"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
rules:
  - id: RP-US-EMAIL-001
    obligation: "Header information (From, Reply-To, routing, originating domain) shall be accurate and identify the person who initiated the message; no false or misleading header information"
    citation: "15 U.S.C. §7704(a)(1); US-R1"
    applies_to: "EM · ALL"
    check: "deterministic"
    detection: "From domain ∈ startup verified domains; SPF/DKIM pass; DMARC aligned; From display name = brand"
    severity: "Block"
    override: none
    evidence: "Domain auth log"
    remediation_message: "\"Send only from the startup's verified domain with accurate sender name.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-002
    obligation: "The subject line shall not be likely to mislead a recipient about a material fact regarding the contents or subject matter of the message"
    citation: "§7704(a)(2); US-R2"
    applies_to: "EM · ALL"
    check: "deterministic_then_ai_review"
    detection: "DET: PL-US-EMAIL-01 (\"Re:\", \"Fwd:\" without prior thread; \"Your invoice\", \"Account alert\" on promotional); AI: subject vs body consistency"
    severity: "Block"
    override: r10_with_reason
    evidence: "Thread ID if Re:"
    remediation_message: "\"Make the subject line match the content; do not fake replies or alerts.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-003
    obligation: "A commercial message shall include a clear and conspicuous identification that it is an advertisement or solicitation, unless the recipient has given prior affirmative consent"
    citation: "§7704(a)(5)(A)(i)"
    applies_to: "EM · ALL"
    check: "deterministic"
    detection: "No affirmative_consent → TPL-US-EMAIL-01 present"
    severity: "Block"
    override: none
    evidence: "Consent or template"
    remediation_message: "\"Identify this email as an advertisement.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-004
    obligation: "A commercial message shall include clear and conspicuous notice of the opportunity to decline further commercial messages and a functioning return email address or internet-based mechanism to do so"
    citation: "§7704(a)(3), (a)(5)(A)(ii)"
    applies_to: "EM · ALL"
    check: "deterministic"
    detection: "TPL-US-EMAIL-02 present; unsubscribe URL returns 200"
    severity: "Block"
    override: none
    evidence: "Link check"
    remediation_message: "\"Add a visible, working unsubscribe link.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-005
    obligation: "A commercial message shall include the sender's valid physical postal address"
    citation: "§7704(a)(5)(A)(iii); 16 CFR §316.2; US-R4"
    applies_to: "EM · ALL"
    check: "deterministic"
    detection: "Footer contains postal_address from verified startup profile (street, PO box registered, or registered PMB)"
    severity: "Block"
    override: none
    evidence: "Address verification"
    remediation_message: "\"Add the startup's valid postal address.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-006
    obligation: "The opt-out mechanism shall remain capable of receiving requests for no less than 30 days after transmission (platform: 24 months)"
    citation: "§7704(a)(3)(A); US-R5"
    applies_to: "EM · ALL"
    check: "deterministic"
    detection: "Unsubscribe token TTL ≥ 24 months"
    severity: "Block"
    override: none
    evidence: "Token config"
    remediation_message: "\"Unsubscribe links must keep working for at least 30 days (platform: 24 months).\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-007
    obligation: "Opt-out requests shall be honoured within 10 business days (platform: immediately), and no further commercial email shall be sent to that address"
    citation: "§7704(a)(4); US-R5; BRL-ELG-02"
    applies_to: "EM · ALL"
    check: "deterministic"
    detection: "Suppression check at dispatch"
    severity: "Block"
    override: none
    evidence: "Suppression record"
    remediation_message: "\"This address opted out.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-008
    obligation: "The sender shall not require a fee, information other than the email address and opt-out preferences, or any step other than replying or visiting a single web page, as a condition of honouring an opt-out"
    citation: "16 CFR §316.5"
    applies_to: "EM · ALL"
    check: "deterministic"
    detection: "Unsubscribe flow: no login, no fields besides preferences, ≤ 1 page"
    severity: "Block"
    override: none
    evidence: "Flow test"
    remediation_message: "\"Make unsubscribe a single page with no login or extra data.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-009
    obligation: "Opted-out addresses shall not be sold, leased, exchanged or transferred, except to a party helping comply with CAN-SPAM"
    citation: "§7704(a)(4)(A)(iv)"
    applies_to: "EM · ALL"
    check: "deterministic"
    detection: "Export jobs exclude suppression list"
    severity: "Block"
    override: none
    evidence: "Export audit"
    remediation_message: "\"Opted-out addresses cannot be shared.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-010
    obligation: "Addresses shall not be obtained by harvesting, dictionary attacks or pattern generation"
    citation: "§7704(b)(1); CJ-GL-01"
    applies_to: "EM · ALL"
    check: "deterministic"
    detection: "email.source_type ∈ {harvested, pattern_generated} → Block"
    severity: "Block"
    override: none
    evidence: "Provenance"
    remediation_message: "\"Harvested or guessed addresses cannot be used.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-011
    obligation: "The primary purpose of a dual-content message shall be determined under 16 CFR §316.3; where commercial content is the primary purpose (or the subject line and body would lead a recipient to so conclude), all commercial-message requirements apply"
    citation: "16 CFR §316.3"
    applies_to: "EM · ALL"
    check: "ai_review"
    detection: "AG-086 classifies primary purpose; dual-purpose → treat as commercial"
    severity: "Warn"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"This email counts as commercial; add the commercial requirements.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-012
    obligation: "Sexually explicit content shall not be sent"
    citation: "16 CFR §316.4; platform policy"
    applies_to: "EM · ALL"
    check: "deterministic"
    detection: "Content classifier flag"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"This content is not permitted.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-013
    obligation: "Endorsements and testimonials shall reflect the honest opinions, findings, beliefs or experience of the endorser; material connections shall be clearly and conspicuously disclosed; results claims shall be typical or the generally expected results disclosed"
    citation: "16 CFR §§255.1, 255.2, 255.5 (2023) (VR-28)"
    applies_to: "EM, LP, SO, AD · ALL"
    check: "deterministic_then_ai_review"
    detection: "Endorsement block → endorsement_record + disclosure token; AI: atypical results"
    severity: "Block"
    override: r10_with_reason
    evidence: "Endorsement record"
    remediation_message: "\"Disclose the endorser's connection and make sure results claims are typical.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-014
    obligation: "Fake or false consumer reviews or testimonials (including those generated by AI and attributed to people who do not exist or lack actual experience), purchased reviews, insider reviews without disclosure, company-controlled review sites presented as independent, review suppression and fake social-media indicators shall not be created, procured or disseminated"
    citation: "16 CFR §§465.2–465.8 (VR-29)"
    applies_to: "ALL · ALL"
    check: "deterministic_then_ai_review"
    detection: "Testimonial must reference real consent_record_id; AI: synthetic reviewer personas, \"independent review\" framing"
    severity: "Block"
    override: r10_with_reason
    evidence: "Source records"
    remediation_message: "\"Use only genuine, consented reviews; never AI-written ones.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-015
    obligation: "Advertising claims shall be truthful, not misleading and substantiated before dissemination; material terms of any offer (price, recurring charges, cancellation) shall be disclosed clearly and conspicuously"
    citation: "FTC Act §5; ROSCA (VR-40); RP-COMMIT"
    applies_to: "ALL · ALL"
    check: "ai_review"
    detection: "AG-086 net-impression review; RP-COMMIT applies"
    severity: "Block"
    override: r10_with_reason
    evidence: "Claim IDs"
    remediation_message: "\"Substantiate the claim and state all material terms.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-016
    obligation: "No marketing text message or marketing call (including AI or pre-recorded voice) shall be made to a US number in this version; future activation requires prior express written consent, National Do Not Call scrub, calling hours 08:00–21:00 recipient local time, and counsel approval of a US telecom pack"
    citation: "TCPA 47 U.S.C. §227; 47 CFR §64.1200 (VR-30); CJ-US-03"
    applies_to: "SMS, VO, WA · ALL"
    check: "deterministic"
    detection: "+1 US number and channel ∈ {SMS, VO} → Block"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"Texts and calls to US numbers are not enabled.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-017
    obligation: "Outbound to US consumers (B2C) is not enabled; only business contacts at business addresses may be emailed"
    citation: "US-R7; state consumer privacy laws (CPRA and others, verify)"
    applies_to: "EM · B2C"
    check: "deterministic"
    detection: "Address class consumer (PL-EU-MKT-01 domains) or contact.type = consumer → Block"
    severity: "Block"
    override: none
    evidence: "Contact class"
    remediation_message: "\"Emailing US consumers is not enabled.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-018
    obligation: "Each startup shall be identified as the sender; when a vendor or the platform sends on a startup's behalf, the startup remains responsible and is named in From and footer"
    citation: "16 CFR §316.2 (sender); US-R6"
    applies_to: "EM · ALL"
    check: "deterministic"
    detection: "Footer TPL-US-EMAIL-03 with startup legal name"
    severity: "Block"
    override: none
    evidence: "Sender profile"
    remediation_message: "\"Name the startup as the sender.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-019
    obligation: "Promotional content in a transactional or relationship message shall not be so prominent as to change its primary purpose"
    citation: "16 CFR §316.3(a)(2)–(3)"
    applies_to: "EM · ALL"
    check: "deterministic_then_ai_review"
    detection: "DET: transactional template contains PL-IN-SMS-01 markers above the transactional content → finding"
    severity: "Warn"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Keep the transactional content first and promotional content minor.\""
    effective_from: null  # set at sign-off
  - id: RP-US-EMAIL-020
    obligation: "The US pack shall not allow any outbound until counsel approval; drafts addressed to the US are held"
    citation: "ADR-184; CJ-US-01"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Pack state ≠ active → Block"
    severity: "Block"
    override: none
    evidence: "Pack state"
    remediation_message: "\"US outreach is not yet enabled.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-US-EMAIL-01
    name: "Deceptive subject patterns"
    match: "prefix and phrase (only when no matching thread or transaction)"
    severity: "Block"
    used_by: "002"
    terms:
      - "Re:"
      - "RE:"
      - "Fwd:"
      - "FW:"
      - "\"Your invoice\""
      - "\"Payment received\""
      - "\"Account suspended\""
      - "\"Action required: account\""
      - "\"Final notice\""
      - "\"You've won\""
  - id: PL-US-EMAIL-02
    name: "Review fabrication cues"
    match: "phrase + AI"
    severity: "Block"
    used_by: "014"
    terms:
      - "\"as rated by our customers\" (no source)"
      - "\"5-star reviews from\" (no source)"
      - "\"verified buyer\" (no record)"
      - "\"independent review site\" (owned)"
  - id: PL-US-EMAIL-03
    name: "Opt-out friction"
    match: "phrase"
    severity: "Block / Warn"
    used_by: "008"
    terms:
      - "\"reply with your password\""
      - "\"log in to manage preferences\" (only route)"
      - "\"allow 10 business days\" (platform immediate)"
```

### 11.15.10.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-US-EMAIL v0.1-draft → proposed v1.0 |
| Reviewer (name, state bar admission) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| CFR and U.S.C. citations confirmed (VR-27…30, 40) | ☐ |
| State-law review (E-4) and B2C position | _______________________ |
| Conditions | _______________________ |
| Next review due | ____ / ____ / ______ |
| R10 approval / signatures | _______________ / _______________ |

---

## 11.15.11 RP-PLAT-ADS: Advertising platform policies (Google Ads, Meta, LinkedIn)

### 11.15.11.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-PLAT-ADS |
| Title | Paid advertising platform policies: restricted categories, personal attributes, sensitive targeting, minors, audience uploads, consent signals, misrepresentation, destinations, branded content and synthetic media |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | All markets where ads run (platform policy), plus the targeted markets' legal packs (CP-01) |
| Channels | AD (search, display, video, social), boosted SO, LP as ad destination |
| Audiences | 18+ only; institutions and businesses; guardians for EduVerse |
| Startups | ALL; Tenant |
| Legal sources | Google Ads policies: Healthcare and medicines; Personalized advertising (sensitive interest categories); Misrepresentation; Editorial; Destination requirements; EU user consent policy (VR-31); Meta Advertising Standards: Personal attributes; Health and wellness; Branded content; Special ad categories; age-targeting restrictions for under-18s; AI disclosure for ads (VR-32); LinkedIn Advertising Policies (VR-33); BRL-MKT-04/05/06; BRL-ELG-14; DEC-030; DEC-038; Part 4.1 AD-R1…R6 |
| Effective dates | Platform policies change continuously; each review records the policy page URL and retrieval date (verify at time of implementation) |
| Owner | R10 Legal/Compliance with the platform-policy specialist and the marketing lead (R05) |
| Review cadence | Quarterly + event-driven (platform policy update or account warning) |
| Expiry / fail-closed | 120 days; AG-086 unavailable → ads Block (AG-086 card: fail closed for ads) |
| Depends on | RP-IN-ADV, RP-HEALTH, RP-EDU-MINORS, RP-EU-AI, RP-EU-MKT, RP-COMMIT |

### 11.15.11.2 Plain-language summary

1. Classify every ad; restricted categories (health, education claims, finance, alcohol, gambling, politics) need certification or are not run.
2. Never say or imply that the viewer has a personal attribute ("Are you diabetic?", "Struggling with debt?").
3. Never target by health, religion, sexual orientation or other sensitive interests; never target under-18s.
4. Upload only consented, hashed contacts to customer lists; pass consent signals for EEA/UK visitors.
5. Ads must not misrepresent the offer; destinations must work, match the ad and show a privacy notice.
6. Boosted creator content uses the platforms' branded-content tools; synthetic realistic people are labelled.
7. Spend only within approved caps.

### 11.15.11.3 Definitions

| Term | Definition |
|---|---|
| Restricted category | A product or service category the platform restricts by certification, geography or audience (verify per platform) |
| Personal attribute assertion | Ad copy that asserts or implies knowledge of the viewer's health, financial status, religion, ethnicity, sexual orientation, disability, criminal record, age or similar (Meta "Personal attributes", verify) |
| Sensitive interest category | Categories excluded from personalised advertising (Google: health, financial hardship, identity and belief, sexual interests, etc., verify) |
| Customer list audience | Hashed contact uploads (Google Customer Match, Meta Custom Audiences, LinkedIn Matched Audiences) |
| Special ad category | Meta categories with restricted targeting: credit/financial products, employment, housing, social issues/elections/politics (verify) |

### 11.15.11.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-PLAT-ADS-001 | Every ad shall be classified by product category before submission; ads in a restricted category shall run only where the advertiser holds the required platform certification for the targeted market, or shall not run | Google Healthcare and medicines and other restricted policies; Meta Advertising Standards (restricted goods); VR-31/32 | AD · ALL | DET | `ad.category` set from offering; category ∈ PL-PLAT-ADS-01 → `certification_id` for platform × market | Block | Certification record | "This category needs platform certification in this market." |
| RP-PLAT-ADS-002 | Ad copy and creative shall not assert or imply personal attributes of the viewer, including health conditions, financial status, religion, ethnicity, sexual orientation, disability, age or criminal record | Meta Advertising Standards (Personal attributes); Google personalized advertising policy | AD · ALL | DET+AI | DET: second-person + attribute regex (PL-PLAT-ADS-02, en and hi); AI: implied attributes in image+text | Block | — | "Do not address the viewer's personal characteristics. Describe the offering instead." |
| RP-PLAT-ADS-003 | Audiences shall not be built on sensitive interest categories or inferred sensitive attributes (health, religion, sexual orientation, financial hardship, etc.) | Google personalized advertising; Meta detailed-targeting restrictions; BRL-MKT-06; BRL-ELG-14; GDPR Art. 9 | AD · ALL | DET | Audience definition keys and interest IDs ∉ sensitive list (PL-PLAT-ADS-03) | Block | Audience snapshot | "Remove sensitive targeting criteria." |
| RP-PLAT-ADS-004 | Ads shall target only persons aged 18 or over; EduVerse ads shall target guardians and institutions; no interest or behavioural targeting associated with children | DEC-030; AD-R2; Meta and Google under-18 restrictions; DPDP s.9(3) | AD · ALL | DET | `age_min ≥ 18`; EduVerse audience types ∈ {guardian, institution} | Block | Audience snapshot | "Ads may target only adults; EduVerse ads target guardians and institutions." |
| RP-PLAT-ADS-005 | Customer-list uploads shall include only contacts with recorded marketing consent for that purpose and platform, hashed as the platform requires, and shall exclude suppressed contacts, minors and any health-related list | AD-R3; platform customer-list terms; DPDP s.6; GDPR Art. 6 | AD · ALL | DET | Upload job filters: consent purpose = `ads_matching`; suppression; age ≥ 18; SHA-256 normalised | Block | Upload manifest | "Only consented, hashed, adult contacts may be uploaded." |
| RP-PLAT-ADS-006 | For EEA and UK visitors, consent signals (e.g. Google Consent Mode v2 parameters) shall be passed and no ad personalisation or measurement shall occur without consent | Google EU user consent policy; ePrivacy Art. 5(3); AD-R4 | AD, LP · EU/UK | DET | Tag config sends consent state; default denied | Block | Tag audit | "Configure consent signals before running ads to EEA/UK visitors." |
| RP-PLAT-ADS-007 | No health events, health page visits, minors' data or sensitive attributes shall be sent to ad pixels or conversion APIs | BRL-MKT-06; CJ-GL-07; AD-R1 | AD, LP · ALL | DET | Pixel event schema denylist; health-related pages have pixels disabled | Block | Tag audit | "Remove ad pixels and events from health-related pages." |
| RP-PLAT-ADS-008 | Ads shall not misrepresent the advertiser, the offering, its price or availability, or omit material information; no clickbait, no sensational or shocking content, no unrealistic promises | Google Misrepresentation; Meta Advertising Standards (deceptive practices) | AD · ALL | AI | AG-086 net-impression review with RP-IN-ADV and RP-COMMIT | Block | Claim IDs | "Make the ad accurate and complete." |
| RP-PLAT-ADS-009 | The destination shall be functional, load on the targeted devices, match the ad's offer, show the advertiser's identity and a privacy notice, and not use dark patterns | Google Destination requirements; Meta landing-page rules; RP-IN-ADV-012…015 | AD, LP · ALL | DET | URL check 200; domain = startup verified; privacy notice link present; offer text on page | Block | Destination check log | "Fix the landing page so it works, matches the ad and shows the privacy notice." |
| RP-PLAT-ADS-010 | Ad text shall meet editorial standards: no excessive or gimmicky capitalisation, repeated punctuation, symbols as words, or unclear phrasing | Google Editorial policy | AD · ALL | DET | Regex: ≥ 2 words fully uppercase (non-acronym), `!!`, emoji in headline (search) | Warn | — | "Use standard capitalisation and punctuation." |
| RP-PLAT-ADS-011 | No political, electoral, social-issue or advocacy ads shall be run by the startups | Meta and Google political ads policies; platform scope | AD · ALL | DET+AI | Category classifier and PL-PLAT-ADS-04 | Block | — | "Political and social-issue ads are not permitted." |
| RP-PLAT-ADS-012 | Where an ad concerns credit, financial products, employment or housing, it shall be declared in the platform's special ad category and use only the permitted targeting | Meta special ad categories; Google financial services verification | AD · ALL | DET | Offering category mapping → special category flag | Block | Declaration | "Declare the special ad category." |
| RP-PLAT-ADS-013 | Healthcare ads shall not promote prescription medicines, unproven or experimental treatments, or medical claims; MedMaarg ads are institutional (B2B) only | Google Healthcare and medicines; Meta Health and wellness; RP-HEALTH | AD · MedMaarg | DET | MedMaarg ad → audience B2B/INST only; RP-HEALTH in applicable set | Block | Audience snapshot | "MedMaarg ads are for institutions only and may not make medical claims." |
| RP-PLAT-ADS-014 | Photorealistic synthetic or digitally altered people, voices or events in ads shall be disclosed through the platform's AI disclosure feature where offered and with a visible label | Meta and Google synthetic-content disclosure requirements (verify scope beyond political ads); BR-V7-AI-01; RP-EU-AI-003; RP-IN-ADV-017 | AD · ALL | DET | `asset.ai_generated and realistic` → platform AI flag set + TPL-IN-ADV-04 / TPL-EU-AI-03 | Block | Submission payload | "Turn on the platform's AI disclosure and add the label." |
| RP-PLAT-ADS-015 | Ads shall be launched only within an approved campaign hash, an approved budget reservation and the daily and monthly spend caps; anomaly > 150% of expected daily spend pauses the campaign | BRL-MKT-04/05; DEC-038; AD-R6 | AD · ALL | DET | Approval hash match; reservation ID; cap counters | Block | Approval and reservation | "Launch needs an approved campaign, budget reservation and spend caps." |
| RP-PLAT-ADS-016 | Boosted or paid promotion of creator or partner content shall use the platform's branded-content tool tagging the brand partner | Meta Branded content policies; ASCI influencer guidelines (VR-06) | AD, SO · ALL | DET | Partner content boosted → `branded_content_tag` present | Block | Submission payload | "Use the branded-content tag when promoting partner content." |
| RP-PLAT-ADS-017 | Competitor trademarks shall not be used in ad text unless permitted by the platform's trademark policy and RP-IN-ADV-004 | Google Trademarks policy; Meta IP policy | AD · ALL | DET+AI | Competitor registry names in ad text | Warn | — | "Remove competitor trademarks from ad text or confirm permitted use." |
| RP-PLAT-ADS-018 | The advertiser account shall be verified (identity and, where required, business operations verification) before ads run | Google advertiser verification; Meta business verification | AD · ALL | DET | `ad_account.verified = true` | Block | Verification record | "Verify the advertiser account first." |
| RP-PLAT-ADS-019 | Education ads shall not promise admissions, results, ranks or jobs and shall follow RP-EDU-MINORS | Google and Meta misleading-claims rules; CCPA Coaching Guidelines 2024 (VR-16); RP-EDU-MINORS-008 | AD · EduVerse | DET+AI | PL-EDU-MINORS-02 match | Block | — | "Remove guarantees of results, ranks or jobs." |
| RP-PLAT-ADS-020 | Ads shall disclose the advertiser identity in line with platform requirements (e.g. "Paid for by" or verified advertiser name), and paid-ad labels applied by the platform shall not be imitated or obscured | Platform transparency rules; RP-IN-ADV-005 | AD · ALL | DET | Advertiser name = startup legal name | Warn | — | "Make sure the advertiser name is the startup's legal or brand name." |

### 11.15.11.5 Required disclosures and approved template wording

| Template | Use | English | Hindi (India-targeted ads) |
|---|---|---|---|
| TPL-PLAT-ADS-01 | Neutral attribute-free hook (replacement pattern) | "Programmes for {organisation type} teams" (instead of "Are you stressed?") | "{organisation type} टीमों के लिए कार्यक्रम" |
| TPL-PLAT-ADS-02 | Synthetic presenter caption | "This presenter is AI-generated." | "यह प्रस्तुतकर्ता AI से बनाया गया है।" |
| TPL-PLAT-ADS-03 | Guardian-targeted EduVerse line | "For parents and guardians: learn about {programme} through your child's school." | "अभिभावकों के लिए: अपने बच्चे के स्कूल के माध्यम से {programme} के बारे में जानें।" |
| TPL-PLAT-ADS-04 | Advertiser identity | "Ad by {Legal entity name}" | "{Legal entity name} द्वारा विज्ञापन" |

### 11.15.11.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-PLAT-ADS-01 | Restricted categories (verify per platform) | healthcare and medicines; online pharmacy; addiction services; clinical trials; financial services; crypto; gambling; alcohol; dating; weight loss; cosmetic procedures; education with outcome claims; government documents | category mapping | Block without certification | 001 |
| PL-PLAT-ADS-02 | Personal-attribute assertions | "are you diabetic"; "your depression"; "struggling with debt"; "bad credit?"; "as a Hindu"; "single and"; "your disability"; "people like you with"; "क्या आप डायबिटीज़ से"; "आपका कर्ज़"; "आपकी बीमारी" | regex: second-person pronoun within 5 tokens of attribute term | Block | 002 |
| PL-PLAT-ADS-03 | Sensitive targeting keys | health conditions; medical; pregnancy; religion; political affiliation; sexual orientation; ethnicity; financial hardship; gambling interest; age < 18 | audience key list | Block | 003 |
| PL-PLAT-ADS-04 | Political and issue terms | election; vote for; party; candidate; protest; referendum; चुनाव; वोट दें | phrase | Block | 011 |

### 11.15.11.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Healthcare institution partnership ad aimed at HR heads | Still health category on some platforms; certification may be required (verify); RP-HEALTH applies |
| E-2 | Job ads for the startups' own hiring | Employment special category; out of marketing scope but rule 012 applies |
| E-3 | Platform's own automated creative (e.g. auto-generated assets) | Treated as AI-generated; must be reviewed before enabling; disable auto-assets for restricted categories |
| E-4 | Lookalike audiences from consented seeds | Allowed only if the seed excludes sensitive and minor data; under-18 exclusion still applies |

### 11.15.11.8 AG-086 review prompt guidance (RP-PLAT-ADS)

- **Look for:** second-person attribute statements (also implied by images, e.g. a person checking blood sugar with "This could be you"); sensational claims; mismatch between ad and destination; political or social-issue themes; synthetic realistic people.
- **Cite:** `RP-PLAT-ADS-0NN` and the platform policy name in `reason`.
- **Escalate:** category classification doubts (health vs wellness); trademark use; certification requirements per country.
- **Never:** approve targeting; it is checked deterministically against the audience snapshot.

### 11.15.11.9 Test cases

| ID | Rule | Type | Input | Expected |
|---|---|---|---|---|
| TC-RP-PLAT-ADS-01 | 002 | Negative | "Struggling with stress at work? Our programme helps" | Block 002 |
| TC-RP-PLAT-ADS-02 | 002 | Positive | "Wellbeing programmes for hospital HR teams" | Pass |
| TC-RP-PLAT-ADS-03 | 003 | Negative | Audience interest "diabetes" | Block 003 |
| TC-RP-PLAT-ADS-04 | 004 | Negative | EduVerse ad age 13–17 | Block 004 |
| TC-RP-PLAT-ADS-05 | 005 | Negative | Customer list including suppressed contacts | Block 005 |
| TC-RP-PLAT-ADS-06 | 006 | Negative | EEA campaign without consent mode | Block 006 |
| TC-RP-PLAT-ADS-07 | 007 | Negative | Pixel on MedMaarg wellness page | Block 007 |
| TC-RP-PLAT-ADS-08 | 009 | Negative | Destination returns 404 | Block 009 |
| TC-RP-PLAT-ADS-09 | 010 | Edge | "BEST DEAL!!!" | Warn 010 (Block via RP-IN-ADV-003) |
| TC-RP-PLAT-ADS-10 | 015 | Negative | Ad launch without approved hash | Block 015 |
| TC-RP-PLAT-ADS-11 | 014 | Negative | Realistic AI spokesperson without platform AI flag | Block 014 |
| TC-RP-PLAT-ADS-12 | 019 | Negative | "100% placement guaranteed" | Block 019 |

### 11.15.11.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-PLAT-ADS
  title: "Paid advertising platform policies: restricted categories, personal attributes, sensitive targeting, minors, audience uploads, consent signals, misrepresentation, destinations, branded content and synthetic media"
  version: "0.1-draft"
  state: draft
  jurisdictions: "All markets where ads run (platform policy), plus the targeted markets' legal packs (CP-01)"
  channels: "AD (search, display, video, social), boosted SO, LP as ad destination"
  audiences: "18+ only; institutions and businesses; guardians for EduVerse"
  startups: "ALL; Tenant"
  effective_dates: "Platform policies change continuously; each review records the policy page URL and retrieval date (verify at time of implementation)"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
rules:
  - id: RP-PLAT-ADS-001
    obligation: "Every ad shall be classified by product category before submission; ads in a restricted category shall run only where the advertiser holds the required platform certification for the targeted market, or shall not run"
    citation: "Google Healthcare and medicines and other restricted policies; Meta Advertising Standards (restricted goods); VR-31/32"
    applies_to: "AD · ALL"
    check: "deterministic"
    detection: "ad.category set from offering; category ∈ PL-PLAT-ADS-01 → certification_id for platform × market"
    severity: "Block"
    override: none
    evidence: "Certification record"
    remediation_message: "\"This category needs platform certification in this market.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-002
    obligation: "Ad copy and creative shall not assert or imply personal attributes of the viewer, including health conditions, financial status, religion, ethnicity, sexual orientation, disability, age or criminal record"
    citation: "Meta Advertising Standards (Personal attributes); Google personalized advertising policy"
    applies_to: "AD · ALL"
    check: "deterministic_then_ai_review"
    detection: "DET: second-person + attribute regex (PL-PLAT-ADS-02, en and hi); AI: implied attributes in image+text"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Do not address the viewer's personal characteristics. Describe the offering instead.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-003
    obligation: "Audiences shall not be built on sensitive interest categories or inferred sensitive attributes (health, religion, sexual orientation, financial hardship, etc.)"
    citation: "Google personalized advertising; Meta detailed-targeting restrictions; BRL-MKT-06; BRL-ELG-14; GDPR Art. 9"
    applies_to: "AD · ALL"
    check: "deterministic"
    detection: "Audience definition keys and interest IDs ∉ sensitive list (PL-PLAT-ADS-03)"
    severity: "Block"
    override: none
    evidence: "Audience snapshot"
    remediation_message: "\"Remove sensitive targeting criteria.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-004
    obligation: "Ads shall target only persons aged 18 or over; EduVerse ads shall target guardians and institutions; no interest or behavioural targeting associated with children"
    citation: "DEC-030; AD-R2; Meta and Google under-18 restrictions; DPDP s.9(3)"
    applies_to: "AD · ALL"
    check: "deterministic"
    detection: "age_min ≥ 18; EduVerse audience types ∈ {guardian, institution}"
    severity: "Block"
    override: none
    evidence: "Audience snapshot"
    remediation_message: "\"Ads may target only adults; EduVerse ads target guardians and institutions.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-005
    obligation: "Customer-list uploads shall include only contacts with recorded marketing consent for that purpose and platform, hashed as the platform requires, and shall exclude suppressed contacts, minors and any health-related list"
    citation: "AD-R3; platform customer-list terms; DPDP s.6; GDPR Art. 6"
    applies_to: "AD · ALL"
    check: "deterministic"
    detection: "Upload job filters: consent purpose = ads_matching; suppression; age ≥ 18; SHA-256 normalised"
    severity: "Block"
    override: none
    evidence: "Upload manifest"
    remediation_message: "\"Only consented, hashed, adult contacts may be uploaded.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-006
    obligation: "For EEA and UK visitors, consent signals (e.g. Google Consent Mode v2 parameters) shall be passed and no ad personalisation or measurement shall occur without consent"
    citation: "Google EU user consent policy; ePrivacy Art. 5(3); AD-R4"
    applies_to: "AD, LP · EU/UK"
    check: "deterministic"
    detection: "Tag config sends consent state; default denied"
    severity: "Block"
    override: none
    evidence: "Tag audit"
    remediation_message: "\"Configure consent signals before running ads to EEA/UK visitors.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-007
    obligation: "No health events, health page visits, minors' data or sensitive attributes shall be sent to ad pixels or conversion APIs"
    citation: "BRL-MKT-06; CJ-GL-07; AD-R1"
    applies_to: "AD, LP · ALL"
    check: "deterministic"
    detection: "Pixel event schema denylist; health-related pages have pixels disabled"
    severity: "Block"
    override: none
    evidence: "Tag audit"
    remediation_message: "\"Remove ad pixels and events from health-related pages.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-008
    obligation: "Ads shall not misrepresent the advertiser, the offering, its price or availability, or omit material information; no clickbait, no sensational or shocking content, no unrealistic promises"
    citation: "Google Misrepresentation; Meta Advertising Standards (deceptive practices)"
    applies_to: "AD · ALL"
    check: "ai_review"
    detection: "AG-086 net-impression review with RP-IN-ADV and RP-COMMIT"
    severity: "Block"
    override: r10_with_reason
    evidence: "Claim IDs"
    remediation_message: "\"Make the ad accurate and complete.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-009
    obligation: "The destination shall be functional, load on the targeted devices, match the ad's offer, show the advertiser's identity and a privacy notice, and not use dark patterns"
    citation: "Google Destination requirements; Meta landing-page rules; RP-IN-ADV-012…015"
    applies_to: "AD, LP · ALL"
    check: "deterministic"
    detection: "URL check 200; domain = startup verified; privacy notice link present; offer text on page"
    severity: "Block"
    override: none
    evidence: "Destination check log"
    remediation_message: "\"Fix the landing page so it works, matches the ad and shows the privacy notice.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-010
    obligation: "Ad text shall meet editorial standards: no excessive or gimmicky capitalisation, repeated punctuation, symbols as words, or unclear phrasing"
    citation: "Google Editorial policy"
    applies_to: "AD · ALL"
    check: "deterministic"
    detection: "Regex: ≥ 2 words fully uppercase (non-acronym), !!, emoji in headline (search)"
    severity: "Warn"
    override: none
    evidence: "—"
    remediation_message: "\"Use standard capitalisation and punctuation.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-011
    obligation: "No political, electoral, social-issue or advocacy ads shall be run by the startups"
    citation: "Meta and Google political ads policies; platform scope"
    applies_to: "AD · ALL"
    check: "deterministic_then_ai_review"
    detection: "Category classifier and PL-PLAT-ADS-04"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Political and social-issue ads are not permitted.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-012
    obligation: "Where an ad concerns credit, financial products, employment or housing, it shall be declared in the platform's special ad category and use only the permitted targeting"
    citation: "Meta special ad categories; Google financial services verification"
    applies_to: "AD · ALL"
    check: "deterministic"
    detection: "Offering category mapping → special category flag"
    severity: "Block"
    override: none
    evidence: "Declaration"
    remediation_message: "\"Declare the special ad category.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-013
    obligation: "Healthcare ads shall not promote prescription medicines, unproven or experimental treatments, or medical claims; MedMaarg ads are institutional (B2B) only"
    citation: "Google Healthcare and medicines; Meta Health and wellness; RP-HEALTH"
    applies_to: "AD · MedMaarg"
    check: "deterministic"
    detection: "MedMaarg ad → audience B2B/INST only; RP-HEALTH in applicable set"
    severity: "Block"
    override: none
    evidence: "Audience snapshot"
    remediation_message: "\"MedMaarg ads are for institutions only and may not make medical claims.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-014
    obligation: "Photorealistic synthetic or digitally altered people, voices or events in ads shall be disclosed through the platform's AI disclosure feature where offered and with a visible label"
    citation: "Meta and Google synthetic-content disclosure requirements (verify scope beyond political ads); BR-V7-AI-01; RP-EU-AI-003; RP-IN-ADV-017"
    applies_to: "AD · ALL"
    check: "deterministic"
    detection: "asset.ai_generated and realistic → platform AI flag set + TPL-IN-ADV-04 / TPL-EU-AI-03"
    severity: "Block"
    override: none
    evidence: "Submission payload"
    remediation_message: "\"Turn on the platform's AI disclosure and add the label.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-015
    obligation: "Ads shall be launched only within an approved campaign hash, an approved budget reservation and the daily and monthly spend caps; anomaly > 150% of expected daily spend pauses the campaign"
    citation: "BRL-MKT-04/05; DEC-038; AD-R6"
    applies_to: "AD · ALL"
    check: "deterministic"
    detection: "Approval hash match; reservation ID; cap counters"
    severity: "Block"
    override: none
    evidence: "Approval and reservation"
    remediation_message: "\"Launch needs an approved campaign, budget reservation and spend caps.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-016
    obligation: "Boosted or paid promotion of creator or partner content shall use the platform's branded-content tool tagging the brand partner"
    citation: "Meta Branded content policies; ASCI influencer guidelines (VR-06)"
    applies_to: "AD, SO · ALL"
    check: "deterministic"
    detection: "Partner content boosted → branded_content_tag present"
    severity: "Block"
    override: none
    evidence: "Submission payload"
    remediation_message: "\"Use the branded-content tag when promoting partner content.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-017
    obligation: "Competitor trademarks shall not be used in ad text unless permitted by the platform's trademark policy and RP-IN-ADV-004"
    citation: "Google Trademarks policy; Meta IP policy"
    applies_to: "AD · ALL"
    check: "deterministic_then_ai_review"
    detection: "Competitor registry names in ad text"
    severity: "Warn"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Remove competitor trademarks from ad text or confirm permitted use.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-018
    obligation: "The advertiser account shall be verified (identity and, where required, business operations verification) before ads run"
    citation: "Google advertiser verification; Meta business verification"
    applies_to: "AD · ALL"
    check: "deterministic"
    detection: "ad_account.verified = true"
    severity: "Block"
    override: none
    evidence: "Verification record"
    remediation_message: "\"Verify the advertiser account first.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-019
    obligation: "Education ads shall not promise admissions, results, ranks or jobs and shall follow RP-EDU-MINORS"
    citation: "Google and Meta misleading-claims rules; CCPA Coaching Guidelines 2024 (VR-16); RP-EDU-MINORS-008"
    applies_to: "AD · EduVerse"
    check: "deterministic_then_ai_review"
    detection: "PL-EDU-MINORS-02 match"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Remove guarantees of results, ranks or jobs.\""
    effective_from: null  # set at sign-off
  - id: RP-PLAT-ADS-020
    obligation: "Ads shall disclose the advertiser identity in line with platform requirements (e.g. \"Paid for by\" or verified advertiser name), and paid-ad labels applied by the platform shall not be imitated or obscured"
    citation: "Platform transparency rules; RP-IN-ADV-005"
    applies_to: "AD · ALL"
    check: "deterministic"
    detection: "Advertiser name = startup legal name"
    severity: "Warn"
    override: none
    evidence: "—"
    remediation_message: "\"Make sure the advertiser name is the startup's legal or brand name.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-PLAT-ADS-01
    name: "Restricted categories (verify per platform)"
    match: "category mapping"
    severity: "Block without certification"
    used_by: "001"
    terms:
      - "healthcare and medicines"
      - "online pharmacy"
      - "addiction services"
      - "clinical trials"
      - "financial services"
      - "crypto"
      - "gambling"
      - "alcohol"
      - "dating"
      - "weight loss"
      - "cosmetic procedures"
      - "education with outcome claims"
      - "government documents"
  - id: PL-PLAT-ADS-02
    name: "Personal-attribute assertions"
    match: "regex: second-person pronoun within 5 tokens of attribute term"
    severity: "Block"
    used_by: "002"
    terms:
      - "\"are you diabetic\""
      - "\"your depression\""
      - "\"struggling with debt\""
      - "\"bad credit?\""
      - "\"as a Hindu\""
      - "\"single and\""
      - "\"your disability\""
      - "\"people like you with\""
      - "\"क्या आप डायबिटीज़ से\""
      - "\"आपका कर्ज़\""
      - "\"आपकी बीमारी\""
  - id: PL-PLAT-ADS-03
    name: "Sensitive targeting keys"
    match: "audience key list"
    severity: "Block"
    used_by: "003"
    terms:
      - "health conditions"
      - "medical"
      - "pregnancy"
      - "religion"
      - "political affiliation"
      - "sexual orientation"
      - "ethnicity"
      - "financial hardship"
      - "gambling interest"
      - "age < 18"
  - id: PL-PLAT-ADS-04
    name: "Political and issue terms"
    match: "phrase"
    severity: "Block"
    used_by: "011"
    terms:
      - "election"
      - "vote for"
      - "party"
      - "candidate"
      - "protest"
      - "referendum"
      - "चुनाव"
      - "वोट दें"
```

### 11.15.11.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-PLAT-ADS v0.1-draft → proposed v1.0 |
| Reviewer (counsel) and platform-policy specialist | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Policy pages checked (URL and retrieval date per platform) | Google: ______ Meta: ______ LinkedIn: ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Certification needs per market confirmed | ☐ |
| Hindi wording reviewed by | _______________________ |
| Conditions | _______________________ |
| Next review due | ____ / ____ / ______ |
| R10 approval / signatures | _______________ / _______________ |

*Continued in Batch 11.15c (§11.15.12 RP-HEALTH onwards).*
