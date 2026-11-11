# _BRIEF.md — ci-actions (#11), a devops work-item DAG for Nousix-LLC/nswe-demo

You are a `swe-coder` DAG. This brief is your whole task spec. Evaluate your own scope and decompose or stay
atomic as you judge; select and load your own methodology bundles for the concerns named below (do not expect a
methodology list here). Deliver, open a PR, and author a root `SYNTHESIS.md` verdict. You do **not** merge your own
PR or push to `main` — the overseer lands it after review.

## Objective
Stand up the engagement's **GitHub Actions CI** for the `Nousix-LLC/nswe-demo` Rust/WebAssembly workspace: a
`.github/workflows/ci.yml` that validates every PR and push and, on `main`, builds and publishes the chirp-server
container image. This closes **issue #11** (`Closes #11`), EPIC #3, milestone M3.

## Acceptance criteria (testable)
1. `.github/workflows/ci.yml` exists and is valid GitHub Actions YAML (parses; no undefined refs).
2. On pull-request and on push, the workflow runs, as distinct required-check-friendly jobs/steps:
   - `cargo fmt --all --check`
   - `cargo clippy --workspace --all-targets -- -D warnings` (the workspace lints are `missing_docs=warn`,
     `unsafe_code=warn`, `clippy::all=warn`; CI promotes warnings to errors via `-D warnings`)
   - `cargo test --workspace`
   - a **wasm frontend build** of `crates/chirp-frontend` (a `wasm-bindgen` SPA with `index.html`, built for
     `wasm32-unknown-unknown`; choose and pin the appropriate toolchain — e.g. `wasm-bindgen-cli`, `wasm-pack`, or
     `trunk` — and document the choice).
   - a **rustdoc check under `RUSTDOCFLAGS=-D warnings`** (`cargo doc --workspace --no-deps`) so intra-doc-link and
     doc warnings fail CI (this is the CRQ-02/F2 fold — see "Folded minors" below).
3. Dependency and build caching for `~/.cargo` and `target/` is configured so re-runs are incrementally cached.
4. On `main` only, a job **builds and pushes the chirp-server container image to GHCR**
   (`ghcr.io/nousix-llc/...`), authenticated via the built-in `GITHUB_TOKEN` with `packages: write`. See the
   ordering note in Scope for how to handle the Dockerfile dependency honestly.
5. Jobs are named stably so they can be adopted as **required status checks** on `main` (name them; you need not
   configure branch protection — that is a repo-admin action, note it in `SYNTHESIS.md`).
6. The workspace at the PR head **passes every check the workflow defines** (if a check cannot pass without a
   source change, make that change within this item's scope — e.g. resolve the rustdoc debt — rather than
   weakening the check).

## Inputs (what you build on — all landed on `main @ fcfc7a2`)
- A Cargo **virtual workspace** (`resolver = "2"`, `edition = 2021`, `rust-version = 1.82`, `members =
  ["crates/*"]`) with crates: `ferric`, `ferric-router`, `ferric-http`, `chirp-types`, `chirp-server` (axum REST
  API + static SPA serving), `chirp-frontend` (ferric wasm SPA). Workspace lints are declared in the root
  `Cargo.toml` (`[workspace.lints]`). The whole app layer is built, tested, and landed.
- Existing `.github/workflows/renew-interaction-limit.yml` (unrelated housekeeping — do not disturb it).
- The chirp-server binary is the deployable; the frontend compiles to wasm and is served as static assets.

## Folded minors (deferred from the #8 chirp-server review — fold into this item)
- **CRQ-02 / F2 — rustdoc intra-doc-link debt.** The codebase currently carries rustdoc intra-doc-link / doc
  warnings that only surface under `RUSTDOCFLAGS=-D warnings`. Add the rustdoc check (acceptance #2) AND resolve
  the existing debt so the check passes — this is the enforcement mechanism that prevents regression.
- **CRQ-01 — README HTTP status doc row.** A README documents an HTTP **422** response where the chirp-server
  actually returns **400** (validation error). Locate the row (likely a crate-level README under
  `crates/chirp-server/` or the API section of the repo README) and correct `422` → `400` so the docs match the
  server's real behavior.

## What to evaluate / concerns to cover (named as distinct concerns; you choose the methodology)
- **CI workflow correctness & reproducibility** — the YAML is valid, jobs run in the right order, toolchain and
  action versions are pinned, and a clean checkout reproduces the result.
- **Build-graph & caching correctness** — the wasm target is installed, caches key on `Cargo.lock`/toolchain and
  do not mask staleness; the matrix (if any) is justified.
- **Security / least-privilege CI posture** — minimal `permissions:` per job (read by default; `packages: write`
  only on the image job), no long-lived secrets (use `GITHUB_TOKEN`), GHCR login scoped to `main`, no secret
  leakage in logs, actions pinned.
- **Required-check friendliness & developer ergonomics** — fast feedback, stable job names, sensible
  PR-vs-push/`main` triggering.
- **Documentation accuracy** — the two folded minors above; plus a short note in `SYNTHESIS.md` of any repo-admin
  follow-up (branch protection, GHCR package visibility).
- **Rust/CI idiom** — idiomatic, current GitHub Actions + cargo practice (one concern among the above, not the
  only one).

## Scope / non-goals / constraints
- Repo scope: `Nousix-LLC/nswe-demo` only. Branch: **`work/ci-actions`**. Open a PR into **`main`** that
  `Closes #11`. Never force-push; never push to `main`; never merge your own PR (P1 — the overseer lands).
- **Ordering dependency to handle honestly:** the GHCR **image build+push** step needs the multi-stage
  **Dockerfile** that work-item **#12 (containerize) has NOT yet landed**. Do not fabricate a build against a
  missing Dockerfile. Author the lint/test/wasm-build/rustdoc checks so they are complete and required-check-ready
  **now**, and include the image build+push job in a form that activates correctly once #12's Dockerfile lands
  (e.g. gated to `main` and referencing the Dockerfile path #12 will add, or guarded so it skips cleanly
  until the Dockerfile exists). **Document this ordering explicitly in `SYNTHESIS.md`** so the overseer can gate
  it — an honest "image job wired, awaiting #12 Dockerfile" is correct; a green that silently builds nothing is
  not.
- Do not change application behavior beyond the CRQ-01 doc correction and the CRQ-02 rustdoc-debt resolution.

## Declared output
- Commits on `work/ci-actions`; a PR into `main` that `Closes #11`.
- A root **`SYNTHESIS.md`** at this workspace root carrying the machine-gate verdict (PASS/FAIL), the checks run
  and their results, the decision record, how the two folded minors were handled, and the #12-Dockerfile ordering
  note. The overseer gates on this root `SYNTHESIS.md` body (not on a pushed branch or posted side-effect).
