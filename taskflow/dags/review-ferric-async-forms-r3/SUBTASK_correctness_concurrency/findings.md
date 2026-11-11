# Correctness and Concurrency Findings
# review-ferric-async-forms-r3 / SUBTASK_correctness_concurrency

**PR**: #193 — Ferric async resources, expanded events, and form binding  
**Head SHA**: `838239e`  
**Scope**: REQ-ASYNC-001, 003, 005, 016, 023, 042 + concurrency/async hazard assessment  
**Spoke inputs**: b1_findings.md (async_resource.rs), b2_findings.md (vdom.rs + dom.rs), b3_findings.md (form.rs)

---

## Findings

### REQ-ASYNC-001 — create_resource two-argument reactive constructor

- **severity**: clean
- **requirement**: REQ-ASYNC-001
- **location**: `crates/ferric/src/async_resource.rs:207–219`
- **description**: `create_resource` takes exactly two arguments — `source: impl Fn() -> S + 'static` and `fetcher: impl Fn(S) -> F + 'static`. `create_effect` is invoked on line 219 and runs its closure eagerly (first execution is synchronous), calling `source()` on line 221, resetting the signal to `Loading` on line 224, and calling `spawn_local` on line 237. The resource fires on construction without any external trigger. REQ-ASYNC-001 is satisfied.

---

### REQ-ASYNC-003 — Source signal change resets to Loading and re-triggers fetcher

- **severity**: clean
- **requirement**: REQ-ASYNC-003
- **location**: `crates/ferric/src/async_resource.rs:219–248`
- **description**: `source()` is called inside the `create_effect` closure, which registers any signals it reads as dependencies. When a tracked signal changes, the full effect body re-runs. Line 224 resets state to `ResourceState::Loading` before the new fetch begins; line 231 calls `fetcher(source_value)` with the updated value; lines 236–244 spawn the new future. The WASM integration test `create_resource_refetches_on_source_change` (lines ~760–793) confirms the transition sequence. REQ-ASYNC-003 is satisfied.

---

### REQ-ASYNC-005 — Stale in-flight futures discarded on new source value

- **severity**: clean
- **requirement**: REQ-ASYNC-005
- **location**: `crates/ferric/src/async_resource.rs:217, 228–229, 236, 240–241`
- **description**: The generation counter (`Rc::new(Cell::new(0u64))`) is incremented before each spawn. The async closure captures the shared `Rc` and the spawn-time generation value. After `fut.await`, the guard on line 240 (`gen_check.get() == next_gen`) compares the current counter against the spawn-time generation. Only the most recently spawned future holds the highest `next_gen` and succeeds the check; every earlier in-flight future discards its result silently. REQ-ASYNC-005 is satisfied.

---

### REQ-ASYNC-016 — Generation counter: stale future's result silently dropped

- **severity**: clean
- **requirement**: REQ-ASYNC-016
- **location**: `crates/ferric/src/async_resource.rs:217–243`
- **description**: The generation counter design is sound. Traced through the multi-source-change scenario: effect run N increments `gen` to N, spawning future Fₙ with `next_gen = N`; effect run N+1 increments `gen` to N+1, spawning Fₙ₊₁ with `next_gen = N+1`. When Fₙ resolves, `gen_check.get()` returns N+1, the guard fails, and the result is discarded. When Fₙ₊₁ resolves, `gen_check.get()` returns N+1, the guard passes, and the result is applied. Even in a non-FIFO network scenario (Fₙ₊₁ resolves before Fₙ), Fₙ's later resolution is correctly rejected. No overflow risk in practice for a `u64`. REQ-ASYNC-016 is satisfied.

---

### Concurrency hazard assessment — spawn_local / create_effect composition

- **severity**: clean
- **requirement**: (concurrency hazard assessment)
- **location**: `crates/ferric/src/async_resource.rs:219–248`
- **description**: No double-borrow or use-after-free hazard. `Cell<u64>` does not issue borrows — `.get()` and `.set()` both take `&self` and operate in-place. `signal: Signal<ResourceState<T>>` is `Copy`, so the effect closure and the async closure each hold independent handles. No reference or borrow is held across any `await` point. The effect closure runs to completion synchronously before any spawned microtask can execute, eliminating reentrant access. WASM executes on a single JS event-loop thread; `spawn_local` queues futures onto the microtask queue — they never execute concurrently with the synchronous `create_effect` closure. The `!Send` marker on `Rc<Cell<u64>>` enforces the single-threaded invariant at compile time. No race scenario is possible under the WASM execution model.

