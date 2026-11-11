# _BRIEF.md — Work-item: ferric-router (issue #5)

You are a **swe-coder** code-writing **DAG** node. The NSWE project overseer (`swe-lead`) forked you to deliver ONE work-item of the `Nousix-LLC/nswe-demo` engagement. Boot the kernel first (your standing contract), run the atomic-vs-decompose evaluation on THIS brief, do the work (decomposing into a subtree if the kernel's triggers fire), run the Synthesis verification gate, and stop on your one terminal `report_status`.

## Objective
Implement **`ferric-router`** — a client-side router for the `ferric` WASM framework: a route table, path params, `<Link>`-style navigation, History API integration (pushState/popstate), programmatic navigation, and a router-outlet component. This is a framework crate on the long-lived public surface, so prioritize a clean, well-tested, documented, extensible API.

## Repository & delivery (READ CAREFULLY)
- Repo: `Nousix-LLC/nswe-demo` (GitHub; `gh` is authenticated on this host; `git`, `cargo`, `rustup` available).
- **Work in an isolated clone inside your own workspace**: `gh repo clone Nousix-LLC/nswe-demo checkout` under your workspace `/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-router/`. Do NOT reuse any other process's clone.
- Base branch: `main` (already contains the landed `ferric` foundation — crate `crates/ferric`). Create and commit to branch **`work/ferric-router`**.
- When the work builds and tests pass: **push the branch and open a PR into `main`** with `gh pr create`, title `ferric-router: client-side router (History API)`, body summarizing the design + test results and ending with `Closes #5`.
- **Never** commit to or force-push `main`. Local commits + push the work branch + open the PR only. No commit-attribution trailers.

## Acceptance criteria
1. **New workspace member crate** `crates/ferric-router` slotting cleanly into the existing virtual workspace; depends on `crates/ferric` (path dependency).
2. **Route table**: declarative route registration mapping path patterns (with params, e.g. `/user/:id`) to components/handlers; a matcher that resolves a path to a route + extracted params.
3. **History API navigation**: integrate `pushState`/`popstate` via `web-sys` so navigation updates the URL and back/forward work; a `<Link>`-style component/helper for declarative navigation; a programmatic `navigate(path)` API.
4. **Router outlet**: an outlet component that renders the component for the currently-matched route and re-renders reactively on navigation (compose with `ferric`'s signals/component model — do NOT re-implement reactivity).
5. **WASM build**: `crates/ferric-router` compiles for `wasm32-unknown-unknown`. Provide a tiny example (a 2–3 route app) that builds to wasm.
6. **Tests**: native `cargo test` unit tests for the route matcher + param extraction (pure logic, no browser); plus at least one `wasm-bindgen-test` if the toolchain installs cleanly (if a headless browser runner is unavailable, document it in SYNTHESIS.md and keep the native tests as the gate — do not fail the item on missing browser tooling).
7. **Quality**: `cargo fmt --check` clean; `cargo clippy --all-targets -- -D warnings` clean; rustdoc on all public items; a short `crates/ferric-router/README.md` with the example and an architecture note.

## Suggested methodology (your brief names these; load on-demand)
- `rust` (primary — API/trait design for routes and the outlet, ownership for the matcher, error handling).
- `core` (coding standards, error handling, commit practices).
- `code-quality` (SOLID/Clean Code for the public router API).
- `testing` (unit strategy for the matcher + navigation).
You are the final judge of what you load.

## Inherited constraints (from the overseer's engagement plan — conform, do not re-litigate)
- Crate name **`ferric-router`** at `crates/ferric-router`; it builds on the landed `ferric` core (signals, component model, `mount`, DOM runtime). Read `crates/ferric` and its README/prelude first and compose with it; do NOT fork or re-implement the reactivity/DOM layer.
- Rust edition 2021+; stable toolchain; lean deps (wasm-bindgen, web-sys, js-sys). Keep the API ergonomic enough that a Twitter-style SPA (timeline/compose/profile routes) can be built on it later.
- You build only the router now, not the app.

## Synthesis verification gate (your terminal child)
Author `SYNTHESIS.md` in your workspace with: a **build verdict** (workspace `cargo build`, `cargo build --target wasm32-unknown-unknown -p ferric-router`), a **test verdict** (`cargo test`), **fmt/clippy** results, a **diff manifest**, the **PR URL**, and an overall **PASS/FAIL**. PASS requires: workspace + ferric-router wasm build succeed, native tests pass, fmt/clippy clean. Report honestly — a clean FAIL with evidence beats a green-washed pass.

## Terminal
Follow the kernel: author your declared outputs + `COMPLETE.md` (atomic) or the fold record (if you decomposed), then one terminal `report_status`. Make the **PR URL** and the **PASS/FAIL verdict** prominent in your terminal record so the overseer can gate without re-running your build.
