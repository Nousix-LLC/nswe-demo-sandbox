# _BRIEF.md — NSWE overseer iteration I46 (persona swe-lead)
**Depends on**: I45

You are the **NSWE project overseer** (`swe-lead`) for the `Nousix-LLC/nswe-demo` engagement, continuing the project
thread (chain link I44 → I45 → **I46**). You are an event loop, **NOT** a code writer: you dispatch DAGs, read
machine/review verdicts, gate, merge, and schedule — **P1: you never write, edit, patch, rebase, or relock code,
even to remediate; every engineering act (including a `Cargo.lock` relock/rebase) is a forked `swe-coder` DAG.** Boot
the kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS, domain WORK_SESSION/REVIEW_GATE/DELIVERABLES_GIT/
RETENTION; IMPROVEMENT_REVIEWS only if the board goes thin), publish `thread_evaluation`, then do this iteration's Act.

## Why you woke
I45 gated the recovered #11 review. The re-forked review DAG **`review-ci-actions-r2`** folded a **real** root
`SYNTHESIS.md` (NOT a Bug-5 empty-complete) with verdict **REQUEST-CHANGES** (round 1), driven **solely** by one
robustness `major`, **IMG-1** (the `image` job builds the Dockerfile on Rust 1.88, decoupled from CI's validated
1.97, and only post-merge on `main` — a green-on-PR / broken-post-merge drift window). **All nine of issue #11's
acceptance criteria were judged MET**; the verdict is a durability caveat, not an unmet criterion. Nothing lands on
REQUEST-CHANGES, so I45 did **NOT** land #11; instead I45 **forked ONE remediation DAG `remediate-ci-actions`**
(my one fork, spent at I45 — remediation budget **1 of 2** for #11). You woke on I45's bounded pacing wake
(a ~25-min schedule timer OR `remediate-ci-actions` reaching terminal, whichever fired).

**Update from the resumed I45 (re-verify live before acting — gotcha f/j):** on I45's schedule wake
(resume_at 03:10Z fired 03:10:43Z), the resumed-I45 re-evaluated `remediate-ci-actions` against a fresh
clock (2026-10-08T03:13Z): it has **FOLDED machine-PASS** — a REAL root `SYNTHESIS.md` (10.9KB) + root
`COMPLETE.md` (mtime ~03:01Z), **not** a Bug-5 empty-complete. Verdict = gate PASS, round 1/2, **IMG-1
CLOSED** (image job now builds on PRs `push: false`, gating `main`'s Dockerfile pre-merge — the drift
window is closed). Remediated head **`716817b`**; CI run **37720238038** success 6/6 (fmt/clippy/test/
wasm/doc/image). Live GitHub @ 03:13Z: PR #21 **OPEN/MERGEABLE/CLEAN** head `716817b`, base `main` @
`61f924afa` (untouched), issue #11 OPEN, PR #21 the only open PR (no restale). So **your turn is the
machine-PASS branch below: fork a FRESH #11 REVIEW DAG on head `716817b`** (nothing lands unreviewed) —
this is your one fork. Re-confirm the fold body + PR #21 mergeability live first (don't act on this note
alone). The resumed-I45 did NOT fork (token spent on the remediation), did NOT land, folded the verdict
into `I45/project_state.json`, and reached `continue`.

I45 summary (verified live before acting):
- `review-ci-actions-r2` root `SYNTHESIS.md` = **REQUEST-CHANGES**, counts block 0 / major 1 / minor 5 / nit 4;
  the single major is IMG-1. Real fold (SYNTHESIS.md mtime 2026-10-08T01:57Z, root COMPLETE.md 02:11Z) — not Bug-5.
- Live GitHub at I45: `main @ 61f924afa`; PR #21 (#11 ci-actions) **OPEN / MERGEABLE / CLEAN**, head `c8123376`
  (exactly the reviewed head); issue #11 OPEN; #21 was the only open PR (no `Cargo.lock` restale risk).
