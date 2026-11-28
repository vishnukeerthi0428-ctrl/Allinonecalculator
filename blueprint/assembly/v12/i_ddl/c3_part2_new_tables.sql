-- C3-11 V6 logical entities absent from Appendix C (MT-09/10/11/18/27/33; ch26 V6 entity table)
CREATE TABLE IF NOT EXISTS company_operating_country (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, country_code char(2) NOT NULL CHECK (country_code ~ '^[A-Z]{2}$'),
  status text NOT NULL DEFAULT 'active' CHECK (status IN ('active','paused','exited')), created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, company_id, country_code), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));
ALTER TABLE division ADD COLUMN IF NOT EXISTS name_norm text GENERATED ALWAYS AS (lower(btrim(name))) STORED;
ALTER TABLE division ADD CONSTRAINT division_company_uq UNIQUE (tenant_id, company_id, division_id);
ALTER TABLE division ADD CONSTRAINT division_name_uq UNIQUE (tenant_id, company_id, name_norm);
ALTER TABLE brand ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'active' CHECK (status IN ('active','retired'));
ALTER TABLE brand ADD COLUMN IF NOT EXISTS valid_from timestamptz NOT NULL DEFAULT now();
ALTER TABLE brand ADD COLUMN IF NOT EXISTS valid_to timestamptz;
ALTER TABLE brand ADD CONSTRAINT brand_company_uq UNIQUE (tenant_id, company_id, brand_id);
ALTER TABLE brand ADD CONSTRAINT brand_division_company_fk FOREIGN KEY (tenant_id, company_id, division_id) REFERENCES division(tenant_id, company_id, division_id);
ALTER TABLE offering ADD CONSTRAINT offering_company_uq UNIQUE (tenant_id, company_id, offering_id);
ALTER TABLE offering ADD CONSTRAINT offering_brand_company_fk FOREIGN KEY (tenant_id, company_id, brand_id) REFERENCES brand(tenant_id, company_id, brand_id);
ALTER TABLE market ADD CONSTRAINT market_company_uq UNIQUE (tenant_id, company_id, market_id);
ALTER TABLE channel_account ADD CONSTRAINT channel_account_company_uq UNIQUE (tenant_id, company_id, account_id);
CREATE TABLE IF NOT EXISTS offering_market (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, offering_id uuid NOT NULL, market_id uuid NOT NULL,
  eligibility_status text NOT NULL DEFAULT 'pending' CHECK (eligibility_status IN ('pending','eligible','held','ineligible')), policy_ref uuid,
  created_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY (tenant_id, company_id, offering_id, market_id),
  FOREIGN KEY (tenant_id, company_id, offering_id) REFERENCES offering(tenant_id, company_id, offering_id),
  FOREIGN KEY (tenant_id, company_id, market_id) REFERENCES market(tenant_id, company_id, market_id));
CREATE TABLE IF NOT EXISTS channel_account_market (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, account_id uuid NOT NULL, market_id uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, company_id, account_id, market_id),
  FOREIGN KEY (tenant_id, company_id, account_id) REFERENCES channel_account(tenant_id, company_id, account_id),
  FOREIGN KEY (tenant_id, company_id, market_id) REFERENCES market(tenant_id, company_id, market_id));
CREATE TABLE IF NOT EXISTS configuration_revision (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, config_revision_id uuid NOT NULL DEFAULT gen_random_uuid(), scope text NOT NULL,
  base_version int NOT NULL CHECK (base_version >= 0), revision int NOT NULL CHECK (revision >= 1), requester_id uuid NOT NULL, reviewer_id uuid,
  snapshot_ref text NOT NULL, snapshot_hash bytea NOT NULL CHECK (octet_length(snapshot_hash) = 32),
  status text NOT NULL CHECK (status IN ('Draft','Pending review','Approved','Rejected','Superseded')), created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, config_revision_id), UNIQUE (tenant_id, company_id, scope, revision),
  FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id),
  CHECK (reviewer_id IS NULL OR reviewer_id <> requester_id), CHECK (status NOT IN ('Approved') OR reviewer_id IS NOT NULL),
  CHECK (revision = base_version + 1));
