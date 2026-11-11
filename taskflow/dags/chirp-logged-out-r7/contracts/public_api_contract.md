# Public API Contract — Chirp Logged-Out Experience

## Purpose

This document declares the PUBLIC API surface that must exist after SUBTASK_backend-api completes. It is a declaration of intent: the exact URL patterns and response shapes will be confirmed in `backend-impl.md` after the backend task determines what already exists vs. what needs to be added.

## Required Endpoints

### Public Timeline

MUST provide an unauthenticated GET endpoint that returns a list of public chirps suitable for display on the landing page.

Constraints:
- MUST require no authentication header or session cookie
- MUST return chirps with at minimum: id, content/text, author username, created_at timestamp
- MUST support pagination (cursor or offset-based) to support end-of-list state
- MUST return a distinguishable empty list (not an error) when no chirps exist

### Public User Profile

MUST provide an unauthenticated GET endpoint that returns a user's public profile and their chirps.

Constraints:
- MUST require no authentication header or session cookie
- MUST return user profile data with at minimum: username, display name, bio (if present)
- MUST return the user's public chirps
- MUST return a 404 or equivalent "user not found" response for unknown usernames

## Implementation Note

SUBTASK_backend-api MUST:
1. Check whether these endpoints already exist in `crates/chirp-server`
2. If they exist but require auth, either make auth optional or add new public variants
3. If they do not exist, add them following existing Axum handler patterns
4. Document the actual endpoint URLs and types in `backend-impl.md`

## Consumer Constraint

SUBTASK_frontend-ui MUST:
- Read `backend-impl.md` to discover the actual endpoint URLs
- Call only the endpoints declared in that file
- Not hardcode API URLs that differ from what the backend task established
