-- Group I (Part 11.9): catalogue analysis of Appendix C + C2 applied to PostgreSQL 16.15
\pset format unaligned
\echo '## A1 tables with tenant_id but RLS disabled'
SELECT c.relname FROM pg_class c JOIN pg_attribute a ON a.attrelid=c.oid AND a.attname='tenant_id' AND NOT a.attisdropped
 WHERE c.relnamespace='public'::regnamespace AND c.relkind='r' AND NOT (c.relrowsecurity AND c.relforcerowsecurity) ORDER BY 1;
\echo '## A2 tables without tenant_id and without RLS (global/platform)'
SELECT c.relname FROM pg_class c WHERE c.relnamespace='public'::regnamespace AND c.relkind='r'
 AND NOT EXISTS (SELECT 1 FROM pg_attribute a WHERE a.attrelid=c.oid AND a.attname='tenant_id') ORDER BY 1;
\echo '## A3 tables with company_id whose policies never reference company'
SELECT c.relname FROM pg_class c JOIN pg_attribute a ON a.attrelid=c.oid AND a.attname='company_id'
 WHERE c.relnamespace='public'::regnamespace AND c.relkind='r'
 AND NOT EXISTS (SELECT 1 FROM pg_policies p WHERE p.tablename=c.relname AND (p.qual ILIKE '%company%' OR p.with_check ILIKE '%company%'));
\echo '## A4 policy command distribution'
SELECT cmd, count(*) FROM pg_policies GROUP BY 1;
\echo '## A5 nullable tenant_id columns'
SELECT table_name FROM information_schema.columns WHERE table_schema='public' AND column_name='tenant_id' AND is_nullable='YES' ORDER BY 1;
\echo '## A6 foreign keys without a supporting index (leading columns)'
SELECT conrelid::regclass AS tbl, conname, pg_get_constraintdef(oid) FROM pg_constraint c WHERE contype='f' AND connamespace='public'::regnamespace
 AND NOT EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid=c.conrelid AND (i.indkey::int2[])[0:array_length(c.conkey,1)-1] @> c.conkey AND (i.indkey::int2[])[0:array_length(c.conkey,1)-1] <@ c.conkey);
\echo '## A7 single-column FKs from tenant-scoped table to tenant-scoped table (not composite)'
SELECT c.conrelid::regclass, pg_get_constraintdef(c.oid) FROM pg_constraint c WHERE contype='f' AND connamespace='public'::regnamespace AND array_length(c.conkey,1)=1
 AND EXISTS (SELECT 1 FROM pg_attribute a WHERE a.attrelid=c.conrelid AND a.attname='tenant_id')
 AND EXISTS (SELECT 1 FROM pg_attribute a WHERE a.attrelid=c.confrelid AND a.attname='tenant_id') AND c.confrelid <> 'tenant'::regclass;
\echo '## A8 status/state/severity text columns without a CHECK naming them'
SELECT table_name, column_name FROM information_schema.columns col WHERE table_schema='public' AND column_name IN ('status','state','severity','contract_status','customer_type','offering_type','channel','request_type','tier','outcome','mode','kind')
 AND NOT EXISTS (SELECT 1 FROM pg_constraint k WHERE k.conrelid=(quote_ident(col.table_name))::regclass AND k.contype='c' AND pg_get_constraintdef(k.oid) ILIKE '%'||col.column_name||'%') ORDER BY 1,2;
\echo '## A9 secondary (non-PK, non-unique) indexes'
SELECT count(*) FROM pg_index i JOIN pg_class c ON c.oid=i.indrelid WHERE c.relnamespace='public'::regnamespace AND NOT i.indisprimary AND NOT i.indisunique;
\echo '## A10 money-like columns'
SELECT table_name, column_name, data_type, numeric_precision, numeric_scale FROM information_schema.columns WHERE table_schema='public' AND (column_name ~ '(amount|price|_minor|rate|cost)') ORDER BY 1;
\echo '## A11 jsonb columns count, tables using generic domain shape'
SELECT count(*) FROM information_schema.columns WHERE table_schema='public' AND data_type='jsonb';
SELECT count(*) FROM pg_class c WHERE relnamespace='public'::regnamespace AND relkind='r' AND EXISTS (SELECT 1 FROM pg_attribute a WHERE a.attrelid=c.oid AND a.attname='schema_ref') AND EXISTS (SELECT 1 FROM pg_attribute a WHERE a.attrelid=c.oid AND a.attname='evidence_refs');
\echo '## A12 roles/grants defined by DDL'
SELECT rolname FROM pg_roles WHERE rolname !~ '^pg_' AND rolname <> 'postgres';
\echo '## A13 triggers and UPDATE coverage'
SELECT tgname, tgtype FROM pg_trigger WHERE NOT tgisinternal;
\echo '## A14 tables lacking created_at'
SELECT count(*) FROM pg_class c WHERE relnamespace='public'::regnamespace AND relkind='r' AND NOT EXISTS (SELECT 1 FROM pg_attribute a WHERE a.attrelid=c.oid AND a.attname IN ('created_at','received_at','occurred_at','run_at','declared_at','detected_at','found_at','signed_at','captured_at'));
