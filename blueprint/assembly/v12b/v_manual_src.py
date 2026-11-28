"""Manual decisions for the residual triage statements, taken after reading each in context (v_out/unclassified.txt).
Keyed by representative statement; emitted by text hash so identical BRD/FSD copies share the decision.
C = covered in different words ('?phrase' = cite first blueprint line containing phrase); N = restored in Part 11.23; S = superseded (DEC)."""
import json, os, re
from v_common import OUT
D = {
'Historical annex is non-normative; unresolved decisions and semantic mappings require expl': ('C', '?non-normative', 'Part 11.12 treats the historical annex as non-normative; semantic mappings approved there'),
'C2 | Demonstration gap | All 60 seeded runs lacked recipient evidence, so no seeded run co': ('C', '?Load compliant example', 'Prototype demonstration gap; production seeds and negative cases in Part 11.10a §11.10.3.10'),
'C3 | Document contradiction | Chapter 01 called recovery objectives “proposed … pending ve': ('S', 'DEC-771; DEC-787', 'Recovery-objective approval contradiction resolved by Founder decisions RTO <= 120 min and RPO <= 15 min'),
'C5 | Evidence breadth | V10 recorded 34 targeted checks and no accessibility result. | 77/': ('C', '?77/77', 'Prototype evidence breadth; Part 11.10a §11.10.3.10 prototype verification evidence'),
'C8 | Stale label | Website browser-tab title still showed “V9”. | Corrected to V11 on both': ('N', 'FR-V12-V-001', 'Version-label defect recorded in the artifact lineage register'),
'D1 | Version labels | HTML titles and banners showed V5/V6. | All four artifacts labelled ': ('N', 'FR-V12-V-001', 'Version labels and SHA-256 of delivered HTML: artifact integrity register'),
'D2 | FSD DTO types | 290 DTO fields typed “string / configured enum”; 65 of them were real': ('C', '?DTO schema registry', 'DTO typing corrections adopted in Part 11.4b DTO registry (156 schemas)'),
'D3 | Traceability chain | Foundations and agents had no IDs in the documents. | Foundation': ('C', '?AGT-', 'Foundation register, AGT registry and 156-row traceability register in Parts 11.6a/11.11a'),
'D7 | Navigation | No Word TOC field or ID index. | TOC field (levels 1–2) and ID index app': ('C', '?id_registry', 'Blueprint ID index: final/id_registry.csv and Part 9.2 registers'),
'D10 | Separation of duties | One demo user could approve own run; approval jumped to Compl': ('C', '?requester', 'Separation of duties (requester != reviewer) and Reconciling state: BRL-APR rules, Part 11.5a run states'),
'D12 | Layered prototype code | v4/v5/v6 function layers. | Still partial by design: protot': ('N', 'FR-V12-V-006', 'Production rule "one implementation per behaviour" not stated in coding standards'),
'M1 | Two V7 lines | The responsive V7 set (6 files, 18 MOB requirements) and the functiona': ('N', 'FR-V12-V-001', 'Merge lineage of the two V7 lines into V8 recorded in the lineage register'),
'D15 | FX rate entry (new) | Rate inputs used integer stepping, so realistic rates below 1 ': ('N', 'FR-V12-V-005', 'FX rate input must accept decimals below 1; UI validation rule not specified'),
'A11Y | Colour contrast and link affordance (new) | axe-core found muted text at 4.34:1 and': ('C', '?#536676', 'Contrast tokens adopted in Part 11.7b accessibility contract'),
'EVD | Evidence and registers | No single status view of all requirements; RCTCFE stage rec': ('C', '?233', 'Requirement status register and evidence scoring: Part 11.10a scorecards'),
'Dynamic detail views | 517 source-derived step contracts; manual walkthrough and state-der': ('C', '?517', '517 step contracts: Part 11.10b/11.10c step tests'),
'ICP: industry, geography, language, business size, sales motion, target personas, volume, ': ('N', 'FR-V12-V-004', 'ICP attribute set (MT-04) only partly specified (A-07-0339 partial)'),
'Subscriber | Research → lead → qualification → engagement → opportunity → proposal → order': ('C', '?verified receipt', 'Subscriber value chain to verified receipt: Parts 1/2.2'),
'Data ownership | Tenant owns supplied business data and authorized outputs subject to agre': ('C', '?BR-V12-04', 'Data ownership: BR-V12-04 (Part 11.1a) and offboarding with legal hold (Part 11.5a/b)'),
'Operator and subscriber metrics, receivables, CRM, support, orders and invoices must be se': ('C', '?operator ledger', 'Operator ledger separate from subscriber data: Part 11.7b A187/A188 and Part 11.5a tenant lifecycle'),
'Applicable customer / sector | Digital acquisition and commerce businesses': ('C', '?Digital acquisition and commerce', 'Service sector: Part 11.2c'),
'Applicable customer / sector | Retail, wholesale, D2C, manufacturers': ('C', '?Retail, wholesale', 'Service sector: Part 11.2c'),
'Replace | Equivalent core automation can be owned by the platform. | Implement reusable na': ('C', '?Defer / exclude', 'Plugin economics classes: Part 11.8a/b plugin register'),
'Conditional external service | Proprietary data, communication, payment, verification or o': ('C', '?Defer / exclude', 'Plugin economics classes: Part 11.8a/b plugin register'),
'Defer / exclude | Not required for the product or no verified runtime requirement. | No in': ('C', '?Defer / exclude', 'Plugin economics classes: Part 11.8a/b plugin register'),
'Real support, value reports, renewal, data portability and billing disputes require approv': ('C', '?CS-14', 'Billing disputes, value reports, renewal and portability policies: OPT CS-14/CS-15, Part 11.10a/c and Part 11.5b'),
'Exit | Export permitted data in structured formats; revoke integrations and secrets; delet': ('C', '?Offboard with legal hold', 'Exit: export, revoke, delete subject to legal hold: Part 11.5a/b TC-V12-E-061'),
'BRD V12 | 8.6': ('C', '?8.6', 'V12 readiness score recorded in Part 11.10a scorecards'),
'Done | 3': ('C', '?1,029', 'Reconciliation inventory counts: Parts 11.10a/11.12'),
'API | 321': ('C', '?321', 'API disposition count 321: Part 11.12'),
'Test | 1029': ('C', '?1,029', 'Test disposition count 1,029: Part 11.10a'),
'QC | 245': ('C', '?245', 'QC disposition count 245: Part 11.12'),
'Accept only applicable scope and documented controls, then verify production security, phy': ('C', '?25+ compan', 'Production verification scope: Part 11.1b'),
'The following responsibility categories are proposed; individual assignees and dates requi': ('C', '?RACI', 'Responsibility categories: RACI in Parts 0/8.1'),
'1 Gap analysis | Six user V7 files + four Claude V7 files | Delta found: two divergent V7 ': ('N', 'FR-V12-V-001', 'RCTCFE V8 stage-gate register restored'),
'2 BRD/FSD upgrade | Responsive BRD/FSD V7 | AI, compliance, appendices, registers integrat': ('N', 'FR-V12-V-001', 'RCTCFE V8 stage-gate register restored'),
'4 Cross-artifact alignment | Six V8 artifacts | IDs, counts and SHA-256 synchronised; serv': ('N', 'FR-V12-V-001', 'RCTCFE V8 stage-gate register restored'),
'5 RCTCFE evaluation | V8 builds | 71 browser checks, axe audit, DB and contract validation': ('N', 'FR-V12-V-001', 'RCTCFE V8 stage-gate register restored'),
'7 Optimization register | 135 OPT | Status recorded for all 135 (ch34); none double-counte': ('N', 'FR-V12-V-001', 'RCTCFE V8 stage-gate register restored'),
'8 Defect resolution | D1–D15 | D14 skip link and D15 FX decimals fixed in V8; D12 partial ': ('N', 'FR-V12-V-001', 'RCTCFE V8 stage-gate register restored'),
'10 Architecture/redundancy audit | 40 MT + 18 MOB + 40 V7 | One requirement per behaviour;': ('N', 'FR-V12-V-001', 'RCTCFE V8 stage-gate register restored'),
'11 Universal implementation | Six artifacts | Synchronised V8 delivered; production gate o': ('N', 'FR-V12-V-001', 'RCTCFE V8 stage-gate register restored'),
'34 W routes / 135 Admin screens (113 A + 14 X + 8 O) | V3 prototype inventory; 113 A is hi': ('C', '?14 X', 'Route and screen counts: Part 11.7a'),
'Policy | Policy & jurisdiction engine (in-process library + cache) | Entitlement, consent,': ('C', '?fail closed', 'Policy engine in-process, fail closed: Part 11.19b / Part 3.1 PDP'),
'AI gateway | Model router + metering + screening | Routes AI-inference steps to approved m': ('C', '?egion-pinned', 'AI gateway region pinning: Parts 11.14 (DEC-772) and 11.19'),
'Modular monolith for core transaction integrity plus worker processes; extracted services ': ('C', '?modular monolith', 'Modular monolith: Part 3.1'),
'Transaction boundary: domain record + outbox in one commit; external effects cannot be ato': ('C', '?outbox', 'Transactional outbox and reconciliation: Part 3.1'),
'Authorization matrix: Anonymous: neutral catalog only; verified customer identity: own ten': ('C', '?auditor', 'Authorization matrix: roles R01–R20 and ABAC (Part 2.3), custom roles (Part 11.19a)'),
'Failed step held, compensate only newly created resources; never delete pre-existing data.': ('C', '?only resources this saga created', 'Provisioning saga compensation: Part 11.5a'),
'Only group names/counts are recoverable here; the original 100 entries and 20 named indust': ('C', '?REC-08', 'Historical use-case groups: REC-08 in Parts 11.3a/11.11a'),
'V4 adds input controls derived from required-input descriptions, sample budget, authority ': ('C', '?V4', 'Prototype workflow guard: Part 11.3a'),
'Role separation | Requester creates run; reviewer can inspect and approve eligible awaitin': ('C', '?requester', 'Role separation: BRL-APR, Part 2.3'),
'Scope | Check current company entitlement and pause. Portfolio gets aggregates only. Compa': ('C', '?aggregate', 'Portfolio aggregates only; capability checks: Part 11.5a'),
'Duplicate / failures | Explicit duplicate scenario or repeated reference+workflow+channel ': ('C', '?TC-DUP', 'Duplicate and failure holds: workflow scenario classes DUP/BUDGET/RECOVERY (Part 11.10c)'),
'The architecture separates reader steps (may see untrusted content, have no effect tools) ': ('C', '?AIX-09', 'Reader/actor separation: AIX-09 in Parts 11.10a/11.13a'),
'AIX-09 | P0 | Reader/actor separation | Steps that read untrusted content have no effect t': ('C', '?AIX-09', 'Reader/actor separation: AIX-09'),
'AIX-11 | P0 | Claims and citation control | Factual statements require evidence citations;': ('C', '?AIX-11', 'Claims and citation control: AIX-11'),
'Matching local configuration has status and illustrative cumulative cap; inherited per-com': ('C', '?MT-30', 'Scoped budgets: MT-30 in Part 11.5a'),
'All new configuration inputs are fictional and stored in browser memory only.': ('C', '?configuration_revision', 'Prototype-only browser memory; production stores configuration revisions server-side (Part 11.9a/b)'),
'Demo identity (Admin) | Separate “Demo user” selector; runs record requested_by; reviewer ': ('C', '?requester', 'Demo identity -> production SoD rule (BRL-APR)'),
'Source route / data mapping | GET /api/v1/admin/ai/runs; GET /api/v1/evidence/{id}; GET /a': ('C', '?A017', 'A017 data mapping: Part 2.7b card and Part 11.7a'),
'Purpose / access candidate | Configure campaigns, audiences and schedules; Admin': ('C', '?A058', 'A058 purpose: Part 2.5/2.7b'),
'Purpose / access candidate | Generate, edit and version B2B proposals; Admin': ('C', '?A065', 'A065 purpose: Part 2.5/2.7b'),
'API contract authority: Proposed routes below require reconciliation with inherited physic': ('C', '?avoid duplicate', 'API contract authority: Part 11.8a'),
'POST /api/v1/commercial/applications | Application DTO + revision + digest; authenticated ': ('C', '?/api/v1/commercial/applications', 'Part 11.8a'),
'GET /api/v1/commercial/applications/{id} | Verified tenant membership or operator intake s': ('C', '?/api/v1/commercial/applications', 'Part 11.8a'),
'ChannelAccount | tenant_id, company_id, account_id, channel, sender_alias, credential_ref,': ('C', '?ChannelAccount', 'Part 11.5a/11.8a'),
'opt_model_evaluation | model/prompt/version/task class; fixture_ref; quality; cost_minor; ': ('C', '?opt_model_evaluation', 'Part 11.9a'),
'opt_scoped_cache | scope/purpose/input_hash/model/prompt/policy/evidence_version; expiry; ': ('C', '?opt_scoped_cache', 'Part 11.9a'),
'growth_model_run | prompt_version_id:uuid; job_run_id:uuid; model:text; input_tokens:int; ': ('C', '?growth_model_run', 'Part 3.6a/b'),
'growth_budget | scope:text; period_start:date; limit_inr:decimal(14,2); reserved_inr:decim': ('C', '?growth_budget', 'Part 3.6a/b'),
'growth_message | thread_id:uuid; draft_id:uuid nullable; direction:text; provider_message_': ('C', '?growth_message', 'Part 3.6a/b'),
'growth_enrollment | sequence_id:uuid; contact_id:uuid; deal_id:uuid nullable; next_step_id': ('C', '?growth_enrollment', 'Part 3.6a/b'),
'sales_usage_charge | tenant_id; subscription_id; usage_id; invoice_id; charge_key; units d': ('C', '?sales_usage_charge', 'Part 3.6a/b'),
'sales_data_transfer | tenant_id; startup_id; direction; dataset; checksum; object_ref; man': ('C', '?sales_data_transfer', 'Part 3.6a/b'),
'sales_action_plan | tenant_id; startup_id; objective; autonomy; input_hash; policy_hash; a': ('C', '?sales_action_plan', 'Part 3.6a/b'),
'sales_bid | tenant_id; startup_id; opportunity_id; proposal_id; deadline; source; eligibil': ('C', '?sales_bid', 'Part 3.6a/b; automatic submission now under DEC-781'),
'sales_order_line | tenant_id; startup_id; order_id; product_id; description; quantity deci': ('C', '?sales_order_line', 'Part 3.6a/b'),
'application | application_id UUID; revision integer; administrator_email text; config JSON': ('C', '?commercial/applications', 'Application intake persistence: Part 11.8a/11.9a'),
'approval_decision | scope/run/payload_digest/policy_version; requester_id/reviewer_id; dec': ('C', '?approval_decision', 'Part 11.9a'),
'workflow_step_event | scope/run/step_id; sequence; state; artifact refs; error code; retry': ('C', '?workflow_step_event', 'Part 11.9a'),
'Executed on the delivered V11 files with Playwright + Chromium (desktop 1366 px, mobile 39': ('C', '?Playwright', 'Prototype evidence tooling: Part 11.10a'),
'Not run | Manual screen-reader study, physical-device testing, load/failover/restore drill': ('C', '?penetration test', 'Not-run production tests are scheduled in Parts 6.1/11.10'),
'Change from V8 (8.2): traceability, security and reliability specifications are more compl': ('C', '?8.2', 'Score history: Part 11.10a'),
'AIX-04 | P0 | Prompt registry | AI engineering | Specified (FSD ch16) | AIX-TC-04 | Produc': ('C', '?AIX-04', 'AIX-04 status row'),
'AIX-07 | P1 | AI grader calibration | AI evaluation | Specified (FSD ch16) | AIX-TC-07 | P': ('C', '?AIX-07', 'AIX-07 status row'),
'AIX-15 | P1 | Caching and batching | AI platform | Specified (FSD ch16) | AIX-TC-15 | Prod': ('C', '?AIX-15', 'AIX-15 status row'),
'AIX-16 | P1 | Fair scheduling | Platform / SRE | Specified (FSD ch16) | AIX-TC-16 | Produc': ('C', '?AIX-16', 'AIX-16 status row'),
'AIX-19 | P1 | Multilingual coverage | AI evaluation | Specified (FSD ch16) | AIX-TC-19 | P': ('C', '?AIX-19', 'AIX-19 status row'),
'Eight-stage wizard | PASS | Local browser fixture': ('C', '?Eight-stage wizard', 'Prototype check; production wizard Part 11.1a/11.5b'),
'V5 browser regression evidence: Chromium rendered the generated HTML through in-memory pag': ('C', '?Playwright', 'Prototype regression evidence metadata'),
'Uncertain write hold | PASS | Local fixture; not production acceptance': ('C', '?TC-RECOVERY', 'Uncertain write hold: RECOVERY class tests'),
'Portfolio operator analytics absent | PASS | Local fixture; not production acceptance': ('C', '?aggregate', 'Portfolio operator analytics absent: aggregate-only rule'),
'After incident | Root cause, fix, regression test, review control gaps and notify stakehol': ('C', '?postmortem', 'After-incident review: Parts 8.3c/11.11'),
}
def main():
    S = {x['sid']: x for x in json.load(open(os.path.join(OUT, 'statements.json')))}
    out = ['# key\tclass\treference\tnote']
    seen = set()
    for pre, (c, r, n) in D.items():
        hs = {s['h'] for s in S.values() if s['text'].startswith(pre)}
        assert hs, pre
        for h in hs:
            if h not in seen:
                seen.add(h); out.append('h:%s\t%s\t%s\t%s' % (h, c, r, n))
    # A113 template rows X26-X39: inputs/outputs present in workflow DTO registry (Part 11.4a) and screen contract (Part 11.7)
    for s in S.values():
        if 'A113' in s['sec'] and re.match(r'X(2[6-9]|3\d) \| ', s['text']) and s['h'] not in seen:
            key = s['text'].split(';')[1].split(',')[0].strip()
            seen.add(s['h'])
            out.append('h:%s\tC\t?%s\tA113 template %s: input/output refs present in Part 11.4a DTO registry; screen via A113 contract' % (s['h'], key, s['text'][:3]))
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v_manual.tsv'), 'w').write('\n'.join(out) + '\n')
    print(len(out) - 1, 'manual decisions')
if __name__ == '__main__':
    main()
