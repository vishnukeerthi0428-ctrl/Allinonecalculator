# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 9 (Batch 9.2), Appendices: Glossary, ID Registry and Consolidated Registers

| Field | Value |
|---|---|
| Document | Part 9, Batch 2 (appendices) |
| Version | 1.1 · 27 Nov 2026 (regenerated after the source-pack enhancement parts and Part 9.5) |
| Purpose | One place to look up every term, every ID family and every tag issued across the blueprint, with the resolution status of each conflict and recommendation, and a map of all part files |
| Baseline | Parts 0, 0A, 0B, 1, 2.1–2.7b, 3.1–3.6b, 4.1–4.4b, 5.1a–5.3, 6.1–6.10, 7.1–7.4b, 8.1–8.3c, 9.1 (DEC-066…156), 9.3, 9.4 and 9.5 (DEC-157…228, DEC-230…233) |
| Generator | `blueprint/assembly/build_registers.py` (standard-library Python + `pdfinfo`). It scans every `Part-*.md` except this file, fills the generated blocks below and writes CSVs to `blueprint/final/` |
| Roles applied | Business Systems Analyst (lead: glossary, registers), Product Owner (resolution status), Solutions Architect (ADR index), QA Lead (ID integrity and duplicate check), Technical Writer (document map) |

**How to read this batch.** Sections 9.2.1 (glossary terms and definitions), 9.2.6 (duplicate-ID analysis) and 9.2.8 (quality gate) are written by hand. Everything between `GEN` markers is produced by the script and must not be edited by hand: re-run the script instead. The script is deterministic, so two runs on the same parts give the same output. Statements in the consolidated registers are **copied from the issuing part** [ASSUMPTION-210]. The issuing part stays authoritative, and Part 9.1 overrides both where it decides.

**Acronyms defined in this part:** BSA (Business Systems Analyst), CSV (comma-separated values), ID (identifier), DEC (decision record). All other acronyms are defined in the glossary.

---

## 9.2.0 Generation method and controls

```mermaid
flowchart TD
    A["Part-*.md files<br/>Parts 0 to 9.5"] --> B["build_registers.py<br/>load in reading order"]
    B --> C["Glossary first-use search<br/>outside code fences"]
    B --> D["ID registry<br/>curated prefixes, computed ranges"]
    B --> E["Tag scanner<br/>ASSUMPTION, GAP, CONFLICT, RECOMMENDATION"]
    E --> F["Status rules<br/>DEC rows in Parts 0A, 9.1 and 9.5"]
    B --> G["ADR and DEC index"]
    B --> H["Duplicate-ID check<br/>same ID, different meaning"]
    B --> I["Document map<br/>pdfinfo pages, Mermaid count"]
    C --> J["Part 9.2 GEN blocks"]
    D --> J
    F --> J
    G --> J
    H --> J
    I --> J
    D --> K["final/*.csv"]
    F --> K
    G --> K
    H --> K
    I --> K
```

| Control | Rule applied by the script | Why |
|---|---|---|
| Reading order | Part 0 → 0A → 0B → 1 → 2.1 … 9.5, with sub-batches (5.1a, 5.1b, …) and two-digit batches (6.10 after 6.9b) in order | "First seen" and "first use" must follow the order a reader meets them |
| Code fences | Mermaid, Gherkin and code blocks are skipped for glossary first use | A term inside a diagram label is not a definition point |
| Tag statement | Taken from the issuing part's register row (first cell = tag). When no register row exists, the text of the line of first use is taken | The register row is the issuer's own wording [ASSUMPTION-210] |
| Mentions of unused numbers | Lines that say "not used", "never used", "unused" or "not issued" do not count as an occurrence | Batch registers list allocated-but-unused numbers; these are not tags |
| CONFLICT status | "Resolved — Part 0A / 9.1 / 9.5 (DEC-…)" when a DEC row in Part 0A, 9.1 or 9.5 cites the conflict, or the Part 9.5 conflict-to-decision index (§9.5.1.11) pairs it with a DEC, including ranges such as `CONFLICT-001…014` and short lists such as `CONFLICT-112/101`. Otherwise "Resolved locally" when the issuing register row states a resolution, else "Open" | [ASSUMPTION-211] |
| RECOMMENDATION status | **Accepted unless a DEC rejects it** (DEC-149 for RECOMMENDATION-001…090, DEC-221 for 300…491; others accepted because no DEC rejects them). The status names the accepting DEC and any DEC that cites or varies the recommendation; "Rejected (DEC-…)" only when a DEC row names the ID followed by rejected / not accepted / declined / withdrawn | [ASSUMPTION-211]; DEC-149; DEC-221 |
| GAP status | "Closed by DEC-…" when a DEC row cites the gap or the Part 9.5 §9.5.1.12 table says "Closed by"; "Narrowed by DEC-…" when it says "narrowed" (GAP-143, DEC-218); otherwise the issuing row's status | [ASSUMPTION-211] |
| ID ranges | Computed from every mention, including citations. Fixture identifiers used inside Gherkin and test data (for example `OPP-7001`, `CMP-9`, `INV-OS-2027-0042`) are not ID families and are excluded | ASSUMPTION-153 makes all AC data synthetic [ASSUMPTION-214] |
| Page counts | `pdfinfo` on each part's PDF at build time | [ASSUMPTION-212] |

---

## 9.2.1 Glossary

Columns: **Term** (bold = the searchable key), **Definition** (with the governing source), **First use** (part and section where the key first appears in reading order, computed by the script [ASSUMPTION-213]). Where a term first appears in a front-matter table, "front matter" is shown.

### 9.2.1.1 Acronyms and abbreviations

<!-- GLOSSARY:BEGIN -->

| Term | Definition | First use |
|---|---|---|
| **AA** (WCAG conformance level AA) | The middle WCAG conformance level. The blueprint targets WCAG 2.2 AA for Website, Portal and Admin (RECOMMENDATION-001, accepted; DEC-098) | Part 0 §0.3.3 |
| **ABAC** (Attribute-Based Access Control) | Access decisions from attributes of user, resource and context (scope, ownership, MFA age, data class) in addition to role. Rules ABAC-01…12 (Part 2.3) | Part 0 §0.11 |
| **ACM** (AWS Certificate Manager) | AWS service that issues and renews TLS certificates for CloudFront and the load balancer, including verified tenant custom domains | Part 3.1 §3.1.13.3 |
| **ADOT** (AWS Distro for OpenTelemetry) | AWS-supported OpenTelemetry collector that ships traces and metrics to X-Ray and CloudWatch (ADR-058) | Part 3.1 ADR-025 Observability: OpenTelemetry, Se |
| **ADR** (Architecture Decision Record) | A recorded architecture decision with context, alternatives, consequences and review trigger. Index in §9.2.5(e) | Part 0 §0.3.3 |
| **AES** (Advanced Encryption Standard) | Symmetric cipher. AES-256-GCM is used for field-level envelope encryption of Restricted fields (ADR-056) | Part 3.3 §3.3.16.4 |
| **AI** (Artificial Intelligence) | In this product: model-assisted drafting, classification, extraction, matching and summarising. AI never signs, pays, submits bids or sets prices (DEC-064, ADR-082) | Part 0 |
| **AIE** (AI evaluation test) | Test type for AI behaviour: grounding, abstention, injection resistance, output schema, cost (Part 4.1 abbreviation, used in Part 6) | Part 4.1 §4.2.1 |
| **ALB** (Application Load Balancer) | AWS layer-7 load balancer in front of the API process groups | Part 3.1 front matter |
| **API** (Application Programming Interface) | Here, the REST/JSON interface of the backend. The derived catalogue holds 555 operations API-001… (DEC-015, DEC-104) | Part 0 §0.1.2 |
| **ASGI** (Asynchronous Server Gateway Interface) | Python interface for asynchronous web servers; relevant if Server-Sent Events are added later (ADR-034) | Part 3.1 §3.1.8 |
| **ASVS** (Application Security Verification Standard) | OWASP checklist of security requirements; Level 2 is the verification target (RECOMMENDATION-073) | Part 6.1 front matter |
| **AWS** (Amazon Web Services) | The cloud provider; primary region ap-south-1 Mumbai (ASSUMPTION-004, DEC-040) | Part 0 §0.3.2 |
| **AZ** (Availability Zone) | An isolated data-centre group inside an AWS region. Pilot runs single-AZ app + PITR database; Multi-AZ at the scale gate (DEC-040, DEC-079) | Part 0 §0.4 |
| **B2B** (Business-to-Business) | Sales to organisations (institutions, enterprises, buyers), the main motion for AppNAI, MedMaarg and OrganicSpec | Part 0 §0.7 |
| **BFF** (Backend for Frontend) | A server-side layer per frontend that holds the OIDC session, exchanges tokens and exposes only that surface's routes (ADR-005) | Part 0A §E |
| **BFLA** (Broken Function-Level Authorization) | OWASP API risk: calling an operation the role must not call. Covered by RBAC tests and AZ- layers (Part 4.1) | Part 2.7a §2.7.7 |
| **BOLA** (Broken Object-Level Authorization) | OWASP API risk: reading or changing another tenant's or user's object by ID. Covered by RLS + object grants (Part 4.1) | Part 2.7a §2.7.7 |
| **BR** (Business Requirement) | Requirement at business level: BR-M01…M66, BR-S001…S140, group BRs BR-TENANT/WEB/AUTO/SVC/QA (Part 1 §1.12; DEC-059) | Part 0 §0.3.1 |
| **BRD** (Business Requirements Document) | One of the two source documents. Cited as BRD §n per the Part 0 §0.1.2 convention | Part 0 front matter |
| **BRIN** (Block Range Index) | PostgreSQL index type for very large, time-ordered tables (audit, events) (Part 3.3) | Part 3.3 §3.3.1.3 |
| **BRL** (Business Rule) | Deterministic business rule BRL-<domain>-## (162 in Part 2.3), e.g. BRL-ELG eligibility, BRL-AI AI guardrails | Part 0 §0.11 |
| **BVA** (Boundary Value Analysis) | Test technique on thresholds and limits; data rows BVA-D01… (Part 6.1) | Part 0 §0.11 |
| **CAN-SPAM** (Controlling the Assault of Non-Solicited Pornography And Marketing Act) | US law on commercial e-mail: identification, opt-out, physical address (ASSUMPTION-003; Part 4.1) | Part 0 §0.4 |
| **CASL** (Canada's Anti-Spam Legislation) | Canadian law requiring express or implied consent for commercial electronic messages (CA-R rules, Part 4.1) | Part 0 §0.4 |
| **CDN** (Content Delivery Network) | CloudFront, serving publication snapshots and static assets (ADR-010) | Part 0 §0.3.3 |
| **CERT-In** (Indian Computer Emergency Response Team) | Indian national CERT; its directions require incident reporting within 6 hours and log retention of 180 days (verify, as of 27 Nov 2026) (DEC-078) | Part 3.4 §A |
| **CGST** (Central Goods and Services Tax) | Central half of intra-state GST, charged with SGST (DEC-027) | Part 0A §C |
| **CI** (Continuous Integration) | Automated build, test and scan on every change (GitHub Actions, ADR-026). Not to be confused with **CI-###** candidate AI ideas (Part 7.1) | Part 0 §0.8 |
| **CI/CD** (Continuous Integration / Continuous Delivery) | The pipeline from commit to production with gates PL-01… (Part 4.3) | Part 0 §0.11 |
| **CLS** (Cumulative Layout Shift) | Core Web Vital for visual stability of public pages (Part 4.2) | Part 2.5 §2.48 |
| **CMK** (Customer-Managed Key) | KMS key controlled by the operator, per data domain (ADR-055) | Part 3.4 front matter |
| **CORS** (Cross-Origin Resource Sharing) | Browser rule set controlling which origins may call the API; locked to the product's own origins (Part 4.1) | Part 1 §1.12.2 |
| **CRM** (Customer Relationship Management) | Organisations, contacts, deals, stages and activities (module group around A018, A029, A032) | Part 0 §0.4 |
| **CSP** (Content Security Policy) | HTTP header restricting script and resource origins on Website, Portal and Admin (Part 4.1) | Part 3.4 Document(s) 04 |
| **CSRF** (Cross-Site Request Forgery) | Attack that makes a signed-in browser send an unwanted request; mitigated by SameSite cookies and tokens in the BFF (Part 4.1) | Part 3.1 §3.1.4.1 |
| **CTA** (Call to Action) | Button or link that asks the visitor to act (enquire, book, download) on public pages | Part 2.1 §2.4.1 |
| **CVSS** (Common Vulnerability Scoring System) | Severity score used to set vulnerability fix deadlines (Part 4.1) | Part 4.1 §4.16.3 |
| **DAG** (Directed Acyclic Graph) | Shape of a declarative workflow: approved node types, no cycles (DEC-051, ADR-027) | Part 0A §D |
| **DAST** (Dynamic Application Security Testing) | Security testing against a running build (OWASP ZAP, ADR-057) | Part 4.1 front matter |
| **DB** (Database) | PostgreSQL in this product. Also the prefix of operational dashboards DB-01… (Part 4.3) | Part 0 §0.1.2 |
| **DBA** (Database Administrator) | Role responsible for schema, indexes, backups and restore drills (Part 3.3) | Part 3.1 front matter |
| **DEK** (Data Encryption Key) | Per-tenant key that encrypts field data; itself wrapped by a KMS key (ADR-055/056) | Part 3.3 §3.3.1.3 |
| **DKIM** (DomainKeys Identified Mail) | E-mail signature standard; enforced per startup sender domain on SES (DEC-025) | Part 0A §C |
| **DLP** (Data Loss Prevention) | Controls that detect and block personal or restricted data in prompts, logs and exports (Presidio, ADR-080) | Part 3.4 front matter |
| **DLQ** (Dead-Letter Queue) | Queue holding messages that failed all retries, for human review and replay (Part 3.1, US-2105) | Part 2.1 §2.2 |
| **DMARC** (Domain-based Message Authentication, Reporting and Conformance) | E-mail policy that tells receivers how to treat mail failing SPF/DKIM (DEC-025) | Part 0A §C |
| **DNS** (Domain Name System) | Used for tenant custom-domain verification (TXT records) and e-mail authentication | Part 1 §1.11 |
| **DoR/DoD** (Definition of Ready / Definition of Done) | Entry and exit checklists for a story: ready = INVEST, AC, data, design; done = tests, scans, accessibility, docs, evidence (Part 5.1a) | Part 0 §0.11 |
| **DPA** (Data Processing Agreement) | Contract with a processor (Anthropic, AWS, providers) on data use, retention and sub-processing (GAP-141) | Part 2.6 §2.6.5.6 |
| **DPDP** (Digital Personal Data Protection Act 2023, India) | India's personal-data law with the DPDP Rules; consent, notice, children's data, rights and breach duties. Verify commencement dates (as of 27 Nov 2026) (ASSUMPTION-003, ASSUMPTION-128) | Part 0 §0.4 |
| **DPIA** (Data Protection Impact Assessment) | Assessment before high-risk processing (children, health-adjacent); triggers DPIA-T1… (RECOMMENDATION-007; Part 4.1) | Part 0A §C |
| **DPO** (Data Protection Officer) | Person accountable for privacy compliance and rights requests | Part 0 §0.9 |
| **DR** (Disaster Recovery) | Restoring service after a major failure; drills DR-1…DR-8 (Part 6.1), RTO/RPO per DEC-079 | Part 0 §0.4 |
| **DRF** (Django REST Framework) | The Python REST toolkit on which the backend API is built (CN-01) | Part 0 §0.7 |
| **DSC** (Digital Signature Certificate) | Indian certificate-based e-signature, one of the legal e-sign routes (DEC-023) | Part 0 §0.9 |
| **DTO** (Data Transfer Object) | Typed request/response shape at the API boundary (Part 3.2) | Part 2.1 §2.3 |
| **E2E** (End-to-End test) | Browser-level test of a complete journey across frontend, API and workers (Playwright; Part 6.1) | Part 0A §F |
| **ECR** (Elastic Container Registry) | AWS registry for the backend container images (ADR-036) | Part 3.1 front matter |
| **ECS** (Elastic Container Service) | AWS container orchestrator; pilot runs ECS on one EC2 instance (ADR-013) | Part 3.1 front matter |
| **EU AI Act** (European Union Artificial Intelligence Act) | EU regulation classifying AI systems by risk; Part 7.3 classifies this product's AI uses (verify obligations, as of 27 Nov 2026) | Part 0 §0.11 |
| **EVR** (Evidence Record) | Structured test-evidence record implementing BRD §12.2 fields (RECOMMENDATION-072) | Part 2.6 front matter |
| **FAQ** (Frequently Asked Questions) | Approved question-and-answer content used by the website assistant and pages | Part 0A §F |
| **FinOps** (Financial Operations) | Practice of tracking and controlling cloud and AI spend against budget lines B01… (Part 8) | Part 0 front matter |
| **FK** (Foreign Key) | Database reference to another table; composite with tenant/startup keys in this product (ADR-002) | Part 0 §0.3.3 |
| **FPO** (Farmer Producer Organisation) | Collective of farmers; a typical OrganicSpec supplier | Part 1 P14 External Customer / Prospect (portal |
| **FR** (Functional Requirement) | FR-W01…W34, FR-A001…A113, FR-OP001…003 and cross-cutting FR-<area>-## (Part 2.1 §2.4) | Part 0 §0.1.2 |
| **FRD** (Functional Requirements Document) | The second source document. Cited as FRD §n | Part 0 front matter |
| **FTE** (Full-Time Equivalent) | Staffing unit. Team = 4.0 engineering FTE + 0.5 growth/compliance (DEC-005) | Part 0 §0.2 |
| **FX** (Foreign Exchange) | Currency conversion. Planning rate ₹90/USD (ASSUMPTION-101, ASSUMPTION-144); FX snapshot recorded per document, no automatic conversion of actuals (DEC-027) | Part 0 §0.4 |
| **GA** (General Availability) | A provider release state; only GA model versions are used in production (DEC-007) | Part 0A §B |
| **GDPR** (General Data Protection Regulation) | EU (and UK GDPR) data-protection law for EU/UK recipients; rules EU-R1… (Part 4.1; DEC-029) | Part 0 §0.4 |
| **GIN** (Generalized Inverted Index) | PostgreSQL index used for full-text and trigram search (ADR-029) | Part 3.1 ADR-029 PostgreSQL full-text and trigram |
| **GST** (Goods and Services Tax) | Indian indirect tax: CGST+SGST intra-state, IGST inter-state, exports zero-rated under LUT (DEC-027) | Part 0 §0.4 |
| **GSTIN** (GST Identification Number) | 15-character GST registration of a startup or buyer, held on the TaxProfile (DEC-027) | Part 0A §C |
| **GTM** (Go-To-Market) | Plan for reaching customers per startup and for the SaaS offer (BRD §8) | Part 0 §0.1.2 |
| **HA** (High Availability) | Redundancy that keeps service up through component failure; deferred to the scale gate (DEC-040) | Part 0 §0.4 |
| **HITL** (Human-in-the-Loop) | A human approves or edits before an AI output has any effect (autonomy L0/L1) | Part 0 §0.11 |
| **HMAC** (Hash-based Message Authentication Code) | Keyed hash. Used for webhook signatures and blind indexes over encrypted fields (ADR-056) | Part 2.7b §2.7.10 |
| **HNSW** (Hierarchical Navigable Small World) | Approximate nearest-neighbour index type in pgvector (Part 3.3) | Part 3.1 ADR-007 pgvector instead of an external |
| **HSN/SAC** (Harmonized System of Nomenclature / Services Accounting Code) | GST classification codes for goods (HSN) and services (SAC); held per offering (DEC-027) | Part 0A §C |
| **HSTS** (HTTP Strict Transport Security) | Header forcing browsers to use HTTPS only (Part 4.1) | Part 4.1 §4.5.1 |
| **IaC** (Infrastructure as Code) | Infrastructure defined in versioned code (OpenTofu, ADR-012; DEC-083) | Part 0 §0.11 |
| **IAM** (Identity and Access Management) | AWS service for roles and policies; CI deploys through OIDC-federated roles (ADR-026) | Part 2.4 §2.35.2 |
| **ICU** (International Components for Unicode) | Library family; ICU MessageFormat is the string format for plurals and variables (DEC-026) | Part 0A §C |
| **IdP** (Identity Provider) | The reused AppNAI identity service issuing tokens for audience `growth-engine` (DEC-003, DEC-019) | Part 0 §0.6 |
| **IDOR** (Insecure Direct Object Reference) | Accessing an object by guessing its ID; same family as BOLA (Part 4.1) | Part 4.1 §4.8.1 |
| **IGST** (Integrated Goods and Services Tax) | GST on inter-state supply (DEC-027) | Part 0A §C |
| **INP** (Interaction to Next Paint) | Core Web Vital for responsiveness (Part 4.2) | Part 2.5 §2.48 |
| **INR** (Indian Rupee) | Base currency; amounts stored as Decimal with ISO 4217 code (ASSUMPTION-012, DEC-027) | Part 0 §0.3.1 |
| **INVEST** (Independent, Negotiable, Valuable, Estimable, Small, Testable) | Quality criteria every user story must meet before it is Ready (Part 5.1a) | Part 0 §0.11 |
| **IRN** (Invoice Reference Number) | Number issued by the GST e-invoice portal; statutory e-invoicing is later scope L-01 | Part 0A §C |
| **ISO 4217** (currency code standard) | Three-letter currency codes stored with every money amount (ASSUMPTION-012) | Part 0 §0.3.3 |
| **IST** (Indian Standard Time) | UTC+05:30; business-hour, quiet-hour and support windows are stated in IST (DEC-044) | Part 0A §C |
| **IT Act** (Information Technology Act 2000, India) | Indian law on electronic records, e-signatures and intermediaries; rules IT-R1… (Part 4.1) | Part 0 §0.4 |
| **JSON** (JavaScript Object Notation) | Data format of the API and of structured AI outputs (ADR-072) | Part 0 §0.3.3 |
| **JWKS** (JSON Web Key Set) | Published public keys used to verify IdP tokens (ASSUMPTION-104) | Part 3.1 §3.1.16 |
| **KEK** (Key Encryption Key) | KMS key that wraps data encryption keys (ADR-055) | Part 3.3 §3.3.1.3 |
| **KMS** (Key Management Service) | AWS service holding encryption keys (ADR-014, ADR-055) | Part 3.1 front matter |
| **KPI** (Key Performance Indicator) | Measured outcome KPI-01…31 with formula, target and owner (Part 1 §1.4) | Part 0 §0.3.2 |
| **LCP** (Largest Contentful Paint) | Core Web Vital for load speed of public pages (Part 4.2) | Part 2.5 §2.48 |
| **LLM** (Large Language Model) | Model such as Claude Haiku or Sonnet used through the model gateway (Part 7) | Part 0A §B |
| **LUT** (Letter of Undertaking) | GST filing that lets an exporter supply without paying IGST; held on the TaxProfile (DEC-027) | Part 0A §C |
| **MAPE** (Mean Absolute Percentage Error) | Forecast-accuracy metric (BR-M60 forecasting; Part 7) | Part 1 §1.4.2 |
| **MFA** (Multi-Factor Authentication) | Second factor at sign-in: TOTP minimum, passkeys/WebAuthn required for privileged and approver roles (DEC-019, DEC-077) | Part 0 §0.3.3 |
| **MoSCoW** (Must, Should, Could, Won't) | Prioritisation scheme for BRs and stories (Part 1) | Part 0 §0.5 |
| **MoU** (Memorandum of Understanding) | Agreement with an institution (e.g. a school) that allows EduVerse outreach through it (DEC-030) | Part 0A §C |
| **MTTR** (Mean Time To Restore) | Average time from incident start to service restoration (Part 4.3) | Part 4.2 front matter |
| **NAT** (Network Address Translation) | Gateway that gives private subnets outbound internet; cost line in Part 3.1 | Part 3.1 §3.1.6.2 |
| **NFR** (Non-Functional Requirement) | Quality requirement NFR-001… (performance, security, availability, accessibility) (Part 0 §0.6; Part 4.2) | Part 0 §0.3.1 |
| **NSE** (No Side Effect) | Test shorthand: no state change, no outbox row, no provider call, and a denial audit event (Part 6 test cases) | Part 6.2a front matter |
| **OIDC** (OpenID Connect) | Authentication protocol on top of OAuth 2.0 used between the BFFs and the IdP (ADR-005) | Part 0 §0.4 |
| **OKR** (Objectives and Key Results) | Goal framework linking G-## goals to KPIs (Part 1) | Part 0 §0.11 |
| **OSS** (Open-Source Software) | Preferred for tooling where it fits the budget (ADR-057, ADR-079, ADR-080) | Part 0 §0.8 |
| **OTP** (One-Time Password) | Single-use code; used to verify guardians and portal users (DEC-030) | Part 0A §C |
| **OWASP** (Open Worldwide Application Security Project) | Community that publishes the Top 10, API Security Top 10, ASVS and ZAP; used as checklists (Part 4.1, Part 6.1) | Part 0 §0.11 |
| **p95** (95th percentile) | Latency below which 95% of requests complete; SLO unit (DEC-018) | Part 0 §0.3.3 |
| **PAN** (Permanent Account Number) | Indian tax identifier; treated as Restricted data | Part 4.1 §4.5.3 |
| **PCI DSS** (Payment Card Industry Data Security Standard) | Card-data security standard; scope is minimised by hosted checkout, so the platform never stores card data (ASSUMPTION-015; PCI-R rules) | Part 0 §0.7 |
| **pd** (person-day) | Effort unit. Programme 287–483 pd; central ≈ 416 pd after DEC-103 | Part 0 §0.3.1 |
| **PDF** (Portable Document Format) | Format of generated quotes, invoices and contracts (WeasyPrint, ADR-032) | Part 0 §0.9 |
| **PDP** (Policy Decision Point) | Deterministic in-process library that rechecks scope, consent, suppression, jurisdiction, quiet hours, caps, entitlement, budget and approval hash at dispatch; first deny wins (ADR-004; BRL-ELG) | Part 2.1 §2.2 |
| **PECR** (Privacy and Electronic Communications Regulations, UK) | UK rules on electronic marketing alongside UK GDPR (ASSUMPTION-003) | Part 0 §0.4 |
| **PII** (Personally Identifiable Information) | Data that identifies a person; classified Restricted (RECOMMENDATION-004) | Part 0 §0.11 |
| **PITR** (Point-In-Time Recovery) | Database restore to any second within the retention window; basis of RPO ≤ 15 min (DEC-018) | Part 0 §0.8 |
| **PK** (Primary Key) | Unique row identifier; UUIDv7 generated in the application (RECOMMENDATION-036) | Part 3.3 §3.3.1.2 |
| **PKCE** (Proof Key for Code Exchange) | OAuth extension that protects the authorization-code flow (ASSUMPTION-104) | Part 0A §C |
| **PO** (Product Owner) | Accountable for backlog and acceptance; the founder/CTO (DEC-005). In OrganicSpec context also *purchase order* | Part 0 §0.5 |
| **QA** (Quality Assurance) | Testing discipline; 0.5 FTE automation QA (DEC-005); BR-QA group | Part 0 front matter |
| **RACI** (Responsible, Accountable, Consulted, Informed) | Responsibility matrix for roles and processes (Part 8) | Part 0 §0.11 |
| **RAG** (Retrieval-Augmented Generation) | AI answers grounded on retrieved approved records with citations; pgvector retrieval scoped by RLS (ADR-041, ADR-077) | Part 0B 0B.2 How the review was done |
| **RBAC** (Role-Based Access Control) | Permissions by role R01–R20 (Part 2.3 §2.26) | Part 0 §0.11 |
| **REST** (Representational State Transfer) | API style used with OpenAPI 3.1 and problem+json errors (ADR-022) | Part 0 §0.2 |
| **RFP** (Request for Proposal) | Buyer document inviting proposals; AppNAI bid desk input (AG-019) | Part 0 §0.2 |
| **RFQ** (Request for Quotation) | Buyer request for prices; drives quotes (WF-01) | Part 0 §0.2 |
| **RLS** (Row-Level Security) | PostgreSQL feature that filters every row by tenant and startup session variables; the primary isolation control (ADR-002, RECOMMENDATION-037) | Part 0 §0.1.2 |
| **RPO/RTO** (Recovery Point Objective / Recovery Time Objective) | Maximum data loss and maximum downtime. RPO ≤ 15 min; RTO ≤ 4 h for instance/AZ/database failure, ≤ 24 h for regional outage in the pilot (DEC-018, DEC-079) | Part 0 §0.3.3 |
| **RPS** (Requests Per Second) | Load-model throughput unit (Part 4.2) | Part 4.2 front matter |
| **RUM** (Real User Monitoring) | Field measurement of page performance from real browsers (first-party web-vitals beacon, ADR-058) | Part 2.7a front matter |
| **S3** (Amazon Simple Storage Service) | Object storage for documents, uploads and publication snapshots; Object Lock compliance mode for audit anchors (DEC-082) | Part 0 §0.7 |
| **SaaS** (Software as a Service) | The product sold to external tenants on metered plans (BR-SVC; DEC-047) | Part 0 §0.1.2 |
| **SAST** (Static Application Security Testing) | Source-code security scanning (Semgrep, Bandit; ADR-057) | Part 3.4 Document(s) 10 |
| **SBOM** (Software Bill of Materials) | Inventory of components in a build for vulnerability tracking (Part 4.3) | Part 3.1 ADR-026 CI/CD with GitHub Actions and OI |
| **SCA** (Software Composition Analysis) | Dependency vulnerability scanning (OSV-Scanner, pip-audit; ADR-057) | Part 4.1 front matter |
| **SES** (Amazon Simple Email Service) | E-mail provider; per-startup configuration sets (DEC-025, ADR-016) | Part 0 §0.4 |
| **SEO** (Search Engine Optimisation) | Public-page structure and metadata for search visibility (EP-11) | Part 0 §0.10.2 |
| **SGST** (State Goods and Services Tax) | State half of intra-state GST (DEC-027) | Part 0A §C |
| **SKU** (Stock Keeping Unit) | Sellable item variant with availability and reservation (OrganicSpec; DEC-045) | Part 0 §0.4 |
| **SLA** (Service Level Agreement) | Contractual service promise; pilot support targets are internal, not contractual (DEC-044) | Part 0 §0.4 |
| **SLI** (Service Level Indicator) | The measured quantity behind an SLO (Part 4.3) | Part 4.2 front matter |
| **SLO** (Service Level Objective) | Internal reliability target SLO-01… (DEC-018; Part 4.3) | Part 0 §0.3.3 |
| **SNS** (Amazon Simple Notification Service) | Delivers SES bounce and complaint events to webhooks (DEC-025) | Part 0A §C |
| **SoD** (Segregation of Duties) | Author cannot approve own item; maker cannot be checker (BRL-APR; `SOD_AUTHOR_CANNOT_APPROVE`) | Part 2.3 §2.29 |
| **SP** (Story Points) | Relative effort unit; 1 SP ≈ 0.5–1.0 pd, central 0.7 (ASSUMPTION-150) | Part 2.6 front matter |
| **SPA** (Single-Page Application) | Browser application model of both React frontends | Part 3.1 §3.1.3.2 |
| **SPF** (Sender Policy Framework) | DNS record listing servers allowed to send mail for a domain (DEC-025) | Part 0A §C |
| **SQL** (Structured Query Language) | PostgreSQL query language | Part 3.3 §3.3.1.1 |
| **SRE** (Site Reliability Engineering) | Operations discipline owning SLOs, alerts and runbooks; 0.5 DevOps/SRE FTE (DEC-005) | Part 0 front matter |
| **SSE** (Server-Sent Events) | One-way push from server to browser; later option after polling (ADR-034) | Part 3.1 §3.1.3.2 |
| **SSO** (Single Sign-On) | One sign-in across applications through the shared IdP (DEC-003) | Part 0 §0.2 |
| **SSRF** (Server-Side Request Forgery) | Attack that makes the server fetch internal URLs; mitigated by egress allowlists for crawling and webhooks (Part 4.1) | Part 3.2 front matter |
| **STRIDE** (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege) | Threat-modelling categories used for THR-001… (RECOMMENDATION-007; Part 4.1) | Part 0 §0.8 |
| **SUS** (System Usability Scale) | Ten-item usability questionnaire used in usability testing (Part 2.5, Part 6) | Part 2.6 §2.6.5.1.4 |
| **TCCCPR** (Telecom Commercial Communications Customer Preference Regulations 2018) | TRAI regulations on commercial SMS/voice, headers, templates and preferences (DLT). Applicability to WhatsApp/e-mail to verify (ASSUMPTION-003; TR-R rules) | Part 0 §0.7 |
| **TCO** (Total Cost of Ownership) | Full cost of a component over time (AI TCO in Part 7.3) | Part 0 §0.11 |
| **TLS** (Transport Layer Security) | Encryption in transit; TLS 1.2+ everywhere (Part 4.1) | Part 3.1 §3.1.3.2 |
| **TOTP** (Time-based One-Time Password) | Authenticator-app second factor; interim minimum until passkeys (DEC-077) | Part 0A §C |
| **TRAI** (Telecom Regulatory Authority of India) | Indian telecom regulator issuing TCCCPR (ASSUMPTION-003) | Part 0 §0.7 |
| **TTFB** (Time To First Byte) | Server responsiveness metric for public pages (DEC-018) | Part 0A §C |
| **TTL** (Time To Live) | Expiry of a cache entry, token or lock (e.g. prompt cache 5 min / 1 h, ADR-075) | Part 2.6 front matter |
| **UAT** (User Acceptance Testing) | Business acceptance by real users before release (DEC-095, Part 8) | Part 0 §0.1.2 |
| **UI** (User Interface) | Screens of the Website/Portal and Admin Command Centre (Part 2.5) | Part 0 §0.1.2 |
| **UPI** (Unified Payments Interface) | Indian instant bank payment rail; pilot payment evidence path with UTR (DEC-022) | Part 0A §C |
| **URL** (Uniform Resource Locator) | Web address; slugs are part of publication snapshots | Part 1 §1.12.1 |
| **USD** (United States Dollar) | Currency of most provider prices; converted at the planning rate (ASSUMPTION-144) | Part 0 §0.7 |
| **UTC** (Coordinated Universal Time) | Storage time standard; displayed in the user's time zone (ADR-030) | Part 0 §0.3.3 |
| **UTR** (Unique Transaction Reference) | Bank/UPI transfer reference recorded as payment evidence; duplicates are blocked (DEC-022) | Part 3.3 §3.3.6.9 |
| **UUID** (Universally Unique Identifier) | Identifier format; UUIDv7 used for primary keys (RECOMMENDATION-036) | Part 0 §0.3.3 |
| **UX** (User Experience) | Design discipline; principles UX-01… (Part 2.5) | Part 0 front matter |
| **VPC** (Virtual Private Cloud) | Isolated AWS network for the application, database and caches | Part 3.1 front matter |
| **WABA** (WhatsApp Business Account) | Meta account through which approved WhatsApp templates and replies are sent via the Cloud API (ADR-039; WA-R rules) | Part 2.1 §2.2 |
| **WAF** (Web Application Firewall) | Filter for malicious HTTP traffic; AWS WAF on CloudFront from W2 (DEC-081) | Part 0A §C |
| **WCAG** (Web Content Accessibility Guidelines) | W3C accessibility standard; version 2.2 level AA is the target (RECOMMENDATION-001) | Part 0 §0.3.3 |
| **WORM** (Write Once, Read Many) | Immutable storage; S3 Object Lock compliance mode for audit anchors (DEC-082) | Part 2.4 §2.34.3 |
| **XSS** (Cross-Site Scripting) | Injection of script into pages; mitigated by output encoding, CSP and sanitised rich text (Part 4.1) | Part 3.1 ADR-005 Backend-for-Frontend authenticat |
| **ZAP** (Zed Attack Proxy) | OWASP open-source DAST scanner (ADR-057) | Part 4.1 §4.2.1 |
| **ZDR** (Zero Data Retention) | Provider option under which prompts and outputs are not stored; eligibility to verify (GAP-141) | Part 7.3 §7.8.2 |

### 9.2.1.2 Product and domain terms

| Term | Definition | First use |
|---|---|---|
| **Owner Portfolio Tenant** | The single tenant that holds all 25+ owned startups as startup workspaces (DEC-065) | Part 0A §F |
| **tenant** | The top isolation boundary: the Owner Portfolio Tenant or one external SaaS client. Cross-tenant aggregation is never permitted (DEC-065; ADR-002) | Part 0 §0.1.2 |
| **startup workspace** | A startup inside a tenant (e.g. AppNAI, MedMaarg) with its own catalogue, senders, budgets and data; RLS key below tenant (DEC-065) | Part 0A §B |
| **portfolio scope** | Multi-startup view inside one tenant: aggregates and drill-down only, every mutating control hidden and denied (DEC-055) | Part 2.1 §2.3 |
| **business line** | A commercial line inside a startup workspace (entity BusinessLine) used for scope and reporting (DEC-016, DEC-084) | Part 2.1 §2.4.1 |
| **offering** | A product or service a startup sells, with versions, claims, prices and status planned/approved/available (DEC-016; Part 3.3 name per DEC-107) | Part 0 §0.4 |
| **capability profile** | Per startup/tenant switchboard that enables desks and features (bid desk, order desk, pilots, guardian intake) instead of hard-coding them to a startup (DEC-052, DEC-084) | Part 0 §0.6 |
| **AppNAI** | Owned startup for global AI project bids; default route for external AI projects (DEC-052) | Part 0 §0.2 |
| **MedMaarg** | Owned startup for institutional wellness partnerships; no patient data (BRD §5; DEC-021) | Part 0 §0.1.2 |
| **EduVerse** | Owned startup in education; no direct outreach, profiling or targeted ads to anyone under 18 (DEC-030) | Part 0 §0.2 |
| **OrganicSpec** | Owned agri buy/sell startup with separate receivable and payable ledgers and SKU reservation (DEC-045) | Part 0 §0.2 |
| **Website/Portal** | Public frontend `commercial-website-react`: 34 screens W01–W34 (public pages, intake, chat, booking and signed-in external portal) (DEC-009) | Part 0 §0.7 |
| **Admin Command Centre** | Confidential frontend `commercial-admin-react`: 113 screens A001–A113 in seven views (DEC-009, DEC-062) | Part 1 §1.1 |
| **seven views** | Command Centre navigation: Overview, Discovery, Outreach & Marketing, Follow-ups, Objections, Closure, Automation (BRD §3; UX-02) | Part 1 §1.1 |
| **Action Centre** | In-app notification and task centre (A106) with e-mail digest (DEC-036) | Part 1 §1.12.2 |
| **Admin Copilot** | Read-only, grounded assistant in the Admin side panel; answers from authorised records with citations; drafts but never executes (DEC-035, ADR-041) | Part 0 §0.4 |
| **signal** | A piece of public evidence suggesting a need or opportunity, reviewed by a human; ≥ 80% precision gate on ≥ 100 reviewed signals (DEC-001, DEC-096) | Part 0 §0.3.2 |
| **evidence** | Source record with URL, date, licence/permission and confidence that grounds signals, opportunities and drafts (PP-05; BRL-SRC) | Part 0 §0.1.2 |
| **claim** | An approved, dated statement about an offering that external content may use; unapproved claims are blocked (BRL-AI-05; M02) | Part 0 §0.2 |
| **opportunity score** | round(100 × Σ wᵢcᵢ / Σ w over known components); "Unknown – review required" when known weight < 0.60; bands ≥ 75 / 50–74 / < 50 (DEC-011) | Part 0 §0.7 |
| **qualified opportunity** | Counted only with evidence, fit and an accountable owner, de-duplicated; unknown remains unqualified (BR-S039; KPI-07) | Part 0 §0.3.2 |
| **cost per qualified opportunity** | (AI + data + channel + allocated infrastructure) ÷ qualified opportunities; scale-gate metric (KPI-22; BR-S090) | Part 0A §B |
| **eligibility** | Whether a contact may be messaged on a channel now: consent or lawful basis, suppression, jurisdiction, quiet hours, caps, entitlement. Unknown fails closed (BRL-ELG-01) | Part 0 §0.2 |
| **suppression list** | Hashed identifiers that must never be contacted again; kept indefinitely (DEC-028) | Part 0 §0.7 |
| **quiet hours** | Local-time window in which outbound messages are deferred; deferrals are not counted late (DEC-032) | Part 0 §0.8 |
| **jurisdiction rule pack** | PDP rule set per recipient country (India, EU/UK, US, Canada …) with an outbound allowlist (DEC-029) | Part 0 §0.8 |
| **first-touch template** | Approved template for first outreach; until approved, first touch is L1, then L2 dispatch with variables only (DEC-071) | Part 1 §1.4.2 |
| **sequence** | Scheduled multi-step outreach with stop rules; contacts are enrolled (enrolment) and leave on reply, opt-out or stop (BRL-SEQ) | Part 0 §0.1.2 |
| **approval hash** | Hash of the exact approved content, recipients, parameters and policy version. Dispatch proceeds only if the hash still matches (PDP recheck; BRL-APR) | Part 1 §1.1 |
| **approval policy** | Versioned per-startup thresholds that decide who must approve (discounts, contracts, cross-border); tightening free, loosening needs founder approval (DEC-038) | Part 0A §C |
| **autonomy L0–L3** | Autonomy levels: L0 suggest only, L1 draft for human approval, L2 act with post-review for routine eligible actions, L3 act within guardrails. Consequential actions capped at L1 (ASSUMPTION-010, DEC-064) | Part 0 §0.4 |
| **Manual / Assisted / Supervised / Controlled Autonomous** | The four autonomy modes of the source, mapped to L0–L3 (ASSUMPTION-010) | Part 0 §0.2 |
| **autonomy cap matrix** | Maximum autonomy per action class: money movement not supported; contracts, quotes, discounts, bid submission, legal terms L1 max (DEC-064, DEC-071) | Part 0A §F |
| **simulation** | Dry-run of a workflow or configuration with zero live effects, required before activation (BRD §1.2; ConfigRevision state "simulated") | Part 0 §0.2 |
| **emergency stop** | Control that halts sends and runs at tenant, startup, workflow or channel scope; effective ≤ 60 s and blocks queued sends (BRL-AUT-05; BR-M55; ADR-085) | Part 0 §0.2 |
| **kill switch** | Multi-scope stop flag in Valkey checked by the gateway and the engine; implements the emergency stop for AI (ADR-085) | Part 0 §0.11 |
| **Tier 0–3** | Model routing tiers: Tier 0 rules/templates/cache; Tier 1a lighter Claude (Haiku-class); Tier 1b Claude Sonnet; Tier 2 free/open-weight fallbacks (Public or Internal-non-personal only, opt-in, default off); Tier 3 degrade to queue/human (DEC-007) | Part 0 §0.5 |
| **model gateway** | The single module through which every model call passes: redaction, routing, budget reservation, caching, audit (ADR-008, ADR-070) | Part 1 §1.1 |
| **abstention** | An AI output that declines to assert a fact because current evidence is missing (e.g. `NO_CURRENT_EVIDENCE`) (BRL-AI-04) | Part 0A §B |
| **AI budget ceilings** | Hard monthly caps on owned-portfolio AI spend: pilot ₹3,000, growth ₹12,000, scale ₹40,000; 80% alert, 100% stop (DEC-008, ADR-083) | Part 1 §1.15 |
| **growth gate** | Unlock of the ₹12,000 AI ceiling when the BRD §8 scale gate metrics are met (DEC-008) | Part 0A §B |
| **scale gate** | BRD §8 condition to increase vendor spend: verified cost per qualified opportunity, consent compliance and conversion (BR-S090) | Part 0 §0.5 |
| **pilot** | First controlled real use with owned startups at BRD §8 volumes (500 fetches, 100 reviewed signals, 2,000 e-mails, 1,000 WhatsApp templates/month) (ASSUMPTION-002) | Part 0 §0.2 |
| **W0–W6** | Delivery waves keyed to source day-phases: W0 Day 1–15 (split W0-A/W0-B, DEC-096) … W5 Day 121–180, W6 Day 181–365 (DEC-006, DEC-034) | Part 0 §0.5 |
| **Release 1 / 2 / Future** | Planning groupings: Release 1 = W0–W3, Release 2 = W4–W5, Future = W6+; not product versions (DEC-006) | Part 0 §0.5 |
| **outcome certainty** | Result state of an external action: confirmed, uncertain, failed, reconciled_confirmed, reconciled_failed. Uncertain blocks retry until reconciled (DEC-050) | Part 0 §0.6 |
| **uncertain outcome** | Provider call whose effect is unknown (timeout after submit); reconciled on a schedule before any retry (ASSUMPTION-162) | Part 2.4 §2.30.2 |
| **closure policy** | Per opportunity type: project/contract types close on executed contract (Won-Contracted) and are marked Paid separately; order types close on verified payment (DEC-054) | Part 0 §0.6 |
| **receipt** | Verified money received, distinct from closure; recorded with maker-checker verification (DEC-022, DEC-054) | Part 0 §0.2 |
| **maker-checker** | Two-person verification: one Finance user records (MakerVerified), a second verifies (CheckerVerified) (DEC-022) | Part 0 §0.3.2 |
| **receivable / payable ledger** | Separate ledgers for money owed to and by OrganicSpec (buy and sell orders) | Part 0 §0.2 |
| **reservation** | Stock held for an approved order; released on cancellation or expiry (DEC-045, DEC-070) | Part 0 §0.2 |
| **bid desk** | Workspace that prepares bid packages and checklists; a human always submits (DEC-053) | Part 0 §0.5 |
| **order desk** | Workspace for buy/sell orders, fulfilment and ledgers, enabled by capability profile (DEC-052) | Part 2.3 §2.26.1 |
| **tender** | Formal public procurement; submission is never automated (DEC-053) | Part 0 §0.4 |
| **publication snapshot** | Immutable, versioned build of public pages per tenant/startup/locale, switched live by an atomic pointer (ADR-010; DEC-084) | Part 2.1 §2.3 |
| **preview grant** | Expiring, non-indexed link to unpublished content (DEC-084) | Part 2.6 §2.6.5.1.1 |
| **custom domain** | Verified tenant/startup domain mapped to a publication; unknown host returns 404 (BRL-TEN-10; NT-046) | Part 2.3 §2.25.1 |
| **guardian** | Adult verified by OTP who acts for a learner under 18 in EduVerse (DEC-030) | Part 0 §0.4 |
| **support access grant** | Time-boxed (≤ 72 h), scoped, tenant-approved access by platform support (DEC-056) | Part 2.3 §2.27.18 |
| **plan archetype** | Starter, Growth and Scale SaaS plans with configurable entitlements; no published price until approved (DEC-047) | Part 2.5 §2.43.1 |
| **entitlement** | Plan-granted right or quota (users, workspaces, channels, AI tasks) checked by the PDP (DEC-047) | Part 0 §0.4 |
| **AI task** | One completed agent invocation returning a validated output; the SaaS metering unit (RECOMMENDATION-064; DEC-086) | Part 3.1 §3.1.4.7 |
| **CostLedger** | Record of AI cost per run, agent, startup and tenant (M53; DEC-086) | Part 2.1 §2.2 |
| **UsageMeterReading** | Billable SaaS meter values, including the nightly "AI tasks" aggregate (DEC-086) | Part 0A §C |
| **CustomerSubscription / ServiceSubscription** | Customer renewals (M50) versus the tenant's SaaS billing subscription (B-SVC) (DEC-085) | Part 3.1 front matter |
| **ConfigRevision** | Typed, versioned configuration with states draft → validated → simulated → approved → scheduled → active → superseded (Part 3.3 ENT-168) | Part 0 §0.4 |
| **ConflictCase** | Record raised when two automations or people contend for the same contact or object (conflict coordinator, A111) | Part 0 §0.4 |
| **DiscrepancyCase** | Reconciliation exception (e.g. settlement vs payment allocation) for human review (REC-01; A074) | Part 3.2 §3.2.6.4 |
| **Customer 360** | Single view of an organisation: owner, stage, eligibility per channel, activity, documents (A032) | Part 0 §0.3.3 |
| **acceptance procedure** | Business acceptance check AP-01…AP-10 (DEC-014) | Part 0A §B |
| **acceptance profile** | Reusable set of FR acceptance conditions CA-<code> (Part 2.1) | Part 2.1 §2.4.12 |
| **two-tenant fixture** | Test data with two tenants (T1, T2) to prove isolation (AP-10; TP-07) | Part 0 §0.3.3 |
| **DERIVED** | Label for catalogue items created by the blueprint because the source catalogue was not supplied (DEC-015, DEC-016, DEC-087) | Part 0 §0.4 |
| **Unknown – review required** | Display value whenever a score or fact cannot be computed safely; never shown as a number (DEC-011) | Part 0A §B |
| **B-SVC** | The service (SaaS) business line: plans, billing and support for external tenants (DEC-008, DEC-047) | Part 0 §0.1.2 |

### 9.2.1.3 Technical and engineering terms

| Term | Definition | First use |
|---|---|---|
| **modular monolith** | One Django codebase and image, split into bounded apps with import-linter rules, run as separate process groups (ADR-001) | Part 0 §0.2 |
| **process group** | A runtime role of the same image: api-web, api-admin, api-hooks, relay, workers, beat (ADR-001) | Part 3.1 §3.1.3.2 |
| **transactional outbox** | Events written in the same database transaction as the state change, then relayed to Celery; guarantees no lost or phantom sends (ADR-003) | Part 0 §0.3.3 |
| **idempotency key** | Client- or provider-supplied key that makes a repeated request or webhook have one effect (ADR-023; UQ-IDEM) | Part 0 §0.3.3 |
| **Celery** | Python task queue used for workers and scheduled jobs (ADR-003, ADR-028) | Part 0 §0.2 |
| **Celery Beat** | Celery scheduler with a database-backed schedule (ADR-028) | Part 0 §0.7 |
| **Valkey** | Open-source Redis-compatible in-memory store: broker, cache, rate limits, kill-switch flags (ADR-003, ADR-085) | Part 0 §0.2 |
| **pgvector** | PostgreSQL extension for vector similarity; used for RAG, matching and the semantic cache (ADR-007, ADR-077) | Part 0 §0.2 |
| **embedding** | Vector representation of text; multilingual E5-large class, 1,024 dimensions, self-hosted (DEC-088) | Part 2.1 §2.2 |
| **semantic cache** | Cache of model answers keyed by meaning (cosine ≥ 0.92), Public/Internal data only (ADR-076) | Part 0A §B |
| **prompt caching** | Provider-side reuse of a stable prompt prefix to cut input cost (ADR-075) | Part 7.3 §7.4.1 |
| **Batch API** | Provider asynchronous API at a discount for non-interactive work (ADR-074) | Part 6.4 AG-001 Knowledge & Claim Ingestion Assis |
| **structured output** | Model output constrained to a JSON Schema and validated before use (ADR-072) | Part 2.1 §2.3 |
| **prompt injection** | Untrusted text that tries to change model instructions; defended by isolation, tool limits and checks (AIR-01; Part 4.1) | Part 3.2 §3.2.1.12 |
| **ports and adapters** | Business code calls typed ports; adapters implement providers and return normalised results (ADR-009; IP-01) | Part 3.1 ADR-009 Provider adapter pattern (ports |
| **circuit breaker** | Stops calling a failing provider for a cool-down period (RECOMMENDATION-031) | Part 3.1 §3.1.13.3 |
| **feature flag** | Switch that enables a capability per scope, default OFF for channels and paid adapters (RECOMMENDATION-005, ADR-015) | Part 1 §1.11 |
| **expand/contract migration** | Schema change in backward-compatible steps; no production down-migrations (ADR-053) | Part 5.3 US-2109 Rollback rehearsal |
| **OpenAPI** | Machine-readable API contract (version 3.1) with breaking-change gate CT-01 (ADR-022) | Part 2.7a §2.7.7 |
| **problem+json** | RFC 9457 error format used by every API error (ADR-022) | Part 3.1 §3.1.4 |
| **OpenTelemetry** | Vendor-neutral tracing and metrics standard; correlation ID from HTTP through outbox to adapter (RECOMMENDATION-006, ADR-025) | Part 0 §0.8 |
| **Sentry** | Error-tracking service (DEC-041) | Part 0 §0.4 |
| **CloudFront** | AWS CDN in front of public snapshots and APIs (ADR-010) | Part 0A §C |
| **OpenTofu** | Open-source Terraform-compatible IaC tool (ADR-012) | Part 0 §0.8 |
| **WeasyPrint** | Server-side HTML-to-PDF renderer for documents (ADR-032) | Part 3.1 §3.1.8 |
| **Presidio** | Open-source PII detection and masking with Indian recognisers (ADR-080) | Part 6.4 front matter |
| **Langfuse** | Open-source LLM observability, self-hosted from the growth gate (ADR-078) | Part 2.7a §2.7.4.7 |
| **promptfoo** | Open-source prompt evaluation tool used in CI (ADR-079) | Part 6.1 §6.1.3.1 |
| **Playwright** | Browser automation framework for E2E tests and PDF rendering | Part 2.1 §2.2 |
| **provider simulator** | Test-only provider fake with scriptable faults: timeouts after submit, duplicate and out-of-order webhooks (RECOMMENDATION-071) | Part 2.6 Document 03 End User Personas |
| **certification ladder** | Evidence levels L-S synthetic → L-T test → L-C controlled → L-P production; synthetic results are never shown as production certification (RECOMMENDATION-072) | Part 6.1 §6.1.1.1 |
| **mutation score** | Share of injected code mutations caught by tests; ≥ 85% for money, tax, ledger and PDP (RECOMMENDATION-070) | Part 4.2 §4.23.8 |
| **error budget** | Allowed unreliability under an SLO; burn rates drive alerts (Part 4.3) | Part 2.4 §2.31.3 |
| **runbook** | Step-by-step operational procedure RB-001… (Part 4.3) | Part 0B 0B.4 Coverage by document |
| **blind index** | HMAC of a normalised value that allows equality search over encrypted fields (ADR-056) | Part 3.3 §3.3.6.5 |
| **envelope encryption** | Data encrypted with a data key, which is encrypted with a KMS key (ADR-056) | Part 3.1 §3.1.6.1 |
| **Object Lock** | S3 feature preventing deletion or change; compliance mode for audit anchors (DEC-082) | Part 2.4 §2.34.3 |
| **monorepo** | One repository for both frontends, shared UI, backend, AI assets, IaC and ops (ADR-060) | Part 3.1 §3.1.8 |
| **story point** | See SP | Part 5.1a front matter |
| **Gherkin** | Given/When/Then syntax for acceptance criteria (Part 5) | Part 0 §0.11 |
| **dimension matrix** | Story test-design dimensions D1–D8 (actor, permission, state, data, channel, tenant, integration, locale) with rows DM-### (Part 5.1a) | Part 0 §0.11 |

### 9.2.1.4 Regulatory and compliance terms

| Term | Definition | First use |
|---|---|---|
| **data principal** | DPDP term for the person the data is about | Part 4.1 §4.11.1 |
| **data fiduciary** | DPDP term for the entity that decides the purpose and means of processing; each tenant for its own contacts | Part 4.1 §4.12.1 |
| **consent** | Free, specific, informed, unambiguous agreement, with evidence stored; one of the lawful bases recorded per contact (BRL-ELG-03; DEC-029) | Part 0 §0.2 |
| **legitimate interest** | GDPR lawful basis recorded where it applies to B2B contacts in the EU/UK (DEC-029) | Part 4.1 §4.11.4 |
| **Data classification** (Public / Internal / Confidential / Restricted) | Four classes; Restricted (personal, children's, health-adjacent, financial, credentials) never goes to free-tier models (RECOMMENDATION-004; BRL-AI-06) | Part 0 §0.8 |
| **Public / Internal / Confidential / Restricted** | See Data classification | Part 0 §0.8 |
| **retention** | Keep periods: invoices 8 years, contracts term + 8, audit 7 years, security/application logs 1 year, AI payloads 90 days, marketing contacts 24 months after last eligible interaction (DEC-028, DEC-078) | Part 0 §0.3.3 |
| **rights request** | Data-principal request (access, correction, erasure, grievance); default deadline 30 days with escalation at 70% (DEC-100) | Part 0 §0.11 |
| **breach notification** | Notice of a personal-data breach to the Data Protection Board and to CERT-In within required times (verify, as of 27 Nov 2026) (Part 4.1) | Part 4.1 §4.11.5 |
| **opt-out** | Recipient withdrawal of consent (e.g. STOP keyword); takes effect before the next dispatch (BRL-ELG) | Part 0 §0.10.3 |
| **DLT** (Distributed Ledger Technology registration under TCCCPR) | Indian SMS sender/template registration platform; relevant only if SMS is enabled (verify) | Part 4.1 §4.12.3 |
| **e-sign** | Legally recognised electronic signature (Aadhaar eSign or DSC under the IT Act); pilot uses signed-PDF upload with hash (DEC-023) | Part 0 §0.4 |
| **e-invoice** | GST invoice registered on the government portal with an IRN; later scope (L-01) | Part 0A §C |
| **SOC 2** (System and Organization Controls 2) | US assurance framework; controls are aligned, no certification sought (ASSUMPTION-003) | Part 0 §0.7 |
| **HIPAA** (Health Insurance Portability and Accountability Act, US) | Not applicable: no protected health information by design (ASSUMPTION-003) | Part 0 §0.7 |
| **EU AI Act risk class** | Classification of each AI use under the EU AI Act; none of this product's uses is intended as high-risk (Part 7.3; verify) | Part 0 §0.11 |
| **Meta WhatsApp Business policy** | Platform rules: opt-in before business-initiated messages, approved templates, 24-hour service window (WA-R1…; ADR-039) | Part 0 §0.7 |
| **children's data** | Data of anyone under 18 (ASSUMPTION-016); no tracking, profiling or targeted ads (DEC-030; DPDP) | Part 0 §0.8 |

### 9.2.1.5 Source-pack terms (Parts 0B, 2.6–2.7, 3.4–3.6, 4.4, 6.8–6.10, 7.4, 8.3, 9.4–9.5)

| Term | Definition | First use |
|---|---|---|
| **source pack** | The client's 38-document engineering package; documents 01/02 are the BRD and FRD already used. Reviewed line by line in the enhancement parts (Part 0B) | Part 0B front matter |
| **OKPI** (Optimization KPI) | The source pack's optimization KPIs (document 38 KPI-01…35), renamed OKPI-01…35 so they never collide with business KPI-01…31; 21 are mandatory and block acceptance (DEC-178) | Part 0B 0B.1 What the source pack is and what it |
| **SPDEC** (Source-pack decision) | Engineering decision of document 24: SPDEC-001…180 retained, SPDEC-X-… expansion. Never a binding DEC; blueprint DECs take precedence (DEC-178) | Part 6.6 §6.6.9 |
| **SRC07-DEC** | Document 07 API decision, renamed from the pack's own DEC numbers (DEC-178) | Part 3.5a front matter |
| **SDEC-08** | Document 08 schema decision (SDEC-08-039…042), renamed (DEC-178) | Part 3.6a §3.6.1.1 |
| **RC-1…RC-3** (recovery classes) | RC-1 critical (business records, ledgers, consent, audit, outbox: RPO ≤ 15 min, RTO ≤ 4 h pilot, ≤ 2 h from the scale gate), RC-2 regenerable (evidence pages, embeddings, projections: 24 h / 8 h), RC-3 ephemeral (broker, cache, sessions: rebuilt ≤ 15 min). The single recovery scheme; DR-T1…T3 are aliases (DEC-158) | Part 2.6 §2.6.5.8.5 |
| **QC** (Quality control) | One of the source pack's 245 quality controls (document 23), mapped to blueprint gates, owners and tests in Part 6.9 and traced in the RTM (Part 6.6 §6.6.11) | Part 4.4a §4.4.1 |
| **QCL** (Quality-control layer) | One of the 31 layers that group the QCs (business requirements, UI/UX, REST operations, …), each with a sign-off role (Part 6.9) | Part 6.6 §6.6.11.3 |
| **UX-QC** | Expansion quality control and sign-off check UX-QC-01…10 (Part 4.4a, Part 6.9) | Part 4.4a §4.4.1 |
| **TRN-SCR** (Training task card) | Training task card for one screen, TRN-SCR-W01…W34 and TRN-SCR-A001…A113 (Part 8.3b) | Part 8.3a §8.3.3.2 |
| **TRN-EX** (Training exercise) | Role exercise with a worked answer, e.g. quotation calculation (Part 8.3b) | Part 8.3a §8.3.3.1 |
| **CSO** (Client service stage) | Client service stages and gates CSO-01…12, from contract/trial to offboarding (Part 8.3c §8.3.5.13.4) | Part 6.6 §6.6.9 |
| **SLA-01…12** | Terms of a SaaS client's service schedule (scope, availability, support hours, credits, …); a revision needs Service Owner and Legal approval (FR-ENH-J-005; DEC-209) | Part 6.6 §6.6.9 |
| **MNT** (Maintenance calendar item) | Recurring maintenance activity MNT-D (daily), W (weekly), M (monthly), Q (quarterly), A (annual), B (before update), R (release), I (after incident) (Part 8.3c §8.3.5.14.2) | Part 8.3a §8.3.3.4 |
| **PC-01…18** (Prompt contract) | Typed contract binding an AI responsibility to its input, output schema, refusal rules and agent (Part 7.4) | Part 6.6 §6.6.9 |
| **PG-01…10** (Procurement gate) | Evidence gates a paid or replacement integration must pass before activation, enforced by AU-044 (Part 7.4) | Part 6.6 §6.6.9 |
| **WP-01…03** (Workload profile) | Load-test design points: WP-01 release gates (50 sessions, 100k opportunities), WP-02 scale gate (250 sessions, 1M opportunities, 100k actions/day), WP-03 traffic mix (DEC-161) | Part 4.4a §4.4.3.1 |
| **FR-ENH** | Source-pack enhanced functional requirement FR-ENH-<group>-###; binding backlog item with the MoSCoW and release of Part 9.5 §9.5.2.3 (DEC-221, DEC-224) | Part 2.6 front matter |
| **TC-ENH** | Source-pack enhancement test case TC-ENH-<group>-###; group K holds the coverage-closure cases of Part 6.10. All are merged into the RTM (DEC-217) | Part 2.6 front matter |
| **LT-ENH** | Source-pack load or resilience test, indexed under WP-01…03; Part 6.1 keeps LT-01…12 (DEC-216) | Part 2.7a §2.7.3.1 |
| **VER** (Verification item) | Inspection, review, analysis or demonstration with owner, evidence and gate, used where a statement is not software behaviour; counted separately from test cases (Part 6.7, Part 6.10) | Part 6.6 §6.6.3.1 |
| **SIT alias** | Source SIT test SM-SIT-A001…A302 mapped to the blueprint stories, FRs and operation tests that verify it (Part 6.6 §6.6.11.2; DEC-217) | Part 3.5a §3.5.1.1 |
| **XBR** (Expansion scope statement) | XBR-01…05, the pack's five "added" BRs, mapped to BR-S138; no new BR (DEC-180) | Part 6.9a §6.9.3.1 |
| **FR-UX** | Per-screen field-specification alias FR-UX-<screen>, not a separate FR (DEC-180) | Part 0 §0.3.1 |
| **RGV** (Release-gate validator) | Fail-closed pipeline check RGV-01…15 on the evidence manifest (missing, duplicate, self-reviewed or N/A mandatory evidence) (Part 4.4b) | Part 4.4a front matter |
| **SMK** (Smoke check) | Post-deploy smoke check SMK-01…14; a failure triggers rollback (Part 4.4b) | Part 4.4a front matter |
| **RBK-T / RBK-R** | Rollback triggers and resume rules (Part 4.4b §4.4.5.7.1) | Part 4.4a §4.4.3.8 |
| **HO-T / HO-B / HO-A** | Delivery handover items: technical, business and access (Part 4.4b §4.4.5.7.2) | Part 4.4a §4.4.3.8 |
| **SEC-ROT** | Secret-rotation procedure SEC-ROT-01…08 with a quarterly drill (Part 4.4b) | Part 4.4a §4.4.3.4 |
| **TDR** (Technical-debt register) | Register of technical debt with owner, severity, estimate and target release, reviewed monthly (CS-DOC-05) | Part 4.4a §4.4.3.4 |
| **coding standard** | Binding rules CS-<family>-## (186 rules) with review checks CR-CHK-01…40 and custom Semgrep rules SG-01…12, enforced per the Part 4.4a enforcement matrix | Part 4.4a §4.4.3.1 |
| **contract state** | Lifecycle of an API operation contract: a route is mounted only from Implemented and enabled in production only from Verified (FR-ENH-D-001) | Part 3.5b §3.5.5.9.1 |
| **freshness class** | F-1 operational (≤ 60 s p95), F-2 analytical (≤ 15 min), F-3 scheduled; stale data is labelled (DEC-160) | Part 4.4b §4.4.5.4.4 |
| **Unassessed** | Verdict for a metric with no denominator or insufficient probe coverage; never shown as Pass or as zero (FR-ENH-I-050) | Part 2.7a §2.7.3.1 |
| **Option 2b** | Plan of record after the enhancements: two contract engineers from Sprint 3 to the Release 2 build gate; Release 1 go/no-go Fri 4 Jun 2027 (DEC-227, approved by DEC-228) | Part 8.4 front matter |
| **management reserve** | 10% of the central enhancement estimate plus the UX-TASK-FIELDS residual, drawn only through the change control board (DEC-225) | Part 3.4 §D |

<!-- GLOSSARY:END -->

---

## 9.2.2 ID registry

Every ID family used across the parts. **Actual range found** and **Distinct IDs** are computed by the script from all mentions, so a range can include an ID that is only cited [ASSUMPTION-214]. "Unused" counts numbers inside the range that never appear (for example, reserved numbers). **Defined in** lists the parts where table rows or headings start with the ID (the definition points); **Owning part** is the governing part per the baseline and Part 9.1.

<!-- GEN:IDREG:BEGIN -->

| Prefix | Meaning | Actual range found | Distinct IDs | Owning part | Defined in (most rows) | Parts citing |
|---|---|---|---|---|---|---|
| BR-M## | Business requirement derived from a BRD module line (M01–M66) | 01–66 | 66 | 1 (§1.12) | 1, 6.6, 5.2 | 39 |
| BR-S### | Business requirement derived from a source statement | 001–140 | 140 | 1 (§1.12) | 1, 6.6, 6.7 | 36 |
| BR-{group} | Group-level business requirement (tenant, website, automation, service, QA) | AUTO; QA; SVC; TENANT; WEB | 5 | 1 (§1.12) | 1, 6.6 | 33 |
| FR-W## | Functional requirement for Website/Portal screen W01–W34 | 01–34 | 34 | 2.1 (§2.4) | 2.1, 6.6, 5.3, 6.3b | 40 |
| FR-A### | Functional requirement for Admin Command Centre screen A001–A113 | 001–113 | 113 | 2.1 (§2.4) | 2.1, 6.6, 5.1c, 6.5 | 49 |
| FR-OP### | Operational/platform functional requirement (health, readiness, config) | 001–003 | 3 | 2.1 (§2.4) | 2.1, 6.6, 5.3, 6.3b | 25 |
| FR-{area}-## | Cross-cutting functional requirement by area (standards, data mgmt, UI states, filters, publication, adapters, …) | ADP 01; COP 01; CSM 01; DM 01–04; ENG 01; FLT 01–11; NEG 01; PUB 01; SRCH 01; STD 01–04; UIS 01–04 | 30 | 2.1 (§2.4) | 2.1, 6.6, 6.3a, 6.7 | 46 |
| NFR-### | Non-functional requirement | 001–099 | 99 | 0 (§0.6); detailed in 4.2 | 4.2, 6.6, 6.7, 0 | 63 |
| DEC-### | Binding decision (DEC-001…065 Part 0A; DEC-066…140 Part 9.1) | 001–421 (76 unused) | 345 | 0A, 9.1 | 9.1, 9.5, 9.6a, 0A | 68 |
| BRL-{domain}-## | Business rule, by rule domain | AI 01–12; APR 01–11; AUT 01–10; BID 01–06; CTR 01–05; ELG 01–18; FIN 01–08; LCY 01–06; MKT 01–10; MTG 01–06; ORD 01–06; PRV 01–07; PUB 01–06; QTE 01–07; SCR 01–09; SEQ 01–05; SRC 01–10; SVC 01–07; TEN 01–12 | 161 | 2.3 | 2.3, 6.5, 6.3a, 6.3b | 56 |
| R## | RBAC role (R01–R20; L suffix = startup-scoped lead variant) | 01–21; L 03–05 (1 unused) | 23 | 2.3 (§2.21) | 2.3, 8.3b, 7.3, 2.6 | 55 |
| P## | Persona | 01–90 (68 unused) | 22 | 1 (§1.6) | 1, 7.1, 2.6, 8.1 | 38 |
| KPI-## | Key performance indicator | 01–35 | 35 | 1 (§1.4) | 1, 8.2 | 54 |
| EP-## | Epic | 01–21 | 21 | 0 (§0.10.2); stories in 5 | 0, 6.6, 8.1, 5.2 | 47 |
| US-#### | User story (first two digits = epic) | 01 0001–0017; 02 0001–0008; 03 0001–0011; 04 0001–0008; 05 0001–0012; 06 0001–0008; 07 0001–0010; 08 0001–0015; 09 0001–0006; 10 0001–0007; 11 0001–0010; 12 0001–0010; 13 0001–0013; 14 0001–0012; 15 0001–0011; 16 0001–0012; 17 0001–0010; 18 0001–0015; … (21 families) | 230 | 5 | 5.3, 6.5, 5.2, 5.1b | 29 |
| AC-####-## | Acceptance criterion of a user story | AC-0101-01 … AC-2110-05 (story-scoped; numbering restarts per story) | 1356 | 5 | 6.4 | 16 |
| TS-##-## | Test scenario (epic-based, DEC-093) | 01 01–20; 02 01–08; 03 01–11; 04 01–08; 05 01–12; 06 01–08; 07 01–10; 08 01–18; 09 01–07; 10 01–08; 11 01–11; 12 01–11; 13 01–14; 14 01–13; 15 01–14; 16 01–11; 17 01–11; 18 01–17; 19 01–13; 20 01–13; 21 01–12 | 250 | 6 | 6.5, 6.3a, 6.2a, 6.2b | 7 |
| TC-##-### | Test case (epic-based, DEC-093) | 01 001–133; 02 001–057; 03 001–099; 04 001–056; 05 001–086; 06 001–056; 07 001–075; 08 001–191 (1 unused); 09 001–047; 10 001–060; 11 001–075; 12 001–083 (1 unused); 13 001–128; 14 001–101; 15 001–109; 16 001–084; 17 001–091; 18 001–138; 19 001–102; … (21 families) | 1979 | 6 | 6.5, 6.3a, 6.2a, 6.3b | 18 |
| TC-AI-AG###-### | AI agent test case (per agent; format per DEC-113) | 001 001–017; 002 001–024; 003 001–015; 004 001–021; 005 001–019; 006 001–018; 007 001–014; 008 001–016; 009 001–017; 010 001–014; 011 001–021; 012 001–018; 013 001–021; 014 001–019; 015 001–030; 016 001–016; 017 001–031; 018 001–019; 019 001–018; … (36 families) | 586 | 6 | 6.4 | 7 |
| TC-AU-AU###-### | Automation test case (per automation; DEC-113) | 001 001–005; 002 001–015 (1 unused); 003 001–004; 004 001–005; 005 001–005; 006 001–015; 007 001–004; 008 001–004; 009 001–003; 010 001–009; 011 001–004; 012 001–008; 013 001–003; 014 001–004; 015 001–004; 016 001–004; 017 001–004; 018 001–003; … (43 families) | 187 | 6 | 6.4 | 4 |
| AG-### | AI agent | 001–080 | 80 | 7.1/7.2 | 7.2, 6.4, 9.4, 9.7a | 29 |
| AU-### | Deterministic or AI-assisted automation | 001–119 | 119 | 7.1/7.2 | 9.4, 9.7b, 6.6, 7.1 | 23 |
| ADR-### | Architecture decision record | 001–139 (33 unused) | 106 | 3.1 (001–043), 4.1/4.3 (050–069), 7.3 (070–085) | 3.1, 7.3, 3.4, 9.7a | 29 |
| RSK-### | Risk (feeds the Part 8 risk register) | 001–379 (217 unused) | 162 | 8 (raised in 3–7) | 8.2, 7.3, 3.1, 4.1 | 19 |
| THR-### | STRIDE threat | 001–082 | 82 | 4.1 (§4.2.2) | 4.1, 6.4 | 13 |
| SC-## | Security control | 01–50 | 50 | 4.1 | 4.1, 6.4 | 14 |
| RB-### | Operational runbook | 001–018 | 18 | 4.3 | 4.3 | 22 |
| SLO-## | Service level objective | 01–12 | 12 | 4.2/4.3 | 4.3 | 11 |
| AL-## | Alert rule (AL-50…58 added in 4.4b) | 01–58 | 58 | 4.1/4.3, 4.4b | 4.3, 4.4b | 11 |
| LT-## | Load/performance test (DEC-092: owned by 6.1) | 01–16 (2 unused) | 14 | 6.1 | 6.1, 4.2 | 25 |
| DQ-### | Data quality check | 001–032 | 32 | 3.3 | 3.3 | 4 |
| API-### | API operation in the derived catalogue (555 ops, DEC-104) | 001–556 | 556 | 3.2 | 3.2 | 17 |
| NT-### | Internal notification type | 001–046 | 46 | 2.4 | 2.4 | 25 |
| NX-## | External (customer-facing) notification type | 01–15 | 15 | 2.4 | 2.4 | 12 |
| RP-## | Report/analytics view | 01–30 | 30 | 2.4 | 2.4 | 31 |
| SR-## | Search capability | 01–08 | 8 | 2.4 | 2.4 | 11 |
| CFG-## | Configuration domain | 01–32 | 32 | 2.4 | 2.4 | 38 |
| WF-## | End-to-end workflow / process flow | 01–39 (1 unused) | 38 | 2.2 | 9.4, 9.10, 9.7b, 2.2 | 47 |
| AP-## | Acceptance procedure (DEC-014) | 01–11 | 11 | 0A; tests in 6 | 6.1 | 41 |
| CAP-## | Business capability (capability map) | 01–20 | 20 | 2.1 | 2.1, 3.4 | 3 |
| CA-{code} | Acceptance profile applied to FRs (e.g. CA-PUB, CA-FIN) | ADMIN; AI; ALL; APPROVE; CONFIG; DISPATCH; FIN; INTAKE; PORTAL; PUB | 10 | 2.1 | 2.1 | 44 |
| J-## | User journey | 01–77 (27 unused) | 50 | 1 (§1.11) | 1, 9.5 | 9 |
| SH-## | Stakeholder | 01–14 | 14 | 1 | 1 | 3 |
| CN-## | Constraint | 01–15 | 15 | 1 | 1 | 10 |
| DP-## | External dependency | 01–15 | 15 | 1 | 1, 8.1 | 13 |
| X-## | Explicit exclusion (out of scope) | 01–12 | 12 | 1 | 1 | 9 |
| L-## | Later / future scope item (W6+) | 01–09 | 9 | 1 | 1, 3.5b | 8 |
| VH-## | Value hypothesis | 01–06 | 6 | 1 | 1 | 4 |
| PP-## | Product principle | 01–12 | 12 | 1 | 1 | 16 |
| PR-## | Problem statement | 01–10 | 10 | 1 | 1 | 1 |
| G-## | Business goal | 01–10 | 10 | 1 | 1 | 4 |
| OQ-### | Open question (all answered in 0A) | 001–030 | 30 | 0, 0A | 0, 0A | 3 |
| AMB-# | Ambiguity in the source (resolved DEC-049…058) | 1–10 | 10 | 0, 0A | 0 | 3 |
| E-## | Errata item (Part 9.1, E-01…); note E-# (one digit) = engine invariant in 2.2 | 01–96 (2 unused) | 94 | 9.1 | referenced only | 3 |
| ABAC-## | Attribute-based access control rule | 01–12 | 12 | 2.3 | 2.3 | 34 |
| ENT-### | Logical data entity | 001–200 | 200 | 3.3 | 3.3, 3.6a | 15 |
| CK-## | Database check constraint pattern | 01–24 | 24 | 3.3 | 3.3 | 4 |
| UQ-{kind}-## | Uniqueness/idempotency key or duplicate rule | DUP 01–05; IDEM 01–19 | 24 | 3.3 | 3.3 | 4 |
| AD-## | Architecture driver | 01–20 | 20 | 3.1 | 3.2, 3.1 | 14 |
| ARP-## | Architecture principle | 01–15 | 15 | 3.1 | 3.1 | 4 |
| FM-## | Failure mode (resilience analysis) | 01–17 | 17 | 3.1 | 3.1 | 5 |
| IP-## | Integration pattern | 01–10 | 10 | 3.2 | 3.2 | 6 |
| CT-## | Contract-test gate | 01–15 | 15 | 3.2 | referenced only | 7 |
| REC-## | Reconciliation job | 01–09 | 9 | 3.2 | referenced only | 2 |
| XR-{role}-## | Cross-role review finding | DBA 01–07; FIN 01–06; PO 01–05; QA 01–06; SEC 01–10; UX 01–06 | 40 | 3.2 | 3.2 | 1 |
| TB-## | Trust boundary | 01–12 | 12 | 4.1 | 4.1 | 3 |
| AZ-## | Authorization enforcement layer | 01–15 | 15 | 4.1 | 4.1 | 3 |
| SE-## | Security event (logged/alerted) | 01–18 | 18 | 4.1 | 4.1 | 6 |
| SO-# | Security objective | 1–8 | 8 | 4.1 | 4.1 | 3 |
| SI-# | Security incident class | 1–8 | 8 | 4.1 | referenced only | 2 |
| AIR-## | AI-specific risk (injection, leakage, …) | 01–12 | 12 | 4.1 | 4.1, 6.4 | 3 |
| DPIA-T# | DPIA trigger | 1–10 | 10 | 4.1 | 4.1 | 1 |
| {rule set}-R# | Regulatory or design rule set (EU/UK GDPR, IT Act, WhatsApp, PCI, TRAI, GST, Canada, index, reporting) | CA 1; EU 1–11; GST 1–5; IT 1–5; IX 1–7; PCI 1–4; RPT 1–10; TR 1–3; WA 1–7 | 53 | 4.1, 3.3, 2.4 | 4.1, 2.4, 3.3 | 18 |
| CH-## | Chaos/resilience experiment | 01–04 | 4 | 4.2 | 4.2 | 6 |
| PL-## | CI/CD pipeline stage | 01–44 (22 unused) | 22 | 4.3 | 4.3 | 12 |
| DB-## | Operational dashboard | 01–10 | 10 | 4.3 | 4.3 | 6 |
| DM-### | Story-dimension matrix row (Part 5.1a) | 001–057 | 57 | 5.1a | 5.1a | 2 |
| MAS-# / RR-# | Mandatory AC scenario / required-risk scenario (story template) | MAS 1–9; RR 1–8 | 17 | 5.1a | referenced only | 4 |
| TP-## | Test principle | 01–12 | 12 | 6.1 | 6.1 | 7 |
| QO-# | Quality objective | 1–10 | 10 | 6.1 | 6.1 | 3 |
| RA-## | Risk area (risk-based testing) | 01–30 | 30 | 6.1 | 6.1 | 8 |
| RBR-# | Release-blocking rule | 1–8 | 8 | 6.1 | 6.1 | 9 |
| PW-## | Pairwise test combination | 01–26 | 26 | 6.1 | 6.1 | 2 |
| EG-## | Error-guessing test idea | 01–20 | 20 | 6.1 | 6.1 | 10 |
| BVA-D## | Boundary-value analysis datum | 01–14 | 14 | 6.1 | 6.1 | 3 |
| DR-# | Disaster-recovery drill | 1–9 | 15 | 6.1 | 6.1 | 9 |
| CI-### | Candidate AI idea (discovery register) | 001–135 | 135 | 7.1 | 7.1 | 8 |
| TL-## | Agent tool in the tool registry | 01–32 | 32 | 7.2 | 7.2, 9.7a | 12 |
| D0# | Delivery persona (delivery-lifecycle AI) | 01–06 | 6 | 7.1 | 7.1 | 9 |
| B## | Budget line (cost table; GAP-006, DEC-020) | 01–24 | 24 | 0, 0A, 8 | 8.2, 7.4a | 51 |
| UX-## | UX principle | 01–09 | 9 | 2.5 | 2.5 | 6 |
| I18N-## | Internationalization rule | 01–11 | 11 | 2.4 | 2.4 | 11 |
| OPT-##-## | FRD optimisation item (source ID, cited) | 01 01–08; 02 01–07; 03 01–08; 04 01–08; 05 01–07; 06 01–05; 07 01–05; 08 01–06; 09 01–05; 10 01–06; 11 01–05; 12 01–04; 13 01–04; 14 01–03; 15 01–04; 16 01–03; 17 01–04; 18 01–04; 19 01–04; 20 01–04 | 104 | Source (FRD) | 8.3c, 3.4, 4.4a, 2.6 | 47 |
| SM-UT-### | Source test alias (FRD; aliases only, DEC-094) | 001–066 | 66 | Source (FRD); 6 | 6.8b, 6.8a | 10 |
| M## | Source module M01–M66 (BRD §7) | 01–66 | 66 | Source (BRD) | 6.9a | 53 |
| W## / A### | Screen ID: Website/Portal W01–W34, Admin A001–A113 | A 001–302 (121 unused); W 001–090 (38 unused) | 233 | Source (FRD §16.2); 2.5 | 8.3a, 2.5, 9.8a, 9.7b | 66 |
| FR-ENH-{G}-### | Source-pack enhanced functional requirement; group letter = enhancement part (A 2.6, B 3.4, C 2.7, D 3.5, E 3.6, F 7.4, H 6.9, I 4.4, J 8.3) | A 001–020; B 001–027; C 001–017; D 001–020; E 001–008; F 001–031; H 001–010; I 001–083 (58 unused); J 001–022 | 180 | 2.6, 2.7, 3.4–3.6, 4.4, 6.9, 7.4, 8.3 | 6.6, 8.3c, 7.4b, 4.4b | 28 |
| NFR-ENH-{G}-## | Source-pack non-functional requirement (growth scale, recovery by class, unit cost) | B 01–08 | 8 | 3.4 | 3.4, 6.6 | 5 |
| US-##-E{G}## | Source-pack enhancement user story (epic, group letter, sequence) | 01-EA 01; 01-EB 01–05; 01-EC 01; 01-ED 01–02; 01-EE 01; 01-EF 01; 01-EI 01–02; 01-EJ 01–03; 02-EF 01; 03-EA 01; 03-EB 01; 03-ED 01; 04-EB 01–02; 04-EC 01; 04-EF 01–05; 04-EI 01; 04-EJ 01; 05-EA 01–04; 05-ED 01; 05-EF 01; 06-EA 01; 08-EA 01–02; … (66 families) | 135 | 2.6–8.3 enhancement parts | 6.6, 2.6, 3.4, 8.3c | 15 |
| AC-##E{G}##-## / AC-##-E{G}##-## | Acceptance criterion of an enhancement story | 01-ED01 01–03; 01-ED02 01–04; 01-EF01 01–03; 01EA01 01–02; 01EB01 01–03; 01EB02 01–02; 02-EF01 01–02; 03-ED01 01–02; 03EA01 01–02; 03EB01 01–02; 04-EF01 01–04; 04-EF02 01–03; 04-EF03 01–03; 04-EF04 01–03; 04-EF05 01–02; 04EB01 01–02; 04EB02 01; … (77 families) | 178 | 2.6–8.3 enhancement parts | referenced only | 6 |
| TC-ENH-{G}-### | Source-pack enhancement test case (D-C candidate, D-E enhancement-operation, D-N negative family; K = coverage closure, Part 6.10) | A- 001–050; B- 001–040; C- 001–247 (80 unused); D- 001–302; D-C 001–019; D-E 001–024; D-N 001–022; E- 001–036; F- 001–040; G- 001–045; H- 001–036; I- 001–077 (36 unused); J- 001–066; K- 001–077 (13 unused) | 952 | 2.6–8.3 enhancement parts; 6.10 | 3.5b, 6.10, 8.3c, 2.6 | 25 |
| LT-ENH-{G}-## | Source-pack load/resilience test (indexed under WP-01…03, DEC-161/216) | B 01–04; C 01; I 01–06 | 11 | 2.7a, 3.4, 4.4b | 6.6, 4.4b, 3.4, 6.10 | 9 |
| TC-{NFR/FLT/BRS}-### | Coverage-closure test case (NFR gate, filter suite, BR-S) | BRS 001–013; FLT 001–045; NFR 001–099 | 157 | 6.7 | 6.7 | 7 |
| VER-### | Verification item (inspection, review, analysis, demonstration); not a test case | 001–048 | 48 | 6.7 | 6.7 | 2 |
| VER-ENH-K-### | Source-pack closure verification item | 001–027 (7 unused) | 20 | 6.10 | 6.10 | 2 |
| OKPI-## | Optimization KPI of the source pack (document 38 KPI-01…35, renamed to avoid KPI-01…31; 21 mandatory) | 01–35 | 35 | 4.4a, 6.9a, 8.3c | 4.4a, 6.6, 8.3c, 6.9a | 24 |
| QC-##/### | Source-pack quality control (document 23; 245 QCs) | 001–999 (763 unused) | 238 | 6.9a/b | 6.6, 6.9b, 6.9a | 10 |
| QCL-## | Quality-control layer (document 23; 31 layers with sign-off role) | 01–31 | 31 | 6.9a/b | 6.6, 6.9a, 6.9b | 5 |
| UX-QC-## | Expansion quality control and sign-off check | 01–10 | 10 | 4.4a, 6.9 | 4.4a, 6.6, 6.9b, 6.9a | 8 |
| SPDEC-### / SPDEC-X-… | Source-pack engineering decision of document 24 (180 retained + expansion), never a binding DEC (DEC-178) | 001–180; X | 184 | 6.9b; 9.5 | 6.9a | 4 |
| SRC07-DEC-### | Document 07 API decision, renamed (DEC-178) | 001–038 | 38 | 3.5b | 3.5b | 4 |
| SDEC-08-### | Document 08 schema decision, renamed (DEC-178) | 039–042 | 4 | 3.6b | 3.6a | 4 |
| SM-SIT-{A/F/M}### | Source SIT test alias (A = operation, F = flow, M = module) | A 001–302; F 001–035; M 001–066 | 403 | 3.5, 6.8, 6.9 | 6.8b, 6.6, 6.8a | 8 |
| SM-UAT-{S/F}### | Source UAT test alias (S = screen, F = flow) | F 001–017; S 001–138 | 155 | 6.1, 6.8 | 6.8b, 6.8a | 15 |
| SM-OP-### | Source API/adapter operation (document 07) | 001–302 | 302 | 3.5a/b | 3.5a, 3.5b | 4 |
| SM-UX-API-## | Source expansion-interface API candidate | 01–19 | 19 | 3.5b | 3.5b, 3.5a | 7 |
| SM-FR-{W/A/OP}… | Source FR alias of FR-W/FR-A/FR-OP (DEC-017) | A 001–113; OP 001–003; W 001–034 | 150 | 6.9a | 6.9a | 5 |
| SM-UX-FR- / FR-UX- | Per-screen field-specification alias, not a separate FR (DEC-180) | A 001–113; W 001–034 | 294 | 6.9a; 9.5 | referenced only | 5 |
| SM-UX-UAT- | Per-screen UAT alias | A 001–113; W 001–034 | 147 | 6.1; 6.8 | 6.8b | 11 |
| SM-UX-SIT-X## | Source expansion SIT check | 01–10 | 10 | 6.8 | 6.8b, 6.8a | 3 |
| API-ENH-{G}-### | Enhancement API operation | D 001–024; I 001–002 | 26 | 3.5b, 4.4b | 3.5b | 6 |
| {family}-ENH-{G}-## | Enhancement item extending a baseline family (rule, ABAC, configuration, KPI, report, acceptance procedure, entity, index, check, runbook, risk) | ABAC-ENH-A 01–05; AP-ENH-A 01–12 (1 unused); BRL-ENH-A 01–14; CFG-ENH-A 01–08; CK-ENH-E 01–12; ENT-ENH-E 01–04; ENT-ENH-H 01–07; ENT-ENH-J 01–03; IX-ENH-E 01–58 (3 unused); KPI-ENH-A 01–05; RB-ENH-B 01–03; RB-ENH-H 01–03; RP-ENH-A 01–04; RSK-ENH-95 01–06; … (15 families) | 144 | 2.6, 3.6, 6.9, 9.5 | 3.6a, 2.6, 3.6b, 6.9b | 14 |
| XBR-## | Expansion scope statement mapped to BR-S138 (no new BR; DEC-180) | 01–05 | 5 | 9.5 | referenced only | 5 |
| RC-# | Recovery class: RC-1 critical, RC-2 regenerable, RC-3 ephemeral (DEC-158) | 1–3 | 3 | 3.4; 4.4b; 9.5 | referenced only | 10 |
| DR-T# | Recovery tier of Part 3.6b, alias of RC (DEC-158) | 1–3 | 3 | 3.6b | referenced only | 3 |
| WP-## | Load-test workload profile (WP-01 release gates, WP-02 scale gate, WP-03 traffic mix; DEC-161) | 01–03 | 3 | 4.4b; 9.5 | referenced only | 6 |
| PC-## | Typed AI prompt contract (PC-01…18) | 01–40 | 40 | 7.4a/b | 7.4a | 8 |
| PG-## | Integration procurement/activation gate (PG-01…10, AU-044) | 01–10 | 10 | 7.4a/b | 7.4b | 8 |
| IC-### | Integration candidate of the capability replacement register | 001–538 (391 unused) | 147 | 7.4a | 7.4a | 4 |
| AL-##.# | Automation-library use case (20 groups × 5) | 01 1–5; 02 1–5; 03 1–5; 04 1–5; 05 1–5; 06 1–5; 07 1–5; 08 1–5; 09 1–5; 10 1–5; 11 1–5; 12 1–5; 13 1–5; 14 1–5; 15 1–5; 16 1–5; 17 1–5; 18 1–5; 19 1–5; 20 1–5 | 100 | 7.4b | referenced only | 2 |
| TPL-## | Automation-library industry template | 01–20 | 20 | 7.4b | 7.4b | 2 |
| SLA-## | SaaS SLA schedule term (SLA-01…12) | 01–12 | 12 | 8.3c | referenced only | 5 |
| CSO-## | Client service stage and gate (CSO-01…12) | 01–12 | 12 | 8.3c | referenced only | 3 |
| MNT-{cadence}## | Recurring maintenance activity (D daily, W weekly, M monthly, Q quarterly, A annual, B before update, R release, I after incident) | A 01–05; B 01–02; D 01–06; I 01; M 01–10 (1 unused); Q 01–07; R 01; W 01–07 | 38 | 8.3c | 8.3c | 2 |
| TRN-SCR- | Training task card per screen | A 001–113; W 001–034 | 147 | 8.3b | 8.3b | 2 |
| TRN-EX-## | Training exercise with worked answer | 01–16 | 16 | 8.3b | referenced only | 3 |
| TM-## | Training module | 01–33 | 33 | 8.3a/b | 8.3b | 4 |
| LJ-## | Role learning journey (document 33) | 01–16 | 16 | 8.3b | 8.3b | 3 |
| OPT-## / OPT-TEST-## | Optimization dimension (21) / optimization test scenario (24) of document 38 | 01–20; TEST | 44 | 4.4a, 8.3c | 8.3a, 8.3c | 10 |
| CS-{family}-## | Coding-standard rule, by family (186 rules) | A11Y 01–06; ADP 01–07; AI 01–08; AIC 01–08; API 01–12; DEP 01–08; DJ 01–10; DOC 01–06; GEN 01–08; GIT 01–08; MIG 01–06; OBS 01–06; PERF 01–08; PY 01–09; RE 01–12; REV 01–12; SEC 01–12; SQL 01–09; TEST 01–10; TS 01–10; WRK 01–10 | 185 | 4.4a | 4.4a | 6 |
| CR-CHK-## | Code-review checklist item | 01–40 | 40 | 4.4a | 4.4a | 1 |
| SG-## | Custom Semgrep rule | 01–78 (64 unused) | 14 | 4.4a/b | referenced only | 5 |
| RGV-## | Release-gate validator rule (PL-17) | 01–15 | 15 | 4.4b | 4.4b | 4 |
| SMK-## | Post-deploy smoke check | 01–14 | 14 | 4.4b | 4.4b | 4 |
| DPL-{PRE/SEQ/ACT}-## | Deployment pre-check, sequence step or activation stage | ACT 01–06; PRE 01–10; SEQ 01–09 | 25 | 4.4b | 4.4b | 2 |
| RBK-{T/R}## | Rollback trigger / resume rule | R 01–05; T 01–08 | 13 | 4.4b | 4.4b | 2 |
| HO-{T/B/A}## | Delivery handover item (technical, business, access) | A 01–06; B 01–06; T 01–10 | 22 | 4.4b | 4.4b | 3 |
| ACC-## / SEC-ROT-## / ENV-## | Access-lifecycle rule / secret-rotation step / configuration-contract item | ACC 01–07; ENV 01–24; SEC-ROT 01–08 | 39 | 4.4b | 4.4b | 5 |
| PT-{ROE/FND}-## | Penetration-test rule of engagement / finding-record field | FND 01–10 (8 unused); ROE 01–12 | 14 | 4.4b | 4.4b | 3 |
| SVM-## / MET-## / SUP-## | Security verification matrix row / metric / support-operations rule | MET 01–12; SUP 01–08; SVM 01–12 | 32 | 4.4b | 4.4b | 3 |
| LT-SAFE-## / LTR-## | Load-test safety rule / load-test record field | LT-SAFE 01–05; LTR 01–14 | 19 | 4.4b | 4.4b | 2 |
| GL-{area}## | Go-live checklist item by area (B business, C compliance, D data, E enhancement, L legal, P people, S security, T technical) | A 01–07; B 01–07; C 01–08; D 01–06; E 01–06; L 01–06; P 01–05; S 01–09; T 01–10 | 64 | 8.2; 4.4b | 8.2, 4.4b | 13 |
| BLK-# | Activation blocker (BRD §11) | 1–11 | 11 | 8.2; 6.9 | 8.2 | 7 |
| WQG-## | Workflow quality gate (graph, node, schedule checks) | 01–12 | 12 | 3.4 | referenced only | 2 |

<!-- GEN:IDREG:END -->

**Reading notes.**
1. `R##` includes the startup-scoped lead variants R03L and R05L (family "L"). `P##` also matches priority labels such as P0/P1 only when two digits are used. Treat its range as personas P01–P16 (Part 1 §1.6).
2. `B##` budget lines and `B-##` cost rows in Part 3.1 §3.1.6 are different families (see §9.2.6).
3. `M##`, `W##`, `A###` and `OPT-##-##` are **source IDs** from the BRD/FRD, listed so the registry is complete. They are cited, not issued.
4. `E-##` errata IDs (Part 9.1) and `E-#` one-digit engine invariants (Part 2.2 §2.2) share a prefix but not a format.

---

## 9.2.3 Tag numbers issued, by issuing part

The programme allocates a tag number range to each batch. The table below is **generated** from the tags actually issued (a tag's issuing part is the part whose register row defines it; else the part of first use). It replaces a hand-kept allocation log, which the baseline does not contain [GAP-180]. This batch's own allocation is ASSUMPTION-210…214 and GAP-180…182.

<!-- GEN:ALLOC:BEGIN -->

| Issuing part | ASSUMPTION | GAP | CONFLICT | RECOMMENDATION | Tags |
|---|---|---|---|---|---|
| Part 0 | 000–020 | 001–034 | 001–014 | 001–018 | 87 |
| Part 1 | — | — | — | 019 | 1 |
| Part 2.3 | — | — | — | 020–021 | 2 |
| Part 2.4 | — | — | — | 022–026 | 5 |
| Part 2.5 | — | — | — | 027–028 | 2 |
| Part 2.6 | 300–309 | 300–310 | 300–304 | 300–315 | 42 |
| Part 2.7a | 340–345 | 340–349 | 340–351 | 340–349 | 38 |
| Part 3.1 | 101–106, 109–110 | 101–102, 104, 107 | 101–102 | 029–030, 035 | 17 |
| Part 3.2 | 107–108 | 103, 105 | 103 | 031–034 | 9 |
| Part 3.3 | 111–119 | 111–116 | 106–109 | 036–039 | 23 |
| Part 3.4 | 320–325 | 320–335 | 320–330 | 320–331 | 45 |
| Part 3.5b | 360–366 | 360–367 | 360–372 | 360–371 | 40 |
| Part 3.6a | — | — | — | 380 | 1 |
| Part 3.6b | 396–397 | 388–395 | 380–387 | 398–399 | 20 |
| Part 4.1 | 120, 128 | 120–121, 124–125 | 111, 114 | 041–044, 048–049 | 14 |
| Part 4.2 | 124–125 | — | 112–113 | 040, 046 | 6 |
| Part 4.3 | 121–123, 126 | 122–123, 126–127 | 110 | 045, 047 | 11 |
| Part 4.4b | 460–464 | 460–469 | 460–473 | 460–473 | 43 |
| Part 5.1c | 150–159 | 150–154 | 130–132 | 050–053 | 22 |
| Part 5.2 | 160–169 | 155–159 | 133–135 | 054–056 | 21 |
| Part 5.3 | 170–179 | 160–164 | 136–138 | 057–059 | 21 |
| Part 6.1 | 180–184 | 165–167 | — | 070–074 | 13 |
| Part 6.2a | 185–187 | — | — | 075–076 | 5 |
| Part 6.3a | 188–190 | — | — | 077–078 | 5 |
| Part 6.4 | 191–193 | 168–169 | — | 079 | 6 |
| Part 6.5 | 194–196 | 170–171 | — | — | 5 |
| Part 6.6 | — | 172 | — | 080, 090 | 3 |
| Part 6.7 | 215–218 | — | — | — | 4 |
| Part 6.8c | 420–424 | 420–425 | 420–424 | 420–425 | 22 |
| Part 6.9b | 440–446 | 440–453 | 440–447 | 440–449 | 39 |
| Part 6.10 | 510–514 | 510–514 | — | — | 10 |
| Part 7.1 | 146 | 143 | — | 061 | 3 |
| Part 7.3 | 140–145, 147 | 140–142, 144–145 | 120–122 | 060, 062–069 | 24 |
| Part 7.4b | 400–405 | 400–412 | 400–412 | 400–416 | 49 |
| Part 8.1 | 197–205, 207, 209 | 173–174, 176–177 | 140–142 | 081–087 | 25 |
| Part 8.2 | 206, 208 | 175, 178–179 | 143–144 | 088–089 | 9 |
| Part 8.3c | 480–490 | 480–490 | 480–491 | 480–490 | 45 |
| Part 9.1 | — | 180–182 | — | — | 3 |
| Part 9.5 | 500–509 | — | — | 500–509 | 20 |
| Part 9.6a | 520–523 | 520 | — | 520–521 | 7 |
| Part 9.6b | 550–556 | — | 550–556 | 550–552 | 17 |
| Part 9.7b | 600–609 | 610–617 | 620–623 | 625–641 | 39 |
| Part 9.8b | 650, 653–654, 656, 662–663, 666 | 660–661, 665 | 657–659 | 651–652, 655, 664, 667–670 | 21 |
| Part 9.9a | — | — | — | 700 | 1 |
| Part 9.9b | 700–706 | 710–714 | 720–726 | 730–738, 741, 744 | 30 |
| Part 9.10 | 750–752 | — | — | 750–753 | 7 |

<!-- GEN:ALLOC:END -->

---

## 9.2.4 Consolidated registers

### 9.2.4.0 Summary

<!-- GEN:TAGSUMMARY:BEGIN -->

| Register | Tags found | Resolved / accepted / closed / cited by DEC | Other status |
|---|---|---|---|
| Assumption | 238 | 16 | 222 |
| Gap | 222 | 62 | 160 |
| Conflict | 165 | 165 | 0 |
| Recommendation | 257 | 257 | 0 |

ADR index: **106** ADRs. DEC index: **345** decisions. Parts scanned: **69** (0–9.10).

<!-- GEN:TAGSUMMARY:END -->

### 9.2.4(a) ASSUMPTION register

Status "Cited by DEC-…" means a DEC row in Part 0A or 9.1 cites the assumption (for example ASSUMPTION-002 adopted by DEC-031, ASSUMPTION-166 resolved by DEC-070). "Retained (Part 0A §G)" covers ASSUMPTION-000…020. Otherwise the validation owner and status in the issuing part apply.

<!-- GEN:ASSUMPTION:BEGIN -->

| ID | First seen | Statement (from the issuing register, else text near the tag) | Status |
|---|---|---|---|
| ASSUMPTION-000 | 0 §0.1.2 | Section numbering convention per 0.1.2 | Retained (Part 0A §G) |
| ASSUMPTION-001 | 0 §0.7 | Industry/domain: multi-vertical B2B/B2C commercial growth SaaS covering AI services, wellness-tech partnerships, ed-tech and agri-commerce; the product itself is vertical-agnostic via templates | Retained (Part 0A §G) |
| ASSUMPTION-002 | 0 §0.4 | Scale (planning): Year 1 has 25–40 startup workspaces, 2–10 external tenants, 15–60 internal users, ≤ 500 portal users/month, ≤ 5,000 public sessions/month. Pilot volumes from BRD §8 (500 fetches, 100 reviewed signals, 2,000 emails, 1,000 WhatsApp … | Cited by DEC-031 |
| ASSUMPTION-003 | 0 §0.7 | Geography and regulation: India primary (Odisha, Tamil Nadu), with worldwide outreach for AppNAI. Applicable: India DPDP Act 2023 + DPDP Rules (verify notified commencement dates as of implementation); IT Act 2000; TRAI TCCCPR 2018 for commercial SMS/voice … | Retained (Part 0A §G) |
| ASSUMPTION-004 | 0 §0.7 | Cloud: AWS, region ap-south-1 (Mumbai) primary; backups copied to a second Indian region (ap-south-2 Hyderabad, verify service availability) | Retained (Part 0A §G) |
| ASSUMPTION-005 | 0 §0.7 | Stack: React + TypeScript, Django + DRF, PostgreSQL with RLS and pgvector, Celery + Celery Beat, Valkey, S3-compatible object storage, AWS Secrets Manager. Exact versions are "verify at implementation" | Retained (Part 0A §G) |
| ASSUMPTION-006 | 0 §0.7 | Team: 1 backend, 1 frontend, 0.5 QA, 0.5 growth/compliance lead, plus founder/CTO as Product Owner and architect. Scrum, 2-week sprints | Retained (Part 0A §G) |
| ASSUMPTION-007 | 0 §0.7 | Budget: engineering ₹13.05–32.93 L; monthly run ₹16,675 (base) to ₹31,165 (with Apollo + dev seats); ads, staff and taxes excluded | Retained (Part 0A §G) |
| ASSUMPTION-008 | 0 §0.7 | Monthly AI budget ceiling: ₹3,000 production inference at pilot base (≈ USD 33 at ₹90/USD; FX to verify). Part 7 also shows the ceiling needed at growth volume | Retained (Part 0A §G) |
| ASSUMPTION-009 | 0 §0.5 | Opportunity score = 100 × Σ(weight × normalized component); unknown ≠ 0 | Retained (Part 0A §G) |
| ASSUMPTION-010 | 0 §0.7 | Autonomy mapping: Manual = L0 (suggest only), Assisted = L1 (draft for approval), Supervised = L2 (act with post-review, limited to routine eligible actions), Controlled Autonomous = L3 (act within guardrails). Consequential actions (formal offers, … | Retained (Part 0A §G) |
| ASSUMPTION-011 | 0 §0.7 | English (en-IN) at launch; UI strings externalized; content locale per publication; Hindi, Tamil and Odia candidates for Wave 5+ | Retained (Part 0A §G) |
| ASSUMPTION-012 | 0 §0.7 | Base currency INR; multi-currency amounts stored as Decimal + ISO 4217; FX snapshot recorded per document; no automatic FX conversion of actuals | Retained (Part 0A §G) |
| ASSUMPTION-013 | 0 §0.4 | Existing auth is Django-based and can issue product-audience tokens/sessions (OIDC-compatible) with MFA | Retained (Part 0A §G) |
| ASSUMPTION-014 | 0 §0.4 | Channels: responsive web (desktop-first Admin, mobile-first Website/Portal) plus REST API for integrations; no native mobile apps | Retained (Part 0A §G) |
| ASSUMPTION-015 | 0 §0.4 | Payments via a hosted-checkout Indian gateway behind a provider-agnostic adapter; the platform never stores card or bank secrets | Retained (Part 0A §G) |
| ASSUMPTION-016 | 0 §0.7 | Anyone under 18 is a child for DPDP purposes. EduVerse acquisition targets guardians, institutions and adult learners; no profiling or targeted advertising to children | Retained (Part 0A §G) |
| ASSUMPTION-017 | 0 §0.7 | Data hosted in India by default (not asserted as a legal mandate; verify) | Retained (Part 0A §G) |
| ASSUMPTION-018 | 0 §0.4 | Provisional retention defaults (legal to confirm): financial/invoice records 8 years (verify Companies Act/GST requirements); contracts life + 8 years; audit log 7 years; marketing contact data 24 months after last eligible interaction; suppression list … | Cited by DEC-028 |
| ASSUMPTION-019 | 0 §0.7 | "Existing login/security reuse" excludes the cost of new MFA/IdP features; any new auth work is a change request | Cited by DEC-019 |
| ASSUMPTION-020 | 0 §0.7 | Delivery-lifecycle AI tooling (Claude Code seats) is a developer tool, not a runtime entitlement, and is budgeted separately (₹3,600) | Retained (Part 0A §G) |
| ASSUMPTION-101 | 3.1 front matter | Currency conversion at ₹90 per USD for all cost estimates (as BRD §6 does for seats) | Open; FinOps updates monthly |
| ASSUMPTION-102 | 3.1 §3.1.12.1 | Workload profile for the capacity model (peak active share 0.5, 20 Admin requests/min, portal 4 sessions × 10 min, 3 origin calls per public session, peak factor 5) | Replace with W2 measurements |
| ASSUMPTION-103 | 3.1 ADR-007 pgvector instead of an external | The capacity model adopts the Part 3.3 §3.3.10 volume drivers (messages, domain events, model runs, fetches, vector chunks) without independent re-derivation | Re-check when Part 3.3 estimates change |
| ASSUMPTION-104 | 3.1 §3.1.7.5 | The reused IdP supports OIDC authorization code + PKCE, JWKS, refresh-token rotation, revocation and max_age/acr_values step-up | Verified by Sprint 0 spike (DEC-019) |
| ASSUMPTION-105 | 3.1 §3.1.6.2 | Pilot processes fit a 4 GiB t4g.medium (≈ 3.0 GiB peak) | Validate by load test in W0 |
| ASSUMPTION-106 | 3.1 §3.1.6.2 | Staging runs ≤ 60 h/week | PO/QA to confirm UAT hours |
| ASSUMPTION-107 | 3.1 §3.1.16 | FRD-named legacy paths are mounted under /api/v1/ exactly as named (FR-OP001–003 show the prefix); /health and /ready also served unprefixed | Validate against any existing integration consumers |
| ASSUMPTION-108 | 3.2 front matter | Provider quotas, prices, API versions, sandbox availability and signature schemes quoted are unverified planning values | Verify at procurement/implementation |
| ASSUMPTION-109 | 3.1 ADR-010 Publication snapshots on S3 + Cl | Publication latency ≤ 5 minutes from approval to live (≤ 50 pages) is acceptable to marketing | Marketing lead to confirm |
| ASSUMPTION-110 | 3.1 §3.1.6.2 | AWS figures exclude GST, consistent with BRD §6 "taxes excluded" | Finance to confirm treatment |
| ASSUMPTION-111 | 3.3 §3.3.3.4 | The "6 candidate entities" are Trigger, ConflictCase, ConfigRevision, NodeTemplate, WorkflowTemplate and ApplicationDraft | Open — validate per source part |
| ASSUMPTION-112 | 3.3 §3.3.10.1 | Volume drivers: active outbound share 25% (Y1) / 40% (Y2), 4 delivery events per message, 120 audited actions per user-day, 150/300 gateway calls per active startup-day, document, organization and job counts as tabulated | Open — validate per source part |
| ASSUMPTION-113 | 3.3 §3.3.5.1 | PostgreSQL 17 on Amazon RDS with pgvector ≥ 0.8, pg_trgm, pg_partman, pgcrypto available (verify) | Open — validate per source part |
| ASSUMPTION-114 | 3.3 §3.3.10.3 | Average row sizes and the 1.6 overhead factor used for storage estimates | Open — validate per source part |
| ASSUMPTION-115 | 3.3 §3.3.11.1 | Financial retention clock starts at the end of the financial year; 35-day backups are not used to meet long retention or legal hold | Cited by DEC-159 |
| ASSUMPTION-116 | 3.3 §3.3.12.1 | Seed data for the four startups exists as spreadsheets/founder snapshots (no legacy database) | Open — validate per source part |
| ASSUMPTION-117 | 3.3 §3.3.8.3 | Full-text uses english for English and simple for Hindi, Tamil and Odia, supplemented by trigram search | Open — validate per source part |
| ASSUMPTION-118 | 3.3 §3.3.16.7 | Learners and guardians are Contact rows (person_type), not a separate entity | Open — validate per source part |
| ASSUMPTION-119 | 3.3 §3.3.6.12 | SaaS usage is metered in hourly aggregate buckets per meter and workspace | Open — validate per source part |
| ASSUMPTION-120 | 4.1 front matter | Application containers run on Amazon ECS (EC2 or Fargate launch type) behind an Application Load Balancer, with TLS inside the VPC. Part 3 may choose otherwise; controls here are platform-neutral except where marked | Reconcile with Part 3 ADRs (DevOps) |
| ASSUMPTION-121 | 4.3 §4.33.1 | GitHub (named in FRD §6 M09) is the SCM and CI platform; free-plan Actions minutes suffice with caching (verify) | Sprint 0 |
| ASSUMPTION-122 | 4.3 §4.34 | OpenTofu is acceptable as the IaC tool (RECOMMENDATION-010 names Terraform/OpenTofu) pending the Part 3 ADR | Reconcile with Part 3 |
| ASSUMPTION-123 | 4.3 §4.43.2 | On-call is staffed by three engineers in weekly rotation with the Founder as secondary; outside support hours only Sev1 pages, best effort | PO confirmation |
| ASSUMPTION-124 | 4.2 §4.25.1 | Traffic model parameters (§4.25.2) and Year 2 per-workspace scaling of message and research volumes | Validate with W2–W5 production telemetry; revise at W5 |
| ASSUMPTION-125 | 4.2 §4.25.4 | AI calls per unit of work (§4.25.4): 2 per fetch, 30% personalized drafts, 10% inbound ratio, 5% chat use, 40% Copilot adoption, 20% Tier 0 | Validate in W1–W3; Part 7 refines per agent |
| ASSUMPTION-126 | 4.3 §4.46.3 | Shared infrastructure costs are allocated by usage drivers (requests, task-seconds, storage) rather than per-tenant resources | FinOps review at W5 |
| ASSUMPTION-128 | 4.1 §4.10.2 | Regulatory timing and content as understood on 27 Nov 2026: DPDP Rules notified Nov 2025 with most obligations from about May 2027; CERT-In 6-hour reporting and 180-day log retention; Amazon Time Sync acceptable as a traceable time source; internal … | Counsel confirmation before W2 (DP-12) |
| ASSUMPTION-140 | 7.1 front matter | Per-call token sizes in §7.2 and a 25% overhead allowance are estimates until measured; replace with usage data after 30 days in W1 | Open — validate per source part |
| ASSUMPTION-141 | 7.2 AG-015 Admin Copilot | Pilot Copilot usage: 8 active internal users × 3 turns × 22 working days; 20-turn daily cap | Open — validate per source part |
| ASSUMPTION-142 | 7.3 §7.5.5 | Call volumes derived from BR-S089 (15% duplicate pages; ≈ 600 inbound/month; 30% rule-resolved; 150 personalised drafts; ≈ 100 public chats) | Open — validate per source part |
| ASSUMPTION-143 | 7.3 §7.5.5 | Growth gate ≈ 4× and scale ≈ 12× pilot volume for owned-portfolio AI | Open — validate per source part |
| ASSUMPTION-144 | 7.3 §7.5.5 | FX ₹90/USD (BRD §6) and Anthropic prices from the reference cached 3 Nov 2026 | Open — validate per source part |
| ASSUMPTION-145 | 7.3 §7.5.5 | Cache-hit rates: interactive 60–70%, batch 30–40% | Open — validate per source part |
| ASSUMPTION-146 | 7.1 §7.1.2 | Delivery personas D01–D06 are derived from the DEC-005 team (PO/architect, backend, frontend, QA 0.5, DevOps 0.5, growth/compliance 0.5) | Open — validate per source part |
| ASSUMPTION-147 | 7.3 §7.5.5 | Token estimates are in target-model tokens (Haiku 5.5 tokenizer ≈ 30% more tokens than older tokenizers) | Open — validate per source part |
| ASSUMPTION-150 | 5.1a front matter | 1 SP ≈ 0.5–1.0 pd, central 0.7; velocity = 4.0 FTE × 10 days × 0.8 ÷ pd-per-SP = 32–64 SP/sprint, planning value 40–46 SP | Open — validate per source part |
| ASSUMPTION-151 | 5.1a §5.7.4 | IaC baseline, CI skeleton and flag framework (Sprint 0) are booked to EP-01; EP-21 should reduce its indicative 25 pd by ≈ 5–6 pd | Open — validate per source part |
| ASSUMPTION-152 | 5.1a §5.5.1 | A point covers design, build, all DoD testing, scans, accessibility, docs and evidence; excludes business UAT and the 0.5 growth/compliance lead | Open — validate per source part |
| ASSUMPTION-153 | 5.1a §5.7.2 | All concrete AC data are synthetic seed fixtures (example.com, .test, reserved phone ranges) | Open — validate per source part |
| ASSUMPTION-154 | 5.1b US-0101 Identity compatibility spike (12 | Django-native auth fallback, if needed after the spike, is a change request outside EP-01 | Open — validate per source part |
| ASSUMPTION-155 | 5.1a §5.7.2 | Default parameter values in AC (quiet hours, caps, upload size 25 MB, eval tolerance 2 pp, contact verification 180 days, OTP 10 min) are configurable policy values | Open — validate per source part |
| ASSUMPTION-156 | 5.1b US-0303 Policy Decision Point skeleton | PDP latency budget p95 ≤ 100 ms | Open — validate per source part |
| ASSUMPTION-157 | 5.1a §5.5.2 | Sprint 0 and Sprint 1 at ≈ 70% of planning velocity | Open — validate per source part |
| ASSUMPTION-158 | 5.1a §5.3.1 | Coverage thresholds 80/70 (general), 90/85 (PDP, RLS, finance, AI guards), 70 (frontend) | Open — validate per source part |
| ASSUMPTION-159 | 5.1a §5.5.1 | Estimates exclude provider procurement/verification lead times | Open — validate per source part |
| ASSUMPTION-160 | 5.2 §5.2.1 | Epic central person-days = Σ mid story points × 0.7; range = Σ low × 0.5 to Σ high × 1.0, consistent with the Part 5.1 estimation basis | Align with Part 5.1 at assembly |
| ASSUMPTION-161 | 5.2 US-0805 Webhook ingestion framework (sha | Webhook dedup window = 30 days per (provider, provider account, event ID) | Confirm with provider retry windows (verify) |
| ASSUMPTION-162 | 5.2 US-0812 Uncertain-outcome reconciliation | Uncertain-outcome reconciliation schedule: +5 min, +30 min, +2 h, +12 h, human task at 24 h | Part 4 SRE runbook |
| ASSUMPTION-163 | 5.2 US-0807 Unified inbound processing: norm | Inbound intent taxonomy (10 intents), STOP keyword list as Tier 0 rules, confidence threshold 0.70 for auto-routing | Legal (keywords) and AI lead (threshold) |
| ASSUMPTION-164 | 5.2 US-0903 Public and portal meeting bookin | Public abuse thresholds: chat 20 msgs/session/10 min, 60/IP/hour, 1,000 chars; booking 30 holds/IP/10 min | Part 4 NFR-022 thresholds |
| ASSUMPTION-165 | 5.2 US-0902 Slot offer and booking with hold | Offered meeting slots expire after 72 h without selection | Product Owner |
| ASSUMPTION-166 | 5.2 US-1408 Purchase and sales order desk wi | Sell-order reservation released if the order is not acknowledged within 14 days of approval/issue (DEC-045 "expiry" undefined) | Cited by DEC-070 |
| ASSUMPTION-167 | 5.2 US-1104 Spike: social platform API acces | Social publishing candidates: official organisation-page APIs (LinkedIn, Meta, X) and self-hosted Postiz; decision via spike | Spike output ADR |
| ASSUMPTION-168 | 5.2 US-1206 Ads provider adapter (sandbox an | Meta and Google Ads provide sandbox/test accounts usable for contract tests | Verify at implementation (as of 27 Nov 2026) |
| ASSUMPTION-169 | 5.2 US-1303 Decimal pricing library with exh | GST test fixtures use an illustrative 18% (9% + 9%) rate for SAC 998314 | Finance advisor to verify rates |
| ASSUMPTION-170 | 5.3 front matter | The Admin Copilot (DEC-035) is delivered in W3, because it needs approved knowledge (W0), the gateway (W0) and CRM projections (W2); DEC-035 names no wave | Product Owner confirms at W2 planning |
| ASSUMPTION-171 | 5.3 US-1501 Payment adapter interface, signe | Until the payment gateway is selected, the adapter's generic webhook check is HMAC-SHA256 over the raw body with a per-account secret reference; replaced by the provider's documented scheme (verify at procurement, as of 27 Nov 2026) | Principal Engineer; procurement (DEC-022) |
| ASSUMPTION-172 | 5.3 US-1506 Customer portal invoice and paym | Verified payment instructions shown in the portal expire after 7 days by default, configurable by Finance | Finance (P08) |
| ASSUMPTION-173 | 5.3 US-1602 Onboarding assignment, SLA remin | Default onboarding task SLA is 3 business days in the owner's timezone where the template sets none | Startup Heads via CFG-19 |
| ASSUMPTION-174 | 5.3 US-2104 System health, SLO dashboards an | SLO alerting uses multi-window burn rates (2% of the monthly error budget in 1 h; 5% in 6 h) until Part 4 sets final thresholds | SRE Lead (Part 4) |
| ASSUMPTION-175 | 5.3 US-2107 Synthetic end-to-end journey sui | The synthetic E2E suite comprises 12 journeys (J1–J12) covering the four vertical routes, outreach opt-out, WhatsApp, payments (AP-04), automation (AP-06), SaaS lifecycle, portal and the two-tenant boundary (AP-10) | QA Lead (Part 6) |
| ASSUMPTION-176 | 5.3 US-2108 Backup restore drill | Restore drills run before every wave exit and at least monthly during the pilot | SRE Lead |
| ASSUMPTION-177 | 5.3 US-2002 Client registration with adminis | SaaS administrator verification = business-email domain match + email OTP + one authority document reviewed by the platform; GSTIN/CIN format checks (verify formats at implementation) | Service Owner; Legal |
| ASSUMPTION-178 | 5.3 US-2005 Plans, entitlements, metering an | Usage reconciliation runs at billing-cycle close with a T+1 day window for late provider events; invoices are drafted only after reconciliation | Service Owner (P12) |
| ASSUMPTION-179 | 5.3 US-1708 Scoped global search (Ctrl/Cmd+K | Global search needs ≥ 2 characters and shows ≤ 10 results per group in the palette, with "see all" to the list screen | UX Lead |
| ASSUMPTION-180 | 6.1 front matter | The FRD's SM-UT-001…066 IDs (63 used) represent control families whose meaning can be inferred from which SM-FR rows cite them; the inferred labels in §6.1.12.5 are informative only, while alias coverage is computed mechanically from each alias's FR set | Cited by DEC-204 |
| ASSUMPTION-181 | 6.1 §6.1.3.1 | Performance workload derivation factors (peak-day factor 2, peak-hour share 15–20%, 6 page views per session, 3 origin requests per uncached view, Admin concurrency 40% at one request per 10 s, safety factors 5–10×, 2 webhook events per message) and … | Open — validate per source part |
| ASSUMPTION-182 | 6.1 §6.1.7.1 | RECOMMENDATION-017's "two tenants, 26 startups" is realized as T1 with 25 owned workspaces (4 seed + 21 synthetic) + T2 with 1 workspace; a third tenant T3 is an extension pack for BR-TENANT's "2 independent external tenants"; the 26th owned startup is … | Open — validate per source part |
| ASSUMPTION-183 | 6.1 §6.1.5.2 | Provider sandboxes and test facilities exist with the capabilities listed in §6.1.6.3 (SES sandbox and mailbox simulator, WhatsApp test number, payment gateway test modes with signed webhooks, e-sign sandbox, calendar test accounts) | Open — validate per source part |
| ASSUMPTION-184 | 6.1 §6.1.11 | Test-oracle interpretations where the baseline is silent: quiet-hours window is half-open [09:00, 19:00); discount stored to 2 decimal places of a percent and "margin below floor" means strictly less than the floor; opportunity score rounding is half-up (not … | Open — validate per source part |
| ASSUMPTION-185 | 6.2a front matter | Test-oracle interpretations O-1…O-11 for EP-08…EP-11 where the baseline leaves a boundary, window, precedence or approver open (rolling windows half-open, SES daily reset, STOP matching, confidence inclusivity, stricter loosening approver, DST Sunday case, … | Product Owner and Compliance Lead confirm in Sprint 0; a different … |
| ASSUMPTION-186 | 6.2a §6.2.7.1 | Test-oracle interpretations O-12…O-21 for EP-12…EP-14 (MFA freshness boundary, business-day definition, validity end of day, inclusive commission and concession limits, anomaly strictly above 150%, duplicate-referral window, renewal notice date, reservation … | Product Owner, Finance lead, Legal |
| ASSUMPTION-187 | 6.2a §6.2.1.4 | Part 5.2 Gherkin object keys (users, opportunities, messages, threads, campaigns, quotes, contracts, bids, orders) are added to GSE-SYN as the versioned edge pack EDGE-P52 with stable keys; values not stated in Part 5.2 are fixture choices | QA automation; GSE-SYN v1.4.0 manifest review (§6.1.7.3 rule 5) |
| ASSUMPTION-188 | 6.3a front matter | Test-oracle interpretations where Part 5.3 is silent: (a) internal task/approval SLAs use Monday–Friday business days minus configured India public holidays, and "1 business day" elapses at the same clock time on the next business day (from AC-1602-01); … | Open — validate per source part |
| ASSUMPTION-189 | 6.3a §6.3.1.1 | Fixture mapping and additions: Part 5.3 fixtures FX-TEN-2, FX-USR, FX-FIN, FX-ORD, FX-BID and FX-ROUTE are realized as stable GSE-SYN keys (§6.3.1.3), including users U-AN-GM, U-EV-ONLY, U-OC1, U-RA1, U-MS1, second-buyer invoice INV-OS-2027-0051, gateway … | Open — validate per source part |
| ASSUMPTION-190 | 6.3a §6.3.2.16 | Thresholds not set by Part 7 or the baseline: AG-015 citation precision ≥ 95% and rubric accuracy ≥ 85% with human–judge agreement ≥ 0.8; per-stratum (vertical or language) accuracy gap ≤ 10 percentage points for AG-015 and AG-026; AG-024 amount exact-match … | Open — validate per source part |
| ASSUMPTION-191 | 6.4 front matter | Regression comparison method. Non-inferiority margins (2 pp for precision, recall, accuracy and groundedness; 0.02 macro-F1; +10% cost per task; +20% p95 latency), a noise band from 3 baseline runs for generative agents, paired comparison on the same frozen … | Open — validate per source part |
| ASSUMPTION-192 | 6.4 §6.4.2.1 | Dataset sizes and derived targets where Part 7 is silent: v1 sizes in §6.4.2; latency p95 ≤ 30 s (AG-004 synchronous), ≤ 10 s (AG-014), ≤ 90 s (AG-019); cost ≤ ₹0.03 per page (AG-008); secondary metrics (duplicate-claim recall ≥ 90%, judge order-flip ≤ 10% … | Open — validate per source part |
| ASSUMPTION-193 | 6.4 §6.4.1.5 | Monitoring and control interpretations. PSI > 0.2 drift, refusal-rate 2× / 0.5×, injection 3× baseline, latency breach sustained 15 minutes, rubber-stamping > 20%; DEC-001 gates apply continuously (rolling reviewer precision below gate blocks L2 until a … | Open — validate per source part |
| ASSUMPTION-194 | 6.5 front matter | Part 5.1 fixture names map to GSE-SYN stable keys as in §6.5.1.4; in particular Part 5.1's "External-A / Acme Foods" is the GSE-SYN two-tenant fixture T2, the same fixture that Part 6.1 calls "Client B" and Batch 6.3 calls "Client Alpha" | Open — validate per source part |
| ASSUMPTION-195 | 6.5 §6.5.1.5 | The 40 risk-based dimension rows of Part 5.1a §5.6.5 are numbered DM-R01…DM-R40 in table order as in §6.5.1.5 | Open — validate per source part |
| ASSUMPTION-196 | 6.5 §6.5.1.1 | Test-oracle interpretations for thresholds Part 5.1 leaves open (MFA 12 h, grant expiry instant, flag precedence, retention purge date, freshness and verification expiry, eval tolerance equality, OTP 10 min, age at IST midnight), listed in §6.5.1.6 | Open — validate per source part |
| ASSUMPTION-197 | 8.1 front matter | Project start Monday 7 Dec 2026 = Day 1; Day 180 = Fri 4 Jun 2027; two-week sprints | Open — validate per source part |
| ASSUMPTION-198 | 8.1 §8.1.1.3 | Holiday and leave allowance per §8.1.1.3 (124 working days in Day 1–180); 2027 dates of Holi, Good Friday and Ambedkar Jayanti to verify | Open — validate per source part |
| ASSUMPTION-199 | 8.1 §8.1.4.2 | Planning velocity 43 SP per 10-day sprint at 4.0 FTE, scaled linearly by FTE and working days; ramp 0.7 in S0–S1 | Open — validate per source part |
| ASSUMPTION-200 | 8.1 §8.1.4.2 | QA uplift adds delivery capacity proportional to FTE (≈ 5.4 SP per full sprint) | Open — validate per source part |
| ASSUMPTION-201 | 8.1 §8.1.6.1 | Rate per pd = ₹1.0–1.5 L ÷ 22 working days = ₹4,545–6,818 | Open — validate per source part |
| ASSUMPTION-202 | 8.1 §8.1.5.2 | Contract roles cost 20% more per FTE-month (₹1.2–1.8 L) | Open — validate per source part |
| ASSUMPTION-203 | 8.1 §8.1.5.1 | The FS engineer holds the Principal Engineer and AI lead roles; the Founder/CTO stays accountable | Open — validate per source part |
| ASSUMPTION-204 | 8.1 §8.1.5.1 | An independent reviewer is available per gate (≈ 10 days in total): a startup head not involved in the scope or an external QA reviewer | Open — validate per source part |
| ASSUMPTION-205 | 8.1 §8.1.5.1 | Founder/CTO spends ≈ 0.6 of their time as PO and architect; this time is not charged to C03 | Open — validate per source part |
| ASSUMPTION-206 | 8.2 §8.2.5 | Hypercare is staffed by the existing team inside sprint capacity (S8–S12) and the W6 budget for Release 2 | Open — validate per source part |
| ASSUMPTION-207 | 8.1 §8.1.7.3 | External dependency lead times are typical ranges; each is verified when the request is made | Open — validate per source part |
| ASSUMPTION-208 | 8.2 §8.2.2.2 | Training is delivered in-house (QA, growth/compliance lead, PO) with help articles and recorded sessions; no learning-management system is bought | Open — validate per source part |
| ASSUMPTION-209 | 8.1 §8.1.2.2 | The 30-day monitored pilot (BRD §8 W5 exit) may start on Release 1 scope after its go/no-go and extend to the closure scope when that is activated; the W5 exit needs 30 days on each scope | Open — validate per source part |
| ASSUMPTION-215 | 6.6 front matter | Part 4.2 NFR load profiles with no Part 6.1 equivalent run as named variants of Part 6.1 runs, not as new LT IDs: LT-01-AIGW (AI gateway, 4.2-LT-09), LT-01-SKEW (noisy neighbour, 4.2-LT-11), LT-08-Y2 (Year 2 profile, 4.2-LT-10), LT-12-ADM (Admin front-end … | Open — validate per source part |
| ASSUMPTION-216 | 6.7 §6.7.4.2 | A filter fixture pack EDGE-FLT (FLT-FIX-A/M/E/O) is added to GSE-SYN with the exact rows of §6.7.4; the per-vertical filter labels are fixture values (configurable per tenant), and role-specific filter fields (e.g. margin_pct for R02 only) follow the … | Open — validate per source part |
| ASSUMPTION-217 | 6.6 §6.6.3.1 | A verification item (inspection, review, analysis, demonstration) with owner, independent reviewer, evidence and wave counts as coverage for statements that are not software behaviour; the RTM reports it separately from test-case coverage | Open — validate per source part |
| ASSUMPTION-218 | 6.7 §6.7.2.6 | NFR targets defined over a production period (availability, field Core Web Vitals, DORA, monthly FinOps, DSR completion, timeliness SLIs) are verified in two steps: a TC-NFR proves the measurement and control in staging/test; a VER records attainment from … | Open — validate per source part |
| ASSUMPTION-300 | 2.6 front matter | RamVan and Smart Biochar are OrganicSpec offerings that stay in state Planned until readiness approval; they are Approved and Available only inside synthetic UAT fixtures | Open — validate per source part |
| ASSUMPTION-301 | 2.6 Document 11 Global Market Intelligence & | Benchmark uses up to 50 permitted records per source family; where fewer exist, the full permitted population is used | Open — validate per source part |
| ASSUMPTION-302 | 2.6 Document 14 Global Customer, Partner & A | Weekly acquisition review lasts 45–60 minutes per startup or cluster, on Monday 09:00 local time | Open — validate per source part |
| ASSUMPTION-303 | 2.6 §2.6.5.1.4 | Productivity study uses 5 representative users per persona group (or all users if fewer) | Open — validate per source part |
| ASSUMPTION-304 | 2.6 Document 12 Digital Marketing & Customer | Deliverability thresholds: pause at hard bounce ≥ 2% or complaint ≥ 0.1% (rolling 7 days); stop at ≥ 5% or ≥ 0.3%; verify provider thresholds at time of implementation (as of 27 Nov 2026) | Open — validate per source part |
| ASSUMPTION-305 | 2.6 Document 13 Sales Intelligence & Commerc | "C03" in SP-11/SP-13 cost lines means the shared engineering-effort line (Part 8.1), not a monthly run budget | Open — validate per source part |
| ASSUMPTION-306 | 2.6 Document 14 Global Customer, Partner & A | Legal disclosure block fields: legal name, CIN or equivalent registration ID, GSTIN where applicable, registered address, contact email/phone, grievance/privacy officer contact, links to privacy and terms; confirm per jurisdiction with counsel | Open — validate per source part |
| ASSUMPTION-307 | 2.6 P17 Agency / Managed-Service Operator (n | Delegation grants default to 90 days and are renewable by the client | Open — validate per source part |
| ASSUMPTION-308 | 2.6 §2.6.5.1.4 | Training records expire after 12 months | Open — validate per source part |
| ASSUMPTION-309 | 2.6 §2.6.5.9.1 | AG-013 confidence below 0.60 maps to class "unknown" (configurable) | Open — validate per source part |
| ASSUMPTION-320 | 3.4 front matter | Growth-column staff sessions are all active at r = 20 requests/min (ASSUMPTION-102 rate applied to every concurrent session) | Open — validate per source part |
| ASSUMPTION-321 | 3.4 §3.4.8 | Opportunity storage ≈ 2.6 KB per row including indexes and evidence links | Open — validate per source part |
| ASSUMPTION-322 | 3.4 §B | RC-1 PITR restore of a growth-size database completes within 75 minutes; to be measured in the quarterly drill (verify RDS restore throughput) | Open — validate per source part |
| ASSUMPTION-323 | 3.4 §3.4.8 | Discipline-to-role mapping (React/UX → FE + UX; Django + PostgreSQL → BE + FS remainder; AI → FS; QA → QA; DevOps → DevOps) and focus factor 0.686 derived from Part 8 capacity (398 pd ÷ 580 FTE-days) | Open — validate per source part |
| ASSUMPTION-324 | 3.4 §C | "Redis" in the source pack means the Redis protocol, satisfied by Valkey | Open — validate per source part |
| ASSUMPTION-325 | 3.4 §3.4.4.1 | Pack predecessors H02/H03 of BR-M01 are pre-existing identity hardening items of the reused service; treated as inputs to the identity spike US-0101 (not defined anywhere in the 38 documents) | Open — validate per source part |
| ASSUMPTION-340 | 2.7a front matter | Doc 06 "Admin role / location" (Admin, Workspace, Existing) is a permission/workspace class, not a navigation home; Part 2.5 navigation stands | Open — validate per source part |
| ASSUMPTION-341 | 2.7a §2.7.7 | Field type, control and validation in Batch 2.7b are inferred by rule set R-FLD from field names; the Part 3.3 data dictionary prevails on conflict | Open — validate per source part |
| ASSUMPTION-342 | 2.7a §2.7.1.2 | Doc 06 and doc 17 field decisions are identical to FRD §16.2 (parser diff = 0), so Part 2.1 traces apply to all three documents | Open — validate per source part |
| ASSUMPTION-343 | 2.7a §2.7.3.1 | Filter-family applicability per screen follows the screen's Command Centre view; vertical families appear only when enabled by the capability profile | Open — validate per source part |
| ASSUMPTION-344 | 2.7a §2.7.4.1 | "Existing NNN" is the original 116-item numbering: A001–A106 hold 106 numbers and the ten retained website capabilities hold the other ten | Open — validate per source part |
| ASSUMPTION-345 | 2.7a §2.7.8 | Doc 06 SM-FR/SM-UT/SM-UAT associations are those of FRD §11 (counts identical), so Part 6.1 §6.1.12.5 alias mapping holds without change | Open — validate per source part |
| ASSUMPTION-360 | 3.5a front matter | Document 07 numbers operations without a prefix; the blueprint cites them as SM-OP-### (sequence number) with the source's own SIT ID SM-SIT-A### | Open — validate per source part |
| ASSUMPTION-361 | 3.5a §3.5.3.1 | "Existing authentication" in a greenfield deployment means the BFF/OIDC identity reuse of DEC-019; legacy /auth/* and /me paths are logical aliases | Open — validate per source part |
| ASSUMPTION-362 | 3.5a §3.5.3.1 | Candidate notation tokens map to the OpenAPI types in §3.5.5.1 | Open — validate per source part |
| ASSUMPTION-363 | 3.5a §3.5.3.1 | Default bounds for strings, arrays, lines and slots where the source gives none; to confirm in contract review | Open — validate per source part |
| ASSUMPTION-364 | 3.5b §3.5.8 | Source run state pending has the same meaning as queued | Open — validate per source part |
| ASSUMPTION-365 | 3.5b §3.5.5.1 | Enum values in source DTOs are initial vocabularies; map types become named, versioned JSON Schemas; clients tolerate unknown enum values (Part 3.2 §3.2.1.3) | Open — validate per source part |
| ASSUMPTION-366 | 3.5a §3.5.3.1 | Source physical table names (growth_*, sales_*, sales_ui_*) correspond to Part 3.3 logical entities; no physical table is asserted here (document 08 group owns entities); ContractEvidence proposed as a logical entity only | Open — validate per source part |
| ASSUMPTION-396 | 3.6a §3.6.4.2 | Doc 08 is the original catalogue referred to by GAP-112/DEC-087; GAP-112 can be closed | Open — validate per source part |
| ASSUMPTION-397 | 3.6a §3.6.3 | Doc 08 provider licence/quota/price lines are reconciled by the document 16 group; prices quoted there (checked 24 Nov 2026) are not restated and must be verified at implementation (as of 27 Nov 2026) | Open — validate per source part |
| ASSUMPTION-400 | 7.4a front matter | The 100 use-case names, 20 industry templates and 13 node types are proposed by Group F because the pack gives only counts and group names | Open — validate per source part |
| ASSUMPTION-401 | 7.4a §7.4.3 | Source priority codes read as P0–P3 adoption priority, R retained alternative, X excluded/not selected, V verification-only inventory | Open — validate per source part |
| ASSUMPTION-402 | 7.4a §7.4.4.2 | Document 16/21 free tiers and rates are historical planning inputs (source checks dated 24 Nov 2026 where stated); verify at implementation, as of 27 Nov 2026 | Open — validate per source part |
| ASSUMPTION-403 | 7.4b §7.4.5.8.7 | Benchmark trial spend for a paid candidate fits in B10 with a one-time cap of ₹3,000 per candidate | Open — validate per source part |
| ASSUMPTION-404 | 7.4b §7.4.8 | Staff-typed meeting notes are a lawful AG-037 input under existing notices; recordings/transcripts stay excluded until GAP-143 is resolved | Open — validate per source part |
| ASSUMPTION-405 | 7.4b §7.4.5.9 | Initial contribution-margin allocation: infrastructure by AI-task and storage share, support by ticket count | Open — validate per source part |
| ASSUMPTION-420 | 6.8a front matter | SM-SIT-M### numbers follow document 22's table order; 50 of 66 differ from BR-M## (BRD module numbers); mapping is by module name | Open — validate per source part |
| ASSUMPTION-421 | 6.8c §6.8.8 | A source test is "Equivalent" only when a blueprint TC asserts the same condition and the same observable outcome; otherwise Partial with an ENH case | Open — validate per source part |
| ASSUMPTION-422 | 6.8b §6.8.4.1 | "Nearest" operation matches (same method and namespace, last segment contained, token Jaccard ≥ 0.5) are provisional | Open — validate per source part |
| ASSUMPTION-423 | 6.8c §6.8.8 | All 799 source cases keep status Not run; no source result is imported as evidence | Open — validate per source part |
| ASSUMPTION-424 | 6.8a §6.8.3.2 | Source fixtures map to GSE-SYN keys as in §6.8.5.1.2; new keys BUD-10U, FIN-1000-600-400 | Open — validate per source part |
| ASSUMPTION-440 | 6.9b front matter | The 172 expansion decisions = 147 per-screen field decisions + 19 candidate operations + 6 candidate entities | Open — validate per source part |
| ASSUMPTION-441 | 6.9a §6.9.4.2 | The 5 "added" BRs of doc 38 are the five BRD §17.1 scope statements (XBR-01…05 → BR-S138) | Open — validate per source part |
| ASSUMPTION-442 | 6.9b §6.9.5.1.2 | Source QC owners translate to blueprint roles (product manager → PO; business owner → R02; finance lead → R08/R09; operations lead → DevOps/SRE) | Open — validate per source part |
| ASSUMPTION-443 | 6.9b §6.9.5.1.4 | Evidence path evidence/qc/QC-###.json → S3 key evr/qc/ / .json under Object Lock | Open — validate per source part |
| ASSUMPTION-444 | 6.9b §6.9.5.3.1 | SM-SIT alias granularity is the FR; operation-level mapping in Part 6.8 | Open — validate per source part |
| ASSUMPTION-445 | 6.9b §6.9.8 | Source PD equals blueprint person-day; SP → pd at 0.7 | Open — validate per source part |
| ASSUMPTION-446 | 6.9b §6.9.5.2.3 | SPDEC records are handled inside A090 and A112 (no new screen); queue SLAs as in §6.9.5.2.3 | Open — validate per source part |
| ASSUMPTION-460 | 4.4b §4.4.8.1 | Doc 31 alert thresholds (AL-50…58) are initial values, tuned after W3 telemetry | DevOps, W3 review |
| ASSUMPTION-461 | 4.4b §4.4.5.4.1 | Staging can be scaled to Topology B instance classes for WP-02 runs only; cost per run is small relative to B01 (verify prices) | DevOps + FinOps |
| ASSUMPTION-462 | 4.4b §4.4.8.1 | Diff coverage is measured with a standard diff-coverage tool on Cobertura/LCOV output (verify tool choice) | DevOps, W0 |
| ASSUMPTION-463 | 4.4a §4.4.5.1.21 | A first-review SLA of 1 business day is achievable with 4.0 FTE (CS-REV-04) | Principal engineer; review at W2 |
| ASSUMPTION-464 | 4.4b §4.4.8.1 | IAM Identity Center (or equivalent) supports just-in-time, time-bound production access within budget (verify) | DevOps, W0 |
| ASSUMPTION-480 | 8.3b §8.3.5.8 | 8.3b §8.3.5.8 | Open — validate per source part |
| ASSUMPTION-481 | 8.3b §8.3.5.2 | 8.3b §8.3.5.2, §8.3.5.11 | Open — validate per source part |
| ASSUMPTION-482 | 8.3c §8.3.5.13.1 | 8.3c §8.3.5.13.1, §8.3.5.13.6 | Open — validate per source part |
| ASSUMPTION-483 | 8.3c §8.3.5.13.7 | 8.3c §8.3.5.13.7 | Open — validate per source part |
| ASSUMPTION-484 | 8.3c §8.3.5.15.2 | 8.3c §8.3.5.15.2 | Open — validate per source part |
| ASSUMPTION-485 | 8.3c §8.3.5.15.9 | 8.3c FR-ENH-J-019 | Open — validate per source part |
| ASSUMPTION-486 | 8.3c §8.3.5.14.2 | 8.3c §8.3.5.14.2 | Open — validate per source part |
| ASSUMPTION-487 | 8.3c §8.3.5.14.4 | 8.3c §8.3.5.14.4 | Open — validate per source part |
| ASSUMPTION-488 | 8.3c §8.3.5.14.2 | 8.3c §8.3.5.14.2 | Open — validate per source part |
| ASSUMPTION-489 | 8.3b §8.3.5.1 | 8.3b §8.3.5.1 | Open — validate per source part |
| ASSUMPTION-490 | 8.3c §8.3.5.13.4 | 8.3c CSO-09 | Open — validate per source part |
| ASSUMPTION-500 | 9.5 §9.5.2.1 | Groups C, E and G gave no estimate and Group H gave story points only for its stories; their packages are sized here by analogy to Part 5 stories (2–8 SP each, 0.7 pd per SP) | Open — validate per source part |
| ASSUMPTION-501 | 9.5 §9.5.2.1 | Group F's 68–110 pd used 1 pd per SP; normalised to Part 8.1's 0.7 pd per SP (47.6–77.0 pd) | Open — validate per source part |
| ASSUMPTION-502 | 9.5 §9.5.2.2 | 20% / 15% / 10% (low / central / high) of net enhancement effort is absorbed into existing baseline stories at refinement | Open — validate per source part |
| ASSUMPTION-503 | 9.5 §9.5.2.5 | An added engineer delivers 7.53 pd per sprint less 15% onboarding/coordination (6.4 pd) and can start Sprint 3 (Day 43) if contracted by about Day 15 | Open — validate per source part |
| ASSUMPTION-504 | 9.5 §9.5.2.5 | Added engineers cost ₹1.0–1.5 L per month each (as instructed; no contract premium); months = days ÷ 30.4 | Open — validate per source part |
| ASSUMPTION-505 | 9.5 §9.5.3 | New run-cost items (probes, restore-instance hours, reserved worker, drift job, training tenant, CI minutes) are estimates; verify AWS and tool prices at time of implementation (as of 27 Nov 2026) | Open — validate per source part |
| ASSUMPTION-506 | 9.5 §9.5.1.10.1 | The five "added" BRs of document 38 are the expansion scope statements XBR-01…05 (BR-S138), because document 24 enumerates 71 BRs that already include the five B-* cross-cutting requirements | Cited by DEC-180, DEC-233 |
| ASSUMPTION-507 | 9.5 §9.5.2.6 | The core team is employed through Day 365 under every option (DEC-005), so a schedule slip consumes W6 capacity rather than adding salary in the Day 1–365 view | Open — validate per source part |
| ASSUMPTION-508 | 9.5 §9.5.2.5 | Gates are set at weekly granularity on Fridays; activation dates shift by about one third (early), two thirds (middle) and all (late Release 1) of the Release 1 slip; sprint boundaries are realigned at the S3 review | Open — validate per source part |
| ASSUMPTION-509 | 9.5 §9.5.2.6 | Penetration-test scope uplift costs ₹0.5–1.0 L per engagement (verify quotes, as of 27 Nov 2026) | Open — validate per source part |
| ASSUMPTION-510 | 6.6 front matter | A source-pack story counts as covered by the tests of the FR-ENH it realizes, and an FR-ENH whose requirement text names control IDs (RGV-, SMK-, AL-, ACC-, SEC-ROT, RBK-) counts as covered by the tests citing those control IDs. Both are reported separately … | Open — validate per source part |
| ASSUMPTION-511 | 6.6 §6.6.1.1 | A QC counts as covered by the tests and VER of the requirements and controls named in its blueprint_verification_refs (H_qc_map.csv), in addition to tests citing the QC directly | Open — validate per source part |
| ASSUMPTION-512 | 6.6 §6.6.1.1 | The RTM columns api_ids and sit_aliases required by DEC-217 are derived from the coverage CSVs: an FR or story carries the SIT aliases of H_sit_alias_map.csv that list it and the API operations of those aliases (D_api_mapping.csv); a TC-ENH carries the … | Open — validate per source part |
| ASSUMPTION-513 | 6.10 §6.10.8 | VER-ENH-K items count as coverage for process QCs (acceptance, sign-off, training, runbooks), as VER-### do for BR-S in Part 6.7 (ASSUMPTION-217) | Open — validate per source part |
| ASSUMPTION-514 | 6.10 §6.10.8 | The pack's SIT, UAT and Unit tests are covered when their mapped blueprint test is defined; execution evidence follows RECOMMENDATION-080 | Open — validate per source part |
| ASSUMPTION-520 | 9.6a §9.6a | A warm-standby or restore-to-ap-south-2 path can meet RC-1 RTO ≤ 2 h for a regional outage in the growth phase; its cost is priced at the growth trigger | First regional drill |
| ASSUMPTION-521 | 9.6a §9.6a | The smallest ElastiCache (Valkey) node is sufficient for pilot broker and cache load | Cited by DEC-243 |
| ASSUMPTION-522 | 9.6a §9.6a | HyperLogLog distinct counting is available on the chosen RDS PostgreSQL version; otherwise exact distinct-key side tables are used | Sprint 1 spike |
| ASSUMPTION-523 | 9.6a §9.6a | The 164 / 164 / 165 offline examples correspond to the 165 explicit proposed contracts of doc 07 §8015 | Cited by DEC-264 |
| ASSUMPTION-550 | 9.6b §9.6b | DEC-328 | Cited by DEC-328 |
| ASSUMPTION-551 | 9.6b §9.6b | §9.6b.7 | Open: verify AWS ap-south-1 prices and model fit in W1 |
| ASSUMPTION-552 | 9.6b §9.6b | DEC-308 | Open: verify at W0 |
| ASSUMPTION-553 | 9.6b §9.6b | DEC-322 | Cited by DEC-322 |
| ASSUMPTION-554 | 9.6b §9.6b | §9.6b.1.3, DEC-310, DEC-315 | Cited by DEC-310 |
| ASSUMPTION-555 | 9.6b §9.6b | DEC-327 | Cited by DEC-327 |
| ASSUMPTION-556 | 9.6b §9.6b | §9.6b.7.1 | Applied |
| ASSUMPTION-600 | 9.7a front matter | Outcome fields needed for ML features (stage history, intent labels, reply timestamps, renewal outcomes) are already retained under DEC-028 | Cited by DEC-028 |
| ASSUMPTION-601 | 9.7a §9.7.2.2 | Account briefs reduce tokens on account-centric agents by ≈ 20% and pursuit preparation by ≈ 1.5 h per qualified account | Measure with AU-065 holdout in A1 |
| ASSUMPTION-602 | 9.7a §9.7.2.2 | RFP co-pilot reduces drafting time by 25–40% once ≥ 50 approved answers exist | Measure on ≥ 5 bids at G-A1 |
| ASSUMPTION-603 | 9.4 §9.4.3 | Additional locales bn, te, mr, kn, ml, gu are wanted by some startups; enabled per startup only | Confirm per startup before A2 |
| ASSUMPTION-604 | 9.4 §9.4.4 | AU-068 finds 10–20% savings at equal quality | Track quarterly |
| ASSUMPTION-605 | 9.7a §9.7.3.1 | A2 and A3 calendar dates follow W6 continuously in Year 2 | Confirm at G-A1 |
| ASSUMPTION-606 | 9.7a §9.7.3.4 | At least 10 past AppNAI bids are available to seed the answer library | Inventory before A1 |
| ASSUMPTION-607 | 9.7a §9.7.5 | Pilot call volumes per agent (§9.7.5 cards) derive from BR-S089 volumes and DEC-031 users | Replace with measured volumes after 4 weeks of each agent |
| ASSUMPTION-608 | 9.7b §9.7.17 | Langfuse self-hosted cost equals the B22 estimate of Part 8.4 (₹2,250–2,700/month) | Verify at deployment |
| ASSUMPTION-609 | 9.7b §9.7.13.1 | Contract AI pod rates fall within the BRD loaded rate band ₹1.0–1.5 lakh per person-month | Quotes before G-X0 |
| ASSUMPTION-650 | 9.8a §9.8.3.5 | X2 needs an incremental squad of 4.0 FTE (2 full-stack, 1 frontend, 0.5 QA, 0.5 RevOps analyst) for Day 237–425 | Confirm at DEC-390 approval; Product Owner |
| ASSUMPTION-653 | 9.8a §9.8.4.2 | Default tier-1 cap of 15 accounts per owner | Tune after A1 baseline; Startup heads |
| ASSUMPTION-654 | 9.8a §9.8.4.2 | Speed-to-lead SLAs of 1 business hour (hot) and 4 business hours (standard) | Tune after baseline; Sales leads |
| ASSUMPTION-656 | 9.8a ADV-X2-F07 Territory planning | Territory view in A2 uses tables and region lists, no map service | Revisit at A3 |
| ASSUMPTION-662 | 9.8b §9.8.13.1 | Development cash allocated to releases pro-rata by central effort; rates from BRD §6 | FinOps to re-baseline at approval |
| ASSUMPTION-663 | 9.8b §9.8.11 | Proposed KPI targets and message volumes (sends, WhatsApp) are planning values pending baselines | Confirm after A1 baseline period |
| ASSUMPTION-666 | 9.8b §9.8.5 | Agent call volumes, token sizes and escalation shares in §9.8.5; low = 0.3 × base, high = 3 × base | Measure in A1; FinOps |
| ASSUMPTION-700 | 9.9b §9.9.12 | X3 team = 2 extended contract engineers + 1 contract data engineer + 1 contract SRE/security engineer + QA 0.5 + UX 0.5 (5.0 FTE) from Day 239 | Cited by DEC-400, DEC-417 |
| ASSUMPTION-701 | 9.9a §9.9.3.1 | Release windows A1 Day 239–299, A2 Day 302–362, A3 Day 393–481 with a December freeze | Open |
| ASSUMPTION-702 | 9.9b §9.9.12 | 20% cross-cutting allowance (12% integration QA, 5% security, 3% training content) | Open |
| ASSUMPTION-703 | 9.9a §9.9.3.2 | The AppNAI IdP supports passkeys for external users and attestation for staff (DEC-019 check 5) | Open; verify in spike |
| ASSUMPTION-704 | 9.9a ADR-137 BYOK through cross-account KMS k | BYOK tenants operate AWS accounts with KMS keys in ap-south-1 | Open |
| ASSUMPTION-705 | 9.9b §9.9.6 | X3 agent volumes and token sizes in 9.9.6 (pilot) | Open; recalibrate after 1 month |
| ASSUMPTION-706 | 9.9b §9.9.13.1 | Translation volume ≈ 15,000 words per locale at ₹1.5–3.0 per word | Open; obtain quotes |
| ASSUMPTION-750 | 9.10 front matter | Overlap deduction of 30 / 45 / 65 pd (§9.10.4) | Open; validate at A1 planning |
| ASSUMPTION-751 | 9.10 §9.10.7.1 | X2 A1 development cost taken pro rata to A1 effort | Open; validate at A1 planning |
| ASSUMPTION-752 | 9.10 §9.10.10 | A1 runs at about 6 FTE beyond the core team over ≈ 90 working days | Cited by DEC-417 |

<!-- GEN:ASSUMPTION:END -->

### 9.2.4(b) GAP register

<!-- GEN:GAP:BEGIN -->

| ID | First seen | Gap (statement) | Status / handling |
|---|---|---|---|
| GAP-001 | 0 §0.3.1 | API catalogue of 302 retained + 19 candidate operations is not attached; only 105 operations are named | Closed by DEC-015 |
| GAP-002 | 0 §0.3.1 | Entity catalogue of 149 + 6 is not attached; 132 named. Core entities are unnamed: Tenant, Startup, BusinessLine, Offering/SKU, PublicationSnapshot, Domain, Bid/Tender, Order, OrderLine, FulfillmentEvent, Plan, Entitlement, ServiceInvoice, UsageMeter, … | Closed by DEC-016 |
| GAP-003 | 0 §0.3.1 | Test catalogue (624 + 175) is not attached. SM-UT-001…066, SM-UAT-S001…, SM-UX-UAT-* are referenced but not defined | Closed by DEC-017 |
| GAP-004 | 0 §0.3.3 | No explicit NFR targets: availability, latency, throughput, concurrency, RTO/RPO, volume growth, browser support | Closed by DEC-018 |
| GAP-005 | 0 §0.4 | Identity dependencies "H02, H03" undefined; the existing auth technology (session vs OIDC provider, MFA method) is unknown | Closed by DEC-019 |
| GAP-006 | 0 §0.4 | Budget IDs B01–B22 and engineering ID C03 are referenced, but the cost table rows carry no IDs; "11 Budget" section is not present | Closed by DEC-020 |
| GAP-007 | 0 §0.1.1 | Referenced artefacts not attached: MedMaarg investor/business deck (slides 2–17), integration workbook (rows 4–541, 538 candidates), HTML prototypes, "20 role perspectives" checklist, sibling investor-application spec | Closed by DEC-021 |
| GAP-008 | 0 §0.4 | Payment provider unnamed ("existing payment provider subject to API") | Closed by DEC-022 |
| GAP-009 | 0 §0.4 | E-signature provider unnamed | Closed by DEC-023 |
| GAP-010 | 0 §0.4 | Calendar provider unnamed | Closed by DEC-024 |
| GAP-011 | 0 §0.4 | Email provider undecided (Resend vs Amazon SES); budget assumes SES | Closed by DEC-025 |
| GAP-012 | 0 §0.3.3 | Supported languages and locales not listed | Closed by DEC-026 |
| GAP-013 | 0 §0.4 | Tax rules (GST, cross-border), rounding rule, FX rate source not specified | Closed by DEC-027 |
| GAP-014 | 0 §0.3.3 | Retention periods per data class not specified | Closed by DEC-028 |
| GAP-015 | 0 §0.4 | Regulations outside India not addressed although AppNAI is worldwide (GDPR/UK GDPR/PECR, CAN-SPAM, CASL, etc.) | Closed by DEC-029 |
| GAP-016 | 0 §0.4 | Mechanism for verifiable guardian consent (children) not specified | Closed by DEC-030 |
| GAP-017 | 0 §0.4 | Number of internal users, portal users and growth trajectory unknown | Closed by DEC-031 |
| GAP-018 | 0 §0.3.3 | "Agreed window" for the 99% workflow-completion target undefined | Closed by DEC-032 |
| GAP-019 | 0 §0.4 | The 9 new interfaces have SM-UX-FR rows but no SM-FR rows | Closed by DEC-033 |
| GAP-020 | 0 §0.4 | Phase gates cite M-ranges ("M01–M09", "M10–M20" …), but IDs are not sequential in the register (M53, M56, M58 sit in the foundation block; M55 in the CRM block; M41 in omnichannel) | Closed by DEC-034 |
| GAP-021 | 0 §0.4 | "Approved Copilot" is mentioned with no functional spec, screen or limits | Closed by DEC-035 |
| GAP-022 | 0 §0.4 | Internal notification channels (in-app, email, push, chat) and digest rules unspecified | Closed by DEC-036 |
| GAP-023 | 0 §0.4 | Global search across records is not specified beyond filters and knowledge search | Closed by DEC-037 |
| GAP-024 | 0 §0.4 | Approval thresholds not quantified (discount %, margin floor, amount bands needing finance/legal, autonomy limits) | Closed by DEC-038 |
| GAP-025 | 0 §0.4 | No data migration source described (existing CRM, spreadsheets, contact lists) | Closed by DEC-039 |
| GAP-026 | 0 §0.4 | Hosting region, HA tier and DR design unspecified ("validate region/HA needs") | Closed by DEC-040 |
| GAP-027 | 0 §0.4 | Monitoring stack only "CloudWatch/Sentry candidates"; no SLOs or alert thresholds | Closed by DEC-041 |
| GAP-028 | 0 §0.4 | Model names and prices quoted in the FRD (Claude Haiku 5.5 $0.10/$0.50, Sonnet 5.5 $2/$10 per MTok) are time-sensitive and unverified | Closed by DEC-042 |
| GAP-029 | 0 §0.4 | Device/channel support not stated (mobile web? native apps?) | Closed by DEC-043 |
| GAP-030 | 0 §0.4 | Support model and SLAs for SaaS clients undefined ("no unverified SLA promise") | Closed by DEC-044 |
| GAP-031 | 0 §0.4 | OrganicSpec inventory/stock reservation is referenced, but no inventory model or rules exist | Closed by DEC-045 |
| GAP-032 | 0 §0.4 | Referral commission referenced ("Commission approval") without commission rules | Closed by DEC-046 |
| GAP-033 | 0 §0.4 | SaaS plan catalogue (plans, quotas, prices for W31/A101) not provided | Closed by DEC-047 |
| GAP-034 | 0 §0.4 | Admin "Copilot" and agent permissions to call internal tools are not enumerated (tool registry) | Closed by DEC-048 |
| GAP-101 | 3.1 front matter | DEC-040 requires cross-region backup copies, but B20 (backup/DR storage) is ₹0 until approved | Request ≈ ₹200/month approval |
| GAP-102 | 3.1 §3.1.6.2 | DEC-020 does not say whether B01 covers non-production environments (staging) | FinOps/PO decision |
| GAP-103 | 2.7a §2.7.2 | The original 302-operation catalogue (BRD §9) is not available; one-to-one reconciliation impossible | Closed by DEC-170 |
| GAP-104 | 3.1 §3.1.6.2 | No WAF budget at pilot (B21 ₹0) while NFR-022 requires abuse controls on public intake | Compensating controls; revisit at W3 |
| GAP-105 | 3.2 §3.2.4.3 | Several providers lack full sandboxes (social posting, some e-sign and ads features, WhatsApp production templates) | Recorded fixtures + internal-recipient canaries |
| GAP-107 | 3.1 §3.1.6.1 | Approach and limits for 25+ startup custom domains on CloudFront (certificates, alternate names, KVS) not specified | Verify quotas in Sprint 0 |
| GAP-111 | 3.2 §3.2.4.2 | Embedding model/provider not decided in the baseline (the Claude API is not assumed to provide embeddings; verify). Interim: dimension 1024 fixed per model; provider chosen in Part 7 | Open — handling per source part |
| GAP-112 | 2.7a §2.7.3.1 | The original 149-entity catalogue was not supplied; 17 retained entities cannot be identified, so a one-to-one reconciliation is impossible | Closed by DEC-087, DEC-191 |
| GAP-113 | 3.3 §3.3.3.1 | DEC-028 does not cover delivery events, eligibility/policy decisions, meetings, business records and configuration; interim periods given; Legal to confirm | Open — handling per source part |
| GAP-114 | 3.3 §3.3.11.3 | Archive retrieval SLA not defined; interim 5 business days | Open — handling per source part |
| GAP-115 | 3.3 §3.3.16.7 | DPDP verifiable parental consent mechanism to be confirmed; the consent model keeps capture_method and evidence extensible | Open — handling per source part |
| GAP-116 | 3.3 §3.3.6.4 | "Global" suppression scope in BRL-ELG-02 is undefined; interpreted as tenant-wide (cross-tenant suppression is prohibited by DEC-065) | Open — handling per source part |
| GAP-120 | 4.1 front matter | No budget line for external penetration tests (B07 is ₹500/month; B11 contingency is shared). Estimated ₹1.5–4 lakh per engagement for this scope (estimate; verify quotes) | Founder to approve a security testing line before end W3 |
| GAP-121 | 4.1 §4.12.1 | No named Grievance Officer / DPDP contact person or CERT-In point of contact | Founder to designate before W2 public launch |
| GAP-122 | 4.3 §4.43.2 | No on-call compensation or out-of-hours coverage commitment in the baseline | Founder decision before W3 |
| GAP-123 | 4.3 §4.49.2 | Part 3 ADRs (compute platform, IaC, CI) not available while this batch was written; ADR-050…053, 058…060 may duplicate or conflict | Closed by DEC-083 |
| GAP-124 | 4.1 §4.12.10 | Cyber insurance not considered | Evaluate at W4 when payments go live |
| GAP-125 | 4.1 §4.12.5 | GDPR Art. 27 EU representative and UK representative not addressed for EU/UK outbound under DEC-029 | Counsel decision before enabling the EU/UK pack |
| GAP-126 | 4.3 §4.43.4 | No customer-facing status page or incident communication channel for SaaS tenants | Closed by DEC-406 |
| GAP-127 | 4.3 §4.49.2 | B22 (LLM observability/eval tooling) is ₹0; the eval harness must run on OSS (DeepEval candidate, M54) and CI minutes | Accept OSS-only at pilot; revisit at the growth gate |
| GAP-140 | 7.1 front matter | No measured AI usage baseline exists | Open — handling per source part |
| GAP-141 | 7.3 §7.3.1 | Anthropic commercial terms for this deployment (data retention, training exclusion, DPA, cross-border processing, ZDR eligibility) not yet confirmed | Open — handling per source part |
| GAP-142 | 6.4 §6.4.2.1 | Golden eval datasets do not exist (≥ 200 labelled per vertical for qualification, DEC-001) | Open — handling per source part |
| GAP-143 | 3.4 Document(s) 05 | No lawful meeting-recording or transcript source exists; meeting summarization is excluded until one is approved with consent | Narrowed by DEC-218 |
| GAP-144 | 6.4 §6.4.6 | Tier 2 provider terms (Groq DPA, Gemini/OpenRouter/Mistral free terms) not legally reviewed | Open — handling per source part |
| GAP-145 | 7.3 §7.5.4 | DEC-047 "AI tasks" quotas have no defined unit or cost basis | Open — handling per source part |
| GAP-150 | 5.1a front matter | Import template columns for catalogues, organizations, contacts and deals are not specified | Open — handling per source part |
| GAP-151 | 5.1b US-0306 Contact, privacy, terms and help | DPDP response deadline for privacy requests not given in the baseline (BRL-PRV-02 says verify) | Closed by DEC-100 |
| GAP-152 | 5.1c US-0506 Buying signal classification and | Signal-type and need-category taxonomies are not enumerated; AC values are illustrative | Open — handling per source part |
| GAP-153 | 5.1c US-0710 Public intake abuse controls | The bot-check mechanism for public intake is not specified; it must not be a cognitive test (WCAG 3.3.8) | Open — handling per source part |
| GAP-154 | 5.1b §5.8.4.1 | Labelled benchmark datasets (≥ 100 reviewed signals; ≥ 200 labelled items per vertical for qualification, DEC-001) have no owner or effort in the baseline | Open — handling per source part |
| GAP-155 | 5.2 US-1108 SEO and visibility dashboard fro | No authorised rank-tracking data source; B17 SEO data is ₹0 until approved. Dashboard shows Search Console average position only | Product Owner decision on B17 |
| GAP-156 | 5.2 US-0802 Channel preflight and approved-m | DEC-064 does not set an autonomy cap for first-touch outbound outreach; stories default to L1 (each first touch approved) | Closed by DEC-071 |
| GAP-157 | 5.2 §5.2.3.1 | Webinar platform and attendance-evidence source not decided (Zoom is only a candidate) | Product Owner; adapter story later if approved |
| GAP-158 | 5.2 US-1410 Acceptance and separate receivab | Amount rule for partial acceptance postings not specified; interim rule = accepted quantity × net unit price per line | Finance lead |
| GAP-159 | 5.2 US-1309 Contracts and MoUs from approved | Format of signer-authority evidence (board resolution, authorisation letter, designation) not specified | Legal |
| GAP-160 | 5.3 front matter | Treatment of tax withheld at source (TDS) on B2B receipts is not specified. Interim rule: a "tax withheld" allocation type with certificate evidence, approved by the Finance Checker | Finance advisor; Part 3 data model |
| GAP-161 | 5.3 US-1902 Immutable publication snapshots, | No target exists for CDN purge latency after publish or rollback (see RECOMMENDATION-058) | SRE Lead (Part 4) |
| GAP-162 | 5.3 US-2001 SaaS introduction, plans and dem | SaaS plan prices and overage rates are not approved (DEC-047). Pages show "Price on request" until the Service Owner approves a rate revision; billing tests use test rates | Service Owner before W5 exit |
| GAP-163 | 5.3 US-1706 Sales forecast (estimate) and fo | No default forecast stage weights exist for a startup with < 30 closed deals and no configured weights. Interim rule: show "Unknown – configure stage weights" | Startup Heads via A088 |
| GAP-164 | 5.3 US-1911 Public site accessibility, acces | The owner and legal wording of the per-startup accessibility statement are not defined. Interim: a platform template approved by R10 per startup | Legal/DPO (P09) |
| GAP-165 | 6.1 front matter | Test capacity. QA-owned test effort is estimated at 43–97 pd against ≈ 50 pd of QA capacity (0.5 FTE, DEC-005), a shortfall of up to ≈ 47 pd at the high end; business UAT participation (60–120 participant-days over W0–W5) is not in any budget or plan | Closed by DEC-095, DEC-133 |
| GAP-166 | 6.1 §6.1.3.1 | Dependent catalogues not yet available: Part 7 agent catalogue (AG IDs, per-agent thresholds, eval harness choice) and the Part 5.1 dimension matrix were not published when this batch was written | Batch 6.3 takes AG IDs and thresholds from Part 7; harness choice defaults to the … |
| GAP-167 | 2.7a §2.7.3.1 | Retained test catalogue and missing alias IDs. The BRD's "624 retained product tests + 175 candidate tests" (BRD §9, §17) were not supplied; SM-UT-037, SM-UT-049 and SM-UT-050 are absent from the FRD although the range runs to 066 | Closed by DEC-094, DEC-204 |
| GAP-168 | 6.4 front matter | Multilingual evaluation resources. No plan or budget for bilingual labellers (Hindi, Tamil, Odia, code-mixed Hinglish) or for curating ML-01…ML-05 and the multilingual red-team set RT-11; Part 7 GAP-142 sizes labelling at 6–10 person-days for golden sets only | Closed by DEC-116 |
| GAP-169 | 6.4 §6.4.11.1 | No approved crisis/self-harm response. The baseline requires handover for clinical topics but defines no approved message, helpline reference or escalation for a visitor or sender in crisis (AG-017, AG-013) | Closed by DEC-115 |
| GAP-170 | 6.5 front matter | Part 2.3 §2.25 states "162 business rules", but its family counts (TEN 12, ELG 18, SRC 10, SCR 9, AI 12, APR 11, SEQ 5, MTG 6, MKT 10, BID 6, QTE 7, CTR 5, ORD 6, FIN 8, LCY 6, PUB 6, AUT 10, PRV 7, SVC 7) sum to 161, and 161 distinct BRL IDs are defined. … | Closed by DEC-141 |
| GAP-171 | 6.5 §6.5.10.2 | Load-test IDs collide: Part 4.2 §4.26 defines LT-01…LT-12 differently from Part 6.1 §6.1.14.1 (for example LT-02 is "Soak at design load" in 4.2 but "Public website and portal" in 6.1; LT-05 is 50 webhooks/s for 10 min vs 2 min). ERRATA-30 says Part 6.1 owns … | Closed by DEC-143 |
| GAP-172 | 6.5 front matter | Gap (closed by Batch 6.7) | Open — handling per source part |
| GAP-173 | 8.1 front matter | No named business UAT participants or approved time exist (second half of GAP-165) | Open — handling per source part |
| GAP-174 | 8.1 §8.1.6.5 | C03 has no line for the QA uplift, DevOps front-load, UX contractor, independent reviewer, pen tests or external counsel | Open — handling per source part |
| GAP-175 | 8.2 §8.2.6 | KPI-03, 05, 09, 10, 11, 15, 22, 26, 28 have "baseline" targets without values; baseline capture dates are set in §8.2.6 | Open — handling per source part |
| GAP-176 | 8.1 §8.1.3.4 | No Service Owner is named for SaaS activation and DEC-047 plan approval | Open — handling per source part |
| GAP-177 | 8.1 §8.1.1.3 | The organisation's holiday calendar and leave policy are not in the baseline | Open — handling per source part |
| GAP-178 | 8.2 §8.2.2.2 | No owner for help-centre content and training materials | Open — handling per source part |
| GAP-179 | 8.1 §8.1.3.3 | No tenant-facing status page or incident channel (Part 4.3 GAP-126) is decided before the first external tenant | Closed by DEC-406 |
| GAP-180 | 9.1 §9.1.5 | DEC-151 · E-91 · Part 9.2 (GAP-180) · No central tag allocation log · §9.2.3 reconstruction is authoritative; future tags continue from the highest number in each register · 9.2 | Closed by DEC-151 |
| GAP-181 | 9.1 §9.1.5 | DEC-148 · E-88 · Part 9.2 (GAP-181) · ID family collisions: AD-## (3.1 drivers vs 3.2 adapters), PP-## (1 principles vs 6.2 precondition profiles), D-# (3.3 drills vs 5.1a DoD items), B-## (3.1 cost rows vs budget lines B##) · IDs stay as written; cross-part … | Closed by DEC-148 |
| GAP-182 | 9.1 §9.1.5 | DEC-149 · E-89 · Part 9.2 (GAP-182) · 68 RECOMMENDATIONs have no recorded accept/reject · All proposed RECOMMENDATION-001…090 are accepted into the baseline under the delegated authority, except where a DEC states otherwise (e.g. ADR-043 superseded by … | Closed by DEC-149 |
| GAP-300 | 2.6 front matter | Referenced artefacts not supplied: "15-sheet commercial source cell inventory" (SP-11, SP-14) and "deck slides 10–14" (SP-11 MedMaarg segments) | Request from the founder; until then AP-ENH-A-05 is Pending and segment claims stay … |
| GAP-301 | 2.6 Document 03 End User Personas | Agency / managed-service operator persona and delegation model absent | P17, R21, FR-ENH-A-015 |
| GAP-302 | 2.6 Document 37 Sales & Marketing Automation | Service arrangement (self-service / managed / hybrid) not modelled | FR-ENH-A-015, CFG-ENH-A-07 |
| GAP-303 | 2.6 Document 14 Global Customer, Partner & A | Website legal disclosure per legal entity not specified | FR-ENH-A-017 |
| GAP-304 | 2.6 Document 11 Global Market Intelligence & | No coverage ledger or per-family freshness | FR-ENH-A-001, BRL-ENH-A-02 |
| GAP-305 | 2.6 Document 14 Global Customer, Partner & A | No acquisition operating plan or weekly review | FR-ENH-A-010, 012 |
| GAP-306 | 2.6 Document 03 End User Personas | NFR-034 baseline undefined | Productivity protocol §2.6.5.1.4 |
| GAP-307 | 2.6 Document 03 End User Personas | Integration administrator and template reviewer not defined | P18/R12I, P19/R11T |
| GAP-308 | 2.6 Document 12 Digital Marketing & Customer | No rule on meeting/webinar recording consent | BRL-ENH-A-05 |
| GAP-309 | 2.6 Document 11 Global Market Intelligence & | No benchmark sample design for discovery | FR-ENH-A-005 |
| GAP-310 | 2.6 Document 11 Global Market Intelligence & | Tool candidates (Scrapy, Trafilatura, SearXNG, PandaDoc, Crossbeam, PostHog, Socialinsider) not dispositioned | §2.6.5.6 |
| GAP-320 | 3.4 front matter | No load profile for the pack's growth column (250 sessions, 1 M opportunities, 100 k actions/day, 100 tenants) | Open — handling per source part |
| GAP-321 | 3.4 Document(s) 04/09/10 | No recovery class for regenerable research data | Open — handling per source part |
| GAP-322 | 3.4 Document(s) 10 | Adapter ports lack estimate/health and a denied outcome | Open — handling per source part |
| GAP-323 | 3.4 Document(s) 10 | Agent envelope lacks 7 of the 11 fields in doc 10 | Open — handling per source part |
| GAP-324 | 3.4 §D | No contract for product events from startups' own delivered products | Open — handling per source part |
| GAP-325 | 3.4 Document(s) 05 | Workflow definitions have no declared execution-policy block | Open — handling per source part |
| GAP-326 | 3.4 Document(s) 05 | Reply taxonomy lacks decline and meeting-request classes | Open — handling per source part |
| GAP-327 | 3.4 Document(s) 04 | No daily-operations runbook; client offboard and data-incident runbooks incomplete | Open — handling per source part |
| GAP-328 | 3.4 Document(s) 10 | No branch-coverage metric for critical decision code | Open — handling per source part |
| GAP-329 | 3.4 Document(s) 10 | No technical-debt register | Open — handling per source part |
| GAP-330 | 3.4 Document(s) 04 | Approval-gate items (38 API definitions, 4 DB confirmations, 138 UI mappings) not tracked | Open — handling per source part |
| GAP-331 | 3.4 Document(s) 05 | Pack integration candidates (PandaDoc, Crossbeam Skills, Socialinsider, PostHog) not evaluated | Open — handling per source part |
| GAP-332 | 3.4 Document(s) 10 | No website/portal/Admin URL route map | Open — handling per source part |
| GAP-333 | 3.4 Document(s) 04/09/10 | No composite dashboard load target | Open — handling per source part |
| GAP-334 | 3.4 Document(s) 05/10 | No fail-fast rule for mandatory configuration | Open — handling per source part |
| GAP-335 | 3.4 Document(s) 05 | No lawful meeting-notes summarization path (GAP-143 excludes recordings) | Open — handling per source part |
| GAP-340 | 2.7a front matter | 278 retained-baseline fields had no field-level specification in the blueprint | Open — handling per source part |
| GAP-341 | 2.7a §2.7.3.1 | No legacy screen ID crosswalk or retained website capability mapping | Open — handling per source part |
| GAP-342 | 2.7a §2.7.2 | 83 distinct legacy operations have no blueprint equivalent; 113 only an equivalent under another path | Open — handling per source part |
| GAP-343 | 2.7a §2.7.2 | 435 related-screen links not represented in navigation | Open — handling per source part |
| GAP-344 | 2.7a §2.7.3.1 | Per-screen integration associations, licence and capacity display not specified | Open — handling per source part |
| GAP-345 | 2.7a §2.7.3.1 | Optimization Intelligence panel not specified | Open — handling per source part |
| GAP-346 | 2.7a §2.7.3.1 | Dashboard latency load scenario (50/250 staff, 100k/1m opportunities) missing | Open — handling per source part |
| GAP-347 | 2.7a §2.7.3.1 | Design handoff record and design evidence pack missing | Open — handling per source part |
| GAP-348 | 2.7a §2.7.3.2 | Status footer items, filter result count and focus restoration missing | Open — handling per source part |
| GAP-349 | 2.7a §2.7.2 | No entity for sales_business_template or sales_ui_service_request; Part 3.2 support-case operations (API-440, API-442) have no entity | Open — handling per source part |
| GAP-360 | 3.5a front matter | Part 3.2 had no per-operation request/response field contracts | Open — handling per source part |
| GAP-361 | 3.5b §3.5.8 | 38 source operations have only descriptive payloads | Open — handling per source part |
| GAP-362 | 3.5a §3.5.3.1 | No operation-level SIT in Part 6 | Open — handling per source part |
| GAP-363 | 3.5b §3.5.8 | 24 operations missing in Part 3.2 | Open — handling per source part |
| GAP-364 | 3.5b §3.5.8 | Three adapter ports missing (storage/extraction, contact verification, own-site audit) | Open — handling per source part |
| GAP-365 | 3.5a §3.5.3.1 | Document 07's "4 database reuse/field confirmations" are not identified anywhere in the document | Open — handling per source part |
| GAP-366 | 3.5a §3.5.3.1 | The "catalog-complete OpenAPI draft" and the 164/164/165 offline examples are not in the package | Closed by DEC-264 |
| GAP-367 | 3.5a §3.5.3.1 | PubMed listed on 10 operations has no blueprint home | Open — handling per source part |
| GAP-388 | 3.6a §3.6.3 | Missing entities: business template, service request, eval case result (and milestone via CONFLICT-383); interim retention for service requests | Open — handling per source part |
| GAP-389 | 3.6a §3.6.3 | 113 column additions on 73 tables (incl. portal grant invite/redemption columns) | Open — handling per source part |
| GAP-390 | 3.6a §3.6.3 | 54 keys and indexes IX-ENH-E-01…54 | Open — handling per source part |
| GAP-391 | 3.6a §3.6.3 | No table-level exposure register | Open — handling per source part |
| GAP-392 | 3.6a §3.6.3 | No schema decision register; 136 field records, 4 blocked rows, 38 API and 138 UI approvals outstanding | Open — handling per source part |
| GAP-393 | 3.6a §3.6.3 | No tiered recovery objectives (regenerable data 24 h / 8 h) | Open — handling per source part |
| GAP-394 | 3.6a §3.6.3 | Restore-drill completeness (dispatch disabled, checksums, object inventory, config history, dedupe keys), disposable DBs and reference SQL smoke missing | Open — handling per source part |
| GAP-395 | 3.6a §3.6.3 | No data-layer offboarding runbook | Open — handling per source part |
| GAP-400 | 7.4a front matter | Source priority codes V/X/R are undefined in documents 16 and 21 | Open — handling per source part |
| GAP-401 | 7.4a §7.4.1.4 | The pack names none of the 100 use cases, 20 templates or 13 node types | Open — handling per source part |
| GAP-402 | 7.4a §7.4.3 | No blueprint entity records candidate, entitlement, approved spend, expiry or benchmark result | Open — handling per source part |
| GAP-403 | 7.4a §7.4.3 | No dependency/model-weight licence register | Open — handling per source part |
| GAP-404 | 7.4a §7.4.3 | No adapter retirement procedure | Open — handling per source part |
| GAP-405 | 7.4a §7.4.3 | Inter-agent envelope lacks six source fields | Open — handling per source part |
| GAP-406 | 7.4a §7.4.3 | Exact cache key lacks grant fingerprint and permission/policy revisions | Open — handling per source part |
| GAP-407 | 7.4a §7.4.3 | No post-ranking ACL recheck or revocation propagation to embeddings/caches | Open — handling per source part |
| GAP-408 | 7.4b §7.4.5.9 | No replacement-economics metrics (net saving, break-even, verified outcome cost) | Open — handling per source part |
| GAP-409 | 7.4a §7.4.3 | Part 8.2 lacks annual, quarterly, seats-only and paid-Apollo-runtime budget views | Open — handling per source part |
| GAP-410 | 7.4a §7.4.3 | No provider invoice-to-usage reconciliation | Open — handling per source part |
| GAP-411 | 7.4a §7.4.3 | Contribution margin per tenant stated (NFR-035) but not computed | Open — handling per source part |
| GAP-412 | 7.4b §7.4.5.11 | Enhancement effort 68–110 pd is outside the BRD §6 287–483 pd envelope | Open — handling per source part |
| GAP-420 | 6.8a front matter | Part 6 had no operation-level SIT TCs; CT-01…14 had no TC IDs | Open — handling per source part |
| GAP-421 | 6.8a §6.8.2.3 | 81 source operations have no Part 3.2 counterpart (list in Part 6.8a §6.8.3.4) | Open — handling per source part |
| GAP-422 | 6.8a §6.8.2.3 | No UAT pack for marketing or customer-success journeys | Open — handling per source part |
| GAP-423 | 6.8a §6.8.3.2 | EVR lacks execution statuses Not run and Blocked | Open — handling per source part |
| GAP-424 | 6.8a §6.8.3.1 | Capacity growth targets and the regenerable data class (RPO 24 h / RTO 8 h) are not in Part 4.2/4.3 | Open — handling per source part |
| GAP-425 | 6.8a §6.8.3.1 | Combined production preflight over six evidence groups is not in the blueprint | Open — handling per source part |
| GAP-440 | 6.9a §6.9.2.2 | Doc 38 counts 76 BRs; only 71 are enumerated anywhere in the pack | Closed by DEC-180 |
| GAP-441 | 6.9b §6.9.5.2 | The 172 expansion decisions have no IDs or individual records in the pack | Open — handling per source part |
| GAP-442 | 6.9a §6.9.2.2 | SM-SIT-A001…A302 not aliased in the blueprint RTM | Open — handling per source part |
| GAP-443 | 6.9a §6.9.3.1 | No layer-wise QC register, evidence manifest or layer sign-off | Open — handling per source part |
| GAP-444 | 6.9a §6.9.2.2 | No per-item approval record for source contract/DB/UI decisions | Open — handling per source part |
| GAP-445 | 6.9b §6.9.5.7 | No entities for EVR, QC, decision, trace approval, work item | Open — handling per source part |
| GAP-446 | 6.9a §6.9.3.1 | No regenerable-data RPO/RTO class | Open — handling per source part |
| GAP-447 | 6.9a §6.9.3.2 | Erasure scope omits derived embeddings and cached snippets | Open — handling per source part |
| GAP-448 | 6.9a §6.9.3.1 | No SaaS client service request entity | Open — handling per source part |
| GAP-449 | 6.9b §6.9.5.5.4 | No production credential handover procedure or access inventory | Open — handling per source part |
| GAP-450 | 6.9a §6.9.3.1 | Approval review effort (32.55/62.85/123.70 PD) unbudgeted | Open — handling per source part |
| GAP-451 | 6.9a §6.9.3.1 | No discipline baseline or estimate-vs-actual tracking | Open — handling per source part |
| GAP-452 | 6.9b §6.9.5.5.1 | No predeployment, daily operations or client offboarding runbook | Open — handling per source part |
| GAP-453 | 6.9b §6.9.5.5.5 | No artefact/version consistency or document inventory check | Open — handling per source part |
| GAP-460 | 4.4a §4.4.3.2 | The blueprint had no coding-standards, development-guideline and code-review document | Closed by §4.4.5.1 |
| GAP-461 | 4.4a §4.4.3.4 | No typed configuration contract with fail-closed validation | Closed by ENV-01…24, FR-ENH-I-041 |
| GAP-462 | 4.4a §4.4.3.1 | No recovery class for regenerable data (OKPI-33/34) | Closed by FR-ENH-I-020 |
| GAP-463 | 4.4a §4.4.3.3 | Release evidence completeness checked manually; no fail-closed validator | Closed by RGV, FR-ENH-I-060 |
| GAP-464 | 4.4a §4.4.3.8 | No delivery package or access handover at release | Closed by HO-T/B/A, FR-ENH-I-061 |
| GAP-465 | 4.4a §4.4.3.7 | No financial-exception or public-content runbook | Closed by RB-016, RB-017 |
| GAP-466 | 4.4a §4.4.3.6 | No penetration-test rules of engagement | Closed by PT-ROE |
| GAP-467 | 4.4a §4.4.3.7 | No budget pause operation (doc 31) | Candidate API-ENH-I-01/02, FR-ENH-I-051; Part 3.2 owner to accept |
| GAP-468 | 4.4a §4.4.3.8 | Pack approval-gate counts (38 API, 4 DB, 138 UI) and the 1,188-record preflight not reconciled to blueprint IDs | Coordinator with groups owning docs 06/07/08/38 |
| GAP-469 | 4.4a §4.4.3.4 | No developer/operator access review and offboarding procedure | Closed by ACC-01…07 |
| GAP-480 | 8.3c §8.3.5.15.3 | 8.3c OKPI-32 | Open — handling per source part |
| GAP-481 | 8.3c §8.3.5.15.3 | 8.3c OKPI-33/34 | Open — handling per source part |
| GAP-482 | 8.3b §8.3.5.4 | 8.3a/8.3b | Open — handling per source part |
| GAP-483 | 8.3b §8.3.5.8 | 8.3b §8.3.5.8 | Open — handling per source part |
| GAP-484 | 8.3c §8.3.5.13.6 | 8.3c §8.3.5.13.6 | Open — handling per source part |
| GAP-485 | 8.3c §8.3.5.14 | 8.3c §8.3.5.14 | Open — handling per source part |
| GAP-486 | 8.3c §8.3.5.15 | 8.3c §8.3.5.15 | Open — handling per source part |
| GAP-487 | 8.3c §8.3.5.15.5 | 8.3c TC-ENH-J-002 | Open — handling per source part |
| GAP-488 | 8.3a §8.3.4.1 | 8.3a §8.3.4.1 | Open — handling per source part |
| GAP-489 | 8.3a §8.3.3.3 | 8.3c §8.3.5.13.5 | Open — handling per source part |
| GAP-490 | 8.3a §8.3.4.1 | 8.3a §8.3.4.1 | Open — handling per source part |
| GAP-510 | 6.6 front matter | Part 2.7a stories US-01-EC01, US-04-EC01, US-17-EC01…04, US-19-EC01, US-21-EC01 are Gherkin features without AC IDs, story fields or FR links | Open — handling per source part |
| GAP-511 | 6.6 §6.6.13.2 | Part 3.6b stories US-01-EE01, US-14-EE01, US-20-EE01/02, US-21-EE01/02 state AC inline ("AC-1 …") without IDs | Open — handling per source part |
| GAP-512 | 6.6 §6.6.13.2 | Part 4.4b TC-ENH-I rows cite control IDs (CS-, RGV-, SMK-) in their Requirement column rather than the FR-ENH-I they verify; six FR-ENH-I had no test | Open — handling per source part |
| GAP-513 | 6.10 §6.10.8 | 54 of 245 QCs had blueprint_verification_refs that are section citations with no test, VER or control ID | Open — handling per source part |
| GAP-514 | 6.6 §6.6.13.2 | Part 6.5 cites "Batch 6.6 §6.6.9" for the tag register; Part 6.6 now numbers the register §6.6.13 after adding sections h, i, j | Open — handling per source part |
| GAP-520 | 9.6a §9.6a | The investor product’s deployment inventory is owned outside this programme and must be supplied for the “two products, four frontends” inspection | Closed by DEC-252 |
| GAP-610 | 9.7a front matter | Per-locale quality of the gateway models for Odia, Bengali, Telugu, Marathi, Kannada, Malayalam and Gujarati is not yet measured | Per-locale eval (TC-ADV-X1-045) before enabling each locale |
| GAP-611 | 9.7b §9.7.14.2 | Current Meta WhatsApp pricing, service-window and AI-use policy must be verified | Verify at implementation (as of 27 Nov 2026) |
| GAP-612 | 9.7b §9.7.14.1 | Legal review cost and content for the memory DPIA, conversation-intelligence notice and concierge terms are not estimated | Obtain counsel quotes (as GAP-174) |
| GAP-613 | 9.7b §9.7.17 | No labelled outcome data yet for propensity and churn | Accumulates from Release 1; data gates in §9.7.3.3 |
| GAP-614 | 9.7b §9.7.17 | Maturity of OpenTelemetry GenAI semantic conventions and Langfuse support for them | Verify at implementation |
| GAP-615 | 9.7b §9.7.17 | Final application dates of EU AI Act obligations under the Digital Omnibus | Verify each quarter |
| GAP-616 | 9.7b §9.7.17 | Answer-library ownership (who owns which answer families) is undefined | Define in A1 sprint 1 |
| GAP-617 | 9.7b §9.7.17 | NBA action catalogue content (actions per stage and startup) needs Product Owner definition | Workshop before A2 |
| GAP-660 | 9.8b §9.8.13 | External legal counsel not estimated for partner agreements, voice-call rules and survey consent by jurisdiction | Obtain quotes; R10 |
| GAP-661 | 9.8b §9.8.13.2 | Third-party intent data vendors' terms, data rights and prices unknown | Benchmark and quote before any enablement |
| GAP-665 | 9.8b §9.8.16 | No HR policy exists for any use of recognition data in performance management | Closed by DEC-398 |
| GAP-710 | 9.9a §9.9.5.15 | DEC-047 has no named "Enterprise" plan; BYOK is mapped to Scale (custom) | Open; Service Owner |
| GAP-711 | 9.9a §9.9.5.16 | No registered DPDP consent manager engaged; adapter readiness only | Open; R10 to monitor registrations |
| GAP-712 | 9.9a ADR-136 Zero-trust Admin access: passkey | No device-management (MDM) in the organization; device certificates via step-ca | Open |
| GAP-713 | 9.9a §9.9.3.1 | Developer terms of use, API licence and BYOK acceptance text not drafted; counsel cost not estimated | Open; legal |
| GAP-714 | 9.9b §9.9.13.1 | No SOC 2 auditor or budget identified | Open; only on trigger |

<!-- GEN:GAP:END -->

### 9.2.4(c) CONFLICT register (with resolution status)

Resolution sources: **Part 0A** (DEC-001…065), **Part 9.1** (DEC-066…140, including the second review cycle §9.1.4) or **locally** in the issuing part (the register row states the rule applied).

<!-- GEN:CONFLICT:BEGIN -->

| ID | First seen | Conflict (statement) | Resolution status |
|---|---|---|---|
| CONFLICT-001 | 0 §0.3.3 | Precision target: "≥80% precision on reviewed pilot sample" vs "Precision ≥90% on approved benchmark" | Resolved — Part 0A (DEC-001) |
| CONFLICT-002 | 0 §0.5 | Fundraising is excluded, yet fundraising/investor wording remains: "customize offerings or funding goals", "Offerings or fundraising thesis" (W33), "offering/issuer thesis", "investment/delivery geography" (filters), "verified funding" … | Resolved — Part 0A (DEC-002) |
| CONFLICT-003 | 0 §0.5 | "M01 Identity: already developed in AppNAI" and "M02 Approved AppNAI product truth" vs an independent, multi-startup product | Resolved — Part 0A (DEC-003) |
| CONFLICT-004 | 0 §0.5 | Pilot base run cost ₹14,500 (table) vs "base runtime ₹15,000 before contingency" vs illustrative ₹15–60k | Resolved — Part 0A (DEC-004) |
| CONFLICT-005 | 0 §0.5 | Effort 287–483 person-days with ~3 FTE (≈ 66 pd/month) gives ≈ 4.3–7.3 months, vs a 90-day foundation and 180-day rollout. Also "₹9–13.5L / 3 months" covers only ≈ 198 pd | Resolved — Part 0A (DEC-005) |
| CONFLICT-006 | 0 §0.5 | "One consolidated dependency-ordered plan; no separate product release labels" vs this blueprint's required Release 1 / 2 / Future and MoSCoW | Resolved — Part 0A (DEC-006) |
| CONFLICT-007 | 0 §0.5 | AI provider: "Claude/OpenAI API", "low-cost model routing", "rules → small model → advanced only when required" vs this prompt's "Claude Sonnet primary + free-tier fallback chain" | Resolved — Part 0A (DEC-007) |
| CONFLICT-008 | 0 §0.5 | AI budget: ₹3,000/month production inference reserve vs Sonnet-primary across many agents and discovery volumes | Resolved — Part 0A (DEC-008) |
| CONFLICT-009 | 0 §0.5 | "React operator workspace and separate React admin workspace … shared PostgreSQL" vs "two frontends: commercial-website-react and commercial-admin-react" and "independent PostgreSQL per product"; also "Automation: connected separate admin … | Resolved — Part 0A (DEC-009) |
| CONFLICT-010 | 0 §0.5 | A104 (bid desk) and A105 (order/fulfilment desk) map only to B-TENANT, but they implement the Project-bid and Order/fulfilment workflows and depend on M43/M44/M46/M47 | Resolved — Part 0A (DEC-010) |
| CONFLICT-011 | 0 §0.5 | Scoring components are "normalized 0–1", but thresholds are "≥75 / 50–74 / <50" | Resolved — Part 0A (DEC-011) |
| CONFLICT-012 | 0 §0.5 | The engineering estimate is said to be "superseded", yet the "original estimate retained: ₹9–13.5L/3 months; ₹18–27L/6 months" | Resolved — Part 0A (DEC-012) |
| CONFLICT-013 | 0 §0.5 | "MVP growth dashboard" (M30 label in BRD §12) vs "no separate product release labels" | Resolved — Part 0A (DEC-013) |
| CONFLICT-014 | 0 §0.5 | BRD §15 and §16 (and FRD §14/§15) repeat the same acceptance procedures with slightly different wording | Resolved — Part 0A (DEC-014) |
| CONFLICT-101 | 3.1 front matter | DEC-018 RTO ≤ 4 h (all failures) vs DEC-040 single-region pilot | Resolved — Parts 9.1 + 9.5 (DEC-079, DEC-158) |
| CONFLICT-102 | 3.1 §3.1.6.2 | B01 ₹5,000 vs DEC-040 pilot topology plus staging | Resolved — Part 9.1 (DEC-105) |
| CONFLICT-103 | 3.1 §3.1.16 | DEC-015 "105 named operations" vs 102 distinct FRD-named entries (104 HTTP operations) | Resolved — Part 9.1 (DEC-104) |
| CONFLICT-106 | 3.3 §3.3.3.2 | Homonyms in the sources: Plan, Subscription, Feedback, Event (two meanings each); Execution = Run. Resolved by distinct physical names | Resolved locally in Part 3.3 |
| CONFLICT-107 | 3.3 §3.3.11.1 | Rejected leads purged at 6 months (DEC-028) vs rejected opportunities never contacted (BRL-ELG-15). Resolved: keep an exclusion hash in suppression | Resolved locally in Part 3.3 |
| CONFLICT-108 | 3.3 §3.3.3.2 | Audit log 7 years vs financial 8 years / contracts term + 8 years: approvals and audit events about financial/contract objects follow the governed object's retention | Resolved locally in Part 3.3 |
| CONFLICT-109 | 3.3 §3.3.6.9 | Marketing contact 24 months vs contract signer evidence term + 8 years. Resolved: marketing profile erased, contractual signer record retained under CTR | Resolved locally in Part 3.3 |
| CONFLICT-110 | 4.1 front matter | B07 (₹500/month monitoring/security/CI) and B21 (CDN/WAF, ₹0 until approved) vs the need for AWS WAF on public intake (NFR-022, THR-003) and possible CI minute overage | Resolved — Part 9.1 (DEC-081) |
| CONFLICT-111 | 4.1 §4.10.2 | DEC-028 sets AI run logs and chat transcripts at 90 days, and no retention for security/application logs. CERT-In requires ICT logs for 180 days in India, and the DPDP Rules are understood to require processing logs for one year (verify) | Resolved — Part 9.1 (DEC-078) |
| CONFLICT-112 | 4.2 §4.23.2 | DEC-018 RTO ≤ 4 h vs DEC-040 pilot topology (single-region, single-AZ application, backups copied cross-region): a full regional outage cannot be recovered in 4 h without pre-provisioned DR infrastructure, which B01 (₹5,000) does not fund | Resolved — Part 9.1 (DEC-079) |
| CONFLICT-113 | 4.2 §4.23.7 | DEC-044 support hours (10:00–18:00 IST, Mon–Sat) vs 24×7 availability SLOs (DEC-018) and Critical escalation in 30 min (Part 2.4 §2.30.2) | Resolved — Part 9.1 (DEC-080) |
| CONFLICT-114 | 4.1 TB-03 Admin Command Centre | DEC-019 spike check 5 expects WebAuthn for privileged roles, while BRL-TEN-08 says "TOTP minimum, WebAuthn recommended" | Resolved — Part 9.1 (DEC-077) |
| CONFLICT-120 | 7.1 front matter | DEC-007 groups self-hosted open models with free-tier fallbacks (Tier 2), while BRL-AI-06 restricts Tier 2 to Public/Internal-non-personal; a self-hosted model in our VPC has none of the third-party data risk | Resolved locally in Part 7.3 |
| CONFLICT-121 | 6.4 §6.4.10.1 | The Copilot panel is part of the W0–W2 shell (DEC-062, Part 2.5) but DEC-035 sets no wave for Copilot capability | Resolved locally in Part 7.3 |
| CONFLICT-122 | 6.4 §6.4.9.2 | B02 is "production inference", but eval runs (M54) and CI review consume API tokens | Resolved — Part 9.1 (DEC-090) |
| CONFLICT-130 | 5.1a front matter | DEC-034 W0 scope (≈ 113.5 SP mid in this batch alone) and W0 + W1 content (≈ 167.5 SP) exceed the Day 1–15 and Day 1–30 capacity at DEC-005 velocity (≈ 48 pd and ≈ 96 pd) | Resolved — Part 9.1 (DEC-096) |
| CONFLICT-131 | 5.1c §5.9.3 | Part 0 §0.10.2 lists A003 under EP-01 and W12–W17 under EP-07, while Part 2.1 maps FR-A003 to EP-17 and FR-W14–W16 to EP-14 | Resolved — Part 9.1 (DEC-097) |
| CONFLICT-132 | 5.1b §5.8.2.1 | FR-A103 belongs to EP-20 (W5) in Part 2.1, but DEC-039 imports are needed in W1 (Part 2.1 itself notes "W1 import") | Resolved — Part 9.1 (DEC-073) |
| CONFLICT-133 | 5.2 US-1403 Tender deadline guard | BRL-BID-01 blocks submission at deadline − buffer, but DEC-053 makes submission a human act outside the system; blocking evidence recording inside the buffer would make records diverge from reality. Resolution: the buffer locks internal … | Resolved — Part 9.1 (DEC-068) |
| CONFLICT-134 | 5.2 US-0903 Public and portal meeting bookin | BRL-MTG-02 fixes a 15-minute slot hold, while Part 2.5 §2.46 (WCAG 2.2.1) requires a warning and an option to extend. Resolution: one 15-minute extension after a fresh free/busy check, warned ≥ 60 s before expiry | Resolved — Part 9.1 (DEC-069) |
| CONFLICT-135 | 5.2 US-0813 Omnichannel identity links and n | Part 0 §0.10.2 lists A046 under EP-08, but Part 2.1 maps FR-A046 to EP-10. Resolution: follow Part 2.1 (later, more specific); A046 is in EP-10 (US-1006); the M41 routing engine stays in EP-08 (US-0813) | Resolved locally in Part 5.2 |
| CONFLICT-136 | 5.3 front matter | Part 0 §0.10.2 lists BR-M09 under EP-01, while Part 1 §1.12.1 maps BR-M09 to EP-21. Resolution in this batch: follow Part 1 (later and more specific); BR-M09 stories are US-2101, US-2102, US-2103, US-2108 | Resolved — Part 9.1 (DEC-072) |
| CONFLICT-137 | 5.3 §5.30.1 | Part 0 §0.10.2 lists EP-19 screens W01–W10, while Part 2.1 assigns W08, W09 to EP-11 and W10 to EP-12. Resolution: follow Part 2.1; EP-19 provides shared enablers only | Resolved locally in Part 5.3 |
| CONFLICT-138 | 5.3 US-2008 Import with dry-run validation a | FR-A103 import is W1 (DEC-039) but sits in EP-20 (a W5 epic) under BR-SVC (Should), although owned startups (BR-TENANT, Must) need import in W1. Resolution: US-2008 is scheduled in W1 at Should (cannot exceed its BR); the Product Owner … | Resolved — Part 9.1 (DEC-073) |
| CONFLICT-140 | 8.1 front matter | Errata 34 defines W0-A as environments, identity spike, CI, RLS/outbox/PDP skeletons and catalogue core, while Part 5.1a §5.5.3 lists US-0104, US-0301, US-0401, US-0402 and US-0404 in W0-A. Resolution: errata 34 is binding; those five … | Resolved — Part 9.1 (DEC-125) |
| CONFLICT-141 | 8.1 §8.1.2.2 | The full DEC-034 W0 scope (139 SP mid including EP-17 and EP-21 W0 stories) cannot complete by Day 30 even with the split. Resolution: Gate W0-B (Day 30) checks the control set built in Sprint 1; a W0-B completion checkpoint on Day 40 … | Resolved — Part 9.1 (DEC-125) |
| CONFLICT-142 | 3.4 Document(s) 04 | BRD §8 day-phase gates vs DEC-005 capacity distribution: Release 1 content ≈ 307 pd vs ≈ 169 pd capacity by Day 90. Resolution: RECOMMENDATION-081 (re-baselined calendar) with Option E available | Resolved — Part 9.1 (DEC-124) |
| CONFLICT-143 | 8.1 §8.1.8.2 | Pen-test timing: Part 4.1 §4.16 "before Release 1 production exposure of the portal (end W3)" vs Part 6.1 RECOMMENDATION-073 "before the first real controlled pilot (W4)". Resolution: pen test 1 at Day 141–150 covers both (portal live in … | Resolved — Part 9.1 (DEC-126) |
| CONFLICT-144 | 8.2 §8.2.1.2 | Part 3.1 ADR-043 plans "no paid WAF at pilot", while errata 18 requires AWS WAF from W2; errata 18 also says "B07 is revised" without a figure. Resolution: errata 18 governs; WAF is charged to B21 (≈ ₹1,300–1,800/month) from public intake … | Resolved — Part 9.1 (DEC-127) |
| CONFLICT-300 | 2.6 front matter | Two opportunity scoring models | Resolved — Part 9.5 (DEC-211) |
| CONFLICT-301 | 2.6 Document Common core (shared by all 38 d | Residual investor/fundraising wording in group A documents | Resolved — Part 9.5 (DEC-179) |
| CONFLICT-302 | 2.6 Document 11 Global Market Intelligence & | Definition of source coverage | Resolved — Part 9.5 (DEC-212) |
| CONFLICT-303 | 2.6 Document 12 Digital Marketing & Customer | Reply classification taxonomy | Resolved — Part 9.5 (DEC-213) |
| CONFLICT-304 | 2.6 Document 13 Sales Intelligence & Commerc | Single relationship stage vs separate state machines | Resolved — Part 9.5 (DEC-214) |
| CONFLICT-320 | 3.4 front matter | Deployment technology: ECS Fargate + ALB + ElastiCache Redis + "Redis broker" | Resolved — Part 9.5 (DEC-163) |
| CONFLICT-321 | 3.4 Document(s) 04/09/10 | Capacity design points: initial 25 owned / 10 external; growth 50+ / 100 | Resolved — Part 9.5 (DEC-161) |
| CONFLICT-322 | 3.4 Document(s) 04/09/10 | Growth RTO ≤ 2 h | Resolved — Part 9.5 (DEC-158) |
| CONFLICT-323 | 3.4 Document(s) 05/10 | Availability "99.9% critical availability over rolling 30 days" | Resolved — Part 9.5 (DEC-157) |
| CONFLICT-324 | 3.4 Document(s) 04 | Budget alert thresholds 70/90% | Resolved — Part 9.5 (DEC-162) |
| CONFLICT-325 | 3.4 Document(s) 04 | "No cross-region replication before approval" | Resolved — Part 9.5 (DEC-164) |
| CONFLICT-326 | 3.4 Document(s) 05 | Investor-product wording: "lead/investor record", "investor/customer tokens", "investment/commercial Django domains", event product = investment_or_commercial | Resolved — Part 9.5 (DEC-179) |
| CONFLICT-327 | 3.4 Document(s) 10 | Agent decomposition: "six runtime responsibilities" vs 18 responsibilities vs blueprint catalogue | Resolved — Part 9.5 (DEC-183) |
| CONFLICT-328 | 3.4 Document(s) 04 | Effort and critical path: 385 PD base for 149 work items; dependency-only path 113.5 days | Resolved — Part 9.5 (DEC-181) |
| CONFLICT-329 | 3.4 Document(s) 04/09 | Names: Django apps (accounts, catalog, …, reporting) and monorepo paths (apps/growth-ui, …) | Resolved — Part 9.5 (DEC-183) |
| CONFLICT-330 | 3.4 §D | Product webhook into the marketing database vs "no live cross-product join or automatic handoff" | Resolved — Part 9.5 (DEC-169) |
| CONFLICT-340 | 2.7a front matter | Residual investor wording not in DEC-002's replacement list: "separate from investor/customer journey" (W31), "not a marketplace investor or customer" (W32), "separately from investor/customer portal", "no … investor/customer records" … | Resolved — Part 9.5 (DEC-179) |
| CONFLICT-341 | 2.7a §2.7.3.1 | "Inspect … two products, four frontends" vs DEC-009 "two frontends only" | Resolved — Part 9.5 (DEC-169) |
| CONFLICT-342 | 2.7a §2.7.2 | Breakpoints: doc 17 desktop ≥ 1200, tablet 768–1199, mobile < 768, tests at 360/768/1440; Part 2.5 §2.48 five tiers (360–599, 600–899, 900–1279, 1280–1679, ≥ 1680); DEC-043 Admin desktop-first 1280 px, usable to 768 px for review/approval | Resolved — Part 9.5 (DEC-215) |
| CONFLICT-343 | 2.7a §2.7.3.1 | API namespaces: doc 06 uses /api/v1/sales/* (A099–A106) and /api/v1/commercial/workspace/{public,client,onboarding,admin}/* (W31–W34, A109–A113); Part 3.2 uses ~/admin/*, ~/portal/*, ~/public/* | Resolved — Part 9.5 (DEC-170) |
| CONFLICT-344 | 2.7a §2.7.4.3 | Generic POST …/{id}/control (12 resources) vs per-action endpoints in Part 3.2 (approve, issue, cancel, suspend, pause, resume, publish, rollback …) | Resolved — Part 9.5 (DEC-171) |
| CONFLICT-345 | 2.7a §2.7.4.3 | Legacy per-object approve/review routes (e.g. /contracts/{id}/approve, /proposals/{id}/review, /messages/drafts/{id}/review, /insurance/pilots/{id}/approve) vs Part 3.2's single Approval resource with only four retained aliases | Resolved — Part 9.5 (DEC-172) |
| CONFLICT-346 | 2.7a §2.7.2 | Development-time Claude plugins (for example CLAUDE.md Management, Claude Code Setup, Plugin Developer Toolkit, Skill Creator, Figma, Postman, document skills) are listed as integrations of runtime screens (A006, A008, A011, A014, A017, … | Resolved — Part 9.5 (DEC-202) |
| CONFLICT-347 | 2.7a §2.7.4.7 | Doc 06 states provider prices as facts (for example a per-million-token rate for a named Claude model, per-credit search pricing, hosted plan fees) | Resolved — Part 9.5 (DEC-202) |
| CONFLICT-348 | 2.7a §2.7.3.1 | OPT-02-04 "read projections refresh ≤ 60 s" vs NFR-047 dashboards ≤ 15 min (A110 monitor ≤ 5 min) | Resolved — Part 9.5 (DEC-160) |
| CONFLICT-349 | 2.7a §2.7.3.1 | Scale figures: OPT-06-01 "25 owned + 10 external initial; 50+ owned + 100 external growth"; dashboard procedure "50/250 concurrent staff, 100k/1m opportunities" vs DEC-031 (Year 1: 25–40 workspaces, 2–10 tenants, 15–60 users; Year 2: 100 … | Resolved — Part 9.5 (DEC-161) |
| CONFLICT-350 | 2.7a §2.7.5.1 | Retained capability 082 (website) lists POST /api/v1/invoices/{id}/payment-link, an Admin operation, among its operations | Resolved — Part 9.5 (DEC-175) |
| CONFLICT-351 | 2.7a §2.7.5.4 | Source single table sales_data_transfer vs blueprint saas_import_job + saas_export_job; source sales_ui_trigger_revision / sales_ui_template_revision vs blueprint versioned aut_trigger / aut_workflow_template | Resolved — Part 9.5 (DEC-190) |
| CONFLICT-360 | 3.5a front matter | Path canon. Document 07 retains "canonical legacy method/path contracts" for 288 operations (e.g. /api/v1/sales/tenants, /api/v1/admin/jobs), while Part 3.2 keeps only the 104 FRD-named paths and gives every other operation a derived ~/ … | Resolved — Part 9.5 (DEC-170) |
| CONFLICT-361 | 3.5a §3.5.3.1 | Idempotency key and revision as body fields (source) vs headers (Part 3.2) | Resolved — Part 9.5 (DEC-173) |
| CONFLICT-362 | 3.5a §3.5.3.1 | List contract naming: page_size / items / next_cursor vs limit / data / page.next_cursor | Resolved — Part 9.5 (DEC-174) |
| CONFLICT-363 | 3.5b §3.5.5.1 | Async response job_id with states queued | Resolved — Part 9.5 (DEC-174) |
| CONFLICT-364 | 3.5a §3.5.3.1 | Source-local DEC-001…038 collide with binding DEC-001…065 | Resolved — Part 9.5 (DEC-178) |
| CONFLICT-365 | 3.5a §3.5.3.1 | Inventory counts (288 vs 302; 138 vs 147 UI; 149 vs 155 vs 199 entities; 302 vs 555 operations) | Resolved — Part 9.5 (DEC-180) |
| CONFLICT-366 | 3.5a §3.5.3.1 | Audience mismatches on five "Portal + Admin" operations (consents, privacy requests, meetings/book, payment-link, onboarding complete) and one Admin acceptance route | Resolved — Part 9.5 (DEC-175) |
| CONFLICT-367 | 3.5a §3.5.3.1 | Token routes under /public/ are "restricted portal endpoints" (source) but API-083 is classified public; agreements, payment status and onboarding are token routes in the source but portal-session routes in Part 3.2 | Resolved — Part 9.5 (DEC-175) |
| CONFLICT-368 | 3.5b §3.5.5.6.4 | Budget allocation per provider (B07/B10 "shared optional") vs DEC-020 dedicated lines (B13, B15, B16, B18, B22) | Resolved — Part 9.5 (DEC-198) |
| CONFLICT-369 | 3.5b §3.5.6 | Retention policy operation: source "Version data-class retention" (create versions freely) vs Part 3.2 API-091 "tighten override only" (DEC-028) | Resolved — Part 9.5 (DEC-177) |
| CONFLICT-370 | 3.5a §3.5.3.1 | Status codes: 24 source proposals differ from the SE-class rule; bid control lists submit as an action | Resolved — Part 9.5 (DEC-176) |
| CONFLICT-371 | 3.5b §3.5.5.6.2 | Provider shortlists: e-sign PandaDoc (source) vs Indian Aadhaar eSign/DSC providers + DocuSign (DEC-023, AD-10); social publishing through Postiz (AGPL self-host) vs direct platform APIs (AD-08) | Resolved — Part 9.5 (DEC-197) |
| CONFLICT-372 | 3.5a §3.5.3.1 | Integration "claude/openai api" on AI operations | Resolved — Part 9.5 (DEC-192) |
| CONFLICT-380 | 3.6a §3.6.0 | Doc 08 numbers its four schema decisions DEC-039…DEC-042; blueprint DEC-039 is the seed-migration decision and DEC-040…042 have other meanings | Resolved — Part 9.5 (DEC-178) |
| CONFLICT-381 | 3.6a §3.6.3 | Doc 08 leaves the embedding dimension open ("vector(d)", "do not guess") while Part 3.3 fixes halfvec(1024) | Resolved — Part 9.5 (DEC-184) |
| CONFLICT-382 | 3.6a §3.6.3 | Doc 08 says reuse the existing identity tables and "no duplicate identity tables"; Part 3.3 defines ten_user as a product-local identity mirror | Resolved — Part 9.5 (DEC-185) |
| CONFLICT-383 | 3.6a §3.6.4.2 | Doc 08 sales_fulfillment is a mutable milestone with state and due date; Part 3.3 com_fulfillment_event is append-only evidence | Resolved — Part 9.5 (DEC-186) |
| CONFLICT-384 | 3.6a §3.6.4.7 | Doc 08 business keys are global (unique(code), unique(base_url), unique(invoice_no)); FRD §5 and DEC-009 require tenant/startup scope | Resolved — Part 9.5 (DEC-187) |
| CONFLICT-385 | 3.6a §3.6.3 | Doc 28 sets RTO ≤ 2 h "growth"; DEC-018/DEC-079 set RTO ≤ 4 h (and 24 h regional at pilot) | Resolved — Part 9.5 (DEC-158) |
| CONFLICT-386 | 3.6a §3.6.4.6 | Doc 08 sales_order.direction includes service, training and project; Part 3.3 com_order.direction is sell/buy only | Resolved — Part 9.5 (DEC-188) |
| CONFLICT-387 | 3.6b §3.6.6 | Doc 08 growth_sequence_step.delay_seconds vs Part 3.3 wait_business_days | Resolved — Part 9.5 (DEC-189) |
| CONFLICT-400 | 7.4a front matter | Model strategy | Resolved — Part 9.5 (DEC-192) |
| CONFLICT-401 | 7.4a §7.4.3 | Search primary | Resolved — Part 9.5 (DEC-193) |
| CONFLICT-402 | 7.4a §7.4.3 | Extraction primary | Resolved — Part 9.5 (DEC-194) |
| CONFLICT-403 | 7.4a §7.4.3 | Budget alert thresholds | Resolved — Part 9.5 (DEC-162) |
| CONFLICT-404 | 7.4a §7.4.3 | Schema-valid threshold | Resolved — Part 9.5 (DEC-195) |
| CONFLICT-405 | 7.4a §7.4.3 | Classification precision | Resolved — Part 9.5 (DEC-196) |
| CONFLICT-406 | 7.4a §7.4.3 | Investor wording | Resolved — Part 9.5 (DEC-179) |
| CONFLICT-407 | 7.4a §7.4.3 | Candidate mis-mapping | Resolved — Part 9.5 (DEC-199) |
| CONFLICT-408 | 7.4b §7.4.6 | Hunter budget line | Resolved — Part 9.5 (DEC-198) |
| CONFLICT-409 | 7.4a §7.4.3 | Error tracking | Resolved — Part 9.5 (DEC-200) |
| CONFLICT-410 | 7.4a front matter | Section numbering | Resolved — Part 9.5 (DEC-182) |
| CONFLICT-411 | 7.4a §7.4.3 | Cost routing as AI task | Resolved — Part 9.5 (DEC-201) |
| CONFLICT-412 | 7.4a §7.4.3 | Pilot runtime figure | Resolved — Part 9.5 (DEC-198) |
| CONFLICT-420 | 6.8a front matter | DEC-094 retains SM-UT-037, -049 and -050 as unassigned aliases with no test obligation, but document 22 defines them (webhook signature/replay; planned offering cannot be published; wellness need matching) | Resolved — Part 9.5 (DEC-204) |
| CONFLICT-421 | 6.8a §6.8.3.1 | Unit coverage gates differ: document 22 "≥ 80% domain-service branch", document 19 "critical branch ≥ 90%", Part 6.1 §6.1.9.6 "domain core ≥ 90% branch + mutation score", NFR-082 "branch ≥ 70% overall" | Resolved — Part 9.5 (DEC-203) |
| CONFLICT-422 | 6.8a §6.8.3.3 | Document 22 SM-UT-057 uses an absolute INR discount; DEC-038 thresholds and BRL-APR-04 are percentages | Resolved — Part 9.5 (DEC-208) |
| CONFLICT-423 | 6.8a §6.8.3.2 | Severity scales: document 22 "Critical/P0 … Low/P3" vs Part 6.1 S1–S4 with separate fix priority FP1–FP4 | Resolved — Part 9.5 (DEC-205) |
| CONFLICT-424 | 6.8a §6.8.3.1 | Growth-point RTO for critical data ≤ 2 h (document 19) vs DEC-018 RTO ≤ 4 h | Resolved — Part 9.5 (DEC-158) |
| CONFLICT-440 | 6.9a §6.9.3.2 | Critical-rule branch coverage | Resolved — Part 9.5 (DEC-203) |
| CONFLICT-441 | 6.9a §6.9.3.1 | Capacity and workload targets | Resolved — Part 9.5 (DEC-161) |
| CONFLICT-442 | 6.9a §6.9.3.1 | Semantic approval coverage | Resolved — Part 9.5 (DEC-203) |
| CONFLICT-443 | 6.9a §6.9.3.1 | Projection refresh | Resolved — Part 9.5 (DEC-160) |
| CONFLICT-444 | 6.9a §6.9.3.1 | Growth critical RTO | Resolved — Part 9.5 (DEC-158) |
| CONFLICT-445 | 6.9a §6.9.1.3 | Decision ID collision | Resolved — Part 9.5 (DEC-178) |
| CONFLICT-446 | 6.9a §6.9.3.1 | Expansion effort | Resolved — Part 9.5 (DEC-181) |
| CONFLICT-447 | 6.9a §6.9.3.1 | BR traces on 11 FRs | Resolved — Part 9.5 (DEC-180, DEC-313) |
| CONFLICT-460 | 4.4a §4.4.4.1 | Critical-service availability | Resolved — Part 9.5 (DEC-157) |
| CONFLICT-461 | 4.4a §4.4.3.1 | Capacity design points | Resolved — Part 9.5 (DEC-161) |
| CONFLICT-462 | 4.4a §4.4.3.1 | Recovery time | Resolved — Part 9.5 (DEC-158) |
| CONFLICT-463 | 4.4a §4.4.3.1 | Projection refresh | Resolved — Part 9.5 (DEC-160) |
| CONFLICT-464 | 4.4a §4.4.3.7 | 5xx alert threshold (internal to doc 31) | Resolved — Part 9.5 (DEC-165) |
| CONFLICT-465 | 4.4a §4.4.3.5 | Spike multiplier (internal to doc 29) | Resolved — Part 9.5 (DEC-161) |
| CONFLICT-466 | 4.4a §4.4.3.5 | Traffic mix | Resolved — Part 9.5 (DEC-161) |
| CONFLICT-467 | 4.4a §4.4.3.5 | Soak duration | Resolved — Part 9.5 (DEC-161) |
| CONFLICT-468 | 4.4a §4.4.3.2 | Coverage gate | Resolved — Part 9.5 (DEC-203) |
| CONFLICT-469 | 4.4a §4.4.3.7 | Five doc-31 API paths | Resolved — Part 9.5 (DEC-170) |
| CONFLICT-470 | 4.4a §4.4.4.1 | Product topology | Resolved — Part 9.5 (DEC-169) |
| CONFLICT-471 | 4.4a §4.4.3.3 | Environment set | Resolved — Part 9.5 (DEC-166) |
| CONFLICT-472 | 4.4a §4.4.3.6 | Vulnerability severity basis | Resolved — Part 9.5 (DEC-168) |
| CONFLICT-473 | 4.4a §4.4.3.3 | Queue topology | Resolved — Part 9.5 (DEC-167) |
| CONFLICT-480 | 8.3a §8.3.4.6 | Projection refresh ≤ 60 s for all scoped projections (OKPI-28, OPT-02-04) | Resolved — Part 9.5 (DEC-160) |
| CONFLICT-481 | 8.3c §8.3.5.15.3 | Usage anomaly alerts at 70% and 90% of cap; pause optional jobs at cap (OPT-03-08) | Resolved — Part 9.5 (DEC-162) |
| CONFLICT-482 | 8.3c §8.3.5.13.6 | Critical availability ≥ 99.9% rolling 30 days (OKPI-06, OPT-05-07) | Resolved — Part 9.5 (DEC-157) |
| CONFLICT-483 | 8.3c §8.3.5.15.3 | Growth validation 50+ owned startups and 100 external tenants (OPT-06-01); 250 staff sessions, 1 m opportunities, 100 k actions/day (OPT-06-02/03) | Resolved — Part 9.5 (DEC-161) |
| CONFLICT-484 | 8.3a §8.3.3.3 | Response P1 15 min, P2 1 h, P3 next business day (document 34) | Resolved — Part 9.5 (DEC-209) |
| CONFLICT-485 | 8.3a §8.3.3.3 | Plans: self-service, managed, enterprise | Resolved — Part 9.5 (DEC-210) |
| CONFLICT-486 | 8.3a §8.3.1.5 | 20 weighted dimensions (documents 36 and 38); assignment brief says 21 | Resolved — Part 9.5 (DEC-207) |
| CONFLICT-487 | 8.3a §8.3.4.1 | 76 business requirements (71 retained + 5 added) | Resolved — Part 9.5 (DEC-180) |
| CONFLICT-488 | 8.3a §8.3.4.1 | Gross effort 349 / 499 / 679 PD (baseline + expansion before overlap) | Resolved — Part 9.5 (DEC-181) |
| CONFLICT-489 | 8.3a §8.3.3.3 | Pack text carries investor-product language: "owner investment data", "investment thesis", "funding goals", "formal securities offers", "four frontends and two backends", "investment-related compensation" | Resolved — Part 9.5 (DEC-179) |
| CONFLICT-490 | 8.3c §8.3.5.15.3 | Schema-valid AI outputs ≥ 99.5% with invalid/timeout counted (OKPI-13) | Resolved — Part 9.5 (DEC-195) |
| CONFLICT-491 | 8.3a §8.3.3.5 | Combined preflight 1,188 records in 6 groups (document 36) vs 1,545 in 9 groups (document 38) | Resolved — Part 9.5 (DEC-206) |
| CONFLICT-550 | 9.6b §9.6b | DEC-306 | Resolved — Part 9.5 (DEC-306) |
| CONFLICT-551 | 9.6b §9.6b | DEC-317 | Resolved — Part 9.5 (DEC-317) |
| CONFLICT-552 | 9.6b §9.6b | DEC-325 | Resolved — Part 9.5 (DEC-325) |
| CONFLICT-553 | 9.6b §9.6b | DEC-304 | Resolved — Part 9.5 (DEC-304) |
| CONFLICT-554 | 9.6b §9.6b | DEC-309 | Resolved — Part 9.5 (DEC-309) |
| CONFLICT-555 | 9.6b §9.6b | DEC-302 | Resolved — Part 9.5 (DEC-302) |
| CONFLICT-556 | 9.6b §9.6b | DEC-324 | Resolved — Part 9.5 (DEC-324) |
| CONFLICT-620 | 9.7a front matter | ADR-071 says only AG-016 plans and agents are never driven at run time; the brief asks for a supervisor over existing agents | Resolved — Part 9.5 (DEC-384) |
| CONFLICT-621 | 9.7b §9.7.15 | DEC-011 / DEC-211: one active scoring model; predictive scoring requested | Resolved — Part 9.5 (DEC-383, Part 9.7b §G summary) |
| CONFLICT-622 | 9.7a Quality gate: Batch 9.7a | Coaching and conversation analytics could become employee evaluation (EU AI Act Annex III, verify) | Resolved — Part 9.5 (DEC-386) |
| CONFLICT-623 | 9.7b §9.7.17 | B02 high scenario already ≈ 101% of ₹3,000 (Part 7.4b) while new agents are requested | Resolved — Part 9.5 (DEC-382) |
| CONFLICT-657 | 9.8b §9.8.14 | SP-12 specifies first/last-touch attribution with window and unknown bucket; AU-040 defaults to last non-direct; X2 adds multi-touch | Resolved — Part 9.5 (DEC-397) |
| CONFLICT-658 | 9.8b §9.8.14 | Part 4.1 TR-R1 states no SMS or voice outreach in W0–W5; X2 proposes call steps | Resolved — Part 9.5 (DEC-392) |
| CONFLICT-659 | 9.8b §9.8.16 | PP-01 "outcomes over activity" vs gamification practices that reward activity | Resolved — Part 9.5 (DEC-398) |
| CONFLICT-720 | 9.9a §9.9.2 | Request for "Indic multilingual UI" vs DEC-026 Admin en-IN only | Resolved — Part 9.5 (DEC-404) |
| CONFLICT-721 | 9.9a §9.9.2 | Developer platform vs Part 3.2 "outbound webhooks not offered in W0–W6" | Resolved — Part 9.5 (DEC-403) |
| CONFLICT-722 | 9.9b §9.9.14 | "Real-time event streaming" vs ADR-003 rejection of CDC/Kafka | Resolved — Part 9.5 (DEC-401) |
| CONFLICT-723 | 9.9a §9.9.5.3 | "Reverse ETL" vs ADR-011 first-party analytics only | Resolved — Part 0A §G (Part 9.9b §G summary) |
| CONFLICT-724 | 9.9a §9.9.5.21 | New FinOps screen/tables vs doc 36 §5 "use existing Admin interfaces; no new physical table or API count assumed" | Resolved — Part 9.5 (DEC-400) |
| CONFLICT-725 | 9.9b §9.9.16.1 | Chaos engineering vs zero external side effects and fail-closed | Resolved — Part 0A §G (Part 9.9b §G summary) |
| CONFLICT-726 | 9.9b §9.9.14 | Auto-remediation vs L1 cap on consequential actions | Resolved — Part 9.5 (DEC-407) |

<!-- GEN:CONFLICT:END -->

### 9.2.4(d) RECOMMENDATION register (with status)

"Accepted" = accepted by a DEC row, by the Part 0A §G summary ("RECOMMENDATION-001…018 all accepted"), or by its own register row. "Proposed" = awaiting the owner named in the issuing part; the Part 10 assembly asks the Product Owner to accept or reject each one.

<!-- GEN:RECOMMENDATION:BEGIN -->

| ID | First seen | Recommendation (statement) | Status |
|---|---|---|---|
| RECOMMENDATION-001 | 0 §0.3.3 | Adopt WCAG 2.2 AA as the accessibility standard for Website, Portal and Admin; automated axe checks in CI plus manual screen-reader passes | Accepted (DEC-098, DEC-149) |
| RECOMMENDATION-002 | 0 §0.4 | Initial SLOs: Website/Portal availability 99.5% (pilot) → 99.9% (scale gate); Admin 99.5%; p95 API read ≤ 500 ms, write ≤ 800 ms (excluding provider calls); RPO ≤ 15 min (PITR), RTO ≤ 4 h; outbox dispatch lag p95 ≤ 60 s (consistent with … | Accepted (DEC-018, DEC-149) |
| RECOMMENDATION-003 | 0 §0.5 | Allow a lighter Claude tier (e.g. Haiku-class) for high-volume classification/extraction where evals show parity. Deviates from "Sonnet only", consistent with FRD OPT-10-01 | Accepted (DEC-007, DEC-149) |
| RECOMMENDATION-004 | 0 §0.8 | Data classification scheme (Public, Internal, Confidential, Restricted). Restricted = personal data, children's data, health-adjacent, financial, credentials. Restricted data never goes to free-tier models; redact or block | Accepted (DEC-149) |
| RECOMMENDATION-005 | 0 §0.8 | Feature flags (open-source, e.g. django-waffle or Unleash OSS) for every external channel, autonomy mode and paid adapter; flags default OFF | Accepted (DEC-149) |
| RECOMMENDATION-006 | 0 §0.8 | OpenTelemetry traces/metrics with a correlation ID propagated from HTTP → outbox → Celery → adapter → webhook | Accepted (DEC-149) |
| RECOMMENDATION-007 | 0 §0.8 | STRIDE threat model plus DPIAs (Data Protection Impact Assessments) for EduVerse (children) and MedMaarg (health-adjacent) flows before activation | Accepted (DEC-149) |
| RECOMMENDATION-008 | 0 §0.8 | Define the Admin Copilot as a read-only, grounded assistant (L0/L1) that answers from scoped records and approved knowledge with citations and can draft but never execute | Accepted (DEC-035, DEC-149) |
| RECOMMENDATION-009 | 0 §0.4 | Scoped global search (PostgreSQL full-text + trigram) across organizations, contacts, deals, documents, with RLS enforced | Accepted (DEC-149) |
| RECOMMENDATION-010 | 0 §0.8 | Infrastructure as Code (Terraform/OpenTofu) and immutable container images; environments dev → test → staging → prod | Accepted (DEC-149) |
| RECOMMENDATION-011 | 0 §0.8 | Consumer-driven / schema contract tests for every provider adapter and webhook, with sandbox fixtures | Accepted (DEC-149) |
| RECOMMENDATION-012 | 0 §0.8 | A single Policy Decision Point service (deterministic) for eligibility, consent, jurisdiction, quiet hours, frequency caps, budget and approval-hash checks, called at plan time *and* at dispatch | Accepted (DEC-149) |
| RECOMMENDATION-013 | 0 §0.5 | Merge duplicated acceptance procedures (BRD §15/§16, FRD §14/§15) into one acceptance register | Accepted (DEC-149) |
| RECOMMENDATION-014 | 0 §0.3.1 | Create FR-W31…FR-W34 and FR-A109…FR-A113 with full acceptance, matching the SM-FR pattern | Accepted (DEC-149) |
| RECOMMENDATION-015 | 0 §0.8 | A Reconciliation console pattern (uncertain outcomes queue) shared by email, WhatsApp, social, ads, e-sign, payments | Accepted (DEC-149) |
| RECOMMENDATION-016 | 0 §0.8 | A Jurisdiction rule pack in the eligibility engine (India DPDP/TRAI, EU GDPR/PECR, US CAN-SPAM, Canada CASL); unknown jurisdiction = deny | Accepted (DEC-029, DEC-149) |
| RECOMMENDATION-017 | 0 §0.8 | Seed synthetic data sets (two tenants, 26 startups, all four verticals, minors and health fixtures) as a versioned test asset | Accepted (DEC-149) |
| RECOMMENDATION-018 | 0 §0.8 | Use the dual-ledger pattern: receivables and payables as separate append-only ledgers; deal/closure states derived, never manually set | Accepted (DEC-149) |
| RECOMMENDATION-019 | 1 §1.4.2 | KPI-03 · Verified contact rate · contacts with verified professional channel ÷ contacts discovered · Baseline in W1; +10 pp by W5 RECOMMENDATION-019 · Monthly · Research lead · A025 | Accepted (DEC-149) |
| RECOMMENDATION-020 | 2.3 §2.25.6 | BRL-APR-09 · Delegation · Approvers may delegate for ≤ 14 days to a user with an equal or higher role in the same scope; audited · None · SVC · Policy | Accepted (DEC-149) |
| RECOMMENDATION-021 | 2.3 §2.26.1 | R15 · Auditor (read-only) · n/a · Admin · Tenant read-only, incl. audit · RECOMMENDATION-021 For internal audit and legal review | Accepted (DEC-149) |
| RECOMMENDATION-022 | 2.4 §2.31.4 | Attribution models offered · First-touch, last non-direct touch (default), linear, position-based (40/20/40) · M52 "attribution caveat"; default chosen for simplicity and explainability RECOMMENDATION-022 | Accepted (DEC-149) |
| RECOMMENDATION-023 | 2.4 §2.33.5 | User lifecycle: invite, activate, change role, expire, revoke, access review (quarterly attestation) RECOMMENDATION-023 · A002 | Accepted (DEC-149) |
| RECOMMENDATION-024 | 2.4 §2.34.2 | prev_hash, hash · Hash chain per tenant for tamper evidence RECOMMENDATION-024 | Accepted (DEC-149) |
| RECOMMENDATION-025 | 2.4 §2.35.2 | Application · DRF permission classes + object-level checks; scoped querysets by default (no unscoped manager in business code) · Static check: unscoped query usage fails CI RECOMMENDATION-025 | Accepted (DEC-149) |
| RECOMMENDATION-026 | 2.4 §2.36.2 | I18N-04 · Numbers formatted per locale; en-IN uses Indian digit grouping (1,00,000) with an option for international grouping in Admin; lakh/crore labels in INR summaries RECOMMENDATION-026 | Accepted (DEC-149) |
| RECOMMENDATION-027 | 2.5 §2.45.1 | Dark mode · Admin: supported via tokens; Website: per startup theme option RECOMMENDATION-027 | Accepted (DEC-149) |
| RECOMMENDATION-028 | 2.5 §2.48 | Performance budgets (public): LCP ≤ 2.5 s (p75, mid-range mobile on 4G), INP ≤ 200 ms, CLS ≤ 0.1; JS ≤ 150 KB gzip per public route RECOMMENDATION-028. | Accepted (DEC-149) |
| RECOMMENDATION-029 | 3.1 front matter | Atomic publication pointer via PostgreSQL (authoritative) mirrored to CloudFront KeyValueStore with immutable revision prefixes and prerendered pages | Accepted (DEC-149) |
| RECOMMENDATION-030 | 3.1 §3.1.1.1 | Single-instance ECS-on-EC2 pilot behind CloudFront without ALB or NAT gateway | Accepted (DEC-149) |
| RECOMMENDATION-031 | 3.1 §3.1.16 | Timeouts, retry policy by failure class, circuit breaker and bulkhead parameters | Accepted (DEC-149) |
| RECOMMENDATION-032 | 3.2 §3.2.1.7 | Extended rate-limit classes (auth, chat, portal, heavy Admin, webhooks, internal) keeping Part 2.4 defaults | Accepted (DEC-149) |
| RECOMMENDATION-033 | 3.1 ADR-020 Event schema versioning | CloudEvents-aligned event envelope with schema registry, major/minor versioning and dual publishing | Accepted (DEC-149) |
| RECOMMENDATION-034 | 3.2 §3.2.5 | Fourteen-layer contract testing approach (CT-01…CT-14) | Accepted (DEC-149) |
| RECOMMENDATION-035 | 3.1 §3.1.6.2 | Managed malware scanning of uploads (GuardDuty Malware Protection for S3) at pilot (defined in Part 3.2) | Accepted (DEC-149) |
| RECOMMENDATION-036 | 3.2 §3.2.1.2 | UUIDv7 primary keys generated in the application; never expose raw IDs as capabilities; 256-bit random tokens stored as hashes for every shared link | Accepted (DEC-149) |
| RECOMMENDATION-037 | 3.2 §3.2.8.1 | RLS with transaction-local session variables, FORCE ROW LEVEL SECURITY, a separate write-scope variable that enforces portfolio read-only in the database, no BYPASSRLS roles, and a CI guard | Accepted (DEC-149) |
| RECOMMENDATION-038 | 3.1 §3.1.6.1 | Field-level envelope encryption with per-tenant KMS keys, HMAC blind indexes for lookup/suppression, crypto-shredding at offboarding | Accepted (DEC-149) |
| RECOMMENDATION-039 | 3.3 §3.3.6.3 | halfvec(1024) embeddings with HNSW (m 16, ef_construction 64), iterative filtered scans, hybrid retrieval; IVFFlat rejected | Accepted (DEC-149) |
| RECOMMENDATION-040 | 4.1 front matter | Admin SPA budgets (NFR-044), search p95 ≤ 1 s (NFR-046), chat session caps (NFR-022), AI gateway overhead and first-token targets (NFR-052) where the baseline had none | Accepted (DEC-149) |
| RECOMMENDATION-041 | 4.1 §4.16.3 | Vulnerability remediation SLAs (Critical 7 d, High 30 d, Medium 90 d) | Accepted (DEC-149) |
| RECOMMENDATION-042 | 4.1 §4.5.3 | Field-level envelope encryption with blind indexes for Restricted fields | Accepted (DEC-149) |
| RECOMMENDATION-043 | 4.1 §4.3.3 | MFA required for every user holding Restricted-data clearance (ABAC-05) from W2, not only privileged roles | Accepted (DEC-149) |
| RECOMMENDATION-044 | 4.1 §4.1.5 | Allowlisting egress proxy for workers and an SSRF-hardened fetcher pool | Accepted (DEC-149) |
| RECOMMENDATION-045 | 4.2 §4.21 | Release strategy: weekly trains, deploy windows inside support hours, rolling → blue/green, expand/contract migrations, monthly rollback rehearsal | Accepted (DEC-149) |
| RECOMMENDATION-046 | 4.2 §4.23.8 | Track DORA metrics with targets (NFR-083) | Accepted (DEC-149) |
| RECOMMENDATION-047 | 4.3 §4.36.1 | Feature-flag tooling and lifecycle (classes, defaults OFF, ≤ 90-day release flags, audited changes) | Accepted (DEC-149) |
| RECOMMENDATION-048 | 4.1 §4.5.1 | External security hygiene: MTA-STS and TLS-RPT for sending domains, security.txt, vulnerability disclosure policy; bug bounty considered at W6 | Accepted (DEC-149) |
| RECOMMENDATION-049 | 4.1 TB-08 Model gateway | AI red-team cadence per wave gate and canary strings to detect system-prompt and cross-tenant leakage | Accepted (DEC-149) |
| RECOMMENDATION-050 | 5.1a front matter | Split the W0 gate into W0-A (Day 15: identity, RLS, outbox, consent, PDP, gateway, cost cap, seed data, CI/IaC, flags) and W0-B (Day 30: remaining W0 stories, owner and claims sign-off) | Accepted (DEC-149) |
| RECOMMENDATION-051 | 5.1a §5.7.3 | Scenario tag convention (@happy/@alt/@neg/@val/@perm/@edge, @sec/@a11y/@obs, rule and DM tags) | Accepted (DEC-149) |
| RECOMMENDATION-052 | 5.1b US-0208 Import of seed catalogues and pr | One shared import engine (versioned templates, dry run, consent gating, async jobs) built in W1 and reused by EP-20 | Accepted (DEC-149) |
| RECOMMENDATION-053 | 5.1a §5.6.2 | Table-driven RBAC test generated from Part 2.3 §2.26.3 (42 × 15 + 10 × 4 = 670 cells) | Accepted (DEC-149) |
| RECOMMENDATION-054 | 5.2 US-0804 Amazon SES email adapter and ema | Shared provider-adapter contract-test kit: consumer-driven contract tests with recorded sandbox fixtures, normalised outcome classes and a nightly sandbox smoke run, used by SES, WhatsApp, Google Calendar, social, ads and e-sign adapters | Accepted (DEC-149) |
| RECOMMENDATION-055 | 5.2 US-1303 Decimal pricing library with exh | Property-based tests (e.g. Hypothesis) over the Decimal pricing library asserting invariants (no float, total = Σ rounded lines + tax, deterministic recompute) plus a lint rule forbidding float in money paths | Accepted (DEC-149) |
| RECOMMENDATION-056 | 5.2 US-0811 Quiet-hours and frequency-cap en | Eligibility "explain" API returning rule IDs and next eligible time, reused by A034 BlockedReason, A039 simulation and A058 exclusion counts | Accepted (DEC-149) |
| RECOMMENDATION-057 | 5.3 front matter | Closure-integrity invariant job (nightly plus event-driven): any WonContracted/Paid deal without policy evidence raises a Critical alert and enters the A089 exception queue, keeping KPI-31 at 0 | Accepted (DEC-149) |
| RECOMMENDATION-058 | 5.3 US-1902 Immutable publication snapshots, | Publication purge target: p95 ≤ 5 minutes from publish or rollback to all CDN edges, verified by a post-publish synthetic fetch | Accepted (DEC-149) |
| RECOMMENDATION-059 | 5.3 US-2106 Production release readiness and | Error-budget release policy: when a production SLO's monthly error budget is exhausted, A090 blocks non-fix releases unless the Founder records an exception | Accepted (DEC-149) |
| RECOMMENDATION-060 | 7.1 front matter | Haiku-first routing with per-agent eval parity and measured escalation shares | Accepted (DEC-149) |
| RECOMMENDATION-061 | 6.4 §6.4.1.1 | Delivery-lifecycle API usage (CI review, eval judge, fixture generation) gets its own delivery AI reserve under C03 rather than consuming B02 | Accepted (DEC-149) |
| RECOMMENDATION-062 | 7.2 §7.2.6 | Keep LLM traces in gateway tables + OpenTelemetry in pilot; adopt Langfuse self-hosted at growth gate; B22 stays ₹0 in pilot | Accepted (DEC-149) |
| RECOMMENDATION-063 | 6.4 AU-004 Data classification & PII redacti | Presidio with Indian recognizers (PAN, Aadhaar patterns, Indian phone formats, Indic names) for AU-004 | Accepted (DEC-149) |
| RECOMMENDATION-064 | 6.4 AU-042 Usage metering & entitlement enfo | Define "AI task" as one completed agent invocation returning a validated output (§7.5.4) | Accepted (DEC-149) |
| RECOMMENDATION-065 | 7.3 §7.3.3 | First Tier 2 opt-in limited to Owner Portfolio, agents AG-003/004/005/017, after legal review | Accepted (DEC-149) |
| RECOMMENDATION-066 | 7.3 §7.4.2 | Weekly 30-minute AI cost and quality review (RP-20, RP-21) owned by the FinOps lead | Accepted (DEC-149) |
| RECOMMENDATION-067 | 7.3 §7.3.3 | W6 spike: self-hosted small open model (vLLM in ap-south-1) as Tier 2e for classifiers; evaluate cost vs Haiku | Accepted (DEC-149, DEC-301) |
| RECOMMENDATION-068 | 6.4 §6.4.9.2 | AI incident severity scheme AI-S1…S3 (§7.6.10) | Accepted (DEC-149) |
| RECOMMENDATION-069 | 6.4 AG-018 Content & Campaign Studio Drafter | Configurable AI-content labelling per jurisdiction (EU AI Act Art. 50; India IT Rules amendments if adopted) | Accepted (DEC-149) |
| RECOMMENDATION-070 | 6.1 front matter | Test pyramid target proportions (unit 60–70%, integration 15–25%, contract 4–6%, system 5–8%, E2E 2–4%) and coverage targets per layer, including mutation score ≥ 85% for money, tax, ledger and PDP modules, ≥ 80% for scoring and ≥ 75% for … | Accepted (DEC-149) |
| RECOMMENDATION-071 | 6.1 §6.1.6.3 | A test-only provider simulator with scriptable fault modes (timeout-after-submit, duplicate and out-of-order webhooks, signature failures, throttling) contract-tested against recorded sandbox fixtures, plus a clock control facility … | Accepted (DEC-149) |
| RECOMMENDATION-072 | 6.1 §6.1.5.4 | Evidence record (EVR) schema implementing the BRD §12.2 fields, and the certification ladder L-S → L-T → L-C → L-P so that A090 can fail closed and no synthetic result is shown as production certification | Accepted (DEC-149) |
| RECOMMENDATION-073 | 6.1 §6.1.3.1 | Independent external penetration test before the first real controlled pilot (W4) and before the first external tenant (W5), then annually; OWASP ASVS Level 2 and WSTG as checklists (verify current versions and cost) | Accepted (DEC-149) |
| RECOMMENDATION-074 | 6.1 §6.1.5.3 | Defect fix SLAs by severity aligned with DEC-044 support hours, the hotfix evidence path, and the flaky-test policy (no auto-retry in gating jobs, 2% quarantine cap, P0 tests never quarantined, 10-day fix limit) | Accepted (DEC-149) |
| RECOMMENDATION-075 | 6.2a front matter | One adapter conformance battery (checks B1–B7: outcome normalisation, idempotent submit, uncertain path, signed webhook, secret hygiene, environment guard, disabled-by-default) run as a single parameterized suite for SES, WhatsApp, Google … | Accepted (DEC-149) |
| RECOMMENDATION-076 | 6.2a §6.2.1.7 | E2E journey register for EP-08…EP-14 (J-08-01…J-14-02), each journey one Playwright TC with axe scans; ★ journeys proposed for the wave's manual top-20 accessibility audit (Part 2.5 §2.46) | Accepted (DEC-149) |
| RECOMMENDATION-077 | 6.3a front matter | Run a closure-integrity oracle as an after-each hook in every EP-15 integration and system test and in the AP-04 run: KPI-31 = 0, Σ receivable ledger entries = Σ allocations per invoice, Σ allocations ≤ invoice total, no deal in … | Accepted (DEC-149) |
| RECOMMENDATION-078 | 6.3a §6.3.7.1 | Every drill (restore DR-1…DR-9, rollback rehearsal, emergency-stop latency, provider outage) emits a machine-readable drill report (JSON: drill ID, release, digest, injected-failure time, last surviving heartbeat, declared and recovered … | Accepted (DEC-149) |
| RECOMMENDATION-079 | 6.4 front matter | Two-tier safety gate with violation classes. Classify every red-team and adversarial result as V1–V7; V1–V6 (external effect, cross-scope disclosure, Restricted to Tier 2, prohibited content to a person, prompt/canary leak, injected state … | Accepted (DEC-109, DEC-149) |
| RECOMMENDATION-080 | 6.5 front matter | Run build_rtm.py (extended to read the pytest/Playwright tc/req markers and EVR results) as a CI artefact on G3 and G4; fail G4 when any in-scope FR, AC or P0 BRL is *Not covered* or has no passing TC, and publish the CSV to the A090 test … | Accepted (DEC-149) |
| RECOMMENDATION-081 | 8.1 front matter | Adopt the re-baselined wave calendar (§8.1.2.2): keep errata 34 gates; Release 1 go/no-go Day 152, Release 2 build go/no-go Day 180, W5 exit ≈ Day 201; activate each capability as soon as it passes (continuous delivery, DEC-006); flag … | Accepted (DEC-149) |
| RECOMMENDATION-082 | 8.1 §8.1.4.2 | Raise QA to 1.0 FTE from Sprint 3 to the end of Release 2 hypercare (+₹2.75–4.13 L) | Accepted (DEC-149) |
| RECOMMENDATION-083 | 8.1 §8.1.4.2 | Front-load DevOps/SRE to 1.0 FTE in Sprints 0–1 (+₹0.6–0.9 L) | Accepted (DEC-149) |
| RECOMMENDATION-084 | 8.1 §8.1.5.1 | Fractional UX contractor, 1 day/week in S2–S9 (≈ 16 days, ₹0.87–1.31 L) | Accepted (DEC-149) |
| RECOMMENDATION-085 | 8.1 §8.1.4.7 | Pre-approve the tier 1 spill list (41.0 SP) as W6 backlog and the tier 2 list as the next contingency, in the order shown | Accepted (DEC-149) |
| RECOMMENDATION-086 | 8.1 §8.1.2.1 | Option E acceleration (two contract engineers S2–S6, ₹5.5–8.3 L) only if Release 1 is needed near Day 124 | Accepted (DEC-149) |
| RECOMMENDATION-087 | 8.1 §8.1.4.3 | Run a procurement track from Sprint 0 (SES, Anthropic terms, WABA, OAuth, merchant, e-sign, pen-test vendor, CloudFront quotas) with owners and dates (§8.1.7.3) | Accepted (DEC-149) |
| RECOMMENDATION-088 | 8.2 §8.2.2.4 | Change control with an impact record (journey, UI, API, persistence, cost, tests), Minor/Major/Emergency classes, a weekly CCB and release scope freezes (S8, S11) | Accepted (DEC-149) |
| RECOMMENDATION-089 | 8.2 §8.2.5 | Hypercare windows (2 weeks per activation, 4 weeks per release), daily metrics and exit criteria; adoption metrics with a training gate before send/approve/publish rights | Accepted (DEC-149) |
| RECOMMENDATION-090 | 6.6 front matter | Recommendation (Batch 6.7) | Accepted (DEC-149) |
| RECOMMENDATION-300 | 2.6 front matter | Persona variants (P03a, P03b, P03c, P07a, P07b, P10a, P13a, P13b, P14e, website roles) and new personas P17–P20 | Accepted (DEC-221) |
| RECOMMENDATION-301 | 2.6 §2.6.5.3.2 | New role R21 and sub-roles R11T, R12I with ABAC-ENH-A-01…05 | Accepted (DEC-221) |
| RECOMMENDATION-302 | 2.6 Document 11 Global Market Intelligence & | Source-family and segment playbook registry SPB-01…24 | Accepted (DEC-221) |
| RECOMMENDATION-303 | 2.6 §2.6.5.1.5 | Coverage ledger and KPI-ENH-A-01 with weekly ≥ 90% target once stable | Accepted (DEC-221) |
| RECOMMENDATION-304 | 2.6 §2.6.5.2.4 | Paid data provider enabled only with ≥ 20% better cost per usable opportunity or incremental eligible records on the same corpus | Accepted (DEC-221) |
| RECOMMENDATION-305 | 2.6 Document 14 Global Customer, Partner & A | Acquisition operating plan AOP-01…05 and weekly acquisition review | Accepted (DEC-221) |
| RECOMMENDATION-306 | 2.6 Document 12 Digital Marketing & Customer | Experiment registry with single-variable rule and stop triggers | Accepted (DEC-221) |
| RECOMMENDATION-307 | 2.6 §2.6.5.1.5 | Outcome economics report and KPI-ENH-A-03 | Accepted (DEC-221) |
| RECOMMENDATION-308 | 2.6 §2.6.8.4 | Jurisdiction activation decision record | Accepted (DEC-221) |
| RECOMMENDATION-309 | 2.6 Document 13 Sales Intelligence & Commerc | Relationship ID and derived relationship stage | Accepted (DEC-221) |
| RECOMMENDATION-310 | 2.6 Document 37 Sales & Marketing Automation | UAT packs and demonstration script from document 37 | Accepted (DEC-221) |
| RECOMMENDATION-311 | 2.6 Document 03 End User Personas | Training and competence record that never grants authority | Accepted (DEC-221) |
| RECOMMENDATION-312 | 2.6 Document 11 Global Market Intelligence & | Integration candidate disposition table | Accepted (DEC-221) |
| RECOMMENDATION-313 | 2.6 Document 03 End User Personas | Acceptance RACI and AP-ENH-A-01…12 | Accepted (DEC-221) |
| RECOMMENDATION-314 | 2.6 Document 03 End User Personas | User-productivity measurement protocol | Accepted (DEC-221) |
| RECOMMENDATION-315 | 2.6 Document 03 End User Personas | Bulk action preview with hash | Accepted (DEC-221) |
| RECOMMENDATION-320 | 3.4 front matter | Validate the pack's capacity matrix with LT-ENH-B-01…04; buy no capacity before a §3.1.6.4 trigger | Accepted (DEC-221) |
| RECOMMENDATION-321 | 3.4 Document(s) 04/09/10 | Adopt recovery classes RC-1…RC-3 with class-ordered restore | Accepted (DEC-221) |
| RECOMMENDATION-322 | 3.4 §A | Adopt agent envelope v1.1 | Accepted (DEC-221) |
| RECOMMENDATION-323 | 3.4 §D | Adopt the product-event ingress allowlist, off by default | Accepted (DEC-221) |
| RECOMMENDATION-324 | 3.4 §E | Build the commercial journey projection as a read model | Accepted (DEC-221) |
| RECOMMENDATION-325 | 3.4 Document(s) 05 | Run the 90-cell workflow regression matrix in SIT from W2 | Accepted (DEC-221) |
| RECOMMENDATION-326 | 3.4 §D | Keep a technical-debt register with monthly review and a 10% capacity reservation for S1/S2 debt | Accepted (DEC-221) |
| RECOMMENDATION-327 | 3.4 Document(s) 04 | Enforce a benchmark record before any paid provider activation | Accepted (DEC-221) |
| RECOMMENDATION-328 | 3.4 Document(s) 04 | Use the pack's discipline shares as a capacity cross-check; skew any Option E hire to backend; schedule the dynamic-field framework before the nine expansion screens | Accepted (DEC-221) |
| RECOMMENDATION-329 | 3.4 §B | Adopt four DRF permission base classes with CI enforcement | Accepted (DEC-221) |
| RECOMMENDATION-330 | 3.4 §A | Price per-tenant KMS keys into plans or use per-tenant data keys under a shared CMK for tenants without a contractual need | Accepted (DEC-221) |
| RECOMMENDATION-331 | 3.4 §3.4.4.4 | Cite OPT IDs in the "Source" column of implementing artefacts | Accepted (DEC-221) |
| RECOMMENDATION-340 | 2.7a front matter | Legacy alias routing layer (single canonical handler, Deprecation/Link headers, alias table) | Accepted (DEC-221) |
| RECOMMENDATION-341 | 2.7a §2.7.8 | Generate a machine-readable field-contract registry (YAML per screen) from Batch 2.7b to drive FormSchemaRenderer, serializers and tests | Accepted (DEC-221) |
| RECOMMENDATION-342 | 2.7a §2.7.6 | Viewport test matrix 360/768/1280/1440 plus 320 reflow | Accepted (DEC-221) |
| RECOMMENDATION-343 | 2.7a §2.7.3.1 | AdapterCard component (licence, capacity, residual cost, benchmark, fallback approval) reused in A008, A011, A012, A033, A102 | Accepted (DEC-221) |
| RECOMMENDATION-344 | 2.7a §2.7.5.2 | Add the Unassessed UI state | Accepted (DEC-221) |
| RECOMMENDATION-345 | 2.7a §2.7.8 | "Related" menu component carrying scope and record ID | Accepted (DEC-221) |
| RECOMMENDATION-346 | 2.7a §2.7.8 | Design evidence pack per wave stored as EVR evidence | Accepted (DEC-221) |
| RECOMMENDATION-347 | 2.7a §2.7.3.2 | Productivity benchmark protocol (baseline vs candidate, named user, no safeguard reduction) | Accepted (DEC-221) |
| RECOMMENDATION-348 | 2.7a §2.7.3.1 | Projection freshness tiers O (≤ 60 s) and A (≤ 15 min) | Accepted (DEC-221) |
| RECOMMENDATION-349 | 2.7a §2.7.5.8 | Build-class weighting for screen-level estimation | Accepted (DEC-221) |
| RECOMMENDATION-360 | 3.5a front matter | OpenAPI x-source-op, x-source-path, x-sit-id, x-contract-state on every operation | Accepted (DEC-221) |
| RECOMMENDATION-361 | 3.5b §3.5.5.3 | Use §3.5.5.3 as the review oracle for serializer-generated OpenAPI (contract-first review, code-first generation) | Accepted (DEC-221) |
| RECOMMENDATION-362 | 3.5b §3.5.5.12.1 | Negative fixture families N01…N22 bound to SE classes | Accepted (DEC-221) |
| RECOMMENDATION-363 | 3.5a §3.5.3.1 | AdapterCommand/AdapterResult envelope | Accepted (DEC-221) |
| RECOMMENDATION-364 | 3.5b §3.5.5.9.1 | Operation contract state machine with route flags and three-lead approval | Accepted (DEC-221) |
| RECOMMENDATION-365 | 3.5a §3.5.3.1 | Provider/tool register with four classes; developer plugins and unapproved SaaS never runtime | Accepted (DEC-221) |
| RECOMMENDATION-366 | 3.5a §3.5.3.1 | Website ingress allowlist generated from the catalogue | Accepted (DEC-221) |
| RECOMMENDATION-367 | 3.5b §3.5.5.9.4 | Catalogue-integrity CI gate CI-1…CI-8 | Accepted (DEC-221) |
| RECOMMENDATION-368 | 3.5a §3.5.3.1 | PubMed as an optional, off-by-default evidence source for MedMaarg claims behind SearchPort, with SourcePolicy | Accepted (DEC-221) |
| RECOMMENDATION-369 | 3.5a §3.5.3.1 | Exclude reverse-IP visitor identification and third-party analytics on public pages; keep the first-party beacon | Accepted (DEC-221) |
| RECOMMENDATION-370 | 3.5b §3.5.5.1 | Four new error codes | Accepted (DEC-221, DEC-217) |
| RECOMMENDATION-371 | 3.5b §3.5.5.10 | Per-operation performance budgets (x-perf) with query-count limits | Accepted (DEC-221) |
| RECOMMENDATION-380 | 3.6a front matter | Section numbering · 3.6.x (this batch); tags ASSUMPTION/GAP/CONFLICT/RECOMMENDATION-380…399 only | Accepted (DEC-221) |
| RECOMMENDATION-398 | 3.6a §3.6.3 | Governance package: two-axis classification, adapter persistence AP-1…6, OPT trace, DCE, backfill quarantine | Accepted (DEC-221) |
| RECOMMENDATION-399 | 3.6a §3.6.3 | Logical backup checksum manifest and restore-credential check; secret-reference table restricted to R01/R13 with audited reads | Accepted (DEC-221, DEC-191) |
| RECOMMENDATION-400 | 7.4a front matter | Adopt AI result envelope v2 | Accepted (DEC-221) |
| RECOMMENDATION-401 | 7.4b §7.4.5.1 | Register PC-01…PC-18 prompt contracts with a common minimum output | Accepted (DEC-221) |
| RECOMMENDATION-402 | 7.4b §7.4.5.3 | Authorization-safe private cache key | Accepted (DEC-221) |
| RECOMMENDATION-403 | 7.4b §7.4.5.2 | Two-sided RAG ACL and AU-046 revocation propagation | Accepted (DEC-221) |
| RECOMMENDATION-404 | 7.4b §7.4.5.8.1 | Integration candidate register and PG-01…PG-10 procurement gate (AU-044) | Accepted (DEC-221) |
| RECOMMENDATION-405 | 7.4a §7.4.3 | Four-method adapter port, denied class, lifecycle with Retire; add Documenso to the e-sign evaluation shortlist after licence/evidentiary review | Accepted (DEC-221) |
| RECOMMENDATION-406 | 7.4a §7.4.3 | Replacement economics metrics with quarterly re-evaluation | Accepted (DEC-221) |
| RECOMMENDATION-407 | 7.4b §7.4.8 | Matched-sample benchmark harness AU-045 as the only path to PG-05 | Accepted (DEC-221) |
| RECOMMENDATION-408 | 7.4b §7.4.8 | Licence register with model weights and CI gate AU-047 | Accepted (DEC-221) |
| RECOMMENDATION-409 | 7.4b §7.4.8 | Provider invoice reconciliation AU-048 | Accepted (DEC-221) |
| RECOMMENDATION-410 | 7.4b §7.4.8 | Tenant contribution margin AU-049 | Accepted (DEC-221) |
| RECOMMENDATION-411 | 7.4b §7.4.5.7 | Seed A113 with the 100/20/13 library | Accepted (DEC-221) |
| RECOMMENDATION-412 | 7.4a §7.4.3 | Add AG-037 and AG-038 (Release 2) and place them on ladder steps 3 and 2 | Accepted (DEC-221) |
| RECOMMENDATION-413 | 7.4b §7.4.8 | Wire OKPI-08…16, 21, 24, 35 into A012/RP-20 with n and undefined handling | Accepted (DEC-221) |
| RECOMMENDATION-414 | 7.4a §7.4.3 | Budget per surface with a public-AI cap | Accepted (DEC-221) |
| RECOMMENDATION-415 | 7.4a §7.4.4.4 | Charge benchmark trial spend to B10 with a per-candidate cap | Accepted (DEC-221) |
| RECOMMENDATION-416 | 7.4b §7.4.5.10 | Add the budget views of §7.4.5.10 to Part 8.2 | Accepted (DEC-221) |
| RECOMMENDATION-420 | 6.8a front matter | Generate the operation-class data rows from the OpenAPI documents so new operations get a class row automatically (CT-05/CT-03 with IDs) | Accepted (DEC-221) |
| RECOMMENDATION-421 | 6.8c §6.8.5.1.6 | Adopt UAT-PK-MKT and UAT-PK-CS | Accepted (DEC-221) |
| RECOMMENDATION-422 | 6.8a §6.8.3.2 | Add execution_status to the EVR | Accepted (DEC-221) |
| RECOMMENDATION-423 | 6.8a front matter | Extend DEC-017 aliases to all SM-* source families | Accepted (DEC-221) |
| RECOMMENDATION-424 | 6.8a §6.8.3.1 | Import the source's 164 candidate request and 165 response examples as OpenAPI examples once DTOs are approved (CT-04) | Accepted (DEC-221) |
| RECOMMENDATION-425 | 6.8c §6.8.5.1.5 | build_rtm.py reads final/coverage/G_test_mapping.csv into the Aliases column | Accepted (DEC-221) |
| RECOMMENDATION-440 | 6.9b front matter | Adopt the QC register and layer sign-off as A090 inputs | Accepted (DEC-221) |
| RECOMMENDATION-441 | 6.9b §6.9.5.2 | Use the SPDEC alias and decision queue | Accepted (DEC-221) |
| RECOMMENDATION-442 | 6.9b §6.9.5.1.4 | Run the fail-closed validator in PL-17 / G4 with exit-code contract 0/1/2 | Accepted (DEC-221) |
| RECOMMENDATION-443 | 6.9b §6.9.5.1.5 | Link tests to QCs by qc("QC-###") markers and extend build_rtm.py with qc_ids, sit_aliases, decision_ids | Accepted (DEC-221) |
| RECOMMENDATION-444 | 6.9a §6.9.3.2 | Add 1440 px to the viewport matrix | Accepted (DEC-221) |
| RECOMMENDATION-445 | 6.9a §6.9.3.2 | Semgrep rule: no external I/O inside transaction.atomic | Accepted (DEC-221) |
| RECOMMENDATION-446 | 6.9a §6.9.3.2 | Fixture GSE-SYN-X10 (26 owned + 10 × 2 client startups, 20 runs) | Accepted (DEC-221) |
| RECOMMENDATION-447 | 6.9a §6.9.3.2 | Full route keyboard sweep and one accessible-error UAT step per interface | Accepted (DEC-221) |
| RECOMMENDATION-448 | 6.9b §6.9.5.4.1 | Log actual PD per work item weekly; report estimate vs actual | Accepted (DEC-221) |
| RECOMMENDATION-449 | 6.9b §6.9.5.1.6 | Same-workload benchmark protocol for non-AI replacements with TCO formula | Accepted (DEC-221) |
| RECOMMENDATION-460 | 4.4a §4.4.5.1 | Adopt the coding standard §4.4.5.1 as binding with its enforcement matrix | Accepted (DEC-221) |
| RECOMMENDATION-461 | 4.4a §4.4.3.3 | Cohort canary for every external activation (DPL-ACT-02) | Accepted (DEC-221) |
| RECOMMENDATION-462 | 4.4a §4.4.3.8 | Release-gate validator RGV in PL-17 | Accepted (DEC-221) |
| RECOMMENDATION-463 | 4.4b §4.4.5.2.2 | Add control and finance queues (amend ADR-021) | Accepted (DEC-221) |
| RECOMMENDATION-464 | 4.4b §4.4.5.6.3 | Add alerts AL-50…58 and metrics MET-01…12 | Accepted (DEC-221) |
| RECOMMENDATION-465 | 4.4b §4.4.5.6.4 | Add runbooks RB-016…018 to the drill schedule | Accepted (DEC-221) |
| RECOMMENDATION-466 | 4.4b §4.4.8.1 | Adopt workload profiles WP-01…03 and LT-ENH-I-01…06 | Accepted (DEC-221) |
| RECOMMENDATION-467 | 4.4a §4.4.3.1 | Authorization-safe cache-key composition (CS-SEC-07) | Accepted (DEC-221) |
| RECOMMENDATION-468 | 4.4a §4.4.3.4 | Configuration manifest hash and drift detection | Accepted (DEC-221) |
| RECOMMENDATION-469 | 4.4b §4.4.5.7.2 | Delivery package and access handover at R1/R2 | Accepted (DEC-221) |
| RECOMMENDATION-470 | 4.4a §4.4.3.5 | Track OKPI-01…35 in the A090 release record with numeric-domain validation; 21 mandatory OKPIs feed RGV-12 | Accepted (DEC-221) |
| RECOMMENDATION-471 | 4.4b §4.4.8.1 | Penetration-test RoE and severity overlay | Accepted (DEC-221) |
| RECOMMENDATION-472 | 4.4a §4.4.3.4 | Technical-debt register with monthly review | Accepted (DEC-221) |
| RECOMMENDATION-473 | 4.4a §4.4.3.1 | Numeric guardrail library (P-08) shared by gates, optimizer and budgets | Accepted (DEC-221) |
| RECOMMENDATION-480 | 8.3c §8.3.5.15.4 | 8.3c §8.3.5.15.4 | Accepted (DEC-221) |
| RECOMMENDATION-481 | 8.3c §8.3.5.15.7 | 8.3c §8.3.5.15.7 | Accepted (DEC-221) |
| RECOMMENDATION-482 | 8.3c §8.3.5.15.9 | 8.3c FR-ENH-J-016 | Accepted (DEC-221) |
| RECOMMENDATION-483 | 8.3c §8.3.5.15.9 | 8.3c FR-ENH-J-015 | Accepted (DEC-221) |
| RECOMMENDATION-484 | 8.3b §8.3.5.8 | 8.3b §8.3.5.8 | Accepted (DEC-221) |
| RECOMMENDATION-485 | 8.3b §8.3.5.12 | 8.3b §8.3.5.12 | Accepted (DEC-221) |
| RECOMMENDATION-486 | 8.3c §8.3.5.13.1 | 8.3c §8.3.5.13.1 | Accepted (DEC-221) |
| RECOMMENDATION-487 | 8.3c §8.3.5.14.2 | 8.3c §8.3.5.14.2 | Accepted (DEC-221) |
| RECOMMENDATION-488 | 8.3c §8.3.5.14.4 | 8.3c §8.3.5.14.4 | Accepted (DEC-221) |
| RECOMMENDATION-489 | 8.3c §8.3.5.13.6 | 8.3c §8.3.5.13.6 | Accepted (DEC-221, DEC-406) |
| RECOMMENDATION-490 | 8.3c §8.3.5.13.7 | 8.3c §8.3.5.13.7 | Accepted (DEC-221) |
| RECOMMENDATION-500 | 9.5 §9.5.2.5 | Adopt Option 2b: two contract engineers from Sprint 3 to the Release 2 build gate | Accepted (no rejecting DEC; issued in Part 9.5) |
| RECOMMENDATION-501 | 9.5 §9.5.2.8 | Approve the Option 2b spend by Day 1, at the latest by the W0-A gate (Day 15) | Accepted (no rejecting DEC; issued in Part 9.5) |
| RECOMMENDATION-502 | 9.5 §9.5.2.8 | Track estimate versus actual per discipline from Sprint 0 in a sheet until B-15 is built | Accepted (no rejecting DEC; issued in Part 9.5) |
| RECOMMENDATION-503 | 9.5 §9.5.2.5 | Hire one backend/platform engineer (I, E, D, X) and one full-stack AI/test-automation engineer (F-1, G, H) | Accepted (no rejecting DEC; issued in Part 9.5) |
| RECOMMENDATION-504 | 9.5 §9.5.2.8 | Hold the UX-TASK-FIELDS residual (14.5–49.4 pd) in the management reserve and size it at the S3 review | Accepted (no rejecting DEC; issued in Part 9.5) |
| RECOMMENDATION-505 | 9.5 §9.5.2.6 | Contract a technical writer for the training content (14.5–28 pd) instead of loading the 0.5 FTE growth/compliance lead | Accepted (no rejecting DEC; issued in Part 9.5) |
| RECOMMENDATION-506 | 9.5 §9.5.2.6 | Use free uptime checks for availability probes; add CloudWatch Synthetics only if OKPI-06 evidence requires it | Accepted (no rejecting DEC; issued in Part 9.5) |
| RECOMMENDATION-507 | 9.5 §9.5.3 | Generate one consolidated enhancement backlog (package ID, story IDs, MoSCoW, release) from §9.5.2.3 into the backlog tool in Sprint 0, and merge all TC-ENH IDs into the RTM (DEC-217) | Accepted (no rejecting DEC; issued in Part 9.5) |
| RECOMMENDATION-508 | 9.5 §9.5.3 | At assembly, add a one-line pointer in each enhancement part's conflicts section to the DEC that resolved each conflict (§9.5.1.11) | Accepted (no rejecting DEC; issued in Part 9.5) |
| RECOMMENDATION-509 | 9.5 §9.5.2.8 | Keep activating capabilities as soon as their stories and Must packages pass, so the business sees value before the Release 1 gate | Accepted (no rejecting DEC; issued in Part 9.5) |
| RECOMMENDATION-520 | 9.6a §9.6a | Run the alias-registry check (TC-ALN-A-001) in CI from Sprint 0 so that aliases never become second implementations | Accepted (no rejecting DEC; issued in Part 9.6a) |
| RECOMMENDATION-521 | 9.6a §9.6a | Approve the net new Release 1 effort of this part as a separately approvable development proposal, or accept a date effect at the Sprint 3 review (DEC-226 (3)) | Accepted (no rejecting DEC; issued in Part 9.6a) |
| RECOMMENDATION-550 | 9.6b §9.6b | DEC-325 | Accepted (DEC-325) |
| RECOMMENDATION-551 | 9.6b ALN-B-14 · F21-023 · Capability 14 Obser | DEC-308 | Accepted (DEC-308) |
| RECOMMENDATION-552 | 9.6b §9.6b | DEC-319 | Accepted (DEC-319) |
| RECOMMENDATION-625 | 9.7a front matter | Supervisor plans for multi-step objectives (FR-ADV-X1-001) | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-626 | 9.7b §9.7.8 | Reuse a single cited account brief across agents (FR-ADV-X1-005) | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-627 | 9.7b §9.7.8 | Pipeline NBA/NBO from a deterministic candidate set (FR-ADV-X1-011) | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-628 | 9.7b §9.7.8 | Experimentation as the evidence base for AI value (FR-ADV-X1-031) | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-629 | 9.7b §9.7.8 | RBAC-bound command bar (FR-ADV-X1-045) | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-630 | 9.7a §9.7.4.7 | Do not adopt guard frameworks wholesale; benchmark first | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-631 | 9.7a §9.7.4.8 | Do not adopt direct agent-to-agent invocation protocols; keep the blackboard | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-632 | 9.7b §9.7.17 | Pull Langfuse forward to A1 | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-633 | 9.7b §9.7.17 | Separate hard-capped B24 line with its own ladder | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-634 | 9.7b §9.7.17 | Deliver through a contract AI pod paired with the core team | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-635 | 9.7b §9.7.17 | Defer voice; WhatsApp first | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-636 | 9.7b §9.7.14.1 | Independent AI red-team review before A1 enablement | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-637 | 9.7b §9.7.17 | Memory OFF by default with DPIA | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-638 | 9.7b §9.7.17 | Propensity shadow ≥ 4 weeks before visible | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-639 | 9.7b §9.7.12.5 | Quarterly AI model review board (AI lead, R10, Founder) | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-640 | 9.7b §9.7.17 | Seed the answer library from ≥ 10 past bids | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-641 | 9.7b §9.7.17 | Report advanced-programme measures (plan approval rate, NBA acceptance, bid drafting time, abstention rate, B24 use) in A128 alongside OKPI-13/14/16/21 | Accepted (no rejecting DEC; issued in Part 9.7b) |
| RECOMMENDATION-651 | 9.8a §9.8.3.5 | If the squad is not funded, approve A1 only and move A2/A3 after Day 365 | Accepted (no rejecting DEC; issued in Part 9.8b) |
| RECOMMENDATION-652 | 9.8a §9.8.4.1 | Adopt sub-roles R03C (Customer Success Manager), R03P (Partner Manager), R16P (External Partner User) and persona variants P03d (Partner/Channel Manager) and P14f (Channel or referral partner, external) | Accepted (no rejecting DEC; issued in Part 9.8b) |
| RECOMMENDATION-655 | 9.8a §9.8.4.2 | Detractor follow-up within 2 business days and no incentives for scores | Accepted (no rejecting DEC; issued in Part 9.8b) |
| RECOMMENDATION-664 | 9.8b §9.8.11 | Use the KPI-ADV-X2- family so X2 KPIs cannot collide with KPI-ADV IDs issued by X1/X3 | Accepted (no rejecting DEC; issued in Part 9.8b) |
| RECOMMENDATION-667 | 9.8b §9.8.13.2 | Show AG-061…070 usage as a visible sub-line B02-X2 inside the DEC-008 cap | Accepted (no rejecting DEC; issued in Part 9.8b) |
| RECOMMENDATION-668 | 9.8b §9.8.16 | Regenerate Part 9.4 with assembly/build_ai_catalogue.py after approval so AG-061…070, AU-080…099 and WF-25…32 appear in the catalogue | Accepted (no rejecting DEC; issued in Part 9.8b) |
| RECOMMENDATION-669 | 9.8b §9.8.16 | Always write "Release A1/A2/A3" for X2 releases, because Part 5.1a uses A1…A8 for actor classes | Accepted (no rejecting DEC; issued in Part 9.8b) |
| RECOMMENDATION-670 | 9.8b AG-066 CPQ Bundle Advisor and Guardrail | AG-066 receives no price values; prices stay server-side | Accepted (no rejecting DEC; issued in Part 9.8b) |
| RECOMMENDATION-700 | 9.9a front matter | ID ranges used · DEC-400…409 · ASSUMPTION/GAP/CONFLICT/RECOMMENDATION-700…749 · ADR-130…139 · AG-071…080 · AU-100…119 · WF-33…39 · FR-ADV-X3-### · US- -V3nn · TC-ADV-X3-### · NFR-ADV-X3-## · screens A150–A169 and W45–W49 · local registers … | Accepted (no rejecting DEC; issued in Part 9.9a) |
| RECOMMENDATION-730 | 9.9a ADR-130 Analytics lakehouse on S3 Parque | Outbox-fed Parquet lakehouse with DuckDB | Accepted (no rejecting DEC; issued in Part 9.9b) |
| RECOMMENDATION-731 | 9.9a ADR-131 Semantic metrics layer as code; | Semantic metrics layer as code (MetricFlow-compatible YAML) | Accepted (no rejecting DEC; issued in Part 9.9b) |
| RECOMMENDATION-732 | 9.9a ADR-131 Semantic metrics layer as code; | NLQ emits validated plans only | Accepted (no rejecting DEC; issued in Part 9.9b) |
| RECOMMENDATION-733 | 9.9a ADR-133 AI observability on Langfuse sel | Bring Langfuse self-hosted forward to A1 with redaction at source | Accepted (no rejecting DEC; issued in Part 9.9b) |
| RECOMMENDATION-734 | 9.9a ADR-135 Chaos and DR drills automated in | AWS FIS in staging with alarm-bound stop conditions | Accepted (no rejecting DEC; issued in Part 9.9b) |
| RECOMMENDATION-735 | 9.9a ADR-136 Zero-trust Admin access: passkey | JIT elevation for privileged bundles | Accepted (no rejecting DEC; issued in Part 9.9b) |
| RECOMMENDATION-736 | 9.9a ADR-136 Zero-trust Admin access: passkey | Passkeys for all staff; offered to all portal users | Accepted (no rejecting DEC; issued in Part 9.9b) |
| RECOMMENDATION-737 | 9.9a ADR-137 BYOK through cross-account KMS k | BYOK via cross-account KMS on the Scale plan | Accepted (no rejecting DEC; issued in Part 9.9b) |
| RECOMMENDATION-738 | 9.9a §9.9.5.31 | New page patterns PP-STATUS and PP-DOCS | Accepted (no rejecting DEC; issued in Part 9.9b) |
| RECOMMENDATION-741 | 9.9a ADR-139 PWA with offline drafts only | PWA with drafts-only offline mode | Accepted (no rejecting DEC; issued in Part 9.9b) |
| RECOMMENDATION-744 | 9.9a ADR-138 Developer platform as a separate | Developer platform as a separate surface and audience | Accepted (no rejecting DEC; issued in Part 9.9b) |
| RECOMMENDATION-750 | 9.10 front matter | Approve A1 only; decide A2 and A3 at their gates | Accepted (DEC-417) |
| RECOMMENDATION-751 | 9.10 §9.10.11 | Fund the Release 1 alignment work to protect the date | Accepted (DEC-416) |
| RECOMMENDATION-752 | 9.10 §9.10.11 | Benchmark the local model against Claude at W1 before fixing the routing order for each task class | Accepted (no rejecting DEC; issued in Part 9.10) |
| RECOMMENDATION-753 | 9.10 §9.10.11 | Regenerate the AI catalogue, registers and RTM after every change to Parts 9.6–9.9 | Accepted |

<!-- GEN:RECOMMENDATION:END -->

### 9.2.4(e) ADR index

Status is taken from the ADR's own "Status" row (Part 3.1) or the status column of the batch register (Parts 4.1, 4.3). Part 7.3 ADRs have no status column and are shown as accepted in that part. Overlaps between Part 3.1 and Part 4.3 ADRs (ADR-012 vs ADR-051, ADR-026 vs ADR-050, ADR-015 vs ADR-052) are settled by **DEC-083: Part 3.1 governs** compute, IaC and CI.

<!-- GEN:ADR:BEGIN -->

| ADR | Title / decision | Status | Part |
|---|---|---|---|
| ADR-001 | Modular monolith on Django | Accepted (baseline): FRD OPT-07-01, NFR-029, CN-01 | 3.1 |
| ADR-002 | Shared-schema multi-tenancy with composite keys and PostgreSQL RLS | Accepted (baseline): FRD §5, DEC-009, DEC-065, §2.35.2 | 3.1 |
| ADR-003 | Transactional outbox with Celery and Valkey | Accepted (baseline): FRD §5, M06, NFR-005/006/007 | 3.1 |
| ADR-004 | Deterministic Policy Decision Point as an in-process library | Accepted (baseline concept): RECOMMENDATION-012, DEC-029, DEC-038, DEC-064. … | 3.1 |
| ADR-005 | Backend-for-Frontend authentication with the reused IdP | Accepted (baseline): DEC-003, DEC-019, DEC-058, NFR-001, NFR-003 | 3.1 |
| ADR-006 | Two frontends with a shared component package in a monorepo | Accepted (baseline): DEC-009, CN-03; package structure Proposed | 3.1 |
| ADR-007 | pgvector instead of an external vector database | Accepted (baseline "pgvector where justified", BRD §1.2); index choice Proposed | 3.1 |
| ADR-008 | Single model gateway with tiered routing | Accepted (baseline): DEC-007, DEC-008, DEC-042, FR-OP001 | 3.1 |
| ADR-009 | Provider adapter pattern (ports and adapters) with a registry | Accepted (baseline): FRD §9, FR-ADP-01, RECOMMENDATION-011 | 3.1 |
| ADR-010 | Publication snapshots on S3 + CloudFront with an atomic pointer | Accepted (baseline intent): BRD §9, FRD §8.1, NFR-020; mechanism Proposed … | 3.1 |
| ADR-011 | First-party analytics only | Accepted (baseline): FR-W10 "first-party attribution", M37 "no health events … | 3.1 |
| ADR-012 | Infrastructure as code with OpenTofu | Proposed (refines RECOMMENDATION-010 "Terraform/OpenTofu") | 3.1 |
| ADR-013 | Hosting on Amazon ECS on EC2 (single instance at pilot) | Proposed RECOMMENDATION-030; scale gate per DEC-040 | 3.1 |
| ADR-014 | Secrets and keys | Accepted (baseline): FRD §6 M05 "AWS Secrets Manager", NFR-004 | 3.1 |
| ADR-015 | Feature flags in-house, OpenFeature-compatible | Proposed (CFG-31, RECOMMENDATION-005) | 3.1 |
| ADR-016 | Email through Amazon SES | Accepted (baseline): DEC-025 | 3.1 |
| ADR-017 | Public search API: Tavily primary, Exa alternative | Accepted (baseline): BRD §6 (B03), FRD §6 M10/M11 | 3.1 |
| ADR-018 | Self-hosted extraction (Firecrawl) with in-process fallback | Accepted (baseline "self-host first", BRD §6 B04); licence handling Proposed | 3.1 |
| ADR-019 | Single region now, multi-region later | Deferred (DEC-040) | 3.1 |
| ADR-020 | Event schema versioning | Proposed [RECOMMENDATION-033 in Part 3.2] | 3.1 |
| ADR-021 | Queue topology and priorities | Proposed (§2.35.3 "transactional > interactive > batch") | 3.1 |
| ADR-022 | REST + OpenAPI 3.1, problem+json errors, no GraphQL | Accepted (baseline): FRD §5, NFR-015 | 3.1 |
| ADR-023 | Idempotency store in PostgreSQL with Valkey fast path | Proposed (FRD §5 "idempotency key/body hash") | 3.1 |
| ADR-024 | Object storage layout and malware scanning | Proposed [RECOMMENDATION-035 in Part 3.2] (NFR-021, BRL-PUB-04) | 3.1 |
| ADR-025 | Observability: OpenTelemetry, Sentry, CloudWatch | Accepted (baseline): DEC-041 | 3.1 |
| ADR-026 | CI/CD with GitHub Actions and OIDC | Proposed (M09, M62, DEC-061, DEC-063) | 3.1 |
| ADR-027 | In-house declarative workflow interpreter on Celery | Proposed (DEC-051, B-AUTO, CN-05) | 3.1 |
| ADR-028 | Scheduling with Celery Beat database scheduler | Proposed | 3.1 |
| ADR-029 | PostgreSQL full-text and trigram search | Accepted (baseline): DEC-037, SR-01 | 3.1 |
| ADR-030 | Money, quantity and time representation at the API boundary | Accepted (baseline): FRD §5, NFR-017, DEC-027 | 3.1 |
| ADR-031 | Caching strategy | Proposed (§3.1.11) | 3.1 |
| ADR-032 | Server-side document rendering with WeasyPrint | Proposed | 3.1 |
| ADR-033 | Identity boundary with the investor product | Accepted (baseline): DEC-003, DEC-058, DP-15 | 3.1 |
| ADR-034 | Near-real-time UI updates by polling, SSE later | Proposed | 3.1 |
| ADR-035 | Rate limiting in two layers | Proposed (§2.35.3 defaults; extended classes in Part 3.2 §3.2.1.7) | 3.1 |
| ADR-036 | Container image and runtime hardening | Proposed | 3.1 |
| ADR-037 | Calendar adapter: Google first, Microsoft Graph in W5 | Accepted (baseline): DEC-024 | 3.1 |
| ADR-038 | Regulated-action adapters with a manual evidence path first (payments, e-sign) | Accepted (baseline): DEC-022, DEC-023 | 3.1 |
| ADR-039 | WhatsApp through the Meta Cloud API directly | Proposed (FRD §6 M31 "Meta Cloud API"; BSP choice open) | 3.1 |
| ADR-040 | Social publishing and listening through platform APIs behind ports | Proposed (FRD §6 M33, M35 "Postiz candidate / platform APIs") | 3.1 |
| ADR-041 | Admin Copilot on the model gateway with RLS-scoped retrieval | Accepted (baseline): DEC-035, BRL-AI-12 | 3.1 |
| ADR-042 | Environment strategy and sandbox adapters | Proposed (§3.1.14, ABAC-12, RECOMMENDATION-017) | 3.1 |
| ADR-043 | Public intake abuse protection without paid WAF at pilot | Proposed (NFR-022; B21 ₹0, GAP-104) | 3.1 |
| ADR-050 | GitHub Actions CI/CD with OIDC federation to environment-scoped AWS roles; no static cloud keys | Proposed; reconcile with Part 3 | 4.3 |
| ADR-051 | OpenTofu for IaC with S3 state, module/live layout, policy-as-code checks; Terraform-compatible subset | Proposed; reconcile with Part 3 | 4.3 |
| ADR-052 | Feature flags via django-waffle behind an internal flags service at pilot; Unleash OSS as a scale-gate option | Proposed | 4.3 |
| ADR-053 | Rolling deploys with ECS circuit breaker at pilot; blue/green at the scale gate; expand/contract migrations mandatory; no production down-migrations | Proposed | 4.3 |
| ADR-054 | BFF confidential clients authenticate to the IdP with private_key_jwt where the IdP supports it; client secret otherwise | Proposed (confirm in Sprint 0 spike) | 4.1 |
| ADR-055 | Customer-managed KMS keys per data domain (§4.5.2), per-tenant DEKs; per-tenant CMK only as a Scale-plan option | Proposed | 4.1 |
| ADR-056 | Field-level envelope encryption (AES-256-GCM) with HMAC blind indexes for Restricted fields | Proposed | 4.1 |
| ADR-057 | OSS-first security tooling: Semgrep, Bandit, OSV-Scanner, pip-audit, gitleaks, Trivy, Checkov, OWASP ZAP | Proposed | 4.1 |
| ADR-058 | Observability: OTel SDKs + ADOT collector → X-Ray, CloudWatch metrics/logs; Sentry for errors; RUM via first-party web-vitals beacon; Grafana OSS … | Proposed | 4.3 |
| ADR-059 | AWS multi-account layout: management, log-archive, nonprod, prod, backup | Proposed | 4.3 |
| ADR-060 | Monorepo (pnpm/Turborepo + uv) for both frontends, shared UI, backend, AI assets, IaC and ops | Proposed | 4.3 |
| ADR-070 | In-house model gateway module in Django (ai.gateway) with provider adapters | Accepted in part (no status column) | 7.3 |
| ADR-071 | Orchestration in-house on Celery + PostgreSQL (agents as DAG steps) | Accepted in part (no status column) | 7.3 |
| ADR-072 | Structured outputs (output_config.format) + JSON Schema validation for every agent | Accepted in part (no status column) | 7.3 |
| ADR-073 | Haiku 5.5 as Tier 1a where per-agent eval parity holds; measured escalation to Sonnet 5.5 | Accepted in part (no status column) | 7.3 |
| ADR-074 | Batch API for all non-interactive agents | Accepted in part (no status column) | 7.3 |
| ADR-075 | Prompt layout: stable prefix first; 5-min TTL default; 1-h TTL only for RFP documents | Accepted in part (no status column) | 7.3 |
| ADR-076 | Semantic cache in pgvector (cosine ≥ 0.92), Public/Internal only, version-keyed | Accepted in part (no status column) | 7.3 |
| ADR-077 | pgvector for RAG and match ranking; no separate vector database | Accepted in part (no status column) | 7.3 |
| ADR-078 | LLM observability: gateway tables + OpenTelemetry in pilot; Langfuse self-hosted from growth gate | Accepted in part (no status column) | 7.3 |
| ADR-079 | promptfoo + DeepEval for evals in CI | Accepted in part (no status column) | 7.3 |
| ADR-080 | Presidio with Indian recognizers for PII detection and masking | Accepted in part (no status column) | 7.3 |
| ADR-081 | Tier 2 chain order Groq → Gemini free → OpenRouter free → Mistral free; default OFF; Public-only except Groq Internal-non-personal after DPA review | Accepted in part (no status column) | 7.3 |
| ADR-082 | No agent holds an external-side-effect tool; dispatch only by the engine through the PDP | Accepted in part (no status column) | 7.3 |
| ADR-083 | Per-agent, startup, tenant and global AI budgets with 80% alert and 100% hard stop; reserved 10% safety slice | Accepted in part (no status column) | 7.3 |
| ADR-084 | Prompt registry in git + immutable DB versions with eval run links | Accepted in part (no status column) | 7.3 |
| ADR-085 | Multi-scope kill switch via Valkey flags checked by gateway and engine | Accepted in part (no status column) | 7.3 |
| ADR-100 | Container compute: ECS on EC2 retained; Fargate for on-demand tasks | Proposed (resolves CONFLICT-320 with ADR-013) | 3.4 |
| ADR-101 | Valkey as broker and cache engine | Proposed (confirms CN-01, ADR-003; resolves CONFLICT-320 wording) | 3.4 |
| ADR-102 | Data recovery classes RC-1…RC-3 | Proposed (FR-ENH-B-002; resolves CONFLICT-322 and GAP-321) | 3.4 |
| ADR-103 | Adapter port contract v2 | Proposed (FR-ENH-B-004; extends ADR-009) | 3.4 |
| ADR-104 | Agent envelope v1.1 | Proposed (FR-ENH-B-009; extends Part 7.2 §7.2.7) | 3.4 |
| ADR-105 | Product-event ingress through an allowlisted internal adapter | Proposed (FR-ENH-B-010; resolves CONFLICT-330) | 3.4 |
| ADR-106 | Commercial journey as a projection, not a state machine | Proposed (FR-ENH-B-011) | 3.4 |
| ADR-107 | Declared execution policy per workflow revision | Proposed (FR-ENH-B-012, FR-ENH-B-013) | 3.4 |
| ADR-108 | Growth-scale validation profiles | Proposed (FR-ENH-B-001; resolves CONFLICT-321) | 3.4 |
| ADR-109 | Four permission base classes per ingress namespace | Proposed (FR-ENH-B-005) | 3.4 |
| ADR-110 | Supervisor-as-planner: AG-039 emits a typed plan; AU-053 validates; the M55 engine executes; ≤ 2 re-plans; agents never call agents | Accepted in part (no status column) | 9.7a |
| ADR-111 | Agent registry v2 with canary rollout (5% → 25% → 100%) and SLO-based auto-rollback | Accepted in part (no status column) | 9.7a |
| ADR-112 | Structured long-term memory in PostgreSQL with allowlisted fact types, evidence, purpose, TTL and consent; OFF by default | Accepted in part (no status column) | 9.7a |
| ADR-113 | Classical ML in-house (scikit-learn, LightGBM, MLflow self-hosted); advisory only; DEC-011 untouched | Accepted in part (no status column) | 9.7a |
| ADR-114 | Envelope v3 with plan binding, capability tokens and monotonic data class | Accepted in part (no status column) | 9.7a |
| ADR-115 | OTel GenAI spans + Langfuse self-hosted from A1 | Accepted in part (no status column) | 9.7a |
| ADR-116 | Ordered, fail-closed guardrail stack with deterministic policy packs VP-01…08; guard frameworks only after benchmark | Accepted in part (no status column) | 9.7a |
| ADR-117 | Eval harness v2: offline + adversarial + shadow + canary + online + drift + ML metrics | Accepted in part (no status column) | 9.7a |
| ADR-118 | Experimentation: pre-registered fixed-horizon A/B with SRM check; Thompson sampling only across pre-approved variants with 10% floor and guardrail … | Accepted in part (no status column) | 9.7a |
| ADR-119 | Separate hard-capped budget line B24 "Advanced AI" with its own ladder; advanced agents shed before any baseline agent | Accepted in part (no status column) | 9.7a |
| ADR-120 | Cadences extend the existing sequence engine (AU-022) and outbox rather than a new engine | Accepted in part (no status column) | 9.8b |
| ADR-121 | Deal rooms, partner portal, survey and QBR pages live in the existing Website/Portal app as new audiences and object grants | Accepted in part (no status column) | 9.8b |
| ADR-122 | Page builder uses an embedded open-source block editor (GrapesJS-class) that emits typed block JSON; rendering is server-side from approved snapshots | Accepted in part (no status column) | 9.8b |
| ADR-123 | Forecast snapshots are append-only rows with payload hash; corrections are new snapshots | Accepted in part (no status column) | 9.8b |
| ADR-124 | L2A matching is deterministic (weighted features with thresholds), not ML, at pilot | Accepted in part (no status column) | 9.8b |
| ADR-125 | Intent engagement events are first-party, consent-gated and stored in PostgreSQL with monthly partitions | Accepted in part (no status column) | 9.8b |
| ADR-130 | Analytics lakehouse on S3 Parquet with DuckDB, fed by the outbox | Proposed (A2) RECOMMENDATION-730 | 9.9a |
| ADR-131 | Semantic metrics layer as code; NLQ emits plans, never SQL | Proposed (A1 layer, A2 NLQ) [RECOMMENDATION-731, RECOMMENDATION-732] | 9.9a |
| ADR-132 | Identity resolution: deterministic first, human-reviewed suggestions | Proposed (A3) | 9.9a |
| ADR-133 | AI observability on Langfuse self-hosted with OTel GenAI conventions and redaction at source | Proposed (A1); brings forward ADR-078 from the growth gate RECOMMENDATION-733 | 9.9a |
| ADR-134 | Remediation runbooks as code with plan-hash approval | Proposed (A2) | 9.9a |
| ADR-135 | Chaos and DR drills automated in staging and the isolated restore account only | Proposed (A1) RECOMMENDATION-734 | 9.9a |
| ADR-136 | Zero-trust Admin access: passkeys, device certificate and JIT elevation | Proposed (A1) [RECOMMENDATION-735, RECOMMENDATION-736] | 9.9a |
| ADR-137 | BYOK through cross-account KMS keys wrapping per-tenant data keys | Proposed (A3, Scale plan only) RECOMMENDATION-737 | 9.9a |
| ADR-138 | Developer platform as a separate surface and audience | Proposed (A3) RECOMMENDATION-744; requires DEC-403 because Part 3.2 says … | 9.9a |
| ADR-139 | PWA with offline drafts only | Proposed (A3) RECOMMENDATION-741 | 9.9a |

<!-- GEN:ADR:END -->

### 9.2.4(f) DEC index (DEC-001…233)

One line per decision. The full text in Part 0A, Part 9.1 and Part 9.5 is binding. Part 9.1 decisions (§9.1.1 first cycle DEC-066…108, §9.1.4 second cycle DEC-109…156) override Part 0A where they amend it (Part 9.1 §9.1.2). Part 9.5 decisions DEC-157…215 resolve the 101 source-pack conflicts, DEC-216…227 close the earlier-part inconsistencies and set the re-plan, and DEC-228 records the Founder's approval of Option 2b (Part 9.5 §9.5.1.12 lists the earlier decisions they extend or supersede). Source-pack decision families SPDEC, SRC07-DEC and SDEC-08 are never part of this series (DEC-178).

<!-- GEN:DEC:BEGIN -->

| DEC | Log | Subject | Decision (one line) |
|---|---|---|---|
| DEC-001 | 0A | CONFLICT-001: 80% vs 90% precision | Two gates. (a) *Signal classification* (M14) must reach ≥ 80% precision on ≥ 100 human-reviewed pilot signals to exit Wave 1. (b) *Qualification* (OPT-04-02) must reach ≥ 90% precision on the approved benchmark set (≥ 200 … |
| DEC-002 | 0A | CONFLICT-002: fundraising wording left over | Replacements: "offerings or fundraising thesis" → "offerings and commercial objectives" (W33); "customize offerings or funding goals" → "customize offerings and commercial objectives"; "offering/issuer thesis" → "offering / … |
| DEC-003 | 0A | CONFLICT-003: "M01 already developed in AppNAI", "Approved AppNAI product truth" | M01 = reuse the AppNAI identity/security codebase as a shared library and IdP with a new, separate OAuth audience growth-engine and two clients (growth-website, growth-admin). Identity is shared; product access is not. M02 = … |
| DEC-004 | 0A | CONFLICT-004: ₹14,500 vs ₹15,000 base | ₹14,500 base, ₹16,675 with 15% contingency, ₹31,165 with Apollo reserve and developer seats. These are the authoritative figures |
| DEC-005 | 0A | CONFLICT-005: effort vs timeline vs team | Core delivery team of 4.0 engineering FTE + 0.5 growth/compliance lead: 1 backend (Django), 1 full-stack, 1 frontend (React), 0.5 QA automation, 0.5 DevOps/SRE (part-time contractor), plus founder/CTO as Product Owner and … |
| DEC-006 | 0A | CONFLICT-006: "no release labels" vs Release 1/2/Future | Use delivery waves W0–W6 mapped to the source day-phases. "Release 1" = W0–W3 (Day 1–90), "Release 2" = W4–W5 (Day 91–180), "Future" = W6+ (Day 181–365+). These are *planning groupings*, not product versions; production is one … |
| DEC-007 | 0A | CONFLICT-007: model provider and routing | Tier 0: deterministic rules, templates, exact/semantic cache (no LLM). Tier 1a: lighter Claude tier (Haiku-class) for high-volume classification and extraction, only where evals show parity (RECOMMENDATION-003 accepted). Tier … |
| DEC-008 | 0A | CONFLICT-008: ₹3,000/month AI reserve | Three budget ceilings, each a hard cap enforced by M53: Pilot ₹3,000/month (owned portfolio, BRD §8 pilot volumes); Growth gate ₹12,000/month (unlocked only when the BRD §8 scale gate passes: measured cost per qualified … |
| DEC-009 | 0A | CONFLICT-009: operator/admin workspace and "shared PostgreSQL" | Two frontends only: commercial-website-react (public site + external portal) and commercial-admin-react (Command Centre, where "Automation" is a separately permissioned route group). One PostgreSQL cluster for this product, … |
| DEC-010 | 0A | CONFLICT-010: A104/A105 under-mapped | A104 → BR-TENANT, WF-08, BR-M43, BR-M44, BR-M46. A105 → BR-TENANT, WF-10, BR-M44, BR-M47, BR-M48 |
| DEC-011 | 0A | CONFLICT-011: 0–1 components vs 0–100 thresholds | Opportunity score = round(100 × Σ wᵢ·cᵢ / Σ wⱼ over known components) with w = fit 0.25, evidence 0.25, intent 0.20, readiness 0.15, timing 0.15. If the known components carry less than 0.60 total weight, the score is "Unknown – … |
| DEC-012 | 0A | CONFLICT-012: superseded estimate retained | Planning basis = 287–483 person-days (₹13.05–32.93 L). The ₹9–13.5 L and ₹18–27 L figures are historical references only |
| DEC-013 | 0A | CONFLICT-013: "MVP growth dashboard" | Drop "MVP". M30 "Growth dashboard" is delivered in W2 |
| DEC-014 | 0A | CONFLICT-014: duplicated acceptance procedures | One Acceptance Procedure Register (AP-01…AP-09): AP-01 Configurable owned startups (26th synthetic startup); AP-02 Scope separation of business capabilities; AP-03 Opportunity qualification; AP-04 Closure and receipt … |
| DEC-015 | 0A | GAP-001 API catalogue missing | internal}/…. If the original 302-operation catalogue surfaces later, it is reconciled by a mapping table |
| DEC-016 | 0A | GAP-002 entity catalogue missing | Part 3 adds the unnamed core entities as *DERIVED*: Tenant, Startup, BusinessLine, Offering, OfferingVersion, CapabilityProfile, Domain, Publication, PublicationSnapshot, PreviewGrant, Bid, BidChecklistItem, Order, OrderLine, … |
| DEC-017 | 0A | GAP-003 test catalogue missing | Part 6 defines test cases (TC-###). The referenced SM-UT-001…066, SM-UAT-S###, SM-UX-UAT-### IDs are kept as aliases inside the traceability matrix so source references still resolve |
| DEC-018 | 0A | GAP-004 NFR targets missing | RECOMMENDATION-002 accepted: Website/Portal availability 99.5% monthly (pilot) → 99.9% at scale gate; Admin 99.5%; API p95 ≤ 500 ms reads / ≤ 800 ms writes (excluding provider latency); public page TTFB p95 ≤ 800 ms (CDN-cached … |
| DEC-019 | 0A | GAP-005 H02/H03 undefined | Interpreted as H02 = existing identity service (login, sessions, recovery) and H03 = existing security controls (MFA, session revocation, audit of auth events). A Sprint 0 compatibility spike (2–3 days) produces a pass/fail … |
| DEC-020 | 0A | GAP-006 budget IDs undefined | B01 AWS hosting ₹5,000 · B02 production AI inference ₹3,000 · B03 public search API ₹1,500 · B04 extraction compute/overage ₹1,000 · B05 email delivery ₹500 · B06 WhatsApp Business ₹2,000 · B07 monitoring/security/CI ₹500 · B08 … |
| DEC-021 | 0A | GAP-007 artefacts not attached | Proceed without them. MedMaarg claims (750+ users, ~150 monthly users, one Odisha location) are management claims, not independently audited (BRD §8). They may be published only after claim approval in M02/A051 with evidence. … |
| DEC-022 | 0A | GAP-008 payment provider | Payment adapter interface. Pilot path (W4): (1) bank transfer / UPI with evidence upload + finance maker-checker verification, which suits B2B, tenders and institutions; (2) an Indian payment gateway with payment links and … |
| DEC-023 | 0A | GAP-009 e-signature provider | E-sign adapter interface. Pilot (W4): signed-PDF upload + SHA-256 hash + counter-party confirmation through the portal (W24), with legal approval of the exact hash. W5: integrate one provider supporting Aadhaar eSign and DSC for … |
| DEC-024 | 0A | GAP-010 calendar | Google Workspace Calendar first (W2); Microsoft 365/Graph in W5. Free/busy only; no event-content reading beyond the booking's own events |
| DEC-025 | 0A | GAP-011 email | Amazon SES (matches budget B05); dedicated configuration set per startup sender; SPF/DKIM/DMARC enforced; bounce/complaint SNS webhooks → suppression. Resend stays an alternative adapter, not installed |
| DEC-026 | 0A | GAP-012 locales | Admin UI: English (en-IN) only. Website/portal UI chrome: en-IN at launch, i18n-ready (ICU message format). Content locales (pages, templates, WhatsApp templates): en-IN at launch; hi-IN, ta-IN, or-IN enabled in W5 for … |
| DEC-027 | 0A | GAP-013 tax, rounding, FX | TaxProfile per startup (GSTIN, state, LUT for exports); HSN/SAC per offering; intra-state CGST+SGST, inter-state IGST, exports zero-rated under LUT. Rounding: ROUND_HALF_UP to 2 decimals per line, document total = sum of rounded … |
| DEC-028 | 0A | GAP-014 retention | ASSUMPTION-018 adopted as baseline (subject to legal confirmation): invoices/financial records 8 years · contracts term + 8 years · audit log 7 years · marketing contact data 24 months after last eligible interaction · … |
| DEC-029 | 0A | GAP-015 non-Indian jurisdictions | Jurisdiction Rule Pack in the Policy Decision Point (RECOMMENDATION-016 accepted). Year 1 outbound allowlist: India (DPDP + TRAI rules), EU/EEA/UK (B2B email only to role-based or professionally published addresses, … |
| DEC-030 | 0A | GAP-016 children / guardian consent | No direct outreach, profiling or targeted advertising to anyone under 18. EduVerse acquisition goes through institutions (schools/colleges under MoU) and verified guardians. Intake (W17) asks age band first. Under 18 → guardian … |
| DEC-031 | 0A | GAP-017 scale | ASSUMPTION-002 adopted: Year 1 = 25–40 startup workspaces, 2–10 external tenants, 15–60 internal users, ≤ 500 portal users/month, ≤ 5,000 public sessions/month. Year 2 design point: 100 workspaces, 30 tenants, 200 internal … |
| DEC-032 | 0A | GAP-018 "agreed window" | Transactional automation (replies, follow-ups, notifications): ≥ 99% of eligible due runs started within 15 minutes of the due time. Scheduled batch (discovery, enrichment, reports): ≥ 99% within 24 hours. Quiet hours and time … |
| DEC-033 | 0A | GAP-019 missing FR rows | Created as FR-W31, FR-W32, FR-W33, FR-W34, FR-A109, FR-A110, FR-A111, FR-A112, FR-A113 in Part 2, using the BRD §17 purpose/acceptance text and the FRD §16.2 field specs |
| DEC-034 | 0A | GAP-020 phase gates vs M-ranges | Phase gates follow register (dependency) order, not numeric order. W0 = M01–M09 + M53 + M56 + M58; W1 = M10–M20; W2 = M21–M30 + M55; W3 = M31–M42 + M57; W4 = M43–M51; W5 = M52, M54, M59–M62; W6 = M63–M66. M54 (AI quality) is … |
| DEC-035 | 0A | GAP-021 Copilot | Admin Copilot (RECOMMENDATION-008 accepted): Admin-only side panel; answers questions over records the user is already authorized to see and over approved knowledge, with citations; can create *drafts* (message, task, note, … |
| DEC-036 | 0A | GAP-022 internal notifications | In-app notification centre (A106) + email digest (immediate for severity High/Critical, hourly or daily digest otherwise, per user preference). No WhatsApp/SMS to internal staff in W0–W5 |
| DEC-037 | 0A | GAP-023 global search | Scoped global search (Admin) over organizations, contacts, deals, bids, orders, documents and content using PostgreSQL full-text + trigram; RLS enforced; results show only permitted fields |
| DEC-038 | 0A | GAP-024 approval thresholds | Default approval policy (configurable per startup, versioned, tightening needs no approval, loosening needs founder approval): any discount > 0% → Sales Manager; > 10% → Startup Head; > 20%, or margin below the startup's floor … |
| DEC-039 | 0A | GAP-025 migration | No legacy system migration assumed. Import via A103 using versioned CSV/JSON templates for organizations, contacts (with consent evidence and source), offerings, price lists and open deals; dry-run validation report; imported … |
| DEC-040 | 0A | GAP-026 hosting/HA | AWS ap-south-1. Pilot: cost-minimal topology within B01 (managed PostgreSQL with PITR, containerized Django/Celery on small instances, S3, CloudFront). Scale gate: Multi-AZ database and two app instances behind a load balancer. … |
| DEC-041 | 0A | GAP-027 monitoring | OpenTelemetry instrumentation; Sentry (errors, free/developer tier first, verify limits) + CloudWatch (infra metrics/logs/alarms) + Prometheus/Grafana OSS optional at scale; SLO dashboards and alert routing defined in Part 4 |
| DEC-042 | 0A | GAP-028 model names and prices | Treated as unverified, time-sensitive. Part 7 shows pricing as formula inputs with "verify at implementation (as of 27 Nov 2026)" |
| DEC-043 | 0A | GAP-029 devices | Responsive web: Website/Portal mobile-first (360 px+), Admin desktop-first (1280 px+, usable down to 768 px for review/approval screens). Supported browsers: last 2 versions of Chrome, Edge, Firefox, Safari (iOS/macOS) |
| DEC-044 | 0A | GAP-030 SaaS support | Pilot support: 10:00–18:00 IST, Monday–Saturday, via portal tickets (W28/W34) and email. Internal response targets (not contractual): S1 2 h, S2 8 business hours, S3 3 business days. No public SLA until measured (OPT-20-03) |
| DEC-045 | 0A | GAP-031 inventory | OrganicSpec: per-SKU availability status + available quantity + reservation on order approval (released on cancellation or expiry). No warehouse, lot or batch management (Later) |
| DEC-046 | 0A | GAP-032 referral commission | Record only: partner, referral, attribution, proposed commission %, approval. Payouts happen outside the platform (finance system) |
| DEC-047 | 0A | GAP-033 SaaS plans | Three plan archetypes with configurable entitlements and no published price until the Service Owner approves: *Starter* (1 startup workspace, 3 users, email channel, 1,000 AI tasks/month), *Growth* (3 workspaces, 10 users, email … |
| DEC-048 | 0A | GAP-034 tool registry | Part 7 defines the agent tool registry (allowlisted internal tools, scopes, rate limits, side-effect class). No agent gets a tool with an external side effect without the dispatch guard |
| DEC-049 | 0A | AMB-1 Copilot | See DEC-035 |
| DEC-050 | 0A | AMB-2 Outcome certainty | Enum confirmed, uncertain, failed, reconciled_confirmed, reconciled_failed. Uncertain blocks retry until reconciled |
| DEC-051 | 0A | AMB-3 Workflow builder | Declarative DAG from approved node types (A113); conditions use a sandboxed expression language over typed fields; no code nodes, no secrets in configuration |
| DEC-052 | 0A | AMB-4 Capability-based bid/order | Bid and order desks are enabled by capability profile per startup/tenant. Owned-portfolio routing default: external AI project → AppNAI; education → EduVerse; healthcare partnership → MedMaarg; organic trade → OrganicSpec (FRD … |
| DEC-053 | 0A | AMB-5 Tender submission | Never automated. The system prepares the bid package and checklist; a human submits on the portal and records evidence (submission ID, timestamp, screenshot/receipt hash). Maximum autonomy L1 |
| DEC-054 | 0A | AMB-6 Closure criteria | ClosurePolicy per opportunity type: project/contract types close on *executed contract* (Won-Contracted) and are separately marked *Paid* on verified receipt; product/order types close on *verified payment or accepted delivery … |
| DEC-055 | 0A | AMB-7 Portfolio read-only | The portfolio (multi-startup) scope renders aggregates and drill-down only. Every mutating control is hidden and also denied server-side until exactly one startup is selected |
| DEC-056 | 0A | AMB-8 Support access | SupportAccessGrant: requested by platform support, approved by the tenant admin, scoped (modules, read-only by default), time-boxed (max 72 h), every access audited and visible to the tenant |
| DEC-057 | 0A | AMB-9 Founder snapshot import | One-way file import (A103) of non-confidential business facts into M02 drafts. Still subject to claim approval. No live link to the investor product |
| DEC-058 | 0A | AMB-10 Investor app | Separate product with a shared IdP and a distinct audience. Tokens for the investor audience are rejected here (NFR-001/OPT-01-01) |
| DEC-059 | 0A | Part 0 counted 118 supplementary business statements. A second pass found 22 more … | Supplementary BR count corrected to 140 (BR-S001…BR-S140), registered in Part 1 §1.12. Total business requirements = 71 primary + 140 supplementary = 211 |
| DEC-060 | 0A | M66 "Future product commercialization" is placed in the last phase, but its control … | The readiness gate (planned/approved/available status blocks promotion) is built in W0 within M02. The launch-approval workflow (A097/A098) is delivered in W6 |
| DEC-061 | 0A | M54 "AI quality and feedback" is placed in Day 121–180, yet "Regression fails block … | Eval harness and CI regression gate in W0 (with M08); human-feedback loop UI (A084) in W5 |
| DEC-062 | 0A | M61 "Admin command center" is in the last build phase, but the seven-view navigation … | Command Centre shell and navigation (A003, A089 frame) in W0–W2; cross-startup aggregate projections and exception queue completed in W5 |
| DEC-063 | 0A | M62 "End-to-end production release" is listed as a module, but release gating applies to … | Release pipeline and gates in W0 (with M09); the full synthetic E2E journey suite is completed in W5 |
| DEC-064 | 0A | Workflow register text "No AI direct finance or binding terms" and actor rule "no … | Autonomy cap matrix: money movement = not supported (record/verify only); contracts, quotes, discounts, bid submission, legal terms = L1 maximum; publishing and campaigns = L1 (approved hash) then L2 dispatch of the approved … |
| DEC-065 | 0A | "Startup" vs "tenant" for owned portfolio is not stated | Owned portfolio = one tenant ("Owner Portfolio Tenant") containing 25+ startup workspaces. Each external SaaS client = its own tenant with one or more startup workspaces. Cross-tenant aggregation is never permitted; … |
| DEC-229 | 8.4 | Budget is presented and governed as two ledgers: (A) development cost, one-time, to the … | Ledger A ₹52.7–84.1 L to Day 208; Ledger B ₹19,895–26,335/month base (₹24,035–30,475 with seats); TCO to 12 months after launch ₹57.1–89.7 L excluding Phase 2 |
| DEC-066 | 9.1 | Part 0 §0.10.2 maps A046 to EP-08; Part 2.1 maps it to EP-10 | Part 2.1 governs for all screen-to-epic mappings. Part 0 §0.10.2 was preliminary |
| DEC-067 | 9.1 | Part 0 places W08–W10 in EP-19 | W08/W09 → EP-11; W10 → EP-12 (Part 2.1) |
| DEC-068 | 9.1 | The bid buffer (BRL-BID-01) blocks recording a human submission made before the real … | BRL-BID-01 amended: the buffer is a warning and an internal readiness gate (status turns red; Startup Head override with reason). The hard block is the true deadline (FR-DM-02). Recording evidence of a submission made before the … |
| DEC-069 | 9.1 | A fixed 15-minute slot hold (BRL-MTG-02) conflicts with WCAG 2.2.1 Timing Adjustable | BRL-MTG-02 amended: 15-minute default hold, a warning 60 s before expiry, extendable once by 15 minutes on request |
| DEC-070 | 9.1 | The order state machine lacks reservation expiry (DEC-045) | Add transition Approved → ReservationExpired → Draft (stock released; owner notified) |
| DEC-071 | 9.1 | DEC-064 sets no cap for first-touch outreach | First-touch outreach = L1 (human approves the message) until a first-touch *template* is approved. Then L2 dispatch of that template with variables only. Never L3 |
| DEC-072 | 9.1 | BR-M09 epic placement differs between Part 0 and Part 1 | BR-M09 → EP-21 (Part 1 governs); Sprint 0 pipeline enablers sit in EP-01 stories that trace to BR-M09 |
| DEC-073 | 9.1 | Import (FR-A103) is needed in W1 but traced only to BR-SVC (Should) | FR-A103 traces to BR-TENANT (Must, W1) for import and BR-SVC (Should, W5) for portability export |
| DEC-074 | 9.1 | BR-M61 (Must) depends on BR-M60 (Could) | The dependency is soft: without M60 the Command Centre shows "Forecast not enabled" |
| DEC-075 | 9.1 | FR-W22 ships in W2 but its order and invoice data arrives in W4 | W22 cards are progressively enabled by capability flag: W2 enquiries, meetings, documents; W4 orders, invoices, onboarding |
| DEC-076 | 9.1 | No notification exists for loss of domain verification | Add NT-046 Domain verification lost / certificate expiring in 14 days: severity High; recipients R12, R05L; escalation to R02 after 1 business day |
| DEC-077 | 9.1 | BRL-TEN-08 says WebAuthn is "recommended"; DEC-019 checks it | Passkeys/WebAuthn required for R01, R02, R08–R12 and all approver roles once the IdP supports them (Sprint 0 check). TOTP is the interim minimum, with a migration deadline at the end of W2 |
| DEC-078 | 9.1 | DEC-028 has no retention for security/application logs; 90-day AI logs may be too short | Amend DEC-028: security and application logs 1 year (meets the CERT-In 180-day minimum and DPDP log expectations; verify). AI run metadata 1 year, AI payload bodies 90 days (redacted) |
| DEC-079 | 9.1 | A 4-hour RTO cannot cover a regional outage in the pilot | Amend DEC-018: RTO ≤ 4 h and RPO ≤ 15 min for instance, AZ and database failures. Regional outage: RTO ≤ 24 h, RPO ≤ 15 min (cross-region backups) in the pilot. Multi-region warm standby is a scale-gate option |
| DEC-080 | 9.1 | Business-hours support (DEC-044) vs 24×7 SLOs and 30-minute Critical escalation | Monitoring and alerting are 24×7 automated. Human out-of-hours response is limited to S1 categories: cross-tenant exposure, emergency stop, suppression breach, payment discrepancy > ₹1 lakh, production outage. Other Critical … |
| DEC-081 | 9.1 | No budget for a WAF although public intake needs one | AWS WAF on CloudFront from W2. Budget line B21 CDN/WAF ≈ ₹800–1,500/month (estimate; verify) |
| DEC-082 | 9.1 | Object Lock mode unspecified | S3 Object Lock in compliance mode for audit anchors (§2.34.3) |
| DEC-083 | 9.1 | Part 4 assumed compute/IaC/CI before Part 3 existed | Part 3.1 ADRs govern compute, IaC and CI. Part 4 pipeline stages apply unchanged |
| DEC-084 | 9.1 | Six DEC-016 entities are not mentioned in Part 2 | Part 3.3 governs the data model: BusinessLine, CapabilityProfile, PublicationSnapshot, PreviewGrant, BidChecklistItem and PlanVersion back FR-A003, A099/A100, A107/A108, A104 and A101 |
| DEC-085 | 9.1 | "Subscription" has two meanings | CustomerSubscription (M50 renewals) and ServiceSubscription (B-SVC billing). The Part 2.3 §2.27.18 Subscription states apply to ServiceSubscription |
| DEC-086 | 9.1 | AI Usage vs SaaS UsageMeterReading | AI usage is recorded in CostLedger (M53). UsageMeterReading holds billable SaaS meters. A nightly job aggregates tenant AI cost into the "AI tasks" meter |
| DEC-087 | 9.1 | Entity count of 199 vs the source's 155 | Accepted as a DERIVED superset. 17 FRD-retained entities cannot be identified (GAP-112); reconcile if the source catalogue is supplied |
| DEC-088 | 9.1 | Embedding dimension provisional | Embedding model = open-source multilingual E5-large class (1024 dimensions), self-hosted on CPU workers (Part 7.3; licence verify). The vector column stays at 1024 |
| DEC-089 | 9.1 | Part 0 §0.2 says "about 3 FTE" and "pgvector optionally" | Superseded by DEC-005 (4.0 + 0.5 FTE) and the ADR adopting pgvector |
| DEC-090 | 9.1 | No budget for delivery-lifecycle AI | New budget line B23 Delivery AI reserve ≈ ₹1,000/month (estimate), separate from runtime B02 |
| DEC-091 | 9.1 | BRL-AUT-06 cites Part 7 | Agent-level caps in Part 7.2 §7.2.9 complement the workflow-level caps in BRL-AUT-06; the stricter applies |
| DEC-092 | 9.1 | Part 4 cites LT-03/05/07 as "Batch 4.2" | Part 6.1 owns LT-01…LT-12; Part 4 references resolve to Part 6.1 |
| DEC-093 | 9.1 | Test ID formats differ (Part 1 §1.14 vs DEC-017) | Epic-based IDs govern: TS- -##, TC- -###, TC-AI-AG###-##, TC-AU-AU###-## |
| DEC-094 | 9.1 | SM-UT-037/049/050 unused in the FRD | Retained as unassigned aliases; no test obligation |
| DEC-095 | 9.1 | QA capacity (0.5 FTE) vs 43–97 pd QA effort; business UAT unplanned | Resolved in Part 8 (staffing uplift and UAT plan); see Part 8 §8.x |
| DEC-096 | 9.1 | W0 does not fit Day 1–15 | W0 split: W0-A Day 1–15 (environments, identity spike, CI, RLS/outbox/PDP skeletons, catalogue core); W0-B Day 16–30 (remaining governance, AI gateway and eval harness, cost control, privacy, observability). W1 runs Day 24–45 … |
| DEC-097 | 9.1 | A003 and W14–W16 epic placement | A003 → EP-17; W14–W16 → EP-14 (Part 2.1) |
| DEC-098 | 9.1 | CA-PUB cites DEC-001 for WCAG | Correct citation is RECOMMENDATION-001 (accepted) |
| DEC-099 | 9.1 | The RBAC row for A004 lacks a Finance price approval | R08 gets A(price) on A004/A068 price versions (WF-01) |
| DEC-100 | 9.1 | Missing defaults | Contact verification expiry 180 days. Privacy response deadline per DPDP Rules (verify); system default 30 days, escalation at 70% |
| DEC-101 | 9.1 | FR-COP-01 and FR-SRCH-01 lack an epic | Both → EP-17 |
| DEC-102 | 9.1 | Dimension code notation differs between batches | Mapping in Part 5.1a §5.6.6 is authoritative; both notations are valid |
| DEC-103 | 9.1 | EP-21 overlaps EP-01 Sprint 0 enablers | EP-21 reduced by ≈ 5.5 pd in planning. Programme central ≈ 416 pd (inside 287–483) |
| DEC-104 | 9.1 | Named operation count | 102 unique FRD-named operations + 3 OP. API catalogue total 555 (DERIVED; approval actions merged into one Approval resource) |
| DEC-105 | 9.1 | Hosting budget scope | B01 = ₹5,000–7,000/month estimate (prod + staging; staging scaled down out of hours). B20 = ₹300–600/month for cross-region backups (verify) |
| DEC-106 | 9.1 | Rate limits incomplete in Part 2.4 | Part 3.2 rate-limit classes govern (login, chat, portal, webhooks, heavy operations added) |
| DEC-107 | 9.1 | Entity names differ between Parts 2.1 and 3.3 | Part 3.3 names govern (e.g. Product → Offering) |
| DEC-108 | 9.1 | AI run volume vs the pilot cap | Gateway runs include Tier 0 cache/rules hits. The ₹3,000 cap applies to pilot volume only. Year 1 volume falls under the ₹12,000 growth ceiling (Part 7.3 estimate ≈ ₹4,600 at 4× pilot) |
| DEC-109 | 9.1 | Prompt-injection pass rule: Part 7 "≥98% clean" vs Part 4.1 "0 violations" | Two-tier safety gate (RECOMMENDATION-079): violation classes V1–V6 (data leak, unauthorized action, restricted data to Tier 2, cross-scope access, prohibited content, binding commitment) are zero tolerance; V7 (minor quality) … |
| DEC-110 | 9.1 | AG-026/AG-032 marked Tier 2 eligible with no Tier 2 provider listed | Tier 2 not enabled for these agents until a provider is listed and evaluated; fallback goes to Tier 3 |
| DEC-111 | 9.1 | Copilot model tier (US-1707 vs Part 7) | Part 7 routing governs: Tier 1a for cited retrieval answers, Tier 1b for synthesis/drafting |
| DEC-112 | 9.1 | Chat FAQ confidence gate 0.75 vs default 0.7 | Per-agent threshold table governs; the customer-facing chat gate is 0.75 |
| DEC-113 | 9.1 | TC-AI ID format | TC-AI-AG###-### and TC-AU-AU###-### govern |
| DEC-114 | 9.1 | AU-006 gate tooling | The pytest harness is the CI gate; promptfoo/DeepEval are optional dataset runners invoked by it |
| DEC-115 | 9.1 | No approved crisis/self-harm response in the public assistant | Fixed, Legal-approved safe-response template with helpline references (verify India helplines) plus immediate human handover; never AI-generated |
| DEC-116 | 9.1 | No bilingual labelling resource | Budget part-time bilingual reviewers per locale (hi/ta/or) from W5 |
| DEC-117 | 9.1 | NT-034 severity mismatch | Part 2.4 governs: Critical |
| DEC-118 | 9.1 | Unachievable 89.9% on 240 items | Gate evaluated as ≥ 90% (≥ 216/240) |
| DEC-119 | 9.1 | Business-day definition | Mon–Sat excluding configured public holidays (DEC-044) unless a contract states otherwise |
| DEC-120 | 9.1 | Bid submission recording at the deadline (AC-2107-02) | Per DEC-068: evidence of a submission made before the deadline can be recorded at any time; a claimed submission time at/after the deadline is rejected |
| DEC-121 | 9.1 | Restore-drill canary interval | 10 s (Part 6.1) |
| DEC-122 | 9.1 | "Subscription" in Part 5.3 | Means ServiceSubscription (DEC-085) |
| DEC-123 | 9.1 | W22 card label | Renamed "Outstanding balance (verified invoices)" |
| DEC-124 | 9.1 | Release 1 scope (~307 pd) vs Day-90 capacity (~169 pd) | Plan of record = re-baselined schedule (Part 8): Release 1 go/no-go about Day 152, Release 2 built by Day 180, W5 exit after the 30-day monitored pilot at about Day 201. Optional acceleration lever (two contract engineers, … |
| DEC-125 | 9.1 | W0 scope vs W0-A/W0-B dates | Part 8 sprint allocation and minimum gate scope govern |
| DEC-126 | 9.1 | Pen-test timing | External pen test before Release 1 go-live, retest before Release 2, then annually and after major changes |
| DEC-127 | 9.1 | ADR-043 "no paid WAF at pilot" | Superseded by DEC-081. B07 stays ₹500; the WAF cost is in B21 |
| DEC-128 | 9.1 | Budget lines | B01 ₹5,000–7,000; B20 ₹300–600; B21 ₹1,300–1,800; B23 ₹1,000 (estimates). Monthly base with 15% contingency ₹19,665–22,885; with optional Apollo and seats ₹34,155–37,375 |
| DEC-129 | 9.1 | Duplicate risks across parts | The Part 8 consolidated register governs; duplicates are merged there |
| DEC-130 | 9.1 | FR-OP001–003 lack an epic | FR-OP001 → EP-04; FR-OP002/003 → EP-21 |
| DEC-131 | 9.1 | Story dependencies split by the W0 cut | Part 8 sprint sequencing orders dependencies first (US-0108 before US-0113; US-0301 before US-0303) |
| DEC-132 | 9.1 | Growth/compliance lead over-allocated in W4–W5 | Raise to 0.75 FTE in W4–W5, or contract legal/compliance support (cost per Part 8) |
| DEC-133 | 9.1 | QA capacity | QA 1.0 FTE from Sprint 3 (+₹2.75–4.13 L); resolves GAP-165 and DEC-095 |
| DEC-134 | 9.1 | Policy loosening approver in AC-0810-03 | R01 Founder (BRL-APR-11) |
| DEC-135 | 9.1 | AC-0811-05 falls on a Sunday | Defer to Monday 09:00 recipient local time (BRL-ELG-08) |
| DEC-136 | 9.1 | Expected status for an unassigned user | 403 for role-denied actions on visible objects; uniform 404 for out-of-scope objects (BRL-TEN-04) |
| DEC-137 | 9.1 | Worked-example IDs in Part 6.1 | Superseded by Part 6.2 IDs (TC-13-036…049) |
| DEC-138 | 9.1 | AC-1206-05 title | R11 requests; R01 approves |
| DEC-139 | 9.1 | GST rates in examples | Illustrative only; finance advisor confirms (DEC-027 verify) |
| DEC-140 | 9.1 | Test automation effort (~100–240 pd) | Mostly inside story estimates (DoD: developers write unit/integration/contract tests; QA writes E2E and evals). Residual risk tracked as RSK-003 |
| DEC-141 | 9.1 | Part 2.3 states 162 business rules; 161 are defined | Rule count corrected to 161 |
| DEC-142 | 9.1 | Part 2.1 states 33 cross-cutting FRs (183 total) | 181 FRs (150 interface/operation + 31 cross-cutting) |
| DEC-143 | 9.1 | LT-01…12 defined in Parts 4.2 and 6.1 with different meanings | Part 6.1 owns LT-xx; Part 4.2 tables are "NFR load profiles", mapped to LT-xx in Part 6.7 |
| DEC-144 | 9.1 | Second-tenant fixture naming varies | Canonical name "T2 External-A" (GSE-SYN) |
| DEC-145 | 9.1 | Seven stories without an FR link | They are enablers tracing to BR/NFR/DEC; acceptable |
| DEC-146 | 9.1 | Part 6.1 risk matrix lacks a product-truth area | Add Product truth and claims gating (EP-02) at P0 depth |
| DEC-147 | 9.1 | NFR (61), FLT (9) and BR-S coverage gaps | Closed by Part 6.7 (TC-NFR, TC-FLT, TC-BRS and VER items); RTM regenerated |
| DEC-148 | 9.1 | ID family collisions: AD-## (3.1 drivers vs 3.2 adapters), PP-## (1 principles vs 6.2 … | IDs stay as written; cross-part references must be qualified with the part (e.g. "3.2/AD-05", "6.2/PP-03", "3.3/D-2", "3.1/B-07"). Unqualified AD-/PP-/D-/B- references mean the owning definitions in Parts 3.1, 1, 5.1a and the … |
| DEC-149 | 9.1 | 68 RECOMMENDATIONs have no recorded accept/reject | All proposed RECOMMENDATION-001…090 are accepted into the baseline under the delegated authority, except where a DEC states otherwise (e.g. ADR-043 superseded by DEC-081). They are implemented through the stories and tests that … |
| DEC-150 | 9.1 | ADR overlap: Part 4.3 ADR-050/051/052 vs Part 3.1 ADR-026/012/015 | Part 3.1 ADRs govern (DEC-083); Part 4.3's ADRs are operational elaborations of them |
| DEC-151 | 9.1 | No central tag allocation log | §9.2.3 reconstruction is authoritative; future tags continue from the highest number in each register |
| DEC-152 | 9.1 | Part 6.1 §6.1.12.1 divides rule coverage by 162 | Denominator is 161 (DEC-141) |
| DEC-153 | 9.1 | Usability targets differ: Part 6.1 (task success ≥ 80%, SUS ≥ 68) vs NFR-090 (≥ 90%, ≥ 70) | Two levels: ≥ 80% / SUS ≥ 68 is the per-wave minimum gate; ≥ 90% / SUS ≥ 70 is the NFR-090 target by Release 2 |
| DEC-154 | 9.1 | Load-test volumes differ between Part 6.1 and Part 4.2 (20 vs 30 req/s; 1,000 vs 5,000 … | The higher Part 4.2 design-capacity figures govern the load runs (LT-01 at 30 req/s; 5,000 due runs); the Part 6.1 figures are the expected Year-1 load |
| DEC-155 | 9.1 | GSE-SYN still names the second tenant "Client B" | Canonical "T2 External-A" (DEC-144) |
| DEC-156 | 9.1 | Part 4.2 §4.28 wave plan has no gate for NFR-023/024/052 | Gates: NFR-023 (accessibility) every wave from W2; NFR-024 (localization) at W5; NFR-052 at Release 2 |
| DEC-157 | 9.5 | Critical-service availability: pack ≥ 99.9% over a rolling 30 days (OPT-05-07, OKPI-06, … | (1) Pilot: 99.5% monthly for Website/Portal and Admin (DEC-018 unchanged). (2) From the scale gate (Topology B): 99.9% for the critical services: Website/Portal intake (public forms, portal sign-in and submissions), the dispatch … |
| DEC-158 | 9.5 | Recovery objectives: pack growth RTO ≤ 2 h (OKPI-32, mandatory), regenerable data 24 h / … | Recovery classes RC-1…RC-3 (Part 3.4 §3.4.5, ADR-102) are the single scheme. • RC-1 Critical (system of record: tenancy, consent/suppression, approvals, prices, contracts, orders, invoices, payments, ledgers, outbox, idempotency … |
| DEC-159 | 9.5 | Backup retention (Part 3.1: cross-region copy 7 days; Part 3.3: copies "expire in step" … | Retention: RDS automated backups and PITR 35 days in ap-south-1; cross-region automated backup copies 7 days in ap-south-2 (sufficient for the 15-minute regional RPO; keeps B20 at ₹300–600); weekly encrypted logical dump to the … |
| DEC-160 | 9.5 | Projection freshness: OKPI-28 (mandatory) ≤ 60 s from committed event to scoped … | Freshness classes (Part 4.4b §4.4.5.4.6) are adopted. F-1 Operational, p95 ≤ 60 s (OKPI-28, mandatory): Customer 360 (A032), pipeline/Kanban (A029), approval and exception queues, inbox, action centre (A106), run monitor (A110), … |
| DEC-161 | 9.5 | Capacity design points: pack initial 25 owned + 10 external, 50 staff sessions, 100k … | (1) DEC-031 remains the business-planning and cost baseline; infrastructure is not sized up. (2) Load-test design targets take the higher of each figure. WP-01 (Release 1 and 2 gates): 40 owned workspaces, 10 external tenants, … |
| DEC-162 | 9.5 | Budget alert thresholds: pack 70% / 90% vs BRL-AI-08 / NT-025 80% alert, 100% stop | For every M53 cap (AI, provider, channel, per surface): 70% = warning to the budget owner; 90% = critical to owner and FinOps, optional and paid jobs paused (degradation-ladder step 3); 100% = hard stop of all spend on that cap … |
| DEC-163 | 9.5 | Pack: ECS Fargate + ALB + ElastiCache Redis | Pilot: ECS on EC2 (ADR-013) and Valkey (ADR-003), single host, no ALB (Topology A). Scale gate (Topology B): ALB, two instances, Multi-AZ RDS, ElastiCache for Valkey; Fargate is an allowed option for on-demand or bursty tasks, … |
| DEC-164 | 9.5 | "No cross-region replication before approval" vs ADR-019 cross-region backup copies from … | DEC-040 is the recorded approval for encrypted backup copies to ap-south-2 (inside India). No live replication of application data outside ap-south-1 without a new decision. The IaC change record cites DEC-040 and this decision … |
| DEC-165 | 9.5 | 5xx alert thresholds inside document 31 | AL-06 pages at > 2% 5xx over 5 min; AL-50 opens a ticket at > 1% over 10 min, both with a minimum-volume rule (≥ 200 requests in the window) |
| DEC-166 | 9.5 | Environment sets differ (pack: local, shared dev, SIT, UAT, staging, prod, recovery; … | Canonical set: local, ci (ephemeral, per pull request), test (persistent non-production integration environment, nightly; = pack "SIT"), staging (= pack "UAT" window and pre-production), prod, recovery (backup-account restore … |
| DEC-167 | 9.5 | Queue topology: pack separates priority-control and financial queues; ADR-021 has neither | ADR-021 amended: add a control queue (emergency stop, revocation, kill switches; one reserved worker slot, prefetch 1) and a finance queue (posting, reconciliation, allocation; prefetch 1, no autoscale-down below one slot). … |
| DEC-168 | 9.5 | Vulnerability severity: pack by business impact vs Part 4.1 CVSS adjusted for exposure | Dual classification; the higher wins. Business-impact Critical (confidential disclosure, financial-integrity loss, credential exposure, uncontrolled dispatch) is never waivable |
| DEC-169 | 9.5 | Product separation: "two products, four frontends, two backends"; startups' own product … | (1) This product = two frontends + one backend (DEC-009, NFR-001, NFR-031). The pack's "four frontends and two backends" counts the separate investor application (DEC-058), which is out of scope; its only effect here is the … |
| DEC-170 | 9.5 | Path canon: source (document 07) retains legacy method/path contracts for 302 operations … | (1) The source's legacy method and path are canonical for every operation in the document 07 register (302 retained + 19 candidate). (2) Where a Part 3.2 derived path differs, the Part 3.2 path is renamed to the source path in … |
| DEC-171 | 9.5 | Generic POST …/{id}/control with an action enum (12 resources) vs Part 3.2 per-action … | The source /control route is the canonical contract (DEC-170). It is implemented as a thin dispatcher: the action value is validated against the resource's state machine and each action keeps its own Part 3.2 operation ID, … |
| DEC-172 | 9.5 | Legacy per-object approve/review routes (/contracts/{id}/approve, … | Legacy approve/review routes are canonical paths (DEC-170) that create or decide the Approval for the object's current revision and content hash (CA-APPROVE). The single Approval resource remains the system of record and its own … |
| DEC-173 | 9.5 | Idempotency key and expected revision as body fields (source) vs headers (Part 3.2) | Idempotency-Key and If-Match headers are normative and mandatory on every state-changing POST/PATCH (stricter than the source). Body fields idempotency_key and expected_revision are accepted for legacy compatibility on legacy … |
| DEC-174 | 9.5 | Two list envelopes and two async vocabularies | One list envelope everywhere: { "data": [...], "page": { "next_cursor", "prev_cursor", "limit" }, "meta": { "as_of", "total_estimate", "total_exact" } }; query limit (1–100, default 25) and cursor; on legacy paths page_size is … |
| DEC-175 | 9.5 | Website/portal boundary: token routes under /public/, five "Portal + Admin" operations, … | (1) Signed-token reads (preferences, slots, API-083) are portal-class on the website ingress with RL-PUB-W; token ≥ 128 bits entropy, single purpose, expiry ≤ 30 days. (2) Agreements, payment status and onboarding use a portal … |
| DEC-176 | 9.5 | 24 status-code proposals differ from Part 3.2's side-effect rule; bid control lists submit | Part 3.2 §3.2.1.10 status rule is normative (the 24 rows are corrected as in Part 3.5a §3.5.4.7). On bids, submit means record a human portal submission with evidence (API-367); the product never submits a bid (DEC-053) |
| DEC-177 | 9.5 | Retention-policy operation: source "create retention versions freely" vs API-091 … | DEC-028 governs: tenants may only tighten retention; loosening is a platform change through release governance |
| DEC-178 | 9.5 | Source-pack decision IDs collide with DEC-001…156 | Renamed families, never part of the DEC series: document 24 decisions (180 retained + 172 expansion) → SPDEC-001…180 and SPDEC-X-…; document 07 decisions → SRC07-DEC-001…038; document 08 schema decisions → SDEC-08-039…042. … |
| DEC-179 | 9.5 | Residual investor and fundraising wording in pack documents 03, 05, 06, 09, 10, 12–14, … | DEC-002 is extended to every new instance. Replacements: "investor/customer" → "customer"; "lead/investor record" → "lead record"; "investor/customer journey/portal/records" → "customer journey/portal/records"; "marketplace … |
| DEC-180 | 9.5 | Inventory counts differ between the pack and the blueprint | Reconciled counts (authoritative for Part 10): see §9.5.1.10. In short: BR 76 = pack "71 retained" (= blueprint's 71 primary BRs: BR-M01…M66 + BR-TENANT/WEB/AUTO/SVC/QA) + 5 "added" expansion scope statements XBR-01…05, which … |
| DEC-181 | 9.5 | Effort double counting: pack 385 PD base + 62/114/196 PD expansion = 349/499/679 PD … | (1) The Part 8.1 story plan is binding for the baseline (DEC-124); the pack's 385 PD is a top-down cross-check (difference 31 pd, ≈ 8%, inside the P80 spread). (2) Overlap stated: the nine expansion screens have stories … |
| DEC-182 | 9.5 | Section-number clashes: Part 2.6 local §2.6.x vs Part 2.2 §2.6; Part 4.4 vs Part 4.1 … | Cross-references always carry the part prefix ("Part 2.2 §2.6.1", "Part 2.6 §2.6.5", "Part 4.1 §4.4", "Part 7.3 §7.5"). Unprefixed references mean the section in the same file. At assembly, Part 7.3's internal §7.4–§7.9 are … |
| DEC-183 | 9.5 | "Six runtime AI responsibilities" vs the Part 7.1 catalogue; pack Django app and … | Part 7.1 governs the agent catalogue (36 agents, 43 automations); the pack's six responsibilities are families (mapping in Part 3.4 §3.4.5.5 B). Part 3.1 module names and ADR-006/ADR-060 repository layout govern; pack names are … |
| DEC-184 | 9.5 | Embedding dimension left open in document 08 | Closed by DEC-088: 1024 dimensions (E5-large class); each migration asserts the dimension per model_id (TC-ENH-E-035); SDEC-08-042 is answered |
| DEC-185 | 9.5 | Reuse existing identity tables vs product-local ten_user | ten_user is a profile extension of the reused identity: primary key equals (or is 1:1 with) the identity subject; no credentials, passwords or MFA data; the W0-A identity spike (DEC-019) confirms the key type before the first … |
| DEC-186 | 9.5 | Mutable fulfilment milestone (source) vs append-only fulfilment events (Part 3.3) | Both: new com_fulfillment_milestone (plan; mutable until accepted) + unchanged append-only com_fulfillment_event (evidence). Delivered quantities are derived from events only. Milestones are Should (W6); acceptance-with-evidence … |
| DEC-187 | 9.5 | Global business keys (unique(code), unique(invoice_no)) vs tenant/startup scope | Scoped keys govern (tenant, startup). Listed exceptions stay global: verified hostname, platform service-invoice number, release tag |
| DEC-188 | 9.5 | sales_order.direction includes service/training/project vs blueprint sell/buy | direction = ledger side (sell/buy) only; new column order_kind ∈ {goods, service, training, project}; receivable/payable separation (BRL-ORD-06) unchanged |
| DEC-189 | 9.5 | delay_seconds vs wait_business_days for sequence steps | Business-day cadence governs outreach (DEC-119); no seconds-based outreach delays; system-internal waits use workflow timers |
| DEC-190 | 9.5 | Source single sales_data_transfer and *_revision tables vs blueprint entities | Blueprint entities govern (DEC-107): saas_import_job + saas_export_job; versioned aut_trigger and aut_workflow_template. Read-only view v_data_transfer serves the legacy list path (DEC-170) |
| DEC-191 | 9.5 | New entities proposed by several groups overlap (service request in C, E and H; evidence … | (1) ServiceRequest = saas_service_request (ENT-ENH-E-02); H's svc_service_request (ENT-ENH-H-07) and C's sales_ui_service_request are aliases; it backs FR-W34, W28 support cases and API-440/442. (2) EvidenceRecord = … |
| DEC-192 | 9.5 | Pack: local model gateway first, no paid AI as a prerequisite; operations list … | DEC-007 stays: Tier 1 = Anthropic Claude (paid, capped by DEC-008); Tier 2 free models opt-in, default off, Public/Internal-non-personal data only; local inference is evaluated in a W6 spike with AU-045 (benchmark) and AU-047 … |
| DEC-193 | 9.5 | Search primary: native source registry/feeds first (pack) vs Tavily primary (AD-05) | Native source adapters (registries, feeds, official APIs) are primary; Tavily free credits are secondary; pay-as-you-go within B03 only after the W1 benchmark shows a coverage gap. SearXNG is not deployed until an AGPL and … |
| DEC-194 | 9.5 | Extraction: Scrapy + Trafilatura, Playwright for JS (pack) vs Firecrawl self-hosted + … | Trafilatura for static pages; Firecrawl (self-hosted, unmodified) vs a Playwright renderer for JS pages is decided by the W1 benchmark; both licence-registered (AU-047) |
| DEC-195 | 9.5 | Schema-valid AI outputs: OKPI-13 ≥ 99.5% (timeouts count invalid) vs ≥ 99% first pass; … | Adopt the pack's stricter thresholds. Release gate from W1 and steady state: final schema-valid ≥ 99.5% (after bounded repair; timeouts and abandoned repairs count as invalid) measured on ≥ 1,000 calls (eval set plus shadow … |
| DEC-196 | 9.5 | Classification precision: OKPI-15 ≥ 90% vs DEC-001 80% at W1 exit | DEC-001 governs W1 (≥ 80% on ≥ 100 reviewed signals); ≥ 90% is required before any L2/L3 autonomy and is the W4 target; sample ≥ 200 per vertical; recall also reported |
| DEC-197 | 9.5 | Provider shortlists: PandaDoc e-sign; Postiz social publishing (AGPL) | DEC-023 governs e-sign (Aadhaar eSign/DSC providers, DocuSign; PandaDoc may enter the AD-10 evaluation only if it gives legally valid signatures for Indian counterparties — verify). Postiz is not adopted for W3 (AGPL network-use … |
| DEC-198 | 9.5 | Budget allocation per provider; Hunter line; pilot run-cost figure; B23 missing from … | (1) DEC-020 governs allocation (dedicated lines B13, B15, B16, B18, B22). (2) Hunter = free-quota validation fallback under B10 only, never additive to B08; B18 stays ₹0 reserved; Part 3.2 AD-19 is corrected. (3) Part 8.2 run … |
| DEC-199 | 9.5 | IC-270 "Apollo GraphQL" mapped to contact discovery | Reclassified developer tools, decision Defer; never a data source |
| DEC-200 | 9.5 | Error tracking: pack avoids hosted Sentry/Datadog | Sentry free/developer tier stays (DEC-041; scrubbed payloads, ₹0); never buy a paid tier; if free limits bind, move to a self-hosted open-source tracker after licence review |
| DEC-201 | 9.5 | "Cost routing" listed as an AI prompt contract | Deterministic (AU-001/AU-002; OPT-10-01 rules first); PC-13 is registered with "no model" |
| DEC-202 | 9.5 | Development-time Claude plugins listed against runtime screens; provider prices stated … | (1) Developer plugins (CLAUDE.md management, plugin toolkit, Figma, Postman, document skills…) are build aids only: no runtime adapter, entitlement, budget line or UI control; cost only under B09 seats. (2) DEC-042 applies to … |
| DEC-203 | 9.5 | Coverage and traceability thresholds differ across docs 19/22/23/24, NFR-082, DoD D-8 … | Adopt the stricter pack thresholds. (1) Critical-rule branch coverage ≥ 90% for PDP, approvals, consent/suppression, finance/ledger and tenancy rule modules, from their first commit (greenfield, cheapest when strict from the … |
| DEC-204 | 9.5 | DEC-094 kept SM-UT-037/049/050 as unassigned aliases; document 22 defines them | DEC-094 is superseded. SM-UT-037 (webhook signature/replay), SM-UT-049 (planned offering cannot be published) and SM-UT-050 (wellness need matching) carry test obligations mapped to TC-15-005/TC-08-048, TC-11-008/TC-13-003 and … |
| DEC-205 | 9.5 | Severity and priority scales | Defects: S1–S4 (with fix priority FP1–FP4, Part 6.1 §6.1.8). Tests: P0–P3 (execution priority). "P0" is never used for defect severity. Mapping table §9.5.1.10.2 |
| DEC-206 | 9.5 | Combined preflight: 1,188 records in 6 groups (doc 36) vs 1,545 in 9 groups (doc 38) | 9-group, 1,545-record definition governs; groups G1–G6 equal the 1,188 subset. The preflight is fail-closed in A090 (RGV, FR-ENH-I-060) |
| DEC-207 | 9.5 | 20 vs 21 optimization dimensions | 20 weighted source dimensions + non-weighted blocking gate G0 (21 rows). No weight is invented |
| DEC-208 | 9.5 | Absolute INR discount (SM-UT-057) vs percentage thresholds (DEC-038, BRL-APR-04) | Both discount types are supported per line and per quote. Store the amount and the effective percentage = discount ÷ pre-discount subtotal, ROUND_HALF_UP to 2 dp. Approval thresholds are evaluated on the effective percentage; … |
| DEC-209 | 9.5 | Support response: doc 34 P1 15 min / P2 1 h / P3 next business day vs DEC-044 (S1 2 h, … | Pilot and owned portfolio: DEC-044 and DEC-080 stay. For contracted SaaS clients, the document 34 targets become a contract option only when (a) a paid support plan with on-call exists, staffed by ≥ 2 trained people per covered … |
| DEC-210 | 9.5 | Plan names: self-service / managed / enterprise vs Starter / Growth / Scale | Two orthogonal axes. Plan tier (entitlements and price) = Starter / Growth / Scale (DEC-047). Service arrangement = self_service / managed / hybrid (FR-ENH-A-015; Group J's service_model is renamed service_arrangement). … |
| DEC-211 | 9.5 | Two opportunity-scoring models in document 11 | DEC-011 stays the default and only active model at launch. The six-factor model is an optional scoring-version template "partnership-fit" (FR-ENH-A-007, Could, W6); activation requires a benchmark on the same labelled set with … |
| DEC-212 | 9.5 | Source coverage definition | KPI-27 stays (inventory coverage); KPI-ENH-A-01 "Fresh source coverage" (successful fresh eligible checks ÷ eligible due sources) is added and shown beside it |
| DEC-213 | 9.5 | Reply taxonomy differs; BRL-SEQ-02 lacks "decline" and does not say whether … | 11-class union (Part 2.6 §2.6.5.2.6): interest/positive, question, objection, decline, unsubscribe/STOP, out-of-office, meeting request, escalation/urgent, clinical, bounce (provider event, not a reply class), unknown. … |
| DEC-214 | 9.5 | One relationship stage (doc 37) vs separate state machines | Separate state machines remain the only writable states; a stable relationship_id and a read-only derived relationship stage are added (FR-ENH-A-016, Should, W6). The stage is never set by hand or by AI |
| DEC-215 | 9.5 | Breakpoints: doc 17 three tiers vs Part 2.5 five tiers vs DEC-043 | Part 2.5 §2.48 tiers stay. Doc 17 terms map: mobile = XS + SM (< 768 effective for Admin), tablet = 768–1279, desktop ≥ 1280. Test matrix 360 / 768 / 1280 / 1440 + 320 px reflow for public and portal. Admin below 768 px is not … |
| DEC-216 | 9.5 | LT IDs used for different scenarios in Parts 4.2 and 6.1; no 250-session profile | DEC-143 confirmed: Part 6.1 owns LT-01…12; enhancement load tests keep their group IDs (LT-ENH-B-01…04, LT-ENH-C-01, LT-ENH-I-01…06) and are indexed in the Part 6.6 RTM under WP-01/02/03 (DEC-161), which now include the … |
| DEC-217 | 9.5 | Part 6 tests reference no API IDs; ports list incomplete; webhook and upload-integrity … | (1) RTM (final/RTM.csv) gains columns api_ids and sit_aliases; TC-ENH-D rows supply operation-level links; all TC-ENH-A…J IDs are merged into the RTM by the Part 6 owner. (2) The Part 3.1 port list is extended with EventsPort, … |
| DEC-218 | 9.5 | GAP-143 excludes all meeting summarisation | GAP-143 narrowed: staff-authored notes may be summarised (AG-037, Should, W6); recordings and transcripts stay excluded |
| DEC-219 | 9.5 | Missing personas, undefined C03, missing seed offerings | (1) Persona variants and P17–P20, sub-roles R11T/R12I adopted; role R21 (managed-service delegate) adopted with A-6 (W6). (2) C03 = the engineering-effort budget line of Part 8.1/8.2 (DEC-020 text amended). (3) RamVan and Smart … |
| DEC-220 | 9.5 | OPT count; no training-completion mechanism; KPI-23 allocation basis; Part 9.3 … | (1) Part 0 §0.3.1 reads "22 OPT IDs cited (13 FRD + 9 BRD-only)". (2) Training completion is recorded by FR-ENH-J-001/004 (Must, J-1). (3) KPI-23 uses the Part 8.3c §8.3.5.13.7 allocation definitions. (4) Part 9.3 inventory … |
| DEC-221 | 9.5 | Status of enhancement artefacts | All RECOMMENDATION-300…491 issued by the ten enhancement parts are accepted into the baseline except where DEC-157…227 vary them (extends DEC-149). Enhanced FRs (FR-ENH-A…J), stories (US-xx-E nn) and tests (TC-ENH-A…J) are … |
| DEC-222 | 9.5 | Estimate-versus-actual tracking | From Sprint 0, every story records base estimate, actual pd and rework pd (in a sheet until B-15 is built); the sprint review reports the ratio per discipline; ratio > 1.25 for two sprints in one discipline triggers … |
| DEC-223 | 9.5 | Cross-group duplicates in the enhancement parts | The owner package in §9.5.2.2 is the only implementation of each duplicated capability (e.g. fail-fast configuration = I-2; authorization-safe cache key = F-1; benchmark record = F-1 AU-045; release-gate/evidence validator = … |
| DEC-224 | 9.5 | MoSCoW of the enhancements | Triage in §9.5.2.3 is binding. Must = safety, compliance, financial integrity, isolation, the 21 mandatory OKPIs, or a defect fix in already-planned scope. Musts land in Release 1 or Release 2 before the activation that needs … |
| DEC-225 | 9.5 | Effort envelope | The programme estimate becomes 532 / 722 / 921 pd (low / central / high; PERT P80 ≈ 778 pd). This supersedes the 287–483 pd envelope of DEC-012 for planning purposes; the BRD §6 figure remains the client's original reference. … |
| DEC-226 | 9.5 | Pull-forward and spill rules after the re-plan | (1) A Should package may be pulled into Release 2 only if the 3-sprint average velocity after S7 is ≥ 48 SP and the Release 2 Must set is on plan. (2) If velocity after S4 is < 40 SP, the Part 8.1 tier 2 spill list applies … |
| DEC-227 | 9.5 | Plan of record after the enhancements | Plan of record = Option 2b (two contract engineers from Sprint 3, Mon 18 Jan 2027, to the Release 2 build gate): Release 1 go/no-go Fri 4 Jun 2027 (Day 180); Release 2 build go/no-go Fri 2 Jul 2027 (Day 208); W5 exit Fri 23 Jul … |
| DEC-228 | 9.5 | Option 2b approved: two contract engineers from Sprint 3 to the Release 2 build gate | Plan of record: Release 1 go/no-go Fri 4 Jun 2027 (Day 180); Release 2 build Fri 2 Jul 2027 (Day 208); W5 exit after the 30-day monitored pilot Fri 23 Jul 2027 (Day 229). Contract engineer cost ₹10.9–16.4 L (estimate); total … |
| DEC-230 | 9.5 | Ledger A (development, one-time) budget approved: ₹52.7–84.1 lakh to the Release 2 build … | Development spend may be committed against Ledger A lines. Monthly burn is reported against the line items; a forecast above the high estimate for any line triggers change control (BRD §11). Provider prices remain "verify at … |
| DEC-231 | 9.5 | Ledger B (subscription and running cost, recurring) budget approved: ₹19,895–26,335 per … | Subscriptions may be opened per line as the plan reaches them; tenant and platform budget caps in the model gateway and FinOps alerts (Part 7.3, Part 8.3) are set to these figures. Any new paid plugin or provider still requires … |
| DEC-232 | 9.5 | QA uplift and growth/compliance allocation confirmed: QA 1.0 FTE from Sprint 3 (DEC-133) … | Team of record: 4 engineers + 2 contract engineers (Sprint 3 → Release 2 gate, DEC-228) + QA 1.0 FTE from Sprint 3 + growth/compliance 0.5 FTE, rising to 0.75 FTE in W4–W5; founder as Product Owner. Costs already within Ledger A … |
| DEC-233 | 9.5 | "+5 business requirements" confirmed as expansion statements XBR-01…05: the five BRs … | BR baseline of record: 71 primary BRs + 5 XBR expansion statements = the source pack's 76; no new primary BR; DEC-180 confirmed. RTM unchanged (100%) |
| DEC-234 | 9.6a | Literal-alignment rule: source names canonical, blueprint names as aliases; pack … | Part 9.5 §9.5.1 (DEC-157…215): Where DEC-234…269 amend a DEC-157…215 outcome, this part governs; Naming (all parts): A name that the source pack gives a field, state, queue, app, path, screen term, metric or ID is canonical; … |
| DEC-235 | 9.6a | Doc 11 “Coverage” metric adopted literally beside the inventory coverage metric ((c) … | KPI-ENH-A-01 (Part 2.6): Renamed to the source term “Coverage” (canonical), alias “Fresh source coverage”; KPI-27 (Part 1): Renamed “Coverage % by approved known sources” (canonical doc 11 wording), alias KPI-27 “source … |
| DEC-236 | 9.6a | Both doc 11 scores active at launch: five-factor priority score and six-factor … | BRL-SCR-01…03 (Part 2.3): Unchanged; New rule text in BRL-SCR-04 (Part 2.3, added by this decision): Qualification fit = round(100 × Σ wᵢcᵢ ÷ Σ w_known) with weights capability 0.30, explicit need 0.25, qualification 0.15, … |
| DEC-237 | 9.6a | Reply handling: any verified reply stops the generic sequence; the eight source classes … | BRL-SEQ-02 (Part 2.3, as amended by DEC-213): Out-of-office now stops the generic sequence like every other verified reply; Reply classification taxonomy (Part 2.6 §2.6.5.2.6, AG-013): The canonical label set is the source's … |
| DEC-238 | 9.6a | Relationship business state with the seven literal doc 37 states and expected outputs … | FR-ENH-A-016 (Part 2.6): The derived relationship_state takes exactly these canonical values: New, Qualified, Engaged, Quote requested, Negotiation, Contracted, Paid / fulfillment; Expected outputs (WF-04, WF-06, WF-08 to WF-10 … |
| DEC-239 | 9.6a | Capacity: the pack's initial and growth columns are the binding design-capacity and … | DEC-031 (Part 0A) reading: DEC-031 is a demand forecast for costing only; NFR-ENH-B-01…04 (Part 3.4): Column headings renamed to the source's “Initial target” and “Growth target”; WP-01 is the initial-target test, WP-02 the … |
| DEC-240 | 9.6a | Recovery objectives: initial ≤ 15 min / ≤ 4 h and growth ≤ 15 min / ≤ 2 h adopted as … | DEC-158 (Part 9.5): “Initial” = the pilot (Topology A); “Growth” = from the first of: the scale gate, or the 11th external tenant, or 26th owned startup (the pack's growth column starts above 25 + 10); Regional outage: The … |
| DEC-241 | 9.6a | Source Django app names and monorepo paths become canonical ((a) Adopt source literally; … | Part 3.1 §3.1.4 (module map) and ADR-006: Canonical Django app labels: accounts (the reused existing account/auth service; product-local profile data per DEC-265), catalog, intelligence, crm, engagement, campaigns, deals, … |
| DEC-242 | 9.6a | Worker contract: Celery with a Redis-protocol broker (Valkey engine) and the four source … | ADR-101: Broker = Celery Redis transport (broker_url = redis://…, kombu Redis transport) against a Valkey server; both source statements are met; ADR-021 (as amended by DEC-167): Canonical queues include the four source queues … |
| DEC-243 | 9.6a | Deployment contract: ALB, ECS Fargate, ElastiCache, S3/CloudFront, Secrets Manager, … | ADR-013 / ADR-100 (Topology A): Pilot ingress = CloudFront → ALB (HTTPS) → ECS services; Cache/broker: ElastiCache (Valkey engine) — the ElastiCache service named by the source — replaces the self-run Valkey container at the … |
| DEC-244 | 9.6a | Pack planning figures recorded literally: 385 PD base allocation over 149 work items and … | Part 8.1 §8.1.6.4: Adds a “Pack planning envelope” line: 287–483 PD envelope; 385 PD base allocation for 149 work items, shared first-owned work counted once; labelled “editable planning estimate, not a team commitment”; Part … |
| DEC-245 | 9.6a | “lead/investor”, “investor/customer” and “issuer/company” read as disjunctions satisfied … | DEC-179 (Part 9.5): Re-based: the source text is kept verbatim in acceptance procedures and the UAT scripts, with a note “the investor alternative belongs to the separate investor product (DEC-058); this product satisfies the … |
| DEC-246 | 9.6a | No cross-region replication before approval: the approval is a signed Legal/Security … | DEC-164 / ADR-019: Cross-Region backup copy (and any later replication) is disabled in IaC by default; Data residency: Target region must be inside India unless a contract requires otherwise and the same approval covers it |
| DEC-247 | 9.6a | Six runtime AI responsibilities are the complete runtime taxonomy; every runtime agent … | Part 7.1 catalogue and Part 9.4 card field: New mandatory field runtime_responsibility ∈ {research, evidence/need, matching, content/draft, inbound intent, QA}; Deterministic boundary: Scoring, consent, sending and closure stay … |
| DEC-248 | 9.6a | Usage anomaly control: alerts at 70 % and 90 %, optional jobs paused at the cap, … | BRL-AI-08 / NT-025 (as amended by DEC-162): Text states the source rule literally first — “alert at 70 % and 90 % of the configured cap; pause optional jobs at the cap” — then the stricter blueprint steps (optional jobs already … |
| DEC-249 | 9.6a | Critical availability target 99.9 % over a rolling 30 days applies from the pilot as the … | DEC-157 (Part 9.5): OKPI-06 target = 99.9 % over a rolling 30 days from the pilot for the critical services listed in DEC-157 (2); Pilot reliability measures (no new infrastructure): Zero-downtime deploys on the single host … |
| DEC-250 | 9.6a | Routing decision adopted verbatim: legacy method/path canonical, new website endpoints … | Part 3.2 §3.2.2 path table: Every operation in the doc 07 register uses its legacy method and path verbatim (DEC-170); API-083 and every legacy /api/v1/public/…/{token} route: Access class changed from public to portal … |
| DEC-251 | 9.6a | Every read projection refreshes in ≤ 60 s (OKPI-28 applies to all projections); … | DEC-160 / NFR-047 (Part 4.2): F-2 is withdrawn for projections: every read projection, including RP-01…RP-21 dashboard aggregates, KPI tiles, attribution counts, SEO counts and cost roll-ups, has p95 ≤ 60 s from committed event … |
| DEC-252 | 9.6a | “Two products, four frontends” inspection performed literally over this product and the … | Part 6 E2E/acceptance pack (procedure “Independent products and frontends”): The deployment inventory lists two products and four frontends: this product's Website/Portal and Admin, and the investor product's two frontends as … |
| DEC-253 | 9.6a | Breakpoints adopted literally: desktop ≥ 1200, tablet 768–1199, mobile < 768; test … | Part 2.5 §2.48: Three canonical tiers: mobile < 768, tablet 768–1199, desktop ≥ 1200; DEC-043 (Part 0A): Admin is desktop-first from 1200 px (was 1280) and responsive at every tier: below 1200 the left nav collapses and the … |
| DEC-254 | 9.6a | Source inventory counts reproduced literally from the catalogue; blueprint extras … | Part 3.2 / 3.5 catalogue: Every source operation carries x-source-op (SM-OP-###) and x-source-class (retained-HTTP, retained-adapter, candidate); Part 3.3 / 3.6 entities: Same rule: 149 retained + 6 candidate = 155 source … |
| DEC-255 | 9.6a | Source contract decisions keep their literal IDs (document-qualified) and their proposed … | Decision queue (A-screen for contract decisions, Part 2.7) and RTM: Each source decision record stores source_doc (07 or 08) and source_decision_id exactly as printed (“DEC-001” … “DEC-042”); Content: Each of the 42 proposed … |
| DEC-256 | 9.6a | “claude/openai api” satisfied by the Claude API under B02; OpenAI kept as a disabled … | Part 7.3 provider table and Part 3.5 §3.5.5.6.4: Record “claude/openai api” carried verbatim; Prices: All model rates in the record are unverified for implementation: verify at time of implementation (as of 27 Nov 2026) … |
| DEC-257 | 9.6a | Calendar API and Zoom charged to B07/B10 shared optional with no new commitment ((a) … | Part 3.2 AD-03, AD-04, AD-18; DEC-020 text: Allocation = B07/B10 shared optional; no new commitment; Verification: Pricing/entitlement not individually verified; verify at time of implementation (as of 27 Nov 2026) |
| DEC-258 | 9.6a | Postiz kept as a self-hosted SocialPort candidate (B01/B10, no hosted subscription) with … | Part 3.2 AD-08 (SocialPort): Postiz listed as self-hosted candidate adapter, allocation B01/B10 shared; no hosted subscription; Plan: Evaluation spike in W3 (licence review, API fit, cost on B01); build of the adapter only if … |
| DEC-259 | 9.6a | PandaDoc included as an e-sign/proposal candidate (B07/B10 shared optional) where … | Part 3.2 AD-10 (ESignPort) and proposal builder: PandaDoc added to the evaluation shortlist with allocation B07/B10 shared optional; no new commitment |
| DEC-260 | 9.6a | Provider candidate register carries the seven source fields verbatim for every operation … | Part 3.5 §3.5.5.6.4 (register): Generated from docs 07/08/16 by script: one row per (operation or entity, provider) with the seven source fields verbatim plus disposition (approved runtime, optional shared B07/B10, developer aid … |
| DEC-261 | 9.6a | Developer plugins associated with screens and operations are recorded as build aids … | Part 2.7 screen cards and Part 3.5 register: Each listed screen card (A006, A008, A011, A014, A017, A029–A039, A047, A050–A059, A065, A066, A084, A090) and operation carries a “Build aids (development-time, B09)” line naming the … |
| DEC-262 | 9.6a | Unapproved commercial SaaS candidates kept as procurement-gated adapters: ₹0 committed, … | Part 3.2 ports (EnrichmentPort, SearchPort, SocialPort, AdsPort, ContentPort): Each provider is a procurement-gated candidate: allocation ₹0 committed; adapter not built until a procurement record exists (vendor, DPA, … |
| DEC-263 | 9.6a | Optional shared tools (PostHog, Canva, Figma, Postman) recorded with their source … | Part 3.5 register and Part 7.3: PostHog: optional analytics sink fed from the first-party beacon (API-291 stays the system of record); self-hosted in ap-south-1 or EU/US cloud only after DPDP cross-border review; consent-gated; … |
| DEC-264 | 9.6a | Offline example set (164 request, 164 invalid, 165 response) regenerated as contract … | Part 6 CT-04 fixtures: The fixture set contains, per explicit proposed contract, at least one valid request (164), one invalid request (164) and one response example (165), keyed to the same SM-OP IDs ASSUMPTION-523; labelled … |
| DEC-265 | 9.6a | Existing identity reused: AUTH_USER_MODEL and membership keys confirmed and mapped; no … | Part 3.3 ENT-006: Renamed “UserProfile (extension of AUTH_USER_MODEL)”, table accounts_user_profile (canonical, inside the reused accounts app, DEC-241), alias ten_user; Membership: Product membership rows FK to the existing … |
| DEC-266 | 9.6a | Embedding entity uses the source column names and type: model text, vector vector(1024); … | Part 3.3 ENT-026: Columns renamed to the source names: model text NOT NULL (alias model_id) and vector vector(1024) NOT NULL (alias embedding); Storage: Full-precision storage ≈ 4 KB per row (was ≈ 2 KB); at 1.6 M stock rows ≈ … |
| DEC-267 | 9.6a | Sequence step carries delay_seconds int ≥ 0 as the minimum delay; business-day cadence … | Part 3.3 ENT-101 eng_sequence_step: Add delay_seconds integer NOT NULL DEFAULT 0 CHECK (delay_seconds >= 0) |
| DEC-268 | 9.6a | sales_fulfillment implemented with all ten source columns as the fulfilment milestone … | Part 3.3 / 3.6 (ENT-ENH-E-03, canonical name sales_fulfillment, alias com_fulfillment_milestone): Columns: id uuid PK; tenant_id; startup_id; order_id uuid → order; line_id uuid → order line; milestone_key text; quantity … |
| DEC-269 | 9.6a | state column added to signature event, handoff and launch approval as the source … | ENT-132 com_signature_event: Add state text NOT NULL CHECK IN (requested, viewed, signed, declined, expired, voided) set at insert; signed_at becomes nullable with CHECK ((state = 'signed') = (signed_at IS NOT NULL)); ENT-149 … |
| DEC-270 | 9.6a | Prototype handoff rule: production uses authenticated services; browser storage is never … | Part 4.1 (session and storage rules): States the source sentence verbatim: no token, role, scope or approval state is trusted from localStorage/sessionStorage/IndexedDB; sessions are HttpOnly cookies via the BFF; any client-side … |
| DEC-300 | 9.6b | Cost routing contract (PC-13). PC-13 'Cost routing' carries the full document-15 typed … | Amends DEC-201 ('no model' → 'executor: Tier 0 deterministic; contract complete'); Part 7.4a §7.4.4 PC-13 row; Part 7.4b PC-13 table row (evaluation 'n/a' → seven source evaluations) |
| DEC-301 | 9.6b | Local model gateway first; paid models as allowance-gated fallback. (1) Gateway order: … | Amends DEC-007 (tier order; Claude becomes the paid fallback), DEC-192 (the reading 'local first = rules and cache first' is replaced), FR-ENH-F-030 (interpretation table), Part 7.3 gateway routing (Tier 0L inserted), … |
| DEC-302 | 9.6b | Classification and qualification precision ≥ 90% from the initial release. (1) For … | Amends DEC-196 (90% moves from W4 target to W1 acceptance for auto-accepted items); TC-ENH-F-013 expected result; Part 7.2 agent cards for classification/qualification agents (threshold τ field) |
| DEC-303 | 9.6b | Schema-valid outputs ≥ 99.5% with token percentiles. DEC-195 is confirmed and completed. … | Amends Part 7.3 §7.6.9 (gate text), TC-ENH-F-012, the Part 9.4 AI catalogue measurement columns |
| DEC-304 | 9.6b | Search: native sources first; hosted search API only after an approved shortfall. (1) … | Amends DEC-193 (Tavily free credits no longer secondary by default), AD-05/AD-06 activation state (Part 3.2), the B03 line (ceiling ₹1,500 unchanged; expected spend ₹0 until activation) |
| DEC-305 | 9.6b | Extraction: Scrapy + Trafilatura + HTTPX, Playwright for permitted JS pages. This is the … | Amends DEC-194 and ADR-018 (preferred implementation), Part 3.2 ExtractionPort adapters, Part 7.4b §7.4.5.8.6 |
| DEC-306 | 9.6b | Budget ladder 70 / 80 / 90 / 100. For every M53 cap (AI, provider, channel, per … | Amends DEC-162 (the pause moves from 90% to 100%; the 80% warning returns as a notification), BRL-AI-08, NT-025, ADR-083, Part 4.3 §4.46.4, RB-005 |
| DEC-307 | 9.6b | Envelope S: the retained pilot envelope ₹16,675. The source's operating budget register … | Amends DEC-198 (3) ('historical' → 'retained and tracked'); Part 8.4 §8.4.3.1 gains the Envelope S view; DEC-231 unchanged |
| DEC-308 | 9.6b | Observability without hosted Sentry or Datadog. Hosted Sentry is removed (browser and … | Supersedes DEC-200; amends DEC-041, ADR-058 and Part 4.3 §4.39.1 (Sentry node → local tracker; Prometheus/Grafana no longer optional), the B07 line content |
| DEC-309 | 9.6b | Apollo GraphQL (IC-270): both source records kept. The candidate register row for IC-270 … | Amends DEC-199 ('never a data source' → 'not activated; conditional licensed data only after verification'); F_integration_candidates.csv row IC-270 |
| DEC-310 | 9.6b | Recovery: initial and growth targets as the source states them. The source terms initial … | Amends DEC-158 (binding point), NFR-057, Part 4.2 §4.30, package I-8 (W6 → Release 1, together with DEC-315), Part 4.3 §4.47 drill schedule |
| DEC-311 | 9.6b | Coverage gates restated literally. DEC-203 is confirmed, and RGV gets these literal … | Amends DoD D-8, NFR-082 (as restated by DEC-203), CS-TEST-03, the RGV rule set (FR-ENH-I-060) |
| DEC-312 | 9.6b | Defect severity labels Critical/P0 … Low/P3. Defect severity values are 'Critical / P0', … | Amends DEC-205 and the §9.5.1.10.2 mapping table, Part 6.1 §6.1.8, Part 6.8c §6.8.5.1.3, the defect-tracker enumeration |
| DEC-313 | 9.6b | RTM business-requirement traces equal to document 24. Every FR row of the RTM gets a … | Amends Part 2.1 §2.4 (FR-W04, FR-W13…W20, FR-A023, FR-A025 BR columns), Part 6.6 RTM export, DEC-180 (CONFLICT-447 closure made explicit) |
| DEC-314 | 9.6b | Traceability approval: 100%, human, no synthetic approval. OKPI-20 = approved applicable … | Amends AP-08 (Part 6.6 §6.6.8.2), confirms DEC-203 (6), Part 6.9b §6.9.5.3.5 |
| DEC-315 | 9.6b | Capacity: source-exact initial and growth workloads and design points. (1) New canonical … | Amends DEC-161 (profiles and placement), Part 4.2 §4.25.1/§4.25.6, Part 4.4b LT-ENH-I-01/02, package I-8 placement (Part 9.5 §9.5.2.3) |
| DEC-316 | 9.6b | Traffic mix 60 / 20 / 10 / 10 for capacity runs. Every WP-01-S/WP-02-S run uses 60% … | Amends DEC-161 (4) (WP-03 becomes the default capacity mix, not only for dashboards), Part 4.2 §4.26 load-test table |
| DEC-317 | 9.6b | Spike 3× and burst 2×, each with its own acceptance. Two scenarios: SPK-3X: public … | Amends DEC-161 (3), Part 4.2 LT-05/LT-07, Part 4.4b LT-ENH-I-04 |
| DEC-318 | 9.6b | Endurance: 8 h soak at the initial target. LT-ENH-I-05 v2 runs 8 hours at WP-01-S (the … | Amends DEC-161 (5), Part 4.2 LT-02 |
| DEC-319 | 9.6b | Projection refresh ≤ 60 s for every scoped projection. (1) Every read projection derived … | Amends DEC-160 (F-2 class withdrawn as a 15-minute class; F-3 kept for period outputs), NFR-047, NFR-008 (unchanged value, wider scope), Part 2.4 §2.31.1, Part 4.4b §4.4.5.4.6, package J-8 |
| DEC-320 | 9.6b | Pack effort figures shown as gross, reconciled as the pack instructs. The planning … | Confirms DEC-181 and DEC-225; adds estimate register row EST-PACK-01 to Part 8.1 §8.1.6.4 (by reference) |
| DEC-321 | 9.6b | Queues named and configured as document 26 states. Canonical queue names: research, ai, … | Amends ADR-021, DEC-167, Part 3.1 containers C07/C08, Part 4.4b FR-ENH-I-030 |
| DEC-322 | 9.6b | Seven environments as document 27 lists them. Canonical environments: local, shared … | Amends DEC-166 ('no shared-dev' withdrawn; UAT split from staging), Part 3.1 §3.1.14, Part 4.3 §4.35, Part 4.4b §4.4.5.3.1 |
| DEC-323 | 9.6b | Security finding severity by business impact. Security findings use doc 30's … | Amends Part 4.1 §4.16.3 (primary scale), confirms DEC-168, Part 4.4b §4.4.5.5.2 |
| DEC-324 | 9.6b | 5xx alerts: both document 31 thresholds. AL-06: > 2% 5xx for 5 min with meaningful … | Amends DEC-165 (runbook text and tuning review), Part 4.3 §4.41 |
| DEC-325 | 9.6b | Availability: 99.9% internal target from Release 1; 99.5% contract negotiation target. … | Amends DEC-157 (start point R1 instead of scale gate, as target), NFR-053/054, SLO-01/02 (Part 4.3 §4.40.1) |
| DEC-326 | 9.6b | Service plans Self-service / Managed / Enterprise. The plan catalogue has three plans … | Amends DEC-047 (archetype names → size presets), DEC-210, FR-ENH-A-015, FR-ENH-J-007, Part 8.3 plan tables |
| DEC-327 | 9.6b | Support acknowledgement P1 15 min / P2 1 h / P3 next business day. For contracted SaaS … | Amends DEC-209 (the 3-month pre-condition is replaced by the source's feasibility evidence), DEC-044 (relabelled), Part 4.3 §4.45, Part 8.3c SLA-05 |
| DEC-328 | 9.6b | Combined preflight: 1,188 / six groups and 1,545 / nine groups, both enforced. A090 … | Amends DEC-206 (both counts enforced, not only 1,545), Part 8.3c §8.3.5.15.10, FR-ENH-I-060 (RGV) |
| DEC-329 | 9.6b | Business requirements: 76. The BR register header, Part 10 counts and the RTM read … | Amends DEC-180 count wording, Part 1 §1.4 register header (by reference), Part 9.2 glossary 'XBR' entry |
| DEC-330 | 9.6b | Optimization KPI IDs: the pack's IDs reproduced in the optimization register. The … | Amends DEC-178 (display rule), J-7 registry schema |
| DEC-331 | 9.6b | Candidate register: source decisions recorded literally (N/A re-check). IC-048 Carta CRM … | Amends F_integration_candidates.csv rows IC-048, IC-050, IC-486 (status N/A → Covered (aligned)); Part 7.4a register |
| DEC-332 | 9.6b | OPT-07-02 independent deployables (N/A re-check). OPT-07-02 'Keep independent … | Amends Part 4.4a §4.4.4.1 row I-OPT-031 (N/A → Covered (aligned)); adds RGV check RGV-ALN-04 |
| DEC-380 | 9.7b | Adopt the X1 advanced AI programme (22 agents, 27 automations, 9 workflows, 16 screens) … | Defines scope and gates G-X0, G-A1, G-A2, G-A3 (§9.7.3); nothing is built before approval |
| DEC-381 | 9.7b | Approve development budget for the proposal: A1 ₹7.1–22.6 L (central ₹13.2 L) plus D4 … | Staged release of money tied to measured value (§9.7.14.5) |
| DEC-382 | 9.7b | Create budget line B24 "Advanced AI" with hard caps ₹2,000/month (pilot), ₹7,500 (growth … | B02 and DEC-008 ceilings unchanged; advanced agents can never starve baseline agents (ADR-119) |
| DEC-383 | 9.7b | Predictive propensity (AU-056) and churn (AU-059) are advisory only: Admin-only display, … | Resolves CONFLICT-621; keeps DEC-011 binding |
| DEC-384 | 9.7b | Multi-agent orchestration follows supervisor-as-planner (ADR-110): AG-039 proposes; … | Resolves CONFLICT-620 with ADR-071 (extends, does not replace) |
| DEC-385 | 9.7b | Long-term memory (ADR-112) is OFF by default per tenant; enabling requires R01 + R10 and … | DPDP purpose limitation and erasure evidenced; AU-061/062 mandatory |
| DEC-386 | 9.7b | Conversation intelligence (AG-045) covers staff-written notes and in-product written … | Resolves CONFLICT-622; keeps the system out of EU AI Act Annex III employment use (verify) |
| DEC-387 | 9.7b | Voice assistant deferred (Won't for this horizon); re-evaluation in A3 only through … | No telephony spend; avoids conflict with DEC-218 |
| DEC-388 | 9.7b | Price-book guidance (AG-048) explains approved price versions and DEC-038 routes only; … | Safety invariant preserved |
| DEC-389 | 9.7b | Adopt open-source MLflow (self-hosted) for the ML registry and pull forward self-hosted … | Open-source first; data stays in region; enables multi-step trace debugging |
| DEC-390 | 9.8b | Adopt the X2 advanced revenue growth capabilities as a separately approvable proposal in … | Funds and schedules X2 per release; no change to Release 1/2 scope or budgets |
| DEC-391 | 9.8b | Forecast governance: categories Omitted / Pipeline / Best case / Commit / … | Accountable forecast with evidence (F21); consistent with BR-M60 and OPT-12-03 |
| DEC-392 | 9.8b | Cadence channels: LinkedIn steps are human tasks only (no automated messages, connection … | Multichannel cadences (F09) without new outbound automation risk; no change to the "no SMS or voice outreach in W0–W5" rule |
| DEC-393 | 9.8b | Partner audience: partners use a separate portal audience (sub-role R16P) with object … | Enables F13/F14 while keeping BR-WEB separation and data minimization |
| DEC-394 | 9.8b | Deal rooms and MAPs: rooms show only approved hashes to verified invited contacts with … | Enables F10/F11 within PP-06 and DEC-064 |
| DEC-395 | 9.8b | CPQ guardrails: quotes draw only from approved price-book revisions; no manual … | Enables F12; reaffirms "AI never sets prices" |
| DEC-396 | 9.8b | Customer health and surveys: health uses commercial and service data only (no patient, … | Enables F15/F18 consistent with BR-M50, DEC-030 and X-02 |
| DEC-397 | 9.8b | Attribution: the default reporting model stays last non-direct touch (AU-040); … | Enables F22/F23 consistent with SP-12 (first/last touch, window, unknown bucket) |
| DEC-398 | 9.8b | Healthy recognition: points only for verified outcomes and quality behaviours, never for … | Enables F27 consistent with PP-01 |
| DEC-399 | 9.8b | Paid tools and AI budget: optional paid tools (OPT-X2-01…06) stay OFF until a … | Keeps open-source first and the AI ceiling unchanged |
| DEC-400 | 9.9b | Approve the X3 package as a separate proposal outside DEC-230/231 and the Phase-2 … | Opens X3 budget lines; authorizes the X3 team (ASSUMPTION-700); new tables and APIs proceed under the doc 36 §5 "implementation approval" condition |
| DEC-401 | 9.9b | Analytics architecture: outbox-fed hourly Parquet lakehouse with DuckDB (ADR-130); a … | Affirms ADR-003; resolves CONFLICT-722 |
| DEC-402 | 9.9b | The semantic layer is the only path from AI or users to numbers; NLQ emits validated … | Protects RLS and ABAC-05; prevents invented metrics |
| DEC-403 | 9.9b | Allow a public developer platform with outbound webhooks from A3 (Year 2), Scale plan or … | Supersedes for Year 2 only the Part 3.2 note "Outbound webhooks to tenants: not offered in W0–W6"; resolves CONFLICT-721 |
| DEC-404 | 9.9b | Indic UI: Website/portal chrome in hi-IN, ta-IN and or-IN from A2 per startup when 100% … | Keeps DEC-026 for Admin; resolves CONFLICT-720 |
| DEC-405 | 9.9b | BYOK offered only on the Scale plan, keys in ap-south-1, with a signed tenant acceptance … | Enterprise enabler; fail-closed per tenant |
| DEC-406 | 9.9b | Status page and trust centre hosted outside the product account; incident text … | Closes GAP-126 and GAP-179 (adopts RECOMMENDATION-489) |
| DEC-407 | 9.9b | Autonomy for operations: L2 only for the protective, reversible, fail-closed set (pause … | Consistent with DEC-064 caps; resolves CONFLICT-726 |
| DEC-408 | 9.9b | SOC 2 / ISO 27001: continuous evidence from A2; an external audit only when an … | Keeps §4.12.10 "not a certification" position; trust-centre wording "SOC 2-aligned" |
| DEC-409 | 9.9b | X3 agents run within DEC-008 ceilings in the lowest AI priority class and degrade to … | No change to DEC-008; protects production AI |
| DEC-410 | 9.10 | Single owner for each overlapping capability, as listed in §9.10.4. AG-048 is merged … | Removes duplicated build (≈ 30–65 pd). The catalogue keeps AG-048 for traceability, marked "merged into AG-066" |
| DEC-411 | 9.10 | Advanced roadmap A1, A2, A3 with gates G-A0, G-A1 and G-A2 (§9.10.5). Releases 1 and 2 … | Advanced work starts only after W5 exit and only with an approved budget |
| DEC-412 | 9.10 | Release 1 literal-alignment work: fund as change request CR-ALN-01 (default), or accept … | Protects the 4 Jun 2027 date if funded |
| DEC-413 | 9.10 | Model routing after literal alignment (DEC-301): the source pack requires … | Routing order: Tier 0 rules and cache → local open model → Claude (Haiku-class, then Sonnet-class) within the per-tenant allowance, with redaction → free fallbacks (non-personal data only, off by default) → degrade. Safety … |
| DEC-414 | 9.10 | Advanced budget proposal: development ₹78.2–143.0 L for A1–A3 (A1 only ≈ ₹28.0–55.4 L); … | Nothing is spent on advanced work until approved |
| DEC-415 | 9.10 | Precedence after v1.1: Part 9.10 > Parts 9.6–9.9 > Part 9.5 §9.5.2.9 > Part 8.4 > Part … | Removes ambiguity between the v1.0 and v1.1 decisions |
| DEC-416 | 9.10 | DEC-412 approved: the Release 1 literal-alignment work is funded as change request … | CR-ALN-01 one-time development ₹2.79–11.64 L (central ₹6.09 L; 61.25 / 107.2 / 170.8 pd after the DEC-418 reduction). Recurring CR-ALN-02 up to ₹1,495–10,120/month, an upper bound now that DEC-418 removes the local-inference … |
| DEC-417 | 9.10 | DEC-414 approved for release A1. The one-time development budget for advanced release A1 … | Procurement of the A1 contract team (AI/LLM, data, SRE/security engineers; ASSUMPTION-700, ASSUMPTION-752) starts at the Release 2 build gate (Day 208). Gate G-A0 is satisfied for budget; the W5-exit condition still applies. A1 … |
| DEC-418 | 9.10 | DEC-413 resolved: Claude Sonnet stays the primary model. DEC-301 is superseded. The … | Literal match: two aspects become Founder-approved deviations. F15-052 (doc 15: paid AI only as a conditional fallback) and F21-015 (doc 21: local model gateway in front of the paid tier). The result is 11,129 / 11,131 = 99.98% … |
| DEC-419 | 9.10 | Build-time tooling approved as recommended in the Cost Estimate v1.0 (§7). Claude Max 5x … | ≈ $821–857 per month (₹73,890–77,094) during the build, in addition to Ledger B (DEC-231); about $6.6–6.9k (₹5.9–6.2 L) over the 8 core build months. After the build, seats fall to the maintenance team. Prices are list prices; … |
| DEC-420 | 9.10 | AI-built delivery approach adopted, with a Sprint 2 calibration gate (Cost Estimate … | Tooling: AI-built tooling replaces the Claude part of DEC-419 (Claude Max 20x for 5 engineers, Pro × 3, CI sandboxes, self-hosted agent observability). Total ≈ $1,336–1,527 per month (₹1.20–1.37 L), about $475–630 more than … |
| DEC-421 | 9.10 | Hosting stack: Vercel + Supabase + AWS ap-south-1 (Mumbai), replacing the AWS-only … | Running cost (pilot hosting): Vercel ₹1,800–3,600 + Supabase ₹3,600–5,400 + AWS ₹2,700–4,050 + DR storage ₹300–600 = ₹8,400–13,650 per month, against ₹6,600–9,400 for the AWS-only lines B01/B20/B21. That is ≈ ₹1,800–4,250 more … |

<!-- GEN:DEC:END -->

---

## 9.2.5 Duplicate-ID check

### 9.2.5.1 Script findings (same ID, different meaning in different parts)

The script compares every ID defined (first cell of a table row) in more than one part. It flags pairs whose meanings share almost no vocabulary, aggregated per ID family. Two families it flags are excluded after reading because the meaning is the same: OQ-### (Part 0A answers the Part 0 questions under short labels) and EP-## (Part 6 test-case batches list risk areas per epic in their coverage tables). Tags issued in two batches with the same meaning (ASSUMPTION-146, GAP-143, RECOMMENDATION-004, -035, -061) are restatements, not duplicates.

<!-- GEN:DUPS:BEGIN -->

| Kind | ID | Part A | Meaning in A | Part B | Meaning in B |
|---|---|---|---|---|---|
| Tag | CONFLICT-300 | Part 2.6 | Two opportunity scoring models | Part 9.5 | DEC-211 |
| Tag | CONFLICT-301 | Part 2.6 | Residual investor/fundraising wording in group A documents | Part 9.5 | DEC-179 |
| Tag | CONFLICT-302 | Part 2.6 | Definition of source coverage | Part 9.5 | DEC-212 |
| Tag | CONFLICT-303 | Part 2.6 | Reply classification taxonomy | Part 9.5 | DEC-213 |
| Tag | CONFLICT-304 | Part 2.6 | Single relationship stage vs separate state machines | Part 9.5 | DEC-214 |
| Tag | CONFLICT-320 | Part 3.4 | Deployment technology: ECS Fargate + ALB + ElastiCache Redis + "Redis broker" | Part 9.5 | DEC-163 |
| Tag | CONFLICT-321 | Part 3.4 | Capacity design points: initial 25 owned / 10 external; growth 50+ / 100 | Part 9.5 | DEC-161 |
| Tag | CONFLICT-322 | Part 3.4 | Growth RTO ≤ 2 h | Part 9.5 | DEC-158 |
| Tag | CONFLICT-323 | Part 3.4 | Availability "99.9% critical availability over rolling 30 days" | Part 9.5 | DEC-157 |
| Tag | CONFLICT-324 | Part 3.4 | Budget alert thresholds 70/90% | Part 9.5 | DEC-162 |
| Tag | CONFLICT-325 | Part 3.4 | "No cross-region replication before approval" | Part 9.5 | DEC-164 |
| Tag | CONFLICT-326 | Part 3.4 | Investor-product wording: "lead/investor record", "investor/customer tokens", "investment/commercial Django … | Part 9.5 | DEC-179 |
| Tag | CONFLICT-327 | Part 3.4 | Agent decomposition: "six runtime responsibilities" vs 18 responsibilities vs blueprint catalogue | Part 9.5 | DEC-183 |
| Tag | CONFLICT-328 | Part 3.4 | Effort and critical path: 385 PD base for 149 work items; dependency-only path 113.5 days | Part 9.5 | DEC-181 |
| Tag | CONFLICT-329 | Part 3.4 | Names: Django apps (accounts, catalog, …, reporting) and monorepo paths (apps/growth-ui, …) | Part 9.5 | DEC-183 |
| Tag | CONFLICT-330 | Part 3.4 | Product webhook into the marketing database vs "no live cross-product join or automatic handoff" | Part 9.5 | DEC-169 |
| Tag | CONFLICT-340 | Part 2.7a | Residual investor wording not in DEC-002's replacement list: "separate from investor/customer journey" … | Part 9.5 | DEC-179 |
| Tag | CONFLICT-341 | Part 2.7a | "Inspect … two products, four frontends" vs DEC-009 "two frontends only" | Part 9.5 | DEC-169 |
| Tag | CONFLICT-342 | Part 2.7a | Breakpoints: doc 17 desktop ≥ 1200, tablet 768–1199, mobile < 768, tests at 360/768/1440; Part 2.5 §2.48 … | Part 9.5 | DEC-215 |
| Tag | CONFLICT-343 | Part 2.7a | API namespaces: doc 06 uses /api/v1/sales/* (A099–A106) and … | Part 9.5 | DEC-170 |
| Tag | CONFLICT-344 | Part 2.7a | Generic POST …/{id}/control (12 resources) vs per-action endpoints in Part 3.2 (approve, issue, cancel, … | Part 9.5 | DEC-171 |
| Tag | CONFLICT-345 | Part 2.7a | Legacy per-object approve/review routes (e.g. /contracts/{id}/approve, /proposals/{id}/review, … | Part 9.5 | DEC-172 |
| Tag | CONFLICT-346 | Part 2.7a | Development-time Claude plugins (for example CLAUDE.md Management, Claude Code Setup, Plugin Developer … | Part 9.5 | DEC-202 |
| Tag | CONFLICT-347 | Part 2.7a | Doc 06 states provider prices as facts (for example a per-million-token rate for a named Claude model, … | Part 9.5 | DEC-202 |
| Tag | CONFLICT-348 | Part 2.7a | OPT-02-04 "read projections refresh ≤ 60 s" vs NFR-047 dashboards ≤ 15 min (A110 monitor ≤ 5 min) | Part 9.5 | DEC-160 |
| Tag | CONFLICT-349 | Part 2.7a | Scale figures: OPT-06-01 "25 owned + 10 external initial; 50+ owned + 100 external growth"; dashboard … | Part 9.5 | DEC-161 |
| Tag | GAP-143 | Part 7.1 | No lawful meeting-recording or transcript source exists; meeting summarization is excluded until one is … | Part 9.5 | Narrowed by DEC-218 |
| Tag | GAP-366 | Part 3.5b | The "catalog-complete OpenAPI draft" and the 164/164/165 offline examples are not in the package | Part 9.6a | Closed by DEC-264 |
| Tag | RECOMMENDATION-090 | Part 6.6 | Recommendation (Batch 6.7) | Part 6.7 | Store every VER item's evidence as an EVR of type review/inspection/analysis/demonstration and extend … |
| Tag | RECOMMENDATION-369 | Part 3.5b | Exclude reverse-IP visitor identification and third-party analytics on public pages; keep the first-party … | Part 9.6a | Superseded by DEC-262 (procurement gate instead of exclusion) |
| ADR | ADR-021 | Part 3.1 | Queue topology and priorities | Part 9.5 | Amended by DEC-167 (control and finance queues) |
| ADR | ADR-101 | Part 3.4 | Valkey as broker and cache engine | Part 9.6a | Broker = Celery Redis transport (broker_url = redis://…, kombu Redis transport) against a Valkey server; … |
| Registry | AD-01…AD-12 (12 IDs) | Part 3.1 | e.g. AD-01 = Tenant and startup isolation | Part 3.2 | e.g. AD-01 = Amazon SES (EmailPort) |
| Registry | AG-049…AG-053 (3 IDs) | Part 9.4 | e.g. AG-049 = Personalization-at-Scale Variant Generator | Part 9.7b | e.g. AG-049 = / AG-050 Variants and localization Draft approved-claim content |
| Registry | B-11…B-13 (3 IDs) | Part 3.1 | e.g. B-11 = KMS customer-managed keys | Part 9.5 | e.g. B-11 = Regression matrix: remaining scenarios (US-18-EB03 part) |
| Registry | C-1…C-8 (8 IDs) | Part 3.3 | e.g. C-1 = Provision workspace from template + capability profile W0 | Part 6.9b | e.g. C-1 = Bulk-action preview QC-082 |
| Registry | C-1…C-7 (7 IDs) | Part 3.3 | e.g. C-1 = Provision workspace from template + capability profile W0 | Part 9.5 | e.g. C-1 = Optimization Intelligence panel as the UI of the J scorecard (US-17-EC01, half) |
| Registry | CAP-01…CAP-10 (10 IDs) | Part 2.1 | e.g. CAP-01 = Tenancy, identity and access | Part 3.4 | e.g. CAP-01 = Owned startups / external tenants |
| Registry | D-1…D-4 (4 IDs) | Part 3.3 | e.g. D-1 = Automated snapshot restore Weekly + every release (NFR-012) | Part 5.1a | e.g. D-1 = Code |
| Registry | D-1…D-4 (4 IDs) | Part 3.3 | e.g. D-1 = Automated snapshot restore Weekly + every release (NFR-012) | Part 9.5 | e.g. D-1 = Contract approval gate and evidence (US-21-ED01, merged with H-2) |
| Registry | D-5…D-16 (12 IDs) | Part 5.1a | e.g. D-5 = Isolation tests | Part 9.5 | e.g. D-5 = Adapter command/result envelope with budget reservation (US-01-ED02) |
| Registry | E-2…E-7 (6 IDs) | Part 2.2 | e.g. E-2 = State change, audit append, budget reservation and outbox insert happen in one database transaction | Part 9.5 | e.g. E-2 = Service request entity and flow (US-20-EE01; replaces H story) |
| Registry | G-1…G-4 (4 IDs) | Part 6.9b | e.g. G-1 = Decision approvals (baseline) 180 | Part 9.5 | e.g. G-1 = Operation-contract class harness (17 classes), execution-status field, SM-UT-037/049/050 |
| Registry | J-10…J-15 (3 IDs) | Part 1 | e.g. J-10 = Reply to meeting | Part 9.5 | e.g. J-10 = SLA schedule (US-20-EJ01) |
| Registry | L-01…L-06 (6 IDs) | Part 1 | e.g. L-01 = Statutory GST e-invoice (IRN) integration | Part 3.5b | e.g. L-01 = Every operation (API-###, API-ENH-D-###) has an OpenAPI x-contract-state; CI blocks a merge that … |
| Registry | LT-01…LT-11 (9 IDs) | Part 4.2 | e.g. LT-01 = Baseline API mix | Part 6.1 | e.g. LT-01 = Admin mixed API load |
| Registry | PP-01…PP-07 (7 IDs) | Part 1 | e.g. PP-01 = Outcomes over activity. Measure qualified opportunities, meetings, awards, fulfilment, … | Part 6.2a | e.g. PP-01 = Admin API (SYS) Deployed build in test; BFF session (audience growth-engine, client … |
| Registry | V-01…V-14 (14 IDs) | Part 3.3 | e.g. V-01 = File SHA-256 not previously imported for this template (UQ-IDEM-18) | Part 6.9b | e.g. V-01 = A required QC ID missing from the submission set |
| Registry | WF-13 | Part 2.2 | e.g. WF-13 = M55, B-AUTO | Part 9.4 | e.g. WF-13 = Autonomous plan |
| Registry | WF-15…WF-23 (9 IDs) | Part 9.4 | e.g. WF-15 = Supervised multi-agent account pursuit | Part 9.7b | e.g. WF-15 = Workflow wiring, simulation fixtures and end-to-end test |
| Registry | X-1…X-3 (3 IDs) | Part 9.5 | e.g. X-1 = Absolute discounts with effective-% approval routing (DEC-208) | Part 9.8b | e.g. X-1 = Agent prompts, schemas, evals for AG-061…070 (AU-006 suites) all |

<!-- GEN:DUPS:END -->

### 9.2.5.2 Analysis and proposed handling

| # | Collision | Evidence | Risk | Proposed handling (for a Part 9.1 errata decision) |
|---|---|---|---|---|
| 1 | **AD-01…12**: architecture drivers (Part 3.1 §3.1.1) vs adapter directory rows (Part 3.2 §3.2.4) | Script finding above | A trace "AD-05" is ambiguous (low run cost vs Tavily adapter) | Rename the Part 3.2 rows to **ADP-01…12** (adapter); keep AD- for drivers |
| 2 | **LT-01…12**: load tests in Part 4.2 vs Part 6.1 with different scenarios | Script finding; DEC-092 already gives Part 6.1 ownership | Part 4.2 LT- references point to the wrong test | Already decided by **DEC-092**; Part 4.2 LT rows are superseded. No new action beyond the Part 10 cross-reference note |
| 3 | **PP-01…07**: product principles (Part 1 §1.3) vs test pre-condition profiles (Part 6.2a §6.2.1) | Script finding | A test row "Pre: PP-01" reads as "Outcomes over activity" | Rename the Part 6 profiles to **PCP-01…07** (pre-condition profile) in Parts 6.2–6.6 |
| 4 | **D-1…D-4**: DR drills (Part 3.3 §3.3.19) vs Definition-of-Done items (Part 5.1a) | Script finding | Low (different contexts), but D- also clashes with dimension codes D1–D8 | Rename Part 3.3 drills to **DRL-1…4** or map them onto Part 6.1 **DR-1…8** |
| 5 | **B##** budget lines (B01–B23, DEC-020) vs **B-##** scale-cost rows (Part 3.1 §3.1.6) | Manual review | Reader may sum B-01 into budget line B01 | Rename the Part 3.1 rows to **SCL-01…** |
| 6 | **P##** personas vs **P-##** pilot cost rows (Part 3.1 §3.1.6.2) and priority labels P0–P2 (Part 6) | Manual review | Low | Keep; formats differ (two digits vs hyphen vs one digit) |
| 7 | **CA-<code>** acceptance profiles (Part 2.1) vs **CA-R#** Canada rules (Part 4.1) | Manual review | Low | Keep; letter code vs R-number; cite "CASL CA-R#" in prose |
| 8 | **E-##** errata (Part 9.1) vs **E-#** engine invariants (Part 2.2) | Manual review | Low | Keep; formats differ |
| 9 | **TC-AI-AG###-##** (DEC-093) vs **TC-AI-AG###-###** (three-digit suffix, Parts 6.1 and 6.3a) | Registry scan | Test IDs not matching the DEC-093 pattern fail ID validation in the RTM | **Resolved by DEC-113**: TC-AI-AG###-### and TC-AU-AU###-### govern. No further action |
| 10 | **CI-###** candidate AI ideas (Part 7.1) vs **CI** (continuous integration) and incident examples such as CI-0007 | Manual review | Low | Keep; four-digit incident IDs are fixture data |

None of the tag IDs (ASSUMPTION/GAP/CONFLICT/RECOMMENDATION) is used with two different meanings. Items 2 (DEC-092) and 9 (DEC-113) are already decided. Items 1, 3, 4 and 5 need errata decisions; they are logged as [GAP-181] for the Part 9.1 owner.

---

## 9.2.6 Document map

Every part file, its contents (top-level sections, excluding tag registers and quality gates), the rendered page count (`pdfinfo`), the number of Mermaid diagrams and the word count. "In progress" means the file had no closing Status line when the script ran.

<!-- GEN:DOCMAP:BEGIN -->

| Part | File | Title | Contents (top-level sections) | Pages | Diagrams | Words | State |
|---|---|---|---|---|---|---|---|
| 0 | Part-00_Document_Ingestion_and_Validation.md | PART 0, Document Ingestion and Validation | Ingestion record; Summary of understanding (under 400 words); Requirements inventory; Gaps register (GAP-###): missing information; Conflicts register (CONFLICT-###): where documents or sections contradict; Ambiguities (to resolve via assumptions or questions); Assumptions register (ASSUMPTION-###); … (+4) | 33 | 0 | 9,962 | Complete |
| 0A | Part-00A_Issue_Resolution_Decisions.md | PART 0A, Issue Resolution and Decision Log | A. Decision principles applied; B. Corrections of probable human errors in the source documents; C. Resolution of gaps; D. Resolution of ambiguities; E. Answers to the open questions (delegated); F. Additional corrections found on a second reading; G. Updated registers (summary) | 16 | 0 | 4,741 | Complete |
| 0B | Part-00B_Source_Pack_Coverage_Report.md | PART 0B, Source Pack (38 Documents) Coverage Report | B.1 What the source pack is and what it is telling us; B.2 How the review was done; B.3 Overall result; B.4 Coverage by document; B.5 Coverage by reviewer group; B.6 Residual items without a recorded action; B.7 Final position after enhancement and literal alignment (Part 9.6a/b); … (+1) | 9 | 0 | 2,423 | Complete |
| 1 | Part-01_Product_and_Business_Foundation.md | PART 1, Product and Business Foundation | Executive summary (draft for the final document); Vision, mission and product principles; Problem statement; Goals, KPIs and OKRs; Scope; Release structure: delivery waves and MoSCoW; Stakeholders; … (+7) | 49 | 0 | 15,168 | Complete |
| 2.1 | Part-02-1_Functional_Design_Modules_and_FR_Register.md | PART 2 (Batch 2.1), Functional Design: Capability Map, Module Catalogue and Functional Requirement Register | Capability map; Module catalogue (66 source modules); Common acceptance profiles (applied to every FR); Functional requirement register | 49 | 1 | 13,140 | Complete |
| 2.2 | Part-02-2_Functional_Design_Process_Flows.md | PART 2 (Batch 2.2), End-to-End Process Flows | Universal execution engine (applies to every flow below); WF-01 Startup catalogue (product truth); WF-02 Market discovery; WF-03 Professional contacts; WF-04 Inbound acquisition; WF-05 Content and campaign; WF-06 Outreach and replies; … (+11) | 44 | 22 | 4,901 | Complete |
| 2.3 | Part-02-3_Business_Rules_RBAC_State_Machines.md | PART 2 (Batch 2.3), Business Rules Catalogue, Roles and Permissions (RBAC/ABAC), State Machines | Business rules catalogue (BRL); Roles and permissions; State machines; Coverage and consistency checks | 47 | 17 | 10,783 | Complete |
| 2.4 | Part-02-4_Cross_Cutting_Functions.md | PART 2 (Batch 2.4), Cross-Cutting Functions: Notifications, Reporting & Analytics, Search, Configuration & Administration, Audit Trail, Multi-Tenancy, Localization | Notifications; Reporting and analytics; Search; Configuration and administration; Audit trail; Multi-tenancy; Localization and internationalization; … (+1) | 26 | 2 | 7,149 | Complete |
| 2.5 | Part-02-5_UX_UI_Design.md | PART 2 (Batch 2.5), UX/UI Design | UX principles; Information architecture; Global shell and navigation (Admin); Layout patterns; Screen inventory (147) with wireframe-level descriptions; Key wireframes; Design system; … (+5) | 31 | 1 | 9,373 | Complete |
| 2.6 | Part-02-6_Source_Pack_Business_Domain_Enhancements.md | PART 2 (Batch 2.6), Source Pack Business Domain Enhancements | Documents reviewed; Coverage register summary; Detailed coverage register; Catalogue reconciliation; Enhancements; Conflicts and proposed resolutions; Expert persona review; … (+1) | 125 | 6 | 36,897 | Complete |
| 2.7a | Part-02-7a_Source_Pack_UI_Catalog_and_UX_Enhancements.md | PART 2 (Batch 2.7a), Source Pack UI Catalog and UX Enhancements | Documents reviewed; Coverage register summary; Detailed coverage register; Catalogue reconciliation; Enhancements; Conflicts and proposed resolutions; Expert persona review; … (+1) | 66 | 2 | 21,800 | Complete |
| 2.7b | Part-02-7b_Source_Pack_UI_Catalog_and_UX_Enhancements.md | PART 2 (Batch 2.7b), Source Pack UI Catalog: Per-Screen Contract Cards (147 screens) | How to read the screen contract cards; Website: public pages; Website: intake forms; Portal and SaaS client; Admin: global shell; Admin: Overview view; Admin: Discovery view; … (+6) | 289 | 0 | 94,155 | Complete |
| 3.1 | Part-03-1_Architecture.md | PART 3 (Batch 3.1), Architecture: Principles, C4 Views, Deployment, Runtime Views, Technology Stack, ADRs, Capacity, HA/DR and Environments | Architecture principles and drivers; System context (C4 level 1); Container view (C4 level 2); Component views (C4 level 3) of the Django modular monolith; Logical view; Deployment view (AWS ap-south-1); Runtime views; … (+8) | 82 | 19 | 22,066 | Complete |
| 3.2 | Part-03-2_API_and_Integration.md | PART 3 (Batch 3.2), API and Integration Design: Standards, Derived API Catalogue, Event Catalogue, Adapter Catalogue, Contract Testing and Cross-Role Review | API design standards; Derived API catalogue (DERIVED, DEC-015); Event catalogue; Integration patterns and adapter catalogue; Contract testing approach RECOMMENDATION-034; Webhook ingestion and reconciliation patterns; Outbound retry, back-off and circuit-breaker parameters RECOMMENDATION-031; … (+1) | 88 | 2 | 33,683 | Complete |
| 3.3 | Part-03-3_Data_Architecture.md | PART 3 (Batch 3.3), Data Architecture | Scope, sources and conventions of this batch; Conceptual data model; Entity catalogue and reconciliation; Logical data model (per domain); Physical model conventions (FRD §5); Data dictionary: core entities (column level); Compact dictionary: remaining 131 entities; … (+13) | 146 | 20 | 46,656 | Complete |
| 3.4 | Part-03-4_Source_Pack_Architecture_and_Workflow_Enhancements.md | PART 3 (Batch 3.4), Source Pack Review: Architecture, Delivery and Workflow Enhancements (documents 04, 05, 09, 10) | Documents reviewed; Coverage register summary; Detailed coverage register; Catalogue reconciliation; Enhancements; Conflicts and proposed resolutions; Expert persona review; … (+1) | 112 | 6 | 36,928 | Complete |
| 3.5a | Part-03-5a_Source_Pack_API_Catalog_Reconciliation.md | PART 3 (Batch 3.5a), Source Pack API Catalog Reconciliation: Document 07 Review, Coverage Register and Operation Mapping | Documents reviewed; Coverage register summary; Detailed coverage register; Catalogue reconciliation | 44 | 0 | 14,874 | Complete |
| 3.5b | Part-03-5b_Source_Pack_API_Catalog_Reconciliation.md | PART 3 (Batch 3.5b), Source Pack API Catalog Reconciliation: Enhancements, Field Contracts, Adapters, Conflicts and Tests | Enhancements; Conflicts and proposed resolutions; Expert persona review; Tags register (Batch 3.5, files a and b) | 96 | 2 | 44,789 | Complete |
| 3.6a | Part-03-6a_Source_Pack_Data_Catalog_Reconciliation.md | PART 3 (Batch 3.6a), Source Pack Data Catalog Reconciliation: Documents, Coverage and Catalogue Mapping | How to read this batch; Documents reviewed; Coverage register summary; Detailed coverage register (prose aspects); Catalogue reconciliation | 49 | 0 | 18,029 | Complete |
| 3.6b | Part-03-6b_Source_Pack_Data_Catalog_Reconciliation.md | PART 3 (Batch 3.6b), Source Pack Data Catalog Reconciliation: Enhancements, Governance, Migration and DR | Enhancements; Conflicts and proposed resolutions; Expert persona review; Tags register (380…399) | 42 | 2 | 13,792 | Complete |
| 4.1 | Part-04-1_Security_and_Compliance.md | PART 4 (Batch 4.1), Security, Privacy and Regulatory Compliance | Security architecture overview; Threat model (STRIDE); Authentication; Authorization; Cryptography and encryption; Secrets management and key rotation; Security control catalogue (SC-##); … (+12) | 76 | 3 | 22,072 | Complete |
| 4.2 | Part-04-2_Non_Functional_Requirements.md | PART 4 (Batch 4.2), Non-Functional Requirements, Capacity and Load Profiles | Measurement conventions; NFR catalogue, part A: refined NFR-001…NFR-038 (from Part 0 §0.3.3); NFR catalogue, part B: new NFR-039…NFR-099; Latency budgets by endpoint class; Capacity and load profiles; Load and resilience test catalogue; Scalability triggers (when to scale or re-architect); … (+3) | 34 | 1 | 9,605 | Complete |
| 4.3 | Part-04-3_DevOps_and_Operations.md | PART 4 (Batch 4.3), DevOps, Release Engineering, Observability and Operations | Repository strategy; Infrastructure as code; Environments and data seeding; Feature flags (RECOMMENDATION-005); Release strategy and database migrations; Rollback strategy; Observability architecture (DEC-041, RECOMMENDATION-006); … (+10) | 50 | 5 | 13,412 | Complete |
| 4.4a | Part-04-4a_Source_Pack_Security_DevOps_Operations_Enhancements.md | PART 4 (Batch 4.4a), Source Pack Review: Security, DevOps, Operations Enhancements and Coding Standards | Documents reviewed; Coverage register summary; Detailed coverage register; Catalogue reconciliation; Enhancements | 73 | 2 | 22,102 | Complete |
| 4.4b | Part-04-4b_Source_Pack_Security_DevOps_Operations_Enhancements.md | PART 4 (Batch 4.4b), Source Pack Review: Security, DevOps, Operations Enhancements (continued), Conflicts and Registers | Enhancements (continued); Conflicts and proposed resolutions; Expert persona review; Tags register | 42 | 3 | 13,803 | Complete |
| 5.1a | Part-05-1a_Epics_Stories_Foundation.md | PART 5 (Batch 5.1a), Epics and User Stories: Front Matter (Purpose, DoR, DoD, INVEST, Estimation, Dimension Matrix, Conventions) | Purpose and structure of Part 5; Definition of Ready (DoR); Definition of Done (DoD); INVEST guidance with examples; Estimation basis; Dimension matrix and coverage rationale; Story-writing conventions (recap, binding on batches 5.1–5.3) | 21 | 0 | 7,948 | Complete |
| 5.1b | Part-05-1b_Epics_Stories_Foundation.md | PART 5 (Batch 5.1b), Epics and User Stories: EP-01 to EP-04 (Foundation, Product Truth, Governance, AI Gateway) | Epics and stories: EP-01 to EP-07 | 70 | 0 | 24,793 | Complete |
| 5.1c | Part-05-1c_Epics_Stories_Foundation.md | PART 5 (Batch 5.1c), Epics and User Stories: EP-05 to EP-07 (Discovery, Qualification, CRM) and Batch 5.1 Coverage | Epics and stories (continued): EP-05 to EP-07 | 61 | 0 | 21,068 | Complete |
| 5.2 | Part-05-2_Epics_Stories_Engagement_and_Commerce.md | PART 5 (Batch 5.2), Epics and User Stories: Engagement and Commerce (EP-08 to EP-14) | Introduction and scope of this batch; EP-08 Messaging: drafting, email, inbound, sequences, omnichannel; EP-09 Meetings, webinars and demos; EP-10 WhatsApp and website assistant; EP-11 Content, SEO and social publishing; EP-12 Campaigns, landing pages, ads and referrals; EP-13 Proposal, quote, negotiation and contract; … (+4) | 84 | 0 | 31,217 | Complete |
| 5.3 | Part-05-3_Epics_Stories_Closure_Automation_Web_SaaS.md | PART 5 (Batch 5.3), Epics and User Stories: Closure, Lifecycle, Command Centre, Automation, Website, SaaS and Release Readiness | Introduction to Batch 5.3; EP-15 Payment, closure, revenue and attribution; EP-16 Onboarding, retention, partners and expansion pilots; EP-17 Dashboards, forecast and Command Centre; EP-18 Workflow, autonomy and automation engine; EP-19 Public website and external portal; EP-20 SaaS client lifecycle and portability; … (+3) | 111 | 0 | 40,008 | Complete |
| 6.1 | Part-06-1_Test_Strategy.md | PART 6 (Batch 6.1), Test Strategy | Purpose, scope and principles; Test levels; Test types; Risk-based prioritization; Entry and exit criteria; Test environments; Test data strategy; … (+8) | 88 | 6 | 32,945 | Complete |
| 6.2a | Part-06-2a_Test_Cases_EP08-EP11.md | PART 6 (Batch 6.2, file a), Test Scenarios and Test Cases: EP-08 to EP-11 | Purpose, inputs and how to read the test cases; EP-08 Messaging: drafting, email, inbound, sequences, omnichannel; EP-09 Meetings, webinars and demos; EP-10 WhatsApp and website assistant; EP-11 Content, SEO and social publishing; Coverage and totals for file a (EP-08 to EP-11) | 102 | 1 | 33,209 | Complete |
| 6.2b | Part-06-2b_Test_Cases_EP12-EP14.md | PART 6 (Batch 6.2, file b), Test Scenarios and Test Cases: EP-12 to EP-14 | Inputs for file b; EP-12 Campaigns, landing pages, ads and referrals; EP-13 Proposal, quote, negotiation and contract; EP-14 Bids, orders and fulfilment (vertical routes); Coverage and totals for file b (EP-12 to EP-14); Batch 6.2 totals, register and inconsistencies (files a and b) | 75 | 0 | 24,216 | Complete |
| 6.3a | Part-06-3a_Test_Cases_EP15-EP18.md | PART 6 (Batch 6.3a), Test Scenarios and Test Cases: EP-15 to EP-18 | How to read this batch; EP-15 Payment, closure, revenue and attribution; EP-16 Onboarding, retention, partners and expansion pilots; EP-17 Dashboards, forecast and Command Centre; EP-18 Workflow, autonomy and automation engine; Coverage and totals for EP-15 to EP-18 | 62 | 0 | 36,659 | Complete |
| 6.3b | Part-06-3b_Test_Cases_EP19-EP21.md | PART 6 (Batch 6.3b), Test Scenarios and Test Cases: EP-19 to EP-21, Acceptance Procedures and Release Drills | EP-19 Public website and external portal; EP-20 SaaS client lifecycle and portability; EP-21 Release readiness, QA and observability; Acceptance procedure scripts AP-01, AP-04, AP-06, AP-09 and AP-10; Coverage and totals for EP-19 to EP-21; Batch roll-up: EP-15 to EP-21 (files a and b); Tags register (Batch 6.3, files a and b); … (+1) | 65 | 0 | 27,356 | Complete |
| 6.4 | Part-06-4_AI_Evaluation_Test_Cases.md | PART 6 (Batch 6.4), AI Evaluation Test Cases | Purpose, scope and conventions; Evaluation datasets; Acceptance thresholds per agent; Shared oracles, harness and fault model; Agent evaluation cases; Cross-model regression across the fallback chain; Regression-gate rules (BRL-AI-09, NFR-033, DEC-061); … (+8) | 169 | 5 | 72,424 | Complete |
| 6.5 | Part-06-5_Test_Cases_EP01-EP07.md | PART 6 (Batch 6.5), Test Scenarios and Test Cases: EP-01 to EP-07 | How to read this batch; EP-01 Platform foundation, identity reuse and tenancy; EP-02 Product truth and knowledge; EP-03 Consent, privacy, eligibility and compliance; EP-04 AI gateway, cost control and AI quality; EP-05 Market intelligence and discovery; EP-06 Opportunity scoring, contacts and research review; … (+2) | 160 | 2 | 60,859 | Complete |
| 6.6 | Part-06-6_Requirements_Traceability_Matrix.md | PART 6 (Batch 6.6), Requirements Traceability Matrix | Method; Coverage summary (generated); (a) BR → FR → US → TC (generated); (b) FR → US → TC for all 150 interface and operation FRs (generated); (d) NFR → test (generated); (e) BRL rule → TC coverage summary (generated); (f) AG/AU → TC-AI/TC-AU (generated); … (+5) | 131 | 0 | 45,838 | Complete |
| 6.7 | Part-06-7_NFR_and_Coverage_Closure_Test_Cases.md | PART 6 (Batch 6.7), NFR and Coverage Closure Test Cases | Purpose, conventions and coverage rule; NFR test cases TC-NFR-001…099; NFR production verification items (VER-001…022); Parameterized filter suite TC-FLT-001…045 (FR-FLT-01…11, FR-FLT-RULES); Supplementary business requirement (BR-S) closure; Coverage closure tables; RTM generator update and regenerated coverage; … (+1) | 66 | 1 | 24,349 | Complete |
| 6.8a | Part-06-8a_Source_Pack_Test_Specification_Reconciliation.md | PART 6 (Batch 6.8a), Source Pack Test Specification Reconciliation: Documents, Coverage Summary and Detailed Register | Documents reviewed; Coverage register summary; Detailed coverage register | 23 | 0 | 7,689 | Complete |
| 6.8b | Part-06-8b_Source_Pack_Test_Specification_Reconciliation.md | PART 6 (Batch 6.8b), Source Pack Test Specification Reconciliation: Catalogue Reconciliation (799 Source Tests → Blueprint TCs) | Catalogue reconciliation | 68 | 1 | 20,179 | Complete |
| 6.8c | Part-06-8c_Source_Pack_Test_Specification_Reconciliation.md | PART 6 (Batch 6.8c), Source Pack Test Specification Reconciliation: Enhancements, Conflicts and Decisions | Enhancements; Conflicts and proposed resolutions; Expert persona review; Tags register | 25 | 1 | 8,910 | Complete |
| 6.9a | Part-06-9a_Source_Pack_QC_RTM_and_Backlog_Reconciliation.md | PART 6 (Batch 6.9a), Source Pack Reconciliation: Quality Controls, Requirements Traceability and Delivery Backlog (Review and Catalogue Reconciliation) | Documents reviewed; Coverage register summary; Detailed coverage register; Catalogue reconciliation | 71 | 1 | 24,308 | Complete |
| 6.9b | Part-06-9b_Source_Pack_QC_RTM_and_Backlog_Reconciliation.md | PART 6 (Batch 6.9b), Source Pack Reconciliation: Quality Controls, Requirements Traceability and Delivery Backlog (Enhancements, Conflicts and Sign-off) | Enhancements; Conflicts and proposed resolutions; Expert persona review; Tags register | 59 | 5 | 19,707 | Complete |
| 6.10 | Part-06-10_Source_Pack_Coverage_Closure.md | PART 6 (Batch 6.10), Source Pack Coverage Closure | Purpose and method; Coverage closure map; Closure test cases: source-pack requirements (FR-ENH, NFR-ENH); Closure test cases: source-pack stories; Closure items: quality controls (QC, source document 23); Traceability supplement for existing source-pack tests; Coverage after closure; … (+1) | 29 | 1 | 8,339 | Complete |
| 7.1 | Part-07-1_AI_Discovery_and_Catalogue.md | PART 7 (Batch 7.1), AI Agents and Automations: Discovery Method and Catalogue | Discovery method (client spec 7.1, with the work shown) | 33 | 1 | 11,152 | Complete |
| 7.2 | Part-07-2_AI_Agent_Specifications.md | PART 7 (Batch 7.2), AI Agent and Automation Specifications and Multi-Agent Orchestration | Specification table; Agent detail cards; Automation specifications (AU, deterministic, Tier 0); Tool registry (DEC-048); Multi-agent orchestration design: overview; Shared memory and state; Inter-agent protocol; … (+5) | 49 | 4 | 25,335 | Complete |
| 7.3 | Part-07-3_AI_Model_Strategy_Cost_Governance.md | PART 7 (Batch 7.3), AI Model Strategy, Routing and Fallback, Cost Optimization, Subscriptions and TCO, AI Governance, Cross-Role Review | Model strategy, routing and fallback; Cost optimization for the paid model (quantified); Subscriptions, tooling and total cost of ownership; AI governance and safeguards; Cross-role review (client spec Section 9) and red-team of the catalogue; Registers for Part 7 | 34 | 2 | 12,612 | Complete |
| 7.4a | Part-07-4a_Source_Pack_AI_Plugin_and_Cost_Enhancements.md | PART 7 (Batch 7.4a), Source Pack Review: AI Agents, Prompts and RAG; Plugins, APIs, Open Source and Cost; Paid-Plugin Replacement (Coverage and Reconciliation) | Documents reviewed; Coverage register summary; Detailed coverage register; Catalogue reconciliation | 59 | 0 | 20,449 | Complete |
| 7.4b | Part-07-4b_Source_Pack_AI_Plugin_and_Cost_Enhancements.md | PART 7 (Batch 7.4b), Source Pack Enhancements: Prompt Contracts, RAG, New Agents and Automations, Automation Library, Integration Procurement, Replacement Economics and Budget | Enhancements; Conflicts and proposed resolutions; Expert persona review; Tags register (Part 7.4a and 7.4b) | 54 | 5 | 17,708 | Complete |
| 8.1 | Part-08-1_Roadmap_Releases_Sprints.md | PART 8 (Batch 8.1), Delivery Plan: Roadmap, Releases, Sprint Plans, Team and RACI, Estimation, Critical Path | Purpose, inputs and planning baseline; Phased roadmap; Release plan; Sprint plans; Team composition, QA gap, UAT and RACI; Estimation method and effort ranges; Critical path and external dependencies; … (+1) | 54 | 3 | 17,878 | Complete |
| 8.2 | Part-08-2_Risks_Change_GoLive_Hypercare.md | PART 8 (Batch 8.2), Delivery Plan: Risk Register, Change Management and Training, Operational Readiness, Go-Live Checklist, Hypercare, KPI Tracking and Budget | Risk register; Change management and training; Operational readiness: DR and support model for go-live (errata 16, 17, 43); Go-live checklist; Hypercare plan ASSUMPTION-206 RECOMMENDATION-089; Post-launch KPI tracking (KPI-01…KPI-31); Budget summary (estimates); … (+1) | 44 | 1 | 14,988 | Complete |
| 8.3a | Part-08-3a_Source_Pack_Training_SaaS_Maintenance_Optimization_Enhancements.md | PART 8 (Batch 8.3a), Source Pack Review: Training, SaaS Service Operations, Maintenance and Optimization (Documents 33–36, 38): Documents Reviewed, Coverage Register and Catalogue Reconciliation | Documents reviewed; Coverage register summary; Detailed coverage register; Catalogue reconciliation | 52 | 0 | 16,605 | Complete |
| 8.3b | Part-08-3b_Source_Pack_Training_SaaS_Maintenance_Optimization_Enhancements.md | PART 8 (Batch 8.3b), Source Pack Enhancements I: Operational Training Manual by Persona and Screen | Enhancements (organized by blueprint part) | 59 | 2 | 18,500 | Complete |
| 8.3c | Part-08-3c_Source_Pack_Training_SaaS_Maintenance_Optimization_Enhancements.md | PART 8 (Batch 8.3c), Source Pack Enhancements II: SaaS Service Operations and SLA, Maintenance Lifecycle, Optimization Model; Conflicts, Persona Review, Tags and Quality Gate | Conflicts and proposed resolutions; Expert persona review; Tags register | 67 | 3 | 22,173 | Complete |
| 8.4 | Part-08-4_Cost_Model_Development_vs_Subscriptions.md | PART 8 (Batch 8.4), Cost Model: Development Cost Separated from Subscription and Running Costs | The two ledgers at a glance; Ledger A: development cost (one-time); Ledger B: subscription and running cost (recurring); Combined view and scale; Decision | 10 | 0 | 3,146 | Complete |
| 9.1 | Part-09-1_Errata_and_Consolidated_Decisions.md | PART 9 (Batch 9.1), Errata Register and Consolidated Decisions | Errata decisions; Effect on earlier decisions; Additional errata decisions (second review cycle); Final errata decisions (third review cycle) | 13 | 0 | 3,757 | Complete |
| 9.3 | Part-09-3_Final_Quality_Report.md | PART 9 (Batch 9.3), Final Quality Report and Cross-Role Review | Success criteria assessment (client Section 2); Traceability coverage (from the regenerated RTM); Blueprint inventory (final); Cross-role review (client Section 9): final red-team; Residual open items requiring owner action (not blockers to start); Statement of completeness; Source-pack update (v1.1): full 38-document review; … (+1) | 11 | 0 | 3,433 | Complete |
| 9.4 | Part-09-4_AI_Agents_Automations_Workflows_Catalogue.md | PART 9 (Batch 9.4), Catalogue of Workflows, AI Agents and Automations | Summary; Business workflows (WF-01…WF-39); AI agents (AG) and their functionality; Automations (AU) and their functionality; How they fit together | 40 | 1 | 19,436 | Complete |
| 9.5 | Part-09-5_Source_Pack_Decisions_and_Replan.md | PART 9 (Batch 9.5), Source Pack Decisions and Re-plan after Enhancements | Decision summary for the Founder; Binding decisions DEC-157 onwards; Re-plan after enhancements; Tags register (allocated ranges ASSUMPTION-500…509, RECOMMENDATION-500…509); Inconsistencies found while writing this part (reported, not changed) | 64 | 1 | 19,196 | Complete |
| 9.6a | Part-09-6a_Source_Pack_Literal_Alignment.md | PART 9 (Batch 9.6a), Source Pack Literal Alignment (groups A–E) | .1 Scope and method; .2 Summary; .3 Alignment register (conflict rows); .4 Not-applicable re-check; .5 Decisions DEC-234…DEC-270; .6 Test cases; .7 Effort and impact; … (+1) | 79 | 1 | 28,727 | Complete |
| 9.6b | Part-09-6b_Source_Pack_Literal_Alignment.md | PART 9 (Batch 9.6b), Source Pack Literal Alignment (groups F–J) | .1 Scope and method; .2 Summary: counts by alignment type and by group, before and after; .3 The alignment register; .4 Not-applicable re-check; .5 Decisions; .6 Test cases; .7 Effort and cost impact; … (+1) | 113 | 3 | 33,486 | Complete |
| 9.7a | Part-09-7a_Advanced_AI_Agents_and_Intelligence.md | PART 9 (Batch 9.7a), Advanced AI Agents and Intelligence | Expert panel; Opportunity inventory; Improvement plan; Agent architecture uplift; Agent specification cards (AG-039…AG-060) | 66 | 7 | 21,789 | Complete |
| 9.7b | Part-09-7b_Advanced_AI_Agents_and_Intelligence.md | PART 9 (Batch 9.7b), Advanced AI Agents and Intelligence | Automations table (AU-053…AU-079); Workflows (WF-15…WF-23); Functional requirements (FR-ADV-X1-001…064); User stories (US- -V1nn); Data, API and screen additions; Test and evaluation cases (TC-ADV-X1-001…092); Governance; … (+5) | 91 | 13 | 27,456 | Complete |
| 9.8a | Part-09-8a_Advanced_Revenue_Growth_Capabilities.md | PART 9 (Batch 9.8), Advanced Revenue Growth Capabilities | Expert panel; Opportunity inventory; Improvement plan; Feature specifications | 59 | 3 | 18,312 | Complete |
| 9.8b | Part-09-8b_Advanced_Revenue_Growth_Capabilities.md | PART 9 (Batch 9.8), Advanced Revenue Growth Capabilities | Agent specification cards (AG-061…AG-070); Automations table (AU-080…AU-099); Workflows (WF-25…WF-32); Functional requirements (FR-ADV-X2-001…096); User stories (US-&lt;EP&gt;-V201…V232); Test cases (TC-ADV-X2-001…104); New business KPIs (KPI-ADV-X2-01…20); … (+5) | 86 | 8 | 27,417 | Complete |
| 9.9a | Part-09-9a_Advanced_Platform_Data_Security_Experience.md | PART 9 (Batch 9.9), Advanced Platform, Data, Security and Experience | Expert panel; Opportunity inventory; Improvement plan; Architecture uplift; Capability specifications | 56 | 4 | 15,979 | In progress (no Status line) |
| 9.9b | Part-09-9b_Advanced_Platform_Data_Security_Experience.md | PART 9 (Batch 9.9), Advanced Platform, Data, Security and Experience (continued) | Agent specification cards (AG-071…080); Automations (AU-100…119); Workflows (WF-33…39); Functional requirements (FR-ADV-X3-001…080); User stories (US- -V3nn); Test cases (TC-ADV-X3-001…062); Effort; … (+4) | 63 | 7 | 20,532 | Complete |
| 9.10 | Part-09-10_Revision_v1.1_Consolidation.md | PART 9 (Batch 9.10), Revision v1.1 Consolidation: 100% Literal Match, Expert Panels and Advanced Capabilities Plan | What revision v1.1 does; Expert panels (who was used, and for what); Identified advanced capabilities and AI agents (the list); Overlaps between panels and how they were resolved; Improvement plan (roadmap); Effort; Cost: separately approvable proposals (approved budgets DEC-230/231 unchanged); … (+4) | 20 | 1 | 6,272 | Complete |
| 9.2 | Part-09-2_Glossary_and_Registers.md | PART 9 (Batch 9.2), Appendices: Glossary, ID Registry and Consolidated Registers | Generation method and controls; Glossary; ID registry; Tag numbers issued, by issuing part; Consolidated registers; Duplicate-ID check; Document map | 189 | 1 | 62,181 | Complete |

**Totals:** 4,723 pages across 70 rendered PDFs; 211 Mermaid diagrams; 1,602,843 words.

<!-- GEN:DOCMAP:END -->

---

## 9.2.7 Tags issued in this batch

| Tag | Statement | Where used | Owner / closure |
|---|---|---|---|
| [ASSUMPTION-210] | Register statements are copied from the issuing part's own register row; when a tag has no register row, the text of its first-use line is used. The issuing part stays authoritative | §9.2.0, §9.2.4 | BSA; re-run the script after any part changes |
| [ASSUMPTION-211] | Resolution and acceptance status is derived by rule: DEC citation in Part 0A/9.1, the Part 0A §G summary, or the issuing register row's own wording. A tag not covered by these is "Open" or "Proposed" | §9.2.0, §9.2.4(c), (d) | Product Owner confirms at Part 10 assembly |
| [ASSUMPTION-212] | Page counts are those of the PDFs present at build time, rendered with `make_pdf.sh` (A4 landscape); re-rendering changes them | §9.2.6 | Part 10 assembly recomputes |
| [ASSUMPTION-213] | Glossary "first use" is the first textual occurrence of the key in reading order, outside code fences; acronyms are matched case-sensitively, phrases case-insensitively | §9.2.1 | BSA |
| [ASSUMPTION-214] | ID ranges count every mention, including citations; synthetic fixture identifiers inside Gherkin and test data are not ID families | §9.2.0, §9.2.2 | QA Lead |
| [GAP-180] | No central tag-allocation log exists; the per-part allocation in §9.2.3 is reconstructed from issued numbers, so unused allocated numbers cannot be told apart from lost ones | §9.2.3 | Programme owner: keep an allocation table in the Part 10 front matter |
| [GAP-181] | ID-family collisions AD- (3.1 vs 3.2), PP- (1 vs 6.2), D- (3.3 vs 5.1a) and B-/B## (3.1 vs budget lines) have no errata decision yet (TC-AI width settled by DEC-113, LT- by DEC-092) | §9.2.5.2 | Part 9.1 owner: issue DEC-141 onwards |
| [GAP-182] | Most RECOMMENDATION tags issued after Part 0 had no recorded accept/reject decision | §9.2.4(d) | **Closed** by DEC-149 (001…090) and DEC-221 (300…491); the regenerated register shows every recommendation as accepted unless a DEC rejects it (none does) |

---

## 9.2.8 Quality gate: Batch 9.2

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Glossary definitions cite DEC/ADR/BRL/NFR/BR/tag IDs; registers carry the issuing part and first-seen section |
| 2 | Assumptions, gaps and conflicts tagged and logged | Pass | ASSUMPTION-210…214 and GAP-180…182 issued and registered in §9.2.7; no CONFLICT or RECOMMENDATION issued (none allocated) |
| 3 | IDs unique and consistent with earlier parts | Pass with findings | Duplicate-ID check run (§9.2.5). No tag duplicates. Family collisions found and logged as GAP-181 with proposed renames; earlier parts not edited (brief boundary) |
| 4 | No story lacks AC and no requirement lacks a test | N/A | Appendix batch; no stories or requirements issued |
| 5 | Negative, edge, security and accessibility cases covered | N/A | No test design in this batch. Tables use text only; colour is not used to carry meaning (WCAG 1.4.1) |
| 6 | No agent lacks guardrail, fallback, KPI and cost estimate | N/A | No agents defined |
| 7 | Time-sensitive facts flagged "verify" with an as-of date | Pass | Regulatory entries (DPDP, CERT-In, TCCCPR, EU AI Act, ZDR) carry "verify, as of 27 Nov 2026"; no prices stated |
| 8 | No restricted data routed to free-tier models | Pass | Glossary restates DEC-007 and BRL-AI-06; no routing defined here |
| 9 | Consistent with earlier parts | Pass | Statements copied from the issuing parts; Part 9.1 and Part 9.5 overrides recorded in the DEC index (DEC-001…233) and ADR note; v1.1 adds the source-pack ID families, 36 source-pack glossary terms, the Part 9.5 conflict index (all 144 conflicts resolved) and the recommendation rule of DEC-149/DEC-221 (211 accepted, 0 rejected). Mermaid diagram renders; `pdftotext … \| grep -ci "diagram error"` = 0 |

**Status: Part 9 Batch 9.2 complete (v1.1, regenerated after the source-pack enhancement parts and Part 9.5). Glossary (358 terms, 36 of them source-pack terms), ID registry (154 families, incl. FR-ENH, NFR-ENH, US-##-E##, TC-ENH, LT-ENH, VER, OKPI, QC/QCL, SPDEC, SRC07-DEC, SDEC-08, SM-* aliases, RC, WP, PC, PG, SLA, CSO, MNT, TRN-SCR/TRN-EX), registers ASSUMPTION 200 · GAP 205 · CONFLICT 144 (all resolved) · RECOMMENDATION 211 (all accepted, none rejected), ADR index 80, DEC index 228 (DEC-001…233), duplicate-ID check and document map generated from all 59 part files (Parts 0–9.5). Next: Part 10 assembly.**
