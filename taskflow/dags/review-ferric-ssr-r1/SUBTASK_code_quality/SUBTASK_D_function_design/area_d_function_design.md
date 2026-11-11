# Area D: Function Size, Duplication, and Extensibility — PR #228

**Status**: FINDING (NON-BLOCKER)

---

## What Was Checked

**Files examined** (all on branch `work/ferric-ssr-r1`):

- `crates/ferric/src/ssr.rs` — all functions in the new SSR path: `is_void_element`, `escape_html`, `render_node`, `render_to_string`
- `crates/ferric/src/hydrate.rs` — all functions in the new hydration path: `hydrate`, `adopt_root_vnode`, `adopt_vnode`, `adopt_children`, `strip_sentinels`, `is_sentinel_comment`, `vnode_label`, `node_type_label`, `emit_mismatch_warning`, `create_node`, `apply_patches_impl`, `resolve_impl`, `resolve_element_impl`, `set_events`, `event_name`, `stash_key`
- `crates/ferric/src/dom.rs` — all private helpers in the existing client-side mount path: `create_node`, `apply_patches`, `resolve`, `resolve_element`, `set_events`, `event_name`, `stash_key`
- `crates/chirp-server/src/ssr.rs` — `assemble_document`, `ssr_handler`
- `crates/ferric/src/lib.rs` — module declarations and pub re-exports to understand the public API surface exposed

**Concerns examined**:

1. Function sizes — all functions in the three new/modified files, with attention to whether any impede review or future extraction
2. Logical duplication — structural and functional comparison of `hydrate.rs` helpers against `dom.rs` helpers for shared logic that is not shared by code
3. Extensibility — the design seam (or absence of one) for injecting async resources when #130 lands, at both the `ferric` library layer and the `chirp-server` integration layer

---

## Evidence

### Function sizes — CLEAN

Every function in the new code is individually reviewable. The largest are match dispatchers over exhaustive enums:

- `crates/ferric/src/hydrate.rs:327` — `apply_patches_impl` (~65 lines): a match over eight `Patch` variants, each arm 4–8 lines of DOM mutation; the length is proportional to the enum
- `crates/ferric/src/hydrate.rs:149` — `adopt_children` (~54 lines): a sequential loop over DOM children with sentinel-skipping and index alignment; long but linear
- `crates/ferric/src/hydrate.rs:91` — `adopt_vnode` (~57 lines): a match over `VNode::Element` and `VNode::Text` plus mismatch recovery; both arms are substantive enough to stay together

All other functions are under 40 lines. No function requires extraction for size alone.

### Finding D-1 — Duplication between `hydrate.rs` and `dom.rs` (seven functions)

The following private functions in `hydrate.rs` duplicate functions in `dom.rs`. The code acknowledges the duplication in doc-comments:

| `hydrate.rs` function | Line | `dom.rs` counterpart | Line | Comment in `hydrate.rs` |
|---|---|---|---|---|
| `create_node` | `crates/ferric/src/hydrate.rs:300` | `create_node` | `crates/ferric/src/dom.rs:104` | (none; near-identical body) |
| `apply_patches_impl` | `crates/ferric/src/hydrate.rs:327` | `apply_patches` | `crates/ferric/src/dom.rs:129` | "Mirrors `dom::apply_patches` exactly." |
| `resolve_impl` | `crates/ferric/src/hydrate.rs:393` | `resolve` | `crates/ferric/src/dom.rs:197` | "Mirrors `dom::resolve`." |
| `resolve_element_impl` | `crates/ferric/src/hydrate.rs:407` | `resolve_element` | `crates/ferric/src/dom.rs:212` | "Mirrors `dom::resolve_element`." |
| `set_events` | `crates/ferric/src/hydrate.rs:417` | `set_events` | `crates/ferric/src/dom.rs:220` | "Uses the same Reflect-based approach as `dom::set_events` with the same stash keys." |
| `event_name` | `crates/ferric/src/hydrate.rs:454` | `event_name` | `crates/ferric/src/dom.rs:260` | (identical bodies) |
| `stash_key` | `crates/ferric/src/hydrate.rs:461` | `stash_key` | `crates/ferric/src/dom.rs:268` | (identical bodies) |

The source of the duplication is structural: all seven `dom.rs` helpers are private (`fn`, not `pub` or `pub(crate)`), so `hydrate.rs` cannot call them and had to copy them.

