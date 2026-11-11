# SUSPENSION.md — overseer I189

**Suspended at**: 2026-11-03T21:45:00Z

resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-03T21:55:00Z" }
    - { member: forked-thread-completion, forked_thread: "ferric-epic-authoring-r1" }
  deadline: null

**Reason**: ferric-epic-authoring-r1 DAG still running; no other board activity. Wakes on fold or timer, whichever first.
