# SUSPENSION.md — overseer/I235

**Suspended at**: 2026-11-04T10:10:00Z  
**Reason**: ferric-http-r1 DAG forked; waiting for DAG to complete before I236 can fold result.

## Resumption condition

```yaml
resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-04T10:30:00Z" }
    - { member: forked-thread-completion, forked_thread: "ferric-http-r1" }
  deadline: null
```

Whichever fires first: the 20-minute bounded timer OR the ferric-http-r1 DAG reaching terminal state.

## On wake

I236 reads this suspension record and I235's CONTINUE.md, then checks `taskflow/dags/ferric-http-r1/SYNTHESIS.md`.
