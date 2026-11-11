# SUBTASK_form_binding

## Objective
Implement two-way form binding in `crates/ferric/src/form.rs`: `FormField<T>` (typed form state)
and `Bind<T>` (two-way binding descriptor), fully replacing the stub left by the walking skeleton.
The design ensures unvalidated input cannot be submitted as `T`.

## Inputs
- Repository: `Nousix-LLC/ferric`, branch `work/ferric-async-forms-r1`
  (walking skeleton has stubs for `form.rs` and `lib.rs` already declares `pub mod form;`)
- Contract: `../contracts/module_interfaces.md` — exact public API surface to implement
- Existing reactive runtime: `crates/ferric/src/signal.rs` (`Signal<T>`, `Memo<T>`, `create_signal`, `create_memo`)
- Existing vdom: `crates/ferric/src/vdom.rs` (`VElement`, `EventKind`, `EventHandler`) — the walking skeleton has already added `Change` and `Input` variants (they already existed; `Submit` is now also available)
- No new Cargo.toml dependencies needed (uses existing `signal` + `vdom` internals)

## Declared Outputs
1. `crates/ferric/src/form.rs` — full implementation replacing the stub:
   - `FormField<T: FromStr + Clone + 'static>` struct:
     - Holds a `Signal<String>` for raw input and a reactive derived parsed value
     - `FormField::new(initial: &str) -> Self`
     - `raw(&self) -> String` — current raw string (reactive read)
     - `parsed(&self) -> Result<T, String>` — parse attempt; `Err` message is `Display` of parse error
     - `set_raw(&self, raw: String)` — updates the raw signal
   - `Bind<T: FromStr + Clone + 'static>` struct wrapping a `FormField<T>`:
     - `Bind::new(field: &FormField<T>) -> Self`
     - `value_attr(&self) -> (&'static str, String)` — returns `("value", current_raw)`
     - `on_input_handler(&self) -> EventHandler` — returns a `Rc<dyn Fn()>` that reads
       the input element's current value and calls `set_raw`. (The input value is captured
       via a `Signal<String>` and updated from JS; see note below.)
   - Exhaustive `#[cfg(test)]` unit tests (non-WASM where possible)
2. Changes committed to `work/ferric-async-forms-r1` and pushed
3. `cargo check --target wasm32-unknown-unknown` passes after changes

## Success Criteria
- `FormField<T>::parsed()` returns `Err(String)` when the raw string does not parse to `T`; callers cannot silently coerce bad input to `T`
- `FormField<T>` is reactive: a `create_effect` that calls `raw()` or `parsed()` re-runs when `set_raw()` is called
- `Bind::on_input_handler()` returns a handler that updates the field's raw value
- Tests cover: initial value round-trip; set_raw → parsed succeeds; set_raw with bad value → parsed returns Err; reactive re-render after set_raw
- No existing tests broken; `cargo check --target wasm32-unknown-unknown` passes

## Implementation Note on on_input_handler

`EventHandler = Rc<dyn Fn()>` takes no arguments. To read the DOM input element's value,
the handler needs to reach into the DOM. Two viable approaches:
1. Store a `Signal<String>` for raw value; the handler updates the signal from a captured
   JS `HtmlInputElement` reference obtained once during binding — this requires WASM.
2. Simpler: the `on_input_handler` just calls `set_raw` with a value read from a secondary
   `Signal<String>` that gets written by a companion `set_input_signal` method the caller
   invokes. This is WASM-free and testable in pure Rust.

Prefer approach 2 for testability. If a WASM-coupled approach is needed, use `#[cfg(target_arch = "wasm32")]` guards and ensure the non-WASM path still compiles and tests run.

## Constraints
- **Owned file**: `crates/ferric/src/form.rs` exclusively. Do not modify `vdom.rs`, `signal.rs`, `dom.rs`, `lib.rs`, or `async_resource.rs`.
- `EventHandler = Rc<dyn Fn()>` is frozen — the handler signature must not change.
- Do not add new Cargo.toml dependencies.
- `T::Err: std::fmt::Display` bound is required for `parsed()` to produce a `String` message.
- Security: never commit credentials or tokens.