CREATE TABLE IF NOT EXISTS workflow_configuration (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, config_id uuid NOT NULL DEFAULT gen_random_uuid(),
  offering_id uuid NOT NULL, market_id uuid NOT NULL, account_id uuid, sku_id text NOT NULL CHECK (sku_id ~ '^SM-SVC-\d{2}$'),
  wf_id text NOT NULL, wf_version int NOT NULL CHECK (wf_version >= 1), budget_minor bigint NOT NULL CHECK (budget_minor >= 0),
  currency char(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'), authority text NOT NULL CHECK (authority IN ('L0','L1','L2','L3')),
  schedule text, status text NOT NULL CHECK (status IN ('Draft','Active','Paused','Retired')), config_revision_id uuid NOT NULL,
  version int NOT NULL DEFAULT 1 CHECK (version >= 1), created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, config_id),
  FOREIGN KEY (tenant_id, company_id, offering_id) REFERENCES offering(tenant_id, company_id, offering_id),
  FOREIGN KEY (tenant_id, company_id, market_id) REFERENCES market(tenant_id, company_id, market_id),
  FOREIGN KEY (tenant_id, company_id, account_id) REFERENCES channel_account(tenant_id, company_id, account_id),
  FOREIGN KEY (tenant_id, config_revision_id) REFERENCES configuration_revision(tenant_id, config_revision_id),
  CHECK (left(wf_id, 9) = sku_id));
CREATE UNIQUE INDEX IF NOT EXISTS ux_workflow_configuration_active ON workflow_configuration (tenant_id, company_id, offering_id, market_id, wf_id) WHERE status = 'Active';
-- BusinessEvent: the attribution fact (MT-27, MT-31; ch29 V6 event attribution). Unknown attribution stays NULL.
CREATE TABLE IF NOT EXISTS business_event (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, event_id uuid NOT NULL DEFAULT gen_random_uuid(), idempotency_key text NOT NULL,
  event_type text NOT NULL CHECK (event_type IN ('lead_created','opportunity_qualified','meeting_held','proposal_sent','deal_won','deal_lost','order_confirmed',
     'invoice_issued','payment_verified','renewal_won','churned','refund_verified')),
  offering_id uuid, market_id uuid, account_id uuid, campaign_id uuid, sku_id text CHECK (sku_id IS NULL OR sku_id ~ '^SM-SVC-\d{2}$'), wf_id text,
  run_id uuid, wf_version int, config_revision_id uuid, correlation_id uuid,
  amount_minor bigint CHECK (amount_minor IS NULL OR amount_minor >= 0), currency char(3) CHECK (currency IS NULL OR currency ~ '^[A-Z]{3}$'),
  evidence_ref text, verified boolean NOT NULL DEFAULT false, is_simulated boolean NOT NULL DEFAULT false, source_kind text NOT NULL DEFAULT 'live'
     CHECK (source_kind IN ('live','import','demo_fixture')),
  occurred_at timestamptz NOT NULL, recorded_at timestamptz NOT NULL DEFAULT now(), metric_version int NOT NULL DEFAULT 1,
  PRIMARY KEY (tenant_id, event_id), UNIQUE (tenant_id, company_id, idempotency_key),
  FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id),
  FOREIGN KEY (tenant_id, company_id, offering_id) REFERENCES offering(tenant_id, company_id, offering_id),
  FOREIGN KEY (tenant_id, company_id, market_id) REFERENCES market(tenant_id, company_id, market_id),
  FOREIGN KEY (tenant_id, company_id, account_id) REFERENCES channel_account(tenant_id, company_id, account_id),
  FOREIGN KEY (tenant_id, company_id, run_id) REFERENCES workflow_run(tenant_id, company_id, run_id),
  CHECK ((amount_minor IS NULL) = (currency IS NULL)),
  CHECK (wf_id IS NULL OR (sku_id IS NOT NULL AND left(wf_id, 9) = sku_id)),
  CHECK (NOT verified OR evidence_ref IS NOT NULL),
  CHECK (source_kind <> 'demo_fixture' OR is_simulated));
CREATE OR REPLACE FUNCTION fn_business_event_attribution() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN  -- run-attributed events inherit only evidenced dimensions from the run; never invent offering/market
  IF NEW.run_id IS NOT NULL THEN
    SELECT r.sku_id, r.wf_id, r.wf_version INTO NEW.sku_id, NEW.wf_id, NEW.wf_version FROM workflow_run r
     WHERE r.tenant_id = NEW.tenant_id AND r.company_id = NEW.company_id AND r.run_id = NEW.run_id;
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER trg_business_event_attr BEFORE INSERT ON business_event FOR EACH ROW EXECUTE FUNCTION fn_business_event_attribution();
CREATE TRIGGER trg_business_event_immutable BEFORE UPDATE OR DELETE ON business_event FOR EACH ROW EXECUTE FUNCTION fn_forbid_mutation();

