-- V0008a__activation_gates_and_rule_pack_requirements
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

CREATE TABLE ge.rulepack_requirement (capability text NOT NULL, jurisdiction text NOT NULL CHECK (jurisdiction IN ('IN','EU','UK','US','AE')),
  pack_code text NOT NULL CHECK (pack_code ~ '^RP-[A-Z0-9-]+$'), PRIMARY KEY (capability, jurisdiction, pack_code));

CREATE TABLE ge.tenant_activation (
  tenant_id uuid NOT NULL REFERENCES ge.tenant (tenant_id), capability text NOT NULL, jurisdiction text NOT NULL CHECK (jurisdiction IN ('IN','EU','UK','US','AE')),
  enabled boolean NOT NULL DEFAULT false, requested_by uuid NOT NULL, approved_by_r01 uuid, approved_by_r10 uuid, approved_at timestamptz,
  revoked_at timestamptz, revoke_reason text, revision integer NOT NULL DEFAULT 1, updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, capability, jurisdiction),
  CONSTRAINT ck_tenant_activation__two_person CHECK (NOT enabled OR (approved_by_r01 IS NOT NULL AND approved_by_r10 IS NOT NULL
    AND approved_by_r01 <> approved_by_r10 AND approved_by_r01 <> requested_by AND approved_by_r10 <> requested_by AND approved_at IS NOT NULL)));

CREATE OR REPLACE FUNCTION ge.fn_touch_revision_nid() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.revision IS DISTINCT FROM OLD.revision + 1 THEN RAISE EXCEPTION 'STALE_REVISION: expected revision %', OLD.revision + 1 USING ERRCODE = '40001'; END IF;
  NEW.updated_at := now(); RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION ge.fn_activation_gate() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.enabled THEN
    IF NOT EXISTS (SELECT 1 FROM ge.rulepack_requirement r WHERE r.capability = NEW.capability AND r.jurisdiction = NEW.jurisdiction) THEN
      RAISE EXCEPTION 'ACTIVATION_NO_RULE_PACK: % has no rule pack for %', NEW.capability, NEW.jurisdiction USING ERRCODE = '23514'; END IF;
    IF EXISTS (SELECT 1 FROM ge.rulepack_requirement r WHERE r.capability = NEW.capability AND r.jurisdiction = NEW.jurisdiction
               AND NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack p WHERE p.pack_code = r.pack_code AND p.status = 'Approved'
                               AND p.counsel_signoff_ref IS NOT NULL AND p.effective_from <= current_date
                               AND (p.effective_to IS NULL OR p.effective_to >= current_date))) THEN
      RAISE EXCEPTION 'ACTIVATION_PACK_NOT_APPROVED: % in % needs every required pack approved with counsel sign-off', NEW.capability, NEW.jurisdiction USING ERRCODE = '23514'; END IF;
    IF NEW.jurisdiction = 'EU' AND ge.app_zone() <> 'EU' AND NEW.capability LIKE 'voice.%' THEN
      RAISE EXCEPTION 'ACTIVATION_ZONE: EU voice processing must run in the EU zone' USING ERRCODE = '23514'; END IF;
  END IF;
  RETURN NEW;
END $$;

CREATE TRIGGER trg_tenant_activation__gate BEFORE INSERT OR UPDATE ON ge.tenant_activation FOR EACH ROW EXECUTE FUNCTION ge.fn_activation_gate();

CREATE TRIGGER trg_tenant_activation__revision BEFORE UPDATE ON ge.tenant_activation FOR EACH ROW EXECUTE FUNCTION ge.fn_touch_revision_nid();

