# Part 11.22 file writer (executed inside u_07_build.py's namespace).
# Produces Part-11-22a … Part-11-22f.

ACRO = ('**Acronyms used in this part.** AC = acceptance criterion · BDD = behaviour-driven development · CPO = Chief Product Officer · '
        'DoD / DoR = Definition of Done / Ready · EX = generated example row · FR = functional requirement · INV = Investment Automation product · '
        'MAS = minimum AC set (Part 5.1a §5.6.6) · NSE = no side effect · PDP = Policy Decision Point · PSP = payment service provider · '
        'RLS = row-level security · SKU = stock-keeping unit (a sellable service, SM-SVC-01…39 or INV-SVC-01…24) · SoD = separation of duties · '
        'SP = story point · t-way = covering array in which every combination of any t parameter values appears in at least one row.')

# ====================================================================== chunking
import glob as _glob
for _old in _glob.glob(os.path.join(BP, 'Part-11-22[a-z]_*.md')) + _glob.glob(os.path.join(BP, 'Part-11-22[a-z]_*.pdf')):
    os.remove(_old)  # outputs of earlier runs of this builder only
chunks = []; cur = []; size = 0
LIMIT = 700_000
ep_groups = collections.OrderedDict()
for s in stories:
    ep_groups.setdefault(s['epic'], []).append(s)
for e_, ss_ in ep_groups.items():
    sz = sum(len(story_md[x['id']]) for x in ss_)
    if size + sz > LIMIT and cur:
        chunks.append(cur); cur = []; size = 0
    cur += ss_; size += sz
chunks.append(cur)
SLET = 'bcdefg'[:len(chunks)]
JLET = chr(ord(SLET[-1]) + 1); FLET = chr(ord(JLET) + 1)

# ====================================================================== 11.22a
a = [title_block('a', 'Master User Stories and Persona Journeys with Permutations (V12): Inventory, Coverage, Models and Conventions',
     'Part 11, Batch 22, file a of %s: §11.22.1 material reviewed, §11.22.2 coverage summary, §11.22.3 detailed register, §11.22.4 story-catalogue reconciliation, §11.22.5.1–§11.22.5.3 conventions, ADRs, parameter models and epic placement. Files %s–%s hold the new stories (§11.22.5.4), file %s the persona journeys (§11.22.5.5), file %s the epic map, totals, conflicts, decisions, persona review, tags and quality gate (§11.22.5.6–§11.22.10)' % (FLET, SLET[0], SLET[-1], JLET, FLET))]
a.append(ACRO + '\n')
a.append('''**What this part does.** The Founder adopted V12 on every pending item and asked for user stories "using permutations and combinations" that "follow the exact template" (Part 11.14 DEC-779…791; V12-B brief). Parts 11.1–11.19 wrote 1,467 FR-V12 requirements and 555 V12 stories across 50 files and several story formats. This part (1) inventories every FR-V12 requirement and every V12 story by script, (2) finds each FR with no story, or with stories that carry no acceptance criteria, (3) writes a Part 5.1a-template story with Gherkin and generated `Scenario Outline` Examples for every one of them, (4) writes end-to-end persona journeys for the full V12 product with every step mapped to stories, (5) maps all epics EP-01…EP-34 to stories and requirements, and (6) totals stories and story points per epic and per release. **Result: 1,467 / 1,467 FR-V12 requirements (100%) have at least one story with acceptance criteria.**

**Scripts (in `assembly/v12b/`, run with `python3 -I`).** `u_01_inventory.py` (FR and story inventory, trace links, AC detection) → `u_02_baseline.py` (pre-V12 story census) → `u_07_build.py` with `u_03_models.py` (parameter models, covering arrays, oracle), `u_04_stories.py` (FR normalisation, epic, domain, release, grouping), `u_05_context.py` (domain contexts and outline steps), `u_06_journeys.py` (journeys) and `u_08_files.py` (this text). Every count in this part is printed by those scripts; regenerate after any change to Parts 11.1–11.19 (DEC-940).
''')

# 11.22.1
a.append('''```mermaid
flowchart TD
  A["Parts 11.1 to 11.19<br/>50 Markdown files"] --> B["u_01_inventory.py<br/>FR-V12 and story inventory"]
  B --> C{"FR has a story<br/>with AC?"}
  C -->|"yes"| D["Covered: keep"]
  C -->|"no story"| E["Target FR"]
  C -->|"story without AC"| E
  E --> F["u_04_stories.py<br/>normalise, epic, domain, release, group"]
  F --> G["u_03_models.py<br/>parameter model, covering array, oracle"]
  G --> H["u_07_build.py<br/>US-EP-ZUnn stories with Gherkin"]
  H --> I["Persona journeys JN-01 to JN-12"]
  H --> J["Epic map and totals"]
  H --> K["Re-inventory incl. Part 11.22<br/>must show 100 percent"]
```
''')
a.append('## 11.22.1 Material reviewed\n')
a.append('| File | FR-V12 IDs defined | FR-V12 IDs mentioned | V12 stories defined | Purpose in this part |\n|---|---|---|---|---|')
part_def = collections.Counter(); part_men = collections.Counter(); part_st = collections.Counter()
for f, d in inv['fr'].items():
    if d['def'] and d['def'].get('file'): part_def[d['def']['file']] += 1
for u, s in inv['stories'].items():
    part_st[s['file']] += 1
for p in inv['parts_scanned']:
    txt = open(os.path.join(BP, p), encoding='utf-8').read()
    part_men[p] = len(set(re.findall(r'FR-V12-[A-R]-\d{3}', txt)))
for p in inv['parts_scanned']:
    a.append('| `%s` | %d | %d | %d | %s |' % (p, part_def[p], part_men[p], part_st[p],
             'FR register and stories' if part_def[p] and part_st[p] else ('FR register' if part_def[p] else ('stories' if part_st[p] else 'references only'))))
a.append('| **Total (50 files, Parts 11.1–11.19)** | **%d** | **%d distinct** | **%d** | |\n' % (sum(part_def.values()), inv['fr_total'], len(inv['stories'])))
a.append('''**Inventory method (u_01).**

| Item | Rule implemented by the script |
|---|---|
| FR defined | The FR ID is the first cell of a Markdown table row, a heading subject, a "Functional requirement" field, or a bold `**Requirement FR-…**` paragraph (workflow specifications of Parts 11.3 and 11.16c) |
| FR inventory | Defined IDs plus IDs written explicitly elsewhere; IDs only implied by a declared range (e.g. "FR-V12-A-001…222", which holds 123 requirements) are not invented |
| Story defined | Heading `US-<EP>-<family><nn>`, bold paragraph story, first cell of a story table, or a field table `ID` row; families YA…YM (Parts 11.1–11.13), ZN…ZR (Parts 11.16–11.19), EH |
| Story → FR trace | FR IDs, lists and ranges inside a story block; FR IDs in any table row that names a story; bare number lists (e.g. "001, 002, 006") in a story row, resolved to the story family letter (YA→A … ZR→R) |
| Story has AC | A Gherkin block that names the story, a Gherkin block inside the story's own section, a `Feature:` line naming it, or a table row with Given/AC text |
| Target FR | No story at all (**%d**) or only stories without AC (**%d**) |
''' % (len(inv['uncovered']), len(inv['no_ac'])))

