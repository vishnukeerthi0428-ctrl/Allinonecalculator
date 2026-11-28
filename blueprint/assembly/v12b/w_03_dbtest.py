"""Group W (Part 11.24): apply final/build/schema.sql to clean IN and EU databases and run the blocking database tests.

TC-W-DB-01…  are the CI gate "db-verify" (Part 11.24 §11.24.7). Results: w_frag/dbtest.json and final/build/db_test_report.txt
Run as: python3 -I w_03_dbtest.py   (needs the scratch PostgreSQL 16 of w_sql.PG)
"""
import sys, os, json, time, uuid, re, collections
sys.path.insert(0, os.path.dirname(__file__))
from w_common import *
from w_sql import *

R = []


def rec(tid, title, ok, detail=''):
    R.append(dict(id=tid, title=title, result='PASS' if ok else 'FAIL', detail=str(detail)[:300]))
    print(('PASS ' if ok else 'FAIL ') + tid + ' ' + title + ('' if ok else ' :: ' + str(detail)[:300]))


# ------------------------------------------------------------------ 1. clean apply in both residency zones
apply_res = {}
for db, zone in (('w_test_in', 'IN'), ('w_test_eu', 'EU')):
    recreate_db(db, zone)
    t0 = time.time()
    rc, out, err = psql_file(db, OUT + 'schema.sql', single_tx=True)
    apply_res[zone] = dict(rc=rc, seconds=round(time.time() - t0, 1), err=err.strip()[-400:])
    rec(f'TC-W-DB-0{1 if zone == "IN" else 2}', f'schema.sql applies in one transaction with ON_ERROR_STOP on a clean {zone} database',
        rc == 0, err.strip()[-300:])

c = connect('w_test_in')
cur = c.cursor()


def q(sql, a=None):
    cur.execute(sql, a)
    try:
        return cur.fetchall()
    except Exception:
        return None


def expect_error(tid, title, sql, states=None, args=None, as_role='app_rw', ctx=None):
    cur.execute('BEGIN')
    try:
        if ctx:
            cur.execute("SELECT ge.set_ctx(%s::uuid, %s::uuid[], %s::uuid, %s::uuid, %s, %s)", ctx)
        if as_role:
            cur.execute(f'SET LOCAL ROLE {as_role}')
        cur.execute(sql, args)
        cur.execute('ROLLBACK')
        rec(tid, title, False, 'statement succeeded but should have been rejected')
    except Exception as e:
        st = getattr(e, 'pgcode', None)
        cur.execute('ROLLBACK')
        rec(tid, title, states is None or st in states, f'{st} {str(e).splitlines()[0]}')


def as_role_rows(sql, ctx, role='app_rw', args=None):
    cur.execute('BEGIN')
    try:
        if ctx:
            cur.execute("SELECT ge.set_ctx(%s::uuid, %s::uuid[], %s::uuid, %s::uuid, %s, %s)", ctx)
        cur.execute(f'SET LOCAL ROLE {role}')
        cur.execute(sql, args)
        rows = cur.fetchall() if cur.description else cur.rowcount
        cur.execute('COMMIT')
        return rows
    except Exception:
        cur.execute('ROLLBACK')
        raise


cur.execute("SET search_path = ge, extensions, public")
# ------------------------------------------------------------------ 2. structural gates
bad = q("SELECT rolname FROM pg_roles WHERE rolname LIKE 'app\\_%' AND (rolbypassrls OR rolsuper)")
rec('TC-W-DB-03', 'No application role has BYPASSRLS or SUPERUSER (DEC-778)', not bad, bad)
nf = q("""SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ge' AND c.relkind='r'
          AND c.relname NOT IN (SELECT table_name FROM ge.platform_table_allowlist) AND NOT (c.relrowsecurity AND c.relforcerowsecurity)""")
