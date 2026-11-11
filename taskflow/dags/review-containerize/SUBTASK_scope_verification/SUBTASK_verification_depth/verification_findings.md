# Verification-depth partial findings — concern 7 (evidence adequacy)

- **Spoke**: `SUBTASK_verification_depth` (concern-7 analysis child of `SUBTASK_scope_verification`)
- **Concerns owned**: concern **7** — verification / evidence adequacy (identity SV2)
- **Diff reviewed**: PR #22 head commit `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751` of `Nousix-LLC/nswe-demo`
- **Evidence source (machine gate, INPUT — not re-run)**: `taskflow/dags/containerize/SYNTHESIS.md`
- **Method**: each of work-item #12's nine acceptance criteria is mapped to the machine gate's recorded build+run evidence and cross-checked against the diff; each is called `evidenced` / `weakly evidenced` / `unverified`. This is an evidence-to-criterion adequacy judgment, **not** a rebuild.

---

## Per-concern disposition

### Concern 7 — verification / evidence adequacy: **PASS-WITH-NOTES**

The machine gate's recorded evidence genuinely **demonstrates all nine** acceptance criteria to an adequate degree, and the diff corroborates every claimed behavior (the `SIGTERM received; draining in-flight requests` log string, the probe deriving its port from `CHIRP_BIND_ADDR`, and both `@sha256` base-image digest pins all appear verbatim in the diff). **No criterion is left unverified and no claimed behavior is false** — hence no `block` and no `major`. Two criteria are demonstrated through strong *by-construction / indirect* evidence rather than an explicit exercised check — criterion 7 ("builds **reproducibly**") rests on the determinism inputs (digest-pinned bases + `--locked` + version-pinned `wasm-bindgen`) without an empirical repeat-build byte-comparison, and criterion 2's "no toolchain/source leakage" face rests on the distroless base + the explicit 3-artifact `COPY` list + the size breakdown rather than a final-image filesystem/scan. These are evidence-*strengthening* wishes, so per severity discipline (SV6 / inherited I4) they are recorded as `minor`/`nit`, not blockers. Hence PASS-WITH-NOTES rather than PASS.

---

## Nine-criteria evidence-adequacy table (identity SV2)

Each of work-item #12's nine acceptance criteria (as enumerated in `taskflow/dags/containerize/SYNTHESIS.md`), with its adequacy call and the specific machine-gate evidence cited.

