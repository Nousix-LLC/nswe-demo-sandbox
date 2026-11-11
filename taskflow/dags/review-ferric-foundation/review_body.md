## Review verdict: APPROVE ✅

Principal-level review of `ferric-foundation` (issue #4) against the issue's acceptance criteria and the `code-review` / `rust` / `core` methodologies. I read the full ~3k-line additive diff myself (reactive core, keyed diff, and the web-sys DOM runtime), rather than deferring to the already-green machine gate. **No block- or major-severity findings.** Six minor/nit/informational findings are listed below; none block the merge.

### What I verified by reading (not just trusting the gate)

- **Reactive-core soundness (`signal.rs`)** — The generational arena is ABA-safe (slot generation bumps on removal; stale `NodeId`s resolve to `None`). Each node's value lives behind its own `Rc<RefCell<Box<dyn Any>>>`, so a read/write borrows only that cell — **never the runtime** — while a user closure runs, which is the property that avoids re-entrant runtime-borrow panics. Dependency re-tracking is correct: each computation clears its sources/children before re-running, so conditional reads unsubscribe (verified by `effect_tracks_only_currently_read_dependencies`). Memos are lazy and glitch-free on diamond graphs (dirty-marking recurses once; a reader recomputes upstream first). `BatchGuard` decrements on unwind, so a panicking batch body cannot wedge the runtime at non-zero depth. The `no_stale_subscriber_leak` and `generational_keys_are_aba_safe` tests genuinely exercise these invariants.
- **Keyed diff (`vdom.rs`)** — Correct. The `working` mirror tracks the evolving child list so every emitted index stays valid, and the shadow-DOM roundtrip tests prove `apply(shadow(old), diff(old,new)) == shadow(new)` across insert/move/remove/replace/reorder, including the combined `a,b,c,d → d,b,e,a` case.
- **Cross-layer consistency** — `MoveChild`'s remove-then-insert index semantics are identical across three places that must agree: the diff's `working` mutation, the shadow-DOM test harness, and the real `web-sys` `apply_patches`. This is exactly the kind of invariant that's easy to get subtly wrong across layers, and it's right.
- **Hazards** — Zero `unsafe`; zero `unwrap()` in production code (the four are in the wasm-only test). The only reachable production `panic!`/`expect`s are provably-guarded invariants or browser-runtime DOM-desync traps.
- **Diff is purely additive** — all 11 paths are additions; nothing on `main` is modified.

### Acceptance criteria (issue #4)

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Virtual workspace + `crates/ferric` | ✅ met (`resolver="2"`, `members=["crates/*"]`) |
| 2 | Sound reactive signals: computed + batching, no stale-subscriber leaks | ✅ met (verified by reading + native tests) |
| 3 | Component model + `mount` | ✅ met (`Component` trait + `Fn() -> VNode` blanket impl; `dom::mount`) |
| 4 | DOM rendering via wasm-bindgen/web-sys, keyed diff + click/input | ✅ met |
| 5 | wasm build + counter example | ✅ met (both build to `wasm32-unknown-unknown`) |
| 6 | Native tests (wasm-bindgen-test optional without headless browser) | ✅ met (36 unit + 6 doctests native; browser test behind `cfg`) |
| 7 | fmt/clippy clean, rustdoc, README | ✅ met |

### Findings

| ID | Severity | Location | Finding |
|----|----------|----------|---------|
| F1 | minor | `dom.rs:220-257` (`set_events`) | Event-handler closures are leaked via `Closure::forget`. The old listener is correctly detached before re-bind (no double-fire), but its closure memory is never reclaimed, so each event-kind-**set** change on a retained element leaks one closure. Bounded in steady state (`SetEvents` only fires when the bound-kind set changes) and documented as an intentional foundation trade-off with a future per-element-registry path. Non-blocking; concurs with the gate's F1. |
| F2 | suggestion | `vdom.rs:357-406` (`diff_keyed_children`) | The keyed diff assumes sibling keys are **unique**; `working.iter().position(...)` silently takes the first match on a duplicate key, producing incorrect reconciliation with no diagnostic. Recommend documenting the uniqueness invariant on `VElement::key`/`diff` and adding a `debug_assert!` on sibling-key uniqueness. Standard keyed-diff invariant; worth hardening for a long-lived public surface. |
| F3 | nit | `lib.rs:9-11` | The crate-root module doc still describes the "walking-skeleton composition root … until then the leaf items are `todo!()` placeholders" scaffold state, but every module is now fully implemented. Update so a new reader isn't told to expect `todo!()` stubs. |
| F4 | nit | `vdom.rs:5`, `lib.rs`, `README` | "minimal … Patch list" slightly overstates the keyed reorder: attr/text/structure diffing is minimal, but the reorder is a greedy left-to-right position pass (not LIS-minimal), so a reshuffle may emit more `MoveChild`s than strictly necessary. Correctness is unaffected (roundtrip-proven). Suggest softening "minimal" or noting the greedy reorder. |
| F5 | nit | `signal.rs:533-543` (`Signal::with`) | `with` holds the value-cell borrow across the user closure `f`; a re-entrant `set`/`update` on the **same** signal inside `f` would panic (RefCell double-borrow). Inherent RefCell constraint and an unusual usage, but a one-line doc note on `with` would help consumers. |
| F6 | informational | `dom.rs` (`apply_patches`/`resolve`) | The DOM runtime is panic-heavy (~20 `expect`s): a patch/live-DOM desync or an externally-injected node is an unrecoverable trap rather than a surfaced error. Acceptable and partly documented for a foundation (no meaningful recovery from model/DOM divergence); consider surfacing diagnostics once the SPA layer and external scripts share the mount point. |

### Praise

The reactive core is genuinely well-engineered — the generational arena, per-node value cells, conditional-dependency re-tracking, lazy glitch-free memos, and panic-safe batching are all correct and backed by tests that target the actual soundness properties rather than happy-path behavior. The public API is additive-only against the frozen contract and ergonomic (builder pattern); a Twitter-style SPA is buildable on this surface later. Nice foundation.

### Decision

No block/major findings, all acceptance criteria substantively met, machine gate green → **APPROVE**. F2 (duplicate-key hardening) and F3 (stale crate-root doc) are the two I'd most encourage picking up in a follow-up, but neither blocks landing this foundation.
