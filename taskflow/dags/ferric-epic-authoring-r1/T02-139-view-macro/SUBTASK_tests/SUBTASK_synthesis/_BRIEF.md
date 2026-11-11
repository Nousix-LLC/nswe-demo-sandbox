# _BRIEF.md — SUBTASK_synthesis: Verification gate + commit for view! test suite

**Slug**: SUBTASK_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_conformance, SUBTASK_trybuild  
**Status**: Pending  

---

## Objective

This is the **verification gate** for the SUBTASK_tests sub-decomposition. It does NOT summarize
the spokes — it asserts that the combined output satisfies all identity assertions and meets the
parent brief's success criteria, then makes the single required commit. It runs the four-check
model and either completes with PASS (fold record written, commit made) or schedules remediation
fix-tasks (FAIL path).

---

## Context

This task is part of the view! macro test suite (see `_GLOBAL.md` in the parent workspace,
at `../` relative to this brief).

**Dependencies**: SUBTASK_conformance (lowering.rs), SUBTASK_trybuild (compile_fail.rs + fixtures + .stderr files)  
**Dependents**: none — this is the final task; its fold record (SYNTHESIS.md) closes the subtree

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Project constraints, identity assertions to verify |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Ownership + identity assertions I-LOWER-01, I-LOWER-02, I-DIAG-01 |
| Conformance tests | `crates/ferric-macros/tests/lowering.rs` | Output of SUBTASK_conformance |
| Trybuild runner | `crates/ferric-macros/tests/compile_fail.rs` | Output of SUBTASK_trybuild |
| Trybuild fixtures | `crates/ferric-macros/tests/compile_fail/` | All 7 `.rs` + `.stderr` files from SUBTASK_trybuild |
| Parent contract | `../../contracts/_MANIFEST.yaml` | T02-139-view-macro identity assertions |

---

## Process Specification — Four-Check Verification Gate

This task runs the four checks. If all checks pass, it commits and folds. If any check fails,
it schedules a remediation fix-task via `engine_amend_plan { add_task }` and reports `failed`.

### Check 1 — Behavioral-Contract Verification (I-LOWER-01, I-LOWER-02)

**Run the conformance test suite on the build server:**
```bash
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "cd ~/nswe-demo && cargo test -p ferric-macros --test lowering 2>&1"'
```

Assert:
- [ ] All conformance tests pass (exit code 0, no test failures)
- [ ] At least 10 tests exist covering all §2.12 rows (I-LOWER-01)
- [ ] The `<For>` test covers I-LOWER-02 (all_keyed, correct key values)

**If FAIL:** The conformance tests fail or don't cover all rows → schedule a remediation
fix-task on SUBTASK_conformance. Report `status="failed"`.

### Check 2 — Wiring Verification (I-DIAG-01)

**Run the full trybuild suite on the build server (WITHOUT TRYBUILD=overwrite):**
```bash
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "cd ~/nswe-demo && cargo test -p ferric-macros --test compile_fail 2>&1"'
```

Assert:
- [ ] Exactly 7 fixture `.rs` files exist in `tests/compile_fail/`
- [ ] All 7 trybuild fixtures pass (exit code 0)
- [ ] All 7 `.stderr` files are present and non-empty (I-DIAG-01)
- [ ] No fixture is listed as FAIL or missing .stderr in the trybuild output

**If FAIL:** Trybuild fixtures fail or .stderr files are absent/wrong → schedule remediation.

### Check 3 — Pre-existing test regression (I-ADDITIVE-01)

**Run the ferric library tests to verify no regression:**
```bash
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "cd ~/nswe-demo && cargo test -p ferric --lib 2>&1"'
```

Assert:
- [ ] All 37 pre-existing tests in `cargo test -p ferric --lib` still pass
- [ ] No compilation errors in the ferric crate

**If FAIL:** A regression was introduced → investigate and schedule fix.

### Check 4 — Code review

**Review the combined output:**
- [ ] `lowering.rs` reads clearly: test names are descriptive, assertions are unambiguous
- [ ] Fixture files are minimal (each triggers exactly one intended error, nothing extraneous)
- [ ] `.stderr` files use author vocabulary (not macro-internal language); if any use internal
  language (BAR-FERRIC-008), note in commit message and flag upward to T02-synthesis
