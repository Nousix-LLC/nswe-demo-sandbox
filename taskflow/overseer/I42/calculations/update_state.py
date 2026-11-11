#!/usr/bin/env python3
"""I42 STATE transform: load I41 copy, apply this iteration's facts, write I42 copy.
Overseer bookkeeping only (no repo code touched). Deterministic; round-trip validated."""
import json, copy

SRC = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I41/project_state.json"
DST = "/home/user/nousix-runtime/nswe-demo/taskflow/overseer/I42/project_state.json"
NOW = "2026-10-07T06:47:00Z"
LAND_SHA = "7a81849f7912d3ef3b9ca63b1287bda7f17e61c9"

with open(SRC) as f:
    s = json.load(f)

# --- top-level ---
s["updated"] = NOW
s["current_pointer"] = 7

dags = {d["item_slug"]: d for d in s["dispatched_dags"]}

# --- #10 infra-bootstrap: LANDED this iteration ---
d = dags["infra-bootstrap"]
d["status"] = "landed-and-reaped"
d["landed_by"] = "overseer/I42"
d["landed_commit"] = LAND_SHA
d["review"] = {
    "verdict": "APPROVE",
    "reviewed_by_dag": "review-infra-bootstrap",
    "reviews_pr": 20,
    "gated_by": "overseer/I42",
    "synthesis": "/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-infra-bootstrap/SYNTHESIS.md",
    "note": ("review-infra-bootstrap folded AUTHORITATIVE APPROVE (06:42:27Z): 0 block; 1 major CORR-1 "
             "explicitly adjudicated carry-as-tracked-follow-up (native-mode k3s pin silently dropped; NOT on the "
             "proven k3d deliverable, NOT land-blocking); 8 minor + 7 nit hardening; 4/4 acceptance PASS; "
             "k3d-vs-native substitution ruled ACCEPTABLE (genuine k3s, identical pin, readiness proven, caveat "
             "honest/complete, downstream #12/#13 targetable); F1 carry-as-tracked-issue. gh review posted COMMENTED "
             "(self-review block); authoritative verdict in SYNTHESIS.md body (gotcha g/i).")
}
d["note"] = d.get("note", "") + (
    " | I42 LANDED #10: review-infra-bootstrap folded APPROVE + live gh confirmed PR #20 OPEN/MERGEABLE/CLEAN "
    "(head 016bd44 unchanged) -> gh pr merge 20 --squash --delete-branch -> squash commit "
    + LAND_SHA + " on main, PR #20 MERGED @ 2026-10-07T06:45:08Z, issue #10 CLOSED + board Done, current_pointer 6->7. "
    "Sibling PRs #21/#22 re-polled after the land: both OPEN/MERGEABLE/CLEAN (no restale - #10 touched deploy/bootstrap/ "
    "only, no Cargo.lock). Filed the review's non-blocking follow-ups as tracked issues #23 (native-install-path harden) "
    "and #24 (ArgoCD RBAC + supply-chain, pre-#13). Code-DAG infra-bootstrap + review-DAG review-infra-bootstrap reaped "
    "whole (scratch). P1 held (mechanical squash-merge, no code touched).")

# --- review-infra-bootstrap: folded APPROVE, reaped ---
d = dags["review-infra-bootstrap"]
d["status"] = "folded-and-reaped"
d["verdict"] = "APPROVE"
d["gated_by"] = "overseer/I42"
d["reaped_by"] = "overseer/I42"
d["note"] = d.get("note", "") + (
    " | I42: FOLDED AUTHORITATIVE APPROVE (root SYNTHESIS.md 06:42:27Z; identities R1-R7 all PASS, review-only R7 "
    "confirmed; 0 block, 1 major CORR-1 carry-as-follow-up, 8 minor + 7 nit; 4/4 AC PASS; k3d ACCEPTABLE; F1 "
    "carry-as-tracked-issue). I42 gated the land on this root body -> LANDED #10 (squash " + LAND_SHA + "). "
    "Non-blocking follow-ups filed as issues #23/#24. Reaped whole after land (scratch).")

