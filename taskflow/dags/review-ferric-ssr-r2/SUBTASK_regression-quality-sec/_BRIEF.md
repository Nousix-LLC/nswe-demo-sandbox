# Task: Regression check, code quality, and security

## Task Specification

**Slug**: SUBTASK_regression-quality-sec
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Verify that the 9 previously-clean acceptance criteria remain satisfied after the ferric-ssr-r4
commits, review the code quality of all new/changed code, check for security issues (HTML
injection, escaping gaps) introduced by the new commits, and identify any fresh non-blocking
issues in the new code.

### Context

review-ferric-ssr-r1 found 9 of 11 criteria clean. The ferric-ssr-r4 commits (3 commits to
`app.rs` and `hydrate_wasm.rs`) may have introduced regressions or new issues. This task
verifies the unchanged criteria are still satisfied and applies standard quality and security
review to the new code.

**Previously-clean criteria (9 of 11)**:
- REQ-SSR-001: `render_to_string` no `web_sys`/DOM dep; compiles on native
- REQ-SSR-002: Reactive scope isolated during SSR; `impl Drop for ReactiveScope` purges subscribers
- REQ-SSR-003: Nested VNode recursion unbounded
- REQ-SSR-004: SSR/hydration markers defined once in `ssr.rs`, imported (not copied) by `hydrate.rs`
- REQ-SSR-005: `render_to_string` is a crate-root export; `chirp-server` can call it; `ssr_handler` calls correctly
- REQ-HYD-001: Adopt pass reuses existing DOM nodes — no `createElement` calls on matching paths
- REQ-HYD-002: Reactive updates after hydration use `create_effect → diff → apply_patches_impl`
- REQ-HYD-004: Marker format enforced at type level — single import, no local copies
- REQ-MIS-001: `assemble_document` produces valid HTML5 document fragment
- REQ-MIS-002: Mismatch detection+recovery replaces mismatched DOM nodes without structural corruption

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|---|---|---|
| PR #228 diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | See all changes |
| `app.rs` | `crates/chirp-frontend/src/app.rs` on branch | cfg-gate quality review |
| `hydrate_wasm.rs` | `crates/ferric/tests/hydrate_wasm.rs` on branch | Test quality review |
| `ssr.rs` | `crates/ferric/src/ssr.rs` on branch | REQ-SSR-004 marker source |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` on branch | REQ-HYD-001, REQ-HYD-002, REQ-MIS-002 |
| `lib.rs` (ferric crate root) | `crates/ferric/src/lib.rs` on branch | REQ-SSR-005 export |
| Issues #223, #224, #226 | GitHub | Requirement texts |
| Parent _GLOBAL.md | `../_GLOBAL.md` | Project context |

---

## Process Guidance

### Part 1: Regression check on 9 previously-clean criteria

For each criterion, verify it is still satisfied after the new commits. Focus on whether the
new code could have broken it — especially:

- **REQ-SSR-004**: Did any commit copy the SSR/hydration marker constants rather than importing
  from `ssr.rs`? Check `hydrate_wasm.rs` test file uses constants via import, not literals.
- **REQ-SSR-005**: Does the new code touch `lib.rs`? Is `render_to_string` still exported?
- **REQ-HYD-001**: Did new code change the adopt pass in `hydrate.rs`?
- **REQ-HYD-002**: Did new code change the reactive update path?
- **REQ-HYD-004**: Did new code add a local copy of the marker type?
- **REQ-MIS-001, REQ-MIS-002**: Did `assemble_document` or mismatch handling change?

For criteria the new commits do not touch, a brief "unchanged — no new code in this area"
is sufficient; don't re-examine what wasn't touched.

### Part 2: Code quality of new code

For `app.rs` (cfg-gate + conditional dispatch):
- Is the cfg-gate pattern idiomatic Rust? (`#[cfg(target_arch = "wasm32")]` placement, scope)
- Is the conditional dispatch (`if root.has_children()` or similar) correct and clear?
- Is error handling complete? What happens if `hydrate()` returns an error?
- Are there any docstring accuracy issues (prior issue: docstring fix in `ssr.rs` per commit)?
- Is the code readable and maintainable?

For `hydrate_wasm.rs` (test file):
- Test structure: are tests well-structured and well-named?
- Setup/teardown: DOM state properly cleaned up between tests?
- Hardcoded strings vs. imported constants?
- Duplication patterns?
- Any fresh non-blocking issues worth filing?

### Part 3: Security

- Does the new code introduce any HTML injection paths not present before?
- Does `assemble_document` or any path the new code touches have escaping gaps?
- Does the test file log or expose anything security-sensitive?
- Any new secrets, tokens, or sensitive data in the test setup?

### Part 4: Fresh non-blockers

If you find issues that are real but non-blocking (style nits, minor quality gaps, suggestions),
note them. Do NOT file GitHub issues — just list them in your verdict. The synthesis task will
decide whether to file them. Do NOT re-raise items #229–#242.

---

## Output Specification

**File**: `verdict-regression-quality-sec.md`
**Location**: `SUBTASK_regression-quality-sec/`

The file should contain:

```markdown
# Verdict — Regression, Code Quality, Security

## Regression Check: 9 Previously-Clean Criteria

### REQ-SSR-001 — [PASS | FAIL | UNCHANGED]
[What was checked; file:line if examined; finding]

### REQ-SSR-002 — [...]
...

(one section per criterion)

## Code Quality: New Code

### app.rs cfg-gate pattern
[Finding]

### hydrate_wasm.rs test file
[Finding]

## Security

[Findings or "No new HTML injection paths or escaping gaps introduced by the new commits"]

## Fresh Non-Blockers (if any)

[List of non-blocking issues found in new code, not previously filed, with file:line]

## Overall: [PASS | FAIL]

[If FAIL: list the specific blockers found in this area]
```

---

## Success Criteria

- [ ] All 9 previously-clean criteria checked (abbreviated where code unchanged is acceptable)
- [ ] Code quality checked for `app.rs` changes and `hydrate_wasm.rs`
- [ ] Security check complete
- [ ] Fresh non-blockers noted (or none found)
- [ ] Overall verdict (PASS or FAIL) stated
- [ ] `verdict-regression-quality-sec.md` written to this task's workspace

---

## Suggested Methodology Files

**Task type**: "Ferric PR review (Rust library)" → Primary: `code-review`, Supporting: `rust`,
`framework-design`; also "Security review" → Supporting: `security`

Specifically:
- `code-review/CodeReview_Process_Methodology.md` — systematic concern coverage
- `code-review/CodeReview_Checklist_Methodology.md` — regression and quality checklist
- `rust/Rust_Testing_Methodology.md` — Rust test quality standards
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/wasm-bindgen patterns
- `security/Security_Secure_Coding_Methodology.md` — HTML injection, escaping, XSS vectors
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` —
  SSR/hydration correctness standards

These are suggested; child agent retains final judgment.

## Inherited Constraints

- Repository: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- Commits under inspection: `7fb90c7`, `e625c3f`, `75c1eef`
- Do not re-raise previously filed non-blockers #229–#242
- Do not reference overseer I267 escalation comments
- Prose bar: no AI-tell patterns in output text
