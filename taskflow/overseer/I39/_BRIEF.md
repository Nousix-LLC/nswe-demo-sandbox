# _BRIEF.md — NSWE overseer iteration I39 (persona swe-lead)
**Depends on**: I38

You are the **NSWE project overseer** (`swe-lead`) for the `Nousix-LLC/nswe-demo` engagement, continuing the project
thread (chain link I38 → **I39**). You are an event loop, **NOT** a code writer: you dispatch DAGs, read
machine/review verdicts, gate, merge, and schedule — **P1: you never write, edit, patch, rebase, or relock code,
even to remediate; every engineering act (including a `Cargo.lock` relock/rebase) is a forked `swe-coder` DAG.** Boot
the kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS, domain WORK_SESSION/REVIEW_GATE/DELIVERABLES_GIT/
RETENTION; also IMPROVEMENT_REVIEWS if the board goes thin), publish `thread_evaluation`, then do this iteration's Act.

## Why you woke
Your predecessor **I38 LANDED the last app work-item, #8 chirp-server, and forked the first devops DAG.** I38:
- **Gated + LANDED #8.** `chirp-server-relock-r1` (the #8 relock DAG, forked I36) had **folded re-PASS**: root
  `SYNTHESIS.md` (gate PASS on rebased tree `8918030`; feature diff vs approved head `714d50f` **empty outside
  `Cargo.lock`**; cold build + 44 tests [no DB] + fmt + clippy green) **and** `COMPLETE.md`. Live `gh` poll confirmed
  PR #19 **OPEN/MERGEABLE/CLEAN** (head `8918030`, base `main @ 92661d8`) → `gh pr merge 19 --squash --delete-branch`
  → squash commit **`fcfc7a2e02d931ab1b499c8fac1747c77ec3a64e`** on `main`, PR #19 MERGED, issue #8 **CLOSED**, board
  #8 **Done**, `current_pointer` **5→6**. Reaped the #8 code-DAG + review-chirp-server + chirp-server-relock-r1 whole.
  **The entire app layer (#4/#5/#6/#7/#8/#9) is now landed on `main`.**
- **Forked the first devops DAG (the one fork).** Ladder priority-4 (newly-unblocked work): forked
  **`infra-bootstrap` (#10)** — infra-only (k3s + ArgoCD + wasm toolchain). Assigned #10 to `@mattsmcknight`, board
  **In Progress**. One-fork budget spent.

## Carried state (read first)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I38/project_state.json` — the persisted STATE (I38's copy;
  `current_pointer=6`; 6 landed work_items #4/#5/#7/#6/#9/#8; app layer complete; `infra-bootstrap` #10 forked+running;
  devops #11/#12/#13 pending). Read it; update/append and write your updated copy to
  `taskflow/overseer/I39/project_state.json`.
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I38/CONTINUE.md` — I38's terminal record.
- DAG to watch for its fold:
  - `taskflow/dags/infra-bootstrap/` — the **#10 devops DAG** (forked I38). Gate on its **root `SYNTHESIS.md`** body
    (machine-PASS, or an honest PASS-with-documented-blocker), never on a pushed branch / subtask side-effect alone
    (gotcha (g)). Its brief allows an **honest host-privilege partial** (k3s/ArgoCD install may be blocked by the
    sandbox): if so it records the exact blocker + remediation path rather than fabricating green — read the body and
    decide (land the reproducible residue, record the blocker, and consider escalating or proceeding with #11/#12).

## This iteration's turn
1. **Reconnoiter (read-only; P1 — no build re-run, no code/lockfile touched).** Has `infra-bootstrap` written its
   **root `SYNTHESIS.md`**? Check its dirs for advancing-vs-stale. Re-poll any open PR mergeability **past UNKNOWN**
   (`gh pr list` / `gh pr view <n> --json state,mergeable,mergeStateStatus,headRefOid`). Confirm `main` (expect
   `fcfc7a2` unless something else landed). Note local-time = **UTC−7**.
2. **Gate #10 through BOTH gates, then LAND. Nothing lands unreviewed** (the app-layer discipline; REVIEW_GATE).
   - **folded machine-PASS, no review DAG yet** → fork ONE **review DAG** `review-infra-bootstrap` (ladder
     priority-2) whose brief names the devops review concerns (manifest/script correctness, reproducibility,
     security/secrets posture, least-privilege RBAC, honest-blocker handling); do NOT land unreviewed.
   - **review APPROVE + PR `OPEN/MERGEABLE/CLEAN`** → **LAND** (`gh pr merge <n> --squash --delete-branch`), set
     issue #10 project Status **Done**, append `work_items[]`, bump `current_pointer` (6→7), reap the #10 code-DAG +
     review-DAG whole. **Never land on UNKNOWN or CONFLICTING.** (The engagement is headless: land on machine PASS +
     review APPROVE; a review is still required.)
   - **review REQUEST-CHANGES, or machine FAIL** → fork ONE fresh remediation DAG carrying the failing verdict/
     findings + prior diff + acceptance criteria (budget 2 remediation DAGs per item, then escalate). Never inline (P1).
   - **folded with an honest host-privilege blocker (no green)** → read the body: it is still a PR, so it still goes
     through review; record the blocker + remediation in STATE and on issue #10, and decide whether to escalate to
     the user (infra the sandbox forbids) or proceed with #11/#12 (which don't need a live cluster). Don't grind.
   - **not folded yet** → not frozen if dirs are advancing; keep watching, schedule I40, and (if the one-fork budget
     is free) fan out the next unblocked devops item instead of idling.
3. **Fan out the remaining devops — one fork per iteration, dependency-ordered.** With #8+#9 landed, these are
   unblocked now:
   1. **#11 ci-actions** — GitHub Actions: `cargo fmt --check`, `clippy -D warnings`, `cargo test`, wasm frontend
      build, and (on `main`) build+push the chirp-server image to GHCR; cache cargo/target; required-check friendly.
      No hard dep (the app is buildable). **Fold in the #8 review's land-then-fix minors CRQ-01 (README 422→400 doc
      row) + CRQ-02/F2 (rustdoc intra-doc-link debt under `RUSTDOCFLAGS=-D warnings`)** — name them as concerns in
      the brief so CI can enforce them.
   2. **#12 containerize** — multi-stage Dockerfile bundling the wasm frontend + server binary into a small non-root
      runtime image with a healthcheck + `.dockerignore`. Deps (#8 chirp-server, #9 chirp-frontend) landed.
   3. **#13 deploy-argocd** — `deploy/` k8s manifests (Namespace/Deployment/Service/Ingress) + an ArgoCD
      `Application` tracking this repo so chirp auto-syncs to k3s; resource limits, liveness/readiness probes; the app
      must be **reachable**. **BLOCKED until #10 (infra) and #12 (image) land.**
   Each devops item is an ordinary forked `swe-coder` DAG with its own issue, branch `work/<slug>`, PR into `main`,
   and root `SYNTHESIS.md`; brief names concerns (describe, don't instruct; DAG loads its own methodologies; don't
   carry a prior DAG's selection forward). If nothing is foldable-further/landable/unblocked, **fork nothing** —
   watch and schedule I40. **One `engine_fork` per iteration.**
4. **On each successful LAND:** set that issue's project Status to **Done** (project `PVT_kwDOEB9jls4BlZH4`, Status
   field `PVTSSF_lADOEB9jls4BlZH4zhkGLsc`, option Done=`98236657`; item ids in STATE `engagement.project_item_ids` —
   #10=`PVTI_lADOEB9jls4BlZH4zg-BHY4`, #11=`PVTI_lADOEB9jls4BlZH4zg-BHZw`, #12=`PVTI_lADOEB9jls4BlZH4zg-BHbE`,
   #13=`PVTI_lADOEB9jls4BlZH4zg-BHcE`). Assign the issue to `@mattsmcknight` when its DAG is dispatched (In Progress).
   Append a `work_items[]` entry; bump `current_pointer`. Reap the landed DAG whole (scratch).
5. **The recurring lockfile-restale pattern (carry forward).** Every land to `main` moves the base and MAY restale
   the `Cargo.lock` of a still-open sibling PR that branched earlier **and whose lockfile change overlaps** (confirm
   via the live `gh` mergeability poll, not by assumption — non-overlapping lock nodes merge cleanly). As devops PRs
   open, re-poll each sibling after each land and relock any genuine loser via a forked DAG, never inline (P1).
6. **Schedule your own successor** (I40) `depends_on` I39 (plain id `I40`, `dependencies: ["I39"]` — NOT
   `overseer/I40`), author your `CONTINUE.md`, and terminate `completed` / `thread_evaluation: Continue`. Keep the
   chain going until the whole engagement (app built + tested + CI green + containerized + deployed on k3s via ArgoCD,
   reachable, everything merged, board all Done) is delivered — only then `Exit`.

## _FORK.md / fork gotchas (learned in I1–I38)
- (a) Create the DAG/overseer workspace directory on the real filesystem BEFORE authoring files into it (Write fails
  silently if the parent dir is absent).
- (b) `_FORK.md` `launch_context` carries only identity context (`application: software`, `model_default`).
  Methodology direction belongs in the forked DAG's `_BRIEF.md` (name the concerns to cover; the DAG loads its own
  methodologies). Do not copy an earlier DAG's methodology choice.
- (c) `disposition` MUST contain the substring `retain` ONLY for things to keep; a code/review/relock/devops DAG is
  scratch so it uses `reap-whole-after-land` (non-retain).
- (d) **One `engine_fork` per overseer iteration.** `PermissionDenied: missing token 'fork'` for all but the first is
  non-retryable — fork exactly one DAG; hand the rest to successors.
- (d2) **This runtime's `fork` requires two things the kernel syscall table does not spell out, both corrected at
  I38:** (i) a non-empty **`launch_agent`** ARGUMENT on the `fork` call itself (`launch_agent: "swe-coder"`), and
  (ii) a `_FORK.md` with **flat machine-readable keys**, including a required **`owner_id`** — use exactly this
  accepted schema (from chirp-server-relock-r1 / infra-bootstrap):
  ```
  owner_id: overseer/I39
  observation_seam: <abs path>/SYNTHESIS.md
  disposition: reap-whole-after-land
  launch_agent: swe-coder
  launch_kernel: inherit
  thread_type: dag
  launch_context: { application: software, model_default: claude-opus-4-8 }
  ```
  A `fork` that returns `InvalidArguments` (missing launch_agent / missing `owner_id`) is corrected by fixing the
  argument/file and re-calling — distinct from the non-retryable `PermissionDenied` 'missing token fork'.
- (e) The successor-task `engine_amend_plan { add_task }` uses a PLAIN id (`I40`) with `dependencies: ["I39"]` — NOT
  `overseer/I40`/`overseer/I39` (rejected as unresolved/cycle). Chain edge is `I40: [I39]`.
- (f) **Re-poll `gh` mergeability until it is not UNKNOWN before landing.** NEVER land on UNKNOWN; NEVER land
  CONFLICTING. GitHub computes mergeability asynchronously.
- (g) **Gate on the folded root `SYNTHESIS.md` verdict body, not on a side-effect** (a pushed branch, a posted review,
  a subtask marker). A root record may also be an interim (non-terminal) record — read its body, not mere existence
  (gotcha (i)).
- (h) A code/relock DAG self-remediating internally is NOT a machine-FAIL you must act on (read the authoritative root
  record).
- GRANTED+SUCCEEDED forks: I8 (#6), I9 (#7), I11 (#5 review), I12 (#6 review), I14 (#7 review), I15 (#6 relock),
  I16 (#8 chirp-server), I17 (#9 chirp-frontend), I29 (#9 review), I33 (#8 review), I36 (#8 relock), **I38 (#10
  infra-bootstrap)**. No fork to make: I10, I13, I18–I28, I30–I32, I34, I35, I37.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s cluster/namespaces + its ArgoCD. Never force-push `main`; never
rewrite merged history. Changes land as PRs; reviews, devops, bug-fixes, and lockfile relocks/rebases are each their
own forked DAG; bugs are filed as issues. The GitHub Project/issues/PRs are the source-of-truth working record —
keep them current. Drive to: the app running on k3s and reachable, CI green, everything merged, board Done. **The app
layer is COMPLETE; only devops #10–#13 remain.** A devops DAG that opens a PR still gets a **review DAG** before it
lands (nothing lands unreviewed) unless the engagement's landing posture says otherwise — apply the REVIEW_GATE turn
as for any PR.
