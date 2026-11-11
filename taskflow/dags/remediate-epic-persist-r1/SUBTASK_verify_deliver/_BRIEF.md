# Task: Verify the blocker is cleared without regression, and deliver the PR update

## Task Specification

**Slug**: SUBTASK_verify_deliver
**Task Kind**: standard
**Status**: Pending

### Objective

Prove that the applied doc corrections turn the required `doc` check green under `-D warnings` on a **fresh** run and
that no durability regression was introduced, then deliver the result by ensuring PR #113 on `work/epic-persist` is
updated in place with a clear, reader-facing description.

### Context

Part of the PR #113 doc-blocker remediation (see `../_GLOBAL.md`). rustdoc reports only the first failing crate, so a
clean `doc` run must be re-confirmed end-to-end after the fix — not inferred from the first error clearing. The
durable store, seam, migrations, and the proofs #65/#66/#67 were accepted on must remain intact; the only behavioral
change is to documentation.

**Dependencies**: `SUBTASK_apply_fixes` (the committed edits + `CHANGESET.md`).
**Dependents**: `SUBTASK_synthesis` reads your verification record to fold the verdict.

### Distinct concerns

- **Blocker verification** — `cargo doc --workspace --no-deps --locked` is green under `RUSTDOCFLAGS: -D warnings` on
  a fresh run; no further public→private / ungated→gated link error surfaces behind the first fix.
- **Non-regression verification** — the previously-green checks (`clippy`, `fmt`, `test`, `wasm`) remain green; the
  diff is documentation/doc-gating only.
- **Delivery** — PR #113 is updated in place on `work/epic-persist` and is mergeable/clean; the PR description and
  commit narrative explain what changed, why, how it was verified, and which issues it closes.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Constraints, scope, success criteria |
| Changeset | `../SUBTASK_apply_fixes/CHANGESET.md` + the commits on `work/epic-persist` | What was changed, to verify |
| Inventory | `../SUBTASK_assess/INVENTORY.md` | The hazards that must now be clear |
| CI / checks | `Nousix-LLC/nswe-demo` PR #113 required checks (`doc`, `clippy`, `fmt`, `test`, `wasm`) | The bars judged |

## Output Specification

**Primary output**: `VERIFICATION.md` in this task's workspace — the evidence that `doc` is green under `-D warnings`
on a fresh run (the command/CI run and its result), that `clippy`/`fmt`/`test`/`wasm` are green, and that PR #113 is
updated and mergeable. Record the PR state and the verifying run by repository identity.

## Success Criteria

- [ ] A fresh `cargo doc --workspace --no-deps --locked` under `-D warnings` is green, evidenced (not inferred).
- [ ] `clippy`, `fmt`, `test`, `wasm` are green on PR #113 — no durability regression.
- [ ] PR #113 is updated in place on `work/epic-persist`, mergeable and clean, with a reader-facing description that
      states what changed, why, how it was verified, and the issues it closes.
- [ ] `VERIFICATION.md` records all of the above by repository identity.

## Constraints

- The DAG **never merges** PR #113 and **never pushes to `main`**; never force-push `main`; never rewrite merged
  history. Delivery means updating the PR, not landing it.
- Only if the branch state makes updating #113 impossible: open exactly one PR into `main` closing #65, #66, #67
  (one `Closes #N` per issue, plain text). Prefer updating #113 in place.
- Output hygiene (hard): nothing posted to GitHub (PR body, comments) carries host/absolute paths, cluster/SSH/
  credential details, or taskflow/agent/run identifiers. Name everything by repository identity.
- No attribution trailers on any commit you make.
