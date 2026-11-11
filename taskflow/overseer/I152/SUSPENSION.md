# SUSPENSION.md — overseer I152

## Self-suspend: waiting for forked DAGs

This iteration self-suspends while two DAGs run:
- **review-design-ferric-1_0-r4** (swe-reviewer; forked this iteration)
- **pin-image-digest-r1** (swe-coder; forked I151)

## Resumption condition

```yaml
resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-03T19:02:00Z" }
    - { member: forked-thread-completion, forked_thread: "review-design-ferric-1_0-r4" }
    - { member: forked-thread-completion, forked_thread: "pin-image-digest-r1" }
  deadline: null
```

Wake whichever fires first: the bounded 60-minute interval (to re-check stalled DAGs) or either forked thread reaching terminal.
