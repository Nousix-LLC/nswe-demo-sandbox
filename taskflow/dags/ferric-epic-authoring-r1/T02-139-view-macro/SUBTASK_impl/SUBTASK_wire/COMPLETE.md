# COMPLETE — SUBTASK_wire: ferric crate wiring

## Status: COMPLETED

## What was done

Made exactly two additive edits to the `ferric` crate on branch `work/ferric-epic-authoring-r1`:

### 1. `crates/ferric/Cargo.toml`
Added to `[dependencies]` section (before the `[dev-dependencies]` block):
```toml
ferric-macros = { path = "../ferric-macros", version = "0.1" }
```

### 2. `crates/ferric/src/lib.rs`
Added as the last line before the closing `}` of `pub mod prelude`:
```rust
    pub use ferric_macros::view;
```

## Declared Outputs

- `crates/ferric/Cargo.toml` — updated with ferric-macros dependency line ✅
- `crates/ferric/src/lib.rs` — updated with `pub use ferric_macros::view;` in prelude ✅

## Verification Against Success Criteria

1. ✅ `crates/ferric/Cargo.toml` contains `ferric-macros = { path = "../ferric-macros", version = "0.1" }` in `[dependencies]`.
2. ✅ `crates/ferric/src/lib.rs` prelude module contains `pub use ferric_macros::view;` (additive only).
3. ✅ No existing public export altered, removed, or renamed — all prior exports intact.
4. ✅ `cargo build -p ferric` will succeed once SUBTASK_macro_impl completes (build verification deferred to SUBTASK_synthesis per constraint).

## Constraints Honored

- Only the two specified files were modified.
- Changes are strictly additive: 1 line inserted in each file (+ 1 blank separator line in Cargo.toml for readability).
- `cargo build` was not run from this task.
- No server address, SSH key path, user name, or host paths in committed files.

## Commit

`912ed57` — `ferric: wire ferric-macros dependency and re-export view! in prelude`  
Branch: `work/ferric-epic-authoring-r1`  
Files changed: 2, insertions: 3
