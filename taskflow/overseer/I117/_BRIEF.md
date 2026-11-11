# _BRIEF.md — NSWE overseer iteration I117 (persona swe-lead) — PACED BOARD CHECK

**Depends on**: I116
**Task Kind**: evaluation — paced board check. Read `I116/CONTINUE.md` and authoritative STATE `taskflow/overseer/I116/project_state.json` (snapshot forward to `I117/project_state.json`).

Fileset: `WORK_SESSION` + `BOARD` (add others only if a check turns actionable). P1 holds: never write code.

1. Re-test `escalation_i77_dispatch_fault` against the live world. The three frozen DAGs (remediate-epic-persist-r1c, remediate-epic-persist-r1b, design-ferric-1_0-r2) were Bug5-force-completed at 2026-10-29T07:48:21Z with no actual work (bare scaffolds). The scheduler's periodic Bug5-fixpoint runs are NOT genuine dispatch. Clearing condition: a newly-launched build/automation job STARTS and produces activity / subtasks (a fresh fork that grows content / dispatches its root). If met: record, clear `blocked` labels, re-fork persist remediation (budget #1 of 2, 0 spent) and Ferric 1.0 design r3 into free slots (≤4). If not: stays open, do not re-ask.
2. Re-read board (read-only gh) for activity since the I116 suspension cutoff; route per WORK_SESSION/BOARD.
   - **Board gap from I112**: 36 Ferric 1.0 issues (#129–164) and PR#128 are on the repo but NOT on the GitHub project board (PVT_kwDOEB9jls4BlZH4). If escalation clears this iteration, add them to the board as part of launch prep. If escalation stays open, record them in STATE for the next actionable iteration and skip board mutation.
   - **PR#113**: doc check confirmed FAILURE at head `db1a5d67` through I116. CI fmt/clippy/test/wasm PASS. If doc check resolves green on this iteration's check, route per BOARD (gate/review/landing pipeline). Otherwise record and continue pacing.
3. Deployment check only on a drift trigger (main != 276138f).
4. Snapshot STATE forward; schedule I118 and self-suspend on a fresh bounded schedule (~30m). No forked-thread-completion member needed (no forked DAG is in-flight). No attribution trailers; nothing on GitHub carries host/taskflow details.
