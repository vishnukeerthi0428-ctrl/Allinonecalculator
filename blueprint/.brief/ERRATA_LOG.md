# Errata and cross-part inconsistencies (to resolve in Part 9)

## From Part 5.2
1. Part 0 §0.10.2 maps A046 to EP-08; Part 2.1 maps it to EP-10. Part 5.2 follows Part 2.1 (CONFLICT-135). Proposed resolution: Part 2.1 governs; correct Part 0's epic map.
2. Part 0's epic map omits W08/W09 from EP-11. Proposed resolution: add them.
3. BRL-BID-01 buffer vs DEC-053/FR-DM-02 (CONFLICT-133). Proposed resolution: the buffer is a soft warning, with a hard block at the true deadline; recording evidence of a submission made before the deadline is always allowed.
4. BRL-MTG-02 fixed 15-minute hold vs WCAG 2.2.1 (CONFLICT-134). Proposed resolution: a 15-minute default hold, extendable once by 15 minutes on user request, with a warning 60 s before expiry.
5. The order state machine lacks a reservation-expiry transition (ASSUMPTION-166). Proposed resolution: add Approved → ReservationExpired → Draft.
6. DEC-064 sets no cap for first-touch outreach (GAP-156). Proposed resolution: first-touch is L1 until the template is approved, then up to L2.

## From Part 5.3
7. CONFLICT-136: Part 0 puts BR-M09 in EP-01; Part 1 puts it in EP-21. Resolution: Part 1 governs (EP-21).
8. CONFLICT-137: Part 0 has W08–W10 under EP-19; Part 2.1 has W08/W09 under EP-11 and W10 under EP-12. Resolution: Part 2.1 governs.
9. CONFLICT-138: FR-A103 import is in W1 but traced to BR-SVC (Should). Resolution: trace the import capability to BR-TENANT (Must, W1) as well; the portability export stays with BR-SVC (W5).
10. BR-M61 (Must) depends on BR-M60 (Could). Resolution: M61 needs only M60's forecast *display slot*; without M60 the Command Centre shows "Forecast not enabled". The dependency is soft.
11. FR-W22 is a W2 screen whose order and invoice data arrives in W4. Resolution: in W2 it shows only enquiries, meetings and documents; its cards are enabled progressively.
12. Part 2.4 has no notification for losing custom-domain verification. Resolution: add NT-046 "Domain verification lost / certificate expiring" (High; R12, R05L).
13. Parts 5.2 and 5.3 cite "Part 5.1 §5.x" placeholders; resolve them after 5.1 lands.
