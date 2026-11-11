# Partial Findings — Concern 3: Test Coverage and Depth

## Findings

- **severity**: blocker
  **concern**: tests
  **location**: crates/ferric/src/async_resource.rs:652
  **description**: The native test `create_resource_two_source_changes_stay_loading` (line 655) carries
  a doc comment that says: "We test this by reading the internal `gen` state indirectly via two
  successive source changes: each change sets Loading (not Ready), proving no stale overwrite
  happened." That claim is incorrect. On non-wasm targets the effect body takes the
  `#[cfg(not(target_arch = "wasm32"))]` branch (`drop(fut)`) — no future is ever spawned, and
  the generation counter's stale-write guard (`if gen_check.get() == next_gen`) never executes.
  The test demonstrates only that a source change re-runs the effect and resets state to Loading,
  not that a concurrent in-flight future's result is discarded. The core REQ-ASYNC-016 scenario —
  source changes while a fetch is mid-flight, the first fetch later resolves, its result must be
  discarded — requires WASM to exercise because `spawn_local` is gated to wasm32.

  The WASM test `create_resource_refetches_on_source_change` (line 778) covers sequential
  refetch only: it waits (`tick().await`) until the first fetch reaches `Ready`, then changes
  the source, then waits for the second fetch to reach `Ready`. In this sequence the first
  future has already completed and been written before the source changes, so the generation
  guard never has a stale write to block. If the check (`if gen_check.get() == next_gen`) were
  deleted, every existing test would still pass.

  What would satisfy: a WASM test that (1) constructs a fetcher backed by a manually-held
  `Promise` resolve handle so the test controls when the future completes; (2) triggers the
  first fetch (gen=1 is started, state is Loading); (3) changes the source signal before
  releasing the first future (gen=2 starts, state remains Loading); (4) releases the first
  future; (5) asserts the signal did *not* become `Ready` with the first result (state is still
  Loading or has become `Ready` with the second result). That test would fail if the generation
  guard were removed.

- **severity**: non-blocker
  **concern**: tests
  **location**: crates/ferric/src/form.rs:220
  **description**: The doc comment for `on_input_event_handler` explicitly names two fail-silent
  paths: "If any step fails (target absent, or the target is not an `<input>` element), the
  closure returns without updating the signal — no panic." Neither path has a test. The WASM
  test at line 488 covers the happy path only. A bug in either branch — for example, panicking
  instead of returning silently, or writing a stale value — would go undetected. These are
  documented behavioral contracts, not implementation details. Satisfying condition: two focused
  WASM tests, each constructing a `WithEvent` handler and passing (a) an event with no target
  and (b) an event whose target is a non-input element, asserting in both cases that the signal
  value did not change.

- **severity**: clean
  **concern**: tests
  **location**: crates/ferric/src/form.rs:488
  **description**: Checked `on_input_event_handler_updates_signal_from_dom_value` for REQ-ASYNC-042
  behavioral depth. The test: creates a real `<input>` element via `document.create_element`;
  attaches it to `document.body()` before dispatch (ensuring `event.target()` resolves);
  writes the DOM value with `input_el.set_value("hello")`; wires the `on_input_event_handler()`
  closure to the element via a `wasm_bindgen::Closure`; dispatches a genuine synthetic event via
  `input_el.dispatch_event`; and asserts `field.raw() == "hello"` with a labeled assertion
  message. The test does not shortcut by calling the handler directly — the event dispatch goes
  through the browser's event system so `event.target()` is set by the runtime. DOM cleanup
  is performed at the end. The full DOM→signal path is exercised end-to-end.

- **severity**: clean
  **concern**: tests
  **location**: crates/ferric/src/dom.rs:630
  **description**: Checked `event_carrying_handler_can_call_prevent_default` for REQ-ASYNC-023
  behavioral depth. The test asserts `!event.default_prevented()` before the handler runs
  (pre-condition guard), invokes the `WithEvent` handler with a real `web_sys::Event`, then
  asserts `event.default_prevented()` is `true` with a labeled message. The behavioral assertion
  would catch deletion of the `prevent_default()` call; the test is not vacuous. The handler is
  invoked directly rather than through `set_events` + `dispatch_event`; the author notes that
  the event-binding path is covered by `mount_renders_initial_view_and_reacts_to_signal_change`.
  No stated requirement demands a combined path test.

- **severity**: clean
  **concern**: tests
  **location**: crates/ferric/src/dom.rs:595
  **description**: Checked REQ-ASYNC-023 acceptance criteria coverage. The requirement is that a
  `WithEvent` handler can call `prevent_default()` on the DOM event and have the cancellation
  take effect. The WASM test at line 630 covers this directly with a behavioral assertion. No
  gap in stated-requirement coverage was found beyond what is reported above.

---

## What was examined

- `crates/ferric/src/async_resource.rs` (full file, 833 lines, commit 838239e via GitHub API)
  - Generation counter implementation (`#[cfg(target_arch = "wasm32")]` / `drop(fut)` branches)
  - Native `mod tests` block (line 320): `create_resource_source_change_resets_to_loading`
    (line 618) and `create_resource_two_source_changes_stay_loading` (line 655) including
    the doc comment's stale-overwrite claim
  - WASM `mod wasm_tests` block (line 722): `create_resource_refetches_on_source_change`
    (line 778) — test structure analyzed for sequential vs. concurrent coverage
- `crates/ferric/src/form.rs` (full file, commit 838239e via GitHub API)
  - `on_input_event_handler` implementation and doc comment (fail-silent paths)
  - `Bind::on_input_handler` (buffer-based approach) and all native tests for `Bind`
  - WASM `mod wasm_tests` (line 466): `on_input_event_handler_updates_signal_from_dom_value`
    (line 488) — analyzed for real DOM attachment, genuine event dispatch, signal assertion,
    and DOM cleanup
- `crates/ferric/src/dom.rs` (full file, commit 838239e via GitHub API)
  - WASM `mod wasm_tests` (line 595): `event_carrying_handler_can_call_prevent_default`
    (line 630) — analyzed for pre-condition assertion, `default_prevented()` post-assertion,
    and whether the test covers the stated REQ-ASYNC-023 behavioral contract
  - `mount_renders_initial_view_and_reacts_to_signal_change` — examined as the complementary
    test covering the event-binding path

- Sub-questions addressed:
  - [x] Q1: Do native tests exercise in-flight source changes with behavioral assertions on stale-future resolution? — No; gap identified (blocker).
  - [x] Q2: Does the WASM test for REQ-ASYNC-042 attach a real DOM element, dispatch a genuine event, and assert signal state? — Yes; clean.
  - [x] Q3: Does the WASM test for `prevent_default` verify `event.default_prevented()` returns `true`? — Yes; clean.
  - [x] Q4: Are there acceptance criteria scenarios for REQ-ASYNC-042 and REQ-ASYNC-023 without test coverage? — REQ-ASYNC-042 fail-silent paths are undocumented in tests (non-blocker); REQ-ASYNC-023 is fully covered.
