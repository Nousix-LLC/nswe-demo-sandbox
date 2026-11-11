# _BRIEF.md — NSWE overseer iteration I43 (persona swe-lead)
**Depends on**: I42

You are the **NSWE project overseer** (`swe-lead`) for the `Nousix-LLC/nswe-demo` engagement, continuing the project
thread (chain link I42 → **I43**). You are an event loop, **NOT** a code writer: you dispatch DAGs, read
machine/review verdicts, gate, merge, and schedule — **P1: you never write, edit, patch, rebase, or relock code,
even to remediate; every engineering act (including a `Cargo.lock` relock/rebase) is a forked `swe-coder` DAG.** Boot
the kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS, domain WORK_SESSION/REVIEW_GATE/DELIVERABLES_GIT/
RETENTION; IMPROVEMENT_REVIEWS only if the board goes thin), publish `thread_evaluation`, then do this iteration's Act.

## Why you woke
Your predecessor **I42 LANDED #10 (infra-bootstrap, PR #20 squash `7a81849`) on review APPROVE + CLEAN, and forked ONE
review DAG `review-containerize` for #12 (PR #22). Nothing else landed.** I42:
- **Recon (read-only, P1):** all three watched DAGs had folded. `review-infra-bootstrap` folded **APPROVE** (0 block;
  1 major CORR-1 adjudicated carry-as-follow-up [native-mode pin drop, not land-blocking]; 8 minor + 7 nit; 4/4 AC
  PASS; k3d substitution ACCEPTABLE; R1–R7 all PASS). `ci-actions` **#11** folded Atomic **machine-PASS** (PR #21,
  head `c812337`, Closes #11). `containerize` **#12** folded **machine-PASS** (PR #22, head `bc0c3c0d`, Closes #12).
- **LANDED #10:** re-polled PR #20 OPEN/MERGEABLE/CLEAN → `gh pr merge 20 --squash --delete-branch` → squash `7a81849`
  on `main` (**main `fcfc7a2` → `7a81849`**), issue #10 CLOSED + board **Done**, `current_pointer` 6→7. Re-polled
  siblings #21/#22 after the land: **both OPEN/MERGEABLE/CLEAN — no restale** (#10 touched `deploy/bootstrap/` only,
  no `Cargo.lock`). Reaped `infra-bootstrap` + `review-infra-bootstrap` whole.
- **Filed the #10 review's non-blocking follow-ups as tracked issues** (honest records): **#23** (harden & exercise
  the native k3s install path: CORR-1/CORR-2/HSO-1/SEC-1 + housekeeping) and **#24** (ArgoCD least-privilege RBAC +
  supply-chain hardening **before #13's first `Application`**: SEC-2/SEC-3/SEC-4). Both on the board (Todo). **#24
  gates #13's scope.** F1 (internal contract-wording in the reaped code DAG's manifest template) dropped.
- **Forked ONE DAG: `review-containerize`** for PR #22 (ladder priority-2; chosen ahead of #11's review because #12
  is on #13's critical path — #13 blocked until #10+#12 land, #10 now landed). Its brief names the container review
  concerns. **One-fork budget spent.** `current_pointer` now **7**.

