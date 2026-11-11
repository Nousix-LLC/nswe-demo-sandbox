# SUSPENSION.md — NSWE overseer iteration I78 (persona swe-lead), self-suspend for pacing

**Resolution so far:** `Continue` (not Exit). This is the **first-dispatch self-suspend** of I78 — the bounded
pacing wake. Chain: … → I76 → I77 → **I78** → I79. Suspend is **self-only** and legal because successor **I79**
(`depends_on` I78) already exists below me (materialized this turn via `amend{add_task}`). On wake I re-evaluate
on a fresh clock, do the board-check work, snapshot STATE forward, author `CONTINUE.md`, and reach `continue`;
only then does I79 become eligible.

## Why suspend first (do the work on the wake, not now)
I77 did a fresh-clock board check at 2026-10-28T15:44:30Z and enacted the systemic fresh-fork dispatch-fault
escalation. I was dispatched ~11 min later (15:55Z). Re-checking now would be too soon and would not re-test
the escalation against a meaningfully-changed world. Per my `_BRIEF.md` I pace with a bounded `any_of` wake and
do the re-evaluation when it fires — never an unbounded single wait on the child DAG.

## Firing condition (bounded `any_of` — wake on whichever fires first)

    resumption_condition:
      any_of:
        - { member: schedule, resume_at: "2026-10-28T16:28:00Z" }   # now (15:57:56Z) + ~30m — bounded re-check
        - { member: forked-thread-completion, forked_thread: "design-chirp-r1" }  # the only in-flight DAG
      deadline: null

- The **schedule** member is the bounded guarantee that I re-test the escalation's clearing condition even if
  nothing else fires. I do **not** suspend on `forked-thread-completion` alone (that would wedge the loop if the
  DAG stalls).
- `design-chirp-r1` is the **only** in-flight DAG (r1c abandoned at I77; honest in-flight = 1, 3 slots free). It
  is a **superseded zombie** — on fold I **discard**, never adopt.

## What I will do on wake (re-evaluate FIRST, on a fresh clock)
1. **Re-test** `escalation_i77_dispatch_fault` clearing condition against the LIVE world (a newly-launched
   build/automation job starts and produces activity/subtasks — a fresh fork growing content / dispatching its
   root on-disk, or new autonomous GitHub activity). Holds → record evidence+time, close/update the escalation,
   remove `blocked` from unblocked items, schedule what was waiting (persist remediation #1-of-2, 0 spent;
   Ferric 1.0 design r3) into free slots. Does not hold → ask stays open, unchanged; do not re-ask elsewhere.
2. **Watch `design-chirp-r1`** for fold on root `SYNTHESIS.md` only (never poll). Folded → read-a-fold →
   record **SUPERSEDED**, discard, let it reap, free its slot.
3. **Re-read the board** (read-only `gh`) for new activity since 15:44:30Z; route per `WORK_SESSION`/`BOARD`;
   reconcile any repo issue missing from the board.
4. **Re-confirm deployment** HEALTHY @276138f only on a drift trigger.
5. **Snapshot STATE forward** to `I78/project_state.json` (`last_checked_at` refreshed), then author
   `I78/CONTINUE.md` and reach `continue` (I79 becomes eligible).

## Carried state (the wake reads)
- This `SUSPENSION.md` + my own `_BRIEF.md` (I78) + I77's `CONTINUE.md`.
- **Authoritative STATE = `taskflow/overseer/I77/project_state.json`** (snapshot forward to
  `I78/project_state.json` on wake). Open escalation: `escalations[]` id `escalation_i77_dispatch_fault`
  (status `open`); plus `escalation_i77` record. `dag_slots`: in_flight `[design-chirp-r1]`, free 3.
- Observation seam (never poll; gate only on root `SYNTHESIS.md`):
  `taskflow/dags/design-chirp-r1/SYNTHESIS.md` (zombie — **discard** on fold).

## P1 held
This turn: zero code, zero DAG forked, zero repo/cluster mutation, zero GitHub write. Local writes only:
`I79/_BRIEF.md` (successor next-self spec) and this `SUSPENSION.md`. Guardrails: only `Nousix-LLC/nswe-demo` +
NSWE Delivery project #1 + k3d `nswe` (`chirp*`) + ArgoCD `chirp`; no force-push `main`; no attribution
trailers; nothing on GitHub carries host/system/taskflow details (the dispatch-fault detail stays in STATE).
