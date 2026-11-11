# _BRIEF.md — NSWE overseer iteration I67 (persona swe-lead) — BOARD CHECK (paced, home-return)
**Depends on**: I66

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I65 → I66 → **I67**). You are an event loop, **NOT** a code writer — **P1 holds.** Boot the kernel + the
NSWE app-files, publish `thread_evaluation`, then Act. This is the terminal board check of the I63-scheduled
series (I64 process-review → I65 remediation #1 → I66 groom → **I67**).

**This turn's filesets: `WORK_SESSION` + `BOARD` (+ others as the check routes).** A paced home-return board
check. An **evaluation decides and schedules; it does not act/fork itself.** Read-only `gh`/`kubectl`/`curl` on a
**FRESH clock**. Never poll a running DAG — gate only on each folded ROOT `SYNTHESIS.md`.

## Context carried in (read first)
- `taskflow/overseer/I66/project_state.json` — latest STATE (after the I64/I65/I66 series).
- The `I64`–`I66` `CONTINUE.md` records — what the series did (review processed, remediation #1 launched/queued,
  backlog groomed).

## What to evaluate
1. **Re-evaluate every in-flight DAG FIRST** (fresh clock; gate only on root `SYNTHESIS.md`):
   - **remediation #1** on `work/epic-persist` (forked at I65, if a slot was free) — on fold → machine gate: PASS
     → the PR is up for **re-review** (launch a review DAG, `REVIEW_GATE`); FAIL → **remediation #2** (the LAST
     automatic attempt, budget 2; then escalate to the user with both attempts). A fold re-enters at the machine
     gate. If I65 recorded it **waiting** (no free slot), check for a freed slot now and launch it.
   - **`design-ferric-1_0`** (#114, under Ferric epic #1) — on fold → **Triage a design** (`PRODUCT_DESIGN` +
     `BOARD`): adopt — tickets under epic #1, de-dupe vs router #5 / HTTP #6, design PR to review, record the
     Ferric 1.0 release bar.
   - **`design-chirp-r1`** (SUPERSEDED zombie) — on fold → **triage-and-discard** (do NOT land/adopt): close any
     duplicate PR/epics/BAR/feature issues it filed against the landed #33 board, record `SUPERSEDED`, let it reap
     whole, free its slot. If still progressing on a fresh clock, leave it a standing watch. If frozen (no
     progress on a fresh clock, not a mere dormancy gap) → discard, do not re-fork. As of I63 it was still
     progressing with ZERO GitHub writes (`SUBTASK_design_pr`/`SUBTASK_delivery_backlog` untouched since Oct 9) —
     catch and close any duplicates the moment they appear.
2. **Board check**: new/edited issues, comments on issues and PRs, reviews posted by anyone; open PRs and
   mergeability (**PR #113** still the live one — after remediation #1: expect `doc` to go green and the PR
   mergeable/clean; landing still waits on an **APPROVE** — current verdict is REQUEST-CHANGES until re-review);
   which DAGs folded/failed and the free-slot count; whether the board says what is true (every repo issue a
   board item, #115–#121 placed under #56); whether any open escalation's clearing condition now holds (none open
   at I63); whether the backlog still leads to the release bar.
3. **Deployment**: HEALTHY @276138f at I59; fold in anything a deployment check defers. A land since the last
   check (none yet — PR #113 not landed) calls for a deployment check (`DEPLOYMENT`).
4. **Slots / waiting launches**: a freed slot (zombie reaped, a design folded) goes to the highest-priority
   waiting launch, then to new work in board-check priority order. A **gap review** of the live product against
   the bar (`design.standing` null) is a candidate once PR #113 settles AND no other design DAG is in flight
   ("one design DAG at a time" — `design-ferric-1_0` is in flight). A **code-goal** launch is a candidate once
   #114's design and PR #113 settle. Until then free slots are reserved for the in-flight folds' follow-on work.

## How to end this turn
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
Only `Nousix-LLC/nswe-demo` + its k3s cluster/namespaces (`chirp*`) + ArgoCD `chirp`. Never force-push `main`;
**no attribution trailers**; **nothing on GitHub carries host/system details** — translate host facts to
repository identities.
