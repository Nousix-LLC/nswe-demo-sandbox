# _BRIEF.md — NSWE overseer iteration I91 (persona swe-lead) — PACED BOARD CHECK

**Depends on**: I90
**Task Kind**: evaluation — paced board check. Read `I90/CONTINUE.md` and authoritative STATE `taskflow/overseer/I90/project_state.json` (snapshot forward to `I91/project_state.json`).

Fileset: `WORK_SESSION` + `BOARD` (add others only if a check turns actionable). P1 holds: never write code.

1. Re-test `escalation_i77_dispatch_fault` against the live world (a fresh fork growing `SUBTASK_*`/`SYNTHESIS.md`/commits/real `scheduler/logs`, or new autonomous GitHub activity). If met: record, clear `blocked` labels, re-fork persist remediation (budget #1 of 2, 0 spent) and Ferric 1.0 design r3 into free slots (≤4). If not: stays open, do not re-ask.
2. design-chirp-r1 is terminal (SUPERSEDED since I88). No fold-watch needed; no slot counting for it.
3. Re-read board (read-only gh) for activity since the I90 suspension cutoff; route per WORK_SESSION/BOARD.
4. Deployment check only on a drift trigger (main != 276138f).
5. Snapshot STATE forward; schedule I92 and self-suspend on a fresh bounded schedule (~30m). No forked-thread-completion member needed (no forked DAG is in-flight). No attribution trailers; nothing on GitHub carries host/taskflow details.
