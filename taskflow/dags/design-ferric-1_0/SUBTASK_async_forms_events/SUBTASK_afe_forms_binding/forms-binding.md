# Ferric 1.0 — Forms and two-way input binding

*Concern 4c of the Ferric 1.0 design (`SUBTASK_async_forms_events` → `SUBTASK_afe_forms_binding`). Owns
`REQ-ASYNC-040..059`. Design, not framework code: every requirement reads as something a stranger could check
against the framework, not a chosen data structure or code path. Two-way binding is specified **on top of** the
payload-carrying handler form owned by the events sibling (`REQ-ASYNC-020`, with its reads in `022`, its control
in `023`, its re-bind guarantee in `024`); this fragment references those ids read-only and does not restate the
handler form (sub-contract identity J3).*

This fragment settles what an app author needs to build a real, data-entry form on Ferric: a way to **bind an
input to a signal so the model and the field stay in sync**, a way to **express validation and surface validity
and error messages reactively**, and a way to **handle submission** — suppressing the browser's default
navigation, reading the entered values, and gating on validity. It states each from the author's side and grounds
the binding story in the reactive core that already exists in the tree.

## What Ferric does today (baseline `Nousix-LLC/nswe-demo` @ `276138f`, read from source)

Grounded in `crates/ferric/src/{signal,vdom,dom}.rs` at the baseline so the 1.0 line is drawn against what is
real:

- **State is a single `Copy` read-write signal handle.** `create_signal::<T>(value) -> Signal<T>` (`signal.rs`)
  returns **one** handle — not a split read/write pair. `Signal<T>` is a `Copy` key into the reactive runtime with
  `.get()` (when `T: Clone`), `.with(|&T| -> R)`, `.set(T)`, and `.update(|&mut T|)`. One handle both reads the
  value (for display) and writes it (on edit), so a two-way binding needs exactly one signal, not a read half and
  a write half threaded separately.
- **Effects re-run on signal change, and attributes are diffed.** A render runs inside an effect (`dom.rs::mount`
  wraps render in `create_effect`), so reading a signal in a view re-renders when it changes; the keyed diff
  updates an element's attributes (including `value`) to match the new render. The "signal → field" direction is
  therefore already expressible: set the field's `value` attribute from `signal.get()`.
- **The "field → signal" direction was impossible at the baseline.** `EventHandler = Rc<dyn Fn()>` is zero-argument
  (`vdom.rs`), so a handler could not read the edited field's value — there was no way to get the typed text back
  into the signal. This is the exact gap the events sibling closes with the payload-carrying handler form
  (`REQ-ASYNC-020`) and the value/key reads (`REQ-ASYNC-022`). Two-way binding stands on that work: it is why this
  task depends on `SUBTASK_afe_events_payloads`.
- **No binding, validation, or submission affordance exists.** There is no `value`-binding helper, no `submit`
  handling (the runtime binds only `click` and `input`, closed now by `REQ-ASYNC-021`), and nothing that expresses
  field or form validity. An author today hand-wires nothing because the handler cannot even read the field.

So the forms capability is latent in the reactive core and the (now-extended) event surface, and is not yet given
to the author. The 1.0 work composes it from pieces that exist — **additively**, never by redefining a frozen item
(sub-contract identity J4; parent `REQ-FW-009`).

## The design decision (what, not how)

**Two-way binding is a convention composed over the payload handler and a reactive attribute — not a new reactive
primitive.** The two directions are each already reachable once the payload seam is in place:

- **signal → field:** the field's value-bearing attribute (`value` for text, `checked` for a checkbox, the
  selected option for a `select`) is written from the bound signal's current value, inside the render effect, so a
  signal write updates the field on the next render.
- **field → signal:** an `input`/`change` **payload-carrying** handler (`REQ-ASYNC-020`) reads the field's current
  value through the framework accessor (`REQ-ASYNC-022`) and writes it into the bound signal (`.set` / `.update`).

A `bind`-style affordance (a binding helper, a `bind`-named convention on the view surface, or a macro attribute —
the concrete surface is left to the authoring-model and code work) is **sugar that wires exactly those two edges
to one `Signal<T>`**. Specifying binding as a composition over `REQ-ASYNC-020`/`022` keeps the handler form defined
in one place (J3), keeps the change additive over the frozen signal and event surfaces (J4), and matches how the
Rust/WASM field actually works: Leptos's `bind:value`, Svelte's `bind:value`, and Vue's `v-model` are all sugar
over the controlled-input pair (a value out, a change in), and Solid and Dioxus expose the controlled pair
directly without a bind shortcut. Ferric's single `Copy` signal handle makes the shortcut natural, because the one
handle is both the source and the sink.

