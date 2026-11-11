# Ferric Async Resource Primitives — API Notes (PR #193)

Survey of async data-fetching primitives, loading/error/data state model, component creation
patterns, and form/event binding introduced by PR #193 in `crates/ferric/`.

---

## Source Locations

- `src/async_resource.rs` — `ResourceState<T>` enum, `Resource<T>` struct, `create_resource`
  function, `suspense` boundary function
- `src/form.rs` — `FormField<T>` typed form state, `Bind<T>` two-way binding descriptor
- `src/component.rs` — `Component` trait, function-component blanket impl, `Children` / `Slot`
  / `SlotFn<T>` slot types
- `src/lib.rs` — prelude re-exports (`ResourceState`, `Resource`, `suspense`, `Bind`,
  `FormField`) that constitute the stable public surface

---

## Public API

### Async State Enum

```rust
/// Three-state discriminant for every async resource.
#[derive(Debug)]
pub enum ResourceState<T> {
    /// Fetch is in flight; no value is available yet.
    Loading,
    /// Fetch completed successfully; the payload is available.
    Ready(T),
    /// Fetch failed; the message is the stringified error.
    Failed(String),
}

impl<T: Clone> Clone for ResourceState<T> { /* … */ }
```

### Resource Handle

```rust
/// Reactive handle to an async-loaded value.
/// `Copy` — cheap to pass to child closures.
pub struct Resource<T: 'static> {
    signal: Signal<ResourceState<T>>,
}

impl<T: 'static> Resource<T> {
    /// Spawn a one-shot async task; initialises the resource in `Loading`.
    pub fn new(fut: impl Future<Output = T> + 'static) -> Self;

    /// Like `new`, but the future returns `Result<T, String>`; maps `Err` to `Failed`.
    pub fn new_fallible(fut: impl Future<Output = Result<T, String>> + 'static) -> Self;

    /// Read the current state.  Reactive: calling inside an effect/memo tracks the signal.
    pub fn state(&self) -> ResourceState<T>
    where
        T: Clone;
}
```

### Reactive Resource Creation

```rust
/// Create a resource that re-fetches automatically when `source` returns a new value.
///
/// * `source` — a reactive closure; whenever it returns a new `S` the fetcher is re-invoked.
/// * `fetcher` — receives the latest `S` and returns a `Future<Output = T>`.
///
/// A generation counter cancels superseded in-flight futures so out-of-order responses
/// cannot overwrite a later result.
pub fn create_resource<S, F, T>(
    source: impl Fn() -> S + 'static,
    fetcher: impl Fn(S) -> F + 'static,
) -> Resource<T>
where
    S: 'static,
    F: Future<Output = T> + 'static,
    T: 'static,
```

### Suspense Boundary

```rust
/// Renders `fallback()` while any `Resource` read inside `children()` is `Loading`.
/// Once all resources inside are `Ready` or `Failed`, renders `children()` instead.
///
/// Implemented via thread-local counters (`SUSPENSE_DEPTH`, `SUSPENSE_HAS_LOADING`);
/// nesting is supported.
pub fn suspense(fallback: impl Fn() -> VNode, children: impl Fn() -> VNode) -> VNode;
```

### Form State

```rust
/// Typed form field: holds the raw string the user typed plus a parse-on-demand policy.
/// Backed by a `Signal<String>` so reading `.raw()` / `.parsed()` inside effects is tracked.
pub struct FormField<T> {
    pub(crate) raw: Signal<String>,
    _marker: PhantomData<T>,
}

impl<T: FromStr + Clone + 'static> FormField<T>
where
    T::Err: std::fmt::Display,
{
    /// Construct with an initial raw string (may or may not parse successfully).
    pub fn new(initial: &str) -> Self;

    /// Current raw text; reactive — tracked when read inside an effect or memo.
    pub fn raw(&self) -> String;

    /// Attempt to parse the raw text; returns `Ok(T)` or `Err(display_message)`.
    /// Never silently coerces invalid input.
    pub fn parsed(&self) -> Result<T, String>;

    /// Update the raw text and notify all reactive subscribers.
    pub fn set_raw(&self, raw: String);
}
```

### Two-Way Input Binding

```rust
/// Binding descriptor for `<input>` elements.  Produces a `value` attribute and an
/// `on_input` event handler that together keep `FormField<T>` and the DOM in sync.
pub struct Bind<T: FromStr + Clone + 'static>
where
    T::Err: std::fmt::Display,
{
    raw: Signal<String>,
    input_buf: Signal<String>,
    _marker: PhantomData<T>,
}

impl<T: FromStr + Clone + 'static> Bind<T>
where
    T::Err: std::fmt::Display,
{
    /// Construct from a `FormField<T>`.
    pub fn new(field: &FormField<T>) -> Self;

    /// Returns `("value", current_raw_string)` for use as a VNode attribute.
    pub fn value_attr(&self) -> (&'static str, String);

    /// Returns a `NoArg` `EventHandler`: flushes the internal buffer into the field signal.
    /// Use when the runtime delivers pre-extracted string values.
    pub fn on_input_handler(&self) -> EventHandler;

    /// Push a new string into the internal buffer (call before `on_input_handler` fires).
    pub fn set_input(&self, value: String);

    /// Returns a `WithEvent` `EventHandler` that reads `HtmlInputElement.value()` via web-sys.
    /// Only available on `wasm32`; preferred for real DOM event dispatch.
    #[cfg(target_arch = "wasm32")]
    pub fn on_input_event_handler(&self) -> EventHandler;
}
```

### Component Abstraction

