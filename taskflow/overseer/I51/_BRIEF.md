# _BRIEF.md — NSWE overseer iteration I51 (persona swe-lead)
**Depends on**: I50

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the project thread
(chain link I49 → I50 → **I51**). You are an event loop, **NOT** a code writer — **P1: you never write, edit,
patch, rebase, or relock code, even to remediate; every engineering act is a forked `swe-coder` DAG.** Boot the
kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS; domain WORK_SESSION/REVIEW_GATE/DELIVERABLES_GIT/
RETENTION, plus IMPROVEMENT_REVIEWS only if you commission one), publish `thread_evaluation`, then do this
iteration's Act.

## Why you woke
I50 routed the #13 review APPROVE verdict and **LANDED PR #28** — the engagement's **last build item**. Both
ROOT gates were re-verified (machine `deploy-argocd/SYNTHESIS.md` PASS 8/8; review `review-deploy-argocd/SYNTHESIS.md`
APPROVE, 0 blockers, 6 non-blockers F1–F6). Squash-merged `22d2df6` + deleted `work/deploy-argocd`; `#13`
auto-closed; board #13→Done, PR #28→Done. **#26 CLOSED** (review-visibility directive demonstrated on PR #28:
board + PR comment + inline F1/F3/F4 + backlog #29). I50 did **NOT** fork — its token is unspent. **You (I51)
hold your own fresh fork token** (one `engine_fork`) for a post-merge devops DAG if the app regressed.

**All build items #4–#13 are now merged on `main @ 22d2df6`.** Remaining open = follow-ups/backlog only.

## This iteration's goal: VERIFY POST-MERGE REACHABILITY FIRST, then triage backlog and decide Exit
Driven by the bounded re-evaluate-then-act cadence (thread header). The **open risk** is the Exit criterion
"app on k3s reachable": #28's merge triggers ArgoCD `automated` sync (prune+selfHeal), which applies the
**committed private-GHCR digest** `@sha256:054af27…`. In-sandbox reachability used a `chirp:local` override
patch; selfHeal may revert it. Absent a `ghcr-pull` dockerconfigjson secret in ns `chirp` (or a public package),
the pod will **ImagePullBackOff** and the app can regress from reachable (review finding **F1**, issue **#29**).

1. **Board check (read-only; P1).** Fresh `date -u`. Confirm `main @ 22d2df6`; confirm no open PRs; read the
   board for any new issues/comments/reviews since I50 (route new requests through intake, WORK_SESSION). #13
   CLOSED, #26 CLOSED. Open backlog: #29, #27, #25, #24, #23 (+ epics #1/#2/#3).
2. **Verify post-merge deploy state (the critical check — this drives everything).** Read-only `kubectl`/`curl`
   against the live k3d `nswe` cluster (context `k3d-nswe`), read-only only (P1):
   - ArgoCD Application `chirp`: does it flip **Healthy + Synced** (F2 resolves on merge), adopting the
     previously-orphaned directly-applied objects?
   - Pod: does it pull the **committed** digest and run `1/1 Running`, or **ImagePullBackOff** (F1)?
   - Reachability: `GET /healthz` via Traefik (`Host: chirp.localhost` → `localhost:8081`) → **200**?
3. **Route on what you find:**
   - **App Healthy/Synced + reachable** → the engagement end-state holds. Mark F2 resolved on #29. Proceed to
     backlog triage (step 4).
   - **App regressed (ImagePullBackOff / sync failure — F1)** → this is a **devops work-item**, so **fork one
     `swe-coder` DAG** (your fresh token; gotcha d/d2) whose brief = provision `ghcr-pull` (a dockerconfigjson
     Secret in ns `chirp` from a token with `read:packages`) **or** make the GHCR `chirp-server` package public,
     then verify the pod pulls `@sha256:054af27…` directly and the Application reaches **Synced + reachable**.
     Describe the objective/acceptance/scope/inputs (F1 on #29, the deploy manifests, the private-GHCR
     constraint); do not prescribe method or methodology. Pace it on a bounded any_of wake (schedule ~20–30m
     AND forked-thread-completion). Re-enter at the machine gate on fold; **budget 2** such DAGs, then escalate
     to the user. **Never an inline fix** — provisioning a cluster secret is a DAG, not overseer work.
4. **Triage the backlog (groom priority; `DELIVERABLES_GIT`/`IMPROVEMENT_REVIEWS`).** Place/confirm priority
   order of the open follow-ups as backlog: **#29 F1 first** (if not already resolved in step 3), then
   #24 (deeper least-privilege/supply-chain), #23 (native k3s path), #25 (containerize polish), #27 (CI
   PR-body hygiene), and #29 F3–F5 polish. These are backlog work, not blockers to engagement completion.
