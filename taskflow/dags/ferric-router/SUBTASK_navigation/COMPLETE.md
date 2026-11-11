# COMPLETE — SUBTASK_navigation (ferric-router navigation + History API + outlet)

**Task**: Implement the stateful routing layer in `src/router.rs` to the frozen contract.
**Status**: COMPLETE
**Commit**: `b87b83a` on `work/ferric-router` ("Implement ferric-router navigation layer (Router, History API, reactive outlet)").
**Output file**: `checkout/crates/ferric-router/src/router.rs` (318 lines, no `todo!()` remaining).

> Resume note: this node was dispatched as a reconstructed resume. A prior invocation had
> authored and committed `src/router.rs` (HEAD `b87b83a`, clean working tree) but never published a
> terminal lifecycle event, so the node was reconstructed RUNNING and re-dispatched. This invocation
> verified the committed implementation against every success criterion and authored this completion
> record; no source change was required (implementation already matches the frozen contract and all
> gates pass), so no new commit was made.

## Design (how it composes `ferric`, never re-implementing it)

### Reactive current-path — the single source of truth
- "What path is routed now" is ONE crate-internal `ferric::signal::Signal<String>` held in a
  `thread_local!` (`CURRENT_PATH`), created lazily by `path_signal()`.
- **Critical lifetime decision**: the signal is always created at *builder time* (inside `outlet()`,
  `mount_history()`, or the first `navigate()`/`current_path()` call) — i.e. *outside* any reactive
  effect. A `ferric` node created while an effect is the active owner would be disposed when that
  effect re-runs; creating it outside any effect makes it a runtime-root node that lives for the whole
  application, so repeated outlet re-renders never dispose the routing state. The `RefCell` borrow is
  never held across `create_signal` (read handle and create-and-store are separate borrows).
- `current_path()` = reactive read (`.get()`) → subscribes the calling reactive context exactly like a
  ferric signal read. `set_current_path()` = `.set()` → notifies every subscribed outlet.

### Route table + resolution (uses the REAL matcher, no mock)
- `Router { routes: Vec<(RoutePattern, ViewFn)>, fallback: Option<ViewFn> }`, where
  `ViewFn = Box<dyn Fn(&Params) -> VNode>`. Builder-style `new`/`route`/`fallback` match the frozen
  signatures. Registration order is preserved; resolution is **first-match-wins** by iterating the
  `Vec` in order and returning the first `pattern.match_path(&path)` that is `Some`.
- Composes `crate::matcher::{Params, RoutePattern}` directly — no re-definition, no mock.

### Outlet wiring (re-renders on navigation via ferric signals)
- `outlet(self) -> impl Component + 'static` forces `path_signal()` into existence at builder time,
  then returns a `move || -> VNode` closure. Inside the closure it does the reactive read
  `current_path()` (subscribing ferric's render effect), resolves first-match-wins against the moved
  route table, and returns the matched view's `VNode`; on no match it invokes `fallback` with
  `Params::default()` (empty params), else returns `text("")` (a sensible empty node). Because the
  read happens inside ferric's render effect, every `navigate()`/`popstate` write re-runs the outlet
  and patches the DOM — the router stores no DOM state of its own.

### History API integration (browser-gated; crate stays natively compilable)
- All browser-only calls are behind `#[cfg(target_arch = "wasm32")]`, mirroring `ferric::dom`:
  - `navigate(path)` → `history.push_state_with_url(&JsValue::NULL, "", Some(path))` then
    `set_current_path`. Off-wasm it skips the History API and only updates the reactive path, so the
    navigation→resolution→view logic is exercisable in native unit tests. Callable from a `ferric`
    click handler (`Fn()` with no event arg) — satisfies the verified ferric event constraint.
  - `mount_history(self)` seeds the signal at builder time, and on wasm sets the path from
    `window.location.pathname` and installs a `popstate` listener (via a `Closure` that is
    `forget`-ed — the router is mounted once for the app lifetime, the same trade-off `ferric::dom`
    documents) that updates the reactive path on browser back/forward.
  - `current_location_path()` has a wasm impl (reads `window.location.pathname`, falls back to `"/"`)
    and a `#[cfg(not(target_arch = "wasm32"))]` stub returning `"/"`.

## Contract conformance
- `Router`, `Router::{new,route,fallback,mount_history,outlet}`, `Default for Router`, `navigate`,
  `current_path` all MATCH the frozen `contracts/ferric_router_api.rs` router-module signatures
  (compiler-checked on both native and wasm targets). Private representation (the thread-local signal,
  the boxed `ViewFn` table) is owner latitude, as the contract permits.
- `contracts/` untouched (read-only). No frozen signature changed.

## Cargo.toml
- No change required this invocation. The crate already declares the `web-sys` features the router
  needs: `Window`, `History`, `Location`, `PopStateEvent`, `Event`, `EventTarget` (additive; no
  existing feature removed).

## Verification (all success criteria — PASS)
- [x] `Router`/`navigate`/`current_path` match frozen signatures (compiler-checked, native + wasm); rustdoc on all public items.
- [x] Resolution uses the REAL matcher; first-match-wins; fallback (empty params) on no match; empty node when no fallback.
- [x] `mount_history` seeds from `location` + installs `popstate`; `navigate` does `pushState` + updates the reactive path.
- [x] `outlet()` returns a `Component` re-rendering on navigation via a ferric signal read (no bespoke reactivity/DOM).
- [x] `cargo build --workspace` — OK.
- [x] `cargo build -p ferric-router --target wasm32-unknown-unknown` — OK.
- [x] `cargo test -p ferric-router` — 23 passed, 0 failed (6 router tests: navigate↔current_path, first-match-wins, fallback-with-empty-params, empty-node-no-fallback, default==new); doc-tests pass (Router example compiles).
- [x] `cargo fmt -p ferric-router -- --check` — clean.
- [x] `cargo clippy -p ferric-router --all-targets -- -D warnings` — clean (verified on a forced clean rebuild).
- [x] Optional `#[wasm_bindgen_test]` present behind `cfg(all(test, target_arch = "wasm32"))` exercising navigate→current_path.

## Constraints honored
- Edited only `src/router.rs`; `contracts/` read-only and signatures matched; composed with `ferric`
  (no re-implemented reactivity/DOM) and the real `matcher` (no re-defined `Params`/`RoutePattern`).
- Work on `work/ferric-router`; `main` untouched; no commit-attribution trailers.

## Handoff to SUBTASK_view
- `src/router.rs` is final and committed. Downstream `SUBTASK_view` can build `src/link.rs` against
  the public `navigate(&str)` (callable from a `Fn()` click handler) and mount `Router::outlet()` via
  `ferric::mount`. The reactive current-path signal is already runtime-root-owned; outlets mounted by
  the example will re-render on `navigate`/`popstate`.
