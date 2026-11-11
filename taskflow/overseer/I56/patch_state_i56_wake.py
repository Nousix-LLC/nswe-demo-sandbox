#!/usr/bin/env python3
"""I56 reconstructed-wake reconciliation patch.
Reconciles STATE against the OBSERVED live world (GitHub), records the
reconstruction anomaly as an escalation, and marks design-chirp-r1 superseded.
Only observed facts are recorded; nothing is fabricated. STATE is local-only
(never GitHub)."""
import json, datetime, shutil

NOW = "2026-10-22T00:40:00Z"
p = "project_state.json"
s = json.load(open(p))
shutil.copy(p, "project_state.pre_i56wake.json")  # snapshot prior version

s["updated"] = NOW
s["status"] = "blocked-on-user"

# main_head: reflect OBSERVED live truth; keep the stale local-snapshot value noted.
s["main_head_local_snapshot"] = s.get("main_head")
s["main_head"] = "276138f"  # observed live HEAD 2026-10-14T03:33:23Z

# Honest record of what this reconstructed wake OBSERVED on the live world.
s["reconstruction_reconciliation"] = {
    "observed_at": NOW,
    "by": "overseer/I56 (reconstructed/woken by schedule timer; mechanical wake CONTINUE.md actual_fired_at 2026-10-22T00:36:05Z)",
    "summary": ("Local persisted taskflow/STATE is a STALE Oct-9 snapshot; the live "
                "repository Nousix-LLC/nswe-demo is ~12 days / dozens of issues AHEAD."),
    "observed_live_world": {
        "main_head": "276138f (2026-10-14T03:33:23Z)",
        "product_design_LANDED": "commit ab824a5 (2026-10-13) 'design(chirp-r1): the product design and release bar for a releasable chirp (#33)' — the design + release bar my design-chirp-r1 DAG was forked to produce ALREADY LANDED.",
        "design_backlog_on_board": "EPICs #53/#72/#77/#83/#89/#90; BAR-* release-bar issues #99-#108; feature issues #63-#98 (identity/auth/sessions, account lifecycle, accessibility, persistence, observability).",
        "open_pr": "#113 'Durable PostgreSQL persistence for chirp' on work/epic-persist (OPEN, mergeable=MERGEABLE, mergeState=UNSTABLE, reviewDecision=none, updated 2026-10-14).",
        "fresh_owner_directive": "#114 'Directive: design and build Ferric to a 1.0 framework, with server-side rendering' by mattsmcknight, 2026-10-21T21:00:37Z (OPEN, 0 comments) — unaddressed.",
        "language_sweep_directives": "#109/#111 (project-voice cleanup).",
        "activity": "Repo idle on commits since 2026-10-14; no competing agent observed actively pushing. Owner steers via board issues (#26, #114).",
    },
    "local_vs_live_divergence": ("My overseer chain tail is I56 (suspended 2026-10-09), I57 scheduled+ineligible; "
                                 "local main_head c805525. No local overseer iteration or DAG produced the Oct-12..21 "
                                 "GitHub advancement. The live repo advanced beyond this taskflow snapshot."),
    "zombie_dag": ("design-chirp-r1 (forked by this I56 on 2026-10-10) is REDUNDANT: the design it would produce "
                   "already landed as #33/ab824a5. Reconstruction re-dispatched it at 2026-10-22T00:36:05Z and it is "
                   "RUNNING leaf tasks (SUBTASK_product_requirements/SUBTASK_product_definition Running @ 00:38:38Z). "
                   "If it runs to completion it will open a duplicate design PR and file duplicate epics/BAR issues, "
                   "polluting the live board. A thread actor has no Tier-1 tool to terminate a running forked DAG "
                   "(engine_cancel_taskflow is Session-tier; amend cannot reach into a DAG). Cannot be safely stopped from here."),
}

