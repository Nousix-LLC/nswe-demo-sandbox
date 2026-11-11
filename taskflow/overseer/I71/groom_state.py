import json, datetime

SRC = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I70/project_state.json"
DST = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I71/project_state.json"

d = json.load(open(SRC))
now = "2026-10-27T21:10:00Z"
d["updated"] = now
d["current_pointer"] = "overseer/I71"

# --- Record the groomed placements under the persist goal (epic #56) in followup_issues ---
fu = d["engagement"]["followup_issues"]
fu["115"] = ("PR #113 review follow-up (durable persistence, epic #56): no required CI gate runs the durable-store "
             "proofs + drill default run overstates coverage. labels devops/review/type:chore + priority:high. "
             "Board Todo under #56, linked PR #113, refs #65/#67. GROOMED I71: priority:high (most load-bearing in "
             "the batch; real post-merge regression risk). Rank 1 of the batch.")
fu["116"] = ("PR #113 review follow-up (epic #56): two suspected durable-concurrency hazards (delete-vs-edge count "
             "drift COR-02; reciprocal-follow deadlock COR-03), each blocker-class for #65 if reproduced; both "
             "uncovered by the suite. labels bug/app/review + priority:high. Board Todo under #56, linked PR #113, "
             "refs #65. GROOMED I71: priority:high (correctness). Rank 2.")
fu["117"] = ("PR #113 review follow-up (epic #56): reclaim sweep has two sources of truth (CronJob raw SQL duplicates "
             "+ bypasses the ChirpRepository seam; failing sweep unobservable). labels devops/review. Board Todo under "
             "#56, linked PR #113, refs #67/#90. GROOMED I71: medium (drift risk, not current divergence). Rank 4.")
fu["118"] = ("PR #113 review follow-up (epic #56): persistence-layer docs describe implemented methods as stubs + "
             "feature-gating doc hygiene. labels documentation/review. Board Todo under #56, linked PR #113, refs "
             "#66/#110. GROOMED I71: the doc-LINK items (in_memory.rs:787 public->private — the CI-01 `doc` blocker — "
             "plus export.rs:7 gated-link and stale-scaffold rustdoc) are being cleared by remediation #1 in flight on "
             "work/epic-persist as part of landing PR #113; posted a grooming comment on #118 marking them addressed "
             "there so they are NOT double-worked, and to re-check/close them on land. Residual backlog = doc-HYGIENE "
             "that does not gate `doc` (false scaffold narrative, leaked work-breakdown vocab, dead FollowRow/LikeRow, "
             "error.rs header, hypothetical-store seam docs, moral-tone adjectives->#110). Rank 6 (residual is low; "
             "doc-link part owned by the remediation).")
fu["119"] = ("PR #113 review follow-up (epic #56): deployment & activation coherence (committed manifests cite absent "
             "scaffolding paths; 'visibly not-ready' overstates post-merge state; activation needs digest pin AND "
             "out-of-band credential Secret). labels devops/review. Board Todo under #56, linked PR #113, refs #64. "
             "GROOMED I71: medium (mostly comment/doc accuracy; relates to #64 which stays open until activation). Rank 5.")
fu["120"] = ("PR #113 review follow-up (epic #56): persistence security follow-ups (plaintext login secret at rest + "
             "non-constant-time verify -> route through a salted KDF + constant-time compare; in-cluster DB traffic "
             "unencrypted, PGSSLMODE disable -> require TLS). labels app/review + priority:high. Board Todo under #56, "
             "linked PR #113, refs #66/#83/#47/#101. GROOMED I71: priority:high (security; close before production "
             "credentials flow). Deferred to the identity/trust epic #83/#47 by design; no change required in PR #113. "
             "Not an exploitable-on-public finding (credential is out-of-band/uncommitted/unlogged; review's blocking "
             "security bar not met) -> open issue is correct routing, no private advisory owed. Rank 3.")
