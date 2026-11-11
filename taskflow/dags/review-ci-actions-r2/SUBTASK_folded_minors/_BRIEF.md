# Task: Review folded #8-review minors — scope & correctness (PR #21, concern 5)

## Task Specification

**Slug**: SUBTASK_folded_minors
**Task Kind**: standard
**Status**: Pending

### Objective

Verify the non-CI changes folded into PR #21: the **~79 rustdoc intra-doc-link fixes** across the
workspace crates and the **chirp-server README validation-error correction (422→400 /
`VALIDATION_ERROR`)**. Confirm the rustdoc changes are genuinely doc/comment-only (no runtime
behavior change), confirm the README correction is accurate, and judge whether folding these into a
CI PR is acceptable scope. Emit findings in the frozen schema. Reviewer role: read-only.

### Context

Part of the review DAG for PR #21 (see `../_GLOBAL.md`). These minors touch `crates/ferric*`,
`crates/chirp-server`, `crates/chirp-frontend` source files (doc comments only, per the PR's claim)
plus the chirp-server README. The machine gate already folded PASS (clippy/test/doc green), which is
corroborating evidence but not a substitute for confirming doc-only scope from the diff.

**Dependencies**: none. **Dependents**: `SUBTASK_synthesis`.

## What to evaluate (judge each block/major/minor/nit)

**Concern 5 — folded #8-review minors, scope & correctness:**
- **Doc-only verification**: inspect the ~79 rustdoc changes in the diff. Are they confined to doc
  comments (`///`, `//!`) / intra-doc links, changing **no** runtime code (no signatures, control
  flow, literals, attributes with behavior, `cfg`, macro bodies)? Sample broadly across the affected
  crates; call out any hunk that is not doc-only.
- **README correction accuracy**: is changing the documented validation-error status from 422 to 400
  (with `VALIDATION_ERROR`) actually correct against chirp-server's real behavior? Check the server's
  actual validation-error response path/status if reachable from the diff or source, and whether the
  README now matches the code.
- **Scope judgment**: is folding ~79 doc fixes + a README correction into a CI-infrastructure PR
  acceptable, or should it be flagged (e.g. as a reviewability / mixed-concern `minor`/`major`)? Make
  and justify the call.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Shared facts & evidence-access | `../_GLOBAL.md` | Repo, PR, head SHA, `gh` access patterns |
| Findings schema (frozen) | `../contracts/findings_schema.md` | Record shape you MUST emit in |
| Ownership (id prefix `DOC-`) | `../contracts/_MANIFEST.yaml` | Output path + finding-id prefix |
| PR diff (non-CI files) | `gh pr diff 21 --repo Nousix-LLC/nswe-demo` | The rustdoc + README changes to inspect |
| chirp-server source/README at head | `gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=c8123376 ...` | Confirm README 400/`VALIDATION_ERROR` matches real behavior |

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `findings.md` (this workspace), per `../contracts/findings_schema.md`, ids `DOC-n`, header stating head `c8123376`. |

## Success Criteria

- [ ] The rustdoc diff hunks inspected across the affected crates; doc-only claim confirmed or any non-doc hunk flagged with `location`.
- [ ] README 422→400 / `VALIDATION_ERROR` correction checked against actual chirp-server behavior; accurate/inaccurate stated with evidence.
- [ ] Scope-folding judgment made and justified.
- [ ] Findings conform to schema; block/major carry `required_change`; roll-up + head reviewed stated ("no findings" explicit if clean).

## Suggested Methodology Files

Parent's Domain-Mapping reading: **"Code review"** (primary: Code Review; supporting: Core, Testing),
plus documentation methodology.

- `code-review/CodeReview_Checklist_Methodology.md` — systematic review; verifying claimed-scope vs actual-diff.
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — severity/scope-flag calibration.
- `operations/BestPractices_Documentation_Methodology.md` — doc/README accuracy standards.
- `core/BestPractices_Coding_Standards_Methodology.md` — recognizing what counts as behavior-affecting vs doc-only.

Load via `engine_load_methodology { name: "code-review" }`, `{ name: "operations" }`,
`{ name: "core" }`. **Suggestions, not an exclusive list.**

## Inherited Constraints

- **Read-only review (P1): push nothing, change nothing.** `gh` read/GET only.
- **Rely on machine-PASS** as corroboration; but still confirm doc-only scope from the actual diff rather than assuming it from the green gate.
- **Emit in the frozen findings schema**; request an additive amendment if inadequate.

## Out-of-Scope Methodologies

- `decomposition/` and `synthesis/` bundles (decomposer/gate-side).
- CI workflow / security / image-job concerns belong to the other three spokes.
