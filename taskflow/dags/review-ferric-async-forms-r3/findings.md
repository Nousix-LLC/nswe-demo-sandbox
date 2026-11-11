# PR #193 — Ferric Async Forms: Review Findings (Concerns 2, 3, 6, 7)

PR: `feat(ferric): async resources, expanded events, and form binding` (head `838239e`)

Concerns covered: code quality and design (C2), test coverage and depth (C3), Rust language idiom (C6), API and contract stability (C7).
Concerns not covered here: async/reactive correctness (C1), security (C4), documentation (C5) — handled by sibling tasks.

---

## Findings

<!-- ============================================================ -->
<!-- BLOCKER (1)                                                   -->
<!-- ============================================================ -->

- **severity**: blocker
  **concern**: tests
  **location**: `crates/ferric/src/async_resource.rs:652`
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

<!-- ============================================================ -->
<!-- NON-BLOCKERS (10)                                            -->
<!-- ============================================================ -->

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:14`
  **description**: `suspense()` is colocated in `async_resource.rs` because it reads `SUSPENSE_DEPTH` and `SUSPENSE_HAS_LOADING`, two thread-local sentinels that `create_resource` increments and sets during reactive re-runs. The colocation avoids leaking those private sentinels across a module boundary — a coherent and defensible choice. What is missing is documentation: the module's doc header does not explain that `suspense()` lives here rather than in a view-layer module. A reader arriving at `async_resource.rs` expecting only resource lifecycle machinery will find `suspense()` unexplained. A module-level doc note stating that `suspense()` resides here because of its dependency on the loading sentinels would make the boundary legible without restructuring.

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `structural`
  **description**: The intra-crate dependency graph for the four modules is: `signal` (leaf) → `vdom` → `async_resource` (signal + vdom) / `dom` (vdom only) / `form` (signal + vdom). `async_resource` sits at the same conceptual level as `form` but adds a dependency on `vdom` — a sideways dependency that is mechanically necessary (see the note on `suspense()` colocation above). No cycles exist and no DOM-layer coupling leaks into application-layer modules. The dependency graph is structurally acceptable; the absence of cycles and the clean DOM isolation are what matter. Documenting the sideways dependency in the module-level doc would prevent future contributors from attempting to remove it without understanding the reason.

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:217`
  **description**: `let gen = Rc::new(Cell::new(0u64));` at line 217 carries no inline comment. The function docstring's `# Cancellation (REQ-ASYNC-016)` section explains the counter at the function level, and the increment comment at lines 226–227 explains it at the mutation site. Neither is visible from the declaration line without scrolling. A reader navigating to line 217 via "Go to definition" from the comparison guard hits the declaration without immediate context. A brief inline comment — e.g., `// generation counter: captures current gen in spawned future, discard if superseded` — would make the invariant legible at first contact. The existing docstring and increment-site comment already contain accurate prose; this gap is one of locality rather than missing information.

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/lib.rs:41` and `crates/ferric/src/async_resource.rs:207`
  **description**: `ferric::prelude` exports `Resource` and `ResourceState` but not `create_resource`. A caller using `use ferric::prelude::*` sees `Resource::new` as the natural construction path; `create_resource` is reachable only via the full module path `ferric::async_resource::create_resource`. The two functions serve different needs: `Resource::new` starts a one-shot future with no reactive re-triggering; `create_resource` wraps the future in a reactive effect and re-fetches when source signals change. A caller who needs reactive refetching but only encounters `Resource::new` in the prelude can reach for the wrong one — the mistake compiles and runs, the resource simply never re-fetches. Adding `create_resource` to the prelude alongside `Resource` closes the discovery gap.

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:112` and `crates/ferric/src/async_resource.rs:133`
  **description**: `create_resource` documents its native / WASM split in its docstring ("# WASM gate") and enforces it with `#[cfg(target_arch = "wasm32")]` / `#[cfg(not(target_arch = "wasm32"))]` blocks (lines 234–247). `Resource::new` and `Resource::new_fallible` call `spawn_local` without any cfg gate and with no equivalent docstring note. On a native target the future is not driven and the resource stays in `Loading` permanently, but nothing in the API surface tells a caller this. The inconsistency is sharpest for a caller who reads `create_resource`'s WASM-gate note, infers that `Resource::new` behaves the same, and is then surprised when their native unit test for a `Resource::new`-based resource never resolves. Adding a "# WASM" section matching `create_resource`'s to both methods makes the platform dependency visible at the API boundary.

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/form.rs:175`
  **description**: `on_input_handler()` returns a handler that reads the internal `input_buf` signal when fired. The docstring says in bold: "Call `set_input` with the new value before invoking the handler." If that call is omitted, the handler fires and writes whatever value is currently in `input_buf` — which starts at `Bind::new` time as the field's initial raw value — with no error raised. The two-method split (`on_input_handler` for testable native use, `on_input_event_handler` for WASM DOM-direct use) is a deliberate and documented testability trade-off. The issue is that the temporal ordering precondition is not type-enforced; silent stale-write is the failure mode. The docstring names this clearly enough for a careful reader, but the method signature gives no hint. A note in the companion rendering code that calls `set_input` before dispatching the handler would reduce the chance of a stale write going unnoticed.

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/vdom.rs:317` and `crates/ferric/src/form.rs:175`
  **description**: `VElement::on(kind, impl Fn() + 'static)` and `VElement::on_with_event(kind, impl Fn(&dyn Any) + 'static)` take closures. `Bind::on_input_handler()` and `Bind::on_input_event_handler()` return `EventHandler` values. There is no `VElement` builder method of the form `with_handler(kind, EventHandler) -> Self`. To attach a `Bind`-produced handler to a `VElement`, a caller must push directly to the public `events` field (`el.events.push((EventKind::Input, bind.on_input_handler()))`), bypassing the builder pattern entirely. For a first-time caller assembling a form component, the absence of a bridge method is unexpected: the builder API feels complete until they try to use a `Bind`. Adding a `VElement::with_handler(kind: EventKind, handler: EventHandler) -> Self` method would make the two subsystems composable through the same builder surface.

