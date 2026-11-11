# SUSPENSION — review-ferric-ssr-r1

## Status

Suspended pending child subtree completion (NeedsDecompose).

## Why Decomposed

The review brief enumerates four distinct analysis areas:
1. Correctness against acceptance criteria for #223, #224, #226
2. Code quality, API design, test coverage, documentation
3. Security — HTML escaping and XSS risk in render_to_string
4. Security — infrastructure detail exposure and supply-chain risk

By the kernel's enumerated-concerns rule, the Scope-Based trigger fires on two or more enumerated
distinct analyses. The Distinct Concerns Test also fires: a correctness auditor, a code-quality
reviewer, an HTML-security analyst, and an infrastructure-exposure auditor are genuinely distinct
specializations. Per the system-prompt directive, trigger results override reviewer instinct.

## Child Subtree Authored

| Child | Workspace | Description |
|-------|-----------|-------------|
| SUBTASK_correctness | `SUBTASK_correctness/` | Acceptance-criteria correctness for #223, #224, #226 |
| SUBTASK_code_quality | `SUBTASK_code_quality/` | Code quality, API design, tests, docs |
| SUBTASK_security_xss | `SUBTASK_security_xss/` | HTML escaping / XSS security |
| SUBTASK_security_infra | `SUBTASK_security_infra/` | Infrastructure exposure / supply-chain |
| SUBTASK_synthesis | `SUBTASK_synthesis/` | Verification gate: verdict, GitHub review, SYNTHESIS.md |

The four spokes (correctness, code_quality, security_xss, security_infra) run in parallel (Group 0).
SUBTASK_synthesis runs in Group 1, depending on all four spokes.

## Resumption Condition

All five child tasks reach terminal lifecycle states.

## Declared Output

`SYNTHESIS.md` at this workspace root (`taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md`) —
authored by SUBTASK_synthesis, which folds this parent SUSPENDED → COMPLETED.
