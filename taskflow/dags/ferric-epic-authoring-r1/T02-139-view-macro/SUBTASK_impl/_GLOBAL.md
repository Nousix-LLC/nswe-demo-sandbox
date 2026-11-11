# _GLOBAL.md — SUBTASK_impl decomposition hub

**Task ID:** ferric-authoring-139-view-impl  
**Hub:** T02-139-view-macro  
**Branch:** `work/ferric-epic-authoring-r1`  
**Starts from:** commit `1ccdce0`

---

## Objective

Decompose the SUBTASK_impl `view!` macro implementation into four sequential+partially-parallel subtasks:
scaffold → (macro_impl ∥ wire) → synthesis/commit.

---

## Scope

**In scope:**
- All files owned by SUBTASK_impl in the parent hub contract (see `../contracts/_MANIFEST.yaml`)
- Creating `crates/ferric-macros/` proc-macro crate
- Implementing the full `view!` macro per `design/ferric/authoring-model.md` §2
- Wiring ferric crate to depend on and re-export `view!`
- One git commit on `work/ferric-epic-authoring-r1` containing all changes

**Out of scope:**
- Test files under `crates/ferric-macros/tests/` (owned by parent's SUBTASK_tests)
- Any ferric crate changes other than Cargo.toml and src/lib.rs prelude wiring

---

## Shared inputs (read-only for all subtasks)

| Source | Location | Note |
|--------|----------|------|
| Specification §2 | `design/ferric/authoring-model.md` | Via `ssh … cat ~/nswe-demo/design/ferric/authoring-model.md` |
| VNode builder API | `crates/ferric/src/vdom.rs` | Frozen — read on branch via `git show origin/work/ferric-epic-authoring-r1:crates/ferric/src/vdom.rs` |
| Hub contract | `../contracts/_MANIFEST.yaml` | Ownership + identity assertions |
| This subtree contract | `contracts/_MANIFEST.yaml` | Per-child ownership |
| Branch tip | commit `1ccdce0` | Starting state |

---

## Task structure

```
SUBTASK_scaffold  ──→  SUBTASK_macro_impl ─────┐
                   └→  SUBTASK_wire  ───────────┴→  SUBTASK_synthesis
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_scaffold` | none | Create `crates/ferric-macros/` crate (Cargo.toml + stub lib.rs). Note: workspace already has `members = ["crates/*"]` glob — no root Cargo.toml change needed. | `crates/ferric-macros/Cargo.toml`, `crates/ferric-macros/src/lib.rs` (stub) |
| `SUBTASK_macro_impl` | `SUBTASK_scaffold` | Implement full `view!` proc-macro: parser, lowering table (§2.12 all 8 constructs), single-root validation (§2.10), 7 diagnostic cases (§2.9) | `crates/ferric-macros/src/lib.rs` (full impl, possibly + sub-modules) |
| `SUBTASK_wire` | `SUBTASK_scaffold` | Update `crates/ferric/Cargo.toml` (+dependency) and `crates/ferric/src/lib.rs` (+prelude re-export) | Updated ferric Cargo.toml, Updated ferric lib.rs |
| `SUBTASK_synthesis` | `SUBTASK_macro_impl`, `SUBTASK_wire` | Verify: `cargo build -p ferric-macros`, `cargo build -p ferric`, `cargo test -p ferric --lib` (37 tests pass). Create git commit referencing issue #139. | Git commit SHA on `work/ferric-epic-authoring-r1` |

### Dependency Graph

```
SUBTASK_scaffold ──→ SUBTASK_macro_impl ──┐
                 └──→ SUBTASK_wire ────────┴──→ SUBTASK_synthesis
```

---

## Subtree Methodology Posture

**Dominant task type:** Rust proc-macro implementation.

**Primary bundles:**
- `rust` — `Rust_Macros_And_Codegen_Methodology.md` (primary), `Rust_Library_Diagnostics_Methodology.md`, `Rust_Cargo_Ecosystem_Methodology.md`
- `compilers` — `Compiler_Parsing_Theory_Methodology.md`, `Compiler_Error_Diagnostics_Methodology.md`
- `synthesis` — SUBTASK_synthesis is a verification gate

**Cross-cutting bindings on all subtasks:**
- MSRV: stable Rust 1.82; no nightly features.
- Proc-macro deps: `proc-macro2`, `quote`, `syn` (features = ["full"]) only.
- Never put server address, SSH key path, user name, or host paths into committed files.
- Use SSH wrapper from project CLAUDE.md for all remote git/cargo operations.

---

## Contract

**Contract location:** `contracts/` (read-only for descendants)  
**Contract kind:** `ownership_map`  
**Manifest:** `contracts/_MANIFEST.yaml`

The seam between children is the crate name and macro name:
- Cargo package name: `ferric-macros`
- Rust crate name: `ferric_macros`
- Macro function name: `view`
- Crate path in workspace: `crates/ferric-macros`
