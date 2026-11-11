# _BRIEF.md — chirp-frontend (#9) — code-writing DAG (persona swe-coder, opus-4-8)

You are a **code-writing DAG** (`swe-coder`, `domain: software`, `claude-opus-4-8`) forked by the NSWE project overseer (`overseer/I17`) for the `Nousix-LLC/nswe-demo` engagement. Do **all** the engineering for work-item **#9 chirp-frontend** by the software methodology's `decompose → implement → synthesize`, behind a terminal **Synthesis verification gate**, and **fold** (write root `SYNTHESIS.md` + `COMPLETE.md`). Boot the DAG Act-branch; load the software methodology bundles on-demand (`rust`, `core`, `architecture`, `testing`, plus `decomposition`+`synthesis` for the gate) from the software `_loader.md`.

## The goal (acceptance criteria)
Build **`crates/chirp-frontend`** — the **chirp Twitter-style client SPA**, a client-side **WASM** application built on the landed `ferric` framework, composing the landed `chirp-types` REST contract. It is the browser front end that talks to the (parallel, separately-landing) `chirp-server` #8 REST API over HTTP/JSON.

Concretely, the crate MUST:
- Be a **new workspace member crate** `crates/chirp-frontend` (the root `Cargo.toml` already globs `members = ["crates/*"]`). Build target **`wasm32-unknown-unknown`** (`cargo build -p chirp-frontend --target wasm32-unknown-unknown` ✅).
- **Compose the landed framework** (path-deps, do NOT re-implement any of it):
  - `ferric` (`crates/ferric`) — reactive signals, component model, `mount`, DOM rendering (wasm-bindgen/web-sys).
  - `ferric-router` (`crates/ferric-router`) — route table + matcher, History API navigation, `<Link>`/`navigate`, reactive outlet.
  - `ferric-http` (`crates/ferric-http`) — fetch-based HTTP/JSON client for the REST calls.
  - `chirp-types` (`crates/chirp-types`) — the shared domain model + request/response DTOs (the client↔server contract); use its types directly as the wire contract. Do NOT redefine DTOs.
- Implement a **coherent SPA**: at minimum a timeline view (list of chirps via `Page<T>` pagination), a compose-chirp form (create-chirp request), a user/profile route (`/user/:id` via the router), and follow/like actions — each wired through `ferric-http` to the chirp-types REST endpoints, with reactive re-render via ferric signals on data change. Use realistic REST paths/methods consistent with the chirp-types API DTOs (auth/user, create-chirp, timeline query, follow, like, `ApiError`/`ErrorCode` handling).
- Handle **loading / error states** from the HTTP client (surface `ApiError`/`ErrorCode` to the UI, no `unwrap`/`expect`/`panic` in library/runtime code; no `unsafe`).
- Provide a **wasm build example / entry** (an `index`/`main` mount + a static `index.html` harness if useful) demonstrating the app mounts and renders. Native unit tests where logic is testable off-DOM; `wasm-bindgen-test` compile-only is acceptable (no headless browser runner — document it, not a FAIL), mirroring the ferric/ferric-router precedent.
- Be **dependency-light** and consistent with the workspace: reuse `[workspace.dependencies]` (serde, wasm-bindgen, web-sys, js-sys, etc.) rather than re-pinning.
- `cargo fmt --all --check` clean; `cargo clippy --workspace --all-targets -- -D warnings` clean; rustdoc on public items; a `README.md`.

## Deliverable / git (local commits + PR)
- Work on a fresh **`work/chirp-frontend`** branch off current `main` (@ `25e90c0`). Commit locally; **open a PR into `main` with `Closes #9`** (the engagement follows the explicit user PR-into-main flow recorded in project STATE, which supersedes the app's local-first default). Do NOT touch `main` directly; do NOT force-push.
- **No attribution trailer** on commits.
- If `cargo build --workspace` requires a `Cargo.lock` update, let **Cargo** author it (`cargo build`); never hand-edit the lockfile.

## Synthesis verification gate (fold)
Your terminal child MUST build the combined workspace, run the suites, and write root **`SYNTHESIS.md`** with:
- a **PASS/FAIL verdict** (workspace build incl. wasm target, chirp-frontend tests, fmt, clippy),
- a **diff manifest** (per-file), and
- **contract/wiring checks** — confirm the SPA composes `chirp-types` DTOs as the wire contract and calls ferric-http correctly; note any REST-path assumptions that chirp-server #8 must honor (so the overseer/reviewer can check cross-crate coherence).
Then fold (`COMPLETE.md` + terminal `report_status`). The overseer reads this verdict at its machine gate; it does not re-run your build.

## Boundary / notes
- This crate is the **front end**; `chirp-server` #8 (axum REST API) is a **parallel** work-item still in flight — you do NOT build-depend on it (you consume the `chirp-types` contract and call it at runtime over HTTP). Where a concrete server base-URL/config is needed, make it configurable (e.g. a build-time/env or a `/api` relative base) and document the assumption rather than hard-coupling to #8's internals.
- Decompose as the work warrants (e.g. scaffold → http/api client layer → views/router wiring → synthesis gate), contract-first across your own spokes. You own your subtree's contract and synthesis; the overseer does not.
