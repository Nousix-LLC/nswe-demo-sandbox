# Task: SUBTASK_compose — login + compose-chirp view (src/compose.rs)

## Task Specification
**Slug**: SUBTASK_compose
**Task Kind**: standard
**Status**: Pending

### Objective
Implement `compose_view(ctx: &AppContext) -> VNode` (`src/compose.rs`): the `/compose` route
offering handle-based **login** (which sets `ctx.session`) and a validated **compose-chirp**
form that posts a new chirp, with reactive loading/error handling.

### Context
Part of chirp-frontend (#9) — see `../_GLOBAL.md`. **Dependency**: `SUBTASK_scaffold` (crate,
`AppContext`/`Session`, frozen view-fn signature, compiling `compose.rs` stub you replace). Runs
in parallel with the other spokes; composes against the frozen `ApiClient` (scaffold stub = L1
mock). **Dependent**: the synthesis gate.

### Inputs
- `../_GLOBAL.md`, `../contracts/app_api.rs`, `../contracts/rest_endpoints.md`.
- The real `ferric` API and `chirp-types` `LoginRequest`/`AuthResponse`/`CreateChirpRequest`/
  `ChirpText`/`Username`/`ValidationError` DTOs.

### Declared output (you own this)
- `../checkout/crates/chirp-frontend/src/compose.rs`:
  - **Login**: a handle field → `ctx.client().login(&LoginRequest{..})`; on success write
    `Some(Session{user, token})` into `ctx.session`. Surface `AppError` (e.g. `Unauthorized`).
  - **Compose**: a text field validated through `ChirpText::parse` (show `ValidationError`
    inline) → `ctx.client().create_chirp(&CreateChirpRequest{..})`; reactive submit with
    loading/disabled state and success/error feedback. Gate the form on an authed session.
  - Own the input-value-reading pattern: `ferric` `EventKind::Input` handlers are zero-arg, so
    read the field's current value from the DOM element (e.g. `web_sys` by id) into a signal.
  - Write files only — **no git**.

### Success criteria
- [ ] Compiles against the frozen `AppContext`/`ApiClient`/`compose_view` signatures.
- [ ] Login writes `ctx.session`; compose validates with `ChirpText` before calling the API.
- [ ] Reactive loading/error/success states; `AppError` + `ValidationError` surfaced to the UI.
- [ ] No `unwrap`/`expect`/`panic`/`unsafe`; documented; `fmt`/`clippy -D warnings` clean.
- [ ] Native unit test for the validation/enablement logic where off-DOM-practical.

## Suggested Methodology Files
Domain Mapping: *Building React components → Frontend + Core* (adapt to `ferric` signals); *Writing Rust code → Rust + Core*.
- `frontend/Frontend_Component_Design_Methodology.md` — form component shape, controlled-input state.
- `rust/Rust_Error_Handling_Methodology.md` — `ValidationError`/`AppError` handling without panics.
- `core/BestPractices_Error_Handling_Methodology.md`.
Suggestions only; the ferric examples (event binding, signals) are the authoritative reference; note the zero-arg event-handler constraint in `../_GLOBAL.md`.

## Inherited Constraints
`../_GLOBAL.md` §Subtree-Wide Constraints. Use DTOs directly; async via `spawn_local` → signals;
errors to UI; write files only; do not touch `app.rs`/`Cargo.toml`.

## Out-of-Scope Methodologies
Not the api-client REST wiring. Not timeline/profile view work. Not synthesis/decomposition.
