# _BRIEF.md — containerize (work-item #12, devops EPIC #3) — persona swe-coder

You are a forked `swe-coder` DAG. Deliver work-item **#12 containerize** for the `Nousix-LLC/nswe-demo`
engagement. Evaluate your own scope and decompose as you see fit; select and load your own methodology bundles
through the methodology loader from the concerns named below. This brief is your whole task spec — it describes
*what* to deliver and *what to evaluate*, not *how*.

## Objective
Package the landed chirp application into a small, reproducible, production-grade **container image**: a
multi-stage build that compiles the Rust workspace, builds the `crates/chirp-frontend` WebAssembly SPA bundle,
and assembles the `chirp-server` binary **plus** the built frontend static assets into one minimal runtime image
that serves the app. This Dockerfile is also the artifact `#11 ci-actions`' GHCR image-build job is waiting on.

Closes issue **#12** (`Nousix-LLC/nswe-demo`, EPIC #3 devops, milestone M3).

## Acceptance criteria (testable)
- A **multi-stage `Dockerfile`** at the repo root (or a conventional path you justify):
  - a build stage that builds the workspace release `chirp-server` binary and produces the `chirp-frontend`
    wasm/JS/HTML asset bundle (the SPA `chirp-server` serves as static files + index.html fallback);
  - a final **minimal runtime stage** (e.g. a slim/distroless base) containing only the server binary, the
    built frontend assets, and runtime needs — no build toolchain, no source.
- The container **runs as a non-root user** (explicit `USER`, non-0 uid).
- A **`HEALTHCHECK`** that exercises the server's `/healthz` endpoint.
- The server's listen address/port and the static-asset path are configurable and documented; the image starts
  and serves the SPA + REST API out of the box with its in-memory repository default (no external DB required).
- A **`.dockerignore`** that keeps the build context small and excludes `target/`, VCS, and local scratch.
- The image builds **reproducibly** and is reasonably small; document the resulting image size and the
  build/run commands. Pin base images by tag/digest as appropriate.
- Brief **docs** (a short section in a README or `deploy/`-adjacent doc) covering build, run, env/config, and the
  healthcheck.

## Inputs (what you build on — all landed on `main @ fcfc7a2e02d931ab1b499c8fac1747c77ec3a64e`)
- `crates/chirp-server` — axum REST API + repository-trait persistence (in-memory default, no DB) + static/SPA
  serving + `/healthz` + tracing (#8, landed).
- `crates/chirp-frontend` — ferric WASM SPA, `wasm32-unknown-unknown` target, built to a static bundle (#9,
  landed). You choose the wasm build toolchain (e.g. wasm-bindgen/trunk) and justify it.
- The ferric framework crates (`ferric`, `ferric-router`, `ferric-http`) and `chirp-types` contract (landed).
- The workspace `Cargo.toml`/`Cargo.lock` at the repo root.

## Scope / non-goals
- **In scope:** the Dockerfile, `.dockerignore`, image build/run plumbing, and its docs. Make only the minimal
  repo changes needed to containerize (e.g. a config env knob if the server lacks one, a build-asset path);
  do not refactor the app.
- **Out of scope:** CI wiring (`#11 ci-actions` owns `.github/workflows` and the GHCR push job — do not author
  workflows); k8s `deploy/` manifests + the ArgoCD `Application` (`#13 deploy-argocd`); any live cluster/registry
  deploy. Build the image locally to prove it; do not push to a registry.

## What to evaluate / concerns to cover (named as distinct concerns — load your own methodology for each)
- **Build correctness & reproducibility** — the multi-stage build deterministically produces a working binary +
  frontend bundle; layer ordering/caching is sound; base images pinned.
- **Runtime image hygiene & size** — minimal final image, no build toolchain or source leakage, slim/distroless
  base choice justified.
- **Container security posture** — non-root runtime, least privilege, no secrets baked into layers, minimal
  attack surface, read-only-friendly filesystem where practical.
- **Operability** — `HEALTHCHECK` against `/healthz`, configurable port/bind/asset-path, clean startup/shutdown,
  sane logging to stdout/stderr for container log capture.
- **The Rust/WASM language idiom** for release builds and wasm asset packaging (one concern among the above, not
  the only one).
Decide the concerns and methodology fresh for this item from what the work touches; do not carry any prior DAG's
selection forward.

## Declared output
- Commits on branch **`work/containerize`**.
- A **PR into `main`** that **Closes #12** (do not merge it yourself; do not push to `main`).
- A root **`SYNTHESIS.md`** carrying the machine verdict (build evidence: the image builds, runs, serves the SPA
  + `/healthz`; image size; the build/run commands) — PASS/FAIL + decision record.

## Constraints
- Repo scope: `Nousix-LLC/nswe-demo` only. Branch `work/containerize`; never force-push or push to `main`; never
  rewrite merged history. Add no commit attribution trailers.
- The app's in-memory repository default means the image needs **no external database** to run.
- If a genuine host/sandbox limitation blocks building the image, deliver an **honest partial**: record the exact
  blocker + remediation path in `SYNTHESIS.md` and the PR, deliver what is verifiably reproducible, mark blocked
  criteria — never fabricate a green build.
