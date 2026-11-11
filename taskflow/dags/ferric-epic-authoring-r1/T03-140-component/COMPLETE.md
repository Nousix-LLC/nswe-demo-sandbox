# COMPLETE — T03: Component model — props, children, named slots (#140)

**Task ID:** ferric-authoring-140-comp  
**Branch:** `work/ferric-epic-authoring-r1`  
**Commit:** `0088a5c`  
**GitHub issue #140:** Closed  
**Status:** completed

---

## Deliverables

### New types — `crates/ferric/src/component.rs` + prelude

| Type | Shape | Added to prelude |
|---|---|---|
| `Children` | `Rc<dyn Fn() -> Vec<VNode>>` | ✓ |
| `Slot` | `Rc<dyn Fn() -> Vec<VNode>>` | ✓ |
| `SlotFn<T>` | `Rc<dyn Fn(T) -> Vec<VNode>>` | ✓ |

`ferric_macros::component` re-exported from `ferric::prelude` as well.

### `#[component]` proc-macro — `crates/ferric-macros/src/component.rs`

- Transforms `#[component] fn Name(…) -> VNode { body }` into:
  - Hidden impl struct `__NameComponentImpl` implementing `Component::render`
  - Public `NameProps` builder with one setter per parameter
- Supported prop modifiers: required (plain), `#[prop(default = expr)]`,
  `#[prop(into)]`, `#[prop(optional)]`
- Generic components (e.g., `fn List<T: Clone + 'static>(…)`) carry generics
  through to both the impl struct and the builder

### `view!` macro update — `crates/ferric-macros/src/lower.rs` + `parser.rs`

- `lower_component` rewritten: `<Name prop={v}/>` → `NameProps::new().prop(v).build()` + `Component::render`
- Children thunk: regular nested content captured as `Rc::new(move || { Vec<VNode> })`
  passed to `.children(…)` setter
- Slot fill syntax: `<slot:name>…</slot:name>` parsed and lowered to
  `.name(Rc::new(move || { Vec<VNode> }))` setter
- `SlotFill` variant added to `ViewNode` / parser

---

## Acceptance criteria — all met

| AC | Status |
|---|---|
| Required + defaulted props (`#[prop(default=N)]`) | ✓ 2 tests |
| Converting prop (`#[prop(into)]`) | ✓ 1 test |
| `Children` parameter | ✓ 1 test |
| Named slot (`Slot`) + `<slot:name>` syntax | ✓ 1 test |
| `SlotFn<T>` type compiles and is usable | ✓ 1 test |
| `dyn Component` dynamic dispatch unaffected | ✓ 1 test |
| Zero-prop component | ✓ 1 test |
| `Children`/`Slot` types callable | ✓ 2 tests |

---

## Test results

| Test suite | Tests | Result |
|---|---|---|
| `ferric --lib` (pre-existing) | 37 | ✓ all pass |
| `ferric-macros --test lowering` (updated) | 16 | ✓ all pass |
| `ferric-macros --test component` (new) | 11 | ✓ all pass |
| `ferric` doc-tests | 7 | ✓ all pass |

---

## Constraints verified

- All additions strictly additive — `Component` trait, blanket `Fn() -> VNode`
  impl, and all existing prelude exports unchanged
- MSRV `cargo +1.82 build` clean
- No nightly features used
- Branch left at `0088a5c` on `work/ferric-epic-authoring-r1`, CI-ready for T04/T05
