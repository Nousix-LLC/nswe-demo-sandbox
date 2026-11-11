# SYNTHESIS.md — chirp-logged-out-r2

**Gate verdict: PASS**

All five acceptance criteria for issue #35 are met. All CI quality gates pass. Wiring
verified end-to-end. Code review finds no security, correctness, or dead-code violations.
PR created targeting `main` with `Closes #35`.

---

## Acceptance Criteria

| AC | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| AC-1 (REQ-PROD-013) | `GET /api/public/timeline` returns 200 without an Authorization header | ✅ MET | Route registered in `router.rs`; handler has no `AuthUser` extractor; 4 integration tests in `tests/api.rs::public_timeline` (empty-store, all-authors, cursor, no-auth) |
| AC-2 (REQ-PROD-014) | `empty_view()` shows a "what Chirp is" description AND Sign up / Sign in controls | ✅ MET | `empty_view()` in `timeline.rs` renders `div.chirp-empty` with `p.chirp-empty-description` ("Chirp is a place to share short thoughts…") and `div.chirp-empty-actions` with "Create account" and "Sign in" links to `/compose` |
| AC-3 (REQ-PROD-014) | Error path renders a human-readable recoverable message | ✅ MET | `chirp-timeline-error` arm calls `error_banner(err)` and renders a "Retry" button; never shows a blank page |
| AC-4 (REQ-PROD-015) | Sign up / Sign in visible in nav bar AND in empty state | ✅ MET | `nav_bar()` in `app.rs` renders "Sign up" and "Sign in" links to `/compose` (always shown); `empty_view()` also shows "Create account" and "Sign in" — both surfaces covered |
| AC-5 (REQ-UX-002/030-032) | Distinct loading / empty / error / end-of-list state arms | ✅ MET | `view_tree()` state machine has four non-overlapping arms: `chirp-loading` (fetch in-flight), `chirp-timeline-error` (error + retry), `chirp-empty` (no chirps), `chirp-end` ("You're all caught up") |

---

## Wiring Checks

| Check | Status | Evidence |
|-------|--------|----------|
| `timeline_view` calls `pub_timeline`, not `timeline` | ✅ | `request_load` in `timeline.rs`: `ctx.client().pub_timeline(&query)` |
| `pub_timeline` calls `GET /public/timeline` (no `/api/` prefix) using an unauthenticated client | ✅ | `api.rs`: builds a no-auth `Client` and calls `.get("/public/timeline")`, ignoring `self.token` |
| Route in `router.rs` maps to `handlers::public_timeline` | ✅ | `.route("/api/public/timeline", get(handlers::public_timeline))` |
| `chirp_item` renders author as `link("/user/{author_id}", ...)` | ✅ | `chirp_item()` in `timeline.rs`: `link(&format!("/user/{}", chirp.author_id.get()), ...)` |
| Sign up / Sign in links in `nav_bar()` in `app.rs` | ✅ | `nav_bar()` has "Sign up" and "Sign in" links to `/compose` |

---

## CI Gate Results

| Gate | Result |
|------|--------|
| `cargo fmt --check` (workspace) | ✅ PASS |
| `cargo clippy --workspace --all-targets -- -D warnings` | ✅ PASS |
| `cargo clippy -p chirp-server --features postgres -- -D warnings` | ✅ PASS |
| `cargo test --workspace` (42 frontend + 59 server unit + 26 integration + 56 ferric + others) | ✅ PASS |
| `cargo build -p chirp-frontend --target wasm32-unknown-unknown` | ✅ PASS |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | ✅ PASS |
| `image` (Docker build via GitHub Actions Buildx) | Runs in CI on PR |

---

## Code Review

| Area | Finding |
|------|---------|
| Security — no sensitive content in committed files | ✅ CLEAN — diff search found no host addresses, SSH paths, internal addresses, or taskflow references |
| Handler authentication | ✅ CLEAN — `public_timeline` handler has only `State` + `Query` extractors; no `AuthUser` |
| Authenticated endpoint isolation | ✅ CLEAN — `GET /api/timeline` and all other authenticated routes unchanged |
| Soft-removed chirp exclusion | ✅ CLEAN — in-memory: `!store.removed.contains(&chirp.id)`; Postgres: `WHERE removed = FALSE` |
| Dead code | ✅ CLEAN — all new methods (`pub_timeline`, `public_timeline` handler, repository trait method) are wired through; no unused imports |
| Ferric hydrate lint fix | ✅ CLEAN — pre-existing `needless_range_loop` in `ferric/src/hydrate.rs` fixed to pass workspace clippy |

---

## Commits on `work/chirp-logged-out`

| Hash | Description |
|------|-------------|
| `1d8edab` | feat(chirp-server): add public_timeline capability seam (skeleton) |
| `7160514` | Implement InMemoryRepository::public_timeline |
| `ec70b78` | Implement PostgresRepository::public_timeline |
| `d57335d` | test(chirp-server): add integration tests for public_timeline endpoint |
| `ac3471c` | style(chirp-server): rustfmt public_timeline stub signature in api.rs |
| `908d703` | feat(chirp-frontend): logged-out visitor experience (AC-1–AC-5) |

All 6 commits carry `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`.

---

## Spoke Completion Records

- `SUBTASK_server/COMPLETE.md` — 89/89 tests, fmt + clippy clean, all server layers implemented
- `SUBTASK_frontend/COMPLETE.md` — 42/42 tests, fmt + clippy + wasm clean, all frontend changes implemented
