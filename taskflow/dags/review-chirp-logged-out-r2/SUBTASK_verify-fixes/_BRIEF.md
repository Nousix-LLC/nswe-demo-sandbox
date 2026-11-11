# Task: Verify B1 and B2 Fix Correctness

## Task Specification

**Slug**: SUBTASK_verify-fixes  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  

### Objective

Examine the remediation diff `decb6196..7f4b684` on `work/chirp-logged-out` in PR #263 (Nousix-LLC/nswe-demo). Verify that Blocker 1 (B1) and Blocker 2 (B2) from review-r1 have been correctly, completely, and minimally fixed. Assess code quality, test coverage, security, and whether any extra changes appear beyond the two targeted single-line fixes. Produce `findings-fixes.md` in this task's workspace.

### Context

This task is part of review-chirp-logged-out-r2 (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: none — runs in parallel with SUBTASK_verify-acs  
**Dependents**: SUBTASK_synthesis consumes this task's output

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | PR metadata, blocker definitions, ACs, constraints |
| r1 review output | `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` | Original blocker detail and what a correct fix looks like |
| PR diff | `gh pr diff 263 -R Nousix-LLC/nswe-demo` | The actual diff `decb6196..7f4b684` under review |
| r27 remediation | `taskflow/dags/chirp-logged-out-r27/SYNTHESIS.md` (if accessible) | What the remediation claimed to change |
| contracts manifest | `../contracts/_MANIFEST.yaml` | Required output schema |

---

## Review concerns to address

### Concern 1 — Correctness of B1 fix

**Location**: `crates/chirp-frontend/src/timeline.rs:218`  
Previous (at `decb6196`): `ctx.client().pub_timeline(&query).await`  
Expected (at `7f4b684`): `ctx.client().timeline(&query).await`

Verify:
- Is `timeline(&query)` present at line 218 (or wherever the call now sits after the commit)?
- Does `timeline()` construct an authenticated client (uses `self.token`) and routes to `/api/timeline`, not `/api/public/timeline`? The module doc at `timeline.rs:4` documents the correct call.
- Is there any remaining `pub_timeline` call in `timeline.rs` that could still route authenticated traffic through the public feed?
- Is the fix consistent with the module-level doc?

### Concern 1 — Correctness of B2 fix

**Location**: `crates/chirp-frontend/src/compose.rs:519`  
Previous (at `decb6196`): `link("/compose", "Log in →")`  
Expected (at `7f4b684`): `link("/signin", "Log in →")`

Verify:
- Is `link("/signin", "Log in →")` present at line 519 (or wherever the link now sits)?
- Does `/signin` resolve to the sign-in view in the route table?
- Is the fix consistent with surrounding context in `compose.rs`?

### Concern 3 — Code quality

For each of the two changed lines:
- Is the change minimal — no extraneous whitespace, no reformatting, no refactoring of surrounding code?
- Does it follow the codebase's code style and naming conventions?
- No unintended changes to neighboring logic?

### Concern 4 — Test coverage

For B1: Is there a test that explicitly confirms `timeline_view` calls `timeline()` (authenticated) rather than `pub_timeline()`? The r1 review (SYNTHESIS.md, Blocker 1) noted the fix needs "a frontend test or manual verification." Check whether a test was added in the remediation commit.

For B2: Is there a test verifying `compose.rs:519` renders a "Log in →" link pointing to `/signin`? Check the existing test suite for `compose.rs` or the sign-up view.

If new tests were added: do they cover the fixed behavior and would they catch a regression?

### Concern 5 — Security

- B1 fix: `timeline()` uses an authenticated client — confirm no unintended credential handling introduced
- B2 fix: a link destination change — no input, no processing, no surface to exploit
- No host paths, internal network addresses (tailnet `100.x` or LAN IPs), internal server URLs, or review DAG internal paths committed in the diff
- No new dependency or unsafe block introduced

### Concern 6 — Regression check

Is the diff limited to the two targeted single-line fixes? If the diff contains any additional modifications (new files, removed lines, changed logic beyond `timeline.rs:218` and `compose.rs:519`), those additional changes must be evaluated against the full review bar.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `findings-fixes.md` |
| Location | `SUBTASK_verify-fixes/` (this task's workspace) |

### Required output structure

```markdown
# Findings: B1 and B2 Fix Verification

**PR**: #263 (`work/chirp-logged-out`)
**HEAD reviewed**: 7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4
**Diff reviewed**: decb6196..7f4b684

## Fix verdicts

| Fix | Verdict | Evidence |
|-----|---------|----------|
| B1 (timeline.rs) | PASS or FAIL | [specific evidence] |
| B2 (compose.rs) | PASS or FAIL | [specific evidence] |

## Code quality: [PASS | FAIL | FLAG]
[Findings or "no issues found"]

## Test coverage: [PASS | FAIL | FLAG]
[Findings — whether B1 and B2 each have a test]

## Security: [PASS or FAIL]
[Findings or "no new attack surface"]

## Regression: [PASS or FAIL]
[Are there extra changes? List if any.]

## Non-blocking findings
| ID | Location | Severity | Description |
|----|----------|----------|-------------|
[List new non-blockers found, if any. Leave empty if none.]

## Clean items
[What was examined and found sound]
```

The output MUST conform to the contract schema in `../contracts/_MANIFEST.yaml`: the file must carry an explicit verdict for each of B1 and B2.

---

## Success criteria

- [ ] `gh pr diff 263 -R Nousix-LLC/nswe-demo` obtained and read
- [ ] B1: `timeline.rs:218` verified — specific call form confirmed
- [ ] B2: `compose.rs:519` verified — specific link destination confirmed
- [ ] Code quality assessed for each change
- [ ] Test coverage assessed for B1 fix and B2 fix
- [ ] Security assessed for each change
- [ ] Regression check: diff confirmed minimal or extra changes documented
- [ ] `findings-fixes.md` written with explicit PASS/FAIL verdicts for B1 and B2

---

## Suggested Methodology Files

**Task type row matched**: "Code review | Code Review (primary) | Core, Testing (supporting)"  
Plus: Rust code review maps to "Rust | Code Review, Core"

**Primary files to load:**
- `code-review/CodeReview_Process_Methodology.md` — the core review process; covers how to structure findings and what a verdict means
- `code-review/CodeReview_Checklist_Methodology.md` — the per-line review checklist applied to each changed line
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — how to frame findings

**Supporting files to consider:**
- `rust/Rust_Async_Tokio_Methodology.md` — relevant to `timeline.rs` which is an async Rust component; confirms what `ctx.client().timeline(&query).await` does
- `testing/Testing_Unit_Testing_Methodology.md` — for assessing whether the test coverage for B1/B2 is adequate

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Scope is `decb6196..7f4b684` only — do not evaluate the full original PR diff (already reviewed in r1)
- HEAD under review is `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4` — do not drift to a different commit
- Non-blockers already tracked as issues #264–#271 from review-r1 — note them as "already tracked" if re-encountered; do not re-file
- Do NOT name host paths, tailnet addresses (`100.x`), or review DAG internal paths in any GitHub-posted content or in findings that will be posted publicly
- The repo is `Nousix-LLC/nswe-demo` — use this form in all public-facing output

## Out-of-Scope Methodologies

- `code-review/CodeReview_PR_Authoring_Methodology.md` — not applicable; this task reads the PR, not authors it
- AC verification — that is SUBTASK_verify-acs's responsibility; this task may note if B1/B2 fix directly fixes AC-1/AC-4 as an observation, but does not formally verify all 5 ACs
