# _BRIEF.md — NSWE overseer iteration I76 (persona swe-lead) — BOARD CHECK (home return, paced)
**Depends on**: I75
**Task Kind**: evaluate — board check / home return

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I73 → I74 → I75 → **I76**). Event loop, **NOT** a code writer — **P1 holds.** **Fileset: `WORK_SESSION` +
`BOARD`** (+ others as the check routes). An **evaluation decides and schedules; it does not act/fork.** Read-only
`gh`/`kubectl`/`curl` on a **FRESH clock**. **Never poll a running DAG** — gate only on each folded root
`SYNTHESIS.md`.

## Context carried in (read first)
- **I75's `CONTINUE.md`** (the remediation recovery: whether `remediate-epic-persist-r1c` was re-forked, its id,
  and the r1b/ferric-r2 abandonment). I74's `CONTINUE.md` (the frozen-DAG diagnosis + dispatch-test rationale).
- **Authoritative STATE = newest `taskflow/overseer/I7x/project_state.json`** (I75's if it wrote one, else I73's).
  I64–I66 are dead pre-authored briefs — ignore.

## What to evaluate (re-evaluate every in-flight DAG FIRST, fresh clock, gate only on root `SYNTHESIS.md`)
1. **DISPATCH TEST — `remediate-epic-persist-r1c`** (the critical thing this check decides). Did the *fresh* re-fork
   actually dispatch? Look for genuine root activity: a non-empty `scheduler/logs/scheduler_decisions.jsonl`,
   `engine_state` / `req-*` / `taskflow_workspaces` dirs, subtasks, growing content. (Contrast the frozen signature:
   `_BRIEF.md`/`_FORK.md` + empty `scheduler/logs/` only, no decisions log, for 15–18h.) Take two samples a short
   interval apart.
   - **Progressing / dispatched** → fresh forks work post-reconstruction. **(a)** Keep pacing r1c; on its fold →
     machine gate (PASS → schedule a review-launch task, `REVIEW_GATE`; FAIL → **remediation #2**, the LAST
     automatic attempt, budget 2, then escalate to the user with both attempts). **(b)** Schedule the **Ferric 1.0
     design recovery**: a "Launch a design DAG" task (`PRODUCT_DESIGN` + `WORK_SESSION`) that abandons the frozen
     `design-ferric-1_0-r2`, confirms a free slot, and re-forks a fresh `swe-designer` DAG (e.g.
     `design-ferric-1_0-r3`) for directive **#114**, carrying forward the prior art again
     (`taskflow/dags/design-ferric-1_0-r2/prior-art/` survives the reaping) — adopt-on-fold → Triage a design.
   - **Still zero progress / frozen (same signature)** → this is a **SYSTEMIC dispatch fault**: freshly-forked DAG
     roots are not being dispatched (r1b, the Ferric original, ferric-r2, and now r1c all froze "root never
     dispatched" while the older `design-chirp-r1` runs normally). Do **NOT** re-fork a third time — that is
     grinding. Schedule an **escalation to the user** (`BOARD` + `RETENTION`): state what was tried and the
     observable evidence (newly-forked DAGs show no scheduler activity for many hours while a pre-existing DAG
     advances), and give a concrete clearing condition (a re-forked DAG produces scheduler activity / subtasks).
     Mark the persist goal (PR #113) and the #114 Ferric design **blocked**. Keep host/taskflow specifics out of
     GitHub — frame the ask for the owner in repository terms (new build/automation work is not being picked up),
     or hold the platform-internal detail in STATE only if it has no clean repository framing.
2. **`design-chirp-r1`** (superseded zombie, redundant to landed PR #33): discard-on-fold, **never adopt**. Still
   progressing → standing watch holds (a thread cannot stop it). **Folded** (root `SYNTHESIS.md` appears) → record
   SUPERSEDED, close any duplicate artifacts (expect none), let it reap, free its slot.
3. **PR #113** (`work/epic-persist`, head `09fa453` until r1c pushes): landing still waits on remediation → `doc`
   green + mergeable/clean + an **APPROVE** re-review (current verdict REQUEST-CHANGES). Re-check #118's doc-link
   items only on a PR #113 land.
4. **Board**: new issues/comments/reviews since ~21:05Z Oct-27 (I74 saw none new; 93 open issues, all board items,
   none stale-Done); every repo issue a board item (periodic reconciliation sweep); any open escalation's clearing
   condition (none open at I74 unless step 1 opened one); whether the backlog still leads to the release bar
   (`design.standing` null — a chirp gap review is a candidate only once PR #113 settles AND no design DAG is in
   flight).
5. **Deployment**: HEALTHY @276138f at last check; no land since → a deployment check is only called for after a
   land (`DEPLOYMENT`).
6. **Slots / waiting launches**: a freed slot goes to the highest-priority waiting launch, then new work in
   board-check order. New code-goal / chirp gap-review launches remain candidates only once PR #113 and the #114
   Ferric design settle.

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
The engagement is complete only when the product meets the release bar its design set (confirmed by a gap review),
everything is merged and delivered, and the board is Done. Until then, continue the chain.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + project #1 + its k3s cluster/namespaces (`chirp*`) + ArgoCD `chirp`. Never
force-push `main`; **no attribution trailers**; **nothing on GitHub carries host/system/taskflow details** —
translate host facts to repository identities.
