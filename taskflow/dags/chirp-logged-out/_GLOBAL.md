# _GLOBAL.md — chirp-logged-out subtree

**Root task:** chirp-logged-out  
**Goal:** Implement the logged-out visitor experience for Chirp — public timeline, public user profiles, and an accurate landing with loading/empty/error/end-of-list states (issue #35).

## Shared context

- **Repository:** `Nousix-LLC/nswe-demo`
- **Branch:** `work/chirp-logged-out` — created from `main` by the backend spoke (first to commit); subsequent spokes pull and commit on top.
- **Target PR:** One PR into `main` with `Closes #35` in the description; authored by the synthesis spoke.
- **GitHub issue:** #35 — "Logged-out reading and a useful landing with accurate states"

## Codebase facts (confirmed by root-task exploration)

**Backend (`crates/chirp-server`):**
- `GET /api/timeline` requires `AuthUser` extractor → 401 for unauthenticated callers.
- `GET /api/users/{id}` is already unauthenticated (no auth extractor on `get_user` handler).
- `ChirpRepository::timeline(&self, viewer: UserId, query: TimelineQuery)` — requires a viewer.
- Implementations: `InMemoryRepository` (`repository/in_memory.rs`) and `PostgresRepository` (`repository/postgres.rs`).
- Router composition: `crates/chirp-server/src/api/router.rs`.
- Handler table: `crates/chirp-server/src/api/handlers.rs`.

**Frontend (`crates/chirp-frontend`):**
- `AppContext::client()` → `ApiClient` with no token for logged-out users, with token for logged-in.
- `ApiClient::timeline(&self, query)` calls `GET /timeline` (relative to base URL `/api`), i.e. `GET /api/timeline`.
- Timeline view (`src/timeline.rs`) calls `ctx.client().timeline(..)`.
- `AppContext::session: Signal<Option<Session>>` — `None` = logged out.
- Route table in `src/app.rs`: `/ → timeline_view`, `/user/:id → profile_view`.
- `TimelineModel` already implements loading/empty/error/end-of-list state machine.

## Sub-task map

| ID | Name | Depends on | Key deliverable |
|----|------|------------|-----------------|
| `SUBTASK_server_public_timeline` | Backend: public timeline endpoint | — | `GET /api/public/timeline` unauthenticated, trait method, both impls, tests |
| `SUBTASK_frontend_logged_out` | Frontend: logged-out visitor UI | `SUBTASK_server_public_timeline` | Public timeline view, sign-up/sign-in CTA, accurate states |
| `SUBTASK_synthesis` | Synthesis: CI gate + PR | `SUBTASK_frontend_logged_out` | PR #35 closing, `SYNTHESIS.md` |

## Acceptance criteria (from brief)

- **AC-1:** Logged-out visitor can load the home/public timeline and open a user profile without signing up.
- **AC-2:** On arrival with no content, the visitor sees a clear statement of what Chirp is plus a sign-up/sign-in route — never a blank page or unexplained error.
- **AC-3:** Timeline load failure shows a clear, recoverable message.
- **AC-4:** "Create an account" route is visible from the landing and from the sign-in screen.
- **AC-5:** Loading, empty, error, and end-of-list states are each visually distinct — never blank or stale.

## Delivery constraints

- CI must pass: `fmt`, `clippy`, `test`, `wasm`, `doc`, `image`.
- No force-push to `main`.
- Nothing committed or posted to GitHub may contain host paths, internal addresses, SSH key paths, or taskflow references.
