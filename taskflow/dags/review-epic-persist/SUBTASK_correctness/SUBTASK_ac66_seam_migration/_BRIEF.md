# Task: #66 — ChirpRepository seam fidelity, single-writer safety, and migration/versioning

## Task Specification

**Slug**: SUBTASK_ac66_seam_migration
**Task Kind**: standard
**Status**: Pending

### Objective

Judge whether PR #113 actually makes acceptance criterion **#66** hold: durable storage plugs into the
existing **`ChirpRepository` seam** soundly — the full capability set behind the seam, single-writer safety,
and a schema that is versioned and applied by a migration runner — with **no capability dropped or weakened**.

### Context

This is one area spoke of the `SUBTASK_correctness` subtree (see `../_GLOBAL.md` for the pinned target, the
inherited constraints, and the finding taxonomy). Read-only review; you write one findings document only.
Your area is acceptance criterion #66, judged for **behavioral correctness**. The seam's contract-stability
*shape* (API signature drift, breaking-change analysis) is owned by the root-level
`SUBTASK_architecture_contract`; where your reading touches it, record your correctness finding and note the
overlap for synthesis rather than expanding scope.

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Pinned commit, target, constraints, overlap policy |
| Root hub | `../../_GLOBAL.md` | The review DAG's pinned target and shared constraints |
| Contract | `../contracts/_MANIFEST.yaml`, `../../contracts/finding_schema.md` | The findings format, severity rubric, and your `COR-20 .. COR-39` id range |
| PR #113 diff @ `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` | `gh pr diff 113` / `git` (read-only) against merge-base with `main` | The change under review |
| Issue #66 | `gh issue view 66` on `Nousix-LLC/nswe-demo` | The acceptance criteria to trace to |
| `ChirpRepository` seam | the trait/interface definition read on `main` and in the diff | What "full capability set behind the seam" must cover |

## The bar (what blocks)

A behavior #66 requires that the change does not actually deliver, or delivers incorrectly, is a **blocking**
finding. In particular:

- Whether **every** capability the `ChirpRepository` seam exposes is implemented by the durable backend — no
  method left unimplemented, stubbed, `todo!()`, or silently weakened (e.g. a method that previously returned
  an error now swallowing it, or a narrower guarantee than the seam promises).
- **Single-writer safety**: whether the criterion's single-writer guarantee actually holds in the durable
  implementation (how concurrent writers are serialized; whether the "single writer" is enforced or merely
  assumed by deployment), and the error/edge paths around it.
- **Migration / schema-versioning**: whether the schema is versioned and applied by a migration runner as #66
  requires; whether migrations are ordered, idempotent/re-runnable, and fail safely; whether anything is
  applied ad hoc outside the runner.
- Error paths and edge cases behind the seam, not only the happy path.

## Output

`SUBTASK_ac66_seam_migration/outputs/findings.md`, conforming to `../../contracts/finding_schema.md`, finding
ids in range `COR-20 .. COR-39`.

## Success criteria

- [ ] #66 traced with "what I checked" enumerated (the seam's capability set, the single-writer mechanism, the
  migration runner).
- [ ] "What I found clean" states specifically what was examined and judged sound.
- [ ] Every finding pinned to `09fa453…` (or explicit whole-PR/design-level with rationale), severity +
  `blocks_landing` set honestly, each with a concrete "what would satisfy me"; `confidence` set verified vs
  suspected.
- [ ] An area sub-verdict (CLEAN / NON-BLOCKING-ONLY / HAS-BLOCKERS).

## Constraints

Read-only on the repo; no GitHub writes. No host/cluster/SSH/credential details or DAG internals in the
findings. Plain voice.
