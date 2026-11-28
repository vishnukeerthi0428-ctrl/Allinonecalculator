"""Group W (Part 11.24): build the consolidated, ordered PostgreSQL migration set and final/build/schema.sql.

Lineage (ADR-280, DEC-980/981):
  V0001-V0002  extensions, schema ge, canonical roles (DEC-778: app_rw), context functions
  V0003        V12 core and enterprise spine: FSD V12 Appendix C (29 core tables) + C2 (19 enterprise tables);
               the 89 generic growth_* tables are NOT created (DEC-661: typed blueprint tables are physical)
  V0004        DDL-V12-I "Appendix C3" (Part 11.9b): controls, 18 new tables, verified policies/indexes (growth_* removed)
  V0005        reconciliation patch for DDL-V12-R (columns the Part 11.19 DDL expects on V12 tables)
  V0006        DDL-V12-R parts 1-6 (Part 11.19a/b): identity, developer platform, connectors, Vercel data path, RPO,
               model registry, benchmarks, canonical role rename
  V0007        blueprint typed tables (Part 3.3 199 entities + 13 association tables, Part 3.6 ENT-ENH-E-01..04) and the
               V12-B tables of Parts 11.16a/c (investment), 11.17b (mandates, commerce, payments, bids), 11.18b (voice)
  V0008        blueprint columns: Part 3.3 columns on the 48 V12-realised entities, Part 3.6b ALTERs, DEC-661 common columns
  V0009        constraints (CHECK, UNIQUE) and foreign keys (blueprint arrows, composite scope keys)
  V0010        triggers (revision, append-only, versioned freeze, residency, domain registry)
  V0011        RLS policies and grants (templates P-CO, P-CO-NULLABLE, P-TEN, P-X, portal)
  V0012        indexes (FK support, Part 3.3 §3.3.8, Part 3.6b IX-ENH-E)
  V0013        compatibility views (V12 logical names over typed tables; Part 3.3 names over V12 tables)
  V0014        seed reference data;  V0015  CI assertions (no RLS bypass, forced RLS on every tenant table)
Each statement is applied to a scratch PostgreSQL 16 database; statements that fail are moved to schema_deferred.sql with
the server error, so schema.sql applies cleanly in one transaction (verified by w_03_dbtest.py).
"""
import re, sys, os, json, collections, csv
sys.path.insert(0, os.path.dirname(__file__))
from w_common import *
from w_sql import *

M = load_json('data_model.json')
T = M['tables']
I = V12 + 'i_ddl/'
DB = 'w_build'
recreate_db(DB, 'IN')
conn = connect(DB)
cur = conn.cursor()

ROLE_MAP = {'ge_owner': 'app_owner', 'ge_app': 'app_rw', 'ge_worker': 'app_worker', 'ge_readonly': 'app_readonly',
            'ge_retention': 'app_retention', 'ge_audit_writer': 'app_audit_writer', 'ge_platform_sec': 'app_platform_sec'}
MIG = collections.OrderedDict()
DEFERRED = []
LOG = collections.Counter()


def tx(sql):
    for a, b in ROLE_MAP.items():
        sql = re.sub(r'\b' + a + r'\b', b, sql)
    sql = re.sub(r'\b(IN|ON) SCHEMA public\b', r'\1 SCHEMA ge', sql)
    sql = re.sub(r'SET search_path = public, pg_temp', 'SET search_path = ge, extensions, public, pg_temp', sql)
    sql = re.sub(r'SET search_path = ge, pg_temp', 'SET search_path = ge, extensions, public, pg_temp', sql)
    return sql


SKIPPED = []   # (migration, reason, statement): statements intentionally not applied


def run(mig, stmts, note='', retry=True):
    """Apply statements one by one; keep the ones that succeed; one retry pass for ordering dependencies."""
    MIG.setdefault(mig, [])
    before = len(DEFERRED)
    _run(mig, stmts)
    if retry and len(DEFERRED) > before:
        again = [d[2] for d in DEFERRED[before:]]
        del DEFERRED[before:]
        LOG[mig + ':deferred'] -= len(again)
        _run(mig, again)


def _run(mig, stmts):
    for s in stmts:
        s = s.strip()
        if not s:
            continue
        try:
            cur.execute('SAVEPOINT w') if not conn.autocommit else None
            cur.execute(s)
            MIG[mig].append(s)
            LOG[mig + ':ok'] += 1
        except Exception as e:
            msg = str(e).split('\n')[0]
            DEFERRED.append((mig, msg, s))
            LOG[mig + ':deferred'] += 1


def q(sql, args=None):
    cur.execute(sql, args)
    return cur.fetchall()


HEADER = ["SET search_path = ge, extensions, public;",
          "SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);",
          "SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);"]

# ======================================================================= V0001 extensions, schema, roles
v1 = ["CREATE SCHEMA IF NOT EXISTS extensions;", "CREATE SCHEMA IF NOT EXISTS ge;",
      "CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA extensions;",
      "CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA extensions;",
      "CREATE EXTENSION IF NOT EXISTS btree_gin WITH SCHEMA extensions;",
      "CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA extensions;",
      "DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'vector') THEN EXECUTE 'CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA extensions'; ELSE RAISE NOTICE 'pgvector not available: halfvec columns are added by V0008 only where the extension exists (Supabase provides it; verify)'; END IF; END $$;",
      "DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'pg_stat_statements') THEN EXECUTE 'CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA extensions'; END IF; END $$;"]
roles = ['anon', 'authenticated', 'service_role', 'app_owner', 'app_migrator', 'app_rw', 'app_worker', 'app_readonly', 'app_retention',
         'app_audit_writer', 'app_platform_sec', 'app_bench', 'app_registry']
login = {'app_migrator', 'app_rw', 'app_worker', 'app_readonly', 'app_retention', 'app_platform_sec', 'app_bench', 'app_registry'}
for r in roles:
    if r in ('anon', 'authenticated', 'service_role'):
        v1.append(f"DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '{r}') THEN CREATE ROLE {r} NOLOGIN; END IF; END $$;")
    else:
        v1.append(f"DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '{r}') THEN CREATE ROLE {r} {'LOGIN' if r in login else 'NOLOGIN'} NOBYPASSRLS NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;")
v1 += ["GRANT app_owner TO app_migrator;",
       "ALTER SCHEMA ge OWNER TO app_owner;",
       "REVOKE ALL ON SCHEMA ge FROM PUBLIC;",
       "DO $$ BEGIN EXECUTE 'REVOKE ALL ON SCHEMA ge FROM anon, authenticated'; END $$;",
       "GRANT USAGE ON SCHEMA ge TO app_rw, app_worker, app_readonly, app_retention, app_audit_writer, app_platform_sec, app_bench, app_registry;",
       "GRANT USAGE ON SCHEMA extensions TO app_owner, app_rw, app_worker, app_readonly, app_retention, app_audit_writer, app_platform_sec, app_bench, app_registry;",
       "ALTER DEFAULT PRIVILEGES IN SCHEMA ge REVOKE ALL ON TABLES FROM PUBLIC;",
       "ALTER DEFAULT PRIVILEGES IN SCHEMA ge REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;",
       "DO $$ BEGIN EXECUTE format('ALTER DATABASE %I SET search_path = ge, extensions, public', current_database()); END $$;"]
v1 += [f"ALTER ROLE {r} SET search_path = ge, extensions, public;" for r in sorted(login | {'app_owner'})]
run('V0001__extensions_schema_roles', HEADER + v1)

