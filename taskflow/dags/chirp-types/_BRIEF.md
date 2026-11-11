# _BRIEF.md — Work-item: chirp-types (issue #7)

You are a **swe-coder** code-writing **DAG** node. The NSWE project overseer (`swe-lead`) forked you to deliver ONE work-item of the `Nousix-LLC/nswe-demo` engagement. Boot the kernel first (your standing contract), run the atomic-vs-decompose evaluation on THIS brief, do the work (decomposing into a subtree if the kernel's triggers fire), run the Synthesis verification gate, and stop on your one terminal `report_status`.

## Objective
Implement **`crates/chirp-types`** — the **shared domain model + client<->server API contract** for the `chirp` Twitter-style app: the domain types (User, Chirp/Post, Timeline, Follow, Like) and the request/response DTOs that form the API contract, `serde`-serializable and usable by BOTH the server (`chirp-server`) and the frontend (`chirp-frontend`). This crate is the contract the rest of the app composes against, so prioritize a clean, coherent, well-documented, stable type surface.

## Repository & delivery (READ CAREFULLY)
- Repo: `Nousix-LLC/nswe-demo` (GitHub; `gh` is authenticated on this host; `git`, `cargo`, `rustup` available).
- **Work in an isolated clone inside your own workspace**: `gh repo clone Nousix-LLC/nswe-demo checkout` under your workspace `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-types/`. Do NOT reuse any other process's clone.
- Base branch: `main` (contains the landed virtual workspace + `crates/ferric`). Create and commit to branch **`work/chirp-types`**.
- When the work builds and tests pass: **push the branch and open a PR into `main`** with `gh pr create`, title `chirp-types: shared domain model + API contract`, body summarizing the design + test results and ending with `Closes #7`.
- **Never** commit to or force-push `main`. Local commits + push the work branch + open the PR only. No commit-attribution trailers.

## Acceptance criteria
1. **New workspace member crate** `crates/chirp-types` slotting cleanly into the existing virtual workspace; a plain library crate (compiles for the native host target; it must NOT require wasm or a browser — both server and frontend depend on it).
2. **Domain model**: coherent types for `User`, `Chirp`/`Post`, `Timeline`, `Follow`, `Like` (ids, timestamps, relationships) with sensible field types and documented invariants.
3. **API contract DTOs**: the request/response types that form the client<->server REST contract (e.g. create-chirp request/response, timeline query/response, follow/unfollow, like/unlike, auth/user DTOs as needed). Design them as the single source of truth both sides import.
4. **Serde**: every domain + DTO type is `serde::{Serialize, Deserialize}` with stable, explicit JSON field naming (document any `rename`/casing convention); round-trip stable.
5. **Tests**: native `cargo test` unit tests covering serde round-trips and any invariants/constructors; no browser/network dependence.
6. **Quality**: `cargo fmt --check` clean; `cargo clippy --all-targets -- -D warnings` clean; rustdoc on all public items; a short `crates/chirp-types/README.md` describing the contract and how server + frontend consume it.

## Suggested methodology (your brief names these; load on-demand)
- `rust` (primary — type/trait design, serde derive conventions, module layout, testing).
- `core` (coding standards, error handling, commit practices).
- `architecture` (this is a shared contract crate — the boundary both server and frontend compose against; design the type surface deliberately and write a short architecture/contract note).
You are the final judge of what you load.

## Inherited constraints (from the overseer's engagement plan — conform, do not re-litigate)
- Crate name **`chirp-types`** at `crates/chirp-types`. It is the shared contract for later work-items `chirp-server` (#8, axum REST API) and `chirp-frontend` (#9, ferric SPA); design the DTOs so both can import this crate directly. Keep it dependency-light (serde, serde_json, maybe a uuid/time crate if justified) — no server or wasm deps.
- Rust edition 2021+; stable toolchain. Match the conventions already on `main` (read the root `Cargo.toml` + `crates/ferric` for edition/lint/style).
- You build only the shared types/contract now, not the server or the frontend.

## Synthesis verification gate (your terminal child)
Author `SYNTHESIS.md` in your workspace with: a **build verdict** (`cargo build --workspace`), a **test verdict** (`cargo test`), **fmt/clippy** results, a **diff manifest**, the **PR URL**, and an overall **PASS/FAIL**. PASS requires: workspace build succeeds, native tests pass, fmt/clippy clean. Report honestly — a clean FAIL with evidence beats a green-washed pass.

## Terminal
Follow the kernel: author your declared outputs + `COMPLETE.md` (atomic) or the fold record (if you decomposed), then one terminal `report_status`. Make the **PR URL** and the **PASS/FAIL verdict** prominent in your terminal record so the overseer can gate without re-running your build.
