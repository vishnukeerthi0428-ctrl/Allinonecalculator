-- V0002__context_functions
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

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
