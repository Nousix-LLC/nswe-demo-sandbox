# SUBTASK_dom_events

## Objective
Extend `crates/ferric/src/dom.rs` to bind all `EventKind` variants declared by the walking
skeleton to real DOM event listeners, replacing the existing two-variant (Click, Input) binding
with the full set from `contracts/event_kind_contract.md`.

## Inputs
- Repository: `Nousix-LLC/ferric`, branch `work/ferric-async-forms-r1`
  (walking skeleton has already extended `EventKind` in `vdom.rs` to the full set)
- Contract: `../contracts/event_kind_contract.md` — full event variant list and DOM string mapping table
- Existing `crates/ferric/src/dom.rs` — has `bind_events` / event attachment logic using `add_event_listener_with_callback`
- Existing `crates/ferric/Cargo.toml` — web-sys features already include `Event`, `EventTarget`, `InputEvent`, `MouseEvent`

## Declared Outputs
1. `crates/ferric/src/dom.rs` — event binding extended:
   - All `EventKind` variants from `contracts/event_kind_contract.md` mapped to their DOM event strings
   - `Custom(String)` variant handled by using the string directly as the event name
   - The existing `Input` / `Change` special handling for `HtmlInputElement.value()` preserved
   - Any required web-sys feature flags added to `crates/ferric/Cargo.toml` (keyboard events, pointer events, drag events, touch events, etc.)
   - Exhaustive `match` on `EventKind` — no `_` wildcard — so adding a new variant is a compile error
2. Changes committed to `work/ferric-async-forms-r1` and pushed
3. `cargo check --target wasm32-unknown-unknown` passes after changes

## Success Criteria
- All 50+ EventKind variants (including Custom) are handled in the DOM binding dispatch
- The `match` on `EventKind` is exhaustive (no wildcard) so future variant additions surface as compile errors
- Existing Click and Input behavior is preserved exactly (no regression)
- Change variant behaves identically to Input for HtmlInputElement targets (reads `.value()`)
- Any newly required web-sys features are added to Cargo.toml
- No existing tests broken; `cargo check --target wasm32-unknown-unknown` passes

## Constraints
- **Owned file**: `crates/ferric/src/dom.rs` and `crates/ferric/Cargo.toml` (web-sys feature additions only — no version changes, no other dep changes) exclusively. Do not modify `vdom.rs`, `signal.rs`, `component.rs`, `lib.rs`, `async_resource.rs`, or `form.rs`.
- `EventHandler = Rc<dyn Fn()>` type is frozen — do not change the handler signature. All event kinds call the handler as `handler()` with no arguments; richer event data extraction is out of scope for this PR.
- Use `wasm_bindgen::closure::Closure` to wrap each handler, as the existing code does. Maintain the same lifetime/leak strategy the existing code uses.
- The `Custom(String)` variant must use the contained string as the raw DOM event name.
- Security: never commit credentials or tokens.
