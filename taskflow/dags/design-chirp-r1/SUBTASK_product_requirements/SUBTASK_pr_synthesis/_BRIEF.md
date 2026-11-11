# Task: Synthesis gate & fold — assemble chirp product-requirements.md

## Task Specification

**Slug**: SUBTASK_pr_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective

Assemble the three concern-fragments into the single, coherent `product-requirements.md` with all five required
sections; **verify** the subtree's contract identities with recorded evidence; and **fold** the result into the
suspended parent task — remediating any fixable gap by decomposing, never by a silent plug or a quiet pass.

### Context

This is the verification gate for the product-requirements subtree (see `../_GLOBAL.md`). It is not a prose
summary: it reconciles the siblings' combined output against `../contracts/` (and the inherited
`../../contracts/`) and asserts every identity. It writes this subtree's single deliverable and its fold record.

**Dependencies**: `SUBTASK_product_definition`, `SUBTASK_users_and_journeys`, `SUBTASK_requirements`
(read all three outputs).
**Dependents**: the parent task folds on this task's completion.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context; the identity list to assert |
| Subtree contract | `../contracts/_MANIFEST.yaml`, `../contracts/section_ownership_map.yaml` (read-only) | Section ownership, identities, the sole-REQ-PROD-minter rule |
| Parent contract | `../../contracts/` (read-only) | Inherited required-section list, id/traceability schema |
| Product definition | `../SUBTASK_product_definition/outputs/product-definition.md` | `product_definition_and_kind` + scope draft |
| Users & journeys | `../SUBTASK_users_and_journeys/outputs/users-and-journeys.md` | `users_personas` + `user_journeys` |
| Requirements | `../SUBTASK_requirements/outputs/requirements.md` | `requirements_and_acceptance_criteria` + `in_scope_out_of_scope` + the `REQ-PROD-*` register |

---

## Scope — the gate this task owns

- **Assemble**: compose the five required sections from their owning fragments (per
  `../contracts/section_ownership_map.yaml`) into one coherent `product-requirements.md`, resolving overlaps and
  ordering so the document reads as a single designer's work — not three stapled fragments.
- **Assert the identities, with recorded evidence** (from `../contracts/_MANIFEST.yaml`): `SECTION_COVERAGE`,
  `REQ_SINGLE_OWNER`, `REQ_WELL_FORMED`, `JOURNEY_TO_REQ`, `KIND_IMPLICATIONS`, `SCOPE_RECORDED`, `HYGIENE`.
  Record, in `SYNTHESIS.md`, how each identity was checked and the evidence that it holds (e.g. the
  journey→`REQ-PROD-*` trace, the section→fragment map, the id-ownership scan).
- **Remediate, do not plug**: if an identity fails in a way that is fixable (a missing required section, an
  untestable or unflagged requirement, a journey with no covering requirement, a hygiene breach), remediate by
  **decomposing a remediation subtree** that fixes it; never silently fill a gap or pass it over. The method for
  how to run a synthesis gate / remediation decomposition is engineering practice in the `software` domain's
  `synthesis` / `decomposition` bundles — reach for it by prose.
- **Fold**: author the fold record `SYNTHESIS.md` at the fold location (the suspended parent task's directory,
  i.e. this subtree root `..`) and author the assembled deliverable at the parent's declared output path
  (`../outputs/product-requirements.md`), then fold the parent `SUSPENDED → COMPLETED`.

### Methodology

Load on demand per the `design` loader's Domain Mapping: **Release Definition**
(CompletenessAndGapReview, ReleaseBar lenses for coverage checking); draw the synthesis-gate method from the
`software` domain's `synthesis` bundle by prose. Load full bundle content yourself for the work you execute.

---

## Output Specification

- `../outputs/product-requirements.md` — the assembled subtree deliverable (the parent task's declared output),
  carrying all five required sections. Repository-ready: no host/system/taskflow detail, no attribution trailers.
- `../SYNTHESIS.md` — the fold record at the fold location (this subtree root): the identity assertions with
  evidence, the section→fragment map, and the fold outcome. Reported as `artifact_path` on the terminal call and
  consumed by the fold.

## Success Criteria

- [ ] `product-requirements.md` carries all five required sections, each sourced from its owning fragment, reading coherently.
- [ ] Every subtree identity is asserted with recorded evidence in `SYNTHESIS.md`; none silently plugged.
- [ ] Any fixable gap is remediated by decomposition, not a quiet pass.
- [ ] The parent task is folded `SUSPENDED → COMPLETED` on this task's completion.
- [ ] Repository-ready hygiene holds across the deliverable.

## Constraints

- Design & requirements only — defer every implementation "how" to later code DAGs.
- Treat every `contracts/` directory as read-only. No silent plugs — a failing identity is remediated or reported.