# ======================================================================= V0002 context functions
v2 = r"""
CREATE OR REPLACE FUNCTION ge.app_tenant() RETURNS uuid LANGUAGE plpgsql STABLE AS $$
DECLARE v text := current_setting('app.tenant_id', true);
BEGIN
  IF v IS NULL OR v = '' THEN RAISE EXCEPTION 'CONTEXT_MISSING: tenant context missing' USING ERRCODE = '42501'; END IF;
  RETURN v::uuid;
END $$;
CREATE OR REPLACE FUNCTION ge.app_company_ids() RETURNS uuid[] LANGUAGE sql STABLE AS
$$ SELECT COALESCE(NULLIF(current_setting('app.company_ids', true), '')::uuid[], '{}'::uuid[]) $$;
CREATE OR REPLACE FUNCTION ge.app_write_company() RETURNS uuid LANGUAGE sql STABLE AS
$$ SELECT NULLIF(current_setting('app.write_company_id', true), '')::uuid $$;
CREATE OR REPLACE FUNCTION ge.app_actor_id() RETURNS uuid LANGUAGE sql STABLE AS
$$ SELECT NULLIF(current_setting('app.actor_id', true), '')::uuid $$;
CREATE OR REPLACE FUNCTION ge.app_actor_kind() RETURNS text LANGUAGE sql STABLE AS
$$ SELECT COALESCE(NULLIF(current_setting('app.actor_kind', true), ''), 'none') $$;
CREATE OR REPLACE FUNCTION ge.app_portfolio_id() RETURNS uuid LANGUAGE sql STABLE AS
$$ SELECT NULLIF(current_setting('app.portfolio_id', true), '')::uuid $$;
CREATE OR REPLACE FUNCTION ge.app_zone() RETURNS text LANGUAGE plpgsql STABLE AS $$
DECLARE r text := current_setting('app.deployment_region', true);
BEGIN
  IF r IS NULL OR r = '' OR r NOT IN ('IN','EU') THEN RAISE EXCEPTION 'RESIDENCY_ZONE_NOT_CONFIGURED' USING ERRCODE = '42501'; END IF;
  RETURN r;
END $$;
-- Part 11.19 names (SA-04) are aliases of the Part 11.9b helpers: one implementation, two spellings
CREATE OR REPLACE FUNCTION ge.ctx_tenant() RETURNS uuid LANGUAGE sql STABLE AS $$ SELECT ge.app_tenant() $$;
CREATE OR REPLACE FUNCTION ge.ctx_company_ids() RETURNS uuid[] LANGUAGE sql STABLE AS $$ SELECT ge.app_company_ids() $$;
CREATE OR REPLACE FUNCTION ge.require_ctx() RETURNS void LANGUAGE plpgsql STABLE AS $$
BEGIN PERFORM ge.app_tenant(); PERFORM ge.app_zone(); END $$;
-- SA-04: first statement of every request/job transaction (all settings transaction-local: pooler safe)
CREATE OR REPLACE FUNCTION ge.set_ctx(p_tenant uuid, p_companies uuid[], p_write_company uuid, p_actor uuid, p_actor_kind text, p_zone text)
RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  IF p_zone IS DISTINCT FROM ge.app_zone() THEN
    RAISE EXCEPTION 'RESIDENCY_ZONE_MISMATCH: request zone % reached % database', p_zone, ge.app_zone() USING ERRCODE = '42501'; END IF;
  IF p_actor_kind NOT IN ('internal','portal','service','ai_agent','support') THEN
    RAISE EXCEPTION 'ACTOR_KIND_INVALID: %', p_actor_kind USING ERRCODE = '22023'; END IF;
  IF p_write_company IS NOT NULL AND NOT (p_write_company = ANY (coalesce(p_companies, '{}'))) THEN
    RAISE EXCEPTION 'WRITE_COMPANY_NOT_IN_SCOPE' USING ERRCODE = '42501'; END IF;
  PERFORM set_config('app.tenant_id', p_tenant::text, true);
  PERFORM set_config('app.company_ids', coalesce(p_companies, '{}')::text, true);
  PERFORM set_config('app.write_company_id', coalesce(p_write_company::text, ''), true);
  PERFORM set_config('app.actor_id', coalesce(p_actor::text, ''), true);
  PERFORM set_config('app.actor_kind', p_actor_kind, true);
END $$;
GRANT EXECUTE ON FUNCTION ge.app_tenant(), ge.app_company_ids(), ge.app_write_company(), ge.app_actor_id(), ge.app_actor_kind(),
  ge.app_portfolio_id(), ge.app_zone(), ge.ctx_tenant(), ge.ctx_company_ids(), ge.require_ctx(),
  ge.set_ctx(uuid, uuid[], uuid, uuid, text, text) TO app_rw, app_worker, app_readonly, app_retention, app_audit_writer, app_bench, app_registry, app_platform_sec;
"""
run('V0002__context_functions', HEADER + split_sql(v2))


# ======================================================================= V0003 V12 spine (Appendix C core + C2)
def v12_filter(stmts):
    out = []
    for s in stmts:
        body = strip_leading_comments(s)
        if re.search(r'\bgrowth_[a-z_]+|\bsales_[a-z_]+', body):
            LOG['dropped_growth_stmt'] += 1
            continue
        if re.match(r'^(CREATE POLICY|ALTER TABLE \w+ ENABLE ROW LEVEL SECURITY)', body) and 'FORCE' not in body:
            pass
        if body.startswith('CREATE EXTENSION'):
            continue
        out.append(tx(body))
    return out


def split_enable_force(stmts):
    """Appendix C writes 'ALTER … ENABLE …; ALTER … FORCE …' on one line; the splitter already separates them."""
    return stmts

spine = []
for fn in ('appendix_c.sql', 'appendix_c2.sql'):
    st = split_sql(open(I + fn, encoding='utf-8').read())
    # the customer FOR ALL policies are replaced by the command-split C3 policies (F1/F2); RLS enable/force is kept
    st = [s for s in st if not strip_leading_comments(s).startswith('CREATE POLICY')]
    spine += v12_filter(st)
run('V0003__v12_core_and_enterprise_spine', HEADER + spine)

# ======================================================================= V0004 C3 (Part 11.9b)
c3 = []
for fn in ('c3_part1_manual.sql', 'c3_part2_new_tables.sql', 'c3_part3_generated.sql'):
    c3 += v12_filter(split_sql(open(I + fn, encoding='utf-8').read()))
run('V0004__ddl_v12_i_appendix_c3_controls', HEADER + c3)

# ======================================================================= V0005 reconciliation patch for DDL-V12-R
patch = """
ALTER TABLE ge.tenant ADD COLUMN IF NOT EXISTS kind text NOT NULL DEFAULT 'client';
ALTER TABLE ge.jurisdiction_pack ADD COLUMN IF NOT EXISTS market char(2);
ALTER TABLE ge.jurisdiction_pack ADD COLUMN IF NOT EXISTS counsel_signoff_ref text;
ALTER TABLE ge.ai_model ADD COLUMN IF NOT EXISTS no_training boolean NOT NULL DEFAULT false;
ALTER TABLE ge.ai_model ADD COLUMN IF NOT EXISTS eval_status text;
ALTER TABLE ge.ai_model ADD COLUMN IF NOT EXISTS security_review_ref text;
ALTER TABLE ge.ai_model ADD COLUMN IF NOT EXISTS cpar_inr numeric(12,4);
ALTER TABLE ge.ai_model ADD COLUMN IF NOT EXISTS latency_p95_ms integer;
CREATE TABLE IF NOT EXISTS ge.app_user (user_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), email extensions.citext NOT NULL UNIQUE,
  display_name text, idp_subject text UNIQUE, status text NOT NULL DEFAULT 'active' CHECK (status IN ('active','disabled')),
  created_at timestamptz NOT NULL DEFAULT now());
"""
run('V0005__reconcile_v12_lineage_for_ddl_v12_r', HEADER + split_sql(patch))

# ======================================================================= V0006 DDL-V12-R (Part 11.19a/b)
r_stmts = []
for f in part('Part-11-19a_') + part('Part-11-19b_'):
    for blk in re.findall(r'```sql\n(.*?)```', open(f, encoding='utf-8').read(), re.S):
        for s in split_sql(blk):
            s = strip_leading_comments(s)
            # Part 11.19b declares ai_model.model_id as uuid; Appendix C defines it as text (inconsistency reported, CONFLICT-1203)
            s = re.sub(r'model_id uuid NOT NULL REFERENCES ge\.ai_model', 'model_id text NOT NULL REFERENCES ge.ai_model', s)
            s = re.sub(r'rollback_to uuid REFERENCES ge\.ai_model', 'rollback_to text REFERENCES ge.ai_model', s)
            s = re.sub(r'^CREATE FUNCTION', 'CREATE OR REPLACE FUNCTION', s)
            if 'RENAME TO' in s:
                SKIPPED.append(('V0006', 'role rename not needed: roles are created with canonical names in V0001 (DEC-778, DEC-894)', s)); continue
            if 'TENANT_TABLE_WITHOUT_FORCED_RLS' in s:
                SKIPPED.append(('V0006', 'assertion moved to V0015 (runs after all tables and policies exist)', s)); continue
            if s.startswith('CREATE VIEW ge.identity_provider'):   # C2 table replaced by the compatibility view (Part 11.19a §D)
                r_stmts.append('DROP TABLE IF EXISTS ge.identity_provider CASCADE;')
            mc = re.match(r'^ALTER TABLE (ge\.\w+) ADD CONSTRAINT (\w+) ', s)
            if mc:   # a later part re-states a constraint: the later definition wins (precedence Part 11.19 > Part 11.9b)
                r_stmts.append(f'ALTER TABLE {mc.group(1)} DROP CONSTRAINT IF EXISTS {mc.group(2)};')
            r_stmts.append(tx(s))
