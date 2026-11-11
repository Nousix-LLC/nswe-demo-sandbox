# Task: Verify B2 — REQ-SSR-006 wasm-bindgen-test coverage

## Task Specification

**Slug**: SUBTASK_b2-verify
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Verify that blocker B2 (REQ-SSR-006) from review-ferric-ssr-r1 is genuinely resolved: confirm
that `crates/ferric/tests/hydrate_wasm.rs` contains `#[wasm_bindgen_test]` functions that
cover the mismatch detection, warning, and recovery code paths — not just any WASM test
existence, but tests that would catch a real regression in those specific paths.

### Context

**Prior blocker**: review-ferric-ssr-r1 found zero `wasm-bindgen-test` coverage for `hydrate.rs`.
Issues #224 and #226 (both `release-gating: true`) explicitly require headless wasm-bindgen-test
coverage.

**Remediation (ferric-ssr-r4)**:
- Commit `e625c3f`: `crates/ferric/tests/hydrate_wasm.rs` (197 lines) — 3 `#[wasm_bindgen_test]`
  functions:
  - `hydrate_adopt_walk_no_structural_mutations` (REQ-SSR-004)
  - `hydrate_event_wiring_post_hydration` (REQ-SSR-005)
  - `hydrate_mismatch_detection_recovery` (REQ-SSR-006)
- Commit `75c1eef`: rustfmt fix on `hydrate_wasm.rs`

**REQ-SSR-006 requirement**: `wasm-bindgen-test` coverage exists for mismatch detection,
warning, and recovery code paths.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|---|---|---|
| `hydrate_wasm.rs` full content | `gh api /repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=work/ferric-ssr-r1` | Examine the 3 test functions |
| `hydrate.rs` (the code under test) | `crates/ferric/src/hydrate.rs` on the branch | Understand what mismatch/recovery paths exist |
| `ssr.rs` (marker constants) | `crates/ferric/src/ssr.rs` on the branch | REQ-SSR-004 marker single-source check |
| Issue #226 | GitHub issue #226 | REQ-SSR-006 requirement text |
| Issue #224 | GitHub issue #224 | Requirement for `release-gating: true` wasm-bindgen-test |
| CI run result | https://github.com/Nousix-LLC/nswe-demo/actions/runs/42120246308 | 7 CI checks green |
| Parent _GLOBAL.md | `../_GLOBAL.md` | Project context and constraints |

---

## Process Guidance

Read `hydrate_wasm.rs` and `hydrate.rs` in full. Then for each of the 3 test functions:

1. **Code path coverage**: Which code path(s) in `hydrate.rs` does this test exercise? Is the
   mismatch detection path specifically exercised by `hydrate_mismatch_detection_recovery`?

2. **Assertion quality**: Does the assertion check observable behavior (the DOM state after
   hydration, event handler firing, error/warning emission) or only that something ran without
   panic? A test that passes even when the mismatch code is deleted is not covering that path.

3. **REQ-SSR-006 specifically**: Does `hydrate_mismatch_detection_recovery` exercise mismatch
   *detection*, *warning* (or logging), and *recovery* as 3 distinct things, or only one?
   Would the test fail if mismatch recovery was broken (node replaced incorrectly or not at all)?

4. **REQ-SSR-004 and REQ-SSR-005**: `hydrate_adopt_walk_no_structural_mutations` and
   `hydrate_event_wiring_post_hydration` — do they test the stated behaviors? Are the assertions
   behavioral?

5. **Test infrastructure**: Is the wasm-bindgen-test setup correct (test harness, appropriate
   feature flags, correct target config)? Would CI actually execute these tests headlessly?

6. **Mismatch code existence**: Does `hydrate.rs` actually contain mismatch detection, warning,
   and recovery code? (If the tests exist but the code paths don't, that's a different problem.)

Report the finding:
- PASS: for each test, what it covers and that the assertions are behavioral
- FAIL (blocker): what is missing or insufficient, what would satisfy this finding

---

## Output Specification

**File**: `verdict-b2.md`
**Location**: `SUBTASK_b2-verify/`

The file should contain:

```markdown
# B2 Verdict — REQ-SSR-006: wasm-bindgen-test coverage

## Verdict: [PASS | FAIL]

## Finding — hydrate_adopt_walk_no_structural_mutations

[Code path, assertion quality, REQ-SSR-004 coverage, file:line citations]

## Finding — hydrate_event_wiring_post_hydration

[Code path, assertion quality, REQ-SSR-005 coverage, file:line citations]

## Finding — hydrate_mismatch_detection_recovery

[Code path, assertion quality, REQ-SSR-006 mismatch+warning+recovery coverage, file:line]

## CI Execution Status

[Would CI actually run these headlessly? Any test-infra concerns?]

## If FAIL: Blocker

[Requirement ID, what is missing, what would satisfy this finding]

## If PASS: What Was Clean

[What specifically was verified — this is the record of examination]
```

---

## Success Criteria

- [ ] `hydrate_wasm.rs` read in full
- [ ] `hydrate.rs` read to understand mismatch code paths
- [ ] All 3 test functions covered with specific file:line citations
- [ ] REQ-SSR-006 mismatch detection+warning+recovery specifically addressed
- [ ] Assertion quality evaluated (behavioral vs. execution-only)
- [ ] Verdict is PASS or FAIL
- [ ] `verdict-b2.md` written to this task's workspace

---

## Suggested Methodology Files

**Task type**: "Rust code review" / "Ferric PR review (Rust library)" → Primary: `code-review`,
Supporting: `rust`, `framework-design`

Specifically:
- `code-review/CodeReview_Process_Methodology.md` — systematic test review; "green is a claim,
  not a proof" discipline
- `code-review/CodeReview_Checklist_Methodology.md` — test coverage checklist
- `rust/Rust_Testing_Methodology.md` — wasm-bindgen-test mechanics, Rust test quality standards
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM test execution, wasm-bindgen-test
  harness, headless test CI patterns

These are suggested starting points; child agent retains final judgment.

## Inherited Constraints

- Repository: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- Commit under inspection: `e625c3f` (the B2-relevant commit), `75c1eef` (rustfmt)
- Do not re-raise previously filed non-blockers #229–#242
- Do not reference overseer I267 escalation comments
- Prose bar: no AI-tell patterns in output text
