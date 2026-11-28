"""Classify every RESIDUAL requirement-like unit of the L material.

Classes (Part 11.12 brief):
  a  genuinely new and still valid -> enhanced at full depth in Part 11.12 (manual decisions only)
  b  superseded by V12 (or by an approved blueprint decision) -> cite the V12 section
  c  out of scope / not a requirement -> reason (Investment product -> CONFLICT-958, DEC-002)

Order: manual decisions (L_manual.tsv, keyed by uid or regex) win; then register rules R-xx below.
Anything not matched by either is written to OUT/unclassified.jsonl and the run fails, so that
no residual statement can be left unread or unclassified.
Outputs: OUT/classified.jsonl, OUT/class_summary.tsv
"""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from L_common import *

V = {  # V12 citations
    'REC10': 'V12 BRD 25 REC-10; BRD 01 BR-C03/BR-C14; FSD 03 (separate deployments/audiences from Investment Automation)',
    'REC12': 'V12 BRD 25 REC-12 (no historical offline test or illustrative cost is production proof); FSD 34 "Historical V3 QA results - not current acceptance evidence"',
    'ARCH': 'V12 BRD 01 / FSD 01 "Historical archive SHA-256" and BRD 25 (original sources retained in the FSD embedded archive; annex non-normative, DEC-V9-02)',
    'API': 'V12 FSD 25 (REST API & Event Contract Master, V8 API convention, V12 Developer platform) + FSD App A / A2 (OpenAPI 3.1, proposed) + FSD 40 "Source disposition candidates - API" (321 rows)',
    'DB': 'V12 FSD 26 (PostgreSQL Schema Master, V8/V12) + FSD App C / C2 (DDL with RLS, proposed) + FSD 40 "Source disposition candidates - Entity" (155 rows)',
    'TEST': 'V12 FSD 33 (Unit, SIT, UAT & AI tests; V8 step-level tests, V9 E2E scenarios) + FSD 40 "Source disposition candidates - Test" (1,029 rows: pending semantic mapping, not executed)',
    'QC': 'V12 FSD 34 (QC & acceptance evidence, V9-V12 RCTCFE gates) + FSD 40 "Source disposition candidates - QC" (245 rows)',
    'TASK': 'V12 FSD 35 (Coding standards & development backlog, V10 source coding controls) + FSD 40 "Source disposition candidates - Task" (162 rows: retain predecessor/estimate, not approved); effort/budget superseded by blueprint DEC-228/DEC-230',
    'DEC': 'V12 BRD 25 "Outstanding production decisions" (180 inherited decision IDs remain source records, not approved) + FSD 40 V8/V9 decision register additions; blueprint alias SPDEC-001...180 (final/coverage/H_decision_map.csv)',
    'TRACE': 'V12 FSD 40 "V8 Master traceability register" + "V12 Enterprise requirement register" + BRD 24 (Business acceptance & traceability)',
    'PLUGIN': 'V12 FSD 28 "V9 Paid plugin replacement register" + BRD 11 "V9 Plugin and provider economics" (DEC-V9-04); blueprint Part 7.4a/b (final/coverage/F_integration_candidates.csv)',
    'OPT': 'V12 FSD 40 "V10 Original optimization control index" (OPT-01-01...OPT-20-04 -> SEC/CJ-R/MT candidates) + FSD 28/30 "V5 optimization requirements and controls"; blueprint OKPI-01...35 (Part 8.3c)',
    'UI': 'V12 FSD 24 (UI/UX master: V8 new and changed screens, website/admin logical crosswalks, 135 registered Admin screens) + FSD 20/21 + BRD 25 REC-04 (34 W + 113 A baseline)',
    'SVC': 'V12 BRD 08/09 (39 services, 156 workflows) + FSD 11/12/13 (functional spec, executable workflows, step/trigger registry) + BRD 10/11 (entitlement, pricing); detailed reconciliation in Parts 11.2-11.4 (groups B-D)',
    'STEP': 'V12 FSD 12 (Executable Workflow Specification - 156 workflows, 517 source-derived steps) + FSD 13 + FSD App B (Workflow DTO JSON schemas)',
    'PUB': 'V12 BRD 25 REC-01/05 (retire public directory and publication APIs; neutral catalogue only) + BRD 01 BR-C01',
    'CNT': 'V12 BRD 25 REC-09/11 (historical counts are candidate) + BRD 01 V10 authoritative inventory',
    'CODE': 'V12 FSD 35 "V8 Prototype code is not production code" + FSD 36 "V10 Source CI/CD stages / environment configuration controls"',
    'SRCWB': 'V12 BRD 23 (Roadmap V9/V12) supersedes the source workbook release windows; blueprint DEC-006/DEC-228 waves and Part 2.1 66-module catalogue',
}

