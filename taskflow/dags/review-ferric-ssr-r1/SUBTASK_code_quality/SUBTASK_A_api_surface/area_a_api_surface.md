# Area A: API Surface and Naming — PR #228

**Status**: FINDING (NON-BLOCKER)

## What Was Checked

The following public items introduced by PR #228 were examined:

**ferric crate (`crates/ferric/src/`)**
- `lib.rs` lines 25–44: new module declarations (`pub mod ssr;`, `#[cfg(target_arch = "wasm32")] pub mod hydrate;`) and their crate-root re-exports (`pub use crate::ssr::render_to_string;`, `#[cfg(target_arch = "wasm32")] pub use crate::hydrate::hydrate;`)
- `ssr.rs`: public surface — constants `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`, and `pub fn render_to_string<F>(f: F) -> String where F: FnOnce() -> VNode`
- `hydrate.rs`: public surface — `pub fn hydrate<F>(root: web_sys::Element, f: F) where F: Fn() -> VNode + 'static`
- Existing module layout (`component`, `dom`, `signal`, `vdom`, `prelude`) compared against the new additions for naming consistency

**chirp-server crate (`crates/chirp-server/src/`)**
- `ssr.rs` line 98: `pub fn assemble_document(server_html: &str, wasm_script_path: &str) -> String`
- `ssr.rs` line 159: `pub async fn ssr_handler() -> Response`

**Naming consistency checks run:**
- Crate root re-export names vs. module names (collision check)
- C-CASE (naming conventions: functions snake_case, constants SCREAMING_SNAKE_CASE)
- C-CONV (closure trait bounds: `FnOnce` vs `Fn` vs `FnMut`)
- C-WORD-ORDER (avoid repeating the module name inside the item name)
- Fit against the existing ferric naming register (`mount`, `create_signal`, `create_effect`, `diff`)
- Placement of new items relative to the frozen `prelude` and existing root re-exports

## Evidence

**Finding 1 — `hydrate` names both a module and a crate-root re-export (naming collision):**

```
crates/ferric/src/lib.rs:31   pub mod hydrate;
crates/ferric/src/lib.rs:42   #[cfg(target_arch = "wasm32")]
crates/ferric/src/lib.rs:43   pub use crate::hydrate::hydrate;
```

The module `ferric::hydrate` (type namespace) and the re-exported function `ferric::hydrate` (value namespace) share a path at the crate root. Rust allows this — modules live in the type namespace, functions in the value namespace — but it creates a discoverable asymmetry: `use ferric::hydrate;` imports the module, not the function. Users who write `use ferric::hydrate;` and then call `hydrate(root, f)` will get a name-resolution error; the function requires either `ferric::hydrate(root, f)` as a path expression or `use ferric::hydrate::hydrate;`. Rustdoc for the `ferric` crate root will list two items named `hydrate` — a module and a free function — with no typographic distinction visible at a glance.

Compare with `render_to_string`, where the module is `ferric::ssr` and the crate-root function is `ferric::render_to_string`. The names are distinct; there is no collision.

**Finding 2 — `ssr_handler` stutters the module name:**

```
crates/chirp-server/src/ssr.rs:159   pub async fn ssr_handler() -> Response {
```

The function lives in `chirp_server::ssr`; its name repeats `ssr`. The fully qualified path is `chirp_server::ssr::ssr_handler`. Rust API Guideline C-WORD-ORDER encodes the convention that a module's name is not repeated inside its items (the canonical failure example from the guidelines: `std::io::IoError` vs the actual `std::io::Error`). The idiomatic name here is `chirp_server::ssr::handler`.

## Finding

**Finding 1** (NON-BLOCKER): `ferric::hydrate` names both a module and a function at the crate root. The two items resolve in different namespaces, so the crate compiles. The practical harm is to first-time users: `use ferric::hydrate;` does not bring the function into scope (it brings the module), which is the opposite of what `use ferric::render_to_string;` does for the SSR path. The asymmetry between the two new entry points is internally consistent — `render_to_string` avoids the collision because its module is named `ssr`, not `render_to_string` — but it means the hydration entry point requires a non-obvious `use` spelling.

Satisfying resolution: rename the module from `hydrate` to `hydration` (or `client`), so the crate-root function is `ferric::hydrate` and the module is `ferric::hydration`. The function's canonical path becomes `ferric::hydration::hydrate`. Alternatively, do not re-export `hydrate` at the crate root; keep it at `ferric::hydrate::hydrate` and document the full path. Either choice removes the collision. Because `ferric` is at `0.x` this is a freely-revisable surface, but correcting it now costs little.

**Finding 2** (NON-BLOCKER): `chirp_server::ssr::ssr_handler` stutters the module name. The idiomatic name under the existing module is `handler`. Because this handler is currently wired into the router directly (`use crate::ssr::ssr_handler;` in `crates/chirp-server/src/api/router.rs`) and no external callers exist yet, the rename is cheap now and costs at least a grep-and-replace once more consumers arrive. Neither finding blocks merge; both are worth a cleanup issue before the surface stabilises.

**What was clean:**
- Function names `render_to_string` and `hydrate`: clear, idiomatic, well-established in this problem space.
- Module names `ferric::ssr` and `ferric::hydrate`: accurately describe contents; `ssr` correctly signals the server-only compile target.
- Constants `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`: correctly named in SCREAMING_SNAKE_CASE; public rather than pub(crate) because they form a cross-crate protocol boundary between the ferric and chirp-server crates, and that rationale is stated in the doc comments.
- Closure bounds: `FnOnce` for `render_to_string` (the closure is called exactly once inside a reactive scope) vs `Fn + 'static` for `hydrate` (the closure is stored and called on every reactive re-render). Both bounds are as permissive as the implementation allows, satisfying C-CONV.
- `assemble_document` and its parameters (`server_html`, `wasm_script_path`): unambiguous names, clearly scoped to their crate (`chirp_server::ssr`), no stuttering.
- New exports excluded from the frozen `prelude`: correct — `render_to_string` is a server-side entry point and `hydrate` is wasm32-only; neither belongs in the universal component prelude.
- Module placement under `crates/ferric/src/`: `ssr.rs` and `hydrate.rs` fit the existing flat-module structure alongside `component.rs`, `dom.rs`, `signal.rs`, `vdom.rs`.
