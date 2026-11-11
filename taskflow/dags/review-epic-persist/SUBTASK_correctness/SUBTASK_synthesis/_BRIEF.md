# Task: Fold the four correctness areas into one concern findings document

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective

Consolidate the four per-area findings documents (#65, #66, #67, durable-persistence requirement + #64) into
the single `SUBTASK_correctness/outputs/findings.md` that the PR #113 review DAG consumes — conforming to the
inherited finding schema, de-duplicating overlaps, and rendering one honest concern sub-verdict for
correctness.

This is the synthesis/verification gate for the `SUBTASK_correctness` subtree. It reads the area outputs,
verifies the subtree's contract identities, folds the result into the parent, and performs the DAG fold that
resolves the suspended `SUBTASK_correctness` parent.

### Context

Part of the `SUBTASK_correctness` subtree (see `../_GLOBAL.md` for the target, constraints, contract, and the
identities this gate asserts). Read-only on the repo; **no GitHub writes** (posting the review and filing
backlog belong solely to the root review DAG's own synthesis task, not here).

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | The subtree's objective, constraints, and contract |
| Sub-contract | `../contracts/_MANIFEST.yaml` | The id-range partition and the identities to assert |
| Finding schema | `../../contracts/finding_schema.md` | The document + per-finding structure the consolidated output must conform to |
| #65 findings | `../SUBTASK_ac65_invariants/outputs/findings.md` | Area input |
| #66 findings | `../SUBTASK_ac66_seam_migration/outputs/findings.md` | Area input |
| #67 findings | `../SUBTASK_ac67_retention_failclosed/outputs/findings.md` | Area input |
| design/#64 findings | `../SUBTASK_design_req_and_64/outputs/findings.md` | Area input |

## What the gate does

- Verify the contract identities in `../contracts/_MANIFEST.yaml` (and the inherited root identities that
  bind here): each of #65/#66/#67 and the durable-persistence requirement traced by exactly one spoke with
  both "what I checked" and "what I found clean"; every finding pinned and carrying an honest severity +
  `blocks_landing`; `COR-NN` ids unique across the consolidated document; #64 noted but not closed/not
  backlog; overlaps with the root architecture/durability-proof concerns recorded, not reconciled away.
- Consolidate the four areas into one `findings.md` with the schema's sections: one "What I checked" (all four
  areas enumerated), one "What I found clean", all findings (preserving each area's `COR-NN` ids), and one
  **concern sub-verdict** = HAS-BLOCKERS iff any area carries `blocks_landing: true`; NON-BLOCKING-ONLY iff
  findings exist but none block; CLEAN iff none. Do not silently plug a failing identity — if an area is
  missing or malformed, report it rather than inventing coverage.
- Run the avoid-ai-writing finishing pass over the consolidated prose before writing it.

## Output

- `SUBTASK_correctness/outputs/findings.md` — the single consolidated concern deliverable (declared output).
- `SUBTASK_correctness/SYNTHESIS.md` — the fold record at the fold location (the suspended
  `SUBTASK_correctness` parent's directory), authored before the terminal call and consumed by the fold that
  flips the parent SUSPENDED → COMPLETED.

## Success criteria

- [ ] All four area findings incorporated; every contract identity asserted (no silent plugs).
- [ ] Consolidated `findings.md` conforms to `finding_schema.md`; `COR-NN` ids unique; one concern sub-verdict
  rendered per the rule above.
- [ ] `SYNTHESIS.md` authored at the fold location; the parent resolved via the fold.
- [ ] No host/cluster/SSH/credential details or DAG internals in the consolidated findings; plain voice.

## Constraints

Read-only on the repo; no GitHub writes. No host/system details or DAG internals in repo-reader-facing output.
Plain voice.
