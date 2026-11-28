#!/usr/bin/env python3
"""Part 11.22 (Group U): end-to-end persona journeys for the full V12 product.

Each step names the stage, the touchpoint (screen IDs), what the persona does,
what the system does (the control that applies) and the stories that deliver it.
A reference that starts with "FR-V12-" is resolved at build time to the new
US-<EP>-ZU<nn> story that carries that requirement; every other reference must
be an existing story ID (checked at build time; the build fails otherwise).
Each journey also declares a small variant model; its pairwise permutations
become the Examples of the journey's end-to-end Scenario Outline.
"""
from u_03_models import REGION, JURIS, AUTONOMY, CONSENT, SKU, X, P

J = []
def journey(**kw):
    J.append(kw)

journey(id='JN-01', persona='Owner / founder', pid='P01', roles='R01 Founder / Portfolio Owner',
  goal='Adopt V12 across the owner portfolio, steer growth through the command centre, and open new markets and the fundraising product safely',
  pre='Owner Portfolio tenant exists; AppNAI, MedMaarg, EduVerse and OrganicSpec are separate company tenants (US-01-YA01)',
  steps=[
   ('Set up the portfolio', 'A197, A203', 'Chooses the residency zone of each owned tenant and connects the corporate IdP', 'Residency fixed at onboarding (DEC-772); SSO with break-glass before enforcement', ['US-01-YA01', 'US-01-ZR28', 'FR-V12-K-121', 'US-01-ZR01']),
   ('Choose services', 'W06, A184, A192', 'Selects full suite for AppNAI and selective SKUs for MedMaarg', 'Bundles expand to released SKU IDs only; foundations always included', ['US-29-YB02', 'US-20-YA01', 'FR-V12-A-005']),
   ('Set budgets and AI ceilings', 'A012, A198', 'Sets tenant, company and workflow AI budgets', 'Soft cap alerts at 80%, hard cap holds AI steps with no provider call', ['FR-V12-F-013', 'US-04-YM37', 'US-04-ZR23']),
   ('Approve a bounded mandate', 'A106, A109', 'Co-approves an L3 follow-up mandate with the startup head', 'Two distinct approvers; scope, caps, window, jurisdiction; instant revocation (DEC-779)', ['US-18-ZP01', 'US-18-ZP02', 'US-18-ZP05']),
   ('Read the decision flash', 'A089, A106', 'Reviews the daily decision-first flash and the 9 optimisation perspectives', 'Only data the owner may see; numbers defined once in the metric registry', ['US-17-YM21', 'US-17-YG02', 'FR-V12-A-121', 'FR-V12-A-150']),
   ('Grant portfolio aggregates', 'A191', 'Grants the group CFO aggregate-only access across companies', 'Owner authority and explicit aggregate scope; revocable; no record access', ['US-01-YE02', 'FR-V12-H-016']),
   ('Stop an anomaly', 'A110, A113', 'Engages the kill switch for one workflow after an anomaly alert', 'Kill switch by scope; tighten-only suspension; reconciliation', ['US-18-ZP06', 'US-18-ZP07', 'FR-V12-F-020']),
   ('Open a market', 'A200, A090', 'Approves the UAE market after counsel and tax sign-off', 'Market opens only with an Approved pack and tax configuration (DEC-776)', ['US-03-YA01', 'FR-V12-K-144', 'FR-V12-K-149', 'FR-V12-K-152']),
   ('Start fundraising', 'A205, W55', 'Subscribes AppNAI to Investment Automation and registers "Seed 2027"', 'Separate product code; securities pack and counsel sign-off per jurisdiction (DEC-783)', ['US-30-ZN01', 'FR-V12-A-006', 'US-31-ZN01']),
   ('Decide go / no-go', 'A090, A190', 'Signs the Release 2 go/no-go from the evidence register', 'Gate cannot pass with missing evidence; P0 controls block affected SKUs', ['US-21-YJ03', 'FR-V12-A-190', 'FR-V12-A-191']),
   ('Compare with peers', 'A089', 'Reads privacy-preserving peer benchmarks', 'Cohorts ≥ 10 tenants with noise; opt-in by contract (DEC-789)', ['US-17-ZR24', 'US-17-ZR25']),
  ],
  model=[('region', REGION), ('jurisdiction', JURIS), ('autonomy/mandate', AUTONOMY), ('channel', P('C1 web desktop', 'C2 mobile web'))],
  outcome='portfolio steered within budgets, mandates and market gates')