---

### REQ-ASYNC-023 — EventHandler enum redesign

- **severity**: clean
- **requirement**: REQ-ASYNC-023
- **location**: `crates/ferric/src/vdom.rs:195–200`, `crates/ferric/src/dom.rs:272–274`
- **description**: `EventHandler` is declared as a public enum with two variants: `NoArg(Rc<dyn Fn()>)` preserving the prior zero-argument shape, and `WithEvent(Rc<dyn Fn(&dyn std::any::Any)>)` for event-carrying closures. `vdom.rs` imports only `std` crates (lines 31–33); no `web_sys` import is present, keeping the module native-testable. The `.on()` builder wraps handlers in `NoArg`, preserving backward compatibility for all existing callers. The event dispatch in `dom.rs` (lines 272–274) correctly matches both variants: `NoArg(f) => f()` and `WithEvent(f) => f(&event as &dyn std::any::Any)`. The WASM test `event_carrying_handler_can_call_prevent_default` (dom.rs:629–656) confirms the full downcast path `&dyn Any → &web_sys::Event → prevent_default()` succeeds in a live browser runtime. REQ-ASYNC-023 is fully satisfied.

---

### REQ-ASYNC-042 — Bind::on_input_event_handler()

- **severity**: clean
- **requirement**: REQ-ASYNC-042
- **location**: `crates/ferric/src/form.rs:215–226`
- **description**: `Bind<T>::on_input_event_handler(&self) -> EventHandler` exists, is `pub`, and is gated `#[cfg(target_arch = "wasm32")]` (compatible with the requirement: browser-only DOM types). The method returns `EventHandler::WithEvent(Rc::new(...))`. The closure body performs all three downcast steps in order: `downcast_ref::<Event>()` on the `&dyn Any`, `event.target()`, and `target.dyn_into::<HtmlInputElement>()`. Each step uses `if let`, so failure at any point leaves the signal unchanged — no panic, no crash. The successful path calls `raw.set(input_el.value())` synchronously on each `input` event. The WASM test `on_input_event_handler_updates_signal_from_dom_value` (form.rs:488–530) exercises the full DOM→signal path with a real DOM element, synthetic dispatch, and a signal equality assertion. REQ-ASYNC-042 is fully satisfied.

---

## What was examined

| Spoke | File | Lines | Questions covered |
|-------|------|-------|-------------------|
| B1+concurrency | `crates/ferric/src/async_resource.rs` | 207–251 | REQ-ASYNC-001: two-arg API, immediate fire; REQ-ASYNC-003: Loading reset, re-trigger; REQ-ASYNC-005: stale future discard; REQ-ASYNC-016: generation counter soundness; concurrency: borrow safety, `!Send` correctness, single-threaded race scenario, `'static` bounds |
| B1+concurrency | `crates/ferric/src/async_resource.rs` | ~680–832 | Native unit tests (source change reset, two-change counter), WASM integration tests |
| B2 | `crates/ferric/src/vdom.rs` | 1–35, 190–205, 315–340 | REQ-ASYNC-023: enum declaration, WithEvent type, no `web_sys` import, `.on()` backward compat, `.on_with_event()` builder |
| B2 | `crates/ferric/src/dom.rs` | 45–55, 229, 265–285, 596–660 | REQ-ASYNC-023: dispatch of both variants, WASM test `event_carrying_handler_can_call_prevent_default` |
| B3 | `crates/ferric/src/form.rs` | 1–36, 112–157, 160–192, 193–226, 466–530 | REQ-ASYNC-042: method existence and signature, WithEvent return, downcast chain, signal write ordering, cfg gate, graceful failure paths, WASM test |

**Coverage confirmation:**
- REQ-ASYNC-001: verified clean (B1)
- REQ-ASYNC-003: verified clean (B1)
- REQ-ASYNC-005: verified clean (B1)
- REQ-ASYNC-016: verified clean (B1)
- REQ-ASYNC-023: verified clean (B2)
- REQ-ASYNC-042: verified clean (B3)
- Concurrency / async hazard assessment: verified clean (B1)

**Blocker summary**: No blockers. All requirements verified clean across all three spokes.

**Non-blocker constraint**: No prior non-blockers (#196–#201) were re-raised by any spoke.

**CI evidence**: All 6 jobs (`fmt`, `clippy`, `doc`, `test`, `wasm`, `image`) passed at `838239e` (https://github.com/Nousix-LLC/nswe-demo/actions/runs/42126720006).
