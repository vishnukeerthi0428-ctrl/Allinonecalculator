#!/usr/bin/env python3
"""Group P (Part 11.17) aspect register -> final/coverage_v12/P_coverage.csv and a
Markdown register fragment. Aspects were read line by line from the V12 BRD/FSD
chapters listed in Part 11.17 §11.17.1; status_before records the blueprint
position before DEC-779/780/781 (Part 11.14)."""
import csv, sys, os, collections
A = []
def a(doc, ch, sec, aid, summ, before, loc, action, new, after="Matched"):
    A.append(dict(doc=doc, chapter=ch, section=sec, aspect_id=aid, aspect_summary=summ, status_before=before,
                  blueprint_location=loc, action=action, new_ids=new, status_after=after))
PF = "Pending Founder (now DEC-779)"
# ---- BRD 18 / FSD 18 authority
a("BRD","18","V5 authority","P-AUT-L0","L0 Manual action recorded","Covered","Part 7.3 §7.6.1 L0; Part 11.1b §11.1.5.7","Map to controls matrix","FR-V12-P-001")
a("BRD","18","V5 authority","P-AUT-L1","L1 AI proposes or drafts; human decides","Covered","Part 7.3 §7.6.1 L1","Map to controls matrix","FR-V12-P-001")
a("BRD","18","V5 authority","P-AUT-L2","L2 Exact approved action with reviewer, expiry and limits","Covered","BRL-APR-02/03; Part 11.1b crosswalk","Controls matrix L2 row; exact-item approval path","FR-V12-P-002")
a("BRD","18","V5 authority","P-AUT-L3","L3 Bounded routine actions under approved mandate, scope, expiry and caps","Conflict","CONFLICT-762, 798, 799, 814","Mandate engine specified (§11.17.5)","FR-V12-P-003; DEC-841")
a("BRD","18","V5 authority","P-AUT-L4","L4 Adaptive orchestration inside L3 constraints; never expands authority","Conflict","CONFLICT-762","L4 plan binding to an L3 mandate; authority-expansion guard","FR-V12-P-004; DEC-841")
a("BRD","18","V5 authority","P-AUT-R3DEF","R3 financial/legal/commitment actions default L2; regulatory or contractual requirements override automation preference","Partially covered","DEC-064; Part 11.1b FR-V12-A-110/111","Default level per effect class; rule-pack override","FR-V12-P-005")
a("BRD","18","V5 authority","P-AUT-SIM","No simulation external effect","Covered","BRL-AUT-04","Mandate shadow mode reuses simulation","FR-V12-P-028")
a("BRD","18","V5 authority","P-AUT-STOP","Emergency stop revokes future effects; uncertain completed effects reconciled","Covered","BRL-AUT-05; DEC-050","Kill switch matrix incl. mandate scope","FR-V12-P-053…058")
a("BRD","18","V5 FL-09","P-FL09-REQ","FL-09 P0 Persistent approval mandates: bind actor, resource, payload digest, action, amount, policy, expiry and revocation","Conflict","CONFLICT-854; AU-175","Mandate object fields §11.17.5.3","FR-V12-P-006…012; AU-260")
a("BRD","18","V5 FL-09","P-FL09-AT","OPT-TC-FL-09: changed payload or expired/revoked mandate blocks effect","Partially covered","AU-175 (stale approval)","Combinatorial model M; TC-V12-P-001…300","TC-V12-P-001…300")
a("FSD","18","V5 effect classes","P-R0","R0 read/draft with source rights; no external action","Covered","BRL-AI-07","Controls matrix","FR-V12-P-005")
a("FSD","18","V5 effect classes","P-R1","R1 scoped internal record update; version lock and audit","Covered","BRL-AUT-03","Controls matrix","FR-V12-P-005")
a("FSD","18","V5 effect classes","P-R2","R2 external write; explicit approval or eligible bounded mandate","Conflict","CONFLICT-799, 854","Mandate eligibility register §11.17.5.14","FR-V12-P-013; DEC-841")
a("FSD","18","V5 effect classes","P-R3","R3 financial/legal/commitment; exact approval and finance/legal gate; mandate only if expressly approved and permissible","Conflict","CONFLICT-798, 814, 854","Mandate types MT-COM/MT-PAY/MT-BID with Finance/Legal approver","FR-V12-P-014; DEC-842")
a("FSD","18","V5 approval record","P-APR-BIND","Approval record binds tenant/company, workflow version, action digest, recipient, budget, currency, actor authority, expiry and policy version","Partially covered","AU-175; BRL-APR-02","Mandate digest canonical form","FR-V12-P-008; AU-260")
a("FSD","18","V5 approval record","P-APR-SEP","Separate prepare/approve/execute/reconcile","Covered","Part 2.2 dispatch; FSD 13","Mandated dispatch WF-58","WF-58")
a("FSD","18","V5 approval record","P-APR-RECHK","Recheck revocation, suppression and budget before adapter call","Covered","PDP at dispatch (DEC-012 family)","PDP order §11.17.5.9","FR-V12-P-040…052")
a("FSD","18","V5 approval record","P-APR-CANCEL","Cancellation never hides already-completed action","Covered","DEC-050","Kill switch CompletedUnreconciled path","TC-V12-P-653…716")
a("FSD","18","V6","P-V6-DUAL","Review by authorized actor distinct from requester; approval binds exact version; stale approvals rejected; demo review is not dual control","Partially covered","BRL-APR-01; MT-32","Two-person approval rules","FR-V12-P-015…020; AU-261")
a("FSD","18","V7 MOB-09","P-MOB09","Mobile approvals same verified actor, scope, payload version, spend limits; step-up; no approval from notification","Partially covered","Part 4.1 §4.3.3","Mandate approval on mobile: step-up; no notification approve","FR-V12-P-019")
a("BRD","01/20","BR-C09","P-BRC09","Draft/simulation no external effects; real external actions require exact approval or eligible bounded mandate; high-risk approvals cannot be bypassed","Conflict","CONFLICT-762","Adopted with mandate engine","FR-V12-P-003; DEC-841")
a("BRD","16","Commerce","P-BRD16","No autonomous commitment without mandate, explicit provider approval and reconciliation","Conflict","CONFLICT-762, 778","Commerce/payment mandates via licensed PSP; reconciliation","FR-V12-P-070…098")
a("FSD","12","R3 rows","P-R3-WF","10 R3 workflows SVC-21/28/30/31/32/37/39 and 9 R3 workflows SVC-14/17/18/19/20 carry 'L3 only with separately approved bounded mandate where lawful'","Conflict","CONFLICT-798, 814","Eligibility register §11.17.5.14","FR-V12-P-013, 014")
a("FSD","12","R2 rows","P-R2-WF","12 R2 workflows (SVC-06/07/09/10/12/16) carry the same mandate clause","Conflict","CONFLICT-799","Eligibility register §11.17.5.14","FR-V12-P-013")
a("FSD","13","Registry","P-FSD13","Approve stage: exact digest + mandate; no effect until dispatch","Partially covered","Part 11.4b registry","WF-58 approve/dispatch split","WF-58")
# ---- SVC-28
for wf, nm, inp, out in (("WF01","Machine-readable catalog publication","Approved offering catalog, access policy, structured schema","Machine-readable catalog"),
                         ("WF02","Authorized AI-agent requirement discovery and quotation exchange","Verified agent identity, scoped mandate, requirements","Authorized quote exchange"),
                         ("WF03","Agent-assisted purchasing and negotiation mandate coordination","Mandate, price limits, negotiation policy","Mandate-linked decision"),
                         ("WF04","Authorized transaction, payment mandate and outcome reconciliation","Approved order, verified payment mandate, provider event","Auditable transaction record")):
    before = "Conflict" if wf in ("WF03","WF04") else "Partially covered"
    a("FSD","12","SM-SVC-28-"+wf,"P-28-"+wf+"-IO", nm+": "+inp+" -> "+out, before, "Part 11.4c/d; CONFLICT-816","WF-59 steps; DTO extension","FR-V12-P-070…098; WF-59")
    a("FSD","12","SM-SVC-28-"+wf,"P-28-"+wf+"-STEPS", "Steps STEP-01…03 with failure paths POLICY_DENIED/EFFECT_UNKNOWN/CONFLICT/REVIEW_REQUIRED", before, "Part 11.4d","Mapped to WF-59 step table","WF-59")
    a("FSD","33","SM-SVC-28-"+wf,"P-28-"+wf+"-TC", "TC-POS/INPUT/SCOPE/ENT/DUP/QUALITY/BUDGET/RECOVERY/APPROVAL/EFFECT", "Partially covered","Part 11.10","Traced to TC-V12-P","TC-V12-P-301…523, 717…")
