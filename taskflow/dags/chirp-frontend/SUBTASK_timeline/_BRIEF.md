# Task: SUBTASK_timeline — timeline view (src/timeline.rs)

## Task Specification
**Slug**: SUBTASK_timeline
**Task Kind**: standard
**Status**: Pending

### Objective
Implement `timeline_view(ctx: &AppContext) -> VNode` (`src/timeline.rs`): the `/` route that
loads a `Page<Chirp>` via the API client and renders a reactive, keyed chirp list with
loading / error / empty states and cursor-based pagination.

### Context
Part of chirp-frontend (#9) — see `../_GLOBAL.md`. **Dependency**: `SUBTASK_scaffold` (crate,
`AppContext`, frozen view-fn signature, compiling `timeline.rs` stub you replace). You run in
parallel with the other feature spokes and `api_client`; compose against the **frozen**
`ApiClient` signature (`contracts/app_api.rs`) — the scaffold stub is your L1 mock. **Dependent**:
the synthesis gate.

### Inputs
- `../_GLOBAL.md`, `../contracts/app_api.rs`, `../contracts/rest_endpoints.md`.
- The real `ferric` reactivity/vdom API and the `chirp-types` `Chirp`/`Page`/`Cursor`/`TimelineQuery` DTOs.

### Declared output (you own this)
- `../checkout/crates/chirp-frontend/src/timeline.rs` — the timeline view: own local
  loading/data/error signals; kick off `ctx.client().timeline(&query)` via
  `wasm_bindgen_futures::spawn_local` writing those signals on completion; render a keyed list
  (key by `ChirpId`) of chirps (author, text, like count, timestamp); show loading, error
  (`AppError::user_message`), and empty states; offer "load more" using `Page::next_cursor`.
  Write files only — **no git**.

### Success criteria
- [ ] The view compiles against the frozen `AppContext`/`ApiClient`/`timeline_view` signatures.
- [ ] Reactive: a data/loading/error signal change re-renders; list items are keyed by id.
- [ ] Loading, error, and empty states are all handled; pagination uses `next_cursor`.
- [ ] No `unwrap`/`expect`/`panic`/`unsafe`; public items documented; `fmt`/`clippy -D warnings` clean.
- [ ] Any off-DOM logic (e.g. query building, state reduction) has a native unit test where practical.

## Suggested Methodology Files
Domain Mapping: *Building React components → Frontend + Core* (apply the component/state ideas to
`ferric`'s signal model, not React APIs); *Writing Rust code → Rust + Core*.
- `frontend/Frontend_Component_Design_Methodology.md`, `frontend/StateManagement_Server_State_Methodology.md`
  — loading/data/error server-state shape and list rendering (adapt to `ferric` signals).
- `rust/Rust_Ownership_Borrowing_Methodology.md` — closures capturing `Copy` signals / cloned `AppContext` in handlers.
- `core/BestPractices_Coding_Standards_Methodology.md`.
Suggestions only; the ferric `counter` + ferric-router `app` examples are the authoritative view-building reference.

## Inherited Constraints
`../_GLOBAL.md` §Subtree-Wide Constraints. Use `chirp-types` DTOs directly; async via `spawn_local`
→ signals; errors to UI (never panic); write files only; do not touch `app.rs`/`Cargo.toml`
(scaffold owns them — request an additive amendment if the frozen seam is inadequate).

## Out-of-Scope Methodologies
Not the api-client's REST wiring (that is `SUBTASK_api_client`). Not synthesis/decomposition.
