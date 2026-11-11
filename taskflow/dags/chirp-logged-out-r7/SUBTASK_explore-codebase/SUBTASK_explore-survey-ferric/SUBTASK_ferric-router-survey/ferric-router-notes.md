# Ferric Router API Notes (PR #203)

Survey of `crates/ferric-router/` from `Nousix-LLC/nswe-demo` at `main` (commit `cb1ced3`).

---

## Source Locations

- `crates/ferric-router/src/lib.rs` — crate root; module declarations and frozen `prelude` re-exports
- `crates/ferric-router/src/router.rs` — `Router` struct, route declaration, outlet, `navigate`, `navigate_replace`, `current_path`, History API integration, nested routes
- `crates/ferric-router/src/matcher.rs` — `RoutePattern` (compiled pattern), `Params` (extracted named parameters), `match_path`, `match_prefix`
- `crates/ferric-router/src/link.rs` — `link` helper function and `Link` builder struct; declarative in-app navigation node

---

## Public API

### Frozen prelude surface (`use ferric_router::prelude::*`)

```rust
// From crates/ferric-router/src/lib.rs
pub mod prelude {
    pub use crate::link::link;
    pub use crate::matcher::{Params, RoutePattern};
    pub use crate::router::{current_path, navigate, navigate_replace, Router};
}
```

### Router type and initialization

```rust
// crates/ferric-router/src/router.rs

pub struct Router {
    routes:   Vec<(RoutePattern, ViewFn)>,
    nested:   Vec<(RoutePattern, LayoutFn, Router)>,
    fallback: Option<ViewFn>,
}

impl Router {
    pub fn new() -> Self { ... }
}

impl Default for Router {
    fn default() -> Self { Self::new() }
}
```

`Router` is a pure builder — it holds no browser state at construction time. The reactive current-path `Signal<String>` is a thread-local that is seeded lazily (on first `navigate`, `current_path`, or `outlet` / `mount_history` call) outside any reactive effect so it lives for the full application lifetime.

### Route declaration — builder API

```rust
// crates/ferric-router/src/router.rs

// Flat route: exact segment match
pub fn route(
    mut self,
    pattern: &str,
    view: impl Fn(&Params) -> VNode + 'static,
) -> Self { ... }

// No-match (404) fallback; invoked with empty Params
pub fn fallback(
    mut self,
    view: impl Fn(&Params) -> VNode + 'static,
) -> Self { ... }

// Nested route: prefix match + child router
pub fn nest(
    mut self,
    prefix: &str,
    layout: impl Fn(&Params, &dyn Component) -> VNode + 'static,
    child_builder: impl FnOnce(Router) -> Router,
) -> Self { ... }
```

Routes are resolved **first-match-wins** in declaration order. Register more specific patterns before more general ones. Nested routes (prefix matching) are tried before flat routes.

### Outlet — consuming the builder into a component

```rust
// crates/ferric-router/src/router.rs

// Consumes the router and returns a reactive ferric Component.
// Mount with ferric::dom::mount(root_element, router.outlet()).
pub fn outlet(self) -> impl Component + 'static { ... }

// Seed the current path and install the popstate listener (call once at startup).
pub fn mount_history(self) -> Self { ... }
```

### Navigation API

```rust
// crates/ferric-router/src/router.rs

/// Push a new History entry and update the reactive path → all outlets re-render.
pub fn navigate(path: &str) { ... }

/// Replace the current History entry (use for redirects / login flows).
pub fn navigate_replace(path: &str) { ... }

/// Read the current path reactively (subscribes the calling reactive context).
pub fn current_path() -> String { ... }
```

`navigate` / `navigate_replace` wrap `history.pushState` / `history.replaceState` respectively on wasm32; off-wasm they only update the reactive signal (useful for native unit tests). Both notify every mounted outlet immediately.

### Route matching and parameters

```rust
// crates/ferric-router/src/matcher.rs

/// Compiled route pattern. Supports static segments (/about) and :name params (/user/:id).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RoutePattern {
    segments: Vec<Segment>, // internal; opaque to callers
}

impl RoutePattern {
    /// Compile a pattern string.
    pub fn new(pattern: &str) -> Self { ... }

    /// Exact segment match: returns Some(Params) on match, None otherwise.
    pub fn match_path(&self, path: &str) -> Option<Params> { ... }

    /// Prefix match (for nested routes): returns Some((Params, remaining_path)) or None.
    pub fn match_prefix(&self, path: &str) -> Option<(Params, String)> { ... }
}

/// Named path parameters extracted from a matched route.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Params {
    pairs: Vec<(String, String)>, // internal; ordered (name, value) pairs
}

impl Params {
    pub fn get(&self, name: &str) -> Option<&str> { ... }
    pub fn is_empty(&self) -> bool { ... }
    pub fn len(&self) -> usize { ... }
    pub fn iter(&self) -> impl Iterator<Item = (&str, &str)> { ... }
}
```

**Matching semantics**: segments are split on `/` with empty segments discarded (trailing slash insignificant, `//` collapses). Matching is **exact over segments** for flat routes; prefix-based for nested routes. `:name` wildcard binds that segment's value. Percent-encoding is passed through verbatim — no URL-decoding.

### Not-found handling

Registered via `.fallback(view_fn)`. When no route matches, `fallback` is invoked with an empty `Params`. If no fallback is registered, an empty text node is rendered. The fallback is scoped per router level — child routers in a `nest` call carry their own independent fallback.

```rust
router.fallback(|_params| text("404 — page not found"))
```

### Redirect handling

There is no dedicated redirect type or route entry. Redirects are expressed as programmatic navigation using `navigate_replace`:

```rust
// In a component event handler or initialization logic:
navigate_replace("/login"); // replaces the current history entry — no "back" to the original page
```

