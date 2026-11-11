# Task: Confirm AC-2, AC-3, and AC-5 Remain PASS

## Task Specification

**Slug**: SUBTASK_ac235-confirm  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Confirm that AC-2, AC-3, and AC-5 — which all PASSED in r1 (HEAD `decb6196`) — remain PASS at HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`. The remediation commit targets only `timeline.rs:218` and `compose.rs:519`. If the relevant files (`landing.rs`, `error.rs`, `public_profile.rs`) are not in the remediation diff, record each as "file not in remediation diff — r1 verdict carries forward." If any are modified, examine whether the modification affects the criterion. Produce `verdict-ac235.md`.

### Context

This task is part of SUBTASK_verify-acs (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: none — runs in parallel with SUBTASK_ac1-verify and SUBTASK_ac4-verify  
**Dependents**: SUBTASK_synthesis consumes this task's output

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Subtree constraints |
| r1 SYNTHESIS | `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` | r1 per-AC evidence (AC-2: landing.rs:286–306; AC-3: AppError/error_banner; AC-5: state machines) |
| PR diff | `gh pr diff 263 -R Nousix-LLC/nswe-demo` | The remediation diff |
| Relevant source files (only if modified) | repo files | Only needed if the diff shows changes to landing.rs, error.rs, or public_profile.rs |
| Contracts manifest | `../contracts/_MANIFEST.yaml` | Required output schema |

---

## What to Verify

### AC-2 (was PASS): Empty state on arrival with no content

r1 found `empty_view()` at `landing.rs:286–306` correct: "Welcome to Chirp" heading, two correctly-routed CTAs (`/signup`, `/signin`).

**Check**: Is `landing.rs` in the remediation diff? If no: record "landing.rs not in remediation diff — r1 verdict carries forward — AC-2 PASS." If yes: examine the modified lines to determine whether `empty_view()` (lines 286–306) is affected, and verify the CTAs still route correctly.

### AC-3 (was PASS): Error state recoverability

r1 found `AppError::user_message()` returns plain-English text on all arms; `error_banner` sets `role="alert"` on every call path; "Retry" button wired to a full re-fetch.

**Check**: Is `error.rs` or the error-handling section of `landing.rs` in the remediation diff? If no: record "error handling files not in remediation diff — r1 verdict carries forward — AC-3 PASS." If yes: examine the modification to determine whether the user_message(), error_banner, or retry behavior is affected.

### AC-5 (was PASS): State branches accurate and distinct

r1 found all four states (loading, empty, error, end-of-list) present and distinct in both `landing.rs` and `public_profile.rs`.

**Check**: Are `landing.rs` or `public_profile.rs` in the remediation diff? If no: record "state machine files not in remediation diff — r1 verdict carries forward — AC-5 PASS." If yes: examine whether the state rendering logic is affected.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `verdict-ac235.md` |
| Location | `SUBTASK_ac235-confirm/` (this task's workspace) |

### Required output structure

```markdown
# Verdict: AC-2, AC-3, AC-5

**ac_2_verdict**: PASS | FAIL  
**ac_3_verdict**: PASS | FAIL  
**ac_5_verdict**: PASS | FAIL

## Evidence

### AC-2: Empty state
[For landing.rs: "not in remediation diff — r1 finding carries forward" OR evidence of change and its effect]

### AC-3: Error state recoverability
[For error.rs / landing.rs error handling: "not in remediation diff — r1 finding carries forward" OR evidence of change and its effect]

### AC-5: State branches accurate and distinct
[For landing.rs / public_profile.rs state machines: "not in remediation diff — r1 finding carries forward" OR evidence of change and its effect]

## Conclusion
[1–3 sentences summarizing whether these three ACs remain PASS]
```

---

## Success Criteria

- [ ] PR diff obtained via `gh pr diff 263 -R Nousix-LLC/nswe-demo`
- [ ] AC-2: `landing.rs` checked — either "not in diff, r1 carries forward" or modification assessed
- [ ] AC-3: Error handling code checked — either "not in diff, r1 carries forward" or modification assessed
- [ ] AC-5: `landing.rs` and `public_profile.rs` checked — either "not in diff, r1 carries forward" or modification assessed
- [ ] `verdict-ac235.md` written with explicit `ac_2_verdict`, `ac_3_verdict`, `ac_5_verdict` fields

---

## Suggested Methodology Files

**Task type row matched**: "Code review | Code Review (primary) | Core, Testing (supporting)"

**Primary files to load:**
- `code-review/CodeReview_Process_Methodology.md` — review process and verdict recording
- `code-review/CodeReview_Checklist_Methodology.md` — checklist applicable if any file is in the diff

Note: If all three files are confirmed absent from the diff (the expected case given the targeted remediation), this task may need fewer than the typical tool calls. The methodology is primarily useful if any of the files are present in the diff and require code-level scrutiny.

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Scope is the remediation diff `decb6196..7f4b684` only
- HEAD under review is `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`
- When a file is not in the diff, explicitly record that finding — do not silently skip
- Non-blockers already tracked as issues #264–#271 — note as "already tracked" if re-encountered
- Do NOT name host paths, tailnet addresses, or review DAG internal paths in any GitHub-posted content
- Repo is `Nousix-LLC/nswe-demo`

## Out-of-Scope

- AC-1 and AC-4 — owned by sibling spokes
- Fix correctness verification — owned by SUBTASK_verify-fixes
