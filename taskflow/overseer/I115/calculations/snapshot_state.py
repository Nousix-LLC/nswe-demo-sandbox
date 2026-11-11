import json, sys

src = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I114/project_state.json"
dst = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I115/project_state.json"

with open(src, "r") as f:
    state = json.load(f)

# Update timestamp
state["updated"] = "2026-10-29T19:40:00Z"

# Add I115 iteration note
if isinstance(state.get("iterations"), list):
    state["iterations"].append({
        "id": "I115",
        "at": "2026-10-29T19:40:00Z",
        "kind": "paced-board-check",
        "resolution": "continue",
        "summary": (
            "I115 paced board check (fresh clock 2026-10-29T19:40:00Z). "
            "Honest in-flight = 0 (all three fresh forks Bug5-force-completed with no actual work "
            "[dispatch fault unchanged; periodic Bug5 fixpoint run at 17:23:00Z is NOT genuine dispatch]; "
            "design-chirp-r1 folded I88, terminal). Free = 4. No DAG forked "
            "(escalation_i77_dispatch_fault still OPEN; all launches blocked). "
            "PR#113: doc=FAILURE at head db1a5d67 (unchanged). Board gap (#129-164, PR#128) deferred. "
            "main unchanged at 276138f. No new issues/PRs since I114 cutoff (19:10Z)."
        )
    })
elif isinstance(state.get("iterations"), dict):
    state["iterations"]["note_i115"] = (
        "I115 paced board check (fresh clock 2026-10-29T19:40:00Z). "
        "Honest in-flight = 0. No DAG forked. PR#113 doc=FAILURE. Escalation still OPEN."
    )
else:
    state["note_i115"] = "I115 paced board check complete."

# Update escalation last_checked
if "escalation_i77" not in state:
    state["escalation_i77"] = {}
state["escalation_i77"]["last_checked_at_i115"] = "2026-10-29T19:40:00Z"
state["escalation_i77"]["status"] = "OPEN"
state["escalation_i77"]["clearing_condition_met_i115"] = False

# Add PR#113 tracking for I115
if "pr_113_tracking_i115" not in state:
    state["pr_113_tracking_i115"] = {}
state["pr_113_tracking_i115"] = {
    "checked_at": "2026-10-29T19:40:00Z",
    "head": "db1a5d67",
    "state": "OPEN",
    "mergeable": "MERGEABLE",
    "mergeStateStatus": "UNSTABLE",
    "doc_check": "FAILURE",
    "fmt_clippy_test_wasm": "SUCCESS",
    "note": "PR#113 doc check still FAILURE at head db1a5d67 (unchanged since I113). Not eligible for landing pipeline."
}

# Board gap deferred note
if "board_gap_ferric_issues" in state:
    state["board_gap_ferric_issues"]["deferred_i115"] = "Escalation still OPEN; board gap (#129-164, PR#128) deferred to next actionable iteration."

with open(dst, "w") as f:
    json.dump(state, f, indent=2)

print("OK: state snapshot written to", dst)
print("Size:", len(json.dumps(state)))
