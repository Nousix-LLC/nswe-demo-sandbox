# Scope & Verification findings — PR #22 / work-item #12

## 1. Header

- **Spoke**: `SUBTASK_scope_verification`
- **Concerns owned**: concern **7** (verification / evidence adequacy) and concern **8** (scope
  conformance — containerization only; no `.github/` CI, no k8s/ArgoCD manifests, no live deploy).
- **Diff reviewed**: PR #22 head commit `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751` of
  `Nousix-LLC/nswe-demo` (`work/containerize` → `main`, OPEN/MERGEABLE).
- **Composition**: merged by the spoke's synthesis gate from two analysis children —
  `SUBTASK_verification_depth` (concern 7, `SCOPE-V*`) and `SUBTASK_scope_conformance`
  (concern 8, `SCOPE-S*`). Finding IDs and dispositions are preserved verbatim from the children.

## 2. Per-concern disposition

### Concern 7 — verification / evidence adequacy: **PASS-WITH-NOTES**

The machine gate's recorded evidence (`taskflow/dags/containerize/SYNTHESIS.md`, an INPUT — not
re-run) genuinely demonstrates **all nine** of work-item #12's acceptance criteria to an adequate
degree, and the diff corroborates every claimed behavior: the `SIGTERM received; draining in-flight
requests` log string, the probe deriving its port from `CHIRP_BIND_ADDR`, and both `@sha256`
base-image digest pins all appear verbatim in the diff. No criterion is left `unverified` and no
claimed behavior is false — hence no `block` and no `major`. Two criteria rest on strong
*by-construction / indirect* evidence rather than an explicit exercised check: criterion 7
("builds **reproducibly**") rests on determinism inputs (digest-pinned bases + `--locked` +
version-pinned `wasm-bindgen`) without an empirical repeat-build byte-comparison (`SCOPE-V1`), and
criterion 2's "no toolchain/source leakage" rests on the distroless base + the explicit 3-artifact
`COPY` list + the size breakdown rather than a final-image scan (`SCOPE-V2`); criterion 5's
configurability is shown indirectly via the non-default-config run rather than an explicit
overridden-port run (`SCOPE-V3`). These are evidence-*strengthening* wishes, held to `minor`/`nit`
per severity discipline (SV6 / inherited I4) — hence PASS-WITH-NOTES rather than PASS.

### Concern 8 — scope conformance: **PASS-WITH-NOTES**