journey(id='JN-02', persona='Tenant administrator', pid='P11 (and P13 during application)', roles='R12 Tenant Administrator; R17 SaaS Client Applicant',
  goal='Onboard an external tenant end to end: apply, accept, provision, connect identity and systems, and run it safely through to offboarding',
  pre='A company "Kestrel Analytics Pvt Ltd" has chosen the platform; no tenant exists yet',
  steps=[
   ('Apply', 'W32, W33', 'Completes the eight-stage application and continues on a phone', 'Server-side drafts; stale revisions rejected; cross-device handoff never activates a subscription', ['US-20-YE02', 'US-20-YA06', 'FR-V12-A-095', 'FR-V12-E-032']),
   ('Accept the quote', 'W23, A187', 'Accepts the exact quote revision', 'Acceptance bound to revision and digest; quote pending shown when no approved rate card', ['US-20-YE05', 'US-20-YA03', 'FR-V12-A-030']),
   ('Get provisioned', 'A184', 'Waits for provisioning after payment', 'Provisioning only after a verified payment event; saga holds and compensates', ['US-20-YE06', 'US-20-YE03']),
   ('Choose residency', 'W33, A197', 'Selects the EU zone', 'Region immutable after onboarding; cross-region writes rejected', ['US-01-ZR28', 'FR-V12-I-013']),
   ('Connect identity', 'A203', 'Connects the IdP, verifies the domain and enforces SSO', 'Break-glass account required before enforcement; MFA policy; session limits', ['US-01-ZR01', 'US-01-ZR02', 'FR-V12-K-101', 'FR-V12-K-106']),
   ('Provision users', 'A203', 'Turns on SCIM provisioning', 'De-provisioned users lose sessions and API access', ['US-01-ZR03', 'FR-V12-K-103']),
   ('Define roles', 'A002', 'Builds custom roles', 'Separation of duties enforced at build and at run time', ['US-01-ZR04', 'FR-V12-K-108', 'FR-V12-I-008']),
   ('Configure the business', 'A197', 'Adds companies, brands, markets and channel accounts', 'Pending configuration reviewed by a second person; rollback is a new reviewed version', ['US-01-YE01', 'FR-V12-A-093', 'FR-V12-A-075']),
   ('Connect systems', 'A008, A168', 'Activates the CRM connector and issues API keys', 'Activation gate: security review, DPA, transfer basis, channel registration', ['US-18-ZR11', 'FR-V12-K-128', 'US-20-ZR06', 'FR-V12-K-112']),
   ('Stream audit', 'A009', 'Streams audit to the SIEM and exports the trail', 'Hash-chained audit; TLS-only sinks; 1/3/7-year retention', ['US-01-ZR05', 'FR-V12-K-110', 'FR-V12-I-009']),
   ('Offboard', 'A184, W34', 'Requests a full export and offboarding', 'Second approver; hashed manifest; 7-day link; retention rules', ['US-20-YE14', 'FR-V12-K-119', 'FR-V12-A-013']),
  ],
  model=[('region', REGION), ('service/SKU', SKU), ('channel', P('C1 web desktop', 'C2 mobile web', 'C3 API'))],
  outcome='tenant live with SSO, SCIM, roles, connectors and audit; offboarding evidenced')

