# Task: Assert the contract identities and assemble the traceability matrix

## Task Specification
**Slug**: SUBTASK_identity_traceability
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Over the completed chirp design, release bar, and board backlog, **assert each of the eight contract identities in
`../../contracts/_MANIFEST.yaml` with recorded evidence**, and **assemble the whole-DAG traceability-matrix skeleton**
(every inherited column except `live_status`), so the fold has a verified, traceable base to measure the live
product against.

### Context
Part of `SUBTASK_synthesis` (the DAG's verification gate + fold; see `../_GLOBAL.md` and `../contracts/_MANIFEST.yaml`).
This is the **internal-consistency** half of the gate: does the combined design/bar/backlog actually compose and
trace? It does **not** touch the live product — that is the sibling `SUBTASK_live_measurement`. The two run in
parallel and are joined by `SUBTASK_fold`.

**Dependencies**: none within this subtree. The inputs below are COMPLETED sibling tasks; read their outputs directly.
**Dependents**: `SUBTASK_fold`.

### Distinct concerns in this task (name-level — evaluate your own scope and decompose if warranted)
These are genuinely distinct analyses over a large corpus (the release bar alone is ~690 lines / 278 `BAR-*`; the
five area designs total several hundred `REQ-*`, with `experience-design.md` alone in the thousands of lines). Judge
your own atomic-vs-decompose evaluation against them honestly:
- **The eight identity assertions** — `ONE_OWNER_PER_FILE`, `CONCERN_COVERAGE`, `BAR_COVERS_GATING_REQS`,
  `BAR_TESTABLE`, `ISSUE_TRACES`, `GAP_HAS_ISSUE` (the design/backlog half — every backlog-claimed gap has an issue;
  the live-measurement half is the sibling's), `SURFACE_COVERAGE`, `GITHUB_HYGIENE`. Each needs its own evidence
  (a mechanical check, a set-logic coverage computation, or an inspection), not a bare "pass".
- **The traceability-matrix skeleton** — one row per `REQ-*`, carrying `release_gating`, its `bar_ids`, its covering
  `epic` and `issue_numbers`, and its `design_doc_ref`, across all five areas and the whole backlog.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints |
| Inherited contract | `../../contracts/` | The eight identities; the id/traceability schema (matrix columns, verification-method vocab); the design-artifact map — READ-ONLY |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your owned columns (skeleton) and the join seam |
| Release bar | `../../SUBTASK_release_bar/outputs/release-bar.md` | `BAR-*` ↔ `REQ-*`, verification methods, stages |
| Backlog + trace map | `../../SUBTASK_delivery_backlog/outputs/backlog.md` | Issues/epics and their traces |
| Design PR record | `../../SUBTASK_design_pr/outputs/design-pr.md` | PR #, branch, repo `design/` file map (for `ONE_OWNER_PER_FILE`, `GITHUB_HYGIENE`) |
| Five area designs | `../../SUBTASK_product_requirements/outputs/product-requirements.md`, `../../SUBTASK_domain_app_design/outputs/domain-application-design.md`, `../../SUBTASK_experience_design/outputs/experience-design.md`, `../../SUBTASK_identity_trust/outputs/identity-security.md`, `../../SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md` | `REQ-*` with `release_gating` flags; concern coverage; surface coverage |

### Methodology
Apply the principal-product-designer persona and the relayed **Release Definition** guidance
(**CompletenessAndGapReview**). The `design` methodology loader is unavailable run-wide (`agent_domain_unset`);
record the limitation and proceed, as the siblings did. Evidence over assertion: an identity verdict names what was
checked and what was found, so a cold reviewer could re-run it.

### Output
- `outputs/identity-and-traceability.md` — the eight identity verdicts (each `PASS`/`FAIL` with recorded evidence and,
  on `FAIL`, what is missing and whether it is fixable), followed by the traceability-matrix skeleton (one row per
  `REQ-*`: `req_id`, `release_gating`, `bar_ids`, `epic`, `issue_numbers`, `design_doc_ref`; `live_status` left for
  the fold to join). Keyed and formatted so the fold can join the sibling's per-`BAR-*` `live_status` mechanically.

### Success criteria
- [ ] All eight identities carry a verdict with recorded evidence; none asserted bare or silently plugged.
- [ ] The matrix skeleton covers every release-gating `REQ-*` with `bar_ids` (≥1), covering `epic`/issue, and a
      `design_doc_ref`; any gating `REQ-*` lacking a `BAR-*` or an issue is surfaced as a `FAIL`/gap, not hidden.
- [ ] The matrix uses the inherited column names and `BAR-*`/`REQ-*`/`EPIC-*`/issue ids verbatim (no renamed scheme).
- [ ] Output is self-contained and composes against `../contracts/` without redefining it.

### Constraints
- Internal consistency only — do **not** exercise the live product (that is `SUBTASK_live_measurement`).
- Do not edit any completed sibling output; report findings, do not rewrite the design or backlog.
- Nothing you write that could reach GitHub carries host/system/taskflow detail or an attribution trailer.
