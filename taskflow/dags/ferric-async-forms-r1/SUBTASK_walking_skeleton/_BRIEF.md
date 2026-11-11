# SUBTASK_walking_skeleton

## Objective
Establish the branch, GitHub issues, and the frozen shared seam (expanded `EventKind` +
module stubs in `lib.rs` + stub source files) that the three feature spokes will compile against.
Every deliverable here is a contract that must not be changed after this task completes.

## Inputs
- Repository: `Nousix-LLC/ferric` (public), currently on `main @ aa24687`
- Contracts manifest: `../contracts/event_kind_contract.md` (full EventKind set)
- Contracts manifest: `../contracts/module_interfaces.md` (public types each new module exports)
- Hub context: `../_GLOBAL.md`

## Declared Outputs
1. Branch `work/ferric-async-forms-r1` exists on `Nousix-LLC/ferric` remote, based on current `main`
2. GitHub issues created in `Nousix-LLC/ferric`:
   - Epic issue: "Ferric 1.0 — Async, Forms, and Events" (label: `epic`, `enhancement`)
   - Sub-issue: "#143: Async resources + suspense" (label: `enhancement`)
   - Sub-issue: "#144: Full DOM event handling" (label: `enhancement`)
   - Sub-issue: "#145: Two-way form binding" (label: `enhancement`)
   - Record the actual assigned issue numbers in this task's COMPLETE.md so synthesis can close them
3. `crates/ferric/src/vdom.rs` — `EventKind` enum extended to full set per `contracts/event_kind_contract.md`
   (all variants, derive `Clone, Debug, PartialEq, Eq, Hash`; `Custom(String)` escape hatch)
4. `crates/ferric/src/lib.rs` — `pub mod async_resource;` and `pub mod form;` declarations added
5. `crates/ferric/src/async_resource.rs` — stub file created (compiles; exports `ResourceState`, `Resource`, `suspense` as `todo!()` / placeholder types)
6. `crates/ferric/src/form.rs` — stub file created (compiles; exports `FormField<T>` and `Bind<T>` as placeholder types)
7. `crates/ferric/Cargo.toml` — `wasm-bindgen-futures = "0.4"` added under `[dependencies]`
8. All changes committed to branch `work/ferric-async-forms-r1` and pushed; `cargo check` passes (CI green or green locally)
9. This task's `COMPLETE.md` records: branch name, actual issue numbers assigned by GitHub, commit SHA

## Success Criteria
- Branch exists and CI (if configured) passes on the branch after push
- `cargo check --target wasm32-unknown-unknown` passes on the stub files
- The expanded `EventKind` enum matches the full set in `contracts/event_kind_contract.md` exactly
- Stub files compile without errors (even if functions are `todo!()`)
- GitHub issues exist with the correct titles, labels, and body text referencing the epic

## Constraints
- **Scope**: `crates/ferric/` only. Do not touch `design/`, docs, or other crates.
- **Additive only**: do not remove or rename existing `EventKind::Click` or `EventKind::Input` variants.
- **No secrets**: never commit tokens, keys, or credentials.
- **No force-push to main**.
- **Files owned exclusively by this task**: `vdom.rs` (extend EventKind), `lib.rs` (pub mod additions), `async_resource.rs` (stub), `form.rs` (stub), `Cargo.toml` (dependency addition). After this task completes, spokes own these files and must not conflict with this task's additions.
- The stub files must compile. Use `#[allow(dead_code)]` and `todo!()` as needed.
- Cargo.toml: add `wasm-bindgen-futures = "0.4"` to `[dependencies]` (not dev-dependencies).
