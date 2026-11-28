#!/usr/bin/env python3
"""Assemble Part 11.17a/b from assembly/v12b/p_src/*.md, expanding
<!--INCLUDE:relative/path--> markers (relative to assembly/v12b/)."""
import re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
def expand(text):
    def rep(m):
        with open(os.path.join(HERE, m.group(1)), encoding="utf-8") as f:
            return f.read().rstrip("\n")
    return re.sub(r"<!--INCLUDE:([^>]+)-->", rep, text)
PARTS = {
    "Part-11-17a_Bounded_Mandates_Agentic_Commerce_and_Payments.md": ["a1_head.md", "a2_mandate.md", "a3_commerce.md"],
    "Part-11-17b_Automatic_Bid_Submission_Agents_Tests_Stories_and_Costs.md": ["b1_bids.md", "b2_agents.md", "b3_ui_data_api.md", "b4_stories.md", "b5_tests.md", "b6_aieval.md", "b7_combi_cost_close.md"],
}
for out, srcs in PARTS.items():
    body = "".join(open(os.path.join(HERE, "p_src", s), encoding="utf-8").read() for s in srcs)
    body = expand(body)
    with open(os.path.join(ROOT, out), "w", encoding="utf-8") as f:
        f.write(body)
    print(out, len(body), "chars", body.count("\n"), "lines")
