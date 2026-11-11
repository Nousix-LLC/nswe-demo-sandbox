# Task: Check CI checks on PR #113 are green

## Task Specification

**Slug**: SUBTASK_ci_verify
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Observe and record the CI check results for PR #113 (`Nousix-LLC/nswe-demo`, branch
`work/epic-persist`) on the current head commit (`e63e607`). Produce evidence — not inference —
that the required `doc` check passed under `RUSTDOCFLAGS=-D warnings` on a fresh run, and that
the other required checks (`clippy`, `fmt`, `test`, `wasm`) also passed with no durability
regression.

### Context

Part of the SUBTASK_verify_deliver subtree (see `../_GLOBAL.md`). The doc corrections in commit
`e63e607` address CI-01 (public→private intra-doc link) and H-02 through H-14 (#118 hazards).
rustdoc reports only the first failing crate, so the `doc` check must be re-confirmed end-to-end
after the fix — not inferred from the first error clearing.

**Dependents**: `SUBTASK_pr_update` and `SUBTASK_synthesis` read `CI_EVIDENCE.md`.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Constraints and context |
| Ancestor hub | `../../_GLOBAL.md` | Full project context |
| Changeset | `../../SUBTASK_apply_fixes/CHANGESET.md` | What was changed and the verifying commit SHA |
| Contract | `../contracts/_MANIFEST.yaml` | Output schema for CI_EVIDENCE.md |

## Output Specification

**Primary output**: `CI_EVIDENCE.md` in this task's workspace.

The output MUST include:
- A summary table of all required checks: `doc`, `clippy`, `fmt`, `test`, `wasm` with observed status
- For the `doc` check: the specific run reference (GitHub Actions run URL or gh output) and the
  verifying commit SHA — evidenced, not inferred
- For each other check: observed status on the same run
- The repository identity (`Nousix-LLC/nswe-demo`) and PR number (#113)

**Output hygiene**: no host/absolute paths, cluster/SSH/credential details, or
taskflow/agent/run identifiers.

## Success Criteria

- [ ] `CI_EVIDENCE.md` exists at this task's workspace
- [ ] The `doc` check status is recorded as PASSED with fresh run reference on `e63e607`
  (if PENDING, record what was observed and the run URL; if FAILED, record the failure)
- [ ] `clippy`, `fmt`, `test`, `wasm` statuses are recorded
- [ ] No host/cluster/SSH/credential/taskflow details appear in the output

## Constraints

- Use `gh pr checks 113 --repo Nousix-LLC/nswe-demo` (or equivalent `gh` commands) to observe
  check status. Do not infer pass/fail from commit message or changeset alone.
- If a check is PENDING (CI still running), record that status with the run URL and note
  the observation timestamp. Do not block — record what is observable.
- Output hygiene is a hard constraint on the content of CI_EVIDENCE.md itself.
