# COMPLETE — SUBTASK_matrix_ux

## What this task did

Extracted the traceability-matrix skeleton's **design-side columns** (`req_id`, `release_gating`,
`design_doc_ref`) for every `REQ-UX-*` defined in the experience design, so `SUBTASK_assemble` can join
this slice with the other design-side, bar, and backlog slices on `req_id`.

## Output

- `outputs/skeleton-ux.md` — one row per `REQ-UX-*`, keyed by `req_id`, carrying verbatim `release_gating`
  (true/false) and a `design_doc_ref` resolving to `design/experience-design.md` + the requirement's own
  `#### REQ-UX-NNN — <title>` section under `## Requirements and acceptance criteria`. The 13 non-gating
  requirements' stated reasons are preserved verbatim. Formatted as a table joinable on `req_id`.

## Result and verification

- **Requirements found: 119**, ids contiguous `REQ-UX-001`..`REQ-UX-119` (matches the source register's
  own stated range). Verified mechanically: 119 table rows, 119 distinct ids, no gap in `001..119`.
- **Gating split: 106 `true`, 13 `false`.** The `false` id set in the output matches the source's
  `release_gating: false` blocks exactly (mechanical diff: MATCH).
- **No `release_gating` defects**: every one of the 119 blocks carries a well-formed
  `- **release_gating**: true|false` field; none absent, none malformed, nothing guessed.
- `req_id` strings used verbatim; no renamed scheme; no row for an id the source does not define.
- Design-side columns only — no `bar_ids`, `epic`, or `issue_numbers` computed; no identity asserted.

## Anomaly surfaced for synthesis

The subtree hub `_GLOBAL.md` (and inherited counts) cite ~153 `REQ-UX-*`; the experience design as
delivered defines **119**. Reported in the output for `SUBTASK_assemble` to resolve against
`design/experience-design.md` as delivered, or to record the 153 figure as stale. Not reconciled here.

## Notes

- Inputs were COMPLETED and read-only; nothing was written back to the experience design.
- The `design` methodology loader was unavailable run-wide (`agent_domain_unset`); recorded in the output.
  The task is a verbatim extraction against a frozen input, so the limitation does not affect the values.
- Output carries repository identity only (repo-relative design path, `REQ-UX-*`/`REQ-PROD-*` ids); no
  host/system/taskflow detail and no attribution trailer.
