# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.15), Regulatory Rule Packs: Draft Legal Wording for Counsel Review

| Field | Value |
|---|---|
| Document | Part 11, Batch 11.15c of 11.15a–11.15c. Holds §11.15.12 to §11.15.18: **RP-HEALTH, RP-EDU-MINORS and RP-COMMIT**, the pack summary and counsel confirmation list, the effect on GAP-980, decisions DEC-761 to DEC-765, the tags register and the quality gate. The common framework (§11.15.3) and the verification register (§11.15.2) are in Batch 11.15a |
| Version | 1.0 · 28 Nov 2026 (document). Every rule pack inside is **v0.1-draft** |
| Baseline | As Batch 11.15a; in particular the safety invariants "MedMaarg: no therapeutic claims and no patient data" (BRL-ELG-14, BRL-LCY-02, CJ-GL-06/07) and "EduVerse: no outreach to minors" (DEC-030, BRL-ELG-13, CJ-IN-03, BR-V7-CJ-08), DEC-064 autonomy caps, DEC-744 no outcome guarantees |
| Roles applied | As Batch 11.15a; the child-safety and education-sector specialist leads §11.15.13 |

> **DISCLAIMER: DRAFT FOR REVIEW BY QUALIFIED COUNSEL. THIS IS NOT LEGAL ADVICE.** Nothing in this batch may be published, activated or relied on until counsel has signed the pack's sign-off block and R10 has approved it in AU-128 (FR-V12-M-028; ADR-184). The three packs in this batch are **cross-cutting**: they apply in every jurisdiction where their startup or content type is in scope (CP-01), and they encode safety invariants that no exception or override can relax (CP-07).

---

## 11.15.12 RP-HEALTH: MedMaarg institutional wellness (no therapeutic claims, no patient data)

### 11.15.12.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-HEALTH |
| Title | Health and wellness communications: prohibition of therapeutic, cure and medical-outcome claims; objectionable medical advertisements; exclusion of patient and health-condition data; institutional-only audience |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | All (cross-cutting); Indian law sources apply to IN; recipient-market packs add their own rules |
| Channels | ALL (EM, WA, SMS, VO, SO, AD, LP, FM, MD, DOC, CH) |
| Audiences | INST and B2B only (hospital and clinic administrators, HR and wellness heads of employers, insurers, institutional partners); **never** patients or consumers as such |
| Startups | MedMaarg; any startup or tenant offering whose category is health, wellness, fitness, nutrition, insurance-health or medical |
| Legal sources | DMR Act 1954 s.3 (advertisements of drugs for diseases in the Schedule), s.4 (misleading advertisements relating to drugs), s.5 (magic remedies), s.7 (penalties) and Schedule (verify section numbers, VR-14); Drugs and Cosmetics Rules 1945 Rule 106 and Schedule J (VR-15); CPA 2019 s.2(28), s.89 (VR-05); CCPA 2022 Guidelines (VR-04); ASCI Code Ch. I and III and ASCI guidance on health claims (VR-08); NMC RMP Professional Conduct Regulations 2023 (VR-17); DPDP Act 2023 (VR-02); WhatsApp Commerce Policy (VR-20); Google Healthcare and medicines and Meta Health and wellness policies (VR-31/32); BRL-ELG-14; BRL-LCY-02; BRL-MKT-06; CJ-GL-06; CJ-GL-07; DEC-021; DEC-052 |
| Effective dates | DMR Act in force since 1954 (as amended 1963; consolidated text 15 Apr 2026, VR-14); other sources as in their packs |
| Owner | R10 Legal/Compliance (with the MedMaarg startup owner as business reviewer) |
| Review cadence | Quarterly + event-driven (DMR Schedule review; Supreme Court petition outcome, VR-14; AYUSH rule changes, VR-15) |
| Expiry / fail-closed | 120 days; suspended → **all MedMaarg external content held**; AG-086 unavailable → MedMaarg AD/SMS Block, other channels to manual R10 review |
| Depends on | RP-IN-ADV, RP-IN-DPDP, RP-PLAT-ADS, RP-IN-WA, RP-COMMIT |

### 11.15.12.2 Plain-language summary

1. MedMaarg sells institutional wellness partnerships. Its content describes programmes, access and participation; it never says or implies that anything diagnoses, treats, cures, mitigates or prevents a disease or improves a medical condition.
2. Never mention diseases from the DMR Schedule (e.g. diabetes, cancer, heart disease, blood pressure, obesity) in any treatment, prevention or improvement context.
3. No "magic remedy", miracle, detox-cure or immunity-boost claims.
4. No patient data, no health-condition data, no medical history anywhere: not in contact records, forms, audiences, personalisation, AI prompts or ad pixels.
5. Talk only to institutions and businesses; never target individuals because of health.
6. Clinical or urgent questions go to a human at once; the AI never gives medical advice.
7. Management figures (e.g. "750+ users") carry the management-claim label.

### 11.15.12.3 Definitions

| Term | Definition |
|---|---|
| Therapeutic claim | Any statement, express or implied, that a product, service, programme or practice diagnoses, cures, mitigates, treats or prevents a disease, disorder or condition, or modifies a physiological function in a medical sense |
| Wellness process claim | A statement about the programme itself (sessions offered, participation, access, scheduling, employee engagement, satisfaction survey results) that makes no health-outcome promise; permitted with an approved claim |
| Schedule disease | A disease or condition listed in the Schedule to the DMR Act (as amended) or in Schedule J to the Drugs and Cosmetics Rules (VR-14, VR-15) |
| Magic remedy | Any talisman, mantra, kavacha or other charm alleged to have miraculous powers to cure, diagnose, prevent or mitigate disease (DMR Act s.2, verify no.) |
| Patient data | Any data about an identifiable individual's health, condition, diagnosis, treatment, medication, test result, appointment or care relationship |
| Institutional audience | Organisations and their business representatives acting in a professional capacity |
| Clinical enquiry | Any inbound message describing symptoms, seeking diagnosis or treatment, or indicating urgency or risk to life |

### 11.15.12.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-HEALTH-001 | No content shall state, suggest or imply that any product, service, programme or activity offered by or through MedMaarg diagnoses, cures, mitigates, treats or prevents any disease, disorder or condition, or produces any medical or physiological outcome | DMR Act s.3, s.4 (verify no.); CPA s.2(28); CJ-GL-06; MedMaarg invariant | ALL · ALL · MedMaarg and health offerings | DET+AI | DET: PL-HEALTH-01 (cure verbs) and PL-HEALTH-02 (conditions) co-occurring within 12 tokens; AI: implied outcomes in text and images | Block | — | "MedMaarg content cannot claim to cure, treat or prevent any condition. Describe the programme, not health outcomes." |
| RP-HEALTH-002 | No content shall refer to any disease or condition listed in the DMR Act Schedule or Schedule J of the Drugs and Cosmetics Rules in the context of a product or service offered, other than in a factual, non-promotional statement approved by R10 | DMR Act Schedule; D&C Rules r.106 and Sch. J (VR-14, VR-15) | ALL · MedMaarg | DET | PL-HEALTH-02 match anywhere in MedMaarg external content → finding unless span is inside an R10-approved `factual_statement` block | Block | R10 approval for factual block | "Remove references to listed diseases from promotional content." |
| RP-HEALTH-003 | No content shall refer to any talisman, mantra, charm or practice as having powers to cure, diagnose, prevent or mitigate disease, nor use "miracle", "magic" or equivalent in a health context | DMR Act s.5 (verify no.) | ALL · ALL | DET | PL-HEALTH-03 match | Block | — | "Remove miracle or magic-remedy language." |
| RP-HEALTH-004 | No content shall promise or imply improvement in health metrics or outcomes for employees, members or patients (e.g. reduced absenteeism due to illness, lower claims, improved immunity, reduced stress levels, weight loss), unless the statement is a wellness process claim with an approved claim ID and no health-outcome element | CPA s.2(28); CCPA 2022 Guidelines (substantiation); ASCI Code Ch. I; DEC-744 | ALL · MedMaarg | DET+AI | DET: PL-HEALTH-04 outcome verbs; AI: implied outcome; claim must be `type = process` | Block | Process claim ID | "State what the programme provides, not health results." |
| RP-HEALTH-005 | No patient data or health-condition data shall be collected, stored, used for personalisation, segmentation or scoring, included in AI prompts, or sent to any ad pixel or conversion API | BRL-ELG-14; BRL-LCY-02; BRL-MKT-06; CJ-GL-07; DPDP s.6 (necessity); GDPR Art. 9 | ALL · ALL | DET | Field and merge-tag scan against PL-IN-DPDP-01 health items and PL-HEALTH-02; AU-004 redaction; pixel denylist | Block | Schema scan log | "Health or patient data fields are not permitted." |
| RP-HEALTH-006 | MedMaarg outbound and ads shall be addressed only to institutional or business audiences in their professional capacity; no individual shall be selected or targeted because of a health characteristic | DEC-052; BRL-ELG-14; RP-PLAT-ADS-013 | ALL · MedMaarg | DET | Audience types ∈ {INST, B2B}; contact `type ≠ consumer`; ad audience has no health interest | Block | Audience snapshot | "MedMaarg content is for institutions only." |
| RP-HEALTH-007 | Neither content nor AI replies shall give medical advice, diagnosis, dosage, or treatment recommendations; clinical or urgent enquiries shall be routed to a qualified human immediately with the safety response in TPL-HEALTH-03 | CJ-GL-06; BRL-AUT-01 | CH, WA, EM (replies) · ALL | DET+AI | DET: inbound classifier `clinical_enquiry` → route to human, AI reply suppressed; AI: advice-like content in drafts | Block | Routing log | "Medical questions must go to a qualified person. The AI reply was blocked." |
| RP-HEALTH-008 | Management claims about MedMaarg (users, locations, partners) shall carry the management-claim label and an approved claim | DEC-021; BRL-MKT-03; RP-IN-ADV-008 | ALL · MedMaarg | DET | Claim `type = management` → TPL-IN-ADV-05 | Block | Claim record | "Label this figure as a management claim." |
| RP-HEALTH-009 | Content shall not use the name, image or endorsement of a registered medical practitioner, hospital or health authority to promote a commercial offering, except a factual partnership statement approved in writing by that partner and R10 | NMC RMP Regulations 2023 (VR-17); CPA endorsements; RP-IN-ADV-006 | ALL · MedMaarg | DET+AI | Titles "Dr.", "MBBS", "MD", hospital registry names → require `partner_approval_id`; AI: endorsement framing | Block | Partner approval | "Doctors and hospitals cannot be shown endorsing the offering without written approval of a factual statement." |
| RP-HEALTH-010 | No testimonial, case story or quote shall describe an individual's health improvement or condition | CPA s.2(28); DMR Act s.4; RP-HEALTH-001 | ALL · MedMaarg | DET+AI | Testimonial block + PL-HEALTH-02/04 → finding | Block | — | "Testimonials cannot describe health results. Use institutional feedback about the programme." |
| RP-HEALTH-011 | No before-and-after imagery, body imagery suggesting health change, or medical imagery (syringes, pills, scans) implying treatment shall be used | ASCI Code Ch. I; platform health policies | MD, AD, SO, LP · MedMaarg | DET+AI | Image classifier labels `before_after`, `medical_device`, `medication` | Block | — | "Remove imagery that implies treatment or health change." |
| RP-HEALTH-012 | Content shall not present any wellness programme as an alternative or substitute for medical treatment, nor discourage seeking medical care | CPA s.2(28); ASCI Code Ch. III | ALL · MedMaarg | AI | Phrases like "no need for medicines", "instead of a doctor" | Block | — | "Do not suggest the programme replaces medical care." |
| RP-HEALTH-013 | Content shall not make any claim about Ayurvedic, Siddha, Unani, homoeopathic or other traditional medicines or remedies | D&C Rules (AYUSH advertisement rules, VR-15); DMR Act | ALL · MedMaarg | DET | PL-HEALTH-05 match | Block | — | "Traditional-medicine claims are not permitted in MedMaarg content." |
| RP-HEALTH-014 | Every MedMaarg external marketing item shall carry the wellness disclaimer TPL-HEALTH-01 | Platform policy; CCPA 2022 Guidelines (disclaimers, as clarification only) | ALL · MedMaarg | DET | Token TPL-HEALTH-01 present (footer, caption or end card) | Block | Template | "Add the MedMaarg wellness disclaimer." |
| RP-HEALTH-015 | Content addressed to insurers or employers shall not promise reductions in premiums, claims or medical costs | CPA s.2(28); DEC-744; RP-COMMIT-004 | ALL · MedMaarg | DET+AI | PL-HEALTH-04 financial-outcome items ("lower claims", "reduce premiums") | Block | — | "Do not promise cost or claims reductions." |
| RP-HEALTH-016 | Website and partnership forms for health offerings shall not contain fields for health, condition, medication or patient information, and shall show the validation message "Health or patient data fields are not permitted on acquisition forms" if such a field is configured | BRL-LCY-02; Part 2 acceptance text | FM · MedMaarg | DET | Form schema scan | Block | Form schema | "Health or patient data fields are not permitted on acquisition forms." |
| RP-HEALTH-017 | Mental-health and stress content shall use non-stigmatising language, shall not trivialise suicide or self-harm, and shall include crisis-help signposting where self-harm is mentioned | ASCI Code Ch. II and III; platform health policies | ALL · MedMaarg | AI | AG-086 tone and safety review | Warn (Block if self-harm without signposting) | — | "Revise wording to be non-stigmatising and add help-line information if self-harm is mentioned." |
| RP-HEALTH-018 | No WhatsApp or SMS content shall promote medical or healthcare products, and none shall mention a recipient's health | RP-IN-WA-007/008; WhatsApp Commerce Policy | WA, SMS · MedMaarg | DET | Channel + PL-HEALTH-02 → Block | Block | — | "Health products and conditions cannot appear in messaging content." |
| RP-HEALTH-019 | Content shall not reference minors' health, schools' health screenings of children, or paediatric conditions | DEC-030; RP-EDU-MINORS | ALL · MedMaarg | DET | PL-HEALTH-06 (child health terms) | Block | — | "Content about children's health is not permitted." |
| RP-HEALTH-020 | Statistics about health in general (e.g. national prevalence data) shall be cited to an official source, dated, and not linked to any product outcome | ASCI Code Ch. I; BRL-AI-03 | ALL · MedMaarg | DET+AI | Number + PL-HEALTH-02 in a statistic → `source_url`, date; AI: linkage to offering | Warn | Source record | "Cite the official source and date, and do not link it to programme results." |

