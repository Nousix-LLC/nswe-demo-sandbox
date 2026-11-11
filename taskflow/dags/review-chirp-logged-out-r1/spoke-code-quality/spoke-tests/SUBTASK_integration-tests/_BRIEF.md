# Task: Integration Test Depth — Concern 2

## Task Specification

**Slug**: SUBTASK_integration-tests
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess the depth of the new integration tests in `crates/chirp-server/tests/api.rs`
(`mod public_timeline`) added in PR #263: whether pagination is covered (cursor round-trip,
boundary at exactly `limit` items) and whether the auth regression guard tests the right endpoint.

### Context

This is concern 2 of the `spoke-tests` decomposition. See `../_GLOBAL.md` for PR details
and shared context.

**Concern assigned to this spoke:**
2. Do the integration tests cover pagination correctly — cursor round-trip, boundary at exactly
   `limit` items? Does the regression guard (`GET /api/timeline` returns 401 without auth)
   actually test the right endpoint?

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignments, pin commit |
| Analysis schema | `../contracts/analysis_schema.md` | Required output format |
| `tests/api.rs` | `gh api "repos/Nousix-LLC/nswe-demo/contents/crates/chirp-server/tests/api.rs?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" --jq '.content' \| base64 -d` | Integration tests including mod public_timeline |

---

## Process Specification

Locate `mod public_timeline` in `tests/api.rs`. For each test in that module, determine:

1. **Pagination — cursor round-trip**: Is there a test that creates enough chirps to fill a page,
   calls the endpoint, receives a cursor, and then uses that cursor to fetch the next page?
   A test that only checks that a cursor is returned does not verify that the cursor actually
   works as a continuation token.

2. **Pagination — boundary at exactly `limit` items**: Is there a test that creates exactly
   `limit` items (not `limit + 1` or `limit - 1`) and asserts the response's cursor behavior
   at that precise boundary? Off-by-one errors in pagination typically require this case.

3. **Auth regression guard**: The brief says the guard should check `GET /api/timeline` returns
   401 without auth. What URL does the test actually hit? What status code does it assert?
   Does it hit `/api/timeline` (the authenticated endpoint) or `/api/public/timeline` (the
   unauthenticated one)?

Apply the integration test methodology: would each test fail if the behavior it is meant to
guard were broken?

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `analysis.md` |
| Format | Markdown |
| Location | `SUBTASK_integration-tests/` (this workspace) |

Structure: exactly per `../contracts/analysis_schema.md`.

---

## Success Criteria

- Verdict declared (CLEAN or FINDING(S))
- Explicit verdict on whether cursor round-trip is tested (not just cursor existence)
- Explicit verdict on whether the boundary at exactly `limit` items is tested
- Explicit verdict on what URL the auth regression guard hits and whether the assertion is correct
- All findings cite file path and line number at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No suspicion-level statements without cited evidence

---

## Suggested Methodology Files

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`, `Testing`

Specific files:
- `testing/Testing_Integration_Testing_Methodology.md` — integration test depth standards;
  use to assess pagination coverage and regression guard correctness
- `code-review/CodeReview_Checklist_Methodology.md` — the checklist covering test coverage
  as part of a code review
- `code-review/CodeReview_Process_Methodology.md` — the reader's independence obligation

These are the parent's suggested starting point. Load fewer if one is clearly inapplicable;
load more if the brief reveals additional methodology surface needed.

## Out-of-Scope

- Handler unit tests (`crates/chirp-server/src/api/handlers.rs`) — concern 1
- Frontend tests (`crates/chirp-frontend/src/api.rs`) — concern 5
- SQL correctness, dead code, error message safety, prose (other spokes)

## Inherited Constraints

- Findings cite file path and line number at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No host paths, private IPs, or infrastructure details in any output
- Prose bar: no moral adjectives on technical things, no narrated candor, no slot-fill templates
- Repository: `Nousix-LLC/nswe-demo` only
