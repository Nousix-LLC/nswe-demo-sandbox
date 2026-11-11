# _FORK.md — review-deploy-ghcr-auth (fork hub)

owner_id: overseer/I52
forked_thread_id: review-deploy-ghcr-auth
thread_type: dag
kind: review
reviews_pr: 30
issue: 29
launch_agent: swe-coder
launch_kernel: inherit
disposition: reap-whole-after-land
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-deploy-ghcr-auth/SYNTHESIS.md
launch_context: { application: software, model_default: claude-opus-4-8 }
reason: Review gate for PR #30 (docs-only GHCR pull-auth runbook, F1 of #29). Nothing lands unreviewed; this review lets a later overseer iteration land PR #30 on its own merit while the live F1 fix waits on a user-provided read:packages credential.
