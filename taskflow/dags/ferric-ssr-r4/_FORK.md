owner_id: proc-dce5bfbd-3aae-43e6-ad03-f1b8507bae48
observation_seam: taskflow/dags/ferric-ssr-r4/SYNTHESIS.md
launch_agent: swe-coder
thread_type: dag
disposition: retain
reap: whole-after-land
launch_context:
  application: software

# _FORK.md — ferric-ssr-r4

**Owner**: overseer I279
**Program**: swe-coder
**Goal**: Code remediation — ferric SSR + hydration review blockers B1 and B2

## Objective

Remediate the two blocking findings from review-ferric-ssr-r1 on PR #228 (branch `work/ferric-ssr-r1`):

**B1 — REQ-HYD-003: `hydrate()` never called from the WASM entry point**

`crates/chirp-frontend/src/app.rs::start()` calls `ferric::dom::mount(root, app)` — the client-mount path — not `ferric::hydrate(root, app)`. The SSR+hydration feature is not functional end-to-end: when the browser loads an SSR page, the WASM bundle creates a fresh reactive tree and replaces the server-rendered DOM under `#app` with a client render. The hydration path is never entered.

A secondary docstring at `crates/chirp-server/src/ssr.rs:141` asserts "the WASM bundle initialises and calls `ferric::hydrate` after the document is parsed" — this is incorrect and must be corrected.

**What satisfies B1**: a change to `crates/chirp-frontend/src/app.rs::start()` (or a new `start_ssr()` variant) that calls `ferric::hydrate(root, app_closure)` when the page contains server-rendered markup in `#app` (e.g., detect by checking if `#app` already has child nodes), plus correction of the `ssr.rs:141` docstring.

---

**B2 — REQ-SSR-006 / Area E: `hydrate.rs` has no `wasm-bindgen-test` coverage**

`crates/ferric/src/hydrate.rs` (466 lines) has no `#[cfg(test)]` block. Issues #224 and #226 (both `release-gating: true`) explicitly require headless `wasm-bindgen-test` coverage. The PR identity table asserts `native-tests-pass` but makes no `wasm-tests-pass` assertion.

Three tests must exist before merge:

1. **REQ-SSR-004 / #224 — adopt walk without structural mutations**: build a minimal SSR HTML string, inject it into a headless browser DOM under `#app`, call `ferric::hydrate(root, || ...)`, confirm zero `appendChild`/`replaceChild` calls via pre/post node-identity check or `MutationObserver`.

2. **REQ-SSR-005 / #224 — event wiring post-hydration**: after hydration, dispatch a `click` event on a wired element, assert the DOM reflects the signal-driven update and the element's node identity is preserved (not recreated).

3. **REQ-SSR-006 / #226 — mismatch detection**: build a server HTML string with a deliberate structural divergence (e.g., the component returns `<p>` but the server DOM has `<div>`); call `hydrate`; assert `console.warn` fired; assert the live DOM matches the client-rendered component.

These tests require `wasm-pack test --headless` or `cargo test --target wasm32-unknown-unknown` with `wasm-bindgen-test-runner`.

**What satisfies B2**: add a `#[cfg(test)]` module in `hydrate.rs` (or a `crates/ferric/tests/hydrate_wasm.rs` file) with the three `#[wasm_bindgen_test]` tests above, all passing under `wasm-pack test --headless`. Add `wasm-tests-pass: ✅` to the PR identity table.

---

## Inputs

- Branch: `work/ferric-ssr-r1`
- PR: #228 (Nousix-LLC/nswe-demo)
- Review synthesis (accepted DAG): `taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md`
- Review comment on PR: https://github.com/Nousix-LLC/nswe-demo/pull/228#issuecomment-6647644348

## Scope

Change only what is needed to satisfy B1 and B2. Do not change the 14 non-blocker issues (#229–#242) in this PR — those are separate backlog items. Keep all existing CI passing.

## Acceptance criteria

- B1 resolved: `ferric::hydrate(root, app)` is called from the WASM entry point when the page contains server-rendered markup; `ssr.rs:141` docstring is corrected.
- B2 resolved: three `wasm-bindgen-test` tests covering adopt walk, event wiring, and mismatch detection, all passing under `wasm-pack test --headless`.
- All 6 CI checks pass (fmt, clippy, doc, build, native-tests, `wasm-pack test`).
- PR #228 updated with the fix commits.

## Declared output

`SYNTHESIS.md` with verdict `PASS` or `FAIL`, carrying:
- commit SHA(s) pushed to `work/ferric-ssr-r1`
- CI run URL
- summary of what was changed
- any residual concerns

## Governing app file

Load `appfiles/WORK_SESSION.md` (code DAG context) for how to structure the work.
