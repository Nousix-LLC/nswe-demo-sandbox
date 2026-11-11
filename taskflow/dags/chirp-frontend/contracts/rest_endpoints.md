# REST endpoint map — chirp-frontend (#9) ⇄ chirp-server (#8)

Frozen wire contract. Each `ApiClient` method (see `app_api.rs`) maps to **exactly one**
method+path below and uses the named `chirp-types` DTOs **directly** (no redefinition).
This is also the set of assumptions `chirp-server` #8 must honor at runtime; the
synthesis gate records them in `SYNTHESIS.md` so the overseer/reviewer can check
cross-crate coherence. chirp-frontend does **not** build-depend on #8 — it calls this
contract over HTTP/JSON at runtime.

## Base URL

- Configurable via `AppContext::base_url`; **default `/api`** (a relative base, so the SPA
  calls the same origin that served it — no hard-coupling to #8's host/port). The scaffold
  documents how to override it (e.g. a build-time/env constant). `ferric_http` joins the
  base and path with exactly one `/`.

## Auth

- `login` / `create_user` are unauthenticated. Every other call attaches
  `Authorization: Bearer <SessionToken>` when a `Session` is present (via
  `ApiClient::with_token` / `AppContext::client`). A `401` surfaces as
  `AppError::Api(ApiError{ code: Unauthorized, .. })`.

## Endpoints

| ApiClient method | HTTP | Path | Request DTO (body/query) | Success response DTO |
|---|---|---|---|---|
| `login`        | POST   | `/sessions`           | `LoginRequest` (JSON body)        | `AuthResponse` |
| `create_user`  | POST   | `/users`              | `CreateUserRequest` (JSON body)   | `User` |
| `create_chirp` | POST   | `/chirps`             | `CreateChirpRequest` (JSON body)  | `Chirp` |
| `timeline`     | GET    | `/timeline`           | `TimelineQuery` (query string: `limit`, `cursor`) | `Page<Chirp>` |
| `get_user`     | GET    | `/users/{id}`         | — (`{id}` = `UserId::get()`)      | `User` |
| `set_follow`   | PUT/DELETE | `/users/{id}/follow` | — (`PUT` to follow, `DELETE` to unfollow) | `FollowResponse` |
| `set_like`     | PUT/DELETE | `/chirps/{id}/like`  | — (`PUT` to like, `DELETE` to unlike)     | `LikeResponse` |

Notes:
- `{id}` path segments use the opaque id's numeric value (`UserId::get()` / `ChirpId::get()`).
- `TimelineQuery` serializes only present fields; build the query string from `limit` and
  `cursor` (the `Cursor` is an opaque string echoed back from `Page::next_cursor`).
- All request/response bodies are JSON with **camelCase** field names (chirp-types pins this
  via serde); ids/timestamps are bare JSON numbers; `ErrorCode` is `SCREAMING_SNAKE_CASE`.

## Errors (the wire error contract)

- A non-2xx response carries a JSON `ApiError { code: ErrorCode, message, details }` body.
  `ferric_http` turns a non-2xx into `Error::Status { status, body: Some(json), .. }`; the
  client decodes `ApiError` from that body into `AppError::Api(..)`. A `fetch`-level failure
  is `AppError::Network(..)`; any non-decodable/encoding failure is `AppError::Transport(..)`.
- `ErrorCode` variants a view may branch on: `ValidationError`, `Unauthorized`, `Forbidden`,
  `NotFound`, `Conflict`, `Internal`.
