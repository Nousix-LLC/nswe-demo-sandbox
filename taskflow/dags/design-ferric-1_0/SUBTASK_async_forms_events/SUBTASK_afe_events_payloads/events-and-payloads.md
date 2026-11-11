# Ferric 1.0 — Full DOM event coverage and the payload-carrying handler form

*Concern 4b of the Ferric 1.0 design (`SUBTASK_async_forms_events` → `SUBTASK_afe_events_payloads`). Owns
`REQ-ASYNC-020..039` and the event-payload handler seam (sub-contract identity J3). Design, not framework
code: every requirement reads as something a stranger could check against the framework, not a chosen data
structure or code path.*

This fragment settles two things an app author needs and today's Ferric does not give them, and states how both
compose with the keyed diff that is already in the tree:

1. **A handler can read the event that triggered it** — an input's current value, the key that was pressed, the
   form that was submitted — while the frozen zero-argument handler form keeps working unchanged. This is the
   **seam** the forms sibling (`SUBTASK_afe_forms_binding`) builds two-way binding on, so it is defined once,
   here.
2. **The range of DOM events an author can bind reaches beyond `click` and `input`** — submit, the keyboard
   events, focus/blur, change, and the long tail of named DOM events — additively over the frozen `EventKind`.

## What Ferric does today (baseline `Nousix-LLC/nswe-demo` @ `276138f`, read from source)

Grounded in `crates/ferric/src/{vdom,dom}.rs` at the baseline so the 1.0 line is drawn against what is real:

- **`EventKind` is a closed enum of two variants** — `Click` and `Input` — deriving
  `Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord` (`vdom.rs`). An author cannot name any other DOM
  event.
- **`EventHandler = Rc<dyn Fn()>` is zero-argument** (`vdom.rs`). A handler takes nothing and returns nothing, so
  it **cannot read the triggering event**: there is no way to get an input's value, a pressed key, or a submit
  target from inside a handler. The builder is `VElement::on(kind, handler: impl Fn() + 'static)`.
- **The runtime already receives the event and throws it away.** `dom.rs::set_events` wraps each handler as
  `Closure::wrap(Box::new(move |_event: web_sys::Event| { handler(); }))` — the `web_sys::Event` is bound and
  then discarded (`_event`). `event_name` and `stash_key` match exhaustively over `{Click, Input}`, and the
  detach loop is hardcoded to `[EventKind::Click, EventKind::Input]`.
- **The keyed diff re-binds by the *set of bound event kinds*.** `vdom.rs::diff_events` collects
  `HashSet<EventKind>` for the old and new element and emits `Patch::SetEvents { path, events }` **only when those
  two sets differ**. Identical sets across a re-render produce no `SetEvents`, so a retained element keeps its
  existing listeners even when the closures differ — which is sound because a signal-based handler reads its
  signals live rather than capturing values at bind time.
- The `vdom.rs` module doc explicitly sanctions this direction: "the DOM layer may additively enrich the handler
  form (e.g. to carry a `web_sys::Event`) when it needs the event payload."

So the capability is latent: the event object already flows into the wrapper and is dropped. The 1.0 work exposes
it to the author's handler and widens which events can be bound — **additively**, never by redefining a frozen
item (sub-contract identity J4; parent `REQ-FW-009`).

## The design decision (what, not how)

**Keep the zero-argument form; add a payload-receiving form beside it.** The frozen
`EventHandler = Rc<dyn Fn()>` and `VElement::on(kind, || …)` stay valid and unchanged — an app written against the
baseline still compiles. Beside them, an author may bind a handler that **receives the triggering event's data**.
The payload is the raw `web_sys::Event` plus small typed accessors for the common reads (an input's value, a
pressed key), rather than a forced typed-event enum. Two reasons drive that choice, and both are checkable
framework properties rather than taste:

- The baseline wrapper already holds a `web_sys::Event`; handing that object to the handler is the smallest
  additive change and is exactly what the module doc sanctioned. A typed-event hierarchy would be a larger
  surface the baseline does not need and would pull the framework toward re-deriving what `web-sys` already
  types.
- Ferric's stated 1.0 position is a lean dependency footprint on `wasm-bindgen`/`web-sys`/`js-sys`
  (`REQ-FW-013`). Exposing `web_sys` event types plus thin helpers keeps that footprint; a bespoke event model
  would not.