### 11.15.12.5 Required disclosures and approved template wording

| Template | Use | English | Hindi |
|---|---|---|---|
| TPL-HEALTH-01 | Wellness disclaimer (mandatory) | "MedMaarg wellness programmes support workplace and community wellbeing activities. They are not medical treatment and do not diagnose, treat, cure or prevent any disease. For any health concern, consult a qualified medical practitioner." | "मेडमार्ग वेलनेस कार्यक्रम कार्यस्थल और सामुदायिक कल्याण गतिविधियों में सहायता करते हैं। ये चिकित्सा उपचार नहीं हैं और किसी भी रोग का निदान, उपचार, इलाज या रोकथाम नहीं करते। किसी भी स्वास्थ्य संबंधी चिंता के लिए किसी योग्य चिकित्सक से परामर्श लें।" |
| TPL-HEALTH-02 | Approved process-claim pattern | "The programme offers {n} sessions per month on {topic}, delivered at {location or online}." | "यह कार्यक्रम हर महीने {topic} पर {n} सत्र प्रदान करता है, जो {location या ऑनलाइन} आयोजित होते हैं।" |
| TPL-HEALTH-03 | Clinical-enquiry safety reply (human handoff) | "We can't give medical advice here. If this is an emergency, call 112 or go to the nearest hospital. A member of our team will contact you about programme questions." | "हम यहाँ चिकित्सा सलाह नहीं दे सकते। आपात स्थिति में 112 पर कॉल करें या नज़दीकी अस्पताल जाएँ। कार्यक्रम संबंधी प्रश्नों के लिए हमारी टीम का कोई सदस्य आपसे संपर्क करेगा।" |
| TPL-HEALTH-04 | Partner statement (factual, approved) | "{Institution} partners with MedMaarg to offer wellness activities to its staff." | "{Institution} अपने कर्मचारियों को वेलनेस गतिविधियाँ प्रदान करने के लिए मेडमार्ग के साथ साझेदारी करता है।" |

### 11.15.12.6 Prohibited content and phrase lists

| List | Name | Terms (en; hi) | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-HEALTH-01 | Therapeutic verbs | cure; cures; heal; heals; treat; treatment for; prevent; prevents; reverse; reverses; remedy; therapy for; get rid of; eliminate; fight; boost immunity; detox; रोग मुक्त; इलाज; उपचार; ठीक करे; रोकथाम; जड़ से खत्म; इम्युनिटी बढ़ाए | word/phrase, stemmed, Devanagari normalised | Block with PL-HEALTH-02, else Warn | 001 |
| PL-HEALTH-02 | Conditions (indicative; counsel to align with DMR Schedule and Sch. J) | diabetes; sugar; cancer; tumour; heart disease; hypertension; blood pressure; obesity; arthritis; asthma; depression; anxiety disorder; infertility; impotence; kidney stone; thyroid; cholesterol; stroke; epilepsy; HIV; AIDS; tuberculosis; मधुमेह; शुगर; कैंसर; हृदय रोग; रक्तचाप; बीपी; मोटापा; गठिया; दमा; डिप्रेशन; बांझपन; थायराइड | word | Block (in promotional context) | 001, 002, 010 |
| PL-HEALTH-03 | Magic remedy | miracle; magical; magic cure; talisman; mantra cure; kavach; guaranteed cure; ancient secret; चमत्कारी; जादुई; ताबीज़; कवच; रामबाण | phrase | Block | 003 |
| PL-HEALTH-04 | Outcome promises | reduce sick days; lower medical costs; reduce claims; reduce premiums; lose weight; improve immunity; lower stress levels; clinically proven; doctor recommended; बीमारी की छुट्टियाँ घटाएँ; वज़न घटाएँ; प्रीमियम कम करें | phrase + AI | Block | 004, 015 |
| PL-HEALTH-05 | Traditional-medicine claims | Ayurvedic cure; herbal remedy; Unani; Siddha medicine; homeopathic treatment; आयुर्वेदिक इलाज; जड़ी-बूटी उपचार | phrase | Block | 013 |
| PL-HEALTH-06 | Child health | children's health check; school health screening; paediatric; kids' immunity; बच्चों की सेहत जाँच | phrase | Block | 019 |

### 11.15.12.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Naming a partner hospital in a factual partnership statement | Allowed only via TPL-HEALTH-04 with partner approval (009); no outcome claims |
| E-2 | Generic wellbeing words ("wellbeing", "wellness", "healthy workplace") | Permitted; not therapeutic on their own |
| E-3 | Official public-health statistics in thought-leadership content | Warn (020); no linkage to outcomes; R10 review |
| E-4 | A user volunteers health information inbound | Not stored in CRM fields; routed to human (007); message retained only as needed for the response, then minimised (BRL-LCY-02) |
| E-5 | Other startups mentioning health incidentally (e.g. OrganicSpec "organic food") | RP-HEALTH applies to any health claim ("organic food prevents disease" is Block) |

### 11.15.12.8 AG-086 review prompt guidance (RP-HEALTH)

- **Look for:** any implied health outcome, including through images, metaphors ("recharge your body"), employer-cost promises, testimonials describing feeling better, doctor or hospital framing, traditional remedies, child health; Hindi and code-mixed health terms.
- **Cite:** `RP-HEALTH-0NN`; when a Schedule disease is involved, name it in `reason`.
- **Escalate (`needs_counsel`):** anything borderline between a process claim and an outcome claim; any medical professional reference; any statistic.
- **Never:** suggest a "softer" health-outcome rewrite; rewrites must remove the outcome and use TPL-HEALTH-02 patterns. Never pass MedMaarg content without TPL-HEALTH-01.

### 11.15.12.9 Test cases

| ID | Rule | Type | Input | Expected |
|---|---|---|---|---|
| TC-RP-HEALTH-01 | 001 | Negative | "Our yoga programme helps reverse diabetes" | Block 001, 002 |
| TC-RP-HEALTH-02 | 001 | Negative | Hinglish "Diabetes ko jad se khatam karein" | Block 001 |
| TC-RP-HEALTH-03 | 004 | Negative | "Cut employee sick days by 30%" | Block 004 |
| TC-RP-HEALTH-04 | 004 | Positive | "The programme offers 8 guided sessions per month at your site" + disclaimer | Pass |
| TC-RP-HEALTH-05 | 005 | Negative | Form field "existing conditions" | Block 005 / 016 |
| TC-RP-HEALTH-06 | 006 | Negative | Ad audience "people interested in diabetes" | Block 006 |
| TC-RP-HEALTH-07 | 007 | Negative | Inbound "I have chest pain, what should I take?" answered by AI | AI reply blocked; human route; TPL-HEALTH-03 |
| TC-RP-HEALTH-08 | 009 | Negative | "Recommended by Dr. X, MD" | Block 009 |
| TC-RP-HEALTH-09 | 014 | Negative | MedMaarg email without disclaimer | Block 014 |
| TC-RP-HEALTH-10 | 015 | Negative | "Insurers see 20% fewer claims" | Block 015 |
| TC-RP-HEALTH-11 | 003 | Negative | "Miracle immunity kavach" | Block 003 |
| TC-RP-HEALTH-12 | 008 | Negative | "750+ users" unlabelled | Block 008 |

### 11.15.12.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-HEALTH
  title: "Health and wellness communications: prohibition of therapeutic, cure and medical-outcome claims; objectionable medical advertisements; exclusion of patient and health-condition data; institutional-only audience"
  version: "0.1-draft"
  state: draft
  jurisdictions: "All (cross-cutting); Indian law sources apply to IN; recipient-market packs add their own rules"
  channels: "ALL (EM, WA, SMS, VO, SO, AD, LP, FM, MD, DOC, CH)"
  audiences: "INST and B2B only (hospital and clinic administrators, HR and wellness heads of employers, insurers, institutional partners); never patients or consumers as such"
  startups: "MedMaarg; any startup or tenant offering whose category is health, wellness, fitness, nutrition, insurance-health or medical"
  effective_dates: "DMR Act in force since 1954 (as amended 1963; consolidated text 15 Apr 2026, VR-14); other sources as in their packs"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
