#!/usr/bin/env python3 -I
"""Snapshot I119 project_state.json -> I120/project_state.json with I120 notes."""
import json, copy, os

src = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I119/project_state.json"
dst = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I120/project_state.json"

with open(src) as f:
    state = json.load(f)

# Update top-level metadata
state["updated"] = "2026-10-29T22:00:00Z"
state["current_pointer"] = "overseer/I120"

# Update escalation_i77_dispatch_fault
esc = next(e for e in state["escalations"] if e.get("id") == "escalation_i77_dispatch_fault")
esc["last_checked_at"] = "2026-10-29T22:00:00Z"
esc["i120_check_result"] = (
    "NOT_MET (fresh clock overseer/I120). On-disk: all three frozen DAGs "
    "unchanged since I119 check -- remediate-epic-persist-r1c: scheduler/logs has exactly "
    "2 entries: Bug5 force-complete at 2026-10-29T07:48:21Z and 2026-10-29T17:23:00Z, "
    "no new dispatch activity; remediate-epic-persist-r1b: same 2 Bug5 entries, mtime Oct27 16:10; "
    "design-ferric-1_0-r2: same 2 Bug5 entries, mtime Oct28 07:43. No SUBTASK_* dirs, "
    "no SYNTHESIS.md, none dispatched their root. "
    "Live-world: no new autonomous GitHub activity since I119 cutoff (2026-10-29T21:30:00Z): "
    "PR#113 OPEN/MERGEABLE/UNSTABLE head db1a5d67, doc FAILURE/clippy+fmt+test+wasm PASS (unchanged); "
    "main unchanged 276138f. "
    "Clearing condition (a newly-launched build/automation job STARTS and produces activity) "
    "STILL NOT MET. Escalation stays OPEN; not re-asked (STATE-only, never on GitHub)."
)

# Add I120 iteration note to iteration_log
if "iteration_log" not in state:
    state["iteration_log"] = {}
state["iteration_log"]["note_i120"] = (
    "I120 paced board check. "
    "1. escalation_i77_dispatch_fault: STILL NOT MET. 3 frozen DAGs (r1c/r1b/ferric-r2) "
    "unchanged since I119: r1c scheduler/logs still has exactly 2 Bug5 entries (07:48:21Z, 17:23:00Z); "
    "r1b and ferric-r2 same. No new dispatch activity at all. "
    "Clearing condition not met; escalation stays OPEN. "
    "persist remediation (budget #1 of 2, 0 spent) and Ferric 1.0 design r3 stay blocked. "
    "2. PR#113: doc check still FAILING at head db1a5d67 (OPEN/MERGEABLE/UNSTABLE). "
    "fmt/clippy/test/wasm all SUCCESS. No change from I119. "
    "3. Board gap (#129-164, PR#128): escalation still open -> mutation deferred, "
    "recorded in board_gap_pending. "
    "4. main: 276138f unchanged, no deployment check needed. "
    "5. No DAG forked (all launches blocked; dispatch fault open). "
    "Honest in-flight = 0. Free = 4. "
    "Scheduled I121 (next paced board check, depends_on I120). "
    "Self-suspended on fresh bounded schedule wake ~30m."
)

# Keep board_gap_pending record updated
if "board_gap_pending" not in state:
    state["board_gap_pending"] = {}
state["board_gap_pending"] = {
    "issues": "#129-164 (36 Ferric 1.0 issues, filed by design-chirp-r1 / design-ferric-1_0-r2)",
    "pr": "#128 (design: Ferric 1.0 framework design, head 9dcd978d)",
    "project_board_id": "PVT_kwDOEB9jls4BlZH4",
    "action": "Add to board when escalation clears (launch prep for persist remediation + Ferric design r3)",
    "recorded_at": "overseer/I119 (confirmed overseer/I120)",
    "note": "Not added to board this iteration (escalation_i77_dispatch_fault still OPEN)"
}

os.makedirs(os.path.dirname(dst), exist_ok=True)
with open(dst, "w") as f:
    json.dump(state, f, indent=2)

print(f"Written to {dst}")
print(f"Size: {os.path.getsize(dst)} bytes")
