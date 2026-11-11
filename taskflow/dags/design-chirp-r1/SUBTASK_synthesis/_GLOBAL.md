# _GLOBAL.md — SUBTASK_synthesis (verification-gate + fold subtree hub)

## Project Context

**Status**: Active

### Objective

This is the decomposition of `design-chirp-r1`'s **verification gate and fold** (`SUBTASK_synthesis`). The gate's
one job splits into two heavy, independent analyses plus the fold:

1. **Assert the eight contract identities** in `../contracts/_MANIFEST.yaml` with recorded evidence, and assemble
   the whole-DAG **traceability matrix** (`REQ-* ↔ BAR-* ↔ epic/issue`).
2. **Measure the live product** deployed at commit `c805525` against **every** `BAR-*` in the release bar, as a
   user and by inspecting the repository, judging each `met | partial | missing | not_applicable` with recorded
   observations.
3. **Fold**: author the DAG's root verdict `SYNTHESIS.md` (the bar; the filed issues indexed by epic; the measured
   standing with every gap mapped to its covering epic/issue) and resolve the subtree so the DAG root
   `design-chirp-r1` reaches COMPLETED with that verdict as its fold seam. Remediate any **fixable** design/backlog
   gap by decomposing a remediation subtree — never by a silent plug or a quiet pass.

This gate verifies and measures; it writes **no product code** and it measures the live product **read-only**.

### Scope

**In Scope:**
- The two analytical concerns (identity-assertion + traceability; live-product measurement) each carried to
  recorded evidence/observations.
- The fold: the root verdict `SYNTHESIS.md`, and resolving the suspended ancestors so the DAG root completes.
- Remediation of fixable gaps by a decomposed remediation subtree (authored by the fold node, which sees both
  analyses).

**Out of Scope:**
- Writing product code, implementing any ticket, or editing the design docs / backlog (those tasks are COMPLETED;
  the gate reads them, it does not rewrite them).
- Any repo/cluster/namespace other than `Nousix-LLC/nswe-demo` (+ read-only use of the live deployment).

### Success Criteria

- [ ] Every one of the eight `../contracts/_MANIFEST.yaml` identities is asserted with recorded evidence; none
      silently plugged.
- [ ] The live product at `c805525` is measured against **every** `BAR-*` (met/partial/missing/not_applicable) with
      observations, not assumptions.
- [ ] The traceability matrix carries every release-gating `REQ-*` with its `bar_ids`, covering `epic`/issue, design
      doc reference, and joined `live_status`.