`navigate_replace` wraps `history.replaceState` on wasm32; `navigate` wraps `history.pushState`. Use `navigate_replace` wherever adding a back-step would be incorrect (login redirects, post-form redirects, etc.).

### Link component

```rust
// crates/ferric-router/src/link.rs

/// Shorthand: returns a navigation VNode for `to` displaying `label`.
pub fn link(to: &str, label: &str) -> VNode { ... }

/// Builder for a navigation link with an overridable CSS class.
pub struct Link {
    to:    String,
    label: String,
    class: String,
}

impl Link {
    pub fn new(to: &str, label: &str) -> Self { ... }
    pub fn class(mut self, class: &str) -> Self { ... }  // overrides default class
    pub fn build(self) -> VNode { ... }
}

/// The CSS class placed on every link element.
pub const LINK_CLASS: &str = "ferric-router-link";
```

`link` / `Link::build` emit a `<span role="link" tabindex="0" class="ferric-router-link" data-to="...">` with a `Click` event handler that calls `navigate`. It is **not** an `<a href>` — the `ferric` click handler is a zero-argument `Fn()` that cannot call `event.preventDefault()`, so a non-anchor element is used to avoid full-page navigation entirely. Active links (where `to == current_path()`) additionally carry `aria-current="page"`.

---

## State Model

The router has **one piece of reactive state**: the current path, held as a crate-internal `Signal<String>` in a thread-local (`CURRENT_PATH: RefCell<Option<Signal<String>>>`).

| State | Description |
|---|---|
| **Uninitialized** | `CURRENT_PATH` is `None` until the first call to `path_signal()` (triggered by `navigate`, `current_path`, `outlet`, or `mount_history`). |
| **Active** | `CURRENT_PATH` is `Some(Signal<String>)` seeded from `window.location.pathname` (wasm32) or `"/"` (native). Every `navigate` / `navigate_replace` write to this signal; every outlet reads it, subscribing to re-render on change. |

The router itself has **no loading or error states** — it is not an async resource. The route view builders receive `&Params` synchronously and return a `VNode` synchronously. Any loading/error state belongs to async resources mounted inside a route's view, not to the router itself.

There is no route-transition lifecycle or cancellation mechanism: navigation is instantaneous at the signal level, and the DOM patch follows on the next `ferric` render effect run.

---

## Usage Example

```rust
use ferric::prelude::*;
use ferric_router::prelude::*;
use ferric::vdom::text;

fn main() {
    // Build the router, seed from window.location, install popstate listener.
    let app = Router::new()
        .route("/", |_params| {
            // Home page — a nav bar plus content
            VElement::new("div")
                .child(link("/", "Home"))
                .child(link("/user/42", "Profile"))
                .child(text("Welcome"))
                .into()
        })
        .route("/user/:id", |params| {
            let id = params.get("id").unwrap_or("unknown");
            text(format!("User: {id}"))
        })
        .nest(
            "/settings",
            |_params, child| {
                VElement::new("div")
                    .child(link("/settings/profile", "Profile Settings"))
                    .child(child.render())
                    .into()
            },
            |child_router| {
                child_router
                    .route("/", |_| text("Settings index"))
                    .route("/profile", |_| text("Profile settings"))
                    .fallback(|_| text("Settings page not found"))
            },
        )
        .fallback(|_params| text("404 — page not found"))
        .mount_history();

    let body = web_sys::window()
        .unwrap()
        .document()
        .unwrap()
        .body()
        .unwrap();
    mount(body.into(), app.outlet());
}

// Programmatic navigation (e.g. after form submit):
fn after_login() {
    navigate_replace("/dashboard"); // redirect — no back to login page
}

fn go_to_profile(id: &str) {
    navigate(&format!("/user/{id}")); // push — user can press back
}
```

---

## Notable Limitations

- **No `<a href>` link**: The `link` helper emits a `<span>` because `ferric`'s click handler is zero-argument and cannot call `event.preventDefault()`. This may affect browser behaviors that rely on a real anchor (right-click → open in new tab, link hover showing destination URL in the status bar, SEO crawlers following `href`).

- **No wildcard / catch-all segments**: The matcher supports `:name` single-segment parameters and static segments only. There is no `*` or `**` glob for matching multiple segments. Routes with an arbitrary number of segments cannot be expressed as a single pattern.

- **No URL query string or hash handling**: `RoutePattern` and `Params` operate on the path portion only. Query parameters (`?key=value`) and fragments (`#section`) are not extracted by the matcher.

- **No typed route params**: Parameters are always `&str`; callers parse numeric IDs or other typed values themselves.

- **No redirect route entry**: Redirects must be expressed as imperative `navigate_replace` calls; there is no `.redirect("/old", "/new")` builder method.

---

## Integration Notes

- **Signals composition**: The router reuses `ferric::signal::{create_signal, Signal}` and `ferric::component::Component` from the main `ferric` crate. It does **not** re-implement reactivity. The outlet's view builder is a plain `Fn() -> VNode` closure that reads `current_path()`, which makes it a `ferric` reactive render node automatically.

- **Async resources inside routes**: Route view builders are synchronous, but nothing prevents them from calling `use_resource` / `suspense` from `ferric::async_resource` inside the returned `VNode`. The router is unaware of async resource lifecycle; navigation that changes which resource is mounted will cause the old resource to be dropped when the DOM patch removes the outlet's previous subtree.

- **SSR**: `crates/ferric-router` does not currently export an SSR-aware route renderer. Server-side rendering of a specific route would require calling the router's resolution logic outside the WASM target context, which is not part of the frozen public surface at this commit. The main `ferric` crate's `render_to_string` can render any `VNode`, so a caller could resolve a route manually and pass the resulting `VNode` to it, but `ferric-router` provides no helper for this.
