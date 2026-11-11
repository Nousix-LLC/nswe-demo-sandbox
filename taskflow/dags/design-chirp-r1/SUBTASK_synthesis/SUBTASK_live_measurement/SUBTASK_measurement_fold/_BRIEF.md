# Task: Union the four measurement partitions into live-measurement.md and fold the subtree

## Task Specification
**Slug**: SUBTASK_measurement_fold
**Task Kind**: synthesis
**Depends on**: SUBTASK_live_journeys, SUBTASK_automated_tests, SUBTASK_inspection_checks, SUBTASK_operational_checks
**Status**: Pending

### Objective
Union the four partition verdict tables into the one `bar_id`-keyed table that is this subtree's declared output,
`../outputs/live-measurement.md`; assert the partition is disjoint and total (278 `BAR-*`, each exactly once) and the
vocabulary conforms; compose the access-note preamble; and fold `SUBTASK_live_measurement` to COMPLETED with that
output as its result.

### Context
This is the synthesis/verification gate of `SUBTASK_live_measurement` (see `../_GLOBAL.md` and
`../contracts/_MANIFEST.yaml`). Its four sibling partitions are COMPLETED; read their outputs directly. The job is
mechanical, not a re-measurement: join the disjoint partitions and verify the contract's identities over the combined
table. Do not re-judge any `BAR-*` and do not silently fill a gap — a shortfall is reported, and if it is a genuine
partition defect (a `BAR-*` missing from every partition, a `BAR-*` in the wrong partition, a count mismatch, a
duplicate, an off-vocabulary value, or an ungrounded observation), it is remediated by restructuring, never by
inventing a verdict.

**Dependencies**: the four measurement partitions (above). **Dependents**: the gate's `SUBTASK_fold` consumes this
subtree's `outputs/live-measurement.md` via the join seam `live_status_key = bar_id`.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Sub-contract | `../contracts/_MANIFEST.yaml` | The verdict-row schema, the partition/ownership map, the `expected_counts`, and the identities to assert |
| id/traceability schema | `../../../contracts/id_and_traceability_schema.yaml` | `live_status` + `verification_method` vocab (authoritative) |
| Release bar | `../../../SUBTASK_release_bar/outputs/release-bar.md` | The authoritative list of all 278 `BAR-*` and each one's declared `verification_method` — the reference for the totality and partition-placement checks |
| Live-journeys verdicts | `../SUBTASK_live_journeys/outputs/live-journeys-measurement.md` | `manual_user_check` partition (139) |
| Automated-test verdicts | `../SUBTASK_automated_tests/outputs/automated-test-measurement.md` | `automated_test` partition (36) |
| Inspection verdicts | `../SUBTASK_inspection_checks/outputs/inspection-measurement.md` | `inspection` partition (35) |
| Operational verdicts | `../SUBTASK_operational_checks/outputs/operational-measurement.md` | `operational_check` partition (68) |

### Methodology
Apply the principal-product-designer persona. Assert the sub-contract's identities over the combined table:
`PARTITION_DISJOINT_TOTAL` (each `BAR-*` appears once, under the child matching its release-bar `verification_method`;
the union is exactly the 278 and per-method counts match `expected_counts`), `LIVE_STATUS_TOTAL`, `OBSERVATION_GROUNDED`,
`VOCAB_CONFORMS`, and `OUTPUT_HYGIENE`. Compose the preamble by merging the partitions' access notes into a single
record of *that* the live product was reached (or why not), by repository/commit identity only. If every identity
holds, write the output and fold. If an identity fails, report it with evidence and restructure to close it (e.g. an
`add_task` for a re-measurement of the specific defect) rather than completing over a known hole — no silent plug.

### Output
- `../outputs/live-measurement.md` — this subtree's declared output: a short access-note preamble (how the live
  product was reached, or why not, by repository/commit identity — no host detail), then one verdict row per `BAR-*`
  (all 278), `bar_id | live_status | observation`, keyed by `bar_id` so the gate's `SUBTASK_fold` joins it into the
  matrix mechanically.
- `../SYNTHESIS.md` — the fold record at this subtree's root (how the four partitions composed, the identity-assertion
  results, any remediation): both this task's terminal record and the record the fold consumes to resolve
  `SUBTASK_live_measurement` SUSPENDED → COMPLETED.

### Success criteria
- [ ] `../outputs/live-measurement.md` carries all 278 `BAR-*`, each exactly once, each with one inherited-vocab
      `live_status` and its grounded observation, keyed by `bar_id`.
- [ ] Every sub-contract identity is asserted with a recorded result; no failure silently plugged.
- [ ] Per-method counts match `expected_counts` (139 / 68 / 36 / 35 = 278); any mismatch is reported and remediated,
      not reconciled by hand.
- [ ] `../SYNTHESIS.md` records the composition and the assertions; the subtree folds to COMPLETED with
      `../outputs/live-measurement.md` as its result.
- [ ] Output and synthesis record carry repository identity only — no host/system/taskflow detail, no attribution
      trailer.

### Constraints
- Mechanical join and verification only; do not re-judge a `BAR-*` and do not write a verdict not grounded in a
  partition output.
- Reference the product only by repository identity, commit SHA, and repo-relative paths.
