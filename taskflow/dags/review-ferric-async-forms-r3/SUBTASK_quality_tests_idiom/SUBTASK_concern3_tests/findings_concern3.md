## Findings — Concern 3 (Test Coverage and Depth)

---

### Finding C3-1 — Generation counter guard: no WASM test exercises the discard path

- **severity**: non-blocker
- **concern**: tests
- **requirement**: REQ-ASYNC-016, REQ-ASYNC-005
- **location**: `crates/ferric/src/async_resource.rs` (generation guard at lines ~71–75; native test `create_resource_two_source_changes_stay_loading` at ~lines 724–738; WASM test `create_resource_refetches_on_source_change` at ~lines 740–757)
- **description**: REQ-ASYNC-016 states the stale future's result must be silently dropped; only the latest generation's result is applied. The guard responsible is:

  ```rust
  if gen_check.get() == next_gen {
      signal.set(ResourceState::Ready(value));
  }
  ```

  Two tests address this area:

  1. **`create_resource_two_source_changes_stay_loading`** (native `#[test]`): Changes the source signal twice and asserts `ResourceState::Loading` holds. This confirms the effect correctly resets state and increments the generation counter on each source change. It does NOT exercise the guard: on native, `spawn_local` is a no-op, so no future actually runs and the branch `gen_check.get() == next_gen` is never evaluated. If the guard were deleted entirely, this test would still pass.

  2. **`create_resource_refetches_on_source_change`** (WASM `#[wasm_bindgen_test]`): Calls `tick().await` to completion after the first source value, then changes the source, then calls `tick().await` again. By the time `src.set(5)` fires, the first future has already resolved and written its result; there is no in-flight stale future to discard. The generation guard is never in a state where `gen_check.get() != next_gen` during the second await. If the guard were inverted (`gen_check.get() != next_gen`) this test would still pass.

  The concurrent scenario REQ-ASYNC-016 specifically guards against — first future still in flight when source changes, second future dispatched, first future resolves late — has no test. A behavioral test would need to hold the first future pending (e.g., via a channel or a future that awaits a signal), change the source, then resolve the first future last, and assert that `resource.state()` reflects the second fetch's result, not the first's.

  **Severity rationale**: The implementation is present and logically correct. The requirement is met in code; the gap is test proof of the specific discard behavior. Per calibration, this is non-blocker because the requirement is not unmet — it is untested for one scenario.

---

### Finding C3-2 — `on_input_event_handler_updates_signal_from_dom_value`: clean

- **severity**: clean
- **concern**: tests
- **requirement**: REQ-ASYNC-042
- **location**: `crates/ferric/src/form.rs` (WASM test module, `on_input_event_handler_updates_signal_from_dom_value`)
- **description**: The test:
  - Creates a real `HtmlInputElement` via `document.create_element("input")`
  - Attaches it to `document.body()` (a live DOM element, not a detached fragment)
  - Sets the input's value to `"hello"` via `input_el.set_value("hello")`
  - Builds a `FormField<String>`, creates a `Bind`, obtains `on_input_event_handler()`
  - Registers the handler as a real DOM event listener via `add_event_listener_with_callback`
  - Dispatches a real `web_sys::Event::new("input")` via `dispatch_event`
  - Asserts `field.raw() == "hello"` with a message naming REQ-ASYNC-042
  - Cleans up by removing the element from the body

  Every step of the acceptance criterion's end-to-end path is exercised: DOM attachment, real event dispatch, `HtmlInputElement::value()` read, signal write. The assertion is behavioral — it would fail if `on_input_event_handler` failed to read the DOM value or failed to write the signal. This is the correct pattern for WASM UI tests.

---

### Finding C3-3 — `event_carrying_handler_can_call_prevent_default`: clean

