# _BRIEF.md — T03: Component model — props, children, named slots (#140)

**Task ID:** ferric-authoring-140-comp  
**Hub:** ferric-epic-authoring-r1  
**Branch:** `work/ferric-epic-authoring-r1` (started by T01, with view! macro from T02)  
**Closes:** GitHub issue #140

---

## Objective

Implement the `#[component]` proc-macro and the associated types that form the declared component
surface per `design/ferric/authoring-model.md` §3. These are strictly additive over the existing
`Component` trait (which remains the runtime interface). `#[component]` is sugar that generates a
typed props struct and builder; nothing in the frozen prelude is redefined.

---

## Inputs

- Branch `work/ferric-epic-authoring-r1` as left by T02 (with the `view!` macro).
- `design/ferric/authoring-model.md` §3 on main — the authoritative specification for
  `#[component]`, typed props (§3.2), `Children` (§3.3), named slots `Slot` and `SlotFn<T>` (§3.4),
  composition (§3.5), additive types and lowering (§3.6), and diagnostics (§3.7).
- `crates/ferric/src/component.rs` — the existing `Component` trait baseline.
- GitHub issue #140 and its acceptance criteria.
- `design/ferric/release-bar.md` §BAR-FERRIC-009.

---

## Acceptance criteria (from issue #140 and authoring-model.md §3)

The following all compile and render correctly:

**Required and optional props with defaults**
```rust
#[component]
fn Greeting(name: String, #[prop(default = 3)] times: usize) -> VNode {
    view! { <p>{format!("Hello {name} ×{times}")}</p> }
}
// Both: view! { <Greeting name={"ferric".into()} times=5 /> }
// Default: view! { <Greeting name={"ferric".into()} /> }  — times = 3
```

**Converting prop (`#[prop(into)]`)**
```rust
#[component]
fn Avatar(#[prop(into)] src: String) -> VNode { view! { <img src={src}/> } }
// Called as: view! { <Avatar src="/img.png"/> }  — &str coerces to String
```

**Children**
```rust
#[component]
fn Card(title: String, children: Children) -> VNode {
    view! { <section><h2>{title}</h2>{children()}</section> }
}
// view! { <Card title={"x".into()}><p>"body"</p></Card> }
```

**Named slots**
```rust
#[component]
fn Page(header: Slot, children: Children) -> VNode {
    view! { <article><header>{header()}</header><main>{children()}</main></article> }
}
// view! { <Page><slot:header><h1>"Title"</h1></slot:header><p>"body"</p></Page> }
```

**Parameterized slot (`SlotFn<T>`)**
```rust
#[component]
fn List<T: Clone + 'static>(items: Vec<T>, row: SlotFn<T>) -> VNode { /* ... */ }
```
(type compiles; full invocation from view! is out of scope for this task — it is `one_oh` per
the design. The type and its signature must be declared and exported.)

**`dyn Component` dynamic dispatch**
```rust
let components: Vec<Box<dyn Component>> = vec![Box::new(Clock), Box::new(spacer)];
```
Renders each via `Component::render`. (The existing trait already supports this; the task confirms
it still compiles with the component model additions present.)

**`From` conversion** (optional-prop accepting a compatible type)
Demonstrated by the `#[prop(into)]` form above.

**Zero-prop component** (the baseline `Fn() -> VNode` form unchanged)
```rust
#[component]
fn Empty() -> VNode { view! { <span/> } }
```

---

## New additive types to export from the ferric prelude

| Type | Shape |
|---|---|
| `Children` | `std::rc::Rc<dyn Fn() -> Vec<VNode>>` |
| `Slot` | `std::rc::Rc<dyn Fn() -> Vec<VNode>>` (distinct from `Children`) |
| `SlotFn<T>` | `std::rc::Rc<dyn Fn(T) -> Vec<VNode>>` |

These are new exports; no existing prelude item changes.

---

## Declared outputs

- `#[component]` proc-macro added to `crates/ferric-macros/`.
- `Children`, `Slot`, `SlotFn<T>` defined in `crates/ferric/` and exported from the prelude.
- Tests for all acceptance-criteria forms above.
- Issue #140 closed.
- `COMPLETE.md` in this workspace.

---

## Constraints

- All additions are strictly additive. The existing `Component` trait, its blanket `Fn` impl,
  and all existing prelude exports are unchanged.
- `#[component]` on a zero-parameter function generates an empty props type and leaves the
  blanket `Fn() -> VNode` impl undisturbed.
- MSRV: stable Rust 1.82; no nightly features.
- Parameterized slots (`SlotFn<T>`) are `one_oh` for the view! invocation side — the type
  itself must be declared, but a full macro invocation form for `SlotFn<T>` is not required at
  this stage. The type must compile and be reachable for direct Rust-level use.
- Leave the branch at a clean, CI-ready state for T04 and T05.
