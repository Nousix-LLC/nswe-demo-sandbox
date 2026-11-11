# Verdict: AC-1

**ac_1_verdict**: PASS

## Evidence

### B1 fix check

`timeline.rs:218` at HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4` reads:

```rust
        let result = ctx.client().timeline(&query).await;
```

Confirmed by direct file read via GitHub API (`/contents/crates/chirp-frontend/src/timeline.rs?ref=7f4b684`). At r1 HEAD `decb6196` the same line read `ctx.client().pub_timeline(&query)` (also confirmed by direct read). The B1 bug is gone at this HEAD.

**Note on PR diff**: this single-line revert does not appear in `gh pr diff 263` because the PR diff computes the aggregate from the merge base (`cb1ced3`, `main`) where the bug never existed. The introduction and the fix are both intra-branch commits that cancel in the aggregate diff. Direct file verification at the respective SHAs is the decisive evidence.

### Public endpoint guard status

All three newly added public backend handlers — `public_chirps`, `user_chirps`, and `public_timeline` — are **in the remediation diff** (`crates/chirp-server/src/api/handlers.rs`). Each is verified to have no `AuthUser` extractor:

| Handler | Signature (extractors) | Auth? |
|---|---|---|
| `public_chirps` | `State(state): State<AppState>`, `Query(query): Query<PublicTimelineQuery>` | None ✓ |
| `user_chirps` | `State(state): State<AppState>`, `Path(username): Path<String>`, `Query(query): Query<PublicTimelineQuery>` | None ✓ |
| `public_timeline` | `State(state): State<AppState>`, `Query(query): Query<TimelineQuery>` | None ✓ |

All three are mounted in `router.rs` (`crates/chirp-server/src/api/router.rs`, also in the diff) without any intervening auth middleware:

```rust
.route("/api/users/{username}/chirps", get(handlers::user_chirps))
.route("/api/chirps", get(handlers::public_chirps).post(handlers::create_chirp))
.route("/api/public/timeline", get(handlers::public_timeline))
```

The only `.layer()` applied to the whole router is `TraceLayer::new_for_http()` — no auth `from_fn` or bearer-token extraction layer. Confirmed from the full `router.rs` file at HEAD.

Auth-gated handlers (`create_chirp`, `timeline`, `follow`, `unfollow`, `like`, `unlike`) — **not modified by remediation diff** — r1 finding carries forward. Confirmed at HEAD by reading `handlers.rs`: all six still carry `AuthUser(…): AuthUser` as their first extractor argument.

### Frontend route table

The frontend route table in `crates/chirp-frontend/src/app.rs` is **in the remediation diff**. At HEAD `7f4b684` the `Router` in `start()` registers:

```rust
.route("/", move |_params| landing_view(&landing_ctx))
.route("/@:handle", move |params| { … public_profile_view(&public_profile_ctx, handle) })
```

No auth check, no session guard, no redirect closure on either entry. The router uses only `.mount_history()` as a terminator — no `from_fn` or middleware layer of any kind. Both public routes are bare closures.

No new auth layer in the frontend router — **not separately modified** (the layer-free structure was unchanged) — r1 finding carries forward (confirmed at HEAD).

## Conclusion

At HEAD `7f4b684`, `timeline.rs:218` correctly calls `ctx.client().timeline(&query)`, restoring the authenticated feed for `/timeline` and leaving the public home route (`/` → `landing_view`) calling the unauthenticated `public_timeline` API client. The public backend endpoints (`/api/chirps`, `/api/users/{username}/chirps`, `/api/public/timeline`) carry no `AuthUser` extractor and are mounted without an auth layer; the frontend routes `/` and `/@:handle` are unguarded. AC-1 passes.
