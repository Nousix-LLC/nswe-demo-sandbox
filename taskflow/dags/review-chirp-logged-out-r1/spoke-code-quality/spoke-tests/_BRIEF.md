# Task: Test Depth Analysis — PR #263

## Task Specification

**Slug**: spoke-tests
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess test depth for the new and modified tests in PR #263 on `Nousix-LLC/nswe-demo`, covering
concerns 1, 2, and 5 from the parent spoke brief.

### Context

This task is part of the code-quality review decomposition. See `../_GLOBAL.md` for PR details,
the full concern assignment table, and the `contracts/` schema for FINDINGS.md output format.

**Concerns assigned to this spoke:**

1. **Handler unit tests** (`crates/chirp-server/src/api/handlers.rs`): Do the 6 new unit tests
   cover the 404 path for `user_chirps`? Does
   `public_chirps_returns_chirp_with_embedded_author` check that the `author` field in the
   response matches the created user? Are any critical error paths untested?

2. **Integration tests** (`crates/chirp-server/tests/api.rs`, `mod public_timeline`): Do the
   integration tests cover pagination correctly — cursor round-trip, boundary at exactly `limit`
   items? Does the regression guard (`GET /api/timeline` returns 401 without auth) actually test
   the right endpoint?

5. **`pub_timeline_url_has_correct_path_and_no_auth` test** (`crates/chirp-frontend/src/api.rs`):
   This test was written for the old `pub_timeline()` method, which called `/api/public/timeline`.
   Now `pub_timeline()` is used by the authenticated `timeline.rs`. Is the test still meaningful,
   or does it now test dead-to-the-public-timeline-feature code?

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignments, pin commit, output schema |
| Contract schema | `../contracts/findings_schema.md` | FINDINGS.md structure |
| handlers.rs | `gh api repos/Nousix-LLC/nswe-demo/contents/crates/chirp-server/src/api/handlers.rs?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba` or `gh pr diff` | Handler unit tests |
| tests/api.rs | `crates/chirp-server/tests/api.rs` at HEAD | Integration tests |
| frontend/api.rs | `crates/chirp-frontend/src/api.rs` at HEAD | `pub_timeline_url_has_correct_path_and_no_auth` test |
| timeline.rs | `crates/chirp-frontend/src/pages/timeline.rs` (or relevant caller) at HEAD | Who calls `pub_timeline()` now |
| Repository trait | `crates/chirp-server/src/repository/mod.rs` at HEAD | Method signatures being tested |

Access files via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```
or view the PR diff:
```bash
gh pr diff 263 -R Nousix-LLC/nswe-demo
```

---

## Process Specification

For each concern, read the relevant test file(s), identify what is tested and what is not,
and determine whether the gap constitutes a finding.

Apply the Testing methodology (unit testing, integration testing) and Code Review checklist:
- Do tests assert behavior or merely assert that something ran?
- Would each test fail if the behavior it is meant to guard were broken?
- Are doubles standing in for boundaries or for the logic under test?

A test that cannot fail is not a test.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Format | Markdown |
| Location | `spoke-tests/` (this workspace) |

Structure: exactly per `../contracts/findings_schema.md`.

---

## Success Criteria

- Concerns 1, 2, and 5 each appear in the Clean Account, whether clean or as a finding reference
- For concern 1: explicit verdict on the 404 path for `user_chirps` and on field-level assertion
  coverage in `public_chirps_returns_chirp_with_embedded_author`
- For concern 2: explicit verdict on pagination coverage (cursor round-trip and boundary) and on
  whether the auth regression guard hits the right endpoint
- For concern 5: explicit verdict on whether `pub_timeline_url_has_correct_path_and_no_auth` is
  still exercising live-to-the-feature code
- No findings left at "I suspect" without the evidence cited
- No internal infrastructure details in any finding

---

## Suggested Methodology Files

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`, `Testing`

Specific files:
- `code-review/CodeReview_Checklist_Methodology.md` — the checklist that covers test coverage
  as part of a code review; run the testing rows explicitly for this spoke
- `testing/Testing_Unit_Testing_Methodology.md` — what a good unit test looks like; use to
  assess whether the 6 handler tests are meaningful (assertion quality, not just line coverage)
- `testing/Testing_Integration_Testing_Methodology.md` — integration test depth standards;
  use to assess pagination coverage and regression guard correctness
- `code-review/CodeReview_Process_Methodology.md` — the reader's independence obligation;
  read the tests as closely as the code

These are the parent's suggested starting point. Load fewer if one is clearly inapplicable;
load more if the brief reveals additional methodology surface needed.

## Out-of-Scope Methodologies

- `testing/Testing_E2E_Testing_Methodology.md` — E2E tests are not in this PR's scope
- `testing/Testing_Performance_Testing_Methodology.md` — not relevant here
- `synthesis/` bundle — belongs to `spoke-synthesis`

## Inherited Constraints

- Findings point at repository file paths and line numbers at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`; no host paths, private IPs, or infrastructure details
- Do not post to the PR; that is `spoke-synthesis`'s parent DAG's responsibility
- Prose in FINDINGS.md must pass the plain-voice bar defined in `../contracts/findings_schema.md`
- Repository: `Nousix-LLC/nswe-demo` only