# --- #11 ci-actions: folded machine-PASS, awaiting review ---
d = dags["ci-actions"]
d["status"] = "folded-machine-PASS-awaiting-review"
d["pr"] = 21
d["folded_at"] = "2026-10-07T06:28:37Z"
d["machine_gate"] = {
    "verdict": "PASS",
    "round": 1,
    "decompose_evaluation": "Atomic",
    "pr": 21,
    "head": "c8123376ca1794c0b0466f41a1204bf3c3301b16",
    "synthesis": "/home/user/nousix-runtime/nswe-demo/taskflow/dags/ci-actions/SYNTHESIS.md",
    "gated_by": "overseer/I42 (machine gate read, not re-run)",
    "note": ("ci-actions folded Atomic machine-PASS (SYNTHESIS.md 06:28:37Z + COMPLETE.md). .github/workflows/ci.yml: "
             "fmt, clippy -D warnings, test (14 suites/207 tests), wasm build+bindgen, doc -D warnings (required-check "
             "candidates) + main-push-only GHCR image job; verified locally AND in the real runner (Actions run 37581289276, "
             "~2m20s); self-validated on PR #21. Folds the deferred #8-review minors CRQ-02/F2 (79 rustdoc intra-doc-link "
             "errors resolved, doc comments only, zero logic lines) and CRQ-01 (README 422->400 VALIDATION_ERROR row; F1 "
             "already fixed in code at 714d50f). HONEST ORDERING: the image job is gated on ./Dockerfile presence - a "
             "green-but-no-op on main until #12 lands, then auto-builds ghcr.io/nousix-llc/chirp-server with no ci.yml edit. "
             "Repo-admin follow-ups flagged (NOT applied): adopt fmt/clippy/test/wasm/doc as required status checks; set GHCR "
             "package visibility post-#12; MSRV-vs-locked-deps (manifest rust-version 1.82 but locked graph needs 1.97, CI "
             "pins 1.97). PR #21 OPEN/MERGEABLE/CLEAN, Closes #11.")
}
d["note"] = d.get("note", "") + (
    " | I42 recon: #11 FOLDED Atomic machine-PASS (PR #21 OPEN/MERGEABLE/CLEAN, head c812337). Needs a review DAG before "
    "it can land (nothing lands unreviewed). I42's one fork went to review-containerize (#12, on #13's critical path); "
    "#11's review (review-ci-actions) is I43's priority-2 fork. Still In Progress on the board.")

# --- #12 containerize: folded machine-PASS, review dispatched this iteration ---
d = dags["containerize"]
d["status"] = "folded-machine-PASS-review-dispatched"
d["pr"] = 22
d["folded_at"] = "2026-10-07T06:38:38Z"
d["review_dag"] = "review-containerize (forked I42)"
d["machine_gate"] = {
    "verdict": "PASS",
    "round": 1,
    "decompose_evaluation": "Atomic",
    "pr": 22,
    "head": "bc0c3c0d6380c9edd1b9433addc7fdcbffb55751",
    "synthesis": "/home/user/nousix-runtime/nswe-demo/taskflow/dags/containerize/SYNTHESIS.md",
    "gated_by": "overseer/I42 (machine gate read, not re-run)",
    "note": ("containerize folded machine-PASS (SYNTHESIS.md 06:38:38Z). Multi-stage Dockerfile (builder rust:1.88-slim-"
             "bookworm -> runtime gcr.io/distroless/cc-debian12:nonroot) building the release server AND the wasm SPA bundle; "
             "image chirp:local 41.7 MB, linux/amd64, USER 65532:65532 non-root; base images pinned by tag + @sha256 digest; "
             "all cargo builds --locked; wasm-bindgen-cli 0.2.129 matched to Cargo.lock. Built AND run locally: /healthz->200, "
             "SPA + client-route fallback + /pkg/*.wasm (application/wasm) + POST /api/users->201 all served; Docker HEALTHCHECK "
             "healthy; docker stop (SIGTERM) exits 0 (minimal main.rs SIGTERM branch added, unix-gated, no API change; "
             "fmt/clippy -D warnings/20 tests green after). 9/9 acceptance checked. Deliverables: Dockerfile, .dockerignore, "
             "deploy/docker/healthcheck.rs, deploy/README.md, README container section, chirp-server/src/main.rs SIGTERM. "
             "Scope honored (no CI/#11, no k8s/#13, no live push). PR #22 OPEN/MERGEABLE/CLEAN, Closes #12.")
}
d["note"] = d.get("note", "") + (
    " | I42 recon: #12 FOLDED machine-PASS (PR #22 OPEN/MERGEABLE/CLEAN, head bc0c3c0d). #12 is on #13's critical path "
    "(#13 blocked until #10+#12 land; #10 landed this iteration). I42 forked ONE review DAG review-containerize (the one fork, "
    "ladder priority-2, dependency-ordered ahead of #11's review). Does NOT land unreviewed. Still In Progress on the board.")

