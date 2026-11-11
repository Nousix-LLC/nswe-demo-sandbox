# Task: B1 Verification — REQ-HYD-003 (hydrate() wiring)

## Task Specification

**Slug**: SUBTASK_b1_verify  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

Verify that Blocker 1 (B1) from review-ferric-ssr-r1 is genuinely resolved: `hydrate()` must now be called from the WASM entry point when the root already has server-rendered children, satisfying REQ-HYD-003.

### Context

Prior review-ferric-ssr-r1 found that `crates/chirp-frontend/src/app.rs::start()` called `ferric::dom::mount(root, app)` unconditionally, never `ferric::hydrate(root, app)`, making SSR+hydration non-functional end-to-end.

Ferric-ssr-r4 delivered two commits that touch app.rs:
- `7fb90c7`: replaced unconditional `mount(root, app)` with conditional `ferric::hydrate(root, app)` / `mount` based on whether root has children
- `75c1eef`: added `#[cfg(target_arch = "wasm32")]` gate on the hydrate block

This task reads the actual changed code and verifies:
1. The conditional dispatch logic is functionally correct (calls `hydrate` when root has children, `mount` when it does not)
2. The `cfg(target_arch = "wasm32")` gate is correct and not over-broad
3. REQ-HYD-003 is fully satisfied — no residual gap
4. Code quality and correctness of the new code in app.rs

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Shared review context, constraints, verdict schema |
| Verdict schema | `../contracts/verdict_schema.md` | Required output format |
| PR diff | GitHub PR #228, Nousix-LLC/nswe-demo | See which lines changed |
| `app.rs` current content | `crates/chirp-frontend/src/app.rs` in repo | Verify wiring logic |
| `ferric::hydrate` / `ferric::dom::mount` signatures | ferric crate source | Confirm the right function is called |
| REQ-HYD-003 requirement | Issue #224 (GitHub) | The bar to verify against |

**How to access the repo**: The repository is at `git@github.com:Nousix-LLC/nswe-demo.git` or use the GitHub CLI (`gh`) to read file contents at HEAD of `work/ferric-ssr-r1`.

Suggested approach:
1. `gh pr view 228 --json commits,files` to see which files changed
2. `gh api repos/Nousix-LLC/nswe-demo/contents/crates/chirp-frontend/src/app.rs?ref=work/ferric-ssr-r1` to read the file (or Bash with git)
3. `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/lib.rs?ref=work/ferric-ssr-r1` to read ferric's public API

---

## Review Focus

For B1 verification, examine:

1. **Dispatch logic**: Does `start()` now check whether the root has server-rendered children before choosing between `hydrate()` and `mount()`? Is the check semantically correct (e.g., `root.has_child_nodes()` or `root.children().length() > 0`)?

2. **cfg-gate correctness**: Is `#[cfg(target_arch = "wasm32")]` the right gate? Does it accidentally exclude the hydrate path in some valid WASM deployment scenario? Is it correctly scoped (only the conditional block, not too much)?

3. **Function identity**: Is it calling `ferric::hydrate(root, app)` (the actual hydration path with adopt-walk) or some other function? Is it importing from the right module?

4. **End-to-end completeness**: After this change, does a client-side boot with an SSR-rendered root actually trigger hydration? Or is there still a code path where `mount` is called instead when it shouldn't be?

5. **Code quality**: Is the conditional logic clear? Are there edge cases (empty root due to whitespace nodes, etc.)? Is the error handling adequate?

6. **REQ-HYD-003 satisfaction**: The requirement states: "`hydrate()` is called from the WASM entry point when the root already has server-rendered children." Does the new code satisfy this literally and completely?

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `b1_verdict.md` |
| Location | `SUBTASK_b1_verify/` (this workspace) |

The output MUST follow `../contracts/verdict_schema.md`. It carries:
- Verdict: `RESOLVED` or `NOT_RESOLVED`
- Requirements Covered: at minimum `REQ-HYD-003`
- Evidence: specific file paths, line numbers, code excerpts
- Findings: any new issues with severity, location, principle, resolution
- What was examined and found clean

---

## Success Criteria

- [ ] `app.rs` read in full (or the relevant changed section)
- [ ] `ferric::hydrate` signature verified (correct function called)
- [ ] Conditional dispatch logic verified as functionally correct
- [ ] `cfg(target_arch = "wasm32")` gate evaluated for correctness
- [ ] REQ-HYD-003 verdict stated clearly (RESOLVED / NOT_RESOLVED) with evidence
- [ ] Any new issues documented with file + line + resolution
- [ ] `b1_verdict.md` written to this workspace in verdict schema format

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: Code Review; Supporting: Rust, Framework Design

Specific files to load:
- `code-review/CodeReview_Process_Methodology.md` — the overall review discipline (evidence over assertion, severity is honesty, what isn't there)
- `code-review/CodeReview_Checklist_Methodology.md` — per-concern checklist for Rust code review
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/browser binding patterns, `cfg` gate conventions, wasm-bindgen patterns
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR + hydration internals, what correct hydration wiring looks like

These are the parent's suggestions based on the task type. Load fewer if clearly inapplicable; load more if your reading of the brief reveals additional surface.

## Inherited Constraints

- Bar is REQ-HYD-003 exactly as stated in issue #224 — do not expand or narrow it
- Do not re-litigate prior-approved code not changed by ferric-ssr-r4 commits
- Do not re-raise non-blockers #229–#242 as blockers
- Security surface for this task: check whether the conditional (e.g., `has_child_nodes()`) could be spoofed by injected DOM nodes before the WASM boots — brief note suffices if no issue found
- Cite evidence at the pinned commit (`75c1eef`)

## Out-of-Scope Methodologies

- `Testing_Strategy_Methodology.md` — test coverage is B2's concern, not this task's
- `Architecture_*` — this is a targeted code verification, not an architecture review
