"""Group W (Part 11.24): render the generated Markdown tables used by the Part 11.24 files (w_frag/*.md)."""
import sys, os, json, csv, collections, re
sys.path.insert(0, os.path.dirname(__file__))
from w_common import *

F = {}
oa = load_json('openapi_stats.json')
ov = load_json('openapi_validation.json')
rows = load_json('openapi_rows.json')
sc = load_json('schema_stats.json')
db = load_json('dbtest.json')
cfg = load_json('config.json')
ci = load_json('ci_iac.json')
skipped = load_json('schema_skipped.json')

# ---------------------------------------------------------------- API
by_tag = collections.defaultdict(lambda: collections.Counter())
part_of_tag = {}
for r in rows:
    t = re.sub(r'\s+', ' ', r.get('tag') or '').strip()
    by_tag[t][r['method']] += 1
    by_tag[t]['_total'] += 1
    by_tag[t]['_base'] += 1 if r.get('baseline') else 0
    part_of_tag.setdefault(t, collections.Counter())[r['part']] += 1
trs = []
for k, (t, c) in enumerate(by_tag.items(), 1):
    trs.append([f'OAS-T{k:02d}', t, ', '.join(f'{p}' for p in part_of_tag[t]), c['_total'], c['_base'], c['GET'], c['POST'], c['PUT'], c['PATCH'], c['DELETE']])
tot = collections.Counter()
for r in trs:
    for i, n in enumerate(('t', 'b', 'g', 'po', 'pu', 'pa', 'd')):
        tot[n] += r[3 + i]
