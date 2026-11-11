# Task: Handler Unit Test Depth — Concern 1

## Task Specification

**Slug**: SUBTASK_handler-unit-tests
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess the depth of the 6 new unit tests in `crates/chirp-server/src/api/handlers.rs` added
in PR #263: whether the 404 path for `user_chirps` is covered and whether
`public_chirps_returns_chirp_with_embedded_author` checks the `author` field value against
the created user.

### Context

This is concern 1 of the `spoke-tests` decomposition. See `../_GLOBAL.md` for PR details
and the shared context. The parent spoke (`spoke-tests`) covers test depth for PR #263 on
`Nousix-LLC/nswe-demo`.

**Concerns assigned to this spoke:**
1. Do the 6 handler unit tests cover the 404 path for `user_chirps`? Does
   `public_chirps_returns_chirp_with_embedded_author` check that the `author` field in the
   response matches the created user? Are any critical error paths untested?

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignments, pin commit |
| Analysis schema | `../contracts/analysis_schema.md` | Required output format |
| `handlers.rs` | `gh api "repos/Nousix-LLC/nswe-demo/contents/crates/chirp-server/src/api/handlers.rs?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" --jq '.content' \| base64 -d` | Handler unit tests |
| `repository/mod.rs` | `gh api "repos/Nousix-LLC/nswe-demo/contents/crates/chirp-server/src/repository/mod.rs?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" --jq '.content' \| base64 -d` | Repository trait signatures (to identify error paths) |

---

## Process Specification

For this concern, determine:

1. **404 path for `user_chirps`**: Is there a test that exercises the handler path where the
   user does not exist? A 404 is a named error path of the API; absence of a test for it is
   a gap.

2. **Field-level assertion in `public_chirps_returns_chirp_with_embedded_author`**: Does the
   test assert the value of the `author` field in the response body against the user created
   in the test setup? Or does it only assert that the response deserialized / that some
   `author` field is present? A test that checks structure but not value does not catch a
   regression where the wrong author is embedded.

3. **Other critical error paths**: Review the repository trait signatures to understand what
   failure modes the handlers could encounter. For each handler under test, identify whether
   the test suite covers those failure modes or leaves them untested.

Apply the testing methodology questions: would each test fail if the behavior it is meant to
guard were broken? Does the assertion check behavior, or only that something ran?

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `analysis.md` |
| Format | Markdown |
| Location | `SUBTASK_handler-unit-tests/` (this workspace) |

Structure: exactly per `../contracts/analysis_schema.md`.

---

## Success Criteria

- Verdict declared (CLEAN or FINDING(S))
- Explicit statement on whether the 404 path for `user_chirps` is tested
- Explicit statement on what `public_chirps_returns_chirp_with_embedded_author` asserts
  (value-level vs. existence-level)
- Other critical error paths either confirmed tested or identified as a gap
- All findings cite file path and line number at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No suspicion-level statements without cited evidence

---

## Suggested Methodology Files

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`, `Testing`

Specific files:
- `testing/Testing_Unit_Testing_Methodology.md` — what a good unit test asserts; use to
  assess whether the handler tests are meaningful (behavior vs. existence assertion)
- `code-review/CodeReview_Checklist_Methodology.md` — the checklist covering test coverage
  as part of a code review; run the testing rows explicitly for this concern
- `code-review/CodeReview_Process_Methodology.md` — the reader's independence obligation;
  read the tests as closely as the code

These are the parent's suggested starting point. Load fewer if one is clearly inapplicable;
load more if the brief reveals additional methodology surface needed.

## Out-of-Scope

- Integration tests (`crates/chirp-server/tests/api.rs`) — concern 2
- Frontend tests (`crates/chirp-frontend/src/api.rs`) — concern 5
- SQL correctness, dead code, error message safety, prose (other spokes)

## Inherited Constraints

- Findings cite file path and line number at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No host paths, private IPs, or infrastructure details in any output
- Prose bar: no moral adjectives on technical things, no narrated candor, no slot-fill templates
- Repository: `Nousix-LLC/nswe-demo` only
