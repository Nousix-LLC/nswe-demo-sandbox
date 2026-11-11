# _BRIEF.md — SUBTASK_conformance: Native conformance tests for view! lowering

**Slug**: SUBTASK_conformance  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  

---

## Objective

Write `crates/ferric-macros/tests/lowering.rs` — a `#[test]` function for every row in
`design/ferric/authoring-model.md` §2.12 (the lowering table) — asserting that `view!{…}` and
the hand-built `VElement`/`vdom::text` builder chain produce structurally equal `VNode` values.
Tests must run via `cargo test -p ferric-macros` without a browser.

---

## Context

This task is part of the view! macro test suite (see `_GLOBAL.md` in the parent workspace,
at `../` relative to this brief).

**Dependencies**: none — runs concurrently with SUBTASK_trybuild  
**Dependents**: SUBTASK_synthesis depends on this task's output

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Project constraints and methodology posture |
| Lowering table (oracle) | `design/ferric/authoring-model.md` §2.12 | Each row is one test case |
| VNode equality | `crates/ferric/src/vdom.rs` | Check if VNode/VElement derive/impl PartialEq |
| Installed macro | `crates/ferric-macros/src/` (all source files) | Understand the actual lowering implementation |
| Hub contract | `../contracts/_MANIFEST.yaml` | Identity assertions I-LOWER-01, I-LOWER-02 |

### Input Verification

Before writing any test code:
- [ ] Read authoring-model.md §2.12 fully (all rows of the lowering table)
- [ ] Read `crates/ferric/src/vdom.rs` to determine if `VNode`/`VElement` implement `PartialEq`
- [ ] Read the ferric-macros source to understand what lowering was actually implemented

---

## Process Specification

### Processing Steps

1. **Read the lowering table** (§2.12). Enumerate every row — each is one test case. Note all
   the forms: static text, dynamic text/attr, nested elements, event handlers, component elements,
   the `<For>` list form, etc.

2. **Check VNode equality support.** Inspect `crates/ferric/src/vdom.rs`:
   - If `VNode`/`VElement` derive/impl `PartialEq`, use `assert_eq!` directly.
   - If not, write a recursive `vnode_eq(a: &VNode, b: &VNode) -> bool` helper, or
     assert on `format!("{:?}", ...)` forms — whatever makes equality unambiguous and readable.
   Document the approach chosen with a brief comment in the test file.

3. **Write one `#[test]` function per lowering-table row.** Name tests descriptively
   (e.g. `test_static_text`, `test_dynamic_attribute`, `test_nested_element`, `test_for_list`).
   Each test asserts that `view!{<the form>}` equals the hand-built equivalent.

4. **For the `<For>` list form (I-LOWER-02)**: assert that every node in the produced `Vec<VNode>`
   is a `VNode::Element` with a non-`None` key equal to the expected key. This satisfies
   I-LOWER-02 from the contracts manifest.

5. **Verify the tests compile and pass.** Run via SSH:
   ```bash
   ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
     'bash -lc "cd ~/nswe-demo && cargo test -p ferric-macros --test lowering 2>&1"'
   ```
   All tests must be green.

### Quality Criteria

- [ ] One test per row in §2.12 lowering table (minimum 10 tests per the parent brief)
- [ ] Tests run without a browser or any JS runtime
- [ ] `assert_eq!` or equivalent helper used — equality must be unambiguous
- [ ] No use of `unwrap()` on test infrastructure; test helper panics should have descriptive messages
- [ ] Do NOT modify any file in `crates/ferric-macros/src/`

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `lowering.rs` |
| Format | Rust integration test |
| Location | `crates/ferric-macros/tests/` |

### Output Structure

```rust
//! Conformance tests for the view! macro lowering table (authoring-model.md §2.12).
//!
//! Each test asserts structural equality between the view!{...} form and the
//! equivalent hand-built VElement/vdom::text builder chain.

use ferric_macros::view;
use ferric::vdom::{VNode, VElement};

// If VNode does not implement PartialEq, include a vnode_eq helper here.

#[test]
fn test_static_text() { ... }

#[test]
fn test_dynamic_text() { ... }

// ... one test per §2.12 row ...

#[test]
fn test_for_list_all_keyed() {
    // Satisfies I-LOWER-02: every node has a non-None key equal to key_fn(item)
    ...
}
```

---

## Success Criteria

This task is complete when:

- [ ] `crates/ferric-macros/tests/lowering.rs` exists and is syntactically valid Rust
- [ ] `cargo test -p ferric-macros --test lowering` on the build server shows all tests green
- [ ] All §2.12 rows are covered by at least one test
- [ ] The `<For>` test satisfies I-LOWER-02 (all_keyed, correct key values)
- [ ] No files in `crates/ferric-macros/src/` were modified

---

## Constraints

- Read the spec and macro source BEFORE writing any test code
- Do not modify `crates/ferric-macros/src/` — that is SUBTASK_impl's domain
- Use the SSH command form for all remote cargo operations (see project CLAUDE.md)
- Never put server address, SSH key path, user name, or host paths into committed files

---

## Suggested Methodology Files

**Matched domain-mapping row:**  
Task type: "Writing tests" → Primary bundle: **Testing** | Supporting: **Core**, **Rust**  
Task type: "Rust testing" → Primary bundle: **Rust** | Supporting: **Testing**

**Specific methodology files to load:**

- `testing/Testing_Unit_Testing_Methodology.md` — for structuring unit/integration test assertions; rationale: conformance tests are integration-style unit tests verifying exact output equality
- `testing/Testing_Conformance_Against_External_Reference_Methodology.md` — the oracle (§2.12 table) is an external reference we do not own; rationale: each row is a spec-driven test case authored from the spec, not from the implementation
- `testing/Testing_Strategy_Methodology.md` — to ensure test coverage of all lowering forms; rationale: need to ensure every spec row is covered
- `rust/Rust_Testing_Methodology.md` — Rust-specific testing patterns (trybuild is a sibling concern, but cargo test integration structure matters here too); rationale: this is Rust code using cargo test

*The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.*

## Inherited Constraints

- Branch: `work/ferric-epic-authoring-r1`
- Do NOT modify any file in `crates/ferric-macros/src/`
- No server credentials in committed files
- Rust workspace rust-version is stable 1.82 — no nightly features

## Out-of-Scope Methodologies

- `testing/Testing_E2E_Testing_Methodology.md` — tests run headlessly via cargo test, no browser
- `testing/Testing_Mocking_Stubbing_Methodology.md` — not needed; the view! macro is deterministic, no mocking required
- `synthesis/Synthesis_Overview_Methodology.md` — synthesis is SUBTASK_synthesis's domain, not this spoke