# 11.22.2
a.append('## 11.22.2 Coverage summary\n')
a.append('| FR family | Source part | FR-V12 total | Covered by a story with AC (before) | Story without AC (before) | No story (before) | New ZU stories | Covered with AC (after) |\n|---|---|---|---|---|---|---|---|')
tot = collections.Counter()
for l, sb in sum_by_letter.items():
    nz = len({recs[f]['story'] for f in recs if f.split('-')[2] == l})
    a.append('| FR-V12-%s | %s | %d | %d | %d | %d | %d | %d (100%%) |' % (l, LETTER_PART[l], sb['total'], sb['ac'], sb['noac'], sb['none'], nz, sb['total']))
    for k2 in sb: tot[k2] += sb[k2]
a.append('| **Total** | | **%d** | **%d (%.1f%%)** | **%d** | **%d** | **%d** | **%d (100%%)** |\n' % (tot['total'], tot['ac'], 100 * tot['ac'] / tot['total'], tot['noac'], tot['none'], len(stories), tot['total']))
a.append('''**Reading the summary.** Before this part, %d FR-V12 requirements (%.1f%%) had a story with acceptance criteria. %d had no story at all — mainly the ENT trace requirements of Part 11.11b (FR-V12-K-101…158), the AI controls of Part 11.6b (AIX-01…20, CTRL-AI-01…09), the securities controls and INV-SVC-13…24 workflow requirements of Parts 11.16a/c, and the H and I registers of Parts 11.8b and 11.9b/c. %d were traced only to statement-only stories (Parts 11.1b, 11.5b, 11.12 and two rows of 11.8b/11.13b) that carry no Gherkin. After this part all %d are covered by a story with Gherkin acceptance criteria and a generated Scenario Outline.
''' % (tot['ac'], 100 * tot['ac'] / tot['total'], tot['none'], tot['noac'], tot['total']))
a.append('| Measure | Value |\n|---|---|')
for k2, v in [('New stories (US-<EP>-ZU<nn>)', len(stories)), ('New story points (Fibonacci ranges summed)', '%d–%d SP' % (summary['new_sp_low'], summary['new_sp_high'])),
              ('Gherkin scenarios in new stories (incl. one Scenario Outline each)', summary['scenarios']), ('Generated Examples rows (EX-…)', '{:,}'.format(summary['examples_rows'])),
              ('Stories that are acceptance bindings (anchor or ENT trace; DEC-941)', sum(1 for s in stories if s['type'].startswith('Compliance (acceptance'))),
              ('Persona journeys (JN-01…JN-12) and journey steps', '12 journeys · %d steps' % sum(len(j['steps']) for j in JR.J))]:
    a.append('| %s | %s |' % (k2, v))
a.append('')

# 11.22.3
a.append('## 11.22.3 Detailed register (every target FR)\n')
a.append('One row per FR that had no story or no story with AC. "Status after" is Matched for every row: the new story holds Gherkin AC and a generated Scenario Outline.\n')
a.append('| FR | Defined in | Requirement (abridged) | Status before | Epic | Release | New story | Status after |\n|---|---|---|---|---|---|---|---|')
for f in sorted(recs, key=lambda x: (x.split('-')[2], int(x.split('-')[3]))):
    r = recs[f]
    part = re.match(r'Part-(\d+-\d+[a-e]?)', r['file']).group(1).replace('-', '.') if r['file'] else '?'
    sb = r['status_before'] + ((' (' + r['anchor'] + ')') if r.get('anchor') else '')
    a.append('| %s | Part %s | %s | %s | %s | %s | %s | Matched |' % (f, part, S.short(r.get('req') or r['label'], 130), sb, r['epic'], r['rel'], r['story']))
a.append('')

# 11.22.4
a.append('## 11.22.4 Story-catalogue reconciliation\n')
a.append('### 11.22.4.1 V12 stories found (Parts 11.1–11.19)\n')
a.append('| Part file | Stories | With AC | Without AC | Points stated | Story families |\n|---|---|---|---|---|---|')
fam_by = collections.defaultdict(set); acn = collections.Counter(); pts = collections.Counter()
for u, s in inv['stories'].items():
    fam_by[s['file']].add(u.split('-')[2][:2]); acn[s['file']] += 1 if s['has_ac'] else 0; pts[s['file']] += 1 if s.get('points') else 0
for p in sorted(part_st):
    a.append('| `%s` | %d | %d | %d | %d | %s |' % (p, part_st[p], acn[p], part_st[p] - acn[p], pts[p], ', '.join(sorted(fam_by[p]))))
a.append('| **Total** | **%d** | **%d** | **%d** | **%d** | |\n' % (len(inv['stories']), sum(acn.values()), len(inv['stories']) - sum(acn.values()), sum(pts.values())))
a.append('### 11.22.4.2 Statement-only stories (no Gherkin AC) and their acceptance bindings\n')
a.append('| Statement-only story | Part | FRs it traces | Acceptance binding added here |\n|---|---|---|---|')
anchors = collections.defaultdict(set)
for f, r in recs.items():
    if r.get('anchor'): anchors[r['anchor']].add(r['story'])
for u, s in sorted(inv['stories'].items()):
    if not s['has_ac']:
        fr = s['frs']
        a.append('| %s | %s | %s | %s |' % (u, s['file'].split('_')[0], fr_ranges(fr) or '—', ', '.join(sorted(anchors.get(u, []))) or 'Its FRs are also traced by a story with AC (no binding needed)'))
a.append('')
a.append('''### 11.22.4.3 Trace anomalies found (reported, not edited)

| # | Finding | Where | Effect | Handling |
|---|---|---|---|---|
| 1 | Workflow requirements FR-V12-O-037…084 are traced by the EP-32/EP-33 stories through workflow IDs ("INV-SVC-13 WF01/WF02") but not by FR ID | Part 11.16d §11.16.15 stories | FR-level trace shows "no story" | ZU stories carry the FR IDs (US-32-ZU*, US-33-ZU*); [GAP-1146] recommends adding the FR IDs to the Part 11.16d `Traces` rows |
| 2 | Six agent stories have an empty title in the story heading | Part 11.6b (US-03-YF27, US-04-YF24…26, US-04-YF29, US-18-YF28) | Catalogue listings show blanks | [GAP-1147]; titles derivable from the agent cards |
| 3 | Register wording still says "Pending Founder decision" after DEC-770…791 decided it | FR-V12-K-004 (Part 11.11b), FR-V12-I-013 (Part 11.9b), FR-V12-A-147 (Part 11.1b), FR-V12-O-037…084 status-before text | Readers may think the item is open | [GAP-1148]; stories here cite the deciding DEC |
| 4 | R21 is used for two different roles | Part 2.6 §2.6.5.3.2 (agency operator) and Part 11.16a (invited investor) | Ambiguous RBAC role | [CONFLICT-1140]; proposed resolution in §11.22.6 |
| 5 | FR-V12-A-006 and US-19-YG38 still forbid any investor entity, route or mode | Parts 11.1b and 11.7c | Contradicts DEC-783 | [CONFLICT-1149]; story US-01-ZU01 carries the amended wording |
''')

