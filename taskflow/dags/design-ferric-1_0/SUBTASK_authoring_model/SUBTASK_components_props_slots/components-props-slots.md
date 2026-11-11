# Ferric 1.0 — Component model: props, children, slots, and composition

This is part B of the Ferric 1.0 authoring model (subtree hub: `../_GLOBAL.md`). It specifies **what an author
writes** to declare a reusable component — how the component states the typed **props** it accepts, how it
accepts **children** and **named slots**, and how components **compose** — and the testable `REQ-API-030..059`
bar each of those must meet. It is design, not implementation: it states the authoring surface and what must
hold against it, not how the `#[component]` macro expands.

Everything here is additive over the frozen Ferric surface. The baseline component surface is a `Component`
trait with one method, `fn render(&self) -> VNode`, and a blanket impl making any `Fn() -> VNode` a
`Component` (`crates/ferric/src/component.rs`). The view tree it returns is `VNode` (`Element(VElement)` or
`Text(String)`), and `VElement` already carries a `children: Vec<VNode>` field plus a `.child(impl Into<VNode>)`
and `.children(impl IntoIterator<Item = VNode>)` builder (`crates/ferric/src/vdom.rs`). The frozen `prelude`
exports `Component`, `VNode`, `VElement`, `EventKind`, the reactive primitives, and `mount`
(`crates/ferric/src/lib.rs`). Nothing in that set is redefined below; the component model adds new items that
lower onto it.

---

## 1. The gap this closes

Today a component is any `Fn() -> VNode`, and there is no way to declare what it accepts. An author who wants a
reusable `Card` writes a closure that captures its inputs by hand, hand-builds the `VElement` tree with
`.child(...)` calls, and has no declared, type-checked surface for a caller to fill. There is no props
convention, no children convention, no named-slot convention, and no composition story beyond calling one
closure from inside another.

Persona A3 — the library/component author (`../../SUBTASK_scope_and_requirements/scope-and-requirements.md`,
§2) — is the user this section owes the most. A3 exposes components others build on and needs a declared
props/children/slots surface and a stable API (parent `REQ-FW-005`, `REQ-FW-010`). Persona A2, the application
author, feels the same gap every time they want to reuse a piece of UI. The bar (parent `REQ-FW-005`,
`usable_early`) is a component/composition model expressive enough to build a real app and documented well
enough to build on.

The four facets below — props, children, slots, composition — are one model seen from four sides, not four
independent features. Children and named slots are themselves kinds of prop; composition is what happens when
one component's declared surface is filled by another's output. A single ergonomic decision (how a component
declares what it accepts) governs all four, which is why they are specified together.

---

## 2. The central decision: a `#[component]` function with a generated typed props builder

An author declares a component as an ordinary Rust function annotated with `#[component]`. Its parameters are
its props; its body returns a `VNode` (typically written with the `view!` macro, part A). The attribute
generates, from the signature, a typed props type and a builder the `view!` macro fills:

```rust
use ferric::prelude::*;

#[component]
fn Greeting(name: String, #[prop(default = 3)] times: usize) -> VNode {
    view! { <p>{format!("Hello {name} ×{times}")}</p> }
}
```

What the author writes to use it (the `view!` grammar is owned by part A; shown here only to fix the
correspondence this section is responsible for):

```rust
view! { <Greeting name={"ferric".into()} times=5 /> }   // both props set
view! { <Greeting name={"ferric".into()} /> }           // times takes its default, 3
```

`#[component] fn Greeting(..) -> VNode` is **sugar over the frozen `Component` trait**. It produces three
things an author never writes by hand but can always fall back to (§7):

1. a **props struct** `GreetingProps` with one field per parameter;
2. a **builder** with one setter per field, honoring each field's required / optional / defaulted / converting
   kind (§3), which is the target the `view!` macro lowers a component invocation onto; and
3. a `Component` implementation whose `render` runs the function body with the props in scope.

This is the design every credible Rust peer converged on, and it is chosen deliberately over the alternatives:

| Declaration style | What the author writes | Why not chosen as the primary surface |
|---|---|---|
| **Positional function arguments, no struct** | `fn Greeting(name: String, times: usize)`, called positionally | Rust has no optional or defaulted function arguments and no named call arguments. Every prop would be required and positional; adding a prop or reordering would break every caller. No optional/defaulted props at all. |
| **Hand-written builder** (plain builder pattern, as Sycamore's lower-level form) | `Greeting::builder().name(..).times(..).build()` | Works and is explicit, but the author writes the builder plumbing for every component. Verbose enough that A3 pays the cost the framework should absorb. |
| **`#[component]` fn + generated typed props builder** (chosen) | the function above | Compile-time required/optional/defaulted props, named arguments through the builder, additive evolution (a new optional prop does not break existing callers), and the author writes a plain function. The cost is macro-generated code and the diagnostic-legibility burden that creates — paid down by the diagnostics bar in §8 (parent `REQ-FW-014`). |

**One divergence from the VDOM peers is deliberate and worth stating.** Yew requires component props to be
`PartialEq` so the framework can skip re-rendering when props are unchanged; Dioxus does likewise. Ferric does
**not** require props to be `PartialEq`, because change detection is not prop-diffing — it is the baseline's
fine-grained reactivity. A component's body runs inside the mount effect (`crates/ferric/src/component.rs`
module docs: "The DOM runtime invokes `render` inside a reactive effect"), so a prop that is a `Signal<T>` or
`Memo<T>` re-renders the parts that read it when it changes, with no prop-equality check. Props that are plain
owned values are set once at construction. This matches Leptos and Sycamore (signal-reactive, no props
`PartialEq` requirement) rather than Yew/Dioxus, and it follows directly from the reactive runtime Ferric
already has.

