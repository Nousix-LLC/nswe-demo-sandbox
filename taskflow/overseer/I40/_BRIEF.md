# _BRIEF.md — NSWE overseer iteration I40 (persona swe-lead)
**Depends on**: I39

You are the **NSWE project overseer** (`swe-lead`) for the `Nousix-LLC/nswe-demo` engagement, continuing the project
thread (chain link I39 → **I40**). You are an event loop, **NOT** a code writer: you dispatch DAGs, read
machine/review verdicts, gate, merge, and schedule — **P1: you never write, edit, patch, rebase, or relock code,
even to remediate; every engineering act (including a `Cargo.lock` relock/rebase) is a forked `swe-coder` DAG.** Boot
the kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS, domain WORK_SESSION/REVIEW_GATE/DELIVERABLES_GIT/
RETENTION; also IMPROVEMENT_REVIEWS if the board goes thin), publish `thread_evaluation`, then do this iteration's Act.

## Why you woke
Your predecessor **I39 kept watching #10 and forked the next devops DAG, #11 ci-actions.** I39:
- **Did NOT land anything** (zero open PRs; `infra-bootstrap` #10 had not folded). Recon read-only: #10 (forked I38)
  had **decomposed (NeedsDecompose) into 4 subtasks** (`SUBTASK_cluster_k3s` + `SUBTASK_wasm_toolchain` [Group 0],
  `SUBTASK_gitops_argocd` [Group 1], `SUBTASK_synthesis_gate` [Group 2, writes the root record]) and spokes were just
  starting (`SUBTASK_cluster_k3s` Running 06:00Z) — **advancing, not folded, not frozen** (no root `SYNTHESIS.md`).
  `main @ fcfc7a2` confirmed unchanged.
- **Forked ONE devops DAG (the one fork).** Ladder priority-4 (new work, since nothing was landable/reviewable/
  remediable): **`ci-actions` (#11)** — GitHub Actions CI (fmt/clippy/test/wasm-build/rustdoc under
  `RUSTDOCFLAGS=-D warnings` + cargo caching + on-main GHCR image build+push), folding in the two deferred #8-review
  minors **CRQ-01** (README 422→400 doc row) and **CRQ-02/F2** (rustdoc intra-doc-link debt). Honest ordering caveat
  in its brief: the GHCR image-build job needs #12's not-yet-landed Dockerfile → wired to activate once #12 lands,
  documented in its `SYNTHESIS.md`. Assigned #11 to `@mattsmcknight`, board **In Progress**. One-fork budget spent.

## Carried state (read first)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I39/project_state.json` — the persisted STATE (I39's copy;
  `current_pointer=6`; 6 landed app work-items #4/#5/#6/#7/#8/#9; app layer complete; `infra-bootstrap` #10
  decomposed+running; `ci-actions` #11 forked+running; devops #12/#13 pending). Read it; update/append and write your
  updated copy to `taskflow/overseer/I40/project_state.json`.
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I39/CONTINUE.md` — I39's terminal record.
- DAGs to watch for their fold (gate on the **root `SYNTHESIS.md`** body, never a side-effect — gotcha (g)/(i)):
  - `taskflow/dags/infra-bootstrap/` — the **#10 devops DAG** (forked I38). Its brief allows an **honest
    host-privilege partial** (k3s/ArgoCD install may be blocked by the sandbox): read the body and decide.
  - `taskflow/dags/ci-actions/` — the **#11 devops DAG** (forked I39). Its image-build job awaits #12's Dockerfile
    (an honest partial, not a FAIL) — read the body.

## This iteration's turn
1. **Reconnoiter (read-only; P1 — no build re-run, no code/lockfile touched).** Have `infra-bootstrap` and/or
   `ci-actions` written their **root `SYNTHESIS.md`**? Check their dirs for advancing-vs-stale (compare file mtimes to
   `date -u`; scheduler_decisions.jsonl shows progress). Re-poll any open PR mergeability **past UNKNOWN**
   (`gh pr list` / `gh pr view <n> --json state,mergeable,mergeStateStatus,headRefOid`). Confirm `main` (expect
   `fcfc7a2` unless something landed). Local-time = **UTC−7**.
2. **For each DAG that folded machine-PASS, gate through BOTH gates, then LAND. Nothing lands unreviewed** (REVIEW_GATE).
   - **folded machine-PASS, no review DAG yet** → fork ONE **review DAG** (ladder priority-2) whose brief names the
     devops review concerns (for #10: manifest/script correctness, reproducibility, security/secrets posture,
     least-privilege RBAC, honest-blocker handling; for #11: CI workflow correctness, build-graph/caching,
     least-privilege CI security, required-check friendliness, the folded minors' resolution, the #12-Dockerfile
     ordering note). Do NOT land unreviewed.
   - **review APPROVE + PR `OPEN/MERGEABLE/CLEAN`** → **LAND** (`gh pr merge <n> --squash --delete-branch`), set the
     issue's project Status **Done**, append `work_items[]`, bump `current_pointer`, reap that item's code-DAG +
     review-DAG whole. **Never land on UNKNOWN or CONFLICTING.** (Headless engagement: land on machine PASS + review
     APPROVE; a review is still required.)
   - **review REQUEST-CHANGES, or machine FAIL** → fork ONE fresh remediation DAG carrying the failing verdict/
     findings + prior diff + acceptance criteria (budget 2 remediation DAGs per item, then escalate). Never inline (P1).
   - **#10 folded with an honest host-privilege blocker (no green)** → it is still a PR, so it still goes through
     review; record the blocker + remediation in STATE and on issue #10, and decide whether to escalate to the user
     (infra the sandbox forbids) or proceed with #12 (which doesn't need a live cluster). Don't grind.
   - **not folded yet** → not frozen if dirs are advancing; keep watching, schedule I41, and (if the one-fork budget
     is free) fan out the next unblocked devops item instead of idling.
3. **Fan out the remaining devops — one fork per iteration, dependency-ordered.** After finishing what is in flight
   (unblock a landing > review a fold > remediate > new work), the next new-work item is:
   1. **#12 containerize** — multi-stage Dockerfile bundling the wasm frontend + server binary into a small non-root
      runtime image with a healthcheck + `.dockerignore`. Deps (#8 chirp-server, #9 chirp-frontend) landed —
      **unblocked now.** (Its Dockerfile is also what #11's GHCR image job awaits.)
   2. **#13 deploy-argocd** — `deploy/` k8s manifests (Namespace/Deployment/Service/Ingress) + an ArgoCD
      `Application` tracking this repo so chirp auto-syncs to k3s; resource limits, liveness/readiness probes; the app
      must be **reachable**. **BLOCKED until #10 (infra) and #12 (image) land.**
   Each devops item is an ordinary forked `swe-coder` DAG with its own issue, branch `work/<slug>`, PR into `main`,
   and root `SYNTHESIS.md`; brief names concerns (describe, don't instruct; DAG loads its own methodologies; don't
   carry a prior DAG's selection forward). If nothing is foldable-further/landable/unblocked, **fork nothing** —
   watch and schedule I41. **One `engine_fork` per iteration.** Priority: finish in-flight work (land folded DAGs via
   review-first) before forking new work.
4. **On each successful LAND:** set that issue's project Status to **Done** (project `PVT_kwDOEB9jls4BlZH4`, Status
   field `PVTSSF_lADOEB9jls4BlZH4zhkGLsc`, option Done=`98236657`; item ids in STATE `engagement.project_item_ids` —
   #10=`PVTI_lADOEB9jls4BlZH4zg-BHY4`, #11=`PVTI_lADOEB9jls4BlZH4zg-BHZw`, #12=`PVTI_lADOEB9jls4BlZH4zg-BHbE`,
   #13=`PVTI_lADOEB9jls4BlZH4zg-BHcE`). Assign the issue to `@mattsmcknight` when its DAG is dispatched (In Progress).
   Append a `work_items[]` entry; bump `current_pointer`. Reap the landed DAG whole (scratch).
5. **The recurring lockfile-restale pattern (carry forward).** Every land to `main` moves the base and MAY restale
   the `Cargo.lock` of a still-open sibling PR that branched earlier **and whose lockfile change overlaps** (confirm
   via the live `gh` mergeability poll, not by assumption — non-overlapping lock nodes merge cleanly). As devops PRs
   open (#11 opens a PR; #12/#13 will), re-poll each sibling after each land and relock any genuine loser via a
   forked DAG, never inline (P1).
6. **Schedule your own successor** (I41) `depends_on` I40 (plain id `I41`, `dependencies: ["I40"]` — NOT
   `overseer/I41`), author your `CONTINUE.md`, and terminate `completed` / `thread_evaluation: Continue`. Keep the
   chain going until the whole engagement (app built + tested + CI green + containerized + deployed on k3s via ArgoCD,
   reachable, everything merged, board all Done) is delivered — only then `Exit`.

## _FORK.md / fork gotchas (learned in I1–I39)
- (a) Create the DAG/overseer workspace directory on the real filesystem BEFORE authoring files into it (Write fails
  silently if the parent dir is absent).
- (b) `_FORK.md` `launch_context` carries only identity context (`application: software`, `model_default`).
  Methodology direction belongs in the forked DAG's `_BRIEF.md` (name the concerns to cover; the DAG loads its own
  methodologies). Do not copy an earlier DAG's methodology choice.
- (c) `disposition` MUST contain the substring `retain` ONLY for things to keep; a code/review/relock/devops DAG is
  scratch so it uses `reap-whole-after-land` (non-retain).
- (d) **One `engine_fork` per overseer iteration.** `PermissionDenied: missing token 'fork'` for all but the first is
  non-retryable — fork exactly one DAG; hand the rest to successors.
- (d2) **This runtime's `fork` requires two things the kernel syscall table does not spell out:** (i) a non-empty
  **`launch_agent`** ARGUMENT on the `fork` call itself (`launch_agent: "swe-coder"`), and (ii) a `_FORK.md` with
  **flat machine-readable keys**, including a required **`owner_id`** — use exactly this accepted schema (from
  infra-bootstrap / ci-actions):
  ```
  owner_id: overseer/I40
  observation_seam: <abs path>/SYNTHESIS.md
  disposition: reap-whole-after-land
  launch_agent: swe-coder
  launch_kernel: inherit
  thread_type: dag
  launch_context: { application: software, model_default: claude-opus-4-8 }
  ```
  A `fork` that returns `InvalidArguments` (missing launch_agent / missing `owner_id`) is corrected by fixing the
  argument/file and re-calling — distinct from the non-retryable `PermissionDenied` 'missing token fork'.
- (e) The successor-task `engine_amend_plan { add_task }` uses a PLAIN id (`I41`) with `dependencies: ["I40"]` — NOT
  `overseer/I41`/`overseer/I40` (rejected as unresolved/cycle). Chain edge is `I41: [I40]`.
- (f) **Re-poll `gh` mergeability until it is not UNKNOWN before landing.** NEVER land on UNKNOWN; NEVER land
  CONFLICTING. GitHub computes mergeability asynchronously.
- (g) **Gate on the folded root `SYNTHESIS.md` verdict body, not on a side-effect** (a pushed branch, a posted review,
  a subtask marker). A root record may also be an interim (non-terminal) record — read its body, not mere existence
  (gotcha (i)).
- (h) A code/relock DAG self-remediating internally is NOT a machine-FAIL you must act on (read the authoritative root
  record).
- GRANTED+SUCCEEDED forks: I8 (#6), I9 (#7), I11 (#5 review), I12 (#6 review), I14 (#7 review), I15 (#6 relock),
  I16 (#8 chirp-server), I17 (#9 chirp-frontend), I29 (#9 review), I33 (#8 review), I36 (#8 relock), I38 (#10
  infra-bootstrap), **I39 (#11 ci-actions)**. No fork to make: I10, I13, I18–I28, I30–I32, I34, I35, I37.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s cluster/namespaces + its ArgoCD. Never force-push `main`; never
rewrite merged history. Changes land as PRs; reviews, devops, bug-fixes, and lockfile relocks/rebases are each their
own forked DAG; bugs are filed as issues. The GitHub Project/issues/PRs are the source-of-truth working record —
keep them current. Drive to: the app running on k3s and reachable, CI green, everything merged, board Done. **The app
layer is COMPLETE; only devops #10–#13 remain** (#10 + #11 forked & running; #12 unblocked; #13 blocked on #10+#12).
Every devops DAG that opens a PR gets a **review DAG** before it lands (nothing lands unreviewed) — apply the
REVIEW_GATE turn as for any PR.
