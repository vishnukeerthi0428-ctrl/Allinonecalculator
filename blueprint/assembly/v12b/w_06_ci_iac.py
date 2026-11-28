"""Group W (Part 11.24): GitHub Actions workflow skeletons and the Terraform/OpenTofu module outline, written to
final/build/ci/ and final/build/terraform/, then parsed (YAML with PyYAML; HCL with python-hcl2 when available).
Writes w_frag/ci_iac.json with file and job counts."""
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(__file__))
from w_common import *
import yaml

CI = OUT + 'ci/.github/workflows/'
TF = OUT + 'terraform/'
for d in (CI, TF):
    os.makedirs(d, exist_ok=True)

PR = r"""
name: pr
on:
  pull_request:
    branches: [main]
permissions: {contents: read, id-token: write, pull-requests: write}
concurrency: {group: "pr-${{ github.ref }}", cancel-in-progress: true}
env: {PYTHON_VERSION: "3.12", NODE_VERSION: "22", PG_IMAGE: "supabase/postgres:15.8.1.060"}  # pin digests; verify current Supabase image/major at implementation
jobs:
  lint:            # PL-02
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - uses: pnpm/action-setup@v4
      - run: uv sync --frozen && uv run ruff check . && uv run ruff format --check .
      - run: pnpm install --frozen-lockfile && pnpm -r lint && pnpm -r format:check
      - run: tofu fmt -check -recursive infra && actionlint
  typecheck:       # PL-03
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: uv sync --frozen && uv run mypy backend
      - run: pnpm install --frozen-lockfile && pnpm -r typecheck
  unit:            # PL-04 coverage gates NFR-082
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: uv sync --frozen && uv run pytest -n auto --cov --cov-fail-under=80 backend/tests/unit
      - run: pnpm install --frozen-lockfile && pnpm -r test -- --coverage
  architecture:    # PL-05 import contracts, unscoped-query rule, route permissions, traceability checker
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: uv sync --frozen && uv run lint-imports
      - run: uv run semgrep --config tools/semgrep/unscoped-query.yml --error backend
      - run: uv run python tools/route_permission_lint.py
      - name: Traceability checker (Part 11.11; blocks orphan FR/US/TC/API/table IDs)
        run: uv run python tools/trace_check.py --rtm docs/rtm.csv --openapi openapi/openapi.yaml --schema db/schema.sql --fail-on orphan,missing-test,missing-ac
  contract:        # PL-06 OpenAPI 3.1 single source (final/build/openapi.yaml) + generated client diff
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: uv sync --frozen && uv run python -m openapi_spec_validator openapi/openapi.yaml
      - run: uv run python manage.py spectacular --file /tmp/generated.yaml && uv run oasdiff breaking openapi/openapi.yaml /tmp/generated.yaml --fail-on ERR
      - run: pnpm install --frozen-lockfile && pnpm --filter api-client generate && git diff --exit-code packages/api-client
      - run: uv run schemathesis run /tmp/generated.yaml --checks all --base-url http://localhost:8000 --hypothesis-max-examples 25
  db-verify:       # PL-07 + PL-08: migrations apply clean; RLS, residency, append-only, activation-gate tests (TC-W-DB-01…42)
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: {POSTGRES_PASSWORD: postgres}
        ports: ["5432:5432"]
        options: --health-cmd pg_isready --health-interval 5s --health-retries 20
    steps:
      - uses: actions/checkout@v4
      - run: uv sync --frozen && uv run python manage.py makemigrations --check --dry-run
      - run: uv run squawk db/migrations/*.sql   # lock_timeout, concurrent indexes, no blind NOT NULL
      - run: uv run python tools/db/apply_and_verify.py --zones IN,EU --schema db/schema.sql --tests db/tests   # w_03_dbtest.py equivalent
      - run: uv run pytest backend/tests/rls -m "rls or authz" --two-tenant-fixture   # BOLA/BFLA suites (Part 4.1 §4.8.2)
  security:        # PL-09
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gitleaks/gitleaks-action@v2
      - run: uv run semgrep --config p/ci --config tools/semgrep --error
      - run: uv run pip-audit && pnpm audit --audit-level high && osv-scanner -r .
      - run: checkov -d infra --framework terraform --quiet
      - name: Forbid service_role and postgres DSNs in runtime config (DEC-778, SA-02)
        run: "! grep -RIn --exclude-dir=.git -E 'SUPABASE_SERVICE_ROLE|postgres://postgres' infra/live deploy backend/growth_engine/settings"
  ai-evals:        # PL-12 (paths: ai/**, gateway, AI adapters)
    if: contains(join(github.event.pull_request.labels.*.name, ','), 'ai') || github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: uv sync --frozen && uv run python -m ai.evals.run --changed-only --suite-registry ai/evals/registry.yaml --fail-on-threshold
  frontend-quality: # PL-13
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm install --frozen-lockfile && pnpm -r build && pnpm size-limit && pnpm lhci autorun
"""