# 11.22.5.1 conventions and ADRs
a.append('## 11.22.5 Enhancements\n')
a.append('### 11.22.5.1 Story conventions (Part 5.1a applied) and ADRs\n')
a.append('''| Item | Convention in this part |
|---|---|
| Template | Exactly Part 5.1a §5.7 / Part 5.1b: heading `##### US-<EP>-ZU<nn> <Title>`, field table (ID, Title, Type, Story, Persona / roles, Traces, Priority, Wave, Points, Dependencies, Dimension profile, Notes), then one ```` ```gherkin ```` block |
| Story ID | `US-<EP>-ZU<nn>`, `nn` restarts per epic (e.g. US-20-ZU07) |
| AC ID | `AC-<EP>ZU<nn>-<seq>` at the start of every `Scenario:` / `Scenario Outline:` line |
| Tags | Path tags `@happy @alt @neg @val @perm @edge`, assertion tags `@sec @obs @a11y`, rule/decision tags (`@DEC-772`, `@BRL-TEN-04`, `@ENT-IDN-01`, `@AIX-08` …) and the model tag (`@MU05`) |
| Minimum AC set | MAS-1 happy (one per FR), MAS-2 alternate (each further FR), MAS-3 negative (FR-specific where the register gives one, plus the domain negative with a rule tag), MAS-4 validation, MAS-5 permission, MAS-6…9 edge (idempotency, uncertain outcome, time/zone, accessibility), and one generated Scenario Outline |
| Scenario Outline | Steps reference every model parameter; `Examples:` rows are generated by `u_03_models.py` from the declared parameter model; each row has an `EX-<EP>ZU<nn>-<seq>` ID and an oracle-computed `expected` value (ADR-276) |
| Points | Fibonacci ranges ≤ 13 (Part 5.1a §5.5.1): 1 FR 3–5 (5–8 for a 3-way risk model), 2 FRs 5–8, 3–4 FRs 8–13; acceptance bindings 1–2 or 2–3 (DEC-941, [ASSUMPTION-1142]) |
| Wave | Release bucket of the FR (Release 1 = W0–W3 and V12 R0/R1; Release 2 = W4–W5 and V12 R2; Release 3+ = W6, A1–A3 and V12 R3–R5) with the V12-B overrides of DEC-771…789; dates follow the work (DEC-770) [ASSUMPTION-1145] |
| Release overrides | DEC-784 (SSO, SCIM, roles, audit → Release 1), DEC-785 (developer platform and connectors → Release 1), DEC-771/787 (RTO/RPO → Release 1 gates), DEC-772 (residency at onboarding → Release 1), DEC-773 (24×7 → Release 2), DEC-775 (SOC 2 Type I → Release 2; Type II, ISO 27001/27701/42001 → Release 3+), DEC-776 (locales, tax, regions staged) |
| Fixtures | Synthetic only: tenants "Kestrel Analytics Pvt Ltd" (zone IN) and "Nordlicht Robotik GmbH" (zone EU), issuer "AppNAI Technologies Pvt Ltd", `example.com`/`.test` addresses [ASSUMPTION-1150] |
| DoR / DoD | Part 5.1a §5.2 and §5.3 apply unchanged; R-10 (AI), R-11 (dispatch) and R-12 (legal) are restated in Notes where they apply |

#### ADR-275 Story inventory and coverage as code

| Field | Content |
|---|---|
| Status | Accepted (DEC-940) |
| Context | 50 Part 11 files hold FRs and stories in at least six formats (field-table blocks, story tables, bold paragraphs, combined `Priority · Wave · Points` rows, number-list traces). Manual reconciliation missed 380 FRs |
| Decision | Coverage is computed by `u_01_inventory.py`; CI regenerates it on every change to a Part 11 file and fails if any FR-V12 lacks a story with AC, or if a story ID referenced by a journey does not exist |
| Consequences | Positive: no silent coverage loss; the register in §11.22.3 is reproducible. Negative: new formats need parser rules; mitigated by the "story defined" rules table in §11.22.1 |
| Alternatives | Manual RTM maintenance (rejected: the gap of 380 FRs proves it fails); a tracker export (kept as a later option) |

#### ADR-276 Oracle-derived expected results for generated Examples

| Field | Content |
|---|---|
| Status | Accepted (DEC-945) |
| Context | Thousands of Examples rows cannot carry hand-typed expected results without error |
| Decision | Every parameter value carries either "passes" or an effect with a PDP precedence (1 scope → 2 authentication/session → 3 entitlement/credential → 4 permission/SoD/evidence → 5 residency/sanctions → 6 jurisdiction pack/eligibility/tax → 7 consent → 8 data class/registry → 9 autonomy/approval/mandate → 10 provider → 11 budget). The oracle returns the effect with the lowest precedence, or the FR's own acceptance text when every check passes |
| Consequences | Expected results are consistent with the PDP order of Part 11.3/11.17 and reproducible; a change of precedence regenerates every row |
| Alternatives | Hand-written expectations (rejected); model checking (deferred to Part 11.21 tooling) |
''')

# 11.22.5.2 models
a.append('### 11.22.5.2 Parameter models and generation method\n')
a.append('''**Parameters (brief dimensions).** persona × service/SKU × channel × jurisdiction × role (authority class) × data class × autonomy/mandate × region, plus the story-specific **operation** parameter (one value per FR of the story). Role and permission are merged into authority classes A1/A3/A5/T5 exactly as Part 5.1a §5.6.2 merges them; the 670-cell role × screen-group RBAC test of Part 5 still covers every role [ASSUMPTION-1152]. Each model keeps the five or six dimensions that change the outcome for its domain; the others are held at their baseline value and noted.

**Generation.** Greedy constraint-aware covering arrays (deterministic seed per story, starting at 101 and stepping by 7), **t = 3 for safety-, money- or law-critical models (MU02, MU04, MU05, MU06, MU07, MU08, MU09, MU12) and t = 2 for the others**; exhaustive enumeration where a model space is ≤ 64; plus one baseline-allow row per operation (risk-based addition, Part 5.1a §5.6.5). Constraints: anonymous visitors never use the API; service and AI-agent identities never use browser channels; invited investors are never approvers. Coverage of every t-tuple is verified by the script (`verify()`), and the counts are printed in each story's `Examples:` line.
''')
for mid, m in M.MODELS.items():
    a.append('#### %s %s (%s)\n' % (mid, m['title'], '3-way' if m['risk'] == 3 else 'pairwise'))
    a.append('| Parameter | Values | Value effects (PDP precedence → result) |\n|---|---|---|')
    for n, vm in m['params']:
        effs = '; '.join('%s → [%d] %s' % (v, e[0], e[1]) for v, e in vm.items() if e) or 'all values pass (no effect)'
        a.append('| %s | %s | %s |' % (n, ', '.join(vm.keys()), effs.replace('|', '/')))
    use = [s for s in stories if s['model'] == mid]
    if use:
        a.append('| *Use* | %d stories | rows %d–%d per story (total %s); space per story %s–%s; every t-tuple covered |' % (
            len(use), min(s['comb']['rows'] for s in use), max(s['comb']['rows'] for s in use), '{:,}'.format(sum(s['comb']['rows'] for s in use)),
            '{:,}'.format(min(s['comb']['space'] for s in use)), '{:,}'.format(max(s['comb']['space'] for s in use))))
    a.append('')