run('V0006__ddl_v12_r_platform_decisions', HEADER + r_stmts)


# ======================================================================= introspection helpers
def existing_tables():
    return {r[0] for r in q("SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ge' AND c.relkind IN ('r','p')")}


def existing_views():
    return {r[0] for r in q("SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ge' AND c.relkind IN ('v','m')")}


def cols_of(t):
    return {r[0]: (r[1], r[2]) for r in q("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_schema='ge' AND table_name=%s", (t,))}


def pk_of(t):
    return [r[0] for r in q("""SELECT a.attname FROM pg_index i JOIN pg_class c ON c.oid=i.indrelid JOIN pg_namespace n ON n.oid=c.relnamespace
        JOIN LATERAL unnest(i.indkey) WITH ORDINALITY k(attnum, ord) ON true JOIN pg_attribute a ON a.attrelid=c.oid AND a.attnum=k.attnum
        WHERE n.nspname='ge' AND c.relname=%s AND i.indisprimary ORDER BY k.ord""", (t,))]


V12_TABLES = existing_tables()
CORE = M['v12_core_map']
# blueprint physical name -> (V12 table, id column)
REAL = {}
for v12, m in CORE.items():
    if v12 in V12_TABLES:
        pk = pk_of(v12)
        idc = [c for c in pk if c not in ('tenant_id',)]
        REAL[m['physical']] = (v12, idc[0] if len(idc) == 1 else (pk[-1] if pk else None))
REAL['ten_startup'] = ('company', 'company_id')
REAL['ten_tenant'] = ('tenant', 'tenant_id')


NATURAL = {'ref_currency': 'code', 'ref_country': 'code', 'ref_unit': 'code'}


def target(tbl):
    """Resolve a blueprint table name to (physical table, referenced key column)."""
    if tbl in REAL:
        return REAL[tbl]
    return (tbl, NATURAL.get(tbl, 'id'))


def coltype(t, c):
    r = q("SELECT format_type(a.atttypid, a.atttypmod) FROM pg_attribute a JOIN pg_class k ON k.oid=a.attrelid JOIN pg_namespace n ON n.oid=k.relnamespace WHERE n.nspname='ge' AND k.relname=%s AND a.attname=%s AND a.attnum>0", (t, c))
    return r[0][0] if r else None

# ======================================================================= V0007 typed tables
CHECK_ENUM = re.compile(r'CHECK IN \(([^)]*)\)')


def default_sql(d, typ):
    d = (d or '').strip().strip('`')
    if not d or d.lower().startswith(('app', 'session', 'next', 'computed', 'trigger', 'generated', 'from ', 'per ', 'see ')):
        return ''
    if d in ('now()', 'true', 'false', 'NULL'):
        return d
    if re.match(r"^'.*'$", d):
        if typ == 'jsonb' and not d.endswith("::jsonb"):
            return d + '::jsonb'
        if typ.endswith('[]') and d in ("'{}'",):
            return d
        return d
    if re.match(r'^-?\d+(\.\d+)?$', d):
        return d
    if d in ('{}', '[]') and typ in ('jsonb',):
        return f"'{d}'::jsonb"
    if d == '{}' and typ.endswith('[]'):
        return "'{}'"
    return ''


def col_checks(t, c):
    """Turn a dictionary 'Constraint' cell into (checks, uniques, fks)."""
    con = (c.get('constraint') or '').replace('`', '')
    n = c['name']
    checks, uniq, fks = [], [], []
    m = CHECK_ENUM.search(con)
    if m:
        vals = [v.strip() for v in m.group(1).split(',') if v.strip()]
        if vals and all(re.match(r'^[A-Za-z0-9_.+ -]+$', v) for v in vals) and not any('…' in v for v in vals):
            checks.append(f"CHECK ({n} IN ({', '.join(repr(v) for v in vals)}))".replace('"', "'"))
    elif re.search(r'CHECK\s*(≥|>=)\s*(-?\d+(\.\d+)?)', con):
        v = re.search(r'CHECK\s*(≥|>=)\s*(-?\d+(\.\d+)?)', con).group(2)
        checks.append(f'CHECK ({n} >= {v})')
    elif re.search(r'CHECK\s*>\s*(-?\d+)', con) and 'created_at' not in con:
        v = re.search(r'CHECK\s*>\s*(-?\d+)', con).group(1)
        checks.append(f'CHECK ({n} > {v})')
    elif re.search(r'CHECK\s*(-?\d+(\.\d+)?)\s*[–-]\s*(\d+(\.\d+)?)\b', con):
        mm = re.search(r'CHECK\s*(-?\d+(\.\d+)?)\s*[–-]\s*(\d+(\.\d+)?)\b', con)
        checks.append(f'CHECK ({n} BETWEEN {mm.group(1)} AND {mm.group(3)})')
    elif re.search(r'CHECK\s+hex', con):
        checks.append(f"CHECK ({n} ~ '^[0-9a-f]{{64}}$')")
    mre = re.search(r"CHECK\s+(\^[^ ;]+\$)", con)
    if mre:
        checks.append(f"CHECK ({n} ~ '{mre.group(1)}')")
    if re.search(r'(^|;\s*)UNIQUE\s*(;|$)', con.strip()):
        uniq.append(([n], ''))
    for mu in re.finditer(r'UNIQUE \(', con):
        k, depth, j = mu.end(), 1, mu.end()
        while j < len(con) and depth:
            depth += {'(': 1, ')': -1}.get(con[j], 0); j += 1
        wm = re.match(r'\s*WHERE ([^;]+)', con[j:])
        parts_ = []
        dpt, buf = 0, ''
        for ch in con[k:j - 1]:
            dpt += {'(': 1, ')': -1}.get(ch, 0)
            if ch == ',' and dpt == 0:
                parts_.append(buf.strip()); buf = ''
            else:
                buf += ch
        parts_.append(buf.strip())
        uniq.append(([x for x in parts_ if x], (wm.group(1) if wm else '').strip()))
    for mf in re.finditer(r'→\s*([a-z][a-z0-9_]+)', con):
        fks.append(mf.group(1))
    return checks, uniq, fks


typed_ddl, post_constraints, fk_list, unique_list, vector_cols = [], [], [], [], []
TYPED = {}
created_now = existing_tables()
for t, d in T.items():
    if t in REAL or t in CORE:
        continue
    scope, imm = d['scope'], d['imm']
    cols = []
    std = []
    # standard sets (Part 3.3 §3.3.6.1)
    from_std = __import__('w_02a_parse_data_parts', fromlist=['x']) if False else None
    TYPED[t] = d
for t, d in TYPED.items():
    pass

def split_top_sql(x):
    out, depth, buf = [], 0, ''
    for ch in x:
        depth += {'(': 1, ')': -1}.get(ch, 0)
        if ch == ',' and depth == 0:
            out.append(buf); buf = ''
        else:
            buf += ch
    return [b for b in out + [buf] if b.strip()]


# load std set builder from the parser module without re-running it
import importlib.util
spec_ = importlib.util.spec_from_file_location('wparse_std', os.path.join(os.path.dirname(__file__), 'w_02a_parse_data_parts.py'))
src = open(spec_.origin, encoding='utf-8').read()
std_src = src[src.index('# ------------------------------------------------------------------ standard column sets'):src.index('# ------------------------------------------------------------------ 1. catalogue')]
ns_ = {}
exec(std_src, ns_)
std_columns = ns_['std_columns']

