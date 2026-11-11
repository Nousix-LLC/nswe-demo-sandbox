# COMPLETE — B3: Bind DOM→signal plumbing (REQ-ASYNC-042)

**Task**: SUBTASK_b3_bind_dom  
**Status**: completed  
**Branch**: work/ferric-async-forms-r2  
**Commit**: 838239e

---

## What was done

Satisfied REQ-ASYNC-042 by adding `Bind::on_input_event_handler()` to
`crates/ferric/src/form.rs` and a WASM integration test that exercises
the full DOM→signal path.

### Changes committed (838239e)

**`crates/ferric/src/form.rs`**

1. Added `#[cfg(target_arch = "wasm32")]` imports:
   ```rust
   #[cfg(target_arch = "wasm32")]
   use wasm_bindgen::JsCast;
   #[cfg(target_arch = "wasm32")]
   use web_sys::{Event, HtmlInputElement};
   ```

2. Added `Bind::on_input_event_handler()` method (gated `#[cfg(target_arch = "wasm32")]`):
   - Returns `EventHandler::WithEvent(Rc::new(...))` 
   - Closure captures `self.raw` (`Signal<String>`)
   - Chain: downcast `&dyn Any` → `&web_sys::Event` → `event.target()` →
     `dyn_into::<HtmlInputElement>()` → `.value()` → `raw.set(value)`
   - Any failing step silently returns — no panic

3. Added `wasm_tests` module with `#[wasm_bindgen_test]` for REQ-ASYNC-042:
   - Inserts real `<input>` into document body (so dispatched events have valid `target()`)
   - Sets element value to `"hello"`
   - Wires handler via `add_event_listener_with_callback`
   - Dispatches synthetic `input` event (browser sets `event.target()` to element)
   - Asserts `field.raw() == "hello"`

**`crates/ferric/src/dom.rs`**, **`crates/ferric/src/vdom.rs`**

Applied `cargo fmt` to pre-existing formatting drift so `cargo fmt --all --check`
is green (required by the CI `fmt` job).

---

## Verification results

| Check | Result |
|-------|--------|
| `cargo test -p ferric` | ✓ 83 passed, 0 failed |
| `cargo clippy -p ferric` | ✓ no warnings |
| `cargo test -p ferric --target wasm32-unknown-unknown --no-run` | ✓ compiles |
| `RUSTDOCFLAGS="-D warnings" cargo doc -p ferric --no-deps` | ✓ no warnings |
| `cargo fmt --all --check` | ✓ clean |

All 18 existing native `form.rs` tests pass unchanged.
`on_input_handler()` and `set_input()` are unmodified.
`vdom.rs` does not import `web_sys`.

---

## Declared output

Committed and pushed to `work/ferric-async-forms-r2` (commit 838239e).
