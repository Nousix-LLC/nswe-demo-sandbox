# SUSPENSION.md — review-chirp-logged-out-r1

## Status

Suspended: NeedsDecompose. This node has decomposed the review into four parallel spoke tasks
plus one synthesis task and is waiting for them to complete.

## Decomposition

The review of PR #263 against issue #35's five acceptance criteria spans five distinct analytical
concerns. The root task decomposed into:

| Child task ID | Concern | Group |
|---|---|---|
| `review-chirp-logged-out-r1/spoke-access-auth` | AC-1: public access and auth boundaries | 0 |
| `review-chirp-logged-out-r1/spoke-ui-states` | AC-2/3/4: UI states, error messages, CTAs | 0 |
| `review-chirp-logged-out-r1/spoke-state-machine` | AC-5: all state branches accurate and distinct | 0 |
| `review-chirp-logged-out-r1/spoke-code-quality` | Code quality, tests, security, idiom, prose | 0 |
| `review-chirp-logged-out-r1/synthesis` | Aggregate, write SYNTHESIS.md, post PR review | 1 |

## Resumption condition

The four group-0 spokes run in parallel. The synthesis child (group 1) runs after all four
complete. This node resumes when `synthesis` reaches terminal status (completed or failed).

## Context preserved for synthesis

Each spoke writes `REVIEW.md` at its own workspace root. The synthesis child reads all four,
writes `SYNTHESIS.md` at the DAG root
(`taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md`), and posts the review to PR #263.

## Key observation propagated to all spokes

`timeline.rs` switched from `ctx.client().timeline()` to `ctx.client().pub_timeline()`. This
routes the authenticated home timeline view through the global public endpoint rather than the
per-user following endpoint. Every spoke must assess this potential regression in its own scope.