INSERT INTO ge.rulepack_requirement VALUES ('outreach.email', 'IN', 'RP-IN-DPDP') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.email', 'IN', 'RP-IN-ADV') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.email', 'IN', 'RP-COMMIT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.email', 'EU', 'RP-EU-MKT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.email', 'EU', 'RP-EU-AI') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.email', 'EU', 'RP-COMMIT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.email', 'US', 'RP-US-EMAIL') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.email', 'US', 'RP-COMMIT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.sms', 'IN', 'RP-IN-SMS') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.sms', 'IN', 'RP-IN-DPDP') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.sms', 'IN', 'RP-IN-ADV') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.whatsapp', 'IN', 'RP-IN-WA') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.whatsapp', 'IN', 'RP-IN-DPDP') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.whatsapp', 'IN', 'RP-IN-ADV') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.whatsapp', 'EU', 'RP-IN-WA') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.whatsapp', 'EU', 'RP-EU-MKT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('outreach.whatsapp', 'EU', 'RP-EU-AI') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('ads.campaigns', 'IN', 'RP-PLAT-ADS') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('ads.campaigns', 'IN', 'RP-IN-ADV') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('ads.campaigns', 'EU', 'RP-PLAT-ADS') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('ads.campaigns', 'EU', 'RP-EU-MKT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('ads.campaigns', 'EU', 'RP-EU-AI') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('ads.campaigns', 'US', 'RP-PLAT-ADS') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('ads.campaigns', 'US', 'RP-US-EMAIL') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.ai_calls', 'IN', 'RP-IN-VOICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.ai_calls', 'IN', 'RP-IN-DPDP') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.ai_calls', 'EU', 'RP-EU-VOICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.ai_calls', 'EU', 'RP-EU-AI') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.ai_calls', 'US', 'RP-US-VOICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.ai_calls', 'AE', 'RP-AE-VOICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.recording', 'IN', 'RP-GL-RECORDING') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.recording', 'IN', 'RP-IN-VOICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.recording', 'EU', 'RP-GL-RECORDING') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.recording', 'EU', 'RP-EU-VOICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.recording', 'US', 'RP-GL-RECORDING') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.recording', 'US', 'RP-US-VOICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.recording', 'AE', 'RP-GL-RECORDING') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('voice.recording', 'AE', 'RP-AE-VOICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('payments.mandated', 'IN', 'RP-IN-PAY') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('payments.mandated', 'IN', 'RP-AML-KYC') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('payments.mandated', 'EU', 'RP-EU-PAY') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('payments.mandated', 'EU', 'RP-AML-KYC') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('commerce.agentic_a2a', 'IN', 'RP-GL-AGENTCOM') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('commerce.agentic_a2a', 'IN', 'RP-GL-A2A-CONTRACT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('commerce.agentic_a2a', 'IN', 'RP-IN-AGENTCOM') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('commerce.agentic_a2a', 'EU', 'RP-GL-AGENTCOM') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('commerce.agentic_a2a', 'EU', 'RP-GL-A2A-CONTRACT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('commerce.agentic_a2a', 'EU', 'RP-EU-AGENTCOM') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('mandates.bounded', 'IN', 'RP-COMMIT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('mandates.bounded', 'EU', 'RP-COMMIT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('mandates.bounded', 'EU', 'RP-EU-AI') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('bids.auto_submission', 'IN', 'RP-IN-PROC') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('bids.auto_submission', 'IN', 'RP-COMMIT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('bids.auto_submission', 'EU', 'RP-EU-PROC') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('bids.auto_submission', 'EU', 'RP-COMMIT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('bids.auto_submission', 'US', 'RP-US-PROC') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('bids.auto_submission', 'US', 'RP-COMMIT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'IN', 'RP-IN-SEC') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'IN', 'RP-AML-KYC') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'IN', 'RP-INV-ADVICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'EU', 'RP-EU-PROSP') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'EU', 'RP-AML-KYC') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'EU', 'RP-INV-ADVICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'UK', 'RP-UK-FINPROM') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'UK', 'RP-AML-KYC') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'UK', 'RP-INV-ADVICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'US', 'RP-US-REGD') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'US', 'RP-AML-KYC') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.mode', 'US', 'RP-INV-ADVICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.reg_cf_portal_handoff', 'US', 'RP-US-REGCF') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('investor.reg_cf_portal_handoff', 'US', 'RP-INV-ADVICE') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('education.minors_outreach', 'IN', 'RP-EDU-MINORS') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('education.minors_outreach', 'IN', 'RP-IN-DPDP') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('education.minors_outreach', 'EU', 'RP-EDU-MINORS') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('education.minors_outreach', 'EU', 'RP-EU-MKT') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('health.wellness_outreach', 'IN', 'RP-HEALTH') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('health.wellness_outreach', 'IN', 'RP-IN-ADV') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('health.wellness_outreach', 'EU', 'RP-HEALTH') ON CONFLICT DO NOTHING;

