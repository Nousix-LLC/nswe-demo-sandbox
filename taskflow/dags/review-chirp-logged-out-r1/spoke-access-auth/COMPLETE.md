# COMPLETE — spoke-access-auth

**Task**: AC-1 public access and auth boundary review
**Status**: completed
**Verdict**: FINDINGS (one blocker)

## Outputs

- `REVIEW.md` — full review with one blocker finding and four clean-checks

## Blocker summary

`crates/chirp-frontend/src/timeline.rs` line 218 calls `ctx.client().pub_timeline(&query)` instead
of `ctx.client().timeline(&query)`. Authenticated users navigating to `/timeline` receive the global
unauthenticated feed from `/api/public/timeline` rather than their personalized home following feed
from `/api/timeline`. Fix: restore the call to `ctx.client().timeline(&query)`.

## Clean checks

1. All three new public server handlers have no `AuthUser` extractor and are confirmed to return 200
   without authentication.
2. All previously auth-gated handlers (`create_chirp`, `timeline`, `follow`, `unfollow`, `like`,
   `unlike`) retain their `AuthUser` extractor.
3. No auth bypass surface was introduced in the server routing layer.
4. Frontend public routes (`/`, `/@:handle`) are correctly unguarded; auth-required routes are
   unchanged.
