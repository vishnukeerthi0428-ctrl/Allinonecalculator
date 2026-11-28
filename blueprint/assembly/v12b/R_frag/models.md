#### M01 Tenant SSO sign-in: IdP × protocol × role × region × domain × enforcement × MFA × assertion

Capability C1 · stories US-01-ZR01, US-01-ZR02 · traces FR-V12-R-001…010; ENT-IDN-01/02/04/05/06; DEC-784; DEC-772

| Parameter | Values | Count |
|---|---|---|
| `idp` | Okta · Microsoft Entra ID · Google Workspace · Generic SAML IdP · Generic OIDC IdP | 5 |
| `protocol` | SAML 2.0 · OIDC | 2 |
| `role` | R12 tenant admin · R02 startup head · R03 growth manager · R15 auditor · Custom privileged role | 5 |
| `region` | IN · EU | 2 |
| `domain` | verified · unverified · verification lost (TXT missing twice) | 3 |
| `enforcement` | off · on | 2 |
| `mfa` | phishing-resistant (amr hwk/webauthn) · OTP (amr otp) · none | 3 |
| `assertion` | valid · wrong audience · wrong issuer · expired (NotOnOrAfter + 60 s skew passed) · replayed assertion or code · unsigned or alg none | 6 |

Raw product 10,800 · valid after constraints 7,200 · method **3-way** · 2,151 valid 3-tuples · **164 cases** (TC-V12-R-101…TC-V12-R-264) · pairwise alone would need 36

#### M02 SCIM 2.0 provisioning: IdP × operation × user state × group mapping × token × region endpoint

Capability C1 · stories US-01-ZR03 · traces FR-V12-R-011…016; ENT-IDN-03; RFC 7643/7644; DEC-784

| Parameter | Values | Count |
|---|---|---|
| `idp` | Okta · Microsoft Entra ID · Google Workspace | 3 |
| `op` | POST create · PUT replace · PATCH active=false · DELETE · PATCH group add · PATCH group remove | 6 |
| `user` | not yet provisioned · active member · deprovisioned · break-glass account | 4 |
| `mapping` | mapped to built-in role · mapped to custom role · mapped to conflicting custom role · unmapped group | 4 |
| `token` | valid · revoked · expired · other tenant | 4 |
| `endpoint` | home-region host · other-region host | 2 |

Raw product 2,304 · valid after constraints 1,824 · method **3-way** · 995 valid 3-tuples · **118 cases** (TC-V12-R-265…TC-V12-R-382) · pairwise alone would need 29

#### M03 Custom roles and separation of duties: permission pair × path × scope × actor

Capability C1 · stories US-01-ZR04 · traces FR-V12-R-017…022; ENT-ACC-01/02; C2-T1; DEC-784

| Parameter | Values | Count |
|---|---|---|
| `pair` | Runs:create + Runs:approve · Configuration:edit + Configuration:approve · Billing:view + Billing:approve · Runs:approve + Runs:dispatch · Finance:verify_first + Finance:verify_second · Leads:read + Leads:write (no conflict) | 6 |
| `path` | API role save · Direct DB insert as app_rw · Membership assignment of two roles · SCIM group mapping | 4 |
| `scope` | tenant-wide · company-scoped | 2 |
| `actor` | R12 tenant admin · R01 founder (owned tenant) · R13 operator support (no JIT grant) · Custom admin lacking billing.approve | 4 |

Raw product 192 · valid after constraints 192 · method **2-way** · 92 valid 2-tuples · **24 cases** (TC-V12-R-383…TC-V12-R-406)

#### M04 Developer API credentials: credential × state × scope × region × host × rate

Capability C2 · stories US-20-ZR06, US-20-ZR07 · traces FR-V12-R-031…040; ENT-API-01/02/03; DEC-785

| Parameter | Values | Count |
|---|---|---|
| `cred` | API key gek_ · OAuth client private_key_jwt · OAuth client client_secret_basic | 3 |
| `state` | active · expired · revoked (≤ 60 s ago) · IP not in allowlist | 4 |
| `scope` | leads:read · leads:write · runs:create · missing scope · approve/send/pay (non-existent scope) | 5 |
| `region` | home region host · other region host | 2 |
| `host` | developer host · browser host (admin/web origin) | 2 |
| `rate` | under limit · at limit · over limit | 3 |

