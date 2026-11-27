# AI Growth Engine: Employee Sales & Marketing Automation
## Application Blueprint: PART 2 (Batch 2.7b), Source Pack UI Catalog: Per-Screen Contract Cards (147 screens)

| Field | Value |
|---|---|
| Document | Application Blueprint · Part 2.7 (Batch 2.7b of 2; companion to Batch 2.7a) |
| Version | 1.0 · 27 Nov 2026 |
| Baseline | Source pack documents 06 (UI Screen, Filter, API and Table Catalog) and 17 (Unified Command Centre UI/UX and Interaction Design); FRD §11, §16.2; Parts 2.1, 2.5, 3.2, 3.3, 6.1 |
| Roles applied | Lead UX/UI Designer, Frontend Lead, Accessibility Specialist, Business Systems Analyst (BSA) |

---

## 2.7.10 How to read the screen contract cards

Each of the 147 interfaces has one card. A card reconciles, row by row, what documents 06 and 17 declare for the screen against the blueprint, and closes every gap found by the parser `assembly/source_pack/C_parse_ui_catalog.py` (Batch 2.7a §2.7.4). The cards are **binding field contracts** for frontend, API serializer and test design: they complete Part 2.5 §2.43 (which delegates field lists to Part 2.1) and Part 2.1 §2.4 (which lists only the standardized and added fields). [GAP-340 closed here]

| Card block | Content | Source → blueprint rule |
|---|---|---|
| Header table | Surface, Command Centre view, layout pattern (Part 2.5), legacy screen ID (doc 06 "existing NNN"), build class, doc 06 location class, FR, wave and epic, acceptance profiles | Legacy ID per FR-ENH-C-001; build class per FR-ENH-C-014 |
| Filters | Filter families FR-FLT-01…11 that apply on the screen | [ASSUMPTION-343]; vertical families appear only when the selected startup's capability profile enables them (DEC-052) |
| Actions and automation | Doc 06/17 automation statement and Part 2.5 key actions | Every action is permission-checked server-side (CA-ADMIN/CA-PORTAL) |
| Field contract | Every field from doc 06 "Current declared fields" (origin **B** = retained baseline) and "Add or standardize" (origin **A**); replace rules from "Remove / replace" (origin **R**) | Type, control and validation inferred by rule set R-FLD [ASSUMPTION-341]; data dictionary Part 3.3 §3.3.6 prevails on conflict |
| Field status | **C** = already named in Part 2.1 key fields or Part 2.5 regions; **P** = baseline field the blueprint did not name, now specified by this card; **N/A** = layout-only | Parser tokens ≥ 50% match |
| Legacy operations | Every method/path doc 06 names for the screen, with the blueprint API ID(s) | **C** exact; **P** equivalent DERIVED path (alias route required, FR-ENH-C-003); **N** no equivalent (new alias or DERIVED op required, §2.7.5.3 of Batch 2.7a) |
| Tables | Every source table (growth_/sales_ prefix) mapped to blueprint ENT and physical table | **C** suffix match; **P** judged synonym; **N** no entity (GAP-349) |
| Integrations | Doc 06 plugin/provider associations, classified INT/OSS/ADP/CMU/DEV | §2.7.5.6 of Batch 2.7a; prices "verify at time of implementation (as of 27 Nov 2026)" |
| Tests | SM-UAT-S (doc 06 implementation table), SM-UX-UAT, SM-UT families, and the new conformance test TC-ENH-C-1nn | Alias rules of Part 6.1 §6.1.12.5 verified mechanically (counts identical) |
| Related screens | Doc 06 "Related" list = required in-context navigation links that keep scope (FR-ENH-C-012) | Part 2.5 rows mention only 3 of 435 links |

**Field-type rule set R-FLD (summary).** Hash → `char(64)` read-only; ID/reference → server-generated identifier; money words → Decimal + ISO 4217 (CA-FIN, DEC-027); currency → ISO 4217 allowlist; quantity/unit → QuantityInput; dates/deadlines → UTC timestamp with time-zone display; status/state/stage → state-machine enum, transition only (Part 2.3); email → encrypted with HMAC lookup; consent/permission → consent record with policy revision; geography → ISO 3166; language → BCP 47 (DEC-026); people → scoped user picker; score/confidence → computed, Unknown ≠ 0 (FR-UIS-02); revision → optimistic concurrency; approval → Approval chip (CA-APPROVE); evidence/source → citation chip; entity names → scoped FK lookup; free text → bounded text area. [ASSUMPTION-341]

## 2.7.11 Website: public pages

### 2.7.11.1 W01: Business growth platform homepage

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website public · PP-HOME |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W01 (alias SM-FR-W01, trace B-WEB, SM-UX-FR-W01) · W2 · EP-19 · CA-ALL, CA-PUB |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Render approved tenant-specific homepage and acquisition CTA |
| Key actions (Part 2.5) | Search businesses, Explore startup, Start as a client |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W02; W04; W12; W21; W31 |
| Tests | SM-UAT-S001; SM-UX-UAT-W01; unit families 001, 002, 010, 011, 012, 013, 015, 020, 021, 022, 023, 024, 030, 046; **TC-ENH-C-101** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contextual / display layout | B | N/A | Layout only | Published page blocks | No data field; content from approved snapshot |
| 2 | Language | A | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 3 | Region | A | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 4 | Business search | A | C | Query parameter | Search box / sort select | Allowlisted fields; server-validated |
| 5 | SaaS client entry | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 6 | Accessibility preferences | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/public/site/pages/{slug}` | P | API-290 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P)

### 2.7.11.2 W02: Company and startup business directory

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website public · PP-CATALOG |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W02 (alias SM-FR-W02, trace B-WEB; B-TENANT, SM-UX-FR-W02) · W2 · EP-19 · CA-ALL, CA-PUB |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Load published business directory dynamically |
| Key actions (Part 2.5) | Open startup site |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W03; W04; W31 |
| Tests | SM-UAT-S002; SM-UX-UAT-W02; unit families 001, 002, 003, 008, 009, 010, 011, 012, 013, 030, 045; **TC-ENH-C-102** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Sector | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Country | B | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 3 | Business capability | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Offering search | A | C | Query parameter | Search box / sort select | Allowlisted fields; server-validated |
| 5 | Location | A | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 6 | Sort | A | C | Query parameter | Search box / sort select | Allowlisted fields; server-validated |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/public/site/pages/{slug}` | P | API-290;API-486 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P)

### 2.7.11.3 W03: Individual startup website

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website public · PP-HOME |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W03 (alias SM-FR-W03, trace B-WEB; B-TENANT, SM-UX-FR-W03) · W2 · EP-19 · CA-ALL, CA-PUB |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Render approved business-specific site |
| Key actions (Part 2.5) | Explore offerings, Contact, Book a meeting |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W04; W12; W13 |
| Tests | SM-UAT-S003; SM-UX-UAT-W03; unit families 001, 002, 010, 011, 012, 013, 015, 020, 021, 022, 023, 024, 030, 046; **TC-ENH-C-103** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contextual / display layout | B | N/A | Layout only | Published page blocks | No data field; content from approved snapshot |
| 2 | Brand identity | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 3 | Business units | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Published offerings | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 5 | Contact channel | A | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 6 | Last updated | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/public/site/pages/{slug}` | P | API-290;API-486 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P)

### 2.7.11.4 W04: Product, service and programme catalog

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website public · PP-CATALOG |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W04 (alias SM-FR-W04, trace B-WEB; B-TENANT, SM-UX-FR-W04) · W2 · EP-19 · CA-ALL, CA-PUB |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Filter approved offering catalog by availability and capability |
| Key actions (Part 2.5) | View details, Request quote/demo |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W05; W06; W13 |
| Tests | SM-UAT-S004; SM-UX-UAT-W04; unit families 001, 002, 010, 011, 012, 013, 030; **TC-ENH-C-104** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Startup | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | derive site context when locked. Must belong to the same tenant and startup (composite FK) |
| 2 | Business line | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Delivery model | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 5 | Category | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 6 | Availability | A | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 7 | Region | A | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 8 | Price currency | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 9 | Search | A | C | Query parameter | Search box / sort select | Allowlisted fields; server-validated |
| 10 | Sort | A | C | Query parameter | Search box / sort select | Allowlisted fields; server-validated |

*Replace rules (doc 06 "Remove / replace"):* Startup: derive site context when locked.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/public/site/pages/{slug}` | P | API-290;API-486 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P)

### 2.7.11.5 W05: Product, service or programme details

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website public · PP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W05 (alias SM-FR-W05, trace B-WEB, SM-UX-FR-W05) · W2 · EP-19 · CA-ALL, CA-PUB |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Show approved details; route eligible enquiry |
| Key actions (Part 2.5) | Enquire, Request quote, Book demo |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W06; W13; W14 |
| Tests | SM-UAT-S005; SM-UX-UAT-W05; unit families 001, 002, 010, 011, 012, 013, 030; **TC-ENH-C-105** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contextual / display layout | B | N/A | Layout only | Published page blocks | No data field; content from approved snapshot |
| 2 | Offering revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 3 | Price basis | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 4 | Eligibility | A | C | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 5 | Availability | A | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 6 | Request type | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/public/site/pages/{slug}` | P | API-290;API-486 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P)

### 2.7.11.6 W06: Approved pricing and commercial packages

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public / Portal |
| Command Centre view · pattern (Part 2.5) | Website public · PP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W06 (alias SM-FR-W06, trace B-WEB, SM-UX-FR-W06) · W3 · EP-19 · CA-ALL, CA-PUB, CA-PORTAL, CA-FIN |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Render current approved prices and expiry |
| Key actions (Part 2.5) | Request quote, Log in |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W14; W23 |
| Tests | SM-UAT-S006; SM-UX-UAT-W06; unit families 001, 002, 010, 011, 012, 013, 030, 056, 057, 058, 059, 066; **TC-ENH-C-106** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Currency | B+R | C | ISO 4217 code | Select (allowed currencies) | allowed pricing currency only. Allowlist per startup TaxProfile (DEC-027) |
| 3 | Price revision | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 4 | Tax inclusion | A | C | TaxProfile / tax line reference | Read-only computed line | Per DEC-027; server-computed |
| 5 | Validity period | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |
| 6 | Region | A | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 7 | Request quote | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |

*Replace rules (doc 06 "Remove / replace"):* Currency: allowed pricing currency only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/public/site/pages/{slug}` | P | API-290;API-486 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P)

### 2.7.11.7 W07: Industry and business solution pages

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website public · PP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W07 (alias SM-FR-W07, trace B-WEB, SM-UX-FR-W07) · W3 · EP-19 · CA-ALL, CA-PUB |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Match industry to approved solutions |
| Key actions (Part 2.5) | Enquire |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W05; W12 |
| Tests | SM-UAT-S007; SM-UX-UAT-W07; unit families 001, 002, 010, 011, 012, 013, 030; **TC-ENH-C-107** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Industry | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 2 | Offering | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | dynamic published list. Must belong to the same tenant and startup (composite FK) |
| 3 | Use case | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Solution capability | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Geography | A | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 6 | Business outcome evidence | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |

*Replace rules (doc 06 "Remove / replace"):* Offering: dynamic published list.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/public/site/pages/{slug}` | P | API-290;API-486 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P)

### 2.7.11.8 W08: Blog, articles and knowledge centre

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website public · PP-ARTICLE |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W08 (alias SM-FR-W08, trace B-WEB, SM-UX-FR-W08) · W3 · EP-11 · CA-ALL, CA-PUB |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Serve approved content and permitted updates |
| Key actions (Part 2.5) | Read, Share, Enquire |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W07; W12 |
| Tests | SM-UAT-S008; SM-UX-UAT-W08; unit families 001, 002, 010, 011, 012, 013, 028, 029, 030, 031, 032; **TC-ENH-C-108** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Topic | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 2 | Language | B+R | C | BCP 47 tag | Select (enabled locales) | available translations only. DEC-026 enabled locales only |
| 3 | Search | A | C | Query parameter | Search box / sort select | Allowlisted fields; server-validated |
| 4 | Content type | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 5 | Published date | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 6 | Evidence revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |

*Replace rules (doc 06 "Remove / replace"):* Language: available translations only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/public/site/pages/{slug}` | P | API-290;API-486 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P)

### 2.7.11.9 W09: Case studies, testimonials and business evidence

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website public · PP-ARTICLE |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W09 (alias SM-FR-W09, trace B-WEB, SM-UX-FR-W09) · W3 · EP-11 · CA-ALL, CA-PUB |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Only publish authorized claims and case evidence |
| Key actions (Part 2.5) | Enquire |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W05; W13 |
| Tests | SM-UAT-S009; SM-UX-UAT-W09; unit families 001, 002, 004, 010, 011, 012, 013, 023, 030, 042; **TC-ENH-C-109** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Industry | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 2 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Evidence reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 4 | Publication permission | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 5 | Date | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 6 | Outcome context | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/public/site/pages/{slug}` | P | API-290;API-486 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P)

### 2.7.11.10 W10: Campaign landing pages

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website public · PP-HOME + PP-FORM |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W10 (alias SM-FR-W10, trace M37; B-WEB, SM-UX-FR-W10) · W3 · EP-12 · CA-ALL, CA-PUB, CA-INTAKE |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Route qualified leads with campaign attribution |
| Key actions (Part 2.5) | Submit enquiry |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W13; W19; W04 |
| Tests | SM-UAT-S010; SM-UX-UAT-W10; unit families 001, 002, 010, 011, 012, 013, 030, 060, 061, 062, 063, 064; **TC-ENH-C-110** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contextual / display layout | B | N/A | Layout only | Published page blocks | No data field; content from approved snapshot |
| 2 | Campaign attribution ID | A | C | Attribution ID / event reference | Read-only text | First-party only; captured server-side |
| 3 | Locale | A | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 4 | Offer expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 5 | Consent notice | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 6 | CTA | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/pages/{slug}` | C | API-290 | exact |
| POST | `/api/v1/public/events` | C | API-291 | exact |

**Tables → blueprint entities:** `growth_attribution_event` → ENT-124 `mkt_attribution_event` (C); `growth_content_version` → ENT-106 `mkt_content_version` (P); `growth_form` → ENT-080 `crm_form` (C); `growth_landing_page` → ENT-111 `mkt_landing_page` (C)

### 2.7.11.11 W11: AI website chat assistant

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website public · PP-CHAT |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W11 (alias SM-FR-W11, trace M32; B-WEB, SM-UX-FR-W11) · W3 · EP-10 · CA-ALL, CA-PUB, CA-INTAKE, CA-AI |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Ground responses; route unresolved questions |
| Key actions (Part 2.5) | Ask, Request human, Share details |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W12; W13; W04 |
| Tests | SM-UAT-S011; SM-UX-UAT-W11; unit families 001, 002, 004, 023, 028, 029, 030, 031, 032, 042; **TC-ENH-C-111** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contextual / display layout | B | N/A | Layout only | Published page blocks | No data field; content from approved snapshot |
| 2 | Session ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 3 | Language | A | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 4 | Knowledge revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 5 | Consent | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 6 | Human handover | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 7 | Evidence links | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/public/chat` | C | API-246 | exact |

**Tables → blueprint entities:** `growth_chat_session` → ENT-099 `eng_chat_session` (C); `growth_lead` → ENT-079 `crm_lead` (C); `growth_message` → ENT-093 `eng_message` (C); `growth_thread` → ENT-092 `eng_thread` (C)

### 2.7.11.12 W30: Contact, privacy, terms and help centre

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public / Portal |
| Command Centre view · pattern (Part 2.5) | Website public · PP-ARTICLE + PP-FORM |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W30 (alias SM-FR-W30, trace M22; B-WEB, SM-UX-FR-W30) · W2 · EP-03 · CA-ALL, CA-PUB, CA-INTAKE |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Route privacy and support requests |
| Key actions (Part 2.5) | Submit privacy/support request |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W12; W29 |
| Tests | SM-UAT-S030; SM-UX-UAT-W30; unit families 001, 002, 010, 011, 012, 013, 030, 065, 066; **TC-ENH-C-112** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Full name | B+R | P | Text (≤ 200) | Text input | optional for general information. Trimmed; required where marked |
| 2 | Email | B | P | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 3 | Request type | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Message | B | P | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 5 | Request ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 6 | Tenant contact | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 7 | Privacy notice revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Response deadline | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Full name: optional for general information.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/public/site/pages/{slug}` | P | API-290;API-486 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/public/leads` | C | API-212 | exact |
| POST | `/api/v1/commercial/portal/requests` | P | API-069 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P); `growth_form` → ENT-080 `crm_form` (C); `growth_lead` → ENT-079 `crm_lead` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_submission` → ENT-082 `crm_submission` (C); `growth_deal` → ENT-086 `crm_deal` (C); `sales_external_access_grant` → ENT-009 `ten_portal_grant` (P); `growth_task` → ENT-148 `lcy_task` (C); `growth_privacy_request` → ENT-036 `gov_privacy_request` (C); `growth_renewal` → ENT-150 `lcy_renewal` (C)

### 2.7.11.13 W31: SaaS introduction, plans & demo

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Confidential Admin; assigned role and scope required |
| Command Centre view · pattern (Part 2.5) | Website public · PP-HOME |
| Legacy screen ID · build class · location class (doc 06) | new in 147-scope · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W31 (alias SM-FR-W31, SM-UX-FR-W31) · W5 · EP-20 · CA-ALL, CA-PUB |
| Filters | None of FLT-01…11 (internal filters excluded, doc 06 Part A); published selectors only |
| Automation (doc 06/17) | Select plan; request demo; begin registration |
| Key actions (Part 2.5) | Book demo, Start application |
| Screen acceptance (doc 06) | No private fundraising offers or implied outcomes; publish only approved service terms |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | W32; W01; W02 |
| Tests | no SM-UAT alias (new interface, Part 6.1 §6.1.12.5); SM-UX-UAT-W31; unit families n/a; **TC-ENH-C-113** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Service plan | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Included features | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 3 | Usage limits | B | C | Integer (computed) | Number (read-only) | Distinct records; Unknown ≠ 0 |
| 4 | Service model | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 5 | Pricing basis | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 6 | Currency | B | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 7 | Demo slot | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Terms revision | B | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/workspace/public/plans` | P | API-501 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `sales_service_plan` → ENT-179 `saas_plan` (P)


## 2.7.12 Website: intake forms

### 2.7.12.1 W12: General business enquiry

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website intake · PP-FORM |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W12 (alias SM-FR-W12, trace M22; B-WEB, SM-UX-FR-W12) · W2 · EP-07 · CA-ALL, CA-PUB, CA-INTAKE |
| Filters | None (bounded intake form; startup/offering locked from context) |
| Automation (doc 06/17) | Qualify and assign; send permitted acknowledgement |
| Key actions (Part 2.5) | Submit |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W13; W21 |
| Tests | SM-UAT-S012; SM-UX-UAT-W12; unit families 001, 002, 004, 010, 011, 012, 013, 023, 030, 042; **TC-ENH-C-114** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Full name | B | C | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Email | B | C | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 4 | Country | B | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 5 | Startup | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 6 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 7 | Message | B | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 8 | Preferred channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 9 | Timezone | B | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 10 | Consent notice | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 11 | Enquiry ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 12 | Source attribution | A | C | Attribution ID / event reference | Read-only text | First-party only; captured server-side |

*Replace rules (doc 06 "Remove / replace"):* Startup and Offering: derive locked context.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/forms/{slug}` | P | API-228 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/public/leads` | C | API-212 | exact |

**Tables → blueprint entities:** `growth_form` → ENT-080 `crm_form` (C); `growth_lead` → ENT-079 `crm_lead` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_submission` → ENT-082 `crm_submission` (C)

### 2.7.12.2 W13: Product demo and partnership enquiry

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website intake · PP-FORM |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W13 (alias SM-FR-W13, trace M22; B-WEB, SM-UX-FR-W13) · W2 · EP-07 · CA-ALL, CA-PUB, CA-INTAKE |
| Filters | None (bounded intake form; startup/offering locked from context) |
| Automation (doc 06/17) | Route demo/partner workflow and eligible scheduling |
| Key actions (Part 2.5) | Submit, Choose a slot |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W18; W21 |
| Tests | SM-UAT-S013; SM-UX-UAT-W13; unit families 001, 002, 004, 010, 011, 012, 013, 023, 030, 042; **TC-ENH-C-115** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Full name | B | P | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Email | B | P | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 4 | Startup | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 6 | Request type | B+R | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | configurable by capability. Values from the active reference dataset (CFG-32); unknown values rejected |
| 7 | Message | B | P | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 8 | Meeting preference | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Partnership category | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 10 | Company size band | A | C | Enumeration | Badge / select | Allowed values from configuration |
| 11 | Consent | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 12 | Request reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |

*Replace rules (doc 06 "Remove / replace"):* Request type: configurable by capability.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/forms/{slug}` | P | API-221;API-228 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/public/leads` | C | API-212 | exact |

**Tables → blueprint entities:** `growth_form` → ENT-080 `crm_form` (C); `growth_lead` → ENT-079 `crm_lead` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_submission` → ENT-082 `crm_submission` (C)

### 2.7.12.3 W14: Request for quotation

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public / Portal |
| Command Centre view · pattern (Part 2.5) | Website intake · PP-FORM |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W14 (alias SM-FR-W14, trace M22; B-WEB, SM-UX-FR-W14) · W4 · EP-14 · CA-ALL, CA-INTAKE, CA-PORTAL, CA-FIN |
| Filters | None (bounded intake form; startup/offering locked from context) |
| Automation (doc 06/17) | Validate request; create scoped quotation draft |
| Key actions (Part 2.5) | Add line, Submit |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W23; W21 |
| Tests | SM-UAT-S014; SM-UX-UAT-W14; unit families 001, 002, 010, 011, 012, 013, 030, 056, 057, 058, 059, 066; **TC-ENH-C-116** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Full name | B | P | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Email | B | P | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 4 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Quantity | B | C | Decimal quantity | QuantityInput (value + unit) | Non-negative; validated range; unit mandatory |
| 6 | Unit | B | C | Unit of measure (ref_unit) | Select | Allowed units per SKU |
| 7 | Delivery region | B | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 8 | Message | B | P | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 9 | SKU or service ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 10 | Quote currency | A | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 11 | Required by date | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 12 | Delivery terms | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 13 | Enquiry ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |

*Replace rules (doc 06 "Remove / replace"):* Quantity and Unit: conditional for service offerings.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/forms/{slug}` | P | API-221;API-228 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/public/leads` | C | API-212 | exact |

**Tables → blueprint entities:** `growth_form` → ENT-080 `crm_form` (C); `growth_lead` → ENT-079 `crm_lead` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_submission` → ENT-082 `crm_submission` (C)

### 2.7.12.4 W15: Project requirement submission

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public / Portal |
| Command Centre view · pattern (Part 2.5) | Website intake · PP-FORM (multi-step) |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W15 (alias SM-FR-W15, trace M22; B-WEB, SM-UX-FR-W15) · W4 · EP-14 · CA-ALL, CA-INTAKE, CA-PORTAL |
| Filters | None (bounded intake form; startup/offering locked from context) |
| Automation (doc 06/17) | Route owned project requests to AppNAI; block ineligible capability |
| Key actions (Part 2.5) | Next, Sign in to upload, Submit |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W18; W21 |
| Tests | SM-UAT-S015; SM-UX-UAT-W15; unit families 001, 002, 048, 051, 052, 058, 060, 061, 062, 063, 064, 066; **TC-ENH-C-117** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Full name | B | P | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Email | B | P | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 4 | Technology | B+R | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | dynamic. Values from the active reference dataset (CFG-32); unknown values rejected |
| 5 | Delivery model | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 6 | Deadline | B+R | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | timezone-aware. Stored UTC; displayed in user and record time zone; range validated |
| 7 | Budget | B+R | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | optional. Decimal only; currency required; server recomputes (CA-FIN) |
| 8 | Message | B | P | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 9 | Project scope | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 10 | Attachments | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Budget currency | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 12 | Procurement reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 13 | Eligibility | A | C | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 14 | Consent | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |

*Replace rules (doc 06 "Remove / replace"):* Budget: optional; Technology: dynamic; Deadline: timezone-aware.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/forms/{slug}` | P | API-221;API-228 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/public/leads` | C | API-212 | exact |

**Tables → blueprint entities:** `growth_form` → ENT-080 `crm_form` (C); `growth_lead` → ENT-079 `crm_lead` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_submission` → ENT-082 `crm_submission` (C)

### 2.7.12.5 W16: Supplier registration and product supply enquiry

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public / Portal |
| Command Centre view · pattern (Part 2.5) | Website intake · PP-FORM (multi-step) |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W16 (alias SM-FR-W16, trace M22; B-WEB, SM-UX-FR-W16) · W4 · EP-14 · CA-ALL, CA-INTAKE, CA-PORTAL |
| Filters | None (bounded intake form; startup/offering locked from context) |
| Automation (doc 06/17) | Route supplier review; verify attachments and eligibility |
| Key actions (Part 2.5) | Submit |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W12; W21 |
| Tests | SM-UAT-S016; SM-UX-UAT-W16; unit families 001, 002, 010, 011, 012, 013, 030, 056, 057, 058, 059, 066; **TC-ENH-C-118** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Full name | B | C | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Email | B | P | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 4 | SKU | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | dynamic. Must belong to the same tenant and startup (composite FK) |
| 5 | Quantity | B | C | Decimal quantity | QuantityInput (value + unit) | Non-negative; validated range; unit mandatory |
| 6 | Unit | B | C | Unit of measure (ref_unit) | Select | Allowed units per SKU |
| 7 | Certification | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | optional by product. Allowlisted, validated server-side |
| 8 | Delivery region | B | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 9 | Message | B | P | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 10 | Supplier legal name | A | C | Text (≤ 200) | Text input | Trimmed; required where marked |
| 11 | Product grade | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 12 | Delivery terms | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 13 | Lead time | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 14 | Certificate expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Certification: optional by product; SKU: dynamic.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/forms/{slug}` | P | API-221;API-228 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/public/leads` | C | API-212 | exact |

**Tables → blueprint entities:** `growth_form` → ENT-080 `crm_form` (C); `growth_lead` → ENT-079 `crm_lead` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_submission` → ENT-082 `crm_submission` (C)

### 2.7.12.6 W17: Student training and institutional enquiry

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public / Portal |
| Command Centre view · pattern (Part 2.5) | Website intake · PP-FORM (branching) |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W17 (alias SM-FR-W17, trace M22; B-WEB, SM-UX-FR-W17) · W3 · EP-07 · CA-ALL, CA-PUB, CA-INTAKE |
| Filters | None (bounded intake form; startup/offering locked from context) |
| Automation (doc 06/17) | Route education enquiry; avoid unnecessary minor data |
| Key actions (Part 2.5) | Submit |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W19; W21 |
| Tests | SM-UAT-S017; SM-UX-UAT-W17; unit families 001, 002, 010, 011, 012, 013, 030, 048, 055; **TC-ENH-C-119** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Full name | B | P | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Email | B | P | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 3 | Institution | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Programme | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Domain | B | C | URL / verified domain | URL input or link | https only; domain must be verified where it drives publication |
| 6 | Grade band | B+R | C | Enumeration | Badge / select | conditional. Allowed values from configuration |
| 7 | Mode | B | C | Enumeration (Manual, Assisted, Supervised, Controlled Autonomous / L0–L3) | Select bounded by policy | Capped by DEC-064 autonomy limits |
| 8 | Cohort | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Guardian permission | B+R | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | conditional for minors. Purpose and policy revision recorded; withdrawal immediate |
| 10 | Message | B | P | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 11 | Preferred language | B | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 12 | Enquiry audience | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 13 | Learner age band | A | C | Enumeration | Badge / select | Allowed values from configuration |
| 14 | Intake consent | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 15 | Institution type | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |

*Replace rules (doc 06 "Remove / replace"):* Guardian permission: conditional for minors; Grade band: conditional.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/forms/{slug}` | P | API-221;API-228 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/public/leads` | C | API-212 | exact |

**Tables → blueprint entities:** `growth_form` → ENT-080 `crm_form` (C); `growth_lead` → ENT-079 `crm_lead` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_submission` → ENT-082 `crm_submission` (C)

### 2.7.12.7 W18: Meeting and appointment booking

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public / Portal |
| Command Centre view · pattern (Part 2.5) | Website intake · PP-FORM + LP-CAL (mini) |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W18 (alias SM-FR-W18, trace M29; M22; B-WEB, SM-UX-FR-W18) · W2 · EP-09 · CA-ALL, CA-INTAKE, CA-PORTAL, CA-DISPATCH |
| Filters | None (bounded intake form; startup/offering locked from context) |
| Automation (doc 06/17) | Reserve verified slot; trigger reminders |
| Key actions (Part 2.5) | Select slot, Confirm |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W22; W13 |
| Tests | SM-UAT-S018; SM-UX-UAT-W18; unit families 001, 002, 004, 014, 015, 023, 024, 042; **TC-ENH-C-120** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Full name | B | P | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Email | B | P | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 3 | Startup | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Date | B+R | P | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | select available slot. Stored UTC; displayed in user and record time zone; range validated |
| 5 | Timezone | B | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 6 | Slot ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 7 | Meeting purpose | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Duration | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |
| 9 | Booking status | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 10 | Reschedule link | A | C | URL / verified domain | URL input or link | https only; domain must be verified where it drives publication |

*Replace rules (doc 06 "Remove / replace"):* Date: select available slot.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/meeting-slots/{token}` | N | — | no exact or equivalent operation |
| POST | `/api/v1/meetings/book` | C | API-243 | exact |
| POST | `/api/v1/public/leads` | C | API-212 | exact |

**Tables → blueprint entities:** `growth_form` → ENT-080 `crm_form` (C); `growth_lead` → ENT-079 `crm_lead` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_submission` → ENT-082 `crm_submission` (C); `growth_calendar_link` → ENT-104 `eng_calendar_link` (C); `growth_deal` → ENT-086 `crm_deal` (C); `growth_meeting` → ENT-103 `eng_meeting` (C)

### 2.7.12.8 W19: Webinar and event registration

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website intake · PP-FORM |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W19 (alias SM-FR-W19, trace M40; B-WEB, SM-UX-FR-W19) · W3 · EP-09 · CA-ALL, CA-PUB, CA-INTAKE |
| Filters | None (bounded intake form; startup/offering locked from context) |
| Automation (doc 06/17) | Register; issue approved reminders; track attendance |
| Key actions (Part 2.5) | Register |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W22; W18 |
| Tests | SM-UAT-S019; SM-UX-UAT-W19; unit families 001, 002, 010, 011, 012, 013, 030, 060, 061, 062, 063, 064; **TC-ENH-C-121** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Full name | B | C | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Email | B | P | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 3 | Event | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Institution | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | conditional. Must belong to the same tenant and startup (composite FK) |
| 5 | Timezone | B | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 6 | Event revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 7 | Consent | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 8 | Attendance state | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 9 | Registration reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 10 | Accessibility needs | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |

*Replace rules (doc 06 "Remove / replace"):* Institution: conditional.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/events/{id}` | P | API-326 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/events/register` | C | API-296 | exact |

**Tables → blueprint entities:** `growth_lead` → ENT-079 `crm_lead` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_business_event` → ENT-170 `ops_domain_event` (P); `growth_event_registration` → ENT-121 `mkt_registration` (P)