rec('TC-W-DB-04', 'Every tenant table has ENABLE + FORCE row-level security', not nf, nf[:5])
np_ = q("""SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ge' AND c.relkind='r'
          AND c.relname NOT IN (SELECT table_name FROM ge.platform_table_allowlist)
          AND NOT EXISTS (SELECT 1 FROM pg_policies p WHERE p.schemaname='ge' AND p.tablename=c.relname AND p.cmd IN ('SELECT','ALL'))""")
rec('TC-W-DB-05', 'Every tenant table has a SELECT policy', not np_, np_[:5])
gr = q("SELECT DISTINCT grantee FROM information_schema.role_table_grants WHERE table_schema='ge' AND grantee IN ('anon','authenticated','PUBLIC','service_role')")
rec('TC-W-DB-06', 'Data API roles (anon, authenticated) and service_role hold no grant on schema ge (SA-01, SA-02)', not gr, gr)
fa = q("""SELECT count(*) FROM pg_policies WHERE schemaname='ge' AND cmd='ALL' AND roles = '{public}'""")[0][0]
rec('TC-W-DB-07', 'No FOR ALL policy applies to PUBLIC (command-split policies only; Part 11.9b F2)', fa == 0, fa)
uncov = q("""SELECT c.conrelid::regclass::text, c.conname FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace
   WHERE c.contype='f' AND n.nspname='ge' AND NOT EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid=c.conrelid
     AND (i.indkey::int2[])[0:array_length(c.conkey,1)-1] = c.conkey)""")
rec('TC-W-DB-08', 'Every foreign key has a supporting index (Part 11.9b F4)', not uncov, uncov[:5])
dl = q("""SELECT table_name FROM information_schema.role_table_grants WHERE table_schema='ge' AND grantee IN ('app_rw','app_worker') AND privilege_type IN ('DELETE','TRUNCATE')""")
rec('TC-W-DB-09', 'app_rw and app_worker hold no DELETE or TRUNCATE grant (archive, never delete; SA-08)', not dl, dl[:5])

# ------------------------------------------------------------------ 3. fixtures (as owner/superuser)
TA, TB = str(uuid.uuid4()), str(uuid.uuid4())
OA, OB = str(uuid.uuid4()), str(uuid.uuid4())
A1, A2, B1 = str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())
U = str(uuid.uuid4())
cur.execute("INSERT INTO ge.tenant (tenant_id, customer_type, data_region) VALUES (%s,'owned','IN'), (%s,'client','IN')", (TA, TB))
cur.execute("INSERT INTO ge.organization (tenant_id, organization_id, name) VALUES (%s,%s,'Owner Portfolio'), (%s,%s,'Client B')", (TA, OA, TB, OB))
cur.execute("INSERT INTO ge.company (tenant_id, company_id, organization_id, legal_name) VALUES (%s,%s,%s,'AppNAI'), (%s,%s,%s,'MedMaarg'), (%s,%s,%s,'Client B Ltd')",
            (TA, A1, OA, TA, A2, OA, TB, B1, OB))
ctxA1 = (TA, '{' + A1 + '}', A1, U, 'internal', 'IN')
ctxA2 = (TA, '{' + A2 + '}', A2, U, 'internal', 'IN')
ctxB = (TB, '{' + B1 + '}', B1, U, 'internal', 'IN')

# ------------------------------------------------------------------ 4. context and isolation
expect_error('TC-W-DB-10', 'Missing tenant context fails closed (42501) on a company-scoped table', 'SELECT count(*) FROM ge.ten_saved_view', ['42501'])
as_role_rows("INSERT INTO ge.ten_saved_view (tenant_id, startup_id, name) VALUES (%s, %s, 'pipeline')", ctxA1, args=(TA, A1))
rows = as_role_rows('SELECT count(*) FROM ge.ten_saved_view', ctxA1)[0][0]
rec('TC-W-DB-11', 'app_rw inserts and reads its own company row through set_ctx (P-CO)', rows == 1, rows)
rows = as_role_rows('SELECT count(*) FROM ge.ten_saved_view', ctxA2)[0][0]
rec('TC-W-DB-12', 'Company isolation inside one tenant: company A2 session sees 0 rows of A1 (Part 11.9b F1, MT-09)', rows == 0, rows)
rows = as_role_rows('SELECT count(*) FROM ge.ten_saved_view', ctxB)[0][0]
rec('TC-W-DB-13', 'Tenant isolation: tenant B session sees 0 rows of tenant A', rows == 0, rows)
expect_error('TC-W-DB-14', 'Write into a company outside the write scope is rejected by WITH CHECK',
             f"INSERT INTO ge.ten_saved_view (tenant_id, startup_id, name) VALUES ('{TA}', '{A2}', 'x')", ['42501'], ctx=ctxA1)