DOMAIN_TYPED = {m['physical']: g for g, m in M['v12_domain_map'].items()}
WRITE_DOMAINS = ('intel_', 'crm_', 'eng_', 'mkt_', 'com_', 'lcy_', 'gov_', 'inv_', 'mandate', 'voice_', 'coaching_', 'payment', 'commerce', 'bid', 'kill_switch')
table_meta = {}
for t, d in TYPED.items():
    scope, imm = d['scope'] if d['scope'] in 'STXP' else 'S', d['imm'] if d['imm'] in 'MVFA' else 'M'
    sets = d.get('sets') or ''
    if d['ent'] in ('NEW',):
        sets = 'STD-S' + (' + STD-W' if imm != 'A' else '')
    if t.startswith(WRITE_DOMAINS) and scope == 'S' and 'STD-W' not in sets and imm != 'A':
        sets += ' + STD-W'
    std = std_columns(sets, scope, imm)
    spec_cols = [c for c in d['columns'] if c['name'] not in [s['name'] for s in std]]
    allc = std + spec_cols
    if d['ent'] == 'NEW' or not spec_cols:
        extra = [('state', 'text', 'N', "'draft'"), ('payload', 'jsonb', 'N', "'{}'::jsonb")]
        for n_, ty, nl, df in extra:
            if n_ not in [c['name'] for c in allc]:
                allc.append(dict(name=n_, type=ty, null=nl, default=df, constraint='', cls='Int', std=False, generic=True))
    if d['ent'] == 'NEW' and 'region' not in [c['name'] for c in allc]:
        allc.append(dict(name='region', type='text', null='N', default="ge.app_zone()", constraint="CHECK IN (IN, EU)", cls='Int'))
    if t in DOMAIN_TYPED:  # DEC-661 V12 common columns on the 89 typed domain tables
        for n_, ty, df in (('schema_ref', 'text', ''), ('evidence_refs', 'uuid[]', "'{}'"), ('payload', 'jsonb', "'{}'::jsonb")):
            if n_ not in [c['name'] for c in allc]:
                allc.append(dict(name=n_, type=ty, null='N' if df else 'Y', default=df, constraint='', cls='Int'))
    lines = []
    seen = set()
    for c in allc:
        n = c['name']
        if n in seen or not re.match(r'^[a-z_][a-z0-9_]*$', n):
            continue
        seen.add(n)
        ty = c['type']
        if ty.startswith(('halfvec', 'vector')):
            vector_cols.append((t, n, ty))
            continue
        nn = ' NOT NULL' if c.get('null', 'Y').startswith('N') else ''
        if n == 'id':
            lines.append('  id uuid NOT NULL DEFAULT gen_random_uuid()')
            continue
        df = c.get('default') if c.get('std') or c.get('generic') or c['name'] == 'region' else default_sql(c.get('default'), ty)
        if c['name'] == 'region':
            df = 'ge.app_zone()'
        if df and df not in ('',) and c.get('std') and not re.match(r"^(now\(\)|true|false|-?\d+|'.*')$", df):
            df = ''
        if nn and not df and n not in ('tenant_id', 'startup_id') and (c.get('inferred') or c.get('desc') == 'compact dictionary'):
            nn = ''
        lines.append(f'  {n} {ty}{nn}' + (f' DEFAULT {df}' if df else ''))
        ck, uq, fk = col_checks(t, c)
        if c.get('std') and c.get('constraint', '').startswith('CHECK ('):
            ck = [c['constraint']]
        if c['name'] == 'region':
            ck = ["CHECK (region IN ('IN','EU'))"]
        for k, ex in enumerate(ck):
            post_constraints.append(f'ALTER TABLE ge.{t} ADD CONSTRAINT ck_{t}__{n}{"_" + str(k) if k else ""} {ex};')
        for cols_, where in uq:
            unique_list.append((t, cols_, where, f'{t} column {n}'))
        for tg in fk:
            fk_list.append((t, [n], tg, 'dictionary arrow'))
    pk = 'id'
    lines.append(f'  CONSTRAINT pk_{t} PRIMARY KEY ({pk})')
    names = [l.strip().split()[0] for l in lines]
    if 'tenant_id' in names:
        lines.append(f'  CONSTRAINT uq_{t}__tenant_id_id UNIQUE (tenant_id, id)')
    if 'tenant_id' in names and 'startup_id' in names:
        lines.append(f'  CONSTRAINT uq_{t}__scope_id UNIQUE (tenant_id, startup_id, id)')
    if t in created_now:
        # already created by the V12 lineage (e.g. voice_number in DDL-V12-R-11): add the missing blueprint columns
        have = cols_of(t)
        for l in lines:
            nm = l.strip().split()[0]
            if nm in ('CONSTRAINT',) or nm in have:
                continue
            typed_ddl.append(f'ALTER TABLE ge.{t} ADD COLUMN IF NOT EXISTS {l.strip().replace(" NOT NULL", "")};')
        table_meta[t] = dict(scope=scope, imm=imm, merged_into_existing=True)
        continue
    typed_ddl.append(f'CREATE TABLE ge.{t} (\n' + ',\n'.join(lines) + '\n);')
    typed_ddl.append(f"COMMENT ON TABLE ge.{t} IS '{(d['ent'] + ' ' + d['entity']).replace(chr(39), '')[:120]} · scope {scope} · Imm. {imm} · {d['source']}';")
    table_meta[t] = dict(scope=scope, imm=imm)
    # association keys
    if d.get('assoc_key'):
        ks = re.findall(r'([a-z_]+_(?:id|ref|role|code))', d['assoc_key'])
        if ks:
            unique_list.append((t, ks, '', 'association key'))
    # compact-dictionary UQ statements
    for con in d.get('constraints', []):
        con = con or ''
        for mu in re.finditer(r'UQ \(', con):
            k, depth, j = mu.end(), 1, mu.end()
            while j < len(con) and depth:
                depth += {'(': 1, ')': -1}.get(con[j], 0); j += 1
            inner = con[k:j - 1]
            wm = re.match(r'\s*WHERE ([^;]+)', con[j:])
            cs = [x.strip().strip('`') for x in split_top_sql(inner)]
            unique_list.append((t, cs, (wm.group(1) if wm else '').strip().strip('`'), 'compact UQ'))
    if scope == 'S':
        fk_list.append((t, ['tenant_id', 'startup_id'], 'ten_startup', 'scope (Part 3.3 §3.3.5.3)'))
    elif scope in ('T', 'X'):
        fk_list.append((t, ['tenant_id'], 'ten_tenant', 'scope'))
        if 'startup_id' in names:
            fk_list.append((t, ['tenant_id', 'startup_id'], 'ten_startup', 'scope (MATCH SIMPLE: NULL = tenant-wide)'))
run('V0007__typed_tables_blueprint_and_v12b', HEADER + typed_ddl)

# ======================================================================= V0008 blueprint columns on V12-realised entities, 3.6b ALTERs
v8 = []
for phys, (v12, idc) in REAL.items():
    if phys not in T or v12 not in existing_tables():
        continue
    have = cols_of(v12)
    alias = {'id': idc, 'startup_id': 'company_id', 'revision': 'version'}
    for c in T[phys]['columns']:
        n = c['name']
        if n in have or alias.get(n) in have or not re.match(r'^[a-z_][a-z0-9_]*$', n):
            continue
        if c['type'].startswith(('halfvec', 'vector')):
            vector_cols.append((v12, n, c['type'])); continue
        v8.append(f'ALTER TABLE ge.{v12} ADD COLUMN IF NOT EXISTS {n} {c["type"]};')
        for tg in col_checks(phys, c)[2]:
            fk_list.append((v12, [n], tg, f'dictionary arrow ({phys})'))
for s in M['alter_sql']:
    m = re.match(r'^ALTER TABLE (\w+) ADD COLUMN (\w+) (.*?);\s*(--.*)?$', s)
    if not m:
        continue
    t, n, rest = m.group(1), m.group(2), m.group(3)
    tt, _ = target(t)
    ref = re.search(r'REFERENCES (\w+) \((\w+)\)', rest)
    rest2 = re.sub(r'\s*REFERENCES \w+ \(\w+\)', '', rest)
    uq = ' UNIQUE' in rest2
    rest2 = rest2.replace(' UNIQUE', '')
    if 'NOT NULL' in rest2 and 'DEFAULT' not in rest2:
        rest2 = rest2  # empty database: NOT NULL without default is valid
    v8.append(f'ALTER TABLE ge.{tt} ADD COLUMN IF NOT EXISTS {n} {rest2};')
    if ref:
        fk_list.append((tt, [n], ref.group(1), 'Part 3.6b'))
    if uq:
        unique_list.append((tt, [n], '', 'Part 3.6b'))
DO_VEC = []
for t, n, ty in vector_cols:
    DO_VEC.append(f"DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN EXECUTE 'ALTER TABLE ge.{t} ADD COLUMN IF NOT EXISTS {n} extensions.{ty}'; END IF; END $$;")
run('V0008__blueprint_columns_and_part_3_6_deltas', HEADER + v8 + DO_VEC)

# ======================================================================= V0009 constraints and foreign keys
ET = existing_tables()
v9 = list(post_constraints)
uniq_done = set()


def ensure_unique(t, cols):
    key = (t, tuple(cols))
    if key in uniq_done:
        return []
    uniq_done.add(key)
    have = q("""SELECT array_agg(a.attname ORDER BY k.ord) FROM pg_index i JOIN pg_class c ON c.oid=i.indrelid JOIN pg_namespace n ON n.oid=c.relnamespace
        JOIN LATERAL unnest(i.indkey) WITH ORDINALITY k(attnum, ord) ON true JOIN pg_attribute a ON a.attrelid=c.oid AND a.attnum=k.attnum
        WHERE n.nspname='ge' AND c.relname=%s AND i.indisunique AND i.indpred IS NULL GROUP BY i.indexrelid""", (t,))
    if any(sorted(h[0]) == sorted(cols) for h in have):
        return []
    return [f'ALTER TABLE ge.{t} ADD CONSTRAINT uq_{t}__{"_".join(cols)[:40]} UNIQUE ({", ".join(cols)});']

