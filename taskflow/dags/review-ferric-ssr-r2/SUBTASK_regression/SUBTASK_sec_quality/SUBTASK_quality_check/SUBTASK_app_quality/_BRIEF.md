# Task: app.rs Code Quality Review — ferric-ssr-r4

## Task Specification

**Slug**: SUBTASK_app_quality
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Review the code quality of new and changed code in `app.rs` introduced by ferric-ssr-r4 commits (`7fb90c7`, `e625c3f`, `75c1eef`). Specifically: assess the new conditional hydrate/mount dispatch for readability, edge cases, dead code, and documentation accuracy. Also check whether any patterns from previously-filed #229–#242 non-blockers appear in genuinely new app.rs code from these commits. Produce `app_quality_raw.md`.

### Context

This task is a spoke of SUBTASK_quality_check (see `../_GLOBAL.md`). It covers app.rs only — hydrate_wasm.rs test code quality is SUBTASK_test_quality's concern. Security concerns (HTML injection, DOM spoofing) are SUBTASK_sec_check's concern and must not be raised here.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Constraints, methodology posture, pinned commit |
| Parent context | `../../_GLOBAL.md` | Review scope and overall constraints |
| Spoke output contract | `../contracts/spoke_intermediate_schema.md` | Required output format for app_quality_raw.md |
| `app.rs` current | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/chirp-frontend/src/app.rs?ref=work/ferric-ssr-r1` | Full current file |
| `app.rs` diff (commit 7fb90c7) | `gh api repos/Nousix-LLC/nswe-demo/commits/7fb90c7` | What was new/changed in this commit |
| Changed files list | `gh pr view 228 --json files` | Confirm which lines are new vs pre-existing in app.rs |

**Note**: Retrieve file content via:
```
gh api <url> | python3 -I -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"
```

To identify what is genuinely new code from these commits vs pre-existing, compare via the commit diff.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `app_quality_raw.md` |
| Location | `SUBTASK_app_quality/` (this workspace) |

The output MUST follow `../contracts/spoke_intermediate_schema.md` §SUBTASK_app_quality. It carries:
- `## App.rs Code Quality Findings` section: enumerated findings or "No app.rs code quality findings."
- `## App.rs Fresh Non-blockers` section: new instances of #229-#242 patterns in new code, or "No fresh non-blockers found in app.rs new code."
- `## App.rs What Was Examined and Found Clean` section: each concern examined with no finding

---

## Success Criteria

- [ ] New conditional hydrate/mount dispatch assessed for readability (is the branch logic clear?), edge cases (what happens if `has_child_nodes()` returns an unexpected result?), dead code (any unreachable branches?), and documentation accuracy (does the comment/docstring accurately describe the invariant?)
- [ ] Every new line of app.rs from commits 7fb90c7/e625c3f/75c1eef checked for patterns from #229-#242 (do not re-raise already-filed issues; only genuinely new instances in new code)
- [ ] Evidence cites file + line at pinned commit `75c1eef`
- [ ] `app_quality_raw.md` written conforming to spoke_intermediate_schema.md

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: Code Review; Supporting: Rust, Framework Design

Specific files to load:
- `code-review/CodeReview_Process_Methodology.md` — review discipline; reading for what isn't there; proportionate depth follows risk; evidence-over-assertion. Load to ground the review approach.
- `code-review/CodeReview_Checklist_Methodology.md` — checklist for new code quality: naming, documentation, dead code. Load to ensure systematic coverage of quality concerns.
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — hydration seam correctness; what the conditional's invariant must guarantee (SSR-rendered vs blank page distinction). Load to evaluate the correctness of the has_child_nodes() invariant.

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Scope is ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT re-raise non-blockers #229–#242; file only genuinely new instances in genuinely new code
- Evidence must cite file + line at pinned commit `75c1eef`
- Security concerns (HTML injection, DOM spoofing) are out of scope — those are SUBTASK_sec_check
- Architecture review is out of scope
- Do not reference overseer escalation comments from I267

## Out-of-Scope

- hydrate_wasm.rs — that is SUBTASK_test_quality's concern
- Security surface analysis — that is SUBTASK_sec_check's concern
- Regression criteria — that is SUBTASK_reg_criteria's concern
- Test sufficiency (B2's concern)
