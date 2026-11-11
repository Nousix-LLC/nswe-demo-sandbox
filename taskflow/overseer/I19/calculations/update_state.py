import json, copy

SRC = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I18/project_state.json"
DST = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I19/project_state.json"

with open(SRC) as f:
    s = json.load(f)

s["updated"] = "2026-10-07T02:04:00Z"

# --- dispatched_dags: refresh #8 chirp-server and #9 chirp-frontend progress notes ---
for d in s["dispatched_dags"]:
    if d.get("item_slug") == "chirp-server":
        d["status"] = "running-decomposed-not-folded"
        d["note"] += (
            " | I19 recon (read-only, P1 held): STILL RUNNING, NOT folded, but progressing — "
            "SUBTASK_scaffold_and_repository now has COMPLETE.md (first spoke landed); SUBTASK_api_layer + "
            "SUBTASK_integration_tests_and_docs + SUBTASK_synthesis_gate hold only _BRIEF.md; live checkout/ + "
            "taskflow_workspaces/ present; NO root SYNTHESIS.md -> still decompose->implement->synthesize. "
            "No open PR for #8 yet. I20: keep watching for ROOT SYNTHESIS.md fold -> PASS: fork review-chirp-server "
            "before landing; FAIL: remediate (budget 2 then escalate)."
        )
    if d.get("item_slug") == "chirp-frontend":
        d["status"] = "running-decomposed-not-folded"
        d["note"] += (
            " | I19 recon (read-only, P1 held): ADVANCED since I18 — workspace now holds _GLOBAL.md + SIX subtasks "
            "(SUBTASK_scaffold, SUBTASK_api_client, SUBTASK_timeline, SUBTASK_compose, SUBTASK_profile, "
            "SUBTASK_synthesis_gate), each with only a _BRIEF.md (no child COMPLETE.md yet), and NO root SYNTHESIS.md "
            "-> decomposed, early implementation, NOT folded. No open PR for #9 yet. I20: keep watching for ROOT "
            "SYNTHESIS.md fold -> PASS: fork review-chirp-frontend before landing; FAIL: remediate."
        )

# --- iterations: append the I19 record ---
s["iterations"].append({
    "iteration": "I19",
    "persona": "swe-lead",
    "woke_to": "continue the chain (I18 -> I19), 'resume reconstructed taskflow node'. Per _BRIEF.md: recon read-only (re-poll gh past UNKNOWN); watch chirp-server/SYNTHESIS.md (#8) and chirp-frontend/SYNTHESIS.md (#9) for their ROOT fold; gate+LAND any approved+CLEAN work mechanically; fork at most one demand-driven DAG; schedule I20.",
    "evaluation": "Continue",
    "scheduled_successor": "I20 (depends_on I19; execution group 17; eligible promptly to re-check #8 chirp-server and #9 chirp-frontend folds, gate/land, and fan out devops once #8 lands)",
    "reconnaissance": "Read-only, P1 held (no build re-run, no rebase, no code/lockfile touched). (1) chirp-server (#8 code DAG) NOT folded but PROGRESSING: root SUSPENSION.md (DECOMPOSED/NeedsDecompose); SUBTASK_scaffold_and_repository now COMPLETE.md (first spoke done); SUBTASK_api_layer + SUBTASK_integration_tests_and_docs + SUBTASK_synthesis_gate still only _BRIEF.md; live checkout/ + taskflow_workspaces/; NO root SYNTHESIS.md -> still running. (2) chirp-frontend (#9 code DAG) NOT folded but ADVANCED since I18: now _GLOBAL.md + 6 subtasks (scaffold, api_client, timeline, compose, profile, synthesis_gate), each only _BRIEF.md (no child COMPLETE.md), NO root SYNTHESIS.md -> decomposed, early implementation. (3) gh (authenticated mattsmcknight), re-polled: NO open PRs. issues #4/#5/#6/#7 CLOSED, #8-#13 OPEN. main @ 25e90c0 confirmed (ferric-http #6). Nothing re-authored.",
    "atomic_action": "NONE - demand-driven watch-and-schedule iteration (the I10/I13/I18 precedent). Nothing folded (no root SYNTHESIS.md for #8 or #9 -> no machine gate), no open PR (nothing landable), no PR CONFLICTING (no relock), and the devops wave (#10-#13) is still gated on a buildable app surface / #8 chirp-server landing per the brief's priority-4 trigger. One-fork budget held unspent; fork token NOT exercised. Priority ladder (relock > review > remediation > newly-unblocked devops) produced no actionable fork. Scheduled successor I20 BEFORE the (null) atomic action per the self-perpetuating continue path.",
    "fork_denied": None,
    "fork_succeeded": None,
    "landed": "none",
    "board_changes": "none (#8 and #9 remain In Progress; #10-#13 remain Todo/In Progress)",
    "terminal": "continue"
})

