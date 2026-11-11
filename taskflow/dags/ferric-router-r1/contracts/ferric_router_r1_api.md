# ferric-router r1 — API contract

This document is the composition root for all additive API surfaces the ferric-router-r1 DAG
lands. The synthesis gate verifies every identity below before creating the PR.

---

## Frozen #5 surface (preserved, unchanged)

All items below are carried forward with identical signatures. Any removal or redefinition
is a contract violation.

```rust
// crates/ferric-router/src/matcher.rs
pub struct Params { /* opaque */ }
impl Params {
    pub fn get(&self, name: &str) -> Option<&str>;
    pub fn is_empty(&self) -> bool;
    pub fn len(&self) -> usize;
    pub fn iter(&self) -> impl Iterator<Item = (&str, &str)>;
}
impl Default for Params { ... }

pub struct RoutePattern { /* opaque */ }
impl RoutePattern {
    pub fn new(pattern: &str) -> Self;
    pub fn match_path(&self, path: &str) -> Option<Params>;
}

// crates/ferric-router/src/router.rs
pub struct Router { /* opaque */ }
impl Router {
    pub fn new() -> Self;
    pub fn route(self, pattern: &str, view: impl Fn(&Params) -> VNode + 'static) -> Self;
    pub fn fallback(self, view: impl Fn(&Params) -> VNode + 'static) -> Self;
    pub fn mount_history(self) -> Self;
    pub fn outlet(self) -> impl Component + 'static;
}
impl Default for Router { ... }

pub fn navigate(path: &str);
pub fn current_path() -> String;

// crates/ferric-router/src/link.rs
pub const LINK_CLASS: &str = "ferric-router-link";
pub fn link(to: &str, label: &str) -> VNode;
pub struct Link { /* opaque */ }
impl Link {
    pub fn new(to: &str, label: &str) -> Self;
    pub fn class(self, class: &str) -> Self;
    pub fn build(self) -> VNode;
}

// crates/ferric-router/src/lib.rs
pub mod prelude {
    pub use crate::link::link;
    pub use crate::matcher::{Params, RoutePattern};
    pub use crate::router::{current_path, navigate, Router};
    // navigate_replace added additively by navigate-replace spoke
}
```

---

## Additive additions (r1 — this DAG)

### navigate_replace (REQ-RT-003 — replace navigation)

```rust
// crates/ferric-router/src/router.rs (additive)
/// Programmatically navigate to `path` by replacing the current History entry instead of
/// pushing a new one. Use for redirects after form-submit or wizard steps where the
/// intermediate URL should not be reachable via the back button.
///
/// Off-wasm: only the reactive current-path is updated (History API skipped).
pub fn navigate_replace(path: &str);

// crates/ferric-router/src/lib.rs — prelude addition
pub mod prelude {
    // ... frozen items unchanged ...
    pub use crate::router::navigate_replace;  // additive
}
```

**Behavioral contract:**
- Calls `history.replaceState(null, "", path)` on wasm32 (no history growth)
- Calls `set_current_path(path)` on all targets (reactive update)
- Native tests verify `current_path()` updates after `navigate_replace`
- wasm32 tests (wasm-bindgen-test) verify history length does not grow on replace

### aria-current active-route awareness on Link (REQ-RT-007)

```rust
// crates/ferric-router/src/link.rs (additive behavior in Link::build)
// Frozen signature unchanged:
pub fn link(to: &str, label: &str) -> VNode;  // unchanged
// Link::build() now calls current_path() and conditionally adds aria-current="page"
// when self.to == current_path(). When paths do not match: element is identical to
// the frozen surface (no aria-current attribute, no class change).
```

**Behavioral contract:**
- `Link::build()` calls `crate::router::current_path()` to get the current path
- If `self.to == current_path()`: emitted element has `attr("aria-current", "page")`
- If `self.to != current_path()`: emitted element has NO `aria-current` attribute
- The emitted element in the inactive case is structurally identical to the frozen surface
- When called inside a reactive render closure (the normal nav-bar usage), the render
  subscribes to path changes automatically via the `current_path()` reactive read

### RoutePattern::match_prefix (REQ-RT-005 prerequisite)

```rust
// crates/ferric-router/src/matcher.rs (additive)
impl RoutePattern {
    /// Match the beginning of `path` against this pattern. On success returns
    /// `Some((params, remaining))` where `params` holds any `:name` captures and
    /// `remaining` is the path suffix after the matched prefix segments, normalized
    /// as a `/`-led string (e.g. pattern `/settings` against `/settings/profile`
    /// returns `("", "/profile")`; against `/settings` returns `("", "/")`).
    /// Returns `None` if any pattern segment fails to match.
    pub fn match_prefix(&self, path: &str) -> Option<(Params, String)>;
}
```

**Behavioral contract:**
- Root pattern (zero segments) matches any path; remaining = the full path normalized
- Pattern `/settings` against `/settings/profile` → `Some((Params::default(), "/profile"))`
- Pattern `/settings` against `/settings` → `Some((Params::default(), "/"))`
- Pattern `/user/:id` against `/user/42/edit` → `Some((params{id="42"}, "/edit"))`
- Pattern `/user/:id` against `/user` → `None` (too few segments)
- Pattern `/user/:id` against `/other/42/edit` → `None` (static mismatch)

### Router::nest (REQ-RT-005 — nested routes + nested outlet)

```rust
// crates/ferric-router/src/router.rs (additive)
impl Router {
    /// Register a nested route. When the current path begins with `prefix`, `layout` is
    /// called with the matched params and a reference to the child router's outlet
    /// component. The child outlet renders the matched child route's view (using the
    /// remaining path after the prefix) and carries its own per-level fallback.
    ///
    /// `child_builder` receives a fresh `Router::new()` and returns the configured child
    /// router. Child routes are relative to the prefix (the remaining path is matched).
    ///
    /// Builder-style (returns `self`). Nested routes are tried before flat routes; the
    /// first prefix match wins.
    pub fn nest(
        self,
        prefix: &str,
        layout: impl Fn(&Params, &dyn Component) -> VNode + 'static,
        child_builder: impl FnOnce(Router) -> Router,
    ) -> Self;
}
```

**Behavioral contract:**
- `Router::outlet()` tries nested routes BEFORE flat routes, in registration order
- When a nested route's prefix matches, the child outlet reads `current_path()` and strips
  the prefix to get the remaining path; the child outlet is a `Component` passed to `layout`
- Per-level fallback: the child router's `.fallback()` renders for unmatched child paths;
  the app-root router's `.fallback()` renders for paths that don't match the prefix at all
- Navigating between sibling child routes does not tear down the parent layout (the parent
  outlet re-renders only the child outlet portion)
- The frozen flat `Router::route` / `.outlet()` behavior is the degenerate single-level case
  (unchanged)

---

## Prelude union (post-r1)

```rust
pub mod prelude {
    pub use crate::link::link;
    pub use crate::matcher::{Params, RoutePattern};
    pub use crate::router::{current_path, navigate, navigate_replace, Router};
}
```

The synthesis gate checks this exact set is present and no frozen item is removed.