**Validation is expressed with the reactive core the author already has, not a bundled validation DSL.** Per-field
and per-form validity are derived reactive values (a memo or a computed signal over the bound signals); error
messages are values the view renders reactively. The framework's bar is that validity and messages are
*expressible and reactive* and *surface in the view* — not that Ferric ships a schema/validator library. That
keeps scope to the framework's own reactivity (what, not how) and leaves a validation library to the ecosystem,
which is where every peer core framework leaves it.

**Submission reads the model, suppresses the default, and gates on validity.** A bound form's `submit` handler
suppresses the browser's default navigation (`REQ-ASYNC-023`) so the single-page app is not reloaded, reads the
submitted values from the bound signals (the model, not a re-scrape of the DOM), and may refuse to submit while
the form is invalid. These are stated as author-facing guarantees, composed on the event surface the sibling
owns.

One structural fact the binding guarantees rest on, stated as rationale and not as a mandated data structure:
because the keyed diff retains an element's listeners when the set of bound event kinds is unchanged and a handler
reads its signals live (`REQ-ASYNC-024`), a bound field's `input` handler keeps writing the current signal across
re-renders without re-attaching. The author therefore binds once and relies on live reads, rather than capturing
the signal at bind time.

---

## Requirements (`REQ-ASYNC-040..059`)

Each requirement states what must be true from an app author's side and carries acceptance criteria a reviewer who
never met the author can check. Every criterion names at least one `verification_method` from the parent schema
(`../../contracts/id_and_traceability_schema.yaml`): `automated_test` (native `cargo test`, headless
`wasm-bindgen-test`, or `trybuild`), `example_build`, or `doc_inspection`. All four requirements are stage
`usable_early` and `release_gating: true` — they specialize `REQ-FW-006` (itself `usable_early`): an author cannot
build a real, form-driven app without binding a field two-way, surfacing validity, and submitting without a page
reload. Ids are assigned monotonically within the assigned range `REQ-ASYNC-040..059` (identity J1).

### REQ-ASYNC-040 — Two-way binding of a signal to an input, so the model and the field stay in sync

- **Statement:** An author can bind an input to a `Signal<T>` so that editing the field updates the signal and
  writing the signal updates the field, through one binding affordance applied to one signal handle. The author
  does not hand-wire the value-out and change-in edges separately; binding expresses both.
- **Rationale:** This is the forms clause of `REQ-FW-006` — "a form binds an input two-way so the model and the
  field stay in sync." At the baseline it was not expressible at all, because the zero-argument handler could not
  read the edited value; the payload-carrying handler (`REQ-ASYNC-020`) and the value read (`REQ-ASYNC-022`) now
  make the field→signal edge reachable, and the render effect already makes the signal→field edge reachable.
  Ferric's `create_signal` returns a single `Copy` read-write handle, so one signal is both the source and the
  sink of the binding — the author binds one handle, not a read/write pair. Peers converge on a two-way shortcut
  over exactly this pair: Leptos `bind:value`, Svelte `bind:value`, Vue `v-model`.
- **Acceptance criteria:**
  - A1. A stated example binds a text input to a `Signal<String>`; typing in the field changes the signal's value,
    and setting the signal from elsewhere changes what the field displays. *(verification: `automated_test` —
    headless `wasm-bindgen-test` types into the field and asserts the signal, then sets the signal and asserts the
    field value; `example_build`.)*
  - A2. The binding is built on the payload-carrying handler form: the field→signal edge uses the handler of
    `REQ-ASYNC-020` and the value read of `REQ-ASYNC-022`, and this requirement does not define a second handler
    form. *(verification: `doc_inspection` — the binding references `REQ-ASYNC-020`/`022`, not a new handler
    form.)*
  - A3. A bound field stays in sync across re-renders without the author re-binding: after an unrelated re-render,
    editing the field still updates the signal and a signal write still updates the field. *(verification:
    `automated_test` — re-render, then exercise both directions; rests on the live-read/re-bind guarantee of
    `REQ-ASYNC-024`.)*
  - A4. Binding is additive over the frozen surfaces: an app written against the baseline signal and event APIs
    still compiles, and binding adds a new affordance rather than redefining `Signal`, `EventKind`,
    `EventHandler`, or `VElement::on`. *(verification: `automated_test`; `doc_inspection`.)*
