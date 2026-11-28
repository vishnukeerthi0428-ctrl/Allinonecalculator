"""Group T (Part 11.21): constraint-aware variable-strength covering-array engine and verifier.

generate():  deterministic AETG-style greedy construction.  Required coverage is a list of
             *strength groups* (param subset, t); every feasible t-tuple of every group must
             appear in at least one row.  Groups give pairwise (t=2), 3-way (t=3), mixed or
             variable-strength coverage (e.g. 3-way among control parameters and 2-way between
             the capability parameter and each control) and 1-way "each-choice" coverage.
             Each new row is seeded from an uncovered tuple and filled parameter by parameter
             with the value that covers the most still-uncovered tuples (ncand candidate rows per
             step, the best is kept).  Constraints are a predicate on partial assignments.
             Tuples that no valid full row can contain are not required (excluded by constraint).
verify():    independent re-implementation: enumerates feasibility with its own depth-first
             completion search, recomputes every required tuple, checks every row is complete and
             valid, and reports the number of missing tuples (must be 0).
Standard library only.
"""
import itertools, random


def _names(params):
    return list(params)


def feasible_factory(params, constraint):
    names = _names(params)
    order = sorted(names, key=lambda n: len(params[n]))
    memo = {}

    def feasible(assign):
        key = tuple(sorted(assign.items()))
        if key in memo:
            return memo[key]
        if not constraint(assign):
            memo[key] = False
            return False
        rest = [n for n in order if n not in assign]
        a = dict(assign)

        def bt(i):
            if i == len(rest):
                return True
            # forward checking: every unassigned parameter keeps at least one consistent value
            for m in rest[i:]:
                okm = False
                for v in params[m]:
                    a[m] = v
                    c = constraint(a)
                    del a[m]
                    if c:
                        okm = True
                        break
                if not okm:
                    return False
            n = rest[i]
            for v in params[n]:
                a[n] = v
                if constraint(a) and bt(i + 1):
                    del a[n]
                    return True
                del a[n]
            return False
        r = bt(0)
        memo[key] = r
        return r
    return feasible


def required_tuples(params, constraint, groups, feasible=None, tuple_filter=None):
    feasible = feasible or feasible_factory(params, constraint)
    names = _names(params)
    pos = {n: i for i, n in enumerate(names)}
    req = set()
    for gp, t in groups:
        gp = sorted(gp, key=lambda n: pos[n])
        for combo in itertools.combinations(gp, t):
            for vals in itertools.product(*[params[n] for n in combo]):
                key = (combo, vals)
                if tuple_filter and not tuple_filter(key):
                    continue
                if feasible(dict(zip(combo, vals))):
                    req.add(key)
    return req


def _combos_by_param(req):
    by = {}
    for combo, _ in req:
        for n in combo:
            by.setdefault(n, set()).add(combo)
    return {n: sorted(s) for n, s in by.items()}


def covered_by(row, combos):
    return {(c, tuple(row[n] for n in c)) for c in combos}


def generate(params, constraint, groups, seed=920, ncand=10, tuple_filter=None):
    names = _names(params)
    feasible = feasible_factory(params, constraint)
    req = required_tuples(params, constraint, groups, feasible, tuple_filter)
    combos = sorted({c for c, _ in req})
    by_param = _combos_by_param(req)
    uncovered = set(req)
    rng = random.Random(seed)
    rows = []
    stall = 0
    while uncovered:
        pool = sorted(uncovered)
        seeds = [pool[0]] + [pool[rng.randrange(len(pool))] for _ in range(ncand - 1)]
        best, best_gain = None, -1
        for combo, vals in seeds:
            row = dict(zip(combo, vals))
            rest = [n for n in names if n not in row]
            rng.shuffle(rest)
            ok = True
            for n in rest:
                bestv, bg = None, -1
                vals_n = list(params[n])
                rng.shuffle(vals_n)
                for v in vals_n:
                    row[n] = v
                    if not constraint(row):
                        continue
                    g = 0
                    for c in by_param.get(n, ()):
                        if all(m in row for m in c) and (c, tuple(row[m] for m in c)) in uncovered:
                            g += 1
                    if g > bg:
                        bg, bestv = g, v
                if bestv is None:
                    ok = False
                    break
                row[n] = bestv
            if not ok or not feasible(row):
                # dead end on the cheap path: complete by backtracking
                row = dict(zip(combo, vals))
                if not feasible(row):
                    continue
                for n in [m for m in names if m not in row]:
                    for v in params[n]:
                        row[n] = v
                        if feasible(row):
                            break
            g = len(covered_by(row, combos) & uncovered)
            if g > best_gain:
                best, best_gain = dict(row), g
        if best is None or best_gain <= 0:
            stall += 1
            if stall > 5:
                raise RuntimeError('generator stalled; uncovered=%d' % len(uncovered))
            continue
        rows.append({n: best[n] for n in names})
        uncovered -= covered_by(best, combos)
    return rows, len(req)


# ----------------------------------------------------------------------------- independent verifier
def _exists_completion(params, constraint, assign):
    names = [n for n in params if n not in assign]
    names.sort(key=lambda n: -len(params[n]))   # different order from the generator
    stack = [(0, dict(assign))]
    while stack:
        i, a = stack.pop()
        if not constraint(a):
            continue
        if i == len(names):
            return True
        dead = False
        for m in names[i:]:
            if not any(constraint(dict(a, **{m: v})) for v in params[m]):
                dead = True
                break
        if dead:
            continue
        n = names[i]
        for v in reversed(params[n]):
            b = dict(a)
            b[n] = v
            stack.append((i + 1, b))
    return False


def verify(params, constraint, groups, rows, tuple_filter=None):
    names = list(params)
    pos = {n: i for i, n in enumerate(names)}
    bad_rows = [r for r in rows if set(r) != set(names) or not constraint(r)]
    present = set()
    for r in rows:
        for gp, t in groups:
            gp = sorted(gp, key=lambda n: pos[n])
            for c in itertools.combinations(gp, t):
                present.add((c, tuple(r[n] for n in c)))
    need, missing = 0, 0
    for gp, t in groups:
        gp = sorted(gp, key=lambda n: pos[n])
        for c in itertools.combinations(gp, t):
            for vals in itertools.product(*[params[n] for n in c]):
                key = (c, vals)
                if tuple_filter and not tuple_filter(key):
                    continue
                if not _exists_completion(params, constraint, dict(zip(c, vals))):
                    continue
                need += 1
                if key not in present:
                    missing += 1
    # de-duplicate tuples counted in several groups
    return dict(rows=len(rows), invalid_rows=len(bad_rows), required=need, missing=missing)


def raw_product(params):
    p = 1
    for v in params.values():
        p *= len(v)
    return p


def valid_count(params, constraint, limit=3_000_000):
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