MAIN = r"""
name: main
on:
  push:
    branches: [main]
permissions: {contents: read, id-token: write, packages: write, attestations: write}
jobs:
  build:           # PL-10/11
    runs-on: ubuntu-latest
    outputs: {digest: "${{ steps.push.outputs.digest }}"}
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with: {role-to-assume: "${{ vars.AWS_ROLE_BUILD }}", aws-region: ap-south-1}
      - id: push
        run: docker buildx build --sbom=true --provenance=true -t $ECR/growth-api:${{ github.sha }} --push .
      - run: cosign sign --yes $ECR/growth-api@${{ steps.push.outputs.digest }}
      - run: trivy image --exit-code 1 --severity CRITICAL $ECR/growth-api@${{ steps.push.outputs.digest }}
      - run: pnpm install --frozen-lockfile && vercel build --prod=false   # prebuilt outputs for website and admin
  deploy-staging:  # PL-14, both zones
    needs: build
    strategy: {matrix: {zone: [in, eu]}}
    environment: staging-${{ matrix.zone }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: tofu -chdir=infra/live/staging/${{ matrix.zone }} apply -auto-approve
      - name: Expand migrations as app_migrator (never service_role)
        run: python tools/db/migrate.py --secret-ref ${{ vars.MIGRATOR_SECRET_REF }} --expand-only --lock-timeout 5s
      - run: python tools/deploy/ecs_deploy.py --zone ${{ matrix.zone }} --digest ${{ needs.build.outputs.digest }} --verify-signature
      - run: vercel deploy --prebuilt --scope growth --token ${{ secrets.VERCEL_TOKEN }} --env ZONE=${{ matrix.zone }}
  e2e:             # PL-15
    needs: deploy-staging
    strategy: {matrix: {zone: [in, eu]}}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm install --frozen-lockfile && pnpm --filter e2e test:smoke -- --project=chromium --grep @smoke
        env: {BASE_URL: "https://staging.${{ matrix.zone }}.example.invalid"}
  dast-perf:       # PL-16
    needs: e2e
    runs-on: ubuntu-latest
    steps:
      - run: docker run --rm ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t https://staging.in.example.invalid -c zap.conf
      - run: k6 run load/smoke.js --threshold-fail-on-regression 20
"""

