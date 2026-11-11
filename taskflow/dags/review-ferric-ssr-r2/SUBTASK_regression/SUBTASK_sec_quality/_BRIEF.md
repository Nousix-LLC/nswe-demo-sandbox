# Task: Security Surface and Code Quality

## Task Specification

**Slug**: SUBTASK_sec_quality  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

Assess the security surface and code quality of new/changed code introduced by the ferric-ssr-r4 commits (`7fb90c7`, `e625c3f`, `75c1eef`). Identify any HTML injection paths, DOM spoofing risks, or code quality issues in `app.rs` and `hydrate_wasm.rs`. File fresh non-blockers if any new issues appear in new code.

### Context

This task is a spoke of SUBTASK_regression (see `../_GLOBAL.md`). It covers security and code quality only — not the 9 regression criteria. Those are SUBTASK_reg_criteria's concern.

**Security concerns to check**:
- HTML injection in `ssr.rs`: Does `render_to_string` or any helper escape user-controlled content before inserting into the HTML string? Any new string interpolation introduced by ferric-ssr-r4 commits (specifically the docstring fix in `7fb90c7`)?
- DOM spoofing in `app.rs`: The new conditional (`root.has_child_nodes()` or similar) — could an attacker inject DOM children before WASM boots to force hydration on a non-SSR page? What is the threat model and is it in scope for this library?
- Test injection safety: Does `hydrate_wasm.rs` construct any DOM from user-controlled string input? Any `innerHTML` assignments in tests?

**Code quality concerns to check**:
- `app.rs` new conditional hydrate/mount dispatch: readable and correct? Edge cases the comment/docstring should acknowledge? Dead code?
- `hydrate_wasm.rs` new code: test helper quality, assertion clarity, copy-paste patterns
- Fresh non-blockers from new code: any naming issues, documentation gaps, or patterns from #229–#242 reappearing in new code (file only genuinely new instances, not previously filed code)

**Commits under review**: `7fb90c7` (app.rs hydrate dispatch + ssr.rs docstring fix), `e625c3f` (hydrate_wasm.rs wasm-bindgen tests), `75c1eef` (cfg(wasm32) gate + rustfmt fix)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Parent context | `../_GLOBAL.md` | Review scope, constraints |
| Findings schema | `../contracts/findings_schema.md` | Required output format |
| `ssr.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/ssr.rs?ref=work/ferric-ssr-r1` | HTML injection surface, escaping checks, docstring change |
| `app.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/chirp-frontend/src/app.rs?ref=work/ferric-ssr-r1` | DOM spoofing check, code quality of new hydrate dispatch |
| `hydrate_wasm.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=work/ferric-ssr-r1` | Test injection safety, code quality |
| Changed files list | `gh pr view 228 --json files` | Confirm what files ferric-ssr-r4 touched |

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `sec_quality_findings.md` |
| Location | `SUBTASK_sec_quality/` (this workspace) |

The output MUST follow `../contracts/findings_schema.md`. It carries:
- **Security Findings** section: for each security concern checked, result (Clean or Finding) with evidence
- **Code Quality Findings** section: enumerated findings with severity, location, description, resolution; or "No code quality findings"
- **What Was Examined and Found Clean** section: list each security/quality concern examined with no finding

---

## Success Criteria

- [ ] HTML injection surface checked (render_to_string escaping, new string interpolations)
- [ ] DOM spoofing risk assessed (has_child_nodes conditional in app.rs)
- [ ] Test injection safety checked (innerHTML, user-controlled DOM in hydrate_wasm.rs)
- [ ] Code quality assessed for app.rs new code and hydrate_wasm.rs
- [ ] Fresh non-blockers documented (file + line) or explicitly confirmed absent
- [ ] Evidence cites file + line at pinned commit `75c1eef`
- [ ] `sec_quality_findings.md` written to this workspace in findings schema format

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: Code Review; Supporting: Rust, Security

Specific files to load:
- `security/Security_Secure_Coding_Methodology.md` — HTML injection, escaping, trust boundaries
- `code-review/CodeReview_Process_Methodology.md` — review discipline; what isn't there; evidence over assertion
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/browser security model, DOM manipulation safety
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR escaping and hydration seam security

These are the parent's suggestions. Load fewer if clearly inapplicable; load more as needed.

## Inherited Constraints

- Scope is ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT re-raise non-blockers #229–#242 from prior review; file only genuinely new instances in new code
- Evidence must cite file + line at pinned commit `75c1eef`
- Security surface is bounded to HTML injection in SSR path and DOM spoofing in hydrate dispatch — not a full security audit
- Do not reference overseer escalation comments from I267

## Out-of-Scope

- The 9 regression criteria (REQ-SSR-001..003, REQ-SSR-005, REQ-HYD-001, REQ-HYD-002, REQ-HYD-004, REQ-MIS-001, REQ-MIS-002) — those are SUBTASK_reg_criteria
- Test sufficiency (B2's concern)
- Architecture review