for t, cs, where, why in unique_list:
    if t not in ET:
        continue
    have = cols_of(t)
    cs2 = [c if c in have else {'startup_id': 'company_id'}.get(c, c) for c in cs]
    plain = [c for c in cs2 if re.match(r'^[a-z_][a-z0-9_]*$', c)]
    exprs = [c for c in cs2 if c not in plain]
    if any(c not in have for c in plain) or any(not all(x in have for x in re.findall(r'\b([a-z_][a-z0-9_]*)\b(?!\s*\()', e) if x not in ('tenant_id',) and not x.startswith('coalesce')) for e in exprs):
        SKIPPED.append(('V0009', 'unique key names a column the dictionary does not define (' + ', '.join(c for c in plain if c not in have) + ')', f'UNIQUE {t} ({", ".join(cs2)}) {where}'))
        continue
    nm = f'uq_{t}__{"_".join(re.sub(r"[^a-z0-9_]", "", c) for c in cs2)}'[:63]
    wh = f' WHERE {where}' if where and re.match(r'^[a-z_ ]+(IS (NOT )?NULL|= ?\'[a-z_]+\'|IN \([^)]*\))(\s+AND\s+.*)?$', where) else ''
    if where and not wh:
        LOG['unique_where_not_parsed'] += 1
    cs2 = [re.sub(r"COALESCE\((\w+)(, *zero-uuid)?\)", r"COALESCE(\1, '00000000-0000-0000-0000-000000000000'::uuid)", c) for c in cs2]
    if wh or exprs:
        v9.append(f'CREATE UNIQUE INDEX IF NOT EXISTS {nm} ON ge.{t} ({", ".join(cs2)}){wh};')
    else:
        v9 += ensure_unique(t, cs2)
DEFER_COLS = {'current_version_id', 'current_snapshot_id', 'active_revision_id', 'active_version_id', 'accepted_quote_id',
              'last_message_id', 'source_application_id', 'provisioned_tenant_id'}
fk_sql = []
fk_seen = set()
for t, cs, tg, why in fk_list:
    tt, idc = target(tg)
    if t not in ET or tt not in ET:
        LOG['fk_skipped_missing_table'] += 1
        continue
    have = cols_of(t)
    if not all(c in have for c in cs):
        cs = [{'startup_id': 'company_id'}.get(c, c) if c not in have else c for c in cs]
        if not all(c in have for c in cs):
            LOG['fk_skipped_missing_column'] += 1
            continue
    if len(cs) == 2:          # composite scope key -> (tenant_id, <company key>)
        tcols = ['tenant_id', idc if tt != 'company' else 'company_id']
    elif tt == 'tenant':
        tcols = ['tenant_id']
    else:
        tcols = [idc]
    tcols_have = cols_of(tt)
    if not all(c in tcols_have for c in tcols):
        SKIPPED.append(('V0009', f'FK target {tt} has no single key column for {tg}', f'FK {t}({", ".join(cs)}) -> {tg}')); continue
    if tg == 'ref_value':
        SKIPPED.append(('V0009', 'ref_value is keyed by (dataset_id, code): code columns are validated by fn/app against the dataset (Part 3.3 ENT-012)', f'FK {t}({", ".join(cs)}) -> ref_value')); continue
    fam = lambda x: 'str' if (x or '').split('(')[0] in ('text', 'character', 'character varying', 'citext') else (x or '').split('(')[0]
    ts_, tt_ = [coltype(t, c) for c in cs], [coltype(tt, c) for c in tcols]
    if [fam(x) for x in ts_] != [fam(x) for x in tt_]:
        SKIPPED.append(('V0009', f'type mismatch {ts_} -> {tt}{tt_}: reference kept as a soft reference (validated in the service layer)', f'FK {t}({", ".join(cs)}) -> {tt}({", ".join(tcols)})')); continue
    if len(cs) == 1 and len(pk_of(tt)) > 1 and tcols[0] in pk_of(tt) and not q("""SELECT 1 FROM pg_index i JOIN pg_class c ON c.oid=i.indrelid JOIN pg_namespace n ON n.oid=c.relnamespace
            JOIN pg_attribute a ON a.attrelid=c.oid AND a.attnum = i.indkey[0] WHERE n.nspname='ge' AND c.relname=%s AND i.indisunique AND i.indnatts=1 AND a.attname=%s""", (tt, tcols[0])) and tcols[0] in ('period', 'purpose', 'version'):
        SKIPPED.append(('V0009', f'{tt} has a composite natural key; single-column reference {tcols[0]} is not unique', f'FK {t}({", ".join(cs)}) -> {tt}')); continue
    key = (t, tuple(cs), tt)
    if key in fk_seen:
        continue
    fk_seen.add(key)
    fk_sql += ensure_unique(tt, tcols)
    nm = f'fk_{t}__{"_".join(cs)}'[:63]
    dfr = ' DEFERRABLE INITIALLY DEFERRED' if cs[-1] in DEFER_COLS else ''
    fk_sql.append(f'ALTER TABLE ge.{t} ADD CONSTRAINT {nm} FOREIGN KEY ({", ".join(cs)}) REFERENCES ge.{tt} ({", ".join(tcols)}) ON DELETE RESTRICT{dfr};')
# the C3 consent → contact FK pointed at a generic table; retarget to the typed contact table (DEC-661)
fk_sql += ensure_unique('intel_contact', ['tenant_id', 'id'])
fk_sql.append('ALTER TABLE ge.consent_record ADD CONSTRAINT consent_record_contact_fk FOREIGN KEY (tenant_id, contact_id) REFERENCES ge.intel_contact (tenant_id, id);')
run('V0009__constraints_and_foreign_keys', HEADER + v9 + fk_sql)

