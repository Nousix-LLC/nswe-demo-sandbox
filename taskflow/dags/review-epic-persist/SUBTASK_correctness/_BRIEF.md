# Task: Correctness against acceptance criteria and the design — PR #113

## Task Specification

**Slug**: SUBTASK_correctness
**Task Kind**: standard
**Status**: Pending

### Objective

Judge whether PR #113 actually delivers what acceptance criteria #65, #66, #67 and the design's
durable-persistence requirement specify — not whether it asserts it, whether it does it.

### Context

Part of the PR #113 review DAG (see `../_GLOBAL.md` for the pinned target, the issues, the design of record,
and the shared constraints). Read-only review; you write a findings document only. This concern covers three
distinct acceptance-criteria areas (#65, #66, #67) plus the durable-persistence design requirement — treat
them as the distinct areas they are when you size your own work.

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Pinned commit, target, constraints |
| Contract | `../contracts/finding_schema.md`, `../contracts/_MANIFEST.yaml` | The findings format and severity rubric you MUST emit |
| PR #113 diff @ `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` | `gh pr diff 113` / `git` (read-only) against merge-base with `main` | The change under review |
| Issues #65, #66, #67 | `gh issue view` on `Nousix-LLC/nswe-demo` | The acceptance criteria to trace to |
| Design of record | `design/domain-application-design.md`, `design/release-bar.md` (read on `main`) | Durable-persistence requirement + applicable `BAR-*`/`REQ-*` |

## The bar (what blocks)

A behavior the acceptance criteria or the design require that the change does not actually deliver, or
delivers incorrectly, is a **blocking** finding. Examine at least:

- Domain invariants and derived counts (follower/following/like counts) in the durable store.
- Opaque-id monotonicity.
- **Concurrency and single-writer hazards** — whether the criteria's "under concurrency" guarantee holds, or
  is merely claimed.
- Migration / schema-versioning behavior (applied by a migration runner; no capability dropped or weakened
  behind the `ChirpRepository` seam).
- The **fail-closed-on-non-durable-write** rule.
- Edge cases and error paths, not just the happy path.
- Whether the #64 "stays open" framing is accurate — confirm, do not close #64, do not file it as backlog.

Seam-fidelity depth (full capability set behind the existing seam) is shared with the architecture concern;
focus here on whether the *behavior* each criterion names is correct, and leave contract-stability shape to
`SUBTASK_architecture_contract`. Where they overlap, record your correctness finding and let synthesis
de-duplicate.

## Output

`SUBTASK_correctness/outputs/findings.md`, conforming to `../contracts/finding_schema.md` (prefix `COR`).

## Success criteria

- [ ] Each of #65/#66/#67 and the durable-persistence requirement traced, with "what I checked" enumerated.
- [ ] "What I found clean" states specifically what was examined and judged sound.
- [ ] Every finding pinned to the commit, severity + `blocks_landing` set honestly, each with a concrete
  "what would satisfy me".
- [ ] A concern sub-verdict (CLEAN / NON-BLOCKING-ONLY / HAS-BLOCKERS).

## Constraints

Read-only on the repo; no GitHub writes from this task. No host/cluster/SSH/credential details or DAG
internals in the findings. Plain voice.
