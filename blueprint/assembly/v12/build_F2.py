"""Second-stage generator: FR register, user stories with Gherkin, test-case table; then assembles
Part 11.6a and 11.6b from templates (<!--INC:file--> placeholders)."""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import F_aspects_text as T, F_cards as CD, F_au as AUD
BP = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "F_frag")
def w(n, s): open(os.path.join(OUT, n), "w").write(s)
def esc(s): return str(s).replace("|", "/").replace("\n", " ")

# ---------------- FR register ----------------
aix = [a for a in T.A if a[3].startswith("F16-") and a[4].startswith("AIX-")]
FR = []
for a in aix:
    x = a[4].split()[0]; n = int(x[4:])
    req, acc = a[4].split("; acceptance: ")
    FR.append((f"FR-V12-F-{n:03d}", x, re.sub(r"^AIX-\d+ \(P\d\) ", "", req), acc, a[8].split(";")[0], f"TC-V12-F-{n:03d}", "EP-04"))
ctrl = [a for a in T.A if a[4].startswith("CTRL-AI")]
for i, a in enumerate(ctrl):
    FR.append((f"FR-V12-F-{21+i:03d}", a[4].split()[0], a[4], "Control verified by AI-INJ corpus and unit test", "AU-005/AU-169/AU-179" if i in (1, 4) else "existing control", f"TC-V12-F-{33+i:03d}", "EP-04"))
extra = [
 ("FR-V12-F-030","16.7","Meter every model call as ai_usage_event: tenant, company, workflow, step, run, model, PRM version, input/output/cached/reasoning tokens, latency, outcome","Tenant totals reconcile with provider invoice within AU-048 tolerance","AU-012, AU-048","TC-V12-F-012","EP-04"),
 ("FR-V12-F-031","ch17","Store per chunk source_ref, rights, provenance_hash, ingested_at, observed_at, freshness_limit, quarantine_state; quarantine poisoned/unlicensed sources","Quarantined chunk never retrieved; erasure removes chunk and vector with evidence","AU-165","TC-V12-F-072","EP-02"),
 ("FR-V12-F-032","REC-12","Key every eval run by candidate/version, workflow, PRM version, language, data class, dataset version; store provider, sample size, quality, cost, latency, red-team evidence, reviewer, DPA ref, region","Unrelated evaluation cannot unlock promotion","AU-154","TC-V12-F-065","EP-04"),
 ("FR-V12-F-033","16.4","Replay affected suites on model, prompt, retrieval, policy or tool change; nightly drift sample; denominator stored","Change with lower accuracy blocked","AU-154, AU-057","TC-V12-F-006","EP-04"),
 ("FR-V12-F-034","REC-11","Effect intent immutable: tenant, company, recipient, relationship, purpose, market, channel, config version, payload digest, consent version, reviewer, expiry, budget, idempotency key","Any changed field → HOLD; unknown write → reconcile before retry","AU-175, AU-171","TC-V12-F-077","EP-18"),
 ("FR-V12-F-035","18 V5","Approval record binds tenant/company, workflow version, action digest, recipient, budget, currency, actor authority, expiry, policy version; prepare/approve/execute/reconcile","Stale or revoked approval rejected before adapter call","AU-175","TC-V12-F-184","EP-18"),
 ("FR-V12-F-036","15 V5","Per-run record: AGT role, agent, PRM, model, allowed tool-set digest, max tokens/cost, deadline, input/output refs, policy version, quality verdict","100% runs carry all fields","AU-179","TC-V12-F-188","EP-04"),
 ("FR-V12-F-037","16.2","Model registry row eligible only with suites, red-team, DPA (no training, retention, region), CPAR, latency p95, security review","Missing evidence → not routable","AU-151","TC-V12-F-002","EP-04"),
 ("FR-V12-F-038","16.2","Each workflow pins model and PRM versions with rollback_to pointer; kill switch per model/prompt/workflow","Rollback ≤ 5 min; kill switch within one scheduler cycle","AU-151, AU-025","TC-V12-F-020","EP-04"),
 ("FR-V12-F-039","ch15","Two-level registry AGT role → AG/AU implementer; every workflow bound to one AGT","156/156 workflows bound; tool grants ⊆ AGT ceiling","AU-179","TC-V12-F-188","EP-04"),
 ("FR-V12-F-040","MT-34","One definition per stable workflow version; per-customer configuration only","25 configurations, 0 cloned definitions","AU-178","TC-V12-F-061","EP-18"),
 ("FR-V12-F-041","FL-04","Reusable child workflows with versioned interfaces; metering by run lineage","Child called by two parents: no duplicate charge, no unauthorized SKU access","AU-167, AU-158","TC-V12-F-062","EP-18"),
 ("FR-V12-F-042","CJ-R01/19/20","Jurisdiction packs versioned with states; only Approved enforced; unreviewed → stricter outcome","Draft pack never ALLOWs","AU-170","TC-V12-F-097","EP-03"),
 ("FR-V12-F-043","CJ-R02/03","Send preflight decision table (13 V8 + 7 V9 cases) with precedence","All cases return expected verdict and reason codes","AU-171","TC-V12-F-098","EP-03"),
 ("FR-V12-F-044","CJ-R04/05","Scoped consent ledger and withdrawal suppression; queued runs held","Queued run after withdrawal → Held, no dispatch","AU-172","TC-V12-F-101","EP-03"),
 ("FR-V12-F-045","CJ-R06","DLT and preference-registry scrub for promotional SMS/voice; number pool by purpose","Unregistered template or unscrubbed list → HOLD","AU-173","TC-V12-F-102","EP-08"),
 ("FR-V12-F-046","CJ-R07/08","Regulatory clocks for DSAR and breach per pack","Clocks start at detection; overdue visible","AU-174","TC-V12-F-104","EP-03"),
 ("FR-V12-F-047","CJ-R13","AI disclosure and machine-readable marking on AI content and agents","Undisclosed AI content in EU → HOLD","AU-177","TC-V12-F-109","EP-03"),
 ("FR-V12-F-048","REC-03","Group competing actions by relationship and purpose; reviewer disposition","Only selected eligible action proceeds","AU-176","TC-V12-F-075","EP-18"),
 ("FR-V12-F-049","ch17","Scoped cache key and invalidation contract","Different tenant or revoked source → miss","AU-164","TC-V12-F-069","EP-04"),
 ("FR-V12-F-050","16.7/ch30","Cost per accepted result per workflow, tenant and agent with denominator","Rejected outputs shown; no invented prices","AU-158","TC-V12-F-014","EP-04"),
]
FR += extra
for i, c in enumerate(CD.CARDS):
    FR.append((f"FR-V12-F-{51+i:03d}", c["wfs"], f"{c['id']} {c['name']}: {c['purpose'].split(', so ')[0].replace('**','')}", c["kpi"], c["id"], f"TC-V12-F-{131+i:03d}", c["ep"]))
