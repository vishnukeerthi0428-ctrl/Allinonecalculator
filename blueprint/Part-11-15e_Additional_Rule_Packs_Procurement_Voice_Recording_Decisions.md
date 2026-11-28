# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.15e), Additional Rule Packs: Procurement, AI Voice and Call Recording; Decisions (Draft Legal Wording for Counsel Review)

| Field | Value |
|---|---|
| Document | Part 11, Batch 11.15e of 11.15d–11.15e. Holds §11.15.29 to §11.15.41: **RP-IN-PROC, RP-EU-PROC, RP-US-PROC, RP-IN-VOICE, RP-US-VOICE, RP-EU-VOICE (with UK profile), RP-AE-VOICE, RP-GL-RECORDING**, the pack summary and applicability matrix, the counsel confirmation list, the effect on GAP-1044 and GAP-1046 (and on GAP-1067, GAP-1068, RECOMMENDATION-1073), decisions DEC-766…769, the tags register and the quality gate. Framework additions, VR-41…77 and the payment and agent-commerce packs are in file d (`Part-11-15d_Additional_Rule_Packs_Payments_AgentCommerce_Procurement_Voice.md`) |
| Version | 1.0 · 28 Nov 2026 (document). Every rule pack inside is **v0.1-draft** |
| Baseline | As file d |
| Roles applied | As file d |
| ID ranges used | As file d |

> **DISCLAIMER: DRAFT FOR REVIEW BY QUALIFIED COUNSEL. THIS IS NOT LEGAL ADVICE.**
> This part is a **drafting aid** prepared by an expert panel for the product team. It is **not** a legal opinion and must not be relied on as legal advice by anyone. Every rule, citation, threshold, effective date, template, model clause and phrase list is a **proposal** for review, correction and sign-off by qualified counsel admitted in the relevant jurisdiction. **No pack in this part may be published, activated or used as the reason an action is allowed until counsel has signed it off and R10 Legal/Compliance has approved it in AU-128** (FR-V12-M-028; ADR-184; DEC-776; MC-10). Until then every pack is in state `draft`: the mandate engine returns HOLD `JURISDICTION_PACK_NOT_APPROVED` (PDP rule 2, Part 11.17a §11.17.5.12) and voice returns `VOICE_NOT_ACTIVE_FOR_JURISDICTION` (Part 11.18a §11.18.5.1). Capabilities are **built** and tested against synthetic packs (`RP-*-syn`), and **activate per jurisdiction only when the pack is approved**. No control in this part is optional.

---

## 11.15.29 RP-IN-PROC: India public procurement: GFR 2017, GeM, CPPP/GePNIC, DSC signing and bidder integrity

### 11.15.29.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-IN-PROC |
| Title | Bids to Indian public buyers: eligibility and registration, portal capability, digital signature certificates, bid security, mandatory declarations, integrity and anti-collusion, deadlines, two-envelope handling, receipts |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | IN (procuring entity of the Government of India, a state government, a PSU or other public body; portal in India) |
| Channels | BID (bid package, portal submission, receipt), DOC (declarations) |
| Audiences | GOV (public buyers) |
| Startups | AppNAI (primary), OrganicSpec, any startup bidding; Tenant |
| Mandate types gated | MT-BID (AUTO mode); assisted and manual modes also checked |
| Legal sources | General Financial Rules 2017 Rules 144, 149, 151, 154–155, 159–160, 170, 173, 175 as amended (incl. OM F.1/3/2024-PPD of 10 Jul 2024 and 2025 limits) (VR-57); Manual for Procurement of Goods / Consultancy / Other Services (DoE, verify current edition); GeM General Terms and Conditions (current version, verify) (VR-58); CPPP / GePNIC bidder terms and Class III DSC requirement (VR-59); IT Act 2000 s.3A, s.5, s.35 and CCA guidelines (VR-52, VR-59); Public Procurement (Preference to Make in India) Order 2017 as revised (verify); DoE Order of 23 Jul 2020 on bidders from countries sharing a land border (verify); MSE Procurement Policy Order 2012 and startup relaxations (verify); Competition Act 2002 s.3(3)(d) (bid rigging) (verify); Prevention of Corruption Act 1988 (verify). Platform: DEC-781, DEC-851, DEC-852, BRL-BID-01…06, §11.17.7 |
| Effective dates | GFR as amended to date (verify latest OM); GeM GTC version current at submission (verify) |
| Owner | R10 Legal/Compliance with R06 Bid Manager |
| Review cadence | Quarterly + every GFR OM, GeM GTC version and portal change |
| Expiry / fail-closed | 120 days; while not `active` every Indian tender is MANUAL (L1) with evidence recording only |
| Depends on | RP-COMMIT (bid content), RP-IN-AGENTCOM (signatures), RP-IN-DPDP (personal data in bids) |

### 11.15.29.2 Plain-language summary

1. The bidding company registers on GeM or the CPPP portal in its own legal name. The platform never owns the bidder account.
2. GeM and NIC portals are treated as assisted-only. The system pre-fills and checks the upload, and a person signs with their own Class III digital signature certificate and clicks submit. AUTO applies only where counsel records that a portal's terms allow automated or API submission.
3. The system never holds or uses a person's DSC or PIN.
4. Every declaration (Make in India local content, land-border country, no debarment, integrity, MSE or startup status) is made by an authorised person and not written by AI.
5. Two portfolio startups may not bid on the same tender without Legal clearance, and no bid information passes between them.
6. Reverse auctions are always live human bidding.
7. Submissions must finish before the portal's closing time, which is authoritative. The receipt is stored.

### 11.15.29.3 Definitions

| Term | Definition for this pack |
|---|---|
| GeM | Government e-Marketplace; procurement of common-use goods and services available on GeM is mandatory for central government buyers (GFR Rule 149, VR-57) |
| CPPP / GePNIC | Central Public Procurement Portal (eprocure.gov.in) running the NIC Government e-Procurement System; state NIC portals use the same system |
| DSC | Digital signature certificate issued by a licensed certifying authority under the IT Act; e-procurement typically requires a Class III certificate with signing and encryption keys (VR-59) |
| Bid security / EMD | Earnest money deposit or a bid-securing declaration accepted in lieu (GFR Rule 170, verify) |
| e-RA | Electronic reverse auction |
| Integrity pact | Pre-bid agreement between procuring entity and bidders on ethical conduct, required for specified tenders (verify) |

### 11.15.29.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-IN-PROC-001 | A bid shall be submitted only from a portal account registered in the legal name of the bidding company (GeM seller ID, CPPP bidder enrolment), administered by an authorised officer of that company, whose registration is active on the submission date | GeM GTC (registration) (VR-58); CPPP bidder enrolment (VR-59); BRL-BID-06 | BID · GOV | DET | `portal_account.owner_legal_entity = bid.bidder_legal_entity` AND `status = active` (checked ≤ 24 h before submit) | Block | Portal account record | "The portal account is not registered to this company or is not active." |
| RP-IN-PROC-002 | AUTO submission shall be used on a portal only if the portal capability registry records, from counsel's review of the portal's current terms, that automated or API submission is permitted; GeM, CPPP/GePNIC and state NIC portals default to ASSISTED_ONLY and any unreviewed portal to MANUAL_ONLY | GeM GTC (compliance; suspension for breach of terms) (VR-58); GFR Rule 149 (VR-57); FR-V12-P-118…122; GAP-1045 [GAP-1168] | BID · GOV | DET | `portal_profile.capability ∈ {API_PERMITTED, AUTOMATION_PERMITTED}` AND `counsel_review.date` ≤ 120 d; else mode = ASSISTED/MANUAL | Block | Portal capability record | "This portal does not permit automated submission. Use assisted or manual submission." |
| RP-IN-PROC-003 | Bids shall be signed with the Class III DSC (or the signature method the portal prescribes) of the company's authorised signatory, operated only by that person; the platform shall never store, hold, export or operate a personal DSC, token or PIN | IT Act s.3A, s.5, s.35 (VR-52, VR-59); §11.17.7.5; FR-V12-P-124 | BID · GOV | DET | Assisted session: signing happens on the signatory's device; no DSC/PIN field in any platform schema; HSM key use for bids only if rule 2 portal row allows an organisational certificate | Block | Assisted-session log | "Only the authorised signatory can sign this bid with their own DSC." |
| RP-IN-PROC-004 | The signatory's authority (board resolution or power of attorney) shall be on file, unexpired and matching the name on the DSC and the portal account | GFR procurement manuals (authorised signatory) (verify) | BID, DOC · GOV | DET | `authority_doc.signatory = dsc.subject_name` AND `valid_until > deadline` | Block | Authority document | "Upload a valid authority document for this signatory." |
| RP-IN-PROC-005 | Bid security (EMD) evidence or a bid-securing declaration, or a valid exemption certificate (MSE/startup) accepted by the tender, shall be attached before submission | GFR Rule 170 (verify); MSE Procurement Policy (verify) | BID · GOV | DET | Tender requires EMD → `emd_ref` or `bsd_doc` or `exemption_cert` with validity | Block | EMD/BSD/exemption document | "Bid security or a valid exemption is missing." |
| RP-IN-PROC-006 | Every statutory or tender declaration (local content under the Make in India order, land-border-country eligibility, non-debarment, no conflict of interest, integrity pact, MSE/startup status, turnover, past performance) shall be made from source records and approved by the authorised signatory; AI may extract and cross-check but shall not author or alter a declaration | PPP-MII Order 2017 (verify); DoE Order 23 Jul 2020 / GFR Rule 144(xi) (verify); GFR Rule 175 (code of integrity) (verify); BRL-AI-07 amended | BID, DOC · GOV | DET | Declaration fields bound to source records; `approved_by` = signatory; AG-206/207 edits on declaration blocks rejected | Block | Signed declarations | "Declarations must come from records and be approved by the signatory." |
| RP-IN-PROC-007 | MSE or startup preferences and exemptions shall be claimed only with a valid Udyam registration or DPIIT recognition for the relevant category | MSE Procurement Policy Order 2012 (verify); DPIIT startup relaxations (verify) | BID · GOV | DET | `claim.msme` → Udyam number verified; `claim.startup` → DPIIT certificate | Block | Certificate | "This preference needs a valid Udyam or DPIIT certificate." |
| RP-IN-PROC-008 | Where two or more companies of the same tenant (or of the Owner Portfolio) intend to bid in the same tender, no bid shall proceed without written clearance by R10 and counsel, and bid information shall be walled between them | Competition Act 2002 s.3(3)(d) (bid rigging) (verify); GFR Rule 175 (verify); BRL-SRC-10 | BID · GOV | DET | `tender_id` shared across companies of one tenant/portfolio → HOLD `AFFILIATE_BID_CLEARANCE`; RLS wall on bid data | Block | Clearance record | "Another company in the group is bidding on this tender. Legal clearance is needed." |
| RP-IN-PROC-009 | Bid documents shall be genuine and unaltered; certificates and financial statements shall be the issued versions; any discrepancy found by the cross-check shall stop submission | GFR Rule 151 (debarment) and 175 (verify); Indian Penal Code / BNS forgery provisions (verify) | BID, DOC · GOV | DET+AI | DET: file hashes vs document vault originals; AI (AG-207): inconsistent figures, dates, names | Block | Cross-check report | "A document does not match its original or other bid data." |
| RP-IN-PROC-010 | The bid price and commercial terms submitted shall equal the MT-BID approved price and terms bound to the package hash; participation in a reverse auction or any live price revision shall be performed by an authorised person only | DEC-781; DEC-851; BRL-BID-03 | BID · GOV | DET | `package_hash = mandate.package_hash`; tender stage `e_ra` → MANUAL | Block | Package hash | "The price differs from the approved package, or this is a reverse auction that needs a person." |
| RP-IN-PROC-011 | Submission shall complete before the closing time shown by the portal (portal server time authoritative); automated attempts shall respect the automation buffer and hard-stop buffer | BRL-BID-01 as amended; DEC-852; AU-278 | BID · GOV | DET | Deadline guard B_auto/B_hard; portal clock offset measured at session start | Block | Guard log | "Too close to the deadline for an automated attempt. A person must submit." |
| RP-IN-PROC-012 | During the tender process the bidder shall communicate with the procuring entity only through the channels the tender designates (pre-bid meeting, portal clarification), and no agent shall contact officials of the procuring entity | GFR Rule 175 (verify); integrity pact (verify); Prevention of Corruption Act (verify) | EM, VO, BID · GOV | DET+AI | DET: outbound to procuring-entity domains blocked except designated clarification channel; AI: improper inducement language | Block | — | "Contact with the buyer is only allowed through the tender's clarification channel." |
| RP-IN-PROC-013 | Financial (commercial) envelopes shall stay encrypted and unopened until upload; the system shall not expose prices to anyone outside the MT-BID approvers before the bid opening | Two-envelope tender rules (verify); §11.17.7.2 | BID · GOV | DET | Tender data key access limited to AU-279 and approvers; access log | Block | Access log | "Commercial envelope access is restricted until submission." |
| RP-IN-PROC-014 | A portal acknowledgement (bid ID, timestamp, tender ID) shall be captured and verified for every submission and stored with object lock; withdrawal or modification shall be performed only by an authorised person | FR-V12-P-125, 131; DEC-851 | BID · GOV | DET | Receipt verification rules (§11.17.7.7) | Block | Receipt artefact | "No verified portal receipt. Check the portal before any further action." |
| RP-IN-PROC-015 | The platform shall not scrape or access portals in a way their terms forbid; tender discovery shall use public listings, RSS feeds or licensed data feeds only | GeM GTC and CPPP terms (verify) (VR-58, VR-59) | BID · GOV | DET | Discovery adapter allowlist per portal | Block | Adapter config | "This discovery method is not permitted for this portal." |
| RP-IN-PROC-016 | Bid records (package, approvals, declarations, receipts, correspondence) shall be retained for at least 8 years or the contract period plus the audit period, whichever is longer | MC-24; GFR record-keeping (verify) | BID · GOV | DET | Retention class `bid_8y` | Block | Evidence pack | "Bid records must be retained." |

**Pack parameters (loaded by AU-128 and read by the PDP, AU-264/272/278/280/281/282; every value "verify at time of implementation, as of 28 Nov 2026" unless its VR entry is verified).**

| Parameter | Draft value | Source / note |
|---|---|---|
| gem_capability_default | ASSISTED_ONLY | VR-58 (no automation clause found; counsel review pending) |
| cppp_capability_default | ASSISTED_ONLY | VR-59 |
| unreviewed_portal_capability | MANUAL_ONLY | FR-V12-P-118 |
| dsc_class_required | Class III (signing + encryption) unless portal states otherwise | VR-59 (verify) |
| reverse_auction_mode | MANUAL (human) | Platform policy |
| automation_buffer_hours | 6 | DEC-852 [ASSUMPTION-1053] |
| hard_stop_buffer_hours | 2 | BRL-BID-01 |
| retention_years | 8 | MC-24 |

### 11.15.29.5 Required disclosures and approved template wording

| Template | Use | English (approved draft wording) | Hindi | Placement |
|---|---|---|---|---|
| TPL-IN-PROC-01 | Assisted-session instruction to the signatory | "The sealed package {package_hash_prefix} is pre-filled on {portal}. Check the uploaded files show 'verified' below, then sign with your own DSC and press Submit. The system cannot sign for you." | "सील किया गया पैकेज {package_hash_prefix} {portal} पर पहले से भरा गया है। नीचे सभी फ़ाइलें 'सत्यापित' दिखें, फिर अपने DSC से हस्ताक्षर करें और सबमिट दबाएँ। सिस्टम आपकी ओर से हस्ताक्षर नहीं कर सकता।" | A268 assisted session |
| TPL-IN-PROC-02 | Declaration approval prompt | "You are confirming, as authorised signatory of {company}, that each declaration below is true and complete based on the attached records. False declarations can lead to debarment and prosecution." | "{company} के अधिकृत हस्ताक्षरकर्ता के रूप में आप पुष्टि कर रहे हैं कि नीचे दी गई प्रत्येक घोषणा संलग्न अभिलेखों के आधार पर सत्य और पूर्ण है। झूठी घोषणा से प्रतिबंध और अभियोजन हो सकता है।" | Before signing |

### 11.15.29.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-IN-PROC-01 | Improper inducement / contact | speed money; facilitation; take care of the officer; inside information; know the evaluation committee; arrange approval; सेटिंग; अंदर की जानकारी | phrase + AI | Block | 012 |
| PL-IN-PROC-02 | Affiliate coordination | our sister company will quote; cover bid; we will quote higher; split the lots; rotate L1 | phrase + AI | Block | 008 |

**Prohibited (absolute, no mandate, exception or override can unlock):** holding or operating a personal DSC; AI-authored declarations; automated reverse-auction bidding; contacting officials outside designated channels; affiliate bids without clearance; scraping portals.

### 11.15.29.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Private buyer e-mail RFQ from a PSU's commercial arm that is not a public tender | Treated as private (RP-GL-AGENTCOM/RP-IN-AGENTCOM), unless the RFQ cites GFR/tender rules → this pack |
| E-2 | Portal with a documented vendor API (some state/PSU portals) | AUTO only after counsel records API terms (rule 002) |
| E-3 | Tender requiring physical submission of documents | MANUAL; system prepares the checklist |
| E-4 | GeM direct purchase (L1 buy without bidding) | Seller-side order acceptance on GeM is a GeM order; acceptance by an authorised person (L1/L2) under GeM GTC |

### 11.15.29.8 AI reviewer review guidance (RP-IN-PROC)

- **Reviewer:** AG-207 (bid compliance cross-checker) and AG-206 (package assembler), applying the AG-086 contract; AG-208 for receipts.
- **Look for:** inconsistencies between declarations and source documents; improper contact; affiliate coordination; altered certificates.
- **Cite:** `RP-IN-PROC-0NN` and the pack version only; quote the document, page and span.
- **Escalate (`needs_counsel`):** any land-border-country or local-content uncertainty; any affiliate overlap; any doubt about document authenticity.
- **Never:** write or edit a declaration; decide eligibility; operate a portal.

### 11.15.29.9 Test cases

| ID | Rule | Type | Input (summary) | Expected |
|---|---|---|---|---|
| TC-RP-IN-PROC-01 | 002 | Negative | GeM tender, MT-BID Active, capability ASSISTED_ONLY | Mode ASSISTED; no AUTO call |
| TC-RP-IN-PROC-02 | 002 | Negative | New state portal never reviewed | Mode MANUAL |
| TC-RP-IN-PROC-03 | 003 | Security | Attempt to upload DSC .pfx and PIN to vault | Rejected; security event |
| TC-RP-IN-PROC-04 | 006 | Negative | AG-206 proposes edited local-content percentage | Edit rejected; declaration from records only |
| TC-RP-IN-PROC-05 | 008 | Negative | AppNAI and a second portfolio startup both shortlisted on tender T-77 | HOLD `AFFILIATE_BID_CLEARANCE` |
| TC-RP-IN-PROC-06 | 010 | Negative | Tender enters e-RA stage | MANUAL; agent excluded |
| TC-RP-IN-PROC-07 | 011 | Boundary | First automated attempt at deadline − 6 h exactly | Allowed (B_auto inclusive start) |
| TC-RP-IN-PROC-08 | 011 | Negative | Deadline − 5 h 59 m | ESCALATE to assisted |
| TC-RP-IN-PROC-09 | 012 | Negative | Draft e-mail to evaluation committee member | Block 012 |
| TC-RP-IN-PROC-10 | 014 | Negative | Portal returns page without bid ID | Reconciling; no resubmission |

### 11.15.29.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-IN-PROC
  title: "Bids to Indian public buyers: eligibility and registration, portal capability, digital signature certificates, bid security, mandatory declarations, integrity and anti-collusion, deadlines, two-envelope handling, receipts"
  version: "0.1-draft"
  state: draft
  jurisdictions: "IN (procuring entity of the Government of India, a state government, a PSU or other public body; portal in India)"
  channels: "BID (bid package, portal submission, receipt), DOC (declarations)"
  audiences: "GOV (public buyers)"
  startups: "AppNAI (primary), OrganicSpec, any startup bidding; Tenant"
  gates_mandate_types: "MT-BID (AUTO mode); assisted and manual modes also checked"
  effective_dates: "GFR as amended to date (verify latest OM); GeM GTC version current at submission (verify)"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  level_cap: "ASSISTED (L2) on GeM, CPPP/GePNIC and state NIC portals until a portal row records counsel-reviewed automation permission; MANUAL (L1) for reverse auctions"
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
parameters:
  gem_capability_default: "ASSISTED_ONLY"
  cppp_capability_default: "ASSISTED_ONLY"
  unreviewed_portal_capability: "MANUAL_ONLY"
  dsc_class_required: "Class III (signing + encryption) unless portal states otherwise"
  reverse_auction_mode: "MANUAL (human)"
  automation_buffer_hours: "6"
  hard_stop_buffer_hours: "2"
  retention_years: "8"
rules:
  - id: RP-IN-PROC-001
    obligation: "A bid shall be submitted only from a portal account registered in the legal name of the bidding company (GeM seller ID, CPPP bidder enrolment), administered by an authorised officer of that company, whose registration is active on the submission date"
    citation: "GeM GTC (registration) (VR-58); CPPP bidder enrolment (VR-59); BRL-BID-06"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "portal_account.owner_legal_entity = bid.bidder_legal_entity AND status = active (checked ≤ 24 h before submit)"
    severity: "Block"
    override: none
    evidence: "Portal account record"
    remediation_message: "\"The portal account is not registered to this company or is not active.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-002
    obligation: "AUTO submission shall be used on a portal only if the portal capability registry records, from counsel's review of the portal's current terms, that automated or API submission is permitted; GeM, CPPP/GePNIC and state NIC portals default to ASSISTED_ONLY and any unreviewed portal to MANUAL_ONLY"
    citation: "GeM GTC (compliance; suspension for breach of terms) (VR-58); GFR Rule 149 (VR-57); FR-V12-P-118…122; GAP-1045 [GAP-1168]"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "portal_profile.capability ∈ {API_PERMITTED, AUTOMATION_PERMITTED} AND counsel_review.date ≤ 120 d; else mode = ASSISTED/MANUAL"
    severity: "Block"
    override: none
    evidence: "Portal capability record"
    remediation_message: "\"This portal does not permit automated submission. Use assisted or manual submission.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-003
    obligation: "Bids shall be signed with the Class III DSC (or the signature method the portal prescribes) of the company's authorised signatory, operated only by that person; the platform shall never store, hold, export or operate a personal DSC, token or PIN"
    citation: "IT Act s.3A, s.5, s.35 (VR-52, VR-59); §11.17.7.5; FR-V12-P-124"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Assisted session: signing happens on the signatory's device; no DSC/PIN field in any platform schema; HSM key use for bids only if rule 2 portal row allows an organisational certificate"
    severity: "Block"
    override: none
    evidence: "Assisted-session log"
    remediation_message: "\"Only the authorised signatory can sign this bid with their own DSC.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-004
    obligation: "The signatory's authority (board resolution or power of attorney) shall be on file, unexpired and matching the name on the DSC and the portal account"
    citation: "GFR procurement manuals (authorised signatory) (verify)"
    applies_to: "BID, DOC · GOV"
    check: "deterministic"
    detection: "authority_doc.signatory = dsc.subject_name AND valid_until > deadline"
    severity: "Block"
    override: none
    evidence: "Authority document"
    remediation_message: "\"Upload a valid authority document for this signatory.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-005
    obligation: "Bid security (EMD) evidence or a bid-securing declaration, or a valid exemption certificate (MSE/startup) accepted by the tender, shall be attached before submission"
    citation: "GFR Rule 170 (verify); MSE Procurement Policy (verify)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Tender requires EMD → emd_ref or bsd_doc or exemption_cert with validity"
    severity: "Block"
    override: none
    evidence: "EMD/BSD/exemption document"
    remediation_message: "\"Bid security or a valid exemption is missing.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-006
    obligation: "Every statutory or tender declaration (local content under the Make in India order, land-border-country eligibility, non-debarment, no conflict of interest, integrity pact, MSE/startup status, turnover, past performance) shall be made from source records and approved by the authorised signatory; AI may extract and cross-check but shall not author or alter a declaration"
    citation: "PPP-MII Order 2017 (verify); DoE Order 23 Jul 2020 / GFR Rule 144(xi) (verify); GFR Rule 175 (code of integrity) (verify); BRL-AI-07 amended"
    applies_to: "BID, DOC · GOV"
    check: "deterministic"
    detection: "Declaration fields bound to source records; approved_by = signatory; AG-206/207 edits on declaration blocks rejected"
    severity: "Block"
    override: none
    evidence: "Signed declarations"
    remediation_message: "\"Declarations must come from records and be approved by the signatory.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-007
    obligation: "MSE or startup preferences and exemptions shall be claimed only with a valid Udyam registration or DPIIT recognition for the relevant category"
    citation: "MSE Procurement Policy Order 2012 (verify); DPIIT startup relaxations (verify)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "claim.msme → Udyam number verified; claim.startup → DPIIT certificate"
    severity: "Block"
    override: none
    evidence: "Certificate"
    remediation_message: "\"This preference needs a valid Udyam or DPIIT certificate.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-008
    obligation: "Where two or more companies of the same tenant (or of the Owner Portfolio) intend to bid in the same tender, no bid shall proceed without written clearance by R10 and counsel, and bid information shall be walled between them"
    citation: "Competition Act 2002 s.3(3)(d) (bid rigging) (verify); GFR Rule 175 (verify); BRL-SRC-10"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "tender_id shared across companies of one tenant/portfolio → HOLD AFFILIATE_BID_CLEARANCE; RLS wall on bid data"
    severity: "Block"
    override: none
    evidence: "Clearance record"
    remediation_message: "\"Another company in the group is bidding on this tender. Legal clearance is needed.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-009
    obligation: "Bid documents shall be genuine and unaltered; certificates and financial statements shall be the issued versions; any discrepancy found by the cross-check shall stop submission"
    citation: "GFR Rule 151 (debarment) and 175 (verify); Indian Penal Code / BNS forgery provisions (verify)"
    applies_to: "BID, DOC · GOV"
    check: "deterministic_then_ai_review"
    detection: "DET: file hashes vs document vault originals; AI (AG-207): inconsistent figures, dates, names"
    severity: "Block"
    override: r10_with_reason
    evidence: "Cross-check report"
    remediation_message: "\"A document does not match its original or other bid data.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-010
    obligation: "The bid price and commercial terms submitted shall equal the MT-BID approved price and terms bound to the package hash; participation in a reverse auction or any live price revision shall be performed by an authorised person only"
    citation: "DEC-781; DEC-851; BRL-BID-03"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "package_hash = mandate.package_hash; tender stage e_ra → MANUAL"
    severity: "Block"
    override: none
    evidence: "Package hash"
    remediation_message: "\"The price differs from the approved package, or this is a reverse auction that needs a person.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-011
    obligation: "Submission shall complete before the closing time shown by the portal (portal server time authoritative); automated attempts shall respect the automation buffer and hard-stop buffer"
    citation: "BRL-BID-01 as amended; DEC-852; AU-278"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Deadline guard B_auto/B_hard; portal clock offset measured at session start"
    severity: "Block"
    override: none
    evidence: "Guard log"
    remediation_message: "\"Too close to the deadline for an automated attempt. A person must submit.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-012
    obligation: "During the tender process the bidder shall communicate with the procuring entity only through the channels the tender designates (pre-bid meeting, portal clarification), and no agent shall contact officials of the procuring entity"
    citation: "GFR Rule 175 (verify); integrity pact (verify); Prevention of Corruption Act (verify)"
    applies_to: "EM, VO, BID · GOV"
    check: "deterministic_then_ai_review"
    detection: "DET: outbound to procuring-entity domains blocked except designated clarification channel; AI: improper inducement language"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Contact with the buyer is only allowed through the tender's clarification channel.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-013
    obligation: "Financial (commercial) envelopes shall stay encrypted and unopened until upload; the system shall not expose prices to anyone outside the MT-BID approvers before the bid opening"
    citation: "Two-envelope tender rules (verify); §11.17.7.2"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Tender data key access limited to AU-279 and approvers; access log"
    severity: "Block"
    override: none
    evidence: "Access log"
    remediation_message: "\"Commercial envelope access is restricted until submission.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-014
    obligation: "A portal acknowledgement (bid ID, timestamp, tender ID) shall be captured and verified for every submission and stored with object lock; withdrawal or modification shall be performed only by an authorised person"
    citation: "FR-V12-P-125, 131; DEC-851"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Receipt verification rules (§11.17.7.7)"
    severity: "Block"
    override: none
    evidence: "Receipt artefact"
    remediation_message: "\"No verified portal receipt. Check the portal before any further action.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-015
    obligation: "The platform shall not scrape or access portals in a way their terms forbid; tender discovery shall use public listings, RSS feeds or licensed data feeds only"
    citation: "GeM GTC and CPPP terms (verify) (VR-58, VR-59)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Discovery adapter allowlist per portal"
    severity: "Block"
    override: none
    evidence: "Adapter config"
    remediation_message: "\"This discovery method is not permitted for this portal.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-PROC-016
    obligation: "Bid records (package, approvals, declarations, receipts, correspondence) shall be retained for at least 8 years or the contract period plus the audit period, whichever is longer"
    citation: "MC-24; GFR record-keeping (verify)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Retention class bid_8y"
    severity: "Block"
    override: none
    evidence: "Evidence pack"
    remediation_message: "\"Bid records must be retained.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-IN-PROC-01
    name: "Improper inducement / contact"
    match: "phrase + AI"
    severity: "Block"
    used_by: "012"
    terms:
      - "speed money"
      - "facilitation"
      - "take care of the officer"
      - "inside information"
      - "know the evaluation committee"
      - "arrange approval"
      - "सेटिंग"
      - "अंदर की जानकारी"
  - id: PL-IN-PROC-02
    name: "Affiliate coordination"
    match: "phrase + AI"
    severity: "Block"
    used_by: "008"
    terms:
      - "our sister company will quote"
      - "cover bid"
      - "we will quote higher"
      - "split the lots"
      - "rotate L1"
templates:
  - id: TPL-IN-PROC-01
    use: "Assisted-session instruction to the signatory"
    en: "\"The sealed package {package_hash_prefix} is pre-filled on {portal}. Check the uploaded files show 'verified' below, then sign with your own DSC and press Submit. The system cannot sign for you.\""
    placement: "A268 assisted session"
  - id: TPL-IN-PROC-02
    use: "Declaration approval prompt"
    en: "\"You are confirming, as authorised signatory of {company}, that each declaration below is true and complete based on the attached records. False declarations can lead to debarment and prosecution.\""
    placement: "Before signing"
