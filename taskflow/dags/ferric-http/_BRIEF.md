# _BRIEF.md — Work-item: ferric-http (issue #6)

You are a **swe-coder** code-writing **DAG** node. The NSWE project overseer (`swe-lead`) forked you to deliver ONE work-item of the `Nousix-LLC/nswe-demo` engagement. Boot the kernel first (your standing contract), run the atomic-vs-decompose evaluation on THIS brief, do the work (decomposing into a subtree if the kernel's triggers fire), run the Synthesis verification gate, and stop on your one terminal `report_status`.

## Objective
Implement **`ferric-http`** — a small async HTTP/JSON client for the `ferric` WASM framework over the browser **Fetch API**: typed JSON `get`/`post`/`put`/`delete` with `serde`, error handling, and request/response helpers. Framework crate on a long-lived public surface — prioritize a clean, well-tested, documented, ergonomic API.

## Repository & delivery (READ CAREFULLY)
- Repo: `Nousix-LLC/nswe-demo` (GitHub; `gh` is authenticated on this host; `git`, `cargo`, `rustup` available).
- **Work in an isolated clone inside your own workspace**: `gh repo clone Nousix-LLC/nswe-demo checkout` under your workspace `/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-http/`. Do NOT reuse any other process's clone.
- Base branch: `main` (already contains the landed `ferric` foundation — crate `crates/ferric`). Create and commit to branch **`work/ferric-http`**.
- When the work builds and tests pass: **push the branch and open a PR into `main`** with `gh pr create`, title `ferric-http: fetch-based HTTP/JSON client`, body summarizing the design + test results and ending with `Closes #6`.
- **Never** commit to or force-push `main`. Local commits + push the work branch + open the PR only. No commit-attribution trailers.

## Acceptance criteria
1. **New workspace member crate** `crates/ferric-http` slotting cleanly into the existing virtual workspace.
2. **Fetch-based client**: async typed JSON methods `get`/`post`/`put`/`delete` over the Fetch API (`web-sys`/`js-sys`, `wasm-bindgen-futures`); request bodies and response bodies (de)serialized with `serde`/`serde_json`.
3. **Error handling**: a clear error type distinguishing network errors, non-2xx HTTP status, and (de)serialization errors; ergonomic `Result`-returning API. No `unwrap`/`panic` on fallible paths.
4. **Request/response helpers**: builder or helper surface for headers, query params, and base URL; reasonable defaults (e.g. JSON content-type).
5. **WASM build**: `crates/ferric-http` compiles for `wasm32-unknown-unknown`.
6. **Tests**: native `cargo test` unit tests for the pure logic that can be tested without a live network/browser (URL/query building, header assembly, error mapping, serde round-trips); plus a `wasm-bindgen-test` if the toolchain installs cleanly (if a headless browser/network runner is unavailable, document it in SYNTHESIS.md and keep the native tests as the gate — do not fail the item on missing browser tooling).
7. **Quality**: `cargo fmt --check` clean; `cargo clippy --all-targets -- -D warnings` clean; rustdoc on all public items; a short `crates/ferric-http/README.md` with a usage example and an architecture note.

## Suggested methodology (your brief names these; load on-demand)
- `rust` (primary — async over wasm-bindgen-futures, error-type design, serde integration, ownership for the client).
- `core` (coding standards, error handling, commit practices).
- `code-quality` (SOLID/Clean Code for the public HTTP API).
- `testing` (unit strategy for a network client with minimal browser dependence).
You are the final judge of what you load.

## Inherited constraints (from the overseer's engagement plan — conform, do not re-litigate)
- Crate name **`ferric-http`** at `crates/ferric-http`. It MAY depend on `crates/ferric` where helpful but the HTTP client should be usable on its own; keep coupling minimal. Read `crates/ferric` first to match conventions (error style, module layout, edition).
- Rust edition 2021+; stable toolchain; lean deps (web-sys, js-sys, wasm-bindgen, wasm-bindgen-futures, serde, serde_json). Ergonomic enough that a Twitter-style SPA can call a REST backend (`chirp-server`) through it later.
- You build only the HTTP client now, not the app.

## Synthesis verification gate (your terminal child)
Author `SYNTHESIS.md` in your workspace with: a **build verdict** (workspace `cargo build`, `cargo build --target wasm32-unknown-unknown -p ferric-http`), a **test verdict** (`cargo test`), **fmt/clippy** results, a **diff manifest**, the **PR URL**, and an overall **PASS/FAIL**. PASS requires: workspace + ferric-http wasm build succeed, native tests pass, fmt/clippy clean. Report honestly — a clean FAIL with evidence beats a green-washed pass.

## Terminal
Follow the kernel: author your declared outputs + `COMPLETE.md` (atomic) or the fold record (if you decomposed), then one terminal `report_status`. Make the **PR URL** and the **PASS/FAIL verdict** prominent in your terminal record so the overseer can gate without re-running your build.
