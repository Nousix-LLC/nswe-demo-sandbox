# COMPLETE — SUBTASK_integration_tests_and_docs

**Task**: End-to-end API integration tests + docs for `chirp-server` (work-item #8).
**Status**: COMPLETED (Atomic). **Evaluation**: single responsibility — characterize-and-document the
committed server; no behavior changed.

## What was produced

1. **`crates/chirp-server/tests/api.rs`** (committed `ea08e73` on `work/chirp-server`) — a 20-test
   end-to-end integration suite. Each test mounts the **real** server via
   `chirp_server::build_router(AppState::new(Arc::new(InMemoryRepository::new())))` and drives it
   in-process with `tower::ServiceExt::oneshot` (no DB, no network), asserting **both** the HTTP
   status **and** the decoded `chirp-types` DTO across the full acceptance surface (users, sessions,
   chirps, home timeline + cursor pagination, follow/unfollow and like/unlike counts, replies,
   health) and the contract `error_mapping` table (401/403/404/409 as `ApiError`).
2. **`crates/chirp-server/README.md`** (committed `ea08e73`) — overview, quick-start `curl` flow,
   configuration env vars, authoritative endpoint/auth/status table, error-contract table, and the
   repository-trait rationale (in-memory default + how to swap the backing store).
3. **`TEST_NOTES.md`** (this workspace) — the handoff the gate reads: harness, verification table,
   full test inventory, the issue-#8 acceptance-criteria → test coverage map, README summary, and two
   recorded findings (F1, F2).

## Verification (local, on committed tree `ea08e73`)

| Check | Result |
|-------|--------|
| `cargo test -p chirp-server` | ✅ 43 passed / 0 failed (23 lib unit + 20 integration), 1 pre-existing ignored doc-example, no DB |
| `cargo build --workspace` | ✅ exit 0 |
| `cargo fmt -p chirp-server --check` | ✅ clean |
| `cargo clippy -p chirp-server --all-targets -- -D warnings` | ✅ clean (lints the test code too) |
| `cargo doc -p chirp-server` (default) | ✅ builds (exit 0) |
| git | on `work/chirp-server`, `main` untouched @ `25e90c0`, branch **not** pushed, no attribution trailers |

## Composition with the parent

Feeds `SUBTASK_synthesis_gate`: the gate runs the authoritative four-check build/test/fmt/clippy, then
pushes `work/chirp-server` and opens the PR into `main` (`Closes #8`). `TEST_NOTES.md` gives the gate
the coverage map plus two findings to weigh:
- **F1 (minor):** DTO-validation failures surface as **422 plain text**, not the contract's **400
  `VALIDATION_ERROR`** `ApiError` (axum default `JsonRejection`). Characterized by a test; recommended
  fix is a small custom JSON extractor. Does not block the functional surface.
- **F2 (trivial):** `cargo doc -D warnings` reports 24 intra-doc-link nits in predecessor-owned
  modules (not `missing_docs`, not a gate identity); recommended as a one-pass follow-up cleanup.

## Constraints honored

Composed against the real committed code via the `lib.rs` app builder; no handler/repository behavior
changed; all wire types imported from `chirp-types` (no DTO re-declared); no DB/external infra for
`cargo test`; all work in the one shared clone on `work/chirp-server`; `main` never touched; branch
not pushed and no PR opened (gate's job); no commit-attribution trailers.
