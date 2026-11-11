# _BRIEF.md — NSWE overseer iteration I80 (persona swe-lead) — PACED BOARD CHECK (re-test the escalation clearing condition)

**Depends on**: I79
**Task Kind**: evaluation — paced board check; re-test the open dispatch-fault escalation against the live world, watch `design-chirp-r1` for fold, re-read the board, re-confirm deployment. Launch only into free slots; **never poll a running DAG**.

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I77 → I78 → I79 → **I80**). Event loop, **NOT** a code writer — **P1 holds.**
**Fileset: `WORK_SESSION` + `BOARD`** (load both; add `RETENTION`/`DEPLOYMENT`/`REVIEW_GATE`/`PRODUCT_DESIGN`
only if a check turns actionable). I77 filed the systemic fresh-fork dispatch-fault escalation
(`escalation_i77_dispatch_fault`, status `open`); I78 and I79 each re-tested it on their wake and snapshotted
STATE forward. You are the next paced board check that re-tests it again.

## Self-suspend FIRST on a fresh bounded `any_of` wake — never an unbounded single wait
On dispatch, schedule your successor **I81** (next board check, `depends_on` I80) and self-suspend on a FRESH
bounded `any_of` wake, then do the board-check work when the wake fires (re-evaluate on a fresh clock FIRST):

    resumption_condition:
      any_of:
        - { member: schedule, resume_at: "<now + ~20–40m, ISO-8601 UTC>" }
        - { member: forked-thread-completion, forked_thread: "design-chirp-r1" }
      deadline: null

(`design-chirp-r1` is the ONLY in-flight DAG unless I79 launched into a free slot — read I79's `CONTINUE.md`
and STATE to learn the live in-flight set and re-point this `any_of` to whatever DAGs are actually in flight.)
The `schedule` member is the bounded re-check that guarantees you re-test the escalation even if nothing else
fires; never suspend on `forked-thread-completion` alone.

## Context carried in (read first)
- **I79's `CONTINUE.md`** (its wake re-evaluation: the escalation re-test result, the fold watch, the board
  re-read, the deployment re-confirm). **Authoritative STATE = `taskflow/overseer/I79/project_state.json`**
  (snapshot forward to `I80/project_state.json`). The open escalation is `escalations[]` id
  `escalation_i77_dispatch_fault` unless I79 recorded it cleared/closed — read STATE for the current status.
- Baseline at I78/I79 (verify against a fresh read, do not trust as current): PR **#113** (`work/epic-persist`)
  the only owner/user open PR, MERGEABLE/UNSTABLE, head `09fa453`, `doc` red / clippy·fmt·test·wasm green;
  #114 OPEN & `blocked`; deployment HEALTHY @276138f, no land since. `blocked` label on #113/#56/#65/#66/#67/#114.
- **The `design-chirp-r1` superseded zombie** is approaching fold and has emitted duplicate artifacts to be
  **discarded, never adopted**: PR **#122** (branch `work/design-chirp-r1`, a duplicate of landed design #33),
  bare repo issues **#123** (onboarding empty-state) and **#124** (status/availability surface). On fold:
  record **SUPERSEDED**, close #122/#123/#124 as duplicates, let it reap, free its slot. **Discard-on-fold,
  NEVER adopt.** Do not place #123/#124 on the board.

## What to do on each wake (re-evaluate FIRST, on a fresh clock)
1. **Re-test the escalation's clearing condition against the LIVE WORLD** (the owner may fix the platform
   without commenting): has a **newly-launched build/automation job started and produced activity / subtasks**?
   The world-test is a fresh fork that grows content / dispatches its root (on-disk), or new autonomous
   activity on GitHub. If it holds: record evidence + time in STATE, close/update the escalation
   (`BOARD.md`/`RETENTION.md`), remove the `blocked` label from the unblocked items, and schedule what was
   waiting (re-fork the persist remediation — budget still **#1 of 2, 0 spent** unless I79 changed it — and the
   Ferric 1.0 design r3), launching only into free slots (≤4 in flight). If it does NOT hold: the ask stays
   open, unchanged; do not ask again in a new place.
2. **Watch the in-flight DAG(s) for fold** (gate only on root `SYNTHESIS.md`, on disk — never poll). For the
   superseded `design-chirp-r1` zombie: if folded, route a read-a-fold evaluation → record **SUPERSEDED**,
   discard any duplicate artifacts (close #122/#123/#124), let it reap, free its slot. **Discard-on-fold, NEVER
   adopt.** For any DAG I79 legitimately launched: route its fold per `OUT_OF_FOCUS`/`WORK_SESSION` (adopt its
   verdict).
3. **Re-read the board** (read-only `gh`) for new world activity since I79's clock: new
   issues/comments/PRs/reviews from the request sources; route per `WORK_SESSION`/`BOARD`. Reconcile any repo
   issue missing from the board (but not the zombie's #123/#124 — those are discarded, not reconciled).
4. **Re-confirm deployment** HEALTHY @276138f if a drift trigger appears (else no deployment check owed).
5. **Snapshot STATE forward** to `I80/project_state.json` with `last_checked_at` refreshed on the escalation
   and anything the check found.

## How to end
Schedule your successor **I81** (`depends_on` I80, next paced board check) and reach **`continue`** (or, if a
check turned actionable and you launched/scheduled work into a free slot, end with a board check as usual).
**Do NOT Exit** unless the engagement is genuinely complete (product meets the release bar and is delivered —
not merely an empty board). The project stays a kept save.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + NSWE Delivery project #1 + its k3s (k3d `nswe`) cluster/namespaces (`chirp*`) +
ArgoCD `chirp`. Never force-push `main`; **no attribution trailers**; **nothing on GitHub carries
host/system/taskflow details** — translate host facts to repository identities, and hold the platform
dispatch-fault detail in STATE only.
