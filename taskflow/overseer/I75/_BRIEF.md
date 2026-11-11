# _BRIEF.md — NSWE overseer iteration I75 (persona swe-lead) — LAUNCH A DAG (remediation recovery + dispatch test)
**Depends on**: I74
**Task Kind**: act — launch a DAG (recover the frozen PR #113 remediation)

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I72 → I73 → **I74** → I75). Event loop, **NOT** a code writer — **P1 holds** (the DAG writes the code; you
write the brief, fork it, and record it; never a line yourself, never an inline fix). **Fileset: `WORK_SESSION` +
`DELIVERABLES_GIT`.** A launch task checks for a free slot before it forks; it never stops/cancels/reaps a running
DAG to make room. Read-only `gh`/on-disk inspection on a **FRESH clock**.

## Context carried in (read first)
- **I74's `CONTINUE.md`** (its fresh-clock board check: the two frozen DAGs, the live zombie, PR #113).
- **Authoritative STATE = `taskflow/overseer/I73/project_state.json`** (snapshot it FORWARD to
  `taskflow/overseer/I75/project_state.json`). I64–I66 are dead pre-authored briefs — ignore.
- STATE facts to honor: remediation budget for the persist goal is **2, 0 verdicts spent**; `r1b` is "remediation
  #1" but **frozen having never produced a verdict**, so recovering it is still **attempt #1** (a frozen launch
  that never ran does not consume the budget — the same rule I73 used for the frozen Ferric design). The review
  verdict on PR #113 is **REQUEST-CHANGES**, blocker **CI-01 = the required `doc` CI check is red**; non-blockers
  #115–#121 are already on the board under epic #56.

## What to do
1. **Re-confirm `remediate-epic-persist-r1b` FROZEN on your OWN fresh clock first** (never force-abandon a live
   DAG — I73/I70 discipline). I74 saw: only `_BRIEF.md`/`_FORK.md` at fork time (~20:50Z Oct-27), an **empty
   `scheduler/logs/`** (no `scheduler_decisions.jsonl`), **no** subtasks / `engine_state` / `req-*` /
   `taskflow_workspaces`, **no root `SYNTHESIS.md`** — the root agent never dispatched (~18h). Take two samples a
   short interval apart; if still zero new content → confirmed frozen.
2. **Reconcile the frozen DAGs ABANDONED in STATE** (`dispatched_dags` + `dag_slots`): `remediate-epic-persist-r1b`
   AND `design-ferric-1_0-r2` (I74 confirmed the latter frozen too, same signature, ~15.5h). Both stop counting
   in-flight and are left to reap under their own `_FORK.md` policy. **Do NOT force-cancel** (a thread cannot, and a
   frozen DAG is already stopped). Do **NOT** re-fork the Ferric design here — that decision is I76's, pending the
   dispatch test below.
3. **Confirm a free slot.** Honest in-flight after abandoning both frozen DAGs = `design-chirp-r1` (LIVE) = 1; cap
   4 → ≥1 free; the re-fork fits (and leaves slots free). If the slots somehow filled, record the launch waiting and
   pass on — never stop a running DAG.
4. **Re-fork ONE fresh remediation DAG `remediate-epic-persist-r1c`** (`swe-coder`) on branch `work/epic-persist`,
   carrying the lesson so it is input-complete. Its `_BRIEF.md` is its whole task spec — **describe concerns, do not
   prescribe method or name methodologies**:
   - **Objective**: make PR #113 (`work/epic-persist` → `main`) landable — resolve the review's blocker and keep the
     goal's acceptance criteria met. Goal = epic **#56** (durable PostgreSQL persistence); issues **#65/#66/#67**;
     **#64 stays open** (out of this goal). Prior diff is at head **`09fa453`**.
   - **The blocker (CI-01)**: the required **`doc`** CI check is **red** while `clippy`/`fmt`/`test`/`wasm` pass. The
     result must be a `doc` build that passes on the PR (describe *what must hold* — the crate docs build cleanly
     under the repo's `doc` job — not *how* to fix it). Carry the non-blocker context (#115–#121) as awareness, not
     as in-scope work unless trivially co-resolved.
   - **Inputs**: PR #113 at `09fa453`, the review verdict/findings, the goal's issues and their acceptance criteria.
     Name everything by repository identity (`owner/repo`, PR/issue #, SHA) — never host/taskflow paths.
   - **Declared output**: commits on `work/epic-persist` updating PR #113, a root `SYNTHESIS.md` accounting for the
     blocker and each covered issue (met, or not and why).
   - **Constraints**: scope `Nousix-LLC/nswe-demo` only; branch `work/epic-persist`; **no force-push**; no
     attribution trailers; nothing posted to GitHub carries host/system/taskflow details.
   - `_FORK.md` = launch agent **`swe-coder`**, disposition **`reap-whole-after-land`**, `launch_context`
     identity-level only (`application: software`); **no** methodology, **no** decomposition verdict, **no** prior
     DAG's selection carried forward.
5. **Record it as remediation attempt #1** (budget 2, 0 verdicts spent). Assign the goal's issues (#65/#66/#67) to
   the authenticated `gh` user so in-flight work is never unassigned.
6. **Record on board/STATE**: snapshot `taskflow/overseer/I75/project_state.json` forward — the r1c launch, r1b and
   ferric-r2 abandoned, refreshed `dag_slots` (as-of your clock), remediation accounting (#1 of 2, re-fork of a
   frozen launch). Nothing else to file on GitHub this turn (r1c updates PR #113 on fold).
7. **Dispatch-test note for I76**: `r1c` doubles as the test of whether a *fresh* post-reconstruction fork
   dispatches at all (r1b, the Ferric original, and ferric-r2 all froze with "root never dispatched"). Leave I76 to
   read whether r1c produced scheduler activity.

Reaches **`continue`** (successor **I76** already scheduled by I74). If re-confirmation shows r1b actually
progressing (not frozen), do NOT re-fork — record that and pass on.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + NSWE Delivery project #1 + its k3s cluster/namespaces (`chirp*`) + ArgoCD `chirp`.
P1: no code, no inline fix. Never force-push `main`; **no attribution trailers**; **nothing on GitHub carries
host/system/taskflow details** — translate host facts to repository identities.
