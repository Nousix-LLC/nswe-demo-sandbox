# Ferric Framework Survey

Survey of the Ferric Rust/WASM frontend framework covering crate structure, async resource
primitives, client-side routing, server-side rendering/hydration, the idiomatic component
pattern, and known gaps. Assembled from API notes for PRs #193, #203, and #228 against
`Nousix-LLC/nswe-demo` `main`.

---

## 1. Crate Structure

### Top-level layout

Ferric ships as two crates:

| Crate | Path | Role |
|---|---|---|
| `ferric` | `crates/ferric/` | Core framework — signals, VDOM, async resources, SSR, hydration |
| `ferric-router` | `crates/ferric-router/` | Client-side routing (separate crate; uses `ferric` signals internally) |

`ferric-macros` lives at `crates/ferric-macros/` and is a proc-macro crate depended on by
`ferric` via a path dependency. It is not a public consumer-facing crate.

### `crates/ferric/src/` module layout

```
src/
  lib.rs           — Module declarations, re-exports, public prelude
  signal.rs        — Signals, effects, memos, batch, context API
  vdom.rs          — VNode, VElement, EventKind — the virtual DOM layer
  dom.rs           — mount() — attaches a component to a real DOM node
  component.rs     — Component trait, function-component blanket impl, Children/Slot/SlotFn
  async_resource.rs — ResourceState<T>, Resource<T>, create_resource, suspense
  form.rs          — FormField<T>, Bind<T> — typed form state + two-way binding
  ssr.rs           — render_to_string, TEXT_OPEN_MARKER, TEXT_CLOSE_MARKER
  hydrate.rs       — hydrate() — wasm32-only; re-attaches to server-rendered DOM
```

### Feature flags

There are **no Cargo feature flags**. SSR and hydration are always compiled; the
server-only vs. browser-only split is by compile-target `cfg`:

```toml
# crates/ferric/Cargo.toml — no [features] section
```

```rust
// lib.rs — hydrate is wasm32-only; render_to_string is always available
pub use crate::ssr::render_to_string;              // unconditional

#[cfg(target_arch = "wasm32")]
pub use crate::hydrate::hydrate;
```

### Public API surface — `ferric::prelude`

```rust
pub mod prelude {
    // Async resources and suspense
    pub use crate::async_resource::{suspense, Resource, ResourceState};
    // Components
    pub use crate::component::{Children, Component, Slot, SlotFn};
    // DOM entry point
    pub use crate::dom::mount;
    // Forms and two-way binding
    pub use crate::form::{Bind, FormField};
    // Reactivity primitives
    pub use crate::signal::{
        batch, create_effect, create_memo, create_signal,
        expect_context, provide_context, use_context,
        Memo, Signal,
    };
    // Virtual DOM types
    pub use crate::vdom::{EventKind, VElement, VNode};
    // Proc-macros
    pub use ferric_macros::{component, view};
}
```

Consumers import this prelude for virtually all Ferric usage. `ferric::render_to_string` and
`ferric::hydrate` are accessed directly (not via prelude).

---

## 2. Async Resource Primitives (PR #193)

### `ResourceState<T>` — the loading/error/data enum

```rust
/// Three-state discriminant for every async resource.
#[derive(Debug)]
pub enum ResourceState<T> {
    /// Fetch in flight; no value is available yet.
    Loading,
    /// Fetch completed successfully; the payload is available.
    Ready(T),
    /// Fetch failed; the message is the stringified error.
    Failed(String),
}

impl<T: Clone> Clone for ResourceState<T> { /* … */ }
```

### `Resource<T>` — reactive handle

```rust
/// Reactive handle to an async-loaded value. `Copy` — cheap to pass to closures.
pub struct Resource<T: 'static> {
    signal: Signal<ResourceState<T>>,
}

impl<T: 'static> Resource<T> {
    /// One-shot fetch; initialises in `Loading`.
    pub fn new(fut: impl Future<Output = T> + 'static) -> Self;

    /// One-shot fallible fetch; maps `Err` → `Failed(message)`.
    pub fn new_fallible(fut: impl Future<Output = Result<T, String>> + 'static) -> Self;

    /// Current state. Reactive: reading inside an effect or memo tracks this signal.
    pub fn state(&self) -> ResourceState<T>
    where T: Clone;
}
```

### `create_resource` — reactive re-fetch

```rust
/// Create a resource that re-fetches when `source` returns a new value.
/// A generation counter prevents out-of-order responses from overwriting a newer result.
pub fn create_resource<S, F, T>(
    source: impl Fn() -> S + 'static,
    fetcher: impl Fn(S) -> F + 'static,
) -> Resource<T>
where
    S: 'static,
    F: Future<Output = T> + 'static,
    T: 'static,
```

