# COMPLETE — navigate_replace (SUBTASK_navigate_replace)

## Summary

Implemented `navigate_replace` in `crates/ferric-router` on branch `work/ferric-router-r1`,
created from `work/ferric-epic-authoring-r1` HEAD (commit `e29e2f4`). All success criteria met.

## What was done

### Branch
- Created `work/ferric-router-r1` from `work/ferric-epic-authoring-r1` HEAD and pushed to `origin`.

### Implementation — `crates/ferric-router/src/router.rs`
Added `navigate_replace(path: &str)` immediately before `current_path()`, following the exact
pattern of `navigate`:

- **On wasm32**: calls `history.replace_state_with_url(&JsValue::NULL, "", Some(path))` using
  the existing `History` web-sys feature already in `Cargo.toml` (no new Cargo.toml entries).
- **All targets**: calls `set_current_path(path.to_string())` to update reactive routing state.
- **Doc-comment**: explains push vs. replace and when to choose replace.

### Prelude — `crates/ferric-router/src/lib.rs`
Added `navigate_replace` to the prelude export (additive only; `navigate`, `current_path`,
`Router`, `link`, `Params`, `RoutePattern` unchanged).

### Tests — native (`#[cfg(test)]`)
- `navigate_replace_updates_current_path`: after `navigate_replace("/new")`, `current_path() == "/new"`.
- `navigate_replace_and_navigate_both_update_path`: verifies replace then push both update `current_path()`.

### Tests — wasm-bindgen browser (`#[cfg(all(test, target_arch = "wasm32"))]`)
- `navigate_replace_does_not_grow_history`: records `history.length` before `navigate_replace`,
  asserts unchanged after; records length after `navigate` (push), asserts it grew.

## Verification

| Check | Result |
|---|---|
| `cargo test -p ferric-router` | ✅ 30 passed (28 pre-existing + 2 new native) |
| `cargo clippy -p ferric-router -- -D warnings` | ✅ Clean |
| `cargo fmt --check -p ferric-router` | ✅ Clean |
| `cargo build -p ferric-router --target wasm32-unknown-unknown` | ✅ Succeeded |
| Frozen prelude items unchanged | ✅ `navigate`, `current_path`, `Router`, `link`, `Params`, `RoutePattern` untouched |
| Contract identity `navigate_replace_added` | ✅ Function present and exported from prelude |

## Commit

Commit `89687da` on `work/ferric-router-r1`:
> feat(ferric-router): add navigate_replace (REQ-RT-003)
