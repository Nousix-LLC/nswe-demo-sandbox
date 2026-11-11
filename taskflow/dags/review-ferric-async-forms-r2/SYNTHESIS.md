# SYNTHESIS — review-ferric-async-forms-r2

**PR**: https://github.com/Nousix-LLC/nswe-demo/pull/193  
**Branch**: work/ferric-async-forms-r2 → main  
**Head SHA at review launch**: CI run 41780600207 (all 6 jobs pass)  
**Verdict**: **REQUEST CHANGES**

---

## Overall verdict

Three blockers prevent approval. One is a fundamental scope gap in the async-resource primitive (no reactive re-fetch); one is a missing handler capability required by spec (no path to call `prevent_default` or `stop_propagation`); and one is a correctness gap in the form binding that breaks the DOM→signal direction in the WASM runtime. The non-blocking findings are separately filed as backlog issues.

---

## Per-concern summary

### 1. Correctness

**Verdict: BLOCKER (3 blocking, 1 non-blocking)**

**What was checked**: Whether `Resource<T>`, `suspense()`, `EventKind`, custom event handling, `FormField<T>`/`Bind<T>`, event teardown, and the edge cases named in the brief all meet the acceptance criteria for REQ-ASYNC-001..024 and REQ-ASYNC-040..043. The design document (`design/ferric/async-forms-events.md`) was read alongside the brief.

---

**BLOCKER-1 — REQ-ASYNC-001, REQ-ASYNC-003, REQ-ASYNC-005: Resource is fire-once, not reactive**

`Resource::new(fut: impl Future<Output = T> + 'static)` accepts a pre-constructed `Future` and spawns it exactly once via `spawn_local`. There is no `create_resource(source, fetcher)` constructor, no signal-dependent async function, and no mechanism to re-fetch when reactive dependencies change.

The brief explicitly requires all three:
- REQ-ASYNC-001: "Resource<T> type … integrated with the reactive system (re-fetches on signal change)"
- REQ-ASYNC-003: "resource() constructor takes a signal-dependent async function and returns Resource<T>"
- REQ-ASYNC-005: "resource re-fetches when any read signal changes (reactive dependency tracking)"

The design document specifies `create_resource(move || filter.get(), |f| async move { … })` as the declared API shape (not mandated, but indicating the intent). The table in the design shows "reactive source change (REQ-ASYNC-006)" as the primary re-fetch trigger alongside `refetch()` (REQ-ASYNC-007).

The test `resource_state_is_reactive` verifies that *the signal underlying a Resource notifies effects when set directly* — this is built-in signal reactivity, not resource re-fetch. It does not test that the resource calls the fetcher again when a reactive dependency changes, because there is no such mechanism.

File: `crates/ferric/src/async_resource.rs` — `Resource::new`, `Resource::new_fallible`.  
Satisfying: add a `create_resource(source: impl Fn() -> S, fetcher: impl Fn(S) -> impl Future<Output = T>)` constructor that wraps the source in a `create_effect` or equivalent reactive dependency tracker, re-runs the fetcher on source changes, and cancels in-flight futures before starting a new one (REQ-ASYNC-016).

---

**BLOCKER-2 — REQ-ASYNC-023: `prevent_default()` and `stop_propagation()` not callable from handlers**

The brief requires: "REQ-ASYNC-023: `event.prevent_default()` and `event.stop_propagation()` callable from handlers."

`EventHandler = Rc<dyn Fn()>` is zero-argument. In `dom.rs`, the DOM closure discards the event: `move |_event: web_sys::Event| { handler(); }`. There is no mechanism — in the current handler type or in the event dispatch path — for a handler to call `prevent_default()` or `stop_propagation()` on the triggering event.

The design document specifies an additive payload-carrying handler form (design REQ-ASYNC-020) that keeps the zero-arg form working and adds a form that receives the event. Neither form is in this PR.

