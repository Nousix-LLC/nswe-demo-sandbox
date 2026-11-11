# Ferric 1.0 — The authoring model

This is the Ferric 1.0 **authoring model**: what an app author writes to build real UI, and the testable bar
each authoring construct must meet. It covers three parts of one surface — the declarative `view!` macro, the
component model (typed props, children, named slots, composition), and context for sharing state down the tree
— and folds them into one register of `REQ-API-001 … REQ-API-070` acceptance criteria.

It is **design, not framework code**. Every requirement states *what the author writes and what must hold* — a
surface they call, a build that succeeds, a diagnostic that fires — not how the proc-macro expands or how the
lookup is implemented. Those are questions for the code DAG that builds this. This document specializes three
framework-level requirements from `scope-and-requirements.md`: `REQ-FW-005` (a declarative authoring model),
`REQ-FW-009` (additive over the frozen surface), and `REQ-FW-014` (actionable diagnostics). It owns the
`REQ-API-*` register (parent identity I1).

**Grounding.** Every claim about today's Ferric is read from the baseline checkout at
`taskflow/dags/ferric-foundation/checkout/crates/ferric/` (`Nousix-LLC/nswe-demo` @ `276138f`): `src/vdom.rs`
(the `VNode`/`VElement` builders and the keyed `diff`), `src/component.rs` (`Component` / `Fn() -> VNode`),
`src/signal.rs` (`Signal`/`Memo`/`create_effect`/`ReactiveScope` owner tree), `src/dom.rs` (`mount`),
`src/lib.rs` (the frozen `prelude`), and `examples/counter.rs`. Peer frameworks (Leptos, Sycamore, Dioxus, Yew;
Solid and Vue 3 as analogs) are compared by name from their documented public behavior.

---

## 1. What the authoring model replaces, and the one fact that shapes all of it

An author today composes a view tree by hand. The counter example is the whole baseline authoring surface in
miniature:

```rust
// examples/counter.rs (baseline, verbatim shape)
let count = create_signal(0i32);
let app = move || -> VNode {
    VElement::new("div")
        .attr("class", "counter")
        .child(
            VElement::new("button")
                .on(EventKind::Click, move || count.update(|n| *n += 1))
                .child(text("increment")),
        )
        .child(VElement::new("p").child(text(format!("count: {}", count.get()))))
        .into()
};
mount(root, app);
```

There is no template macro, no way for a component to declare what it accepts, and no way to share a value down
a subtree without threading it through every call. The authoring model closes those three gaps. Everything it
adds is sugar over the baseline: it produces the same `VNode`, drives the same `Component` trait, and rides the
same reactive runtime. Nothing below adds a runtime capability the builders lack.

### 1.1 The reactivity model, stated once up front

One baseline fact governs how the macro, reactive props, and reactive context all behave, so it is stated here
rather than three times: **Ferric's reactivity is coarse-grained.** `mount` wraps the entire component render
in one `create_effect` (`src/dom.rs`). Every `Signal`/`Memo` read anywhere in a render subscribes that single
effect; a later write re-runs the **whole** render, and the keyed `diff` computes a minimal patch applied to the
live DOM. Ferric has no fine-grained per-node DOM binding.

This is the virtual-DOM model Ferric shares with Yew, Dioxus, and Vue 3 — not the fine-grained-signal model of
Leptos, Sycamore, and Solid, where an interpolation updates exactly one text node without re-running the
component. An author arriving from Leptos will assume fine-grained behavior and must be told otherwise up front:
a signal read in a view re-renders the component and the keyed diff reconciles the result. The three sections
below each inherit this fact — an interpolated `{count.get()}`, a `Signal<T>` prop, and a `Signal<T>` carried
through context all propagate change the same way, by the component re-rendering when a signal it read changes.
The performance cost of that model is measured by `REQ-PERF-*`, not claimed away here.

---

## 2. The `view!` macro — elements, attributes, events, control flow, lists

An author writes a `view!` macro instead of builder chains. The counter, rewritten:

```rust
let count = create_signal(0i32);
let app = move || view! {
    <div class="counter">
        <button on:click={move || count.update(|n| *n += 1)}>"increment"</button>
        <p>"count: " {count.get()}</p>
    </div>
};
mount(root, app);
```

Ferric adopts an **HTML/JSX-style** flavor — angle-bracket tags with brace-delimited Rust interpolation — in
the family of Leptos's `view!` and Yew's `html!`. The flavor is a deliberate trade-off, not a verdict (§6
compares the alternatives): angle brackets read like the HTML an author already knows and make the open/close
tree visible, which suits a framework whose mental model is "a tree that re-renders." Sycamore's terse
`div { .. }` and Dioxus's struct-style `rsx!` are quieter and more Rust-native but read less like markup; the
brief names a `view!`/JSX-style macro and the HTML-like flavor is the better fit for an author weighing Ferric
against the JS frameworks it competes with. The flavor is a surface choice; the lowering in §2.7 is independent
of it.

### 2.1 Elements, text, and attributes

- **Elements.** `<tag> … </tag>` and self-closing `<tag/>`. A lowercase tag is an HTML element; a capitalized
  tag is a component invocation (§3.5).
- **Text.** A string literal is a text node: `<p>"hello"</p>`. Text is written quoted (as in Sycamore and Yew's
  expression blocks) so the macro never has to guess where markup ends and prose begins — this removes a class
  of whitespace ambiguity (§2.8) and is the cost of the HTML-like flavor.
- **Attributes.** `name="literal"` for a static value, `name={expr}` for a dynamic one, with names written as
  they appear on the element (`class`, `id`, `href`). Baseline attributes are `(String, String)` pairs, so a
  dynamic value must be `impl Into<String>`; a non-string value is converted explicitly by the author
  (`width={n.to_string()}`) rather than silently stringified, which keeps formatting in the author's hands and
  gives the macro a precise place to point a diagnostic (§2.6).

### 2.2 Event handlers, and the open event set

A handler is written `on:<name>={closure}` and lowers to `.on(EventKind::<Variant>, closure)`:

```rust
view! { <button on:click={move || count.update(|n| *n += 1)}>"+"</button> }
```

Two baseline facts shape this. First, **handlers are zero-argument today**: the frozen `EventHandler` is
`Rc<dyn Fn()>`, so the closure takes no arguments (the DOM layer receives and discards the `web_sys::Event`). An
event-payload-carrying handler form is an additive refinement owned by `REQ-ASYNC-*`; this model names the seam
and defers the form rather than inventing an event-argument signature the frozen `EventHandler` does not have.
Second, **the event-name → `EventKind` mapping is open**: `on:click` and `on:input` resolve today, and as
`REQ-ASYNC-*` extends `EventKind` (submit, keydown, focus, …) those names resolve with no change to the macro
grammar. A name with no matching variant is a compile diagnostic (§2.6), not a silently dropped handler.

### 2.3 Interpolated reactive values

A `{expr}` in child position evaluates a Rust expression during the component's render:

```rust
view! { <p>"count: " {count.get()}</p> }   // reads `count` each render
```

Because the whole render runs inside one effect (§1.1), reading `count` here subscribes that effect, so a later
`count.set(..)` re-renders the component and the keyed diff patches the changed text in place — the same
mechanism the hand-built counter already relies on, with the `text(format!(..))` boilerplate removed. A plain
read needs no `move ||` wrapper to be reactive, because the read already happens inside the render effect. A
`{move || …}` *closure* interpolation is reserved as the additive seam for any future fine-grained binding; 1.0
provides none and the design does not imply one. A text interpolation whose value is not already a string is
written `{format!("count: {}", n)}` or `{n.to_string()}`; the bare `{expr}` text form accepts any
`impl Into<String>`.