### 2.7.12.9 W20: Partner referral form

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public |
| Command Centre view · pattern (Part 2.5) | Website intake · PP-FORM |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W20 (alias SM-FR-W20, trace M42; B-WEB, SM-UX-FR-W20) · W3 · EP-12 · CA-ALL, CA-PUB, CA-INTAKE |
| Filters | None (bounded intake form; startup/offering locked from context) |
| Automation (doc 06/17) | Qualify and assign referral; prevent duplicates |
| Key actions (Part 2.5) | Submit |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W12; W21 |
| Tests | SM-UAT-S020; SM-UX-UAT-W20; unit families 001, 002, 004, 023, 042, 060, 061, 062, 063, 064; **TC-ENH-C-122** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Full name | B | P | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Email | B | P | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 4 | Referral | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | avoid unnecessary third-party personal details. Must belong to the same tenant and startup (composite FK) |
| 5 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 6 | Message | B | P | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 7 | Referrer relationship | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Referral consent | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 9 | Attribution code | A | C | Attribution ID / event reference | Read-only text | First-party only; captured server-side |
| 10 | Partner status | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |

*Replace rules (doc 06 "Remove / replace"):* Referral: avoid unnecessary third-party personal details.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/public/referrals` | C | API-298 | exact |

**Tables → blueprint entities:** `growth_lead` → ENT-079 `crm_lead` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_partner` → ENT-153 `lcy_partner` (C); `growth_referral` → ENT-123 `mkt_referral` (C)

### 2.7.12.10 W32: Startup & third-party client registration

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Confidential Admin; assigned role and scope required |
| Command Centre view · pattern (Part 2.5) | Website intake · LP-WIZARD |
| Legacy screen ID · build class · location class (doc 06) | new in 147-scope · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W32 (alias SM-FR-W32, SM-UX-FR-W32) · W5 · EP-20 · CA-ALL, CA-INTAKE |
| Filters | None (bounded intake form; startup/offering locked from context) |
| Automation (doc 06/17) | Submit application; verify administrator; resume registration |
| Key actions (Part 2.5) | Next, Verify email, Submit application |
| Screen acceptance (doc 06) | Prove administrator authority; no provisioning before verified identity and approval |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | W33; W31 |
| Tests | no SM-UAT alias (new interface, Part 6.1 §6.1.12.5); SM-UX-UAT-W32; unit families n/a; **TC-ENH-C-123** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Legal business name | B | C | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Legal identifier | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 3 | Country | B | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 4 | Business email | B | C | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 5 | Administrator name | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Website | B | C | URL / verified domain | URL input or link | https only; domain must be verified where it drives publication |
| 7 | Service model | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 8 | Plan | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Terms consent | B | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 10 | Verification status | B | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/commercial/workspace/public/applications` | P | API-503;API-505;API-506 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `sales_ui_application` → ENT-187 `saas_application_draft` (P)


## 2.7.13 Portal and SaaS client

### 2.7.13.1 W21: Customer registration, login and recovery

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Authentication |
| Command Centre view · pattern (Part 2.5) | Portal · PP-FORM |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W21 (alias SM-FR-W21, trace M01; B-WEB, SM-UX-FR-W21) · W2 · EP-19 · CA-ALL, CA-PORTAL |
| Filters | Own-record selectors only (status, date, reference); no internal filters |
| Automation (doc 06/17) | Reuse identity service; scope customer access |
| Key actions (Part 2.5) | Sign in, Register, Recover |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PUB |
| Related screens (in-context links, FR-ENH-C-012) | W22; W27 |
| Tests | SM-UAT-S021; SM-UX-UAT-W21; unit families 001, 002, 003, 004, 005, 006, 007, 060, 061, 062, 063, 064; **TC-ENH-C-124** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Email | B | C | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 2 | Password | B+R | C | Identity attribute held by the reused IdP | IdP-hosted control | never persist in demo. Never persisted or displayed by this product (DEC-019) |
| 3 | MFA method | A | C | Identity attribute held by the reused IdP | IdP-hosted control | Never persisted or displayed by this product (DEC-019) |
| 4 | Recovery method | A | C | Identity attribute held by the reused IdP | IdP-hosted control | Never persisted or displayed by this product (DEC-019) |
| 5 | Terms revision | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 6 | Identity provider | A | C | Identity attribute held by the reused IdP | IdP-hosted control | Never persisted or displayed by this product (DEC-019) |

*Replace rules (doc 06 "Remove / replace"):* Password: never persist in demo.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/auth/login` | C | API-001 | exact |
| GET | `/me` | C | API-002 | exact |
| POST | `/auth/logout` | P | API-012 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/commercial/portal/external-grants/accept` | P | API-151;API-356 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `existing membership table` → ENT-008 `ten_membership` (P); `existing role table` → ENT-007 `ten_role` (P); `existing user table` → ENT-006 `ten_user` (P); `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_contact` → ENT-074 `intel_contact` (C); `sales_external_access_grant` → ENT-009 `ten_portal_grant` (P)

### 2.7.13.2 W22: Customer self-service dashboard

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Portal |
| Command Centre view · pattern (Part 2.5) | Portal · PT-DASH |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W22 (alias SM-FR-W22, trace B-WEB, SM-UX-FR-W22) · W2 · EP-19 · CA-ALL, CA-PORTAL |
| Filters | Own-record selectors only (status, date, reference); no internal filters |
| Automation (doc 06/17) | Project shared customer journey with scoped records |
| Key actions (Part 2.5) | Open item |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W23; W24; W25; W26; W27; W28 |
| Tests | SM-UAT-S022; SM-UX-UAT-W22; unit families 001, 002, 007, 015, 046, 056, 057, 058, 059, 066; **TC-ENH-C-125** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contextual / display layout | B | N/A | Layout only | Published page blocks | No data field; content from approved snapshot |
| 2 | Active offering | A | C | Boolean | Toggle (role-gated) | Change audited |
| 3 | Open tasks | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Next milestone | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 5 | Unpaid verified invoices | A | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 6 | Last updated | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/portal/overview` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_lead` → ENT-079 `crm_lead` (C); `growth_deal` → ENT-086 `crm_deal` (C); `growth_contact` → ENT-074 `intel_contact` (C); `sales_external_access_grant` → ENT-009 `ten_portal_grant` (P); `growth_onboarding` → ENT-147 `lcy_onboarding` (C)

### 2.7.13.3 W23: Proposal and quotation review

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Portal |
| Command Centre view · pattern (Part 2.5) | Portal · PT-DOC |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W23 (alias SM-FR-W23, trace B-WEB, SM-UX-FR-W23) · W4 · EP-13 · CA-ALL, CA-PORTAL, CA-FIN |
| Filters | Own-record selectors only (status, date, reference); no internal filters |
| Automation (doc 06/17) | Validate current quote; route customer response |
| Key actions (Part 2.5) | Accept, Request changes (comment), Download PDF |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W24; W26; W22 |
| Tests | SM-UAT-S023; SM-UX-UAT-W23; unit families 001, 002, 014, 015, 024, 056, 057, 058, 059, 066; **TC-ENH-C-126** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Status | B+R | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | read-only. Changed only by controlled transition; never free text |
| 3 | Quote revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 4 | Valid until | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 5 | Currency | A | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 6 | Approval state | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Accept/request revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |

*Replace rules (doc 06 "Remove / replace"):* Status: read-only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/portal/quotations/{id}` | N | — | no exact or equivalent operation |
| POST | `/api/v1/commercial/portal/quotations/{id}/respond` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_audit_event` → ENT-172 `ops_audit_event` (C); `sales_external_access_grant` → ENT-009 `ten_portal_grant` (P); `growth_proposal` → ENT-125 `com_proposal` (C); `growth_quote` → ENT-127 `com_quote` (C); `growth_quote_line` → ENT-128 `com_quote_line` (C)

### 2.7.13.4 W24: Agreement review and e-signature

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Portal |
| Command Centre view · pattern (Part 2.5) | Portal · PT-DOC |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W24 (alias SM-FR-W24, trace M46; B-WEB, SM-UX-FR-W24) · W4 · EP-13 · CA-ALL, CA-PORTAL, CA-DISPATCH |
| Filters | Own-record selectors only (status, date, reference); no internal filters |
| Automation (doc 06/17) | Route authorized e-sign; reject stale document |
| Key actions (Part 2.5) | Sign (via provider or signed upload), Decline |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W23; W25; W22 |
| Tests | SM-UAT-S024; SM-UX-UAT-W24; unit families 001, 002, 007, 015, 033, 034, 035, 036, 043, 044, 046; **TC-ENH-C-127** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Document type | B | C | File reference (object storage key + scan state) | FileUpload with scan status | Scanned before use (NFR-021); size/type allowlist |
| 2 | Status | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | read-only. Changed only by controlled transition; never free text |
| 3 | Signature authority | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Document revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 5 | Terms hash | A | C | char(64) SHA-256 | HashBadge (read-only) | Server-computed; never editable |
| 6 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 7 | Sign status | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |

*Replace rules (doc 06 "Remove / replace"):* Status: read-only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/agreements/{token}` | P | API-358 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/public/agreements/{token}/sign` | P | API-359 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_contract` → ENT-131 `com_contract` (C); `growth_signature_event` → ENT-132 `com_signature_event` (C)

### 2.7.13.5 W25: Order, project and service status

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Portal |
| Command Centre view · pattern (Part 2.5) | Portal · PT-DASH |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W25 (alias SM-FR-W25, trace B-WEB, SM-UX-FR-W25) · W4 · EP-14 · CA-ALL, CA-PORTAL |
| Filters | Own-record selectors only (status, date, reference); no internal filters |
| Automation (doc 06/17) | Reflect verified fulfillment and service events |
| Key actions (Part 2.5) | Accept delivery, Raise discrepancy |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W26; W27; W22 |
| Tests | SM-UAT-S025; SM-UX-UAT-W25; unit families 001, 002, 056, 057, 058, 059, 066; **TC-ENH-C-128** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Status | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | read-only. Changed only by controlled transition; never free text |
| 3 | Order/project reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 4 | Milestone | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 5 | Delivery ETA | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 6 | Exception | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 7 | Last update | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Status: read-only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/portal/orders/{id}` | C | API-382 | exact |

**Tables → blueprint entities:** `sales_external_access_grant` → ENT-009 `ten_portal_grant` (P); `sales_fulfillment` → ENT-137 `com_fulfillment_event` (P); `sales_order` → ENT-135 `com_order` (P); `sales_order_line` → ENT-136 `com_order_line` (P)

### 2.7.13.6 W26: Payment and invoice status

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Portal |
| Command Centre view · pattern (Part 2.5) | Portal · PT-DASH |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W26 (alias SM-FR-W26, trace M47; B-WEB, SM-UX-FR-W26) · W4 · EP-15 · CA-ALL, CA-PORTAL, CA-FIN |
| Filters | Own-record selectors only (status, date, reference); no internal filters |
| Automation (doc 06/17) | Show verified transactions; no raw bank secrets |
| Key actions (Part 2.5) | Download invoice, View instructions, Upload payment proof |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W25; W22 |
| Tests | SM-UAT-S026; SM-UX-UAT-W26; unit families 001, 002, 015, 033, 040, 041; **TC-ENH-C-129** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contextual / display layout | B | N/A | Layout only | Published page blocks | No data field; content from approved snapshot |
| 2 | Invoice ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 3 | Currency | A | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 4 | Amount due | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 5 | Receipt verification | A | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 6 | Payment instruction expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/payment-status/{token}` | N | — | no exact or equivalent operation |
| POST | `/api/v1/invoices/{id}/payment-link` | P | API-398 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_invoice` → ENT-140 `com_invoice` (C); `growth_payment` → ENT-142 `com_payment` (C)

### 2.7.13.7 W27: Customer onboarding and document exchange

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Portal |
| Command Centre view · pattern (Part 2.5) | Portal · PT-DASH |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W27 (alias SM-FR-W27, trace M48; B-WEB, SM-UX-FR-W27) · W4 · EP-16 · CA-ALL, CA-PORTAL |
| Filters | Own-record selectors only (status, date, reference); no internal filters |
| Automation (doc 06/17) | Route documents and update checklist |
| Key actions (Part 2.5) | Upload, Mark task done |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W25; W28; W22 |
| Tests | SM-UAT-S027; SM-UX-UAT-W27; unit families 001, 002, 004, 015, 016, 017, 018, 019, 029, 032, 033, 036, 038, 039, 047; **TC-ENH-C-130** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Subject | B | P | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Message | B | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 3 | Attachment | B+R | C | File reference (object storage key + scan state) | FileUpload with scan status | conditional and validated. Scanned before use (NFR-021); size/type allowlist |
| 4 | Onboarding case | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 5 | Task due | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 6 | File scan state | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Document revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Recipient scope | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |

*Replace rules (doc 06 "Remove / replace"):* Attachment: conditional and validated.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/onboarding/{token}` | P | API-437 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/onboarding/{id}/complete` | C | API-413 | exact |
| POST | `/api/v1/commercial/portal/documents` | P | API-424 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/commercial/portal/documents/{id}/complete` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `sales_external_access_grant` → ENT-009 `ten_portal_grant` (P); `growth_onboarding` → ENT-147 `lcy_onboarding` (C); `growth_document` → ENT-024 `cat_document` (P); `growth_handoff` → ENT-149 `lcy_handoff` (C); `growth_outbox` → ENT-169 `ops_outbox` (C); `growth_task` → ENT-148 `lcy_task` (C)

### 2.7.13.8 W28: Support, feedback and renewal requests

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Portal |
| Command Centre view · pattern (Part 2.5) | Portal · PT-DASH + PP-FORM |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W28 (alias SM-FR-W28, trace B-WEB, SM-UX-FR-W28) · W4 · EP-16 · CA-ALL, CA-PORTAL |
| Filters | Own-record selectors only (status, date, reference); no internal filters |
| Automation (doc 06/17) | Classify support and renewal requests; escalate |
| Key actions (Part 2.5) | Create case, Reply |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W22; W29 |
| Tests | SM-UAT-S028; SM-UX-UAT-W28; unit families 001, 002, 007, 015, 046, 065, 066; **TC-ENH-C-131** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Request type | B+R | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | route by capability. Values from the active reference dataset (CFG-32); unknown values rejected |
| 2 | Subject | B | P | Text (≤ 200) | Text input | Trimmed; required where marked |
| 3 | Message | B | P | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 4 | Case ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 5 | Offering reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 6 | Severity | A | C | Enumeration | Badge / select | Allowed values from configuration |
| 7 | SLA | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 8 | Contact preference | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |

*Replace rules (doc 06 "Remove / replace"):* Request type: route by capability.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/commercial/portal/requests` | P | API-069 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `sales_external_access_grant` → ENT-009 `ten_portal_grant` (P); `growth_task` → ENT-148 `lcy_task` (C); `growth_privacy_request` → ENT-036 `gov_privacy_request` (C); `growth_renewal` → ENT-150 `lcy_renewal` (C)

### 2.7.13.9 W29: Communication preferences and opt-out

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Public / Portal |
| Command Centre view · pattern (Part 2.5) | Portal · PP-FORM |
| Legacy screen ID · build class · location class (doc 06) | original W-ID (no legacy number) · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W29 (alias SM-FR-W29, trace M04; M56; B-WEB, SM-UX-FR-W29) · W2 · EP-03 · CA-ALL, CA-PORTAL |
| Filters | Own-record selectors only (status, date, reference); no internal filters |
| Automation (doc 06/17) | Apply scoped opt-out; stop scheduled messages |
| Key actions (Part 2.5) | Save, Unsubscribe from all |
| Screen acceptance (doc 06) | Use applicable published/authorized selectors from current fields; no confidential filters on public pages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-PORTAL |
| Related screens (in-context links, FR-ENH-C-012) | W30; W21 |
| Tests | SM-UAT-S029; SM-UX-UAT-W29; unit families 001, 002, 004, 023, 042, 048, 055; **TC-ENH-C-132** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Email | B+R | P | Email address (encrypted at rest, HMAC lookup) | Email input | derive verified identity where possible. RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 2 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Request type | B | P | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Consent scope | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 5 | Effective suppression | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 6 | Policy revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 7 | Confirmation reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |

*Replace rules (doc 06 "Remove / replace"):* Email: derive verified identity where possible.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/public/preferences/{token}` | P | API-081;API-083 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/consents` | C | API-066 | exact |
| POST | `/api/v1/opt-out` | C | API-067 | exact |
| POST | `/api/v1/privacy/requests` | C | API-069 | exact |

**Tables → blueprint entities:** `growth_consent` → ENT-027 `gov_consent` (C); `growth_privacy_request` → ENT-036 `gov_privacy_request` (C); `growth_enrollment` → ENT-102 `eng_enrollment` (C); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_suppression` → ENT-028 `gov_suppression` (C)

### 2.7.13.10 W33: AI business onboarding & configuration wizard

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Confidential Admin; assigned role and scope required |
| Command Centre view · pattern (Part 2.5) | Portal · LP-WIZARD + LP-EDITOR |
| Legacy screen ID · build class · location class (doc 06) | new in 147-scope · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W33 (alias SM-FR-W33, SM-UX-FR-W33) · W5 · EP-20 · CA-ALL, CA-AI, CA-CONFIG |
| Filters | Own-record selectors only (status, date, reference); no internal filters |
| Automation (doc 06/17) | Generate draft; edit; simulate; submit for approval; activate only when authorized |
| Key actions (Part 2.5) | Generate proposal, Accept/edit item, Simulate, Submit |
| Screen acceptance (doc 06) | AI proposals are unverified; no real dispatch or spend during onboarding |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | W34; W32 |
| Tests | no SM-UAT alias (new interface, Part 6.1 §6.1.12.5); SM-UX-UAT-W33; unit families n/a; **TC-ENH-C-133** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Business description | B | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 2 | Source documents | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 3 | Industry template | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Capabilities | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 5 | Business units | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 6 | Offerings or fundraising thesis | B | P | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 7 | Markets | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Language | B | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 9 | Channel permissions | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 10 | Objectives | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Workflow templates | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 12 | Budget proposal | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 13 | Readiness | B | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 14 | Configuration revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/workspace/onboarding/{id}` | P | API-412;API-422;API-437 | resource-equivalent path elsewhere in catalogue |
| PATCH | `/api/v1/commercial/workspace/onboarding/{id}` | P | API-509 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/commercial/workspace/onboarding/{id}/submit` | P | API-511 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `sales_ui_application` → ENT-187 `saas_application_draft` (P); `sales_ui_config_revision` → ENT-168 `aut_config_revision` (P)

### 2.7.13.11 W34: SaaS client service portal

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Confidential Admin; assigned role and scope required |
| Command Centre view · pattern (Part 2.5) | Portal · PT-DASH |
| Legacy screen ID · build class · location class (doc 06) | new in 147-scope · Template/typed configuration (doc 06 operating contract) · Website |
| FR · wave · epic · profiles | FR-W34 (alias SM-FR-W34, SM-UX-FR-W34) · W5 · EP-20 · CA-ALL, CA-PORTAL, CA-FIN |
| Filters | Own-record selectors only (status, date, reference); no internal filters |
| Automation (doc 06/17) | View invoices; request support; request plan change; open authorized Admin |
| Key actions (Part 2.5) | Request plan change, Request export, Open Admin |
| Screen acceptance (doc 06) | Client-only scoped billing; no cross-tenant or investor/customer records |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | W33 |
| Tests | no SM-UAT alias (new interface, Part 6.1 §6.1.12.5); SM-UX-UAT-W34; unit families n/a; **TC-ENH-C-134** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Tenant | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Authorized startups | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 3 | Service plan | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Entitlements | B | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 5 | Onboarding progress | B | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 6 | Usage | B | C | Integer (computed) | Number (read-only) | Distinct records; Unknown ≠ 0 |
| 7 | Invoice | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | Renewal | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Support case | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Export request | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Admin workspace link | B | C | URL / verified domain | URL input or link | https only; domain must be verified where it drives publication |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/workspace/client/service` | P | API-513;API-514;API-515;API-518 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/commercial/workspace/client/service-requests` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `sales_tenant` → ENT-001 `ten_tenant` (P); `sales_service_subscription` → ENT-182 `saas_subscription` (P); `sales_service_invoice` → ENT-184 `saas_service_invoice` (P); `sales_usage_charge` → ENT-183 `saas_usage_meter_reading` (P); `sales_ui_service_request` → none  (N)


## 2.7.14 Admin: global shell

### 2.7.14.1 A001: Login, MFA and account recovery

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Global · Auth page |
| Legacy screen ID · build class · location class (doc 06) | existing 001 · Reuse · Existing |
| FR · wave · epic · profiles | FR-A001 (alias SM-FR-A001, trace M01, SM-UX-FR-A001) · W0 · EP-01 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-05 Operations |
| Automation (doc 06/17) | Reuse existing identity; enforce session boundary |
| Key actions (Part 2.5) | Sign in, Verify |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Reuse existing login and security; connect navigation |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A003; A089 |
| Tests | SM-UAT-S031; SM-UX-UAT-A001; unit families 001, 002, 003, 004, 005, 006, 007; **TC-ENH-C-135** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Email | B | P | Email address (encrypted at rest, HMAC lookup) | Email input | RFC 5322 syntax; masked per ABAC; never used as lookup key on public paths |
| 2 | Password | B | C | Identity attribute held by the reused IdP | IdP-hosted control | Never persisted or displayed by this product (DEC-019) |
| 3 | MFA code | B | C | Identity attribute held by the reused IdP | IdP-hosted control | Never persisted or displayed by this product (DEC-019) |
| 4 | Identity provider | A | C | Identity attribute held by the reused IdP | IdP-hosted control | Never persisted or displayed by this product (DEC-019) |
| 5 | Recovery method | A | C | Identity attribute held by the reused IdP | IdP-hosted control | Never persisted or displayed by this product (DEC-019) |
| 6 | MFA method | A | C | Identity attribute held by the reused IdP | IdP-hosted control | Never persisted or displayed by this product (DEC-019) |
| 7 | Session scope | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |

*Replace rules (doc 06 "Remove / replace"):* Password and MFA code: never persist; no raw secret display.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/auth/login` | C | API-001 | exact |
| GET | `/me` | C | API-002 | exact |
| POST | `/auth/logout` | P | API-007 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `existing membership table` → ENT-008 `ten_membership` (P); `existing role table` → ENT-007 `ten_role` (P); `existing user table` → ENT-006 `ten_user` (P)

**Integrations (doc 06):** django auth [OSS]; django [OSS]; drf [OSS]

### 2.7.14.2 A003: Growth workspace navigation

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Global · Shell (§2.41) |
| Legacy screen ID · build class · location class (doc 06) | existing 003 · New shell · Workspace |
| FR · wave · epic · profiles | FR-A003 (alias SM-FR-A003, trace M01, SM-UX-FR-A003) · W0 · EP-17 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-05 Operations |
| Automation (doc 06/17) | Restore permitted context; clear stale scoped cache |
| Key actions (Part 2.5) | Change scope, STOP (role-gated) |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Shared menu and role-aware layout; no new login |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A089; A042; A029 |
| Tests | SM-UAT-S033; SM-UX-UAT-A003; unit families 001, 002, 003, 008, 009, 013, 045; **TC-ENH-C-136** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Startup | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | dynamic authorized directory. Must belong to the same tenant and startup (composite FK) |
| 2 | Business line | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Qualified leads | B | P | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 4 | Pipeline | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Verified revenue | B | P | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 6 | Tenant | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 7 | Capability | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | Objective | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Offering | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 10 | Active runs | A | C | Boolean | Toggle (role-gated) | Change audited |
| 11 | Workspace freshness | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |

*Replace rules (doc 06 "Remove / replace"):* Startup: dynamic authorized directory.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/me` | C | API-002 | exact |

**Tables → blueprint entities:** `existing membership table` → ENT-008 `ten_membership` (P); `existing role table` → ENT-007 `ten_role` (P); `existing user table` → ENT-006 `ten_user` (P)

**Integrations (doc 06):** django auth [OSS]; django [OSS]; drf [OSS]; postgresql [OSS]

### 2.7.14.3 A106: Persistent action and notification centre

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Global · Drawer + LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 116 · Contextual panel · Workspace |
| FR · wave · epic · profiles | FR-A106 (alias SM-FR-A106, trace B-AUTO, SM-UX-FR-A106) · W2 · EP-17 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-05 Operations |
| Automation (doc 06/17) | Deduplicate and prioritize interventions |
| Key actions (Part 2.5) | Open, Acknowledge, Snooze (not Critical), Archive |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Show overdue tasks, replies, bid deadlines, approvals, cost alerts and job failures; open scoped detail without resetting filters. |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A089; A014; A102 |
| Tests | SM-UAT-S136; SM-UX-UAT-A106; unit families 001, 002, 015, 016, 017, 018, 019, 032, 033, 036, 047; **TC-ENH-C-137** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Notification | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Severity | B | C | Enumeration | Badge / select | Allowed values from configuration |
| 3 | Action | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Due date | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 5 | Owner | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | lifecycle-derived. Changed only by controlled transition; never free text |
| 7 | Event/run ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Scope | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 9 | Action link | A | C | URL / verified domain | URL input or link | https only; domain must be verified where it drives publication |
| 10 | Acknowledgement | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | SLA | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 12 | Dedup key | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |

*Replace rules (doc 06 "Remove / replace"):* Status: lifecycle-derived.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sales/notifications` | P | API-549 | resource-equivalent DERIVED path on same screen |
| PATCH | `/api/v1/sales/notifications/{id}` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_task` → ENT-148 `lcy_task` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_job_run` → ENT-173 `ops_job_run` (C); `growth_notification` → ENT-174 `ops_notification` (C)

**Integrations (doc 06):** Internal React/Django [INT]


## 2.7.15 Admin: Overview view

### 2.7.15.1 A018: Organization directory

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-LIST + LP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | existing 019 · New · Workspace |
| FR · wave · epic · profiles | FR-A018 (alias SM-FR-A018, trace M13, SM-UX-FR-A018) · W1 · EP-05 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Resolve duplicates in authorized scope |
| Key actions (Part 2.5) | Create, Merge (review), Open 360 |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Filter hospitals, doctors' practices, IT companies and insurers |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A024; A020; A032 |
| Tests | SM-UAT-S048; SM-UX-UAT-A018; unit families 001, 002, 003, 008, 009, 013, 045; **TC-ENH-C-138** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Country | B | P | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 3 | Industry | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Organization type | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Size | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | verified band not guessed. Allowlisted, validated server-side |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Canonical organization ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Industry taxonomy | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 9 | Region | A | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 10 | Identity match | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Source provenance | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |

*Replace rules (doc 06 "Remove / replace"):* Size: verified band not guessed.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/organizations` | C | API-164 | exact |
| POST | `/api/v1/organizations` | C | API-165 | exact |
| GET | `/api/v1/organizations/{id}` | P | API-164;API-189 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/organizations/{id}/merge` | P | API-190;API-191 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_organization` → ENT-063 `intel_organization` (C); `growth_org_location` → ENT-064 `intel_location` (P); `growth_org_alias` → ENT-065 `intel_alias` (P)

**Integrations (doc 06):** Clay [CMU]; Leadfeeder [CMU]

### 2.7.15.2 A029: CRM sales pipeline

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-BOARD + LP-LIST toggle |
| Legacy screen ID · build class · location class (doc 06) | existing 030 · New · Workspace |
| FR · wave · epic · profiles | FR-A029 (alias SM-FR-A029, trace M21, SM-UX-FR-A029) · W2 · EP-07 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency); vertical: FLT-08…11 by capability profile |
| Automation (doc 06/17) | Update shared pipeline from business events |
| Key actions (Part 2.5) | New deal (from qualified), Transition, Assign |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Move deals through stages and record verified outcomes |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A032; A034; A065; A073 |
| Tests | SM-UAT-S059; SM-UX-UAT-A029; unit families 001, 002, 003, 008, 009, 013, 015, 033, 040, 041, 045; **TC-ENH-C-139** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Deal | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Stage | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | controlled transition. Changed only by controlled transition; never free text |
| 5 | Amount | B+R | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | currency required. Decimal only; currency required; server recomputes (CA-FIN) |
| 6 | Owner | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 7 | Next action | B | C | Task reference + due timestamp | Inline task chip | Due date required; owner required |
| 8 | Opportunity ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | Currency | A | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 10 | Stage event | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 11 | Active workflows | A | C | Boolean | Toggle (role-gated) | Change audited |
| 12 | Hold reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 13 | Next action due | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Stage: controlled transition; Amount: currency required.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/deals` | C | API-209 | exact |
| POST | `/api/v1/deals` | C | API-210 | exact |
| GET | `/api/v1/deals/{id}` | P | API-209;API-214;API-217 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/deals/{id}/transition` | C | API-211 | exact |
| POST | `/api/v1/deals/{id}/assign` | P | API-216 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `existing user table` → ENT-006 `ten_user` (P); `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_opportunity` → ENT-072 `intel_opportunity` (C); `growth_stage` → ENT-084 `crm_stage` (C); `growth_activity` → ENT-088 `crm_activity` (C)

**Integrations (doc 06):** customer-sales-automation [DEV]

### 2.7.15.3 A030: Sales pipeline and assignment rules

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 031 · New · Admin |
| FR · wave · epic · profiles | FR-A030 (alias SM-FR-A030, trace M21, SM-UX-FR-A030) · W2 · EP-07 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Validate transitions; route eligible assignment |
| Key actions (Part 2.5) | Save, Validate, Simulate, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure stages, owners and SLA rules |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A029; A031 |
| Tests | SM-UAT-S060; SM-UX-UAT-A030; unit families 001, 002, 003, 004, 005, 006, 007, 008, 009, 013, 045; **TC-ENH-C-140** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Stage | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | configurable allowed state. Changed only by controlled transition; never free text |
| 2 | Entry rule | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Exit rule | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Assignment | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 5 | Priority | B | C | Enumeration | Badge / select | Allowed values from configuration |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Rule revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Capability scope | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | SLA | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 10 | Conflict priority | A | C | Enumeration | Badge / select | Allowed values from configuration |
| 11 | Test fixture | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |

*Replace rules (doc 06 "Remove / replace"):* Stage: configurable allowed state.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/pipeline-stages` | N | — | no exact or equivalent operation |
| POST | `/api/v1/admin/pipeline-stages` | N | — | no exact or equivalent operation |
| POST | `/api/v1/deals/{id}/assign` | P | API-216 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `existing user table` → ENT-006 `ten_user` (P); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_stage` → ENT-084 `crm_stage` (C); `growth_activity` → ENT-088 `crm_activity` (C)

**Integrations (doc 06):** customer-sales-automation [DEV]