**Divergence risk**: Rust's exhaustive match provides compile-time protection for the most critical shared abstraction — any new `Patch` or `EventKind` variant will cause a compile error in both `apply_patches_impl` and the `event_name`/`stash_key` matches in both files simultaneously, so enum additions cannot silently diverge. The unprotected paths are:

- `create_node` — behavioral drift in attribute ordering, encoding, or VNode variant handling would be silent; the two copies would disagree on the DOM shape they produce, corrupting the hand-off between the SSR adopt pass and subsequent reactive re-renders
- `set_events` event detachment loop (`crates/ferric/src/hydrate.rs:417`, `crates/ferric/src/dom.rs:220`) — both contain a hardcoded array of `EventKind` variants to detach during patch; a new kind added to the enum would cause the match arms to fail to compile (caught), but the detachment array in both files would silently miss the new kind (not caught)

The duplication is real and the unextracted shared abstraction is the finding. The documentation in comments confirms the author's awareness; what is absent is the extraction. The fix is to promote the shared helpers to `pub(crate)` in `dom.rs` (or a new `dom_ops.rs`/`runtime.rs` module) so `hydrate.rs` imports rather than copies them.

### Finding D-2 — `render_to_string` has no seam for async resource injection (#130)

`crates/ferric/src/ssr.rs:135`:

```rust
pub fn render_to_string<F>(f: F) -> String
where
    F: FnOnce() -> VNode,
```

The function is synchronous. It calls `scope.run(f)` once and serializes the returned `VNode` tree to HTML. There is no hook, context parameter, or trait boundary through which a caller could supply resolved async resource data before the render runs.

When #130 (async resources) lands, changing this function's signature — to `async fn`, to a `-> impl Future<Output = String>`, or to accept a resource-resolver parameter — will be a breaking change for every caller. Currently there is one caller (`crates/chirp-server/src/ssr.rs`), so the blast radius is small, but the ferric library has no provisional seam that would let the server-side API evolve without a signature break.

The `chirp-server` layer does carry an explicit seam: `crates/chirp-server/src/ssr.rs` declares `ssr_handler` as `async fn` and documents the BAR-005 state island via a commented-out `State(state): State<AppState>` parameter. That is a good pattern. The ferric library layer has no equivalent: neither a placeholder type parameter, a resource-context argument (`fn render_to_string<F, R>(f: F, resources: R) -> String`), nor a provisional trait (`AsyncResourceResolver`) signals the anticipated direction and keeps the future signature change localized.

---

## Finding

**Two non-blocking issues were found.**

### D-1: Unextracted shared DOM helpers (duplication)

Seven private helper functions in `crates/ferric/src/hydrate.rs` are copies of private helpers in `crates/ferric/src/dom.rs`. The code acknowledges the duplication in comments but does not extract the shared abstraction.

The practical risk is not in this change but in the next one: any behavioral fix or enhancement to the DOM-walking or event-wiring logic must be applied in both files. The unprotected divergence paths — `create_node` body drift and the hardcoded event-detachment array in `set_events` — are silent: Rust will not catch them.

Satisfactory resolution: promote the shared helpers to `pub(crate)` visibility in `dom.rs`, or extract them to a crate-private `dom_ops.rs` module, so `hydrate.rs` imports them rather than replicates them. Because both modules are `#[cfg(target_arch = "wasm32")]`-gated, the extraction does not require any cross-cfg changes — the shared module would carry the same gate.

### D-2: `render_to_string` has no async seam

`crates/ferric/src/ssr.rs:135` — the synchronous `FnOnce() -> VNode` signature has no hook for async resource resolution. When #130 lands, the signature must change, and that change will be a breaking API update rather than an additive one.

This is deferred by explicit design decision; it is not a correctness issue in this PR. The finding is that the current shape does not leave the door ajar: a resource-context parameter (`fn render_to_string<F, R: ResourceResolver>(f: F, ctx: R)`) or a provisional `NoResources` unit type for the context would signal the anticipated direction and avoid a full-signature break when #130 lands. Without it, the caller is not warned that the signature is provisional.

Neither issue blocks merge. D-1 should be tracked as a follow-on refactor before the next significant addition to `dom.rs` or `hydrate.rs`. D-2 should be revisited at the start of #130 implementation planning.
