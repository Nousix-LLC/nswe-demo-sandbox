# SUBTASK_walking_skeleton — COMPLETE

## Status
Completed successfully. All declared outputs delivered; `cargo check --target wasm32-unknown-unknown` passes.

## Branch
`work/ferric-async-forms-r1` — pushed to `Nousix-LLC/ferric` remote.

## Commit SHA
`5e49c4fe6bbd888a21ee2dd60eb7e53e87d20d18`

## GitHub Issues Created

| Role        | Title                                  | Issue # | Labels             |
|-------------|----------------------------------------|---------|--------------------|
| Epic        | Ferric 1.0 — Async, Forms, and Events | #1      | epic, enhancement  |
| Sub-issue   | Async resources + suspense             | #2      | enhancement        |
| Sub-issue   | Full DOM event handling                | #3      | enhancement        |
| Sub-issue   | Two-way form binding                   | #4      | enhancement        |

## Files Delivered

| File | Change |
|------|--------|
| `crates/ferric/src/vdom.rs` | `EventKind` expanded to full 50-variant set; derives changed to `Clone, Debug, PartialEq, Eq, Hash` (no Copy/PartialOrd/Ord — `Custom(String)` prevents them); all `*k` deref usages changed to `k.clone()`; test shadow `BTreeSet<EventKind>` changed to `HashSet<EventKind>` |
| `crates/ferric/src/dom.rs` | Minimal compilation fix: `*kind` derefs changed to `kind.clone()`; `event_name` and `stash_key` given `_ => todo!()` arms for new variants (SUBTASK_dom_events will replace these) |
| `crates/ferric/src/lib.rs` | Added `pub mod async_resource;` and `pub mod form;` |
| `crates/ferric/src/async_resource.rs` | New stub: `ResourceState<T>`, `Resource<T>`, `suspense()` — all bodies `todo!()` |
| `crates/ferric/src/form.rs` | New stub: `FormField<T>`, `Bind<T>` — all bodies `todo!()` |
| `crates/ferric/Cargo.toml` | Added `wasm-bindgen-futures = "0.4"` to `[dependencies]` |

## Notes for Spoke Tasks

- **dom.rs ownership**: `dom.rs` was minimally patched (only the two `*kind` deref sites and
  the `todo!()` arms in `event_name`/`stash_key`) to maintain compilation after `Copy` was
  removed from `EventKind`. SUBTASK_dom_events owns the full implementation of these functions
  and must replace the `todo!()` arms with the complete mapping from
  `contracts/event_kind_contract.md`.

- **EventKind is frozen**: The 50-variant set (including `Custom(String)`) is the contract.
  Spoke tasks must not add, remove, or rename variants.

- **API surfaces are frozen**: The public types and method signatures in `async_resource.rs`
  and `form.rs` are the contract per `contracts/module_interfaces.md`. Spoke tasks implement
  the bodies; they must not change the signatures.

- **wasm-bindgen-futures** is now a direct dependency in `crates/ferric/Cargo.toml`.
  SUBTASK_async_resource should use `wasm_bindgen_futures::spawn_local` for future execution.