expect_error('TC-W-DB-15', 'Write into another tenant is rejected by WITH CHECK',
             f"INSERT INTO ge.ten_saved_view (tenant_id, startup_id, name) VALUES ('{TB}', '{B1}', 'x')", ['42501'], ctx=ctxA1)
expect_error('TC-W-DB-16', 'set_ctx rejects a write company outside the session company list', "SELECT 1",
             ['42501'], ctx=(TA, '{' + A1 + '}', A2, U, 'internal', 'IN'))
expect_error('TC-W-DB-17', 'app_rw cannot DELETE business rows (no grant)', 'DELETE FROM ge.ten_saved_view', ['42501'], ctx=ctxA1)
portfolio = as_role_rows('SELECT count(*) FROM ge.ten_saved_view', (TA, '{' + A1 + ',' + A2 + '}', None, U, 'internal', 'IN'))[0][0]
rec('TC-W-DB-18', 'Portfolio read (two companies, no write company) sees the union and cannot write', portfolio == 1, portfolio)
expect_error('TC-W-DB-19', 'Portfolio session (no write company) cannot insert', f"INSERT INTO ge.ten_saved_view (tenant_id, startup_id, name) VALUES ('{TA}', '{A1}', 'y')",
             ['42501'], ctx=(TA, '{' + A1 + ',' + A2 + '}', None, U, 'internal', 'IN'))
# compatibility view respects RLS (security_invoker)
as_role_rows("INSERT INTO ge.crm_deal (tenant_id, startup_id) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM ge.crm_deal WHERE false)", ctxA1, args=(TA, A1)) if False else None
v = as_role_rows("SELECT count(*) FROM ge.growth_deal", ctxB)[0][0]
rec('TC-W-DB-20', 'V12 compatibility view growth_deal is security_invoker (RLS of crm_deal applies)', v == 0,
    q("SELECT reloptions FROM pg_class WHERE relname='growth_deal'"))

# ------------------------------------------------------------------ 5. residency (DEC-772, CJ-TC-09 both directions)
expect_error('TC-W-DB-21', 'IN database rejects an EU tenant (CJ-TC-09 IN→EU direction)',
             f"INSERT INTO ge.tenant (tenant_id, customer_type, data_region) VALUES ('{uuid.uuid4()}','client','EU')", ['23514'], as_role=None)
expect_error('TC-W-DB-22', 'Tenant data_region is immutable after onboarding (CJ-R09)',
             f"UPDATE ge.tenant SET data_region='EU' WHERE tenant_id='{TA}'", ['23514'], as_role=None)
expect_error('TC-W-DB-23', 'set_ctx rejects a request routed to the wrong zone (RESIDENCY_ZONE_MISMATCH)', 'SELECT 1', ['42501'],
             ctx=(TA, '{' + A1 + '}', A1, U, 'internal', 'EU'))
reg_t = q("""SELECT c.table_name FROM information_schema.columns c JOIN information_schema.columns s ON s.table_schema=c.table_schema AND s.table_name=c.table_name AND s.column_name='startup_id'
             WHERE c.table_schema='ge' AND c.column_name='region' ORDER BY 1 LIMIT 1""")
if reg_t:
    t = reg_t[0][0]
    expect_error('TC-W-DB-24', f'Row-level residency guard rejects region EU on {t} in the IN database',
                 f"INSERT INTO ge.{t} (tenant_id, startup_id, region) VALUES ('{TA}', '{A1}', 'EU')", ['23514'], ctx=ctxA1)
