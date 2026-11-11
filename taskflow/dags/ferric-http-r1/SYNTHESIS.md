# SYNTHESIS — ferric-http-r1 (issues #132, #148 — usable_early verification gate)

## Verdict
gate: **PASS**
round: 1
PR: **https://github.com/Nousix-LLC/nswe-demo/pull/210**
(OPEN — base `main` ← `work/ferric-http-r1`, `Closes #132`, `Closes #148`)

The `ferric-http` crate on `main` already satisfies every acceptance criterion for
issue #148 (`usable_early` scope: REQ-HTTP-001–008, 013, BAR-FERRIC-017). No new
functional code was required. This work-item adds `crates/ferric-http/CHANGELOG.md`
(a formal documentation of the frozen public API surface and acceptance-criteria
evidence), delivered as PR #210. All 6 CI jobs passed on the first run.

## Decompose-evaluation (why atomic)

Declared **Atomic**. The scope is single-responsibility: verify the existing
`ferric-http` crate satisfies the usable_early acceptance criteria, document the
frozen API surface, and deliver a PR that closes #132 and #148. No new functional
code paths span distinct concerns; the documentation commit is inseparable from the
verification. Decomposing would have been ceremony, not a genuine split.

## CI gate — machine verdict (run 41812754296, PR #210)

| Job | Result | Duration |
|-----|--------|----------|
| `fmt` | ✅ pass | 15 s |
| `clippy` (workspace + postgres feature) | ✅ pass | 24 s |
| `test` | ✅ pass | 30 s |
| `wasm` | ✅ pass | 23 s |
| `doc` | ✅ pass | 17 s |
| `image` | ✅ pass | 2 m 52 s |

**All 6 CI jobs: PASS.**

## Acceptance criteria — #148 (usable_early)

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `Client` accepts a base URL at configuration time | ✅ `ClientBuilder::base_url()` |
| 2 | `RequestBuilder` chains URL resolution per RFC 3986: GET, POST, PUT, DELETE | ✅ `Client::{get,post,put,delete}` + `resolve_url()` |
| 3 | Typed `body::<T>()` serializes `T` to JSON (Content-Type: application/json) | ✅ `RequestBuilder::json()` |
| 4 | Typed `send::<T>()` deserializes response body as `T` | ✅ `RequestBuilder::send_json::<T>()` |
| 5 | Matchable `Error` enum: network failure, non-2xx status, deserialization failure | ✅ `Error::{Network,Status,Deserialize,...}` |
| 6 | Non-2xx responses surface as `Err` by default | ✅ `send_json()` → `Err(Error::Status)` |
| 7 | Request headers can be set per-request | ✅ `RequestBuilder::header()` |
| 8 | All #6 baseline prelude surfaces preserved (no removal or redefinition) | ✅ frozen surface intact |
| 9 | Stated HTTP client examples compile | ✅ doctests in `src/lib.rs` pass (`cargo test`) |
| 10 | REQ-HTTP-011: no `ferric` dep; `send_json()` driven from async context | ✅ `cargo tree -p ferric-http` clean; `crates/chirp-frontend/src/api.rs` drives `send_json()` from `spawn_local` closures |

## CI gate — locally verified (before push)

All checks were run locally on the server against the branch before PR creation:

| Check | Command | Result |
|-------|---------|--------|
| fmt | `cargo fmt --all --check --locked` | ✅ exit 0 |
| clippy (workspace) | `cargo clippy --workspace --all-targets --locked -- -D warnings` | ✅ exit 0 |
| clippy (postgres) | `cargo clippy -p chirp-server --features postgres --all-targets --locked -- -D warnings` | ✅ exit 0 |
| test | `cargo test --workspace --locked` | ✅ exit 0 |
| wasm (ferric-http) | `cargo build -p ferric-http --target wasm32-unknown-unknown --locked` | ✅ exit 0 |
| wasm (chirp-frontend) | `cargo build -p chirp-frontend --target wasm32-unknown-unknown --locked` | ✅ exit 0 |
| doc | `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --locked` | ✅ exit 0 |

## What was produced

Single additive commit `d6a9b6e` on branch `work/ferric-http-r1`:

| File | +lines |
|------|--------|
| `crates/ferric-http/CHANGELOG.md` (new) | 142 |

The `CHANGELOG.md` documents the frozen public API surface (`Client`, `ClientBuilder`,
`RequestBuilder`, `Response`, `Error`, `Method`, `Result`) and records the full
acceptance-criteria evidence for the usable_early scope. No functional code was
modified; every public surface from the #6 baseline is preserved.

## Issues closed by PR #210

- **#148** — HTTP methods, JSON bodies, error handling (usable_early)
- **#132** — ferric-http 1.0 epic (all usable_early requirements met; #149 is a
  separate, not-yet-scheduled work item and does NOT block #132 closure)

## Notes

- Branch `work/ferric-http-r1` based on `main` HEAD `f481a5e`.
- `main` was never force-pushed; no existing history was rewritten.
- Issue #149 (PATCH, timeout, lean footprint) is NOT in scope — deferred per the brief.
- **Overall verdict: PASS. PR #210 is open and ready for merge.**