journey(id='JN-03', persona='Sales executive', pid='P03', roles='R03 Growth Manager (R03L Sales Lead approves)',
  goal='Turn qualified opportunities into meetings, proposals and contracts across email, SMS, WhatsApp and AI voice, within consent, mandate and pack rules',
  pre='Startup AppNAI subscribed to SM-SVC-03…10, 17, 18 and 26; seller has R03 on AppNAI',
  steps=[
   ('Plan the day', 'A106, A034', 'Opens the daily worklist of eligible prospects with drafts', 'Only eligible contacts; contact pressure limited across services', ['US-08-YM03', 'US-05-YM32']),
   ('Qualify', 'A022–A025', 'Reviews match and score with evidence', 'Explainable scores; unknown inputs shown as unknown', ['US-06-YC04', 'US-06-YC03']),
   ('Preflight', 'A034', 'Runs the dispatch preflight', 'Nine checks in fixed order; dry-run has zero provider calls', ['FR-V12-D-007', 'FR-V12-D-008']),
   ('Check law and consent', 'A200, A201', 'Sees a UK contact held because the UK pack is Draft', 'Only Approved packs enforce; withdrawn consent holds queued runs', ['FR-V12-F-042', 'FR-V12-F-044', 'US-03-YG02']),
   ('Send and follow up', 'A034, A035', 'Sends email and an SMS follow-up', 'DLT and registry scrub; 09:00–21:00 local window (DEC-777)', ['US-08-YC06', 'US-23-ZR14', 'FR-V12-F-045']),
   ('Call with AI voice', 'A170', 'Lets the AI voice agent place a consented call', 'AI discloses itself; recording only with notice/consent; human handoff on every call', ['US-22-ZQ03', 'US-22-ZQ01', 'US-22-ZQ05', 'US-22-ZQ02']),
   ('Book the meeting', 'A040, W18', 'Books a demo', 'Calendar and timezone aware; confirmation to the attendee', ['US-09-YC10']),
   ('Propose and quote', 'A065–A068', 'Prepares a proposal and quote', 'Approved price version only; discount over limit routes to R03L', ['US-13-YC17', 'US-13-YB03']),
   ('Negotiate and contract', 'A069–A072', 'Negotiates within approved bounds and sends the contract', 'Clause findings; e-signature; signed hash stored', ['US-13-YC18', 'US-13-YF18']),
   ('Keep the CRM true', 'A029', 'Sees the deal synced to Salesforce', 'Field ownership; protected consent fields never overwritten', ['US-07-ZR12', 'US-07-ZR13']),
   ('Improve', 'A180', 'Reviews coaching from permitted call recordings', 'Only recordings with consent; rubric calibrated', ['US-08-ZQ01', 'US-08-ZQ02']),
   ('Submit a bid (AppNAI)', 'A104', 'Lets the agent submit a sealed bid under a per-tender mandate', 'Human approved package hash, price, terms and portal before the mandate (DEC-781)', ['US-14-ZP01', 'US-14-ZP02', 'US-14-ZP03']),
  ],
  model=[('jurisdiction', JURIS), ('consent', CONSENT), ('autonomy/mandate', AUTONOMY), ('channel', P('email', 'SMS', 'AI voice', 'WhatsApp'))],
  outcome='meeting booked and contract sent with every dispatch rechecked by the PDP')

journey(id='JN-04', persona='Marketer', pid='P05', roles='R05 Marketing Specialist (R05L Marketing Lead approves)',
  goal='Plan, create, approve and run compliant multichannel campaigns and measure them with consent-aware analytics',
  pre='MedMaarg subscribed to SM-SVC-11…16, 27, 30 and 38',
  steps=[
   ('Define audiences', 'A056', 'Defines an offering-specific audience for India and the EU', 'Market eligibility and source rights by offering; no cross-product assumptions', ['FR-V12-A-078', 'US-06-YD01']),
   ('Preflight the campaign', 'A056', 'Runs the campaign pre-flight', 'Pre-flight attached to the approval so approvers see risks', ['US-12-YM15', 'US-12-YM16']),
   ('Create content', 'A050–A052, A171', 'Generates copy, images and a short video', 'Rights, brand and claim QA before approval; metered per asset', ['US-11-YC11', 'US-11-YD01', 'US-28-YB01', 'US-28-YB02']),
   ('Label AI content', 'A171', 'Publishes with AI labels', 'Machine-readable marking; undisclosed AI content in the EU is held', ['FR-V12-F-047', 'US-11-YM35', 'US-03-YM38']),
   ('Search and social', 'A053–A055', 'Publishes SEO pages and social posts', 'Approved claims only; listening drafts need approval', ['US-11-YC13', 'US-11-YC12']),
   ('Email and SMS', 'A034, A182', 'Sends an email wave and an SMS reminder', 'DLT templates, NCPR/DND scrub, local window', ['US-08-YC06', 'US-23-YB02', 'FR-V12-F-045']),
   ('Landing pages', 'A058, W10', 'Publishes a landing page with intake', 'Consent captured with notice version; spam and minors checks', ['US-12-YC15', 'US-03-YG07']),
   ('Experiment', 'A174', 'Runs a pre-registered A/B test', 'Guardrail metrics; human decision', ['US-12-YD01', 'US-12-YI01']),
   ('Measure', 'A088', 'Reads consent-aware acquisition analytics', 'No tracking without consent; zero denominators shown as not applicable', ['FR-V12-I-045', 'FR-V12-A-152']),
  ],
  model=[('jurisdiction', JURIS), ('consent', CONSENT), ('channel', P('email', 'SMS', 'social', 'landing page')), ('region', REGION)],
  outcome='campaign live in approved markets with labelled AI content and measured results')

