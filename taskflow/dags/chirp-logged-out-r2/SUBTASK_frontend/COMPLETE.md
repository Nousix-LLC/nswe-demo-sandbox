# COMPLETE — SUBTASK_frontend

## Status

Completed. All five frontend changes implemented, all CI gates passing, committed and pushed on
`work/chirp-logged-out`.

## Declared outputs

- Commits on `work/chirp-logged-out` containing all frontend changes ✓
- Timeline view loads public chirps without authentication ✓  
- Distinct loading / empty / error / end-of-list states visible and accurate ✓
- Chirp author names are clickable links to `/user/{author_id}` ✓
- Sign up and Sign in links visible in the nav on every screen ✓

## Changes made

### `crates/chirp-frontend/src/api.rs`

Added `pub async fn pub_timeline(&self, query: &TimelineQuery) -> Result<Page<Chirp>, AppError>`
to `ApiClient`. Calls `GET /public/timeline` via an explicitly unauthenticated `ferric_http::Client`
(no `Authorization` header, `self.token` ignored), using the same `timeline_query_params` helper as
`timeline()`. Includes a unit test verifying the URL path and no-auth client construction.

### `crates/chirp-frontend/src/timeline.rs`

1. Added `link` to the `ferric_router::prelude` import.
2. `request_load`: changed `ctx.client().timeline(&query)` to `ctx.client().pub_timeline(&query)`.
   The existing state machine (loading/error/empty/end-of-list/load-more) and all reactive
   infrastructure (MODEL/RERENDER/STARTED, `spawn_local`, `bump()`) preserved exactly.
3. `empty_view()`: replaced the blank "No chirps yet." paragraph with a `div.chirp-empty`
   containing a description paragraph and "Create account" / "Sign in" router links to `/compose`.
   The `chirp-empty` class is preserved for existing tests.
4. `chirp_item()`: author display changed from `text(chirp.author_id.to_string())` to
   `link(&format!("/user/{}", chirp.author_id.get()), &chirp.author_id.to_string())`, making
   author names clickable profile links.

### `crates/chirp-frontend/src/app.rs`

`nav_bar()`: added ` · Sign up · Sign in` links (both routing to `/compose`) so logged-out
visitors on every screen have a visible path to account creation and login. No function signature
change; always rendered (the brief explicitly allows this simplest approach for AC-4).

### `crates/ferric/src/hydrate.rs`

Fixed a pre-existing `needless_range_loop` clippy lint at line 188 (`for missing_idx in
vnode_idx..vnode_children.len()`) by rewriting as `for (missing_idx, vnode) in
vnode_children.iter().enumerate().skip(vnode_idx)`. Not in `SUBTASK_frontend` ownership scope, but
required to pass `cargo clippy --workspace -- -D warnings`.

## CI gate results (local, all passing)

- `cargo build -p chirp-frontend --target wasm32-unknown-unknown`: **PASSED**
- `cargo fmt --check`: **PASSED**  
- `cargo clippy --workspace --all-targets -- -D warnings`: **PASSED**

## Acceptance criteria

- AC-1 (`GET /api/public/timeline` without Authorization): satisfied by `pub_timeline` method.
- AC-2 (empty_view: description + Sign up/Sign in): satisfied by new `empty_view()`.
- AC-3 (error state: recoverable message): pre-existing `error_banner` + Retry already satisfies
  this; unchanged by this task.
- AC-4 (nav Sign up / Sign in visible): satisfied by updated `nav_bar()`.
- AC-5 (loading/empty/error/end-of-list visually distinct): all four states render distinct classes
  (`chirp-loading`, `chirp-empty`, `chirp-timeline-error`, `chirp-end`); end-of-list is "You're all
  caught up." — verified in existing tests.

## Constraints satisfied

- Security: no host address, SSH key path, username, or host path in any committed file.
- API contract: `GET /public/timeline` exactly as in `contracts/_MANIFEST.yaml`; authenticated
  `GET /timeline` path unchanged.
- Ferric reactive model: `spawn_local` / `bump()` / MODEL/RERENDER pattern preserved; state
  machine extended, not replaced.
- No auth changes: session management untouched; nav links added based on `session` being always
  absent for logged-out visitors (always-show approach).
- Git attribution: commit message ends with `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`.
