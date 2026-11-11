# findings — SUBTASK_dockerfile_build

## Header

- **Spoke**: `SUBTASK_dockerfile_build`
- **Concerns owned**: concern **1** (Dockerfile build correctness & reproducibility); concern **2** — **layer-composition + size face only** (the secret/credential-leakage face is owned by `SUBTASK_security_supplychain`); concern **6** — **Dockerfile/shell idiom slice only**.
- **Diff reviewed**: PR #22 head commit `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751` of `Nousix-LLC/nswe-demo`.
- **Artifacts examined**: `Dockerfile`, `.dockerignore` (both fetched read-only at head); corroborated against `Cargo.lock` (wasm-bindgen pin) and the code-DAG machine gate `taskflow/dags/containerize/SYNTHESIS.md`. No build was run (read-only; green gate relied upon).

---

## Per-concern dispositions

### Concern 1 — Dockerfile build correctness & reproducibility: **PASS**

Verified against the actual file content, not merely the gate summary:

- **Both artifacts are built by the one builder stage.** `cargo build --release --locked -p chirp-server` and `cargo build --release --locked -p chirp-frontend --example chirp --target wasm32-unknown-unknown`, followed by `wasm-bindgen --target web --no-typescript --out-name chirp` emitting `chirp.js` + `chirp_bg.wasm` into `/out/static/pkg`, matching the `./pkg/chirp.js` import in `index.html`. The server binary and the SPA bundle are both produced (Dockerfile §Stage 1, the `set -eux` RUN).
- **`--locked` throughout.** All three cargo invocations carry `--locked` (`cargo install wasm-bindgen-cli --version "${WASM_BINDGEN_VERSION}" --locked`, and both `cargo build … --locked`). `Cargo.lock` is retained in the build context (`.dockerignore` does not exclude it), so `--locked` is enforceable.
- **Base images pinned by tag AND `@sha256` digest.** Builder `rust:1.88-slim-bookworm@sha256:38bc5a86d998772d4aec2348656ed21438d20fcdce2795b56ca434cf21430d89`; runtime `gcr.io/distroless/cc-debian12:nonroot@sha256:9dac0a79194e45a7da0158a9c6da57b217585af0786db3845d1f0ec1a0dd182f`. Both facets present, matching the claim.
- **wasm-bindgen-cli ↔ crate version match confirmed.** `ARG WASM_BINDGEN_VERSION=0.2.129` equals the `wasm-bindgen` version pinned in `Cargo.lock` (`version = "0.2.129"`), so the generated JS glue and the wasm module agree at init. Checked directly against `Cargo.lock` at head.
- **Builder-Rust-1.88-vs-MSRV-1.82 bump is sound.** MSRV is a floor; 1.88 ≥ 1.82, so compiling the workspace with 1.88 is valid. The bump is justified and documented: `wasm-bindgen-cli` 0.2.129's transitive deps (`icu_*`, `time`) require rustc 1.88. `-slim-bookworm` keeps glibc 2.36 (the ABI constraint — see concern 2), so the newer compiler does not change the runtime target.
- **`.dockerignore` trims context without starving the build.** Excludes `target/`, VCS, `.github/`, docs/`*.md`, and local scratch; retains `crates/`, `Cargo.toml`, `Cargo.lock`, `crates/chirp-frontend/index.html` (not markdown), and `deploy/docker/healthcheck.rs`. Nothing the `COPY . .` build needs is excluded.

No `block`/`major` defects. One maintainability/reproducibility note recorded below (BUILD-1).

### Concern 2 (layer composition + size face) — **PASS**

