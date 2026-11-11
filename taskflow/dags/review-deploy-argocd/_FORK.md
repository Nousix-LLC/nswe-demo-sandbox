# _FORK.md — review-deploy-argocd (NSWE #13 review DAG fork hub)

owner_id: overseer/I49
forked_thread_id: review-deploy-argocd
thread_type: dag
launch_agent: swe-coder
launch_kernel: inherit
disposition: reap-whole-after-land
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-deploy-argocd/SYNTHESIS.md
launch_context: { application: software, model_default: claude-opus-4-8 }

## Fork context
Review DAG for the #13 deploy-argocd change. Reviews **PR #28** (`work/deploy-argocd` → `main`, head
`63a299a0`, `Closes #13`) — k8s manifests + ArgoCD Application deploying `chirp-server` onto the live k3d k3s
cluster via GitOps. The #13 code DAG folded machine-PASS (gate=PASS, round 1, reachability HTTP 200). Nothing
lands unreviewed; this DAG produces the review gate. Its full task spec is `_BRIEF.md` at this root.

## Reap policy
Scratch, `reap-whole-after-land`: reaped whole once #13 lands (PR #28 merged) or the review's findings are
recorded on the board. The authoritative verdict is this DAG's root `SYNTHESIS.md` body (the posted PR comment
is the GitHub-visible record per the #26 directive; `gh pr review --approve` is blocked for a same-account
author, so the comment — not the gh review state — carries the visible verdict).

## Ownership
Owned and supervised (lifecycle only) by the NSWE project overseer thread `overseer` (this fork by iteration
I49). The overseer observes the `observation_seam` on a bounded wake and routes the fold; it never does the
review's work (P1).
