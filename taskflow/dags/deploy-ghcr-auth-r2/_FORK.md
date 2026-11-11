# _FORK.md — deploy-ghcr-auth-r2 (thread fork hub)

owner_id: overseer/I54
forked_by: overseer/I54
thread_type: dag
launch_agent: swe-coder
launch_kernel: inherit
disposition: reap-whole-after-land
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-ghcr-auth-r2/SYNTHESIS.md
launch_context: { application: software, model_default: claude-opus-4-8 }

## Context
Devops DAG, F1 deploy **attempt #2 of 2**: verify and complete the live reachability of Chirp on its committed
image for `Nousix-LLC/nswe-demo`, and reconcile the running cluster with the committed GitOps desired state.
Released now because the owner acted directly on reachability (commit `c805525`, host-less ingress) and the
prior escalation issue was closed; this attempt tests the live world fresh rather than retrying the old
blocked credential path. The full task spec, inputs, acceptance criteria (issue #32), concerns, declared
output, and constraints are in this directory's `_BRIEF.md`.

## Reap policy
`reap-whole-after-land`: scratch DAG, reaped whole once its residue has landed or been recorded by the
overseer (its PR merged or its verdict folded into STATE). The lesson from a failed/blocked attempt goes into
the next DAG's brief; the deliberation is dropped. Never reaped piecemeal while live.