5. **Exit decision (step 3 of I50's brief, now yours).** The engagement is done when **app on k3s reachable +
   CI green + everything merged + the board all Done** (all build items merged ✓; follow-ups #23/#24/#25/#27/#29
   triaged/closed or **placed as backlog** — placed-as-backlog counts). If post-merge reachability holds and the
   follow-ups are placed/triaged as backlog → evaluate **`Exit`** (write `COMPLETE.md` at the thread root; the
   project remains a kept save, resumable by `open project`, with its backlog). If reachability is still being
   recovered (a devops DAG in flight) or new work arrived → schedule successor **I52** `depends_on` I51
   (plain id `I52`, `dependencies: ["I51"]` — gotcha e), author your terminal record, and continue the chain.

## Carried state (read first)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I50/project_state.json` — the persisted STATE (#13
  landed; `turn_pointer.open_risk` = post-merge reachability unverified; `awaiting` = this iteration's plan).
  Read it; update/append and write your own copy to `taskflow/overseer/I51/project_state.json`.
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I50/CONTINUE.md` — I50's terminal record.
- `/home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-argocd/SYNTHESIS.md` — the #13 machine verdict
  (PASS; Q1 image-pull + Q2 sync-deferred qualifiers explain the post-merge checks to make).
- `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-deploy-argocd/SYNTHESIS.md` — the review verdict
  (APPROVE; F1–F6 detail and the post-merge verification F1/F2 recommend).

## Gotchas (learned I1–I50) — carry forward
- (a) Create a DAG/overseer workspace dir on the real FS BEFORE authoring files into it (Write fails silently if
  the parent dir is absent).
- (d) **One `engine_fork` per iteration**; `PermissionDenied: missing token 'fork'` is non-retryable. A
  resumed/reconstructed iteration SHARES the original's spent token — check your own I51 dir for a prior
  SUSPENSION.md/CONTINUE.md/project_state.json FIRST; if a prior instance already forked, do NOT re-fork.
- (d2) `fork` requires a non-empty `launch_agent: "swe-coder"` ARGUMENT **and** a `_FORK.md` with flat keys incl.
  `owner_id: overseer/I51`, `observation_seam: <abs>/SYNTHESIS.md`, `disposition: reap-whole-after-land`,
  `launch_agent: swe-coder`, `launch_kernel: inherit`, `thread_type: dag`,
  `launch_context: { application: software, model_default: claude-opus-4-8 }`.
- (e) Successor `add_task` uses PLAIN id (`I52`) with `dependencies: ["I51"]` — never `overseer/I52`.
- (f) Re-poll `gh` mergeability until not UNKNOWN before any land; never land UNKNOWN/CONFLICTING. (No land is
  pending this iteration unless a post-merge remediation produces a new PR.)
- (g) Gate on a folded ROOT `SYNTHESIS.md` body, never a side-effect. (i) Bug-5: a reconstruct can force-complete
  a RUNNING DAG with NO root `SYNTHESIS.md` — re-fork a fresh slug. (j) Judge advancing-vs-frozen vs a FRESH
  clock; a long dormancy gap is not a stall; re-verify any land/fork a prior instance claims before repeating it.
- (gh-self-review) `gh pr review --approve` is rejected when the PR author == authenticated account; a review
  DAG's `SYNTHESIS.md` body is the authoritative verdict, posted additionally as a PR comment (#26 pattern).
- GRANTED+SUCCEEDED forks through I50: I8,I9,I11,I12,I14,I15,I16,I17,I29,I33,I36,I38,I39,I40,I41,I42,I43,I44,
  I45,I46,I48 (deploy-argocd #13), I49 (review-deploy-argocd #13 review). No fork: I10,I13,I18–I28,I30–I32,
  I34,I35,I37,I47,**I50** (landed on APPROVE; no fork needed).

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s (k3d-hosted) cluster/namespaces + its ArgoCD. Never force-push
`main`; never rewrite merged history; add no attribution trailers to commits or PR bodies (the engagement forbids
them — #27/HYG-1). Changes land as PRs; reviews, devops, bug-fixes, remediations, relocks are each their own
forked DAG; bugs/findings are filed as issues. Keep the GitHub Project/issues/PRs current. Drive to: the app
running on k3s and reachable, CI green, everything merged, board all Done — **then `Exit`**. **All build items
#4–#13 are merged on `main @ 22d2df6`; the only thing between here and `Exit` is confirming post-merge
reachability holds (recover F1 via a devops DAG if it regressed) and the follow-ups #23/#24/#25/#27/#29 are
placed as backlog.**
