# Task: Regression + Code Quality + Security

## Task Specification

**Slug**: SUBTASK_regression  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

Verify that the 9 previously-clean criteria from review-ferric-ssr-r1 remain clean after ferric-ssr-r4's commits; apply code quality and security bars to the new/changed code; identify any fresh non-blockers introduced by the new commits.

### Context

Review-ferric-ssr-r1 found 9 of 11 criteria clean. The 2 blockers (B1, B2) are covered by SUBTASK_b1_verify and SUBTASK_b2_verify. This task covers the remaining 9:

**Issue #223 — SSR render_to_string (REQ-SSR-001 through REQ-SSR-003, REQ-SSR-005)**
- REQ-SSR-001: `render_to_string` has no `web_sys` or DOM dependency; compiles/runs on native host
- REQ-SSR-002: Reactive scope is isolated during SSR; no leaked subscriptions after render (`impl Drop for ReactiveScope`)
- REQ-SSR-003: Nested component VNode recursion is unbounded (arbitrarily deep component trees render)
- REQ-SSR-005: `render_to_string` is a crate-root export; `chirp-server` can call it without explicit path; `ssr_handler` calls correctly

**Issue #224 — Hydration (REQ-HYD-001, REQ-HYD-002, REQ-HYD-004)**
- REQ-HYD-001: Adopt pass reuses existing DOM nodes — no `createElement` calls on matching paths
- REQ-HYD-002: Reactive updates after hydration use the same `create_effect → diff → apply_patches_impl` path as `dom::mount`
- REQ-HYD-004: Marker format is enforced at the type level — single import, no local copies

**Issue #226 — SSR mismatch detection (REQ-MIS-001, REQ-MIS-002)**
- REQ-MIS-001: `assemble_document` produces a valid HTML5 document fragment the browser will parse
- REQ-MIS-002: Mismatch detection+recovery replaces mismatched DOM nodes without structural corruption

Note: REQ-SSR-004 is covered by the wasm-bindgen-test named in B2's scope (markers defined once in `ssr.rs`, imported in `hydrate.rs`).

**Security focus**: Any new HTML injection paths or escaping gaps introduced by the new commits.

**Code quality**: The new/changed code in `app.rs` and `hydrate_wasm.rs` — correctness, clarity, edge cases.

