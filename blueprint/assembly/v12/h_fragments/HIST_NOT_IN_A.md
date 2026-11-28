| Source op | Method | Path | Purpose | Blueprint op(s) |
|---|---|---|---|---|
| SM-OP-017 | GET | `/api/v1/public/preferences/{token}` | Read scoped preference state | API-083 |
| SM-OP-019 | POST | `/api/v1/opt-out` | Suppress and cancel scheduled sends; enrollment hook when enabled | API-067 |
| SM-OP-033 | POST | `/api/v1/internal/ai/run` | Internal model call with cost reservation | API-134 |
| SM-OP-045 | GET | `/api/v1/health` | Liveness; no database required | API-117 |
| SM-OP-046 | GET | `/api/v1/ready` | Readiness check without sensitive details | API-118 |
| SM-OP-092 | GET | `/api/v1/public/forms/{slug}` | Read published enquiry form | API-228 |
| SM-OP-093 | POST | `/api/v1/public/leads` | Capture valid consented enquiry | API-212 |
| SM-OP-122 | GET | `/api/v1/public/meeting-slots/{token}` | Read scoped available slots | API-272 |
| SM-OP-137 | POST | `/api/v1/public/chat` | Answer approved FAQ and capture consented lead | API-246 |
| SM-OP-164 | GET | `/api/v1/public/pages/{slug}` | Read published landing page | API-290 |
| SM-OP-165 | POST | `/api/v1/public/events` | Record minimized attribution event | API-291 |
| SM-OP-177 | GET | `/api/v1/public/events/{id}` | Read published event | API-326 |
| SM-OP-178 | POST | `/api/v1/events/register` | Register authorized attendee | API-296 |
| SM-OP-182 | POST | `/api/v1/public/referrals` | Submit authorized referral | API-298 |
| SM-OP-196 | GET | `/api/v1/public/agreements/{token}` | Read scoped agreement | API-358 |
| SM-OP-197 | POST | `/api/v1/public/agreements/{token}/sign` | Initiate authorized e-sign provider flow | API-359 |
| SM-OP-203 | GET | `/api/v1/public/payment-status/{token}` | Read scoped payment status | API-409 |
| SM-OP-210 | GET | `/api/v1/public/onboarding/{token}` | Read customer scoped next steps | API-437 |
| SM-OP-289 | GET | `/api/v1/commercial/public/site/pages/{slug}` | Read only currently published approved website snapshot for resolved verified host and locale. | API-290 |
| SM-OP-290 | GET | `/api/v1/commercial/admin/website/pages` | List startup-owned website drafts and publications. | API-486 |
| SM-OP-291 | POST | `/api/v1/commercial/admin/website/pages` | Create immutable draft or edit by creating next draft revision. | API-487;API-488 |
| SM-OP-292 | POST | `/api/v1/commercial/admin/website/pages/{id}/control` | Validate/preview/submit/approve/publish/unpublish or rollback approved revision. | API-489;API-490;API-492;API-494;API-495;API-541;API-539 |
| SM-OP-295 | POST | `/api/v1/commercial/portal/external-grants/accept` | Redeem a one-time invitation after identity verification; bind grant to authenticated external identity. | API-013 |
| SM-OP-296 | POST | `/api/v1/commercial/portal/documents` | Request upload for a specifically granted onboarding or project request; never knowledge ingestion. | API-235 |
| SM-OP-297 | POST | `/api/v1/commercial/portal/documents/{id}/complete` | Complete own quarantined document upload and enqueue scan. | API-236; API-ENH-D-018 |
| SM-OP-298 | GET | `/api/v1/commercial/portal/overview` | Own customer dashboard with authorized lead, agreement, order and onboarding summaries. | API-436 |
| SM-OP-299 | GET | `/api/v1/commercial/portal/quotations/{id}` | Read approved recipient-specific quote/proposal. | API-354;API-355 |
| SM-OP-300 | POST | `/api/v1/commercial/portal/quotations/{id}/respond` | Accept or request revision of an approved quotation; creates internal review event. | API-356;API-357 |
| SM-OP-301 | GET | `/api/v1/commercial/portal/orders/{id}` | Own order or project fulfillment status. | API-382 |
| SM-OP-302 | POST | `/api/v1/commercial/portal/requests` | Own support, feedback, renewal or privacy request with typed kind. | API-440;API-069 |
