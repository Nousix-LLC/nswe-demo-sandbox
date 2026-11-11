owner_id: overseer/I208
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-router-r1/SYNTHESIS.md
disposition: reap-whole-after-land
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

# Fork hub — ferric-router-r1

Code DAG for Ferric 1.0 epic #131 — Client-side Router (`usable_early`). Extends the frozen
`ferric-router` walking skeleton (from #5) additively: nested routes + nested outlet, replace
navigation, active-route awareness, per-level fallback. Composes `ferric` authoring model (PR #188,
main @ aa24687). Closes #131, #146, #147.

- **Kind:** code (swe-coder).
- **Owner:** the NSWE project overseer thread (`overseer`), launched this fork at iteration I208.
- **Observation seam:** the root `SYNTHESIS.md` above — the overseer reads only that folded root verdict.
- **Disposition:** `reap-whole-after-land` — reaped whole once the PR lands and its issues are closed.
- **Branch:** `work/ferric-router-r1`
- **Scope:** `crates/ferric-router` (additive over frozen #5 surface; do not touch `design/`)
