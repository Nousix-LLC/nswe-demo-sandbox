# Task: Regression Check — 9 Previously-Clean Criteria

## Task Specification

**Slug**: SUBTASK_regression-check
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Verify that all 9 acceptance criteria found clean in review-ferric-ssr-r1 are still satisfied
after the ferric-ssr-r4 commits (`7fb90c7`, `e625c3f`, `75c1eef`) to `app.rs` and
`hydrate_wasm.rs`.

For each criterion: determine whether the new commits touch code relevant to it; if they do,
examine that code and confirm the criterion still holds; if they do not, record "unchanged —
no new code in this area."

### Context

This task is part of the SUBTASK_regression-quality-sec spoke of review-ferric-ssr-r2 (see
`../_GLOBAL.md`). Three sibling spokes run in parallel: this one (regression), SUBTASK_code-quality,
and SUBTASK_security. The synthesis task depends on all three.

**Previously-clean criteria to verify** (all 9 must pass):

| ID | Description |
|---|---|
| REQ-SSR-001 | `render_to_string` has no `web_sys`/DOM dependency; compiles on native |
| REQ-SSR-002 | Reactive scope isolated during SSR; `impl Drop for ReactiveScope` purges subscribers |
| REQ-SSR-003 | Nested VNode recursion in SSR is unbounded (no artificial cap) |
| REQ-SSR-004 | SSR/hydration markers defined once in `ssr.rs`, imported (not copied) by `hydrate.rs` |
| REQ-SSR-005 | `render_to_string` is a crate-root export; `chirp-server` can call it |
| REQ-HYD-001 | Adopt pass reuses existing DOM nodes — no `createElement` calls on matching paths |
| REQ-HYD-002 | Reactive updates after hydration use `create_effect → diff → apply_patches_impl` |
| REQ-HYD-004 | Marker format enforced at type level — single import, no local copies |
| REQ-MIS-001 | `assemble_document` produces valid HTML5 document fragment |
| REQ-MIS-002 | Mismatch detection+recovery replaces mismatched DOM nodes without structural corruption |

### Focus Areas for New Commits

Examine these criteria particularly carefully — the new commits may affect them:

- **REQ-SSR-004**: Did any commit copy SSR/hydration marker constants rather than importing from
  `ssr.rs`? Check that `hydrate_wasm.rs` test file uses constants via import, not literals.
- **REQ-SSR-005**: Does the new code touch `lib.rs`? Is `render_to_string` still exported?
- **REQ-HYD-001**: Did new code change the adopt pass in `hydrate.rs`?
- **REQ-HYD-002**: Did new code change the reactive update path in `hydrate.rs`?
- **REQ-HYD-004**: Did any new code add a local copy of the marker type?
- **REQ-MIS-001, REQ-MIS-002**: Did `assemble_document` or mismatch handling change?

For criteria the new commits do not touch, "unchanged — no new code in this area" with a brief
explanation is sufficient.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Project constraints and context |
| Parent hub | `../../_GLOBAL.md` | Full review context |
| PR #228 diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | See all changes in ferric-ssr-r4 commits |
| `ssr.rs` | `crates/ferric/src/ssr.rs` on branch | REQ-SSR-004 marker source of truth |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` on branch | REQ-HYD-001/002, REQ-MIS-002 |
| `lib.rs` | `crates/ferric/src/lib.rs` on branch | REQ-SSR-005 export |
| `app.rs` | `crates/chirp-frontend/src/app.rs` on branch | New entry-point code |
| `hydrate_wasm.rs` | `crates/ferric/tests/hydrate_wasm.rs` on branch | New test file |
| Issues #223, #224, #226 | GitHub (`gh issue view N --repo Nousix-LLC/nswe-demo`) | Requirement texts for criteria context |

**Note on reading source files**: Use `gh` or `git` to read files at the branch HEAD. Example:
```
gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/ssr.rs?ref=work/ferric-ssr-r1 \
  --jq '.content' | base64 -d
```
Or via SSH to the build server per CLAUDE.md.

---

## Output Specification

**File**: `regression-check.md`
**Location**: `SUBTASK_regression-check/`

The file must contain:

```markdown
# Regression Check — 9 Previously-Clean Criteria

## Summary

[Brief summary: N criteria PASS/UNCHANGED, M criteria FAIL]

## Per-Criterion Findings

### REQ-SSR-001 — [PASS | FAIL | UNCHANGED]
[What was checked; file:line if examined; finding]

### REQ-SSR-002 — [PASS | FAIL | UNCHANGED]
[...]

### REQ-SSR-003 — [...]
(one section per criterion — all 9)

## Overall Regression Verdict: [PASS | FAIL]

[If FAIL: list the specific criteria that failed and why]
```

---

## Success Criteria

- [ ] All 9 previously-clean criteria covered (one section each)
- [ ] Each finding states what was checked and whether the criterion holds
- [ ] Focus areas given appropriate depth (not just "looks fine")
- [ ] Overall PASS or FAIL verdict stated
- [ ] `regression-check.md` written to this task's workspace

---

## Suggested Methodology Files

**Task type**: "Code review" → Primary: `code-review`, Supporting: `rust`; also "Ferric PR review"

Specifically:
- `code-review/CodeReview_Process_Methodology.md` — systematic concern coverage
- `code-review/CodeReview_Checklist_Methodology.md` — regression checklist
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` —
  SSR/hydration correctness standards (for understanding what each criterion means)
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/wasm-bindgen patterns

These are suggested starting points. The child agent retains final judgment.

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- **Commits under inspection**: `7fb90c7`, `e625c3f`, `75c1eef`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text
- **Scope**: Regression check only — code quality and security are handled by sibling spokes
