# SUSPENSION.md — SUBTASK_scope_verification (NeedsDecompose)

## Disposition

**Suspended pending child subtree completion.** This spoke evaluated `NeedsDecompose` and
decomposed into a hub-and-spoke sub-DAG. It remains SUSPENDED until its subtree resolves to
terminal states and the synthesis gate folds it `SUSPENDED → COMPLETED`.

## Why decomposed (evaluation record)

The parent brief enumerated **two distinct concerns** — concern 7 (verification / evidence adequacy,
primary input = the machine-gate evidence record, lens = the `testing` bundle) and concern 8 (scope
conformance, primary input = the PR #22 file manifest, lens = the `code-review` bundle). Per the
Task Decomposition Framework:

- **Scope-Based trigger FIRED** — enumerated distinct concerns + two distinct methodologies to apply.
- **Distinct Concerns Test passed-as-fire** — the two judgments are independent and parallelizable.
- **Single-Responsibility / conjunction** — "judge evidence adequacy AND judge scope conformance" joins two distinct verbs.
- **Trigger Precedence** — the single declared output (`findings.md`) is the weakest signal and does NOT override the fired scope trigger.
- **Token / Output-Size triggers** cleared (small), but cleared weak signals cannot cancel a fired scope trigger; asymmetric bias resolves uncertainty to decompose.

Verdict: `NeedsDecompose`.

## Children materialized

| Child | Depends on | Concern | Declared output |
|---|---|---|---|
| `SUBTASK_verification_depth` | none | 7 — nine-criteria evidence adequacy | `SUBTASK_verification_depth/verification_findings.md` |
| `SUBTASK_scope_conformance` | none | 8 — touched-file scope boundary | `SUBTASK_scope_conformance/scope_findings.md` |
| `SUBTASK_findings_synthesis` | both spokes | integration gate | `findings.md` (this workspace) + `SYNTHESIS.md` (fold record) |

## Subtree named state authored

- `_GLOBAL.md` — subtree hub (objective, posture, Task Summary DAG, contract, identities SV1–SV6).
- `contracts/_MANIFEST.yaml` — taxonomy sub-contract: `SCOPE-V*`/`SCOPE-S*` finding-ID partition,
  per-concern ownership, merge identities; extends (does not override) the inherited
  `../contracts/findings_schema.md`.
- `SUBTASK_verification_depth/_BRIEF.md`, `SUBTASK_scope_conformance/_BRIEF.md`,
  `SUBTASK_findings_synthesis/_BRIEF.md`.

## Resumption condition

All three child tasks reach terminal lifecycle state. `SUBTASK_findings_synthesis` writes
`findings.md` + `SYNTHESIS.md` at this spoke's workspace (the fold location) and calls
`engine_resume_suspended`, folding this spoke `SUSPENDED → COMPLETED` with `findings.md` as its
declared output for the grandparent review DAG.