rules:
  - id: RP-HEALTH-001
    obligation: "No content shall state, suggest or imply that any product, service, programme or activity offered by or through MedMaarg diagnoses, cures, mitigates, treats or prevents any disease, disorder or condition, or produces any medical or physiological outcome"
    citation: "DMR Act s.3, s.4 (verify no.); CPA s.2(28); CJ-GL-06; MedMaarg invariant"
    applies_to: "ALL · ALL · MedMaarg and health offerings"
    check: "deterministic_then_ai_review"
    detection: "DET: PL-HEALTH-01 (cure verbs) and PL-HEALTH-02 (conditions) co-occurring within 12 tokens; AI: implied outcomes in text and images"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"MedMaarg content cannot claim to cure, treat or prevent any condition. Describe the programme, not health outcomes.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-002
    obligation: "No content shall refer to any disease or condition listed in the DMR Act Schedule or Schedule J of the Drugs and Cosmetics Rules in the context of a product or service offered, other than in a factual, non-promotional statement approved by R10"
    citation: "DMR Act Schedule; D&C Rules r.106 and Sch. J (VR-14, VR-15)"
    applies_to: "ALL · MedMaarg"
    check: "deterministic"
    detection: "PL-HEALTH-02 match anywhere in MedMaarg external content → finding unless span is inside an R10-approved factual_statement block"
    severity: "Block"
    override: none
    evidence: "R10 approval for factual block"
    remediation_message: "\"Remove references to listed diseases from promotional content.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-003
    obligation: "No content shall refer to any talisman, mantra, charm or practice as having powers to cure, diagnose, prevent or mitigate disease, nor use \"miracle\", \"magic\" or equivalent in a health context"
    citation: "DMR Act s.5 (verify no.)"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "PL-HEALTH-03 match"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"Remove miracle or magic-remedy language.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-004
    obligation: "No content shall promise or imply improvement in health metrics or outcomes for employees, members or patients (e.g. reduced absenteeism due to illness, lower claims, improved immunity, reduced stress levels, weight loss), unless the statement is a wellness process claim with an approved claim ID and no health-outcome element"
    citation: "CPA s.2(28); CCPA 2022 Guidelines (substantiation); ASCI Code Ch. I; DEC-744"
    applies_to: "ALL · MedMaarg"
    check: "deterministic_then_ai_review"
    detection: "DET: PL-HEALTH-04 outcome verbs; AI: implied outcome; claim must be type = process"
    severity: "Block"
    override: r10_with_reason
    evidence: "Process claim ID"
    remediation_message: "\"State what the programme provides, not health results.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-005
    obligation: "No patient data or health-condition data shall be collected, stored, used for personalisation, segmentation or scoring, included in AI prompts, or sent to any ad pixel or conversion API"
    citation: "BRL-ELG-14; BRL-LCY-02; BRL-MKT-06; CJ-GL-07; DPDP s.6 (necessity); GDPR Art. 9"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Field and merge-tag scan against PL-IN-DPDP-01 health items and PL-HEALTH-02; AU-004 redaction; pixel denylist"
    severity: "Block"
    override: none
    evidence: "Schema scan log"
    remediation_message: "\"Health or patient data fields are not permitted.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-006
    obligation: "MedMaarg outbound and ads shall be addressed only to institutional or business audiences in their professional capacity; no individual shall be selected or targeted because of a health characteristic"
    citation: "DEC-052; BRL-ELG-14; RP-PLAT-ADS-013"
    applies_to: "ALL · MedMaarg"
    check: "deterministic"
    detection: "Audience types ∈ {INST, B2B}; contact type ≠ consumer; ad audience has no health interest"
    severity: "Block"
    override: none
    evidence: "Audience snapshot"
    remediation_message: "\"MedMaarg content is for institutions only.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-007
    obligation: "Neither content nor AI replies shall give medical advice, diagnosis, dosage, or treatment recommendations; clinical or urgent enquiries shall be routed to a qualified human immediately with the safety response in TPL-HEALTH-03"
    citation: "CJ-GL-06; BRL-AUT-01"
    applies_to: "CH, WA, EM (replies) · ALL"
    check: "deterministic_then_ai_review"
    detection: "DET: inbound classifier clinical_enquiry → route to human, AI reply suppressed; AI: advice-like content in drafts"
    severity: "Block"
    override: r10_with_reason
    evidence: "Routing log"
    remediation_message: "\"Medical questions must go to a qualified person. The AI reply was blocked.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-008
    obligation: "Management claims about MedMaarg (users, locations, partners) shall carry the management-claim label and an approved claim"
    citation: "DEC-021; BRL-MKT-03; RP-IN-ADV-008"
    applies_to: "ALL · MedMaarg"
    check: "deterministic"
    detection: "Claim type = management → TPL-IN-ADV-05"
    severity: "Block"
    override: none
    evidence: "Claim record"
    remediation_message: "\"Label this figure as a management claim.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-009
    obligation: "Content shall not use the name, image or endorsement of a registered medical practitioner, hospital or health authority to promote a commercial offering, except a factual partnership statement approved in writing by that partner and R10"
    citation: "NMC RMP Regulations 2023 (VR-17); CPA endorsements; RP-IN-ADV-006"
    applies_to: "ALL · MedMaarg"
    check: "deterministic_then_ai_review"
    detection: "Titles \"Dr.\", \"MBBS\", \"MD\", hospital registry names → require partner_approval_id; AI: endorsement framing"
    severity: "Block"
    override: r10_with_reason
    evidence: "Partner approval"
    remediation_message: "\"Doctors and hospitals cannot be shown endorsing the offering without written approval of a factual statement.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-010
    obligation: "No testimonial, case story or quote shall describe an individual's health improvement or condition"
    citation: "CPA s.2(28); DMR Act s.4; RP-HEALTH-001"
    applies_to: "ALL · MedMaarg"
    check: "deterministic_then_ai_review"
    detection: "Testimonial block + PL-HEALTH-02/04 → finding"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Testimonials cannot describe health results. Use institutional feedback about the programme.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-011
    obligation: "No before-and-after imagery, body imagery suggesting health change, or medical imagery (syringes, pills, scans) implying treatment shall be used"
    citation: "ASCI Code Ch. I; platform health policies"
    applies_to: "MD, AD, SO, LP · MedMaarg"
    check: "deterministic_then_ai_review"
    detection: "Image classifier labels before_after, medical_device, medication"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Remove imagery that implies treatment or health change.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-012
    obligation: "Content shall not present any wellness programme as an alternative or substitute for medical treatment, nor discourage seeking medical care"
    citation: "CPA s.2(28); ASCI Code Ch. III"
    applies_to: "ALL · MedMaarg"
    check: "ai_review"
    detection: "Phrases like \"no need for medicines\", \"instead of a doctor\""
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Do not suggest the programme replaces medical care.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-013
    obligation: "Content shall not make any claim about Ayurvedic, Siddha, Unani, homoeopathic or other traditional medicines or remedies"
    citation: "D&C Rules (AYUSH advertisement rules, VR-15); DMR Act"
    applies_to: "ALL · MedMaarg"
    check: "deterministic"
    detection: "PL-HEALTH-05 match"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"Traditional-medicine claims are not permitted in MedMaarg content.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-014
    obligation: "Every MedMaarg external marketing item shall carry the wellness disclaimer TPL-HEALTH-01"
    citation: "Platform policy; CCPA 2022 Guidelines (disclaimers, as clarification only)"
    applies_to: "ALL · MedMaarg"
    check: "deterministic"
    detection: "Token TPL-HEALTH-01 present (footer, caption or end card)"
    severity: "Block"
    override: none
    evidence: "Template"
    remediation_message: "\"Add the MedMaarg wellness disclaimer.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-015
    obligation: "Content addressed to insurers or employers shall not promise reductions in premiums, claims or medical costs"
    citation: "CPA s.2(28); DEC-744; RP-COMMIT-004"
    applies_to: "ALL · MedMaarg"
    check: "deterministic_then_ai_review"
    detection: "PL-HEALTH-04 financial-outcome items (\"lower claims\", \"reduce premiums\")"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Do not promise cost or claims reductions.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-016
    obligation: "Website and partnership forms for health offerings shall not contain fields for health, condition, medication or patient information, and shall show the validation message \"Health or patient data fields are not permitted on acquisition forms\" if such a field is configured"
    citation: "BRL-LCY-02; Part 2 acceptance text"
    applies_to: "FM · MedMaarg"
    check: "deterministic"
    detection: "Form schema scan"
    severity: "Block"
    override: none
    evidence: "Form schema"
    remediation_message: "\"Health or patient data fields are not permitted on acquisition forms.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-017
    obligation: "Mental-health and stress content shall use non-stigmatising language, shall not trivialise suicide or self-harm, and shall include crisis-help signposting where self-harm is mentioned"
    citation: "ASCI Code Ch. II and III; platform health policies"
    applies_to: "ALL · MedMaarg"
    check: "ai_review"
    detection: "AG-086 tone and safety review"
    severity: "Warn (Block if self-harm without signposting)"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Revise wording to be non-stigmatising and add help-line information if self-harm is mentioned.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-018
    obligation: "No WhatsApp or SMS content shall promote medical or healthcare products, and none shall mention a recipient's health"
    citation: "RP-IN-WA-007/008; WhatsApp Commerce Policy"
    applies_to: "WA, SMS · MedMaarg"
    check: "deterministic"
    detection: "Channel + PL-HEALTH-02 → Block"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"Health products and conditions cannot appear in messaging content.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-019
    obligation: "Content shall not reference minors' health, schools' health screenings of children, or paediatric conditions"
    citation: "DEC-030; RP-EDU-MINORS"
    applies_to: "ALL · MedMaarg"
    check: "deterministic"
    detection: "PL-HEALTH-06 (child health terms)"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"Content about children's health is not permitted.\""
    effective_from: null  # set at sign-off
  - id: RP-HEALTH-020
    obligation: "Statistics about health in general (e.g. national prevalence data) shall be cited to an official source, dated, and not linked to any product outcome"
    citation: "ASCI Code Ch. I; BRL-AI-03"
    applies_to: "ALL · MedMaarg"
    check: "deterministic_then_ai_review"
    detection: "Number + PL-HEALTH-02 in a statistic → source_url, date; AI: linkage to offering"
    severity: "Warn"
    override: r10_with_reason
    evidence: "Source record"
    remediation_message: "\"Cite the official source and date, and do not link it to programme results.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-HEALTH-01
    name: "Therapeutic verbs"
    match: "word/phrase, stemmed, Devanagari normalised"
    severity: "Block with PL-HEALTH-02, else Warn"
    used_by: "001"
    terms:
      - "cure"
      - "cures"
      - "heal"
      - "heals"
      - "treat"
      - "treatment for"
      - "prevent"
      - "prevents"
      - "reverse"
      - "reverses"
      - "remedy"
      - "therapy for"
      - "get rid of"
      - "eliminate"
      - "fight"
      - "boost immunity"
      - "detox"
      - "रोग मुक्त"
      - "इलाज"
      - "उपचार"
      - "ठीक करे"
      - "रोकथाम"
      - "जड़ से खत्म"
      - "इम्युनिटी बढ़ाए"
  - id: PL-HEALTH-02
    name: "Conditions (indicative; counsel to align with DMR Schedule and Sch. J)"
    match: "word"
    severity: "Block (in promotional context)"
    used_by: "001, 002, 010"
    terms:
      - "diabetes"
      - "sugar"
      - "cancer"
      - "tumour"
      - "heart disease"
      - "hypertension"
      - "blood pressure"
      - "obesity"
      - "arthritis"
      - "asthma"
      - "depression"
      - "anxiety disorder"
      - "infertility"
      - "impotence"
      - "kidney stone"
      - "thyroid"
      - "cholesterol"
      - "stroke"
      - "epilepsy"
      - "HIV"
      - "AIDS"
      - "tuberculosis"
      - "मधुमेह"
      - "शुगर"
      - "कैंसर"
      - "हृदय रोग"
      - "रक्तचाप"
      - "बीपी"
      - "मोटापा"
      - "गठिया"
      - "दमा"
      - "डिप्रेशन"
      - "बांझपन"
      - "थायराइड"
  - id: PL-HEALTH-03
    name: "Magic remedy"
    match: "phrase"
    severity: "Block"
    used_by: "003"
    terms:
      - "miracle"
      - "magical"
      - "magic cure"
      - "talisman"
      - "mantra cure"
      - "kavach"
      - "guaranteed cure"
      - "ancient secret"
      - "चमत्कारी"
      - "जादुई"
      - "ताबीज़"
      - "कवच"
      - "रामबाण"
  - id: PL-HEALTH-04
    name: "Outcome promises"
    match: "phrase + AI"
    severity: "Block"
    used_by: "004, 015"
    terms:
      - "reduce sick days"
      - "lower medical costs"
      - "reduce claims"
      - "reduce premiums"
      - "lose weight"
      - "improve immunity"
      - "lower stress levels"
      - "clinically proven"
      - "doctor recommended"
      - "बीमारी की छुट्टियाँ घटाएँ"
      - "वज़न घटाएँ"
      - "प्रीमियम कम करें"
  - id: PL-HEALTH-05
    name: "Traditional-medicine claims"
    match: "phrase"
    severity: "Block"
    used_by: "013"
    terms:
      - "Ayurvedic cure"
      - "herbal remedy"
      - "Unani"
      - "Siddha medicine"
      - "homeopathic treatment"
      - "आयुर्वेदिक इलाज"
      - "जड़ी-बूटी उपचार"
  - id: PL-HEALTH-06
    name: "Child health"
    match: "phrase"
    severity: "Block"
    used_by: "019"
    terms:
      - "children's health check"
      - "school health screening"
      - "paediatric"
      - "kids' immunity"
      - "बच्चों की सेहत जाँच"
