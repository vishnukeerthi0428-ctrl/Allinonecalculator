| V12 candidate | Method | Path | Result / contract | Blueprint operation(s) | Relation | Before | Enhancement |
|---|---|---|---|---|---|---|---|
| MT-API-01 | POST | `/api/v1/tenants/applications` | Validated SM-APPLICATION-6 envelope; 202 pending; no entitlement | API-503; API-506 | Alias | Covered | — |
| MT-API-02 | POST | `/api/v1/tenants/{id}/companies` | Authorized tenant admin; org FK, company version; 201 pending | API-030 | Alias | Covered | — |
| MT-API-03 | GET | `/api/v1/companies/{id}/configuration` | Versioned scoped graph; no CRM payload | API-038; API-002 | Alias | Covered | — |
| MT-API-04 | POST | `/api/v1/companies/{id}/configuration/drafts` | Draft ID and diff; 409 stale | API-039; API-040 | Alias | Covered | — |
| MT-API-05 | POST | `/api/v1/configuration/{id}/review` | Independent reviewer; approved version or reject | API-541; API-539 | Approval | Covered | — |
| MT-API-06 | POST | `/api/v1/configuration/{id}/rollback-draft` | New draft version; re-review; no automatic restore | API-043 | Partial | Partially covered | (semantic amendment of API-043, §11.8.5.3) |
| MT-API-07 | GET | `/api/v1/context/options` | Only permitted descendants; no stale selection | API-014 | Alias | Covered | — |
| MT-API-08 | POST | `/api/v1/workflow-runs` | BusinessContext DTO; run ID/hold reason; no duplicate effect | API-456; API-449 | Partial | Partially covered | API-V12-H-068 |
| MT-API-09 | GET | `/api/v1/metrics/business` | Native and converted totals with rate version and missing rates | API-537; API-388 | Partial | Partially covered | API-V12-H-064 |
| MT-API-10 | POST | `/api/v1/portfolio/grants` | Grant/revoke aggregate scope; independent clients excluded | API-021 | Partial | Partially covered | API-V12-H-063 |
| OPT-API-01 | POST | `/api/v1/optimization/preflight` | Plan/hold, gate reasons, cost estimate; no external effect | API-449; API-455 | Partial | Partially covered | API-V12-H-068 (dry_run) |
| OPT-API-02 | GET | `/api/v1/optimization/cost-summary` | Meter categories, allocated/unallocated cost, accepted denominator | API-136 | Partial | Partially covered | API-V12-H-065 |
| OPT-API-03 | GET | `/api/v1/optimization/health` | SLO/SLI, incident status, freshness | API-119 | Alias | Covered | — |
| OPT-API-04 | POST | `/api/v1/optimization/feedback` | Case revision and state; dedupe by idempotency key | API-149; API-418 | Alias | Covered | — |
| OPT-API-05 | GET | `/api/v1/optimization/customer-value` | Accepted output, usage, value assumption, renewal state | API-513; API-514 | Partial | Partially covered | API-V12-H-066 |
| OPT-API-06 | POST | `/api/v1/private/application-drafts` | Private draft ID/revision; authenticated, replay protected | API-504; API-ENH-D-019 | Alias | Covered | — |
| OPT-API-07 | POST | `/api/v1/optimization/model-evaluations` | Evaluation reference, quality/cost/latency, pending promotion | API-138; API-148 | Alias | Covered | — |
| OPT-API-08 | GET | `/api/v1/operator/conversion-metrics` | Funnel counts, attribution quality, acquisition cost; aggregate only | API-537 | Partial | Partially covered | API-V12-H-067 |
| API-V2-RUN | POST | `/api/v2/workflow-runs` | {service_id,workflow_id,version,input,mode,idempotency_key} → 202 {run_id,state} | API-456 | New | Not covered | API-V12-H-068 |
| API-V2-RESULT | GET | `/api/v2/workflow-runs/{id}` | {state,step_states,result_ref,error,usage} | API-467 | Alias | Partially covered | API-V12-H-069 |
| API-V2-APPROVAL | POST | `/api/v2/workflow-runs/{id}/approvals` | {action_digest,decision,expiry,expected_version} → approval_ref | API-541; API-539 | Approval | Partially covered | API-V12-H-070 |
| API-V2-CANCEL | POST | `/api/v2/workflow-runs/{id}/cancel` | {expected_version,reason} → state; reconcile effects | API-471 | Alias | Partially covered | API-V12-H-071 |
| API-V2-CATALOG | GET | `/api/v2/public/services` | Released neutral SKU projection; public read only | API-501 | Alias | Covered | (route alias RA-V12-H-01) |
| API-V2-INTAKE | POST | `/api/v2/public/enquiries` | {contact,selected_skus,consent,requirements} → opaque receipt | API-212; API-229 | Alias | Covered | (route alias RA-V12-H-02) |
| API-V2-WEBHOOK | POST | `/api/v2/connectors/{kind}/events` | Provider signed payload → accepted event receipt | API-483 | Partial | Partially covered | API-V12-H-073 |
| V4-API-01 | POST | `/api/v1/commercial/applications` | Application DTO + revision + digest; 201 or 409/422 | API-503 | Alias | Covered | — |
| V4-API-02 | PUT | `/api/v1/commercial/applications/{id}` | Compare expected revision; reject stale or provisioned change | API-504 | Alias | Covered | — |
| V4-API-03 | GET | `/api/v1/commercial/applications/{id}` | Minimal authorized configuration | API-507; API-ENH-D-019 | Alias | Covered | — |
| V4-API-04 | POST | `/api/v1/commercial/workflow-runs` | Run ID, state, reservation, correlation | API-456 | Partial | Partially covered | API-V12-H-068 |
| V4-API-05 | POST | `/api/v1/commercial/workflow-runs/{id}/decisions` | Approval/hold result; 403/409 on denied/stale | API-541; API-539 | Approval | Covered | API-V12-H-070 (v2 spelling) |
| V4-API-06 | GET | `/api/v1/commercial/workflow-runs/{id}/steps` | Step status list, no provider secrets | API-467 | Alias | Partially covered | API-V12-H-072 |
| V4-API-07 | PATCH | `/api/v1/commercial/domain-records/{id}` | New version; reset review; 409 stale | Per-entity PATCH operations (e.g. API-480, API-485, API-ENH-D-001) | Split | Covered | — |
