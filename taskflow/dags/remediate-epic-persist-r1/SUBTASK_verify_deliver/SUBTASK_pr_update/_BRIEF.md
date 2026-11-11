# Task: Update PR #113 in place with a reader-facing description

## Task Specification

**Slug**: SUBTASK_pr_update
**Task Kind**: standard
**Depends on**: SUBTASK_ci_verify
**Status**: Pending

### Objective

Update PR #113 (`Nousix-LLC/nswe-demo`, `work/epic-persist` → `main`) in place with a clear,
reader-facing description that states what changed, why, how it was verified, and which issues
(#65, #66, #67) it closes. The PR must be mergeable and clean after the update.

### Context

Part of the SUBTASK_verify_deliver subtree (see `../_GLOBAL.md`). The `CI_EVIDENCE.md` from
`SUBTASK_ci_verify` confirms the check statuses and must be referenced in the narrative. Delivery
means updating the PR description — the DAG never merges the PR.

**Dependencies**: `SUBTASK_ci_verify` (CI_EVIDENCE.md must confirm checks before delivery)  
**Dependents**: `SUBTASK_synthesis` reads `PR_UPDATE.md`

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Constraints and context |
| Ancestor hub | `../../_GLOBAL.md` | Full project context (issues, scope) |
| Changeset | `../../SUBTASK_apply_fixes/CHANGESET.md` | The 13 corrections applied and commit SHA |
| Inventory | `../../SUBTASK_assess/INVENTORY.md` | The hazards addressed (CI-01, H-02 to H-14) |
| CI evidence | `../SUBTASK_ci_verify/CI_EVIDENCE.md` | Check results to reference in the PR narrative |
| Contract | `../contracts/_MANIFEST.yaml` | Output schema for PR_UPDATE.md |

## Output Specification

**Primary output**: `PR_UPDATE.md` in this task's workspace.

`PR_UPDATE.md` MUST record:
- Repository identity (`Nousix-LLC/nswe-demo`), PR number (#113), branch (`work/epic-persist`)
- Confirmation that the PR was updated in place (via `gh pr edit`)
- The text that was written to the PR description (verbatim or a clear summary)
- Which issues the description closes: #65, #66, #67 (one `Closes #N` per issue in the PR body)
- Confirmation the PR is mergeable/clean

The PR description itself (posted to GitHub) MUST:
- State what changed (doc corrections: CI-01, #118 hazards)
- State why (to clear the `doc` CI blocker and close #118 accuracy hazards)
- State how it was verified (CI checks: `doc` green, no regression in `clippy`/`fmt`/`test`/`wasm`)
- Close #65, #66, #67 (one `Closes #N` per issue, plain text)
- NOT contain host/absolute paths, cluster/SSH/credential details, or taskflow/agent/run identifiers

## Success Criteria

- [ ] PR #113 has been updated in place via `gh pr edit`
- [ ] The PR description states what changed, why, how verified, and closes #65, #66, #67
- [ ] `PR_UPDATE.md` records the update with the posted description text
- [ ] PR is mergeable and clean (check with `gh pr view`)
- [ ] Output hygiene: no host/cluster/SSH/credential/taskflow details in PR_UPDATE.md or the
      PR description posted to GitHub

## Constraints

- Use `gh pr edit 113 --repo Nousix-LLC/nswe-demo --body "..."` to update the PR description
- Prefer updating #113 in place. Only if the branch state makes this impossible: open exactly
  one PR into `main` closing #65, #66, #67 (one `Closes #N` per issue, plain text)
- Never push to main, never force-push, never merge the PR
- Output hygiene is a hard constraint