journey(id='JN-05', persona='Approver', pid='P02', roles='R02 Startup Head; R03L Sales Lead; R05L Marketing Lead',
  goal='Approve exactly what was reviewed, quickly and from any device, without ever approving one\'s own request',
  pre='Pending items exist in the action inbox: a discount, a campaign, a mandate and a bid package',
  steps=[
   ('Open the inbox', 'A106', 'Opens the scoped action inbox', 'Items limited to the approver\'s scope; operations separate', ['US-17-YG03']),
   ('Review a group', 'A106', 'Reviews similar items as one group with outliers highlighted', 'Neutral note with risks and diffs', ['US-18-YM05', 'US-18-YM06']),
   ('Approve the exact item', 'A106', 'Approves a payload', 'Approval bound to payload, amount, policy and hash', ['US-18-YD03', 'FR-V12-F-034']),
   ('Refuse a conflict', 'A106', 'Is blocked from approving own request', 'SoD at build and at run time', ['US-01-ZR04', 'FR-V12-I-008', 'FR-V12-K-108']),
   ('Co-approve a mandate', 'A109', 'Gives the second approval of a bounded mandate', 'Two distinct people; caps and window visible', ['US-18-ZP02']),
   ('Approve price and discount', 'A066', 'Approves a discount within authority', 'Over-limit routes to a higher approver', ['US-13-YC17']),
   ('Seal a bid', 'A104', 'Approves the sealed bid package', 'Hash, price, terms and portal fixed before the mandate', ['US-14-ZP01']),
   ('Resolve competing actions', 'A106', 'Chooses one of two competing actions to the same account', 'Only the selected eligible action proceeds', ['FR-V12-F-048']),
   ('Approve on the phone', 'A106 (360 px)', 'Approves a low-risk item on mobile', 'Same checks on mobile; step-up for privileged actions', ['US-17-YG05', 'FR-V12-K-104']),
  ],
  model=[('authority', {'A1 authorised': X, 'A3 SoD conflict or over limit': (4, '403 `SOD_CONFLICT` – routed to another approver')}),
         ('channel', P('C1 web desktop', 'C2 mobile web')), ('autonomy/mandate', AUTONOMY), ('region', REGION)],
  outcome='exact item approved once, by an eligible person, with the evidence recorded')

journey(id='JN-06', persona='Finance', pid='P08', roles='R08 Finance Maker; R09 Finance Checker',
  goal='Bill, collect, pay, reconcile and report every rupee and euro with maker-checker control and evidence',
  pre='Kestrel Analytics has an active subscription and AppNAI uses payment mandates through a licensed PSP',
  steps=[
   ('Price and tax', 'A186, A187', 'Checks the quote price and tax lines', 'Approved rate card or "Quote pending"; tax per approved rule', ['FR-V12-A-030', 'US-20-YE10', 'FR-V12-K-149']),
   ('Invoice and collect', 'A187', 'Issues invoices and runs dunning', 'Integer minor units; suspension only after grace', ['US-20-YE11', 'FR-V12-K-153']),
   ('Handle a dispute', 'A187, W26', 'Resolves a billing dispute with a credit note', 'Private case; refund only under policy with maker-checker', ['FR-V12-A-034', 'US-20-YE12']),
   ('Pay under mandate', 'A073', 'Lets an approved payment mandate pay a supplier through the PSP', 'Per-transaction and period caps; counterparty allowlist (DEC-780)', ['US-15-ZP01']),
   ('Reconcile', 'A074', 'Reconciles settlements and posts journals', 'Unmatched items held; nothing posted twice', ['US-15-ZP02', 'US-15-ZP03']),
   ('Recognise revenue', 'A187', 'Runs daily revenue recognition and month close', 'Schedule reconciles to ledger', ['US-20-YE13', 'FR-V12-E-077']),
   ('Know unit cost', 'A012, A101', 'Reviews per-SKU cost and TCO', 'Cost per accepted output; price floor formula', ['FR-V12-A-032', 'FR-V12-A-031', 'FR-V12-F-014']),
   ('Check AI spend', 'A012', 'Reconciles AI usage with provider invoices', 'Every model call metered; tolerance check', ['FR-V12-F-012', 'FR-V12-F-030']),
   ('Report in two currencies', 'A089', 'Reports INR and EUR', 'Native totals; converted totals only with an approved rate', ['FR-V12-K-150', 'FR-V12-I-018', 'FR-V12-A-036']),
   ('Verify investor receipts (INV)', 'A229', 'Verifies investor receipts and allotment clocks', 'No custody; receipts evidence only; day-60 allotment block (IN)', ['US-31-ZN12', 'FR-V12-O-014', 'FR-V12-N-028']),
  ],
  model=[('authority', {'A1 authorised': X, 'A3 SoD conflict or over limit': (4, '403 `SOD_CONFLICT` – checker must differ from maker')}),
         ('jurisdiction', {'IN GST rules Approved': X, 'EU VAT rules Approved': X, 'UK VAT rules Draft': (6, 'HOLD `TAX_RULE_NOT_APPROVED`')}),
         ('region', REGION), ('currency', P('INR', 'EUR'))],
  outcome='ledger reconciled with maker-checker evidence and correct tax')

