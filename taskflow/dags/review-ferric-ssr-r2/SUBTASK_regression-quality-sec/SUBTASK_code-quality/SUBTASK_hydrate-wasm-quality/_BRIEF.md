# Task: hydrate_wasm.rs Test Quality Review

## Task Specification

**Slug**: SUBTASK_hydrate-wasm-quality
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Review the code quality of `hydrate_wasm.rs`, a 197-line test file added by the ferric-ssr-r4
commits, covering five quality dimensions: test structure and naming, setup/teardown and DOM
cleanup, hardcoded strings vs. imported constants, duplication, and assertion quality. Produce
`hydrate-wasm-notes.md` with a severity-labeled finding per dimension.

### Context

This task is part of SUBTASK_code-quality (see `../_GLOBAL.md`). It runs in parallel with
SUBTASK_app-rs-quality. The synthesis task SUBTASK_quality-synthesis reads this task's output
and SUBTASK_app-rs-quality's output to produce the final `code-quality.md`.

`hydrate_wasm.rs` is a new `wasm-bindgen-test` file that tests the hydration behavior added in
`app.rs`. It runs in a real browser context (wasm-pack test with --headless). Tests must
correctly set up and tear down DOM state so they do not contaminate each other.

A key concern flagged in the parent brief: if the test file uses locally-defined string
constants for SSR/hydration markers rather than importing them from production code, those
constants can diverge silently and produce false passes (REQ-SSR-004 concern).

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Project constraints and subtree-wide context |
| Parent hub | `../../_GLOBAL.md` | Broader review context and inherited constraints |
| PR #228 diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | Full diff to identify what was added in hydrate_wasm.rs |
| `hydrate_wasm.rs` | branch `work/ferric-ssr-r1`, path `crates/ferric/tests/hydrate_wasm.rs` | Primary file for review |
| `ssr.rs` | branch `work/ferric-ssr-r1`, path `crates/ferric/src/ssr.rs` | To determine whether SSR marker constants are defined here and importable |

**Reading files via gh API**:
```bash
gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=work/ferric-ssr-r1 \
  --jq '.content' | base64 -d

gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/ssr.rs?ref=work/ferric-ssr-r1 \
  --jq '.content' | base64 -d
```

**Reading the PR diff**:
```bash
gh pr diff 228 --repo Nousix-LLC/nswe-demo
```

---

## Quality Dimensions to Review

Review `hydrate_wasm.rs` across these five dimensions:

### 1. Test structure and naming
Are tests well-structured, well-named, and focused on one behavior each? Do test names describe
what behavior is being verified (e.g., `hydrate_with_ssr_content_uses_existing_dom` rather than
`test1`)? Is there any test that covers multiple behaviors and should be split?

### 2. Setup/teardown and DOM cleanup
Is DOM state properly cleaned up between tests? `wasm-bindgen-test` runs tests in the same
browser context — a test that mutates the DOM without cleanup contaminates subsequent tests.
Check whether each test that inserts DOM elements removes or resets them before returning (or
whether a cleanup helper is used consistently).

### 3. Hardcoded strings vs. imported constants
Does the test file define its own string constants for SSR/hydration markers (e.g., the
"data-ferric-ssr" attribute name or the SSR marker text), or does it import them from
production code (`ssr.rs` or `hydrate.rs`)? Local copies are a correctness risk: they can
diverge from production values and produce false passes. This is also a REQ-SSR-004 concern
if the test is intended to verify the SSR marker behavior.

### 4. Duplication
Are there repeated patterns across test cases that should be extracted into helper functions?
Is setup logic copy-pasted into multiple tests when it could be a `setup()` helper?

### 5. Assertion quality
Do assertions check behavior or just that something ran? Would they catch a real regression?
For example: does the test for hydration check that the existing DOM nodes were reused
(not replaced), or only that no error was returned? Does an assertion that the SSR marker
was removed actually verify the marker is gone from the DOM, or just that the function returned
Ok?

---

## Output Specification

**File**: `hydrate-wasm-notes.md`
**Location**: `SUBTASK_hydrate-wasm-quality/`

The file MUST follow the finding-note format defined in `../contracts/_MANIFEST.yaml`:

```markdown
# hydrate_wasm.rs Quality Notes

## Test structure and naming

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [file:line or N/A]

[Finding text — plain voice, concrete, citable]

## Setup/teardown and DOM cleanup

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [file:line or N/A]

[Finding text]

## Hardcoded strings vs. imported constants

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [file:line or N/A]

[Finding text]

## Duplication

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [file:line or N/A]

[Finding text]

## Assertion quality

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [file:line or N/A]

[Finding text]

## Fresh Non-Blockers (if any)

[List with file:line, or "None found"]
```

**Severity semantics**:
- **Blocker**: Must be fixed before the PR can merge; would cause a production defect, incorrect
  behavior, test-suite unreliability, or violated contract (e.g., hardcoded strings that diverge
  from production values, DOM contamination that invalidates test results).
- **Warning**: Should be fixed; a real quality concern but not an immediate defect risk.
- **Pass**: The dimension checks out; nothing to fix.

---

## Success Criteria

- [ ] All five quality dimensions assessed with severity and evidence
- [ ] The hardcoded-strings dimension specifically checks whether SSR marker constants are
      imported from production code or redefined locally, and cites the specific lines
- [ ] The DOM cleanup dimension checks all test functions, not just the first one
- [ ] Each finding cites specific file:line from the branch (or "N/A" for structural absences)
- [ ] Fresh non-blockers noted or "None found" stated
- [ ] `hydrate-wasm-notes.md` written to this task's workspace

---

## Suggested Methodology Files

**Task type**: "Rust testing" + "Rust code review" → Primary: `rust`, `code-review`

| File | Rationale |
|---|---|
| `rust/Rust_Testing_Methodology.md` | Primary methodology for this task — Rust test quality standards including test naming, assertion quality, and test isolation; most directly applicable to all five quality dimensions |
| `rust/Rust_WebAssembly_Browser_Methodology.md` | wasm-bindgen-test framework specifics — necessary for evaluating DOM cleanup patterns and browser test isolation conventions |
| `code-review/CodeReview_Process_Methodology.md` | Systematic concern coverage — ensures all five test quality dimensions are examined without stopping at the first finding |
| `code-review/CodeReview_Checklist_Methodology.md` | Quality checklist for reviewing test code — particularly the assertion quality and duplication checks |

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD
load these as a starting point but is the final judge of what its work requires — load fewer if
some are clearly inapplicable; load more if the brief reveals additional methodology surface the
parent did not anticipate.

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- **Commits under inspection**: `7fb90c7`, `e625c3f`, `75c1eef`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text (no moral adjectives on metrics, no narrated
  candor, no slot-fill templates, no padding filler)
- **Scope**: Code quality only — security (HTML injection, escaping) belongs to SUBTASK_security

## Out-of-Scope Methodologies

- `security/Security_Secure_Coding_Methodology.md` — security concerns (XSS, injection) are
  SUBTASK_security's scope
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` —
  useful for context on SSR/hydration but the app.rs review (SUBTASK_app-rs-quality) is the
  primary consumer of this file; load it here only if the hardcoded-strings dimension requires
  deeper understanding of what the SSR markers represent
