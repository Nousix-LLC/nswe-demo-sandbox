# _BRIEF.md — navigate-replace

**Goal slug**: `navigate-replace`
**Kind**: code (atomic)
**Repo**: Nousix-LLC/nswe-demo
**Branch**: `work/ferric-router-r1`
**Workspace**: `taskflow/dags/ferric-router-r1/SUBTASK_navigate_replace/`

---

## Objective

Create the `work/ferric-router-r1` branch from `work/ferric-epic-authoring-r1` HEAD, then
implement `navigate_replace` — the `replaceState` counterpart to the frozen `navigate` function
— in `crates/ferric-router`. Add `navigate_replace` to the prelude. Write tests.

This closes the replace-navigation requirement (REQ-RT-003) for the history navigation
capability in issue #146.

---

## Inputs

- Working repo at `/home/user/nswe-demo` (`Nousix-LLC/nswe-demo`)
- Current branch to base from: `work/ferric-epic-authoring-r1` (commit `e29e2f4`)
- Existing frozen surface: `crates/ferric-router/src/router.rs` (contains `navigate`,
  `navigate_replace` does NOT yet exist)
- Frozen prelude in `crates/ferric-router/src/lib.rs`:
  `pub use crate::router::{current_path, navigate, Router};`
- Contract: `taskflow/dags/ferric-router-r1/contracts/ferric_router_r1_api.md`
  (identity: `navigate_replace_added`)

---

## Declared output

- Branch `work/ferric-router-r1` created from `work/ferric-epic-authoring-r1` HEAD and pushed
  to `origin`
- Commits on `work/ferric-router-r1`:
  - `navigate_replace(path: &str)` function in `crates/ferric-router/src/router.rs`:
    - On wasm32: calls `history.replace_state_with_url(&JsValue::NULL, "", Some(path))` (using
      the existing `web-sys` `History` feature, already in `Cargo.toml`)
    - On all targets: calls `set_current_path(path.to_string())`
    - Doc-comment explains push vs. replace and when to choose replace
  - `navigate_replace` exported from the prelude in `crates/ferric-router/src/lib.rs`
  - Native tests in `src/router.rs` (or a `navigate_replace` submodule):
    - `navigate_replace_updates_current_path`: after `navigate_replace("/new")`,
      `current_path() == "/new"`
    - `navigate_replace_and_navigate_both_update_path`: verify replace and push both
      update `current_path()` (native — no history-length assertion off-wasm)
  - wasm-bindgen test (behind `#[cfg(all(test, target_arch = "wasm32"))]`):
    - `navigate_replace_does_not_grow_history`: records `history.length` before and after
      `navigate_replace`, asserts length unchanged; records it after `navigate`, asserts grew

---

## Success criteria

1. `work/ferric-router-r1` branch exists on `origin` with the commit(s) above.
2. `cargo test -p ferric-router` passes all tests (new + pre-existing frozen tests).
3. `cargo build -p ferric-router --target wasm32-unknown-unknown` succeeds.
4. `cargo clippy -p ferric-router -- -D warnings` clean.
5. `cargo fmt --check -p ferric-router` clean.
6. Contract identity `navigate_replace_added` is met (function present, prelude exports it).
7. The frozen prelude items (`navigate`, `current_path`, `Router`, `link`, `Params`,
   `RoutePattern`) are unchanged.

---

## Constraints

- Additive only: do not remove or modify any frozen #5 item.
- Use `history.replace_state_with_url` (the existing `History` web-sys feature already in
  `Cargo.toml`; no new Cargo.toml changes needed for this spoke).
- The exact name `navigate_replace` is specified. Do not name it `replace_navigate` or any
  other variant.
- Do not touch `design/` or any crate other than `crates/ferric-router`.
- Do not create a PR; leave that to the synthesis gate.
- Commit messages must NOT include the host server address, SSH key path, user name, or
  local paths.
