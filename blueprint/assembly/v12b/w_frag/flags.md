| key | class | default | owner | approval | source | note |
|---|---|---|---|---|---|---|
| channel.email.dispatch | External channel enablement | OFF | R12 | R12 + R01 (paid) + activation matrix | BRD §10; Part 4.3 §4.36 | Global kill switch ENV-13 overrides |
| channel.whatsapp.dispatch | External channel enablement | OFF | R12 | R12 + R01 (paid) + activation matrix | BRD §10; Part 4.3 §4.36 | Global kill switch ENV-13 overrides |
| channel.sms.dispatch | External channel enablement | OFF | R12 | R12 + R01 (paid) + activation matrix | BRD §10; Part 4.3 §4.36 | Global kill switch ENV-13 overrides |
| channel.rcs.dispatch | External channel enablement | OFF | R12 | R12 + R01 (paid) + activation matrix | BRD §10; Part 4.3 §4.36 | Global kill switch ENV-13 overrides |
| channel.voice.dispatch | External channel enablement | OFF | R12 | R12 + R01 (paid) + activation matrix | BRD §10; Part 4.3 §4.36 | Global kill switch ENV-13 overrides |
| channel.linkedin.dispatch | External channel enablement | OFF | R12 | R12 + R01 (paid) + activation matrix | BRD §10; Part 4.3 §4.36 | Global kill switch ENV-13 overrides |
| channel.social.dispatch | External channel enablement | OFF | R12 | R12 + R01 (paid) + activation matrix | BRD §10; Part 4.3 §4.36 | Global kill switch ENV-13 overrides |
| channel.web_chat.dispatch | External channel enablement | OFF | R12 | R12 + R01 (paid) + activation matrix | BRD §10; Part 4.3 §4.36 | Global kill switch ENV-13 overrides |
| adapter.payment.psp | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.esign | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.calendar.google | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.calendar.m365 | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.crm.salesforce | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.crm.hubspot | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.crm.zoho | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.sms.dlt_aggregator | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.voice.cpaas | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.whatsapp.bsp | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.search.tavily | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.search.exa | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| adapter.extract.firecrawl | Paid adapter / connector | OFF | R11/R12 | Connector gate (AU-295, C2-T6) + R01 for paid | DEC-785; Part 11.19a |  |
| ai.tier2.free_fallback | AI routing | OFF | R11 | R01 + R10; registry row approved (DEC-788) | DEC-007; DEC-788 |  |
| ai.advanced_tier | AI routing | OFF | R11 | R01 + R10; registry row approved (DEC-788) | DEC-007; DEC-788 |  |
| ai.multimodal.image | AI routing | OFF | R11 | R01 + R10; registry row approved (DEC-788) | DEC-007; DEC-788 |  |
| ai.multimodal.video | AI routing | OFF | R11 | R01 + R10; registry row approved (DEC-788) | DEC-007; DEC-788 |  |
| ai.multimodal.voice | AI routing | OFF | R11 | R01 + R10; registry row approved (DEC-788) | DEC-007; DEC-788 |  |
| ai.agent.<AG-id>.enabled | Ops / kill switch | ON once launched | On-call, R11 | Change record | ADR-085 | One per AG-001…219 |
| ai.kill_switch.global | Ops / kill switch | OFF (not engaged) | On-call, R01 | Any one of R01/IC; release needs two people | Part 11.19b API-V12-R-048 |  |
| autonomy.<workflow>.L2 | Autonomy | OFF | R02 (L2) / R01 (L3, L4) | L3/L4 only under an active bounded mandate (DEC-779) | DEC-064; DEC-779 |  |
| autonomy.<workflow>.L3 | Autonomy | OFF | R02 (L2) / R01 (L3, L4) | L3/L4 only under an active bounded mandate (DEC-779) | DEC-064; DEC-779 |  |
| autonomy.<workflow>.L4 | Autonomy | OFF | R02 (L2) / R01 (L3, L4) | L3/L4 only under an active bounded mandate (DEC-779) | DEC-064; DEC-779 |  |
| capability.mandates.bounded | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-779 |  |
| capability.commerce.agentic_a2a | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-780 |  |
| capability.payments.mandated | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-780 |  |
| capability.bids.auto_submission | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-781 |  |
| capability.voice.ai_calls.outbound | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-782 |  |
| capability.voice.ai_calls.inbound | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-782 |  |
| capability.voice.recording | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-782 |  |
| capability.voice.coaching_from_recordings | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-782 |  |
| capability.investor.mode | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-783 |  |
| capability.investor.public_offer_surfaces | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-783 |  |
| capability.pricing.experiments | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-791 |  |
| capability.media.generative | Regulated capability (tenant × jurisdiction) | OFF | R01 | Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel | DEC-791 |  |
| sso.enforcement | Platform capability | OFF | R12 / platform | Tenant admin with step-up; platform prerequisites green | DEC-784 |  |
| scim.provisioning | Platform capability | OFF | R12 / platform | Tenant admin with step-up; platform prerequisites green | DEC-784 |  |
| developer.api_keys | Platform capability | OFF | R12 / platform | Tenant admin with step-up; platform prerequisites green | DEC-785 |  |
| developer.oauth_clients | Platform capability | OFF | R12 / platform | Tenant admin with step-up; platform prerequisites green | DEC-785 |  |
| developer.webhooks | Platform capability | OFF | R12 / platform | Tenant admin with step-up; platform prerequisites green | DEC-785 |  |
| developer.sandbox | Platform capability | OFF | R12 / platform | Tenant admin with step-up; platform prerequisites green | DEC-785 |  |
| benchmarks.participation | Platform capability | OFF | R12 / platform | Tenant admin with step-up; platform prerequisites green | DEC-789 |  |
| edge.personal_data_path | Platform capability | OFF | R12 / platform | Tenant admin with step-up; platform prerequisites green | DEC-786 |  |
| residency.eu_zone | Platform capability | OFF | R12 / platform | Tenant admin with step-up; platform prerequisites green | DEC-772 |  |
| sla.enterprise_tier | Platform capability | OFF | R12 / platform | Tenant admin with step-up; platform prerequisites green | DEC-774 |  |
| release.<feature> | Release | OFF in prod | Engineering | Change record; removed ≤ 90 days after rollout | Part 4.3 §4.36 |  |
| experiment.<ui_test> | Experiment | OFF | Product owner | Never eligibility, pricing or consent | Part 4.3 §4.36 |  |
