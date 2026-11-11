# _BRIEF.md — NSWE overseer iteration I58 (persona swe-lead) — LAUNCH a review of PR #113
**Depends on**: I57

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I56 → I57 → **I58**). You are an event loop, **NOT** a code writer — **P1: you never write, edit,
patch, rebase, relock, or design inline; every engineering act is a forked DAG.** Boot the kernel + the NSWE
app-files, publish `thread_evaluation`, then do this iteration's Act.

**This turn's filesets: `REVIEW_GATE` + `WORK_SESSION` (+ `DELIVERABLES_GIT` as needed).** This is an
**action**: *launch a review* — write the review brief from the review gate and fork one review DAG
(`swe-reviewer`) for **PR #113**. An action does one thing and schedules the evaluation that follows it.

## What to do
1. **Re-check the slot budget before forking** (`WORK_SESSION`, "At most four DAGs in flight"): confirm
   `< 4` DAGs in flight. The superseded `design-chirp-r1` zombie counts as 1; after launch there must still
   be `≤ 4`. If no slot is free, record the launch in STATE `waiting_launches` and pass on (do NOT stop/reap
   a running DAG). Your I58 fork token is FRESH (one `engine_fork` this iteration).
2. **Re-poll PR #113 live** (read-only `gh`): confirm it is still OPEN, `mergeable != UNKNOWN`, head
   `work/epic-persist`, author `mattsmcknight`, and still has **no review**. Note the live CI rollup — at
   I57 the `doc` check was **FAILING** (clippy/fmt/test/wasm PASS), so `mergeState=UNSTABLE`. The PR is
   **not clean to land** while a required check fails; the review must call this out, and landing waits on it.
3. **Write the review `_BRIEF.md`** from `REVIEW_GATE` (describe, do not instruct). Name as distinct concerns
   what the review must evaluate — correctness of the durable-persistence change against the issues it closes
   (persistence epic #56: #64 durable store, #65 invariants/counts/ids under concurrency, #66 ChirpRepository
   seam, #67 retention/durability drill — read the PR to confirm which it claims to close), the design-of-record
   it must trace to (`design/domain-application-design.md` durable-persistence requirement, `design/release-bar.md`
   `BAR-*`), code quality, test coverage/durability proof, and security — each with the bar it is held to and
   what counts as a finding. Include the **failing `doc` CI check** as a concern to diagnose. The DAG selects
   and loads its own methodologies; do NOT name bundles or put methodology in `_FORK.md`/`launch_context`.
   `_FORK.md`: launch agent `swe-reviewer`, `reap-whole-after-land`, `launch_context: {application: software}`.
4. **Fork** the review DAG into a free slot; record it in STATE `dispatched_dags` (slug e.g.
   `review-epic-persist`, kind `review`, the PR, its branch, workspace, observation seam its root
   `SYNTHESIS.md`), and make sure PR #113 shows **In review** on the board (that is the follow-up board task's
   job if not done here).
5. **Schedule the successor** (`I59` depends_on `I58`): the next task in the series — the **deployment check**
   (see the series plan carried in I57). Write its brief fresh.

## Carried state (read first)
- `taskflow/overseer/I57/project_state.json` — STATE as of the I57 re-home board check (design record
  reconciled; zombie standing watch; the scheduled series).
- `taskflow/overseer/I57/CONTINUE.md` — I57's terminal record (the full board-check findings + the series plan).

## Gotchas
- (d) One `engine_fork` per iteration; confirm `< 4` DAGs in flight first (zombie = 1). A reconstructed
  instance shares a spent token — if a prior I58 already forked the review, do NOT re-fork; pick up its fold.
- (f) Re-poll `gh` mergeability until not `UNKNOWN` before anything lands; never land `UNKNOWN`/`CONFLICTING`
  or with a failing required check.
- (g) Gate on a folded ROOT `SYNTHESIS.md` body, never a side-effect. (gh-review) `gh pr review --approve` is
  rejected on your own org's PR authored by the owner — post the verdict as a PR **comment** + inline.

## Exit decision — do NOT Exit
The engagement is not complete (PR #113 unreviewed, #114 unaddressed, backlog open, zombie to discard,
deployment to re-verify, `design.standing` null). Continue the chain.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + its k3s (k3d `nswe`) cluster/namespaces (`chirp*`) + its ArgoCD Application
`chirp`. Never force-push `main`; **no attribution trailers** on commits or PR bodies. **Nothing on GitHub
carries host/system details** — translate host facts to repository identities.
