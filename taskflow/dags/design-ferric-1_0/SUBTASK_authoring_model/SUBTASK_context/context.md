# Context — sharing state down the tree without prop drilling

*Ferric 1.0 authoring model, section C. Design, not implementation: this states the authoring surface an
author writes and the bar it must meet, not how the lookup is built. Owns the `REQ-API-060 … 079` band.*

## Summary

Today a value shared by many components must be passed as a prop through every component between the one that
owns it and the one that uses it. A toolbar button that toggles a theme owned by the app root has to receive
the theme through every intermediate component, even those that never touch it. Context removes that threading:
an ancestor **provides** a value to its subtree, and any descendant **reads** it directly from inside its own
body, typed by the value's type.

Ferric's context is three functions added to `ferric::prelude`:

```rust
// Additive over the frozen prelude. Provide into the current reactive owner scope;
// read by walking ancestor owner scopes, nearest first.
pub fn provide_context<T: Clone + 'static>(value: T);
pub fn use_context<T: Clone + 'static>() -> Option<T>;   // None when no ancestor provided `T`
pub fn expect_context<T: Clone + 'static>() -> T;        // panics with a located message when absent
```

The value is keyed by its Rust type. `provide_context::<Theme>(..)` makes a `Theme` available to the subtree;
`use_context::<Theme>()` retrieves it with no provider-is-missing surprise (`None`), and `expect_context::<Theme>()`
is the convenience for the common case where a provider is required, returning `T` and panicking with a message
that names the missing type when none is found. This split follows Leptos exactly (`use_context -> Option<T>`,
`expect_context -> T`); the reasons are in [§Design decisions](#design-decisions-and-peer-comparison).

Context carries a value; it is not itself reactive. When the provided value is a `Signal<T>` or `Memo<T>` — the
normal case for shared mutable state — a consumer that reads the handle inside its body re-renders on change,
because the read tracks the signal, not because the lookup tracks anything. The lifetime of a provided value is
bounded by the reactive owner scope it was provided into: when that scope is disposed, the entry is released
and no stale reference survives, which is the same ownership tree and the same `no_stale_subscriber_leak`
property the baseline reactive runtime already guarantees (`crates/ferric/src/signal.rs`).

---

## The authoring surface — what the author writes

### Provide and read

An ancestor provides a value in its body; a descendant reads it in its body, however deep. Nothing in between
declares or forwards it.

```rust
use ferric::prelude::*;

// Shared app state. `Signal` is `Copy`, so a `Theme` is a cheap handle to carry through context.
#[derive(Clone, Copy)]
struct Theme {
    dark: Signal<bool>,
}

// App root: own the state, provide it to the whole subtree, then render children.
fn app() -> VNode {
    let theme = Theme { dark: create_signal(false) };
    provide_context(theme);          // visible to every descendant from here down
    view! { <Toolbar /> }            // Toolbar and its descendants receive nothing explicitly
}

// A deeply nested component reads the theme directly — no prop was threaded to reach it.
fn theme_toggle() -> VNode {
    let theme = expect_context::<Theme>();
    view! {
        <button on:click=move |_| theme.dark.update(|d| *d = !*d)>
            { move || if theme.dark.get() { "Switch to light" } else { "Switch to dark" } }
        </button>
    }
}
```

The `view!` forms (`<Toolbar />`, `on:click`, the interpolated closure) are fixed by the sibling view-macro and
component sections; this section composes against them only at the point that matters for context — that
`provide_context` and `use_context`/`expect_context` are ordinary calls in a component body (see
[§The context seam](#the-context-seam-ia3), identity IA3).

### The no-provider case, stated

A lookup with no matching provider is a case the author handles, not a silent default. `use_context` returns
`None` so a component can render a fallback; `expect_context` is for when a provider is a precondition, and its
panic names the type so the author can see what was not provided.

```rust
// Optional context: render a fallback when no provider exists.
fn maybe_themed() -> VNode {
    match use_context::<Theme>() {
        Some(theme) => render_with(theme),
        None        => render_default(),      // no ancestor provided a Theme
    }
}

// Required context: fail loudly and locatably rather than limp on a wrong default.
fn requires_theme() -> VNode {
    let theme = expect_context::<Theme>();   // panics if absent:
    // panicked at: no context of type `my_app::Theme` was found; an ancestor component must call
    //              `provide_context::<my_app::Theme>(..)` before this component is rendered
    render_with(theme)
}
```

The located panic message is part of the authoring model's diagnostics bar (parent `REQ-FW-014`): a missing
provider is one of the common context mistakes, and the message names the author's type rather than a framework
internal.

### Reactivity flows through the provided handle

Context is a typed channel, not a second reactivity system. The value you provide is whatever you put in; when
it is a reactive handle, change propagation is the handle's, unchanged from reading a signal anywhere else.

```rust
#[derive(Clone, Copy)]
struct Session {
    user: Signal<Option<UserId>>,
}

fn nav_bar() -> VNode {
    let session = expect_context::<Session>();
    view! {
        // Reading `session.user` inside this body subscribes this component's render effect to the
        // signal, so a later `session.user.set(..)` from anywhere re-renders `nav_bar`. The context
        // lookup itself established no dependency — only the signal read did.
        <span>{ move || match session.user.get() {
            Some(id) => format!("signed in as {id}"),
            None     => "signed out".to_string(),
        } }</span>
    }
}
```

This is the distinction an author relies on: `use_context::<Session>()` resolves the same `Session` every render
(looking it up is not a reactive dependency), and the UI tracks `session.user` because the body reads that
signal. Providing a plain, non-reactive value (say a `Config`) is equally valid; it simply never changes, so no
consumer re-renders on its account.

### Scoped cleanup

A provided value lives exactly as long as the reactive owner scope it was provided into. When a subtree is
disposed — a component unmounts, a conditional branch is torn down — the context entries provided within it are
released with the scope, the same disposal that unsubscribes that scope's effects and memos. A reader outside a
disposed scope never observes a value from it, and no released value is reachable afterward.

```rust
// `show` gates a subtree. While it is true, `Panel` is mounted under its own owner scope and may
// provide panel-local context. When `show` flips to false the subtree is disposed: its provided
// `PanelState` is released together with the scope's effects — the same drop that the baseline
// `no_stale_subscriber_leak` test exercises for effects and memos.
fn container() -> VNode {
    let show = create_signal(true);
    view! {
        { move || if show.get() { view! { <Panel /> } } else { view! { <Empty /> } } }
    }
}
```

Tying context lifetime to the owner scope is what keeps "shared state" from becoming "state that outlives the
part of the UI it belonged to." It reuses the baseline `ReactiveScope` owner tree directly (see
[§Sitting on the baseline](#sitting-on-the-baseline-reactive-runtime)); context adds no second lifetime rule to
reason about.

---

## Design decisions and peer comparison

Each decision is stated against how the named peer frameworks make it, with the trade-off, so a reviewer can
check the choice rather than take it on assertion.

### Type-keyed lookup, not an explicit context handle

Ferric keys context by the value's Rust type: `use_context::<T>()` finds the nearest ancestor-provided `T`. This
is the convention across the Rust peers — Leptos `provide_context`/`use_context::<T>()`, Dioxus
`use_context_provider`/`use_context::<T>()` (keyed by `TypeId`), Sycamore `provide_context`/`use_context::<T>()`,
and Yew's `use_context::<T>()` — and it composes with Ferric's `Copy` signal handles: you provide a `Signal<T>`
(or a small `Copy`/`Clone` struct of them) and read it back by type with no wrapper object to carry.

The alternative is Solid's model: `createContext(default)` returns an explicit `Context` object that the author
passes to `useContext(ctx)` and to a `<Provider>`. The trade-off is real and goes both ways. The explicit handle
lets two providers of the *same* underlying type coexist (they are different context objects) and it carries a
compile-time default; type-keyed lookup cannot distinguish two `Signal<bool>`s provided as "context" without a
newtype. Ferric takes the type-keyed side because the Rust newtype is the idiomatic way to say "these two
booleans are different things" (`struct Theme(Signal<bool>)`, `struct Sidebar(Signal<bool>)`), and because the
explicit-handle model adds a `Context` object the author must route to every provider and reader — the prop
threading context exists to remove, reintroduced one level up. The newtype cost is small and local; the handle
cost is paid at every use site.

### `use_context -> Option<T>` plus `expect_context -> T`

Ferric offers both a fallible read and an infallible one, matching Leptos (`use_context -> Option<T>`,
`expect_context -> T`). Dioxus and Sycamore make the plain `use_context::<T>()` panic on a missing provider and
offer `try_use_context -> Option<T>` for the fallible path. The two designs cover the same two needs; they differ
only in which one is the unadorned name.

Ferric makes the fallible read the plain `use_context` for one reason: the name an author reaches for first
should not be the one that panics. A component that reaches for context it did not set up gets a `None` to match
on, not a crash, and opts into the panic explicitly by writing `expect_context` — the same shape as `Option::unwrap`/
`expect` that every Rust author already reads correctly. The cost is a slightly longer call for the common
required-context case (`expect_context` rather than `use_context`); that is the right thing to make explicit.

### Value bound `T: Clone + 'static`; read clones out

`use_context`/`expect_context` return `T` by cloning the stored value out, requiring `T: Clone + 'static`. This
matches the `Clone` bound Leptos, Sycamore, and Dioxus all place on context values. For Ferric the bound is close
to free in the case that matters: `Signal<T>` and `Memo<T>` are `Copy` (`crates/ferric/src/signal.rs`), so a
context value is normally a handle or a small struct of handles, and the clone is a key copy, not a deep copy of
the underlying state. An author who wants to share a large owned value without cloning it provides a `Signal` of
it (or an `Rc`) and reads the handle — the same move the reactive model already asks for.

### Nearest-ancestor resolution, with shadowing

When the same type is provided at more than one level, `use_context::<T>()` resolves to the nearest ancestor that
provided it; an inner provider shadows an outer one for its own subtree only. This is the shared behavior of the
Rust peers (Leptos's `Provider` provides to descendants without overwriting an outer same-type context except
within its subtree; Sycamore scopes context per reactive scope). It lets a subtree override app-wide context —
a modal that provides a restricted `Session`, say — without disturbing the rest of the tree.

---

## Sitting on the baseline reactive runtime

Context introduces no new lifetime model. It reuses the ownership tree the baseline already maintains in
`crates/ferric/src/signal.rs`:

- The runtime keeps an **owner stack**; every reactive node records the owner that created it, and an owner holds
  its children for disposal (`Node.owner`, `Node.children`, `Runtime::owner_stack`). A component renders inside a
  `create_effect`, so while a component body runs there is a current owner on that stack — the scope context
  attaches to and reads from.
- `provide_context::<T>(v)` records `v` against the current owner scope, keyed by `TypeId::of::<T>()`.
  `use_context::<T>()` walks the `owner` parent chain from the current scope outward and returns the first `T` it
  finds (nearest-ancestor resolution), or `None`.
- Disposal already releases everything a scope owns and detaches it from every subscriber and source set
  (`Runtime::dispose`, the `no_stale_subscriber_leak` identity). A scope's provided context entries are owned by
  the scope node, so the same `dispose` that unsubscribes the scope's effects releases its context — one disposal
  path, not two.

This keeps the crate-internal `ReactiveScope` exactly as it is: still `pub(crate)`, still the disposer the frozen
public API does not expose. Context does not promote it or hand the author a scope handle. The author's surface is
the three free functions; the owner scope they bind to is the one the runtime already pushes around a rendering
component.

### Additive over the frozen surface

Everything here is additive, so parent `REQ-FW-009` (frozen surfaces carried forward) and identity IA4 hold:

- `provide_context`, `use_context`, `expect_context` are **new** items added to `ferric::prelude`. No existing
  prelude item (`create_signal`, `create_memo`, `create_effect`, `batch`, `Signal`, `Memo`, `Component`, `mount`,
  `VNode`, `VElement`, `EventKind`) changes signature or meaning.
- The internal reactive `Node` gains an internal, per-owner typed context store. This is a private runtime detail,
  not part of the frozen public surface; no public type's shape changes.
- `ReactiveScope` stays crate-internal. An app written against the baseline prelude still compiles; it simply has
  three more functions available.

---

## REQ-API register — context (band 060–079)

Ids are zero-padded 3-digit and monotonic within the band (identity IA1). Every acceptance criterion names a
`verification_method` from the inherited vocabulary (`automated_test` | `example_build` | `doc_inspection`;
identity IA6), and conforms to `../../contracts/id_and_traceability_schema.yaml`. All are `stage: usable_early`
(context is part of the early-usable authoring floor per `REQ-FW-005`, §5.2) and `release_gating: true` unless
noted.

---

### REQ-API-060 — Provide a value to a subtree
- **Statement:** An author can make a value available to an entire component subtree by calling
  `provide_context(value)` once in an ancestor component body, without passing it as a prop to any intermediate
  component.
- **Rationale:** This is the capability `REQ-FW-005` names ("read a value provided by an ancestor via context
  without threading it through every call") and the baseline authoring model lacks entirely. Every peer provides
  it (Leptos/Sycamore `provide_context`, Dioxus `use_context_provider`, Yew `ContextProvider`, Solid `Provider`).
- **Acceptance criteria:** An example in which a root component calls `provide_context(v)` and a descendant three
  or more components deep reads `v`, with no intermediate component declaring or forwarding it, compiles and
  renders the value. **Verification:** `example_build`.
- **Stage:** `usable_early` · **Release gating:** true · **References:** `REQ-FW-005`.

### REQ-API-061 — Read a provided value without prop drilling
- **Statement:** An author can read a provided value from inside any descendant component body with
  `use_context::<T>()`, which returns `Option<T>`.
- **Rationale:** The read side of context; returning `Option<T>` makes "no provider" an ordinary value the author
  handles rather than a crash. Matches Leptos `use_context -> Option<T>` and Yew's `Option`-returning hook.
- **Acceptance criteria:** A headless test provides a `T`, reads it via `use_context::<T>()` in a nested
  component, and asserts the returned `Some(T)` equals the provided value. **Verification:** `automated_test`
  (headless `wasm-bindgen-test`).
- **Stage:** `usable_early` · **Release gating:** true · **References:** `REQ-FW-005`.

### REQ-API-062 — Typed lookup keyed by the value's type, nearest-ancestor resolution
- **Statement:** Context is keyed by the value's Rust type: `use_context::<T>()`/`expect_context::<T>()` resolve
  to the nearest ancestor that provided a value of type `T`; a provider in an inner scope shadows an outer
  provider of the same type for that inner subtree only.
- **Rationale:** Type-keying is the Rust-peer convention (Leptos, Dioxus `TypeId`, Sycamore, Yew) and composes
  with `Copy` signal handles; nearest-ancestor shadowing lets a subtree override app-wide context without
  disturbing siblings.
- **Acceptance criteria:** A headless test provides `T` at an outer scope and a different `T` value at an inner
  scope, then asserts a reader in the inner subtree sees the inner value and a reader outside it sees the outer
  value. A second case asserts two distinct types provided at one scope are both readable. **Verification:**
  `automated_test`.
- **Stage:** `usable_early` · **Release gating:** true.

### REQ-API-063 — The no-provider case is explicit and located
- **Statement:** When no ancestor provided type `T`, `use_context::<T>()` returns `None`, and
  `expect_context::<T>()` panics with a message that names `T` and states that an ancestor must provide it.
- **Rationale:** A missing provider is a common authoring mistake; the behavior must be a value to match on or a
  located failure, not a wrong default or an opaque crash (parent `REQ-FW-014`). Leptos's `expect_context` and
  Sycamore's panicking `use_context` set the precedent for the located-panic half.
- **Acceptance criteria:** A test with no provider asserts `use_context::<T>()` is `None`. A second case asserts
  `expect_context::<T>()` panics and that the panic message contains the type name of `T`. **Verification:**
  `automated_test`.
- **Stage:** `usable_early` · **Release gating:** true · **References:** `REQ-FW-014`.

### REQ-API-064 — A provided reactive value drives consumer re-render
- **Statement:** When the provided value is or contains a `Signal<T>`/`Memo<T>`, a consumer that reads that handle
  inside its body re-renders when the handle changes, exactly as if the handle had been obtained any other way.
- **Rationale:** Context must compose with reactivity rather than bypass it; shared *mutable* state is the main
  use, and it works by providing a reactive handle, not by making the lookup reactive. Matches Leptos/Solid, where
  context identity is stable and reactivity lives in the provided signal.
- **Acceptance criteria:** A headless test provides a struct holding a `Signal`, renders a consumer that reads the
  signal, mutates the signal from outside the consumer, and asserts the consumer re-rendered with the new value.
  **Verification:** `automated_test`.
- **Stage:** `usable_early` · **Release gating:** true · **References:** `REQ-FW-005`.

### REQ-API-065 — Context lookup is not itself a reactive dependency
- **Statement:** Calling `use_context`/`expect_context` establishes no reactive subscription; a consumer re-renders
  only because of the signals it reads from the returned value, not because it performed a lookup.
- **Rationale:** States the boundary an author relies on, so that resolving context every render is cheap and does
  not spuriously re-run effects; distinguishes "the lookup" from "the signal read" (the half authors most often
  conflate).
- **Acceptance criteria:** A headless test provides a non-reactive value (no signal), reads it via `use_context` in
  a component, and asserts the component does not re-render when unrelated signals change; a `doc_inspection`
  confirms the guide states the lookup is untracked. **Verification:** `automated_test`.
- **Stage:** `usable_early` · **Release gating:** true.

### REQ-API-066 — Context is readable from inside a component body (seam IA3)
- **Statement:** `provide_context` and `use_context`/`expect_context` are callable from inside a component body —
  the unit the `view!` macro renders — not only at a special mount entry point.
- **Rationale:** This is the authoring-seam correspondence IA3 with the component/macro sections: context is read
  from the same place props and children are, so a component is a self-contained unit that can both consume and
  provide context.
- **Acceptance criteria:** An example in which a function component rendered by `view!` both calls
  `expect_context` to read and `provide_context` to provide to its own children compiles and renders. A
  `doc_inspection` confirms the context section and the component section agree that context calls occur in a
  component body. **Verification:** `example_build`.
- **Stage:** `usable_early` · **Release gating:** true.

### REQ-API-067 — App-global context from the application root
- **Statement:** An author can provide context at the application root (the top-level component mounted by
  `mount`) and read it from any component in the application, establishing app-wide shared state.
- **Rationale:** The common case — a theme, a session, a router handle shared by the whole app — must be reachable
  without a dedicated global; the mount root is a reactive owner scope, so a root `provide_context` covers the
  whole tree. Requires no change to `mount`'s signature (additive; IA4).
- **Acceptance criteria:** An example that calls `provide_context` in the root component and reads it from a leaf,
  built and mounted via the existing `mount`, renders the shared value. **Verification:** `example_build`.
- **Stage:** `usable_early` · **Release gating:** true · **References:** `REQ-FW-009`.

### REQ-API-068 — Context lifetime is bounded by the reactive owner scope (scoped cleanup, seam IA3)
- **Statement:** A value provided within a reactive owner scope is released when that scope is disposed (its
  component subtree unmounted or its conditional branch torn down); after disposal no provided value from that
  scope is reachable, and no stale reference survives.
- **Rationale:** Shared state must not outlive the part of the UI it belonged to; tying context to the owner scope
  reuses the baseline `ReactiveScope` disposal and the `no_stale_subscriber_leak` property rather than adding a
  second lifetime rule. This is the second half of seam IA3.
- **Acceptance criteria:** A native or headless test provides context inside a scope, disposes the scope, and
  asserts (a) a subsequent lookup does not return the released value and (b) the owner node and its context entry
  are reclaimed — mirroring the baseline `no_stale_subscriber_leak` / `disposing_scope_also_disposes_owned_memo`
  tests in `signal.rs`. **Verification:** `automated_test`.
- **Stage:** `usable_early` · **Release gating:** true · **References:** `REQ-FW-009`.

### REQ-API-069 — Context surface is additive over the frozen prelude (IA4)
- **Statement:** `provide_context`, `use_context`, and `expect_context` are added to `ferric::prelude` as new
  items; no existing prelude item changes, and `ReactiveScope` remains crate-internal. An app written against the
  baseline prelude still compiles at 1.0.
- **Rationale:** Parent `REQ-FW-009` and identity IA4 require the frozen foundation surface to be carried forward
  additively; context extends it, never redefines it.
- **Acceptance criteria:** A `doc_inspection` of the diff confirms the three functions are additions and no frozen
  prelude item is removed or re-signed; an `example_build` confirms a program using only the baseline prelude
  items still compiles. **Verification:** `doc_inspection` and `example_build`.
- **Stage:** `usable_early` · **Release gating:** true · **References:** `REQ-FW-009`.

### REQ-API-070 — Value bound and clone-out read semantics
- **Statement:** Context values satisfy `T: Clone + 'static`; `use_context`/`expect_context` return the value by
  cloning the stored entry. The idiomatic value is a `Copy` reactive handle (`Signal`/`Memo`) or a small struct of
  them, so the clone is a handle copy rather than a deep copy of the underlying state.
- **Rationale:** The `Clone + 'static` bound matches Leptos/Sycamore/Dioxus and is close to free for the handle
  case that dominates; an author sharing a large owned value provides a `Signal`/`Rc` of it and reads the handle.
- **Acceptance criteria:** A test provides a `Copy` handle struct, reads it twice via `use_context`, and asserts
  both reads refer to the same underlying signal (a write through one is visible through the other). A
  `doc_inspection` confirms the guide states the `Clone + 'static` bound and the handle idiom. **Verification:**
  `automated_test`.
- **Stage:** `usable_early` · **Release gating:** true.

*Band headroom: `REQ-API-071 … 079` are unassigned, reserved for additive context requirements discovered during
synthesis or implementation.*

---

## The context seam (IA3)

This section closes the contract's context seam (`../contracts/req_api_partition.yaml`, `context_seam`), whose
rule is: *context must be readable from the unit the macro renders (a component), not only at mount; and must not
outlive its owner scope.* Both correspondences hold:

1. **Readable inside a component body.** `provide_context`/`use_context`/`expect_context` are free functions
   called in a component body, which renders inside the current reactive owner scope. The component/macro sections
   render components as `Fn() -> VNode` bodies (seam IA2), so a context call sits in the same place a prop or child
   read does. Covered by REQ-API-066. No form on either side is orphaned: every way context is provided or read is
   a call reachable from a rendered component.
2. **Bounded by the owner scope.** A provided value is owned by the reactive scope it was provided into and
   released by that scope's disposal — the baseline `ReactiveScope` owner tree and `no_stale_subscriber_leak`
   path, with no second lifetime rule. Covered by REQ-API-068.

The design is additive over the frozen surface (REQ-API-069, identity IA4): the only public change is three new
`prelude` functions.

---

## Metadata

- **Section:** C — Context, of the Ferric 1.0 authoring model (`../authoring-model.md` at synthesis).
- **Owns:** `REQ-API-060 … 079`; assigned `060 … 070`, `071 … 079` reserved.
- **Specializes:** parent `REQ-FW-005` (declarative authoring model — the context clause); references
  `REQ-FW-009` (frozen surfaces, additive), `REQ-FW-014` (actionable diagnostics).
- **Baseline grounding:** `crates/ferric/src/signal.rs` (`Signal`/`Memo`/`create_effect`/`ReactiveScope` owner
  tree, `no_stale_subscriber_leak`), `component.rs` (`Fn() -> VNode` components), `lib.rs` (frozen `prelude`).
- **Peers compared by name:** Leptos (`provide_context`/`use_context`→`Option`/`expect_context`, type-keyed, tied
  to the reactive `Owner`), Dioxus (`use_context_provider`/`use_context`/`try_use_context`, `TypeId`-keyed),
  Sycamore (`provide_context`/`use_context` panics/`try_use_context`, scope-tied), Yew (`ContextProvider<T>` +
  `use_context::<T>()`→`Option`), Solid (explicit-handle `createContext`/`useContext`, JS analog).
- **Verification vocabulary:** `automated_test`, `example_build`, `doc_inspection` (inherited; identity IA6).
