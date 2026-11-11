# Findings — SUBTASK_supply_chain_security (concern 3)

**Spoke**: `SUBTASK_supply_chain_security` · **Concern covered**: 3 (workflow security / least-privilege / supply-chain)
**PR**: #21 "CI: GitHub Actions for the Rust/WASM workspace (#11)", `Nousix-LLC/nswe-demo`
**PR head reviewed**: `c8123376` (`c8123376ca1794c0b0466f41a1204bf3c3301b16`)
**Artifact under review**: `.github/workflows/ci.yml` (fetched at head via `gh api`)
**Reviewer role**: read-only; nothing pushed, nothing changed.

---

## Findings

| id | severity | concern | location | finding | rationale | required_change |
|----|----------|---------|----------|---------|-----------|-----------------|
| SEC-1 | minor | 3 | `.github/workflows/ci.yml` — all `uses:` steps (checkout, rust-toolchain, rust-cache, docker/login, docker/metadata, docker/setup-buildx, docker/build-push) | Every third-party action is pinned by a **mutable tag/branch ref** (`actions/checkout@v4`, `dtolnay/rust-toolchain@1.97`, `Swatinem/rust-cache@v2`, `docker/login-action@v3`, `docker/metadata-action@v5`, `docker/setup-buildx-action@v3`, `docker/build-push-action@v6`), not by an immutable commit SHA. None is SHA-pinned. | Mutable refs let the action owner — or an attacker who compromises that account — re-point the ref to malicious code that then runs on the runner (the tag-move attack class, e.g. the Mar-2025 `tj-actions/changed-files` compromise that dumped CI secrets). SHA-pinning is the GitHub / OpenSSF-Scorecard "Pinned-Dependencies" recommended mitigation. **Impact is non-uniform**: the fmt/clippy/test/wasm/doc jobs hold only `contents: read`, so a poisoned action there has a read-only blast radius; the **`image` job is the higher-impact slice** — its `docker/login-action@v3` and `docker/build-push-action@v6` run with `packages: write` and the `GITHUB_TOKEN`, so a poisoned tag there could exfiltrate the write-scoped token or push a malicious image to GHCR. Mitigating factors keeping this below `major`: (a) supply-chain hardening is an explicitly owned, separate track — **issue #24** — so blocking this CI-standup PR on it would reflexively block what #24 owns; (b) all refs are reputable, widely-used publishers (GitHub-first-party `actions/*`, `docker/*`, `dtolnay`, `Swatinem`); (c) the write-token actions fire **only on push to `main`** (post-merge), never on PR triggers, so a malicious PR cannot reach them. Hence advisory, not verdict-forcing. | — (minor; advisory) **Suggested for issue #24**: SHA-pin all third-party actions (`uses: owner/action@<40-char-sha>  # vX.Y.Z`), and **prioritize the `image` job's `docker/*` actions first** since they are the write-scoped slice; adopt Dependabot `package-ecosystem: github-actions` to keep the SHAs current. |
| SEC-2 | nit | 3 | `.github/workflows/ci.yml` — `image` job, `docker/build-push-action@v6` step | The published GHCR image carries no build **provenance / attestation** and no SBOM (`provenance:` / `sbom:` inputs unset; no `id-token: write` / `attestations: write`). | Artifact-integrity hardening (SLSA provenance, signed attestations, SBOM) is the "trust the artifact you produced" half of supply-chain security. Its absence is not a defect in a CI-standup PR and overlaps the #24 hardening track, but recording it completes the concern-3 picture. | — (nit; optional) **Suggested for issue #24**: add `id-token: write` to the `image` job and set `provenance: true` (and optionally `sbom: true`) on `docker/build-push-action`, or sign with cosign, when the image publish path is hardened. |

---

## Concern-coverage note (concern 3)

- **Top-level least-privilege** — *clean.* `permissions: contents: read` sets a read-only `GITHUB_TOKEN` as the workflow-wide default; no permission is granted that a job does not need. This is the recommended secure-by-default posture.
- **Per-job `packages: write` scoping** — *clean.* The elevated `packages: write` lives only in the `image` job's job-level `permissions` block, which *replaces* (does not merge with) the top-level set, so the write scope is confined to that single job and every other job retains only `contents: read`. The elevation is minimal (`contents: read` + `packages: write`, nothing more) and justified (GHCR push).
- **Secret handling** — *clean.* The only secret referenced is the built-in `${{ secrets.GITHUB_TOKEN }}` for GHCR login; no long-lived PATs and no external secrets. The write-scoped token is reachable only on `push`→`main` (the `image` job's `if:` gate excludes PR events), so it is never exposed to PR-triggered or fork runs. No untrusted `github.event.*` expression is interpolated into any `run:` shell step (no expression-injection sink).
- **Third-party action pinning** — *has findings.* Every external action is tag/branch-pinned rather than SHA-pinned (SEC-1); the produced image lacks provenance/attestation (SEC-2). Both are supply-chain exposures calibrated against the owned hardening track **issue #24** and recorded accordingly.
- **Cross-reference (not duplicated here):** the *functional* correctness of the `image` job (build context, image name/tag derivation, digest/push, the Dockerfile-missing skip logic) is `SUBTASK_image_job`'s scope; the rust-toolchain/`@1.97` + `with: toolchain` redundancy and cache-key reproducibility are `SUBTASK_workflow_correctness`'s scope. This spoke judged only the *security* of permissions, secrets, and action provenance.

## Spoke roll-up

**block: 0 · major: 0 · minor: 1 · nit: 1**

No finding from this spoke forces `REQUEST-CHANGES`. The workflow's security design (least-privilege top-level default, correctly confined per-job write scope, `GITHUB_TOKEN`-only secrets, PR-safe gating of the write path, no injection sinks) is sound; the two recorded items are deferred supply-chain *hardening* exposures owned by issue #24, not defects that would fire on `main`.