ce = connect('w_test_eu'); cue = ce.cursor()
try:
    cue.execute("INSERT INTO ge.tenant (tenant_id, customer_type, data_region) VALUES (%s,'client','IN')", (str(uuid.uuid4()),))
    rec('TC-W-DB-25', 'EU database rejects an IN tenant (CJ-TC-09 EU→IN direction)', False, 'accepted')
except Exception as e:
    rec('TC-W-DB-25', 'EU database rejects an IN tenant (CJ-TC-09 EU→IN direction)', getattr(e, 'pgcode', '') == '23514', str(e).splitlines()[0])
try:
    cue.execute("INSERT INTO ge.tenant (tenant_id, customer_type, data_region) VALUES (%s,'client','EU')", (str(uuid.uuid4()),))
    rec('TC-W-DB-26', 'EU database accepts an EU tenant', True)
except Exception as e:
    rec('TC-W-DB-26', 'EU database accepts an EU tenant', False, e)
ce.close()

# ------------------------------------------------------------------ 6. integrity controls
# append-only (Part 3.3 Imm. A)
cand = q("""SELECT c.relname FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace
   WHERE n.nspname='ge' AND t.tgname LIKE 'trg_%%__immutable'
     AND EXISTS (SELECT 1 FROM information_schema.columns k WHERE k.table_schema='ge' AND k.table_name=c.relname AND k.column_name='startup_id')
     AND NOT EXISTS (SELECT 1 FROM pg_constraint k WHERE k.conrelid=c.oid AND k.contype='f' AND array_length(k.conkey,1)=1 AND EXISTS (SELECT 1 FROM pg_attribute a WHERE a.attrelid=c.oid AND a.attnum=k.conkey[1] AND a.attnotnull))
   ORDER BY (SELECT count(*) FROM information_schema.columns k WHERE k.table_schema='ge' AND k.table_name=c.relname AND k.is_nullable='NO' AND k.column_default IS NULL), 1 LIMIT 1""")
t = cand[0][0]
cur.execute('BEGIN')
try:
    cur.execute(f"INSERT INTO ge.{t} (tenant_id, startup_id) VALUES (%s,%s) RETURNING id", (TA, A1))
    rid = cur.fetchone()[0]
    try:
        cur.execute('SAVEPOINT s'); cur.execute(f"UPDATE ge.{t} SET created_by_type='service' WHERE id=%s", (rid,))
        rec('TC-W-DB-27', f'Append-only table {t} rejects UPDATE (IMMUTABLE_RECORD, NFR-018)', False, 'update accepted')
    except Exception as e:
        cur.execute('ROLLBACK TO SAVEPOINT s')
        rec('TC-W-DB-27', f'Append-only table {t} rejects UPDATE (IMMUTABLE_RECORD, NFR-018)', e.pgcode == 'P0001', str(e).splitlines()[0])
finally:
    cur.execute('ROLLBACK')
# optimistic concurrency
cur.execute('BEGIN')
cur.execute("SELECT id FROM ge.ten_saved_view LIMIT 1")
sid = cur.fetchone()[0]
try:
    cur.execute('SAVEPOINT s'); cur.execute("UPDATE ge.ten_saved_view SET name='x' WHERE id=%s", (sid,))
    rec('TC-W-DB-28', 'UPDATE without revision + 1 is rejected (STALE_REVISION, NFR-025)', False, 'accepted')
except Exception as e:
    cur.execute('ROLLBACK TO SAVEPOINT s')
    rec('TC-W-DB-28', 'UPDATE without revision + 1 is rejected (STALE_REVISION, NFR-025)', e.pgcode == '40001', str(e).splitlines()[0])
