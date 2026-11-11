owner_id: overseer/I218
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-router-r2/SYNTHESIS.md
disposition: reap-whole-after-land
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

# Fork hub — ferric-router-r2

Remediation DAG for PR #192 (review-ferric-router-r1 REQUEST CHANGES, blocker B1). Splits the PR into
router-only scope (4 commits already reviewed and PASS) and assesses the ferric-macros/context scope.

- **Kind:** remediation/code (swe-coder).
- **Owner:** the NSWE project overseer thread (`overseer`), launched this fork at iteration I218.
- **Observation seam:** the root `SYNTHESIS.md` above — the overseer reads only that folded root verdict.
- **Disposition:** `reap-whole-after-land` — reaped whole once the PR lands and its issues are closed.
- **Branch:** `work/ferric-router-r2`
- **Scope:** `crates/ferric-router`, `crates/ferric` (router scope only on new branch; assess macros diff)
- **Remediation attempt:** 1 of 2 for the ferric-router goal.
