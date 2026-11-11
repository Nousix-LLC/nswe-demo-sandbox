# Ferric 1.0 — The `view!` macro authoring surface

This is section A of the Ferric 1.0 authoring model (subtree hub: `../_GLOBAL.md`): the declarative
`view!` macro an app author writes instead of hand-building `VElement::new(..).child(..)` trees. It
specifies **what the author writes and what must hold** — the authoring surface, how it lowers onto the
existing `VNode` model, and the quality bar for compile-time diagnostics. It does **not** specify the
proc-macro's internal token expansion; that is an implementation question for the code DAG that builds it.

**Grounding.** Every claim about today's Ferric is read from the baseline checkout at
`taskflow/dags/ferric-foundation/checkout/crates/ferric/` (the frozen surface the 1.0 carries forward
additively, `Nousix-LLC/nswe-demo` @ `276138f`): `src/vdom.rs` (the `VNode`/`VElement` builders and the
keyed `diff`), `src/component.rs` (`Component` / `Fn() -> VNode`), `src/signal.rs` (`Signal`/`Memo`/
`create_effect`), `src/dom.rs` (`mount`), `src/lib.rs` (the frozen `prelude`), and `examples/counter.rs`.
Peer view-macros are compared by name from their documented public behavior (§4).

**What this section owns.** The `REQ-API-001 … REQ-API-029` band (contract `../contracts/req_api_partition.yaml`,
identity IA1). It specializes parent `REQ-FW-005` (a declarative authoring model), `REQ-FW-009` (additive over
the frozen surface), and `REQ-FW-014` (actionable diagnostics). It composes against — and does not redefine —
the component model (band B, `../SUBTASK_components_props_slots/`) across the invocation seam IA2, and the
context model (band C) across the context seam IA3.

---

## 0. The baseline the macro replaces and lowers onto

An author today composes a view tree by hand. The counter example is the whole authoring surface in miniature:

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

Four baseline facts fix everything the macro may and may not do:

1. **The node model is closed and frozen.** `VNode` is exactly `Element(VElement) | Text(String)`. A
   `VElement` carries `tag: String`, `key: Option<Key>` (`Key = String`), `attrs: Vec<(String, String)>`,
   `events: Vec<(EventKind, EventHandler)>`, and `children: Vec<VNode>`. The builders `VElement::new`,
   `.key`, `.attr`, `.on`, `.child`, `.children`, the free function `vdom::text`, and `From<VElement> for
   VNode` are the only ways to construct a node. `EventKind` is `Click | Input` today. `EventHandler` is
   `Rc<dyn Fn()>` — a **zero-argument** closure. The macro MUST produce nodes through exactly these
   constructors and MUST NOT redefine any of them (parent `REQ-FW-009`, identity IA4).

2. **Rendering is coarse-grained: whole-component re-render plus keyed diff.** `mount` wraps the entire
   component render in **one** `create_effect` (`src/dom.rs`). Every `Signal`/`Memo` read anywhere in the
   render subscribes that single effect; any later write re-runs the **whole** render, and the keyed
   `diff` computes a minimal patch that `dom.rs` applies to the live DOM. Ferric has **no** fine-grained
   per-node DOM bindings. This is the Vue 3 / Dioxus / Yew virtual-DOM model, not the Leptos/Sycamore
   fine-grained-signal model — the scope doc places Ferric's closest analog as Vue 3 for exactly this
   reason. The macro's reactivity story is bound by this fact and must not imply otherwise (§1.4).

3. **Lists reconcile by key only when every sibling is a keyed element.** `diff_children` uses the keyed
   path **only** when `all_keyed(old) && all_keyed(new)` — i.e. every child on both sides is a
   `VElement` with `key.is_some()`. A single unkeyed sibling drops the whole parent's child list to a
   positional diff (which reconciles by index, so an insert in the middle re-patches the tail). The
   macro's list syntax must make producing a fully-keyed sibling list the natural thing to write (§1.6).

4. **Handlers re-bind only when the set of bound `EventKind`s changes, and read signals live.** Closures
   are opaque, so the diff cannot compare them; `diff_events` emits `SetEvents` only when the *set of
   kinds* changes. Because a handler reads its signals at call time rather than capturing values, keeping
   a retained element's prior closure across a re-render is sound. The macro does not need to do anything
   special here — lowering a handler to `.on(kind, closure)` inherits this behavior — but the design notes
   it so the diagnostics bar (§3) does not promise handler-identity checks the runtime cannot make.

The macro is pure sugar over this model: it is a more pleasant way to write the tree above, producing the
identical `VNode`. Nothing below adds a runtime capability the builders lack.