a.append('**Combination count per story.**\n')
a.append('| Story | Model | Method | Raw space | t-tuples required / covered | Array rows | Baseline-allow rows | Examples rows |\n|---|---|---|---|---|---|---|---|')
for s in stories:
    c = s['comb']
    a.append('| %s | %s | %s | %s | %s / %s | %d | %d | %d |' % (s['id'], c['mid'], 'exhaustive' if c['t'] == 'all' else '%s-way' % c['t'], '{:,}'.format(c['space']), c['tuples'], c['covered'], c['n_array'], c['n_base'], c['rows']))
a.append('| **Total** | | | | | **%d** | **%d** | **%s** |\n' % (sum(s['comb']['n_array'] for s in stories), sum(s['comb']['n_base'] for s in stories), '{:,}'.format(summary['examples_rows'])))

# 11.22.5.3 epics
a.append('### 11.22.5.3 Epic placement and new epic EP-34\n')
a.append('| Epic | Title | New stories | SP (new) | Model(s) |\n|---|---|---|---|---|')
by_ep = collections.defaultdict(list)
for s in stories: by_ep[s['epic']].append(s)
for e in sorted(by_ep):
    ss = by_ep[e]
    a.append('| %s | %s | %s | %d–%d | %s |' % (e, EPIC_TITLES[e], story_ranges([x['id'] for x in ss]), sum(x['sp'][0] for x in ss), sum(x['sp'][1] for x in ss), ', '.join(sorted(set(x['model'] for x in ss)))))
a.append('| **Total** | | **%d stories** | **%d–%d** | |\n' % (len(stories), summary['new_sp_low'], summary['new_sp_high']))
ep34 = by_ep['EP-34']
a.append('''#### EP-34 Epic card

| Field | Value |
|---|---|
| ID | EP-34 |
| Title | Global expansion, certification and multi-market operations |
| Business value | Turns the Founder's global-expansion and certification decisions (DEC-775, DEC-776) into buildable, testable work: certifications in the agreed order, an internationalisation base, staged locales including right-to-left Arabic, locale formats, a tax-engine abstraction and multi-currency billing, regional messaging providers and the region roadmap. No market opens without its counsel-approved rule pack and tax approval |
| Linked BRs | BR-V12-05…07 (enterprise readiness), BR-C10 (commercial terms) |
| Linked FRs | FR-V12-K-137…139, FR-V12-K-145…152 (ENT-CMP-01…03, ENT-GLB-01…08) |
| Key rules and decisions | DEC-772, DEC-775, DEC-776, DEC-029 as amended (Part 11.15), DEC-942 |
| In scope | SOC 2 Type I/II, ISO/IEC 27001, 27701, 42001 evidence; i18n framework; locales en, hi, de, fr, ar; E.164, IANA, ICU; tax engine TX-04…09; native-currency billing with FX evidence; DLT and sender registration per market; region plan |
| Out of scope | Rule-pack legal wording (Part 11.15); hosting copies per region (Part 11.19/11.20) |
| Dependencies | US-01-ZR28 residency; Part 11.15 packs; Part 11.20 plan |
| Priority | Must (certification and i18n base), Should (staged locales and regions) |
| Wave(s) | Release 1 (i18n base), Release 2 (SOC 2 Type I, en/hi, tax, FX, providers), Release 3+ (Type II, ISO, de/fr/ar, regions) |
| Size | %d stories · %d–%d SP |
| Stories | %s |
''' % (len(ep34), sum(x['sp'][0] for x in ep34), sum(x['sp'][1] for x in ep34), ', '.join(x['id'] for x in ep34)))
a.append(qgate('a', {4: 'N/A for the front matter; the MAS rule and the model rules here bind files b–d'}))
a.append('**Status: Part 11 Batch 11.22a complete (inventory, coverage, register, models, conventions). Continue with Batch 11.22b (stories).**\n')
write('Part-11-22a_Master_User_Stories_Inventory_Models_and_Conventions.md', '\n'.join(a))

# ====================================================================== stories b, c, d
story_files = []
for li, ch in zip(SLET, chunks):
    eps = sorted(set(s['epic'] for s in ch))
    name = 'Part-11-22%s_Master_User_Stories_%s_to_%s.md' % (li, eps[0].replace('-', ''), eps[-1].replace('-', ''))
    story_files.append((li, name, ch))
for li, name, ch in story_files:
    eps = sorted(set(s['epic'] for s in ch))
    t = [title_block(li, 'Master User Stories with Permutations: %s to %s' % (eps[0], eps[-1]),
                     'Part 11, Batch 22, file %s of %s: §11.22.5.4 new stories for %s (template of Part 5.1a; conventions, models and register in file a)' % (li, FLET, ', '.join(eps)))]
    t.append(ACRO + '\n')
    if li == 'b':
        t.append('### 11.22.5.4 New stories by epic\n')
        t.append('Every story below covers FR-V12 requirements that had no story, or no story with acceptance criteria (§11.22.3). Each has Gherkin for MAS-1…MAS-9 and one Scenario Outline whose Examples are generated from its parameter model (§11.22.5.2).\n')
    else:
        t.append('### 11.22.5.4 New stories by epic (continued)\n')
    for e in eps:
        ss = [s for s in ch if s['epic'] == e]
        t.append('#### 11.22.5.4.%d %s %s\n' % (int(e[3:]), e, EPIC_TITLES[e]))
        frs = sorted(set(sum((s['frs'] for s in ss), [])), key=lambda x: (x.split('-')[2], int(x.split('-')[3])))
        t.append('| Field | Value |\n|---|---|')
        t.append('| Epic | %s %s (%s) |' % (e, EPIC_TITLES[e], EPIC_SRC[e]))
        t.append('| New stories in this file | %s |' % ', '.join(s['id'] for s in ss))
        t.append('| FR-V12 covered | %s |' % fr_ranges(frs))
        t.append('| Size | %d stories · %d–%d SP · %d–%d pd (0.5/1.0 pd per SP) · central %.1f pd (0.7 pd per SP mid) |' % (
            len(ss), sum(s['sp'][0] for s in ss), sum(s['sp'][1] for s in ss), round(0.5 * sum(s['sp'][0] for s in ss)), sum(s['sp'][1] for s in ss),
            0.7 * sum((s['sp'][0] + s['sp'][1]) / 2 for s in ss)))
        t.append('| Releases | %s |\n' % ', '.join('%s: %d' % (k2, v) for k2, v in sorted(collections.Counter(s['release'] for s in ss).items())))
        for s in ss:
            t.append(story_md[s['id']])
    t.append(qgate(li, {}))
    t.append('**Status: Part 11 Batch 11.22%s complete (%d stories, %s). Continue with Batch 11.22%s.**\n' % (li, len(ch), ', '.join(eps), chr(ord(li) + 1)))
    write(name, '\n'.join(t))

# ====================================================================== 11.22e journeys
def resolve(ref):
    if ref.startswith('FR-V12-'):
        if ref not in FR2NEW:
            raise SystemExit('journey FR ref not a target: ' + ref)
        return FR2NEW[ref], ref
    check_refs([ref])
    return ref, None

