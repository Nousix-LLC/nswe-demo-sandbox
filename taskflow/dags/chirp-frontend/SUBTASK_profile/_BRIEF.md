# Task: SUBTASK_profile — user profile + follow/like (src/profile.rs)

## Task Specification
**Slug**: SUBTASK_profile
**Task Kind**: standard
**Status**: Pending

### Objective
Implement `profile_view(ctx: &AppContext, params: &Params) -> VNode` (`src/profile.rs`): the
`/user/:id` route that loads a `User`, shows the profile + follower/following counts, and offers
**follow/unfollow** and **like** actions wired to the API client with reactive count updates.

### Context
Part of chirp-frontend (#9) — see `../_GLOBAL.md`. **Dependency**: `SUBTASK_scaffold` (crate,
`AppContext`, frozen view-fn signature, compiling `profile.rs` stub you replace). Runs in parallel
with the other spokes; composes against the frozen `ApiClient` (scaffold stub = L1 mock).
**Dependent**: the synthesis gate.

### Inputs
- `../_GLOBAL.md`, `../contracts/app_api.rs`, `../contracts/rest_endpoints.md`.
- The real `ferric`/`ferric-router` APIs (`Params::get`, `navigate`/`link`) and `chirp-types`
  `User`/`UserId`/`ChirpId`/`FollowResponse`/`LikeResponse` DTOs.

### Declared output (you own this)
- `../checkout/crates/chirp-frontend/src/profile.rs`:
  - Read `params.get("id")`, parse it to a `UserId`, load the `User` via `ctx.client().get_user(id)`
    with loading/error/not-found states.
  - A **follow/unfollow** control calling `ctx.client().set_follow(id, follow)` and reflecting the
    returned `FollowResponse` (updated `follower_count`, `following`) reactively.
  - A **like** action calling `ctx.client().set_like(chirp_id, like)` reflecting the returned
    `LikeResponse` reactively (e.g. on a profile's chirp or a representative like control).
  - Write files only — **no git**.

### Success criteria
- [ ] Compiles against the frozen `AppContext`/`ApiClient`/`profile_view` signatures.
- [ ] Reads the route param, loads the user, handles loading/error/not-found.
- [ ] Follow and like actions call the client and update counts reactively from the responses.
- [ ] No `unwrap`/`expect`/`panic`/`unsafe`; documented; `fmt`/`clippy -D warnings` clean.
- [ ] Native unit test for any off-DOM logic (e.g. id parsing, count/state reduction) where practical.

## Suggested Methodology Files
Domain Mapping: *Building React components → Frontend + Core* (adapt to `ferric` signals); *Writing Rust code → Rust + Core*.
- `frontend/Frontend_Component_Design_Methodology.md`, `frontend/StateManagement_Server_State_Methodology.md` — entity load + optimistic/authoritative count updates.
- `rust/Rust_Ownership_Borrowing_Methodology.md` — signals/context captured in action handlers.
- `core/BestPractices_Coding_Standards_Methodology.md`.
Suggestions only; the ferric-router `app` example (param reading, `/user/:id`) is the authoritative reference.

## Inherited Constraints
`../_GLOBAL.md` §Subtree-Wide Constraints. Use DTOs directly; async via `spawn_local` → signals;
errors to UI; write files only; do not touch `app.rs`/`Cargo.toml`.

## Out-of-Scope Methodologies
Not the api-client REST wiring. Not timeline/compose view work. Not synthesis/decomposition.