The `source` closure is reactive: whenever the signal(s) it reads change, the fetcher is
re-invoked with the new source value and the resource resets to `Loading`.

### `suspense` — loading boundary

```rust
/// Renders `fallback()` while any `Resource` read inside `children()` is `Loading`.
/// Nesting is supported.
pub fn suspense(fallback: impl Fn() -> VNode, children: impl Fn() -> VNode) -> VNode;
```

### Form state

```rust
/// Typed form field backed by a `Signal<String>`.
pub struct FormField<T> { /* … */ }

impl<T: FromStr + Clone + 'static> FormField<T> {
    pub fn new(initial: &str) -> Self;
    pub fn raw(&self) -> String;         // reactive read
    pub fn parsed(&self) -> Result<T, String>;
    pub fn set_raw(&self, raw: String);
}

/// Two-way binding descriptor for `<input>` elements.
pub struct Bind<T: FromStr + Clone + 'static> { /* … */ }

impl<T: FromStr + Clone + 'static> Bind<T> {
    pub fn new(field: &FormField<T>) -> Self;
    pub fn value_attr(&self) -> (&'static str, String);
    pub fn on_input_handler(&self) -> EventHandler;
    pub fn set_input(&self, value: String);

    #[cfg(target_arch = "wasm32")]
    pub fn on_input_event_handler(&self) -> EventHandler;
}
```

### State transitions

```
Loading ──→ Ready(T)        on successful fetch
        └─→ Failed(String)  on error (new_fallible only)
```

When `create_resource`'s source signal changes, the resource resets to `Loading` and a new
generation fetch begins. A generation counter ensures a superseded in-flight response cannot
write over a newer `Loading` state.

---

## 3. Router API (PR #203)

The router lives in a **separate crate**, `crates/ferric-router/`. It reuses
`ferric::signal` and `ferric::component` internally.

```rust
use ferric_router::prelude::*;
// exports: Router, navigate, navigate_replace, current_path, Params, RoutePattern, link
```

### `Router` — builder

```rust
pub struct Router {
    routes:   Vec<(RoutePattern, ViewFn)>,
    nested:   Vec<(RoutePattern, LayoutFn, Router)>,
    fallback: Option<ViewFn>,
}

impl Router {
    pub fn new() -> Self;

    // Flat route — exact segment match.
    pub fn route(self, pattern: &str, view: impl Fn(&Params) -> VNode + 'static) -> Self;

    // No-match fallback; invoked with empty Params.
    pub fn fallback(self, view: impl Fn(&Params) -> VNode + 'static) -> Self;

    // Nested route — prefix match with a layout wrapper.
    pub fn nest(
        self,
        prefix: &str,
        layout: impl Fn(&Params, &dyn Component) -> VNode + 'static,
        child_builder: impl FnOnce(Router) -> Router,
    ) -> Self;

    // Seed from window.location and install popstate listener (call once at startup).
    pub fn mount_history(self) -> Self;

    // Consume into a reactive Component. Mount with ferric::dom::mount.
    pub fn outlet(self) -> impl Component + 'static;
}
```

Routes resolve **first-match-wins** in declaration order. Register more specific patterns
before more general ones. Nested routes are tried before flat routes.

### Navigation API

```rust
/// Push a new History entry; all outlets re-render.
pub fn navigate(path: &str);

/// Replace the current History entry (use for login redirects, post-form redirects).
pub fn navigate_replace(path: &str);

/// Read the current path reactively (subscribes the calling context).
pub fn current_path() -> String;
```

On `wasm32`, `navigate` / `navigate_replace` wrap `history.pushState` /
`history.replaceState`. On native targets they update only the reactive signal, which is
useful for unit tests.

### Route matching and parameters

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RoutePattern { /* compiled; opaque */ }

impl RoutePattern {
    pub fn new(pattern: &str) -> Self;
    pub fn match_path(&self, path: &str) -> Option<Params>;        // exact
    pub fn match_prefix(&self, path: &str) -> Option<(Params, String)>; // prefix
}

#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Params { /* opaque; ordered (name, value) pairs */ }

impl Params {
    pub fn get(&self, name: &str) -> Option<&str>;
    pub fn is_empty(&self) -> bool;
    pub fn len(&self) -> usize;
    pub fn iter(&self) -> impl Iterator<Item = (&str, &str)>;
}
```

Supported pattern syntax: static segments (`/about`) and `:name` single-segment parameters
(`/user/:id`). Trailing slashes are insignificant; `//` collapses.

### Not-found handling