**Widen the event surface in two layers:** a first-class set of common DOM events (discoverable, typo-safe at
compile time) *and* an escape hatch that binds any DOM event by name. A closed enum alone cannot name every event
a real app needs (custom events, the less-common ones); a name-only API gives up compile-time discoverability for
the common cases. An author gets both — `EventKind::Click` and friends stay first-class variants, new common
events join them, and any other DOM event is bindable by its name. The concrete shape (new enum variants plus a
named/custom variant, or a parallel registry) is implementation and is left to the code DAG; the author-facing
requirement is the capability and its testable behavior.

One structural fact the author-side re-binding guarantee rests on: the diff detects re-binding by comparing the
**set** of bound events, so whatever identifies an event (enum variant or event name) must remain comparable for
set membership — the widened surface preserves the `Eq`/`Hash` identity the baseline already relies on. This is
stated as rationale for the guarantees in `REQ-ASYNC-024`, not as a mandated data structure.

---

## Requirements (`REQ-ASYNC-020..039`)

Each requirement states what must be true from an app author's side and carries acceptance criteria a reviewer
who never met the author can check. Every criterion names at least one `verification_method` from the parent
schema (`../../contracts/id_and_traceability_schema.yaml`): `automated_test` (native `cargo test`, headless
`wasm-bindgen-test`, or `trybuild`), `example_build`, or `doc_inspection`. All five requirements are stage
`usable_early` and `release_gating: true` — they specialize `REQ-FW-006`, which is `usable_early`: an author
cannot build a real, form-driven app without reading events and binding more than two of them.

### REQ-ASYNC-020 — The payload-carrying handler form (additive over the frozen zero-arg handler)

- **Statement:** An author can bind an event handler that optionally **receives the triggering event's payload**,
  while the frozen zero-argument handler form (`EventHandler = Rc<dyn Fn()>`, `VElement::on(kind, || …)`) remains
  valid and unchanged. Both forms are available on every bound event; the author chooses per binding whether the
  handler needs the payload.
- **Rationale:** The zero-arg form cannot read the event, so an author cannot get an input's value or a pressed
  key from inside a handler — the gap that blocks forms and real event handling. The baseline wrapper already
  receives a `web_sys::Event` and discards it, and the `vdom.rs` module doc sanctions enriching the handler form
  to carry it. Every Rust peer gives handlers their event: Leptos passes the typed `web_sys` event to
  `on:input`/`on:click` closures; Dioxus passes typed event data (`Event<MouseData>`, `KeyboardData`, …); Yew's
  callbacks receive `web_sys` events; Sycamore's `on:*` closures receive the `web_sys::Event`. A zero-arg-only
  framework is alone in withholding it.
- **Acceptance criteria:**
  - A1. An app written against the baseline — handlers bound with the zero-argument `.on(kind, || …)` form —
    compiles and runs unchanged against the 1.0 surface; no previously exported item is removed or redefined.
    *(verification: `automated_test` — a `trybuild`/`cargo test` build of a baseline-style view; `example_build`.)*
  - A2. An author can bind a handler that receives the triggering event's payload and reads from it within the
    handler body; a stated example binds such a handler and observes the payload. *(verification:
    `automated_test` — headless `wasm-bindgen-test` dispatches an event and asserts the handler saw the payload;
    `example_build`.)*
  - A3. The zero-argument and payload-carrying forms coexist on the same element and the same event type (one
    element may bind a zero-arg handler for one event and a payload handler for another). *(verification:
    `automated_test`.)*
  - A4. The payload-carrying form is defined in exactly this requirement for the whole concern; the forms sibling
    and the event-coverage requirements reference it rather than restating it. *(verification: `doc_inspection`
    — `REQ-ASYNC-040..059` reference `REQ-ASYNC-020`/`022`, not a second handler form.)*
- **Stage:** usable_early · **Release gating:** true
- **References:** `REQ-FW-006`, `REQ-FW-009` (frozen surfaces carried forward additively); consumed read-only by
  `REQ-ASYNC-022`, `REQ-ASYNC-023`, and the forms register `REQ-ASYNC-040..059`. Sub-contract seam J3.

### REQ-ASYNC-021 — Full DOM event coverage beyond click/input

- **Statement:** An author can bind the range of DOM events a real app needs — at least `submit`, the keyboard
  events (`keydown`, `keyup`, `keypress`), `focus`/`blur`, and `change`, in addition to the baseline `click` and
  `input` — **and** can bind any other DOM event by its name, without the framework having to enumerate it ahead
  of time. The baseline `EventKind::Click` and `EventKind::Input` remain valid and first-class.