File: `crates/ferric/src/dom.rs` (closure at the event binding site), `crates/ferric/src/vdom.rs` (EventHandler type).  
Satisfying: either add a payload-carrying `EventHandler` variant that receives `web_sys::Event`, or expose a handler form that wraps `prevent_default`/`stop_propagation` calls without changing the frozen zero-arg signature — and ensure REQ-ASYNC-023 is verifiable by test.

---

**BLOCKER-3 — REQ-ASYNC-042: `Bind` DOM→signal direction broken in the WASM runtime**

REQ-ASYNC-042 requires "binding updates the signal on user input." `Bind::on_input_handler()` returns a closure that reads `self.input_buf` and writes it to the field's raw signal. `input_buf` is updated only by `Bind::set_input()`. The documentation states: "In a WASM renderer, step 1 is performed by the DOM event plumbing (reading `HtmlInputElement::value()` and calling `set_input`) before dispatching the handler."

The DOM event plumbing in `dom.rs` does not do this. Its closure is `move |_event: web_sys::Event| { handler(); }` — the event is discarded, and the closure has no reference to the DOM input element or to `Bind::set_input`. Nothing in the diff wires up `set_input` from the DOM side.

Result: in the WASM runtime, every input event fires the handler, which reads `input_buf` (unchanged since `Bind::new`), and writes the initial value back to the field's signal. The user's typed value is never propagated. The DOM→signal direction of the two-way binding is broken.

The 18 native form tests all call `bind.set_input(…)` manually before firing the handler — they test the abstraction, not the DOM round-trip. The 3 WASM tests cover `Resource`/`suspense` only; no WASM test covers form binding.

File: `crates/ferric/src/form.rs` (Bind struct, `on_input_handler`), `crates/ferric/src/dom.rs` (event dispatch closure).  
Satisfying: either (a) the DOM layer, before dispatching any `Input`/`Change` handler on an input element, reads the element's current value and writes it somewhere the handler can read (requires exposing a hook), or (b) the handler closure closes over the DOM element reference directly (requires the handler to be constructed at bind time with access to the element, which the current `EventHandler = Rc<dyn Fn()>` type does not support). Option (b) is entangled with BLOCKER-2.

---

**Non-blocker: REQ-ASYNC-002 variant name mismatch**

The brief specifies `ResourceState::Error(String)`. The implementation uses `ResourceState::Failed(String)`. The variant name is part of the public API surface and differs from the spec. Semantically equivalent; a renaming ticket is filed separately.

---

**What is sound in correctness**: `suspense()` correctly saves and restores the outer boundary's loading flag across nested boundaries; the transitions `Loading → Ready` and `Loading → Failed` work correctly and reactively notify subscribers; the `suspense` tests (native and WASM) cover the state machine thoroughly. `static_event_kinds()` is exhaustive for the 47 static variants. The stash-key collision prevention (`__ferric_on_custom_{name}` vs `__ferric_on_{name}`) is correct and tested. `FormField<T>` never silently coerces invalid input.

---

### 2. Code quality and design

**Verdict: non-blocker (clean, with one noted limitation)**

The module split (`async_resource.rs`, `form.rs`, `dom.rs`, `vdom.rs`) is clean. Each module owns one responsibility and the coupling is minimal: `async_resource` depends on `signal` and `vdom`; `form` depends on `signal` and `vdom`; `dom` owns the WASM bridge; `vdom` owns the pure data types.

`FormField<T>` / `Bind<T>` is a thoughtful separation: `FormField` is the type-safe validated state; `Bind` is the render-time wiring. The `input_buf` testability abstraction is documented. The limitation is that the abstraction's correctness in WASM depends on a DOM-layer contract that isn't yet implemented (covered by BLOCKER-3 above).

`Resource<T>` is a clean thin wrapper over `Signal<ResourceState<T>>`. The `Copy` impl via signal handle is correct. `thread_local!` for suspense tracking is the right primitive for WASM's single-threaded runtime.

The exhaustive `match` in `event_name()` and `stash_key()` (no wildcard) means the compiler reports any new `EventKind` variant that isn't handled — a good invariant. `static_event_kinds()` is manually maintained (non-blocker; filed separately).