# --- new dispatched_dags entry: review-containerize ---
s["dispatched_dags"].append({
    "item_slug": "review-containerize",
    "issue": 12,
    "kind": "review",
    "reviews_pr": 22,
    "reviews_head": "bc0c3c0d6380c9edd1b9433addc7fdcbffb55751",
    "persona": "swe-coder",
    "model": "claude-opus-4-8",
    "workspace": "/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-containerize",
    "dispatched_at": NOW,
    "dispatched_by": "overseer/I42",
    "forked_thread_id": "review-containerize",
    "placement": "peer",
    "status": "dispatched-running",
    "note": ("I42's one demand-driven fork (ladder priority-2: #12 folded machine-PASS, PR #22 OPEN/MERGEABLE/CLEAN, no "
             "review DAG yet; chosen ahead of #11's review because #12 is on #13's critical path - #13 blocked until #10+#12 "
             "land, #10 landed this iteration). Review DAG for PR #22 (containerize #12, devops EPIC #3). Concerns named in "
             "_BRIEF.md (DAG selects/loads its own bundles, gotcha b): Dockerfile build correctness & reproducibility; runtime "
             "image hygiene & size; container security posture (non-root, no baked secrets, least privilege, supply-chain/"
             "dependency trust boundary); operability (/healthz healthcheck, configurable bind/asset-path, stdout logging); "
             "correctness of the minimal main.rs SIGTERM change; code quality & idiom; testing/verification depth; infra-#12-only "
             "scope conformance. _FORK.md flat-key schema (owner_id overseer/I42, observation_seam .../review-containerize/"
             "SYNTHESIS.md, disposition reap-whole-after-land, launch_agent swe-coder, launch_kernel inherit, thread_type dag, "
             "launch_context identity-only). Fork SUCCEEDED first attempt (status=forked, placement=peer). Renders the "
             "authoritative APPROVE/REQUEST-CHANGES verdict in its root SYNTHESIS.md (overseer gates the #12 land on THAT, not "
             "gh review state nor the machine gate alone - gate_on_synthesis_not_review_body). I43 watches review-containerize "
             "fold -> APPROVE + PR #22 OPEN/MERGEABLE/CLEAN => LAND #12 (then #13 unblocked); REQUEST-CHANGES => remediation DAG "
             "(budget 2, then escalate). Scratch: reaped whole once #12 lands.")
})