-- C3-12 Analytics: metric contract (ch29 V5 "Metric contract"), versioned aggregates, experiments, feedback, SLI, customer value
CREATE TABLE IF NOT EXISTS metric_definition (
  metric_id text NOT NULL CHECK (metric_id ~ '^[A-Z][A-Z0-9]*(-[A-Z0-9]+)*-\d{2,3}$'), metric_version int NOT NULL CHECK (metric_version >= 1),
  name text NOT NULL, formula text NOT NULL, numerator_sql_ref text NOT NULL, denominator_sql_ref text, unit text NOT NULL CHECK (unit IN ('count','ratio','fraction','ms','seconds','score','minor_currency','percent')),
  source_event_types text[] NOT NULL, currency_rule text NOT NULL CHECK (currency_rule IN ('native_only','no_currency','approved_fx_display')),
  timezone text NOT NULL DEFAULT 'Asia/Kolkata', period_grain text NOT NULL CHECK (period_grain IN ('hour','day','week','month','quarter','rolling_30d')),
  filters jsonb NOT NULL DEFAULT '{}', attribution_rule text CHECK (attribution_rule IN ('none','first_touch','last_non_direct','linear','position_40_20_40')),
  observation_window_days int CHECK (observation_window_days BETWEEN 1 AND 365), owner text NOT NULL, baseline numeric, threshold numeric,
  threshold_direction text CHECK (threshold_direction IN ('<=','>=','=')), audience text NOT NULL CHECK (audience IN ('tenant','operator')),
  status text NOT NULL CHECK (status IN ('Draft','Approved','Retired')), approved_by uuid, approved_at timestamptz,
  PRIMARY KEY (metric_id, metric_version), CHECK (status <> 'Approved' OR approved_by IS NOT NULL));
CREATE TABLE IF NOT EXISTS metric_aggregate (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, metric_id text NOT NULL, metric_version int NOT NULL, period_start timestamptz NOT NULL,
  dimension_hash bytea NOT NULL, dimensions jsonb NOT NULL DEFAULT '{}', aggregate_version int NOT NULL DEFAULT 1 CHECK (aggregate_version >= 1),
  numerator numeric NOT NULL, denominator numeric CHECK (denominator IS NULL OR denominator >= 0), unknown_count bigint NOT NULL DEFAULT 0 CHECK (unknown_count >= 0),
  value numeric GENERATED ALWAYS AS (CASE WHEN denominator IS NULL THEN numerator WHEN denominator = 0 THEN NULL ELSE numerator / denominator END) STORED,
  currency char(3) CHECK (currency IS NULL OR currency ~ '^[A-Z]{3}$'), source_event_count bigint NOT NULL CHECK (source_event_count >= 0),
  computed_at timestamptz NOT NULL DEFAULT now(), superseded_at timestamptz, late_event_reason text,
  PRIMARY KEY (tenant_id, company_id, metric_id, metric_version, period_start, dimension_hash, aggregate_version),
  FOREIGN KEY (metric_id, metric_version) REFERENCES metric_definition(metric_id, metric_version),
  FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id),
  CHECK (aggregate_version = 1 OR late_event_reason IS NOT NULL));
CREATE UNIQUE INDEX IF NOT EXISTS ux_metric_aggregate_current ON metric_aggregate (tenant_id, company_id, metric_id, metric_version, period_start, dimension_hash) WHERE superseded_at IS NULL;
CREATE TABLE IF NOT EXISTS experiment (
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, experiment_id uuid NOT NULL DEFAULT gen_random_uuid(), name text NOT NULL,
  hypothesis text NOT NULL, primary_metric_id text NOT NULL, primary_metric_version int NOT NULL, guardrail_metric_ids text[] NOT NULL DEFAULT '{}',
  allocation jsonb NOT NULL, consent_class text NOT NULL CHECK (consent_class IN ('necessary','analytics','marketing')),
  min_sample_per_arm int NOT NULL CHECK (min_sample_per_arm >= 100), stopping_rule text NOT NULL, max_duration_days int NOT NULL CHECK (max_duration_days BETWEEN 7 AND 90),
  status text NOT NULL CHECK (status IN ('Draft','Approved','Running','Stopped','Concluded')), winner_arm text, decided_by uuid, decided_at timestamptz,
  created_by uuid NOT NULL, PRIMARY KEY (tenant_id, experiment_id), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id),
  FOREIGN KEY (primary_metric_id, primary_metric_version) REFERENCES metric_definition(metric_id, metric_version),
  CHECK (winner_arm IS NULL OR (decided_by IS NOT NULL AND decided_by <> created_by AND status = 'Concluded')));   -- CV-14: no automatic winner
CREATE TABLE IF NOT EXISTS feedback_case (   -- ch26 V5 opt_feedback_case; ch29 CS-12 (CSAT, CES, NPS)
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, case_id uuid NOT NULL DEFAULT gen_random_uuid(), revision int NOT NULL DEFAULT 1,
  milestone text NOT NULL CHECK (milestone IN ('onboarding_complete','first_value','support_resolved','renewal','quarterly')),
  output_ref text, topic text, csat smallint CHECK (csat BETWEEN 1 AND 5), ces smallint CHECK (ces BETWEEN 1 AND 7), nps smallint CHECK (nps BETWEEN 0 AND 10),
  responded boolean NOT NULL, consent_class text NOT NULL CHECK (consent_class IN ('necessary','analytics','marketing')), owner_id uuid,
  state text NOT NULL CHECK (state IN ('Invited','Responded','Expired','In follow-up','Resolved')), resolution_ref text, invited_at timestamptz NOT NULL, responded_at timestamptz,
  PRIMARY KEY (tenant_id, case_id, revision), FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id),
  CHECK (responded = (responded_at IS NOT NULL)), CHECK (responded OR (csat IS NULL AND ces IS NULL AND nps IS NULL)),
  CHECK (state <> 'Resolved' OR resolution_ref IS NOT NULL));
