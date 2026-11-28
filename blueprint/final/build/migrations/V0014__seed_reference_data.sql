-- V0014__seed_reference_data
SET search_path = ge, extensions, public;

SELECT set_config('app.zone', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

SELECT set_config('app.deployment_region', coalesce(nullif(current_setting('app.deployment_region', true), ''), 'IN'), false);

INSERT INTO ge.ref_currency (code, name, minor_units, is_active) VALUES ('INR', 'Indian rupee', 2, true);

INSERT INTO ge.ref_currency (code, name, minor_units, is_active) VALUES ('EUR', 'Euro', 2, true);

INSERT INTO ge.ref_currency (code, name, minor_units, is_active) VALUES ('USD', 'US dollar', 2, true);

INSERT INTO ge.ref_currency (code, name, minor_units, is_active) VALUES ('GBP', 'Pound sterling', 2, true);

INSERT INTO ge.ref_currency (code, name, minor_units, is_active) VALUES ('AED', 'UAE dirham', 2, true);

INSERT INTO ge.ref_currency (code, name, minor_units, is_active) VALUES ('SGD', 'Singapore dollar', 2, true);

INSERT INTO ge.recovery_path (zone, path, retention_days, location, enabled) VALUES ('IN', 'P1_supabase_pitr', 35, 'Supabase PITR (Mumbai)', true) ON CONFLICT DO NOTHING;

INSERT INTO ge.recovery_path (zone, path, retention_days, location, enabled) VALUES ('IN', 'P2_walg_standby', 35, 'S3 ap-south-1 WAL-G', true) ON CONFLICT DO NOTHING;

INSERT INTO ge.recovery_path (zone, path, retention_days, location, enabled) VALUES ('IN', 'P3_logical_dump', 35, 'S3 ap-south-1 nightly dump', true) ON CONFLICT DO NOTHING;

INSERT INTO ge.recovery_path (zone, path, retention_days, location, enabled) VALUES ('EU', 'P1_supabase_pitr', 35, 'Supabase PITR (Frankfurt)', true) ON CONFLICT DO NOTHING;

INSERT INTO ge.recovery_path (zone, path, retention_days, location, enabled) VALUES ('EU', 'P2_walg_standby', 35, 'S3 eu-central-1 WAL-G', true) ON CONFLICT DO NOTHING;

INSERT INTO ge.recovery_path (zone, path, retention_days, location, enabled) VALUES ('EU', 'P3_logical_dump', 35, 'S3 eu-central-1 nightly dump', true) ON CONFLICT DO NOTHING;

INSERT INTO ge.edge_project (project, zone, function_regions, carries_personal_data) VALUES ('web-in', 'IN', ARRAY['bom1'], true) ON CONFLICT DO NOTHING;

INSERT INTO ge.edge_project (project, zone, function_regions, carries_personal_data) VALUES ('admin-in', 'IN', ARRAY['bom1'], true) ON CONFLICT DO NOTHING;

INSERT INTO ge.edge_project (project, zone, function_regions, carries_personal_data) VALUES ('web-eu', 'EU', ARRAY['fra1'], true) ON CONFLICT DO NOTHING;

INSERT INTO ge.edge_project (project, zone, function_regions, carries_personal_data) VALUES ('admin-eu', 'EU', ARRAY['fra1'], true) ON CONFLICT DO NOTHING;

INSERT INTO ge.edge_project (project, zone, function_regions, carries_personal_data) VALUES ('developers', NULL, ARRAY['bom1','fra1'], false) ON CONFLICT DO NOTHING;