# --- work_items: append #10 ---
s["work_items"].append({
    "item_slug": "infra-bootstrap",
    "issue": 10,
    "pr": 20,
    "acceptance_criteria": ("AC1 k3s cluster installed & proven Ready with exact versions recorded; AC2 ArgoCD in its own "
        "namespace proven healthy, access runtime-retrieved + rotate/delete documented, never staged; AC3 wasm target + "
        "wasm-bindgen CLI set up & PROVEN by building to pkg/*.wasm (CLI==crate 0.2.129); AC4 unified README with run order + "
        "per-track verification, idempotent/re-runnable/version-pinned/no secrets. Infra-only (no #12 containerize, no #13 "
        "deploy manifests/ArgoCD Application)."),
    "landed_commit_shas": [LAND_SHA],
    "diff_summary": ("+912/-0 across 11 files under deploy/bootstrap/ (k3s + ArgoCD install/verify shell scripts, wasm build "
        "script, unified runbook README). Squash commit 7a81849 (PR #20). Infra-only; no app crate touched."),
    "dag_decision_record": ("Decomposed into cluster_k3s + wasm_toolchain + gitops_argocd spokes + synthesis_gate. Native "
        "systemd k3s install cannot run on the rootless sandbox (uid 1001, no non-interactive sudo) -> install-k3s.sh "
        "auto-selected a genuine k3d-hosted k3s cluster (Rancher k3s-in-Docker, same distribution, identical pinned "
        "v1.35.5+k3s1), proven Ready via kubectl wait + CoreDNS gate (fails closed) - NO BLOCKED criterion. ArgoCD isolated in "
        "argocd ns with closed-by-default ClusterIP + NetworkPolicies, proven healthy, admin pw + kubeconfig runtime-retrieved. "
        "wasm proven by a real cargo build --target wasm32-unknown-unknown + wasm-bindgen asserting pkg/chirp.js + chirp_bg.wasm "
        "(0061736d magic header), CLI==crate==0.2.129. Four-check model + contract identities I1-I6 all PASS; one minor "
        "non-blocking F1 (contract-wording tension, recorded-not-plugged). Machine gate PASS round 1."),
    "gate_outcome": "approved (machine PASS + review APPROVE; delegated landing authority, headless engagement)",
    "machine_gate": "PASS (round 1; honest PASS via a proven-Ready genuine k3d-hosted k3s)",
    "review_verdict": ("APPROVE (review-infra-bootstrap root SYNTHESIS.md, gated_by overseer/I42; 0 block; 1 major CORR-1 "
        "adjudicated carry-as-tracked-follow-up [native-mode k3s pin silently dropped - not on the proven deliverable, not "
        "land-blocking]; 8 minor + 7 nit hardening; 4/4 acceptance PASS; k3d substitution ACCEPTABLE; F1 carry-as-tracked-issue; "
        "R1-R7 all PASS incl. review-only R7). gh review COMMENTED (self-review block)."),
    "landed_at": "2026-10-07T06:45:08Z",
    "landed_by": "overseer/I42",
    "compacted": False,
    "land_then_fix_followups": ("Non-blocking review findings filed as tracked issues (honest records; do NOT block any land): "
        "#23 'harden & exercise the native k3s install path' = CORR-1 (major, pass pin inside the privileged shell via "
        "env/--preserve-env) + CORR-2 (assert-not-print the pinned version) + HSO-1 (exercise native systemd path on a privileged "
        "host + provision a durable #13 target cluster) + SEC-1 (native kubeconfig 0600) + housekeeping (CORR-3/HSO-2/nits); "
        "#24 'ArgoCD least-privilege RBAC + supply-chain hardening BEFORE #13 first Application' = SEC-2 (scope the "
        "application-controller ClusterRole off */*/*) + SEC-3 (digest-pin manifest/images, cosign) + SEC-4 (survive a stock "
        "--force-conflicts re-run). #24 gates #13's scope. F1 (internal contract-wording in the now-reaped code DAG's manifest "
        "template) dropped - the artifact is reaped and it has zero repo-code bearing. Both issues added to the board (Todo).")
})

# --- iterations: append I42 ---
s["iterations"].append({
    "iteration": "I42",
    "persona": "swe-lead",
    "evaluation": "Continue",
    "scheduled_successor": "I43",
    "atomic_action": ("Recon (read-only, P1): review-infra-bootstrap FOLDED APPROVE; #11 ci-actions + #12 containerize both "
        "FOLDED machine-PASS (PRs #21/#22); PR #20 re-polled OPEN/MERGEABLE/CLEAN; main @ fcfc7a2. LANDED #10 (gh pr merge 20 "
        "--squash --delete-branch -> squash 7a81849; main fcfc7a2->7a81849; issue #10 CLOSED + board Done; current_pointer 6->7). "
        "Re-polled siblings #21/#22 post-land: both MERGEABLE/CLEAN (no restale). Filed follow-up issues #23/#24 (board Todo). "
        "Forked ONE DAG review-containerize (#12 review, priority-2, #13 critical path). Reaped infra-bootstrap + "
        "review-infra-bootstrap whole."),
    "terminal": "continue"
})

