# TEST_NOTES.md — end-to-end integration tests + docs (handoff to `SUBTASK_synthesis_gate`)

The **verify-by-test + document** stage of the `chirp-server` subtree. End-to-end API integration
tests, the crate `README.md`, and rustdoc verification were authored against the **real committed
server** (no behavior changed) and committed to `work/chirp-server`. This note is what the gate reads
to confirm coverage before it runs the authoritative build.

## Clone / branch / commit pointers

| What | Value |
|------|-------|
| Clone path | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout` |
| Branch | `work/chirp-server` |
| Predecessor HEAD (api layer) | `d9c19f0` |
| This stage's commit | `ea08e73` — `test(chirp-server): end-to-end API integration suite + README` |
| Backing store under test | `InMemoryRepository` — **no database, no network bind** |

## Harness

`crates/chirp-server/tests/api.rs` — one integration-test crate. Every test builds the real app via
`chirp_server::build_router(AppState::new(Arc::new(InMemoryRepository::new())))` and drives it
in-process with `tower::ServiceExt::oneshot`; requests are built from the `chirp-types` DTOs and
responses decoded back into them, so each test asserts **both** the HTTP status **and** the decoded
wire type. Each test constructs its own `TestApp`, so the suite is isolated and order-independent.
Dev-deps used (`tower` `util`, `http-body-util`) were already provisioned by the scaffold spoke.

## Local verification (all clean)

| Check | Command | Result |
|-------|---------|--------|
| build (workspace) | `cargo build --workspace` | ✅ exit 0 |
| test | `cargo test -p chirp-server` | ✅ **43 passed, 0 failed**, 1 ignored (pre-existing auth doc-example), no DB |
| fmt | `cargo fmt -p chirp-server --check` | ✅ clean |
| clippy | `cargo clippy -p chirp-server --all-targets -- -D warnings` | ✅ no warnings (lints the test code too) |
| doc (default) | `cargo doc -p chirp-server --no-deps` | ✅ exit 0 (builds; see finding F2 for `-D warnings` nits) |

Test breakdown: **23 library unit tests** (14 repository + 5 handler + 4 error — predecessors') +
**20 end-to-end integration tests** (this stage, `tests/api.rs`).

## Integration test inventory (`tests/api.rs`)

### `happy_path` (9 tests) — the acceptance surface, end to end
| Test | Asserts |
|------|---------|
| `healthz_reports_liveness` | `GET /healthz` → 200; body `{status:"ok", service:"chirp-server", version}` |
| `create_user_then_fetch_profile_round_trips` | `POST /api/users` → 201 + `User` (zeroed counts); `GET /api/users/{id}` → 200 returns the identical `User` |
| `login_issues_a_token_that_authenticates_requests` | `POST /api/sessions` → 200 + `AuthResponse`; token then authenticates `GET /api/timeline` |
| `post_chirp_appears_on_authors_own_timeline` | `POST /api/chirps` (auth) → 201 + `Chirp` (author id, zero likes); chirp shows on the author's timeline |
| `home_timeline_is_scoped_to_self_plus_followees_newest_first` | timeline = self + followees, newest-first; an unfollowed user's chirp is excluded |
| `follow_then_unfollow_moves_the_follower_count` | follow → `following=true`, `followerCount=1`, visible on profile; idempotent re-follow stays 1; unfollow → 0 |
| `like_then_unlike_moves_the_like_count` | like → `liked=true`, `likeCount=1`; idempotent; unlike → 0 |
| `reply_chirp_links_to_its_parent` | `POST /api/chirps` with `replyTo` → 201 + `Chirp.replyTo == parent` |

### `errors` (10 tests) — the contract `error_mapping` table (status + decoded `ApiError`)
| Test | Asserts |
|------|---------|
| `duplicate_username_is_409_conflict` | 409 + `ApiError.code == CONFLICT` |
| `unknown_user_id_is_404_not_found` | 404 + `NOT_FOUND` |
| `login_unknown_handle_is_404_not_found` | 404 + `NOT_FOUND` |
| `missing_token_is_401_unauthorized` | 401 + `UNAUTHORIZED` |
| `invalid_token_is_401_unauthorized` | 401 + `UNAUTHORIZED` |
| `self_follow_is_403_forbidden` | 403 + `FORBIDDEN` |
| `follow_absent_user_is_404_not_found` | 404 + `NOT_FOUND` |
| `like_absent_chirp_is_404_not_found` | 404 + `NOT_FOUND` |
| `reply_to_absent_chirp_is_404_not_found` | 404 + `NOT_FOUND` |
| `invalid_dto_field_is_rejected_as_422_not_contract_400` | **characterization** of finding F1 (see below) |

### `pagination` (2 tests)
| Test | Asserts |
|------|---------|
| `timeline_paginates_newest_first_with_cursor_and_limit` | `limit=2` over 5 chirps paginates newest-first across 3 pages via `nextCursor`; pages cover all 5 once; last page has no cursor |
| `timeline_clamps_an_oversized_limit_without_erroring` | `limit=100000` is clamped (not rejected); all items returned, no cursor |

## Coverage map — issue #8 acceptance criteria → test(s)

| Acceptance criterion (`_GLOBAL.md`) | Covered by |
|-------------------------------------|-----------|
| Crate slots into workspace; `cargo build --workspace` succeeds | `cargo build --workspace` ✅ (authoritative run is the gate's) |
| All REST endpoints over `chirp-types` DTOs | all 9 API routes + `/healthz` exercised across `happy_path` + `errors` (status **and** DTO asserted) |
| Typed errors → HTTP status + `ApiError`/`ErrorCode` | `errors::*` assert `ApiError.code` for 401/403/404/409 (400 → see F1) |
| Persistence behind trait; in-memory default; **no DB** for `cargo test` | harness mounts `InMemoryRepository`; suite runs with no infra |
| Static serving + SPA fallback; `GET /healthz`; `tracing` | `healthz_reports_liveness` covers the probe. Static/SPA + tracing are the api-layer's wiring and are verified by that spoke's `SYNTHESIS.md`; they carry no new behavior in this stage and are not re-asserted here (see note) |
| Unit + integration tests pass; `fmt`/`clippy -D warnings` clean | local run table above ✅ |
| `README.md` (endpoints + run + repository rationale); rustdoc on public items | `crates/chirp-server/README.md` authored; `missing_docs` satisfied (clippy `-D warnings` clean) |
| PR into `main` (`Closes #8`); `SYNTHESIS.md` verdict | **gate's job** (`SUBTASK_synthesis_gate`) |

