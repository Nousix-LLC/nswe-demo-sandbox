# Q4 Sub-Findings: Correct-Use Design

concern: code-quality  
PR: #193  
Question: Does the design across all four changed files invite correct use and discourage misuse from a caller's perspective?

---

## Findings

### NB-1: `create_resource` absent from the prelude; `Resource::new` is reachable, `create_resource` is not

- **severity**: non-blocker
- **concern**: code-quality
- **location**: `crates/ferric/src/lib.rs:41` and `crates/ferric/src/async_resource.rs:207`

`ferric::prelude` exports `Resource` and `ResourceState` but not `create_resource`. A caller writing `use ferric::prelude::*` sees `Resource::new` as the natural construction path; `create_resource` is reachable only via the full module path `ferric::async_resource::create_resource`. The two functions serve different needs — `Resource::new` starts a one-shot future with no reactive re-triggering; `create_resource` wraps the future in a reactive effect and re-fetches when source signals change. A caller who needs reactive refetching but only sees `Resource::new` in the prelude can plausibly reach for the wrong one. The mistake compiles and runs; the resource just never re-fetches. Adding `create_resource` to the prelude alongside `Resource` closes the discovery gap. As-is, the calling convention for the common case requires a separate `use` import the docs do not prominently point to.

---

### NB-2: `Resource::new` and `Resource::new_fallible` call `spawn_local` without a WASM gate or docstring warning

- **severity**: non-blocker
- **concern**: code-quality
- **location**: `crates/ferric/src/async_resource.rs:112` and `crates/ferric/src/async_resource.rs:133`

`create_resource` documents its native / WASM split in its docstring ("# WASM gate") and enforces it with `#[cfg(target_arch = "wasm32")]` / `#[cfg(not(target_arch = "wasm32"))]` blocks (lines 234–247). `Resource::new` and `Resource::new_fallible` call `spawn_local` without any cfg gate and with no equivalent docstring note. The behavior difference matters: on a native target the future is not driven and the resource stays in `Loading` permanently, but nothing in the API surface — no attribute, no doc section — tells a caller this. The inconsistency is sharpest for a caller who reads `create_resource`'s WASM-gate note, infers that `Resource::new` behaves the same way, and is then surprised when their native unit test for a `Resource::new`-based resource never resolves. Adding a "# WASM" note matching `create_resource`'s to both methods makes the platform dependency visible at the API boundary.

---

### NB-3: `Bind::on_input_handler` buffer-first precondition is not type-enforced; violation writes stale data silently

- **severity**: non-blocker
- **concern**: code-quality
- **location**: `crates/ferric/src/form.rs:175`

`on_input_handler()` returns a handler that reads the internal `input_buf` signal when fired. The docstring says in bold: "Call `set_input` with the new value before invoking the handler (or before the DOM dispatches it)." If that call is omitted, the handler fires and writes whatever value is currently in `input_buf` — which starts at `Bind::new` time as the field's initial raw value. No error is raised; the wrong value is propagated to the field signal. The two-method split (`on_input_handler` for testable native use, `on_input_event_handler` for WASM DOM-direct use) is a deliberate testability trade-off and is explained in both docstrings. The issue is that the precondition on `on_input_handler` is a temporal ordering contract that the type system cannot enforce in stable Rust without a typestate pattern, and silent stale-write on violation is the failure mode. The docstring names this clearly enough for a careful reader, but the method signature gives no hint. A note in the method name or a comment at the call site in the WASM renderer reminding the DOM layer to call `set_input` before dispatch would reduce the chance of a stale write going unnoticed.

---

### NB-4: No `VElement` builder method accepts a pre-built `EventHandler`; `Bind` → `VElement` wiring requires direct field access

- **severity**: non-blocker
- **concern**: code-quality
- **location**: `crates/ferric/src/vdom.rs:317` and `crates/ferric/src/form.rs:175`

`VElement::on(kind, impl Fn() + 'static)` and `VElement::on_with_event(kind, impl Fn(&dyn Any) + 'static)` take closures. `Bind::on_input_handler()` and `Bind::on_input_event_handler()` return `EventHandler` values. There is no `VElement` builder method of the form `with_handler(kind, EventHandler) -> Self`. To attach a `Bind`-produced handler to a `VElement`, a caller must push directly to the public `events` field (`el.events.push((EventKind::Input, bind.on_input_handler()))`), bypassing the builder pattern entirely. This creates two registration paths: the fluent builder for inline closures and the field mutation for pre-built handlers. For a first-time caller assembling a form component, the absence of a bridge method is not fatal but is unexpected: the builder API feels complete until they try to use a `Bind`. Adding a `VElement::with_handler(kind: EventKind, handler: EventHandler) -> Self` method would make the two subsystems composable through the same builder surface.

---

### CLEAN-1: `ResourceState<T>` is exhaustively matchable; callers must handle all three lifecycle states

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/async_resource.rs:58`

`ResourceState<T>` is a three-variant enum with no `#[non_exhaustive]` attribute and no default variant. Any `match` on a `ResourceState` must cover `Loading`, `Ready(T)`, and `Failed(String)` or the code does not compile. The docstring explicitly calls this property out ("Exhaustively matchable — callers cannot receive a Ready before the future has resolved"). The variant names model the lifecycle correctly: `Loading` is the initial state, `Ready(T)` carries the resolved value (the caller cannot construct a `Ready` without it), and `Failed(String)` requires an error message. The type encoding prevents the caller from ever accessing a `T` before the future has resolved because `T` is only present inside the `Ready` variant.