- **Stage:** usable_early · **Release gating:** true
- **References:** `REQ-FW-006`, `REQ-FW-009`; composes read-only on `REQ-ASYNC-020` (payload handler),
  `REQ-ASYNC-022` (value read), `REQ-ASYNC-024` (live reads across re-render). Sub-contract seam J3.

### REQ-ASYNC-041 — Two-way binding across the common input kinds

- **Statement:** An author can bind two-way across the input kinds a real form needs — at least a text input and
  textarea (to a string signal), a checkbox (to a boolean signal), a radio group (to the selected value), a
  single and multiple `select` (to the selected option or options), and a number input (to a numeric signal) —
  with the binding reading and writing the property appropriate to each kind, not a one-size value coercion.
- **Rationale:** "Bind an input two-way" is not one shape: a checkbox's state is `checked`, not `value`; a
  `select` carries a selected option; a multiple select carries several; a number field is a numeric model behind
  a string field. A binding that only handled `<input type=text>.value` would not carry a real form. Peers handle
  the kinds explicitly: Svelte has `bind:value`, `bind:checked`, and `bind:group`; Vue's `v-model` adapts to the
  control and offers `.number`/`.trim` modifiers; Leptos binds `value` and `checked`. The payload read of
  `REQ-ASYNC-022` exposes the target, so per-kind reads compose on the one seam.
- **Acceptance criteria:**
  - A1. A stated example binds, two-way, each of: a text input and a textarea to a string signal, a checkbox to a
    boolean signal, a radio group to a selected-value signal, a single `select` to a selected-option signal, and a
    number input to a numeric signal; each field edit updates its signal and each signal write updates its field.
    *(verification: `automated_test` — `wasm-bindgen-test` per kind; `example_build`.)*
  - A2. A multiple `select` binds to a collection signal so selecting and deselecting options updates the
    collection and setting the collection updates the selection. *(verification: `automated_test`.)*
  - A3. A number input's binding surfaces a numeric model (not a raw string) to the author, and a non-numeric or
    empty field is observable to the author rather than silently coerced to a wrong number. *(verification:
    `automated_test`; `doc_inspection` — the documented behavior for an unparseable value is stated.)*
  - A4. Each kind's binding reads and writes through the framework's payload accessor and the reactive attribute,
    adding no dependency beyond the existing `wasm-bindgen`/`web-sys`/`js-sys` base (`REQ-FW-013`).
    *(verification: `doc_inspection` — dependency set unchanged; `example_build`.)*
- **Stage:** usable_early · **Release gating:** true
- **References:** `REQ-FW-006`, `REQ-FW-013`; composes on `REQ-ASYNC-040` and read-only on `REQ-ASYNC-022`.

### REQ-ASYNC-042 — Validation ergonomics: reactive per-field and per-form validity and messages

- **Statement:** An author can express per-field and whole-form validation over the bound signals and surface the
  resulting validity and error messages in the view reactively, so that a field becoming invalid shows its message
  and becoming valid clears it without manual refresh wiring. The framework provides the reactive substrate
  (derived values over the bound signals); it does not require a bundled validation schema language.
- **Rationale:** A form that cannot tell the user what is wrong is not usable, and validity is a function of the
  model that must update as the model updates — exactly what the reactive core (`create_memo` / derived signals)
  is for. Keeping validation as author-expressed reactive values, rather than a bundled validator DSL, matches
  every peer core framework: Leptos, Solid, and Dioxus leave validation to the author's reactive code (or an
  ecosystem library such as Felte or VeeValidate) and provide the reactivity it rests on. Ferric's bar is that
  validity and messages are expressible, reactive, and renderable — not that Ferric ships a validator.
- **Acceptance criteria:**
  - A1. A stated example derives a field's validity from its bound signal and renders an error message when the
    field is invalid; editing the field to a valid value removes the message reactively, with no explicit
    re-render call by the author. *(verification: `automated_test` — `wasm-bindgen-test` drives the bound signal
    across the validity boundary and asserts the rendered message appears and clears; `example_build`.)*
  - A2. An author can derive a whole-form validity value from multiple fields' validity, and it updates when any
    contributing field changes. *(verification: `automated_test`.)*
  - A3. Validity and messages are expressed with the framework's existing reactive primitives (signals/memos/
    effects) over the bound signals, requiring no primitive beyond the reactive core and no third-party
    dependency. *(verification: `doc_inspection`; `example_build`.)*
  - A4. The guide states the intended validation pattern for the author — derive validity reactively from the
    bound signals and render messages from derived values — so the approach is discoverable rather than implied.
    *(verification: `doc_inspection`.)*
