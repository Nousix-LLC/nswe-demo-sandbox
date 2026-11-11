# Task: Frontend Test Validity — Concern 5

## Task Specification

**Slug**: SUBTASK_frontend-test-validity
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Determine whether `pub_timeline_url_has_correct_path_and_no_auth` in
`crates/chirp-frontend/src/api.rs` is still exercising live-to-the-public-timeline-feature code
after PR #263's refactoring changed which callers use `pub_timeline()`.

### Context

This is concern 5 of the `spoke-tests` decomposition. See `../_GLOBAL.md` for PR details
and shared context.

**Concern assigned to this spoke:**
5. `pub_timeline_url_has_correct_path_and_no_auth` was written for the old `pub_timeline()`
   method, which called `/api/public/timeline`. Now `pub_timeline()` is used by the
   authenticated `timeline.rs`. Is the test still meaningful, or does it now test
   dead-to-the-public-timeline-feature code?

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignments, pin commit |
| Analysis schema | `../contracts/analysis_schema.md` | Required output format |
| `frontend/api.rs` | `gh api "repos/Nousix-LLC/nswe-demo/contents/crates/chirp-frontend/src/api.rs?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" --jq '.content' \| base64 -d` | The test + pub_timeline() definition |
| `frontend/pages/timeline.rs` | `gh api "repos/Nousix-LLC/nswe-demo/contents/crates/chirp-frontend/src/pages/timeline.rs?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" --jq '.content' \| base64 -d` | Caller of pub_timeline() (try first) |

If `timeline.rs` is not at that path, search for `pub_timeline` callsites in the diff:
```bash
gh pr diff 263 -R Nousix-LLC/nswe-demo | grep -n pub_timeline
```

---

## Process Specification

1. Read `frontend/api.rs`:
   - What URL does `pub_timeline()` construct?
   - What does `pub_timeline_url_has_correct_path_and_no_auth` assert about that URL and
     its authorization headers (or absence thereof)?

2. Find the callsite(s) of `pub_timeline()` at HEAD:
   - Which code in the codebase calls `pub_timeline()`?
   - Is it called from code that handles the unauthenticated public timeline, or from
     code that handles the authenticated timeline?

3. Determine validity:
   - If the public timeline feature no longer calls `pub_timeline()`, then the test is
     guarding a URL/auth behavior that the feature never exercises — the test passes even
     if the public timeline feature is broken in a way that involves this URL.
   - If `pub_timeline()` is still called from the public timeline path, the test is still
     meaningful.

A test that cannot fail on a regression it was intended to catch is not a guard.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `analysis.md` |
| Format | Markdown |
| Location | `SUBTASK_frontend-test-validity/` (this workspace) |

Structure: exactly per `../contracts/analysis_schema.md`.

---

## Success Criteria

- Verdict declared (CLEAN or FINDING(S))
- Explicit verdict on whether `pub_timeline_url_has_correct_path_and_no_auth` is testing
  code that the public timeline feature still exercises at HEAD
- If the test is dead-to-the-feature, state what it is now guarding and whether that is
  still a useful guard or effectively inert
- All findings cite file path and line number at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No suspicion-level statements without cited evidence

---

## Suggested Methodology Files

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`, `Testing`

Specific files:
- `testing/Testing_Unit_Testing_Methodology.md` — what a unit test should guard; use to
  assess whether this test still guards the behavior it was intended to guard
- `code-review/CodeReview_Checklist_Methodology.md` — the checklist covering test coverage
  as part of a code review
- `code-review/CodeReview_Process_Methodology.md` — the reader's independence obligation;
  trace callsites, do not assume the description matches the code

These are the parent's suggested starting point. Load fewer if one is clearly inapplicable;
load more if the brief reveals additional methodology surface needed.

## Out-of-Scope

- Handler unit tests (`crates/chirp-server/src/api/handlers.rs`) — concern 1
- Integration tests (`crates/chirp-server/tests/api.rs`) — concern 2
- SQL correctness, dead code, error message safety, prose (other spokes)

## Inherited Constraints

- Findings cite file path and line number at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No host paths, private IPs, or infrastructure details in any output
- Prose bar: no moral adjectives on technical things, no narrated candor, no slot-fill templates
- Repository: `Nousix-LLC/nswe-demo` only
