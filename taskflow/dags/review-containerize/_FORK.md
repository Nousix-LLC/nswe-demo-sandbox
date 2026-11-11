# _FORK.md — review-containerize (fork hub)

Fork context, reap policy, and kernel metadata for the review DAG that reviews PR #22 (work-item #12,
`containerize`). The reaper reads this.

owner_id: overseer/I42
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-containerize/SYNTHESIS.md
disposition: reap-whole-after-land
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Context

- **Kind:** review DAG (reviews only; never edits/merges).
- **Reviews:** PR #22 (`work/containerize` → `main`, Closes #12, head `bc0c3c0d`), machine-PASS per
  `taskflow/dags/containerize/SYNTHESIS.md`.
- **Produces:** an authoritative APPROVE / REQUEST-CHANGES verdict in this DAG's root `SYNTHESIS.md`, plus a
  posted review on PR #22.
- **Reap:** scratch — reaped whole once #12 has landed (or the verdict has been acted on). Not retained.
- Methodology is the DAG's own choice (see `_BRIEF.md`); `launch_context` is identity-level only.
