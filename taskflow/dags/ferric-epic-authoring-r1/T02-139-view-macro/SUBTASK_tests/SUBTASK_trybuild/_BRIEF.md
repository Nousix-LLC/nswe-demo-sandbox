# _BRIEF.md — SUBTASK_trybuild: trybuild diagnostic fixtures for view!

**Slug**: SUBTASK_trybuild  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  

---

## Objective

Write the trybuild test runner (`tests/compile_fail.rs`) and all 7 fixture `.rs` files
(`tests/compile_fail/*.rs`) for the error cases in `design/ferric/authoring-model.md` §2.9.
Then run `TRYBUILD=overwrite cargo test -p ferric-macros` on the build server to generate and
commit the `.stderr` files. All 7 trybuild fixtures must pass as part of `cargo test`.

---

## Context

This task is part of the view! macro test suite (see `_GLOBAL.md` in the parent workspace,
at `../` relative to this brief).

**Dependencies**: none — runs concurrently with SUBTASK_conformance  
**Dependents**: SUBTASK_synthesis depends on this task's output

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Project constraints and methodology posture |
| Diagnostics spec | `design/ferric/authoring-model.md` §2.9 | 7 error cases with expected message vocabulary |
| Installed macro | `crates/ferric-macros/src/` (all source files) | Understand what errors the macro can produce |
| Hub contract | `../contracts/_MANIFEST.yaml` | Identity assertion I-DIAG-01 |

### Input Verification

Before writing any fixture code:
- [ ] Read authoring-model.md §2.9 fully (all 7 error cases with expected message vocabulary)
- [ ] Read the ferric-macros source to understand how errors are reported
- [ ] Check if trybuild is already a dev-dependency in `crates/ferric-macros/Cargo.toml`; if not, add it

---

## Process Specification

### Processing Steps

1. **Read §2.9 diagnostics spec.** Identify all 7 error cases and their expected message
   vocabulary. The messages must use author vocabulary (naming the element/tag/attribute the
   author wrote), not macro-internal identifiers (BAR-FERRIC-008 constraint).

2. **Add trybuild dev-dependency** (if not already present):
   ```toml
   [dev-dependencies]
   trybuild = "1"
   ```

3. **Write the trybuild runner** `tests/compile_fail.rs`:
   ```rust
   #[test]
   fn compile_fail() {
       let t = trybuild::TestCases::new();
       t.compile_fail("tests/compile_fail/*.rs");
   }
   ```

4. **Write one fixture `.rs` file per error case.** Each fixture must trigger exactly the
   intended error from §2.9. The 7 required fixture files:

   | Fixture file | Diagnostic category |
   |---|---|
   | `unclosed_element.rs` | Error at open tag span, naming the unclosed element |
   | `mismatched_close_tag.rs` | Error naming the open tag and the mismatching close tag |
   | `multiple_top_level.rs` | Error at second-sibling span, naming the single-root rule |
   | `dynamic_not_into_string.rs` | Type error at the `{expr}` span (expr not `Into<String>`) |
   | `unknown_event_name.rs` | Error naming the bad event and listing `click, input` |
   | `handler_not_closure.rs` | Error at the value span, naming that a closure is required |
   | `for_missing_key.rs` | Compile error flagging the absent `key` attribute on `<For>` |

   Each fixture is a minimal Rust file that invokes `view!{…}` in a way that triggers the
   intended error. Use `use ferric_macros::view;` or the full crate path as appropriate.

5. **Generate `.stderr` files via SSH:**
   ```bash
   ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
     'bash -lc "cd ~/nswe-demo && TRYBUILD=overwrite cargo test -p ferric-macros 2>&1"'
   ```
   This writes actual compiler output into each `tests/compile_fail/*.stderr` file.

