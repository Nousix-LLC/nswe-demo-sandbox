# Concern 2 — Code Quality: Partial Findings

PR #193 (`feat(ferric): async resources, expanded events, and form binding`)  
Merged from: Q1 (responsibility/coupling), Q2 (EventHandler boundary), Q3 (generation counter), Q4 (correct-use design)

---

## Findings

<!-- Non-blockers (8 total; no blockers present) -->

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:14`
  **description**: `suspense()` is colocated in `async_resource.rs` because it reads `SUSPENSE_DEPTH` and `SUSPENSE_HAS_LOADING`, two thread-local sentinels that `create_resource` increments and sets during reactive re-runs. The colocation avoids leaking those private sentinels across a module boundary — a coherent and defensible choice. What is missing is documentation: the module's doc header does not explain that `suspense()` lives here rather than in a view-layer module. A reader arriving at `async_resource.rs` expecting only resource lifecycle machinery will find `suspense()` unexplained. A module-level doc note stating that `suspense()` resides here because of its dependency on the loading sentinels would make the boundary legible without restructuring. (Q1 source: Finding 1)

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `structural`
  **description**: The intra-crate dependency graph for the four modules is: `signal` (leaf) → `vdom` → `async_resource` (signal + vdom) / `dom` (vdom only) / `form` (signal + vdom). `async_resource` sits at the same conceptual level as `form` but adds a dependency on `vdom` — a sideways dependency that is mechanically necessary (see the note on `suspense()` colocation above). No cycles exist and no DOM-layer coupling leaks into application-layer modules. The dependency graph is structurally acceptable; the absence of cycles and the clean DOM isolation are what matter. (Q1 source: Finding 5)

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/dom.rs` (static_event_kinds function)
  **description**: `event_name()` and `stash_key()` use exhaustive `match` expressions over `EventKind` — adding a new static variant without updating those functions is a compiler error. The detachment pass in `set_events` iterates `static_event_kinds()`, which is a manually-counted `[EventKind; 47]` array literal. If a contributor adds a new static variant, updates the exhaustive matches (compiler-forced), but forgets to add the variant to `static_event_kinds()` and increment the return-type annotation, the code compiles cleanly. The new variant's stash slot is never purged on a re-bind, so the previous closure leaks and the event fires twice. The array is currently correct (47 matches the non-`Custom` variant count). What would satisfy: add a unit test that verifies the array count matches the enum's non-`Custom` variant count, or at minimum update the comment to call out explicitly that the array length annotation must be incremented when adding a variant. (Q2 source: Finding 4)

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:217`
  **description**: `let gen = Rc::new(Cell::new(0u64));` at line 217 carries no inline comment. The function docstring's `# Cancellation (REQ-ASYNC-016)` section explains the counter at the function level, and the increment comment at lines 226–227 explains it at the mutation site. Neither is visible from the declaration line without scrolling. A reader navigating to line 217 via "Go to definition" from the comparison guard hits the declaration without immediate context. A brief inline comment — e.g., `// generation counter: captures current gen in spawned future, discard if superseded` — would make the invariant legible at first contact. The existing docstring and increment-site comment already contain accurate prose; this gap is one of locality rather than missing information. (Q3 source: Q3.1)

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/lib.rs:41` and `crates/ferric/src/async_resource.rs:207`
  **description**: `ferric::prelude` exports `Resource` and `ResourceState` but not `create_resource`. A caller using `use ferric::prelude::*` sees `Resource::new` as the natural construction path; `create_resource` is reachable only via the full module path `ferric::async_resource::create_resource`. The two functions serve different needs: `Resource::new` starts a one-shot future with no reactive re-triggering; `create_resource` wraps the future in a reactive effect and re-fetches when source signals change. A caller who needs reactive refetching but only encounters `Resource::new` in the prelude can reach for the wrong one — the mistake compiles and runs, the resource simply never re-fetches. Adding `create_resource` to the prelude alongside `Resource` closes the discovery gap. (Q4 source: NB-1)

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:112` and `crates/ferric/src/async_resource.rs:133`
  **description**: `create_resource` documents its native / WASM split in its docstring ("# WASM gate") and enforces it with `#[cfg(target_arch = "wasm32")]` / `#[cfg(not(target_arch = "wasm32"))]` blocks (lines 234–247). `Resource::new` and `Resource::new_fallible` call `spawn_local` without any cfg gate and with no equivalent docstring note. On a native target the future is not driven and the resource stays in `Loading` permanently, but nothing in the API surface tells a caller this. The inconsistency is sharpest for a caller who reads `create_resource`'s WASM-gate note, infers that `Resource::new` behaves the same, and is then surprised when their native unit test for a `Resource::new`-based resource never resolves. Adding a "# WASM" section matching `create_resource`'s to both methods makes the platform dependency visible at the API boundary. (Q4 source: NB-2)

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/form.rs:175`
  **description**: `on_input_handler()` returns a handler that reads the internal `input_buf` signal when fired. The docstring says in bold: "Call `set_input` with the new value before invoking the handler." If that call is omitted, the handler fires and writes whatever value is currently in `input_buf` — which starts at `Bind::new` time as the field's initial raw value — with no error raised. The two-method split (`on_input_handler` for testable native use, `on_input_event_handler` for WASM DOM-direct use) is a deliberate and documented testability trade-off. The issue is that the temporal ordering precondition is not type-enforced; silent stale-write is the failure mode. The docstring names this clearly enough for a careful reader, but the method signature gives no hint. A note in the companion rendering code that calls `set_input` before dispatching the handler would reduce the chance of a stale write going unnoticed. (Q4 source: NB-3)

- **severity**: non-blocker
  **concern**: code-quality
  **location**: `crates/ferric/src/vdom.rs:317` and `crates/ferric/src/form.rs:175`
  **description**: `VElement::on(kind, impl Fn() + 'static)` and `VElement::on_with_event(kind, impl Fn(&dyn Any) + 'static)` take closures. `Bind::on_input_handler()` and `Bind::on_input_event_handler()` return `EventHandler` values. There is no `VElement` builder method of the form `with_handler(kind, EventHandler) -> Self`. To attach a `Bind`-produced handler to a `VElement`, a caller must push directly to the public `events` field (`el.events.push((EventKind::Input, bind.on_input_handler()))`), bypassing the builder pattern entirely. For a first-time caller assembling a form component, the absence of a bridge method is unexpected: the builder API feels complete until they try to use a `Bind`. Adding a `VElement::with_handler(kind: EventKind, handler: EventHandler) -> Self` method would make the two subsystems composable through the same builder surface. (Q4 source: NB-4)

<!-- Clean verifications (15 total) -->

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/vdom.rs:31-33`
  **description**: The import block of `vdom.rs` is `use std::collections::{BTreeMap, HashSet}; use std::fmt; use std::rc::Rc;`. No `web_sys` import is present — not as a `use` path, not as a qualified `web_sys::` type in any type or expression position. The `web_sys::Event` name appears only in doc comments as usage guidance for callers. The `EventKind` expansion and the `EventHandler` type change from type alias to enum are view-representation changes consistent with the vdom layer's responsibility. `BTreeSet<EventKind>` → `HashSet<EventKind>` in the test shadow struct follows naturally from removing `Ord` (which requires `Copy`, which `Custom(String)` prevents). The module's responsibility boundary — virtual DOM representation, pure keyed diff algorithm, event binding type definitions — is intact. Checked from Q1 (module coupling) and Q2 (EventHandler boundary). (Q1 F2 / Q2 F1 merged)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/dom.rs`
  **description**: The import line in `dom.rs` is `use crate::vdom::{diff, EventHandler, EventKind, Patch, VNode};`. No `async_resource`, no `form`. The module correctly fulfills its bridge role: it receives type-erased `&dyn Any` from vdom, materialises a real `web_sys::Event`, and dispatches it. The concrete DOM coupling is fully contained in this module. No cross-layer leakage outward. (Q1 source: Finding 3)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/form.rs`
  **description**: `form.rs` imports `crate::signal::{create_signal, Signal}` and `crate::vdom::EventHandler`. No import from `async_resource`. `web_sys` types (`Event`, `HtmlInputElement`) appear only inside `#[cfg(target_arch = "wasm32")]`. The buffer-based `on_input_handler()` path is fully native, enabling all 18 `#[cfg(test)]` tests to run without a WASM target. The `#[cfg]` split is a deliberate testability design whose rationale is documented in the `Bind` doc comment under "Testability — approach 2 (WASM-free)." Responsibility boundary: `form.rs` owns form-state types and produces view-layer wiring descriptors without crossing into resource lifecycle or concrete DOM dispatch. (Q1 source: Finding 4)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/vdom.rs` (~lines 193–200)
  **description**: The two-variant `EventHandler` enum models the actual use-case split cleanly. `NoArg(Rc<dyn Fn()>)` covers the common case where the handler updates signals and needs no event details. `WithEvent(Rc<dyn Fn(&dyn std::any::Any)>)` covers the cases that need the DOM event — `prevent_default()`, reading input value, keyboard key codes — via type erasure. The names are precise. The `#[allow(clippy::type_complexity)]` on the enum is appropriate; the type is readable as written. The design correctly avoids a third variant that would require `vdom.rs` to know specific `web_sys` event subtypes. (Q2 source: Finding 2)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/dom.rs` (set_events, ~line 272–275)
  **description**: The dispatch closure matches exhaustively over both `EventHandler` variants with no wildcard arm — the compiler guarantees every case is handled. The upcast `&event as &dyn std::any::Any` is correct: `web_sys::Event` is `'static` and implements `Any`. The dom.rs WASM test confirms the `WithEvent` → downcast → `prevent_default()` round-trip. No unreachable arms, no missing arms. (Q2 source: Finding 3)

