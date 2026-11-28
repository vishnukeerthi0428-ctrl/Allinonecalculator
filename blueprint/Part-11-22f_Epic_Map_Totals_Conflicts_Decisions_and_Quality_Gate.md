# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 11 (Batch 11.22f), Epic Map, Story and Story-Point Totals, Conflicts, Decisions, Tags and Quality Gate

| Field | Value |
|---|---|
| Document | Part 11, Batch 22, file f of f: §11.22.5.6 epic map EP-01…EP-34 to stories and requirements, §11.22.5.7 totals per epic and per release, §11.22.6 conflicts, §11.22.7 decisions, §11.22.8 expert persona review, §11.22.9 tags register, §11.22.10 quality gate |
| Version | 1.0 · 28 Nov 2026 |
| Baseline | Parts 0–9.10; Parts 11.1–11.19 (V12 review and V12-B Founder decisions, Part 11.14 DEC-770…791); story template Part 5.1a (§5.2 DoR, §5.3 DoD, §5.5 estimation, §5.6 dimension matrix, §5.7 conventions) |
| Roles applied | Chief Product Officer · Principal Agile Product Owner · Business Systems Analyst (BDD/Gherkin) · UX researcher (persona journeys) · QA Lead (combinatorial design) |
| ID ranges used | DEC-940…959 · tags ASSUMPTION/GAP/CONFLICT/RECOMMENDATION-1140…1159 · ADR-275…279 · stories US-&lt;EP&gt;-ZU&lt;nn&gt; · AC-&lt;EP&gt;ZU&lt;nn&gt;-&lt;seq&gt; · example rows EX-&lt;EP&gt;ZU&lt;nn&gt;-&lt;seq&gt; · parameter models MU01…MU13 · journeys JN-01…JN-12 · new epic EP-34 · new personas P21–P23 |

**Acronyms used in this part.** AC = acceptance criterion · BDD = behaviour-driven development · CPO = Chief Product Officer · DoD / DoR = Definition of Done / Ready · EX = generated example row · FR = functional requirement · INV = Investment Automation product · MAS = minimum AC set (Part 5.1a §5.6.6) · NSE = no side effect · PDP = Policy Decision Point · PSP = payment service provider · RLS = row-level security · SKU = stock-keeping unit (a sellable service, SM-SVC-01…39 or INV-SVC-01…24) · SoD = separation of duties · SP = story point · t-way = covering array in which every combination of any t parameter values appears in at least one row.

### 11.22.5.6 Epic map: EP-01…EP-34 to stories and requirements

| Epic | Title | Defined in | Baseline stories (Part 5 / enhancement / advanced) | V12 stories (Parts 11.1–11.19) | New ZU stories (this part) | FR-V12 requirements mapped |
|---|---|---|---|---|---|---|
| EP-01 | Platform foundation, identity reuse and tenancy | Part 0 §0.10.2 | 35 (17 / 16 / 2) | 36: US-01-YA01; US-01-YE01…10; US-01-YG01…06; US-01-YH01…08; US-01-YI01…03; US-01-ZR01…05, 26…28 | 14: US-01-ZU01…14 | 115: A: 006, 070–072, 074, 125; E: 001–005, 010–021; G: 067, 073, 082–083, 086, 103; H: 001–003, 005–007, 016, 018, 022–023, 035–038; I: 001–005, 008–011, 013, 017–018, 025–026, 030–031; K: 101–111, 120–121; R: 001–030, 143–155 |
| EP-02 | Product truth and knowledge | Part 0 §0.10.2 | 10 (8 / 1 / 1) | 5: US-02-YA01; US-02-YB01; US-02-YD01; US-02-YM19…20 | 2: US-02-ZU01…02 | 13: A: 075–077, 079; B: 059; D: 125; F: 031; M: 059–064 |
| EP-03 | Consent, privacy, eligibility and compliance | Part 0 §0.10.2 | 17 (11 / 3 / 3) | 17: US-03-YA01…02; US-03-YE01; US-03-YF27; US-03-YG01…07; US-03-YH01; US-03-YI01…02; US-03-YM09…10, 38 | 8: US-03-ZU01…08 | 41: A: 053, 130–135; E: 022, 126; F: 042–044, 046–047; G: 029, 070–072, 075, 081, 096; H: 013, 033; I: 006–007, 014; K: 140–144; M: 027–033, 100; P: 069, 133 |
| EP-04 | AI gateway, cost control and AI quality | Part 0 §0.10.2 | 29 (8 / 10 / 11) | 22: US-04-YA01; US-04-YF24…26, 29; US-04-YG01…04; US-04-YH01; US-04-YI01; US-04-YK08; US-04-YL06; US-04-YM27…28, 33…34, 37; US-04-ZR20…23 | 17: US-04-ZU01…17 | 93: A: 032–033, 054, 111, 113–118; F: 001–030, 032–033, 036–039, 049–050; G: 068–069, 079–080; H: 012, 017; I: 007, 016; K: 010; L: 021–026; M: 081–085, 093–096, 099; R: 111–130 |
| EP-05 | Market intelligence and discovery | Part 0 §0.10.2 | 21 (12 / 6 / 3) | 8: US-05-YB01…02; US-05-YC01…02; US-05-YM01…02, 31…32 | 1: US-05-ZU01 | 22: A: 078; B: 031–034; C: 013–020; M: 001–006, 090–092 |
| EP-06 | Opportunity scoring, contacts and research review | Part 0 §0.10.2 | 14 (8 / 1 / 5) | 7: US-06-YB01…03; US-06-YC03…04; US-06-YD01; US-06-YG01 | 0: — | 13: B: 035–036, 078; C: 021–028; D: 129; G: 043 |
| EP-07 | CRM, lead capture and Customer 360 | Part 0 §0.10.2 | 15 (10 / 0 / 5) | 5: US-07-YB01; US-07-YC05; US-07-YG01; US-07-ZR12…13 | 0: — | 13: B: 037; C: 029–032; G: 039; R: 063–069 |
| EP-08 | Messaging: drafting, email, inbound, sequences, omnichannel | Part 0 §0.10.2 | 23 (15 / 5 / 3) | 19: US-08-YB01…04; US-08-YC06, 08…09; US-08-YD01…02; US-08-YF01, 11, 21; US-08-YG01…02; US-08-YM03…04; US-08-ZQ01…03 | 2: US-08-ZU01…02 | 51: A: 077, 133; B: 038, 040–041, 094; C: 033–036, 041–048; D: 126, 138; F: 045, 051, 061, 071; G: 040, 052; H: 024–025; M: 007–013; Q: 020–027, 040–046, 048 |
| EP-09 | Meetings, webinars and demos | Part 0 §0.10.2 | 12 (6 / 4 / 2) | 4: US-09-YB01…02; US-09-YC10, 16 | 0: — | 10: B: 042, 049; C: 049–052, 073–076 |
| EP-10 | WhatsApp and website assistant | Part 0 §0.10.2 | 8 (7 / 0 / 1) | 3: US-10-YB01; US-10-YC07; US-10-YF22 | 0: — | 6: B: 039; C: 037–040; F: 072 |
| EP-11 | Content, SEO and social publishing | Part 0 §0.10.2 | 15 (10 / 1 / 4) | 18: US-11-YB01…04; US-11-YC11…13; US-11-YD01…02; US-11-YF03…04, 08…09, 19…20; US-11-YG01…02; US-11-YM35 | 0: — | 28: B: 043–045, 092–093; C: 053–064; D: 127, 135; F: 053–054, 058–059, 069–070; G: 041, 049; M: 097 |
| EP-12 | Campaigns, landing pages, ads and referrals | Part 0 §0.10.2 | 21 (10 / 3 / 8) | 13: US-12-YB01…03; US-12-YC14…15; US-12-YD01; US-12-YF02; US-12-YG01; US-12-YI01; US-12-YM15…16, 29…30 | 1: US-12-ZU01 | 29: A: 052; B: 046–048, 079–080; C: 065–072; D: 130; F: 052; G: 044; I: 045–046; M: 048–053, 086–089 |
| EP-13 | Proposal, quote, negotiation and contract | Part 0 §0.10.2 | 17 (13 / 0 / 4) | 13: US-13-YB01…03; US-13-YC17…18; US-13-YD01…02; US-13-YF05, 18; US-13-YG01…04 | 0: — | 21: B: 050–051, 095–097; C: 077–084; D: 128, 137; F: 055, 068; G: 023–024, 042, 051 |
| EP-14 | Bids, orders and fulfilment (vertical routes) | Part 0 §0.10.2 | 18 (12 / 3 / 3) | 18: US-14-YB01…02; US-14-YC19…20; US-14-YD01…02; US-14-YF12…13, 16; US-14-YG01…03; US-14-YM17…18; US-14-ZP01…04 | 0: — | 119: B: 052–054; C: 085–092; D: 131, 139; F: 062–063, 066; G: 025, 045, 053; M: 054–058; P: 001–006, 008, 012–015, 019–023, 027–029, 031–033, 036–040, 052–053, 058–059, 061–062, 064–065, 067–099, 110–135, 150 |
| EP-15 | Payment, closure, revenue and attribution | Part 0 §0.10.2 | 14 (11 / 2 / 1) | 13: US-15-YB01…02; US-15-YD01; US-15-YE01; US-15-YF10, 17; US-15-YG01; US-15-YI01; US-15-YM11…12; US-15-ZP01…03 | 1: US-15-ZU01 | 114: A: 036; B: 055, 058; D: 121; E: 079–082; F: 060, 067; G: 026; I: 042; M: 034–040; P: 001–006, 008, 012–015, 019–023, 027–029, 031–033, 036–040, 052–053, 058–059, 061–062, 064–065, 067–099, 110–135, 150 |
| EP-16 | Onboarding, retention, partners and expansion pilots | Part 0 §0.10.2 | 23 (12 / 3 / 8) | 19: US-16-YA01…02; US-16-YB01…04; US-16-YD01…03; US-16-YF06, 14…15, 23; US-16-YG01…05; US-16-YI01 | 6: US-16-ZU01…06 | 32: A: 020, 153, 160–167, 169–170; B: 056–057, 085, 090–091; D: 122–123, 132; F: 056, 064–065, 073; G: 027–028, 046–048; I: 047; K: 156–157 |
| EP-17 | Dashboards, forecast and Command Centre | Part 0 §0.10.2 | 36 (10 / 13 / 13) | 18: US-17-YA01…02; US-17-YD01; US-17-YG01…08; US-17-YI01…02; US-17-YM21…22, 36; US-17-ZR24…25 | 5: US-17-ZU01…05 | 55: A: 036, 072, 120–125, 152; D: 124; G: 050, 091, 094, 100–101, 109–110, 115; H: 015; I: 040, 043–044; M: 065–069, 098; P: 068, 130; R: 131–155 |
| EP-18 | Workflow, autonomy and automation engine | Part 0 §0.10.2 | 26 (15 / 8 / 3) | 43: US-18-YA01; US-18-YC21…22; US-18-YD01…10; US-18-YE01…02; US-18-YF28; US-18-YG01…07; US-18-YH01; US-18-YI01…02; US-18-YL01, 04; US-18-YM05…07, 26; US-18-ZP01…10; US-18-ZR11 | 14: US-18-ZU01…14 | 234: A: 002, 110–112; C: 001–012; D: 001–028; E: 039, 046, 060–061, 095–101, 106; F: 034–035, 040–041, 048; G: 062–065, 090, 111, 116; H: 011, 019–021, 026–027; I: 015, 023; K: 124–127; L: 001–015, 017–020; M: 014–026, 079–080; P: 001–006, 008, 012–015, 019–023, 027–029, 031–033, 036–040, 052–053, 058–059, 061–062, 064–065, 067–099, 110–135, 150; R: 056–080 |
| EP-19 | Public website and external portal | Part 0 §0.10.2 | 25 (13 / 7 / 5) | 43: US-19-YA01…03; US-19-YG01…38; US-19-YK10; US-19-YL02 | 5: US-19-ZU01…05 | 59: A: 050–061, 144, 222; E: 051; G: 001–022, 030, 035–038, 077, 092–093, 095, 097–099, 106–108, 117; I: 059; K: 009; L: 002, 012, 014; M: 021 |
| EP-20 | SaaS client lifecycle and portability | Part 0 §0.10.2 | 33 (12 / 15 / 6) | 64: US-20-YA01…08; US-20-YD01…02; US-20-YE01…16; US-20-YF07; US-20-YG01…20; US-20-YH01; US-20-YI01…03; US-20-YK03…06; US-20-YL03; US-20-YM23…25; US-20-ZR06…10 | 37: US-20-ZU01…37 | 212: A: 001–005, 010–024, 030–035, 055–057, 071, 073, 080, 090–097, 120, 134, 140, 143, 145–146, 168, 180–189, 192, 202; D: 133–134; E: 030–038, 040, 045–051, 055–065, 070–078, 083–089, 121, 127; F: 057; G: 031–034, 054–059, 061, 074, 084–085, 089, 104–105, 112–114; H: 001–010, 014, 028–030, 034, 039–040; I: 019–022, 024; K: 001–002, 005–006, 012, 014, 112–119, 122–123, 153–155, 158; L: 015–020; M: 070–080; R: 031–055 |
| EP-21 | Release readiness, QA and observability | Part 0 §0.10.2 | 49 (10 / 34 / 5) | 40: US-21-YA01…03; US-21-YD01; US-21-YE01…04; US-21-YG01…07; US-21-YH01; US-21-YI01…03; US-21-YJ01…05; US-21-YK01…02, 07, 09, 11…12; US-21-YL05, 07; US-21-YM08, 13…14; US-21-ZR16…19, 29 | 22: US-21-ZU01…22 | 144: A: 140–143, 147, 150–152, 190–191, 200–202, 210, 220–221; D: 136; E: 082, 088, 102–103, 105–116, 120–126, 130–135; G: 060, 066, 076, 078, 087–088, 102; H: 031–032, 041; I: 012, 041, 050–058; J: 001–006; K: 003–004, 007–008, 011, 013, 015, 020–023, 025–026, 128–136; L: 027–030; M: 022–025, 041–047; R: 027, 078, 081–110, 124, 137 |
| EP-22 | Voice and intelligent telephony | Part 11.2a | 0 (0 / 0 / 0) | 22: US-22-YB01…06; US-22-ZQ01…15; US-22-ZR15 | 0: — | 65: B: 060–065; Q: 001–055; R: 075–078 |
| EP-23 | SMS, RCS and business messaging | Part 11.2a | 0 (0 / 0 / 0) | 5: US-23-YB01…04; US-23-ZR14 | 0: — | 9: B: 098–101; R: 070–074 |
| EP-24 | Agentic commerce and AI-to-AI transactions | Part 11.2a | 0 (0 / 0 / 0) | 12: US-24-YB01…07; US-24-ZP01…05 | 0: — | 102: B: 071–077; P: 001–006, 008, 012–015, 019–023, 027–029, 031–033, 036–040, 052–053, 058–059, 061–062, 064–065, 067–099, 110–135, 150 |
| EP-25 | Marketplace and e-commerce channel operations | Part 11.2a | 0 (0 / 0 / 0) | 4: US-25-YB01…04 | 0: — | 4: B: 081–084 |
| EP-26 | Procurement and supplier management | Part 11.2a | 0 (0 / 0 / 0) | 4: US-26-YB01…04 | 0: — | 4: B: 102–105 |
| EP-27 | Customer service and support operations | Part 11.2a | 0 (0 / 0 / 0) | 4: US-27-YB01…04 | 0: — | 4: B: 086–089 |
| EP-28 | Multimodal creative production | Part 11.2a | 0 (0 / 0 / 0) | 5: US-28-YB01…05 | 0: — | 5: B: 066–070 |
| EP-29 | Automation service catalogue, SKU entitlement and metering | Part 11.2a | 0 (0 / 0 / 0) | 12: US-29-YB01…12 | 0: — | 30: B: 001–030 |
| EP-30 | Investment Automation I: platform, investor-mode website, discovery and engagement | Part 11.16e | 0 (0 / 0 / 0) | 18: US-30-ZN01…18 | 1: US-30-ZU01 | 88: N: 001–019, 021, 023, 031–049, 101–148 |
| EP-31 | Investment Automation II-a: diligence, offers, applications and receipts | Part 11.16e | 0 (0 / 0 / 0) | 16: US-31-ZN01…16 | 1: US-31-ZU01 | 40: N: 015–016, 020, 022, 024–030, 050–062, 133–148 |
| EP-32 | Investment Closing, Investor Lifecycle and Engagement Operations | Part 11.16d | 0 (0 / 0 / 0) | 10: US-32-ZO01…10 | 9: US-32-ZU01…09 | 36: O: 001–020, 037–052 |
| EP-33 | Specialised Funding, Ownership, Governance, Verification and Securities Compliance | Part 11.16d | 0 (0 / 0 / 0) | 15: US-33-ZO01…15 | 16: US-33-ZU01…16 | 65: O: 003–012, 021–036, 053–091 |
| EP-34 | Global expansion, certification and multi-market operations (new, DEC-942) | this part | 0 (0 / 0 / 0) | 0: — | 4: US-34-ZU01…04 | 11: K: 137–139, 145–152 |

**FR-to-epic rule.** An FR maps to the epic in its register row, to the epic of every story that traces it, and to the epic of its new ZU story; an FR can therefore appear under more than one epic. Every one of the 1467 FR-V12 requirements maps to at least one epic: yes.

#### 11.22.5.6.1 Story-level map (V12 and new stories)

