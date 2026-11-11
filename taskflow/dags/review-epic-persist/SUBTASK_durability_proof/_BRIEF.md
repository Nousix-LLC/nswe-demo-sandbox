# Task: Durability proof — test coverage, depth, and the drill — PR #113

## Task Specification

**Slug**: SUBTASK_durability_proof
**Task Kind**: standard
**Status**: Pending

### Objective

Judge whether the tests and the durability drill actually *prove* the acceptance criteria and the failure
paths — or pass vacuously. Read the tests as closely as the code.

### Context

Part of the PR #113 review DAG (see `../_GLOBAL.md`). This is the companion to the correctness concern:
correctness asks "does the code do it"; this asks "is it proven". Read-only; write a findings document only.

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Pinned commit, target, constraints |
| Contract | `../contracts/finding_schema.md`, `../contracts/_MANIFEST.yaml` | Findings format + rubric |
| PR #113 diff @ `09fa453` | `gh pr diff 113` / `git` (read-only) | Tests, drill scripts, CI wiring |
| Issues #65, #66, #67 | `gh issue view` | The criteria each test/drill must prove |
| Design | `design/release-bar.md` | Any `BAR-*` naming a durability/proof bar |

## The bar (what blocks)

A criterion with **no real proof**, or a drill/test that proves less than it claims, is a finding — **blocking
when it leaves an acceptance criterion unproven**. Examine at least:

- Do tests + drill exercise each acceptance criterion AND the failure paths: **restart, redeploy,
  reschedule**; **concurrency**; **a write that cannot durably commit** (fail-closed)?
- Do assertions check **real surviving state** — byte-for-byte rows AND system-level sign-in / content /
  counts through the HTTP API — rather than that something merely ran? Does any double stand in for the logic
  under test instead of for a boundary?
- Is the drill **genuinely repeatable and runnable by a stranger** with no hidden local state?
- Is the `postgres` feature **correctly gated** so the default build/test stays store-free while the durable
  tests run against a real PostgreSQL?

## Output

`SUBTASK_durability_proof/outputs/findings.md`, conforming to `../contracts/finding_schema.md` (prefix `DUR`).

## Success criteria

- [ ] Each criterion's proof (or absence of proof) assessed; failure paths checked; drill repeatability and
  feature-gating judged.
- [ ] "What I checked" and "what I found clean" both stated specifically.
- [ ] Findings pinned, severities + `blocks_landing` honest, each with "what would satisfy me"; sub-verdict.

## Constraints

Read-only on the repo; no GitHub writes. No host/cluster/SSH/credential details or DAG internals. Plain voice.
