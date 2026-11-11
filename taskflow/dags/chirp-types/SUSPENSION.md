# SUSPENSION — chirp-types subtree (NeedsDecompose)

**Task**: `chirp-types` (forked DAG root, work-item #7)
**Terminal state**: SUSPENDED — `decompose_evaluation = NeedsDecompose`
**Resumption condition**: all child tasks reach terminal lifecycle state; the subtree then folds via
the synthesis gate's `SYNTHESIS.md` → `resume_suspended`, flipping this node SUSPENDED → COMPLETED.

## Decompose evaluation (recorded for audit)

Applied the kernel triggers to this brief at the evaluation point:

| Trigger / test | Outcome | Note |
|---|---|---|
| Token-based | CLEARS | Inputs tiny (brief + conventions to read). |
| Output Size | FIRES | Crate source + tests + README + verdict exceed 400 lines across files (weakest signal). |
| Scope-Based / enumerated-concerns | FIRES | Two distinct *kinds* of work: author the coherent type surface vs. a verification gate + PR delivery (different methodology surfaces: rust/core/architecture vs. synthesis/code-review). |
| Single-Responsibility | FIRES | "implement the crate AND verify-and-deliver it" — change-then-judge serial pipeline. |
| Distinct Concerns | FIRES | Implementation and the gate are different responsibilities with a hard serial dependency. |

Verdict: **NeedsDecompose**. Multiple triggers fire; asymmetric bias and the fork's explicit
`decompose → implement → synthesize` framing confirm. The domain-model + DTO type surface is kept in
ONE implementation spoke deliberately: it is one single-source-of-truth artifact written into shared
files (`lib.rs`, `Cargo.toml`); splitting it would put two writers on one file — an
ownership-disjointness violation (invalid cut), not an improvement.

## Chosen cut (greenfield contract-first shape, degenerate width N=1)

Serial pipeline **implement → synthesis-gate**:

| Task id | Group | Kind | Depends on | Output |
|---|---|---|---|---|
| `SUBTASK_implement_crate` | 0 | standard | none | `SUBTASK_implement_crate/IMPLEMENTATION_NOTES.md` (+ crate committed to `work/chirp-types` in `checkout/`) |
| `SUBTASK_synthesis_gate` | 1 | synthesis | `SUBTASK_implement_crate` | `SYNTHESIS.md` (this workspace — fold location / observation seam) |

## Contract (seam)

The one cross-sibling edge is serialized by the dependency (the gate reads the real built clone), so
no interface freeze/mock is needed for the data. The thin `contracts/_MANIFEST.yaml` freezes the
forced/stable shared conventions (clone path, branch `work/chirp-types`, crate path/name, dependency
policy, PR title/body, fold-record path) and the gate's assertion set (build/test/fmt/clippy + PR),
each identity carrying a runnable check.

## Named state authored this invocation

- `_GLOBAL.md` — subtree hub (this workspace)
- `contracts/_MANIFEST.yaml` — thin contract
- `SUBTASK_implement_crate/_BRIEF.md`
- `SUBTASK_synthesis_gate/_BRIEF.md`
- `SUSPENSION.md` — this record

Both children materialized via `engine_amend_plan { add_task }`. This invocation did NOT execute any
child's work.