- [ ] No server addresses, SSH key paths, user names, or host paths in committed files
- [ ] No files in `crates/ferric-macros/src/` were modified by either spoke

**If FAIL (BAR-FERRIC-008 violation):** Note in commit message, flag upward but do NOT block
the commit — BAR-FERRIC-008 is a flag for T02-synthesis, not a blocker for this gate.

### Commit (after all checks pass)

**Stage and commit all new/modified files:**
```bash
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "cd ~/nswe-demo && git add \
    crates/ferric-macros/tests/lowering.rs \
    crates/ferric-macros/tests/compile_fail.rs \
    crates/ferric-macros/tests/compile_fail/ \
    && git commit -m \"feat(ferric-macros): add view! conformance tests and trybuild suite (closes #139)\n\nAll §2.12 lowering table rows have passing native conformance tests.\nAll 7 trybuild diagnostic fixtures pass with committed .stderr files.\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>\" 2>&1"'
```

The commit message MUST reference issue #139 and state that the trybuild suite is complete.
If any BAR-FERRIC-008 violations were found in Check 4, add a note in the commit message body.

---

## Output Specification

### Primary Output

| Artifact | Location |
|----------|----------|
| Fold record | `../SYNTHESIS.md` (at the SUBTASK_tests workspace — fold location is the parent) |

The fold record (SYNTHESIS.md) is written at the fold location: `../SYNTHESIS.md` relative to
this task's workspace (i.e., at `SUBTASK_tests/SYNTHESIS.md`). This is the record that
`engine_resume_suspended` consumes to fold the SUBTASK_tests parent `SUSPENDED → COMPLETED`.

### Fold record structure

```markdown
# SYNTHESIS.md — SUBTASK_tests verification gate

## Gate Result: PASS

## Identity Assertions

- I-LOWER-01: SATISFIED — N conformance tests in lowering.rs; all pass
- I-LOWER-02: SATISFIED — <For> list test verifies all_keyed and correct keys
- I-DIAG-01: SATISFIED — 7 trybuild fixtures present and passing with committed .stderr files

## Pre-existing Test Regression

- I-ADDITIVE-01 (scope): cargo test -p ferric --lib — all 37 tests pass ✓

## Code Review Notes

- [any BAR-FERRIC-008 notes, or "none identified"]

## Commit

- Commit hash: [actual hash after commit]
- Files committed: [list]
```

---

## Success Criteria

This task is complete when:

- [ ] All four checks passed (or remediation fix-tasks scheduled on FAIL)
- [ ] `../SYNTHESIS.md` exists at the fold location with PASS verdict
- [ ] A single commit on `work/ferric-epic-authoring-r1` contains all new test files
- [ ] The commit message references issue #139 and states trybuild suite is complete

---

## Constraints

- Run all cargo commands on the build server via SSH (see project CLAUDE.md)
- Never put server address, SSH key path, user name, or host paths into committed files
- BAR-FERRIC-008 violations: note in commit message, flag upward but do NOT block
- The fold record MUST be written at `../SYNTHESIS.md` (the parent's workspace), not in this task's workspace

---

## Suggested Methodology Files

**Matched domain-mapping row:**  
Task type: "Synthesizing / verifying a hub-and-spoke decomposition" → Primary bundle: **Synthesis**  
Supporting: Code Review, Code Quality

**Specific methodology files to load:**

- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model and gate pass/fail decision; ALWAYS load first; rationale: this IS a synthesis/verification gate task
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify identity assertions I-LOWER-01, I-LOWER-02, I-DIAG-01 are satisfied; rationale: behavioral contract from ../contracts/_MANIFEST.yaml must be checked
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify all required test files are present and wired into the test runner; rationale: need to confirm no fixture is missing or unconnected
- `synthesis/Synthesis_Code_Review_Methodology.md` — code review of the combined test output; rationale: check test quality, BAR-FERRIC-008 compliance, absence of server credentials

*The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.*

## Inherited Constraints

- Branch: `work/ferric-epic-authoring-r1`
- Do NOT modify any file in `crates/ferric-macros/src/`
- No server credentials in committed files
- Commit message must reference issue #139

## Out-of-Scope Methodologies

- `testing/Testing_Unit_Testing_Methodology.md` — the spokes wrote the tests; this gate verifies them
- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — the two spokes wrote to disjoint files; duplication is not a concern here
