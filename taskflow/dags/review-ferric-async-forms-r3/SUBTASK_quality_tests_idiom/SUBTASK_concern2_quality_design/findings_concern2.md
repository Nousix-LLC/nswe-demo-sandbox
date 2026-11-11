## Findings — Concern 2 (Code Quality and Design)

---

### Finding 1

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/vdom.rs` (module-level)
- **description**: `vdom.rs` is entirely free of `web_sys` imports — confirmed by reading the full file at head commit `838239e`. The module doc explicitly asserts this: *"Everything in this module is pure and native-testable: it performs no `web-sys` calls."* The `EventHandler::WithEvent` variant uses `Rc<dyn Fn(&dyn std::any::Any)>` as its type erasure layer, keeping the virtual DOM module platform-independent. The boundary is principled: `vdom.rs` defines the abstraction; `dom.rs` holds the concrete `web_sys::Event` and passes it through the erasure with `f(&event as &dyn std::any::Any)`. This is the design criterion from `FrameworkDesign_Library_API_Design_Methodology.md` §Escape hatches — the lower-layer concern is confined to the right module without leaking internals upward.

---

### Finding 2

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/vdom.rs:60–90` (EventHandler enum and EventKind enum)
- **description**: The `EventHandler` enum variant scheme is a sound abstraction boundary. Replacing the previous type alias `type EventHandler = Rc<dyn Fn()>` with a two-variant enum (`NoArg` / `WithEvent`) makes the distinction explicit at every call site. Callers who want to call `prevent_default()` or read `event.target()` choose `WithEvent` and perform the downcast; callers who do not choose `NoArg`. Neither the dom layer's `set_events` nor `form.rs`'s `on_input_handler()` have to guess or branch silently. The VElement builder preserves a clean forward-compatible API: `.on()` for NoArg, `.on_with_event()` for WithEvent — existing callers passing `move || { ... }` closures to `.on()` are unaffected. The enum satisfies `Clone` (not `Copy`, since `Custom(String)` prevents it), and all impacted `*k` → `k.clone()` mechanical adaptations in `diff_events` and `event_kinds` are present and correct.

---

### Finding 3

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/async_resource.rs:188–243` (create_resource generation counter)
- **description**: The generation counter invariant is straightforward and followable in a single pass. The pattern is: allocate `Rc<Cell<u64>>` initialized to `0`; on each reactive re-trigger, compute `next_gen = gen.get() + 1`, call `gen.set(next_gen)`, then inside the spawned async closure read `gen_check.get() == next_gen` — where `gen_check` is an `Rc::clone` of the same counter. The function-level doc comment identifies exactly this pattern and ties it to REQ-ASYNC-016. Variable naming — `gen` (the shared counter), `next_gen` (the value at spawn time), `gen_check` (the clone for the async closure) — is locally clear: `next_gen` being a captured *value* and `gen_check` being a *reference clone* together make the check self-explanatory without tracing through extra indirection. A future reader does not need to leave `create_resource` to understand the cancellation invariant.

---

### Finding 4

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/async_resource.rs`, `crates/ferric/src/vdom.rs`, `crates/ferric/src/dom.rs`, `crates/ferric/src/form.rs`
- **description**: Responsibility separation across the four files is clean with no unexpected imports or tight coupling introduced by the remediation. `async_resource.rs` owns reactive async state (resource lifecycle, suspense tracking, generation counter); it imports only from `crate::signal` and `crate::vdom::VNode` — no DOM coupling. `vdom.rs` owns the pure virtual DOM (tree representation, keyed diff); no web_sys. `dom.rs` owns the DOM runtime (mounting, patching, event binding); it imports web_sys as expected and is the sole module that holds `web_sys::Event` and passes it through the `&dyn Any` erasure. `form.rs` owns typed form state (`FormField<T>`) and the bridge between DOM events and form state (`Bind<T>`); it imports only `crate::signal`, `crate::vdom::EventHandler`, and — gated to `#[cfg(target_arch = "wasm32")]` — `web_sys::Event` and `web_sys::HtmlInputElement`. The cfg gate correctly confines web_sys coupling to WASM builds. No cross-module coupling leaks were introduced.

---

