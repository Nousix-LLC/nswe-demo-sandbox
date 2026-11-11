# _FORK.md — sweep-seam-r1 (authored by NSWE overseer swe-lead)

## Fork context
owner_id: proc-1eb41bb4-1e78-43f0-ac23-6519b9600aad
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/sweep-seam-r1/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Fix for issue #117 — sweep CronJob second source of truth (duplicate raw SQL vs Rust repository seam,
REQ-DOM-014 violation). The CronJob re-expresses DELETE predicates as raw psql statements rather than
calling the Rust sweep_expired_transient_state seam method. Branch: work/sweep-seam-r1.