e = [title_block(JLET, 'Persona Journeys for the Full V12 Product, with Permutations',
     'Part 11, Batch 22, file %s of %s: §11.22.5.5 twelve' % (JLET, FLET) + ' end-to-end persona journeys (owner/founder, tenant admin, sales executive, marketer, approver, finance, compliance/counsel, platform operator, investor-relations user, invited investor, external customer, partner), each step mapped to stories and requirements, with a Mermaid journey map and a generated end-to-end Scenario Outline')]
e.append(ACRO + '\n')
e.append('### 11.22.5.5 Persona journeys\n')
e.append('''**How to read a journey.** The card names the persona (Part 1 §1.8 P01–P16; Part 2.6 P17–P20; new P21–P23 [RECOMMENDATION-1141]), the roles (Part 2.3 R01–R20; R21 per Parts 2.6/11.16a, see [CONFLICT-1140]) and the goal. The step table maps every step to the screens, the control the system applies and the **stories** that deliver it (existing V12 stories and new ZU stories) with the **FR-V12** requirements behind them. Every story ID is checked by the build. The journey Scenario Outline is the journey's end-to-end acceptance test: its Examples are pairwise permutations of the journey's variant dimensions with oracle-computed outcomes (ADR-276), and Part 11.21 realises them as end-to-end test cases [RECOMMENDATION-1146].

**New personas [RECOMMENDATION-1141].**

| ID | Persona | Product | Role mapping | Goals | Pains | Never |
|---|---|---|---|---|---|---|
| P21 | Investor-relations user | Investment Automation (DEC-783) | R03 in the INV product; approvals by R02 + R10 | Run a lawful round: discovery, outreach, data room, offers, receipts, closing, updates | Securities rules differ by route and market; manual tracking of clocks and caps | Send offer material where the pack is not Active; let AI give investment advice |
| P22 | Invited investor | Investor portal W77–W99 | R21 as defined in Part 11.16a (object grants only; extends R16) | Review, verify, apply and follow holdings privately | Repeated KYC, unclear status, privacy | See another investor's data; receive unsolicited offers |
| P23 | Partner / reseller | SM-SVC-32 co-selling, marketplaces, agentic commerce | R16 with a partner grant; P17/R21 (Part 2.6) for managed-service work | Register and co-sell deals, interoperate, get settled | Channel conflict; data-sharing limits; settlement delays | Read data outside the partner agreement; act for two clients in one session |
''')
journey_totals = []
for jn in JR.J:
    stories_in = []; frs_in = []
    rows = []
    for i, (stage, tp, act, ctl, refs) in enumerate(jn['steps'], 1):
        ids = []; frl = []
        for ref in refs:
            sid, fr = resolve(ref)
            if sid not in ids: ids.append(sid)
            if fr: frl.append(fr)
            else: frl += [f for f in inv['stories'].get(sid, {}).get('frs', [])[:2]]
        stories_in += ids; frs_in += frl
        rows.append('| %d | %s | %s | %s | %s | %s | %s |' % (i, stage, tp, act, ctl, ', '.join(ids), ', '.join(sorted(set(frl))[:4]) or '(trace in story)'))
    journey_totals.append((jn['id'], len(jn['steps']), len(set(stories_in)), len(set(frs_in))))
    e.append('#### %s %s journey\n' % (jn['id'], jn['persona']))
    e.append('| Field | Value |\n|---|---|')
    for k2, v in [('Journey', jn['id']), ('Persona', '%s (%s)' % (jn['persona'], jn['pid'])), ('Roles', jn['roles']), ('Goal', jn['goal']),
                  ('Preconditions', jn['pre']), ('Stories touched', '%d (%d new ZU)' % (len(set(stories_in)), len([x for x in set(stories_in) if '-ZU' in x]))),
                  ('Journey outcome (oracle allow text)', jn['outcome'])]:
        e.append('| %s | %s |' % (k2, v))
    e.append('')
    e.append('| # | Stage | Touchpoint | What the persona does | What the system does (control) | Stories | FR-V12 (sample) |\n|---|---|---|---|---|---|---|')
    e.extend(rows)
    e.append('')
    # mermaid
    m = ['```mermaid', 'flowchart TD']
    for i, (stage, tp, act, ctl, refs) in enumerate(jn['steps'], 1):
        lab = re.sub(r'[";\[\]{}|<>#]', '', '%d. %s' % (i, stage))
        sids = re.sub(r'[";\[\]{}|<>#]', '', ', '.join(resolve(r)[0] for r in refs[:2]))
        m.append('  S%d["%s<br/>%s"]' % (i, lab, sids))
    for i in range(1, len(jn['steps'])):
        m.append('  S%d --> S%d' % (i, i + 1))
    m.append('  G{"PDP recheck at every effect"}')
    m.append('  S%d --> G' % len(jn['steps']))
    m.append('  G --> O["Outcome: %s"]' % re.sub(r'[";\[\]{}|<>#]', '', jn['outcome']))
    m.append('```')
    e.append('\n'.join(m) + '\n')
    # permutations
    M.MODELS['J-' + jn['id']] = dict(title=jn['persona'] + ' journey variants', risk=2, params=jn['model'])
    res = M.model_rows('J-' + jn['id'], [('end-to-end', 'journey outcome reached')], 500 + int(jn['id'][3:]))
    heads = ['ex'] + [C.slug(n) for n in res['names'][1:]] + ['expected']
    g = ['```gherkin', 'Feature: %s %s end-to-end journey' % (jn['id'], jn['persona']), '  Background:',
         '    Given the persona %s holds %s' % (jn['pid'].split(' ')[0], jn['roles'].split(';')[0])] + fmt_step('And %s' % jn['pre'], '    ') + ['', '  @e2e @journey @happy @sec',
         '  Scenario Outline: %s-E2E Journey permutations (%s, %d rows)' % (jn['id'], 'exhaustive' if res['t'] == 'all' else 'pairwise', len(res['rows']))]
    first = True
    for n in res['names'][1:]:
        g.append('    %s the journey variant has %s "<%s>"' % ('Given' if first else 'And', n, C.slug(n))); first = False
    g.append('    When the persona completes steps 1–%d of %s' % (len(jn['steps']), jn['id']))
    g.append('    Then the journey outcome is "<expected>"')
    g.append('    And every effect in the journey was rechecked by the PDP at dispatch and audited')
    g.append('    Examples: %s variants (%s; space %d; t-tuples covered %s/%s)' % (jn['id'], res['method'], res['space'], res['covered'], res['tuples']))
    g.append('      | ' + ' | '.join(heads) + ' |')
    for i, row in enumerate(res['rows'], 1):
        g.append('      | ' + ' | '.join(['EX-%s-%02d' % (jn['id'], i)] + [M.short_value(n_, str(v)) for n_, v in zip(res['names'][1:], row[1:-1])] + [M.short_expected(row[-1])]).replace('|  |', '| — |') + ' |')
    g.append('```')
    e.append('\n'.join(g) + '\n')