### Finding 5

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/async_resource.rs:40–80` (ResourceState), `crates/ferric/src/form.rs:50–130` (FormField)
- **description**: Both `ResourceState` and `FormField`/`Bind` are designed to invite correct use and make common misuse harder to express. `ResourceState` is an exhaustive three-variant enum (`Loading`, `Ready(T)`, `Failed(String)`) that must be matched; callers cannot receive a `Ready` value and silently ignore loading or error states. `FormField::parsed()` returns `Result<T, String>` — the doc explicitly states "No silent `unwrap` or default is applied" — forcing every submit handler to handle parse failure. The `Bind` pattern separates the input buffer (`set_input`) from the event dispatch (`on_input_handler`), keeping the NoArg path WASM-free and testable without a browser. Both designs follow `FrameworkDesign_Library_API_Design_Methodology.md` §One obvious way and §Design for the pit of success: illegal states require active work to reach, and the correct path is the obvious path.

---

### Finding 6

- **severity**: non-blocker
- **concern**: code-quality
- **location**: `crates/ferric/src/dom.rs:275–330` (`static_event_kinds` function)
- **description**: `static_event_kinds()` is a manually-maintained array of all 47 non-`Custom` `EventKind` variants. The function doc notes it "must be kept in sync when new variants are added to `EventKind`." The two adjacent functions — `event_name()` and `stash_key()` — use exhaustive `match` statements with no wildcard arm, so adding a new non-`Custom` variant to `EventKind` will produce a compile error in those functions. `static_event_kinds()` has no such guard: it is a plain array literal, and the compiler will not flag a missing entry. The result is an asymmetry: a developer adding a new variant will see compile errors in `event_name`/`stash_key` (and fix them), but may overlook `static_event_kinds`. If the new variant is omitted from the array, the detach pass in `set_events` will not remove any previously-stashed closure for that variant on re-bind, leaving a stale, double-firing listener.

  The existing doc comment correctly identifies the coupling but relies on human discipline rather than the type system. One approach that would make this compiler-enforced: replace the separate array with a single lookup table `fn static_event_table() -> [(EventKind, &'static str, &'static str); N]` and derive `event_name`, `stash_key`, and the detach iteration from the same exhaustive source — or store the set of previously-bound static variants alongside Custom names on the element so the detach pass iterates only what was actually bound. Neither is required to merge; the current approach is functional and the existing comment adequately warns maintainers. Raise as a follow-on task.

---

### Finding 7

- **severity**: non-blocker
- **concern**: code-quality
- **location**: `crates/ferric/src/vdom.rs:62` (`#[allow(clippy::type_complexity)]`)
- **description**: The `#[allow(clippy::type_complexity)]` attribute suppresses a clippy lint on the entire `EventHandler` enum. The triggering type is `Rc<dyn Fn(&dyn std::any::Any)>` (double `dyn`). The suppression is applied at the enum level, which means future additions to the enum that genuinely do increase type complexity will be silently excluded from the lint. A type alias — e.g. `type AnyEventFn = Rc<dyn Fn(&dyn std::any::Any)>` declared locally or in the same file — would eliminate the need for the allow attribute and self-document the erased function type. No behavior impact; raise as a follow-on style nit if the team has a policy against allow attributes on public types.

---

## What was examined

| File | Lines / area examined | Sub-question addressed |
|------|----------------------|----------------------|
| `crates/ferric/src/vdom.rs` | Full module (file read at commit `838239e`): imports section (lines 30–34), EventHandler enum declaration (lines ~62–80), EventKind enum expansion (~60–155), VElement builder methods `.on()` / `.on_with_event()` (~310–340), `diff_events` and `event_kinds` adaptations (~437–441, ~625) | EventHandler abstraction boundary; web_sys import check; EventKind design |
| `crates/ferric/src/async_resource.rs` | PR diff lines 1–340 (full file is new): imports (~15–22), `ResourceState` enum (~40–80), `Resource<T>` struct and `state()` method (~90–165), `create_resource` function and generation counter (~188–243) | Generation counter clarity; responsibility separation; design for correct use |
| `crates/ferric/src/dom.rs` | PR diff lines 215–522: `set_events` rewrite, `static_event_kinds()`, `event_name()`, `stash_key()` | Responsibility separation; dispatch coupling; static_event_kinds maintenance concern |
| `crates/ferric/src/form.rs` | PR diff lines 620–900 (full new file): `FormField<T>` struct and impl, `Bind<T>` struct and impl, `on_input_handler()`, `on_input_event_handler()` (wasm32 gate), cfg imports | Responsibility separation; design for correct use; web_sys coupling confinement |
| `crates/ferric/src/vdom.rs` import list | Confirmed by full file read: `use std::collections::{BTreeMap, HashSet}`, `use std::fmt`, `use std::rc::Rc` only | web_sys import check (required by brief) |
| `crates/ferric/src/async_resource.rs` import list | Lines 15–22: `std::cell::Cell`, `std::future::Future`, `std::rc::Rc`, `wasm_bindgen_futures::spawn_local`, `crate::signal`, `crate::vdom::VNode` | Coupling check; confirms no web_sys at module level |
