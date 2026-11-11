# _BRIEF.md — NSWE overseer iteration I55 (persona swe-lead)
**Depends on**: I54

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the project thread
(chain link I50 → … → I54 → **I55**). You are an event loop, **NOT** a code writer — **P1: you never write,
edit, patch, rebase, or relock code, even to remediate; every engineering act is a forked DAG.** Boot the
kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS; domain WORK_SESSION/BOARD/DEPLOYMENT/REVIEW_GATE/
DELIVERABLES_GIT/RETENTION — **this turn you most likely need WORK_SESSION + DEPLOYMENT + REVIEW_GATE + BOARD +
RETENTION**, because you are processing a devops DAG fold), publish `thread_evaluation`, then do this
iteration's Act.

## Why you woke — the forked devops DAG FOLDED **PASS**; route it (verdict already read by I54)
I54 did a fresh board check, resolved the F1 escalation (the ask-as-posed; owner acted directly), filed the
live-reachability tracking **issue #32**, and **forked the devops DAG `deploy-ghcr-auth-r2`** (`swe-coder`,
F1 attempt **#2 of 2** — the LAST automatic devops attempt), then self-suspended on a bounded any_of wake. A
resumed I54 instance woke on the schedule-cadence member (2026-10-10T02:26Z), re-evaluated the DAG on a fresh
clock, and found it **FOLDED with a root `SYNTHESIS.md` PASS verdict** — so it reached `continue` and handed to
you to process that fold. **Re-confirm on a FRESH clock, then route.**

**The fold verdict (already confirmed present at `taskflow/dags/deploy-ghcr-auth-r2/SYNTHESIS.md`, PASS):**
Chirp is **live-reachable on the committed digest** `@sha256:054af27f…`, verified live 2026-10-10 by executed
cluster checks (AC1–5 all PASS): committed-digest pod `1/1 Ready` as the sole Service endpoint (stale
local-image RS at 0), ArgoCD `chirp` **Synced + Healthy at `c805525`**, `/healthz` → `200` from the digest pod
on **both** ingress routes (host-less + `chirp.localhost`), **selfHeal/prune survival proven by a reconcile
rehearsal**, supply-chain/least-privilege posture preserved. **The fix was fully OUT-OF-BAND** — the owner's
`ghcr-pull` Secret (present ~31h) resolved the pull, plus the already-committed host-less ingress at `c805525`.
**No repository change was required and NO PR exists; NO external input is still needed.**

## This iteration's work: process the PASS fold (no PR to review/land), full board check, route
**First, FRESH board check (read-only `gh`, fresh clock)** — new PRs/issues/comments since I54
(2026-10-10T01:48Z); re-test every open item against the live world. **Re-confirm `deploy-ghcr-auth-r2`'s root
`SYNTHESIS.md` is still present** (gotcha g/j — gate on the folded ROOT body, not a side-effect; a dormancy gap
is not a stall). It was present and PASS at the I54 wake; confirm, don't re-run the DAG.

**Then route the PASS fold (an evaluation decides; each action is its own scheduled task with its own fileset).**
Because the fix is out-of-band with **no PR**, there is **nothing to review and nothing to land** — skip the
review/landing cycle entirely. The route is:
- **Deployment check** (`DEPLOYMENT`, `WORK_SESSION`): read the live system read-only and record it — the DAG
  already verified it live, but STATE/board must reflect it. Confirm synced+healthy at `c805525`, digest pod
  Ready as sole endpoint, `/healthz` 200. (Do not re-drive; this is the overseer's own read + record.)
- **Close #32 directly** (`BOARD`): close issue #32 referencing the live-reconcile evidence (committed-digest
  pod 1/1 Ready as sole endpoint, ArgoCD Synced+Healthy at `c805525`, `/healthz` 200 both routes, survives
  selfHeal/prune). No `Closes #32` PR line exists because there is no PR — close it by hand with the evidence.
  Move #32 to **Done** on the Delivery board. Written for GitHub readers (no host/system details).
- **Update STATE** (`RETENTION`): `dispatched_dags` → `deploy-ghcr-auth-r2` = folded-PASS (reap-whole-after
  record; frees a slot); `deployment` record = `deployed_sha c805525`, health healthy, `last_verified_at`
  2026-10-10; escalation F1 stays resolved; append the reachability outcome. The F1 devops budget is now
  **resolved** — reachability is achieved; no further devops attempt is owed.
- **Collect the devops DAG's residue / let it be reaped** per `reap-whole-after-land` (its verdict is recorded;
  there are no non-blocking findings to file since no PR/review).
- If the board check found **new** PRs/issues/comments, intake/groom them as their own `BOARD` tasks.

If instead a FRESH-clock re-confirm finds the root SYNTHESIS.md **gone / force-completed-empty** (gotcha i,
Bug-5 — a reconstruct marked a RUNNING DAG Complete with NO root SYNTHESIS.md): do NOT gate on it; **re-fork a
fresh slug** (`deploy-ghcr-auth-r3`, `swe-coder`) carrying the attempt-1 + attempt-2 lessons + AC1–5 forward
(that re-fork is your own action with your own fresh token). This is NOT expected — the fold was present and
PASS at the I54 wake — but re-confirm before relying on it.

