"""Group W: SQL helpers (statement splitter aware of quotes, dollar quotes and comments; scratch PostgreSQL access)."""
import re, os, subprocess

PG = dict(host=os.environ.get('WPGHOST', '/tmp/pgw'), port=int(os.environ.get('WPGPORT', '55433')), user='postgres')


def split_sql(text):
    """Split SQL text into statements. Handles '...', "...", $tag$...$tag$, -- and /* */ comments."""
    out, buf, i, n = [], [], 0, len(text)
    while i < n:
        c = text[i]
        if c == '-' and text.startswith('--', i):
            j = text.find('\n', i)
            j = n if j < 0 else j
            buf.append(text[i:j]); i = j; continue
        if c == '/' and text.startswith('/*', i):
            j = text.find('*/', i + 2)
            j = n if j < 0 else j + 2
            buf.append(text[i:j]); i = j; continue
        if c == "'":
            j = i + 1
            while j < n:
                if text[j] == "'" and j + 1 < n and text[j + 1] == "'":
                    j += 2; continue
                if text[j] == "'":
                    break
                j += 1
            buf.append(text[i:j + 1]); i = j + 1; continue
        if c == '"':
            j = text.find('"', i + 1)
            buf.append(text[i:j + 1]); i = j + 1; continue
        if c == '$':
            m = re.match(r'\$([A-Za-z_][A-Za-z0-9_]*)?\$', text[i:])
            if m:
                tag = m.group(0)
                j = text.find(tag, i + len(tag))
                j = n if j < 0 else j + len(tag)
                buf.append(text[i:j]); i = j; continue
        if c == ';':
            s = ''.join(buf).strip()
            if s and not all(l.strip().startswith('--') or not l.strip() for l in s.split('\n')):
                out.append(s + ';')
            buf = []; i += 1; continue
        buf.append(c); i += 1
    s = ''.join(buf).strip()
    if s and not all(l.strip().startswith('--') or not l.strip() for l in s.split('\n')):
        out.append(s if s.endswith(';') else s + ';')
    return out


def strip_leading_comments(stmt):
    return '\n'.join(l for l in stmt.split('\n') if not l.strip().startswith('--')).strip()


def connect(db='postgres'):
    import psycopg2
    c = psycopg2.connect(dbname=db, **PG)
    c.autocommit = True
    return c


def recreate_db(name, region='IN'):
    c = connect()
    cur = c.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {name} WITH (FORCE)')
    cur.execute(f'CREATE DATABASE {name}')
    cur.execute(f"ALTER DATABASE {name} SET app.deployment_region = '{region}'")
    cur.execute(f"ALTER DATABASE {name} SET app.zone = '{region}'")
    c.close()


def psql_file(db, path, single_tx=True):
    args = ['psql', '-h', PG['host'], '-p', str(PG['port']), '-U', 'postgres', '-d', db, '-v', 'ON_ERROR_STOP=1', '-q', '-f', path]
    if single_tx:
        args.insert(-2, '-1')
    p = subprocess.run(args, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr
