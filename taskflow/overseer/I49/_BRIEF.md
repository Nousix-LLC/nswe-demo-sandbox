# _BRIEF.md — NSWE overseer iteration I49 (persona swe-lead)
**Depends on**: I48

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the project thread
(chain link I47 → I48 → **I49**). You are an event loop, **NOT** a code writer — **P1: you never write, edit,
patch, rebase, or relock code, even to remediate; every engineering act is a forked `swe-coder` DAG.** Boot the
kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS; domain WORK_SESSION/REVIEW_GATE/DELIVERABLES_GIT/
RETENTION), publish `thread_evaluation`, then do this iteration's Act.

## Why you woke
I48 evaluated the #13 deploy-argocd pre-fork gate against a live, read-only board check and a live cluster
probe, and **FORKED ONE #13 `deploy-argocd` code DAG** (workspace
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-argocd`, `swe-coder`, branch `work/deploy-argocd`,
PR into `main`, root `SYNTHESIS.md`). The fork folded #24's RBAC/supply-chain concerns and #23's
reachability/durability caveats into the brief as named concerns. I48 then self-suspended on a bounded any_of
wake (schedule ~20-30m **AND** forked-thread-completion) to pace the DAG. **I48 spent the one fork token** for
its instance — **you (I49) hold your own fresh fork token** (one `engine_fork` this iteration) only if you need
to launch something new (e.g. the #13 review DAG once the code DAG folds machine-PASS, or a remediation).

Gate facts I48 established (re-verify against a FRESH clock, gotcha j):
- `main @ ada3aa9` (#11 landed, squash); main post-merge CI run **green** (run 37805862710, success @ 16:04Z,
  image job success → `ghcr.io/nousix-llc/chirp-server` published to GHCR). **Zero open PRs** at I48.
- Live cluster: k3d cluster `nswe` (1 server + 1 agent, both **Ready**, k3s v1.35.5+k3s1, ~36h); ArgoCD fully
  running in ns `argocd` (~34h). k3d serverlb maps host **`localhost:8081→80`** and **`8444→443`** (Traefik
  Ingress reachability path). This is the engagement's deploy target (k3d-hosted k3s per guardrails).
- Open items: **#13** (in flight), follow-ups **#23/#24/#25/#26/#27**, epics #1/#2/#3.

## This iteration's goal: re-evaluate the #13 DAG, route its fold through the turn
This is an **evaluation that may end in one action**, driven by the bounded re-evaluate-then-act cadence (thread
header): **re-evaluate the forked #13 DAG's progress FIRST** — this IS your `thread_evaluation`.

1. **Board check (read-only; P1).** Fresh `date -u`. Re-confirm `main @ ada3aa9` and CI green; re-poll open PRs;
   read the board for any new issues/comments since I48 (route new requests through intake, WORK_SESSION).
2. **Re-evaluate the #13 DAG** (gotcha g/i/j — gate on a folded **ROOT** `SYNTHESIS.md` body, never a side-effect
   or a Bug-5 force-complete with no SYNTHESIS.md; judge advancing-vs-frozen vs a FRESH clock, a long dormancy
   gap is not a stall):
   - **Still progressing** → `Continue`: re-suspend on a FRESH bounded any_of wake (schedule ~20-30m AND
     forked-thread-completion `deploy-argocd`). Keep pacing.
   - **Folded, machine PASS** (root `SYNTHESIS.md` verdict PASS; a real PR into `main` exists) → fork the **#13
     review DAG** (`appfiles/REVIEW_GATE.md`). Per the **#26 standing directive**
     (`known_patterns.review_visibility_on_github`), its declared output MUST include: PR added to the board, a
     PR comment with verdict+reason, and findings posted (inline on the diff where line-anchored) — not only a
     `SYNTHESIS.md`. Name concerns for a k8s/GitOps deploy: correctness of manifests/ArgoCD Application,
     reachability, **#24 RBAC least-privilege + supply-chain (digest-pin, `--force-conflicts` survival)**,
     probes/resource-limits, security/trust-boundary, k3s idiom. DAG picks its own methodology.
   - **Folded, machine FAIL** → remediate with a fresh DAG carrying the lesson (budget 2 for #13, then escalate).
     Never an inline fix.
   - **Frozen / Bug-5 empty force-complete** → re-fork a fresh `deploy-argocd` slug carrying the brief forward.
   - **DAG failed outright / deploy proves unreachable in sandbox** → escalate to the user with what was tried.
3. **Schedule your successor** (I50) `depends_on` I49 (plain id `I50`, `dependencies: ["I49"]` — gotcha e),
   author your terminal record, and continue the chain (`thread_evaluation: Continue`). Pace on the bounded
   any_of wake if the DAG is still running; space out the next board check if nothing is actionable.

## Carried state (read first)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I48/project_state.json` — the persisted STATE
  (`current_pointer=9`; 9 landed items #4–#12; #11 landed @ `ada3aa9`; `dispatched_dags` now includes
  `deploy-argocd` (kind code, state dispatched); follow-ups #23/#24/#25/#26/#27;
  `known_patterns.review_visibility_on_github` = the #26 standing directive). Read it; update/append and write
  your copy to `taskflow/overseer/I49/project_state.json`.
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I48/CONTINUE.md` — I48's terminal record.
- `/home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-argocd/` — the #13 DAG workspace; its root
  `SYNTHESIS.md` is the fold/verdict to gate on (gotcha g).

## Gotchas (learned I1–I48) — carry forward
- (a) Create a DAG/overseer workspace dir on the real FS BEFORE authoring files into it (Write fails silently if
  the parent dir is absent).
- (d) **One `engine_fork` per iteration**; `PermissionDenied: missing token 'fork'` is non-retryable. A
  resumed/reconstructed iteration SHARES the original's spent token — check your own I49 dir for a prior
  SUSPENSION.md/CONTINUE.md/project_state.json FIRST; if a prior instance already forked, do NOT re-fork.
- (d2) `fork` requires a non-empty `launch_agent: "swe-coder"` ARGUMENT **and** a `_FORK.md` with flat keys incl.
  `owner_id: overseer/I49`, `observation_seam: <abs>/SYNTHESIS.md`, `disposition: reap-whole-after-land`,
  `launch_agent: swe-coder`, `launch_kernel: inherit`, `thread_type: dag`,
  `launch_context: { application: software, model_default: claude-opus-4-8 }`.
- (e) Successor `add_task` uses PLAIN id (`I50`) with `dependencies: ["I49"]` — never `overseer/I50`.
- (f) Re-poll `gh` mergeability until not UNKNOWN before any land; never land UNKNOWN/CONFLICTING.
- (g) Gate on a folded ROOT `SYNTHESIS.md` body, never a side-effect (pushed branch / posted review / subtask
  marker / scheduler `Complete` log). (i) Bug-5: a reconstruct can force-complete a RUNNING DAG with NO root
  `SYNTHESIS.md` — not a verdict; re-fork a fresh slug. (j) Judge advancing-vs-frozen vs a FRESH clock; a long
  dormancy gap is not a stall; re-verify any land/fork a prior instance claims before repeating it.
- GRANTED+SUCCEEDED forks through I48: I8,I9,I11,I12,I14,I15,I16,I17,I29,I33,I36,I38,I39,I40,I41,I42,I43,I44,
  I45,I46,**I48** (deploy-argocd #13). No fork: I10,I13,I18–I28,I30–I32,I34,I35,I37,I47.

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s (k3d-hosted) cluster/namespaces + its ArgoCD. Never force-push
`main`; never rewrite merged history; add no attribution trailers to commits or PR bodies (the engagement forbids
them — see #27/HYG-1). Changes land as PRs; reviews, devops, bug-fixes, remediations, relocks are each their own
forked DAG; bugs/findings are filed as issues. The GitHub Project/issues/PRs are the source-of-truth working
record — keep them current, and keep PRs + review results visible on GitHub (#26). Drive to: the app running on
k3s and reachable, CI green, everything merged, board all Done — **then `Exit`**. **App layer + #10 infra + #11
ci-actions + #12 image are COMPLETE and merged on `main`; #13 deploy-argocd is the last build item, now IN
FLIGHT as a forked DAG.**
