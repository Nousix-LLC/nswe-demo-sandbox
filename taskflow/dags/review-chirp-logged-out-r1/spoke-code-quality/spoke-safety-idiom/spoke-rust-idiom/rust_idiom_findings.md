# rust_idiom_findings.md — Concern 10: Rust/WASM Idiom Patterns

**Reviewed at commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
**Files examined**: `crates/ferric/src/hydrate.rs`, `crates/ferric/src/async_resource.rs`, `crates/ferric/src/signal.rs`

## Verdict

FINDINGS

## Findings

### Finding 1: hydrate.rs::set_events uses Closure::forget() without documenting the bounded memory leak

- **Location**: `crates/ferric/src/hydrate.rs`, line 473 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: Intentional memory leaks must be documented at or near the call site, so the trade-off remains visible to maintainers of that file.
- **Why it matters**: `hydrate.rs::set_events` (line 417) is structurally identical to `dom.rs::set_events` (line 229). The `dom.rs` module comment at lines 27–33 explains that `Closure::forget()` permanently leaks the Rust closure allocation for each handler slot: the stash/detach protocol removes the DOM listener reference, but the underlying `Box<dyn FnMut(web_sys::Event)>` allocated by `Closure::wrap` is unrecoverable once forgotten. `hydrate.rs` carries the same leaking call at line 473 with no equivalent note. A maintainer changing event-handler lifecycle in `hydrate.rs` has no prompt to check whether a future migration to a deterministic closure registry (described in `dom.rs` line 33 as a planned improvement) would need to cover `hydrate.rs` as well.
- **Severity**: non-blocking
- **Satisfying condition**: Add a comment to `hydrate.rs` — in the module doc or immediately above `set_events` — stating that `Closure::forget()` permanently leaks the closure allocation and that this is a bounded trade-off (one allocation per active handler slot per element), matching the note at `dom.rs` lines 27–33.

---

### Finding 2: Resource::new and Resource::new_fallible call spawn_local without a wasm32 cfg gate or API doc note

- **Location**: `crates/ferric/src/async_resource.rs`, lines 112 and 133 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: WASM-only entry points should state their target restriction in their API documentation, or use `#[cfg]` gates consistently with equivalent functions in the same module.
- **Why it matters**: `create_resource` (line 207) wraps its `spawn_local` call at line 237 in `#[cfg(target_arch = "wasm32")]` and documents the native fallback in a "WASM gate" doc section. `Resource::new` (line 112) and `Resource::new_fallible` (line 133) call `spawn_local` unconditionally — these methods compile only on WASM. A developer reading the doc comment for `Resource::new` sees no indication of the target restriction; a developer extending the resource API by following the `Resource::new` pattern will produce a WASM-only constructor without noticing the alternative `create_resource` establishes. The asymmetry is noted only in a test comment at line 426, which is not part of the public API surface.
- **Severity**: non-blocking
- **Satisfying condition**: Either (a) add a `# Platform notes` or `# WASM gate` section to the `Resource::new` and `Resource::new_fallible` doc comments stating these methods require `wasm32` and citing `create_resource` for the native-compatible pattern, or (b) add `#[cfg(target_arch = "wasm32")]` to both methods and add `#[cfg(not(target_arch = "wasm32"))]` stubs that drop the future and return a resource in `Loading` state, matching `create_resource`'s behavior.

---

## Clean Account

- **Concern 10 — spawn_local for async effects**: Checked `crates/ferric/src/async_resource.rs` lines 112–148 (`Resource::new`, `Resource::new_fallible`) and 207–244 (`create_resource`). `wasm_bindgen_futures::spawn_local` is the idiomatic WASM equivalent of `tokio::spawn` and is the correct mechanism for running futures from synchronous reactive code. Captured closures hold only signal keys — generational arena handles that become silent no-ops if the backing node is disposed — so there is no harmful fire-and-forget concern. `create_resource` applies a generation counter (lines 217–240) to discard results from superseded in-flight fetches. `Resource::new` and `Resource::new_fallible` omit the counter because each instance spawns exactly one future. Finding 2 (documentation gap, non-blocking).

- **Concern 10 — thread_local! + RefCell for reactive state**: Checked `crates/ferric/src/signal.rs` lines 50–56 (RUNTIME declaration and `with_rt`). The reactive runtime is stored as `thread_local! { static RUNTIME: RefCell<Runtime> }`. The `with_rt` accessor acquires `borrow_mut()`, runs the callback, and releases the borrow before returning. Per-node values live in separate `Rc<RefCell<Box<dyn Any>>>` cells; user closure execution in `run_computation` (lines 349–395) holds no RUNTIME borrow during the closure call, so there is no re-entrant borrow panic risk in normal usage. `Cell<bool>` and `Cell<u32>` in `async_resource.rs` (not `RefCell`) are used for the suspense tracking statics where no borrow check is needed. The same pattern underlies Leptos's reactive runtime. Clean.

- **Concern 10 — Cell<bool> for the started guard**: Checked `crates/ferric/src/async_resource.rs` lines 28–33 (`SUSPENSE_DEPTH: Cell<u32>` at line 30 and `SUSPENSE_HAS_LOADING: Cell<bool>` at line 32). `Cell<T>` for `Copy` types has no borrow-check overhead and no panic risk. WASM is single-threaded; `thread_local!` enforces that these statics are accessed only from one thread, making `Cell` sufficient and `AtomicBool`/`AtomicU32` unnecessary. The flag is reset to `false` at each `suspense()` entry and read back before exiting — no cross-invocation state bleed. The `const { Cell::new(0) }` initializer avoids lazy-init overhead. Clean.

- **Concern 10 — Closure::forget() in hydrate.rs**: Checked `crates/ferric/src/hydrate.rs` lines 417–487 (`set_events`). Event handler closures must outlive the calling frame: `add_event_listener_with_callback` registers a JS function reference held by the DOM, and dropping the Rust `Closure` would invalidate that reference. `closure.forget()` at line 473 is the correct choice for a persistent event handler. The stash/detach protocol (steps 1–2 of `set_events`) correctly removes old DOM listeners before each re-bind. The `dom.rs` module comment (lines 27–33) documents the resulting bounded memory leak; `hydrate.rs` carries the same leaking call without the same documentation. Finding 1 (documentation gap, non-blocking).