Raw product 720 · valid after constraints 720 · method **3-way** · 593 valid 3-tuples · **67 cases** (TC-V12-R-407…TC-V12-R-473) · pairwise alone would need 22

#### M05 Outbound webhook delivery: event × endpoint response × attempt × endpoint state × region

Capability C2 · stories US-20-ZR08 · traces FR-V12-R-041…046; ENT-API-05; DEC-785

| Parameter | Values | Count |
|---|---|---|
| `event` | lead.created · run.awaiting_approval · invoice.issued · connector.degraded | 4 |
| `response` | 2xx within 10 s · 5xx · timeout > 10 s · 410 Gone · TLS failure · 3xx redirect | 6 |
| `attempt` | 1 · 3 · 6 | 3 |
| `endpoint` | verified · unverified (challenge not passed) | 2 |
| `region` | IN · EU | 2 |

Raw product 288 · valid after constraints 288 · method **2-way** · 110 valid 2-tuples · **24 cases** (TC-V12-R-474…TC-V12-R-497)

#### M06 Webhook signature verification in the SDKs: timestamp × signature × replay (exhaustive)

Capability C2 · stories US-20-ZR08, US-20-ZR10 · traces FR-V12-R-042, 052; ENT-API-05/06

| Parameter | Values | Count |
|---|---|---|
| `timestamp` | fresh · 299 s old · 301 s old · 301 s in the future | 4 |
| `signature` | valid current secret · valid previous secret within 24 h overlap · previous secret after 24 h overlap · tampered body · wrong secret | 5 |
| `replay` | first delivery · duplicate event_id | 2 |

Raw product 40 · valid after constraints 40 · method **exhaustive** · **40 cases** (TC-V12-R-498…TC-V12-R-537)

#### M07 Connectors: connector × auth × failure mode × residency × environment × activation gate

Capability C3 · stories US-18-ZR11, US-07-ZR12, US-07-ZR13, US-23-ZR14, US-22-ZR15 · traces FR-V12-R-056…080; ENT-INT-01…05; INT-01/04/05; CJ-IN-06/07; DEC-785

| Parameter | Values | Count |
|---|---|---|
| `connector` | Salesforce · HubSpot · Zoho CRM · SMS-DLT aggregator · Voice CPaaS (140/160 series) | 5 |
| `auth` | OAuth 2.0 auth code + PKCE · OAuth 2.0 client credentials / JWT bearer · API key in vault | 3 |
| `failure` | none · 429 throttled · 5xx · 401 token revoked · timeout on write (uncertain) · validation 4xx · DLT template mismatch · DND/preference-registry hit · missed provider event (gap) | 9 |
| `residency` | IN · EU | 2 |
| `env` | sandbox · production | 2 |
| `gate` | complete · DPA missing · transfer basis CJ-R15 missing · DLT registration missing · security review missing | 5 |

Raw product 2,700 · valid after constraints 624 · method **3-way** · 976 valid 3-tuples · **184 cases** (TC-V12-R-538…TC-V12-R-721) · pairwise alone would need 47

#### M08 Vercel personal-data path: surface × tenant region × request × header × logging × function region

Capability C4 · stories US-21-ZR16, US-21-ZR17 · traces FR-V12-R-081…095; DEC-786; DEC-772

| Parameter | Values | Count |
|---|---|---|
| `surface` | Website (startup domain) · Portal (customer) · Admin · Developer portal | 4 |
| `region` | IN · EU | 2 |
| `request` | page GET (no personal data) · API POST with personal data · file upload (portal document) · auth callback | 4 |
| `header` | allowlisted only · non-allowlisted header added · X-Origin-Verify missing (direct-to-origin) | 3 |
| `logging` | metadata only · body capture attempted | 2 |
| `function_region` | pinned to home region · deployed to a non-home region | 2 |

Raw product 384 · valid after constraints 288 · method **3-way** · 392 valid 3-tuples · **46 cases** (TC-V12-R-722…TC-V12-R-767) · pairwise alone would need 17

#### M09 Recovery: region × failure × WAL archive age × restore path × release gate

Capability C5 · stories US-21-ZR18, US-21-ZR19 · traces FR-V12-R-096…110; DEC-787; DEC-771; KPI-18/19/32; OPT-TC-ST-14

