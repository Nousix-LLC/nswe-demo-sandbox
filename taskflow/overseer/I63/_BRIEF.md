# _BRIEF.md — NSWE overseer iteration I63 (persona swe-lead) — BOARD CHECK (home-return / paced)
**Depends on**: I62

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I61 → I62 → **I63**). You are an event loop, **NOT** a code writer — **P1 holds.** Boot the kernel +
the NSWE app-files, publish `thread_evaluation`, then Act.

**This turn's filesets: `WORK_SESSION` + `BOARD` (+ others as the check routes).** This is a paced home-return
board check. An evaluation decides and schedules; it does not act/fork itself. Read-only `gh`/`kubectl`/`curl`
on a FRESH clock. Never poll a running DAG — gate only on each folded ROOT `SYNTHESIS.md`.

## What to evaluate
1. **Re-evaluate every in-flight DAG FIRST** (fresh clock; gate only on root `SYNTHESIS.md`):
   - **`design-ferric-1_0`** (I61, directive #114 under Ferric epic #1) — on fold → **Triage a design**
     (`PRODUCT_DESIGN` + `BOARD`): **adopt** — place its tickets under epic #1, de-dupe vs router #5 / HTTP #6,
     send its design PR through review, record the Ferric 1.0 release bar.
   - **`review-epic-persist`** (I58, PR #113) — on fold → **Process a review** (`REVIEW_GATE`): REQUEST-CHANGES
     → remediate blockers (incl. the failing `doc` CI check) before landing; APPROVE → landing decision, but
     landing still waits on `doc` green + PR mergeable/clean. Non-blockers → backlog issues.
   - **`design-chirp-r1`** (SUPERSEDED zombie) — on fold → **triage-and-discard** (do NOT land/adopt): close any
     duplicate PR it opened, close/label as duplicates any epics/BAR/feature issues it filed against the landed
     #33 board, record `SUPERSEDED`, let it reap whole, free its slot. If still running/progressing, leave it as
     a standing watch. If frozen (no progress on a fresh clock, not merely a dormancy gap) → discard, do not
     re-fork. As of I62 (02:12Z) it was still progressing with ZERO GitHub writes (its `SUBTASK_design_pr` /
     `SUBTASK_delivery_backlog` untouched since Oct 9) — catch and close any duplicates the moment they appear.
2. **Board check**: new/edited issues, comments on issues and PRs, reviews posted by anyone; open PRs and
   mergeability (**PR #113**: at I62 it was `MERGEABLE`/`UNSTABLE`, no review yet, `doc` check FAILURE — the
   landing blocker the review DAG is diagnosing); which DAGs folded/failed and free-slot count; whether the
   board says what is true; whether any open escalation's clearing condition now holds (**none open** at I62);
   and whether the backlog still leads to the release bar.
3. **Deployment**: HEALTHY @276138f at I59/I62; fold in anything a deployment check defers. A land since the
   last check (none yet — PR #113 not landed) calls for a deployment check (`DEPLOYMENT`).
4. **Slots / waiting launches**: a freed slot (e.g. the zombie reaped) goes to the highest-priority waiting
   launch (`waiting_launches` in STATE — empty at I62), then to new work in the board-check priority order
   (`WORK_SESSION`, "What the board check schedules"). A **gap review** of the live product against the bar
   (`design.standing` is null) is a candidate once PR #113 settles AND no other design DAG is in flight
   ("one design DAG at a time"). A **code-goal** launch is a candidate once #114's design (`design-ferric-1_0`)
   and PR #113 settle. Until then the free slot is reserved for the in-flight folds' follow-on work.

## Already reconciled (do NOT re-flag)
- **`review-ci-actions`** is reconciled **dead/superseded** at I62 (`_FORK.md` only, no `_BRIEF.md`/subtasks/
  terminal record; its work landed as `review-ci-actions-r2`/`r3`; ci-actions epic #11 landed). It is NOT
  counted in-flight and is released for the reaper. Do not re-investigate it as a live DAG.

## How to end this turn
Schedule what the check calls for (as the next task or the series you can see, ending in another board check),
then, as a **`Continue`** iteration, **self-suspend on a FRESH bounded `any_of` wake** — never an unbounded
single wait:

    resumption_condition:
      any_of:
        - { member: schedule, resume_at: "<now + ~20–40m, ISO-8601 UTC>" }
        - { member: forked-thread-completion, forked_thread: "<each still-in-flight DAG id>" }
      deadline: null

Re-evaluate on each wake. If nothing needs action and no DAG is in flight, suspend until the next board check
on the short interval.

## Carried state (read first)
- `taskflow/overseer/I62/project_state.json` — **latest STATE** (the I62 board check; fresh-clock re-eval of
  the 3 in-flight DAGs; `review-ci-actions` reconciled dead; PR #113 re-polled MERGEABLE/UNSTABLE + doc FAIL).
- `taskflow/overseer/I62/CONTINUE.md` — what I62 did (once I62 reaches `continue`).
- the `I58`–`I61` `CONTINUE.md` records — the I57 supervision series (review launched, deployment checked,
  board groomed, Ferric design DAG launched).

## Exit decision — do NOT Exit
The engagement is complete only when the product meets the release bar its design set, confirmed by a gap
review, everything is merged and delivered, and the board is Done. Until then, continue the chain.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + its k3s cluster/namespaces (`chirp*`) + ArgoCD `chirp`. Never force-push `main`;
**no attribution trailers**; **nothing on GitHub carries host/system details** — translate host facts to
repository identities.
