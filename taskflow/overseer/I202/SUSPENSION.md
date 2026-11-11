# SUSPENSION.md — overseer I202

**Suspended at**: 2026-11-04T03:05:00Z
**Reason**: Review DAG `review-ferric-epic-authoring-r1` not yet folded. No other board activity requires action.

## Resumption condition

resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-04T03:15:00Z" }
    - { member: forked-thread-completion, forked_thread: "review-ferric-epic-authoring-r1" }
  deadline: null

## On wake

I203 becomes eligible and re-checks:
1. Whether `taskflow/dags/review-ferric-epic-authoring-r1/SYNTHESIS.md` has appeared.
2. If APPROVE: schedule process review, land PR #188, deployment check, board check.
3. If REQUEST-CHANGES: schedule process review, remediation DAG.
4. If still absent: re-suspend on fresh bounded wake and schedule I204.
