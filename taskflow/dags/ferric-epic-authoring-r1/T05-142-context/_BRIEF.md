# _BRIEF.md — T05: Context and dependency injection (#142)

**Task ID:** ferric-authoring-142-ctx  
**Hub:** ferric-epic-authoring-r1  
**Branch:** `work/ferric-epic-authoring-r1` (with component model from T03)  
**Closes:** GitHub issue #142

---

## Objective

Implement the context API — `provide_context`, `use_context`, and `expect_context` — per
`design/ferric/authoring-model.md` §4. These are free functions added to the `ferric` prelude.
They enable passing values to any descendant component without prop threading.

The context value store sits on the existing reactive owner scope (`ReactiveScope` in `signal.rs`);
no second lifetime rule is introduced. When a scope is disposed, its context entries are released
with it — the same disposal path that already unsubscribes effects and memos.

---

## Inputs

- Branch `work/ferric-epic-authoring-r1` as left by T03 (with the component model; this task may
  run in parallel with T04 since neither touches the other's code).
- `design/ferric/authoring-model.md` §4 on main — authoritative specification for the context API
  surface (§4.1), no-provider case (§4.2), reactivity through the provided handle (§4.3), scoped
  cleanup (§4.4), design decisions (§4.5), runtime integration (§4.6), and the context seam IA3
  (§4.7).
- `crates/ferric/src/signal.rs` — the existing `ReactiveScope`, `Runtime`, and owner stack that
  the context implementation extends.
- GitHub issue #142 and its acceptance criteria.
- `design/ferric/release-bar.md` §BAR-FERRIC-011.

---

## Acceptance criteria (from issue #142 and authoring-model.md §4)

**API surface (all in `ferric::prelude`)**
```rust
pub fn provide_context<T: Clone + 'static>(value: T);
pub fn use_context<T: Clone + 'static>() -> Option<T>;   // None when absent
pub fn expect_context<T: Clone + 'static>() -> T;        // panics with named message when absent
```

**No prop threading** — a value provided at an outer component is readable by an inner component
with no parameter threading through intermediate components.

**Type-keyed lookup** — `use_context::<T>()` and `expect_context::<T>()` find the nearest-ancestor
provided value of that type. Two distinct newtypes (`struct A(Signal<i32>)`, `struct B(Signal<i32>)`)
resolve to their respective provided values independently.

**Nearest-ancestor shadowing** — when the same type is provided at two levels, `use_context`
returns the inner value for components in the inner scope.

**Scoped cleanup** — a provided value is released when the owner scope it was provided into is
disposed. After disposal, a lookup of that type in a scope that was inside the disposed scope
returns `None` (or a value from a surviving outer provider, if present).

**`expect_context` panic message** — when no provider is found, the panic message names the
missing type (e.g., "no context of type `my_app::Theme` was found; an ancestor component must
call `provide_context::<my_app::Theme>(..)` before this component is rendered").

**Tests must cover:**
- Providing and reading a simple value (string, integer, `Clone` struct).
- Providing a `Signal<T>` and reading it in a descendant; confirming the signal value is live.
- `use_context` returning `None` when no provider exists.
- `expect_context` panicking with a message that names the missing type.
- Nearest-ancestor shadowing: inner provider value is returned for inner components.
- Scoped cleanup: disposing the providing scope removes the context entry.

---

## Declared outputs

- Context store added to `crates/ferric/src/signal.rs` (or a new `src/context.rs` module), using
  the existing `ReactiveScope` / owner stack infrastructure.
- `provide_context`, `use_context`, `expect_context` exported from the ferric prelude.
- Test suite covering all cases above (native, no browser required).
- Issue #142 closed.
- `COMPLETE.md` in this workspace.

---

## Constraints

- All additions are strictly additive. The existing `ReactiveScope`, `Signal`, `Memo`, and all
  public prelude items are unchanged.
- Context is not itself reactive (authoring-model.md §4). Reactivity is through the provided
  handle (a `Signal<T>` or `Memo<T>` in the value), not through the lookup.
- MSRV: stable Rust 1.82; no nightly features.
- Do not introduce a second lifetime rule for context. Context entries share the existing
  owner-scope disposal path.
- This task may land its commits on the branch in parallel with T04. The two tasks touch
  disjoint parts of the codebase (T04 is diagnostic fixtures only; T05 is `signal.rs` and
  prelude). If a merge conflict arises, resolve it cleanly.
- Leave the branch at a clean, CI-ready state for T06.
