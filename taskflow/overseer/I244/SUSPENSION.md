# SUSPENSION.md — overseer I244

**Reason**: No clearing condition met for PR #210 escalation. Re-suspending to give user time to respond.

resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-04T21:30:00Z" }
  deadline: null

**On wake**: I245 evaluates PR #210 for user response (retry-review / approve / close).