6. **Inspect the generated `.stderr` files.** For each file:
   - If the diagnostic uses macro-internal language (e.g., references token-stream variable names
     or proc-macro implementation details rather than the author's tag/attribute names) → this is
     a BAR-FERRIC-008 violation. Note it and flag for SUBTASK_synthesis.
   - Otherwise, the `.stderr` file is correct as-is.

7. **Stage and verify** that the `.stderr` files are present and non-empty. Run:
   ```bash
   ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
     'bash -lc "cd ~/nswe-demo && cargo test -p ferric-macros --test compile_fail 2>&1"'
   ```
   All 7 fixtures must pass (trybuild reports PASS when the actual output matches the `.stderr`).

8. **Git-add the generated `.stderr` files.** The `.stderr` files must be committed — trybuild
   fixtures fail on CI when `.stderr` files are absent or stale.

### Quality Criteria

- [ ] Exactly 7 fixture `.rs` files, matching the names in the table above
- [ ] Each fixture triggers exactly the intended error (not a different error, not a compile success)
- [ ] All 7 `.stderr` files are generated on the build server (not hand-authored)
- [ ] All 7 trybuild fixtures pass (`cargo test -p ferric-macros --test compile_fail` is green)
- [ ] `.stderr` files are staged for commit (git add)
- [ ] Do NOT modify any file in `crates/ferric-macros/src/`

---

## Output Specification

### Primary Outputs

| Artifact | Location |
|----------|----------|
| Trybuild runner | `crates/ferric-macros/tests/compile_fail.rs` |
| Fixture: unclosed_element | `crates/ferric-macros/tests/compile_fail/unclosed_element.rs` + `.stderr` |
| Fixture: mismatched_close_tag | `crates/ferric-macros/tests/compile_fail/mismatched_close_tag.rs` + `.stderr` |
| Fixture: multiple_top_level | `crates/ferric-macros/tests/compile_fail/multiple_top_level.rs` + `.stderr` |
| Fixture: dynamic_not_into_string | `crates/ferric-macros/tests/compile_fail/dynamic_not_into_string.rs` + `.stderr` |
| Fixture: unknown_event_name | `crates/ferric-macros/tests/compile_fail/unknown_event_name.rs` + `.stderr` |
| Fixture: handler_not_closure | `crates/ferric-macros/tests/compile_fail/handler_not_closure.rs` + `.stderr` |
| Fixture: for_missing_key | `crates/ferric-macros/tests/compile_fail/for_missing_key.rs` + `.stderr` |

---

## Success Criteria

This task is complete when:

- [ ] `crates/ferric-macros/tests/compile_fail.rs` exists
- [ ] All 7 fixture `.rs` files exist under `tests/compile_fail/`
- [ ] All 7 `.stderr` files exist and were generated on the build server via `TRYBUILD=overwrite`
- [ ] `cargo test -p ferric-macros --test compile_fail` on the build server shows all 7 fixtures green
- [ ] Any BAR-FERRIC-008 violations identified and flagged for SUBTASK_synthesis
- [ ] No files in `crates/ferric-macros/src/` were modified

---

## Constraints

- Read §2.9 fully BEFORE writing any fixture code
- Do not modify `crates/ferric-macros/src/`
- Do not hand-author `.stderr` content — generate via `TRYBUILD=overwrite` on the build server
- SSH command form: `ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 'bash -lc "…"'`
- Never put server address, SSH key path, user name, or host paths into committed files

---

## Suggested Methodology Files

**Matched domain-mapping row:**  
Task type: "Writing tests" → Primary bundle: **Testing** | Supporting: **Core**, **Rust**  
Task type: "Rust testing" → Primary bundle: **Rust** | Supporting: **Testing**

**Specific methodology files to load:**

- `testing/Testing_Unit_Testing_Methodology.md` — for structuring the trybuild test runner and fixture design; rationale: trybuild fixtures are unit tests for compiler diagnostics
- `rust/Rust_Testing_Methodology.md` — covers trybuild and compile-fail testing patterns in Rust; rationale: trybuild is a Rust-specific testing tool, Rust_Testing_Methodology likely covers it
- `testing/Testing_Strategy_Methodology.md` — to ensure all 7 error cases are covered and each fixture is minimal and focused; rationale: need to cover all spec-mandated error cases

*The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.*

## Inherited Constraints

- Branch: `work/ferric-epic-authoring-r1`
- Do NOT modify any file in `crates/ferric-macros/src/`
- No server credentials in committed files
- Rust workspace rust-version is stable 1.82 — no nightly features
- BAR-FERRIC-008: Diagnostic messages must use author vocabulary, not macro-internal identifiers; flag violations for synthesis

## Out-of-Scope Methodologies

- `testing/Testing_Conformance_Against_External_Reference_Methodology.md` — conformance testing is SUBTASK_conformance's domain; this task focuses on compiler diagnostics
- `testing/Testing_E2E_Testing_Methodology.md` — tests run headlessly via cargo test, no browser
- `synthesis/Synthesis_Overview_Methodology.md` — synthesis is SUBTASK_synthesis's domain
