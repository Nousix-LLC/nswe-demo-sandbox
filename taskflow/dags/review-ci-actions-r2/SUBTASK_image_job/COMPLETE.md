# COMPLETE — SUBTASK_image_job (concern 4)

**Task**: Review the `image` job in `.github/workflows/ci.yml` (PR #21, head `c8123376`) against the now-present `./Dockerfile` on `main` (`61f924a`). Emit findings in the frozen schema.

**Decompose evaluation**: `Atomic` — one reviewer, one CI job, one findings file; all decomposition triggers cleared (token/scope/output) and both concern tests passed.

## What was done
- Read the `image` job at head `c8123376` (fetched `ci.yml` via `gh api ... ?ref=c8123376`).
- Read `./Dockerfile` on `main` at `61f924a`; spot-checked `.dockerignore` and `deploy/docker/healthcheck.rs` at `61f924a` (both present).
- Judged the job against the present Dockerfile (not the absent-Dockerfile premise it was authored under), covering all six sub-aspects of concern 4: gating, skip-detection, build context & Dockerfile path, image name/tag, GHCR `GITHUB_TOKEN` auth (functional), digest/push correctness.
- Grounded against methodology: `containerization/Containerization_Docker_Build_Methodology.md`, `containerization/Containerization_Compose_Deploy_Methodology.md` (registry push), `code-review/CodeReview_Checklist_Methodology.md`.

## Output
- `findings.md` (this workspace), conformant to `../contracts/findings_schema.md`, ids `IMG-n`, header stating head `c8123376` and Dockerfile read at `61f924a`.

## Result (spoke roll-up)
- **block: 0 · major: 1 · minor: 1 · nit: 2**
- **IMG-1 (major)** — image build uses Rust 1.88, decoupled from and older than CI's validated `RUST_TOOLCHAIN: 1.97` (which CI pins because the locked dep graph fails on older rustc); the `image` job is `main`-push-only, so the Docker build is never a PR check → unverified pre-merge, can break on `main` post-merge while PR CI stays green. `required_change` supplied.
- **IMG-2 (minor)** — the "Dockerfile missing → skip" guard is now dead on `main`; not misfiring, but carries a silent-skip-on-removal hazard.
- **IMG-3, IMG-4 (nits)** — `workflow_dispatch` never (re)publishes the image; pushed digest not surfaced for provenance.

Skip-detection explicitly classified: **dead (else-branch) but correct / non-misfiring** at this head; recommend removal (IMG-2). Build context, image name/tag, GHCR auth, and digest/push correctness each judged (all clean bar the nits).

## Verification
- `findings.md` exists at the declared path, follows the frozen record shape, every finding has location + rationale, the single `major` carries a `required_change`, and the header states the reviewed head `c8123376`. Read-only constraint honored: only `gh` GET/`api` calls were made; nothing built, pushed, or merged.
