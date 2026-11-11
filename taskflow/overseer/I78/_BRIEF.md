# _BRIEF.md — NSWE overseer iteration I78 (persona swe-lead) — PACED BOARD CHECK (re-test the escalation clearing condition)

**Depends on**: I77
**Task Kind**: evaluation — paced board check; re-test the open dispatch-fault escalation against the live world, watch `design-chirp-r1` for fold, re-read the board, re-confirm deployment. Launch only into free slots; **never poll a running DAG**.

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I75 → I76 → I77 → **I78**). Event loop, **NOT** a code writer — **P1 holds.**
**Fileset: `WORK_SESSION` + `BOARD`** (load both; add `RETENTION`/`DEPLOYMENT`/`REVIEW_GATE`/`PRODUCT_DESIGN`
only if a check turns actionable). I77 filed the systemic fresh-fork dispatch-fault escalation and reached
`continue`; you are the paced board check that re-tests it.

## Self-suspend FIRST on a fresh bounded `any_of` wake — never an unbounded single wait
On dispatch, schedule your successor **I79** (next board check, `depends_on` I78) and self-suspend on a FRESH
bounded `any_of` wake, then do the board-check work when the wake fires (re-evaluate on a fresh clock FIRST):

    resumption_condition:
      any_of:
        - { member: schedule, resume_at: "<now + ~20–40m, ISO-8601 UTC>" }
        - { member: forked-thread-completion, forked_thread: "design-chirp-r1" }
      deadline: null

(`design-chirp-r1` is the ONLY in-flight DAG — r1c was abandoned at I77.) The `schedule` member is the bounded
re-check that guarantees you re-test the escalation even if nothing else fires; never suspend on
`forked-thread-completion` alone.

## Context carried in (read first)
- **I77's `CONTINUE.md`** (the enacted escalation + blocked markings + r1c abandonment). I76's `CONTINUE.md`
  (the FROZEN verdict). **Authoritative STATE = `taskflow/overseer/I77/project_state.json`** (snapshot forward
  to `I78/project_state.json`). The open escalation is `escalations[]` id `escalation_i77_dispatch_fault`
  (status `open`), plus the `escalation_i77` iteration record.
- At I77 (fresh ~15:44Z, read-only): PR **#113** (`work/epic-persist`) is the only open PR, MERGEABLE, head
  `09fa453`, `doc` red / clippy·fmt·test·wasm green; #114 OPEN; **zero** GitHub activity today. Deployment
  HEALTHY @276138f, no land since. The `blocked` label is on #113/#56/#65/#66/#67/#114.

## What to do on each wake (re-evaluate FIRST, on a fresh clock)
1. **Re-test the escalation's clearing condition against the LIVE WORLD** (the owner may fix the platform
   without commenting): has a **newly-launched build/automation job started and produced activity / subtasks**?
   The world-test is a fresh fork that grows content / dispatches its root (on-disk), or new autonomous
   activity on GitHub. If it holds: record evidence + time in STATE, close/update the escalation
   (`BOARD.md`/`RETENTION.md`), remove the `blocked` label from the unblocked items, and schedule what was
   waiting (re-fork the persist remediation #1 — budget still **#1 of 2, 0 spent** — and the Ferric 1.0
   design r3). If it does NOT hold: the ask stays open, unchanged; do not ask again in a new place.
2. **Watch `design-chirp-r1` for fold** (gate only on root `SYNTHESIS.md`, on disk — never poll): if folded,
   route a read-a-fold evaluation → record **SUPERSEDED**, discard any duplicate artifacts (expect none), let
   it reap, free its slot. **Discard-on-fold, NEVER adopt.** If not folded, standing watch holds.
3. **Re-read the board** (read-only `gh`) for new world activity since 15:44Z: new issues/comments/PRs/reviews
   from the request sources; route per `WORK_SESSION`/`BOARD`. Reconcile any repo issue missing from the board.
4. **Re-confirm deployment** HEALTHY @276138f if a drift trigger appears (else no deployment check owed).
5. **Snapshot STATE forward** to `I78/project_state.json` with `last_checked_at` refreshed on the escalation
   and anything the check found.

## How to end
Schedule your successor **I79** (`depends_on` I78, next paced board check) and reach **`continue`** (or, if a
check turned actionable and you launched/scheduled work into a free slot, end with a board check as usual).
**Do NOT Exit** — the engagement is not complete (PR #113 blocked, #114 design blocked, release bar unmet,
`design.standing` null). The project stays a kept save.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + NSWE Delivery project #1 + its k3s (k3d `nswe`) cluster/namespaces (`chirp*`) +
ArgoCD `chirp`. Never force-push `main`; **no attribution trailers**; **nothing on GitHub carries
host/system/taskflow details** — translate host facts to repository identities, and hold the platform
dispatch-fault detail in STATE only.
