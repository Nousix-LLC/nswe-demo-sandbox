# Task: Synthesis gate — verify, measure the live product, and fold the design DAG

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Act as this design subtree's **verification gate and fold**: assert the contract identities with recorded
evidence, **measure the live product** at `c805525` against the release bar as a user would, and author the
root `SYNTHESIS.md` that states the bar, indexes the issues by epic, and gives a measured account of where the
live product stands. This establishes `design.standing` for the project (the first measurement).

### Context
Part of design-chirp-r1 (see `../_GLOBAL.md`, `../contracts/`). You are the gate, not a prose summary. You read
the whole subtree's combined output — the design PR, the backlog, and the release bar — and the live product,
and you verify the pieces actually composed. Where you find a **fixable** design/backlog gap, you **remediate
by decomposing a remediation subtree** (author its hub + child briefs and materialize children) rather than
failing the whole DAG or papering over it with a silent plug or a quiet pass. The method for *how* to run a
decomposition and a synthesis gate is engineering practice in the `software` domain's `decomposition` /
`synthesis` bundles — reach for it by prose.
**Dependencies**: `SUBTASK_design_pr`, `SUBTASK_delivery_backlog`, `SUBTASK_release_bar`, and all five concern
designs.

## Distinct concerns in this task (name-level — evaluate your own scope and decompose if warranted)
- **Identity assertion** — evaluate each contract identity in `../contracts/_MANIFEST.yaml` (ONE_OWNER_PER_FILE,
  CONCERN_COVERAGE, BAR_COVERS_GATING_REQS, BAR_TESTABLE, ISSUE_TRACES, GAP_HAS_ISSUE, SURFACE_COVERAGE,
  GITHUB_HYGIENE) and record the evidence for each pass/fail; assemble the `traceability_matrix` derived
  artifact.
- **Live-product measurement** — exercise the deployed product over its public endpoint as a user would
  (sign-up/in, posting, timeline/reading, following, and the other journeys the bar names), and judge each
  `BAR-*` as met / partial / missing / not_applicable, with what you observed.
- **The fold** — author `SYNTHESIS.md` (the bar; the issues indexed by epic; the measured standing with each
  gap mapped to its covering epic/issue) and fold the parent via the synthesis→resume path.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub + contract | `../_GLOBAL.md`, `../contracts/` | The identities to assert; shared constraints |
| Design PR record | `../SUBTASK_design_pr/outputs/design-pr.md` | The PR and design-doc repo paths |
| Backlog + trace map | `../SUBTASK_delivery_backlog/outputs/backlog.md` | Issues/epics and their traces to verify |
| Release bar | `../SUBTASK_release_bar/outputs/release-bar.md` | The `BAR-*` to measure against |
| All concern designs | `../SUBTASK_*/outputs/*.md` | The combined design to reconcile |
| Live deployment | ArgoCD app `chirp` @ `c805525` (read-only) | Measure the product (environment facts only; keep out of GitHub-posted content) |

## Methodology
Bundle IDs (Domain Mapping): **Release Definition** (CompletenessAndGapReview, ReleaseBar). Synthesis-gate and
remediation-decomposition method: reach to the `software` domain by prose.

## Output
- `SYNTHESIS.md` authored at **this subtree's root** (the parent `design-chirp-r1/` workspace — the fold
  location and the DAG's observation seam). It states the release bar, indexes the filed issues by epic, and
  gives the measured live-product standing (met/partial/missing/not_applicable per `BAR-*`, each gap mapped to
  its covering epic/issue). Then fold the parent: report completion with this `SYNTHESIS.md` as the artifact
  and resume the suspended parent against it.

## Success criteria
- [ ] Every contract identity is asserted with recorded evidence; no identity silently plugged.
- [ ] The live product is measured against every `BAR-*`, with observations, not assumptions.
- [ ] `SYNTHESIS.md` states the bar, indexes issues by epic, and maps every gap to a covering epic/issue.
- [ ] Any fixable gap is remediated by a decomposed remediation subtree, not by failing or papering over.
- [ ] `SYNTHESIS.md` and anything posted to GitHub carry no host/system/taskflow detail or attribution trailer.

## Constraints
- Measurement is read-only on the live product; no product code.
- This is the fold: the root `SYNTHESIS.md` is the DAG's verdict.