### 2.7.15.4 A031: Lead form and routing configuration

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-CONFIG + LP-EDITOR |
| Legacy screen ID · build class · location class (doc 06) | existing 033 · New · Admin |
| FR · wave · epic · profiles | FR-A031 (alias SM-FR-A031, trace M22, SM-UX-FR-A031) · W2 · EP-07 · CA-ALL, CA-ADMIN, CA-CONFIG, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Generate adaptive forms and route inbound leads |
| Key actions (Part 2.5) | Save, Preview, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure enquiry forms and assignment |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A030; A056; A107 |
| Tests | SM-UAT-S061; SM-UX-UAT-A031; unit families 001, 002, 003, 004, 005, 006, 007, 010, 011, 012, 013, 030; **TC-ENH-C-141** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Form | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Offering | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | dynamic scoped list. Must belong to the same tenant and startup (composite FK) |
| 3 | Routing rule | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Consent | B | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 5 | Owner | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Form revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Field schema | A | C | JSON Schema document (versioned) | Schema editor with validation report | Allowed field types only; validated before activation (CA-CONFIG) |
| 9 | Consent revision | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 10 | Source attribution | A | C | Attribution ID / event reference | Read-only text | First-party only; captured server-side |
| 11 | Duplicate strategy | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Offering: dynamic scoped list.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/forms` | P | API-221 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/admin/forms` | P | API-222;API-223 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_form` → ENT-080 `crm_form` (C); `growth_policy_version` → ENT-029 `gov_policy_version` (C)

**Integrations (doc 06):** react forms [OSS]; react [OSS]; Common Room [CMU]

### 2.7.15.5 A032: Customer 360 profile

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | existing 034 · New · Workspace |
| FR · wave · epic · profiles | FR-A032 (alias SM-FR-A032, trace M21; M23; M24, SM-UX-FR-A032) · W2 · EP-07 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Unify shared customer history and stop conflicting outreach |
| Key actions (Part 2.5) | Invite to portal, Start outreach (opens A034), Stop conflicting run |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | See contacts, deals, evidence, history and channel eligibility |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A029; A037; A065; A075 |
| Tests | SM-UAT-S062; SM-UX-UAT-A032; unit families 001, 002, 003, 004, 005, 006, 007, 008, 009, 013, 045; **TC-ENH-C-142** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Contact | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Stage | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 5 | Owner | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Eligibility | B+R | C | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | computed read-only. Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 7 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 8 | Canonical relationship | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Identity links | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Timeline | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Consent history | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 12 | Open orders | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 13 | Active runs | A | C | Boolean | Toggle (role-gated) | Change audited |

*Replace rules (doc 06 "Remove / replace"):* Eligibility: computed read-only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/deals/{id}` | P | API-209;API-214 | resource-equivalent path elsewhere in catalogue |
| GET | `/api/v1/organizations/{id}/360` | C | API-213 | exact |
| POST | `/api/v1/engagement/check` | C | API-068 | exact |

**Tables → blueprint entities:** `growth_lead` → ENT-079 `crm_lead` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_deal` → ENT-086 `crm_deal` (C); `growth_contact` → ENT-074 `intel_contact` (C); `sales_external_access_grant` → ENT-009 `ten_portal_grant` (P); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_suppression` → ENT-028 `gov_suppression` (C); `growth_organization` → ENT-063 `intel_organization` (C); `growth_contact_verification` → ENT-077 `intel_contact_verification` (C); `growth_stage` → ENT-084 `crm_stage` (C); `growth_activity` → ENT-088 `crm_activity` (C); `growth_account_projection` → ENT-193 `ana_account_projection` (C); `growth_eligibility_decision` → ENT-031 `gov_eligibility_decision` (P)

**Integrations (doc 06):** postgresql [OSS]

### 2.7.15.6 A042: Growth dashboard

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | existing 045 · New · Workspace |
| FR · wave · epic · profiles | FR-A042 (alias SM-FR-A042, trace M30, SM-UX-FR-A042) · W2 · EP-17 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Project scoped KPIs and drill down |
| Key actions (Part 2.5) | Change period, Drill down, Update task |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Track leads, meetings, pipeline and tasks |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A029; A082; A089 |
| Tests | SM-UAT-S072; SM-UX-UAT-A042; unit families 001, 002, 003, 008, 009, 013, 015, 016, 017, 018, 019, 032, 033, 036, 045, 047; **TC-ENH-C-143** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Startup | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | dynamic authorized list. Must belong to the same tenant and startup (composite FK) |
| 2 | Qualified leads | B | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 3 | Pipeline | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Verified revenue | B | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 5 | Conversion | B | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 6 | Tenant | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 7 | Objective | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | Offering | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Verified revenue basis | A | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 10 | Cost per outcome | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Data freshness | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |

*Replace rules (doc 06 "Remove / replace"):* Startup: dynamic authorized list.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/metrics/funnel` | C | API-537 | exact |
| GET | `/api/v1/tasks` | P | API-265 | resource-equivalent DERIVED path on same screen |
| PATCH | `/api/v1/tasks/{id}` | P | API-266 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_lead` → ENT-079 `crm_lead` (C); `growth_deal` → ENT-086 `crm_deal` (C); `growth_meeting` → ENT-103 `eng_meeting` (C); `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_task` → ENT-148 `lcy_task` (C); `growth_metric_snapshot` → ENT-192 `ana_metric_snapshot` (C)

**Integrations (doc 06):** postgresql [OSS]

### 2.7.15.7 A043: Management dashboard

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | existing 046 · New · Admin |
| FR · wave · epic · profiles | FR-A043 (alias SM-FR-A043, trace M30, SM-UX-FR-A043) · W2 · EP-17 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Aggregate scoped team metrics and alerts |
| Key actions (Part 2.5) | Drill to owner |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Monitor automated KPIs and SLA alerts |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A042; A087; A089 |
| Tests | SM-UAT-S073; SM-UX-UAT-A043; unit families 001, 002, 003, 008, 009, 013, 015, 016, 017, 018, 019, 032, 033, 036, 045, 047; **TC-ENH-C-144** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Team | B+R | C | User/team reference (scoped membership) | User picker (scoped) | authorized group only. Only members with the required role in scope |
| 2 | Target | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 3 | Pipeline | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Verified revenue | B | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 5 | Conversion | B | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 6 | Tenant | A | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 7 | Team scope | A | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 8 | Capacity | A | C | Integer limit (bounded) | Number input with unit | Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 9 | SLA | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 10 | Budget variance | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Intervention rate | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |

*Replace rules (doc 06 "Remove / replace"):* Team: authorized group only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/metrics/funnel` | C | API-537 | exact |
| GET | `/api/v1/tasks` | P | API-265 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_lead` → ENT-079 `crm_lead` (C); `growth_deal` → ENT-086 `crm_deal` (C); `growth_meeting` → ENT-103 `eng_meeting` (C); `growth_task` → ENT-148 `lcy_task` (C); `growth_metric_snapshot` → ENT-192 `ana_metric_snapshot` (C)

**Integrations (doc 06):** postgresql [OSS]

### 2.7.15.8 A082: Revenue and attribution dashboard

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | existing 092 · New · Workspace |
| FR · wave · epic · profiles | FR-A082 (alias SM-FR-A082, trace M52, SM-UX-FR-A082) · W5 · EP-15 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Reconcile attribution against verified revenue |
| Key actions (Part 2.5) | Change model, Export |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Track revenue, CAC and channel performance |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A083; A042; A060 |
| Tests | SM-UAT-S112; SM-UX-UAT-A082; unit families 001, 002, 003, 008, 009, 013, 045, 060, 061, 062, 063, 064; **TC-ENH-C-145** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 2 | Campaign | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Verified revenue | B+R | C | Verification state + evidence reference | StateBadge with evidence link | ledger-derived. Set only by the verification workflow; expiry enforced |
| 4 | Cost | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 5 | Conversion | B | P | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Attribution model revision | A | C | Attribution ID / event reference | Read-only text | First-party only; captured server-side |
| 8 | Currency basis | A | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 9 | Outcome ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 10 | Cost allocation | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Freshness | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |

*Replace rules (doc 06 "Remove / replace"):* Verified revenue: ledger-derived.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/metrics/revenue` | C | API-388 | exact |

**Tables → blueprint entities:** `growth_attribution_event` → ENT-124 `mkt_attribution_event` (C); `growth_invoice` → ENT-140 `com_invoice` (C); `growth_payment` → ENT-142 `com_payment` (C); `growth_metric_snapshot` → ENT-192 `ana_metric_snapshot` (C)

**Integrations (doc 06):** postgresql [OSS]; Socialinsider [CMU]; PostHog [ADP]

### 2.7.15.9 A083: Revenue reconciliation and KPI settings

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 093 · New · Admin |
| FR · wave · epic · profiles | FR-A083 (alias SM-FR-A083, trace M52, SM-UX-FR-A083) · W5 · EP-15 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Validate KPI formula and source provenance |
| Key actions (Part 2.5) | Edit draft, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Verify financial totals and definitions |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A082; A074; A087 |
| Tests | SM-UAT-S113; SM-UX-UAT-A083; unit families 001, 002, 015, 033, 040, 041, 060, 061, 062, 063, 064; **TC-ENH-C-146** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Metric | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Period | B | P | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |
| 3 | Source | B | P | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 4 | Currency | B | P | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 5 | Amount | B+R | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | read-only computed metric. Decimal only; currency required; server recomputes (CA-FIN) |
| 6 | Verification | B | P | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 7 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 8 | Metric definition | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Denominator | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | FX date | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Evidence reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 12 | Calculation version | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |

*Replace rules (doc 06 "Remove / replace"):* Amount: read-only computed metric.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/metrics/revenue` | C | API-388 | exact |
| POST | `/api/v1/admin/kpi-definitions` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_attribution_event` → ENT-124 `mkt_attribution_event` (C); `growth_invoice` → ENT-140 `com_invoice` (C); `growth_payment` → ENT-142 `com_payment` (C); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_metric_snapshot` → ENT-192 `ana_metric_snapshot` (C)

**Integrations (doc 06):** postgresql [OSS]; Socialinsider [CMU]; PostHog [ADP]

### 2.7.15.10 A087: Sales forecasting dashboard

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | existing 097 · New · Workspace |
| FR · wave · epic · profiles | FR-A087 (alias SM-FR-A087, trace M60, SM-UX-FR-A087) · W5 · EP-17 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Recalculate from shared pipeline and assumptions |
| Key actions (Part 2.5) | Change scenario |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | View weighted pipeline and forecasts |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A088; A029; A043 |
| Tests | SM-UAT-S117; SM-UX-UAT-A087; unit families 001, 002, 003, 008, 009, 013, 024, 025, 026, 027, 028, 045; **TC-ENH-C-147** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Team | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 2 | Period | B | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |
| 3 | Pipeline | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Weighted forecast | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | computed. Allowlisted, validated server-side |
| 5 | Confidence | B | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Currency basis | A | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 8 | Forecast as-of | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Scenario | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Model revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 11 | Confidence interval | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |

*Replace rules (doc 06 "Remove / replace"):* Weighted forecast: computed.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/metrics/forecast` | C | API-389 | exact |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_stage_metric` → ENT-197 `ana_stage_metric` (C); `growth_forecast` → ENT-196 `ana_forecast` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.15.11 A088: Forecast model settings

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 098 · Extension · Admin |
| FR · wave · epic · profiles | FR-A088 (alias SM-FR-A088, trace M60, SM-UX-FR-A088) · W5 · EP-17 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Backtest; approve or rollback forecast config |
| Key actions (Part 2.5) | Run backtest, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve assumptions and changes |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A087; A084; A083 |
| Tests | SM-UAT-S118; SM-UX-UAT-A088; unit families 001, 002, 003, 008, 009, 013, 024, 025, 026, 027, 028, 045; **TC-ENH-C-148** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Model | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 2 | Period | B | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |
| 3 | Stage weight | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 4 | Confidence | B+R | P | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | validated model result. Computed server-side; Unknown shown separately from 0 |
| 5 | Revision | B | P | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Training period | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |
| 8 | Backtest results | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Stage weights version | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 10 | Calibration | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Approval | A | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |

*Replace rules (doc 06 "Remove / replace"):* Confidence: validated model result.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/metrics/forecast` | C | API-389 | exact |
| POST | `/api/v1/admin/forecast-settings` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_stage_metric` → ENT-197 `ana_stage_metric` (C); `growth_forecast` → ENT-196 `ana_forecast` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.15.12 A089: Unified admin command centre

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | existing 099 · Extension · Admin |
| FR · wave · epic · profiles | FR-A089 (alias SM-FR-A089, trace M25; M61, SM-UX-FR-A089) · W2 shell / W5 · EP-17 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Aggregate seven views; drill down; avoid portfolio mutation |
| Key actions (Part 2.5) | Open view, Decide approval (single startup only) |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Consolidate live operational metrics and approvals |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A042; A029; A106; A102; A110 |
| Tests | SM-UAT-S119; SM-UX-UAT-A089; unit families 001, 002, 015, 016, 017, 018, 019, 032, 033, 036, 047; **TC-ENH-C-149** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Startup | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | dynamic authorized directory. Must belong to the same tenant and startup (composite FK) |
| 2 | Qualified leads | B | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 3 | Pipeline | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Verified revenue | B | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 5 | Conversion | B | P | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 6 | Tenant | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 7 | Objective | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | Offering | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Concurrent runs | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Held actions | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Budget remaining | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 12 | Freshness | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |

*Replace rules (doc 06 "Remove / replace"):* Startup: dynamic authorized directory.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/approvals` | P | API-540 | resource-equivalent DERIVED path on same screen |
| GET | `/api/v1/admin/dashboard` | C | API-538 | exact |
| POST | `/api/v1/admin/approvals/{id}/decide` | C | API-539 | exact |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_message_draft` → ENT-091 `eng_message_draft` (C); `growth_metric_snapshot` → ENT-192 `ana_metric_snapshot` (C); `growth_admin_projection` → ENT-194 `ana_admin_projection` (C)

**Integrations (doc 06):** react [OSS]

### 2.7.15.13 A097: Future product catalog view

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 107 · Extension · Workspace |
| FR · wave · epic · profiles | FR-A097 (alias SM-FR-A097, trace M66, SM-UX-FR-A097) · W6 · EP-02 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Track product readiness without publishing draft claims |
| Key actions (Part 2.5) | Open, Request launch |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Show internal planned status, not public promotion |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A098; A004; A005 |
| Tests | SM-UAT-S127; SM-UX-UAT-A097; unit families 001, 002, 014, 015; **TC-ENH-C-150** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Startup | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Category | B | P | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Readiness | B+R | C | Computed indicator | Indicator badge or tile (read-only) | computed. Computed server-side with as_of; Unknown shown separately |
| 5 | Revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 6 | Status | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Capability code | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | Launch dependency | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Evidence revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 10 | Publication status | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 11 | Target region | A | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |

*Replace rules (doc 06 "Remove / replace"):* Readiness: computed.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/products/planned` | P | API-064 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_product` → ENT-016 `cat_offering` (P); `growth_launch_approval` → ENT-023 `cat_launch_approval` (P)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.15.14 A098: Future product launch approval

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Overview · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 108 · Extension · Admin |
| FR · wave · epic · profiles | FR-A098 (alias SM-FR-A098, trace M66, SM-UX-FR-A098) · W6 · EP-02 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-04 Engagement, FLT-05 Operations (as_of), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Publish approved offering version only |
| Key actions (Part 2.5) | Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve evidence, availability and pricing |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A097; A051; A107 |
| Tests | SM-UAT-S128; SM-UX-UAT-A098; unit families 001, 002, 010, 011, 012, 013, 030; **TC-ENH-C-151** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Readiness | B | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 3 | Claim check | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 4 | Reviewer | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 5 | Approval | B+R | C | Approval reference (gov_approval) | Approval chip with approver and SLA | controlled. Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Launch revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Claims evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 9 | Pricing approval | A | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 10 | Release gate | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Rollback | A | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |

*Replace rules (doc 06 "Remove / replace"):* Approval: controlled.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/products/planned` | P | API-064 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/admin/products/{id}/launch` | C | API-050 | exact |

**Tables → blueprint entities:** `growth_product` → ENT-016 `cat_offering` (P); `growth_claim` → ENT-020 `cat_claim` (P); `growth_approval` → ENT-034 `gov_approval` (C); `growth_launch_approval` → ENT-023 `cat_launch_approval` (P)

**Integrations (doc 06):** Internal / no direct plugin [INT]


## 2.7.16 Admin: Discovery view

### 2.7.16.1 A015: Research planner

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-LIST + LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 016 · New · Workspace |
| FR · wave · epic · profiles | FR-A015 (alias SM-FR-A015, trace M07; M10; M11, SM-UX-FR-A015) · W1 · EP-05 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type); vertical: FLT-08…11 by capability profile |
| Automation (doc 06/17) | Schedule research within approved source and cost bounds |
| Key actions (Part 2.5) | New plan, Run now, Pause |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Choose product, segment, geography and search queries |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A016; A010; A023 |
| Tests | SM-UAT-S045; SM-UX-UAT-A015; unit families 001, 002, 024, 025, 026, 027, 028, 045; **TC-ENH-C-152** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Plan name | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Country | B | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 3 | Industry | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Organization type | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Source | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 6 | Frequency | B+R | C | Schedule rule (RRULE) | Schedule builder | conditional for trigger type. Bounded by caps and quiet hours |
| 7 | Budget | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 8 | Objective | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Source policy set | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 10 | Schedule timezone | A | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 11 | Max results | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 12 | Freshness SLA | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |

*Replace rules (doc 06 "Remove / replace"):* Frequency: conditional for trigger type.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sources` | C | API-158 | exact |
| GET | `/api/v1/research/plans` | P | API-160 | path match, method differs |
| POST | `/api/v1/research/plans` | C | API-160 | exact |
| POST | `/api/v1/research/run` | C | API-161 | exact |
| PATCH | `/api/v1/research/plans/{id}` | P | API-181 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_product` → ENT-016 `cat_offering` (P); `growth_job_run` → ENT-173 `ops_job_run` (C); `growth_source` → ENT-053 `intel_source` (C); `growth_source_policy` → ENT-054 `intel_source_policy` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_search_plan` → ENT-055 `intel_search_plan` (C); `growth_query_run` → ENT-056 `intel_query_run` (C); `growth_source_record` → ENT-057 `intel_source_record` (C); `growth_fetch_log` → ENT-058 `intel_fetch_log` (C)

**Integrations (doc 06):** tavily [ADP]; exa [ADP]; Tavily [ADP]

### 2.7.16.2 A016: Market discovery results

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 017 · New · Workspace |
| FR · wave · epic · profiles | FR-A016 (alias SM-FR-A016, trace M11; M12, SM-UX-FR-A016) · W1 · EP-05 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type); vertical: FLT-08…11 by capability profile |
| Automation (doc 06/17) | Deduplicate results; trigger qualification |
| Key actions (Part 2.5) | Open evidence, Send to review, Dismiss |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | View discovered organizations and public source links |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A017; A018; A019; A022 |
| Tests | SM-UAT-S046; SM-UX-UAT-A016; unit families 001, 002, 024, 025, 026, 027, 028, 045; **TC-ENH-C-153** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Country | B | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 3 | Industry | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Buying signal | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Source | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 6 | Evidence freshness | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 7 | Status | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | derived qualification stage. Changed only by controlled transition; never free text |
| 8 | Evidence ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | Signal confidence | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 10 | Objective | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 11 | Canonical organization | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 12 | Last verified | A | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |

*Replace rules (doc 06 "Remove / replace"):* Status: derived qualification stage.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/research/results` | C | API-162 | exact |
| GET | `/api/v1/research/runs/{id}` | P | API-183 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_search_plan` → ENT-055 `intel_search_plan` (C); `growth_query_run` → ENT-056 `intel_query_run` (C); `growth_source_record` → ENT-057 `intel_source_record` (C); `growth_fetch_log` → ENT-058 `intel_fetch_log` (C); `growth_evidence` → ENT-059 `intel_evidence` (C)

**Integrations (doc 06):** firecrawl [ADP]; Firecrawl [ADP]; Tavily [ADP]

### 2.7.16.3 A017: Evidence detail panel

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · Drawer |
| Legacy screen ID · build class · location class (doc 06) | existing 018 · New · Workspace |
| FR · wave · epic · profiles | FR-A017 (alias SM-FR-A017, trace M08; M12, SM-UX-FR-A017) · W1 · EP-05 · CA-ALL, CA-ADMIN, CA-AI |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Refresh evidence; invalidate stale derived scores |
| Key actions (Part 2.5) | Mark irrelevant, Refresh |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Inspect source excerpts, dates and confidence |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A016; A020; A086 |
| Tests | SM-UAT-S047; SM-UX-UAT-A017; unit families 001, 002, 015, 024, 025, 026, 027, 028, 033, 034, 035, 036, 043, 044, 045; **TC-ENH-C-154** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Evidence | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 2 | Source | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 3 | Observed date | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 4 | Permission | B | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 5 | Confidence | B+R | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | evidence score not permission. Computed server-side; Unknown shown separately from 0 |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Content hash | A | C | char(64) SHA-256 | HashBadge (read-only) | Server-computed; never editable |
| 8 | Retrieved date | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 9 | Source permission revision | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 10 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Claim link | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |

*Replace rules (doc 06 "Remove / replace"):* Confidence: evidence score not permission.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/ai/runs` | C | API-135 | exact |
| GET | `/api/v1/evidence/{id}` | C | API-163 | exact |
| GET | `/api/v1/evidence` | P | API-163;API-186 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_embedding` → ENT-026 `cat_embedding` (P); `growth_prompt_version` → ENT-045 `ai_prompt_version` (C); `growth_model_run` → ENT-046 `ai_model_run` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_budget` → ENT-052 `ai_budget` (C); `growth_cost_ledger` → ENT-051 `ai_cost_ledger` (C); `growth_source_record` → ENT-057 `intel_source_record` (C); `growth_fetch_log` → ENT-058 `intel_fetch_log` (C); `growth_evidence` → ENT-059 `intel_evidence` (C)

**Integrations (doc 06):** firecrawl [ADP]; Firecrawl [ADP]; claude/openai api [ADP]; deepeval [OSS]; Agent SDK Dev [DEV]; Pydantic AI [OSS]

### 2.7.16.4 A019: Buying signals board

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-BOARD |
| Legacy screen ID · build class · location class (doc 06) | existing 020 · New · Workspace |
| FR · wave · epic · profiles | FR-A019 (alias SM-FR-A019, trace M14, SM-UX-FR-A019) · W1 · EP-05 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Create eligible opportunity from verified signals |
| Key actions (Part 2.5) | Confirm, Reject (reason), Override priority (reason) |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review business announcements and relevance |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A020; A022; A016 |
| Tests | SM-UAT-S049; SM-UX-UAT-A019; unit families 001, 002, 024, 025, 026, 027, 028, 045; **TC-ENH-C-155** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Signal | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Source | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 4 | Stage | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 5 | Priority | B+R | C | Enumeration | Badge / select | computed with override reason. Allowed values from configuration |
| 6 | Observed date | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 7 | Signal type | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 9 | Evidence ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 10 | Trigger event | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 11 | Assigned objective | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |

*Replace rules (doc 06 "Remove / replace"):* Priority: computed with override reason.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/signals` | C | API-166 | exact |
| POST | `/api/v1/signals/{id}/review` | C | API-167 | exact |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_evidence` → ENT-059 `intel_evidence` (C); `growth_signal_type` → ENT-066 `intel_signal_type` (C); `growth_signal` → ENT-067 `intel_signal` (C)

**Integrations (doc 06):** llm gateway [ADP]; llm [ADP]; Common Room [CMU]

### 2.7.16.5 A020: Business need review

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 021 · New · Workspace |
| FR · wave · epic · profiles | FR-A020 (alias SM-FR-A020, trace M15, SM-UX-FR-A020) · W1 · EP-05 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Classify need and route uncertain evidence |
| Key actions (Part 2.5) | Confirm, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Distinguish confirmed needs from inferred needs |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A021; A022; A017 |
| Tests | SM-UAT-S050; SM-UX-UAT-A020; unit families 001, 002, 024, 025, 026, 027, 028, 045; **TC-ENH-C-156** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Need | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Industry | B | P | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Urgency | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | derived with reason. Allowlisted, validated server-side |
| 5 | Evidence | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Need category | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 8 | Evidence revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 9 | Urgency basis | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Budget confidence | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Reviewer | A | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |

*Replace rules (doc 06 "Remove / replace"):* Urgency: derived with reason.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/needs` | C | API-168 | exact |
| POST | `/api/v1/needs/{id}/verify` | C | API-169 | exact |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_evidence` → ENT-059 `intel_evidence` (C); `growth_need` → ENT-068 `intel_need` (C); `growth_need_evidence` → ENT-069 `intel_need_evidence` (C)

**Integrations (doc 06):** llm gateway [ADP]; llm [ADP]

### 2.7.16.6 A021: Product solution matching

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 022 · New · Workspace |
| FR · wave · epic · profiles | FR-A021 (alias SM-FR-A021, trace M16; M08, SM-UX-FR-A021) · W1 · EP-05 · CA-ALL, CA-ADMIN, CA-AI |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Match approved offerings; block unsupported capability |
| Key actions (Part 2.5) | Recompute |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | See matched offering, evidence and limitations |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A020; A022; A005 |
| Tests | SM-UAT-S051; SM-UX-UAT-A021; unit families 001, 002, 015, 024, 025, 026, 027, 028, 033, 034, 035, 036, 043, 044, 045; **TC-ENH-C-157** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Business line | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Fit score | B+R | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | computed. Computed server-side; Unknown shown separately from 0 |
| 5 | Confidence | B | P | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Capability match | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | Match explanation | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Exclusion rule | A | C | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |
| 10 | Pricing revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 11 | Score revision | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |

*Replace rules (doc 06 "Remove / replace"):* Fit score: computed.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/matches` | P | API-192 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/matches/recompute` | C | API-170 | exact |

**Tables → blueprint entities:** `growth_product` → ENT-016 `cat_offering` (P); `growth_capability` → ENT-018 `cat_capability` (P); `growth_embedding` → ENT-026 `cat_embedding` (P); `growth_job_run` → ENT-173 `ops_job_run` (C); `growth_prompt_version` → ENT-045 `ai_prompt_version` (C); `growth_model_run` → ENT-046 `ai_model_run` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_budget` → ENT-052 `ai_budget` (C); `growth_cost_ledger` → ENT-051 `ai_cost_ledger` (C); `growth_need` → ENT-068 `intel_need` (C); `growth_solution_match` → ENT-070 `intel_match` (P)

**Integrations (doc 06):** pgvector [OSS]

### 2.7.16.7 A022: Opportunity shortlist and scoring

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 023 · New · Workspace |
| FR · wave · epic · profiles | FR-A022 (alias SM-FR-A022, trace M17, SM-UX-FR-A022) · W1 · EP-06 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type); vertical: FLT-08…11 by capability profile |
| Automation (doc 06/17) | Prioritize eligible leads and deduplicate |
| Key actions (Part 2.5) | Recalculate, Open |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Prioritize opportunities with score explanation |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A024; A027; A029 |
| Tests | SM-UAT-S052; SM-UX-UAT-A022; unit families 001, 002, 024, 025, 026, 027, 028, 045; **TC-ENH-C-158** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Opportunity | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Fit score | B | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 5 | Priority | B+R | C | Enumeration | Badge / select | computed. Allowed values from configuration |
| 6 | Stage | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 8 | Opportunity ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | Score components | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 10 | Next action | A | C | Task reference + due timestamp | Inline task chip | Due date required; owner required |
| 11 | Conflict state | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 12 | Freshness | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |

*Replace rules (doc 06 "Remove / replace"):* Priority: computed.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/opportunities` | C | API-171 | exact |
| POST | `/api/v1/opportunities/{id}/score` | C | API-172 | exact |

**Tables → blueprint entities:** `growth_solution_match` → ENT-070 `intel_match` (P); `growth_opportunity` → ENT-072 `intel_opportunity` (C); `growth_score_version` → ENT-073 `intel_score_version` (P)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.16.8 A023: Research rules and scoring settings

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 024 · New · Admin |
| FR · wave · epic · profiles | FR-A023 (alias SM-FR-A023, trace M10; M11; M12; M13; M14; M15; M16; M17, SM-UX-FR-A023) · W1 · EP-06 · CA-ALL, CA-ADMIN, CA-CONFIG, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Simulate rules; approve version before activation |
| Key actions (Part 2.5) | Simulate, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Manage taxonomy, evidence quality, weights and review rules |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A015; A022; A028 |
| Tests | SM-UAT-S053; SM-UX-UAT-A023; unit families 001, 002, 024, 025, 026, 027, 028, 045; **TC-ENH-C-159** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Rule | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Industry | B | P | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 3 | Signal weight | B | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 4 | Fit threshold | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | validated numeric domain. Allowlisted, validated server-side |
| 5 | Confidence | B | P | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Scoring version | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Validation dataset | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Weight sum | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 10 | Exclusions | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Approval | A | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |

*Replace rules (doc 06 "Remove / replace"):* Fit threshold: validated numeric domain.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/research/plans` | P | API-160 | path match, method differs |
| POST | `/api/v1/research/plans` | C | API-160 | exact |
| PATCH | `/api/v1/research/plans/{id}` | P | API-181 | resource-equivalent path elsewhere in catalogue |
| GET | `/api/v1/research/runs/{id}` | P | API-135;API-139;API-147;API-148 | resource-equivalent path elsewhere in catalogue |
| GET | `/api/v1/evidence` | P | API-163;API-186 | resource-equivalent path elsewhere in catalogue |
| GET | `/api/v1/organizations` | C | API-164 | exact |
| GET | `/api/v1/signals` | C | API-166 | exact |
| POST | `/api/v1/admin/signal-types` | N | — | no exact or equivalent operation |
| GET | `/api/v1/needs` | C | API-168 | exact |
| GET | `/api/v1/matches` | P | API-192 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/admin/scoring-rules` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_product` → ENT-016 `cat_offering` (P); `growth_capability` → ENT-018 `cat_capability` (P); `growth_source` → ENT-053 `intel_source` (C); `growth_search_plan` → ENT-055 `intel_search_plan` (C); `growth_query_run` → ENT-056 `intel_query_run` (C); `growth_source_record` → ENT-057 `intel_source_record` (C); `growth_fetch_log` → ENT-058 `intel_fetch_log` (C); `growth_evidence` → ENT-059 `intel_evidence` (C); `growth_organization` → ENT-063 `intel_organization` (C); `growth_org_location` → ENT-064 `intel_location` (P); `growth_org_alias` → ENT-065 `intel_alias` (P); `growth_signal_type` → ENT-066 `intel_signal_type` (C); `growth_signal` → ENT-067 `intel_signal` (C); `growth_need` → ENT-068 `intel_need` (C); `growth_need_evidence` → ENT-069 `intel_need_evidence` (C); `growth_solution_match` → ENT-070 `intel_match` (P); `growth_score_version` → ENT-073 `intel_score_version` (P)

**Integrations (doc 06):** tavily [ADP]; exa [ADP]; Tavily [ADP]; firecrawl [ADP]; Firecrawl [ADP]; Clay [CMU]; Leadfeeder [CMU]; llm gateway [ADP]; llm [ADP]; Common Room [CMU]; pgvector [OSS]

### 2.7.16.9 A024: Decision-maker and contact discovery

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 025 · New · Workspace |
| FR · wave · epic · profiles | FR-A024 (alias SM-FR-A024, trace M18, SM-UX-FR-A024) · W1 · EP-06 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Discover only permitted professional contacts |
| Key actions (Part 2.5) | Queue discovery, Open |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | View business roles and licensed contact candidates; Apollo pilot |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A025; A026; A032 |
| Tests | SM-UAT-S054; SM-UX-UAT-A024; unit families 001, 002, 015, 020, 021, 022, 023, 024, 046, 053, 054, 066; **TC-ENH-C-160** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contact | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Role | B | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 4 | Channel | B+R | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | capability gated. Only channels enabled and eligible for scope |
| 5 | Eligibility | B | P | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Contact ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Source entitlement | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 9 | Verified identity | A | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 10 | Consent scope | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 11 | Preferred language | A | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |

*Replace rules (doc 06 "Remove / replace"):* Channel: capability gated.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/organizations/{id}/contacts` | C | API-173 | exact |
| POST | `/api/v1/organizations/{id}/contacts/discover` | P | API-196 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_contact` → ENT-074 `intel_contact` (C); `growth_job_run` → ENT-173 `ops_job_run` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_organization` → ENT-063 `intel_organization` (C); `growth_role_hypothesis` → ENT-075 `intel_role_hypothesis` (C); `growth_contact_source` → ENT-076 `intel_contact_source` (C); `growth_contact_verification` → ENT-077 `intel_contact_verification` (C)

**Integrations (doc 06):** hunter [ADP]; Apollo.io [ADP]; Endgame [CMU]