- **Runtime carries only what it must.** The distroless stage `COPY --from=builder` brings in exactly three things: `/usr/local/bin/chirp-server`, `/usr/local/bin/healthcheck`, and `/srv/chirp` (the SPA bundle). No toolchain, cargo registry, source tree, or build cache crosses the stage boundary — the cache-mounted `target/` never becomes a layer, and artifacts are staged to `/out` precisely so the runtime copies stable paths rather than the build tree.
- **glibc ABI match is correct.** Builder is Debian 12 bookworm (glibc 2.36); runtime `cc-debian12` is the same Debian 12 base. The dynamically-linked server binary runs unchanged; the gate independently verified both report glibc 2.36.
- **Size (41.7 MB) is reasonable and the breakdown holds.** distroless/cc base ≈29 MB + server ≈2.5 MB + stripped healthcheck ≈0.37 MB (`rustc -C strip=symbols`) + SPA ≈0.31 MB. Within the compiled-language `< 50 MB` target; the arithmetic is consistent with the gate's reported total.
- **Ownership/permissions are minimal and correct.** SPA copied `--chown=65532:65532` and read-only at runtime; binaries are root-owned `0755` (default for COPY'd files) and executed — not owned — by the non-root user. No over-provisioning.
- **Cross-reference (not re-filed):** the secret/credential-leakage face of concern 2 is owned by `SUBTASK_security_supplychain`. For its convenience I observed no `ARG`/`COPY` of credentials and no secret material written into any layer; adjudication of that face remains with the security spoke per identity I2.

### Concern 6 (Dockerfile/shell idiom slice) — **PASS**

Idiom is exemplary: `# syntax=docker/dockerfile:1` header (required for the BuildKit cache mounts used); exec-form `ENTRYPOINT ["/usr/local/bin/chirp-server"]` so the server is PID 1 and receives SIGTERM directly; exec-form `HEALTHCHECK CMD ["/usr/local/bin/healthcheck"]`; `set -eux` in the multi-command RUN; single apt layer with `--no-install-recommends` and in-layer `rm -rf /var/lib/apt/lists/*`; absolute `WORKDIR`; OCI `LABEL`s; named builder stage; thorough, accurate comments. One cosmetic `.dockerignore` redundancy noted below (BUILD-2). The healthcheck probe's compile command (`rustc -C opt-level=z -C strip=symbols deploy/docker/healthcheck.rs`) is an intentional, acceptable idiom for a std-only single-file probe (no dependency graph to `--locked`); the probe's own Rust idiom/correctness is `SUBTASK_rustcode_sigterm`'s concern and is not adjudicated here.

---

## Findings table

| Finding ID | Concern | Severity | Location | Evidence | Remediation |
|---|---|---|---|---|---|
| BUILD-1 | 1 | minor | `Dockerfile` (builder stage) `ARG WASM_BINDGEN_VERSION=0.2.129` vs `Cargo.lock` `wasm-bindgen` | The CLI version is hand-duplicated from the authoritative `wasm-bindgen` pin in `Cargo.lock`. The two match today (`0.2.129` = `0.2.129`), so the build is correct. But nothing mechanically enforces the coupling: a future `Cargo.lock` bump that does not also update the ARG would silently reintroduce the exact JS-glue/wasm-module init mismatch the inline comment warns about. | Optional (non-blocking): add a build-time assertion in the RUN that greps the locked version out of `Cargo.lock` and compares, e.g. `test "$(grep -A1 '^name = "wasm-bindgen"$' Cargo.lock \| sed -n 's/^version = "\(.*\)"/\1/p')" = "${WASM_BINDGEN_VERSION}"`, failing the build on drift. Keeps the single source of truth in `Cargo.lock`. |
| BUILD-2 | 6 | nit | `.dockerignore` | Redundant entries: `target/` is subsumed by `**/target/`, and `deploy/README.md` is already covered by the `*.md` rule. Harmless (no functional effect), purely cosmetic. | Optional: drop the redundant `target/` and `deploy/README.md` lines, or keep them as intentional explicitness. No action required. |

---

## Notes

- **Read-only honored.** All diff access was authenticated read-only `gh api .../contents/<path>?ref=bc0c3c0d…`; nothing was edited, staged, committed, pushed, or merged; no container build was run (identity I5; the green machine gate was relied upon for build/run facts).
- **Severity discipline (I4).** No `block`/`major` is filed because none is warranted: the build is correct, reproducible (tag+digest pinning, `--locked`, matched CLI/crate versions), and the runtime image is minimal and ABI-correct. The two recorded items are a maintainability note (minor) and a cosmetic redundancy (nit) — neither is a concrete landable defect that should gate merge; both deliberately avoid dressing a hardening wish as a blocker.
