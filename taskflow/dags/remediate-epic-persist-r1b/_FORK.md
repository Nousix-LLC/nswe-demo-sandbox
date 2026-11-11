owner_id: overseer/I69
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/remediate-epic-persist-r1b/SYNTHESIS.md
disposition: reap-whole-after-land
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

# Fork hub — remediate-epic-persist-r1b

Remediation round **1** (budget 2) of PR #113 ("Durable PostgreSQL persistence for chirp", `work/epic-persist`
→ `main`; epic #56 / issues #65, #66, #67; #64 stays open). The PR review verdict was REQUEST-CHANGES with a
single landing blocker: the required `doc` CI check fails under `-D warnings` on a public→`pub(crate)`
intra-doc link (`in_memory.rs:787`). This DAG clears that blocker and the connected documentation /
feature-gating doc hazards grouped in issue #118, on `work/epic-persist`, without re-architecting the durable
store (the implementation is sound per the review).

- **Kind:** code remediation. Runs as `swe-coder`.
- **Owner:** the NSWE project overseer thread (`overseer`), launched this fork at iteration **I69**.
- **Re-drive note:** this supersedes the dead orphan `remediate-epic-persist-r1` (forked by a superseded chain
  node, frozen mid-assessment, produced no verdict and pushed nothing; reconciled dead and released to the
  reaper). This is therefore the first remediation attempt that will produce a result — attempt #1 of 2.
- **Observation seam:** the root `SYNTHESIS.md` above — the overseer reads only that folded root verdict, never
  a subtask synthesis or a posted side effect, and never polls the DAG while it runs.
- **Disposition:** `reap-whole-after-land` — scratch; reaped whole once its residue (commits updating PR #113)
  has landed or been recorded. A failed attempt's lesson goes into the next DAG's brief; the deliberation is
  dropped.
- **Re-entry on fold:** the machine gate — a later board check / fold read routes this root `SYNTHESIS.md`
  (PASS → re-review of PR #113; FAIL → remediation #2, the last automatic attempt, then escalate).
- The task spec is in `_BRIEF.md` at this root. Methodology selection belongs to the DAG; none is named here.