# ======================================================================= V0010 triggers
ET = existing_tables()
v10 = [r"""CREATE OR REPLACE FUNCTION ge.fn_touch_revision() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.revision IS DISTINCT FROM OLD.revision + 1 THEN
    RAISE EXCEPTION 'STALE_REVISION: expected revision %', OLD.revision + 1 USING ERRCODE = '40001'; END IF;
  NEW.updated_at := now();
  IF NEW.created_at IS DISTINCT FROM OLD.created_at OR NEW.id IS DISTINCT FROM OLD.id THEN
    RAISE EXCEPTION 'IMMUTABLE_RECORD: identity columns are frozen' USING ERRCODE = 'P0001'; END IF;
  RETURN NEW;
END $$;""",
       r"""CREATE OR REPLACE FUNCTION ge.fn_freeze_versioned() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE o jsonb := to_jsonb(OLD); n jsonb := to_jsonb(NEW);
BEGIN
  IF (o->>'status') IN ('approved','published','active','superseded') THEN
    IF (n - ARRAY['status','superseded_by_id','effective_to','revision','updated_at','updated_by']) IS DISTINCT FROM
       (o - ARRAY['status','superseded_by_id','effective_to','revision','updated_at','updated_by'])
       OR (n->>'status') NOT IN ('superseded','expired','retired', o->>'status') THEN
      RAISE EXCEPTION 'IMMUTABLE_RECORD: % version is frozen', o->>'status' USING ERRCODE = 'P0001'; END IF;
  END IF;
  RETURN NEW;
END $$;""",
       r"""CREATE OR REPLACE FUNCTION ge.fn_row_region_guard() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE r text := ge.app_zone(); v text := coalesce(to_jsonb(NEW)->>'region', to_jsonb(NEW)->>'zone', to_jsonb(NEW)->>'data_region');
BEGIN
  IF v IS NOT NULL AND v NOT IN ('GLOBAL') AND v <> r THEN
    RAISE EXCEPTION 'RESIDENCY_VIOLATION: row for zone % written to % database (DEC-772, CJ-TC-09)', v, r USING ERRCODE = '23514'; END IF;
  RETURN NEW;
END $$;""",
       r"""CREATE OR REPLACE FUNCTION ge.fn_validate_typed_domain_row() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE r ge.domain_schema_registry%ROWTYPE; st text := coalesce(to_jsonb(NEW)->>'status', to_jsonb(NEW)->>'state');
BEGIN
  IF NEW.schema_ref IS NULL THEN
    IF NEW.payload IS DISTINCT FROM '{}'::jsonb THEN RAISE EXCEPTION 'SCHEMA_REF_REQUIRED: payload needs schema_ref (DEC-661)' USING ERRCODE = '23514'; END IF;
    RETURN NEW; END IF;
  SELECT * INTO r FROM ge.domain_schema_registry d WHERE d.schema_ref = NEW.schema_ref AND d.table_name = TG_TABLE_NAME AND d.status = 'Approved'
   ORDER BY d.version DESC LIMIT 1;
  IF NOT FOUND THEN RAISE EXCEPTION 'unknown or unapproved schema_ref % for %', NEW.schema_ref, TG_TABLE_NAME USING ERRCODE = '23514'; END IF;
  IF st IS NOT NULL AND NOT (st = ANY (r.allowed_statuses)) THEN RAISE EXCEPTION 'status % not allowed for %', st, NEW.schema_ref USING ERRCODE = '23514'; END IF;
  IF NOT (NEW.payload ?& r.required_keys) THEN RAISE EXCEPTION 'payload missing required keys for %', NEW.schema_ref USING ERRCODE = '23514'; END IF;
  IF pg_column_size(NEW.payload) > r.max_payload_bytes THEN RAISE EXCEPTION 'payload exceeds % bytes', r.max_payload_bytes USING ERRCODE = '54000'; END IF;
  RETURN NEW;
END $$;"""]
trig = collections.Counter()
for t in sorted(ET):
    have = cols_of(t)
    meta = table_meta.get(t)
    if meta and not meta.get('merged_into_existing'):
        if 'revision' in have and 'updated_at' in have and meta['imm'] in ('M', 'F', 'V'):
            v10.append(f'CREATE TRIGGER trg_{t}__revision BEFORE UPDATE ON ge.{t} FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision();'); trig['revision'] += 1
        if meta['imm'] == 'A':
            v10.append(f'CREATE TRIGGER trg_{t}__immutable BEFORE UPDATE OR DELETE ON ge.{t} FOR EACH ROW EXECUTE FUNCTION ge.fn_forbid_mutation();'); trig['append_only'] += 1
        if meta['imm'] == 'V' and 'status' in have:
            v10.append(f'CREATE TRIGGER trg_{t}__freeze BEFORE UPDATE ON ge.{t} FOR EACH ROW EXECUTE FUNCTION ge.fn_freeze_versioned();'); trig['versioned_freeze'] += 1
        if 'schema_ref' in have and 'payload' in have and t in DOMAIN_TYPED:
            v10.append(f'CREATE TRIGGER trg_{t}__domain_registry BEFORE INSERT OR UPDATE ON ge.{t} FOR EACH ROW EXECUTE FUNCTION ge.fn_validate_typed_domain_row();'); trig['domain_registry'] += 1
    if t != 'tenant' and any(c in have for c in ('region', 'zone')) and ('tenant_id' in have):
        v10.append(f'CREATE TRIGGER trg_{t}__residency BEFORE INSERT OR UPDATE ON ge.{t} FOR EACH ROW EXECUTE FUNCTION ge.fn_row_region_guard();'); trig['residency'] += 1
run('V0010__triggers', HEADER + v10)

# ======================================================================= V0011 RLS and grants
ET = existing_tables()
pol_have = {r[0] for r in q("SELECT DISTINCT tablename FROM pg_policies WHERE schemaname='ge'")}
v11 = []
tmpl_count = collections.Counter()
platform = []
APPEND = {t for t, m in table_meta.items() if m['imm'] == 'A'} | {'audit_event', 'consent_record', 'ai_usage_event', 'eval_run', 'webhook_delivery', 'incident_notification'}
BENCH = {'benchmark_contribution', 'benchmark_privacy_ledger', 'benchmark_cell'}
REGISTRY = {'ai_model', 'ai_model_region', 'ai_model_approval', 'ai_model_pin', 'prompt_version', 'eval_suite', 'eval_run', 'permission_catalogue', 'subprocessor'}
PLATSEC = {'security_finding', 'ops_incident', 'incident_notification', 'jurisdiction_pack', 'jurisdiction_rule', 'tax_rule', 'sod_conflict'}
PORTAL_OBJ = {'com_proposal': 'proposal', 'com_quote': 'quote', 'com_contract': 'contract', 'com_invoice': 'invoice', 'com_order': 'order',
              'lcy_onboarding': 'onboarding', 'lcy_renewal': 'renewal', 'saas_service_request': 'ticket'}
for t in sorted(ET):
    have = cols_of(t)
    if t in BENCH:
        v11.append(f'GRANT SELECT, INSERT, UPDATE ON ge.{t} TO app_bench;')
        if t == 'benchmark_cell':   # Part 11.19b C7: app_rw reads published cells only
            v11 += [f'ALTER TABLE ge.{t} ENABLE ROW LEVEL SECURITY;', f'ALTER TABLE ge.{t} FORCE ROW LEVEL SECURITY;',
                    f'GRANT SELECT ON ge.{t} TO app_rw, app_readonly;',
                    f"CREATE POLICY rls_{t}__published ON ge.{t} FOR SELECT TO app_rw, app_readonly USING (state = 'published');",
                    f'CREATE POLICY rls_{t}__bench ON ge.{t} FOR ALL TO app_bench USING (true) WITH CHECK (true);']
            tmpl_count['benchmark (published-only read)'] += 1
        else:
            platform.append(t)
            tmpl_count['platform (app_bench only)'] += 1
        continue
    if 'tenant_id' not in have:
        platform.append(t)
        v11.append(f'GRANT SELECT ON ge.{t} TO app_rw, app_worker, app_readonly;')
        if t in REGISTRY:
            v11.append(f'GRANT SELECT, INSERT, UPDATE ON ge.{t} TO app_registry;')
        if t in PLATSEC:
            v11.append(f'GRANT SELECT, INSERT, UPDATE ON ge.{t} TO app_platform_sec;')
        if t in ('oauth_jti_seen', 'edge_conformance_check', 'rpo_sample', 'restore_drill', 'inbox'):
            v11.append(f'GRANT INSERT ON ge.{t} TO app_worker;')
        tmpl_count['platform (grants only)'] += 1
        continue
    comp = 'startup_id' if 'startup_id' in have else ('company_id' if 'company_id' in have else None)
    v11.append(f'ALTER TABLE ge.{t} ENABLE ROW LEVEL SECURITY;')
    v11.append(f'ALTER TABLE ge.{t} FORCE ROW LEVEL SECURITY;')
    if t in APPEND and t != 'audit_event':
        v11.append(f'GRANT SELECT, INSERT ON ge.{t} TO app_rw, app_worker;')
    elif t != 'audit_event':
        v11.append(f'GRANT SELECT, INSERT, UPDATE ON ge.{t} TO app_rw, app_worker;')
    v11.append(f'GRANT SELECT ON ge.{t} TO app_readonly;')
    v11.append(f'GRANT SELECT, DELETE ON ge.{t} TO app_retention;')
    if t in pol_have:
        tmpl_count['Part 11.9b C3 (verified, kept)'] += 1
        continue
    TEN = 'tenant_id = (SELECT ge.app_tenant())'
    if comp and have[comp][1] == 'NO':
        sel = f'{TEN} AND {comp} = ANY ((SELECT ge.app_company_ids())::uuid[])'
        wr = f'{TEN} AND {comp} = (SELECT ge.app_write_company())'
        tm = 'P-CO'
    elif comp:
        sel = f'{TEN} AND ({comp} IS NULL OR {comp} = ANY ((SELECT ge.app_company_ids())::uuid[]))'
        wr = f"{TEN} AND ({comp} = (SELECT ge.app_write_company()) OR ({comp} IS NULL AND (SELECT ge.app_actor_kind()) IN ('internal','service')))"
        tm = 'P-CO-NULLABLE'
    elif have['tenant_id'][1] == 'YES':
        sel = f'tenant_id IS NULL OR {TEN}'
        wr = TEN
        tm = 'P-X'
    else:
        sel = TEN
        wr = TEN
        tm = 'P-TEN'
    tmpl_count[tm] += 1
    v11.append(f'CREATE POLICY rls_{t}__select ON ge.{t} FOR SELECT USING ({sel});')
    v11.append(f'CREATE POLICY rls_{t}__insert ON ge.{t} FOR INSERT WITH CHECK ({wr});')
    if t not in APPEND:
        v11.append(f'CREATE POLICY rls_{t}__update ON ge.{t} FOR UPDATE USING ({wr}) WITH CHECK ({wr});')
    v11.append(f"CREATE POLICY rls_{t}__retention_delete ON ge.{t} FOR DELETE TO app_retention USING ({TEN} AND current_setting('app.retention_run_id', true) <> '');")
    if t in PORTAL_OBJ:
        v11.append(f"""CREATE POLICY rls_{t}__portal_select ON ge.{t} FOR SELECT USING ({TEN} AND (SELECT ge.app_actor_kind()) = 'portal' AND EXISTS (
  SELECT 1 FROM ge.ten_portal_grant g WHERE g.tenant_id = {t}.tenant_id AND g.object_type = '{PORTAL_OBJ[t]}' AND g.object_id = {t}.id
  AND g.subject_user_id = (SELECT ge.app_actor_id()) AND g.revoked_at IS NULL AND (g.expires_at IS NULL OR g.expires_at > now())));""")
        tmpl_count['portal object-grant predicate (additional)'] += 1
