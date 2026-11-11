# Analysis: Frontend Test Validity — Concern 5

## Verdict

FINDING(S)

---

## Findings

### Finding A: Test does not invoke `pub_timeline()` and cannot guard its path or no-auth behavior

- **Concern**: 5
- **Location**: `crates/chirp-frontend/src/api.rs`, line 434 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: A unit test must invoke the unit under test. A test that reproduces the unit's internals inline and asserts properties of those reproduced internals asserts a tautology: the assertion passes whether or not the unit under test behaves correctly.
- **Why it matters**: The test's comment at line 435 states its intent — that `pub_timeline()` builds an unauthenticated client and hits `/public/timeline`, not `/timeline`. But the test body never calls `pub_timeline()`. It instead reproduces the method's URL-building steps inline, using the same `Client::builder().base_url(...).build().get("/public/timeline").query(&params).url()` chain, and asserts the URL that chain produces. That assertion is about `ferric_http::Client`'s URL-joining behavior with hardcoded arguments. It does not touch `pub_timeline()`'s implementation at all. Two specific regressions in `pub_timeline()` would leave this test green: (1) changing the path from `/public/timeline` to any other value (e.g., `/chirps`) — the test's inline chain still uses `/public/timeline`; (2) switching `pub_timeline()` from `Client::builder()...build()` to `self.http_client()` — which attaches `Authorization: Bearer <token>` when a token is present — the test never calls the method so the header change is invisible. No other test at the pinned commit guards these properties of `pub_timeline()`.
- **Severity**: non-blocking
- **Satisfying condition**: The test body calls `client.pub_timeline(&query)` directly (or through the production call path) and asserts properties of the request that `pub_timeline()` constructs — the URL path is `/public/timeline` and no `Authorization` header is present. If `ferric_http` does not expose outgoing-header inspection in a `#[test]` context, the test should at minimum call `pub_timeline()` and check the URL the method produces, rather than computing the same URL with an independent `Client::builder()` chain.

---

## Evidence

**`crates/chirp-frontend/src/api.rs` at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`**

`pub_timeline()` is defined at line 196. It constructs a fresh, header-free HTTP client via `Client::builder().base_url(self.base_url.clone()).build()` (not `self.http_client()`, which would attach the bearer token), calls `.get("/public/timeline")`, serializes query parameters, and calls `.send_json()`. The comment in the method body confirms the intent: the client carries no authorization header even when `self.token` is set.

The test `pub_timeline_url_has_correct_path_and_no_auth` starts at line 434. It constructs an `ApiClient` with a bearer token (line 436), builds a `TimelineQuery` with limit and cursor (lines 437–440), then reproduces `pub_timeline()`'s internal `Client::builder()` chain inline (lines 447–451). It calls `.url()` on the result and asserts `"/api/public/timeline?limit=10&cursor=pg2"` (line 452). The method `pub_timeline()` is never called. The assertion is about `ferric_http::Client`'s URL construction with the hardcoded path `/public/timeline` and the two query parameters — it is not about whether `pub_timeline()` uses that path.

**`crates/chirp-frontend/src/timeline.rs` at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`**

`request_load()` at line 208 calls `ctx.client().pub_timeline(&query).await` at line 218 inside a `wasm_bindgen_futures::spawn_local` closure. This module is the public timeline view mounted at `/`, shown to both logged-out visitors and authenticated users. `pub_timeline()` is the live call path for the public timeline feature at the pinned commit.

**Conclusion on the brief's framing**

The brief asks whether `pub_timeline()` is now "dead-to-the-public-timeline-feature." It is not: `timeline.rs` (the public home page at `/`) still calls `pub_timeline()` at line 218. The finding is different. Because the test never calls `pub_timeline()`, the method's path and no-auth behavior are unguarded regardless of which feature calls it. The test cannot distinguish a correct `pub_timeline()` from one that calls the wrong path or leaks the bearer token.
