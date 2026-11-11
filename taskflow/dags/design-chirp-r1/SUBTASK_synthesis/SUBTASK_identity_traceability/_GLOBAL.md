# _GLOBAL.md — SUBTASK_identity_traceability (identity-assertion + traceability-matrix subtree hub)

## Project Context

**Status**: Active

### Objective

This is the decomposition of the synthesis gate's **internal-consistency half** (`SUBTASK_identity_traceability`).
Its one job splits into two things that must be done over a large corpus and then joined:

1. **Assert each of the eight contract identities** in `../../contracts/_MANIFEST.yaml` with recorded evidence —
   a mechanical check, a set-logic coverage computation, or an inspection — never a bare "pass".
2. **Assemble the whole-DAG traceability-matrix skeleton** — one row per `REQ-*`, carrying every inherited column
   except `live_status` (`req_id`, `release_gating`, `bar_ids`, `epic`, `issue_numbers`, `design_doc_ref`), keyed so
   the fold can mechanically join the sibling's per-`BAR-*` `live_status`.

The corpus is why this is a subtree and not one invocation: the release bar is 688 lines / 279 `BAR-*`; the five
area designs total ~9,440 lines and ~525 `REQ-*` (`experience-design.md` alone is 4,671 lines / 153 `REQ-UX-*`);
the backlog + PR record add the epic/issue traces. No single invocation reads all of that and cross-references it
without degrading. The work is therefore **partitioned by source**: each spoke parses one region of the corpus
exactly once, emits its slice of the matrix and the identities groundable in that source, and the synthesis child
joins the slices into the matrix, asserts the one cross-source identity, and writes the gate's one deliverable.

This subtree verifies and traces only. It does **not** touch the live product (that is the parallel sibling
`SUBTASK_live_measurement`), it writes no product code, and it does not edit any completed design/bar/backlog output.

### Scope

**In Scope:**
- Extracting, per area, each `REQ-*`'s `req_id`, `release_gating`, and `design_doc_ref` (the matrix skeleton's
  design-side columns).
- Inverting the release bar to `REQ → bar_ids`, and the backlog to `REQ/BAR → (epic, issue_numbers)`.
- Asserting all eight inherited identities with recorded evidence, one asserting owner per identity.
- Joining the slices into the matrix skeleton and writing the gate deliverable
  `outputs/identity-and-traceability.md` at this subtree's root.

**Out of Scope:**
- Exercising or measuring the live product (the sibling `SUBTASK_live_measurement` owns `live_status`).
- Editing the design docs, release bar, backlog, or PR (COMPLETED and read-only here; a finding is reported, not
  fixed in place).
- Redefining the inherited id scheme, matrix columns, `live_status` vocab, or the identities (compose against
  `../../contracts/`; extend additively, never override).

### Success Criteria

- [ ] All eight identities (`ONE_OWNER_PER_FILE`, `CONCERN_COVERAGE`, `BAR_COVERS_GATING_REQS`, `BAR_TESTABLE`,
      `ISSUE_TRACES`, `GAP_HAS_ISSUE`, `SURFACE_COVERAGE`, `GITHUB_HYGIENE`) carry a `PASS`/`FAIL` verdict with
      recorded evidence; none asserted bare or silently plugged; on `FAIL`, what is missing and whether it is fixable.
- [ ] Every release-gating `REQ-*` appears as a matrix row with `bar_ids` (≥1), covering `epic`/`issue_numbers`, and
      a `design_doc_ref`; any gating `REQ-*` lacking a `BAR-*` or an issue is surfaced as a `FAIL`/gap, not hidden.
- [ ] The matrix uses the inherited column names and `REQ-*`/`BAR-*`/`EPIC-*`/issue ids verbatim (no renamed scheme).
- [ ] `outputs/identity-and-traceability.md` is self-contained, composes against `../../contracts/` and
      `../contracts/` without redefining them, and is keyed so the fold joins `live_status` by `bar_id` mechanically.
- [ ] Nothing written that could reach GitHub carries host/system/taskflow detail or an attribution trailer.

---

## Constraints and Requirements

### Process Constraints
- **Internal consistency only.** Do not exercise the live product; that is the parallel sibling.
- **Completed inputs are immutable.** The five area designs, the release bar, the backlog, and the PR record are
  COMPLETED and read-only; report findings, do not rewrite them.
- **No silent plugs.** A failing identity or an uncovered gating `REQ-*` is reported with evidence (and, if fixable,
  surfaced for the fold to remediate), never reconciled quietly or passed bare.
- **Evidence over assertion.** Every identity verdict names what was checked and what was found, so a cold reviewer
  could re-run it and reach the same verdict.