- **severity**: non-blocker
  **concern**: tests
  **location**: `crates/ferric/src/form.rs:220`
  **description**: The doc comment for `on_input_event_handler` explicitly names two fail-silent
  paths: "If any step fails (target absent, or the target is not an `<input>` element), the
  closure returns without updating the signal — no panic." Neither path has a test. The WASM
  test at line 488 covers the happy path only. A bug in either branch — for example, panicking
  instead of returning silently, or writing a stale value — would go undetected. These are
  documented behavioral contracts, not implementation details. Satisfying condition: two focused
  WASM tests, each constructing a `WithEvent` handler and passing (a) an event with no target
  and (b) an event whose target is a non-input element, asserting in both cases that the signal
  value did not change.

- **severity**: non-blocker
  **concern**: idiom
  **location**: `crates/ferric/src/dom.rs:287`
  **description**: `closure.forget()` in the production `set_events()` function has no inline comment at the call site. The lifecycle is managed: the closure reference is stashed on the DOM element via `Reflect::set` at lines 282–286 (under `stash_key(kind)`), and the cleanup path at lines 215–263 retrieves that stash key to call `remove_event_listener_with_callback` before rebinding. This is not a leak. However, a reader encounters the `forget()` after a comment about stashing and must connect those two code regions to confirm cleanup will occur. The analogous test-side `closure.forget()` at `form.rs:515` carries an explicit inline comment explaining why the forget is bounded. Adding a note at the call site — such as `// Ownership transferred to JS: the browser holds the closure via the event listener; the stash slot above provides the reference for future detachment.` — would make the lifecycle self-evident without requiring the reader to follow the cleanup path. Readability observation, not a correctness issue.

- **severity**: non-blocker
  **concern**: api-stability
  **location**: `crates/ferric/src/lib.rs:40–41`
  **description**: `Bind` and `FormField` are added to `ferric::prelude`, but `Bind::on_input_handler()` returns `EventHandler`, which is not in the prelude. Callers using `use ferric::prelude::*` who call `bind.on_input_handler()` receive a value of a type they cannot name without an additional `use ferric::vdom::EventHandler` import. This is a usability gap, not a correctness break. Satisfying condition: add `pub use crate::vdom::EventHandler;` to the prelude block in `lib.rs`.

