# _GLOBAL.md — Review DAG: review-chirp-logged-out-r1

## Parent objective

Review PR #263 (`work/chirp-logged-out`, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`) in
`Nousix-LLC/nswe-demo` against issue #35's five acceptance criteria and the codebase quality bar.
The declared outputs are a `SYNTHESIS.md` at this workspace root and a review comment posted on
PR #263.

## Shared context (all spokes read this)

**PR**: "feat: logged-out public timeline and user profiles (#35)"
**Files changed**: 19 files, +3134/−72
**Key new files**: `crates/chirp-frontend/src/landing.rs`,
`crates/chirp-frontend/src/public_profile.rs`, `crates/chirp-frontend/src/sign_in.rs`,
`crates/chirp-frontend/src/sign_up.rs`
**Modified**: `crates/chirp-frontend/src/{api,app,compose,timeline}.rs`,
`crates/chirp-server/src/api/{handlers,router}.rs`,
`crates/chirp-server/src/repository/{in_memory,mod,postgres}.rs`,
`crates/chirp-server/tests/api.rs`, `crates/chirp-types/src/api.rs`,
`crates/ferric/src/hydrate.rs`

**Server endpoints added**:
- `GET /api/chirps` → `public_chirps` handler (no `AuthUser` extractor; `before`+`limit` query)
- `GET /api/users/{username}/chirps` → `user_chirps` handler (no auth; case-insensitive lookup)
- `GET /api/public/timeline` → `public_timeline` handler (no auth; opaque cursor pagination)

**Frontend client methods** (in `api.rs`):
- `pub_timeline()` calls `/api/public/timeline` (opaque cursor)
- `public_timeline()` calls `/api/chirps` (timestamp `before` cursor) — used by `landing.rs`

**Notable cross-cutting observation**:
`timeline.rs` changed its call from `ctx.client().timeline(&query)` to
`ctx.client().pub_timeline(&query)`. This routes the authenticated home timeline view through
`/api/public/timeline` (the global unauthenticated feed) rather than through `/api/timeline` (the
per-user following feed). Every spoke should be aware this may be a regression in the authenticated
timeline behavior.

**Route table** (from `app.rs`):
```
/             → landing_view       (new: public landing)
/@:handle     → public_profile_view (new)
/signin       → sign_in_view       (new, from sign_in.rs)
/sign-in      → sign_in_view       (alias, comment says "for AC-3" — anomaly)
/signup       → signup_view        (new, from compose.rs — functional)
/compose      → compose_view       (unchanged)
/user/:id     → profile_view       (unchanged)
/timeline     → timeline_view      (unchanged)
fallback      → not_found_view
```

Note: `sign_up.rs` exports `sign_up_view` (a placeholder stub) which is NOT in the route table.

## Subtree structure

| Workspace | Concern | Group | Depends on |
|-----------|---------|-------|------------|
| `spoke-access-auth/` | AC-1: public access without forced auth | 0 | — |
| `spoke-ui-states/` | AC-2/3/4: UI states, error messages, CTAs | 0 | — |
| `spoke-state-machine/` | AC-5: all state branches accurate and distinct | 0 | — |
| `spoke-code-quality/` | Code quality, tests, security, prose, idiom | 0 | — |
| `synthesis/` | Aggregate findings, write SYNTHESIS.md, post PR review | 1 | all spokes |

Each spoke produces a `REVIEW.md` at its own workspace root. The synthesis child reads all four
`REVIEW.md` files, writes `SYNTHESIS.md` at this workspace root, and posts the review to PR #263.