| Parameter | Values | Count |
|---|---|---|
| `region` | IN · EU | 2 |
| `failure` | row corruption by bug · bad migration · accidental tenant delete · Supabase project unavailable · AZ loss · region loss | 6 |
| `wal_age` | 1 min · 5 min · 14 min · 16 min | 4 |
| `path` | Supabase PITR to new project · AWS WAL-G archive restore · AWS WAL-G archive restore (in-zone secondary region) · Nightly logical dump | 4 |
| `gate` | Release 1 gate · Release 2 gate · Quarterly drill | 3 |

Raw product 576 · valid after constraints 456 · method **3-way** · 455 valid 3-tuples · **91 cases** (TC-V12-R-768…TC-V12-R-858) · pairwise alone would need 28

#### M10 Model registry routing: task × data class × region × candidate × registry state × availability

Capability C6 · stories US-04-ZR22, US-04-ZR23 · traces FR-V12-R-111…130; DEC-788; AIX-02/03; AU-151/152/298

| Parameter | Values | Count |
|---|---|---|
| `task` | classification · drafting · complex synthesis · embedding · safety screening | 5 |
| `data` | Public · Internal (non-personal) · Personal (masked) · Personal (unmasked) · Restricted | 5 |
| `region` | IN · EU | 2 |
| `candidate` | Claude Sonnet (approved primary) · Claude Haiku-class · Claude larger model (MDL-L1) · OpenAI GPT family · Google Gemini · Open-weight in region (Llama/Mistral/Qwen) · Free Tier 2 provider | 7 |
| `state` | approved · candidate · suspended · DPA expired · eval suite failed | 5 |
| `availability` | ok · 5xx / timeout | 2 |

Raw product 3,500 · valid after constraints 2,400 · method **3-way** · 1,304 valid 3-tuples · **197 cases** (TC-V12-R-859…TC-V12-R-1055) · pairwise alone would need 38

#### M11 Cross-tenant benchmarks: cohort size × dominance × participation × metric × scope × owner flag × budget

Capability C7 · stories US-17-ZR24, US-17-ZR25 · traces FR-V12-R-131…142; DEC-789; CONFLICT-983 resolution

| Parameter | Values | Count |
|---|---|---|
| `cohort` | 9 tenants · 10 tenants · 25 tenants | 3 |
| `dominance` | no tenant > 30% · one tenant > 30% of events | 2 |
| `participant` | opted in · not opted in · withdrawn | 3 |
| `metric` | reply rate · lead-to-meeting cycle time · win rate | 3 |
| `scope` | IN zone · EU zone · global | 3 |
| `owner` | external tenant · Owner Portfolio startup without R01 opt-in · Owner Portfolio startup with R01 opt-in | 3 |
| `budget` | ε budget available · ε budget exhausted for the period | 2 |

Raw product 972 · valid after constraints 972 · method **3-way** · 690 valid 3-tuples · **44 cases** (TC-V12-R-1056…TC-V12-R-1099) · pairwise alone would need 15

#### M12 Supabase access model: database role × context × operation × path

Capability C8 · stories US-01-ZR26, US-01-ZR27 · traces FR-V12-R-143…155; DEC-778; SB-01…SB-10

| Parameter | Values | Count |
|---|---|---|
| `role` | app_rw · app_worker · app_migrator · service_role · postgres · anon via Data API · authenticated via Data API | 7 |
| `context` | tenant and companies set · app.tenant_id not set · company not in app.company_ids | 3 |
| `op` | SELECT own rows · INSERT own row · UPDATE row of another tenant · DELETE own row | 4 |
| `path` | Django API · Celery worker · CI migration (normal) · CI migration with break-glass approval · Browser | 5 |

Raw product 420 · valid after constraints 264 · method **2-way** · 118 valid 2-tuples · **28 cases** (TC-V12-R-1100…TC-V12-R-1127)

#### M13 Registry approval: modality × evidence × approvers (exhaustive)

Capability C6 · stories US-04-ZR21 · traces FR-V12-R-111…118; DEC-788

| Parameter | Values | Count |
|---|---|---|
| `modality` | text LLM · embedding · image generation · video generation · voice (TTS/ASR) | 5 |
| `evidence` | complete · DPA no-training clause · region/processing location · EVAL suites · red-team pass · security review · cost per accepted result | 7 |
| `approvers` | two distinct approvers · one approver · same person twice | 3 |

Raw product 105 · valid after constraints 45 · method **exhaustive** · **45 cases** (TC-V12-R-1128…TC-V12-R-1172)
