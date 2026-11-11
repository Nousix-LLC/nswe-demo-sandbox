# _BRIEF.md — REMEDIATE_implementation

**Parent task:** CHILD_ci_verify (failed — this task is remediation)
**Parent hub:** `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/_GLOBAL.md`

## Task Specification

**Slug:** REMEDIATE_implementation
**Task Kind:** standard
**Depends on:** none
**Status:** Pending

## Objective

Create the branch `work/chirp-logged-out` from `main` at commit `62febf5faf6023b3492365d246c7ac39c9f659a3` on the build server (`~/nswe-demo`), and implement the complete `public_timeline` feature in `crates/chirp-server/`. This covers all implementation code: the `ChirpRepository` trait method, the `InMemoryRepository` implementation, the `PostgresRepository` implementation (feature-gated), the axum handler, and the route mount. Verify `cargo build` passes. Commit all changes on the branch.

## Background

The original predecessor tasks (CHILD_skeleton, CHILD_in_memory, CHILD_postgres) claimed to have created this branch and committed implementation code, but their git operations did not persist — the branch does not exist in any repository. All prior COMPLETE.md records cite commits that cannot be found. This task re-implements from scratch.

## Inputs

- `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/_GLOBAL.md` — contains exact code patterns for every file, the precise SQL for PostgresRepository, the InMemoryRepository pattern, the handler signature, and the route mount. USE this as the authoritative implementation reference.
- Access to the build server (`ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 'bash -lc "..."'`) with `~/nswe-demo` as the codebase root.
- `CLAUDE.md` at the project root — SSH and git conventions for this sandbox.

## Scope

Implement these changes on `work/chirp-logged-out`:
- `crates/chirp-server/src/repository/mod.rs` — add `public_timeline` trait method
- `crates/chirp-server/src/repository/in_memory.rs` — full `InMemoryRepository::public_timeline` implementation
- `crates/chirp-server/src/repository/postgres.rs` — full `PostgresRepository::public_timeline` implementation (feature-gated)
- `crates/chirp-server/src/api/handlers.rs` — `pub async fn public_timeline` handler
- `crates/chirp-server/src/api/router.rs` — `GET /public/timeline` route mount

## Declared outputs

- Branch `work/chirp-logged-out` on `Nousix-LLC/nswe-demo`, created from `62febf5faf6023b3492365d246c7ac39c9f659a3`
- All five files modified and committed on the branch
- `cargo build -p chirp-server` exits 0
- `cargo build -p chirp-server --features postgres` exits 0
- `COMPLETE.md` in this workspace

## Success criteria

- Branch `work/chirp-logged-out` exists on GitHub and locally
- `git log work/chirp-logged-out` shows a commit with all five file changes
- `cargo build -p chirp-server` → exit 0, no warnings
- `cargo build -p chirp-server --features postgres` → exit 0, no warnings
- Nothing committed contains host paths, internal addresses, SSH key paths, or taskflow references

## Constraints

- Build server: `mattm@100.90.75.93`, codebase at `~/nswe-demo`
- Use `bash -lc` to load server PATH for `cargo` and `git`
- Base commit: `62febf5faf6023b3492365d246c7ac39c9f659a3` (tip of `main` at the time the DAG was created)
- No `todo!()` stubs — implement fully (the implementations are known from _GLOBAL.md patterns and original COMPLETE.md records)
- Commit message convention: conventional commits (`feat(chirp-server): add public_timeline endpoint`)

## Suggested Methodology Files

Domain mapping: **Writing new code** → primary `core`, supporting `operations`

- `operations/DevTools_Build_Systems_Methodology.md` — cargo build conventions, CI toolchain
- `core/BestPractices_Coding_Standards_Methodology.md` — code quality baseline

These are parent-flagged suggestions; the agent is the final judge of what to load.

## Inherited Constraints

- Run CI commands without `--features postgres` (in-memory harness tests only)
- Follow the axum/async_trait patterns already in the codebase; do not introduce new dependencies
- Keep existing routes and auth completely unchanged