### 2.7.16.10 A025: Contact verification queue

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 026 · New · Workspace |
| FR · wave · epic · profiles | FR-A025 (alias SM-FR-A025, trace M19; M18, SM-UX-FR-A025) · W1 · EP-06 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Verify allowed channels and refresh evidence |
| Key actions (Part 2.5) | Verify, Correct, Mark failed |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Check source, freshness and verification status |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A026; A024; A027 |
| Tests | SM-UAT-S055; SM-UX-UAT-A025; unit families 001, 002, 015, 020, 021, 022, 023, 024, 046, 053, 054, 066; **TC-ENH-C-161** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contact | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 4 | Verification | B+R | C | Verification state + evidence reference | StateBadge with evidence link | computed status. Set only by the verification workflow; expiry enforced |
| 5 | Evidence | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 6 | Status | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Verification method | A | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 8 | Evidence revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 9 | Verified at | A | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 10 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Failure reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |

*Replace rules (doc 06 "Remove / replace"):* Verification: computed status.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/contacts/verification-queue` | N | — | no exact or equivalent operation |
| POST | `/api/v1/contacts/{id}/verify` | C | API-174 | exact |
| PATCH | `/api/v1/contacts/{id}` | P | API-197 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_contact` → ENT-074 `intel_contact` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_organization` → ENT-063 `intel_organization` (C); `growth_contact_source` → ENT-076 `intel_contact_source` (C); `growth_contact_verification` → ENT-077 `intel_contact_verification` (C)

**Integrations (doc 06):** hunter [ADP]; Apollo.io [ADP]; Hunter [ADP]; Clay [CMU]

### 2.7.16.11 A026: Contact quality and role mapping

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 027 · New · Admin |
| FR · wave · epic · profiles | FR-A026 (alias SM-FR-A026, trace M13; M18; M19; B-QA, SM-UX-FR-A026) · W1 · EP-06 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Normalize role and route uncertain match |
| Key actions (Part 2.5) | Merge, Remap role |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Resolve conflicts, duplicates and role mappings |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A025; A027; A032 |
| Tests | SM-UAT-S056; SM-UX-UAT-A026; unit families 001, 002, 015, 020, 021, 022, 023, 024, 046, 053, 054, 066; **TC-ENH-C-162** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contact | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Role | B | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 4 | Confidence | B+R | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | qualified score. Computed server-side; Unknown shown separately from 0 |
| 5 | Verified date | B | P | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Role taxonomy | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 8 | Identity match confidence | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 9 | Source revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 10 | Decision authority | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Reviewer | A | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |

*Replace rules (doc 06 "Remove / replace"):* Confidence: qualified score.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/organizations/{id}/merge` | P | API-190;API-198 | resource-equivalent DERIVED path on same screen |
| GET | `/api/v1/organizations/{id}/contacts` | C | API-173 | exact |
| POST | `/api/v1/admin/role-mappings` | P | API-199 | resource-equivalent DERIVED path on same screen |
| GET | `/api/v1/contacts/verification-queue` | N | — | no exact or equivalent operation |
| PATCH | `/api/v1/contacts/{id}` | P | API-197 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_contact` → ENT-074 `intel_contact` (C); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_organization` → ENT-063 `intel_organization` (C); `growth_org_alias` → ENT-065 `intel_alias` (P); `growth_role_hypothesis` → ENT-075 `intel_role_hypothesis` (C); `growth_contact_source` → ENT-076 `intel_contact_source` (C); `growth_contact_verification` → ENT-077 `intel_contact_verification` (C)

**Integrations (doc 06):** hunter [ADP]; Apollo.io [ADP]; Endgame [CMU]; Hunter [ADP]; Clay [CMU]; postgresql [OSS]

### 2.7.16.12 A027: Qualified opportunity review

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 028 · New · Workspace |
| FR · wave · epic · profiles | FR-A027 (alias SM-FR-A027, trace M17; M20, SM-UX-FR-A027) · W1 · EP-06 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type); vertical: FLT-08…11 by capability profile |
| Automation (doc 06/17) | Advance eligible opportunities and assign owner |
| Key actions (Part 2.5) | Accept (assign owner), Reject (reason) |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Accept or reject opportunities; see alerts |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A029; A032; A034 |
| Tests | SM-UAT-S057; SM-UX-UAT-A027; unit families 001, 002, 024, 025, 026, 027, 028, 045; **TC-ENH-C-163** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Opportunity | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Fit score | B+R | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | read-only. Computed server-side; Unknown shown separately from 0 |
| 5 | Owner | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Qualification reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 8 | Objective ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | Consent readiness | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 10 | Assignment rule | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 11 | Evidence expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Fit score: read-only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/opportunities` | C | API-171 | exact |
| POST | `/api/v1/opportunities/{id}/review` | C | API-175 | exact |
| GET | `/api/v1/alerts` | C | API-176 | exact |
| POST | `/api/v1/alerts/{id}/read` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_solution_match` → ENT-070 `intel_match` (P); `growth_opportunity` → ENT-072 `intel_opportunity` (C); `growth_score_version` → ENT-073 `intel_score_version` (P); `growth_review` → ENT-078 `intel_review` (C); `growth_notification` → ENT-174 `ops_notification` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.16.13 A028: Research approval and alert rules

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 029 · New · Admin |
| FR · wave · epic · profiles | FR-A028 (alias SM-FR-A028, trace M20, SM-UX-FR-A028) · W1 · EP-06 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Fire qualified alerts; suppress duplicates |
| Key actions (Part 2.5) | Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure review thresholds and queues |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A023; A015; A106 |
| Tests | SM-UAT-S058; SM-UX-UAT-A028; unit families 001, 002, 024, 025, 026, 027, 028, 045; **TC-ENH-C-164** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Rule | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Source | B | P | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 3 | Priority | B | P | Enumeration | Badge / select | Allowed values from configuration |
| 4 | Alert channel | B+R | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | approved eligible channel. Only channels enabled and eligible for scope |
| 5 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Trigger condition | A | C | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |
| 8 | Schedule timezone | A | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 9 | Dedup window | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 10 | Alert recipient | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Rule revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |

*Replace rules (doc 06 "Remove / replace"):* Alert channel: approved eligible channel.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/alerts` | C | API-176 | exact |
| POST | `/api/v1/admin/research-review-rules` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_review` → ENT-078 `intel_review` (C); `growth_notification` → ENT-174 `ops_notification` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.16.14 A048: Social listening feed

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 052 · New · Workspace |
| FR · wave · epic · profiles | FR-A048 (alias SM-FR-A048, trace M33, SM-UX-FR-A048) · W3 · EP-05 · CA-ALL, CA-ADMIN, CA-AI |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Ingest permitted mentions; alert eligible owners |
| Key actions (Part 2.5) | Promote to evidence, Dismiss |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review permitted organizational signals |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A049; A050; A085 |
| Tests | SM-UAT-S078; SM-UX-UAT-A048; unit families 001, 002, 024, 025, 026, 027, 028, 045, 060, 061, 062, 063, 064; **TC-ENH-C-165** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Mention | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Platform | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 3 | Topic | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Sentiment | B+R | C | Computed indicator | Indicator badge or tile (read-only) | model inference label. Computed server-side with as_of; Unknown shown separately |
| 5 | Source | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Permitted source ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Mention timestamp | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Attribution | A | C | Attribution ID / event reference | Read-only text | First-party only; captured server-side |
| 10 | Evidence freshness | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 11 | Review gate | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Sentiment: model inference label.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/social/signals` | C | API-177 | exact |

**Tables → blueprint entities:** `growth_source` → ENT-053 `intel_source` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_source_record` → ENT-057 `intel_source_record` (C); `growth_signal` → ENT-067 `intel_signal` (C); `growth_social_post` → ENT-060 `intel_social_post` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.16.15 A049: Social source permissions

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 053 · Extension · Admin |
| FR · wave · epic · profiles | FR-A049 (alias SM-FR-A049, trace M33, SM-UX-FR-A049) · W3 · EP-05 · CA-ALL, CA-ADMIN, CA-CONFIG, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Block unsupported social collection |
| Key actions (Part 2.5) | Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure authorized sources and quotas |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A048; A010; A053 |
| Tests | SM-UAT-S079; SM-UX-UAT-A049; unit families 001, 002, 024, 025, 026, 027, 028, 045, 060, 061, 062, 063, 064; **TC-ENH-C-166** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Platform | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 2 | Source | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 3 | Permission | B+R | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | explicit capability matrix. Purpose and policy revision recorded; withdrawal immediate |
| 4 | Access method | B | P | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 5 | Expiry | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Provider capability grant | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 8 | Data retention | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Permitted purpose | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Review expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Revocation | A | C | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |

*Replace rules (doc 06 "Remove / replace"):* Permission: explicit capability matrix.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/admin/social/sources` | P | API-206 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_integration` → ENT-040 `int_integration` (C); `growth_source` → ENT-053 `intel_source` (C); `growth_source_policy` → ENT-054 `intel_source_policy` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_source_record` → ENT-057 `intel_source_record` (C); `growth_signal` → ENT-067 `intel_signal` (C); `growth_social_post` → ENT-060 `intel_social_post` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.16.16 A085: Competitor and market watch

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 095 · New · Workspace |
| FR · wave · epic · profiles | FR-A085 (alias SM-FR-A085, trace M59, SM-UX-FR-A085) · W5 · EP-05 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Monitor allowed market signals and route review |
| Key actions (Part 2.5) | Review, Alert |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Track public developments and evidence |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A086; A016; A048 |
| Tests | SM-UAT-S115; SM-UX-UAT-A085; unit families 001, 002, 014, 015, 024, 025, 026, 027, 028, 045; **TC-ENH-C-167** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Industry | B | P | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 3 | Signal | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Source | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 5 | Observed date | B | P | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 6 | Status | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | evidence lifecycle. Changed only by controlled transition; never free text |
| 7 | Signal taxonomy | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 8 | Permitted source | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 9 | Evidence freshness | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 10 | Region | A | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 11 | Alert condition | A | C | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |

*Replace rules (doc 06 "Remove / replace"):* Status: evidence lifecycle.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/market/competitors` | C | API-178 | exact |

**Tables → blueprint entities:** `growth_evidence` → ENT-059 `intel_evidence` (C); `growth_competitor` → ENT-061 `intel_competitor` (C); `growth_market_event` → ENT-062 `intel_market_event` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.16.17 A086: Competitor source review

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Discovery · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 096 · Extension · Admin |
| FR · wave · epic · profiles | FR-A086 (alias SM-FR-A086, trace M59, SM-UX-FR-A086) · W5 · EP-05 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-03 Evidence, FLT-02 Geography, FLT-07 Commercial (need, customer/supplier type) |
| Automation (doc 06/17) | Block disallowed competitor source |
| Key actions (Part 2.5) | Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve monitoring sources |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A085; A010; A017 |
| Tests | SM-UAT-S116; SM-UX-UAT-A086; unit families 001, 002, 014, 015, 024, 025, 026, 027, 028, 045; **TC-ENH-C-168** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Source | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Permission | B+R | P | Consent / permission record reference | ConsentNotice or toggle with policy revision | explicit use scope. Purpose and policy revision recorded; withdrawal immediate |
| 4 | Evidence | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 5 | Reviewer | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Licence | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | Permitted purpose | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 10 | Evidence digest | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 11 | Decision reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |

*Replace rules (doc 06 "Remove / replace"):* Permission: explicit use scope.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/market/competitors` | C | API-178 | exact |
| POST | `/api/v1/admin/competitor-sources` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_source` → ENT-053 `intel_source` (C); `growth_source_policy` → ENT-054 `intel_source_policy` (C); `growth_evidence` → ENT-059 `intel_evidence` (C); `growth_competitor` → ENT-061 `intel_competitor` (C); `growth_market_event` → ENT-062 `intel_market_event` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]


## 2.7.17 Admin: Outreach & Marketing view

### 2.7.17.1 A034: Personalized outreach editor

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-EDITOR |
| Legacy screen ID · build class · location class (doc 06) | existing 036 · New · Workspace |
| FR · wave · epic · profiles | FR-A034 (alias SM-FR-A034, trace M24; M25; M26; M08, SM-UX-FR-A034) · W2 · EP-08 · CA-ALL, CA-ADMIN, CA-AI, CA-APPROVE, CA-DISPATCH |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Draft and evaluate channel/action preflight |
| Key actions (Part 2.5) | Generate draft, Edit, Submit for approval / Queue (if pre-approved) |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review AI draft and evidence before permitted send |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A035; A037; A032 |
| Tests | SM-UAT-S064; SM-UX-UAT-A034; unit families 001, 002, 015, 020, 021, 022, 023, 024, 025, 026, 027, 028, 045, 046; **TC-ENH-C-169** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contact | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Template | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Subject | B | P | Text (≤ 200) | Text input | Trimmed; required where marked |
| 5 | Eligibility | B | C | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 6 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 7 | Relationship ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Template revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 9 | Evidence citations | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 10 | Consent result | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 11 | Schedule | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 12 | Cost estimate | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |

*Replace rules (doc 06 "Remove / replace"):* Eligibility and Approval: computed gates.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/engagement/check` | C | API-068 | exact |
| POST | `/api/v1/messages/draft` | C | API-237 | exact |
| POST | `/api/v1/messages/drafts/{id}/review` | N | — | no exact or equivalent operation |
| POST | `/api/v1/messages/send` | C | API-238 | exact |

**Tables → blueprint entities:** `growth_message` → ENT-093 `eng_message` (C); `growth_thread` → ENT-092 `eng_thread` (C); `growth_consent` → ENT-027 `gov_consent` (C); `growth_outbox` → ENT-169 `ops_outbox` (C); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_suppression` → ENT-028 `gov_suppression` (C); `growth_claim` → ENT-020 `cat_claim` (P); `growth_approval` → ENT-034 `gov_approval` (C); `growth_embedding` → ENT-026 `cat_embedding` (P); `growth_prompt_version` → ENT-045 `ai_prompt_version` (C); `growth_model_run` → ENT-046 `ai_model_run` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_budget` → ENT-052 `ai_budget` (C); `growth_cost_ledger` → ENT-051 `ai_cost_ledger` (C); `growth_opportunity` → ENT-072 `intel_opportunity` (C); `growth_contact_verification` → ENT-077 `intel_contact_verification` (C); `growth_eligibility_decision` → ENT-031 `gov_eligibility_decision` (P); `growth_message_template` → ENT-090 `eng_message_template` (P); `growth_message_draft` → ENT-091 `eng_message_draft` (C)

**Integrations (doc 06):** claude api [ADP]; Sales [DEV]; Endgame [CMU]

### 2.7.17.2 A035: Message templates and approval queue

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-LIST + LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 037 · New · Admin |
| FR · wave · epic · profiles | FR-A035 (alias SM-FR-A035, trace M25; M27, SM-UX-FR-A035) · W2 · EP-08 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Validate templates and permitted localization |
| Key actions (Part 2.5) | New template, Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve claims, responses and escalations |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A034; A007; A051 |
| Tests | SM-UAT-S065; SM-UX-UAT-A035; unit families 001, 002, 015, 016, 017, 018, 019, 020, 021, 022, 023, 024, 032, 033, 036, 046, 047; **TC-ENH-C-170** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Template | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Language | B | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 4 | Revision | B | P | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 5 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | derived approval. Changed only by controlled transition; never free text |
| 7 | Variable schema | A | C | JSON Schema document (versioned) | Schema editor with validation report | Allowed field types only; validated before activation (CA-CONFIG) |
| 8 | Claims references | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Provider template ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 10 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Locale fallback | A | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |

*Replace rules (doc 06 "Remove / replace"):* Status: derived approval.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/message-templates` | N | — | no exact or equivalent operation |
| POST | `/api/v1/admin/message-templates` | N | — | no exact or equivalent operation |
| POST | `/api/v1/messages/drafts/{id}/review` | N | — | no exact or equivalent operation |
| GET | `/api/v1/admin/approvals` | P | API-540;API-542 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/threads/{id}/handoff` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_thread` → ENT-092 `eng_thread` (C); `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_task` → ENT-148 `lcy_task` (C); `growth_claim` → ENT-020 `cat_claim` (P); `growth_approval` → ENT-034 `gov_approval` (C); `growth_message_template` → ENT-090 `eng_message_template` (P); `growth_message_draft` → ENT-091 `eng_message_draft` (C); `growth_intent` → ENT-096 `eng_intent` (C)

**Integrations (doc 06):** claude api [ADP]; Sales [DEV]; Endgame [CMU]; llm [ADP]

### 2.7.17.3 A036: Email channel configuration

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 038 · New · Admin |
| FR · wave · epic · profiles | FR-A036 (alias SM-FR-A036, trace M05; M26, SM-UX-FR-A036) · W2 · EP-08 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Check sender health; pause invalid connection |
| Key actions (Part 2.5) | Add sender, Test, Disable |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure sender and sending limits |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A008; A037; A007 |
| Tests | SM-UAT-S066; SM-UX-UAT-A036; unit families 001, 002, 015, 020, 021, 022, 023, 024, 033, 040, 041, 046; **TC-ENH-C-171** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Sender | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Domain | B | C | URL / verified domain | URL input or link | https only; domain must be verified where it drives publication |
| 3 | Provider | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Daily limit | B+R | C | Integer limit (bounded) | Number input with unit | bounded by provider. Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 5 | Authentication | B | P | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Credential reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Domain verification | A | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 9 | SPF/DKIM/DMARC result | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Bounce rate | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 11 | Suppression | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |

*Replace rules (doc 06 "Remove / replace"):* Daily limit: bounded by provider; no secret values.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/admin/integrations` | P | API-097 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/admin/integrations/test` | C | API-096 | exact |

**Tables → blueprint entities:** `growth_message` → ENT-093 `eng_message` (C); `growth_thread` → ENT-092 `eng_thread` (C); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C); `growth_job_run` → ENT-173 `ops_job_run` (C); `growth_integration` → ENT-040 `int_integration` (C); `growth_credential_ref` → ENT-041 `int_credential_ref` (C); `growth_quota` → ENT-042 `int_quota` (P); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_delivery_event` → ENT-094 `eng_delivery_event` (C)

**Integrations (doc 06):** resend [ADP]; ses [ADP]; Resend [ADP]

### 2.7.17.4 A037: Unified inbox and outbox

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-INBOX |
| Legacy screen ID · build class · location class (doc 06) | existing 039 · New · Workspace |
| FR · wave · epic · profiles | FR-A037 (alias SM-FR-A037, trace M26; M27; M41, SM-UX-FR-A037) · W2 · EP-08 · CA-ALL, CA-ADMIN, CA-DISPATCH |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Unify channels; cancel inappropriate follow-ups |
| Key actions (Part 2.5) | Reply, Assign, Human takeover, Stop sequence |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | View email threads, delivery status and AI replies |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A032; A038; A069; A111 |
| Tests | SM-UAT-S067; SM-UX-UAT-A037; unit families 001, 002, 015, 033, 040, 041, 060, 061, 062, 063, 064; **TC-ENH-C-172** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contact | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Subject | B | P | Text (≤ 200) | Text input | Trimmed; required where marked |
| 4 | Response | B+R | P | Text (≤ 4,000) | Text area with counter | split inbound and draft. No secrets or special-category data; length limit |
| 5 | Owner | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Conversation ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Identity match | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Direction | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Intent | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Delivery receipt | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 12 | Human takeover | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 13 | Linked runs | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Response: split inbound and draft.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/messages/send` | C | API-238 | exact |
| POST | `/api/v1/webhooks/email` | C | API-239 | exact |
| GET | `/api/v1/messages/{id}` | N | — | no exact or equivalent operation |
| POST | `/api/v1/webhooks/inbound` | C | API-240 | exact |
| GET | `/api/v1/threads` | C | API-241 | exact |
| GET | `/api/v1/threads/{id}/messages` | N | — | no exact or equivalent operation |
| POST | `/api/v1/threads/{id}/handoff` | N | — | no exact or equivalent operation |
| GET | `/api/v1/inbox` | C | API-247 | exact |

**Tables → blueprint entities:** `growth_message` → ENT-093 `eng_message` (C); `growth_thread` → ENT-092 `eng_thread` (C); `growth_outbox` → ENT-169 `ops_outbox` (C); `growth_task` → ENT-148 `lcy_task` (C); `growth_suppression` → ENT-028 `gov_suppression` (C); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_eligibility_decision` → ENT-031 `gov_eligibility_decision` (P); `growth_message_draft` → ENT-091 `eng_message_draft` (C); `growth_intent` → ENT-096 `eng_intent` (C); `growth_delivery_event` → ENT-094 `eng_delivery_event` (C); `growth_identity_link` → ENT-097 `eng_identity_link` (C); `growth_routing_rule` → ENT-098 `eng_routing_rule` (C)

**Integrations (doc 06):** resend [ADP]; ses [ADP]; Resend [ADP]; llm [ADP]

### 2.7.17.5 A044: WhatsApp channel and templates

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 047 · New · Admin |
| FR · wave · epic · profiles | FR-A044 (alias SM-FR-A044, trace M31, SM-UX-FR-A044) · W3 · EP-10 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Check template and conversation eligibility |
| Key actions (Part 2.5) | Connect, Sync templates |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Connect WABA, approve templates and audit opt-in |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A045; A008; A007 |
| Tests | SM-UAT-S074; SM-UX-UAT-A044; unit families 001, 002, 015, 020, 021, 022, 023, 024, 046; **TC-ENH-C-173** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Template | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Sender | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | verified account only. Must belong to the same tenant and startup (composite FK) |
| 3 | Language | B | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 4 | Category | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 5 | Approval | B | P | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Business account ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Provider template ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | Opt-in evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 10 | Service window | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 11 | Health | A | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |

*Replace rules (doc 06 "Remove / replace"):* Sender: verified account only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/whatsapp/accounts` | N | — | no exact or equivalent operation |
| POST | `/api/v1/admin/whatsapp/accounts` | P | API-107 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/admin/whatsapp/templates` | P | API-108 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_message` → ENT-093 `eng_message` (C); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_integration` → ENT-040 `int_integration` (C); `growth_credential_ref` → ENT-041 `int_credential_ref` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_message_template` → ENT-090 `eng_message_template` (P); `growth_delivery_event` → ENT-094 `eng_delivery_event` (C); `growth_channel_account` → ENT-089 `eng_channel_account` (C)

**Integrations (doc 06):** meta cloud api [ADP]

### 2.7.17.6 A045: WhatsApp conversations

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-INBOX (same component as A037, channel filter) |
| Legacy screen ID · build class · location class (doc 06) | existing 048 · Extension · Workspace |
| FR · wave · epic · profiles | FR-A045 (alias SM-FR-A045, trace M26; M31; M41, SM-UX-FR-A045) · W3 · EP-10 · CA-ALL, CA-ADMIN, CA-DISPATCH |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Use same state as A037; no duplicate messaging engine |
| Key actions (Part 2.5) | Reply within window; template outside window |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Extend inbox with WhatsApp and channel ownership |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A037; A044; A032 |
| Tests | SM-UAT-S075; SM-UX-UAT-A045; unit families 001, 002, 015, 020, 021, 022, 023, 024, 046, 060, 061, 062, 063, 064; **TC-ENH-C-174** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Contact | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Channel | B | P | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Subject | B | P | Text (≤ 200) | Text input | Trimmed; required where marked |
| 4 | Response | B+R | P | Text (≤ 4,000) | Text area with counter | reuse unified thread composer. No secrets or special-category data; length limit |
| 5 | Owner | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Shared thread ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Service window | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 9 | Consent | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 10 | Delivery receipt | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Handover | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Response: reuse unified thread composer.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/messages/send` | C | API-238 | exact |
| GET | `/api/v1/webhooks/whatsapp` | C | API-249 | exact |
| POST | `/api/v1/webhooks/whatsapp` | C | API-245 | exact |
| GET | `/api/v1/whatsapp/conversations` | N | — | no exact or equivalent operation |
| GET | `/api/v1/inbox` | C | API-247 | exact |
| POST | `/api/v1/threads/{id}/assign` | C | API-248 | exact |

**Tables → blueprint entities:** `growth_message` → ENT-093 `eng_message` (C); `growth_thread` → ENT-092 `eng_thread` (C); `growth_outbox` → ENT-169 `ops_outbox` (C); `growth_suppression` → ENT-028 `gov_suppression` (C); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C); `growth_integration` → ENT-040 `int_integration` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_activity` → ENT-088 `crm_activity` (C); `growth_eligibility_decision` → ENT-031 `gov_eligibility_decision` (P); `growth_message_template` → ENT-090 `eng_message_template` (P); `growth_message_draft` → ENT-091 `eng_message_draft` (C); `growth_delivery_event` → ENT-094 `eng_delivery_event` (C); `growth_identity_link` → ENT-097 `eng_identity_link` (C); `growth_routing_rule` → ENT-098 `eng_routing_rule` (C); `growth_channel_account` → ENT-089 `eng_channel_account` (C)

**Integrations (doc 06):** meta cloud api [ADP]

### 2.7.17.7 A050: Content studio

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-EDITOR |
| Legacy screen ID · build class · location class (doc 06) | existing 054 · New · Workspace |
| FR · wave · epic · profiles | FR-A050 (alias SM-FR-A050, trace M34, SM-UX-FR-A050) · W3 · EP-11 · CA-ALL, CA-ADMIN, CA-AI |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Generate content drafts; verify evidence and brand |
| Key actions (Part 2.5) | Generate, Revise, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Create and edit branded marketing content |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A051; A052; A056 |
| Tests | SM-UAT-S080; SM-UX-UAT-A050; unit families 001, 002, 028, 029, 030, 031, 032; **TC-ENH-C-175** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Title | B | C | Text (≤ 200) | Text input | Trimmed; required where marked |
| 2 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 4 | Audience | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 6 | Approval | B+R | P | Approval reference (gov_approval) | Approval chip with approver and SLA | computed. Computed from Approval record; hash-bound (CA-APPROVE) |
| 7 | Content format | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Claim references | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 9 | Brand revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 10 | Locale | A | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 11 | Channel requirements | A | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 12 | Schedule | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Approval: computed.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/content` | P | API-299;API-300 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/content/draft` | C | API-284 | exact |
| PATCH | `/api/v1/content/{id}` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_content_version` → ENT-106 `mkt_content_version` (P); `growth_claim` → ENT-020 `cat_claim` (P); `growth_model_run` → ENT-046 `ai_model_run` (C); `growth_content_asset` → ENT-105 `mkt_content_asset` (C)

**Integrations (doc 06):** content studio [DEV]; Content Studio [DEV]; content-marketing [DEV]; Marketing [DEV]; seo-content-creation [DEV]; Skill Creator [DEV]; Canva [ADP]; PubMed [ADP]

### 2.7.17.8 A051: Content and claims approval

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 055 · Extension · Admin |
| FR · wave · epic · profiles | FR-A051 (alias SM-FR-A051, trace M25; M34, SM-UX-FR-A051) · W3 · EP-11 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Hold unsupported claims; version approvals |
| Key actions (Part 2.5) | Approve hash, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review clinical and brand claims |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A050; A057; A005 |
| Tests | SM-UAT-S081; SM-UX-UAT-A051; unit families 001, 002, 010, 011, 012, 013, 015, 016, 017, 018, 019, 030, 032, 033, 036, 047; **TC-ENH-C-176** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Content | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Claim | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 3 | Source | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 4 | Revision | B | P | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 5 | Reviewer | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B+R | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | controlled approval. Changed only by controlled transition; never free text |
| 7 | Claim ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Evidence expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 9 | Risk class | A | C | Enumeration | Badge / select | Allowed values from configuration |
| 10 | Approved content hash | A | C | char(64) SHA-256 | HashBadge (read-only) | Server-computed; never editable |
| 11 | Decision reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |

*Replace rules (doc 06 "Remove / replace"):* Status: controlled approval.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/approvals` | P | API-542 | resource-equivalent DERIVED path on same screen |
| GET | `/api/v1/content` | P | API-299;API-300 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/content/{id}/approve` | C | API-285 | exact |

**Tables → blueprint entities:** `growth_content_version` → ENT-106 `mkt_content_version` (P); `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_claim` → ENT-020 `cat_claim` (P); `growth_approval` → ENT-034 `gov_approval` (C); `growth_message_draft` → ENT-091 `eng_message_draft` (C); `growth_content_asset` → ENT-105 `mkt_content_asset` (C)

**Integrations (doc 06):** content studio [DEV]; Content Studio [DEV]; content-marketing [DEV]; Marketing [DEV]; seo-content-creation [DEV]; Skill Creator [DEV]; Canva [ADP]; PubMed [ADP]

### 2.7.17.9 A052: Social publishing calendar

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-CAL |
| Legacy screen ID · build class · location class (doc 06) | existing 056 · New · Workspace |
| FR · wave · epic · profiles | FR-A052 (alias SM-FR-A052, trace M35, SM-UX-FR-A052) · W3 · EP-11 · CA-ALL, CA-ADMIN, CA-DISPATCH |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Schedule approved publishing; reconcile unknown outcome |
| Key actions (Part 2.5) | Schedule, Cancel, Reconcile |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Schedule, preview and track approved posts |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A050; A053; A051 |
| Tests | SM-UAT-S082; SM-UX-UAT-A052; unit families 001, 002, 015, 033, 040, 041, 060, 061, 062, 063, 064; **TC-ENH-C-177** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Post | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Platform | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 3 | Date | B | P | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 4 | Timezone | B | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 5 | Approval | B+R | C | Approval reference (gov_approval) | Approval chip with approver and SLA | immutable revision check. Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Post revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Provider account | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Schedule timezone | A | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 10 | Delivery result | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Retry state | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |

*Replace rules (doc 06 "Remove / replace"):* Approval: immutable revision check.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/social/posts` | P | API-286 | path match, method differs |
| POST | `/api/v1/social/posts` | C | API-286 | exact |
| GET | `/api/v1/social/status` | C | API-287 | exact |
| POST | `/api/v1/social/posts/{id}/cancel` | P | API-303 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_content_version` → ENT-106 `mkt_content_version` (P); `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_channel_account` → ENT-089 `eng_channel_account` (C); `growth_social_publication` → ENT-107 `mkt_social_publication` (C)

**Integrations (doc 06):** postiz [ADP]; Postiz [ADP]; social-publishing [DEV]; Socialinsider [CMU]

### 2.7.17.10 A053: Social account and publishing controls

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 057 · Extension · Admin |
| FR · wave · epic · profiles | FR-A053 (alias SM-FR-A053, trace M35, SM-UX-FR-A053) · W3 · EP-11 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Enforce platform account permissions and quotas |
| Key actions (Part 2.5) | Connect, Revoke |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Authorize accounts and pause publishing |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A052; A049; A008 |
| Tests | SM-UAT-S083; SM-UX-UAT-A053; unit families 001, 002, 015, 033, 040, 041, 060, 061, 062, 063, 064; **TC-ENH-C-178** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Account | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Platform | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 3 | Permission | B+R | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | scoped. Purpose and policy revision recorded; withdrawal immediate |
| 4 | Daily limit | B | C | Integer limit (bounded) | Number input with unit | Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 5 | Health | B | P | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 6 | Status | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Credential reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Account ownership | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Capability grant | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 10 | Revocation | A | C | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |
| 11 | Rate remaining | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |

*Replace rules (doc 06 "Remove / replace"):* Permission: scoped; no tokens.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/social/posts` | P | API-286 | path match, method differs |
| GET | `/api/v1/social/status` | C | API-287 | exact |
| POST | `/api/v1/admin/social/accounts` | P | API-113;API-114 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/social/posts/{id}/cancel` | P | API-303 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_content_version` → ENT-106 `mkt_content_version` (P); `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_integration` → ENT-040 `int_integration` (C); `growth_credential_ref` → ENT-041 `int_credential_ref` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_channel_account` → ENT-089 `eng_channel_account` (C); `growth_social_publication` → ENT-107 `mkt_social_publication` (C)

**Integrations (doc 06):** postiz [ADP]; Postiz [ADP]; social-publishing [DEV]; Socialinsider [CMU]

### 2.7.17.11 A054: SEO and visibility dashboard

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | existing 058 · New · Workspace |
| FR · wave · epic · profiles | FR-A054 (alias SM-FR-A054, trace M36, SM-UX-FR-A054) · W3 · EP-11 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Collect authorized metrics; identify optimization tasks |
| Key actions (Part 2.5) | Queue audit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review keywords, site audit and search metrics |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A055; A056; A082 |
| Tests | SM-UAT-S084; SM-UX-UAT-A054; unit families 001, 002, 003, 008, 009, 013, 045, 060, 061, 062, 063, 064; **TC-ENH-C-179** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Page | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Keyword | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Impressions | B | C | Integer (computed) | Number (read-only) | Distinct records; Unknown ≠ 0 |
| 4 | Clicks | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 5 | Rank | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | sourced metric not editable. Allowlisted, validated server-side |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Property ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Period | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |
| 9 | Locale | A | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 10 | Metric source | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 11 | Indexability | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 12 | Freshness | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |

*Replace rules (doc 06 "Remove / replace"):* Rank: sourced metric not editable.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/seo/audit` | C | API-288 | exact |
| POST | `/api/v1/seo/audit/run` | P | API-134;API-138;API-161;API-533 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_job_run` → ENT-173 `ops_job_run` (C); `growth_keyword` → ENT-108 `mkt_keyword` (C); `growth_seo_issue` → ENT-109 `mkt_seo_issue` (C); `growth_page_metric` → ENT-110 `mkt_page_metric` (C)

**Integrations (doc 06):** search console [ADP]; seo-analysis-monitoring [DEV]; seo-content-creation [DEV]; seo-technical-optimization [DEV]; Writesonic [CMU]

### 2.7.17.12 A055: SEO review backlog

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 059 · New · Admin |
| FR · wave · epic · profiles | FR-A055 (alias SM-FR-A055, trace M36, SM-UX-FR-A055) · W3 · EP-11 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Queue proposed fixes; verify after change |
| Key actions (Part 2.5) | Assign, Verify fix |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve SEO actions |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A054; A056 |
| Tests | SM-UAT-S085; SM-UX-UAT-A055; unit families 001, 002, 060, 061, 062, 063, 064; **TC-ENH-C-180** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Page | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Issue | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 3 | Keyword | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Priority | B+R | C | Enumeration | Badge / select | derived. Allowed values from configuration |
| 5 | Owner | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Issue evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 8 | Impact estimate | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Page revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 10 | Validation method | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Change approval | A | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |

*Replace rules (doc 06 "Remove / replace"):* Priority: derived.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/seo/audit` | C | API-288 | exact |
| POST | `/api/v1/seo/tasks` | C | API-289 | exact |