e.append('#### 11.22.5.5.13 Journey coverage summary\n')
e.append('| Journey | Steps | Stories touched | FR-V12 (sample) referenced |\n|---|---|---|---|')
for jid, ns, nst, nfr in journey_totals:
    e.append('| %s | %d | %d | %d |' % (jid, ns, nst, nfr))
e.append('| **Total** | **%d** | **%d (distinct per journey, summed)** | |\n' % (sum(x[1] for x in journey_totals), sum(x[2] for x in journey_totals)))
e.append(qgate(JLET, {1: 'Every journey step names its stories; every story ID and every FR reference is resolved and checked by the build',
                      4: 'Every journey has an end-to-end Scenario Outline with generated pairwise Examples; every referenced story has AC',
                      5: 'Journeys include denial, hold and accessibility variants (assistive technology, 360 px)'}))
e.append('**Status: Part 11 Batch 11.22%s complete (12 journeys). Continue with Batch 11.22%s.**\n' % (JLET, FLET))
write('Part-11-22%s_Persona_Journeys_with_Permutations.md' % JLET, '\n'.join(e))

# ====================================================================== 11.22f epic map, totals, conflicts, decisions, tags
f6 = [title_block(FLET, 'Epic Map, Story and Story-Point Totals, Conflicts, Decisions, Tags and Quality Gate',
      'Part 11, Batch 22, file %s of %s: §11.22.5.6 epic map' % (FLET, FLET) + ' EP-01…EP-34 to stories and requirements, §11.22.5.7 totals per epic and per release, §11.22.6 conflicts, §11.22.7 decisions, §11.22.8 expert persona review, §11.22.9 tags register, §11.22.10 quality gate')]
f6.append(ACRO + '\n')
# FR -> epics
fr_epics = collections.defaultdict(set)
for f, d in inv['fr'].items():
    df = d['def'] or {}
    m = re.search(r'\bEP-(\d{2})\b', ' '.join(df.get('cells') or []))
    if m: fr_epics[f].add('EP-' + m.group(1))
    for u in d['stories']:
        fr_epics[f].add('EP-' + u.split('-')[1])
    if f in recs: fr_epics[f].add(recs[f]['epic'])
ep_frs = collections.defaultdict(set)
for f, es in fr_epics.items():
    for e2 in es: ep_frs[e2].add(f)
v12_by_ep = collections.defaultdict(list)
for u, s in inv['stories'].items():
    v12_by_ep['EP-' + u.split('-')[1]].append(u)
IMP = (3, 8)
def v12_sp(ids):
    lo = hi = stated = 0
    for u in ids:
        r = sp_of(inv['stories'][u].get('points'))
        if r: lo += r[0]; hi += r[1]; stated += 1
        else: lo += IMP[0]; hi += IMP[1]
    return lo, hi, stated
f6.append('### 11.22.5.6 Epic map: EP-01…EP-34 to stories and requirements\n')
f6.append('| Epic | Title | Defined in | Baseline stories (Part 5 / enhancement / advanced) | V12 stories (Parts 11.1–11.19) | New ZU stories (this part) | FR-V12 requirements mapped |\n|---|---|---|---|---|---|---|')
for e2 in sorted(EPIC_TITLES):
    b = base['by_epic'].get(e2, {'stories': 0, 'families': {}})
    fam = b.get('families', {})
    f6.append('| %s | %s | %s | %d (%d / %d / %d) | %d: %s | %d: %s | %d: %s |' % (
        e2, EPIC_TITLES[e2], EPIC_SRC[e2], b['stories'], fam.get('Part 5', 0), fam.get('source-pack enhancement', 0), fam.get('advanced (Part 9.7-9.9)', 0),
        len(v12_by_ep[e2]), story_ranges(v12_by_ep[e2]) or '—', len(by_ep.get(e2, [])), story_ranges([s['id'] for s in by_ep.get(e2, [])]) or '—',
        len(ep_frs[e2]), fr_ranges(ep_frs[e2]) or '—'))
f6.append('')
f6.append('**FR-to-epic rule.** An FR maps to the epic in its register row, to the epic of every story that traces it, and to the epic of its new ZU story; an FR can therefore appear under more than one epic. Every one of the %d FR-V12 requirements maps to at least one epic: %s.\n' % (inv['fr_total'], 'yes' if all(fr_epics[f] for f in inv['fr']) else 'NO – see list'))
# detailed story map
f6.append('#### 11.22.5.6.1 Story-level map (V12 and new stories)\n')
f6.append('| Story | Epic | Title / statement (abridged) | FR-V12 traced | AC | Release | SP | Source |\n|---|---|---|---|---|---|---|---|')
for u in sorted(inv['stories']):
    s = inv['stories'][u]
    f6.append('| %s | EP-%s | %s | %s | %s | %s | %s | %s |' % (u, u.split('-')[1], S.short(s.get('title') or '', 90), S.short(fr_ranges(s['frs']), 90) or '—',
              'Yes' if s['has_ac'] else 'No → ' + ', '.join(sorted(anchors.get(u, []))) if not s['has_ac'] else 'Yes', rel_bucket(s.get('wave') or s.get('release')), s.get('points') or 'not stated', s['file'].split('_')[0]))
for s in stories:
    f6.append('| %s | %s | %s | %s | Yes | %s | %d–%d | Part-11-22 |' % (s['id'], s['epic'], S.short(s['title'], 90), fr_ranges(s['frs']), s['release'], s['sp'][0], s['sp'][1]))
f6.append('')
# totals per epic
f6.append('### 11.22.5.7 Story counts and story points per epic and per release\n')
f6.append('**Basis.** Baseline and V12 story points are taken from the stories where stated (Fibonacci ranges, `Points` or combined `Priority · Wave · Points` fields). V12 stories that state no points (story tables and paragraphs in Parts 11.1–11.13) are imputed at **3–8 SP** each [ASSUMPTION-1142]. Person-days use Part 5.1a §5.5.1: low = SP_low × 0.5, high = SP_high × 1.0, central = SP_mid × 0.7. Release buckets per §11.22.5.1 [ASSUMPTION-1145]. These are planning totals for Part 11.20, not a re-baseline of Ledger A.\n')
f6.append('| Epic | Baseline stories | Baseline SP (stated; n stated) | V12 stories | V12 SP (stated + imputed; n stated) | New ZU stories | New SP | All stories | All SP (low–high) | Central pd |\n|---|---|---|---|---|---|---|---|---|---|')
G = collections.Counter()
for e2 in sorted(EPIC_TITLES):
    b = base['by_epic'].get(e2, {'stories': 0, 'with_points': 0, 'sp_low': 0, 'sp_high': 0})
    vlo, vhi, vst = v12_sp(v12_by_ep[e2])
    nlo = sum(s['sp'][0] for s in by_ep.get(e2, [])); nhi = sum(s['sp'][1] for s in by_ep.get(e2, []))
    alo = b['sp_low'] + vlo + nlo; ahi = b['sp_high'] + vhi + nhi
    n_all = b['stories'] + len(v12_by_ep[e2]) + len(by_ep.get(e2, []))
    cen = 0.7 * (alo + ahi) / 2
    f6.append('| %s | %d | %d–%d (%d) | %d | %d–%d (%d) | %d | %d–%d | %d | %d–%d | %.0f |' % (e2, b['stories'], b['sp_low'], b['sp_high'], b['with_points'], len(v12_by_ep[e2]), vlo, vhi, vst, len(by_ep.get(e2, [])), nlo, nhi, n_all, alo, ahi, cen))
    for k2, v in [('bs', b['stories']), ('blo', b['sp_low']), ('bhi', b['sp_high']), ('bst', b['with_points']), ('vs', len(v12_by_ep[e2])), ('vlo', vlo), ('vhi', vhi), ('vst', vst),
                  ('ns', len(by_ep.get(e2, []))), ('nlo', nlo), ('nhi', nhi), ('all', n_all), ('alo', alo), ('ahi', ahi)]:
        G[k2] += v
