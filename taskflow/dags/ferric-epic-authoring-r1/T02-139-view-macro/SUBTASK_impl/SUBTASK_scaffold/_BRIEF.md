# _BRIEF.md — SUBTASK_scaffold: ferric-macros crate scaffold

**Task ID:** ferric-authoring-139-view-impl-scaffold  
**Hub:** SUBTASK_impl  
**Task Kind:** standard  
**Depends on:** none

---

## Objective

Create the `crates/ferric-macros/` proc-macro crate with `Cargo.toml` and a compilable stub `src/lib.rs`.
This establishes the crate structure that SUBTASK_macro_impl and SUBTASK_wire depend on.

**Important:** The root workspace `Cargo.toml` uses `members = ["crates/*"]` — a glob. Creating
`crates/ferric-macros/` automatically makes it a workspace member. Do NOT modify the root `Cargo.toml`.

---

## Inputs

| Input | Location |
|-------|----------|
| Hub context | `../_GLOBAL.md` |
| Hub contract | `../contracts/_MANIFEST.yaml` |
| Root workspace Cargo.toml | `git show origin/work/ferric-epic-authoring-r1:Cargo.toml` via SSH |
| Ferric Cargo.toml | `git show origin/work/ferric-epic-authoring-r1:crates/ferric/Cargo.toml` via SSH |
| Existing crates list | `git ls-tree origin/work/ferric-epic-authoring-r1:crates/` via SSH |

Access branch files via:
```
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "git -C ~/nswe-demo show origin/work/ferric-epic-authoring-r1:FILE"'
```

---

## Declared Outputs

1. `crates/ferric-macros/Cargo.toml` — proc-macro crate manifest
2. `crates/ferric-macros/src/lib.rs` — stub proc-macro (compiles cleanly; macro body is a placeholder)

The files must be authored on the server checkout via SSH `git checkout work/ferric-epic-authoring-r1 && mkdir -p crates/ferric-macros/src && ...` or equivalent.

---

## Success Criteria

1. `crates/ferric-macros/Cargo.toml` exists on the branch with `proc-macro = true`, `edition = "2021"`, `rust-version = "1.82"`, and dependencies `proc-macro2`, `quote`, `syn` (features = ["full"]).
2. `crates/ferric-macros/src/lib.rs` exists with a compilable stub `view!` proc-macro (may output empty TokenStream).
3. `cargo build -p ferric-macros` succeeds on stable Rust 1.82.
4. Root `Cargo.toml` is NOT modified.
5. Files are present on branch `work/ferric-epic-authoring-r1` after the task.

---

## Constraints

- Do NOT modify root `Cargo.toml` (the glob `members = ["crates/*"]` already covers the new crate).
- Do NOT modify any ferric crate files (that is SUBTASK_wire's job).
- Proc-macro deps: `proc-macro2`, `quote`, `syn` only (no `proc-macro-error` or other crates).
- MSRV: stable Rust 1.82; no nightly features.
- Never put server address, SSH key path, user name, or host paths into committed files.

---

## Suggested Methodology Files

**Task-type row:** "Writing Rust code" → Primary: `rust`; Supporting: `core`

- `rust/Rust_Cargo_Ecosystem_Methodology.md` — workspace member setup, crate manifest conventions,
  proc-macro crate setup (how to declare `proc-macro = true`, workspace inheritance)
- `core/BestPractices_Coding_Standards_Methodology.md` — baseline code quality; correct file/module
  structure for a minimal Rust crate

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load
these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Workspace rust-version: 1.82 (from `[workspace.package]`)
- Workspace edition: 2021
- Use `workspace = true` inheritance where applicable (e.g. `version.workspace = true`)
- The crate purpose is a Rust procedural macro; `proc-macro = true` is required in Cargo.toml
- Proc-macro crate cannot have `[lib] crate-type` other than `proc-macro` on stable Rust

## Out-of-Scope Methodologies

- `Rust_Macros_And_Codegen_Methodology.md` — the full macro implementation is SUBTASK_macro_impl's job,
  not this task's. This task only creates the scaffolding.
