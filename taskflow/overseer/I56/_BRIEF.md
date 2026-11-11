# _BRIEF.md — NSWE overseer iteration I56 (persona swe-lead)
**Depends on**: I55

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the project thread
(chain link I50 → … → I54 → I55 → **I56**). You are an event loop, **NOT** a code writer — **P1: you never
write, edit, patch, rebase, or relock code, even to remediate; every engineering act is a forked DAG, and you do
not design the product inline either.** Boot the kernel + the NSWE app-files, publish `thread_evaluation`, then
do this iteration's Act.

**This turn's filesets: `PRODUCT_DESIGN` + `WORK_SESSION` (+ `BOARD`, `RETENTION`).** You are a **Launch a
design DAG** action task (per WORK_SESSION "The thread's tasks"): I55 already evaluated and decided the route;
you execute it.

## Why you woke — reachability is RESOLVED; measure the product against its release bar
I55 processed the `deploy-ghcr-auth-r2` devops PASS fold (fresh clock 2026-10-10T02:34Z): re-confirmed the root
`SYNTHESIS.md` present+PASS, did a fresh board check (no new PRs/issues/comments), ran a read-only deployment
check that corroborated the verdict **live** (ArgoCD `chirp` Synced+Healthy at `c805525`; committed-digest pod
`chirp-server-bbff68f5b-22spd` 1/1 Ready as the sole Service endpoint; `/healthz` → 200 on both ingress routes;
stale local RS at 0), **closed #32 directly** with the live evidence (board auto-moved it to Done), and updated
STATE (r2 → folded-PASS-reaped — **frees a DAG slot, now 0 in flight**; deployment healthy/verified; F1
resolved). **Chirp now RUNS and is reachable live. That is delivery, not the release bar.**

**The release bar has never been measured.** STATE `design.standing` is **null** — no design gap review has
assessed whether the live product is a *releasable* product (the swe-lead bar: something you could actually put
online, with real accounts, real data, and designed screens, unless the engagement asks for less). Per
WORK_SESSION "What the board check schedules," a release bar that is unmet with nothing on the board leading to
it is a **design** move (item 7), ahead of launching new hardening work (item 8). So the next move is a
**design DAG run as `swe-designer`**, NOT an Exit and NOT jumping to #24.