journey(id='JN-07', persona='Compliance / counsel', pid='P09', roles='R10 Legal / Compliance / DPO; R10C external counsel (Part 11.16a)',
  goal='Author, sign off and enforce jurisdiction rule packs, consent, privacy rights, AI disclosure, recordings and securities rules, with evidence',
  pre='Rule-pack registry holds RP-IN, RP-EU, RP-UK (Draft) and the securities packs of Part 11.16d',
  steps=[
   ('Author and sign off a pack', 'A200', 'Signs off RP-EU after counsel review', 'Versioned packs; only Approved enforced; unreviewed → stricter outcome', ['US-03-YM09', 'FR-V12-F-042', 'FR-V12-K-144']),
   ('Gate a market', 'A200', 'Leaves RP-UK in Draft', 'Outbound blocked until counsel approves', ['US-03-YA01']),
   ('Run the consent ledger', 'A201', 'Investigates a withdrawal', 'Scoped consent; withdrawal holds queued runs', ['US-03-YG03', 'FR-V12-F-044']),
   ('Meet rights clocks', 'A163, W49', 'Completes a DSAR before its clock', 'Clocks start at detection; identity verified before completion', ['US-03-YI02', 'FR-V12-F-046']),
   ('Handle a breach', 'A202', 'Opens a breach with notification clocks', 'Per-pack deadlines; tabletop evidence', ['US-03-YG04', 'US-21-YI03']),
   ('Require AI disclosure', 'A199', 'Checks AI labels', 'Undisclosed AI content in the EU is held', ['FR-V12-F-047', 'US-03-YM38']),
   ('Govern recordings', 'A170', 'Approves the recording-notice wording per jurisdiction', 'All-party consent where required; retention and redaction', ['US-22-ZQ05', 'US-22-ZQ10']),
   ('Register an offering', 'A232', 'Signs off the s.42 route for "Seed 2027"', 'Counsel sign-off per jurisdiction before activation', ['US-31-ZN01', 'US-33-ZO12']),
   ('Review promotions', 'A256', 'Reviews a financial promotion and legends', 'UK s.21 approver gateway; no public offer where prohibited', ['US-33-ZO14', 'FR-V12-N-021']),
   ('Keep the legal set', 'W52', 'Publishes DPA, sub-processor list and legal documents', '30-day sub-processor notice; DPIA and EU AI Act assessment before EU launch', ['FR-V12-K-140', 'FR-V12-K-141', 'FR-V12-K-143']),
  ],
  model=[('jurisdiction', {'IN pack Approved': X, 'EU pack Approved': X, 'UK pack Draft': JURIS['UK pack Draft'],
                           'US pack Expired': (6, 'HOLD `PACK_EXPIRED`')}), ('consent', CONSENT), ('channel', P('email', 'SMS / voice', 'portal'))],
  outcome='only lawful actions run; every right and clock met with evidence')

