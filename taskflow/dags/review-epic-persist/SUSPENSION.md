# SUSPENSION — review-epic-persist root (NeedsDecompose)

## Why suspended

The review of PR #113 ("Durable PostgreSQL persistence for chirp") is not one invocation's work. Applying the
Task Decomposition Framework to the brief, the Scope-Based trigger and the Distinct Concerns Test fired by
the enumeration of seven+ distinct review concerns, each with its own bar, plus a standalone CI-failure
diagnosis and a multi-artifact delivery (PR review, root verdict, backlog issues). The Token/size trigger
also fired: the change is +11,851 / −77 across 28 files. Per Trigger Precedence, the fired scope triggers
decide — `NeedsDecompose`.

## What was decomposed

Hub-and-spoke over PR #113 at pinned commit `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`:

| Child | Group | Concern |
|---|---|---|
| `SUBTASK_correctness` | 0 | Correctness vs #65/#66/#67 + durable-persistence design requirement |
| `SUBTASK_durability_proof` | 0 | Tests, depth, and the stranger-runnable drill; `postgres` feature gating |
| `SUBTASK_code_quality` | 0 | Code quality, design, and Rust idiom |
| `SUBTASK_architecture_contract` | 0 | `ChirpRepository` seam + deployment-contract stability; AppProject minimality |
| `SUBTASK_security` | 0 | Credentials, injection, migration safety, Pod Security, dependency pull-ins |
| `SUBTASK_operational_readiness` | 0 | Provisioning, `/readyz` gating, reclaim CronJob, digest-pin follow-up |
| `SUBTASK_ci_doc_diagnosis` | 0 | Root-cause the failing required `doc` CI check; record as landing blocker |
| `SUBTASK_synthesis` | 1 | Fold all findings → one APPROVE/REQUEST-CHANGES verdict; author root `SYNTHESIS.md`; post the PR review; file backlog |

Named state authored: `_GLOBAL.md` (hub), `contracts/_MANIFEST.yaml` + `contracts/finding_schema.md` (the
finding-taxonomy contract every spoke composes against), and one `_BRIEF.md` per child. Each child
materialized via `engine_amend_plan { add_task }`.

## Resumption condition

All eight child tasks reach terminal lifecycle states. The `SUBTASK_synthesis` gate authors
`SYNTHESIS.md` at this workspace root (the fold location / observation seam) and folds this root
`SUSPENDED → COMPLETED` via `engine_resume_suspended`. The overseer gates on that folded root `SYNTHESIS.md`.
