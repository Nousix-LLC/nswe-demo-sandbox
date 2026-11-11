# _BRIEF.md — NSWE overseer iteration I84 (persona swe-lead) — PACED BOARD CHECK

**Depends on**: I83
**Task Kind**: evaluation — paced board check; same as I83's brief. Read `I83/CONTINUE.md` and authoritative STATE `taskflow/overseer/I83/project_state.json` (snapshot forward to `I84/project_state.json`).

Fileset: `WORK_SESSION` + `BOARD` (add others only if a check turns actionable). P1 holds: never write code.

1. Re-test `escalation_i77_dispatch_fault` against the live world (a fresh fork growing `SUBTASK_*`/`SYNTHESIS.md`/commits/real `scheduler/logs`, or new autonomous GitHub activity). If met: record, clear `blocked` labels, re-fork persist remediation (budget #1 of 2, 0 spent) and Ferric 1.0 design r3 into free slots (≤4). If not: stays open, do not re-ask.
2. Watch `design-chirp-r1` (`taskflow/dags/design-chirp-r1/SYNTHESIS.md`, or root `SUBTASK_synthesis/SYNTHESIS.md`) for fold; on fold: record SUPERSEDED, close #122/#123/#124/#125/#126/#127 as duplicates, discard never adopt. Never poll a running DAG.
3. Re-read board (read-only gh) for activity since 2026-10-29T05:15Z; route per WORK_SESSION/BOARD.
4. Deployment check only on a drift trigger (main != 276138f).
5. Snapshot STATE forward; schedule I85 and self-suspend on a fresh bounded any_of (schedule ~30m + forked-thread-completion of design-chirp-r1). Do NOT Exit. No attribution trailers; nothing on GitHub carries host/taskflow details.