- [ ] Root `SYNTHESIS.md` states the bar, indexes issues by epic, and maps every gap to a covering epic/issue.
- [ ] Any fixable gap is remediated by a decomposed remediation subtree, not by failing the DAG or papering over it.
- [ ] `SYNTHESIS.md` (and anything posted to GitHub) carries no host/system/taskflow detail and no attribution
      trailer — repository identity only (`owner/repo`, commit SHA, repo-relative paths, `REQ-*`/`BAR-*`/`EPIC-*`/issue #).

---

## Constraints and Requirements

### Process Constraints
- **Read-only measurement.** Exercising the live product MUST NOT mutate it beyond the normal effect of a user's
  own actions on a throwaway test account, and MUST NOT touch any repo/cluster/namespace outside the project's own.
  No product code is written.
- **Completed inputs are immutable.** The sibling outputs (the five concern designs, the release bar, the design PR,
  the backlog) are COMPLETED and read-only here. A gate finding about them is reported and, if fixable, remediated
  by a **new** decomposed subtree — never by editing a completed task's output in place.
- **No silent plugs.** A failing identity or an uncovered gap is reported with evidence and remediated by
  decomposition, never reconciled silently.

### Hygiene (binding on the root `SYNTHESIS.md` and anything posted to GitHub)
No host or cluster address, no filesystem or taskflow path, no agent/DAG/run id, no `SYNTHESIS.md`/`SUSPENSION.md`
location, no attribution footer. Name things by repository identity only. The host/deployment facts needed to reach
the live product (per the project `CLAUDE.md`) are for running checks and MUST NOT appear in the verdict.

---

## Input Specifications

Paths are relative to each child's own workspace (`SUBTASK_synthesis/SUBTASK_<slug>/`). The sibling tasks these
read from are all COMPLETED; read their outputs directly (do not poll, do not re-verify completion).

| Source | Location (from a child) | Role |
|--------|--------------------------|------|
| This subtree hub | `../_GLOBAL.md` | Shared context (this file) |
| Inherited contract | `../../contracts/` | The eight identities, the id/traceability schema, the design-artifact map — READ-ONLY, not redefined |
| This subtree's sub-contract | `../contracts/_MANIFEST.yaml` | Column ownership + the matrix/measurement join seam + this gate's identities |
| Release bar | `../../SUBTASK_release_bar/outputs/release-bar.md` | The 278 `BAR-*` to assert testability of and to measure against |
| Backlog + trace map | `../../SUBTASK_delivery_backlog/outputs/backlog.md` | Epics/issues and their traces to verify |
| Design PR record | `../../SUBTASK_design_pr/outputs/design-pr.md` | PR #, branch, and the repo `design/` file map (the assembled design) |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | `REQ-PROD-*` + release_gating flags |
| Domain & application | `../../SUBTASK_domain_app_design/outputs/domain-application-design.md` | `REQ-DOM-*` |
| Experience | `../../SUBTASK_experience_design/outputs/experience-design.md` | `REQ-UX-*` |
| Identity, security & trust | `../../SUBTASK_identity_trust/outputs/identity-security.md` | `REQ-ID-*` |
| Operational readiness | `../../SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md` | `REQ-OPS-*` |
| Live deployment | ArgoCD app `chirp` @ `c805525` (reached per the project `CLAUDE.md` host notes) | Measure the product read-only (environment facts only; keep out of the verdict) |
| Repository @ `c805525` | cloned under `../../SUBTASK_design_pr/repo` (or a fresh clone) | Inspect code/config/manifests for `inspection` / `automated_test` criteria |

---

## Methodology Posture

The Phase-B `design` methodology loader is unavailable run-wide (`agent_domain_unset`; every sibling synthesis gate
hit the same and proceeded). Each child applies the **principal-product-designer persona** and the relayed
Release Definition guidance — **CompletenessAndGapReview** and **ReleaseBar** — plus, for the fold, the
software-domain **synthesis-gate** and **remediation-decomposition** practice reached by prose. Children do not
block on the loader; they record the limitation and proceed, as the siblings did.

---

## Task Structure

### Overview

```
SUBTASK_synthesis/
├── _GLOBAL.md                              (this hub)
├── contracts/
│   └── _MANIFEST.yaml                      (sub-contract: column ownership, join seam, gate identities — READ-ONLY)
├── SUBTASK_identity_traceability/_BRIEF.md (assert the 8 identities + build the traceability matrix skeleton)
├── SUBTASK_live_measurement/_BRIEF.md      (measure the live product vs every BAR-*; per-BAR live_status + observation)
└── SUBTASK_fold/_BRIEF.md                  (synthesis: join, verdict SYNTHESIS.md, remediation, fold to root)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_identity_traceability` | none | Assert each of the eight `../contracts/_MANIFEST.yaml` identities with recorded evidence; assemble the traceability-matrix skeleton (`req_id, release_gating, bar_ids, epic, issue_numbers, design_doc_ref` — every column except `live_status`) over the whole design + bar + backlog. | `outputs/identity-and-traceability.md` |
| `SUBTASK_live_measurement` | none | Exercise the live product at `c805525` (sign-up/in, posting, timeline/reading, replies, likes, follows, profiles, and the other journeys the bar names) and inspect the repository, judging **every** `BAR-*` `met \| partial \| missing \| not_applicable` with recorded observations. | `outputs/live-measurement.md` |
| `SUBTASK_fold` | `SUBTASK_identity_traceability`, `SUBTASK_live_measurement` | **Synthesis gate.** Join the measurement into the matrix (`live_status`), confirm GAP→issue coverage, author the DAG-root verdict `SYNTHESIS.md` (bar; issues by epic; measured standing with each gap→covering epic/issue), remediate any fixable gap by decomposing a remediation subtree, and fold so the DAG root `design-chirp-r1` reaches COMPLETED with that verdict as seam. | `design-chirp-r1/SYNTHESIS.md` (the DAG verdict/fold seam) |

### Dependency Graph

```
SUBTASK_identity_traceability ──┐
                                ├── SUBTASK_fold ── (fold → DAG root design-chirp-r1 COMPLETED)
SUBTASK_live_measurement      ──┘
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the sub-contract below. The three
children are parts of one gate; they share a real seam — one traceability matrix whose columns are split between the
two analytical children and joined by the fold, and the identities the fold asserts over their combined output. That
seam is frozen before any child runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (extends the inherited `../contracts/` additively; never overrides it)

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| design-chirp-r1 manifest | `../../contracts/_MANIFEST.yaml` | The eight identities to assert; one-owner-per-artifact |
| id & traceability schema | `../../contracts/id_and_traceability_schema.yaml` | `REQ-/BAR-/epic/issue` id scheme; traceability-matrix columns; `live_status` vocab; verification-method vocab |
| design-artifact map | `../../contracts/design_artifact_map.yaml` | Which design file carries which area's requirements |

This subtree MUST compose against these and MUST NOT redefine the id scheme, the matrix columns, or the identities.

### Structural Declarations, Ownership, Identities, Join Seam

Declared in `contracts/_MANIFEST.yaml`. In summary: `SUBTASK_identity_traceability` owns the identity verdicts and
the matrix skeleton (all columns except `live_status`, keyed by `req_id` with its `bar_ids`);
`SUBTASK_live_measurement` owns the per-`BAR-*` `live_status` + observation table (keyed by `bar_id`); `SUBTASK_fold`
owns the join (deriving each row's `live_status` from its `bar_ids`), the root verdict `SYNTHESIS.md`, and any
remediation subtree. No artifact has two owners.

### Thin-Seam Note

The seam is not thin: a shared, column-split matrix plus the gate identities are a real contract. Children MUST
compose against `contracts/` and MUST NOT redefine the inherited id scheme, matrix columns, or identities.