```

### 11.15.12.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-HEALTH v0.1-draft → proposed v1.0 |
| Reviewer (name, enrolment no.) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| DMR Act section numbers and current Schedule confirmed (VR-14); Sch. J and AYUSH rule status (VR-15) | ☐ ☐ |
| PL-HEALTH-02 aligned to Schedule | ☐ |
| NMC regulation reference confirmed (VR-17) | ☐ |
| Hindi wording reviewed by | _______________________ |
| Conditions | _______________________ |
| Next review due | ____ / ____ / ______ |
| R10 approval / signatures | _______________ / _______________ |

---

## 11.15.13 RP-EDU-MINORS: EduVerse education communications and protection of minors

### 11.15.13.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-EDU-MINORS |
| Title | No direct outreach, profiling or targeted advertising to anyone under 18; guardian and institution channels only; verifiable parental consent; truthful education advertising |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | All (cross-cutting); Indian sources for IN; any non-India child audience is out of scope and blocked |
| Channels | ALL |
| Audiences | GDN (verified guardians), INST (schools and colleges under MoU, their administrators), B2B; **never** learners under 18; adult learners (18+) only with their own consent |
| Startups | EduVerse; any startup or tenant with an education offering; any audience with age band < 18 or unknown |
| Legal sources | DEC-030; BRL-ELG-13; CJ-IN-03; BR-V7-CJ-08; DPDP Act 2023 s.2(f), s.9(1)–(3), (5) and DPDP Rules 2025 Rule 10 and exemptions schedule (verify no., VR-01/02); CCPA Guidelines for Prevention of Misleading Advertisement in Coaching Sector 2024 (VR-16); CCPA 2022 Guidelines (advertisements addressed to children, VR-04); ASCI Code Ch. III (children) and ASCI guidance on education advertising (VR-08); RP-PLAT-ADS-004; US COPPA and UK AADC used only to exclude those audiences (VR-36) |
| Effective dates | DPDP children provisions with Rules from ≈ 13 May 2027 (VR-01); applied by the platform from activation (DEC-030); Coaching Guidelines 2024 (verify date) |
| Owner | R10 Legal/Compliance (with the child-safety specialist and the EduVerse owner) |
| Review cadence | Quarterly + event-driven |
| Expiry / fail-closed | 120 days; suspended → all EduVerse outbound held; age unknown → treated as minor (Block) |
| Depends on | RP-IN-DPDP, RP-IN-ADV, RP-PLAT-ADS, RP-COMMIT |

### 11.15.13.2 Plain-language summary

1. Never send anything to, profile, or target ads at anyone under 18. If age is unknown, treat the person as a minor.
2. Reach families only through verified guardians (OTP to the guardian's own channel + declaration + consent record) and schools or colleges under MoU.
3. Keep learner data to name, grade band and programme; no minor data in AI prompts beyond grade band.
4. No tracking pixels, behavioural monitoring or targeted advertising directed at children.
5. Do not write content aimed at children, and do not use "pester power" ("ask your parents").
6. Do not promise admissions, ranks, marks, selection or jobs; success stories only with written consent and full disclosure.
7. Accreditation and affiliation claims need documents.

### 11.15.13.3 Definitions

| Term | Definition |
|---|---|
| Minor / child | An individual under 18 years (DPDP s.2(f); DEC-030) |
| Age band | Self-declared or institution-provided age category captured first at intake (W17) |
| Verified guardian | A parent or lawful guardian verified by OTP on the guardian's own channel, explicit declaration and consent record (DEC-030); DPDP Rule 10 mechanism (e.g. DigiLocker tokens) to be confirmed (verify) |
| Institution under MoU | A school, college or university with a signed memorandum with EduVerse defining permitted communications |
| Child-directed content | Content whose subject, language, characters, imagery or offers are designed to appeal primarily to under-18s |
| Pester power | Content urging children to ask or pressure adults to buy |
| Outcome claim (education) | Any claim about admissions, ranks, marks, selection, placement, salary or success rate |

### 11.15.13.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-EDU-MINORS-001 | No communication, outreach, follow-up, sequence step or retargeting shall be addressed to any person whose age band is under 18 | DEC-030; BRL-ELG-13; CJ-IN-03; BR-V7-CJ-08 | ALL · ALL | DET | `contact.age_band < 18` or `school_learner = true` → Block | Block | Age band record | "Outreach to learners under 18 is not permitted. Contact the verified guardian or the institution instead." |
| RP-EDU-MINORS-002 | Where the age of a learner-facing contact is unknown, the contact shall be treated as a minor until age is established through the intake flow | BR-V7-CJ-08 ("age-unknown cases reviewed"); CP-05 | ALL · EduVerse | DET | EduVerse learner contact with `age_band = null` → Block and create review task | Block | Review task | "Age unknown: treated as a minor. Complete the age check first." |
| RP-EDU-MINORS-003 | Communications about a minor's education shall be sent only to a verified guardian (OTP to the guardian's own channel, explicit declaration and consent record) or to an institution under MoU through its designated officer | DEC-030; DPDP s.9(1) | ALL · GDN, INST | DET | Recipient role ∈ {verified_guardian, institution_officer}; `guardian_verification_id` or `mou_id` present | Block | Verification or MoU | "Send only to a verified guardian or the institution's designated contact." |
| RP-EDU-MINORS-004 | Processing of a child's personal data shall take place only after verifiable consent of the parent or lawful guardian, obtained through the mechanism approved by counsel under the DPDP Rules | DPDP s.9(1); Rule 10 (verify) | FM, ALL · GDN | DET | `vpc_record` with method, timestamp, guardian ID before any processing beyond intake | Block | VPC record | "Verified guardian consent is required before using the learner's details." |
| RP-EDU-MINORS-005 | Learner data shall be limited to name, grade band and programme; no other minor data shall be collected for marketing, and no minor data beyond grade band shall enter any AI prompt | DEC-030; DPDP s.6 (necessity); AU-004 | FM, ALL AI · ALL | DET | Form schema and prompt redaction log; fields ∉ allowed set → Block | Block | Schema and redaction logs | "Only name, grade band and programme may be recorded for a learner." |
| RP-EDU-MINORS-006 | No tracking, behavioural monitoring or targeted advertising shall be directed at children; pages and flows for minors and guardians shall carry no advertising pixels or third-party trackers | DPDP s.9(3); CJ-IN-03; RP-PLAT-ADS-004 | LP, AD · ALL | DET | Child- or guardian-flow pages: pixel and tracker list empty; ad audiences `age_min ≥ 18` | Block | Tag audit | "Remove trackers from these pages and target adults only." |
| RP-EDU-MINORS-007 | Content shall not be directed at children by subject, language, characters, imagery or offers, and shall not urge children to persuade adults to buy | ASCI Code Ch. III (children, verify no.); CCPA 2022 Guidelines (advertisements addressed to children) | ALL · ALL | DET+AI | DET: PL-EDU-MINORS-01; AI: cartoon characters, child slang, "ask your parents" | Block | — | "Write for guardians and institutions, not for children." |
| RP-EDU-MINORS-008 | Content shall not guarantee or imply guaranteed admission, rank, marks, selection, placement, job or salary, and shall not claim a success rate unless substantiated by an approved claim | CCPA Coaching Guidelines 2024 (VR-16); CPA s.2(28); DEC-744 | ALL · EduVerse | DET+AI | PL-EDU-MINORS-02; numeric success rates need `claim_id` | Block | Claim ID | "Remove guarantees of admission, ranks or jobs." |
| RP-EDU-MINORS-009 | The name, photograph, rank or testimonial of any successful learner shall be used only with prior written consent (of the guardian if under 18, and never in outreach to minors), and shall disclose the course actually taken, its duration and whether it was paid | CCPA Coaching Guidelines 2024 (VR-16); BRL-MKT-09 | ALL · EduVerse | DET | Learner showcase block → `consent_record_id` (+ guardian if minor) and disclosure fields | Block | Consent and disclosure | "Get written consent and disclose the course taken before featuring a learner." |
| RP-EDU-MINORS-010 | Claims of recognition, accreditation, affiliation, approval or ranking (e.g. by a university, board, regulator or ranking body) shall be made only with an approved claim backed by documents | CPA s.2(28); CCPA Coaching Guidelines 2024; RP-IN-ADV-019 | ALL · EduVerse | DET | PL-EDU-MINORS-03 → `claim_id` type `accreditation` | Block | Accreditation document | "Attach the accreditation document as an approved claim or remove the claim." |
| RP-EDU-MINORS-011 | Content shall not create false urgency about seats, admissions or fees | Dark-pattern Guidelines (false urgency); RP-IN-ADV-012 | ALL · EduVerse | DET | PL-IN-ADV-03 match → data binding | Block | Data binding | "Remove seat-urgency claims or bind them to live data." |
| RP-EDU-MINORS-012 | Fees shall be stated in full, including all mandatory charges, with the refund and cancellation policy referenced | CCPA Coaching Guidelines 2024 (verify); RP-IN-ADV-014; RP-COMMIT-007 | ALL · EduVerse | DET | Fee token → pricebook match + refund policy link | Warn | Pricebook and policy | "Show the full fee and link the refund policy." |
| RP-EDU-MINORS-013 | Institution outreach shall be addressed to administrators in their professional capacity and shall not ask the institution to forward marketing to students or to share student contact data | DEC-030; DPDP s.9 | EM, WA · INST | AI | AG-086: "share with your students", "forward to class groups" | Block | — | "Do not ask schools to forward marketing to students." |
| RP-EDU-MINORS-014 | Images or videos of minors shall be used only with guardian consent and the institution's approval under the MoU, never in ads, and never AI-generated to depict realistic children | DEC-030; RP-EU-AI-004; RP-IN-ADV-017 | MD, SO, LP · EduVerse | DET | Image classifier `minor_present` → `guardian_consent_id` and `mou_media_approval`; channel ≠ AD; `ai_generated` → Block | Block | Consents | "Images of children need guardian and school approval and cannot be used in ads or generated by AI." |
| RP-EDU-MINORS-015 | The intake form (W17) shall ask age band first; under 18 shall switch to the guardian flow before any other field | DEC-030; Part 0A | FM · EduVerse | DET | Form schema order check | Block | Form schema | "Ask age band first and switch to the guardian flow for under-18s." |
| RP-EDU-MINORS-016 | Children outside India (including US under-13s and UK children) shall not be processed or contacted | Platform scope; COPPA, UK AADC (VR-36) | ALL · ALL | DET | Age < 18 and jurisdiction ≠ IN → Block | Block | — | "Learners outside India are not supported." |
| RP-EDU-MINORS-017 | A DPIA covering the guardian and institution flows shall be approved before EduVerse activation | DEC-030 (DPIA-T1) | ALL · EduVerse | DET | `dpia.eduverse.status = approved` | Block | DPIA record | "Complete the EduVerse DPIA before activation." |
| RP-EDU-MINORS-018 | Adult learners (18 and over) may be contacted only with their own consent and under RP-IN-DPDP; adult status shall be confirmed, not inferred from grade or course | DPDP s.6; DEC-030 | ALL · B2C adults | DET | `age_band ≥ 18` from intake declaration; inferred age → Block | Block | Declaration | "Confirm the learner is an adult before contacting them." |
| RP-EDU-MINORS-019 | Content to guardians shall not exploit fears about a child's future, failure or social comparison | ASCI Code Ch. III; RP-EU-AI-009 | ALL · GDN | AI | AG-086 fear-appeal review ("your child will fall behind") | Block | — | "Remove fear-based messages about the child's future." |
| RP-EDU-MINORS-020 | Scholarship, free-course and discount offers shall state eligibility and conditions and match approved terms | CCPA 2022 Guidelines (free claims); RP-COMMIT-003 | ALL · EduVerse | DET | Offer tokens → `offer_term_id` | Block | Offer term | "State the conditions and link the approved offer." |

### 11.15.13.5 Required disclosures and approved template wording

| Template | Use | English | Hindi |
|---|---|---|---|
| TPL-EDU-01 | Intake age question (first field) | "Are you 18 or older? ◯ Yes ◯ No, I'm under 18 (a parent or guardian will need to complete this form)." | "क्या आपकी आयु 18 वर्ष या उससे अधिक है? ◯ हाँ ◯ नहीं, मेरी आयु 18 वर्ष से कम है (यह फ़ॉर्म माता-पिता या अभिभावक को भरना होगा)।" |
| TPL-EDU-02 | Guardian declaration | "I declare that I am the parent or lawful guardian of {learner name}, and I consent to {Startup} using their name, grade band and programme to {purpose}. I can withdraw this consent at any time." | "मैं घोषणा करता/करती हूँ कि मैं {learner name} का/की माता-पिता या वैध अभिभावक हूँ, और मैं {Startup} को उनके नाम, कक्षा-स्तर और कार्यक्रम का उपयोग {purpose} के लिए करने की सहमति देता/देती हूँ। मैं यह सहमति कभी भी वापस ले सकता/सकती हूँ।" |
| TPL-EDU-03 | Guardian OTP message | "{Startup}: your verification code is {otp}. You are confirming that you are the parent or guardian of a learner. Do not share this code." | "{Startup}: आपका सत्यापन कोड {otp} है। आप पुष्टि कर रहे हैं कि आप एक विद्यार्थी के माता-पिता या अभिभावक हैं। यह कोड किसी को न बताएँ।" |
| TPL-EDU-04 | Results disclaimer | "Past results do not guarantee future admissions, ranks or jobs. Featured learners took {course} for {duration} ({paid/free})." | "पिछले परिणाम भविष्य में प्रवेश, रैंक या नौकरी की गारंटी नहीं देते। प्रदर्शित विद्यार्थियों ने {duration} के लिए {course} ({सशुल्क/निःशुल्क}) किया था।" |
| TPL-EDU-05 | Institution outreach footer | "This message is intended for school or college administrators only. Please do not forward it to students." | "यह संदेश केवल स्कूल या कॉलेज के प्रशासकों के लिए है। कृपया इसे विद्यार्थियों को अग्रेषित न करें।" |

### 11.15.13.6 Prohibited content and phrase lists

| List | Name | Terms (en; hi) | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-EDU-MINORS-01 | Child-directed and pester-power cues | hey kids; ask your parents; tell your mom; tell your dad; for kids like you; cool kids; your friends already have; बच्चों; मम्मी-पापा से कहो; अपने माता-पिता से पूछो | phrase + AI | Block | 007 |
| PL-EDU-MINORS-02 | Guaranteed outcomes | guaranteed admission; guaranteed selection; 100% selection; assured rank; guaranteed job; placement guaranteed; top rank assured; sure-shot; पक्का एडमिशन; 100% चयन; नौकरी की गारंटी; रैंक की गारंटी | phrase | Block | 008 |
| PL-EDU-MINORS-03 | Accreditation claims | UGC approved; AICTE approved; CBSE affiliated; recognised by; accredited; NAAC; ranked No.; मान्यता प्राप्त; संबद्ध | phrase | Block without claim | 010 |
| PL-EDU-MINORS-04 | Fear appeals | your child will fall behind; don't let your child fail; others are ahead; future ruined; आपका बच्चा पीछे रह जाएगा | phrase + AI | Block | 019 |

### 11.15.13.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Transactional message to a verified guardian about an enrolled learner (timetable, fee receipt) | Allowed to the guardian; not to the learner |
| E-2 | Learner turns 18 | Contact needs their own consent; guardian consent does not transfer |
| E-3 | DPDP Rules exemptions for educational institutions (tracking for educational activities or safety) | Do not cover marketing; not relied on |
| E-4 | Institution asks EduVerse to present at a school assembly | Offline; materials still follow 007–010 |
| E-5 | Inbound message from a self-declared minor | Reply only with TPL-EDU-01-style redirection to a guardian; no data stored beyond what is needed to send that reply; no follow-up |

### 11.15.13.8 AG-086 review prompt guidance (RP-EDU-MINORS)

- **Look for:** any sign the reader is a child (second person + school-age references, games, cartoons, slang); requests to forward to students; guaranteed outcomes; unconsented learner showcases; fear appeals to parents; AI-generated children.
- **Cite:** `RP-EDU-MINORS-0NN`.
- **Escalate:** age ambiguity of any recipient; content for 16–18 year-old exam preparation (likely minors); accreditation wording.
- **Never:** pass content when the audience could include minors; uncertainty is `needs_counsel` and the deterministic age rule still blocks.

### 11.15.13.9 Test cases

| ID | Rule | Type | Input | Expected |
|---|---|---|---|---|
| TC-RP-EDU-MINORS-01 | 001 | Negative | Email to learner age band 15 (TC-V12-M-012 parity) | Block 001 |
| TC-RP-EDU-MINORS-02 | 002 | Negative | Learner with no age band | Block 002; review task |
| TC-RP-EDU-MINORS-03 | 003 | Positive | Email to verified guardian with OTP record | Pass |
| TC-RP-EDU-MINORS-04 | 003 | Negative | Guardian not verified | Block 003 |
| TC-RP-EDU-MINORS-05 | 006 | Negative | Meta pixel on guardian sign-up page | Block 006 |
| TC-RP-EDU-MINORS-06 | 007 | Negative | "Hey kids, ask your parents to sign you up!" | Block 007 |
| TC-RP-EDU-MINORS-07 | 008 | Negative | "100% selection guaranteed" | Block 008 |
| TC-RP-EDU-MINORS-08 | 009 | Negative | Topper photo without consent | Block 009 |
| TC-RP-EDU-MINORS-09 | 013 | Negative | "Please share this with all your students" | Block 013 |
| TC-RP-EDU-MINORS-10 | 014 | Negative | AI-generated realistic classroom children | Block 014 |
| TC-RP-EDU-MINORS-11 | 015 | Negative | W17 form asks email before age | Block 015 |
| TC-RP-EDU-MINORS-12 | 005 | Security | Prompt includes learner's date of birth | Block 005 |

### 11.15.13.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-EDU-MINORS
  title: "No direct outreach, profiling or targeted advertising to anyone under 18; guardian and institution channels only; verifiable parental consent; truthful education advertising"
  version: "0.1-draft"
  state: draft
  jurisdictions: "All (cross-cutting); Indian sources for IN; any non-India child audience is out of scope and blocked"
  channels: "ALL"
  audiences: "GDN (verified guardians), INST (schools and colleges under MoU, their administrators), B2B; never learners under 18; adult learners (18+) only with their own consent"
  startups: "EduVerse; any startup or tenant with an education offering; any audience with age band < 18 or unknown"
  effective_dates: "DPDP children provisions with Rules from ≈ 13 May 2027 (VR-01); applied by the platform from activation (DEC-030); Coaching Guidelines 2024 (verify date)"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
rules:
  - id: RP-EDU-MINORS-001
    obligation: "No communication, outreach, follow-up, sequence step or retargeting shall be addressed to any person whose age band is under 18"
    citation: "DEC-030; BRL-ELG-13; CJ-IN-03; BR-V7-CJ-08"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "contact.age_band < 18 or school_learner = true → Block"
    severity: "Block"
    override: none
    evidence: "Age band record"
    remediation_message: "\"Outreach to learners under 18 is not permitted. Contact the verified guardian or the institution instead.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-002
    obligation: "Where the age of a learner-facing contact is unknown, the contact shall be treated as a minor until age is established through the intake flow"
    citation: "BR-V7-CJ-08 (\"age-unknown cases reviewed\"); CP-05"
    applies_to: "ALL · EduVerse"
    check: "deterministic"
    detection: "EduVerse learner contact with age_band = null → Block and create review task"
    severity: "Block"
    override: none
    evidence: "Review task"
    remediation_message: "\"Age unknown: treated as a minor. Complete the age check first.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-003
    obligation: "Communications about a minor's education shall be sent only to a verified guardian (OTP to the guardian's own channel, explicit declaration and consent record) or to an institution under MoU through its designated officer"
    citation: "DEC-030; DPDP s.9(1)"
    applies_to: "ALL · GDN, INST"
    check: "deterministic"
    detection: "Recipient role ∈ {verified_guardian, institution_officer}; guardian_verification_id or mou_id present"
    severity: "Block"
    override: none
    evidence: "Verification or MoU"
    remediation_message: "\"Send only to a verified guardian or the institution's designated contact.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-004
    obligation: "Processing of a child's personal data shall take place only after verifiable consent of the parent or lawful guardian, obtained through the mechanism approved by counsel under the DPDP Rules"
    citation: "DPDP s.9(1); Rule 10 (verify)"
    applies_to: "FM, ALL · GDN"
    check: "deterministic"
    detection: "vpc_record with method, timestamp, guardian ID before any processing beyond intake"
    severity: "Block"
    override: none
    evidence: "VPC record"
    remediation_message: "\"Verified guardian consent is required before using the learner's details.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-005
    obligation: "Learner data shall be limited to name, grade band and programme; no other minor data shall be collected for marketing, and no minor data beyond grade band shall enter any AI prompt"
    citation: "DEC-030; DPDP s.6 (necessity); AU-004"
    applies_to: "FM, ALL AI · ALL"
    check: "deterministic"
    detection: "Form schema and prompt redaction log; fields ∉ allowed set → Block"
    severity: "Block"
    override: none
    evidence: "Schema and redaction logs"
    remediation_message: "\"Only name, grade band and programme may be recorded for a learner.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-006
    obligation: "No tracking, behavioural monitoring or targeted advertising shall be directed at children; pages and flows for minors and guardians shall carry no advertising pixels or third-party trackers"
    citation: "DPDP s.9(3); CJ-IN-03; RP-PLAT-ADS-004"
    applies_to: "LP, AD · ALL"
    check: "deterministic"
    detection: "Child- or guardian-flow pages: pixel and tracker list empty; ad audiences age_min ≥ 18"
    severity: "Block"
    override: none
    evidence: "Tag audit"
    remediation_message: "\"Remove trackers from these pages and target adults only.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-007
    obligation: "Content shall not be directed at children by subject, language, characters, imagery or offers, and shall not urge children to persuade adults to buy"
    citation: "ASCI Code Ch. III (children, verify no.); CCPA 2022 Guidelines (advertisements addressed to children)"
    applies_to: "ALL · ALL"
    check: "deterministic_then_ai_review"
    detection: "DET: PL-EDU-MINORS-01; AI: cartoon characters, child slang, \"ask your parents\""
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Write for guardians and institutions, not for children.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-008
    obligation: "Content shall not guarantee or imply guaranteed admission, rank, marks, selection, placement, job or salary, and shall not claim a success rate unless substantiated by an approved claim"
    citation: "CCPA Coaching Guidelines 2024 (VR-16); CPA s.2(28); DEC-744"
    applies_to: "ALL · EduVerse"
    check: "deterministic_then_ai_review"
    detection: "PL-EDU-MINORS-02; numeric success rates need claim_id"
    severity: "Block"
    override: r10_with_reason
    evidence: "Claim ID"
    remediation_message: "\"Remove guarantees of admission, ranks or jobs.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-009
    obligation: "The name, photograph, rank or testimonial of any successful learner shall be used only with prior written consent (of the guardian if under 18, and never in outreach to minors), and shall disclose the course actually taken, its duration and whether it was paid"
    citation: "CCPA Coaching Guidelines 2024 (VR-16); BRL-MKT-09"
    applies_to: "ALL · EduVerse"
    check: "deterministic"
    detection: "Learner showcase block → consent_record_id (+ guardian if minor) and disclosure fields"
    severity: "Block"
    override: none
    evidence: "Consent and disclosure"
    remediation_message: "\"Get written consent and disclose the course taken before featuring a learner.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-010
    obligation: "Claims of recognition, accreditation, affiliation, approval or ranking (e.g. by a university, board, regulator or ranking body) shall be made only with an approved claim backed by documents"
    citation: "CPA s.2(28); CCPA Coaching Guidelines 2024; RP-IN-ADV-019"
    applies_to: "ALL · EduVerse"
    check: "deterministic"
    detection: "PL-EDU-MINORS-03 → claim_id type accreditation"
    severity: "Block"
    override: none
    evidence: "Accreditation document"
    remediation_message: "\"Attach the accreditation document as an approved claim or remove the claim.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-011
    obligation: "Content shall not create false urgency about seats, admissions or fees"
    citation: "Dark-pattern Guidelines (false urgency); RP-IN-ADV-012"
    applies_to: "ALL · EduVerse"
    check: "deterministic"
    detection: "PL-IN-ADV-03 match → data binding"
    severity: "Block"
    override: none
    evidence: "Data binding"
    remediation_message: "\"Remove seat-urgency claims or bind them to live data.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-012
    obligation: "Fees shall be stated in full, including all mandatory charges, with the refund and cancellation policy referenced"
    citation: "CCPA Coaching Guidelines 2024 (verify); RP-IN-ADV-014; RP-COMMIT-007"
    applies_to: "ALL · EduVerse"
    check: "deterministic"
    detection: "Fee token → pricebook match + refund policy link"
    severity: "Warn"
    override: none
    evidence: "Pricebook and policy"
    remediation_message: "\"Show the full fee and link the refund policy.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-013
    obligation: "Institution outreach shall be addressed to administrators in their professional capacity and shall not ask the institution to forward marketing to students or to share student contact data"
    citation: "DEC-030; DPDP s.9"
    applies_to: "EM, WA · INST"
    check: "ai_review"
    detection: "AG-086: \"share with your students\", \"forward to class groups\""
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Do not ask schools to forward marketing to students.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-014
    obligation: "Images or videos of minors shall be used only with guardian consent and the institution's approval under the MoU, never in ads, and never AI-generated to depict realistic children"
    citation: "DEC-030; RP-EU-AI-004; RP-IN-ADV-017"
    applies_to: "MD, SO, LP · EduVerse"
    check: "deterministic"
    detection: "Image classifier minor_present → guardian_consent_id and mou_media_approval; channel ≠ AD; ai_generated → Block"
    severity: "Block"
    override: none
    evidence: "Consents"
    remediation_message: "\"Images of children need guardian and school approval and cannot be used in ads or generated by AI.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-015
    obligation: "The intake form (W17) shall ask age band first; under 18 shall switch to the guardian flow before any other field"
    citation: "DEC-030; Part 0A"
    applies_to: "FM · EduVerse"
    check: "deterministic"
    detection: "Form schema order check"
    severity: "Block"
    override: none
    evidence: "Form schema"
    remediation_message: "\"Ask age band first and switch to the guardian flow for under-18s.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-016
    obligation: "Children outside India (including US under-13s and UK children) shall not be processed or contacted"
    citation: "Platform scope; COPPA, UK AADC (VR-36)"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Age < 18 and jurisdiction ≠ IN → Block"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"Learners outside India are not supported.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-017
    obligation: "A DPIA covering the guardian and institution flows shall be approved before EduVerse activation"
    citation: "DEC-030 (DPIA-T1)"
    applies_to: "ALL · EduVerse"
    check: "deterministic"
    detection: "dpia.eduverse.status = approved"
    severity: "Block"
    override: none
    evidence: "DPIA record"
    remediation_message: "\"Complete the EduVerse DPIA before activation.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-018
    obligation: "Adult learners (18 and over) may be contacted only with their own consent and under RP-IN-DPDP; adult status shall be confirmed, not inferred from grade or course"
    citation: "DPDP s.6; DEC-030"
    applies_to: "ALL · B2C adults"
    check: "deterministic"
    detection: "age_band ≥ 18 from intake declaration; inferred age → Block"
    severity: "Block"
    override: none
    evidence: "Declaration"
    remediation_message: "\"Confirm the learner is an adult before contacting them.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-019
    obligation: "Content to guardians shall not exploit fears about a child's future, failure or social comparison"
    citation: "ASCI Code Ch. III; RP-EU-AI-009"
    applies_to: "ALL · GDN"
    check: "ai_review"
    detection: "AG-086 fear-appeal review (\"your child will fall behind\")"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Remove fear-based messages about the child's future.\""
    effective_from: null  # set at sign-off
  - id: RP-EDU-MINORS-020
    obligation: "Scholarship, free-course and discount offers shall state eligibility and conditions and match approved terms"
    citation: "CCPA 2022 Guidelines (free claims); RP-COMMIT-003"
    applies_to: "ALL · EduVerse"
    check: "deterministic"
    detection: "Offer tokens → offer_term_id"
    severity: "Block"
    override: none
    evidence: "Offer term"
    remediation_message: "\"State the conditions and link the approved offer.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-EDU-MINORS-01
    name: "Child-directed and pester-power cues"
    match: "phrase + AI"
    severity: "Block"
    used_by: "007"
    terms:
      - "hey kids"
      - "ask your parents"
      - "tell your mom"
      - "tell your dad"
      - "for kids like you"
      - "cool kids"
      - "your friends already have"
      - "बच्चों"
      - "मम्मी-पापा से कहो"
      - "अपने माता-पिता से पूछो"
  - id: PL-EDU-MINORS-02
    name: "Guaranteed outcomes"
    match: "phrase"
    severity: "Block"
    used_by: "008"
    terms:
      - "guaranteed admission"
      - "guaranteed selection"
      - "100% selection"
      - "assured rank"
      - "guaranteed job"
      - "placement guaranteed"
      - "top rank assured"
      - "sure-shot"
      - "पक्का एडमिशन"
      - "100% चयन"
      - "नौकरी की गारंटी"
      - "रैंक की गारंटी"
  - id: PL-EDU-MINORS-03
    name: "Accreditation claims"
    match: "phrase"
    severity: "Block without claim"
    used_by: "010"
    terms:
      - "UGC approved"
      - "AICTE approved"
      - "CBSE affiliated"
      - "recognised by"
      - "accredited"
      - "NAAC"
      - "ranked No."
      - "मान्यता प्राप्त"
      - "संबद्ध"
  - id: PL-EDU-MINORS-04
    name: "Fear appeals"
    match: "phrase + AI"
    severity: "Block"
    used_by: "019"
    terms:
      - "your child will fall behind"
      - "don't let your child fail"
      - "others are ahead"
      - "future ruined"
      - "आपका बच्चा पीछे रह जाएगा"
```