journey(id='JN-08', persona='Platform operator', pid='P12', roles='R13 Platform Support; R14 Platform Billing; R11 release manager',
  goal='Operate the multi-region SaaS: catalogue, releases, recovery, incidents, security programme and support access, with 24×7 cover',
  pre='Stacks live in zone IN (Mumbai) and zone EU (DEC-772)',
  steps=[
   ('Acquire customers', 'A184', 'Runs SaaS acquisition from the operator tenant', 'Operator cannot read customer private records by default', ['FR-V12-A-073']),
   ('Run the catalogue', 'A192, A186', 'Moves a SKU from pilot to released', 'Readiness gate; alias map; drafts never public', ['US-29-YB12', 'FR-V12-A-004', 'FR-V12-E-045']),
   ('Gate a release', 'A190', 'Assembles GO-01…08 evidence', 'P0 controls block affected SKUs only', ['US-21-YE03', 'FR-V12-A-191', 'FR-V12-E-130']),
   ('Deploy per region', 'A190', 'Promotes the same digest to both zones', 'Pinned Vercel functions; header allowlist; no body logging (DEC-786)', ['US-21-ZR16', 'US-21-ZR17']),
   ('Prove recovery', 'A156', 'Runs the restore drill at the gate', 'RPO ≤ 15 min; growth RTO ≤ 120 min (DEC-771/787)', ['US-21-ZR18', 'US-21-ZR19', 'FR-V12-A-147']),
   ('Run incidents', 'A014, W45', 'Declares a SEV1 and publishes status', '24×7 on-call (DEC-773); independent status page', ['US-21-YK01', 'FR-V12-K-004', 'FR-V12-A-142']),
   ('Secure the SDLC', 'A190', 'Reviews SBOM and the pen-test report', 'SAST/DAST/SCA per change; remediation SLA clock', ['FR-V12-K-129', 'FR-V12-K-130', 'FR-V12-K-132']),
   ('Support a tenant', 'A099', 'Requests just-in-time access to a tenant', 'Ticket-linked, tenant-approved, time-limited, audited', ['FR-V12-K-111', 'US-01-ZR05']),
   ('Govern models', 'A198', 'Onboards a candidate model', 'Two-person approval with evidence; Claude Sonnet primary (DEC-788)', ['US-04-ZR20', 'US-04-ZR23']),
   ('Manage plugins', 'A188', 'Reviews the paid-plugin replacement register', 'Every candidate disabled until evidence', ['FR-V12-H-032']),
  ],
  model=[('region', REGION), ('evidence', {'evidence complete': X, 'evidence missing': (4, 'GATE BLOCKED `EVIDENCE_MISSING`')}),
         ('severity', P('SEV1', 'SEV3', 'no incident')), ('channel', P('C1 web desktop', 'pager / phone'))],
  outcome='release promoted in both zones with recovery and security evidence')

journey(id='JN-09', persona='Investor-relations user', pid='P21 (new, RECOMMENDATION-1141)', roles='R03 in the INV product; approvals by R02 + R10',
  goal='Run a compliant fundraising round from discovery to closing and investor updates in the Investment Automation product',
  pre='AppNAI subscribed to Investment Automation (separate product code); "Seed 2027" registered under IN s.42',
  steps=[
   ('Get access', 'A205', 'Signs in to the INV product', 'Separate product entitlement; foundation capabilities included', ['US-30-ZN01', 'FR-V12-O-002']),
   ('Discover funders', 'A207', 'Finds funding routes and investors with evidence', 'Evidence-backed discovery; signals monitored', ['US-30-ZN05', 'US-30-ZN06']),
   ('Screen eligibility', 'A209', 'Screens mandate fit and eligibility', 'Deterministic eligibility; explainable propensity', ['US-30-ZN07', 'US-30-ZN08']),
   ('Write to investors', 'A217', 'Drafts and sends investor emails', 'Securities communication guard; solicitation guard', ['US-30-ZN10', 'US-30-ZN11', 'FR-V12-N-021']),
   ('Answer questions', 'A219', 'Lets the assistant answer factual questions', 'No personalised investment advice by AI', ['US-31-ZN16', 'FR-V12-N-023', 'US-33-ZO15']),
   ('Meet', 'A221', 'Holds investor meetings', 'Recording only with consent', ['US-30-ZN17']),
   ('Open the data room', 'A225, W75', 'Opens gated diligence access', 'Gated, watermarked, fair disclosure', ['US-31-ZN06', 'US-31-ZN07']),
   ('Issue offers', 'A227', 'Issues formal offers', 'Caps per route; two-person approval; no mandate for securities actions', ['US-31-ZN09', 'FR-V12-N-026']),
   ('Track receipts', 'A229, A233', 'Tracks receipts and the allotment clock', 'Day-60 block and refund task (IN)', ['US-31-ZN12', 'FR-V12-O-014']),
   ('Close', 'A233, A234', 'Prepares the closing record and filings', 'Authorised closing; statutory deadlines', ['US-32-ZO01', 'US-32-ZO02', 'FR-V12-O-037']),
   ('Update investors', 'A235', 'Sends an investor update', 'Rights-scoped personalisation; figures tie out', ['US-32-ZO03', 'FR-V12-O-016']),
   ('Manage the pipeline', 'A237', 'Works the pipeline', 'Next actions respect solicitation mode', ['US-32-ZO05', 'FR-V12-O-018']),
  ],
  model=[('jurisdiction', {'IN s.42 pack Approved': X, 'US 506(c) pack Approved': X, 'UK FPO pack Draft': (6, 'HOLD `PACK_NOT_ACTIVE`')}),
         ('investor eligibility', {'verified eligible': X, 'unverified': (6, 'BLOCK `ELIGIBILITY_UNVERIFIED`')}),
         ('solicitation', {'pre-existing relationship': X, 'no relationship': (6, 'BLOCK `GENERAL_SOLICITATION`')}), ('region', REGION)],
  outcome='round closed lawfully with evidence for each investor and jurisdiction')