Note on static/SPA + tracing: an `oneshot`-level test could assert the SPA fallback returns the
placeholder `index.html` for an unknown non-`/api` path, but that exercises `tower-http::ServeDir`
(already covered by the api-layer spoke) rather than this crate's logic, and the committed
`static/index.html` placeholder is a #9 concern. Left to the api-layer's verification to avoid
testing the framework.

## README summary

`crates/chirp-server/README.md`: one-screen overview + quick-start `curl` flow (create user → login
→ chirp → timeline), the configuration env-var table, the authoritative endpoint/auth/status table,
the error-contract table (with the F1 gap called out), the repository-trait rationale ("why in-memory
is the default" + "how to swap the backing store" with a `SqlRepository` sketch), and the
test/scope/status sections.

## Findings for the gate (behavior NOT modified — recorded, not papered over)

### F1 — DTO validation returns **422 plain text**, not the contract's **400 `VALIDATION_ERROR`** (MINOR)
- **Observed.** A well-formed-JSON body with an invalid field value (e.g. `username: "has space"`,
  or over-length `ChirpText`) returns **`422 Unprocessable Entity`** with a plain-text body
  (`Failed to deserialize the JSON body into the target type: …`).
- **Expected (contract).** `contracts/_MANIFEST.yaml` `error_mapping` and `API_NOTES.md` document a
  DTO-validation failure as **`400 VALIDATION_ERROR`** carrying an `ApiError` with field `details`.
- **Root cause.** Validation happens at the serde boundary of the plain `axum::Json<T>` extractor
  (the `chirp-types` value objects use `#[serde(try_from = "String")]`). A `try_from` failure becomes
  axum's default `JsonRejection::JsonDataError` → 422, which never routes through
  `ServerError::Validation` / `IntoResponse`. The 400 `VALIDATION_ERROR` branch of `IntoResponse` is
  consequently unreachable via the HTTP surface today.
- **Impact.** Low — invalid input is still safely rejected and never persisted; only the error
  *status + body shape* deviate. No happy path or other error code is affected.
- **Recommended fix (small, additive, no behavior change elsewhere).** Introduce a custom JSON
  extractor (or a `From<JsonRejection> for ServerError`) that maps a deserialization failure to
  `ServerError::Validation`, so the handlers emit a 400 `ApiError` with field `details` as the
  contract specifies. The characterization test `invalid_dto_field_is_rejected_as_422_not_contract_400`
  pins current behavior and will visibly flip when this is fixed.
- **Disposition for the gate.** This is a contract-vs-implementation gap the api-layer spoke's notes
  did not flag (its route table claims "400 invalid handle/body"). Recommend scheduling it as a
  remediation fix-task if issue #8 requires strict error-contract conformance; it does not block the
  functional surface.

### F2 — `cargo doc` intra-doc-link warnings under `-D warnings` (TRIVIAL / tracked)
- **Observed.** Default `cargo doc -p chirp-server` builds (exit 0). Under the stricter
  `RUSTDOCFLAGS="-D warnings"` it reports **24** intra-doc-link nits in predecessor-owned modules:
  ~19 "redundant explicit link target" (`[`X`](X)` → `[`X`]`), 2 unresolved `crate::main` links
  (lib → binary item) in `src/api/router.rs`, 2 public-doc-links-to-private-item (`static_dir`,
  `Store`), and 2 ambiguous links (`axum::serve` fn-vs-module; `async_trait` crate-vs-macro).
- **Scope note.** None are `missing_docs` (that bar is met — the crate is `clippy -D warnings`
  clean), none are gate identities (`cargo doc -D warnings` is not in the assertion set), and all sit
  in files owned by the scaffold/api-layer spokes. They were deliberately **not** mass-rewritten in
  this stage to avoid churning predecessor-owned doc comments across six files right before the gate.
- **Recommended fix.** A one-pass doc-lint cleanup (`cargo doc` with `-D rustdoc::all` locally) —
  mechanical and zero-behavior. Optionally add `RUSTDOCFLAGS=-D warnings cargo doc` to CI (#10–#13).

## Out of scope for this stage (left to the gate / later work-items)
- The authoritative full-workspace `cargo test` + four-check gate, the push of `work/chirp-server`,
  and the PR into `main` (`Closes #8`) — `SUBTASK_synthesis_gate`.
- The real frontend SPA (#9); deploy/CI (#10–#13).
