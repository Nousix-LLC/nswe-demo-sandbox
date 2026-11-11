# Task: B2 Verification — REQ-SSR-006 (wasm-bindgen-test coverage)

## Task Specification

**Slug**: SUBTASK_b2_verify  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

Verify that Blocker 2 (B2) from review-ferric-ssr-r1 is genuinely resolved: `wasm-bindgen-test` coverage now exists for the mismatch detection, warning, and recovery code paths in `hydrate.rs`, satisfying REQ-SSR-006 (and REQ-SSR-004, REQ-SSR-005 as named in the test descriptions).

### Context

Prior review-ferric-ssr-r1 found zero `wasm-bindgen-test` for `hydrate.rs`. Issues #224 and #226 are `release-gating: true` and explicitly require headless wasm-bindgen-test coverage.

Ferric-ssr-r4 commit `e625c3f` added `crates/ferric/tests/hydrate_wasm.rs` (197 lines) with 3 `#[wasm_bindgen_test]` functions:
- `hydrate_adopt_walk_no_structural_mutations` (REQ-SSR-004)
- `hydrate_event_wiring_post_hydration` (REQ-SSR-005)
- `hydrate_mismatch_detection_recovery` (REQ-SSR-006)

Commit `75c1eef` applied rustfmt to this file.

This task reads the actual test file and evaluates:
1. Whether each test function covers the stated code path substantively
2. Whether test assertions would catch real regressions (not just "it ran without panic")
3. Whether the mismatch detection + warning + recovery path (REQ-SSR-006) is specifically exercised
4. CI status confirmation
5. Code quality of the test file

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Shared review context |
| Verdict schema | `../contracts/verdict_schema.md` | Required output format |
| `hydrate_wasm.rs` | `crates/ferric/tests/hydrate_wasm.rs` in repo (branch `work/ferric-ssr-r1`) | The test file to evaluate |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` in repo | The code being tested |
| `ssr.rs` marker constants | `crates/ferric/src/ssr.rs` in repo | Used by tests (REQ-SSR-004) |
| CI run | https://github.com/Nousix-LLC/nswe-demo/actions/runs/42120246308 | Confirm pass/green |
| REQ-SSR-006 requirement | Issue #226 (GitHub) | The bar to verify against |

**How to access**: Use `gh` CLI:
- `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=work/ferric-ssr-r1`
- `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/hydrate.rs?ref=work/ferric-ssr-r1`
- `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/ssr.rs?ref=work/ferric-ssr-r1`
- `gh run view 42120246308` (or `gh api /repos/Nousix-LLC/nswe-demo/actions/runs/42120246308`)

---

## Review Focus

For B2 verification, evaluate:

1. **Test existence and structure**: Are the 3 test functions annotated `#[wasm_bindgen_test]`? Are they in a module with `wasm_bindgen_test::wasm_bindgen_test_configure!(run_in_browser);` or similar setup?

2. **`hydrate_adopt_walk_no_structural_mutations` (REQ-SSR-004)**:
   - Does it set up a DOM tree with server-rendered children?
   - Does it call `hydrate()` on that tree?
   - Does it assert that no `createElement` calls occurred (adopt walk, not fresh-mount walk)?
   - Would it fail if the adopt pass silently called `createElement`?

3. **`hydrate_event_wiring_post_hydration` (REQ-SSR-005)**:
   - Does it set up an SSR-rendered element with an expected event?
   - Does it call `hydrate()` and then trigger the event?
   - Does it assert that the event handler fires (reactive update path)?
   - Would it fail if event wiring was broken post-hydration?

4. **`hydrate_mismatch_detection_recovery` (REQ-SSR-006 — primary)**:
   - Does it deliberately introduce a structural mismatch between SSR HTML and the VDOM?
   - Does it call `hydrate()` with that mismatch?
   - Does it assert that (a) a warning is emitted, (b) the mismatch is recovered (mismatched node replaced), (c) the DOM is not left corrupted?
   - Is the warning assertion substantive (e.g., `expect_console_warn!` or similar) rather than just checking no panic?
   - Would this test fail if `detect_mismatch` returned early without replacing the node?

5. **Assertion depth**: Are the assertions checking behavioral outcomes (DOM shape, event callbacks, warning emission) or just calling `hydrate()` and checking it doesn't panic? A test that panics only on `unwrap()` is not substantive coverage.

6. **Code quality of test file**: Are the test helpers reusable? Is DOM setup verbose but correct? Are there any copy-paste error patterns?

7. **CI confirmation**: Was the CI run on commit `75c1eef`? Did wasm-pack / wasm-bindgen-test jobs pass?

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `b2_verdict.md` |
| Location | `SUBTASK_b2_verify/` (this workspace) |

The output MUST follow `../contracts/verdict_schema.md`. It carries:
- Verdict: `RESOLVED` or `NOT_RESOLVED`
- Requirements Covered: `REQ-SSR-006` (primary) plus `REQ-SSR-004`, `REQ-SSR-005` as covered by the test names
- Evidence: test file line numbers, assertion excerpts, CI status
- Findings: any shallow assertions, missing paths, or test quality issues
- What was examined and found clean

---

## Success Criteria

- [ ] `hydrate_wasm.rs` read in full
- [ ] `hydrate.rs` read to verify what the tests are actually exercising
- [ ] Each test function's assertions evaluated for behavioral depth
- [ ] Mismatch detection + recovery path specifically evaluated
- [ ] CI run status confirmed (pass/fail, which job)
- [ ] REQ-SSR-006 verdict stated clearly (RESOLVED / NOT_RESOLVED) with evidence
- [ ] `b2_verdict.md` written to this workspace in verdict schema format

---

## Suggested Methodology Files

**Task-type row matched**: "Rust testing" → Primary: Rust (Testing); "Ferric PR review" → Code Review

Specific files to load:
- `rust/Rust_Testing_Methodology.md` — `#[wasm_bindgen_test]` patterns, what constitutes real behavioral coverage vs. smoke test
- `testing/Testing_Unit_Testing_Methodology.md` — assertion depth, what a test must assert to catch a real regression
- `code-review/CodeReview_Checklist_Methodology.md` — the bar for evaluating test quality in a PR review
- `rust/Rust_WebAssembly_Browser_Methodology.md` — wasm-bindgen-test runner setup, browser vs. Node test environments

These are the parent's suggestions. Load fewer if clearly inapplicable; load more if your reading reveals additional surface.

## Inherited Constraints

- Bar for "genuine coverage" is: a test must fail when the specific behavior it claims to test is broken
- Shallow tests (call function, check no panic) are non-blockers at best if the behavior is otherwise unreachable in CI — but if the REQ explicitly requires headless wasm-bindgen-test for mismatch recovery and the test does not assert recovery, that is a blocker
- Do not re-raise #229–#242 as blockers
- Cite evidence at pinned commit (`75c1eef`)

## Out-of-Scope Methodologies

- `Architecture_*` — not an architecture review
- `Security_*` — security surface for WASM tests is minimal; brief note suffices if anything catches your eye
- `FrameworkDesign_UI_Reactivity_And_Rendering_Internals` — that's B1's methodology; B2 is test-quality focused