```

### 11.15.29.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-IN-PROC v0.1-draft → proposed v1.0 |
| Reviewer (name, enrolment/bar no., jurisdiction of admission) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Rules amended (IDs and summary) | _______________________ |
| Pack parameters confirmed (values and sources) | ☐ All ☐ Amended: __________ |
| Citations confirmed against primary text (VR entries) | ☐ VR-52 ☐ VR-57 ☐ VR-58 ☐ VR-59 |
| Translations reviewed by (if any) | _______________________ |
| Conditions or limitations of the sign-off | _______________________ |
| Next review due | ____ / ____ / ______ (≤ 120 days) |
| R10 approval (name, date) | _______________________ |
| Signature (counsel) / Signature (R10) | _______________ / _______________ |

---

## 11.15.30 RP-EU-PROC: EU public procurement: Directive 2014/24/EU, national eSubmission platforms, eIDAS signatures, ESPD and integrity

### 11.15.30.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-EU-PROC |
| Title | Bids to EU/EEA contracting authorities: designated electronic tools, signature level, ESPD and exclusion grounds, time limits, conflicts and collusion, confidentiality, abnormally low tenders, third-country restrictions |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | EU/EEA (contracting authority in an EEA state); national platform overlay §11.15.30.12 |
| Channels | BID, DOC |
| Audiences | GOV |
| Startups | AppNAI and any startup bidding in the EU; Tenant |
| Mandate types gated | MT-BID |
| Legal sources | Directive 2014/24/EU Arts 4, 18, 21, 22, 24, 35, 56–59, 63, 69, Annex IV (VR-60); Commission Delegated Regulation (EU) 2025/2152 thresholds for 2026–2027 (VR-61); Implementing Regulation (EU) 2019/1780 eForms (verify); eIDAS (EU) 910/2014 as amended Arts 25, 26, 35 (VR-55); Council Regulation (EU) 833/2014 Art. 5k (Russia-related participation ban) (verify); International Procurement Instrument Regulation (EU) 2022/1031 (verify); Foreign Subsidies Regulation (EU) 2022/2560 notification in procurement (verify); national transposition laws (verify per state); GDPR (VR-24) |
| Effective dates | Directive in force; thresholds from 1 Jan 2026 (VR-61); Commission proposal to revise the procurement directives expected (verify) |
| Owner | R10 Legal/Compliance with R06 |
| Review cadence | Quarterly + per national platform terms change |
| Expiry / fail-closed | 120 days; MANUAL while not `active` |
| Depends on | RP-EU-AGENTCOM (signatures), RP-COMMIT, RP-EU-AI (AI disclosure in any messages) |

### 11.15.30.2 Plain-language summary

1. Submit only through the electronic tool the contracting authority names, following that platform's terms.
2. Where a qualified signature of a person is required, that person signs. A qualified electronic seal of the company may be used only where the authority accepts seals and counsel records it for that platform.
3. The European Single Procurement Document (ESPD) and every exclusion-ground statement come from records and are approved by an authorised person. Serious misrepresentation is itself a ground for exclusion.
4. Late tenders are rejected. The platform's timestamp decides.
5. No affiliate bidding or information exchange without clearance. Electronic auctions are human-only.
6. Mark trade secrets. Be ready to explain a low price.
7. Check third-country restrictions, such as the Russia-related ban on participation.

### 11.15.30.3 Definitions

| Term | Definition for this pack |
|---|---|
| Contracting authority | State, regional or local authority, body governed by public law or association of them (Art. 2(1)(1)) |
| ESPD | European Single Procurement Document: self-declaration on exclusion grounds and selection criteria (Art. 59) |
| Electronic tool | The submission platform designated in the procurement documents, meeting Art. 22 and Annex IV |
| Qualified electronic seal | A seal of a legal person created by a qualified device on a qualified certificate (eIDAS Art. 3(27)); presumed integrity and origin (Art. 35(2)) |

### 11.15.30.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-EU-PROC-001 | Tenders shall be submitted only through the electronic tool and in the format the procurement documents designate, using a bidder account registered to the bidding company | Directive 2014/24/EU Art. 22(1), Annex IV (VR-60) | BID · GOV | DET | `portal_profile` = tool named in tender; account owner = bidder | Block | Tender reference; account record | "Use the submission platform named in the tender with this company's account." |
| RP-EU-PROC-002 | AUTO submission shall be used only where the national platform row records counsel's confirmation that the platform's terms permit API or automated submission; otherwise ASSISTED or MANUAL | National platform terms (verify per platform); FR-V12-P-118…122; GAP-1045 | BID · GOV | DET | Capability registry; review ≤ 120 d | Block | Capability record | "This platform does not permit automated submission." |
| RP-EU-PROC-003 | Where the procurement documents require an advanced or qualified electronic signature of a natural person, it shall be created by that person under their sole control; the platform shall not trigger it; a qualified electronic seal of the bidder may be used only where the documents accept a seal and counsel has recorded this for the platform [ASSUMPTION-1169] | Directive Art. 22(6)(c) (VR-60); eIDAS Arts 25, 26, 35 (VR-55) | BID · GOV | DET | `tender.signature_requirement` ∈ {QES_person, AES_person} → ASSISTED; `QSeal_accepted = true` and portal row allows → AUTO possible | Block | Signature record | "A person must sign this tender with their own signature." |
| RP-EU-PROC-004 | The ESPD and every statement on exclusion grounds and selection criteria shall be generated from records and approved by an authorised person; AI shall not author or alter them | Directive Arts 57, 59 (VR-60) | BID, DOC · GOV | DET | ESPD fields bound to source; approval recorded; edit by AI rejected | Block | Approved ESPD | "The ESPD must come from records and be approved by an authorised person." |
| RP-EU-PROC-005 | No statement in a tender shall misrepresent information required for verifying exclusion grounds or selection criteria, and documents shall be genuine | Directive Art. 57(4)(h) (VR-60) | BID, DOC · GOV | DET+AI | As RP-IN-PROC-009 | Block | Cross-check report | "A statement or document may be inaccurate. Submission stopped." |
| RP-EU-PROC-006 | Tenders shall be received before the time limit; the platform's timestamp is authoritative; automated attempts respect the deadline guard | Directive Arts 26–28, 47 (VR-60); AU-278 | BID · GOV | DET | Deadline guard; platform clock | Block | Guard log | "Too close to the deadline for automated submission." |
| RP-EU-PROC-007 | Where affiliated companies may bid in the same procedure, the bid shall be held until R10 and counsel clear it, and no information shall be exchanged between them | Directive Art. 57(4)(d) (agreements distorting competition); TFEU Art. 101 (VR-60, VR-55) | BID · GOV | DET | As RP-IN-PROC-008 | Block | Clearance record | "An affiliated company is bidding. Legal clearance needed." |
| RP-EU-PROC-008 | Electronic auctions and any live price revision shall be performed by an authorised person | Directive Art. 35 (VR-60); DEC-851 | BID · GOV | DET | Stage `e_auction` → MANUAL | Block | — | "Electronic auctions need a person." |
| RP-EU-PROC-009 | Information the bidder designates as confidential (trade or technical secrets) shall be marked as such in the tender as the documents require | Directive Art. 21 (VR-60) | BID, DOC · GOV | DET+AI | DET: confidentiality marking fields present where documents allow; AI: unmarked sensitive pricing methodology | Warn | Marking record | "Mark confidential parts of the tender as the documents require." |
| RP-EU-PROC-010 | Where the tendered price is below the cost floor recorded in the package, a price-explanation dossier shall be prepared before submission for use if the authority requests it | Directive Art. 69 (abnormally low tenders) (VR-60) | BID · GOV | DET | `price_total < cost_floor × (1 + min_margin)` → dossier required | Warn | Dossier | "Prepare an explanation for this low price in case the authority asks." |
| RP-EU-PROC-011 | Where the bidder relies on the capacities of other entities or subcontracts, their ESPDs and commitments shall be attached as the documents require | Directive Art. 63, Art. 71 (VR-60) | BID · GOV | DET | `reliance_entities[]` → ESPD and commitment letters present | Block | Attachments | "Add the ESPD and commitment of each entity relied on." |
| RP-EU-PROC-012 | No tender shall be submitted where the bidder or a relied-upon entity or significant subcontractor falls within the Russia-related participation ban or another EU restrictive measure; foreign-subsidy notifications shall be made where thresholds are met | Reg. (EU) 833/2014 Art. 5k (verify); Reg. (EU) 2022/2560 (verify); Reg. (EU) 2022/1031 (verify) | BID · GOV | DET | Ownership screening of bidder and relied-upon entities; FSR threshold check | Block | Screening record | "A restricted-party or foreign-subsidy check is outstanding." |
| RP-EU-PROC-013 | The procedure's regime (above or below EU thresholds) shall be recorded from the notice; below-threshold national rules shall have a counsel-completed national row before AUTO | Delegated Reg. (EU) 2025/2152 (VR-61); national law (verify) | BID · GOV | DET | `tender.value` vs `param.thresholds`; below → national row required | Block | Regime record | "The rules for this below-threshold procedure are not configured." |
| RP-EU-PROC-014 | Notice data shall be read from TED and national platforms only through their published APIs or feeds under their terms | TED API terms (verify) | BID · GOV | DET | Discovery adapter allowlist | Block | Adapter config | "Use the published notice API for this source." |
| RP-EU-PROC-015 | Remedies, standstill challenges and complaints shall be decided and filed by authorised persons; personal data in tenders processed under GDPR and kept in the EU region | Remedies Directives 89/665/EEC as amended (verify); GDPR (VR-24); DEC-772 | BID, DOC · GOV | DET | Challenge workflow L1; region router | Block | — | "Challenges are filed by authorised persons only." |

**Pack parameters (loaded by AU-128 and read by the PDP, AU-264/272/278/280/281/282; every value "verify at time of implementation, as of 28 Nov 2026" unless its VR entry is verified).**

| Parameter | Draft value | Source / note |
|---|---|---|
| thresholds | works €5,404,000; central supplies/services €140,000; sub-central €216,000 (1 Jan 2026–31 Dec 2027) | VR-61 (verify against OJ) |
| unreviewed_platform_capability | MANUAL_ONLY | FR-V12-P-118 |
| e_auction_mode | MANUAL | Platform policy |

### 11.15.30.5 Required disclosures and approved template wording

| Template | Use | English (approved draft wording) | Other languages | Placement |
|---|---|---|---|---|
| TPL-EU-PROC-01 | ESPD approval prompt | "You are confirming, as authorised representative of {company}, that the ESPD statements below are accurate and complete. Serious misrepresentation can lead to exclusion." | de/fr pending legal translation [GAP-996] | Before ESPD approval |
| TPL-EU-PROC-02 | Assisted-session instruction | "The sealed package {package_hash_prefix} is staged on {platform}. Confirm the files are verified, then apply your own signature and submit." | de/fr pending | Assisted session |

### 11.15.30.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-EU-PROC-01 | Collusion and inducement | cover bid; complementary bid; bid rotation; agree prices with; let them win this lot; Schutzangebot; offre de couverture | phrase + AI | Block | 007 |

**Prohibited (absolute, no mandate, exception or override can unlock):** triggering a person's qualified signature; AI-authored ESPD statements; automated electronic-auction bidding; submitting where a restricted-party check fails.

### 11.15.30.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | PEPPOL-based ordering after award | Not a tender submission; RP-EU-AGENTCOM applies |
| E-2 | Utilities (Directive 2014/25/EU) and concessions (2014/23/EU) | Out of v0.1 scope: MANUAL until counsel adds rows |
| E-3 | Defence and security procurement (2009/81/EC) | Out of scope; MANUAL |

### 11.15.30.8 AI reviewer review guidance (RP-EU-PROC)

- **Reviewer:** AG-207 and AG-206 applying the AG-086 contract.
- **Look for:** ESPD inconsistencies; unmarked confidential content; collusion language; low-price risk.
- **Cite:** `RP-EU-PROC-0NN` and the pack version only; quote the document and span.
- **Escalate (`needs_counsel`):** restricted-party doubts; affiliate overlap; signature requirement unclear.
- **Never:** author ESPD statements; decide the signature level.

### 11.15.30.9 Test cases

| ID | Rule | Type | Input (summary) | Expected |
|---|---|---|---|---|
| TC-RP-EU-PROC-01 | 003 | Negative | Tender requires QES of legal representative | ASSISTED |
| TC-RP-EU-PROC-02 | 003 | Positive | Tender accepts qualified seal; platform row confirms; MT-BID Active | AUTO allowed |
| TC-RP-EU-PROC-03 | 004 | Negative | AI edits ESPD Part III answer | Rejected |
| TC-RP-EU-PROC-04 | 008 | Negative | Procedure enters e-auction | MANUAL |
| TC-RP-EU-PROC-05 | 012 | Negative | Relied-upon entity has 51% Russian ownership | Block 012 |
| TC-RP-EU-PROC-06 | 013 | Negative | Below-threshold tender in a state without a national row | Block 013 (MANUAL) |

### 11.15.30.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-EU-PROC
  title: "Bids to EU/EEA contracting authorities: designated electronic tools, signature level, ESPD and exclusion grounds, time limits, conflicts and collusion, confidentiality, abnormally low tenders, third-country restrictions"
  version: "0.1-draft"
  state: draft
  jurisdictions: "EU/EEA (contracting authority in an EEA state); national platform overlay §11.15.30.12"
  channels: "BID, DOC"
  audiences: "GOV"
  startups: "AppNAI and any startup bidding in the EU; Tenant"
  gates_mandate_types: "MT-BID"
  effective_dates: "Directive in force; thresholds from 1 Jan 2026 (VR-61); Commission proposal to revise the procurement directives expected (verify)"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  level_cap: "ASSISTED (L2) unless the national platform row records API or automated submission permitted and the signature requirement can be met lawfully without a person; electronic auctions MANUAL"
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
parameters:
  thresholds: "works €5,404,000; central supplies/services €140,000; sub-central €216,000 (1 Jan 2026–31 Dec 2027)"
  unreviewed_platform_capability: "MANUAL_ONLY"
  e_auction_mode: "MANUAL"
rules:
  - id: RP-EU-PROC-001
    obligation: "Tenders shall be submitted only through the electronic tool and in the format the procurement documents designate, using a bidder account registered to the bidding company"
    citation: "Directive 2014/24/EU Art. 22(1), Annex IV (VR-60)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "portal_profile = tool named in tender; account owner = bidder"
    severity: "Block"
    override: none
    evidence: "Tender reference; account record"
    remediation_message: "\"Use the submission platform named in the tender with this company's account.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-002
    obligation: "AUTO submission shall be used only where the national platform row records counsel's confirmation that the platform's terms permit API or automated submission; otherwise ASSISTED or MANUAL"
    citation: "National platform terms (verify per platform); FR-V12-P-118…122; GAP-1045"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Capability registry; review ≤ 120 d"
    severity: "Block"
    override: none
    evidence: "Capability record"
    remediation_message: "\"This platform does not permit automated submission.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-003
    obligation: "Where the procurement documents require an advanced or qualified electronic signature of a natural person, it shall be created by that person under their sole control; the platform shall not trigger it; a qualified electronic seal of the bidder may be used only where the documents accept a seal and counsel has recorded this for the platform [ASSUMPTION-1169]"
    citation: "Directive Art. 22(6)(c) (VR-60); eIDAS Arts 25, 26, 35 (VR-55)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "tender.signature_requirement ∈ {QES_person, AES_person} → ASSISTED; QSeal_accepted = true and portal row allows → AUTO possible"
    severity: "Block"
    override: none
    evidence: "Signature record"
    remediation_message: "\"A person must sign this tender with their own signature.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-004
    obligation: "The ESPD and every statement on exclusion grounds and selection criteria shall be generated from records and approved by an authorised person; AI shall not author or alter them"
    citation: "Directive Arts 57, 59 (VR-60)"
    applies_to: "BID, DOC · GOV"
    check: "deterministic"
    detection: "ESPD fields bound to source; approval recorded; edit by AI rejected"
    severity: "Block"
    override: none
    evidence: "Approved ESPD"
    remediation_message: "\"The ESPD must come from records and be approved by an authorised person.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-005
    obligation: "No statement in a tender shall misrepresent information required for verifying exclusion grounds or selection criteria, and documents shall be genuine"
    citation: "Directive Art. 57(4)(h) (VR-60)"
    applies_to: "BID, DOC · GOV"
    check: "deterministic_then_ai_review"
    detection: "As RP-IN-PROC-009"
    severity: "Block"
    override: r10_with_reason
    evidence: "Cross-check report"
    remediation_message: "\"A statement or document may be inaccurate. Submission stopped.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-006
    obligation: "Tenders shall be received before the time limit; the platform's timestamp is authoritative; automated attempts respect the deadline guard"
    citation: "Directive Arts 26–28, 47 (VR-60); AU-278"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Deadline guard; platform clock"
    severity: "Block"
    override: none
    evidence: "Guard log"
    remediation_message: "\"Too close to the deadline for automated submission.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-007
    obligation: "Where affiliated companies may bid in the same procedure, the bid shall be held until R10 and counsel clear it, and no information shall be exchanged between them"
    citation: "Directive Art. 57(4)(d) (agreements distorting competition); TFEU Art. 101 (VR-60, VR-55)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "As RP-IN-PROC-008"
    severity: "Block"
    override: none
    evidence: "Clearance record"
    remediation_message: "\"An affiliated company is bidding. Legal clearance needed.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-008
    obligation: "Electronic auctions and any live price revision shall be performed by an authorised person"
    citation: "Directive Art. 35 (VR-60); DEC-851"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Stage e_auction → MANUAL"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"Electronic auctions need a person.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-009
    obligation: "Information the bidder designates as confidential (trade or technical secrets) shall be marked as such in the tender as the documents require"
    citation: "Directive Art. 21 (VR-60)"
    applies_to: "BID, DOC · GOV"
    check: "deterministic_then_ai_review"
    detection: "DET: confidentiality marking fields present where documents allow; AI: unmarked sensitive pricing methodology"
    severity: "Warn"
    override: r10_with_reason
    evidence: "Marking record"
    remediation_message: "\"Mark confidential parts of the tender as the documents require.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-010
    obligation: "Where the tendered price is below the cost floor recorded in the package, a price-explanation dossier shall be prepared before submission for use if the authority requests it"
    citation: "Directive Art. 69 (abnormally low tenders) (VR-60)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "price_total < cost_floor × (1 + min_margin) → dossier required"
    severity: "Warn"
    override: r10_with_reason
    evidence: "Dossier"
    remediation_message: "\"Prepare an explanation for this low price in case the authority asks.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-011
    obligation: "Where the bidder relies on the capacities of other entities or subcontracts, their ESPDs and commitments shall be attached as the documents require"
    citation: "Directive Art. 63, Art. 71 (VR-60)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "reliance_entities[] → ESPD and commitment letters present"
    severity: "Block"
    override: none
    evidence: "Attachments"
    remediation_message: "\"Add the ESPD and commitment of each entity relied on.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-012
    obligation: "No tender shall be submitted where the bidder or a relied-upon entity or significant subcontractor falls within the Russia-related participation ban or another EU restrictive measure; foreign-subsidy notifications shall be made where thresholds are met"
    citation: "Reg. (EU) 833/2014 Art. 5k (verify); Reg. (EU) 2022/2560 (verify); Reg. (EU) 2022/1031 (verify)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Ownership screening of bidder and relied-upon entities; FSR threshold check"
    severity: "Block"
    override: none
    evidence: "Screening record"
    remediation_message: "\"A restricted-party or foreign-subsidy check is outstanding.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-013
    obligation: "The procedure's regime (above or below EU thresholds) shall be recorded from the notice; below-threshold national rules shall have a counsel-completed national row before AUTO"
    citation: "Delegated Reg. (EU) 2025/2152 (VR-61); national law (verify)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "tender.value vs param.thresholds; below → national row required"
    severity: "Block"
    override: none
    evidence: "Regime record"
    remediation_message: "\"The rules for this below-threshold procedure are not configured.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-014
    obligation: "Notice data shall be read from TED and national platforms only through their published APIs or feeds under their terms"
    citation: "TED API terms (verify)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Discovery adapter allowlist"
    severity: "Block"
    override: none
    evidence: "Adapter config"
    remediation_message: "\"Use the published notice API for this source.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-PROC-015
    obligation: "Remedies, standstill challenges and complaints shall be decided and filed by authorised persons; personal data in tenders processed under GDPR and kept in the EU region"
    citation: "Remedies Directives 89/665/EEC as amended (verify); GDPR (VR-24); DEC-772"
    applies_to: "BID, DOC · GOV"
    check: "deterministic"
    detection: "Challenge workflow L1; region router"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"Challenges are filed by authorised persons only.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-EU-PROC-01
    name: "Collusion and inducement"
    match: "phrase + AI"
    severity: "Block"
    used_by: "007"
    terms:
      - "cover bid"
      - "complementary bid"
      - "bid rotation"
      - "agree prices with"
      - "let them win this lot"
      - "Schutzangebot"
      - "offre de couverture"
templates:
  - id: TPL-EU-PROC-01
    use: "ESPD approval prompt"
    en: "\"You are confirming, as authorised representative of {company}, that the ESPD statements below are accurate and complete. Serious misrepresentation can lead to exclusion.\""
    placement: "Before ESPD approval"
  - id: TPL-EU-PROC-02
    use: "Assisted-session instruction"
    en: "\"The sealed package {package_hash_prefix} is staged on {platform}. Confirm the files are verified, then apply your own signature and submit.\""
    placement: "Assisted session"
```

### 11.15.30.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-EU-PROC v0.1-draft → proposed v1.0 |
| Reviewer (name, enrolment/bar no., jurisdiction of admission) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Rules amended (IDs and summary) | _______________________ |
| Pack parameters confirmed (values and sources) | ☐ All ☐ Amended: __________ |
| Citations confirmed against primary text (VR entries) | ☐ VR-24 ☐ VR-55 ☐ VR-60 ☐ VR-61 |
| Translations reviewed by | _______________________ |
| Conditions or limitations of the sign-off | _______________________ |
| Next review due | ____ / ____ / ______ (≤ 120 days) |
| R10 approval (name, date) | _______________________ |
| Signature (counsel) / Signature (R10) | _______________ / _______________ |

### 11.15.30.12 National platform overlay (counsel to complete; until a row is complete the platform is MANUAL_ONLY)

| State | Typical platform(s) (verify) | Expected capability (verify) | Signature commonly required (verify) | Notes |
|---|---|---|---|---|
| DE | Federal e-Vergabe; Länder platforms | ASSISTED_ONLY | Text form or AES/QES per authority | Many tenders accept text form (§53 VgV, verify) |
| FR | PLACE and regional profiles d'acheteur | ASSISTED_ONLY | Signature often required only at award (verify) | DUME (French ESPD) |
| NL | TenderNed | ASSISTED_ONLY | Per authority | — |
| IE | eTenders | ASSISTED_ONLY | Per authority | — |
| Other | Counsel | MANUAL_ONLY | Counsel | — |


---

## 11.15.31 RP-US-PROC: US federal procurement: FAR (and the FAR overhaul), SAM.gov, submission rules, certifications and integrity