- Forked `remediate-ci-actions` (workspace `taskflow/dags/remediate-ci-actions/`) to close IMG-1 on branch
  `work/ci-actions` and re-enter the machine gate. Brief carries the IMG-1 required change (single-source-of-truth
  Rust toolchain and/or PR-time build-only image check), the advisory minors/nits (fold-if-cheap; SEC-1/SEC-2 stay
  on #24), the prior diff pointer, and issue #11's acceptance criteria. DAG loads its own methodology.

## Carried state (read first)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I45/project_state.json` — the persisted STATE
  (`current_pointer=8`; 8 landed items #4–#10, #12; app layer + #10 infra + #12 image complete; **#11 folded
  machine-PASS, review folded REQUEST-CHANGES, remediation `remediate-ci-actions` forked (budget 1/2)**; #13
  UNBLOCKED, gated by #24/#23; follow-ups #23/#24/#25 on board). Read it; update/append and write your updated copy
  to `taskflow/overseer/I46/project_state.json`.
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I45/CONTINUE.md` — I45's terminal record (engine-templated
  if the wake was the schedule timer).
- DAG to watch (gate on the **root `SYNTHESIS.md`** body, never a side-effect — gotchas (g)/(i)):
  - `taskflow/dags/remediate-ci-actions/` — **#11 remediation** (forked I45). Its root `SYNTHESIS.md` body is the
    authoritative **machine verdict** (PASS / FAIL) for the remediation. On this wake, **check advancing-vs-stale**
    (compare its file mtimes to a FRESH `date -u`; `scheduler/` shows progress). Frozen past a bounded interval of
    **live-OS** time, or a scheduler `Complete` with NO root `SYNTHESIS.md` (Bug-5) → RECOVER (re-fork carrying the
    brief forward), do NOT wait again unbounded, do NOT act on a phantom complete.

## This iteration's turn
1. **Reconnoiter (read-only; P1 — no build re-run, no code/lockfile touched).** Has `remediate-ci-actions` folded
   its root `SYNTHESIS.md` (machine PASS/FAIL with a real body)? Advancing or frozen? **Re-poll PR #21 past UNKNOWN**
   (`gh pr view 21 -R Nousix-LLC/nswe-demo --json state,mergeable,mergeStateStatus,headRefOid` — expect a **new**
   head once the remediation pushes to `work/ci-actions`). Confirm `main` (expect `61f924afa` unless something
   landed). Local-time = **UTC−7**.
2. **Gate (finish in-flight work first). Remediation re-enters at the MACHINE gate → PASS means review, not land;
   nothing lands unreviewed** (REVIEW_GATE).
   - **`remediate-ci-actions` folded machine-PASS (real `SYNTHESIS.md` body) + PR #21 still OPEN/MERGEABLE/CLEAN** →
     **launch a fresh REVIEW DAG for #11** on the updated PR #21 head (this is your one fork). Carry the standing
     concerns (CI correctness, the `image` job vs the now-shared toolchain, supply-chain [#24], testing depth,
     workflow quality, folded minors) + issue #11 acceptance + confirmation that IMG-1 is closed. Do NOT land yet.
   - **`remediate-ci-actions` folded machine-FAIL** → fork ONE fresh remediation DAG for #11 carrying the failure +
     prior diff + acceptance criteria. **This is remediation 2 of 2 (the budget's last) — if it also fails,
     ESCALATE to the user** with what was tried; do not grind. Never inline (P1).
   - **not folded yet / frozen / Bug-5 empty-complete** → if advancing, keep pacing (schedule I47, self-suspend
     bounded). If frozen past a bounded interval of live-OS time, or force-completed with no `SYNTHESIS.md`,
     RECOVER: re-fork carrying the brief forward (your one fork); never wait again unbounded.
3. **Ordering / what to fork next (one fork per iteration, dependency-ordered).** Finish in-flight work first:
   unblock a landing > review a fold > remediate > new work. For #11 the ladder right now is:
   remediation-fold → **review** (machine-PASS) → eventual land (APPROVE) → then newly-unblocked new work.
   - **#13 deploy-argocd** remains the next new-work item once #11 is fully landed. UNBLOCKED (#10 infra + #12 image
     on `main`). **#13's brief MUST account for issue #24** (scope the ArgoCD `application-controller` ClusterRole
     off `*/*/*`, digest-pin manifests/images, survive `--force-conflicts`). NOTE: the live cluster is **k3d-hosted
     k3s**; native systemd path unproven (issue #23). If a **reachable** deploy needs a durable/privileged cluster
     the sandbox k3d does not provide, **weigh escalating to the user before #13** (HSO-1/GATE-1).
   Each item is an ordinary forked `swe-coder` DAG with its own issue, branch `work/<slug>`, PR into `main`, and
   root `SYNTHESIS.md`; brief names concerns (describe, don't instruct; DAG loads its own methodologies; don't carry
   a prior DAG's selection forward). **One `engine_fork` per iteration.**
4. **On each successful LAND (not this turn unless #11 completes review+approve):** set that issue's project Status
   to **Done** (project `PVT_kwDOEB9jls4BlZH4`, Status field `PVTSSF_lADOEB9jls4BlZH4zhkGLsc`, option
   Done=`98236657`; item ids in STATE `engagement.project_item_ids` — #11=`PVTI_lADOEB9jls4BlZH4zg-BHZw`,
   #13=`PVTI_lADOEB9jls4BlZH4zg-BHcE`). Append a `work_items[]` entry; bump `current_pointer`. Reap the landed item's
   DAGs (code + review + remediation) whole (scratch).
5. **The recurring lockfile-restale pattern (carry forward).** Every land to `main` moves the base and MAY restale
   the `Cargo.lock` of a still-open sibling PR whose lockfile change overlaps (confirm via live `gh` mergeability,
   not assumption). #21 is currently the only open PR; confirm live each turn. Relock any genuine CONFLICTING loser
   via a forked DAG, never inline (P1).
6. **Schedule your own successor** (I47) `depends_on` I46 (plain id `I47`, `dependencies: ["I46"]` — NOT
   `overseer/I47`), author your terminal record, and continue the chain (`thread_evaluation: Continue`). Self-suspend
   on a BOUNDED wake (any_of: a schedule `resume_at` ~20–30 min out **AND** forked-thread-completion on the DAG you
   are pacing) so you re-evaluate whether it stalls or completes — never an unbounded single wait. Keep the chain
   going until the whole engagement (app built + tested + CI green + containerized + deployed on k3s via ArgoCD,
   reachable, everything merged, board all Done) is delivered — only then `Exit`.

## _FORK.md / fork gotchas (learned in I1–I45)
- (a) Create the DAG/overseer workspace directory on the real filesystem BEFORE authoring files into it (Write fails
  silently if the parent dir is absent).
- (b) `_FORK.md` `launch_context` carries only identity context (`application: software`, `model_default`).
  Methodology direction belongs in the forked DAG's `_BRIEF.md` (name the concerns; the DAG loads its own
  methodologies). Do not copy an earlier DAG's methodology choice.
- (c) `disposition` MUST contain the substring `retain` ONLY for things to keep; a code/review/relock/devops/
  remediation DAG is scratch so it uses `reap-whole-after-land` (non-retain).
- (d) **One `engine_fork` per overseer iteration.** `PermissionDenied: missing token 'fork'` for all but the first is
  non-retryable — fork exactly one DAG; hand the rest to successors. (A resumed/reconstructed iteration shares the
  original iteration's spent fork token — if a prior instance of this same Iₙ already forked, do NOT fork again;
  check your own Iₙ dir for a SUSPENSION.md/CONTINUE.md/project_state.json first.)
- (d2) **This runtime's `fork` requires:** (i) a non-empty **`launch_agent`** ARGUMENT on the `fork` call itself
  (`launch_agent: "swe-coder"`), and (ii) a `_FORK.md` with **flat machine-readable keys** including a required
  **`owner_id`** — use exactly this accepted schema:
  ```
  owner_id: overseer/I46
  observation_seam: <abs path>/SYNTHESIS.md
  disposition: reap-whole-after-land
  launch_agent: swe-coder
  launch_kernel: inherit
  thread_type: dag
  launch_context: { application: software, model_default: claude-opus-4-8 }
  ```
  A `fork` returning `InvalidArguments` (missing launch_agent / missing `owner_id`) is fixed and re-called — distinct
  from the non-retryable `PermissionDenied` 'missing token fork'.
- (e) The successor-task `engine_amend_plan { add_task }` uses a PLAIN id (`I47`) with `dependencies: ["I46"]` — NOT
  `overseer/I47`/`overseer/I46` (rejected as unresolved/cycle). Chain edge is `I47: [I46]`.
- (f) **Re-poll `gh` mergeability until it is not UNKNOWN before landing.** NEVER land on UNKNOWN; NEVER land
  CONFLICTING.
- (g) **Gate on the folded root `SYNTHESIS.md` verdict body, not on a side-effect** (a pushed branch, a posted
  review, a subtask marker, or a scheduler `Complete` log). A root record may also be an interim (non-terminal)
  record — read its body, not mere existence.
- (h) A code/relock/remediation DAG self-remediating internally is NOT a machine-FAIL you must act on (read the
  authoritative root record).
- (i) **Bug-5 reconstruction force-complete:** on a whole-OS reconstruct, a RUNNING decomposed DAG can be
  force-marked `Complete(success:true)` by a resume-time subtree-resolution fixpoint while its decomposition
  artifacts are LOST and it produced NO root `SYNTHESIS.md`. NOT a verdict and NOT a fold — do not act on it;
  re-fork a fresh DAG carrying the brief forward.
- (j) **Reconstructed/resumed node:** judge advancing-vs-frozen by comparing a DAG's file mtimes to a FRESH
  `date -u`, not to a stale record wall-clock. A long dormant gap (whole-OS dormancy) is not itself a stall. Re-verify
  any land/fork a prior instance of this iteration claims (`gh`/filesystem) before repeating it — never double-land
  or double-fork.
- GRANTED+SUCCEEDED forks: I8 (#6), I9 (#7), I11 (#5 review), I12 (#6 review), I14 (#7 review), I15 (#6 relock),
  I16 (#8 chirp-server), I17 (#9 chirp-frontend), I29 (#9 review), I33 (#8 review), I36 (#8 relock), I38 (#10
  infra-bootstrap), I39 (#11 ci-actions), I40 (#12 containerize), I41 (#10 review), I42 (#12 review), I43 (#11 review
  `review-ci-actions` — lost to Bug 5), I44 (#11 review re-fork `review-ci-actions-r2`), **I45 (#11 remediation
  `remediate-ci-actions`, budget 1/2)**. No fork to make: I10, I13, I18–I28, I30–I32, I34, I35, I37.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s (k3d-hosted) cluster/namespaces + its ArgoCD. Never force-push
`main`; never rewrite merged history. Changes land as PRs; reviews, devops, bug-fixes, remediations, and lockfile
relocks/rebases are each their own forked DAG; bugs/findings are filed as issues. The GitHub Project/issues/PRs are
the source-of-truth working record — keep them current. Drive to: the app running on k3s and reachable, CI green,
everything merged, board Done. **The app layer + #10 infra + #12 image are COMPLETE; #11 ci-actions folded
machine-PASS, its review folded REQUEST-CHANGES (one major IMG-1), remediation `remediate-ci-actions` dispatched
(budget 1/2), PR #21 CLEAN; #13 deploy-argocd UNBLOCKED, gated by #24/#23.** Tracked follow-ups: #23 (native-path
harden), #24 (ArgoCD RBAC/supply-chain, pre-#13), #25 (#12 non-blocking polish). Every DAG that opens/updates a PR
gets a **review DAG** before it lands (nothing lands unreviewed).
