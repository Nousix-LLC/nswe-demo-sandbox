# SUBTASK_tests — view! macro test suite

## Project Context

**Status**: Active  
**Hub**: T02-139-view-macro  
**Branch**: `work/ferric-epic-authoring-r1`  
**Parent contract**: `../contracts/_MANIFEST.yaml`

### Objective

Write a complete test suite for the `view!` macro on top of the implementation committed by
SUBTASK_impl. This subtree is split into two independent authoring concerns (conformance tests
and trybuild diagnostic fixtures), plus a synthesis gate that verifies all identity assertions
and makes the single required commit.

### Scope

**In Scope:**
- Native conformance tests that assert structural equality between `view!{…}` and hand-built VNode trees for every row in authoring-model.md §2.12
- trybuild diagnostic fixtures for all 7 error cases in authoring-model.md §2.9, with committed `.stderr` files generated on the build server
- Final `cargo test -p ferric-macros` verification, identity-assertion gate, and commit

**Out of Scope:**
- Any modification to `crates/ferric-macros/src/` (owned by SUBTASK_impl)
- Any modification to `crates/ferric/src/` beyond what spec requires for tests

### Success Criteria

- [ ] `cargo test -p ferric-macros` passes with all conformance tests green
- [ ] All 7 trybuild fixtures pass (requires committed `.stderr` files)
- [ ] `cargo test -p ferric --lib` (37 pre-existing tests) still passes
- [ ] Identity assertions I-LOWER-01, I-LOWER-02, I-DIAG-01 all satisfied
- [ ] Single commit on `work/ferric-epic-authoring-r1` containing exactly the new/modified test files

---

## Constraints and Requirements

### Technical Constraints

- **Do not modify `crates/ferric-macros/src/`** — that is SUBTASK_impl's domain (owned artifact boundary)
- **`.stderr` files MUST be generated on the build server** via `TRYBUILD=overwrite cargo test -p ferric-macros`, not hand-authored
- **Never put server address, SSH key path, user name, or host paths into committed files**
- SSH command form: `ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 'bash -lc "…"'`
- Read `design/ferric/authoring-model.md` §2.12 and §2.9 fully before writing any test code
- If a `.stderr` file uses macro-internal language (BAR-FERRIC-008 violation), note it in the commit message and flag for SUBTASK_synthesis

### Inherited Constraints from Parent

- Branch: `work/ferric-epic-authoring-r1` — all work on this branch
- Closes issue #139
- Identity assertions I-LOWER-01, I-LOWER-02, I-DIAG-01 are from `../contracts/_MANIFEST.yaml` and must be satisfied

---

## Input Specifications

### Primary Data Sources

| Source | Location | Format | Description |
|--------|----------|--------|-------------|
| Lowering table (oracle) | `design/ferric/authoring-model.md` §2.12 | Markdown | Each row is a conformance test case |
| Diagnostics spec | `design/ferric/authoring-model.md` §2.9 | Markdown | 7 error cases with expected message vocabulary |
| VNode equality | `crates/ferric/src/vdom.rs` | Rust | Check if VNode/VElement derive PartialEq |
| Installed macro | `crates/ferric-macros/` | Rust | The implementation — read to understand lowering |
| Parent contract | `../contracts/_MANIFEST.yaml` | YAML | Identity assertions I-LOWER-01, I-LOWER-02, I-DIAG-01 |

---

## Task Structure

### Overview

```
_GLOBAL.md (this document)
├── contracts/_MANIFEST.yaml            (this subtree's ownership + identities)
├── SUBTASK_conformance/_BRIEF.md       (write tests/lowering.rs)
├── SUBTASK_trybuild/_BRIEF.md          (write compile_fail.rs + fixtures + generate .stderr)
└── SUBTASK_synthesis/_BRIEF.md         (verification gate + commit)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_conformance` | none | Write native conformance tests for all §2.12 lowering table rows | `crates/ferric-macros/tests/lowering.rs` |
| `SUBTASK_trybuild` | none | Write trybuild runner + 7 fixtures + generate `.stderr` via SSH | `tests/compile_fail.rs`, `tests/compile_fail/*.rs`, `tests/compile_fail/*.stderr` |
| `SUBTASK_synthesis` | `SUBTASK_conformance`, `SUBTASK_trybuild` | Verification gate: run cargo test, check identity assertions, commit | `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_conformance ──┐
                      ├── SUBTASK_synthesis
SUBTASK_trybuild    ──┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)  
**Contract kind**: `behavioral_spec`

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | behavioral_spec | File ownership between spokes; identity assertions this synthesis verifies |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `crates/ferric-macros/tests/lowering.rs` | `SUBTASK_conformance` |
| `crates/ferric-macros/tests/compile_fail.rs` | `SUBTASK_trybuild` |
| `crates/ferric-macros/tests/compile_fail/*.rs` | `SUBTASK_trybuild` |
| `crates/ferric-macros/tests/compile_fail/*.stderr` | `SUBTASK_trybuild` |
| `SYNTHESIS.md` (fold record) | `SUBTASK_synthesis` |

### Identities

Synthesis must assert ALL of the following before PASS:

- [ ] I-LOWER-01: All §2.12 lowering rows have passing native conformance tests (view!{...} == hand-built VNode)
- [ ] I-LOWER-02: `<For>` list form produces all_keyed Vec<VNode> with correct key values
- [ ] I-DIAG-01: Exactly 7 trybuild fixtures present, all pass, .stderr files committed and matching CI toolchain output
- [ ] Cargo test -p ferric-macros passes with all tests green
- [ ] Cargo test -p ferric --lib (37 pre-existing tests) still passes

---

## Subtree Methodology Posture

**Dominant task type:** Writing tests (Testing bundle primary)  
**Primary bundles:** Testing, Rust  
**Cross-cutting bindings:** All children read authoring-model.md §2.12/§2.9 as the oracle spec

---

## Output Specifications

| Deliverable | Format | Location |
|-------------|--------|----------|
| Conformance tests | Rust | `crates/ferric-macros/tests/lowering.rs` |
| Trybuild runner | Rust | `crates/ferric-macros/tests/compile_fail.rs` |
| Trybuild fixtures | Rust + text | `crates/ferric-macros/tests/compile_fail/` |
| Final commit | git | `work/ferric-epic-authoring-r1` |
| Fold record | Markdown | `SUBTASK_tests/SYNTHESIS.md` |
