"""Group W: validate final/build/openapi.yaml with openapi-spec-validator (OpenAPI 3.1) plus blueprint lint rules.
Writes w_frag/openapi_validation.json."""
import sys, os, re, json, collections
sys.path.insert(0, os.path.dirname(__file__))
from w_common import *
import yaml

spec = yaml.safe_load(open(OUT + 'openapi.yaml', encoding='utf-8'))
res = {'validator': None, 'validator_errors': [], 'lint': {}}
try:
    import openapi_spec_validator as osv
    from openapi_spec_validator import validate
    from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
    errs = []
    try:
        from openapi_spec_validator import OpenAPIV31SpecValidator
        v = OpenAPIV31SpecValidator(spec)
        errs = [str(e.message)[:300] for e in v.iter_errors()]
    except ImportError:
        try:
            validate(spec)
        except Exception as e:  # pragma: no cover
            errs = [str(e)[:300]]
    res['validator'] = 'openapi-spec-validator ' + getattr(osv, '__version__', '?') + ' (OpenAPI 3.1 schema + semantic checks)'
    res['validator_errors'] = errs
except ImportError:
    res['validator'] = 'not available'

# blueprint lint rules (Part 3.2 standards)
ops = [(p, m, o) for p, d in spec['paths'].items() for m, o in d.items()]
L = collections.Counter()
ids = collections.Counter(o['operationId'] for _, _, o in ops)
L['operations'] = len(ops)
L['paths'] = len(spec['paths'])
L['duplicate_operationIds'] = sum(1 for k, v in ids.items() if v > 1)
tmpl = collections.Counter(re.sub(r'\{[^}]+\}', '{}', p) for p in spec['paths'])
L['equivalent_templated_paths'] = sum(1 for v in tmpl.values() if v > 1)
for p, m, o in ops:
    names = [x['$ref'].split('/')[-1] if '$ref' in x else x['name'] for x in o.get('parameters', [])]
    if m == 'post' and 'IdempotencyKey' not in names and not re.match(r'^/(hooks|bff|scim|oauth)/', p) and '/webhooks/' not in p:
        if re.search(r'State|nonce|If-Match|Event ID|envelope|Yes', o.get('x-idempotency') or ''):
            L['post_with_documented_idempotency_alternative'] += 1
        else:
            L['post_without_idempotency_key'] += 1
    if m in ('put', 'patch', 'delete') and 'IfMatch' not in names:
        L['write_without_if_match'] += 1
    if not o.get('security'):
        L['no_security_declared'] += 1
    if o.get('security') == [{}] and not re.match(r'^/(bff|\.well-known|health|ready)|/public/|/api/v1/(health|ready)', p) and o.get('x-namespace', '').split('+')[0] not in ('public', 'bff', 'bff-web', 'bff-admin'):
        L['anonymous_non_public'] += 1
    for pn in re.findall(r'\{([^}]+)\}', p):
        if pn not in names:
            L['undeclared_path_param'] += 1
    if not re.match(r'^/[a-z0-9._{}/~-]*$', p.replace('Users', 'users').replace('Groups', 'groups').replace('Bulk', 'bulk').replace('ServiceProviderConfig', 'spc').replace('Schemas', 'schemas').replace('ResourceTypes', 'rt')):
        L['path_style_exceptions'] += 1
    if 'x-side-effect-class' in o and o['x-side-effect-class'] == 'X' and not re.search(r'[PD]', o.get('x-pdp') or ''):
        L['external_effect_without_pdp'] += 1
res['lint'] = dict(L)
res['by_version_prefix'] = dict(collections.Counter(('v2' if '/api/v2/' in p else 'v1' if '/api/v1/' in p else p.split('/')[1]) for p, _, _ in ops))
save_json('openapi_validation.json', res)
print(json.dumps(res, indent=1)[:3000])
