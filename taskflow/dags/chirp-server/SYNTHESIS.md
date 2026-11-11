# SYNTHESIS — chirp-server (work-item #8) — SUBTASK_reverify_gate

## Verdict

**gate: PASS**  ·  round: 1 (re-verification after F1 remediation; ceiling = 3)
**PR: https://github.com/Nousix-LLC/nswe-demo/pull/19** (OPEN, `work/chirp-server` → `main`, body ends `Closes #8`)

The F1 contract violation that blocked the round-0 gate is **resolved and mechanically re-verified**.
All four authoritative mechanical identities pass, all four verification checks are clean over the
combined output, the branch is pushed, and the PR into `main` is open. This record supersedes the
interim round-0 FAIL as the authoritative fold/observation record at the hub.

> The round-0 gate refused to open a PR on broken work (DTO-validation surfaced as `422` plain text,
> not the contract's `400 ApiError`). The single injected fix-task (`SUBTASK_fix_validation_error_mapping`,
> commit `714d50f`) closed exactly that gap and nothing else. This gate re-ran everything cold and
> confirms the output now conforms — so delivery proceeds. No code was modified in the gate.

## Checks

| Check | Result | Mechanical evidence | Notes |
|-------|--------|---------------------|-------|
| build (`cargo build --workspace`) | **pass** | exit 0 — `Finished dev profile` | crate slots into the virtual workspace cleanly |
| test (`cargo test`) | **pass** | exit 0 — chirp-server **24 unit + 20 integration = 44 passed, 0 failed** (lib bin 0; 2 ignored doc-examples: auth + json); rest of workspace green; **no DB** | unit count rose 23→24 (new `error.rs` `InvalidBody` unit test); the F1 integration test now asserts the contract |
| fmt (`cargo fmt --check`) | **pass** | exit 0 | clean |
| clippy (`cargo clippy --all-targets -- -D warnings`) | **pass** | exit 0 — `Finished` | no warnings; lints test code too ⇒ corroborates no detached dead code |
| wiring | **pass** | `router.rs` mounts all 9 `/api/…` routes + `GET /healthz` + `.fallback_service(spa)` SPA; all handlers call through `state.repo.*`; new `pub mod json;` is re-exported and consumed by the three body handlers; clippy `-D warnings` clean ⇒ no orphaned items | every in-scope endpoint routed + reachable; no repository bypass; the F1 fix is live on the HTTP surface, not dead code |
| contract | **pass** | (a) no `chirp-types` DTO re-declared in `chirp-server` (grep clean); (b) **validation errors now surface as `ApiError`/`ErrorCode`** — F1 re-check below | both clauses of the `contract` identity hold; the round-0 clause (b) failure is cleared |
| duplication | **pass** | one producer per `ownership` manifest artifact; the fix added only `src/api/json.rs` (new) + in-ownership edits to `error.rs`/`handlers.rs`/`api/mod.rs`/`lib.rs`/`tests`; no re-declared DTO; no duplicated shared logic | ownership coverage + respect hold; `ValidatedJson` is a single transport wrapper owned by the api layer |
| code-review | **pass** (1 tracked minor, non-gating) | combined diff reviewed: clean, layered transport→service→repository; `Arc<dyn ChirpRepository>` seam; typed-error discipline intact; the fix is the idiomatic axum custom-`FromRequest` extractor, well-documented | F2 (rustdoc intra-doc-link nits under `RUSTDOCFLAGS=-D warnings`) remains non-gating tracked debt — `cargo doc -D warnings` is not in the gate assertion set and `missing_docs` is satisfied |

## F1 re-verification (the round-0 blocker)

**Resolved.** A well-formed-JSON body with an invalid DTO field value now returns the contract's
**400 `VALIDATION_ERROR`** `ApiError` with non-empty `details` — confirmed by three independent lines of evidence:

1. **Flipped characterization test passes.** `tests/api.rs::errors::invalid_dto_field_is_rejected_as_400_validation_error`
   (renamed from the round-0 `..._as_422_not_contract_400`) asserts `status == 400 BAD_REQUEST`,
   `api_error().code == ErrorCode::ValidationError`, and `!details.is_empty()`. It passes. **No test pins `422`**
   anywhere in the crate (remaining `422` strings are doc/comment text describing the fixed behavior).
