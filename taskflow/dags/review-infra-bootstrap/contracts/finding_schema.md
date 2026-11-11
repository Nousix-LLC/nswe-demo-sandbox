# Finding record schema (review-infra-bootstrap contract)

READ-ONLY. Every finding every lens spoke emits, and every gate-level finding, MUST use this record shape so the
synthesis gate can mechanically assemble the consolidated per-severity list and the acceptance-criteria checklist.

## Finding record

Each finding is a block with these fields:

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Per the manifest `finding_id_convention` — `CORR-<n>` / `SEC-<n>` / `HSO-<n>` / `GATE-<n>`; the carried code-DAG finding is referenced as `F1`. |
| `lens` | yes | `correctness` \| `security` \| `honesty_scope_ops` \| `gate`. |
| `concern` | yes | Which of the 8 named concerns this finding belongs to (manifest `ownership.concerns` key). |
| `severity` | yes | `block` \| `major` \| `minor` \| `nit` (manifest `severity_vocabulary`). `block` = must fix before land. |
| `location` | yes | File + (where knowable) line/function/script section, e.g. `cluster/install-k3s.sh:42` or `gitops/README.md §Access`. Use `—` only when genuinely global. |
| `statement` | yes | What is wrong (or, for a PASS-style observation, what was verified) — specific, not generic. |
| `evidence` | yes | What was actually read/observed to support it — a quoted line, an absent pattern, a `grep` result, the code-DAG gate's recorded evidence. Not an unfounded reading. |
| `remediation` | required for `block`/`major` | The concrete, actionable change that would resolve it (reviewers propose; they do NOT apply it). Optional for `minor`/`nit`. |
| `acceptance_criteria_touched` | yes | Zero or more of `AC1_cluster`,`AC2_gitops`,`AC3_wasm`,`AC4_runbook` — which criteria this finding bears on (drives the gate's R2 checklist). `[]` if purely cross-cutting (e.g. an idiom nit). |

### Recommended rendering (Markdown)

```
- [CORR-1] severity=major concern=reproducibility_idempotency lens=correctness
  location=`wasm/build-chirp-wasm.sh:NN`
  acceptance_criteria_touched=[AC3_wasm, AC4_runbook]
  statement: <specific problem>
  evidence: <quoted line / observed behavior / absent guard>
  remediation: <concrete actionable fix the overseer's remediation DAG would apply>
```

## Per-lens output document shape

Each lens spoke writes ONE findings doc (its owned artifact). It MUST contain, at minimum:

1. **Lens summary** — one paragraph: overall read of the PR through this lens.
2. **Concern-by-concern assessment** — a short subsection per concern this lens owns (manifest
   `ownership.concerns`), each stating the concern's disposition (clean / findings raised) with evidence.
3. **Findings** — zero or more finding records in the schema above. A lens with no defects records that
   explicitly (an empty findings list with the evidence that justifies "clean") — absence of findings MUST be
   an asserted, evidenced conclusion, never silence.
4. **Acceptance-criteria bearing** — which of AC1..AC4 this lens's findings touch, so the gate can assemble R2.

## Gate output (SYNTHESIS.md) required elements

Owned by `SUBTASK_synthesis_gate`, authored at the PARENT workspace (the fold/observation seam
`review-infra-bootstrap/SYNTHESIS.md`). It MUST carry:

- `verdict:` exactly one of `APPROVE` / `REQUEST-CHANGES` (per manifest `verdict_rule`).
- **Consolidated per-severity finding list** (block / major / minor / nit) merged from the three lens docs + any `GATE-<n>`.
- **Acceptance-criteria checklist** AC1..AC4, each with an explicit pass/fail and the finding(s)/evidence behind it (R2).
- **k3d-vs-native line** — the single verdict (acceptable | blocking-weakening) with reasoning (R4).
- **F1 disposition** — carry-as-tracked-issue | drop, with rationale (R5).
- **Open-blocker statement** — whether any block/major finding is open (drives R6 consistency with `verdict`).
- **Identity assertion table** R1..R7 — each evaluated pass/fail with evidence; a failing identity is reported, never plugged.