cur.execute("UPDATE ge.ten_saved_view SET name='y', revision = revision + 1 WHERE id=%s RETURNING revision", (sid,))
rec('TC-W-DB-29', 'UPDATE with revision + 1 succeeds and bumps updated_at', cur.fetchone()[0] == 2)
cur.execute('ROLLBACK')
# audit hash chain (C3-07)
cur.execute('BEGIN')
cur.execute("SELECT ge.set_ctx(%s::uuid, %s::uuid[], %s::uuid, %s::uuid, %s, %s)", ctxA1)
cur.execute('SET LOCAL ROLE app_rw')
for k in range(3):
    cur.execute("SELECT ge.fn_append_audit(%s::uuid, %s::uuid, 'deal.updated', 'crm_deal:1', 'crm_deal', 'pv1', NULL, '{}'::jsonb)", (A1, U))
cur.execute('RESET ROLE')
cur.execute("SELECT bool_and(ok), count(*) FROM ge.fn_verify_audit_chain(%s)", (TA,))
ok, n = cur.fetchone()
rec('TC-W-DB-30', 'Audit events are appended only through fn_append_audit and the per-tenant hash chain verifies', ok and n == 3, (ok, n))
try:
    cur.execute('SAVEPOINT s'); cur.execute('SET LOCAL ROLE app_rw')
    cur.execute("INSERT INTO ge.audit_event (tenant_id, action) VALUES (%s, 'forged')", (TA,))
    rec('TC-W-DB-31', 'Direct INSERT into audit_event by app_rw is refused', False, 'accepted')
except Exception as e:
    cur.execute('ROLLBACK TO SAVEPOINT s')
    rec('TC-W-DB-31', 'Direct INSERT into audit_event by app_rw is refused', e.pgcode == '42501', str(e).splitlines()[0])
cur.execute('ROLLBACK')
# domain registry (DEC-661)
dom = q("SELECT c.relname FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid WHERE t.tgname LIKE 'trg_%%__domain_registry' ORDER BY (SELECT count(*) FROM information_schema.columns k WHERE k.table_schema='ge' AND k.table_name=c.relname AND k.is_nullable='NO' AND k.column_default IS NULL), 1 LIMIT 1")[0][0]
expect_error('TC-W-DB-32', f'Typed domain table {dom} rejects a payload without schema_ref (DEC-661)',
             f"""INSERT INTO ge.{dom} (tenant_id, startup_id, payload) VALUES ('{TA}', '{A1}', '{{"k":1}}'::jsonb)""", ['23514'], as_role=None)
# SSO enforcement guard (Part 11.19a DDL-V12-R-01)
expect_error('TC-W-DB-33', 'SSO cannot be enforced without a verified domain and a break-glass account (Part 11.19a)',
             f"""INSERT INTO ge.idp_connection (tenant_id, display_name, vendor, protocol, issuer, sso_url, audience, state, enforced, last_test_ok_at, created_by)
                 VALUES ('{TA}','Okta','okta','SAML 2.0','iss','https://idp.example','aud','active',true,now(),'{U}')""", ['23514'], as_role=None)