**Tables → blueprint entities:** `growth_task` → ENT-148 `lcy_task` (C); `growth_keyword` → ENT-108 `mkt_keyword` (C); `growth_seo_issue` → ENT-109 `mkt_seo_issue` (C); `growth_page_metric` → ENT-110 `mkt_page_metric` (C)

**Integrations (doc 06):** search console [ADP]; seo-analysis-monitoring [DEV]; seo-content-creation [DEV]; seo-technical-optimization [DEV]; Writesonic [CMU]

### 2.7.17.13 A056: Landing page builder

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-EDITOR |
| Legacy screen ID · build class · location class (doc 06) | existing 060 · New · Workspace |
| FR · wave · epic · profiles | FR-A056 (alias SM-FR-A056, trace M37, SM-UX-FR-A056) · W3 · EP-12 · CA-ALL, CA-ADMIN, CA-AI |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Generate page drafts and capture permitted attribution |
| Key actions (Part 2.5) | Save, Preview link, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Create campaign pages and tracking links |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A057; A058; A107 |
| Tests | SM-UAT-S086; SM-UX-UAT-A056; unit families 001, 002, 010, 011, 012, 013, 030; **TC-ENH-C-181** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Page | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Audience | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | approved segment. Must belong to the same tenant and startup (composite FK) |
| 4 | Locale | B | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 5 | Revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 6 | Approval | B | P | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 7 | Brand revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | CTA route | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Form schema | A | C | JSON Schema document (versioned) | Schema editor with validation report | Allowed field types only; validated before activation (CA-CONFIG) |
| 10 | Tracking consent | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 11 | Preview URL | A | C | URL / verified domain | URL input or link | https only; domain must be verified where it drives publication |
| 12 | Claim references | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |

*Replace rules (doc 06 "Remove / replace"):* Audience: approved segment.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/landing-pages` | P | API-308 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/landing-pages` | P | API-309 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_content_version` → ENT-106 `mkt_content_version` (P); `growth_form` → ENT-080 `crm_form` (C); `growth_landing_page` → ENT-111 `mkt_landing_page` (C)

**Integrations (doc 06):** react [OSS]; Leadfeeder [CMU]; PostHog [ADP]

### 2.7.17.14 A057: Landing page approvals

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 062 · Extension · Admin |
| FR · wave · epic · profiles | FR-A057 (alias SM-FR-A057, trace M37, SM-UX-FR-A057) · W3 · EP-12 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Gate page publication and rollback |
| Key actions (Part 2.5) | Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve copy and forms |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A056; A108; A051 |
| Tests | SM-UAT-S087; SM-UX-UAT-A057; unit families 001, 002, 010, 011, 012, 013, 030; **TC-ENH-C-182** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Page | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Revision | B | P | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 3 | Reviewer | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 4 | Claim check | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 5 | Approval | B+R | C | Approval reference (gov_approval) | Approval chip with approver and SLA | controlled decision. Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Content hash | A | C | char(64) SHA-256 | HashBadge (read-only) | Server-computed; never editable |
| 8 | Accessibility result | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 9 | Privacy review | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Publish decision | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Approval: controlled decision.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/landing-pages` | P | API-308 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/landing-pages/{id}/publish` | P | API-073;API-223 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_content_version` → ENT-106 `mkt_content_version` (P); `growth_form` → ENT-080 `crm_form` (C); `growth_landing_page` → ENT-111 `mkt_landing_page` (C); `growth_approval` → ENT-034 `gov_approval` (C)

**Integrations (doc 06):** react [OSS]; Leadfeeder [CMU]; PostHog [ADP]

### 2.7.17.15 A058: Campaign builder and audience

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-EDITOR |
| Legacy screen ID · build class · location class (doc 06) | existing 063 · New · Workspace |
| FR · wave · epic · profiles | FR-A058 (alias SM-FR-A058, trace M38, SM-UX-FR-A058) · W3 · EP-12 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Simulate campaigns and hold until approval |
| Key actions (Part 2.5) | Simulate, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure campaigns, audiences and schedules |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A059; A060; A056 |
| Tests | SM-UAT-S088; SM-UX-UAT-A058; unit families 001, 002, 015, 033, 034, 035, 036, 043, 044, 060, 061, 062, 063, 064; **TC-ENH-C-183** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Campaign | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Audience | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | permitted segment. Must belong to the same tenant and startup (composite FK) |
| 4 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 5 | Budget | B+R | P | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | hard limit. Decimal only; currency required; server recomputes (CA-FIN) |
| 6 | Start date | B | P | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 7 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 8 | Objective ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | Audience permission | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 10 | Channel eligibility | A | C | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 11 | Schedule | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 12 | Spend cap | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 13 | Conversion event | A | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |

*Replace rules (doc 06 "Remove / replace"):* Budget: hard limit; Audience: permitted segment.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/campaigns` | P | API-292 | path match, method differs |
| POST | `/api/v1/campaigns` | C | API-292 | exact |

**Tables → blueprint entities:** `growth_audience` → ENT-117 `mkt_audience` (C); `growth_campaign` → ENT-115 `mkt_campaign` (C); `growth_campaign_version` → ENT-116 `mkt_campaign_version` (C)

**Integrations (doc 06):** content-marketing [DEV]; Marketing [DEV]

### 2.7.17.16 A059: Campaign approval and budgets

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 064 · New · Admin |
| FR · wave · epic · profiles | FR-A059 (alias SM-FR-A059, trace M25; M38, SM-UX-FR-A059) · W3 · EP-12 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Reserve authorized budget; block stale changes |
| Key actions (Part 2.5) | Approve, Reject, Suspend |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve audience, content and spend |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A058; A061; A060 |
| Tests | SM-UAT-S089; SM-UX-UAT-A059; unit families 001, 002, 015, 016, 017, 018, 019, 032, 033, 036, 047, 060, 061, 062, 063, 064; **TC-ENH-C-184** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Campaign | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Audience | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Channel | B | P | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 4 | Budget | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 5 | Reviewer | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B+R | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | approval lifecycle. Changed only by controlled transition; never free text |
| 7 | Budget reservation | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 8 | Approved campaign hash | A | C | char(64) SHA-256 | HashBadge (read-only) | Server-computed; never editable |
| 9 | Risk review | A | C | Enumeration | Badge / select | Allowed values from configuration |
| 10 | Decision reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 11 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Status: approval lifecycle.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/approvals` | P | API-540;API-542 | resource-equivalent path elsewhere in catalogue |
| GET | `/api/v1/campaigns` | P | API-292 | path match, method differs |
| POST | `/api/v1/campaigns/{id}/approve` | C | API-293 | exact |
| POST | `/api/v1/campaigns/{id}/pause` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_budget` → ENT-052 `ai_budget` (C); `growth_message_draft` → ENT-091 `eng_message_draft` (C); `growth_audience` → ENT-117 `mkt_audience` (C); `growth_campaign` → ENT-115 `mkt_campaign` (C); `growth_campaign_version` → ENT-116 `mkt_campaign_version` (C)

**Integrations (doc 06):** content-marketing [DEV]; Marketing [DEV]

### 2.7.17.17 A060: Paid advertising dashboard

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | existing 065 · New · Workspace |
| FR · wave · epic · profiles | FR-A060 (alias SM-FR-A060, trace M39, SM-UX-FR-A060) · W3 · EP-12 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Detect spend anomalies and reconcile metrics |
| Key actions (Part 2.5) | Create draft, Pause |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Draft ads and review metrics |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A059; A061; A082 |
| Tests | SM-UAT-S090; SM-UX-UAT-A060; unit families 001, 002, 003, 008, 009, 013, 045, 060, 061, 062, 063, 064; **TC-ENH-C-185** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Campaign | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Channel | B | P | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Spend | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 4 | Impressions | B | P | Integer (computed) | Number (read-only) | Distinct records; Unknown ≠ 0 |
| 5 | Conversions | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | measured read-only. Allowlisted, validated server-side |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Provider account | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | Attribution window | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 9 | Conversion source | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 10 | Cost per conversion | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Spend variance | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |

*Replace rules (doc 06 "Remove / replace"):* Conversions: measured read-only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/ads/drafts` | C | API-294 | exact |
| GET | `/api/v1/ads/metrics` | C | API-295 | exact |

**Tables → blueprint entities:** `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_budget` → ENT-052 `ai_budget` (C); `growth_channel_account` → ENT-089 `eng_channel_account` (C); `growth_campaign` → ENT-115 `mkt_campaign` (C); `growth_ad_campaign` → ENT-118 `mkt_ad_campaign` (C); `growth_ad_spend_event` → ENT-119 `mkt_spend_event` (P)

**Integrations (doc 06):** Adspirer [CMU]

### 2.7.17.18 A061: Advertising spend controls

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 066 · Extension · Admin |
| FR · wave · epic · profiles | FR-A061 (alias SM-FR-A061, trace M39, SM-UX-FR-A061) · W3 · EP-12 · CA-ALL, CA-ADMIN, CA-DISPATCH, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Enforce caps before chargeable actions |
| Key actions (Part 2.5) | Launch within cap, Pause |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve launch, cap spend and pause |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A060; A012; A059 |
| Tests | SM-UAT-S091; SM-UX-UAT-A061; unit families 001, 002, 015, 033, 034, 035, 036, 043, 044, 060, 061, 062, 063, 064; **TC-ENH-C-186** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Account | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Campaign | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Daily limit | B | C | Integer limit (bounded) | Number input with unit | Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 4 | Monthly limit | B | C | Integer limit (bounded) | Number input with unit | Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 5 | Currency | B | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 6 | Approval | B+R | P | Approval reference (gov_approval) | Approval chip with approver and SLA | controlled. Computed from Approval record; hash-bound (CA-APPROVE) |
| 7 | Reserved spend | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 8 | Actual spend | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 9 | Effective cap | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 10 | Account currency | A | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 11 | Emergency stop | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Approval: controlled.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/ads/metrics` | C | API-295 | exact |
| POST | `/api/v1/ads/{id}/launch` | P | API-318 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/ads/{id}/pause` | P | API-319 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_budget` → ENT-052 `ai_budget` (C); `growth_ad_campaign` → ENT-118 `mkt_ad_campaign` (C); `growth_ad_spend_event` → ENT-119 `mkt_spend_event` (P)

**Integrations (doc 06):** Adspirer [CMU]

### 2.7.17.19 A062: Webinar and demo event manager

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-CAL + LP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | existing 067 · New · Workspace |
| FR · wave · epic · profiles | FR-A062 (alias SM-FR-A062, trace M40, SM-UX-FR-A062) · W3 · EP-09 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Schedule event and permitted follow-up |
| Key actions (Part 2.5) | Create, Verify attendance |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Manage events and registrations |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A063; A038; A032 |
| Tests | SM-UAT-S092; SM-UX-UAT-A062; unit families 001, 002, 014, 015, 024, 060, 061, 062, 063, 064; **TC-ENH-C-187** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Event | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Date | B | P | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 4 | Timezone | B | P | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 5 | Registrations | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | derived metric. Allowlisted, validated server-side |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Capacity | A | C | Integer limit (bounded) | Number input with unit | Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 8 | Event format | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Host | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Registration ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 11 | Attendance | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 12 | Approved content revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |

*Replace rules (doc 06 "Remove / replace"):* Registrations: derived metric.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/events/business` | N | — | no exact or equivalent operation |
| POST | `/api/v1/events/business` | N | — | no exact or equivalent operation |
| POST | `/api/v1/webhooks/events` | C | API-297 | exact |

**Tables → blueprint entities:** `growth_business_event` → ENT-170 `ops_domain_event` (P); `growth_event_registration` → ENT-121 `mkt_registration` (P); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C); `growth_event_attendance` → ENT-122 `mkt_attendance` (P); `growth_product` → ENT-016 `cat_offering` (P)

**Integrations (doc 06):** zoom [ADP]; Zoom [ADP]

### 2.7.17.20 A063: Event and reminder settings

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 069 · New · Admin |
| FR · wave · epic · profiles | FR-A063 (alias SM-FR-A063, trace M40, SM-UX-FR-A063) · W3 · EP-09 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Send eligible reminders; stop on cancellation |
| Key actions (Part 2.5) | Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure events and approved reminders |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A062; A035; A039 |
| Tests | SM-UAT-S093; SM-UX-UAT-A063; unit families 001, 002, 014, 015, 024; **TC-ENH-C-188** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Event | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Interval | B | C | Schedule rule (RRULE) | Schedule builder | Bounded by caps and quiet hours |
| 4 | Consent | B+R | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | scoped. Purpose and policy revision recorded; withdrawal immediate |
| 5 | Template | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Quiet hours | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 8 | Channel eligibility | A | C | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 9 | Attendance trigger | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 10 | Stop rule | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 11 | Policy revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |

*Replace rules (doc 06 "Remove / replace"):* Consent: scoped.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/events/business` | N | — | no exact or equivalent operation |
| POST | `/api/v1/admin/events/{id}/settings` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_business_event` → ENT-170 `ops_domain_event` (P); `growth_event_registration` → ENT-121 `mkt_registration` (P); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C); `growth_event_attendance` → ENT-122 `mkt_attendance` (P); `growth_message_template` → ENT-090 `eng_message_template` (P)

**Integrations (doc 06):** zoom [ADP]; Zoom [ADP]

### 2.7.17.21 A064: Referral and partner approvals

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 071 · New · Admin |
| FR · wave · epic · profiles | FR-A064 (alias SM-FR-A064, trace M42, SM-UX-FR-A064) · W3 · EP-12 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Validate referrals; assign qualified opportunity |
| Key actions (Part 2.5) | Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review partners, referral policy and attribution |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A032; A077; A029 |
| Tests | SM-UAT-S094; SM-UX-UAT-A064; unit families 001, 002, 014, 015, 024, 060, 061, 062, 063, 064; **TC-ENH-C-189** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Partner | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Referral | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Source | B+R | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | permitted provenance. Must resolve to permitted, unexpired evidence |
| 5 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Partner ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Referral consent | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 9 | Attribution code | A | C | Attribution ID / event reference | Read-only text | First-party only; captured server-side |
| 10 | Commission approval | A | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 11 | Duplicate check | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Source: permitted provenance.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/referrals` | P | API-327 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/admin/referrals/{id}/review` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_lead` → ENT-079 `crm_lead` (C); `growth_partner` → ENT-153 `lcy_partner` (C); `growth_referral` → ENT-123 `mkt_referral` (C); `growth_approval` → ENT-034 `gov_approval` (C)

**Integrations (doc 06):** Crossbeam Skills [CMU]

### 2.7.17.22 A107: Website configuration and content management

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-EDITOR + LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | original A-ID · Template/typed configuration (doc 06 operating contract) · Admin (new interface) |
| FR · wave · epic · profiles | FR-A107 (alias SM-FR-A107, trace B-WEB; B-TENANT, SM-UX-FR-A107) · W2 · EP-19 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Generate white-label pages from scoped config |
| Key actions (Part 2.5) | Save draft, Request domain verification, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A108; A056; A051 |
| Tests | SM-UAT-S137; SM-UX-UAT-A107; unit families 001, 002, 003, 004, 005, 006, 007, 010, 011, 012, 013, 030; **TC-ENH-C-190** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Page | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Domain | B+R | C | URL / verified domain | URL input or link | verified selection. https only; domain must be verified where it drives publication |
| 3 | Locale | B | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 4 | Template | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 6 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 7 | Brand revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Domain verification | A | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 9 | Config schema | A | C | JSON Schema document (versioned) | Schema editor with validation report | Allowed field types only; validated before activation (CA-CONFIG) |
| 10 | Publication target | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Locale fallback | A | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 12 | Claim evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |

*Replace rules (doc 06 "Remove / replace"):* Domain: verified selection.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/admin/website/pages` | P | API-486 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/commercial/admin/website/pages` | P | API-487;API-489 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P); `growth_audit_event` → ENT-172 `ops_audit_event` (C)

### 2.7.17.23 A108: Website preview, approval, publishing and analytics

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Outreach & Marketing · LP-QUEUE + LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | original A-ID · Template/typed configuration (doc 06 operating contract) · Admin (new interface) |
| FR · wave · epic · profiles | FR-A108 (alias SM-FR-A108, trace B-WEB; B-TENANT, SM-UX-FR-A108) · W2 · EP-19 · CA-ALL, CA-ADMIN, CA-APPROVE, CA-DISPATCH |
| Filters | FLT-01 Scope, FLT-06 Marketing, FLT-04 Engagement, FLT-03 Evidence (claims), FLT-02 Geography (language, timezone) |
| Automation (doc 06/17) | Publish immutable approved snapshot; roll back safely |
| Key actions (Part 2.5) | Approve, Publish, Schedule, Roll back |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A107; A057; A082 |
| Tests | SM-UAT-S138; SM-UX-UAT-A108; unit families 001, 002, 010, 011, 012, 013, 030, 060, 061, 062, 063, 064; **TC-ENH-C-191** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Page | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 3 | Immutable hash | B+R | C | char(64) SHA-256 | HashBadge (read-only) | read-only. Server-computed; never editable |
| 4 | Reviewer | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 5 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Publication environment | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Preview URL | A | C | URL / verified domain | URL input or link | https only; domain must be verified where it drives publication |
| 9 | Publish schedule | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 10 | Rollback revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 11 | Access policy | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |

*Replace rules (doc 06 "Remove / replace"):* Immutable hash: read-only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/admin/website/pages` | P | API-290;API-486 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/commercial/admin/website/pages/{id}/control` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_website_publication` → ENT-112 `mkt_publication` (P); `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P); `growth_audit_event` → ENT-172 `ops_audit_event` (C)


## 2.7.18 Admin: Follow-ups view

### 2.7.18.1 A038: Follow-up sequences and tasks

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-LIST (tabs: Enrolments, Tasks) |
| Legacy screen ID · build class · location class (doc 06) | existing 040 · New · Workspace |
| FR · wave · epic · profiles | FR-A038 (alias SM-FR-A038, trace M28; M30, SM-UX-FR-A038) · W2 · EP-08 · CA-ALL, CA-ADMIN, CA-DISPATCH |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Trigger follow-up only if eligible; cancel on reply |
| Key actions (Part 2.5) | Enrol (eligible only), Stop, Complete task |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review scheduled actions, stop and response triggers |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A039; A040; A037 |
| Tests | SM-UAT-S068; SM-UX-UAT-A038; unit families 001, 002, 015, 020, 021, 022, 023, 024, 046, 048, 055; **TC-ENH-C-192** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Task | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Contact | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Sequence | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Due date | B+R | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | conditional on wait state. Stored UTC; displayed in user and record time zone; range validated |
| 5 | Priority | B | C | Enumeration | Badge / select | Allowed values from configuration |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Run ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Wait event | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Sequence revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 10 | Stop reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 11 | Deadline timezone | A | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 12 | SLA | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |

*Replace rules (doc 06 "Remove / replace"):* Due date: conditional on wait state.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sequences` | P | API-261 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sequences/{id}/enroll` | C | API-242 | exact |
| POST | `/api/v1/enrollments/{id}/stop` | P | API-264 | resource-equivalent DERIVED path on same screen |
| GET | `/api/v1/enrollments` | P | API-263 | resource-equivalent DERIVED path on same screen |
| GET | `/api/v1/tasks` | P | API-265 | resource-equivalent DERIVED path on same screen |
| PATCH | `/api/v1/tasks/{id}` | P | API-266 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_contact` → ENT-074 `intel_contact` (C); `growth_task` → ENT-148 `lcy_task` (C); `growth_enrollment` → ENT-102 `eng_enrollment` (C); `growth_eligibility_decision` → ENT-031 `gov_eligibility_decision` (P); `growth_sequence` → ENT-100 `eng_sequence` (C); `growth_sequence_step` → ENT-101 `eng_sequence_step` (C)

**Integrations (doc 06):** celery beat [OSS]; celery [OSS]; customer-sales-automation [DEV]; Sales [DEV]

### 2.7.18.2 A039: Follow-up policies

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 041 · New · Admin |
| FR · wave · epic · profiles | FR-A039 (alias SM-FR-A039, trace M28, SM-UX-FR-A039) · W2 · EP-08 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Coordinate contact timing and suppression |
| Key actions (Part 2.5) | Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve sequences and pause campaigns |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A038; A007; A033 |
| Tests | SM-UAT-S069; SM-UX-UAT-A039; unit families 001, 002, 015, 020, 021, 022, 023, 024, 046, 048, 055; **TC-ENH-C-193** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Policy | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Interval | B+R | C | Schedule rule (RRULE) | Schedule builder | conditional by channel. Bounded by caps and quiet hours |
| 4 | Max attempts | B | C | Integer (computed) | Number (read-only) | Distinct records; Unknown ≠ 0 |
| 5 | Stop condition | B | C | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Frequency cap scope | A | C | Schedule rule (RRULE) | Schedule builder | Bounded by caps and quiet hours |
| 8 | Quiet hours | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 9 | Consent check | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 10 | Max cumulative contacts | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Policy revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |

*Replace rules (doc 06 "Remove / replace"):* Interval: conditional by channel.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sequences` | P | API-261 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/admin/sequences` | P | API-262 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/enrollments/{id}/stop` | P | API-264;API-458 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_enrollment` → ENT-102 `eng_enrollment` (C); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_message_template` → ENT-090 `eng_message_template` (P); `growth_sequence` → ENT-100 `eng_sequence` (C); `growth_sequence_step` → ENT-101 `eng_sequence_step` (C)

**Integrations (doc 06):** celery beat [OSS]; celery [OSS]; customer-sales-automation [DEV]; Sales [DEV]

### 2.7.18.3 A040: Meeting calendar and agenda

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-CAL |
| Legacy screen ID · build class · location class (doc 06) | existing 042 · New · Workspace |
| FR · wave · epic · profiles | FR-A040 (alias SM-FR-A040, trace M29, SM-UX-FR-A040) · W2 · EP-09 · CA-ALL, CA-ADMIN, CA-DISPATCH |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Coordinate booking, reminders and action items |
| Key actions (Part 2.5) | Book slot, Reschedule, Record outcome |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Manage demos, appointments and meeting briefs |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A041; A032; A038 |
| Tests | SM-UAT-S070; SM-UX-UAT-A040; unit families 001, 002, 014, 015, 024; **TC-ENH-C-194** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Meeting | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Date | B+R | P | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | validated slot. Stored UTC; displayed in user and record time zone; range validated |
| 4 | Timezone | B | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 5 | Owner | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Slot ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Provider | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Booking state | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 10 | Attendees | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Meeting outcome | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 12 | Approved notes | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |

*Replace rules (doc 06 "Remove / replace"):* Date: validated slot.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/meetings` | P | API-268 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/meetings/book` | C | API-243 | exact |
| POST | `/api/v1/webhooks/calendar` | C | API-244 | exact |

**Tables → blueprint entities:** `growth_calendar_link` → ENT-104 `eng_calendar_link` (C); `growth_deal` → ENT-086 `crm_deal` (C); `growth_meeting` → ENT-103 `eng_meeting` (C); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C)

**Integrations (doc 06):** calendar api [ADP]

### 2.7.18.4 A041: Calendar configuration

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 044 · New · Admin |
| FR · wave · epic · profiles | FR-A041 (alias SM-FR-A041, trace M29, SM-UX-FR-A041) · W2 · EP-09 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Sync slots and prevent double bookings |
| Key actions (Part 2.5) | Connect, Test sync |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Set availability and assignment rules |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A040; A008 |
| Tests | SM-UAT-S071; SM-UX-UAT-A041; unit families 001, 002, 003, 004, 005, 006, 007, 014, 015, 024; **TC-ENH-C-195** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Calendar | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Provider | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Timezone | B | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 4 | Availability | B+R | P | Computed indicator | Indicator badge or tile (read-only) | provider-scoped. Computed server-side with as_of; Unknown shown separately |
| 5 | Buffer | B | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Calendar identity | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | OAuth grant reference | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 9 | Sync health | A | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 10 | Work hours | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Conflict policy | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |

*Replace rules (doc 06 "Remove / replace"):* Availability: provider-scoped.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/admin/calendar-links` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_calendar_link` → ENT-104 `eng_calendar_link` (C); `growth_meeting` → ENT-103 `eng_meeting` (C); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C); `growth_integration` → ENT-040 `int_integration` (C)

**Integrations (doc 06):** calendar api [ADP]

### 2.7.18.5 A075: Customer onboarding checklist

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | existing 084 · New · Workspace |
| FR · wave · epic · profiles | FR-A075 (alias SM-FR-A075, trace M48, SM-UX-FR-A075) · W4 · EP-16 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Instantiate offering-specific onboarding |
| Key actions (Part 2.5) | Complete step, Request document |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Manage handoff and onboarding tasks |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A076; A077; A032 |
| Tests | SM-UAT-S105; SM-UX-UAT-A075; unit families 001, 002, 014, 015; **TC-ENH-C-196** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Customer | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Stage | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | controlled. Changed only by controlled transition; never free text |
| 4 | Owner | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 5 | Due date | B | P | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Onboarding template | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | Task dependencies | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Entitlement | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 10 | Customer acknowledgment | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 11 | Risk flag | A | C | Enumeration | Badge / select | Allowed values from configuration |

*Replace rules (doc 06 "Remove / replace"):* Stage: controlled.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/onboarding` | C | API-412 | exact |
| POST | `/api/v1/onboarding/{id}/complete` | C | API-413 | exact |

**Tables → blueprint entities:** `sales_external_access_grant` → ENT-009 `ten_portal_grant` (P); `growth_onboarding` → ENT-147 `lcy_onboarding` (C); `growth_document` → ENT-024 `cat_document` (P); `growth_handoff` → ENT-149 `lcy_handoff` (C); `growth_task` → ENT-148 `lcy_task` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.18.6 A076: Onboarding assignment

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 086 · Extension · Admin |
| FR · wave · epic · profiles | FR-A076 (alias SM-FR-A076, trace M48, SM-UX-FR-A076) · W4 · EP-16 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Assign, remind and escalate overdue tasks |
| Key actions (Part 2.5) | Assign, Escalate |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Assign owner and SLA |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A075; A077; A079 |
| Tests | SM-UAT-S106; SM-UX-UAT-A076; unit families 001, 002, 014, 015; **TC-ENH-C-197** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Customer | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Task | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Owner | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 4 | Due date | B+R | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | timezone-aware. Stored UTC; displayed in user and record time zone; range validated |
| 5 | Priority | B | P | Enumeration | Badge / select | Allowed values from configuration |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Task dependency | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | SLA | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 9 | Required evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 10 | Assignment rule | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 11 | Escalation | A | C | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |

*Replace rules (doc 06 "Remove / replace"):* Due date: timezone-aware.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/onboarding` | C | API-412 | exact |
| POST | `/api/v1/onboarding/{id}/assign` | P | API-425 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_onboarding` → ENT-147 `lcy_onboarding` (C); `growth_handoff` → ENT-149 `lcy_handoff` (C); `growth_task` → ENT-148 `lcy_task` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.18.7 A077: Partner deployment pipeline

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-BOARD |
| Legacy screen ID · build class · location class (doc 06) | existing 087 · New · Workspace |
| FR · wave · epic · profiles | FR-A077 (alias SM-FR-A077, trace M49, SM-UX-FR-A077) · W4 · EP-16 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Coordinate partner readiness and deployment |
| Key actions (Part 2.5) | Create partner/pilot, Transition |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Track site, pilot and readiness |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A078; A075; A079 |
| Tests | SM-UAT-S107; SM-UX-UAT-A077; unit families 001, 002, 003, 008, 009, 013, 045, 053, 054, 066; **TC-ENH-C-198** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Partner | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Stage | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | controlled transition. Changed only by controlled transition; never free text |
| 4 | Delivery region | B | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 5 | Owner | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Due date | B | P | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 7 | Deployment template | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 8 | Milestone evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 9 | Capacity | A | C | Integer limit (bounded) | Number input with unit | Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 10 | Region eligibility | A | C | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 11 | Block reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |

*Replace rules (doc 06 "Remove / replace"):* Stage: controlled transition.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/partners` | P | API-414 | path match, method differs |
| POST | `/api/v1/partners` | C | API-414 | exact |
| POST | `/api/v1/pilots/{id}/status` | C | API-415 | exact |
| POST | `/api/v1/partner-pilots` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_partner` → ENT-153 `lcy_partner` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_organization` → ENT-063 `intel_organization` (C); `growth_pilot` → ENT-154 `lcy_pilot` (C); `growth_deployment` → ENT-155 `lcy_deployment` (C)

**Integrations (doc 06):** Crossbeam Skills [CMU]

### 2.7.18.8 A078: Deployment readiness approval

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 088 · New · Admin |
| FR · wave · epic · profiles | FR-A078 (alias SM-FR-A078, trace M49, SM-UX-FR-A078) · W4 · EP-16 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Block deployment if mandatory checks fail |
| Key actions (Part 2.5) | Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve site and pilot readiness |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A077; A075; A090 |
| Tests | SM-UAT-S108; SM-UX-UAT-A078; unit families 001, 002, 003, 008, 009, 013, 045, 053, 054, 066; **TC-ENH-C-199** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Partner | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Checklist | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Reviewer | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 5 | Approval | B+R | C | Approval reference (gov_approval) | Approval chip with approver and SLA | controlled. Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Checklist revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Evidence digest | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 9 | Capability checks | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 10 | Decision reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 11 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Approval: controlled.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/partners` | P | API-414 | path match, method differs |
| POST | `/api/v1/pilots/{id}/status` | C | API-415 | exact |

