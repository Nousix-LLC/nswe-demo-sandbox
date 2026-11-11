# Spoke Review: AC-5 — State Branches Accurate and Distinct

**Verdict**: PASS with non-blocking findings  
**Commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`  
**Files reviewed**: `crates/chirp-frontend/src/landing.rs`,
`crates/chirp-frontend/src/public_profile.rs`

---

## State Enumeration

### landing.rs — LandingModel

`view_tree` renders via two nested if-else chains: a top-level split on `model.loaded` and
`model.chirps.is_empty()`, then a footer sub-split on `error`, `loading_more`, and `has_more`.

| # | State | Guard condition | Root class / element |
|---|-------|-----------------|----------------------|
| 1 | Loading (initial) | `!loaded && error.is_none()` | `chirp-loading` (`<p>`) |
| 2 | Initial error | `!loaded && error.is_some()` | `chirp-landing-error` (`<div>`) |
| 3 | Empty | `loaded && chirps.is_empty()` | `chirp-landing-empty` (`<div>`) |
| 4 | Continuation error | `loaded && !chirps.is_empty() && error.is_some()` | `chirp-load-more-error` (`<div>`) in footer |
| 5 | Loading more | `loaded && !chirps.is_empty() && loading_more` | `chirp-loading-more` (`<p>`) in footer |
| 6 | Has more | `loaded && !chirps.is_empty() && has_more && !loading_more && error.is_none()` | Load more `<button>` in footer |
| 7 | End of list | `loaded && !chirps.is_empty() && !has_more && !loading_more && error.is_none()` | `chirp-end` (`<p>`), "You're all caught up." |

The seven branches match the PR's "7 state branches" claim. All four AC-5 states are covered:
**loading** → State 1; **empty** → State 3; **error** → States 2 and 4; **end-of-list** → State 7.

### public_profile.rs — ProfileModel

`view_tree` dispatches on the `LoadPhase` enum, then `loaded_view` subdivides within
`LoadPhase::Loaded`.

| # | State | Guard condition | Root class / element |
|---|-------|-----------------|----------------------|
| 1 | Loading | `phase = Loading` | `chirp-profile chirp-profile-loading` |
| 2 | Not found | `phase = NotFound` | `chirp-profile chirp-profile-not-found` |
| 3 | Error (non-404) | `phase = Error(e)` | `chirp-profile chirp-profile-error` |
| 4 | Empty (loaded) | `phase = Loaded && chirps.is_empty()` | `chirp-profile-empty` (`<p>`) |
| 5 | Continuation error | `phase = Loaded && !chirps.is_empty() && continuation_error.is_some()` | `chirp-load-more-error` in footer |
| 6 | Loading more | `phase = Loaded && !chirps.is_empty() && loading_more` | `chirp-loading-more` in footer |
| 7 | Has more | `phase = Loaded && !chirps.is_empty() && has_more && !loading_more && continuation_error.is_none()` | Load more `<button>` in footer |
| 8 | End of list | `phase = Loaded && !chirps.is_empty() && !has_more && !loading_more && continuation_error.is_none()` | `chirp-end` (`<p>`), "No more chirps." |

The PR and doc comment say "6 distinct states" (loading, not-found, empty, loaded, end-of-list,
error), treating States 5–8 as sub-states within "loaded." That framing is internally consistent.
The rendering tree has eight distinct leaves. All four AC-5 states are covered: **loading** →
State 1; **empty** → State 4; **error** → States 2 and 3; **end-of-list** → State 8.

---

## Concern 1: State Enumeration vs. AC-5 Requirements

**Checked**: `view_tree` in `landing.rs` lines 238–267, `footer` lines 352–375; `view_tree` in
`public_profile.rs` lines 285–298, `loaded_view` lines 338–386, `profile_footer` lines 421–453.

AC-5 names four required states. Each is confirmed present in both files with a distinct CSS
class and unambiguous text content:

- **Loading**: `landing.rs` State 1 (`chirp-loading`, "Loading…"); `public_profile.rs` State 1
  (`chirp-profile-loading`). Both render before any server response arrives.
- **Empty**: `landing.rs` State 3 (`chirp-landing-empty`, welcome message + CTAs); `public_profile.rs`
  State 4 (`chirp-profile-empty`, "No chirps yet."). Both are reached only after a successful
  initial fetch that returned zero items.
- **Error**: Initial-load errors render full-screen and replace the body (`chirp-landing-error`,
  `chirp-profile-error`). Continuation errors render inline in the footer alongside the existing
  chirp list (`chirp-load-more-error`). The two surfaces are contextually appropriate.
- **End-of-list**: `landing.rs` State 7 (`chirp-end`, "You're all caught up."); `public_profile.rs`
  State 8 (`chirp-end`, "No more chirps."). Reached only when `has_more = false` after at least
  one page has loaded.

No AC-5 state is missing. The PR's "7 state branches" count for landing.rs matches the seven
branches above. **PASS.**

---

## Concern 2: State Distinctness

**Checked**: CSS class attributes and text content across all 7 (`landing.rs`) and 8
(`public_profile.rs`) leaf nodes.

Every pair of states produces a different combination of class and content. The cases most likely
to collapse:

- **States 1 and 3 in landing.rs** (loading vs. empty): `chirp-loading` / "Loading…" vs.
  `chirp-landing-empty` with no loading indicator and a full welcome section. No class or text
  is shared.
- **States 1 and 2 in landing.rs** (loading vs. initial error): different classes, different
  elements, different text; initial error contains a "Retry" button, loading does not.
- **States 2 and 4** (initial error vs. continuation error): initial error renders as the entire
  body, replacing the chirp list; continuation error renders only in the footer alongside a
  visible chirp list. These two surfaces cannot be confused.
- **States 7 and 5 in landing.rs** (end-of-list vs. loading-more): `chirp-end` / "You're all
  caught up." vs. `chirp-loading-more` / "Loading more…". Different classes and text.

One inconsistency between the two test helpers (not an AC-5 issue): `find_class` in `landing.rs`
tests (line 423) does an exact-string match on the `class` attribute (`v == class`), while the
equivalent in `public_profile.rs` (line 501) splits on whitespace and matches tokens. The
`public_profile.rs` version is correct for compound class strings like
`"chirp-profile chirp-profile-loading"`. Since `landing.rs` currently uses only single-class
attribute values, the exact-match works in practice but would silently miss any multi-class
element added in the future.

Distinctness: **PASS.**

---

## Concern 3: State Transition Correctness

### begin_initial resets all rendering-relevant fields

**Checked**: `LandingModel::begin_initial` at `landing.rs` lines 82–89.

```rust
fn begin_initial(&mut self) {
    self.loaded = false;
    self.chirps.clear();
    self.before_cursor = None;
    self.has_more = false;
    self.loading_more = false;
    self.error = None;
}
```

All six fields that determine which of the 7 states renders are reset: `loaded`, `chirps`,
`has_more`, `loading_more`, `error`, and `before_cursor`. The function is correct.

**Finding F-3** (non-blocking — test gap): `begin_initial_resets_all_state` at line 487 verifies
`loaded`, `chirps.is_empty()`, `before_cursor.is_none()`, `has_more`, and `error.is_none()`, but
does not assert `!m.loading_more`. The implementation resets `loading_more` correctly; the test
has a coverage gap on that field.

Transition correctness for `begin_initial`: **PASS.**

### apply_error 404 vs. non-404 distinction in ProfileModel

**Checked**: `ProfileModel::apply_error` at `public_profile.rs` lines 132–147.

```rust
let is_not_found = matches!(&err, AppError::Api(api) if api.code == ErrorCode::NotFound);
match kind {
    LoadKind::Initial => {
        self.phase = if is_not_found { LoadPhase::NotFound } else { LoadPhase::Error(err) };
    }
    LoadKind::More => {
        self.loading_more = false;
        self.continuation_error = Some(err);
    }
}
```

For initial loads, 404 → `NotFound` phase; any other error → `Error(err)` phase. For
continuation loads, any error (including 404) becomes a recoverable inline continuation error —
the user exists per the successful initial load, so a 404 on a "More" request is treated as a
transient failure rather than a not-found condition. This is correct.

Three tests cover the three branches: `apply_error_on_initial_not_found_sets_not_found_phase`
(line 565), `apply_error_on_initial_server_error_sets_error_phase` (line 574), and
`apply_error_on_more_sets_continuation_error` (line 581). All three are present, all three
exercise distinct paths.

Transition correctness for `apply_error`: **PASS.**

### apply_more empty-page guard in LandingModel

**Checked**: `LandingModel::apply_more` at `landing.rs` lines 105–114.

```rust
fn apply_more(&mut self, resp: PublicTimelineResponse) {
    // Keep existing cursor if the continuation page is empty (guard against empty more pages).
    if let Some(last) = resp.chirps.last() {
        self.before_cursor = Some(last.created_at);
    }
    self.chirps.extend(resp.chirps);
    self.has_more = resp.has_more;
    self.loading_more = false;
    self.error = None;
}
```

The cursor is advanced only when `resp.chirps` is non-empty. An empty continuation response
leaves the cursor intact. The same guard appears in `ProfileModel::apply_more` at
`public_profile.rs` lines 122–130.

**Finding F-4** (non-blocking — test gap): `apply_more_appends_and_updates_cursor` at `landing.rs`
line 456 tests the happy path with a non-empty response but does not test the empty-response
case. The code comment at line 106 documents the guard, but no unit test verifies that an
empty-chirp `apply_more` leaves `before_cursor` unchanged.

What would satisfy this: add a test that calls `apply_more` with an empty chirp list and asserts
that `before_cursor` retains its previous value.

Transition correctness for `apply_more`: **PASS**. Guard is present; test coverage is incomplete.

---

## Concern 4: STARTED Cell Behavior on Re-visit

**Checked**: `STARTED: Cell<bool>` at `landing.rs` line 129, used at lines 148–153;
`public_profile_view` reset at `public_profile.rs` lines 177–186 (line 181 sets `STARTED` to
false when the handle changes).

In `landing_view`:

```rust
// landing.rs lines 148–153
STARTED.with(|started| {
    if !started.get() {
        started.set(true);
        request_load(ctx.clone(), LoadKind::Initial);
    }
});
```

`STARTED` is set to `true` on the first render and never reset. If the user navigates away from
`/` and returns, `landing_view` runs again, `STARTED.get()` returns `true`, and `request_load`
is not called.

**What the user sees on re-visit**: `MODEL` is a persistent `thread_local!`; it retains whatever
state it held when the user navigated away. The view renders that state through a fresh `tick`
signal created on each call to `landing_view`. The `bump()` guard at line 224
(`if current_path() != ROUTE_PATH { return; }`) prevents in-flight requests from firing a
re-render while away, but the model is still updated when those responses arrive. Net effect:
re-visiting `/` shows the last-known state — including any chirps already loaded — without a
spinner or a re-fetch.

**Contrast with public_profile_view**: the profile view resets `STARTED` and re-fetches whenever
the handle changes (`public_profile.rs` lines 177–186). That reset is a correctness requirement:
different users sharing a browser cannot see each other's chirps. For `/`, the route itself is
fixed; there is no handle or identity parameter to key a reset on. Preserving the cache is a
deliberate choice, consistent with the module doc comment ("Loads GET /api/chirps on first
display").

**AC-5 impact**: AC-5's four states are exercised correctly on first visit. Subsequent visits
render the cached model, which may be in any valid state. The re-visit behavior does not violate
AC-5. No STARTED reset is needed to satisfy this AC.

**Finding F-5** (non-blocking — design note): A re-visit to `/` after navigating away shows cached
state with no freshness indicator and no mechanism to trigger a fresh load beyond scrolling to the
"Load more" button (which continues from the previous cursor, not from the top). If the product
later requires fresh-on-return semantics, `STARTED` would need to be reset whenever `landing_view`
is re-entered, or the app would need an explicit route lifecycle hook. This is out of scope for
AC-5 but worth tracking.

---

## Concern 5: Test Completeness for AC-5

### landing.rs — 11 tests

**State-reduction** (5): `apply_initial_marks_loaded_sets_cursor_and_has_more` (line 444),
`apply_more_appends_and_updates_cursor` (line 456), `apply_error_on_initial_keeps_unloaded`
(line 468), `apply_error_after_load_keeps_loaded` (line 476), `begin_initial_resets_all_state`
(line 487).

**View-tree** (6): `unloaded_model_renders_loading_state` (line 501),
`every_state_includes_header_nav_links` (line 508),
`empty_model_renders_welcome_statement_and_cta_links` (line 525),
`loaded_model_renders_chirp_list_and_load_more_button` (line 546),
`last_page_renders_end_note_not_load_more` (line 568),
`initial_error_renders_error_message_and_retry_button` (line 584).

AC-5 states with view-tree coverage: loading ✓, empty ✓, initial error ✓, end-of-list ✓,
loaded+has_more ✓.

**Finding F-1** (non-blocking — test gap): No view-tree test covers the **continuation-error
state** (State 4: `loaded=true`, `chirps` non-empty, `error=Some`). If `footer` dropped the
`chirp-load-more-error` branch and fell through to the has-more or end-of-list branch, no test
would catch it. No view-tree test covers the **loading-more state** (State 5: `loading_more=true`);
if `chirp-loading-more` were absent, no test would fail.

What would satisfy F-1: add two view-tree tests in `mod tests`:
1. Build a `LandingModel` with `loaded=true`, at least one chirp, and `error=Some(...)`, render
   with `view_tree`, assert `find_class(&tree, "chirp-load-more-error").is_some()`.
2. Build a `LandingModel` with `loaded=true`, at least one chirp, and `loading_more=true`, render,
   assert `find_class(&tree, "chirp-loading-more").is_some()`.

### public_profile.rs — 12 tests

**State-reduction** (6): `reset_for_clears_all_prior_state` (line 533),
`apply_initial_transitions_to_loaded` (line 544), `apply_more_appends_chirps` (line 555),
`apply_error_on_initial_not_found_sets_not_found_phase` (line 565),
`apply_error_on_initial_server_error_sets_error_phase` (line 574),
`apply_error_on_more_sets_continuation_error` (line 581).

**View-tree** (6): `loading_state_renders_loading_indicator` (line 594),
`not_found_state_renders_distinct_message` (line 606), `error_state_renders_message_and_retry`
(line 623), `empty_loaded_state_renders_empty_message` (line 640),
`loaded_with_chirps_renders_list_and_load_more` (line 656), `end_of_list_renders_end_note`
(line 669).

AC-5 states with view-tree coverage: loading ✓, not-found ✓, error ✓, empty ✓, end-of-list ✓,
loaded+has_more ✓.

The PR description says "13 profile" tests; the file has 12. The count is off by one.

**Finding F-2** (non-blocking — test gap): Same gap as F-1 for public profile. No view-tree test
covers the **continuation-error state** (State 5: `continuation_error=Some` with chirps present)
or the **loading-more state** (State 6: `loading_more=true`). The transition test
`apply_error_on_more_sets_continuation_error` (line 581) verifies the model updates correctly but
does not render the tree and check the resulting class.

What would satisfy F-2: two additional view-tree tests, one for each missing state, asserting
`chirp-load-more-error` and `chirp-loading-more` respectively.

---

## Concern 6: One-State-Model Criterion

**Checked**: control flow in `view_tree` and `footer` / `profile_footer` in both files; reachable
state combinations through the `LandingModel` and `ProfileModel` state machines.

### landing.rs

The top-level branch structure is a Rust `if / else if / else`: only one of `!loaded`,
`chirps.is_empty()`, or the loaded-with-chirps arm executes. Within `footer`, the branches check
`error.is_some()` first, then `loading_more`, then `has_more`, then fall through — exactly one
branch executes.

Can `loaded=true && chirps.is_empty() && error=Some` occur? `apply_initial` is the only method
that sets `loaded=true`; it also assigns `self.chirps = resp.chirps` and `self.error = None`. An
empty initial response results in `loaded=true, chirps.is_empty(), error=None` — the empty-state
branch. A subsequent continuation error requires `begin_more`, which requires `has_more=true`
(`trigger_more` checks `!m.has_more` and returns early at line 173). An empty-chirp `apply_initial`
sets `has_more=false`, so no continuation can be triggered. The state machine does not permit
`loaded=true && chirps.is_empty() && error=Some`.

Can `loading_more=true && error=Some` both be set? `begin_more` sets `loading_more=true` and
clears `self.error = None` (line 93). After that, only one of `apply_more`, `apply_error`, or
`reload` runs. The states are mutually exclusive.

### public_profile.rs

`LoadPhase` is a Rust enum; the `match` in `view_tree` is exhaustive by the type system. Within
`loaded_view`, the `profile_footer` branches check `continuation_error` first, then
`loading_more`. `ProfileModel::begin_more` (lines 107–110) sets `loading_more=true` and clears
`continuation_error=None`, so they cannot both be set through the state machine.

One-state-model criterion: **PASS** for both views.

---

## Summary

| Sub-concern | Verdict |
|-------------|---------|
| State enumeration vs. AC-5 requirements | PASS — all four named states present in both views |
| State distinctness | PASS — every state has a unique class/text combination |
| `begin_initial` reset | PASS — all rendering fields reset; F-3 is a test gap |
| `apply_error` 404 vs. non-404 | PASS — correctly routes via `ErrorCode::NotFound` |
| `apply_more` empty-page guard | PASS — guard present; F-4 is a test gap |
| `STARTED` re-visit behavior | PASS for AC-5 — by-design caching; F-5 documents the trade-off |
| Test completeness for AC-5 | FINDINGS — F-1 and F-2 are view-tree gaps for footer sub-states |
| One-state-model criterion | PASS — mutually exclusive in both views |

**Overall verdict: PASS.** AC-5's required states (loading, empty, error, end-of-list) are
present, correctly rendered, and distinct in both `landing.rs` and `public_profile.rs`. State
transition logic is correct. No finding rises to blocker severity.

---

## Findings Index

| ID | File | Lines | Severity | Description |
|----|------|-------|----------|-------------|
| F-1 | `crates/chirp-frontend/src/landing.rs` | `mod tests` | Non-blocking | No view-tree test for continuation-error (State 4) or loading-more (State 5) |
| F-2 | `crates/chirp-frontend/src/public_profile.rs` | `mod tests` | Non-blocking | No view-tree test for continuation-error (State 5) or loading-more (State 6) |
| F-3 | `crates/chirp-frontend/src/landing.rs` | 487–497 | Non-blocking | `begin_initial_resets_all_state` does not assert `!m.loading_more` |
| F-4 | `crates/chirp-frontend/src/landing.rs` | 456–466 | Non-blocking | `apply_more_appends_and_updates_cursor` does not test the empty-page guard |
| F-5 | `crates/chirp-frontend/src/landing.rs` | 129, 148–153 | Non-blocking (design note) | Re-visit to `/` shows cached state with no re-fetch; intentional, documented here |