### 11.15.13.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-EDU-MINORS v0.1-draft → proposed v1.0 |
| Reviewer (name, enrolment no.) and child-safety reviewer | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| VPC mechanism under DPDP Rule 10 approved (method: ______) | ☐ |
| Coaching Guidelines 2024 applicability to EduVerse confirmed (VR-16) | ☐ |
| Hindi wording reviewed by | _______________________ |
| Conditions | _______________________ |
| Next review due | ____ / ____ / ______ |
| R10 approval / signatures | _______________ / _______________ |

---

## 11.15.14 RP-COMMIT: Commitments and promises (all startups)

### 11.15.14.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-COMMIT |
| Title | Commitments, prices, discounts, delivery dates, SLAs, guarantees, refunds and offer language: every commitment must be backed by an approved term; AI never sets prices or makes binding offers |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | All (cross-cutting); Indian Contract Act and CPA for IN; FTC Act/ROSCA for US; UCPD for EU (via their packs) |
| Channels | ALL, including DOC (proposals, quotes) and bid drafts |
| Audiences | ALL |
| Startups | ALL (AppNAI bids, OrganicSpec orders, MedMaarg partnerships, EduVerse fees, SaaS operator); Tenant |
| Legal sources | Indian Contract Act 1872 ss.2–10 (offer, acceptance, consideration) (VR-34); CPA 2019 s.2(28), s.2(47) incl. false warranty or guarantee (verify sub-clause) (VR-05); CCPA 2022 Guidelines (VR-04); FSSAI (Organic Foods) Regulations 2017 (VR-35); FTC Act §5; ROSCA (VR-40); UCPD Arts 6–7; DEC-064 (autonomy caps); DEC-744 (no outcome guarantees); BRL-AUT-01; CJ-GL-04, CJ-GL-12, CJ-GL-13; FR-V12-M-011; AG-086 card (commitment detection); TC-V12-M-017 |
| Effective dates | Stable law; platform invariants in force |
| Owner | R10 Legal/Compliance (with Finance for pricebook and terms) |
| Review cadence | Quarterly + event-driven (pricebook, SLA or refund-policy version change) |
| Expiry / fail-closed | 120 days; pricebook or terms lookup unavailable → Block |
| Depends on | All packs (applies alongside them) |

### 11.15.14.2 Plain-language summary

1. Any number, date, percentage, price, discount, SLA, warranty, guarantee, refund or deadline in outbound content must match an approved term for that offering, market, customer and date.
2. AI never sets or changes prices or discounts; it can only quote the pricebook.
3. No outcome guarantees ("guaranteed leads", "guaranteed ROI"); forecasts are labelled estimates.
4. Marketing does not make legal promises (liability, exclusivity, indemnity); those belong in contracts approved by a person.
5. Never write a message that could be accepted as a binding offer unless it is an approved quote at L1.
6. Do not promote offerings that are planned or unavailable.
7. Product-quality claims (e.g. "certified organic") need certificates.

### 11.15.14.3 Definitions

| Term | Definition |
|---|---|
| Commitment | Any statement by which the startup undertakes, promises or represents a future act, result, quantity, quality, time, price or remedy |
| Approved term | A record in the pricebook (TL-27 `pricebook.lookup`), offer terms, SLA catalogue, refund policy, contract template or claims library (TL-09) with version, scope and validity |
| Backed commitment | A commitment span linked to an approved term whose scope covers the offering, market, customer segment and date |
| Offer language | Words indicating willingness to be bound on acceptance ("we hereby offer", "accept by replying", "this quote is binding") |
| Outcome guarantee | A promise of a business or personal result (leads, revenue, ROI, rank, health) |

