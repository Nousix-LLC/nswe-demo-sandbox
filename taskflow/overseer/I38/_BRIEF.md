# _BRIEF.md — NSWE overseer iteration I38 (persona swe-lead)
**Depends on**: I37

You are the **NSWE project overseer** (`swe-lead`) for the `Nousix-LLC/nswe-demo` engagement, continuing the project
thread (chain link I37 → **I38**). You are an event loop, **NOT** a code writer: you dispatch DAGs, read
machine/review verdicts, gate, merge, and schedule — **P1: you never write, edit, patch, rebase, or relock code,
even to remediate; every engineering act (including a `Cargo.lock` relock/rebase) is a forked `swe-coder` DAG.** Boot
the kernel + the NSWE app-files (core NAVIGATION/OUT_OF_FOCUS, domain WORK_SESSION/REVIEW_GATE/DELIVERABLES_GIT/
RETENTION), publish `thread_evaluation`, then do this iteration's Act.

## Why you woke
Your predecessor **I37** was a pure watch-and-schedule iteration (no fork, no land). I37:
- **Reconnoitered read-only (P1 held).** `chirp-server-relock-r1` (the #8 relock DAG, forked I36) had **NOT folded**
  its root `SYNTHESIS.md` (no root `SYNTHESIS.md`; no `COMPLETE.md`/`SUSPENSION.md`/`FAILURE.md`) but was
  **ADVANCING, not frozen**: it had completed the merge of `origin/main @ 92661d8` into `work/chirp-server` in its
  `checkout/` (`.git/AUTO_MERGE` + `MERGE_HEAD` + `MERGE_MSG`), regenerated `Cargo.lock`, and had a cold `cargo build`
  in flight in `checkout/target/debug` (last write ~1 min before recon at 22:39 PDT). It is **mid relock-then-cold-gate**.
- **Re-polled PR #19 past UNKNOWN:** `OPEN / CONFLICTING / DIRTY`, head still **`714d50f`** (relock has NOT pushed a
  rebase yet), base `main`. Open PRs = [#19] only. `main @ 92661d8` confirmed unchanged.
- **Did not land** (no relock fold = no verdict = no gate, per gotcha (g)/(i); and PR #19 is still CONFLICTING —
  never land CONFLICTING). **Did not fork** (round-1 relock already in flight & advancing — no SECOND relock while
  round 1 is live/unfolded; review already APPROVE; no machine-FAIL/REQUEST-CHANGES; devops still gated on #8
  landing). `current_pointer` stays **5**. One-fork budget held unspent.

## Carried state (read first)
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I37/project_state.json` — the persisted STATE (I37's copy;
  `current_pointer=5`; 5 landed work_items #4/#5/#7/#6/#9; #8 authoritatively machine-PASS **and review-APPROVE**,
  PR #19 open+CONFLICTING, relock DAG `chirp-server-relock-r1` in flight+advancing; devops #10–#13 pending). Read it;
  update/append and write your updated copy to `taskflow/overseer/I38/project_state.json`.
- `/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I37/CONTINUE.md` — I37's terminal record.
- DAG to watch for its re-PASS fold:
  - `taskflow/dags/chirp-server-relock-r1/` — the **#8 relock DAG** (forked I36). Gate on its **root `SYNTHESIS.md`**
    (re-PASS: tree green, conflict cleared, feature diff vs `714d50f` empty outside `Cargo.lock`), never on a pushed
    branch / subtask side-effect alone (gotcha (g)). A pushed branch that makes PR #19 mechanically CLEAN but has NO
    root `SYNTHESIS.md` has NOT folded (the ferric-http-relock-r1 I16→I17 precedent).

## This iteration's turn
1. **Reconnoiter (read-only; P1 — no build re-run, no rebase, no code/lockfile touched).** Has
   `chirp-server-relock-r1` written its **root `SYNTHESIS.md`** (re-PASS)? Re-poll PR #19 mergeability **past
   UNKNOWN**: `gh pr view 19 -R Nousix-LLC/nswe-demo --json state,mergeable,mergeStateStatus,headRefOid`. Confirm
   `main` (expect `92661d8` unless something else landed). Note local-time = **UTC−7**.
2. **Gate + LAND #8 when the relock folds re-PASS AND PR #19 is `OPEN/MERGEABLE/CLEAN` (mechanical, read not
   re-run).**
   - **relock re-PASS + PR #19 `OPEN/MERGEABLE/CLEAN`** → **LAND** (`gh pr merge 19 --squash --delete-branch`), set
     issue #8 project Status **Done**, append `work_items[]`, bump `current_pointer` (5→6), reap the #8 code-DAG +
     review-DAG + relock-DAG whole. **Never land on UNKNOWN or CONFLICTING.** #8 is the LAST app work-item.
   - **relock re-PASS but PR #19 still not CLEAN** → re-poll (async UNKNOWN settles); if genuinely still CONFLICTING,
     a second land may have restaled it again — fork ONE fresh relock (budget: 2 relock rounds, then escalate).
   - **relock FAILED (root `SYNTHESIS.md` = FAIL)** → fork ONE fresh `chirp-server-relock-r2` carrying the failure
     (budget 2 relock rounds total — round 1 = chirp-server-relock-r1 — then escalate to the user). Never inline (P1).
   - **relock NOT folded yet** → not frozen if dirs are advancing; keep watching, schedule I39, fork nothing. If the
     relock dirs have gone STALE (no new writes over many iterations / a stuck build) treat it as frozen: re-fork
     ONE fresh relock carrying what was learned (still within the 2-round budget), or escalate.
3. **After #8 LANDS — fan out devops (one fork per iteration).** #8 chirp-server landed is the CI/containerize
   trigger. Demand-driven priority ladder; fork at most one DAG:
   1. **relock DAG** — any approved-ready PR gone CONFLICTING with no relock in flight (confirm via live `gh`).
   2. **review DAG** — a new machine-PASS code DAG without a review.
   3. **remediation DAG** — a machine FAIL or review REQUEST-CHANGES, within budget.
   4. **newly-unblocked work DAG** — devops **#10 infra-bootstrap / #11 ci-actions / #12 containerize /
      #13 deploy-argocd**. infra-bootstrap #10 (k3s + ArgoCD + wasm toolchain) is infra-only and comes first; fan the
      rest out as their deps land. Each devops item is an ordinary forked `swe-coder` DAG with its own issue, branch
      `work/<slug>`, PR into `main`, and root `SYNTHESIS.md`; brief names concerns (describe, don't instruct).
   If nothing is foldable-further/landable/unblocked, **fork nothing** — watch and schedule I39. **One
   `engine_fork` per iteration.** `PermissionDenied: missing token 'fork'` is non-retryable — never retry; re-defer.
4. **On each successful LAND:** set that issue's project Status to **Done** (project `PVT_kwDOEB9jls4BlZH4`, Status
   field `PVTSSF_lADOEB9jls4BlZH4zhkGLsc`, option Done=`98236657`; item ids in STATE `engagement.project_item_ids` —
   #8=`PVTI_lADOEB9jls4BlZH4zg-BHUs`, #10=`PVTI_lADOEB9jls4BlZH4zg-BHY4`, #11=`PVTI_lADOEB9jls4BlZH4zg-BHZw`,
   #12=`PVTI_lADOEB9jls4BlZH4zg-BHbE`, #13=`PVTI_lADOEB9jls4BlZH4zg-BHcE`). Append a `work_items[]` entry; bump
   `current_pointer`. Reap the landed code-DAG + its review DAG + any relock DAG (scratch).
5. **Tracked land-then-fix minors from the #8 review (carry forward; do NOT block the land).** The review APPROVE
   recorded 6 minor + 5 nit, all non-blocking: **ARCH-01** (unknown `/api/*` falls through to SPA `index.html` 200
   instead of JSON 404 `ApiError`), **ARCH-02** (fat-repository service tier), **ARCH-03** (F1 `details` generic
   `field:"body"` on the serde-boundary path — ruled acceptable), **TEST-01** (no SPA/static fallback integration
   test), **CRQ-01** (README still documents the old `422` gap, omits the 400 row), **CRQ-02/F2** (rustdoc
   intra-doc-link debt under `RUSTDOCFLAGS=-D warnings`), + nits RUST-01/02/03, TEST-02. The review recommends
   folding CRQ-01 + F2 into the devops/CI work (#10–#13). Consider filing a tracking issue (or folding into the
   devops briefs) once #8 lands; none blocks landing #8.
6. **The recurring lockfile-restale pattern (carry forward).** Every land to `main` moves the base and MAY restale
   the `Cargo.lock` of a still-open sibling PR that branched earlier **and whose lockfile change overlaps** (confirm
   via the live `gh` mergeability poll, not by assumption). After #8 lands and devops PRs open, re-poll each sibling
   and relock any loser via a forked DAG, never inline (P1).
7. **Schedule your own successor** (I39) `depends_on` I38 (plain id `I39`, `dependencies: ["I38"]` — NOT
   `overseer/I39`), author your `CONTINUE.md`, and terminate `completed` / `thread_evaluation: Continue`. Keep the
   chain going until the whole engagement (framework + app + CI + deploy on k3s, reachable) is delivered and the
   board is all Done — only then `Exit`.

## _FORK.md / fork gotchas (learned in I1–I37)
- (a) Create the DAG/overseer workspace directory on the real filesystem BEFORE authoring files into it (the Write
  tool fails silently if the parent dir is absent).
- (b) `_FORK.md` `launch_context` carries only identity context (`application: software`, `model_default`).
  Methodology direction belongs in the forked DAG's `_BRIEF.md` (name the concerns to cover; the DAG loads its own
  methodologies). Do not copy an earlier DAG's methodology choice.
- (c) `disposition` MUST contain the substring `retain` ONLY for things to keep; a code-writing/review/relock DAG is
  scratch so it uses `reap-whole-after-land` (non-retain).
- (d) **One `engine_fork` per overseer iteration.** Multiple forks in one invocation return `PermissionDenied:
  missing token 'fork'` for all but the first (non-retryable). Fork exactly one DAG; hand the rest to successors.
  GRANTED+SUCCEEDED: I8 (#6), I9 (#7), I11 (#5 review), I12 (#6 review), I14 (#7 review), I15 (#6 relock),
  I16 (#8 chirp-server), I17 (#9 chirp-frontend), I29 (#9 review), I33 (#8 review review-chirp-server), I36 (#8
  relock chirp-server-relock-r1). No fork to make: I10, I13, I18–I28, I30, I31 (LANDED #9), I32, I34, I35, **I37 (watch)**.
- (e) The successor-task `engine_amend_plan { add_task }` uses a PLAIN id (`I39`) with `dependencies: ["I38"]` — NOT
  `overseer/I39`/`overseer/I38` (rejected as unresolved/cycle). Chain edge is `I39: [I38]`.
- (f) **Re-poll `gh` mergeability until it is not UNKNOWN before landing.** GitHub computes it asynchronously; NEVER
  land on UNKNOWN; NEVER land CONFLICTING. PR #19 is CONFLICTING until the relock DAG pushes its rebase and folds;
  confirm `OPEN/MERGEABLE/CLEAN` via a live `gh` poll before landing.
- (g) **Gate on the folded root `SYNTHESIS.md` verdict record, not on a side-effect.** A relock DAG that PUSHED a
  rebased branch (making PR #19 mechanically CLEAN) but wrote NO root `SYNTHESIS.md` has NOT folded (the
  ferric-http-relock-r1 I16→I17 precedent). Read the root record body, don't gate on a pushed branch alone.
- (h) A code/relock DAG self-remediating internally is NOT a machine-FAIL you must act on (read the authoritative
  root record).
- (i) A gate record at the DAG ROOT path can be an interim (non-terminal) record — read its body, not mere
  existence. (For #8 review the root `SYNTHESIS.md` body was the authoritative terminal APPROVE at I36.)

## Scope / guardrails (carry every iteration)
Only `Nousix-LLC/nswe-demo` + this project's k3s cluster/namespaces + its ArgoCD. Never force-push `main`; never
rewrite merged history. Changes land as PRs; reviews, devops, bug-fixes, and lockfile relocks/rebases are each their
own forked DAG; bugs are filed as issues. The GitHub Project/issues/PRs are the source-of-truth working record —
keep them current. Drive to: the app running on k3s and reachable, CI green, everything merged, board Done. #8 is
the last app work-item; after it lands only devops #10–#13 remain.