---

### 3. Test coverage and depth

**Verdict: non-blocker (noted gaps)**

The 20 `async_resource.rs` native tests cover all three `ResourceState` variants, the reactive notification contract, all suspense states (fallback/children/failed/nested), and transitions. Assertions check real state values, not vacuous presence. The 3 WASM tests verify that `spawn_local` completes to `Ready`/`Failed` and that `suspense` resolves after a tick.

The 18 `form.rs` native tests cover `FormField` round-trips (valid, invalid, chained), `Bind::value_attr`, `Bind::on_input_handler` with multiple updates and reactive notifications, and an edge case (handler fires without prior `set_input`). Assertions are concrete; no test passes vacuously.

**Gaps (non-blocking):**
- No WASM test covers form binding — the DOM→signal direction is not exercised in the browser environment. This gap is structural (BLOCKER-3 must be fixed before such a test would even be meaningful).
- No test covers teardown: mounting a component with a bound `Bind` or a live `Resource`, then unmounting it, and verifying that listeners are removed and no future writes arrive. The `closure.forget()` model means stale closures may fire after element removal if the element is re-inserted; no test verifies this cannot happen.
- The brief's REQ-ASYNC-009..016 (cancel in-flight on re-fetch, concurrent safety, out-of-order result handling) have no tests because the re-fetch capability is absent.

---

### 4. Security

**Verdict: clean**

**Custom event names** (`EventKind::Custom(String)`) are used only as the string argument to `add_event_listener_with_callback`; they are not evaluated as code or used as privileged keys. The stash key format `__ferric_on_custom_{name}` isolates custom keys from static keys. No trust boundary is crossed.

**DOM values via `Bind`**: `Bind::on_input_handler` reads `input_buf.get()` (a `Signal<String>`), not an arbitrary JS value, so there's no `unwrap` on a JS value. The `Bind` path is DOM-safe.

**wasm-bindgen bridge**: The `js_sys::Reflect::get` calls use `if let Ok(…)` with fallback; `js_sys::Reflect::delete_property` results are discarded (benign). `element.unchecked_ref` is used only after type-narrowing via `is_function()` or `dyn_ref::<js_sys::Array>()`. No `unsafe` block appears anywhere in the diff.

**No infrastructure details**: No server addresses, internal IPs, tailnet addresses, host paths, or taskflow directory paths appear in the diff.

**Dependency**: `wasm-bindgen-futures = "0.4"` is a well-known Rust/WASM crate from the `wasm-bindgen` project, adding no new trust surface.

---

### 5. Rust idioms

**Verdict: non-blocker (one pattern worth noting)**

The `Copy` removal from `EventKind` is sound and necessary — `Custom(String)` cannot be `Copy`. All `*k` usages in `vdom.rs` are updated to `k.clone()`. The `BTreeSet<EventKind>` → `HashSet<EventKind>` change in test code is correct (Ord removed). The `chirp-frontend` usages of `EventKind::Click` and `EventKind::Input` are inline constructor expressions, not stored variables, so removing `Copy` causes no breakage there.

`thread_local!` with `Cell<u32>` / `Cell<bool>` is idiomatic for interior mutability in a single-threaded context (WASM).

`spawn_local` is used correctly: captured variables are `'static` (all closures capture `Signal<ResourceState<T>>`, which is `Copy + 'static`).

**Noted pattern**: `resource_new_starts_loading_wasm` is not guarded with `#[cfg(target_arch = "wasm32")]` despite the name implying it. The test happens to work on native because it uses `std::future::pending()` (which `spawn_local` queues but never runs). The name misleads readers about where the test runs. Non-blocking; filed separately.

`EventKind::KeyPress` is in the DOM spec's deprecation track (deprecated in UI Events in favor of `keydown`/`keyup`). Including it as a first-class variant risks encouraging its use. Non-blocking; filed separately.

No `unsafe`, no gratuitous `Box<dyn …>`, no avoidable `unwrap` on fallible paths. Clippy passes per CI.

