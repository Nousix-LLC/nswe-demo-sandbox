# _BRIEF.md — ferric-async-forms-r1

**Goal slug**: `ferric-async-forms-r1`
**Kind**: code DAG
**Launch agent**: swe-coder
**Repo**: Nousix-LLC/nswe-demo
**Branch**: `work/ferric-async-forms-r1`
**Epic**: #130 — Ferric 1.0: Async, Forms, and Events (usable_early)

---

## Objective

Implement **Ferric 1.0 — Async Resources, DOM Events, and Forms** (epic #130) on branch
`work/ferric-async-forms-r1`. This is the second Ferric 1.0 implementation epic, landing on top of
the Authoring Model (PR #188, merge commit `aa2468771eccd9e2ee79c12c79b8943fca18e07a`).

The goal delivers three tightly coupled capabilities that together make a real data-driven SPA
possible in Ferric 1.0:

1. **Async resources and suspense** (#143) — a reactive `create_resource` primitive with four
   distinct states (loading, loaded, empty, error), a suspense boundary that aggregates pending
   resources, imperative `refetch`, and reactive composition with the existing signal graph.

2. **Full DOM event handling** (#144) — a payload-carrying handler form that lets handlers read the
   triggering event (additive over the frozen zero-arg `EventHandler = Rc<dyn Fn()>`), coverage
   of `submit`, keyboard, focus/blur, and `change` beyond today's `click`/`input`, and
   `preventDefault` / `stopPropagation` from handler code.

3. **Forms and two-way binding** (#145) — a binding affordance that wires both the signal→field
   and field→signal directions to one `Signal<T>` handle, per-kind coverage (text, checkbox, radio,
   select, number), reactive validation ergonomics built over the existing reactive core, and a
   submit handler that suppresses the default navigation, reads the bound-signal model, and gates on
   validity.

All three capabilities are stage **usable_early** and release-gating. They must be additive over
the frozen authoring-model surface delivered by PR #188 (see "Frozen surfaces" below).

---

## Issues covered

### #130 — Ferric 1.0: Async, Forms, and Events (epic)

The parent epic. Closed when all three sub-issues are met.

### #143 — Ferric 1.0: Async resources and suspense

**Acceptance criteria** (from issue body):
- `create_resource` tracks four states — loading, loaded, empty, and error — and re-renders
  consumers when the state changes.
- `<Suspense>` shows the fallback while any enclosed resource is loading and switches to resolved
  content when all are loaded; the boundary can be nested.
- A resource can be refetched on demand, keeping previous data visible during the refetch.
- `<ErrorBoundary>` renders the error slot with the error value and allows retry.
- A deferred resource starts loading only when first read.
- Reactive scope cleanup cancels any in-flight resource load.
- All stated test cases for these states and transitions pass.

**Design traces**: `design/ferric/async-forms-events.md` §1 (REQ-ASYNC-001 through REQ-ASYNC-016,
REQ-ASYNC-015); BAR-FERRIC-012.
**Verification**: automated_test.
**Depends on**: #140 (Component model — delivered by PR #188).

### #144 — Ferric 1.0: DOM event handling

**Acceptance criteria** (from issue body):
- An author attaches handlers to DOM events using `on:<event_name>={handler}` syntax in `view!`.
- The handler receives a typed payload (the concrete event type) for all named events: click, input,
  change, submit, keydown, keyup, keypress, focus, blur.
- `event.prevent_default()` and `event.stop_propagation()` compile and work.
- For an event not in the named set, an author can attach a handler by string name as an escape
  hatch.
- Examples for each category compile.

**Design traces**: `design/ferric/async-forms-events.md` §2 (REQ-ASYNC-020 through REQ-ASYNC-024);
BAR-FERRIC-013.
**Verification**: automated_test.
**Depends on**: #139 (view! macro surface — delivered by PR #188).

### #145 — Ferric 1.0: Forms and two-way binding

**Acceptance criteria** (from issue body):
- An author binds a signal to a text input, checkbox, and `<select>` two-way: the input reflects
  the current signal value and a change to the input updates the signal.
- A submit handler on a `<form>` fires with the form data.
- Validation feedback can be wired to a signal updated on submit or on change.
- Stated examples for each input kind compile and demonstrate the two-way relationship.

**Design traces**: `design/ferric/async-forms-events.md` §3 (REQ-ASYNC-040 through REQ-ASYNC-043);
BAR-FERRIC-014.
**Verification**: automated_test.
**Depends on**: #144 (DOM event handling — in this epic).

---

## Inputs

### Landed authoring model (the base to build on)

PR #188 merged at `aa2468771eccd9e2ee79c12c79b8943fca18e07a` (branch `main` on
`Nousix-LLC/nswe-demo`) delivers all Ferric 1.0 Authoring Model (epic #129) capabilities —
reactive signals (`create_signal`, `Signal`, `Memo`, `create_effect`, `batch`, `create_memo`),
virtual DOM (`VNode`, `VElement`, `VText`), the `view!` macro, component model (props, children,
named slots, dynamic dispatch), context, and the WASM runtime (`mount`, the event loop). This is
the base; `work/ferric-async-forms-r1` branches from it.

**Frozen surfaces** (additive constraint — do not remove or redefine):
- `create_signal`, `Signal<T>`, `Memo<T>`, `create_effect(impl FnMut() + 'static)`, `create_memo`,
  `batch`, `mount`, `VNode`, `VElement`, `VElement::on(kind, || …)`, `EventHandler = Rc<dyn Fn()>`,
  `EventKind::Click`, `EventKind::Input`.
- The existing reactive-core tests must still pass with the new surface in place.

### Design documents

- `design/ferric/async-forms-events.md` (commit `ade5bdde424638b9f993c5699219c638d02e0e59`, PR
  #128 merged) — the primary design for this epic: §1 async resources and suspense
  (REQ-ASYNC-001..016), §2 DOM event handling (REQ-ASYNC-020..024), §3 forms and two-way binding
  (REQ-ASYNC-040..043). All 25 requirements in this file are the acceptance bar for this goal.
- `design/ferric/scope-and-requirements.md` (same commit) — the full 1.0 requirement index;
  BAR-FERRIC-012 through BAR-FERRIC-014 are the bar entries for this epic.

### Repo

`Nousix-LLC/nswe-demo` — `crates/ferric` is the library crate this goal extends.

---

## Declared output

- Commits on branch `work/ferric-async-forms-r1` (never force-pushed).
- One PR into `main` with:
  - `Closes #130`, `Closes #143`, `Closes #144`, `Closes #145` in the description.
  - Description written for the repository's readers: what changed, how it was verified, what it
    closes. No host paths or taskflow internals.
- Root `SYNTHESIS.md` at the DAG's workspace (`taskflow/dags/ferric-async-forms-r1/SYNTHESIS.md`),
  accounting for each issue: met or not, and why.
- CI all six jobs PASS on the PR head: `fmt`, `clippy`, `test`, `wasm`, `doc`, `image`.

---

## Concerns to evaluate

### C1 — Correctness against the design

Each of the 25 requirements in `design/ferric/async-forms-events.md` is met. For each:
- REQ-ASYNC-001..016: `create_resource` and the suspense/error-boundary primitives behave as the
  requirement states from the author's side.
- REQ-ASYNC-020..024: the payload-carrying handler form, the extended event surface, event-data
  reads, `preventDefault`/`stopPropagation`, and re-binding guarantees all hold.
- REQ-ASYNC-040..043: two-way binding across all required input kinds, reactive validation
  ergonomics, and submission ergonomics all behave as stated.
- The additive constraint holds: all frozen surfaces remain valid and their existing tests pass.

### C2 — CI: all six jobs PASS

`fmt`, `clippy`, `test`, `wasm`, `doc`, `image` all pass on the PR head commit (GitHub Actions CI
on `Nousix-LLC/nswe-demo`). No warnings treated as errors by clippy. WASM build succeeds for
`crates/ferric` and `crates/chirp-frontend`. Doc builds without broken links or missing crate
references.

### C3 — Test coverage

Automated tests cover:
- Each of the four resource states (loading, loaded, empty, error), the transitions between them,
  and re-fetch with prior-value preservation.
- Suspense boundary aggregation (multiple pending resources → single fallback; boundary resolves
  when all do) and nesting.
- Each named event kind (click, input, change, submit, keydown, keyup, keypress, focus, blur)
  receiving the correct payload and `preventDefault`/`stopPropagation` working.
- Two-way binding for each required input kind (text, checkbox, radio, select, number) in both
  directions.
- Reactive validation derived from bound signals appearing and clearing in the rendered output.
- Submit suppressing the default navigation and reading the model.
Tests run in `wasm-bindgen-test` where DOM is required, `cargo test` for pure reactive logic.

### C4 — Rust idioms and API surface quality

The new API is idiomatic Rust: clean generics, no unnecessary `Rc<RefCell<>>` sprawl, appropriate
use of `wasm-bindgen-futures` for async, documentation for all public items. The event-payload
surface does not introduce a bespoke event model but rather exposes `web_sys` types directly (per
REQ-ASYNC-022/REQ-FW-013). The two-way binding affordance is discoverable and consistent with how
signals work in the authoring model.

### C5 — API surface compatibility with the authoring model on main

Nothing in this PR changes or removes any API item present on `main` at `aa24687`. Code written
against the authoring model (using `create_signal`, `Signal`, `view!`, `component`, `context`,
`mount`) continues to compile and behave identically. The additive guarantee in REQ-ASYNC-015 and
REQ-ASYNC-020-A1 is verified by the existing reactive-core tests passing unchanged.

---

## Constraints

- Repo: `Nousix-LLC/nswe-demo`.
- Branch: `work/ferric-async-forms-r1`. Never force-push.
- Do not modify anything under `design/` (design documents are read-only inputs).
- Do not merge the PR. The overseer's review gate does that.
- Do not prescribe decomposition; choose your own.
