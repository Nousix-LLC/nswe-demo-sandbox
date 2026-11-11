# Findings — spoke-tests

## Verdict

FINDINGS

## Findings

### Finding 1: `public_chirps_returns_chirp_with_embedded_author` does not assert `author.display_name`

- **Concern**: 1
- **Location**: `crates/chirp-server/src/api/handlers.rs`, line 474 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: Assertion depth — a test that checks structure but not value does not catch a regression where the wrong value is returned
- **Why it matters**: The test creates a user with `display_name: "Alice A".to_owned()` (line 451) and the `public_chirps` handler maps the display name conditionally at lines 183–187 (`if author.display_name.is_empty() { None } else { Some(author.display_name) }`). The test asserts `resp.chirps[0].author.username == "alice"` (line 474), which catches a wrong-author regression. However, `resp.chirps[0].author.display_name` is never asserted. A regression in the conditional branch — for example, if the handler always returned `display_name: None` — would leave this test passing.
- **Severity**: non-blocking
- **Satisfying condition**: Add `assert_eq!(resp.chirps[0].author.display_name, Some("Alice A".to_owned()));` after the `author.username` assertion at line 474. The user is already created with a non-empty `display_name` in the test setup, so no additional setup is required.

### Finding 2: Pagination boundary at exactly `limit` items not tested

- **Concern**: 2
- **Location**: `crates/chirp-server/tests/api.rs`, lines 869–903 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: Pagination cursor emission at the boundary where item count equals the page size
- **Why it matters**: When exactly `limit` items exist in the store, an implementation can return a cursor (pointing to a next page that happens to be empty) or return no cursor (signaling that the data set is exhausted at this boundary). The two behaviors differ meaningfully for consumers: a consumer that stops paginating on `next_cursor == None` behaves differently depending on which the server implements. Off-by-one bugs in cursor emission at this exact boundary are a well-known failure mode that requires a test at `n == limit`. The existing test uses 3 items with `limit=2` (n = limit + 1), which covers the "more pages remain" case; it does not cover `n == limit`.
- **Severity**: non-blocking
- **Satisfying condition**: Add a test to `mod public_timeline` that creates exactly `limit` items — for example, 2 chirps with `?limit=2` — calls `GET /api/public/timeline?limit=2`, and explicitly asserts whether `next_cursor` is `None` or `Some(...)`. The assertion must reflect the intended behavior at that boundary.

### Finding 3: `pub_timeline_url_has_correct_path_and_no_auth` does not invoke `pub_timeline()`

- **Concern**: 5
- **Location**: `crates/chirp-frontend/src/api.rs`, line 434 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: A unit test must invoke the unit under test. A test that reproduces the unit's internals inline and asserts properties of that reproduction asserts a tautology: the assertion passes whether or not the unit under test behaves correctly.
- **Why it matters**: The test body never calls `pub_timeline()`. It instead reproduces the method's URL-building steps inline — using the same `Client::builder().base_url(...).build().get("/public/timeline").query(&params).url()` chain — and asserts the URL that chain produces. That assertion is about `ferric_http::Client`'s URL-joining behavior with hardcoded arguments. It does not touch `pub_timeline()`'s implementation. Two regressions in `pub_timeline()` would leave this test green: (1) changing the path from `/public/timeline` to another value — the test's inline chain still uses `/public/timeline`; (2) switching from `Client::builder()` to `self.http_client()` — which attaches `Authorization: Bearer <token>` when a token is present — the test never calls the method so the header change is invisible. No other test at the pinned commit guards either property.
- **Severity**: non-blocking
- **Satisfying condition**: The test body calls `client.pub_timeline(&query)` directly and asserts properties of the request that `pub_timeline()` constructs — the URL path is `/public/timeline` and no `Authorization` header is present. If `ferric_http` does not expose outgoing-header inspection in a `#[test]` context, the test should at minimum call `pub_timeline()` and check the URL the method produces, rather than computing the same URL with an independent `Client::builder()` chain.

## Clean Account

- **Concern 1 — Handler unit test depth**: Checked 404 path coverage and assertion depth for the two new handlers (`public_chirps`, `user_chirps`) in `handlers.rs`. The 404 path test (`user_chirps_returns_404_for_missing_user`) is behavior-level and covers the one documented error variant (`NotFound`). The `public_chirps_returns_chirp_with_embedded_author` test asserts `author.username` correctly but omits `author.display_name`, leaving the conditional-mapping branch unguarded. See Finding 1.

- **Concern 2 — Integration test pagination and auth regression**: Checked cursor round-trip coverage and auth-regression guard correctness across the four tests in `mod public_timeline`. The cursor round-trip is tested: test 3 passes the cursor from page 1 as a query parameter to page 2 and asserts the returned items. The auth-regression guard (`public_timeline_requires_no_auth`) targets `/api/timeline` and asserts `UNAUTHORIZED` — the correct URL and status code for the authenticated endpoint. The `n == limit` pagination boundary has no test. See Finding 2.

- **Concern 5 — Frontend test validity after refactoring**: Checked whether `pub_timeline_url_has_correct_path_and_no_auth` guards the path and no-auth behavior of `pub_timeline()` at the pinned commit. `pub_timeline()` remains live — called in `timeline.rs` at line 218. The test does not call `pub_timeline()` and cannot guard either property; two distinct regressions in the method would leave the test passing. See Finding 3.