CREATE TABLE IF NOT EXISTS sli_sample (   -- ch26 V5 opt_sli_sample; ch29 KPI-05/06/26–31
  component text NOT NULL, tenant_scope uuid NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000', metric_id text NOT NULL, metric_version int NOT NULL, window_start timestamptz NOT NULL, window_end timestamptz NOT NULL,
  numerator bigint NOT NULL CHECK (numerator >= 0), denominator bigint NOT NULL CHECK (denominator >= 0), status text NOT NULL CHECK (status IN ('ok','missing_data','excluded_approved')),
  exclusion_ref text, PRIMARY KEY (component, metric_id, metric_version, window_start, tenant_scope),
  CHECK (window_end > window_start), CHECK (numerator <= denominator OR metric_id ~ '^KPI-(05|26|27|28|29|30|31)$'), CHECK (status <> 'excluded_approved' OR exclusion_ref IS NOT NULL));
CREATE TABLE IF NOT EXISTS customer_value (   -- ch26 V5 opt_customer_value: no guaranteed value
  tenant_id uuid NOT NULL, sku_id text NOT NULL CHECK (sku_id ~ '^SM-SVC-\d{2}$'), period text NOT NULL CHECK (period ~ '^\d{4}-(0[1-9]|1[0-2])$'),
  accepted_count int NOT NULL CHECK (accepted_count >= 0), allowance int NOT NULL CHECK (allowance >= 0), outcome_evidence_refs text[] NOT NULL DEFAULT '{}',
  assumption_version int NOT NULL, label text NOT NULL DEFAULT 'Estimate - not a guarantee' CHECK (label LIKE 'Estimate%'),
  PRIMARY KEY (tenant_id, sku_id, period));
CREATE TABLE IF NOT EXISTS journey_event (   -- ch26 V5 opt_journey_event; ch29 AT-14 consent-aware acquisition analytics
  event_id uuid NOT NULL, audience text NOT NULL CHECK (audience IN ('operator','subscriber')), tenant_id uuid, cohort text, acquisition_source text NOT NULL DEFAULT 'unknown',
  consent_class text NOT NULL CHECK (consent_class IN ('necessary','analytics','marketing')), pseudonymous_ref bytea, stage text NOT NULL, sku_id text,
  occurred_at timestamptz NOT NULL, correlation_id uuid, PRIMARY KEY (event_id),
  CHECK (consent_class <> 'necessary' OR pseudonymous_ref IS NULL), CHECK (pseudonymous_ref IS NULL OR octet_length(pseudonymous_ref) = 32),
  CHECK (audience <> 'subscriber' OR tenant_id IS NOT NULL));
CREATE TABLE IF NOT EXISTS domain_record_version (   -- ch26 "Proposed V4 persistence additions"
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, table_name text NOT NULL, record_id uuid NOT NULL, revision int NOT NULL CHECK (revision >= 1),
  payload jsonb NOT NULL, reason text NOT NULL, actor_id uuid NOT NULL, review_state text NOT NULL CHECK (review_state IN ('none','pending','approved','rejected')),
  created_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY (tenant_id, table_name, record_id, revision),
  FOREIGN KEY (tenant_id, company_id) REFERENCES company(tenant_id, company_id));
CREATE TRIGGER trg_domain_record_version_immutable BEFORE UPDATE OR DELETE ON domain_record_version FOR EACH ROW EXECUTE FUNCTION fn_forbid_mutation();
CREATE TABLE IF NOT EXISTS usage_reservation (   -- ch26 V4 usage_reservation; DB-V2-USAGE
  tenant_id uuid NOT NULL, company_id uuid NOT NULL, reservation_id uuid NOT NULL DEFAULT gen_random_uuid(), sku_id text NOT NULL, period text NOT NULL,
  run_id uuid NOT NULL, units int NOT NULL CHECK (units > 0), amount_minor bigint NOT NULL CHECK (amount_minor >= 0), currency char(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
  state text NOT NULL CHECK (state IN ('Reserved','Committed','Released','Reconciled')), idempotency_key text NOT NULL, created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, reservation_id), UNIQUE (tenant_id, run_id, period), UNIQUE (tenant_id, idempotency_key),
  FOREIGN KEY (tenant_id, company_id, run_id) REFERENCES workflow_run(tenant_id, company_id, run_id));
