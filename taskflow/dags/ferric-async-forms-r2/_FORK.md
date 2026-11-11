owner_id: overseer/I210
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-async-forms-r2/SYNTHESIS.md
disposition: reap-whole-after-land
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

# Fork hub — ferric-async-forms-r2

Remediation code DAG (attempt 2 of 2) for Ferric 1.0 epic #130 — Async, Forms, and Events
(`usable_early`). Prior attempt (ferric-async-forms-r1) failed the machine gate: PR was opened in
`Nousix-LLC/ferric` (wrong repo) instead of `Nousix-LLC/nswe-demo`, and no CI ran. This DAG
examines the prior commits, ports/corrects the implementation into `Nousix-LLC/nswe-demo`, and
ensures all 6 CI jobs PASS. Closes #130, #143, #144, #145.

- **Kind:** code remediation (swe-coder).
- **Owner:** the NSWE project overseer thread (`overseer`), launched this fork at iteration I210.
- **Observation seam:** the root `SYNTHESIS.md` above — the overseer reads only that folded root verdict.
- **Disposition:** `reap-whole-after-land` — reaped whole once the PR lands and its issues are closed.
- **Branch:** `work/ferric-async-forms-r2`
- **Scope:** `crates/ferric` in `Nousix-LLC/nswe-demo` (additive over PR #188 surface at aa24687; do not touch `design/`)
- **Lesson carried:** prior attempt created PR in `Nousix-LLC/ferric` (not nswe-demo); CI never ran.