| # | Acceptance criterion (abbrev.) | Call | Machine-gate / diff evidence cited |
|---|---|---|---|
| 1 | Multi-stage `Dockerfile` at repo root; builds release server **and** the wasm SPA bundle | **evidenced** | Gate "Design"/"Build evidence": two stages (builder→distroless); builder runs `cargo build --release --locked -p chirp-server` **and** `-p chirp-frontend --example chirp --target wasm32-unknown-unknown` + `wasm-bindgen --target web`. `docker build`→exit 0, 41.7 MB. Run: `GET /` 200 `text/html` (SPA), `GET /pkg/chirp_bg.wasm` 200 **`application/wasm`** (282 026 B), `GET /pkg/chirp.js` 200. Diff `Dockerfile:1-113` confirms both build invocations. Both server and SPA built *and* served — directly demonstrated. |
| 2 | Minimal runtime stage (distroless; no toolchain/source leakage) | **evidenced** (see `SCOPE-V2`) | Runtime base `gcr.io/distroless/cc-debian12:nonroot` (diff `Dockerfile` Stage 2); runtime stage `COPY`s only the server binary, the probe, and `/srv/chirp` (3 artifacts). Image 41.7 MB with breakdown (base ≈29 MB + server 2.5 + probe 0.37 + SPA 0.31). "Distroless (minimal)" directly evidenced by base image + size; "no leakage" is demonstrated **by construction** (distroless/cc has no shell/pkg-mgr/toolchain by definition; only 3 named artifacts cross from builder) — strong but not an explicit final-image scan. |
| 3 | Runs as non-root (explicit `USER 65532`, non-0 uid) | **evidenced** | Diff `Dockerfile`: `USER 65532:65532`. Gate run evidence: "Runtime user: `Config.User=65532:65532`; live PID 1 runs as uid `65532` (non-root)" — static directive **and** runtime-observed live uid both confirm. |
| 4 | `HEALTHCHECK` exercising `/healthz` | **evidenced** | Diff `Dockerfile`: `HEALTHCHECK … CMD ["/usr/local/bin/healthcheck"]`; `deploy/docker/healthcheck.rs` issues `GET /healthz`. Gate: "Docker `HEALTHCHECK` healthy, failing-streak 0, probe exit 0" and `GET /healthz` 200 `{"status":"ok",…}`. The probe was actually exercised and observed healthy. |
| 5 | Listen addr/port + static path configurable + documented; starts & serves SPA + API out of the box, in-memory default (no external DB) | **evidenced** (see `SCOPE-V3`) | "Out of the box" face directly evidenced: `GET /` 200 + `POST /api/users` 201 + "External DB required: **No** — in-memory repository default". Documentation: `deploy/README.md` Configuration table (`CHIRP_BIND_ADDR`/`CHIRP_STATIC_DIR`/`RUST_LOG`) + one-knob port example. Configurability demonstrated **indirectly**: the container ran with non-dev-default `CHIRP_BIND_ADDR=0.0.0.0:8080` (vs the `127.0.0.1` dev default) and `CHIRP_STATIC_DIR=/srv/chirp`, and was reachable + served the SPA — i.e. both knobs are honored at runtime. An explicit overridden-port run (e.g. `-e CHIRP_BIND_ADDR=0.0.0.0:9000` with the healthcheck tracking it) is documented but not exercised. |
| 6 | `.dockerignore` excluding `target/`, VCS, local scratch | **evidenced** | Diff `.dockerignore:1-34` contains `target/`, `**/target/`, `.git/`, `.gitignore` (VCS), `.env`, `.env.*`, `.vscode/`, `.idea/`, `*.swp`, `.DS_Store` (scratch). All three required exclusion classes present verbatim; the required content is directly visible in the diff (static-artifact criterion). |
| 7 | Builds reproducibly, reasonably small (41.7 MB); bases pinned by tag + digest; size + build/run commands documented | **weakly evidenced** (see `SCOPE-V1`) | "Small" evidenced (41.7 MB, < 50 MB target, breakdown). "Digest-pinned" evidenced: diff `Dockerfile` both `FROM` lines carry tag **+** `@sha256` (`rust:1.88-slim-bookworm@sha256:38bc5a86…`, `distroless/cc-debian12:nonroot@sha256:9dac0a79…`). "Documented" evidenced (`deploy/README.md` + `README.md` build/run; size in gate). **"Reproducibly"** rests on the determinism *inputs* — digest pins + all `cargo … --locked` + `wasm-bindgen-cli … --locked` version-pinned — recorded from **one** build (exit 0); no second independent build / byte-comparison was run, so empirical reproducibility is inferred, not exercised. |
| 8 | Brief docs (`deploy/README.md` + README section): build, run, env/config, healthcheck | **evidenced** | Diff `deploy/README.md:1-104` has Build, Run, Configuration (env table), and Healthcheck sections; `README.md` adds a "Running chirp in a container" section with build/run/`curl /healthz`. All four required topics directly present. |
| 9 | Commits on `work/containerize`; PR into `main` that `Closes #12`; PR not merged; `main` not pushed | **evidenced** | Gate header: branch `work/containerize` (2 commits off `main`), PR #22 **OPEN**, base `main`, `Closes #12`, "`main` after this work — **unchanged**". Corroborated by the grandparent hub's PR coordinates (PR #22 OPEN/MERGEABLE/CLEAN, head `bc0c3c0…`, `Closes #12`). Observation (not a defect, reconciled upstream): the gate recorded `main` at `fcfc7a2`, while the review hub notes `main` advanced to `7a81849` after #10 landed and already asserts PR #22 still MERGEABLE/CLEAN against it — no action needed here; flagged only so the verdict gate is aware. |