---

## 1. The authoring surface — what an author writes

### 1.1 Syntax flavor, and the choice behind it

Ferric adopts an **HTML/JSX-style `view!`** — angle-bracket tags with brace-delimited Rust interpolation —
in the family of Leptos's `view!` and Yew's `html!`. The counter, rewritten:

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

The choice is deliberate and is a trade-off, not a verdict (§4 compares the alternatives by name):

- **Angle brackets (chosen)** read like the HTML an author already knows and make the open/close structure
  visible, which matters for a VDOM framework whose mental model is "a tree that re-renders." Leptos and
  Yew take this route.
- **Sycamore's terse `div { .. }`** and **Dioxus's `rsx!` struct-style `div { class: "x", .. }`** are
  less visually noisy and more Rust-native, but they read less like markup and make the element/attribute/
  child boundary rely on punctuation the author must learn. They are reasonable; the brief names this a
  `view!`/JSX-style macro, and the HTML-like flavor is the better fit for an author evaluating Ferric
  against the JS frameworks it ultimately competes with.

The flavor is a surface decision. Everything in §2 (lowering) is independent of it: a different flavor would
lower to the same builder calls.

### 1.2 Elements, text, and attributes

- **Elements.** `<tag> … </tag>` and self-closing `<tag/>`. A lowercase tag name is an HTML element
  (§1.7 covers capitalized tags, which are component invocations).
- **Text.** A string literal is a text node: `<p>"hello"</p>`. Text is written quoted (as in Sycamore and
  in Yew's expression blocks) so the macro never has to guess where markup ends and prose begins — this
  removes a whole class of whitespace ambiguity (§1.10) and is the cost of the HTML-like flavor.
- **Attributes.** `name="literal"` for a static value and `name={expr}` for a dynamic one. Attribute
  **names** are written as the author expects them on the element (`class`, `id`, `href`, `type`).

```rust
view! { <a href="/x" class={active_class}>"link"</a> }
```

Baseline constraint: attributes are `(String, String)` pairs, so a dynamic attribute value
must be `impl Into<String>`. A non-string value is converted explicitly by the author — `width={n.to_string()}`
— rather than silently stringified by the macro; this keeps the author in control of formatting and gives
the macro a precise place to point a diagnostic when the type is wrong (§3). Boolean/presence attributes
are expressed as their string value (`aria-hidden="true"`); a first-class boolean-attribute shorthand is a
possible additive sugar but is not required for 1.0 and is not promised here.

### 1.3 Event handlers, and the open event set

A handler is written `on:<name>={closure}` and lowers to `.on(EventKind::<Variant>, closure)`:

```rust
view! { <button on:click={move || count.update(|n| *n += 1)}>"+"</button> }
```

Two baseline-driven facts shape this facet:

- **Handlers are zero-argument today.** The frozen `EventHandler` is `Rc<dyn Fn()>`, so the closure takes
  no arguments (the DOM layer wraps it in a listener that receives but discards the `web_sys::Event`). The
  macro's handler form is a `Fn()` closure. An **event-payload-carrying** handler form (a closure that
  receives the event) is an additive refinement owned by `REQ-ASYNC-*` (full DOM event coverage); this
  section names the seam and defers the form — it does not invent an event-argument signature the frozen
  `EventHandler` does not have.
- **The event-name → `EventKind` mapping is open.** Today `on:click` and `on:input` resolve (the two
  `EventKind` variants bound by `dom.rs`). The macro grammar maps the name token to an `EventKind`
  variant; as `REQ-ASYNC-*` extends `EventKind` (submit, keydown, focus, blur, change, …), those names
  resolve **with no change to the macro's grammar**. A name with no matching `EventKind` variant is a
  compile-time diagnostic (§3), not a silently dropped handler. (`EventKind` is owned cross-area; this is a
  read-only reference to `REQ-ASYNC-*`.)

### 1.4 Interpolated reactive values

A `{expr}` in child position embeds a Rust expression evaluated **during the component's render**:

```rust
view! { <p>"count: " {count.get()}</p> }   // reads `count` each render
```

Because `mount` wraps the whole render in one effect (baseline fact 2), reading `count` inside `{…}`
subscribes that mount effect, so a later `count.set(..)` re-runs the whole render and the keyed diff
patches the changed text in place. This is the same mechanism the hand-built counter already relies on
(`text(format!("count: {}", count.get()))`); the macro only removes the `text(format!(..))` boilerplate.

