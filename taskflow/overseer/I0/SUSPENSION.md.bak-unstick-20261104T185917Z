# SUSPENSION.md — NSWE overseer (TASK_ROOT_DECOMPOSE), iteration I0 → self-suspend on wake-on-DAG-fold

## What this iteration did (Act)
As the NSWE project overseer (`swe-lead`) for `Nousix-LLC/nswe-demo`, I booted the kernel + NSWE app-files, did INTAKE/recon, and set up the engagement — then dispatched the first code-writing DAG. **I wrote no code** (P1); all engineering is forked DAGs.

Established (the "Jira" working record):
- **GitHub Project** "NSWE Delivery" #1 (`PVT_kwDOEB9jls4BlZH4`, https://github.com/orgs/Nousix-LLC/projects/1), Status field `PVTSSF_lADOEB9jls4BlZH4zhkGLsc` (Todo `f75ad846` / In Progress `47fc9ee4` / Done `98236657`).
- **Milestones**: M1 Framework (#1), M2 Application (#2), M3 CI/CD & Deployment (#3).
- **Labels**: epic, framework, app, devops, infra, review, type:feature, type:chore, type:deploy, priority:high, blocked (+ defaults).
- **Issues #1–#13** (3 epics + 10 work-items), all on the board. Map in `project_state.json`.
- **Dispatched DAG**: `ferric-foundation` (issue #4) — forked `swe-coder` opus-4-8 DAG, workspace `taskflow/dags/ferric-foundation/`, board status In Progress. It will build the Cargo workspace + ferric core and open a PR into `main`.

Persisted STATE: `taskflow/overseer/I0/project_state.json` (authoritative carried memory).

## Why suspended (firing condition)
Continue-and-observe: I detached the `ferric-foundation` DAG and self-suspend at zero token cost until it folds. The resumption condition is the forked-thread-completion firing condition on thread id **`ferric-foundation`**.

## On resume — the turn to run (fresh invocation reads project_state.json + this file + the engine-templated resume seam)
Full step-by-step is in `taskflow/overseer/I1/_BRIEF.md`. Summary:
1. **3_MACHINE_GATE** — read `taskflow/dags/ferric-foundation/SYNTHESIS.md` (and `gh pr list/view -R Nousix-LLC/nswe-demo`). Do NOT re-run the build. FAIL → remediate (fork a fresh DAG, budget 2 then escalate). PASS → review gate.
2. **Review (a DAG)** — fork a `swe-coder` review DAG (bundles code-review+rust+core) to review the PR against acceptance criteria + methodologies, post `gh pr review`, write a verdict.
3. **Gate + LAND** — on approving review + green machine verdict, `gh pr merge --squash --delete-branch` into main (closes #4). Never force-push main.
4. **Board + STATE** — set #4 Status Done; append a `work_items[]` entry; bump current_pointer.
5. **Fan out** — fork the next wave: ferric-router (#5), ferric-http (#6), chirp-types (#7). Set them In Progress.
6. **Re-suspend** on those DAGs folding; continue the chain. Exit only when the whole engagement is delivered (framework + app + CI + ArgoCD-on-k3s reachable) and the board is all Done.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s cluster/namespaces + its ArgoCD. Never force-push `main`; never rewrite merged history. Changes land as PRs; reviews and devops and bug-fixes are each their own forked DAG; bugs are filed as issues.