**SV2 completeness**: all nine criteria appear, each with exactly one call and cited evidence. Calls: **7 evidenced, 1 weakly evidenced (#7), 0 unverified**; #2 and #5 are evidenced with a strengthening nit noted below. No criterion omitted.

---

## Findings (`SCOPE-V` partition of the inherited `SCOPE` namespace)

| Finding ID | Concern | Severity | Location | Evidence | Remediation |
|---|---|---|---|---|---|
| `SCOPE-V1` | 7 | `minor` | `Dockerfile` (both `FROM` lines) + machine gate "Build evidence" (single `docker build`) | Criterion 7's "builds **reproducibly**" is demonstrated by determinism *inputs* only — base images digest-pinned, all Cargo builds `--locked`, `wasm-bindgen-cli` version+`--locked` — recorded from a single build. No independent repeat build or digest/byte comparison was performed, so empirical reproducibility is inferred, not observed. Standard, accepted basis for the claim; the gap is confidence-strengthening, not a defect (SV6). | (optional) In a follow-up, run the build twice (ideally on two hosts) and compare the resulting image `@sha256` / layer digests, or record a `docker buildx --sbom`/rebuild comparison, to convert the reproducibility claim from by-construction to empirically observed. |
| `SCOPE-V2` | 7 | `nit` | `Dockerfile` Stage 2 (runtime) | Criterion 2's "no toolchain/source leakage" is demonstrated by construction (distroless/cc base has no shell/package-manager/toolchain; runtime stage `COPY`s only the 3 named artifacts from the builder; 41.7 MB size breakdown leaves no room for a leaked toolchain) rather than by an explicit final-image filesystem listing or image scan. | (optional) Record a one-line `docker run --entrypoint … ` is impossible (no shell) — instead attach a `docker sbom chirp:local` / `dive`/`syft` inventory of the final image to the evidence to make "no source/toolchain in the runtime layer" an exercised check. |
| `SCOPE-V3` | 7 | `nit` | `deploy/README.md` §Configuration + machine gate run evidence (single default-config run) | Criterion 5's configurability is demonstrated indirectly: the container ran with non-dev-default `CHIRP_BIND_ADDR`/`CHIRP_STATIC_DIR` and served correctly, which shows both knobs are honored. The specifically documented one-knob alternate-port run (e.g. `-e CHIRP_BIND_ADDR=0.0.0.0:9000`, with the `HEALTHCHECK` probe tracking the new port via the same variable) was not exercised in the recorded evidence. | (optional) Add one recorded run on a non-default port demonstrating both the server bind and the healthcheck following `CHIRP_BIND_ADDR`, closing the only un-exercised face of criterion 5. |

No `block` and no `major` findings: every acceptance criterion carries adequate demonstrating evidence (direct, or strong by-construction/indirect), and the diff cross-check surfaced no false claimed behavior. The three findings above are evidence-strengthening notes held to `minor`/`nit` per the inherited severity discipline (SV6 / I4).

---

## Metadata

- **Identity**: SV2 (nine-criteria completeness) satisfied — all nine criteria individually called with cited evidence.
- **Finding-ID prefix**: `SCOPE-V` (per `../contracts/_MANIFEST.yaml` ownership partition); no collision with the sibling's `SCOPE-S` namespace.
- **Constraints honored**: read-only (I5) — no rebuild, no edit/stage/commit/push, no GitHub write; relied on `taskflow/dags/containerize/SYNTHESIS.md` for build/run facts; diff accessed read-only via `gh pr diff 22`.
- **Scope boundary**: scope-conformance (concern 8) and the per-artifact deep analyses (build/security/operability/Rust) are owned by siblings and are **not** adjudicated here; the criterion-9 `main`-SHA observation is passed through to the verdict gate, not filed as a finding.
- **Input**: machine gate + PR #22 diff (6 touched files: `.dockerignore`, `Dockerfile`, `README.md`, `crates/chirp-server/src/main.rs`, `deploy/README.md`, `deploy/docker/healthcheck.rs`).
</content>
</invoke>
