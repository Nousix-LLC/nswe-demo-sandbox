# Task: Security Surface Analysis — ferric-ssr-r4

## Task Specification

**Slug**: SUBTASK_sec_check  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

Review the security surface of the three files changed by ferric-ssr-r4 commits (`7fb90c7`, `e625c3f`, `75c1eef`): check HTML injection risk in `ssr.rs`, DOM spoofing risk in `app.rs`, and test injection safety in `hydrate_wasm.rs`. Produce `security_raw_findings.md` with one entry per concern.

### Context

This task is a spoke of SUBTASK_sec_quality (see `../_GLOBAL.md`). It covers security concerns only — code quality is SUBTASK_quality_check's concern.

**Security concerns to check**:

1. **HTML injection in `ssr.rs`**: Does `render_to_string` or any helper escape user-controlled content before inserting into the HTML string? Does the docstring fix in `7fb90c7` introduce any new string interpolation into the SSR output? Check the escaping strategy for all points where user data could enter the HTML string.

2. **DOM spoofing in `app.rs`** (`7fb90c7`): The new conditional (`root.has_child_nodes()` or similar check) decides whether to hydrate vs. mount fresh. Could an attacker inject DOM children before WASM boots, forcing hydration on a non-SSR page? Assess the threat model: is this a realistic attack surface for a Rust WASM UI library shipped as a crate (not a served page), and does the conditional's behavior in the malicious-children case represent a security or correctness boundary?

3. **Test injection safety in `hydrate_wasm.rs`** (`e625c3f`): Does any test helper construct DOM from user-controlled string input (e.g., `innerHTML` assignments, `insertAdjacentHTML`)? Check all DOM construction in the new test file for injection patterns.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Parent context | `../_GLOBAL.md` | Review scope and constraints |
| Spoke output schema | `../contracts/spoke_output_schema.md` | Required output format for security_raw_findings.md |
| `ssr.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/ssr.rs?ref=work/ferric-ssr-r1` | HTML injection surface, escaping checks |
| `app.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/chirp-frontend/src/app.rs?ref=work/ferric-ssr-r1` | DOM spoofing check — has_child_nodes conditional |
| `hydrate_wasm.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=work/ferric-ssr-r1` | Test injection safety |
| Changed files list | `gh pr view 228 --json files` | Confirm scope of ferric-ssr-r4 changes |

**Note**: Retrieve file content via `gh api … | python3 -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"` to decode the base64 response.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `security_raw_findings.md` |
| Location | `SUBTASK_sec_check/` (this workspace) |

The output MUST follow `../contracts/spoke_output_schema.md` §SUBTASK_sec_check. It carries:
- `## Security Findings` section with one subsection per concern (HTML Injection in ssr.rs, DOM Spoofing in app.rs, Test Injection Safety in hydrate_wasm.rs)
- Each subsection: **Result** (Clean or Finding), **Evidence** (file:line at commit `75c1eef`), **Finding** only if applicable

Security concerns found clean belong in the `## What Was Examined and Found Clean` stub at the bottom (this stub feeds SUBTASK_synthesis's assembly).

---

## Success Criteria

- [ ] HTML injection surface fully checked (render_to_string, all string interpolation points, docstring fix)
- [ ] DOM spoofing risk assessed with threat-model reasoning (is it in scope for a crate library?)
- [ ] Test injection safety verified (no innerHTML or user-controlled DOM construction in hydrate_wasm.rs)
- [ ] Evidence cites file + line at pinned commit `75c1eef`
- [ ] `security_raw_findings.md` written conforming to spoke_output_schema.md

---

## Suggested Methodology Files

**Task-type row matched**: "Security review" → Primary: Security; Supporting: Code Review  
Also applicable: "Ferric PR review (Rust library)" → Primary: Code Review; Supporting: Rust, Security

Specific files to load:
- `security/Security_Secure_Coding_Methodology.md` — HTML injection, escaping, trust boundaries, secure-by-default principles; directly applies to checking render_to_string escaping
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/browser security model, DOM manipulation safety; applies to the has_child_nodes conditional and test DOM construction
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR escaping and hydration seam security; applies to both ssr.rs and the app.rs hydration conditional
- `code-review/CodeReview_Process_Methodology.md` — evidence over assertion; reading for what isn't there (missing escaping, missing guard)

These are the parent's suggested methodologies. Load fewer if clearly inapplicable; load more as needed.

## Inherited Constraints

- Scope is ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT re-raise non-blockers #229–#242; file only genuinely new instances in new code
- Evidence must cite file + line at pinned commit `75c1eef`
- Security surface is bounded to HTML injection in SSR path and DOM spoofing in hydrate dispatch — not a full security audit
- Do not reference overseer escalation comments from I267

## Out-of-Scope

- Code quality concerns (naming, readability, dead code) — those are SUBTASK_quality_check
- The 9 regression criteria — those are SUBTASK_reg_criteria
- Test sufficiency — not in scope
- Architecture review