---

## 3. Typed props

A prop is a parameter of the `#[component]` function. Its kind is read from its type and its `#[prop(..)]`
attribute:

- **Required** — a plain typed parameter with no attribute. The caller must supply it; omission is a
  compile error that names the missing prop (§8).

  ```rust
  #[component]
  fn Avatar(src: String, alt: String) -> VNode { /* both required */ }
  ```

- **Optional** — `#[prop(optional)]`, which makes the prop an `Option<T>` defaulting to `None` when the
  caller omits it.

  ```rust
  #[component]
  fn Avatar(src: String, #[prop(optional)] alt: Option<String>) -> VNode { /* alt defaults to None */ }
  ```

- **Defaulted** — `#[prop(default = expr)]`, which supplies `expr` when the caller omits the prop.

  ```rust
  #[component]
  fn Avatar(src: String, #[prop(default = 48)] size_px: u32) -> VNode { /* size_px defaults to 48 */ }
  ```

- **Converting** — `#[prop(into)]`, which accepts any `T: Into<FieldType>` so the caller can pass, for
  example, a `&str` where the prop is a `String`:

  ```rust
  #[component]
  fn Avatar(#[prop(into)] src: String) -> VNode { /* called as src="/a.png" */ }
  ```

- **Reactive** — a prop whose type is a reactive handle (`Signal<T>`, `Memo<T>`). These are `Copy` keys into
  the reactive runtime (`crates/ferric/src/signal.rs`), so passing one into a component is cheap and the
  component stays subscribed: reading it in the body re-renders on change. No special attribute is needed; the
  type carries the reactivity.

  ```rust
  #[component]
  fn Counter(count: Signal<i32>) -> VNode {
      view! { <p>{move || count.get()}</p> }   // re-renders when count changes
  }
  ```

A component with no props is the baseline function component unchanged — `#[component]` is not required for a
zero-prop closure, and when used on a zero-parameter function it generates an empty props type:

```rust
let clock = move || -> VNode { view! { <time>{now()}</time> } };   // still a Component
```

Props are type-checked at compile time against the generated builder. A value of the wrong type for a prop is a
compile error that names the prop and its expected type (§8), not a deferred runtime failure.

---

## 4. Children

A component accepts child content by declaring a parameter named `children` of type `Children`:

```rust
use ferric::prelude::*;

#[component]
fn Card(title: String, children: Children) -> VNode {
    view! {
        <section class="card">
            <h2>{title}</h2>
            <div class="body">{children()}</div>
        </section>
    }
}
```

What the author writes to fill it:

```rust
view! {
    <Card title={"Welcome".into()}>
        <p>"First paragraph."</p>
        <p>"Second paragraph."</p>
    </Card>
}
```

`Children` is an additive type this model introduces (§6): a deferred, reference-counted thunk that produces
the child nodes the caller nested, as a `Vec<VNode>`:

```rust
pub type Children = std::rc::Rc<dyn Fn() -> Vec<VNode>>;
```

Two properties make this lower cleanly onto the frozen surface:

- **It is `Vec<VNode>`, not `VNode`.** A children block may hold several sibling nodes, and the baseline
  `VNode` enum is frozen at two variants (`Element`, `Text`) with no fragment variant — adding one would
  redefine a frozen item, which identity IA4 forbids. Returning `Vec<VNode>` carries multiple roots without
  touching `VNode`, and the component splices them with the existing
  `VElement::children(impl IntoIterator<Item = VNode>)` builder: `view!`'s `{children()}` lowers to
  `.children(children())`.
- **It is deferred (a thunk), not a value.** The component decides *where* and *whether* to render its
  children by calling `children()` at that point in its body. Because the call happens inside the component's
  render, which runs inside the mount effect, any signal the child content reads stays tracked and the children
  re-render on change — consistent with the baseline reactive model.

Children are required by default: a component that declares `children: Children` expects to be given child
content. A component accepts **optional** children by declaring `#[prop(optional)] children: Option<Children>`
and rendering them only when present. A component that declares **no** `children` parameter does not accept
children; nesting content inside it in the `view!` macro is a diagnostic that names the component (§8) — this
is the macro side of the correspondence in §7.