2. **Source path verified, not summarized.** `src/api/json.rs` defines `ValidatedJson<T>: FromRequest` that
   delegates to `axum::Json` and maps `JsonRejection` via `?` → `From<JsonRejection> for ServerError` →
   `ServerError::InvalidBody`. `error.rs` `code()` maps both `InvalidBody` and `Validation` → `ErrorCode::ValidationError`,
   `IntoResponse` maps `ValidationError → StatusCode::BAD_REQUEST (400)`, and `into_api_error()` lifts `InvalidBody`
   into a non-empty `FieldError` detail. The three body-bearing handlers (`create_user`, `login`, `create_chirp`)
   extract with `ValidatedJson<T>` — so the 400 arm is now reachable via the HTTP surface.
3. **Unit test corroboration.** `error::tests::invalid_body_maps_to_validation_code_with_a_generic_field_detail` passes.

**No regression:** every other error row still holds via passing integration tests — 401 (`invalid_token`,
`missing_token`), 403 (`self_follow`), 404 (`login_unknown_handle`, `unknown_user_id`, `follow_absent_user`,
`reply_to_absent_chirp`, `like_absent_chirp`), 409 (`duplicate_username`); timeline limit-clamp holds. No new
duplication, no re-declared DTO, no dead code introduced by the fix.

**Documented limitation (accepted, contract-satisfying):** the offending field name is not structurally
recoverable from axum's `JsonRejection` without adding `serde_path_to_error`, so `details` carries a single
generic `FieldError { field: "body", message: <rejection text> }`. This satisfies the contract's "populate
details (Vec<FieldError>)" requirement; the minimal-dependency trade-off is reasonable and does not weaken the
wire contract.

## Diff manifest (files added/changed vs `main`, `work/chirp-server` @ `714d50f`)

`git diff --stat main...HEAD`: **16 files changed, +3437 / −4**

```
crates/chirp-server/Cargo.toml                   +68
crates/chirp-server/README.md                    +148
crates/chirp-server/src/lib.rs                   +48
crates/chirp-server/src/error.rs                 +285
crates/chirp-server/src/api/mod.rs               +33
crates/chirp-server/src/api/auth.rs              +96
crates/chirp-server/src/api/state.rs             +44
crates/chirp-server/src/api/json.rs              +61   (new — ValidatedJson extractor, the F1 fix)
crates/chirp-server/src/api/handlers.rs          +339
crates/chirp-server/src/api/router.rs            +106
crates/chirp-server/src/repository/mod.rs        +187
crates/chirp-server/src/repository/in_memory.rs  +722
crates/chirp-server/src/main.rs                  +69
crates/chirp-server/tests/api.rs                 +618
crates/chirp-server/static/index.html            +31
Cargo.lock                                       +586/−4
```

Commits on `work/chirp-server` atop `main` (`25e90c0`): `6ba64d0` (scaffold+repository) · `6f32dc0` `8c0336f`
`d9c19f0` (api layer) · `ea08e73` (integration tests + README) · **`714d50f` (F1 fix — validation→400 `ApiError`)**.

## Notes

- Authoritative checks were re-run cold from the ONE shared clone at `checkout/` (contract `clone_path`);
  the clone is clean and on `work/chirp-server` @ `714d50f`. `main` is untouched (local and `origin/main`
  both `25e90c0`; `714d50f` is not an ancestor of `main`). The only write to `main` is via PR #19. No
  force-push; no commit-attribution trailers were added.
- The subtree is complete against the acceptance surface: repository trait + in-memory default (no DB),
  all 9 REST endpoints + `/healthz` + static/SPA fallback + `tracing`, typed errors for 400/401/403/404/409/500
  surfacing as `ApiError`/`ErrorCode`, README + rustdoc, and a 44-test suite. The round-0 F1 gap is closed.
- Delivery mechanics: branch pushed to `origin/work/chirp-server`; PR #19 opened into `main` with the
  contract's title (`conventions.pr.title`) and a body ending `Closes #8`. The overseer observes this hub
  `SYNTHESIS.md` at the observation seam (`_FORK.md`, `reap-whole-after-land`); a landable PR now exists.
- F2 (rustdoc intra-doc-link cleanup) remains tracked, non-gating debt for the CI work-items (#10–#13).

## Remediation / escalation

None required — gate = PASS at round 1. No fix-tasks injected; no escalation. The remediation ceiling (3)
was not approached.

## Coverage assertion (gate = PASS ⇒ all four lines asserted)

- ownership coverage: every declared `ownership` artifact has exactly one producer  ✓
- wiring: every component registered + consumed (9 routes + `/healthz` + SPA fallback; `json` module consumed; no dead code)  ✓
- identities: every contract identity evaluated against real command output, none plugged; errors surface as `ApiError`/`ErrorCode` (incl. the F1 400 path)  ✓
- review: combined output reviewed; no block- or major-severity finding open (F2 minor is tracked, non-gating)  ✓