- **severity**: clean
  **concern**: code-quality
  **location**: `structural`
  **description**: The EventHandler abstraction boundary is navigable for future contributors. A new handler variant belongs in `vdom.rs` (`EventHandler` enum) and the dispatch match in `dom.rs` `set_events` will produce a compiler error until the new arm is added. A new event kind belongs in `vdom.rs` (`EventKind` enum), and the exhaustive matches in `event_name` and `stash_key` in `dom.rs` produce compiler errors until they are updated. Both directions have compiler-enforced update paths — except for `static_event_kinds()` (see non-blocker above). The module-level doc comment in `dom.rs` correctly places all web_sys responsibilities in that module. (Q2 source: Finding 5)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:226-229`
  **description**: The increment site comment at lines 226–227 reads: "Bump the generation so any in-flight future from the previous source value will see a stale generation and discard its result (REQ-ASYNC-016)." The comment names what the increment does, what it causes in concurrent futures, and references the requirement. A reader catching a bug in this path would know immediately what the counter protects without reading beyond this block. This is a why-not-what comment that makes state-mutation sites self-explanatory. (Q3 source: Q3.2)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:239-240`
  **description**: The comparison guard comment at line 239 reads: "Only write if our generation is still the latest (no newer fetch started)." The guard condition is stated in terms of behavior (a newer fetch) rather than mechanics (integer equality). `next_gen` is a captured `u64` and `gen_check.get()` is the shared counter's current value; both are single-purpose enough that the comment closes any remaining gap. (Q3 source: Q3.3)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:217-240`
  **description**: The generation counter is `Rc<Cell<u64>>`. `u64` is not idiomatic for a length or loop variable (those would be `usize`), and the `Rc<Cell<_>>` wrapper signals shared mutable state rather than a simple accumulator. The read-snapshot-compare pattern (`gen.get() + 1 → gen.set(next_gen); ... gen_check.get() == next_gen`) is the canonical optimistic-concurrency generation check; a reader familiar with concurrent Rust patterns will recognise it immediately. No extra abstraction layer is missing or needed. (Q3 source: Q3.4)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:217`
  **description**: `gen` does not resemble a loop variable (`i`, `j`) or a size variable (`len`, `count`). The name is terse but established for the generation-counter pattern. The `Rc` and `Cell` wrappers in the type make the shared-mutable-integer semantics explicit even without a comment. `gen_check` (line 236, the clone moved into the async block) names the clone's use rather than its nature; the guard at line 239 makes the purpose clear three lines later. (Q3 source: Q3.5)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/async_resource.rs:58`
  **description**: `ResourceState<T>` is a three-variant enum (`Loading`, `Ready(T)`, `Failed(String)`) with no `#[non_exhaustive]` attribute and no default variant. Any `match` on a `ResourceState` must cover all three variants or the code does not compile. The docstring explicitly calls this property out ("Exhaustively matchable — callers cannot receive a Ready before the future has resolved"). The variant names model the lifecycle correctly. The type encoding prevents the caller from ever accessing a `T` before the future has resolved because `T` is only present inside the `Ready` variant. (Q4 source: CLEAN-1)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/form.rs:89`
  **description**: `FormField::parsed()` calls `raw.get().parse::<T>().map_err(|e| e.to_string())` and returns the result. The caller is forced to handle `Err` at the type level. Combined with the `FromStr + 'static` bound on `T`, the type system prevents a caller from obtaining a `T` from the field without explicitly checking the parse result. The raw string is preserved and exposed via `raw()` for validation feedback. The docstring is explicit: "The caller must handle the error; no silent coercion or default is applied." This is a well-constructed pit of success for form handling. (Q4 source: CLEAN-2)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/form.rs:216`
  **description**: `#[cfg(target_arch = "wasm32")]` on `on_input_event_handler` means the method does not exist on native targets. A caller writing cross-platform code that accidentally references this method gets a compile error rather than a runtime panic. The companion method `on_input_handler` with `set_input` is available on all targets. The cfg gate cleanly enforces the design intent: DOM-reading code belongs to the WASM layer; testable buffer-based code is universally available. (Q4 source: CLEAN-3)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/vdom.rs:317` and `crates/ferric/src/vdom.rs:329`
  **description**: For a component author attaching event handlers, there are two clearly named builder methods: `on(kind, closure)` for no-argument handlers and `on_with_event(kind, closure)` for handlers that receive the DOM event. The name distinction communicates the difference. If you need `prevent_default()` or any event property, you use `on_with_event`; otherwise `on`. The dom.rs WASM test (`event_carrying_handler_can_call_prevent_default`) confirms the `on_with_event` → downcast → `prevent_default()` path works end-to-end. (Note: the gap for attaching `Bind`-produced `EventHandler` values is recorded as non-blocker NB-4 above.) (Q4 source: CLEAN-4)

- **severity**: clean
  **concern**: code-quality
  **location**: `crates/ferric/src/dom.rs:376` and `crates/ferric/src/dom.rs:447`
  **description**: `event_name()` and `stash_key()` both use exhaustive `match` with no wildcard. The dom.rs doc comment notes this explicitly: "The `match` is exhaustive — no wildcard — so the compiler reports an error if a new variant is added to the enum without updating this table." If a future change adds a variant to `EventKind`, both functions are compile-time errors until the new variant is handled. This directly encodes a correctness invariant in the type system: the DOM event name and stash key tables cannot fall out of sync with the enum without a build failure. (Q4 source: CLEAN-5)

---

## What was examined

**Sub-questions covered:**

- **Q1 — Responsibility partitioning and coupling** (SUBTASK_q1_coupling): Examined import lists and module-level doc comments for `async_resource.rs`, `vdom.rs`, `dom.rs`, and `form.rs`; traced the intra-crate dependency graph across all four files; checked for unexpected cross-layer imports and cycles. Full file contents read via `gh pr diff 193 --repo Nousix-LLC/nswe-demo`.

- **Q2 — EventHandler abstraction boundary** (SUBTASK_q2_eventhandler): Examined `vdom.rs` import block (lines 31–33), `EventHandler` enum definition (~lines 193–200), `on`/`on_with_event` builder methods, `diff_events`/`event_kinds` helpers, and test module; examined `dom.rs` `set_events` dispatch closure, `static_event_kinds` array, and `event_name`/`stash_key` exhaustive matches; examined WASM32 test for `WithEvent` downcast path.

- **Q3 — Generation counter clarity** (SUBTASK_q3_gen_counter): Examined `async_resource.rs` lines 186–193 (`# Cancellation` docstring), line 217 (declaration site), lines 226–229 (increment site), line 236 (clone site), lines 239–241 (comparison guard), and lines 648–668 (counter behavior test).