**Ferric's reactivity is coarse-grained**, and an author arriving from Leptos or Solid will assume
otherwise. A signal read inside a view re-renders the *entire component*, which the
keyed diff then reconciles against the live DOM — it does **not** create a fine-grained binding that updates
only that one text node without re-running the component. This is the VDOM model Ferric shares with Vue 3,
Dioxus, and Yew, and it is a deliberate consequence of the frozen `mount`/`diff` foundation, not a gap the
macro papers over. The ergonomic payoff is that `{expr}` is just a Rust expression — no `move ||` wrapper is
required around a plain read for it to be reactive, because the read already happens inside the render
effect. (A `{move || …}` *closure* interpolation is reserved as the additive seam for any future
fine-grained binding; 1.0 does not provide one, and the design does not imply it does.)

For a text interpolation whose value is not already a string, the author writes `{format!("count: {}", n)}`
or `{n.to_string()}`, exactly as the counter does today; the bare `{expr}` text form accepts any
`impl Into<String>`.

### 1.5 Control flow — conditionals

Conditional rendering is a Rust `if` / `match` / ternary in interpolation position that yields a `VNode`:

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

Two notes from the baseline diff:

- **An "empty" branch still needs a node.** `VNode` has no null/empty variant, so a branch that renders
  nothing yields an empty text node (`""`). The design standardizes this: the macro provides an explicit
  empty-node form for the "render nothing" branch so the author does not reach for an ad-hoc `text("")`,
  and both branches of a conditional in child position always produce a `VNode`.
- **A conditional that changes node kind or tag re-renders as a `Replace`.** When the two branches differ
  in kind (element↔text) or tag (`<span>` vs `<a>`), the diff emits a wholesale `Replace` at that position
  rather than an in-place patch (baseline `diff_node`). This is correct and expected; the design states it
  so the author understands that toggling between two different elements rebuilds that subtree, and so the
  performance section is not surprised by it.

### 1.6 Lists and keys

Keyed reconciliation is the baseline's one non-trivial list behavior, and it has a hard precondition (fact
3): the keyed-diff path engages **only** when every sibling in the list is a keyed element on both the old
and new sides. The list syntax is designed to make that the default, not a thing the author must remember.

A keyed-list form, in the spirit of Leptos's `<For each key>`, binds each item and requires a key:

```rust
view! {
    <ul>
        <For each={todos.get()} key={|t| t.id.to_string()} let:todo>
            <li>{todo.label.clone()}</li>
        </For>
    </ul>
}
```

This lowers to a `Vec<VNode>` in which **every** element carries its key, spliced into the parent via
`.children(..)` (§2). Because the key is part of the form rather than an afterthought, the produced sibling
list satisfies `all_keyed`, so inserts, moves, and removes reconcile by identity (the baseline's
`keyed_children_*` tests are exactly this behavior) rather than by position.

The key expression yields the baseline `Key` (`String`); `key={|t| t.id.to_string()}` is the shape that follows,
since `Key = String`.

Design guidance the list facet must carry, grounded in `all_keyed`:

- **Do not mix a keyed list with unkeyed static siblings under the same parent.** One unkeyed `<li>` beside
  the `<For>` output drops the whole `<ul>`'s children to positional diffing, silently losing identity
  reconciliation for the list. The guidance is to let the list be the sole content of its container (as
  above) or to key the static siblings too. A plain `{iter.map(..).collect::<Vec<_>>()}` splice is also
  supported for the advanced case, with the same keying responsibility on the author.
- **A standalone `key={expr}` on any element** lowers to `.key(expr)` and is available outside the `<For>`
  form for hand-rolled lists.

### 1.7 Invoking a component (the IA2 seam)

A **capitalized** tag is a component invocation; a lowercase tag is an HTML element. This
capitalization convention is the one every peer uses (Leptos, Yew, Dioxus, Sycamore), and it lets the macro
decide element-vs-component purely from the tag token.

```rust
view! {
    <TodoList items={todos.get()}>          // props
        <TodoHeader/>                        // child
        <slot:footer><Pager/></slot:footer>  // named slot fill
    </TodoList>
}
```

The macro side of the invocation seam (identity IA2, owned jointly with band B) has exactly three passing
forms, each of which must correspond to a declaration form the component model defines:

| Macro-side form (this section) | Corresponds to (band B declares) |
|---|---|
| `name={value}` on a component tag | a declared prop (name, type, required/optional/default) |
| children nested inside a component element | the component's declared `children` acceptance |
| `<slot:name> … </slot:name>` | a named slot the component declares |

