# SUSPENSION.md — overseer I296

Suspending on bounded watch for chirp-logged-out DAG fold or +20 min schedule, whichever fires first.

resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-05T00:20:00Z" }
    - { member: forked-thread-completion, forked_thread: "chirp-logged-out" }
  deadline: null
