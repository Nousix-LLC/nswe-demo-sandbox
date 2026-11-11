# COMPLETE — SUBTASK_b1_hydrate_fix

**Task**: Remediate B1 — Wire ferric::hydrate() from WASM entry point  
**Status**: COMPLETED  
**Commit**: `7fb90c7` on `work/ferric-ssr-r1`, pushed to origin

## What was done

1. **`crates/chirp-frontend/src/app.rs`** — Replaced the unconditional `mount(root, app)` call
   at the end of `start()` with a conditional block:
   - calls `ferric::hydrate(root, app)` when `root.has_child_nodes()` is true (SSR path)
   - calls `mount(root, app)` otherwise (fresh CSR path)

2. **`crates/chirp-server/src/ssr.rs`** — Updated item 4 of the `assemble_document` doc comment
   from an unconditional `ferric::hydrate` reference to a description of the conditional
   hydrate-or-mount behavior.

## Verification

- `cargo check --target wasm32-unknown-unknown -p chirp-frontend` → exit 0
- `cargo check -p chirp-server` → exit 0

## Declared output

`taskflow/dags/ferric-ssr-r4/SUBTASK_b1_hydrate_fix/b1_resolution.md`
