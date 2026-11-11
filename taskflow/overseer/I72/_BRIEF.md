# _BRIEF.md — NSWE overseer iteration I72 (persona swe-lead) — BOARD CHECK (home return, paced)
**Depends on**: I71

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I68 → I69 → I70 → I71 → **I72**). Event loop, **NOT** a code writer — **P1 holds.** Boot the kernel + NSWE
app-files, publish `thread_evaluation`, then Act. This is the **home-return board check** closing the
I67-scheduled series (I68 process-review → I69 remediation #1 → I70 discard zombie → I71 groom → **I72**).
Fileset: **`WORK_SESSION` + `BOARD`** (+ others as the check routes). An **evaluation decides and schedules; it
does not act/fork.** Read-only `gh`/`kubectl`/`curl` on a **FRESH clock**. **Never poll a running DAG** — gate
only on each folded ROOT `SYNTHESIS.md`.

## Context carried in (read first)
- I67's `CONTINUE.md` and the I68–I71 `CONTINUE.md` records — what this series did. `taskflow/overseer/I63/project_state.json`
  is the baseline STATE; each action task updated STATE as it ran. (The earlier I64–I66 dirs are dead
  pre-authored briefs that never executed — ignore them.)

## What to evaluate (re-evaluate every in-flight DAG FIRST, fresh clock, gate only on root `SYNTHESIS.md`)
1. **remediation #1** on `work/epic-persist` (forked at I69): on fold → machine gate. PASS → PR #113 is up for
   **re-review** (schedule a review-launch task, `REVIEW_GATE`). FAIL → **remediation #2** (the LAST automatic
   attempt, budget 2; then escalate to the user with both attempts). A fold re-enters at the machine gate.
2. **`design-ferric-1_0`** (#114, Ferric epic #1): on fold → **Triage a design** (`PRODUCT_DESIGN` + `BOARD`):
   adopt — tickets under epic #1, de-dupe vs router #5 / HTTP #6, design PR to review, record the Ferric 1.0
   release bar. If still progressing on a fresh clock, standing watch. (It was actively writing content at
   16:08Z on 2026-10-22.)
3. **`design-chirp-r1`**: I70 should have recorded it SUPERSEDED/discarded and freed its slot — confirm it is no
   longer counted and filed no duplicates; if anything new appeared, close it.
4. **Board**: PR #113 mergeability (expect `doc` to go green and the PR mergeable/clean once remediation #1
   lands; landing still waits on an **APPROVE** — current verdict REQUEST-CHANGES until re-review); #115–#121 on
   the board and groomed; every repo issue a board item; any open escalation's clearing condition; whether the
   backlog still leads to the release bar.
5. **Deployment**: HEALTHY @276138f at last check; a land since (none yet — PR #113 unlanded) calls for a
   deployment check (`DEPLOYMENT`).
6. **Slots / waiting launches**: a freed slot goes to the highest-priority waiting launch, then new work in
   board-check order. A product **gap review** (`design.standing` null) is a candidate only once PR #113 settles
   AND no design DAG is in flight. A new **code-goal** launch is a candidate once #114's design and PR #113
   settle.

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
Only `Nousix-LLC/nswe-demo` + its k3s cluster/namespaces (`chirp*`) + ArgoCD `chirp`. Never force-push `main`;
**no attribution trailers**; **nothing on GitHub carries host/system details** — translate host facts to
repository identities.