### Methodology Posture
The Phase-B `design` methodology loader is unavailable run-wide (`agent_domain_unset`); every sibling gate hit the
same and proceeded. Each child applies the **principal-product-designer persona** and the relayed Release Definition
guidance — **CompletenessAndGapReview** and **ReleaseBar** — reached by prose. Children record the limitation and
proceed; they do not block on the loader.

### Hygiene (binding on every output and anything that could reach GitHub)
No host or cluster address, no filesystem or taskflow path, no agent/DAG/run id, no workspace locations. Name things
by repository identity only (`owner/repo`, commit SHA, repo-relative design paths, `REQ-*`/`BAR-*`/`EPIC-*`/issue #).

---

## Input Specifications

Paths below are relative to each child's own workspace (`SUBTASK_identity_traceability/SUBTASK_<slug>/`). All sources
are COMPLETED; read their outputs directly (do not poll, do not re-verify completion).

| Source | Location (from a child) | Role |
|--------|--------------------------|------|
| This subtree hub | `../_GLOBAL.md` | Shared context (this file) |
| Inherited DAG-root contract | `../../../contracts/` | The eight identities; the id/traceability schema (matrix columns, `live_status` + verification-method vocab); the design-artifact map — READ-ONLY |
| Gate sub-contract | `../../contracts/_MANIFEST.yaml` | The gate's column ownership + join seam + gate identities — READ-ONLY |
| This subtree's sub-contract | `../contracts/_MANIFEST.yaml` | Column/identity ownership split across these children + the join seam — READ-ONLY |
| Release bar | `../../../SUBTASK_release_bar/outputs/release-bar.md` | `BAR-*` entries (`stage · method — statement _Enforces REQ-*_`) + the surfaces sweep |
| Backlog + trace map | `../../../SUBTASK_delivery_backlog/outputs/backlog.md` | Epics/issues, waves, and the `REQ/BAR` trace map |
| Design PR record | `../../../SUBTASK_design_pr/outputs/design-pr.md` | PR #122, branch, the `design/` file-owner map, hygiene attestations |
| Product requirements | `../../../SUBTASK_product_requirements/outputs/product-requirements.md` | `REQ-PROD-*` (42) + `release_gating` |
| Domain & application | `../../../SUBTASK_domain_app_design/outputs/domain-application-design.md` | `REQ-DOM-*` (111) + `release_gating` |
| Experience | `../../../SUBTASK_experience_design/outputs/experience-design.md` | `REQ-UX-*` (153) + `release_gating` |
| Identity, security & trust | `../../../SUBTASK_identity_trust/outputs/identity-security.md` | `REQ-ID-*` (110) + `release_gating` |
| Operational readiness | `../../../SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md` | `REQ-OPS-*` (109) + `release_gating` |

Each `REQ-<AREA>-NNN` entry in a design file carries `- **release_gating**: true|false`. The authoritative
`REQ → bar_ids` mapping is the inversion of each bar criterion's `_Enforces REQ-*_` line, not whatever a design file
says about itself. `design_doc_ref` is the repo-relative design path from `design_artifact_map.yaml` plus the REQ's
own section.

---

## Task Structure

### Overview

```
SUBTASK_identity_traceability/
├── _GLOBAL.md                           (this hub)
├── contracts/
│   └── _MANIFEST.yaml                   (sub-contract: column + identity ownership split, join seam — READ-ONLY)
├── SUBTASK_matrix_prod_dom/_BRIEF.md    (design-side skeleton rows: REQ-PROD-* + REQ-DOM-*)
├── SUBTASK_matrix_ux/_BRIEF.md          (design-side skeleton rows: REQ-UX-*)
├── SUBTASK_matrix_id_ops/_BRIEF.md      (design-side skeleton rows: REQ-ID-* + REQ-OPS-*)
├── SUBTASK_bar_mapping/_BRIEF.md        (REQ→bar_ids inversion + BAR_TESTABLE)
├── SUBTASK_backlog_pr/_BRIEF.md         (REQ/BAR→epic+issues + ISSUE_TRACES, GAP_HAS_ISSUE, GITHUB_HYGIENE, ONE_OWNER_PER_FILE)
├── SUBTASK_concern_surface/_BRIEF.md    (CONCERN_COVERAGE + SURFACE_COVERAGE over the design set)
└── SUBTASK_assemble/_BRIEF.md           (synthesis: join matrix, assert BAR_COVERS_GATING_REQS, collect 8 verdicts, write deliverable, fold)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_matrix_prod_dom` | none | Extract the matrix skeleton's design-side columns (`req_id`, `release_gating`, `design_doc_ref`) for every `REQ-PROD-*` and `REQ-DOM-*`. | `outputs/skeleton-prod-dom.md` |
| `SUBTASK_matrix_ux` | none | Extract the matrix skeleton's design-side columns for every `REQ-UX-*`. | `outputs/skeleton-ux.md` |
| `SUBTASK_matrix_id_ops` | none | Extract the matrix skeleton's design-side columns for every `REQ-ID-*` and `REQ-OPS-*`. | `outputs/skeleton-id-ops.md` |
| `SUBTASK_bar_mapping` | none | Parse the release bar into a per-`BAR-*` table (`stage`, `verification_method`, referenced `REQ-*`) and the inverted `REQ → bar_ids` map; assert `BAR_TESTABLE` with evidence. | `outputs/bar-mapping.md` |
| `SUBTASK_backlog_pr` | none | Build the `REQ/BAR → (epic, issue_numbers)` map from the backlog trace; assert `ISSUE_TRACES`, `GAP_HAS_ISSUE` (design/backlog half), `GITHUB_HYGIENE`, and `ONE_OWNER_PER_FILE` with evidence. | `outputs/backlog-pr.md` |
| `SUBTASK_concern_surface` | none | Inspect the design set for `CONCERN_COVERAGE` (the six brief concerns) and `SURFACE_COVERAGE` (the recurring account/operational surfaces); assert both with evidence. | `outputs/concern-surface.md` |
| `SUBTASK_assemble` | `SUBTASK_matrix_prod_dom`, `SUBTASK_matrix_ux`, `SUBTASK_matrix_id_ops`, `SUBTASK_bar_mapping`, `SUBTASK_backlog_pr`, `SUBTASK_concern_surface` | **Synthesis gate.** Join the skeleton columns into one matrix (every column except `live_status`); assert the cross-source identity `BAR_COVERS_GATING_REQS`; collect all eight identity verdicts with evidence (no silent plugs); write the deliverable and fold this subtree. | `../outputs/identity-and-traceability.md`, `../SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_matrix_prod_dom ──┐
SUBTASK_matrix_ux       ──┤
SUBTASK_matrix_id_ops   ──┤
SUBTASK_bar_mapping     ──├── SUBTASK_assemble ── (fold → SUBTASK_identity_traceability COMPLETED)
SUBTASK_backlog_pr      ──┤
SUBTASK_concern_surface ──┘
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the sub-contract in `contracts/`.
These seven children are parts of ONE task (assert-the-identities-and-trace); they share a real seam — one
traceability matrix whose columns are split across the sources and joined by the synthesis child, and the eight
identities, each assigned exactly one asserting owner so none is doubly asserted and none is a hole. That seam is
frozen in `contracts/_MANIFEST.yaml` before any child runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (extends `../contracts/` and `../../contracts/` additively; never overrides the
inherited id scheme, matrix columns, `live_status`/verification-method vocab, or the eight identities)

### Inherited Contracts

| Ancestor contract | Path (from here) | What it binds |
|---|---|---|
| DAG-root manifest | `../../contracts/_MANIFEST.yaml` | The eight identities; one-owner-per-file |
| id & traceability schema | `../../contracts/id_and_traceability_schema.yaml` | `REQ-/BAR-/epic/issue` id scheme; matrix columns; `live_status` + verification-method vocab |
| design-artifact map | `../../contracts/design_artifact_map.yaml` | Which design file carries which area's requirements |
| Gate sub-contract | `../contracts/_MANIFEST.yaml` | The gate's column ownership + join seam + gate identities |

This subtree composes against all of these and MUST NOT redefine the id scheme, matrix columns, vocab, or identities.

### Structural Declarations, Ownership, Identities

Declared in `contracts/_MANIFEST.yaml`. In summary: the three `SUBTASK_matrix_*` spokes own the design-side columns
(`req_id`, `release_gating`, `design_doc_ref`), partitioned by area with no overlap; `SUBTASK_bar_mapping` owns the
`REQ → bar_ids` map; `SUBTASK_backlog_pr` owns the `REQ/BAR → (epic, issue_numbers)` map; `SUBTASK_concern_surface`
and `SUBTASK_backlog_pr` and `SUBTASK_bar_mapping` each own a disjoint subset of the eight identities;
`SUBTASK_assemble` owns the joined matrix skeleton, the single cross-source identity `BAR_COVERS_GATING_REQS`, the
collection of all eight verdicts, and the gate deliverable. No artifact and no identity has two owners.

### Thin-Seam Note

The seam is not thin: a shared, column-split matrix plus eight singly-owned identity verdicts are a real contract.
Children MUST compose against `contracts/` and MUST NOT redefine the inherited id scheme, matrix columns, or identities.
