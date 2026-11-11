# Q1 — Responsibility Partitioning and Coupling: Sub-Findings

concern: code-quality

---

## Findings

### Finding 1 — async_resource.rs: suspense() colocation introduces a vdom dependency into the resource-lifecycle module

**severity**: non-blocker
**concern**: code-quality
**location**: crates/ferric/src/async_resource.rs:14 (use crate::vdom::VNode) / structural

`async_resource.rs` imports `crate::vdom::VNode` because `suspense()` takes and returns `VNode` closures:

```rust
use crate::vdom::VNode;

pub fn suspense(fallback: impl Fn() -> VNode, children: impl Fn() -> VNode) -> VNode { ... }
```

This makes `async_resource` depend on `vdom`. The resulting intra-crate dependency order is: `signal` (leaf) → `vdom` (depends on std only) → `async_resource` (depends on `signal` + `vdom`) → `dom` (depends on `vdom`) / `form` (depends on `signal` + `vdom`).

The brief identified `async_resource.rs` as responsible for resource lifecycle — signal/subscription management and generation-counter bookkeeping — with "no DOM concerns expected." There are no `web_sys` imports and no DOM concerns. But `suspense()` is a view-layer compositor: it renders a fallback `VNode` or the children `VNode` depending on loading state. Colocating it in the resource module makes `async_resource` carry two responsibilities: resource lifecycle and view-boundary composition.

The colocation is defensible: `suspense()` reads `SUSPENSE_DEPTH` and `SUSPENSE_HAS_LOADING`, two thread-local sentinels that `create_resource` increments and sets during reactive re-runs. Splitting `suspense()` out into a separate `suspense.rs` or `view.rs` would require either exporting those sentinels (leaking internals) or crossing a module boundary that the current design avoids by keeping them private. The tradeoff is real and the author made a coherent choice.

What is not clean is that the module's doc header and brief description say nothing about this view-compositor role. A reader arriving at `async_resource.rs` expecting only resource lifecycle machinery will find `suspense()` unexplained. A doc note at the top-level module doc comment explaining that `suspense()` lives here because it depends on the loading sentinels would make the boundary legible without restructuring.

This is a **non-blocker**: the coupling does not violate any stated requirement, it is mechanically necessary given the colocation of the sentinels, and the `web_sys` boundary is fully respected. The gap is documentation rather than structure.

---

### Finding 2 — vdom.rs: clean of web_sys; dyn Any used for type erasure, not DOM coupling

**severity**: clean
**concern**: code-quality
**location**: crates/ferric/src/vdom.rs

Imports in the modified file are:

```rust
use std::collections::{BTreeMap, HashSet};
use std::fmt;
use std::rc::Rc;
// (std::any::Any used inline in EventHandler::WithEvent)
```

No `web_sys`, no `wasm_bindgen`, no `async_resource`, no `form`. The `WithEvent` variant carries `Rc<dyn Fn(&dyn std::any::Any)>`: `std::any::Any` is a Rust standard-library trait, not a browser type. The DOM layer (`dom.rs`) does the downcast to `web_sys::Event` on the other side of the type erasure — `vdom.rs` itself never touches a concrete browser type.

The `EventKind` expansion (2 → 47 + `Custom(String)`) and the `EventHandler` type change from `type alias = Rc<dyn Fn()>` to an enum are view-representation changes consistent with the vdom layer's responsibility. `BTreeSet<EventKind>` → `HashSet<EventKind>` in the test shadow struct follows naturally from removing `Ord` (which requires `Copy`, which `Custom(String)` prevents).

The module's responsibility boundary — virtual DOM representation, pure keyed diff algorithm, event binding type definitions — is intact. No unexpected imports or layer crossings.

---

### Finding 3 — dom.rs: clean of async_resource and form coupling

**severity**: clean
**concern**: code-quality
**location**: crates/ferric/src/dom.rs

The import line (unchanged in this PR):

```rust
use crate::vdom::{diff, EventHandler, EventKind, Patch, VNode};
```

No `async_resource`, no `form`. The PR's changes to `dom.rs` expand `event_name()` and `stash_key()` to handle the 47 + `Custom(String)` variants (signature change: `EventKind` → `&EventKind`, return type `&'static str` → `String`), add `static_event_kinds()` to produce the array for the detachment pass, and extend `set_events()` to wire `Custom` names through a `__ferric_custom_events` JS array.

The `EventHandler` dispatch now branches:
```rust
EventHandler::NoArg(f) => f(),
EventHandler::WithEvent(f) => f(&event as &dyn Any),
```

This is `dom.rs` correctly fulfilling its bridge role: it receives the type-erased `&dyn Any` from vdom, materialises a real `web_sys::Event`, and dispatches it. The concrete DOM coupling is fully contained in this module. No cross-layer leakage outward.

---

### Finding 4 — form.rs: clean of async_resource; web_sys gated to wasm32

**severity**: clean
**concern**: code-quality
**location**: crates/ferric/src/form.rs

Imports at the top of the file:

```rust
use std::marker::PhantomData;
use std::rc::Rc;
use std::str::FromStr;

