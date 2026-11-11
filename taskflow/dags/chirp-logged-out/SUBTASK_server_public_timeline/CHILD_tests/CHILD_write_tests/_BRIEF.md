# _BRIEF.md — CHILD_write_tests

**Parent task:** CHILD_tests (decomposed)  
**Parent hub:** `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/_GLOBAL.md`

## Task Specification

**Slug:** CHILD_write_tests  
**Task Kind:** standard  
**Depends on:** none  
**Status:** Pending

## Objective

Add the `public_timeline` stub to `UnhealthyStore` and write four integration test cases for `GET /api/public/timeline` in `crates/chirp-server/tests/api.rs`. Commit the result on branch `work/chirp-logged-out`.

## Context

All implementation is live on `work/chirp-logged-out`: `public_timeline` is in the `ChirpRepository` trait (`src/repository/mod.rs`), implemented in `InMemoryRepository` (`in_memory.rs`) and `PostgresRepository` (`postgres.rs`). The existing test harness (`TestApp`, `build_app`, `username`, `new_user`, `post_chirp`, `register`, `login`, `register_and_login`) is in scope in every test submodule via `use super::*`.

**Compilation blocker:** `UnhealthyStore` in `mod readiness` implements `ChirpRepository` but does not yet have `public_timeline`. This prevents compilation. Fix this FIRST.

## Inputs

- `crates/chirp-server/tests/api.rs` — existing harness + tests to extend
- `crates/chirp-server/src/repository/mod.rs` — trait method signature (line ~301)
- Parent hub: `_GLOBAL.md` (see Implementation context and Tests to write sections)

## Changes to make

### 1. UnhealthyStore: add `public_timeline` stub

In `mod readiness`, inside the `impl ChirpRepository for UnhealthyStore` block, add this method (position: anywhere in the `unimplemented` list, e.g. after `timeline`):

```rust
async fn public_timeline(
    &self,
    _query: TimelineQuery,
) -> Result<Page<Chirp>, ServerError> {
    unimplemented!()
}
```

`TimelineQuery`, `Page`, and `Chirp` are all in scope via `use super::*` (the outer harness already imports them).

### 2. New test module: `mod public_timeline`

Add a new module at the end of `tests/api.rs` (after `mod readiness`):

```rust
// ---------------------------------------------------------------------------------------------
// Public timeline — unauthenticated global feed endpoint.
// ---------------------------------------------------------------------------------------------
mod public_timeline {
    use super::*;

    #[tokio::test]
    async fn public_timeline_empty_store_returns_200_with_empty_page() {
        let app = TestApp::new();
        let resp = app.get("/api/public/timeline", None).await;
        assert_eq!(resp.status, StatusCode::OK);
        let page: Page<Chirp> = resp.json();
        assert!(page.items.is_empty(), "empty store yields no items");
        assert!(page.next_cursor.is_none(), "empty store yields no cursor");
    }

    #[tokio::test]
    async fn public_timeline_includes_all_users_newest_first() {
        let app = TestApp::new();
        let (_, alice_token) = app.register_and_login("alice").await;
        let (_, bob_token) = app.register_and_login("bob").await;

        let a1 = app.post_chirp(&alice_token, "alice one").await;
        let b1 = app.post_chirp(&bob_token, "bob one").await;
        let a2 = app.post_chirp(&alice_token, "alice two").await;

        let resp = app.get("/api/public/timeline", None).await;
        assert_eq!(resp.status, StatusCode::OK);
        let page: Page<Chirp> = resp.json();
        let ids: Vec<ChirpId> = page.items.iter().map(|c| c.id).collect();
        // Newest-first: a2, b1, a1.
        assert_eq!(ids, vec![a2.id, b1.id, a1.id]);
    }

    #[tokio::test]
    async fn public_timeline_paginates_with_cursor() {
        let app = TestApp::new();
        let (_, token) = app.register_and_login("alice").await;

        // Three chirps posted in ascending id order.
        let mut posted = Vec::new();
        for i in 0..3 {
            posted.push(app.post_chirp(&token, &format!("chirp {i}")).await);
        }

        // Page 1: limit=2, newest two items, non-None cursor.
        let resp = app.get("/api/public/timeline?limit=2", None).await;
        assert_eq!(resp.status, StatusCode::OK);
        let page1: Page<Chirp> = resp.json();
        assert_eq!(page1.items.len(), 2);
        let cursor = page1
            .next_cursor
            .clone()
            .expect("first page has a continuation cursor");
        assert_eq!(page1.items[0].id, posted[2].id, "newest first");
        assert_eq!(page1.items[1].id, posted[1].id);

        // Page 2: remaining one item, no cursor.
        let resp = app
            .get(
                &format!("/api/public/timeline?limit=2&cursor={}", cursor.0),
                None,
            )
            .await;
        assert_eq!(resp.status, StatusCode::OK);
        let page2: Page<Chirp> = resp.json();
        assert_eq!(page2.items.len(), 1);
        assert_eq!(page2.items[0].id, posted[0].id);
        assert!(page2.next_cursor.is_none(), "last page has no cursor");
    }

    #[tokio::test]
    async fn public_timeline_requires_no_auth() {
        let app = TestApp::new();

        // Public endpoint: no Authorization header → 200.
        let resp = app.get("/api/public/timeline", None).await;
        assert_eq!(
            resp.status,
            StatusCode::OK,
            "GET /api/public/timeline must not require authentication"
        );

        // Home timeline still requires auth (regression guard).
        let resp = app.get("/api/timeline", None).await;
        assert_eq!(
            resp.status,
            StatusCode::UNAUTHORIZED,
            "GET /api/timeline must still require authentication"
        );
    }
}
```

## Declared outputs

- `crates/chirp-server/tests/api.rs` — `public_timeline` stub added to `UnhealthyStore`, four test cases added in `mod public_timeline`
- Changes committed on `work/chirp-logged-out` with a message in the style of prior commits (e.g., `"test(chirp-server): add integration tests for public_timeline endpoint"`)

## Success criteria

- `crates/chirp-server/tests/api.rs` compiles (no trait-method missing errors)
- Four new `#[tokio::test]` functions present in `mod public_timeline`
- Committed on `work/chirp-logged-out`
- Nothing committed contains host paths, internal addresses, SSH key paths, or taskflow references

## Constraints

- Use the existing harness exactly as-is — do NOT modify `TestApp`, `build_app`, or any other harness helpers
- Tests are infrastructure-free: they use `TestApp::new()` / `build_app()`, no database, no network
- Branch: `work/chirp-logged-out`

## Suggested Methodology Files

Domain mapping row: **Writing tests** → primary `testing`, supporting `core`

Specific files:
- `testing/Testing_Integration_Testing_Methodology.md` — in-process integration test patterns; relevant because tests drive the assembled server end-to-end via tower oneshot, same pattern as the existing suite
- `testing/Testing_Unit_Testing_Methodology.md` — assertion discipline, test isolation, naming conventions
- `core/BestPractices_Coding_Standards_Methodology.md` — code style standards that also apply to test files

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Rust test framework: `tokio::test` (async), `assert_eq!`, standard Rust test patterns
- In-process testing via `tower::ServiceExt::oneshot` — no test database, no network
- Commit message style follows prior commits on the branch: short imperative subject line
- Nothing in committed code may contain host paths, internal addresses, SSH key paths, or taskflow references

## Out-of-Scope Methodologies

- `testing/Testing_E2E_Testing_Methodology.md` — not applicable; these are in-process tests with no external infrastructure
- `testing/Testing_Performance_Testing_Methodology.md` — not applicable; no performance assertions required
