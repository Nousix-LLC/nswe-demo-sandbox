# COMPLETE — T05: Context and dependency injection (#142)

**Task ID:** ferric-authoring-142-ctx  
**Branch:** `work/ferric-epic-authoring-r1`  
**Commit:** `82d267f` (rebased over T04)  
**Issue closed:** #142

---

## Deliverables

### Context store — `crates/ferric/src/signal.rs`

Added a `context: HashMap<TypeId, Box<dyn Any>>` field to the existing `Node` struct.  
Initialized to `HashMap::new()` in `Node::blank()`.  
No new module; the context implementation shares the same runtime internals and
disposal path as signals and effects.

### Three public free functions (all additive; nothing removed or changed)

| Function | Signature | Behaviour |
|---|---|---|
| `provide_context` | `pub fn provide_context<T: Clone + 'static>(value: T)` | Stores value under `TypeId::of::<T>()` on the current owner node. No-op if no active owner. |
| `use_context` | `pub fn use_context<T: Clone + 'static>() -> Option<T>` | Walks the owner parent chain (innermost first); returns first matching `T`, or `None`. Not reactive — does not subscribe the caller. |
| `expect_context` | `pub fn expect_context<T: Clone + 'static>() -> T` | Calls `use_context`; panics with `"no context of type \`{type_name}\` was found; an ancestor component must call \`provide_context::<{type_name}>(..) \`before this component is rendered"` if absent. |

### Prelude export — `crates/ferric/src/lib.rs`

Added `expect_context`, `provide_context`, `use_context` to the signal re-export line
in `ferric::prelude`. Merged cleanly with T04's component additions.

### Test suite — six acceptance-criteria cases (native, no browser)

| Test | Criterion |
|---|---|
| `context_provide_and_read_simple_value` | Provide/read integer and String |
| `context_provide_signal_and_read_live_value` | Provide `Signal<i32>`; confirm live handle |
| `use_context_returns_none_when_no_provider` | Returns `None` with no provider |
| `expect_context_panics_with_named_type` | `#[should_panic(expected = "no context of type")]` |
| `context_nearest_ancestor_shadowing` | Inner provider shadows outer; outer restored after inner run |
| `context_scoped_cleanup` | `live_node_count()` returns to baseline after scope drop |

All 43 unit tests + 7 doc-tests pass (`cargo test -p ferric`).

---

## Design decisions

**Single disposal path.** Context entries are stored as a HashMap field on the `Node` struct.
When `Runtime::dispose` removes a node from the arena (`arena.remove(id)`), the Node is dropped,
which drops the HashMap and its `Box<dyn Any>` entries. No second lifetime rule; no separate
cleanup hook.

**Non-reactive lookup.** `use_context`/`expect_context` do not call `rt.track(...)`.
Reactivity is obtained through the provided handle (e.g. a `Signal<T>`), not through the
lookup itself — per design spec §4.3.

**TypeId key.** `TypeId::of::<T>()` is stable and infallible on stable Rust 1.82.
The HashMap key guarantees the downcast in `use_context` always matches — the `downcast_ref`
path is a safety belt, not a runtime branch.

**No active owner — silent no-op.** `provide_context` with no owner stack entry is silently
discarded. Panicking here would surprise callers at the application root, which is a valid
pattern.

---

## CI status

Branch pushed to `origin/work/ferric-epic-authoring-r1`. Rebased cleanly over T04 (disjoint
areas — T04 adds component exports; T05 adds context functions). Ready for T06.
