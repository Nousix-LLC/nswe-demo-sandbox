# _BRIEF.md — Review DAG: review-chirp-logged-out-r1 (persona swe-reviewer)

## Objective

Review PR #263 (`work/chirp-logged-out`, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`) against issue #35's acceptance criteria and the codebase quality bar.

## Target

- **PR**: `Nousix-LLC/nswe-demo` #263 — "feat: logged-out public timeline and user profiles (#35)"
- **Branch**: `work/chirp-logged-out` at `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Issue closed**: `Nousix-LLC/nswe-demo` #35 — "Logged-out reading and a useful landing with accurate states"
- **Code machine verdict**: PASS — chirp-logged-out-r26, CI 6/6 green, all 5 ACs confirmed in SYNTHESIS.md at `taskflow/dags/chirp-logged-out-r26/SYNTHESIS.md`

## Acceptance Criteria (issue #35)

Review the PR against each AC:

- **AC-1**: Public timeline + user profiles accessible without login — no auth extractor on `GET /api/chirps` and `GET /api/users/{username}/chirps`; no redirect from `/` or `/@:handle`
- **AC-2**: Clear landing with sign-up prompt on empty state — `empty_view` in `crates/chirp-frontend/src/landing.rs`
- **AC-3**: Clear recoverable error message on timeline load failure — `error_banner` with `role=alert` + Retry button
- **AC-4**: "Create an account" route visible on landing AND sign-in screen — `nav_bar`, `header_nav`, `sign_in_view`
- **AC-5**: Loading, empty, error, end-of-list states accurate and distinct — all 7 state branches in `view_tree` + footer; same for `public_profile`

## Review Concerns

Evaluate each concern as a distinct section in the review output:

1. **Correctness**: Does the change implement all 5 ACs correctly, including edge cases, error paths, and async hazards? Does the public route handling correctly strip auth guards without opening auth bypass paths? Does the empty/error/loading state machine cover all branches distinctly?

2. **Code quality and design**: Responsibilities, coupling, abstraction boundaries, duplication, naming, function size, error-handling style. Does the change leave the code simpler to extend?

3. **Test coverage and depth**: Do tests exercise each AC and the edge/error paths? Do they assert real behavior rather than passing vacuously? Are test doubles used soundly?

4. **Security**: Input handling, trust boundaries. Does removing auth guards on public endpoints create any auth bypass path for authenticated endpoints? No SSRF exposure from new fetch paths. No host-specific paths, private network addresses (e.g. Tailscale `100.x` IPs), internal server URLs, or host taskflow/runtime paths committed to the diff.

5. **Language idiom**: Rust/WASM idiom correctness — signal usage, component lifecycle, error propagation, lifetime management.

6. **Regression safety**: No regressions in existing authenticated flows — authenticated timeline, profile editing, posting chirps, sign-in/sign-up still work correctly through the same route/component structure.

## Declared Output

- Review verdict: **APPROVE** or **REQUEST-CHANGES**
- Review posted on PR #263 (as a review comment if formal approval is not available due to same-account restriction)
- Root `SYNTHESIS.md` at `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` containing:
  - Overall verdict (APPROVE / REQUEST-CHANGES)
  - Per-concern findings with severity and whether each blocks
  - What each concern checked and found clean
  - Non-blocking findings for board filing
- Non-blocking findings listed for board issue filing

## Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Do not force-push
- Post review to PR #263
- Findings posted to the PR point at repository files and lines; do not name host paths, private IPs, or internal infrastructure details
