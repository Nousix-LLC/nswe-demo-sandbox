# SUSPENSION.md — overseer I211

**Suspended at**: 2026-11-04T05:35:00Z
**Reason**: Both forked DAGs (ferric-async-forms-r2, ferric-router-r1) are still RUNNING. No folds detected.
No new GitHub activity. No board hygiene issues found. No action to take until a DAG folds or the routine timer fires.

## State at suspension

- ferric-async-forms-r2: RUNNING (remediation attempt 2 of 2)
- ferric-router-r1: RUNNING (attempt 1)
- free_dag_slots: 2 (both taken)
- open PRs: 0
- last GitHub activity: 2026-11-04T05:00:00Z (board note at I210)
- last CI run: 41767186758 (success, sha aa24687, 2026-11-04T03:26:52Z)

## Resumption condition

```yaml
resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-04T05:45:00Z" }
    - { member: forked-thread-completion, forked_thread: "ferric-async-forms-r2" }
    - { member: forked-thread-completion, forked_thread: "ferric-router-r1" }
  deadline: null
```

## On wake

I212 becomes eligible and runs the next board check. If a DAG has folded, schedule a fold-read task.
If neither has folded, evaluate the board and suspend again on the bounded wake.
