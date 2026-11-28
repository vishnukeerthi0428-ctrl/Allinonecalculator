-- V0005__reconcile_v12_lineage_for_ddl_v12_r
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

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
