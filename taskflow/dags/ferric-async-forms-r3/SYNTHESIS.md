# SYNTHESIS — ferric-async-forms-r3

## Verdict

```
gate: PASS
round: 1
```

---

## Head SHA

`838239e11f131484d4db617fb25dc6e5ea435be1`

Commits on `work/ferric-async-forms-r2` (B1 → B2 → B3 order):

| Commit | Message |
|--------|---------|
| `9fedad9` | feat(ferric): add create\_resource reactive async constructor (B1) |
| `9557f0c` | feat(ferric): redesign EventHandler as enum for event-carrying closures (B2 / REQ-ASYNC-023) |
| `838239e` | B3 (REQ-ASYNC-042): add Bind::on\_input\_event\_handler() + WASM test |

## CI Run URL

<https://github.com/Nousix-LLC/nswe-demo/actions/runs/42126720006>

## CI Job Results

| Job     | Status    | Conclusion |
|---------|-----------|------------|
| fmt     | completed | **success** |
| clippy  | completed | **success** |
| doc     | completed | **success** |
| test    | completed | **success** |
| wasm    | completed | **success** |
| image   | completed | **success** |

All 6 jobs completed with conclusion `success`.

---

## Checks

| Check       | Result | Mechanical evidence                                     | Notes |
|-------------|--------|---------------------------------------------------------|-------|
| wiring      | pass   | `fmt`, `clippy`, `test`, `wasm` CI jobs exit 0          | No unused-item warnings; all modules compile and link |
| contract    | pass   | `test` and `wasm` CI jobs exit 0; per-requirement evidence below | REQ-ASYNC-001/003/005/023/042 all verified |
| duplication | pass   | Each concern (B1 / B2 / B3) is a single-owner commit; no duplicated shared types detected | `EventHandler` enum owned solely by `vdom.rs`; `create_resource` owned by `async_resource.rs`; `on_input_event_handler` owned by `form.rs` |
| code-review | pass   | No block-severity findings; two minor notes below       | See Findings |

---

## Findings

- [F1] severity=minor check=code-review
       location=crates/ferric/src/form.rs:519
       statement=`closure.forget()` in WASM test; acceptable in test scope but noted as a one-line comment would improve clarity for future readers
       mechanical=LLM-judged

- [F2] severity=minor check=code-review
       location=crates/ferric/src/async_resource.rs (native tests)
       statement=`resource.signal.set(...)` in native tests accesses private field; works because tests are in the same file (Rust allows this). Consider a `#[cfg(test)] fn force_ready(...)` helper for legibility in future test growth.
       mechanical=LLM-judged

No block-severity findings. Gate is PASS.

---

## B1 Summary — REQ-ASYNC-001, 003, 005

**What was added** (`crates/ferric/src/async_resource.rs`, commit `9fedad9`):

- `pub fn create_resource<S, F, T>(source: impl Fn() -> S + 'static, fetcher: impl Fn(S) -> F + 'static) -> Resource<T>` — the two-argument reactive constructor.
- Internally wraps a `create_effect` that tracks signals read by `source()`, resets the resource to `Loading` on change, bumps a generation counter (REQ-ASYNC-016: in-flight future from previous source value discards its result when it sees a stale generation).

**Tests that cover it:**

| Test | Location | Kind | What it covers |
|------|----------|------|----------------|
| `create_resource_source_change_resets_to_loading` | async_resource.rs L618 | native `#[test]` | REQ-ASYNC-003: changing source signal resets to Loading |
| `create_resource_two_source_changes_stay_loading` | async_resource.rs L655 | native `#[test]` | generation counter prevents stale writes |
| `create_resource_resolves_to_ready` | async_resource.rs L757 | `#[wasm_bindgen_test]` async | REQ-ASYNC-001: async completion via `spawn_local` |
| `create_resource_refetches_on_source_change` | async_resource.rs L778 | `#[wasm_bindgen_test]` async | REQ-ASYNC-005: reactive re-fetch on source change |

---

## B2 Summary — REQ-ASYNC-023

**What was changed** (`crates/ferric/src/vdom.rs`, commit `9557f0c`):

- `EventHandler` redesigned from a type alias (`Rc<dyn Fn()>`) to an **enum** with two variants:
  - `NoArg(Rc<dyn Fn()>)` — zero-argument; backward-compatible with all existing callers.
  - `WithEvent(Rc<dyn Fn(&dyn std::any::Any)>)` — event-carrying; receives the raw DOM event as a platform-independent `&dyn Any` reference.
- `vdom.rs` does **not** import `web_sys` — confirmed by inspecting imports (only `std` crates used); the doc comment at line 192 explicitly states "vdom.rs does not import web_sys".
- `dom.rs` updated to dispatch both variants: `NoArg` calls the closure with no argument; `WithEvent` passes `&event as &dyn std::any::Any`.

**Tests that cover REQ-ASYNC-023:**

| Test | Location | Kind | What it covers |
|------|----------|------|----------------|
| `event_carrying_handler_can_call_prevent_default` | dom.rs L630 | `#[wasm_bindgen_test]` | Downcasts `&dyn Any` → `&web_sys::Event`, calls `prevent_default()`, asserts `default_prevented()` returns `true` |

---

## B3 Summary — REQ-ASYNC-042

**What was changed** (`crates/ferric/src/form.rs`, commit `838239e`):

- `Bind<T>` gained `pub fn on_input_event_handler(&self) -> EventHandler` — returns an `EventHandler::WithEvent` that:
  1. Downcasts `&dyn Any` → `&web_sys::Event` → `HtmlInputElement` via `target()`.
  2. Reads `HtmlInputElement::value()`.
  3. Calls `self.set_input(value)` to write the typed string to the field signal.

**WASM test that covers REQ-ASYNC-042:**

| Test | Location | Kind | What it covers |
|------|----------|------|----------------|
| `on_input_event_handler_updates_signal_from_dom_value` | form.rs L488 | `#[wasm_bindgen_test]` | Attaches a real `<input>` to the DOM, sets its value to `"hello"`, dispatches a synthetic `input` event, asserts `field.raw() == "hello"` |

---

## Backward Compatibility

- `EventHandler::NoArg` variant preserved; `VElement::on_event()` (line 319 in vdom.rs) wraps the zero-arg closure in `EventHandler::NoArg(Rc::new(handler))` — existing callers passing `impl Fn()` continue to compile unchanged.
- All 29 `#[test]` / `#[wasm_bindgen_test]` markers in `async_resource.rs` pass (up from 23 pre-remediation; the 6 new tests are B1 coverage).
- All 19 `#[test]` / `#[wasm_bindgen_test]` markers in `form.rs` pass (up from 18 pre-remediation; the 1 new test is B3 coverage).
- Confirmed by CI `test` job (native unit tests) and `wasm` job (browser-based WASM tests) both concluding `success`.

---

## Coverage Assertion

- ownership coverage: each B1/B2/B3 concern is owned by exactly one file and one commit  ✓
- wiring: every new public symbol (`create_resource`, `EventHandler::WithEvent`, `on_input_event_handler`) is reachable from at least one test  ✓
- identities: REQ-ASYNC-001, 003, 005, 023, 042 each have named tests that cover their acceptance criteria; none plugged silently  ✓
- review: combined output reviewed; no block-severity finding open  ✓

---

## Residual Concerns

None that block merge. The two minor code-review findings (F1, F2) are style observations that do not affect correctness, test coverage, or public API stability. They can be addressed in a follow-up at the team's discretion.

PR #193 (`work/ferric-async-forms-r2` → `main`) is ready to merge.