**Backlog — reachability now HOLDS, so the remaining path to Exit opens up.** With F1 resolved and reachability
verified live, the backlog is #23/#24/#25/#27 (non-release-gating hardening/polish per STATE
`backlog_assessment`) + EPIC trackers #1/#2/#3 (OPEN by design). **#24** (ArgoCD least-privilege RBAC +
supply-chain hardening) is the natural next goal now that nothing gates it; #23/#25 are hardening, #27 a tiny
docs/hygiene item. Launch the next goal only into a free DAG slot (`deploy-ghcr-auth-r2`'s fold freed one), as
its own `WORK_SESSION`+`DELIVERABLES_GIT` launch task. Groom/rank as a `BOARD` task if a batch of new issues
arrived. **Before treating a nearly-empty board as "done," ask whether the RELEASE BAR has been measured:** a
healthy deployment shows the software *runs*, not that the product is *releasable* — that is a design **gap
review**'s verdict against the release bar (`PRODUCT_DESIGN`/`WORK_SESSION`: "an empty board with the bar unmet
calls for design, not rest"). Check STATE `design.standing`: if no gap review has measured the live product, or
one found it short, the next step is a **design gap review DAG** (`swe-designer`), not an Exit.

## Exit decision — do NOT Exit yet (reachability holds, but the bar is not confirmed met)
Reachability now HOLDS (verified live). Do NOT `Exit` unless ALSO: CI is green, everything is merged, the board
is all Done (OPEN follow-ups #23/#24/#25/#27 + EPIC trackers #1/#2/#3 resolved or explicitly closed
out-of-scope), **and the product meets the release bar its design set, confirmed by a gap review** (not merely
that the deployment is healthy). Until then keep the project open and schedule successor **I56** (`depends_on
I55`, plain id `I56`, `dependencies: ["I55"]`, gotcha e); continue the chain. If after the board check and the
fold processing nothing further is actionable and a DAG is in flight, self-suspend on a FRESH bounded any_of
wake (schedule board-cadence ~20–40m OR forked-thread-completion of the in-flight DAG); if nothing is in
flight, a schedule-only wake on the short board cadence.

## Carried state (read first)
- `taskflow/overseer/I54/project_state.json` — persisted STATE (status re-derived to `active`; `escalations[0]`
  = F1 resolved-by-owner-action; `deployment` record; `dispatched_dags` incl. `deploy-ghcr-auth-r2`=in-flight;
  `owner_changes` incl. `c805525`; `backlog_assessment`; `#32` in `engagement.followup_issues`).
- `taskflow/overseer/I54/CONTINUE.md` — I54's terminal record (what it did + forward plan).
- `taskflow/dags/deploy-ghcr-auth-r2/{_BRIEF.md,SYNTHESIS.md,FAILURE.md}` — the r2 task spec and (when folded)
  its verdict. `taskflow/dags/deploy-ghcr-auth/{SYNTHESIS.md,FAILURE.md}` — the attempt-1 verdict + ruled-out
  hypotheses (feed any re-fork; do not re-tread).
- Owner change: commit `c805525` on `main` (host-less tailnet ingress). `main` HEAD = `c805525`.

## Gotchas (learned I1–I54) — carry forward
- (a) Create a DAG/overseer workspace dir on the real FS BEFORE authoring files into it (Write fails silently
  if the parent dir is absent).
- (d) **One `engine_fork` per iteration**; `PermissionDenied: missing token 'fork'` is non-retryable. A
  resumed/reconstructed iteration SHARES the original's spent token — check your own I55 dir for a prior
  SUSPENSION.md/CONTINUE.md/project_state.json FIRST; if a prior instance already forked, do NOT re-fork.
- (d2) `fork` needs a non-empty `launch_agent` ARGUMENT (`swe-reviewer` for a review DAG, `swe-coder` for a
  devops/code/remediation DAG, `swe-designer` for design) **and** a `_FORK.md` with flat keys incl.
  `owner_id: overseer/I55`, `observation_seam: <abs>/SYNTHESIS.md`, `disposition: reap-whole-after-land`,
  `launch_agent: <agent>`, `launch_kernel: inherit`, `thread_type: dag`,
  `launch_context: { application: software, model_default: claude-opus-4-8 }`.
- (e) Successor `add_task` uses PLAIN id (`I56`) with `dependencies: ["I55"]` — never `overseer/I56`.
- (f) Re-poll `gh` mergeability until not UNKNOWN before any land; never land UNKNOWN/CONFLICTING.
- (g) Gate on a folded ROOT `SYNTHESIS.md` body, never a side-effect. (i) Bug-5: a reconstruct can force-complete
  a RUNNING DAG with NO root `SYNTHESIS.md` — re-fork a fresh slug. (j) Judge advancing-vs-frozen vs a FRESH
  clock; a long dormancy gap is not a stall; re-verify any land/fork a prior instance claims before repeating it.
- (owner-direct) The owner may push directly to `main` (author "Matt McKnight", distinct from `mattsmcknight`)
  and answer by DOING, not commenting. Treat an owner commit + a closed item as the clearing signal; re-test
  the live world. (STATE `known_patterns.owner_acts_directly`.)
- (gh-review) `gh pr review --approve` is rejected on your own PR; post the verdict as a PR **comment** +
  inline findings (STATE `known_patterns.review_visibility_on_github`, gh_self_review_block).
- Devops-DAG budget: `deploy-ghcr-auth-r2` is the **last** automatic devops attempt for F1. If it cannot finish
  live, **escalate** (don't auto-retry); only a Bug-5 empty force-complete warrants a fresh re-fork.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s (k3d `nswe`) cluster/namespaces (`chirp*`) + its ArgoCD
Application `chirp`. Never force-push `main`; never rewrite merged history; **no attribution trailers** on
commits or PR bodies (#27/HYG-1). Changes land as PRs; reviews, devops, fixes, remediations, relocks are each
their own forked DAG; bugs/findings are filed as issues. **Nothing on GitHub carries host/system details**
(no server address, SSH key path, user name, host paths, taskflow internals) — translate host facts to
repository identities. Keep the GitHub Project/issues/PRs current. Drive to: the app running on k3s and
reachable (on the committed digest, or the owner-chosen reachability, verified live), CI green, everything
merged, board all Done — **then `Exit`**.
