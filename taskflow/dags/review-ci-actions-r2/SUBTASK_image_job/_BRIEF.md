# Task: Review the `image` job against the now-present Dockerfile (PR #21, concern 4)

## Task Specification

**Slug**: SUBTASK_image_job
**Task Kind**: standard
**Status**: Pending

### Objective

Evaluate how the `image` job in `.github/workflows/ci.yml` (at PR head `c8123376`) behaves once this
PR is on `main`, **given that #12's `./Dockerfile` has since merged to `main` (`61f924a`)** — build
context, image name/tag, GHCR auth via `GITHUB_TOKEN`, digest/push correctness, and whether the
"skip when Dockerfile missing" logic is now dead or could misfire. Emit findings in the frozen
schema. This is the **most important newly-relevant concern**; call out any `block`/`major`
explicitly. Reviewer role: read-only, push nothing.

### Context

Part of the review DAG for PR #21 (see `../_GLOBAL.md`). PR #21 was authored while #12's
`Dockerfile` was **absent**, so the `image` job was written to "skip cleanly when `Dockerfile` is
missing." That premise no longer holds: a real `./Dockerfile` now exists on `main`. The point of
this spoke is to re-judge the `image` job against present reality.

**Dependencies**: none. **Dependents**: `SUBTASK_synthesis`.

## What to evaluate (judge each block/major/minor/nit)

**Concern 4 — the `image` job now that #12 has landed:**
- **Gating**: the job is gated to `push` on `main`. Confirm the trigger/condition actually scopes it
  to `main` pushes (not PRs).
- **Skip-detection logic**: trace the "Dockerfile missing → skip" logic. With `./Dockerfile` now
  present on `main`, is that logic now **dead code**, or could it **misfire** (e.g. wrong path,
  wrong working directory, a check that still evaluates "missing" and skips a build that should
  run, or conversely runs a build that was meant to stay guarded)?
- **Build context & Dockerfile path**: does the job build the correct context and reference the
  real `./Dockerfile` path that now exists on `main`?
- **Image name/tag**: is the GHCR image name/tag correct and sensible (repo/owner, tag scheme,
  `latest`/sha tagging)?
- **GHCR auth**: is login to GHCR via `GITHUB_TOKEN` correct, with `packages: write` available to
  this job (the *security* scoping judgment is the security spoke's; here judge *functional*
  auth/push correctness)?
- **Digest / push correctness**: does the push actually publish, and is any digest/output handling
  correct?

Compare the `image` job (from `ci.yml` at head) against the actual `./Dockerfile` on `main`.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Shared facts & evidence-access | `../_GLOBAL.md` | Repo, PR, head SHA, base `61f924a`, `gh` access patterns |
| Findings schema (frozen) | `../contracts/findings_schema.md` | Record shape you MUST emit in |
| Ownership (id prefix `IMG-`) | `../contracts/_MANIFEST.yaml` | Output path + finding-id prefix |
| `ci.yml` at head | `gh api repos/Nousix-LLC/nswe-demo/contents/.github/workflows/ci.yml?ref=c8123376 -q .content \| base64 -d` | The `image` job under review |
| `./Dockerfile` on `main` | `gh api repos/Nousix-LLC/nswe-demo/contents/Dockerfile?ref=61f924a -q .content \| base64 -d` | The now-present Dockerfile the job will build |

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `findings.md` (this workspace), per `../contracts/findings_schema.md`, ids `IMG-n`, header stating head `c8123376` (and that the Dockerfile was read at `61f924a`). |

## Success Criteria

- [ ] `ci.yml` `image` job read at head `c8123376` AND `./Dockerfile` read on `main` (`61f924a`); the job is judged against the present Dockerfile, not the absent-Dockerfile premise.
- [ ] Skip-detection logic explicitly classified: dead / correct / misfire-risk, with evidence.
- [ ] Build context, image name/tag, GHCR `GITHUB_TOKEN` auth, and digest/push correctness each judged.
- [ ] Any `block`/`major` called out explicitly with a `required_change`; roll-up and head reviewed stated ("no findings" explicit if clean).

## Suggested Methodology Files

Parent's Domain-Mapping reading: **"Container deployment / production ops"** (primary:
Containerization; supporting: Operations, Security) and **"Code review"**.

- `containerization/Containerization_Docker_Build_Methodology.md` — correct build context, Dockerfile reference, tagging.
- `containerization/Containerization_Compose_Deploy_Methodology.md` — registry push / image publication correctness (GHCR).
- `operations/DevTools_CICD_Methodology.md` — job gating to `main` pushes; required-check interaction.
- `code-review/CodeReview_Checklist_Methodology.md` — systematic coverage so no sub-aspect (gating, path, tag, auth, push, dead-code) is skipped.

Load via `engine_load_methodology { name: "containerization" }`, `{ name: "operations" }`,
`{ name: "code-review" }`. **Suggestions, not an exclusive list.**

## Inherited Constraints

- **Read-only review (P1): push nothing, build nothing to a registry.** `gh` read/GET only; do not run the `image` job or push an image.
- **Emit in the frozen findings schema**; request an additive amendment if inadequate.
- This is flagged by the root brief as the most important newly-relevant concern — be thorough and explicit about any block/major.

## Out-of-Scope Methodologies

- `decomposition/` and `synthesis/` bundles (decomposer/gate-side).
- The *security scoping* of `packages: write` is `SUBTASK_supply_chain_security`; general workflow correctness/caching is `SUBTASK_workflow_correctness`.
