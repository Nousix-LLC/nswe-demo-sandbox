# Task: ferric-router navigation + History API + outlet

## Task Specification
**Slug**: SUBTASK_navigation
**Task Kind**: standard
**Status**: Pending

### Objective
Implement the stateful routing layer in `src/router.rs`: the declarative route table, the reactive
"current path" state, History API integration (`pushState`/`popstate`), programmatic `navigate`, the
reactive `current_path`, and the router-outlet — all composing `ferric` signals (never re-implementing them).

### Context
Part of the `ferric-router` work-item (see `../_GLOBAL.md`, `../contracts/`). Third task in the serial
pipeline: the real `matcher` module now exists — call `RoutePattern`/`Params` directly (no mock). You
replace the body of `src/router.rs` only.

**Dependencies**: `SUBTASK_matcher`. **Dependents**: `SUBTASK_view` (and downstream).

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | context, constraints, the verified ferric event constraint |
| Frozen contract | `../contracts/ferric_router_api.rs` (router module) | exact `Router`/`navigate`/`current_path` signatures to MATCH |
| Real matcher | `checkout/crates/ferric-router/src/matcher.rs` (COMPLETED) | the matching/param API you compose against |
| `ferric` surface | cloned `crates/ferric` (`signal`, `vdom`, `component`, `dom`) + its README | signals/effects/VNode/Component you reuse |
| Shared clone | `<subtree_root>/checkout/` on `work/ferric-router` | the tree you edit + commit in |

## What to do (approach — your design, not a script)
Implement `src/router.rs` to the frozen contract:
- A **reactive current-path state** — the single source of truth for "what path is routed now." Reuse
  `ferric`'s signal runtime (e.g. a crate-internal thread-local `Signal<String>`); do NOT build your
  own reactivity. Reads must subscribe the caller (so outlets re-render); writes must notify.
- `Router` with builder-style `new`/`route`/`fallback`, storing `(RoutePattern, view-builder)` entries.
- `mount_history(self)` — seed the current path from `window.location` and install a `popstate`
  listener (via `web-sys`) that updates the reactive current path on browser back/forward.
- `navigate(path)` — `history.pushState` + update the reactive current path.
- `current_path()` — reactive read of the current path.
- `outlet(self)` — consume the router into a `ferric` `Component` (`Fn() -> VNode`) that, read inside
  `ferric::mount`'s effect, resolves the current path against the route table (first match wins; else
  `fallback`, else a sensible empty node) and returns the matched view's `VNode`, re-rendering when the
  current path changes.
Gate browser-only code so the crate still compiles natively (mirror `ferric::dom`'s pattern — `web-sys`
provides off-wasm stubs). Add any extra `web-sys` features you need to `Cargo.toml` additively. Add a
`#[wasm_bindgen_test]` behind `cfg(all(test, target_arch = "wasm32"))` exercising navigate→current_path
if it fits cleanly (optional per the manifest). Commit on `work/ferric-router`.

## Outputs (you own)
- `checkout/crates/ferric-router/src/router.rs` (final implementation)
- additive `web-sys` feature additions in `Cargo.toml` if needed (note them; do not remove existing ones)
- a commit; `COMPLETE.md` recording the design (esp. the reactive current-path + outlet wiring) + build/test results.

## Success Criteria
- [ ] `Router`, `navigate`, `current_path` match the frozen signatures (compiler-checked); rustdoc on all public items.
- [ ] Route registration + resolution uses the REAL matcher; first-match-wins; fallback on no match.
- [ ] `mount_history` seeds from `location` and reacts to `popstate`; `navigate` does `pushState` + updates the reactive path.
- [ ] `outlet()` returns a `Component` that re-renders on navigation via ferric signals (no bespoke reactivity/DOM).
- [ ] `cargo build --workspace` + `cargo build -p ferric-router --target wasm32-unknown-unknown` succeed; `cargo test -p ferric-router` passes; fmt/clippy clean for this module.

## Constraints
- `../contracts/` READ-ONLY; MATCH signatures. Compose with the REAL `matcher`; do not re-define `Params`/`RoutePattern`.
- Compose with `ferric` signals/component/dom — do NOT re-implement reactivity or the DOM diff.
- **ferric event constraint (verified, see hub):** click handlers are `Fn()` with no event arg — this
  shapes the `<Link>` helper (owned by the view spoke); your `navigate` must be callable from such a handler.
- Edit only `src/router.rs` (+ additive Cargo.toml features); NEVER touch `main`; no attribution trailers.

## Suggested Methodology Files (parent's flags — you are the final judge)
Task type: **Writing Rust code** + **Rust async/runtime-adjacent (web-sys FFI)** → primary **Rust**,
supporting **Core**, **Code Quality**.
- `rust` — `rust/Rust_Trait_Design_Methodology.md` (the `impl Fn(&Params)->VNode` view-builder seam &
  `impl Component` return), `rust/Rust_Ownership_Borrowing_Methodology.md` (capturing route builders;
  `'static` closures), `rust/Rust_Error_Handling_Methodology.md` (graceful behavior when no route matches),
  `rust/Rust_Unsafe_FFI_Methodology.md` (web-sys/js-sys boundary — `Closure`, listener lifetime, as ferric's dom.rs does).
- `code-quality` — `code-quality/Framework_SOLID_Principles_Methodology.md`, `code-quality/Framework_Clean_Code_Methodology.md` (a clean, extensible public router API).
- `core` — `core/BestPractices_Error_Handling_Methodology.md`.

## Inherited Constraints
Compose with `ferric` (do not re-implement); lean deps; edition 2021/stable; rustdoc required; browser
code gated so the crate stays natively compilable.

## Out-of-Scope Methodologies
Do NOT load `decomposition`/`synthesis`. Do NOT re-implement signal/effect machinery — reuse ferric's.
