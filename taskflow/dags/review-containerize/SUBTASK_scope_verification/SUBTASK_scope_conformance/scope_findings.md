# Scope-conformance findings — PR #22 / work-item #12 (concern 8)

## 1. Header

- **Spoke**: `SUBTASK_scope_conformance`
- **Concerns owned**: concern 8 — scope conformance (containerization only; no `.github/` CI,
  no k8s/ArgoCD manifests, no live deploy). Finding-ID prefix `SCOPE-S` (identity SV3/SV4).
- **Diff reviewed**: PR #22 head commit `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751` of
  `Nousix-LLC/nswe-demo` (`work/containerize` → `main`, OPEN/MERGEABLE).
- **Method**: authoritative touched-file set from `gh pr view 22 --json files` cross-checked
  against `gh pr diff 22` (both read-only, account `mattsmcknight`). No GitHub write; no rebuild.

## 2. Per-concern disposition

### Concern 8 — scope conformance: **PASS-WITH-NOTES**

PR #22 touches exactly six files, and every one is squarely within work-item #12's
containerization scope: the `Dockerfile` + `.dockerignore` (the build recipe and its context
control), `deploy/docker/healthcheck.rs` (the distroless `HEALTHCHECK` probe the Dockerfile
compiles and runs), `deploy/README.md` + the `README.md` "Running chirp in a container" section
(the container build/run/config documentation #12 owes), and the `crates/chirp-server/src/main.rs`
SIGTERM change (the minimal, unix-gated graceful-shutdown handler #12 explicitly calls for so a
containerized instance drains and exits 0 rather than being SIGKILL'd). **No file under `.github/`
is authored, no Kubernetes/ArgoCD manifest is added, and no live registry push or cluster deploy
action appears anywhere in the diff.** The Dockerfile contains no `docker push`, no registry
login, and no `kubectl`/`argocd` invocation — it is a pure build recipe (`LABEL
org.opencontainers.image.source=...` is only metadata, not a push).

The diff is, in fact, affirmatively boundary-respecting rather than merely non-infringing: it
*names* the adjacent work-items' territory precisely to disclaim it. `.dockerignore` excludes
`.github/` with the comment *"CI/CD — owned by the ci-actions work-item, not needed to build the
image,"* and `deploy/README.md` states *"CI image publishing (GHCR) is owned by the `ci-actions`
work-item (`.github/workflows`), and Kubernetes manifests / ArgoCD by `deploy-argocd`; neither is
in this image's scope."* Those references to `.github/`, GHCR, k8s, and ArgoCD are **mentions of
the boundary, not crossings of it** — the opposite of scope creep.

The one advisory note (`SCOPE-S1`, below) is a forward-looking directory-namespace observation,
not a scope defect — hence PASS-**WITH-NOTES** rather than FAIL. No `block` or `major` finding
exists for this concern.

### The `Dockerfile`-as-hand-off distinction (declared boundary, NOT a breach)

Work-item #11 (`ci-actions`, owner of `.github/`) will later add a GitHub Actions image-build job
that **consumes** this `Dockerfile` to build and push the image to GHCR. That downstream
consumption relationship is a **declared, honest hand-off, not a scope incursion by #12**:

- #12 authors the *build recipe* (the `Dockerfile`); #11 authors the *CI that invokes it* and
  performs the GHCR push. These are disjoint artifacts in disjoint paths.
- #12 authors **nothing** under `.github/`, performs **no** registry authentication or push, and
  configures **no** GHCR. The hand-off is one-directional and artifact-mediated: #11 reads #12's
  output; #12 does not reach into #11.
- The boundary is not merely clean, it is **documented** (the `deploy/README.md` note quoted
  above), which is precisely how a declared hand-off should look.

A Dockerfile that a later CI job consumes is therefore the expected, in-scope deliverable of a
containerization work-item — it would be impossible for #12 to deliver "a container image for the
chirp app" without it. Filing the `Dockerfile` as an out-of-scope encroachment on #11 would be a
category error, and is explicitly **not** done here.

## 3. Enumerated touched-file set (identity SV3 — complete set, each judged in/out of #12 scope)

The complete PR #22 touched-file set is the six files below; each is judged against work-item #12
scope (containerization only). All six are **IN SCOPE**; none falls under `.github/`, a k8s/ArgoCD
manifest path, or a live-deploy action.

| # | Path | Δ (add/del) | In/Out of #12 scope | Basis |
|---|------|-------------|---------------------|-------|
| 1 | `Dockerfile` | +113 / 0 | **IN** | The core #12 artifact: multi-stage build of the release server + wasm SPA into a non-root distroless runtime. Build recipe only — no push/deploy. Declared hand-off consumed by #11's image-build job (see §distinction). |
| 2 | `.dockerignore` | +34 / 0 | **IN** | Build-context hygiene for the `Dockerfile`. Lists `.github/` as an *exclusion* with an explicit "owned by ci-actions" note — a boundary disclaimer, not CI authorship. |
| 3 | `deploy/docker/healthcheck.rs` | +58 / 0 | **IN** | Std-only `/healthz` probe the Dockerfile's `HEALTHCHECK` runs (distroless has no shell/curl). Container operability artifact of #12; not a Cargo crate (does not touch the workspace manifest). |
| 4 | `deploy/README.md` | +104 / 0 | **IN** | Container build/run/configuration/healthcheck reference doc for the image. Explicitly scopes out GHCR→#11 and k8s/ArgoCD→#13. Documentation slice of #12. |
| 5 | `README.md` | +16 / 0 | **IN** | Adds only a "Running chirp in a container" section (local `docker build`/`run`/`curl`). The pre-existing lines mentioning Actions/ArgoCD/k3s are unchanged context, not added by this PR. |
| 6 | `crates/chirp-server/src/main.rs` | +33 / −6 | **IN** | Extends `shutdown_signal()` to also await `SIGTERM` (unix-gated, with a `#[cfg(not(unix))]` fallback). Narrowly the graceful-container-shutdown change #12 requires; no unrelated feature change. |

**Out-of-scope files**: none. **Files under `.github/`**: none. **k8s/ArgoCD manifest files**:
none (the `deploy/` directory contains only `README.md` and `docker/healthcheck.rs` — container
artifacts, not deployment manifests). **Live registry/cluster deploy actions**: none.

## 4. Findings table (`SCOPE-S` prefix, conforming to `../../contracts/findings_schema.md`)

| Finding ID | Concern | Severity | Location | Evidence | Remediation |
|---|---|---|---|---|---|
| `SCOPE-S1` | 8 | `nit` | `deploy/` directory namespace (`deploy/README.md`, `deploy/docker/healthcheck.rs`) | `deploy/` currently holds only container artifacts, which is in scope. However, deployment manifests (k8s/ArgoCD) owned by work-item #13 `deploy-argocd` conventionally also live under a `deploy/` path. There is **no collision today** — #12 added no manifest — but the two work-items share a top-level directory name. This is a forward-looking posture/naming observation, **not** a scope defect in this diff (severity discipline I4/SV6: a boundary posture preference is `nit`, not `block`/`major`). | Optional (nit; none required). If desired, keep container assets under `deploy/docker/` (the probe already is) and leave `deploy/k8s/` or `deploy/argocd/` free for #13, so the shared `deploy/` root stays unambiguous as both work-items land. |

## 5. Notes / cross-references (not findings)

- **Verification/evidence adequacy (concern 7)** is owned by the sibling `SUBTASK_verification_depth`;
  whether the machine-gate evidence *demonstrates* the nine acceptance criteria is assessed there,
  not here. This spoke judged only the scope *boundary*.
- The per-artifact deep analyses (build correctness, security/supply-chain, operability, Rust
  idiom) are owned by the four sibling spokes of the grandparent DAG; this spoke did not re-file
  into their territory (grandparent identities I1/I2).
- Read-only honored throughout: only `gh pr view`/`gh pr diff` (read) were used; nothing was
  edited, staged, committed, pushed, or posted to GitHub.

---
*Spoke `SUBTASK_scope_conformance` · concern 8 · PR #22 @ `bc0c3c0d` · disposition PASS-WITH-NOTES
(1 nit, 0 minor, 0 major, 0 block).*
