"""Group W (Part 11.24): configuration and secrets catalogue, feature-flag registry, rule-pack gates and the
per-jurisdiction activation matrix. Sources: Part 4.4b ENV-01…24, Part 11.5a §11.5.4.4 (V12 ch36 + DEC-421), Part 4.3 §4.36
(flag classes), Part 2.4 CFG-01…32, Part 11.19b §11.19.5.5 E (dr.*), Parts 11.15a–e / 11.16d (rule-pack metadata), DEC-770…791.
Outputs (final/build/config/): env_catalogue.csv, feature_flags.csv, rulepack_gates.csv, activation_matrix.csv,
backend.env.example, website.env.example, admin.env.example; w_frag/config.json (consumed by w_02b for V0016)."""
import sys, os, csv, re, json, glob, collections
sys.path.insert(0, os.path.dirname(__file__))
from w_common import *

CD = OUT + 'config/'
os.makedirs(CD, exist_ok=True)

# ------------------------------------------------------------------ 1. environment variables (ENV-##); W = new in Part 11.24
# id, name, type/allowed, default, store, scope (process), per-env rule, source
ENV = [
 ('ENV-01', 'APP_PRODUCT', 'enum commercial', 'commercial', 'Parameter', 'all', 'immutable; mismatch with image label exits', 'Part 4.4b ENV-01; V12 ch36'),
 ('ENV-02', 'APP_ENV', 'enum local|dev|staging|preprod|prod|recovery', 'none (required)', 'Parameter', 'all', 'must match the AWS account and Supabase project; prod image in non-prod account exits', 'Part 4.4b ENV-02; DEC-592; Part 11.24'),
 ('ENV-03', 'WEBSITE_ORIGIN', 'HTTPS URL list', 'none', 'Parameter', 'api, bff-web', 'no wildcard; distinct from ADMIN_ORIGIN', 'Part 4.4b'),
 ('ENV-04', 'ADMIN_ORIGIN', 'HTTPS URL', 'none', 'Parameter', 'api, bff-admin', 'distinct origin per zone (admin.in.*, admin.eu.*)', 'Part 4.4b'),
 ('ENV-05', 'OAUTH_ISSUER', 'HTTPS URL', 'none', 'Parameter', 'bff', 'discovery reachable at start; iss match', 'Part 4.4b'),
 ('ENV-06', 'WEBSITE_AUDIENCE / PORTAL_AUDIENCE', 'string', 'none', 'Parameter', 'bff-web', 'must differ from ADMIN_AUDIENCE', 'Part 4.4b; V12 ch36'),
 ('ENV-07', 'ADMIN_AUDIENCE', 'string', 'none', 'Parameter', 'bff-admin, api', 'rejects external identities (R16/R17/R21)', 'Part 4.4b'),
 ('ENV-08', 'DATABASE_SECRET_REF (DATABASE_URL)', 'Secrets Manager ARN → Supabase pooler DSN, role app_rw', 'none', 'Secret ref', 'api', 'sslmode=verify-full; role must be app_rw (never owner, postgres or service_role); transaction pooler', 'Part 4.4b ENV-08; Part 11.5a; DEC-778'),
 ('ENV-08W', 'WORKER_DATABASE_SECRET_REF', 'ARN → pooler DSN, role app_worker', 'none', 'Secret ref', 'workers, outbox-relay, beat', 'role app_worker; same rules as ENV-08', 'Part 11.19b SA-02'),
 ('ENV-09', 'BROKER_SECRET_REF (BROKER_URL)', 'ARN → Valkey URL (TLS, ACL user per process)', 'none', 'Secret ref', 'api, workers', 'TLS; per-process ACL user', 'Part 4.4b'),
 ('ENV-10', 'OBJECT_STORE_REF', 'bucket names by purpose', 'growth-{env}-{zone}-objects', 'Parameter', 'api, workers', 'bucket in this account and zone; public-access block verified', 'Part 4.4b; DEC-772'),
 ('ENV-11', 'VECTOR_STORE_REF', 'schema name', 'vec', 'Parameter', 'ai gateway', 'RLS enabled check at start', 'Part 11.5a'),
 ('ENV-12', 'AUTOMATION_ENABLED', 'bool', 'false', 'Parameter + flag', 'automation engine', 'missing → false; recovery forces false', 'Part 4.4b'),
 ('ENV-13', 'EXTERNAL_DISPATCH_ENABLED', 'bool', 'false', 'Parameter + flag', 'adapter registry', 'true only in prod after A090 activation record; recovery forces false', 'Part 4.4b; V12 ch36'),
 ('ENV-14', 'PAID_FALLBACK_ENABLED', 'bool', 'false', 'Parameter + flag', 'gateway, adapters', 'true only with an approved budget line', 'Part 4.4b'),
 ('ENV-15', 'PROVIDER_TIMEOUTS', 'map provider → connect/read s', '5 / 20', 'Parameter', 'adapters', '1–120 each', 'Part 4.4b'),
 ('ENV-16', 'RETRY_POLICY', 'attempts, base, factor, cap', '3, 30 s, 2, 15 min', 'Parameter', 'workers', 'attempts ≤ 3 (BRL-AUT-06)', 'Part 4.4b; NFR-016'),
 ('ENV-17', 'LOG_LEVEL', 'enum', 'INFO (prod)', 'Parameter', 'all', 'DEBUG in prod only by sampled flag', 'Part 4.4b'),
 ('ENV-18', 'OTEL_EXPORTER_OTLP_ENDPOINT', 'URL', 'collector sidecar', 'Parameter', 'all', 'private endpoint in the zone', 'Part 4.4b; ADR-025'),
 ('ENV-19', 'LOG_REDACTION_POLICY', 'policy ID + version', 'current approved', 'Parameter', 'logger', 'must exist; missing → exit', 'Part 4.4b'),
 ('ENV-20', 'ALERT_DESTINATIONS', 'SNS ARNs by severity', 'none', 'Parameter', 'alarms', 'test publish at deploy', 'Part 4.4b'),
 ('ENV-21', 'MAX_REQUEST_BYTES / RATE_LIMIT_CLASSES', 'int / map', 'ADR-035, NFR-022', 'Parameter', 'api, edge', 'public intake ≤ 64 KB', 'Part 4.4b'),
 ('ENV-22', 'ALLOWED_HOSTS', 'host list', 'none', 'Parameter', 'api', 'no wildcard in prod', 'Part 4.4b'),
 ('ENV-23', 'WORKER_QUEUE_PREFIX', 'string', 'commercial.{env}.{zone}.', 'Parameter', 'workers', 'must start with APP_PRODUCT and contain env and zone', 'Part 4.4b; Part 11.5a'),
 ('ENV-24', 'RECOVERY_TARGETS', 'RPO/RTO per class', 'RC-1 15 min/4 h; growth 15 min/120 min; RC-2 24 h/8 h', 'Parameter', 'ops jobs', 'read by AU-297 and drills', 'Part 4.4b; DEC-771; DEC-787'),
 ('ENV-W01', 'ZONE', 'enum IN|EU', 'none (required)', 'Parameter', 'all backend + edge', 'must equal the database app.deployment_region; every request zone checked by ge.set_ctx (RESIDENCY_ZONE_MISMATCH)', 'DEC-772; Part 11.5a REGION_CODE'),
 ('ENV-W02', 'AWS_REGION', 'ap-south-1 (IN) | eu-central-1 (EU)', 'by ZONE', 'Parameter', 'all AWS clients', 'SCP denies other regions per zone account', 'DEC-772'),
 ('ENV-W03', 'SUPABASE_PROJECT_REF', 'string', 'per env and zone', 'Parameter', 'ops, CI', 'project region must match ZONE (Mumbai / Frankfurt, verify names)', 'Part 11.5a; DEC-772'),
 ('ENV-W04', 'SUPABASE_MIGRATOR_SECRET_REF', 'ARN → direct DSN, role app_migrator', 'none', 'Secret ref (CI only)', 'CI migrate job', 'never present in runtime task definitions; CI policy check', 'DEC-778; Part 11.19b SA-03'),
 ('ENV-W05', 'SUPABASE_SERVICE_ROLE_REF', 'ARN', 'none', 'Secret ref (break-glass)', 'CI break-glass only', 'two-person approval, ≤ 2 h, audit db.break_glass.used; any runtime reference fails the deploy', 'DEC-778; SA-02/03'),
 ('ENV-W06', 'VERCEL_FUNCTION_REGION', 'bom1 (IN) | fra1 (EU)', 'by ZONE', 'Vercel project setting (IaC)', 'Vercel functions/rewrites', 'AU-296 conformance check; deployment blocked when different', 'DEC-786; Part 11.19a VD-01…12'),
 ('ENV-W07', 'API_ORIGIN (VERCEL_API_ORIGIN)', 'HTTPS URL', 'https://api.{zone}.{domain}', 'Vercel env (public)', 'website, admin', 'HTTPS only; rewrite target per zone', 'Part 11.5a'),
 ('ENV-W08', 'KMS_KEY_ALIAS', 'alias/growth-{env}-{zone}-*', 'per purpose', 'Parameter', 'api, workers', 'zone key only; BYOK via tenant_key_config', 'DEC-776; C3-09'),
 ('ENV-W09', 'SES_CONFIGURATION_SET', 'string', 'growth-{env}-{zone}', 'Parameter', 'email adapter', 'SES in the zone region', 'DEC-772'),
 ('ENV-W10', 'MODEL_PROVIDER_SECRET_REFS', 'map provider → ARN', 'none', 'Secret ref', 'ai gateway', 'only registry-approved rows (DEC-788) are callable; zone endpoint', 'DEC-788; Part 11.19b C6'),
 ('ENV-W11', 'AI_BUDGET_CEILINGS_INR', 'map tenant tier → INR/month', '3000 / 12000 / 40000', 'Parameter + DB', 'ai gateway', 'hard stop at ceiling, degradation ladder', 'DEC-008'),
 ('ENV-W12', 'MESSAGING_WINDOW_LOCAL', 'HH:MM–HH:MM', '09:00–21:00', 'Parameter + DB policy', 'PDP', 'recipient local time; stricter rule pack wins', 'DEC-777'),
 ('ENV-W13', 'BENCH_PEPPER_REF', 'ARN', 'none', 'Secret ref', 'AU-299 worker (app_bench)', 'set as app.bench_pepper only inside the benchmark job', 'DEC-789; Part 11.19b C7'),
 ('ENV-W14', 'WEBHOOK_SIGNING_KEY_REF', 'ARN', 'none', 'Secret ref', 'webhook delivery (AU-294)', 'rotation with previous_secret_ref overlap', 'DEC-785'),
 ('ENV-W15', 'OAUTH_TOKEN_SIGNING_KEY_REF', 'ARN (KMS asymmetric)', 'none', 'Secret ref', 'token endpoint', 'per zone; JWKS published', 'DEC-785'),
 ('ENV-W16', 'SCIM_BASE_URL', 'HTTPS URL', 'https://api.{zone}.{domain}/scim/v2', 'Parameter', 'api', 'zone host only', 'DEC-784'),
 ('ENV-W17', 'PSP_SECRET_REFS', 'map psp → ARN', 'none', 'Secret ref', 'payments adapter', 'licensed PSP only; test keys outside prod', 'DEC-780; Part 11.17a'),
 ('ENV-W18', 'VOICE_CPAAS_SECRET_REFS', 'map provider → ARN', 'none', 'Secret ref', 'voice gateway', 'zone media region; recording storage in zone', 'DEC-782; Part 11.18'),
 ('ENV-W19', 'DLT_AGGREGATOR_SECRET_REF', 'ARN', 'none', 'Secret ref', 'SMS adapter (IN)', 'IN zone only', 'RP-IN-SMS; Part 11.19a'),
 ('ENV-W20', 'SENTRY_DSN', 'URL (server) / public DSN (browser)', 'none', 'Secret ref / public', 'all', 'PII scrubbing on; EU events to EU ingestion where offered (verify)', 'ADR-025'),
 ('ENV-W21', 'STATUS_PAGE_COMPONENT_IDS', 'map', 'none', 'Parameter', 'ops', '—', 'DEC-773/774'),
 ('ENV-W22', 'FEATURE_FLAG_SOURCE', 'enum db|unleash', 'db', 'Parameter', 'flags service', 'server-side evaluation only', 'ADR-052'),
 ('ENV-W23', 'DR_RPO_TARGET_S / DR_RTO_GROWTH_MIN', 'int', '900 / 120', 'Parameter (fixed)', 'AU-297', 'fixed by decision', 'DEC-787; DEC-771; Part 11.19b E'),
 ('ENV-W24', 'DR_LAG_WARN_S / PAGE_S / SEV1_S', 'int', '300 / 600 / 900', 'Parameter', 'AU-297', '—', 'Part 11.19b E'),
 ('ENV-W25', 'WALG_ARCHIVE_TIMEOUT_S / WALG_RETAIN_DAYS', 'int', '60 / 35', 'Parameter', 'standby subscriber', '—', 'Part 11.19b E'),
 ('ENV-W26', 'BUILD_SHA / IMAGE_DIGEST', 'string', 'set by CI', 'CI', 'all', 'must match the A090 release record', 'Part 4.3 PL-10'),
]
FRONT = [
 ('FE-01', 'VITE_API_ORIGIN', 'HTTPS URL', 'https://api.{zone}.{domain}', 'website, admin', 'Part 11.5a'),
 ('FE-02', 'VITE_ZONE', 'IN|EU', 'per Vercel project', 'website, admin', 'DEC-772'),
 ('FE-03', 'VITE_APP_SURFACE', 'website|admin', 'per project', 'website, admin', 'ADR-006'),
 ('FE-04', 'VITE_SENTRY_DSN', 'public DSN', 'none', 'website, admin', 'ADR-025'),
 ('FE-05', 'VITE_BUILD_SHA', 'string', 'CI', 'website, admin', 'Part 4.3'),
 ('FE-06', 'VITE_DEFAULT_LOCALE', 'BCP-47', 'en-IN (IN) / en-GB (EU)', 'website, admin', 'DEC-776'),
]