- **severity**: non-blocker
  **concern**: api-stability
  **location**: `crates/ferric/src/async_resource.rs:1`
  **description**: `ResourceState<T>` and `EventHandler` are both public enums with no `#[non_exhaustive]` attribute. Any caller writing an exhaustive `match` on either type will get a compile error if a new variant is added in a future minor version. `ResourceState` is intended to be matched by callers (the `suspense` primitive is built around reading it); adding a fourth state (e.g., `Cancelled` or `Stale`) would be a major version break without the guard. The library is pre-1.0, so the immediate semver cost is bounded — this is a forward-proofing gap, not an active break. Satisfying condition: add `#[non_exhaustive]` to both enums. (Distinct from #196, which concerns variant naming, not the exhaustiveness guard.)

<!-- ============================================================ -->
<!-- CLEAN VERIFICATIONS (23)                                     -->
<!-- ============================================================ -->

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/vdom.rs:31-33`
  **description**: The import block of `vdom.rs` is `use std::collections::{BTreeMap, HashSet}; use std::fmt; use std::rc::Rc;`. No `web_sys` import is present — not as a `use` path, not as a qualified `web_sys::` type in any type or expression position. The `web_sys::Event` name appears only in doc comments as usage guidance for callers. The `EventKind` expansion and the `EventHandler` type change from type alias to enum are view-representation changes consistent with the vdom layer's responsibility. `BTreeSet<EventKind>` → `HashSet<EventKind>` in the test shadow struct follows naturally from removing `Ord` (which requires `Copy`, which `Custom(String)` prevents). The module's responsibility boundary — virtual DOM representation, pure keyed diff algorithm, event binding type definitions — is intact. Checked from Q1 (module coupling) and Q2 (EventHandler boundary).

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/dom.rs`
  **description**: The import line in `dom.rs` is `use crate::vdom::{diff, EventHandler, EventKind, Patch, VNode};`. No `async_resource`, no `form`. The module correctly fulfills its bridge role: it receives type-erased `&dyn Any` from vdom, materialises a real `web_sys::Event`, and dispatches it. The concrete DOM coupling is fully contained in this module. No cross-layer leakage outward.

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/form.rs`
  **description**: `form.rs` imports `crate::signal::{create_signal, Signal}` and `crate::vdom::EventHandler`. No import from `async_resource`. `web_sys` types (`Event`, `HtmlInputElement`) appear only inside `#[cfg(target_arch = "wasm32")]`. The buffer-based `on_input_handler()` path is fully native, enabling all 18 `#[cfg(test)]` tests to run without a WASM target. The `#[cfg]` split is a deliberate testability design whose rationale is documented in the `Bind` doc comment under "Testability — approach 2 (WASM-free)." Responsibility boundary: `form.rs` owns form-state types and produces view-layer wiring descriptors without crossing into resource lifecycle or concrete DOM dispatch.

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/vdom.rs` (~lines 193–200)
  **description**: The two-variant `EventHandler` enum models the actual use-case split cleanly. `NoArg(Rc<dyn Fn()>)` covers the common case where the handler updates signals and needs no event details. `WithEvent(Rc<dyn Fn(&dyn std::any::Any)>)` covers the cases that need the DOM event — `prevent_default()`, reading input value, keyboard key codes — via type erasure. The names are precise. The `#[allow(clippy::type_complexity)]` on the enum is appropriate; the type is readable as written. The design correctly avoids a third variant that would require `vdom.rs` to know specific `web_sys` event subtypes.

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/dom.rs` (set_events, ~lines 272–275)
  **description**: The dispatch closure matches exhaustively over both `EventHandler` variants with no wildcard arm — the compiler guarantees every case is handled. The upcast `&event as &dyn std::any::Any` is correct: `web_sys::Event` is `'static` and implements `Any`. The dom.rs WASM test confirms the `WithEvent` → downcast → `prevent_default()` round-trip. No unreachable arms, no missing arms.

- **severity**: clean
  **concern**: code-quality
  **location**: `structural`
  **description**: The EventHandler abstraction boundary is navigable for future contributors. A new handler variant belongs in `vdom.rs` (`EventHandler` enum) and the dispatch match in `dom.rs` `set_events` will produce a compiler error until the new arm is added. A new event kind belongs in `vdom.rs` (`EventKind` enum), and the exhaustive matches in `event_name` and `stash_key` in `dom.rs` produce compiler errors until they are updated. Both directions have compiler-enforced update paths — except for `static_event_kinds()` (see issue #198). The module-level doc comment in `dom.rs` correctly places all web_sys responsibilities in that module.

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:226-229`
  **description**: The increment site comment at lines 226–227 reads: "Bump the generation so any in-flight future from the previous source value will see a stale generation and discard its result (REQ-ASYNC-016)." The comment names what the increment does, what it causes in concurrent futures, and references the requirement. A reader catching a bug in this path would know immediately what the counter protects without reading beyond this block. This is a why-not-what comment that makes state-mutation sites self-explanatory.

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:239-240`
  **description**: The comparison guard comment at line 239 reads: "Only write if our generation is still the latest (no newer fetch started)." The guard condition is stated in terms of behavior (a newer fetch) rather than mechanics (integer equality). `next_gen` is a captured `u64` and `gen_check.get()` is the shared counter's current value; both are single-purpose enough that the comment closes any remaining gap.

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:217-240`
  **description**: The generation counter is `Rc<Cell<u64>>`. `u64` is not idiomatic for a length or loop variable (those would be `usize`), and the `Rc<Cell<_>>` wrapper signals shared mutable state rather than a simple accumulator. The read-snapshot-compare pattern (`gen.get() + 1 → gen.set(next_gen); ... gen_check.get() == next_gen`) is the canonical optimistic-concurrency generation check; a reader familiar with concurrent Rust patterns will recognise it immediately. No extra abstraction layer is missing or needed.

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:217`
  **description**: `gen` does not resemble a loop variable (`i`, `j`) or a size variable (`len`, `count`). The name is terse but established for the generation-counter pattern. The `Rc` and `Cell` wrappers in the type make the shared-mutable-integer semantics explicit even without a comment. `gen_check` (line 236, the clone moved into the async block) names the clone's use rather than its nature; the guard at line 239 makes the purpose clear three lines later.

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:58`
  **description**: `ResourceState<T>` is a three-variant enum (`Loading`, `Ready(T)`, `Failed(String)`) with no default variant. Any `match` on a `ResourceState` must cover all three variants or the code does not compile. The docstring explicitly calls this property out ("Exhaustively matchable — callers cannot receive a Ready before the future has resolved"). The variant names model the lifecycle correctly. The type encoding prevents the caller from ever accessing a `T` before the future has resolved because `T` is only present inside the `Ready` variant.

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/form.rs:89`
  **description**: `FormField::parsed()` calls `raw.get().parse::<T>().map_err(|e| e.to_string())` and returns the result. The caller is forced to handle `Err` at the type level. Combined with the `FromStr + 'static` bound on `T`, the type system prevents a caller from obtaining a `T` from the field without explicitly checking the parse result. The raw string is preserved and exposed via `raw()` for validation feedback. The docstring is explicit: "The caller must handle the error; no silent coercion or default is applied." This is a well-constructed pit of success for form handling.

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/form.rs:216`
  **description**: `#[cfg(target_arch = "wasm32")]` on `on_input_event_handler` means the method does not exist on native targets. A caller writing cross-platform code that accidentally references this method gets a compile error rather than a runtime panic. The companion method `on_input_handler` with `set_input` is available on all targets. The cfg gate cleanly enforces the design intent: DOM-reading code belongs to the WASM layer; testable buffer-based code is universally available.

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/vdom.rs:317` and `crates/ferric/src/vdom.rs:329`
  **description**: For a component author attaching event handlers, there are two clearly named builder methods: `on(kind, closure)` for no-argument handlers and `on_with_event(kind, closure)` for handlers that receive the DOM event. The name distinction communicates the difference. If you need `prevent_default()` or any event property, you use `on_with_event`; otherwise `on`. The dom.rs WASM test (`event_carrying_handler_can_call_prevent_default`) confirms the `on_with_event` → downcast → `prevent_default()` path works end-to-end. (Note: the gap for attaching `Bind`-produced `EventHandler` values is recorded as non-blocker above.)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/dom.rs:376` and `crates/ferric/src/dom.rs:447`
  **description**: `event_name()` and `stash_key()` both use exhaustive `match` with no wildcard. The dom.rs doc comment notes this explicitly: "The `match` is exhaustive — no wildcard — so the compiler reports an error if a new variant is added to the enum without updating this table." If a future change adds a variant to `EventKind`, both functions are compile-time errors until the new variant is handled. This directly encodes a correctness invariant in the type system: the DOM event name and stash key tables cannot fall out of sync with the enum without a build failure.

- **severity**: clean
  **concern**: tests
  **location**: `crates/ferric/src/form.rs:488`
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
  **location**: `crates/ferric/src/dom.rs:630`
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
  **location**: `crates/ferric/src/dom.rs:595`
  **description**: Checked REQ-ASYNC-023 acceptance criteria coverage. The requirement is that a
  `WithEvent` handler can call `prevent_default()` on the DOM event and have the cancellation
  take effect. The WASM test at line 630 covers this directly with a behavioral assertion. No
  gap in stated-requirement coverage was found beyond what is reported above.

- **severity**: clean
  **concern**: idiom
  **location**: `crates/ferric/src/form.rs:515`
  **description**: `closure.forget()` in the WASM integration test is commented at lines 513–514: `// 'forget()' is acceptable in a test: the closure has test scope and the element is removed at the end of the test.` This names the reason and the bounding condition. The DOM element is removed at line 529, which eliminates the browser's event-listener reference. The pattern is standard wasm-bindgen practice for closures whose lifetime is managed by the browser within a bounded test scope.

- **severity**: clean
  **concern**: idiom
  **location**: `crates/ferric/src/async_resource.rs:634`
  **description**: `resource.signal.set(ResourceState::Ready(99))` and the similar calls at lines 662 and 667 access the private `signal` field of `Resource<T>`. Rust's module visibility rules allow child modules (`mod tests`) to read and write private fields of types defined in the parent module — this is correct. The comment at lines 632–633 (`// (The 'signal' field is accessible here because this test lives in the same file.)`) correctly states this. The pattern is consistent with the rest of the test module. A `#[cfg(test)] fn force_ready(...)` helper would add an indirection layer without readability benefit for two tests in the same file; direct field access in same-file test modules is the established pattern here.

- **severity**: clean
  **concern**: idiom
  **location**: `structural`
  **description**: Scanned `async_resource.rs`, `form.rs`, `dom.rs`, and `vdom.rs` for `unsafe` blocks. None were found in any of the four files. `dom.rs` uses wasm-bindgen's `unchecked_ref::<js_sys::Function>()` and `unchecked_into()` in WASM-gated production code at lines 255 and 276; these are safe functions in Rust's type system and are applied to values the framework placed there itself. No `unsafe {}` blocks were introduced by this PR.

- **severity**: clean
  **concern**: idiom
  **location**: `structural`
  **description**: Checked `unwrap()` usage in production code paths (non-`#[cfg(test)]`) across all four files. No bare `unwrap()` calls appear in production paths. `form.rs`'s `on_input_event_handler()` uses `if let` chains that silently no-op on a missing or mistyped event target — appropriate for DOM event handling. `dom.rs`'s `set_events()` uses `.expect("set_events: add_event_listener failed")` for the event-listener registration — an appropriate choice for a condition that indicates a programming error (calling on a valid element), not a user-input error path. `async_resource.rs` production code handles both `Ok` and `Err` variants explicitly in `new_fallible()`. `unwrap()` appears freely in test code, which is acceptable.

- **severity**: clean
  **concern**: idiom
  **location**: `structural`
  **description**: Checked `.clone()` calls in production code paths across all four files. All are structurally required: `dom.rs:271` clones `EventHandler` (which wraps `Rc<dyn Fn...>`) to move it into a `move` closure — this is an Rc refcount increment, not a deep copy; `dom.rs:290` clones a `String` from an iterator reference to push into a `Vec<String>`; `dom.rs:437` clones the contained `String` from `EventKind::Custom(s)` where the return type requires an owned value; `async_resource.rs:71–72` clones the payload in the `Clone` impl for `ResourceState<T>`, which is the correct implementation. `vdom.rs` clone calls in the diff/patch paths are inherent to a structural VDOM diff algorithm. No unnecessary copies appear in production paths.

- **severity**: clean
  **concern**: api-stability
  **location**: `crates/ferric/src/vdom.rs:62`
  **description**: `VElement::on()` backward compatibility checked. The method signature (`impl Fn() + 'static`) is unchanged from before this PR. The `EventHandler::NoArg` wrapping is an internal detail invisible to callers; any pre-PR usage of `element.on(kind, closure)` continues to compile without modification.

- **severity**: clean
  **concern**: api-stability
  **location**: `crates/ferric/src/lib.rs:38`
  **description**: `EventHandler` type alias → enum change checked against the prelude surface. `EventHandler` is not re-exported from `ferric::prelude` before or after this PR; `EventKind`, `VElement`, and `VNode` remain the vdom prelude surface. The flat non-prelude re-export also excludes `EventHandler`. Callers using `use ferric::prelude::*` are unaffected by this change.

- **severity**: clean
  **concern**: api-stability
  **location**: `crates/ferric/src/form.rs:197–259`
  **description**: `on_input_event_handler()` on `Bind<T>` checked. The method is correctly gated to `#[cfg(target_arch = "wasm32")]`. Documentation covers the four-step behavior description, the failure mode (silent no-op if `target()` is absent or the target is not `<input>`), the reason for the `wasm32` gate, and cross-links to `on_input_handler` and `set_input`. The companion WASM integration test (`on_input_event_handler_updates_signal_from_dom_value`) exercises the full DOM → signal path with a real inserted element and a dispatched synthetic event, covering REQ-ASYNC-042. Documentation and coverage are adequate.

- **severity**: clean
  **concern**: api-stability
  **location**: `crates/ferric/src/async_resource.rs`
  **description**: `create_resource` naming convention checked. The function follows the library's established `create_*` pattern: `create_signal`, `create_effect`, `create_memo`, `create_resource`. The function takes a reactive source closure and a fetcher closure, consistent with the pattern used in this space. No naming convention deviation found.

---

## What was examined

**Concern 2 — Code quality and design**

- `crates/ferric/src/async_resource.rs` — full file (832 lines)
  - Import list; module-level doc comment; `suspense()` colocation (~lines 1–50)
  - `ResourceState<T>` enum definition (line 58); `Resource<T>` struct (line 65)
  - `create_resource` function: docstring, `# Cancellation (REQ-ASYNC-016)` section, cfg branches (~lines 186–247)
  - Generation counter: declaration (line 217), increment (lines 226–229), clone (line 236), comparison guard (lines 239–241)
  - `Resource::new`, `Resource::new_fallible` (lines 112, 133) — WASM gate note presence
  - `lib.rs:40–51` — prelude exports (Resource, ResourceState, create_resource)
  - Sub-questions addressed: [x] Q1 coupling, [x] Q2 EventHandler boundary, [x] Q3 generation counter, [x] Q4 correct-use design

- `crates/ferric/src/vdom.rs` — full change section
  - Import block (lines 31–33) — web_sys absence verified
  - `EventHandler` enum definition (~lines 193–200) and builder methods `on`, `on_with_event` (lines 317, 329)
  - `diff_events` and `event_kinds` helpers; test module

- `crates/ferric/src/dom.rs` — full change section
  - Import line — scope verification
  - `set_events` dispatch closure (~lines 272–275) — exhaustive match, Any upcast
  - `static_event_kinds()` array; `event_name()` (line 376), `stash_key()` (line 447) — exhaustive matches
  - WASM test for `WithEvent` downcast path (line 630)

- `crates/ferric/src/form.rs` — full file (531 lines)
  - Import list; `FormField<T>` struct (line 89); `Bind<T>` struct
  - `on_input_handler()` (line 175), `on_input_event_handler()` (line 216)
  - 18 native `#[cfg(test)]` tests for `Bind`

- `crates/ferric/src/lib.rs` — prelude additions (lines 40–51)
- `crates/ferric/Cargo.toml` — dependency additions (scope verification)
- `crates/ferric/src/component.rs` — handler invocation change (EventHandler transition)

**Concern 3 — Test coverage and depth**

- `crates/ferric/src/async_resource.rs` (full file, 833 lines, commit 838239e)
  - Generation counter implementation (`#[cfg(target_arch = "wasm32")]` / `drop(fut)` branches)
  - Native `mod tests` block (line 320): `create_resource_source_change_resets_to_loading` (line 618) and `create_resource_two_source_changes_stay_loading` (line 655) including doc comment stale-overwrite claim
  - WASM `mod wasm_tests` block (line 722): `create_resource_refetches_on_source_change` (line 778) — test structure analyzed for sequential vs. concurrent coverage
  - Sub-questions addressed: [x] Q1 native in-flight source change tests (blocker found), [x] Q2 REQ-ASYNC-042 WASM test depth (clean), [x] Q3 prevent_default test for REQ-ASYNC-023 (clean), [x] Q4 acceptance criteria without test coverage (non-blocker found for REQ-ASYNC-042 fail-silent paths)

- `crates/ferric/src/form.rs` (full file, commit 838239e)
  - `on_input_event_handler` implementation and doc comment (fail-silent paths, line 220)
  - `Bind::on_input_handler` (buffer-based approach) and all native tests for `Bind`
  - WASM `mod wasm_tests` (line 466): `on_input_event_handler_updates_signal_from_dom_value` (line 488) — analyzed for real DOM attachment, genuine event dispatch, signal assertion, and DOM cleanup

- `crates/ferric/src/dom.rs` (full file, commit 838239e)
  - WASM `mod wasm_tests` (line 595): `event_carrying_handler_can_call_prevent_default` (line 630) — analyzed for pre-condition assertion, `default_prevented()` post-assertion, REQ-ASYNC-023 behavioral contract coverage
  - `mount_renders_initial_view_and_reacts_to_signal_change` — complementary event-binding path coverage

**Concern 6 — Rust language idiom**

- `crates/ferric/src/form.rs` — full file (531 lines)
  - Production code: `FormField<T>`, `Bind<T>`, `on_input_event_handler()` (~lines 1–228)
  - Native test module: `mod tests` (~lines 230–455)
  - WASM integration test block (~lines 457–531); `closure.forget()` at line 515 and inline comment at lines 513–514
  - `unwrap()` scan in production: none found; `.clone()` scan in production: none found
  - Sub-questions addressed: [x] closure.forget() bounded lifetime, [x] private field access validity, [x] unsafe blocks, [x] unwrap() in production, [x] unnecessary .clone(), [x] production memory leaks

- `crates/ferric/src/async_resource.rs` — full file (832 lines)
  - Production code (~lines 1–315); native test module (~lines 316–end)
  - `resource.signal.set(...)` calls at lines 634, 662, 667 and surrounding context
  - `unsafe` scan: none found; `unwrap()` scan in production: none found; `.clone()` in production: `ResourceState::Clone` impl at lines 71–72 (necessary)

- `crates/ferric/src/dom.rs` — production and test sections
  - `set_events()` production function (~lines 215–302): `closure.forget()` at line 287, stash logic at lines 282–286, cleanup loop at lines 215–263
  - `event_name()` helper (~lines 390–439): `s.clone()` at line 437
  - `unsafe` scan: none found (only `unchecked_ref`, `unchecked_into` — not `unsafe` blocks)
  - `unwrap()` scan in production: none found; `.expect()` with message at line 280
  - WASM test block (~lines 605–621): `unwrap()` and `.clone()` acceptable in test context

- `crates/ferric/src/vdom.rs` — production and test sections
  - `unsafe` scan: none found; `.clone()` scan: all production clones in VDOM diff/patch paths where structural copies are required; `unwrap()`: only in test code (line 761)

**Concern 7 — API and contract stability**

- `crates/ferric/src/vdom.rs` — `EventHandler` definition and `VElement::on()` implementation; on() signature verified unchanged from pre-PR
- `crates/ferric/src/lib.rs` — full diff; all flat `pub use` and `prelude` exports enumerated; EventHandler pre/post-PR export status verified
- `crates/ferric/src/form.rs` — full file (531 lines); `on_input_event_handler()` implementation, doc comment, cfg gate; WASM integration test block
- `crates/ferric/src/async_resource.rs` — public API surface: `ResourceState<T>`, `Resource<T>`, `create_resource`, `suspense`; naming compared to `create_signal`, `create_effect`, `create_memo`
- Previously filed issues #196–#201 — confirmed non-overlap: #196 ResourceState::Failed naming, #197 workspace dep, #198 static_event_kinds sync, #199 lifecycle teardown tests, #200 test name, #201 KeyPress deprecation
  - Sub-questions addressed: [x] Q1 EventHandler backward compat (clean), [x] Q2 on_input_event_handler documentation (clean), [x] Q3 create_resource naming (clean)
