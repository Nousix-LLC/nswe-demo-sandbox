# _BRIEF.md — chirp-logged-out-r3/pr-gate

## Objective

Gate PR #263 (`work/chirp-logged-out` → `main`, closing issue #35) by verifying that all
required CI checks pass on the latest branch commit. Update the parent SYNTHESIS.md with the
final CI confirmation and mark the PR as ready.

## Context

- **Repository:** `Nousix-LLC/nswe-demo`
- **PR:** #263 — "feat: logged-out reading and accurate landing states (#35)"
- **Head commit:** `2615ba1d91509e505290d577b4997aa134fab4bf`
- **Parent SYNTHESIS.md:** `taskflow/dags/chirp-logged-out-r3/SYNTHESIS.md`
  (already written; describes AC-1–AC-5 status and CI jobs)

## Required CI checks

The PR is gated on all five required jobs passing:

| Job | Required |
|-----|---------|
| fmt | yes |
| clippy | yes |
| test | yes |
| wasm | yes |
| doc | yes |

The `image` job is a build-only artifact gate; it must not fail.

## Declared output

- `COMPLETE.md` at this workspace confirming all required checks passed and the PR is mergeable.

## Success criteria

All five required CI jobs on commit `2615ba1` are `completed: success`. The PR is open with
`Closes #35` in the description body and no merge conflicts.
