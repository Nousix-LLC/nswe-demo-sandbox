# Task: HTML Injection Analysis — ssr.rs

## Task Specification

**Slug**: SUBTASK_html_inj
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Examine `ssr.rs` at commit `75c1eef` for HTML injection risk. Determine whether user-controlled content can reach the HTML string output of `render_to_string` without escaping, and whether the docstring fix in commit `7fb90c7` introduces any new string interpolation into the SSR output path. Produce `html_inj_finding.md` with the finding for the "HTML Injection in ssr.rs" concern.

### Context

Spoke of the SUBTASK_sec_check decomposition. See `../_GLOBAL.md` for scope, constraints, and repo access instructions. Covers security only — code quality is a separate spoke.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub document | `../_GLOBAL.md` | Scope, constraints, repo access instructions, pinned commit |
| Finding format | `../contracts/finding_format.md` | Required output structure |
| `ssr.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/ssr.rs?ref=work/ferric-ssr-r1` | File under review |

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `html_inj_finding.md` |
| Location | `SUBTASK_html_inj/` (this workspace) |

The output file MUST conform to `../contracts/finding_format.md` with concern name `HTML Injection in ssr.rs`.

---

## Success Criteria

- [ ] `ssr.rs` read at commit `75c1eef`
- [ ] `render_to_string` and all string-building helpers inspected: does any point in the SSR output path accept user-controlled input without escaping?
- [ ] Docstring changes from commit `7fb90c7` examined: do they introduce new string interpolation into the HTML output?
- [ ] Escaping strategy (or its absence) identified and cited by file + line
- [ ] `html_inj_finding.md` written conforming to `../contracts/finding_format.md`

---

## Suggested Methodology Files

**Task-type row matched**: "Security review" → Primary: `security`; Supporting: `code-review`  
Also applicable: "SSR / hydration in a Rust UI framework" → `framework-design`

Specific files to load:
- `security/Security_Secure_Coding_Methodology.md` — HTML injection patterns, escaping requirements, trust boundary analysis; directly applies to checking `render_to_string` and string interpolation points in SSR output
- `code-review/CodeReview_Process_Methodology.md` — evidence over assertion; reading for what isn't there (missing escaping, missing guard)
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR escaping and hydration seam security; applies to the SSR output path

These are the parent's suggestions based on task type. Load fewer if inapplicable; load more if the work requires.

## Inherited Constraints

- Scope: ferric-ssr-r4 commits only (`7fb90c7`, `e625c3f`, `75c1eef`)
- Evidence must cite file + line at pinned commit `75c1eef` (not the branch head)
- Do NOT re-raise non-blockers #229–#242
- Do not reference overseer escalation comments from I267
- Code quality concerns are out of scope (separate spoke)
