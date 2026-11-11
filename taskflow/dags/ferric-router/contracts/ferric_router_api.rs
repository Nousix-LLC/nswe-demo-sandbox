// contracts/ferric_router_api.rs — FROZEN public API surface of the `ferric-router` crate.
// Kind: rust_trait. READ-ONLY for every descendant task. This is a REFERENCE artifact, not a
// compiled crate member: implementers MATCH these signatures in crates/ferric-router/src/<module>.rs.
//
// WHAT IS FROZEN (binding): the module layout (`matcher`, `router`, `link`), the set of public items
// named below, their signatures and roles, and the `prelude` re-export surface. These are the
// cross-layer seam between the serial spokes AND the cross-crate surface the example and the future
// `chirp-frontend` work-item will depend on. Changing a frozen public signature requires an ADDITIVE
// plan amendment — not an in-place edit of this file.
//
// WHAT IS LATITUDE (owner's design): every private/internal type and representation — how `Params`
// stores pairs, how `RoutePattern` stores segments, how `Router` stores its route table, the
// thread-local current-path signal machinery, the concrete element `link` emits. Owners may refine
// these freely and MAY ADD public items additively (e.g. a richer `Link` builder, a `Params::iter`)
// without an amendment, so long as nothing frozen below is removed or changed in place.
//
// Dependency crates (declared by scaffold in crates/ferric-router/Cargo.toml): ferric (path),
// wasm-bindgen, js-sys, web-sys (History/Window/Location/PopStateEvent features as needed),
// wasm-bindgen-test (dev). Keep deps lean.
//
// Compose with ferric's frozen surface (do NOT re-implement): ferric::vdom::{VNode, VElement, text,
// EventKind}, ferric::signal::{create_signal, create_effect, Signal}, ferric::component::Component,
// ferric::dom::mount.

use ferric::component::Component;
use ferric::vdom::VNode;

// =====================================================================================
// module: matcher           owner: SUBTASK_matcher          file: src/matcher.rs
// Pure, browser-free route matching: compile a pattern like `/user/:id`, match a concrete path,
// and extract named parameters. Natively testable with no wasm/DOM. This module MUST NOT depend on
// web-sys or any browser API.
// =====================================================================================

/// Named path parameters extracted from a matched route (e.g. pattern `/user/:id` against
/// `/user/42` yields `id = "42"`).
pub struct Params { /* owner-designed: ordered name→value pairs */ }

impl Params {
    /// The value bound to parameter `name`, if the matched pattern declared it.
    pub fn get(&self, name: &str) -> Option<&str> { todo!() }
    /// True when the matched pattern declared no parameters.
    pub fn is_empty(&self) -> bool { todo!() }
    /// The number of bound parameters.
    pub fn len(&self) -> usize { todo!() }
}

/// A compiled route pattern. Supports static segments (`/about`), named params (`/user/:id`), and
/// the root (`/`). Trailing-slash normalization and any wildcard support are owner latitude.
pub struct RoutePattern { /* owner-designed: parsed segments */ }

impl RoutePattern {
    /// Compile a path pattern. `pattern` is a `/`-separated path; a segment beginning `:` is a
    /// named parameter whose name is the remainder.
    pub fn new(pattern: &str) -> Self { todo!() }
    /// Match a concrete `path` against this pattern. Returns `Some(params)` with any extracted
    /// named parameters on a match, `None` otherwise. Matching is exact over segments (a pattern
    /// MUST NOT match a path with extra or missing segments unless the pattern says so).
    pub fn match_path(&self, path: &str) -> Option<Params> { todo!() }
}

// =====================================================================================
// module: router            owner: SUBTASK_navigation       file: src/router.rs
// The stateful routing layer: a declarative route table, the reactive "current path" state, the
// History API integration (pushState/popstate), programmatic navigation, and the reactive outlet.
// Composes ferric signals for reactivity — it MUST NOT re-implement reactivity or the DOM diff.
// A route's view builder is `Fn(&Params) -> VNode`: it receives the matched params and returns a
// ferric view tree.
// =====================================================================================

/// The client-side router: a declarative route table plus History-API navigation, rendered through
/// a reactive outlet that re-renders when the current path changes.
pub struct Router { /* owner-designed: route table + fallback + reactive current-path handle */ }

impl Router {
    /// Create an empty router.
    pub fn new() -> Self { todo!() }
    /// Register a route: `pattern` (see [`RoutePattern::new`]) mapped to a view builder that
    /// receives the matched params and returns a ferric [`VNode`]. Builder-style (returns `self`).
    pub fn route(self, pattern: &str, view: impl Fn(&Params) -> VNode + 'static) -> Self { todo!() }
    /// Register the fallback (no-match / "404") view, invoked with empty params when no route matches.
    pub fn fallback(self, view: impl Fn(&Params) -> VNode + 'static) -> Self { todo!() }
    /// Seed the current path from `window.location` and install the `popstate` listener so browser
    /// back/forward updates the reactive current path. Call once at startup. Builder-style.
    pub fn mount_history(self) -> Self { todo!() }
    /// Consume the router into a [`Component`] (the router-outlet) that renders the view of the
    /// currently-matched route and re-renders reactively whenever the current path changes. Mount
    /// it with `ferric::mount(root, router.outlet())`.
    pub fn outlet(self) -> impl Component + 'static { todo!() }
}

impl Default for Router {
    fn default() -> Self { todo!() }
}

/// Programmatically navigate to `path`: push a new History entry (`pushState`) and update the
/// reactive current path so every mounted outlet re-renders. Safe to call from an event handler.
pub fn navigate(path: &str) { todo!() }

/// Read the current path reactively (subscribes the calling reactive context, like a ferric signal
/// read). Returns the path portion currently routed (e.g. `"/user/42"`).
pub fn current_path() -> String { todo!() }

// =====================================================================================
// module: link              owner: SUBTASK_view             file: src/link.rs
// Declarative navigation helper producing a ferric view node.
//
// NOTE (ferric event constraint): ferric's click handler is `Fn()` with no event argument, so
// `preventDefault()` is NOT reachable. `link` MUST therefore emit an element the browser will not
// full-page-navigate on (e.g. a styled non-anchor element, or an `<a>` without a followed href),
// wired with a click handler that calls [`navigate`]. The exact element/markup is owner latitude.
// =====================================================================================

/// A declarative in-app navigation link: returns a ferric [`VNode`] that, when clicked, calls
/// [`navigate`] to `to` (client-side, no full page reload) and displays `label`. Owners MAY add a
/// richer builder (children, attributes) additively.
pub fn link(to: &str, label: &str) -> VNode { todo!() }

// =====================================================================================
// crate root               owner: SUBTASK_scaffold          file: src/lib.rs
// Module declarations + the frozen prelude re-export surface below. Scaffold authors lib.rs with
// `pub mod matcher; pub mod router; pub mod link;` and this prelude; module bodies are filled by
// their owning spokes.
// =====================================================================================

pub mod prelude {
    pub use crate::link::link;
    pub use crate::matcher::{Params, RoutePattern};
    pub use crate::router::{current_path, navigate, Router};
}
