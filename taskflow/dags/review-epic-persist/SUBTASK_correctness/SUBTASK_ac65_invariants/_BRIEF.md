# Task: #65 — invariants, derived counts, and opaque-id monotonicity under concurrency

## Task Specification

**Slug**: SUBTASK_ac65_invariants
**Task Kind**: standard
**Status**: Pending

### Objective

Judge whether PR #113 actually makes acceptance criterion **#65** hold in the durable store: that domain
invariants, the derived counts (follower/following/like counts), and opaque monotonic ids are preserved
**under concurrency** — and whether that is *proved* by the change rather than merely asserted.

### Context

This is one area spoke of the `SUBTASK_correctness` subtree (see `../_GLOBAL.md` for the pinned target, the
inherited constraints, and the finding taxonomy). Read-only review; you write one findings document only.
Your area is acceptance criterion #65 and nothing else; where your reading touches #66/#67 or the sibling
root-level concerns, record the correctness finding and note the overlap for the synthesis gate rather than
expanding scope.

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Pinned commit, target, constraints, overlap policy |
| Root hub | `../../_GLOBAL.md` | The review DAG's pinned target and shared constraints |
| Contract | `../contracts/_MANIFEST.yaml`, `../../contracts/finding_schema.md` | The findings format, severity rubric, and your `COR-01 .. COR-19` id range |
| PR #113 diff @ `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` | `gh pr diff 113` / `git` (read-only) against merge-base with `main` | The change under review |
| Issue #65 | `gh issue view 65` on `Nousix-LLC/nswe-demo` | The acceptance criteria to trace to |

## The bar (what blocks)

A behavior #65 requires that the change does not actually deliver, or delivers incorrectly, is a **blocking**
finding. In particular:

- Whether follower/following/like counts in the durable store stay consistent with the underlying edges —
  including under concurrent writers (two likes, a like racing an unlike, concurrent follow/unfollow).
- Whether opaque ids are actually monotonic as #65 requires (generation source, uniqueness, ordering under
  concurrent inserts), not monotonic only in a single-threaded test.
- The domain invariants #65 names, and their error/edge paths (empty, duplicate, retry, partial failure) — not
  only the happy path.
- Whether #65's "under concurrency" guarantee is **proved** by the change or merely claimed. An unproven
  concurrency guarantee is a blocker, framed with the test or reproducer that would settle it.

Single-writer *mechanism* safety and the drill's *test depth* are owned by sibling concerns (#66 spoke; the
root `SUBTASK_durability_proof`). Where #65's correctness depends on them, record your finding and note the
overlap; do not reconcile.

## Output

`SUBTASK_ac65_invariants/outputs/findings.md`, conforming to `../../contracts/finding_schema.md`, finding ids
in range `COR-01 .. COR-19`.

## Success criteria

- [ ] #65 traced with "what I checked" enumerated (files, behaviors, the concurrency scenarios examined).
- [ ] "What I found clean" states specifically what was examined and judged sound.
- [ ] Every finding pinned to `09fa453…` (or explicit whole-PR/design-level with rationale), severity +
  `blocks_landing` set honestly, each with a concrete "what would satisfy me"; `confidence` set verified vs
  suspected.
- [ ] An area sub-verdict (CLEAN / NON-BLOCKING-ONLY / HAS-BLOCKERS).

## Constraints

Read-only on the repo; no GitHub writes. No host/cluster/SSH/credential details or DAG internals in the
findings. Plain voice.
