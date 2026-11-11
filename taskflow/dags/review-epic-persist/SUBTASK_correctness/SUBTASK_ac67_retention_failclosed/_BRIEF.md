# Task: #67 — retention/capacity commitments and fail-closed-on-non-durable-write

## Task Specification

**Slug**: SUBTASK_ac67_retention_failclosed
**Task Kind**: standard
**Status**: Pending

### Objective

Judge whether PR #113 actually makes acceptance criterion **#67** hold: retention and capacity commitments are
honoured — documented lifetimes for transient state, the reclaim job, and **no automatic expiry for user
content** — and the **fail-closed-on-non-durable-write** rule is actually enforced.

### Context

This is one area spoke of the `SUBTASK_correctness` subtree (see `../_GLOBAL.md` for the pinned target, the
inherited constraints, and the finding taxonomy). Read-only review; you write one findings document only.
Your area is acceptance criterion #67, judged for **behavioral correctness**. The proof-depth of the
durability *drill* (restart/redeploy/reschedule; whether assertions are real vs vacuous; stranger-runnability)
is owned by the root-level `SUBTASK_durability_proof`; where your reading touches it, record your correctness
finding and note the overlap for synthesis rather than expanding scope.

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Pinned commit, target, constraints, overlap policy |
| Root hub | `../../_GLOBAL.md` | The review DAG's pinned target and shared constraints |
| Contract | `../contracts/_MANIFEST.yaml`, `../../contracts/finding_schema.md` | The findings format, severity rubric, and your `COR-40 .. COR-59` id range |
| PR #113 diff @ `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` | `gh pr diff 113` / `git` (read-only) against merge-base with `main` | The change under review |
| Issue #67 | `gh issue view 67` on `Nousix-LLC/nswe-demo` | The acceptance criteria to trace to |

## The bar (what blocks)

A behavior #67 requires that the change does not actually deliver, or delivers incorrectly, is a **blocking**
finding. In particular:

- Whether lifetimes for transient state are documented and actually honoured by the code/config, and whether
  the reclaim job reclaims the right things on the stated cadence without touching durable user content.
- **No automatic expiry for user content**: whether any path (TTL, cache eviction, reclaim job, migration)
  can silently delete or expire user content that #67 requires be retained.
- **Fail-closed-on-non-durable-write**: whether a write that is not durably persisted actually fails closed
  (surfaces an error / refuses to acknowledge success) rather than silently returning success. Trace the write
  path and its error handling; this is the highest-risk behavior in the area.
- Error paths and edge cases, not only the happy path (full store, write timeout, backend unavailable).

## Output

`SUBTASK_ac67_retention_failclosed/outputs/findings.md`, conforming to `../../contracts/finding_schema.md`,
finding ids in range `COR-40 .. COR-59`.

## Success criteria

- [ ] #67 traced with "what I checked" enumerated (retention/lifetimes, reclaim job, user-content expiry
  paths, the fail-closed write path).
- [ ] "What I found clean" states specifically what was examined and judged sound.
- [ ] Every finding pinned to `09fa453…` (or explicit whole-PR/design-level with rationale), severity +
  `blocks_landing` set honestly, each with a concrete "what would satisfy me"; `confidence` set verified vs
  suspected.
- [ ] An area sub-verdict (CLEAN / NON-BLOCKING-ONLY / HAS-BLOCKERS).

## Constraints

Read-only on the repo; no GitHub writes. No host/cluster/SSH/credential details or DAG internals in the
findings. Plain voice.
