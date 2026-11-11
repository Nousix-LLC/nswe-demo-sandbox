owner_id: overseer/I187
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-epic-authoring-r1/SYNTHESIS.md
disposition: reap-whole-after-land
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

# Fork hub — ferric-epic-authoring-r1

Code DAG for Ferric 1.0 epic #129 — Authoring Model (`usable_early`). Implements the reactive signals,
virtual DOM, `view!` macro, component model, compile-time diagnostics, and context API specified in
`design/ferric/authoring-model.md` (merged PR #128, now on main). Closes sub-issues #137, #138, #139,
#140, #141, #142.

- **Kind:** code (swe-coder).
- **Owner:** the NSWE project overseer thread (`overseer`), launched this fork at iteration I187.
- **Observation seam:** the root `SYNTHESIS.md` above — the overseer reads only that folded root verdict.
- **Disposition:** `reap-whole-after-land` — reaped whole once the PR lands and its issues are closed.
- **Branch:** `work/ferric-epic-authoring-r1`
- **Scope:** `crates/ferric` only
