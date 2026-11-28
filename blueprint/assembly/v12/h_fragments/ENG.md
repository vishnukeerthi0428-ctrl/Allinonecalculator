| File | Parsed content | Operations outside reconciled set | Disposition |
|---|---|---|---|
| src/engineering/api_catalog.json | 302 operations (A–Y source columns incl. licence, quota, allocation) | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/api_contract_review.csv | 302 rows; contract_status: Review required — source payload is descriptive 38; Proposed cursor/page-size parameters; response DTO still blocked 82; Proposed explicit DTO — approval required 164; Adapter contract review — provider-specific; no browser endpoint 17; Proposed public response allowlist — approval required 1 | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/api_field_proposals.csv | 1370 field rows for 266 operations (body 633, response 464, query 164, path 109); all approval Pending | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/closure/api_candidate_contracts.csv/.json | 38 decision rows (25 candidate DTOs, 8 provider bindings, 5 identity reuse) = SRC07-DEC-001…038 | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/closure/openapi_closure_candidate.json/.yaml | 285 operations on 255 paths; no component schemas | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/starter/openapi_catalog_draft.json/.yaml | 285 operations; identical operation set to the closure candidate | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/starter/api_payload_review.csv | 285 rows; source_typed No for all; reviews Pending | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
| src/engineering/ui_upgrade/candidate_openapi.json | 19 operations = SM-UX-API-01…19 | 0 | Covered by Part 3.5a/3.5b; V12 conventions (DEC-641) apply |