RULES = [
    # id, predicate(u)->bool, class, reason, cite
    ('R-INV', lambda u: u['src'] in ('INV-CAT', 'WEB-INV') or 'Investment' in u['family'] or re.search(r'\bINV-(SVC|\d\d-\d\d)|INV-UX-UAT|\binv_[a-z]', u['text']),
     'c', 'Investment Automation sibling product (24 services / 96 workflows, investor/fundraising): outside the commercial product boundary; CONFLICT-958 raised against DEC-002 (Pending Founder decision)', 'REC10'),
    ('R-PUB', lambda u: 'SUPERSEDED PUBLIC ROUTE' in u['heading'] + u['text'] or re.search(r'public (startup )?directory|publication API|tenant-publication', u['text'], re.I),
     'b', 'Public directory / tenant publication route retired', 'PUB'),
    ('R-MANIFEST', lambda u: re.search(r'sha256|SHA-256|member inventory|\.zip|manifest|render_report|final_render|verification_report|delivery_validation|fresh_verification|guardrail_verification|scope_summary|package_reconciliation|document_review|document_final_assessment|Document_Review|Audit_Dashboard|01_Dashboard|review_perspectives|source_coverage|document_index|excellence_upgrade|closure_summary|optimization_validation_summary|estimate_summary|Summary\.csv|README|START_HERE|catalog_verification|historical_prior_delivery', u['file'] + ' ' + u['family'], re.I)
     or re.search(r'^(Worksheet source|Source: engineering/|Fields: )|records \| candidate/historical status retained|"(checked|document_count|documents_structurally_opened|workbook_sheets|status|passed|failed)":', u['text']),
     'c', 'Packaging, provenance, integrity or document-review metadata (file lists, hashes, counts, render/review scores, read-me navigation): not a product requirement', 'ARCH'),
    ('R-LOG', lambda u: re.search(r'(qc_gate|optimization_gate|_tests|_results|_regression|check_results|synthetic_run|closure_tests|offline_tests)\.txt', u['file']),
     'c', 'Offline/synthetic gate or test-run log output: evidence of a prior package, not a requirement', 'REC12'),
    ('R-FIXTURE', lambda u: re.search(r'postman_|operation_fixtures|synthetic_matched|benchmark_synthetic|evidence_manifest_example|ai_eval_seed|catalog_parsed_fields|catalog_field_proposals|catalog_dependency_graph', u['file'] + u['family']),
     'c', 'Synthetic fixture / review collection / generated dependency graph: test data for local review only (no live host, NOT_A_REAL_TOKEN)', 'REC12'),
    ('R-CODE', lambda u: u['kind'] == 'code' or re.search(r'\.(py|sql|js|tsx|tf|sh|yml|yaml|dot|jsonl)$|Dockerfile|requirements-reference|env\.example|environment\.example', u['family']) or re.search(r'^(const|let|function|import|def|return|if|for|assert|select|create|alter|insert|\}|\))\b', u['text'].strip()),
     'c', 'Reference / starter / prototype source code statement (non-production); rule values inside were read and are reconciled in L_manual.tsv where they carry a requirement', 'CODE'),
    ('R-STEP', lambda u: 'Proposed step execution contract' in u['heading'] or re.search(r'-FINAL\b|Internal INR / invocation', u['text']),
     'b', 'V1 proposed per-workflow step execution contract', 'STEP'),
    ('R-SVC', lambda u: '2031 commercial catalogue' in u['family'] or re.search(r'\bSM-SVC-\d\d', u['text'] + u['heading']),
     'b', '2031 commercial catalogue / 39-service SKU content (V1 rendering)', 'SVC'),
    ('R-API', lambda u: re.search(r'api_field_proposals|api_contract_review|api_catalog|api_payload_review|candidate_api|openapi|api_candidate_contracts|ui_api_table_mapping|non_screen_operation|current_api_inventory|06_APIs|reuse_impact', u['family'], re.I),
     'b', 'Historical API contract / DTO field proposal / review row', 'API'),
    ('R-DB', lambda u: re.search(r'database_|07_Database|current_database_inventory|candidate_database|database_confirmation|Logical entity inventory', u['family'], re.I),
     'b', 'Historical entity / field / constraint proposal row', 'DB'),
    ('R-TEST', lambda u: re.search(r'unit_sit_uat_test_register|operation_specific_test_variants|11_Unit_Tests|12_SIT_Tests|13_UAT_Tests|expansion_product_tests|Acceptance_Tests', u['family'], re.I)
     or re.search(r'\bSM-(UT|SIT|UAT|UX-UAT)-', u['text']) and not re.search(r'\bTASK-|QC-\d', u['text']),
     'b', 'Historical unit / SIT / UAT test case row', 'TEST'),
    ('R-QC', lambda u: re.search(r'quality_control_execution|14_Quality_Control|expansion_qc', u['family'], re.I) or re.search(r'\bQC-\d', u['text']),
     'b', 'Historical QC check row', 'QC'),
    ('R-TASK', lambda u: re.search(r'development_tasks|10_Development_Tasks|expansion_tasks|closure_effort_review|task_traceability|Task-level estimates', u['family'], re.I) or re.search(r'\bTASK-', u['text']),
     'b', 'Historical development task / estimate row', 'TASK'),
    ('R-DEC', lambda u: re.search(r'decision_queue|27_Decision_Queue|decision_resolution|expansion_decisions', u['family'], re.I) or re.search(r'\b(UX-DEC-[AW]\d|DEC-\d{3})', u['text']),
     'b', 'Historical decision-queue / review record (proposal pending owner)', 'DEC'),
    ('R-TRACE', lambda u: re.search(r'traceability|functional_requirements|business_requirements|02_Business_Requirements|03_Functional_Requirements|20_Master_Traceability|non_screen_|Interface acceptance and mapping', u['family'], re.I) or re.search(r'\bSM-(UX-)?FR-', u['text']),
     'b', 'Historical BR/FR/traceability row', 'TRACE'),
    ('R-PLUGIN', lambda u: re.search(r'paid_plugin|09_Integrations|source_plugin_register|source_budget', u['family'], re.I),
     'b', 'Historical plugin / provider replacement decision row', 'PLUGIN'),
    ('R-OPT', lambda u: re.search(r'optimization|2[1-4]_Optimization', u['family'], re.I) or re.search(r'\bOPT-\d\d-\d\d', u['text']),
     'b', 'Historical optimization control / KPI / scenario row', 'OPT'),
    ('R-UI', lambda u: re.search(r'ui_catalog|current_ui|04_Website_UI|05_Admin_UI|29_UI_Field|30_UI_Scope|147_Screen_Field|Admin\.csv|Website\.csv|New_screens|layout_catalog|route_reconciliation|ui_upgrade|Commercial prototype implementation reference', u['family'], re.I),
     'b', 'Historical screen / field / layout / route row', 'UI'),
    ('R-SRCWB', lambda u: re.search(r'complete_source_cell_inventory|source_modules|source_module_detail|source_architecture|source_strategy|source_market_playbooks', u['family']),
     'b', 'Original source workbook cell (APPNAI delivery decision centre) underlying the 38-document pack', 'SRCWB'),
    ('R-CNT', lambda u: re.search(r'(Previous|Target|Net increase): |=COUNTA|\[cached:', u['text']),
     'b', 'Historical scope-count worksheet cell', 'CNT'),
]