This section states only the macro side and does **not** define how a component declares a prop, children,
or a slot — that is band B. The synthesis gate asserts IA2 closes in both directions (no macro passing form
without a component declaration form, and no declaration form unreachable from the macro). A component
invocation lowers to the component model's invocation form (band B), which yields a `VNode` the macro
splices as a child (§2); the macro does not construct the component itself and does not redefine the
component model (IA4).

### 1.8 Context, read from a component body (IA3, referenced)

Context — providing a value to a subtree and reading it without prop-drilling — is owned by band C
(`../SUBTASK_context/`, `REQ-API-060..079`) and the context seam IA3. It touches this section at one point:
a context value is read **inside a component body**, which is the unit the macro renders. The macro places
no obstacle in the way — a context read is an ordinary expression usable in a `{…}` interpolation or in a
handler closure, exactly like a signal read — and it adds no context syntax of its own. This is a read-only
reference to band C; IA3 (context lifetime tied to the reactive owner scope) is asserted there, not here.

### 1.9 Fragments and the single-root rule

`VNode` is a single node and the enum is frozen (fact 1), so a `Fragment` variant cannot be added without
redefining it — which IA4 forbids. Two consequences, both forced by the baseline:

- **A top-level `view!` yields exactly one root `VNode`.** Multiple top-level nodes are a compile
  diagnostic that names the problem and suggests wrapping them in a single element (§3). This differs from
  Leptos/Dioxus, which allow top-level fragments; Ferric does not, because its node model has no fragment.
- **In child position, multiple nodes splice.** `{vec_of_vnodes}`, a `<For>`, or a sequence of sibling
  tags all contribute several children to their parent. Fragmentation is a child-list concern, which the
  `Vec<VNode>`-into-`.children(..)` lowering already expresses; it is never a root concern.

### 1.10 Interop, the escape hatch, and whitespace

- **Interop is two-way.** `view!` produces an ordinary `VNode`, usable anywhere the builders are; and a
  builder-produced (or component-produced) `VNode` is spliceable into a view via `{expr}`. An author can
  adopt the macro incrementally and drop to builders for a case the macro does not express.
- **Escape hatch.** Any `{expr}` evaluating to a `VNode` is spliced directly as a child — the explicit
  exit to raw builder code, so the macro never becomes a cage.
- **Whitespace.** Because text is written quoted (§1.2), whitespace and newlines *between* tags are
  insignificant and are discarded; only text inside quotes is rendered. The rule is simple and documented,
  so the rendered text is exactly what the author quoted — no surprising collapsed or injected spaces.

---

## 2. Lowering onto `VNode` (what it produces — additive, nothing redefined)

The macro is defined by the tree it produces, stated as *what it produces*, not how the expansion is
written. Every row below lowers onto a frozen constructor; no frozen item is redefined (identity IA4,
parent `REQ-FW-009`).

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
| `<Capitalized … />` | the component model's invocation form (band B / IA2), yielding a `VNode` spliced as a child |
| the element at the end of a `view!` | `.into()` to a `VNode` (`From<VElement> for VNode`) |

The counter's hand-built tree and the `view!` version of §1.1 produce byte-identical `VNode`s; this
equivalence is the additivity check (§3, `REQ-API-023`).

The macro and the `vdom::text` helper are exported additively. `text` is in the `vdom` module but not in
today's frozen `prelude`; adding `view!` and re-exporting `text` into the prelude are additive changes (new
items), which `REQ-FW-009` permits — no existing export is removed or changed.

---

## 3. Compile-time diagnostics (the `trybuild`-checkable bar)

Much of the day-to-day feel of a macro is what happens when the author gets it wrong (parent `REQ-FW-014`).
The bar is that a malformed view produces an error that names the author's mistake **in terms of their
code**, at the span of the offending tokens — not a wall of internal macro errors. The bar is checkable with
`trybuild`: a fixture of malformed views, each with an expected `stderr`, is the automated test (IA6).

