# SUSPENSION.md — overseer I348

Suspended waiting for I349 scheduled wake or DAG fold.

resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-06T06:50:00Z" }
    - { member: forked-thread-completion, forked_thread: "chirp-logged-out-r12" }
  deadline: null