### 11.15.14.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-COMMIT-001 | Every commitment in outbound content (delivery date or lead time, quantity, price, discount, SLA, uptime, response time, warranty, guarantee, refund, penalty, free addition, validity period) shall be backed by an approved term valid for the offering, market, recipient and date of dispatch | AG-086 card; FR-V12-M-011; CPA s.2(28); Indian Contract Act ss.2–10 | ALL · ALL | DET+AI | DET: extract numbers, dates, %, currency, duration and PL-COMMIT-01 terms; join to term store; AI: implicit commitments; unbacked → finding | Block (price, discount, refund, guarantee, delivery date); Warn (other) | `term_id` per span | "This promise is not backed by an approved term. Link the term or remove the promise." |
| RP-COMMIT-002 | Prices shall be quoted only from the approved pricebook; AI shall not compute, propose, round or modify a price | DEC-064; BRL-AUT-01; safety invariant "AI never sets prices" | ALL · ALL | DET | Every currency amount = pricebook value for offering × market × date (exact match, incl. tax treatment) | Block | Pricebook entry | "Prices must come from the approved pricebook." |
| RP-COMMIT-003 | Discounts, credits, free periods and bundles shall be stated only where an approved discount or offer term within the approval band exists and has been approved by a person (L1) | DEC-064; BRL-AUT-01; RP-IN-ADV-009 | ALL · ALL | DET | `%`, "off", "discount", "free month" → `offer_term_id` with approver | Block | Offer term | "Discounts need an approved offer term." |
| RP-COMMIT-004 | Content shall not guarantee or promise business, financial, academic or health outcomes (e.g. leads, revenue, ROI, conversion, ranking, selection, weight loss) | DEC-744; CPA s.2(47) (false guarantee); FTC Act §5; RP-HEALTH-004; RP-EDU-MINORS-008 | ALL · ALL | DET+AI | PL-COMMIT-02 + outcome noun; AI: implied guarantees | Block | — | "Do not guarantee results. Describe what the service does." |
| RP-COMMIT-005 | Forecasts, projections and estimates shall be labelled as estimates with their basis and shall not be presented as commitments | CJ-GL-13; RP-IN-ADV-020 | ALL · ALL | DET+AI | Future-tense numeric outcome → TPL-COMMIT-02 present | Block | Estimate basis | "Label this as an estimate and state its basis." |
| RP-COMMIT-006 | Statements about service levels (availability, response, resolution, support hours) shall match the published SLA version for the plan | BRD 21 (SLA); FR-V12-A SLA set; CPA s.2(28) | ALL · ALL | DET | SLA tokens ("99.9%", "within 4 hours", "24x7") → `sla_id` and value match | Block | SLA version | "Use the SLA values of the customer's plan." |
| RP-COMMIT-007 | Refund, cancellation and return statements shall match the current approved policy version and shall not promise more or less than it | CPA s.2(47); ROSCA (US); Consumer Protection (E-Commerce) Rules 2020 (VR-39) | ALL · ALL | DET | "refund", "money back", "cancel anytime" → `policy_version` link and text match | Block | Policy version | "Refund and cancellation wording must match the approved policy." |
| RP-COMMIT-008 | Marketing and outreach content shall not state legal terms (liability caps, indemnities, exclusivity, IP ownership, governing law, penalties); these shall appear only in approved contract documents reviewed by a person | DEC-064 (legal terms ≤ L1); CJ-GL-12 | EM, WA, SO, LP · ALL | DET+AI | PL-COMMIT-03 | Block | — | "Legal terms belong in the approved contract, not in this message." |
| RP-COMMIT-009 | Content shall not contain offer language capable of acceptance (e.g. "we hereby offer", "reply YES to accept", "this quote is binding") unless the item is an approved quote or proposal document with an L1 approval hash | Indian Contract Act ss.2(a)–(b), 7; DEC-064; BRL-AUT-01 | ALL · ALL | DET+AI | PL-COMMIT-04; item type ≠ approved_quote → finding | Block | Approval hash | "This wording could create a binding offer. Use an approved quote instead." |
| RP-COMMIT-010 | Planned, unavailable or unlicensed offerings shall not be promoted, quoted or committed to | CJ-GL-04; RP-IN-ADV-021 | ALL · ALL | DET | Offering `status ≠ available` for market | Block | Offering status | "This offering is not available; remove the commitment." |
| RP-COMMIT-011 | Every offer shall state its validity period, and the stated period shall not exceed the term's validity | CCPA 2022 Guidelines (bait); UCPD Annex I no. 7 | ALL · ALL | DET | Offer present → `valid_until` ≤ term validity; stated in content | Warn | Term validity | "State when this offer ends, within the approved validity." |
| RP-COMMIT-012 | Prices shall state currency and whether taxes (GST, VAT) are included; tax figures shall come from the approved tax configuration | CJ-IN-10; DEC-027; Legal Metrology/CPA price display (verify) | ALL · ALL | DET | Currency code/symbol present; "incl./excl. GST" token | Warn | Tax config | "State the currency and whether tax is included." |
| RP-COMMIT-013 | Bid and tender drafts (AppNAI) shall not contain any commitment, price, timeline or compliance declaration not approved by a person, and AI shall never submit a bid | DEC-064; BRL-BID-02; safety invariant | DOC · AppNAI | DET | Bid draft commitment spans → each `term_id` + reviewer; submission action by AI → Block | Block | Bid approval | "Every bid commitment must be approved by a person; AI cannot submit bids." |
| RP-COMMIT-014 | Product-quality, origin and certification claims for goods (e.g. "certified organic", "Jaivik Bharat", "NPOP certified", grade, moisture, origin) shall be backed by a valid certificate or lab report linked as an approved claim | FSSAI (Organic Foods) Regulations 2017 (VR-35); CPA s.2(28) | ALL · OrganicSpec | DET | PL-COMMIT-05 → `certificate_id` valid on dispatch date | Block | Certificate | "Attach the valid certificate before claiming organic or quality grades." |
| RP-COMMIT-015 | Response-time promises in replies ("we will call you within the hour") shall be made only where the owning team's operating calendar supports them | CPA s.2(28); BRL-ELG-08 | EM, WA, CH · ALL | DET+AI | Duration tokens in replies → team calendar capacity check | Warn | Calendar | "Avoid promising a response time the team cannot meet." |
| RP-COMMIT-016 | Free trials and "no cost" statements shall match the entitlement configuration, including duration, limits and conversion to paid | DEC-502; RP-IN-ADV-009; ROSCA | ALL · ALL | DET | Trial tokens → `entitlement_plan` match | Block | Entitlement record | "Trial wording must match the configured trial." |
| RP-COMMIT-017 | The same offer sent to multiple recipients in one campaign shall be identical in its commitments, except for approved personalisation fields | AU-122 grouped approval (DEC-745) | ALL · ALL | DET | Commitment spans hashed per item; outliers flagged | Warn | Packet hash | "Commitments differ between recipients; review the outliers." |
| RP-COMMIT-018 | Commitments in Hindi, other Indian languages and code-mixed text shall be detected and backed in the same way | DEC-026; G-8 | ALL · ALL | DET+AI | PL-COMMIT-01 Hindi terms; numeral normalisation (Devanagari digits) | Block | As rule 001 | "This promise in {language} needs an approved term." |
| RP-COMMIT-019 | Warranties or guarantees of performance, efficacy or life of a product or service shall not be given unless based on an adequate or proper test and approved as a term | CPA s.2(47) (false warranty, verify sub-clause) | ALL · ALL | DET+AI | "warranty", "guarantee", "lasts", "assured" → `term_id` type `warranty` | Block | Warranty term and test basis | "Warranties need an approved term backed by a test." |
| RP-COMMIT-020 | Content shall not offer, solicit or refer to investment, fundraising, securities, returns on investment in the startup, or investor opportunities | DEC-002; BRL-TEN-12 | ALL · ALL | DET | PL-COMMIT-06 | Block | — | "This product does not support investment or fundraising content." |

### 11.15.14.5 Required disclosures and approved template wording

| Template | Use | English | Hindi |
|---|---|---|---|
| TPL-COMMIT-01 | Offer terms line | "Offer valid until {date} for {eligible customers}. Price {amount} {currency} {incl./excl.} GST. Full terms: {link}." | "यह ऑफ़र {date} तक {eligible customers} के लिए मान्य है। मूल्य {amount} {currency}, GST {सहित/अतिरिक्त}। पूर्ण शर्तें: {link}।" |
| TPL-COMMIT-02 | Estimate label | "Estimate based on {basis}; actual results may differ and are not guaranteed." | "{basis} पर आधारित अनुमान; वास्तविक परिणाम भिन्न हो सकते हैं और इनकी गारंटी नहीं है।" |
| TPL-COMMIT-03 | Indicative information (no offer) | "This message is for information only and is not an offer. A formal quote will follow after review." | "यह संदेश केवल जानकारी के लिए है और कोई प्रस्ताव नहीं है। समीक्षा के बाद औपचारिक कोटेशन भेजा जाएगा।" |
| TPL-COMMIT-04 | SLA reference | "Service levels for your plan are described in {SLA name, version}." | "आपकी योजना के सेवा स्तर {SLA name, version} में दिए गए हैं।" |
| TPL-COMMIT-05 | No outcome guarantee | "We do not guarantee specific business results." | "हम किसी विशिष्ट व्यावसायिक परिणाम की गारंटी नहीं देते।" |

### 11.15.14.6 Prohibited content and phrase lists

| List | Name | Terms (en; hi) | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-COMMIT-01 | Commitment markers | deliver by; delivered within; in {n} days; lead time; we will; we commit; guaranteed; assured; refund; money-back; SLA; uptime; within {n} hours; discount; % off; free; warranty; penalty; डिलीवरी; दिनों में; गारंटी; पक्का; रिफ़ंड; छूट; मुफ़्त; वारंटी | regex with number/date capture | Triggers rule 001 | 001, 018 |
| PL-COMMIT-02 | Outcome guarantees | guaranteed leads; guaranteed ROI; guaranteed revenue; guaranteed growth; double your sales; assured returns; risk-free results; पक्के लीड; गारंटीड मुनाफ़ा; बिक्री दोगुनी | phrase | Block | 004 |
| PL-COMMIT-03 | Legal terms in marketing | liability; indemnify; indemnity; exclusive rights; governing law; jurisdiction of courts; liquidated damages; penalty clause; IP ownership; दायित्व; क्षतिपूर्ति; अनन्य अधिकार | phrase | Block | 008 |
| PL-COMMIT-04 | Offer language | we hereby offer; reply YES to accept; this quote is binding; deemed accepted; accept by replying; hereby agree; हम एतद्द्वारा प्रस्ताव करते हैं; स्वीकार करने के लिए YES लिखें | phrase | Block unless approved quote | 009 |
| PL-COMMIT-05 | Quality and origin claims | certified organic; 100% organic; Jaivik Bharat; NPOP; India Organic; chemical-free; pesticide-free; Grade A; प्रमाणित जैविक; रसायन मुक्त | phrase | Block without certificate | 014 |
| PL-COMMIT-06 | Investment and fundraising | invest in us; investment opportunity; equity; shares; fundraising; investor deck; assured returns on investment; निवेश का अवसर; शेयर | phrase | Block | 020 |

### 11.15.14.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Approved quote or proposal document with L1 hash | Rules 008 and 009 do not block content inside the approved document; edits invalidate the hash (BRL-APR, TC-V12-M-018) |
| E-2 | Restating the customer's own requested date ("you asked for delivery by 5 May") | Not a commitment if clearly attributed; AG-086 may pass; DET flags and AI decides |
| E-3 | Historic facts ("we delivered 40 t in March") | Claim, not commitment; RP-IN-ADV-002 applies |
| E-4 | Internal notes | Out of scope |
| E-5 | Transactional confirmation of an already approved order | Values must equal the order record (DET); no new commitments |

### 11.15.14.8 AG-086 review prompt guidance (RP-COMMIT)

- **Look for:** every span that a recipient could hold the startup to: numbers with units, dates, deadlines, "we will", "guaranteed", refunds, SLAs, legal terms, acceptance mechanics; implicit commitments ("you'll never miss a tender again"); code-mixed promises.
- **Cite:** `RP-COMMIT-0NN`; for each commitment return `{span, type, backed_by_term_id or null}` as the AG-086 output schema requires.
- **Escalate:** offer-vs-information ambiguity; warranty wording; commitments in bids.
- **Never:** suggest a different price, discount or date; rewrites may only remove the commitment, insert an estimate label, or reference the approved term.

### 11.15.14.9 Test cases

| ID | Rule | Type | Input | Expected |
|---|---|---|---|---|
| TC-RP-COMMIT-01 | 001 | Negative | "We will deliver in 3 days" without term (Part 11.13b Gherkin) | Block 001 (Part 11.13b scenario showed `fix`; this pack sets delivery dates to Block, see DEC-765) |
| TC-RP-COMMIT-02 | 001 | Positive | "Delivery in 7–10 days" linked to lead-time term for the market | Pass |
| TC-RP-COMMIT-03 | 002 | Negative | AI computed "₹45,000 after adjustment" | Block 002 |
| TC-RP-COMMIT-04 | 003 | Negative | "15% off this week" without offer term (TC-V12-M-017 parity) | Block 003 |
| TC-RP-COMMIT-05 | 004 | Negative | "Guaranteed 50 qualified leads a month" | Block 004 |
| TC-RP-COMMIT-06 | 006 | Negative | "99.99% uptime" on a plan with 99.5% SLA | Block 006 |
| TC-RP-COMMIT-07 | 008 | Negative | "Our liability is limited to fees paid" in a WhatsApp message | Block 008 |
| TC-RP-COMMIT-08 | 009 | Negative | "Reply YES to accept this offer" in a cold email | Block 009 |
| TC-RP-COMMIT-09 | 013 | Negative | AppNAI bid draft with unapproved completion date | Block 013 |
| TC-RP-COMMIT-10 | 014 | Negative | OrganicSpec "certified organic" with expired certificate | Block 014 |
| TC-RP-COMMIT-11 | 018 | Negative | "3 din mein delivery pakka" | Block 018 |
| TC-RP-COMMIT-12 | 020 | Negative | "Investment opportunity in OrganicSpec" | Block 020 |