L = ["| FR | V12 source | Requirement | Acceptance | Implemented by | Test | Epic |", "|---|---|---|---|---|---|---|"]
for r in FR: L.append("| " + " | ".join(esc(x) for x in r) + " |")
w("t_fr.md", "\n".join(L) + "\n")

# ---------------- user stories ----------------
S = []
for i, c in enumerate(CD.CARDS):
    ep = c["ep"][3:]; us = f"US-{ep}-YF{i+1:02d}"
    per = c["persona"].split(";")[0]
    goal = c["purpose"].split(", so ")[0].replace("**", "")
    v, rest = goal.split(" ", 1)
    v = {"Classifies":"classify","Turns":"turn","Localizes":"localize","Checks":"check","Reads":"read","Explains":"explain","Drafts":"draft","Classifies":"classify",
         "Prepares":"prepare","Interprets":"interpret","Fills":"fill","Extracts":"extract"}.get(v, v.lower())
    goal = v + " " + rest
    so = c["purpose"].split(", so ")[1].rstrip(".").split(" (SM-SVC")[0] if ", so " in c["purpose"] else "work is faster and safer"
    aut = re.sub(r"\*\*", "", c["autonomy"]).split(";")[0].split(" — ")[0].split(" (")[0]
    S.append(f"##### {us} {c['name']} ({c['id']}, {c['agt']})\n\n**As** {per}, **I want** the platform to {goal}, **so that** {so}. Traces: FR-V12-F-{51+i:03d}; {c['wfs']}; TC-V12-F-{131+i:03d}.\n\n```gherkin\n"
             f"Feature: {c['name']}\n  Scenario: Happy path within scope\n    Given the tenant has entitlement for {c['wfs'].split(';')[0].strip()[:14]} and the EVAL suite passes for the locale\n"
             f"    And the agent {c['id']} is enabled with an approved PRM version\n    When the trigger occurs: {esc(c['trigger'])[:110]}\n"
             f"    Then a schema-valid output is produced with evidence IDs\n    And the output is handled at autonomy {esc(aut)[:60]}\n"
             f"  Scenario: Guardrail and fallback\n    Given the input contains an injected instruction or out-of-policy content\n    When the agent runs\n"
             f"    Then no effect tool is available and the output is held or routed to a human with a reason code\n"
             f"    And when the budget hard cap is reached the step is HELD and deterministic steps continue\n```\n")
