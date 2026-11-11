## Verdict

FINDING(S)

## Findings

### Finding A: Pagination boundary at exactly `limit` items not tested

- **Concern**: 2
- **Location**: `crates/chirp-server/tests/api.rs`, lines 869–903 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: Pagination cursor emission at the boundary where item count equals the page size
- **Why it matters**: When exactly `limit` items exist in the store, a pagination implementation can either return a cursor (pointing at a next page that happens to be empty) or return no cursor (signaling that the data set is exhausted at this boundary). The two behaviors differ meaningfully for consumers: a consumer that stops paginating on `next_cursor == None` will behave differently depending on which behavior the server implements. Off-by-one bugs in cursor emission — emitting a cursor when `count == limit` when none should exist, or omitting a cursor when `count == limit` and more items follow — are a classic failure mode that requires testing at this exact boundary. The existing test uses 3 items with `limit=2` (n = limit + 1), which exercises the "more pages remain" case but does not cover `n == limit`.
- **Severity**: non-blocking
- **Satisfying condition**: Add a test to `mod public_timeline` that creates exactly `limit` items — for example, 2 chirps with `?limit=2` — calls `GET /api/public/timeline?limit=2`, and explicitly asserts whether `next_cursor` is `None` or `Some(...)`. The assertion must be an intentional choice that documents the specified behavior at that boundary.

## Evidence

Examined all four tests in `mod public_timeline` (`crates/chirp-server/tests/api.rs`, lines 837–925 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`):

**Test 1 — `public_timeline_empty_store_returns_200_with_empty_page` (lines 841–848)**: empty store, no limit parameter. Asserts `items.is_empty()` and `next_cursor.is_none()`. Establishes the zero-item baseline; no pagination mechanics exercised.

**Test 2 — `public_timeline_includes_all_users_newest_first` (lines 851–866)**: 3 chirps from 2 users, no limit parameter. Asserts newest-first order by id. No pagination mechanics exercised.

**Test 3 — `public_timeline_paginates_with_cursor` (lines 869–903)**: creates 3 chirps (indices 0–2), fetches page 1 with `?limit=2`. Asserts 2 items and extracts the cursor at lines 885–888 (`page1.next_cursor.clone().expect(...)`). Fetches page 2 at `/api/public/timeline?limit=2&cursor={cursor.0}` (line 894). Asserts 1 item (the oldest chirp) and `page2.next_cursor.is_none()` at line 902. This is an actual cursor round-trip: the cursor received in page 1 is passed as a query parameter to page 2, and the endpoint returns items older than the cursor position. The 3-item / limit=2 setup covers n = limit + 1; it does not cover n = limit.

**Test 4 — `public_timeline_requires_no_auth` (lines 906–924)**: two requests. First, `GET /api/public/timeline` without an `Authorization` header; asserts `StatusCode::OK` at line 912. Second, `GET /api/timeline` without an `Authorization` header at line 919; asserts `StatusCode::UNAUTHORIZED` at line 922 with message `"GET /api/timeline must still require authentication"`. The regression guard targets `/api/timeline` — the authenticated home-timeline endpoint — not `/api/public/timeline`. The URL and the status assertion are both correct.

**Cursor round-trip** (criterion 2a): tested and verified clean. Test 3 receives a cursor from page 1 and supplies it to the page-2 request; the endpoint uses it to return items strictly older than the cursor position.

**Boundary at exactly `limit` items** (criterion 2b): not covered. No test in `mod public_timeline` creates a chirp count equal to the page-size parameter. The gap is at lines 869–903: a test exists for `n > limit` but not for `n == limit`.

**Auth regression guard** (criterion 2c): correct. The guard at lines 918–923 targets `/api/timeline` and asserts `UNAUTHORIZED`. The URL is not `/api/public/timeline`, and the assertion is the right status code for an auth-required endpoint.