# --- turn_pointer refresh ---
tp = s["turn_pointer"]
tp["wave"] = (
    "FERRIC FRAMEWORK COMPLETE on main: ferric #4 + ferric-router #5 + ferric-http #6 all landed. CHIRP contract "
    "chirp-types #7 landed. chirp-server #8: FORKED by I16, running (DECOMPOSED into 4 subtasks; scaffold_and_repository "
    "spoke now COMPLETE.md; api_layer/integration_tests_and_docs/synthesis_gate still running; NO root SYNTHESIS.md) -> "
    "watch for ROOT SYNTHESIS.md fold. chirp-frontend #9: FORKED by I17, running (now DECOMPOSED into 6 subtasks; all only "
    "_BRIEF.md; NO root SYNTHESIS.md) -> watch for ROOT SYNTHESIS.md fold. Remaining: #8 + #9 gate+land, then devops "
    "#10-#13 (infra/CI/containerize/deploy-argocd)."
)
tp["running"] = [
    "chirp-server (forked by I16; crates/chirp-server axum REST API + repo-trait persistence + static serving + integration tests against the landed chirp-types contract; branch work/chirp-server; DECOMPOSED into 4 subtasks, scaffold spoke COMPLETE, still running; watch for ROOT SYNTHESIS.md fold -> PASS: fork review-chirp-server before landing / FAIL: remediate)",
    "chirp-frontend (forked by I17; crates/chirp-frontend ferric SPA composing ferric+ferric-router+ferric-http + chirp-types REST contract; branch work/chirp-frontend; DECOMPOSED into 6 subtasks, early implementation, still running; watch for ROOT SYNTHESIS.md fold -> PASS: fork review-chirp-frontend before landing / FAIL: remediate)"
]
tp["folded_awaiting_action"] = []
tp["awaiting"] = (
    "I20+ to: (1) recon read-only; re-poll gh past UNKNOWN. (2) When chirp-server #8 and/or chirp-frontend #9 FOLD "
    "(ROOT SYNTHESIS.md) -> read machine verdict -> PASS: fork review-<slug> (do not land unreviewed) / FAIL: remediate "
    "(budget 2 then escalate); on review APPROVE + PR OPEN/MERGEABLE/CLEAN -> LAND (squash-merge, board Done, append STATE, "
    "bump pointer, reap whole). (3) Fork one demand-driven DAG per the priority. Then fan out devops #10-#13 once buildable "
    "(#8 landed trigger). One fork per iteration."
)
tp["fork_token_note"] = (
    "I3-I7 denied the 'fork' token (reconstructed nodes); I8 (#6), I9 (#7), I11 (#5 review), I12 (#6 review), I14 (#7 review), "
    "I15 (#6 relock), I16 (#8 chirp-server), I17 (#9 chirp-frontend) GRANTED + all forks SUCCEEDED. I10, I13, I18, and I19 had "
    "NO fork to make (demand-driven watch-and-schedule iterations). The chain is self-perpetuating (each schedules its successor "
    "BEFORE the atomic action). P1 held on every iteration incl. I19: the overseer read DAG state / PR states (read-only, no build "
    "re-run), forked nothing (nothing foldable/landable/unblocked, no relock due), scheduled its successor, and updated STATE."
)

with open(DST, "w") as f:
    json.dump(s, f, indent=2)

# validate round-trip
with open(DST) as f:
    json.load(f)

print("WROTE", DST)
print("iterations:", [it["iteration"] for it in s["iterations"]])
print("current_pointer:", s["current_pointer"], "work_items:", len(s["work_items"]))
