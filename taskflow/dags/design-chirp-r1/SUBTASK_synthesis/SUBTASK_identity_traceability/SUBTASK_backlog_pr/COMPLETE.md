# COMPLETE — SUBTASK_backlog_pr

**Task:** Build the `REQ/BAR → (epic, issue_numbers)` map from the backlog trace and the design-PR
record, and assert `ISSUE_TRACES`, `GAP_HAS_ISSUE` (design/backlog half), `GITHUB_HYGIENE`, and
`ONE_OWNER_PER_FILE` with recorded evidence.

**Evaluation:** Atomic. One input-complete verification-synthesis responsibility over a single bounded
source region (the delivery backlog + the PR #122 record). Every size trigger cleared and both concern
tests passed on the actual work; the four "different kinds" of check are verdict types in one report over
shared inputs, not separable analyses (children would re-read the same two documents, not partition
distinct sources). Ran ≈12 tool calls; no falsification signal fired.

## What was produced

`outputs/backlog-pr.md` — self-contained, composes against the inherited contracts without redefining the
id scheme, matrix columns, or identities. Contains:

1. **`REQ/BAR → (epic, issue_numbers)` map** (ids verbatim) — the mechanical inversion of the backlog §4
   trace map: 276 distinct `REQ-*` and 237 distinct `BAR-*`, each with its epic(s) and issue number(s),
   keyed for the synthesis join (A.2 by `req_id`, A.3 by `bar_id`). Derived with a documented,
   reproducible parser (area prefix carried across slash groups); the parser was scratch and removed.
2. **Four identity verdicts**, each with clause-by-clause evidence and, where applicable, a recorded
   residual/fixability (no bare passes, no silent plugs):
   - `ISSUE_TRACES` — **PASS** for the design-requirement issue set (all 60 issues under exactly one
     epic; each epic one landable goal with stated deps; every requirement-bearing issue cites ≥1 REQ,
     56/60). Scoped exception surfaced: the 4 non-gating folded follow-ups #23/#24/#25/#27 cite no
     REQ/BAR (trivially fixable, non-gating).
   - `GAP_HAS_ISSUE` (design/backlog half) — **PASS**: both gaps the backlog records are filed (#123 under
     #34; #124 under #90). Live-measurement half explicitly deferred to the sibling.
   - `GITHUB_HYGIENE` — **PASS** on the recorded artifacts + owning-tasks' attestations; live posted-text
     re-scan noted as out of the completed-inputs scope.
   - `ONE_OWNER_PER_FILE` — **PASS**: 7 `design/*.md`, one owner each, PR #122 file map and
     `design_artifact_map.yaml` agree; one produced-at sub-path detail reconciled (owner unchanged).

## Success criteria

- [x] Map covers the backlog trace entries, ids verbatim.
- [x] All four identities carry a PASS/FAIL verdict with recorded evidence; none bare, none silently plugged.
- [x] `GAP_HAS_ISSUE` scoped to the design/backlog half; live-measurement half explicitly deferred.
- [x] The one shortfall (4 folded non-gating follow-ups without a REQ/BAR trace) is surfaced with
      specifics and fixability, not hidden. No other untraced issue, dependency-less epic, hygiene leak,
      or unowned/double-owned `design/*.md` found.

## Constraints honored

- Owned only the `epic`/`issue_numbers` map and the four named identities; did not build design rows, the
  `REQ → bar_ids` map, or other identities.
- Read-only over completed inputs; reported findings, edited nothing.
- Output carries no host/system/filesystem/run detail and no attribution trailer. (Owning-task slugs
  appear only as the design contracts' ownership vocabulary required by `ONE_OWNER_PER_FILE`.)

## Limitation

The `design` methodology loader was unavailable (`agent_domain_unset`); proceeded on the
principal-product-designer posture and the relayed Release Definition guidance by prose, as every sibling
gate did. Recorded in the deliverable.

## For the synthesis child (`SUBTASK_assemble`)

- Join `epic`/`issue_numbers` onto each matrix row by `req_id` from A.2; A.3 carries the same relation by
  `bar_id` for the fold.
- Decide whether the 4 folded non-gating follow-ups (#23/#24/#25/#27) are in `ISSUE_TRACES`' scope; the
  shortfall is isolated and non-gating.
- Complete `GAP_HAS_ISSUE` once the live-measurement gaps are known.
