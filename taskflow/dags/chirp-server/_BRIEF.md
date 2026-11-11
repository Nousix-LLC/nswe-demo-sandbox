# _BRIEF.md — Work-item: chirp-server (issue #8)

You are a **swe-coder** code-writing **DAG** node. The NSWE project overseer (`swe-lead`) forked you to deliver ONE work-item of the `Nousix-LLC/nswe-demo` engagement. Boot the kernel first (your standing contract), run the atomic-vs-decompose evaluation on THIS brief, do the work (decomposing into a subtree if the kernel's triggers fire), run the Synthesis verification gate, and stop on your one terminal `report_status`.

## Objective
Implement **`crates/chirp-server`** — the **axum REST API backend** for the `chirp` Twitter-style app: REST endpoints, persistence behind a repository trait, static-asset / SPA serving, health endpoint, structured logging, and integration tests over the API. It composes against the **already-landed shared contract crate `crates/chirp-types`** (issue #7, on `main` as of squash commit `2e32aed`) — import its domain types + DTOs directly; do NOT re-define the wire contract.

## Repository & delivery (READ CAREFULLY)
- Repo: `Nousix-LLC/nswe-demo` (GitHub; `gh` is authenticated on this host; `git`, `cargo`, `rustup` available).
- **Work in an isolated clone inside your own workspace**: `gh repo clone Nousix-LLC/nswe-demo checkout` under your workspace `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/`. Do NOT reuse any other process's clone.
- Base branch: `main` (contains the landed virtual workspace + `crates/ferric` + `crates/ferric-router` + `crates/chirp-types`). Create and commit to branch **`work/chirp-server`**.
- When the work builds and tests pass: **push the branch and open a PR into `main`** with `gh pr create`, title `chirp-server: axum REST API + persistence + static serving`, body summarizing the design + test results and ending with `Closes #8`.
- **Never** commit to or force-push `main`. Local commits + push the work branch + open the PR only. No commit-attribution trailers.
- NOTE: other work-items have open PRs (#15 ferric-http). Your branch adds a NEW crate `crates/chirp-server` + a `members` entry; a sibling landing may restale your `Cargo.lock` later — that is the overseer's relock concern (P1), not yours; just build cleanly against current `main` at fork time.

## Acceptance criteria (from issue #8)
1. **New workspace member crate** `crates/chirp-server` (axum) slotting into the virtual workspace; native binary crate (server), builds on the stable host target.
2. **REST endpoints** for the core app surface: timeline (list), post a chirp, user profiles, follow/unfollow, like/unlike — using the `chirp-types` request/response DTOs as the wire contract.
3. **Persistence** behind a **repository trait**: SQLite via `sqlx`, OR a well-abstracted in-memory store for the demo (the trait is the point — swappable backing). Document the choice.
4. **Serves the built WASM SPA + static assets** (a static-file service + SPA fallback route) and a **health endpoint** (e.g. `GET /healthz`).
5. **Structured logging** (e.g. `tracing`).
6. **Integration tests over the API** (spin the router, exercise endpoints end-to-end against the in-memory/SQLite repo; assert status + DTO round-trips). Production-quality error handling (typed errors → HTTP status + `ApiError`/`ErrorCode` from `chirp-types`).
7. **Quality**: `cargo build --workspace` clean; `cargo test` (server unit + integration) passes; `cargo fmt --check` clean; `cargo clippy --all-targets -- -D warnings` clean; rustdoc on public items; a short `crates/chirp-server/README.md` describing endpoints + how to run.

## Suggested methodology (your brief names these; load on-demand)
- `rust` (primary — axum handler/state design, error-as-value, trait objects / generics for the repository, async).
- `core` (coding standards, error handling, commit practices).
- `architecture` (layering: transport → service → repository; the repository trait boundary; how static serving + SPA fallback compose).
- `testing` (API integration tests; test the repository trait against its in-memory impl; round-trip DTOs).
You are the final judge of what you load.

## Inherited constraints (from the overseer's engagement plan — conform, do not re-litigate)
- Crate name **`chirp-server`** at `crates/chirp-server`. Depends on `chirp-types` (path dep within the workspace) for ALL wire types — single source of truth; do not fork or re-declare the contract.
- Keep the demo runnable without external infra: prefer an in-memory repository (behind the trait) as the default so the server boots with no DB, with SQLite/`sqlx` an optional documented backing if you implement it. Do not require a running database for `cargo test`.
- Static-serving: serve a `static/`/`dist/` directory + SPA fallback; the actual `chirp-frontend` WASM (#9) is not built yet — wire the serving path and document it (an empty/placeholder dir is acceptable; #9 lands the SPA later).
- Rust edition 2021+; stable toolchain. Match the conventions already on `main` (read the root `Cargo.toml` + existing crates for edition/lint/style).
- You build only the server now, not the frontend (#9) or deploy/CI (#10–#13).

## Synthesis verification gate (your terminal child)
Author `SYNTHESIS.md` in your workspace with: a **build verdict** (`cargo build --workspace`), a **test verdict** (`cargo test`, including the API integration tests), **fmt/clippy** results, a **diff manifest**, the **PR URL**, and an overall **PASS/FAIL**. PASS requires: workspace build succeeds, native + integration tests pass, fmt/clippy clean. Report honestly — a clean FAIL with evidence beats a green-washed pass.

## Terminal
Follow the kernel: author your declared outputs + `COMPLETE.md` (atomic) or the fold record (if you decomposed), then one terminal `report_status`. Make the **PR URL** and the **PASS/FAIL verdict** prominent in your terminal record so the overseer can gate without re-running your build.