RELEASE = r"""
name: release
on:
  push:
    tags: ["v*.*.*.*"]
permissions: {contents: read, id-token: write}
jobs:
  evidence:        # PL-17: release record in A090 (tests, evals, SBOM, scans, migration plan, flags, rollback plan, restore drill age)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python tools/release/assemble_evidence.py --tag ${{ github.ref_name }} --require restore_drill_age_days<=31 --require rto_growth_min<=120 --require rpo_s<=900
  preprod:         # rehearsal on pre-prod per zone with production-shaped config and synthetic data
    needs: evidence
    strategy: {matrix: {zone: [in, eu]}}
    environment: preprod-${{ matrix.zone }}
    runs-on: ubuntu-latest
    steps:
      - run: python tools/deploy/full_cutover_rehearsal.py --zone ${{ matrix.zone }} --tag ${{ github.ref_name }}
  production:      # PL-18/19/20 (environment protection: two reviewers, approver != author)
    needs: preprod
    strategy: {max-parallel: 1, matrix: {zone: [in, eu]}}
    environment: prod-${{ matrix.zone }}
    runs-on: ubuntu-latest
    steps:
      - name: Restore point (Supabase PITR timestamp + WAL-G LSN + logical dump checksum)
        run: python tools/dr/capture_restore_point.py --zone ${{ matrix.zone }}
      - name: Dispatch freeze during schema step
        run: python tools/flags/set.py EXTERNAL_DISPATCH_ENABLED=false --zone ${{ matrix.zone }} --reason release
      - run: python tools/db/migrate.py --secret-ref ${{ vars.MIGRATOR_SECRET_REF }} --expand-only --lock-timeout 5s --statement-timeout 60s
      - run: python tools/deploy/ecs_deploy.py --zone ${{ matrix.zone }} --canary 10,50,100 --step-minutes 15 --burn-rate-abort 14.4
      - run: vercel promote ${{ vars.VERCEL_DEPLOYMENT_URL }} --scope growth --token ${{ secrets.VERCEL_TOKEN }}
      - name: Smoke SMK-01…SMK-20 and 30-minute SLO watch
        run: python tools/smoke/run.py --zone ${{ matrix.zone }} --watch-minutes 30
      - name: Re-enable dispatch only from the A090 activation record
        run: python tools/flags/restore_from_release_record.py --zone ${{ matrix.zone }}
  rollback:        # PL-20 (manual or automatic on failure)
    if: failure()
    needs: production
    runs-on: ubuntu-latest
    steps:
      - run: python tools/deploy/rollback.py --previous-task-definition --vercel-instant-rollback --flags-revert --no-db-down-migration
"""

NIGHTLY = r"""
name: nightly
on:
  schedule: [{cron: "30 20 * * *"}]   # 02:00 IST
  workflow_dispatch: {}
permissions: {contents: read, id-token: write}
jobs:
  full-suites:
    strategy: {matrix: {zone: [in, eu]}}
    runs-on: ubuntu-latest
    steps:
      - run: uv run pytest backend/tests -m "rls or authz or residency" --full
      - run: pnpm --filter e2e test:full
      - run: uv run python -m ai.evals.run --all --suite-registry ai/evals/registry.yaml   # 111 suites (DEC-788)
      - run: tofu -chdir=infra/live/prod/${{ matrix.zone }} plan -detailed-exitcode   # drift must be empty (exit 0)
      - run: python tools/db/privilege_drift.py --zone ${{ matrix.zone }}   # AU-292 snapshot compare
      - run: python tools/dr/restore_smoke.py --zone ${{ matrix.zone }} --path P3   # weekly full drill in dr-drill.yml
"""

DRILL = r"""
name: dr-drill
on:
  workflow_dispatch:
    inputs:
      zone: {type: choice, options: [in, eu], required: true}
      path: {type: choice, options: [P1_supabase_pitr, P2_walg_standby, P3_logical_dump], required: true}
      trigger: {type: choice, options: [release_gate, quarterly, incident], required: true}
  schedule: [{cron: "0 3 1 */3 *"}]   # quarterly
permissions: {contents: read, id-token: write}
jobs:
  drill:           # RPO <= 15 min (DEC-787), growth RTO <= 120 min (DEC-771); restore never leaves the zone
    environment: dr-${{ inputs.zone || 'in' }}
    runs-on: ubuntu-latest
    timeout-minutes: 180
    steps:
      - run: python tools/dr/drill.py --zone ${{ inputs.zone }} --path ${{ inputs.path }} --target-time "now-1m" --isolated-target --record restore_drill
      - run: python tools/dr/prv_pack.py --checks PRV-01,PRV-02,PRV-03,PRV-04,PRV-05,PRV-06,PRV-07,PRV-08
      - run: python tools/dr/assert_objectives.py --rpo-max-s 900 --rto-growth-max-min 120
      - run: python tools/dr/destroy_isolated_target.py
"""

