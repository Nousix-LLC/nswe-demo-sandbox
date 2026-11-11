# _FORK.md — review-update-sweep-digest-r1 (authored by NSWE overseer swe-lead)

## Fork context
owner_id: proc-4d9e0df8-e914-44f3-a071-214bf456e355
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-update-sweep-digest-r1/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-reviewer
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Review of PR #187 (work/update-sweep-digest-r1 → main) — devops digest update pinning the sweep CronJob to the febeb151 build image. Devops DAG update-cronjob-digest-r1 folded PASS (all CI SUCCESS, branch MERGEABLE/CLEAN). This review DAG (swe-reviewer) reviews PR #187 against five concerns in the brief, posts the review on PR #187, and reports findings in SYNTHESIS.md. Landing is under delegated authority (auto_land: true) on APPROVE — the overseer lands after reading the fold.
