# _BRIEF.md — NSWE overseer iteration I54 (persona swe-lead)
**Depends on**: I53

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the project thread
(chain link I50 → I51 → I52 → I53 → **I54**). You are an event loop, **NOT** a code writer — **P1: you never
write, edit, patch, rebase, or relock code, even to remediate; every engineering act is a forked `swe-coder`
DAG.** Boot the kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS; domain WORK_SESSION/BOARD/DEPLOYMENT/
REVIEW_GATE/DELIVERABLES_GIT/RETENTION — note **BOARD + DEPLOYMENT** are needed this turn), publish
`thread_evaluation`, then do this iteration's Act.

## Why you woke — THE WORLD CHANGED: the owner acted directly (re-evaluate against a FRESH clock)
I53 landed PR #30 (docs runbook) on `main @ 9df6baf` and self-suspended on a bounded board-cadence wake while
`blocked-on-user`. A resumed I53 instance woke on the schedule timer (fired 2026-10-10T01:36Z) and
**re-evaluated on a fresh clock (2026-10-10T01:38Z)** — it found the **owner answered by doing, not by
commenting** (the pattern OUT_OF_FOCUS/BOARD warn about). Two concrete signals, both GitHub-observable:

1. **Owner pushed a direct commit to `main`: `c805525` (2026-10-09T16:17Z, author "Matt McKnight", tagged
   "(owner change)").** It adds a **host-less ingress rule** to `deploy/chirp/30-ingress.yaml` (additive, 12/0)
   so Chirp is reachable by the server's **tailnet address** (e.g. `http://100.90.75.93:8081/`) for **any
   Host**, alongside the existing host-based (`chirp.localhost`) rule. `main` HEAD is now **`c805525`** (not
   `9df6baf`). This is a **reachability/topology change the owner made themselves** — it addresses north-south
   reachability, **not** the pod image-pull (`ImagePullBackOff` on the private digest, the F1 root cause).
2. **Issue #29 (the F1 escalation vehicle) is CLOSED** (2026-10-08T19:27:39Z, ~3s after PR #30's squash-merge
   — likely a merge auto-close, but it IS closed and the owner has since acted directly). The `read:packages`
   credential was **never supplied**, and the owner did **not** take the credential path — they changed the
   **reachability approach** (tailnet ingress) instead.

Other board facts this re-eval found (fresh clock): **0 open PRs**; GHCR package API still **403** to our token
(our `gh` token lacks `read:packages`, so public/private is **inconclusive from here** — only a devops DAG with
cluster/registry reach can tell); **no new issues**; remaining OPEN backlog is the pre-existing follow-ups
**#23 / #24 / #25 / #27** (Todo) plus the three EPIC trackers **#1 / #2 / #3** (OPEN by design). All build items
#4–#13 are merged.

**You hold a FRESH, UNSPENT `engine_fork` token** — the prior I53 did not fork (gotcha d). But FIRST check your
own I54 dir for a prior-instance SUSPENSION.md/CONTINUE.md/project_state.json; if a prior I54 already forked,
the token is spent/shared — do NOT re-fork (gotcha d).

## This iteration's goal: route the owner's action; the overseer CANNOT verify the cluster inline (no kubectl)
Do a **full fresh board check FIRST** (read-only `gh`, fresh clock), then schedule the series you can see.
An evaluation decides; each action is its own scheduled task with its own fileset. The likely series:

1. **Resolve the #29 escalation (owner acted).** Load BOARD + RETENTION. The owner closed #29 and drove
   reachability directly (`c805525`). Record the resolution honestly in STATE (`escalations[].resolved_at` +
   `evidence` = the owner's commit + the close), and record `c805525` as an owner change on `main`. Do NOT
   reopen #29 just to track the residual — if live reachability still needs completing, track THAT as its own
   issue/escalation against the live world, not against the old ask.
2. **Check the deployment (you cannot do this inline — fork it).** The overseer sandbox has **no kubectl**
   (the overseer dispatches compute DAGs for judgment; it does not verify the cluster itself). So assess what
   is GitHub-observable, then **fork a devops DAG** (DEPLOYMENT loaded; this is the F1 **attempt #2 of 2**, now
   released because the owner acted) — slug `deploy-ghcr-auth-r2`, `launch_agent: swe-coder`. Its objective:
   **verify AC1–4 live reachability** against the owner's new **tailnet host-less ingress** approach AND the
   committed digest `@sha256:054af27…`; determine whether the pod is actually Running (image-pull resolved by
   the owner out-of-band, e.g. a `ghcr-pull` Secret created or the package flipped public) or still in
   `ImagePullBackOff`; **create the `ghcr-pull` Secret only if the pod still cannot pull** and a credential is
   now reachable; and reconcile the committed GitOps state (ArgoCD `Application chirp`) with what is actually
   running. Its `_BRIEF.md` carries: the prior verdict + ruled-out hypotheses
   (`taskflow/dags/deploy-ghcr-auth/SYNTHESIS.md` + `FAILURE.md` — **do not re-tread**), the owner's `c805525`
   change, AC1–4, and the concerns to cover (reachability, image-pull/supply-chain, GitOps
   drift/selfHeal-survival, ops). **Do NOT prescribe method/methodology.** If #2/2 also cannot finish live,
   escalate again with what it found. (Budget: this is the last automatic devops attempt.)
3. **A new issue / comment / scope change on the board?** None found this re-eval beyond the above. If a board
   check finds one, intake it as a work-item (issue + acceptance criteria + priority), ranked against the
   backlog.
4. **Backlog follow-ups #23/#24/#25/#27.** Assess whether they belong to the release bar or are optional
   polish; groom/rank; launch as goals within the 4 DAG-slot limit only when they are the next thing that
   moves the engagement forward (reachability verification comes first).
5. **Exit decision — do NOT Exit** unless committed-digest (or the owner-chosen) reachability **HOLDS, verified
   live by the devops DAG**, CI is green, everything is merged, and the board is all Done (the OPEN follow-ups
   and EPIC trackers must be resolved or explicitly closed as out-of-scope). Until then keep the project open
   (a kept save) and schedule successor **I55** (`depends_on I54`, plain id `I55`, `dependencies: ["I54"]`,
   gotcha e), continue the chain. If after the board check nothing is actionable and a devops DAG is in flight,
   self-suspend on a FRESH bounded **any_of** wake (schedule board-cadence ~20–40m OR forked-thread-completion
   `deploy-ghcr-auth-r2`); if nothing is in flight, a schedule-only wake.

## Carried state (read first)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I53/project_state.json` — persisted STATE (status
  `blocked-on-user` as last written; re-derive it this turn from the live world — the owner has acted, so it is
  no longer a clean blocked-on-user). `dispatched_dags` incl. `review-deploy-ghcr-auth`=folded-APPROVE-landed;
  PR #30 in `work_items`; `deploy-ghcr-auth`=folded-failed-blocked (attempt 1/2).
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I53/CONTINUE.md` — I53's terminal record (the
  fresh-clock re-eval that found the owner acted and handed to you).
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I52/escalation-29.md` — the user-facing #29 ask (now
  closed/overtaken by the owner's direct action).
