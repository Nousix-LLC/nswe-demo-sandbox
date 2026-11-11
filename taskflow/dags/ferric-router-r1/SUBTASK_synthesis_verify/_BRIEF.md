# _BRIEF.md — synthesis-verify

**Goal slug**: `synthesis-verify`  
**Kind**: code atomic (synthesis gate — folds root `ferric-router-r1`)  
**Repo**: `Nousix-LLC/nswe-demo`  
**Branch**: `work/ferric-router-r1`  
**PR**: #192 — https://github.com/Nousix-LLC/nswe-demo/pull/192

---

## Objective

Confirm that PR #192 is green across all six CI checks after the `clippy-fix` spoke pushes
its commit. Write the final `SYNTHESIS.md` at the observation seam. Then fold the suspended
root DAG node (`ferric-router-r1`) by calling `engine_resume_suspended`.

---

## Inputs

- PR #192 (`work/ferric-router-r1` → `main`) on `Nousix-LLC/nswe-demo`.
- `clippy-fix` task COMPLETE (its commit has been pushed to the branch).
- Existing `taskflow/dags/ferric-router-r1/SYNTHESIS.md` (the previous synthesis document;
  this task overwrites it with a corrected version).

---

## Verification steps

1. **Wait for CI re-run** — GitHub Actions automatically re-runs all checks on the new push.
   Poll `gh pr view 192 --json statusCheckRollup` until all six checks reach a terminal state.

2. **Confirm all checks pass**:

   | Check | Expected |
   |---|---|
   | `fmt` | SUCCESS |
   | `clippy` | SUCCESS |
   | `test` | SUCCESS |
   | `wasm` | SUCCESS |
   | `doc` | SUCCESS |
   | `image` | SUCCESS or SKIPPED |

3. **Verify contract identities** are still met after the fix commit (all five from
   `contracts/ferric_router_r1_api.md`; the fix is a one-line import removal in test code
   and must not affect them).

---

## Declared outputs

### 1. `taskflow/dags/ferric-router-r1/SYNTHESIS.md`

Overwrite the existing `SYNTHESIS.md` at the observation seam. The document must:

- Report the final CI status (all six checks).
- Confirm all five contract identities from `contracts/ferric_router_r1_api.md` are met.
- Record coverage of issues #131, #146, #147 (acceptance criteria met or not and why).
- State the head commit SHA on the branch after the clippy-fix commit.
- Record the PR URL (#192).

### 2. `COMPLETE.md` at this workspace

A brief completion record stating what was verified and the final outcome.

---

## Folding the root

After writing `SYNTHESIS.md`, call `mcp__hal__resume_suspended` to fold the suspended root:

```
target_task_id:    ferric-router-r1
synthesized_task_id: synthesis-verify
seam_path:         /home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-router-r1/SYNTHESIS.md
```

Then publish your own terminal `mcp__hal__report_status { status: "completed", ... }`.

---

## Constraints

- Do not merge the PR. The overseer's review gate merges.
- Do not modify any source files in `crates/ferric-router`.
- Do not touch `design/`.
- Security: never put the host's server address, SSH key path, user name, or local paths into
  GitHub issues, PRs, or committed files.
