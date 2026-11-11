# _BRIEF.md — Spoke: AC-5 State Branches Accurate and Distinct

## Objective

Review the state machine implementations in `landing.rs` and `public_profile.rs` against AC-5
of issue #35, verifying that all required state branches are present, distinct, and accurately
rendered, and that the state transition logic is correct.

**AC-5**: The logged-out landing/timeline exercises its loading, empty, error, and end-of-list
states accurately and distinctly (`REQ-UX-002/030/031/032`, `BAR-011`, one-state-model
criterion). The PR brief mentions "7 state branches" and the PR claims "6 distinct states" for
the public profile view.

## Inputs

- PR #263 diff: `Nousix-LLC/nswe-demo`, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Global context: `taskflow/dags/review-chirp-logged-out-r1/_GLOBAL.md`
- Primary code areas:
  - `crates/chirp-frontend/src/landing.rs` — `LandingModel` state struct, `view_tree`,
    `loading_view`, `empty_view`, `footer` (covering end-of-list, load-more, continuation-error,
    loading-more states), `STARTED` Cell guard
  - `crates/chirp-frontend/src/public_profile.rs` — `ProfileModel` state struct, `LoadPhase`
    enum, `view_tree`, `loading_view`, `not_found_view`, `error_view`, `loaded_view` (covering
    empty-loaded, loaded+more, end-of-list states), `profile_footer` (continuation-error,
    loading-more)
  - Tests in both files: `mod tests` in `landing.rs` and `mod tests` in `public_profile.rs`

## Specific concerns this spoke must resolve

1. **State enumeration vs. AC-5 requirements**: AC-5 names loading, empty, error, and
   end-of-list as required states. The PR brief says "7 state branches". Enumerate every distinct
   rendered state across `landing.rs` and `public_profile.rs`. Are the named AC-5 states covered?
   Are any of the 7 claimed states missing or duplicated?

2. **State distinctness**: Can any two states be confused — same CSS class, same visible text, or
   same DOM structure — such that a user (or test) cannot tell them apart?

3. **State transition correctness**:
   - Does `begin_initial` in `LandingModel` reset every field that affects rendering?
   - Does `apply_error` in `ProfileModel` correctly distinguish a 404 (`NotFound` phase) from
     other errors (`Error` phase)?
   - Does `apply_more` in `LandingModel` guard against empty continuation pages advancing the
     `before_cursor` incorrectly?

4. **`STARTED` Cell in `landing.rs`**: The global `STARTED: Cell<bool>` is set to `true` on
   first call and never reset. If a user navigates away from `/` and returns, `landing_view` will
   not call `request_load` again. Is the model reset, or does the view show stale state silently?
   Compare with `public_profile_view` which resets `STARTED` when the handle changes.

5. **Test completeness for AC-5**: Do the tests in `landing.rs` and `public_profile.rs` cover
   each distinct state branch with an assertion that would fail if the state were missing or
   collapsed with another state? Are the view-tree tests for the loading/error/empty/end-of-list
   branches asserting distinct enough conditions?

6. **One-state-model criterion**: Does any state render as a mix of two logical states (e.g.,
   showing the chirp list AND a full-screen error simultaneously)? Is the state model mutually
   exclusive across branches?

## Declared output

A `REVIEW.md` at `taskflow/dags/review-chirp-logged-out-r1/spoke-state-machine/REVIEW.md`
containing:

- Verdict for this concern: PASS or FINDINGS
- A complete enumeration of every rendered state in `landing.rs` and `public_profile.rs`,
  mapped against the AC-5 requirements
- For each finding: location (file + line at the pinned commit), what principle is at stake, why
  it matters, severity (blocker / non-blocking), and what would satisfy it
- An account of what each sub-concern checked and found clean

## Success criteria

- Every distinct rendered state is named and located in the code
- AC-5's required states (loading, empty, error, end-of-list) are confirmed present in both
  views
- The `STARTED` guard question is answered definitively (re-visit behavior documented)
- The state-transition edge cases (empty continuation page, 404 vs. non-404 error) are assessed
- Tests are assessed against whether they would catch a state collapse or a missing state

## Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Do not post to the PR; that is the synthesis child's responsibility
- Findings point at repository file paths and lines; do not name host paths, private IPs, or
  internal infrastructure details
