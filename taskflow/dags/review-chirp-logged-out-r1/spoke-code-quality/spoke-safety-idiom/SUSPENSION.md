# Suspension Record — spoke-safety-idiom

## Status

Suspended (NeedsDecompose). Waiting on child subtree to reach terminal states.

## Decomposition Decision

The brief for `spoke-safety-idiom` enumerated two distinct analyses from different methodology
domains:

- **Concern 8** (error message safety): security domain — `AppError`/`user_message()` leakage to UI
- **Concern 10** (Rust/WASM idiom): Rust domain — `spawn_local`, `thread_local!`+`RefCell`,
  `Cell<bool>`, `Closure::forget()` in `hydrate.rs`

The scope-based trigger and the Distinct Concerns Test fired by that enumeration. These are
independent analyses on disjoint file sets that can run in parallel with different specialist
methodologies.

## Children Materialized

| Child | Concern | Output | Status |
|-------|---------|--------|--------|
| `spoke-error-safety` | 8 — AppError / user_message() safety | `spoke-error-safety/error_safety_findings.md` | Pending |
| `spoke-rust-idiom` | 10 — Rust/WASM idiom patterns in hydrate.rs | `spoke-rust-idiom/rust_idiom_findings.md` | Pending |
| `spoke-safety-synthesis` | Synthesis gate | `FINDINGS.md` (fold record: `SYNTHESIS.md`) | Pending (depends on above) |

## Resumption Condition

All three child tasks reach terminal lifecycle states. The synthesis child (`spoke-safety-synthesis`)
folds this task SUSPENDED→COMPLETED by calling `engine_resume_suspended` after producing
`FINDINGS.md` and `SYNTHESIS.md` at this workspace root.

## Outputs Expected at Completion

- `FINDINGS.md` — combined findings for concerns 8 and 10, conforming to
  `../contracts/findings_schema.md`