```rust
router.fallback(|_params| text("404 — page not found"))
```

Child routers in a `nest` call carry their own independent fallback.

### Redirect handling

No dedicated redirect route entry. Use programmatic navigation:

```rust
navigate_replace("/login");   // replace — no back to the original page
navigate("/dashboard");       // push — user can press back
```

### Link component

```rust
pub fn link(to: &str, label: &str) -> VNode;

pub struct Link { /* … */ }
impl Link {
    pub fn new(to: &str, label: &str) -> Self;
    pub fn class(self, class: &str) -> Self;
    pub fn build(self) -> VNode;
}

pub const LINK_CLASS: &str = "ferric-router-link";
```

`link` / `Link::build` emit a `<span role="link" tabindex="0" class="ferric-router-link"
data-to="…">` with a click handler calling `navigate`. **Not an `<a href>`** — the `ferric`
click handler is a zero-argument `Fn()` that cannot call `event.preventDefault()`.
Active links additionally carry `aria-current="page"`.

### Router state model

One piece of reactive state: a crate-internal `Signal<String>` holding the current path,
seeded lazily from `window.location.pathname` on first use.

| State | Description |
|---|---|
| **Uninitialized** | Signal is `None` before first use |
| **Active** | Signal holds current path; every `navigate` write re-renders all outlets |

The router has **no loading or error states** — routing is synchronous. Any loading or
error state belongs to async resources mounted inside a route's view.

---

## 4. SSR and Hydration (PR #228)

### `render_to_string` — server rendering (always compiled)

```rust
pub fn render_to_string<F>(f: F) -> String
where
    F: FnOnce() -> VNode,
```

Renders a Ferric component closure to an HTML string. Calls `f` once inside a fresh
`ReactiveScope` that is disposed before returning, so no signal subscriptions leak between
calls.

Output encoding rules:
- Text nodes are wrapped in sentinel comments (`<!--$t-->…<!--/$t-->`) so the hydration
  walk can locate them by index.
- Text content and attribute values are HTML-escaped (`<`, `>`, `&`, `"`, `'`).
- **Event handlers are silently dropped** — not emitted to HTML.
- Void elements (`<br>`, `<input>`, etc.) are emitted as self-closing tags.

### Sentinel constants (shared between SSR and hydration)

```rust
/// Opens a text-boundary region around a VNode::Text node.
pub const TEXT_OPEN_MARKER: &str = "<!--$t-->";

/// Closes a text-boundary region.
pub const TEXT_CLOSE_MARKER: &str = "<!--/$t-->";
```

Both `ssr.rs` and `hydrate.rs` use these same constants; `hydrate.rs` imports them from
`crate::ssr`. Changing them is a breaking change to the SSR + hydration contract.

### `hydrate` — client-side hydration (wasm32-only)

```rust
#[cfg(target_arch = "wasm32")]
pub fn hydrate<F>(root: web_sys::Element, f: F)
where
    F: Fn() -> VNode + 'static,
```

Adopts an existing server-rendered DOM subtree without structural mutations, wires event
handlers, then installs a reactive effect for subsequent signal-driven updates.

Three-phase protocol:
1. **Adopt pass** — walk DOM against VNode tree; skip sentinel comment nodes; wire events;
   recover mismatches by client-rendering the diverged subtree.
2. **Sentinel cleanup** — remove all sentinel comment nodes so DOM child indices align with
   VNode path indices for subsequent diff/patch.
3. **Reactive effect** — subsequent updates go through the standard `vdom::diff` + patch
   path, identical to `dom::mount`.

Mismatch warnings are emitted via `console.warn` in **debug builds only**. Release builds
recover silently.

### Axum integration (in `chirp-server`, not in `ferric`)

```rust
// crates/chirp-server/src/ssr.rs

/// Wraps server-rendered markup in a full HTML document shell.
pub fn assemble_document(server_html: &str, wasm_script_path: &str) -> String;

/// GET / handler — renders the app root and returns an HTML Response.
pub async fn ssr_handler() -> Response;
```

`ferric` itself provides no Axum-specific types. The integration pattern is a plain call
from an async Axum handler:

```rust
// Server side
pub async fn ssr_handler() -> Response {
    let server_html = ferric::render_to_string(|| {
        ferric::VElement::new("div")
            .attr("id", "ferric-root")
            .child(ferric::vdom::text("Loading\u{2026}"))
            .into()
    });
    let doc = assemble_document(&server_html, "/pkg/chirp.js");
    (StatusCode::OK, [(header::CONTENT_TYPE, "text/html; charset=utf-8")], doc)
        .into_response()
}

// Client side — WASM entry point
#[wasm_bindgen(start)]
pub fn main() {
    let root = web_sys::window().unwrap()
        .document().unwrap()
        .get_element_by_id("app").unwrap();

    // `app_root` MUST produce the same VNode tree as was passed to render_to_string.
    let app_root = move || -> ferric::VNode { /* same closure */ };
    ferric::hydrate(root, app_root);
}
```

