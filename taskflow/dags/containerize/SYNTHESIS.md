# SYNTHESIS — work-item #12 `containerize` (EPIC #3 devops)

**Verdict: PASS** — a multi-stage container image for the chirp app was authored, **built, and run
locally**, and verifiably serves the SPA + REST API + `/healthz` as a small, non-root,
health-checked image. Delivered as PR #22 into `main` (not merged; `main` untouched).

| Field | Value |
|---|---|
| Work-item | #12 `containerize` (EPIC #3, milestone M3) |
| Repo | `Nousix-LLC/nswe-demo` |
| Branch | `work/containerize` (2 commits off `main@fcfc7a2`) |
| PR | https://github.com/Nousix-LLC/nswe-demo/pull/22 — **OPEN**, base `main`, `Closes #12` |
| `main` after this work | `fcfc7a2…` — **unchanged** (PR not merged, no push to main) |
| Image | `chirp:local` — **41.7 MB**, `linux/amd64`, `USER 65532:65532` |
| Build host | Docker 29.5.2 + BuildKit/buildx 0.34.0 |

## Deliverables

| Path | Role |
|---|---|
| `Dockerfile` | Multi-stage build (builder → distroless runtime) |
| `.dockerignore` | Build-context trim (`target/`, VCS, CI, docs, scratch) |
| `deploy/docker/healthcheck.rs` | Std-only `/healthz` probe (distroless has no curl/wget) |
| `deploy/README.md` | Build / run / config / healthcheck reference |
| `README.md` | Added a "Running chirp in a container" section |
| `crates/chirp-server/src/main.rs` | SIGTERM handling for clean container shutdown (minimal) |

## Design (decision record)

- **Two stages.** Builder `rust:1.88-slim-bookworm` compiles the release `chirp-server`, builds the
  `chirp-frontend` `chirp` wasm example and runs `wasm-bindgen --target web`, and compiles the
  healthcheck probe. Runtime `gcr.io/distroless/cc-debian12:nonroot` carries only the server binary,
  the probe, and the SPA bundle — no shell, package manager, or toolchain.
- **glibc ABI match.** Builder is Debian 12 bookworm (glibc 2.36); the distroless `cc-debian12`
  runtime is the same, so the dynamically-linked server binary runs there unchanged. (Verified: both
  report glibc 2.36.)
- **Rust 1.88, not 1.82.** The workspace MSRV is 1.82, but `wasm-bindgen-cli` 0.2.129's transitive
  deps (`icu_*`, `time`) need rustc 1.88; a first build on `rust:1.82-slim` failed on exactly that.
  Bumped the *builder* to 1.88 (still ≥ workspace MSRV; bookworm keeps glibc 2.36).
- **wasm toolchain.** `cargo install wasm-bindgen-cli --version 0.2.129 --locked`, pinned to match
  the `wasm-bindgen` crate version in `Cargo.lock` (a CLI/crate mismatch breaks wasm init). Chosen
  over a prebuilt GitHub-release binary to keep the build fully from crates.io and arch-independent.
- **Reproducibility.** Both base images pinned by tag **+ `@sha256` digest**; all Cargo builds
  `--locked`. Digests: builder `sha256:38bc5a86…`, runtime `sha256:9dac0a79…`.
- **Security posture.** Non-root `65532` (explicit `USER`); distroless minimal attack surface; no
  secrets in any layer (no `ARG`/`COPY` of credentials); SPA bundle copied read-only to `/srv/chirp`;
  friendly to `--read-only --cap-drop=ALL --security-opt=no-new-privileges` (documented).
- **Operability.** `HEALTHCHECK` against `/healthz` via the standalone probe (which derives its port
  from the same `CHIRP_BIND_ADDR` the server reads — one knob); exec-form `ENTRYPOINT` so the server
  is PID 1; logs to stdout/stderr via `RUST_LOG`. Config via `CHIRP_BIND_ADDR` (`0.0.0.0:8080`),
  `CHIRP_STATIC_DIR` (`/srv/chirp`), `RUST_LOG`.
- **SIGTERM fix (minimal repo change).** The server's `shutdown_signal()` awaited only SIGINT, so a
  container was SIGKILL'd (exit 137) on `docker stop`/Kubernetes stop. Added a SIGTERM branch
  (unix-gated) so it drains and exits 0 — the minimal change required to run cleanly in a container;
  no API/transport change. `cargo fmt`/`clippy -D warnings`/`test` (20 passed) all clean afterward.
- **Image size.** 41.7 MB = distroless base ≈29 MB + server 2.5 MB + healthcheck 0.37 MB (stripped
  from 3.7 MB via `rustc -C strip=symbols`) + SPA bundle 0.31 MB. Within the compiled-language
  < 50 MB target.

## Build evidence (machine verdict)

Build: `docker build -t chirp:local .` → **exit 0**, image **41.7 MB**.

Run: `docker run --rm -p 8080:8080 chirp:local`, probed over the published port:

| Check | Result |
|---|---|
| `GET /healthz` | **200** `{"status":"ok","service":"chirp-server","version":"0.1.0"}` (`application/json`) |
| `GET /` (SPA) | **200** `text/html` (the chirp `index.html`) |
| `GET /user/42` (client route) | **200** `text/html` — SPA `index.html` fallback |
| `GET /pkg/chirp.js` | **200** `text/javascript` (26 345 B) |
| `GET /pkg/chirp_bg.wasm` | **200** **`application/wasm`** (282 026 B) |
| `POST /api/users` (valid DTO) | **201** — returns the created `User` |
| Docker `HEALTHCHECK` | **healthy**, failing-streak 0, probe exit 0 |
| `docker stop` (SIGTERM) | **exit 0** in ~0.3 s; log: "SIGTERM received; draining in-flight requests" → "chirp-server stopped" |
| Runtime user | `Config.User=65532:65532`; live PID 1 runs as uid `65532` (non-root) |
| External DB required | **No** — in-memory repository default |

Server-side quality (after the SIGTERM change): `cargo fmt --check` clean · `cargo clippy
--all-targets -- -D warnings` clean · `cargo test -p chirp-server` → **20 passed, 0 failed**.

## Acceptance criteria

- [x] Multi-stage `Dockerfile` at repo root (builds release server **and** the wasm SPA bundle)
- [x] Minimal runtime stage (distroless; no toolchain/source leakage)
- [x] Runs as a non-root user (explicit `USER 65532`, non-0 uid)
- [x] `HEALTHCHECK` exercising `/healthz`
- [x] Listen addr/port and static-asset path configurable + documented; starts & serves SPA + API
      out of the box with the in-memory default (no external DB)
- [x] `.dockerignore` excluding `target/`, VCS, local scratch
- [x] Builds reproducibly, reasonably small (41.7 MB); base images pinned by tag + digest; size +
      build/run commands documented
- [x] Brief docs (`deploy/README.md` + README section): build, run, env/config, healthcheck
- [x] Commits on `work/containerize`; PR into `main` that `Closes #12`; PR **not** merged; `main` not pushed

## Scope boundary (honored)

Out of scope and **untouched**: CI workflows / GHCR push (`#11 ci-actions` owns `.github/workflows`
— this Dockerfile is the artifact its image-build job consumes), k8s/ArgoCD manifests
(`#13 deploy-argocd`), and any live registry/cluster deploy. The image was built and run locally to
prove it; nothing was pushed to a registry.

## Blockers

None. The image builds reproducibly and runs; no host/sandbox limitation was hit. (Build was fully
local with network access to crates.io, Docker Hub, and gcr.io.)