files = {'pr.yml': PR, 'main.yml': MAIN, 'release.yml': RELEASE, 'nightly.yml': NIGHTLY, 'dr-drill.yml': DRILL}
ci_stats = {}
for n, t in files.items():
    write(CI + n, t.lstrip())
    y = yaml.safe_load(t)
    ci_stats[n] = len(y['jobs'])

# ------------------------------------------------------------------ Terraform / OpenTofu outline
MOD = {
 'zone_stack': ('Composition of one residency zone (IN or EU) for one environment', ['aws_network', 'aws_security_baseline', 'aws_data', 'aws_compute', 'aws_edge_api', 'aws_dr_standby', 'aws_observability', 'supabase_project', 'vercel_projects']),
 'aws_network': ('VPC, 2–3 AZ private subnets, NAT egress with static EIPs (Supabase network restriction allowlist), VPC endpoints (S3, Secrets Manager, KMS, ECR, Logs)', []),
 'aws_security_baseline': ('Account SCP attachments (deny regions outside the zone), CloudTrail, GuardDuty, Config, Security Hub, IAM roles for GitHub OIDC', []),
 'aws_data': ('ElastiCache for Valkey (TLS, ACL users), S3 buckets (objects, evidence, exports, backups) with SSE-KMS and public-access block, KMS keys per purpose, SES identity and configuration set', []),
 'aws_compute': ('ECS cluster, services api-web, api-admin, api-hooks, outbox-relay, worker-tx, worker-batch, beat, renderer; task roles; autoscaling; deployment circuit breaker', []),
 'aws_edge_api': ('ALB, ACM certificates, AWS WAF (managed + rate rules) for api.{zone}.{domain} and hooks.{zone}.{domain}; Route 53 records', []),
 'aws_dr_standby': ('PostgreSQL logical-replication subscriber (P2), WAL-G archive and base-backup buckets with Object Lock, in-zone cross-region replication (IN: ap-south-2; EU: second EU region), restore-drill IAM', []),
 'aws_observability': ('OTel collector, CloudWatch log groups (180-day IN, per DPA EU), metric filters, alarms AL-##, dashboards, SNS topics, Sentry project wiring', []),
 'supabase_project': ('Supabase project in the zone region, PITR add-on, network restrictions, SSL enforcement, Data API disabled/ge not exposed, log drain (verify provider resources)', []),
 'vercel_projects': ('Vercel projects website-{zone} and admin-{zone}: function region bom1/fra1, rewrites to api.{zone}, headers (CSP, HSTS), firewall rules, env (public only), log drain without bodies', []),
 'github_oidc': ('GitHub OIDC provider and per-environment deploy roles; environment protection rules mirrored in GitHub', []),
}
VERS = """terraform {
  required_version = ">= 1.9"   # OpenTofu 1.9+/Terraform 1.9+ (ADR-012/ADR-051); verify at implementation (27 Nov 2026)
  required_providers {
    aws      = { source = "hashicorp/aws", version = "~> 5.80" }
    supabase = { source = "supabase/supabase", version = "~> 1.5" }
    vercel   = { source = "vercel/vercel", version = "~> 2.0" }
  }
}
"""
for m, (desc, subs) in MOD.items():
    d = TF + 'modules/' + m + '/'
    os.makedirs(d, exist_ok=True)
    body = f'# Module {m}: {desc}\n'
    if m == 'zone_stack':
        body += VERS + '\n'
        for s in subs:
            body += f'module "{s}" {{\n  source = "../{s}"\n  env    = var.env\n  zone   = var.zone\n  tags   = local.tags\n}}\n\n'
        body += 'locals {\n  tags = { product = "commercial", env = var.env, zone = var.zone, data_residency = var.zone }\n}\n'
    elif m == 'supabase_project':
        body += ('resource "supabase_project" "this" {\n  organization_id   = var.supabase_org_id\n  name              = "growth-${var.env}-${lower(var.zone)}"\n'
                 '  database_password = var.db_bootstrap_password   # rotated immediately; app roles created by migration V0001\n'
                 '  region            = var.zone == "IN" ? "ap-south-1" : "eu-central-1"   # verify Supabase region identifiers\n'
                 '  lifecycle { prevent_destroy = true }\n}\n\n'
                 'resource "supabase_settings" "this" {\n  project_ref = supabase_project.this.id\n'
                 '  api = jsonencode({ db_schema = "graphql_public", max_rows = 1 })   # schema ge never exposed (SA-01)\n}\n')
    elif m == 'vercel_projects':
        body += ('resource "vercel_project" "site" {\n  for_each  = toset(["website", "admin"])\n  name      = "${each.key}-${lower(var.zone)}"\n  framework = "vite"\n'
                 '  serverless_function_region = var.zone == "IN" ? "bom1" : "fra1"   # DEC-786; AU-296 verifies\n}\n')
    else:
        body += f'# resources: see Part 11.24 §11.24.6.3 table row "{m}"\n'
    body += '\n'
    write(d + 'main.tf', body)
    write(d + 'variables.tf', 'variable "env" { type = string }\nvariable "zone" {\n  type = string\n  validation {\n    condition     = contains(["IN", "EU"], var.zone)\n    error_message = "zone must be IN or EU (DEC-772)."\n  }\n}\n'
          + ('variable "tags" {\n  type    = map(string)\n  default = {}\n}\n' if m != 'zone_stack' else '')
          + ('variable "supabase_org_id" { type = string }\nvariable "db_bootstrap_password" {\n  type      = string\n  sensitive = true\n}\n' if m == 'supabase_project' else ''))
