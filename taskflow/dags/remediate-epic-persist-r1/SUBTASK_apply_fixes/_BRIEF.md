# Task: Apply the doc corrections and commit to `work/epic-persist`

## Task Specification

**Slug**: SUBTASK_apply_fixes
**Task Kind**: standard
**Status**: Pending

### Objective

Apply every correction in the diagnosed inventory to the `chirp-server` crate's doc comments, intra-doc links, and
doc feature-gate attributes, and commit the result to `Nousix-LLC/nswe-demo` `work/epic-persist` so PR #113 is
updated in place — making one kind of change (documentation and doc-gating text) and nothing else.

### Context

Part of the PR #113 doc-blocker remediation (see `../_GLOBAL.md`). The implementation underneath was found sound on
review and MUST NOT be re-architected. You consume the correction inventory as a hard input; you do not re-diagnose
or redesign it (if it is inadequate, request a plan amendment rather than deviating silently).

**Dependencies**: `SUBTASK_assess` (its `INVENTORY.md`).
**Dependents**: `SUBTASK_verify_deliver` builds/verifies and pushes; `SUBTASK_synthesis` asserts coverage.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Constraints, scope, success criteria |
| Correction schema | `../contracts/inventory.schema.yaml` (read-only) | The shape of the records you consume |
| Correction inventory | `../SUBTASK_assess/INVENTORY.md` | The exact set of docs-only edits to apply |
| Branch under remediation | `Nousix-LLC/nswe-demo` `work/epic-persist`, PR #113 | The branch to edit and commit to |

## Output Specification

**Primary output**: `CHANGESET.md` in this task's workspace — records, per inventory `id`, the file and doc item
changed and the resulting commit SHA(s) on `work/epic-persist`. The substantive artifact is the committed source
edits themselves on that branch.

## Success Criteria

- [ ] Every inventory record is applied as a docs-only edit (doc comment text, intra-doc link, or doc feature-gate
      attribute) — the diff touches source only where a doc comment/link/gate must change.
- [ ] CI-01's public→private link no longer links a public item into a private/`pub(crate)` item.
- [ ] #118 edits are applied: ungated→gated references are gating-correct; stale scaffold/placeholder docs are
      rewritten to match implemented behavior; internal build vocabulary is removed from shipped comments.
- [ ] Changes are committed to `work/epic-persist` (updating PR #113 in place); `CHANGESET.md` maps every inventory
      `id` to its commit.

## Constraints

- **Docs-only.** No change to store logic, schema, migrations, the `ChirpRepository` seam, or wiring. If an
  inventory record cannot be satisfied without a non-doc change, do not make that change — record it and request an
  amendment.
- Branch `work/epic-persist` only; **never force-push `main`**, never rewrite merged history, never merge the PR.
- **No attribution trailers** on commits.
- Output hygiene: commit messages and anything posted name everything by repository identity — no host/cluster/SSH/
  credential/taskflow details, no absolute/host paths.
- Do not run the verification/push-as-delivery narrative here beyond committing — the fresh `doc` green-under-`-D
  warnings` proof, the no-regression check, and the PR description belong to `SUBTASK_verify_deliver`.