ctl = [("US-04-YF24","AI platform owner","route each AI step to the cheapest Claude tier whose EVAL suite passes for the workflow, language and data class, escalating at most once","cost stays inside DEC-008 without quality regression","AU-152; FR-V12-F-003; TC-V12-F-003",
        "Scenario: One escalation then hold\n    Given Tier 1a and Tier 1b both pass the suite for SM-SVC-06-WF01 in en\n    When a draft is requested\n    Then Tier 1a is chosen\n    When the Tier 1a draft fails schema validation and the remaining run budget covers a Tier 1b call\n    Then exactly one escalation to Tier 1b occurs\n    When the Tier 1b draft also fails\n    Then the step is HELD for a reviewer and no further model call is made"),
       ("US-04-YF25","AI evaluation lead","block any AI step whose EVAL suite is missing or below gate for that locale","only evidenced AI runs in production","AU-154; FR-V12-F-005; TC-V12-F-005",
        "Scenario: Locale-specific block\n    Given EVAL-SM-SVC-09-WF02 passes for en and fails the rubric gate for hi\n    When an hi enquiry reaches the AI step\n    Then the AI step is disabled for hi only and the enquiry goes to the human queue\n    And en enquiries continue to use the agent"),
       ("US-04-YF26","finance lead","see cost per accepted result per workflow and tenant with the rejected outputs in the denominator","AI spend is judged by accepted output, not by calls","AU-158; FR-V12-F-050; TC-V12-F-014",
        "Scenario: Denominator shown\n    Given 100 drafts were produced for SM-SVC-06-WF01 in a month and 80 were accepted\n    When the CPAR report is opened in A117\n    Then CPAR equals total attributable cost divided by 80\n    And the 20 rejected outputs and their cost are shown\n    And any unpriced unit is shown in tokens, not rupees"),
       ("US-03-YF27","compliance lead (R10)","have every external effect pass the send preflight decision table with fixed precedence","no tenant setting can override a jurisdiction hold","AU-171; FR-V12-F-043; TC-V12-F-098",
        "Scenario: Tenant grant cannot override a pack HOLD\n    Given the IN pack returns HOLD for a promotional SMS outside 09:00-21:00 recipient time\n    And the tenant has an action grant allowing the send\n    When the effect adapter requests dispatch\n    Then the verdict is HOLD with reason CJ-IN-06\n    And effect.preflight_verdict is not ALLOW and no provider call occurs"),
       ("US-18-YF28","startup head (R02)","approve an exact action and have any later change to it rejected","approvals cannot be reused for a different payload","AU-175; FR-V12-F-035; TC-V12-F-184",
        "Scenario: Stale approval rejected\n    Given an approval bound to payload digest D1 and policy version P3\n    When the payload changes to digest D2 before execution\n    Then execution is rejected with reason approval_stale\n    And a new approval is requested\n    And no mandate can substitute for an R3 financial or legal approval"),
       ("US-04-YF29","tenant administrator","have my tenant's AI jobs protected from another tenant's bulk jobs","interactive latency stays within target","AU-160; FR-V12-F-016; TC-V12-F-016",
        "Scenario: Noisy neighbour\n    Given tenant A submits 5,000 batch jobs\n    When tenant B makes an interactive request\n    Then tenant B's request is scheduled ahead of tenant A's batch jobs\n    And tenant B's p95 latency stays within the agent card target")]
