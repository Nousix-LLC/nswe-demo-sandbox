# Module Interface Contracts

These are the public types each new module must export at completion. They are frozen
by the walking skeleton (declared as stubs) and filled in by the feature spokes.
Synthesis verifies the exports match this contract before creating the PR.

---

## async_resource.rs

Owned by: SUBTASK_async_resource

### Required Exports (re-exported via `crates/ferric/src/lib.rs` prelude)

```rust
/// Async resource lifecycle state.
/// Exhaustively matchable — callers cannot receive a `Ready(T)` before it has resolved.
pub enum ResourceState<T> {
    Loading,
    Ready(T),
    Failed(String),
}

/// A reactive handle to an async-loaded value.
/// Wraps a `Signal<ResourceState<T>>` driven by a Rust async future.
pub struct Resource<T: 'static> { /* opaque */ }

impl<T: 'static> Resource<T> {
    /// Create a resource that runs `fut` once and stores the result.
    pub fn new(fut: impl Future<Output = T> + 'static) -> Self;

    /// Read the current state. Reactive: calling this inside a signal/effect
    /// subscribes the caller to state changes.
    pub fn state(&self) -> ResourceState<T>;
}
```

### Suspense component (may be a function component or struct, implementer's choice)

```rust
/// Renders `fallback` while any child Resource is Loading, then renders `children`.
/// Minimal viable form: takes two VNode closures.
pub fn suspense(fallback: impl Fn() -> VNode, children: impl Fn() -> VNode) -> VNode;
```

### wasm-bindgen / async integration notes

- Use `wasm_bindgen_futures::spawn_local` to drive the future.
- Signal updates from the async callback must be valid (no cross-thread issues since WASM is single-threaded).
- `ResourceState<T>` must derive `Clone` where `T: Clone`, or store inside `Rc<RefCell<...>>`.

---

## form.rs

Owned by: SUBTASK_form_binding

### Required Exports (re-exported via prelude)

```rust
/// Typed form state wrapper.
/// `T` is the validated/parsed form value type (e.g., a struct).
/// The raw string buffer is kept separate so unvalidated input cannot be submitted.
pub struct FormField<T> {
    // internal: raw string signal + parsed signal
}

impl<T: FromStr + Clone + 'static> FormField<T>
where T::Err: std::fmt::Display
{
    /// Create a field with an initial raw value.
    pub fn new(initial: &str) -> Self;

    /// Current raw string (for binding to input.value).
    pub fn raw(&self) -> String;

    /// Current parsed value, or the parse error message.
    pub fn parsed(&self) -> Result<T, String>;

    /// Update raw value (called on input/change events).
    pub fn set_raw(&self, raw: String);
}

/// Two-way binding descriptor for use in VElement construction.
/// Produces the `value` attribute and an `on_input` / `on_change` handler pair.
pub struct Bind<T: FromStr + Clone + 'static>
where T::Err: std::fmt::Display
{
    // wraps a FormField<T>
}

impl<T: FromStr + Clone + 'static> Bind<T>
where T::Err: std::fmt::Display
{
    pub fn new(field: &FormField<T>) -> Self;

    /// Returns `("value", current_raw)` attr pair.
    pub fn value_attr(&self) -> (&'static str, String);

    /// Returns the on_input handler (wraps set_raw).
    pub fn on_input_handler(&self) -> EventHandler;
}
```

### Design note on "typed so unvalidated input cannot be submitted"

`FormField<T>` keeps raw and parsed as separate reactive signals.
A form submit handler reads `field.parsed()` and gets `Err(_)` if the input is invalid,
forcing the caller to handle the error case explicitly. The form binding never silently
coerces invalid input to `T`. That is the contract.

---

## Cargo.toml additions (skeleton adds, spokes must not duplicate)

For async_resource.rs the skeleton adds to `crates/ferric/Cargo.toml`:

```toml
[dependencies]
wasm-bindgen-futures = "0.4"
```

The skeleton also adds the following web-sys feature if not already present:
```toml
# (no additional web-sys features needed for basic resource impl)
```

For form.rs: no new dependencies (uses existing `Signal`, `Memo`, `EventKind`).
