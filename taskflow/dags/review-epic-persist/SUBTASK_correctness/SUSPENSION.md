# SUSPENSION — SUBTASK_correctness (NeedsDecompose)

## Why suspended

`SUBTASK_correctness` is too broad for one invocation. Its brief enumerates four distinct requirement areas —
acceptance criteria **#65**, **#66**, **#67**, and the **durable-persistence design requirement** (plus the
**#64** framing check) — and explicitly directs the agent to "treat them as the distinct areas they are when
you size your own work." Applied to the actual brief and the +11,851/−77 / 28-file target at commit
`09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`, the decomposition triggers fired:

- **Scope / Enumerated-concerns**: four distinct acceptance-criteria / requirement areas named by the brief —
  fires by enumeration alone.
- **Distinct Concerns Test**: each area traces a different "proved, not asserted" guarantee against different
  code paths; they could be judged by different specialists in parallel.
- **Token**: tracing the full diff against three issues and three design docs exceeds a comfortable single
  invocation.
- **Trigger Precedence**: the single declared `outputs/findings.md` and a low token guess do NOT override the
  fired scope trigger (N concerns into 1 file is still N concerns).

Verdict: `NeedsDecompose`. The reviewer instinct that one reader should hold the whole correctness picture
carries no weight at the evaluation point and was set aside per the kernel's mechanical rule.

## Children materialized (recursive-depth parent = SUBTASK_correctness)

| Child task id | Area | Depends on | Output |
|---|---|---|---|
| `SUBTASK_ac65_invariants` | #65 — invariants / derived counts / opaque-id monotonicity under concurrency | none | `SUBTASK_ac65_invariants/outputs/findings.md` |
| `SUBTASK_ac66_seam_migration` | #66 — seam capability set / single-writer / migration-runner versioning | none | `SUBTASK_ac66_seam_migration/outputs/findings.md` |
| `SUBTASK_ac67_retention_failclosed` | #67 — retention/capacity + fail-closed-on-non-durable-write | none | `SUBTASK_ac67_retention_failclosed/outputs/findings.md` |
| `SUBTASK_design_req_and_64` | durable-persistence design requirement + BAR-*/REQ- + #64 framing | none | `SUBTASK_design_req_and_64/outputs/findings.md` |
| `SUBTASK_correctness_synthesis` (Task Kind: synthesis, workspace `SUBTASK_synthesis/`) | fold the four areas into one concern findings doc + render sub-verdict | the four area spokes | `SUBTASK_correctness/outputs/findings.md`, `SUBTASK_correctness/SYNTHESIS.md` |

## Named state authored this invocation

- `SUBTASK_correctness/_GLOBAL.md` — subtree hub.
- `SUBTASK_correctness/contracts/_MANIFEST.yaml` — sub-contract (extends the root finding taxonomy: COR id
  partition + consolidation identities).
- One `_BRIEF.md` per child (five).

## Resumption condition

All child tasks reach terminal lifecycle state. The synthesis gate authors
`SUBTASK_correctness/outputs/findings.md` (the deliverable the review DAG consumes) and
`SUBTASK_correctness/SYNTHESIS.md` at the fold location, then folds this `SUBTASK_correctness` parent
SUSPENDED → COMPLETED.
