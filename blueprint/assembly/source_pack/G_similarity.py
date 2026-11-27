#!/usr/bin/env python3
"""Group G: TF-IDF candidate finder (source test -> blueprint TC). Used to propose candidates; final mapping is curated
in G_map.py. Usage: python3 G_similarity.py doc22.json bp.json out_candidates.json [families...]"""
import json
import math
import re
import sys
from collections import Counter, defaultdict

STOP = set("the a an and or of to in on for with by is are be as at from that this it its no not only any all each "
           "into per via use used using than then when where which who after before must should can may one two "
           "verify record test case fixture synthetic scope run p0 p1 p2 p3 sys ut it e2e uat ct y n".split())


def tok(s):
    s = s.lower()
    s = re.sub(r"`|\*", " ", s)
    return [w for w in re.findall(r"[a-z][a-z0-9\-]{2,}", s) if w not in STOP]


def main(src, bp, out, fams):
    S = json.load(open(src))["records"]
    B = json.load(open(bp))["tcs"]
    docs = {k: Counter(tok(v["title"] * 1 + " " + v["title"] + " " + v["text"])) for k, v in B.items()}
    df = Counter()
    for c in docs.values():
        df.update(set(c))
    N = len(docs)
    idf = {w: math.log((N + 1) / (n + 1)) + 1 for w, n in df.items()}

    def vec(c):
        v = {w: (1 + math.log(n)) * idf.get(w, math.log(N + 1) + 1) for w, n in c.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        return {w: x / norm for w, x in v.items()}

    V = {k: vec(c) for k, c in docs.items()}
    inv = defaultdict(list)
    for k, v in V.items():
        for w, x in v.items():
            inv[w].append((k, x))
    res = {}
    for r in S:
        if fams and r["family"] not in fams:
            continue
        q = vec(Counter(tok(" ".join([r["title"], r["title"], r["steps"], r["expected"], r.get("negative", "")]))))
        sc = Counter()
        for w, x in q.items():
            for k, y in inv.get(w, []):
                sc[k] += x * y
        res[r["id"]] = [(k, round(s, 3), B[k]["title"][:110]) for k, s in sc.most_common(12)]
    json.dump(res, open(out, "w"), indent=0, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], set(sys.argv[4:]))