v11.append('CREATE TABLE IF NOT EXISTS ge.platform_table_allowlist (table_name text PRIMARY KEY, reason text NOT NULL);')
for t in platform:
    v11.append(f"INSERT INTO ge.platform_table_allowlist VALUES ('{t}', 'no tenant column: platform metadata, reference data or zone evidence; writes only by app_owner migrations or a named service role') ON CONFLICT DO NOTHING;")
v11.append("GRANT SELECT ON ge.platform_table_allowlist TO app_readonly;")
v11.append("GRANT EXECUTE ON FUNCTION ge.fn_append_audit(uuid,uuid,text,text,text,text,uuid,jsonb) TO app_rw, app_worker;")
run('V0011__rls_policies_and_grants', HEADER + v11)

# ======================================================================= V0012 indexes
ET = existing_tables()
v12 = []
fkrows = q("""SELECT c.conrelid::regclass::text, array_agg(a.attname ORDER BY k.ord)
   FROM pg_constraint c JOIN pg_namespace n ON n.oid = c.connamespace
   JOIN LATERAL unnest(c.conkey) WITH ORDINALITY k(attnum, ord) ON true JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = k.attnum
   WHERE c.contype = 'f' AND n.nspname = 'ge' GROUP BY c.oid, c.conrelid""")
idxrows = q("""SELECT i.indrelid::regclass::text, array_agg(a.attname ORDER BY k.ord) FROM pg_index i
   JOIN LATERAL unnest(i.indkey) WITH ORDINALITY k(attnum, ord) ON true JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = k.attnum
   JOIN pg_class c ON c.oid = i.indrelid JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'ge' GROUP BY i.indexrelid, i.indrelid""")
idx = collections.defaultdict(list)
for t, cols_ in idxrows:
    idx[t.replace('ge.', '')].append(cols_)
fk_support = 0
done = set()
for t, cols_ in fkrows:
    t = t.replace('ge.', '')
    if any(ix[:len(cols_)] == cols_ for ix in idx[t]) or (t, tuple(cols_)) in done:
        continue
    done.add((t, tuple(cols_)))
    v12.append(f'CREATE INDEX IF NOT EXISTS ix_{t}__{"_".join(cols_)}'[:63 + 27] .replace(f'ix_{t}__{"_".join(cols_)}', f'ix_{t}__{"_".join(cols_)}'[:63]) + f' ON ge.{t} ({", ".join(cols_)});')
    fk_support += 1
def remap_cols(expr, src, tt):
    if src == tt:
        return expr
    have = cols_of(tt)
    idc = REAL.get(src, (tt, 'id'))[1]
    for a, b in (('startup_id', 'company_id'), ('id', idc), ('state', 'status'), ('created_at', 'run_at')):
        if a not in have and b in have:
            expr = re.sub(r'\b' + a + r'\b', b, expr)
    return expr


for k in M['key_indexes']:
    tt, _ = target(k['table'])
    if tt not in ET:
        continue
    dfn = remap_cols(k['definition'].replace('BRIN ', ''), k['table'], tt)
    using = ' USING brin' if k['definition'].startswith('BRIN') else ''
    m = re.match(r'^\((.*)\)\s*(WHERE (.*))?$', dfn.strip())
    if not m:
        continue
    v12.append(f'CREATE INDEX IF NOT EXISTS {k["name"][:63]} ON ge.{tt}{using} ({m.group(1)})' + (f' WHERE {m.group(3)}' if m.group(3) else '') + ';')
for s in M['index_sql']:
    s2 = s.replace(' CONCURRENTLY', '').split('--')[0].strip()
    m = re.match(r'^(CREATE (?:UNIQUE )?INDEX) (\w+) ON (\w+) (.*)$', s2)
    if not m:
        continue
    tt, _ = target(m.group(3))
    body_ = remap_cols(m.group(4), m.group(3), tt)
    hv = cols_of(tt)
    miss = [w for w in re.findall(r'\b([a-z_][a-z0-9_]*)\b', re.sub(r"'[^']*'", '', body_)) if w not in hv and w not in ('coalesce', 'lower', 'uuid', 'desc', 'asc', 'using', 'gin', 'btree', 'brin', 'gist', 'jsonb_path_ops', 'gin_trgm_ops', 'where', 'and', 'or', 'not', 'null', 'is', 'in', 'text')]
    if miss:
        SKIPPED.append(('V0012', f'index names columns not defined on {tt}: {", ".join(miss)}', s2)); continue
    v12.append(f'{m.group(1)} IF NOT EXISTS {m.group(2)} ON ge.{tt} {body_}')
# generic list index for tenant tables with state/status and updated_at (Part 3.3 §3.3.8.1 "every list filter has an index")
for t in sorted(ET):
    have = cols_of(t)
    sc = 'startup_id' if 'startup_id' in have else ('company_id' if 'company_id' in have else None)
    st = 'state' if 'state' in have else ('status' if 'status' in have else None)
    if 'tenant_id' in have and sc and st and 'updated_at' in have:
        v12.append(f'CREATE INDEX IF NOT EXISTS {("ix_" + t + "__list")[:63]} ON ge.{t} (tenant_id, {sc}, {st}, updated_at DESC);')
run('V0012__indexes', HEADER + v12)

# ======================================================================= V0013 compatibility views
ET = existing_tables()
EV = existing_views()
v13 = []
for g, m in M['v12_domain_map'].items():
    p = m['physical']
    if p not in ET or g in ET or g in EV:
        continue
    have = cols_of(p)
    st = 'state' if 'state' in have else ('status' if 'status' in have else "NULL::text")
    f_ = lambda c, alt: c if c in have else alt
    sc_ = 'startup_id' if 'startup_id' in have else ('company_id' if 'company_id' in have else 'NULL::uuid')
    idc_ = 'id' if 'id' in have else (REAL.get(p, (p, None))[1] or 'NULL::uuid')
    v13.append(f"""CREATE VIEW ge.{g} WITH (security_invoker = true) AS
  SELECT tenant_id, {sc_} AS company_id, {idc_} AS id, {f_('schema_ref', 'NULL::text')} AS schema_ref, {f_('revision', '1')} AS version, {st} AS status,
         {f_('payload', "'{}'::jsonb")} AS payload, {f_('evidence_refs', "'{}'::uuid[]")} AS evidence_refs, {f_('created_by', 'NULL::uuid')} AS created_by,
         {f_('created_at', 'NULL::timestamptz')} AS created_at, {f_('updated_at', f_('created_at', 'NULL::timestamptz'))} AS updated_at FROM ge.{p};""")
    v13.append(f'GRANT SELECT ON ge.{g} TO app_rw, app_worker, app_readonly;')
for phys, (v12t, idc) in REAL.items():
    if phys in ET or phys in EV or v12t not in ET or phys == v12t:
        continue
    have = cols_of(v12t)
    extra = []
    if 'id' not in have and idc:
        extra.append(f'{idc} AS id')
    if 'company_id' in have and 'startup_id' not in have:
        extra.append('company_id AS startup_id')
    v13.append(f'CREATE VIEW ge.{phys} WITH (security_invoker = true) AS SELECT {v12t}.*' + (', ' + ', '.join(extra) if extra else '') + f' FROM ge.{v12t};')
    v13.append(f'GRANT SELECT ON ge.{phys} TO app_rw, app_worker, app_readonly;')
run('V0013__compatibility_views', HEADER + v13)

# ======================================================================= V0014 seed reference data
seed = []
ET = existing_tables()
if 'ref_currency' in ET:
    hc = cols_of('ref_currency')
    for code, name, mu in (('INR', 'Indian rupee', 2), ('EUR', 'Euro', 2), ('USD', 'US dollar', 2), ('GBP', 'Pound sterling', 2), ('AED', 'UAE dirham', 2), ('SGD', 'Singapore dollar', 2)):
        cols_ = ['code'] + (['name'] if 'name' in hc else []) + (['minor_units'] if 'minor_units' in hc else []) + (['is_active'] if 'is_active' in hc else [])
        vals = [f"'{code}'"] + ([f"'{name}'"] if 'name' in hc else []) + ([str(mu)] if 'minor_units' in hc else []) + (['true'] if 'is_active' in hc else [])
        seed.append(f'INSERT INTO ge.ref_currency ({", ".join(cols_)}) VALUES ({", ".join(vals)});')
