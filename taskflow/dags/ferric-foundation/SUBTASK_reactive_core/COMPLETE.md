# COMPLETE — SUBTASK_reactive_core

**Task**: Implement `ferric`'s reactive core in `crates/ferric/src/signal.rs` — `Signal`/`Memo`,
effects, batching, sound subscriber cleanup — behind the frozen `signal` API, native-testable.
**Status**: COMPLETED (Atomic)
**Branch**: `work/ferric-foundation` · **Commit**: `f6db6c8`
**Owned path written**: `checkout/crates/ferric/src/signal.rs` (the only file this task owns per
`contracts/_MANIFEST.yaml`). `contracts/` was treated as read-only; no other module was touched.

## What was delivered

A sound, native-testable fine-grained reactive runtime replacing the `todo!()` stubs, matching the
frozen public surface exactly (owner-designed internals only).

### Design chosen (internal representation — my design per the contract's latitude)

- **One thread-local `Runtime`** holding a **generational arena** of reactive nodes. `Signal<T>` and
  `Memo<T>` are `Copy` generational keys `{index, generation}` into that arena, not the values
  themselves. The generation is bumped when a slot is freed, so a stale handle can **never** alias a
  node later allocated into the reused slot (ABA-safe) — the backbone of soundness. (A hand-rolled
  arena was used rather than adding a `slotmap`/`generational-arena` dependency, honoring the
  lean-deps constraint — **no new dependencies were added**.)
- **Values** live in per-node `Rc<RefCell<Box<dyn Any>>>` cells. Reads (`with`/`get`) and writes
  (`set`/`update`) clone the `Rc` out of the runtime first, so the runtime borrow is never held
  across a user closure — this avoids re-entrant `RefCell` panics when a closure reads other signals.
- **Automatic dependency tracking** via an observer stack: the running effect/memo at the top is
  recorded as a subscriber of each signal/memo it reads. **Every run first clears the observer's
  previous source set** (removing those back-subscriptions), so a conditional read that stops
  happening is correctly unsubscribed and subscriber sets never grow unboundedly.
- **Ownership & disposal**: every node is owned by the scope or the running effect/memo that created
  it. Re-running an effect disposes the nodes it created in its previous run (leak-free dynamic
  graphs); dropping a `ReactiveScope` disposes its owned effects/memos and detaches them from every
  subscriber/source set. Disposal + generational keys together are the `no_stale_subscriber_leak`
  guarantee.
- **Memos are lazy**: one eager computation at creation discovers dependencies and the initial
  value; thereafter a dependency change marks the memo dirty and propagates to dependents, and the
  recompute is deferred until the next read. Reads are memoized (no recompute without a change).
- **Batching**: `batch` increments a depth counter (RAII guard, unwind-safe) and defers the flush
  until the outermost batch ends; the pending-effect queue is deduplicated and drained once, so each
  affected effect re-runs at most once per batch. A re-entrant write made by a re-running effect is
  absorbed by the queue rather than nesting flushes.

### Public API note (scope handle)
The frozen `signal` surface was kept exactly (`Signal`/`Memo` get/with/set/update, `create_signal`,
`create_memo`, `create_effect`, `batch`; `Clone`+`Copy` for both handles). The brief's "dropping an
effect/**scope** must unsubscribe it" requirement is realized by a **crate-internal**
`pub(crate) ReactiveScope` (a disposable reactive root), since the frozen `create_effect` returns no
disposer. It has no production caller yet in this serialized layer pipeline (hence a justified,
commented `#[allow(dead_code)]` on the not-yet-consumed scope items); it is exercised by the
soundness tests. It can be promoted to `pub` additively if a later layer needs explicit teardown —
no frozen signature was changed and no amendment was required.

## Test results (native — `cargo test -p ferric`)

`13 passed; 0 failed` (unit) + doctests `3 passed; 1 ignored` (the ignored one is the lib-level
`ignore` example). Coverage maps to the required areas and the manifest identity:

| Test | Exercises |
|------|-----------|
| `signal_get_set_update` | signal read/write/update |
| `signal_with_reads_by_reference_without_clone` | `with` on a non-`Clone` payload |
| `effect_runs_once_immediately_then_on_change` | effect semantics (run-once + re-run) |
| `effect_subscriber_set_does_not_grow_across_reruns` | bounded subscriber set across re-runs |
| `effect_tracks_only_currently_read_dependencies` | dependency re-diffing (stale dep dropped) |
| `memo_computes_and_memoizes` | computed value, memoization, lazy recompute |
| `memo_chains_propagate` | memo→memo chains |
| `effect_reads_memo_and_reruns_on_change` | effect depending on a memo |
| `batch_coalesces_notifications` | batching coalesces to one flush |
| `nested_batches_flush_once_at_the_outermost_boundary` | nested-batch flush semantics |
| **`no_stale_subscriber_leak`** | **soundness identity**: drop owning scope → subscriber removed; `set` after the only subscriber is gone does not touch freed state and does not grow the subscriber set; disposed nodes reclaimed |
| `disposing_scope_also_disposes_owned_memo` | scope disposal unsubscribes a memo |
| `generational_keys_are_aba_safe` | slot reuse bumps generation; stale key resolves to no node |

## Success criteria / identity check (run inside `checkout/`)

- [x] Frozen `signal` surface implemented + rustdoc on all public items; prelude unchanged so
      `use ferric::prelude::*;` still resolves (verified by passing doctests that use the prelude).
- [x] `cargo test -p ferric` passes natively (signals, computed, batching, cleanup).
- [x] `no_stale_subscriber_leak` demonstrated by a native `#[test]`.
- [x] `cargo fmt --all --check` clean.
- [x] `cargo clippy --all-targets -- -D warnings` clean (exit 0).
- [x] `cargo build --workspace` (host) builds.
- [x] `cargo build -p ferric --target wasm32-unknown-unknown` builds.
- [x] No new dependencies; `contracts/` untouched; only the owned `signal.rs` written; committed to
      `work/ferric-foundation`; `main` untouched.

## Composition with the subtree

The downstream layers read the **real** reactive runtime over the serialized seam:
- `SUBTASK_view_and_diff` can run component `render` inside a real `create_effect` and read real
  `Signal`/`Memo` values.
- `SUBTASK_dom_runtime`'s `mount` wraps rendering in `create_effect`; signal changes re-run it, and
  nested effects created per render are disposed automatically on re-render. If explicit unmount
  teardown is later wanted, promote `ReactiveScope` to `pub` (additive).
- The `native_tests_pass` and `no_stale_subscriber_leak` manifest identities for the reactive core
  are satisfied; the synthesis gate can re-run the manifest checks on green.
