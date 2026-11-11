# _BRIEF.md — ferric-async-forms-r2 (remediation)

**Goal slug**: `ferric-async-forms-r2`
**Kind**: code DAG (remediation — attempt 2 of 2)
**Launch agent**: swe-coder
**Repo**: Nousix-LLC/nswe-demo
**Branch**: `work/ferric-async-forms-r2`
**Epic**: #130 — Ferric 1.0: Async, Forms, and Events (usable_early)

---

## Lesson from the prior attempt (ferric-async-forms-r1 — FAIL)

**ferric-async-forms-r1 delivered its PR to the wrong repository.** The PR (PR #5) was opened in
`Nousix-LLC/ferric`, which is a separate GitHub repository and is NOT this engagement's target.
All code for this engagement — including `crates/ferric` — lives in `Nousix-LLC/nswe-demo`.
The `Nousix-LLC/ferric` repository has no GitHub Actions CI configuration, so no CI ran
(`statusCheckRollup: []`). The SYNTHESIS self-declared PASS on a local `cargo check`, which does
not meet the declared output requirements.

Specifically:
1. **Wrong repo**: Branch `work/ferric-async-forms-r1` was pushed to `Nousix-LLC/ferric`, not
   `Nousix-LLC/nswe-demo`. PR #5 in `Nousix-LLC/ferric` closes issues #1–4 in that repo's tracker,
   not the nswe-demo board issues #130, #143, #144, #145.
2. **CI not run**: All six CI jobs (`fmt`, `clippy`, `test`, `wasm`, `doc`, `image`) must PASS on
   `Nousix-LLC/nswe-demo`'s GitHub Actions CI. None ran because the wrong repository was targeted.
3. **Declared output not met**: The brief required a PR in `Nousix-LLC/nswe-demo` closing
   #130/#143/#144/#145 with all 6 CI PASS. This was not delivered.

**Do not modify or close PR #5 in `Nousix-LLC/ferric` — leave it as-is.**

---

## Prior code (examine and use if correct)

The five commits on branch `work/ferric-async-forms-r1` in `Nousix-LLC/ferric` implement the three
capabilities:

| Commit | Description |
|--------|-------------|
| `5e49c4f` | Walking skeleton |
| `ab7620a` | async_resource |
| `98a7559` | FormField/Bind |
| `6de5e09` | EventKind set |
| `ad657f5` | Prelude re-exports |

This code may be sound but was delivered to the wrong repository. You must:
1. Examine the prior commits in `Nousix-LLC/ferric` on branch `work/ferric-async-forms-r1`.
2. Assess whether the implementation is correct against the design and acceptance criteria below.
3. If correct (or largely correct), port it into `Nousix-LLC/nswe-demo` on a new branch
   `work/ferric-async-forms-r2`, branched from `main` at
   `aa2468771eccd9e2ee79c12c79b8943fca18e07a`.
4. Ensure all 6 CI jobs PASS on `Nousix-LLC/nswe-demo`.

---

## Objective

Implement **Ferric 1.0 — Async Resources, DOM Events, and Forms** (epic #130) on branch
`work/ferric-async-forms-r2` in `Nousix-LLC/nswe-demo`, branched from `main` at commit
`aa2468771eccd9e2ee79c12c79b8943fca18e07a`.

The goal delivers three tightly coupled capabilities:

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
the frozen authoring-model surface delivered by PR #188.

---

## Issues covered

### #130 — Ferric 1.0: Async, Forms, and Events (epic)

The parent epic. Closed when all three sub-issues are met.

### #143 — Ferric 1.0: Async resources and suspense

**Acceptance criteria**:
- `create_resource` tracks four states — loading, loaded, empty, and error — and re-renders
  consumers when the state changes.
- `<Suspense>` shows the fallback while any enclosed resource is loading and switches to resolved
  content when all are loaded; the boundary can be nested.
- A resource can be refetched on demand, keeping previous data visible during the refetch.
- `<ErrorBoundary>` renders the error slot with the error value and allows retry.
- A deferred resource starts loading only when first read.
- Reactive scope cleanup cancels any in-flight resource load.
- All stated test cases for these states and transitions pass.

**Design traces**: `design/ferric/async-forms-events.md` §1 (REQ-ASYNC-001..016); BAR-FERRIC-012.
**Verification**: automated_test.
**Depends on**: #140 (Component model — delivered by PR #188).

### #144 — Ferric 1.0: DOM event handling

**Acceptance criteria**:
- An author attaches handlers to DOM events using `on:<event_name>={handler}` syntax in `view!`.
- The handler receives a typed payload (the concrete event type) for all named events: click, input,
  change, submit, keydown, keyup, keypress, focus, blur.
- `event.prevent_default()` and `event.stop_propagation()` compile and work.
- For an event not in the named set, an author can attach a handler by string name as an escape
  hatch.
- Examples for each category compile.

**Design traces**: `design/ferric/async-forms-events.md` §2 (REQ-ASYNC-020..024); BAR-FERRIC-013.
**Verification**: automated_test.
**Depends on**: #139 (view! macro surface — delivered by PR #188).

### #145 — Ferric 1.0: Forms and two-way binding

**Acceptance criteria**:
- An author binds a signal to a text input, checkbox, and `<select>` two-way: the input reflects
  the current signal value and a change to the input updates the signal.
- A submit handler on a `<form>` fires with the form data.
- Validation feedback can be wired to a signal updated on submit or on change.
- Stated examples for each input kind compile and demonstrate the two-way relationship.

**Design traces**: `design/ferric/async-forms-events.md` §3 (REQ-ASYNC-040..043); BAR-FERRIC-014.
**Verification**: automated_test.
**Depends on**: #144 (DOM event handling — in this epic).

---

## Inputs

### Landed authoring model (the base to build on)

PR #188 merged at `aa2468771eccd9e2ee79c12c79b8943fca18e07a` (branch `main` on
`Nousix-LLC/nswe-demo`) delivers all Ferric 1.0 Authoring Model capabilities —
reactive signals (`create_signal`, `Signal`, `Memo`, `create_effect`, `batch`, `create_memo`),
virtual DOM (`VNode`, `VElement`, `VText`), the `view!` macro, component model (props, children,
named slots, dynamic dispatch), context, and the WASM runtime (`mount`, the event loop).
Branch `work/ferric-async-forms-r2` MUST be branched from this commit.

**Frozen surfaces** (additive constraint — do not remove or redefine):
- `create_signal`, `Signal<T>`, `Memo<T>`, `create_effect(impl FnMut() + 'static)`, `create_memo`,
  `batch`, `mount`, `VNode`, `VElement`, `VElement::on(kind, || …)`, `EventHandler = Rc<dyn Fn()>`,
  `EventKind::Click`, `EventKind::Input`.
- The existing reactive-core tests must still pass with the new surface in place.

### Prior implementation (to examine and port if correct)

Branch `work/ferric-async-forms-r1` in `Nousix-LLC/ferric` (the wrong repo — do NOT use that repo
for this PR). Commits: `5e49c4f` → `ab7620a` → `98a7559` → `6de5e09` → `ad657f5`. These may
provide a working implementation; examine them for correctness against the design and port into
`Nousix-LLC/nswe-demo` if sound.

### Design documents

- `design/ferric/async-forms-events.md` (commit `ade5bdde424638b9f993c5699219c638d02e0e59`, PR
  #128 merged, in `Nousix-LLC/nswe-demo`) — the primary design: §1 async resources and suspense
  (REQ-ASYNC-001..016), §2 DOM event handling (REQ-ASYNC-020..024), §3 forms and two-way binding
  (REQ-ASYNC-040..043). All 25 requirements are the acceptance bar.
- `design/ferric/scope-and-requirements.md` (same commit) — full 1.0 requirement index;
  BAR-FERRIC-012 through BAR-FERRIC-014 are the bar entries for this epic.

### Repo

`Nousix-LLC/nswe-demo` — `crates/ferric` is the library crate this goal extends.

---

## Declared output

- Commits on branch `work/ferric-async-forms-r2` in `Nousix-LLC/nswe-demo` (never force-pushed).
- One PR into `main` on `Nousix-LLC/nswe-demo` with:
  - `Closes #130`, `Closes #143`, `Closes #144`, `Closes #145` in the description (plain text,
    not inside code blocks).
  - Description written for the repository's readers: what changed, how it was verified, what it
    closes. No host paths or taskflow internals.
- Root `SYNTHESIS.md` at `taskflow/dags/ferric-async-forms-r2/SYNTHESIS.md`, accounting for each
  issue: met or not, and why.
- **CI all six jobs PASS on the PR head in `Nousix-LLC/nswe-demo`**: `fmt`, `clippy`, `test`,
  `wasm`, `doc`, `image`. This is the machine gate; a local `cargo check` does not substitute for
  actual GitHub Actions CI on `Nousix-LLC/nswe-demo`.

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
- If the prior code (ferric-async-forms-r1 commits) is used, verify it correctly meets these
  requirements before porting; correct any gaps found during the assessment.

### C2 — CI: all six jobs PASS in Nousix-LLC/nswe-demo

`fmt`, `clippy`, `test`, `wasm`, `doc`, `image` all pass on the PR head commit on GitHub Actions
CI for `Nousix-LLC/nswe-demo`. No warnings treated as errors by clippy. WASM build succeeds for
`crates/ferric` and `crates/chirp-frontend`. Doc builds without broken links or missing crate
references. **A local build or `cargo check` is not sufficient — actual CI on the target repo must
pass.**

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
against the authoring model continues to compile and behave identically. The additive guarantee in
REQ-ASYNC-015 and REQ-ASYNC-020-A1 is verified by the existing reactive-core tests passing
unchanged.

---

## Constraints

- **Repo: `Nousix-LLC/nswe-demo`** — all commits, the branch, and the PR MUST be in this repo.
  `Nousix-LLC/ferric` is a separate repository; do not create branches or PRs there.
- Branch: `work/ferric-async-forms-r2`, branched from `main` at
  `aa2468771eccd9e2ee79c12c79b8943fca18e07a`. Never force-push.
- Do not modify anything under `design/` (design documents are read-only inputs).
- Do not merge the PR. The overseer's review gate does that.
- Do not prescribe decomposition; choose your own.
- This is remediation attempt 2 of 2. Deliver the full declared output.