INSERT INTO ge.rulepack_requirement VALUES ('health.wellness_outreach', 'EU', 'RP-EU-MKT') ON CONFLICT DO NOTHING;

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'AE', 1, 'Draft', 'RP-AE-VOICE' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-AE-VOICE');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'AML', 1, 'Draft', 'RP-AML-KYC' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-AML-KYC');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'COMMIT', 1, 'Draft', 'RP-COMMIT' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-COMMIT');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'EDU', 1, 'Draft', 'RP-EDU-MINORS' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-EDU-MINORS');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'EU', 1, 'Draft', 'RP-EU-AGENTCOM' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-EU-AGENTCOM');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'EU', 1, 'Draft', 'RP-EU-AI' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-EU-AI');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'EU', 1, 'Draft', 'RP-EU-MKT' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-EU-MKT');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'EU', 1, 'Draft', 'RP-EU-PAY' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-EU-PAY');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'EU', 1, 'Draft', 'RP-EU-PROC' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-EU-PROC');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'EU', 1, 'Draft', 'RP-EU-PROSP' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-EU-PROSP');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'EU', 1, 'Draft', 'RP-EU-VOICE' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-EU-VOICE');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'GL', 1, 'Draft', 'RP-GL-A2A-CONTRACT' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-GL-A2A-CONTRACT');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'GL', 1, 'Draft', 'RP-GL-AGENTCOM' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-GL-AGENTCOM');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'GL', 1, 'Draft', 'RP-GL-RECORDING' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-GL-RECORDING');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'HEALTH', 1, 'Draft', 'RP-HEALTH' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-HEALTH');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'IN', 1, 'Draft', 'RP-IN-ADV' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-IN-ADV');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'IN', 1, 'Draft', 'RP-IN-AGENTCOM' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-IN-AGENTCOM');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'IN', 1, 'Draft', 'RP-IN-DPDP' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-IN-DPDP');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'IN', 1, 'Draft', 'RP-IN-PAY' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-IN-PAY');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'IN', 1, 'Draft', 'RP-IN-PROC' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-IN-PROC');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'IN', 1, 'Draft', 'RP-IN-SEC' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-IN-SEC');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'IN', 1, 'Draft', 'RP-IN-SMS' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-IN-SMS');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'IN', 1, 'Draft', 'RP-IN-VOICE' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-IN-VOICE');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'IN', 1, 'Draft', 'RP-IN-WA' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-IN-WA');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'INV', 1, 'Draft', 'RP-INV-ADVICE' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-INV-ADVICE');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'PLAT', 1, 'Draft', 'RP-PLAT-ADS' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-PLAT-ADS');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'UK', 1, 'Draft', 'RP-UK-FINPROM' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-UK-FINPROM');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'US', 1, 'Draft', 'RP-US-EMAIL' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-US-EMAIL');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'US', 1, 'Draft', 'RP-US-PROC' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-US-PROC');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'US', 1, 'Draft', 'RP-US-REGCF' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-US-REGCF');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'US', 1, 'Draft', 'RP-US-REGD' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-US-REGD');

INSERT INTO ge.jurisdiction_pack (jurisdiction, version, status, pack_code) SELECT 'US', 1, 'Draft', 'RP-US-VOICE' WHERE NOT EXISTS (SELECT 1 FROM ge.jurisdiction_pack WHERE pack_code = 'RP-US-VOICE');
