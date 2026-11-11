# COMPLETE — SUBTASK_profile (chirp-frontend #9)

## What was done
Replaced the scaffold stub with the real `src/profile.rs`: the `/user/:id` profile route
(`profile_view(ctx: &AppContext, params: &Params) -> VNode`) realizing the frozen
`contracts/app_api.rs` signature, composing against the frozen `AppContext` / `ApiClient` and the
`chirp-types` DTOs used directly (no DTO redefined).

Behaviour delivered:
- **Route param → load.** Reads `params.get("id")`, parses it to a `UserId`, and loads the `User`
  via `ctx.client().get_user(id)`. Renders **loading**, **invalid-id**, **not-found**
  (`ErrorCode::NotFound`), **error** (with a Retry control), and **loaded** states; every
  `ApiError`/network failure surfaces to the UI as `AppError` text (never swallowed, never panics).
- **Follow / unfollow.** Calls `ctx.client().set_follow(id, target)` and folds the returned
  `FollowResponse` (`following`, `follower_count`) back into the view reactively. Gated on a
  logged-in viewer; self-follow is shown as "This is you".
- **Like.** A representative like control (the profile endpoint returns no chirps, which the brief
  sanctions) calls `ctx.client().set_like(chirp, target)` and reflects the returned `LikeResponse`
  (`liked`, `like_count`) reactively. Gated on being logged in.

## Key design decision (reactivity under `ferric`)
`ferric` has no per-component state: `mount` wraps the whole-app render in one reactive effect, and
any signal created *during* a render is disposed on the next re-render (so handlers must only
capture persistent, root-owned signals). `app.rs` is owned by the scaffold and out of scope, so the
view keeps its mutable state in a module-local `thread_local` store of **plain data** (survives
re-renders) and drives reactive re-renders through the persistent `AppContext::session` signal:
`profile_view` reads `session` every render (also the legitimate logged-in check), and async
completions / click handlers update the store then nudge `session` so `ferric` re-renders and the
view re-reads the store. Nudging a runtime-root signal is panic-free; capturing a per-render signal
in a handler would not be. Async `fetch` is bridged with `wasm_bindgen_futures::spawn_local`,
isolated behind `#[cfg(target_arch = "wasm32")]` (mirroring `ferric` / `ferric-router`) so the
module also compiles and unit-tests natively.

## Declared output
- `checkout/crates/chirp-frontend/src/profile.rs`

## Verification (read-only; no git — per subtree git discipline, the gate owns all git)
- `rustfmt --edition 2021 --check src/profile.rs` → clean.
- `cargo test -p chirp-frontend` → 30 passed (6 new profile tests: id parse accept/reject, toggle
  target, follow label, like label, loading-reset).
- `cargo clippy -p chirp-frontend --all-targets -- -D warnings` → clean (native).
- `cargo clippy -p chirp-frontend --target wasm32-unknown-unknown -- -D warnings` → clean.
- `cargo build -p chirp-frontend --target wasm32-unknown-unknown` → succeeds (combined tree, with
  the now-landed real `api.rs` / `compose.rs`).
- No `unwrap`/`expect`/`panic!`/`todo!`/`unimplemented!`/`unsafe` in the module.

## Composition notes for the synthesis gate
- DTOs used directly from `chirp_types::prelude` (`User`, `UserId`, `ChirpId`, `FollowResponse`,
  `LikeResponse`, `ErrorCode`); no parallel DTO defined. The only new types are view-state
  (`Load`, `ProfileState`), not wire types.
- `set_like` is wired to a representative chirp id (`ChirpId::new(profile_id.get())`) because the
  profile endpoint returns no chirps — documented in-code and in the UI ("representative like
  control"). If #8/synthesis prefers a concrete authored chirp, that is an additive change behind
  the same control.
- Owns only `src/profile.rs`; touched no sibling file, `app.rs`, or `Cargo.toml`; ran no git.