PR #22 touches exactly six files, and every one is squarely within work-item #12's
containerization scope: the `Dockerfile` + `.dockerignore` (the build recipe and its context
control), `deploy/docker/healthcheck.rs` (the distroless `HEALTHCHECK` probe the Dockerfile
compiles and runs), `deploy/README.md` + the `README.md` "Running chirp in a container" section
(the container documentation #12 owes), and the `crates/chirp-server/src/main.rs` SIGTERM change
(the minimal, unix-gated graceful-shutdown handler #12 explicitly calls for). **No file under
`.github/` is authored, no Kubernetes/ArgoCD manifest is added, and no live registry push or
cluster deploy action appears anywhere in the diff** — the Dockerfile has no `docker push`, no
registry login, and no `kubectl`/`argocd` invocation; `LABEL org.opencontainers.image.source=...`
is metadata, not a push. The diff is affirmatively boundary-respecting: `.dockerignore` excludes
`.github/` with the comment *"CI/CD — owned by the ci-actions work-item"*, and `deploy/README.md`
explicitly scopes GHCR publishing out to `ci-actions` (#11) and k8s/ArgoCD out to `deploy-argocd`
(#13). Those are mentions of the boundary, not crossings of it. The one advisory note (`SCOPE-S1`)
is a forward-looking directory-namespace observation, not a scope defect — hence PASS-WITH-NOTES.

**The `Dockerfile`-as-hand-off distinction (declared boundary, NOT a breach).** Work-item #11
(`ci-actions`) will later add a GitHub Actions job that *consumes* this `Dockerfile` to build and
push to GHCR. That is a declared, one-directional, artifact-mediated hand-off: #12 authors the
build recipe; #11 authors the CI that invokes it and performs the push. #12 authors nothing under
`.github/`, performs no registry auth/push, and configures no GHCR. A Dockerfile that a later CI
job consumes is the expected in-scope deliverable of a containerization work-item — filing it as an
encroachment on #11 would be a category error, and is explicitly not done.

## 3. Findings table

| Finding ID | Concern | Severity | Location | Evidence | Remediation |
|---|---|---|---|---|---|
| `SCOPE-V1` | 7 | `minor` | `Dockerfile` (both `FROM` lines) + machine gate "Build evidence" (single `docker build`) | Criterion 7's "builds **reproducibly**" is demonstrated by determinism *inputs* only — base images digest-pinned, all Cargo builds `--locked`, `wasm-bindgen-cli` version+`--locked` — recorded from a single build. No independent repeat build or digest/byte comparison was performed, so empirical reproducibility is inferred, not observed. A standard, accepted basis for the claim; the gap is confidence-strengthening, not a defect (SV6). | (optional) In a follow-up, run the build twice (ideally on two hosts) and compare the resulting image `@sha256` / layer digests, or record a `docker buildx --sbom`/rebuild comparison, to convert the reproducibility claim from by-construction to empirically observed. |
| `SCOPE-V2` | 7 | `nit` | `Dockerfile` Stage 2 (runtime) | Criterion 2's "no toolchain/source leakage" is demonstrated by construction (distroless/cc base has no shell/package-manager/toolchain; the runtime stage `COPY`s only the 3 named artifacts from the builder; the 41.7 MB size breakdown leaves no room for a leaked toolchain) rather than by an explicit final-image filesystem listing or image scan. | (optional) Attach a `docker sbom chirp:local` / `dive` / `syft` inventory of the final image to the evidence to make "no source/toolchain in the runtime layer" an exercised check. |
| `SCOPE-V3` | 7 | `nit` | `deploy/README.md` §Configuration + machine gate run evidence (single default-config run) | Criterion 5's configurability is demonstrated indirectly: the container ran with non-dev-default `CHIRP_BIND_ADDR`/`CHIRP_STATIC_DIR` and served correctly, which shows both knobs are honored. The specifically documented one-knob alternate-port run (e.g. `-e CHIRP_BIND_ADDR=0.0.0.0:9000`, with the `HEALTHCHECK` probe tracking the new port via the same variable) was not exercised in the recorded evidence. | (optional) Add one recorded run on a non-default port demonstrating both the server bind and the healthcheck following `CHIRP_BIND_ADDR`, closing the only un-exercised face of criterion 5. |
| `SCOPE-S1` | 8 | `nit` | `deploy/` directory namespace (`deploy/README.md`, `deploy/docker/healthcheck.rs`) | `deploy/` currently holds only container artifacts, which is in scope. However, deployment manifests (k8s/ArgoCD) owned by work-item #13 `deploy-argocd` conventionally also live under a `deploy/` path. There is **no collision today** — #12 added no manifest — but the two work-items share a top-level directory name. A forward-looking posture/naming observation, **not** a scope defect in this diff (I4/SV6). | (optional; none required) If desired, keep container assets under `deploy/docker/` (the probe already is) and leave `deploy/k8s/` or `deploy/argocd/` free for #13, so the shared `deploy/` root stays unambiguous as both work-items land. |

**Summary**: 0 `block`, 0 `major`, 1 `minor`, 3 `nit`. No OPEN `block` finding ⇒ neither concern
forces REQUEST-CHANGES from this spoke; both dispositions are PASS-WITH-NOTES.

## 4. Nine-criteria evidence-adequacy detail (concern 7, identity SV2)

Each of work-item #12's nine acceptance criteria, with its adequacy call and the specific
machine-gate / diff evidence (carried forward from `SUBTASK_verification_depth`):

| # | Acceptance criterion (abbrev.) | Call | Evidence (machine gate / diff) |
|---|---|---|---|
| 1 | Multi-stage `Dockerfile`; builds release server **and** wasm SPA bundle | **evidenced** | Two stages (builder→distroless); builder runs `cargo build --release --locked -p chirp-server` **and** `-p chirp-frontend --example chirp --target wasm32-unknown-unknown` + `wasm-bindgen --target web`. `docker build`→exit 0, 41.7 MB. Run: `GET /` 200 `text/html`, `GET /pkg/chirp_bg.wasm` 200 `application/wasm` (282 026 B), `GET /pkg/chirp.js` 200. Diff `Dockerfile:1-113` confirms both build invocations. |
| 2 | Minimal runtime stage (distroless; no toolchain/source leakage) | **evidenced** (see `SCOPE-V2`) | Runtime base `gcr.io/distroless/cc-debian12:nonroot`; runtime stage `COPY`s only the server binary, the probe, and `/srv/chirp` (3 artifacts). 41.7 MB with breakdown (base ≈29 MB + server 2.5 + probe 0.37 + SPA 0.31). "No leakage" shown **by construction**. |
| 3 | Runs as non-root (explicit `USER 65532`, non-0 uid) | **evidenced** | Diff `Dockerfile`: `USER 65532:65532`. Gate: live PID 1 runs as uid `65532`; `Config.User=65532:65532`. Static directive **and** runtime-observed uid both confirm. |
| 4 | `HEALTHCHECK` exercising `/healthz` | **evidenced** | Diff: `HEALTHCHECK … CMD ["/usr/local/bin/healthcheck"]`; `deploy/docker/healthcheck.rs` issues `GET /healthz`. Gate: `HEALTHCHECK` healthy, failing-streak 0, probe exit 0; `GET /healthz` 200 `{"status":"ok",…}`. |
| 5 | Addr/port + static path configurable + documented; serves SPA + API out of the box, in-memory default | **evidenced** (see `SCOPE-V3`) | `GET /` 200 + `POST /api/users` 201 + "External DB required: No". `deploy/README.md` Configuration table (`CHIRP_BIND_ADDR`/`CHIRP_STATIC_DIR`/`RUST_LOG`). Configurability shown **indirectly**: ran with non-dev-default `CHIRP_BIND_ADDR=0.0.0.0:8080` + `CHIRP_STATIC_DIR=/srv/chirp` and served the SPA. |
| 6 | `.dockerignore` excluding `target/`, VCS, local scratch | **evidenced** | Diff `.dockerignore:1-34`: `target/`, `**/target/`, `.git/`, `.gitignore`, `.env`, `.env.*`, `.vscode/`, `.idea/`, `*.swp`, `.DS_Store`. All three exclusion classes present verbatim. |
| 7 | Builds reproducibly, ~41.7 MB; bases pinned by tag + digest; size + commands documented | **weakly evidenced** (see `SCOPE-V1`) | "Small" (41.7 MB < 50 MB target). "Digest-pinned": both `FROM` lines carry tag **+** `@sha256`. "Documented": `deploy/README.md` + `README.md`. "**Reproducibly**" rests on determinism inputs recorded from **one** build; no second build / byte-comparison — inferred, not exercised. |
| 8 | Brief docs (`deploy/README.md` + README section): build, run, env/config, healthcheck | **evidenced** | Diff `deploy/README.md:1-104` has Build, Run, Configuration (env table), Healthcheck; `README.md` adds a "Running chirp in a container" section with build/run/`curl /healthz`. |
| 9 | Commits on `work/containerize`; PR into `main` `Closes #12`; PR not merged; `main` not pushed | **evidenced** | Gate: branch `work/containerize` (2 commits off `main`), PR #22 OPEN, base `main`, `Closes #12`, `main` unchanged. (Observation, not a defect, passed to the verdict gate: gate recorded `main` at `fcfc7a2` while the review hub notes `main` advanced to `7a81849` after #10 landed, PR #22 still MERGEABLE/CLEAN — no action here.) |

All nine criteria called exactly once: **8 evidenced, 1 weakly evidenced (#7), 0 unverified.**

## 5. Scope-conformance detail (concern 8, identity SV3)

The complete PR #22 touched-file set is the six files below; each judged against work-item #12
scope (containerization only). All six are **IN SCOPE**; none falls under `.github/`, a k8s/ArgoCD
manifest path, or a live-deploy action.

| # | Path | Δ (add/del) | In/Out | Basis |
|---|------|-------------|--------|-------|
| 1 | `Dockerfile` | +113 / 0 | **IN** | Core #12 artifact: multi-stage build of release server + wasm SPA into a non-root distroless runtime. Build recipe only. Declared hand-off consumed by #11. |
| 2 | `.dockerignore` | +34 / 0 | **IN** | Build-context hygiene. Lists `.github/` as an *exclusion* with an "owned by ci-actions" note — a boundary disclaimer, not CI authorship. |
| 3 | `deploy/docker/healthcheck.rs` | +58 / 0 | **IN** | Std-only `/healthz` probe the Dockerfile's `HEALTHCHECK` runs (distroless has no shell/curl). Not a Cargo crate. |
| 4 | `deploy/README.md` | +104 / 0 | **IN** | Container build/run/config/healthcheck doc. Explicitly scopes out GHCR→#11 and k8s/ArgoCD→#13. |
| 5 | `README.md` | +16 / 0 | **IN** | Adds only a "Running chirp in a container" section (local `docker build`/`run`/`curl`). Pre-existing Actions/ArgoCD/k3s lines are unchanged context, not added here. |
| 6 | `crates/chirp-server/src/main.rs` | +33 / −6 | **IN** | Extends `shutdown_signal()` to await `SIGTERM` (unix-gated, `#[cfg(not(unix))]` fallback). Narrowly the graceful-container-shutdown change #12 requires; no unrelated feature. |

**Out-of-scope files**: none. **Under `.github/`**: none. **k8s/ArgoCD manifests**: none. **Live
registry/cluster deploy actions**: none.

## 6. Notes / cross-references (not findings)

- The per-artifact deep analyses (build correctness, security/supply-chain, operability, Rust
  idiom) are owned by the four sibling spokes of the parent DAG; this spoke did not re-file into
  their territory (grandparent identities I1/I2).
- The criterion-9 `main`-SHA observation (gate `fcfc7a2` vs review hub `7a81849` post-#10) is a
  pass-through to the grandparent `SUBTASK_verdict_synthesis`, not a finding here.
- Rendering the overall PR verdict and posting the single GitHub review are the grandparent
  verdict-synthesis gate's job alone; this spoke posts nothing.
- Read-only honored throughout (identity I5): only `gh pr view`/`gh pr diff` (read) were used by
  the children; nothing edited, staged, committed, pushed, or posted; no container rebuild.

---
*Spoke `SUBTASK_scope_verification` · concerns 7 + 8 · PR #22 @ `bc0c3c0d` · dispositions
PASS-WITH-NOTES / PASS-WITH-NOTES · 0 block, 0 major, 1 minor, 3 nit · merged by
`SUBTASK_findings_synthesis` (gate PASS).*
