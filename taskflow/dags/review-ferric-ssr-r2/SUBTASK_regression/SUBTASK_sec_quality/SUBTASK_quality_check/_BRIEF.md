# Task: Code Quality Analysis — ferric-ssr-r4

## Task Specification

**Slug**: SUBTASK_quality_check  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

Review the code quality of new and changed code introduced by ferric-ssr-r4 commits (`7fb90c7`, `e625c3f`, `75c1eef`) in `app.rs` and `hydrate_wasm.rs`. File fresh non-blockers if any new instances of issue patterns from #229–#242 appear in genuinely new code. Produce `quality_raw_findings.md`.

### Context

This task is a spoke of SUBTASK_sec_quality (see `../_GLOBAL.md`). It covers code quality only — security concerns are SUBTASK_sec_check's concern.

**Code quality concerns to check**:

1. **`app.rs` new conditional hydrate/mount dispatch** (`7fb90c7`): Is the new conditional (choosing between hydration and fresh mount) readable? Does the branch logic handle edge cases the comment or docstring should acknowledge? Is there dead code introduced? Does the documentation accurately describe the invariant the conditional enforces (e.g., the promise that `has_child_nodes()` distinguishes SSR-rendered pages from blank ones)?

2. **`hydrate_wasm.rs` new test code** (`e625c3f`): Quality of test helpers — are they clear, well-named, non-redundant? Are assertions specific enough to catch regressions (do they check behavior or merely that something ran)? Any copy-paste patterns suggesting missed abstraction?

3. **Fresh non-blockers from new code**: Do any patterns from the previously-filed #229–#242 non-blockers appear in the NEW code introduced by these three commits (not in pre-existing code)? File only genuinely new instances; do not re-raise already-filed issues.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Parent context | `../_GLOBAL.md` | Review scope and constraints |
| Spoke output schema | `../contracts/spoke_output_schema.md` | Required output format for quality_raw_findings.md |
| `app.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/chirp-frontend/src/app.rs?ref=work/ferric-ssr-r1` | Code quality of new hydrate/mount dispatch conditional |
| `hydrate_wasm.rs` | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=work/ferric-ssr-r1` | Code quality of new test code |
| Changed files list | `gh pr view 228 --json files` | Confirm which lines are new vs pre-existing |

**Note**: Retrieve file content via `gh api … | python3 -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"` to decode the base64 response.

To identify what is genuinely new code from these commits vs pre-existing, compare the file against a base ref. You may also check the commit diff: `gh api repos/Nousix-LLC/nswe-demo/commits/7fb90c7` and `gh api repos/Nousix-LLC/nswe-demo/commits/e625c3f`.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `quality_raw_findings.md` |
| Location | `SUBTASK_quality_check/` (this workspace) |

The output MUST follow `../contracts/spoke_output_schema.md` §SUBTASK_quality_check. It carries:
- `## Code Quality Findings` section: enumerated findings with Severity, Location, Description, Resolution — or "No code quality findings."
- `## What Was Examined and Found Clean` section: each quality concern examined with no finding

---

## Success Criteria

- [ ] app.rs new conditional assessed for readability, edge cases, dead code, documentation accuracy
- [ ] hydrate_wasm.rs test code assessed for helper quality, assertion specificity, copy-paste patterns
- [ ] Fresh non-blockers documented (file + line) or explicitly confirmed absent
- [ ] Evidence cites file + line at pinned commit `75c1eef`
- [ ] `quality_raw_findings.md` written conforming to spoke_output_schema.md

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: Code Review; Supporting: Rust, Framework Design

Specific files to load:
- `code-review/CodeReview_Process_Methodology.md` — review discipline; reading for what isn't there; proportionate depth follows risk; evidence-over-assertion
- `code-review/CodeReview_Checklist_Methodology.md` — checklist for new code quality: naming, documentation, dead code, test quality
- `rust/Rust_Testing_Methodology.md` — Rust test quality; assertion specificity; test-double strategy; patterns that make tests weak (testing that code ran vs testing behavior)
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — hydration seam correctness; what the conditional's invariant must guarantee

These are the parent's suggested methodologies. Load fewer if clearly inapplicable; load more as needed.

## Inherited Constraints

- Scope is ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT re-raise non-blockers #229–#242; file only genuinely new instances in genuinely new code
- Evidence must cite file + line at pinned commit `75c1eef`
- Do not reference overseer escalation comments from I267

## Out-of-Scope

- Security concerns (HTML injection, DOM spoofing, test injection) — those are SUBTASK_sec_check
- The 9 regression criteria — those are SUBTASK_reg_criteria
- Test sufficiency (B2's concern)
- Architecture review