# ------------------------------------------------------------------ 2. feature flags (Part 4.3 §4.36 classes)
FLAGS = []
def flag(key, cls, default, owner, approval, source, note=''):
    FLAGS.append((key, cls, default, owner, approval, source, note))
for ch in ('email', 'whatsapp', 'sms', 'rcs', 'voice', 'linkedin', 'social', 'web_chat'):
    flag(f'channel.{ch}.dispatch', 'External channel enablement', 'OFF', 'R12', 'R12 + R01 (paid) + activation matrix', 'BRD §10; Part 4.3 §4.36', 'Global kill switch ENV-13 overrides')
for ad in ('payment.psp', 'esign', 'calendar.google', 'calendar.m365', 'crm.salesforce', 'crm.hubspot', 'crm.zoho', 'sms.dlt_aggregator', 'voice.cpaas', 'whatsapp.bsp', 'search.tavily', 'search.exa', 'extract.firecrawl'):
    flag(f'adapter.{ad}', 'Paid adapter / connector', 'OFF', 'R11/R12', 'Connector gate (AU-295, C2-T6) + R01 for paid', 'DEC-785; Part 11.19a')
for t in ('tier2.free_fallback', 'advanced_tier', 'multimodal.image', 'multimodal.video', 'multimodal.voice'):
    flag(f'ai.{t}', 'AI routing', 'OFF', 'R11', 'R01 + R10; registry row approved (DEC-788)', 'DEC-007; DEC-788')