### SSR state model

SSR + hydration is **stateless across the server/client boundary** as of PR #228 (no
pre-fetched data serialization; deferred to BAR-005 tracked as #225).

| Phase | Description |
|---|---|
| **Rendering** (server) | `render_to_string` runs the closure once in a scoped reactive environment |
| **Done** (server) | Scope disposed; HTML string returned; no server-side state survives |
| **Adopt** (client) | DOM examined, event handlers wired, sentinels removed |
| **Live** (client) | Reactive effect fires on signal changes; standard diff/patch updates the DOM |

---

## 5. Component Pattern

This section synthesizes the async resource and router APIs into a concrete, idiomatic
Ferric component that handles all observable states.

### Pattern: data-fetching component with four states

Requirements:
- Triggers an async fetch on mount
- Shows a loading indicator while pending
- Shows an error state with a Retry button on failure
- Shows content when resolved
- Shows an empty-list state when the response is empty

```rust
use ferric::prelude::*;
use ferric::vdom::text;

#[derive(Clone)]
pub struct Post {
    pub id:    u64,
    pub title: String,
}

/// Application-defined data fetcher.
async fn fetch_posts() -> Result<Vec<Post>, String> {
    // … HTTP call …
    Ok(vec![])
}

/// A post-list component covering all four states.
///
/// Design notes:
///   • `create_resource` with T = Result<Vec<Post>, String> gives both reactive
///     re-fetch (via the `refresh` counter signal) and error propagation through
///     the Ready(Err(…)) arm.
///   • `Signal` is Copy, so `refresh` can be captured by multiple closures.
///   • `suspense` shows the fallback while posts is in the initial Loading state.
///     The inner Loading arm handles mid-session re-fetches (after the user clicks
///     Retry and the resource briefly returns to Loading while already mounted).
pub fn post_list_view() -> VNode {
    // A counter signal; incrementing it triggers a re-fetch via create_resource.
    let refresh = create_signal(0_u32);

    let posts: Resource<Result<Vec<Post>, String>> = create_resource(
        move || refresh.get(),   // source — read is tracked; any change re-fetches
        |_gen| async move { fetch_posts().await },
    );

    // Signal is Copy; capture by-value in both closures is safe.
    let on_retry = move || refresh.set(refresh.get() + 1);

    suspense(
        // Loading fallback — shown during the initial fetch.
        || VElement::new("p")
               .attr("class", "loading")
               .child(text("Loading posts…"))
               .into(),

        // Children — rendered once the resource is Ready or Failed.
        move || match posts.state() {
            // Loading: suspense shows the fallback on first mount.
            // This arm is reached on a retry re-fetch while already rendered.
            ResourceState::Loading => VElement::new("p")
                .child(text("Refreshing…"))
                .into(),

            // create_resource does not produce Failed; handled defensively.
            ResourceState::Failed(msg) => VElement::new("p")
                .child(text(format!("Unexpected resource failure: {msg}")))
                .into(),

            // Network / API error — show the message and offer a Retry button.
            ResourceState::Ready(Err(msg)) => VElement::new("div")
                .attr("class", "error-panel")
                .child(
                    VElement::new("p")
                        .child(text(format!("Failed to load posts: {msg}")))
                        .into(),
                )
                .child(
                    VElement::new("button")
                        .on(EventKind::Click, on_retry)
                        .child(text("Retry"))
                        .into(),
                )
                .into(),

            // Server returned an empty list.
            ResourceState::Ready(Ok(items)) if items.is_empty() => VElement::new("p")
                .attr("class", "empty-state")
                .child(text("No posts yet — check back soon."))
                .into(),

            // Populated list — render one <li> per post.
            ResourceState::Ready(Ok(items)) => {
                let mut list = VElement::new("ul").attr("class", "post-list");
                for post in &items {
                    list = list.child(
                        VElement::new("li")
                            .child(text(post.title.clone()))
                            .into(),
                    );
                }
                list.into()
            }
        },
    )
}
```

### Pattern notes