- **severity**: clean
- **concern**: tests
- **requirement**: REQ-ASYNC-023
- **location**: `crates/ferric/src/dom.rs` (WASM test module, `event_carrying_handler_can_call_prevent_default`)
- **description**: The test:
  - Creates an `EventHandler::WithEvent` whose closure downcasts `&dyn Any` to `&web_sys::Event` and calls `prevent_default()`
  - Creates a `web_sys::Event::new("click")`
  - Asserts `!event.default_prevented()` before dispatch (baseline)
  - Dispatches the handler directly: `f(&event as &dyn std::any::Any)`
  - Asserts `event.default_prevented()` after dispatch (behavioral)

  The before-and-after assertion pattern is exactly right: it proves `prevent_default()` took effect, not merely that the handler ran. If `prevent_default()` were removed from the closure, the final assertion would fail. This satisfies the behavioral depth requirement for REQ-ASYNC-023.

---

### Finding C3-4 — Acceptance criteria coverage summary

- **severity**: clean (with C3-1 non-blocker noted)
- **concern**: tests
- **description**: Coverage across all in-scope acceptance criteria:

  | Requirement | Test | Behavioral depth |
  |-------------|------|-----------------|
  | REQ-ASYNC-001 | `create_resource_fires_immediately` (native), `create_resource_refetches_on_source_change` (WASM) | Yes — asserts `ResourceState::Ready(11)` after `tick()` |
  | REQ-ASYNC-003 | `create_resource_two_source_changes_stay_loading` (native), `create_resource_refetches_on_source_change` (WASM) | Yes — asserts `Loading` immediately after source change, `Ready(15)` after second tick |
  | REQ-ASYNC-005 | `create_resource_refetches_on_source_change` (WASM) — sequential case only | Partial — sequential re-fetch proven; concurrent discard unproven (see C3-1) |
  | REQ-ASYNC-016 | No test exercises `gen_check.get() != next_gen` path | Gap — see C3-1 |
  | REQ-ASYNC-023 | `event_carrying_handler_can_call_prevent_default` (WASM) | Yes — `default_prevented()` asserted true |
  | REQ-ASYNC-042 | `on_input_event_handler_updates_signal_from_dom_value` (WASM) | Yes — `field.raw() == "hello"` after real DOM event |

  All six requirements have at least one test touching their core path. REQ-ASYNC-016's specific claim (stale write discarded) is the only scenario with no test verifying the discard behavior, documented in C3-1.

---

## What was examined

**Test functions reviewed:**

1. `crates/ferric/src/async_resource.rs`
   - `create_resource_fires_immediately` — asserts `ResourceState::Loading` before tick, `Ready(11)` after; behavioral (REQ-ASYNC-001)
   - `create_resource_two_source_changes_stay_loading` — asserts `Loading` on each source change; behavioral for reset, vacuous for discard (REQ-ASYNC-003/REQ-ASYNC-016)
   - `create_resource_refetches_on_source_change` (WASM) — asserts sequential re-fetch; behavioral for REQ-ASYNC-003; covers REQ-ASYNC-005 sequential case only

2. `crates/ferric/src/dom.rs`
   - `event_carrying_handler_can_call_prevent_default` (WASM) — asserts `default_prevented()` = true; behavioral (REQ-ASYNC-023)

3. `crates/ferric/src/form.rs`
   - `on_input_event_handler_updates_signal_from_dom_value` (WASM) — real DOM, real event dispatch, signal assertion; behavioral (REQ-ASYNC-042)

**Assertions inspected per test:**
- Generation counter guard path: verified `spawn_local` is conditional on `cfg(target_arch = "wasm32")`, confirming native tests cannot exercise async dispatch
- `tick().await` ordering in WASM refetch test: confirmed both source changes are sequential, not concurrent
- DOM attachment in form WASM test: confirmed `append_child` to `document.body()` before dispatch
- Before/after `default_prevented()` assertions in dom WASM test: confirmed both assertions present

**Acceptance criteria mapped:** REQ-ASYNC-001 ✓, REQ-ASYNC-003 ✓, REQ-ASYNC-005 partial, REQ-ASYNC-016 gap (non-blocker), REQ-ASYNC-023 ✓, REQ-ASYNC-042 ✓