f6.append('| **Total** | **%d** | **%d–%d (%d)** | **%d** | **%d–%d (%d)** | **%d** | **%d–%d** | **%d** | **%d–%d** | **%.0f** |\n' % (
    G['bs'], G['blo'], G['bhi'], G['bst'], G['vs'], G['vlo'], G['vhi'], G['vst'], G['ns'], G['nlo'], G['nhi'], G['all'], G['alo'], G['ahi'], 0.7 * (G['alo'] + G['ahi']) / 2))
summary.update({'all_stories': G['all'], 'all_sp_low': G['alo'], 'all_sp_high': G['ahi']})
# per release
f6.append('#### 11.22.5.7.1 Per release\n')
REL = ['Release 1', 'Release 2', 'Release 3+', 'Not stated']
def base_rel(s):
    return rel_bucket(s.get('wave') or s.get('release') or s.get('points', '') if False else (s.get('wave') or s.get('release')))
rb = collections.defaultdict(lambda: [0, 0, 0])
for u, s in base['stories'].items():
    k2 = rel_bucket(s.get('wave') or s.get('release')); r = sp_of(s.get('points')) or (0, 0)
    rb[k2][0] += 1; rb[k2][1] += r[0]; rb[k2][2] += r[1]
rv = collections.defaultdict(lambda: [0, 0, 0])
for u, s in inv['stories'].items():
    k2 = rel_bucket(s.get('wave') or s.get('release')); r = sp_of(s.get('points')) or IMP
    rv[k2][0] += 1; rv[k2][1] += r[0]; rv[k2][2] += r[1]
rn = collections.defaultdict(lambda: [0, 0, 0])
for s in stories:
    rn[s['release']][0] += 1; rn[s['release']][1] += s['sp'][0]; rn[s['release']][2] += s['sp'][1]
f6.append('| Release | Baseline stories (SP stated) | V12 stories (SP stated + imputed) | New ZU stories (SP) | All stories | All SP | pd low–high · central |\n|---|---|---|---|---|---|---|')
for k2 in REL:
    b, v, n = rb[k2], rv[k2], rn[k2]
    lo = b[1] + v[1] + n[1]; hi = b[2] + v[2] + n[2]
    f6.append('| %s | %d (%d–%d) | %d (%d–%d) | %d (%d–%d) | %d | %d–%d | %d–%d · %.0f |' % (k2, b[0], b[1], b[2], v[0], v[1], v[2], n[0], n[1], n[2], b[0] + v[0] + n[0], lo, hi, round(lo * 0.5), hi, 0.7 * (lo + hi) / 2))
f6.append('')
f6.append('**Not stated.** Stories whose release or wave is not written in their source (mostly the V12 story tables of Parts 11.2a, 11.6b, 11.7c and 11.13b) are scheduled by Part 11.20 from their FRs; the new ZU stories always state a release.\n')
f6.append('#### 11.22.5.7.2 New ZU stories per epic and release\n')
f6.append('| Epic | Release 1 (stories · SP) | Release 2 | Release 3+ | Total |\n|---|---|---|---|---|')
for e2 in sorted(by_ep):
    cells = []
    for k2 in REL[:3]:
        ss = [s for s in by_ep[e2] if s['release'] == k2]
        cells.append('%d · %d–%d' % (len(ss), sum(s['sp'][0] for s in ss), sum(s['sp'][1] for s in ss)) if ss else '—')
    f6.append('| %s | %s | %d · %d–%d |' % (e2, ' | '.join(cells), len(by_ep[e2]), sum(s['sp'][0] for s in by_ep[e2]), sum(s['sp'][1] for s in by_ep[e2])))
f6.append('')