### 2.4 Control flow — conditionals

A Rust `if` / `match` / ternary in interpolation position yields a `VNode`:

```rust
view! {
    <div>
        { if signed_in.get() {
              view! { <span class="who">{user.get()}</span> }
          } else {
              view! { <a href="/login">"sign in"</a> }
          } }
    </div>
}
```

Two notes from the baseline diff. `VNode` has no null variant, so a branch that renders nothing yields an empty
text node; the macro provides an explicit empty-node form so the author does not reach for an ad-hoc `text("")`,
and both branches in child position always produce a `VNode`. And when branches differ in node kind
(element↔text) or tag (`<span>` vs `<a>`), the diff emits a wholesale `Replace` at that position rather than an
in-place patch (baseline `diff_node`); the design states this so the author understands that toggling between
two different elements rebuilds that subtree.

### 2.5 Lists and keys

Keyed reconciliation is the baseline's one non-trivial list behavior, with a hard precondition: the keyed-diff
path engages **only** when every sibling is a keyed element on both the old and new sides (`diff_children` uses
the keyed path only when `all_keyed(old) && all_keyed(new)`). A single unkeyed sibling drops the whole parent's
child list to a positional diff. The list form is designed to make a fully-keyed sibling list the default, in
the spirit of Leptos's `<For each key>`:

```rust
view! {
    <ul>
        <For each={todos.get()} key={|t| t.id.to_string()} let:todo>
            <li>{todo.label.clone()}</li>
        </For>
    </ul>
}
```

This lowers to a `Vec<VNode>` in which every element carries its key, spliced into the parent via `.children(..)`
(§2.7). Because the key is part of the form rather than an afterthought, the produced list satisfies `all_keyed`,
so inserts, moves, and removes reconcile by identity (the baseline `keyed_children_*` behavior). The key
expression yields the baseline `Key` (`= String`). Guidance the form carries: do not mix a keyed list with
unkeyed static siblings under one parent (one unkeyed `<li>` drops the whole `<ul>` to positional diffing); let
the list be the sole content of its container, or key the static siblings too. A plain
`{iter.map(..).collect::<Vec<_>>()}` splice is supported for the advanced case, with the same keying
responsibility on the author, and a standalone `key={expr}` lowers to `.key(expr)` for hand-rolled lists.

### 2.6 Compile-time diagnostics (the `trybuild`-checkable bar)

Much of a macro's day-to-day feel is what happens when the author gets it wrong (`REQ-FW-014`). The bar is that
a malformed view produces an error that names the author's mistake **in terms of their code**, at the span of
the offending tokens, rather than a wall of internal macro errors — and the whole bar is checkable with
`trybuild` (a fixture of malformed views, each with a committed expected `stderr`).

