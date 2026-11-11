# _BRIEF.md — NSWE overseer iteration I73 (persona swe-lead) — RECOVER the frozen Ferric 1.0 design DAG
**Depends on**: I72
**Task Kind**: action — "Launch a design DAG" (recovery re-fork)

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I70 → I71 → I72 → **I73** → I74). Event loop, **NOT** a code writer — **P1 holds**: you brief and fork a
DAG; you never design the product or write code inline. Boot the kernel + NSWE app-files, publish
`thread_evaluation`, then Act. **Fileset: `PRODUCT_DESIGN` + `WORK_SESSION`** (+ `DELIVERABLES_GIT` only if you
need repo identities). An **action does one thing and schedules the evaluation that follows it.**

## Why this task exists (decided by I72's board check)
On a fresh clock (2026-10-27T21:08:38Z) I72 re-evaluated all in-flight DAGs and confirmed **`design-ferric-1_0`
is genuinely FROZEN**: its scheduler last advanced local 2026-10-22 09:49 (= 16:49Z Oct-22), newest content file
same, **no root `SYNTHESIS.md`**, ~5 days with zero progress — unlike `design-chirp-r1`, whose scheduler was LIVE
at 21:08Z. This is the fresh-clock confirmation I69/I70/I71 asked for. Per the thread-pacing rule ("Frozen / not
progressing → RECOVER, do NOT wait again") the call is **recover**, not keep-watching.

## What to do
1. **Re-confirm frozen on YOUR fresh clock first** (same discipline I70 used for chirp — never force-abandon a
   live DAG). Sample `taskflow/dags/design-ferric-1_0/scheduler/logs/scheduler_decisions.jsonl` and the newest
   content mtime twice a few seconds apart. If it has started progressing again → it is a standing watch, record
   that and **pass on** (schedule I74, do not re-fork). If it has **folded** (root `SYNTHESIS.md` now present) →
   this is a "Triage a design" not a recovery: adopt it per `PRODUCT_DESIGN` + `BOARD` instead of re-forking.
   Only if still frozen do steps 2–4.
2. **Check a free DAG slot before forking** (`WORK_SESSION`, "At most four DAGs in flight"). Honest in-flight at
   I72: `design-chirp-r1` (LIVE) + `remediate-epic-persist-r1b` (just forked) = 2 live; `design-ferric-1_0` is
   the frozen one you are abandoning (stops counting). So a re-fork fits (≥1 free). If slots filled since,
   record the launch waiting and pass on to I74.
3. **Reconcile the frozen `design-ferric-1_0` as abandoned**: record it dead/stalled in STATE `dispatched_dags`
   (frozen 5 days, no verdict → like the I65 orphan I69 reconciled-dead; it does not count against anything and
   produced no design to adopt), stop counting its slot, and let it be reaped under its own `_FORK.md` policy.
   You cannot stop a DAG from a thread; a frozen one is already stopped — do not force-cancel.
4. **Fork a fresh `swe-designer` design DAG** for the **Ferric 1.0** directive, **carrying forward** the partial
   design the frozen DAG already produced so work is not lost. Inputs to name in its brief:
   - **Directive #114** (`type:feature,human-directive`, 2026-10-22): "design and build Ferric to a 1.0
     framework, with server-side …" — read the live issue body for the full directive; it is the objective.
   - The frozen DAG's **partial outputs** as prior art to build on, not redo: the folded
     `SUBTASK_router_and_http/SYNTHESIS.md` and the content files `router-and-http.md`, `async-forms-events.md`,
     `authoring-model.md`, `release-and-distribution.md`, plus its `_GLOBAL.md`/`_BRIEF.md` scope. (These are
     taskflow-internal paths — read them to inform the brief; **translate everything that reaches GitHub to
     repository identities**, never host/taskflow paths.)
   - Reconcile against what already exists so you do not duplicate: the existing `ferric-foundation` /
     `ferric-http` / `ferric-router` DAGs and any landed Ferric work, and the brief's note of a Ferric epic #1 /
     router / HTTP already on a board. Confirm whether #114's design belongs on **this** project's board
     (NSWE Delivery #1) — your scope is `Nousix-LLC/nswe-demo` + project #1; do **not** touch the separate
     `Ferric Delivery` project #4 or any sibling repo.
   - **Declared output** of the design DAG: a design PR, its tickets placed on the board (de-duped vs existing
     Ferric items), the **Ferric 1.0 release bar**, and a root `SYNTHESIS.md`.
   - Write the brief to **describe concerns, not instruct method**; the DAG selects its own methodology. `_FORK.md`
     = launch agent **`swe-designer`**, `reap-whole-after-land`, identity-level `launch_context`
     (`application: software`) only — no methodology, no decomposition verdict.
5. **Record** on the board and in STATE: the recovery launch, the abandoned frozen DAG, refreshed `dag_slots`
   (as-of, in-flight, free), and that #114's design is (re)in-flight. Assign nothing to code yet — this is design.

## How to end
You are an **action** iteration; your successor **I74** (board check + home return) is already scheduled by I72
and exists on disk (`depends_on I73`). So author **no** successor and do **not** suspend — do this one task and
reach **`continue`** (write `I73/CONTINUE.md`, publish `status: completed, thread_evaluation: Continue`), letting
I74 run. If step 1 found the DAG progressing or folded, record that outcome instead and still reach `continue`.

## Exit decision — do NOT Exit
The engagement is complete only when the product meets the release bar its design set (confirmed by a gap
review), everything is merged and delivered, and the board is Done. Not now. Continue the chain.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + project #1 + its k3s cluster/namespaces (`chirp*`) + ArgoCD `chirp`. Never
force-push `main`; **no attribution trailers**; **nothing on GitHub carries host/system/taskflow details** —
translate host facts to repository identities. Never an inline fix; never poll a running DAG.