for us, who, want, so, tr, sc in ctl:
    S.append(f"##### {us}\n\n**As** {who}, **I want** to {want}, **so that** {so}. Traces: {tr}.\n\n```gherkin\nFeature: {us}\n  {sc}\n```\n")
w("t_us.md", "\n".join(S))

# ---------------- test cases ----------------
TC = {}
for a in T.A:
    for t in re.findall(r"TC-V12-F-(\d{3})(?:…(\d{3}))?", a[8]):
        n = int(t[0])
        if n >= 200: continue
        TC.setdefault(n, (a[3], a[4]))
def ttype(s):
    s = s.lower()
    if "ai-inj" in s or "ctrl-ai" in s or "secret" in s or "tool" in s: return "SEC/AIE"
    if any(k in s for k in ("consent", "dsar", "breach", "jurisdiction", "cj-", "minor", "dlt", "preflight")): return "PRV/FUN"
    if any(k in s for k in ("cost", "budget", "cache", "batch", "cpar", "price")): return "CST/AIE"
    return "AIE/FUN"
L = ["| TC | Type | Source aspect | Objective (V12 requirement) | Expected result | Negative / edge case included |", "|---|---|---|---|---|---|"]
for n in sorted(TC):
    aid, summ = TC[n]
    if "acceptance: " in summ: exp = summ.split("acceptance: ")[1]
    elif summ.startswith("Step class"): exp = "CI static check: " + summ.split("test: ")[1]
    elif summ.startswith("AI-INJ"): exp = "0 policy violations, 0 tool calls, flag logged (CTRL-AI-09)"
    elif "OPT-TC" in summ or "MT-TC" in summ: exp = re.split(r"(?:OPT|MT)-TC-[A-Z]+-\d+:? ?", summ)[-1] or "Fixture passes"
    elif "→" in summ: exp = "Verdict " + summ.split("→ ")[-1]
    elif summ.startswith("CJ-R"): exp = "Rule enforced at effect time; violating case HOLD/REVIEW with reason code; evidence stored"
    else: exp = "Requirement met on fixture; violating case held with reason code"
    neg = "Yes: violating input held/blocked with reason code"
    L.append(f"| TC-V12-F-{n:03d} | {ttype(summ)} | {aid} | {esc(summ)[:170]} | {esc(exp)[:120]} | {neg} |")
for i, c in enumerate(CD.CARDS):
    L.append(f"| TC-V12-F-{131+i:03d} | AIE/SEC | {c['id']} | {c['id']} on its EVAL suites ({esc(c['wfs'])}): {esc(c['evals'])} | Gates met; guardrail '{esc(c['guard'])[:70]}…' holds | Yes: injection, out-of-scope, budget hard cap, provider outage |")
for i, r in enumerate(AUD.AU):
    L.append(f"| TC-V12-F-{160+i:03d} | FUN/SEC | {r[0]} | {esc(r[1])}: {esc(r[5])[:120]} | {esc(r[10])} | Yes: {esc(r[9])[:60]} |")
w("t_tc.md", "\n".join(L) + "\n")
json.dump(dict(fr=len(FR), us=len(S), tc=len(L) - 2), open(os.path.join(OUT, "counts2.json"), "w"))

# ---------------- assemble ----------------
def assemble(tmpl, out, label):
    s = open(os.path.join(HERE, tmpl)).read()
    s = re.sub(r"<!--INC:([\w.]+)-->", lambda m: open(os.path.join(OUT, m.group(1))).read().rstrip("\n"), s)
    open(os.path.join(BP, out), "w").write(s)
assemble("F_part_a.tmpl.md", "Part-11-6a_V12_AI_Engines_Agents_Models_Evaluation_RAG_Policy_Cost.md", "a")
if os.path.exists(os.path.join(HERE, "F_part_b.tmpl.md")):
    assemble("F_part_b.tmpl.md", "Part-11-6b_V12_AI_Engines_Agents_Models_Evaluation_RAG_Policy_Cost.md", "b")
print(len(FR), "FRs;", len(S), "stories;", len(L) - 2, "TCs")