- `/home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-ghcr-auth/SYNTHESIS.md` + `FAILURE.md` — the F1
  devops verdict + ruled-out hypotheses (feed attempt 2/2; do not re-tread).
- The owner's change is commit `c805525` on `main` (`deploy/chirp/30-ingress.yaml`, host-less tailnet ingress).

## Gotchas (learned I1–I53) — carry forward
- (a) Create a DAG/overseer workspace dir on the real FS BEFORE authoring files into it (Write fails silently if
  the parent dir is absent).
- (d) **One `engine_fork` per iteration**; `PermissionDenied: missing token 'fork'` is non-retryable. A
  resumed/reconstructed iteration SHARES the original's spent token — check your own I54 dir for a prior
  SUSPENSION.md/CONTINUE.md/project_state.json FIRST; if a prior instance already forked, do NOT re-fork.
- (d2) `fork` requires a non-empty `launch_agent: "swe-coder"` ARGUMENT **and** a `_FORK.md` with flat keys incl.
  `owner_id: overseer/I54`, `observation_seam: <abs>/SYNTHESIS.md`, `disposition: reap-whole-after-land`,
  `launch_agent: swe-coder`, `launch_kernel: inherit`, `thread_type: dag`,
  `launch_context: { application: software, model_default: claude-opus-4-8 }`.
- (e) Successor `add_task` uses PLAIN id (`I55`) with `dependencies: ["I54"]` — never `overseer/I55`.
- (f) Re-poll `gh` mergeability until not UNKNOWN before any land; never land UNKNOWN/CONFLICTING.
- (g) Gate on a folded ROOT `SYNTHESIS.md` body, never a side-effect. (i) Bug-5: a reconstruct can force-complete
  a RUNNING DAG with NO root `SYNTHESIS.md` — re-fork a fresh slug. (j) Judge advancing-vs-frozen vs a FRESH
  clock; a long dormancy gap is not a stall; re-verify any land/fork a prior instance claims before repeating it.
- (owner-direct) The owner may push directly to `main` (author "Matt McKnight", distinct from the `mattsmcknight`
  gh identity the DAGs commit under) and may answer an escalation by DOING rather than commenting. Treat an
  owner commit + a closed escalation as the clearing signal; re-test the live world, don't wait on a comment.
- Devops-DAG budget: `deploy-ghcr-auth` was F1 recovery attempt **#1 of 2** (folded blocked-on-external-
  credential). Attempt **#2 of 2** is now RELEASED (the owner acted) — spend it to **verify/complete live
  reachability** against the owner's tailnet approach, not on a blind credential retry. Then escalate again if
  #2 also cannot finish.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s (k3d-hosted) cluster/namespaces + its ArgoCD. Never force-push
`main`; never rewrite merged history; add no attribution trailers to commits or PR bodies (#27/HYG-1). Changes
land as PRs; reviews, devops, bug-fixes, remediations, relocks are each their own forked DAG; bugs/findings are
filed as issues. Keep the GitHub Project/issues/PRs current. Drive to: the app running on k3s and reachable
(on the committed digest, or the owner-chosen reachability, verified live), CI green, everything merged, board
all Done — **then `Exit`**. The one thing between here and `Exit` is live reachability; the owner has acted on
it directly (`c805525` + closed #29), so the next move is to **verify it live via a devops DAG**, not to keep
waiting on a credential. Hold the project open until reachability is verified and the board is Done.
