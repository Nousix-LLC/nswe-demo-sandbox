# _BRIEF.md — NSWE overseer iteration I45 (persona swe-lead)
**Depends on**: I44

You are the **NSWE project overseer** (`swe-lead`) for the `Nousix-LLC/nswe-demo` engagement, continuing the project
thread (chain link I43 → I44 → **I45**). You are an event loop, **NOT** a code writer: you dispatch DAGs, read
machine/review verdicts, gate, merge, and schedule — **P1: you never write, edit, patch, rebase, or relock code,
even to remediate; every engineering act (including a `Cargo.lock` relock/rebase) is a forked `swe-coder` DAG.** Boot
the kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS, domain WORK_SESSION/REVIEW_GATE/DELIVERABLES_GIT/
RETENTION; IMPROVEMENT_REVIEWS only if the board goes thin), publish `thread_evaluation`, then do this iteration's Act.

## Why you woke
I44 **recovered the lost #11 review.** The original `review-ci-actions` DAG was force-marked COMPLETE by a
resume-time subtree-resolution fixpoint ("Bug 5") during whole-OS reconstruction **without producing any verdict**
(no root `SYNTHESIS.md`, no posted review; its `_GLOBAL.md`+subtask were lost). I44 confirmed this read-only, did
**not** land #11 on the phantom "Complete" marker (nothing lands unreviewed), and **re-forked a fresh review DAG
`review-ci-actions-r2`** for PR #21 (my one-fork budget, spent at I44). You woke on I44's bounded pacing wake
(a ~25-min schedule timer OR `review-ci-actions-r2` reaching terminal, whichever fired). I44 summary:
- **Recon (read-only, P1):** `review-ci-actions` had NO root `SYNTHESIS.md`; scheduler log showed
  `Complete(success:true)` "all tasks reached terminal state during resume-time subtree-resolution fixpoint
  (Bug 5)" at 2026-10-08T01:27:56Z — a reconstruction force-complete, not a real fold. PR #21 had **zero** reviews.
  So #11 is machine-PASS but UNREVIEWED.
- **Live GitHub re-poll:** `main @ 61f924afa`; PR #21 (#11 ci-actions) **OPEN/MERGEABLE/CLEAN**, head `c8123376`;
  issue #11 OPEN; no `Cargo.lock` restale.
- **Re-forked `review-ci-actions-r2`** (workspace `taskflow/dags/review-ci-actions-r2/`) — fresh #11 review,
  brief carries the CI/supply-chain/testing/image-job concerns + issue #11 acceptance + the note that #12's
  `Dockerfile` has LANDED (so the `image` job now takes its real build+push path, not the skip path). DAG loads
  its own methodology. **One-fork budget spent (I44).**
- The defunct empty `review-ci-actions` DAG is superseded; it carries `reap-whole-after-land` and will be reaped
  when #11 lands (the app never deletes artifacts itself).

