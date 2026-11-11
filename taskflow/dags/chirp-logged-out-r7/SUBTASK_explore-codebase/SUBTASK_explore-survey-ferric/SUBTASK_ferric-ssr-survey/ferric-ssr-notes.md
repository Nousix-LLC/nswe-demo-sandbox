# Ferric SSR + Hydration Survey (PR #228)

Survey of the server-side rendering and client-side hydration APIs introduced in PR #228 at
`Nousix-LLC/nswe-demo` `main` (commit `cb1ced3`).

---

## Source Locations

- `crates/ferric/src/ssr.rs` — SSR render function (`render_to_string`), text-boundary sentinel
  constants (`TEXT_OPEN_MARKER`, `TEXT_CLOSE_MARKER`), and the internal HTML-escaping and
  void-element helpers
- `crates/ferric/src/hydrate.rs` — client-side hydration entry point (`hydrate`); wasm32-only
  (`#![cfg(target_arch = "wasm32")]` at the file top)
- `crates/ferric/src/lib.rs` — re-exports: `render_to_string` unconditionally,
  `hydrate` behind `#[cfg(target_arch = "wasm32")]`
- `crates/ferric/Cargo.toml` — no `[features]` section; SSR/hydration are always compiled;
  the native/wasm32 split is by compile-target `cfg`, not Cargo features
- `crates/chirp-server/src/ssr.rs` — application-layer Axum integration: `ssr_handler`
  (the `GET /` Axum handler) and `assemble_document` (HTML document shell helper)

---

## Public API

### `ferric::render_to_string` (always compiled, native + wasm32)

```rust
pub fn render_to_string<F>(f: F) -> String
where
    F: FnOnce() -> VNode,
```

Renders a Ferric component closure to an HTML string. Calls `f` exactly once inside a fresh
`ReactiveScope`. That scope is disposed before the function returns, ensuring no signal
subscriptions from one render leak into subsequent calls or run as effects on the server.

Output encoding:
- Text nodes (`VNode::Text`) are wrapped in `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` comment
  sentinels so the client hydration walk can locate them by index.
- Text content and attribute values are HTML-escaped (`<`, `>`, `&`, `"`, `'`).
- Event handlers on `VNode::Element` are **silently dropped** — not emitted to HTML.
- Void elements (`<br>`, `<input>`, etc.) are emitted as self-closing `<tag ... />`.

### Sentinel constants (shared between SSR and hydration)

```rust
/// Opens a text-boundary region around a VNode::Text node.
pub const TEXT_OPEN_MARKER: &str = "<!--$t-->";

/// Closes a text-boundary region.
pub const TEXT_CLOSE_MARKER: &str = "<!--/$t-->";
```

Both sides of the SSR + hydration boundary (`ssr.rs` and `hydrate.rs`) MUST use these exact
constants; local copies are forbidden by the module contract.

### `ferric::hydrate` (wasm32-only)

```rust
#[cfg(target_arch = "wasm32")]
pub fn hydrate<F>(root: web_sys::Element, f: F)
where
    F: Fn() -> VNode + 'static,
```

Adopts an existing server-rendered DOM subtree rooted at `root` without structural mutations
(assuming the DOM matches the VNode tree), wires event handlers, then installs a reactive
`create_effect` that re-renders and diffs/patches the live DOM whenever a signal changes.

Three-phase protocol:
1. **Adopt pass** — walk DOM against VNode tree; skip `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`
   sentinel Comment nodes; wire events on matching elements; recover mismatches by client-rendering.
2. **Sentinel cleanup** — remove all sentinel Comment nodes so DOM child indices align with VNode
   path indices for subsequent diff/patch passes.
3. **Reactive effect** — subsequent signal-driven re-renders go through the standard `vdom::diff`
   + `apply_patches` path (identical to `dom::mount`).

Mismatch warnings are emitted via `console.warn` in debug builds only.

### Axum integration helpers (in `chirp-server`, not in `ferric`)

```rust
// crates/chirp-server/src/ssr.rs

/// Wraps server-rendered markup in a full HTML document shell.
pub fn assemble_document(server_html: &str, wasm_script_path: &str) -> String;

/// GET / handler — renders the application root component and returns an HTML response.
pub async fn ssr_handler() -> Response;
```

`ferric` itself provides no Axum-specific types or extractors. The integration pattern is a
plain library call from an async Axum handler (see Usage Example).

---

## State Model

SSR + hydration in Ferric is **stateless across the server/client boundary** as of PR #228.

The server call path has two states per request:
- **Rendering** — `render_to_string` runs the component closure once inside a scoped reactive
  environment; all signal state created during the call is local to that scope.
