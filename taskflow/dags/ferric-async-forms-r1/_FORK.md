owner_id: overseer/I207
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-async-forms-r1/SYNTHESIS.md
disposition: reap-whole-after-land
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

# Fork hub — ferric-async-forms-r1

Code DAG for Ferric 1.0 epic #130 — Async, Forms, and Events (`usable_early`). Implements async
resources + suspense, full DOM event handling, and two-way form binding on top of the Authoring
Model (PR #188, main @ aa24687). Closes #130, #143, #144, #145.

- **Kind:** code (swe-coder).
- **Owner:** the NSWE project overseer thread (`overseer`), launched this fork at iteration I207.
- **Observation seam:** the root `SYNTHESIS.md` above — the overseer reads only that folded root verdict.
- **Disposition:** `reap-whole-after-land` — reaped whole once the PR lands and its issues are closed.
- **Branch:** `work/ferric-async-forms-r1`
- **Scope:** `crates/ferric` (additive over authoring model; do not touch `design/`)
