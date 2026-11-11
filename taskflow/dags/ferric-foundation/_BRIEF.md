# _BRIEF.md — Work-item: ferric-foundation (issue #4)

You are a **swe-coder** code-writing **DAG** node. The NSWE project overseer (`swe-lead`) forked you to deliver ONE work-item of the `Nousix-LLC/nswe-demo` engagement. Boot the kernel first (your standing contract), run the atomic-vs-decompose evaluation on THIS brief, do the work (decomposing into a subtree if the kernel's triggers fire), run the Synthesis verification gate, and stop on your one terminal `report_status`.

## Objective
Establish the Cargo **workspace** at the repo root and implement the **core of `ferric`** — a small client-side web-application framework in Rust compiled to WebAssembly. This is the foundation the rest of the engagement builds on, so prioritize a clean, well-tested, documented, extensible core over breadth.

## Repository & delivery (READ CAREFULLY)
- Repo: `Nousix-LLC/nswe-demo` (GitHub; `gh` is authenticated on this host; `git`, `cargo`, `rustup` available).
- **Work in an isolated clone inside your own workspace**: `git clone` the repo (e.g. `gh repo clone Nousix-LLC/nswe-demo checkout` under your workspace `/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-foundation/`). Do NOT reuse `~/nousix-runtime/nswe-demo/repo` (another process may touch it).
- Base branch: `main`. Create and commit to branch **`work/ferric-foundation`**.
- When the work builds and tests pass: **push the branch and open a PR into `main`** with `gh pr create`, title `ferric-foundation: workspace + ferric core`, body summarizing the design + test results and ending with `Closes #4`.
- **Never** commit to or force-push `main`. Local commits + push the work branch + open the PR only. No commit-attribution trailers.

## Acceptance criteria
1. **Workspace**: root `Cargo.toml` as a virtual workspace; member crate `crates/ferric`. Workspace lints/profiles sensible.
2. **Reactive signals**: `Signal<T>` (or equivalent) with get/set, subscriber registration, and change notification; support derived/computed values and batched updates to avoid redundant re-render. Must be sound (no leaks of stale subscribers).
3. **Component model**: a component abstraction (trait and/or function-components) that produces a view tree; a `mount(root, component)` entry that renders into a DOM element.
4. **DOM rendering**: render the view tree to real DOM via `wasm-bindgen` + `web-sys`, with a minimal keyed diff/patch on signal change; event binding for at least click and input. Keep the vdom/patch small but correct.
5. **WASM build**: `crates/ferric` compiles for `wasm32-unknown-unknown` (`rustup target add wasm32-unknown-unknown` in your DAG). Use `wasm-bindgen`. Provide a tiny example (a counter) under `crates/ferric/examples/` or an `examples/counter` crate that builds to wasm.
6. **Tests**: native `cargo test` unit tests for the reactive core (signals/computed/batching) that run without a browser; plus at least one `wasm-bindgen-test` if the toolchain installs cleanly (if `wasm-bindgen-test-runner`/headless browser is unavailable in this environment, document that in SYNTHESIS.md and keep the native tests as the gate — do not fail the whole item on missing browser tooling).
7. **Quality**: `cargo fmt --check` clean; `cargo clippy --all-targets -- -D warnings` clean; rustdoc on all public items; `crates/ferric/README.md` with the counter example and a short architecture note.

## Suggested methodology (your brief names these; load on-demand)
- `rust` (primary — ownership/borrowing for the signal graph, trait design for components, error handling, cargo workspace, testing).
- `core` (coding standards, error handling, commit practices).
- `code-quality` (SOLID/Clean Code for the framework API; this is a long-lived public surface).
- `testing` (unit + the test strategy for a reactive core).
You are the final judge of what you load; add `architecture` if you decide the component/render boundary needs a design note.

## Inherited constraints (from the overseer's engagement plan — conform, do not re-litigate)
- Framework crate name is **`ferric`** at `crates/ferric`; the workspace will later gain `crates/ferric-router`, `crates/ferric-http`, `crates/chirp-types`, `crates/chirp-server`, `crates/chirp-frontend`. Lay the workspace out so those slot in cleanly.
- Rust edition 2021+; stable toolchain. Keep framework dependencies lean (wasm-bindgen, web-sys, js-sys; avoid heavy frameworks — we are BUILDING a framework).
- Public API should be ergonomic enough that a Twitter-style SPA (timeline, compose, profile, follow/like) can be built on it in later work-items. You do NOT build the app now — only the foundation it needs.

## Synthesis verification gate (your terminal child)
Author `SYNTHESIS.md` in your workspace with: a **build verdict** (workspace `cargo build`, `cargo build --target wasm32-unknown-unknown -p ferric`), a **test verdict** (`cargo test` results), **fmt/clippy** results, a **diff manifest** (files added/changed), the **PR URL**, and an overall **PASS/FAIL**. PASS requires: workspace + ferric wasm build succeed, native tests pass, fmt/clippy clean. Report honestly — a clean FAIL with evidence is more useful than a green-washed pass.

## Terminal
Follow the kernel: author your declared outputs + `COMPLETE.md` (atomic) or the fold record (if you decomposed), then one terminal `report_status`. Make the **PR URL** and the **PASS/FAIL verdict** prominent in your terminal record so the overseer can gate without re-running your build.