| Concern | Mechanism |
|---|---|
| Initial fetch | `create_resource` runs the fetcher on first subscription (mount) |
| Re-fetch on demand | Increment the `refresh` signal; `create_resource` source changes → re-fetch |
| Loading indicator | `suspense` fallback for first load; inner `Loading` arm for re-fetch |
| Error + retry | `Ready(Err(msg))` arm; `on_retry` closure increments `refresh` |
| Empty list | Guard pattern `Ready(Ok(items)) if items.is_empty()` |
| Event handling | `VElement::on(EventKind::Click, closure)` — zero-argument `Fn()` |
| Reactive subscription | `resource.state()` inside the `suspense` children closure is auto-tracked |

**SSR behavior**: this component renders in its initial state when passed to
`render_to_string`. Async resources resolve to `Loading` on the server (no pre-fetched data
serialization yet — see Section 6). The suspense fallback HTML will be what the server
emits; the client re-fetches after hydration.

---

## 6. Gaps and Limitations

### No pre-fetched data serialization across the SSR boundary

`render_to_string` runs `Resource` calls in their initial `Loading` state; there is no
mechanism to serialize resolved resource data into the HTML and re-use it on the client.
The client will always re-fetch after hydration. This is explicitly deferred to BAR-005
(tracked as issue #225); a placeholder comment in `assemble_document`'s output marks the
intended `<script type="application/json" id="__state">` location.

**Workaround**: the frontend must show a loading indicator after hydration while resources
re-fetch. Design UX to expect a brief re-fetch on page load.

### `FnOnce` vs. `Fn` closure constraint mismatch

`render_to_string` takes `FnOnce() -> VNode` (server); `hydrate` takes `Fn() -> VNode + 'static`
(client). The same closure cannot be passed to both directly:

```rust
// This does NOT compile — Fn() does not satisfy FnOnce() uniquely, and
// the type expected differs between render_to_string and hydrate.
let app = || VElement::new("div").into();

// Application must call both sides explicitly:
let server_html = ferric::render_to_string(|| app());   // FnOnce wrapper
ferric::hydrate(root, app);                             // Fn() + 'static
```

The convention is to define the component as a `Fn() -> VNode` and call it in a
`FnOnce`-compatible wrapper on the server.

### Event handlers silently absent in SSR output

Event handlers on `VNode::Element` are silently dropped by `render_to_string`. There is no
compile-time or runtime warning. All interactivity requires the client `hydrate` call;
server-rendered HTML is completely inert until the WASM bundle loads and runs.

**Impact**: a UI that shows interactive elements (buttons, forms) will appear functional but
be unresponsive between initial HTML render and WASM hydration. Use CSS or placeholder
attributes to signal "not yet interactive" if that window is long.

### Hydration mismatch recovery is debug-only

`hydrate` emits `console.warn` on mismatch only under `#[cfg(debug_assertions)]`. Release
builds silently recover by client-rendering the diverged subtree. This makes production
mismatch bugs invisible in observability tooling.

### No `<a href>` link (router)

`ferric-router`'s `link` / `Link` helpers emit a `<span>` with a click handler rather than
an `<a href="…">`. This affects:
- Right-click → open in new tab
- Link hover showing destination URL in the browser status bar
- SEO crawlers following `href` attributes
- Keyboard navigation conventions for links

**Workaround**: none within the current API. Custom `<a>` elements with programmatic
`navigate()` calls are the alternative; they require calling `event.preventDefault()`, which
is not supported by the zero-argument click handler.

### No wildcard / catch-all route segments

`RoutePattern` supports only static segments and `:name` single-segment parameters. There
is no `*` or `**` glob for matching multiple trailing segments.

### No URL query string or fragment handling

The router operates on the path portion only. `?key=value` and `#section` are not extracted
by `RoutePattern` or `Params`; callers must parse `window.location.search` / `.hash`
directly.

### No SSR-aware route renderer

`ferric-router` does not export a server-side route resolver. Server-rendering a specific
route requires the caller to resolve the route manually and pass the resulting `VNode` to
`ferric::render_to_string`. There is no helper for this.

### `suspense` is not SSR-aware

The `suspense` thread-local counters (`SUSPENSE_DEPTH`, `SUSPENSE_HAS_LOADING`) are
WASM-runtime primitives. SSR integration may require separate handling; `suspense` boundaries
are not honored by `render_to_string`.

### No `use_resource` ergonomic shorthand

There is no single-call `use_resource(cx, || async { … })` wrapper. Callers manage the
`Resource` handle explicitly via `Resource::new` / `Resource::new_fallible` /
`create_resource`.

### `new_fallible` accepts only `Result<T, String>`

Arbitrary error types must be pre-converted with `.map_err(|e| e.to_string())` before
passing to `Resource::new_fallible`.

### No streaming SSR

`render_to_string` is synchronous and collects the entire output into a `String`. Streaming
/ chunked HTML delivery is not supported.
