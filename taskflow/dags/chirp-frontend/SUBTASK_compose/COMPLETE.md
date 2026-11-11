# COMPLETE — SUBTASK_compose (login + compose-chirp view)

**Task**: Implement the real `compose_view(ctx: &AppContext) -> VNode` in
`crates/chirp-frontend/src/compose.rs` — the `/compose` route: handle-based **login**
(sets `ctx.session`) and a validated **compose-chirp** form (`create_chirp`), with reactive
loading/error/success handling. Atomic leaf; dependency `SUBTASK_scaffold` (COMPLETED).

## Output produced (owned by this task)

- `checkout/crates/chirp-frontend/src/compose.rs` — replaces the scaffold's compiling stub with
  the real view. ~470 lines incl. docs + native tests.

## What was built

- **Logged-out login**: a handle `<input id="chirp-login-handle">` + *Log in* button. On submit the
  handle is validated with `Username::parse` (trimmed; `ValidationError` shown inline), then
  `ctx.client().login(&LoginRequest{..})` is awaited via `spawn_local`. On success the returned
  `AuthResponse` is written into `ctx.session` as `Some(Session{ user, token })`; a server failure is
  surfaced via `AppError::user_message()` (e.g. `Unauthorized`).
- **Logged-in compose**: gated on an authed session. A `<textarea id="chirp-compose-text">` + *Chirp*
  button. On submit the body is validated with `ChirpText::parse` (inline `ValidationError`, no
  round-trip), then `ctx.client().create_chirp(&CreateChirpRequest{ text, reply_to: None })` is
  awaited; success clears the field and confirms, errors surface as `AppError` state.
- **Reactive loading/disabled**: the submit button shows "Logging in…/Chirping…" and carries
  `disabled` while a request is in flight or the field is blank. Fetch→signal bridge is
  `wasm_bindgen_futures::spawn_local` writing reactive state on completion.
- **Input reading**: `ferric` event handlers are zero-arg, so values are read from the DOM element
  by `id` (`web_sys`), per the subtree constraint. Inputs are uncontrolled (no `value` attr set), so
  re-renders never clobber in-progress typing.

## Key design note (reviewed for the gate)

`ferric` re-renders the whole app from one root effect and gives a route view no per-component setup
phase: a `Signal` created during render is owned by that effect and disposed on its next run (cf. the
`counter` example, which creates state *above* `mount`). A view therefore cannot hold a long-lived
local signal. This view keeps transient UI state (busy/error/success/drafts) in plain thread-local
`ComposeState` and uses the long-lived `session` signal — created once in `AppContext`, outside any
effect — as its render anchor (`request_rerender` re-notifies it without changing its value). Login
success uses the natural `session.set`. This keeps the view panic-free (no stale-signal reads) within
the frozen `AppContext`/`compose_view` contract.

## Composition with the subtree

- Composes against the **frozen** `contracts/app_api.rs` (`AppContext`, `Session`, `ApiClient`
  methods, `compose_view` signature) and `rest_endpoints.md` (`login`→`POST /sessions`,
  `create_chirp`→`POST /chirps`). `chirp-types` DTOs used directly; **no DTO redefined**.
- Did **not** read sibling spoke outputs (`api.rs`/`timeline.rs`/`profile.rs`) — none are COMPLETED;
  composed only against the frozen signatures + scaffold-owned `app.rs`/`error.rs`/`lib.rs` + the
  landed framework crates, per the file-access rules.
- Wrote files only; performed **no git** (the synthesis gate owns all git).

## Verification performed (combined tree, from `checkout/`)

- `cargo build -p chirp-frontend --target wasm32-unknown-unknown` → **success** (the load-bearing identity).
- `cargo test -p chirp-frontend` → **24 passed** (10 new `compose::tests` covering handle/chirp
  validation, trimming, empty/over-length rejection, login/compose enablement, and error-message mapping).
- `cargo fmt -p chirp-frontend -- --check` → **clean**.
- `cargo clippy -p chirp-frontend --all-targets -- -D warnings` (native) and
  `cargo clippy -p chirp-frontend --target wasm32-unknown-unknown -- -D warnings` → **clean**.
- No `unwrap`/`expect`/`panic!`/`unsafe`/`todo!`/`unimplemented!` in runtime code (the two `expect`s are
  `#[cfg(test)]`-only), satisfying the `no_panic_no_unsafe_in_runtime` identity.

## Success criteria

- [x] Compiles against the frozen `AppContext`/`ApiClient`/`compose_view` signatures (native + wasm).
- [x] Login writes `ctx.session`; compose validates with `ChirpText` before calling the API.
- [x] Reactive loading/error/success; `AppError` + `ValidationError` surfaced to the UI.
- [x] No `unwrap`/`expect`/`panic`/`unsafe`; documented; `fmt`/`clippy -D warnings` clean.
- [x] Native unit test for the validation/enablement logic.