| Author mistake | Expected diagnostic (at the author's span) |
|---|---|
| Unclosed element — `<div>` with no `</div>` | "unclosed element `<div>`" pointing at the open tag |
| Mismatched close — `<div> … </span>` | "closing tag `</span>` does not match open tag `<div>`" |
| Multiple top-level nodes in one `view!` | "a `view!` must have a single root element; wrap these in one element" |
| Dynamic attr / text value not `Into<String>` | type error reported at the `{expr}` span, naming the required `Into<String>` |
| Unknown event name — `on:klick=` | "unknown event `klick`; bound events are: click, input" (the list grows with `EventKind`) |
| Handler value is not a closure | "`on:click` expects a handler closure" at the value span |
| `<For>` item without a key | "list item needs `key={…}` for keyed reconciliation" at the item (best-effort; see note) |
| Capitalized tag with no such component in scope | the ordinary "cannot find `TodoList` in this scope" at the tag span |

Two limits the bar states rather than overselling:

- **Keyless-list detection is best-effort.** The macro can flag a missing `key` on the direct `<For>`
  form, where the item element is syntactically visible. It cannot catch every keyless list built by an
  arbitrary `{iter.map(..)}` expression, because the elements are produced by opaque Rust the macro does
  not see into. For that case the bar is a documented convention plus the `<For>` form that makes keying
  the default — not a guarantee the macro catches every case.
- **No handler-identity diagnostics.** The runtime cannot compare closures (fact 4), so the macro promises
  nothing about handler-equality; it only guarantees the handler lowers to a `.on(kind, closure)` call.

---

## 4. Peer view-macros, compared by name

All four Rust peers provide a declarative view macro; they differ in syntax flavor and — more consequentially
— in reactivity model. Comparison rests on their documented public behavior.

| Peer | Syntax flavor | Reactivity model | Keyed lists | Bearing on Ferric |
|---|---|---|---|---|
| **Leptos `view!`** | Angle-bracket HTML-like; `on:click=`, `class:` directives, attribute shorthand `{x}` | Fine-grained signals, **no VDOM** — an interpolation is a fine-grained binding | `<For each key let:item>` | The flavor Ferric follows; but Ferric's VDOM re-render is *not* Leptos's fine-grained binding — the key difference (§1.4) |
| **Yew `html!`** | JSX-like angle brackets; `{ expr }` blocks, `onclick={..}` | React-like **VDOM** + diff | `key={..}` per item | Closest to Ferric's model (VDOM + macro); informs the single-node/`key` design |
| **Dioxus `rsx!`** | Rust-struct-like — `div { class: "x", onclick: .., "text" }` | React-like **VDOM** + diff | `key: ..` per item | A considered flavor; rejected for the HTML-like one, but the VDOM model is shared |
| **Sycamore `view!`** | Terse — `div(class="x") { "text" }`, `on:click=` | Fine-grained signals, no VDOM | keyed `Keyed`/`Indexed` views | A considered flavor; same fine-grained caveat as Leptos |
| **Solid / Vue 3 (JS analogs)** | JSX / templates | Solid fine-grained; **Vue 3 signals + VDOM** | keyed `For` / `v-for :key` | Vue 3 is Ferric's closest architectural analog (signals *and* a VDOM) |

The ergonomic trade-offs:

- **Flavor** is the least consequential axis. Angle brackets (Leptos/Yew) read like markup; Dioxus's
  struct style and Sycamore's terse style are quieter and more Rust-native but read less like HTML. Ferric
  picks angle brackets to match the mental model of an author evaluating it against JS frameworks (§1.1).
- **Reactivity model** is the consequential axis, and it is where the design must be precise with the
  author. Leptos and Sycamore update exactly the one text node an interpolation feeds, without
  re-running the component;
  Ferric, like Yew/Dioxus/Vue 3, re-runs the component and diffs. An author porting a Leptos mental model
  will expect fine-grained updates and must be told, up front, that Ferric's `{expr}` triggers a
  component re-render reconciled by the keyed diff (§1.4). The macro is equally ergonomic to write; the
  performance characteristics differ, and the performance area (`REQ-PERF-*`) measures the difference
  rather than this section claiming it away.
- **Keyed lists** converge: every peer makes the author supply a key. Ferric's constraint is sharper
  because its diff only keys a sibling list when *all* siblings are keyed (fact 3), which is why the
  `<For>` form bakes the key in rather than leaving it optional.

---

## 5. Requirements register — `REQ-API-001 … REQ-API-029`

Each requirement states what must be true from an app author's side, with acceptance criteria a stranger
could check. `verification_method` ∈ {`automated_test`, `example_build`, `doc_inspection`} (inherited vocab,
IA6). All are `release_gating: true`. Stage is `usable_early` (the declarative authoring model is the
early-usable floor, parent `REQ-FW-005`/`REQ-FW-014`). Ids are zero-padded, monotonic within band 001–029
(IA1). Cross-references to `REQ-FW-*`, `REQ-ASYNC-*`, and bands B/C are read-only.

### A. The macro and element/text/attribute surface

**REQ-API-001 — A `view!` macro is the declarative authoring entry point.**
- *Statement:* An author can describe an element tree declaratively with a `view!` macro instead of
  hand-building `VElement` builder chains.
- *Acceptance:* `view! { <div class="counter"><p>"hi"</p></div> }` compiles and evaluates to a `VNode`
  equal to the equivalent builder tree. *(automated_test, example_build)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

**REQ-API-002 — Element nodes (open/close and self-closing) lower to `VElement::new(tag)`.**
- *Statement:* `<tag>…</tag>` and `<tag/>` produce an element with that tag.
- *Acceptance:* `<br/>` produces `VElement::new("br")`; `<div>…</div>` produces a `div` with the nested
  children in order. *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

**REQ-API-003 — Text children lower to `vdom::text`.**
- *Statement:* A quoted string literal, and a `{expr}` whose value is `impl Into<String>`, each produce a
  text node.
- *Acceptance:* `<p>"count: " {n.to_string()}</p>` produces two text children, `"count: "` and the value
  of `n.to_string()`. *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

**REQ-API-004 — Static and dynamic attributes lower to `.attr(name, value)`.**
- *Statement:* `name="literal"` and `name={expr}` (expr `Into<String>`) set an attribute.
- *Acceptance:* `<a href="/x" class={c}>` produces attrs `("href","/x")` and `("class", c.into())`; the
  example app compiles and renders those attributes. *(automated_test, example_build)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

**REQ-API-005 — Nesting and mixed children lower to ordered `.child` calls.**
- *Statement:* Nested elements and interleaved text/element children appear as children in source order.
- *Acceptance:* a `<div>` containing text, an element, and an interpolation produces three children in the
  written order. *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

### B. Events

**REQ-API-006 — `on:<name>={closure}` lowers to `.on(EventKind::<Variant>, closure)`.**
- *Statement:* An author binds an event with `on:click`/`on:input`, supplying a `Fn()` closure.
- *Acceptance:* `<button on:click={h}>` produces one event binding `(EventKind::Click, _)` whose closure,
  when invoked, runs `h`; the counter example built with the macro increments on click. *(automated_test,
  example_build)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005, REQ-FW-014.

**REQ-API-007 — The event-name set is open and additive.**
- *Statement:* The handler grammar maps an event-name token to an `EventKind` variant; `click`/`input`
  resolve today, and additional names resolve as `REQ-ASYNC-*` extends `EventKind`, with no change to the
  macro grammar.
- *Acceptance:* `on:click` and `on:input` compile against the baseline; a doc note states that new event
  names become available when `EventKind` gains the variant (no macro change). An unmapped name fails per
  REQ-API-026. *(doc_inspection, automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-ASYNC-\* (read-only), REQ-FW-006.

### C. Reactivity

**REQ-API-008 — Interpolated reactive values re-render on change.**
- *Statement:* A `{expr}` that reads a `Signal`/`Memo` inside a rendered view re-renders the component when
  that signal changes, because the read subscribes the mount effect.
- *Acceptance:* a headless `wasm-bindgen-test` mounts a component with `<p>{count.get()}</p>`, calls
  `count.set(..)`, and observes the rendered text update. *(automated_test, example_build)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

**REQ-API-009 — The reactivity model is stated as coarse-grained (component re-render + keyed diff).**
- *Statement:* The docs state that a signal read in a view re-renders the whole component, reconciled by
  the keyed diff, and that Ferric provides no fine-grained per-node binding — so an author does not expect
  Leptos/Sycamore fine-grained behavior.
- *Acceptance:* a reviewer confirms the authoring guide states the coarse-grained model and contrasts it
  with fine-grained peers. *(doc_inspection)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005; REQ-PERF-\* (read-only).

### D. Control flow

**REQ-API-010 — Conditional rendering yields a `VNode`, with an explicit empty node.**
- *Statement:* A Rust `if`/`match`/ternary in interpolation position produces a `VNode`; the "render
  nothing" branch produces an explicit empty node.
- *Acceptance:* a conditional view compiles with both branches producing a `VNode`, and the empty branch
  renders no visible content. *(automated_test, example_build)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

**REQ-API-011 — Kind/tag-changing conditionals reconcile as a `Replace`.**
- *Statement:* When a conditional's branches differ in node kind or tag, toggling re-renders that position
  as a wholesale replacement, and this is documented.
- *Acceptance:* a test toggles a conditional between `<span>` and `<a>` and observes a `Replace`-shaped
  patch (the subtree is rebuilt); the guide states this. *(automated_test, doc_inspection)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

### E. Lists and keys

**REQ-API-012 — A keyed-list form produces a `Vec<VNode>` spliced via `.children`.**
- *Statement:* A `<For each key let:item>` form iterates items and produces a child list.
- *Acceptance:* a `<For>` over three items produces a `<ul>` with three `<li>` children in order; the
  example renders the list. *(automated_test, example_build)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

**REQ-API-013 — The keyed-list form produces a fully-keyed sibling list.**
- *Statement:* Every element the list form produces carries its key, so the sibling list satisfies the
  diff's `all_keyed` precondition and reconciles by identity (insert/move/remove).
- *Acceptance:* reordering the item collection produces `MoveChild` patches and no `Replace` of keyed
  nodes (mirrors the baseline `keyed_children_reorder_*` behavior). *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

**REQ-API-014 — `key={expr}` lowers to `.key(expr)`; mixing keyed and unkeyed siblings is documented.**
- *Statement:* A standalone `key={expr}` sets an element's key; the guide states that an unkeyed sibling in
  the same parent drops that parent to positional diffing.
- *Acceptance:* `<li key={id}>` produces `.key(id)`; a reviewer confirms the mixing caveat is documented.
  *(automated_test, doc_inspection)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

### F. Component invocation (the IA2 macro side)

**REQ-API-015 — Capitalized tag = component; lowercase tag = HTML element.**
- *Statement:* The macro routes a capitalized tag to a component invocation and a lowercase tag to an HTML
  element, by the tag token alone.
- *Acceptance:* `<div/>` produces an element; `<TodoList/>` is treated as a component invocation (resolves
  to the in-scope component item). *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005; band B (IA2).

**REQ-API-016 — A macro prop `name={value}` corresponds to a declared prop.**
- *Statement:* Passing `name={value}` on a component tag maps to a prop the component declares (band B).
- *Acceptance:* a stated example passes a prop through the macro to a component that declares it, and it
  compiles and renders. *(example_build, automated_test)* — closure asserted by synthesis (IA2).
- *Stage:* usable_early · *Gating:* true · *Refs:* band B (IA2).

**REQ-API-017 — Children nested in a component element correspond to its declared children acceptance.**
- *Statement:* Nesting children inside `<Comp>…</Comp>` maps to the component's declared `children`.
- *Acceptance:* a stated example nests children into a component that declares children; it compiles and
  renders. *(example_build)* — closure asserted by synthesis (IA2).
- *Stage:* usable_early · *Gating:* true · *Refs:* band B (IA2).

**REQ-API-018 — A `<slot:name>` fill corresponds to a component-declared named slot.**
- *Statement:* Filling `<slot:name>…</slot:name>` maps to a named slot the component declares.
- *Acceptance:* a stated example fills a named slot of a component that declares it; it compiles and
  renders into the slot position. *(example_build)* — closure asserted by synthesis (IA2).
- *Stage:* usable_early · *Gating:* true · *Refs:* band B (IA2).

**REQ-API-019 — A component invocation lowers to the component model's invocation form, yielding a `VNode`.**
- *Statement:* The macro splices the `VNode` the component model's invocation form produces; it does not
  construct the component or redefine the component model.
- *Acceptance:* the macro's component-invocation output is a `VNode` child; no frozen component API is
  redefined (checked with REQ-API-023 / IA4). *(automated_test, doc_inspection)*
- *Stage:* usable_early · *Gating:* true · *Refs:* band B (IA2), REQ-FW-009 (IA4).

### G. Fragments, interop, additivity

**REQ-API-020 — A top-level `view!` yields exactly one root node.**
- *Statement:* Multiple top-level nodes are rejected with a diagnostic (forced by the frozen single-node
  `VNode`).
- *Acceptance:* a single-root `view!` compiles; a two-root `view!` fails per REQ-API-024's multi-root case.
  *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-009 (IA4).

**REQ-API-021 — Child-position splicing of multiple nodes and the `VNode` escape hatch.**
- *Statement:* `{Vec<VNode>}`, `<For>`, and sibling tags splice multiple children; any `{expr}` yielding a
  `VNode` is spliced directly.
- *Acceptance:* a view with `{vec_of_vnodes}` renders each as a child; a `{builder_vnode}` splice renders
  the builder-produced node. *(automated_test, example_build)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

**REQ-API-022 — Two-way interop with the builder API.**
- *Statement:* `view!` output is an ordinary `VNode` usable anywhere the builders are, and builder-produced
  `VNode`s are usable inside a view via interpolation.
- *Acceptance:* a `view!`-produced node is passed to `.child(..)` of a builder tree and vice versa, both
  compile and render. *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-009.

**REQ-API-023 — Every construct lowers additively onto the frozen surface; nothing is redefined (IA4).**
- *Statement:* All macro output is built from the frozen `VNode`/`VElement`/`EventKind`/`EventHandler`
  constructors and the frozen `prelude`; added items (`view!`, a re-exported `text`) are additive only.
- *Acceptance:* a `view!` tree and the equivalent hand-built tree produce equal `VNode`s; an app written
  against the baseline `prelude` still compiles with the macro present (no removed/redefined export).
  *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-009 (IA4).

### H. Diagnostics (the `trybuild`-checkable bar, IA6)

**REQ-API-024 — Structural view errors produce a diagnostic at the author's span.**
- *Statement:* Unclosed elements, mismatched closing tags, and multiple top-level nodes each produce an
  error that names the problem at the offending tokens.
- *Acceptance:* `trybuild` fixtures for each case produce the expected `stderr` naming the tag/problem.
  *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-014.

**REQ-API-025 — A wrong-typed attribute or text value is diagnosed at the expression span.**
- *Statement:* A dynamic attribute or text interpolation whose value is not `Into<String>` produces a type
  error pointing at the `{expr}`, naming the required conversion.
- *Acceptance:* a `trybuild` fixture with a non-string attr value fails with the error located at the
  expression. *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-014.

**REQ-API-026 — An unknown event name is diagnosed with the bound set.**
- *Statement:* `on:<name>` with no matching `EventKind` variant produces an error naming the unknown event
  and listing the bound kinds.
- *Acceptance:* a `trybuild` fixture `on:klick=` fails with "unknown event `klick`; bound events are:
  click, input". *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-014, REQ-ASYNC-\* (read-only).

**REQ-API-027 — The keyless-list case is diagnosed best-effort, with its limit documented.**
- *Statement:* The direct `<For>` form flags a missing `key`; the docs state that an arbitrary
  `{iter.map(..)}` list cannot be fully checked and that the `<For>` form is the keyed default.
- *Acceptance:* a `trybuild` fixture for a keyless `<For>` fails with a "needs `key`" diagnostic; a
  reviewer confirms the documented limit. *(automated_test, doc_inspection)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-014.

**REQ-API-028 — The diagnostics story as a whole is `trybuild`-checkable (IA6).**
- *Statement:* A fixture suite of malformed views, each with a committed expected `stderr`, is part of the
  test suite.
- *Acceptance:* `cargo test` runs the `trybuild` suite and all expected-failure fixtures match their
  committed `stderr`. *(automated_test)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-014.

### I. Whitespace

**REQ-API-029 — Whitespace handling is predictable and documented.**
- *Statement:* Only quoted text is rendered; whitespace and newlines between tags are insignificant and
  discarded, and the rule is documented.
- *Acceptance:* a view formatted across several indented lines renders only its quoted text with no
  injected or collapsed spaces; a reviewer confirms the documented rule. *(automated_test, doc_inspection)*
- *Stage:* usable_early · *Gating:* true · *Refs:* REQ-FW-005.

---

## 6. Traceability and metadata

- **Owns:** `REQ-API-001 … REQ-API-029` (band A; contract `../contracts/req_api_partition.yaml`, identity
  IA1). No id outside the band is minted here.
- **Specializes (read-only):** parent `REQ-FW-005` (declarative authoring model), `REQ-FW-009` (additive
  over frozen surfaces), `REQ-FW-014` (actionable diagnostics) — `../SUBTASK_scope_and_requirements/scope-and-requirements.md`.
- **Composes against (not redefined):** the component model, band B
  `../SUBTASK_components_props_slots/` across invocation seam **IA2** (§1.7, REQ-API-015..019); context,
  band C `../SUBTASK_context/` across context seam **IA3** (§1.8). Closure of both seams is asserted by the
  subtree synthesis gate, not here.
- **Cross-area references (read-only):** `REQ-ASYNC-*` (the additive `EventKind` set and the
  event-payload handler form), `REQ-PERF-*` (the cost of the coarse-grained re-render model).
- **Identities this section upholds:** IA1 (band discipline), IA2 (macro side of the invocation seam),
  IA4 (additive over the frozen surface), IA6 (`trybuild`-checkable diagnostics + inherited
  `verification_method` on every criterion).
- **Conforms to:** `../../contracts/id_and_traceability_schema.yaml` (REQ fields, `stage`, `release_gating`,
  `verification_method`) and `../contracts/req_api_partition.yaml` (band + authoring seam).
- **Grounding:** `Nousix-LLC/nswe-demo` @ `276138f`, baseline checkout
  `taskflow/dags/ferric-foundation/checkout/crates/ferric/` (`vdom.rs`, `component.rs`, `signal.rs`,
  `dom.rs`, `lib.rs`, `examples/counter.rs`).
- **Folds into:** `../authoring-model.md` at synthesis (`SUBTASK_synthesis`), as the macro section and its
  slice of the merged `REQ-API-*` register.
