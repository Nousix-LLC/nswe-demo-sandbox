# SUBTASK_dom_events — COMPLETE

## Status
Completed successfully.

## What was done

### `crates/ferric/src/dom.rs`
- Replaced the two-variant `todo!()` stubs (`Click`, `Input`) with exhaustive `match` tables
  covering all 48 `EventKind` variants (47 static + `Custom(String)`).
- Changed `event_name` / `stash_key` signatures from `(EventKind) -> &'static str` to
  `(&EventKind) -> String` so the `Custom(String)` variant can return its contained string
  without lifetime violations.
- Added `static_event_kinds()` helper returning all 47 static variants as a `[EventKind; 47]`
  array; used by `set_events` to scan every stash slot during the detachment pass.
- Updated `set_events` detachment step:
  - Iterates `static_event_kinds()` to remove any previously-stashed static listeners.
  - Reads a `js_sys::Array` stored under `"__ferric_custom_events"` on the element to remove
    previously-bound custom listeners, then deletes the property.
- Updated `set_events` bind step:
  - All 48 variants use `Closure::wrap(... |_event: web_sys::Event| handler() ...)` with the
    existing `closure.forget()` lifetime/leak strategy.
  - Tracks newly-bound `Custom` event names and writes them to `"__ferric_custom_events"` for
    the next re-bind pass.
- `Custom(String)` stash key is `"__ferric_on_custom_{s}"` — prefixed differently from every
  static key to prevent collisions (e.g. `Custom("click")` ≠ static `Click`).
- Exhaustive `match` in both `event_name` and `stash_key` — no `_` wildcard — so adding a new
  `EventKind` variant produces a compile error.
- Updated and extended native unit tests to cover the full variant set and Custom behavior.

### `crates/ferric/Cargo.toml`
Added eight web-sys features (additive only; no version changes):
`KeyboardEvent`, `FocusEvent`, `PointerEvent`, `DragEvent`, `TouchEvent`,
`ClipboardEvent`, `AnimationEvent`, `TransitionEvent`.

## Verification
- `cargo check -p ferric --target wasm32-unknown-unknown` — **passed** (clean, 0 errors)
- `cargo test -p ferric` — **74 passed, 0 failed** (all pre-existing tests plus new dom tests)

## Commit
`6de5e09` — `feat(dom): extend event binding to full EventKind set`  
Branch: `work/ferric-async-forms-r1` (pushed to origin)