**Tables → blueprint entities:** `growth_partner` → ENT-153 `lcy_partner` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_pilot` → ENT-154 `lcy_pilot` (C); `growth_deployment` → ENT-155 `lcy_deployment` (C)

**Integrations (doc 06):** Crossbeam Skills [CMU]

### 2.7.18.9 A079: Renewal and retention calendar

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-CAL + LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 089 · New · Workspace |
| FR · wave · epic · profiles | FR-A079 (alias SM-FR-A079, trace M50, SM-UX-FR-A079) · W4 · EP-16 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Trigger eligible reminders and renewal review |
| Key actions (Part 2.5) | Review, Start renewal |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Track renewals and permitted reminders |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A080; A032; A081 |
| Tests | SM-UAT-S109; SM-UX-UAT-A079; unit families 001, 002, 014, 015, 024, 065, 066; **TC-ENH-C-200** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Customer | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Date | B | P | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 4 | Amount | B+R | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | approved renewal price. Decimal only; currency required; server recomputes (CA-FIN) |
| 5 | Owner | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Renewal ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Contract expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 9 | Entitlement | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 10 | Consent | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 11 | Next action | A | C | Task reference + due timestamp | Inline task chip | Due date required; owner required |
| 12 | Risk score | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |

*Replace rules (doc 06 "Remove / replace"):* Amount: approved renewal price.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/renewals` | C | API-416 | exact |
| POST | `/api/v1/renewals/{id}/review` | C | API-417 | exact |

**Tables → blueprint entities:** `growth_renewal` → ENT-150 `lcy_renewal` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_subscription` → ENT-151 `lcy_customer_subscription` (P); `growth_account_metric` → ENT-152 `lcy_account_metric` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.18.10 A080: Renewal policies

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 090 · Extension · Admin |
| FR · wave · epic · profiles | FR-A080 (alias SM-FR-A080, trace M50, SM-UX-FR-A080) · W4 · EP-16 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Stop reminders on renewal, opt-out or cancellation |
| Key actions (Part 2.5) | Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Manage cancellation and reminder rules |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A079; A039; A038 |
| Tests | SM-UAT-S110; SM-UX-UAT-A080; unit families 001, 002, 014, 015, 024, 065, 066; **TC-ENH-C-201** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Policy | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Interval | B+R | C | Schedule rule (RRULE) | Schedule builder | conditional. Bounded by caps and quiet hours |
| 4 | Channel | B | P | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 5 | Stop condition | B | C | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Policy revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Contract notice period | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |
| 9 | Consent scope | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 10 | Trigger | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 11 | Frequency cap | A | C | Schedule rule (RRULE) | Schedule builder | Bounded by caps and quiet hours |

*Replace rules (doc 06 "Remove / replace"):* Interval: conditional.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/renewals` | C | API-416 | exact |
| POST | `/api/v1/admin/renewal-policies` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_renewal` → ENT-150 `lcy_renewal` (C); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_message_template` → ENT-090 `eng_message_template` (P); `growth_subscription` → ENT-151 `lcy_customer_subscription` (P); `growth_account_metric` → ENT-152 `lcy_account_metric` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.18.11 A081: Lost deal and feedback

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 091 · New · Workspace |
| FR · wave · epic · profiles | FR-A081 (alias SM-FR-A081, trace M51, SM-UX-FR-A081) · W4 · EP-16 · CA-ALL, CA-ADMIN, CA-AI |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Classify loss and recommend process improvements |
| Key actions (Part 2.5) | Record loss, Recommend action |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Capture loss reason and corrections |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A029; A084; A087 |
| Tests | SM-UAT-S111; SM-UX-UAT-A081; unit families 001, 002, 015, 020, 021, 022, 023, 024, 046, 065, 066; **TC-ENH-C-202** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Deal | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Reason | B | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 4 | Feedback | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | redact sensitive data. Allowlisted, validated server-side |
| 5 | Owner | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Loss reason taxonomy | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 8 | Feedback permission | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 9 | Reopen eligibility | A | C | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 10 | Evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 11 | Learning action | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Feedback: redact sensitive data.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/deals/{id}/lost` | C | API-387 | exact |
| POST | `/api/v1/feedback` | C | API-418 | exact |
| GET | `/api/v1/feedback` | P | API-418 | path match, method differs |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_enrollment` → ENT-102 `eng_enrollment` (C); `growth_model_run` → ENT-046 `ai_model_run` (C); `growth_activity` → ENT-088 `crm_activity` (C); `growth_deal_outcome` → ENT-158 `lcy_outcome` (P); `growth_feedback` → ENT-157 `lcy_feedback` (P)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.18.12 A091: Insurance institutional pilot

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | existing 101 · New · Workspace |
| FR · wave · epic · profiles | FR-A091 (alias SM-FR-A091, trace M63, SM-UX-FR-A091) · W6 · EP-16 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal); vertical: FLT-09 MedMaarg |
| Automation (doc 06/17) | Route eligible institutional pilot and approvals |
| Key actions (Part 2.5) | Create, Update |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Manage organization-level pilot requirements |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A092; A032; A077 |
| Tests | SM-UAT-S121; SM-UX-UAT-A091; unit families 001, 002, 053, 054, 066; **TC-ENH-C-203** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Offering | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | capability gated. Must belong to the same tenant and startup (composite FK) |
| 3 | Pilot | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Delivery region | B | P | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 5 | Stage | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Pilot scope revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Institution type | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 9 | Eligibility | A | C | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 10 | Data restrictions | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Milestone evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |

*Replace rules (doc 06 "Remove / replace"):* Offering: capability gated.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/insurance/pilots` | N | — | no exact or equivalent operation |
| POST | `/api/v1/pilots` | C | API-419 | exact |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_partner` → ENT-153 `lcy_partner` (C); `growth_contract` → ENT-131 `com_contract` (C); `growth_pilot` → ENT-154 `lcy_pilot` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.18.13 A092: Insurance pilot approval

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 102 · Extension · Admin |
| FR · wave · epic · profiles | FR-A092 (alias SM-FR-A092, trace M63, SM-UX-FR-A092) · W6 · EP-16 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal); vertical: FLT-09 MedMaarg |
| Automation (doc 06/17) | Block unapproved pilot deployment |
| Key actions (Part 2.5) | Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Legal and commercial review |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A091; A072; A078 |
| Tests | SM-UAT-S122; SM-UX-UAT-A092; unit families 001, 002, 053, 054, 066; **TC-ENH-C-204** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Pilot | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Scope | B | P | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 4 | Reviewer | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 5 | Approval | B+R | C | Approval reference (gov_approval) | Approval chip with approver and SLA | controlled. Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Pilot revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Data agreement | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Risk review | A | C | Enumeration | Badge / select | Allowed values from configuration |
| 10 | Approval expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |

*Replace rules (doc 06 "Remove / replace"):* Approval: controlled.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/insurance/pilots` | N | — | no exact or equivalent operation |
| POST | `/api/v1/insurance/pilots/{id}/approve` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_partner` → ENT-153 `lcy_partner` (C); `growth_contract` → ENT-131 `com_contract` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_pilot` → ENT-154 `lcy_pilot` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.18.14 A093: Technology licensing enquiries

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 103 · New · Workspace |
| FR · wave · epic · profiles | FR-A093 (alias SM-FR-A093, trace M64, SM-UX-FR-A093) · W6 · EP-16 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Qualify licensing enquiry; route legal review |
| Key actions (Part 2.5) | Record, Route to legal |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Track integration requests and licensing opportunities |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A094; A032; A065 |
| Tests | SM-UAT-S123; SM-UX-UAT-A093; unit families 001, 002, 014, 015; **TC-ENH-C-205** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Technology | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 3 | Use case | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Scope | B+R | C | Text (≤ 4,000) | Text area with counter | configurable and restricted. No secrets or special-category data; length limit |
| 5 | Country | B | P | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Technology ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | License model | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 9 | Permitted use | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Region | A | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 11 | Requested API capabilities | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Scope: configurable and restricted.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/integration-enquiries` | P | API-420 | path match, method differs |
| POST | `/api/v1/integration-enquiries` | C | API-420 | exact |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_contract` → ENT-131 `com_contract` (C); `growth_integration_deal` → ENT-156 `lcy_integration_deal` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.18.15 A094: Licensing and API scope approval

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 104 · Extension · Admin |
| FR · wave · epic · profiles | FR-A094 (alias SM-FR-A094, trace M64, SM-UX-FR-A094) · W6 · EP-16 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Provision only approved entitlements |
| Key actions (Part 2.5) | Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve readiness and commercial terms |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A093; A071; A072 |
| Tests | SM-UAT-S124; SM-UX-UAT-A094; unit families 001, 002, 015, 033, 034, 035, 036, 043, 044; **TC-ENH-C-206** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | License | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | API scope | B+R | C | Text (≤ 4,000) | Text area with counter | approved capability list. No secrets or special-category data; length limit |
| 4 | Legal reviewer | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 5 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | License revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Entitlement set | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 9 | Security review | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Approved hash | A | C | char(64) SHA-256 | HashBadge (read-only) | Server-computed; never editable |

*Replace rules (doc 06 "Remove / replace"):* API scope: approved capability list.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/integration-enquiries` | P | API-420 | path match, method differs |
| POST | `/api/v1/integration-enquiries/{id}/approve` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_contract` → ENT-131 `com_contract` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_integration_deal` → ENT-156 `lcy_integration_deal` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.18.16 A095: Phygital expansion tracker

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-BOARD |
| Legacy screen ID · build class · location class (doc 06) | existing 105 · Extension · Workspace |
| FR · wave · epic · profiles | FR-A095 (alias SM-FR-A095, trace M65, SM-UX-FR-A095) · W6 · EP-16 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Trigger deployment tasks and exceptions |
| Key actions (Part 2.5) | Update progress |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Track partner territories and deployment milestones |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A096; A077; A078 |
| Tests | SM-UAT-S125; SM-UX-UAT-A095; unit families 001, 002, 053, 054, 066; **TC-ENH-C-207** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Location | B | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 2 | Partner | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Stage | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | controlled. Changed only by controlled transition; never free text |
| 5 | Owner | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Due date | B | P | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 7 | Location ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Delivery capacity | A | C | Integer limit (bounded) | Number input with unit | Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 9 | Partner grant | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 10 | Milestone evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 11 | Risk flag | A | C | Enumeration | Badge / select | Allowed values from configuration |

*Replace rules (doc 06 "Remove / replace"):* Stage: controlled.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/deployments` | C | API-421 | exact |
| PATCH | `/api/v1/deployments/{id}` | P | API-435 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_partner` → ENT-153 `lcy_partner` (C); `growth_pilot` → ENT-154 `lcy_pilot` (C); `growth_deployment` → ENT-155 `lcy_deployment` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.18.17 A096: Phygital readiness approval

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Follow-ups · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 106 · Extension · Admin |
| FR · wave · epic · profiles | FR-A096 (alias SM-FR-A096, trace M65, SM-UX-FR-A096) · W6 · EP-16 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-04 Engagement, FLT-05 Operations (task, deadline), FLT-07 Commercial (renewal) |
| Automation (doc 06/17) | Gate site activation on readiness |
| Key actions (Part 2.5) | Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review operational readiness |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A095; A078; A090 |
| Tests | SM-UAT-S126; SM-UX-UAT-A096; unit families 001, 002, 053, 054, 066; **TC-ENH-C-208** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Location | B | P | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 2 | Partner | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Checklist | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Reviewer | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 5 | Approval | B+R | C | Approval reference (gov_approval) | Approval chip with approver and SLA | controlled. Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Checklist revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Regional permissions | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Evidence digest | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 10 | Decision reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 11 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Approval: controlled.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/deployments` | C | API-421 | exact |
| POST | `/api/v1/deployments/{id}/approve` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_partner` → ENT-153 `lcy_partner` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_pilot` → ENT-154 `lcy_pilot` (C); `growth_deployment` → ENT-155 `lcy_deployment` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]


## 2.7.19 Admin: Objections view

### 2.7.19.1 A046: Chat FAQ and omnichannel routing

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Objections · LP-CONFIG + LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 050 · New · Admin |
| FR · wave · epic · profiles | FR-A046 (alias SM-FR-A046, trace M32; M41, SM-UX-FR-A046) · W3 · EP-10 · CA-ALL, CA-ADMIN, CA-AI, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-04 Engagement (objection, escalation), FLT-07 Commercial (quotation) |
| Automation (doc 06/17) | Route eligible conversations and abstain on unknowns |
| Key actions (Part 2.5) | Add FAQ, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Set answer policies, retention and channel priorities |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A037; A005; A084 |
| Tests | SM-UAT-S076; SM-UX-UAT-A046; unit families 001, 002, 015, 020, 021, 022, 023, 024, 046, 065, 066; **TC-ENH-C-209** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | FAQ | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Answer | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | approved revision only. Allowlisted, validated server-side |
| 5 | Escalation | B | P | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |
| 6 | Approval | B | P | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 7 | Intent taxonomy | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 8 | Knowledge revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 9 | Confidence gate | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 10 | Routing priority | A | C | Enumeration | Badge / select | Allowed values from configuration |
| 11 | Handover SLA | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |

*Replace rules (doc 06 "Remove / replace"):* Answer: approved revision only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/admin/chat/settings` | N | — | no exact or equivalent operation |
| GET | `/api/v1/inbox` | C | API-247 | exact |
| POST | `/api/v1/threads/{id}/assign` | C | API-248 | exact |
| POST | `/api/v1/admin/routing-rules` | P | API-283 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_message` → ENT-093 `eng_message` (C); `growth_thread` → ENT-092 `eng_thread` (C); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_prompt_version` → ENT-045 `ai_prompt_version` (C); `growth_activity` → ENT-088 `crm_activity` (C); `growth_identity_link` → ENT-097 `eng_identity_link` (C); `growth_routing_rule` → ENT-098 `eng_routing_rule` (C)

**Integrations (doc 06):** rag [ADP]

### 2.7.19.2 A069: Negotiation and objections

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Objections · LP-LIST + drawer |
| Legacy screen ID · build class · location class (doc 06) | existing 076 · New · Workspace |
| FR · wave · epic · profiles | FR-A069 (alias SM-FR-A069, trace M45, SM-UX-FR-A069) · W4 · EP-13 · CA-ALL, CA-ADMIN, CA-AI |
| Filters | FLT-01 Scope, FLT-04 Engagement (objection, escalation), FLT-07 Commercial (quotation) |
| Automation (doc 06/17) | Retrieve evidence; route concessions |
| Key actions (Part 2.5) | Record, Use approved answer, Escalate |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Track questions, responses and exceptions |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A070; A065; A037 |
| Tests | SM-UAT-S099; SM-UX-UAT-A069; unit families 001, 002, 028, 029, 030, 031, 032; **TC-ENH-C-210** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Concern | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 3 | Category | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Response | B+R | C | Text (≤ 4,000) | Text area with counter | draft until approved. No secrets or special-category data; length limit |
| 5 | Owner | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Relationship ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Objection evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 9 | Response revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 10 | Concession limit | A | C | Integer limit (bounded) | Number input with unit | Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 11 | Next action | A | C | Task reference + due timestamp | Inline task chip | Due date required; owner required |

*Replace rules (doc 06 "Remove / replace"):* Response: draft until approved.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/deals/{id}/objections` | P | API-331 | path match, method differs |
| POST | `/api/v1/deals/{id}/objections` | C | API-331 | exact |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_objection` → ENT-129 `com_objection` (C); `growth_negotiation` → ENT-130 `com_negotiation` (C)

**Integrations (doc 06):** llm gateway [ADP]; llm [ADP]

### 2.7.19.3 A070: Negotiation exception queue

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Objections · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 077 · Extension · Admin |
| FR · wave · epic · profiles | FR-A070 (alias SM-FR-A070, trace M45, SM-UX-FR-A070) · W4 · EP-13 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-04 Engagement (objection, escalation), FLT-07 Commercial (quotation) |
| Automation (doc 06/17) | Escalate nonroutine negotiation |
| Key actions (Part 2.5) | Approve, Reject, Counter-propose |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review nonstandard terms |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A069; A068; A072 |
| Tests | SM-UAT-S100; SM-UX-UAT-A070; unit families 001, 002, 015, 016, 017, 018, 019, 032, 033, 036, 047; **TC-ENH-C-211** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Exception | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Category | B | P | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Escalation | B | P | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |
| 5 | Reviewer | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B+R | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | controlled. Changed only by controlled transition; never free text |
| 7 | Risk class | A | C | Enumeration | Badge / select | Allowed values from configuration |
| 8 | Linked negotiation | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | SLA | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 10 | Decision evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 11 | Resolution condition | A | C | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |

*Replace rules (doc 06 "Remove / replace"):* Status: controlled.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/deals/{id}/objections` | P | API-331 | path match, method differs |
| POST | `/api/v1/negotiations/{id}/review` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_approval` → ENT-034 `gov_approval` (C); `growth_objection` → ENT-129 `com_objection` (C); `growth_negotiation` → ENT-130 `com_negotiation` (C)

**Integrations (doc 06):** llm gateway [ADP]; llm [ADP]


## 2.7.20 Admin: Closure view

### 2.7.20.1 A065: Proposal builder and preview

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Closure · LP-EDITOR |
| Legacy screen ID · build class · location class (doc 06) | existing 072 · New · Workspace |
| FR · wave · epic · profiles | FR-A065 (alias SM-FR-A065, trace M43, SM-UX-FR-A065) · W4 · EP-13 · CA-ALL, CA-ADMIN, CA-AI, CA-FIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-05 Operations (approval, deadline), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Generate draft; route scope and pricing approval |
| Key actions (Part 2.5) | Generate draft, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Generate, edit and version B2B proposals |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A066; A067; A071 |
| Tests | SM-UAT-S095; SM-UX-UAT-A065; unit families 001, 002, 014, 015; **TC-ENH-C-212** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Proposal | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Amount | B+R | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | computed from approved pricing. Decimal only; currency required; server recomputes (CA-FIN) |
| 5 | Currency | B | P | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 6 | Revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 7 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 8 | Proposal ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | Price version | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 10 | Validity | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |
| 11 | Scope version | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 12 | Terms revision | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 13 | Evidence links | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |

*Replace rules (doc 06 "Remove / replace"):* Amount: computed from approved pricing.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/deals/{id}/proposals` | P | API-328 | path match, method differs |
| POST | `/api/v1/deals/{id}/proposals` | C | API-328 | exact |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_proposal` → ENT-125 `com_proposal` (C); `growth_product` → ENT-016 `cat_offering` (P); `growth_proposal_version` → ENT-126 `com_proposal_version` (C)

**Integrations (doc 06):** pandadoc [ADP]; Sales [DEV]; PandaDoc [ADP]

### 2.7.20.2 A066: Proposal approval queue

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Closure · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 073 · Extension · Admin |
| FR · wave · epic · profiles | FR-A066 (alias SM-FR-A066, trace M25; M43, SM-UX-FR-A066) · W4 · EP-13 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-05 Operations (approval, deadline), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Approve exact revision; block stale proposals |
| Key actions (Part 2.5) | Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve medical claims and commercial terms |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A065; A068; A071 |
| Tests | SM-UAT-S096; SM-UX-UAT-A066; unit families 001, 002, 015, 016, 017, 018, 019, 032, 033, 036, 047; **TC-ENH-C-213** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Proposal | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Amount | B+R | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | read-only. Decimal only; currency required; server recomputes (CA-FIN) |
| 4 | Revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 5 | Reviewer | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Proposal hash | A | C | char(64) SHA-256 | HashBadge (read-only) | Server-computed; never editable |
| 8 | Risk class | A | C | Enumeration | Badge / select | Allowed values from configuration |
| 9 | Decision reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 10 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Reviewer scope | A | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |

*Replace rules (doc 06 "Remove / replace"):* Amount: read-only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/approvals` | P | API-542 | resource-equivalent DERIVED path on same screen |
| GET | `/api/v1/deals/{id}/proposals` | P | API-328 | path match, method differs |
| POST | `/api/v1/proposals/{id}/review` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_proposal` → ENT-125 `com_proposal` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_message_draft` → ENT-091 `eng_message_draft` (C); `growth_proposal_version` → ENT-126 `com_proposal_version` (C)

**Integrations (doc 06):** pandadoc [ADP]; Sales [DEV]; PandaDoc [ADP]

### 2.7.20.3 A067: Quotation builder

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Closure · LP-EDITOR |
| Legacy screen ID · build class · location class (doc 06) | existing 074 · New · Workspace |
| FR · wave · epic · profiles | FR-A067 (alias SM-FR-A067, trace M44, SM-UX-FR-A067) · W4 · EP-13 · CA-ALL, CA-ADMIN, CA-FIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-05 Operations (approval, deadline), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Calculate exact decimal totals; route exceptions |
| Key actions (Part 2.5) | Add line, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Create approved quotes and validity periods |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A068; A065; A073 |
| Tests | SM-UAT-S097; SM-UX-UAT-A067; unit families 001, 002, 056, 057, 058, 059, 066; **TC-ENH-C-214** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Quotation | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Offering | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Quantity | B | C | Decimal quantity | QuantityInput (value + unit) | Non-negative; validated range; unit mandatory |
| 4 | Unit price | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 5 | Discount | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 6 | Tax | B | C | TaxProfile / tax line reference | Read-only computed line | Per DEC-027; server-computed |
| 7 | Currency | B | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 8 | SKU/service line | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Price list revision | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 10 | Tax jurisdiction | A | C | TaxProfile / tax line reference | Read-only computed line | Per DEC-027; server-computed |
| 11 | Rounding rule | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 12 | Total | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 13 | Validity | A | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |

*Replace rules (doc 06 "Remove / replace"):* Unit price and Discount: bounded by approved policy.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/quotes` | P | API-329 | path match, method differs |
| POST | `/api/v1/quotes` | C | API-329 | exact |

**Tables → blueprint entities:** `growth_quote` → ENT-127 `com_quote` (C); `growth_quote_line` → ENT-128 `com_quote_line` (C); `growth_price_version` → ENT-021 `cat_price_version` (P); `growth_proposal_version` → ENT-126 `com_proposal_version` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.20.4 A068: Price and discount approval

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Closure · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 075 · Extension · Admin |
| FR · wave · epic · profiles | FR-A068 (alias SM-FR-A068, trace M44, SM-UX-FR-A068) · W4 · EP-13 · CA-ALL, CA-ADMIN, CA-APPROVE, CA-FIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-05 Operations (approval, deadline), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Hold excessive discount; approve exact quote version |
| Key actions (Part 2.5) | Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Set commercial approval limits |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A067; A070; A066 |
| Tests | SM-UAT-S098; SM-UX-UAT-A068; unit families 001, 002, 056, 057, 058, 059, 066; **TC-ENH-C-215** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Quote | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Discount | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 4 | Amount | B+R | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | computed read-only. Decimal only; currency required; server recomputes (CA-FIN) |
| 5 | Reviewer | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Discount rule | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 8 | Margin floor | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 9 | Approved quote hash | A | C | char(64) SHA-256 | HashBadge (read-only) | Server-computed; never editable |
| 10 | Decision reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 11 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Amount: computed read-only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/quotes` | P | API-329 | path match, method differs |
| POST | `/api/v1/quotes/{id}/approve` | C | API-330 | exact |

**Tables → blueprint entities:** `growth_quote` → ENT-127 `com_quote` (C); `growth_quote_line` → ENT-128 `com_quote_line` (C); `growth_approval` → ENT-034 `gov_approval` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.20.5 A071: Contracts and MoUs

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Closure · LP-LIST + LP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | existing 078 · New · Workspace |
| FR · wave · epic · profiles | FR-A071 (alias SM-FR-A071, trace M46, SM-UX-FR-A071) · W4 · EP-13 · CA-ALL, CA-ADMIN, CA-DISPATCH |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-05 Operations (approval, deadline), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Route agreement review and authorized signing |
| Key actions (Part 2.5) | Generate draft, Send for signature (after legal approval), Record signed upload |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Track agreement versions and signing status |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A072; A073; A075 |
| Tests | SM-UAT-S101; SM-UX-UAT-A071; unit families 001, 002, 007, 015, 033, 040, 041, 046; **TC-ENH-C-216** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Agreement | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Type | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 5 | Signature | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | verified provider state. Allowlisted, validated server-side |
| 6 | Approval | B | P | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 7 | Signer authority | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Agreement hash | A | C | char(64) SHA-256 | HashBadge (read-only) | Server-computed; never editable |
| 9 | Effective date | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 10 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Signature evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |

*Replace rules (doc 06 "Remove / replace"):* Signature: verified provider state.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/contracts` | P | API-332 | path match, method differs |
| POST | `/api/v1/contracts` | C | API-332 | exact |
| POST | `/api/v1/webhooks/esign` | C | API-333 | exact |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_quote` → ENT-127 `com_quote` (C); `growth_contract` → ENT-131 `com_contract` (C); `growth_signature_event` → ENT-132 `com_signature_event` (C); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C)

**Integrations (doc 06):** PandaDoc [ADP]

### 2.7.20.6 A072: Contract and legal approvals

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Closure · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 080 · New · Admin |
| FR · wave · epic · profiles | FR-A072 (alias SM-FR-A072, trace M46, SM-UX-FR-A072) · W4 · EP-13 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-05 Operations (approval, deadline), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Enforce legal approval before execution |
| Key actions (Part 2.5) | Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review contract and authorized signers |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A071; A070; A073 |
| Tests | SM-UAT-S102; SM-UX-UAT-A072; unit families 001, 002, 007, 015, 046; **TC-ENH-C-217** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Agreement | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Revision | B | P | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 4 | Legal reviewer | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 5 | Approval | B+R | C | Approval reference (gov_approval) | Approval chip with approver and SLA | immutable revision. Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Legal jurisdiction | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Required checks | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Approved hash | A | C | char(64) SHA-256 | HashBadge (read-only) | Server-computed; never editable |
| 10 | Decision expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |

*Replace rules (doc 06 "Remove / replace"):* Approval: immutable revision.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/contracts` | P | API-332 | path match, method differs |
| POST | `/api/v1/contracts/{id}/approve` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_contract` → ENT-131 `com_contract` (C); `growth_signature_event` → ENT-132 `com_signature_event` (C); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C); `growth_approval` → ENT-034 `gov_approval` (C)

**Integrations (doc 06):** PandaDoc [ADP]

### 2.7.20.7 A073: Payment and deal closure

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Closure · LP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | existing 081 · New · Workspace |
| FR · wave · epic · profiles | FR-A073 (alias SM-FR-A073, trace M47, SM-UX-FR-A073) · W4 · EP-15 · CA-ALL, CA-ADMIN, CA-FIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-05 Operations (approval, deadline), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Reconcile receipt; close only eligible deal |
| Key actions (Part 2.5) | Create invoice draft, Verify (maker), Close (if gate passes) |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Record verified payment and won/lost status |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A074; A075; A082 |
| Tests | SM-UAT-S103; SM-UX-UAT-A073; unit families 001, 002, 007, 015, 033, 040, 041, 046; **TC-ENH-C-218** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Payment | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Deal | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Currency | B | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 5 | Amount | B+R | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | verified not editable. Decimal only; currency required; server recomputes (CA-FIN) |
| 6 | Verification | B | P | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 7 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 8 | Invoice reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | External payment ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 10 | Currency match | A | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 11 | Verified receipt | A | C | Verification state + evidence reference | StateBadge with evidence link | Set only by the verification workflow; expiry enforced |
| 12 | Closure gate | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Amount: verified not editable.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/deals/{id}/payments` | P | API-393 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/deals/{id}/invoices` | P | API-390;API-392 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/webhooks/payment` | C | API-385 | exact |
| POST | `/api/v1/deals/{id}/close` | C | API-386 | exact |
| POST | `/api/v1/invoices/{id}/payment-link` | P | API-398 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_contract` → ENT-131 `com_contract` (C); `growth_signature_event` → ENT-132 `com_signature_event` (C); `growth_invoice` → ENT-140 `com_invoice` (C); `growth_payment` → ENT-142 `com_payment` (C); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C); `growth_activity` → ENT-088 `crm_activity` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.20.8 A074: Payment reconciliation

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Closure · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 083 · New · Admin |
| FR · wave · epic · profiles | FR-A074 (alias SM-FR-A074, trace M47, SM-UX-FR-A074) · W4 · EP-15 · CA-ALL, CA-ADMIN, CA-FIN |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-05 Operations (approval, deadline), FLT-02 Geography (currency) |
| Automation (doc 06/17) | Prevent double allocation; escalate mismatch |
| Key actions (Part 2.5) | Match, Verify (checker), Raise discrepancy |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Verify payment evidence and exceptions |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A073; A083; A105 |
| Tests | SM-UAT-S104; SM-UX-UAT-A074; unit families 001, 002, 007, 015, 033, 040, 041, 046; **TC-ENH-C-219** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Payment | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Invoice | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Currency | B | P | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 4 | Amount | B | P | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 5 | Match | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | computed. Allowlisted, validated server-side |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Receipt ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Idempotency key | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Allocation balance | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | FX evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 11 | Discrepancy reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |

*Replace rules (doc 06 "Remove / replace"):* Match: computed.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/deals/{id}/payments` | P | API-393 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/webhooks/payment` | C | API-385 | exact |
| POST | `/api/v1/deals/{id}/close` | C | API-386 | exact |
| POST | `/api/v1/payments/{id}/reconcile` | P | API-154;API-254;API-304 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_contract` → ENT-131 `com_contract` (C); `growth_signature_event` → ENT-132 `com_signature_event` (C); `growth_invoice` → ENT-140 `com_invoice` (C); `growth_payment` → ENT-142 `com_payment` (C); `growth_inbound_event` → ENT-095 `eng_inbound_event` (C); `growth_activity` → ENT-088 `crm_activity` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.20.9 A104: Global project bid and tender desk

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Closure · LP-LIST + LP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | existing 114 · Contextual panel · Workspace |
| FR · wave · epic · profiles | FR-A104 (alias SM-FR-A104, trace B-TENANT, SM-UX-FR-A104) · W4 · EP-14 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-05 Operations (approval, deadline), FLT-02 Geography (currency); vertical: FLT-08 AppNAI |
| Automation (doc 06/17) | Route owned AI projects to AppNAI; allow eligible external clients |
| Key actions (Part 2.5) | Create, Decide bid/no-bid, Record submission, Record award |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | AppNAI global AI projects: deadline, eligibility, requirements, bid/no-bid, proposal, authorized submission and award. |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A022; A065; A072; A029 |
| Tests | SM-UAT-S134; SM-UX-UAT-A104; unit families 001, 002, 048, 051, 052, 058, 066; **TC-ENH-C-220** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Tender | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Technology | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 4 | Deadline | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 5 | Delivery model | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 6 | Budget | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 7 | Eligibility | B+R | C | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | computed. Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 8 | Stage | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 9 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 10 | Tender ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 11 | Capability grant | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 12 | Deadline timezone | A | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 13 | Eligibility evidence | A | C | Computed eligibility decision (gov_eligibility_decision) | EligibilityBadge per channel (read-only, rule tooltip) | Computed by the PDP; never editable; shows blocking rule ID (UX-04) |
| 14 | Bid revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 15 | Submission gate | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Eligibility: computed; Startup position-based restrictions removed.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sales/bids` | P | API-362;API-364 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sales/bids` | P | API-363;API-366;API-367;API-368 | resource-equivalent DERIVED path on same screen |
| PATCH | `/api/v1/sales/bids/{id}` | P | API-365 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sales/bids/{id}/control` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_proposal` → ENT-125 `com_proposal` (C); `growth_task` → ENT-148 `lcy_task` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_evidence` → ENT-059 `intel_evidence` (C); `growth_opportunity` → ENT-072 `intel_opportunity` (C); `sales_bid` → ENT-133 `com_bid` (P)

**Integrations (doc 06):** Internal React/Django [INT]

### 2.7.20.10 A105: Purchase, sales order and fulfillment desk

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Closure · LP-LIST + LP-DETAIL |
| Legacy screen ID · build class · location class (doc 06) | existing 115 · Contextual panel · Workspace |
| FR · wave · epic · profiles | FR-A105 (alias SM-FR-A105, trace B-TENANT, SM-UX-FR-A105) · W4 · EP-14 · CA-ALL, CA-ADMIN, CA-FIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-07 Commercial, FLT-05 Operations (approval, deadline), FLT-02 Geography (currency); vertical: FLT-11 OrganicSpec |
| Automation (doc 06/17) | Validate stock/order and update shared fulfillment state |
| Key actions (Part 2.5) | Create, Approve, Issue, Record fulfilment, Cancel |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Buy/sell/service/training/project direction; multiple lines; actual delivery/receipt; payable/receivable and reconciliation. |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A067; A073; A074; A075 |
| Tests | SM-UAT-S135; SM-UX-UAT-A105; unit families 001, 002, 056, 057, 058, 059, 066; **TC-ENH-C-221** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Order | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Organization | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Direction | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | permitted capability. Allowlisted, validated server-side |
| 4 | SKU | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Quantity | B | C | Decimal quantity | QuantityInput (value + unit) | Non-negative; validated range; unit mandatory |
| 6 | Unit | B | C | Unit of measure (ref_unit) | Select | Allowed units per SKU |
| 7 | Amount | B+R | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | calculated. Decimal only; currency required; server recomputes (CA-FIN) |
| 8 | Fulfillment | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 10 | Order ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 11 | Capability grant | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 12 | Price revision | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 13 | Inventory/reservation | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 14 | Tax currency | A | C | TaxProfile / tax line reference | Read-only computed line | Per DEC-027; server-computed |
| 15 | Fulfillment event | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 16 | Invoice ref | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |

*Replace rules (doc 06 "Remove / replace"):* Direction: permitted capability; Amount: calculated; fixed startup restriction removed.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sales/orders` | P | API-370;API-372 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sales/orders` | P | API-371;API-374;API-375;API-376 | resource-equivalent DERIVED path on same screen |
| PATCH | `/api/v1/sales/orders/{id}` | P | API-373 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sales/orders/{id}/control` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/orders/{id}/milestones` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/milestones/{id}/accept` | P | API-151;API-356 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_deal` → ENT-086 `crm_deal` (C); `growth_quote` → ENT-127 `com_quote` (C); `sales_fulfillment` → ENT-137 `com_fulfillment_event` (P); `sales_order` → ENT-135 `com_order` (P); `sales_order_line` → ENT-136 `com_order_line` (P); `growth_invoice` → ENT-140 `com_invoice` (C); `growth_payment` → ENT-142 `com_payment` (C); `growth_approval` → ENT-034 `gov_approval` (C)

**Integrations (doc 06):** Internal React/Django [INT]


## 2.7.21 Admin: Automation view (workflow, governance, administration, operations)

### 2.7.21.1 A002: User and role administration

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-LIST + drawer |
| Legacy screen ID · build class · location class (doc 06) | existing 002 · Reuse · Existing |
| FR · wave · epic · profiles | FR-A002 (alias SM-FR-A002, trace M01, SM-UX-FR-A002) · W0 · EP-01 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Invite and revoke; invalidate permissions |
| Key actions (Part 2.5) | Invite, Change grants, Revoke |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Reuse existing user management; verify new business roles |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A099; A003 |
| Tests | SM-UAT-S032; SM-UX-UAT-A002; unit families 001, 002, 003, 004, 005, 006, 007, 008, 009, 013, 045; **TC-ENH-C-222** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | User | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 2 | Role | B | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 3 | Team | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 4 | Startup | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Status | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 6 | Tenant | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 7 | Membership expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 8 | Grant scope | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 9 | Invite status | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 10 | Role revision | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 11 | MFA requirement | A | C | Identity attribute held by the reused IdP | IdP-hosted control | Never persisted or displayed by this product (DEC-019) |

*Replace rules (doc 06 "Remove / replace"):* Access: replace broad flag with scoped grants.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/me` | C | API-002 | exact |
| GET | `/admin/users` | P | API-019 | resource-equivalent DERIVED path on same screen |
| POST | `/admin/users/{id}/roles` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `existing membership table` → ENT-008 `ten_membership` (P); `existing role table` → ENT-007 `ten_role` (P); `existing user table` → ENT-006 `ten_user` (P)