- **Done** — scope disposed; HTML string returned; no server-side mutable state survives.

The client call path after `hydrate` has two operational phases:
- **Adopt (first run)** — DOM is examined and matched against the initial VNode tree; event
  handlers are wired; sentinel comments are removed.
- **Live (subsequent runs)** — reactive effect fires on signal changes; standard diff/patch
  updates the DOM.

There is no serialized/transferred state between server and client in this PR. The
`<script type="application/json" id="__state">` island for pre-fetched async data is deferred
to BAR-005 (tracked as issue #225); a placeholder comment in `assemble_document`'s output marks
its intended location.

---

## Usage Example

### Server side (Axum handler)

```rust
// crates/chirp-server/src/ssr.rs — simplified from the actual implementation

use axum::http::{header, StatusCode};
use axum::response::{IntoResponse, Response};

pub async fn ssr_handler() -> Response {
    // 1. Render the component tree to an HTML string.
    let server_html = ferric::render_to_string(|| {
        ferric::VElement::new("div")
            .attr("id", "ferric-root")
            .child(ferric::vdom::text("Loading\u{2026}"))
            .into()
    });

    // 2. Wrap in a full HTML document shell with the WASM bootstrap script.
    let doc = assemble_document(&server_html, "/pkg/chirp.js");

    // 3. Return with correct Content-Type.
    (
        StatusCode::OK,
        [(header::CONTENT_TYPE, "text/html; charset=utf-8")],
        doc,
    )
        .into_response()
}

// Register the route:
// Router::new().route("/", get(ssr_handler)).with_state(state)
```

### Client side (WASM entry point)

```rust
// In the WASM bundle's entry point (called when the page loads):

use wasm_bindgen::prelude::*;

#[wasm_bindgen(start)]
pub fn main() {
    let document = web_sys::window().unwrap().document().unwrap();
    // Target the same mount point assemble_document embeds the server markup in.
    let root = document.get_element_by_id("app").unwrap();

    // `app_root` must be the same component closure used for `render_to_string` on the server.
    let app_root = move || -> ferric::VNode {
        ferric::VElement::new("div")
            .attr("id", "ferric-root")
            .child(ferric::vdom::text("Loading\u{2026}"))
            .into()
    };

    ferric::hydrate(root, app_root);
}
```

---

## Notable Limitations

- **No pre-fetched data serialization** — async resource data fetched during SSR cannot be
  injected into the HTML and reused by the client on hydration. The client re-fetches. This is
  explicitly deferred to BAR-005 (#225); the placeholder comment in `assemble_document`'s output
  marks where the `<script type="application/json" id="__state">` island will go.
- **`FnOnce` vs `Fn` closure constraint mismatch** — `render_to_string` takes `FnOnce` (server);
  `hydrate` takes `Fn() + 'static` (client). The same closure cannot be passed to both directly;
  the application must define the component as a `Fn` closure and call both with it, or wrap
  accordingly.
- **Event handlers silently absent in SSR output** — there is no compile-time or runtime
  indication that a handler will not be in the server HTML. Developers must know that all
  interactivity requires hydration on the client.
- **Mismatch recovery in debug only** — hydration mismatch warnings (`console.warn`) are gated
  on `#[cfg(debug_assertions)]`. Release builds silently recover without diagnostics.
- **No streaming SSR** — `render_to_string` is synchronous and collects the entire output into a
  `String` before returning. Streaming / chunked HTML delivery is not supported.

---

## Integration Notes

- **`TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` are shared state** — both `ssr.rs` and `hydrate.rs`
  depend on the exact same sentinel literal values. `hydrate.rs` imports them from `crate::ssr`.
  Any change to these constants is a breaking change to the SSR + hydration contract.
- **Same component closure required on both sides** — the `hydrate` adopt pass will mismatch (and
  fall back to client rendering) if the closure passed to `hydrate` on the client does not produce
  the same VNode tree as was passed to `render_to_string` on the server. Signal-driven differences
  are expected only after hydration is complete.
- **No interaction with async resources in this PR** — the async resource API (`async_resource.rs`)
  is not referenced from either `ssr.rs` or `hydrate.rs`. Resources that resolve asynchronously
  will render in their initial `Loading` state on the server and trigger a re-fetch on the client.
- **`ferric::dom::mount` is the fallback** — if `#app` contains no server markup (e.g. static
  `index.html` served without SSR), the WASM bundle calls `dom::mount` instead of `hydrate`. Both
  are valid entry points; `assemble_document`'s script tag and the application entry point must
  choose the right one based on whether server markup is present.