- **Rationale:** Today's runtime binds only `click` and `input`; a form cannot submit, a key cannot be observed,
  a field cannot react to blur. `REQ-FW-006` names submit, keyboard, focus/blur, and change as the floor. A
  framework that fixes its event set in a closed enum cannot carry the custom and less-common events real apps
  use, so the common events are first-class for discoverability and the long tail is reachable by name — the
  shape peers converge on (Leptos and Yew expose the full typed DOM event set; Dioxus names the common events and
  types their data).
- **Acceptance criteria:**
  - A1. A stated example binds and fires each of `submit`, `keydown`, `focus`, `blur`, and `change` and observes
    the handler run; the baseline `click` and `input` bindings continue to fire. *(verification: `automated_test`
    — headless `wasm-bindgen-test` dispatches each event type; `example_build`.)*
  - A2. An author can bind a DOM event that is not in the first-class set by naming it, and the handler fires when
    that event is dispatched. *(verification: `automated_test`.)*
  - A3. The widening is additive: the baseline `EventKind` variants and the baseline `.on` binding are unchanged;
    no frozen variant is removed or renamed. *(verification: `automated_test` — a baseline binding still
    compiles; `doc_inspection`.)*
  - A4. Each first-class event, bound with the payload-carrying form of `REQ-ASYNC-020`, delivers the event data
    appropriate to it (a key for keyboard events, the target for change/submit). *(verification: `automated_test`;
    `example_build`.)*
- **Stage:** usable_early · **Release gating:** true
- **References:** `REQ-FW-006`; builds on `REQ-ASYNC-020` (payload form) and is read by `REQ-ASYNC-024`
  (re-binding). Sub-contract identity J4 (additive over frozen `EventKind`).

### REQ-ASYNC-022 — Reading the triggering event's data from the payload

- **Statement:** From a payload-carrying handler, an author can read the data the event carries — an input or
  change target's current **value**, the **key** of a keyboard event, and the underlying `web_sys` event itself —
  through the framework, without reaching around it to raw DOM lookups.
- **Rationale:** Receiving the payload (`REQ-ASYNC-020`) is only useful if the common reads are ergonomic. The
  dominant read is "what did the user type," which every peer makes a one-liner: Leptos ships
  `event_target_value(&ev)` and a typed `on:input:target` giving `ev.target().value()`; Dioxus exposes
  `event.value()` on form events; Yew reads the target via `target_dyn_into::<HtmlInputElement>()`. Ferric should
  give the author the value and the key directly, and still expose the raw `web_sys::Event` for anything the
  helpers do not cover — keeping the lean `web-sys` footprint (`REQ-FW-013`) rather than a bespoke event model.
- **Acceptance criteria:**
  - A1. A handler on an `input` or `change` event reads the field's current value through a framework accessor and
    the value matches what was typed. *(verification: `automated_test` — `wasm-bindgen-test` sets a field value,
    dispatches the event, asserts the read value; `example_build`.)*
  - A2. A handler on a keyboard event reads which key was pressed through a framework accessor. *(verification:
    `automated_test`.)*
  - A3. The raw `web_sys::Event` is reachable from the payload so an author can handle an event the accessors do
    not cover. *(verification: `automated_test`; `doc_inspection`.)*
  - A4. Reading the payload requires no dependency beyond the framework and its existing
    `wasm-bindgen`/`web-sys`/`js-sys` base. *(verification: `doc_inspection` — the dependency set is unchanged;
    `example_build`.)*
- **Stage:** usable_early · **Release gating:** true
- **References:** `REQ-FW-006`, `REQ-FW-013`; composes on `REQ-ASYNC-020`; consumed read-only by the forms
  two-way binding register `REQ-ASYNC-040..059`.

### REQ-ASYNC-023 — Default-action and propagation control from a handler

- **Statement:** From a handler that receives the payload, an author can suppress the browser's default action for
  the event (for example, stop a `submit` from navigating the page) and can stop the event propagating to ancestor
  handlers.
- **Rationale:** A two-way-bound form is unusable without `preventDefault` on `submit` — otherwise the browser
  performs a full-page form navigation and the single-page app is lost. Propagation control is needed wherever
  nested elements both handle an event. Peers provide both: Dioxus exposes `event.prevent_default()` /
  `stop_propagation()`; Leptos and Yew expose them on the `web_sys` event. This is a direct consequence of
  `REQ-ASYNC-020` delivering the event, and is the specific capability the forms sibling's submit flow relies on.