journey(id='JN-10', persona='Invited investor', pid='P22 (new, RECOMMENDATION-1141)', roles='R21 invited investor (Part 11.16a; see CONFLICT-1140)',
  goal='Review an invitation, complete verification, diligence, application and payment instructions, and follow holdings and governance, privately',
  pre='Priya Raman has a pre-existing relationship with AppNAI and receives a portal invitation',
  steps=[
   ('Accept the invitation', 'W77', 'Opens the private invitation', 'Object grants only; MFA; region-pinned', ['US-31-ZN06']),
   ('Ask privately', 'W82', 'Submits a signed private enquiry', 'Stored as enquiry only where the pack is inactive', ['US-32-ZO07', 'FR-V12-O-020']),
   ('Get verified', 'W76', 'Completes eligibility and KYC hand-off', 'Regulated provider; sanctions possible match held; no tip-off', ['US-31-ZN02', 'US-33-ZO11', 'FR-V12-O-036']),
   ('Do diligence', 'W75', 'Reviews the data room and asks questions', 'Watermarked; fair disclosure of answers', ['US-31-ZN06', 'US-31-ZN07']),
   ('Apply', 'W85, W86', 'Reads the offer letter and applies with e-signature', 'Offer within caps; two approvals behind it', ['US-32-ZO10', 'US-31-ZN10']),
   ('Pay', 'W87', 'Receives payment instructions', 'No custody by the platform; receipt evidence only', ['FR-V12-N-028', 'US-31-ZN12']),
   ('Cross-border check', 'W82', 'Is held for a cross-border review', 'Issuer IN, investor US → hold until reviewed', ['FR-V12-N-029', 'US-33-ZO07']),
   ('Follow holdings', 'W88, W90', 'Sees holdings and updates', 'Only items within rights', ['US-32-ZO10', 'US-32-ZO03']),
   ('Vote', 'W91', 'Attends a shareholder meeting and votes', 'Notice, quorum and voting rules', ['US-33-ZO09']),
   ('Exercise privacy rights', 'W35', 'Requests a copy of personal data', 'DSR in the investor\'s residency zone', ['US-30-ZN04']),
  ],
  model=[('investor eligibility', {'verified eligible': X, 'unverified': (6, 'BLOCK `ELIGIBILITY_UNVERIFIED`'), 'sanctions possible match': (5, 'HOLD for R10 review; no tip-off')}),
         ('jurisdiction', {'IN s.42 pack Approved': X, 'US 506(b) pack Approved': X, 'UK FPO pack Draft': (6, 'HOLD `PACK_NOT_ACTIVE`')}),
         ('channel', P('C1 web desktop', 'C2 mobile web')), ('region', REGION)],
  outcome='application accepted and holdings visible, privately and lawfully')