def load_manual():
    m = []
    p = os.path.join(os.path.dirname(__file__), 'L_manual.tsv')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            if not line.strip() or line.startswith('#'):
                continue
            key, cls, reason, cite, ref = (line.rstrip('\n').split('\t') + [''] * 5)[:5]
            m.append((key, cls, reason, cite, ref))
    return m


MAN = load_manual()


def classify(u):
    for key, cls, reason, cite, ref in MAN:
        if key == u['uid'] or (key.startswith('re:') and re.search(key[3:], u['text'])) or (key.startswith('fam:') and re.search(key[4:], u['family'])):
            return ('M:' + (ref or key[:40]), cls, reason, cite)
    for rid, pred, cls, reason, cite in RULES:
        if pred(u):
            return (rid, cls, reason, V[cite])
    return None


def main():
    out, unc = [], []
    summ = collections.Counter()
    for line in open(OUT + '/residual.jsonl'):
        u = json.loads(line)
        hit = classify(u)
        if not hit:
            unc.append(u)
            continue
        u['rule'], u['cls'], u['reason'], u['cite'] = hit
        summ[(u['rule'], u['cls'])] += 1
        out.append(u)
    with open(OUT + '/classified.jsonl', 'w') as f:
        for u in out:
            f.write(json.dumps(u, ensure_ascii=False) + '\n')
    with open(OUT + '/unclassified.jsonl', 'w') as f:
        for u in unc:
            f.write(json.dumps(u, ensure_ascii=False) + '\n')
    with open(OUT + '/class_summary.tsv', 'w') as f:
        for (r, c), n in sorted(summ.items()):
            f.write(f'{r}\t{c}\t{n}\n')
    print('classified', len(out), 'unclassified', len(unc))
    for (r, c), n in sorted(summ.items(), key=lambda x: -x[1]):
        print(r, c, n, sep='\t')
    if unc:
        sys.exit('unclassified residual units remain: read them and extend L_manual.tsv')


if __name__ == '__main__':
    main()
