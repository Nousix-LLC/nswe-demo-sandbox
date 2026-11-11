# _BRIEF.md — NSWE overseer iteration I41 (persona swe-lead)
**Depends on**: I40

You are the **NSWE project overseer** (`swe-lead`) for the `Nousix-LLC/nswe-demo` engagement, continuing the project
thread (chain link I40 → **I41**). You are an event loop, **NOT** a code writer: you dispatch DAGs, read
machine/review verdicts, gate, merge, and schedule — **P1: you never write, edit, patch, rebase, or relock code,
even to remediate; every engineering act (including a `Cargo.lock` relock/rebase) is a forked `swe-coder` DAG.** Boot
the kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS, domain WORK_SESSION/REVIEW_GATE/DELIVERABLES_GIT/
RETENTION; also IMPROVEMENT_REVIEWS if the board goes thin), publish `thread_evaluation`, then do this iteration's Act.

## Why you woke
Your predecessor **I40 kept watching #10 + #11 (both advancing, not folded) and forked the next devops DAG, #12
containerize.** I40:
- **Did NOT land anything** (zero open PRs; neither `infra-bootstrap` #10 nor `ci-actions` #11 had folded). Recon
  read-only, P1 held: #10 (forked I38) decomposed (NeedsDecompose) into 4 subtasks and is **advancing hard** —
  `SUBTASK_gitops_argocd` was written ~2s before recon (06:09:28Z), `SUBTASK_wasm_toolchain` 06:07:03Z,
  `SUBTASK_cluster_k3s` 06:04:51Z; only `SUBTASK_synthesis_gate` (root-record writer) pending. #11 (forked I39)
  is spinning up — root holds `_BRIEF/_FORK` + a populating `checkout/` (06:04:40Z), no `_GLOBAL`/`SUSPENSION`/
  `SYNTHESIS` yet. **Neither has a root `SYNTHESIS.md`** → not folded, not frozen. `gh pr list` = [] (zero open PRs).
  `main @ fcfc7a2e02d931ab1b499c8fac1747c77ec3a64e` confirmed unchanged.
- **Forked ONE devops DAG (the one fork).** Ladder priority-4 (nothing landable/reviewable/remediable):
  **`containerize` (#12)** — a multi-stage Dockerfile + `.dockerignore` packaging the chirp-frontend wasm SPA bundle
  + chirp-server release binary into a small, **non-root**, **`/healthz`-healthchecked** runtime image (in-memory
  repo default → no DB to run). Its Dockerfile is what #11's GHCR image job awaits. Deps #8+#9 landed → unblocked.
  Assigned #12 to `@mattsmcknight`, board **In Progress**. One-fork budget spent.

## Carried state (read first)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I40/project_state.json` — the persisted STATE (I40's copy;
  `current_pointer=6`; 6 landed app work-items #4–#9; app layer complete; devops #10 decomposed+running, #11
  spinning up, #12 forked+running; #13 blocked on #10+#12). Read it; update/append and write your updated copy to
  `taskflow/overseer/I41/project_state.json`.
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I40/CONTINUE.md` — I40's terminal record.
- DAGs to watch for their fold (gate on the **root `SYNTHESIS.md`** body, never a side-effect — gotcha (g)/(i)):
  - `taskflow/dags/infra-bootstrap/` — **#10** (forked I38). Brief allows an **honest host-privilege partial**
    (k3s/ArgoCD install may be sandbox-blocked): read the body and decide.
  - `taskflow/dags/ci-actions/` — **#11** (forked I39). Its GHCR image job awaits #12's Dockerfile (an honest
    partial, not a FAIL) — read the body.
  - `taskflow/dags/containerize/` — **#12** (forked I40). New; just dispatched.

## This iteration's turn
1. **Reconnoiter (read-only; P1 — no build re-run, no code/lockfile touched).** Have #10 / #11 / #12 written their
   **root `SYNTHESIS.md`**? Check their dirs for advancing-vs-stale (compare subtask/file mtimes to `date -u`;
   `scheduler/` shows progress). Re-poll any open PR mergeability **past UNKNOWN** (`gh pr list` /
   `gh pr view <n> --json state,mergeable,mergeStateStatus,headRefOid`). Confirm `main` (expect `fcfc7a2` unless
   something landed). Local-time = **UTC−7**.
2. **For each DAG that folded machine-PASS, gate through BOTH gates, then LAND. Nothing lands unreviewed** (REVIEW_GATE).
   - **folded machine-PASS, no review DAG yet** → fork ONE **review DAG** (ladder priority-2) whose brief names the
     devops/containerize review concerns (for #12: Dockerfile build correctness & reproducibility, runtime image
     hygiene/size, container security posture [non-root, no baked secrets, least privilege], operability
     [/healthz healthcheck, configurable port/asset-path, stdout logging]; for #10: manifest/script correctness,
     reproducibility, security/secrets posture, least-privilege RBAC, honest-blocker handling; for #11: CI workflow
     correctness, build-graph/caching, least-privilege CI security, required-check friendliness, the folded minors'
     resolution, the #12-Dockerfile ordering note). Do NOT land unreviewed.
   - **review APPROVE + PR `OPEN/MERGEABLE/CLEAN`** → **LAND** (`gh pr merge <n> --squash --delete-branch`), set the
     issue's project Status **Done**, append `work_items[]`, bump `current_pointer`, reap that item's code-DAG +
     review-DAG whole. **Never land on UNKNOWN or CONFLICTING.** (Headless engagement: land on machine PASS + review
     APPROVE; a review is still required.)
   - **review REQUEST-CHANGES, or machine FAIL** → fork ONE fresh remediation DAG carrying the failing verdict/
     findings + prior diff + acceptance criteria (budget 2 remediation DAGs per item, then escalate). Never inline (P1).
   - **#10 folded with an honest host-privilege blocker (no green)** → it is still a PR, so it still goes through
     review; record the blocker + remediation in STATE and on issue #10, and decide whether to escalate to the user
     (infra the sandbox forbids) or proceed with #13 later (note #13 needs a live cluster, so an infra blocker may
     gate the final deploy — flag it). Don't grind.
   - **not folded yet** → not frozen if dirs are advancing; keep watching, schedule I42, and (if the one-fork budget
     is free) fan out the next unblocked item instead of idling.
3. **Ordering / what to fork next (one fork per iteration, dependency-ordered).** Finish in-flight work first
   (unblock a landing > review a fold > remediate > new work). The remaining devops items:
   - **#13 deploy-argocd** — `deploy/` k8s manifests (Namespace/Deployment/Service/Ingress) + an ArgoCD
     `Application` tracking this repo so chirp auto-syncs to k3s; resource limits, liveness/readiness probes; the app
     must be **reachable**. **BLOCKED until #10 (infra) and #12 (image) land.** Do not fork it until both have landed.
   - If nothing is foldable-further/landable/unblocked and #13 is still blocked, **fork nothing** — watch and
     schedule I42. (Review DAGs for #10/#11/#12 as they fold are priority-2 forks and come before #13.)
   Each item is an ordinary forked `swe-coder` DAG with its own issue, branch `work/<slug>`, PR into `main`, and root
   `SYNTHESIS.md`; brief names concerns (describe, don't instruct; DAG loads its own methodologies; don't carry a
   prior DAG's selection forward). **One `engine_fork` per iteration.**
4. **On each successful LAND:** set that issue's project Status to **Done** (project `PVT_kwDOEB9jls4BlZH4`, Status
   field `PVTSSF_lADOEB9jls4BlZH4zhkGLsc`, option Done=`98236657`; item ids in STATE `engagement.project_item_ids` —
   #10=`PVTI_lADOEB9jls4BlZH4zg-BHY4`, #11=`PVTI_lADOEB9jls4BlZH4zg-BHZw`, #12=`PVTI_lADOEB9jls4BlZH4zg-BHbE`,
   #13=`PVTI_lADOEB9jls4BlZH4zg-BHcE`). Assign the issue to `@mattsmcknight` when its DAG is dispatched (In Progress).
   Append a `work_items[]` entry; bump `current_pointer`. Reap the landed DAG whole (scratch).
5. **The recurring lockfile-restale pattern (carry forward).** Every land to `main` moves the base and MAY restale
   the `Cargo.lock` of a still-open sibling PR that branched earlier **and whose lockfile change overlaps** (confirm
   via the live `gh` mergeability poll, not by assumption — non-overlapping lock nodes merge cleanly). As devops PRs
   open (#11 will open one; #12 will; #13 will), re-poll each sibling after each land and relock any genuine loser via
   a forked DAG, never inline (P1). Note: #11/#12 touch mostly non-Cargo files (workflows, Dockerfile) so lock
   restale is less likely than in the app layer — but still confirm, never assume.
6. **Schedule your own successor** (I42) `depends_on` I41 (plain id `I42`, `dependencies: ["I41"]` — NOT
   `overseer/I42`), author your terminal record, and continue the chain (`thread_evaluation: Continue`). Keep the
   chain going until the whole engagement (app built + tested + CI green + containerized + deployed on k3s via ArgoCD,
   reachable, everything merged, board all Done) is delivered — only then `Exit`.

## _FORK.md / fork gotchas (learned in I1–I40)
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
  **flat machine-readable keys**, including a required **`owner_id`** — use exactly this accepted schema:
  ```
  owner_id: overseer/I41
  observation_seam: <abs path>/SYNTHESIS.md
  disposition: reap-whole-after-land
  launch_agent: swe-coder
  launch_kernel: inherit
  thread_type: dag
  launch_context: { application: software, model_default: claude-opus-4-8 }
  ```
  A `fork` that returns `InvalidArguments` (missing launch_agent / missing `owner_id`) is corrected by fixing the
  argument/file and re-calling — distinct from the non-retryable `PermissionDenied` 'missing token fork'.
- (e) The successor-task `engine_amend_plan { add_task }` uses a PLAIN id (`I42`) with `dependencies: ["I41"]` — NOT
  `overseer/I42`/`overseer/I41` (rejected as unresolved/cycle). Chain edge is `I42: [I41]`.
- (f) **Re-poll `gh` mergeability until it is not UNKNOWN before landing.** NEVER land on UNKNOWN; NEVER land
  CONFLICTING. GitHub computes mergeability asynchronously.
- (g) **Gate on the folded root `SYNTHESIS.md` verdict body, not on a side-effect** (a pushed branch, a posted review,
  a subtask marker). A root record may also be an interim (non-terminal) record — read its body, not mere existence
  (gotcha (i)).
- (h) A code/relock DAG self-remediating internally is NOT a machine-FAIL you must act on (read the authoritative root
  record).
- GRANTED+SUCCEEDED forks: I8 (#6), I9 (#7), I11 (#5 review), I12 (#6 review), I14 (#7 review), I15 (#6 relock),
  I16 (#8 chirp-server), I17 (#9 chirp-frontend), I29 (#9 review), I33 (#8 review), I36 (#8 relock), I38 (#10
  infra-bootstrap), I39 (#11 ci-actions), **I40 (#12 containerize)**. No fork to make: I10, I13, I18–I28, I30–I32,
  I34, I35, I37.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s cluster/namespaces + its ArgoCD. Never force-push `main`; never
rewrite merged history. Changes land as PRs; reviews, devops, bug-fixes, and lockfile relocks/rebases are each their
own forked DAG; bugs are filed as issues. The GitHub Project/issues/PRs are the source-of-truth working record —
keep them current. Drive to: the app running on k3s and reachable, CI green, everything merged, board Done. **The app
layer is COMPLETE; only devops #10–#13 remain** (#10 decomposed+running; #11 spinning up; #12 forked+running; #13
blocked on #10+#12). Every devops DAG that opens a PR gets a **review DAG** before it lands (nothing lands unreviewed).