LIVE = []
for env in ('dev', 'staging', 'preprod', 'prod'):
    for zone in ('in', 'eu'):
        d = TF + f'live/{env}/{zone}/'
        os.makedirs(d, exist_ok=True)
        write(d + 'main.tf', f'# {env} / {zone.upper()} — provisioned {"when the first EU tenant is contracted (DEC-772)" if zone == "eu" and env in ("preprod", "prod") else "from Sprint 0"}\n'
              f'terraform {{\n  backend "s3" {{\n    bucket       = "growth-tfstate-{zone}"\n    key          = "{env}/{zone}/terraform.tfstate"\n    region       = "{"ap-south-1" if zone == "in" else "eu-central-1"}"\n    encrypt      = true\n    use_lockfile = true\n  }}\n}}\n\n'
              f'module "zone" {{\n  source = "../../../modules/zone_stack"\n  env    = "{env}"\n  zone   = "{zone.upper()}"\n}}\n')
        LIVE.append(f'{env}/{zone}')
hcl_ok, hcl_err = None, []
try:
    import hcl2
    hcl_ok = 0
    for f in glob.glob(TF + '**/*.tf', recursive=True):
        try:
            hcl2.load(open(f)); hcl_ok += 1
        except Exception as e:
            hcl_err.append(f'{f}: {str(e)[:120]}')
except ImportError:
    pass
st = dict(workflows=ci_stats, jobs=sum(ci_stats.values()), modules=len(MOD), live_roots=LIVE, tf_files=len(glob.glob(TF + '**/*.tf', recursive=True)),
          hcl_parsed=hcl_ok, hcl_errors=hcl_err, yaml_parsed=len(files))
save_json('ci_iac.json', st)
print(st)