| Story | Epic | Title / statement (abridged) | FR-V12 traced | AC | Release | SP | Source |
|---|---|---|---|---|---|---|---|
| US-01-YA01 | EP-01 | As the Founder, I want each owned company to be its own tenant and to see portfolio… | A: 070–072, 074, 125 | Yes | Release 1 | 13 | Part-11-1b |
| US-01-YE01 | EP-01 | As a tenant administrator I want to add an organization and companies under my tenant so… | E: 001–002 | Yes | Not stated | not stated | Part-11-5b |
| US-01-YE02 | EP-01 | As a tenant administrator I want to grant another tenant aggregate-only portfolio access… | E: 003 | Yes | Not stated | not stated | Part-11-5b |
| US-01-YE03 | EP-01 | As a tenant administrator I want to connect my SAML or OIDC IdP so that staff sign in… | E: 010, 015 | Yes | Not stated | not stated | Part-11-5b |
| US-01-YE04 | EP-01 | As a tenant administrator I want to verify my email domain so that SSO can be enforced… | E: 011 | Yes | Not stated | not stated | Part-11-5b |
| US-01-YE05 | EP-01 | As an IT administrator I want SCIM de-provisioning so that leavers lose access quickly | E: 012 | Yes | Not stated | not stated | Part-11-5b |
| US-01-YE06 | EP-01 | As a tenant administrator I want to set MFA and session policy within platform bounds | E: 013–014 | Yes | Not stated | not stated | Part-11-5b |
| US-01-YE07 | EP-01 | As a tenant administrator I want custom roles that cannot break separation of duties | E: 016–017 | Yes | Not stated | not stated | Part-11-5b |
| US-01-YE08 | EP-01 | As an auditor I want to export and verify the audit trail and stream it to our SIEM | E: 018–019 | Yes | Not stated | not stated | Part-11-5b |
| US-01-YE09 | EP-01 | As the platform I want job-scoped service-principal grants so that workers never inherit… | E: 021 | No → US-01-ZU03 | Not stated | not stated | Part-11-5b |
| US-01-YE10 | EP-01 | As a tenant I want region-pinned data and pooled-connection safety | E: 004–005, 020 | No → US-01-ZU02 | Not stated | not stated | Part-11-5b |
| US-01-YG01 | EP-01 | As the tenant administrator (R12), I want A197 Business and Organization Management… | G: 067 | Yes | Not stated | not stated | Part-11-7c |
| US-01-YG02 | EP-01 | As the tenant administrator (R12), I want A203 Identity, SSO | G: 073 | Yes | Not stated | not stated | Part-11-7c |
| US-01-YG03 | EP-01 | As the tenant administrator (R12), I want A002 User and role administration: V12 A123… | G: 082 | Yes | Not stated | not stated | Part-11-7c |
| US-01-YG04 | EP-01 | As the tenant administrator (R12), I want A009 Audit and job activity: V12 A124 delta so… | G: 083 | Yes | Not stated | not stated | Part-11-7c |
| US-01-YG05 | EP-01 | As the tenant administrator (R12), I want A008 Integration connections: V12 A128 delta so… | G: 086 | Yes | Not stated | not stated | Part-11-7c |
| US-01-YG06 | EP-01 | As the tenant administrator (R12), I want Four access experiences (Platform operator | G: 103 | Yes | Not stated | not stated | Part-11-7c |
| US-01-YH01 | EP-01 | As a tenant administrator I want scoped, expiring API keys shown once so that our servers… | H: 001, 003 | Yes | Release 1 | not stated | Part-11-8b |
| US-01-YH02 | EP-01 | As an integration developer I want OAuth client credentials so that server tokens are… | H: 002 | No →  | Release 2 | not stated | Part-11-8b |
| US-01-YH03 | EP-01 | As a tenant administrator I want signed outbound webhooks with a delivery log and replay… | H: 005, 035 | Yes | Release 1 | not stated | Part-11-8b |
| US-01-YH04 | EP-01 | As a developer I want a portal with reference, guides and a sandbox so that I can build… | H: 006–007 | No →  | Release 2 | not stated | Part-11-8b |
| US-01-YH05 | EP-01 | As a tenant administrator I want SAML/OIDC SSO with verified domains and break-glass so… | H: 036 | Yes | Release 1 | not stated | Part-11-8b |
| US-01-YH06 | EP-01 | As an IT administrator I want SCIM provisioning so that leavers lose access within 15… | H: 036 | Yes | Release 2 | not stated | Part-11-8b |
| US-01-YH07 | EP-01 | As a tenant administrator I want custom roles that cannot combine request and approve so… | H: 037 | Yes | Release 2 | not stated | Part-11-8b |
| US-01-YH08 | EP-01 | As an automation lead I want to install connectors behind an activation gate so that no… | H: 018, 022–023 | Yes | Release 1 | not stated | Part-11-8b |
| US-01-YI01 | EP-01 | As the platform security lead I want application roles that cannot bypass RLS and a… | I: 002 | Yes | Not stated | not stated | Part-11-9b |
| US-01-YI02 | EP-01 | As an Owner Portfolio executive I want to read several companies but write only in one… | I: 003 | Yes | Not stated | not stated | Part-11-9b |
| US-01-YI03 | EP-01 | As a tenant administrator I want brands, offerings and markets bound to my company so… | I: 010 | Yes | Not stated | not stated | Part-11-9b |
| US-01-ZR01 | EP-01 | Tenant SSO connection with SAML 2.0 and OIDC through the broker | E: 010–015; H: 036; R: 001–016, 028–029 | Yes | Release 1 | 8–13 | Part-11-19c |
| US-01-ZR02 | EP-01 | Verified domains, enforcement, break-glass, MFA and session policy | E: 010–015; H: 036; R: 001–016, 030 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-01-ZR03 | EP-01 | SCIM 2.0 provisioning and de-provisioning in Release 1 | E: 010–015; H: 036; R: 001–026, 030 | Yes | Release 1 | 8–13 | Part-11-19c |
| US-01-ZR04 | EP-01 | Custom roles and separation of duties | E: 016–020; H: 037; R: 011–030 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-01-ZR05 | EP-01 | SIEM streaming, audit export, JIT support and quarterly recertification | E: 016–020; H: 037; R: 011–030 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-01-ZR26 | EP-01 | Least-privilege database role app_rw with per-transaction context | R: 143–155 | Yes | Release 1 | 3–5 | Part-11-19c |
| US-01-ZR27 | EP-01 | Data API disabled and service_role only through break-glass | R: 143–155 | Yes | Release 1 | 2–3 | Part-11-19c |
| US-01-ZR28 | EP-01 | Residency choice at onboarding and region routing | R: 005 | Yes | Release 1 | 3–5 | Part-11-19c |
| US-02-YA01 | EP-02 | As a tenant admin, I want divisions, brands, markets and channel accounts with separate… | A: 075–077, 079 | No → US-02-ZU01 | Release 1 | 8 | Part-11-1b |
| US-02-YB01 | EP-02 | SM-SVC-25 Business Document & Knowledge Intelligence Automation: V12 SKU deltas | B: 059 | Yes | Release 3+ | not stated | Part-11-2a |
| US-02-YD01 | EP-02 | As Compliance (R10), I want document intake, grounding | D: 125 | Yes | Not stated | 5–8 | Part-11-4d |
| US-02-YM19 | EP-02 | As a Research Analyst I want relations extracted with provenance so that I can trust the… | M: 059–064 | Yes | Release 3+ | not stated | Part-11-13b |
| US-02-YM20 | EP-02 | As a seller I want warm-path queries so that I reach buying committees through known… | M: 059–064 | Yes | Release 3+ | not stated | Part-11-13b |
| US-03-YA01 | EP-03 | As legal, I want a market pack to block outbound until counsel approves it | A: 053, 130–135 | Yes | Release 1 | 5 | Part-11-1b |
| US-03-YA02 | EP-03 | As a data principal, I want to lodge grievance and nomination requests and receive a due… | A: 053, 130–135 | No →  | Release 1 | 3 | Part-11-1b |
| US-03-YE01 | EP-03 | As a compliance lead I want deny reasons ordered by V12 precedence | E: 022 | No → US-03-ZU01 | Not stated | not stated | Part-11-5b |
| US-03-YF27 | EP-03 |  | F: 043 | Yes | Not stated | not stated | Part-11-6b |
| US-03-YG01 | EP-03 | As the DPO (R10), I want W29 repurposed as 'Communication preferences' | G: 029 | Yes | Not stated | not stated | Part-11-7c |
| US-03-YG02 | EP-03 | As the DPO (R10), I want A200 Jurisdiction policy packs and send preflight | G: 070 | Yes | Not stated | not stated | Part-11-7c |
| US-03-YG03 | EP-03 | As the DPO (R10), I want A201 Consent and suppression ledger | G: 071 | Yes | Not stated | not stated | Part-11-7c |
| US-03-YG04 | EP-03 | As the DPO (R10), I want A202 Breach and incident notification register | G: 072 | Yes | Not stated | not stated | Part-11-7c |
| US-03-YG05 | EP-03 | As the DPO (R10), I want W49 Rights request tracker: V12 W35 delta so that the V12… | G: 075 | Yes | Not stated | not stated | Part-11-7c |
| US-03-YG06 | EP-03 | As the DPO (R10), I want A163 Rights Case Console (with A013 Privacy request queue): V12… | G: 081 | Yes | Not stated | not stated | Part-11-7c |
| US-03-YG07 | EP-03 | As the DPO (R10), I want Cookie consent banner and preferences with notice version | G: 096 | Yes | Not stated | not stated | Part-11-7c |
| US-03-YH01 | EP-03 | As a DPO I want to record withdrawals, open incidents with clocks and record… | H: 013 | No → US-03-ZU04 | Release 1 | not stated | Part-11-8b |
| US-03-YI01 | EP-03 | As the DPO I want breach deadlines validated when notifications are planned so that… | I: 014 | Yes | Not stated | not stated | Part-11-9b |
| US-03-YI02 | EP-03 | As the DPO I want DSAR completion blocked until identity is verified and evidence attached | I: 006–007 | Yes | Not stated | not stated | Part-11-9b |
| US-03-YM09 | EP-03 | As Legal/Compliance I want rule packs versioned and signed off so that AI checks cite… | M: 027–033 | Yes | Release 3+ | not stated | Part-11-13b |
| US-03-YM10 | EP-03 | As a marketer I want clause-level findings and commitment flags before approval so that I… | M: 027–033 | Yes | Release 3+ | not stated | Part-11-13b |
| US-03-YM38 | EP-03 | As a recipient or user I want AI assistance disclosed so that I know where AI was used | M: 100 | No → US-03-ZU08 | Release 3+ | not stated | Part-11-13b |
| US-04-YA01 | EP-04 | As the AI owner, I want AI labels, region pinning and language slice gates before a… | A: 054, 111, 114–117 | No → US-04-ZU01, US-04-ZU03 | Release 1 | 5 | Part-11-1b |
| US-04-YF24 | EP-04 |  | F: 003 | Yes | Not stated | not stated | Part-11-6b |
| US-04-YF25 | EP-04 |  | F: 005 | Yes | Not stated | not stated | Part-11-6b |
| US-04-YF26 | EP-04 |  | F: 050 | Yes | Not stated | not stated | Part-11-6b |
| US-04-YF29 | EP-04 |  | F: 016 | Yes | Not stated | not stated | Part-11-6b |
| US-04-YG01 | EP-04 | As the AI lead (R11), I want A198 AI model registry and routing | G: 068 | Yes | Not stated | not stated | Part-11-7c |
| US-04-YG02 | EP-04 | As the AI lead (R11), I want A199 Prompt-injection defence and red-team | G: 069 | Yes | Not stated | not stated | Part-11-7c |
| US-04-YG03 | EP-04 | As the AI lead (R11), I want A128 AI Evaluation, Red-Team and Drift Observatory: V12 A115… | G: 079 | Yes | Not stated | not stated | Part-11-7c |
| US-04-YG04 | EP-04 | As the AI lead (R11), I want A012 API cost and budget dashboard: V12 A117 delta so that… | G: 080 | Yes | Not stated | not stated | Part-11-7c |
| US-04-YH01 | EP-04 | As an AI lead I want model promotion to require passing suites and a kill switch… | H: 012 | Yes | Release 1 | not stated | Part-11-8b |
| US-04-YI01 | EP-04 | As the AI governance lead I want every AI step to record model and prompt version and… | I: 007 | Yes | Not stated | not stated | Part-11-9b |
| US-04-YK08 | EP-04 | Robust AI cost anomaly hold | K: 010 | Yes | Not stated | not stated | Part-11-11b |
| US-04-YL06 | EP-04 | As the FinOps lead, I want every paid candidate benchmarked against the native baseline… | L: 021–026 | Yes | Not stated | 5 | Part-11-12 |
| US-04-YM27 | EP-04 | As the AI lead I want prompt candidates proposed from failures so that quality improves… | M: 081–085 | Yes | Release 3+ | not stated | Part-11-13b |
| US-04-YM28 | EP-04 | As the AI lead I want candidates proven offline and canaried so that no regression… | M: 081–085 | Yes | Release 3+ | not stated | Part-11-13b |
| US-04-YM33 | EP-04 | As the security lead I want abnormal agent tool use quarantined so that injection or… | M: 093–094 | Yes | Release 3+ | not stated | Part-11-13b |
| US-04-YM34 | EP-04 | As the security lead I want agents blocked when the firewall is down or unprofiled so… | M: 095–096 | Yes | Release 3+ | not stated | Part-11-13b |
| US-04-YM37 | EP-04 | As the FinOps lead I want all new agents metered to a capped budget line so that spend… | M: 099 | No → US-04-ZU17 | Release 3+ | not stated | Part-11-13b |
| US-04-ZR20 | EP-04 | Model registry data model and two-person approval | F: 002–003, 037–038; R: 111–130 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-04-ZR21 | EP-04 | Approval evidence, multimodal rows and re-certification | F: 002–003, 037–038; R: 111–130 | Yes | Release 1 | 3–5 | Part-11-19c |
| US-04-ZR22 | EP-04 | Zone- and class-aware routing through the registry | F: 002–003, 037–038; R: 111–130 | Yes | Release 1 | 8–13 | Part-11-19c |
| US-04-ZR23 | EP-04 | Claude Sonnet primary record, advanced tier and candidate onboarding | F: 002–003, 037–038; R: 111–130 | Yes | Release 1 | 3–5 | Part-11-19c |
| US-05-YB01 | EP-05 | SM-SVC-01 Market & Competitive Intelligence Automation: V12 SKU deltas | B: 031–032 | Yes | Release 3+ | not stated | Part-11-2a |
| US-05-YB02 | EP-05 | SM-SVC-02 Global Business Opportunity Discovery Automation: V12 SKU deltas | B: 033–034 | Yes | Release 3+ | not stated | Part-11-2a |
| US-05-YC01 | EP-05 | Market & Competitive Intelligence Automation | C: 013–016 | Yes | Not stated | not stated | Part-11-3b |
| US-05-YC02 | EP-05 | Global Business Opportunity Discovery Automation | C: 017–020 | Yes | Not stated | not stated | Part-11-3b |
| US-05-YM01 | EP-05 | As a Research Analyst I want to run a broad question as a swarm so that I get an answer… | M: 001–006 | Yes | Release 3+ | not stated | Part-11-13b |
| US-05-YM02 | EP-05 | As a Research Analyst I want each claim independently verified so that I do not pass on… | M: 001–006 | Yes | Release 3+ | not stated | Part-11-13b |
| US-05-YM31 | EP-05 | As an Automation Lead I want signals routed to the right services through an approved… | M: 090 | Yes | Release 3+ | not stated | Part-11-13b |
| US-05-YM32 | EP-05 | As an account owner I want contact pressure limited across services and sales held during… | M: 091–092 | Yes | Release 3+ | not stated | Part-11-13b |
| US-06-YB01 | EP-06 | SM-SVC-03 B2B Contact & Decision-Maker Intelligence Automation: V12 SKU deltas | B: 035 | Yes | Release 3+ | not stated | Part-11-2a |
| US-06-YB02 | EP-06 | SM-SVC-04 Lead Qualification & Intelligent Matching Automation: V12 SKU deltas | B: 036 | Yes | Release 3+ | not stated | Part-11-2a |
| US-06-YB03 | EP-06 | SM-SVC-29 Account-Based Marketing & Enterprise Buying Group Automation: V12 SKU deltas | B: 078 | Yes | Release 3+ | not stated | Part-11-2a |
| US-06-YC03 | EP-06 | B2B Contact & Decision-Maker Intelligence Automation | C: 021–024 | Yes | Not stated | not stated | Part-11-3b |
| US-06-YC04 | EP-06 | Lead Qualification & Intelligent Matching Automation | C: 025–028 | Yes | Not stated | not stated | Part-11-3b |
| US-06-YD01 | EP-06 | As a Growth Manager, I want account selection, buying-group maps and coordinated plays… | D: 129 | Yes | Not stated | 5–8 | Part-11-4d |
| US-06-YG01 | EP-06 | As a permitted user, I want A173 Account-Based Marketing & Enterprise Buying Group… | G: 043 | Yes | Not stated | not stated | Part-11-7c |
| US-07-YB01 | EP-07 | SM-SVC-05 CRM & Sales Pipeline Automation: V12 SKU deltas | B: 037 | Yes | Release 3+ | not stated | Part-11-2a |
| US-07-YC05 | EP-07 | CRM & Sales Pipeline Automation | C: 029–032 | Yes | Not stated | not stated | Part-11-3b |
| US-07-YG01 | EP-07 | As a visitor on a tenant-owned site (R18), I want W54 Embedded tenant-owned intake form | G: 039 | Yes | Not stated | not stated | Part-11-7c |
| US-07-ZR12 | EP-07 | CRM bi-directional sync with Salesforce, HubSpot and Zoho CRM | R: 063, 066–069 | Yes | Release 1 | 8–13 | Part-11-19c |
| US-07-ZR13 | EP-07 | CRM field ownership, conflicts and protected consent | R: 064–065 | Yes | Release 1 | 3–5 | Part-11-19c |
| US-08-YB01 | EP-08 | SM-SVC-06 Email Marketing & Outreach Automation: V12 SKU deltas | B: 038 | Yes | Release 3+ | not stated | Part-11-2a |
| US-08-YB02 | EP-08 | SM-SVC-08 Omnichannel Follow-up & Lead Nurturing Automation: V12 SKU deltas | B: 040 | Yes | Release 3+ | not stated | Part-11-2a |
| US-08-YB03 | EP-08 | SM-SVC-09 AI Chat, Unified Inbox & Objection Automation: V12 SKU deltas | B: 041 | Yes | Release 3+ | not stated | Part-11-2a |
| US-08-YB04 | EP-08 | SM-SVC-36 AI Sales Enablement & Coaching Automation: V12 SKU deltas | B: 094 | Yes | Release 3+ | not stated | Part-11-2a |
| US-08-YC06 | EP-08 | Email Marketing & Outreach Automation | C: 033–036 | Yes | Not stated | not stated | Part-11-3b |
| US-08-YC08 | EP-08 | Omnichannel Follow-up & Lead Nurturing Automation | C: 041–044 | Yes | Not stated | not stated | Part-11-3b |
| US-08-YC09 | EP-08 | AI Chat, Unified Inbox & Objection Automation | C: 045–048 | Yes | Not stated | not stated | Part-11-3b |
| US-08-YD01 | EP-08 | As the Founder (R01), I want SVC-26 fully specified but disabled | D: 126 | Yes | Not stated | 1–2 | Part-11-4d |
| US-08-YD02 | EP-08 | As a Marketing Lead, I want DLT-compliant SMS/RCS campaigns with STOP handling from… | D: 138 | Yes | Not stated | 8–13 | Part-11-4d |
| US-08-YF01 | EP-08 | Inbound Voice Enquiry Router (AG-100, AGT-20) | F: 051 | Yes | Not stated | not stated | Part-11-6b |
| US-08-YF11 | EP-08 | SMS and RCS Inbound Triage and Fallback Planner (AG-110, AGT-20) | F: 061 | Yes | Not stated | not stated | Part-11-6b |
| US-08-YF21 | EP-08 | Deliverability Diagnostics Advisor (AG-120, AGT-06) | F: 071 | Yes | Not stated | not stated | Part-11-6b |
| US-08-YG01 | EP-08 | As a permitted user, I want A170 AI Voice & Intelligent Telephony workspace (V12 X26 | G: 040 | Yes | Not stated | not stated | Part-11-7c |
| US-08-YG02 | EP-08 | As a permitted user, I want A182 SMS, RCS & Business Messaging workspace (V12 X38 | G: 052 | Yes | Not stated | not stated | Part-11-7c |
| US-08-YM03 | EP-08 | As a seller I want a daily worklist of eligible prospects with drafts so that I spend my… | M: 007–013 | Yes | Release 3+ | not stated | Part-11-13b |
| US-08-YM04 | EP-08 | As a Sales Lead I want SDR assistance to stop automatically when complaints rise so that… | M: 007–013 | Yes | Release 3+ | not stated | Part-11-13b |
| US-08-ZQ01 | EP-08 | Coaching from permitted recordings | Q: 020–027, 040–046, 048, 672 | Yes | Release 2 | 8–13 | Part-11-18c |
| US-08-ZQ02 | EP-08 | Rubric governance and calibration | Q: 020–027, 040–046, 048 | Yes | Release 2 | 3–5 | Part-11-18c |
| US-08-ZQ03 | EP-08 | Team aggregates and coaching retention | Q: 020–027, 040–046, 048 | Yes | Release 2 | 3–5 | Part-11-18c |
| US-09-YB01 | EP-09 | SM-SVC-10 Meeting, Demo & Appointment Automation: V12 SKU deltas | B: 042 | Yes | Release 3+ | not stated | Part-11-2a |
| US-09-YB02 | EP-09 | SM-SVC-16 Webinar, Event & Referral Acquisition Automation: V12 SKU deltas | B: 049 | Yes | Release 3+ | not stated | Part-11-2a |
| US-09-YC10 | EP-09 | Meeting, Demo & Appointment Automation | C: 049–052 | Yes | Not stated | not stated | Part-11-3b |
| US-09-YC16 | EP-09 | Webinar, Event & Referral Acquisition Automation | C: 073–076 | Yes | Not stated | not stated | Part-11-3c |
| US-10-YB01 | EP-10 | SM-SVC-07 WhatsApp Business Marketing Automation: V12 SKU deltas | B: 039 | Yes | Release 3+ | not stated | Part-11-2a |
| US-10-YC07 | EP-10 | WhatsApp Business Marketing Automation | C: 037–040 | Yes | Not stated | not stated | Part-11-3b |
| US-10-YF22 | EP-10 | Multimodal Enquiry Interpreter (AG-121, AGT-08) | F: 072 | Yes | Not stated | not stated | Part-11-6b |
| US-11-YB01 | EP-11 | SM-SVC-11 Content Marketing Automation: V12 SKU deltas | B: 043 | Yes | Release 3+ | not stated | Part-11-2a |
| US-11-YB02 | EP-11 | SM-SVC-12 Social Media Publishing & Listening Automation: V12 SKU deltas | B: 044 | Yes | Release 3+ | not stated | Part-11-2a |
| US-11-YB03 | EP-11 | SM-SVC-13 SEO & Search Visibility Automation: V12 SKU deltas | B: 045 | Yes | Release 3+ | not stated | Part-11-2a |
| US-11-YB04 | EP-11 | SM-SVC-35 Brand Reputation & Review Intelligence Automation: V12 SKU deltas | B: 092–093 | Yes | Release 3+ | not stated | Part-11-2a |
| US-11-YC11 | EP-11 | Content Marketing Automation | C: 053–056 | Yes | Not stated | not stated | Part-11-3c |
| US-11-YC12 | EP-11 | Social Media Publishing & Listening Automation | C: 057–060 | Yes | Not stated | not stated | Part-11-3c |
| US-11-YC13 | EP-11 | SEO & Search Visibility Automation | C: 061–064 | Yes | Not stated | not stated | Part-11-3c |
| US-11-YD01 | EP-11 | As a Marketing Lead (R05L), I want every creative checked for rights | D: 127 | Yes | Not stated | 3–5 | Part-11-4d |
| US-11-YD02 | EP-11 | As a Marketing Lead, I want authorized reviews monitored | D: 135 | Yes | Not stated | 8–13 | Part-11-4d |
| US-11-YF03 | EP-11 | Audio, Subtitle and Creative Localization Agent (AG-102, AGT-20) | F: 053 | Yes | Not stated | not stated | Part-11-6b |
| US-11-YF04 | EP-11 | Creative Brand, Rights and Claims Validator (AG-103, AGT-20) | F: 054 | Yes | Not stated | not stated | Part-11-6b |
| US-11-YF08 | EP-11 | Review and Reputation Monitor (AG-107, AGT-20) | F: 058 | Yes | Not stated | not stated | Part-11-6b |
| US-11-YF09 | EP-11 | Review Response Drafter (AG-108, AGT-20) | F: 059 | Yes | Not stated | not stated | Part-11-6b |
| US-11-YF19 | EP-11 | Search and Answer-Engine Visibility Analyst (AG-118, AGT-11) | F: 069 | Yes | Not stated | not stated | Part-11-6b |
| US-11-YF20 | EP-11 | Social Listening and Community Response Drafter (AG-119, AGT-11) | F: 070 | Yes | Not stated | not stated | Part-11-6b |
| US-11-YG01 | EP-11 | As a permitted user, I want A171 Multimodal Creative & Localization workspace (V12 X27 | G: 041 | Yes | Not stated | not stated | Part-11-7c |
| US-11-YG02 | EP-11 | As a permitted user, I want A179 Brand Reputation & Review Intelligence workspace | G: 049 | Yes | Not stated | not stated | Part-11-7c |
| US-11-YM35 | EP-11 | As a marketer I want AI-generated media signed and labelled so that we meet disclosure… | M: 097 | Yes | Release 3+ | not stated | Part-11-13b |
| US-12-YB01 | EP-12 | SM-SVC-14 Paid Digital Advertising Automation: V12 SKU deltas | B: 046 | Yes | Release 3+ | not stated | Part-11-2a |
| US-12-YB02 | EP-12 | SM-SVC-15 Landing Page & Website Lead Intake Automation: V12 SKU deltas | B: 047–048 | Yes | Release 3+ | not stated | Part-11-2a |
| US-12-YB03 | EP-12 | SM-SVC-30 Conversion Rate Optimization & Intelligent Experimentation Automation: V12 SKU… | B: 079–080 | Yes | Release 3+ | not stated | Part-11-2a |
| US-12-YC14 | EP-12 | Paid Digital Advertising Automation | C: 065–068 | Yes | Not stated | not stated | Part-11-3c |
| US-12-YC15 | EP-12 | Landing Page & Website Lead Intake Automation | C: 069–072 | Yes | Not stated | not stated | Part-11-3c |
| US-12-YD01 | EP-12 | As a Marketing Lead, I want funnel analysis and pre-registered experiments from SVC-30 | D: 130 | Yes | Not stated | 5–8 | Part-11-4d |
| US-12-YF02 | EP-12 | Marketing Creative Brief and Image Drafter (AG-101, AGT-20) | F: 052 | Yes | Not stated | not stated | Part-11-6b |
| US-12-YG01 | EP-12 | As a permitted user, I want A174 Conversion Rate Optimization & Intelligent… | G: 044 | Yes | Not stated | not stated | Part-11-7c |
| US-12-YI01 | EP-12 | As a growth manager I want experiments with guardrails and a human decision | I: 046 | Yes | Not stated | not stated | Part-11-9c |
| US-12-YM15 | EP-12 | As a marketer I want a campaign pre-flight so that I avoid pauses after launch | M: 048–053 | Yes | Release 3+ | not stated | Part-11-13b |
| US-12-YM16 | EP-12 | As a Startup Head I want the pre-flight attached to the approval so that I approve with… | M: 048–053 | Yes | Release 3+ | not stated | Part-11-13b |
| US-12-YM29 | EP-12 | As a marketer I want a synthetic pre-test of variants so that real experiments start… | M: 086–089 | Yes | Release 3+ | not stated | Part-11-13b |
| US-12-YM30 | EP-12 | As a marketer I want the panel disabled when it is not predictive so that I am not misled | M: 086–089 | Yes | Release 3+ | not stated | Part-11-13b |
| US-13-YB01 | EP-13 | SM-SVC-17 Proposal & Quotation Automation: V12 SKU deltas | B: 050 | Yes | Release 3+ | not stated | Part-11-2a |
| US-13-YB02 | EP-13 | SM-SVC-18 Negotiation, Contract & MoU Automation: V12 SKU deltas | B: 051 | Yes | Release 3+ | not stated | Part-11-2a |
| US-13-YB03 | EP-13 | SM-SVC-37 Pricing, Offer & Revenue Optimization Automation: V12 SKU deltas | B: 095–097 | Yes | Release 3+ | not stated | Part-11-2a |
| US-13-YC17 | EP-13 | Proposal & Quotation Automation | C: 077–080 | Yes | Not stated | not stated | Part-11-3c |
| US-13-YC18 | EP-13 | Negotiation, Contract & MoU Automation | C: 081–084 | Yes | Not stated | not stated | Part-11-3c |
| US-13-YD01 | EP-13 | As a Sales Lead (R03L), I want verified external AI agents to read our approved catalogue… | D: 128 | Yes | Not stated | 8–13 | Part-11-4d |
| US-13-YD02 | EP-13 | As Finance, I want margin and pricing-policy monitoring from SVC-37 using deterministic… | D: 137 | Yes | Not stated | 3–5 | Part-11-4d |
| US-13-YF05 | EP-13 | Agentic Commerce Counterparty Reader and Quotation Drafter (AG-104, AGT-20) | F: 055 | Yes | Not stated | not stated | Part-11-6b |
| US-13-YF18 | EP-13 | Contract Drafting and Obligation Extractor (AG-117, AGT-14) | F: 068 | Yes | Not stated | not stated | Part-11-6b |
| US-13-YG01 | EP-13 | As a permitted user, I want W23 repurposed as 'Subscription quotation review' | G: 023 | Yes | Not stated | not stated | Part-11-7c |
| US-13-YG02 | EP-13 | As a permitted user, I want W24 repurposed as 'Service agreement review' | G: 024 | Yes | Not stated | not stated | Part-11-7c |
| US-13-YG03 | EP-13 | As a permitted user, I want A172 Agentic Commerce & AI-to-AI Business Transaction… | G: 042 | Yes | Not stated | not stated | Part-11-7c |
| US-13-YG04 | EP-13 | As a permitted user, I want A181 Pricing, Offer & Revenue Optimization workspace | G: 051 | Yes | Not stated | not stated | Part-11-7c |
| US-14-YB01 | EP-14 | SM-SVC-19 Tender & Project Bid Automation: V12 SKU deltas | B: 052 | Yes | Release 3+ | not stated | Part-11-2a |
| US-14-YB02 | EP-14 | SM-SVC-20 Sales Order & Fulfillment Automation: V12 SKU deltas | B: 053–054 | Yes | Release 3+ | not stated | Part-11-2a |
| US-14-YC19 | EP-14 | Tender & Project Bid Automation | C: 085–088 | Yes | Not stated | not stated | Part-11-3c |
| US-14-YC20 | EP-14 | Sales Order & Fulfillment Automation | C: 089–092 | Yes | Not stated | not stated | Part-11-3c |
| US-14-YD01 | EP-14 | As an Order Coordinator (R07), I want marketplace listings, inventory | D: 131 | Yes | Not stated | 13–21 | Part-11-4d |
| US-14-YD02 | EP-14 | As an Order Coordinator, I want supplier qualification, RFQ comparison | D: 139 | Yes | Not stated | 8–13 | Part-11-4d |
| US-14-YF12 | EP-14 | Supplier Qualification and RFQ Analyst (AG-111, AGT-20) | F: 062 | Yes | Not stated | not stated | Part-11-6b |
| US-14-YF13 | EP-14 | Marketplace Order-Event Classifier (AG-112, AGT-20) | F: 063 | Yes | Not stated | not stated | Part-11-6b |
| US-14-YF16 | EP-14 | Order Fulfilment Exception Analyst (AG-115, AGT-13) | F: 066 | Yes | Not stated | not stated | Part-11-6b |
| US-14-YG01 | EP-14 | As a permitted user, I want W25 repurposed as 'Subscription order status' | G: 025 | Yes | Not stated | not stated | Part-11-7c |
| US-14-YG02 | EP-14 | As a permitted user, I want A175 Marketplace & E-commerce Channel Operations workspace | G: 045 | Yes | Not stated | not stated | Part-11-7c |
| US-14-YG03 | EP-14 | As a permitted user, I want A183 Procurement & Supplier Management workspace (V12 X39 | G: 053 | Yes | Not stated | not stated | Part-11-7c |
| US-14-YM17 | EP-14 | As a buyer I want a normalised quote comparison and should-cost range so that I negotiate… | M: 054–058 | Yes | Release 3+ | not stated | Part-11-13b |
| US-14-YM18 | EP-14 | As a buyer I want a negotiation pack and draft that I control so that I negotiate… | M: 054–058 | Yes | Release 3+ | not stated | Part-11-13b |
| US-14-ZP01 | EP-14 | Seal and cross-check the bid package | P: 001–150 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-14-ZP02 | EP-14 | Decide the submission mode and submit under a per-tender mandate | P: 110–135 | Yes | Release 2 | 8–13 | Part-11-17b |
| US-14-ZP03 | EP-14 | Verify receipts and reconcile unknown outcomes | P: 110–135 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-14-ZP04 | EP-14 | Maintain the portal capability registry and assisted sessions | P: 110–135 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-15-YB01 | EP-15 | SM-SVC-21 Payment, Invoice & Reconciliation Automation: V12 SKU deltas | B: 055 | Yes | Release 3+ | not stated | Part-11-2a |
| US-15-YB02 | EP-15 | SM-SVC-24 Revenue, Attribution & Sales Forecast Automation: V12 SKU deltas | B: 058 | Yes | Release 3+ | not stated | Part-11-2a |
| US-15-YD01 | EP-15 | As a Finance Maker (R08), I want payment evidence imported | D: 121 | Yes | Not stated | 8–13 | Part-11-4d |
| US-15-YE01 | EP-15 | As a finance user I want SaaS, provider, subscriber and ad-spend ledgers separate | E: 079–082 | No → US-15-ZU01 | Not stated | not stated | Part-11-5b |
| US-15-YF10 | EP-15 | Pricing and Margin Insight Analyst (AG-109, AGT-20) | F: 060 | Yes | Not stated | not stated | Part-11-6b |
| US-15-YF17 | EP-15 | Receivable Discrepancy and Overdue-Risk Explainer (AG-116, AGT-16) | F: 067 | Yes | Not stated | not stated | Part-11-6b |
| US-15-YG01 | EP-15 | As a permitted user, I want W26 repurposed as 'Billing & invoice status' | G: 026 | Yes | Not stated | not stated | Part-11-7c |
| US-15-YI01 | EP-15 | As a revenue lead I want attributed revenue only from verified events with evidenced… | I: 042 | Yes | Not stated | not stated | Part-11-9c |
| US-15-YM11 | EP-15 | As Finance maker I want leakage findings with amounts and evidence so that I recover… | M: 034–040 | Yes | Release 3+ | not stated | Part-11-13b |
| US-15-YM12 | EP-15 | As Finance checker I want corrective documents to go through maker-checker so that… | M: 034–040 | Yes | Release 3+ | not stated | Part-11-13b |
| US-15-ZP01 | EP-15 | Register payment mandates and execute payments via a licensed PSP | P: 001–150 | Yes | Release 2 | 8–13 | Part-11-17b |
| US-15-ZP02 | EP-15 | Reconcile settlements and post journals | P: 062–064, 083–092 | Yes | Release 2 | 8–13 | Part-11-17b |
| US-15-ZP03 | EP-15 | Handle refunds, disputes and chargebacks | P: 083–092 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-16-YA01 | EP-16 | As a customer success manager, I want a first-value milestone and success plan for each… | A: 160–161 | No → US-16-ZU02 | Release 2 | 8 | Part-11-1b |
| US-16-YA02 | EP-16 | As a customer success manager, I want health scores that show unknown inputs and never… | A: 162–163 | No → US-16-ZU03 | Release 3+ | 5 | Part-11-1b |
| US-16-YB01 | EP-16 | SM-SVC-22 Customer, Partner & Institutional Onboarding Automation: V12 SKU deltas | B: 056 | Yes | Release 3+ | not stated | Part-11-2a |
| US-16-YB02 | EP-16 | SM-SVC-23 Customer Retention, Renewal & Feedback Automation: V12 SKU deltas | B: 057 | Yes | Release 3+ | not stated | Part-11-2a |
| US-16-YB03 | EP-16 | SM-SVC-32 Partner, Distributor & Co-Selling Automation: V12 SKU deltas | B: 085 | Yes | Release 3+ | not stated | Part-11-2a |
| US-16-YB04 | EP-16 | SM-SVC-34 Product-Led Growth & Usage Intelligence Automation: V12 SKU deltas | B: 090–091 | Yes | Release 3+ | not stated | Part-11-2a |
| US-16-YD01 | EP-16 | As a Startup Head (R02), I want onboarding plans, pilot readiness and adaptive due dates… | D: 122 | Yes | Not stated | 5–8 | Part-11-4d |
| US-16-YD02 | EP-16 | As a Growth Manager (R03), I want renewal reminders | D: 123 | Yes | Not stated | 5–8 | Part-11-4d |
| US-16-YD03 | EP-16 | As a Startup Head, I want partner recruitment, enablement | D: 132 | Yes | Not stated | 5–8 | Part-11-4d |
| US-16-YF06 | EP-16 | Product Usage and Activation Analyst (AG-105, AGT-20) | F: 056 | Yes | Not stated | not stated | Part-11-6b |
| US-16-YF14 | EP-16 | Support Recovery and Recurring-Issue Analyst (AG-113, AGT-20) | F: 064 | Yes | Not stated | not stated | Part-11-6b |
| US-16-YF15 | EP-16 | Sales Capability-Gap and Training Recommender (AG-114, AGT-20) | F: 065 | Yes | Not stated | not stated | Part-11-6b |
| US-16-YF23 | EP-16 | Onboarding and Pilot Readiness Planner (AG-122, AGT-17) | F: 073 | Yes | Not stated | not stated | Part-11-6b |
| US-16-YG01 | EP-16 | As a permitted user, I want W27 repurposed as 'Private onboarding checklist' | G: 027 | Yes | Not stated | not stated | Part-11-7c |
| US-16-YG02 | EP-16 | As a permitted user, I want W28 repurposed as 'Support | G: 028 | Yes | Not stated | not stated | Part-11-7c |
| US-16-YG03 | EP-16 | As a permitted user, I want A176 Partner, Distributor & Co-Selling workspace (V12 X32 | G: 046 | Yes | Not stated | not stated | Part-11-7c |
| US-16-YG04 | EP-16 | As a permitted user, I want A177 Customer Service & Support Operations workspace | G: 047 | Yes | Not stated | not stated | Part-11-7c |
| US-16-YG05 | EP-16 | As a permitted user, I want A178 Product-Led Growth & Usage Intelligence workspace | G: 048 | Yes | Not stated | not stated | Part-11-7c |
| US-16-YI01 | EP-16 | As a customer-success lead I want CSAT/CES/NPS with response rates | I: 047 | Yes | Not stated | not stated | Part-11-9c |
| US-17-YA01 | EP-17 | As a manager, I want 14 differentiated Command Centre views with cascading filters that… | A: 120, 122–123 | No → US-17-ZU03 | Release 2 | 13 | Part-11-1b |
| US-17-YA02 | EP-17 | As an analyst, I want drill-down totals that reconcile to tiles in native currency | A: 036, 124 | No → US-17-ZU01 | Release 2 | 5 | Part-11-1b |
| US-17-YD01 | EP-17 | As Finance (R08), I want attribution, forecast scenarios and calibration from SVC-24 | D: 124 | Yes | Not stated | 5–8 | Part-11-4d |
| US-17-YG01 | EP-17 | As a startup head (R02), I want A180 AI Sales Enablement & Coaching workspace (V12 X36 | G: 050 | Yes | Not stated | not stated | Part-11-7c |
| US-17-YG02 | EP-17 | As a startup head (R02), I want A089 Unified Command Centre: 14 management views | G: 091 | Yes | Not stated | not stated | Part-11-7c |
| US-17-YG03 | EP-17 | As a startup head (R02), I want A106 scoped action inbox separate from operator-wide… | G: 094 | Yes | Not stated | not stated | Part-11-7c |
| US-17-YG04 | EP-17 | As a startup head (R02), I want Responsive records: labelled keyboard-focusable scroll… | G: 100 | Yes | Not stated | not stated | Part-11-7c |
| US-17-YG05 | EP-17 | As a startup head (R02), I want Contextual mobile filters in native disclosures… | G: 101 | Yes | Not stated | not stated | Part-11-7c |
| US-17-YG06 | EP-17 | As a startup head (R02), I want Scope-keyed saved filter views revalidated on apply | G: 109 | Yes | Not stated | not stated | Part-11-7c |
| US-17-YG07 | EP-17 | As a startup head (R02), I want Cascading context filters: changing… | G: 110 | Yes | Not stated | not stated | Part-11-7c |
| US-17-YG08 | EP-17 | As a startup head (R02), I want Customer experience controls in UI: guided tours | G: 115 | Yes | Not stated | not stated | Part-11-7c |
| US-17-YI01 | EP-17 | As an executive I want every KPI tile to open a drill-down whose rows add up to the tile | I: 040 | Yes | Not stated | not stated | Part-11-9c |
| US-17-YI02 | EP-17 | As an analytics owner I want metric definitions approved and versioned so that late… | I: 044 | Yes | Not stated | not stated | Part-11-9c |
| US-17-YM21 | EP-17 | As the Founder I want a daily decision-first flash so that nothing waits on me unnoticed | M: 065–069 | Yes | Release 3+ | not stated | Part-11-13b |
| US-17-YM22 | EP-17 | As a Startup Head I want my weekly brief to show only data I may see so that… | M: 065–069 | Yes | Release 3+ | not stated | Part-11-13b |
| US-17-YM36 | EP-17 | As a SaaS client admin I want peer benchmarks, only if privacy is guaranteed | M: 098 | No →  | Release 3+ | not stated | Part-11-13b |
| US-17-ZR24 | EP-17 | Benchmark participation under contract clause | M: 098; R: 131–155 | Yes | Release 2 | 3–5 | Part-11-19c |
| US-17-ZR25 | EP-17 | Differentially private benchmark computation and publication | M: 098; R: 131–155 | Yes | Release 2 | 8–13 | Part-11-19c |
| US-18-YA01 | EP-18 | As the compliance lead, I want V12 authority levels mapped to the DEC-064 caps so that no… | A: 110–112 | Yes | Release 1 | 5 | Part-11-1b |
| US-18-YC21 | EP-18 | Contract registry and typed runs | C: 001–012 | Yes | Not stated | not stated | Part-11-3a |
| US-18-YC22 | EP-18 | Authority crosswalk and risk classes | C: 001–012 | Yes | Not stated | not stated | Part-11-3a |
| US-18-YD01 | EP-18 | As an Automation Lead (R11), I want every V12 workflow registered under its literal ID… | D: 001, 003 | Yes | Not stated | 5–8 | Part-11-4d |
| US-18-YD02 | EP-18 | As a Requester, I want my run input validated against the workflow DTO with field-level… | D: 002, 023 | Yes | Not stated | 3–5 | Part-11-4d |
| US-18-YD03 | EP-18 | As a Reviewer, I want approvals bound to the exact payload, amount | D: 009, 026 | Yes | Not stated | 5–8 | Part-11-4d |
| US-18-YD04 | EP-18 | As an SRE, I want checkpoints, heartbeats and a reaper | D: 004–006 | Yes | Not stated | 5–8 | Part-11-4d |
| US-18-YD05 | EP-18 | As an Automation Lead, I want five trigger kinds with misfire policy and reviewer… | D: 010–011, 016–017 | Yes | Not stated | 8–13 | Part-11-4d |
| US-18-YD06 | EP-18 | As an operator in A110, I want the V12 run states and a timeline with reservations | D: 018 | Yes | Not stated | 5–8 | Part-11-4d |
| US-18-YD07 | EP-18 | As a tenant, I want fair scheduling and a budget hierarchy | D: 019–020, 028 | Yes | Not stated | 8–13 | Part-11-4d |
| US-18-YD08 | EP-18 | As an Automation Lead, I want parallel read branches with joins | D: 021 | Yes | Not stated | 3–5 | Part-11-4d |
| US-18-YD09 | EP-18 | As a Tenant Administrator (R12), I want to pause and re-cadence my schedules within… | D: 022 | Yes | Not stated | 3–5 | Part-11-4d |
| US-18-YD10 | EP-18 | As a Product Owner, I want templates as parameter sets and KPIs registered per workflow | D: 013–015, 024–025, 027 | Yes | Not stated | 5–8 | Part-11-4d |
| US-18-YE01 | EP-18 | As an automation lead I want to replay dead letters only with current policy and the… | E: 095, 097–099 | Yes | Not stated | not stated | Part-11-5b |
| US-18-YE02 | EP-18 | As the platform I want backpressure and degradation so overload never loses accepted work | E: 096, 100–101 | No → US-18-ZU03 | Not stated | not stated | Part-11-5b |
| US-18-YF28 | EP-18 |  | F: 035 | Yes | Not stated | not stated | Part-11-6b |
| US-18-YG01 | EP-18 | As an automation lead (R11), I want A192 Automation service catalogue (tenant view) | G: 062 | Yes | Not stated | not stated | Part-11-7c |
| US-18-YG02 | EP-18 | As an automation lead (R11), I want A193 Service workspace detail | G: 063 | Yes | Not stated | not stated | Part-11-7c |
| US-18-YG03 | EP-18 | As an automation lead (R11), I want A194 Workflow registry | G: 064 | Yes | Not stated | not stated | Part-11-7c |
| US-18-YG04 | EP-18 | As an automation lead (R11), I want A195 Workflow contract detail and walkthrough | G: 065 | Yes | Not stated | not stated | Part-11-7c |
| US-18-YG05 | EP-18 | As an automation lead (R11), I want A110 Live Automation Execution Monitor: V12 RUNS… | G: 090 | Yes | Not stated | not stated | Part-11-7c |
| US-18-YG06 | EP-18 | As an automation lead (R11), I want Run state display and separation of duties: Queued | G: 111 | Yes | Not stated | not stated | Part-11-7c |
| US-18-YG07 | EP-18 | As an automation lead (R11), I want Shared domain-panel component for 39 service… | G: 116 | Yes | Not stated | not stated | Part-11-7c |
| US-18-YH01 | EP-18 | As an integrator I want one run gateway with typed DTOs and dry-run so that I can start… | H: 011 | Yes | Release 1 | not stated | Part-11-8b |
| US-18-YI01 | EP-18 | As a workflow owner I want effects to move forward only and never be deleted so that… | I: 015 | Yes | Not stated | not stated | Part-11-9b |
| US-18-YI02 | EP-18 | As a configuration owner I want workflow configurations tied to an approved revision with… | I: 023 | Yes | Not stated | not stated | Part-11-9b |
| US-18-YL01 | EP-18 | As an Admin user, I want scope, filters, record linkage | L: 001–015 | No → US-18-ZU10, US-18-ZU11, US-18-ZU12, US-18-ZU13 | Not stated | 8 | Part-11-12 |
| US-18-YL04 | EP-18 | As the product owner, I want UX-BR-02…05 verified on the 36-tenant fixture | L: 017–020 | No → US-18-ZU14 | Not stated | 5 | Part-11-12 |
| US-18-YM05 | EP-18 | As an approver I want similar items grouped with outliers highlighted so that I review… | M: 014–019 | Yes | Release 3+ | not stated | Part-11-13b |
| US-18-YM06 | EP-18 | As an approver I want a neutral note with risks and diffs so that I know what to check | M: 014–019 | Yes | Release 3+ | not stated | Part-11-13b |
| US-18-YM07 | EP-18 | As an Automation Lead I want weekly service improvement proposals so that services meet… | M: 020–026 | Yes | Release 3+ | not stated | Part-11-13b |
| US-18-YM26 | EP-18 | As a tenant I want to install a certified template as a draft so that I adopt proven… | M: 079–080 | No →  | Release 3+ | not stated | Part-11-13b |
| US-18-ZP01 | EP-18 | Draft and simulate a bounded mandate | P: 001–150 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-18-ZP02 | EP-18 | Approve a mandate with two distinct people | P: 006–022, 032 | Yes | Release 2 | 8–13 | Part-11-17b |
| US-18-ZP03 | EP-18 | Recheck every mandated dispatch in the PDP | P: 040–052 | Yes | Release 2 | 8–13 | Part-11-17b |
| US-18-ZP04 | EP-18 | Reserve and commit consumption exactly once | P: 023–036 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-18-ZP05 | EP-18 | Revoke and tighten a mandate instantly | P: 006–022, 032, 053–058, 095 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-18-ZP06 | EP-18 | Engage and release the kill switch by scope | P: 053–058 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-18-ZP07 | EP-18 | Detect anomalies and suspend tighten-only | P: 037, 059–067 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-18-ZP08 | EP-18 | Reconcile mandates and export evidence packs | P: 037, 059–067 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-18-ZP09 | EP-18 | Run new mandate types in shadow first | P: 037, 059–067 | Yes | Release 2 | 3–5 | Part-11-17b |
| US-18-ZP10 | EP-18 | Bind L4 plans to L3 mandates | P: 004–005, 098 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-18-ZR11 | EP-18 | Connector framework and activation gate | R: 056–080 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-19-YA01 | EP-19 | As a visitor, I want a neutral catalogue of 39 automation services with no customer data | A: 050–052, 055 | Yes | Release 1 | 8 | Part-11-1b |
| US-19-YA02 | EP-19 | As a visitor, I want public data-rights and AI-transparency pages | A: 053–054 | No →  | Release 1 | 5 | Part-11-1b |
| US-19-YA03 | EP-19 | As a visitor, I want explainable SKU suggestions, comparisons and a TCO/ROI estimate that… | A: 056–057, 059 | No → US-19-ZU02 | Release 2 | 8 | Part-11-1b |
| US-19-YG01 | EP-19 | As an anonymous visitor (R18), I want W01 repurposed as 'Home' | G: 001 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG02 | EP-19 | As an anonymous visitor (R18), I want W02 repurposed as 'Automation categories' | G: 002 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG03 | EP-19 | As an anonymous visitor (R18), I want W03 repurposed as 'Automation family details' | G: 003 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG04 | EP-19 | As an anonymous visitor (R18), I want W04 repurposed as 'Complete automation catalog' | G: 004 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG05 | EP-19 | As an anonymous visitor (R18), I want W05 repurposed as 'Individual automation details' | G: 005 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG06 | EP-19 | As an anonymous visitor (R18), I want W06 repurposed as 'Plans & automation selection' | G: 006 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG07 | EP-19 | As an anonymous visitor (R18), I want W07 repurposed as 'Industry solution guide' | G: 007 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG08 | EP-19 | As an anonymous visitor (R18), I want W08 repurposed as 'Resources & automation guides' | G: 008 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG09 | EP-19 | As an anonymous visitor (R18), I want W09 repurposed as 'Illustrative use cases' | G: 009 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG10 | EP-19 | As an anonymous visitor (R18), I want W10 repurposed as 'Campaign automation overview' | G: 010 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG11 | EP-19 | As an anonymous visitor (R18), I want W11 repurposed as 'Automation selection assistant' | G: 011 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG12 | EP-19 | As an anonymous visitor (R18), I want W12 repurposed as 'Service enquiry' | G: 012 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG13 | EP-19 | As an anonymous visitor (R18), I want W13 repurposed as 'Product demo & partnership… | G: 013 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG14 | EP-19 | As an anonymous visitor (R18), I want W14 repurposed as 'Custom quotation request' | G: 014 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG15 | EP-19 | As an anonymous visitor (R18), I want W15 repurposed as 'Automation requirements builder'… | G: 015 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG16 | EP-19 | As an anonymous visitor (R18), I want W16 repurposed as 'Channel & integration options' | G: 016 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG17 | EP-19 | As an anonymous visitor (R18), I want W17 repurposed as 'Service delivery models' | G: 017 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG18 | EP-19 | As an anonymous visitor (R18), I want W18 repurposed as 'Consultation & demo booking' | G: 018 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG19 | EP-19 | As an anonymous visitor (R18), I want W19 repurposed as 'Product webinars & events' | G: 019 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG20 | EP-19 | As an anonymous visitor (R18), I want W20 repurposed as 'Service referral programme' | G: 020 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG21 | EP-19 | As an anonymous visitor (R18), I want W21 repurposed as 'Client sign-in & recovery' | G: 021 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG22 | EP-19 | As an anonymous visitor (R18), I want W22 repurposed as 'Client service dashboard' | G: 022 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG23 | EP-19 | As an anonymous visitor (R18), I want W30 repurposed as 'Contact | G: 030 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG24 | EP-19 | As an anonymous visitor (R18), I want W50 AI transparency and trust | G: 035 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG25 | EP-19 | As an anonymous visitor (R18), I want W51 Enterprise capabilities | G: 036 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG26 | EP-19 | As an anonymous visitor (R18), I want W52 Legal centre | G: 037 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG27 | EP-19 | As an anonymous visitor (R18), I want W53 Not found (404) (V12 | G: 038 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG28 | EP-19 | As an anonymous visitor (R18), I want W47 Developer portal: V12 W39 delta so that the V12… | G: 077 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG29 | EP-19 | As an anonymous visitor (R18), I want A107 renamed 'Tenant-owned website intake… | G: 092 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG30 | EP-19 | As an anonymous visitor (R18), I want A108 renamed 'Tenant-owned landing page review &… | G: 093 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG31 | EP-19 | As an anonymous visitor (R18), I want Internationalisation: externalised ICU strings | G: 095 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG32 | EP-19 | As an anonymous visitor (R18), I want Inline form validation: aria-invalid | G: 097 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG33 | EP-19 | As an anonymous visitor (R18), I want Skip link, route focus to main | G: 098 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG34 | EP-19 | As an anonymous visitor (R18), I want Mobile bottom navigation: website Home, Services | G: 099 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG35 | EP-19 | As an anonymous visitor (R18), I want W05/W08 workflow sample library: four workflow… | G: 106 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG36 | EP-19 | As an anonymous visitor (R18), I want Planning calculators: W01 illustrative savings | G: 107 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG37 | EP-19 | As an anonymous visitor (R18), I want Readiness assessment and opportunity report | G: 108 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YG38 | EP-19 | As an anonymous visitor (R18), I want No investor / fundraising mode in the commercial… | G: 117 | Yes | Not stated | not stated | Part-11-7c |
| US-19-YK10 | EP-19 | Scoped mobile notifications | K: 009 | Yes | Not stated | not stated | Part-11-11b |
| US-19-YL02 | EP-19 | As a public visitor or portal user, I want only published | L: 002, 012, 014 | No →  | Not stated | 3 | Part-11-12 |
| US-20-YA01 | EP-20 | As a subscriber admin, I want to buy a single SKU without buying its upstream SKUs | A: 001–003, 010–011, 014, 016–022, 055–057, 071, 090, 096–097, 120 | Yes | Release 2 | 5 | Part-11-1b |
| US-20-YA02 | EP-20 | As a subscriber admin, I want to preview the effect of an upgrade or downgrade before I… | A: 001–003, 014, 016–022, 055–057, 071, 090, 096–097, 120 | No →  | Release 2 | 8 | Part-11-1b |
| US-20-YA03 | EP-20 | As finance, I want a quote and its acceptance bound to the exact application revision and… | A: 001–003, 014, 016–022, 055–057, 071, 090, 096–097, 120 | No →  | Release 2 | 5 | Part-11-1b |
| US-20-YA04 | EP-20 | As finance, I want failed payments to enter a grace period with notices before… | A: 001–003, 014, 016–022, 055–057, 071, 090, 096–097, 120 | No →  | Release 2 | 5 | Part-11-1b |
| US-20-YA05 | EP-20 | As a subscriber admin, I want to cancel without a forced survey and receive my export and… | A: 001–003, 014, 016–022, 055–057, 071, 090, 096–097, 120, 168 | No → US-20-ZU10 | Release 2 | 5 | Part-11-1b |
| US-20-YA06 | EP-20 | As an applicant, I want an eight-stage wizard that saves server-side drafts and rejects… | A: 001–003, 014, 016–022, 055–057, 071, 090–092, 096–097, 120 | No → US-20-ZU07 | Release 2 | 13 | Part-11-1b |
| US-20-YA07 | EP-20 | As the service owner, I want a per-SKU meter registry with pilot caps and cost ranges | A: 032–033, 035 | No → US-20-ZU05 | Release 2 | 8 | Part-11-1b |
| US-20-YA08 | EP-20 | As the CPO, I want BR-V12 enterprise capabilities registered with release mapping and… | A: 180–189 | No → US-20-ZU11, US-20-ZU12, US-20-ZU13 | Release 1 | 3 | Part-11-1b |
| US-20-YD01 | EP-20 | As a support lead, I want cases created, triaged, resolved and SLA-monitored by SVC-33 | D: 133 | Yes | Not stated | 8–13 | Part-11-4d |
| US-20-YD02 | EP-20 | As a Growth Manager, I want usage, activation and expansion signals from SVC-34 | D: 134 | Yes | Not stated | 5–8 | Part-11-4d |
| US-20-YE01 | EP-20 | As an applicant I want to submit a configuration envelope and have stale revisions… | E: 030–031, 040 | Yes | Not stated | not stated | Part-11-5b |
| US-20-YE02 | EP-20 | As an applicant I want to complete eight stages and resume a draft on any device | E: 032–034, 036–037 | No → US-20-ZU15, US-20-ZU16 | Not stated | not stated | Part-11-5b |
| US-20-YE03 | EP-20 | As a platform operator I want a provisioning saga that holds on failure and compensates… | E: 035, 038 | Yes | Not stated | not stated | Part-11-5b |
| US-20-YE04 | EP-20 | As a catalogue reviewer I want SKU versions to move through a controlled lifecycle and… | E: 045–051 | No → US-20-ZU17, US-20-ZU18 | Not stated | not stated | Part-11-5b |
| US-20-YE05 | EP-20 | As a billing owner I want to accept an exact quote revision so that I am bound only to… | E: 055–057, 065 | Yes | Not stated | not stated | Part-11-5b |
| US-20-YE06 | EP-20 | As the platform I want provisioning only after a verified payment event | E: 057, 075 | Yes | Not stated | not stated | Part-11-5b |
| US-20-YE07 | EP-20 | As the platform I want entitlement checked at API, enqueue, worker and effect | E: 059–061 | Yes | Not stated | not stated | Part-11-5b |
| US-20-YE08 | EP-20 | As a billing owner I want to preview a plan change with proration before confirming | E: 062–063 | No → US-20-ZU20 | Not stated | not stated | Part-11-5b |
| US-20-YE09 | EP-20 | As the platform I want atomic reservations that release unused units and keep uncertain… | E: 070–071 | Yes | Not stated | not stated | Part-11-5b |
| US-20-YE10 | EP-20 | As a finance user I want invoices with correct tax in integer minor units | E: 072–074 | Yes | Not stated | not stated | Part-11-5b |
| US-20-YE11 | EP-20 | As a finance user I want dunning to suspend only after grace and reinstate on payment | E: 063, 076 | Yes | Not stated | not stated | Part-11-5b |
| US-20-YE12 | EP-20 | As a billing owner I want to dispute lines and receive a credit note after review | E: 064, 078, 084 | No → US-20-ZU21 | Not stated | not stated | Part-11-5b |
| US-20-YE13 | EP-20 | As a finance user I want revenue recognized daily and reconciled at close | E: 077, 086 | No → US-20-ZU22 | Not stated | not stated | Part-11-5b |
| US-20-YE14 | EP-20 | As a tenant I want controlled offboarding with export and retention | E: 058, 127 | No → US-20-ZU19 | Not stated | not stated | Part-11-5b |
| US-20-YE15 | EP-20 | As a customer-success lead I want TTFV and quota forecasts per tenant | E: 083, 089 | No → US-20-ZU23 | Not stated | not stated | Part-11-5b |
| US-20-YE16 | EP-20 | As a commercial lead I want the partner model, procurement pack and per-SKU service… | E: 085, 087–088 | No → US-20-ZU24 | Not stated | not stated | Part-11-5b |
| US-20-YF07 | EP-20 | Trial Conversion and Upgrade Recommendation Drafter (AG-106, AGT-20) | F: 057 | Yes | Not stated | not stated | Part-11-6b |
| US-20-YG01 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 031 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG02 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 032 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG03 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 033 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG04 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 034 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG05 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 054 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG06 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 055 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG07 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14), I want A186 Plans | G: 056 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG08 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 057 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG09 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 058 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG10 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 059 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG11 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 061 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG12 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 074 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG13 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 084 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG14 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14), I want A103 Import | G: 085 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG15 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 089 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG16 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 104 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG17 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 105 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG18 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 112 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG19 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 113 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YG20 | EP-20 | As a SaaS client admin (R17/R12) or operator (R13/R14) | G: 114 | Yes | Not stated | not stated | Part-11-7c |
| US-20-YH01 | EP-20 | As a billing administrator I want invoice previews with tax lines so that customers see… | H: 039 | No → US-20-ZU28 | Release 2 | not stated | Part-11-8b |
| US-20-YI01 | EP-20 | As a tenant administrator I want a full export with a second approver and a link valid… | I: 020 | Yes | Not stated | not stated | Part-11-9b |
| US-20-YI02 | EP-20 | As a Scale-plan tenant I want to bring my own KMS key and have my data made unreadable if… | I: 021 | Yes | Not stated | not stated | Part-11-9b |
| US-20-YI03 | EP-20 | As a developer of a tenant I want API keys shown once and stored only as a hash | I: 019 | Yes | Not stated | not stated | Part-11-9b |
| US-20-YK03 | EP-20 | Tiered support response targets | K: 005 | Yes | Not stated | not stated | Part-11-11b |
| US-20-YK04 | EP-20 | Status page with maintenance and unknown state | K: 002, 012 | Yes | Not stated | not stated | Part-11-11b |
| US-20-YK05 | EP-20 | SLA schedule and monthly statement | K: 001 | Yes | Not stated | not stated | Part-11-11b |
| US-20-YK06 | EP-20 | Help centre top 50 tasks | K: 006 | Yes | Not stated | not stated | Part-11-11b |
| US-20-YL03 | EP-20 | As a SaaS client administrator, I want a service portal separate from customer roles | L: 015–020 | No → US-20-ZU37 | Not stated | 3 | Part-11-12 |
| US-20-YM23 | EP-20 | As a SaaS client admin I want a go-live checklist that verifies itself so that I know… | M: 070–075 | Yes | Release 3+ | not stated | Part-11-13b |
| US-20-YM24 | EP-20 | As a SaaS client admin I want a copilot that explains blockers and drafts artefacts so… | M: 070–075 | Yes | Release 3+ | not stated | Part-11-13b |
| US-20-YM25 | EP-20 | As a tenant I want to publish a template safely so that others benefit without seeing my… | M: 076–080 | Yes | Release 3+ | not stated | Part-11-13b |
| US-20-ZR06 | EP-20 | Scoped, zone-bound API keys | H: 001–007; R: 031–055 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-20-ZR07 | EP-20 | OAuth 2.0 client credentials | H: 001–007; R: 031–055 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-20-ZR08 | EP-20 | Signed webhooks with delivery log and replay | H: 001–007; R: 031–055 | Yes | Release 1 | 8–13 | Part-11-19c |
| US-20-ZR09 | EP-20 | Developer portal, versioning policy and sandbox with promotion | H: 001–007; R: 031–055 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-20-ZR10 | EP-20 | SDKs for TypeScript, Python and Java | H: 001–007; R: 031–055 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-21-YA01 | EP-21 | As the CPO, I want every KPI defined once in a metric registry with denominator and… | A: 150–152, 220 | No → US-21-ZU03 | Release 2 | 8 | Part-11-1b |
| US-21-YA02 | EP-21 | As the service owner, I want SLA tier templates attachable only after three months of… | A: 140–141, 143 | No → US-21-ZU01 | Release 2 | 5 | Part-11-1b |
| US-21-YA03 | EP-21 | As QA, I want V12 acceptance IDs to resolve to blueprint tests in the RTM | A: 200–202 | No → US-21-ZU05 | Release 1 | 3 | Part-11-1b |
| US-21-YD01 | EP-21 | As a salesperson, I want playbooks, practice and private coaching from SVC-36 | D: 136 | Yes | Not stated | 5–8 | Part-11-4d |
| US-21-YE01 | EP-21 | As a DevOps lead I want the DEC-421 pipeline to promote the same digest with automatic… | E: 105–111, 115–116, 131 | Yes | Not stated | not stated | Part-11-5b |
| US-21-YE02 | EP-21 | As an SRE I want quarterly restore drills that replay erasures and prove RPO/RTO | E: 120–126 | Yes | Not stated | not stated | Part-11-5b |
| US-21-YE03 | EP-21 | As a release manager I want per-SKU gates and GO-01…08 evidence in A090 | E: 130, 132–135 | No → US-21-ZU10, US-21-ZU11 | Not stated | not stated | Part-11-5b |
| US-21-YE04 | EP-21 | As an SRE I want provisioning load tests, autoscaling and a compute benchmark | E: 102–103, 112–114 | No → US-21-ZU08, US-21-ZU09 | Not stated | not stated | Part-11-5b |
| US-21-YG01 | EP-21 | As a release manager (R13), I want A190 Release gates & decision register | G: 060 | Yes | Not stated | not stated | Part-11-7c |
| US-21-YG02 | EP-21 | As a release manager (R13), I want A196 Screen inventory and traceability | G: 066 | Yes | Not stated | not stated | Part-11-7c |
| US-21-YG03 | EP-21 | As a release manager (R13), I want W46 Trust centre: V12 W38 delta so that the V12… | G: 076 | Yes | Not stated | not stated | Part-11-7c |
| US-21-YG04 | EP-21 | As a release manager (R13), I want W45 Status page: V12 W40 delta so that the V12… | G: 078 | Yes | Not stated | not stated | Part-11-7c |
| US-21-YG05 | EP-21 | As a release manager (R13), I want A159 Status and Trust Centre Admin | G: 087 | Yes | Not stated | not stated | Part-11-7c |
| US-21-YG06 | EP-21 | As a release manager (R13), I want A156 SLO and Remediation Console | G: 088 | Yes | Not stated | not stated | Part-11-7c |
| US-21-YG07 | EP-21 | As a release manager (R13), I want Device parity: every registered Website and Admin… | G: 102 | Yes | Not stated | not stated | Part-11-7c |
| US-21-YH01 | EP-21 | As an SRE I want to declare incidents and publish status on an independent host so that… | H: 041 | No → US-21-ZU13 | Release 2 | not stated | Part-11-8b |
| US-21-YI01 | EP-21 | As the release manager I want CI guards on RLS coverage | I: 012 | Yes | Not stated | not stated | Part-11-9b |
| US-21-YI02 | EP-21 | As the security lead I want a release blocked by an overdue Critical finding or an… | I: 050–052 | Yes | Not stated | not stated | Part-11-9c |
| US-21-YI03 | EP-21 | As the DPO I want quarterly incident tabletop exercises with breach clocks | I: 057 | Yes | Not stated | not stated | Part-11-9c |
| US-21-YJ01 | EP-21 | Run the V12 workflow tests of a SKU as one parameterized suite | J: 005 | Yes | Not stated | not stated | Part-11-10c |
| US-21-YJ02 | EP-21 | See the RCTCFE and 20-dimension scorecards for a release | J: 001–003 | Yes | Not stated | not stated | Part-11-10c |
| US-21-YJ03 | EP-21 | Block a release while a gate is not satisfied | J: 001–003 | Yes | Not stated | not stated | Part-11-10c |
| US-21-YJ04 | EP-21 | Maintain the V12 acceptance register | J: 004 | Yes | Not stated | not stated | Part-11-10c |
| US-21-YJ05 | EP-21 | Reject invalid KPI evidence in the preflight | J: 005 | Yes | Not stated | not stated | Part-11-10c |
| US-21-YK01 | EP-21 | Declare and communicate incidents by SEV | K: 003 | Yes | Not stated | not stated | Part-11-11b |
| US-21-YK02 | EP-21 | Paging test and communication game day | K: 003, 015 | Yes | Not stated | not stated | Part-11-11b |
| US-21-YK07 | EP-21 | Post-incident review evidence | K: 007 | Yes | Not stated | not stated | Part-11-11b |
| US-21-YK09 | EP-21 | SLOs with policy-hold separation | K: 011 | Yes | Not stated | not stated | Part-11-11b |
| US-21-YK11 | EP-21 | V12 traceability chains in the RTM | K: 020–021, 026 | Yes | Not stated | not stated | Part-11-11b |
| US-21-YK12 | EP-21 | Customer decision queue with owners | K: 022, 025 | Yes | Not stated | not stated | Part-11-11b |
| US-21-YL05 | EP-21 | As the QA lead, I want the UAT-L pack automated on FX-L-36 | — | No →  | Not stated | 8 | Part-11-12 |
| US-21-YL07 | EP-21 | As the configuration manager, I want annex precedence, archive hashes | L: 027–030 | Yes | Not stated | 3 | Part-11-12 |
| US-21-YM08 | EP-21 | As an Automation Lead I want safe parameters tuned within bands and reverted… | M: 022–025 | No →  | Release 3+ | not stated | Part-11-13b |
| US-21-YM13 | EP-21 | As Platform Support I want integration failures detected and safe ones fixed… | M: 041–047 | Yes | Release 3+ | not stated | Part-11-13b |
| US-21-YM14 | EP-21 | As a Tenant Administrator I want a tested fix proposal for integration failures so that I… | M: 041–047 | Yes | Release 3+ | not stated | Part-11-13b |
| US-21-ZR16 | EP-21 | Regional Vercel projects with pinned functions | R: 081–095 | Yes | Release 1 | 3–5 | Part-11-19c |
| US-21-ZR17 | EP-21 | Vercel logging, header allowlist, origin verification and sub-processor controls | R: 081–095 | Yes | Release 1 | 3–5 | Part-11-19c |
| US-21-ZR18 | EP-21 | Continuous WAL archiving, standby and RPO monitoring | E: 122–125; R: 096–110 | Yes | Release 1 | 8–13 | Part-11-19c |
| US-21-ZR19 | EP-21 | Restore drills at every release gate and per zone | E: 122–125; R: 096–110 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-21-ZR29 | EP-21 | Operability of automations AU-290…299 | R: 027, 078, 093, 100, 124, 137 | Yes | Release 1 | 3–5 | Part-11-19c |
| US-22-YB01 | EP-22 | WF01 inbound: disclose that the caller is speaking with an AI assistant at the… | B: 060–065 | Yes | Release 3+ | not stated | Part-11-2a |
| US-22-YB02 | EP-22 | WF02 outbound: a call is placed only to a contact with recorded call permission… | B: 060–065 | Yes | Release 3+ | not stated | Part-11-2a |
| US-22-YB03 | EP-22 | WF03 multilingual: recognize language, answer from grounded knowledge and… | B: 060–065 | Yes | Release 3+ | not stated | Part-11-2a |
| US-22-YB04 | EP-22 | WF04 call intelligence: transcribe only calls with recorded consent, redact… | B: 060–065 | Yes | Release 3+ | not stated | Part-11-2a |
| US-22-YB05 | EP-22 | The AI voice agent never quotes a non-approved price, accepts an order, agrees… | B: 060–065 | Yes | Release 3+ | not stated | Part-11-2a |
| US-22-YB06 | EP-22 | Call minutes are metered per SKU with a hard budget | B: 060–065 | Yes | Release 3+ | not stated | Part-11-2a |
| US-22-ZQ01 | EP-22 | Inbound AI answering with self-identification and routing | B: 060, 064; Q: 001–055, 134, 273, 400 | Yes | Release 2 | 8–13 | Part-11-18c |
| US-22-ZQ02 | EP-22 | Human handoff on every call | B: 060, 064; Q: 001–055 | Yes | Release 2 | 8–13 | Part-11-18c |
| US-22-ZQ03 | EP-22 | Outbound AI call dispatch preflight | Q: 001–055, 134, 273, 400 | Yes | Release 2 | 13–21 | Part-11-18c |
| US-22-ZQ04 | EP-22 | Calling consent capture and opt-out | Q: 001–055 | Yes | Release 2 | 8–13 | Part-11-18c |
| US-22-ZQ05 | EP-22 | Recording notice and consent per jurisdiction | Q: 001–055 | Yes | Release 2 | 8–13 | Part-11-18c |
| US-22-ZQ06 | EP-22 | Voicemail and answering-machine rules | Q: 001–055 | Yes | Release 2 | 5–8 | Part-11-18c |
| US-22-ZQ07 | EP-22 | Multilingual voice booking | B: 060, 064; Q: 001–055 | Yes | Release 2 | 8–13 | Part-11-18c |
| US-22-ZQ08 | EP-22 | Number inventory and caller ID | Q: 001–055 | Yes | Release 2 | 8–13 | Part-11-18c |
| US-22-ZQ09 | EP-22 | Transcription and redaction | Q: 001–055 | Yes | Release 2 | 8–13 | Part-11-18c |
| US-22-ZQ10 | EP-22 | Recording storage, retention and access | Q: 001–055 | Yes | Release 2 | 8–13 | Part-11-18c |
| US-22-ZQ11 | EP-22 | Call summaries and CRM synchronisation | Q: 001–055 | Yes | Release 2 | 5–8 | Part-11-18c |
| US-22-ZQ12 | EP-22 | Provider-neutral voice stack, latency SLOs and failover | Q: 001–055 | Yes | Release 2 | 13–21 | Part-11-18c |
| US-22-ZQ13 | EP-22 | Call-minute metering, budget and kill switch | Q: 001–055 | Yes | Release 2 | 5–8 | Part-11-18c |
| US-22-ZQ14 | EP-22 | Synthetic voice policy, voice-clone misuse protection and QA | B: 064; Q: 001–055 | Yes | Release 2 | 8–13 | Part-11-18c |
| US-22-ZQ15 | EP-22 | Jurisdiction activation, simulation, accessibility and audit | Q: 001–055 | Yes | Release 2 | 8–13 | Part-11-18c |
| US-22-ZR15 | EP-22 | Voice transport connector with number series and recording consent | R: 075–078 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-23-YB01 | EP-23 | WF01 verifies the sender (DLT entity, header, template IDs, RCS agent) and… | B: 098–101 | Yes | Release 3+ | not stated | Part-11-2a |
| US-23-YB02 | EP-23 | WF02 checks consent, preference (NCPR/DND), quiet hours and frequency, then… | B: 098–101 | Yes | Release 3+ | not stated | Part-11-2a |
| US-23-YB03 | EP-23 | WF03 reconciles delivery reports, classifies replies (STOP cancels queued… | B: 098–101 | Yes | Release 3+ | not stated | Part-11-2a |
| US-23-YB04 | EP-23 | WF04 reports performance, usage, complaints and opt-outs and enforces… | B: 098–101 | Yes | Release 3+ | not stated | Part-11-2a |
| US-23-ZR14 | EP-23 | SMS via DLT with registry scrubbing | R: 070–074 | Yes | Release 1 | 5–8 | Part-11-19c |
| US-24-YB01 | EP-24 | WF01 publishes a machine-readable catalogue of approved offerings (approved… | B: 071–077 | Yes | Release 3+ | not stated | Part-11-2a |
| US-24-YB02 | EP-24 | WF02 accepts requirement and quotation requests only from external agents with… | B: 071–077 | Yes | Release 3+ | not stated | Part-11-2a |
| US-24-YB03 | EP-24 | A mandate record holds principal, counterpart agent identity, scope, item and… | B: 071–077 | Yes | Release 3+ | not stated | Part-11-2a |
| US-24-YB04 | EP-24 | WF03 compares offers within the mandate and routes every consequential decision… | B: 071–077 | Yes | Release 3+ | not stated | Part-11-2a |
| US-24-YB05 | EP-24 | WF04 executes an approved transaction only through the approved provider after… | B: 071–077 | Yes | Release 3+ | not stated | Part-11-2a |
| US-24-YB06 | EP-24 | Interaction logs with external agents are append-only, signed and linked to the… | B: 071–077 | Yes | Release 3+ | not stated | Part-11-2a |
| US-24-YB07 | EP-24 | Untrusted content from external agents is sanitized and never treated as… | B: 071–077 | Yes | Release 3+ | not stated | Part-11-2a |
| US-24-ZP01 | EP-24 | Publish our agent identity and catalog | P: 001–150 | Yes | Release 2 | 5–8 | Part-11-17b |
| US-24-ZP02 | EP-24 | Verify counterparties and manage trust tiers | P: 070–079, 094, 097 | Yes | Release 2 | 8–13 | Part-11-17b |
| US-24-ZP03 | EP-24 | Negotiate within approved bounds | P: 078–087 | Yes | Release 2 | 8–13 | Part-11-17b |
| US-24-ZP04 | EP-24 | Decide commerce payments under mandates | P: 070–098 | Yes | Release 2 | 8–13 | Part-11-17b |
| US-24-ZP05 | EP-24 | Gate external agent interoperability | P: 070–077, 094, 097 | Yes | Release 2 | 3–5 | Part-11-17b |
| US-25-YB01 | EP-25 | WF01 maps approved SKU catalogue fields to each marketplace schema, validates… | B: 081–084 | Yes | Release 3+ | not stated | Part-11-2a |
| US-25-YB02 | EP-25 | WF02 synchronizes price and availability only from the approved price version… | B: 081–084 | Yes | Release 3+ | not stated | Part-11-2a |
| US-25-YB03 | EP-25 | WF03 deduplicates order, cancellation and return events into an order-event… | B: 081–084 | Yes | Release 3+ | not stated | Part-11-2a |
| US-25-YB04 | EP-25 | WF04 matches marketplace sales, fees and verified receipts and reports… | B: 081–084 | Yes | Release 3+ | not stated | Part-11-2a |
| US-26-YB01 | EP-26 | WF01 validates the need, scores suppliers against qualification rules and… | B: 102–105 | Yes | Release 3+ | not stated | Part-11-2a |
| US-26-YB02 | EP-26 | WF02 drafts the RFQ and normalizes supplier quotes (unit, currency, terms, lead… | B: 102–105 | Yes | Release 3+ | not stated | Part-11-2a |
| US-26-YB03 | EP-26 | WF03 calculates the purchase order, requires purchasing approval within budget… | B: 102–105 | Yes | Release 3+ | not stated | Part-11-2a |
| US-26-YB04 | EP-26 | WF04 tracks milestones, reconciles receipts against the PO (three-way match)… | B: 102–105 | Yes | Release 3+ | not stated | Part-11-2a |
| US-27-YB01 | EP-27 | WF01 creates or matches a case from any channel, classifies severity and… | B: 086–089 | Yes | Release 3+ | not stated | Part-11-2a |
| US-27-YB02 | EP-27 | WF02 proposes a grounded fix and executes only actions on the approved… | B: 086–089 | Yes | Release 3+ | not stated | Part-11-2a |
| US-27-YB03 | EP-27 | WF03 calculates SLA deadlines from the entitlement and policy, alerts risk and… | B: 086–089 | Yes | Release 3+ | not stated | Part-11-2a |
| US-27-YB04 | EP-27 | WF04 analyzes resolved cases for recurring causes and recommends corrective… | B: 086–089 | Yes | Release 3+ | not stated | Part-11-2a |
| US-28-YB01 | EP-28 | WF01 generates marketing image variants from an approved brand brief, checks… | B: 066–070 | Yes | Release 3+ | not stated | Part-11-2a |
| US-28-YB02 | EP-28 | WF02 builds a storyboard and video draft from approved product facts | B: 066–070 | Yes | Release 3+ | not stated | Part-11-2a |
| US-28-YB03 | EP-28 | WF03 localizes approved assets: translation with glossary (AU-076), captions… | B: 066–070 | Yes | Release 3+ | not stated | Part-11-2a |
| US-28-YB04 | EP-28 | WF04 records a creative QA record (rights evidence, licence, claim validation… | B: 066–070 | Yes | Release 3+ | not stated | Part-11-2a |
| US-28-YB05 | EP-28 | Creative assets are metered per creative asset with a hard budget per provider | B: 066–070 | Yes | Release 3+ | not stated | Part-11-2a |
| US-29-YB01 | EP-29 | Service, workflow and bundle registry | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-29-YB02 | EP-29 | Foundation inclusion and selection modes | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-29-YB03 | EP-29 | Per-action SKU entitlement in the PDP | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-29-YB04 | EP-29 | Meters, caps and commercial model | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-29-YB05 | EP-29 | Migration and legacy entitlements | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-29-YB06 | EP-29 | Event envelope, idempotency and recovery | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-29-YB07 | EP-29 | Agent identity, interoperability and model portability | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-29-YB08 | EP-29 | Side-effect class and autonomy cap | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-29-YB09 | EP-29 | First value, enhancement metrics and outcome acceptance | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-29-YB10 | EP-29 | Shared engines | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-29-YB11 | EP-29 | Public service catalogue projection | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-29-YB12 | EP-29 | Readiness gate and catalogue administration | B: 001–030 | Yes | Not stated | not stated | Part-11-2a |
| US-30-ZN01 | EP-30 | Investment product provisioning and SKU entitlement gate | N: 001–010, 101–108, 121–124, 129–132, 137–140, 145–148 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-30-ZN02 | EP-30 | Securities rule-pack activation gate consumer (AU-201) | N: 019, 101–112, 117–120, 125–128, 141–148 | Yes | Release 2 | 5–8 | Part-11-16e |
| US-30-ZN03 | EP-30 | Investor-mode public storefront W55–W74 (neutral) | N: 011–018, 101–108, 117–120, 133–136, 141–148 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-30-ZN04 | EP-30 | Investor-data privacy, DSR and residency | N: 117–124, 129–136, 145–148 | Yes | Release 2 | 5–8 | Part-11-16e |
| US-30-ZN05 | EP-30 | Funding route and opportunity discovery with evidence (INV-SVC-01 WF01–WF03) | N: 031, 101–104, 109–112, 117–120, 133–140, 145–148 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-30-ZN06 | EP-30 | Continuous funding signal detection (INV-SVC-01-WF04) | N: 032, 101–120, 137–140, 145–148 | Yes | Release 3+ | 5–8 | Part-11-16e |
| US-30-ZN07 | EP-30 | Mandate fit and deterministic eligibility screening (INV-SVC-02 WF01–WF03) | N: 033–034, 105–112, 117–120, 125–128, 137–140, 145–148 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-30-ZN08 | EP-30 | Explainable investor propensity (INV-SVC-02-WF04) | N: 035, 105–112, 117–124, 129–132, 137–148 | Yes | Release 3+ | 5–8 | Part-11-16e |
| US-30-ZN09 | EP-30 | Investor representative contact intelligence (INV-SVC-03) | N: 036–037, 105–112, 117–148 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-30-ZN10 | EP-30 | Investor email drafting with the securities communication guard (INV-SVC-04-WF01) | N: 038, 109–120, 125–128, 137–148 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-30-ZN11 | EP-30 | Controlled investor email dispatch under the securities gate (INV-SVC-04-WF02) | N: 039, 101–124, 137–148 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-30-ZN12 | EP-30 | Delivery processing and sender health (INV-SVC-04 WF03–WF04) | N: 040, 113–116, 121–124, 141–148 | Yes | Release 2 | 5–8 | Part-11-16e |
| US-30-ZN13 | EP-30 | WhatsApp investor engagement (INV-SVC-05) | N: 041–042, 113–124, 141–148 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-30-ZN14 | EP-30 | Investor follow-up sequences with caps and offer-state stops (INV-SVC-06) | N: 043–044, 113–116, 121–124, 145–148 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-30-ZN15 | EP-30 | Investor conversation, objections and human handover (INV-SVC-07 WF01–WF03) | N: 045–047, 105–120, 125–128, 137–140, 145–148 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-30-ZN16 | EP-30 | Multilingual multimodal enquiry handling (INV-SVC-07-WF04) | N: 047, 113–120, 125–132, 145–148 | Yes | Release 3+ | 5–8 | Part-11-16e |
| US-30-ZN17 | EP-30 | Investor meetings, briefs and recording consent (INV-SVC-08 WF01–WF03) | N: 048–049, 113–116, 129–132, 145–148 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-30-ZN18 | EP-30 | Pitch rehearsal and post-meeting intelligence (INV-SVC-08-WF04) | N: 049, 113–116, 129–132, 145–148 | Yes | Release 3+ | 3–5 | Part-11-16e |
| US-31-ZN01 | EP-31 | Offering registration and counsel sign-off per jurisdiction (A232) | N: 025 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-31-ZN02 | EP-31 | Investor eligibility gate and KYC/AML hand-off (W76, A230) | N: 016, 020, 024 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-31-ZN03 | EP-31 | Deterministic funding scenario calculator (INV-SVC-09-WF01) | N: 050, 133 | Yes | Release 2 | 3–5 | Part-11-16e |
| US-31-ZN04 | EP-31 | Pitch narrative drafting and disclosure consistency (INV-SVC-09 WF02–WF04) | N: 051–052, 134–136 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-31-ZN05 | EP-31 | Data-room document intake and readiness (INV-SVC-10 WF01, WF04) | N: 053, 137, 140 | Yes | Release 2 | 5–8 | Part-11-16e |
| US-31-ZN06 | EP-31 | Gated data-room access and invited-investor room (INV-SVC-10-WF02, W75) | N: 015, 022, 054, 138 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-31-ZN07 | EP-31 | Diligence Q&A with fair disclosure (INV-SVC-10-WF03) | N: 055, 139 | Yes | Release 2 | 5–8 | Part-11-16e |
| US-31-ZN08 | EP-31 | Terms and agreements from counsel-approved templates (INV-SVC-11-WF01) | N: 056, 141 | Yes | Release 2 | 5–8 | Part-11-16e |
| US-31-ZN09 | EP-31 | Formal offer issue under caps and two-person approval (INV-SVC-11-WF02) | N: 057, 142 | Yes | Release 2 | 13 | Part-11-16e |
| US-31-ZN10 | EP-31 | Application, e-signature and acceptance (INV-SVC-11-WF03) | N: 058, 143 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-31-ZN11 | EP-31 | Term-sheet comparison (INV-SVC-11-WF04) | N: 059, 144 | Yes | Release 3+ | 5–8 | Part-11-16e |
| US-31-ZN12 | EP-31 | Receipt import and verification (INV-SVC-12-WF01) | N: 060, 145 | Yes | Release 2 | 5–8 | Part-11-16e |
| US-31-ZN13 | EP-31 | Atomic allocation and exceptions (INV-SVC-12-WF02) | N: 061, 146 | Yes | Release 2 | 8–13 | Part-11-16e |
| US-31-ZN14 | EP-31 | Discrepancies, anomalies and statutory timers (INV-SVC-12 WF03–WF04) | N: 062, 147–148 | Yes | Release 2 | 5–8 | Part-11-16e |
| US-31-ZN15 | EP-31 | Kill switch, revocation and mandate boundary | N: 027, 030 | Yes | Release 2 | 5–8 | Part-11-16e |
| US-31-ZN16 | EP-31 | No-AI-advice evaluation suite EVAL-N-ADV | — | Yes | Release 2 | 5–8 | Part-11-16e |
| US-32-ZO01 | EP-32 | Closing readiness and authorised closing record | O: 013 | Yes | Release 2 | 5–8 | Part-11-16d |
| US-32-ZO02 | EP-32 | Statutory filing tasks and regulatory deadline monitoring | O: 013 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-32-ZO03 | EP-32 | Investor update with figure tie-out and rights-scoped dispatch | O: 015 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-32-ZO04 | EP-32 | Investor onboarding, obligations and use-of-funds milestones | O: 015 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-32-ZO05 | EP-32 | Fundraising pipeline stage gates and next actions | O: 017 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-32-ZO06 | EP-32 | Probability-weighted forecast and bottleneck analytics | O: 017 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-32-ZO07 | EP-32 | Signed private enquiry intake and routing | O: 019 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-32-ZO08 | EP-32 | Intake health monitoring and external AI-agent intake | O: 019 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-32-ZO09 | EP-32 | Single-SKU entitlement isolation for INV-SVC-13…24 | O: 013 | Yes | Release 2 | 5–8 | Part-11-16d |
| US-32-ZO10 | EP-32 | Investor portal: offer letter, application, payment instructions and holdings | O: 003–012 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-33-ZO01 | EP-33 | Grant eligibility, drafting and submission readiness | O: 021 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-33-ZO02 | EP-33 | Grant utilisation and milestone reporting | O: 021 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-33-ZO03 | EP-33 | Debt readiness, dossier, scenarios and covenant monitoring | O: 023 | Yes | Release 2 | 5–8 | Part-11-16d |
| US-33-ZO04 | EP-33 | Continuous readiness, burn and runway | O: 025 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-33-ZO05 | EP-33 | Cap-table reconciliation and authorised ownership change | O: 027 | Yes | Release 2 | 5–8 | Part-11-16d |
| US-33-ZO06 | EP-33 | ESG evidence and impact disclosure release | O: 029 | Yes | Release 2 | 5–8 | Part-11-16d |
| US-33-ZO07 | EP-33 | Cross-border requirement matrix and restriction routing | O: 031 | Yes | Release 2 | 5–8 | Part-11-16d |
| US-33-ZO08 | EP-33 | Dilution and instrument scenario modelling | O: 027 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-33-ZO09 | EP-33 | Board and shareholder meetings, notice, quorum and voting | O: 033 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-33-ZO10 | EP-33 | Decision tracking and governance information packs | O: 033 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-33-ZO11 | EP-33 | Investor verification and screening hand-off | O: 035 | Yes | Release 2 | 5–8 | Part-11-16d |
| US-33-ZO12 | EP-33 | Securities rule-pack registry, counsel sign-off and activation | O: 085–091 | Yes | Release 2 | 5–8 | Part-11-16d |
| US-33-ZO13 | EP-33 | Offer eligibility ledger and solicitation gate | O: 085–091 | Yes | Release 2 | 5–8 | Part-11-16d |
| US-33-ZO14 | EP-33 | Financial promotion review and legends | O: 003–012 | Yes | Release 2 | 3–5 | Part-11-16d |
| US-33-ZO15 | EP-33 | No personalised investment advice by AI | O: 085–091 | Yes | Release 2 | 5–8 | Part-11-16d |
| US-01-ZU01 | EP-01 | Product separation between Sales & Marketing and Investment Automation | A: 006 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-01-ZU02 | EP-01 | Region code on every tenant key and request-region check | E: 004–005 | Yes | Release 1 | 1–2 | Part-11-22 |
| US-01-ZU03 | EP-01 | Central authorisation with SKU dimension and job-scoped service principals | E: 021 | Yes | Release 1 | 1–2 | Part-11-22 |
| US-01-ZU04 | EP-01 | Portfolio aggregate grants and SIEM audit streaming | H: 016, 038 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-01-ZU05 | EP-01 | Canonical table names, tenant-context enforcement and tenant-pinned keys | I: 001, 004–005 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-01-ZU06 | EP-01 | SoD on role build and assignment, hash-chained audit and domain schema validation | I: 008–009, 011 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-01-ZU07 | EP-01 | Region-pinned database, exact money and approved FX rates | I: 013, 017–018 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-01-ZU08 | EP-01 | Audit sinks, reference-data governance and analytics tables | I: 025–026, 030 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-01-ZU09 | EP-01 | Immutable record versions and atomic usage reservation | I: 031 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-01-ZU10 | EP-01 | ENT-IDN-01…03 acceptance: SSO per tenant, verified domains and SCIM | K: 101–103 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-01-ZU11 | EP-01 | ENT-IDN-04…06 acceptance: MFA policy, session policy and break-glass | K: 104–106 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-01-ZU12 | EP-01 | ENT-ACC-01…03 acceptance: custom roles, SoD matrix and tamper-evident audit | K: 107–109 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-01-ZU13 | EP-01 | ENT-ACC-04…05 acceptance: SIEM streaming and just-in-time support access | K: 110–111 | Yes | Release 1 | 1–2 | Part-11-22 |
| US-01-ZU14 | EP-01 | ENT-DAT-02…03 acceptance: customer-managed keys and residency at onboarding | K: 120–121 | Yes | Release 1 | 1–2 | Part-11-22 |
| US-02-ZU01 | EP-02 | Divisions, brands, markets, channel accounts and offering lifecycle | A: 075–077, 079 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-02-ZU02 | EP-02 | Knowledge-chunk provenance, rights, freshness and quarantine | F: 031 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-03-ZU01 | EP-03 | Deny-reason precedence in the V12 order | E: 022 | Yes | Release 1 | 1–2 | Part-11-22 |
| US-03-ZU02 | EP-03 | Versioned jurisdiction packs, scoped consent ledger and regulatory clocks | F: 042, 044, 046 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-03-ZU03 | EP-03 | AI disclosure and machine-readable marking | F: 047 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-03-ZU04 | EP-03 | Compliance API routes: packs, preflight, consent, DSAR, incidents and cookies | H: 013 | Yes | Release 1 | 1–2 | Part-11-22 |
| US-03-ZU05 | EP-03 | Contact-data vendor activation gate: transfer register, DPA and CJ-GL-01 | H: 033 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-03-ZU06 | EP-03 | ENT-CMP-04…06 acceptance: DPA and sub-processors, DPIA and EU AI Act, accessibility report | K: 140–142 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-03-ZU07 | EP-03 | ENT-CMP-07…08 acceptance: approved legal set and counsel-reviewed market packs | K: 143–144 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-03-ZU08 | EP-03 | AI-assisted labelling of every Part 11.13 AI output | M: 100 | Yes | Release 3+ | 1–2 | Part-11-22 |
| US-04-ZU01 | EP-04 | AI transparency page, AI labels, region pinning and private customer data | A: 054, 114–116 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-04-ZU02 | EP-04 | Context budgeting, multimodal cost tiers and the AI step inventory | A: 113, 118 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-04-ZU03 | EP-04 | Launch-language evaluation slices gate a locale | A: 117 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-04-ZU04 | EP-04 | AIX-01, 04, 06: step classification, prompt registry and regression gate | F: 001, 004, 006 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-04-ZU05 | EP-04 | AIX-07…09: calibrated judges, untrusted-content isolation and reader/actor separation | F: 007–009 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-04-ZU06 | EP-04 | AIX-10…12: output handling, claims and citations, per-call AI metering | F: 010–012 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-04-ZU07 | EP-04 | AIX-13…15: tenant AI budgets, cost per accepted result and scoped caching | F: 013–015 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-04-ZU08 | EP-04 | AIX-17…19: provider data handling, drift monitoring and multilingual gates | F: 017–019 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-04-ZU09 | EP-04 | AIX-20 kill switch and CTRL-AI-01…02 delimiting and normalisation | F: 020–022 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-04-ZU10 | EP-04 | CTRL-AI-03…05: injection classifier, tool isolation and output validation | F: 023–025 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-04-ZU11 | EP-04 | CTRL-AI-06…08: no secrets in context, tenant-filtered retrieval and signed agent mandates | F: 026–028 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-04-ZU12 | EP-04 | CTRL-AI-09 logging, ai_usage_event metering and keyed evaluation runs | F: 029–030, 032 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-04-ZU13 | EP-04 | Suite replay on change, per-run agent record and two-level AGT registry | F: 033, 036, 039 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-04-ZU14 | EP-04 | Scoped AI cache key and invalidation contract | F: 049 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-04-ZU15 | EP-04 | Optimisation API routes: preflight, cost, health, feedback and model evaluations | H: 017 | Yes | Release 2 | 3–5 | Part-11-22 |
| US-04-ZU16 | EP-04 | Vector column and HNSW index behind the embedding-model gate | I: 016 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-04-ZU17 | EP-04 | Metering of Part 11.13 agents to Ledger B line B25 with a hard cap | M: 099 | Yes | Release 3+ | 1–2 | Part-11-22 |
| US-05-ZU01 | EP-05 | Offering-specific audiences with market eligibility and source rights | A: 078 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-08-ZU01 | EP-08 | DLT and preference-registry scrub for promotional SMS and voice | F: 045 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-08-ZU02 | EP-08 | Multiple channel accounts per company with scoped sender identities | H: 024–025 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-12-ZU01 | EP-12 | Consent-aware acquisition analytics | I: 045 | Yes | Release 1 | 3–5 | Part-11-22 |
| US-15-ZU01 | EP-15 | Distinct ledgers, native-currency reporting and cost allocation | E: 079–082 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-16-ZU01 | EP-16 | CSAT, CES and NPS at defined milestones | A: 153 | Yes | Release 2 | 3–5 | Part-11-22 |
| US-16-ZU02 | EP-16 | First-value milestone, activation checklist and success plan per SKU | A: 160–161 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-16-ZU03 | EP-16 | Customer health score and underused-service detection | A: 162–163 | Yes | Release 3+ | 1–2 | Part-11-22 |
| US-16-ZU04 | EP-16 | Connector expiry alerts, customer value report and customer-controlled schedules | A: 164–166 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-16-ZU05 | EP-16 | Complementary-service recommendations, grounded help and enterprise success reviews | A: 167, 169–170 | Yes | Release 3+ | 8–13 | Part-11-22 |
| US-16-ZU06 | EP-16 | ENT-BIZ-04…05 acceptance: success playbooks and partner/reseller programme | K: 156–157 | Yes | Release 3+ | 5–8 | Part-11-22 |
| US-17-ZU01 | EP-17 | Native-currency integrity and reconciled drill-down | A: 036, 124 | Yes | Release 1 | 1–2 | Part-11-22 |
| US-17-ZU02 | EP-17 | Nine optimisation perspectives with role visibility | A: 121 | Yes | Release 2 | 3–5 | Part-11-22 |
| US-17-ZU03 | EP-17 | Context filters and cascading filter semantics | A: 122–123 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-17-ZU04 | EP-17 | Business metrics API with scoped dimensions and approved rates | H: 015 | Yes | Release 1 | 3–5 | Part-11-22 |
| US-17-ZU05 | EP-17 | Fourteen management views with production metrics | I: 043 | Yes | Release 1 | 3–5 | Part-11-22 |
| US-18-ZU01 | EP-18 | Nine-check preflight, confidence-floor routing and safe cancellation | D: 007–008, 012 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-18-ZU02 | EP-18 | Configuration diff, rollback as a new draft and snapshot protection | E: 039 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-18-ZU03 | EP-18 | Circuit breakers, backpressure and dependency-aware degradation | E: 096, 100–101 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-18-ZU04 | EP-18 | Immutable effect intent, one definition per workflow version and reusable child workflows | F: 034, 040–041 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-18-ZU05 | EP-18 | Competing actions grouped for reviewer disposition | F: 048 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-18-ZU06 | EP-18 | Vault-only connector secrets, per-connector rate limits and health dashboards | H: 019–021 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-18-ZU07 | EP-18 | Incremental provider sync and provider shortlist rationalisation | H: 026–027 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-18-ZU08 | EP-18 | ENT-INT-01…03 acceptance: adapter contract, vault secrets and resilient writes | K: 124–126 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-18-ZU09 | EP-18 | ENT-INT-04 acceptance: connector health, sync lag and alerts | K: 127 | Yes | Release 1 | 1–2 | Part-11-22 |
| US-18-ZU10 | EP-18 | UX rules G01–G04: workspace and portal scope, contextual and capability filters | L: 001–004 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-18-ZU11 | EP-18 | UX rules G05–G08: omnichannel policy, workflow operations, record linkage and AI evidence | L: 005–008 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-18-ZU12 | EP-18 | UX rules G09–G12: financial controls, approval and audit, data lifecycle and navigation | L: 009–012 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-18-ZU13 | EP-18 | UX rules G13–G15: UI states, simulation safeguards and service lifecycle | L: 013–015 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-18-ZU14 | EP-18 | UX business requirements UX-BR-02…05 on the 36-tenant fixture | L: 017–020 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-19-ZU01 | EP-19 | Workflow output previews, maturity assessment and controlled sandbox | A: 058, 060–061 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-19-ZU02 | EP-19 | TCO estimator and ROI sensitivity | A: 059 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-19-ZU03 | EP-19 | Localised help centre and in-product guides | A: 144 | Yes | Release 2 | 3–5 | Part-11-22 |
| US-19-ZU04 | EP-19 | Positioning and segment evidence without superiority claims | A: 222 | Yes | Release 2 | 3–5 | Part-11-22 |
| US-19-ZU05 | EP-19 | PWA offline boundary | I: 059 | Yes | Release 2 | 3–5 | Part-11-22 |
| US-20-ZU01 | EP-20 | Catalogue versioning, alias map and bundle expansion | A: 004–005 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-20-ZU02 | EP-20 | Signed SKU expansion, tenant lifecycle and consumption forecast | A: 012–013, 015 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-20-ZU03 | EP-20 | Bring-your-own provider and delivery models | A: 023–024 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-20-ZU04 | EP-20 | Transparent pricing, TCO and contribution, and billing disputes | A: 030–031, 034 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-20-ZU05 | EP-20 | Per-SKU cost model, price floor and SKU meter registry | A: 032–033, 035 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-20-ZU06 | EP-20 | Operator acquisition tenant and the 14 customer types | A: 073, 080 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-20-ZU07 | EP-20 | Progressive onboarding with session and draft recovery | A: 091–092 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-20-ZU08 | EP-20 | Business & Organization Management Centre, templates and cross-device handoff | A: 093–095 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-20-ZU09 | EP-20 | Per-SKU workflow SLA matrix and customer responsibilities schedule | A: 145–146 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-20-ZU10 | EP-20 | Ethical cancellation and win-back | A: 168 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-20-ZU11 | EP-20 | BR-V12 capability register (1/3): identity, access, developer platform, data ownership | A: 180–183 | Yes | Release 3+ | 2–3 | Part-11-22 |
| US-20-ZU12 | EP-20 | BR-V12 capability register (2/3): ecosystem, security, legal readiness, global reach | A: 184–187 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-20-ZU13 | EP-20 | BR-V12 capability register (3/3): dependable service and commercial operations | A: 188–189 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-20-ZU14 | EP-20 | SKU release groups mapped to waves | A: 192 | Yes | Release 2 | 3–5 | Part-11-22 |
| US-20-ZU15 | EP-20 | Eight-stage wizard, server-backed drafts, customer types and country model | E: 032–034, 036 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-20-ZU16 | EP-20 | Region, language and IANA timezone per market with DST | E: 037 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-20-ZU17 | EP-20 | SKU, workflow-version, bundle and foundation registries | E: 045–048 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-20-ZU18 | EP-20 | Engines register, legacy capability map and public projection allowlist | E: 049–051 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-20-ZU19 | EP-20 | Tenant lifecycle, portability and offboarding | E: 058, 127 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-20-ZU20 | EP-20 | Plan-change preview, effective date and proration | E: 062 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-20-ZU21 | EP-20 | Refunds, credit notes and billing disputes | E: 064, 078, 084 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-20-ZU22 | EP-20 | Revenue recognition schedule and reconciliation jobs RJ-01…06 | E: 077, 086 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-20-ZU23 | EP-20 | Consumption forecast, quota alerts and TTFV playbooks | E: 083, 089 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-20-ZU24 | EP-20 | Per-SKU service sheet, partner model and procurement pack | E: 085, 087–088 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-20-ZU25 | EP-20 | Appendix A/A2 API contract conventions and one authoritative registry | H: 008–010 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-20-ZU26 | EP-20 | Tenant and company configuration contracts, BYO provider accounts and tier planning | H: 014, 028–029 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-20-ZU27 | EP-20 | Self-service operations, cross-device handoff contract and customer-managed keys | H: 030, 034, 040 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-20-ZU28 | EP-20 | Invoice preview with per-line tax determination | H: 039 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-20-ZU29 | EP-20 | Synthetic-data sandboxes and verified webhook endpoints | I: 022, 024 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-20-ZU30 | EP-20 | Per-SKU service schedule | K: 014 | Yes | Release 2 | 3–5 | Part-11-22 |
| US-20-ZU31 | EP-20 | ENT-API-01…03 acceptance: scoped keys, client credentials and rate limits | K: 112–114 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-20-ZU32 | EP-20 | ENT-API-04…06 acceptance: versioning, signed webhooks and SDKs | K: 115–117 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-20-ZU33 | EP-20 | ENT-API-07 acceptance: developer portal and sandbox access | K: 118 | Yes | Release 1 | 1–2 | Part-11-22 |
| US-20-ZU34 | EP-20 | ENT-DAT-01, 04, 05 acceptance: tenant export, synthetic sandboxes and promotion | K: 119, 122–123 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-20-ZU35 | EP-20 | ENT-BIZ-01…03 acceptance: billing chain, approved price book and signed order forms | K: 153–155 | Yes | Release 3+ | 8–13 | Part-11-22 |
| US-20-ZU36 | EP-20 | ENT-BIZ-06 acceptance: enterprise procurement pack | K: 158 | Yes | Release 3+ | 3–5 | Part-11-22 |
| US-20-ZU37 | EP-20 | UX-BR-01 configuration-driven onboarding on the non-production fixture | L: 016 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-21-ZU01 | EP-21 | SLA tier templates, severity model and tiered support desk | A: 140–141, 143 | Yes | Release 2 | 2–3 | Part-11-22 |
| US-21-ZU02 | EP-21 | Independent status page and recovery objectives per data class | A: 142, 147 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-21-ZU03 | EP-21 | KPI register, metric registry, zero-denominator rules and business objectives | A: 150–152, 220 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-21-ZU04 | EP-21 | V12 phase map and P0/P1/P2 priority gating | A: 190–191 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-21-ZU05 | EP-21 | Readiness register, acceptance-ID aliases and per-SKU acceptance record | A: 200–202 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-21-ZU06 | EP-21 | Decision ownership register | A: 210 | Yes | Release 1 | 3–5 | Part-11-22 |
| US-21-ZU07 | EP-21 | Pilot outcome hypotheses | A: 221 | Yes | Release 3+ | 3–5 | Part-11-22 |
| US-21-ZU08 | EP-21 | Synthetic probes, chaos tests, scalability tests and safe autoscaling | E: 102–103, 112–113 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-21-ZU09 | EP-21 | Compute benchmark BM-01 | E: 114 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-21-ZU10 | EP-21 | GO-01…08 sequence, per-SKU release gates and maintenance cadence | E: 130, 132–134 | Yes | Release 1 | 2–3 | Part-11-22 |
| US-21-ZU11 | EP-21 | Optimisation release process | E: 135 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-21-ZU12 | EP-21 | Idle-resource detection and paid-plugin replacement register | H: 031–032 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-21-ZU13 | EP-21 | Locales list and operational incident declaration contracts | H: 041 | Yes | Release 2 | 1–2 | Part-11-22 |
| US-21-ZU14 | EP-21 | Load profiles, penetration tests and bug-bounty programme | I: 041, 053–054 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-21-ZU15 | EP-21 | Encryption and key rotation, secrets rotation and SEC-08…13 evidence | I: 055–056, 058 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-21-ZU16 | EP-21 | Release evidence matrix: SKU → workflow → step → test → task → release | J: 006 | Yes | Release 2 | 3–5 | Part-11-22 |
| US-21-ZU17 | EP-21 | 24×7 human on-call for SEV1 and SEV2 | K: 004 | Yes | Release 2 | 3–5 | Part-11-22 |
| US-21-ZU18 | EP-21 | Alert set, training-card aliases and source-archive register | K: 008, 013, 023 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-21-ZU19 | EP-21 | ENT-INT-05 acceptance: connector activation gate | K: 128 | Yes | Release 1 | 1–2 | Part-11-22 |
| US-21-ZU20 | EP-21 | ENT-SEC-01…03 acceptance: secure SDLC, SBOM and remediation SLAs | K: 129–131 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-21-ZU21 | EP-21 | ENT-SEC-04…06 acceptance: penetration tests, bug bounty and encryption | K: 132–134 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-21-ZU22 | EP-21 | ENT-SEC-07…08 acceptance: secrets management and 24×7 security monitoring | K: 135–136 | Yes | Release 1 | 5–8 | Part-11-22 |
| US-30-ZU01 | EP-30 | Solicitation guard and no AI investment advice (SEC-CTL-N-03, N-05) | N: 021, 023 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-31-ZU01 | EP-31 | Route caps, no custody and cross-border hold (SEC-CTL-N-09, N-11, N-14) | N: 026, 028–029 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-32-ZU01 | EP-32 | INV action envelope and per-action entitlement for INV-SVC-13…24 | O: 001–002 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-32-ZU02 | EP-32 | Allotment clock and refund task from each receipt | O: 014 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-32-ZU03 | EP-32 | Rights-scoped personalisation of investor updates | O: 016 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-32-ZU04 | EP-32 | Next actions that respect the round's solicitation mode | O: 018 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-32-ZU05 | EP-32 | Enquiries from markets without an active pack stay enquiries | O: 020 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-32-ZU06 | EP-32 | INV-SVC-13 Legal Investment Closing & Statutory Task Automation: workflow contracts… | O: 037–040 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-32-ZU07 | EP-32 | INV-SVC-14 Investor Reporting & Capital Lifecycle Automation: workflow contracts WF01–WF04 | O: 041–044 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-32-ZU08 | EP-32 | INV-SVC-15 Fundraising CRM, Pipeline & Analytics Automation: workflow contracts WF01–WF04 | O: 045–048 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-32-ZU09 | EP-32 | INV-SVC-16 Private Website Enquiry & Integration Automation: workflow contracts WF01–WF04 | O: 049–052 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-33-ZU01 | EP-33 | Grant submission readiness with a human-approved package hash | O: 022 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-33-ZU02 | EP-33 | Covenant alerts and checklist-scoped dossier sharing | O: 024 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-33-ZU03 | EP-33 | Reproducible readiness scores labelled as internal | O: 026 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-33-ZU04 | EP-33 | Golden-fixture scenario and conversion calculations | O: 028 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-33-ZU05 | EP-33 | Commitment deviations create corrective actions | O: 030 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-33-ZU06 | EP-33 | Deterministic cross-border restriction holds | O: 032 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-33-ZU07 | EP-33 | Rights-scoped governance packs with redaction | O: 034 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-33-ZU08 | EP-33 | Sanctions possible matches held, true matches blocked, no tip-off | O: 036 | Yes | Release 2 | 5–8 | Part-11-22 |
| US-33-ZU09 | EP-33 | INV-SVC-17 Grant & Non-Dilutive Funding Application Automation: workflow contracts… | O: 053–056 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-33-ZU10 | EP-33 | INV-SVC-18 Debt Financing & Credit Readiness Automation: workflow contracts WF01–WF04 | O: 057–060 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-33-ZU11 | EP-33 | INV-SVC-19 Continuous Fundraising Readiness & Financial Intelligence Automation: workflow… | O: 061–064 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-33-ZU12 | EP-33 | INV-SVC-20 Cap Table & Ownership Intelligence Automation: workflow contracts WF01–WF04 | O: 065–068 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-33-ZU13 | EP-33 | INV-SVC-21 ESG, Climate & Impact Funding Intelligence Automation: workflow contracts… | O: 069–072 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-33-ZU14 | EP-33 | INV-SVC-22 Cross-Border Funding Compliance Coordination Automation: workflow contracts… | O: 073–076 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-33-ZU15 | EP-33 | INV-SVC-23 Board & Shareholder Governance Automation: workflow contracts WF01–WF04 | O: 077–080 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-33-ZU16 | EP-33 | INV-SVC-24 Investor Identity, Ownership & Risk Evidence Automation: workflow contracts… | O: 081–084 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-34-ZU01 | EP-34 | ENT-CMP-01…03: SOC 2, ISO/IEC 27001, 27701 and 42001 in the decided sequence | K: 137–139 | Yes | Release 2 | 8–13 | Part-11-22 |
| US-34-ZU02 | EP-34 | ENT-GLB-01…03: internationalisation framework, staged locales and right-to-left | K: 145–147 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-34-ZU03 | EP-34 | ENT-GLB-04…06: locale formats, tax-engine abstraction and multi-currency billing | K: 148–150 | Yes | Release 1 | 8–13 | Part-11-22 |
| US-34-ZU04 | EP-34 | ENT-GLB-07…08: regional messaging providers and region expansion plan | K: 151–152 | Yes | Release 2 | 5–8 | Part-11-22 |

### 11.22.5.7 Story counts and story points per epic and per release

**Basis.** Baseline and V12 story points are taken from the stories where stated (Fibonacci ranges, `Points` or combined `Priority · Wave · Points` fields). V12 stories that state no points (story tables and paragraphs in Parts 11.1–11.13) are imputed at **3–8 SP** each [ASSUMPTION-1142]. Person-days use Part 5.1a §5.5.1: low = SP_low × 0.5, high = SP_high × 1.0, central = SP_mid × 0.7. Release buckets per §11.22.5.1 [ASSUMPTION-1145]. These are planning totals for Part 11.20, not a re-baseline of Ledger A.

| Epic | Baseline stories | Baseline SP (stated; n stated) | V12 stories | V12 SP (stated + imputed; n stated) | New ZU stories | New SP | All stories | All SP (low–high) | Central pd |
|---|---|---|---|---|---|---|---|---|---|
| EP-01 | 35 | 75–103 (27) | 36 | 133–292 (9) | 14 | 57–93 | 85 | 265–488 | 264 |
| EP-02 | 10 | 29–43 (10) | 5 | 22–40 (2) | 2 | 7–11 | 17 | 58–94 | 53 |
| EP-03 | 17 | 58–79 (17) | 17 | 53–128 (2) | 8 | 28–46 | 42 | 139–253 | 137 |
| EP-04 | 29 | 95–115 (26) | 22 | 77–169 (6) | 17 | 102–166 | 68 | 274–450 | 253 |
| EP-05 | 21 | 74–107 (21) | 8 | 24–64 (0) | 1 | 5–8 | 30 | 103–179 | 99 |
| EP-06 | 14 | 51–63 (14) | 7 | 23–56 (1) | 0 | 0–0 | 21 | 74–119 | 68 |
| EP-07 | 15 | 52–66 (15) | 5 | 20–42 (2) | 0 | 0–0 | 20 | 72–108 | 63 |
| EP-08 | 23 | 71–94 (23) | 19 | 65–150 (5) | 2 | 10–16 | 44 | 146–260 | 142 |
| EP-09 | 12 | 28–39 (12) | 4 | 12–32 (0) | 0 | 0–0 | 16 | 40–71 | 39 |
| EP-10 | 8 | 27–35 (8) | 3 | 9–24 (0) | 0 | 0–0 | 11 | 36–59 | 33 |
| EP-11 | 15 | 40–52 (15) | 18 | 59–146 (2) | 0 | 0–0 | 33 | 99–198 | 104 |
| EP-12 | 21 | 86–105 (21) | 13 | 41–104 (1) | 1 | 3–5 | 35 | 130–214 | 120 |
| EP-13 | 17 | 46–61 (17) | 13 | 44–106 (2) | 0 | 0–0 | 30 | 90–167 | 90 |
| EP-14 | 18 | 47–63 (17) | 18 | 80–167 (6) | 0 | 0–0 | 36 | 127–230 | 125 |
| EP-15 | 14 | 30–47 (14) | 13 | 56–119 (4) | 1 | 2–3 | 28 | 88–169 | 90 |
| EP-16 | 23 | 68–84 (23) | 19 | 70–149 (5) | 6 | 26–43 | 48 | 164–276 | 154 |
| EP-17 | 36 | 115–134 (29) | 18 | 73–148 (5) | 5 | 11–19 | 59 | 199–301 | 175 |
| EP-18 | 26 | 86–110 (25) | 43 | 184–346 (24) | 14 | 54–86 | 83 | 324–542 | 303 |
| EP-19 | 25 | 80–98 (24) | 43 | 141–336 (4) | 5 | 18–30 | 73 | 239–464 | 246 |
| EP-20 | 33 | 90–113 (25) | 64 | 240–505 (16) | 37 | 123–201 | 134 | 453–819 | 445 |
| EP-21 | 49 | 98–127 (31) | 40 | 141–303 (11) | 22 | 86–140 | 111 | 325–570 | 313 |
| EP-22 | 0 | 0–0 (0) | 22 | 144–252 (16) | 0 | 0–0 | 22 | 144–252 | 139 |
| EP-23 | 0 | 0–0 (0) | 5 | 17–40 (1) | 0 | 0–0 | 5 | 17–40 | 20 |
| EP-24 | 0 | 0–0 (0) | 12 | 53–108 (5) | 0 | 0–0 | 12 | 53–108 | 56 |
| EP-25 | 0 | 0–0 (0) | 4 | 12–32 (0) | 0 | 0–0 | 4 | 12–32 | 15 |
| EP-26 | 0 | 0–0 (0) | 4 | 12–32 (0) | 0 | 0–0 | 4 | 12–32 | 15 |
| EP-27 | 0 | 0–0 (0) | 4 | 12–32 (0) | 0 | 0–0 | 4 | 12–32 | 15 |
| EP-28 | 0 | 0–0 (0) | 5 | 15–40 (0) | 0 | 0–0 | 5 | 15–40 | 19 |
| EP-29 | 0 | 0–0 (0) | 12 | 36–96 (0) | 0 | 0–0 | 12 | 36–96 | 46 |
| EP-30 | 0 | 0–0 (0) | 18 | 121–196 (18) | 1 | 5–8 | 19 | 126–204 | 115 |
| EP-31 | 0 | 0–0 (0) | 16 | 104–160 (16) | 1 | 8–13 | 17 | 112–173 | 100 |
| EP-32 | 0 | 0–0 (0) | 10 | 34–56 (10) | 9 | 57–92 | 19 | 91–148 | 84 |
| EP-33 | 0 | 0–0 (0) | 15 | 61–99 (15) | 16 | 104–168 | 31 | 165–267 | 151 |
| EP-34 | 0 | 0–0 (0) | 0 | 0–0 (0) | 4 | 29–47 | 4 | 29–47 | 27 |
| **Total** | **461** | **1346–1738 (414)** | **555** | **2188–4569 (188)** | **166** | **735–1195** | **1182** | **4269–7502** | **4120** |

#### 11.22.5.7.1 Per release

| Release | Baseline stories (SP stated) | V12 stories (SP stated + imputed) | New ZU stories (SP) | All stories | All SP | pd low–high · central |
|---|---|---|---|---|---|---|
| Release 1 | 232 (528–813) | 44 (213–331) | 57 (228–369) | 333 | 969–1513 | 484–1513 · 869 |
| Release 2 | 91 (203–305) | 115 (687–1065) | 100 (475–773) | 306 | 1365–2143 | 682–2143 · 1228 |
| Release 3+ | 71 (408–413) | 110 (340–874) | 9 (32–53) | 190 | 780–1340 | 390–1340 · 742 |
| Not stated | 67 (207–207) | 286 (948–2299) | 0 (0–0) | 353 | 1155–2506 | 578–2506 · 1281 |

**Not stated.** Stories whose release or wave is not written in their source (mostly the V12 story tables of Parts 11.2a, 11.6b, 11.7c and 11.13b) are scheduled by Part 11.20 from their FRs; the new ZU stories always state a release.

#### 11.22.5.7.2 New ZU stories per epic and release

| Epic | Release 1 (stories · SP) | Release 2 | Release 3+ | Total |
|---|---|---|---|---|
| EP-01 | 14 · 57–93 | — | — | 14 · 57–93 |
| EP-02 | 1 · 2–3 | 1 · 5–8 | — | 2 · 7–11 |
| EP-03 | 5 · 14–23 | 2 · 13–21 | 1 · 1–2 | 8 · 28–46 |
| EP-04 | 2 · 7–11 | 14 · 94–153 | 1 · 1–2 | 17 · 102–166 |
| EP-05 | — | 1 · 5–8 | — | 1 · 5–8 |
| EP-08 | 1 · 5–8 | 1 · 5–8 | — | 2 · 10–16 |
| EP-12 | 1 · 3–5 | — | — | 1 · 3–5 |
| EP-15 | — | 1 · 2–3 | — | 1 · 2–3 |
| EP-16 | — | 3 · 12–20 | 3 · 14–23 | 6 · 26–43 |
| EP-17 | 3 · 7–12 | 2 · 4–7 | — | 5 · 11–19 |
| EP-18 | 5 · 18–29 | 9 · 36–57 | — | 14 · 54–86 |
| EP-19 | — | 5 · 18–30 | — | 5 · 18–30 |
| EP-20 | 9 · 35–56 | 25 · 75–124 | 3 · 13–21 | 37 · 123–201 |
| EP-21 | 14 · 64–103 | 7 · 19–32 | 1 · 3–5 | 22 · 86–140 |
| EP-30 | — | 1 · 5–8 | — | 1 · 5–8 |
| EP-31 | — | 1 · 8–13 | — | 1 · 8–13 |
| EP-32 | — | 9 · 57–92 | — | 9 · 57–92 |
| EP-33 | — | 16 · 104–168 | — | 16 · 104–168 |
| EP-34 | 2 · 16–26 | 2 · 13–21 | — | 4 · 29–47 |

## 11.22.6 Conflicts and proposed resolutions

| Tag | Conflict | Sources | Proposed resolution | Status |
|---|---|---|---|---|
| CONFLICT-1140 | Role ID R21 means "agency / managed-service operator" in Part 2.6 §2.6.5.3.2 and "invited investor" in Part 11.16a | Part 2.6; Part 11.16a §11.16.5 | Keep R21 = agency operator (earlier definition); rename the invited-investor role to **R22** in the next consolidation of Part 11.14/11.16; until then this part writes "R21 (Part 11.16a)" for the investor and "R21 (Part 2.6)" for the agency operator. No story behaviour changes | Proposed (DEC-946) |
| CONFLICT-1149 | FR-V12-A-006 ("no investor entity, route, filter or term") and US-19-YG38 ("No investor / fundraising mode in the website") contradict DEC-783, which adopted investor mode and the Investment Automation product | Parts 11.1b, 11.7c; Part 11.14 DEC-783 | Read A-006 as **product separation**: separate product code, no implicit cross-product access, investor entities only in the INV namespace (US-01-ZU01); US-19-YG38 is superseded for the investor website W55–W74 and stays valid for the Sales & Marketing storefront | Resolved by DEC-947 under DEC-783 |

## 11.22.7 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-940 | Part 11.22 is the master story register for V12; coverage is computed by `u_01_inventory.py` and must stay at 100% of FR-V12 with a story that has AC (ADR-275) | Founder V12-B instruction (DEC-790/791), applied by Group U, 28 Nov 2026 | CI gate on Part 11 changes; register §11.22.3 regenerated |
| DEC-941 | FRs traced only to statement-only stories, and ENT trace requirements designed elsewhere, get **acceptance-binding** ZU stories (1–3 SP for AC, examples and test automation); the anchor keeps its build points | Founder V12-B instruction, applied by Group U | No double counting of build effort; every FR gains executable AC |
| DEC-942 | New epic **EP-34 Global expansion, certification and multi-market operations** for ENT-CMP-01…03 and ENT-GLB-01…08 | Founder decisions DEC-775/776, applied by Group U | Epic map extended to EP-34 |
| DEC-943 | Twelve persona journeys JN-01…JN-12 are acceptance journeys; their Scenario Outlines become end-to-end tests in Part 11.21; new personas P21–P23 adopted | Founder V12-B instruction, applied by Group U | E2E suite per persona; persona register extended |
| DEC-944 | Story release buckets follow §11.22.5.1 with the overrides of DEC-771…789; dates follow the work (DEC-770) | Founder decisions DEC-770…789 | Part 11.20 schedules ZU stories by bucket |
| DEC-945 | Combinatorial standard for stories: t = 3 for safety-, money- and law-critical models, t = 2 otherwise, exhaustive ≤ 64, baseline-allow rows, oracle by PDP precedence (ADR-276) | V12-B brief (permutations mandatory), applied by Group U | All Examples reproducible from seeds |
| DEC-946 | Proposed: invited-investor role renamed R22 at the next consolidation (CONFLICT-1140) | Proposed to the Part 11.14 owner (consolidation) | No behaviour change; naming only |
| DEC-947 | FR-V12-A-006 is read as product separation under DEC-783; US-19-YG38 superseded for the investor website (CONFLICT-1149) | Founder decision DEC-783 | US-01-ZU01 carries the amended acceptance |
| DEC-948 | Register wording "Pending Founder decision" in FR-V12-K-004, I-013, A-147 and the O-037…084 status texts is read as decided by DEC-771/772/773/783 (GAP-1148) | Founder decisions DEC-771…783 | Stories cite the deciding DEC |

## 11.22.8 Expert persona review

| Reviewer | Finding | Action taken |
|---|---|---|
| Chief Product Officer | 380 of 1,467 FR-V12 requirements (25.9%) had no executable acceptance; the riskiest (ENT controls, AI controls, securities controls) were among them | Every one now has a story with AC; ENT and AI control stories are Release 1 where DEC-784/785 require |
| Chief Product Officer | Investment Automation workflow requirements were traced only by workflow ID | ZU stories carry FR IDs; GAP-1146 asks Part 11.16d to add them |
| Principal Agile Product Owner | Acceptance bindings must not double-count build effort | DEC-941: bindings carry 1–3 SP; anchors keep build SP |
| Principal Agile Product Owner | Many V12 stories state no points or release | Totals impute 3–8 SP with the assumption logged; Part 11.20 schedules "Not stated" from FR waves |
| Business Systems Analyst | Hand-typed expected results in thousands of Examples rows would drift from the PDP order | ADR-276 oracle; regeneration is deterministic |
| Business Systems Analyst | Scenario Outline steps must reference every Examples column | Step templates per model reference every parameter; checked by build |
| UX researcher | Investor, invited-investor and partner journeys had no persona in the register | P21–P23 added with goals, pains and "never" rules |
| UX researcher | Journeys must include assistive technology and mobile variants | JN-11 and JN-05 variant models include assistive technology, 360 px and phone channels |
| QA Lead | 3-way arrays for law- and money-critical models are large | Kept at 5–6 dimensions per model; every t-tuple verified; counts printed per story |

## 11.22.9 Tags register

| Tag | Type | Statement | Where used | Status |
|---|---|---|---|---|
| CONFLICT-1140 | Conflict | R21 defined twice (agency operator, invited investor) | §11.22.4.3, §11.22.6, file e | Proposed resolution DEC-946 |
| RECOMMENDATION-1141 | Recommendation | Add personas P21 investor-relations user, P22 invited investor, P23 partner / reseller | File e | Adopted DEC-943 |
| ASSUMPTION-1142 | Assumption | Acceptance-binding stories 1–3 SP; V12 stories without stated points imputed at 3–8 SP for totals | §11.22.5.1, §11.22.5.7 | Open – replace with team estimates at refinement |
| GAP-1143 | Gap | 116 FRs were traced only to statement-only stories without AC | §11.22.2, §11.22.4.2 | Closed by acceptance-binding stories |
| GAP-1144 | Gap | 264 FRs had no story at all | §11.22.2, §11.22.3 | Closed by new stories |
| ASSUMPTION-1145 | Assumption | Release bucket mapping (W0–W3/R0–R1 → Release 1; W4–W5/R2 → Release 2; W6/A1–A3/R3–R5 → Release 3+) | §11.22.5.1 | Open – Part 11.20 confirms |
| RECOMMENDATION-1146 | Recommendation | Part 11.21 realises every EX row and journey row as a TC-V12-T test case; Part 11.16d adds FR IDs to EP-32/EP-33 story traces (GAP-1146 trace part) | §11.22.4.3, file e | Open |
| GAP-1146 | Gap | O-037…084 traced by workflow ID only | §11.22.4.3 | Closed here; source fix recommended |
| GAP-1147 | Gap | Six Part 11.6b agent stories have empty titles | §11.22.4.3 | Open (owner Part 11.6) |
| GAP-1148 | Gap | Stale "Pending Founder decision" wording in decided FR rows | §11.22.4.3, DEC-948 | Closed by DEC-948 reading |
| CONFLICT-1149 | Conflict | FR-V12-A-006 / US-19-YG38 versus DEC-783 | §11.22.6, US-01-ZU01 | Resolved DEC-947 |
| ASSUMPTION-1150 | Assumption | All fixtures are synthetic tenants, people and `example` domains | All story files | Closed |
| RECOMMENDATION-1151 | Recommendation | New epic EP-34 for certification and global expansion | §11.22.5.3 | Adopted DEC-942 |
| ASSUMPTION-1152 | Assumption | Role × permission merged into authority classes per Part 5.1a §5.6.2; other dimensions held at baseline per model | §11.22.5.2 | Closed (RBAC matrix test still exhaustive) |

## 11.22.10 Quality gate and status


## Quality gate: Batch 11.22f

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | **Pass** | Epic map rows computed from the inventory; every FR maps to an epic; every count printed by the scripts |
| 2 | Assumptions, gaps and conflicts tagged and logged | **Pass** | Tags from 1140–1159 only; register in §11.22.9 (last file of Batch 11.22) |
| 3 | IDs unique and consistent with earlier parts | **Pass** | US-<EP>-ZU<nn> unique per epic; AC and EX IDs derived; epics EP-01…EP-33 as defined; EP-34 new |
| 4 | No story lacks AC; no requirement lacks a test | **Pass** | 1467 / 1467 FR-V12 have a story with AC; every new story has Gherkin and a generated outline; journeys have E2E outlines |
| 5 | Negative, edge, security and accessibility cases covered | **Pass** | MAS-1…MAS-9 applied; @sec/@obs outlines; @a11y in website and UI stories |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | **N/A** | N/A – no new agents; AI stories reuse the registry, gateway and eval gates |
| 7 | Time-sensitive facts flagged "verify" with as-of date | **Pass** | No prices or model versions stated; regulatory items defer to counsel-approved packs (verify at implementation, as of 28 Nov 2026) |
| 8 | No restricted data routed to free-tier models | **Pass** | Restricted personal data appears only as a blocking value in MU05 (DEC-007, DEC-788) |
| 9 | Consistent with earlier parts | **Pass** | Template of Part 5.1a copied; V12-B decisions DEC-770…791 applied; inconsistencies reported, not edited |

**Self-review corrections.** (1) The first inventory pass expanded declared ranges ("FR-V12-A-001…222") into 222 IDs and reported 140 phantom gaps; the rule now keeps defined and explicitly written IDs only (123 in family A). (2) Paragraph-form stories and `**Requirement FR-…**` workflow definitions were missed at first; both are now parsed. (3) Combined `Priority · Wave · Points` rows were not read; baseline stories with points rose from 143 to 414 of 461. (4) Keyword routing put "Delivery models" and "Severity model" under AI; family A now uses an explicit domain table.

**Status: Part 11 Batch 11.22 complete (files a–f): 1467 FR-V12 requirements inventoried; 166 new stories (US-<EP>-ZU<nn>, 735–1195 SP) close 264 uncovered and 116 AC-less requirements, so 100% of FR-V12 have a story with acceptance criteria; 6,604 generated Examples rows; 12 persona journeys; epic map EP-01…EP-34 with totals per epic and release.**