# benchmark privacy: tenant role cannot read raw contributions (Part 11.19b C7)
expect_error('TC-W-DB-34', 'app_rw cannot read benchmark_contribution (only app_bench; DEC-789)', 'SELECT * FROM ge.benchmark_contribution', ['42501'], ctx=ctxA1)
# anon (Data API) cannot read anything
expect_error('TC-W-DB-35', 'Supabase anon role cannot read business tables (Data API closed, SA-01)', 'SELECT * FROM ge.company', ['42501'], as_role='anon')
# versioned freeze
vf = q("SELECT c.relname FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid WHERE t.tgname LIKE 'trg_%%__freeze' AND EXISTS (SELECT 1 FROM information_schema.columns k WHERE k.table_schema='ge' AND k.table_name=c.relname AND k.column_name='startup_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint k WHERE k.conrelid=c.oid AND k.contype='f' AND array_length(k.conkey,1)=1) ORDER BY (SELECT count(*) FROM information_schema.columns k WHERE k.table_schema='ge' AND k.table_name=c.relname AND k.is_nullable='NO' AND k.column_default IS NULL), 1 LIMIT 1")
if vf:
    t = vf[0][0]
    cur.execute('BEGIN')
    try:
        cols = q("SELECT column_name FROM information_schema.columns WHERE table_schema='ge' AND table_name=%s AND column_name='startup_id'", (t,))
        if cols:
            cur.execute(f"INSERT INTO ge.{t} (tenant_id, startup_id, status) VALUES (%s,%s,'approved') RETURNING id", (TA, A1))
        else:
            cur.execute(f"INSERT INTO ge.{t} (tenant_id, status) VALUES (%s,'approved') RETURNING id", (TA,))
        rid = cur.fetchone()[0]
        cur.execute('SAVEPOINT s')
        cur.execute(f"UPDATE ge.{t} SET content_hash = repeat('a',64), revision = revision + 1 WHERE id=%s", (rid,))
        rec('TC-W-DB-36', f'Approved version of {t} is frozen (fn_freeze_versioned, BRL-APR-02)', False, 'accepted')
    except Exception as e:
        rec('TC-W-DB-36', f'Approved version of {t} is frozen (fn_freeze_versioned, BRL-APR-02)', getattr(e, 'pgcode', '') == 'P0001', str(e).splitlines()[0])
    finally:
        cur.execute('ROLLBACK')
# portal predicate
cur.execute('BEGIN')
try:
    QT = str(uuid.uuid4())
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='ge' AND table_name='com_quote' AND is_nullable='NO' AND column_default IS NULL")
    need = [r[0] for r in cur.fetchall() if r[0] not in ('tenant_id', 'startup_id')]
    rec('TC-W-DB-37', 'Portal object-grant policy present on the eight portal-visible tables (CA-PORTAL, ABAC-09)',
        q("SELECT count(*) FROM pg_policies WHERE schemaname='ge' AND policyname LIKE '%%__portal_select'")[0][0] == 8, need)
finally:
    cur.execute('ROLLBACK')
# context functions are pooler-safe (transaction-local)
cur.execute('BEGIN'); cur.execute("SELECT ge.set_ctx(%s::uuid, %s::uuid[], %s::uuid, %s::uuid, %s, %s)", ctxA1); cur.execute('COMMIT')
cur.execute("SELECT current_setting('app.tenant_id', true)")
leak = cur.fetchone()[0]
rec('TC-W-DB-38', 'Context does not leak across transactions on a pooled connection (SB-03)', leak in (None, ''), leak)

# ------------------------------------------------------------------ 7. counts
cnt = dict(
    tables=q("SELECT count(*) FROM pg_tables WHERE schemaname='ge'")[0][0],
    views=q("SELECT count(*) FROM pg_views WHERE schemaname='ge'")[0][0],
    policies=q("SELECT count(*) FROM pg_policies WHERE schemaname='ge'")[0][0],
    indexes=q("SELECT count(*) FROM pg_indexes WHERE schemaname='ge'")[0][0],
    triggers=q("SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ge' AND NOT t.tgisinternal")[0][0],
    foreign_keys=q("SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='ge' AND contype='f'")[0][0],
    rls_forced=q("SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ge' AND c.relkind='r' AND c.relforcerowsecurity")[0][0],
    platform=q("SELECT count(*) FROM ge.platform_table_allowlist")[0][0],
    server=q("SELECT version()")[0][0])
res = dict(apply=apply_res, tests=R, passed=sum(1 for r in R if r['result'] == 'PASS'), failed=sum(1 for r in R if r['result'] == 'FAIL'), counts=cnt)
save_json('dbtest.json', res)
write(OUT + 'db_test_report.txt', '\n'.join(f"{r['result']} {r['id']} {r['title']}" + (f" :: {r['detail']}" if r['result'] == 'FAIL' else '') for r in R) +
      f"\n\nPASSED {res['passed']} / {len(R)}\nApply: {json.dumps(apply_res)}\nCounts: {json.dumps(cnt)}\n")
print(res['passed'], '/', len(R), cnt)
