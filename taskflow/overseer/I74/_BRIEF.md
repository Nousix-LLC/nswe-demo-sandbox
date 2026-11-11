# _BRIEF.md — NSWE overseer iteration I74 (persona swe-lead) — BOARD CHECK (home return, paced)
**Depends on**: I73
**Task Kind**: evaluate — board check / home return

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I71 → I72 → I73 → **I74**). Event loop, **NOT** a code writer — **P1 holds.** Boot the kernel + NSWE
app-files, publish `thread_evaluation`, then Act. **Fileset: `WORK_SESSION` + `BOARD`** (+ others as the check
routes). An **evaluation decides and schedules; it does not act/fork.** Read-only `gh`/`kubectl`/`curl` on a
**FRESH clock**. **Never poll a running DAG** — gate only on each folded ROOT `SYNTHESIS.md`.

## Context carried in (read first)
- I72's `CONTINUE.md`/`SUSPENSION.md` (this board check's fresh-clock findings) and I73's `CONTINUE.md` (what the
  Ferric recovery did). Authoritative STATE is the newest `taskflow/overseer/I7x/project_state.json` (I73's if it
  wrote one, else I71's). The I64–I66 dirs are dead pre-authored briefs — ignore them.

## What to evaluate (re-evaluate every in-flight DAG FIRST, fresh clock, gate only on root `SYNTHESIS.md`)
1. **remediation #1** `remediate-epic-persist-r1b` (PR #113 `work/epic-persist`, head was `09fa453`): at I72
   (21:08Z) it was ~19 min old with **no scheduler/subtasks yet** — too early to call frozen. **Re-check now:**
   progressing → keep pacing; **folded** → machine gate (PASS → schedule a review-launch task, `REVIEW_GATE`;
   FAIL → **remediation #2**, the LAST automatic attempt, budget 2, then escalate to the user with both attempts);
   **still zero progress / frozen on your fresh clock** → RECOVER (re-fork carrying the lesson), do not wait again.
2. **Ferric 1.0 design** (recovered by I73): read I73's result. If I73 re-forked a fresh `swe-designer` design
   DAG → watch it; on fold → **Triage a design** (`PRODUCT_DESIGN` + `BOARD`): place tickets under the Ferric
   epic, de-dupe vs existing Ferric items, design PR to review, record the Ferric 1.0 release bar. If I73 instead
   found the old DAG progressing/folded, act on what it recorded.
3. **`design-chirp-r1`** (superseded zombie): LIVE at 21:08Z, discard-on-fold **never adopt** (redundant to
   landed PR #33). Folded → close any duplicate artifacts (expect none), record SUPERSEDED, let it reap, free its
   slot. Still progressing → standing watch holds (a thread cannot stop it). Long-quiet → discards cleanly.
4. **Board**: PR #113 mergeability (landing still waits on remediation → `doc` green + mergeable/clean + an
   APPROVE re-review; current verdict REQUEST-CHANGES); #115–#121 groomed under epic #56 (re-check #118's doc-link
   items on any PR #113 land); every repo issue a board item (I72 reconciled: all 93 open issues on board, none
   stale-Done); any open escalation's clearing condition (none open at I72); whether the backlog still leads to
   the release bar (`design.standing` null — a chirp gap review is a candidate only once PR #113 settles AND no
   design DAG is in flight).
5. **Deployment**: HEALTHY @276138f at last check; no land since (PR #113 unlanded) → a deployment check is only
   called for after a land (`DEPLOYMENT`).
6. **Slots / waiting launches**: a freed slot goes to the highest-priority waiting launch, then new work in
   board-check order. A **new code-goal** launch is a candidate once PR #113 and the #114 Ferric design settle. A
   chirp **gap review** is a candidate once PR #113 settles AND no design DAG is in flight.

## How to end
Schedule what the check calls for (the next task or the series you can see, ending in another board check), then,
as a **`Continue`** iteration, **self-suspend on a FRESH bounded `any_of` wake** — never an unbounded single wait:

    resumption_condition:
      any_of:
        - { member: schedule, resume_at: "<now + ~20–40m, ISO-8601 UTC>" }
        - { member: forked-thread-completion, forked_thread: "<each still-in-flight DAG id>" }
      deadline: null

Re-evaluate on each wake. If an actionable fold is present, do NOT re-suspend — reach `continue` and advance to
the scheduled follow-on. If nothing needs action and no DAG is in flight, suspend until the next board check on
the short interval.

## Exit decision — do NOT Exit
The engagement is complete only when the product meets the release bar its design set (confirmed by a gap
review), everything is merged and delivered, and the board is Done. Until then, continue the chain.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + project #1 + its k3s cluster/namespaces (`chirp*`) + ArgoCD `chirp`. Never
force-push `main`; **no attribution trailers**; **nothing on GitHub carries host/system/taskflow details** —
translate host facts to repository identities.