| Author mistake | Expected diagnostic (at the author's span) |
|---|---|
| Unclosed element — `<div>` with no `</div>` | "unclosed element `<div>`" pointing at the open tag |
| Mismatched close — `<div> … </span>` | "closing tag `</span>` does not match open tag `<div>`" |
| Multiple top-level nodes in one `view!` | "a `view!` must have a single root element; wrap these in one element" |
| Dynamic attr / text value not `Into<String>` | type error at the `{expr}` span, naming the required `Into<String>` |
| Unknown event name — `on:klick=` | "unknown event `klick`; bound events are: click, input" (the list grows with `EventKind`) |
| Handler value is not a closure | "`on:click` expects a handler closure" at the value span |
| `<For>` item without a key | "list item needs `key={…}` for keyed reconciliation" at the item (best-effort) |
| Capitalized tag with no such component in scope | the ordinary "cannot find `TodoList` in this scope" at the tag span |

Two limits the bar states rather than oversells. Keyless-list detection is **best-effort**: the macro flags a
missing `key` on the direct `<For>` form, where the item element is syntactically visible, but cannot catch
every keyless list built by an arbitrary `{iter.map(..)}` expression, because those elements are produced by
opaque Rust the macro does not see into — for that case the bar is the documented convention plus the `<For>`
form, not a guarantee. And there are **no handler-identity diagnostics**: the runtime cannot compare closures
(the diff emits `SetEvents` only when the set of bound `EventKind`s changes), so the macro promises nothing about
handler equality, only that the handler lowers to a `.on(kind, closure)` call.

### 2.7 Lowering onto `VNode` (what the macro produces)

The macro is defined by the tree it produces — stated as *what it produces*, not how the expansion is written.
Every row lowers onto a frozen constructor; no frozen item is redefined (IA4, `REQ-FW-009`):

| Author writes | Lowers to (the `VNode` it produces) |
|---|---|
| `<div> … </div>` / `<br/>` | `VElement::new("div").children([ … ])` / `VElement::new("br")` |
| `"text"` | `vdom::text("text")` |
| `{expr}` in child position (`expr: Into<String>`) | `vdom::text(expr)` |
| `{expr}` in child position (`expr: VNode`) | the `VNode` itself, spliced as a child |
| `{vec}` / `<For …>` in child position | the `Vec<VNode>`, appended via `.children(vec)` |
| `name="v"` / `name={e}` | `.attr("name", v)` / `.attr("name", e)` (`e: Into<String>`) |
| `key={e}` | `.key(e)` (`e: Into<Key>`, `Key = String`) |
| `on:click={h}` / `on:input={h}` | `.on(EventKind::Click, h)` / `.on(EventKind::Input, h)` |
| `on:<name>={h}` for a future kind | `.on(EventKind::<Variant>, h)` once `REQ-ASYNC-*` adds the variant |
| `<Capitalized … />` | the component model's invocation form (§3, IA2), yielding a `VNode` spliced as a child |
| the element at the end of a `view!` | `.into()` to a `VNode` (`From<VElement> for VNode`) |

The counter's hand-built tree and the `view!` version produce byte-identical `VNode`s; this equivalence is the
additivity check (REQ-API-023). `view!` and a re-exported `text` are additive items the `prelude` gains;
no existing export is removed or changed.

### 2.8 Fragments, interop, and whitespace

`VNode` is a single frozen node with no `Fragment` variant, so a top-level `view!` yields exactly **one** root
`VNode`; multiple top-level nodes are a diagnostic suggesting a wrapping element (this differs from
Leptos/Dioxus, which allow top-level fragments — Ferric's node model has none). In child position, multiple
nodes splice: `{vec_of_vnodes}`, a `<For>`, or a sequence of sibling tags each contribute several children,
expressed by the `Vec<VNode>`-into-`.children(..)` lowering. Interop is two-way — a `view!` produces an ordinary
`VNode` usable anywhere the builders are, and any `{expr}` yielding a `VNode` splices directly as a child, the
explicit exit to raw builder code so the macro never becomes a cage. Whitespace between tags is insignificant
and discarded; only quoted text renders, so the rendered text is exactly what the author quoted.

---

## 3. The component model — props, children, slots, composition

Today a component is any `Fn() -> VNode` with no way to declare what it accepts. An author who wants a reusable
`Card` writes a closure that captures its inputs by hand and has no typed surface a caller fills. The component
model gives a component a declared props/children/slots surface. It is the surface persona A3 (the
library/component author) depends on most, and persona A2 feels its absence every time they want to reuse a
piece of UI. Props, children, named slots, and composition are one model seen from four sides — children and
slots are themselves kinds of prop, and composition is what happens when one component's declared surface is
filled by another's output.

### 3.1 A `#[component]` function with a generated typed props builder

An author declares a component as an ordinary Rust function annotated with `#[component]`; its parameters are
its props, and its body returns a `VNode` (typically written with `view!`):

```rust
use ferric::prelude::*;

#[component]
fn Greeting(name: String, #[prop(default = 3)] times: usize) -> VNode {
    view! { <p>{format!("Hello {name} ×{times}")}</p> }
}
```

```rust
view! { <Greeting name={"ferric".into()} times=5 /> }   // both props set
view! { <Greeting name={"ferric".into()} /> }           // times takes its default, 3
```

`#[component]` is **sugar over the frozen `Component` trait**. It generates three things the author never writes
by hand but can always fall back to (§3.5): a props struct `GreetingProps` with one field per parameter; a
builder with one setter per field, which is the target the `view!` macro lowers a component invocation onto; and
a `Component` impl whose `render` runs the function body with the props in scope.

This is the design every credible Rust peer converged on, chosen deliberately over the alternatives:

| Declaration style | What the author writes | Why not the primary surface |
|---|---|---|
| Positional function arguments, no struct | `fn Greeting(name, times)`, called positionally | Rust has no optional/defaulted/named arguments; every prop would be required and positional, and adding or reordering a prop breaks every caller |
| Hand-written builder | `Greeting::builder().name(..).build()` | Works and is explicit, but the author writes the builder plumbing for every component — verbose enough that A3 pays a cost the framework should absorb |
| **`#[component]` fn + generated builder (chosen)** | the function above | Compile-time required/optional/defaulted props, named arguments through the builder, additive evolution (a new optional prop breaks no caller), and the author writes a plain function. The cost is macro-generated code whose errors can read in terms of generated types — paid down by the diagnostics bar (§3.6) |

One divergence from the VDOM peers is deliberate: **Ferric does not require props to be `PartialEq`.** Yew
requires it so the framework can skip re-render when props are unchanged, and Dioxus does likewise. Ferric's
change detection is not prop-diffing — a component body runs inside the mount effect, so a prop that is a
`Signal<T>`/`Memo<T>` re-renders the parts that read it with no equality check, and a plain owned prop is set
once. This follows the signal-reactive peers (Leptos, Sycamore) rather than the prop-diffing peers (Yew,
Dioxus), and it follows directly from the reactive runtime Ferric already has.

### 3.2 Typed props

A prop's kind is read from its type and its `#[prop(..)]` attribute:

- **Required** — a plain typed parameter with no attribute; omission is a compile error naming the missing prop.
- **Optional** — `#[prop(optional)]`, making the prop an `Option<T>` that defaults to `None` when omitted.
- **Defaulted** — `#[prop(default = expr)]`, supplying `expr` when the caller omits the prop.
- **Converting** — `#[prop(into)]`, accepting any `T: Into<FieldType>` so a caller may pass a `&str` where the
  prop is a `String`, moving the conversion to the declaration as Leptos does.
- **Reactive** — a prop typed as a `Signal<T>`/`Memo<T>`. These are `Copy` keys into the reactive runtime, so
  passing one is cheap and the component stays subscribed; reading it in the body re-renders on change. No
  attribute is needed — the type carries the reactivity.

A component with no props is the baseline function component unchanged; `#[component]` is not required for a
bare `Fn() -> VNode`, and on a zero-parameter function it generates an empty props type. Props are type-checked
at compile time against the generated builder; a wrong-typed value is a compile error naming the prop and its
expected type (§3.6), not a deferred runtime failure.

### 3.3 Children and named slots

A component accepts unlabelled child content by declaring `children: Children`:

```rust
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

```rust
view! {
    <Card title={"Welcome".into()}>
        <p>"First paragraph."</p>
        <p>"Second paragraph."</p>
    </Card>
}
```

`Children` is `Rc<dyn Fn() -> Vec<VNode>>` — a deferred, reference-counted thunk producing the nested child
nodes. Two properties make it lower cleanly: it is `Vec<VNode>`, not `VNode`, so a children block can carry
several sibling roots without a fragment variant the frozen `VNode` lacks (`{children()}` lowers onto the
existing `VElement::children(..)` builder); and it is **deferred**, so the component decides where and whether to
render its children by calling `children()` at that point — and because the call happens inside the render,
signals the child content reads stay tracked. Children are required by default; `#[prop(optional)] children:
Option<Children>` makes them optional; a component with no `children` parameter does not accept children, and
nesting content inside it is a diagnostic (§3.6).

A component that needs **more than one** labelled region declares each as a typed **slot**:

```rust
#[component]
fn Page(header: Slot, #[prop(optional)] footer: Option<Slot>, children: Children) -> VNode {
    view! {
        <article>
            <header>{header()}</header>
            <main>{children()}</main>
            { footer.map(|f| view! { <footer>{f()}</footer> }) }
        </article>
    }
}
```

```rust
view! {
    <Page>
        <slot:header><h1>"Title"</h1></slot:header>
        <p>"Main body — the default children region."</p>
        <slot:footer>"© 2026"</slot:footer>
    </Page>
}
```

`Slot` has the same shape as `Children` (`Rc<dyn Fn() -> Vec<VNode>>`) but is a distinct field the author fills
by name. Each named slot is filled at most once; filling an undeclared slot or filling one twice is a
diagnostic. A `Slot` field is required, an `Option<Slot>` field optional. Named slots and a `children` field
coexist: unlabelled content fills `children`, labelled content fills the matching slot (`Page` does both).
**Parameterized slots** (render-prop style) let a component pass a value *into* the caller-provided content — the
pattern a generic list needs — declared as `SlotFn<T> = Rc<dyn Fn(T) -> Vec<VNode>>` and passed as an ordinary
prop. The zero-argument named slot is part of the early floor; parameterized slots are a 1.0 enhancement (staged
`one_oh`), since a real app can be built with plain slots and a parameterized slot can be expressed as a child
closure in the interim.

### 3.4 The additive types

The model introduces exactly these items, all additive — none redefines a frozen item (IA4):

| New item | Shape | Role |
|---|---|---|
| `#[component]` | attribute macro on `fn(..) -> VNode` | Generates the props type, builder, and `Component` impl |
| `<Name>Props` + its builder | generated struct + builder | The typed declaration surface the `view!` macro fills |
| `#[prop(optional)]` / `#[prop(default = ..)]` / `#[prop(into)]` | field attributes | Mark a prop optional, defaulted, or converting |
| `Children` | `Rc<dyn Fn() -> Vec<VNode>>` | Deferred, reactive child content |
| `Slot` | `Rc<dyn Fn() -> Vec<VNode>>` | One named, deferred, reactive content region |
| `SlotFn<T>` | `Rc<dyn Fn(T) -> Vec<VNode>>` | A parameterized slot (render-prop) |

### 3.5 Composition and the escape hatch

Composition is nesting: a component is placed in another's body, filled through its declared props, children,
and slots. Because every component — generated, hand-written, or a bare closure — is a `Component` that renders
to one `VNode`, and `VNode`s nest through `VElement.children`, composition needs no rule beyond the lowering:

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

A component invocation `<Name .. />` lowers to: build `NameProps` through its builder, construct the component,
and call `Component::render` — the **frozen trait method** — to get one `VNode` spliced into the enclosing
element with `.child(..)`. The escape hatch keeps the model from locking anyone in: `#[component]` is sugar, so
a component can always be hand-written against the trait, and hand-written, generated, and bare-closure
components interoperate because all three are the same frozen trait. The baseline's object-safe dynamic dispatch
(`&dyn Component`, `Box<dyn Component>`) is carried forward, so a component may hold a dynamic set of child
components.

### 3.6 Component diagnostics (the testable failure bar)

A declared, type-checked surface is only worth having if getting it wrong points at the author's code. The model
commits to a `trybuild`-checkable bar for the common mistakes; each message names the author's error in terms of
their code, not framework internals:

| Author mistake | Required diagnostic |
|---|---|
| Omit a required prop | names the missing prop and component — "missing required prop `name` on `Greeting`" |
| Pass a prop of the wrong type | names the prop and expected type — "prop `size_px` on `Avatar` expects `u32`" |
| Pass a prop the component does not declare | names the unknown prop and component — "`Avatar` has no prop `widht`" |
| Nest children in a component with no `children` field | states the component does not accept children |
| Fill an undeclared slot, or fill one twice | names the slot and component |
| Omit a required slot | names the missing slot |

---

## 4. Context — sharing state down the tree without prop drilling

Today a value shared by many components must be passed as a prop through every component between its owner and
its user. Context removes that threading: an ancestor **provides** a value to its subtree, and any descendant
**reads** it directly from inside its own body, typed by the value's type. Context is three functions added to
`ferric::prelude`:

```rust
// Additive over the frozen prelude. Provide into the current reactive owner scope;
// read by walking ancestor owner scopes, nearest first.
pub fn provide_context<T: Clone + 'static>(value: T);
pub fn use_context<T: Clone + 'static>() -> Option<T>;   // None when no ancestor provided `T`
pub fn expect_context<T: Clone + 'static>() -> T;        // panics with a located message when absent
```

```rust
#[derive(Clone, Copy)]
struct Theme { dark: Signal<bool> }

fn app() -> VNode {
    let theme = Theme { dark: create_signal(false) };
    provide_context(theme);          // visible to every descendant from here down
    view! { <Toolbar /> }            // Toolbar and its descendants receive nothing explicitly
}

fn theme_toggle() -> VNode {
    let theme = expect_context::<Theme>();   // read directly — no prop was threaded to reach it
    view! {
        <button on:click={move || theme.dark.update(|d| *d = !*d)}>
            { move || if theme.dark.get() { "Switch to light" } else { "Switch to dark" } }
        </button>
    }
}
```

The value is keyed by its Rust type. `use_context::<T>()` returns `Option<T>` so a missing provider is a value
the author matches on, not a crash; `expect_context::<T>()` returns `T` and panics with a message naming the
missing type for the common case where a provider is a precondition. This split follows Leptos exactly, and
makes the plain name (`use_context`) the one that does not panic — an author opts into the panic by writing
`expect_context`, the same shape as `Option::unwrap`/`expect`.

**Context carries a value; it is not itself reactive.** When the provided value is a `Signal<T>`/`Memo<T>` — the
normal case for shared mutable state — a consumer that reads the handle inside its body re-renders on change,
because the read tracks the signal, not because the lookup tracks anything. Resolving context every render is
therefore cheap and establishes no subscription. This is the boundary an author relies on: the lookup is
untracked; the signal read is what re-renders.

**Context lifetime is bounded by the reactive owner scope it was provided into.** When that scope is disposed —
a component unmounts, a conditional branch is torn down — the provided entries are released with the scope, the
same disposal that unsubscribes the scope's effects and memos. This reuses the baseline `ReactiveScope` owner
tree and the `no_stale_subscriber_leak` property (`src/signal.rs`) directly, adding no second lifetime rule: a
provided value does not outlive the part of the UI it belonged to, and no released value is reachable afterward.
`ReactiveScope` stays crate-internal; the author's surface is the three free functions, and the owner scope they
bind to is the one the runtime already pushes around a rendering component. When the same type is provided at
more than one level, `use_context` resolves to the nearest ancestor and an inner provider shadows an outer one
for its own subtree only — letting a subtree override app-wide context (a modal with a restricted `Session`)
without disturbing the rest of the tree.

Context values satisfy `T: Clone + 'static` and are returned by cloning the stored entry — a bound close to free
for the handle case that dominates, since `Signal`/`Memo` are `Copy` and a context value is normally a handle or
a small struct of handles. An author sharing a large owned value provides a `Signal`/`Rc` of it and reads the
handle, the move the reactive model already asks for.

---

## 5. How the three parts compose — the authoring seams

The macro, the component model, and context are one surface, and two seams fix how they meet. These are the
correspondences the synthesis gate asserted (IA2, IA3); they are stated here as the single authoring story,
since an author crosses them constantly — a `view!` body invokes components, those components declare the props,
children, and slots the macro fills, and a context value is read inside a component body the macro renders.

**The invocation seam (macro ↔ component model).** Every way the macro passes something to a component
corresponds to a declaration form the component model defines, and every declaration form is reachable from the
macro — no orphan on either side:

| Macro-side passing form (§2) | Component-side declaration form (§3) |
|---|---|
| `name={value}` on a component tag | a prop: a `#[component]` fn parameter → generated builder setter → props field |
| attribute omitted | an optional (`→ None`) or defaulted prop, or a named diagnostic if the prop is required |
| `name={expr}` where `expr` is a `Signal`/`Memo` | a prop whose declared type is that reactive handle (no separate passing form) |
| bare content nested inside `<Comp>…</Comp>` | a `children: Children` (or `Option<Children>`) field |
| `<slot:label>…</slot:label>` | a named slot field `label: Slot` (or `Option<Slot>`) |
| `row={Rc::new(|x| …)}` on a component tag | a parameterized slot `SlotFn<T>` field, passed as an ordinary prop |
| `<Comp/>` in child position | the component's `Component::render` output, one `VNode`, spliced via `.child(..)` |

**The context seam (context ↔ component body + reactive runtime).** `provide_context`/`use_context`/
`expect_context` are ordinary calls in a component body — the unit the macro renders — not special mount-time
entry points, so context is read from the same place props and children are, and a component can both consume
and provide context. And a provided value is released by its owner scope's disposal, so context does not outlive
its subtree. The macro adds no context syntax and places no obstacle: a context read is an ordinary expression
usable in a `{…}` interpolation or a handler closure, exactly like a signal read.

---

## 6. Everything is additive over the frozen surface

Every construct in this model lowers onto the baseline `VNode`/`VElement`/`EventKind`/`EventHandler`/`Component`
model and the frozen `ferric::prelude`, adding only new items (`REQ-FW-009`, identity IA4):

- **The macro** produces nodes through the frozen `VElement`/`vdom::text` constructors; `view!` and a re-exported
  `text` are new items, and a `view!` tree equals the hand-built tree byte for byte.
- **The component model** adds `#[component]`, the generated `*Props` types, `Children`, `Slot`, and `SlotFn`;
  the `Component` trait and its blanket impl over `Fn() -> VNode` are unchanged, so the baseline counter's bare
  closure still compiles as a `Component` at 1.0.
- **Context** adds `provide_context`, `use_context`, and `expect_context` to the `prelude`; no existing prelude
  item changes signature or meaning, and `ReactiveScope` stays crate-internal (the reactive `Node` gains an
  internal per-owner typed store, a private detail).

An app written against the baseline `prelude` still compiles at 1.0 with the authoring model present; no
previously exported item is removed or redefined.

---

## 7. Where Ferric's authoring model sits among its peers

All four Rust peers provide a declarative view macro and a component model; they differ in syntax flavor and —
more consequentially — in reactivity model. The comparison rests on their documented public behavior.

**View macro.**

| Peer | Syntax flavor | Reactivity model | Keyed lists | Bearing on Ferric |
|---|---|---|---|---|
| Leptos `view!` | Angle-bracket HTML-like | Fine-grained signals, no VDOM | `<For each key let:item>` | The flavor Ferric follows; but Ferric's VDOM re-render is **not** Leptos's fine-grained binding (§1.1) |
| Yew `html!` | JSX-like angle brackets | React-like VDOM + diff | `key={..}` per item | Closest to Ferric's model (VDOM + macro); informs the single-root/`key` design |
| Dioxus `rsx!` | Rust-struct-like | React-like VDOM + diff | `key: ..` per item | A considered flavor, rejected for the HTML-like one; the VDOM model is shared |
| Sycamore `view!` | Terse `div(..) { .. }` | Fine-grained signals, no VDOM | keyed `Keyed`/`Indexed` views | A considered flavor; same fine-grained caveat as Leptos |
| Solid / Vue 3 (JS) | JSX / templates | Solid fine-grained; Vue 3 signals + VDOM | keyed `For` / `v-for :key` | Vue 3 is Ferric's closest architectural analog (signals *and* a VDOM) |

**Component model.** Ferric's `#[component]` fn + generated typed props builder is closest to **Leptos** and
adopts its `#[prop(optional|default|into)]` vocabulary directly, because Leptos is the signal-reactive Rust
framework whose props ergonomics are the most refined and whose reactivity Ferric's most resembles. **Sycamore**
shares the "props are a typed struct" center with a smaller surface and more explicit builder authoring.
**Dioxus** supplies the render-prop shape Ferric borrows for `SlotFn<T>`, but diffs props and leans on
`PartialEq`. **Yew** mandates `#[derive(Properties, PartialEq)]` because it re-renders by comparing props —
the sharpest divergence, since Ferric drops the mandatory `PartialEq` on the strength of its signal-based change
detection.

**Context.** Ferric keys context by Rust type (`use_context::<T>()`), the convention across Leptos, Dioxus
(`TypeId`), Sycamore, and Yew, and it composes with Ferric's `Copy` signal handles. The alternative is Solid's
explicit-handle `createContext`/`useContext`: that model lets two providers of the same underlying type coexist
and carries a compile-time default, but it reintroduces an object the author routes to every provider and reader
— the prop threading context exists to remove. Ferric takes the type-keyed side because the Rust newtype
(`struct Theme(Signal<bool>)`) is the idiomatic way to distinguish two values of the same shape, and the newtype
cost is small and local where the handle cost is paid at every use site.

The one ergonomic constraint Rust imposes on all of them: Rust has no named or defaulted function arguments, so
*some* generated surface (a struct + builder) is unavoidable to get optional, defaulted, and named props. Every
peer generates one, and every peer pays the same cost — macro-generated code whose compile errors can read in
terms of generated types rather than the author's call. The diagnostics bars in §2.6 and §3.6 are the commitment
to pay that cost down rather than leave it.

---

## 8. The merged `REQ-API-*` register

One register, three disjoint bands (identity IA1), each id stated once (identity IA5): the `view!` macro owns
`REQ-API-001 … 029`, the component model owns `REQ-API-030 … 059` (`030 … 052` assigned, `053 … 059` reserved),
and context owns `REQ-API-060 … 079` (`060 … 070` assigned, `071 … 079` reserved). Every acceptance criterion
uses a `verification_method` from the inherited vocabulary — `automated_test` | `example_build` |
`doc_inspection` (identity IA6) — and conforms to `../../contracts/id_and_traceability_schema.yaml`. Unless
noted, each entry is `release_gating: true`.

### Band A — the `view!` macro (`REQ-API-001 … 029`, owner `SUBTASK_view_macro`)

**REQ-API-001 — A `view!` macro is the declarative authoring entry point.** An author describes an element tree
with `view!` instead of `VElement` builder chains. *Acceptance:* `view! { <div class="counter"><p>"hi"</p></div> }`
compiles and evaluates to a `VNode` equal to the builder tree. *(automated_test, example_build)* · usable_early ·
Refs: REQ-FW-005.

**REQ-API-002 — Element nodes lower to `VElement::new(tag)`.** `<tag>…</tag>` and `<tag/>` produce an element
with that tag. *Acceptance:* `<br/>` → `VElement::new("br")`; `<div>…</div>` nests its children in order.
*(automated_test)* · usable_early · Refs: REQ-FW-005.

**REQ-API-003 — Text children lower to `vdom::text`.** A quoted literal and a `{expr}` of `impl Into<String>`
each produce a text node. *Acceptance:* `<p>"count: " {n.to_string()}</p>` produces two text children.
*(automated_test)* · usable_early · Refs: REQ-FW-005.

**REQ-API-004 — Static and dynamic attributes lower to `.attr(name, value)`.** `name="literal"` and
`name={expr}` (`expr: Into<String>`) set an attribute. *Acceptance:* `<a href="/x" class={c}>` produces attrs
`("href","/x")` and `("class", c.into())`, and the example renders them. *(automated_test, example_build)* ·
usable_early · Refs: REQ-FW-005.

**REQ-API-005 — Nesting and mixed children lower to ordered children.** Nested elements and interleaved
text/element/interpolation children appear in source order. *Acceptance:* a `<div>` of text, an element, and an
interpolation produces three children in written order. *(automated_test)* · usable_early · Refs: REQ-FW-005.

**REQ-API-006 — `on:<name>={closure}` lowers to `.on(EventKind::<Variant>, closure)`.** An author binds an event
with a `Fn()` closure. *Acceptance:* `<button on:click={h}>` produces one `(EventKind::Click, _)` binding whose
closure runs `h`; the macro counter increments on click. *(automated_test, example_build)* · usable_early · Refs:
REQ-FW-005, REQ-FW-014.

**REQ-API-007 — The event-name set is open and additive.** The grammar maps a name token to an `EventKind`
variant; `click`/`input` resolve today, further names resolve as `REQ-ASYNC-*` extends `EventKind` with no macro
change. *Acceptance:* `on:click`/`on:input` compile; a doc note states new names become available with the
variant; an unmapped name fails per REQ-API-026. *(doc_inspection, automated_test)* · usable_early · Refs:
REQ-ASYNC-* (read-only), REQ-FW-006.

**REQ-API-008 — Interpolated reactive values re-render on change.** A `{expr}` reading a `Signal`/`Memo` in a
view re-renders the component when the signal changes, because the read subscribes the mount effect.
*Acceptance:* a headless `wasm-bindgen-test` mounts `<p>{count.get()}</p>`, calls `count.set(..)`, observes the
text update. *(automated_test, example_build)* · usable_early · Refs: REQ-FW-005.

**REQ-API-009 — The reactivity model is stated as coarse-grained.** The docs state a signal read in a view
re-renders the whole component, reconciled by the keyed diff, with no fine-grained per-node binding. *Acceptance:*
a reviewer confirms the guide states the coarse-grained model and contrasts it with fine-grained peers.
*(doc_inspection)* · usable_early · Refs: REQ-FW-005; REQ-PERF-* (read-only).

**REQ-API-010 — Conditional rendering yields a `VNode`, with an explicit empty node.** A Rust `if`/`match`/
ternary in interpolation position produces a `VNode`; the "render nothing" branch produces an explicit empty
node. *Acceptance:* a conditional view compiles with both branches producing a `VNode`, the empty branch
rendering no visible content. *(automated_test, example_build)* · usable_early · Refs: REQ-FW-005.

**REQ-API-011 — Kind/tag-changing conditionals reconcile as a `Replace`.** When branches differ in node kind or
tag, toggling re-renders that position wholesale, and this is documented. *Acceptance:* a test toggles between
`<span>` and `<a>` and observes a `Replace`-shaped patch; the guide states it. *(automated_test,
doc_inspection)* · usable_early · Refs: REQ-FW-005.

**REQ-API-012 — A keyed-list form produces a `Vec<VNode>` spliced via `.children`.** A `<For each key let:item>`
iterates items into a child list. *Acceptance:* a `<For>` over three items produces a `<ul>` with three ordered
`<li>` children; the example renders the list. *(automated_test, example_build)* · usable_early · Refs:
REQ-FW-005.

**REQ-API-013 — The keyed-list form produces a fully-keyed sibling list.** Every element the form produces
carries its key, satisfying `all_keyed` so the list reconciles by identity. *Acceptance:* reordering the
collection produces `MoveChild` patches and no `Replace` of keyed nodes (mirrors baseline
`keyed_children_reorder_*`). *(automated_test)* · usable_early · Refs: REQ-FW-005.

**REQ-API-014 — `key={expr}` lowers to `.key(expr)`; the mixing caveat is documented.** A standalone
`key={expr}` sets an element's key; the guide states an unkeyed sibling drops the parent to positional diffing.
*Acceptance:* `<li key={id}>` → `.key(id)`; a reviewer confirms the caveat. *(automated_test, doc_inspection)* ·
usable_early · Refs: REQ-FW-005.

**REQ-API-015 — Capitalized tag = component; lowercase tag = HTML element.** The macro routes by the tag token
alone. *Acceptance:* `<div/>` is an element; `<TodoList/>` is a component invocation resolving to the in-scope
item. *(automated_test)* · usable_early · Refs: REQ-FW-005; band B (IA2).

**REQ-API-016 — A macro prop `name={value}` corresponds to a declared prop.** *Acceptance:* a stated example
passes a prop through the macro to a component that declares it; it compiles and renders — closure asserted by
synthesis (IA2). *(example_build, automated_test)* · usable_early · Refs: band B (IA2).

**REQ-API-017 — Children nested in a component element correspond to its declared children acceptance.**
*Acceptance:* a stated example nests children into a component declaring `children`; compiles and renders —
closure asserted by synthesis (IA2). *(example_build)* · usable_early · Refs: band B (IA2).

**REQ-API-018 — A `<slot:name>` fill corresponds to a component-declared named slot.** *Acceptance:* a stated
example fills a named slot of a component declaring it; renders into the slot position — closure asserted by
synthesis (IA2). *(example_build)* · usable_early · Refs: band B (IA2).

**REQ-API-019 — A component invocation lowers to the component model's invocation form, yielding a `VNode`.** The
macro splices the produced `VNode`; it neither constructs the component nor redefines the component model.
*Acceptance:* the output is a `VNode` child; no frozen component API is redefined (checked with
REQ-API-023 / IA4). *(automated_test, doc_inspection)* · usable_early · Refs: band B (IA2), REQ-FW-009 (IA4).

**REQ-API-020 — A top-level `view!` yields exactly one root node.** Multiple top-level nodes are rejected (forced
by the frozen single-node `VNode`). *Acceptance:* a single-root `view!` compiles; a two-root `view!` fails per
REQ-API-024. *(automated_test)* · usable_early · Refs: REQ-FW-009 (IA4).

**REQ-API-021 — Child-position splicing and the `VNode` escape hatch.** `{Vec<VNode>}`, `<For>`, and sibling tags
splice multiple children; any `{expr}` yielding a `VNode` splices directly. *Acceptance:* a view with
`{vec_of_vnodes}` renders each child; a `{builder_vnode}` splice renders the builder-produced node.
*(automated_test, example_build)* · usable_early · Refs: REQ-FW-005.

**REQ-API-022 — Two-way interop with the builder API.** `view!` output is an ordinary `VNode`, and
builder-produced `VNode`s are usable inside a view via interpolation. *Acceptance:* a `view!` node is passed to
`.child(..)` and a builder node is spliced into a view; both compile and render. *(automated_test)* ·
usable_early · Refs: REQ-FW-009.

**REQ-API-023 — Every construct lowers additively; nothing is redefined (IA4).** All output is built from the
frozen constructors and `prelude`; added items (`view!`, re-exported `text`) are additive. *Acceptance:* a
`view!` tree equals the hand-built tree; an app against the baseline `prelude` still compiles with the macro
present. *(automated_test)* · usable_early · Refs: REQ-FW-009 (IA4).

**REQ-API-024 — Structural view errors produce a diagnostic at the author's span.** Unclosed elements, mismatched
closes, and multiple top-level nodes each name the problem at the offending tokens. *Acceptance:* `trybuild`
fixtures for each produce the expected `stderr`. *(automated_test)* · usable_early · Refs: REQ-FW-014.

**REQ-API-025 — A wrong-typed attribute or text value is diagnosed at the expression span.** A dynamic value not
`Into<String>` produces a type error at the `{expr}`, naming the required conversion. *Acceptance:* a `trybuild`
fixture with a non-string attr value fails with the error located at the expression. *(automated_test)* ·
usable_early · Refs: REQ-FW-014.

**REQ-API-026 — An unknown event name is diagnosed with the bound set.** `on:<name>` with no matching variant
names the unknown event and lists the bound kinds. *Acceptance:* a `trybuild` fixture `on:klick=` fails with
"unknown event `klick`; bound events are: click, input". *(automated_test)* · usable_early · Refs: REQ-FW-014,
REQ-ASYNC-* (read-only).

**REQ-API-027 — The keyless-list case is diagnosed best-effort, with its limit documented.** The direct `<For>`
form flags a missing `key`; the docs state an arbitrary `{iter.map(..)}` list cannot be fully checked and that
`<For>` is the keyed default. *Acceptance:* a `trybuild` fixture for a keyless `<For>` fails with a "needs `key`"
diagnostic; a reviewer confirms the documented limit. *(automated_test, doc_inspection)* · usable_early · Refs:
REQ-FW-014.

**REQ-API-028 — The diagnostics story as a whole is `trybuild`-checkable (IA6).** A fixture suite of malformed
views, each with a committed expected `stderr`, is part of the test suite. *Acceptance:* `cargo test` runs the
`trybuild` suite and all expected-failure fixtures match their committed `stderr`. *(automated_test)* ·
usable_early · Refs: REQ-FW-014.

**REQ-API-029 — Whitespace handling is predictable and documented.** Only quoted text renders; whitespace
between tags is insignificant and discarded, and the rule is documented. *Acceptance:* a view formatted across
indented lines renders only its quoted text with no injected or collapsed spaces; a reviewer confirms the rule.
*(automated_test, doc_inspection)* · usable_early · Refs: REQ-FW-005.

### Band B — the component model (`REQ-API-030 … 059`, owner `SUBTASK_components_props_slots`)

**REQ-API-030 — A component declares typed props as a `#[component]` function's parameters.** The attribute
generates a typed props type and a builder the `view!` macro fills. *Acceptance:* a stated `#[component]` with
two props compiles, and `view!`-invoking it with both set renders the described UI. *(example_build)* ·
usable_early · Refs: REQ-FW-005.

**REQ-API-031 — Required props must be supplied.** A prop with no default and no `optional` must be supplied.
*Acceptance:* a snippet supplying every required prop builds and renders (the omission case is REQ-API-050).
*(example_build)* · usable_early.

**REQ-API-032 — Optional props default to absent.** `#[prop(optional)]` makes the prop `Option<T>`, defaulting to
`None`. *Acceptance:* a component with an optional prop compiles and renders both when supplied and when omitted
(the omitted case observably takes the `None` branch). *(example_build)* · usable_early.

**REQ-API-033 — Defaulted props take a declared default.** `#[prop(default = expr)]` supplies `expr` when
omitted. *Acceptance:* a component renders with the default when the prop is omitted and the supplied value when
present. *(example_build)* · usable_early.

**REQ-API-034 — Converting props accept `Into` conversions.** `#[prop(into)]` accepts any `T: Into<FieldType>`.
*Acceptance:* a component with an `into` `String` prop compiles when called with a `&str` literal and renders.
*(example_build)* · **one_oh** · Refs: Leptos `#[prop(into)]`.

**REQ-API-035 — Props may be reactive handles.** A `Signal<T>`/`Memo<T>` prop passes the handle; reading it in
the body re-renders the parts that read it, with no props-equality check. *Acceptance:* a headless test mounts a
component taking a `Signal<i32>` prop, changes the signal, and observes the DOM update in place. *(automated_test)* ·
usable_early · Refs: baseline `signal.rs`.

**REQ-API-036 — Props do not require `PartialEq`.** Change detection is signal-based, not prop-diff-based.
*Acceptance:* a component whose prop type does not implement `PartialEq` compiles and renders. *(example_build)* ·
usable_early · Refs: contrast Yew `#[derive(Properties, PartialEq)]`.

**REQ-API-037 — A zero-prop component needs no props struct.** A bare `Fn() -> VNode` stays a `Component`;
`#[component]` on a zero-parameter function generates an empty props type. *Acceptance:* the baseline counter's
bare closure still compiles and renders as a `Component` at 1.0; a zero-prop `#[component]` also compiles and
renders. *(example_build)* · usable_early · Refs: REQ-FW-009; baseline `component.rs`.

**REQ-API-038 — A component accepts children via a `Children` prop.** `children: Children` is a deferred
`Rc<dyn Fn() -> Vec<VNode>>` the component calls where it places the children. *Acceptance:* a `Card`-style
component renders caller-nested content at the point it calls `children()`; a multi-node children block renders
all its nodes. *(example_build)* · usable_early · Refs: REQ-FW-005.

**REQ-API-039 — Children lower onto `VElement.children` additively and stay reactive.** `{children()}` lowers
onto the baseline `VElement::children(..)`; children read inside the render stay tracked. *Acceptance:* a
headless test whose children read a signal observes the children update in place on change; the block produces
the same `VElement.children` a hand-built tree would. *(automated_test)* · usable_early · Refs: baseline
`vdom.rs`; IA4.

**REQ-API-040 — Optional children.** `#[prop(optional)] children: Option<Children>` renders only when present.
*Acceptance:* a component with optional children renders correctly both with and without a children block.
*(example_build)* · usable_early.

**REQ-API-041 — A component declares named slots as typed fields.** Each labelled region is a `Slot` field; the
author fills each by label. *Acceptance:* a `Page`-style component with `header` and `footer` slots renders the
labelled content in the matching regions. *(example_build)* · usable_early · Refs: REQ-FW-005.

**REQ-API-042 — Each named slot is filled at most once.** Filling an undeclared slot, or filling one twice, is a
diagnostic (REQ-API-052). *Acceptance:* a single correct fill per slot builds and renders; error cases are
REQ-API-052. *(example_build)* · usable_early.

**REQ-API-043 — Required vs optional slots.** A `Slot` field is required; an `Option<Slot>` field is optional.
*Acceptance:* a component renders with an optional slot both filled and omitted (missing-required is
REQ-API-052). *(example_build)* · usable_early.

**REQ-API-044 — Named slots and children coexist.** Unlabelled nested content fills `children`; labelled content
fills the matching slot. *Acceptance:* a component with `header`/`footer` slots and a `children` body renders
labelled content in its regions and unlabelled content in the body, from one `view!` block. *(example_build)* ·
usable_early.

**REQ-API-045 — Parameterized slots (render-prop).** A `SlotFn<T>` (`Rc<dyn Fn(T) -> Vec<VNode>>`) lets a
component pass a value into caller-provided content. *Acceptance:* a generic `List<T>` taking a `SlotFn<T>`,
called with a per-item template, renders one templated row per item. *(example_build)* · **one_oh** · Refs:
Dioxus render-props.

**REQ-API-046 — Components compose by nesting through their declared surface.** A component is invoked in another
component's `view!` body and lowers to its `Component::render` output spliced as a `VNode`. *Acceptance:* a
multi-level composition (a component holding another in a slot and a third in its children) compiles and renders
the combined UI. *(example_build)* · usable_early · Refs: REQ-FW-005.

**REQ-API-047 — Composition is additive over the frozen `Component`/`VNode` surface.** Generated, hand-written,
and bare-closure components are all the frozen `Component` trait and compose; no frozen item is redefined.
*Acceptance:* a composition mixing a `#[component]`, a hand-written `impl Component`, and a bare closure renders;
a baseline app still compiles at 1.0. *(example_build)* · usable_early · Refs: REQ-FW-009; IA4; baseline
`component.rs`, `lib.rs`.

**REQ-API-048 — The declaration macro is a removable escape-hatch sugar.** Any component can be written by hand
against the trait, and the two forms interoperate; nothing is reachable only through the macro. *Acceptance:* a
component written once with `#[component]` and once as `impl Component` is used interchangeably at a call site.
*(example_build)* · usable_early.

**REQ-API-049 — Dynamic-dispatch composition is carried forward.** `&dyn Component` / `Box<dyn Component>` remain
available for a dynamic set of child components. *Acceptance:* a component holding `Vec<Box<dyn Component>>`
renders each; the baseline trait-object test still passes at 1.0. *(automated_test)* · **one_oh** · Refs:
baseline `component.rs` (`trait_object_component_renders`).

**REQ-API-050 — Missing or mistyped required prop is an actionable diagnostic.** Omitting a required prop or
passing a wrong-typed one names the prop, the component, and (for a type mismatch) the expected type — not a raw
builder-state error. *Acceptance:* `trybuild` fixtures for (a) a missing required prop and (b) a wrong-typed prop
fail with a message naming the prop and component (and expected type for (b)). *(automated_test)* · usable_early ·
Refs: REQ-FW-014.

**REQ-API-051 — Unknown prop is an actionable diagnostic.** Passing an undeclared prop names the unknown prop and
the component. *Acceptance:* a `trybuild` fixture passing an undeclared prop fails naming the unknown prop and
component. *(automated_test)* · usable_early · Refs: REQ-FW-014.

**REQ-API-052 — Children and slot misuse are actionable diagnostics.** Children on a childless component, an
undeclared slot fill, a double slot fill, or a missing required slot each name the component and the offending
region. *Acceptance:* `trybuild` fixtures for (a)–(d) each fail with a message naming the component and region.
*(automated_test)* · usable_early · Refs: REQ-FW-014.

*(Band B: `REQ-API-053 … 059` reserved as headroom.)*

### Band C — context (`REQ-API-060 … 079`, owner `SUBTASK_context`)

**REQ-API-060 — Provide a value to a subtree.** `provide_context(value)` in an ancestor body makes a value
available to the whole subtree without threading it as a prop. *Acceptance:* a root calls `provide_context(v)`
and a descendant three or more components deep reads `v`, with no intermediate component forwarding it; it
compiles and renders. *(example_build)* · usable_early · Refs: REQ-FW-005.

**REQ-API-061 — Read a provided value without prop drilling.** `use_context::<T>()` returns `Option<T>`.
*Acceptance:* a headless test provides a `T`, reads it in a nested component, and asserts `Some(T)` equals the
provided value. *(automated_test)* · usable_early · Refs: REQ-FW-005.

**REQ-API-062 — Typed lookup keyed by the value's type, nearest-ancestor resolution.** `use_context::<T>()` /
`expect_context::<T>()` resolve to the nearest ancestor providing `T`; an inner provider shadows an outer one for
its subtree only. *Acceptance:* a headless test with an outer and an inner `T` asserts the inner reader sees the
inner value and an outer reader sees the outer; a second case asserts two distinct types at one scope are both
readable. *(automated_test)* · usable_early.

**REQ-API-063 — The no-provider case is explicit and located.** With no provider, `use_context` returns `None`
and `expect_context` panics with a message naming `T`. *Acceptance:* a test asserts `use_context::<T>()` is
`None`; a second asserts `expect_context::<T>()` panics and the message contains the type name of `T`.
*(automated_test)* · usable_early · Refs: REQ-FW-014.

**REQ-API-064 — A provided reactive value drives consumer re-render.** When the provided value is or holds a
`Signal`/`Memo`, a consumer reading that handle re-renders on change. *Acceptance:* a headless test provides a
struct holding a `Signal`, renders a consumer that reads it, mutates the signal from outside, and asserts the
consumer re-rendered with the new value. *(automated_test)* · usable_early · Refs: REQ-FW-005.

**REQ-API-065 — Context lookup is not itself a reactive dependency.** The lookup establishes no subscription; a
consumer re-renders only because of the signals it reads from the returned value. *Acceptance:* a headless test
provides a non-reactive value, reads it via `use_context`, and asserts the component does not re-render when
unrelated signals change; a `doc_inspection` confirms the guide states the lookup is untracked. *(automated_test)* ·
usable_early.

**REQ-API-066 — Context is readable from inside a component body (seam IA3).** `provide_context` /
`use_context` / `expect_context` are callable from a component body — the unit `view!` renders — not only at
mount. *Acceptance:* an example in which a `view!`-rendered component both reads via `expect_context` and
provides via `provide_context` to its children compiles and renders; a `doc_inspection` confirms the context and
component sections agree context calls occur in a component body. *(example_build)* · usable_early.

**REQ-API-067 — App-global context from the application root.** Providing at the mount root makes a value
readable from any component. *Acceptance:* an example calling `provide_context` in the root component and reading
it from a leaf, built and mounted via the existing `mount`, renders the shared value. *(example_build)* ·
usable_early · Refs: REQ-FW-009.

**REQ-API-068 — Context lifetime is bounded by the reactive owner scope (scoped cleanup, seam IA3).** A value
provided within a scope is released when that scope is disposed; afterward no provided value from it is
reachable. *Acceptance:* a test provides context inside a scope, disposes the scope, and asserts (a) a subsequent
lookup does not return the released value and (b) the owner node and its context entry are reclaimed — mirroring
the baseline `no_stale_subscriber_leak` / `disposing_scope_also_disposes_owned_memo` tests. *(automated_test)* ·
usable_early · Refs: REQ-FW-009.

**REQ-API-069 — Context surface is additive over the frozen prelude (IA4).** The three functions are new
`prelude` items; no existing item changes and `ReactiveScope` stays crate-internal. *Acceptance:* a
`doc_inspection` of the diff confirms the additions and that no frozen prelude item is removed or re-signed; an
`example_build` confirms a baseline-prelude program still compiles. *(doc_inspection, example_build)* ·
usable_early · Refs: REQ-FW-009.

**REQ-API-070 — Value bound and clone-out read semantics.** Context values satisfy `T: Clone + 'static` and are
returned by cloning the stored entry; the idiomatic value is a `Copy` handle or small struct of handles.
*Acceptance:* a test provides a `Copy` handle struct, reads it twice via `use_context`, and asserts both reads
refer to the same underlying signal (a write through one is visible through the other); a `doc_inspection`
confirms the bound and the handle idiom. *(automated_test)* · usable_early.

*(Band C: `REQ-API-071 … 079` reserved for additive context requirements.)*

### Register summary

- **Bands (IA1):** A = `001–029` (29 assigned); B = `030–052` assigned, `053–059` reserved; C = `060–070`
  assigned, `071–079` reserved. Disjoint, zero-padded 3-digit, monotonic per band.
- **Stage split:** `one_oh` — `REQ-API-034`, `REQ-API-045`, `REQ-API-049`; every other assigned id is
  `usable_early`. All assigned ids are `release_gating: true` (no post-1.0 deferral in the authoring model).
- **Verification vocabulary (IA6):** `automated_test`, `example_build`, `doc_inspection` only — no `benchmark_run`
  or `publishability` is used in this register.

---

## 9. Traceability and metadata

- **Owns:** `REQ-API-001 … 079` (bands A/B/C; identity I1). No id outside the API area is minted here.
- **Specializes (read-only):** `REQ-FW-005` (declarative authoring model — the `view!` macro, props/children/
  slots, and context are exactly its three named clauses), `REQ-FW-009` (additive over frozen surfaces),
  `REQ-FW-014` (actionable diagnostics). Each is covered: `REQ-FW-005` by the whole register; `REQ-FW-009`/IA4
  by REQ-API-023, 047, 069 and §6; `REQ-FW-014` by the diagnostics requirements REQ-API-024–028 and
  REQ-API-050–052, 063.
- **Authoring seams closed:** IA2 (invocation seam, §5) and IA3 (context seam, §5) both close in both directions,
  asserted by the synthesis gate.
- **Cross-area references (read-only):** `REQ-ASYNC-*` (the additive `EventKind` set and the event-payload
  handler form), `REQ-PERF-*` (the cost of the coarse-grained re-render model).
- **Grounding:** `Nousix-LLC/nswe-demo` @ `276138f`, baseline checkout
  `taskflow/dags/ferric-foundation/checkout/crates/ferric/` (`vdom.rs`, `component.rs`, `signal.rs`, `dom.rs`,
  `lib.rs`, `examples/counter.rs`).
- **Conforms to:** `../../contracts/id_and_traceability_schema.yaml` (REQ fields, `stage`, `release_gating`,
  `verification_method`) and `../contracts/req_api_partition.yaml` (band partition + authoring seams).
- **Repository target:** `design/ferric/authoring-model.md` (placed by the outer `SUBTASK_design_pr`).
