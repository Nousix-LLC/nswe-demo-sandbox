# _FORK.md — review-sweep-seam-r1 (authored by NSWE overseer swe-lead)

## Fork context
owner_id: proc-7271abdb-377b-4518-8655-6b2b90d6f586
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-sweep-seam-r1/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-reviewer
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Review of PR #183 (work/sweep-seam-r1 → main) closing issue #117 (replace psql sweep CronJob with chirp-server sweep subcommand). Remediation DAG sweep-seam-r1-r1 folded PASS (all CI SUCCESS, branch MERGEABLE/CLEAN). This review DAG (swe-reviewer) reviews PR #183 against seven concerns in the brief, posts the review on PR #183, and reports findings in SYNTHESIS.md. Landing is under delegated authority (auto_land: true) on APPROVE — the overseer lands after reading the fold.