### 11.15.14.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-COMMIT
  title: "Commitments, prices, discounts, delivery dates, SLAs, guarantees, refunds and offer language: every commitment must be backed by an approved term; AI never sets prices or makes binding offers"
  version: "0.1-draft"
  state: draft
  jurisdictions: "All (cross-cutting); Indian Contract Act and CPA for IN; FTC Act/ROSCA for US; UCPD for EU (via their packs)"
  channels: "ALL, including DOC (proposals, quotes) and bid drafts"
  audiences: "ALL"
  startups: "ALL (AppNAI bids, OrganicSpec orders, MedMaarg partnerships, EduVerse fees, SaaS operator); Tenant"
  effective_dates: "Stable law; platform invariants in force"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
rules:
  - id: RP-COMMIT-001
    obligation: "Every commitment in outbound content (delivery date or lead time, quantity, price, discount, SLA, uptime, response time, warranty, guarantee, refund, penalty, free addition, validity period) shall be backed by an approved term valid for the offering, market, recipient and date of dispatch"
    citation: "AG-086 card; FR-V12-M-011; CPA s.2(28); Indian Contract Act ss.2–10"
    applies_to: "ALL · ALL"
    check: "deterministic_then_ai_review"
    detection: "DET: extract numbers, dates, %, currency, duration and PL-COMMIT-01 terms; join to term store; AI: implicit commitments; unbacked → finding"
    severity: "Block (price, discount, refund, guarantee, delivery date); Warn (other)"
    override: r10_with_reason
    evidence: "term_id per span"
    remediation_message: "\"This promise is not backed by an approved term. Link the term or remove the promise.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-002
    obligation: "Prices shall be quoted only from the approved pricebook; AI shall not compute, propose, round or modify a price"
    citation: "DEC-064; BRL-AUT-01; safety invariant \"AI never sets prices\""
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Every currency amount = pricebook value for offering × market × date (exact match, incl. tax treatment)"
    severity: "Block"
    override: none
    evidence: "Pricebook entry"
    remediation_message: "\"Prices must come from the approved pricebook.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-003
    obligation: "Discounts, credits, free periods and bundles shall be stated only where an approved discount or offer term within the approval band exists and has been approved by a person (L1)"
    citation: "DEC-064; BRL-AUT-01; RP-IN-ADV-009"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "%, \"off\", \"discount\", \"free month\" → offer_term_id with approver"
    severity: "Block"
    override: none
    evidence: "Offer term"
    remediation_message: "\"Discounts need an approved offer term.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-004
    obligation: "Content shall not guarantee or promise business, financial, academic or health outcomes (e.g. leads, revenue, ROI, conversion, ranking, selection, weight loss)"
    citation: "DEC-744; CPA s.2(47) (false guarantee); FTC Act §5; RP-HEALTH-004; RP-EDU-MINORS-008"
    applies_to: "ALL · ALL"
    check: "deterministic_then_ai_review"
    detection: "PL-COMMIT-02 + outcome noun; AI: implied guarantees"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Do not guarantee results. Describe what the service does.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-005
    obligation: "Forecasts, projections and estimates shall be labelled as estimates with their basis and shall not be presented as commitments"
    citation: "CJ-GL-13; RP-IN-ADV-020"
    applies_to: "ALL · ALL"
    check: "deterministic_then_ai_review"
    detection: "Future-tense numeric outcome → TPL-COMMIT-02 present"
    severity: "Block"
    override: r10_with_reason
    evidence: "Estimate basis"
    remediation_message: "\"Label this as an estimate and state its basis.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-006
    obligation: "Statements about service levels (availability, response, resolution, support hours) shall match the published SLA version for the plan"
    citation: "BRD 21 (SLA); FR-V12-A SLA set; CPA s.2(28)"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "SLA tokens (\"99.9%\", \"within 4 hours\", \"24x7\") → sla_id and value match"
    severity: "Block"
    override: none
    evidence: "SLA version"
    remediation_message: "\"Use the SLA values of the customer's plan.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-007
    obligation: "Refund, cancellation and return statements shall match the current approved policy version and shall not promise more or less than it"
    citation: "CPA s.2(47); ROSCA (US); Consumer Protection (E-Commerce) Rules 2020 (VR-39)"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "\"refund\", \"money back\", \"cancel anytime\" → policy_version link and text match"
    severity: "Block"
    override: none
    evidence: "Policy version"
    remediation_message: "\"Refund and cancellation wording must match the approved policy.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-008
    obligation: "Marketing and outreach content shall not state legal terms (liability caps, indemnities, exclusivity, IP ownership, governing law, penalties); these shall appear only in approved contract documents reviewed by a person"
    citation: "DEC-064 (legal terms ≤ L1); CJ-GL-12"
    applies_to: "EM, WA, SO, LP · ALL"
    check: "deterministic_then_ai_review"
    detection: "PL-COMMIT-03"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Legal terms belong in the approved contract, not in this message.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-009
    obligation: "Content shall not contain offer language capable of acceptance (e.g. \"we hereby offer\", \"reply YES to accept\", \"this quote is binding\") unless the item is an approved quote or proposal document with an L1 approval hash"
    citation: "Indian Contract Act ss.2(a)–(b), 7; DEC-064; BRL-AUT-01"
    applies_to: "ALL · ALL"
    check: "deterministic_then_ai_review"
    detection: "PL-COMMIT-04; item type ≠ approved_quote → finding"
    severity: "Block"
    override: r10_with_reason
    evidence: "Approval hash"
    remediation_message: "\"This wording could create a binding offer. Use an approved quote instead.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-010
    obligation: "Planned, unavailable or unlicensed offerings shall not be promoted, quoted or committed to"
    citation: "CJ-GL-04; RP-IN-ADV-021"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Offering status ≠ available for market"
    severity: "Block"
    override: none
    evidence: "Offering status"
    remediation_message: "\"This offering is not available; remove the commitment.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-011
    obligation: "Every offer shall state its validity period, and the stated period shall not exceed the term's validity"
    citation: "CCPA 2022 Guidelines (bait); UCPD Annex I no. 7"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Offer present → valid_until ≤ term validity; stated in content"
    severity: "Warn"
    override: none
    evidence: "Term validity"
    remediation_message: "\"State when this offer ends, within the approved validity.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-012
    obligation: "Prices shall state currency and whether taxes (GST, VAT) are included; tax figures shall come from the approved tax configuration"
    citation: "CJ-IN-10; DEC-027; Legal Metrology/CPA price display (verify)"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Currency code/symbol present; \"incl./excl. GST\" token"
    severity: "Warn"
    override: none
    evidence: "Tax config"
    remediation_message: "\"State the currency and whether tax is included.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-013
    obligation: "Bid and tender drafts (AppNAI) shall not contain any commitment, price, timeline or compliance declaration not approved by a person, and AI shall never submit a bid"
    citation: "DEC-064; BRL-BID-02; safety invariant"
    applies_to: "DOC · AppNAI"
    check: "deterministic"
    detection: "Bid draft commitment spans → each term_id + reviewer; submission action by AI → Block"
    severity: "Block"
    override: none
    evidence: "Bid approval"
    remediation_message: "\"Every bid commitment must be approved by a person; AI cannot submit bids.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-014
    obligation: "Product-quality, origin and certification claims for goods (e.g. \"certified organic\", \"Jaivik Bharat\", \"NPOP certified\", grade, moisture, origin) shall be backed by a valid certificate or lab report linked as an approved claim"
    citation: "FSSAI (Organic Foods) Regulations 2017 (VR-35); CPA s.2(28)"
    applies_to: "ALL · OrganicSpec"
    check: "deterministic"
    detection: "PL-COMMIT-05 → certificate_id valid on dispatch date"
    severity: "Block"
    override: none
    evidence: "Certificate"
    remediation_message: "\"Attach the valid certificate before claiming organic or quality grades.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-015
    obligation: "Response-time promises in replies (\"we will call you within the hour\") shall be made only where the owning team's operating calendar supports them"
    citation: "CPA s.2(28); BRL-ELG-08"
    applies_to: "EM, WA, CH · ALL"
    check: "deterministic_then_ai_review"
    detection: "Duration tokens in replies → team calendar capacity check"
    severity: "Warn"
    override: r10_with_reason
    evidence: "Calendar"
    remediation_message: "\"Avoid promising a response time the team cannot meet.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-016
    obligation: "Free trials and \"no cost\" statements shall match the entitlement configuration, including duration, limits and conversion to paid"
    citation: "DEC-502; RP-IN-ADV-009; ROSCA"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Trial tokens → entitlement_plan match"
    severity: "Block"
    override: none
    evidence: "Entitlement record"
    remediation_message: "\"Trial wording must match the configured trial.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-017
    obligation: "The same offer sent to multiple recipients in one campaign shall be identical in its commitments, except for approved personalisation fields"
    citation: "AU-122 grouped approval (DEC-745)"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "Commitment spans hashed per item; outliers flagged"
    severity: "Warn"
    override: none
    evidence: "Packet hash"
    remediation_message: "\"Commitments differ between recipients; review the outliers.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-018
    obligation: "Commitments in Hindi, other Indian languages and code-mixed text shall be detected and backed in the same way"
    citation: "DEC-026; G-8"
    applies_to: "ALL · ALL"
    check: "deterministic_then_ai_review"
    detection: "PL-COMMIT-01 Hindi terms; numeral normalisation (Devanagari digits)"
    severity: "Block"
    override: r10_with_reason
    evidence: "As rule 001"
    remediation_message: "\"This promise in {language} needs an approved term.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-019
    obligation: "Warranties or guarantees of performance, efficacy or life of a product or service shall not be given unless based on an adequate or proper test and approved as a term"
    citation: "CPA s.2(47) (false warranty, verify sub-clause)"
    applies_to: "ALL · ALL"
    check: "deterministic_then_ai_review"
    detection: "\"warranty\", \"guarantee\", \"lasts\", \"assured\" → term_id type warranty"
    severity: "Block"
    override: r10_with_reason
    evidence: "Warranty term and test basis"
    remediation_message: "\"Warranties need an approved term backed by a test.\""
    effective_from: null  # set at sign-off
  - id: RP-COMMIT-020
    obligation: "Content shall not offer, solicit or refer to investment, fundraising, securities, returns on investment in the startup, or investor opportunities"
    citation: "DEC-002; BRL-TEN-12"
    applies_to: "ALL · ALL"
    check: "deterministic"
    detection: "PL-COMMIT-06"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"This product does not support investment or fundraising content.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-COMMIT-01
    name: "Commitment markers"
    match: "regex with number/date capture"
    severity: "Triggers rule 001"
    used_by: "001, 018"
    terms:
      - "deliver by"
      - "delivered within"
      - "in {n} days"
      - "lead time"
      - "we will"
      - "we commit"
      - "guaranteed"
      - "assured"
      - "refund"
      - "money-back"
      - "SLA"
      - "uptime"
      - "within {n} hours"
      - "discount"
      - "% off"
      - "free"
      - "warranty"
      - "penalty"
      - "डिलीवरी"
      - "दिनों में"
      - "गारंटी"
      - "पक्का"
      - "रिफ़ंड"
      - "छूट"
      - "मुफ़्त"
      - "वारंटी"
  - id: PL-COMMIT-02
    name: "Outcome guarantees"
    match: "phrase"
    severity: "Block"
    used_by: "004"
    terms:
      - "guaranteed leads"
      - "guaranteed ROI"
      - "guaranteed revenue"
      - "guaranteed growth"
      - "double your sales"
      - "assured returns"
      - "risk-free results"
      - "पक्के लीड"
      - "गारंटीड मुनाफ़ा"
      - "बिक्री दोगुनी"
  - id: PL-COMMIT-03
    name: "Legal terms in marketing"
    match: "phrase"
    severity: "Block"
    used_by: "008"
    terms:
      - "liability"
      - "indemnify"
      - "indemnity"
      - "exclusive rights"
      - "governing law"
      - "jurisdiction of courts"
      - "liquidated damages"
      - "penalty clause"
      - "IP ownership"
      - "दायित्व"
      - "क्षतिपूर्ति"
      - "अनन्य अधिकार"
  - id: PL-COMMIT-04
    name: "Offer language"
    match: "phrase"
    severity: "Block unless approved quote"
    used_by: "009"
    terms:
      - "we hereby offer"
      - "reply YES to accept"
      - "this quote is binding"
      - "deemed accepted"
      - "accept by replying"
      - "hereby agree"
      - "हम एतद्द्वारा प्रस्ताव करते हैं"
      - "स्वीकार करने के लिए YES लिखें"
  - id: PL-COMMIT-05
    name: "Quality and origin claims"
    match: "phrase"
    severity: "Block without certificate"
    used_by: "014"
    terms:
      - "certified organic"
      - "100% organic"
      - "Jaivik Bharat"
      - "NPOP"
      - "India Organic"
      - "chemical-free"
      - "pesticide-free"
      - "Grade A"
      - "प्रमाणित जैविक"
      - "रसायन मुक्त"
  - id: PL-COMMIT-06
    name: "Investment and fundraising"
    match: "phrase"
    severity: "Block"
    used_by: "020"
    terms:
      - "invest in us"
      - "investment opportunity"
      - "equity"
      - "shares"
      - "fundraising"
      - "investor deck"
      - "assured returns on investment"
      - "निवेश का अवसर"
      - "शेयर"