```rust
/// A component renders itself to a view tree.  `render` is re-invoked by the runtime
/// (inside a reactive `create_effect`) when the signals it reads change.
pub trait Component {
    fn render(&self) -> VNode;
}

/// Any `Fn() -> VNode` is a component — no boilerplate struct needed.
impl<F: Fn() -> VNode> Component for F {
    fn render(&self) -> VNode { (self)() }
}

/// Deferred child content — `Rc<dyn Fn() -> Vec<VNode>>`.
pub type Children = ::std::rc::Rc<dyn Fn() -> Vec<VNode>>;

/// Named content region, same shape as `Children`.
pub type Slot = ::std::rc::Rc<dyn Fn() -> Vec<VNode>>;

/// Parameterised content region (render-prop pattern).
pub type SlotFn<T> = ::std::rc::Rc<dyn Fn(T) -> Vec<VNode>>;
```

### Prelude Re-exports

The stable public surface consumers import from `ferric::prelude`:

```rust
pub use crate::async_resource::{suspense, Resource, ResourceState};
pub use crate::form::{Bind, FormField};
// (signal, component, vdom APIs also re-exported — see lib.rs)
```

---

## State Model

`ResourceState<T>` is a three-variant discriminant enum covering the full async lifecycle:

| Variant | Meaning | When present |
|---------|---------|--------------|
| `Loading` | Fetch in flight, no value yet | Initial state; also set when `create_resource` re-fetches on a source change |
| `Ready(T)` | Fetch succeeded, payload available | Set by the runtime after the future resolves to `T` |
| `Failed(String)` | Fetch failed, message is display string | Set when `new_fallible` future resolves to `Err(msg)` |

**Transitions**: `Loading → Ready(T)` on success; `Loading → Failed(String)` on error.
When a reactive source signal changes, the resource resets to `Loading` and a new fetch begins.
A generation counter ensures that an out-of-order response from a superseded fetch cannot
transition the state from a newer `Loading` to a stale `Ready`.

`FormField<T>` has no explicit state enum — validity is on-demand via `parsed() -> Result<T, String>`.
Invalid input is preserved verbatim in the `raw` signal; the field never coerces or discards user
input silently.

---

## Usage Example

### One-Shot Resource (no reactive source)

```rust
use ferric::prelude::*;

// A function component that loads a post by ID.
let post_id: u64 = 42;
let resource = Resource::<Post>::new_fallible(async move {
    fetch_post(post_id).await.map_err(|e| e.to_string())
});

// Render via suspense boundary:
let view = move || -> VNode {
    suspense(
        || text("Loading…"),
        move || match resource.state() {
            ResourceState::Loading  => text("Loading…"),
            ResourceState::Ready(p) => VElement::new("article")
                                           .child(text(p.title))
                                           .into(),
            ResourceState::Failed(e) => text(format!("Error: {e}")),
        },
    )
};
```

### Reactive Resource (re-fetches on signal change)

```rust
use ferric::prelude::*;

let page = create_signal(1_u32);

// Automatically re-fetches whenever `page` changes.
let posts = create_resource(
    move || page.get(),            // source — read is tracked
    |p| async move { fetch_page(p).await },  // fetcher
);

let view = move || -> VNode {
    suspense(
        || text("Loading…"),
        move || match posts.state() {
            ResourceState::Loading    => text("…"),
            ResourceState::Ready(ps)  => render_post_list(ps),
            ResourceState::Failed(e)  => text(format!("Error: {e}")),
        },
    )
};

// Navigating to page 2 triggers a re-fetch automatically:
page.set(2);
```

### Form Field + Two-Way Binding

```rust
use ferric::prelude::*;

let username: FormField<String> = FormField::new("");
let bind = Bind::new(&username);

// In the view closure — produce an <input> with live two-way binding:
let (attr_name, attr_val) = bind.value_attr();          // ("value", current_raw)
let handler = bind.on_input_handler();                  // NoArg handler flushes buffer
// On wasm32 use on_input_event_handler() instead for real DOM events.

let submit = move || {
    match username.parsed() {
        Ok(name)  => submit_form(name),
        Err(msg)  => show_error(msg),
    }
};
```

---

## Notable Limitations

- **No `use_resource` hook shorthand**: the API is `Resource::new` / `create_resource`; there
  is no single-call `use_resource(cx, || async { … })` ergonomic wrapper.  Callers manage
  the resource handle explicitly.
- **`new_fallible` only** covers `Result<T, String>`; arbitrary error types require pre-conversion
  (`map_err(|e| e.to_string())`).
- **`on_input_event_handler` is `wasm32`-only**: on non-WASM targets (tests, SSR) only the
  `set_input` + `on_input_handler` path is available; real DOM event dispatch is WASM-exclusive.
- **No derived `PartialEq` on `ResourceState<T>`**: equality comparisons require pattern-matching
  or a manual `impl`.
- **`suspense` is not async-aware for SSR**: the `SUSPENSE_DEPTH` / `SUSPENSE_HAS_LOADING`
  thread-locals are WASM-runtime primitives; SSR integration (PR #228) may require separate
  handling.

---

## Integration Notes

- `Resource<T>` wraps a `Signal<ResourceState<T>>`, so reading `resource.state()` inside any
  reactive context (effect, memo, component render) automatically tracks the resource and
  re-renders when the fetch completes.
- `FormField<T>` and `Bind<T>` are also signal-backed; a component that reads `field.raw()`
  re-renders whenever the user types.
- Component render functions (`Fn() -> VNode`) are run inside `create_effect` by the DOM
  runtime; no explicit subscription call is needed — signal reads in the render closure are
  tracked automatically.
- `Children` / `Slot` / `SlotFn<T>` from `component.rs` compose naturally with `suspense`:
  pass a slot thunk as the `children` argument to wrap an entire child tree under one suspense
  boundary.
