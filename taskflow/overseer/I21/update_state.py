import json, copy

src = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I20/project_state.json"
dst = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I21/project_state.json"

with open(src) as f:
    s = json.load(f)

s["updated"] = "2026-10-07T03:16:15Z"

# Refresh #8 chirp-server dispatched_dags note (append I21 recon)
for d in s["dispatched_dags"]:
    if d.get("item_slug") == "chirp-server":
        d["note"] += (" | I21 recon (read-only, P1 held): STILL RUNNING, NOT folded, PROGRESSING past I20 - "
            "root SUSPENSION.md (NeedsDecompose); SUBTASK_scaffold_and_repository COMPLETE.md (first spoke done); "
            "SUBTASK_api_layer has NOW ITSELF DECOMPOSED AND SUSPENDED (carries _GLOBAL.md + SUSPENSION.md + contracts/ -> a running sub-subtree; "
            "at I20 it held _GLOBAL.md + contracts/ without its own SUSPENSION.md); SUBTASK_integration_tests_and_docs + SUBTASK_synthesis_gate hold only _BRIEF.md; "
            "live checkout/ + taskflow_workspaces/; NO root SYNTHESIS.md -> still decompose->implement->synthesize. No open PR for #8 yet. "
            "I22: keep watching for ROOT SYNTHESIS.md fold -> PASS: fork review-chirp-server before landing; FAIL: remediate (budget 2 then escalate).")
    if d.get("item_slug") == "chirp-frontend":
        d["note"] += (" | I21 recon (read-only, P1 held): STILL RUNNING, NOT folded - root SUSPENSION.md (DECOMPOSED) + 6 subtasks "
            "(scaffold, api_client, timeline, compose, profile, synthesis_gate), each only _BRIEF.md (no child COMPLETE.md yet), "
            "NO root SYNTHESIS.md -> decomposed, early implementation. No open PR for #9 yet. "
            "I22: keep watching for ROOT SYNTHESIS.md fold -> PASS: fork review-chirp-frontend before landing; FAIL: remediate.")

# Append the I21 iteration record
s["iterations"].append({
    "iteration": "I21",
    "persona": "swe-lead",
    "woke_to": ("continue the chain (I20 -> I21), 'resume reconstructed taskflow node'. Per _BRIEF.md: recon read-only "
        "(re-poll gh past UNKNOWN); watch chirp-server/SYNTHESIS.md (#8) and chirp-frontend/SYNTHESIS.md (#9) for their "
        "ROOT fold; gate+LAND any approved+CLEAN work mechanically; fork at most one demand-driven DAG; schedule I22."),
    "evaluation": "Continue",
    "scheduled_successor": ("I22 (depends_on I21; execution group 19; eligible promptly to re-check #8 chirp-server and "
        "#9 chirp-frontend folds, gate/land, and fan out devops once #8 lands)"),
    "reconnaissance": ("Read-only, P1 held (no build re-run, no rebase, no code/lockfile touched). "
        "(1) chirp-server (#8 code DAG) NOT folded but PROGRESSING past I20: root SUSPENSION.md (NeedsDecompose); "
        "SUBTASK_scaffold_and_repository COMPLETE.md (first spoke done); SUBTASK_api_layer has NOW ITSELF DECOMPOSED AND SUSPENDED "
        "(_GLOBAL.md + SUSPENSION.md + contracts/ -> running sub-subtree, further than I20's _GLOBAL.md+contracts/ without SUSPENSION.md); "
        "SUBTASK_integration_tests_and_docs + SUBTASK_synthesis_gate only _BRIEF.md; live checkout/ + taskflow_workspaces/; "
        "NO root SYNTHESIS.md -> still running. "
        "(2) chirp-frontend (#9 code DAG) NOT folded: root SUSPENSION.md (DECOMPOSED) + 6 subtasks each only _BRIEF.md, "
        "NO root SYNTHESIS.md -> decomposed, early implementation. "
        "(3) gh (authenticated mattsmcknight), re-polled: NO open PRs (nothing to re-poll mergeability on, no gate due). "
        "issues #4/#5/#6/#7 CLOSED, #8-#13 OPEN (+ epics #1/#2/#3 OPEN). main @ 25e90c0 confirmed (ferric-http #6). Nothing re-authored."),
    "atomic_action": ("NONE - demand-driven watch-and-schedule iteration (the I10/I13/I18/I19/I20 precedent). "
        "Nothing folded (no root SYNTHESIS.md for #8 or #9 -> no machine gate), no open PR (nothing landable), "
        "no PR CONFLICTING (no relock), and the devops wave (#10-#13) is still gated on a buildable app surface / #8 chirp-server "
        "landing per the brief's priority-4 trigger. One-fork budget held unspent; fork token NOT exercised. "
        "Priority ladder (relock > review > remediation > newly-unblocked devops) produced no actionable fork. "
        "Scheduled successor I22 BEFORE the (null) atomic action per the self-perpetuating continue path."),
    "fork_denied": None,
    "fork_succeeded": None,
    "landed": "none",
    "board_changes": "none (#8 and #9 remain In Progress; #10-#13 remain Todo/In Progress)",
    "terminal": "continue",
})

