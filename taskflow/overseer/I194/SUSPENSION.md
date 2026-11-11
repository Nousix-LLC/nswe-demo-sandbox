# SUSPENSION.md — overseer/I194

**Purpose**: bounded re-evaluate wake while ferric-epic-authoring-r1 DAG runs.

```yaml
resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-03T23:05:00Z" }
    - { member: forked-thread-completion, forked_thread: "ferric-epic-authoring-r1" }
  deadline: null
```

**Rationale**: T02 fully folded (PASS, issue #139 closed). T03–T06 unblocked but not yet dispatched. 
Root SYNTHESIS.md not yet present. Pacing: re-evaluate in 10 min or on DAG fold, whichever first.
