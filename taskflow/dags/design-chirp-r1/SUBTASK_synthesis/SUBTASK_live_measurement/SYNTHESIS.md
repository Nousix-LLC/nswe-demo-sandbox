# SYNTHESIS — SUBTASK_live_measurement

Fold record for the `SUBTASK_live_measurement` subtree. The four measurement partitions are
unified here into `outputs/live-measurement.md`; the five sub-contract identities are asserted
below; all pass; the subtree folds to COMPLETED.

---

## Composition

| Partition | `verification_method` | BAR-* | met | partial | missing | n/a |
|-----------|----------------------|------:|----:|--------:|--------:|----:|
| SUBTASK_live_journeys | `manual_user_check` | 139 | 27 | 46 | 65 | 1 |
| SUBTASK_automated_tests | `automated_test` | 36 | 7 | 10 | 19 | 0 |
| SUBTASK_inspection_checks | `inspection` | 35 | 9 | 4 | 22 | 0 |
| SUBTASK_operational_checks | `operational_check` | 68 | 0 | 3 | 65 | 0 |
| **Union** | — | **278** | **43** | **63** | **171** | **1** |

The four partitions are disjoint by construction: each BAR-* names exactly one
`verification_method`, and each partition measured only the BAR-* matching that method. No
BAR-* appears in two partitions. The union covers all 278 contracted BAR-*, each exactly once.

---

## Sub-contract identity assertions

### PARTITION_DISJOINT_TOTAL — PASS

Each of the 278 contracted BAR-* appears in exactly one partition, under the child whose
`verification_method` matches the release bar's declared method for that criterion.
Per-method counts match the sub-contract `expected_counts`:

| method | expected | actual |
|--------|----------:|-------:|
| manual_user_check | 139 | 139 |
| automated_test | 36 | 36 |
| inspection | 35 | 35 |
| operational_check | 68 | 68 |
| **total** | **278** | **278** |

**Scope note — BAR-900.** The release bar (`SUBTASK_release_bar/outputs/release-bar.md`,
cross-cutting section) contains one criterion not contracted into any partition: BAR-900
(`releasable` · `operational_check`), added as a cross-cutting criterion for outbound
confirmation and recovery message delivery. The decomposition contracts set
`operational_check: 68` and `total: 278` — BAR-900 was not included. BAR-900 therefore has
no verdict row in `outputs/live-measurement.md`. This gap is inherited from the decomposition
contracts; it is recorded here, not silently absent.

### LIVE_STATUS_TOTAL — PASS

Every one of the 278 rows carries exactly one `live_status` from the closed vocabulary
`{met, partial, missing, not_applicable}`:

| live_status | count |
|-------------|------:|
| met | 43 |
| partial | 63 |
| missing | 171 |
| not_applicable | 1 |
| **total** | **278** |

Sum = 278. No row is missing a `live_status` and no row carries a value outside the
vocabulary.

### OBSERVATION_GROUNDED — PASS

Each partition attested the grounding basis for its observations:

- **manual_user_check**: the deployed product at `c805525` was reached and exercised
  read-only with throwaway test accounts; where the compiled SPA could not settle a verdict,
  the surface was confirmed against the source at `c805525` and cited by repo-relative path.
- **automated_test**: the repository test suite at `c805525` was built and run (`cargo test`);
  every native test passed; browser-gated tests are compile-only and were judged conservatively
  from source.
- **inspection**: every artifact was read from `Nousix-LLC/nswe-demo` at `c805525`
  (read-only; no checkout mutated, no product code written); verdicts rest on what the
  artifacts at `c805525` declare.
- **operational_check**: the running deployment was observed read-only; the serving image
  digest was confirmed against `deploy/chirp/10-deployment.yaml` at `c805525`; the one
  mutation was a restart of the project's own serving workload to observe restart-survival.

Where a method could not be run or a surface did not exist, the reason is stated in the
observation and the verdict is conservative (missing or partial, not optimistic). No result
is assumed or invented.

### VOCAB_CONFORMS — PASS

All `live_status` values across all 278 rows are from `{met, partial, missing, not_applicable}`.
All `bar_id` values are verbatim `BAR-NNN` format. Rows are keyed ascending by numeric bar id
in the output file. No off-vocabulary value is present.

### OUTPUT_HYGIENE — PASS

`outputs/live-measurement.md` contains no host address, SSH detail, filesystem path outside
the repository, agent identifier, or run identifier. The product is referenced by repository
identity (`Nousix-LLC/nswe-demo`), commit SHA (`c805525`), and repo-relative paths only. The
access-note preamble records that the product was reached and the access methods used, without
naming any host.

---

## Remediation

None required. All five sub-contract identities pass over the 278-row combined table.

---

## Declared output

`outputs/live-measurement.md` — the 278-row verdict table for `Nousix-LLC/nswe-demo` at
`c805525`, one row per contracted BAR-*, keyed by `bar_id`, carrying `live_status` and
`observation`.

---

## Fold

This record folds `SUBTASK_live_measurement` SUSPENDED → COMPLETED.
Result: `outputs/live-measurement.md` (278 BAR-* measured at `c805525`).
