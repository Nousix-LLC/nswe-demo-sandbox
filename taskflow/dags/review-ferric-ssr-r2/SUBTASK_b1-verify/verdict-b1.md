# B1 Verdict — REQ-HYD-003: hydrate() wiring

## Verdict: PASS

---

## Finding

Commits inspected: `7fb90c7`, `75c1eef` on branch `work/ferric-ssr-r1`, PR #228.
All file citations are at `75c1eef` (the final state of the branch at review).

---

### 1. Conditional dispatch

**File**: `crates/chirp-frontend/src/app.rs`, `start()` function.

```rust
#[cfg(target_arch = "wasm32")]
if root.has_child_nodes() {
    ferric::hydrate(root, app);
} else {
    mount(root, app);
}
#[cfg(not(target_arch = "wasm32"))]
mount(root, app);
```

`start()` checks whether the mount root has children before choosing a path. The SSR
path calls `ferric::hydrate(root, app)`; the client-only path calls `mount(root, app)`.
The logic is correct and the two arms are mutually exclusive.

**PASS** — `hydrate()` is dispatched on the SSR-populated-root path; `mount()` on the
empty-root path.

---

### 2. cfg-gate correctness

`ferric::hydrate` is a wasm32-only export. `crates/ferric/src/hydrate.rs` opens with
`#![cfg(target_arch = "wasm32")]`, and `crates/ferric/src/lib.rs` re-exports it under
`#[cfg(target_arch = "wasm32")] pub use crate::hydrate::hydrate`. Calling it from code
that is not gated would be a compile error on non-wasm targets.

The gate in `app.rs` — `#[cfg(target_arch = "wasm32")]` on the whole `if/else` block —
excludes that call from non-wasm compilation. The separate
`#[cfg(not(target_arch = "wasm32"))] mount(root, app)` provides the native fallback.
Clippy and native-test builds see only the mount call; wasm builds see both arms and
select at runtime.

One syntactic note: `#[cfg(...)]` on an `if` expression covers both the `if` body and
its `else` clause as a single statement in Rust. The `else { mount(...) }` arm is part
of the same expression and is excluded along with the `if` body when the cfg does not
match. This is correct.

**PASS** — cfg gating is applied at the right granularity; non-wasm compilation is
clean; native fallback is present.

---

### 3. Hydrate function wiring

Call site in `app.rs`: `ferric::hydrate(root, app)`.

Signature in `crates/ferric/src/hydrate.rs`:
```rust
pub fn hydrate<F>(root: web_sys::Element, f: F)
where
    F: Fn() -> VNode + 'static,
```

`root` is obtained via:
```rust
document
    .get_element_by_id("app")
    .or_else(|| document.body().map(Into::into))
    .expect("…")
```

`get_element_by_id` returns `Option<web_sys::Element>`. `body()` returns
`Option<HtmlBodyElement>`, and `Into<Element>` is implemented for `HtmlBodyElement`, so
`.map(Into::into)` yields `Option<web_sys::Element>`. The `root` binding is
`web_sys::Element` in both cases — matching the first parameter.

`app` is defined as `let app = move || -> VNode { ... }`, satisfying `Fn() -> VNode`.
The `move` captures ensure the closure owns its captured values, satisfying `'static`.

**PASS** — argument types and lifetime bound match the signature exactly.

---

### 4. Children check logic

`root.has_child_nodes()` calls `Node.hasChildNodes()` from the DOM API
(`web_sys::Element` derefs to `web_sys::Node`). It returns `true` when the node has at
least one child node of any kind (element, text, comment).

The SSR path that produces the content is `crates/chirp-server/src/ssr.rs`,
`assemble_document`:
```rust
<div id="app">{server_html}</div>
```

`server_html` is non-empty markup produced by `ferric::render_to_string`. It is
interpolated directly after the opening `>` tag, so the `#app` element has element
children when SSR ran. `has_child_nodes()` returns `true`. The hydration branch fires.

A page served without SSR has an empty `#app` (no children from the server).
`has_child_nodes()` returns `false`. The mount branch fires.

**False-positive risk**: a third-party script injecting content into `#app` before
the WASM module initializes would trigger the hydration path without real SSR markup.
This is outside the deployment model (the page is served by chirp-server and no
other scripts write to `#app`). It is not a concern under normal operation.

**False-negative risk**: none. `render_to_string` always produces at least one element
node; an empty string from it would still place `server_html` inside `#app`, which the
browser would parse as a text node — triggering `has_child_nodes()`.

**PASS** — the condition is correct for the SSR case and the client-only case; no
plausible false-negative; edge-case false-positive is outside the deployment model.

---

### 5. End-to-end wiring

The chain:

1. **Server render**: `ssr_handler()` in `crates/chirp-server/src/ssr.rs` calls
   `ferric::render_to_string(|| { VElement("div")… })` and passes the result to
   `assemble_document(server_html, "/pkg/chirp.js")`.

2. **HTML delivery**: `assemble_document` returns a full HTML document with
   `<div id="app">{server_html}</div>` and a `<script type="module" src="/pkg/chirp.js">`.
   The response is served as `text/html; charset=utf-8`.

3. **Browser parse**: The browser parses the document. `#app` contains the server-rendered
   markup as DOM children before any script runs.

4. **WASM initialization**: The module script loads and calls `start()`.

5. **Root acquisition**: `document.get_element_by_id("app")` returns the already-populated
   `#app` element.

6. **Dispatch**: `root.has_child_nodes()` is `true`; `ferric::hydrate(root, app)` is called.

The chain is complete. `hydrate()` is reachable from a server-rendered page load with no
gaps in control flow.

**Observation (out of scope for REQ-HYD-003)**: `ssr_handler` renders a placeholder
component (`div#ferric-root > text("Loading…")`), while `start()`'s `app` closure is
the full application (nav bar + router outlet). The VNode trees will not match on first
hydration pass. The `hydrate` module handles this via mismatch recovery (REQ-SSR-009:
`console.warn` in debug builds, client-render recovery for mismatched subtrees), so
there is no crash or silent corruption, but zero-structural-mutation on first render
(REQ-SSR-004) will not hold. This is a fidelity issue between the SSR component and
the hydration component, separate from the wiring requirement. It is noted here for
completeness; whether it falls within the already-filed issues (#229–#242) is left to
the parent review node.

**PASS** — the SSR+hydration path is wired end-to-end; `hydrate()` is reachable and
called on a server-rendered page load.

---

### 6. Mount fallback

Two mount fallback paths:

- **WASM, no SSR content** (`else` arm inside `#[cfg(target_arch = "wasm32")]`):
  `mount(root, app)` — called when `#app` is empty. Correct.

- **Non-WASM targets** (`#[cfg(not(target_arch = "wasm32"))] mount(root, app)`):
  Called unconditionally on native. Correct — native builds have no DOM to hydrate.

Both arms reach the same `mount` import that existed before this fix, so no regression
to the client-only mount path.

**PASS** — both fallback paths are correct and cover their respective targets without
overlap.

---

## What Was Clean

The fix is narrow and correct. It adds exactly one runtime branch and one cfg split,
with no changes to the `hydrate` or `mount` implementations themselves. The
`web_sys::Element::has_child_nodes()` condition is the right discriminant for the
SSR-vs-client-only decision in this deployment model. The cfg-gate pattern matches
the convention already used in `ferric/src/lib.rs` for the hydrate module. Type
alignment between the call site and the `hydrate` signature was verified directly.
The end-to-end chain from `ssr_handler` to `hydrate()` is traceable without gaps.

REQ-HYD-003 is resolved.
