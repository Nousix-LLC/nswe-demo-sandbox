# B1 Verdict — REQ-HYD-003: `hydrate()` wiring in `app.rs`

---

## Verdict

**RESOLVED**

`hydrate()` is now called from the WASM entry point when the root already has server-rendered children. The conditional dispatch is functionally correct, the `cfg` gate is correctly scoped and covers the right targets, the function called is the genuine hydration path, and the code satisfies REQ-HYD-003 literally and completely. No residual gap found.

---

## Requirements Covered

`REQ-HYD-003`

---

## Evidence

**Files read:**

| Source | Commit / ref | What was verified |
|--------|-------------|-------------------|
| `crates/chirp-frontend/src/app.rs` | `75c1eef776953993ddd62dba1436845a0d53a281` | Conditional dispatch logic, cfg gates |
| `crates/ferric/src/lib.rs` | `work/ferric-ssr-r1` HEAD (== `75c1eef`) | `hydrate` re-export, module gating |
| `crates/ferric/src/hydrate.rs` | `work/ferric-ssr-r1` HEAD | `hydrate` function signature and behavior |
| GitHub issue #224 | — | REQ-HYD-003 requirement text |
| PR #228 commit log | — | Commit scope and changelog |

**Key code block** (`app.rs`, end of `start()`; commit `75c1eef`):

```rust
// Hydrate when the server has already populated the mount root with SSR markup; fall back
// to a fresh client-side mount when there is no server-rendered content in the root.
// `ferric::hydrate` is wasm32-only; the cfg gate keeps non-wasm (native test / clippy)
// compilation clean while preserving the runtime conditional on the wasm32 target.
#[cfg(target_arch = "wasm32")]
if root.has_child_nodes() {
    ferric::hydrate(root, app);
} else {
    mount(root, app);
}
#[cfg(not(target_arch = "wasm32"))]
mount(root, app);
```

**`ferric::hydrate` signature** (`crates/ferric/src/hydrate.rs`, commit `75c1eef`):

```rust
pub fn hydrate<F>(root: web_sys::Element, f: F)
where
    F: Fn() -> VNode + 'static,
```

**`ferric::hydrate` re-export** (`crates/ferric/src/lib.rs`, commit `75c1eef`):

```rust
#[cfg(target_arch = "wasm32")]
pub use crate::hydrate::hydrate;
```

The module declaration itself is similarly gated:

```rust
#[cfg(target_arch = "wasm32")]
pub mod hydrate;
```

---

## Findings

No findings.

---

## What Was Examined and Found Clean

**1. Conditional dispatch logic — clean**

`root.has_child_nodes()` returns `true` when the root element has any child nodes — elements, text nodes, or comment nodes (including the SSR sentinel comments `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`). For a page served with SSR markup, the root contains the rendered HTML and sentinel comments, so `has_child_nodes()` correctly returns `true`, routing to `ferric::hydrate`. For a fresh client-only page, the `<div id="app">` is empty (the `assemble_document` helper inserts `server_html` directly with no surrounding whitespace), so `has_child_nodes()` correctly returns `false`, routing to `mount`. The two paths are semantically correct and mutually exclusive.

**2. `cfg(target_arch = "wasm32")` gate — correctly scoped**

`ferric::hydrate` is a wasm32-only symbol: `crates/ferric/src/lib.rs` re-exports it only under `#[cfg(target_arch = "wasm32")]`, and the hydrate module itself begins with `#![cfg(target_arch = "wasm32")]`. Without the gate in `app.rs`, native `cargo test --workspace` and `cargo clippy --all-targets` would fail with E0425 (unresolved name) — the commit message for `75c1eef` confirms this was exactly the CI failure that commit fixed. The gate is correctly scoped to the if-else block; the `#[cfg(not(target_arch = "wasm32"))]` fallback preserves a valid code path for all non-WASM targets. The gate is not over-broad: it covers only the two lines that differ by target, not any surrounding logic.

**3. Function identity — correct hydration path**

`ferric::hydrate(root, app)` calls `crates/ferric/src/hydrate.rs::hydrate`, which performs the full three-phase hydration: (1) adopt walk — walks the existing DOM against the VNode tree, skipping sentinel comment nodes, wiring event handlers (REQ-SSR-005); (2) sentinel cleanup — removes `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` comment nodes after the walk; (3) reactive effects — `create_effect` establishes the diff/patch loop for subsequent signal-driven re-renders. This is the right function: not a stub, not `mount`, and not any intermediary — the same function covered by `hydrate_wasm.rs` test coverage.

**4. End-to-end boot path — no residual gap**

Prior to commit `7fb90c7`, `start()` called `ferric::dom::mount(root, app)` unconditionally, bypassing hydration entirely. After `7fb90c7` and `75c1eef`, the boot path with an SSR-rendered root is: `start()` → `root.has_child_nodes()` → `true` → `ferric::hydrate(root, app)` → adopt-walk, event wiring, reactive loop. There is no code path on the WASM target where `mount` is called on an SSR-rendered root; the conditional has no early-exit or fallback that could bypass it.

**5. Security surface (DOM injection before WASM boot) — no vulnerability**

If a script could inject nodes into `#app` before WASM boots, `has_child_nodes()` would return `true` on a non-SSR page, routing to `ferric::hydrate`. The hydrate function handles mismatch: when the VNode tree does not match the DOM, it emits a `console::warn_1` in debug builds and replaces the mismatched subtree with a client-rendered version (REQ-SSR-009 mismatch recovery). The worst outcome is an extra client-side re-render — not a security breach, not data exposure, not privilege escalation. Reaching this scenario requires XSS in the first place, which is a larger problem. No security finding.

**6. Code comment quality — clean**

The inline comment accurately describes intent ("Hydrate when the server has already populated the mount root with SSR markup; fall back to a fresh client-side mount when there is no server-rendered content in the root") and explains the cfg rationale ("ferric::hydrate is wasm32-only; the cfg gate keeps non-wasm (native test / clippy) compilation clean while preserving the runtime conditional on the wasm32 target"). The explanation is accurate and sufficient for a maintainer reading the code cold.

**7. CI baseline — green at pinned commit**

CI run https://github.com/Nousix-LLC/nswe-demo/actions/runs/42120246308 shows 7 green checks at commit `75c1eef`. This confirms the native compilation path (`cargo check`, `cargo clippy --workspace --all-targets`, `cargo test`) passes with the cfg gates in place, consistent with the analysis above. Treated as one supporting data point, not a substitute for judgment.
