# COMPLETE: closure.forget() Scope Verification

## Task

Verify that `closure.forget()` in `form.rs`'s WASM test is strictly confined to test scope and assess the production `closure.forget()` in `dom.rs`'s `set_events()`.

## Verdict

**severity: clean** — both `closure.forget()` occurrences are correct:

1. `crates/ferric/src/form.rs:515` — strictly test-scoped via `#[cfg(all(test, target_arch = "wasm32"))]`; cannot appear in production WASM output.
2. `crates/ferric/src/dom.rs:287` — the stash-then-forget pattern: closure is set on the DOM element via `js_sys::Reflect::set` (lines 282–285) before `forget()` is called (line 287). The matching detach path (lines 236–262) confirms full lifecycle management.

## Output Produced

- `finding_forget.md` — sub-finding with severity, concern, location, description, and line-level evidence for all three sub-checks.

## What Was Examined

- PR #193 diff (commit 838239e) for all `closure.forget` occurrences
- `crates/ferric/src/form.rs` at HEAD of `work/ferric-async-forms-r2`: confirmed `#[cfg(all(test, target_arch = "wasm32"))]` outer gate and `#[wasm_bindgen_test]` inner gate
- `crates/ferric/src/dom.rs` at HEAD: confirmed stash-then-forget sequence, module-level doc comment naming the pattern, and detach path that removes listener and clears property