- **Acceptance criteria:**
  - A1. A `submit` handler that suppresses the default action prevents the page navigation; a stated example
    submits a form and the view is not reloaded. *(verification: `automated_test` — `wasm-bindgen-test`;
    `example_build`.)*
  - A2. A handler can stop propagation so an ancestor handler for the same event does not fire. *(verification:
    `automated_test`.)*
  - A3. Default-action and propagation control are reachable only through the payload-carrying form; the
    zero-argument form is unaffected and still valid. *(verification: `doc_inspection`; `automated_test`.)*
- **Stage:** usable_early · **Release gating:** true
- **References:** `REQ-FW-006`; composes on `REQ-ASYNC-020`; relied on by the forms submission flow in
  `REQ-ASYNC-040..059`.

### REQ-ASYNC-024 — Re-binding across the keyed diff, stated from the author's side

- **Statement:** An author can rely on these re-binding guarantees across re-renders, for the full event surface
  of `REQ-ASYNC-021` and both handler forms of `REQ-ASYNC-020`:
  1. **A render that does not change which event types are bound on an element keeps that element's existing
     listeners** — the framework does not detach and re-attach on every render. Because handlers read their
     signals live, a retained listener reflects current state; an author therefore reads dynamic values from
     signals (or from the event payload) inside the handler, not by capturing them at bind time.
  2. **Adding or removing an event type on an element across a render re-binds that element's listeners** to match
     the new set (for example, conditionally binding `keydown` only while a mode is active attaches and detaches
     the `keydown` listener as the condition flips).
  3. These guarantees hold identically whether an event is a first-class kind or bound by name, and whether its
     handler is zero-argument or payload-carrying.
- **Rationale:** The baseline `diff_events` emits `Patch::SetEvents` only when the set of bound `EventKind`s
  changes between the old and new element; this requirement states that behavior as an author-facing contract and
  extends it over the widened surface, so an author knows when a handler swap takes effect and why reading live
  state inside the handler is the correct pattern. It is stated from the author's side — what re-binding they can
  rely on — not as diff internals.
- **Acceptance criteria:**
  - A1. Re-rendering an element with the same set of bound event types does not re-attach its listeners; a
    handler that reads a signal observes the signal's current value when the event fires. *(verification:
    `automated_test` — `wasm-bindgen-test` re-renders, fires the event, asserts current state is read;
    the existing `vdom.rs` diff tests cover the no-`SetEvents`-on-equal-set case with `cargo test`.)*
  - A2. Adding an event type across a render causes that event to fire a handler afterward, and removing it causes
    it to stop firing. *(verification: `automated_test`.)*
  - A3. The guarantees are documented for the author (a guide statement that live-signal reads inside handlers are
    the intended pattern and when re-binding occurs). *(verification: `doc_inspection`.)*
- **Stage:** usable_early · **Release gating:** true
- **References:** `REQ-FW-006`; reads `REQ-ASYNC-020` and `REQ-ASYNC-021`; the live-signal-read guarantee is the
  property the forms two-way binding register `REQ-ASYNC-040..059` relies on.

---

## Seam for the forms sibling (`SUBTASK_afe_forms_binding`, read-only)

Two-way binding is built **on top of** the capabilities above; the forms register (`REQ-ASYNC-040..059`)
references these ids read-only and MUST NOT restate the handler form (sub-contract identity J3):

| What forms binding needs | Provided by | How forms composes on it |
|---|---|---|
| A handler that receives the event | `REQ-ASYNC-020` | The `input`/`change` handler that drives a signal is a payload-carrying handler. |
| Reading the field's current value | `REQ-ASYNC-022` | Two-way binding writes the read value into the bound signal on each `input`. |
| `submit` with the default suppressed | `REQ-ASYNC-023` | A bound form's submit handler suppresses the page navigation before running validation/submission. |
| Listener stability + live-signal reads | `REQ-ASYNC-024` | The bound signal is read live inside the handler, so a retained listener stays correct across renders. |

The handler form is therefore defined once, here. The forms sibling declares a dependency on this task
(precursor → dependent) and cites `REQ-ASYNC-020`/`022`/`023`/`024` rather than redefining any of them.

## Peer comparison (by name, from documented behavior)

