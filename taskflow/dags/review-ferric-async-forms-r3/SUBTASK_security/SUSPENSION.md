# SUSPENSION — SUBTASK_security

## Status

Suspended for child subtree execution (NeedsDecompose).

## Decomposition

**Trigger:** The `_BRIEF.md` explicitly enumerates four distinct named security concern areas (HTML injection/escaping, secrets and infrastructure data, unsafe code, event handler surface / closure.forget()). The TDF enumerated-concerns rule fires for ≥2 distinct areas, and the Distinct Concerns Test confirms each area maps to a genuinely separate analysis specialty. Trigger precedence rules: scope/distinct-concerns overrides output-size clearing. Verdict: NeedsDecompose.

## Children Materialized

| Child task | Concern | Depends on |
|------------|---------|------------|
| `SUBTASK_sec_injection` | HTML injection / escaping gap | none |
| `SUBTASK_sec_secrets` | Secrets and infrastructure data scan | none |
| `SUBTASK_sec_unsafe` | Unsafe code audit | none |
| `SUBTASK_sec_event` | Event handler security surface + closure.forget() | none |
| `SUBTASK_sec_synthesis` | Verification gate: compile findings.md | all 4 spokes |

## Resumption Condition

All 5 child tasks must reach a terminal lifecycle state (COMPLETED or FAILED) before this node can complete. The synthesis child (`SUBTASK_sec_synthesis`) produces the declared output `findings.md` at this workspace root.

## Declared Output

`findings.md` at `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-async-forms-r3/SUBTASK_security/findings.md` (produced by `SUBTASK_sec_synthesis`).
