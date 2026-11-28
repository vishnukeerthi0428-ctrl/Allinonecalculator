"""Group T (Part 11.21): constraint-aware variable-strength covering-array engine and verifier.

Constraint model.  Every Part 11.21 model states its constraints as a predicate that only ever
relates two parameters at a time (a binary constraint network).  The engine therefore derives the
table of allowed value pairs for every parameter pair once, and decides whether a partial
assignment can be completed to a valid full row by arc consistency (AC-3) plus backtracking with
the smallest remaining domain first.  Tuples that no valid full row can contain are "excluded by
constraint" and are not required.

generate():  deterministic AETG-style greedy construction.  Required coverage is a list of
             *strength groups* (param subset, t); every feasible t-tuple of every group must appear
             in at least one row.  Groups give pairwise (t=2), 3-way (t=3), variable-strength (e.g.
             3-way among control parameters plus 2-way capability x control) and 1-way coverage.
             Each new row is seeded from an uncovered tuple and filled parameter by parameter with
             the value covering most still-uncovered tuples, keeping the domains arc-consistent;
             ncand candidate rows are built per step and the best is kept.
verify():    independent check: (a) every row is complete and satisfies the original predicate on
             the full row; (b) every required tuple is recomputed with a separate depth-first
             completion search (forward checking on the raw predicate, not on the pair tables)
             and must occur in a row.  Reports required and missing counts (missing must be 0).
Standard library only.
"""
import itertools, random


class Net:
    def __init__(self, params, constraint):
        self.params = params
        self.names = list(params)
        self.pos = {n: i for i, n in enumerate(self.names)}
        self.allowed = {}
        for a, b in itertools.combinations(self.names, 2):
            tab = {}
            for va in params[a]:
                s = set()
                for vb in params[b]:
                    if constraint({a: va, b: vb}):
                        s.add(vb)
                tab[va] = s
            self.allowed[(a, b)] = tab
            inv = {}
            for vb in params[b]:
                inv[vb] = {va for va in params[a] if vb in tab[va]}
            self.allowed[(b, a)] = inv
        self.unary = {n: {v for v in params[n] if constraint({n: v})} for n in self.names}

    def ac3(self, dom, changed=None):
        if changed is None:
            queue = [(a, b) for a in self.names for b in self.names if a != b]
        else:
            queue = [(a, changed) for a in self.names if a != changed]
        while queue:
            a, b = queue.pop()
            tab = self.allowed[(a, b)]
            db = dom[b]
            new = {va for va in dom[a] if tab[va] & db}
            if new != dom[a]:
                if not new:
                    return False
                dom[a] = new
                queue.extend((c, a) for c in self.names if c != a and c != b)
        return True

    def domains(self, assign):
        dom = {}
        for n in self.names:
            if n in assign:
                if assign[n] not in self.unary[n]:
                    return None
                dom[n] = {assign[n]}
            else:
                dom[n] = set(self.unary[n])
                if not dom[n]:
                    return None
        return dom

    def solve(self, dom):
        if not self.ac3(dom):
            return None
        free = [n for n in self.names if len(dom[n]) > 1]
        if not free:
            return {n: next(iter(dom[n])) for n in self.names}
        n = min(free, key=lambda m: len(dom[m]))
        for v in sorted(dom[n], key=lambda x: self.params[n].index(x)):
            d2 = {k: set(s) for k, s in dom.items()}
            d2[n] = {v}
            r = self.solve(d2)
            if r:
                return r
        return None

    def feasible(self, assign):
        dom = self.domains(assign)
        if dom is None:
            return False
        return self.solve(dom) is not None


def required_tuples(params, constraint, groups, net=None, tuple_filter=None):
    net = net or Net(params, constraint)
    pos = net.pos
    req = set()
    for gp, t in groups:
        gp = sorted(gp, key=lambda n: pos[n])
        for combo in itertools.combinations(gp, t):
            for vals in itertools.product(*[params[n] for n in combo]):
                key = (combo, vals)
                if tuple_filter and not tuple_filter(key):
                    continue
                a = dict(zip(combo, vals))
                if t == 1 or t == 2:
                    # pairs: AC-3 + search (fast); singles likewise
                    pass
                if net.feasible(a):
                    req.add(key)
    return req


def covered_by(row, combos):
    return {(c, tuple(row[n] for n in c)) for c in combos}