**Fresh non-blockers**: If the new commits introduce new issues beyond B1/B2, file them. Do NOT re-raise #229–#242.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Review scope, constraints |
| Verdict schema | `../contracts/verdict_schema.md` | Required output format |
| `ssr.rs` | `crates/ferric/src/ssr.rs` (branch `work/ferric-ssr-r1`) | REQ-SSR-001..003, REQ-SSR-005, REQ-MIS-001, marker constants |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` | REQ-HYD-001, REQ-HYD-002, REQ-HYD-004, REQ-MIS-002 |
| `lib.rs` | `crates/ferric/src/lib.rs` | REQ-SSR-005 (crate-root export) |
| `ssr_handler` in chirp-server | e.g. `crates/chirp-server/src/main.rs` or routes | REQ-SSR-005 (how ssr_handler calls render_to_string) |
| `app.rs` | `crates/chirp-frontend/src/app.rs` | Quality + security of changed code |
| Changed files list | `gh pr view 228 --json files` | Know what else changed |
| Issues #223, #224, #226 | GitHub | Requirement text if needed |

**How to access**:
```
gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/ssr.rs?ref=work/ferric-ssr-r1
gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/hydrate.rs?ref=work/ferric-ssr-r1
gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/lib.rs?ref=work/ferric-ssr-r1
gh pr view 228 --json files,commits
```

---

## Review Focus

### Regression checks (verify unchanged by new commits)

For each criterion, the question is: do the ferric-ssr-r4 commits (`7fb90c7`, `e625c3f`, `75c1eef`) introduce any change that breaks or degrades it?

- **REQ-SSR-001**: Does any import in `ssr.rs` pull in `web_sys` or DOM? Did any new code add DOM dependencies to the SSR path? (Check the new docstring fix in `ssr.rs` from `7fb90c7` for any content changes beyond doc.)
- **REQ-SSR-002**: `impl Drop for ReactiveScope` — still present and purges subscribers? Did any new reactive usage in `app.rs` create a subscription that leaks during SSR?
- **REQ-SSR-003**: VNode recursion — still unbounded depth? No new stack limit introduced?
- **REQ-SSR-005**: `render_to_string` still a crate-root export in `lib.rs`? `chirp-server`'s `ssr_handler` still calls it correctly?
- **REQ-HYD-001**: Adopt-pass still uses existing DOM nodes on matching paths? New test `hydrate_adopt_walk_no_structural_mutations` is a data point, but verify the implementation in `hydrate.rs`.
- **REQ-HYD-002**: Reactive updates post-hydration still use `create_effect → diff → apply_patches_impl`? New app.rs wiring doesn't bypass this?
- **REQ-HYD-004**: Marker format still type-level enforced? Only one import of marker constants (from `ssr.rs`), no local copies in `hydrate.rs` or new code?
- **REQ-MIS-001**: `assemble_document` still produces valid HTML5? No new string interpolation introduced by `ssr.rs` docstring fix?
- **REQ-MIS-002**: Mismatch detection+recovery still replaces mismatched nodes without corruption? New test covers this, but verify the implementation in `hydrate.rs` hasn't changed in a way that breaks it.

### Security

- **HTML injection in `ssr.rs`**: Does `render_to_string` or any helper called from it escape user-controlled content before inserting into the HTML string? Any new string interpolation introduced by ferric-ssr-r4 commits?
- **DOM spoofing in `app.rs`**: The new conditional (`root.has_child_nodes()` or similar) — could an attacker inject DOM children before WASM boots to force hydration on a non-SSR page? What's the threat model and is it in scope for this library?
- **Test injection safety**: Does `hydrate_wasm.rs` construct any DOM from user-controlled string input? Any `innerHTML` assignments in tests?

### Code quality

- **`app.rs` new code**: Is the conditional hydrate/mount dispatch readable and correct? Are there edge cases the comment/docstring should acknowledge? Any dead code?
- **`hydrate_wasm.rs` new code**: Test helper quality, assertion clarity, copy-paste patterns. (B2 covers assertion depth; this task covers style/structure quality.)
- **Fresh non-blockers from new code**: Any naming issues, documentation gaps, or patterns from #229–#242 reappearing in NEW code (not previously filed code — filing only genuinely new instances).

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `regression_verdict.md` |
| Location | `SUBTASK_regression/` (this workspace) |

The output MUST follow `../contracts/verdict_schema.md`. It carries:
- Verdict: `PASS` (all 9 criteria clean) or `FAIL` (at least one criterion degraded)
- Requirements Covered: REQ-SSR-001..003, REQ-SSR-005, REQ-HYD-001, REQ-HYD-002, REQ-HYD-004, REQ-MIS-001, REQ-MIS-002
- Evidence per criterion
- Findings (security / code quality / fresh non-blockers)
- What was examined and found clean (required — name each criterion)

---

## Success Criteria

- [ ] All 9 previously-clean criteria checked against new commits
- [ ] Security surface checked (HTML injection in SSR path, DOM spoofing in hydrate dispatch)
- [ ] Code quality assessed for new/changed code in `app.rs` and `hydrate_wasm.rs`
- [ ] Verdict stated for each criterion with evidence
- [ ] Any fresh non-blockers documented with file + line + resolution
- [ ] `regression_verdict.md` written to this workspace in verdict schema format

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: Code Review; Supporting: Rust, Security

Specific files to load:
- `code-review/CodeReview_Process_Methodology.md` — the review discipline; green is a claim not a proof; what isn't there
- `code-review/CodeReview_Checklist_Methodology.md` — per-concern checklist
- `security/Security_Secure_Coding_Methodology.md` — HTML injection, escaping, trust boundaries
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/browser security model, DOM manipulation safety
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR escaping and hydration seam security

These are the parent's suggestions. Load fewer if clearly inapplicable; load more as needed.

## Inherited Constraints

- Regression check covers ONLY the 9 previously-clean criteria — do not recheck B1/B2 (those are SUBTASK_b1_verify and SUBTASK_b2_verify)
- Do not re-raise #229–#242; file only genuinely new instances of issues in new code
- Security surface is bounded to ferric-ssr-r4's changes — not a full security audit of the whole PR
- Cite evidence at pinned commit (`75c1eef`)

## Out-of-Scope Methodologies

- `Testing_Strategy_Methodology.md` — test sufficiency is B2's concern; this task checks functional correctness of tested behavior
- `Architecture_*` — not an architecture review