- **Stage:** usable_early · **Release gating:** true
- **References:** `REQ-FW-006`; composes on `REQ-ASYNC-040` (bound signals) and the reactive core
  (`create_signal`/`create_memo`/`create_effect`).

### REQ-ASYNC-043 — Submission ergonomics: submit without a page reload, read the model, gate on validity

- **Statement:** An author can handle a form's submission so that the browser's default navigation is suppressed
  (the single-page app is not reloaded), the submitted values are read from the bound signals (the model), and
  submission can be refused or deferred while the form is invalid — all stated from the author's side.
- **Rationale:** Without suppressing the default `submit` action the browser performs a full-page form navigation
  and the app is lost, so `preventDefault` on submit (`REQ-ASYNC-023`) is the capability a bound form's submit flow
  depends on. Reading the submitted values from the bound signals rather than re-scraping the DOM means the author
  works against the model they already have. Gating on validity (`REQ-ASYNC-042`) is what turns a bound, validated
  form into one that submits only acceptable data. Every peer handles submit through the event with
  `preventDefault` and reads the model, not the DOM.
- **Acceptance criteria:**
  - A1. A stated example attaches a `submit` handler that suppresses the default action; submitting the form does
    not reload or navigate the page. *(verification: `automated_test` — `wasm-bindgen-test` dispatches `submit` and
    asserts no navigation; `example_build`.)*
  - A2. The submit handler reads the submitted values from the bound signals, and the values it reads match what
    was entered through the two-way binding. *(verification: `automated_test`.)*
  - A3. A stated example refuses or defers submission while the form's derived validity is false and proceeds once
    it is true, surfacing to the user why submission did not proceed. *(verification: `automated_test`;
    `example_build`.)*
  - A4. The submit flow composes on the payload-carrying handler and its default-action control and does not
    define its own handler form or its own `preventDefault`. *(verification: `doc_inspection` — references
    `REQ-ASYNC-023`, not a new control surface.)*
- **Stage:** usable_early · **Release gating:** true
- **References:** `REQ-FW-006`; composes read-only on `REQ-ASYNC-023` (default-action control) and `REQ-ASYNC-020`
  (payload handler); composes on `REQ-ASYNC-040` (bound signals) and `REQ-ASYNC-042` (validity gating).

---

## How this fragment composes on the event-payload seam (read-only)

Two-way binding is built **on top of** the capabilities the events sibling owns; this register cites their ids
read-only and does not restate the handler form (sub-contract identity J3):

| What forms binding uses | Provided by (read-only) | How this fragment composes on it |
|---|---|---|
| A handler that receives the triggering event | `REQ-ASYNC-020` | The `input`/`change` handler that drives a bound signal is a payload-carrying handler. |
| Reading the field's current value / selected state | `REQ-ASYNC-022` | The field→signal edge reads the value (or `checked`, or the selection) and writes it into the bound signal. |
| `submit` with the default action suppressed | `REQ-ASYNC-023` | The bound form's submit handler suppresses the page navigation before reading the model and running validity gating. |
| Listener stability + live-signal reads across the keyed diff | `REQ-ASYNC-024` | The bound signal is read live inside the handler, so a retained listener stays correct across re-renders and the author binds once. |

The handler form, its reads, and its default-action control are defined once, in the events fragment. This
fragment adds the binding convention, the per-kind coverage, the validation substrate, and the submission flow
that sit on top.

## Peer comparison (by name, from documented behavior)

