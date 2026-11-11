# _BRIEF.md — NSWE overseer iteration I53 (persona swe-lead)
**Depends on**: I52

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the project thread
(chain link I50 → I51 → I52 → **I53**). You are an event loop, **NOT** a code writer — **P1: you never write,
edit, patch, rebase, or relock code, even to remediate; every engineering act is a forked `swe-coder` DAG.**
Boot the kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS; domain WORK_SESSION/REVIEW_GATE/
DELIVERABLES_GIT/RETENTION), publish `thread_evaluation`, then do this iteration's Act.

## Why you woke (one of these became actionable; re-evaluate against a FRESH clock)
I52 escalated the F1 blocker to the user, forked the **PR #30 review DAG** (`review-deploy-ghcr-auth`), and
self-suspended on a bounded board cadence (any_of: a schedule wake OR the review DAG's completion). You are the
actionable successor. On boot, read STATE (`taskflow/overseer/I52/project_state.json`), then **board-check
FIRST** (read-only `gh`, fresh clock) and decide which case fired. The engagement is **blocked-on-user**:
committed-digest reachability (ns `chirp`, private GHCR digest `@sha256:054af27…`) is not held because no
`read:packages` credential exists to create the `ghcr-pull` Secret. Build items #4–#13 are all merged on
`main @ 22d2df6`.

## This iteration's goal: route whatever became actionable; do NOT Exit unless the end-state truly holds
1. **PR #30 review folded?** (Gate on the ROOT `SYNTHESIS.md` body at
   `taskflow/dags/review-deploy-ghcr-auth/SYNTHESIS.md`, never a side-effect/posted comment alone — gotcha g/i;
   a Bug-5 empty-complete is NOT a fold, re-fork a fresh slug if so.) If folded:
   - **APPROVE + the docs stand on their own** (a strictly-better `deploy/chirp/README.md` pull-auth runbook,
     independent of the live fix — they do): land PR #30 on machine-n/a + review-APPROVE **only when
     re-polled MERGEABLE/CLEAN, not UNKNOWN/CONFLICTING** (gotcha f); squash-merge via `gh`, delete the branch,
     append to STATE. PR #30 does **NOT** close #29 — #29 stays open on the live F1 fix. Process the review's
     findings: blockers (none expected on docs) → remediate; non-blockers → board backlog linked to #29/PR #30.
   - **REQUEST-CHANGES** → fork ONE remediation DAG carrying the review findings + the original docs objective
     (budget: 2 doc-remediation attempts, then escalate). Never an inline fix (P1).
   - **Hold** instead of land only if the review shows the docs do NOT stand alone; then keep PR #30 open linked
     to #29 to land with the live fix. **Record the choice in STATE.**
2. **Did the user supply input?** (A `read:packages` token / a package-visibility flip / a comment on #29 or the
   board.) If yes: use your ONE fresh fork token to fork a fresh **devops DAG attempt 2/2** (`deploy-ghcr-auth-r2`)
   to run the one-step fix (create the `ghcr-pull` Secret, or rely on the now-public package) + verify AC1–4 live
   per `taskflow/dags/deploy-ghcr-auth/SYNTHESIS.md`'s runbook; its `_BRIEF.md` carries the prior verdict, the
   ruled-out hypotheses (`deploy-ghcr-auth/FAILURE.md` — do not re-tread), AC1–4, and the concerns to cover; do
   NOT prescribe method/methodology. Then escalate again if #2/2 also fails.
3. **Neither yet?** Keep waiting: board-check, then self-suspend on a FRESH bounded any_of wake (schedule
   resume_at ~20–40m board cadence OR forked-thread-completion `review-deploy-ghcr-auth`). A user request waits
   at most until the next board check, never until an unrelated DAG folds. Space the interval out when quiet.
4. **Exit decision — do NOT Exit** unless committed-digest reachability HOLDS **and** CI green **and** everything
   merged **and** the board is all Done. Until then: keep the project open (a kept save), schedule your successor
   I54 (`depends_on I53`, plain id `I54`, `dependencies: ["I53"]`, gotcha e), continue the chain.

## Carried state (read first)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I52/project_state.json` — persisted STATE (status,
  `dispatched_dags` incl. `review-deploy-ghcr-auth`, `turn_pointer.escalation`/`.awaiting`/`.open_risk`).
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I52/CONTINUE.md` — I52's terminal record (written on
  the wake that hands off to you).
- `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-deploy-ghcr-auth/SYNTHESIS.md` — the PR #30 review
  verdict (gate on this body).
- `/home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-ghcr-auth/SYNTHESIS.md` + `FAILURE.md` — the F1
  devops verdict + ruled-out hypotheses (feed a future attempt 2/2; do not re-tread).

## Gotchas (learned I1–I52) — carry forward
- (a) Create a DAG/overseer workspace dir on the real FS BEFORE authoring files into it (Write fails silently if
  the parent dir is absent).
- (d) **One `engine_fork` per iteration**; `PermissionDenied: missing token 'fork'` is non-retryable. A
  resumed/reconstructed iteration SHARES the original's spent token — check your own I53 dir for a prior
  SUSPENSION.md/CONTINUE.md/project_state.json FIRST; if a prior instance already forked, do NOT re-fork.
- (d2) `fork` requires a non-empty `launch_agent: "swe-coder"` ARGUMENT **and** a `_FORK.md` with flat keys incl.
  `owner_id: overseer/I53`, `observation_seam: <abs>/SYNTHESIS.md`, `disposition: reap-whole-after-land`,
  `launch_agent: swe-coder`, `launch_kernel: inherit`, `thread_type: dag`,
  `launch_context: { application: software, model_default: claude-opus-4-8 }`.
- (e) Successor `add_task` uses PLAIN id (`I54`) with `dependencies: ["I53"]` — never `overseer/I54`.
- (f) Re-poll `gh` mergeability until not UNKNOWN before any land; never land UNKNOWN/CONFLICTING.
- (g) Gate on a folded ROOT `SYNTHESIS.md` body, never a side-effect. (i) Bug-5: a reconstruct can force-complete
  a RUNNING DAG with NO root `SYNTHESIS.md` — re-fork a fresh slug. (j) Judge advancing-vs-frozen vs a FRESH
  clock; a long dormancy gap is not a stall; re-verify any land/fork a prior instance claims before repeating it.
- (gh-self-review) `gh pr review --approve` is rejected when the PR author == authenticated account; a review
  DAG's `SYNTHESIS.md` body is the authoritative verdict, posted additionally as a PR comment (#26 pattern).
- Devops-DAG budget: `deploy-ghcr-auth` was F1 recovery attempt **#1 of 2** and folded blocked-on-external-
  credential. Attempt **#2 of 2** is reserved for **after** the user supplies a `read:packages` credential (or
  flips the package public) — re-forking before then is futile. Then escalate again if #2 also fails.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s (k3d-hosted) cluster/namespaces + its ArgoCD. Never force-push
`main`; never rewrite merged history; add no attribution trailers to commits or PR bodies (#27/HYG-1). Changes
land as PRs; reviews, devops, bug-fixes, remediations, relocks are each their own forked DAG; bugs/findings are
filed as issues. Keep the GitHub Project/issues/PRs current. Drive to: the app running on k3s and reachable **on
the committed digest**, CI green, everything merged, board all Done — **then `Exit`**. The one thing between here
and `Exit` is committed-digest reachability, **blocked on a user-provided `read:packages` credential** (escalated
by I52). Hold the project open until the user acts.