# --- engagement: record the new follow-up issues ---
s["engagement"].setdefault("followup_issues", {})
s["engagement"]["followup_issues"]["23"] = "native k3s install path hardening (from #10 review: CORR-1/CORR-2/HSO-1/SEC-1 + housekeeping) - board Todo, epic #3"
s["engagement"]["followup_issues"]["24"] = "ArgoCD least-privilege RBAC + supply-chain hardening before #13's first Application (SEC-2/SEC-3/SEC-4) - board Todo, epic #3, gates #13 scope"

# --- turn_pointer: rewrite for I42 -> I43 ---
s["turn_pointer"] = {
    "landed": ("App layer (all of #4/#5/#6/#7/#8/#9) COMPLETE on main. DEVOPS: #10 infra-bootstrap -> main @ " + LAND_SHA +
        " (issue #10 Done/CLOSED, I42; PR #20 squash-merged on review APPROVE + CLEAN). Remaining devops: #11/#12 folded "
        "machine-PASS awaiting review+land; #13 blocked."),
    "wave": ("DEVOPS EPIC #3 in flight. #10 infra-bootstrap LANDED (I42). #11 ci-actions FOLDED machine-PASS (PR #21). "
        "#12 containerize FOLDED machine-PASS (PR #22). #13 deploy-argocd BLOCKED until #12 (image) lands (#10 already landed). "
        "Goal: app built+tested, CI green, containerized, deployed on k3s (k3d-hosted) via ArgoCD + reachable, everything merged, "
        "board all Done - then Exit."),
    "running": [
        ("review-containerize (#12 review; forked I42). Reviews PR #22 (containerize, work/containerize->main, head bc0c3c0d, "
         "Closes #12) for Dockerfile build correctness/reproducibility, runtime image hygiene/size, container security posture + "
         "supply-chain trust boundary, operability (/healthz, configurable bind/asset-path, stdout logs), the minimal main.rs "
         "SIGTERM change, code quality/idiom, testing depth, #12-only scope. Folds the authoritative APPROVE/REQUEST-CHANGES "
         "verdict into its root SYNTHESIS.md. I43 gates the #12 land on that verdict. Scratch: reaped once #12 lands."),
        ("ci-actions #11 (forked I39) FOLDED Atomic machine-PASS (SYNTHESIS.md 06:28:37Z + COMPLETE.md). PR #21 "
         "OPEN/MERGEABLE/CLEAN, head c812337, Closes #11. Awaiting a review DAG (nothing lands unreviewed). review-ci-actions is "
         "I43's priority-2 fork (one fork/iteration; I42 spent its fork on review-containerize)."),
        ("containerize #12 (forked I40) FOLDED machine-PASS (SYNTHESIS.md 06:38:38Z). PR #22 OPEN/MERGEABLE/CLEAN, head bc0c3c0d, "
         "Closes #12. Review DAG review-containerize dispatched by I42. On its APPROVE + PR #22 CLEAN, I43+ LANDS #12 -> unblocks #13.")
    ],
    "folded_awaiting_action": [
        ("#11 ci-actions FOLDED machine-PASS (PR #21 CLEAN) - AWAITING a review DAG (review-ci-actions, I43 priority-2 fork), "
         "then gate+LAND on APPROVE + CLEAN."),
        ("#12 containerize FOLDED machine-PASS (PR #22 CLEAN) - review-containerize dispatched (I42). AWAITING its verdict -> on "
         "APPROVE + PR #22 CLEAN, LAND #12 (then re-poll siblings for restale; relock any CONFLICTING via a forked DAG, never "
         "inline). #12 landing unblocks #13.")
    ],
    "fork_pending_next_iterations": ("I43: recon read-only (review-containerize verdict? #11 still CLEAN? re-poll PRs past UNKNOWN; "
        "confirm main @ 7a81849). Ladder (one fork): priority-1 relock (a CONFLICTING sibling next to land) -> priority-2 review "
        "(a folded machine-PASS PR with no review: #11 -> fork review-ci-actions) -> priority-3 remediation (machine-FAIL / "
        "REQUEST-CHANGES, incl. a #12 review REQUEST-CHANGES, budget 2/item) -> priority-4 new work (#13 deploy-argocd, BLOCKED "
        "until #12 lands - #10 already landed). FINISH IN-FLIGHT FIRST: on review-containerize APPROVE + PR #22 CLEAN => LAND #12 "
        "(squash --delete-branch, issue #12 Done, append work_items[], current_pointer 7->8, reap containerize + review-containerize "
        "whole), then re-poll #11 + any sibling for a base/lock restale (relock any genuine CONFLICTING loser via a forked DAG, "
        "never inline, P1). Then fork review-ci-actions for #11 (if not already done). #13 brief must account for issue #24 "
        "(ArgoCD RBAC/supply-chain hardening before the first Application) and NOTE the live cluster is k3d-hosted k3s (#13 targets "
        "it); if the k3d substitution gates a reachable deploy on a durable cluster, weigh escalating to the user before #13. "
        "Never land on UNKNOWN/CONFLICTING. Keep the chain going until app on k3s reachable + CI green + all merged + board Done, "
        "then Exit."),
    "awaiting": ("review-containerize root SYNTHESIS.md verdict (APPROVE/REQUEST-CHANGES) for PR #22 -> the #12 landing gate; a "
        "review DAG for #11 (review-ci-actions, I43 priority-2 fork) -> the #11 landing gate. #13 deploy-argocd BLOCKED until #12 "
        "(image) lands (#10 infra already landed I42). Tracked follow-ups #23 (native-path) + #24 (ArgoCD RBAC/supply-chain, "
        "pre-#13) on the board."),
    "fork_token_note": ("One engine_fork per overseer iteration (gotcha d: PermissionDenied 'missing token fork' for all but the "
        "first, non-retryable). I42 spent its one fork on review-containerize (#12 review). I43 gets a fresh token (priority: #11 "
        "review, unless a higher-ladder relock/land/remediation fires)."),
    "remaining_backlog": ("Devops EPIC #3 only (app layer COMPLETE; #10 infra LANDED I42 @ 7a81849): #11 ci-actions FOLDED "
        "machine-PASS (PR #21 CLEAN, needs review+land); #12 containerize FOLDED machine-PASS (PR #22 CLEAN, review dispatched, "
        "lands on APPROVE); #13 deploy-argocd BLOCKED until #12 lands. Plus tracked follow-up issues #23 (native-path harden) + #24 "
        "(ArgoCD RBAC/supply-chain, pre-#13). Goal: app built+tested, CI green, containerized, deployed on k3s (k3d-hosted) via "
        "ArgoCD + reachable, everything merged, board all Done.")
}

# --- write + round-trip validate ---
with open(DST, "w") as f:
    json.dump(s, f, indent=1, ensure_ascii=False)
with open(DST) as f:
    rt = json.load(f)
assert rt["current_pointer"] == 7
assert rt["dispatched_dags"][-1]["item_slug"] == "review-containerize"
assert rt["work_items"][-1]["issue"] == 10
assert rt["iterations"][-1]["iteration"] == "I42"
assert {d["item_slug"]: d["status"] for d in rt["dispatched_dags"]}["infra-bootstrap"] == "landed-and-reaped"
print("OK wrote", DST)
print("current_pointer:", rt["current_pointer"])
print("dispatched_dags:", len(rt["dispatched_dags"]), "| work_items:", len(rt["work_items"]), "| iterations:", len(rt["iterations"]))
print("infra-bootstrap status:", {d["item_slug"]: d["status"] for d in rt["dispatched_dags"]}["infra-bootstrap"])
print("ci-actions status:", {d["item_slug"]: d["status"] for d in rt["dispatched_dags"]}["ci-actions"])
print("containerize status:", {d["item_slug"]: d["status"] for d in rt["dispatched_dags"]}["containerize"])
