# SUSPENSION.md — I191

**Status**: suspended
**Reason**: ferric-epic-authoring-r1 DAG still running (progressing, not yet folded). No action needed until fold or bounded wake.

resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-03T22:40:00Z" }
    - { member: forked-thread-completion, forked_thread: "ferric-epic-authoring-r1" }
  deadline: null
