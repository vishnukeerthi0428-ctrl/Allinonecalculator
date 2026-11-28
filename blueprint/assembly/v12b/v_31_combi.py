"""V-31: combinatorial models for the Part 11.23 stories and tests (exhaustive where <= 64 combinations).
M1 Admin V2 screen rule: audience(4) x object grant(2) x UI state(5) = 40 (exhaustive).
M2 Mandate eligibility of investment actions: action class(10) x mandate state(2) x jurisdiction pack(2) = 40 (exhaustive).
M3 FX rate entry: boundary values (11, exhaustive list).
M4 Artifact integrity: artifact(7) x line endings(2) = 14 (exhaustive)."""
import itertools, json, os
from v_common import OUT

AUD = [('Operator', 'R14'), ('Tenant workspace', 'R02'), ('Portfolio (aggregate)', 'R01'), ('Automation ops', 'R13')]
GRANT = ['granted', 'not granted']
STATE = ['loading', 'empty', 'error', 'held', 'success']

def m1():
    rows = []
    for (a, r), g, s in itertools.product(AUD, GRANT, STATE):
        if g == 'not granted':
            exp = 'denied view, HTTP 403 from the API, no record data in DOM or bundle, audit event `access.denied`'
        elif a.startswith('Portfolio'):
            exp = {'loading': 'skeleton, no partial company rows', 'empty': 'aggregate empty state "No reconciled data for this period"',
                   'error': 'error state with retry and correlation ID, no data', 'held': 'held banner with reason code, aggregate only',
                   'success': 'aggregate KPIs only; drill-down requires object-level grant'}[s]
        else:
            exp = {'loading': 'skeleton with aria-busy, actions disabled', 'empty': 'empty state with permitted create action only',
                   'error': 'error state with retry and correlation ID; form values kept', 'held': 'held banner with reason code and owner; effect actions disabled',
                   'success': 'records of the granted scope; keyboard and compact-layout operable; audit on every write'}[s]
        rows.append((a, r, g, s, exp))
    return rows

ACT = ['offer issue', 'offering-tagged dispatch', 'closing', 'allotment reference', 'filing status', 'cap-table revision',
       'vote certification', 'KYC decision', 'external submission', 'non-offering IR message']
MST = ['Active', 'Revoked']
JUR = ['Approved', 'Not approved']

def m2():
    rows = []
    for a, m, j in itertools.product(ACT, MST, JUR):
        if a != 'non-offering IR message':
            exp = 'MANDATE_NOT_ALLOWED_SECURITIES; route to per-action L1 approval (two-person for closing and cap table)'
        elif m != 'Active':
            exp = 'MANDATE_INACTIVE; held, human approval required'
        elif j != 'Approved':
            exp = 'JURISDICTION_NOT_APPROVED; held, no dispatch'
        else:
            exp = 'allowed under mandate (L3) after PDP recheck: caps, consent, quiet hours, kill switch off'
        rows.append((a, m, j, exp))
    return rows

def m3():
    return [('0.012', 'accepted', 'stored as numeric(20,10) 0.0120000000'), ('0.5', 'accepted', 'stored'), ('1', 'accepted', 'stored'),
            ('83.2512', 'accepted', 'stored'), ('0.0000000001', 'accepted', 'smallest positive at 10 decimals'),
            ('0.00000000001', 'rejected', 'FX_RATE_PRECISION: more than 10 decimals'), ('0', 'rejected', 'FX_RATE_NOT_POSITIVE'),
            ('-0.5', 'rejected', 'FX_RATE_NOT_POSITIVE'), ('abc', 'rejected', 'FX_RATE_FORMAT'), ('1,000.5', 'rejected', 'FX_RATE_FORMAT (no grouping separators)'),
            ('9999999999.9999999999', 'accepted', 'upper bound numeric(20,10)')]

ART = [('commercial_website_desktop_V12.html', 'b9c3fa5cad677a9268d4124ad93679574579fe63dc8952d7d6fb5ba5236c60e2', '8ceb0c24518ad1bc1fa993c67d9f273f41c3aafc2cd358026d576c9d2c6b5bd7'),
       ('commercial_website_mobile_V12.html', '84c748e298ddb27104565667398b57ef24a33230365ed3f09f6b83aac95754b3', '2d1c49fb96541a0480e8134a32699ee2e47033c1c65f40a8a8a6c07614ecc9fe'),
       ('commercial_admin_desktop_V12.html', '2801359a3d598d51e5b5bc44737f712a8171252cb6f4379e66bb82d98f4dade0', 'ec90cde87bd6f2ed85bc5b4305bdb55b5622835c6ebcaf6233e758ff6cc99ad0'),
       ('commercial_admin_mobile_V12.html', '5995a670fd635d2795e479240e3bd5e633e1b1df601ef55c10faceb30a0a7e2c', 'cfd2bb40783bcc04e3e876227248fb4c170ee4f3d2f2685a22d448ccba02595f'),
       ('Sales_Marketing_Automation_BRD_V12.docx', '(not declared)', '7be408bf7d7450b4d6e58751a6190521819a3f72fde6387f8308de0fdeeceeec'),
       ('Sales_Marketing_Automation_FSD_V12.docx', '(not declared)', '0c90b8d6da68f15eb56e773905923131312cebd97d4ce1e5b4f290c69bd49aa3'),
       ('38 documents.zip (historical archive)', '6fa3a27bbd2f6af18fe179f5e1a1ff9500dbbfa3eb1e0963475cd4bc550b0de3', '6fa3a27bbd2f6af18fe179f5e1a1ff9500dbbfa3eb1e0963475cd4bc550b0de3')]

def m4():
    rows = []
    for (f, decl, recv), mode in itertools.product(ART, ['as received', 'LF-normalised']):
        if f.endswith('.docx'):
            exp = 'record as-received SHA-256 as the reference (no declared hash); binary, no normalisation'
        elif f.startswith('38'):
            exp = 'MATCH (binary, unchanged)'
        elif mode == 'as received':
            exp = 'MISMATCH (CRLF line endings added in transit); not a content change'
        else:
            exp = 'MATCH declared hash ' + decl[:12] + '…'
        rows.append((f, mode, exp))
    return rows

def main():
    d = dict(m1=m1(), m2=m2(), m3=m3(), m4=m4(), art=ART)
    json.dump(d, open(os.path.join(OUT, 'combi.json'), 'w'), indent=0)
    print({k: len(v) for k, v in d.items()})

if __name__ == '__main__':
    main()