journey(id='JN-11', persona='External customer', pid='P14 (visitor P15 before sign-in)', roles='R18 Anonymous Visitor → R16 External Customer',
  goal='Evaluate the service on the neutral storefront, enquire, talk to the AI assistant or voice agent, request a quote, get support and give feedback',
  pre='Public snapshot published for en-IN; Sunrise Clinics is a prospect',
  steps=[
   ('Browse', 'W01–W05', 'Browses the neutral catalogue of 39 services', 'No customer data; published snapshot only', ['US-19-YA01', 'US-19-YG01', 'US-19-YG04']),
   ('See examples', 'W05, W08', 'Views fictional workflow output previews', 'Labelled synthetic and AI-disclosed', ['FR-V12-A-058', 'US-19-YG35']),
   ('Assess maturity', 'W11', 'Takes the maturity assessment', 'No mandatory personal data; reproducible score', ['FR-V12-A-060', 'US-19-YG37']),
   ('Consent to cookies', 'W30', 'Chooses cookie preferences', 'Notice version recorded; analytics only with consent', ['US-03-YG07', 'FR-V12-I-045']),
   ('Enquire', 'W12', 'Sends an enquiry', 'Accessible validation; consent captured', ['US-19-YG12', 'US-19-YG32']),
   ('Call the company', 'phone', 'Calls and is answered by the AI voice agent', 'AI self-identifies; human handoff on request', ['US-22-ZQ01', 'US-22-ZQ02', 'US-22-ZQ07']),
   ('Request a quote', 'W14', 'Requests a quotation', 'Quote request only; no checkout', ['US-20-YG17']),
   ('Sign in', 'W21, W22', 'Signs in to the portal', 'Own records only', ['US-19-YG21', 'US-19-YG22']),
   ('Get support', 'W28', 'Opens a support case', 'SLA clock from entitlement; grounded answers', ['US-27-YB01', 'US-27-YB03', 'US-20-YD01']),
   ('Self-help', 'W08', 'Reads help articles', 'Top 50 tasks per launch locale', ['FR-V12-A-144', 'US-20-YK06']),
   ('Manage preferences', 'W29', 'Opts out of SMS', 'STOP cancels queued messages', ['US-03-YG01', 'US-23-YB03']),
   ('Give feedback', 'W28', 'Answers CSAT', 'Missing response is not counted as satisfied', ['FR-V12-A-153', 'US-16-YI01']),
  ],
  model=[('channel', P('C1 web desktop', 'C2 mobile web 360 px', 'assistive technology', 'phone')), ('locale', P('en-IN', 'hi-IN', 'de-DE')),
         ('consent', CONSENT), ('region', REGION)],
  outcome='enquiry answered, quote requested and support resolved with consent respected')

journey(id='JN-12', persona='Partner', pid='P23 partner / reseller (new, RECOMMENDATION-1141); P17 agency operator', roles='R16 with partner grant; R21 agency operator per Part 2.6',
  goal='Join the partner programme, register and co-sell deals, interoperate through agents and marketplaces, and get settled, with separate consent and billing ownership',
  pre='AppNAI runs SM-SVC-32 partner co-selling; partner "Bluepeak Systems LLP" applies',
  steps=[
   ('Join the programme', 'A176', 'Signs the partner agreement', 'Separate tenant consent and billing ownership', ['US-16-YB03', 'FR-V12-K-157']),
   ('Get enabled', 'A176', 'Completes enablement', 'Training records; scoped assets', ['US-16-YD03']),
   ('Register a deal', 'A176', 'Registers a deal', 'Conflict check; owner approval', ['US-16-YD03', 'US-16-YG03']),
   ('Co-sell', 'A176', 'Shares account plans', 'Only data covered by the agreement', ['US-16-YG03']),
   ('Connect partner agents', 'A172', 'Connects the partner\'s AI agent for quotations', 'Verified agent identity; trust tier; untrusted content sanitised', ['US-24-ZP02', 'US-24-ZP03', 'US-24-YB07']),
   ('List on marketplaces', 'A175', 'Lists offerings on a marketplace', 'Approved price version only', ['US-25-YB01', 'US-25-YB02']),
   ('Supply', 'A183', 'Acts as a supplier in an RFQ', 'Qualification rules; approved PO; three-way match', ['US-26-YB01', 'US-26-YB03']),
   ('Integrate', 'A008', 'Syncs CRM records', 'Field ownership; protected consent', ['US-07-ZR12']),
   ('Run managed service', 'A099', 'Works inside a client tenant under delegation', 'Delegation grant; one client per session', ['US-20-YE16', 'FR-V12-K-157']),
   ('Get settled', 'A074', 'Receives commission settlement', 'Reconciled settlement', ['US-15-ZP02']),
  ],
  model=[('region', REGION), ('jurisdiction', JURIS), ('autonomy/mandate', AUTONOMY), ('channel', P('C1 web desktop', 'C3 API', 'agent-to-agent'))],
  outcome='deal co-sold and settled with partner data kept separate')
