# _GLOBAL.md — ferric-ssr-r1 SSR + Hydration Subtree Hub

## Why This Subtree Exists

This DAG implements the SSR and hydration foundation for Ferric (issues #223, #224, #226 from
epic #133). The goal is a complete, production-quality SSR pipeline: server renders a Ferric
component tree to HTML, the client adopts that HTML without structural mutations, and event
handlers + reactive effects are wired onto the adopted DOM. BAR-005 (#225 — state carry and
async resource resume) is explicitly out of scope; it is blocked on issue #130.

## Decomposition Cut and Rationale

The work spans two fundamentally different compile targets and three distinct concerns:

1. **Server-side rendering** — a pure Rust function (`render_to_string`) that walks a VNode tree
   and emits HTML. Runs on native (non-wasm) targets; must never reference `web_sys` or
   `wasm_bindgen`. Owns `crates/ferric/src/ssr.rs`.

2. **Client-side hydration** — a WASM function (`hydrate`) that adopts a server-rendered DOM
   without structural mutations, wires event handlers, establishes reactive effects, and detects
   + recovers from tree mismatches. Owns `crates/ferric/src/hydrate.rs`.

3. **Axum integration** — a document assembly helper and route handler in `crates/chirp-server`
   that calls `render_to_string` and composes with the existing `build_router`. Owns new files in
   `crates/chirp-server/src/` and `crates/chirp-server/Cargo.toml`.

The cut is a walking-skeleton → three parallel disjoint spokes → synthesis gate:

```
ferric-ssr-r1-skeleton
    → ferric-ssr-r1-server-render  (branch work/ferric-ssr-r1-server)
    → ferric-ssr-r1-client-hydrate (branch work/ferric-ssr-r1-client)
    → ferric-ssr-r1-axum-integration (branch work/ferric-ssr-r1-axum)
         → ferric-ssr-r1-synthesis
```

**Why a skeleton first**: `crates/ferric/src/lib.rs` and `Cargo.toml` are shared structural files.
The skeleton takes sole ownership of them, pre-declares the new module slots with correct
compile-target gating, and leaves working stubs so each spoke can compile cleanly against a
real (if unimplemented) API surface. After the skeleton, spokes own strictly disjoint files.

**Why three parallel spokes**: server-render (Rust-only), client-hydrate (WASM-only), and
axum-integration (separate crate) have zero file overlap and can proceed concurrently.

**Why a synthesis gate**: The gate merges the three sub-branches (which are disjoint, so no
conflicts), runs the full identity-assertion checklist from `contracts/_MANIFEST.yaml`, and
creates the single PR closing all three issues.

## Contract Seam: Text-Boundary Markers

The critical composition seam between server-render and client-hydrate is the HTML
text-boundary marker format. These are HTML comment nodes that bracket every `VNode::Text`
in the server output. The client's hydration walk locates text nodes without counting these
comment nodes as structural VNode children, keeping child-index alignment stable.

The contract fixes this format before any spoke begins:
- Open marker: `<!--$t-->`
- Close marker: `<!--/$t-->`

Both spokes import this constant from `crate::ssr` or from the contract file — never from
inline string literals.

## Methodology Posture

- **Greenfield feature shape** (anchor: decomposition/DECOMPOSITION_ANCHOR.md,
  sibling: GREENFIELD_FEATURE_SHAPES.md): skeleton → parallel spokes → synthesis gate.
- **Contract Layer** (modules/contract_layer/CONTRACT_LAYER.md): `contracts/` is authored
  at this hub and inherited read-only by all descendant tasks.
- Each spoke applies the standard software methodology for its concern (server-side Rust
  implementation, WASM runtime implementation, Axum handler integration).

## Frozen Surface (Do Not Modify)

The following `crates/ferric/src/` files are part of the frozen prelude and must not be
modified by any task in this subtree:

- `dom.rs`
- `signal.rs`
- `vdom.rs`
- `component.rs`

New surface (`render_to_string`, `hydrate`) is strictly additive.

## Branch Strategy

| Branch | Owner Task | Purpose |
|---|---|---|
| `work/ferric-ssr-r1` | skeleton, then synthesis | Main feature branch; skeleton commits stubs; synthesis merges spokes |
| `work/ferric-ssr-r1-server` | server-render spoke | Server-render implementation |
| `work/ferric-ssr-r1-client` | client-hydrate spoke | Client hydration + mismatch |
| `work/ferric-ssr-r1-axum` | axum-integration spoke | Axum handler integration |

All sub-branches are based on `work/ferric-ssr-r1` after the skeleton has committed. All are
merged into `work/ferric-ssr-r1` by the synthesis gate before PR creation.