## Carried state (read first)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I44/project_state.json` — the persisted STATE
  (`current_pointer=8`; 8 landed items #4–#10, #12; app layer + #10 infra + #12 image complete; **#11 folded
  machine-PASS, review re-forked as `review-ci-actions-r2` after the original review was lost to Bug 5**; #13
  UNBLOCKED, gated by #24/#23; follow-ups #23/#24/#25 on board). Read it; update/append and write your updated copy
  to `taskflow/overseer/I45/project_state.json`.
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I44/CONTINUE.md` — I44's terminal record.
- DAG to watch (gate on the **root `SYNTHESIS.md`** body, never a side-effect — gotcha (g)/(i)):
  - `taskflow/dags/review-ci-actions-r2/` — **#11 review** (forked I44). Its verdict (APPROVE / REQUEST-CHANGES) is
    the authoritative landing verdict for PR #21. On this wake, **check advancing-vs-stale** (compare its file
    mtimes to a FRESH `date -u`; `scheduler/` shows progress). If it has NOT progressed since dispatch past the
    bounded interval of **live-OS** time, treat it as frozen and RECOVER (re-fork carrying its brief forward, or
    synthesize-what-exists) — do NOT wait again unbounded. **Watch for the Bug-5 pattern:** a `scheduler` log
    `Complete` with NO root `SYNTHESIS.md` is NOT a verdict — do not land on it; re-fork.

## This iteration's turn
1. **Reconnoiter (read-only; P1 — no build re-run, no code/lockfile touched).** Has `review-ci-actions-r2` folded
   its root `SYNTHESIS.md` (APPROVE/REQUEST-CHANGES with a real body)? Advancing or frozen? **Re-poll PR #21
   mergeability past UNKNOWN** (`gh pr view 21 -R Nousix-LLC/nswe-demo --json state,mergeable,mergeStateStatus,headRefOid`).
   Confirm `main` (expect `61f924afa` unless something landed). Local-time = **UTC−7**.
2. **Gate + LAND (finish in-flight work first). Nothing lands unreviewed** (REVIEW_GATE).
   - **`review-ci-actions-r2` folded APPROVE (real `SYNTHESIS.md` body) + PR #21 `OPEN/MERGEABLE/CLEAN`** →
     **LAND #11** (`gh pr merge 21 -R Nousix-LLC/nswe-demo --squash --delete-branch`), set issue #11 project Status
     **Done** (item id `PVTI_lADOEB9jls4BlZH4zg-BHZw`), append `work_items[]`, bump `current_pointer` to 9, reap
     `ci-actions` + both review DAGs (`review-ci-actions` defunct + `review-ci-actions-r2`) whole. File the
     review's non-blocking findings as backlog issues (epic #3) if the DAG did not. **Never land on UNKNOWN or
     CONFLICTING.** After the land, re-poll any open sibling for a base/`Cargo.lock` restale — relock any genuine
     CONFLICTING loser via a forked DAG, never inline (P1). (After #11 lands, ALL devops PRs except #13 are merged.)
   - **`review-ci-actions-r2` folded REQUEST-CHANGES** → fork ONE fresh remediation DAG for #11 carrying the review
     findings + prior diff (PR #21 head `c8123376`) + acceptance criteria (budget 2 remediation DAGs per item,
     then escalate). Never inline (P1). Each remediation re-enters at the machine gate.
   - **not folded yet / frozen / Bug-5 empty-complete** → if advancing, keep pacing (schedule I46, self-suspend
     bounded). If **frozen** (no progress past a bounded interval of live-OS time) or **force-completed with no
     `SYNTHESIS.md`**, RECOVER: re-fork the #11 review carrying its brief forward (this is your one fork); do not
     wait again unbounded.
3. **Ordering / what to fork next (one fork per iteration, dependency-ordered).** Finish in-flight work first:
   unblock a landing > review a fold > remediate > new work. Ladder: priority-1 relock → priority-2 review (none
   pending once #11 is under review) → priority-3 remediation (within budget) → priority-4 newly-unblocked new work
   (**#13 deploy-argocd**, UNBLOCKED).
   - **A land is NOT a fork.** If #11 is landable this iteration, LAND #11 first, then your one fork is **#13
     deploy-argocd** (unless a higher-ladder relock/remediation fires).
   - **#13 deploy-argocd** — `deploy/` k8s manifests (Namespace/Deployment/Service/Ingress) + an ArgoCD
     `Application` tracking this repo so chirp auto-syncs to the k3s cluster; resource limits,
     liveness/readiness probes; the app must be **reachable**. UNBLOCKED (#10 infra + #12 image both on `main`).
     **#13's brief MUST account for issue #24** (scope the ArgoCD `application-controller` ClusterRole off
     `*/*/*`, digest-pin manifests/images, survive `--force-conflicts` — harden before the first `Application`).
     NOTE: the live cluster is **k3d-hosted k3s**; the native systemd path is unproven (issue #23). If a
     **reachable** deploy needs a durable/privileged cluster the sandbox k3d does not provide, **weigh escalating
     to the user before #13** (HSO-1/GATE-1).
   Each item is an ordinary forked `swe-coder` DAG with its own issue, branch `work/<slug>`, PR into `main`, and
   root `SYNTHESIS.md`; brief names concerns (describe, don't instruct; DAG loads its own methodologies; don't
   carry a prior DAG's selection forward). **One `engine_fork` per iteration.**
4. **On each successful LAND:** set that issue's project Status to **Done** (project `PVT_kwDOEB9jls4BlZH4`, Status
   field `PVTSSF_lADOEB9jls4BlZH4zhkGLsc`, option Done=`98236657`; item ids in STATE `engagement.project_item_ids` —
   #11=`PVTI_lADOEB9jls4BlZH4zg-BHZw`, #13=`PVTI_lADOEB9jls4BlZH4zg-BHcE`). Assign the issue to `@mattsmcknight`
   when its DAG is dispatched (In Progress=`47fc9ee4`). Append a `work_items[]` entry; bump `current_pointer`. Reap
   the landed item's DAGs (code + review + any remediation) whole (scratch).
5. **The recurring lockfile-restale pattern (carry forward).** Every land to `main` moves the base and MAY restale
   the `Cargo.lock` of a still-open sibling PR that branched earlier **and whose lockfile change overlaps** (confirm
   via the live `gh` mergeability poll, not assumption). After #11 lands there are no open sibling PRs until #13
   opens one, so restale risk is nil this turn; still confirm live. Relock any genuine CONFLICTING loser via a
   forked DAG, never inline (P1).
6. **Schedule your own successor** (I46) `depends_on` I45 (plain id `I46`, `dependencies: ["I45"]` — NOT
   `overseer/I46`), author your terminal record, and continue the chain (`thread_evaluation: Continue`). Self-suspend
   on a BOUNDED wake (any_of: a schedule `resume_at` ~20–30 min out **AND** forked-thread-completion on the DAG you
   are pacing) so you re-evaluate whether it stalls or completes — never an unbounded single wait. Keep the chain
   going until the whole engagement (app built + tested + CI green + containerized + deployed on k3s via ArgoCD,
   reachable, everything merged, board all Done) is delivered — only then `Exit`.

## _FORK.md / fork gotchas (learned in I1–I44)
- (a) Create the DAG/overseer workspace directory on the real filesystem BEFORE authoring files into it (Write fails
  silently if the parent dir is absent).
- (b) `_FORK.md` `launch_context` carries only identity context (`application: software`, `model_default`).
  Methodology direction belongs in the forked DAG's `_BRIEF.md` (name the concerns to cover; the DAG loads its own
  methodologies). Do not copy an earlier DAG's methodology choice.
- (c) `disposition` MUST contain the substring `retain` ONLY for things to keep; a code/review/relock/devops DAG is
  scratch so it uses `reap-whole-after-land` (non-retain).
- (d) **One `engine_fork` per overseer iteration.** `PermissionDenied: missing token 'fork'` for all but the first is
  non-retryable — fork exactly one DAG; hand the rest to successors. (A resumed/reconstructed iteration shares the
  original iteration's spent fork token — if a prior instance of this same Iₙ already forked, do NOT fork again.)
- (d2) **This runtime's `fork` requires:** (i) a non-empty **`launch_agent`** ARGUMENT on the `fork` call itself
  (`launch_agent: "swe-coder"`), and (ii) a `_FORK.md` with **flat machine-readable keys**, including a required
  **`owner_id`** — use exactly this accepted schema:
  ```
  owner_id: overseer/I45
  observation_seam: <abs path>/SYNTHESIS.md
  disposition: reap-whole-after-land
  launch_agent: swe-coder
  launch_kernel: inherit
  thread_type: dag
  launch_context: { application: software, model_default: claude-opus-4-8 }
  ```
  A `fork` returning `InvalidArguments` (missing launch_agent / missing `owner_id`) is fixed and re-called — distinct
  from the non-retryable `PermissionDenied` 'missing token fork'.
- (e) The successor-task `engine_amend_plan { add_task }` uses a PLAIN id (`I46`) with `dependencies: ["I45"]` — NOT
  `overseer/I46`/`overseer/I45` (rejected as unresolved/cycle). Chain edge is `I46: [I45]`.
- (f) **Re-poll `gh` mergeability until it is not UNKNOWN before landing.** NEVER land on UNKNOWN; NEVER land
  CONFLICTING.
- (g) **Gate on the folded root `SYNTHESIS.md` verdict body, not on a side-effect** (a pushed branch, a posted
  review, a subtask marker, or a scheduler `Complete` log). A root record may also be an interim (non-terminal)
  record — read its body, not mere existence.
- (h) A code/relock DAG self-remediating internally is NOT a machine-FAIL you must act on (read the authoritative
  root record).
- (i) **Bug-5 reconstruction force-complete:** on a whole-OS reconstruct, a RUNNING decomposed DAG can be
  force-marked `Complete(success:true)` by a resume-time subtree-resolution fixpoint while its decomposition
  artifacts are LOST and it produced NO root `SYNTHESIS.md`. This is NOT a verdict and NOT a fold — do not land on
  it; re-fork a fresh review/code DAG carrying the brief forward (this happened to `review-ci-actions` → I44 forked
  `review-ci-actions-r2`).
- (j) **Reconstructed/resumed node:** judge advancing-vs-frozen by comparing a DAG's file mtimes to a FRESH
  `date -u`, not to a stale record wall-clock. A long dormant gap (whole-OS dormancy) is not itself a stall. Re-verify
  any land/fork a prior instance of this iteration claims (`gh`/filesystem) before repeating it — never double-land
  or double-fork.
- GRANTED+SUCCEEDED forks: I8 (#6), I9 (#7), I11 (#5 review), I12 (#6 review), I14 (#7 review), I15 (#6 relock),
  I16 (#8 chirp-server), I17 (#9 chirp-frontend), I29 (#9 review), I33 (#8 review), I36 (#8 relock), I38 (#10
  infra-bootstrap), I39 (#11 ci-actions), I40 (#12 containerize), I41 (#10 review), I42 (#12 review
  `review-containerize`), I43 (#11 review `review-ci-actions` — lost to Bug 5), **I44 (#11 review re-fork
  `review-ci-actions-r2`)**. No fork to make: I10, I13, I18–I28, I30–I32, I34, I35, I37.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s (k3d-hosted) cluster/namespaces + its ArgoCD. Never force-push
`main`; never rewrite merged history. Changes land as PRs; reviews, devops, bug-fixes, and lockfile relocks/rebases
are each their own forked DAG; bugs/findings are filed as issues. The GitHub Project/issues/PRs are the source-of-truth
working record — keep them current. Drive to: the app running on k3s and reachable, CI green, everything merged, board
Done. **The app layer + #10 infra + #12 image are COMPLETE; #11 ci-actions folded machine-PASS awaiting review+land
(`review-ci-actions-r2` dispatched after the original review was lost to Bug 5, PR #21 CLEAN); #13 deploy-argocd
UNBLOCKED, gated by #24/#23.** Tracked follow-ups: #23 (native-path harden), #24 (ArgoCD RBAC/supply-chain, pre-#13),
#25 (#12 non-blocking polish). Every devops DAG that opens a PR gets a **review DAG** before it lands (nothing lands
unreviewed).
