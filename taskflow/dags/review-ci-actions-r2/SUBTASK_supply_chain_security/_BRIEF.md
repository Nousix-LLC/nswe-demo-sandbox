# Task: Review workflow security / least-privilege / supply-chain (PR #21, concern 3)

## Task Specification

**Slug**: SUBTASK_supply_chain_security
**Task Kind**: standard
**Status**: Pending

### Objective

Review the security posture of `.github/workflows/ci.yml` at PR head `c8123376` — least-privilege
permissions, secret handling, and third-party-action supply-chain exposure — emitting findings in
the frozen findings schema. Reviewer role: read-only, push nothing.

### Context

Part of the review DAG for PR #21 (see `../_GLOBAL.md`). **Dependencies**: none. **Dependents**:
`SUBTASK_synthesis`.

## What to evaluate (judge each block/major/minor/nit)

**Concern 3 — workflow security / least-privilege / supply-chain:**
- Top-level `permissions: contents: read` — is the workflow least-privilege at the top level?
- The `image` job's `packages: write` scoping — is the elevated permission confined to only the job
  that needs it (GHCR push), not granted workflow-wide?
- Secrets: is the workflow `GITHUB_TOKEN`-only (no long-lived PATs / external secrets)?
- Third-party actions pinned **by tag vs by commit SHA** — enumerate every external action used
  (`dtolnay/rust-toolchain@...`, `Swatinem/rust-cache@v2`, `actions/checkout@...`, any docker/login
  or build-push actions, etc.) and assess the supply-chain exposure of tag-pinning vs SHA-pinning.
  **Note:** this engagement tracks supply-chain hardening as issue **#24** — calibrate severity
  accordingly (tag-pinning that is already tracked as a separate hardening issue is typically a
  `minor`/`major` judgment, not necessarily a `block`; make and justify the call).

Evaluate the *security* of the `image` job's permissions and auth here; the *functional* correctness
of that job against the Dockerfile is `SUBTASK_image_job`'s scope — cross-reference, don't duplicate.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Shared facts & evidence-access | `../_GLOBAL.md` | Repo, PR, head SHA, `gh` access patterns |
| Findings schema (frozen) | `../contracts/findings_schema.md` | Record shape you MUST emit in |
| Ownership (id prefix `SEC-`) | `../contracts/_MANIFEST.yaml` | Output path + finding-id prefix |
| `ci.yml` at head | `gh api repos/Nousix-LLC/nswe-demo/contents/.github/workflows/ci.yml?ref=c8123376 -q .content \| base64 -d` | The workflow under review |

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `findings.md` (this workspace), per `../contracts/findings_schema.md`, ids `SEC-n`, header stating head `c8123376`. |

## Success Criteria

- [ ] Permissions (top-level + per-job), secret handling, and every third-party action's pinning mode assessed, with the tag-vs-SHA supply-chain exposure explicitly judged and severity justified relative to issue #24.
- [ ] Findings conform to the schema; block/major carry `required_change`.
- [ ] `findings.md` states the head reviewed and a roll-up ("no findings" stated explicitly if clean).

## Suggested Methodology Files

Parent's Domain-Mapping reading: **"Security review"** (primary: Security; supporting: Code Review),
with CI-supply-chain cross-refs.

- `security/Security_Dependency_Security_Methodology.md` — third-party dependency / action supply-chain risk; pinning discipline.
- `security/Security_Secure_Coding_Methodology.md` — least-privilege and secret-handling principles applied to the workflow.
- `code-review/CodeReview_Checklist_Methodology.md` — systematic security-review coverage.
- `open-source/OSS_SBOM_Supply_Chain_Methodology.md` — tag-vs-SHA action pinning and supply-chain hardening framing (relevant to issue #24).
- `fast-delivery/FastDelivery_CICD_Release_And_Security_Automation_Methodology.md` — least-privilege `GITHUB_TOKEN`/`permissions` scoping and required-check security wiring (consult if useful).

Load via `engine_load_methodology { name: "security" }`, `{ name: "code-review" }`, and (if useful)
`{ name: "open-source" }` / `{ name: "fast-delivery" }`. **Suggestions, not an exclusive list** —
your judgment governs final load.

## Inherited Constraints

- **Read-only review (P1): push nothing, change nothing.** `gh` read/GET only.
- **Emit in the frozen findings schema**; request an additive amendment if inadequate.
- Supply-chain tag-pinning is tracked separately as issue #24 — factor that into severity (don't reflexively `block` what is already an owned hardening track), but still record the exposure.

## Out-of-Scope Methodologies

- `decomposition/` and `synthesis/` bundles (decomposer/gate-side).
- Functional workflow correctness/caching is `SUBTASK_workflow_correctness`; image-job build/GHCR-push functional correctness is `SUBTASK_image_job`.