flag('ai.agent.<AG-id>.enabled', 'Ops / kill switch', 'ON once launched', 'On-call, R11', 'Change record', 'ADR-085', 'One per AG-001…219')
flag('ai.kill_switch.global', 'Ops / kill switch', 'OFF (not engaged)', 'On-call, R01', 'Any one of R01/IC; release needs two people', 'Part 11.19b API-V12-R-048')
for lvl in ('L2', 'L3', 'L4'):
    flag(f'autonomy.<workflow>.{lvl}', 'Autonomy', 'OFF', 'R02 (L2) / R01 (L3, L4)', 'L3/L4 only under an active bounded mandate (DEC-779)', 'DEC-064; DEC-779')
for cap, dec in (('mandates.bounded', 'DEC-779'), ('commerce.agentic_a2a', 'DEC-780'), ('payments.mandated', 'DEC-780'), ('bids.auto_submission', 'DEC-781'),
                 ('voice.ai_calls.outbound', 'DEC-782'), ('voice.ai_calls.inbound', 'DEC-782'), ('voice.recording', 'DEC-782'), ('voice.coaching_from_recordings', 'DEC-782'),
                 ('investor.mode', 'DEC-783'), ('investor.public_offer_surfaces', 'DEC-783'), ('pricing.experiments', 'DEC-791'), ('media.generative', 'DEC-791')):
    flag(f'capability.{cap}', 'Regulated capability (tenant × jurisdiction)', 'OFF', 'R01', 'Two-person (R01 + R10) and activation matrix: every required rule pack approved by counsel', dec)