---

## 5. Named slots

Children are one unlabelled region. A component that needs **more than one** labelled region — a header and a
footer around a body, say — declares each region as a typed **slot** field:

```rust
use ferric::prelude::*;

#[component]
fn Page(
    header: Slot,
    #[prop(optional)] footer: Option<Slot>,
    children: Children,
) -> VNode {
    view! {
        <article>
            <header>{header()}</header>
            <main>{children()}</main>
            { footer.map(|f| view! { <footer>{f()}</footer> }) }
        </article>
    }
}
```

What the author writes to fill it:

```rust
view! {
    <Page>
        <slot:header><h1>"Title"</h1></slot:header>
        <p>"Main body — the default children region."</p>
        <p>"Still the body."</p>
        <slot:footer>"© 2026"</slot:footer>
    </Page>
}
```

`Slot` has the same shape as `Children` — a deferred `Rc<dyn Fn() -> Vec<VNode>>` — but is a distinct declared
field the author fills by name (`slot:header`) rather than by nesting bare content. The rules:

- **One region per slot.** Each named slot is filled at most once. Filling a slot the component did not
  declare, or filling one twice, is a diagnostic that names the slot (§8).
- **Required vs optional.** A `Slot` field is required; an `Option<Slot>` field is optional and absent when
  the caller omits it. A missing required slot is a compile-time diagnostic that names the slot.
- **Slots and children coexist.** A component may declare named slots **and** a `children` field; content the
  author nests without a `slot:` label fills `children`, and labelled content fills the matching slot. `Page`
  above does both.

**Parameterized slots (render-prop style)** let a component pass a value *into* the content the caller
provides — the pattern a list that renders a caller-supplied template for each item needs. A parameterized slot
is declared as `Fn(T) -> Vec<VNode>` rather than a zero-argument thunk:

```rust
#[component]
fn List<T: Clone + 'static>(items: Vec<T>, row: SlotFn<T>) -> VNode {
    view! { <ul>{ items.into_iter().map(|it| view! { <li>{row(it)}</li> }).collect::<Vec<_>>() }</ul> }
}
```

where `SlotFn<T> = Rc<dyn Fn(T) -> Vec<VNode>>`. The basic (zero-argument) named slot is part of the early
floor; parameterized slots are a 1.0 enhancement (staged `one_oh` below), since a real app can be built with
plain named slots and a parameterized slot can always be expressed as a child that is a closure in the interim.

---

## 6. The additive types, and how the model lowers onto the frozen surface

The model introduces exactly these items, all additive — none redefines a frozen item, satisfying identity
IA4:

| New item | Shape | Role |
|---|---|---|
| `#[component]` | attribute macro on `fn(..) -> VNode` | Generates the props type, the builder, and the `Component` impl. |
| `<Name>Props` + its builder | generated struct + builder, one field/setter per prop | The typed, compile-time-checked declaration surface the `view!` macro fills. |
| `#[prop(optional)]` / `#[prop(default = ..)]` / `#[prop(into)]` | field attributes | Mark a prop optional, defaulted, or converting. |
| `Children` | `Rc<dyn Fn() -> Vec<VNode>>` | Deferred, reactive child content. |
| `Slot` | `Rc<dyn Fn() -> Vec<VNode>>` | One named, deferred, reactive content region. |
| `SlotFn<T>` | `Rc<dyn Fn(T) -> Vec<VNode>>` | A parameterized slot (render-prop). |

How each construct reaches the baseline:

- A **component invocation** `<Name .. />` in child position lowers to: build `NameProps` through its builder,
  construct the component value, and call `Component::render(&value)` — the **frozen trait method** — to get
  one `VNode`, which is appended to the enclosing element with the existing `.child(..)`. Several component
  invocations among siblings each contribute their one `VNode`.
- **Props** become fields of the generated struct; a required field with no default makes the builder's
  `build()` ill-typed until set (the mechanism behind the missing-prop diagnostic, §8).
- **Children / slots** are captured as `Rc<dyn Fn() -> Vec<VNode>>` thunks and spliced where the component
  calls them with the baseline `.children(..)` / `.child(..)` builders.
- **Reactivity** rides entirely on the baseline: components render inside the mount effect, props that are
  signals are read live, and no new reactive machinery is added here (context's interaction with the reactive
  owner scope is owned by part C, `REQ-API-060..079`, and is out of this band).

No new `prelude` export is required for the model to work, but the model intends `Component` (already frozen)
plus the additive `#[component]`, `Children`, and `Slot` to be brought into scope the same way; whether they
join the `prelude` is a packaging decision the synthesis and release areas settle, constrained to additive-only
(parent `REQ-FW-009`).

---

## 7. Composition, and the escape hatch