```

### 11.15.14.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-COMMIT v0.1-draft → proposed v1.0 |
| Reviewer (name, enrolment no.) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Opinion on offer vs invitation-to-treat wording (rule 009) | _______________________ |
| CPA s.2(47) sub-clause references confirmed | ☐ |
| FSSAI organic labelling reference confirmed (VR-35) | ☐ |
| Hindi wording reviewed by | _______________________ |
| Conditions | _______________________ |
| Next review due | ____ / ____ / ______ |
| R10 approval / signatures | _______________ / _______________ |

---

## 11.15.15 Pack summary, applicability matrix and counsel confirmation list

### 11.15.15.1 Rules per pack

| Pack | Rules | Block | Warn | DET | AI | DET+AI | Phrase lists | Templates | Tests | Languages of templates |
|---|---|---|---|---|---|---|---|---|---|---|
| RP-IN-ADV | 22 | 19 | 3 | 11 | 3 | 8 | 7 | 9 | 15 | en, hi |
| RP-IN-SMS | 20 | 19 | 1 | 19 | 0 | 1 | 3 | 5 | 13 | en, hi |
| RP-IN-DPDP | 21 | 16 | 5 | 18 | 1 | 2 | 3 | 6 | 13 | en, hi |
| RP-IN-WA | 20 | 19 | 1 | 16 | 0 | 4 | 3 | 5 | 12 | en, hi |
| RP-EU-AI | 17 | 15 | 2 | 13 | 1 | 3 | 3 | 6 | 11 | en (de, fr pending) |
| RP-EU-MKT | 20 | 18 | 2 | 18 | 1 | 1 | 3 | 6 | 11 | en (de, fr pending) |
| RP-US-EMAIL | 20 | 18 | 2 | 14 | 2 | 4 | 3 | 6 | 10 | en |
| RP-PLAT-ADS | 20 | 17 | 3 | 15 | 1 | 4 | 4 | 4 | 12 | en, hi |
| RP-HEALTH | 20 | 18 | 2 | 10 | 2 | 8 | 6 | 4 | 12 | en, hi |
| RP-EDU-MINORS | 20 | 19 | 1 | 16 | 2 | 2 | 4 | 5 | 12 | en, hi |
| RP-COMMIT | 20 | 16 | 4 | 12 | 0 | 8 | 6 | 5 | 12 | en, hi |
| **Total** | **220** | **194** | **26** | **162** | **13** | **45** | **45** | **61** | **133** | — |

### 11.15.15.2 Applicability matrix (CP-01)

| Pack | EM | WA | SMS/VO | SO | AD | LP/FM | MD | CH | DOC | Jurisdiction trigger | Startup trigger |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RP-IN-ADV | ● | ● | ● | ● | ● | ● | ● | ○ | ● | IN recipient/target or IN sender | All |
| RP-IN-SMS | — | — | ● | — | — | — | — | — | — | +91 numbers | All |
| RP-IN-DPDP | ● | ● | ● | ○ | ● | ● | — | ● | ● | IN data principals | All |
| RP-IN-WA | — | ● | — | — | — | ○ | ● | ● | — | All (platform policy) | All |
| RP-EU-AI | ● | ● | ● | ● | ● | ● | ● | ● | ● | EU/EEA | All |
| RP-EU-MKT | ● | ● | ● | ● | ● | ● | — | ○ | ● | EU/EEA (UK blocked) | All |
| RP-US-EMAIL | ● | ● | ● | ○ | ○ | ○ | — | — | — | US | All |
| RP-PLAT-ADS | — | — | — | ○ | ● | ● | ● | — | — | All where ads run | All |
| RP-HEALTH | ● | ● | ● | ● | ● | ● | ● | ● | ● | All | MedMaarg, health offerings |
| RP-EDU-MINORS | ● | ● | ● | ● | ● | ● | ● | ● | ● | All | EduVerse, education offerings, age < 18 or unknown |
| RP-COMMIT | ● | ● | ● | ● | ● | ● | ○ | ● | ● | All | All |

● applies · ○ applies to part of the channel (e.g. boosted posts, chat replies) · — not applicable.

### 11.15.15.3 What counsel must still confirm (consolidated)

| # | Item | Packs | Counsel |
|---|---|---|---|
| C-01 | Read every VR entry marked verified against the primary text (government gazette, Official Journal, CFR, platform pages) and every entry marked "verify" | All | All counsel |
| C-02 | DPDP: interpretation of s.3(c)(ii) for B2B outreach; s.7 legitimate uses; DPDP Rules numbering; VPC mechanism under Rule 10; grievance timelines | RP-IN-DPDP, RP-EDU-MINORS | India |
| C-03 | TCCCPR: header-suffix scheme, consent validity, opt-out text, legal time window, revocation timeline, whitelisting and variable-tagging directions, RCS treatment, status of the draft Third Amendment | RP-IN-SMS | India telecom |
| C-04 | CCPA guideline clause numbers (2022, 2023 dark patterns, 2024 coaching); ASCI Code clause numbers; status of ASCI AI-labelling guidelines | RP-IN-ADV, RP-EDU-MINORS | India advertising |
| C-05 | DMR Act section numbers and current Schedule; Sch. J; AYUSH advertisement rules; NMC endorsement rule | RP-HEALTH | India health |
| C-06 | Whether the platform is an "intermediary" or SGI tool provider under the IT Amendment Rules 2026 | RP-IN-ADV | India technology |
| C-07 | AI Act Art. 50 dates and Digital Omnibus citation in the Official Journal; provider/deployer allocation; sufficiency of C2PA and text marking | RP-EU-AI | EU |
| C-08 | Member-state B2B email profiles; tracking-pixel consent positions; Art. 27 representative | RP-EU-MKT | EU |
| C-09 | CAN-SPAM, 16 CFR 255/316/465 references; multi-advertiser sender designation; state law; TCPA position | RP-US-EMAIL | US |
| C-10 | Platform policy versions (Meta WhatsApp, Google, Meta, LinkedIn) with retrieval dates; WhatsApp opt-in scope; AI chatbot terms | RP-IN-WA, RP-PLAT-ADS | Platform-policy specialist |
| C-11 | Offer vs invitation to treat; CPA s.2(47) warranty sub-clause; FSSAI organic labelling | RP-COMMIT | India commercial |
| C-12 | Hindi (and German/French) legal translations of every template | All with templates | Legal translators [GAP-996] |

---

## 11.15.16 Effect on GAP-980

**GAP-980 ("legal content of the 11 rule packs needs counsel authoring"): drafted; pending counsel sign-off.**

| Element of GAP-980 | Status after this part |
|---|---|
| Legal content of the 11 packs | **Drafted** as v0.1-draft: 220 rules with obligation wording, citations, applicability, check type, detection logic, severity, evidence and remediation; phrase lists, templates (English and Hindi for India-facing packs), exceptions, AG-086 guidance, tests and AU-128 YAML |
| Counsel authoring and sign-off | **Pending.** Sign-off blocks are ready per pack; C-01…C-12 list what counsel must confirm. No pack can be activated until signed (FR-V12-M-028; ADR-184; DEC-761) |
| Quarterly upkeep | Procedure Q-REV defined (§11.15.3.5); cost line M-R5 unchanged (Part 11.13b) |
| Quotes for counsel work (M-D4) | Still to obtain; the drafts should reduce counsel effort towards the low end of M-D4 (₹1.00–2.75 L, verify by quotes) [RECOMMENDATION-997] |

GAP-980 remains **open** in the Part 11.13 register until all 11 sign-off blocks are completed; it is reduced from "authoring" to "review and sign-off".

---

## 11.15.17 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-761 | Adopt the 11 rule packs in this part as **v0.1-draft** counsel-review drafts. Every pack stays in state `draft` and cannot contribute to a `pass` until counsel signs its block and R10 approves it in AU-128; outbound in affected markets is held meanwhile | Expert drafting, Founder instruction 28 Nov 2026 | Implements FR-V12-M-028 and ADR-184; reduces GAP-980 to review and sign-off |
| DEC-762 | Cross-pack precedence: applicability set CP-01, all packs must pass CP-02, **strictest wins** CP-03, platform rules are a floor CP-04, **fail closed** CP-05, exceptions only as written CP-06, safety invariants override everything CP-07 | Expert drafting, Founder instruction 28 Nov 2026 | Binding evaluation semantics for AU-128 and AG-086 |
| DEC-763 | Pack expiry at last counsel review + 120 days with automatic suspension (HOLD), quarterly review Q-REV and event-driven review within 10 business days | Pending counsel sign-off | Fail-closed expiry for every pack [RECOMMENDATION-998] |
| DEC-764 | Jurisdiction detection J1–J7 with union of signals, strictest EU member-state profile when unknown, and Block on no signal | Expert drafting, Founder instruction 28 Nov 2026 | Implements BRL-ELG-05 deterministically |
| DEC-765 | Platform labelling and commitment defaults that are stricter than some laws: (a) AI-generated content is labelled in **all** markets (not only the EU); (b) unbacked prices, discounts, refunds, guarantees **and delivery dates** are Block (tightening the `fix` shown in the Part 11.13b Gherkin scenario); (c) the platform quiet window (BRL-ELG-08) governs promotional SMS even where TRAI allows more | Pending counsel sign-off | Tightens AG-086 and AU-128 behaviour; no invariant weakened |

---

## 11.15.18 Tags register

| Tag | Type | Statement | Where used | Owner / resolution |
|---|---|---|---|---|
| ASSUMPTION-994 | Assumption | For owned startups the startup is advertiser, sender and data fiduciary; for SaaS tenants the tenant is controller/fiduciary and the platform processor (BR-V7-CJ-11). An "active" pack certifies the platform's controls only, not a tenant's compliance | §11.15.1; all packs | R10; counsel to confirm in tenant terms |
| GAP-995 | Gap | Primary government and regulator sites could not be fetched from this environment; verification relied on secondary sources; clause numbers of ASCI Code, CCPA guidelines, DMR Act, DPDP Rules and TCCCPR need primary-text checks | §11.15.2 VR register | Counsel (C-01) before sign-off |
| GAP-996 | Gap | Hindi (and German/French) template wording needs certified legal translation and counsel review; other Eighth-Schedule languages (DEC-026: ta, or) not yet drafted | Templates in all India-facing packs; RP-EU-AI | R10 with legal translators before activation |
| RECOMMENDATION-997 | Recommendation | Engage counsel in three lots following ADR-184 order: (1) India firm for RP-IN-ADV, RP-IN-SMS, RP-IN-DPDP, RP-HEALTH, RP-EDU-MINORS, RP-COMMIT plus a platform-policy specialist for RP-IN-WA and RP-PLAT-ADS; (2) EU counsel for RP-EU-AI and RP-EU-MKT; (3) US counsel for RP-US-EMAIL when the US market is prioritised; use these drafts to fix-scope the quotes for M-D4 | §11.15.16 | R10 / Founder |
| RECOMMENDATION-998 | Recommendation | Expire every pack 120 days after its last counsel review and suspend automatically (HOLD), with T-30/T-14/T-3 reminders | §11.15.3.5; DEC-763 | R10 |
| GAP-999 | Gap | Open legal questions needing counsel opinion before activation: DPDP s.3(c)(ii) for B2B outreach; TCCCPR promotional time window and amendment details; platform's status under the IT SGI Rules 2026; AI Act provider/deployer allocation with the model provider | RP-IN-DPDP-002 E-2; RP-IN-SMS-009; VR-09; RP-EU-AI E-6 | Counsel (C-02, C-03, C-06, C-07) |

---

## 11.15.19 Quality gate (Batches 11.15a, 11.15b and 11.15c)

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every rule cites a statute, regulation, guideline, platform policy or blueprint ID (BRL-, DEC-, CJ-, BR-V7-, FR-V12-); platform-policy tightenings cite the BRL or DEC they implement |
| 2 | Assumptions, gaps and conflicts tagged and logged | Pass | 6 tags, ASSUMPTION/RECOMMENDATION/GAP-994…999 only, in §11.15.18; no CONFLICT tag needed (DEC-765 tightens, does not conflict) |
| 3 | IDs unique and consistent with earlier parts | Pass | Rule, list, template and test IDs are pack-local and new; DEC-761…765 unused before (checked by grep); references to AU-128, AG-086, WF-46, TL-09/27/37, API-V12-M-09, FR-V12-M-027…033 match Part 11.13 |
| 4 | No story lacks AC and no requirement lacks a test | Pass (N/A for stories) | No new stories; every pack has positive and negative tests for its key rules (TC-RP-…); full rule coverage is delivered by the AG-086 golden set (600 drafts, Part 11.13b) extended per pack at Q5 |
| 5 | Negative, edge, security and accessibility cases covered | Pass | Negative and edge cases in every pack; security cases (prompt data leakage RP-IN-DPDP-015, RP-EDU-MINORS-005; credential requests RP-IN-SMS-020, RP-IN-WA-006); accessibility of AI disclosures (RP-EU-AI-006) |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | N/A | No new agent; AG-086 contract G-1…G-9 strengthens existing guardrails; fallback per CP-05 |
| 7 | Time-sensitive facts flagged "verify" with an as-of date | Pass | Verification register VR-01…40 with "verified as of 28 Nov 2026, source" or "verify at time of implementation"; primary-text check outstanding (GAP-995) |
| 8 | No restricted data routed to free-tier models | Pass | RP-IN-DPDP-015 and RP-EDU-MINORS-005 block personal and minor data in prompts and any Tier 2 use (DEC-418, BRL-AI-06) |
| 9 | Consistent with earlier parts | Pass | DEC-029 as amended by DEC-507/ADR-184 (EU, UK, US gated); DEC-030 (no minors); MedMaarg no therapeutic claims or patient data; DEC-064 L1 caps; DEC-744 no outcome guarantees; DEC-418 Claude primary. Observation (not fixed here): Part 11.13b Gherkin "Unbacked commitment is flagged" expects `fix`; DEC-765 proposes Block for delivery dates; Part 11.13b to be aligned if DEC-765 is approved |

**Status: Part 11 Batch 11.15 complete (11.15a, 11.15b, 11.15c). 11 rule packs drafted as v0.1-draft for counsel review, with rules, phrase lists, approved template wording (English, plus Hindi for India-facing packs), exceptions, AG-086 guidance, tests, AU-128 YAML and sign-off blocks; cross-pack precedence, jurisdiction detection and quarterly review defined; GAP-980 drafted, pending counsel sign-off; 5 decisions (DEC-761…765) and 6 tags (994–999). This is a draft for review by qualified counsel, not legal advice; nothing goes live until counsel signs off (FR-V12-M-028).**
