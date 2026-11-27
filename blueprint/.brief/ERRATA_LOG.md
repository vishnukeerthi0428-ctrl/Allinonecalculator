# Errata and cross-part inconsistencies (to resolve in Part 9)

## From Part 5.2
1. Part 0 §0.10.2 maps A046 to EP-08; Part 2.1 maps it to EP-10. Part 5.2 follows Part 2.1 (CONFLICT-135). Proposed resolution: Part 2.1 governs; correct Part 0's epic map.
2. Part 0's epic map omits W08/W09 from EP-11. Proposed resolution: add them.
3. BRL-BID-01 buffer vs DEC-053/FR-DM-02 (CONFLICT-133). Proposed resolution: the buffer is a soft warning, with a hard block at the true deadline; recording evidence of a submission made before the deadline is always allowed.
4. BRL-MTG-02 fixed 15-minute hold vs WCAG 2.2.1 (CONFLICT-134). Proposed resolution: a 15-minute default hold, extendable once by 15 minutes on user request, with a warning 60 s before expiry.
5. The order state machine lacks a reservation-expiry transition (ASSUMPTION-166). Proposed resolution: add Approved → ReservationExpired → Draft.
6. DEC-064 sets no cap for first-touch outreach (GAP-156). Proposed resolution: first-touch is L1 until the template is approved, then up to L2.