# Refresh turn_pointer
tp = s["turn_pointer"]
tp["wave"] = ("FERRIC FRAMEWORK COMPLETE on main: ferric #4 + ferric-router #5 + ferric-http #6 all landed. "
    "CHIRP contract chirp-types #7 landed. chirp-server #8: FORKED by I16, running (DECOMPOSED into 4 subtasks; "
    "scaffold_and_repository spoke COMPLETE; api_layer now ITSELF decomposed AND suspended -> a running sub-subtree; "
    "integration_tests_and_docs/synthesis_gate still only _BRIEF.md; NO root SYNTHESIS.md) -> watch for ROOT SYNTHESIS.md fold. "
    "chirp-frontend #9: FORKED by I17, running (DECOMPOSED into 6 subtasks; all only _BRIEF.md; NO root SYNTHESIS.md) -> watch for ROOT SYNTHESIS.md fold. "
    "Remaining: #8 + #9 gate+land, then devops #10-#13 (infra/CI/containerize/deploy-argocd).")
tp["running"] = [
    ("chirp-server (forked by I16; crates/chirp-server axum REST API + repo-trait persistence + static serving + integration tests "
     "against the landed chirp-types contract; branch work/chirp-server; DECOMPOSED - scaffold spoke COMPLETE, api_layer now itself "
     "sub-decomposed AND suspended, still running; watch for ROOT SYNTHESIS.md fold -> PASS: fork review-chirp-server before landing / FAIL: remediate)"),
    ("chirp-frontend (forked by I17; crates/chirp-frontend ferric SPA composing ferric+ferric-router+ferric-http + chirp-types REST contract; "
     "branch work/chirp-frontend; DECOMPOSED into 6 subtasks, early implementation, still running; watch for ROOT SYNTHESIS.md fold -> "
     "PASS: fork review-chirp-frontend before landing / FAIL: remediate)"),
]
tp["awaiting"] = ("I22+ to: (1) recon read-only; re-poll gh past UNKNOWN. (2) When chirp-server #8 and/or chirp-frontend #9 FOLD "
    "(ROOT SYNTHESIS.md) -> read machine verdict -> PASS: fork review-<slug> (do not land unreviewed) / FAIL: remediate (budget 2 then escalate); "
    "on review APPROVE + PR OPEN/MERGEABLE/CLEAN -> LAND (squash-merge, board Done, append STATE, bump pointer, reap whole). "
    "(3) Fork one demand-driven DAG per the priority. Then fan out devops #10-#13 once buildable (#8 landed trigger). One fork per iteration.")
tp["fork_token_note"] = ("I3-I7 denied the 'fork' token (reconstructed nodes); I8 (#6), I9 (#7), I11 (#5 review), I12 (#6 review), "
    "I14 (#7 review), I15 (#6 relock), I16 (#8 chirp-server), I17 (#9 chirp-frontend) GRANTED + all forks SUCCEEDED. "
    "I10, I13, I18, I19, I20, and I21 had NO fork to make (demand-driven watch-and-schedule iterations). "
    "The chain is self-perpetuating (each schedules its successor BEFORE the atomic action). P1 held on every iteration incl. I21: "
    "the overseer read DAG state / PR states (read-only, no build re-run), forked nothing (nothing foldable/landable/unblocked, no relock due), "
    "scheduled its successor, and updated STATE.")

with open(dst, "w") as f:
    json.dump(s, f, indent=2)

# round-trip validate
with open(dst) as f:
    json.load(f)
print("OK wrote", dst, "iterations:", len(s["iterations"]), "current_pointer:", s["current_pointer"], "work_items:", len(s["work_items"]))
