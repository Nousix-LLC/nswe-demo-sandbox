# Task: Fold the remediation verdict — root SYNTHESIS.md

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective

Verify that the parts of this remediation actually composed and fold them into the subtree's single verdict: a root
`SYNTHESIS.md` that accounts for CI-01 (fixed, with its verification) and each #118 item (fixed, or not and why), and
confirms no durability regression — the record the overseer reads as its observation seam.

### Context

Part of the PR #113 doc-blocker remediation (see `../_GLOBAL.md`). This is the decomposition's synthesis/verification
gate. Evaluate the contract identities in `../contracts/_MANIFEST.yaml` as assertions against the actual child
outputs; do **not** silently plug a failing identity — if an identity fails, report it plainly in the verdict so the
machine gate can route the result (PASS → re-review; FAIL → remediation #2).

**Dependencies**: `SUBTASK_assess`, `SUBTASK_apply_fixes`, `SUBTASK_verify_deliver`.
**Dependents**: none (this is the fold). On completion this folds the suspended root parent to COMPLETED.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Objective, success criteria |
| Contract | `../contracts/_MANIFEST.yaml`, `../contracts/inventory.schema.yaml` (read-only) | The identities to assert |
| Inventory | `../SUBTASK_assess/INVENTORY.md` | The diagnosed hazards (coverage denominator) |
| Changeset | `../SUBTASK_apply_fixes/CHANGESET.md` | The applied fixes (coverage numerator) |
| Verification | `../SUBTASK_verify_deliver/VERIFICATION.md` | The green-`doc` / no-regression / PR-state evidence |

## Output Specification

**Primary output**: `SYNTHESIS.md` written at the **subtree root** (the parent workspace,
`../SYNTHESIS.md` — the fold location). It must:
- State an overall verdict (PASS / FAIL) for the remediation.
- Account for **CI-01**: fixed? with what verification (the fresh green `doc` run under `-D warnings`)?
- Account for **each #118 item** (export.rs ungated→gated link; stale scaffold/placeholder docs; internal
  vocabulary): fixed, or not and why.
- Confirm **no durability regression** (clippy/fmt/test/wasm green; docs-only diff).
- Evaluate each contract identity (coverage, scope_docs_only, blocker_cleared, no_regression, output_hygiene) as
  pass/fail with the evidence, plugging nothing.
- Name PR #113's updated/mergeable state by repository identity.

## Success Criteria

- [ ] Every contract identity is evaluated with evidence; no failure is silently reconciled.
- [ ] The verdict cites CI-01 and each #118 item explicitly with its disposition.
- [ ] Non-regression is confirmed from the verification record.
- [ ] `SYNTHESIS.md` is self-contained and reader-facing, named entirely by repository identity.

## Constraints

- Report, do not repair: this gate does not edit source, commit, or push. If the parts did not compose, the verdict
  says so and why.
- Output hygiene: `SYNTHESIS.md` carries no host/cluster/SSH/credential/taskflow details; repository identities only.
