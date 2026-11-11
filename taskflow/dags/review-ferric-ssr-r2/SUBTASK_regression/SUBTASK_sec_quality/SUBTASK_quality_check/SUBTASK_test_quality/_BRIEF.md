# Task: hydrate_wasm.rs Test Code Quality Review — ferric-ssr-r4

## Task Specification

**Slug**: SUBTASK_test_quality
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Review the code quality of new test code in `hydrate_wasm.rs` introduced by ferric-ssr-r4 commits (`7fb90c7`, `e625c3f`, `75c1eef`). Specifically: assess new test helpers for naming clarity and non-redundancy; evaluate whether assertions are specific enough to catch regressions (checking behavior vs. merely that code ran); and identify any copy-paste patterns suggesting missed abstraction. Also check whether any patterns from previously-filed #229–#242 non-blockers appear in genuinely new hydrate_wasm.rs code from these commits. Produce `test_quality_raw.md`.

### Context

This task is a spoke of SUBTASK_quality_check (see `../_GLOBAL.md`). It covers hydrate_wasm.rs only — app.rs conditional quality is SUBTASK_app_quality's concern. Security concerns (test injection safety) are SUBTASK_sec_check's concern and must not be raised here.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Constraints, methodology posture, pinned commit |
| Parent context | `../../_GLOBAL.md` | Review scope and overall constraints |
| Spoke output contract | `../contracts/spoke_intermediate_schema.md` | Required output format for test_quality_raw.md |
| `hydrate_wasm.rs` current | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=work/ferric-ssr-r1` | Full current test file |
| `hydrate_wasm.rs` diff (commit e625c3f) | `gh api repos/Nousix-LLC/nswe-demo/commits/e625c3f` | What was new/changed in this commit |
| Changed files list | `gh pr view 228 --json files` | Confirm which lines are new vs pre-existing |

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
| Filename | `test_quality_raw.md` |
| Location | `SUBTASK_test_quality/` (this workspace) |

The output MUST follow `../contracts/spoke_intermediate_schema.md` §SUBTASK_test_quality. It carries:
- `## hydrate_wasm.rs Code Quality Findings` section: enumerated findings or "No hydrate_wasm.rs code quality findings."
- `## hydrate_wasm.rs Fresh Non-blockers` section: new instances of #229-#242 patterns in new code, or "No fresh non-blockers found in hydrate_wasm.rs new code."
- `## hydrate_wasm.rs What Was Examined and Found Clean` section: each concern examined with no finding

---

## Success Criteria

- [ ] New test helpers assessed for naming clarity (are names descriptive and unambiguous?) and non-redundancy (do multiple helpers do essentially the same thing?)
- [ ] Assertions assessed for specificity: would each assertion actually fail if the behavior it's meant to test were broken? Does it check behavior or only that something ran?
- [ ] Copy-paste patterns identified: are there structurally similar test blocks that should share a helper or parameterized test?
- [ ] Every new line of hydrate_wasm.rs from commits 7fb90c7/e625c3f/75c1eef checked for patterns from #229-#242 (only genuinely new instances in new code)
- [ ] Evidence cites file + line at pinned commit `75c1eef`
- [ ] `test_quality_raw.md` written conforming to spoke_intermediate_schema.md

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: Code Review; Supporting: Rust, Framework Design

Specific files to load:
- `code-review/CodeReview_Checklist_Methodology.md` — checklist for test code quality: assertion specificity, helper naming, test structure. Load to ensure systematic coverage of test quality concerns.
- `rust/Rust_Testing_Methodology.md` — Rust test quality; assertion specificity; test-double strategy; patterns that make tests weak (testing that code ran vs testing behavior). Load as the primary source for evaluating test quality in Rust/WASM context.
- `code-review/CodeReview_Process_Methodology.md` — review discipline; reading for what isn't there; evidence-over-assertion. Load to ground the approach.

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Scope is ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT re-raise non-blockers #229–#242; file only genuinely new instances in genuinely new code
- Evidence must cite file + line at pinned commit `75c1eef`
- Security concerns (test injection) are out of scope — those are SUBTASK_sec_check
- Architecture review is out of scope
- Do not reference overseer escalation comments from I267

## Out-of-Scope

- app.rs — that is SUBTASK_app_quality's concern
- Security surface analysis — that is SUBTASK_sec_check's concern
- Regression criteria — that is SUBTASK_reg_criteria's concern
- Test sufficiency (B2's concern)
