# _BRIEF.md — SUBTASK_synthesis: verification gate + commit

**Task ID:** ferric-authoring-139-view-impl-synthesis  
**Hub:** SUBTASK_impl  
**Task Kind:** synthesis  
**Depends on:** SUBTASK_macro_impl, SUBTASK_wire

---

## Objective

This task is a **verification gate**, not a prose summary. Run the four-check model against the combined
outputs of SUBTASK_scaffold + SUBTASK_macro_impl + SUBTASK_wire, assert all identity assertions from
`contracts/_MANIFEST.yaml`, then create the git commit on `work/ferric-epic-authoring-r1`.

PASS = all identities hold AND commit created.  
FAIL = any identity fails → remediation required before commit.

---

## Inputs

| Input | Location |
|-------|----------|
| Hub context | `../_GLOBAL.md` |
| Hub contract | `../contracts/_MANIFEST.yaml` (identity assertions to verify) |
| Parent hub contract | `../../contracts/_MANIFEST.yaml` (identity assertions IA4, IA6) |
| Sibling outputs | All files in `crates/ferric-macros/` and updated ferric files on branch |
| Design spec §2 | `design/ferric/authoring-model.md` §2 — oracle for behavioral verification |

Access branch state via SSH. Run cargo commands on the server:
```
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "cd ~/nswe-demo && git checkout work/ferric-epic-authoring-r1 && cargo build -p ferric-macros 2>&1"'
```

---

## Verification Checks

### Check 1 — Compilation (I-BUILD-01, I-BUILD-02)

```
cargo build -p ferric-macros   # must succeed, no errors
cargo build -p ferric           # must succeed, no errors  
```

Both must exit 0 on stable Rust 1.82. If either fails: FAIL — file `FAILURE.md`, report failure.

### Check 2 — Existing test suite (I-TEST-01, I-ADDITIVE-01)

```
cargo test -p ferric --lib      # must show 37 tests PASSED, 0 FAILED
```

Pre-existing tests must all pass. No new test failures allowed. If any test fails: FAIL.

### Check 3 — Lowering coverage (I-LOWER-ALL)

Verify by reading `crates/ferric-macros/src/lib.rs` (and sub-modules) that all 8 construct rows from
§2.12 are present in the implementation:
- DOM element open/close and self-closing
- Text literals → `vdom::text("…")`
- `{expr: Into<String>}` → `vdom::text(expr)`
- `{expr: VNode}` → child splice
- `{vec}` / `<For>` → `.children(iter)`
- Attributes (static and dynamic) → `.attr("name", value)`
- `key={e}` → `.key(e)`
- `on:click={h}` / `on:input={h}` → `.on(EventKind::…, h)`

If any row is missing: FAIL.

### Check 4 — Diagnostic coverage (I-DIAG-ALL) + Export check (I-EXPORT-01)

Verify by reading the implementation that all 7 §2.9 diagnostic cases are handled with span-accurate
author-vocabulary errors. Verify that `pub use ferric_macros::view;` is present in the ferric prelude.

If diagnostics are missing or export is absent: FAIL.

---

## Declared Outputs

On PASS:
1. Git commit on `work/ferric-epic-authoring-r1` containing all changes from SUBTASK_scaffold,
   SUBTASK_macro_impl, and SUBTASK_wire.
   - Commit message must state which §2.12 constructs are implemented and reference issue #139.
   - Format: "feat(ferric-macros): implement view! macro with [constructs list] (#139)" plus body
2. `SYNTHESIS.md` at this task workspace (the fold record)

On FAIL:
1. `FAILURE.md` documenting which assertion failed and what was observed

---

## Commit message format

The commit message must reference issue #139 and enumerate the §2.12 constructs implemented:

```
feat(ferric-macros): implement view! macro (#139)

Introduces the `ferric-macros` proc-macro crate with the `view!` declarative
macro. All §2.12 lowering constructs are implemented:

- DOM elements (open/close and self-closing)
- Text literals → vdom::text
- Interpolated expressions ({expr: Into<String>}, {expr: VNode})
- Vec<VNode> and <For each key let:ident> keyed list form
- Attributes: static ("v") and dynamic ({expr})
- key={e} → .key(e)
- on:click and on:input event handlers
- Component invocation (capitalized tag)

Implements 7 compile-time diagnostic cases per §2.9 (span-accurate,
author-vocabulary errors).

Wires view! into ferric::prelude via ferric-macros dependency.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

---

## Success Criteria

1. All 7 identity assertions in `contracts/_MANIFEST.yaml` hold (see Verification Checks).
2. `cargo build -p ferric-macros` and `cargo build -p ferric` exit 0.
3. `cargo test -p ferric --lib` shows 37 tests PASSED, 0 FAILED.
4. Git commit created on `work/ferric-epic-authoring-r1` with the correct message format.
5. `SYNTHESIS.md` authored at this workspace describing the verification outcome.

---

## Constraints

- This task writes NO implementation code. It verifies and commits only.
- If any check fails, author `FAILURE.md` and report `status="failed"` — do not create a partial commit.
- Use `git diff HEAD` to review changes before committing; ensure only owned artifacts are staged.
- Never put server address, SSH key path, user name, or host paths into committed files or commit messages.
- The commit message MUST end with:
  ```
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
  ```

---

## Suggested Methodology Files

**Task-type row:** "Synthesizing / verifying a hub-and-spoke decomposition" → Primary: `synthesis`

- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model, go/no-go decision, SYNTHESIS.md
  schema; this task IS a synthesis gate
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify that the ferric prelude correctly
  wires the macro export (I-EXPORT-01) and the Cargo.toml correctly lists the dependency
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify all identity assertions in
  `contracts/_MANIFEST.yaml` are satisfied
- `rust/Rust_Cargo_Ecosystem_Methodology.md` — cargo build/test invocation, understanding exit codes
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — git commit discipline, staging, commit messages

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load
these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Commit on `work/ferric-epic-authoring-r1` from SUBTASK_wire's tip (all prior changes already on branch).
- Commit message must reference issue #139.
- Attribution line required: `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- Branch must be CI-ready after the commit (builds clean, tests pass).
