# SUSPENSION — SUBTASK_synthesis (NeedsDecompose)

## Decision
`decompose_evaluation = NeedsDecompose`. This is the DAG's verification gate + fold, resumed on a reconstructed
node with only its `_BRIEF.md` present (no prior terminal record — the gate had not yet run). Its one job splits
into two heavy, independent analyses plus the fold, so it decomposes rather than executing whole.

## Why decomposition (trigger application, recorded)
The brief enumerates three distinct concerns (identity assertion; live-product measurement; the fold), and the
first two are large independent analyses:
- **Scope-Based / enumerated-concerns — FIRES.** Two or more distinct analyses named in the brief.
- **Distinct Concerns Test — FIRES.** The internal-consistency audit (assert 8 identities + build the matrix over
  the whole corpus) and the empirical measurement (exercise the live product at `c805525` + inspect the repo, 278
  `BAR-*`) are different specialists and run in parallel — neither depends on the other.
- **Single-Responsibility Test — FIRES.** "Assert the identities **and** measure the live product **and** author the
  fold" is three kinds of change / three kinds of output.
- **Token-Based — strong candidate.** Faithful execution reads the full corpus (689-line bar + ~400 `REQ-*` across
  five deep area trees + the backlog) and inspects the repo, then measures 278 criteria — well beyond one invocation.
- **Output-Size — fires, weakest.** Two 278-row tables + the verdict exceed 400 lines; per Trigger Precedence this
  does not override the fired Scope signals, and the single declared `SYNTHESIS.md` does not make the task atomic.

Trigger Precedence resolves it: Scope / Distinct-Concerns / Single-Responsibility win. The only argument for `Atomic`
was "a gate is one coherent judgment best held whole" — disqualified by the standing contract and the Task
Generation Invariant. Mechanically `NeedsDecompose`.

## Subtree materialized (named state authored at this workspace)
- `_GLOBAL.md` — subtree hub (context, constraints, inputs, task tree, contract).
- `contracts/_MANIFEST.yaml` — sub-contract extending `../../contracts/` additively: the one shared traceability
  matrix with its columns split across the two analytical children and joined by the fold (`join_rule`), plus the
  six gate identities (`IDENTITIES_ALL_ASSERTED`, `MATRIX_COMPLETE`, `LIVE_STATUS_TOTAL`, `GAP_MAPPED`,
  `VERDICT_COMPLETE`, `VERDICT_HYGIENE`).
- Three child `_BRIEF.md` files.

Children materialized via `engine_amend_plan { add_task }`:

| Child | Task Kind | Depends on | Owns | Output |
|-------|-----------|-----------|------|--------|
| `SUBTASK_identity_traceability` | standard | none | the 8 identity verdicts + traceability-matrix skeleton (all columns but `live_status`) | `outputs/identity-and-traceability.md` |
| `SUBTASK_live_measurement` | standard | none | per-`BAR-*` `live_status` + observations (all 278) | `outputs/live-measurement.md` |
| `SUBTASK_fold` | synthesis | both above | the matrix join, the DAG-root verdict, any remediation subtree, the fold | `design-chirp-r1/SYNTHESIS.md` |

## Fold wiring
`SUBTASK_synthesis` is this DAG's designated root-synthesis child; the root `design-chirp-r1` is SUSPENDED awaiting a
`SYNTHESIS.md` at its workspace root (the `_FORK.md` observation seam). Because `SUBTASK_synthesis` decomposed, that
root fold is carried by the nested synthesis `SUBTASK_fold`, which authors `design-chirp-r1/SYNTHESIS.md` (the DAG
verdict: bar; issues by epic; measured standing with each gap mapped to its covering epic/issue) and resolves the
suspended ancestors so `design-chirp-r1` reaches COMPLETED with that verdict as its fold seam — following the
established in-DAG pattern (`SUBTASK_release_bar` / `SUBTASK_bar_synthesis`). A fixable gap found during the fold is
remediated by a further decomposed subtree, never a silent plug.

## Resumption condition
All child tasks reach terminal lifecycle state; the subtree folds through `SUBTASK_fold`, which resolves this node
and the DAG root.

## Environment note (taskflow-internal; kept out of the repository-bound verdict)
The Phase-B `design` methodology loader is unavailable run-wide (`agent_domain_unset`); every sibling synthesis gate
hit the same and proceeded. The children apply the principal-product-designer persona and the relayed Release
Definition guidance (CompletenessAndGapReview, ReleaseBar), reaching the software-domain synthesis-gate and
remediation-decomposition practice by prose, and record the limitation rather than blocking.
