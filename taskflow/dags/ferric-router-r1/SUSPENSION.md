# SUSPENSION.md — ferric-router-r1 (pass 2)

**Status**: suspended/NeedsDecompose  
**Reason**: PR #192 is open with one failing CI check (clippy). Decomposed into two
sequential tasks to fix the error and verify CI.

---

## Background

The original four spokes (`navigate-replace`, `active-link`, `nested-routes`, `synthesis-gate`)
all COMPLETED and PR #192 was created. Five API contract identities are met. However, the
synthesis gate verified clippy with `cargo clippy -p ferric-router -- -D warnings` (single
crate, no `--all-targets`), which does not check test code. The GitHub Actions CI pipeline
runs `cargo clippy --workspace --all-targets --locked -- -D warnings`, which does lint test
code and found:

```
error: unused import: `VNode`
  --> crates/ferric-router/src/router.rs:436:46
```

## Child tasks

| ID | Description | Group |
|---|---|---|
| `clippy-fix` | Remove unused `VNode` import from router.rs:436; run full clippy; commit + push | 1 |
| `synthesis-verify` | Verify all 6 CI checks pass; write final SYNTHESIS.md; fold root | 2 |

## Resumption condition

This node resumes when `synthesis-verify` reaches terminal COMPLETED state and calls
`engine_resume_suspended { target_task_id: "ferric-router-r1", synthesized_task_id:
"synthesis-verify" }` with the final SYNTHESIS.md at the observation seam.