**Integrations (doc 06):** django auth [OSS]; django [OSS]; drf [OSS]

### 2.7.21.2 A004: Product and capability editor

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-EDITOR |
| Legacy screen ID · build class · location class (doc 06) | existing 004 · New · Admin |
| FR · wave · epic · profiles | FR-A004 (alias SM-FR-A004, trace M02, SM-UX-FR-A004) · W0 · EP-02 · CA-ALL, CA-ADMIN, CA-CONFIG, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Generate approved offering config and publish options |
| Key actions (Part 2.5) | Save, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure offerings, price, availability and approved claims |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A005; A006; A107 |
| Tests | SM-UAT-S034; SM-UX-UAT-A004; unit families 001, 002, 014, 015; **TC-ENH-C-223** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Startup | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Business line | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Category | B+R | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | dynamic taxonomy. Values from the active reference dataset (CFG-32); unknown values rejected |
| 5 | Delivery model | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 6 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 7 | Region | B | C | ISO 3166 code or reference location | Searchable select | Allowlist; jurisdiction rule pack applies (DEC-029) |
| 8 | Capability codes | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | SKU/service ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 10 | Price revision | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Tax profile | A | C | TaxProfile / tax line reference | Read-only computed line | Per DEC-027; server-computed |
| 12 | Lifecycle state | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |

*Replace rules (doc 06 "Remove / replace"):* Category: dynamic taxonomy.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/products` | C | API-048 | exact |
| GET | `/api/v1/products/{id}` | P | API-048 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/admin/products` | N | — | no exact or equivalent operation |
| PATCH | `/api/v1/admin/products/{id}` | N | — | no exact or equivalent operation |
| POST | `/api/v1/admin/claims/approve` | C | API-049 | exact |
| POST | `/api/v1/admin/products/{id}/prices` | P | API-057 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_product` → ENT-016 `cat_offering` (P); `growth_capability` → ENT-018 `cat_capability` (P); `growth_claim` → ENT-020 `cat_claim` (P); `growth_price_version` → ENT-021 `cat_price_version` (P); `growth_approval` → ENT-034 `gov_approval` (C)

**Integrations (doc 06):** claude api [ADP]; pgvector [OSS]; PubMed [ADP]

### 2.7.21.3 A005: Product knowledge catalog

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 005 · New · Workspace |
| FR · wave · epic · profiles | FR-A005 (alias SM-FR-A005, trace M02; M03, SM-UX-FR-A005) · W0 · EP-02 · CA-ALL, CA-ADMIN, CA-AI |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Refresh authorized knowledge only |
| Key actions (Part 2.5) | Search approved knowledge |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | View approved products and capabilities |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A004; A006; A021 |
| Tests | SM-UAT-S035; SM-UX-UAT-A005; unit families 001, 002, 028, 029, 030, 031, 032; **TC-ENH-C-224** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Category | B | P | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 3 | Revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 4 | Source | B | P | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 5 | Approval | B | P | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | computed. Changed only by controlled transition; never free text |
| 7 | Knowledge ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Claim references | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 9 | Scope | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 10 | Freshness SLA | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 11 | Embedding revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |

*Replace rules (doc 06 "Remove / replace"):* Status: computed.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/products` | C | API-048 | exact |
| GET | `/api/v1/products/{id}` | P | API-048 | resource-equivalent DERIVED path on same screen |
| GET | `/api/v1/knowledge/search` | C | API-052 | exact |

**Tables → blueprint entities:** `growth_document` → ENT-024 `cat_document` (P); `growth_product` → ENT-016 `cat_offering` (P); `growth_capability` → ENT-018 `cat_capability` (P); `growth_claim` → ENT-020 `cat_claim` (P); `growth_price_version` → ENT-021 `cat_price_version` (P); `growth_document_chunk` → ENT-025 `cat_chunk` (P); `growth_embedding` → ENT-026 `cat_embedding` (P)

**Integrations (doc 06):** claude api [ADP]; pgvector [OSS]; PubMed [ADP]

### 2.7.21.4 A006: Knowledge documents and approval

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-LIST + LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 006 · New · Admin |
| FR · wave · epic · profiles | FR-A006 (alias SM-FR-A006, trace M03, SM-UX-FR-A006) · W0 · EP-02 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Scan, classify, route approval and refresh index |
| Key actions (Part 2.5) | Upload, Approve, Reject |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Upload, version, approve and search source documents |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A005; A051; A084 |
| Tests | SM-UAT-S036; SM-UX-UAT-A006; unit families 001, 002, 004, 028, 029, 030, 031, 032, 038, 039; **TC-ENH-C-225** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Document | B | C | File reference (object storage key + scan state) | FileUpload with scan status | Scanned before use (NFR-021); size/type allowlist |
| 2 | Offering | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 4 | Source | B+R | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | validated provenance. Must resolve to permitted, unexpired evidence |
| 5 | Reviewer | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | File scan | A | C | File reference (object storage key + scan state) | FileUpload with scan status | Scanned before use (NFR-021); size/type allowlist |
| 8 | Classification | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Content hash | A | C | char(64) SHA-256 | HashBadge (read-only) | Server-computed; never editable |
| 10 | Access grant | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 11 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 12 | Approval evidence | A | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |

*Replace rules (doc 06 "Remove / replace"):* Source: validated provenance.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/knowledge/uploads` | C | API-051 | exact |
| GET | `/api/v1/knowledge/documents` | P | API-061;API-062 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/knowledge/documents/{id}/review` | N | — | no exact or equivalent operation |
| GET | `/api/v1/knowledge/search` | C | API-052 | exact |

**Tables → blueprint entities:** `growth_document` → ENT-024 `cat_document` (P); `growth_approval` → ENT-034 `gov_approval` (C); `growth_document_chunk` → ENT-025 `cat_chunk` (P); `growth_embedding` → ENT-026 `cat_embedding` (P); `growth_job_run` → ENT-173 `ops_job_run` (C)

**Integrations (doc 06):** document skills dev [DEV]; document skills [DEV]; s3 [ADP]

### 2.7.21.5 A007: Consent and communication policies

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 007 · New · Admin |
| FR · wave · epic · profiles | FR-A007 (alias SM-FR-A007, trace M04, SM-UX-FR-A007) · W0 · EP-03 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Enforce unified suppression and cross-workflow caps |
| Key actions (Part 2.5) | Submit, Search suppression |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure eligible channels, suppression and opt-out rules |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A039; A047; A010 |
| Tests | SM-UAT-S037; SM-UX-UAT-A007; unit families 001, 002, 004, 010, 011, 012, 013, 023, 030, 042; **TC-ENH-C-226** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Policy | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Jurisdiction | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Consent | B+R | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | scoped records. Purpose and policy revision recorded; withdrawal immediate |
| 5 | Frequency | B+R | C | Schedule rule (RRULE) | Schedule builder | explicit period. Bounded by caps and quiet hours |
| 6 | Stop condition | B | P | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |
| 7 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 8 | Consent scope | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 9 | Quiet hours | A | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 10 | Channel permission | A | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | Purpose and policy revision recorded; withdrawal immediate |
| 11 | Suppression ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 12 | Policy revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 13 | Frequency cap | A | C | Schedule rule (RRULE) | Schedule builder | Bounded by caps and quiet hours |

*Replace rules (doc 06 "Remove / replace"):* Consent: scoped records; Frequency: explicit period.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/consents` | C | API-066 | exact |
| GET | `/api/v1/admin/policies` | P | API-071 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/admin/policies` | P | API-072;API-073 | resource-equivalent DERIVED path on same screen |
| GET | `/api/v1/admin/suppressions` | P | API-074 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_consent` → ENT-027 `gov_consent` (C); `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_suppression` → ENT-028 `gov_suppression` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.21.6 A008: Integration connections

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-LIST + LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 009 · New · Admin |
| FR · wave · epic · profiles | FR-A008 (alias SM-FR-A008, trace M05, SM-UX-FR-A008) · W0 · EP-01 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Validate entitlement and suspend failing connection |
| Key actions (Part 2.5) | Connect, Test, Disable |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Connect provider accounts, permissions and limits |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A012; A014; A036 |
| Tests | SM-UAT-S038; SM-UX-UAT-A008; unit families 001, 002, 015, 033, 034, 035, 036, 043, 044; **TC-ENH-C-227** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Provider | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | never display tokens. Must belong to the same tenant and startup (composite FK) |
| 2 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Scope | B | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 4 | Quota | B | C | Integer limit (bounded) | Number input with unit | Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 5 | Health | B | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Connection scope | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 8 | Credential reference | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | Capability grant | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 10 | Auth expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Webhook health | A | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 12 | Fallback | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Provider: never display tokens.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/integrations` | C | API-095 | exact |
| POST | `/api/v1/admin/integrations` | P | API-096;API-097;API-099 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/admin/integrations/test` | C | API-096 | exact |
| POST | `/api/v1/admin/integrations/{id}/disable` | P | API-099 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_job_run` → ENT-173 `ops_job_run` (C); `growth_integration` → ENT-040 `int_integration` (C); `growth_credential_ref` → ENT-041 `int_credential_ref` (C); `growth_quota` → ENT-042 `int_quota` (P)

**Integrations (doc 06):** aws secrets manager [ADP]; aws [ADP]; MCP Server Dev [DEV]

### 2.7.21.7 A009: Audit and job activity

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-MONITOR |
| Legacy screen ID · build class · location class (doc 06) | existing 010 · New · Admin |
| FR · wave · epic · profiles | FR-A009 (alias SM-FR-A009, trace M06, SM-UX-FR-A009) · W0 · EP-01 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Correlate events; surface anomalies |
| Key actions (Part 2.5) | Filter, Export, Retry job |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | View events, failed jobs and controlled replay |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A014; A106; A090 |
| Tests | SM-UAT-S039; SM-UX-UAT-A009; unit families 001, 002, 014, 015, 016, 017, 018, 019, 024, 032, 033, 036, 047; **TC-ENH-C-228** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Event | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Actor | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 3 | Action | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Timestamp | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 5 | Outcome | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | immutable event result. Changed only by controlled transition; never free text |
| 6 | Status | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Correlation ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Run ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | Tenant/startup | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 10 | Policy revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 11 | Evidence digest | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |

*Replace rules (doc 06 "Remove / replace"):* Outcome: immutable event result.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/events` | C | API-115 | exact |
| GET | `/api/v1/admin/jobs` | P | API-124;API-125 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/admin/jobs/{id}/retry` | C | API-116 | exact |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_outbox` → ENT-169 `ops_outbox` (C); `growth_job_run` → ENT-173 `ops_job_run` (C)

**Integrations (doc 06):** celery [OSS]; redis [OSS]

### 2.7.21.8 A010: Source permissions and registry

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-LIST + LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 011 · New · Admin |
| FR · wave · epic · profiles | FR-A010 (alias SM-FR-A010, trace M07, SM-UX-FR-A010) · W0 · EP-05 · CA-ALL, CA-ADMIN, CA-APPROVE, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Block expired or unauthorized research source |
| Key actions (Part 2.5) | Register, Approve, Expire |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Approve sources, access methods and expiry |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A015; A049; A086 |
| Tests | SM-UAT-S040; SM-UX-UAT-A010; unit families 001, 002, 024, 025, 026, 027, 028, 045; **TC-ENH-C-229** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Source | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 2 | Access method | B | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 3 | Permission | B+R | C | Consent / permission record reference | ConsentNotice or toggle with policy revision | explicit capability not free text. Purpose and policy revision recorded; withdrawal immediate |
| 4 | Expiry | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 5 | Category | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 6 | Status | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Usage licence | A | C | Integer (computed) | Number (read-only) | Distinct records; Unknown ≠ 0 |
| 8 | Permitted purpose | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Refresh schedule | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 10 | Access scope | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 11 | Review owner | A | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |

*Replace rules (doc 06 "Remove / replace"):* Permission: explicit capability not free text.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sources` | C | API-158 | exact |
| POST | `/api/v1/admin/sources` | C | API-159 | exact |
| PATCH | `/api/v1/admin/sources/{id}` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_policy_version` → ENT-029 `gov_policy_version` (C); `growth_source` → ENT-053 `intel_source` (C); `growth_source_policy` → ENT-054 `intel_source_policy` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.21.9 A011: AI configuration and evaluation

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-CONFIG + LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | existing 012 · New · Admin |
| FR · wave · epic · profiles | FR-A011 (alias SM-FR-A011, trace M08, SM-UX-FR-A011) · W0 · EP-04 · CA-ALL, CA-ADMIN, CA-AI, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Route lower-cost model only if quality gates pass |
| Key actions (Part 2.5) | Edit, Run eval, Submit |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure prompts, model limits and validation |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A084; A012; A102 |
| Tests | SM-UAT-S041; SM-UX-UAT-A011; unit families 001, 002, 015, 028, 029, 030, 031, 032, 033, 040, 041; **TC-ENH-C-230** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Model | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 2 | Task type | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Token budget | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 4 | Quality threshold | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | task specific. Allowlisted, validated server-side |
| 5 | Fallback | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Model revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Task route | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Evaluation sample size | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Cost ceiling | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Guardrail result | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 12 | Rollback | A | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |

*Replace rules (doc 06 "Remove / replace"):* Quality threshold: task specific.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/ai/runs` | C | API-135 | exact |
| POST | `/api/v1/admin/ai/prompts` | P | API-142 | resource-equivalent DERIVED path on same screen |
| GET | `/api/v1/admin/ai/eval-cases` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_embedding` → ENT-026 `cat_embedding` (P); `growth_prompt_version` → ENT-045 `ai_prompt_version` (C); `growth_model_run` → ENT-046 `ai_model_run` (C); `growth_eval_case` → ENT-047 `ai_eval_case` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_budget` → ENT-052 `ai_budget` (C); `growth_cost_ledger` → ENT-051 `ai_cost_ledger` (C)

**Integrations (doc 06):** claude/openai api [ADP]; deepeval [OSS]; Agent SDK Dev [DEV]; Pydantic AI [OSS]

### 2.7.21.10 A012: API cost and budget dashboard

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-DASH + LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 013 · New · Admin |
| FR · wave · epic · profiles | FR-A012 (alias SM-FR-A012, trace M53, SM-UX-FR-A012) · W0 · EP-04 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Enforce budgets before provider execution |
| Key actions (Part 2.5) | Set caps, Emergency pause |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Track usage, budgets and emergency stop |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A008; A061; A101 |
| Tests | SM-UAT-S042; SM-UX-UAT-A012; unit families 001, 002, 003, 008, 009, 013, 015, 033, 034, 035, 036, 043, 044, 045; **TC-ENH-C-231** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Provider | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Usage | B | C | Integer (computed) | Number (read-only) | Distinct records; Unknown ≠ 0 |
| 3 | Cost | B+R | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | separate actual/reserved. Decimal only; currency required; server recomputes (CA-FIN) |
| 4 | Budget | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 5 | Quota | B | P | Integer limit (bounded) | Number input with unit | Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Reserved spend | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 8 | Actual spend | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 9 | Objective cost | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 10 | Budget remaining | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Forecast | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 12 | Hard stop | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Cost: separate actual/reserved.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/costs` | C | API-136 | exact |
| POST | `/api/v1/admin/budgets` | C | API-137 | exact |
| POST | `/api/v1/admin/budgets/{id}/pause` | P | API-144 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_budget` → ENT-052 `ai_budget` (C); `growth_cost_ledger` → ENT-051 `ai_cost_ledger` (C)

**Integrations (doc 06):** cloudwatch [ADP]

### 2.7.21.11 A013: Privacy request queue

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 014 · New · Admin |
| FR · wave · epic · profiles | FR-A013 (alias SM-FR-A013, trace M56, SM-UX-FR-A013) · W0 · EP-03 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Route requests and suppression; prevent unauthorized deletion |
| Key actions (Part 2.5) | Verify, Fulfil, Restrict |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review deletion and correction requests |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A007; A103; A047 |
| Tests | SM-UAT-S043; SM-UX-UAT-A013; unit families 001, 002, 004, 023, 042, 065, 066; **TC-ENH-C-232** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Request | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Request type | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 3 | Received | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 4 | Deadline | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 5 | Owner | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B+R | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | controlled transition. Changed only by controlled transition; never free text |
| 7 | Subject scope | A | C | Text (≤ 200) | Text input | Trimmed; required where marked |
| 8 | Proof | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Legal hold | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 10 | Data categories | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Fulfillment evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |

*Replace rules (doc 06 "Remove / replace"):* Status: controlled transition.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/privacy/requests` | C | API-069 | exact |
| GET | `/api/v1/admin/privacy/requests` | P | API-084 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/admin/privacy/requests/{id}/resolve` | N | — | no exact or equivalent operation |
| POST | `/api/v1/admin/retention-policies` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_privacy_request` → ENT-036 `gov_privacy_request` (C); `growth_retention_policy` → ENT-037 `gov_retention_policy` (C)

**Integrations (doc 06):** Internal / no direct plugin [INT]

### 2.7.21.12 A014: System health and incidents

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | existing 015 · New growth-specific view · Admin |
| FR · wave · epic · profiles | FR-A014 (alias SM-FR-A014, trace M06; M58, SM-UX-FR-A014) · W0 · EP-21 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Detect incident; pause impacted workflows |
| Key actions (Part 2.5) | Acknowledge, Resolve |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Monitor deployment, errors and service outages |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A009; A090; A106 |
| Tests | SM-UAT-S044; SM-UX-UAT-A014; unit families 001, 002, 015, 016, 017, 018, 019, 028, 029, 030, 031, 032, 033, 036, 047; **TC-ENH-C-233** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Service | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Latency | B | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |
| 3 | Availability | B | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |
| 4 | Incident | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Severity | B | C | Enumeration | Badge / select | Allowed values from configuration |
| 6 | Status | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | monitored read-only. Changed only by controlled transition; never free text |
| 7 | Service scope | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 8 | Error rate | A | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 9 | Queue depth | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | SLO | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Run correlation | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 12 | Recovery state | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |

*Replace rules (doc 06 "Remove / replace"):* Status: monitored read-only.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/jobs` | P | API-124;API-125 | resource-equivalent path elsewhere in catalogue |
| GET | `/api/v1/admin/health` | C | API-119 | exact |
| POST | `/api/v1/admin/incidents/{id}/resolve` | P | API-130 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_job_run` → ENT-173 `ops_job_run` (C); `growth_release` → ENT-177 `ops_release` (C); `growth_incident` → ENT-176 `ops_incident` (C)

**Integrations (doc 06):** github [DEV]; sentry [ADP]; aws [ADP]; Playwright [OSS]; AWS Core [ADP]; Claude Code Setup [DEV]; CLAUDE.md Management [DEV]; Postman [DEV]; GitHub [DEV]; Security Guidance [DEV]; Figma [DEV]; Plugin Developer Toolkit [DEV]; AWS Serverless [ADP]; cloudwatch [ADP]; Sentry [ADP]

### 2.7.21.13 A033: Workflow control centre

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-LIST + LP-GRAPH |
| Legacy screen ID · build class · location class (doc 06) | existing 035 · New · Admin |
| FR · wave · epic · profiles | FR-A033 (alias SM-FR-A033, trace M53; M55; B-AUTO, SM-UX-FR-A033) · W2 · EP-18 · CA-ALL, CA-ADMIN, CA-CONFIG, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Edit graph; validate; simulate; version and publish |
| Key actions (Part 2.5) | Create, Simulate, Submit, Enable, Pause, STOP |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure, pause and stop automated workflows |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A102; A038; A012; A109 |
| Tests | SM-UAT-S063; SM-UX-UAT-A033; unit families 001, 002, 015, 016, 017, 018, 019, 032, 033, 036, 047; **TC-ENH-C-234** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Workflow | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Trigger | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | select registry. Must belong to the same tenant and startup (composite FK) |
| 3 | Mode | B+R | C | Enumeration (Manual, Assisted, Supervised, Controlled Autonomous / L0–L3) | Select bounded by policy | policy bounded. Capped by DEC-064 autonomy limits |
| 4 | Policy | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Approval | B | P | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Node library | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Edge conditions | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Workflow revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 10 | Step budget | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Retry | A | C | Integer (computed) | Number (read-only) | Distinct records; Unknown ≠ 0 |
| 12 | Trigger ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 13 | Test fixture | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |

*Replace rules (doc 06 "Remove / replace"):* Trigger: select registry; Mode: policy bounded.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/admin/budgets/{id}/pause` | P | API-445 | resource-equivalent DERIVED path on same screen |
| GET | `/api/v1/workflows` | C | API-444 | exact |
| POST | `/api/v1/admin/workflows` | P | API-445;API-446;API-448;API-449 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/admin/workflows/pause` | C | API-445 | exact |
| POST | `/api/v1/admin/workflows/{id}/resume` | N | — | no exact or equivalent operation |
| GET | `/api/v1/workflows/{id}/executions` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_budget` → ENT-052 `ai_budget` (C); `growth_workflow` → ENT-159 `aut_workflow` (C); `growth_workflow_execution` → ENT-162 `aut_run` (P); `growth_step_run` → ENT-163 `aut_step_run` (C)

**Integrations (doc 06):** celery [OSS]

### 2.7.21.14 A047: Compliance incident dashboard

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-DASH + LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 051 · New · Admin |
| FR · wave · epic · profiles | FR-A047 (alias SM-FR-A047, trace M57, SM-UX-FR-A047) · W3 · EP-03 · CA-ALL, CA-ADMIN |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Suspend violating actions and escalate |
| Key actions (Part 2.5) | Contain, Resolve |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Monitor complaints, violations and automatic pause |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A007; A013; A014 |
| Tests | SM-UAT-S077; SM-UX-UAT-A047; unit families 001, 002, 003, 008, 009, 013, 045; **TC-ENH-C-235** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Incident | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Channel | B | C | Enumeration (email, whatsapp, web, phone, social, portal) | Select / channel icon | Only channels enabled and eligible for scope |
| 3 | Severity | B+R | C | Enumeration | Badge / select | rule-derived with reviewer override. Allowed values from configuration |
| 4 | Policy | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Owner | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Policy revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Affected run | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Containment action | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Evidence | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 11 | Resolution deadline | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |

*Replace rules (doc 06 "Remove / replace"):* Severity: rule-derived with reviewer override.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/compliance` | C | API-070 | exact |
| POST | `/api/v1/admin/compliance/{id}/resolve` | P | API-094 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_audit_event` → ENT-172 `ops_audit_event` (C); `growth_policy_decision` → ENT-032 `gov_policy_decision` (C); `growth_compliance_incident` → ENT-039 `gov_compliance_incident` (C)

**Integrations (doc 06):** Security Guidance [DEV]

### 2.7.21.15 A084: AI quality and feedback review

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-DASH + LP-LIST |
| Legacy screen ID · build class · location class (doc 06) | existing 094 · Extension · Admin |
| FR · wave · epic · profiles | FR-A084 (alias SM-FR-A084, trace M51; M54; B-QA, SM-UX-FR-A084) · W5 · EP-04 · CA-ALL, CA-ADMIN, CA-AI |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Compare model quality, cost and latency |
| Key actions (Part 2.5) | Queue eval, Accept feedback |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review corrected examples and approve model changes |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A011; A046; A102 |
| Tests | SM-UAT-S114; SM-UX-UAT-A084; unit families 001, 002, 015, 028, 029, 030, 031, 032, 033, 040, 041; **TC-ENH-C-236** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Model | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 2 | Evaluation set | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 3 | Accuracy | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | benchmark defined. Allowlisted, validated server-side |
| 4 | Latency | B | C | Period or duration | Period picker / duration display | Bounded; freshness shown against target (amber when stale) |
| 5 | Cost | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 6 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 7 | Dataset revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 8 | Sample size | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Baseline quality | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Gate result | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Rollback | A | C | Computed indicator | Indicator badge or tile (read-only) | Computed server-side with as_of; Unknown shown separately |

*Replace rules (doc 06 "Remove / replace"):* Accuracy: benchmark defined.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| POST | `/api/v1/feedback` | C | API-418 | exact |
| GET | `/api/v1/feedback` | P | API-418 | path match, method differs |
| POST | `/api/v1/admin/evals/run` | C | API-138 | exact |
| GET | `/api/v1/admin/evals/results` | P | API-162 | resource-equivalent path elsewhere in catalogue |

**Tables → blueprint entities:** `growth_prompt_version` → ENT-045 `ai_prompt_version` (C); `growth_model_run` → ENT-046 `ai_model_run` (C); `growth_eval_case` → ENT-047 `ai_eval_case` (C); `growth_deal_outcome` → ENT-158 `lcy_outcome` (P); `growth_feedback` → ENT-157 `lcy_feedback` (P); `growth_eval_run` → ENT-048 `ai_eval_run` (C)

**Integrations (doc 06):** deepeval [OSS]; DeepEval [OSS]; Langfuse [ADP]; Skill Creator [DEV]

### 2.7.21.16 A090: Production release readiness

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-DASH + LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | existing 100 · Extension · Admin |
| FR · wave · epic · profiles | FR-A090 (alias SM-FR-A090, trace M62; B-QA, SM-UX-FR-A090) · W0 / W5 · EP-21 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Fail closed on incomplete release evidence |
| Key actions (Part 2.5) | Approve release |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Review release checks and incident drills; internal admin view |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A014; A009; A106 |
| Tests | SM-UAT-S120; SM-UX-UAT-A090; unit families 001, 002, 003, 008, 009, 013, 015, 033, 034, 035, 036, 043, 044, 045; **TC-ENH-C-237** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Control | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 2 | Evidence | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 3 | Environment | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Reviewer | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 5 | Severity | B | C | Enumeration | Badge / select | Allowed values from configuration |
| 6 | Status | B+R | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | computed from mandatory evidence. Changed only by controlled transition; never free text |
| 7 | Release ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Required control ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | Evidence digest | A | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 10 | Independent reviewer | A | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 11 | Blocking gate | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |

*Replace rules (doc 06 "Remove / replace"):* Status: computed from mandatory evidence.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/admin/releases` | C | API-120 | exact |
| POST | `/api/v1/admin/releases/{id}/approve` | P | API-132 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_approval` → ENT-034 `gov_approval` (C); `growth_release` → ENT-177 `ops_release` (C); `growth_incident` → ENT-176 `ops_incident` (C); `growth_test_run` → ENT-178 `ops_test_run` (C)

**Integrations (doc 06):** playwright [OSS]; pytest [OSS]; Playwright [OSS]; Postman [DEV]

