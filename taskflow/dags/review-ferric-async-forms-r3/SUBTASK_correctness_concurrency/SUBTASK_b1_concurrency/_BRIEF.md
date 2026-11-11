# Task: B1 Correctness + Concurrency Analysis — async_resource.rs

## Task Specification

**Slug**: SUBTASK_b1_concurrency
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Verify that B1 (REQ-ASYNC-001, REQ-ASYNC-003, REQ-ASYNC-005, REQ-ASYNC-016) is
correctly implemented in `create_resource` in `crates/ferric/src/async_resource.rs`
(PR #193, head `838239e`). Additionally assess whether the `spawn_local`/`create_effect`
composition introduces any concurrency or async hazards.

---

## Context

See `../_GLOBAL.md` for subtree context. See `../../_GLOBAL.md` for full project
context, acceptance criteria, and PR coordinates.

**Files to review**: `crates/ferric/src/async_resource.rs` (new file in PR #193)

**Key commit**: `9fedad9` — "feat(ferric): add create_resource reactive async constructor"

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Scope, constraints, contract |
| Project context | `../../_GLOBAL.md` | Acceptance criteria, REQ-ASYNC-001,003,005,016 |
| PR diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| async_resource.rs | PR diff (new file) | The create_resource implementation |
| Inherited contract | `../../contracts/_MANIFEST.yaml` | Findings schema |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Ownership + identities |

---

## Review Scope

**B1 correctness questions (REQ-ASYNC-001, 003, 005, 016):**
- Does `create_resource(source, fetcher)` exist as a two-argument function? Does it fire immediately on construction (REQ-ASYNC-001)?
- When a signal read by `source()` changes, does the resource reset to `Loading` and re-trigger the fetcher with the new source value (REQ-ASYNC-003)?
- Are in-flight futures from stale source values discarded — specifically, is there a generation counter, and does the future compare its generation before writing its result (REQ-ASYNC-005, REQ-ASYNC-016)?

**Concurrency and async hazard questions:**
- Does `create_resource` use `spawn_local` inside a reactive effect (`create_effect`)? Verify no double-borrow or use-after-free issues in closure captures (Rc/Cell patterns).
- Does the generation counter use types with `'static` bounds as required by the async closure? Is `Rc<Cell<u64>>` correct here?
- In a single-threaded WASM executor: is there any scenario where the effect and the future's completion handler race to access the same mutable state without protection? Verify the reasoning is sound.
- Is the generation counter implementation sound (no stale future can overwrite a newer result)?

---

## Output Specification

**Primary Output**: `b1_findings.md` at `SUBTASK_b1_concurrency/` workspace root

Must contain:
1. `## Findings` — entries for each question above with:
   - severity: blocker | non-blocker | clean
   - requirement: REQ-ASYNC-NNN
   - location: crates/ferric/src/async_resource.rs:LINE
   - description
2. `## What was examined` — files, line ranges, specific questions checked

---

## Constraints

- Repository-relative paths only in all locations
- Non-blockers #196–#201 must NOT be re-raised as blockers
- A finding is a blocker only if the requirement is unmet
- Evidence must come from reading the actual source code

## Success Criteria

- REQ-ASYNC-001, 003, 005, 016 each answered with evidence from code
- Concurrency hazard assessment complete for spawn_local/create_effect composition
- b1_findings.md produced with every question answered and severity assigned
