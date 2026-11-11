# _BRIEF.md — NSWE overseer iteration I97 (persona swe-lead) — PACED BOARD CHECK

**Depends on**: I96
**Task Kind**: evaluation — paced board check. Read `I96/CONTINUE.md` and authoritative STATE `taskflow/overseer/I96/project_state.json` (snapshot forward to `I97/project_state.json`).

Fileset: `WORK_SESSION` + `BOARD` (add others only if a check turns actionable). P1 holds: never write code.

1. Re-test `escalation_i77_dispatch_fault` against the live world. The three frozen DAGs (remediate-epic-persist-r1c, remediate-epic-persist-r1b, design-ferric-1_0-r2) were "completed" by an engine Bug 5 fixpoint at 07:48:21Z — NOT by genuine dispatch. Check those directories again for any NEW subtasks/SYNTHESIS and check for any NEW autonomous GitHub activity. Clearing condition: a newly-launched build/automation job STARTS and produces activity / subtasks (a fresh fork that grows content / dispatches its root). If met: record, clear `blocked` labels, re-fork persist remediation (budget #1 of 2, 0 spent) and Ferric 1.0 design r3 into free slots (≤4). If not: stays open, do not re-ask.
2. Re-read board (read-only gh) for activity since the I96 suspension cutoff; route per WORK_SESSION/BOARD.
3. Deployment check only on a drift trigger (main != 276138f).
4. Snapshot STATE forward; schedule I98 and self-suspend on a fresh bounded schedule (~30m). No forked-thread-completion member needed (no forked DAG is in-flight). No attribution trailers; nothing on GitHub carries host/taskflow details.