for p, dec in (('sso.enforcement', 'DEC-784'), ('scim.provisioning', 'DEC-784'), ('developer.api_keys', 'DEC-785'), ('developer.oauth_clients', 'DEC-785'), ('developer.webhooks', 'DEC-785'),
               ('developer.sandbox', 'DEC-785'), ('benchmarks.participation', 'DEC-789'), ('edge.personal_data_path', 'DEC-786'), ('residency.eu_zone', 'DEC-772'), ('sla.enterprise_tier', 'DEC-774')):
    flag(p, 'Platform capability', 'OFF', 'R12 / platform', 'Tenant admin with step-up; platform prerequisites green', dec)
flag('release.<feature>', 'Release', 'OFF in prod', 'Engineering', 'Change record; removed ≤ 90 days after rollout', 'Part 4.3 §4.36')
flag('experiment.<ui_test>', 'Experiment', 'OFF', 'Product owner', 'Never eligibility, pricing or consent', 'Part 4.3 §4.36')

# ------------------------------------------------------------------ 3. rule packs (harvested) and activation matrix
packs = {}
for f in sorted(glob.glob(B + 'Part-*.md')):
    for h, hdr, rows, ln in tables(f):
        if hdr[:2] == ['Field', 'Value']:
            d = {r[0]: r[1] for r in rows if len(r) >= 2}
            pid = d.get('Pack ID', '')
            if pid.startswith('RP-'):
                packs[pid] = dict(pack=pid, title=d.get('Title', '')[:140], jurisdiction=d.get('Jurisdiction(s)', '')[:120],
                                  channels=d.get('Channels', '')[:80], state=re.sub(r'[`*]', '', d.get('Version / state', ''))[:40],
                                  owner=d.get('Owner', 'R10')[:40], expiry=d.get('Expiry / fail-closed', '')[:120],
                                  source='Part ' + re.sub(r'Part-(\d+)-(\w+?)_.*', r'\1.\2', os.path.basename(f)))
