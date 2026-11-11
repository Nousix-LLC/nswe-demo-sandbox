# COMPLETE — SUBTASK_dom_runtime

**Task**: Implement `ferric`'s browser runtime (`src/dom.rs`): `mount` + keyed web-sys patch
application + click/input event binding; a wasm **counter** example; the crate **README**.
**Status**: COMPLETE. All manifest identities pass (see table below).
**Branch**: `work/ferric-foundation` @ commit `a88cb4d` (committed, **not** pushed — push + PR belong
to `SUBTASK_synthesis`). Worked only in `../checkout/`; `main` untouched.

## Outputs produced
- `../checkout/crates/ferric/src/dom.rs` — the DOM runtime (replaced the `todo!()` stub).
- `../checkout/crates/ferric/examples/counter.rs` — the wasm counter example.
- `../checkout/crates/ferric/README.md` — counter walkthrough + architecture note + build/run/test.
- `COMPLETE.md` (this file).

## Runtime design (`dom.rs`)
- **`mount(root, component)`** clears `root`, then wraps rendering in `create_effect`. The first
  render builds real DOM under `root`; every later render `diff`s the new view tree against the
  previous one and applies the view layer's keyed `Patch` list to the **live** DOM
  (`SetText`/`SetAttr`/`RemoveAttr`/`SetEvents`/`InsertChild`/`RemoveChild`/`MoveChild`/`Replace`),
  not a subtree rebuild. The effect re-renders automatically whenever a signal the render read
  changes. Render happens **before** any `RefCell` borrow of the retained tree, so no borrow is held
  across a reactive read.
- **Patch addressing**: patches are path-addressed (child indices from the mounted root node). The
  runtime keeps exactly one node under `root` (`root.first_child()`) and walks `child_nodes()` to
  resolve a path; `MoveChild` re-reads the child list after removal and inserts before `to`, matching
  the view layer's documented remove-then-insert positioning semantics.
- **Events**: `click` and `input` are bound from the handlers carried on the view tree. Each listener
  is a `wasm_bindgen` `Closure` stashed on the element object (via `Reflect`) and `forget()`-ed to
  keep it alive for the element's lifetime; `SetEvents` detaches the previously stashed listener
  (`removeEventListener`) before binding the new one, so a re-bind never double-fires. Handlers are
  the view layer's real `Rc<dyn Fn()>` type (consumed, not redefined); a signal-based handler reads
  its state live, so no event payload is needed for the counter.
- **No `unsafe`**: everything goes through safe `web-sys`/`js-sys` wrappers.

## Contract composition (L0 — serialized, real outputs)
- Consumed the **real** `signal` (`create_effect`), `vdom` (`VNode`/`VElement`/`Patch`/`diff`/
  `EventHandler`/`EventKind`), and `component` (`Component`) layers — no mocks, nothing redefined.
- **Additive refinement (within owner latitude, as the contract anticipates)**: `mount` now takes
  the frozen contract's commented-out `root: web_sys::Element` parameter —
  `mount(root: web_sys::Element, component: impl Component + 'static)`. This is additive and does not
  change the prelude re-export surface (`use ferric::prelude::*;` still brings `mount` into scope).
  `contracts/` was **not** edited. No other frozen signature changed; the `vdom` `EventHandler` type
  was left as the view layer froze it (`Rc<dyn Fn()>`).

## Build / test results (`wasm32` toolchain present: rustc/cargo 1.97, target installed)
| Identity | Check | Result |
|---|---|---|
| `workspace_builds` | `cargo build --workspace` | PASS |
| `ferric_wasm_builds` | `cargo build -p ferric --target wasm32-unknown-unknown` | PASS |
| `native_tests_pass` | `cargo test --workspace` | PASS (36 unit + 6 doctests) |
| `fmt_clean` | `cargo fmt --all --check` | PASS |
| `clippy_clean` | `cargo clippy --all-targets -- -D warnings` | PASS (host); also clean on `--target wasm32` |
| `public_api_surface` | `use ferric::prelude::*;` names each item | PASS (counter + compile-only probe) |
| `no_stale_subscriber_leak` | native `#[test]` in `signal.rs` | PASS |
| `counter_example_wasm_builds` | `cargo build -p ferric --example counter --target wasm32-unknown-unknown` | PASS |

## wasm-bindgen-test status (per the brief: run-or-document-as-skipped)
A browser test lives behind `#[cfg(all(test, target_arch = "wasm32"))]` in `dom.rs`
(`mount_renders_initial_view_and_reacts_to_signal_change`). **It could not be RUN in this
environment**: no `wasm-bindgen-test-runner` and no headless browser (chromium/firefox/driver) are
installed. It **does compile** for wasm — verified with
`cargo test -p ferric --target wasm32-unknown-unknown --no-run` (exit 0). Per the brief and the
manifest note, this is not a failure: the **native tests remain the gate** and the wasm **build**
(mandatory) is green. To run the browser test where tooling exists:
`cargo install wasm-bindgen-cli && wasm-pack test --headless --firefox` (or `--chrome`).

## Notes for `SUBTASK_synthesis` (the verification gate)
- All 8 manifest identities verified green here; re-run them inside `../checkout/` to confirm.
- `wasm-bindgen-test` is **compile-verified only** (no runner/browser in this environment) — record
  this in `SYNTHESIS.md`; do not fail the item on missing browser tooling.
- Record the one additive contract refinement: `mount` gained the anticipated `root:
  web_sys::Element` parameter (additive; `contracts/` not modified). If the gate prefers it ratified,
  it is an additive amendment, not an in-place contract edit.
- The crate is complete and shippable: workspace + `ferric` build host & wasm, native tests pass,
  fmt/clippy clean, rustdoc on all public items, README present. Remaining gate work is delivery
  (push `work/ferric-foundation`, open the PR into `main` ending with `Closes #4`).