- **Q4 — Correct-use design** (SUBTASK_q4_correct_use): Examined `form.rs` lines 1–531 (FormField, Bind, on_input_handler, on_input_event_handler, WASM tests); `async_resource.rs` lines 1–313 (module doc, ResourceState, Resource, create_resource, suspense); `vdom.rs` lines 66–352 (EventKind, EventHandler, VElement builders); `dom.rs` lines 229–511 (set_events, static_event_kinds, event_name, stash_key); `lib.rs` lines 40–51 (prelude exports).

**Files examined across all four spokes:**

| File | Examined via |
|------|--------------|
| `crates/ferric/src/async_resource.rs` | Full new-file content (832 lines) — Q1, Q3, Q4 |
| `crates/ferric/src/vdom.rs` | Full change section — Q1, Q2, Q4 |
| `crates/ferric/src/dom.rs` | Full change section — Q1, Q2, Q4 |
| `crates/ferric/src/form.rs` | Full new-file content (531 lines) — Q1, Q4 |
| `crates/ferric/src/lib.rs` | Prelude additions (lines 40–51) — Q4 |
| `crates/ferric/Cargo.toml` | Dependency additions — Q1 (scope verification) |
| `crates/ferric/src/component.rs` | Handler invocation change — Q2 (EventHandler transition) |
