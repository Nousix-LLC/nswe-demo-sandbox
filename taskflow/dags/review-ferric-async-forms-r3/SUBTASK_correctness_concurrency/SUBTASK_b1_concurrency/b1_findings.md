# B1 Findings: create_resource Correctness + Concurrency Analysis

**Reviewed file**: `crates/ferric/src/async_resource.rs` (new file, PR #193)
**Head commit**: `838239e` | **Key commit**: `9fedad9`
**Function under review**: `create_resource` (lines 207–251)

---

## Findings

### Q1 — REQ-ASYNC-001: Two-argument API and immediate fire

- **Severity**: clean
- **Requirement**: REQ-ASYNC-001
- **Location**: `crates/ferric/src/async_resource.rs:207–219`
- **Description**: `create_resource` takes exactly two arguments — `source: impl Fn() -> S + 'static` and `fetcher: impl Fn(S) -> F + 'static`. `create_effect` is invoked on line 219 and runs its closure eagerly (first execution is synchronous). That first run calls `source()` (line 221), resets the signal to `Loading` (line 224), increments the generation counter (lines 228–229), and calls `spawn_local` (line 237). The resource fires on construction without any external trigger. REQ-ASYNC-001 is satisfied.

---

### Q2 — REQ-ASYNC-003: Source signal change resets to Loading and re-triggers fetcher

- **Severity**: clean
- **Requirement**: REQ-ASYNC-003
- **Location**: `crates/ferric/src/async_resource.rs:219–248`
- **Description**: `source()` on line 221 is called inside the `create_effect` closure, which registers any signals it reads as dependencies of the effect. When a tracked signal changes, the effect body re-runs in its entirety. Line 224 (`signal.set(ResourceState::Loading)`) resets state to `Loading` before the new fetch begins. Line 231 calls `fetcher(source_value)` with the updated source value, and lines 236–244 spawn the new future. The WASM integration test `create_resource_refetches_on_source_change` (lines ~760–793) confirms the transition sequence under a live browser executor. REQ-ASYNC-003 is satisfied.

---

### Q3 — REQ-ASYNC-005 / REQ-ASYNC-016: Generation counter present and stale futures discarded

- **Severity**: clean
- **Requirement**: REQ-ASYNC-005, REQ-ASYNC-016
- **Location**: `crates/ferric/src/async_resource.rs:217, 228–229, 236, 240–241`
- **Description**: The generation counter is established at line 217 as `Rc::new(Cell::new(0u64))`. Each effect run increments it before spawning (lines 228–229: `let next_gen = gen.get() + 1; gen.set(next_gen)`). The async closure captures `gen_check: Rc::clone(&gen)` (line 236) — a clone of the **same** `Rc`, sharing the underlying `Cell` — and `next_gen: u64`, the generation at spawn time. After `fut.await` completes, the guard on line 240 (`gen_check.get() == next_gen`) compares the CURRENT shared counter against the spawn-time generation. If any subsequent effect run has incremented the counter, the stale future discards its result. Only the most recent future holds the highest `next_gen`, which matches the counter on success. Neither REQ-ASYNC-005 nor REQ-ASYNC-016 have an unmet predicate.

---

### Q4 — Concurrency hazard: spawn_local / create_effect composition; closure captures

- **Severity**: clean
- **Requirement**: (concurrency hazard assessment)
- **Location**: `crates/ferric/src/async_resource.rs:219–248`
- **Description**: No double-borrow or use-after-free hazard. `Cell<u64>` does not issue borrows — `.get()` and `.set()` both take `&self` and operate in-place, so no `BorrowRef` can conflict. `signal: Signal<ResourceState<T>>` is `Copy` (line 99), so the effect closure and the async closure each hold independent copies of a cheap handle, not a shared borrow. No reference or borrow is held across any `await` point: the async closure accesses `gen_check` and `signal` only after `fut.await` returns. The effect closure itself runs to completion synchronously before any spawned microtask can execute, eliminating reentrant access to the shared counter during effect execution.

---

### Q5 — `'static` bounds compatibility and correctness of `Rc<Cell<u64>>`

- **Severity**: clean
- **Requirement**: (async hazard assessment)
- **Location**: `crates/ferric/src/async_resource.rs:217, 236–243`
- **Description**: `wasm_bindgen_futures::spawn_local` requires `F: Future + 'static` but does **not** require `Send`. All values captured by the async closure on line 237 satisfy `'static`: `gen_check: Rc<Cell<u64>>` owns its data with no lifetime parameters (`Cell<u64>` is `'static`); `next_gen: u64` is a copy of a primitive; `signal: Signal<ResourceState<T>>` is `Copy` with `T: 'static` enforced at the struct level (line 89); `fut: F` where `F: Future<Output = T> + 'static` by the function's where-clause (line 213). `Rc<Cell<u64>>` is `!Send` and `!Sync`, which is correct for the WASM single-threaded environment and is compatible with `spawn_local`. No `Send` bound is imposed, and the `!Send` property prevents accidental misuse in multi-threaded contexts.

---

### Q6 — Single-threaded WASM race scenario

- **Severity**: clean
- **Requirement**: (concurrency hazard assessment)
- **Location**: `crates/ferric/src/async_resource.rs:234–244`
- **Description**: WASM executes on a single JS event-loop thread. `spawn_local` queues futures onto the microtask queue; they never execute concurrently with the synchronous `create_effect` closure. The effect completes synchronously — incrementing the generation counter and returning — before any spawned microtask can be dispatched. When the spawned future's continuation runs (after `fut.await`), the effect is not on the call stack, and no overlapping mutation of `gen` or `signal` is possible. No lock or critical section is needed; the execution model guarantees sequential access. The `!Send` marker on `Rc<Cell<u64>>` enforces this at compile time: the type cannot be sent across threads, so the safety property cannot be accidentally violated by a future port to a threaded target.

---

### Q7 — Generation counter soundness: no stale future can overwrite a newer result

- **Severity**: clean
- **Requirement**: REQ-ASYNC-005, REQ-ASYNC-016
- **Location**: `crates/ferric/src/async_resource.rs:217–243`
- **Description**: Traced through the multi-source-change scenario:
  - Effect run N: `gen` becomes N; future Fₙ captures `next_gen = N` and `gen_check` (shared counter).
  - Effect run N+1: `gen` becomes N+1; future Fₙ₊₁ captures `next_gen = N+1`.
  - Fₙ resolves: `gen_check.get()` returns N+1 (the current shared value); `N+1 == N` is false → discards. ✓
  - Fₙ₊₁ resolves: `gen_check.get()` returns N+1; `N+1 == N+1` is true → writes Ready. ✓
  - If Fₙ₊₁ resolves before Fₙ (non-FIFO network): when Fₙ finally resolves, `gen_check.get()` is still N+1 (or higher if more runs occurred); the guard discards correctly. ✓

  The counter is monotonically increasing within a single reactive scope (no overflow risk in practice for a u64), and sharing via `Rc` ensures all futures read the same authoritative value. The design is sound.

---

## What was examined

| Item | Location | Lines | Questions checked |
|------|----------|-------|-------------------|
| `create_resource` function signature and type bounds | `crates/ferric/src/async_resource.rs` | 207–214 | REQ-ASYNC-001 (two-arg API, 'static bounds, F: Future) |
| Initial signal creation and generation counter setup | `crates/ferric/src/async_resource.rs` | 216–217 | REQ-ASYNC-001 (starts in Loading), REQ-ASYNC-016 (counter type) |
| `create_effect` closure body — source tracking | `crates/ferric/src/async_resource.rs` | 219–221 | REQ-ASYNC-001 (fires on construction), REQ-ASYNC-003 (re-trigger on change) |
| `signal.set(ResourceState::Loading)` | `crates/ferric/src/async_resource.rs` | 224 | REQ-ASYNC-003 (reset to Loading before re-fetch) |
| Generation increment before spawn | `crates/ferric/src/async_resource.rs` | 228–229 | REQ-ASYNC-005, REQ-ASYNC-016 (bump-before-spawn ordering) |
| `Rc::clone(&gen)` and `spawn_local` | `crates/ferric/src/async_resource.rs` | 236–244 | Q4 (borrow safety), Q5 ('static bounds), Q6 (single-threaded race) |
| Generation guard after `fut.await` | `crates/ferric/src/async_resource.rs` | 240–242 | REQ-ASYNC-005, REQ-ASYNC-016, Q7 (soundness) |
| Native fallback (`drop(fut)`) | `crates/ferric/src/async_resource.rs` | 246–247 | REQ-ASYNC-001, REQ-ASYNC-003 (testability on native) |
| `Resource { signal }` return | `crates/ferric/src/async_resource.rs` | 250 | REQ-ASYNC-001 (construction contract) |
| Native unit tests for reactive re-trigger | `crates/ferric/src/async_resource.rs` | ~680–735 | REQ-ASYNC-003 (create_resource_source_change_resets_to_loading) |
| Native unit tests for generation counter | `crates/ferric/src/async_resource.rs` | ~737–762 | REQ-ASYNC-016 (create_resource_two_source_changes_stay_loading) |
| WASM integration tests | `crates/ferric/src/async_resource.rs` | ~760–832 | REQ-ASYNC-003 (refetch on source change), full async dispatch path |

**Specific questions checked**:
1. Does `create_resource(source, fetcher)` exist as a two-argument function that fires immediately? → Verified (lines 207–219).
2. Does a source signal change reset to `Loading` and re-trigger the fetcher? → Verified (lines 219–248).
3. Is there a generation counter, and does the future compare its generation before writing? → Verified (lines 217, 228–229, 236, 240–241).
4. Does `create_resource` use `spawn_local` inside `create_effect`? Any double-borrow or use-after-free? → Verified no hazard (lines 219–248).
5. Does the generation counter use types satisfying `'static` bounds for `spawn_local`? Is `Rc<Cell<u64>>` correct? → Verified (lines 207–214, 217, 236–243).
6. Is there a scenario where the effect and future completion handler race on shared mutable state? → Verified no race possible (lines 234–244, single-threaded WASM model).
7. Is the generation counter implementation sound — can no stale future overwrite a newer result? → Verified sound (lines 217–243, traced multi-run scenario).

**Verdict**: All seven questions answered CLEAN. No blockers. No non-blockers warranted by B1 scope. REQ-ASYNC-001, REQ-ASYNC-003, REQ-ASYNC-005, and REQ-ASYNC-016 are all correctly implemented.
