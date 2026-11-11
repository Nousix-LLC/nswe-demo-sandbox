# Task: Release-bar synthesis — assemble the bar, finalize staging, run the gap review, fold the parent

## Task Specification
**Slug**: SUBTASK_bar_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_bar_prod, SUBTASK_bar_dom, SUBTASK_bar_ux, SUBTASK_bar_id, SUBTASK_bar_ops
**Status**: Pending

### Objective
Integrate the five per-area `BAR-*` fragments into the single `release-bar.md` with its three required sections,
finalize the one cross-cutting **MVP-vs-releasable** staging line, run the **completeness & gap review** over
the whole design, assert this subtree's contract identities with recorded evidence (no silent plugs), and
**fold the parent** `SUBTASK_release_bar` so its declared output exists.

### Context
The verification gate and hub of the `SUBTASK_release_bar` subtree (see `../_GLOBAL.md` and `../contracts/`).
The five spokes each own their area's `BAR-*` range and propose a stage per criterion; you own the cross-cutting
concerns they cannot: the coherent MVP line across all areas, the whole-design gap review, and the assembled
deliverable. This is a verification gate — assert each identity with evidence; where you find a fixable gap
(e.g. a release-gating requirement no `BAR-*` covers, or an expected surface neither designed nor waived),
remediate it (mint a cross-cutting `BAR-900..999`, or record the out-of-scope judgment with a reason, or — if
the gap is larger than a gate fix — decompose a remediation subtree). Never plug a failing identity silently and
never pass a gate that does not hold.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, the identities to assert, methodology posture |
| Inherited contract | `../../contracts/` (read-only) | `BAR`/`REQ` schema, verification vocab, stages, the `release-bar.md` required sections |
| Subtree sub-contract | `../contracts/` (read-only) | BAR partition, fragment format, the proposed→final staging split, the identities |
| Five bar fragments | `../SUBTASK_bar_prod/outputs/bar-prod.md`, `../SUBTASK_bar_dom/outputs/bar-dom.md`, `../SUBTASK_bar_ux/outputs/bar-ux.md`, `../SUBTASK_bar_id/outputs/bar-id.md`, `../SUBTASK_bar_ops/outputs/bar-ops.md` | The per-area `BAR-*` + coverage notes to merge |
| The five area designs | `../../SUBTASK_product_requirements/outputs/product-requirements.md`, `../../SUBTASK_domain_app_design/outputs/domain-application-design.md`, `../../SUBTASK_experience_design/outputs/experience-design.md`, `../../SUBTASK_identity_trust/outputs/identity-security.md`, `../../SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md` | The whole design, for the gap review and to confirm gating coverage |

## The concerns you own
- **MVP-vs-releasable scoping** — the one honest line across all areas: what reaches a usable product early vs
  what the release requires on top. Reconcile the spokes' `proposed_stage` values into a coherent per-`BAR-*`
  final stage; hidden cuts are worse than stated ones.
- **The assembled release bar** — the consolidated `BAR-*` register at its final stage, each criterion testable
  (a verification method from the frozen vocabulary) and referencing the `REQ-*` it enforces, across the stages.
- **Completeness & gap review** — a deliberate Product-Surfaces sweep over the whole design for surfaces a
  product of this kind is expected to have — sign-up/in/recovery, account deletion, data export, onboarding,
  settings, notifications, admin/support, billing — recording an in-scope or out-of-scope judgment, with a
  reason, for each, so absence is a decision and not an oversight.

## Output
- `../outputs/release-bar.md` — the parent `SUBTASK_release_bar`'s declared output: the three sections from
  `../../contracts/design_artifact_map.yaml` (`mvp_vs_releasable_scoping`, `release_bar`,
  `completeness_and_gap_review`). Repository-ready (no host/system/taskflow detail, no attribution trailers).
- `../SYNTHESIS.md` — the fold record at the parent `SUBTASK_release_bar` workspace (the fold location): the
  per-identity verdicts with evidence, how the fragments were merged, staging decisions, gap-review findings and
  any remediation. Taskflow-internal (not repository content). After authoring it, resume the parent
  (`engine_resume_suspended`: target `SUBTASK_release_bar`, synthesized this task, seam `../SYNTHESIS.md`), which
  flips the parent SUSPENDED → COMPLETED with `outputs/release-bar.md` as its output.

## Success criteria
- [ ] All eight identities in `../contracts/_MANIFEST.yaml` asserted with recorded evidence; every one PASS (or a
      failure remediated, not plugged).
- [ ] Every release-gating `REQ-*` across all five areas is covered by ≥1 `BAR-*`; no `BAR-*` collision; ranges respected.
- [ ] Every `BAR-*` testable and references ≥1 `REQ-*`; every `BAR-*` has a final stage; scoping section agrees with the stages.
- [ ] The gap review records an in/out-of-scope judgment with a reason for each expected surface.
- [ ] `release-bar.md` has exactly the three required sections and is repository-ready; the parent is folded.

## Constraints
- A gate, not a prose summary — evidence-backed verdicts; no silent plugs; no passing a gate that does not hold.
- A bar, not an aspiration — each criterion checkable by someone who was not in the room.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary — MVP/release scoping, the bar, completeness & gap review); Release Readiness, Product
  Strategy, Identity and Trust, Product Surfaces (support — the gap-review lens). The synthesis-gate method is
  engineering practice reached by prose in the `software` domain's `synthesis` bundle; do not restate it here.
