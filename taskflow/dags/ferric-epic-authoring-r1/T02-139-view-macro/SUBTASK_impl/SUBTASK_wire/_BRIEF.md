# _BRIEF.md — SUBTASK_wire: ferric crate wiring

**Task ID:** ferric-authoring-139-view-impl-wire  
**Hub:** SUBTASK_impl  
**Task Kind:** standard  
**Depends on:** SUBTASK_scaffold

---

## Objective

Make two additive file edits to the `ferric` crate so it depends on `ferric-macros` and re-exports `view!`
from its prelude. No implementation code is written here; only Cargo.toml dependency addition and one
`pub use` line in lib.rs.

---

## Inputs

| Input | Location |
|-------|----------|
| Hub context | `../_GLOBAL.md` |
| Hub contract | `../contracts/_MANIFEST.yaml` |
| Current ferric Cargo.toml | `git show origin/work/ferric-epic-authoring-r1:crates/ferric/Cargo.toml` via SSH |
| Current ferric lib.rs | `git show origin/work/ferric-epic-authoring-r1:crates/ferric/src/lib.rs` via SSH |
| Scaffold output | `crates/ferric-macros/Cargo.toml` exists on branch (confirms crate path) |

Access branch files via:
```
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "git -C ~/nswe-demo show origin/work/ferric-epic-authoring-r1:FILE"'
```

---

## Exact changes required

### crates/ferric/Cargo.toml

Add to `[dependencies]` section:
```toml
ferric-macros = { path = "../ferric-macros", version = "0.1" }
```

### crates/ferric/src/lib.rs

Inside `pub mod prelude { … }`, add as the last line before the closing `}`:
```rust
pub use ferric_macros::view;
```

No other lines are added or modified. No existing items are removed or renamed.

---

## Declared Outputs

1. `crates/ferric/Cargo.toml` — updated with ferric-macros dependency line
2. `crates/ferric/src/lib.rs` — updated with `pub use ferric_macros::view;` in prelude

Files must be written directly to the server checkout on branch `work/ferric-epic-authoring-r1`.

---

## Success Criteria

1. `crates/ferric/Cargo.toml` contains `ferric-macros = { path = "../ferric-macros", version = "0.1" }` in `[dependencies]`.
2. `crates/ferric/src/lib.rs` prelude module contains `pub use ferric_macros::view;` (additive only).
3. No existing public export in `crates/ferric/src/lib.rs` is altered, removed, or renamed.
4. `cargo build -p ferric` will succeed once SUBTASK_macro_impl completes (this task only writes the files, not verifies the build — that is SUBTASK_synthesis's job).

---

## Constraints

- Only two files may be modified: `crates/ferric/Cargo.toml` and `crates/ferric/src/lib.rs`.
- Changes are strictly additive: insert one line in each file.
- Do NOT run `cargo build` from within this task — compilation verification belongs to SUBTASK_synthesis.
- Never put server address, SSH key path, user name, or host paths into committed files.

---

## Suggested Methodology Files

**Task-type row:** "Writing Rust code" → Primary: `rust`; Supporting: `core`

- `rust/Rust_Cargo_Ecosystem_Methodology.md` — workspace dependency declarations, path dependencies,
  how to add a dependency line to Cargo.toml while preserving workspace conventions
- `core/BestPractices_Coding_Standards_Methodology.md` — minimal correct additive change discipline

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load
these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Additive-only: identity IA4 (from parent hub contract `../contracts/_MANIFEST.yaml`) forbids
  removing or modifying any existing public export.
- Workspace `[lints]` apply; no new lints need to be suppressed for this additive change.
- The `pub use ferric_macros::view;` line re-exports a proc-macro, which is accessible via the
  macro_rules scoping after `use ferric::prelude::*;`.

## Out-of-Scope Methodologies

- `Rust_Macros_And_Codegen_Methodology.md` — not needed; this task writes no macro code.
- `synthesis/Synthesis_Overview_Methodology.md` — verification is SUBTASK_synthesis's job.
