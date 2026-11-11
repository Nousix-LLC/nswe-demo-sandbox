# SUBTASK_async_resource

## Objective
Implement `Resource<T>` with `ResourceState<T>` (Loading / Ready / Failed) and a `suspense`
boundary component in `crates/ferric/src/async_resource.rs`, fully replacing the stub
left by the walking skeleton. Integrates with Ferric's reactive signal runtime.

## Inputs
- Repository: `Nousix-LLC/ferric`, branch `work/ferric-async-forms-r1`
  (created and pushed by SUBTASK_walking_skeleton; `async_resource.rs` stub is present)
- Contract: `../contracts/module_interfaces.md` — exact public API surface to implement
- Existing reactive runtime: `crates/ferric/src/signal.rs` (`Signal<T>`, `create_signal`, `create_effect`, `batch`)
- Existing vdom: `crates/ferric/src/vdom.rs` (`VNode`, `VElement`)
- Dependency already added by skeleton: `wasm-bindgen-futures = "0.4"` in Cargo.toml

## Declared Outputs
1. `crates/ferric/src/async_resource.rs` — full implementation replacing the stub:
   - `ResourceState<T>` enum: `Loading`, `Ready(T)`, `Failed(String)` — exhaustively matchable
   - `Resource<T>` struct wrapping a `Signal<ResourceState<T>>`, driven by `wasm_bindgen_futures::spawn_local`
   - `Resource::<T>::new(fut)` — creates the resource and starts the future
   - `Resource::<T>::state()` — reads current state (reactive: subscribes caller to changes)
   - `suspense(fallback: impl Fn() -> VNode, children: impl Fn() -> VNode) -> VNode` — renders fallback while any resource used inside `children` is Loading
   - Exhaustive `#[cfg(test)]` unit tests (wasm-bindgen-test where async needed, plain unit tests where possible)
2. Changes committed to `work/ferric-async-forms-r1` and pushed
3. `cargo check --target wasm32-unknown-unknown` still passes after changes

## Success Criteria
- `ResourceState<T>` is `Clone` where `T: Clone`; it is an exhaustive enum with no hidden states
- `Resource::new(fut)` compiles and runs: starts the future via `spawn_local`, updates the signal on completion
- `Resource::state()` is reactive (calling it inside an effect subscribes the effect to future changes)
- `suspense` renders the fallback when resources are Loading and transitions to children when Ready
- Tests cover: initial Loading state; transition to Ready; transition to Failed (simulated async error); suspense fallback visible then replaced on Ready
- No existing tests broken; `cargo check` passes

## Constraints
- **Owned file**: `crates/ferric/src/async_resource.rs` exclusively. Do not modify `vdom.rs`, `signal.rs`, `dom.rs`, `lib.rs`, or `form.rs`.
- **Additive**: do not remove or rename types from `signal.rs`.
- **WASM target**: this module runs in WASM. Use `wasm_bindgen_futures::spawn_local` (already in Cargo.toml from skeleton). Do not introduce `tokio` or other async runtimes.
- `ResourceState<T>` must be `std::fmt::Debug` where `T: Debug`.
- The `Failed` variant carries a `String` message (not a boxed error), for WASM-friendliness.
- `suspense` takes two closures (`impl Fn() -> VNode`), not a component trait object, for simplicity.
- Do not change the `Fn()` EventHandler type or vdom structures — out of scope.
- Security: never commit credentials or tokens.