### 11.15.31.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-US-PROC |
| Title | Offers to US federal agencies: SAM.gov registration and terms of use, submission per solicitation instructions, late-offer rules, representations and certifications, procurement integrity, conflicts, size status, CUI and export controls |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | US-FED (federal executive agencies); state and local procurement out of scope (Block) |
| Channels | BID, DOC |
| Audiences | GOV |
| Startups | AppNAI and any startup bidding in the US; Tenant |
| Mandate types gated | MT-BID |
| Legal sources | FAR subparts 3.1, 3.104, 4.1 (52.204-7), 4.12 (52.204-8), 4.5, 4.7, 9.1, 9.5, 15.2 (52.215-1), 14.3; 52.203-2, 52.203-5, 52.204-24/25/26 (VR-62); Revolutionary FAR Overhaul model deviations under EO 14275 and OMB M-25-26 (VR-63); SAM.gov Terms of Use (VR-64); 41 U.S.C. §2102 Procurement Integrity Act; 18 U.S.C. §1001; 31 U.S.C. §3729 (False Claims Act); 15 U.S.C. §632(w) (size misrepresentation); 32 CFR Part 2002 and NIST SP 800-171 (CUI); ITAR 22 CFR 120–130 and EAR 15 CFR 730–774 (all verify) |
| Effective dates | FAR and agency deviations as stated in each solicitation (RFO transition: the solicitation's clause set governs) (VR-63) |
| Owner | R10 Legal/Compliance with R06; US counsel |
| Review cadence | Quarterly + on FAR Council/RFO releases |
| Expiry / fail-closed | 120 days; MANUAL while not `active` |
| Depends on | RP-US-EMAIL (any e-mail to agencies), RP-COMMIT |

### 11.15.31.2 Plain-language summary

1. The bidding company must have an active SAM.gov registration and current representations and certifications, maintained by its authorised Entity Administrator. The system never does registration actions.
2. SAM.gov data is used only through official APIs with keys, never scraping.
3. Offers are submitted exactly as the solicitation instructs. Late is late.
4. Certifications and representations are made by an authorised person. False statements carry criminal and False Claims Act exposure.
5. No non-public source-selection information is used. Affiliates bidding on the same solicitation need clearance and an independent-price certificate.
6. Solicitations with Controlled Unclassified Information or export-controlled technical data are handled outside the platform in v0.1.

### 11.15.31.3 Definitions

| Term | Definition for this pack |
|---|---|
| SAM.gov | System for Award Management, the federal registration and data system |
| UEI | Unique Entity ID assigned in SAM.gov |
| Reps and certs | Annual representations and certifications in SAM (FAR 52.204-8) plus solicitation-specific ones |
| Source selection information | Non-public information prepared for use by an agency to evaluate offers (41 U.S.C. §2101(7)) |
| CUI | Controlled Unclassified Information (32 CFR Part 2002) |
| RFO | Revolutionary FAR Overhaul: rewrite of FAR parts issued as model deviations from 2025 (VR-63) |

### 11.15.31.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-US-PROC-001 | An offer shall be submitted only for a bidder with an active SAM.gov registration (UEI) in its legal name, current reps and certs and no active exclusion, checked within 24 hours before submission | FAR 4.1102, 52.204-7, 52.204-8, 9.405 (VR-62) | BID · GOV | DET | SAM entity API: `registrationStatus = Active`, `exclusionStatusFlag = N`, reps current | Block | SAM extract | "The SAM.gov registration is not active or an exclusion is recorded." |
| RP-US-PROC-002 | The platform shall access SAM.gov only through official APIs and extracts with keys issued to the tenant, shall not scrape or use bots on SAM.gov pages, shall rotate keys at least every 90 days and shall not share individual keys; registration, renewal and reps-and-certs actions shall be performed only by the bidder's authorised Entity Administrator | SAM.gov Terms of Use (VR-64) | BID · GOV | DET | Adapter allowlist (API endpoints only); key age ≤ 90 d; no write calls to registration | Block | Key metadata | "Use the official SAM.gov API with a current key; registration actions are human-only." |
| RP-US-PROC-003 | Offers shall be submitted by the method, to the address or system and in the format the solicitation specifies; AUTO is permitted only for e-mail submission designated by the solicitation and approved per solicitation by counsel; all other federal submissions are ASSISTED or MANUAL | FAR 52.215-1(c), 14.302 (VR-62); RECOMMENDATION-1171 | BID · GOV | DET | `solicitation.submission_method = email` AND `counsel_row.approved = true` → AUTO possible; else ASSISTED/MANUAL | Block | Solicitation row | "This solicitation requires assisted or manual submission." |
| RP-US-PROC-004 | Offers shall be received by the exact time specified; for electronic submissions the automated deadline shall be the earlier of the platform hard stop and the time that ensures receipt at the government's initial point of entry by 5:00 p.m. one working day before the deadline where the late-offer exception depends on it | FAR 52.215-1(c)(3) (verify) (VR-62) | BID · GOV | DET | `submit_not_after = min(deadline − B_hard, param.us_email_entry_cutoff)` | Block | Guard log | "Too close to the deadline for automated submission." |
| RP-US-PROC-005 | Every certification and representation (including independent price determination, lobbying, covered telecommunications equipment, Buy American/TAA, size and socio-economic status) shall be made by an authorised person from records; AI shall not author or alter them | FAR 52.203-2, 52.203-5, 52.204-24/25/26 (VR-62); 18 U.S.C. §1001; 31 U.S.C. §3729 (verify) | BID, DOC · GOV | DET | Cert fields bound to records; approval by signatory; AI edits rejected | Block | Signed certifications | "Certifications must be made by an authorised person from records." |
| RP-US-PROC-006 | No non-public source selection or contractor bid or proposal information shall be obtained, ingested or used; documents marked as such shall be quarantined and reported to R10 | 41 U.S.C. §2102; FAR 3.104 (verify) | BID, DOC · GOV | DET+AI | DET: markings 'Source Selection Information', 'Proprietary'; AI: suspicious provenance | Block | Quarantine record | "This document may be protected procurement information. It has been quarantined." |
| RP-US-PROC-007 | Where affiliates may submit offers on the same solicitation, submission shall be held until R10 and US counsel clear it and the Certificate of Independent Price Determination can be truthfully made; organisational conflicts of interest shall be identified | FAR 52.203-2, 9.5 (VR-62) | BID · GOV | DET | As RP-IN-PROC-008 + OCI questionnaire | Block | Clearance record | "An affiliate is bidding or an OCI question is open. Clearance needed." |
| RP-US-PROC-008 | Small-business size and socio-economic status shall be claimed only where the SAM record and SBA certification support it for the NAICS code of the solicitation | 13 CFR Part 121; 15 U.S.C. §632(w) (verify) | BID · GOV | DET | Claimed status ∈ SAM reps for NAICS; SBA certification where required | Block | SAM reps; SBA record | "This size or status claim is not supported for the solicitation's NAICS code." |
| RP-US-PROC-009 | Solicitations or attachments marked as CUI, and technical data controlled under ITAR or EAR, shall not be uploaded to or processed by the platform in this release | 32 CFR Part 2002; NIST SP 800-171; ITAR; EAR (verify) | BID, DOC · GOV | DET | Marking detector (CUI banners, 'ITAR', ECCN) → Block upload; manual handling | Block | Detector log | "This material is controlled and cannot be processed on the platform." |
| RP-US-PROC-010 | Electronic signatures on offers shall be applied by an authorised person by a method the agency accepts | FAR 4.502(d) (verify) | BID · GOV | DET | Signature task L1 unless counsel row allows otherwise | Block | Signature record | "An authorised person must sign this offer." |
| RP-US-PROC-011 | The clause set of each solicitation (FAR or RFO deviation text) shall be recorded and the checklist built from it; if the clause set cannot be determined the submission is MANUAL | RFO model deviations (VR-63) [GAP-1170] | BID · GOV | DET | `solicitation.clause_set` parsed; unknown → MANUAL | Warn | Clause set record | "The applicable clause set is unclear. Manual review required." |
| RP-US-PROC-012 | No agent shall contact contracting officers or evaluators except through the solicitation's designated Q&A channel and only with human-approved questions | FAR 15.201 (verify); procurement integrity | EM, VO, BID · GOV | DET+AI | Outbound to .gov/.mil domains limited to designated contact; human approval | Block | — | "Questions to the agency go only through the designated channel after approval." |
| RP-US-PROC-013 | State, local and tribal procurements shall not use this pack and shall be MANUAL until a dedicated pack exists | Scope | BID · GOV | DET | `buyer.level ≠ federal` → MANUAL | Block | — | "Only federal procurement is configured. Use manual submission." |
| RP-US-PROC-014 | Records of each offer shall be kept for at least 8 years (exceeding FAR 4.703 contractor retention where applicable) | FAR 4.703 (verify); MC-24 | BID · GOV | DET | Retention class `bid_8y` | Block | Evidence pack | "Offer records must be retained." |

**Pack parameters (loaded by AU-128 and read by the PDP, AU-264/272/278/280/281/282; every value "verify at time of implementation, as of 28 Nov 2026" unless its VR entry is verified).**

| Parameter | Draft value | Source / note |
|---|---|---|
| federal_default_mode | ASSISTED or MANUAL | RECOMMENDATION-1171 |
| sam_api_key_max_age_days | 90 | VR-64 |
| us_email_entry_cutoff | 17:00 local, one working day before deadline (where 52.215-1(c)(3)(ii)(A)(1) applies, verify) | VR-62 |
| cui_processing | false | Platform policy v0.1 |

### 11.15.31.5 Required disclosures and approved template wording

| Template | Use | English (approved draft wording) | Other languages | Placement |
|---|---|---|---|---|
| TPL-US-PROC-01 | Certification approval prompt | "You are certifying, as an authorized representative of {company}, that the representations and certifications below are current, accurate and complete. False statements may be subject to criminal and civil penalties." | — | Before certification |

### 11.15.31.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-US-PROC-01 | Protected procurement information markers | source selection information; contractor bid or proposal information; see FAR 2.101 and 3.104; FOUO; CUI; NOFORN; ITAR controlled; ECCN | phrase | Block (quarantine) | 006, 009 |

**Prohibited (absolute, no mandate, exception or override can unlock):** scraping SAM.gov; registration actions by the system; AI-authored certifications; ingesting source selection information, CUI or export-controlled data; state/local automation.

### 11.15.31.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Commercial marketplace purchases (e.g. GSA Advantage) after award | Out of scope; manual |
| E-2 | Other transaction agreements (OTAs) | Not FAR-based; MANUAL; counsel row required |

### 11.15.31.8 AI reviewer review guidance (RP-US-PROC)

- **Reviewer:** AG-207/AG-206 applying the AG-086 contract.
- **Look for:** certification inconsistencies; protected-information markers; contact attempts; size claims.
- **Cite:** `RP-US-PROC-0NN` and the pack version only; quote the clause number and span.
- **Escalate (`needs_counsel`):** any OCI question; any marking doubt; RFO clause uncertainty.
- **Never:** author certifications; decide size status.

### 11.15.31.9 Test cases

| ID | Rule | Type | Input (summary) | Expected |
|---|---|---|---|---|
| TC-RP-US-PROC-01 | 001 | Negative | SAM status Expired | Block 001 |
| TC-RP-US-PROC-02 | 002 | Negative | Adapter configured to parse SAM.gov HTML pages | Block 002 at config |
| TC-RP-US-PROC-03 | 003 | Negative | Solicitation requires PIEE upload | ASSISTED |
| TC-RP-US-PROC-04 | 005 | Negative | AI fills 52.204-24 representation | Rejected |
| TC-RP-US-PROC-05 | 009 | Negative | Attachment banner 'CUI//SP-PROPIN' | Upload blocked |
| TC-RP-US-PROC-06 | 013 | Negative | City procurement RFP | MANUAL |

### 11.15.31.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-US-PROC
  title: "Offers to US federal agencies: SAM.gov registration and terms of use, submission per solicitation instructions, late-offer rules, representations and certifications, procurement integrity, conflicts, size status, CUI and export controls"
  version: "0.1-draft"
  state: draft
  jurisdictions: "US-FED (federal executive agencies); state and local procurement out of scope (Block)"
  channels: "BID, DOC"
  audiences: "GOV"
  startups: "AppNAI and any startup bidding in the US; Tenant"
  gates_mandate_types: "MT-BID"
  effective_dates: "FAR and agency deviations as stated in each solicitation (RFO transition: the solicitation's clause set governs) (VR-63)"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  level_cap: "MANUAL or ASSISTED for all federal submissions in v0.1; AUTO only for an e-mail submission the solicitation designates, after counsel approves the solicitation row [RECOMMENDATION-1171]"
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
parameters:
  federal_default_mode: "ASSISTED or MANUAL"
  sam_api_key_max_age_days: "90"
  us_email_entry_cutoff: "17:00 local, one working day before deadline (where 52.215-1(c)(3)(ii)(A)(1) applies, verify)"
  cui_processing: "false"
rules:
  - id: RP-US-PROC-001
    obligation: "An offer shall be submitted only for a bidder with an active SAM.gov registration (UEI) in its legal name, current reps and certs and no active exclusion, checked within 24 hours before submission"
    citation: "FAR 4.1102, 52.204-7, 52.204-8, 9.405 (VR-62)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "SAM entity API: registrationStatus = Active, exclusionStatusFlag = N, reps current"
    severity: "Block"
    override: none
    evidence: "SAM extract"
    remediation_message: "\"The SAM.gov registration is not active or an exclusion is recorded.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-002
    obligation: "The platform shall access SAM.gov only through official APIs and extracts with keys issued to the tenant, shall not scrape or use bots on SAM.gov pages, shall rotate keys at least every 90 days and shall not share individual keys; registration, renewal and reps-and-certs actions shall be performed only by the bidder's authorised Entity Administrator"
    citation: "SAM.gov Terms of Use (VR-64)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Adapter allowlist (API endpoints only); key age ≤ 90 d; no write calls to registration"
    severity: "Block"
    override: none
    evidence: "Key metadata"
    remediation_message: "\"Use the official SAM.gov API with a current key; registration actions are human-only.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-003
    obligation: "Offers shall be submitted by the method, to the address or system and in the format the solicitation specifies; AUTO is permitted only for e-mail submission designated by the solicitation and approved per solicitation by counsel; all other federal submissions are ASSISTED or MANUAL"
    citation: "FAR 52.215-1(c), 14.302 (VR-62); RECOMMENDATION-1171"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "solicitation.submission_method = email AND counsel_row.approved = true → AUTO possible; else ASSISTED/MANUAL"
    severity: "Block"
    override: none
    evidence: "Solicitation row"
    remediation_message: "\"This solicitation requires assisted or manual submission.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-004
    obligation: "Offers shall be received by the exact time specified; for electronic submissions the automated deadline shall be the earlier of the platform hard stop and the time that ensures receipt at the government's initial point of entry by 5:00 p.m. one working day before the deadline where the late-offer exception depends on it"
    citation: "FAR 52.215-1(c)(3) (verify) (VR-62)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "submit_not_after = min(deadline − B_hard, param.us_email_entry_cutoff)"
    severity: "Block"
    override: none
    evidence: "Guard log"
    remediation_message: "\"Too close to the deadline for automated submission.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-005
    obligation: "Every certification and representation (including independent price determination, lobbying, covered telecommunications equipment, Buy American/TAA, size and socio-economic status) shall be made by an authorised person from records; AI shall not author or alter them"
    citation: "FAR 52.203-2, 52.203-5, 52.204-24/25/26 (VR-62); 18 U.S.C. §1001; 31 U.S.C. §3729 (verify)"
    applies_to: "BID, DOC · GOV"
    check: "deterministic"
    detection: "Cert fields bound to records; approval by signatory; AI edits rejected"
    severity: "Block"
    override: none
    evidence: "Signed certifications"
    remediation_message: "\"Certifications must be made by an authorised person from records.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-006
    obligation: "No non-public source selection or contractor bid or proposal information shall be obtained, ingested or used; documents marked as such shall be quarantined and reported to R10"
    citation: "41 U.S.C. §2102; FAR 3.104 (verify)"
    applies_to: "BID, DOC · GOV"
    check: "deterministic_then_ai_review"
    detection: "DET: markings 'Source Selection Information', 'Proprietary'; AI: suspicious provenance"
    severity: "Block"
    override: r10_with_reason
    evidence: "Quarantine record"
    remediation_message: "\"This document may be protected procurement information. It has been quarantined.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-007
    obligation: "Where affiliates may submit offers on the same solicitation, submission shall be held until R10 and US counsel clear it and the Certificate of Independent Price Determination can be truthfully made; organisational conflicts of interest shall be identified"
    citation: "FAR 52.203-2, 9.5 (VR-62)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "As RP-IN-PROC-008 + OCI questionnaire"
    severity: "Block"
    override: none
    evidence: "Clearance record"
    remediation_message: "\"An affiliate is bidding or an OCI question is open. Clearance needed.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-008
    obligation: "Small-business size and socio-economic status shall be claimed only where the SAM record and SBA certification support it for the NAICS code of the solicitation"
    citation: "13 CFR Part 121; 15 U.S.C. §632(w) (verify)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Claimed status ∈ SAM reps for NAICS; SBA certification where required"
    severity: "Block"
    override: none
    evidence: "SAM reps; SBA record"
    remediation_message: "\"This size or status claim is not supported for the solicitation's NAICS code.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-009
    obligation: "Solicitations or attachments marked as CUI, and technical data controlled under ITAR or EAR, shall not be uploaded to or processed by the platform in this release"
    citation: "32 CFR Part 2002; NIST SP 800-171; ITAR; EAR (verify)"
    applies_to: "BID, DOC · GOV"
    check: "deterministic"
    detection: "Marking detector (CUI banners, 'ITAR', ECCN) → Block upload; manual handling"
    severity: "Block"
    override: none
    evidence: "Detector log"
    remediation_message: "\"This material is controlled and cannot be processed on the platform.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-010
    obligation: "Electronic signatures on offers shall be applied by an authorised person by a method the agency accepts"
    citation: "FAR 4.502(d) (verify)"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Signature task L1 unless counsel row allows otherwise"
    severity: "Block"
    override: none
    evidence: "Signature record"
    remediation_message: "\"An authorised person must sign this offer.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-011
    obligation: "The clause set of each solicitation (FAR or RFO deviation text) shall be recorded and the checklist built from it; if the clause set cannot be determined the submission is MANUAL"
    citation: "RFO model deviations (VR-63) [GAP-1170]"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "solicitation.clause_set parsed; unknown → MANUAL"
    severity: "Warn"
    override: r10_with_reason
    evidence: "Clause set record"
    remediation_message: "\"The applicable clause set is unclear. Manual review required.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-012
    obligation: "No agent shall contact contracting officers or evaluators except through the solicitation's designated Q&A channel and only with human-approved questions"
    citation: "FAR 15.201 (verify); procurement integrity"
    applies_to: "EM, VO, BID · GOV"
    check: "deterministic_then_ai_review"
    detection: "Outbound to .gov/.mil domains limited to designated contact; human approval"
    severity: "Block"
    override: r10_with_reason
    evidence: "—"
    remediation_message: "\"Questions to the agency go only through the designated channel after approval.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-013
    obligation: "State, local and tribal procurements shall not use this pack and shall be MANUAL until a dedicated pack exists"
    citation: "Scope"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "buyer.level ≠ federal → MANUAL"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"Only federal procurement is configured. Use manual submission.\""
    effective_from: null  # set at sign-off
  - id: RP-US-PROC-014
    obligation: "Records of each offer shall be kept for at least 8 years (exceeding FAR 4.703 contractor retention where applicable)"
    citation: "FAR 4.703 (verify); MC-24"
    applies_to: "BID · GOV"
    check: "deterministic"
    detection: "Retention class bid_8y"
    severity: "Block"
    override: none
    evidence: "Evidence pack"
    remediation_message: "\"Offer records must be retained.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-US-PROC-01
    name: "Protected procurement information markers"
    match: "phrase"
    severity: "Block (quarantine)"
    used_by: "006, 009"
    terms:
      - "source selection information"
      - "contractor bid or proposal information"
      - "see FAR 2.101 and 3.104"
      - "FOUO"
      - "CUI"
      - "NOFORN"
      - "ITAR controlled"
      - "ECCN"
templates:
  - id: TPL-US-PROC-01
    use: "Certification approval prompt"
    en: "\"You are certifying, as an authorized representative of {company}, that the representations and certifications below are current, accurate and complete. False statements may be subject to criminal and civil penalties.\""
    placement: "Before certification"
```

### 11.15.31.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-US-PROC v0.1-draft → proposed v1.0 |
| Reviewer (name, enrolment/bar no., jurisdiction of admission) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Rules amended (IDs and summary) | _______________________ |
| Pack parameters confirmed (values and sources) | ☐ All ☐ Amended: __________ |
| Citations confirmed against primary text (VR entries) | ☐ VR-62 ☐ VR-63 ☐ VR-64 |
| — | _______________________ |
| Conditions or limitations of the sign-off | _______________________ |
| Next review due | ____ / ____ / ______ (≤ 120 days) |
| R10 approval (name, date) | _______________________ |
| Signature (counsel) / Signature (R10) | _______________ / _______________ |

---

## 11.15.32 RP-IN-VOICE: India AI voice calls: TRAI TCCCPR voice rules, NCPR/DND, 140/1600 series, calling hours, AI disclosure

### 11.15.32.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-IN-VOICE |
| Title | India voice-specific rules for AI inbound and outbound calls, supplementing RP-IN-SMS (DLT, number series, preferences, consent) and RP-IN-DPDP |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | IN (any +91 number, J3; caller or callee in India) |
| Channels | VO (outbound and inbound telecom voice), CH (voice bot), REC (via RP-GL-RECORDING) |
| Audiences | B2B, B2C (adults only) |
| Startups | ALL (EduVerse: no outbound to minors; MedMaarg: no patient topics); Tenant |
| Mandate types gated | MT-OUT (voice); voice activation checklist DEC-861 |
| Legal sources | TCCCPR 2018 as amended incl. Second Amendment Feb 2025 (VR-10) and TRAI 2026 releases (PR 119/2026, draft Third Amendment: content verify) (VR-11, VR-75); Telecommunications Act 2023 (user protection, verify) (VR-75); DPDP Act 2023 and Rules 2025 (VR-01, VR-02); IT Amendment Rules 2026 on SGI (VR-09); CPA 2019 and RP-IN-ADV; CJ-IN-06, CJ-IN-07; Part 11.18a §11.18.5.2–§11.18.5.10; DEC-777, DEC-860…866, DEC-874 |
| Effective dates | TCCCPR Second Amendment phased from Feb 2025 (verify each); SGI Rules from 20 Feb 2026; DPDP Rules phased to 13 May 2027 (VR-01) |
| Owner | R10 Legal/Compliance |
| Review cadence | Quarterly + monthly TRAI horizon scan |
| Expiry / fail-closed | 120 days; voice in India returns `VOICE_NOT_ACTIVE_FOR_JURISDICTION` while not `active`; scrub data unavailable → HOLD |
| Depends on | RP-IN-SMS (rules 001, 006, 007, 011, 012, 014, 015, 017 apply to VO unchanged), RP-IN-DPDP, RP-IN-ADV, RP-COMMIT, RP-GL-RECORDING, RP-HEALTH, RP-EDU-MINORS |

### 11.15.32.2 Plain-language summary

1. Voice is switched on in India only when this pack and RP-IN-SMS are active and the voice activation checklist is complete.
2. Promotional calls come only from 140-series numbers and service calls only from 1600-series numbers. A call that mixes promotion into service is promotional.
3. Before a promotional call, check the National Customer Preference Register (NCPR) within 24 hours. Only DLT digital consent overrides a block.
4. The AI says first, within 2 seconds, that it is an AI assistant with an AI-generated voice, and offers a person (press 0) and an opt-out (press 9). It never claims to be human.
5. Promotional calls run 09:00–19:00, Monday to Saturday. Service calls run 09:00–21:00, recipient local time. Attempts are capped.
6. An opt-out stops calls within a second on the platform and reaches DLT within an hour.
7. Recording follows RP-GL-RECORDING (India profile).

### 11.15.32.3 Definitions

| Term | Definition for this pack |
|---|---|
| Promotional call | A commercial voice call offering or promoting goods, services or interests (TCCCPR); includes any call mixing promotion with service content (VR-10) |
| Service / transactional call | A call about an existing transaction or relationship without promotion |
| AI voice call | A call in which speech is generated by TTS or a speech-to-speech model under AI control (Part 11.18a) |
| First-touch call | The first outbound call from the startup to a contact in a campaign context |
| Abandoned call | A call answered by a person where no AI or agent speech begins within 2 s |

### 11.15.32.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-IN-VOICE-001 | No AI voice call (inbound answering or outbound) shall be made or answered by the AI in India unless this pack, RP-IN-SMS and RP-IN-DPDP are active and the voice activation checklist items 1–10 for the tenant and startup are complete | DEC-860, DEC-861; RP-IN-SMS-001; Part 11.18a §11.18.5.3.4 | VO, CH · ALL | DET | `voice_activation[IN][startup].complete = true` AND packs active | Block | Activation record | "Voice is not activated in India for this startup." |
| RP-IN-VOICE-002 | Every outbound call shall be classified as promotional or service/transactional from the approved script and campaign purpose; a script that contains any promotional element is promotional | TCCCPR Second Amendment (mixed content) (VR-10); RP-IN-SMS-004 | VO · ALL | DET+AI | DET: PL-IN-SMS-01 in service scripts; AI (AG-219): implied promotion | Block | Script classification | "This service call script contains promotion. Use promotional controls." |
| RP-IN-VOICE-003 | Promotional calls shall originate only from 140-series numbers and service/transactional calls only from 1600-series numbers registered to the startup's PE; inbound AI answering only on numbers assigned to the startup | TCCCPR Second Amendment (VR-10); RP-IN-SMS-011; AU-284 | VO · ALL | DET | Caller-ID prefix vs classification; number pool purpose | Block | Number allocation | "Use a 140 number for promotional calls and a 1600 number for service calls." |
| RP-IN-VOICE-004 | A promotional call shall not be placed to a number whose NCPR preference blocks the category unless verified DLT digital consent for that PE and purpose is active; scrub results older than 24 hours or unavailable shall hold the call | TCCCPR (preferences, DCA) (VR-10); RP-IN-SMS-006/007; Part 11.18a §11.18.5.5 | VO · B2B, B2C | DET | `scrub.age ≤ 24 h`; blocked → `dlt_consent.active`; missing → HOLD `REGISTRY_SCRUB_UNAVAILABLE` | Block | Scrub log; DLT consent ID | "This number has blocked promotional calls and there is no valid DLT consent." |
| RP-IN-VOICE-005 | An outbound AI call shall have a lawful basis for the purpose under DPDP (consent recorded in the consent ledger, or a callback request); imported consent shall not be relied on until R10 has reviewed its evidence | DPDP Act s.6, s.7 (VR-02); Part 11.18a §11.18.5.4 | VO · ALL | DET | `consent(contact, voice, purpose).status = valid` AND `source ≠ import_unreviewed` | Block | Consent record | "No valid consent or callback request for this call purpose." |
| RP-IN-VOICE-006 | The first utterance of every AI-handled call shall be the approved disclosure TPL-IN-VO-01 in the call language, starting within 2.0 s of answer (inbound) or of human-speech detection (outbound), naming the brand, stating that the voice is AI-generated, and offering a person; the AI shall answer identity questions truthfully and never claim or imply to be human | RP-IN-SMS-012; BR-V7-AI-01; IT SGI Rules 2026 (VR-09); DEC-862; Part 11.18a D-1…D-4 | VO, CH · ALL | DET | AU-283 template hash + ASR loopback WER ≤ 15%; `disclosure_played_at − answered_at ≤ 2.0 s`; identity intent → TPL-IN-VO-02 | Block | Disclosure event | "The AI disclosure did not play first. Call ended." |
| RP-IN-VOICE-007 | Promotional calls shall offer an opt-out key (9) within the first 15 seconds and at the end, and every call shall offer a person (0 or 'agent') at any time | RP-IN-SMS-008 (TPL-IN-SMS-03); Part 11.18a D-6 | VO · ALL | DET | Script timeline contains TPL-IN-SMS-03 at ≤ 15 s and end; DTMF map 0/9 | Block | Script record | "Add the opt-out and the person option to this script." |
| RP-IN-VOICE-008 | Promotional calls shall be placed only 09:00–19:00 Monday–Saturday and service calls only 09:00–21:00, recipient local time, excluding configured national holidays, and in any case within any legal window TRAI prescribes; calls outside the window are held and rescheduled | RP-IN-SMS-009 (platform window); DEC-777; DEC-765(c); VR-13 [GAP-1174] | VO · ALL | DET | Effective window = intersection(platform window by class, legal window parameter); outside → DEFER with jitter 0–20 min | Block (defer) | Schedule log | "Outside the calling hours for this call type. Rescheduled." |
| RP-IN-VOICE-009 | Attempts per contact per campaign shall not exceed 3, at least 4 hours apart and at most 1 per day; connected promotional calls per contact shall not exceed 1 per 7 days across the startup's campaigns | BRL-ELG-09; Part 11.18a §11.18.5.6 | VO · ALL | DET | Attempt counters at dispatch | Block (defer) | Counter log | "Call attempt limit reached for this contact." |
| RP-IN-VOICE-010 | Abandoned calls shall be avoided: AI or agent speech shall begin within 2 s of answer; an abandonment rate above 1% per campaign per day pauses the campaign for review | Part 11.18a §11.18.5.6; TCCCPR UCC prevention (verify) | VO · ALL | DET | AU-289 monitor | Block (campaign) | Campaign metrics | "Too many abandoned calls. Campaign paused." |
| RP-IN-VOICE-011 | A voicemail shall be left only where the campaign policy allows it and the contact gave express consent or a callback request; it shall use TPL-IN-VO-04 only, last ≤ 30 s, contain no personal or sensitive detail, count as an attempt and be limited to 1 per contact per campaign per 7 days; ringless voicemail drops are prohibited | Part 11.18a VM-1…VM-6; DEC-874 | VO · ALL | DET | AMD result MACHINE → voicemail policy and consent check | Block | Voicemail event | "A voicemail cannot be left for this contact." |
| RP-IN-VOICE-012 | An opt-out expressed by voice, DTMF 9, STOP on any channel or complaint shall end the call politely and suppress the contact for the scope within 1 s on the platform, hold queued calls, and propagate to DLT within the regulatory period (platform target ≤ 1 hour) | RP-IN-SMS-014; AU-288; Part 11.18a §11.18.5.4 | VO · ALL | DET | Opt-out detector (PL-IN-VO-01) → suppression write; sync log | Block | Suppression record | "The contact opted out. No further calls." |
| RP-IN-VOICE-013 | A UCC complaint shall suppress the complainant, open an incident and count to the campaign pause threshold (rate > 0.1% or ≥ 3 in 24 h) | RP-IN-SMS-015; TCCCPR complaint thresholds (5 complaints in 10 days trigger operator action, VR-10) | VO · ALL | DET | Complaint events → AU-289 | Block (campaign) | Incident record | "Campaign paused after complaints." |
| RP-IN-VOICE-014 | No outbound call shall be placed to a person under 18 or with age unknown for EduVerse, and no call shall discuss a patient's health condition for MedMaarg | DEC-030; RP-EDU-MINORS; RP-HEALTH; BRL-ELG-14 | VO · B2C | DET | Age band and vertical flags | Block | — | "This contact cannot be called for this purpose." |
| RP-IN-VOICE-015 | The AI shall never ask for or accept OTPs, PINs, card or bank details or Aadhaar numbers; a payment intent pauses recording and sends a payment link from a licensed PSP on a consented channel | RP-IN-SMS-020; RP-IN-PAY-002/009; TPL-VO-REC-03 | VO, CH · ALL | DET | Intent detector + DLP; PL-IN-PAY-01 | Block | DLP log | "Never ask for codes or card details on a call." |
| RP-IN-VOICE-016 | Only stock or licensed brand voices registered in the voice registry may be used; no voice shall imitate a real, identifiable person; stored AI audio shall carry provenance metadata | IT SGI Rules 2026 (VR-09); RP-IN-ADV-017; DEC-869 | VO · ALL | DET | `voice_id ∈ registry.approved`; storage hook writes `ai_generated=true` | Block | Voice registry record | "This voice is not approved." |
| RP-IN-VOICE-017 | Call scripts shall pass RP-IN-ADV and RP-COMMIT checks (no unapproved claims, prices or commitments), and the AI shall speak only grounded, approved answers | RP-IN-ADV; RP-COMMIT; AG-219; DEC-873 | VO, CH · ALL | DET+AI | Script review; runtime claim check per sentence | Block | Script approval | "The script or answer contains an unapproved claim." |
| RP-IN-VOICE-018 | If a caller indicates an emergency, the AI shall say TPL-IN-VO-05 (112) and transfer to a person immediately | Part 11.18a TPL-VO-EMR-01; duty of care | VO, CH · ALL | DET+AI | Emergency intent detector (phrase list + model) | Block | Event log | "Emergency handling did not run." |

**Pack parameters (loaded by AU-128 and read by the PDP, AU-264/272/278/280/281/282; every value "verify at time of implementation, as of 28 Nov 2026" unless its VR entry is verified).**

| Parameter | Draft value | Source / note |
|---|---|---|
| promotional_window_local | 09:00–19:00 Mon–Sat | RP-IN-SMS-009; DEC-765(c) |
| service_window_local | 09:00–21:00 | DEC-777; Part 11.18a |
| legal_window | unverified (VR-13) — set by counsel | GAP-1174 |
| ncpr_scrub_max_age_hours | 24 | Platform policy |
| disclosure_max_seconds | 2.0 | DEC-862 |
| opt_out_key | 9 | TPL-IN-SMS-03 |
| person_key | 0 | TPL-VO-DISC-01 |
| attempts_per_campaign | 3 (≥ 4 h apart, ≤ 1/day) | Part 11.18a |
| connected_promo_per_7d | 1 | Part 11.18a |
| abandonment_pause_pct | 1.0 | Part 11.18a |
| dlt_revocation_sync_target_minutes | 60 | RP-IN-SMS-014 |

### 11.15.32.5 Required disclosures and approved template wording

| Template | Use | English (approved draft wording) | Hindi (approved draft wording) | Placement |
|---|---|---|---|---|
| TPL-IN-VO-01 | AI disclosure, outbound (= TPL-VO-DISC-01 en/hi; inbound omits {purpose}) | "Hello, this is {brand}'s AI assistant. I'm an automated assistant using an AI-generated voice, calling about {purpose}. You can say 'agent' or press 0 at any time to speak with a person." | "नमस्ते, मैं {brand} की AI सहायक हूँ। मैं AI-जनित आवाज़ वाली स्वचालित सहायक हूँ और {purpose} के बारे में कॉल कर रही हूँ। किसी व्यक्ति से बात करने के लिए कभी भी 'एजेंट' बोलें या 0 दबाएँ।" | First utterance ≤ 2.0 s |
| TPL-IN-VO-02 | Identity challenge (= TPL-VO-DISC-02) | "I'm an AI assistant, not a person. Would you like me to connect you to a colleague now?" | "मैं एक AI सहायक हूँ, कोई व्यक्ति नहीं। क्या मैं आपको अभी किसी सहकर्मी से जोड़ दूँ?" | On any identity question |
| TPL-IN-VO-03 | Promotional opt-out (= TPL-IN-SMS-03) | "To stop promotional calls from {brand}, press 9 now." | "{brand} की प्रचार कॉल बंद करने के लिए अभी 9 दबाएँ।" | ≤ 15 s and at end |
| TPL-IN-VO-04 | Voicemail (= TPL-VO-VM-01) | "This is an automated message from {brand}, recorded with an AI-generated voice, about {purpose_generic}. Please call us back on {callback_number}. To stop these calls, {opt_out_instruction}." | "यह {brand} का स्वचालित संदेश है, जो AI-जनित आवाज़ में रिकॉर्ड किया गया है, {purpose_generic} के बारे में। कृपया हमें {callback_number} पर कॉल करें। ये कॉल बंद करने के लिए {opt_out_instruction}।" | Voicemail only |
| TPL-IN-VO-05 | Emergency (= TPL-VO-EMR-01 with 112) | "If this is an emergency, please hang up and call 112 now. I'm connecting you to a colleague." | "यदि यह आपातकाल है, तो कृपया फ़ोन रखें और अभी 112 पर कॉल करें। मैं आपको एक सहकर्मी से जोड़ रही हूँ।" | On emergency intent |
| TPL-IN-VO-06 | Opt-out confirmation (= TPL-VO-OPT-01) | "Understood. We won't call you again about this. You'll receive a confirmation." | "समझ गई। हम इस बारे में आपको दोबारा कॉल नहीं करेंगे। आपको पुष्टि मिलेगी।" | After opt-out |

### 11.15.32.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-IN-VO-01 | Spoken opt-out | stop calling; don't call me; remove my number; not interested, don't call; कॉल मत करो; फ़ोन मत करना; मेरा नंबर हटाओ; दोबारा कॉल मत करना | phrase + ASR semantic | Block (triggers 012) | 012 |
| PL-IN-VO-02 | Human-impersonation phrases in scripts | I am a real person; this is not a recording; I'm calling personally; मैं असली इंसान हूँ | phrase | Block | 006 |
| PL-IN-VO-03 | Emergency | emergency; ambulance; heart attack; suicide; accident; आपातकाल; एम्बुलेंस; दुर्घटना | phrase + model | Block (triggers 018) | 018 |

**Prohibited (absolute, no mandate, exception or override can unlock):** claiming to be human; promotional calls from 10-digit or 1600 numbers; calls to NCPR-blocked numbers without DLT consent; ringless voicemail; calls to minors; collecting authentication data; cloned real-person voices.

### 11.15.32.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Caller-requested callback at a time the caller chose | Allowed within 08:00–21:00 local even outside the promotional window (ASSUMPTION-1075; R10 to confirm with counsel) |
| E-2 | Inbound call to a published number | Rules 004, 005, 008, 009 do not apply; 001, 006, 012, 014–018 apply |
| E-3 | Human-dialled call with AI assist only (no AI speech) | Rule 006 does not apply; RP-IN-SMS applies; recording per RP-GL-RECORDING |
| E-4 | Draft Third Amendment provisions | Not law until notified; R10 may adopt as platform policy (tightening only) |

### 11.15.32.8 AI reviewer review guidance (RP-IN-VOICE)

- **Reviewer:** AG-219 (voice script compliance reviewer) at script approval; AG-217 (voice compliance QA auditor) on calls; both apply the AG-086 contract.
- **Look for:** hidden promotion in service scripts; human-impersonation wording; unapproved claims; pressure tactics; missing opt-out timing.
- **Cite:** `RP-IN-VOICE-0NN` and the pack version only; quote the script line or transcript timestamp.
- **Escalate (`needs_counsel`):** category debatable (e.g. renewal with discount); any health or education reference; any script in a tier-B language.
- **Never:** decide scrub, window, number-series or consent results.

### 11.15.32.9 Test cases

| ID | Rule | Type | Input (summary) | Expected |
|---|---|---|---|---|
| TC-RP-IN-VOICE-01 | 003 | Negative | Promotional campaign assigned a 1600 number | Block 003 |
| TC-RP-IN-VOICE-02 | 004 | Negative | NCPR fully blocked, no DLT consent | Block 004 |
| TC-RP-IN-VOICE-03 | 004 | Negative | Scrub 25 h old | HOLD `REGISTRY_SCRUB_UNAVAILABLE` |
| TC-RP-IN-VOICE-04 | 006 | Negative | Disclosure starts 2.3 s after human detection | Call ended `DISCLOSURE_FAILED` |
| TC-RP-IN-VOICE-05 | 006 | Negative | Caller asks "are you a real person?", AI says "yes" | Block (eval failure) 006 |
| TC-RP-IN-VOICE-06 | 008 | Boundary | Promotional call scheduled Sat 18:59 IST | Placed |
| TC-RP-IN-VOICE-07 | 008 | Negative | Promotional call Sun 11:00 IST | Deferred to Mon 09:00 + jitter |
| TC-RP-IN-VOICE-08 | 008 | Positive | Service call Fri 20:30 IST | Placed |
| TC-RP-IN-VOICE-09 | 011 | Negative | Voicemail to contact with only web enquiry, no callback request | No voicemail |
| TC-RP-IN-VOICE-10 | 012 | Positive | Caller says "मुझे कॉल मत करो" | TPL-IN-VO-06; suppression ≤ 1 s |
| TC-RP-IN-VOICE-11 | 014 | Negative | EduVerse outbound to contact age unknown | Block 014 |
| TC-RP-IN-VOICE-12 | 002 | Negative | Service script "your order shipped; 10% off next order" | Classified promotional; 140 required |

### 11.15.32.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-IN-VOICE
  title: "India voice-specific rules for AI inbound and outbound calls, supplementing RP-IN-SMS (DLT, number series, preferences, consent) and RP-IN-DPDP"
  version: "0.1-draft"
  state: draft
  jurisdictions: "IN (any +91 number, J3; caller or callee in India)"
  channels: "VO (outbound and inbound telecom voice), CH (voice bot), REC (via RP-GL-RECORDING)"
  audiences: "B2B, B2C (adults only)"
  startups: "ALL (EduVerse: no outbound to minors; MedMaarg: no patient topics); Tenant"
  gates_mandate_types: "MT-OUT (voice); voice activation checklist DEC-861"
  effective_dates: "TCCCPR Second Amendment phased from Feb 2025 (verify each); SGI Rules from 20 Feb 2026; DPDP Rules phased to 13 May 2027 (VR-01)"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  level_cap: "L3 under Active MT-OUT for service calls and consented promotional calls; L1 for first-touch promotional calls"
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
parameters:
  promotional_window_local: "09:00–19:00 Mon–Sat"
  service_window_local: "09:00–21:00"
  legal_window: "unverified (VR-13) — set by counsel"
  ncpr_scrub_max_age_hours: "24"
  disclosure_max_seconds: "2.0"
  opt_out_key: "9"
  person_key: "0"
  attempts_per_campaign: "3 (≥ 4 h apart, ≤ 1/day)"
  connected_promo_per_7d: "1"
  abandonment_pause_pct: "1.0"
  dlt_revocation_sync_target_minutes: "60"
rules:
  - id: RP-IN-VOICE-001
    obligation: "No AI voice call (inbound answering or outbound) shall be made or answered by the AI in India unless this pack, RP-IN-SMS and RP-IN-DPDP are active and the voice activation checklist items 1–10 for the tenant and startup are complete"
    citation: "DEC-860, DEC-861; RP-IN-SMS-001; Part 11.18a §11.18.5.3.4"
    applies_to: "VO, CH · ALL"
    check: "deterministic"
    detection: "voice_activation[IN][startup].complete = true AND packs active"
    severity: "Block"
    override: none
    evidence: "Activation record"
    remediation_message: "\"Voice is not activated in India for this startup.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-002
    obligation: "Every outbound call shall be classified as promotional or service/transactional from the approved script and campaign purpose; a script that contains any promotional element is promotional"
    citation: "TCCCPR Second Amendment (mixed content) (VR-10); RP-IN-SMS-004"
    applies_to: "VO · ALL"
    check: "deterministic_then_ai_review"
    detection: "DET: PL-IN-SMS-01 in service scripts; AI (AG-219): implied promotion"
    severity: "Block"
    override: r10_with_reason
    evidence: "Script classification"
    remediation_message: "\"This service call script contains promotion. Use promotional controls.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-003
    obligation: "Promotional calls shall originate only from 140-series numbers and service/transactional calls only from 1600-series numbers registered to the startup's PE; inbound AI answering only on numbers assigned to the startup"
    citation: "TCCCPR Second Amendment (VR-10); RP-IN-SMS-011; AU-284"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Caller-ID prefix vs classification; number pool purpose"
    severity: "Block"
    override: none
    evidence: "Number allocation"
    remediation_message: "\"Use a 140 number for promotional calls and a 1600 number for service calls.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-004
    obligation: "A promotional call shall not be placed to a number whose NCPR preference blocks the category unless verified DLT digital consent for that PE and purpose is active; scrub results older than 24 hours or unavailable shall hold the call"
    citation: "TCCCPR (preferences, DCA) (VR-10); RP-IN-SMS-006/007; Part 11.18a §11.18.5.5"
    applies_to: "VO · B2B, B2C"
    check: "deterministic"
    detection: "scrub.age ≤ 24 h; blocked → dlt_consent.active; missing → HOLD REGISTRY_SCRUB_UNAVAILABLE"
    severity: "Block"
    override: none
    evidence: "Scrub log; DLT consent ID"
    remediation_message: "\"This number has blocked promotional calls and there is no valid DLT consent.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-005
    obligation: "An outbound AI call shall have a lawful basis for the purpose under DPDP (consent recorded in the consent ledger, or a callback request); imported consent shall not be relied on until R10 has reviewed its evidence"
    citation: "DPDP Act s.6, s.7 (VR-02); Part 11.18a §11.18.5.4"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "consent(contact, voice, purpose).status = valid AND source ≠ import_unreviewed"
    severity: "Block"
    override: none
    evidence: "Consent record"
    remediation_message: "\"No valid consent or callback request for this call purpose.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-006
    obligation: "The first utterance of every AI-handled call shall be the approved disclosure TPL-IN-VO-01 in the call language, starting within 2.0 s of answer (inbound) or of human-speech detection (outbound), naming the brand, stating that the voice is AI-generated, and offering a person; the AI shall answer identity questions truthfully and never claim or imply to be human"
    citation: "RP-IN-SMS-012; BR-V7-AI-01; IT SGI Rules 2026 (VR-09); DEC-862; Part 11.18a D-1…D-4"
    applies_to: "VO, CH · ALL"
    check: "deterministic"
    detection: "AU-283 template hash + ASR loopback WER ≤ 15%; disclosure_played_at − answered_at ≤ 2.0 s; identity intent → TPL-IN-VO-02"
    severity: "Block"
    override: none
    evidence: "Disclosure event"
    remediation_message: "\"The AI disclosure did not play first. Call ended.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-007
    obligation: "Promotional calls shall offer an opt-out key (9) within the first 15 seconds and at the end, and every call shall offer a person (0 or 'agent') at any time"
    citation: "RP-IN-SMS-008 (TPL-IN-SMS-03); Part 11.18a D-6"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Script timeline contains TPL-IN-SMS-03 at ≤ 15 s and end; DTMF map 0/9"
    severity: "Block"
    override: none
    evidence: "Script record"
    remediation_message: "\"Add the opt-out and the person option to this script.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-008
    obligation: "Promotional calls shall be placed only 09:00–19:00 Monday–Saturday and service calls only 09:00–21:00, recipient local time, excluding configured national holidays, and in any case within any legal window TRAI prescribes; calls outside the window are held and rescheduled"
    citation: "RP-IN-SMS-009 (platform window); DEC-777; DEC-765(c); VR-13 [GAP-1174]"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Effective window = intersection(platform window by class, legal window parameter); outside → DEFER with jitter 0–20 min"
    severity: "Block (defer)"
    override: none
    evidence: "Schedule log"
    remediation_message: "\"Outside the calling hours for this call type. Rescheduled.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-009
    obligation: "Attempts per contact per campaign shall not exceed 3, at least 4 hours apart and at most 1 per day; connected promotional calls per contact shall not exceed 1 per 7 days across the startup's campaigns"
    citation: "BRL-ELG-09; Part 11.18a §11.18.5.6"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Attempt counters at dispatch"
    severity: "Block (defer)"
    override: none
    evidence: "Counter log"
    remediation_message: "\"Call attempt limit reached for this contact.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-010
    obligation: "Abandoned calls shall be avoided: AI or agent speech shall begin within 2 s of answer; an abandonment rate above 1% per campaign per day pauses the campaign for review"
    citation: "Part 11.18a §11.18.5.6; TCCCPR UCC prevention (verify)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "AU-289 monitor"
    severity: "Block (campaign)"
    override: none
    evidence: "Campaign metrics"
    remediation_message: "\"Too many abandoned calls. Campaign paused.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-011
    obligation: "A voicemail shall be left only where the campaign policy allows it and the contact gave express consent or a callback request; it shall use TPL-IN-VO-04 only, last ≤ 30 s, contain no personal or sensitive detail, count as an attempt and be limited to 1 per contact per campaign per 7 days; ringless voicemail drops are prohibited"
    citation: "Part 11.18a VM-1…VM-6; DEC-874"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "AMD result MACHINE → voicemail policy and consent check"
    severity: "Block"
    override: none
    evidence: "Voicemail event"
    remediation_message: "\"A voicemail cannot be left for this contact.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-012
    obligation: "An opt-out expressed by voice, DTMF 9, STOP on any channel or complaint shall end the call politely and suppress the contact for the scope within 1 s on the platform, hold queued calls, and propagate to DLT within the regulatory period (platform target ≤ 1 hour)"
    citation: "RP-IN-SMS-014; AU-288; Part 11.18a §11.18.5.4"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Opt-out detector (PL-IN-VO-01) → suppression write; sync log"
    severity: "Block"
    override: none
    evidence: "Suppression record"
    remediation_message: "\"The contact opted out. No further calls.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-013
    obligation: "A UCC complaint shall suppress the complainant, open an incident and count to the campaign pause threshold (rate > 0.1% or ≥ 3 in 24 h)"
    citation: "RP-IN-SMS-015; TCCCPR complaint thresholds (5 complaints in 10 days trigger operator action, VR-10)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Complaint events → AU-289"
    severity: "Block (campaign)"
    override: none
    evidence: "Incident record"
    remediation_message: "\"Campaign paused after complaints.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-014
    obligation: "No outbound call shall be placed to a person under 18 or with age unknown for EduVerse, and no call shall discuss a patient's health condition for MedMaarg"
    citation: "DEC-030; RP-EDU-MINORS; RP-HEALTH; BRL-ELG-14"
    applies_to: "VO · B2C"
    check: "deterministic"
    detection: "Age band and vertical flags"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"This contact cannot be called for this purpose.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-015
    obligation: "The AI shall never ask for or accept OTPs, PINs, card or bank details or Aadhaar numbers; a payment intent pauses recording and sends a payment link from a licensed PSP on a consented channel"
    citation: "RP-IN-SMS-020; RP-IN-PAY-002/009; TPL-VO-REC-03"
    applies_to: "VO, CH · ALL"
    check: "deterministic"
    detection: "Intent detector + DLP; PL-IN-PAY-01"
    severity: "Block"
    override: none
    evidence: "DLP log"
    remediation_message: "\"Never ask for codes or card details on a call.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-016
    obligation: "Only stock or licensed brand voices registered in the voice registry may be used; no voice shall imitate a real, identifiable person; stored AI audio shall carry provenance metadata"
    citation: "IT SGI Rules 2026 (VR-09); RP-IN-ADV-017; DEC-869"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "voice_id ∈ registry.approved; storage hook writes ai_generated=true"
    severity: "Block"
    override: none
    evidence: "Voice registry record"
    remediation_message: "\"This voice is not approved.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-017
    obligation: "Call scripts shall pass RP-IN-ADV and RP-COMMIT checks (no unapproved claims, prices or commitments), and the AI shall speak only grounded, approved answers"
    citation: "RP-IN-ADV; RP-COMMIT; AG-219; DEC-873"
    applies_to: "VO, CH · ALL"
    check: "deterministic_then_ai_review"
    detection: "Script review; runtime claim check per sentence"
    severity: "Block"
    override: r10_with_reason
    evidence: "Script approval"
    remediation_message: "\"The script or answer contains an unapproved claim.\""
    effective_from: null  # set at sign-off
  - id: RP-IN-VOICE-018
    obligation: "If a caller indicates an emergency, the AI shall say TPL-IN-VO-05 (112) and transfer to a person immediately"
    citation: "Part 11.18a TPL-VO-EMR-01; duty of care"
    applies_to: "VO, CH · ALL"
    check: "deterministic_then_ai_review"
    detection: "Emergency intent detector (phrase list + model)"
    severity: "Block"
    override: r10_with_reason
    evidence: "Event log"
    remediation_message: "\"Emergency handling did not run.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-IN-VO-01
    name: "Spoken opt-out"
    match: "phrase + ASR semantic"
    severity: "Block (triggers 012)"
    used_by: "012"
    terms:
      - "stop calling"
      - "don't call me"
      - "remove my number"
      - "not interested, don't call"
      - "कॉल मत करो"
      - "फ़ोन मत करना"
      - "मेरा नंबर हटाओ"
      - "दोबारा कॉल मत करना"
  - id: PL-IN-VO-02
    name: "Human-impersonation phrases in scripts"
    match: "phrase"
    severity: "Block"
    used_by: "006"
    terms:
      - "I am a real person"
      - "this is not a recording"
      - "I'm calling personally"
      - "मैं असली इंसान हूँ"
  - id: PL-IN-VO-03
    name: "Emergency"
    match: "phrase + model"
    severity: "Block (triggers 018)"
    used_by: "018"
    terms:
      - "emergency"
      - "ambulance"
      - "heart attack"
      - "suicide"
      - "accident"
      - "आपातकाल"
      - "एम्बुलेंस"
      - "दुर्घटना"
templates:
  - id: TPL-IN-VO-01
    use: "AI disclosure, outbound (= TPL-VO-DISC-01 en/hi; inbound omits {purpose})"
    en: "\"Hello, this is {brand}'s AI assistant. I'm an automated assistant using an AI-generated voice, calling about {purpose}. You can say 'agent' or press 0 at any time to speak with a person.\""
    placement: "First utterance ≤ 2.0 s"
  - id: TPL-IN-VO-02
    use: "Identity challenge (= TPL-VO-DISC-02)"
    en: "\"I'm an AI assistant, not a person. Would you like me to connect you to a colleague now?\""
    placement: "On any identity question"
  - id: TPL-IN-VO-03
    use: "Promotional opt-out (= TPL-IN-SMS-03)"
    en: "\"To stop promotional calls from {brand}, press 9 now.\""
    placement: "≤ 15 s and at end"
  - id: TPL-IN-VO-04
    use: "Voicemail (= TPL-VO-VM-01)"
    en: "\"This is an automated message from {brand}, recorded with an AI-generated voice, about {purpose_generic}. Please call us back on {callback_number}. To stop these calls, {opt_out_instruction}.\""
    placement: "Voicemail only"
  - id: TPL-IN-VO-05
    use: "Emergency (= TPL-VO-EMR-01 with 112)"
    en: "\"If this is an emergency, please hang up and call 112 now. I'm connecting you to a colleague.\""
    placement: "On emergency intent"
  - id: TPL-IN-VO-06
    use: "Opt-out confirmation (= TPL-VO-OPT-01)"
    en: "\"Understood. We won't call you again about this. You'll receive a confirmation.\""
    placement: "After opt-out"
```

### 11.15.32.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-IN-VOICE v0.1-draft → proposed v1.0 |
| Reviewer (name, enrolment/bar no., jurisdiction of admission) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Rules amended (IDs and summary) | _______________________ |
| Pack parameters confirmed (values and sources) | ☐ All ☐ Amended: __________ |
| Citations confirmed against primary text (VR entries) | ☐ VR-01 ☐ VR-02 ☐ VR-09 ☐ VR-10 ☐ VR-11 ☐ VR-13 ☐ VR-75 |
| Hindi and Tamil wording reviewed by | _______________________ |
| Conditions or limitations of the sign-off | _______________________ |
| Next review due | ____ / ____ / ______ (≤ 120 days) |
| R10 approval (name, date) | _______________________ |
| Signature (counsel) / Signature (R10) | _______________ / _______________ |

---

## 11.15.33 RP-US-VOICE: US AI voice calls: TCPA, prior express written consent, AI voice as artificial voice, DNC, state mini-TCPA laws, calling hours

### 11.15.33.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-US-VOICE |
| Title | US federal and state rules for outbound and inbound AI voice calls: consent standards, DNC and reassigned numbers, identification and opt-out, calling hours, abandonment, caller ID, voicemail, TSR disclosures |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | US (called number with +1 US area code, or US address); state overlay table §11.15.33.12 |
| Channels | VO, CH, REC (via RP-GL-RECORDING) |
| Audiences | B2B, B2C (adults) |
| Startups | ALL; Tenant |
| Mandate types gated | MT-OUT (voice) |
| Legal sources | TCPA 47 U.S.C. §227 (b), (c), (e) and 47 CFR 64.1200 (a)(1)–(3), (a)(7), (a)(10), (b), (c), (d), (f)(9) (VR-66); FCC Declaratory Ruling FCC 24-17 (released 8 Feb 2024) on AI-generated voices (VR-65); FCC final rule on PEWC definition 29 Aug 2025 (VR-30); FCC revocation rules incl. Jan 2026 waiver to 31 Jan 2027 and Sept 2026 Report and Order revising 'revoke all' (VR-67); Telemarketing Sales Rule 16 CFR Part 310 (verify); Truth in Caller ID Act 47 U.S.C. §227(e); STIR/SHAKEN 47 CFR Part 64 Subpart HH (verify); E-SIGN (VR-54); state mini-TCPA and calling-hour laws (FL Stat. 501.059, OK, MD, WA, UT SB 38, VA, CT and others) (VR-68); California B&P Code §17940–17943 bot disclosure (verify) |
| Effective dates | TCPA rules in force; FCC Sept 2026 order effective 30 days after Federal Register publication (verify); Utah SB 38 from May 2026 (verify) |
| Owner | R10 with US counsel |
| Review cadence | Quarterly + monthly state legislative scan |
| Expiry / fail-closed | 120 days; US voice inactive while not `active`; DNC data stale → HOLD |
| Depends on | RP-US-EMAIL (consent records shared), RP-GL-RECORDING (US profiles), RP-COMMIT |

### 11.15.33.2 Plain-language summary

1. An AI voice is an 'artificial voice' under the TCPA. Telemarketing calls using it to residential or wireless numbers need prior express written consent (PEWC). The platform also requires PEWC for every outbound AI marketing call, including to business lines.
2. PEWC is a signed written agreement, which an E-SIGN signature can satisfy. It names the startup, discloses AI or prerecorded calls, gives the number, and is not a condition of purchase. Check the Reassigned Numbers Database before relying on older consent.
3. Scrub the National DNC (data no older than 31 days), the internal DNC list and subscribed state lists.
4. Identify the business at the start, give a callback number, offer an automated opt-out, and honour opt-outs immediately.
5. Calling hours are 09:00–21:00 local, narrowed to 09:00–20:00 in states with 8 p.m. limits. If the time zone is unknown, use the intersection of all possible zones.
6. Keep abandonment ≤ 3% per 30 days (platform alert at 1% a day). Show valid caller ID with A-level attestation. A ringless voicemail counts as a call.

### 11.15.33.3 Definitions

| Term | Definition for this pack |
|---|---|
| Artificial or prerecorded voice | Includes AI-generated voices, voice cloning and similar technologies (FCC 24-17, VR-65) |
| PEWC | An agreement in writing bearing the signature of the person called that clearly authorizes the seller to deliver telemarketing calls using an autodialer or an artificial or prerecorded voice, and the telephone number to which it may be delivered (47 CFR 64.1200(f)(9), VR-66, VR-30) |
| Telemarketing | Initiation of a call for the purpose of encouraging the purchase or rental of, or investment in, property, goods or services (47 CFR 64.1200(f)) |
| Seller | The person on whose behalf a telemarketing call is made; each startup is a separate seller |
| RND | FCC Reassigned Numbers Database |

### 11.15.33.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-US-VOICE-001 | An outbound AI voice call that includes or introduces an advertisement or constitutes telemarketing shall be placed only with PEWC of the called party for that seller (startup) and number; a non-marketing AI voice call to a wireless number shall be placed only with prior express consent; the platform requires PEWC for every outbound AI marketing call including to business numbers | 47 U.S.C. §227(b); 47 CFR 64.1200(a)(2), (a)(3) (VR-66); FCC 24-17 (VR-65); DEC-769 | VO · ALL | DET | `consent(contact, number, seller, purpose=call_ai_marketing).standard = PEWC`; service → `standard ≥ PEC` | Block | PEWC record | "No prior express written consent for AI marketing calls to this number." |
| RP-US-VOICE-002 | A PEWC record shall contain the signed agreement (E-SIGN compliant), the disclosure that calls may use an artificial or AI-generated voice, the seller's name, the number, the statement that consent is not a condition of purchase, the timestamp and the capture evidence; consent obtained from lead generators or imported lists shall not be relied on unless R10 and US counsel approve its evidence | 47 CFR 64.1200(f)(9) (VR-66, VR-30); E-SIGN (VR-54); Part 11.18a §11.18.5.4 | VO · ALL | DET | Required fields present; `source = import` → R10 approval flag | Block | PEWC record fields | "The consent record is incomplete for PEWC." |
| RP-US-VOICE-003 | Before relying on consent obtained before the number's last permanent disconnection date, the RND shall be queried and a 'yes, reassigned' result shall invalidate the consent | 47 CFR 64.1200(m) (RND safe harbor, verify) (VR-66) | VO · ALL | DET | RND query per campaign for consents older than `param.rnd_check_age` | Block | RND query record | "This number may have been reassigned. Consent is invalid until re-confirmed." |
| RP-US-VOICE-004 | Telemarketing calls shall not be placed to numbers on the National DNC Registry (data no older than 31 days), the seller's internal DNC list or subscribed state DNC lists, unless the PEWC covers the call (signed written agreement) | 47 CFR 64.1200(c)(2), (d) (VR-66); state DNC laws (VR-68) | VO · ALL | DET | Scrub age ≤ 31 d; list hits → PEWC check; missing data → HOLD | Block | Scrub record | "This number is on a do-not-call list and no written agreement covers the call." |
| RP-US-VOICE-005 | Calls shall be placed only within the effective window: 09:00–21:00 called-party local time (federal 08:00–21:00 ∩ platform), narrowed by state law (for example 08:00–20:00 in FL, OK, MD, WA, UT, VA → effective 09:00–20:00; CT 09:00–20:00); state holiday or Sunday restrictions apply; unknown or ambiguous zone → intersection of candidate zones | 47 CFR 64.1200(c)(1) (VR-66); state laws (VR-68); DEC-777; Part 11.18a §11.18.5.3.2 | VO · ALL | DET | Window resolver with state table §11.15.33.12 | Block (defer) | Schedule log | "Outside calling hours for this state. Rescheduled." |
| RP-US-VOICE-006 | State attempt limits shall apply (for example no more than 3 commercial calls on the same subject in 24 hours in Florida) together with the platform cap of 3 attempts per campaign, ≥ 4 h apart, ≤ 1 per day | Fla. Stat. 501.059 / 501.616 (verify) (VR-68); Part 11.18a §11.18.5.6 | VO · ALL | DET | Counters by state rule | Block (defer) | Counter log | "Call attempt limit reached." |
| RP-US-VOICE-007 | At the beginning of every artificial-voice call the message shall state the identity of the business responsible for the call and, during or after the message, a telephone number of that business; the AI disclosure TPL-US-VO-01 satisfies this and states that the voice is AI-generated | 47 CFR 64.1200(b)(1), (b)(2) (VR-66); FCC 24-17; Part 11.18a D-1, D-5 | VO · ALL | DET | AU-283 disclosure check; callback number token | Block | Disclosure event | "The call must start with the business identity and AI disclosure." |
| RP-US-VOICE-008 | Every artificial-voice telemarketing call shall provide an automated, interactive opt-out mechanism (voice or key press) at the start, which records the opt-out on the seller's DNC list immediately and ends the call | 47 CFR 64.1200(b)(3) (VR-66); AU-288 | VO · ALL | DET | Script contains TPL-US-VO-02 within first 15 s; DTMF/voice handler | Block | Script record | "Add the automated opt-out at the start of the call." |
| RP-US-VOICE-009 | A revocation of consent made by any reasonable means (voice, text reply, e-mail, web) shall be honoured on the platform immediately and in any case within the period the FCC rules allow; it shall apply to all marketing calls and texts of that seller and, unless the FCC rules in force allow narrower scope and R10 approves, to all robocalls of that seller | 47 CFR 64.1200(a)(10) as revised (VR-67) [GAP-1173]; DEC-769 | VO, SMS, EM · ALL | DET | Revocation detector → suppression (seller scope) ≤ 1 s | Block | Suppression record | "The contact revoked consent. No further calls." |
| RP-US-VOICE-010 | The seller shall maintain a written DNC policy, train staff, and record do-not-call requests made during calls for at least 5 years (platform: retained indefinitely as hashed suppression) | 47 CFR 64.1200(d)(1)–(6) (VR-66) | VO · ALL | DET | Policy document reference in activation checklist; suppression retention class | Block | Policy record | "Upload the written do-not-call policy for this seller." |
| RP-US-VOICE-011 | Abandoned calls shall not exceed 3% of answered calls per campaign per 30-day period; a prerecorded identification and opt-out message shall play within 2 seconds of the completed greeting when no agent is available; calls shall ring at least 15 seconds or 4 rings | 47 CFR 64.1200(a)(7) (VR-66) (verify ring rule) | VO · ALL | DET | AU-289 rolling 30-day ratio; ring timer ≥ `param.ring_min_seconds` | Block (campaign) | Campaign metrics | "Abandonment limit at risk. Campaign paused." |
| RP-US-VOICE-012 | Caller ID shall transmit a valid number assigned to the seller that can be called back during business hours (and name where available), shall not be spoofed, and shall carry STIR/SHAKEN A-level attestation through the originating carrier | 47 CFR 64.1601(e) (verify); Truth in Caller ID Act 47 U.S.C. §227(e); STIR/SHAKEN rules (verify) | VO · ALL | DET | Number registry: owner = seller; attestation level A on test calls | Block | Number verification | "Caller ID is not valid or not attested for this seller." |
| RP-US-VOICE-013 | A voicemail left with an artificial voice, including a ringless voicemail, is a call: it shall be left only with PEWC, use TPL-US-VO-03 and contain the identification and opt-out instructions; ringless voicemail drops are prohibited by platform policy | FCC rulings on ringless voicemail (verify); 47 CFR 64.1200(b) (VR-66); Part 11.18a VM-2, VM-5 | VO · ALL | DET | AMD MACHINE → PEWC check → template | Block | Voicemail event | "A voicemail cannot be left without written consent." |
| RP-US-VOICE-014 | No artificial-voice call shall be made to emergency lines, to guest or patient rooms of healthcare facilities, or to numbers for which the called party is charged, except as the rules permit | 47 CFR 64.1200(a)(1) (VR-66) | VO · ALL | DET | Number-type lookup; PSAP and healthcare-facility blocklists | Block | Lookup record | "This type of number cannot receive AI calls." |
| RP-US-VOICE-015 | Telemarketing calls to consumers shall make the Telemarketing Sales Rule disclosures promptly (seller identity, sales purpose, nature of goods or services, prize-promotion disclosures where relevant) and shall contain no misrepresentation; payment shall not be taken on the call (link via licensed PSP) | 16 CFR 310.3, 310.4 (verify); RP-COMMIT | VO · B2C | DET+AI | Script checks (AG-219) for TSR disclosures; payment intent → link | Block | Script approval | "Add the required telemarketing disclosures and remove payment collection from the call." |
| RP-US-VOICE-016 | Where a state law requires bot disclosure (for example California for bots that incentivise a sale or influence a vote) or other AI-call disclosures, the disclosure shall be given; the platform disclosure TPL-US-VO-01 is given in all states | Cal. B&P Code §17941 (verify); state AI-call laws (verify) (VR-68) | VO, CH · ALL | DET | As rule 007 | Block | Disclosure event | "Give the AI disclosure required in this state." |
| RP-US-VOICE-017 | Where a state requires telemarketer registration, bonding or exemption filing, the seller's status shall be recorded before outbound calls to that state | State telemarketing registration laws (verify) (VR-68) | VO · ALL | DET | `state_registration[state]` ∈ {registered, exempt} | Block | Registration record | "Telemarketing registration for this state is missing." |
| RP-US-VOICE-018 | Consent, scrub and call records needed to defend TCPA claims shall be retained for at least 6 years | 47 U.S.C. §227; 28 U.S.C. §1658 (4-year limitation) (verify); Part 11.18a retention | VO · ALL | DET | Retention class `tcpa_6y` | Block | Retention record | "These records must be retained for 6 years." |
| RP-US-VOICE-019 | No outbound call shall be made to a person under 18 or of unknown age for an education offering, and no call shall discuss health conditions | DEC-030; COPPA context (VR-36); RP-HEALTH | VO · B2C | DET | Age band; vertical flags | Block | — | "This contact cannot be called." |
| RP-US-VOICE-020 | Each startup is a separate seller: consent, DNC lists and opt-outs shall be kept per seller, and consent for one startup shall not be used by another | 47 CFR 64.1200(d)(3), (f)(9) (VR-66); FCC 2025 PEWC rule (VR-30) | VO · ALL | DET | Consent ledger key includes `seller_id` | Block | Consent ledger | "This consent belongs to another startup." |

**Pack parameters (loaded by AU-128 and read by the PDP, AU-264/272/278/280/281/282; every value "verify at time of implementation, as of 28 Nov 2026" unless its VR entry is verified).**

| Parameter | Draft value | Source / note |
|---|---|---|
| federal_window_local | 08:00–21:00 | 47 CFR 64.1200(c)(1) |
| platform_window_local | 09:00–21:00 | DEC-777 |
| state_8pm_states | FL, OK, MD, WA, UT, VA (verify; list maintained by counsel) | VR-68 |
| national_dnc_max_age_days | 31 | VR-66 (verify) |
| abandonment_max_pct_30d | 3.0 | 47 CFR 64.1200(a)(7) |
| ring_min_seconds | 15 | verify |
| rnd_check_age | consents older than the last permanent disconnect date | verify |
| fl_same_subject_calls_24h | 3 | VR-68 (verify) |
| retention_years | 6 | Platform policy |

### 11.15.33.5 Required disclosures and approved template wording

| Template | Use | English (approved draft wording) | Other languages | Placement |
|---|---|---|---|---|
| TPL-US-VO-01 | Identification and AI disclosure (= TPL-VO-DISC-01 en) | "Hello, this is {brand}'s AI assistant. I'm an automated assistant using an AI-generated voice, calling about {purpose}. You can reach {brand} at {callback_number}. Say 'agent' or press 0 at any time to speak with a person." | es: pending (verify) | First utterance ≤ 2.0 s |
| TPL-US-VO-02 | Automated opt-out | "If you don't want calls from {brand}, say 'stop' or press 9 now and we'll add you to our do-not-call list." | es: pending | ≤ 15 s |
| TPL-US-VO-03 | Voicemail (PEWC only) | "This is an automated message from {brand}, recorded with an AI-generated voice, about {purpose_generic}. Call us at {callback_number}. To stop these calls, call {callback_number} and press 9." | es: pending | Voicemail only |
| TPL-US-VO-04 | PEWC capture text (web form, unticked box) | "By checking this box and signing, I agree that {brand} may call me at the number above with marketing calls, including calls that use an AI-generated or prerecorded voice. Consent is not required to buy anything. I can revoke it at any time." | es: pending | Form; E-SIGN signature |

### 11.15.33.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-US-VO-01 | Revocation phrases | stop; stop calling; remove me; do not call; unsubscribe; take me off your list; quit; cancel | phrase + ASR semantic | Block (triggers 009) | 009 |

**Prohibited (absolute, no mandate, exception or override can unlock):** AI marketing calls without PEWC; spoofed caller ID; ringless voicemail; calls to emergency or healthcare-room lines; sharing consent between startups.

### 11.15.33.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Inbound AI answering | Rules 001, 003–006, 011, 013 do not apply; 007 (disclosure), 016, 019 apply; recording per RP-GL-RECORDING |
| E-2 | Calls to a business with an established business relationship (EBR) by a human | EBR may satisfy DNC rules for live calls (verify); never for AI calls (platform) |
| E-3 | Exempt informational calls (healthcare, banks) under FCC exemptions | Not used by the portfolio; Block |

### 11.15.33.8 AI reviewer review guidance (RP-US-VOICE)

- **Reviewer:** AG-219 for scripts; AG-217 for call audits (AG-086 contract).
- **Look for:** missing TSR disclosures; misrepresentation; pressure; human impersonation; payment collection on call.
- **Cite:** `RP-US-VOICE-0NN` and the pack version only; quote script line or timestamp.
- **Escalate (`needs_counsel`):** consent evidence from third parties; ambiguous state; B2C prize or investment content.
- **Never:** decide consent, DNC, window or RND results.

### 11.15.33.9 Test cases

| ID | Rule | Type | Input (summary) | Expected |
|---|---|---|---|---|
| TC-RP-US-VOICE-01 | 001 | Negative | AI marketing call, consent = web form without signature | Block 001 |
| TC-RP-US-VOICE-02 | 003 | Negative | RND returns reassigned for 2024 consent | Block 003 |
| TC-RP-US-VOICE-03 | 004 | Negative | National DNC data 32 days old | HOLD |
| TC-RP-US-VOICE-04 | 005 | Boundary | FL contact, 19:59 local | Placed |
| TC-RP-US-VOICE-05 | 005 | Negative | FL contact, 20:00 local | Deferred |
| TC-RP-US-VOICE-06 | 005 | Edge | Mobile number, zone unknown (ET/PT candidates), 10:00 ET | Deferred until 12:00 ET (09:00 PT) |
| TC-RP-US-VOICE-07 | 008 | Negative | Script with opt-out at 40 s | Block 008 |
| TC-RP-US-VOICE-08 | 009 | Positive | Contact replies STOP to SMS from same seller | Voice calls suppressed ≤ 1 s |
| TC-RP-US-VOICE-09 | 011 | Negative | 30-day abandonment 3.1% | Campaign paused |
| TC-RP-US-VOICE-10 | 013 | Negative | Ringless voicemail requested | Block 013 |
| TC-RP-US-VOICE-11 | 020 | Negative | AppNAI campaign uses OrganicSpec PEWC | Block 020 |

### 11.15.33.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-US-VOICE
  title: "US federal and state rules for outbound and inbound AI voice calls: consent standards, DNC and reassigned numbers, identification and opt-out, calling hours, abandonment, caller ID, voicemail, TSR disclosures"
  version: "0.1-draft"
  state: draft
  jurisdictions: "US (called number with +1 US area code, or US address); state overlay table §11.15.33.12"
  channels: "VO, CH, REC (via RP-GL-RECORDING)"
  audiences: "B2B, B2C (adults)"
  startups: "ALL; Tenant"
  gates_mandate_types: "MT-OUT (voice)"
  effective_dates: "TCPA rules in force; FCC Sept 2026 order effective 30 days after Federal Register publication (verify); Utah SB 38 from May 2026 (verify)"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  level_cap: "L3 under Active MT-OUT only with PEWC on file; otherwise no outbound AI call"
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
parameters:
  federal_window_local: "08:00–21:00"
  platform_window_local: "09:00–21:00"
  state_8pm_states: "FL, OK, MD, WA, UT, VA (verify; list maintained by counsel)"
  national_dnc_max_age_days: "31"
  abandonment_max_pct_30d: "3.0"
  ring_min_seconds: "15"
  rnd_check_age: "consents older than the last permanent disconnect date"
  fl_same_subject_calls_24h: "3"
  retention_years: "6"
rules:
  - id: RP-US-VOICE-001
    obligation: "An outbound AI voice call that includes or introduces an advertisement or constitutes telemarketing shall be placed only with PEWC of the called party for that seller (startup) and number; a non-marketing AI voice call to a wireless number shall be placed only with prior express consent; the platform requires PEWC for every outbound AI marketing call including to business numbers"
    citation: "47 U.S.C. §227(b); 47 CFR 64.1200(a)(2), (a)(3) (VR-66); FCC 24-17 (VR-65); DEC-769"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "consent(contact, number, seller, purpose=call_ai_marketing).standard = PEWC; service → standard ≥ PEC"
    severity: "Block"
    override: none
    evidence: "PEWC record"
    remediation_message: "\"No prior express written consent for AI marketing calls to this number.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-002
    obligation: "A PEWC record shall contain the signed agreement (E-SIGN compliant), the disclosure that calls may use an artificial or AI-generated voice, the seller's name, the number, the statement that consent is not a condition of purchase, the timestamp and the capture evidence; consent obtained from lead generators or imported lists shall not be relied on unless R10 and US counsel approve its evidence"
    citation: "47 CFR 64.1200(f)(9) (VR-66, VR-30); E-SIGN (VR-54); Part 11.18a §11.18.5.4"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Required fields present; source = import → R10 approval flag"
    severity: "Block"
    override: none
    evidence: "PEWC record fields"
    remediation_message: "\"The consent record is incomplete for PEWC.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-003
    obligation: "Before relying on consent obtained before the number's last permanent disconnection date, the RND shall be queried and a 'yes, reassigned' result shall invalidate the consent"
    citation: "47 CFR 64.1200(m) (RND safe harbor, verify) (VR-66)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "RND query per campaign for consents older than param.rnd_check_age"
    severity: "Block"
    override: none
    evidence: "RND query record"
    remediation_message: "\"This number may have been reassigned. Consent is invalid until re-confirmed.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-004
    obligation: "Telemarketing calls shall not be placed to numbers on the National DNC Registry (data no older than 31 days), the seller's internal DNC list or subscribed state DNC lists, unless the PEWC covers the call (signed written agreement)"
    citation: "47 CFR 64.1200(c)(2), (d) (VR-66); state DNC laws (VR-68)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Scrub age ≤ 31 d; list hits → PEWC check; missing data → HOLD"
    severity: "Block"
    override: none
    evidence: "Scrub record"
    remediation_message: "\"This number is on a do-not-call list and no written agreement covers the call.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-005
    obligation: "Calls shall be placed only within the effective window: 09:00–21:00 called-party local time (federal 08:00–21:00 ∩ platform), narrowed by state law (for example 08:00–20:00 in FL, OK, MD, WA, UT, VA → effective 09:00–20:00; CT 09:00–20:00); state holiday or Sunday restrictions apply; unknown or ambiguous zone → intersection of candidate zones"
    citation: "47 CFR 64.1200(c)(1) (VR-66); state laws (VR-68); DEC-777; Part 11.18a §11.18.5.3.2"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Window resolver with state table §11.15.33.12"
    severity: "Block (defer)"
    override: none
    evidence: "Schedule log"
    remediation_message: "\"Outside calling hours for this state. Rescheduled.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-006
    obligation: "State attempt limits shall apply (for example no more than 3 commercial calls on the same subject in 24 hours in Florida) together with the platform cap of 3 attempts per campaign, ≥ 4 h apart, ≤ 1 per day"
    citation: "Fla. Stat. 501.059 / 501.616 (verify) (VR-68); Part 11.18a §11.18.5.6"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Counters by state rule"
    severity: "Block (defer)"
    override: none
    evidence: "Counter log"
    remediation_message: "\"Call attempt limit reached.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-007
    obligation: "At the beginning of every artificial-voice call the message shall state the identity of the business responsible for the call and, during or after the message, a telephone number of that business; the AI disclosure TPL-US-VO-01 satisfies this and states that the voice is AI-generated"
    citation: "47 CFR 64.1200(b)(1), (b)(2) (VR-66); FCC 24-17; Part 11.18a D-1, D-5"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "AU-283 disclosure check; callback number token"
    severity: "Block"
    override: none
    evidence: "Disclosure event"
    remediation_message: "\"The call must start with the business identity and AI disclosure.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-008
    obligation: "Every artificial-voice telemarketing call shall provide an automated, interactive opt-out mechanism (voice or key press) at the start, which records the opt-out on the seller's DNC list immediately and ends the call"
    citation: "47 CFR 64.1200(b)(3) (VR-66); AU-288"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Script contains TPL-US-VO-02 within first 15 s; DTMF/voice handler"
    severity: "Block"
    override: none
    evidence: "Script record"
    remediation_message: "\"Add the automated opt-out at the start of the call.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-009
    obligation: "A revocation of consent made by any reasonable means (voice, text reply, e-mail, web) shall be honoured on the platform immediately and in any case within the period the FCC rules allow; it shall apply to all marketing calls and texts of that seller and, unless the FCC rules in force allow narrower scope and R10 approves, to all robocalls of that seller"
    citation: "47 CFR 64.1200(a)(10) as revised (VR-67) [GAP-1173]; DEC-769"
    applies_to: "VO, SMS, EM · ALL"
    check: "deterministic"
    detection: "Revocation detector → suppression (seller scope) ≤ 1 s"
    severity: "Block"
    override: none
    evidence: "Suppression record"
    remediation_message: "\"The contact revoked consent. No further calls.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-010
    obligation: "The seller shall maintain a written DNC policy, train staff, and record do-not-call requests made during calls for at least 5 years (platform: retained indefinitely as hashed suppression)"
    citation: "47 CFR 64.1200(d)(1)–(6) (VR-66)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Policy document reference in activation checklist; suppression retention class"
    severity: "Block"
    override: none
    evidence: "Policy record"
    remediation_message: "\"Upload the written do-not-call policy for this seller.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-011
    obligation: "Abandoned calls shall not exceed 3% of answered calls per campaign per 30-day period; a prerecorded identification and opt-out message shall play within 2 seconds of the completed greeting when no agent is available; calls shall ring at least 15 seconds or 4 rings"
    citation: "47 CFR 64.1200(a)(7) (VR-66) (verify ring rule)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "AU-289 rolling 30-day ratio; ring timer ≥ param.ring_min_seconds"
    severity: "Block (campaign)"
    override: none
    evidence: "Campaign metrics"
    remediation_message: "\"Abandonment limit at risk. Campaign paused.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-012
    obligation: "Caller ID shall transmit a valid number assigned to the seller that can be called back during business hours (and name where available), shall not be spoofed, and shall carry STIR/SHAKEN A-level attestation through the originating carrier"
    citation: "47 CFR 64.1601(e) (verify); Truth in Caller ID Act 47 U.S.C. §227(e); STIR/SHAKEN rules (verify)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Number registry: owner = seller; attestation level A on test calls"
    severity: "Block"
    override: none
    evidence: "Number verification"
    remediation_message: "\"Caller ID is not valid or not attested for this seller.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-013
    obligation: "A voicemail left with an artificial voice, including a ringless voicemail, is a call: it shall be left only with PEWC, use TPL-US-VO-03 and contain the identification and opt-out instructions; ringless voicemail drops are prohibited by platform policy"
    citation: "FCC rulings on ringless voicemail (verify); 47 CFR 64.1200(b) (VR-66); Part 11.18a VM-2, VM-5"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "AMD MACHINE → PEWC check → template"
    severity: "Block"
    override: none
    evidence: "Voicemail event"
    remediation_message: "\"A voicemail cannot be left without written consent.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-014
    obligation: "No artificial-voice call shall be made to emergency lines, to guest or patient rooms of healthcare facilities, or to numbers for which the called party is charged, except as the rules permit"
    citation: "47 CFR 64.1200(a)(1) (VR-66)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Number-type lookup; PSAP and healthcare-facility blocklists"
    severity: "Block"
    override: none
    evidence: "Lookup record"
    remediation_message: "\"This type of number cannot receive AI calls.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-015
    obligation: "Telemarketing calls to consumers shall make the Telemarketing Sales Rule disclosures promptly (seller identity, sales purpose, nature of goods or services, prize-promotion disclosures where relevant) and shall contain no misrepresentation; payment shall not be taken on the call (link via licensed PSP)"
    citation: "16 CFR 310.3, 310.4 (verify); RP-COMMIT"
    applies_to: "VO · B2C"
    check: "deterministic_then_ai_review"
    detection: "Script checks (AG-219) for TSR disclosures; payment intent → link"
    severity: "Block"
    override: r10_with_reason
    evidence: "Script approval"
    remediation_message: "\"Add the required telemarketing disclosures and remove payment collection from the call.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-016
    obligation: "Where a state law requires bot disclosure (for example California for bots that incentivise a sale or influence a vote) or other AI-call disclosures, the disclosure shall be given; the platform disclosure TPL-US-VO-01 is given in all states"
    citation: "Cal. B&P Code §17941 (verify); state AI-call laws (verify) (VR-68)"
    applies_to: "VO, CH · ALL"
    check: "deterministic"
    detection: "As rule 007"
    severity: "Block"
    override: none
    evidence: "Disclosure event"
    remediation_message: "\"Give the AI disclosure required in this state.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-017
    obligation: "Where a state requires telemarketer registration, bonding or exemption filing, the seller's status shall be recorded before outbound calls to that state"
    citation: "State telemarketing registration laws (verify) (VR-68)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "state_registration[state] ∈ {registered, exempt}"
    severity: "Block"
    override: none
    evidence: "Registration record"
    remediation_message: "\"Telemarketing registration for this state is missing.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-018
    obligation: "Consent, scrub and call records needed to defend TCPA claims shall be retained for at least 6 years"
    citation: "47 U.S.C. §227; 28 U.S.C. §1658 (4-year limitation) (verify); Part 11.18a retention"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Retention class tcpa_6y"
    severity: "Block"
    override: none
    evidence: "Retention record"
    remediation_message: "\"These records must be retained for 6 years.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-019
    obligation: "No outbound call shall be made to a person under 18 or of unknown age for an education offering, and no call shall discuss health conditions"
    citation: "DEC-030; COPPA context (VR-36); RP-HEALTH"
    applies_to: "VO · B2C"
    check: "deterministic"
    detection: "Age band; vertical flags"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"This contact cannot be called.\""
    effective_from: null  # set at sign-off
  - id: RP-US-VOICE-020
    obligation: "Each startup is a separate seller: consent, DNC lists and opt-outs shall be kept per seller, and consent for one startup shall not be used by another"
    citation: "47 CFR 64.1200(d)(3), (f)(9) (VR-66); FCC 2025 PEWC rule (VR-30)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Consent ledger key includes seller_id"
    severity: "Block"
    override: none
    evidence: "Consent ledger"
    remediation_message: "\"This consent belongs to another startup.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-US-VO-01
    name: "Revocation phrases"
    match: "phrase + ASR semantic"
    severity: "Block (triggers 009)"
    used_by: "009"
    terms:
      - "stop"
      - "stop calling"
      - "remove me"
      - "do not call"
      - "unsubscribe"
      - "take me off your list"
      - "quit"
      - "cancel"
templates:
  - id: TPL-US-VO-01
    use: "Identification and AI disclosure (= TPL-VO-DISC-01 en)"
    en: "\"Hello, this is {brand}'s AI assistant. I'm an automated assistant using an AI-generated voice, calling about {purpose}. You can reach {brand} at {callback_number}. Say 'agent' or press 0 at any time to speak with a person.\""
    placement: "First utterance ≤ 2.0 s"
  - id: TPL-US-VO-02
    use: "Automated opt-out"
    en: "\"If you don't want calls from {brand}, say 'stop' or press 9 now and we'll add you to our do-not-call list.\""
    placement: "≤ 15 s"
  - id: TPL-US-VO-03
    use: "Voicemail (PEWC only)"
    en: "\"This is an automated message from {brand}, recorded with an AI-generated voice, about {purpose_generic}. Call us at {callback_number}. To stop these calls, call {callback_number} and press 9.\""
    placement: "Voicemail only"
  - id: TPL-US-VO-04
    use: "PEWC capture text (web form, unticked box)"
    en: "\"By checking this box and signing, I agree that {brand} may call me at the number above with marketing calls, including calls that use an AI-generated or prerecorded voice. Consent is not required to buy anything. I can revoke it at any time.\""
    placement: "Form; E-SIGN signature"
```

### 11.15.33.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-US-VOICE v0.1-draft → proposed v1.0 |
| Reviewer (name, enrolment/bar no., jurisdiction of admission) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Rules amended (IDs and summary) | _______________________ |
| Pack parameters confirmed (values and sources) | ☐ All ☐ Amended: __________ |
| Citations confirmed against primary text (VR entries) | ☐ VR-30 ☐ VR-36 ☐ VR-54 ☐ VR-65 ☐ VR-66 ☐ VR-67 ☐ VR-68 |
| Spanish wording reviewed by (if used) | _______________________ |
| Conditions or limitations of the sign-off | _______________________ |
| Next review due | ____ / ____ / ______ (≤ 120 days) |
| R10 approval (name, date) | _______________________ |
| Signature (counsel) / Signature (R10) | _______________ / _______________ |

### 11.15.33.12 State overlay (counsel maintains; values verify, as of 28 Nov 2026)

| State | Effective platform window | Extra rules (summary, verify) | Recording model (RP-GL-RECORDING) |
|---|---|---|---|
| FL | 09:00–20:00 | FTSA: autodialer consent; ≤ 3 calls / 24 h same subject; state DNC | All-party |
| OK | 09:00–20:00 | OTSA modelled on FTSA | One-party |
| MD | 09:00–20:00 | Stop the Spam Calls Act | All-party |
| WA | 09:00–20:00 | Telemarketing rules; CEMA for texts | All-party |
| UT | 09:00–20:00 | SB 38 from May 2026 | One-party |
| VA | 09:00–20:00 | Telephone Privacy Protection Act | One-party |
| CT | 09:00–20:00 | Mini-TCPA (2023) | Hybrid: civil notice for phone recording |
| CA | 09:00–21:00 | Bot disclosure §17941; CCPA/CPRA notices | All-party (PC §632) |
| TX | 09:00–21:00 | Telemarketing registration (verify) | One-party |
| Others | 09:00–21:00 | Counsel to add rows; unknown state → strictest row | Unknown → all-party |


---

## 11.15.34 RP-EU-VOICE: EU/EEA (and UK profile) AI voice calls: ePrivacy and GDPR for calls, AI Act disclosure, national opt-in and opt-out registers

### 11.15.34.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-EU-VOICE |
| Title | EU/EEA rules for AI voice calls (automated calling systems), national telemarketing regimes and registers, calling windows, GDPR transparency and objection, AI Act transparency; UK PECR profile for separate UK counsel sign-off |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | EU/EEA (member-state profile required, §11.15.34.12); UK profile (rows marked UK) — UK activation also needs UK counsel sign-off (ADR-184) |
| Channels | VO, CH, REC (via RP-GL-RECORDING) |
| Audiences | B2B, B2C (adults) |
| Startups | ALL; Tenant |
| Mandate types gated | MT-OUT (voice) |
| Legal sources | ePrivacy Directive 2002/58/EC Art. 13(1), 13(3), 13(5) and national implementations (VR-25); GDPR Arts 6, 7, 12–14, 21, 22, 35 (VR-24); AI Act (EU) 2024/1689 Art. 5(1)(f), Art. 50(1)–(2) (VR-22, VR-23); France: Code de la consommation L.223-1 ff. as amended by the law of 30 Jun 2025, décret 2026-662 of 23 Jul 2026, décret 2022-1313 (VR-69); Netherlands Telecommunicatiewet art. 11.7 (VR-70); Italy Registro Pubblico delle Opposizioni (VR-71); Spain Ley 11/2022 General de Telecomunicaciones art. 66 (VR-71); Germany UWG §7(2) no. 1, §7a (VR-72); UK PECR regs 19, 21, 24 and Data (Use and Access) Act 2025 (VR-38); CJ-EU-01…10; CJ-UK-02; Part 11.18a §11.18.5.3 |
| Effective dates | AI Act Art. 50 from 2 Aug 2026; France opt-in from 11 Aug 2026 and Bloctel discontinued (VR-69); Netherlands existing-customer exception abolished 1 Jul 2026 (VR-70, verify) |
| Owner | R10 with EU counsel (and UK counsel for UK rows) |
| Review cadence | Quarterly + per member-state change |
| Expiry / fail-closed | 120 days; member state without a completed profile row → outbound voice Block (inbound with disclosure allowed only if the row says so) |
| Depends on | RP-EU-MKT, RP-EU-AI, RP-GL-RECORDING, RP-COMMIT |

### 11.15.34.2 Plain-language summary

1. An AI voice call is a call by an automated calling system. Direct marketing by such calls needs the person's prior consent in every member state, whatever national registers say. The platform applies the same opt-in standard to business numbers (DEC-769).
2. Human-dialled calls follow each member state's own regime. France is opt-in from 11 Aug 2026, with consent valid for at most a year and Bloctel discontinued. The Netherlands is opt-in. Italy and Spain have their own registers or consent rules. Profiles are in §11.15.34.12.
3. France: calls only Monday to Friday 10:00–13:00 and 14:00–20:00, with at most 4 attempts per consumer in 30 days.
4. Say first that this is an AI assistant (AI Act Art. 50). Give a short GDPR notice with a link, and honour objections to direct marketing at once.
5. Show a valid caller ID. Do not infer individuals' emotions. Mark stored AI audio as AI-generated.
6. UK rows follow PECR: prior consent for automated calls, a TPS/CTPS check for live calls, and valid caller ID.

### 11.15.34.3 Definitions

| Term | Definition for this pack |
|---|---|
| Automated calling system | A system that makes calls without human intervention (ePrivacy Art. 13(1)); the panel treats AI voice agents as such [verify per state] |
| Direct marketing | Communication of advertising or marketing material directed to particular individuals (GDPR Recital 47, Art. 21(2)); for ePrivacy, includes promotion of the startup's offerings |
| Opt-out register | National register of subscribers objecting to marketing calls (e.g. Italy RPO; formerly France Bloctel; UK TPS/CTPS) |
| Member-state profile | Row of §11.15.34.12 giving consent model, register, windows, attempt limits and recording model for a state |

### 11.15.34.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-EU-VOICE-001 | Direct-marketing calls made by AI voice to subscribers in the EU/EEA shall be made only with the called subscriber's prior consent that meets GDPR Art. 4(11) and Art. 7, recorded per purpose; the platform applies this standard also to legal-person subscribers (DEC-769) | ePrivacy Art. 13(1) (VR-25); GDPR Arts 6(1)(a), 7 (VR-24); DEC-769 | VO · ALL | DET | `consent(contact, voice, call_ai_marketing).standard = opt_in` AND evidence present | Block | Consent record | "AI marketing calls in the EU need the person's prior opt-in." |
| RP-EU-VOICE-002 | Human-dialled marketing calls (including AI-assisted calls where only a human speaks) shall follow the member-state profile (opt-in, register scrub, existing-customer exception) and shall never use an AI voice | ePrivacy Art. 13(3) and national law (VR-25, VR-69…72) | VO · ALL | DET | Profile row for `contact.member_state`; register scrub age ≤ profile limit | Block | Profile row; scrub record | "This call does not meet this country's telemarketing rules." |
| RP-EU-VOICE-003 | France: consumer telephone canvassing shall be made only with the consumer's prior consent obtained and kept per the décret of 23 Jul 2026, valid for no more than 1 year, except for calls relating to an existing contract as the law allows; contracts concluded after an unlawful call are void, so such orders shall be blocked | Code de la consommation L.223-1 ff. as amended (law of 30 Jun 2025) and décret 2026-662 (VR-69) [GAP-1172] | VO · B2C | DET | `member_state = FR` AND consumer → consent age ≤ 365 d OR `existing_contract_topic = true` | Block | Consent record (FR) | "Calls to consumers in France need consent from the last 12 months." |
| RP-EU-VOICE-004 | France: calls to consumers shall be placed only Monday–Friday 10:00–13:00 and 14:00–20:00 local time, never on Saturdays, Sundays or public holidays, and no more than 4 call attempts per consumer per 30 days across the startup's campaigns | Décret 2022-1313 (VR-69, verify continued application) | VO · B2C | DET | FR window resolver; attempt counter 30 d | Block (defer) | Schedule log | "Outside the French calling hours or attempt limit. Rescheduled." |
| RP-EU-VOICE-005 | All other EEA calls shall be placed within 09:00–21:00 recipient local time (DEC-777) intersected with any national window in the profile | DEC-777; national law (verify) | VO · ALL | DET | Window resolver | Block (defer) | Schedule log | "Outside calling hours. Rescheduled." |
| RP-EU-VOICE-006 | Calls shall present a valid caller ID assigned to the startup that can be called back; caller-ID suppression is prohibited for marketing calls; French calls use numbers from ARCEP-designated ranges for automated or canvassing calls where required | National law, e.g. Germany TKG and UWG (verify); ARCEP numbering decisions (verify) (VR-72, VR-69) | VO · ALL | DET | Number registry and CLI test | Block | Number record | "Use a valid, displayed caller ID from the permitted range." |
| RP-EU-VOICE-007 | The first utterance shall inform the person that they are interacting with an AI system (TPL-EU-VO-01), unless obvious, and AI-generated audio stored or played as content shall be marked as AI-generated in machine-readable form | AI Act Art. 50(1), 50(2) (VR-22); Part 11.18a D-1, D-7 | VO, CH · ALL | DET | AU-283 disclosure; storage provenance hook | Block | Disclosure event | "The AI disclosure must come first." |
| RP-EU-VOICE-008 | The call shall give a short privacy notice (controller identity, purpose, right to object) and a link or callback route to the full notice, and an objection to direct marketing shall be honoured immediately for all channels | GDPR Arts 13/14, 21(2)–(3) (VR-24) | VO · ALL | DET | TPL-EU-VO-02 in script; objection → suppression ≤ 1 s | Block | Notice event; suppression | "Add the short privacy notice and honour objections immediately." |
| RP-EU-VOICE-009 | No emotion recognition or individual sentiment scoring of callers or employees shall be performed; only aggregated, anonymous call-quality metrics | AI Act Art. 5(1)(f) (workplace) and Annex III (VR-23); Part 11.18a §11.18.5.12 | VO · ALL | DET | Model registry: emotion models disabled for EU tenants; summary schema has no sentiment field | Block | Registry config | "Emotion recognition is not allowed." |
| RP-EU-VOICE-010 | Consent evidence shall be kept per member-state rules (for example Germany: documented and kept 5 years; France: as the décret requires) and at least 6 years on the platform | UWG §7a (VR-72); décret 2026-662 (VR-69); GDPR Art. 7(1) | VO · ALL | DET | Retention class `voice_consent_6y` | Block | Consent evidence | "Consent evidence must be retained." |
| RP-EU-VOICE-011 | A voicemail with an AI voice shall be left only with documented prior opt-in for that purpose | ePrivacy Art. 13(1) (VR-25); Part 11.18a VM-2 | VO · ALL | DET | AMD MACHINE → opt-in check | Block | Voicemail event | "A voicemail cannot be left without opt-in." |
| RP-EU-VOICE-012 | Personal data of EU calls (audio, transcripts, summaries, consent) shall be processed in the EU region; any non-EEA provider in the voice stack requires a Chapter V mechanism and a DPIA covering it | GDPR Arts 35, 44–49 (VR-24); DEC-772 | VO, REC · ALL | DET | Provider registry region and transfer mechanism; DPIA ID | Block | Registry; DPIA | "This provider is not approved for EU call data." |
| RP-EU-VOICE-013 | No outbound call to minors or about health conditions; no automated decision with legal or similarly significant effect is taken from a call | DEC-030; GDPR Arts 9, 22 (VR-24) | VO · ALL | DET | Age band; vertical; no decision tools | Block | — | "This call or decision is not allowed." |
| RP-EU-VOICE-014 | Scripts shall pass RP-EU-MKT and RP-EU-AI content rules and use formal address in de/fr | RP-EU-MKT; RP-EU-AI; DEC-873 | VO · ALL | DET+AI | AG-219 review | Block | Script approval | "The script does not meet EU content rules." |
| RP-EU-VOICE-015 | UK: automated (AI) marketing calls require the subscriber's prior consent to such calls from this caller; live (human) marketing calls shall not be made to numbers on TPS/CTPS (data ≤ 28 days) unless the subscriber has specifically consented to calls from this caller; caller ID shall be valid and dialable | PECR regs 19, 21, 24 (VR-38); Ofcom CLI guidance (verify) | VO · ALL | DET | `country = UK` → opt-in for AI; TPS/CTPS scrub for human; CLI check | Block | Consent; scrub record | "UK calls need consent for AI calls and a TPS check for live calls." |
| RP-EU-VOICE-016 | UK: the UK profile shall be activated only after UK counsel signs the UK rows and ADR-184 enables the UK market | ADR-184; CJ-UK-02 | VO · ALL | DET | `uk_rows.signed = true` AND market enabled | Block | Sign-off record | "UK voice is not enabled yet." |

**Pack parameters (loaded by AU-128 and read by the PDP, AU-264/272/278/280/281/282; every value "verify at time of implementation, as of 28 Nov 2026" unless its VR entry is verified).**

| Parameter | Draft value | Source / note |
|---|---|---|
| fr_window | Mon–Fri 10:00–13:00, 14:00–20:00; no Sat/Sun/holidays | VR-69 |
| fr_max_attempts_30d | 4 | VR-69 (verify) |
| fr_consent_validity_days | 365 | VR-69 |
| default_window_local | 09:00–21:00 | DEC-777 |
| uk_tps_max_age_days | 28 | VR-38 (verify) |
| consent_retention_years | 6 | Platform policy |

### 11.15.34.5 Required disclosures and approved template wording

| Template | Use | English (approved draft wording) | German / French (from Part 11.18a, drafts) | Placement |
|---|---|---|---|---|
| TPL-EU-VO-01 | AI disclosure (= TPL-VO-DISC-01) | "Hello, this is {brand}'s AI assistant. I'm an automated assistant using an AI-generated voice, calling about {purpose}. You can say 'agent' or press 0 at any time to speak with a person." | de: "Guten Tag, hier ist der KI-Assistent von {brand}. Ich bin ein automatisierter Assistent mit einer KI-generierten Stimme und rufe wegen {purpose} an. Sagen Sie jederzeit 'Mitarbeiter' oder drücken Sie die 0, um mit einer Person zu sprechen." · fr: "Bonjour, ici l'assistant IA de {brand}. Je suis un assistant automatisé doté d'une voix générée par IA et je vous appelle au sujet de {purpose}. Dites « conseiller » ou appuyez sur 0 à tout moment pour parler à une personne." | First utterance ≤ 2.0 s |
| TPL-EU-VO-02 | Short privacy notice | "{brand} uses your details to handle this call. You can object to marketing at any time by saying 'stop'. Full details: {notice_url_short} or press 8 to hear how to get them." | de/fr: pending legal translation [GAP-996] | After disclosure, before purpose discussion |
| TPL-EU-VO-03 | Objection confirmation | "Understood. {brand} will not contact you for marketing again." | de/fr pending | On objection |

### 11.15.34.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-EU-VO-01 | Objection phrases (en/de/fr) | stop; no more calls; remove me; ich widerspreche; keine Anrufe mehr; rufen Sie mich nicht mehr an; je m'oppose; ne m'appelez plus; supprimez mon numéro | phrase + ASR semantic | Block (triggers 008) | 008 |

**Prohibited (absolute, no mandate, exception or override can unlock):** AI marketing calls without prior opt-in; reliance on a national opt-out register for AI calls; consumer calls in France outside the window or with consent older than 12 months; emotion recognition; suppressed caller ID.

### 11.15.34.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Inbound AI answering | Rules 001–006 and 011 do not apply; 007, 008, 009, 012–014 apply |
| E-2 | France calls about an existing contract | Allowed without new consent if the call relates to that contract (VR-69); window and attempt limits still apply |
| E-3 | Member state without a completed profile row | Outbound Block; inbound allowed only if the row says so |

### 11.15.34.8 AI reviewer review guidance (RP-EU-VOICE)

- **Reviewer:** AG-219 (scripts) and AG-217 (audits), AG-086 contract.
- **Look for:** missing AI disclosure; unclear purpose; pressure; informal address; marketing in service calls.
- **Cite:** `RP-EU-VOICE-0NN` and the pack version only; quote the line or timestamp.
- **Escalate (`needs_counsel`):** member-state row missing or unclear; consumer vs business status unclear.
- **Never:** decide consent validity, windows or register results.

### 11.15.34.9 Test cases

| ID | Rule | Type | Input (summary) | Expected |
|---|---|---|---|---|
| TC-RP-EU-VOICE-01 | 001 | Negative | DE business contact, AI marketing call, no opt-in | Block 001 |
| TC-RP-EU-VOICE-02 | 003 | Negative | FR consumer, consent captured 13 months ago | Block 003 |
| TC-RP-EU-VOICE-03 | 003 | Positive | FR consumer, call about existing contract renewal, no new consent | Allowed (window applies) |
| TC-RP-EU-VOICE-04 | 004 | Negative | FR call Saturday 11:00 | Deferred to Monday 10:00 |
| TC-RP-EU-VOICE-05 | 004 | Negative | FR fifth attempt within 30 days | Block 004 |
| TC-RP-EU-VOICE-06 | 009 | Negative | Model registry enables emotion detector for EU tenant | Block at deploy |
| TC-RP-EU-VOICE-07 | 015 | Negative | UK live call to TPS-registered number, no specific consent | Block 015 |
| TC-RP-EU-VOICE-08 | 002 | Negative | Country with no profile row (e.g. PT) | Block 002 |

### 11.15.34.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-EU-VOICE
  title: "EU/EEA rules for AI voice calls (automated calling systems), national telemarketing regimes and registers, calling windows, GDPR transparency and objection, AI Act transparency; UK PECR profile for separate UK counsel sign-off"
  version: "0.1-draft"
  state: draft
  jurisdictions: "EU/EEA (member-state profile required, §11.15.34.12); UK profile (rows marked UK) — UK activation also needs UK counsel sign-off (ADR-184)"
  channels: "VO, CH, REC (via RP-GL-RECORDING)"
  audiences: "B2B, B2C (adults)"
  startups: "ALL; Tenant"
  gates_mandate_types: "MT-OUT (voice)"
  effective_dates: "AI Act Art. 50 from 2 Aug 2026; France opt-in from 11 Aug 2026 and Bloctel discontinued (VR-69); Netherlands existing-customer exception abolished 1 Jul 2026 (VR-70, verify)"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  level_cap: "L3 under Active MT-OUT only with documented prior opt-in for AI calls; no outbound AI call to consumers in FR outside the FR window"
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
parameters:
  fr_window: "Mon–Fri 10:00–13:00, 14:00–20:00; no Sat/Sun/holidays"
  fr_max_attempts_30d: "4"
  fr_consent_validity_days: "365"
  default_window_local: "09:00–21:00"
  uk_tps_max_age_days: "28"
  consent_retention_years: "6"
rules:
  - id: RP-EU-VOICE-001
    obligation: "Direct-marketing calls made by AI voice to subscribers in the EU/EEA shall be made only with the called subscriber's prior consent that meets GDPR Art. 4(11) and Art. 7, recorded per purpose; the platform applies this standard also to legal-person subscribers (DEC-769)"
    citation: "ePrivacy Art. 13(1) (VR-25); GDPR Arts 6(1)(a), 7 (VR-24); DEC-769"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "consent(contact, voice, call_ai_marketing).standard = opt_in AND evidence present"
    severity: "Block"
    override: none
    evidence: "Consent record"
    remediation_message: "\"AI marketing calls in the EU need the person's prior opt-in.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-002
    obligation: "Human-dialled marketing calls (including AI-assisted calls where only a human speaks) shall follow the member-state profile (opt-in, register scrub, existing-customer exception) and shall never use an AI voice"
    citation: "ePrivacy Art. 13(3) and national law (VR-25, VR-69…72)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Profile row for contact.member_state; register scrub age ≤ profile limit"
    severity: "Block"
    override: none
    evidence: "Profile row; scrub record"
    remediation_message: "\"This call does not meet this country's telemarketing rules.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-003
    obligation: "France: consumer telephone canvassing shall be made only with the consumer's prior consent obtained and kept per the décret of 23 Jul 2026, valid for no more than 1 year, except for calls relating to an existing contract as the law allows; contracts concluded after an unlawful call are void, so such orders shall be blocked"
    citation: "Code de la consommation L.223-1 ff. as amended (law of 30 Jun 2025) and décret 2026-662 (VR-69) [GAP-1172]"
    applies_to: "VO · B2C"
    check: "deterministic"
    detection: "member_state = FR AND consumer → consent age ≤ 365 d OR existing_contract_topic = true"
    severity: "Block"
    override: none
    evidence: "Consent record (FR)"
    remediation_message: "\"Calls to consumers in France need consent from the last 12 months.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-004
    obligation: "France: calls to consumers shall be placed only Monday–Friday 10:00–13:00 and 14:00–20:00 local time, never on Saturdays, Sundays or public holidays, and no more than 4 call attempts per consumer per 30 days across the startup's campaigns"
    citation: "Décret 2022-1313 (VR-69, verify continued application)"
    applies_to: "VO · B2C"
    check: "deterministic"
    detection: "FR window resolver; attempt counter 30 d"
    severity: "Block (defer)"
    override: none
    evidence: "Schedule log"
    remediation_message: "\"Outside the French calling hours or attempt limit. Rescheduled.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-005
    obligation: "All other EEA calls shall be placed within 09:00–21:00 recipient local time (DEC-777) intersected with any national window in the profile"
    citation: "DEC-777; national law (verify)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Window resolver"
    severity: "Block (defer)"
    override: none
    evidence: "Schedule log"
    remediation_message: "\"Outside calling hours. Rescheduled.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-006
    obligation: "Calls shall present a valid caller ID assigned to the startup that can be called back; caller-ID suppression is prohibited for marketing calls; French calls use numbers from ARCEP-designated ranges for automated or canvassing calls where required"
    citation: "National law, e.g. Germany TKG and UWG (verify); ARCEP numbering decisions (verify) (VR-72, VR-69)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Number registry and CLI test"
    severity: "Block"
    override: none
    evidence: "Number record"
    remediation_message: "\"Use a valid, displayed caller ID from the permitted range.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-007
    obligation: "The first utterance shall inform the person that they are interacting with an AI system (TPL-EU-VO-01), unless obvious, and AI-generated audio stored or played as content shall be marked as AI-generated in machine-readable form"
    citation: "AI Act Art. 50(1), 50(2) (VR-22); Part 11.18a D-1, D-7"
    applies_to: "VO, CH · ALL"
    check: "deterministic"
    detection: "AU-283 disclosure; storage provenance hook"
    severity: "Block"
    override: none
    evidence: "Disclosure event"
    remediation_message: "\"The AI disclosure must come first.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-008
    obligation: "The call shall give a short privacy notice (controller identity, purpose, right to object) and a link or callback route to the full notice, and an objection to direct marketing shall be honoured immediately for all channels"
    citation: "GDPR Arts 13/14, 21(2)–(3) (VR-24)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "TPL-EU-VO-02 in script; objection → suppression ≤ 1 s"
    severity: "Block"
    override: none
    evidence: "Notice event; suppression"
    remediation_message: "\"Add the short privacy notice and honour objections immediately.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-009
    obligation: "No emotion recognition or individual sentiment scoring of callers or employees shall be performed; only aggregated, anonymous call-quality metrics"
    citation: "AI Act Art. 5(1)(f) (workplace) and Annex III (VR-23); Part 11.18a §11.18.5.12"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Model registry: emotion models disabled for EU tenants; summary schema has no sentiment field"
    severity: "Block"
    override: none
    evidence: "Registry config"
    remediation_message: "\"Emotion recognition is not allowed.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-010
    obligation: "Consent evidence shall be kept per member-state rules (for example Germany: documented and kept 5 years; France: as the décret requires) and at least 6 years on the platform"
    citation: "UWG §7a (VR-72); décret 2026-662 (VR-69); GDPR Art. 7(1)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Retention class voice_consent_6y"
    severity: "Block"
    override: none
    evidence: "Consent evidence"
    remediation_message: "\"Consent evidence must be retained.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-011
    obligation: "A voicemail with an AI voice shall be left only with documented prior opt-in for that purpose"
    citation: "ePrivacy Art. 13(1) (VR-25); Part 11.18a VM-2"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "AMD MACHINE → opt-in check"
    severity: "Block"
    override: none
    evidence: "Voicemail event"
    remediation_message: "\"A voicemail cannot be left without opt-in.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-012
    obligation: "Personal data of EU calls (audio, transcripts, summaries, consent) shall be processed in the EU region; any non-EEA provider in the voice stack requires a Chapter V mechanism and a DPIA covering it"
    citation: "GDPR Arts 35, 44–49 (VR-24); DEC-772"
    applies_to: "VO, REC · ALL"
    check: "deterministic"
    detection: "Provider registry region and transfer mechanism; DPIA ID"
    severity: "Block"
    override: none
    evidence: "Registry; DPIA"
    remediation_message: "\"This provider is not approved for EU call data.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-013
    obligation: "No outbound call to minors or about health conditions; no automated decision with legal or similarly significant effect is taken from a call"
    citation: "DEC-030; GDPR Arts 9, 22 (VR-24)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Age band; vertical; no decision tools"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"This call or decision is not allowed.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-014
    obligation: "Scripts shall pass RP-EU-MKT and RP-EU-AI content rules and use formal address in de/fr"
    citation: "RP-EU-MKT; RP-EU-AI; DEC-873"
    applies_to: "VO · ALL"
    check: "deterministic_then_ai_review"
    detection: "AG-219 review"
    severity: "Block"
    override: r10_with_reason
    evidence: "Script approval"
    remediation_message: "\"The script does not meet EU content rules.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-015
    obligation: "UK: automated (AI) marketing calls require the subscriber's prior consent to such calls from this caller; live (human) marketing calls shall not be made to numbers on TPS/CTPS (data ≤ 28 days) unless the subscriber has specifically consented to calls from this caller; caller ID shall be valid and dialable"
    citation: "PECR regs 19, 21, 24 (VR-38); Ofcom CLI guidance (verify)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "country = UK → opt-in for AI; TPS/CTPS scrub for human; CLI check"
    severity: "Block"
    override: none
    evidence: "Consent; scrub record"
    remediation_message: "\"UK calls need consent for AI calls and a TPS check for live calls.\""
    effective_from: null  # set at sign-off
  - id: RP-EU-VOICE-016
    obligation: "UK: the UK profile shall be activated only after UK counsel signs the UK rows and ADR-184 enables the UK market"
    citation: "ADR-184; CJ-UK-02"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "uk_rows.signed = true AND market enabled"
    severity: "Block"
    override: none
    evidence: "Sign-off record"
    remediation_message: "\"UK voice is not enabled yet.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-EU-VO-01
    name: "Objection phrases (en/de/fr)"
    match: "phrase + ASR semantic"
    severity: "Block (triggers 008)"
    used_by: "008"
    terms:
      - "stop"
      - "no more calls"
      - "remove me"
      - "ich widerspreche"
      - "keine Anrufe mehr"
      - "rufen Sie mich nicht mehr an"
      - "je m'oppose"
      - "ne m'appelez plus"
      - "supprimez mon numéro"
templates:
  - id: TPL-EU-VO-01
    use: "AI disclosure (= TPL-VO-DISC-01)"
    en: "\"Hello, this is {brand}'s AI assistant. I'm an automated assistant using an AI-generated voice, calling about {purpose}. You can say 'agent' or press 0 at any time to speak with a person.\""
    placement: "First utterance ≤ 2.0 s"
  - id: TPL-EU-VO-02
    use: "Short privacy notice"
    en: "\"{brand} uses your details to handle this call. You can object to marketing at any time by saying 'stop'. Full details: {notice_url_short} or press 8 to hear how to get them.\""
    placement: "After disclosure, before purpose discussion"
  - id: TPL-EU-VO-03
    use: "Objection confirmation"
    en: "\"Understood. {brand} will not contact you for marketing again.\""
    placement: "On objection"
```

### 11.15.34.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-EU-VOICE v0.1-draft → proposed v1.0 |
| Reviewer (name, enrolment/bar no., jurisdiction of admission) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Rules amended (IDs and summary) | _______________________ |
| Pack parameters confirmed (values and sources) | ☐ All ☐ Amended: __________ |
| Citations confirmed against primary text (VR entries) | ☐ VR-22 ☐ VR-23 ☐ VR-24 ☐ VR-25 ☐ VR-38 ☐ VR-69 ☐ VR-70 ☐ VR-71 ☐ VR-72 |
| German and French wording reviewed by | _______________________ |
| Conditions or limitations of the sign-off | _______________________ |
| Next review due | ____ / ____ / ______ (≤ 120 days) |
| R10 approval (name, date) | _______________________ |
| Signature (counsel) / Signature (R10) | _______________ / _______________ |

### 11.15.34.12 Member-state and UK profiles (counsel to confirm each row before activation; values verify, as of 28 Nov 2026)

| State | Human-dialled marketing (consumers) | Register | AI (automated) marketing calls | Window (effective) | Attempt limits | Recording model | Sources |
|---|---|---|---|---|---|---|---|
| FR | **Opt-in** from 11 Aug 2026; consent ≤ 1 year; existing-contract exception | Bloctel **discontinued** 11 Aug 2026 | Opt-in | Mon–Fri 10:00–13:00, 14:00–20:00 | ≤ 4 / 30 days | Affirmative consent (platform) | VR-69 |
| DE | Opt-in (prior express consent) for consumers; presumed consent for businesses (human calls only) | None | Opt-in | 09:00–21:00 | Platform | All-party (StGB §201) | VR-72 |
| NL | Opt-in; existing-customer exception abolished 1 Jul 2026 (verify) | Bel-me-niet register superseded (verify) | Opt-in | 09:00–21:00 | Platform | Consent (platform) | VR-70 |
| IT | Opt-out via RPO (fixed and mobile, verify) for human calls | RPO | Opt-in | 09:00–21:00 (Garante code of conduct may narrow, verify) | Platform | Consent (platform) | VR-71 |
| ES | Consent or legitimate interest per LGTel art. 66 (verify); Lista Robinson | Lista Robinson (verify) | Opt-in | 09:00–21:00 (consumer-law limits, verify) | Platform | Consent (platform) | VR-71 [GAP-1178] |
| IE | Opt-out via National Directory Database (verify) | NDD | Opt-in | 09:00–21:00 | Platform | Consent (platform) | verify |
| Other EEA | Counsel | Counsel | Opt-in | 09:00–21:00 | Platform | All-party (default) | Block until row complete |
| UK | Live calls: TPS/CTPS screening unless specific consent | TPS/CTPS | Opt-in (PECR reg. 19) | 09:00–21:00 | Platform | Notice-and-object allowed if pack approves (IPA business regs) | VR-38 |


---

## 11.15.35 RP-AE-VOICE: UAE AI voice calls: telemarketing regulations (Cabinet Resolutions 56 and 57 of 2024), DNCR, hours, mandatory recording, PDPL

### 11.15.35.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-AE-VOICE |
| Title | UAE rules for AI inbound and outbound calls: licensed company and registered local numbers, Do Not Call Register, 09:00–18:00 window, mandatory recording of marketing calls with notice, refusal handling, consent under the PDPL, recording offences |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | AE (+971 numbers or UAE residents) |
| Channels | VO, CH, REC |
| Audiences | B2B, B2C (adults) |
| Startups | ALL; Tenant (requires a UAE-licensed entity for outbound marketing) |
| Mandate types gated | MT-OUT (voice) — outbound marketing remains L1 in v0.1 |
| Legal sources | Cabinet Resolution No. 56 of 2024 on telemarketing (effective 27 Aug 2024) and No. 57 of 2024 on penalties (VR-76); TDRA DNCR (verify); Federal Decree-Law 45/2021 (PDPL) (verify; executive regulations status verify); Federal Decree-Law 34/2021 on combating rumours and cybercrimes Art. 44 and Federal Decree-Law 31/2021 (Crimes and Penalties) Art. 431 (recording and privacy) (VR-77); Federal Law 15/2020 consumer protection (verify); CJ-AE-01; Part 11.18a §11.18.5.3 (GAP-1067) |
| Effective dates | Resolutions 56/57 from 27 Aug 2024 (VR-76) |
| Owner | R10 with UAE counsel |
| Review cadence | Quarterly |
| Expiry / fail-closed | 120 days; AE voice inactive while not `active`; last in activation order (RECOMMENDATION-1074) |
| Depends on | RP-GL-RECORDING (AE profile), RP-COMMIT |

### 11.15.35.2 Plain-language summary

1. Only a company licensed in the UAE (including free-zone companies) may telemarket, using local numbers registered under its licence. Never use personal numbers.
2. Do not make marketing calls to numbers on the Do Not Call Register (DNCR). The platform blocks them all.
3. Marketing calls run only 09:00–18:00 UAE time.
4. Marketing calls must be recorded, and the person told at the start. Because recording without consent is an offence, the platform asks for consent. If the person refuses, the marketing call ends politely and is not continued unrecorded.
5. If the person declines the offer, do not call again about the same product. Disclose the AI and the company. No aggressive or misleading selling.
6. Inbound AI answering is allowed with disclosure and a PDPL notice. Recording inbound calls needs consent.

### 11.15.35.3 Definitions

| Term | Definition for this pack |
|---|---|
| Telemarketing | Marketing of products or services by telephone by companies licensed in the State (Res. 56/2024, VR-76) |
| DNCR | Do Not Call Register operated by TDRA (verify) |
| Licensed company | Company with a UAE trade licence (mainland or free zone) |

### 11.15.35.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-AE-VOICE-001 | Outbound marketing calls to UAE numbers shall be made only on behalf of a UAE-licensed company of the tenant, from UAE local numbers registered under that company's trade licence; personal numbers shall never be used | Res. 56/2024 (VR-76) | VO · ALL | DET | `company.uae_licence` present; `number.registered_to_licence = true` | Block | Licence and number records | "Outbound marketing in the UAE needs a UAE-licensed company and a registered local number." |
| RP-AE-VOICE-002 | No marketing call shall be made to a number on the DNCR; scrub data unavailable → HOLD (platform blocks DNCR numbers even with prior consent until counsel confirms an exception) | Res. 56/2024; Res. 57/2024 (VR-76) | VO · ALL | DET | DNCR scrub per regulation freshness (verify); hit → Block | Block | Scrub record | "This number is on the UAE Do Not Call Register." |
| RP-AE-VOICE-003 | Marketing calls shall be made only between 09:00 and 18:00 UAE time | Res. 57/2024 penalty table (VR-76) | VO · ALL | DET | Window 09:00–18:00 Asia/Dubai | Block (defer) | Schedule log | "UAE marketing calls are allowed only from 09:00 to 18:00." |
| RP-AE-VOICE-004 | Marketing calls shall be recorded and the consumer informed at the start of the call; because recording without consent is an offence, the platform shall obtain affirmative consent (TPL-AE-VO-02) and, if consent is refused, end the marketing call politely without continuing it unrecorded | Res. 56/2024 (recording obligation) (VR-76); Decree-Law 34/2021 Art. 44, Decree-Law 31/2021 Art. 431 (VR-77) [GAP-1177] | VO, REC · ALL | DET | AU-282 AE profile: mode = MANDATORY_WITH_CONSENT; refusal → end call with TPL-AE-VO-03 | Block | Recording consent event | "Marketing calls in the UAE must be recorded with consent. The call has ended." |
| RP-AE-VOICE-005 | Where a consumer declines the offer, no further marketing call about the same product or service shall be made to that consumer (platform: for 30 days, and never on the same day), and the platform cap of 1 attempt per day and 2 per week applies | Res. 56/2024 (repeat calls, verify) (VR-76); platform policy | VO · ALL | DET | Decline disposition → product-scoped suppression | Block | Disposition record | "This person declined. No further calls about this product." |
| RP-AE-VOICE-006 | The call shall begin with the AI disclosure, the company name and purpose (TPL-AE-VO-01) in Arabic or English per the contact's preference | Res. 56/2024 (identification, verify); BR-V7-AI-01; DEC-862 | VO, CH · ALL | DET | AU-283 disclosure | Block | Disclosure event | "Start the call with the AI disclosure and company name." |
| RP-AE-VOICE-007 | Calls shall not use aggressive, misleading or harassing methods and shall not promote products without the required approvals | Res. 56/2024 (verify); Federal Law 15/2020 (verify); RP-COMMIT | VO · ALL | DET+AI | AG-219 script review; AG-217 audits | Block | Script approval | "The script contains pressure or misleading wording." |
| RP-AE-VOICE-008 | Personal data shall be processed under a PDPL lawful basis (consent for marketing), with a short notice in the call and a link to the full notice | PDPL (Decree-Law 45/2021) (verify) | VO · ALL | DET | Consent ledger; TPL-AE-VO-04 | Block | Consent record | "No lawful basis for this call under the UAE data-protection law." |
| RP-AE-VOICE-009 | Outbound marketing campaigns in the UAE shall run at L1 (each campaign batch approved by a person) in v0.1 | Platform policy; RECOMMENDATION-1074 | VO · ALL | DET | Mandate eligibility: AE MT-OUT voice disabled | Block | Approval record | "UAE outbound campaigns need human approval for each batch." |
| RP-AE-VOICE-010 | Opt-outs shall suppress the contact immediately and be added to the company's internal do-not-call list | Res. 56/2024 (verify); AU-288 | VO · ALL | DET | Opt-out detector → suppression | Block | Suppression record | "The contact opted out." |
| RP-AE-VOICE-011 | No AI voicemail shall be left in the UAE in v0.1 | Platform policy (no clear basis) | VO · ALL | DET | AMD MACHINE → hang up | Block | — | "Voicemail is disabled for the UAE." |
| RP-AE-VOICE-012 | Inbound AI answering is allowed with disclosure; recording inbound calls requires affirmative consent of the caller | VR-77; RP-GL-RECORDING AE profile | VO, REC · ALL | DET | Inbound AE → TPL-AE-VO-02 before recording | Block | Consent event | "Ask for consent before recording this call." |

**Pack parameters (loaded by AU-128 and read by the PDP, AU-264/272/278/280/281/282; every value "verify at time of implementation, as of 28 Nov 2026" unless its VR entry is verified).**

| Parameter | Draft value | Source / note |
|---|---|---|
| window_local | 09:00–18:00 Asia/Dubai | VR-76 |
| dncr_scrub_max_age | per TDRA rules (verify); platform 24 h | verify |
| decline_suppression_days | 30 (platform) | verify law |
| attempts | ≤ 1 / day, ≤ 2 / week (platform) | verify law |
| outbound_level_v01 | L1 | Platform policy |

### 11.15.35.5 Required disclosures and approved template wording

| Template | Use | English (approved draft wording) | Arabic (from Part 11.18a, draft) | Placement |
|---|---|---|---|---|
| TPL-AE-VO-01 | AI disclosure (= TPL-VO-DISC-01) | "Hello, this is {brand}'s AI assistant. I'm an automated assistant using an AI-generated voice, calling about {purpose}. You can say 'agent' or press 0 at any time to speak with a person." | "مرحبًا، معك المساعد الذكي لشركة {brand}. أنا مساعد آلي بصوت مولَّد بالذكاء الاصطناعي، وأتصل بخصوص {purpose}. يمكنك قول «موظف» أو الضغط على 0 في أي وقت للتحدث مع شخص." | First utterance |
| TPL-AE-VO-02 | Recording consent (marketing) | "This call must be recorded under UAE telemarketing rules. Do you agree to the recording? Press 1 or say 'yes' to continue; press 2 or say 'no' and we will end the call." | ar: pending native-speaker and counsel review [ASSUMPTION-1066] | Before any marketing content |
| TPL-AE-VO-03 | Refusal close | "Thank you. We won't continue this call. You can contact {brand} at {callback_number} whenever you wish." | ar: pending | On refusal |
| TPL-AE-VO-04 | Short privacy notice | "{brand} processes your details for this call under UAE data-protection law. Details: {notice_url_short}." | ar: pending | After consent |

### 11.15.35.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-AE-VO-01 | Decline and opt-out (en/ar) | not interested; stop calling; don't call; غير مهتم; لا تتصل; توقف عن الاتصال | phrase + ASR semantic | Block (triggers 005/010) | 005, 010 |

**Prohibited (absolute, no mandate, exception or override can unlock):** calls to DNCR numbers; calls outside 09:00–18:00; continuing a marketing call unrecorded after refusal; personal numbers; AI voicemail.

### 11.15.35.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Service call about an existing transaction (not marketing) | Rules 002, 003, 005 do not apply (verify); recording per RP-GL-RECORDING AE profile (consent) |
| E-2 | Tenant without a UAE-licensed entity | Outbound Block; inbound answering for a UAE number still requires counsel review |

### 11.15.35.8 AI reviewer review guidance (RP-AE-VOICE)

- **Reviewer:** AG-219 and AG-217, AG-086 contract.
- **Look for:** pressure tactics; unapproved product claims; missing identification.
- **Cite:** `RP-AE-VOICE-0NN` and the pack version only; quote line or timestamp.
- **Escalate (`needs_counsel`):** regulated products (financial, health); any Arabic script not reviewed.
- **Never:** decide DNCR, window or licence status.

### 11.15.35.9 Test cases

| ID | Rule | Type | Input (summary) | Expected |
|---|---|---|---|---|
| TC-RP-AE-VOICE-01 | 002 | Negative | Number on DNCR with web consent | Block 002 |
| TC-RP-AE-VOICE-02 | 003 | Negative | Call scheduled 18:05 Dubai | Deferred to next day 09:00 |
| TC-RP-AE-VOICE-03 | 004 | Negative | Consumer refuses recording | Call ended with TPL-AE-VO-03; no marketing content |
| TC-RP-AE-VOICE-04 | 005 | Negative | Second call same day after decline | Block 005 |
| TC-RP-AE-VOICE-05 | 011 | Negative | Voicemail detected | Hang up; no message |

### 11.15.35.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-AE-VOICE
  title: "UAE rules for AI inbound and outbound calls: licensed company and registered local numbers, Do Not Call Register, 09:00–18:00 window, mandatory recording of marketing calls with notice, refusal handling, consent under the PDPL, recording offences"
  version: "0.1-draft"
  state: draft
  jurisdictions: "AE (+971 numbers or UAE residents)"
  channels: "VO, CH, REC"
  audiences: "B2B, B2C (adults)"
  startups: "ALL; Tenant (requires a UAE-licensed entity for outbound marketing)"
  gates_mandate_types: "MT-OUT (voice) — outbound marketing remains L1 in v0.1"
  effective_dates: "Resolutions 56/57 from 27 Aug 2024 (VR-76)"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  level_cap: "L1 for outbound marketing calls in v0.1 (human-initiated campaign approval per call batch); inbound AI answering L3"
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
parameters:
  window_local: "09:00–18:00 Asia/Dubai"
  dncr_scrub_max_age: "per TDRA rules (verify); platform 24 h"
  decline_suppression_days: "30 (platform)"
  attempts: "≤ 1 / day, ≤ 2 / week (platform)"
  outbound_level_v01: "L1"
rules:
  - id: RP-AE-VOICE-001
    obligation: "Outbound marketing calls to UAE numbers shall be made only on behalf of a UAE-licensed company of the tenant, from UAE local numbers registered under that company's trade licence; personal numbers shall never be used"
    citation: "Res. 56/2024 (VR-76)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "company.uae_licence present; number.registered_to_licence = true"
    severity: "Block"
    override: none
    evidence: "Licence and number records"
    remediation_message: "\"Outbound marketing in the UAE needs a UAE-licensed company and a registered local number.\""
    effective_from: null  # set at sign-off
  - id: RP-AE-VOICE-002
    obligation: "No marketing call shall be made to a number on the DNCR; scrub data unavailable → HOLD (platform blocks DNCR numbers even with prior consent until counsel confirms an exception)"
    citation: "Res. 56/2024; Res. 57/2024 (VR-76)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "DNCR scrub per regulation freshness (verify); hit → Block"
    severity: "Block"
    override: none
    evidence: "Scrub record"
    remediation_message: "\"This number is on the UAE Do Not Call Register.\""
    effective_from: null  # set at sign-off
  - id: RP-AE-VOICE-003
    obligation: "Marketing calls shall be made only between 09:00 and 18:00 UAE time"
    citation: "Res. 57/2024 penalty table (VR-76)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Window 09:00–18:00 Asia/Dubai"
    severity: "Block (defer)"
    override: none
    evidence: "Schedule log"
    remediation_message: "\"UAE marketing calls are allowed only from 09:00 to 18:00.\""
    effective_from: null  # set at sign-off
  - id: RP-AE-VOICE-004
    obligation: "Marketing calls shall be recorded and the consumer informed at the start of the call; because recording without consent is an offence, the platform shall obtain affirmative consent (TPL-AE-VO-02) and, if consent is refused, end the marketing call politely without continuing it unrecorded"
    citation: "Res. 56/2024 (recording obligation) (VR-76); Decree-Law 34/2021 Art. 44, Decree-Law 31/2021 Art. 431 (VR-77) [GAP-1177]"
    applies_to: "VO, REC · ALL"
    check: "deterministic"
    detection: "AU-282 AE profile: mode = MANDATORY_WITH_CONSENT; refusal → end call with TPL-AE-VO-03"
    severity: "Block"
    override: none
    evidence: "Recording consent event"
    remediation_message: "\"Marketing calls in the UAE must be recorded with consent. The call has ended.\""
    effective_from: null  # set at sign-off
  - id: RP-AE-VOICE-005
    obligation: "Where a consumer declines the offer, no further marketing call about the same product or service shall be made to that consumer (platform: for 30 days, and never on the same day), and the platform cap of 1 attempt per day and 2 per week applies"
    citation: "Res. 56/2024 (repeat calls, verify) (VR-76); platform policy"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Decline disposition → product-scoped suppression"
    severity: "Block"
    override: none
    evidence: "Disposition record"
    remediation_message: "\"This person declined. No further calls about this product.\""
    effective_from: null  # set at sign-off
  - id: RP-AE-VOICE-006
    obligation: "The call shall begin with the AI disclosure, the company name and purpose (TPL-AE-VO-01) in Arabic or English per the contact's preference"
    citation: "Res. 56/2024 (identification, verify); BR-V7-AI-01; DEC-862"
    applies_to: "VO, CH · ALL"
    check: "deterministic"
    detection: "AU-283 disclosure"
    severity: "Block"
    override: none
    evidence: "Disclosure event"
    remediation_message: "\"Start the call with the AI disclosure and company name.\""
    effective_from: null  # set at sign-off
  - id: RP-AE-VOICE-007
    obligation: "Calls shall not use aggressive, misleading or harassing methods and shall not promote products without the required approvals"
    citation: "Res. 56/2024 (verify); Federal Law 15/2020 (verify); RP-COMMIT"
    applies_to: "VO · ALL"
    check: "deterministic_then_ai_review"
    detection: "AG-219 script review; AG-217 audits"
    severity: "Block"
    override: r10_with_reason
    evidence: "Script approval"
    remediation_message: "\"The script contains pressure or misleading wording.\""
    effective_from: null  # set at sign-off
  - id: RP-AE-VOICE-008
    obligation: "Personal data shall be processed under a PDPL lawful basis (consent for marketing), with a short notice in the call and a link to the full notice"
    citation: "PDPL (Decree-Law 45/2021) (verify)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Consent ledger; TPL-AE-VO-04"
    severity: "Block"
    override: none
    evidence: "Consent record"
    remediation_message: "\"No lawful basis for this call under the UAE data-protection law.\""
    effective_from: null  # set at sign-off
  - id: RP-AE-VOICE-009
    obligation: "Outbound marketing campaigns in the UAE shall run at L1 (each campaign batch approved by a person) in v0.1"
    citation: "Platform policy; RECOMMENDATION-1074"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Mandate eligibility: AE MT-OUT voice disabled"
    severity: "Block"
    override: none
    evidence: "Approval record"
    remediation_message: "\"UAE outbound campaigns need human approval for each batch.\""
    effective_from: null  # set at sign-off
  - id: RP-AE-VOICE-010
    obligation: "Opt-outs shall suppress the contact immediately and be added to the company's internal do-not-call list"
    citation: "Res. 56/2024 (verify); AU-288"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "Opt-out detector → suppression"
    severity: "Block"
    override: none
    evidence: "Suppression record"
    remediation_message: "\"The contact opted out.\""
    effective_from: null  # set at sign-off
  - id: RP-AE-VOICE-011
    obligation: "No AI voicemail shall be left in the UAE in v0.1"
    citation: "Platform policy (no clear basis)"
    applies_to: "VO · ALL"
    check: "deterministic"
    detection: "AMD MACHINE → hang up"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"Voicemail is disabled for the UAE.\""
    effective_from: null  # set at sign-off
  - id: RP-AE-VOICE-012
    obligation: "Inbound AI answering is allowed with disclosure; recording inbound calls requires affirmative consent of the caller"
    citation: "VR-77; RP-GL-RECORDING AE profile"
    applies_to: "VO, REC · ALL"
    check: "deterministic"
    detection: "Inbound AE → TPL-AE-VO-02 before recording"
    severity: "Block"
    override: none
    evidence: "Consent event"
    remediation_message: "\"Ask for consent before recording this call.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-AE-VO-01
    name: "Decline and opt-out (en/ar)"
    match: "phrase + ASR semantic"
    severity: "Block (triggers 005/010)"
    used_by: "005, 010"
    terms:
      - "not interested"
      - "stop calling"
      - "don't call"
      - "غير مهتم"
      - "لا تتصل"
      - "توقف عن الاتصال"
templates:
  - id: TPL-AE-VO-01
    use: "AI disclosure (= TPL-VO-DISC-01)"
    en: "\"Hello, this is {brand}'s AI assistant. I'm an automated assistant using an AI-generated voice, calling about {purpose}. You can say 'agent' or press 0 at any time to speak with a person.\""
    placement: "First utterance"
  - id: TPL-AE-VO-02
    use: "Recording consent (marketing)"
    en: "\"This call must be recorded under UAE telemarketing rules. Do you agree to the recording? Press 1 or say 'yes' to continue; press 2 or say 'no' and we will end the call.\""
    placement: "Before any marketing content"
  - id: TPL-AE-VO-03
    use: "Refusal close"
    en: "\"Thank you. We won't continue this call. You can contact {brand} at {callback_number} whenever you wish.\""
    placement: "On refusal"
  - id: TPL-AE-VO-04
    use: "Short privacy notice"
    en: "\"{brand} processes your details for this call under UAE data-protection law. Details: {notice_url_short}.\""
    placement: "After consent"
```

### 11.15.35.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-AE-VOICE v0.1-draft → proposed v1.0 |
| Reviewer (name, enrolment/bar no., jurisdiction of admission) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Rules amended (IDs and summary) | _______________________ |
| Pack parameters confirmed (values and sources) | ☐ All ☐ Amended: __________ |
| Citations confirmed against primary text (VR entries) | ☐ VR-76 ☐ VR-77 |
| Arabic wording reviewed by | _______________________ |
| Conditions or limitations of the sign-off | _______________________ |
| Next review due | ____ / ____ / ______ (≤ 120 days) |
| R10 approval (name, date) | _______________________ |
| Signature (counsel) / Signature (R10) | _______________ / _______________ |

---

## 11.15.36 RP-GL-RECORDING: Call recording and transcription: one-party vs all-party consent matrix, notice wording, retention and access

### 11.15.36.1 Pack metadata

| Field | Value |
|---|---|
| Pack ID | RP-GL-RECORDING |
| Title | Recording, persisted transcription and coaching use of calls: mode resolution, consent and notice, joining parties, payment pauses, redaction, residency, retention, access, DSAR, evidence |
| Version / state | v0.1-draft · `draft` |
| Jurisdiction(s) | ALL (jurisdiction rows in §11.15.36.12; a row must be signed before recording is enabled in that jurisdiction) |
| Channels | REC (audio recording, persisted transcript, coaching excerpt), VO, CH |
| Audiences | ALL parties to the call (customers, prospects, employees, third parties) |
| Startups | ALL; Tenant |
| Mandate types gated | MT-OUT (voice) recording mode; SM-SVC-26-WF04; SM-SVC-36-WF03 |
| Legal sources | See §11.15.36.12 per jurisdiction (VR-02, VR-24, VR-38, VR-69, VR-72, VR-73, VR-74, VR-76, VR-77); PCI DSS (recording of card data, verify); GDPR Arts 5, 6, 13, 15, 17, 35, 88 and BDSG §26 / BetrVG §87(1) no. 6 for employees (verify); Part 11.18a §11.18.5.3.3, §11.18.5.13, §11.18.5.14; DEC-863, DEC-865, DEC-866, DEC-870 |
| Effective dates | On sign-off per jurisdiction row |
| Owner | R10 with counsel per jurisdiction |
| Review cadence | Quarterly |
| Expiry / fail-closed | 120 days; on expiry recording mode = OFF everywhere (calls continue unrecorded; UAE marketing calls stop because recording is mandatory) |
| Depends on | RP-IN-VOICE, RP-US-VOICE, RP-EU-VOICE, RP-AE-VOICE, RP-IN-DPDP, RP-EU-MKT |

### 11.15.36.2 Plain-language summary

1. Recording mode is set by the strictest rule among all parties' locations. An unknown location counts as all-party.
2. The platform default is affirmative consent of every party. Notice-and-object is used only where this pack's row allows it (India, the UK and US one-party states). The UAE requires marketing calls to be recorded with consent.
3. Recording starts only when consent or notice is given, never before. When someone joins, recording pauses and their consent is sought where the rule requires it.
4. Payment talk pauses recording. Card data never enters recordings. Recordings are redacted before storage, and are not stored if redaction fails.
5. Recordings stay in the tenant's region, encrypted with per-tenant keys. Retention defaults to 90 days, with a maximum per jurisdiction. Access is role-based, purpose-prompted and logged.
6. Persisted transcripts exist only for recorded calls. Coaching use needs the coaching purpose in the notice or consent, and a works agreement in Germany.

### 11.15.36.3 Definitions

| Term | Definition for this pack |
|---|---|
| CONSENT_ALL | Affirmative consent (verbal yes or DTMF 1) of every party before recording |
| NOTICE_OBJECT | Recording after a clear notice, stopped and partial audio deleted on objection |
| MANDATORY_WITH_CONSENT | Recording required by law for the call type (UAE marketing) and obtained with consent; refusal ends the call type |
| Persisted transcript | Diarized transcript retained after the call (Part 11.18a §11.18.5.12) |
| Coaching excerpt | Redacted segment shared by the learner for coaching (SM-SVC-36-WF03) |

### 11.15.36.4 Rules

| Rule ID | Obligation (draft legal wording) | Citation | Applies to | Check | Detection logic / pattern | Severity | Required evidence | Remediation message shown to user |
|---|---|---|---|---|---|---|---|---|
| RP-GL-RECORDING-001 | Before recording, the mode shall be resolved as the strictest of the rows applicable to every party's location (unknown location = CONSENT_ALL) and recorded with the signals used | DEC-863; CP-03; §11.15.36.12 | REC · ALL | DET | AU-282 resolver over parties; evidence_ref of signals | Block | Mode decision record | "The recording mode could not be resolved. The call will not be recorded." |
| RP-GL-RECORDING-002 | In CONSENT_ALL mode, recording shall start only after every party has given affirmative consent with TPL-GL-REC-02; silence for 6 s or refusal means no recording, and refusal shall be stored | Part 11.18a §11.18.5.13; VR-72, VR-73, VR-77 | REC · ALL | DET | Consent events per party; timeout 6 s | Block | Consent events | "Not every party agreed. The call is not recorded." |
| RP-GL-RECORDING-003 | NOTICE_OBJECT mode shall be used only where the jurisdiction row permits it and only for the purposes named in TPL-GL-REC-01; an objection at any time stops recording and deletes partial audio | VR-02, VR-38, VR-74; ASSUMPTION-1063 | REC · ALL | DET | Row permits notice; objection detector → stop + delete | Block | Notice and objection events | "Notice-only recording is not allowed here, or the person objected." |
| RP-GL-RECORDING-004 | Recording shall begin at the consent or notice timestamp; no pre-consent buffer shall be kept | Part 11.18a §11.18.5.13 | REC · ALL | DET | Gateway buffer flush at answer; start offset ≥ consent time | Block | Gateway log | "Recording started before consent. Audio discarded." |
| RP-GL-RECORDING-005 | When a party joins, recording shall pause, TPL-GL-REC-04 shall play and, where the mode is CONSENT_ALL, the new party's consent shall be captured before resuming | Part 11.18a §11.18.5.3.3 | REC · ALL | DET | `leg.joined` → pause; consent | Block | Leg events | "A new party joined. Recording paused until they agree." |
| RP-GL-RECORDING-006 | Recordings and transcripts shall be used only for the purposes stated in the notice or consent; coaching use requires the coaching purpose for every party and, for employees in Germany, a works agreement; recordings shall never be used to rank or make employment decisions | GDPR Art. 5(1)(b), Art. 88; BDSG §26; BetrVG §87(1) no. 6 (verify); DEC-870 | REC · ALL | DET | Purpose tags on consent; coaching source check (AU-282) | Block | Purpose record | "This use is not covered by the purpose given to the caller." |
| RP-GL-RECORDING-007 | When payment or card details may be discussed, recording shall pause with TPL-GL-REC-03 and DTMF shall be masked; card data shall never be recorded | PCI DSS (verify); RP-IN-PAY-002; RP-EU-PAY-002 | REC · ALL | DET | Payment intent → pause; DTMF suppression | Block | Pause events | "Recording paused for payment." |
| RP-GL-RECORDING-008 | Audio and transcripts shall be redacted for PII and PCI before persistence; if redaction fails the recording shall not be persisted | DEC-866; Part 11.18a R-1…R-6 | REC · ALL | DET | Redaction job status; `redaction_failed` → discard | Block | Redaction record | "Redaction failed. The recording was not stored." |
| RP-GL-RECORDING-009 | Recordings shall be stored only in the tenant's residency region with per-tenant keys; provider-side copies shall be deleted within 5 minutes with a deletion receipt | DEC-772; ADR-252; GDPR Ch. V (VR-24) | REC · ALL | DET | Region router; provider deletion receipt | Block | Storage and deletion receipts | "Recording storage is outside the allowed region or a provider copy remains." |
| RP-GL-RECORDING-010 | Retention shall follow the defaults (audio 90 days, persisted transcript 12 months) and never exceed the jurisdiction maximum in §11.15.36.12 unless a legal hold applies | DEC-865; Part 11.18a retention table | REC · ALL | DET | AU-286 retention job; max per row | Block | Deletion receipts | "This recording is past its retention period." |
| RP-GL-RECORDING-011 | Access shall be by role and purpose prompt, through 5-minute signed URLs, logged in `voice_access_log`; export only by R10 with watermark; bulk access over 20 per user per day alerts | Part 11.18a §11.18.5.13 access table | REC · ALL | DET | ABAC check; access log write | Block | Access log | "You do not have access to this recording for this purpose." |
| RP-GL-RECORDING-012 | Data-subject requests for access to or erasure of recordings shall be fulfilled within the jurisdiction's clock, except items on legal hold, which shall be reported as the law allows | GDPR Arts 15, 17 (VR-24); DPDP s.11–s.13 (VR-02); AU-174 | REC · ALL | DET | DSAR workflow across audio, transcript, excerpts | Block | DSAR record | "This data request is overdue." |
| RP-GL-RECORDING-013 | A persisted transcript shall exist only for a call recorded with a valid mode; otherwise only the transient working transcript (destroyed ≤ 10 minutes after the call) and the structured summary are kept | Part 11.18a §11.18.5.12 | REC · ALL | DET | Transcript persistence guard | Block | — | "No recording basis, so the transcript cannot be stored." |
| RP-GL-RECORDING-014 | Stored AI-generated audio shall carry provenance metadata (AI-generated, model registry ID, voice ID) | AI Act Art. 50(2) (VR-22); IT SGI Rules 2026 (VR-09) | REC · ALL | DET | Storage hook | Block | Object metadata | "AI audio must carry provenance metadata." |
| RP-GL-RECORDING-015 | Refusing recording shall not reduce the service given (except where law requires recording for the call type, such as UAE marketing calls, which then end) | GDPR Art. 7(4) (VR-24); RP-AE-VOICE-004 | REC, VO · ALL | DET+AI | DET: flow continues unrecorded; AI audit for pressure to accept recording | Block | Call audit | "Do not pressure people to accept recording." |
| RP-GL-RECORDING-016 | Consent, refusal, notice and objection evidence (timestamp, prompt hash, DTMF/ASR result, party) shall be retained for 6 years | Part 11.18a retention; GDPR Art. 7(1) | REC · ALL | DET | Retention class `rec_consent_6y` | Block | Evidence record | "Recording consent evidence must be retained." |

**Pack parameters (loaded by AU-128 and read by the PDP, AU-264/272/278/280/281/282; every value "verify at time of implementation, as of 28 Nov 2026" unless its VR entry is verified).**

| Parameter | Draft value | Source / note |
|---|---|---|
| default_mode | CONSENT_ALL | DEC-863 |
| consent_timeout_seconds | 6 | Part 11.18a |
| audio_retention_default_days | 90 | DEC-865 |
| transcript_retention_default_months | 12 | DEC-865 |
| provider_copy_delete_minutes | 5 | ADR-252 |
| bulk_access_alert_per_day | 20 | Part 11.18a |

### 11.15.36.5 Required disclosures and approved template wording

| Template | Use | English (approved draft wording) | Other languages | Placement |
|---|---|---|---|---|
| TPL-GL-REC-01 | Notice (NOTICE_OBJECT rows) (= TPL-VO-REC-01) | "This call is recorded and transcribed for quality, training and to keep a record of your request. Say 'don't record' at any time and we will stop." | hi/de/fr/ar/ta: as Part 11.18a drafts [ASSUMPTION-1066] | After AI disclosure |
| TPL-GL-REC-02 | Affirmative consent (= TPL-VO-REC-02) | "May we record and transcribe this call for quality, coaching and record keeping? Press 1 or say 'yes' to agree, press 2 or say 'no' to continue without recording." | as above | Before recording |
| TPL-GL-REC-03 | Payment pause (= TPL-VO-REC-03) | "For your security I've paused recording. Please don't share card details with me; I'll send you a secure link instead." | as above | On payment intent |
| TPL-GL-REC-04 | Joining party (= TPL-VO-REC-04) | "My colleague {first_name} is joining; the call {is / is not} being recorded as you agreed." | as above | On leg join |

### 11.15.36.6 Prohibited content and phrase lists

| List | Name | Terms | Match mode | Severity | Used by |
|---|---|---|---|---|---|
| PL-GL-REC-01 | Recording objection | don't record; stop recording; I don't agree; रिकॉर्ड मत करो; nicht aufnehmen; n'enregistrez pas; لا تسجل | phrase + ASR semantic | Block (triggers 003) | 003 |

**Prohibited (absolute, no mandate, exception or override can unlock):** recording before consent or notice; notice-only recording in all-party jurisdictions; storing unredacted audio; recording card data; using recordings for employment decisions.

### 11.15.36.7 Exceptions and edge cases

| # | Case | Treatment |
|---|---|---|
| E-1 | Emergency or threat during a call | Recording continues only in the mode already lawful; a legal hold may be placed by R10 |
| E-2 | Legal hold | Suspends deletion for named sessions until R10 releases (DEC-865) |
| E-3 | Internal staff-only calls | Employee notice and works agreement govern; this pack applies with the employee rows |

### 11.15.36.8 AI reviewer review guidance (RP-GL-RECORDING)

- **Reviewer:** AG-214 (redaction verifier) and AG-217 (audits), AG-086 contract.
- **Look for:** missed PII/PCI; pressure to accept recording; recording references in coaching without purpose.
- **Cite:** `RP-GL-RECORDING-0NN` and the pack version only; quote timestamp spans.
- **Escalate (`needs_counsel`):** any doubt on a party's location; employee recording outside a works agreement.
- **Never:** un-redact; decide the mode.

### 11.15.36.9 Test cases

| ID | Rule | Type | Input (summary) | Expected |
|---|---|---|---|---|
| TC-RP-GL-RECORDING-01 | 001 | Edge | IN caller, agent in DE joins | Mode becomes CONSENT_ALL; pause and consent |
| TC-RP-GL-RECORDING-02 | 001 | Edge | US mobile, state unknown | CONSENT_ALL |
| TC-RP-GL-RECORDING-03 | 002 | Negative | CA caller silent 6 s after prompt | Not recorded; refusal stored |
| TC-RP-GL-RECORDING-04 | 003 | Negative | NOTICE_OBJECT requested for FR | Block 003 |
| TC-RP-GL-RECORDING-05 | 004 | Negative | Gateway keeps 3 s pre-consent buffer | Discarded; finding 004 |
| TC-RP-GL-RECORDING-06 | 007 | Positive | Caller says "let me give you my card" | TPL-GL-REC-03; pause; link sent |
| TC-RP-GL-RECORDING-07 | 008 | Negative | Redaction service down | Not persisted; `redaction_failed` |
| TC-RP-GL-RECORDING-08 | 010 | Negative | DE audio at day 181 | Deleted by AU-286 (DE max 6 months) |
| TC-RP-GL-RECORDING-09 | 015 | Negative | Script says "we can only help if you allow recording" (IN) | Block 015 |

### 11.15.36.10 Machine-readable YAML (AU-128)

```yaml
# AU-128 load file. Generated from the rule table above; the table is the source of truth.
pack:
  id: RP-GL-RECORDING
  title: "Recording, persisted transcription and coaching use of calls: mode resolution, consent and notice, joining parties, payment pauses, redaction, residency, retention, access, DSAR, evidence"
  version: "0.1-draft"
  state: draft
  jurisdictions: "ALL (jurisdiction rows in §11.15.36.12; a row must be signed before recording is enabled in that jurisdiction)"
  channels: "REC (audio recording, persisted transcript, coaching excerpt), VO, CH"
  audiences: "ALL parties to the call (customers, prospects, employees, third parties)"
  startups: "ALL; Tenant"
  gates_mandate_types: "MT-OUT (voice) recording mode; SM-SVC-26-WF04; SM-SVC-36-WF03"
  effective_dates: "On sign-off per jurisdiction row"
  owner: R10
  review_cadence: quarterly
  expires_after_days: 120
  on_expiry: suspend_and_hold
  on_registry_unavailable: block
  on_unknown_jurisdiction: block
  level_cap: "Recording mode per §11.15.36.12; no recording without the mode's condition"
  sign_off: {counsel_reviewer: null, firm: null, date: null, r10_approver: null, conditions: null}
parameters:
  default_mode: "CONSENT_ALL"
  consent_timeout_seconds: "6"
  audio_retention_default_days: "90"
  transcript_retention_default_months: "12"
  provider_copy_delete_minutes: "5"
  bulk_access_alert_per_day: "20"
rules:
  - id: RP-GL-RECORDING-001
    obligation: "Before recording, the mode shall be resolved as the strictest of the rows applicable to every party's location (unknown location = CONSENT_ALL) and recorded with the signals used"
    citation: "DEC-863; CP-03; §11.15.36.12"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "AU-282 resolver over parties; evidence_ref of signals"
    severity: "Block"
    override: none
    evidence: "Mode decision record"
    remediation_message: "\"The recording mode could not be resolved. The call will not be recorded.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-002
    obligation: "In CONSENT_ALL mode, recording shall start only after every party has given affirmative consent with TPL-GL-REC-02; silence for 6 s or refusal means no recording, and refusal shall be stored"
    citation: "Part 11.18a §11.18.5.13; VR-72, VR-73, VR-77"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "Consent events per party; timeout 6 s"
    severity: "Block"
    override: none
    evidence: "Consent events"
    remediation_message: "\"Not every party agreed. The call is not recorded.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-003
    obligation: "NOTICE_OBJECT mode shall be used only where the jurisdiction row permits it and only for the purposes named in TPL-GL-REC-01; an objection at any time stops recording and deletes partial audio"
    citation: "VR-02, VR-38, VR-74; ASSUMPTION-1063"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "Row permits notice; objection detector → stop + delete"
    severity: "Block"
    override: none
    evidence: "Notice and objection events"
    remediation_message: "\"Notice-only recording is not allowed here, or the person objected.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-004
    obligation: "Recording shall begin at the consent or notice timestamp; no pre-consent buffer shall be kept"
    citation: "Part 11.18a §11.18.5.13"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "Gateway buffer flush at answer; start offset ≥ consent time"
    severity: "Block"
    override: none
    evidence: "Gateway log"
    remediation_message: "\"Recording started before consent. Audio discarded.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-005
    obligation: "When a party joins, recording shall pause, TPL-GL-REC-04 shall play and, where the mode is CONSENT_ALL, the new party's consent shall be captured before resuming"
    citation: "Part 11.18a §11.18.5.3.3"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "leg.joined → pause; consent"
    severity: "Block"
    override: none
    evidence: "Leg events"
    remediation_message: "\"A new party joined. Recording paused until they agree.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-006
    obligation: "Recordings and transcripts shall be used only for the purposes stated in the notice or consent; coaching use requires the coaching purpose for every party and, for employees in Germany, a works agreement; recordings shall never be used to rank or make employment decisions"
    citation: "GDPR Art. 5(1)(b), Art. 88; BDSG §26; BetrVG §87(1) no. 6 (verify); DEC-870"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "Purpose tags on consent; coaching source check (AU-282)"
    severity: "Block"
    override: none
    evidence: "Purpose record"
    remediation_message: "\"This use is not covered by the purpose given to the caller.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-007
    obligation: "When payment or card details may be discussed, recording shall pause with TPL-GL-REC-03 and DTMF shall be masked; card data shall never be recorded"
    citation: "PCI DSS (verify); RP-IN-PAY-002; RP-EU-PAY-002"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "Payment intent → pause; DTMF suppression"
    severity: "Block"
    override: none
    evidence: "Pause events"
    remediation_message: "\"Recording paused for payment.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-008
    obligation: "Audio and transcripts shall be redacted for PII and PCI before persistence; if redaction fails the recording shall not be persisted"
    citation: "DEC-866; Part 11.18a R-1…R-6"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "Redaction job status; redaction_failed → discard"
    severity: "Block"
    override: none
    evidence: "Redaction record"
    remediation_message: "\"Redaction failed. The recording was not stored.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-009
    obligation: "Recordings shall be stored only in the tenant's residency region with per-tenant keys; provider-side copies shall be deleted within 5 minutes with a deletion receipt"
    citation: "DEC-772; ADR-252; GDPR Ch. V (VR-24)"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "Region router; provider deletion receipt"
    severity: "Block"
    override: none
    evidence: "Storage and deletion receipts"
    remediation_message: "\"Recording storage is outside the allowed region or a provider copy remains.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-010
    obligation: "Retention shall follow the defaults (audio 90 days, persisted transcript 12 months) and never exceed the jurisdiction maximum in §11.15.36.12 unless a legal hold applies"
    citation: "DEC-865; Part 11.18a retention table"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "AU-286 retention job; max per row"
    severity: "Block"
    override: none
    evidence: "Deletion receipts"
    remediation_message: "\"This recording is past its retention period.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-011
    obligation: "Access shall be by role and purpose prompt, through 5-minute signed URLs, logged in voice_access_log; export only by R10 with watermark; bulk access over 20 per user per day alerts"
    citation: "Part 11.18a §11.18.5.13 access table"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "ABAC check; access log write"
    severity: "Block"
    override: none
    evidence: "Access log"
    remediation_message: "\"You do not have access to this recording for this purpose.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-012
    obligation: "Data-subject requests for access to or erasure of recordings shall be fulfilled within the jurisdiction's clock, except items on legal hold, which shall be reported as the law allows"
    citation: "GDPR Arts 15, 17 (VR-24); DPDP s.11–s.13 (VR-02); AU-174"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "DSAR workflow across audio, transcript, excerpts"
    severity: "Block"
    override: none
    evidence: "DSAR record"
    remediation_message: "\"This data request is overdue.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-013
    obligation: "A persisted transcript shall exist only for a call recorded with a valid mode; otherwise only the transient working transcript (destroyed ≤ 10 minutes after the call) and the structured summary are kept"
    citation: "Part 11.18a §11.18.5.12"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "Transcript persistence guard"
    severity: "Block"
    override: none
    evidence: "—"
    remediation_message: "\"No recording basis, so the transcript cannot be stored.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-014
    obligation: "Stored AI-generated audio shall carry provenance metadata (AI-generated, model registry ID, voice ID)"
    citation: "AI Act Art. 50(2) (VR-22); IT SGI Rules 2026 (VR-09)"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "Storage hook"
    severity: "Block"
    override: none
    evidence: "Object metadata"
    remediation_message: "\"AI audio must carry provenance metadata.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-015
    obligation: "Refusing recording shall not reduce the service given (except where law requires recording for the call type, such as UAE marketing calls, which then end)"
    citation: "GDPR Art. 7(4) (VR-24); RP-AE-VOICE-004"
    applies_to: "REC, VO · ALL"
    check: "deterministic_then_ai_review"
    detection: "DET: flow continues unrecorded; AI audit for pressure to accept recording"
    severity: "Block"
    override: r10_with_reason
    evidence: "Call audit"
    remediation_message: "\"Do not pressure people to accept recording.\""
    effective_from: null  # set at sign-off
  - id: RP-GL-RECORDING-016
    obligation: "Consent, refusal, notice and objection evidence (timestamp, prompt hash, DTMF/ASR result, party) shall be retained for 6 years"
    citation: "Part 11.18a retention; GDPR Art. 7(1)"
    applies_to: "REC · ALL"
    check: "deterministic"
    detection: "Retention class rec_consent_6y"
    severity: "Block"
    override: none
    evidence: "Evidence record"
    remediation_message: "\"Recording consent evidence must be retained.\""
    effective_from: null  # set at sign-off
phrase_lists:
  - id: PL-GL-REC-01
    name: "Recording objection"
    match: "phrase + ASR semantic"
    severity: "Block (triggers 003)"
    used_by: "003"
    terms:
      - "don't record"
      - "stop recording"
      - "I don't agree"
      - "रिकॉर्ड मत करो"
      - "nicht aufnehmen"
      - "n'enregistrez pas"
      - "لا تسجل"
templates:
  - id: TPL-GL-REC-01
    use: "Notice (NOTICE_OBJECT rows) (= TPL-VO-REC-01)"
    en: "\"This call is recorded and transcribed for quality, training and to keep a record of your request. Say 'don't record' at any time and we will stop.\""
    placement: "After AI disclosure"
  - id: TPL-GL-REC-02
    use: "Affirmative consent (= TPL-VO-REC-02)"
    en: "\"May we record and transcribe this call for quality, coaching and record keeping? Press 1 or say 'yes' to agree, press 2 or say 'no' to continue without recording.\""
    placement: "Before recording"
  - id: TPL-GL-REC-03
    use: "Payment pause (= TPL-VO-REC-03)"
    en: "\"For your security I've paused recording. Please don't share card details with me; I'll send you a secure link instead.\""
    placement: "On payment intent"
  - id: TPL-GL-REC-04
    use: "Joining party (= TPL-VO-REC-04)"
    en: "\"My colleague {first_name} is joining; the call {is / is not} being recorded as you agreed.\""
    placement: "On leg join"
```

### 11.15.36.11 Counsel sign-off block

| Field | Entry |
|---|---|
| Pack / version reviewed | RP-GL-RECORDING v0.1-draft → proposed v1.0 |
| Reviewer (name, enrolment/bar no., jurisdiction of admission) | _______________________ |
| Firm | _______________________ |
| Date of review | ____ / ____ / ______ |
| Rules approved as drafted | ☐ All ☐ All except: __________ |
| Rules amended (IDs and summary) | _______________________ |
| Pack parameters confirmed (values and sources) | ☐ All ☐ Amended: __________ |
| Citations confirmed against primary text (VR entries) | ☐ VR-02 ☐ VR-09 ☐ VR-22 ☐ VR-24 ☐ VR-38 ☐ VR-69 ☐ VR-72 ☐ VR-73 ☐ VR-74 ☐ VR-76 ☐ VR-77 |
| Translations reviewed by | _______________________ |
| Conditions or limitations of the sign-off | _______________________ |
| Next review due | ____ / ____ / ______ (≤ 120 days) |
| R10 approval (name, date) | _______________________ |
| Signature (counsel) / Signature (R10) | _______________ / _______________ |

### 11.15.36.12 Recording consent matrix by jurisdiction (the parameter table AU-282 loads; values verify, as of 28 Nov 2026)

| Jurisdiction | Legal model (summary) | Platform mode | Notice wording | Lawful basis (data protection) | Max audio retention (default 90 days) | Sources |
|---|---|---|---|---|---|---|
| IN India | No specific participant-recording statute; participant recording generally lawful; DPDP basis needed | NOTICE_OBJECT if pack approves s.7(a); CONSENT for coaching | TPL-GL-REC-01 / 02 | DPDP s.6 or s.7(a) [ASSUMPTION-1063, ASSUMPTION-1175] | 12 months | VR-02 |
| US federal / one-party states (e.g. NY, TX, OK, UT, VA, GA, NC, OH) | One-party consent (18 U.S.C. §2511(2)(d)); business is a party | NOTICE_OBJECT | TPL-GL-REC-01 | Notice | 12 months | VR-74 |
| US all-party states: CA, FL, IL, MD, MA, MT, NH, PA, WA (and NV for phone calls; MI disputed) | All-party consent | CONSENT_ALL | TPL-GL-REC-02 | Consent | 12 months | VR-73 [GAP-1176] |
| US hybrid: CT (civil: notice or consent for phone), DE, OR (in-person all-party) | Treated as all-party (platform) | CONSENT_ALL | TPL-GL-REC-02 | Consent | 12 months | VR-73 |
| US unknown state | — | CONSENT_ALL | TPL-GL-REC-02 | Consent | 12 months | Strictest wins |
| UK | Business recording lawful with reasonable notice (IPA 2016 and Interception by Businesses Regs 2018); UK GDPR basis | NOTICE_OBJECT if pack approves; CONSENT for coaching | TPL-GL-REC-01 | Legitimate interests (LIA) or consent | 12 months | VR-74, VR-38 |
| DE Germany | Recording non-public spoken word without consent is an offence (StGB §201) | CONSENT_ALL | TPL-GL-REC-02 | GDPR Art. 6(1)(a) | 6 months (platform for DE, verify) | VR-72 |
| FR France | Recording private speech without consent is an offence (Code pénal 226-1); CNIL: prior information and right to object; training recordings ≤ 6 months | CONSENT_ALL (platform) | TPL-GL-REC-02 | Consent | 6 months | VR-69 (CNIL guidance verify) |
| Other EEA | Counsel per state | CONSENT_ALL | TPL-GL-REC-02 | Consent | 6 months | Default strictest |
| AE UAE | Recording without consent is an offence (Decree-Law 34/2021 Art. 44; Decree-Law 31/2021 Art. 431); marketing calls must be recorded with notice (Res. 56/2024) | MANDATORY_WITH_CONSENT (marketing); CONSENT_ALL (other) | TPL-AE-VO-02 / TPL-GL-REC-02 | PDPL consent | 12 months (verify any minimum retention for marketing recordings) | VR-76, VR-77 [GAP-1177] |
| CA Canada (not activated) | One-party under Criminal Code s.184; PIPEDA requires notice and purpose | Not active | — | — | — | verify |
| AU Australia (not activated) | State/territory laws differ; most require consent | Not active | — | — | — | verify |

**Resolution rule.** Mode = strictest of all parties' rows (CONSENT_ALL > MANDATORY_WITH_CONSENT > NOTICE_OBJECT > OFF). A party whose location is unknown takes CONSENT_ALL. A party joining later re-evaluates the mode (rule 005).


---

## 11.15.37 Pack summary, applicability matrix and counsel confirmation list

### 11.15.37.1 Rules per pack (Batches 11.15d and 11.15e)

| Pack | Rules | Block | Warn | DET | AI | DET+AI | Phrase lists | Templates | Tests | Parameters | Template languages |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RP-IN-PAY | 20 | 20 | 0 | 17 | 0 | 3 | 3 | 6 | 14 | 13 | en, hi |
| RP-EU-PAY | 19 | 18 | 1 | 19 | 0 | 0 | 2 | 5 | 12 | 10 | en (de, fr: EPC official translations) |
| RP-GL-AGENTCOM | 16 | 16 | 0 | 12 | 0 | 4 | 3 | 4 | 11 | 6 | en |
| RP-IN-AGENTCOM | 13 | 12 | 1 | 12 | 0 | 1 | 1 | 2 | 7 | 4 | en |
| RP-EU-AGENTCOM | 12 | 12 | 0 | 11 | 0 | 1 | 1 | 1 | 6 | 2 | en |
| RP-GL-A2A-CONTRACT | 15 | 15 | 0 | 13 | 0 | 2 | 1 | 3 | 7 | 6 | en |
| RP-IN-PROC | 16 | 16 | 0 | 14 | 0 | 2 | 2 | 2 | 10 | 8 | en |
| RP-EU-PROC | 15 | 13 | 2 | 13 | 0 | 2 | 1 | 2 | 6 | 3 | en |
| RP-US-PROC | 14 | 13 | 1 | 12 | 0 | 2 | 1 | 1 | 6 | 4 | en |
| RP-IN-VOICE | 18 | 18 | 0 | 15 | 0 | 3 | 3 | 6 | 12 | 11 | en, hi (ta and other Indic: tier B, verbatim) |
| RP-US-VOICE | 20 | 20 | 0 | 19 | 0 | 1 | 1 | 4 | 11 | 9 | en (es optional, verify) |
| RP-EU-VOICE | 16 | 16 | 0 | 15 | 0 | 1 | 1 | 3 | 8 | 6 | en, de, fr (11.18a drafts); others pending |
| RP-AE-VOICE | 12 | 12 | 0 | 11 | 0 | 1 | 1 | 4 | 5 | 5 | en, ar (11.18a drafts) |
| RP-GL-RECORDING | 16 | 16 | 0 | 15 | 0 | 1 | 1 | 4 | 9 | 6 | en, hi, de, fr, ar, ta (Part 11.18a drafts) |
| **Total** | **222** | **217** | **5** | **198** | **0** | **24** | **22** | **47** | **124** | **93** | — |

Combined with Parts 11.15a–c (220 rules in 11 packs), Part 11.15 now holds **442 rules in 25 packs**. The securities packs of Part 11.16d are counted separately.

### 11.15.37.2 Applicability matrix (CP-01 extended)

| Pack | PAY | MND | COM/CTR | BID | VO/CH | REC | EM/SMS/WA (notices) | Jurisdiction trigger | Mandate / capability |
|---|---|---|---|---|---|---|---|---|---|
| RP-IN-PAY | ● | ● | ○ | — | ○ | — | ● | J8a IN | MT-PAY, MT-SPEND, MT-PROC |
| RP-EU-PAY | ● | ● | ○ | — | ○ | — | ● | J8a EEA | MT-PAY, MT-SPEND, MT-PROC |
| RP-GL-AGENTCOM | — | — | ● | — | — | — | — | Any party (with national pack) | MT-COM, MT-PROC |
| RP-IN-AGENTCOM | — | — | ● | — | — | — | — | J8b IN | MT-COM, MT-PROC |
| RP-EU-AGENTCOM | — | — | ● | — | — | — | — | J8b EEA | MT-COM, MT-PROC |
| RP-GL-A2A-CONTRACT | ○ | ● | ● | — | — | — | — | Any party | Interop gate FR-V12-P-076 |
| RP-IN-PROC | — | — | — | ● | ○ | — | ○ | J8c IN | MT-BID |
| RP-EU-PROC | — | — | — | ● | — | — | — | J8c EEA | MT-BID |
| RP-US-PROC | — | — | — | ● | ○ | — | ○ | J8c US federal | MT-BID |
| RP-IN-VOICE | — | — | — | — | ● | ○ | — | J3/J8d +91 | Voice (DEC-860/861) |
| RP-US-VOICE | — | — | — | — | ● | ○ | ○ | J8d US | Voice |
| RP-EU-VOICE | — | — | — | — | ● | ○ | — | J8d EEA / UK rows | Voice |
| RP-AE-VOICE | — | — | — | — | ● | ● | — | J8d +971 | Voice |
| RP-GL-RECORDING | — | — | — | — | ○ | ● | — | Every party's location | Recording (AU-282), coaching |

● applies · ○ applies to part of the channel · — not applicable.

### 11.15.37.3 Coverage of rules that Part 11.18 relies on (RECOMMENDATION-1073)

| Part 11.18a rule or table | Pack rule(s) now holding it |
|---|---|
| D-1…D-4 AI self-identification, identity challenge, no human impersonation, repeat on leg join | RP-IN-VOICE-006, RP-US-VOICE-007/016, RP-EU-VOICE-007, RP-AE-VOICE-006, RP-GL-RECORDING-005 |
| D-5 purpose and business identity; D-6 opt-out mechanism; D-7 provenance marking | RP-US-VOICE-007/008, RP-IN-VOICE-007, RP-GL-RECORDING-014, RP-EU-VOICE-007 |
| §11.18.5.3.1 consent standards and registries | RP-IN-VOICE-004/005, RP-US-VOICE-001…004, RP-EU-VOICE-001…003/015, RP-AE-VOICE-002/008 |
| §11.18.5.3.2 calling windows | RP-IN-VOICE-008, RP-US-VOICE-005 (+ state table), RP-EU-VOICE-004/005, RP-AE-VOICE-003 |
| §11.18.5.3.3 recording matrix; DEC-863 default | RP-GL-RECORDING-001…005 and §11.15.36.12 |
| §11.18.5.4 consent capture and withdrawal | RP-IN-VOICE-012, RP-US-VOICE-002/009, RP-EU-VOICE-008/010, RP-AE-VOICE-010 |
| §11.18.5.5 scrub and freshness, fail closed | RP-IN-VOICE-004, RP-US-VOICE-003/004, RP-EU-VOICE-015, RP-AE-VOICE-002 |
| §11.18.5.6 attempt caps, abandonment, ring time, complaint pause | RP-IN-VOICE-009/010/013, RP-US-VOICE-006/011, RP-EU-VOICE-004, RP-AE-VOICE-005 |
| §11.18.5.10 voicemail VM-1…VM-6 | RP-IN-VOICE-011, RP-US-VOICE-013, RP-EU-VOICE-011, RP-AE-VOICE-011 |
| §11.18.5.13 recording gate, storage, retention, redaction, access | RP-GL-RECORDING-004…013, 016 |
| §11.18.5.14 coaching from recordings | RP-GL-RECORDING-006 |
| §11.18.5.17 number rules (140/1600, CLI, STIR/SHAKEN, UAE local numbers) | RP-IN-VOICE-003, RP-US-VOICE-012, RP-EU-VOICE-006, RP-AE-VOICE-001 |

### 11.15.37.4 What counsel must still confirm (consolidated, continues C-01…C-12 of Part 11.15c)

| # | Item | Packs | Counsel |
|---|---|---|---|
| C-13 | Read VR-41…77 against primary text; confirm RBI E-mandate Framework 2026 transition clauses, Authentication Directions exemptions, PA Directions as updated 11 Nov 2026, NPCI AutoPay windows | RP-IN-PAY | India payments |
| C-14 | Platform as technology service provider, not a PA or payment system operator, given no funds are held [ASSUMPTION-1163] | RP-IN-PAY, RP-EU-PAY | India and EU payments |
| C-15 | SCA exemption usage for API payouts (RTS Arts 13, 17) by named PSPs; MIT treatment; PSR application date and switch-over | RP-EU-PAY | EU payments |
| C-16 | IT Act s.11(c) attribution of agent messages; s.12 acknowledgement design; First Schedule exclusions; stamp duty on ACFA and POs; MSMED 45-day rule | RP-IN-AGENTCOM, RP-GL-A2A-CONTRACT | India commercial |
| C-17 | E-Commerce Directive derogations in ACFA cl. 6; eIDAS seal vs signature; member-state overlay; GDPR Art. 22 for sole traders | RP-EU-AGENTCOM | EU commercial |
| C-18 | ACFA model terms (all 20 clauses and schedules), including liability, governing law and arbitration | RP-GL-A2A-CONTRACT | Commercial (India + EU) |
| C-19 | GeM GTC, CPPP and state portal terms on automation; Class III DSC; land-border and Make in India declarations; affiliate bidding | RP-IN-PROC | India procurement |
| C-20 | National eSubmission platform rows; qualified-seal acceptance; Art. 5k screening | RP-EU-PROC | EU procurement |
| C-21 | RFO clause sets; e-mail late-offer rule; OCI/affiliates; SAM.gov terms | RP-US-PROC | US government contracts |
| C-22 | TRAI promotional window and 2026 releases; DLT voice consent; India recording basis [ASSUMPTION-1175] | RP-IN-VOICE, RP-GL-RECORDING | India telecom |
| C-23 | PEWC elements post-2025; FCC Sept 2026 revocation order effective date and scope; state table; RND safe harbor; ring rule; ringless voicemail | RP-US-VOICE | US TCPA |
| C-24 | Member-state profiles (FR décret 2026-662 details, NL, IT, ES, IE); AI calls as automated calling; UK PECR rows | RP-EU-VOICE | EU and UK |
| C-25 | UAE Res. 56/57 text (refusal and repeat-call rules, recording retention), DNCR access, PDPL basis, recording-consent interplay | RP-AE-VOICE | UAE |
| C-26 | US all-party state list; DE/FR retention maxima; employee recording (works agreements) | RP-GL-RECORDING | US, DE, FR |

---

## 11.15.38 Effect on GAP-1044 and GAP-1046 (and on GAP-1067, GAP-1068, RECOMMENDATION-1073)

**GAP-1044 ("Part 11.15 has no payment, agentic-contracting or e-procurement packs"): drafted; pending counsel sign-off.**

| Element of GAP-1044 | Status after this part |
|---|---|
| RP-IN-PAY, RP-EU-PAY | **Drafted** (v0.1-draft): 20 + 19 rules with parameters the PDP reads (AFA limits, pre-debit lead, SDD pre-notification, VoP, refund rights) |
| RP-GL-AGENTCOM, RP-IN-AGENTCOM, RP-EU-AGENTCOM | **Drafted**: 16 + 13 + 12 rules |
| RP-IN-PROC, RP-EU-PROC, RP-US-PROC | **Drafted**: 16 + 15 + 14 rules; portal capability defaults set conservatively (GeM/CPPP ASSISTED_ONLY; US federal ASSISTED/MANUAL) |
| Synthetic packs in tests (`RP-*-syn`, Part 11.17b PP-P1) | Replace their parameter values with the parameter tables of these packs; keep the synthetic packs for tests in state `Approved` |
| Activation | Still blocked: no pack is signed (DEC-856 unchanged). GAP-1044 moves from **"authoring"** to **"review and sign-off"** and stays **open** until all eight sign-off blocks are complete |

**GAP-1046 ("contracting framework for agent-to-agent commerce, platform-not-a-party terms"): drafted; pending counsel sign-off.** RP-GL-A2A-CONTRACT (15 rules) makes an executed **Agent Commerce Framework Agreement** a hard precondition of interoperability. §11.15.28.12 gives the model terms in 20 clauses and four schedules: attribution, mandate limits, formation, input-error correction, conduct, platform not a party, liability, law and disputes. Still open: (a) the matching clause in the **tenant MSA** that the platform is a technology provider, not a party, holding no funds (Legal; no MSA text is in this part); (b) the consumer (B2C) agentic-commerce pack, out of scope in this release. GAP-1046 stays **open** until the ACFA is signed off and the MSA clause is adopted.

**GAP-1067 (UAE) and GAP-1068 (France).** Researched and drafted. The hours (09:00–18:00), licensed local numbers, DNCR and mandatory recording with notice come from Res. 56/57 of 2024 (VR-76). France's consumer opt-in from 11 Aug 2026, with consent valid one year and Bloctel discontinued, comes from VR-69. Both remain open only for counsel confirmation. Part 11.18a §11.18.5.3 still shows Bloctel and "reported" opt-in; the owner should align it [GAP-1172].

**RECOMMENDATION-1073.** Implemented: the voice and recording rules of Part 11.18 now live in four voice packs and RP-GL-RECORDING (§11.15.37.3), so counsel signs one source.

---

## 11.15.39 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-766 | Adopt the **14 additional packs** in Parts 11.15d–e as **v0.1-draft**, with the action-pack framework additions: channel codes PAY/MND/COM/CTR/BID/REC, `parameters`, `level_cap` and `gates_mandate_types` on `rulepack`, **CP-08** (pack caps the level), **CP-09** (parameter merge, strictest wins), **CP-10** (CP-07 read with the mandate amendments) and jurisdiction signal **J8**. No mandate type or voice capability activates in a jurisdiction until every gating pack in §11.15.22.5 is signed and Approved | Expert drafting; Founder DEC-776, DEC-779…782 | Implements MC-10, FR-V12-P-005, DEC-856, DEC-860/861; reduces GAP-1044 to review and sign-off |
| DEC-767 | **Agent-to-agent contracting** requires an executed Agent Commerce Framework Agreement (model terms §11.15.28.12) with each counterparty before interoperability; agents never negotiate or sign the ACFA; the platform is never a party, agent, guarantor or holder of funds (cl. 16 non-negotiable); B2B only | Pending counsel sign-off | Closes the drafting part of GAP-1046; enforces FR-V12-P-076 |
| DEC-768 | **Procurement defaults:** GeM, CPPP/GePNIC and state NIC portals ASSISTED_ONLY; unreviewed portals MANUAL_ONLY; reverse auctions and electronic auctions always human; US federal submissions ASSISTED/MANUAL except counsel-approved e-mail submission; personal DSC/QES never held or triggered by the system; declarations, ESPD and certifications never authored by AI; affiliate bids on the same tender need Legal clearance | Pending counsel sign-off [RECOMMENDATION-1171] | Tightens Part 11.17b expected defaults; no AUTO until portal rows are reviewed (GAP-1045) |
| DEC-769 | **Voice and recording defaults stricter than some laws:** (a) AI voice is treated as artificial/automated calling everywhere: outbound AI marketing calls need PEWC (US) or prior opt-in (EU/UK/AE), including to business numbers; (b) India promotional voice follows RP-IN-SMS-009 (09:00–19:00 Mon–Sat), service calls 09:00–21:00; (c) recording default CONSENT_ALL with unknown location = all-party, and Germany audio retention maximum 6 months; (d) US revocation applies to all marketing calls of the seller regardless of narrower FCC scope; (e) UAE outbound marketing stays L1 in v0.1 and refusal of the mandatory recording ends the marketing call | Pending counsel sign-off | Aligns Part 11.18 with Part 11.15 (CP-03); resolves the India window difference in favour of the stricter rule [GAP-1174] |

---

## 11.15.40 Tags register

| Tag | Type | Statement | Where used | Owner / resolution |
|---|---|---|---|---|
| GAP-1160 | Gap | Regulator primary texts (RBI, NPCI, FCC, EUR-Lex, DGCCRF, UAE legislation, acquisition.gov) were located but read only through search summaries; counsel must read primary text | §11.15.21 | Counsel (C-13…C-26) |
| GAP-1161 | Gap | RBI PA Directions updated 11 Nov 2026 and Authentication Directions exemptions not read in full; e-NACH limits and NPCI AutoPay peak windows not verified | RP-IN-PAY rules 001, 016, 019; VR-43, VR-44 | India payments counsel |
| GAP-1162 | Gap | PSD3/PSR not yet in the Official Journal; RP-EU-PAY drafted on PSD2/RTS with rule 018 dormant | RP-EU-PAY-018; VR-48 | R10; MAJOR revision on publication |
| ASSUMPTION-1163 | Assumption | The platform is a technology service provider, not a payment aggregator or payment system operator, because it never receives, holds or settles funds and the tenant is merchant of record | RP-IN-PAY-001/019; RP-EU-PAY-001; §11.15.20 | Counsel C-14 |
| ASSUMPTION-1164 | Assumption | Messages from the tenant's agent are attributable to the tenant under IT Act s.11(c) as an information system programmed on its behalf to operate automatically, supported by a tenant attestation | RP-IN-AGENTCOM-002; ACFA Sch. 1 | Counsel C-16 |
| GAP-1165 | Gap | India is not shown as a party to the UN ECC and Indian law gives no statutory input-error right; error correction depends on contract (ACFA cl. 7) | RP-IN-AGENTCOM-006; VR-53 | Counsel C-16 |
| RECOMMENDATION-1166 | Recommendation | Make the ACFA a hard precondition of interop, with a default input-error window of 2 business hours before performance and a 60-second signed confirmation | RP-GL-A2A-CONTRACT; RP-GL-AGENTCOM-008 | R10 (DEC-767) |
| GAP-1167 | Gap | Card-network agentic tokens are not generally available in India (controlled demonstrations only) and RBI tokenisation binds tokens to merchant and device; agent tokens are disabled in India | RP-IN-PAY-017; VR-51 | Payments counsel; re-check quarterly |
| GAP-1168 | Gap | No express automation clause found in GeM GTC or CPPP terms; capability must be set per portal by counsel (extends GAP-1045) | RP-IN-PROC-002; VR-58 | Counsel C-19 |
| ASSUMPTION-1169 | Assumption | An EU contracting authority may accept a qualified electronic seal of the bidder instead of a person's signature; AUTO is possible only where the tender and platform row confirm this | RP-EU-PROC-003 | Counsel C-20 |
| GAP-1170 | Gap | FAR clause numbering is changing under the Revolutionary FAR Overhaul; RP-US-PROC cites pre-overhaul FAR and reads each solicitation's clause set | RP-US-PROC-011; VR-63 | US counsel C-21 |
| RECOMMENDATION-1171 | Recommendation | Offer no AUTO submission to US federal agencies in v0.1 except counsel-approved designated e-mail submission; SAM.gov actions human-only | RP-US-PROC-002/003; DEC-768 | R10 / Founder |
| GAP-1172 | Gap | France moved to consumer opt-in on 11 Aug 2026 and Bloctel ceased; Part 11.18a §11.18.5.3.1/§11.18.5.5 and AU-280 still reference a Bloctel scrub (not edited here) | RP-EU-VOICE-003; VR-69 | **Closed v1.2** (Part 11.25): Part 11.18a and the 11.18c/d voice oracle aligned; counsel C-24 confirmation remains |
| GAP-1173 | Gap | FCC Sept 2026 order revises the "revoke all" rule previously waived to 31 Jan 2027; Part 11.15a VR-30 and Part 11.18a are out of date; RP-US-VOICE-009 keeps the stricter seller-wide scope | RP-US-VOICE-009; VR-67 | **Closed v1.2** (Part 11.25): Part 11.15a VR-30 and Part 11.18a updated; US counsel C-23 confirmation remains |
| GAP-1174 | Gap | TRAI promotional calling window still unverified (VR-13, VR-75); Part 11.18a uses 09:00–21:00 for India while RP-IN-SMS-009 sets 09:00–19:00 Mon–Sat for promotional SMS and voice; DEC-769(b) applies the stricter window | RP-IN-VOICE-008 | **Closed v1.2** for the blueprint text (Part 11.18a window table and oracle aligned to 09:00–19:00 Mon–Sat); TRAI legal window still for counsel C-22 |
| ASSUMPTION-1175 | Assumption | India has no general all-party recording statute; participant recording with notice and a DPDP basis is lawful (extends ASSUMPTION-1063) | RP-GL-RECORDING §11.15.36.12 | Counsel C-22 |
| GAP-1176 | Gap | Sources conflict on the US all-party list (MT, NV, MI, CT, DE, OR); the platform treats disputed states as all-party | RP-GL-RECORDING matrix; VR-73 | US counsel C-26 |
| GAP-1177 | Gap | UAE law requires recording of marketing calls with notice while recording without consent is an offence; the platform obtains consent and ends refused calls; refusal, repeat-call and retention details of Res. 56/57 still need primary-text confirmation (narrows GAP-1067) | RP-AE-VOICE-004/005; VR-76, VR-77 | UAE counsel C-25 |
| GAP-1178 | Gap | Member-state voice profiles for NL, IT, ES, IE and others rest on secondary sources (Spain conflicting) | RP-EU-VOICE §11.15.34.12; VR-70, VR-71 | EU counsel C-24 |
| RECOMMENDATION-1179 | Recommendation | Engage counsel in lots: India (PAY, AGENTCOM, PROC, VOICE); EU (PAY, AGENTCOM, PROC, VOICE); US (PROC, VOICE, recording states); UAE (VOICE); UK counsel for the UK rows of RP-EU-VOICE and the recording matrix, splitting them into RP-UK-VOICE at sign-off. Budget within the Part 11.17b counsel line (₹6.0–20.0 L for the eight GAP-1044 packs; verify by quotes) plus voice packs (estimate ₹3.0–8.0 L, verify) | §11.15.37.4 | R10 / Founder |

---

## 11.15.41 Quality gate (Batches 11.15d and 11.15e)

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every rule cites a statute, regulation, regulator direction, scheme rule, portal term or blueprint ID (DEC-, MC-, FR-V12-P/Q-, BRL-, Part 11.17/11.18 sections); platform tightenings cite DEC-766…769 |
| 2 | Assumptions, gaps and conflicts tagged and logged | Pass | 20 tags (GAP/ASSUMPTION/RECOMMENDATION-1160…1179) in §11.15.40; no CONFLICT tag (inconsistencies with Parts 11.15a and 11.18a are logged as GAP-1172, 1173, 1174 and not edited) |
| 3 | IDs unique and consistent with earlier parts | Pass | DEC-766…769 unused before (checked by grep); VR-41…77 continue VR-01…40; pack, rule, list, template and test IDs new; references to MC-, PDP rules, MT-*, AU-, AG-, TPL-VO-* match Parts 11.17 and 11.18 |
| 4 | No story lacks AC and no requirement lacks a test | Pass (N/A for stories) | No new stories; each pack has positive, negative and boundary tests (124 pack tests); full rule coverage via synthetic-pack combinatorial models of Parts 11.17b/11.18d and AG golden sets extended per pack at Q5 |
| 5 | Negative, edge, security and accessibility cases covered | Pass | Boundary tests on AFA limit, pre-debit lead, SDD notice, deadlines, windows; security cases on credential collection (RP-IN-PAY-002/009), counterparty injection (RP-GL-AGENTCOM-012), DSC custody (RP-IN-PROC-003), CUI (RP-US-PROC-009), redaction fail-closed (RP-GL-RECORDING-008); accessibility via DTMF alternatives (person/opt-out keys) |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | N/A | No new agent; reviewer mapping §11.15.22.4 uses existing AG cards; fallback per CP-05/CP-08 |
| 7 | Time-sensitive facts flagged "verify" with an as-of date | Pass | VR-41…77 with "verified as of 28 Nov 2026, source" or "verify"; every parameter carries its source or "verify"; primary-text reading outstanding (GAP-1160) |
| 8 | No restricted data routed to free-tier models | Pass | Payment, commerce, bid and voice data are Confidential/Restricted; reviewers run Tier 1 only; RP-IN-PAY-002, RP-GL-RECORDING-008 prevent credentials and unredacted audio reaching any model |
| 9 | Consistent with earlier parts | Pass with observations | Follows Part 11.15a template and CP-01…07; Part 11.17 mandate engine and gating; Part 11.18 voice controls. Observations (not fixed here): Part 11.18a Bloctel references (GAP-1172), India voice window (GAP-1174), Part 11.15a VR-30 revocation status (GAP-1173), Part 11.17a §11.17.5.15 note "packs not yet in Part 11.15" now superseded by §11.15.22.5 |

**Status: Part 11 Batch 11.15d–e complete. 14 additional rule packs drafted as v0.1-draft for counsel review (222 rules, 22 phrase lists, 47 templates, 124 pack tests, parameter tables and AU-128 YAML, sign-off blocks), including the eight GAP-1044 packs, RP-GL-A2A-CONTRACT with the Agent Commerce Framework Agreement model terms (GAP-1046), four voice packs plus RP-AE-VOICE, and RP-GL-RECORDING with the one-party/all-party matrix; VR-41…77; decisions DEC-766…769; 20 tags (1160–1179). This is a draft for review by qualified counsel, not legal advice. Nothing activates until counsel signs off each pack (FR-V12-M-028; DEC-856).**