## This iteration's work: launch the design DAG (one fork), record it, schedule I56's successor
1. **Boot `PRODUCT_DESIGN` first** and let it govern. Quick FRESH-clock re-confirm (read-only `gh` + the live
   deployment) that nothing changed since I55 and the deployment is still healthy at `c805525`; if a **new**
   PR/issue/comment arrived, handle intake/grooming as its own `BOARD` task (don't let it block the launch).
2. **Determine the design move from `PRODUCT_DESIGN` + the repo:** check whether a design + an explicit,
   testable **release bar** already exist in the repository (`design.location`/`design.release_bar` are empty
   in STATE, so verify in-repo). 
   - If a release bar exists → the move is a **design gap review**: measure the live product at `c805525`
     against that bar as a user would, and file the gaps as work-items.
   - If no release bar exists yet → the move is a **product-design DAG that first establishes the release bar**
     for chirp (a Twitter-style app on ferric: accounts/sign-in, the core post/timeline data model, the
     user-facing flows and designed screens, real data) and then measures the live product against it.
   `PRODUCT_DESIGN` governs which; decide it there, not from this brief.
3. **Write the design DAG `_BRIEF.md`** per WORK_SESSION "Writing a DAG brief" + `PRODUCT_DESIGN` (describe, do
   not instruct; name the concerns — what a releasable product of this kind needs, the release bar's concreteness
   and testability, the design artifacts/tickets, traceability — each with its bar; do NOT name methodology
   bundles; do NOT carry a previous DAG's selection forward). Declared output: the design PR, its tickets on the
   board, and the release bar (+ a root `SYNTHESIS.md`; a gap review's verdict is bar-met or the gaps).
4. **Fork it** (`swe-designer`, `claude-opus-4-8`) **into the free slot** (confirm < 4 in flight first; now 0).
   One `engine_fork` this iteration (gotcha d). `_FORK.md` flat keys incl. `owner_id: overseer/I56`,
   `observation_seam: <abs>/SYNTHESIS.md`, `disposition: reap-whole-after-land`, `launch_agent: swe-designer`,
   `launch_kernel: inherit`, `thread_type: dag`,
   `launch_context: { application: software, model_default: claude-opus-4-8 }`. No methodology in `_FORK.md`.
5. **Record** the DAG in STATE `dispatched_dags` (kind `design`) and `design.design_dags`, and on the board;
   update STATE `updated`. Then **schedule successor I57** (`depends_on I56`, plain id `I57`,
   `dependencies: ["I56"]`, gotcha e) and **self-suspend on a FRESH bounded any_of wake**
   (schedule board-cadence ~20–40m OR forked-thread-completion of the design DAG), per the template in gotcha
   block below. I57 observes the design fold and triages it (`PRODUCT_DESIGN`/`BOARD`).

If `PRODUCT_DESIGN` instead concludes a gap review is premature or the bar is already met and recorded (not
expected — `standing` is null), do NOT fork idly: record that finding, then the next move is the hardening
backlog — **#24** (ArgoCD least-privilege RBAC + supply-chain hardening, the most substantive follow-up, epic
#3) as the next goal (its own `WORK_SESSION`+`DELIVERABLES_GIT` launch task), with #23/#25/#27 behind it.

## Backlog after the design move
With reachability resolved, the open board is #24/#23/#25/#27 (non-release-gating hardening/polish, epic #3) +
EPIC trackers #1/#2/#3 (OPEN by design). #24 is the natural next hardening goal once the design move is under
way; #25 is containerize polish; #23 is native-k3s install hardening; #27 is a tiny PR-body-hygiene docs item.
Launch new goals only into free DAG slots, each as its own launch task. Epics that don't depend on each other
and don't touch the same code may run concurrently within the 4 slots.

## Exit decision — do NOT Exit yet
Reachability HOLDS (verified live at `c805525`), but the engagement is **not** complete: the release bar has not
been measured (`design.standing` null), and open follow-ups #23/#24/#25/#27 + EPIC trackers #1/#2/#3 remain.
Do NOT `Exit` unless ALSO: CI green, everything merged, the board all Done (follow-ups resolved or explicitly
closed out-of-scope), **and the product meets the release bar its design set, confirmed by a gap review** (not
merely a healthy deployment). Until then keep the project open and continue the chain (I57, I58, …).

## Carried state (read first)
- `taskflow/overseer/I55/project_state.json` — persisted STATE (status `active`; `escalations[0]` F1 resolved
  with live evidence; `deployment` healthy/verified at `c805525`; `dispatched_dags` incl.
  `deploy-ghcr-auth-r2` = folded-PASS-reaped → 0 in flight; `backlog_assessment` = reachability resolved, design
  gap review is the next move; `design` empty / `standing` null; `engagement.followup_issues` incl. #32 closed).
- `taskflow/overseer/I55/CONTINUE.md` — I55's terminal record (what it did + this forward plan).
- Live world as of 2026-10-10T02:34Z: `main` HEAD `c805525` (owner-direct host-less ingress); ArgoCD `chirp`
  Synced+Healthy at `c805525`; chirp live-reachable; 0 open PRs; open issues #27/#25/#24/#23 + EPIC #1/#2/#3.

## Gotchas (learned I1–I55) — carry forward
- (a) Create a DAG/overseer workspace dir on the real FS BEFORE authoring files into it (Write fails silently
  if the parent dir is absent).
- (d) **One `engine_fork` per iteration**; `PermissionDenied: missing token 'fork'` is non-retryable. A
  resumed/reconstructed iteration SHARES the original's spent token — check your own I56 dir for a prior
  SUSPENSION.md/CONTINUE.md/project_state.json FIRST; if a prior instance already forked, do NOT re-fork.
- (d2) `fork` needs a non-empty `launch_agent` ARGUMENT (`swe-designer` for a design DAG) **and** a `_FORK.md`
  with the flat keys listed in step 4.
- (e) Successor `add_task` uses PLAIN id (`I57`) with `dependencies: ["I56"]` — never `overseer/I57`.
- (f) Re-poll `gh` mergeability until not UNKNOWN before any land; never land UNKNOWN/CONFLICTING.
- (g) Gate on a folded ROOT `SYNTHESIS.md` body, never a side-effect. (i) Bug-5: a reconstruct can
  force-complete a RUNNING DAG with NO root `SYNTHESIS.md` — re-fork a fresh slug. (j) Judge advancing-vs-frozen
  vs a FRESH clock; a long dormancy gap is not a stall; re-verify any land/fork a prior instance claims.
- (bounded wake) Self-suspend as a `Continue` iteration on a FRESH bounded `any_of` wake when a DAG is in
  flight — schedule board-cadence (~20–40m, ISO-8601 UTC) OR forked-thread-completion of the forked DAG — never
  an unbounded single wait. On each wake RE-EVALUATE the forked DAG's progress FIRST on a fresh clock:
  progressing → re-suspend with a fresh bounded wake; terminal → fold/triage; frozen → recover (re-fork
  carrying lessons / escalate), do not wait again.
- (owner-direct) The owner may push directly to `main` (author "Matt McKnight") and answer by DOING, not
  commenting; treat an owner commit + a closed item as the clearing signal; re-test the live world.
- (gh-review) `gh pr review --approve` is rejected on your own PR; post the verdict as a PR **comment** + inline
  findings.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s (k3d `nswe`) cluster/namespaces (`chirp*`) + its ArgoCD
Application `chirp`. Never force-push `main`; never rewrite merged history; **no attribution trailers** on
commits or PR bodies (#27/HYG-1). Changes land as PRs; reviews, devops, fixes, remediations, relocks, and
design are each their own forked DAG; bugs/findings are filed as issues. **Nothing on GitHub carries
host/system details** (no server address, SSH key path, user name, host paths, taskflow internals) — translate
host facts to repository identities. Keep the GitHub Project/issues/PRs current. Drive to: the app running on
k3s and reachable (verified live — DONE), CI green, everything merged, board all Done, **and the product meeting
the release bar its design set, confirmed by a gap review** — then `Exit`.