def generate(params, constraint, groups, seed=920, ncand=10, tuple_filter=None):
    net = Net(params, constraint)
    names = net.names
    req = required_tuples(params, constraint, groups, net, tuple_filter)
    combos = sorted({c for c, _ in req})
    by_param = {}
    for c in combos:
        for n in c:
            by_param.setdefault(n, []).append(c)
    uncovered = set(req)
    rng = random.Random(seed)
    rows = []
    while uncovered:
        pool = sorted(uncovered)
        seeds = [pool[0]] + [pool[rng.randrange(len(pool))] for _ in range(ncand - 1)]
        best, best_gain = None, -1
        for combo, vals in seeds:
            assign = dict(zip(combo, vals))
            dom = net.domains(assign)
            if dom is None or not net.ac3(dom):
                continue
            rest = [n for n in names if n not in assign]
            rng.shuffle(rest)
            ok = True
            for n in rest:
                if len(dom[n]) == 1:
                    assign[n] = next(iter(dom[n]))
                    continue
                cands = sorted(dom[n], key=lambda x: params[n].index(x))
                rng.shuffle(cands)
                scored = []
                for v in cands:
                    g = 0
                    for c in by_param.get(n, ()):
                        if all((m == n) or (m in assign) for m in c):
                            key = (c, tuple(v if m == n else assign[m] for m in c))
                            if key in uncovered:
                                g += 1
                    scored.append((-g, cands.index(v), v))
                scored.sort()
                placed = False
                for _, _, v in scored:
                    d2 = {k: set(s) for k, s in dom.items()}
                    d2[n] = {v}
                    if net.ac3(d2, changed=n):
                        dom = d2
                        assign[n] = v
                        placed = True
                        break
                if not placed:
                    ok = False
                    break
            if not ok or len(assign) != len(names):
                continue
            g = len(covered_by(assign, combos) & uncovered)
            if g > best_gain:
                best, best_gain = dict(assign), g
        if best is None or best_gain <= 0:
            raise RuntimeError('generator stalled; uncovered=%d' % len(uncovered))
        rows.append({n: best[n] for n in names})
        uncovered -= covered_by(best, combos)
    return rows, len(req)


# ----------------------------------------------------------------------------- independent verifier
def _exists_completion(params, constraint, assign):
    names = [n for n in params if n not in assign]
    names.sort(key=lambda n: -len(params[n]))   # different order from the generator

    def dfs(i, a):
        if not constraint(a):
            return False
        if i == len(names):
            return True
        for m in names[i:]:
            if not any(constraint(dict(a, **{m: v})) for v in params[m]):
                return False
        n = names[i]
        for v in params[n]:
            a[n] = v
            if dfs(i + 1, a):
                del a[n]
                return True
            del a[n]
        return False
    return dfs(0, dict(assign))


def verify(params, constraint, groups, rows, tuple_filter=None, sample_infeasible_check=True):
    names = list(params)
    pos = {n: i for i, n in enumerate(names)}
    bad_rows = [r for r in rows if set(r) != set(names) or not constraint(r)]
    present = set()
    for r in rows:
        for gp, t in groups:
            gp = sorted(gp, key=lambda n: pos[n])
            for c in itertools.combinations(gp, t):
                present.add((c, tuple(r[n] for n in c)))
    need, missing, excluded = 0, 0, 0
    net = Net(params, constraint)
    seen = set()
    for gp, t in groups:
        gp = sorted(gp, key=lambda n: pos[n])
        for c in itertools.combinations(gp, t):
            for vals in itertools.product(*[params[n] for n in c]):
                key = (c, vals)
                if key in seen:
                    continue
                seen.add(key)
                if tuple_filter and not tuple_filter(key):
                    continue
                if key in present:
                    need += 1
                    continue
                # not present: it must be infeasible, proven by the independent search
                if _exists_completion_fast(net, params, constraint, dict(zip(c, vals))):
                    need += 1
                    missing += 1
                else:
                    excluded += 1
    return dict(rows=len(rows), invalid_rows=len(bad_rows), required=need, missing=missing, excluded=excluded)


def _exists_completion_fast(net, params, constraint, assign):
    """Independent proof search for a tuple absent from the array: depth-first with forward
    checking on the raw predicate, variables ordered by the pair-table support (not the AC-3 path)."""
    names = [n for n in params if n not in assign]

    def dfs(a, rest):
        if not constraint(a):
            return False
        if not rest:
            return True
        doms = {}
        for m in rest:
            d = [v for v in params[m] if constraint(dict(a, **{m: v}))]
            if not d:
                return False
            doms[m] = d
        n = min(rest, key=lambda m: (len(doms[m]), -len(params[m])))
        r2 = [m for m in rest if m != n]
        for v in doms[n]:
            a[n] = v
            if dfs(a, r2):
                del a[n]
                return True
            del a[n]
        return False
    return dfs(dict(assign), names)


def raw_product(params):
    p = 1
    for v in params.values():
        p *= len(v)
    return p


def valid_count(params, constraint, limit=2_000_000):
    """Exact count of valid full combinations when the product is small enough, else None."""
    if raw_product(params) > limit:
        return None
    names = list(params)
    c = 0
    for combo in itertools.product(*[params[n] for n in names]):
        if constraint(dict(zip(names, combo))):
            c += 1
    return c


def exhaustive(params, constraint):
    names = list(params)
    out = []
    for combo in itertools.product(*[params[n] for n in names]):
        r = dict(zip(names, combo))
        if constraint(r):
            out.append(r)
    return out
