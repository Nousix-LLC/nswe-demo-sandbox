# _GLOBAL.md — CHILD_tests subtree

**Task:** CHILD_tests (decomposed)  
**Parent hub:** `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/_GLOBAL.md`

## Goal

Complete the integration-test and CI-verification layer for the `GET /api/public/timeline` feature:
1. Write four integration test cases in `crates/chirp-server/tests/api.rs` and add the `public_timeline` stub to `UnhealthyStore`.
2. Run `cargo fmt --check`, `cargo clippy`, and `cargo test`; fix any formatting or lint issues introduced by prior commits; commit clean; author the declared `COMPLETE.md` records.

## Shared context

- **Repository:** `Nousix-LLC/nswe-demo`
- **Branch:** `work/chirp-logged-out`
- **Codebase root:** `/home/user/nswe-demo/crates/chirp-server/`
- **Target test file:** `crates/chirp-server/tests/api.rs`
- **Route under test:** `GET /api/public/timeline` (mounts as `GET /api/public/timeline` from client perspective)

## Implementation context

CHILD_skeleton (1d8edab), CHILD_in_memory (7160514), and CHILD_postgres (ec70b78) are all committed on `work/chirp-logged-out`. The `public_timeline` method is live in `InMemoryRepository` and `PostgresRepository`. The existing test file has an `UnhealthyStore` test double that implements `ChirpRepository` but does NOT yet have `public_timeline` — adding it (as `unimplemented!()`) is required for the file to compile.

## Tests to write

Add a new `mod public_timeline` block to `tests/api.rs` with four `#[tokio::test]` functions:

1. **`public_timeline_empty_store_returns_200_with_empty_page`** — `GET /api/public/timeline` with no Authorization header returns 200 and a `Page<Chirp>` with empty `items` and `None` next_cursor.

2. **`public_timeline_includes_all_users_newest_first`** — Register two users (alice, bob), have each post chirps, call `GET /api/public/timeline` without auth. All chirps from both appear in the response, ordered newest-first (largest chirp id first).

3. **`public_timeline_paginates_with_cursor`** — Register one user, post 3 chirps, call `GET /api/public/timeline?limit=2` (no auth). Page 1 returns 2 items and a non-None `next_cursor`. Page 2 (using `?limit=2&cursor=<value>`) returns the remaining 1 item and `None` next_cursor.

4. **`public_timeline_requires_no_auth`** — `GET /api/public/timeline` with no Authorization → 200. `GET /api/timeline` with no Authorization → 401 (regression guard).

## UnhealthyStore addition

In the `readiness` module's `UnhealthyStore` impl block, add:
```rust
async fn public_timeline(&self, _query: TimelineQuery) -> Result<Page<Chirp>, ServerError> {
    unimplemented!()
}
```
`TimelineQuery` and `Page` are already in scope via `use chirp_types::api::{..., TimelineQuery, Page}` and `use chirp_types::domain::Chirp` in the outer harness, imported through `use super::*`.

## Security constraint

Nothing committed to the repository may contain host paths, internal addresses, SSH key paths, or taskflow references.

## Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `CHILD_write_tests` | none | Write 4 test cases + UnhealthyStore stub; commit | `crates/chirp-server/tests/api.rs` |
| `CHILD_ci_verify` | `CHILD_write_tests` | Run CI, fix any issues, commit, write COMPLETE.md records | `SUBTASK_server_public_timeline/COMPLETE.md`, `CHILD_tests/SYNTHESIS.md` |

## Subtree Methodology Posture

- **Dominant task type:** Writing tests + CI verification (Testing + Operations bundles)
- **Primary bundles:** `testing` (integration testing patterns), `operations` (CI/CD, build systems)
- **Cross-cutting:** Rust-specific test patterns; existing in-memory harness pattern must be followed exactly

## Contract

**Contract location:** `contracts/`  
**Contract kind:** yaml_schema