use crate::signal::{create_signal, Signal};
use crate::vdom::EventHandler;

#[cfg(target_arch = "wasm32")]
use wasm_bindgen::JsCast;
#[cfg(target_arch = "wasm32")]
use web_sys::{Event, HtmlInputElement};
```

No import from `async_resource`. `form.rs` does not reach into resource lifecycle internals in any form — no use of `Resource`, `ResourceState`, `create_resource`, `suspense`, or the SUSPENSE thread-locals.

The `crate::vdom::EventHandler` import is expected: `Bind::on_input_handler()` returns `EventHandler::NoArg(...)` and `on_input_event_handler()` returns `EventHandler::WithEvent(...)`. The form module sits at the application layer and produces handler values that dom.rs will later dispatch — that path through `vdom::EventHandler` is the correct one.

`web_sys` types (`Event`, `HtmlInputElement`) appear only inside `#[cfg(target_arch = "wasm32")]`. The buffer-based `on_input_handler()` path is fully native, enabling all 18 `#[cfg(test)]` tests to run without a WASM target. The DOM-direct `on_input_event_handler()` path is explicitly gated. The `#[cfg]` split is a deliberate testability design: its rationale is documented in the `Bind` doc comment under "Testability — approach 2 (WASM-free)."

Responsibility boundary: `form.rs` owns form-state types (`FormField<T>`, `Bind<T>`) and produces view-layer wiring descriptors (`EventHandler`, attribute pairs) without crossing into resource lifecycle or concrete DOM dispatch.

---

### Finding 5 — Cross-module dependency graph: one acceptable sideways dependency

**severity**: non-blocker
**concern**: code-quality
**location**: structural

After reading all four files, the intra-crate dependency graph for the four modules under review is:

```
signal (leaf, no internal deps)
  ↑           ↑
vdom          |
  ↑           |
  ├── async_resource (signal + vdom)
  ├── dom      (vdom only)
  └── form     (signal + vdom)
```

The only sideways dependency is `async_resource → vdom`, surfaced in Finding 1. All other dependencies run downward through the layer model. `dom.rs` does not import from `async_resource` or `form`. `form.rs` does not import from `async_resource`. No cycles.

The dependency graph is not fully flat-layered — `async_resource` sits at the same conceptual level as `form` but depends on `vdom` while `form` also depends on `vdom`, making both sit above `vdom`. This is consistent and not a structural problem; both are application-level modules that compose view-layer types. The absence of a cycle and the absence of any `dom`-layer coupling from application-layer modules (`async_resource`, `form`) is what matters.

---

## What was examined

**Files read in full (via `gh pr diff 193 --repo Nousix-LLC/nswe-demo`):**

| File | Diff lines read | Notes |
|------|----------------|-------|
| `crates/ferric/src/async_resource.rs` | Full new-file content (832 lines) | Import list, suspense() signature, thread-locals, public API |
| `crates/ferric/src/vdom.rs` | Full change section | EventKind expansion, EventHandler enum, diff_events, test shadow struct |
| `crates/ferric/src/dom.rs` | Full change section | event_name/stash_key signature changes, set_events expansion, EventHandler dispatch |
| `crates/ferric/src/form.rs` | Full new-file content (531 lines) | Import list, FormField, Bind, test suite, wasm_tests module |
| `crates/ferric/src/lib.rs` | Prelude additions | async_resource, form added to pub mod and prelude exports |
| `crates/ferric/Cargo.toml` | Dependency additions | wasm-bindgen-futures, 8 web-sys features |
| `crates/ferric/src/component.rs` | Handler invocation change | Confirms EventHandler enum transition |

**Sub-questions covered:**

1. **Q1.1 — Single responsibility per file**: Examined each file's module-level doc comment, public API surface, and import list against the expected layer model. All four files have a legible primary responsibility. The one impurity is `suspense()` in `async_resource.rs` (Finding 1, non-blocker).

2. **Q1.2 — Unexpected imports / cross-layer dependencies**: Checked every `use` statement in each changed file. The only cross-layer dependency from the brief's expected model is `async_resource` importing `crate::vdom::VNode`. No cycles, no DOM-layer imports from application-layer modules.

3. **Q1.3 — Module-boundary concerns not covered by Q2 or Q4**: Q2 owns the EventHandler enum design decision; Q4 owns correct-use patterns. This review did not duplicate those. The dependency graph question (Finding 5) and the `suspense()` colocation question (Finding 1) are the structural concerns not covered elsewhere.

**What was not examined here:** Generation counter logic (Q3), EventHandler variant design rationale (Q2), and correct-use / misuse-resistance patterns (Q4) — those are owned by their respective spoke tasks.
