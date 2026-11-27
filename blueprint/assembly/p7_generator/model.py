"""Cost model for Part 7 (all prices: verify at time of implementation, as of 27 Nov 2026)."""
from agents import A, SEATS
FX = 90.0  # INR per USD, BRD §6 assumption (verify)
# USD per million tokens. Source: claude-api skill model table (cached 2026-11-03) and prompt-caching guide.
PRICES = {
    "H": dict(name="Claude Haiku 5.5 (claude-haiku-5-5)", inp=0.10, out=0.50, cr=0.01, cw5=0.125, cw1h=0.20),
    "S": dict(name="Claude Sonnet 5.5 (claude-sonnet-5-5)", inp=2.00, out=10.00, cr=0.10, cw5=2.50, cw1h=4.00),
}
BATCH = 0.5
SEAT_INR = 2 * 20 * FX  # B09: 2 seats x $20 (BRD §6) = ₹3,600

SCEN = {"low": dict(calls=0.5, hit=+0.10, esc=0.5, out=1.0),
        "base": dict(calls=1.0, hit=0.0, esc=1.0, out=1.0),
        "high": dict(calls=2.0, hit=-0.20, esc=1.5, out=1.25)}

def per_call_usd(model, c, hit, out_mult=1.0):
    p = PRICES[model]
    cw = p["cw1h"] if c["ttl"] == "1h" else p["cw5"]
    S, I, O = c["S"], c["I"], c["O"] * out_mult
    usd = (S * (hit * p["cr"] + (1 - hit) * cw) + (I - S) * p["inp"] + O * p["out"]) / 1e6
    return usd * (BATCH if c["batch"] else 1.0)

def comp_cost_inr(c, scen="base", vol=1.0):
    s = SCEN[scen]
    hit = min(0.95, max(0.0, c["hit"] + s["hit"]))
    esc = min(1.0, c["esc"] * s["esc"])
    calls = c["calls"] * s["calls"] * vol
    if c["model"] == "H":
        per = (1 - esc) * per_call_usd("H", c, hit, s["out"]) + esc * per_call_usd("S", c, hit, s["out"])
    else:
        per = per_call_usd("S", c, hit, s["out"])
    return per * FX * calls, per * FX, calls

def agent_cost(a, scen="base", vol=1.0, line=None):
    tot = 0.0
    for c in a["cost"]:
        if line and c["line"] != line: continue
        tot += comp_cost_inr(c, scen, vol)[0]
    return tot

def tokens_per_call(a):
    if not a["cost"]: return "n/a (seat)"
    c = a["cost"][0]
    return f'{c["I"]:,} in ({c["S"]:,} cacheable) / {c["O"]:,} out'

def calls_base(a):
    return sum(c["calls"] for c in a["cost"])

def release(wave):
    w = wave.split()[0]
    return {"W0": "R1", "W1": "R1", "W2": "R1", "W3": "R1", "W4": "R2", "W5": "R2", "W6": "Future"}[w]

def lines(a):
    s = sorted({c["line"] for c in a["cost"]})
    if a.get("seat_share"): s.append("B09")
    return ", ".join(s) if s else "B09"

if __name__ == "__main__":
    for scen in SCEN:
        t = {}
        for a in A:
            if release(a["wave"]) == "Future": continue
            for c in a["cost"]:
                t[c["line"]] = t.get(c["line"], 0) + comp_cost_inr(c, scen)[0]
        print(scen, {k: round(v) for k, v in t.items()})
    for a in A:
        print(a["id"], release(a["wave"]), round(agent_cost(a, "low")), round(agent_cost(a)), round(agent_cost(a, "high")))
    for v in (4, 12):
        print("vol", v, round(sum(agent_cost(a, "base", v, "B02") for a in A if release(a["wave"]) != "Future")))