fu["121"] = ("PR #113 review follow-up (epic #56): minor correctness/schema/idiom polish on the durable store "
             "(restart-id proof via fresh pool; remove_chirp advertises unused Forbidden; single-writer rests on "
             "replicas:1 with no hard guard; sessions.expires_at nullable; fail-closed proven at substrate not "
             "end-to-end; capacity classification non-uniform; capacity 500 vs 503; #66 caps at seam not /api surface). "
             "labels app/review. Board Todo under #56, linked PR #113, refs #65/#66/#67. GROOMED I71: low (polish/nits; "
             "none defeats an acceptance criterion). Rank 7 (bottom of the batch).")

# --- The grooming record ---
d["grooming_i71"] = {
    "groomed_by": "overseer/I71",
    "groomed_at": now,
    "scope": "PR #113 review non-blocking follow-ups #115-#121, board NSWE Delivery (#1), all under epic #56.",
    "trigger": "Board absorbed a batch of new issues (I68 reconciled #115-#121 onto the board under #56, linked to PR #113).",
    "de_duplication": {
        "result": "No merges. The seven are a cleanly partitioned batch by concern (CI/proofs=115, concurrency=116, "
                  "sweep-source-of-truth=117, docs=118, deployment=119, security=120, polish=121) with no twins among "
                  "them and no twin of any pre-existing board issue. Each extends/links the related item rather than "
                  "duplicating it: #116->#65, #117->#67/#90, #118->#66/#110, #119->#64, #120->#83/#47/#101, #121->#65/#66/#67.",
        "118_remediation_crosslink": "#118's doc-LINK items are being cleared by remediation #1 (in flight on "
                  "work/epic-persist) as part of landing PR #113; posted grooming comment "
                  "https://github.com/Nousix-LLC/nswe-demo/issues/118#issuecomment-6453537144 so they are not "
                  "double-worked and are re-checked/closed on land. Already board-linked to PR #113 (no body rewrite needed)."
    },
    "ordering": {
        "mechanism": "This is a 3-status board (Todo/In Progress/Done) with no priority field; backlog order expressed "
                     "via the project's one severity label priority:high (correctness/security/load-bearing ahead of "
                     "medium and polish), plus the rank recorded per-issue in followup_issues.",
        "priority_high_added": [115, 116, 120],
        "rank": {"115": 1, "116": 2, "120": 3, "117": 4, "119": 5, "118": 6, "121": 7},
        "rationale": "Correctness (#116) and security (#120) and the load-bearing CI-enforcement gap (#115) rank above "
                     "the medium drift/coherence items (#117,#119) and the doc-hygiene residual (#118) and the polish "
                     "nits (#121), per the brief (#116 and #120 above #121's polish)."
    },
    "acceptance_criteria_refresh": "No staleness to correct: nothing from epic #56 has landed yet (PR #113 OPEN, "
                  "MERGEABLE, head still 09fa453, remediation #1 in flight, not pushed). Each issue pins the review SHA "
                  "09fa453 as evidence and states acceptance refs + 'what would satisfy' (outcome-described). Criteria "
                  "are current; re-check #118's doc-link items when PR #113 lands.",
    "readability": "Confirmed clean for repository readers: all citations are repo-relative (crates/..., deploy/..., "
                  ".github/workflows/ci.yml), outcome-described with 'what would satisfy', suggested directions not "
                  "recipes, no host/system/taskflow details. (The SUBTASK_* strings named inside #118/#119 are the "
                  "FINDING — leaked work-breakdown vocabulary in committed source/manifests that must be removed — not a "
                  "leak by the board.) No body edits needed.",
    "board_state_after": "All seven remain board items under epic #56 at status Todo; #115/#116/#120 now priority:high; "
                  "#118 carries the remediation cross-link comment. GitHub writes this iteration: 3 label adds + 1 comment. "
                  "P1 held (board work, no code, no DAG).",
    "authoritative_state": "taskflow/overseer/I71/project_state.json (supersedes I70's)."
}

json.dump(d, open(DST, "w"), indent=1)
print("wrote", DST)
print("followup_issues keys:", sorted(d["engagement"]["followup_issues"].keys(), key=lambda x:int(x)))
print("grooming_i71.ordering.rank:", d["grooming_i71"]["ordering"]["rank"])