| Framework | Handler receives the event? | Reading an input value | Event coverage | Default/propagation |
|---|---|---|---|---|
| **Leptos** (verified) | Yes — `on:click`/`on:input` closures receive the typed `web_sys` event | `event_target_value(&ev)`; typed `on:input:target` → `ev.target().value()` | Full typed DOM event set via `on:*` | On the `web_sys` event |
| **Dioxus** (verified) | Yes — typed event data (`Event<MouseData>`, `KeyboardData`, `FormData`) | `event.value()` on form events | Named handlers (`onclick`, `oninput`, `onkeydown`, …) with typed data | `event.prevent_default()` / `stop_propagation()` |
| **Yew** | Yes — `Callback` receives `web_sys` events (`MouseEvent`, `InputEvent`, `KeyboardEvent`) | `target_dyn_into::<HtmlInputElement>()` then `.value()` | Full `web_sys` event set | On the `web_sys` event |
| **Sycamore** | Yes — `on:*` closures receive the `web_sys::Event` | Read the target from the event | Full DOM event surface | On the `web_sys` event |
| **Solid** (JS design analog) | Yes — native DOM events | `e.currentTarget.value` | Native DOM events | Native event methods |
| **Ferric today** (`276138f`) | **No** — `EventHandler = Rc<dyn Fn()>` is zero-arg; the runtime receives and discards the event | **Not possible** | **`click` + `input` only** | **Not reachable** |

Verified against current sources: Leptos — [`event_target_value`](https://docs.rs/leptos/latest/leptos/prelude/fn.event_target_value.html)
and the [Forms and Inputs](https://book.leptos.dev/view/05_forms.html) chapter; Dioxus —
[event handlers guide](https://dioxuslabs.com/learn/0.7/essentials/basics/event_handlers/),
[`oninput`](https://docs.rs/dioxus/latest/dioxus/events/fn.oninput.html), and
[`dioxus_core::Event`](https://docs.rs/dioxus-core/latest/dioxus_core/struct.Event.html). The Yew, Sycamore, and
Solid rows state each framework's established public model (handlers receive the DOM/`web_sys` event and read the
target from it); they were not re-verified against their docs in this pass and are presented as directional, not
as freshly read citations. The assessment stands on the two verified rows: giving a handler its event is the
settled norm across the field, and Ferric is the outlier in withholding it. The 1.0 work closes that gap
additively, which is what `REQ-ASYNC-020..024` specify.

## Conformance and traceability

- **Owns `REQ-ASYNC-020..024`**, all within the assigned range `REQ-ASYNC-020..039` (sub-contract identity J1);
  ids assigned monotonically within the range.
- **Covers the event clause of `REQ-FW-006`** — "event handlers beyond click/input (submit, keyboard,
  focus/blur, change) can be attached and fire" — and supplies the payload capability the forms clause needs
  (identity J2).
- **Owns the event-payload handler seam** (identity J3): the payload-carrying handler form is defined only in
  `REQ-ASYNC-020` (with its reads in `022`, its control in `023`); the forms register references it read-only.
- **Additive over the frozen surface** (identity J4): `EventKind`, `EventHandler = Rc<dyn Fn()>`, `VElement::on`,
  and `Patch::SetEvents` are extended, never redefined or removed; the baseline `click`/`input` bindings and the
  zero-argument handler form stay valid.
- **Conforms to `../../contracts/id_and_traceability_schema.yaml`** (identity J7): requirement fields, the
  `usable_early` stage, `release_gating`, and the `verification_method` vocabulary; this fragment adds no new
  vocabulary and redefines none.

## Note on execution

The methodology surface was not bindable in this reconstructed node (the agent's methodology domain was unset, so
the `design` loader returned `agent_domain_unset` before and after boot). Per the orchestrated-execution rule to
proceed with the most reasonable interpretation and record the assumption rather than stall, this fragment was
authored from product-design and event-system/API-design practice and grounded directly in the read baseline
source and the two verified peer sources above; no methodology file was available to cite.

## Metadata

- **Owning task:** `SUBTASK_afe_events_payloads` (owns `REQ-ASYNC-020..039`; owns the event-payload seam J3).
- **Assembled into:** `../async-forms-events.md` by `SUBTASK_afe_synthesis` (repo target
  `design/ferric/async-forms-events.md`), merged in order into the one continuous `REQ-ASYNC` register.
- **Grounding commit:** `Nousix-LLC/nswe-demo` @ `276138f` (`crates/ferric/src/vdom.rs`, `dom.rs`).
- **Conforms to:** `../../contracts/id_and_traceability_schema.yaml`, `../contracts/_MANIFEST.yaml`.