# Design record: reflect that the design LANDED (observed via #33/ab824a5), and mark the local DAG superseded.
d = s.get("design") or {}
d["location"] = "landed in-repo via #33 (commit ab824a5, 2026-10-13); exact design-doc path and release-bar text TO BE RECONCILED by reading the landed tree (not yet read this wake)"
d["commit"] = "ab824a5"
d["release_bar"] = "established by #33 (BAR-* issues #99-#108 on the board); exact text to be reconciled"
for dd in d.get("design_dags", []):
    if dd.get("slug") == "design-chirp-r1":
        dd["outcome"] = ("SUPERSEDED — redundant. The design it was forked to produce already landed as #33/ab824a5 "
                         "(2026-10-13). The local DAG never folded on disk (no root SYNTHESIS.md, no leaf COMPLETE.md) "
                         "and was re-dispatched by reconstruction at 2026-10-22T00:36:05Z; now a running zombie. "
                         "Must be reaped/neutralized (user adjudication) rather than allowed to duplicate-write to GitHub.")
        dd["folded_at"] = None
s["design"] = d

# New escalation: the reconstruction anomaly (system-level; NOT filed on GitHub — host/taskflow internals).
esc = s.get("escalations", [])
esc.append({
    "what": ("Reconstruction anomaly: the persisted taskflow/STATE snapshot (overseer at I56, 2026-10-09; "
             "design-chirp-r1 just forked) is badly diverged from the far-ahead live repository (design already "
             "landed as #33 on 2026-10-13; board dozens of issues ahead; main 276138f; fresh directive #114). "
             "The in-flight design-chirp-r1 DAG is now redundant and, if left running, will duplicate already-landed "
             "design work on the live board; a thread actor has no safe tool to terminate a running forked DAG."),
    "why": ("Resuming autonomous supervision off this inconsistent base risks duplicate/conflicting writes to the "
            "live repository. The inconsistency is system-level (stale local snapshot vs. advanced live repo + an "
            "unstoppable redundant DAG) and cannot be put on GitHub (host/taskflow internals) or self-healed with "
            "thread-level tools. Only the user can adjudicate how to reconcile."),
    "asked_where": "overseer terminal record (SUSPENSION.md) + STATE blocked-on-user. NOT filed on GitHub (system-level, not a repository fact).",
    "clearing_condition": ("User adjudicates: e.g. (a) reap/neutralize the redundant design-chirp-r1 DAG and re-home "
                           "the overseer onto the live repository state (full board re-derivation from GitHub), or "
                           "(b) direct otherwise. Each bounded wake re-tests the live world (the owner may answer by "
                           "acting — closing/relabelling, pushing, or commenting)."),
    "raised_at": NOW,
    "last_checked_at": NOW,
    "resolved_at": None,
    "evidence": None,
})
s["escalations"] = esc

s["backlog_assessment"] = {
    "assessed_at": NOW,
    "note": ("RECONSTRUCTED WAKE re-eval on fresh clock 2026-10-22T00:38Z. Design DAG design-chirp-r1 re-evaluated: "
             "ALIVE/running leaves after recovery (not frozen), but REDUNDANT — the product design + release bar it "
             "was forked to produce already LANDED on the live repo as #33/commit ab824a5 (2026-10-13). Live board is "
             "~12 days ahead of this stale local snapshot: EPICs #53/#72/#77/#83/#89/#90, BAR-* #99-#108, feature "
             "issues #63-#98, open PR #113 (persistence), fresh owner directive #114 (Ferric 1.0 + SSR). ESCALATED to "
             "the user: local taskflow/STATE diverged from the far-ahead live repo + an unstoppable redundant DAG in "
             "flight. Project kept OPEN (engagement not done — #114 is a large new goal); NOT Exit. No GitHub writes, "
             "no code, no fork this wake (P1 + fork token already spent on design-chirp-r1)."),
}
s["current_focus"] = ("BLOCKED-ON-USER (reconstruction anomaly). I56 reconstructed/woken by schedule timer; found the "
                      "live repo far ahead of the stale local snapshot and the in-flight design-chirp-r1 DAG redundant "
                      "(design already landed as #33). Escalated for user adjudication. Self-suspended on a bounded "
                      "any_of wake (schedule re-check OR design-chirp-r1 terminal); each wake re-tests the live world. "
                      "I57 (depends_on I56) stays ineligible until I56 reaches continue. No fork, no re-schedule of I57, "
                      "no GitHub writes this wake.")

json.dump(s, open(p, "w"), indent=1)
print("STATE patched OK. updated=", s["updated"], "status=", s["status"], "escalations=", len(s["escalations"]))
print("design.commit=", s["design"]["commit"], " main_head=", s["main_head"], " (local snapshot was", s["main_head_local_snapshot"], ")")
