# _BRIEF.md — NSWE overseer iteration I82 (persona swe-lead) — PACED BOARD CHECK (re-test the escalation clearing condition)

**Depends on**: I81
**Task Kind**: evaluation — paced board check; re-test the open dispatch-fault escalation against the live world, watch the in-flight DAG(s) for fold, re-read the board, re-confirm deployment only on a drift trigger. Launch only into free slots; **never poll a running DAG**.

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I79 → I80 → I81 → **I82**). Event loop, **NOT** a code writer — **P1 holds.**
**Fileset: `WORK_SESSION` + `BOARD`** (load both; add `RETENTION`/`DEPLOYMENT`/`REVIEW_GATE`/`PRODUCT_DESIGN`
only if a check turns actionable). I77 filed the systemic fresh-fork dispatch-fault escalation
(`escalation_i77_dispatch_fault`, status `open`); I78/I79/I80/I81 each re-tested it on their wake and snapshotted
STATE forward. You are the next paced board check that re-tests it again.

## Context carried in (read first)
- **I81's `CONTINUE.md`** (its wake re-evaluation) and **authoritative STATE `taskflow/overseer/I81/project_state.json`**
  (snapshot forward to `I82/project_state.json`). The open escalation is `escalations[2]` / id `escalation_i77_dispatch_fault` —
  read STATE for its current status (`open` unless I81 recorded it cleared).
- **Baseline at I81 (fresh clock 2026-10-29T03:56:22Z — verify against a fresh read, do not trust as current):**
  PR **#113** (`work/epic-persist`) OPEN, MERGEABLE/UNSTABLE, blocked behind the dispatch fault; **#114** (Ferric 1.0
  directive, issue) blocked; deployment HEALTHY @**276138f** (main unchanged, last commit 2026-10-14; no land since #33 →
  no drift, no deployment check owed). `blocked` label on #113/#56/#65/#66/#67/#114.
- **Dispatch-fault re-test at I81: NOT MET.** All three fresh-fork scaffolds (`remediate-epic-persist-r1c`,
  `remediate-epic-persist-r1b`, `design-ferric-1_0-r2`) still bare — 0 `SUBTASK_*`, 0 `SYNTHESIS.md`, empty
  `scheduler/logs`, no commits → never dispatched. No new autonomous GitHub activity. Escalation stays OPEN.
- **The `design-chirp-r1` superseded zombie** was still LIVE & NOT folded at I81 (no root `SYNTHESIS.md`; last
  on-disk activity 2026-10-28T20:56:03Z — stalled ~7h at I81's clock but NOT folded; a thread cannot stop it). It has
  emitted duplicate artifacts to be **discarded, never adopted**: PR **#122** (branch `work/design-chirp-r1`, CLEAN
  duplicate of landed design #33), bare repo issues **#123** (onboarding empty-state) and **#124** (status/availability
  surface). On fold: record **SUPERSEDED**, close #122/#123/#124 as duplicates, let it reap, free its slot.
  **Discard-on-fold, NEVER adopt.** Do not place #123/#124 on the board. Honest in-flight at I81 = `design-chirp-r1`
  (1 counting; 3 free); the fresh-fork scaffolds (r1c/r1b/design-ferric-1_0-r2) are frozen/undispatched and do NOT count.

## What to do on this wake (re-evaluate FIRST, on a fresh clock)
1. **Re-test `escalation_i77_dispatch_fault`'s clearing condition against the LIVE WORLD** (the owner may fix the
   platform without commenting): has a **newly-launched build/automation job started and produced genuine
   activity/subtasks** (a fresh fork that grows `SUBTASK_*`/`SYNTHESIS.md`/commits or real `scheduler/logs`
   content on-disk, or new autonomous GitHub activity)? An empty `scheduler/`+`scheduler/logs` scaffold with
   0 subtasks is NOT dispatch. If it holds: record evidence + time in STATE, close/update the escalation
   (`BOARD`/`RETENTION`), remove the `blocked` label from the unblocked items, and schedule what was waiting
   (re-fork the persist remediation — budget **#1 of 2, 0 spent** unless STATE changed it — and the Ferric 1.0
   design r3), launching only into free slots (≤4 in flight). If it does NOT hold: the ask stays open,
   unchanged; do not ask again in a new place.
2. **Watch the in-flight DAG(s) for fold** (gate only on root `SYNTHESIS.md`, on disk — never poll).
   `design-chirp-r1` seam: `taskflow/dags/design-chirp-r1/SYNTHESIS.md` (or in its root `SUBTASK_synthesis/`).
   If folded → read-a-fold evaluation → record **SUPERSEDED**, close #122/#123/#124 as duplicates, let it reap,
   free its slot. **Discard-on-fold, NEVER adopt.** Any DAG legitimately launched later → route its fold per
   `OUT_OF_FOCUS`/`WORK_SESSION` (adopt its verdict). Re-point your own `any_of` to whatever DAGs are actually
   in flight per STATE.
3. **Re-read the board** (read-only `gh`) for new world activity since I81's 2026-10-29T03:56:22Z clock: new
   issues/comments/PRs/reviews from the request sources; route per `WORK_SESSION`/`BOARD`. Reconcile any repo
   issue missing from the board (but not the zombie's #123/#124 — discarded, not reconciled).
4. **Re-confirm deployment** HEALTHY @276138f only if a drift trigger appears (a land since last check); else
   no deployment check owed.
5. **Snapshot STATE forward** to `I82/project_state.json` with `last_checked_at` refreshed on the escalation
   and anything the check found.

## How to end
Schedule your successor **I83** (`depends_on` I82, next paced board check) and self-suspend on a FRESH bounded
`any_of` wake, then reach **`continue`** (or, if a check turned actionable and you launched/scheduled work into
a free slot, end with a board check as usual):

    resumption_condition:
      any_of:
        - { member: schedule, resume_at: "<now + ~20–40m, ISO-8601 UTC>" }
        - { member: forked-thread-completion, forked_thread: "<the in-flight DAG(s) per STATE, e.g. design-chirp-r1>" }
      deadline: null

The `schedule` member is the bounded re-check that guarantees you re-test the escalation even if nothing else
fires; **never suspend on `forked-thread-completion` alone.** **Do NOT Exit** unless the engagement is genuinely
complete (product meets the release bar and is delivered — not merely an empty board). The project stays a kept save.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + NSWE Delivery project #1 + its k3s (k3d `nswe`) cluster/namespaces (`chirp*`) +
ArgoCD `chirp`. Never force-push `main`; **no attribution trailers**; **nothing on GitHub carries
host/system/taskflow details** — translate host facts to repository identities, and hold the platform
dispatch-fault detail in STATE only.
