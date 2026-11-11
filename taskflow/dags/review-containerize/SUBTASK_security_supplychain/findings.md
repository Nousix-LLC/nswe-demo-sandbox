# findings — SUBTASK_security_supplychain

## 1. Header

- **Spoke**: `SUBTASK_security_supplychain`
- **Concerns owned**: Concern 3 (container security posture **and** supply-chain / dependency trust boundary); the **secret/credential-leakage slice of Concern 2** (security face only — layer-composition + size face is owned by `SUBTASK_dockerfile_build`).
- **Diff reviewed**: PR #22 head commit `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751` of `Nousix-LLC/nswe-demo` (read-only).

## 2. Per-concern disposition

### Concern 3 — Container security posture: `PASS-WITH-NOTES`

The runtime posture is strong and the diff's security claims verify against the actual `Dockerfile` and the machine gate (`taskflow/dags/containerize/SYNTHESIS.md`):

- **Non-root, non-zero uid**: `USER 65532:65532` is explicit (`Dockerfile:103`), on top of the distroless `:nonroot` base default. The machine gate independently confirms `Config.User=65532:65532` and that **live PID 1 runs as uid 65532**.
- **PID 1 is the server (exec form)**: `ENTRYPOINT ["/usr/local/bin/chirp-server"]` (`Dockerfile:113`) and `HEALTHCHECK … CMD ["/usr/local/bin/healthcheck"]` (`Dockerfile:111`) are both exec-form, so the server is PID 1 and receives SIGTERM directly (gate: `docker stop` → exit 0 in ~0.3 s). No shell-form signal-swallowing wrapper.
- **Minimal attack surface**: runtime base is `gcr.io/distroless/cc-debian12:nonroot` — no shell, package manager, or toolchain. The `apt-get install ca-certificates` exists only in the discarded builder stage and is cleaned in-layer (`rm -rf /var/lib/apt/lists/*`).
- **Least-privilege friendliness**: `deploy/README.md §Hardened run` documents `--read-only --tmpfs /tmp --cap-drop=ALL --security-opt=no-new-privileges --pids-limit 128`; the in-memory server writes nothing to disk, so a read-only rootfs is viable. These are operator run-flags the image image cannot itself enforce (enforcement at the orchestrator is #13's territory, out of scope here) — documenting them is the right posture for an image deliverable.

The one note is `SEC-1` (minor): the served SPA bundle is `COPY --chown=65532:65532`'d, i.e. writable by the very process that serves it. See the findings table.

### Concern 3 — Supply-chain / dependency trust boundary: `PASS`

Every trust-boundary claim in the diff is substantiated by the actual file content:

- **Base images digest-pinned**: builder `FROM rust:1.88-slim-bookworm@sha256:38bc5a86d998772d4aec2348656ed21438d20fcdce2795b56ca434cf21430d89` (`Dockerfile:27`) and runtime `FROM gcr.io/distroless/cc-debian12:nonroot@sha256:9dac0a79194e45a7da0158a9c6da57b217585af0786db3845d1f0ec1a0dd182f` (`Dockerfile:68`). Both carry tag **and** `@sha256` digest; both digests match the machine gate's record. Digest pinning defeats tag-mutation / image-substitution in the base-image trust boundary.
- **`--locked` builds throughout**: `cargo install wasm-bindgen-cli --version "${WASM_BINDGEN_VERSION}" --locked` (`Dockerfile:52`) and `cargo build --release --locked -p chirp-server` / `… -p chirp-frontend …` (`Dockerfile:62-63`). `--locked` forces the committed `Cargo.lock` / the tool's own lock — no silent re-resolution to a different (possibly malicious) transitive tree. Aligns with the Dependency-Security lock-file + `npm ci`-equivalent discipline.
- **`wasm-bindgen-cli` provenance**: installed from **crates.io**, **version-pinned** to `0.2.129` (`ARG WASM_BINDGEN_VERSION=0.2.129`, `Dockerfile:40`) to match the `wasm-bindgen` crate in `Cargo.lock`, and built `--locked`. The comment (`Dockerfile:59-60`) and the gate's design record note this was **deliberately chosen over a prebuilt GitHub-release binary** — the right call: a prebuilt binary would be an opaque, non-digest-pinned artifact outside the crates.io integrity-checked path, whereas `cargo install --locked` builds from source whose `.crate` checksums Cargo verifies against the registry index under the digest-pinned `rust:1.88` toolchain. The trust boundary is crates.io + Cargo integrity verification, reproducibly pinned end to end.

No concrete supply-chain defect. One advisory nit (`SEC-2`) on the `.dockerignore` denylist shape.

### Concern 2 (secret/credential-leakage face only) — `PASS`

No secret or credential leaks into any builder or runtime layer:

- **No credential material in instructions**: the only `ARG`/`ENV` are non-secret (`WASM_BINDGEN_VERSION`, `CHIRP_BIND_ADDR`, `CHIRP_STATIC_DIR`, `RUST_LOG`). No `--mount=type=secret` is needed (the build pulls only public crates.io/base images), and none is mis-used.
- **No credential files copied**: the builder's `COPY . .` (`Dockerfile:56`) is scoped by `.dockerignore`, which excludes `.env`, `.env.*`, `.git/`, `.vscode/`, `.idea/` — so environment files and VCS history never enter even the discarded builder context. The runtime stage copies only the three explicit artifacts (`/out/bin/chirp-server`, `/out/bin/healthcheck`, `/out/static`) — no source, no toolchain, no dotfiles.
- **No secrets in the repo to leak**: the app runs on the in-memory repository default (no DB credentials); the gate confirms "External DB required: No".

Cross-reference (not re-filed per identity I2): the **layer-composition / cache / size** implications of `COPY . .` and the discarded-builder hygiene belong to `SUBTASK_dockerfile_build`; I adjudicate only leakage here and find none.

## 3. Findings table

| Finding ID | Concern | Severity | Location | Evidence | Remediation |
|---|---|---|---|---|---|
| SEC-1 | 3 | minor | `Dockerfile:85` (`COPY --from=builder --chown=65532:65532 /out/static /srv/chirp`) | The served SPA bundle is owned by the runtime user `65532`, so the process that serves `/srv/chirp` can also **write** it. By least-privilege, assets a process only ever reads should not be writable by that process; the `--chown` grants an unneeded write capability (marginal post-compromise asset-poisoning surface — a compromised server could rewrite the `index.html`/`chirp.js`/`.wasm` it serves to browsers). Non-blocking: the server never writes there, and `deploy/README.md` documents the `--read-only` hardened run that closes it at runtime. | Drop `--chown=65532:65532` on this `COPY` so the static bundle is `root:root`, mode `0644`/`0755` — world-readable, writable by no one at runtime. The non-root user can still read and serve it; no functional change. (The binaries at `Dockerfile:80-81` already follow this root-owned pattern.) |
| SEC-2 | 3 | nit | `.dockerignore` | The context exclusion is a denylist (`target/`, `.git/`, `.env`, `.env.*`, editor/OS noise). It correctly covers the known secret-bearing paths, but a denylist only protects against the patterns it enumerates; a stray `*.pem`/`*.key`/`*.p12`/`credentials*` left in the tree would enter the builder context. | Optional hardening: add defensive key-material globs (`*.pem`, `*.key`, `*.p12`, `*.pfx`, `id_rsa*`, `credentials*`) to `.dockerignore`. Advisory only — no such file exists in the repo today, so there is no concrete leak. |

## Metadata

- **Concern-3 posture claims checked against the diff**: non-root `USER 65532` ✓, exec-form `ENTRYPOINT`/`HEALTHCHECK` ✓, no baked secrets ✓, read-only-friendly (documented) ✓.
- **Supply-chain claims checked against the diff**: base-image `@sha256` digest pinning (both) ✓, `--locked` (install + both builds) ✓, `wasm-bindgen-cli` crates.io + version-pin + `--locked`, chosen over prebuilt binary ✓.
- **Severity discipline (I4)**: no `block`/`major` filed — the single concrete least-privilege item (SEC-1) is a non-blocking improvement, not a significant defect, and the `.dockerignore` denylist item (SEC-2) is a hardening wish; both correctly ranked minor/nit rather than block/major.
- **Read-only (I5) honored**: diff accessed via `gh pr diff` only; nothing edited/staged/committed/pushed; no post to GitHub.
- **Machine gate relied upon** for build/run facts (live uid 65532, SIGTERM exit 0, digests); not re-run.
