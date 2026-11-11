# Task: Code Quality Review — New Code

## Task Specification

**Slug**: SUBTASK_code-quality
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Review the code quality of all new and changed code introduced by the ferric-ssr-r4 commits
(`7fb90c7`, `e625c3f`, `75c1eef`). Focus on `app.rs` (cfg-gate + conditional dispatch) and
`hydrate_wasm.rs` (new test file, 197 lines).

### Context

This task is part of the SUBTASK_regression-quality-sec spoke of review-ferric-ssr-r2 (see
`../_GLOBAL.md`). It runs in parallel with SUBTASK_regression-check and SUBTASK_security.

The ferric-ssr-r4 commits add:
- A cfg-gate pattern and conditional `hydrate()` dispatch in `app.rs`
- A `hydrate_wasm.rs` test file (197 lines) using `wasm-bindgen-test`

This task does NOT cover security (HTML injection, escaping) — that is SUBTASK_security.
This task does NOT re-check acceptance criteria — that is SUBTASK_regression-check.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Project constraints and context |
| PR #228 diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | See all quality-relevant changes |
| `app.rs` | `crates/chirp-frontend/src/app.rs` on branch | cfg-gate quality review |
| `hydrate_wasm.rs` | `crates/ferric/tests/hydrate_wasm.rs` on branch | Test file quality review |

**Note on reading files**: Use `gh` API or SSH to the build server per CLAUDE.md:
```
gh api repos/Nousix-LLC/nswe-demo/contents/crates/chirp-frontend/src/app.rs?ref=work/ferric-ssr-r1 \
  --jq '.content' | base64 -d
```

---

## Process Guidance

### app.rs — cfg-gate and conditional dispatch

Review the following quality dimensions:

1. **cfg-gate idiom**: Is `#[cfg(target_arch = "wasm32")]` placed at the right scope? Is the
   pattern idiomatic Rust (attribute placement, cfg vs cfg_attr, conditional imports)?
2. **Conditional dispatch logic**: Is the `if root.has_children()` (or equivalent) check correct
   and clear? Is the condition semantically right for the SSR/hydrate vs mount decision?
3. **Error handling**: What happens when `hydrate()` returns an error? Is the error path complete?
4. **Docstring accuracy**: Does the function/module docstring accurately describe the new behavior?
5. **Readability**: Is the new code clear to a reader unfamiliar with the change?

### hydrate_wasm.rs — test file

Review the following:

1. **Test structure**: Are tests well-structured, well-named, and focused?
2. **Setup/teardown**: Is DOM state properly cleaned up between tests to prevent cross-test
   contamination?
3. **Hardcoded strings vs. imported constants**: Does the test file use SSR/hydration marker
   constants via import, or does it define them locally? Local copies are both a correctness
   risk (can diverge) and a REQ-SSR-004 concern.
4. **Duplication**: Are there repeated patterns that should be extracted into helpers?
5. **Assertion quality**: Do assertions check behavior or just that something ran? Would they
   catch a real regression?
6. **Any fresh non-blocking issues**: Note anything real but non-blocking.

---

## Output Specification

**File**: `code-quality.md`
**Location**: `SUBTASK_code-quality/`

The file must contain:

```markdown
# Code Quality Review — New Code

## app.rs — cfg-gate Pattern

### cfg-gate idiom
[Finding]

### Conditional dispatch logic
[Finding]

### Error handling
[Finding]

### Docstring accuracy
[Finding]

### Readability
[Finding]

## hydrate_wasm.rs — Test File

### Test structure and naming
[Finding]

### Setup/teardown and DOM cleanup
[Finding]

### Hardcoded strings vs. imported constants
[Finding]

### Duplication
[Finding]

### Assertion quality
[Finding]

## Fresh Non-Blockers (if any)

[List with file:line, or "None found"]

## Overall Code Quality Verdict: [PASS | FAIL]

[If FAIL: state what must be fixed and why it is a blocker]
```

---

## Success Criteria

- [ ] app.rs cfg-gate pattern reviewed across all five quality dimensions
- [ ] hydrate_wasm.rs test file reviewed across all five quality dimensions
- [ ] Fresh non-blockers noted (or "None found")
- [ ] Overall PASS or FAIL verdict stated
- [ ] `code-quality.md` written to this task's workspace

---

## Suggested Methodology Files

**Task type**: "Code review" → Primary: `code-review`, Supporting: `rust`; also "Rust testing"

Specifically:
- `code-review/CodeReview_Process_Methodology.md` — systematic quality coverage
- `code-review/CodeReview_Checklist_Methodology.md` — quality checklist
- `rust/Rust_Testing_Methodology.md` — Rust test quality standards (most relevant for hydrate_wasm.rs)
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/wasm-bindgen patterns
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` —
  SSR/hydration correctness (for understanding what the new code is trying to do)

These are suggested starting points. The child agent retains final judgment.

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- **Commits under inspection**: `7fb90c7`, `e625c3f`, `75c1eef`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text
- **Scope**: Code quality only — regression check is SUBTASK_regression-check; security is
  SUBTASK_security
- **Non-blockers**: List in this file only; synthesis task decides whether to file GitHub issues
