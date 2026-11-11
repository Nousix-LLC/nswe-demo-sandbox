# Task: Synthesize CI evidence and PR update into VERIFICATION.md; fold parent

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_ci_verify, SUBTASK_pr_update
**Status**: Pending

### Objective

Read `CI_EVIDENCE.md` and `PR_UPDATE.md`, verify the identities declared in the contract, and
produce `VERIFICATION.md` at the PARENT workspace (`../VERIFICATION.md`) as the folded result.
Then fold the parent task (`SUBTASK_verify_deliver`) from SUSPENDED to COMPLETED by calling
`engine_resume_suspended`.

### Context

Part of the SUBTASK_verify_deliver subtree (see `../_GLOBAL.md`). This task is the synthesis gate.
It verifies the contract identities hold and consolidates the evidence into the single declared
output of the parent task.

**Parent task ID** (for `engine_resume_suspended`): `SUBTASK_verify_deliver`  
**Fold record location**: `../VERIFICATION.md` (the parent workspace, one level up from this task's
workspace)

**Dependencies**: both `SUBTASK_ci_verify` (CI_EVIDENCE.md) and `SUBTASK_pr_update` (PR_UPDATE.md)

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Contract identities to verify, ownership |
| Ancestor hub | `../../_GLOBAL.md` | Full project success criteria |
| CI evidence | `../SUBTASK_ci_verify/CI_EVIDENCE.md` | Check results (doc, clippy, fmt, test, wasm) |
| PR update record | `../SUBTASK_pr_update/PR_UPDATE.md` | Delivery confirmation |
| Contract | `../contracts/_MANIFEST.yaml` | Identities to assert |

## Output Specification

**Primary output**: `../VERIFICATION.md` (at the PARENT workspace — one directory up from this
task's workspace).

`VERIFICATION.md` is both this synthesis task's terminal record (artifact_path) and the fold
record for `engine_resume_suspended`. It MUST include:

- **Evidence section**: the `doc` check is PASSED with fresh run reference and commit SHA `e63e607`
- **Non-regression section**: `clippy`, `fmt`, `test`, `wasm` are all PASSED
- **Delivery section**: PR #113 was updated in place; PR is mergeable/clean; description closes
  #65, #66, #67
- **Identity assertions**: each contract identity evaluated (ci_doc_green, no_regression,
  delivery_confirmed, output_hygiene) — PASSED or FAILED; no silent plugs
- **Repository identity**: `Nousix-LLC/nswe-demo`, PR #113, commit `e63e607`

Output hygiene: no host/absolute paths, cluster/SSH/credential details, or
taskflow/agent/run identifiers in VERIFICATION.md.

## Success Criteria

- [ ] All four contract identities are evaluated and recorded in VERIFICATION.md
- [ ] `doc` check is PASSED — evidenced in VERIFICATION.md
- [ ] `clippy`, `fmt`, `test`, `wasm` all PASSED — evidenced in VERIFICATION.md
- [ ] PR #113 updated in place and mergeable — confirmed in VERIFICATION.md
- [ ] `VERIFICATION.md` written at `../VERIFICATION.md` before the terminal report
- [ ] `engine_resume_suspended` called to fold `SUBTASK_verify_deliver` SUSPENDED → COMPLETED

## Synthesis Fold

After writing `../VERIFICATION.md` and reporting terminal status, call:

```
engine_resume_suspended {
  target_task_id: "SUBTASK_verify_deliver",
  synthesized_task_id: "SUBTASK_synthesis",
  seam_path: "<absolute path to ../VERIFICATION.md>"
}
```

This folds the parent task to COMPLETED, enabling `SUBTASK_synthesis` (the root DAG synthesis) to
proceed. VERIFICATION.md is both this task's `artifact_path` and the `seam_path`.

## Constraints

- Write `VERIFICATION.md` at `../VERIFICATION.md` (the parent workspace), NOT at this task's workspace
- The fold record and the declared output are ONE file (VERIFICATION.md) — no duplicate SYNTHESIS.md
- Output hygiene is a hard constraint: nothing in VERIFICATION.md carries host/SSH/cluster/credential/taskflow details
- If any contract identity FAILS, record it honestly in VERIFICATION.md; do not silently plug failures