a("FSD","26","agent_transaction","P-28-DTO","DTO agent_ref, mandate_ref, offering_ref, order_ref -> quote_ref, mandate_state, transaction_ref, reconciliation_state","Partially covered","Part 11.9a","Enum values defined; entity model §11.17.9","FR-V12-P-099")
a("BRD","08","SM-SVC-28","P-28-ACC","Verified mandate and idempotency 100%; unauthorized transactions = 0","Partially covered","Part 11.2b","KPI KPI-P-01/02","KPI-P-01, KPI-P-02")
a("BRD","08","SM-SVC-28","P-28-RISK","Verify agent identity, mandate, spending limits and approval before any transaction; reconcile via authorized provider","Conflict","CONFLICT-778","PDP order + PSP adapter","FR-V12-P-040…052, 080…090")
a("BRD","08","SM-SVC-28","P-28-PROV","Supported agent protocols and authorized payment/commerce providers; verified mandates","Not covered","—","Protocol adapter + PSP registry","FR-V12-P-070…075; ADR-242, 243")
a("BRD","08","SM-SVC-28","P-28-METER","Meter: agent transaction case; pilot allowance 50 (not approved)","Partially covered","Part 11.2a","Metering unit adopted","FR-V12-P-099")
a("FSD","15","V5","P-15-INTEROP","External agent interoperability off until validated signed mandate and scoped contract","Partially covered","CONFLICT-854","Interop gate FR-V12-P-076","FR-V12-P-076")
a("FSD","16","16.5","P-INJ06","AI-INJ-06 counterparty agent asks to exceed mandate -> signed mandate limits; hold above cap","Not covered","Part 11.6a F16-044","AI eval TC-AI-AG202/203","TC-AI-AG202-004")
a("FSD","16","16.5","P-CTRL08","CTRL-AI-08 SM-SVC-28 mandates signed with limits; counterparty messages are untrusted data","Not covered","Part 11.6a F16-058","Signed mandate + JWS envelope","FR-V12-P-008, 072")
a("FSD","20","Website fixtures","P-W-28","Website fixtures: quote only after verified mandate and identity; mandate review max sample spend ₹2,000; no payment made; reconcile before replay","Partially covered","Part 11.7","Demo fixtures reused in TC data","TC-V12-P-717…")
a("FSD","20","Website fixtures","P-W-14","SM-SVC-14-WF02 activation held: no approved spend mandate","Partially covered","Part 11.7","Spend mandate type MT-SPEND","FR-V12-P-013")
a("FSD","20","Website fixtures","P-W-39","SM-SVC-39-WF03 purchase proposal: approved mandate and signatory missing","Partially covered","Part 11.7","MT-PROC mandate type","FR-V12-P-013")
a("FSD","21","Domain panel","P-21-28","SVC-28 panel: Mandate reference; Counterparty / transaction; Spending limit; Approval state; Review mandate; evidence: Mandate version; Recipient / approval reference; Transaction reconciliation","Partially covered","A172 (Part 11.7b)","Screens A260…A267","A260…A267")
# ---- SVC-19-WF03
a("FSD","12","SM-SVC-19-WF03","P-19-AUTH","R3; L2 mandatory approved effect; L3 only with bounded mandate where lawful; capability grant and explicit bid approval; no automatic submission to restricted portal","Conflict","CONFLICT-781, 800","Per-tender mandate MT-BID; portal capability registry","FR-V12-P-110…135; DEC-851")
a("FSD","12","SM-SVC-19-WF03","P-19-STEPS","STEP-01 draft; 02 validate attachments; 03 route approval; 04 coordinate authorized submission and track receipt","Conflict","CONFLICT-800","WF-60 steps","WF-60")
a("FSD","12","SM-SVC-19-WF03","P-19-KPI","Attachment completeness; verified receipt rate; unapproved bid submissions = 0","Partially covered","AU-034","KPI-P-06…08","KPI-P-06…08")
a("FSD","11","SM-SVC-19","P-19-PROV","Authorized tender feeds/portal and account; manual submission unless permitted API","Conflict","CONFLICT-781","Portal capability registry modes","FR-V12-P-118…122")
a("FSD","40","QC-26","P-QC26","Verify tender eligibility, deadline, budget, technical requirements and authorized bid submission; track award separately","Partially covered","BRL-BID-02/05","Pre-submission gate","FR-V12-P-112")
a("FSD","12","SM-SVC-19-WF03","P-19-DTO","DTO deadline RFC 3339; submission_ref output","Partially covered","Part 11.3","Receipt model","FR-V12-P-125")
# ---- blueprint-internal amendments
for rid, txt in (("BRL-AI-07","No AI consequential action"),("BRL-AUT-01","Autonomy caps DEC-064"),("BRL-BID-04","Human submission"),
                 ("BRL-BID-01","Deadline buffer"),("BRL-FIN-07","No card/bank credentials"),("BRL-APR-07","Finance maker-checker"),
                 ("DEC-053","Tender submission never automated"),("DEC-064","Autonomy cap matrix"),("X-06","Payments never")):
    a("Blueprint","—",rid,"P-AMD-"+rid, "Amend/scope "+rid+" ("+txt+") for actions under an Active mandate", "Conflict" if rid in ("BRL-AI-07","BRL-AUT-01","BRL-BID-04","DEC-053","DEC-064","X-06") else "Covered",
      "Part 2.3 / Part 0A / Part 7","Amendment text §11.17.4.2","DEC-841, 848, 851")
def main(out_csv, out_md):
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(A[0]))
        w.writeheader(); w.writerows(A)
    cb = collections.Counter(x["status_before"] for x in A)
    ca = collections.Counter(x["status_after"] for x in A)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("| Aspect | Source | Summary | Before | Blueprint location (before) | Action | New IDs | After |\n|---|---|---|---|---|---|---|---|\n")
        for x in A:
            f.write("| %s | %s %s · %s | %s | %s | %s | %s | %s | %s |\n" % (x["aspect_id"], x["doc"], x["chapter"], x["section"],
                    x["aspect_summary"].replace("|","/"), x["status_before"], x["blueprint_location"], x["action"], x["new_ids"], x["status_after"]))
    print(len(A), dict(cb), dict(ca))
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
