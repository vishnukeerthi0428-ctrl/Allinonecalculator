"""Assumptions for building the application with AI models and AI agents (agentic development).

Three cases. 'optimistic' and 'conservative' bound the estimate; 'central' is the planning case.
All factors are planning assumptions, to be calibrated against measured throughput at the Sprint 2 calibration gate.
"""

CASES = ("optimistic", "central", "conservative")

# Effort reduction on each activity when AI agents do the drafting/coding and humans supervise.
# (activity, optimistic, central, conservative, agent-executed share of the traditional effort, what the AI does, what humans still do)
ACCEL = [
    ("Requirements analysis, backlog and user-story drafting", 0.70, 0.55, 0.40, 0.60,
     "Drafts and refines stories, Gherkin AC and estimates from the blueprint drafts", "PO prioritizes and accepts; growth lead checks rules"),
    ("UX/UI design and accessibility", 0.35, 0.25, 0.15, 0.20,
     "Generates screen variants, copy, component code from the design system; accessibility checks", "Designer owns IA, flows, usability tests and final design"),
    ("Architecture, security and data design", 0.30, 0.20, 0.10, 0.15,
     "Drafts ADRs, schemas, threat-model checklists, IaC skeletons", "Lead architect decides; independent reviewer signs off"),
    ("Backend development (APIs, rules, workflows, data)", 0.65, 0.55, 0.35, 0.60,
     "Coding agents implement APIs, rules, migrations and workflows from specs and tests", "Engineers write specs, review every pull request, own design and merges"),
    ("Frontend development (Website and Admin)", 0.65, 0.55, 0.35, 0.60,
     "Agents build React screens from the screen contracts and design system", "Engineers review, fix edge cases, verify accessibility"),
    ("AI engineering (agents, gateway, RAG, evaluations)", 0.40, 0.30, 0.20, 0.35,
     "Drafts prompt contracts, eval sets, fixtures; scaffolds agents", "AI engineer owns guardrails, routing, evaluation thresholds"),
    ("Test strategy and test-case drafting", 0.75, 0.65, 0.50, 0.70,
     "Generates test cases, data and traceability from stories and FRs", "QA lead reviews coverage and risk focus"),
    ("Test automation and execution (unit, SIT, UAT, performance, security)", 0.50, 0.40, 0.30, 0.50,
     "Writes unit/API/UI tests, triages failures, proposes fixes", "QA executes UAT with users; performance and pen tests unchanged"),
    ("DevOps, infrastructure, observability and release", 0.45, 0.35, 0.25, 0.40,
     "Writes IaC, pipelines, dashboards and runbooks", "DevOps engineer approves changes to production"),
    ("Project management, ceremonies and reporting", 0.25, 0.15, 0.10, 0.10,
     "Status summaries, burn-down analysis, meeting notes", "Lead and PO run ceremonies and decisions"),
    ("Documentation, training content and handover", 0.70, 0.60, 0.45, 0.60,
     "Drafts docs, runbooks, task cards and release notes", "Owners review for accuracy"),
]

# New work that exists only because AI agents build the software (as % of traditional effort).
# (overhead, optimistic, central, conservative, description)
OVERHEAD = [
    ("Agent orchestration, specification and prompt engineering", 0.03, 0.04, 0.06, "Writing precise specs, acceptance tests and task prompts for agents; managing agent runs"),
    ("Human review and verification of AI output", 0.05, 0.07, 0.10, "Every pull request reviewed by an engineer; spot checks of generated tests and docs"),
    ("Security, licence and provenance review of AI-generated code", 0.01, 0.015, 0.02, "SAST, dependency and licence scans, secret checks, provenance log"),
    ("Rework allowance for AI defects", 0.02, 0.03, 0.05, "Fixing subtle defects that pass review and surface in SIT/UAT"),
]

# Agent token economics (per person-day of work executed by agents), USD, list prices to verify.
MODEL_PRICES = {  # per million tokens: input, cached-input read, output
    "Opus-class": (5.0, 0.50, 25.0),
    "Sonnet-class": (3.0, 0.30, 15.0),
    "Haiku-class": (1.0, 0.10, 5.0),
}
MODEL_MIX = {"Opus-class": 0.20, "Sonnet-class": 0.70, "Haiku-class": 0.10}
TOKENS_PER_AGENT_PD = dict(input_m=4.0, cached_share=0.80, output_m=0.20)
TOKEN_MULT = {"optimistic": 0.5, "central": 1.0, "conservative": 3.0}   # retries, parallel exploration, long contexts


def usd_per_agent_pd():
    t = TOKENS_PER_AGENT_PD
    tot = 0.0
    for m, share in MODEL_MIX.items():
        pin, pc, pout = MODEL_PRICES[m]
        c = t["input_m"] * (1 - t["cached_share"]) * pin + t["input_m"] * t["cached_share"] * pc + t["output_m"] * pout
        tot += share * c
    return tot


# AI build tooling per month (USD, list prices to verify), in addition to the approved DEC-419 tooling where noted
AI_TOOLS = [
    ("Claude Max 20x for engineers who supervise coding agents", "Higher usage limits for continuous Claude Code sessions", 200, 200, 5, "Replaces Max 5x in DEC-419 for engineers", 2),
    ("Claude Pro for QA, growth/compliance lead and PO", "Drafting, review, test data", 20, 20, 3, "As DEC-419", 2),
    ("CI runners and agent sandboxes", "Ephemeral environments where agents build and test branches safely", 50, 200, 1, "GitHub larger runners or AWS dev sandboxes", 1),
    ("Agent observability (self-hosted Langfuse, dev instance)", "Traces, cost and quality of build agents", 25, 30, 1, "Hosting only; open source", 1),
    ("Static analysis and licence scanning", "Semgrep/SonarQube Community, Trivy, licence checker", 0, 0, 1, "Open source", 1),
]
# DEC-419 tooling other than Claude stays the same (GitHub, Figma, Workspace, Bitwarden, BrowserStack, domains)

# Team for the AI-built option A (same dates, smaller team). Indicative composition.
AI_TEAM = [
    ("Engineering lead / solutions architect", 1.0, "Specs, architecture, final review, merges"),
    ("Senior full-stack engineers supervising coding agents", 3.0, "Write specs and acceptance tests, review agent pull requests"),
    ("Contract engineer (Sprint 3 → Release 2 gate)", 1.0, "Down from 2 in the traditional plan"),
    ("QA lead (AI evaluation and test review)", 1.0, "From Sprint 3, as approved"),
    ("Growth / compliance lead", 0.5, "0.75 in W4–W5, as approved"),
    ("UX designer (contract)", 0.35, "Reduced: agents generate variants from the design system"),
    ("Independent reviewer (architecture and AI-code security)", 0.1, "Extra focus on AI-generated code"),
]
TRAD_TEAM_PEAK = 8.5

MAINT_PCT_AI = (0.12, 0.17)   # maintenance % of cumulative development per year with AI agents (vs 15–20%)
