# Spoke Review — AC-1: Public Access and Auth Boundaries

**PR**: #263 (`Nousix-LLC/nswe-demo`, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`)
**Concern**: Access-control and authentication boundaries for the new public endpoints
**Verdict**: FINDINGS — one blocker

---

## Finding 1 (Blocker) — Authenticated home timeline silently serves the global unauthenticated feed

**Location**: `crates/chirp-frontend/src/timeline.rs`, line 218 (pinned commit `decb6196`)

```rust
// line 208 — fn request_load
fn request_load(ctx: AppContext, kind: LoadKind) {
    ...
    wasm_bindgen_futures::spawn_local(async move {
        let result = ctx.client().pub_timeline(&query).await;   // ← line 218
        apply_result(kind, result);
    });
}
```

**What is at stake**: AC-1 requires a logged-out visitor to reach the public timeline without being
forced to sign in. The flip side is that a logged-in user navigating to `/timeline` should see their
per-user home following feed — the feed that returns only chirps from people they follow, computed
server-side with the authenticated viewer's id.

**Why it matters here**: `timeline_view` is still mounted at `/timeline` in `app.rs`. An
authenticated user who navigates there now gets the global unauthenticated feed
(`/api/public/timeline`, backed by `ChirpRepository::public_timeline`) instead of their personalized
home feed (`/api/timeline`, backed by `ChirpRepository::timeline(viewer, query)`). The two data
sources are entirely separate: the public endpoint is a reverse-chronological list of all chirps from
all users; the home endpoint is scoped to the viewer's follows. A user following five accounts will
see every chirp from every user in the system instead.

The module doc comment at the top of `timeline.rs` (line 4) documents the correct call as
`ctx.client().timeline(..)`, making this change inconsistent with the module's own stated contract.

`pub_timeline()` in `api.rs` also **explicitly strips the auth token even when one is set** — it
constructs a fresh unauthenticated client rather than forwarding `self.token`. So the regression is
unconditional: there is no code path under which an authenticated user on `/timeline` reaches their
home feed after this change.

**What would satisfy this finding**:
Change line 218 of `crates/chirp-frontend/src/timeline.rs` from

```rust
let result = ctx.client().pub_timeline(&query).await;
```

to

```rust
let result = ctx.client().timeline(&query).await;
```

An integration test in `crates/chirp-server/tests/api.rs` already asserts `GET /api/timeline`
returns 401 without a token (line 915–919), confirming the server-side endpoint is correctly
guarded. The fix needs a corresponding frontend test (or at minimum a manual verification) that
`timeline_view` calls `timeline()`, not `pub_timeline()`, to guard against recurrence.

---

## What was checked and found clean

### 1. New public endpoints: no AuthUser extractor

All three new handlers in `crates/chirp-server/src/api/handlers.rs` accept only the state and query
extractors; `AuthUser` does not appear in their signatures:

| Handler | Signature extractors |
|---------|----------------------|
| `public_chirps` | `State(state): State<AppState>`, `Query(query): Query<PublicTimelineQuery>` |
| `user_chirps` | `State(state): State<AppState>`, `Path(username): Path<String>`, `Query(query): Query<PublicTimelineQuery>` |
| `public_timeline` | `State(state): State<AppState>`, `Query(query): Query<TimelineQuery>` |

In Axum, `AuthUser` acts as an extractor-middleware: if the `Authorization: Bearer` header is absent
or invalid, Axum rejects the request before the handler body executes. Its absence here is the
correct implementation of "no auth required". The route registrations in
`crates/chirp-server/src/api/router.rs` mount these handlers directly on the router without any
tower auth layer wrapping them.

Handler-level unit tests (inside `handlers.rs`) assert 200 responses without a token for
`public_chirps` and `user_chirps`. The integration test at `crates/chirp-server/tests/api.rs`
line 841 (`public_timeline_empty_store_returns_200_with_empty_page`) and line 907
(`public_timeline_requires_no_auth`) confirm the same for `GET /api/public/timeline`.

### 2. Authenticated endpoints still require and enforce auth

The following handlers in `handlers.rs` all retain their `AuthUser` extractor and are unmodified
from their pre-PR form:

- `create_chirp` — `AuthUser(author): AuthUser`
- `timeline` — `AuthUser(viewer): AuthUser`
- `follow` / `unfollow` — `AuthUser(follower): AuthUser`
- `like` / `unlike` — `AuthUser(user): AuthUser`

The integration test at line 915–919 provides a regression guard: `GET /api/timeline` without a
token returns 401. No other previously auth-gated endpoint lost its extractor in this diff.

### 3. No auth bypass surface from route changes

The public routes are registered on a plain `Router` without any middleware layer that would
propagate auth state to previously protected routes. The route table in
`crates/chirp-server/src/api/router.rs` mounts public and authenticated routes as siblings; there
is no shared `from_fn` or `layer` that would strip or forward auth headers across route
boundaries. The `pub_timeline()` frontend method deliberately constructs an independent HTTP client
that omits the token, so a logged-in user calling it does not accidentally forward their bearer
token to the public endpoint.

### 4. Frontend route table: public routes are genuinely unguarded

`crates/chirp-frontend/src/app.rs` registers `/` → `landing_view` and `/@:handle` →
`public_profile_view` without any auth guard component wrapping them. The `timeline_view` and
`compose_view` routes remain under `/timeline` and `/compose` respectively. No previously
unauthenticated page had an auth gate added accidentally.

---

## Summary

The public endpoint surface is correctly wired: three new handlers expose read-only data without
requiring authentication, the existing auth-gated handlers are untouched, and no bypass path was
introduced in the routing layer. The one blocker is in the frontend client: `timeline_view` was
changed to call `pub_timeline()` instead of `timeline()`, silently serving the global chronological
feed to authenticated users who expect their personalized home feed. The fix is a single-line
change.
