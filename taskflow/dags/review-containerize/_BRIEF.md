# _BRIEF.md — review-containerize (review DAG for PR #22 / work-item #12, persona swe-coder)

You are a code-review DAG for the `Nousix-LLC/nswe-demo` engagement. Your job is to **review, not fix**: read
the change, evaluate it against the concerns below and the work-item's acceptance criteria, and render an
authoritative **APPROVE / REQUEST-CHANGES** verdict with findings. You do not edit, stage, commit, push, rebase,
relock, or merge anything; you touch neither the work branch nor `main`. You select and load your own methodology
(the code-review methodology is your spine; add what the diff warrants).

## What you are reviewing

- **PR #22** — `work/containerize` → `main`, **Closes #12**, head `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751`,
  base `main` (now at `7a81849` after #10 landed; PR is OPEN/MERGEABLE/CLEAN). Review the diff of
  `work/containerize` against its merge base, read-only (`git`/`gh`).
- **The work-item:** #12 `containerize` (EPIC #3 devops, milestone M3) — produce a multi-stage container image
  for the chirp app that builds the release server **and** the wasm SPA bundle, runs non-root from a minimal
  runtime, health-checks `/healthz`, is configurable + documented, and is reproducible and reasonably small.
- **The code DAG's machine verdict (input, do not re-run):** `containerize` folded **PASS** — see
  `/home/user/nousix-runtime/nswe-demo/taskflow/dags/containerize/SYNTHESIS.md`. It records: image `chirp:local`
  41.7 MB, `linux/amd64`, `USER 65532:65532` distroless; base images pinned by tag **+ `@sha256` digest**; all
  cargo builds `--locked`; the image was built and run locally with `/healthz`→200, SPA + client-route fallback +
  `/pkg/*.wasm` (`application/wasm`) + `POST /api/users`→201 all served; Docker `HEALTHCHECK` healthy; `docker stop`
  (SIGTERM) exits 0. Rely on that machine gate; do not rebuild to reconfirm it — your job is judgment over the
  diff, not re-execution.

### Deliverables in the diff (what the PR changes)

`Dockerfile` (multi-stage builder `rust:1.88-slim-bookworm` → runtime `gcr.io/distroless/cc-debian12:nonroot`),
`.dockerignore`, `deploy/docker/healthcheck.rs` (std-only `/healthz` probe), `deploy/README.md`, a "Running chirp
in a container" section in `README.md`, and a **minimal `crates/chirp-server/src/main.rs` change** adding SIGTERM
handling (unix-gated) so the container drains and exits 0 on `docker stop`/Kubernetes stop.

## Concerns to evaluate (named as distinct concerns; cover each explicitly)

1. **Dockerfile build correctness & reproducibility** — multi-stage correctness; the builder actually produces
   both the release server and the `wasm-bindgen --target web` SPA bundle; `--locked` throughout; base images
   pinned by tag **and digest**; the `wasm-bindgen-cli` version matches the `wasm-bindgen` crate in `Cargo.lock`;
   the builder-Rust-1.88-vs-workspace-MSRV-1.82 bump is sound and justified; `.dockerignore` trims the context
   correctly without excluding anything the build needs.
2. **Runtime image hygiene & size** — distroless runtime carries only what it must (server binary, probe, SPA
   bundle); no toolchain/source/secret leakage into runtime layers; the glibc ABI match (bookworm builder ↔
   `cc-debian12` runtime) is correct; size (41.7 MB) is reasonable and the reported breakdown holds.
3. **Container security posture** — non-root (`USER 65532`, non-zero uid, PID-1 as the server via exec-form
   `ENTRYPOINT`); no secrets baked into any layer or `ARG`/`COPY`; least-privilege friendliness
   (`--read-only`/`--cap-drop=ALL`/`no-new-privileges`); SPA bundle read-only. This diff pulls base images and
   installs a CLI from crates.io — assess the **supply-chain / dependency trust boundary** (digest pinning,
   `--locked`, provenance).
4. **Operability** — `HEALTHCHECK` genuinely exercises `/healthz`; the standalone probe derives its port from the
   same `CHIRP_BIND_ADDR` the server reads (one knob); configurable bind addr / static-asset path / log level,
   and documented; logs to stdout/stderr; starts and serves out of the box with the in-memory default (no
   external DB).
5. **Correctness of the repo-code change (SIGTERM handling in `main.rs`)** — the signal handling is correct and
   unix-gated, introduces no API/transport/behavior change beyond clean shutdown, and does not regress the
   server; does it belong in this item's scope (it is the minimal change required to run cleanly in a container).
6. **Code quality & idiom** — Dockerfile / shell / Rust idiom; clarity and maintainability of the probe and the
   docs; whether the docs match real behavior.
7. **Testing / verification depth** — whether the machine gate's build+run evidence actually demonstrates the
   acceptance criteria, and whether anything material is unverified.
8. **Scope conformance** — containerization only: it must not author CI workflows/GHCR push (#11's `.github/`),
   k8s/ArgoCD manifests (#13), or perform any live registry/cluster deploy. Confirm the diff stays in `#12` scope
   (the Dockerfile is the artifact #11's image-build job consumes — a declared, honest hand-off, not a scope
   breach).

Decide the concern set and the methodology bundles yourself from what the diff actually touches; do not carry a
previous review's selection forward. The language/Dockerfile idiom is one concern among these, never the only one.

## Declared output

- A **posted review on PR #22** via `gh` (if the platform blocks a formal self-approval because the authoring
  account owns the PR, post the verdict + key findings as a review comment — the authoritative verdict is your
  root `SYNTHESIS.md` body, not the gh review state).
- A root **`SYNTHESIS.md`** at this DAG's workspace root carrying: the **APPROVE / REQUEST-CHANGES** verdict, an
  explicit per-acceptance-criterion pass/fail, and a severity-tagged findings list (block / major / minor / nit)
  with location + evidence + remediation for each block/major. REQUEST-CHANGES iff ≥1 open blocking finding;
  APPROVE requires zero open blockers and an explicit call on every open major. A `major`/`block` must name a
  concrete, landable defect — not a hardening wish; record non-blocking hardening as minor/nit.

## Constraints

- Repo scope: `Nousix-LLC/nswe-demo` only. **Read-only**: no edit/stage/commit/push/rebase/relock/merge; no
  force-push; `main` and the work branch stay untouched. Reviews read and report; they do not fix.
- Rely on the code DAG's machine gate for build/test facts; do not re-run the build to reconfirm a green gate.
- Render exactly one authoritative verdict in the root `SYNTHESIS.md`.