for zone, path, days, loc in (('IN', 'P1_supabase_pitr', 35, 'Supabase PITR (Mumbai)'), ('IN', 'P2_walg_standby', 35, 'S3 ap-south-1 WAL-G'), ('IN', 'P3_logical_dump', 35, 'S3 ap-south-1 nightly dump'),
                              ('EU', 'P1_supabase_pitr', 35, 'Supabase PITR (Frankfurt)'), ('EU', 'P2_walg_standby', 35, 'S3 eu-central-1 WAL-G'), ('EU', 'P3_logical_dump', 35, 'S3 eu-central-1 nightly dump')):
    seed.append(f"INSERT INTO ge.recovery_path (zone, path, retention_days, location, enabled) VALUES ('{zone}', '{path}', {days}, '{loc}', true) ON CONFLICT DO NOTHING;")
for p_, z, regs, pd in (('web-in', 'IN', "ARRAY['bom1']", 'true'), ('admin-in', 'IN', "ARRAY['bom1']", 'true'), ('web-eu', 'EU', "ARRAY['fra1']", 'true'), ('admin-eu', 'EU', "ARRAY['fra1']", 'true'), ('developers', None, "ARRAY['bom1','fra1']", 'false')):
    seed.append(f"INSERT INTO ge.edge_project (project, zone, function_regions, carries_personal_data) VALUES ('{p_}', {('NULL' if z is None else repr(z))}, {regs}, {pd}) ON CONFLICT DO NOTHING;")
run('V0014__seed_reference_data', HEADER + seed)

# ======================================================================= V0015 CI assertions (DDL-V12-R-16 + Part 11.24)
v15 = [r"""DO $$ BEGIN
  IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname IN ('app_rw','app_worker','app_readonly','app_retention','app_bench','app_registry','app_migrator','app_platform_sec') AND (rolbypassrls OR rolsuper)) THEN
    RAISE EXCEPTION 'APP_ROLE_CAN_BYPASS_RLS'; END IF;
  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE n.nspname = 'ge' AND c.relkind IN ('r','p') AND c.relname NOT IN (SELECT table_name FROM ge.platform_table_allowlist)
               AND NOT (c.relrowsecurity AND c.relforcerowsecurity)) THEN
    RAISE EXCEPTION 'TENANT_TABLE_WITHOUT_FORCED_RLS'; END IF;
  IF EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE n.nspname = 'ge' AND c.relkind IN ('r','p') AND c.relname NOT IN (SELECT table_name FROM ge.platform_table_allowlist)
               AND NOT EXISTS (SELECT 1 FROM pg_policies p WHERE p.schemaname = 'ge' AND p.tablename = c.relname AND p.cmd IN ('SELECT','ALL'))) THEN
    RAISE EXCEPTION 'TENANT_TABLE_WITHOUT_SELECT_POLICY'; END IF;
  IF EXISTS (SELECT 1 FROM information_schema.role_table_grants WHERE table_schema = 'ge' AND grantee IN ('anon','authenticated','PUBLIC')) THEN
    RAISE EXCEPTION 'DATA_API_ROLE_HAS_GRANT'; END IF;
END $$;"""]
run('V0015__ci_assertions', HEADER + v15)

# ======================================================================= write files
MD = OUT + 'migrations/'
os.makedirs(MD, exist_ok=True)
for f in os.listdir(MD):
    os.remove(MD + f)
allsql = ['-- AI Growth Engine: consolidated schema (Part 11.24, generated by assembly/v12b/w_02b_build_schema.py)',
          '-- Apply to an EMPTY regional database after: ALTER DATABASE <db> SET app.deployment_region = \'IN\' (or \'EU\').',
          '-- Production: migrations are applied by role app_migrator (SET ROLE app_owner) through the CI pipeline; never service_role (DEC-778).',
          '-- Indexes are created inline because the database is empty; on populated databases use CREATE INDEX CONCURRENTLY (Part 3.3 §3.3.5.11).', '']
order = []
for k, (mig, stmts) in enumerate(MIG.items(), 1):
    body = '\n\n'.join(stmts) + '\n'
    write(MD + mig + '.sql', f'-- {mig}\n' + body)
    allsql.append(f'-- ===================================================================== {mig}\n' + body)
    order.append([k, mig + '.sql', len(stmts), sum(1 for s in stmts if s.startswith('CREATE TABLE')), LOG[mig + ':deferred']])
write(OUT + 'schema.sql', '\n'.join(allsql))
with open(OUT + 'migration_order.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['order', 'file', 'statements', 'create_table', 'deferred_statements']); w.writerows(order)
write(OUT + 'schema_deferred.sql', '-- Statements from the source parts that did not apply on the consolidated schema; each needs a decision (see Part 11.24 §11.24.4.9)\n\n' +
      '\n\n'.join(f'-- [{m}] ERROR: {e}\n-- ' + s.replace('\n', '\n-- ') for m, e, s in DEFERRED))

# table index
ET = sorted(existing_tables())
EV = sorted(existing_views())
pol = collections.Counter(r[0] for r in q("SELECT tablename FROM pg_policies WHERE schemaname='ge'"))
rls = {r[0]: (r[1], r[2]) for r in q("SELECT c.relname, c.relrowsecurity, c.relforcerowsecurity FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ge' AND c.relkind='r'")}
ncols = {r[0]: r[1] for r in q("SELECT table_name, count(*) FROM information_schema.columns WHERE table_schema='ge' GROUP BY 1")}
origin = {}
for mig, stmts in MIG.items():
    for s in stmts:
        m = re.match(r'^CREATE TABLE (?:IF NOT EXISTS )?(?:ge\.)?(\w+)', s)
        if m:
            origin.setdefault(m.group(1), mig)
with open(OUT + 'table_index.csv', 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['table', 'migration', 'source', 'ent', 'scope', 'imm', 'columns', 'rls_forced', 'policies', 'blueprint_alias_view'])
    alias = {v[0]: k for k, v in REAL.items()}
    for t in ET:
        d = T.get(t, {})
        src = d.get('source') or ('FSD V12 Appendix C/C2 (Part 11.9a/b)' if origin.get(t, '').startswith(('V0003', 'V0004')) else ('Part 11.19a/b DDL-V12-R' if origin.get(t, '').startswith('V0006') else ('Part 11.24 reconciliation' if origin.get(t, '').startswith(('V0005', 'V0011')) else '')))
        w.writerow([t, origin.get(t, ''), src, d.get('ent', CORE.get(t, {}).get('ent', '')), d.get('scope', table_meta.get(t, {}).get('scope', '')),
                    d.get('imm', ''), ncols.get(t, 0), 'yes' if rls.get(t, (0, 0))[1] else 'no', pol.get(t, 0), alias.get(t, '')])
stats = dict(tables=len(ET), views=len(EV), columns=sum(ncols.get(t, 0) for t in ET), policies=sum(pol.values()),
             rls_forced=sum(1 for t in ET if rls.get(t, (0, 0))[1]), platform_tables=len(platform),
             indexes=q("SELECT count(*) FROM pg_indexes WHERE schemaname='ge'")[0][0],
             triggers=q("SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='ge' AND NOT t.tgisinternal")[0][0],
             functions=q("SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='ge'")[0][0],
             foreign_keys=q("SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='ge' AND contype='f'")[0][0],
             checks=q("SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='ge' AND contype='c'")[0][0],
             statements=sum(len(v) for v in MIG.values()), deferred=len(DEFERRED), skipped=len(SKIPPED), skipped_by_reason=dict(collections.Counter(r.split(':')[0].split('(')[0][:60] for _, r, _ in SKIPPED)), templates=dict(tmpl_count), triggers_by_kind=dict(trig),
             fk_support_indexes=fk_support, migrations=order, log=dict(LOG), vector_columns=len(vector_cols),
             deferred_by_mig=dict(collections.Counter(m for m, _, _ in DEFERRED)),
             by_origin=dict(collections.Counter(origin.get(t, '?').split('__')[0] for t in ET)))
save_json('schema_stats.json', stats)
save_json('schema_skipped.json', [dict(mig=m, reason=e, stmt=s_[:300]) for m, e, s_ in SKIPPED])
save_json('schema_deferred.json', [dict(mig=m, error=e, stmt=s[:400]) for m, e, s in DEFERRED])
print(json.dumps({k: v for k, v in stats.items() if k not in ('migrations',)}, indent=1))
