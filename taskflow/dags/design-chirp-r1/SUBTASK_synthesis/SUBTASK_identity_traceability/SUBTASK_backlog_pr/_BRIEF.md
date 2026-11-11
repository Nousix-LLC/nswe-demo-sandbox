# Task: Map REQ/BAR to epics and issues, and assert ISSUE_TRACES, GAP_HAS_ISSUE, GITHUB_HYGIENE, ONE_OWNER_PER_FILE

## Task Specification
**Slug**: SUBTASK_backlog_pr
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
From the delivery backlog and the design-PR record, produce the matrix's **`REQ/BAR → (epic, issue_numbers)`** map,
and assert the four identities that are grounded in the backlog and the GitHub-posted artifacts:
`ISSUE_TRACES`, `GAP_HAS_ISSUE` (design/backlog half), `GITHUB_HYGIENE`, and `ONE_OWNER_PER_FILE` — each with
recorded evidence.

### Context
Part of `SUBTASK_identity_traceability` (see `../_GLOBAL.md`). This spoke owns the matrix's `epic` and
`issue_numbers` columns (as the `REQ/BAR → (epic, issue_numbers)` map) and four of the eight identities. It does not
build design rows or the `REQ → bar_ids` map (other spokes own those).

These are several distinct checks over the backlog/PR corpus (one data-map build plus four identity assertions of
different kinds — traceability, gap-coverage, text-hygiene, and file-ownership). Evaluate your own
atomic-vs-decompose decision honestly against that; if the checks genuinely need separating, decompose.

**Dependencies**: none. **Dependents**: `SUBTASK_assemble`.

### Inputs
| Input | Source (from this workspace) | Purpose |
|-------|------------------------------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints |
| Subtree sub-contract | `../contracts/_MANIFEST.yaml` | `epic`/`issue_numbers` ownership + the four identity assignments — READ-ONLY |
| Inherited schema | `../../../contracts/id_and_traceability_schema.yaml` | `epic`/`issue` rules; the `each_issue_has` fields; matrix columns |
| DAG-root identities | `../../../contracts/_MANIFEST.yaml` | The exact `ISSUE_TRACES`, `GAP_HAS_ISSUE`, `GITHUB_HYGIENE`, `ONE_OWNER_PER_FILE` statements to assert |
| Design-artifact map | `../../../contracts/design_artifact_map.yaml` | The one-owner-per-`design/*.md` assignment for `ONE_OWNER_PER_FILE` |
| Backlog + trace map | `../../../SUBTASK_delivery_backlog/outputs/backlog.md` | Epics, issues, waves, and the `REQ/BAR` trace map |
| Design PR record | `../../../SUBTASK_design_pr/outputs/design-pr.md` | PR #122, the `design/` file-owner map, and the hygiene attestations |

### Output
- `outputs/backlog-pr.md` — containing:
  1. The `REQ/BAR → (epic, issue_numbers)` map derived from the backlog trace, for the synthesis join
     (ids verbatim; one or more issues/epics per traced `REQ-*`/`BAR-*`).
  2. Four identity verdicts, each `PASS`/`FAIL` with recorded evidence and, on `FAIL`, what is missing and whether
     it is fixable:
     - **`ISSUE_TRACES`** — every filed issue's acceptance criteria cite ≥1 `REQ-*` or `BAR-*`; every issue sits
       under exactly one epic; each epic is one coherent landable code goal with stated dependencies.
     - **`GAP_HAS_ISSUE`** (design/backlog half only) — every gap the backlog itself records or claims maps to ≥1
       filed issue/epic. (The live-measurement half of this identity belongs to the sibling `SUBTASK_live_measurement`
       and is out of scope here — note that explicitly.)
     - **`GITHUB_HYGIENE`** — the artifacts posted to GitHub (PR #122's body/commit per the PR record, and the filed
       epics/issues in the backlog) carry no host/system/taskflow detail and no attribution trailer.
     - **`ONE_OWNER_PER_FILE`** — each `design/*.md` has exactly one owning task (PR #122's file-owner map agrees
       with `design_artifact_map.yaml`; none unowned, none double-written).

### Success criteria
- [ ] The `REQ/BAR → (epic, issue_numbers)` map covers the backlog's trace entries and uses ids verbatim.
- [ ] All four identities carry a `PASS`/`FAIL` verdict with recorded evidence; none bare, none silently plugged.
- [ ] `GAP_HAS_ISSUE` is scoped to the design/backlog half, with the live-measurement half explicitly deferred.
- [ ] Any issue without a trace, any epic without stated dependencies, any hygiene leak, or any unowned/double-owned
      `design/*.md` is surfaced as a `FAIL` with specifics, not hidden.

### Constraints
- Own only the `epic`/`issue_numbers` map + the four named identities.
- Read-only over completed inputs; report findings, do not edit the backlog or PR.
- The `design` methodology loader is unavailable run-wide (`agent_domain_unset`); record the limitation and proceed.
- Output carries no host/system/taskflow detail and no attribution trailer.
