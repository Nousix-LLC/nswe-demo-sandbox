# COMPLETE — SUBTASK_explore-survey-backend

## Status: completed

## Output

- `backend-survey.md` — written at this workspace

## Summary

Surveyed `crates/chirp-server/` and documented the full API endpoint surface.

**Key findings:**

1. **Public timeline**: `GET /api/chirps` (`public_chirps` handler) already satisfies the
   contract. It is unauthenticated, returns chirps with embedded `author.username`, supports
   `before`-cursor pagination, and returns an empty list (not an error) when no chirps exist.
   No new endpoint is needed.

2. **Public user profile**: `GET /api/users/{username}/chirps` (`user_chirps` handler) already
   satisfies the contract. It is unauthenticated, returns `username`/`display_name`/`bio` +
   paginated chirps, and returns 404 for unknown usernames. No new endpoint is needed.

3. **Auth pattern**: No global middleware. Authentication is per-handler via the `AuthUser`
   extractor (`FromRequestParts`), which reads `Authorization: Bearer <token>` and resolves it
   through the repository. Unauthenticated handlers simply omit `AuthUser` from their arguments.

**SUBTASK_backend-api implication**: Both target endpoints are already implemented and satisfy
the public API contract. The backend task may focus on verifying tests pass, checking the wire
types against the contract, and documenting the URLs in `backend-impl.md`.