CAP = {   # capability -> {jurisdiction: [packs]}  (strictest wins; any missing or unapproved pack keeps the flag OFF)
 'outreach.email': {'IN': ['RP-IN-DPDP', 'RP-IN-ADV', 'RP-COMMIT'], 'EU': ['RP-EU-MKT', 'RP-EU-AI', 'RP-COMMIT'], 'US': ['RP-US-EMAIL', 'RP-COMMIT']},
 'outreach.sms': {'IN': ['RP-IN-SMS', 'RP-IN-DPDP', 'RP-IN-ADV']},
 'outreach.whatsapp': {'IN': ['RP-IN-WA', 'RP-IN-DPDP', 'RP-IN-ADV'], 'EU': ['RP-IN-WA', 'RP-EU-MKT', 'RP-EU-AI']},
 'ads.campaigns': {'IN': ['RP-PLAT-ADS', 'RP-IN-ADV'], 'EU': ['RP-PLAT-ADS', 'RP-EU-MKT', 'RP-EU-AI'], 'US': ['RP-PLAT-ADS', 'RP-US-EMAIL']},
 'voice.ai_calls': {'IN': ['RP-IN-VOICE', 'RP-IN-DPDP'], 'EU': ['RP-EU-VOICE', 'RP-EU-AI'], 'US': ['RP-US-VOICE'], 'AE': ['RP-AE-VOICE']},
 'voice.recording': {'IN': ['RP-GL-RECORDING', 'RP-IN-VOICE'], 'EU': ['RP-GL-RECORDING', 'RP-EU-VOICE'], 'US': ['RP-GL-RECORDING', 'RP-US-VOICE'], 'AE': ['RP-GL-RECORDING', 'RP-AE-VOICE']},
 'payments.mandated': {'IN': ['RP-IN-PAY', 'RP-AML-KYC'], 'EU': ['RP-EU-PAY', 'RP-AML-KYC']},
 'commerce.agentic_a2a': {'IN': ['RP-GL-AGENTCOM', 'RP-GL-A2A-CONTRACT', 'RP-IN-AGENTCOM'], 'EU': ['RP-GL-AGENTCOM', 'RP-GL-A2A-CONTRACT', 'RP-EU-AGENTCOM']},
 'mandates.bounded': {'IN': ['RP-COMMIT'], 'EU': ['RP-COMMIT', 'RP-EU-AI']},
 'bids.auto_submission': {'IN': ['RP-IN-PROC', 'RP-COMMIT'], 'EU': ['RP-EU-PROC', 'RP-COMMIT'], 'US': ['RP-US-PROC', 'RP-COMMIT']},
 'investor.mode': {'IN': ['RP-IN-SEC', 'RP-AML-KYC', 'RP-INV-ADVICE'], 'EU': ['RP-EU-PROSP', 'RP-AML-KYC', 'RP-INV-ADVICE'], 'UK': ['RP-UK-FINPROM', 'RP-AML-KYC', 'RP-INV-ADVICE'],
                   'US': ['RP-US-REGD', 'RP-AML-KYC', 'RP-INV-ADVICE']},
 'investor.reg_cf_portal_handoff': {'US': ['RP-US-REGCF', 'RP-INV-ADVICE']},
 'education.minors_outreach': {'IN': ['RP-EDU-MINORS', 'RP-IN-DPDP'], 'EU': ['RP-EDU-MINORS', 'RP-EU-MKT']},
 'health.wellness_outreach': {'IN': ['RP-HEALTH', 'RP-IN-ADV'], 'EU': ['RP-HEALTH', 'RP-EU-MKT']},
}
JUR = ['IN', 'EU', 'UK', 'US', 'AE']
matrix = []
for cap, m in CAP.items():
    for j in JUR:
        req = m.get(j)
        if req:
            missing = [p for p in req if p not in packs]
            matrix.append(dict(capability=cap, jurisdiction=j, flag=f'activation.{cap}.{j}', required_packs=';'.join(req),
                               packs_drafted='yes' if not missing else 'no: ' + ','.join(missing),
                               default='OFF', can_enable_when='every required pack approved, counsel sign-off on file, not expired; R01 + R10 two-person approval; zone stack live',
                               status_today='blocked (packs in draft, counsel sign-off pending)'))
        else:
            matrix.append(dict(capability=cap, jurisdiction=j, flag=f'activation.{cap}.{j}', required_packs='—', packs_drafted='no pack drafted',
                               default='OFF (hard)', can_enable_when='not activatable: no rule pack exists for this jurisdiction (DEC-776 legal gate)',
                               status_today='blocked (no pack)'))


