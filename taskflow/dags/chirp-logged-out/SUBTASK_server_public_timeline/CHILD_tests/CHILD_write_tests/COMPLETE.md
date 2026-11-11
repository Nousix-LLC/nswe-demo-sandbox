# COMPLETE — CHILD_write_tests

## Summary

Added the `public_timeline` stub to `UnhealthyStore` and four integration tests in `mod public_timeline` to `crates/chirp-server/tests/api.rs`. Committed on `work/chirp-logged-out`.

## Outputs

- `crates/chirp-server/tests/api.rs` — modified with:
  - `public_timeline` stub added to `impl ChirpRepository for UnhealthyStore` (compilation fix)
  - New `mod public_timeline` with four `#[tokio::test]` functions:
    1. `public_timeline_empty_store_returns_200_with_empty_page`
    2. `public_timeline_includes_all_users_newest_first`
    3. `public_timeline_paginates_with_cursor`
    4. `public_timeline_requires_no_auth`

## Commit

Branch: `work/chirp-logged-out`  
Commit: `d57335d` — `test(chirp-server): add integration tests for public_timeline endpoint`

## Success Criteria Verified

- [x] `crates/chirp-server/tests/api.rs` compiles (no trait-method missing errors — `public_timeline` stub added to `UnhealthyStore`)
- [x] Four new `#[tokio::test]` functions present in `mod public_timeline`
- [x] Committed on `work/chirp-logged-out`
- [x] No host paths, internal addresses, SSH key paths, or taskflow references in committed code
- [x] Existing harness helpers unchanged (`TestApp`, `build_app`, etc.)
- [x] Tests are infrastructure-free (use `TestApp::new()` / `build_app()`, no database, no network)
