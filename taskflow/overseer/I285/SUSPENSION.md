# SUSPENSION.md — I285

**Suspended at**: 2026-11-06T00:21:00Z
**Reason**: Both review DAGs still in flight at I285 check. Awaiting synthesis from review-ferric-ssr-r2 and review-ferric-async-forms-r3.

## State

- **review-ferric-ssr-r2**: SYNTHESIS.md not present — still in flight (PR #228, issues #223/#224/#226)
- **review-ferric-async-forms-r3**: SYNTHESIS.md not present — still in flight (PR #193, issue #130)

## Successor

I286 scheduled at `taskflow/overseer/I286/_BRIEF.md` (depends_on I285).

## Resumption condition

```yaml
resumption_condition:
  any_of:
    - { member: schedule, resume_at: "2026-11-06T00:36:00Z" }
    - { member: forked-thread-completion, forked_thread: "review-ferric-ssr-r2" }
    - { member: forked-thread-completion, forked_thread: "review-ferric-async-forms-r3" }
  deadline: null
```

## On wake

I285 writes CONTINUE.md and I286 (depends_on I285) becomes eligible. I286 reads prior STATE at `taskflow/overseer/I285/project_state.json` and re-checks both SYNTHESIS.md paths.