| Framework | Two-way binding affordance | Input-kind coverage | Validation | Submit model |
|---|---|---|---|---|
| **Leptos** (verified) | `bind:value` / `bind:checked` sugar over the signal + event pair | `value`, `checked`; group/select via the typed event target | Author-expressed with reactive signals/memos; no bundled validator | `on:submit` with `ev.prevent_default()`; read the model |
| **Svelte** (verified) | `bind:value`, `bind:checked`, `bind:group` | Text, checkbox, radio group, select (single + `multiple`), number (`bind:value` coerces) | Author or ecosystem (Felte, Superforms); constraint API available | `on:submit\|preventDefault`; read bound state |
| **Vue** (verified) | `v-model` with `.number` / `.trim` / `.lazy` modifiers | Adapts to text, checkbox, radio, select (single + multiple), number | Author or ecosystem (VeeValidate); none in core | `@submit.prevent`; read the reactive model |
| **Dioxus** | No bind shortcut — controlled input (`value` + `oninput` writing a signal) | Author wires per kind via the typed form event | Author-expressed over signals | `onsubmit` with `prevent_default`; read `FormData`/signals |
| **Solid** (JS design analog) | No bind by default — controlled input (value + `onInput` setter) | Author wires per kind | Author-expressed over signals/stores | `onSubmit` with `preventDefault`; read the model |
| **Ferric today** (`276138f`) | **None** — and two-way was impossible: the zero-arg handler could not read the field | **None** | **None** | **None** — `submit` was not even bindable |

Verified against current sources: Leptos — the [Forms and Inputs](https://book.leptos.dev/view/05_forms.html)
chapter (`bind:value`, controlled/uncontrolled inputs, `on:submit` + `prevent_default`); Svelte — the
[bindings tutorial](https://svelte.dev/tutorial/svelte/text-inputs) and `bind:value`/`bind:checked`/`bind:group`
docs; Vue — the [Form Input Bindings](https://vuejs.org/guide/essentials/forms.html) guide (`v-model` and its
modifiers). The Dioxus and Solid rows state each framework's established public model (controlled inputs: a value
out and a change handler writing a signal, no built-in two-way shortcut) and are presented as directional, not as
freshly re-read citations this pass. The pattern the verified rows establish: a two-way `bind` is a convenience
over the controlled pair, core frameworks leave validation to the author or ecosystem, and submission runs through
the event with the default suppressed and reads the model. `REQ-ASYNC-040..043` specify exactly that shape for
Ferric, composed additively on the payload seam.

## Conformance and traceability

- **Owns `REQ-ASYNC-040..043`**, all within the assigned range `REQ-ASYNC-040..059` (sub-contract identity J1);
  ids assigned monotonically within the range.
- **Covers the forms clause of `REQ-FW-006`** — "a form binds an input two-way so the model and the field stay in
  sync" — and extends it with the per-kind coverage, validation, and submission an author needs to use it
  (identity J2).
- **Honors the event-payload seam** (identity J3): two-way binding, value reads, submit control, and the live-read
  guarantee are referenced read-only at `REQ-ASYNC-020`/`022`/`023`/`024`; this fragment defines no handler form.
- **Additive over the frozen surface** (identity J4): `Signal`/`create_signal`, `EventKind`,
  `EventHandler = Rc<dyn Fn()>`, `VElement::on`, and `dom::mount` are composed on and extended, never redefined or
  removed; an app written against the baseline signal and event APIs still compiles.
- **Conforms to `../../contracts/id_and_traceability_schema.yaml`** (identity J7): requirement fields, the
  `usable_early` stage, `release_gating`, and the `verification_method` vocabulary; this fragment adds no new
  vocabulary and redefines none.

## Note on execution

The methodology surface was not bindable in this reconstructed node (the agent's methodology domain was unset, so
the `design` loader returned `agent_domain_unset` before and after boot). Per the orchestrated-execution rule to
proceed with the most reasonable interpretation and record the assumption rather than stall, this fragment was
authored from product-design and form-ergonomics practice and grounded directly in the read baseline source
(`crates/ferric/src/{signal,vdom,dom}.rs` @ `276138f`), the completed events-sibling fragment, and the three
verified peer sources above; no methodology file was available to cite. This matches how the completed events
sibling recorded the same condition.

## Metadata

- **Owning task:** `SUBTASK_afe_forms_binding` (owns `REQ-ASYNC-040..059`; composes read-only on the event-payload
  seam J3).
- **Depends on:** `SUBTASK_afe_events_payloads` (the payload-carrying handler form this builds on).
- **Assembled into:** `../async-forms-events.md` by `SUBTASK_afe_synthesis` (repo target
  `design/ferric/async-forms-events.md`), merged in order into the one continuous `REQ-ASYNC` register.
- **Grounding commit:** `Nousix-LLC/nswe-demo` @ `276138f` (`crates/ferric/src/signal.rs`, `vdom.rs`, `dom.rs`).
- **Conforms to:** `../../contracts/id_and_traceability_schema.yaml`, `../contracts/_MANIFEST.yaml`.
</content>
</invoke>