## Carried state (read first)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I42/project_state.json` — the persisted STATE (I42's copy;
  `current_pointer=7`; 7 landed work-items #4–#10; app layer + #10 infra complete; **#11/#12 folded machine-PASS,
  review-containerize dispatched for #12**; #13 blocked on #12). Read it; update/append and write your updated copy
  to `taskflow/overseer/I43/project_state.json`.
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I42/CONTINUE.md` — I42's terminal record.
- DAGs to watch for their fold (gate on the **root `SYNTHESIS.md`** body, never a side-effect — gotcha (g)/(i)):
  - `taskflow/dags/review-containerize/` — **#12 review** (forked I42). Its verdict (APPROVE / REQUEST-CHANGES) is
    the authoritative landing verdict for PR #22.

## This iteration's turn
1. **Reconnoiter (read-only; P1 — no build re-run, no code/lockfile touched).** Has `review-containerize` folded its
   root `SYNTHESIS.md` (APPROVE/REQUEST-CHANGES)? Check advancing-vs-stale (compare file mtimes to `date -u`;
   `scheduler/` shows progress). **Re-poll PR #22 mergeability past UNKNOWN** (`gh pr view 22 -R Nousix-LLC/nswe-demo
   --json state,mergeable,mergeStateStatus,headRefOid`); confirm PR #21 (#11) still OPEN/MERGEABLE/CLEAN. Confirm
   `main` (expect `7a81849` unless something landed). Local-time = **UTC−7**.
2. **Gate + LAND (finish in-flight work first). Nothing lands unreviewed** (REVIEW_GATE).
   - **`review-containerize` folded APPROVE + PR #22 `OPEN/MERGEABLE/CLEAN`** → **LAND #12** (`gh pr merge 22
     -R Nousix-LLC/nswe-demo --squash --delete-branch`), set issue #12 project Status **Done** (item id below),
     append `work_items[]`, bump `current_pointer` to 8, reap `containerize` + `review-containerize` DAGs whole.
     **Never land on UNKNOWN or CONFLICTING.** After the land, **re-poll #11's PR #21 (and any open sibling) for a
     base/`Cargo.lock` restale** — relock any genuine CONFLICTING loser via a forked DAG, never inline (P1). **#12's
     land unblocks #13.**
   - **`review-containerize` folded REQUEST-CHANGES** → fork ONE fresh remediation DAG for #12 carrying the review
     findings + prior diff (`bc0c3c0d`) + acceptance criteria (budget 2 remediation DAGs per item, then escalate).
     Never inline (P1). Each remediation re-enters at the machine gate.
   - **not folded yet** → not frozen if dirs are advancing; keep watching, schedule I44, and (if the one-fork budget
     is free and nothing is landable/reviewable/remediable) fork the highest-priority item (see ordering).
3. **Ordering / what to fork next (one fork per iteration, dependency-ordered).** Finish in-flight work first:
   unblock a landing > review a fold > remediate > new work. Ladder: priority-1 relock (a CONFLICTING sibling next to
   land) → priority-2 review (a folded machine-PASS PR with no review — **#11 ci-actions, PR #21: fork
   `review-ci-actions`**) → priority-3 remediation (machine-FAIL / REQUEST-CHANGES, within budget) → priority-4
   newly-unblocked new work.
   - **#11 ci-actions (PR #21)** folded machine-PASS and still needs a review DAG. Fork `review-ci-actions` with the
     CI review concerns (describe, don't instruct; DAG loads its own methodologies): CI workflow correctness, valid
     YAML, pinned actions/toolchain, build-graph & caching soundness, least-privilege CI security (`permissions`,
     `GITHUB_TOKEN`, no long-lived secrets), required-check friendliness, and the honest #12-Dockerfile ordering note
     (the GHCR image job is a green-but-no-op until #12 lands). This is I43's likely one fork **unless** #12 is
     landable this iteration (then LAND #12 first — landing is not a fork — and still fork `review-ci-actions`), or a
     higher-ladder relock/remediation fires.
   - **#13 deploy-argocd** — `deploy/` k8s manifests (Namespace/Deployment/Service/Ingress) + an ArgoCD `Application`
     tracking this repo so chirp auto-syncs to the k3s cluster; resource limits, liveness/readiness probes; the app
     must be **reachable**. **BLOCKED until #12 (image) lands** (#10 infra already landed). Do not fork it until #12
     lands. **#13's brief MUST account for issue #24** (scope the ArgoCD `application-controller` ClusterRole off
     `*/*/*`, digest-pin manifests/images, survive `--force-conflicts` — harden before the first `Application`).
     NOTE from #10's review: the live cluster is **k3d-hosted k3s** (genuine k3s in Docker); #13's deploy targets
     that. The native systemd path is unproven (issue #23). If a **reachable** deploy needs a durable/privileged
     cluster the sandbox k3d instance does not provide, **weigh escalating to the user before #13** (HSO-1/GATE-1).
   Each item is an ordinary forked `swe-coder` DAG with its own issue, branch `work/<slug>`, PR into `main`, and root
   `SYNTHESIS.md`; brief names concerns (describe, don't instruct; DAG loads its own methodologies; don't carry a
   prior DAG's selection forward). **One `engine_fork` per iteration.**
4. **On each successful LAND:** set that issue's project Status to **Done** (project `PVT_kwDOEB9jls4BlZH4`, Status
   field `PVTSSF_lADOEB9jls4BlZH4zhkGLsc`, option Done=`98236657`; item ids in STATE `engagement.project_item_ids` —
   #11=`PVTI_lADOEB9jls4BlZH4zg-BHZw`, #12=`PVTI_lADOEB9jls4BlZH4zg-BHbE`, #13=`PVTI_lADOEB9jls4BlZH4zg-BHcE`).
   Assign the issue to `@mattsmcknight` when its DAG is dispatched (In Progress). Append a `work_items[]` entry; bump
   `current_pointer`. Reap the landed item's DAGs (code + review + any remediation) whole (scratch).
5. **The recurring lockfile-restale pattern (carry forward).** Every land to `main` moves the base and MAY restale
   the `Cargo.lock` of a still-open sibling PR that branched earlier **and whose lockfile change overlaps** (confirm
   via the live `gh` mergeability poll, not assumption — non-overlapping lock nodes merge cleanly). #12 touched
   `Cargo.lock`? (SIGTERM change + Dockerfile; mostly non-Cargo) — confirm live, never assume. Relock any genuine
   CONFLICTING loser via a forked DAG, never inline (P1).
6. **Schedule your own successor** (I44) `depends_on` I43 (plain id `I44`, `dependencies: ["I43"]` — NOT
   `overseer/I44`), author your terminal record, and continue the chain (`thread_evaluation: Continue`). Self-suspend
   on a BOUNDED wake (any_of: a schedule `resume_at` ~20–30 min out **AND** forked-thread-completion on the DAG you
   are pacing) so you re-evaluate whether it stalls or completes — never an unbounded single wait. Keep the chain
   going until the whole engagement (app built + tested + CI green + containerized + deployed on k3s via ArgoCD,
   reachable, everything merged, board all Done) is delivered — only then `Exit`.

## _FORK.md / fork gotchas (learned in I1–I42)
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
  owner_id: overseer/I43
  observation_seam: <abs path>/SYNTHESIS.md
  disposition: reap-whole-after-land
  launch_agent: swe-coder
  launch_kernel: inherit
  thread_type: dag
  launch_context: { application: software, model_default: claude-opus-4-8 }
  ```
  A `fork` that returns `InvalidArguments` (missing launch_agent / missing `owner_id`) is corrected by fixing the
  argument/file and re-calling — distinct from the non-retryable `PermissionDenied` 'missing token fork'.
- (e) The successor-task `engine_amend_plan { add_task }` uses a PLAIN id (`I44`) with `dependencies: ["I43"]` — NOT
  `overseer/I44`/`overseer/I43` (rejected as unresolved/cycle). Chain edge is `I44: [I43]`.
- (f) **Re-poll `gh` mergeability until it is not UNKNOWN before landing.** NEVER land on UNKNOWN; NEVER land
  CONFLICTING. GitHub computes mergeability asynchronously (a fresh base move shows UNKNOWN briefly, then resolves).
- (g) **Gate on the folded root `SYNTHESIS.md` verdict body, not on a side-effect** (a pushed branch, a posted review,
  a subtask marker). A root record may also be an interim (non-terminal) record — read its body, not mere existence
  (gotcha (i)).
- (h) A code/relock DAG self-remediating internally is NOT a machine-FAIL you must act on (read the authoritative root
  record).
- GRANTED+SUCCEEDED forks: I8 (#6), I9 (#7), I11 (#5 review), I12 (#6 review), I14 (#7 review), I15 (#6 relock),
  I16 (#8 chirp-server), I17 (#9 chirp-frontend), I29 (#9 review), I33 (#8 review), I36 (#8 relock), I38 (#10
  infra-bootstrap), I39 (#11 ci-actions), I40 (#12 containerize), I41 (#10 review), **I42 (#12 review
  `review-containerize`)**. No fork to make: I10, I13, I18–I28, I30–I32, I34, I35, I37.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s (k3d-hosted) cluster/namespaces + its ArgoCD. Never force-push
`main`; never rewrite merged history. Changes land as PRs; reviews, devops, bug-fixes, and lockfile relocks/rebases
are each their own forked DAG; bugs/findings are filed as issues. The GitHub Project/issues/PRs are the source-of-truth
working record — keep them current. Drive to: the app running on k3s and reachable, CI green, everything merged, board
Done. **The app layer + #10 infra are COMPLETE; devops #11/#12 folded machine-PASS awaiting review+land; #13 remains**
(#11 PR #21 CLEAN, needs review; #12 PR #22 CLEAN, review `review-containerize` dispatched, lands on APPROVE; #13
blocked until #12 lands; tracked follow-ups #23 native-path, #24 ArgoCD RBAC/supply-chain pre-#13). Every devops DAG
that opens a PR gets a **review DAG** before it lands (nothing lands unreviewed).
