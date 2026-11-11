# SUSPENSION.md — overseer I190

**Suspended at**: 2026-11-03T22:18:00Z
**Reason**: ferric-epic-authoring-r1 DAG still running; no new GitHub activity; nothing else to act on.

resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-03T22:28:00Z" }
    - { member: forked-thread-completion, forked_thread: "ferric-epic-authoring-r1" }
  deadline: null
