# Area B: Abstraction Boundaries — PR #228

**Status**: FINDING (NON-BLOCKER)

## What Was Checked

**SSR module (`crates/ferric/src/ssr.rs`, new)**
Reviewed all imports and the full module body. `ssr.rs` imports only `crate::vdom::VNode`; it carries no reference to `web_sys`, `wasm_bindgen`, or `js-sys`. `render_to_string` calls `crate::signal::ReactiveScope::new()` and `scope.run(f)` — both pure-Rust signal primitives. The `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` sentinel constants are defined here and re-used by `hydrate.rs` via `use crate::ssr::{...}`, avoiding inline copies. The module is unconditionally compiled (`pub mod ssr;` in `lib.rs`), which is correct for a native-callable SSR path.

**Hydration module (`crates/ferric/src/hydrate.rs`, new)**
Reviewed the module-level cfg gate and all browser-API references. `hydrate.rs` opens with `#![cfg(target_arch = "wasm32")]`, which suppresses the entire file on non-wasm targets. The corresponding `lib.rs` declaration is `#[cfg(target_arch = "wasm32")] pub mod hydrate;` and the crate-root re-export is `#[cfg(target_arch = "wasm32")] pub use crate::hydrate::hydrate;`. The module makes heavy use of `web_sys`, `wasm_bindgen`, and `js-sys`; none of these escape to the native target because the file-level gate is authoritative. Compile-time boundary holds.

**DOM module (`crates/ferric/src/dom.rs`, unchanged by this PR)**
Reviewed the module declaration in `lib.rs` and the top of `dom.rs`. `dom.rs` uses `wasm_bindgen::closure::Closure`, `wasm_bindgen::{JsCast, JsValue}`, and `web_sys` throughout its body. It carries no `#![cfg(target_arch = "wasm32")]` gate. The module declaration in `lib.rs` is the unconditional `pub mod dom;`. The `prelude` block re-exports `crate::dom::mount` without a cfg guard.

**Server handler (`crates/chirp-server/src/ssr.rs`, new)**
Reviewed the full module body. The handler calls `ferric::render_to_string(...)` and `ferric::VElement::new(...)` — both always-compiled paths. No `web_sys` or `wasm_bindgen` items are imported directly. The handler does not reach into `ferric::dom` or `ferric::hydrate`.

**Cargo manifests**
Reviewed `crates/chirp-server/Cargo.toml` (adds `ferric = { path = "../ferric" }`) and `crates/ferric/Cargo.toml` (unchanged). `ferric/Cargo.toml` lists `wasm-bindgen`, `js-sys`, and `web-sys` in `[dependencies]` unconditionally — not under `[target.'cfg(target_arch = "wasm32")'.dependencies]`.

**cfg / feature flags**
No Cargo feature flags are used to gate the SSR vs. client-side split; separation is by compile target only. Reviewed `lib.rs` for every module declaration and re-export, checking which carry `#[cfg(target_arch = "wasm32")]` and which do not.

---

## Evidence

The core SSR/client boundary (`ssr.rs` clean, `hydrate.rs` gated) is correctly maintained. The finding is an asymmetry between `dom` and `hydrate`, both of which are browser-only modules, exposed by the PR making `ferric` a native dependency for the first time.

**Location of the gap:**

```
crates/ferric/src/lib.rs:22   pub mod dom;
```

`pub mod dom;` carries no `#[cfg(target_arch = "wasm32")]` gate, while the peer declaration introduced by this PR does:

```
crates/ferric/src/lib.rs:33   #[cfg(target_arch = "wasm32")]
crates/ferric/src/lib.rs:34   pub mod hydrate;
```

**`dom.rs` uses browser APIs without a module gate:**

```
crates/ferric/src/dom.rs:46   use wasm_bindgen::closure::Closure;
crates/ferric/src/dom.rs:47   use wasm_bindgen::{JsCast, JsValue};
```

(approximate line numbers from pre-existing file; content confirmed via API)

**Prelude re-exports `dom::mount` without a cfg guard:**

```
crates/ferric/src/lib.rs   pub use crate::dom::mount;   (inside pub mod prelude { … })
```

**`dom.rs` module comment acknowledges the reliance on panicking stubs:**

> "The runtime calls into the DOM, so it is only meaningful in a browser/wasm context; `web-sys` provides panicking stubs off-wasm, which keeps the crate compiling and the non-DOM layers natively testable without a browser."

This rationale was written before `ferric` was a native server dependency; it documents intentional behavior in a wasm-only context, not a deliberately maintained server/client boundary.

---

## Finding

The SSR separation is correct: `ssr.rs` has no browser-only imports, and `hydrate.rs` is fully compile-time-gated. The finding is that `pub mod dom;` is not gated to `wasm32` in `lib.rs`, and the PR does not add that gate even though it introduces the identical pattern for `hydrate`.

**Impact:** `ferric::dom` and `ferric::prelude::mount` are now reachable from `chirp-server` (native build) because this PR adds `ferric` as a native dependency. They compile only because `web-sys` ships panicking stubs for non-wasm targets. If any downstream code in `chirp-server` (or any crate that depends on it) calls `ferric::dom::mount` or anything exported from `ferric::dom`, it will compile silently and panic at runtime — a silent correctness hazard that compile-time gating would prevent entirely.

**Why this matters now:** Before this PR, `ferric` was always compiled for `wasm32`; the absence of a gate on `dom` had no consequence. The PR is what exposes `dom` to the native build. The PR demonstrates the right fix — `#[cfg(target_arch = "wasm32")]` on `pub mod hydrate;` — but does not apply it to the equivalent existing module.

**What would satisfy this finding:**

1. Add `#[cfg(target_arch = "wasm32")]` to `pub mod dom;` in `crates/ferric/src/lib.rs`.
2. Add `#[cfg(target_arch = "wasm32")]` to `pub use crate::dom::mount;` in the `prelude` block (or accept that the whole `prelude` is wasm-only and gate the block).
3. Optionally, move `wasm-bindgen`, `js-sys`, and `web-sys` from `[dependencies]` to `[target.'cfg(target_arch = "wasm32")'.dependencies]` in `crates/ferric/Cargo.toml`, which would make the manifest's intent match the source-code gating.

The concern is scoped to the boundary: naming consistency belongs in Area A, the broader duplication question belongs in Area D.
