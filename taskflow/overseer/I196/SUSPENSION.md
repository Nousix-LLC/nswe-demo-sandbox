# SUSPENSION.md — overseer/I196

**Node**: overseer/I196  
**Suspended at**: 2026-11-03T23:50:00Z  

## Reason

Board check complete. ferric-epic-authoring-r1 DAG running (T04+T05 dispatched and running since 23:22-23Z; no COMPLETE.md yet). No new GitHub activity. No action to take until DAG progresses or folds.

## Resumption condition

```yaml
resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-04T00:00:00Z" }
    - { member: forked-thread-completion, forked_thread: "ferric-epic-authoring-r1" }
  deadline: null
```

Wake on whichever fires first: 10-minute bounded timer OR ferric-epic-authoring-r1 reaching terminal state.