trs.append(['', '**Total**', '', f"**{tot['t']}**", f"**{tot['b']}**", tot['g'], tot['po'], tot['pu'], tot['pa'], tot['d']])
F['api_by_tag'] = md_table(['Tag ID', 'OpenAPI tag (domain group)', 'Source part(s)', 'Operations', 'Baseline (579)', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'], trs)

PARTS = [('3.2', 'Part 3.2 §3.2.2.4', 'API-001…555', 'Baseline catalogue'), ('3.5b', 'Part 3.5b §3.5.5.2', 'API-ENH-D-001…024', 'Baseline source-pack additions'),
         ('9.7b', 'Part 9.7b §9.7.x', 'API-ADV-X1-01…40', 'Advanced AI agents'), ('11.5b', 'Part 11.5b §11.5.5.12', 'API-V12-W-#### (no source ID)', 'V12 platform architecture'),
         ('11.8b', 'Part 11.8b §11.8.5.5', 'API-V12-H-001…076', 'V12 REST/enterprise additions'), ('11.13b', 'Part 11.13b', 'API-V12-M-01…24', 'AI improvement panel'),
         ('11.16a', 'Part 11.16a §11.16.5.11', 'API-V12-N-001…152', 'Investment Automation I'), ('11.16c', 'Part 11.16c §11.16.15.19', 'API-V12-W-#### (no source ID)', 'Investment Automation II'),
         ('11.17b', 'Part 11.17b §11.17.9.3', 'API-V12-W-#### (no source ID)', 'Mandates, agentic commerce, payments, bids'), ('11.18b', 'Part 11.18b §11.18.5.25', 'API-V12-Q-001…040', 'AI voice and recordings'),
         ('11.19a', 'Part 11.19a', 'API-V12-R-001…042', 'Identity, developer platform, connectors'), ('11.19b', 'Part 11.19b', 'API-V12-R-043…052', 'RPO, model registry, benchmarks')]
prs = []
for p, loc, ids, what in PARTS:
    prs.append([loc, ids, what, oa['by_part_rows'].get(p, 0), oa['by_part_ops'].get(p, 0), oa['by_part_rows'].get(p, 0) - oa['by_part_ops'].get(p, 0)])
prs.append(['**Total**', '', '', f"**{oa['rows_harvested']}**", f"**{oa['unique_operations']}**", f"**{oa['duplicates_merged']}**"])
F['api_by_part'] = md_table(['Source', 'Operation IDs', 'Content', 'Rows harvested (after expansion)', 'Unique operations kept', 'Merged as duplicates (x-also-defined-as)'], prs)
F['api_by_ns'] = md_table(['x-namespace', 'Operations'], sorted(([k, v] for k, v in oa['by_ns'].items()), key=lambda x: -x[1]))
fam = oa['families']
F['api_families'] = md_table(['ID family', 'Distinct source IDs'], [['API-001…555 (Part 3.2)', sum(v for k, v in fam.items() if re.match(r'API-\d$', k))]] +
                             [[k, v] for k, v in fam.items() if not re.match(r'API-\d$', k)])
lint = ov['lint']
F['api_validation'] = md_table(['Check', 'Result'], [
    ['Validator', ov['validator']], ['Validator errors', len(ov['validator_errors'])],
    ['Operations / paths', f"{lint['operations']} / {lint['paths']}"], ['Duplicate operationId', lint.get('duplicate_operationIds', 0)],
    ['Equivalent templated paths (OpenAPI 3.1 §4.8.8)', lint.get('equivalent_templated_paths', 0)],
    ['POST without Idempotency-Key, documented alternative (State/nonce, If-Match, Event ID, envelope)', lint.get('post_with_documented_idempotency_alternative', 0)],
    ['POST without Idempotency-Key and no alternative', f"{lint.get('post_without_idempotency_key', 0)} (POST /api/v2/mandates/{{id}}/simulate: read-only simulation; accepted, GAP-1206)"],
    ['PUT/PATCH/DELETE without If-Match', lint.get('write_without_if_match', 0)], ['Undeclared path parameters', lint.get('undeclared_path_param', 0)],
    ['Operations without security requirement', lint.get('no_security_declared', 0)], ['Anonymous access outside public/BFF namespaces', lint.get('anonymous_non_public', 0)],
    ['Side-effect class X without PDP (P, D or P+D)', lint.get('external_effect_without_pdp', 0)],
    ['Version prefixes', ', '.join(f'{k}: {v}' for k, v in ov['by_version_prefix'].items())],
    ['WebSocket streams kept out of OpenAPI (x-websockets)', oa['excluded']]])

# ---------------------------------------------------------------- schema
mig = sc['migrations']
desc = {'V0001': 'Extensions (schema extensions), schema ge, ten canonical roles, Data API closure, default privileges',
        'V0002': 'Context functions: app_tenant(), app_company_ids(), app_write_company(), app_actor_*(), app_zone(), set_ctx(), require_ctx(), ctx_* aliases',
        'V0003': 'FSD V12 Appendix C core (29) + C2 enterprise (19) tables; customer FOR ALL policies dropped; 89 generic growth_* tables not created (DEC-661)',
        'V0004': 'Appendix C3 (Part 11.9b): roles grants, scope integrity, 80 CHECKs, residency guard, SoD, audit hash chain, breach clocks, crypto-shredding, registry, 18 tables, verified policies and indexes',
        'V0005': 'Reconciliation patch: columns DDL-V12-R expects (tenant.kind, jurisdiction_pack.market/pack_code/counsel_signoff_ref, ai_model evidence columns), app_user',
        'V0006': 'DDL-V12-R parts 1–6 (Part 11.19a/b): identity, SCIM, roles, API keys, OAuth clients, webhooks, sandbox, connectors, CRM sync, DLT, Vercel conformance, recovery, registry, benchmarks',
        'V0007': 'Typed tables: Part 3.3 (199 entities + 13 association tables), Part 3.6 ENT-ENH-E-01…04, V12-B tables of Parts 11.16a/c, 11.17b, 11.18b',
        'V0008': 'Part 3.3 columns on the V12-realised entities; Part 3.6b ALTER deltas; DEC-661 common columns (schema_ref, evidence_refs, payload)',
        'V0008a': 'Rule-pack requirements (capability × jurisdiction × pack), tenant_activation with two-person check and DB activation gate; 32 packs seeded as Draft',
        'V0009': 'CHECK and UNIQUE constraints from the dictionaries; foreign keys (dictionary arrows, composite scope keys, Part 3.6b)',
        'V0010': 'Triggers: revision/updated_at, append-only, versioned freeze, domain registry (typed), row residency guard',
        'V0011': 'RLS ENABLE + FORCE, command-split policies (P-CO, P-CO-NULLABLE, P-TEN, P-X, portal object grants), grants per role, platform allowlist',
        'V0012': 'Indexes: FK support, Part 3.3 §3.3.8.2 key indexes, Part 3.6b IX-ENH-E, list indexes (tenant, company, state, updated_at)',
        'V0013': 'Compatibility views (security_invoker): 89 V12 logical names over typed tables; Part 3.3 names over V12 spine tables',
        'V0014': 'Seed: currencies, recovery paths per zone (P1/P2/P3), Vercel edge projects (bom1/fra1)',
        'V0015': 'CI assertions: no RLS bypass, forced RLS, SELECT policy on every tenant table, no Data API grants'}
mrows = []
for m in mig:
    k = m[1].split('__')[0]
    mrows.append([m[0], f'`{m[1]}`', desc.get(k, ''), m[2], m[3]])
mrows.append(['', '**Total**', '', f"**{sum(m[2] for m in mig)}**", f"**{sum(m[3] for m in mig)}**"])
F['migration_order'] = md_table(['#', 'Migration file (final/build/migrations/)', 'Content', 'Statements', 'CREATE TABLE'], mrows)
F['schema_counts'] = md_table(['Object', 'Count (PostgreSQL catalog after apply)'], [
    ['Tables (schema ge)', sc['tables']], ['Views (compatibility, security_invoker)', sc['views']], ['Columns', sc['columns']],
    ['Tables with ENABLE + FORCE RLS', sc['rls_forced']], ['Platform tables (no tenant column; allowlisted; grants only)', sc['platform_tables']],
    ['RLS policies', sc['policies']], ['Indexes', sc['indexes']], ['Foreign keys', sc['foreign_keys']], ['CHECK constraints', sc['checks']],
    ['Triggers (non-internal)', sc['triggers']], ['Functions in ge', sc['functions']], ['SQL statements in schema.sql', sc['statements']],
    ['Statements deferred (failed to apply)', sc['deferred']], ['Statements intentionally skipped (reasoned, listed in §11.24.4.9)', sc['skipped']]])
F['rls_templates'] = md_table(['Policy template', 'Tables'], [[k, v] for k, v in sc['templates'].items()])
F['triggers_by_kind'] = md_table(['Trigger family (generated in V0010)', 'Tables'], [[k, v] for k, v in sc['triggers_by_kind'].items()])
ti = list(csv.DictReader(open(OUT + 'table_index.csv', encoding='utf-8')))
dom = collections.Counter()
for r in ti:
    p = r['table'].split('_')[0]
    dom[p] += 1
PREF = {'ten': 'Tenancy (Part 3.3)', 'ref': 'Reference data', 'cat': 'Catalogue and knowledge', 'gov': 'Governance', 'ai': 'AI and cost', 'int': 'Integrations',
        'intel': 'Intelligence', 'crm': 'CRM', 'eng': 'Engagement', 'mkt': 'Marketing', 'com': 'Commerce', 'lcy': 'Lifecycle', 'aut': 'Automation',
        'ops': 'Platform operations', 'saas': 'SaaS lifecycle', 'ana': 'Analytics', 'inv': 'Investment Automation (11.16)', 'voice': 'Voice (11.18)',
        'coaching': 'Voice coaching (11.18)', 'mandate': 'Mandates (11.17)'}
drows = sorted(([PREF.get(k, 'V12 spine / platform: ' + k + '_*'), v] for k, v in dom.items()), key=lambda x: -x[1])
grp = collections.Counter()
for n, v in drows:
    grp['V12 spine and platform (Appendix C/C2/C3, DDL-V12-R)' if n.startswith('V12 spine') else n] += v
F['tables_by_domain'] = md_table(['Domain (table prefix)', 'Tables'], sorted(([k, v] for k, v in grp.items()), key=lambda x: -x[1]))
byorig = collections.Counter()
for r in ti:
    byorig[r['migration'].split('__')[0] + ' ' + (r['source'] or '')[:60]] += 1
F['tables_by_origin'] = md_table(['Created in / source', 'Tables'], sorted(([k, v] for k, v in byorig.items()), key=lambda x: (-x[1])))
F['db_tests'] = md_table(['Test', 'Check', 'Result'], [[t['id'], t['title'], t['result']] for t in db['tests']])
F['db_apply'] = md_table(['Zone database', 'Exit code', 'Seconds', 'Mode'], [[z, v['rc'], v['seconds'], 'psql -1 -v ON_ERROR_STOP=1 (single transaction)'] for z, v in db['apply'].items()])
F['skipped'] = md_table(['#', 'Migration', 'Reason', 'Statement / reference (truncated)'], [[k, s['mig'], s['reason'][:150], s['stmt'][:140].replace('\n', ' ')] for k, s in enumerate(skipped, 1)])

# ---------------------------------------------------------------- config
def csvrows(n):
    return list(csv.reader(open(OUT + 'config/' + n, encoding='utf-8')))
e = csvrows('env_catalogue.csv')
F['env_catalogue'] = md_table(e[0], e[1:])
fe = csvrows('frontend_env_catalogue.csv')
F['fe_catalogue'] = md_table(fe[0], fe[1:])
fl = csvrows('feature_flags.csv')
F['flags'] = md_table(fl[0], fl[1:])
rp = csvrows('rulepack_gates.csv')
F['rulepacks'] = md_table(['Pack', 'Title', 'Jurisdiction', 'Channels', 'State today', 'Source'], [[r[0], r[1][:90], r[2][:60], r[3][:50], r[4], r[7]] for r in rp[1:]])
am = csvrows('activation_matrix.csv')
caps = sorted({r[0] for r in am[1:]})
jur = ['IN', 'EU', 'UK', 'US', 'AE']
cell = {(r[0], r[1]): r[3] for r in am[1:]}
F['activation_matrix'] = md_table(['Capability flag `activation.<capability>.<J>`'] + jur,
                                  [[c] + [('—' if cell.get((c, j), '—') == '—' else cell[(c, j)].replace(';', ' + ')) for j in jur] for c in caps])

# ---------------------------------------------------------------- CI / IaC
F['ci_stats'] = md_table(['Workflow file', 'Jobs'], [[k, v] for k, v in ci['workflows'].items()] + [['**Total**', ci['jobs']]])
save_json('frag_index.json', sorted(F))
for k, v in F.items():
    write(FRAG + k + '.md', v)
print(len(F), 'fragments')
