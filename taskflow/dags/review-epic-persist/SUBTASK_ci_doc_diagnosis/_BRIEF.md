# Task: Diagnose the failing `doc` CI check — PR #113

## Task Specification

**Slug**: SUBTASK_ci_doc_diagnosis
**Task Kind**: standard
**Status**: Pending

### Objective

Diagnose exactly what the required `doc` CI job is failing on for PR #113, name the change that would make it
pass, and record it as a blocker to landing.

### Context

Part of the PR #113 review DAG (see `../_GLOBAL.md`). The live CI rollup is: `clippy` PASS, `fmt` PASS, `test`
PASS, `wasm` PASS, `image` skipping, **`doc` FAILING** → merge state `UNSTABLE`. `doc` is a *required* check:
the PR is not clean to land while it fails. The remediation (the actual fix) is a separate code DAG, **not**
this task — you diagnose and record, you do not fix. Read-only; write a findings document only.

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Pinned commit, target, constraints |
| Contract | `../contracts/finding_schema.md`, `../contracts/_MANIFEST.yaml` | Findings format + rubric |
| CI runs for PR #113 @ `09fa453` | `gh pr checks 113`, `gh run view --log` / `gh run view --log-failed` for the `doc` job | The failing job and its log |
| PR #113 diff @ `09fa453` | `gh pr diff 113` (read-only) | Correlate the failure to the change (e.g. a broken doc link, a failing doctest, an `rustdoc` warning-as-error) |

## The bar

The `doc` failure is a **blocker** to landing (`blocks_landing: true`), regardless of how clean the code
concerns are. Produce:

- The concrete root cause: which step of the `doc` job failed and on what (quote the relevant log lines by
  content, not host paths), tied to the change where possible.
- The specific change that would make `doc` pass.
- An explicit statement that landing is gated on `doc` going green **and** the PR being mergeable and clean.

## Output

`SUBTASK_ci_doc_diagnosis/outputs/findings.md`, conforming to `../contracts/finding_schema.md` (prefix `CI`).
At least one `blocker` finding for the `doc` failure.

## Success criteria

- [ ] Root cause of the `doc` failure identified from the job log, with the fix named.
- [ ] Recorded as a blocking finding; the landing gate stated explicitly.
- [ ] "What I checked" / "what I found clean" (e.g. the other checks passing) both stated; sub-verdict
  HAS-BLOCKERS.

## Constraints

Read-only on the repo; no GitHub writes. No host paths, runner internals, or DAG internals in the findings —
describe the failure by its content. Plain voice.