Composition is nesting: a component is placed in another's body, filled through its declared props, children,
and slots. Because every component — generated or hand-written — is a `Component` that renders to one `VNode`,
and `VNode`s nest through `VElement.children`, composition needs no new rule beyond the lowering in §6.

```rust
#[component]
fn Dashboard(user: Signal<User>) -> VNode {
    view! {
        <Page>
            <slot:header><Greeting name={user.get().name} /></slot:header>
            <Card title={"Activity".into()}>
                <List items={user.get().events} row={Rc::new(|e| view! { <span>{e.label}</span> })} />
            </Card>
        </Page>
    }
}
```

`Dashboard` fills `Page`'s header slot with a `Greeting` component and its body with a `Card` that itself holds
a `List`. Each inner component is invoked through the same declared surface a leaf caller uses; there is no
special "container component" concept. A **layout component** that forwards content is just a component that
declares `children` (or slots) and renders them in a wrapper, as `Card` and `Page` do.

**The escape hatch keeps the model from locking anyone in.** `#[component]` is sugar; a component can always be
written by hand against the frozen trait, and the two forms interoperate:

```rust
struct Clock { tz: String }
impl Component for Clock {
    fn render(&self) -> VNode { view! { <time>{now_in(&self.tz)}</time> } }
}
// and the baseline bare closure remains a Component unchanged:
let spacer = || -> VNode { VElement::new("hr").into() };
```

A hand-written `impl Component` and a bare `Fn() -> VNode` compose with generated components freely, because all
three are the same frozen trait. The baseline's object-safe dynamic dispatch (`&dyn Component`,
`Box<dyn Component>`; `crates/ferric/src/component.rs` tests exercise it) is carried forward: a component may
hold `Box<dyn Component>` children where the concrete set is dynamic. Nothing in this model removes or narrows
that.

---

## 8. Diagnostics (the testable failure bar — IA6, parent `REQ-FW-014`)

A declared, type-checked surface is only worth having if getting it wrong points at the author's code. The
model commits to a `trybuild`-checkable diagnostics bar for the common component mistakes. Each case below is a
stated compile-fail fixture whose message names the author's error in terms of their code, not framework
internals:

| Author mistake | Required diagnostic (names the author's code) |
|---|---|
| Omit a required prop | Error names the missing prop and the component — e.g. "missing required prop `name` on `Greeting`" — not a raw builder-state type error. |
| Pass a prop of the wrong type | Error names the prop and the expected type — "prop `size_px` on `Avatar` expects `u32`". |
| Pass a prop the component does not declare | Error names the unknown prop and the component — "`Avatar` has no prop `widht`" (typo case). |
| Nest children in a component with no `children` field | Error states the component does not accept children. |
| Fill a slot the component did not declare, or fill one twice | Error names the slot and the component. |
| Omit a required slot | Error names the missing slot. |

The acceptance of each is a `trybuild` fixture (a `.rs` that must fail to compile with a stated message
substring); the diagnostics quality of the `view!` macro itself (malformed element trees) is owned by part A.
This section owns the component-declaration diagnostics above.

---

## 9. The component side of the invocation seam (IA2)

Identity IA2 (`../contracts/req_api_partition.yaml`) requires that every way the `view!` macro passes a prop, a
child, or a named slot to a component corresponds to a declaration form this model defines, and that every
declaration form is reachable from the macro — no orphan on either side. This section states the
component-declaration side of that correspondence; the macro-passing side is owned by part A, and the synthesis
gate checks the two sides close.

| Macro-side passing form (part A owns the grammar) | Component-side declaration form (this model) | Closure |
|---|---|---|
| Attribute `name=value` on a component element | A prop: a `#[component]` fn parameter → a generated builder setter → a props-struct field (§3) | Every attribute resolves to one setter; every declared prop has one setter reachable as an attribute. |
| Attribute omitted | An optional (`#[prop(optional)]` → `None`) or defaulted (`#[prop(default=..)]`) prop; or a compile error if the prop is required (§3, §8) | Omission is defined for every prop: it defaults or it is a named diagnostic. |
| `name={expr}` where `expr` is a `Signal`/`Memo` | A prop whose declared type is that reactive handle (§3, reactive props) | Reactive values pass as ordinary props; no separate passing form. |
| Bare content nested inside `<Comp>…</Comp>` | A `children: Children` (or `Option<Children>`) field (§4) | Nesting corresponds to the `children` field; a component with no such field makes nesting a diagnostic. |
| `<slot:label>…</slot:label>` inside a component element | A named slot field `label: Slot` (or `Option<Slot>`) (§5) | Every `slot:label` resolves to a declared slot or is a diagnostic; every declared slot is fillable by its label. |
| A component element in child position, `<Comp/>` | The component's `Component::render` output, one `VNode`, spliced via `.child(..)` (§6) | Every component invocation lowers to a `VNode`; every component is invocable. |

The rule the gate asserts: **no macro-side passing form without a component-side declaration form, and no
declaration form unreachable from the macro.** The table above is closed in both directions — every macro form
has a declaration counterpart, and every declaration form (`required/optional/defaulted/into/reactive` prop,
`children`, named `slot`, component invocation) is reachable from a macro form.

---

## 10. Where this sits among its peers (named comparison)

The props/children/slots designs of the Rust peers, and where Ferric's lands relative to each:

- **Leptos** — `#[component]` on a function whose parameters are props; `#[prop(optional)]`, `#[prop(default =
  ..)]`, `#[prop(into)]` attributes; a generated builder; `children: Children` as a callable producing a view;
  named slots via a `#[slot]` struct. Ferric's design is closest to Leptos and adopts its attribute vocabulary
  directly, because Leptos is the signal-reactive Rust framework whose props ergonomics are the most refined
  and the model Ferric's reactivity most resembles. Ferric diverges only in not requiring `PartialEq`-based
  memoization (§2), which Leptos also avoids for the same signal-reactive reason.
- **Sycamore** — `#[component]` with a `Props`-deriving struct; `children: Children`; a smaller surface than
  Leptos. Ferric matches Sycamore's "props are a typed struct" center and, like it, keeps the surface small;
  the trade-off Sycamore accepts is more explicit builder/struct authoring, which Ferric's generated builder
  hides.
- **Dioxus** — `#[component]` plus `#[derive(Props)]` with `#[props(default)]`/`#[props(optional)]`; `children:
  Element`; render-props for the parameterized case. Dioxus is a React-style VDOM and diffs props, so it leans
  on props `PartialEq`; Ferric does not need that because change detection is signal-based (§2). Ferric borrows
  Dioxus's render-prop shape for parameterized slots (`SlotFn<T>`, §5).
- **Yew** — `#[derive(Properties, PartialEq)]` on a props struct passed to a `#[function_component]`;
  `children: Children`/`Html`; the `PartialEq` bound is mandatory because Yew re-renders by comparing props.
  Ferric deliberately drops the mandatory `PartialEq` (§2); this is the sharpest divergence and it follows from
  Ferric pairing a VDOM with fine-grained signals rather than relying on prop-diffing for change detection.

The ergonomic trade-off against Rust's type system: Rust has no named or defaulted function
arguments, so *some* generated surface (a struct + builder) is unavoidable to get optional, defaulted, and
named props — every peer above generates one. The cost every peer pays, and Ferric with them, is macro-
generated code whose compile errors can read in terms of generated types rather than the author's call; §8 is
the commitment to pay that cost down with a diagnostics bar rather than leave it. The one design choice
left — whether props must be `PartialEq` — Ferric answers "no" on the strength of its existing reactive
runtime, which follows directly from the architecture the baseline already fixed.

---

## 11. Requirements register — `REQ-API-030..059`

Band `030..059` is this spoke's (identity IA1). Ids are zero-padded 3-digit and monotonic within the band; ids
`053..059` are left unused as headroom. Every acceptance criterion uses a `verification_method` from the
inherited vocabulary (`automated_test` | `example_build` | `doc_inspection`;
`../../contracts/id_and_traceability_schema.yaml`). Each entry specializes parent `REQ-FW-005` (declarative
authoring) and, for the diagnostics entries, parent `REQ-FW-014` (actionable diagnostics); stability for A3 is
parent `REQ-FW-010` (read-only cross-references).

### A. Typed props

#### REQ-API-030 — A component declares typed props as a `#[component]` function's parameters
- **Statement:** An author declares a component as `#[component] fn Name(..) -> VNode`, whose parameters are
  its typed props; the attribute generates a typed props type and a builder the `view!` macro fills.
- **Rationale:** A declared, type-checked props surface is what makes a component reusable by a caller other
  than its author (A3, parent `REQ-FW-005`); every Rust peer generates one because Rust lacks named/defaulted
  function arguments.
- **Acceptance criteria:** A stated `#[component]` with two props compiles, and `view!`-invoking it with both
  props set renders the described UI. **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true · **References:** parent `REQ-FW-005`.

#### REQ-API-031 — Required props must be supplied
- **Statement:** A prop declared with no default and no `optional` must be supplied by the caller.
- **Rationale:** Required inputs a component cannot render without must be enforced at the call site, not
  defaulted silently.
- **Acceptance criteria:** A snippet supplying every required prop builds and renders; the omission case is
  covered by REQ-API-050. **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true.

#### REQ-API-032 — Optional props default to absent
- **Statement:** A prop marked `#[prop(optional)]` has type `Option<T>` and defaults to `None` when the caller
  omits it.
- **Rationale:** Real components have inputs a caller may legitimately not provide; optional props express that
  without a sentinel value.
- **Acceptance criteria:** A stated component with an optional prop compiles and renders both when the prop is
  supplied and when it is omitted (the omitted case observably takes the `None` branch).
  **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true.

#### REQ-API-033 — Defaulted props take a declared default
- **Statement:** A prop marked `#[prop(default = expr)]` takes `expr` when the caller omits it.
- **Rationale:** Many props have a sensible default; defaulting at declaration keeps call sites terse and keeps
  the default in one place.
- **Acceptance criteria:** A stated component with a defaulted prop renders with the default when the prop is
  omitted and with the supplied value when present. **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true.

#### REQ-API-034 — Converting props accept `Into` conversions
- **Statement:** A prop marked `#[prop(into)]` accepts any `T: Into<FieldType>`, so a caller may pass, for
  example, a `&str` where the prop is a `String`.
- **Rationale:** Without it, callers litter call sites with `.into()` / `.to_string()`; the conversion belongs
  at the declaration, as in Leptos.
- **Acceptance criteria:** A stated component with an `into` `String` prop compiles when called with a `&str`
  literal and renders the described UI. **Verification:** `example_build`.
- **Stage:** one_oh · **Release gating:** true · **References:** Leptos `#[prop(into)]`.

#### REQ-API-035 — Props may be reactive handles
- **Statement:** A prop whose type is a `Signal<T>` or `Memo<T>` passes the reactive handle; reading it in the
  component body re-renders the parts that read it when it changes, with no props-equality check.
- **Rationale:** Fine-grained reactivity is the baseline's model (`signal.rs`); passing signals as props is how
  a parent shares live state with a child without the child re-rendering wholesale.
- **Acceptance criteria:** A headless test mounts a component taking a `Signal<i32>` prop, changes the signal,
  and observes the rendered DOM update in place. **Verification:** `automated_test` (headless
  `wasm-bindgen-test`).
- **Stage:** usable_early · **Release gating:** true · **References:** baseline `signal.rs`.

#### REQ-API-036 — Props do not require `PartialEq`
- **Statement:** Declaring and using props does not require the prop types to implement `PartialEq`; change
  detection is signal-based, not prop-diff-based.
- **Rationale:** Ferric pairs a VDOM with fine-grained signals; unlike Yew/Dioxus it need not compare props to
  decide re-render, so it must not impose the bound those frameworks require.
- **Acceptance criteria:** A stated component whose prop type does not implement `PartialEq` compiles and
  renders. **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true · **References:** contrast Yew `#[derive(Properties,
  PartialEq)]`.

#### REQ-API-037 — A zero-prop component needs no props struct
- **Statement:** A component with no props is the baseline function component unchanged; `#[component]` is not
  required for a bare `Fn() -> VNode`, and when applied to a zero-parameter function it generates an empty
  props type.
- **Rationale:** The frozen `Component` blanket impl over `Fn() -> VNode` must keep working; the model adds to
  it and takes nothing away (parent `REQ-FW-009`).
- **Acceptance criteria:** The baseline `counter` example's bare closure still compiles and renders as a
  `Component` at 1.0; a stated zero-prop `#[component]` also compiles and renders. **Verification:**
  `example_build`.
- **Stage:** usable_early · **Release gating:** true · **References:** parent `REQ-FW-009`; baseline
  `component.rs`.

### B. Children

#### REQ-API-038 — A component accepts children via a `Children` prop
- **Statement:** A component declares it accepts child content by a parameter `children: Children`; `Children`
  is a deferred `Rc<dyn Fn() -> Vec<VNode>>` the component calls where it places the children.
- **Rationale:** Wrapper and layout components (cards, panels, list containers) need to receive and place
  caller content; children are the unlabelled form of that.
- **Acceptance criteria:** A stated `Card`-style component declaring `children: Children` renders caller-nested
  content at the point it calls `children()`; a multi-node children block renders all its nodes.
  **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true · **References:** parent `REQ-FW-005`.

#### REQ-API-039 — Children lower onto `VElement.children` additively and stay reactive
- **Statement:** `{children()}` lowers onto the baseline `VElement::children(impl IntoIterator<Item = VNode>)`
  builder; because the component renders inside the mount effect, signals read within the child content stay
  tracked and the children re-render on change.
- **Rationale:** Children must compose with the frozen view tree without a new `VNode` variant (IA4) and must
  not break reactivity.
- **Acceptance criteria:** A headless test mounts a component whose children read a signal, changes the signal,
  and observes the children update in place; the children block produces the same `VElement.children` a
  hand-built tree would. **Verification:** `automated_test`.
- **Stage:** usable_early · **Release gating:** true · **References:** baseline `vdom.rs`
  (`VElement::children`); IA4.

#### REQ-API-040 — Optional children
- **Statement:** A component accepts children optionally by declaring `#[prop(optional)] children:
  Option<Children>` and renders them only when present.
- **Rationale:** Some components render child content only in some states; optional children express that
  without requiring every caller to pass content.
- **Acceptance criteria:** A stated component with optional children renders correctly both with and without a
  children block. **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true.

### C. Named slots

#### REQ-API-041 — A component declares named slots as typed fields
- **Statement:** A component that needs more than one labelled content region declares each as a `Slot` field
  (`Rc<dyn Fn() -> Vec<VNode>>`); the author fills each by its label.
- **Rationale:** A single `children` region cannot express a header/body/footer layout; named slots give each
  region an identity the caller fills by name.
- **Acceptance criteria:** A stated `Page`-style component with `header` and `footer` slots renders the
  author's labelled content in the matching regions. **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true · **References:** parent `REQ-FW-005`.

#### REQ-API-042 — Each named slot is filled at most once
- **Statement:** A named slot is filled once; filling a slot a component did not declare, or filling one twice,
  is a compile-time diagnostic (see REQ-API-052).
- **Rationale:** A slot names a single region; a double or unknown fill is an author error that must be caught,
  not silently last-wins.
- **Acceptance criteria:** A single correct fill per slot builds and renders; the error cases are covered by
  REQ-API-052. **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true.

#### REQ-API-043 — Required vs optional slots
- **Statement:** A `Slot` field is required; an `Option<Slot>` field is optional and absent when omitted.
- **Rationale:** Some regions a component cannot render without (a required `header`); others are optional (a
  `footer`). The type expresses which.
- **Acceptance criteria:** A stated component renders with an optional slot both filled and omitted; the
  missing-required-slot case is covered by REQ-API-052. **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true.

#### REQ-API-044 — Named slots and children coexist
- **Statement:** A component may declare named slots and a `children` field together; unlabelled nested content
  fills `children`, labelled content fills the matching slot.
- **Rationale:** The common layout — named regions plus a default body — needs both in one component.
- **Acceptance criteria:** A stated component with `header`/`footer` slots and a `children` body renders
  labelled content in its regions and unlabelled content in the body, from one `view!` block.
  **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true.

#### REQ-API-045 — Parameterized slots (render-prop)
- **Statement:** A slot declared as `SlotFn<T>` (`Rc<dyn Fn(T) -> Vec<VNode>>`) lets a component pass a value
  into the caller-provided content, so the caller can render a template per item.
- **Rationale:** A generic list or table component renders caller-controlled markup for each row; the value
  (the row datum) must flow from component to caller content.
- **Acceptance criteria:** A stated generic `List<T>` component takes a `SlotFn<T>`, is called with a per-item
  template, and renders one templated row per item. **Verification:** `example_build`.
- **Stage:** one_oh · **Release gating:** true · **References:** Dioxus render-props.

### D. Composition

#### REQ-API-046 — Components compose by nesting through their declared surface
- **Statement:** A component is invoked as an element in another component's `view!` body, filled through its
  declared props, children, and slots; the invocation lowers to its `Component::render` output spliced into the
  parent as a `VNode`.
- **Rationale:** Composition is the point of a component model; nesting through the declared surface is what
  lets A3's components be assembled by A2 (parent `REQ-FW-005`, `REQ-FW-008`).
- **Acceptance criteria:** A stated multi-level composition (a component holding another component in a slot and
  a third in its children) compiles and renders the combined UI. **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true · **References:** parent `REQ-FW-005`.

#### REQ-API-047 — Composition is additive over the frozen `Component`/`VNode` surface
- **Statement:** Generated components, hand-written `impl Component`, and bare `Fn() -> VNode` closures are all
  the frozen `Component` trait and compose with one another; no frozen item (`Component`, `VNode`, `VElement`,
  `prelude`) is redefined.
- **Rationale:** The baseline froze these surfaces and apps are written against them (parent `REQ-FW-009`, IA4);
  the model must extend, never break, them.
- **Acceptance criteria:** A stated composition mixes a `#[component]`, a hand-written `impl Component`, and a
  bare closure in one tree and renders; an app written against the baseline component surface still compiles at
  1.0. **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true · **References:** parent `REQ-FW-009`; IA4; baseline
  `component.rs`, `lib.rs`.

#### REQ-API-048 — The declaration macro is a removable escape-hatch sugar
- **Statement:** `#[component]` is sugar over `Component`; any component can be written by hand against the
  trait, and hand-written and generated components interoperate. There is no construct reachable only through
  the macro.
- **Rationale:** A3 must not be locked into the macro; an escape hatch to the plain trait keeps the model from
  being a dead end when the macro does not fit.
- **Acceptance criteria:** A stated component is written once with `#[component]` and once as a hand-written
  `impl Component`, and both are used interchangeably at a call site. **Verification:** `example_build`.
- **Stage:** usable_early · **Release gating:** true.

#### REQ-API-049 — Dynamic-dispatch composition is carried forward
- **Statement:** The baseline's object-safe `Component` dispatch (`&dyn Component`, `Box<dyn Component>`)
  remains available, so a component may hold a dynamic set of child components.
- **Rationale:** The baseline supports and tests trait-object components; dynamic children (a list of
  heterogeneous components chosen at runtime) depend on it.
- **Acceptance criteria:** A stated component holding `Vec<Box<dyn Component>>` renders each; the baseline
  trait-object test still passes at 1.0. **Verification:** `automated_test`.
- **Stage:** one_oh · **Release gating:** true · **References:** baseline `component.rs`
  (`trait_object_component_renders`).

### E. Diagnostics (specializing parent `REQ-FW-014`)

#### REQ-API-050 — Missing or mistyped required prop is an actionable diagnostic
- **Statement:** Omitting a required prop, or passing a prop of the wrong type, produces a compile-time
  diagnostic naming the prop, the component, and (for a type mismatch) the expected type — not a raw
  generated-builder type error.
- **Rationale:** The daily experience of the component model is its errors; opaque builder-state errors are a
  top reason authors abandon Rust frontends (parent `REQ-FW-014`).
- **Acceptance criteria:** `trybuild` fixtures for (a) a missing required prop and (b) a wrong-typed prop fail
  to compile with a message naming the prop and component (and expected type for (b)). **Verification:**
  `automated_test` (`trybuild`).
- **Stage:** usable_early · **Release gating:** true · **References:** parent `REQ-FW-014`.

#### REQ-API-051 — Unknown prop is an actionable diagnostic
- **Statement:** Passing a prop the component does not declare produces a compile-time diagnostic naming the
  unknown prop and the component.
- **Rationale:** Typos and stale call sites are common; naming the unknown prop (and not a generic "no such
  field") is what makes the fix obvious.
- **Acceptance criteria:** A `trybuild` fixture passing an undeclared prop fails with a message naming the
  unknown prop and the component. **Verification:** `automated_test` (`trybuild`).
- **Stage:** usable_early · **Release gating:** true · **References:** parent `REQ-FW-014`.

#### REQ-API-052 — Children and slot misuse are actionable diagnostics
- **Statement:** Nesting children in a component with no `children` field, filling an undeclared slot, filling a
  slot twice, or omitting a required slot each produces a compile-time diagnostic naming the component and the
  offending region.
- **Rationale:** The children/slot surface needs the same diagnostic quality as props; silent acceptance or an
  opaque error defeats the point of declaring slots.
- **Acceptance criteria:** `trybuild` fixtures for (a) children on a childless component, (b) an undeclared slot
  fill, (c) a double slot fill, and (d) a missing required slot each fail with a message naming the component
  and the region. **Verification:** `automated_test` (`trybuild`).
- **Stage:** usable_early · **Release gating:** true · **References:** parent `REQ-FW-014`.

### Register summary

- Band `030..059`; ids `030..052` assigned, `053..059` reserved headroom (monotonic, IA1).
- Stage split: `usable_early` — 030, 031, 032, 033, 035, 036, 037, 038, 039, 040, 041, 042, 043, 044, 046, 047,
  048, 050, 051, 052; `one_oh` — 034, 045, 049. All `release_gating: true` (no post-1.0 deferrals in this
  band).
- Verification split: `example_build` (030–034, 036, 037, 038, 040, 041, 042, 043, 044, 045, 046, 047, 048),
  `automated_test` (035, 039, 049, 050, 051, 052), `doc_inspection` (none in this band — the model's
  documentation obligation is carried by the consolidated `authoring-model.md` and owned by docs & DX,
  `REQ-DX-*`).

---

## Metadata

- **Owning task:** `SUBTASK_components_props_slots` (owns `REQ-API-030..059`, identity IA1).
- **Folds into:** `../authoring-model.md` at synthesis (`SUBTASK_synthesis`), merged into one `REQ-API-*`
  register.
- **Conforms to:** `../contracts/req_api_partition.yaml` (band 030–059, invocation seam IA2),
  `../contracts/_MANIFEST.yaml` (identities IA1/IA2/IA4/IA6), `../../contracts/id_and_traceability_schema.yaml`
  (REQ fields, verification vocabulary, stage vocabulary, `release_gating`).
- **Grounded in:** Ferric baseline at `taskflow/dags/ferric-foundation/checkout/crates/ferric/` —
  `component.rs` (`Component`, `Fn() -> VNode`), `vdom.rs` (`VNode`, `VElement`, `.child`/`.children`,
  `EventKind`), `signal.rs` (`Signal`/`Memo`, reactive effect model), `lib.rs` (frozen `prelude`),
  `examples/counter.rs`.
- **Peers compared by name:** Leptos (`#[component]`/`#[prop]`), Sycamore (`#[component]`/`Props`), Dioxus
  (`#[derive(Props)]`/render-props), Yew (`#[derive(Properties, PartialEq)]`).
- **Specializes (read-only):** parent `REQ-FW-005` (declarative authoring), `REQ-FW-009` (frozen surfaces),
  `REQ-FW-010` (stable API for A3), `REQ-FW-014` (diagnostics).
- **Seam owned here:** the component-declaration side of IA2; the macro-passing side is owned by
  `SUBTASK_view_macro` (`REQ-API-001..029`).