def wcsv(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(header); w.writerows(rows)

wcsv(CD + 'env_catalogue.csv', ['id', 'name', 'type_allowed', 'default', 'store', 'consumers', 'validation_fail_closed', 'source'], ENV)
wcsv(CD + 'frontend_env_catalogue.csv', ['id', 'name', 'type', 'default', 'consumers', 'source'], FRONT)
wcsv(CD + 'feature_flags.csv', ['key', 'class', 'default', 'owner', 'approval', 'source', 'note'], FLAGS)
wcsv(CD + 'rulepack_gates.csv', ['pack', 'title', 'jurisdiction', 'channels', 'state', 'owner', 'expiry_fail_closed', 'source'],
     [[p[k] for k in ('pack', 'title', 'jurisdiction', 'channels', 'state', 'owner', 'expiry', 'source')] for p in packs.values()])
wcsv(CD + 'activation_matrix.csv', list(matrix[0].keys()), [list(r.values()) for r in matrix])


def env_example(env, zone):
    L = [f'# backend.env.example ({env}, {zone}) — non-secret values only; secrets are *_REF ARNs resolved at start (Part 11.24 §11.24.5)']
    for e in ENV:
        name = e[1].split(' ')[0]
        val = e[3]
        if 'Secret ref' in e[4]:
            val = f'arn:aws:secretsmanager:{"ap-south-1" if zone == "IN" else "eu-central-1"}:<account>:secret:/growth/{env}/{zone.lower()}/{name.lower()}'
        if name == 'APP_ENV':
            val = env
        if name == 'ZONE':
            val = zone
        if name == 'AWS_REGION':
            val = 'ap-south-1' if zone == 'IN' else 'eu-central-1'
        if name in ('EXTERNAL_DISPATCH_ENABLED', 'AUTOMATION_ENABLED', 'PAID_FALLBACK_ENABLED'):
            val = 'false'
        L.append(f'{name}={val}')
    return '\n'.join(L) + '\n'

write(CD + 'backend.env.example', env_example('dev', 'IN'))
write(CD + 'website.env.example', '\n'.join(f'{f[1]}={f[3]}' for f in FRONT) + '\nVITE_APP_SURFACE=website\n')
write(CD + 'admin.env.example', '\n'.join(f'{f[1]}={f[3]}' for f in FRONT) + '\nVITE_APP_SURFACE=admin\n')
cfg = dict(env=len(ENV), frontend_env=len(FRONT), flags=len(FLAGS), packs=len(packs), matrix_rows=len(matrix),
           matrix_with_packs=sum(1 for r in matrix if r['required_packs'] != '—'), capabilities=len(CAP), jurisdictions=JUR,
           requirements=[(r['capability'], r['jurisdiction'], p) for r in matrix if r['required_packs'] != '—' for p in r['required_packs'].split(';')],
           packs_list=sorted(packs), flag_classes=dict(collections.Counter(f[1] for f in FLAGS)))
save_json('config.json', cfg)
print({k: v for k, v in cfg.items() if k not in ('requirements', 'packs_list')})
