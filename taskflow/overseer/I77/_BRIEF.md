# _BRIEF.md — NSWE overseer iteration I77 (persona swe-lead) — ESCALATE TO THE USER (systemic fresh-fork dispatch fault)
**Depends on**: I76
**Task Kind**: act — escalate to the user (+ reconcile r1c abandoned, mark items blocked), then schedule a board check

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I74 → I75 → I76 → **I77**). Event loop, **NOT** a code writer — **P1 holds.** **Fileset: `BOARD` + `RETENTION`**
(load both; they govern escalations, blocked markings, and STATE). This is the **action** iteration I76 (the resumed
board-check / dispatch-test evaluation) scheduled: I76 **conclusively resolved** the fresh-fork dispatch test and
decided to escalate. You **enact** that decision; you do not re-open it. Read-only `gh` for confirmation; the only
writes are the escalation, the blocked markings, and STATE. **Never poll a running DAG.**

## What I76 resolved (read I76's `CONTINUE.md` first — this is its enacted decision)
The dispatch test on **`remediate-epic-persist-r1c`** is resolved **FROZEN**. On a fresh clock (~15:34Z, r1c forked
14:58Z → ~37 min) two byte-identical on-disk samples showed the frozen "root never dispatched" signature: only
`_BRIEF.md` + `_FORK.md` at fork time, **no `scheduler/` dir ever created**, no `engine_state`/`req-*`/
`taskflow_workspaces`, no subtasks, no root `SYNTHESIS.md` — zero content growth. The control `design-chirp-r1`
advanced its scheduler decisions log **459 → 480 lines** (mtime ~15:30Z) in the same window, proving the
engine/scheduler machinery is running. **Four** freshly-forked DAGs have now frozen identically — `remediate-epic-persist-r1b`,
the original `design-ferric-1_0`, `design-ferric-1_0-r2`, and now `remediate-epic-persist-r1c` — over windows from
~37 min to ~18h, while the pre-existing reconstructed `design-chirp-r1` keeps advancing. **A 4th blind re-fork would
be grinding.** This is a **systemic fresh-fork dispatch fault**, not a code fault.

## Context carried in (read first)
- **I76's `CONTINUE.md`** (the resolved verdict + the escalate decision you enact). I75's `CONTINUE.md` (r1c re-fork;
  r1b + ferric-r2 abandoned; remediation accounting = **attempt #1 of 2, 0 verdicts spent**). I74's (the dispatch-fault
  diagnosis).
- **Authoritative STATE = `taskflow/overseer/I75/project_state.json`** (snapshot forward to `I77/project_state.json`).
  I64–I66 are dead pre-authored briefs — ignore. No open escalations currently in STATE (F1 + reconstruction anomaly
  both resolved).
- Board (confirmed fresh ~15:34Z, read-only): PR **#113** (`work/epic-persist`) is the **only** open PR, MERGEABLE,
  head `09fa453`, `doc` red / clippy·fmt·test·wasm green (r1c pushed nothing). **No** GitHub activity since 15:00Z.
  Deployment HEALTHY @276138f, no land since.

## What to do (escalation action — `BOARD` + `RETENTION` govern the mechanics)
1. **Open the escalation** per `BOARD.md` "Asking the user" + `RETENTION.md`:
   - **The ask (what only the user can give):** the platform is not picking up newly-launched build/automation work —
     fresh jobs never start — so automated remediation of PR #113 and the #114 design cannot make progress, and the
     project cannot self-heal it with its own tools. Only the owner can clear it.
   - **Clearing condition (concrete, world-testable):** a newly-launched build/automation job **starts and produces
     activity / subtasks** (i.e. new work is being picked up again). Every board check re-tests this against the live
     world (the owner may fix it without commenting).
   - **Where:** record it as an **open escalation in STATE** with that clearing condition, the evidence, and the
     attempt history (r1b/ferric-orig/ferric-r2/r1c). On **GitHub**, this fault is **platform-internal and has no clean
     repository identity** — like the prior reconstruction-anomaly escalation, keep host/taskflow specifics OUT of
     GitHub. If and only if there is a clean repository framing, you MAY post a brief, host-free note on the blocked
     items (PR #113 and/or directive #114) saying automated progress is paused pending the owner — in repository terms
     only ("new automated runs are not being picked up"), no taskflow/host/agent/DAG internals. If no clean framing
     exists, hold the detail in STATE only and do not invent a GitHub artifact. Never ask for a secret in an issue.
2. **Mark the blocked items** on the board (`BOARD.md` hygiene — status matches the world):
   - **PR #113 / the persist goal** (epic **#56**, issues **#65/#66/#67**): **blocked** — remediation cannot be
     dispatched. (#64 stays open as before.) Keep the GitHub-facing wording host-free.
   - **The #114 Ferric 1.0 design**: **blocked** — its design DAG cannot be dispatched (ferric-r2 frozen; no r3 forked,
     deliberately — not grinding).
3. **Reconcile `remediate-epic-persist-r1c` ABANDONED** in STATE (`dispatched_dags` + `dag_slots`): frozen, root never
   dispatched, **no verdict and no commits → does NOT consume the remediation budget** (persist goal stays at
   **attempt #1 of 2, 0 verdicts spent**; do NOT burn attempt #2 on a fault the DAG didn't cause). Left to reap under
   its own `_FORK.md`; do **not** force-cancel (a thread cannot, and a frozen DAG is already stopped). Honest in-flight
   after abandoning r1c = `design-chirp-r1` (LIVE, superseded zombie) = **1 counting; 3 free**.
4. **Snapshot STATE forward** to `taskflow/overseer/I77/project_state.json`: the open escalation + clearing condition,
   r1c abandoned, refreshed `dag_slots`, PR #113 + #114 marked blocked, remediation accounting unchanged (#1/2, 0
   spent), and an `escalation_i77` record.
5. **`design-chirp-r1`** (superseded zombie): standing watch holds — **discard-on-fold, NEVER adopt**; a thread cannot
   stop it. If it has folded on disk (root `SYNTHESIS.md`), record SUPERSEDED, close any duplicate artifacts (expect
   none), let it reap, free its slot — but do not act on it inline here beyond recording; route a fold through a read-a-fold
   evaluation if one is present.

## How to end
Schedule your successor **I78** (a board check, `WORK_SESSION` + `BOARD`) `depends_on` I77, then reach **`continue`**
(the escalation is filed; the successor board check re-tests the clearing condition against the live world each wake).
I78 self-suspends on a **FRESH bounded `any_of` wake** — never an unbounded single wait:

    resumption_condition:
      any_of:
        - { member: schedule, resume_at: "<now + ~20–40m, ISO-8601 UTC>" }
        - { member: forked-thread-completion, forked_thread: "design-chirp-r1" }
      deadline: null

(Only `design-chirp-r1` remains in flight once r1c is abandoned.) On each wake I78 re-tests the escalation's clearing
condition (a fresh fork produces activity), watches `design-chirp-r1` for fold (discard), re-reads the board for new
world activity, and re-confirms deployment. **Do NOT Exit** — the engagement is not complete (PR #113 blocked, #114
design blocked, release bar unmet, `design.standing` null).

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + NSWE Delivery project #1 + its k3s (k3d `nswe`) cluster/namespaces (`chirp*`) + ArgoCD
`chirp`. Never force-push `main`; **no attribution trailers**; **nothing on GitHub carries host/system/taskflow
details** — translate host facts to repository identities, and hold the platform dispatch-fault detail in STATE only.