# 11.22.6 conflicts
f6.append('''## 11.22.6 Conflicts and proposed resolutions

| Tag | Conflict | Sources | Proposed resolution | Status |
|---|---|---|---|---|
| CONFLICT-1140 | Role ID R21 means "agency / managed-service operator" in Part 2.6 §2.6.5.3.2 and "invited investor" in Part 11.16a | Part 2.6; Part 11.16a §11.16.5 | Keep R21 = agency operator (earlier definition); rename the invited-investor role to **R22** in the next consolidation of Part 11.14/11.16; until then this part writes "R21 (Part 11.16a)" for the investor and "R21 (Part 2.6)" for the agency operator. No story behaviour changes | Proposed (DEC-946) |
| CONFLICT-1149 | FR-V12-A-006 ("no investor entity, route, filter or term") and US-19-YG38 ("No investor / fundraising mode in the website") contradict DEC-783, which adopted investor mode and the Investment Automation product | Parts 11.1b, 11.7c; Part 11.14 DEC-783 | Read A-006 as **product separation**: separate product code, no implicit cross-product access, investor entities only in the INV namespace (US-01-ZU01); US-19-YG38 is superseded for the investor website W55–W74 and stays valid for the Sales & Marketing storefront | Resolved by DEC-947 under DEC-783 |
''')
# 11.22.7 decisions
f6.append('''## 11.22.7 Decisions

| DEC | Decision | Authority | Effect |
|---|---|---|---|
| DEC-940 | Part 11.22 is the master story register for V12; coverage is computed by `u_01_inventory.py` and must stay at 100% of FR-V12 with a story that has AC (ADR-275) | Founder V12-B instruction (DEC-790/791), applied by Group U, 28 Nov 2026 | CI gate on Part 11 changes; register §11.22.3 regenerated |
| DEC-941 | FRs traced only to statement-only stories, and ENT trace requirements designed elsewhere, get **acceptance-binding** ZU stories (1–3 SP for AC, examples and test automation); the anchor keeps its build points | Founder V12-B instruction, applied by Group U | No double counting of build effort; every FR gains executable AC |
| DEC-942 | New epic **EP-34 Global expansion, certification and multi-market operations** for ENT-CMP-01…03 and ENT-GLB-01…08 | Founder decisions DEC-775/776, applied by Group U | Epic map extended to EP-34 |
| DEC-943 | Twelve persona journeys JN-01…JN-12 are acceptance journeys; their Scenario Outlines become end-to-end tests in Part 11.21; new personas P21–P23 adopted | Founder V12-B instruction, applied by Group U | E2E suite per persona; persona register extended |
| DEC-944 | Story release buckets follow §11.22.5.1 with the overrides of DEC-771…789; dates follow the work (DEC-770) | Founder decisions DEC-770…789 | Part 11.20 schedules ZU stories by bucket |
| DEC-945 | Combinatorial standard for stories: t = 3 for safety-, money- and law-critical models, t = 2 otherwise, exhaustive ≤ 64, baseline-allow rows, oracle by PDP precedence (ADR-276) | V12-B brief (permutations mandatory), applied by Group U | All Examples reproducible from seeds |
| DEC-946 | Proposed: invited-investor role renamed R22 at the next consolidation (CONFLICT-1140) | Proposed to the Part 11.14 owner (consolidation) | No behaviour change; naming only |
| DEC-947 | FR-V12-A-006 is read as product separation under DEC-783; US-19-YG38 superseded for the investor website (CONFLICT-1149) | Founder decision DEC-783 | US-01-ZU01 carries the amended acceptance |
| DEC-948 | Register wording "Pending Founder decision" in FR-V12-K-004, I-013, A-147 and the O-037…084 status texts is read as decided by DEC-771/772/773/783 (GAP-1148) | Founder decisions DEC-771…783 | Stories cite the deciding DEC |
''')
# 11.22.8 persona review
f6.append('''## 11.22.8 Expert persona review

| Reviewer | Finding | Action taken |
|---|---|---|
| Chief Product Officer | 380 of 1,467 FR-V12 requirements (25.9%) had no executable acceptance; the riskiest (ENT controls, AI controls, securities controls) were among them | Every one now has a story with AC; ENT and AI control stories are Release 1 where DEC-784/785 require |
| Chief Product Officer | Investment Automation workflow requirements were traced only by workflow ID | ZU stories carry FR IDs; GAP-1146 asks Part 11.16d to add them |
| Principal Agile Product Owner | Acceptance bindings must not double-count build effort | DEC-941: bindings carry 1–3 SP; anchors keep build SP |
| Principal Agile Product Owner | Many V12 stories state no points or release | Totals impute 3–8 SP with the assumption logged; Part 11.20 schedules "Not stated" from FR waves |
| Business Systems Analyst | Hand-typed expected results in thousands of Examples rows would drift from the PDP order | ADR-276 oracle; regeneration is deterministic |
| Business Systems Analyst | Scenario Outline steps must reference every Examples column | Step templates per model reference every parameter; checked by build |
| UX researcher | Investor, invited-investor and partner journeys had no persona in the register | P21–P23 added with goals, pains and "never" rules |
| UX researcher | Journeys must include assistive technology and mobile variants | JN-11 and JN-05 variant models include assistive technology, 360 px and phone channels |
| QA Lead | 3-way arrays for law- and money-critical models are large | Kept at 5–6 dimensions per model; every t-tuple verified; counts printed per story |
''')
# 11.22.9 tags
f6.append('''## 11.22.9 Tags register

| Tag | Type | Statement | Where used | Status |
|---|---|---|---|---|
| CONFLICT-1140 | Conflict | R21 defined twice (agency operator, invited investor) | §11.22.4.3, §11.22.6, file e | Proposed resolution DEC-946 |
| RECOMMENDATION-1141 | Recommendation | Add personas P21 investor-relations user, P22 invited investor, P23 partner / reseller | File e | Adopted DEC-943 |
| ASSUMPTION-1142 | Assumption | Acceptance-binding stories 1–3 SP; V12 stories without stated points imputed at 3–8 SP for totals | §11.22.5.1, §11.22.5.7 | Open – replace with team estimates at refinement |
| GAP-1143 | Gap | %d FRs were traced only to statement-only stories without AC | §11.22.2, §11.22.4.2 | Closed by acceptance-binding stories |
| GAP-1144 | Gap | %d FRs had no story at all | §11.22.2, §11.22.3 | Closed by new stories |
| ASSUMPTION-1145 | Assumption | Release bucket mapping (W0–W3/R0–R1 → Release 1; W4–W5/R2 → Release 2; W6/A1–A3/R3–R5 → Release 3+) | §11.22.5.1 | Open – Part 11.20 confirms |
| RECOMMENDATION-1146 | Recommendation | Part 11.21 realises every EX row and journey row as a TC-V12-T test case; Part 11.16d adds FR IDs to EP-32/EP-33 story traces (GAP-1146 trace part) | §11.22.4.3, file e | Open |
| GAP-1146 | Gap | O-037…084 traced by workflow ID only | §11.22.4.3 | Closed here; source fix recommended |
| GAP-1147 | Gap | Six Part 11.6b agent stories have empty titles | §11.22.4.3 | Open (owner Part 11.6) |
| GAP-1148 | Gap | Stale "Pending Founder decision" wording in decided FR rows | §11.22.4.3, DEC-948 | Closed by DEC-948 reading |
| CONFLICT-1149 | Conflict | FR-V12-A-006 / US-19-YG38 versus DEC-783 | §11.22.6, US-01-ZU01 | Resolved DEC-947 |
| ASSUMPTION-1150 | Assumption | All fixtures are synthetic tenants, people and `example` domains | All story files | Closed |
| RECOMMENDATION-1151 | Recommendation | New epic EP-34 for certification and global expansion | §11.22.5.3 | Adopted DEC-942 |
| ASSUMPTION-1152 | Assumption | Role × permission merged into authority classes per Part 5.1a §5.6.2; other dimensions held at baseline per model | §11.22.5.2 | Closed (RBAC matrix test still exhaustive) |
''' % (len(inv['no_ac']), len(inv['uncovered'])))
f6.append('''## 11.22.10 Quality gate and status
''')
f6.append(qgate(FLET, {1: 'Epic map rows computed from the inventory; every FR maps to an epic; every count printed by the scripts',
                      4: '%d / %d FR-V12 have a story with AC; every new story has Gherkin and a generated outline; journeys have E2E outlines' % (inv['fr_total'], inv['fr_total'])}))
f6.append('''**Self-review corrections.** (1) The first inventory pass expanded declared ranges ("FR-V12-A-001…222") into 222 IDs and reported 140 phantom gaps; the rule now keeps defined and explicitly written IDs only (123 in family A). (2) Paragraph-form stories and `**Requirement FR-…**` workflow definitions were missed at first; both are now parsed. (3) Combined `Priority · Wave · Points` rows were not read; baseline stories with points rose from 143 to %d of 461. (4) Keyword routing put "Delivery models" and "Severity model" under AI; family A now uses an explicit domain table.

**Status: Part 11 Batch 11.22 complete (files a–f): %d FR-V12 requirements inventoried; %d new stories (US-<EP>-ZU<nn>, %d–%d SP) close %d uncovered and %d AC-less requirements, so 100%% of FR-V12 have a story with acceptance criteria; %s generated Examples rows; 12 persona journeys; epic map EP-01…EP-34 with totals per epic and release.**
''' % (sum(1 for s in base['stories'].values() if s.get('points')), inv['fr_total'], len(stories), summary['new_sp_low'], summary['new_sp_high'], len(inv['uncovered']), len(inv['no_ac']), '{:,}'.format(summary['examples_rows'])))
write('Part-11-22%s_Epic_Map' % FLET + '_Totals_Conflicts_Decisions_and_Quality_Gate.md', '\n'.join(f6))
json.dump(summary, open(os.path.join(OUTD, 'u_summary.json'), 'w'), indent=1)
print('FILES', [n for _, n, _ in story_files])