---

### 6. API/contract stability

**Verdict: non-blocker (copy-safe for current chirp-frontend; spec naming gap)**

**Prelude exports**: `suspense`, `Resource`, `ResourceState`, `Bind`, `FormField` are all re-exported from `ferric::prelude`. `EventKind` was already there via the top-level `pub use crate::vdom::EventKind`. ✓

**Backward compatibility with chirp-frontend**: The existing usages in `crates/chirp-frontend` are `EventKind::Click` and `EventKind::Input` — both inline constructor expressions passed to `.on(kind, handler)`. The `.on()` method takes `EventKind` by value; inline constructor expressions need no `Copy`. The removal of `Copy` and `Ord` causes no breakage. ✓

**Spec naming gap**: The brief specifies `ResourceState::Error(String)`; the implementation exposes `ResourceState::Failed(String)`. Since `ResourceState` is a public enum that app authors will `match` on, publishing it as `Failed` now and renaming it later is a breaking API change. The variant should match the spec before stabilizing. Non-blocking; filed separately (see BLOCKER-1 fix window is the natural time to rename).

**`static_event_kinds()` sync risk**: The `event_name()` and `stash_key()` functions have exhaustive `match` (compiler-enforced). `static_event_kinds()` is a manually-written array with a comment saying it must stay in sync. A new `EventKind` variant added without updating `static_event_kinds()` silently skips listener detachment for that variant — a correctness gap that would be hard to notice. Filed as a backlog issue.

---

## Blockers summary

| # | Requirement | File | Description |
|---|---|---|---|
| B1 | REQ-ASYNC-001, 003, 005 | async_resource.rs | Resource is fire-once; no reactive re-fetch, no signal-dependent constructor |
| B2 | REQ-ASYNC-023 | dom.rs, vdom.rs | No path to call prevent_default/stop_propagation from a handler |
| B3 | REQ-ASYNC-042 | form.rs, dom.rs | Bind DOM→signal direction broken in WASM; input_buf never updated by DOM event plumbing |

---

## Non-blocking findings (backlog issues)

| Issue | File | Description |
|---|---|---|
| NB-1 | async_resource.rs | `ResourceState::Failed` should be `ResourceState::Error` to match brief spec |
| NB-2 | Cargo.toml | `wasm-bindgen-futures` should use `workspace = true` like sibling wasm-bindgen crates |
| NB-3 | dom.rs | `static_event_kinds()` has no compile-time sync guarantee with EventKind variants |
| NB-4 | async_resource.rs / form.rs | No teardown test: unmount with active Bind or live Resource |
| NB-5 | async_resource.rs | `resource_new_starts_loading_wasm` is not wasm-only but the name implies it is |
| NB-6 | vdom.rs | `EventKind::KeyPress` is deprecated in the DOM spec (UI Events) |

Non-blocking issues filed on Nousix-LLC/nswe-demo:

| Issue | Description |
|---|---|
| [#196](https://github.com/Nousix-LLC/nswe-demo/issues/196) | `ResourceState::Failed` should be `ResourceState::Error` per brief spec |
| [#197](https://github.com/Nousix-LLC/nswe-demo/issues/197) | `wasm-bindgen-futures` should be a workspace dependency |
| [#198](https://github.com/Nousix-LLC/nswe-demo/issues/198) | `static_event_kinds()` needs compile-time sync guarantee with EventKind variants |
| [#199](https://github.com/Nousix-LLC/nswe-demo/issues/199) | Add teardown tests for Bind and Resource lifecycle |
| [#200](https://github.com/Nousix-LLC/nswe-demo/issues/200) | `resource_new_starts_loading_wasm` test name misleads about target |
| [#201](https://github.com/Nousix-LLC/nswe-demo/issues/201) | `EventKind::KeyPress` is deprecated in the DOM spec |

Review posted as comment: https://github.com/Nousix-LLC/nswe-demo/pull/193#issuecomment-6624208222