---

### CLEAN-2: `FormField::parsed()` returns `Result<T, String>`; unvalidated input cannot be silently promoted to `T`

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/form.rs:89`

`parsed()` calls `raw.get().parse::<T>().map_err(|e| e.to_string())` and returns the result. The caller is forced to handle `Err` at the type level. The docstring is explicit: "The caller must handle the error; no silent coercion or default is applied." Combined with the `FromStr + 'static` bound on `T`, the type system prevents a caller from constructing a `FormField<T>` where `T` does not implement `FromStr`, and prevents a caller from obtaining a `T` from the field without explicitly checking the parse result. The raw string is preserved and exposed via `raw()` for validation feedback. This is a well-constructed pit of success for form handling.

---

### CLEAN-3: `on_input_event_handler` is properly platform-gated; the WASM-only method is absent on native

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/form.rs:216`

`#[cfg(target_arch = "wasm32")]` on `on_input_event_handler` means the method does not exist on native targets. A caller writing cross-platform code that accidentally references this method gets a compile error rather than a runtime panic. The companion method `on_input_handler` with `set_input` is available on all targets. The cfg gate cleanly enforces the design intent: DOM-reading code belongs to the WASM layer; testable buffer-based code is universally available.

---

### CLEAN-4: `VElement` event registration has one primary path for typical component authors

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/vdom.rs:317` and `crates/ferric/src/vdom.rs:329`

For a component author attaching event handlers, there are two clearly named builder methods: `on(kind, closure)` for no-argument handlers and `on_with_event(kind, closure)` for handlers that receive the DOM event. The name distinction (`on` vs `on_with_event`) communicates the difference. `on_with_event`'s docstring explains the downcast pattern (`event.downcast_ref::<web_sys::Event>()`). There is no ambiguity about which to reach for: if you need `prevent_default()` or any event property, you use `on_with_event`; otherwise `on`. The dom.rs WASM test (`event_carrying_handler_can_call_prevent_default`) confirms that the `on_with_event` → downcast → `prevent_default()` path works end-to-end.

---

### CLEAN-5: `EventKind` exhaustive match in `event_name` and `stash_key` enforces table synchrony

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/dom.rs:376` and `crates/ferric/src/dom.rs:447`

`event_name()` and `stash_key()` both use exhaustive `match` with no wildcard. The dom.rs doc comment notes this explicitly: "The `match` is exhaustive — no wildcard — so the compiler reports an error if a new variant is added to the enum without updating this table." If a future change adds a variant to `EventKind`, both functions are compile-time errors until the new variant is handled. This directly encodes a correctness invariant in the type system: the DOM event name and stash key tables cannot fall out of sync with the enum without a build failure.

---

## What was examined

| File | Lines / Areas | Sub-question |
|------|---------------|-------------|
| `crates/ferric/src/form.rs` | 1–55 (module doc, FormField struct), 55–103 (FormField impl), 104–228 (Bind struct and impl, on_input_handler, on_input_event_handler), WASM test 465–531 | Q4.1 on_input_event_handler calling convention; Q4.4 type encoding |
| `crates/ferric/src/async_resource.rs` | 1–34 (module doc, suspense state), 57–75 (ResourceState enum), 81–170 (Resource struct and impl including state()), 207–251 (create_resource), 288–313 (suspense) | Q4.2 create_resource footguns; Q4.4 type encoding |
| `crates/ferric/src/vdom.rs` | 66–187 (EventKind enum), 193–201 (EventHandler enum), 287–352 (VElement builder methods: on, on_with_event) | Q4.3 EventHandler registration paths; Q4.4 type encoding |
| `crates/ferric/src/dom.rs` | 229–302 (set_events, closure dispatch), 309–370 (static_event_kinds), 376–438 (event_name exhaustive match), 447–511 (stash_key exhaustive match) | Q4.3 EventHandler registration and dispatch; Q4.4 type encoding |
| `crates/ferric/src/lib.rs` | 40–51 (prelude exports) | Q4.2 create_resource discoverability |

**Sub-question coverage:**

- **Q4.1 — `on_input_event_handler` calling convention**: Examined method signature (form.rs:216), `#[cfg]` gate, return type, documentation, companion `on_input_handler` (form.rs:175), and both methods' interaction with `set_input`. Findings: NB-3 (buffer precondition footgun), NB-4 (no VElement bridge), CLEAN-3 (cfg gate is correct).
- **Q4.2 — `create_resource` API footguns**: Examined `Resource::new`, `Resource::new_fallible`, `create_resource`, `suspense`, prelude exports. Findings: NB-1 (prelude discoverability gap), NB-2 (missing WASM gate on `new`/`new_fallible`).
- **Q4.3 — EventHandler registration paths**: Examined `VElement::on` and `VElement::on_with_event` builder methods, EventHandler enum definition, dom.rs dispatch in `set_events`. Findings: CLEAN-4 (one primary path, clear naming), NB-4 (Bind → VElement gap).
- **Q4.4 — Type system encoding of correctness**: Examined ResourceState exhaustiveness, FormField::parsed return type, FromStr bound, cfg gate on on_input_event_handler, EventKind exhaustive match tables. Findings: CLEAN-1 through CLEAN-5. Noted two un-encoded invariants: temporal ordering of set_input before on_input_handler (NB-3), and one-shot vs reactive construction distinction (NB-1).
