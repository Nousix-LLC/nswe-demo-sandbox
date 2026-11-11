# Public API Specification — Logged-Out Endpoints

This document defines the JSON API shape for the two public (unauthenticated) endpoints that
the logged-out visitor experience requires. Both `SUBTASK_backend` (implementing the endpoints)
and `SUBTASK_frontend` (consuming them from the browser) MUST compose against this spec.

**Frozen at decompose time — read-only to all descendants.**
Additive amendments go through the plan-amendment channel; no descendant silently edits this file.

---

## Endpoint 1: Public Timeline

**Method + Path:** `GET /api/chirps`

**Authentication:** None required. No `Authorization` header needed.

**Query parameters (optional):**
| Parameter | Type | Description |
|-----------|------|-------------|
| `before` | string (ISO 8601 timestamp) | Pagination cursor — return chirps created before this timestamp |
| `limit` | integer (1–50, default 20) | Max chirps to return |

**Response 200 OK:**
```json
{
  "chirps": [
    {
      "id": "string (UUID)",
      "content": "string",
      "author": {
        "username": "string",
        "display_name": "string | null"
      },
      "created_at": "string (ISO 8601)",
      "like_count": 0
    }
  ],
  "has_more": true
}
```

**Response states the frontend MUST handle:**
- `loading` — request in flight
- `empty` — `chirps` array is empty AND `has_more` is false (no content exists yet)
- `loaded` — one or more chirps rendered
- `end_of_list` — `has_more` is false AND at least one page was already displayed
- `error` — HTTP error or network failure (show recoverable message per AC-3)

---

## Endpoint 2: Public User Profile

**Method + Path:** `GET /api/users/:username/chirps`

**Authentication:** None required.

**Path parameter:** `:username` — the user's login handle (URL-safe string, case-insensitive lookup acceptable)

**Query parameters (optional):**
| Parameter | Type | Description |
|-----------|------|-------------|
| `before` | string (ISO 8601 timestamp) | Pagination cursor |
| `limit` | integer (1–50, default 20) | Max chirps to return |

**Response 200 OK:**
```json
{
  "user": {
    "username": "string",
    "display_name": "string | null",
    "bio": "string | null",
    "chirp_count": 0
  },
  "chirps": [
    {
      "id": "string (UUID)",
      "content": "string",
      "created_at": "string (ISO 8601)",
      "like_count": 0
    }
  ],
  "has_more": true
}
```

**Response 404 Not Found:**
```json
{
  "error": "user not found"
}
```

**Response states the frontend MUST handle:**
- `loading` — request in flight
- `empty` — user exists but `chirps` is empty
- `loaded` — user and chirps rendered
- `end_of_list` — `has_more` is false after first page displayed
- `not_found` — HTTP 404 (user does not exist)
- `error` — other HTTP error or network failure

---

## Sign-Up / Sign-In Navigation

The landing/home page MUST include links to:
- Sign in: navigates to the existing sign-in route (e.g. `/sign-in` or `/login`)
- Create an account: navigates to the sign-up route (e.g. `/sign-up` or `/register`)

The exact routes depend on what already exists in chirp-frontend — `SUBTASK_explore_and_setup`
will determine the existing route names. These links MUST be present even when the timeline is
in loading or empty state (AC-4).

---

## Error Format (general)

For non-404 HTTP errors:
```json
{
  "error": "string (human-readable message)"
}
```

---

## Implementation Notes for SUBTASK_backend

- If a public timeline endpoint (`GET /api/chirps` or similar) already exists, verify it
  requires no auth and returns the shape above (adjust if different structure already exists).
- If no unauthenticated endpoint exists, add one. The route handler MUST NOT call any
  auth-extraction middleware that returns 401 when auth is absent; use an optional auth extractor
  or no auth extractor at all.
- The `like_count` field can return 0 if the likes feature is not yet implemented.

## Implementation Notes for SUBTASK_frontend

- The frontend MUST consume these endpoints using Ferric's async Resource primitive.
- Compose against the JSON shapes defined above (using `serde_json` deserialization to Rust structs).
- Do not wait for `SUBTASK_backend` to be complete — implement against this spec; the backend
  implements to the same spec.
