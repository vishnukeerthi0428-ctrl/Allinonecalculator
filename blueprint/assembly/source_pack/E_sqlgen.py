"""Group E: turn reviewed column/index proposals into DDL text for Part 3.6b."""
import re
Z = "'00000000-0000-0000-0000-000000000000'::uuid"
def coldef(table, text, src):
    """text like 'name text NOT NULL; UQ (...)' or 'x uuid NULL -> tbl (comment)'"""
    comment = [f'source {src}']
    t = text
    depth = 0
    for i, ch in enumerate(t):
        depth += (ch == '(') - (ch == ')')
        if ch == ';' and depth == 0:
            comment.append(t[i+1:].strip()); t = t[:i]; break
    fk = None
    if ' -> ' in t:
        t, fkpart = t.split(' -> ', 1)
        fk = fkpart.split()[0]
        rest = fkpart[len(fk):].strip()
        if rest: comment.append(rest.strip('() '))
    t = t.strip()
    m = re.search(r'\s*\(([^()]*)\)\s*$', t)
    if m and not re.search(r'\bIN\s*\([^()]*\)\s*$', t):
        comment.append(m.group(1)); t = t[:m.start()].strip()
    name = t.split()[0]
    t = re.sub(r'CHECK IN \(([^)]*)\)', lambda mm: 'CHECK (' + name + ' IN (' + ', '.join("'" + v.strip() + "'" for v in mm.group(1).split(',')) + '))', t)
    t = re.sub(r'CHECK (\d+)-(\d+)', lambda mm: f'CHECK ({name} BETWEEN {mm.group(1)} AND {mm.group(2)})', t)
    t = t.replace('DEFAULT {}', "DEFAULT '{}'::jsonb").replace('DEFAULT []', "DEFAULT '[]'::jsonb")
    t = re.sub(r"DEFAULT ([a-z_]+)\b", lambda mm: mm.group(0) if mm.group(1) in ('true','false','now') else f"DEFAULT '{mm.group(1)}'", t)
    if fk: t += f' REFERENCES {fk} (id)'
    return f"ALTER TABLE {table} ADD COLUMN {t};  -- " + '; '.join(c for c in comment if c)
def indexddl(table, prop, nid):
    p = prop.split(';')[0]
    note = prop[len(p):].strip('; ')
    on_new = re.search(r' on new column (\w+)', p)
    if on_new: note = (note + ' new column ' + on_new.group(1)).strip(); p = p[:on_new.start()]
    m = re.match(r'(\w+) \((.+?)\)(\s+WHERE .+)?$', p.strip())
    if not m: return f'-- {nid} {table}: {prop}'
    name, cols, where = m.group(1), m.group(2), (m.group(3) or '')
    cols = cols.replace('zero-uuid', Z)
    uq = 'UNIQUE ' if name.startswith('uq_') else ''
    s = f'CREATE {uq}INDEX CONCURRENTLY {name} ON {table} ({cols}){where};'
    return s + f'  -- {nid}' + (f'; {note}' if note else '')