### 2.7.21.17 A099: Tenant, startup and membership administration

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-LIST + LP-WIZARD |
| Legacy screen ID · build class · location class (doc 06) | existing 109 · Contextual panel · Admin |
| FR · wave · epic · profiles | FR-A099 (alias SM-FR-A099, trace B-TENANT, SM-UX-FR-A099) · W0 · EP-01 · CA-ALL, CA-ADMIN, CA-CONFIG, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Provision owned and third-party workspaces with independent data |
| Key actions (Part 2.5) | Provision, Suspend, Offboard |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Provision independent tenant, configure startup, assign product-specific roles and time-limited client support; suspend/offboard. |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A002; A100; A101; A112 |
| Tests | SM-UAT-S129; SM-UX-UAT-A099; unit families 001, 002, 003, 004, 005, 006, 007; **TC-ENH-C-238** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Tenant | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Startup | B+R | C | Entity reference (scoped FK) | Scoped lookup / select | dynamic directory. Must belong to the same tenant and startup (composite FK) |
| 3 | User | B | P | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |
| 4 | Role | B | P | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 5 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 6 | Ownership type | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 7 | Legal ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 8 | Tenant slug | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 9 | Service model | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 10 | Admin invite | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 11 | Capability profile | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 12 | Lifecycle state | A | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |

*Replace rules (doc 06 "Remove / replace"):* Access: scoped grants; Startup: dynamic directory.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sales/tenants` | P | API-026 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sales/tenants` | P | API-027;API-028 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sales/tenants/{id}/control` | N | — | no exact or equivalent operation |
| GET | `/api/v1/sales/startups` | P | API-029 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sales/startups` | P | API-030 | resource-equivalent DERIVED path on same screen |
| PATCH | `/api/v1/sales/startups/{id}` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/memberships` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/support-grants` | P | API-024 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `sales_startup` → ENT-002 `ten_startup` (P); `growth_approval` → ENT-034 `gov_approval` (C); `sales_tenant` → ENT-001 `ten_tenant` (P); `sales_membership` → ENT-008 `ten_membership` (P); `sales_support_grant` → ENT-188 `saas_support_access_grant` (P)

**Integrations (doc 06):** Internal React/Django [INT]

### 2.7.21.18 A100: Business profile templates and branding

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | existing 110 · Contextual panel · Admin |
| FR · wave · epic · profiles | FR-A100 (alias SM-FR-A100, trace B-TENANT, SM-UX-FR-A100) · W5 · EP-20 · CA-ALL, CA-ADMIN, CA-CONFIG, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Generate reusable business config; review before activation |
| Key actions (Part 2.5) | Create, Validate, Submit, Apply |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Configure industry, offerings, typed filters, scoring, pipeline, approvals and verified domains; approved revision immutable. |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A099; A004; A107 |
| Tests | SM-UAT-S130; SM-UX-UAT-A100; unit families 001, 002, 003, 004, 005, 006, 007, 010, 011, 012, 013, 030; **TC-ENH-C-239** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Template | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Startup | B | P | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Business line | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Brand | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | separate approved theme revision. Allowlisted, validated server-side |
| 5 | Locale | B | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |
| 6 | Revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 7 | Approval | B | P | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 8 | Industry taxonomy | A | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 9 | Capability set | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 10 | Field schema | A | C | JSON Schema document (versioned) | Schema editor with validation report | Allowed field types only; validated before activation (CA-CONFIG) |
| 11 | Objective templates | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 12 | Workflow bindings | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 13 | Locale fallback | A | C | BCP 47 tag | Select (enabled locales) | DEC-026 enabled locales only |

*Replace rules (doc 06 "Remove / replace"):* Brand: separate approved theme revision.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sales/templates` | P | API-033 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sales/templates` | P | API-034;API-035;API-036;API-037 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sales/templates/{id}/control` | N | — | no exact or equivalent operation |
| GET | `/api/v1/sales/domains` | P | API-044 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sales/domains` | P | API-045 | resource-equivalent path elsewhere in catalogue |
| POST | `/api/v1/sales/domains/{id}/control` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `sales_brand_domain` → ENT-005 `ten_domain` (P); `sales_startup` → ENT-002 `ten_startup` (P); `growth_product` → ENT-016 `cat_offering` (P); `growth_approval` → ENT-034 `gov_approval` (C); `sales_business_template` → none  (N)

**Integrations (doc 06):** Internal React/Django [INT]

### 2.7.21.19 A101: Service subscriptions, usage and billing

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-LIST + LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | existing 111 · Contextual panel · Admin |
| FR · wave · epic · profiles | FR-A101 (alias SM-FR-A101, trace B-SVC, SM-UX-FR-A101) · W5 · EP-20 · CA-ALL, CA-ADMIN, CA-FIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Meter use; enforce plan and notify billing |
| Key actions (Part 2.5) | Change plan, Suspend, Approve rate revision |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Manage trials, feature limits, metered service charges, invoices, credits and margin; separate from customer transactions. |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A099; A012; A103 |
| Tests | SM-UAT-S131; SM-UX-UAT-A101; unit families 001, 002, 015, 033, 034, 035, 036, 040, 041, 043, 044; **TC-ENH-C-240** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Tenant | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Plan | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Usage | B | C | Integer (computed) | Number (read-only) | Distinct records; Unknown ≠ 0 |
| 4 | Budget | B+R | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | separate limit and consumption. Decimal only; currency required; server recomputes (CA-FIN) |
| 5 | Currency | B | C | ISO 4217 code | Select (allowed currencies) | Allowlist per startup TaxProfile (DEC-027) |
| 6 | Invoice | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 7 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 8 | Entitlement revision | A | C | Role / grant reference (scoped) | Multi-select with scope chips | Least privilege; change audited; revocation within 60 s (NFR-050) |
| 9 | Usage meter | A | C | Integer (computed) | Number (read-only) | Distinct records; Unknown ≠ 0 |
| 10 | Reserved spend | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Billing cycle | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 12 | Renewal date | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 13 | Suspension reason | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |

*Replace rules (doc 06 "Remove / replace"):* Budget: separate limit and consumption.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sales/service-plans` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/service-plans` | N | — | no exact or equivalent operation |
| GET | `/api/v1/sales/service-subscriptions` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/service-subscriptions/{id}/control` | N | — | no exact or equivalent operation |
| GET | `/api/v1/sales/service-invoices` | P | API-526 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/sales/service-invoices/{id}/reconcile` | P | API-154;API-254;API-304 | resource-equivalent path elsewhere in catalogue |
| GET | `/api/v1/sales/usage-charges` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/usage-charges/{id}/adjust` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_api_usage` → ENT-050 `ai_usage` (P); `growth_budget` → ENT-052 `ai_budget` (C); `sales_service_plan` → ENT-179 `saas_plan` (P); `sales_service_subscription` → ENT-182 `saas_subscription` (P); `sales_service_invoice` → ENT-184 `saas_service_invoice` (P); `sales_usage_charge` → ENT-183 `saas_usage_meter_reading` (P)

**Integrations (doc 06):** Internal React/Django [INT]

### 2.7.21.20 A102: Autonomous commercial planner and simulation

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-WIZARD + LP-DASH |
| Legacy screen ID · build class · location class (doc 06) | existing 112 · Contextual panel · Admin |
| FR · wave · epic · profiles | FR-A102 (alias SM-FR-A102, trace B-AUTO, SM-UX-FR-A102) · W2 (simulation) / W5 (L3) · EP-18 · CA-ALL, CA-ADMIN, CA-AI, CA-APPROVE, CA-DISPATCH |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Generate plan; simulate; launch eligible runs |
| Key actions (Part 2.5) | Generate, Simulate, Submit, Start, Pause, Stop |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Plan research, campaigns, follow-ups and tasks; simulate cost/eligibility; approve exact hash; activate or stop. |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A033; A015; A106; A012; A110 |
| Tests | SM-UAT-S132; SM-UX-UAT-A102; unit families 001, 002, 015, 016, 017, 018, 019, 032, 033, 036, 047; **TC-ENH-C-241** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Plan | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 2 | Startup | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Objective | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Mode | B+R | C | Enumeration (Manual, Assisted, Supervised, Controlled Autonomous / L0–L3) | Select bounded by policy | policy bounded. Capped by DEC-064 autonomy limits |
| 5 | Budget | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 6 | Policy | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 7 | Status | B | P | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 8 | Objective ID | A | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 9 | Plan revision | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 10 | Template IDs | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 11 | Concurrency limit | A | C | Integer limit (bounded) | Number input with unit | Within plan/entitlement bounds; tightening needs no approval, loosening does (DEC-038) |
| 12 | Simulation cost | A | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 13 | Stop policy | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 14 | Approval gate | A | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |

*Replace rules (doc 06 "Remove / replace"):* Mode: policy bounded.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sales/action-plans` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/action-plans` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/action-plans/{id}/control` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_task` → ENT-148 `lcy_task` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_budget` → ENT-052 `ai_budget` (C); `growth_workflow` → ENT-159 `aut_workflow` (C); `growth_workflow_execution` → ENT-162 `aut_run` (P); `sales_action_plan` → ENT-164 `aut_autonomy_plan` (P)

**Integrations (doc 06):** Internal React/Django [INT]

### 2.7.21.21 A103: Import, export and client portability

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Admin |
| Command Centre view · pattern (Part 2.5) | Automation · LP-WIZARD |
| Legacy screen ID · build class · location class (doc 06) | existing 113 · Contextual panel · Admin |
| FR · wave · epic · profiles | FR-A103 (alias SM-FR-A103, trace B-SVC, SM-UX-FR-A103) · W1 (import) / W5 (portability) · EP-20 · CA-ALL, CA-ADMIN, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Export scoped records; controlled offboarding |
| Key actions (Part 2.5) | Validate, Submit, Download |
| Screen acceptance (doc 06) | Apply authorized workspace scope; filter by relevant record state and dates |
| Intent (doc 17) | Quarantined import, typed mapping, validation and commit; secure export, offboard and retention. |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A013; A099; A101 |
| Tests | SM-UAT-S133; SM-UX-UAT-A103; unit families 001, 002, 004, 014, 015, 016, 017, 018, 019, 032, 033, 036, 042, 047; **TC-ENH-C-242** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Request type | B | C | Enumeration from versioned taxonomy (ref_value) | Select / multi-select (taxonomy) | Values from the active reference dataset (CFG-32); unknown values rejected |
| 2 | Entity | B+R | C | Text or enumeration (confirm in data dictionary) | Text input / select | authorized selection. Allowlisted, validated server-side |
| 3 | Format | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 4 | Scope | B | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 5 | Reason | B | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 6 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 7 | Data classification | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Export scope | A | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 9 | Redaction | A | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Expiry | A | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 11 | Format version | A | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 12 | Legal hold | A | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |

*Replace rules (doc 06 "Remove / replace"):* Entity: authorized selection.

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/sales/data-transfers` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/data-transfers` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/data-transfers/{id}/complete` | N | — | no exact or equivalent operation |
| POST | `/api/v1/sales/data-transfers/{id}/control` | N | — | no exact or equivalent operation |
| GET | `/api/v1/sales/data-transfers/{id}/download` | P | API-535 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `sales_startup` → ENT-002 `ten_startup` (P); `growth_privacy_request` → ENT-036 `gov_privacy_request` (C); `growth_approval` → ENT-034 `gov_approval` (C); `growth_job_run` → ENT-173 `ops_job_run` (C); `sales_data_transfer` → ENT-189 `saas_export_job` (P)

**Integrations (doc 06):** Internal React/Django [INT]

### 2.7.21.22 A109: Event & Trigger Management Centre

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Confidential Admin; assigned role and scope required |
| Command Centre view · pattern (Part 2.5) | Automation · LP-LIST + LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | new in 147-scope · Template/typed configuration (doc 06 operating contract) · Admin (new interface) |
| FR · wave · epic · profiles | FR-A109 (alias SM-FR-A109, SM-UX-FR-A109) · W2 · EP-18 · CA-ALL, CA-ADMIN, CA-CONFIG |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Create; test synthetic event; replay in sandbox; enable; pause |
| Key actions (Part 2.5) | Create, Test, Sandbox replay, Enable, Pause |
| Screen acceptance (doc 06) | Verify signatures and scope; dedupe; never replay a live side effect |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A033; A102; A110 |
| Tests | no SM-UAT alias (new interface, Part 6.1 §6.1.12.5); SM-UX-UAT-A109; unit families n/a; **TC-ENH-C-243** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Trigger ID | B | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 2 | Event type | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Source | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 4 | Event schema version | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 5 | Startup scope | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 6 | Objective | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 7 | Schedule | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 8 | Timezone | B | C | IANA time-zone ID | Searchable select | Must be a valid IANA zone; default from user/startup profile |
| 9 | Condition | B | C | Typed rule expression | RuleBuilder (typed conditions) | Sandboxed expression over typed fields (DEC-051); validated and simulated |
| 10 | Workflow version | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 11 | Dedup window | B | C | Duration (ISO 8601) or time window | Duration input | Within configured bounds |
| 12 | Enabled | B | C | Boolean | Toggle (role-gated) | Change audited |
| 13 | Last fire | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 14 | Next fire | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 15 | Credential reference | B | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/workspace/admin/triggers` | P | API-459 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/commercial/workspace/admin/triggers` | P | API-460;API-462;API-463;API-464 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/commercial/workspace/admin/triggers/{id}/control` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_workflow` → ENT-159 `aut_workflow` (C); `sales_ui_trigger_revision` → ENT-161 `aut_trigger` (P)

### 2.7.21.23 A110: Live Automation Execution Monitor

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Confidential Admin; assigned role and scope required |
| Command Centre view · pattern (Part 2.5) | Automation · LP-MONITOR |
| Legacy screen ID · build class · location class (doc 06) | new in 147-scope · Template/typed configuration (doc 06 operating contract) · Admin (new interface) |
| FR · wave · epic · profiles | FR-A110 (alias SM-FR-A110, SM-UX-FR-A110) · W2 · EP-18 · CA-ALL, CA-ADMIN, CA-DISPATCH |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Filter; inspect run; pause; resume; request retry; cancel; export evidence |
| Key actions (Part 2.5) | Pause, Resume, Request retry, Cancel, Export evidence |
| Screen acceptance (doc 06) | Pause/resume revalidate policy; unknown external outcome must reconcile before retry |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A109; A111; A014; A102; A089 |
| Tests | no SM-UAT alias (new interface, Part 6.1 §6.1.12.5); SM-UX-UAT-A110; unit families n/a; **TC-ENH-C-244** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Run ID | B | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 2 | Workflow revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 3 | Trigger event ID | B | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 4 | Startup | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 5 | Objective | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 6 | Mode | B | C | Enumeration (Manual, Assisted, Supervised, Controlled Autonomous / L0–L3) | Select bounded by policy | Capped by DEC-064 autonomy limits |
| 7 | Current node | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Progress | B | C | Decimal 0–100 (or 0–1) computed | ScoreBreakdown / progress bar (read-only) | Computed server-side; Unknown shown separately from 0 |
| 9 | Started | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 10 | Wait reason | B | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 11 | Cost reserved | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 12 | Actual cost | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 13 | Retry count | B | C | Integer (computed) | Number (read-only) | Distinct records; Unknown ≠ 0 |
| 14 | Outcome certainty | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |
| 15 | Evidence | B | C | Evidence / source reference | CitationChip or EvidenceCard (drawer) | Must resolve to permitted, unexpired evidence |
| 16 | Owner | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/workspace/admin/executions` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_workflow_execution` → ENT-162 `aut_run` (P); `growth_step_run` → ENT-163 `aut_step_run` (C)

### 2.7.21.24 A111: Automation Coordination & Conflict Resolution

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Confidential Admin; assigned role and scope required |
| Command Centre view · pattern (Part 2.5) | Automation · LP-QUEUE |
| Legacy screen ID · build class · location class (doc 06) | new in 147-scope · Template/typed configuration (doc 06 operating contract) · Admin (new interface) |
| FR · wave · epic · profiles | FR-A111 (alias SM-FR-A111, SM-UX-FR-A111) · W3 · EP-18 · CA-ALL, CA-ADMIN, CA-DISPATCH |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Hold; merge candidate; choose eligible action; escalate; audit |
| Key actions (Part 2.5) | Hold, Merge, Choose, Escalate |
| Screen acceptance (doc 06) | Never expose unrelated tenant data; use idempotency and policy before dispatch |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A110; A037; A047 |
| Tests | no SM-UAT alias (new interface, Part 6.1 §6.1.12.5); SM-UX-UAT-A111; unit families n/a; **TC-ENH-C-245** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Conflict ID | B | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 2 | Scope | B | C | Text (≤ 4,000) | Text area with counter | No secrets or special-category data; length limit |
| 3 | Relationship ID | B | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 4 | Candidate runs | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 5 | Action type | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 6 | Duplicate key | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 7 | Priority | B | C | Enumeration | Badge / select | Allowed values from configuration |
| 8 | Frequency count | B | C | Schedule rule (RRULE) | Schedule builder | Bounded by caps and quiet hours |
| 9 | Suppression | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 10 | Budget reservation | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Conflict rule | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 12 | Resolution | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 13 | Reviewer | B | C | User/team reference (scoped membership) | User picker (scoped) | Only members with the required role in scope |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/workspace/admin/conflicts` | P | API-473;API-474 | resource-equivalent DERIVED path on same screen |
| POST | `/api/v1/commercial/workspace/admin/conflicts/{id}/resolve` | P | API-475 | resource-equivalent DERIVED path on same screen |

**Tables → blueprint entities:** `growth_workflow_execution` → ENT-162 `aut_run` (P); `sales_ui_conflict` → ENT-165 `aut_conflict_case` (P)

### 2.7.21.25 A112: Business Configuration Change Centre

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Confidential Admin; assigned role and scope required |
| Command Centre view · pattern (Part 2.5) | Automation · LP-CONFIG |
| Legacy screen ID · build class · location class (doc 06) | new in 147-scope · Template/typed configuration (doc 06 operating contract) · Admin (new interface) |
| FR · wave · epic · profiles | FR-A112 (alias SM-FR-A112, SM-UX-FR-A112) · W5 · EP-20 · CA-ALL, CA-ADMIN, CA-CONFIG, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Compare; simulate; approve; publish; revert future config |
| Key actions (Part 2.5) | Validate, Simulate, Submit, Schedule, Roll back |
| Screen acceptance (doc 06) | Running workflow revisions remain immutable; no authorization expansion without review |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A099; A100; A102; A113 |
| Tests | no SM-UAT alias (new interface, Part 6.1 §6.1.12.5); SM-UX-UAT-A112; unit families n/a; **TC-ENH-C-246** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Configuration ID | B | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 2 | Tenant | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Startup | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Active revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 5 | Candidate revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 6 | Field/capability diff | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 7 | Affected UI and workflows | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Risk | B | C | Enumeration | Badge / select | Allowed values from configuration |
| 9 | Validation report | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 10 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 11 | Effective date | B | C | Timestamp (UTC stored) or date | DateTimePicker with time zone / DateTimeDisplay | Stored UTC; displayed in user and record time zone; range validated |
| 12 | Rollback revision | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/workspace/admin/configurations` | N | — | no exact or equivalent operation |
| POST | `/api/v1/commercial/workspace/admin/configurations` | N | — | no exact or equivalent operation |
| POST | `/api/v1/commercial/workspace/admin/configurations/{id}/control` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `sales_startup` → ENT-002 `ten_startup` (P); `sales_ui_config_revision` → ENT-168 `aut_config_revision` (P)

### 2.7.21.26 A113: Automation Template & Node Library

| Attribute | Value |
|---|---|
| Surface / access (doc 06) | Confidential Admin; assigned role and scope required |
| Command Centre view · pattern (Part 2.5) | Automation · LP-LIST + detail |
| Legacy screen ID · build class · location class (doc 06) | new in 147-scope · Template/typed configuration (doc 06 operating contract) · Admin (new interface) |
| FR · wave · epic · profiles | FR-A113 (alias SM-FR-A113, SM-UX-FR-A113) · W2 · EP-18 · CA-ALL, CA-ADMIN, CA-CONFIG, CA-APPROVE |
| Filters | FLT-01 Scope, FLT-05 Operations (workflow state, approval, cost, quota, error, as_of) |
| Automation (doc 06/17) | Search; clone; configure; test; approve; publish; deprecate |
| Key actions (Part 2.5) | Clone, Configure, Test, Submit, Deprecate |
| Screen acceptance (doc 06) | Only approved nodes; no arbitrary code or secret values; immutable published versions |
| Interaction pattern (doc 17 → 2.7a §2.7.5.2) | IP-ADMIN |
| Related screens (in-context links, FR-ENH-C-012) | A033; A102; A109; A112 |
| Tests | no SM-UAT alias (new interface, Part 6.1 §6.1.12.5); SM-UX-UAT-A113; unit families n/a; **TC-ENH-C-247** (field and contract conformance) |

**Field contract**

| # | Field | Origin | Status | Type | Control | Validation and rule |
|---|---|---|---|---|---|---|
| 1 | Template ID | B | C | Identifier (UUIDv7 or opaque reference) | Read-only text, copy button | Server-generated; not user-editable |
| 2 | Business capability | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 3 | Objective | B | C | Entity reference (scoped FK) | Scoped lookup / select | Must belong to the same tenant and startup (composite FK) |
| 4 | Version | B | C | Integer revision / version label | Read-only label with diff link | Optimistic concurrency; stale → 409 |
| 5 | Node types | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 6 | Input/output schema | B | C | JSON Schema document (versioned) | Schema editor with validation report | Allowed field types only; validated before activation (CA-CONFIG) |
| 7 | Allowed channels | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 8 | Required permissions | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 9 | Risk class | B | C | Enumeration | Badge / select | Allowed values from configuration |
| 10 | Cost estimate | B | C | Money: Decimal(18,2) + ISO 4217 | MoneyInput / MoneyDisplay | Decimal only; currency required; server recomputes (CA-FIN) |
| 11 | Test fixtures | B | C | Text or enumeration (confirm in data dictionary) | Text input / select | Allowlisted, validated server-side |
| 12 | Approval | B | C | Approval reference (gov_approval) | Approval chip with approver and SLA | Computed from Approval record; hash-bound (CA-APPROVE) |
| 13 | Deprecation status | B | C | Enumeration (state machine, Part 2.3) | StateBadge; transition menu shows only valid transitions | Changed only by controlled transition; never free text |

**Legacy operations → blueprint API**

| Method | Source path | Status | Blueprint op(s) | Match basis |
|---|---|---|---|---|
| GET | `/api/v1/commercial/workspace/admin/automation-templates` | N | — | no exact or equivalent operation |
| POST | `/api/v1/commercial/workspace/admin/automation-templates` | N | — | no exact or equivalent operation |
| POST | `/api/v1/commercial/workspace/admin/automation-templates/{id}/control` | N | — | no exact or equivalent operation |

**Tables → blueprint entities:** `growth_workflow` → ENT-159 `aut_workflow` (C); `sales_ui_template_revision` → ENT-167 `aut_workflow_template` (P)


## 2.7.22 Per-screen conformance test cases (TC-ENH-C-101…247)

Each card's conformance test is one parameterized test case run against the card. All follow this template; the parameter set is the card itself.

```gherkin
Feature: Screen field and contract conformance (TC-ENH-C-1nn)
  Scenario Outline: Screen <screen> matches its contract card
    Given a two-tenant synthetic fixture with startups S1 and S2 and a user holding the card's role in S1 only
    When the user opens <screen> in scope S1
    Then every field in the card is rendered with its declared control, label and validation
    And read-only, computed and lifecycle-derived fields cannot be edited in the UI or through the API
    And each legacy operation in the card resolves to the mapped blueprint operation with identical authorization
    And the network log shows no call outside the card's operations and no Admin route from a Website bundle
    When the user switches scope to S2 without a grant
    Then in-flight requests are aborted, cached S1 records are cleared and a denied state is shown
    And loading, empty, denied, stale, error and success states each render with an accessible name
  Examples:
    | screen |
    | each of the 147 card IDs |
```

| TC | Screen | TC | Screen | TC | Screen | TC | Screen |
|---|---|---|---|---|---|---|---|
| TC-ENH-C-101 | W01 | TC-ENH-C-102 | W02 | TC-ENH-C-103 | W03 | TC-ENH-C-104 | W04 |
| TC-ENH-C-105 | W05 | TC-ENH-C-106 | W06 | TC-ENH-C-107 | W07 | TC-ENH-C-108 | W08 |
| TC-ENH-C-109 | W09 | TC-ENH-C-110 | W10 | TC-ENH-C-111 | W11 | TC-ENH-C-112 | W30 |
| TC-ENH-C-113 | W31 | TC-ENH-C-114 | W12 | TC-ENH-C-115 | W13 | TC-ENH-C-116 | W14 |
| TC-ENH-C-117 | W15 | TC-ENH-C-118 | W16 | TC-ENH-C-119 | W17 | TC-ENH-C-120 | W18 |
| TC-ENH-C-121 | W19 | TC-ENH-C-122 | W20 | TC-ENH-C-123 | W32 | TC-ENH-C-124 | W21 |
| TC-ENH-C-125 | W22 | TC-ENH-C-126 | W23 | TC-ENH-C-127 | W24 | TC-ENH-C-128 | W25 |
| TC-ENH-C-129 | W26 | TC-ENH-C-130 | W27 | TC-ENH-C-131 | W28 | TC-ENH-C-132 | W29 |
| TC-ENH-C-133 | W33 | TC-ENH-C-134 | W34 | TC-ENH-C-135 | A001 | TC-ENH-C-136 | A003 |
| TC-ENH-C-137 | A106 | TC-ENH-C-138 | A018 | TC-ENH-C-139 | A029 | TC-ENH-C-140 | A030 |
| TC-ENH-C-141 | A031 | TC-ENH-C-142 | A032 | TC-ENH-C-143 | A042 | TC-ENH-C-144 | A043 |
| TC-ENH-C-145 | A082 | TC-ENH-C-146 | A083 | TC-ENH-C-147 | A087 | TC-ENH-C-148 | A088 |
| TC-ENH-C-149 | A089 | TC-ENH-C-150 | A097 | TC-ENH-C-151 | A098 | TC-ENH-C-152 | A015 |
| TC-ENH-C-153 | A016 | TC-ENH-C-154 | A017 | TC-ENH-C-155 | A019 | TC-ENH-C-156 | A020 |
| TC-ENH-C-157 | A021 | TC-ENH-C-158 | A022 | TC-ENH-C-159 | A023 | TC-ENH-C-160 | A024 |
| TC-ENH-C-161 | A025 | TC-ENH-C-162 | A026 | TC-ENH-C-163 | A027 | TC-ENH-C-164 | A028 |
| TC-ENH-C-165 | A048 | TC-ENH-C-166 | A049 | TC-ENH-C-167 | A085 | TC-ENH-C-168 | A086 |
| TC-ENH-C-169 | A034 | TC-ENH-C-170 | A035 | TC-ENH-C-171 | A036 | TC-ENH-C-172 | A037 |
| TC-ENH-C-173 | A044 | TC-ENH-C-174 | A045 | TC-ENH-C-175 | A050 | TC-ENH-C-176 | A051 |
| TC-ENH-C-177 | A052 | TC-ENH-C-178 | A053 | TC-ENH-C-179 | A054 | TC-ENH-C-180 | A055 |
| TC-ENH-C-181 | A056 | TC-ENH-C-182 | A057 | TC-ENH-C-183 | A058 | TC-ENH-C-184 | A059 |
| TC-ENH-C-185 | A060 | TC-ENH-C-186 | A061 | TC-ENH-C-187 | A062 | TC-ENH-C-188 | A063 |
| TC-ENH-C-189 | A064 | TC-ENH-C-190 | A107 | TC-ENH-C-191 | A108 | TC-ENH-C-192 | A038 |
| TC-ENH-C-193 | A039 | TC-ENH-C-194 | A040 | TC-ENH-C-195 | A041 | TC-ENH-C-196 | A075 |
| TC-ENH-C-197 | A076 | TC-ENH-C-198 | A077 | TC-ENH-C-199 | A078 | TC-ENH-C-200 | A079 |
| TC-ENH-C-201 | A080 | TC-ENH-C-202 | A081 | TC-ENH-C-203 | A091 | TC-ENH-C-204 | A092 |
| TC-ENH-C-205 | A093 | TC-ENH-C-206 | A094 | TC-ENH-C-207 | A095 | TC-ENH-C-208 | A096 |
| TC-ENH-C-209 | A046 | TC-ENH-C-210 | A069 | TC-ENH-C-211 | A070 | TC-ENH-C-212 | A065 |
| TC-ENH-C-213 | A066 | TC-ENH-C-214 | A067 | TC-ENH-C-215 | A068 | TC-ENH-C-216 | A071 |
| TC-ENH-C-217 | A072 | TC-ENH-C-218 | A073 | TC-ENH-C-219 | A074 | TC-ENH-C-220 | A104 |
| TC-ENH-C-221 | A105 | TC-ENH-C-222 | A002 | TC-ENH-C-223 | A004 | TC-ENH-C-224 | A005 |
| TC-ENH-C-225 | A006 | TC-ENH-C-226 | A007 | TC-ENH-C-227 | A008 | TC-ENH-C-228 | A009 |
| TC-ENH-C-229 | A010 | TC-ENH-C-230 | A011 | TC-ENH-C-231 | A012 | TC-ENH-C-232 | A013 |
| TC-ENH-C-233 | A014 | TC-ENH-C-234 | A033 | TC-ENH-C-235 | A047 | TC-ENH-C-236 | A084 |
| TC-ENH-C-237 | A090 | TC-ENH-C-238 | A099 | TC-ENH-C-239 | A100 | TC-ENH-C-240 | A101 |
| TC-ENH-C-241 | A102 | TC-ENH-C-242 | A103 | TC-ENH-C-243 | A109 | TC-ENH-C-244 | A110 |
| TC-ENH-C-245 | A111 | TC-ENH-C-246 | A112 | TC-ENH-C-247 | A113 |  |  |

Priority: P0 for screens with CA-FIN, CA-DISPATCH or CA-APPROVE profiles; P1 otherwise. Automation: Playwright component and end-to-end suites with axe-core; API leg via Schemathesis contract tests (Part 6.1). Each TC links FR-… of its screen, FR-ENH-C-002 and FR-ENH-C-003.

## 2.7.23 Quality gate: Batch 2.7b

| # | Check | Result | Notes and fixes applied |
|---|---|---|---|
| 1 | Every requirement traced to a source | Pass | Every card row cites doc 06/17 content and the blueprint row it reconciles |
| 2 | Assumptions, gaps, conflicts tagged and logged | Pass | ASSUMPTION-341/343, GAP-340/349, CONFLICT-346 used here; register in Batch 2.7a §2.7.8 |
| 3 | IDs unique and consistent | Pass | 147 cards, one per screen; TC-ENH-C-101…247 unique; FR, API and ENT IDs from Parts 2.1, 3.2, 3.3 |
| 4 | No requirement lacks a test | Pass | One conformance TC per card plus alias tests |
| 5 | Negative, edge, security, accessibility | Pass | Conformance template covers cross-scope denial, read-only enforcement, states and accessible names |
| 6 | Agents: guardrail, fallback, KPI, cost | N/A | No agent defined in this batch |
| 7 | Time-sensitive facts flagged | Pass | Integration prices not restated; classification ADP/CMU says verify at implementation (as of 27 Nov 2026) |
| 8 | No restricted data to free-tier models | Pass | No routing change |
| 9 | Consistent with earlier parts | Pass | Types defer to Part 3.3 data dictionary on conflict (ASSUMPTION-341) |

**Status: Part 2 Batch 2.7b complete. 147 screen contract cards, 1604 field rows, 444 screen-operation rows, 155 table mappings, 147 conformance test cases.**
