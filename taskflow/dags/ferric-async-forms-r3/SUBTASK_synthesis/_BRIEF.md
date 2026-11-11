# Task: Synthesis — CI verification and verdict

## Task Specification

**Slug**: SUBTASK_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_b2_b3_event_dom  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Verify that all 6 CI checks pass on the final HEAD of `work/ferric-async-forms-r2` after B1, B2, and B3 fixes are committed; write `SYNTHESIS.md` at `taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md` with verdict `PASS` or `FAIL`.

### Context

This task is part of ferric-async-forms-r3 (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: `SUBTASK_b2_b3_event_dom` — both prior tasks must be COMPLETED (B1 and B2+B3 committed to the branch) before this task becomes READY.  
**Dependents**: None — this is the terminal gate for the ferric-async-forms-r3 subtree.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Shared constraints, branch, acceptance criteria |
| B1 output | Commits on `work/ferric-async-forms-r2` from `SUBTASK_b1_reactive_resource` | Confirm SHA and verify test coverage |
| B2+B3 output | Commits on `work/ferric-async-forms-r2` from `SUBTASK_b2_b3_event_dom` | Confirm SHA and verify test coverage |
| CI run results | GitHub Actions runs for `work/ferric-async-forms-r2` HEAD | All 6 jobs: fmt, clippy, doc, test, wasm, image |
| PR status | PR #193 on Nousix-LLC/nswe-demo | Confirm commits are reflected in the PR |

---

## Scope

### Verification

This task integrates the work of `SUBTASK_b1_reactive_resource` and `SUBTASK_b2_b3_event_dom` by checking:

1. **CI status**: All 6 CI jobs (fmt, clippy, doc, test, wasm, image) pass on the final HEAD commit of `work/ferric-async-forms-r2`. Use the GitHub CLI or API to retrieve the check runs for the HEAD SHA.
2. **B1 coverage**: `create_resource(source, fetcher)` exists; at least one test covers reactive re-fetch; at least one WASM test covers async completion.
3. **B2 coverage**: An event-carrying `EventHandler` variant exists in `vdom.rs` with no `web_sys` import; at least one test verifies `prevent_default()` callable.
4. **B3 coverage**: At least one WASM test fires a synthetic input event on a bound element and verifies the signal updates.
5. **Backward compatibility**: Zero-arg `EventHandler` callers compile and pass; existing 23 async_resource and 18 form.rs tests all pass.

### On CI failure

If any CI job fails, the verdict is `FAIL`. The `SYNTHESIS.md` must identify: which job(s) failed, what the likely root cause is, and what a remediation path would look like. Do not attempt to fix code in this task — that is out of scope.

---

## Output Specification

### Declared output

`taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md`

The file must contain:
- **Verdict**: `PASS` or `FAIL` (prominent, at the top)
- **Head SHA**: the final commit SHA on `work/ferric-async-forms-r2`
- **CI run URL**: the GitHub Actions run URL for that SHA
- **CI job results**: table of all 6 jobs and their status
- **B1 summary**: what was added, which tests cover it
- **B2 summary**: what was changed, which tests cover REQ-ASYNC-023
- **B3 summary**: what was changed, which WASM test covers REQ-ASYNC-042
- **Residual concerns** (if any): items not addressed, known limitations, follow-up issues

---

## Success Criteria

- [ ] `SYNTHESIS.md` exists at `taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md`.
- [ ] Verdict is `PASS` only when all 6 CI jobs pass AND B1/B2/B3 acceptance criteria are met.
- [ ] Verdict is `FAIL` with explanation if any CI job fails or any acceptance criterion is unmet.
- [ ] CI run URL and HEAD SHA are present and accurate.

---

## Constraints

- Do not modify any source code — this is a verification-only task.
- Do not push additional commits; read the branch state as committed by prior tasks.
- Infrastructure details must not appear in committed files or PR comments.
