# COMPLETE — SUBTASK_view_and_diff

**Task**: Implement `ferric`'s view layer — the `VNode` view tree, the `Component` abstraction, and
a keyed `diff → Vec<Patch>` — pure and native-testable, matching the frozen
`contracts/ferric_api.rs` surface.

**Status**: COMPLETE. `decompose_evaluation = Atomic`.

## What was delivered

Replaced the `todo!()` stubs of the two modules I own (per `contracts/_MANIFEST.yaml`):

- **`crates/ferric/src/vdom.rs`** — the view tree, the `Patch` enum, the keyed `diff`, ergonomic
  builders, and the module's native test suite.
- **`crates/ferric/src/component.rs`** — the `Component` trait + function-component blanket impl
  (frozen form, already correct in the skeleton) finalized with a doctest and native tests that
  exercise both component forms reading the **real** reactive `Signal` surface.

No other files touched (`lib.rs`/prelude is owned by `SUBTASK_scaffold`; `signal.rs` is the real
reactive core from `SUBTASK_reactive_core` and was imported, not modified or mocked).

## Design decisions (and their rationale)

### 1. `EventHandler` kept as the frozen `Rc<dyn Fn()>` — not enriched to carry `web_sys::Event`
The frozen contract shows `Rc<dyn Fn(/* web_sys::Event */)>` with the argument commented out, and
both `contracts/ferric_api.rs` and the `dom.rs` stub flag realizing a `web_sys::Event` parameter as
an **owner-latitude additive refinement for the DOM layer (and this layer)**. I deliberately did
**not** take it, because:
- My brief scopes web-sys **out** of this layer ("no web-sys calls here … the view tree must be
  pure/native-testable"). Pulling `web_sys::Event` into the `vdom` type alias would seat a web-sys
  type in the pure layer.
- Changing `Rc<dyn Fn()>` → `Rc<dyn Fn(web_sys::Event)>` is a **non-additive** signature change; the
  contract requires an additive plan amendment for that, not a silent in-place edit.
- It is not needed for my deliverables (view tree + keyed diff + native tests), and the counter
  example's handlers are click handlers that need no event payload.

**Handoff for `SUBTASK_dom_runtime`**: if the DOM runtime needs the event payload (e.g. to read an
`<input>`'s value on `EventKind::Input`), that is exactly the anticipated additive refinement.
Request a plan amendment to extend `EventHandler` (e.g. `Rc<dyn Fn(web_sys::Event)>`) — the required
`web-sys` features (`Event`, `InputEvent`, `MouseEvent`, `HtmlInputElement`) are already enabled in
`Cargo.toml`. Until then, handlers are zero-arg; a signal-capturing click handler works directly.

### 2. `Patch` is path-addressed; children are reconciled by key with a positional fallback
- Each `Patch` addresses a node by a `path` of child indices from the root (empty = root). Variants:
  `Replace`, `SetText`, `SetAttr`, `RemoveAttr`, `SetEvents`, `InsertChild`, `RemoveChild`,
  `MoveChild`.
- **Application order is part of the contract**: the runtime applies patches in list order. For each
  parent, `diff` emits structural child edits (removals descending, then a left-to-right
  move/insert positioning pass) **before** recursing into retained children, so every `path`
  resolves against the arrangement produced by the patches already applied. The emission mirrors a
  working child list so indices stay valid as the list mutates.
- **Keyed vs positional**: a child list is reconciled by `Key` when every child on both sides is a
  keyed element (insert / move / remove by identity); otherwise a positional index-wise diff is used
  (recurse the common prefix, append/trim the tail). This is the standard keyed/non-keyed split and
  is documented on `diff`. The target use case (a Twitter-style timeline of keyed items) is a
  fully-keyed list.

### 3. Event re-binding keyed on `EventKind` set
Closures are not comparable, so the diff cannot minimise against handler identity. A retained
element emits `SetEvents` (re-binding the new handler set) **only when the set of bound
`EventKind`s changes**. Consequently a no-op diff of structurally identical trees produces **zero**
patches even when handlers are present. Keeping a retained element's prior closure across a
re-render is sound here because handlers read their `Signal`s live rather than capturing values.

### 4. Additive ergonomic builders
Added (additive to the frozen surface, allowed by the contract's "plus any convenience builders the
owners add"): `VElement::new(tag)` with chainable `.key/.attr/.on/.child/.children`, a free
`text(..)`, and `impl From<VElement> for VNode`. These make hand-written SPA views ergonomic without
touching the scaffold-owned prelude (the frozen `VElement`/`VNode`/`EventKind`/`Component` re-exports
already reach the builders as methods).

## Verification (all run inside `checkout/` on branch `work/ferric-foundation`)

| Check | Command | Result |
|---|---|---|
| Host build | `cargo build --workspace` | PASS |
| Native tests | `cargo test --workspace` | PASS — 34 unit tests + 6 doctests (1 `ignore`d by design in `lib.rs`) |
| fmt | `cargo fmt --all --check` | PASS |
| clippy (warnings = errors) | `cargo clippy --all-targets -- -D warnings` | PASS (clean; satisfies `missing_docs` on all public items) |
| wasm build | `cargo build -p ferric --target wasm32-unknown-unknown` | PASS |

### Test coverage highlights (diff correctness)
A **shadow-DOM apply simulator** in `vdom.rs` tests is the gold assertion: for every (old, new)
case, `apply(shadow(old), diff(old, new)) == shadow(new)`. On top of it, targeted cases assert
minimality/shape:
- `no_op_equal_trees_produce_no_patches`, `no_op_is_empty_even_with_event_handlers`
- `text_change_produces_single_settext`, `attr_add_change_and_remove`
- `tag_change_is_replace`, `element_to_text_is_replace`
- `event_binding_added_emits_setevents`, `event_binding_removed_emits_setevents`
- keyed children: `insert_in_middle`, `remove`, `reorder_emits_moves_not_replaces`,
  `reorder_preserves_identity_and_patches_content`, `keyed_move_insert_and_remove_combined`,
  `full_list_clear_and_full_list_fill`
- `unkeyed_children_diff_positionally`, `nested_recursive_diff_reaches_deep_nodes`
- `component.rs`: function component + trait-object component render a `VNode`; a function component
  reads a real `Signal` and reflects a later `set`; an event handler drives a signal when invoked.

## Success criteria (from `_BRIEF.md`)
- [x] Frozen `vdom`/`component` surface implemented + documented; prelude still resolves (workspace
      lib build validates the `pub use` re-exports).
- [x] Keyed diff produces correct minimal patches; covered by passing native tests (apply-simulator
      round-trip + targeted cases).
- [x] Components (trait + function form) produce a `VNode` tree and may read reactive signals.
- [x] fmt/clippy clean for these modules; crate builds host + `wasm32-unknown-unknown`.

## Outputs
- `checkout/crates/ferric/src/vdom.rs`
- `checkout/crates/ferric/src/component.rs`
- This `COMPLETE.md`

Committed on `work/ferric-foundation` as `0f80cdc`. `SUBTASK_dom_runtime` can now build `mount()`
on the real `VNode`/`Patch`/`diff`/`Component` output (and should request the additive
`EventHandler` enrichment if it needs the event payload).
