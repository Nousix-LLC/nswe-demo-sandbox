# COMPLETE — SUBTASK_api_client (typed REST client, `src/api.rs`)

**Task**: Implement the real `ApiClient` in `src/api.rs` — a typed async REST client over
`ferric-http` that (de)serializes `chirp-types` DTOs, attaches the bearer token, and maps every
failure to `AppError`, signature-identical to the frozen `contracts/app_api.rs` +
`contracts/rest_endpoints.md`.

**decompose_evaluation**: Atomic (one module, one responsibility — the typed REST client; all
triggers cleared, both concern tests passed).

## Declared output (produced)

- `checkout/crates/chirp-frontend/src/api.rs` — the real `ApiClient`, replacing the scaffold stub.

## What was done

Replaced the scaffold's non-panicking stub with the real implementation, composed against the
landed crates' real APIs (read as ground truth, not paraphrased):

- **Struct**: `ApiClient { base_url: String, token: Option<SessionToken> }`, `#[derive(Debug, Clone)]`
  (cheap to clone, per contract). A private `http_client()` builds a fresh `ferric_http::Client`
  per call via `Client::builder().base_url(..)`, adding `Authorization: Bearer <token>` as a
  default header when a token is present.
- **`new` / `with_token`**: signature-identical to `contracts/app_api.rs`; `with_token` consumes
  self and carries the bearer token.
- **Seven methods**, each mapping one-to-one to `rest_endpoints.md`:
  - `login` → `POST /sessions` (`LoginRequest` → `AuthResponse`)
  - `create_user` → `POST /users` (`CreateUserRequest` → `User`)
  - `create_chirp` → `POST /chirps` (`CreateChirpRequest` → `Chirp`)
  - `timeline` → `GET /timeline` (`TimelineQuery` → `Page<Chirp>`), query string built from only
    the present `limit`/`cursor` fields
  - `get_user` → `GET /users/{id}` (`{id}` = `UserId::get()`) → `User`
  - `set_follow` → `PUT`(follow)/`DELETE`(unfollow) `/users/{id}/follow` → `FollowResponse`
  - `set_like` → `PUT`(like)/`DELETE`(unlike) `/chirps/{id}/like` → `LikeResponse`
- **Error mapping**: every failure funnels through `AppError::from_http` (owned by the scaffold's
  `error.rs`), which decodes a server `chirp_types::ApiError` out of a non-2xx `Error::Status` body
  into `AppError::Api`, maps `Error::Network` → `AppError::Network`, and everything else (builder /
  (de)serialize / body / undecodable non-2xx) → `AppError::Transport`. JSON-body serialization
  errors on POST are mapped the same way. No `unwrap`/`expect`/`panic!`/`todo!`/`unimplemented!`
  and no `unsafe` in the module body.
- **Pure helpers** (`user_path`, `follow_path`, `like_path`, `timeline_query_params`) factor the
  path/query construction so it is unit-testable off-DOM; `send`/`send_json` (the only browser-only
  calls) are left to the compile-only wasm smoke tests.

## Contract fidelity

- Public signatures are byte-identical to `contracts/app_api.rs` (the three feature-view spokes
  compile against the scaffold stub's L1 shape and recompose against this impl at the gate).
- `chirp-types` DTOs are used directly from `chirp_types::prelude::*`; no DTO is redefined.
- Base URL / auth-header / `{id}` interpolation / `TimelineQuery` rules follow `rest_endpoints.md`.

## Verification (read-only; no git — the gate commits)

All run in the shared checkout on branch `work/chirp-frontend`:

- `cargo fmt -p chirp-frontend -- --check` — clean.
- `cargo clippy -p chirp-frontend --all-targets -- -D warnings` — clean.
- `cargo test -p chirp-frontend` — 15 passed / 0 failed (11 new `api::tests` covering client
  construction, path interpolation, timeline query building incl. percent-encoded URL, and
  `AppError` decoding of a non-2xx `ApiError` body + network/undecodable cases; plus the 4
  inherited `error::tests`).
- `cargo build -p chirp-frontend --target wasm32-unknown-unknown` — succeeds.

## Success criteria

- [x] Every method matches `rest_endpoints.md` one-to-one (method, path, request/response DTO,
      auth-header rule, `TimelineQuery` query-string building, `{id}` path interpolation).
- [x] Error mapping decodes `chirp_types::ApiError` from a non-2xx body; distinguishes network vs
      transport; no `unwrap`/`expect`/`panic`/`unsafe` in the module body.
- [x] Native unit tests (off-DOM) for URL/path/query building and `AppError` decoding.
- [x] `cargo fmt`/`clippy -D warnings` clean on the crate; public items documented.

## Notes for the synthesis gate

- Wrote files only; performed **no** git operations (checkout left on `work/chirp-frontend`).
- Test-module helper uses `expect` inside `#[cfg(test)]` only, mirroring the scaffold's committed
  `error.rs` test precedent; the runtime module body contains no panic/unwrap/expect/unsafe.
- Verification compiled the whole crate against the *current* sibling stubs; the gate re-verifies
  the combined tree once `timeline`/`compose`/`profile` land.
