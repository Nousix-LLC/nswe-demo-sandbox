# _GLOBAL.md — chirp-logged-out-r2 subtree hub

## Objective

Implement the logged-out visitor experience for Chirp (GitHub issue #35): a public
unauthenticated timeline endpoint on the server, and a frontend landing that shows that
timeline with accurate loading/empty/error/end-of-list states, sign-up/sign-in navigation,
profile links from chirp items, and a useful empty state that communicates what Chirp is.

## Cut Rationale

**Chosen cut: serial pipeline — server → frontend → synthesis.**

Three candidate cuts were evaluated:

- **Cut A (server → frontend → synthesis)**: disjoint file ownership (`crates/chirp-server/**`
  vs `crates/chirp-frontend/**`), 2 dependency edges, all M-band tasks. The only forced
  serialization is git: both spokes commit to the same branch `work/chirp-logged-out`, which
  prevents true parallel execution even though files are disjoint. **Selected.**

- **Cut B (server + frontend parallel → synthesis)**: same disjoint file ownership, but the
  git branch serialization (one branch, sequential commits) means no actual parallelism is
  achieved — just added coordination overhead with no benefit.

- **Cut C (skeleton → server spoke → frontend spoke → synthesis)**: the skeleton would own
  `router.rs` and `handlers.rs` stubs that the server spoke must also modify, eliminating the
  ownership disjointness benefit without reducing total task count.

The API contract between server and frontend is already frozen in `chirp-types`: the new
endpoint uses `TimelineQuery` (input) and `Page<Chirp>` (output), both pre-existing types.
See `contracts/` for the endpoint contract and ownership manifest.

## Task DAG

| Group | Task | Depends on | Declared output |
|-------|------|------------|-----------------|
| 0 | SUBTASK_server | — | Commits on `work/chirp-logged-out` with server changes |
| 1 | SUBTASK_frontend | SUBTASK_server | Commits on `work/chirp-logged-out` with frontend changes |
| 2 | SUBTASK_synthesis | SUBTASK_server + SUBTASK_frontend | SYNTHESIS.md + PR closing #35 |

## Subtree Methodology Posture

**Dominant task type:** Writing new Rust code — new API endpoint (Axum server) and new
WASM frontend logic (Ferric reactive framework).

**Primary bundles children will draw on:**
- `rust` — Axum web services (server), WebAssembly browser (frontend), Rust testing
- `core` — coding standards, error handling, commit practices

**Cross-cutting bindings that apply to every leaf:**
- Security constraint: Never put host addresses, SSH key paths, usernames, or host paths into
  any committed file, GitHub issue, PR, comment, or description. All such references are
  runtime SSH mechanics only.
- Branch: `work/chirp-logged-out` from main at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
- One PR into main with `Closes #35` as plain text in the description body
- CI must pass: `fmt`, `clippy`, `test`, `wasm`, `doc`, `image`
- Attribution: commit messages end with `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`

Child agents retain final judgment on which methodology files to load — the above are starting
points, not an exclusive list.

## Subtree-Wide Constraints

1. **API contract**: The public timeline endpoint is `GET /api/public/timeline` (no auth).
   Input: `TimelineQuery { limit?: u32, cursor?: Cursor }` as query params. Output:
   `Page<Chirp>`. Types defined in `chirp-types`. Do not introduce new shared types.

2. **No authentication removal**: Do not remove authentication from any currently-authenticated
   endpoint. Only add new unauthenticated routes.

3. **Repository trait pattern**: All persistence logic goes through the `ChirpRepository`
   trait. Add `pub_timeline` as a new method on the trait and implement it in both
   `InMemoryRepository` and `PostgresRepository`.

4. **Ferric reactive model**: Frontend uses thread-local state with `bump()` for reactive
   updates, `spawn_local` for WASM async, and `Signal<Option<Session>>` for session state.
   The timeline view already has this pattern — extend it, do not replace it.

5. **Git delivery**: Changes reach the cluster via repo + ArgoCD. All environment concerns
   (server address, SSH details) are SSH runtime mechanics and MUST NOT appear in commits.
