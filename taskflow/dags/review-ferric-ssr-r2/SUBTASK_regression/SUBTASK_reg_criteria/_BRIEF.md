# Task: Regression Criteria Check

## Task Specification

**Slug**: SUBTASK_reg_criteria  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

Check whether the ferric-ssr-r4 commits (`7fb90c7`, `e625c3f`, `75c1eef`) introduced any change that breaks or degrades the 9 previously-clean criteria from review-ferric-ssr-r1. Produce a findings document with a PASS/FAIL verdict and evidence for each criterion.

### Context

This task is a spoke of SUBTASK_regression (see `../_GLOBAL.md`). It covers ONLY the regression dimension — not security or code quality. Those are SUBTASK_sec_quality's concern.

**Criteria to check**:

| Criterion | What to verify |
|-----------|---------------|
| REQ-SSR-001 | No `web_sys` or DOM dependency in `ssr.rs`; new code from `7fb90c7` doesn't add any |
| REQ-SSR-002 | `impl Drop for ReactiveScope` still present and purges subscribers; new reactive usage in `app.rs` doesn't leak subscriptions during SSR |
| REQ-SSR-003 | VNode recursion in `ssr.rs` still unbounded — no new stack limit introduced |
| REQ-SSR-005 | `render_to_string` still a crate-root export in `lib.rs`; `ssr_handler` in chirp-server still calls it correctly |
| REQ-HYD-001 | Adopt-pass in `hydrate.rs` still reuses existing DOM nodes on matching paths — no `createElement` on matching paths |
| REQ-HYD-002 | Reactive updates post-hydration still use `create_effect → diff → apply_patches_impl` path; new `app.rs` wiring doesn't bypass this |
| REQ-HYD-004 | Marker format still type-level enforced: single import of marker constants from `ssr.rs`, no local copies in `hydrate.rs` or new code |
| REQ-MIS-001 | `assemble_document` still produces valid HTML5; no new string interpolation introduced by `ssr.rs` docstring fix in `7fb90c7` |
| REQ-MIS-002 | Mismatch detection+recovery in `hydrate.rs` still replaces mismatched nodes without structural corruption |

**Commits under review**: `7fb90c7` (app.rs hydrate dispatch + ssr.rs docstring fix), `e625c3f` (hydrate_wasm.rs wasm-bindgen tests), `75c1eef` (cfg(wasm32) gate on hydrate block + rustfmt fix)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Parent context | `../_GLOBAL.md` | Review scope, constraints |
| Findings schema | `../contracts/findings_schema.md` | Required output format |
| `ssr.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/ssr.rs?ref=work/ferric-ssr-r1` | REQ-SSR-001..003, REQ-MIS-001, REQ-HYD-004 (marker source) |
| `hydrate.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/hydrate.rs?ref=work/ferric-ssr-r1` | REQ-HYD-001, REQ-HYD-002, REQ-HYD-004, REQ-MIS-002 |
| `lib.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/lib.rs?ref=work/ferric-ssr-r1` | REQ-SSR-005 (crate-root export) |
| chirp-server handler | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/chirp-server/src/main.rs?ref=work/ferric-ssr-r1` or routes file | REQ-SSR-005 (ssr_handler call) |
| `app.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/chirp-frontend/src/app.rs?ref=work/ferric-ssr-r1` | REQ-SSR-002 (reactive scope), REQ-HYD-002 (hydrate wiring) |
| Changed files list | `gh pr view 228 --json files` | Confirm scope of ferric-ssr-r4 changes |

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `criteria_findings.md` |
| Location | `SUBTASK_reg_criteria/` (this workspace) |

The output MUST follow `../contracts/findings_schema.md`. It carries:
- **Criteria Results** section: one entry per REQ-ID with PASS/FAIL verdict and evidence at pinned commit `75c1eef`
- **What Was Examined and Found Clean** section: list each criterion checked with no finding

---

## Success Criteria

- [ ] All 9 criteria checked against the actual source files at `work/ferric-ssr-r1` (commit `75c1eef`)
- [ ] Each criterion has a PASS or FAIL verdict with evidence (file, line)
- [ ] Evidence cites the pinned commit `75c1eef` or the branch state at that commit
- [ ] `criteria_findings.md` written to this workspace in findings schema format

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: Code Review; Supporting: Rust, Framework Design

Specific files to load:
- `code-review/CodeReview_Process_Methodology.md` — review discipline; green is a claim not a proof; what isn't there
- `code-review/CodeReview_Checklist_Methodology.md` — per-concern checklist
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/browser security model, reactive scope, hydration
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR/hydration seam; reactive subscription lifecycle

These are the parent's suggestions. Load fewer if clearly inapplicable; load more as needed.

## Inherited Constraints

- Scope is ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT check B1 (REQ-HYD-003) or B2 (REQ-SSR-006) — those are separate tasks
- Do NOT re-raise non-blockers #229–#242 from prior review
- Evidence must cite file + line at pinned commit `75c1eef`
- Do not reference overseer escalation comments from I267

## Out-of-Scope

- Security surface (HTML injection, DOM spoofing) — that is SUBTASK_sec_quality
- Code quality of new code — that is SUBTASK_sec_quality
- Test sufficiency (B2's concern)
