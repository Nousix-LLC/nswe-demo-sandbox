# _BRIEF.md — NSWE overseer iteration I62 (persona swe-lead) — BOARD CHECK (home return / re-arm)
**Depends on**: I61

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I60 → I61 → **I62**). You are an event loop, **NOT** a code writer — **P1 holds.** Boot the kernel +
the NSWE app-files, publish `thread_evaluation`, then Act.

**This turn's filesets: `WORK_SESSION` + `BOARD` (+ others as the check routes).** This is the **home-return
board check** that closes the I57-launched supervision series and re-arms the chain. An evaluation decides and
schedules; it does not act/fork itself. Read-only `gh`/`kubectl`/`curl` on a FRESH clock.

## What to evaluate
1. **Re-evaluate every in-flight DAG FIRST** (gotcha g/i/j, fresh clock):
   - the **`design-chirp-r1` zombie** — if its root `SYNTHESIS.md` has appeared, it folded: **triage-and-discard**
     (do NOT land/adopt — close any duplicate PR it opened, close/label as duplicates any epics/BAR/feature
     issues it filed against the existing landed #33 board, record `SUPERSEDED`, let it reap whole, free its
     slot). If it wrote duplicates to GitHub, catch and close them. If still running/progressing, leave it as a
     standing watch. If frozen (no progress on a fresh clock, not merely a dormancy gap) → it is to be discarded,
     not re-forked.
   - the **review DAG** (I58, PR #113) and the **Ferric-1.0 design DAG** (I61) — read each only via its root
     `SYNTHESIS.md` if present; a fold routes to processing/triage (`REVIEW_GATE` / `PRODUCT_DESIGN`). Never poll.
2. **Board check**: new/edited issues, comments on issues and PRs, reviews posted by anyone; open PRs and
   whether they can merge (PR #113 — re-poll until not `UNKNOWN`; the `doc` CI check was failing at I57); which
   DAGs folded/failed and how many are in flight (free slots); whether the board says what is true; whether any
   open escalation's clearing condition now holds (none open at I57); and whether the backlog still leads to the
   release bar.
3. **Deployment**: fold in anything the I59 deployment check deferred.
4. **Slots / waiting launches**: a freed slot (e.g. the zombie reaped) goes to the highest-priority waiting
   launch (`waiting_launches` in STATE), then to new work — the next ready epic whose dependencies have landed
   (`WORK_SESSION`, "The unit of work"); a code-goal launch is a candidate once #114's design and #113 settle.
   A gap review of the live product against the bar (`design.standing` is null) is a candidate once the owner's
   in-flight work settles (`PRODUCT_DESIGN`).

## How to end this turn
Schedule what the check calls for (as the next task or the series you can see, ending in another board check),
then, as a **`Continue`** iteration, **self-suspend on a FRESH bounded `any_of` wake** — never an unbounded
single wait:

    resumption_condition:
      any_of:
        - { member: schedule, resume_at: "<now + ~20–40m, ISO-8601 UTC>" }
        - { member: forked-thread-completion, forked_thread: "<a still-in-flight DAG id>" }
      deadline: null

Re-evaluate on each wake. If nothing needs action and no DAG is in flight, suspend until the next board check
on the short interval.

## Carried state (read first)
- `taskflow/overseer/I57/project_state.json` — STATE (updated by the I57 series; design reconciled).
- the `I58`–`I61` `CONTINUE.md` records — what the series did (review launched, deployment checked, board
  groomed, design DAG launched).

## Exit decision — do NOT Exit
The engagement is complete only when the product meets the release bar its design set, confirmed by a gap
review, everything is merged and delivered, and the board is Done. Until then, continue the chain.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + its k3s cluster/namespaces (`chirp*`) + ArgoCD `chirp`. Never force-push `main`;
**no attribution trailers**; **nothing on GitHub carries host/system details** — translate host facts to
repository identities.
