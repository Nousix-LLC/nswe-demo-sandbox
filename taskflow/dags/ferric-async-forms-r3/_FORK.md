owner_id: proc-dce5bfbd-3aae-43e6-ad03-f1b8507bae48
observation_seam: taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md
launch_agent: swe-coder
thread_type: dag
disposition: retain
reap: whole-after-land
launch_context:
  application: software

# _FORK.md — ferric-async-forms-r3

**Owner**: overseer I279
**Program**: swe-coder
**Goal**: Code remediation — ferric async-forms-events review blockers B1, B2, and B3

## Objective

Remediate the three blocking findings from review-ferric-async-forms-r2 on PR #193 (branch `work/ferric-async-forms-r2`):

**B1 — REQ-ASYNC-001, 003, 005: `Resource<T>` is fire-once, not reactive**

`Resource::new(fut: impl Future<Output = T> + 'static)` accepts a pre-constructed `Future` and spawns it exactly once via `spawn_local`. There is no `create_resource(source, fetcher)` constructor, no signal-dependent async function, and no mechanism to re-fetch when reactive dependencies change.

The spec requires:
- REQ-ASYNC-001: `Resource<T>` integrated with the reactive system (re-fetches on signal change)
- REQ-ASYNC-003: `resource()` constructor takes a signal-dependent async function and returns `Resource<T>`
- REQ-ASYNC-005: resource re-fetches when any read signal changes (reactive dependency tracking)

**What satisfies B1**: add a `create_resource(source: impl Fn() -> S + 'static, fetcher: impl Fn(S) -> impl Future<Output = T> + 'static)` constructor that wraps the source in a `create_effect` or equivalent reactive dependency tracker, re-runs the fetcher when the source signal changes, and cancels in-flight futures before starting a new one (REQ-ASYNC-016). The existing `Resource::new` taking a pre-built `Future` may be retained for backward compatibility or converted.

---

**B2 — REQ-ASYNC-023: `prevent_default()` and `stop_propagation()` not callable from handlers**

`EventHandler = Rc<dyn Fn()>` is zero-argument. The DOM closure discards the event: `move |_event: web_sys::Event| { handler(); }`. No mechanism exists for a handler to call `prevent_default()` or `stop_propagation()`.

The spec requires: "REQ-ASYNC-023: `event.prevent_default()` and `event.stop_propagation()` callable from handlers."

The design document specifies an additive payload-carrying handler form (design REQ-ASYNC-020) that keeps the zero-arg form working and adds a form that receives the event.

**What satisfies B2**: add a payload-carrying `EventHandler` variant (e.g., `EventHandlerWithEvent = Rc<dyn Fn(web_sys::Event)>`) or an enum covering both forms. The DOM closure passes the event to handlers that accept it. REQ-ASYNC-023 must be verifiable by test. Ensure this is compatible with BLOCKER-3 resolution (they share the DOM event dispatch path).

---

**B3 — REQ-ASYNC-042: `Bind` DOM→signal direction broken in WASM**

REQ-ASYNC-042 requires "binding updates the signal on user input." `Bind::on_input_handler()` reads `self.input_buf` and writes it to the field's signal, but `input_buf` is updated only by `Bind::set_input()`. The DOM event plumbing in `dom.rs` discards the event and has no reference to the DOM input element or to `Bind::set_input`. Nothing wires up `set_input` from the DOM side.

Result: in the WASM runtime, every input event fires the handler, reads `input_buf` (unchanged since `Bind::new`), and writes the initial value back. The user's typed value is never propagated.

**What satisfies B3**: the DOM layer, before dispatching any `Input`/`Change` handler on an input element, reads the element's current value from the DOM (`HtmlInputElement::value()`) and writes it to the binding (via a hook or closure over the element + binding reference). Option: construct the handler closure at bind time with access to the element, requiring `EventHandler` to support event-carrying closures (entangled with B2). Add at least one WASM test that fires a synthetic input event on an input element bound via `Bind<T>` and asserts the signal was updated with the typed value.

---

## Inputs

- Branch: `work/ferric-async-forms-r2`
- PR: #193 (Nousix-LLC/nswe-demo)
- Review synthesis (accepted DAG): `taskflow/dags/review-ferric-async-forms-r2/SYNTHESIS.md`
- Review comment on PR: https://github.com/Nousix-LLC/nswe-demo/pull/193#issuecomment-6624208222
- Epic: #130 (Async, Forms, and Events)

## Scope

Change only what is needed to satisfy B1, B2, and B3. Do not regress the passing CI checks (all 6 currently pass). The non-blocking issues filed from the review are separate backlog items and are not in scope for this PR.

## Acceptance criteria

- B1 resolved: `create_resource(source, fetcher)` constructor exists; resource re-fetches when the source signal changes; `REQ-ASYNC-001`, `REQ-ASYNC-003`, `REQ-ASYNC-005` satisfied and covered by test.
- B2 resolved: handlers can call `prevent_default()` and `stop_propagation()` on the triggering event; `REQ-ASYNC-023` satisfied and verifiable by test.
- B3 resolved: in the WASM runtime, an input event on a bound `<input>` element updates the signal to the typed value; at least one WASM test covers this.
- All 6 CI checks pass.
- PR #193 updated with the fix commits.

## Declared output

`SYNTHESIS.md` with verdict `PASS` or `FAIL`, carrying:
- commit SHA(s) pushed to `work/ferric-async-forms-r2`
- CI run URL
- summary of what was changed
- any residual concerns

## Governing app file

Load `appfiles/WORK_SESSION.md` (code DAG context) for how to structure the work.
